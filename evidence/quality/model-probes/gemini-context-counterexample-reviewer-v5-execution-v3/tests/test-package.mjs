#!/usr/bin/env node
// Executable verification of checklist items C01-C13. Every test names the item it covers.
// No agy process, no model call and no network call is made anywhere in this file: the only
// process-shaped thing is a mock `invoke` function passed explicitly into the library.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseNoDuplicate,readCanonical,jsonBytes,sha256,shaFile,walk} from '../lib.mjs';
import {checkManifest,buildManifest,manifestSha256,sourcePaths,MANIFEST_PATH,GENERATED_PREFIXES,TASK_ID} from '../build-manifest.mjs';
import {verifyPredecessorBindings,replay} from '../build-frozen-base.mjs';
import {checkFreeze,freeze,buildFromRoot,freezeState} from '../freezer.mjs';
import {jsonIntegrity,leakageScan,preflight} from '../preflight.mjs';
import {parseEnvelope} from '../parser.mjs';
import {validateReference,scoreCell,scoresDocument} from '../scorer.mjs';
import {deriveState,appendRow,startRow,finishRow,readRows,executionEmpty,nextAttempt,LEDGER_PATH,ROW_KEYS,QUALIFICATION_CELLS,PILOT_AGY_PROCESS_CEILING,capturePaths as ledgerCapturePaths} from '../ledger.mjs';
import {TASK_DIR,gatePaths,validateGates,GATE_ORDER} from '../gates.mjs';
import * as qualificationModule from '../qualification.mjs';
import {captureQualification,finalizeQualification,validateQualification,CAPTURE_RECEIPT_PATH,files as qfiles,syntheticItems,MODEL_LIST_CELL,SYNTHETIC_CELL,argvModel} from '../qualification.mjs';
import {runCell,deriveRaw,requestInput,capturePaths,rawPath,plan,requestEntry} from '../runner.mjs';
import * as runModule from '../run.mjs';
import {parseArgv} from '../run.mjs';
import {postRun,reconstruct} from '../post-run.mjs';

const here=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const realRepo=path.resolve(here,'../../../..');
const pkgRel='evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v3';
const PRED=['evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5','evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v1','evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v2'];
const V5_GATE='.ai/task/research-gemini-context-counterexample-reviewer-v5/ROUND-0003-TERMINALIZATION-REVIEW-GATE-001.json';
const AUTHORIZED=['discovery-A-run-1-shard-1','discovery-C-run-1-shard-1'];
const tmp=()=>fs.mkdtempSync(path.join(os.tmpdir(),'v5x3-'));
const write=(p,x)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,Buffer.isBuffer(x)?x:jsonBytes(x))};
const fixture=readCanonical(path.join(here,'tests/fixtures/valid-envelope.json'));
const gateSchema=g=>`gemini-context-v5-execution-gate-${g.toLowerCase()}-v1`;

function baseRepo(){
  const repo=tmp();
  fs.cpSync(path.join(realRepo,pkgRel),path.join(repo,pkgRel),{recursive:true});
  for(const rel of PRED)fs.cpSync(path.join(realRepo,rel),path.join(repo,rel),{recursive:true});
  fs.cpSync(path.join(realRepo,V5_GATE),path.join(repo,V5_GATE));
  return{repo,root:path.join(repo,pkgRel)};
}
// C12: the mock reproduces the checked-in real-shape fixture VERBATIM. It injects no top-level
// `model` key, because no real agy capture in this repository carries one. `selfReport` opts a
// case into a present-but-different self-report, which must STOP_ROUTE.
function agyStdout(items,{selfReport=undefined}={}){return jsonBytes({...fixture,...(selfReport===undefined?{}:{model:selfReport}),structured_output:{items}})}
function qualificationInvoke(counter,{selfReport=undefined,syntheticExits=[]}={}){
  let synthetic=0;
  return ({argv})=>{
    counter.argvs.push(argv);counter.n++;
    if(argv[0]==='models')return{exit_code:0,timed_out:false,signal:null,stdout:Buffer.from('{"models":[{"id":"gemini-3.7-flash-high"},{"id":"other-model"}]}'),stderr:Buffer.alloc(0)};
    const exit=syntheticExits[synthetic++]??0;
    return{exit_code:exit,timed_out:false,signal:null,stdout:agyStdout(syntheticItems().map(x=>({item_id:x.item_id,candidates:[]})),{selfReport}),stderr:Buffer.from('redacted diagnostic')};
  };
}
// Mock cell invoke. findOn: item_ids that should come back with one FINDING candidate.
function cellInvoke(counter,{findOn=()=>false,exit=0,stdout=null}={}){
  return p=>{
    counter.n++;
    if(stdout!==null)return{exit_code:exit,timed_out:false,signal:null,stdout,stderr:Buffer.alloc(0)};
    const inp=requestInput(p.request);
    const items=inp.items.map(x=>({item_id:x.item_id,candidates:findOn(x)?[{verdict:'FINDING',claim_type:'OTHER',target_span:x.target.slice(0,Math.min(24,x.target.length)),correction:'rewrite',evidence:x.source.slice(0,Math.min(24,x.source.length))}]:[]}));
    return{exit_code:exit,timed_out:false,signal:null,stdout:agyStdout(items),stderr:Buffer.alloc(0)};
  };
}
// Builds a temp repo advanced through all three gates, with qualification finalized.
// A temp repo advanced only as far as the PACKAGE_REVIEW gate (qualification not yet run).
function reviewedRepo(){
  const {repo,root}=baseRepo();
  freeze(root);
  const manifest_sha256=manifestSha256(root);
  write(path.join(repo,gatePaths.PACKAGE_REVIEW),{schema_version:gateSchema('PACKAGE_REVIEW'),task_id:TASK_ID,gate:'PACKAGE_REVIEW',status:'SATISFIED_CHECKLIST_C01_C14_PASS',manifest_sha256,checklist_items_passed:Array.from({length:14},(_,i)=>`C${String(i+1).padStart(2,'0')}`)});
  return{repo,root,manifest_sha256};
}
// Authors the QUALIFICATION and EXECUTION_AUTHORIZATION gates over an already-finalized
// qualification. Budgets are parameters so budget arithmetic can be exercised directly.
function authorize(repo,root,manifest_sha256,{cells=AUTHORIZED,agy_process_budget=4,inference_call_budget=3}={}){
  write(path.join(repo,gatePaths.QUALIFICATION),{schema_version:gateSchema('QUALIFICATION'),task_id:TASK_ID,gate:'QUALIFICATION',status:'SATISFIED_NON_SCORED_ROUTE_QUALIFICATION',manifest_sha256,predecessor_gate:{path:gatePaths.PACKAGE_REVIEW,sha256:shaFile(path.join(repo,gatePaths.PACKAGE_REVIEW))},qualification_evidence:{path:`${pkgRel}/qualification/EVIDENCE.json`,sha256:shaFile(path.join(root,qfiles.evidence))},reported_model:readCanonical(path.join(root,qfiles.evidence)).reported_model});
  write(path.join(repo,gatePaths.EXECUTION_AUTHORIZATION),{schema_version:gateSchema('EXECUTION_AUTHORIZATION'),task_id:TASK_ID,gate:'EXECUTION_AUTHORIZATION',status:'AUTHORIZED_EXACT_CELLS_AND_ROUTE',manifest_sha256,predecessor_gate:{path:gatePaths.QUALIFICATION,sha256:shaFile(path.join(repo,gatePaths.QUALIFICATION))},authorized_cells:cells,agy_process_budget,inference_call_budget,request_manifest_sha256:shaFile(path.join(root,'frozen/REQUEST-MANIFEST.json')),route_contract_sha256:shaFile(path.join(root,'ROUTE-CONTRACT.json'))});
}
function setup({findOn}={}){
  const {repo,root}=baseRepo();
  freeze(root);
  const manifest_sha256=manifestSha256(root);
  write(path.join(repo,gatePaths.PACKAGE_REVIEW),{schema_version:gateSchema('PACKAGE_REVIEW'),task_id:TASK_ID,gate:'PACKAGE_REVIEW',status:'SATISFIED_CHECKLIST_C01_C14_PASS',manifest_sha256,checklist_items_passed:Array.from({length:14},(_,i)=>`C${String(i+1).padStart(2,'0')}`)});
  const counter={n:0,argvs:[]};
  captureQualification(root,{invoke:qualificationInvoke(counter),repoRoot:repo});
  write(path.join(repo,CAPTURE_RECEIPT_PATH),{schema_version:'gemini-context-v5-qualification-capture-receipt-v1',task_id:TASK_ID,purpose:'route_qualification_capture',dispatch_id:'qual-dispatch-1',agent_id:'qual-agent-1',archive_confirmed:true,manifest_sha256,draft_sha256:shaFile(path.join(root,qfiles.draft))});
  finalizeQualification(root,{repoRoot:repo});
  authorize(repo,root,manifest_sha256);
  return{repo,root,manifest_sha256,qualificationCalls:counter};
}
let n=0;
async function test(name,fn){try{await fn();console.log(`ok ${++n} - ${name}`)}catch(e){console.error(`not ok ${n+1} - ${name}\n${e.stack}`);process.exitCode=1}}

