#!/usr/bin/env node
// Two-stage, non-scored route qualification. Exactly TWO agy processes, both here:
//   process 1  agy models      (non-inference)  cell qualification-models-list
//   process 2  one synthetic 16-item request D-I001..D-I016 (inference, never scored)
//                                                            cell qualification-synthetic
// There is no `--version` process.
//
// C15: both processes are journaled in the SAME append-only execution/LEDGER.jsonl as the
// execution cells -- one START row before the spawn and one FINISH row after it, in the same
// seven-key row shape. Nothing here reports a process count: every counter is derived from
// those rows (deriveState().agy_processes_spawned / .inference_calls_made). Captures are
// attempt-numbered for auditability, and v4 permits no retry after the first journaled process.
//
// Route identity is the `models` capture naming gemini-3.7-flash-high exactly once
// plus the argv `--model` binding of the synthetic request. The envelope's top-level `model`
// field is an OPTIONAL runtime self-report: real captures do not carry it, so its ABSENCE is
// never a mismatch; a PRESENT and DIFFERENT value is STOP_ROUTE (SPEC 8).
//
// Stage 1 captureQualification() writes only package-local capture bytes, reuse contracts,
// the updated package manifest, and a DRAFT.
// The dispatch is then archived by the task owner, who writes the task-owned
// QUALIFICATION-CAPTURE-RECEIPT.json. Stage 2 finalizeQualification() is PURE: it spawns
// nothing, derives RAW from the captured stdout, and writes qualification/EVIDENCE.json.
// Package code never writes any file under .ai/task/ (C11/C12).
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readCanonical,shaFile,sha256,jsonBytes,writeStable,exactKeys,parseNoDuplicate,hex64,verifyAgyExecutable,validateRouteRelocation,routeRelocation} from './lib.mjs';
import {parseEnvelope,extractAgy} from './parser.mjs';
import {buildRequest} from './request-lib.mjs';
import {checkManifest,manifestSha256,writeManifest,TASK_ID} from './build-manifest.mjs';
import {TASK_DIR,validateGates} from './gates.mjs';
import {deriveState,nextAttempt,appendRow,startRow,finishRow,isoNow,capturePaths,readRows,ledgerLine,LEDGER_PATH,QUALIFICATION_CELLS,PILOT_AGY_PROCESS_CEILING} from './ledger.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),defaultRepo=path.resolve(here,'../../../..');
export const [MODEL_LIST_CELL,SYNTHETIC_CELL]=QUALIFICATION_CELLS;
export const CAPTURE_RECEIPT_PATH=`${TASK_DIR}/QUALIFICATION-CAPTURE-RECEIPT.json`;
export const files={request:'qualification/SYNTHETIC-REQUEST.txt',draft:'qualification/EVIDENCE-DRAFT.json',raw:'qualification/RAW-SYNTHETIC.json',evidence:'qualification/EVIDENCE.json'};
export const REUSE_CONTRACT_PATH='qualification/REUSE-CONTRACT.json';
export const ORIGINAL_CANDIDATE_MANIFEST_SHA256='46816850a059f6af7fe82e8da1d369b690fdd08ac3540c309c86dae5c489e545';
export const ORIGINAL_PACKAGE_REVIEW_GATE_PATH=`${TASK_DIR}/PACKAGE-REVIEW-GATE.json`;
export const ORIGINAL_PACKAGE_REVIEW_GATE_SHA256='9e72ab247d1e34f0b6c1f1841aa1dce3c2fffc04f29d07d5489550646276fcb0';
export const ROUTE_MODEL='gemini-3.7-flash-high';
export const REUSE_CONTRACT_SCHEMA='gemini-context-v5-qualification-reuse-contract-v1';
export const SYNTHETIC_REUSE_CONTRACT_PATH='qualification/SYNTHETIC-REUSE-CONTRACT.json';
export const SYNTHETIC_REUSE_CONTRACT_SCHEMA='gemini-context-v5-qualification-synthetic-reuse-contract-v2';
export const SYNTHETIC_ORIGINAL_CANDIDATE_MANIFEST_SHA256='6de58ccb69ef1de9672b7ca455c6d17c001dca563fb65c992984fd5946536a31';
export const SYNTHETIC_ORIGINAL_PACKAGE_REVIEW_GATE_SHA256='189836ce5aea0f15b958b4dc7dc744e41048eb3a8f611492e43b7406e33fedc2';
const reuseKeys=['attempt','capture','cell','ledger_prefix','original_candidate_manifest_sha256','original_package_review_gate_path','original_package_review_gate_sha256','route','schema_version','task_id'];
const reuseCaptureKeys=['stderr_path','stderr_sha256','stdout_path','stdout_sha256'];
const reuseRouteKeys=['argv','executable','executable_sha256','route_contract_sha256'];
const syntheticReuseKeys=['attempt','capture','cell','ledger_prefix','original_candidate_manifest_sha256','original_package_review_gate_path','original_package_review_gate_sha256','route','schema_version','task_id'];
const syntheticReuseCaptureKeys=reuseCaptureKeys;
const syntheticReuseLedgerPrefixKeys=['path','prefix_sha256','row_count','rows'];
const syntheticReuseRouteKeys=['argv_sha256','executable','executable_sha256','route_contract_sha256'];
const bytes=x=>Buffer.isBuffer(x)?x:Buffer.from(x??'');
function manifestLists(root,rel){try{const m=readCanonical(path.join(root,'MANIFEST.json'));return m.files?.some(x=>x.path===rel&&x.sha256===shaFile(path.join(root,rel)))===true}catch{return false}}
function qualificationCellsAreFirstFour(rows){return rows.length===4&&rows[0]?.cell===MODEL_LIST_CELL&&rows[1]?.cell===MODEL_LIST_CELL&&rows[2]?.cell===SYNTHETIC_CELL&&rows[3]?.cell===SYNTHETIC_CELL&&rows.every(x=>x.attempt===1)}
function captureRouteMatches(root,captured,currentRoute,currentRouteSha,{historical=false}={}){
  const direct=captured?.route_contract_sha256===currentRouteSha&&captured?.executable===currentRoute.cli_contract?.executable&&captured?.executable_sha256===currentRoute.cli_contract?.executable_sha256;
  if(direct&&!historical)return true;
  const relocation=validateRouteRelocation(root,currentRoute);
  return relocation.valid&&captured?.route_contract_sha256===relocation.contract.original_route.sha256&&captured?.executable===relocation.contract.original_executable.path&&captured?.executable_sha256===relocation.contract.original_executable.sha256;
}
function systemProcess({command,argv,env,timeout_ms}){const r=spawnSync(command,argv,{env,encoding:null,timeout:timeout_ms,maxBuffer:16*1024*1024});return{exit_code:Number.isInteger(r.status)?r.status:null,signal:r.signal??null,timed_out:r.error?.code==='ETIMEDOUT',stdout:Buffer.from(r.stdout??''),stderr:Buffer.from(r.stderr??'')}}
export function syntheticItems(){return Array.from({length:16},(_,i)=>({item_id:`D-I${String(i+1).padStart(3,'0')}`,source:`synthetic source ${i+1}`,target:`synthetic target ${i+1}`}))}
// STOP_ROUTE: the listing must name gemini-3.7-flash-high exactly once.
// The argv --model binding: the flag and its value as literally handed to the process.
export function argvModel(argv){const i=argv.indexOf('--model');return i>=0&&i+1<argv.length?argv[i+1]:null}
export function parseModels(b,model){
  if(typeof model!=='string'||!model)throw Error('MODEL_LIST_TARGET');
  const text=bytes(b).toString('utf8').replace(/\r\n?/gu,'\n');
  const lines=text.split('\n').filter(x=>x.trim());
  if(!lines.length)throw Error('MODEL_LIST_TSV');
  const rows=lines.map(line=>{
    const fields=line.split('\t').map(x=>x.trim());
    if(fields.length!==2||fields.some(x=>!x))throw Error('MODEL_LIST_TSV');
    return fields;
  });
  const exact=rows.filter(([id])=>id===model).length;
  if(exact!==1)throw Error('MODEL_LIST_EXACT_ROUTE');
  return{model_count:rows.length,qualified_model:model}
}
function reuseError(result){return result.valid?null:`REUSE_CONTRACT:${result.errors.join(',')}`}
function buildReuseContract(root,route,r){
  const rows=readRows(root).rows.filter(x=>x.cell===r.cell&&x.attempt===r.attempt);
  if(rows.length!==2)throw Error(`REUSE_LEDGER_ROWS:${r.cell}:${r.attempt}`);
  return{
    schema_version:REUSE_CONTRACT_SCHEMA,
    task_id:TASK_ID,
    original_candidate_manifest_sha256:ORIGINAL_CANDIDATE_MANIFEST_SHA256,
    original_package_review_gate_path:ORIGINAL_PACKAGE_REVIEW_GATE_PATH,
    original_package_review_gate_sha256:ORIGINAL_PACKAGE_REVIEW_GATE_SHA256,
    route:{route_contract_sha256:shaFile(path.join(root,'ROUTE-CONTRACT.json')),executable:route.cli_contract.executable,executable_sha256:route.cli_contract.executable_sha256,argv:[...r.argv]},
    cell:r.cell,
    attempt:r.attempt,
    ledger_prefix:{row_count:2,start:rows[0],finish:rows[1]},
    capture:{stdout_path:r.stdout_path,stdout_sha256:sha256(r.stdout),stderr_path:r.stderr_path,stderr_sha256:sha256(r.stderr)}
  };
}
export function validateReuseContract(root=here,{route=null,requireManifest=true}={}){
  const errors=[],p=path.join(root,REUSE_CONTRACT_PATH);let c,currentRoute;
  try{c=readCanonical(p)}catch(e){return{valid:false,errors:[`READ:${e.message}`],contract:null,sha256:null}}
  try{currentRoute=route??readCanonical(path.join(root,'ROUTE-CONTRACT.json'))}catch(e){errors.push(`ROUTE:${e.message}`)}
  if(!exactKeys(c,reuseKeys)||c.schema_version!==REUSE_CONTRACT_SCHEMA||c.task_id!==TASK_ID)errors.push('SCHEMA');
  if(c.original_candidate_manifest_sha256!==ORIGINAL_CANDIDATE_MANIFEST_SHA256)errors.push('ORIGINAL_MANIFEST');
  if(c.original_package_review_gate_path!==ORIGINAL_PACKAGE_REVIEW_GATE_PATH||c.original_package_review_gate_sha256!==ORIGINAL_PACKAGE_REVIEW_GATE_SHA256)errors.push('ORIGINAL_PACKAGE_GATE');
  if(!exactKeys(c.route,reuseRouteKeys)||!Array.isArray(c.route.argv))errors.push('ROUTE_SHAPE');
  if(!exactKeys(c.capture,reuseCaptureKeys)||!exactKeys(c.ledger_prefix,['finish','row_count','start'])||c.ledger_prefix?.row_count!==2)errors.push('PROVENANCE_SHAPE');
  if(c.cell!==MODEL_LIST_CELL||c.attempt!==1)errors.push('CELL_ATTEMPT');
  if(currentRoute){
    let routeSha=null;try{routeSha=shaFile(path.join(root,'ROUTE-CONTRACT.json'))}catch{errors.push('ROUTE_CONTRACT_FILE')}
    const historical=c.capture?.stdout_sha256==='b1cc011310435afa07b1e132a5b7f3e22297aa21427177461c858bcbd6a58794';
    if(!captureRouteMatches(root,c.route,currentRoute,routeSha,{historical}))errors.push('ROUTE_RELOCATION_BINDING');
    if(!manifestLists(root,routeRelocation.path))errors.push('ROUTE_RELOCATION_NOT_LISTED');
    if(JSON.stringify(c.route?.argv)!==JSON.stringify(currentRoute.qualification?.model_list_argv))errors.push('MODEL_LIST_ARGV_BINDING');
  }
  const rr=readRows(root);errors.push(...rr.errors.map(x=>`LEDGER:${x}`));
  const prefix=rr.rows.slice(0,2);
  if(prefix.length!==2||JSON.stringify(prefix)!==JSON.stringify([c.ledger_prefix?.start,c.ledger_prefix?.finish]))errors.push('LEDGER_PREFIX_BINDING');
  const rows=rr.rows.filter(x=>x.cell===c.cell&&x.attempt===c.attempt);
  if(rows.length!==2||rows[0]?.finished_at!==null||rows[1]?.finished_at===null||rows[1]?.exit!==0)errors.push('LEDGER_SUCCESS_BINDING');
  if(c.capture?.stdout_path!==capturePaths(c.cell,c.attempt).stdout||c.capture?.stderr_path!==capturePaths(c.cell,c.attempt).stderr)errors.push('CAPTURE_PATH_BINDING');
  for(const k of ['stdout','stderr']){
    const pp=c.capture?.[`${k}_path`],expected=c.capture?.[`${k}_sha256`];
    if(!pp||!expected||!fs.existsSync(path.join(root,pp))||shaFile(path.join(root,pp))!==expected)errors.push(`CAPTURE_${k.toUpperCase()}_BINDING`);
    if(rows[1]?.[`${k}_sha256`]!==expected)errors.push(`FINISH_${k.toUpperCase()}_BINDING`);
  }
  if(requireManifest&&!manifestLists(root,REUSE_CONTRACT_PATH))errors.push('MANIFEST_NOT_LISTED');
  const sha=fs.existsSync(p)?shaFile(p):null;
  return{valid:errors.length===0,errors,contract:c,sha256:sha};
}
export function writeReuseContract(root,route,r){
  const contract=buildReuseContract(root,route,r);
  writeStable(path.join(root,REUSE_CONTRACT_PATH),contract);
  const checked=validateReuseContract(root,{route,requireManifest:false});
  if(!checked.valid)throw Error(reuseError(checked));
  return checked;
}
function syntheticArgv(root,route){
  const request=fs.readFileSync(path.join(root,files.request),'utf8');
  return route.qualification.synthetic_argv.map(x=>x==='[SYNTHETIC_REQUEST_BYTES]'?request:x==='[BUNDLE_SCHEMA]'?fs.readFileSync(path.join(root,route.cli_contract.schema),'utf8'):x);
}
function qualificationPrefix(rows){return rows.slice(0,4)}
function qualificationPrefixSha256(rows){return sha256(Buffer.from(qualificationPrefix(rows).map(ledgerLine).join('')))}
function buildSyntheticReuseContract(root,route,r,argv){
  const rr=readRows(root);if(rr.errors.length)throw Error(`REUSE_LEDGER:${rr.errors.join(',')}`);
  const prefix=qualificationPrefix(rr.rows);
  if(!qualificationCellsAreFirstFour(prefix))throw Error('REUSE_LEDGER_QUALIFICATION_PREFIX');
  return{
    schema_version:SYNTHETIC_REUSE_CONTRACT_SCHEMA,
    task_id:TASK_ID,
    original_candidate_manifest_sha256:SYNTHETIC_ORIGINAL_CANDIDATE_MANIFEST_SHA256,
    original_package_review_gate_path:ORIGINAL_PACKAGE_REVIEW_GATE_PATH,
    original_package_review_gate_sha256:SYNTHETIC_ORIGINAL_PACKAGE_REVIEW_GATE_SHA256,
    route:{route_contract_sha256:shaFile(path.join(root,'ROUTE-CONTRACT.json')),executable:route.cli_contract.executable,executable_sha256:route.cli_contract.executable_sha256,argv_sha256:sha256(jsonBytes(argv))},
    cell:r.cell,
    attempt:r.attempt,
    ledger_prefix:{path:LEDGER_PATH,row_count:prefix.length,rows:prefix,prefix_sha256:qualificationPrefixSha256(prefix)},
    capture:{stdout_path:r.stdout_path,stdout_sha256:sha256(r.stdout),stderr_path:r.stderr_path,stderr_sha256:sha256(r.stderr)}
  };
}
export function validateSyntheticReuseContract(root=here,{route=null,argv=null,requireManifest=true}={}){
  const errors=[],p=path.join(root,SYNTHETIC_REUSE_CONTRACT_PATH);let c,currentRoute,currentArgv;
  try{c=readCanonical(p)}catch(e){return{valid:false,errors:[`READ:${e.message}`],contract:null,sha256:null}}
  try{currentRoute=route??readCanonical(path.join(root,'ROUTE-CONTRACT.json'))}catch(e){errors.push(`ROUTE:${e.message}`)}
  if(!exactKeys(c,syntheticReuseKeys)||c.schema_version!==SYNTHETIC_REUSE_CONTRACT_SCHEMA||c.task_id!==TASK_ID)errors.push('SCHEMA');
  if(c.original_candidate_manifest_sha256!==SYNTHETIC_ORIGINAL_CANDIDATE_MANIFEST_SHA256)errors.push('ORIGINAL_MANIFEST');
  if(c.original_package_review_gate_path!==ORIGINAL_PACKAGE_REVIEW_GATE_PATH||c.original_package_review_gate_sha256!==SYNTHETIC_ORIGINAL_PACKAGE_REVIEW_GATE_SHA256)errors.push('ORIGINAL_PACKAGE_GATE');
  if(!exactKeys(c.route,syntheticReuseRouteKeys)||!hex64(c.route?.argv_sha256))errors.push('ROUTE_SHAPE');
  if(!exactKeys(c.capture,syntheticReuseCaptureKeys)||!exactKeys(c.ledger_prefix,syntheticReuseLedgerPrefixKeys)||c.ledger_prefix?.row_count!==4||!Array.isArray(c.ledger_prefix?.rows)||!hex64(c.ledger_prefix?.prefix_sha256))errors.push('PROVENANCE_SHAPE');
  if(c.cell!==SYNTHETIC_CELL||c.attempt!==1)errors.push('CELL_ATTEMPT');
  if(currentRoute){
    let routeSha=null;try{routeSha=shaFile(path.join(root,'ROUTE-CONTRACT.json'))}catch{errors.push('ROUTE_CONTRACT_FILE')}
    const historical=c.capture?.stdout_sha256==='d06ea853a5ed9fafa6a71a859e4afe62a39efdaeb9f622b0e0207024184e11b4';
    if(!captureRouteMatches(root,c.route,currentRoute,routeSha,{historical}))errors.push('ROUTE_RELOCATION_BINDING');
    if(!manifestLists(root,routeRelocation.path))errors.push('ROUTE_RELOCATION_NOT_LISTED');
    try{currentArgv=argv??syntheticArgv(root,currentRoute)}catch(e){errors.push(`SYNTHETIC_ARGV:${e.message}`)}
    if(currentArgv&&!Array.isArray(currentArgv))errors.push('SYNTHETIC_ARGV_SHAPE');
    if(currentArgv&&c.route?.argv_sha256!==sha256(jsonBytes(currentArgv)))errors.push('SYNTHETIC_ARGV_BINDING');
  }
  const rr=readRows(root);errors.push(...rr.errors.map(x=>`LEDGER:${x}`));
  const ledgerPath=path.join(root,LEDGER_PATH),prefix=qualificationPrefix(rr.rows);
  if(!fs.existsSync(ledgerPath)||c.ledger_prefix?.path!==LEDGER_PATH||c.ledger_prefix?.row_count!==prefix.length||c.ledger_prefix?.prefix_sha256!==qualificationPrefixSha256(prefix)||JSON.stringify(c.ledger_prefix?.rows)!==JSON.stringify(prefix))errors.push('LEDGER_PREFIX_BINDING');
  if(!qualificationCellsAreFirstFour(prefix))errors.push('LEDGER_QUALIFICATION_PREFIX');
  const rows=prefix.filter(x=>x.cell===c.cell&&x.attempt===c.attempt);
  if(rows.length!==2||rows[0]?.finished_at!==null||rows[1]?.finished_at===null||rows[1]?.exit!==0)errors.push('LEDGER_SUCCESS_BINDING');
  if(c.capture?.stdout_path!==capturePaths(c.cell,c.attempt).stdout||c.capture?.stderr_path!==capturePaths(c.cell,c.attempt).stderr)errors.push('CAPTURE_PATH_BINDING');
  for(const k of ['stdout','stderr']){
    const pp=c.capture?.[`${k}_path`],expected=c.capture?.[`${k}_sha256`];
    if(!pp||!expected||!fs.existsSync(path.join(root,pp))||shaFile(path.join(root,pp))!==expected)errors.push(`CAPTURE_${k.toUpperCase()}_BINDING`);
    if(rows[1]?.[`${k}_sha256`]!==expected)errors.push(`FINISH_${k.toUpperCase()}_BINDING`);
  }
  if(requireManifest&&!manifestLists(root,SYNTHETIC_REUSE_CONTRACT_PATH))errors.push('MANIFEST_NOT_LISTED');
  const sha=fs.existsSync(p)?shaFile(p):null;
  return{valid:errors.length===0,errors,contract:c,sha256:sha};
}
export function writeSyntheticReuseContract(root,route,r,argv){
  const contract=buildSyntheticReuseContract(root,route,r,argv);
  writeStable(path.join(root,SYNTHETIC_REUSE_CONTRACT_PATH),contract);
  const checked=validateSyntheticReuseContract(root,{route,argv,requireManifest:false});
  if(!checked.valid)throw Error(reuseError(checked));
  return checked;
}
const capture=(r,parsed)=>({cell:r.cell,attempt:r.attempt,command:r.command,argv:r.argv,exit_code:r.exit_code,signal:r.signal,timed_out:r.timed_out,stdout_path:r.stdout_path,stdout_sha256:sha256(r.stdout),stderr_path:r.stderr_path,stderr_sha256:sha256(r.stderr),parsed});
export const CAPTURE_KEYS=['argv','attempt','cell','command','exit_code','parsed','signal','stderr_path','stderr_sha256','stdout_path','stdout_sha256','timed_out'];
// One journaled agy process: START row -> spawn -> attempt-numbered captures -> FINISH row.
// The START row exists on disk before the process is spawned, so a crash between the two
// leaves the process visible (and, per C09, blocks automatic replay).
function journaledRun(root,cell,{invoke,command,argv,env,timeout_ms,route}){
  const state=deriveState(root);
  if(state.errors.length)throw Error(`LEDGER:${state.errors.join(',')}`);
  if(state.agy_processes_spawned+1>PILOT_AGY_PROCESS_CEILING)throw Error(`STOP_BUDGET:${state.agy_processes_spawned}/${PILOT_AGY_PROCESS_CEILING}`);
  const {attempt,blocked}=nextAttempt(state,cell);
  if(!attempt)throw Error(`ATTEMPT_BLOCKED:${cell}:${blocked}`);
  // Only a new spawn rechecks the host executable. Reuse is read-only recovery of a spent call
  // and must remain possible even if a later host binary update changed the current file hash.
  if(route)verifyAgyExecutable(route,root);
  const cap=capturePaths(cell,attempt),start=startRow(cell,attempt,isoNow());
  appendRow(root,start);
  const r=invoke({command,argv,env,timeout_ms});
  const stdout=bytes(r.stdout),stderr=bytes(r.stderr);
  writeStable(path.join(root,cap.stdout),stdout);writeStable(path.join(root,cap.stderr),stderr);
  const exit_code=Number.isInteger(r.exit_code)&&r.timed_out!==true?r.exit_code:-1;
  appendRow(root,finishRow(start,{exit:exit_code,stdout_sha256:sha256(stdout),stderr_sha256:sha256(stderr),finished_at:isoNow()}));
  return{cell,attempt,command,argv,exit_code,signal:r.signal??null,timed_out:r.timed_out===true,stdout,stderr,stdout_path:cap.stdout,stderr_path:cap.stderr};
}
// Resumable: a cell whose journaled attempt already succeeded is NOT respawned; its captured
// bytes are re-read and hash-checked against the FINISH row instead.
function captureReuseContract(root,cell,spec){
  if(cell===MODEL_LIST_CELL)return validateReuseContract(root,{route:spec.route});
  if(cell===SYNTHETIC_CELL)return validateSyntheticReuseContract(root,{route:spec.route,argv:spec.argv});
  throw Error(`REUSE_CELL_UNSUPPORTED:${cell}`);
}
function ensureCapture(root,cell,spec){
  const c=deriveState(root).cells[cell];
  if(c&&c.successful_attempt!==null){
    const reuse=captureReuseContract(root,cell,spec);
    if(!reuse.valid)throw Error(reuseError(reuse));
    const attempt=c.successful_attempt,a=c.attempts.find(x=>x.attempt===attempt),cap=capturePaths(cell,attempt);
    const stdout=fs.readFileSync(path.join(root,cap.stdout)),stderr=fs.readFileSync(path.join(root,cap.stderr));
    if(sha256(stdout)!==a.stdout_sha256||sha256(stderr)!==a.stderr_sha256)throw Error(`CAPTURE_HASH_MISMATCH:${cell}:${attempt}`);
    return{cell,attempt,command:spec.command,argv:spec.argv,exit_code:a.exit,signal:null,timed_out:false,stdout,stderr,stdout_path:cap.stdout,stderr_path:cap.stderr,reused:true,reuse_contract:reuse};
  }
  return{...journaledRun(root,cell,spec),reused:false};
}
// Read-only recovery of the already successful call 1. This deliberately has no fallback
// invoke: validating the reuse contract and parsing its capture must leave the ledger and
// process counters unchanged before the synthetic qualification call can be considered.
export function reuseModelListCapture(root=here,{repoRoot=defaultRepo}={}){
  const mErrors=checkManifest(root);if(mErrors.length)throw Error(`MANIFEST:${mErrors.join(',')}`);
  const route=readCanonical(path.join(root,'ROUTE-CONTRACT.json'));
  const before=deriveState(root),cell=before.cells[MODEL_LIST_CELL];
  if(before.errors.length)throw Error(`LEDGER:${before.errors.join(',')}`);
  if(!((before.agy_processes_spawned===1&&before.inference_calls_made===0)||(before.agy_processes_spawned===2&&before.inference_calls_made===1)))throw Error('REUSE_PHASE_NOT_QUALIFICATION_CAPTURE');
  if(!cell||cell.successful_attempt===null)throw Error('REUSE_MODEL_LIST_NOT_SUCCESSFUL');
  const spec={command:route.cli_contract.executable,argv:route.qualification.model_list_argv,invoke:()=>{throw Error('REUSE_SPAWN_FORBIDDEN')},env:{},timeout_ms:route.cli_contract.timeout_ms};
  const capture=ensureCapture(root,MODEL_LIST_CELL,spec),models=parseModels(capture.stdout,ROUTE_MODEL),after=deriveState(root);
  if(capture.reused!==true||after.agy_processes_spawned!==before.agy_processes_spawned||after.inference_calls_made!==before.inference_calls_made)throw Error('REUSE_PROCESS_COUNT_DRIFT');
  return{status:'REUSED_CALL_1',reused:true,model_list:models,capture_sha256:sha256(capture.stdout),stderr_sha256:sha256(capture.stderr),agy_processes_spawned:after.agy_processes_spawned,inference_calls_made:after.inference_calls_made,reuse_contract_sha256:capture.reuse_contract.sha256};
}
// Read-only recovery of both successful qualification calls. The injected invokes are
// deliberately forbidden: a missing or invalid contract must fail rather than respawn either
// already-spent process. This is the zero-spawn verifier used after the dual-channel repair.
export function reuseQualificationCaptures(root=here,{repoRoot=defaultRepo}={}){
  const mErrors=checkManifest(root);if(mErrors.length)throw Error(`MANIFEST:${mErrors.join(',')}`);
  const route=readCanonical(path.join(root,'ROUTE-CONTRACT.json'));
  const before=deriveState(root);if(before.errors.length)throw Error(`LEDGER:${before.errors.join(',')}`);
  if(before.agy_processes_spawned!==2||before.inference_calls_made!==1)throw Error('REUSE_PHASE_NOT_AFTER_SYNTHETIC');
  const ledgerPath=path.join(root,LEDGER_PATH),beforeLedger=fs.readFileSync(ledgerPath),forbidden=()=>{throw Error('REUSE_SPAWN_FORBIDDEN')};
  const modelSpec={command:route.cli_contract.executable,argv:route.qualification.model_list_argv,invoke:forbidden,env:{},timeout_ms:route.cli_contract.timeout_ms,route};
  const mr=ensureCapture(root,MODEL_LIST_CELL,modelSpec),models=parseModels(mr.stdout,ROUTE_MODEL);
  const argv=syntheticArgv(root,route);
  const syntheticSpec={command:route.cli_contract.executable,argv,invoke:forbidden,env:{},timeout_ms:route.cli_contract.timeout_ms,route};
  const sr=ensureCapture(root,SYNTHETIC_CELL,syntheticSpec),agy=extractAgy(sr.stdout),after=deriveState(root);
  if(agy.reported_model!==null&&agy.reported_model!==ROUTE_MODEL)throw Error(`STOP_ROUTE_REPORTED_MODEL:${agy.reported_model}`);
  if(mr.reused!==true||sr.reused!==true||after.agy_processes_spawned!==before.agy_processes_spawned||after.inference_calls_made!==before.inference_calls_made)throw Error('REUSE_PROCESS_COUNT_DRIFT');
  if(!fs.readFileSync(ledgerPath).equals(beforeLedger))throw Error('REUSE_LEDGER_DRIFT');
  if(JSON.stringify(agy.output?.items?.map(x=>x.item_id))!==JSON.stringify(syntheticItems().map(x=>x.item_id)))throw Error('REUSE_SYNTHETIC_IDS');
  return{status:'REUSED_CALLS_1_2',reused:true,model_list_capture_sha256:sha256(mr.stdout),synthetic_capture_sha256:sha256(sr.stdout),ledger_sha256:sha256(beforeLedger),agy_processes_spawned:after.agy_processes_spawned,inference_calls_made:after.inference_calls_made,model_list_reuse_contract_sha256:mr.reuse_contract.sha256,synthetic_reuse_contract_sha256:sr.reuse_contract.sha256};
}

