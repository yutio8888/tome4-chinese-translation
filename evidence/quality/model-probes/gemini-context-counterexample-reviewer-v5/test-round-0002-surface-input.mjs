#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {runPreflight} from './preflight.mjs';
import {replay} from './replay.mjs';
import {jsonBytes, readRoundBundles, sha256} from './round-lineage.mjs';
import {ROUND1_HASHES, ROUND2_REPAIR_REVIEW_PATHS, validateFrozenRound1Files} from './round-0002-surface-input.mjs';
import {ROUND2_SURFACE_CALL, validateRound2RawSurfaceResponse, validateRound2SurfaceArtifacts} from './round-0002-surface-results.mjs';

const here=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(here,'..','..','..','..'),round2=path.join(here,'rounds','ROUND-0002');
const expectedPairs=[['V4-C-D04','9434af52c3e301a7cae6b3a98dd1f59fe1389044005dd001c47e296b3b5157e5'],['V4-D-D05','a75b87d16d74dd486b47c31f243306721f640023ad5d8fa9d3708d9e60ad7548'],['V4-C-D06','358d6a470b17724efda25d94a4e2a94359995915995cdc9715db603e86711614'],['V4-D-D07','7eb0d7e8fd088ecf540c5acec3a7e78f1b5732befddce462ace35f1222b49542'],['V4-D-D12','a000ce616a6c7be9934e0188fbb5846688ed8dc2b03872e1acf20fc72f448f63'],['V4-C-N01','e52429af5d339cbdbdfc10d53a7e31446e1f3c3ed8605ed00e219343baeeed9d'],['V4-D-N02','1df4e22846462f86ca706fcfef6f0c8a80aed59de7253564213841d47733006f'],['V4-C-N05','afa7ce681bd5715b93cd7f81df285157ae188fb3b5adb6257a0ba5f335af77b6'],['V4-D-N12','28d26866539824bd3b1ac8254145b6c6413bc60385007ea1442b620833517e9a'],['V4-C-N16','f5273e0635139d3454b91cb264334404b45b31ebcaf85202527ed01be281f350']];
const eligible=expectedPairs.map(x=>x[0]).filter(id=>id!=='V4-C-D06'),queueBytes=fs.readFileSync(path.join(round2,'SURFACE-QUEUE.json')),viewBytes=fs.readFileSync(path.join(round2,'SURFACE-QUEUE-VIEW.json')),responseBytes=fs.readFileSync(path.join(here,ROUND2_SURFACE_CALL.response_path)),queue=JSON.parse(queueBytes);
assert.equal(validateFrozenRound1Files(here),true);assert.deepEqual(queue.items.map(x=>[x.neutral_id,x.revision_id]),expectedPairs);assert.equal(queue.predecessor_release_sha256,ROUND1_HASHES.release);assert.equal(queue.active_frame_sha256,ROUND1_HASHES.active_frame);
assert.equal(fs.readdirSync(round2).sort().join(','),'CONTEXT-AGGREGATE.json,CONTEXT-QUEUE-VIEW.json,CONTEXT-QUEUE.json,CONTEXT-RECORDS.json,CONTEXT-SOURCE-ANCHORS.json,SURFACE-AGGREGATE.json,SURFACE-QUEUE-VIEW.json,SURFACE-QUEUE.json,SURFACE-RECORDS.json');const liveBundle=readRoundBundles(path.join(here,'rounds'),'ROUND-0002')[1];assert.equal(liveBundle.pending_surface_stage,true);assert.equal(liveBundle.pending_context_results,true);
const docs=replay(here),artifacts=validateRound2SurfaceArtifacts({root:here}),preflight=runPreflight(here);assert.equal(docs['ROUND-INDEX.json'].completed_rounds,1);assert.equal(sha256(jsonBytes(docs['ACTIVE-FRAME.json'])),ROUND1_HASHES.active_frame);assert.equal(preflight.decision,'NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED');assert.equal(preflight.static_integrity,'PASS');assert.equal(preflight.real_release_created,false);

