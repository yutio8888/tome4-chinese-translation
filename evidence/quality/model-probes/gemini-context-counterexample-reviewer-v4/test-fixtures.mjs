#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {replaceRejectedRows,assertFrameCaps,remainingRejectionTolerance} from './selection-lib.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const read=(d,n)=>JSON.parse(fs.readFileSync(path.join(d,n),'utf8'));
const frame=read(here,'FROZEN-RANKED-64-FRAME.json');

function installSurfaceEvidence(tmp, items){
  const queue=read(here,'SURFACE-AUDIT-QUEUE.json');fs.copyFileSync(path.join(here,'SURFACE-AUDIT-QUEUE.json'),path.join(tmp,'SURFACE-AUDIT-QUEUE.json'));
  const aggregate={schema_version:'gemini-context-surface-audit-aggregate-v1',stage:'SURFACE',queue_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(tmp,'SURFACE-AUDIT-QUEUE.json'))).digest('hex'),accepted_count:0,accepted_ids:[],items:items.map(x=>({neutral_id:x.neutral_id,revision_id:x.revision_id??frame.items.find(q=>q.neutral_id===x.neutral_id)?.revision_id,verdict:x.reason}))};
  fs.writeFileSync(path.join(tmp,'SURFACE-AUDIT-AGGREGATE.json'),`${JSON.stringify(aggregate,null,2)}\n`);const ah=crypto.createHash('sha256').update(fs.readFileSync(path.join(tmp,'SURFACE-AUDIT-AGGREGATE.json'))).digest('hex');
  fs.writeFileSync(path.join(tmp,'AUDIT-RELEASE-STATE.json'),`${JSON.stringify({surface_released:true,surface_queue_sha256:aggregate.queue_sha256,surface_aggregate_sha256:ah},null,2)}\n`);
}
function runRejections(count){
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'v4-replace-'));
  const items=frame.items.filter(x=>x.profile==='narrative').slice(0,count)
    .map((x,i)=>({neutral_id:x.neutral_id,revision_id:x.revision_id,reason:i===0?'OUT_OF_SCOPE_NON_PROSE':'NOT_CLEAN'}));
  const ledgerPath=path.join(tmp,'reject.json');
  fs.writeFileSync(ledgerPath,`${JSON.stringify({items},null,2)}\n`);
  fs.writeFileSync(path.join(tmp,'REJECTED-BASES-INPUT.json'),`${JSON.stringify({schema_version:'gemini-context-v4-rejected-bases-input-v1',items:[]},null,2)}\n`);installSurfaceEvidence(tmp,items);
  const run=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--freeze-rejections'],{encoding:'utf8',env:{...process.env,V4_OUTPUT_DIR:tmp,V4_REJECTED_BASES_PATH:ledgerPath,V4_CANONICAL_INPUT_SHA256:crypto.createHash('sha256').update(fs.readFileSync(path.join(tmp,'REJECTED-BASES-INPUT.json'))).digest('hex')}});
  assert.equal(run.status,0,run.stderr);
  return {tmp,ledger:read(tmp,'REPLACEMENT-LEDGER.json'),source:read(tmp,'SOURCE-FRAME.json'),availability:read(tmp,'AVAILABILITY.json')};
}

for(const count of [1,28,29]){
  const result=runRejections(count);
  assert.equal(result.ledger.items.length,count);
  assert.match(result.ledger.previous_rejected_base_input_sha256,/^[0-9a-f]{64}$/u);
  assert.equal(result.availability.initial_narrative_reserve_rows,78);
  assert.equal(result.availability.consumed_narrative_replacements,count);
  assert.equal(result.availability.remaining_narrative_rejection_tolerance,78-count);
  assert.equal(result.availability.reserve_narrative_rows,78-count);
  assert.equal(result.availability.initial_consumed_narrative_replacements,0);
  assert.equal(result.availability.remaining_narrative_rejection_tolerance,result.availability.reserve_narrative_rows);
  const frozen=spawnSync(process.execPath,[path.join(here,'freeze-hashes.mjs')],{encoding:'utf8',env:{...process.env,V4_OUTPUT_DIR:result.tmp}});assert.equal(frozen.status,0,frozen.stderr);
  assert.deepEqual(result.source.items.map(x=>x.neutral_id),frame.items.map(x=>x.neutral_id));
  fs.rmSync(result.tmp,{recursive:true,force:true});
}