/* ------------------------------------------------------------------ C01 */
await test('C01 predecessor documents and all three predecessor trees are byte-unchanged',()=>{
  assert.deepEqual(verifyPredecessorBindings(here,realRepo),[]);
  const b=readCanonical(path.join(here,'frozen/PREDECESSOR-BINDINGS.json'));
  assert.equal(b.round_artifacts.length,30);
  assert.deepEqual(b.predecessor_trees.map(x=>x.root),PRED);
  const {repo,root}=baseRepo();
  fs.appendFileSync(path.join(repo,PRED[1],'README.md'),'tamper');
  const errs=verifyPredecessorBindings(root,repo);
  assert.ok(errs.some(x=>x.startsWith('PREDECESSOR_TREE_DRIFT:')&&x.includes('execution-v1')),errs.join(','));
});

/* ------------------------------------------------------------------ C02 */
await test('C02 MANIFEST.json lists every source file and rebuilds byte-identically',()=>{
  assert.deepEqual(checkManifest(here),[]);
  const m=readCanonical(path.join(here,MANIFEST_PATH));
  assert.equal(m.file_count,m.files.length);
  assert.deepEqual(m.files.map(x=>x.path),sourcePaths(here));
  assert.ok(!m.files.some(x=>x.path===MANIFEST_PATH),'manifest must exclude itself');
  const {root}=baseRepo();
  fs.writeFileSync(path.join(root,'STRAY.txt'),'x');
  assert.ok(checkManifest(root).some(x=>x==='UNLISTED_FILE:STRAY.txt'));
  fs.rmSync(path.join(root,'STRAY.txt'));
  fs.appendFileSync(path.join(root,'README.md'),'drift');
  assert.ok(checkManifest(root).some(x=>x==='MANIFEST_HASH_DRIFT:README.md'));
});
await test('C02 generated phase artifacts are excluded, not silently unlisted',()=>{
  const {root}=baseRepo();
  freeze(root);
  assert.deepEqual(checkManifest(root),[]);
  assert.ok(fs.existsSync(path.join(root,'frozen/REQUEST-MANIFEST.json')));
  assert.ok(GENERATED_PREFIXES.includes('model-facing/requests/'));
});

/* ------------------------------------------------------------------ C03 */
await test('C03 every JSON file parses, rejects duplicate keys and round-trips canonically',()=>{
  assert.deepEqual(jsonIntegrity(here),[]);
  assert.throws(()=>parseNoDuplicate(fs.readFileSync(path.join(here,'tests/fixtures/duplicate-key.txt'),'utf8')),/DUPLICATE_KEY/);
  assert.throws(()=>parseNoDuplicate('{"a":1,"a":2}'),/DUPLICATE_KEY/);
  const d=tmp();fs.writeFileSync(path.join(d,'x.json'),'{"a": 1}');
  assert.throws(()=>readCanonical(path.join(d,'x.json')),/NONCANONICAL/);
});

/* ------------------------------------------------------------------ C04 */
await test('C04 renderer emits 32 deterministic requests, 7 exact-source appends, all under the byte ceiling',()=>{
  const r=checkFreeze(here);
  assert.deepEqual(r.errors,[]);
  assert.equal(r.built.requests.length,32);
  assert.equal(r.built.manifest.exact_source_appended_count,7);
  assert.equal(new Set(r.built.requests.map(x=>x.cell)).size,32);
  for(const x of r.built.requests){
    assert.ok(x.utf8_bytes<=120000,`${x.path} ${x.utf8_bytes}`);
    assert.equal(sha256(x.bytes),x.sha256);
    assert.equal(x.bytes.length,x.utf8_bytes);
  }
  const m=r.built.manifest;
  assert.equal(m.requests.length,32);
  for(const [i,x] of m.requests.entries())assert.equal(x.sha256,r.built.requests[i].sha256);
  assert.equal(new Set(m.requests.flatMap(x=>x.item_ids)).size,64);
  const second=buildFromRoot(here);
  for(const [i,x] of second.requests.entries())assert.ok(x.bytes.equals(r.built.requests[i].bytes));
  assert.ok(jsonBytes(second.manifest).equals(jsonBytes(m)));
});

/* ------------------------------------------------------------------ C05 */
await test('C05 leakage scan over all 32 rendered requests finds nothing forbidden',()=>{
  const built=buildFromRoot(here);
  assert.deepEqual(leakageScan(built),[]);
  const forbidden=['proposal_sha256','row_sha256','base_item_id','planned_role','public_source_file','revision_uid','normalized_context_sha256'];
  for(const r of built.requests){const t=r.bytes.toString('utf8');for(const f of forbidden)assert.ok(!t.includes(f),`${r.path} leaks ${f}`)}
});

