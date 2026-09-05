#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateRound3RawSurfaceResponse} from './round-0003-surface-results.mjs';
import {assertNoRound3ContextLeakage,buildRound3ContextInput,CONTEXT_IDS,jsonBytes,OUTPUT_HASHES,validateRound3ContextCandidate,validateRound3ContextInput,validateRound3RuntimeBinding} from './round-0003-context-input.mjs';
import {replayRound3Context} from './round-0003-context-replay.mjs';
import {runRound3ContextPreflight} from './round-0003-context-preflight.mjs';
import {publicContextReplay} from './public-context-replay.mjs';
import {publicContextPreflight} from './public-context-preflight.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(here,'..','..','..','..'),round=path.join(here,'rounds/ROUND-0003');
const actual=validateRound3ContextInput({root:here,repo}),candidate=validateRound3ContextCandidate(repo),view=JSON.parse(fs.readFileSync(path.join(round,'CONTEXT-QUEUE-VIEW.json'))),anchors=JSON.parse(fs.readFileSync(path.join(round,'CONTEXT-SOURCE-ANCHORS.json')));
assert.deepEqual(view.items.map(x=>x.neutral_id),CONTEXT_IDS);assert.equal(actual.item_count,2);assert.equal(actual.source_file_count,2);assert.equal(anchors.file_count,2);assert.doesNotThrow(()=>assertNoRound3ContextLeakage(view));
for(const forbidden of ['lineage','reserve','verdict','evidence','rejected','rank','reviewer','model','reference','adjudicat'])assert.equal(JSON.stringify(view).toLowerCase().includes(`"${forbidden}`),false,forbidden);
const raw=fs.readFileSync(path.join(here,'AUDITOR-RESPONSE-ROUND-0003-SURFACE-CALL-001.json'));assert.equal(raw.at(-1),'}'.charCodeAt(0));assert.equal(raw.includes(Buffer.from('\n')),false);assert.equal(validateRound3RawSurfaceResponse({root:here}).response.results.length,2);
const built=buildRound3ContextInput({root:here,repo});assert.ok(built.queueBytes.equals(fs.readFileSync(path.join(round,'CONTEXT-QUEUE.json'))));assert.ok(built.anchorsBytes.equals(fs.readFileSync(path.join(round,'CONTEXT-SOURCE-ANCHORS.json'))));assert.ok(built.viewBytes.equals(fs.readFileSync(path.join(round,'CONTEXT-QUEUE-VIEW.json'))));
assert.deepEqual([actual.context_queue_sha256,actual.context_source_anchors_sha256,actual.context_queue_view_sha256],[OUTPUT_HASHES.queue,OUTPUT_HASHES.anchors,OUTPUT_HASHES.view]);
const anchorFiles=new Map(anchors.files.map(x=>[x.public_source_file,x]));
for(const [label,mutate]of[['stale-coordinate',x=>x.occurrence.line++],['file-boundary',x=>x.runtime_context.before.sentinel='[[CONTEXT_FILE_START]]']]){const item=structuredClone(view.items[0]);mutate(item);assert.throws(()=>validateRound3RuntimeBinding(item,anchors.items[0],anchorFiles.get(item.public_source_file)),/ROUND3_CONTEXT_RUNTIME|ROUND3_CONTEXT_ANCHOR/u,label);}
const replay=publicContextReplay();assert.equal(replay.completed_rounds,2);assert.equal(replay.public_phase,'ROUND_0003_CONTEXT_INPUT');assert.equal(replay.context_auditor_call_authorized,false);const preflight=publicContextPreflight();assert.equal(preflight.decision,'NO_GO_ROUND_0003_CONTEXT_INPUT_REVIEW_REQUIRED');assert.equal(preflight.static_integrity,'PASS');assert.equal(runRound3ContextPreflight().decision,preflight.decision);assert.equal(replayRound3Context().candidate_ref,candidate.candidate_ref);
function fixture(){const base=fs.mkdtempSync(path.join(os.tmpdir(),'v5-r3-context-')),r=path.join(base,'repo');fs.mkdirSync(path.join(r,'.ai/task'),{recursive:true});fs.cpSync(here,path.join(r,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5'),{recursive:true});fs.cpSync(path.join(repo,'.ai/task/research-gemini-context-counterexample-reviewer-v5'),path.join(r,'.ai/task/research-gemini-context-counterexample-reviewer-v5'),{recursive:true});return {base,repo:r,root:path.join(r,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5'),round:path.join(r,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0003')};}
function rejects(label,mutate,pattern=/ROUND3|ROUND4|CONTEXT|CANDIDATE|FILE_TYPE|ENOENT/u){const t=fixture();try{mutate(t);assert.throws(()=>replayRound3Context(t.root,t.repo),pattern,label);}finally{fs.rmSync(t.base,{recursive:true,force:true});}}
rejects('tamper',t=>{const f=path.join(t.round,'CONTEXT-QUEUE-VIEW.json'),v=JSON.parse(fs.readFileSync(f));v.items[0].target+='x';fs.writeFileSync(f,jsonBytes(v));});
rejects('stale-coordinate',t=>{const f=path.join(t.round,'CONTEXT-QUEUE-VIEW.json'),v=JSON.parse(fs.readFileSync(f));v.items[0].occurrence.line++;fs.writeFileSync(f,jsonBytes(v));});
rejects('file-boundary',t=>{const f=path.join(t.round,'CONTEXT-QUEUE-VIEW.json'),v=JSON.parse(fs.readFileSync(f));v.items[0].runtime_context.before.sentinel='[[CONTEXT_FILE_START]]';fs.writeFileSync(f,jsonBytes(v));});
rejects('missing',t=>fs.unlinkSync(path.join(t.round,'CONTEXT-SOURCE-ANCHORS.json')));
rejects('extra',t=>fs.writeFileSync(path.join(t.round,'CONTEXT-RECORDS.json'),'{}\n'));
rejects('noncanonical',t=>fs.appendFileSync(path.join(t.round,'CONTEXT-QUEUE.json'),' '));
rejects('symlink',t=>{const f=path.join(t.round,'CONTEXT-QUEUE-VIEW.json'),outside=path.join(t.base,'same.json');fs.copyFileSync(f,outside);fs.unlinkSync(f);fs.symlinkSync(outside,f);});
rejects('raw missing',t=>fs.unlinkSync(path.join(t.root,'AUDITOR-RESPONSE-ROUND-0003-SURFACE-CALL-001.json')));
rejects('ROUND4',t=>fs.mkdirSync(path.join(t.root,'rounds/ROUND-0004')));
{const duplicate=Buffer.from('{"schema_version":"gemini-context-v5-surface-auditor-response-v2","schema_version":"gemini-context-v5-surface-auditor-response-v2","queue_view_sha256":"f1f35c1a1c28638c706630b45422efa6b94380b8ff89397fecef78c4f3e6ca0b","results":[]}');assert.throws(()=>validateRound3RawSurfaceResponse({root:here,responseBytes:duplicate}),/DUPLICATE_KEY/u);}
console.log(JSON.stringify({status:'PASS',candidate_ref:candidate.candidate_ref,candidate_file_count:candidate.file_count,hashes:OUTPUT_HASHES,tests:['exact raw bytes/hash/schema/view/order/count','surface records and aggregate replay','exact context 2/order','fixed source anchors','self-contained no-leak view','generator reproduction','lstat/canonical/symlink/tamper/missing/extra','stale-coordinate/file-boundary','ROUND4 forbidden','public/dedicated replay and preflight completed_rounds=2']},null,2));