function fixture(){const root=fs.mkdtempSync(path.join(os.tmpdir(),'v5-r2-results-')),packageDir=path.join(root,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5'),taskDir=path.join(root,'.ai/task/research-gemini-context-counterexample-reviewer-v5');fs.cpSync(here,packageDir,{recursive:true});fs.cpSync(path.join(repo,'.ai/task/research-gemini-context-counterexample-reviewer-v5'),taskDir,{recursive:true});return {root,packageDir,round:path.join(packageDir,'rounds/ROUND-0002')};}
function replayReject(label,mutate,pattern){const tmp=fixture();try{mutate(tmp);assert.throws(()=>replay(tmp.packageDir),pattern,label);}finally{fs.rmSync(tmp.root,{recursive:true,force:true});}}
for(const [label,mutate,pattern] of [
 ['records tamper',t=>{const f=path.join(t.round,'SURFACE-RECORDS.json'),v=JSON.parse(fs.readFileSync(f));v.items[0].evidence+='x';fs.writeFileSync(f,jsonBytes(v));},/SURFACE_/u],
 ['aggregate tamper',t=>{const f=path.join(t.round,'SURFACE-AGGREGATE.json'),v=JSON.parse(fs.readFileSync(f));v.pass_ids.pop();fs.writeFileSync(f,jsonBytes(v));},/SURFACE_AGGREGATE/u],
 ['raw tamper',t=>fs.appendFileSync(path.join(t.packageDir,ROUND2_SURFACE_CALL.response_path),' '),/ROUND2_SURFACE_RESPONSE_NONCANONICAL_BYTES|ROUND2_SURFACE_RESPONSE_HASH/u],
 ['missing',t=>fs.unlinkSync(path.join(t.round,'SURFACE-AGGREGATE.json')),/PENDING_ROUND_ARTIFACTS/u],
 ['extra context',t=>fs.writeFileSync(path.join(t.round,'CONTEXT-QUEUE.json'),'{}\n'),/PENDING_ROUND_ARTIFACTS|ROUND2_CONTEXT/u],
 ['round3',t=>{const d=path.join(t.packageDir,'rounds/ROUND-0003');fs.mkdirSync(d);fs.writeFileSync(path.join(d,'SURFACE-QUEUE.json'),'{}\n');},/ROUND_REQUIRED_ARTIFACT_MISSING|PENDING_ROUND_ARTIFACTS/u]
])replayReject(label,mutate,pattern);
{
 const raw=JSON.parse(responseBytes),semanticReject=(mutate,pattern)=>{const value=structuredClone(raw);mutate(value);const bytes=jsonBytes(value);assert.throws(()=>validateRound2RawSurfaceResponse({root:here,queueBytes,viewBytes,responseBytes:bytes,expectedResponseSha256:sha256(bytes)}),pattern);};
 semanticReject(v=>v.schema_version='bad',/ROUND2_SURFACE_RESPONSE_SCHEMA/u);semanticReject(v=>[v.results[0],v.results[1]]=[v.results[1],v.results[0]],/ROUND2_SURFACE_RESPONSE_ORDER_OR_DUPLICATE/u);semanticReject(v=>v.results[1].neutral_id=v.results[0].neutral_id,/ROUND2_SURFACE_RESPONSE_ORDER_OR_DUPLICATE/u);semanticReject(v=>v.results[0].evidence='',/ROUND2_SURFACE_RESPONSE_ITEM/u);semanticReject(v=>v.results[0].verdict='UNKNOWN',/ROUND2_SURFACE_RESPONSE_ITEM/u);
 const duplicate=Buffer.from(responseBytes.toString('utf8').replace('"schema_version":','"schema_version":"duplicate",\n  "schema_version":'));assert.throws(()=>validateRound2RawSurfaceResponse({root:here,queueBytes,viewBytes,responseBytes:duplicate,expectedResponseSha256:sha256(duplicate)}),/DUPLICATE_KEY/u);
}
for(const [label,mutate] of [['missing senior',t=>fs.unlinkSync(path.join(t.root,ROUND2_REPAIR_REVIEW_PATHS.senior))],['gate tamper',t=>{const f=path.join(t.root,ROUND2_REPAIR_REVIEW_PATHS.gate),v=JSON.parse(fs.readFileSync(f));v.auditor_contract.call_count_allowance=2;fs.writeFileSync(f,jsonBytes(v));}]]){const tmp=fixture();try{mutate(tmp);assert.equal(runPreflight(tmp.packageDir).static_integrity,'FAIL_CLOSED',label);}finally{fs.rmSync(tmp.root,{recursive:true,force:true});}}
{const tmp=fixture();try{assert.equal(replay(tmp.packageDir)['ROUND-INDEX.json'].completed_rounds,1);assert.equal(runPreflight(tmp.packageDir).decision,'NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED');}finally{fs.rmSync(tmp.root,{recursive:true,force:true});}}
assert.equal(validateFrozenRound1Files(here),true);assert.equal(fs.existsSync(path.join(round2,'CONTEXT-QUEUE.json')),true);assert.equal(fs.existsSync(path.join(round2,'CONTEXT-RECORDS.json')),true);assert.equal(fs.existsSync(path.join(round2,'RELEASE.json')),false);assert.equal(fs.existsSync(path.join(here,'rounds','ROUND-0003')),false);
console.log(JSON.stringify({status:'PASS',decision:preflight.decision,queue_sha256:sha256(queueBytes),view_sha256:sha256(viewBytes),...artifacts,context_eligible_ids:eligible,call_count:{allowance:1,started:1,remaining:0},negative_classes:['invalid-schema','order','duplicate-id','duplicate-key','empty-evidence','invalid-verdict','raw-tamper','records-tamper','aggregate-tamper','missing','extra','round3','gate'],clean_copy_replay:true,completed_rounds:1,state_unchanged:true},null,2));