/* ------------------------------------------------------------------ C06 */
await test('C06 parser accepts the real-shape envelope and rejects each malformation',()=>{
  const input={items:syntheticItems()};
  const binding={attempt:1,cohort:'discovery',protocol:'A',qualification_binding_sha256:'a'.repeat(64),request_path:'p.txt',request_sha256:'b'.repeat(64),route_contract_sha256:'c'.repeat(64),run:1,shard:1};
  const trusted={valid:true,identity_tier:'QUALIFIED_ROUTE_BOUND',qualification_binding_sha256:binding.qualification_binding_sha256,route_contract_sha256:binding.route_contract_sha256};
  const envelope=x=>({status:'SUCCESS',request_binding:binding,runtime:{command:'agy',argv_sha256:'d'.repeat(64),exit_code:0,stdout_sha256:'e'.repeat(64),stderr_sha256:'f'.repeat(64)},structured_output:{items:input.items.map(y=>({item_id:y.item_id,candidates:[]}))},response:null,...x});
  const good=envelope({});
  assert.equal(parseEnvelope(JSON.stringify(good),input,binding,trusted).valid,true);
  // duplicate keys anywhere
  assert.equal(parseEnvelope('{"status":"SUCCESS","status":"SUCCESS"}',input,binding,trusted).classification,'HARNESS_OR_OUTPUT_PARSE_FAILURE');
  // wrong item count
  const short=envelope({structured_output:{items:good.structured_output.items.slice(0,15)}});
  assert.equal(parseEnvelope(JSON.stringify(short),input,binding,trusted).valid,false);
  // wrong item order
  const swapped=envelope({structured_output:{items:[good.structured_output.items[1],good.structured_output.items[0],...good.structured_output.items.slice(2)]}});
  assert.equal(parseEnvelope(JSON.stringify(swapped),input,binding,trusted).valid,false);
  // extra channel: both structured_output and response non-null
  const both=envelope({response:JSON.stringify({items:good.structured_output.items})});
  const r=parseEnvelope(JSON.stringify(both),input,binding,trusted);
  assert.equal(r.valid,false);
  assert.ok(r.errors.includes('STRUCTURED_CHANNEL_CARDINALITY'),r.errors.join(','));
  // the checked-in real-shape agy stdout fixture carries exactly one channel and 16 items
  assert.equal(fixture.response,null);
  assert.equal(fixture.structured_output.items.length,16);
});

/* ------------------------------------------------------------------ C07 */
await test('C07 scorer maps findings x reference rows by the one-directional containment rule',()=>{
  const d=readCanonical(path.join(here,'tests/fixtures/scorer-case.json'));
  assert.deepEqual(validateReference(d.reference),[]);
  const s=scoreCell(d.raw_items,d.reference.items);
  assert.deepEqual(s,d.expected);
  assert.equal(s.context_hits,1);   // reported span contains frozen span
  assert.equal(s.surface_hits,1);
  assert.equal(s.clean_with_findings,1);
  // reverse containment must not score: frozen span contains the reported span
  const reverse=[{item_id:'F-I002',candidates:[{verdict:'FINDING',claim_type:'EVENT',target_span:'gamma',correction:'c',evidence:'e'}]}];
  assert.equal(scoreCell(reverse,[d.reference.items[1]]).context_hits,0);
  const forward=[{item_id:'F-I002',candidates:[{verdict:'FINDING',claim_type:'EVENT',target_span:'the gamma delta clause',correction:'c',evidence:'e'}]}];
  assert.equal(scoreCell(forward,[d.reference.items[1]]).context_hits,1);
  // byte-identical SCORES output on repeated runs
  const cells=[{cell:'discovery-A-run-1-shard-1',protocol:'A',raw_path:'execution/RAW/x.json',raw_sha256:'0'.repeat(64),score:s}];
  const a=jsonBytes(scoresDocument({reference_sha256:'1'.repeat(64),sample_sha256:'2'.repeat(64),cells})),
        b=jsonBytes(scoresDocument({reference_sha256:'1'.repeat(64),sample_sha256:'2'.repeat(64),cells:[...cells]}));
  assert.ok(a.equals(b),'SCORES bytes must be reproducible');
});

/* ------------------------------------------------------------------ C09 (ledger rules, no process) */
await test('C09 attempt sequence is [1] or [1,2] and attempt 2 needs a finished retryable attempt 1',()=>{
  const d=tmp(),cell='discovery-A-run-1-shard-1';
  assert.equal(deriveState(d).no_run,true);
  const s1=startRow(cell,1,'2026-09-02T00:00:00.000Z');
  appendRow(d,s1);
  let st=deriveState(d);
  assert.equal(st.cells[cell].ambiguous,true);
  assert.equal(nextAttempt(st,cell).attempt,null);
  assert.equal(nextAttempt(st,cell).blocked,'AMBIGUOUS_STARTED_BLOCKS_REPLAY');   // STARTED-without-FINISHED blocks replay
  appendRow(d,finishRow(s1,{exit:1,stdout_sha256:'0'.repeat(64),stderr_sha256:'1'.repeat(64),finished_at:'2026-09-02T00:00:01.000Z'}));
  st=deriveState(d);
  assert.deepEqual(st.errors,[]);
  assert.equal(st.cells[cell].attempts[0].state,'FINISHED_RETRYABLE');
  assert.equal(nextAttempt(st,cell).attempt,2);
  const s2=startRow(cell,2,'2026-09-02T00:00:02.000Z');
  appendRow(d,s2);
  appendRow(d,finishRow(s2,{exit:0,stdout_sha256:'2'.repeat(64),stderr_sha256:'3'.repeat(64),finished_at:'2026-09-02T00:00:03.000Z'}));
  st=deriveState(d);
  assert.deepEqual(st.errors,[]);
  assert.deepEqual(st.cells[cell].attempt_numbers,[1,2]);
  assert.equal(st.cells[cell].successful_attempt,2);
  assert.equal(nextAttempt(st,cell).attempt,null);
  assert.equal(nextAttempt(st,cell).blocked,'ALREADY_SUCCEEDED');
  // two failed attempts exhaust the rule: there is no attempt 3
  const e=tmp(),c2='discovery-A-run-2-shard-1';
  for(const k of [1,2]){const s=startRow(c2,k,`2026-09-02T00:00:0${k}.000Z`);appendRow(e,s);appendRow(e,finishRow(s,{exit:7,stdout_sha256:'0'.repeat(64),stderr_sha256:'1'.repeat(64),finished_at:`2026-09-02T00:00:1${k}.000Z`}))}
  const es=deriveState(e);
  assert.deepEqual(es.errors,[]);
  assert.equal(nextAttempt(es,c2).attempt,null);
  assert.equal(nextAttempt(es,c2).blocked,'ATTEMPT_RULE_EXHAUSTED');
});
await test('C09 attempt 2 after a SUCCESSFUL attempt 1 is rejected by ledger derivation',()=>{
  const d=tmp(),cell='discovery-C-run-1-shard-1';
  const s1=startRow(cell,1,'2026-09-02T00:00:00.000Z');
  appendRow(d,s1);
  appendRow(d,finishRow(s1,{exit:0,stdout_sha256:'0'.repeat(64),stderr_sha256:'1'.repeat(64),finished_at:'2026-09-02T00:00:01.000Z'}));
  assert.equal(nextAttempt(deriveState(d),cell).blocked,'ALREADY_SUCCEEDED');
  const s2=startRow(cell,2,'2026-09-02T00:00:02.000Z');
  appendRow(d,s2);
  assert.ok(deriveState(d).errors.some(x=>x.startsWith('ATTEMPT_2_WITHOUT_FINISHED_RETRYABLE_1')));
});
await test('C09 attempt 3, an out-of-order finish and a non-canonical line are all rejected',()=>{
  for(const [label,mutate] of [
    ['attempt3',d=>{const s=startRow('discovery-A-run-1-shard-1',1,'2026-09-02T00:00:00.000Z');appendRow(d,s);appendRow(d,finishRow(s,{exit:1,stdout_sha256:'0'.repeat(64),stderr_sha256:'1'.repeat(64),finished_at:'2026-09-02T00:00:01.000Z'}));fs.appendFileSync(path.join(d,LEDGER_PATH),JSON.stringify({attempt:3,cell:'discovery-A-run-1-shard-1',started_at:'2026-09-02T00:00:02.000Z',finished_at:null,exit:null,stdout_sha256:null,stderr_sha256:null})+'\n')}],
    ['finish_first',d=>{fs.mkdirSync(path.join(d,'execution'),{recursive:true});fs.writeFileSync(path.join(d,LEDGER_PATH),JSON.stringify({attempt:1,cell:'discovery-A-run-1-shard-1',started_at:'2026-09-02T00:00:00.000Z',finished_at:'2026-09-02T00:00:01.000Z',exit:0,stdout_sha256:'0'.repeat(64),stderr_sha256:'1'.repeat(64)})+'\n')}],
    ['reordered_keys',d=>{fs.mkdirSync(path.join(d,'execution'),{recursive:true});fs.writeFileSync(path.join(d,LEDGER_PATH),JSON.stringify({cell:'discovery-A-run-1-shard-1',attempt:1,started_at:'2026-09-02T00:00:00.000Z',finished_at:null,exit:null,stdout_sha256:null,stderr_sha256:null})+'\n')}]
  ]){
    const d=tmp();mutate(d);
    assert.ok(deriveState(d).errors.length>0,label);
  }
  assert.deepEqual(ROW_KEYS,['attempt','cell','started_at','finished_at','exit','stdout_sha256','stderr_sha256']);
});

