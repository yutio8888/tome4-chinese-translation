#!/usr/bin/env node
// Two-stage, non-scored route qualification. Exactly TWO agy processes, both here:
//   process 1  agy models list --json      (non-inference)  cell qualification-models-list
//   process 2  one synthetic 16-item request D-I001..D-I016 (inference, never scored)
//                                                            cell qualification-synthetic
// There is no `--version` process.
//
// C15: both processes are journaled in the SAME append-only execution/LEDGER.jsonl as the
// execution cells -- one START row before the spawn and one FINISH row after it, in the same
// seven-key row shape. Nothing here reports a process count: every counter is derived from
// those rows (deriveState().agy_processes_spawned / .inference_calls_made). Captures are
// attempt-numbered, so a failed capture is retried under the same [1] / [1,2] attempt rule
// with no manual file deletion, and the retry is visible as a third journaled process.
//
// Route identity is the `models list --json` capture naming gemini-3.7-flash-high exactly once
// plus the argv `--model` binding of the synthetic request. The envelope's top-level `model`
// field is an OPTIONAL runtime self-report: real captures do not carry it, so its ABSENCE is
// never a mismatch; a PRESENT and DIFFERENT value is STOP_ROUTE (SPEC 8).
//
// Stage 1 captureQualification() writes only package-local capture bytes and a DRAFT.
// The dispatch is then archived by the task owner, who writes the task-owned
// QUALIFICATION-CAPTURE-RECEIPT.json. Stage 2 finalizeQualification() is PURE: it spawns
// nothing, derives RAW from the captured stdout, and writes qualification/EVIDENCE.json.
// Package code never writes any file under .ai/task/ (C11/C12).
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readCanonical,shaFile,sha256,jsonBytes,writeStable,exactKeys,parseNoDuplicate} from './lib.mjs';
import {parseEnvelope,extractAgy} from './parser.mjs';
import {buildRequest} from './request-lib.mjs';
import {checkManifest,manifestSha256,TASK_ID} from './build-manifest.mjs';
import {TASK_DIR,validateGates} from './gates.mjs';
import {deriveState,nextAttempt,appendRow,startRow,finishRow,isoNow,capturePaths,QUALIFICATION_CELLS,PILOT_AGY_PROCESS_CEILING} from './ledger.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),defaultRepo=path.resolve(here,'../../../..');
export const [MODEL_LIST_CELL,SYNTHETIC_CELL]=QUALIFICATION_CELLS;
export const CAPTURE_RECEIPT_PATH=`${TASK_DIR}/QUALIFICATION-CAPTURE-RECEIPT.json`;
export const files={request:'qualification/SYNTHETIC-REQUEST.txt',draft:'qualification/EVIDENCE-DRAFT.json',raw:'qualification/RAW-SYNTHETIC.json',evidence:'qualification/EVIDENCE.json'};
export const ROUTE_MODEL='gemini-3.7-flash-high';
const bytes=x=>Buffer.isBuffer(x)?x:Buffer.from(x??'');
function systemProcess({command,argv,env,timeout_ms}){const r=spawnSync(command,argv,{env,encoding:null,timeout:timeout_ms,maxBuffer:16*1024*1024});return{exit_code:Number.isInteger(r.status)?r.status:null,signal:r.signal??null,timed_out:r.error?.code==='ETIMEDOUT',stdout:Buffer.from(r.stdout??''),stderr:Buffer.from(r.stderr??'')}}
export function syntheticItems(){return Array.from({length:16},(_,i)=>({item_id:`D-I${String(i+1).padStart(3,'0')}`,source:`synthetic source ${i+1}`,target:`synthetic target ${i+1}`}))}
// STOP_ROUTE: the listing must name gemini-3.7-flash-high exactly once.
// The argv --model binding: the flag and its value as literally handed to the process.
export function argvModel(argv){const i=argv.indexOf('--model');return i>=0&&i+1<argv.length?argv[i+1]:null}
export function parseModels(b,model){const v=parseNoDuplicate(b.toString('utf8'),'MODEL_LIST'),rows=Array.isArray(v)?v:v?.models;if(!Array.isArray(rows))throw Error('MODEL_LIST_SCHEMA');const ids=rows.map(x=>typeof x==='string'?x:x?.id??x?.name??x?.model);if(ids.filter(x=>x===model).length!==1)throw Error('MODEL_LIST_EXACT_ROUTE');return{model_count:ids.length,qualified_model:model}}
const capture=(r,parsed)=>({cell:r.cell,attempt:r.attempt,command:r.command,argv:r.argv,exit_code:r.exit_code,signal:r.signal,timed_out:r.timed_out,stdout_path:r.stdout_path,stdout_sha256:sha256(r.stdout),stderr_path:r.stderr_path,stderr_sha256:sha256(r.stderr),parsed});
export const CAPTURE_KEYS=['argv','attempt','cell','command','exit_code','parsed','signal','stderr_path','stderr_sha256','stdout_path','stdout_sha256','timed_out'];
// One journaled agy process: START row -> spawn -> attempt-numbered captures -> FINISH row.
// The START row exists on disk before the process is spawned, so a crash between the two
// leaves the process visible (and, per C09, blocks automatic replay).
function journaledRun(root,cell,{invoke,command,argv,env,timeout_ms}){
  const state=deriveState(root);
  if(state.errors.length)throw Error(`LEDGER:${state.errors.join(',')}`);
  if(state.agy_processes_spawned+1>PILOT_AGY_PROCESS_CEILING)throw Error(`STOP_BUDGET:${state.agy_processes_spawned}/${PILOT_AGY_PROCESS_CEILING}`);
  const {attempt,blocked}=nextAttempt(state,cell);
  if(!attempt)throw Error(`ATTEMPT_BLOCKED:${cell}:${blocked}`);
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
function ensureCapture(root,cell,spec){
  const c=deriveState(root).cells[cell];
  if(c&&c.successful_attempt!==null){
    const attempt=c.successful_attempt,a=c.attempts.find(x=>x.attempt===attempt),cap=capturePaths(cell,attempt);
    const stdout=fs.readFileSync(path.join(root,cap.stdout)),stderr=fs.readFileSync(path.join(root,cap.stderr));
    if(sha256(stdout)!==a.stdout_sha256||sha256(stderr)!==a.stderr_sha256)throw Error(`CAPTURE_HASH_MISMATCH:${cell}:${attempt}`);
    return{cell,attempt,command:spec.command,argv:spec.argv,exit_code:a.exit,signal:null,timed_out:false,stdout,stderr,stdout_path:cap.stdout,stderr_path:cap.stderr};
  }
  return journaledRun(root,cell,spec);
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
  const spec=argv=>({invoke,command:route.cli_contract.executable,argv,env,timeout_ms:route.cli_contract.timeout_ms});

  // process 1 (non-inference): the model listing is the route identity evidence.
  const mr=ensureCapture(root,MODEL_LIST_CELL,spec(route.qualification.model_list_argv));
  if(mr.exit_code!==0||mr.timed_out)throw Error('MODEL_LIST_EXIT');
  const models=parseModels(mr.stdout,ROUTE_MODEL);

  // process 2 (inference, never scored): the argv --model binding is the second half of identity.
  const argv=route.qualification.synthetic_argv.map(x=>x==='[SYNTHETIC_REQUEST_BYTES]'?built.request.toString('utf8'):x==='[BUNDLE_SCHEMA]'?fs.readFileSync(path.join(root,route.cli_contract.schema),'utf8'):x);
  if(argvModel(argv)!==ROUTE_MODEL)throw Error('STOP_ROUTE_ARGV_MODEL');
  const sr=ensureCapture(root,SYNTHETIC_CELL,spec(argv));
  if(sr.exit_code!==0||sr.timed_out)throw Error('SYNTHETIC_EXIT');
  const agy=extractAgy(sr.stdout);
  // ABSENT self-report is not a mismatch; PRESENT and DIFFERENT is STOP_ROUTE.
  if(agy.reported_model!==null&&agy.reported_model!==ROUTE_MODEL)throw Error(`STOP_ROUTE_REPORTED_MODEL:${agy.reported_model}`);
  if(JSON.stringify(agy.output?.items?.map(x=>x.item_id))!==JSON.stringify(items.map(x=>x.item_id)))throw Error('SYNTHETIC_IDS');

  const draft={schema_version:'gemini-context-v5-qualification-draft-v1',task_id:TASK_ID,manifest_sha256:manifestSha256(root),route_contract_sha256:shaFile(path.join(root,'ROUTE-CONTRACT.json')),input:{items},model_list:capture(mr,models),synthetic:capture(sr,{channel:'structured_output_or_response_exactly_one',output_sha256:sha256(jsonBytes(agy.output)),reported_model:agy.reported_model})};
  writeStable(path.join(root,files.draft),draft);
  const derived=deriveState(root);
  return{status:'CAPTURED_AWAITING_ARCHIVED_DISPATCH_RECEIPT',agy_processes_spawned:derived.agy_processes_spawned,inference_calls_made:derived.inference_calls_made,draft_sha256:shaFile(path.join(root,files.draft))};
}
export function bindingHash({manifest_sha256,route_contract_sha256,capture_receipt}){return sha256(jsonBytes({task_id:TASK_ID,manifest_sha256,route_contract_sha256,capture_receipt}))}
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
  const capture_receipt=readReceipt(repoRoot,draftSha);
  if(capture_receipt.sha256&&readCanonical(path.join(repoRoot,CAPTURE_RECEIPT_PATH)).manifest_sha256!==manifest_sha256)throw Error('CAPTURE_RECEIPT_MANIFEST_MISMATCH');
  const qualification_binding_sha256=bindingHash({manifest_sha256,route_contract_sha256:draft.route_contract_sha256,capture_receipt});
  const raw=rawSynthetic(root,draft,qualification_binding_sha256);
  writeStable(path.join(root,files.raw),raw);
  // No process counter is written here: C15 requires every count to be derived from the ledger.
  // What is recorded is which journaled attempt of which cell produced each capture.
  const evidence={schema_version:'gemini-context-v5-qualification-evidence-v1',task_id:TASK_ID,non_scored:true,manifest_sha256,route_contract_sha256:draft.route_contract_sha256,route_identity:routeIdentity(draft),reported_model:draft.synthetic.parsed.reported_model,qualification_binding_sha256,capture_receipt,capture_attempts:{[MODEL_LIST_CELL]:draft.model_list.attempt,[SYNTHETIC_CELL]:draft.synthetic.attempt},draft_path:files.draft,draft_sha256:draftSha,raw_path:files.raw,raw_sha256:sha256(raw)};
  writeStable(path.join(root,files.evidence),evidence);
  const v=validateQualification(root,{repoRoot});
  if(!v.valid)throw Error(`FINALIZED_INVALID:${v.errors.join(',')}`);
  return v;
}
// C12: route identity, stated explicitly, from the two pieces of evidence that are NOT the
// runtime self-report -- the model listing and the argv --model binding.
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
    if(!exactKeys(q,['capture_attempts','capture_receipt','draft_path','draft_sha256','manifest_sha256','non_scored','qualification_binding_sha256','raw_path','raw_sha256','reported_model','route_contract_sha256','route_identity','schema_version','task_id'])||q.schema_version!=='gemini-context-v5-qualification-evidence-v1'||q.task_id!==TASK_ID||q.non_scored!==true||q.manifest_sha256!==manifest_sha256||q.draft_sha256!==shaFile(path.join(root,q.draft_path))||q.route_contract_sha256!==shaFile(path.join(root,'ROUTE-CONTRACT.json')))e.push('EVIDENCE_IDENTITY');
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
    if(q.qualification_binding_sha256!==bindingHash({manifest_sha256,route_contract_sha256:q.route_contract_sha256,capture_receipt:q.capture_receipt}))e.push('QUALIFICATION_BINDING');
    const rb=rawSynthetic(root,draft,q.qualification_binding_sha256);
    if(!fs.existsSync(path.join(root,q.raw_path))||!fs.readFileSync(path.join(root,q.raw_path)).equals(rb)||q.raw_sha256!==sha256(rb))e.push('RAW_DETERMINISTIC_REBUILD');
    const binding={attempt:0,cohort:'qualification',protocol:'Q',qualification_binding_sha256:q.qualification_binding_sha256,request_path:files.request,request_sha256:shaFile(path.join(root,files.request)),route_contract_sha256:q.route_contract_sha256,run:0,shard:0};
    const parsed=parseEnvelope(rb.toString('utf8'),{items:draft.input.items},binding,{valid:true,identity_tier:'QUALIFIED_ROUTE_BOUND',qualification_binding_sha256:q.qualification_binding_sha256,route_contract_sha256:q.route_contract_sha256});
    if(!parsed.valid)e.push(`RAW_PARSE:${parsed.errors.join(',')}`);
    return{status:e.length?'INVALID':'PASS_NON_SCORED',valid:e.length===0,non_scored:true,errors:e,evidence_sha256:shaFile(ep),qualification_binding_sha256:q.qualification_binding_sha256,route_contract_sha256:q.route_contract_sha256,reported_model:q.reported_model,route_identity:q.route_identity,...counts()};
  }catch(x){return{status:'INVALID',valid:false,non_scored:true,errors:[x.message],...counts()}}
}
if(import.meta.url===`file://${process.argv[1]}`){console.error('Qualification is a two-stage library workflow. No qualification has been run.');process.exitCode=3}
