// Execution library. One cell per call, one attempt per call, one ledger.
// The production entry point is run.mjs (--cell <id> only); this module is what it calls.
//
// Order per attempt, with no exception:
//   append START row -> spawn -> write stdout/stderr captures -> append FINISH row -> derive RAW
// RAW is never produced by a second invocation; it is always a pure function of the
// captured stdout bytes (see deriveRaw / C10).
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readCanonical,parseNoDuplicate,sha256,jsonBytes,writeExclusive} from './lib.mjs';
import {checkManifest} from './build-manifest.mjs';
import {verifyPredecessorBindings} from './build-frozen-base.mjs';
import {validateGates} from './gates.mjs';
import {validateQualification} from './qualification.mjs';
import {parseEnvelope,extractAgy} from './parser.mjs';
import {deriveState,nextAttempt,appendRow,startRow,finishRow,isoNow,stem,capturePaths} from './ledger.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),defaultRepo=path.resolve(here,'../../../..');
const bytes=x=>Buffer.isBuffer(x)?x:Buffer.from(x??'');
export {stem,capturePaths};
export const rawPath=(cell,attempt)=>`execution/RAW/${stem(cell,attempt)}.json`;
export function requestEntry(root,cell){const m=readCanonical(path.join(root,'frozen/REQUEST-MANIFEST.json')),e=m.requests.find(x=>x.cell===cell);if(!e)throw Error(`UNKNOWN_CELL:${cell}`);return e}
export function requestInput(text){const a=text.indexOf('INPUT JSON:\n'),b=text.lastIndexOf('\n\nOUTPUT SCHEMA:');if(a<0||b<a)throw Error('REQUEST_INPUT_PARSE');return parseNoDuplicate(text.slice(a+12,b),'REQUEST_INPUT')}
export function plan(root,entry){
  const r=readCanonical(path.join(root,'ROUTE-CONTRACT.json')),request=fs.readFileSync(path.join(root,entry.path),'utf8');
  if(sha256(request)!==entry.sha256)throw Error(`REQUEST_DRIFT:${entry.path}`);
  const argv=r.cli_contract.argv_template.map(x=>x==='[REQUEST_BYTES]'?request:x==='[BUNDLE_SCHEMA]'?fs.readFileSync(path.join(root,r.cli_contract.schema),'utf8'):x);
  return{command:r.cli_contract.executable,argv,env:Object.fromEntries(r.environment.allowlist.filter(k=>process.env[k]!==undefined).map(k=>[k,process.env[k]])),timeout_ms:r.cli_contract.timeout_ms,request};
}
function systemInvoke(p){const r=spawnSync(p.command,p.argv,{env:p.env,encoding:null,timeout:p.timeout_ms,maxBuffer:16*1024*1024});return{exit_code:Number.isInteger(r.status)?r.status:null,signal:r.signal??null,stdout:Buffer.from(r.stdout??''),stderr:Buffer.from(r.stderr??''),timed_out:r.error?.code==='ETIMEDOUT'}}
export function rawBytes({entry,attempt,exit_code,stdout,stderr,argv,command,qualification_binding_sha256,route_contract_sha256}){
  const a=extractAgy(stdout);
  return jsonBytes({status:'SUCCESS',request_binding:{attempt,cohort:entry.cohort,protocol:entry.protocol,qualification_binding_sha256,request_path:entry.path,request_sha256:entry.sha256,route_contract_sha256,run:entry.run,shard:entry.shard},runtime:{argv_sha256:sha256(jsonBytes(argv)),command,exit_code,stderr_sha256:sha256(stderr),stdout_sha256:sha256(stdout),...(a.reported_model?{reported_model:a.reported_model}:{})},structured_output:a.output,response:null});
}
// C10: FINISHED with exit 0 but no RAW -> derive RAW from the captured stdout alone.
// This function has no invoke parameter and spawns nothing, by construction.
export function deriveRaw(root=here,cell,attempt,{repoRoot=defaultRepo}={}){
  const state=deriveState(root),c=state.cells[cell],a=c?.attempts.find(x=>x.attempt===attempt);
  if(!a)throw Error(`NO_LEDGER_ATTEMPT:${cell}:${attempt}`);
  if(a.state!=='FINISHED_SUCCESS')throw Error(`NOT_FINISHED_SUCCESS:${cell}:${attempt}:${a.state}`);
  const cap=capturePaths(cell,attempt),stdout=fs.readFileSync(path.join(root,cap.stdout)),stderr=fs.readFileSync(path.join(root,cap.stderr));
  if(sha256(stdout)!==a.stdout_sha256||sha256(stderr)!==a.stderr_sha256)throw Error(`CAPTURE_HASH_MISMATCH:${cell}:${attempt}`);
  const q=validateQualification(root,{repoRoot});if(!q.valid)throw Error(`QUALIFICATION:${q.errors.join(',')}`);
  const entry=requestEntry(root,cell),p=plan(root,entry);
  const rb=rawBytes({entry,attempt,exit_code:a.exit,stdout,stderr,argv:p.argv,command:p.command,qualification_binding_sha256:q.qualification_binding_sha256,route_contract_sha256:q.route_contract_sha256});
  const rp=path.join(root,rawPath(cell,attempt));
  if(fs.existsSync(rp)){if(!fs.readFileSync(rp).equals(rb))throw Error(`RAW_DRIFT:${cell}:${attempt}`)}else writeExclusive(rp,rb);
  const parsed=parseEnvelope(rb.toString('utf8'),requestInput(p.request),{attempt,cohort:entry.cohort,protocol:entry.protocol,qualification_binding_sha256:q.qualification_binding_sha256,request_path:entry.path,request_sha256:entry.sha256,route_contract_sha256:q.route_contract_sha256,run:entry.run,shard:entry.shard},{valid:true,identity_tier:'QUALIFIED_ROUTE_BOUND',qualification_binding_sha256:q.qualification_binding_sha256,route_contract_sha256:q.route_contract_sha256});
  return{raw_path:rawPath(cell,attempt),raw_sha256:sha256(rb),parsed};
}
// Full gate + budget + attempt-rule check, then at most one spawn.
export function runCell(cell,{root=here,repoRoot=defaultRepo,invoke=systemInvoke}={}){
  const mErrors=checkManifest(root);if(mErrors.length)throw Error(`MANIFEST:${mErrors.join(',')}`);
  const pErrors=verifyPredecessorBindings(root,repoRoot);if(pErrors.length)throw Error(`PREDECESSOR:${pErrors.join(',')}`);
  const g=validateGates(root,{repoRoot});if(!g.valid)throw Error(`GATES:${g.errors.join(',')}`);
  const auth=g.gates.EXECUTION_AUTHORIZATION;
  if(!auth.authorized_cells.includes(cell))throw Error(`CELL_NOT_AUTHORIZED:${cell}`);
  const q=validateQualification(root,{repoRoot});if(!q.valid)throw Error(`QUALIFICATION:${q.errors.join(',')}`);
  const state=deriveState(root);
  if(state.errors.length)throw Error(`LEDGER:${state.errors.join(',')}`);
  // C15: the process count is the number of START rows in the ledger -- qualification included,
  // since qualification journals its two processes here too. No constant is added to it.
  const spawned=state.agy_processes_spawned;
  if(spawned+1>auth.agy_process_budget)throw Error(`STOP_BUDGET:${spawned}/${auth.agy_process_budget}`);
  const {attempt,blocked}=nextAttempt(state,cell);
  if(!attempt)throw Error(`ATTEMPT_BLOCKED:${cell}:${blocked}`);
  const entry=requestEntry(root,cell),p=plan(root,entry),cap=capturePaths(cell,attempt);
  const start=startRow(cell,attempt,isoNow());
  appendRow(root,start);
  const inv=invoke(p);
  const out=bytes(inv.stdout),err=bytes(inv.stderr);
  writeExclusive(path.join(root,cap.stdout),out);writeExclusive(path.join(root,cap.stderr),err);
  const exit=Number.isInteger(inv.exit_code)&&!inv.timed_out?inv.exit_code:-1;
  appendRow(root,finishRow(start,{exit,stdout_sha256:sha256(out),stderr_sha256:sha256(err),finished_at:isoNow()}));
  // F3: classification comes back from the ledger, which treats an exit-0 attempt whose captured
  // stdout yields no agy envelope as FINISHED_RETRYABLE -- so attempt 2 is available once and
  // SPEC 8 STOP_PARSE follows the attempt rule instead of firing after a single attempt.
  const after=deriveState(root),outcome=after.cells[cell]?.attempts.find(a=>a.attempt===attempt);
  if(outcome?.state!=='FINISHED_SUCCESS')return{cell,attempt,exit,success:false,state:outcome?.state??'UNKNOWN',retryable:after.cells[cell]?.next_attempt===2,classification:exit===0?'ENVELOPE_UNPARSEABLE':'PROCESS_FAILED',raw_path:null};
  const d=deriveRaw(root,cell,attempt,{repoRoot});
  return{cell,attempt,exit,success:true,state:outcome.state,retryable:false,classification:'ENVELOPE_EXTRACTED',raw_path:d.raw_path,raw_sha256:d.raw_sha256,parse_valid:d.parsed.valid,parse_errors:d.parsed.errors};
}