/* ------------------------------------------------------------------ C11 */
await test('C11 run.mjs accepts only --cell <id> and exposes no root/state/invoke knob',()=>{
  assert.deepEqual(parseArgv(['--cell','discovery-A-run-1-shard-1']),{ok:true,cell:'discovery-A-run-1-shard-1'});
  for(const argv of [[],['--cell'],['--cell','a','b'],['--cells','discovery-A-run-1-shard-1'],['discovery-A-run-1-shard-1'],['--cell','--root'],['--cell',''],['--cell','discovery-A-run-1-shard-3'],['--cell','discovery-E-run-1-shard-1'],['--root','/tmp','--cell','discovery-A-run-1-shard-1'],['--cell','discovery-A-run-1-shard-1','--force']])
    assert.equal(parseArgv(argv).ok,false,JSON.stringify(argv));
  assert.deepEqual(Object.keys(runModule).sort(),['AUTHORIZATION_PATH','USAGE','parseArgv']);
  assert.equal(runModule.AUTHORIZATION_PATH,`${TASK_DIR}/EXECUTION-AUTHORIZATION.json`);
  const src=fs.readFileSync(path.join(here,'run.mjs'),'utf8');
  // the CLI reads no environment variable and its only argv branch is parseArgv
  assert.ok(!src.includes('process.env'),'run.mjs must not read the environment');
  assert.equal((src.match(/process\.argv\.slice\(2\)/gu)??[]).length,1);
  for(const flag of ['--root','--repo','--state','--invoke','--authorize','--force','--cells','-c'])
    assert.equal(parseArgv([flag,'discovery-A-run-1-shard-1']).ok,false,flag);
});