const bannedReserve=frame.items.length;
const reserveInput=read(here,'RANKED-SAME-PROFILE-RESERVE.json').items.find(x=>x.profile==='narrative');
assert.ok(reserveInput?.revision_id);
const bannedTmp=fs.mkdtempSync(path.join(os.tmpdir(),'v4-banned-reserve-'));
const bannedLedger=path.join(bannedTmp,'reject.json');const bannedItem=frame.items.find(x=>x.profile==='narrative');fs.writeFileSync(bannedLedger,`${JSON.stringify({items:[{neutral_id:bannedItem.neutral_id,revision_id:bannedItem.revision_id,reason:'NOT_CLEAN'}]},null,2)}\n`);fs.writeFileSync(path.join(bannedTmp,'REJECTED-BASES-INPUT.json'),`${JSON.stringify({schema_version:'gemini-context-v4-rejected-bases-input-v1',items:[]},null,2)}\n`);installSurfaceEvidence(bannedTmp,[{neutral_id:bannedItem.neutral_id,reason:'NOT_CLEAN'}]);
const bannedRun=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--freeze-rejections'],{encoding:'utf8',env:{...process.env,V4_OUTPUT_DIR:bannedTmp,V4_REJECTED_BASES_PATH:bannedLedger,V4_CANONICAL_INPUT_SHA256:crypto.createHash('sha256').update(fs.readFileSync(path.join(bannedTmp,'REJECTED-BASES-INPUT.json'))).digest('hex')}});assert.equal(bannedRun.status,0,bannedRun.stderr);assert.equal(read(bannedTmp,'REPLACEMENT-LEDGER.json').items.length,1);assert.equal(read(bannedTmp,'AVAILABILITY.json').reserve_narrative_rows,77);fs.rmSync(bannedTmp,{recursive:true,force:true});
const monotonicTmp=fs.mkdtempSync(path.join(os.tmpdir(),'v4-monotonic-'));const prior={schema_version:'gemini-context-v4-rejected-bases-input-v1',items:[{neutral_id:frame.items[0].neutral_id,revision_id:frame.items[0].revision_id,reason:'NOT_CLEAN'}]};fs.writeFileSync(path.join(monotonicTmp,'REJECTED-BASES-INPUT.json'),`${JSON.stringify(prior,null,2)}\n`);const emptyLedger=path.join(monotonicTmp,'empty.json');fs.writeFileSync(emptyLedger,'{"items":[]}\n');const priorHash=crypto.createHash('sha256').update(fs.readFileSync(path.join(monotonicTmp,'REJECTED-BASES-INPUT.json'))).digest('hex');const shrink=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--freeze-rejections'],{encoding:'utf8',env:{...process.env,V4_OUTPUT_DIR:monotonicTmp,V4_REJECTED_BASES_PATH:emptyLedger,V4_CANONICAL_INPUT_SHA256:priorHash}});assert.notEqual(shrink.status,0);assert.match(shrink.stderr,/superset/u);const missingHash=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--freeze-rejections'],{encoding:'utf8',env:{...process.env,V4_OUTPUT_DIR:monotonicTmp,V4_REJECTED_BASES_PATH:emptyLedger}});assert.notEqual(missingHash.status,0);assert.match(missingHash.stderr,/precondition/u);fs.rmSync(monotonicTmp,{recursive:true,force:true});
const row=(revision_id,file,extra={})=>({revision_id,public_source_file:file,profile:'narrative',normalized_source:`s-${revision_id}`,selection_context:`c-${revision_id}`,...extra});
// A replacement may be rejected in a later transition; the old revision remains banned and the slot advances again.
const chainTmp=fs.mkdtempSync(path.join(os.tmpdir(),'v4-chain-'));const chainLedger=path.join(chainTmp,'reject.json');const chainBase={schema_version:'gemini-context-v4-rejected-bases-input-v1',items:[]};fs.writeFileSync(path.join(chainTmp,'REJECTED-BASES-INPUT.json'),`${JSON.stringify(chainBase,null,2)}\n`);const chainItem={neutral_id:frame.items[0].neutral_id,revision_id:frame.items[0].revision_id,reason:'NOT_CLEAN'};fs.writeFileSync(chainLedger,`${JSON.stringify({items:[chainItem]},null,2)}\n`);installSurfaceEvidence(chainTmp,[chainItem]);const chainEnv={...process.env,V4_OUTPUT_DIR:chainTmp,V4_REJECTED_BASES_PATH:chainLedger,V4_CANONICAL_INPUT_SHA256:crypto.createHash('sha256').update(fs.readFileSync(path.join(chainTmp,'REJECTED-BASES-INPUT.json'))).digest('hex')};let chainRun=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--freeze-rejections'],{encoding:'utf8',env:chainEnv});assert.equal(chainRun.status,0,chainRun.stderr);const first=read(chainTmp,'REPLACEMENT-LEDGER.json').items[0];const priorInput=read(chainTmp,'REJECTED-BASES-INPUT.json');const chainItem2={neutral_id:chainItem.neutral_id,revision_id:first.replacement_revision_id,reason:'NOT_CLEAN'};fs.writeFileSync(chainLedger,`${JSON.stringify({items:[chainItem,chainItem2]},null,2)}\n`);const q2=read(chainTmp,'SURFACE-AUDIT-QUEUE.json');const agg2={schema_version:'gemini-context-surface-audit-aggregate-v1',stage:'SURFACE',queue_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(chainTmp,'SURFACE-AUDIT-QUEUE.json'))).digest('hex'),accepted_count:0,accepted_ids:[],items:[chainItem,chainItem2].map(x=>({neutral_id:x.neutral_id,revision_id:x.revision_id,verdict:x.reason}))};fs.writeFileSync(path.join(chainTmp,'SURFACE-AUDIT-AGGREGATE.json'),`${JSON.stringify(agg2,null,2)}\n`);fs.writeFileSync(path.join(chainTmp,'AUDIT-RELEASE-STATE.json'),`${JSON.stringify({surface_released:true,surface_queue_sha256:agg2.queue_sha256,surface_aggregate_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(chainTmp,'SURFACE-AUDIT-AGGREGATE.json'))).digest('hex')},null,2)}\n`);chainEnv.V4_CANONICAL_INPUT_SHA256=crypto.createHash('sha256').update(fs.readFileSync(path.join(chainTmp,'REJECTED-BASES-INPUT.json'))).digest('hex');chainRun=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--freeze-rejections'],{encoding:'utf8',env:chainEnv});assert.equal(chainRun.status,0,chainRun.stderr);const chainResult=read(chainTmp,'REPLACEMENT-LEDGER.json');assert.equal(chainResult.items.length,2);assert.equal(chainResult.items[0].replacement_revision_id,first.replacement_revision_id);assert.notEqual(chainResult.items[1].replacement_revision_id,first.replacement_revision_id);assert.equal(read(chainTmp,'REJECTED-BASES-INPUT.json').items.length,2);const chainCheck=spawnSync(process.execPath,[path.join(here,'select-and-freeze.mjs'),'--check'],{encoding:'utf8',env:{...process.env,V4_OUTPUT_DIR:chainTmp}});assert.equal(chainCheck.status,0,chainCheck.stderr);fs.rmSync(chainTmp,{recursive:true,force:true});
const selected=[
  row('reject-1','slot-1',{neutral_id:'V4-C-N01',cohort:'confirmation'}),
  row('retain-d1','dreadfell',{neutral_id:'V4-D-N01',cohort:'discovery'}),
  row('retain-d2','dreadfell',{neutral_id:'V4-C-N03',cohort:'confirmation'}),
  row('reject-2','slot-2',{neutral_id:'V4-D-N02',cohort:'discovery'}),
  row('reject-3','slot-3',{neutral_id:'V4-C-N02',cohort:'confirmation'}),
  row('retain-d3','dreadfell',{neutral_id:'V4-D-N04',cohort:'discovery'}),
  row('reject-4','slot-4',{neutral_id:'V4-D-N03',cohort:'discovery'}),
  row('retain-future','future-file',{neutral_id:'V4-C-N04',cohort:'confirmation',revision_uid:'future-base',normalized_source:'future-source',selection_context:'future-context'})
];
const reserve=[
  row('dreadfell-reserve','dreadfell'),
  row('future-collision','future-file',{revision_uid:'future-base',normalized_source:'future-source'}),
  row('source-collision','source-file',{normalized_source:'s-retain-d1'}),
  row('context-collision','context-file',{selection_context:'c-retain-d1'}),
  row('replacement-1','replacement-1'),row('replacement-2','replacement-2'),
  row('replacement-3','replacement-3'),row('replacement-4','replacement-4')
];
const synthetic=replaceRejectedRows({selected,reserve,rejectedRevisionIds:new Set(['reject-1','reject-2','reject-3','reject-4'])});
assert.deepEqual(synthetic.selected.map(x=>x.neutral_id),selected.map(x=>x.neutral_id));
assert.equal(synthetic.ledger.length,4);
assert.equal(synthetic.ledger[0].replacement_revision_id,'replacement-1');
assert.equal(synthetic.ledger[0].skipped_incompatible_reserves[0].reason,'ACTIVE_FILE_CAP');
assert.equal(synthetic.ledger[0].skipped_incompatible_reserves[1].reason,'BASE_IDENTITY_COLLISION');
assert.equal(synthetic.ledger[0].skipped_incompatible_reserves[2].reason,'NORMALIZED_SOURCE_COLLISION');
assert.equal(synthetic.ledger[0].skipped_incompatible_reserves[3].reason,'NORMALIZED_CONTEXT_COLLISION');
assert.equal(synthetic.ledger[0].skipped_incompatible_reserves[0].revision_id,'dreadfell-reserve');
assertFrameCaps(synthetic.selected);
assert.equal(synthetic.ledger[0].skipped_incompatible_reserves[1].revision_id,'future-collision');

