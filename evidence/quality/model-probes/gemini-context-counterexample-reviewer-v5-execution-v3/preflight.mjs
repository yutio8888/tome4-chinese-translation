#!/usr/bin/env node
// The single preflight. Static, read-only, spawns nothing, opens no socket.
// It answers: is the package internally consistent, are the predecessors byte-unchanged,
// which of the three gates are satisfied, and how many agy processes have been spawned.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readCanonical,jsonBytes,sha256} from './lib.mjs';
import {checkManifest,sourcePaths,manifestSha256,MANIFEST_PATH} from './build-manifest.mjs';
import {verifyPredecessorBindings} from './build-frozen-base.mjs';
import {checkFreeze} from './freezer.mjs';
import {scanRequestBytes,REQUEST_MAX_UTF8_BYTES} from './request-lib.mjs';
import {validateReference} from './scorer.mjs';
import {validateGates,GATE_ORDER} from './gates.mjs';
import {validateQualification} from './qualification.mjs';
import {deriveState} from './ledger.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),defaultRepo=path.resolve(here,'../../../..');
// C03: every JSON file in the package parses, rejects duplicate keys, and is canonical.
export function jsonIntegrity(root=here){
  const errors=[];
  for(const rel of [MANIFEST_PATH,...sourcePaths(root)]){
    if(!rel.endsWith('.json'))continue;
    try{const v=readCanonical(path.join(root,rel));if(!jsonBytes(v).equals(fs.readFileSync(path.join(root,rel))))errors.push(`JSON_ROUND_TRIP:${rel}`)}
    catch(e){errors.push(`JSON:${e.message}`)}
  }
  return errors;
}
// C05: no forbidden internal identifier or marker in any of the 32 rendered requests.
export function leakageScan(built){
  const errors=[];
  for(const r of built.requests){
    for(const x of scanRequestBytes(r.bytes))errors.push(`REQUEST_LEAK:${r.path}:${x}`);
    if(r.utf8_bytes>REQUEST_MAX_UTF8_BYTES)errors.push(`REQUEST_SIZE:${r.path}`);
  }
  return errors;
}
export function preflight(root=here,{repoRoot=defaultRepo}={}){
  const integrity=[],blocked=[];
  let built=null,state=null,q=null;
  try{
    integrity.push(...checkManifest(root).map(x=>`manifest:${x}`));
    integrity.push(...verifyPredecessorBindings(root,repoRoot).map(x=>`predecessor:${x}`));
    integrity.push(...jsonIntegrity(root));
    const f=checkFreeze(root);integrity.push(...f.errors.map(x=>`freeze:${x}`));built=f.built;
    if(built){
      integrity.push(...leakageScan(built));
      integrity.push(...validateReference(built.reference,built.sampleDoc,sha256(jsonBytes(built.reference))).map(x=>`reference:${x}`));
      const bases=readCanonical(path.join(root,'frozen/BASES.json'));
      if(bases.items.length!==64)integrity.push('BASE_COUNT');
      if(built.requests.length!==32)integrity.push('REQUEST_COUNT');
    }
    state=deriveState(root);integrity.push(...state.errors.map(x=>`ledger:${x}`));
    q=validateQualification(root,{repoRoot});
  }catch(e){integrity.push(`EXCEPTION:${e.message}`)}
  const gates=validateGates(root,{repoRoot});
  for(const g of GATE_ORDER)if(!gates.present[g])blocked.push(g);
  // C15: both counters are derived from the ledger's START rows -- qualification journals its
  // two processes in the same ledger, so nothing is added from qualification/EVIDENCE.json.
  const agy_processes_spawned=state?.agy_processes_spawned??0;
  const inference_calls_made=state?.inference_calls_made??0;
  const execution_state=state?.no_run?'NO_RUN':'PARTIAL_OR_COMPLETE';
  return{
    schema_version:'gemini-context-v5-execution-preflight-v1',
    experiment_id:'gemini-context-counterexample-reviewer-v5-execution-v3',
    manifest_sha256:(()=>{try{return manifestSha256(root)}catch{return null}})(),
    decision:integrity.length?'NO_GO_STATIC_INTEGRITY':blocked.length?'NO_GO_REQUIRED_GATES':'GO',
    static_integrity:integrity.length?'FAIL':'PASS',
    execution_state,
    gates_present:gates.present,
    blocked_gates:blocked,
    integrity_errors:integrity,
    qualification_status:q?.status??'NOT_RUN',
    agy_processes_spawned,
    inference_calls_made,
    network_calls_made:0
  };
}
if(import.meta.url===`file://${process.argv[1]}`){const r=preflight();console.log(JSON.stringify(r,null,2));process.exitCode=r.decision==='GO'?0:3}