/* ------------------------------------------------------------------ C12 */
await test('C12 qualification is two-stage, spawns exactly two processes and never runs --version',()=>{
  const f=setup();
  assert.equal(f.qualificationCalls.n,2);
  assert.deepEqual(f.qualificationCalls.argvs[0],['models','list','--json']);
  for(const argv of f.qualificationCalls.argvs)assert.ok(!argv.includes('--version'),'no --version process');
  assert.ok(f.qualificationCalls.argvs[1].includes('--model'));
  const v=validateQualification(f.root,{repoRoot:f.repo});
  assert.equal(v.valid,true,v.errors.join(','));
  assert.equal(v.agy_processes_spawned,2);
  assert.equal(v.inference_calls_made,1);
  assert.match(fs.readFileSync(path.join(f.root,qfiles.request),'utf8'),/D-I016/);
  assert.deepEqual(Object.keys(qualificationModule).sort().filter(x=>x.startsWith('capture')||x.startsWith('finalize')),['captureQualification','finalizeQualification']);
});
await test('C12 an ABSENT runtime model self-report is not a mismatch; identity is the listing plus the argv binding',()=>{
  // The mock stdout is the checked-in fixture shape verbatim: it has no top-level `model` key,
  // exactly like every real agy capture in this repository.
  assert.ok(!Object.prototype.hasOwnProperty.call(fixture,'model'),'the fixture must not self-report a model');
  assert.ok(!Object.prototype.hasOwnProperty.call(parseNoDuplicate(agyStdout([]).toString('utf8')),'model'),'the mock must not inject a model key');
  const f=setup();
  const q=readCanonical(path.join(f.root,qfiles.evidence));
  assert.equal(q.reported_model,null,'absent self-report is recorded as null, not as a mismatch');
  assert.equal(q.route_identity.model_list_qualified_model,'gemini-3.7-flash-high');
  assert.equal(q.route_identity.argv_model_binding,'gemini-3.7-flash-high');
  assert.equal(q.route_identity.runtime_self_report_is_not_identity_evidence,true);
  const v=validateQualification(f.root,{repoRoot:f.repo});
  assert.equal(v.valid,true,v.errors.join(','));
  assert.deepEqual(v.errors,[]);
  // and the gate accepts the null self-report, so the QUALIFICATION gate is satisfiable
  const g=validateGates(f.root,{repoRoot:f.repo});
  assert.equal(g.valid,true,g.errors.join(','));
  assert.equal(readCanonical(path.join(f.repo,gatePaths.QUALIFICATION)).reported_model,null);
  // the route contract and the code agree that the self-report is not identity evidence
  const route=readCanonical(path.join(here,'ROUTE-CONTRACT.json'));
  assert.equal(route.qualification.runtime_self_report_is_not_identity_evidence,true);
  assert.equal(route.qualification.runtime_self_report_absent_is_not_a_mismatch,true);
  assert.deepEqual(route.qualification.route_identity_evidence,['models_list_capture','argv_model_binding']);
  assert.equal(argvModel(readCanonical(path.join(f.root,qfiles.draft)).synthetic.argv),'gemini-3.7-flash-high');
});
await test('C12 a PRESENT but DIFFERENT runtime model self-report is STOP_ROUTE',()=>{
  const {repo,root}=reviewedRepo();
  const counter={n:0,argvs:[]};
  assert.throws(()=>captureQualification(root,{invoke:qualificationInvoke(counter,{selfReport:'gemini-3.7-flash-low'}),repoRoot:repo}),/STOP_ROUTE_REPORTED_MODEL:gemini-3\.7-flash-low/);
  assert.ok(!fs.existsSync(path.join(root,qfiles.draft)),'no draft is written for an off-route reply');
  // the process is still journaled and still counted, exactly as SPEC 6 requires
  assert.equal(deriveState(root).agy_processes_spawned,2);
  // and a hand-written gate carrying an off-route self-report is refused
  const bad=validateGates(root,{repoRoot:repo,through:'PACKAGE_REVIEW'});
  assert.equal(bad.present.PACKAGE_REVIEW,true);
  write(path.join(repo,gatePaths.QUALIFICATION),{schema_version:gateSchema('QUALIFICATION'),task_id:TASK_ID,gate:'QUALIFICATION',status:'SATISFIED_NON_SCORED_ROUTE_QUALIFICATION',manifest_sha256:manifestSha256(root),predecessor_gate:{path:gatePaths.PACKAGE_REVIEW,sha256:shaFile(path.join(repo,gatePaths.PACKAGE_REVIEW))},qualification_evidence:{path:`${pkgRel}/qualification/EVIDENCE.json`,sha256:'0'.repeat(64)},reported_model:'gemini-3.7-flash-low'});
  assert.ok(validateGates(root,{repoRoot:repo}).errors.includes('QUALIFICATION:STOP_ROUTE'));
});
await test('C12 finalization is pure and refuses without the task-owned archived receipt',()=>{
  const {repo,root}=baseRepo();
  freeze(root);
  const manifest_sha256=manifestSha256(root);
  write(path.join(repo,gatePaths.PACKAGE_REVIEW),{schema_version:gateSchema('PACKAGE_REVIEW'),task_id:TASK_ID,gate:'PACKAGE_REVIEW',status:'SATISFIED_CHECKLIST_C01_C14_PASS',manifest_sha256,checklist_items_passed:Array.from({length:14},(_,i)=>`C${String(i+1).padStart(2,'0')}`)});
  const counter={n:0,argvs:[]};
  captureQualification(root,{invoke:qualificationInvoke(counter),repoRoot:repo});
  // package code did not create anything under .ai/task/
  assert.ok(!fs.existsSync(path.join(repo,CAPTURE_RECEIPT_PATH)));
  assert.throws(()=>finalizeQualification(root,{repoRoot:repo}),/CAPTURE_RECEIPT_ABSENT_DISPATCH_NOT_ARCHIVED/);
  assert.ok(!fs.existsSync(path.join(root,qfiles.evidence)));
  write(path.join(repo,CAPTURE_RECEIPT_PATH),{schema_version:'gemini-context-v5-qualification-capture-receipt-v1',task_id:TASK_ID,purpose:'route_qualification_capture',dispatch_id:'d',agent_id:'a',archive_confirmed:false,manifest_sha256,draft_sha256:shaFile(path.join(root,qfiles.draft))});
  assert.throws(()=>finalizeQualification(root,{repoRoot:repo}),/CAPTURE_RECEIPT_FIELDS/);
  fs.rmSync(path.join(repo,CAPTURE_RECEIPT_PATH));
  write(path.join(repo,CAPTURE_RECEIPT_PATH),{schema_version:'gemini-context-v5-qualification-capture-receipt-v1',task_id:TASK_ID,purpose:'route_qualification_capture',dispatch_id:'d',agent_id:'a',archive_confirmed:true,manifest_sha256,draft_sha256:shaFile(path.join(root,qfiles.draft))});
  const before=counter.n;
  finalizeQualification(root,{repoRoot:repo});
  assert.equal(counter.n,before,'finalization must spawn nothing');
  assert.ok(fs.existsSync(path.join(root,qfiles.evidence)));
});
await test('C12 no package code writes anything under .ai/task/',()=>{
  // static: no write call anywhere in the package addresses a task-owned path
  for(const rel of sourcePaths(here).filter(x=>x.endsWith('.mjs')&&!x.startsWith('tests/'))){
    const src=fs.readFileSync(path.join(here,rel),'utf8');
    for(const m of src.matchAll(/(?:writeFileSync|appendFileSync|writeExclusive|writeStable|renameSync|rmSync|cpSync)\(([^;\n]*)/gu))
      for(const token of ['TASK_DIR','CAPTURE_RECEIPT_PATH','gatePaths','.ai/task'])
        assert.ok(!m[1].includes(token),`${rel} writes a task-owned path: ${m[0]}`);
  }
  // runtime: a full gated run leaves the task directory byte-identical
  const f=setup(),counter={n:0};
  const snap=()=>walk(path.join(f.repo,'.ai')).map(x=>`${x} ${shaFile(path.join(f.repo,'.ai',x))}`).sort();
  const before=snap();
  for(const cell of AUTHORIZED)runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)});
  postRun(f.root,{repoRoot:f.repo,write:true});
  assert.deepEqual(snap(),before,'package code must not touch .ai/task');
});

