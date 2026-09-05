#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateSurfaceQueueViewBytes, jsonBytes, sha256} from './surface-queue-view.mjs';
import {readRoundBundles, readInitialPackage, initialize, applyRound, activeFrameDocument} from './round-lineage.mjs';

const here = path.dirname(fileURLToPath(import.meta.url)), repo = path.resolve(here, '..', '..', '..', '..');
const initial = readInitialPackage(here), historicalState = initialize(structuredClone(initial.frame), structuredClone(initial.reserves));
const round = path.join(here, 'rounds', 'ROUND-0001'), queueBytes = fs.readFileSync(path.join(round, 'SURFACE-QUEUE.json')), viewBytes = fs.readFileSync(path.join(round, 'SURFACE-QUEUE-VIEW.json')), activeFrameBytes = jsonBytes(activeFrameDocument(historicalState)), base = JSON.parse(viewBytes);
const labels = [];
function rejected(label, mutate, pattern = /SURFACE_QUEUE_VIEW_BINDING/u) {
  const value = structuredClone(base); mutate(value);
  assert.throws(() => validateSurfaceQueueViewBytes({repo, queueBytes, activeFrameBytes, viewBytes: jsonBytes(value)}), pattern, label); labels.push(label);
}

assert.equal(sha256(queueBytes), '2ab071cbd21e39075573bc9e3475f7492bf3a2efa6f66ea79e590793a0e51268');
assert.equal(sha256(viewBytes), '421640fd2b31d998c1a5b3832d7cb1314770a633f652bdb1ab689ffa1e3cc631');
validateSurfaceQueueViewBytes({repo, queueBytes, activeFrameBytes, viewBytes}); labels.push('canonical positive');
assert.throws(() => validateSurfaceQueueViewBytes({repo, queueBytes, viewBytes}), /VIEW_HISTORICAL_INPUT_REQUIRED/u); labels.push('historical active frame required');
{
  const wrongHistorical = JSON.parse(activeFrameBytes); wrongHistorical.last_completed_round = 1;
  assert.throws(() => validateSurfaceQueueViewBytes({repo, queueBytes, activeFrameBytes: jsonBytes(wrongHistorical), viewBytes}), /VIEW_ACTIVE_FRAME_BYTES/u); labels.push('wrong historical active frame');
}
rejected('queue hash', value => { value.surface_queue_sha256 = '0'.repeat(64); });
rejected('authorization hash', value => { value.authorization_record_sha256 = '0'.repeat(64); });
rejected('active frame hash', value => { value.active_frame_sha256 = '0'.repeat(64); });
rejected('ID mismatch', value => { value.items[0].neutral_id = 'V4-D-D99'; });
rejected('order mismatch', value => { [value.items[0], value.items[1]] = [value.items[1], value.items[0]]; });
rejected('count mismatch', value => { value.items.pop(); });
rejected('source bytes', value => { value.items[0].source += ' '; });
rejected('source hash', value => { value.items[0].source_sha256 = '0'.repeat(64); });
rejected('normalized source hash', value => { value.items[0].normalized_source_sha256 = '0'.repeat(64); });
rejected('target bytes', value => { value.items[0].target += '。'; });
rejected('target hash', value => { value.items[0].target_sha256 = '0'.repeat(64); });
rejected('inventory provenance', value => { value.provenance.inventory.raw_sha256 = '0'.repeat(64); });
rejected('tracked provenance', value => { value.provenance.tracked_v4_evidence.target_bindings_sha256 = '0'.repeat(64); });
rejected('row identity', value => { value.items[0].row_identity_sha256 = '0'.repeat(64); });
rejected('revision binding', value => { value.items[0].revision_binding_sha256 = '0'.repeat(64); });
rejected('schema extra', value => { value.unexpected = true; });
assert.throws(() => validateSurfaceQueueViewBytes({repo, queueBytes, activeFrameBytes, viewBytes: Buffer.from(JSON.stringify(base))}), /NONCANONICAL/u); labels.push('noncanonical bytes');

function pendingFixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-view-fs-')), dir = path.join(root, 'ROUND-0001'); fs.mkdirSync(dir);
  fs.copyFileSync(path.join(round, 'SURFACE-QUEUE.json'), path.join(dir, 'SURFACE-QUEUE.json'));
  fs.copyFileSync(path.join(round, 'SURFACE-QUEUE-VIEW.json'), path.join(dir, 'SURFACE-QUEUE-VIEW.json'));
  return {root, dir};
}
{
  const tmp = pendingFixture(); fs.unlinkSync(path.join(tmp.dir, 'SURFACE-QUEUE-VIEW.json'));
  assert.throws(() => readRoundBundles(tmp.root, 'ROUND-0001'), /PENDING_ROUND_ARTIFACTS/u); fs.rmSync(tmp.root, {recursive: true, force: true}); labels.push('missing view');
}
{
  const tmp = pendingFixture(), outside = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-view-target-')), target = path.join(outside, 'view.json'); fs.renameSync(path.join(tmp.dir, 'SURFACE-QUEUE-VIEW.json'), target); fs.symlinkSync(target, path.join(tmp.dir, 'SURFACE-QUEUE-VIEW.json'));
  assert.throws(() => readRoundBundles(tmp.root, 'ROUND-0001'), /ROUND_ARTIFACT_TYPE/u); fs.rmSync(tmp.root, {recursive: true, force: true}); fs.rmSync(outside, {recursive: true, force: true}); labels.push('view symlink');
}
{
  const tmp = pendingFixture(); fs.writeFileSync(path.join(tmp.dir, 'SURFACE-RECORDS.json'), '{}\n');
  assert.throws(() => readRoundBundles(tmp.root, 'ROUND-0001'), /PENDING_ROUND_ARTIFACTS/u); fs.rmSync(tmp.root, {recursive: true, force: true}); labels.push('premature records');
}
{
  const input = readInitialPackage(here), state = initialize(input.frame, input.reserves), queue = JSON.parse(queueBytes);
  const records = jsonBytes({schema_version: 'gemini-context-v5-surface-records-v2', round_id: 'ROUND-0001', stage: 'SURFACE', surface_queue_sha256: sha256(queueBytes), surface_queue_view_sha256: '0'.repeat(64), items: queue.items.map(item => ({neutral_id: item.neutral_id, verdict: 'NOT_CLEAN', evidence: 'fixture evidence'}))});
  assert.throws(() => applyRound(state, {root: here, surface_queue: queueBytes, surface_queue_view: viewBytes, surface_records: records, surface_aggregate: jsonBytes({}), context_queue: null, context_records: null, context_aggregate: null, release: jsonBytes({})}), /SURFACE_RECORDS_SIDECAR_BINDING/u); labels.push('forged records-sidecar binding');
}

console.log(JSON.stringify({status: 'PASS', tests: labels}, null, 2));