const freedFile=replaceRejectedRows({selected:[row('reject-same','same-file',{neutral_id:'V4-D-N05',cohort:'discovery'}),row('keep-same-1','same-file',{neutral_id:'V4-C-N05',cohort:'confirmation'}),row('keep-same-2','same-file',{neutral_id:'V4-D-N06',cohort:'discovery'})],reserve:[row('accepted-same','same-file')],rejectedRevisionIds:new Set(['reject-same'])});
assert.equal(freedFile.selected[0].revision_id,'accepted-same');assertFrameCaps(freedFile.selected);
assert.equal(remainingRejectionTolerance(78,28,1),49);
const aggregateProbe=fs.mkdtempSync(path.join(os.tmpdir(),'v4-aggregate-'));fs.writeFileSync(path.join(aggregateProbe,'records.json'),'{}');const aggregateRun=spawnSync(process.execPath,[path.join(here,'aggregate-audits.mjs'),'surface',path.join(aggregateProbe,'records.json'),path.join(aggregateProbe,'out.json')],{encoding:'utf8'});assert.notEqual(aggregateRun.status,0,'surface aggregate must remain blocked before release');fs.rmSync(aggregateProbe,{recursive:true,force:true});

assert.throws(()=>replaceRejectedRows({
  selected:[
    row('only','active',{neutral_id:'V4-D-N01',cohort:'discovery'}),
    row('retained-1','active',{neutral_id:'V4-C-N01',cohort:'confirmation'}),
    row('retained-2','active',{neutral_id:'V4-D-N02',cohort:'discovery'}),
    row('retained-3','active',{neutral_id:'V4-C-N02',cohort:'confirmation'})
  ],
  reserve:[row('blocked','active')],
  rejectedRevisionIds:new Set(['only'])
}),/exact shortfall: narrative\/discovery replacement reserve exhausted/);

console.log(JSON.stringify({status:'PASS',tests:[
  '1 narrative rejection succeeds below the initial reserve gate',
  '28 narrative rejections succeed below the initial reserve gate',
  '29 narrative rejections succeed below the initial reserve gate',
  'exact rejection set V4-C-N01,V4-D-N02,V4-C-N02,V4-D-N03',
  'dreadfell ACTIVE_FILE_CAP, base-identity, and normalized-source skips',
  'successful same-file replacement after capacity is freed',
  'surface aggregate blocked before release',
  'final original slot order and caps',
  'compatible reserve exhaustion fails closed',
  'two-transition monotonic slot lineage and deterministic replay'
]},null,2));