/* ------------------------------------------------------------------ C15 */
await test('C15 both qualification processes are journaled in execution/LEDGER.jsonl before they are spawned',()=>{
  const {repo,root}=reviewedRepo();
  assert.equal(fs.existsSync(path.join(root,LEDGER_PATH)),false);
  // the START row for a cell must already be on disk when its process is invoked
  const seen=[];
  const spy=({argv})=>{
    const rows=readRows(root).rows,last=rows[rows.length-1];
    seen.push({argv0:argv[0],rows:rows.length,open:last.finished_at===null?last.cell:null});
    if(argv[0]==='models')return{exit_code:0,timed_out:false,signal:null,stdout:Buffer.from('{"models":[{"id":"gemini-3.7-flash-high"},{"id":"other-model"}]}'),stderr:Buffer.alloc(0)};
    return{exit_code:0,timed_out:false,signal:null,stdout:agyStdout(syntheticItems().map(x=>({item_id:x.item_id,candidates:[]}))),stderr:Buffer.alloc(0)};
  };
  captureQualification(root,{invoke:spy,repoRoot:repo});
  assert.deepEqual(seen[0],{argv0:'models',rows:1,open:MODEL_LIST_CELL},'models list is journaled before it is spawned');
  assert.deepEqual(seen[1],{argv0:'-p',rows:3,open:SYNTHETIC_CELL},'the synthetic request is journaled before it is spawned');
  const rows=readRows(root).rows;
  assert.deepEqual(rows.map(r=>Object.keys(r)),rows.map(()=>ROW_KEYS),'same seven-key row shape as an execution cell');
  assert.deepEqual(rows.map(r=>`${r.cell}:${r.finished_at===null?'START':'FINISH'}`),
    [`${MODEL_LIST_CELL}:START`,`${MODEL_LIST_CELL}:FINISH`,`${SYNTHETIC_CELL}:START`,`${SYNTHETIC_CELL}:FINISH`]);
  assert.deepEqual(QUALIFICATION_CELLS,['qualification-models-list','qualification-synthetic']);
  const st=deriveState(root);
  assert.deepEqual(st.errors,[]);
  assert.equal(st.agy_processes_spawned,2);
  assert.equal(st.inference_calls_made,1,'models list is the one non-inference process');
});
await test('C15 process count is DERIVED from the ledger: a failed-then-retried capture counts 3, not 2',()=>{
  const {repo,root,manifest_sha256}=reviewedRepo();
  const counter={n:0,argvs:[]};
  // attempt 1 of the synthetic request exits non-zero; attempt 2 succeeds
  const invoke=qualificationInvoke(counter,{syntheticExits:[7]});
  assert.throws(()=>captureQualification(root,{invoke,repoRoot:repo}),/SYNTHETIC_EXIT/);
  assert.equal(deriveState(root).agy_processes_spawned,2);
  // retried under the SAME [1] / [1,2] attempt rule, with no manual file deletion:
  // captures are attempt-numbered and the successful models-list capture is reused, not respawned
  const before=counter.n;
  captureQualification(root,{invoke,repoRoot:repo});
  assert.equal(counter.n,before+1,'only the failed cell is respawned');
  const st=deriveState(root);
  assert.deepEqual(st.errors,[]);
  assert.deepEqual(st.cells[MODEL_LIST_CELL].attempt_numbers,[1]);
  assert.deepEqual(st.cells[SYNTHETIC_CELL].attempt_numbers,[1,2]);
  assert.equal(st.agy_processes_spawned,3,'three processes were really spawned');
  assert.equal(st.inference_calls_made,2);
  assert.ok(fs.existsSync(path.join(root,ledgerCapturePaths(SYNTHETIC_CELL,1).stdout)),'the failed attempt keeps its own capture');
  assert.ok(fs.existsSync(path.join(root,ledgerCapturePaths(SYNTHETIC_CELL,2).stdout)));
  // finalize, and confirm no process count is stored as a constant anywhere in the evidence
  write(path.join(repo,CAPTURE_RECEIPT_PATH),{schema_version:'gemini-context-v5-qualification-capture-receipt-v1',task_id:TASK_ID,purpose:'route_qualification_capture',dispatch_id:'d',agent_id:'a',archive_confirmed:true,manifest_sha256,draft_sha256:shaFile(path.join(root,qfiles.draft))});
  finalizeQualification(root,{repoRoot:repo});
  for(const doc of [readCanonical(path.join(root,qfiles.evidence)),readCanonical(path.join(root,qfiles.draft))])
    for(const k of ['agy_processes_spawned','inference_calls_made'])
      assert.ok(!(k in doc),`${k} must not be a constant in qualification evidence`);
  const v=validateQualification(root,{repoRoot:repo});
  assert.equal(v.valid,true,v.errors.join(','));
  assert.equal(v.agy_processes_spawned,3,'derived from the ledger, not from EVIDENCE.json');
  assert.equal(readCanonical(path.join(root,qfiles.evidence)).capture_attempts[SYNTHETIC_CELL],2);
  // budget arithmetic still totals correctly: the 4th process is the pilot cell, the 5th is refused
  authorize(repo,root,manifest_sha256);
  const cells={n:0};
  runCell(AUTHORIZED[0],{root,repoRoot:repo,invoke:cellInvoke(cells)});
  const pf=preflight(root,{repoRoot:repo});
  assert.equal(pf.agy_processes_spawned,4);
  assert.equal(pf.inference_calls_made,3);
  assert.throws(()=>runCell(AUTHORIZED[1],{root,repoRoot:repo,invoke:cellInvoke(cells)}),/STOP_BUDGET:4\/4/);
  assert.equal(cells.n,1);
  assert.equal(postRun(root,{repoRoot:repo}).agy_processes_spawned,4);
});
await test('C15 a fourth process is refused with STOP_BUDGET when only three are authorized',()=>{
  const {repo,root,manifest_sha256}=reviewedRepo();
  const counter={n:0,argvs:[]},invoke=qualificationInvoke(counter,{syntheticExits:[7]});
  assert.throws(()=>captureQualification(root,{invoke,repoRoot:repo}),/SYNTHETIC_EXIT/);
  captureQualification(root,{invoke,repoRoot:repo});
  write(path.join(repo,CAPTURE_RECEIPT_PATH),{schema_version:'gemini-context-v5-qualification-capture-receipt-v1',task_id:TASK_ID,purpose:'route_qualification_capture',dispatch_id:'d',agent_id:'a',archive_confirmed:true,manifest_sha256,draft_sha256:shaFile(path.join(root,qfiles.draft))});
  finalizeQualification(root,{repoRoot:repo});
  assert.equal(deriveState(root).agy_processes_spawned,3);
  authorize(repo,root,manifest_sha256,{agy_process_budget:3,inference_call_budget:2});
  const cells={n:0};
  assert.throws(()=>runCell(AUTHORIZED[0],{root,repoRoot:repo,invoke:cellInvoke(cells)}),/STOP_BUDGET:3\/3/);
  assert.equal(cells.n,0,'nothing is spawned once the budget is spent');
  // and the SPEC 6 ceiling is enforced on qualification itself, before any authorization exists
  assert.equal(PILOT_AGY_PROCESS_CEILING,4);
  const over=readCanonical(path.join(repo,gatePaths.EXECUTION_AUTHORIZATION));
  over.agy_process_budget=40;fs.rmSync(path.join(repo,gatePaths.EXECUTION_AUTHORIZATION));write(path.join(repo,gatePaths.EXECUTION_AUTHORIZATION),over);
  assert.ok(validateGates(root,{repoRoot:repo}).errors.includes('EXECUTION_AUTHORIZATION:BUDGET'));
});

/* ------------------------------------------------------------------ F3 (advisory) */
await test('F3 an exit-0 attempt with an unextractable envelope is FINISHED_RETRYABLE, so attempt 2 is allowed',()=>{
  const f=setup(),counter={n:0},cell=AUTHORIZED[0];
  // exit 0, but stdout is not an agy envelope
  const bad=runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter,{exit:0,stdout:Buffer.from('{"status":"SUCCESS"}\n')})});
  assert.equal(bad.exit,0,'the true exit code is journaled unchanged');
  assert.equal(bad.success,false);
  assert.equal(bad.state,'FINISHED_RETRYABLE');
  assert.equal(bad.classification,'ENVELOPE_UNPARSEABLE');
  assert.equal(bad.retryable,true);
  assert.ok(!fs.existsSync(path.join(f.root,rawPath(cell,1))),'no RAW for an unextractable attempt');
  const st=deriveState(f.root);
  assert.deepEqual(st.errors,[]);
  assert.equal(st.cells[cell].attempts[0].state,'FINISHED_RETRYABLE');
  assert.equal(nextAttempt(st,cell).attempt,2,'STOP_PARSE follows the attempt rule, not a single attempt');
  const good=runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)});
  assert.equal(good.attempt,2);
  assert.equal(good.success,true);
  assert.equal(counter.n,2);
  // C10 is intact: a genuine success whose RAW is missing still re-derives and never re-invokes
  const rp=path.join(f.root,rawPath(cell,2)),before=fs.readFileSync(rp);
  fs.rmSync(rp);
  const d=deriveRaw(f.root,cell,2,{repoRoot:f.repo});
  assert.equal(counter.n,2,'re-derivation must not spawn');
  assert.ok(fs.readFileSync(rp).equals(before));
  assert.equal(d.raw_sha256,good.raw_sha256);
});

// A frozen copy of the package: the request byte streams only exist after a freeze.
const frozenRoot=(()=>{const {root}=baseRepo();freeze(root);return root})();