export function captureQualification(root=here,{invoke=systemProcess,repoRoot=defaultRepo}={}){
  const mErrors=checkManifest(root);if(mErrors.length)throw Error(`MANIFEST:${mErrors.join(',')}`);
  const g=validateGates(root,{repoRoot,through:'PACKAGE_REVIEW'});
  if(!g.present.PACKAGE_REVIEW)throw Error(`PACKAGE_REVIEW_GATE:${g.errors.join(',')}`);
  const route=readCanonical(path.join(root,'ROUTE-CONTRACT.json')),schema=readCanonical(path.join(root,route.cli_contract.schema)),items=syntheticItems();
  if(route.cli_contract.model!==ROUTE_MODEL)throw Error('STOP_ROUTE_CONTRACT_MODEL');
  const built=buildRequest({prompt:'Return one JSON instance matching OUTPUT SCHEMA. Do not return the schema itself.',schema,items,withContext:false});
  writeStable(path.join(root,files.request),built.request);
  const env=Object.fromEntries(route.environment.allowlist.filter(k=>process.env[k]!==undefined).map(k=>[k,process.env[k]]));
  const spec=argv=>({invoke,command:route.cli_contract.executable,argv,env,timeout_ms:route.cli_contract.timeout_ms,route});

  // process 1 (non-inference): the model listing is the route identity evidence. A new spawn is
  // checked inside journaledRun; an already successful capture takes the no-spawn reuse path.
  const mr=ensureCapture(root,MODEL_LIST_CELL,spec(route.qualification.model_list_argv));
  if(mr.exit_code!==0||mr.timed_out)throw Error('MODEL_LIST_EXIT');
  const models=parseModels(mr.stdout,ROUTE_MODEL);
  const reuse=mr.reused===true?mr.reuse_contract:writeReuseContract(root,route,mr);

  // process 2 (inference, never scored): the argv --model binding is the second half of identity.
  const argv=route.qualification.synthetic_argv.map(x=>x==='[SYNTHETIC_REQUEST_BYTES]'?built.request.toString('utf8'):x==='[BUNDLE_SCHEMA]'?fs.readFileSync(path.join(root,route.cli_contract.schema),'utf8'):x);
  if(argvModel(argv)!==ROUTE_MODEL)throw Error('STOP_ROUTE_ARGV_MODEL');
  const sr=ensureCapture(root,SYNTHETIC_CELL,spec(argv));
  if(sr.exit_code!==0||sr.timed_out)throw Error('SYNTHETIC_EXIT');
  const syntheticReuse=sr.reused===true?sr.reuse_contract:writeSyntheticReuseContract(root,route,sr,argv);
  const agy=extractAgy(sr.stdout);
  // ABSENT self-report is not a mismatch; PRESENT and DIFFERENT is STOP_ROUTE.
  if(agy.reported_model!==null&&agy.reported_model!==ROUTE_MODEL)throw Error(`STOP_ROUTE_REPORTED_MODEL:${agy.reported_model}`);
  if(JSON.stringify(agy.output?.items?.map(x=>x.item_id))!==JSON.stringify(items.map(x=>x.item_id)))throw Error('SYNTHETIC_IDS');
  // The two reuse contracts are immutable provenance inputs, so add them to the package
  // identity before binding the draft. This is package-local only; task-owned gates/receipts
  // remain outside the package writer.
  writeManifest(root);
  const listedReuse=validateReuseContract(root,{route}),listedSyntheticReuse=validateSyntheticReuseContract(root,{route,argv});
  if(!listedReuse.valid)throw Error(reuseError(listedReuse));
  if(!listedSyntheticReuse.valid)throw Error(`SYNTHETIC_${reuseError(listedSyntheticReuse)}`);

  const draft={schema_version:'gemini-context-v5-qualification-draft-v1',task_id:TASK_ID,manifest_sha256:manifestSha256(root),route_contract_sha256:shaFile(path.join(root,'ROUTE-CONTRACT.json')),reuse_contract_path:REUSE_CONTRACT_PATH,reuse_contract_sha256:reuse.sha256,reuse_provenance:reuse.contract,synthetic_reuse_contract_path:SYNTHETIC_REUSE_CONTRACT_PATH,synthetic_reuse_contract_sha256:syntheticReuse.sha256,synthetic_reuse_provenance:syntheticReuse.contract,input:{items},model_list:capture(mr,models),synthetic:capture(sr,{channel:'structured_output_authoritative_response_items_equal',output_sha256:sha256(jsonBytes(agy.output)),reported_model:agy.reported_model})};
  writeStable(path.join(root,files.draft),draft);
  const derived=deriveState(root);
  return{status:'CAPTURED_AWAITING_ARCHIVED_DISPATCH_RECEIPT',agy_processes_spawned:derived.agy_processes_spawned,inference_calls_made:derived.inference_calls_made,draft_sha256:shaFile(path.join(root,files.draft))};
}
export function bindingHash({manifest_sha256,route_contract_sha256,reuse_contract_sha256,synthetic_reuse_contract_sha256,capture_receipt}){return sha256(jsonBytes({task_id:TASK_ID,manifest_sha256,route_contract_sha256,reuse_contract_sha256,synthetic_reuse_contract_sha256,capture_receipt}))}
function readReceipt(repoRoot,draftSha){
  const p=path.join(repoRoot,CAPTURE_RECEIPT_PATH);
  if(!fs.existsSync(p))throw Error('CAPTURE_RECEIPT_ABSENT_DISPATCH_NOT_ARCHIVED');
  const r=readCanonical(p);
  if(!exactKeys(r,['agent_id','archive_confirmed','dispatch_id','draft_sha256','manifest_sha256','purpose','schema_version','task_id'])||r.schema_version!=='gemini-context-v5-qualification-capture-receipt-v1'||r.task_id!==TASK_ID||r.purpose!=='route_qualification_capture'||r.archive_confirmed!==true||r.draft_sha256!==draftSha)throw Error('CAPTURE_RECEIPT_FIELDS');
  return{path:CAPTURE_RECEIPT_PATH,sha256:shaFile(p),dispatch_id:r.dispatch_id,agent_id:r.agent_id};
}
// Pure: reads captures, spawns nothing, writes only package-local files.
export function finalizeQualification(root=here,{repoRoot=defaultRepo}={}){
  const draftSha=shaFile(path.join(root,files.draft)),draft=readCanonical(path.join(root,files.draft)),manifest_sha256=manifestSha256(root);
  if(draft.manifest_sha256!==manifest_sha256)throw Error('DRAFT_MANIFEST_MISMATCH');
  const reuse=validateReuseContract(root),syntheticReuse=validateSyntheticReuseContract(root);if(!reuse.valid)throw Error(reuseError(reuse));if(!syntheticReuse.valid)throw Error(`SYNTHETIC_${reuseError(syntheticReuse)}`);
  if(draft.reuse_contract_path!==REUSE_CONTRACT_PATH||draft.reuse_contract_sha256!==reuse.sha256||JSON.stringify(draft.reuse_provenance)!==JSON.stringify(reuse.contract))throw Error('DRAFT_REUSE_PROVENANCE');
  if(draft.synthetic_reuse_contract_path!==SYNTHETIC_REUSE_CONTRACT_PATH||draft.synthetic_reuse_contract_sha256!==syntheticReuse.sha256||JSON.stringify(draft.synthetic_reuse_provenance)!==JSON.stringify(syntheticReuse.contract))throw Error('DRAFT_SYNTHETIC_REUSE_PROVENANCE');
  const capture_receipt=readReceipt(repoRoot,draftSha);
  if(capture_receipt.sha256&&readCanonical(path.join(repoRoot,CAPTURE_RECEIPT_PATH)).manifest_sha256!==manifest_sha256)throw Error('CAPTURE_RECEIPT_MANIFEST_MISMATCH');
  const qualification_binding_sha256=bindingHash({manifest_sha256,route_contract_sha256:draft.route_contract_sha256,reuse_contract_sha256:reuse.sha256,synthetic_reuse_contract_sha256:syntheticReuse.sha256,capture_receipt});
  const raw=rawSynthetic(root,draft,qualification_binding_sha256);
  writeStable(path.join(root,files.raw),raw);
  // No process counter is written here: C15 requires every count to be derived from the ledger.
  // What is recorded is which journaled attempt of which cell produced each capture.
  const evidence={schema_version:'gemini-context-v5-qualification-evidence-v1',task_id:TASK_ID,non_scored:true,manifest_sha256,route_contract_sha256:draft.route_contract_sha256,reuse_contract_path:REUSE_CONTRACT_PATH,reuse_contract_sha256:reuse.sha256,reuse_provenance:reuse.contract,synthetic_reuse_contract_path:SYNTHETIC_REUSE_CONTRACT_PATH,synthetic_reuse_contract_sha256:syntheticReuse.sha256,synthetic_reuse_provenance:syntheticReuse.contract,route_identity:routeIdentity(draft),reported_model:draft.synthetic.parsed.reported_model,qualification_binding_sha256,capture_receipt,capture_attempts:{[MODEL_LIST_CELL]:draft.model_list.attempt,[SYNTHETIC_CELL]:draft.synthetic.attempt},draft_path:files.draft,draft_sha256:draftSha,raw_path:files.raw,raw_sha256:sha256(raw)};
  writeStable(path.join(root,files.evidence),evidence);
  const v=validateQualification(root,{repoRoot});
  if(!v.valid)throw Error(`FINALIZED_INVALID:${v.errors.join(',')}`);
  return v;
}
// C12: route identity, stated explicitly, from the two pieces of evidence that are NOT the
// runtime self-report -- the models listing and the argv --model binding.
function routeIdentity(draft){return{source:'models_list_capture_and_argv_model_binding',model_list_qualified_model:draft.model_list.parsed.qualified_model,argv_model_binding:argvModel(draft.synthetic.argv),runtime_self_report_is_not_identity_evidence:true}}
function rawSynthetic(root,draft,qualification_binding_sha256){
  const agy=extractAgy(fs.readFileSync(path.join(root,draft.synthetic.stdout_path)));
  return jsonBytes({status:'SUCCESS',request_binding:{attempt:0,cohort:'qualification',protocol:'Q',qualification_binding_sha256,request_path:files.request,request_sha256:shaFile(path.join(root,files.request)),route_contract_sha256:draft.route_contract_sha256,run:0,shard:0},runtime:{argv_sha256:sha256(jsonBytes(draft.synthetic.argv)),command:draft.synthetic.command,exit_code:draft.synthetic.exit_code,stderr_sha256:draft.synthetic.stderr_sha256,stdout_sha256:draft.synthetic.stdout_sha256,...(agy.reported_model?{reported_model:agy.reported_model}:{})},structured_output:agy.output,response:null});
}
export function validateQualification(root=here,{repoRoot=defaultRepo}={}){
  const ep=path.join(root,files.evidence);
  // Process counters are DERIVED from the ledger in every branch, including this one (C15).
  const counts=()=>{try{const d=deriveState(root);return{agy_processes_spawned:d.agy_processes_spawned,inference_calls_made:d.inference_calls_made,qualification_processes_spawned:d.rows?Object.entries(d.cells).filter(([c])=>QUALIFICATION_CELLS.includes(c)).reduce((n,[,c])=>n+c.attempt_numbers.length,0):0}}catch{return{agy_processes_spawned:0,inference_calls_made:0,qualification_processes_spawned:0}}};
  if(!fs.existsSync(ep))return{status:'NOT_RUN',valid:false,non_scored:true,errors:['EVIDENCE_ABSENT'],...counts()};
  const e=[];
  try{
    const q=readCanonical(ep),draft=readCanonical(path.join(root,q.draft_path)),manifest_sha256=manifestSha256(root);
    if(!exactKeys(q,['capture_attempts','capture_receipt','draft_path','draft_sha256','manifest_sha256','non_scored','qualification_binding_sha256','raw_path','raw_sha256','reported_model','reuse_contract_path','reuse_contract_sha256','reuse_provenance','synthetic_reuse_contract_path','synthetic_reuse_contract_sha256','synthetic_reuse_provenance','route_contract_sha256','route_identity','schema_version','task_id'])||q.schema_version!=='gemini-context-v5-qualification-evidence-v1'||q.task_id!==TASK_ID||q.non_scored!==true||q.manifest_sha256!==manifest_sha256||q.draft_sha256!==shaFile(path.join(root,q.draft_path))||q.route_contract_sha256!==shaFile(path.join(root,'ROUTE-CONTRACT.json')))e.push('EVIDENCE_IDENTITY');
    const reuse=validateReuseContract(root),syntheticReuse=validateSyntheticReuseContract(root);
    if(!reuse.valid)e.push(`REUSE_CONTRACT:${reuse.errors.join(',')}`);
    if(!syntheticReuse.valid)e.push(`SYNTHETIC_REUSE_CONTRACT:${syntheticReuse.errors.join(',')}`);
    if(q.reuse_contract_path!==REUSE_CONTRACT_PATH||q.reuse_contract_sha256!==reuse.sha256||JSON.stringify(q.reuse_provenance)!==JSON.stringify(reuse.contract))e.push('REUSE_PROVENANCE_BINDING');
    if(q.synthetic_reuse_contract_path!==SYNTHETIC_REUSE_CONTRACT_PATH||q.synthetic_reuse_contract_sha256!==syntheticReuse.sha256||JSON.stringify(q.synthetic_reuse_provenance)!==JSON.stringify(syntheticReuse.contract))e.push('SYNTHETIC_REUSE_PROVENANCE_BINDING');
    if(draft.reuse_contract_path!==REUSE_CONTRACT_PATH||draft.reuse_contract_sha256!==reuse.sha256||JSON.stringify(draft.reuse_provenance)!==JSON.stringify(reuse.contract))e.push('DRAFT_REUSE_PROVENANCE');
    if(draft.synthetic_reuse_contract_path!==SYNTHETIC_REUSE_CONTRACT_PATH||draft.synthetic_reuse_contract_sha256!==syntheticReuse.sha256||JSON.stringify(draft.synthetic_reuse_provenance)!==JSON.stringify(syntheticReuse.contract))e.push('DRAFT_SYNTHETIC_REUSE_PROVENANCE');
    // C12 route identity: the listing and the argv binding are the evidence. The runtime
    // self-report may be ABSENT (real captures have no top-level `model`); only a PRESENT and
    // DIFFERENT value is STOP_ROUTE.
    if(q.route_identity?.model_list_qualified_model!==ROUTE_MODEL)e.push('STOP_ROUTE_MODEL_LIST');
    if(q.route_identity?.argv_model_binding!==ROUTE_MODEL)e.push('STOP_ROUTE_ARGV_MODEL');
    if(q.reported_model!==null&&q.reported_model!==ROUTE_MODEL)e.push('STOP_ROUTE_REPORTED_MODEL');
    if(JSON.stringify(q.route_identity)!==JSON.stringify(routeIdentity(draft)))e.push('ROUTE_IDENTITY_BINDING');
    // Each capture must be the journaled attempt of its journaled cell, hash-bound both ways.
    const st=deriveState(root);
    if(st.errors.length)e.push(`LEDGER:${st.errors.join(',')}`);
    for(const [label,x] of [['MODEL_LIST',draft.model_list],['SYNTHETIC',draft.synthetic]]){
      if(!exactKeys(x,CAPTURE_KEYS)){e.push(`CAPTURE_${label}_SHAPE`);continue}
      if(q.capture_attempts?.[x.cell]!==x.attempt)e.push(`CAPTURE_${label}_ATTEMPT_BINDING`);
      const cap=capturePaths(x.cell,x.attempt);
      if(x.stdout_path!==cap.stdout||x.stderr_path!==cap.stderr)e.push(`CAPTURE_${label}_PATH`);
      const row=st.cells[x.cell]?.attempts.find(a=>a.attempt===x.attempt);
      if(!row||row.state!=='FINISHED_SUCCESS'||row.stdout_sha256!==x.stdout_sha256||row.stderr_sha256!==x.stderr_sha256||row.exit!==x.exit_code)e.push(`CAPTURE_${label}_NOT_JOURNALED`);
      for(const k of ['stdout','stderr']){const pp=x[`${k}_path`];if(typeof pp!=='string'||!fs.existsSync(path.join(root,pp))||shaFile(path.join(root,pp))!==x[`${k}_sha256`])e.push(`CAPTURE_${label}_${k.toUpperCase()}`)}
    }
    let receipt=null;try{receipt=readReceipt(repoRoot,q.draft_sha256)}catch(x){e.push(`CAPTURE_RECEIPT:${x.message}`)}
    if(receipt&&JSON.stringify(receipt)!==JSON.stringify(q.capture_receipt))e.push('CAPTURE_RECEIPT_BINDING');
    if(q.qualification_binding_sha256!==bindingHash({manifest_sha256,route_contract_sha256:q.route_contract_sha256,reuse_contract_sha256:q.reuse_contract_sha256,synthetic_reuse_contract_sha256:q.synthetic_reuse_contract_sha256,capture_receipt:q.capture_receipt}))e.push('QUALIFICATION_BINDING');
    const rb=rawSynthetic(root,draft,q.qualification_binding_sha256);
    if(!fs.existsSync(path.join(root,q.raw_path))||!fs.readFileSync(path.join(root,q.raw_path)).equals(rb)||q.raw_sha256!==sha256(rb))e.push('RAW_DETERMINISTIC_REBUILD');
    const binding={attempt:0,cohort:'qualification',protocol:'Q',qualification_binding_sha256:q.qualification_binding_sha256,request_path:files.request,request_sha256:shaFile(path.join(root,files.request)),route_contract_sha256:q.route_contract_sha256,run:0,shard:0};
    const parsed=parseEnvelope(rb.toString('utf8'),{items:draft.input.items},binding,{valid:true,identity_tier:'QUALIFIED_ROUTE_BOUND',qualification_binding_sha256:q.qualification_binding_sha256,route_contract_sha256:q.route_contract_sha256});
    if(!parsed.valid)e.push(`RAW_PARSE:${parsed.errors.join(',')}`);
    return{status:e.length?'INVALID':'PASS_NON_SCORED',valid:e.length===0,non_scored:true,errors:e,evidence_sha256:shaFile(ep),qualification_binding_sha256:q.qualification_binding_sha256,route_contract_sha256:q.route_contract_sha256,reported_model:q.reported_model,route_identity:q.route_identity,...counts()};
  }catch(x){return{status:'INVALID',valid:false,non_scored:true,errors:[x.message],...counts()}}
}
if(import.meta.url===`file://${process.argv[1]}`){console.error('Qualification is a two-stage library workflow. No qualification has been run.');process.exitCode=3}
