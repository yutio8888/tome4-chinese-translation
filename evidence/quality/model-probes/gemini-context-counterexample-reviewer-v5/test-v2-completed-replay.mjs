#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {activeFrameSha256, applyRound, initialize, jsonBytes, makeRound, outputDocuments, readInitialPackage} from './round-lineage.mjs';
import {checkReplay} from './replay.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..', '..', '..');
const input = readInitialPackage(here);
const state = initialize(structuredClone(input.frame), structuredClone(input.reserves));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-v2-completed-replay-'));
const authorization = {
  authorization_id: 'V5-FIXTURE-SURFACE-AUDIT',
  authorization_record_sha256: 'a'.repeat(64),
  authorized_candidate_ref: 'b'.repeat(64),
  final_pass_reviewer_agent_ids: {
    normal: '11111111-1111-4111-8111-111111111111',
    senior: '22222222-2222-4222-8222-222222222222'
  }
};

function decisions(rejectedId) {
  return state.active.map(row => row.neutral_id === rejectedId
    ? {neutral_id: row.neutral_id, surface_verdict: 'NOT_CLEAN', surface_evidence: 'positive v2 replacement fixture'}
    : {neutral_id: row.neutral_id, surface_verdict: 'PASS_SURFACE', surface_evidence: 'positive v2 surface fixture', context_verdict: 'CLEAN_NO_MATERIAL_DEFECT', context_evidence: 'positive v2 context fixture'});
}

function persistRound(bundle, roundId) {
  const dir = path.join(tmp, 'rounds', roundId); fs.mkdirSync(dir, {recursive: true});
  for (const [key, filename] of Object.entries({surface_queue: 'SURFACE-QUEUE.json', surface_queue_view: 'SURFACE-QUEUE-VIEW.json', surface_records: 'SURFACE-RECORDS.json', surface_aggregate: 'SURFACE-AGGREGATE.json', context_queue: 'CONTEXT-QUEUE.json', context_records: 'CONTEXT-RECORDS.json', context_aggregate: 'CONTEXT-AGGREGATE.json', release: 'RELEASE.json'})) if (bundle[key]) fs.writeFileSync(path.join(dir, filename), bundle[key]);
}

try {
  for (const name of ['INHERITANCE.json', 'INITIAL-FRAME.json', 'INITIAL-RESERVE-DIALOGUE.json', 'INITIAL-RESERVE-NARRATIVE.json']) fs.copyFileSync(path.join(here, name), path.join(tmp, name));

  const initialActiveHash = activeFrameSha256(state), firstRejected = state.active.find(row => row.profile === 'narrative').neutral_id;
  const round1 = makeRound(state, decisions(firstRejected), {surfaceV2: authorization, repo});
  persistRound(round1, 'ROUND-0001'); applyRound(state, round1);
  assert.equal(state.round, 1); assert.notEqual(activeFrameSha256(state), initialActiveHash);

  const round1PostActiveHash = activeFrameSha256(state), replacementRevision = state.active.find(row => row.neutral_id === firstRejected).revision_id;
  const secondRejected = state.active.find(row => row.profile === 'dialogue').neutral_id;
  const round2 = makeRound(state, decisions(secondRejected), {surfaceV2: authorization, repo});
  const round2View = JSON.parse(round2.surface_queue_view);
  assert.equal(round2View.round_id, 'ROUND-0002');
  assert.equal(round2View.active_frame_sha256, round1PostActiveHash);
  assert.equal(round2View.items.find(item => item.neutral_id === firstRejected).revision_id, replacementRevision);
  persistRound(round2, 'ROUND-0002'); applyRound(state, round2);
  assert.equal(state.round, 2); assert.notEqual(activeFrameSha256(state), round1PostActiveHash);

  for (const [name, doc] of Object.entries(outputDocuments(state))) fs.writeFileSync(path.join(tmp, name), jsonBytes(doc));
  const result = checkReplay(tmp); assert.equal(result.status, 'PASS'); assert.equal(result.completed_rounds, 2); assert.equal(result.byte_identical_outputs, true);
  console.log(JSON.stringify({status: 'PASS', tests: ['completed v2 queue/view/records/aggregate/release', 'persisted derived state', 'replay --check with historical pre-round frames', 'ROUND-0002 v2 construction and replacement revision view']}, null, 2));
} finally {
  fs.rmSync(tmp, {recursive: true, force: true});
}