/* ------------------------------------------------------------------ F1 (advisory) */
await test('F1 the env allowlist carries agy config and credential names, and no env value reaches argv',()=>{
  const route=readCanonical(path.join(here,'ROUTE-CONTRACT.json'));
  for(const k of ['HOME','XDG_CONFIG_HOME','XDG_CACHE_HOME','XDG_DATA_HOME','TMPDIR','GEMINI_API_KEY','GOOGLE_API_KEY','GOOGLE_APPLICATION_CREDENTIALS','GOOGLE_CLOUD_PROJECT','AGY_ADC_AUTH'])
    assert.ok(route.environment.allowlist.includes(k),`allowlist must carry ${k}`);
  assert.equal(new Set(route.environment.allowlist).size,route.environment.allowlist.length);
  assert.equal(route.environment.credentials_never_substituted_into_argv,true);
  // every allowlisted variable is passed through as an environment value and NEVER as argv text
  const saved=Object.fromEntries(route.environment.allowlist.map(k=>[k,process.env[k]]));
  const sentinel=k=>`SENTINEL-VALUE-FOR-${k}-8f3a1c`;
  try{
    for(const k of route.environment.allowlist)process.env[k]=sentinel(k);
    const p=plan(frozenRoot,requestEntry(frozenRoot,'discovery-A-run-1-shard-1'));
    for(const k of route.environment.allowlist){
      assert.equal(p.env[k],sentinel(k),`${k} must reach the process environment`);
      for(const token of p.argv)assert.ok(!String(token).includes(sentinel(k)),`${k} value leaked into argv`);
      assert.ok(!p.request.includes(sentinel(k)),`${k} value leaked into the request bytes`);
    }
    const qArgv=route.qualification.synthetic_argv.map(x=>x==='[SYNTHETIC_REQUEST_BYTES]'?'REQUEST':x==='[BUNDLE_SCHEMA]'?'SCHEMA':x);
    for(const k of route.environment.allowlist)for(const token of [...qArgv,...route.qualification.model_list_argv])assert.ok(!String(token).includes(sentinel(k)));
  }finally{for(const [k,v] of Object.entries(saved))if(v===undefined)delete process.env[k];else process.env[k]=v}
});

/* ------------------------------------------------------------------ F6 (advisory) */
await test('F6 the outer spawn timeout has headroom over the CLI --print-timeout',()=>{
  const route=readCanonical(path.join(here,'ROUTE-CONTRACT.json'));
  assert.equal(route.cli_contract.timeout_ms,1620000);
  for(const argv of [route.cli_contract.argv_template,route.qualification.synthetic_argv]){
    const i=argv.indexOf('--print-timeout');
    assert.ok(i>=0);
    assert.equal(argv[i+1],'25m');
    assert.ok(route.cli_contract.timeout_ms>25*60*1000,'the outer timeout must not race the CLI timeout');
    assert.equal(route.cli_contract.timeout_ms-25*60*1000,120000);
    assert.equal(argvModel(argv),'gemini-3.7-flash-high');
  }
  assert.equal(plan(frozenRoot,requestEntry(frozenRoot,'discovery-A-run-1-shard-1')).timeout_ms,1620000);
});

/* ------------------------------------------------------------------ F8 (advisory) */
await test('F8 a partial freeze fails static integrity',()=>{
  const {root}=baseRepo();
  const empty=checkFreeze(root);
  assert.deepEqual(empty.errors,[]);
  assert.equal(empty.freeze_state.present,0,'an unfrozen tree is not a partial freeze');
  assert.equal(empty.freeze_state.partial,false);
  freeze(root);
  const full=checkFreeze(root);
  assert.deepEqual(full.errors,[]);
  assert.equal(full.freeze_state.partial,false);
  assert.equal(full.freeze_state.present,full.freeze_state.targets);
  assert.equal(full.freeze_state.targets,35);   // 3 frozen documents + 32 request byte streams
  // remove exactly one frozen target: the tree is now neither unfrozen nor frozen
  const victim=buildFromRoot(root).requests[7].path;
  fs.rmSync(path.join(root,victim));
  const partial=checkFreeze(root);
  assert.equal(partial.freeze_state.partial,true);
  assert.ok(partial.errors.some(x=>x.startsWith('FREEZE_PARTIAL:34/35')),partial.errors.join(','));
  const pf=preflight(root,{repoRoot:realRepo});
  assert.equal(pf.static_integrity,'FAIL');
  assert.equal(pf.decision,'NO_GO_STATIC_INTEGRITY');
  assert.ok(pf.integrity_errors.some(x=>x.startsWith('freeze:FREEZE_PARTIAL')),pf.integrity_errors.join(','));
  // and the same partial tree is still completable by re-running the freeze
  freeze(root);
  assert.deepEqual(checkFreeze(root).errors,[]);
  assert.equal(freezeState(root,buildFromRoot(root)).partial,false);
});

/* ------------------------------------------------------------------ gates */
await test('three gates only, in order, each bound to manifest_sha256 and its predecessor',()=>{
  assert.deepEqual(GATE_ORDER,['PACKAGE_REVIEW','QUALIFICATION','EXECUTION_AUTHORIZATION']);
  const f=setup();
  const g=validateGates(f.root,{repoRoot:f.repo});
  assert.equal(g.valid,true,g.errors.join(','));
  // a repackaged manifest invalidates every gate bound to the old one
  fs.appendFileSync(path.join(f.root,'README.md'),'drift');
  assert.ok(checkManifest(f.root).some(x=>x.startsWith('MANIFEST_HASH_DRIFT')));
  write(path.join(f.root,'MANIFEST.json'),buildManifest(f.root));
  assert.deepEqual(checkManifest(f.root),[]);
  const drifted=validateGates(f.root,{repoRoot:f.repo});
  assert.equal(drifted.valid,false);
  assert.equal(drifted.errors.filter(x=>x.endsWith('MANIFEST_BINDING')).length,3);
  // out-of-order: removing the middle gate blocks the last one
  const g2=setup();
  fs.rmSync(path.join(g2.repo,gatePaths.QUALIFICATION));
  const r=validateGates(g2.root,{repoRoot:g2.repo});
  assert.equal(r.valid,false);
  assert.ok(r.errors.includes('QUALIFICATION:ABSENT'));
  assert.ok(r.errors.some(x=>x.startsWith('EXECUTION_AUTHORIZATION:PREDECESSOR')));
});

/* ------------------------------------------------------------------ C08 / C10 / C13 */
await test('C13 NO_RUN is reported only for an entirely empty execution/',()=>{
  const {root}=baseRepo();
  assert.equal(executionEmpty(root),true);
  assert.equal(postRun(root).decision,'NO_RUN');
  fs.mkdirSync(path.join(root,'execution'),{recursive:true});
  assert.equal(executionEmpty(root),true,'an empty directory is still NO_RUN');
  assert.equal(postRun(root).decision,'NO_RUN');
  fs.writeFileSync(path.join(root,LEDGER_PATH),JSON.stringify({attempt:1,cell:'discovery-A-run-1-shard-1',started_at:'2026-09-02T00:00:00.000Z',finished_at:null,exit:null,stdout_sha256:null,stderr_sha256:null})+'\n');
  assert.equal(executionEmpty(root),false);
  assert.notEqual(postRun(root).decision,'NO_RUN','any ledger row makes it non-NO_RUN');
});
await test('C08 the run reconstructed from the ledger equals the runner view',()=>{
  const f=setup();
  const counter={n:0};
  const views=AUTHORIZED.map(cell=>runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter,{findOn:x=>x.item_id==='D-I001'})}));
  assert.equal(counter.n,2);
  for(const v of views)assert.equal(v.success,true,JSON.stringify(v));
  const rec=reconstruct(f.root,{repoRoot:f.repo});
  assert.deepEqual(rec.errors,[]);
  assert.deepEqual(rec.cells.map(x=>x.cell),[...AUTHORIZED].sort());
  for(const v of views){
    const r=rec.cells.find(x=>x.cell===v.cell);
    assert.equal(r.successful_attempt,v.attempt);
    assert.equal(r.raw_path,v.raw_path);
    assert.equal(r.raw_sha256,v.raw_sha256);
    assert.equal(r.success,true);
  }
  // and the ledger is the only state: no STATE.json anywhere in the package
  assert.ok(!walk(f.root).some(x=>path.basename(x)==='STATE.json'));
  const rows=readRows(f.root);
  assert.deepEqual(rows.errors,[]);
  assert.equal(rows.rows.length,8);   // (2 qualification + 2 execution cells) x (START + FINISH)
  assert.deepEqual([...new Set(rows.rows.map(r=>r.cell))].sort(),[...AUTHORIZED,...QUALIFICATION_CELLS].sort());
  const pr=postRun(f.root,{repoRoot:f.repo,write:true});
  assert.equal(pr.decision,'PILOT_COMPLETE',JSON.stringify(pr.errors));
  assert.equal(pr.agy_processes_spawned,4);
  assert.equal(pr.inference_calls_made,3);
  assert.equal(pr.scores.totals.clean_with_findings,2);
  const first=shaFile(path.join(f.root,'SCORES.json'));
  const again=postRun(f.root,{repoRoot:f.repo,write:true});
  assert.equal(again.decision,'PILOT_COMPLETE');
  assert.equal(shaFile(path.join(f.root,'SCORES.json')),first,'SCORES must be byte-identical on a rerun');
});
await test('C10 a FINISHED success with no RAW re-derives RAW from captured stdout, never a new call',()=>{
  const f=setup();
  const counter={n:0},cell=AUTHORIZED[0];
  const v=runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)});
  assert.equal(counter.n,1);
  const rp=path.join(f.root,rawPath(cell,v.attempt)),before=fs.readFileSync(rp);
  fs.rmSync(rp);
  const rowsBefore=readRows(f.root).rows.length;
  const d=deriveRaw(f.root,cell,v.attempt,{repoRoot:f.repo});   // no invoke parameter exists
  assert.equal(counter.n,1,'derivation must not spawn');
  assert.equal(readRows(f.root).rows.length,rowsBefore,'derivation must not append a ledger row');
  assert.ok(fs.readFileSync(rp).equals(before),'re-derived RAW must be byte-identical');
  assert.equal(d.raw_sha256,v.raw_sha256);
  assert.equal(d.parsed.valid,true,d.parsed.errors.join(','));
  assert.ok(!/\binvoke\b/u.test(String(deriveRaw)),'deriveRaw must have no invoke path');
  // a corrupted capture cannot be laundered into RAW
  fs.rmSync(rp);
  fs.appendFileSync(path.join(f.root,capturePaths(cell,v.attempt).stdout),' ');
  assert.throws(()=>deriveRaw(f.root,cell,v.attempt,{repoRoot:f.repo}),/CAPTURE_HASH_MISMATCH/);
});
await test('runner refuses unauthorized cells, exhausted attempts and a spent budget',()=>{
  const f=setup(),counter={n:0};
  assert.throws(()=>runCell('discovery-B-run-1-shard-1',{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)}),/CELL_NOT_AUTHORIZED/);
  assert.equal(counter.n,0);
  runCell(AUTHORIZED[0],{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)});
  assert.throws(()=>runCell(AUTHORIZED[0],{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)}),/ATTEMPT_BLOCKED.*ALREADY_SUCCEEDED/);
  assert.equal(counter.n,1);
  // budget: qualification (2) + this cell (1) + one more = 4, a fifth process is refused
  runCell(AUTHORIZED[1],{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)});
  assert.equal(counter.n,2);
  const g=validateGates(f.root,{repoRoot:f.repo}).gates.EXECUTION_AUTHORIZATION;
  assert.equal(g.agy_process_budget,4);
  const extra=setup(),c2={n:0};
  const auth=readCanonical(path.join(extra.repo,gatePaths.EXECUTION_AUTHORIZATION));
  auth.authorized_cells=['discovery-A-run-1-shard-1','discovery-C-run-1-shard-1'];
  auth.agy_process_budget=3;auth.inference_call_budget=2;
  write(path.join(extra.repo,gatePaths.EXECUTION_AUTHORIZATION),auth);
  runCell('discovery-A-run-1-shard-1',{root:extra.root,repoRoot:extra.repo,invoke:cellInvoke(c2)});
  assert.throws(()=>runCell('discovery-C-run-1-shard-1',{root:extra.root,repoRoot:extra.repo,invoke:cellInvoke(c2)}),/STOP_BUDGET/);
  assert.equal(c2.n,1);
});
await test('a non-zero exit writes no RAW, and the retry is attempt 2 only',()=>{
  const f=setup(),counter={n:0},cell=AUTHORIZED[0];
  const bad=runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter,{exit:9,stdout:Buffer.from('{bad')})});
  assert.equal(bad.success,false);
  assert.equal(bad.raw_path,null);
  assert.ok(!fs.existsSync(path.join(f.root,rawPath(cell,1))));
  const good=runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)});
  assert.equal(good.attempt,2);
  assert.equal(good.success,true);
  // the two attempts plus the two qualification processes exhaust the 4-process budget
  assert.throws(()=>runCell(cell,{root:f.root,repoRoot:f.repo,invoke:cellInvoke(counter)}),/STOP_BUDGET:4\/4/);
  assert.equal(counter.n,2);
  const rec=reconstruct(f.root,{repoRoot:f.repo});
  assert.deepEqual(rec.errors,[]);
  assert.equal(rec.cells[0].successful_attempt,2);
});

/* ------------------------------------------------------------------ preflight */
await test('preflight passes static integrity, reports NO_RUN and zero calls, blocks on gates',()=>{
  const r=preflight(here,{repoRoot:realRepo});
  assert.deepEqual(r.integrity_errors,[]);
  assert.equal(r.static_integrity,'PASS');
  assert.equal(r.execution_state,'NO_RUN');
  assert.equal(r.agy_processes_spawned,0);
  assert.equal(r.inference_calls_made,0);
  assert.equal(r.network_calls_made,0);
  assert.equal(r.decision,'NO_GO_REQUIRED_GATES');
  assert.deepEqual(r.blocked_gates,GATE_ORDER);
  const f=setup();
  const g=preflight(f.root,{repoRoot:f.repo});
  assert.deepEqual(g.integrity_errors,[]);
  assert.equal(g.decision,'GO');
  assert.equal(g.agy_processes_spawned,2);
});
await test('replay of the terminal V5 frame yields 64 bases and 30 round bindings',()=>{
  const out=replay(realRepo);
  assert.equal(out.base.items.length,64);
  assert.equal(out.bindings.round_artifacts.length,30);
  assert.equal(out.bindings.predecessor_trees.length,3);
  assert.ok(jsonBytes(out.base).equals(fs.readFileSync(path.join(here,'frozen/BASES.json'))));
});

if(process.exitCode)process.exit(process.exitCode);
console.log(`1..${n}`);
