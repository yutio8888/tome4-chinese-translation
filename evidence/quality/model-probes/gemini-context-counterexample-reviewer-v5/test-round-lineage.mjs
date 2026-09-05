#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {initialize, readInitialPackage, makeRound, applyRound, outputDocuments, jsonBytes, readRoundBundles, sha256} from './round-lineage.mjs';

const here = path.dirname(fileURLToPath(import.meta.url)), input = readInitialPackage(here);
const fresh = (frame = input.frame, reserves = input.reserves) => initialize(structuredClone(frame), structuredClone(reserves));
const reject = neutral_id => ({neutral_id, surface_verdict: 'NOT_CLEAN', surface_evidence: 'deterministic rejection fixture'});
const clean = neutral_id => ({neutral_id, surface_verdict: 'PASS_SURFACE', surface_evidence: 'surface fixture pass', context_verdict: 'CLEAN_NO_MATERIAL_DEFECT', context_evidence: 'direct-source fixture pass'});
const contextReject = neutral_id => ({neutral_id, surface_verdict: 'PASS_SURFACE', surface_evidence: 'surface fixture pass', context_verdict: 'NOT_CLEAN', context_evidence: 'direct-source rejection fixture'});
const cloneBundle = bundle => Object.fromEntries(Object.entries(bundle).map(([key, value]) => [key, value && Buffer.from(value)]));

// Zero rejection: a released clean round preserves the exact frame and reserve.
{
  const state = fresh(), before = jsonBytes(outputDocuments(state)['ACTIVE-FRAME.json']);
  applyRound(state, makeRound(state, [clean(state.active[0].neutral_id)]));
  assert.equal(state.round, 1); assert.equal(state.consumed.size, 0); assert.equal(state.banned.size, 0);
  assert.deepEqual(state.active.map(row => row.revision_id), input.frame.items.map(row => row.revision_id));
  assert.notDeepEqual(jsonBytes(outputDocuments(state)['ACTIVE-FRAME.json']), before, 'round counter must advance while rows remain identical');
}

// One rejection consumes exactly one reserve and appends one exact lineage edge.
let firstBundle;
{
  const state = fresh(), slot = state.active.find(row => row.profile === 'narrative'); firstBundle = makeRound(state, [reject(slot.neutral_id)]); applyRound(state, firstBundle);
  const edge = state.lineage.get(slot.neutral_id).edges[0], reserve = outputDocuments(state)['RESERVE-STATE.json'];
  assert.equal(edge.rejected_revision_id, slot.revision_id); assert.equal(edge.replacement_revision_id, state.active.find(row => row.neutral_id === slot.neutral_id).revision_id);
  const expectedReserveRank = input.reserves.find(row => row.revision_id === edge.replacement_revision_id).reserve_rank;
  assert.ok(Number.isInteger(edge.reserve_rank)); assert.equal(edge.reserve_rank, expectedReserveRank);
  const serializedEdge = JSON.parse(jsonBytes(outputDocuments(state)['LINEAGE.json'])).items.find(item => item.neutral_id === slot.neutral_id).edges[0];
  assert.ok(Object.hasOwn(serializedEdge, 'reserve_rank')); assert.ok(Number.isInteger(serializedEdge.reserve_rank)); assert.equal(serializedEdge.reserve_rank, expectedReserveRank);
  assert.equal(reserve.consumed_revision_ids.length, 1); assert.equal(reserve.banned_revision_ids.length, 1); assert.equal(reserve.unavailable_reserve_revision_ids.length, 1); assert.equal(reserve.remaining_narrative_reserve_rows, 77);
  assert.deepEqual(Object.keys(state.active.find(row => row.neutral_id === slot.neutral_id)), ['neutral_id', 'cohort', 'profile', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256']);
}

// Context rejection binds the lineage edge to context evidence; surface out-of-scope
// maps to its distinct non-defect-attribution reason class.
{
  const state = fresh(), slot = state.active.find(row => row.profile === 'narrative'), bundle = makeRound(state, [contextReject(slot.neutral_id)]); applyRound(state, bundle);
  const edge = state.lineage.get(slot.neutral_id).edges[0]; assert.equal(edge.stage, 'CONTEXT'); assert.equal(edge.verdict, 'NOT_CLEAN'); assert.equal(edge.reason_class, 'DIRECT_AUDIT_REJECTION'); assert.equal(edge.queue_sha256, sha256(bundle.context_queue)); assert.equal(edge.aggregate_sha256, sha256(bundle.context_aggregate));
}
{
  const state = fresh(), slot = state.active[0], bundle = makeRound(state, [{neutral_id: slot.neutral_id, surface_verdict: 'OUT_OF_SCOPE_NON_PROSE', surface_evidence: 'bounded scope fixture'}]); applyRound(state, bundle);
  const edge = state.lineage.get(slot.neutral_id).edges[0]; assert.equal(edge.stage, 'SURFACE'); assert.equal(edge.reason_class, 'OUT_OF_SCOPE_NON_PROSE'); assert.equal(edge.verdict, 'OUT_OF_SCOPE_NON_PROSE');
}

// The same neutral slot may be rejected again in a later round; the consumed-and-banned
// replacement is counted once in unavailable reserve accounting.
{
  const state = fresh(), slot = state.active.find(row => row.profile === 'narrative'); applyRound(state, makeRound(state, [reject(slot.neutral_id)]));
  const firstReplacement = state.active.find(row => row.neutral_id === slot.neutral_id).revision_id;
  applyRound(state, makeRound(state, [reject(slot.neutral_id)]));
  const chain = state.lineage.get(slot.neutral_id), reserve = outputDocuments(state)['RESERVE-STATE.json'];
  assert.equal(chain.revisions.length, 3); assert.equal(chain.edges.length, 2); assert.equal(chain.edges[1].rejected_revision_id, firstReplacement); assert.equal(chain.edges[0].replacement_revision_id, chain.edges[1].rejected_revision_id);
  const expectedReserveRanks = chain.edges.map(edge => input.reserves.find(row => row.revision_id === edge.replacement_revision_id).reserve_rank);
  chain.edges.forEach((edge, index) => { assert.ok(Number.isInteger(edge.reserve_rank)); assert.equal(edge.reserve_rank, expectedReserveRanks[index]); });
  const serializedEdges = JSON.parse(jsonBytes(outputDocuments(state)['LINEAGE.json'])).items.find(item => item.neutral_id === slot.neutral_id).edges;
  serializedEdges.forEach((edge, index) => { assert.ok(Object.hasOwn(edge, 'reserve_rank')); assert.ok(Number.isInteger(edge.reserve_rank)); assert.equal(edge.reserve_rank, expectedReserveRanks[index]); });
  assert.ok(reserve.consumed_revision_ids.includes(firstReplacement)); assert.ok(reserve.banned_revision_ids.includes(firstReplacement)); assert.equal(reserve.unavailable_reserve_revision_ids.length, 2); assert.equal(reserve.remaining_narrative_reserve_rows, 76);
}

// Simultaneous rejections remove all rejected rows before deterministic slot-order fill.
{
  const state = fresh(), slots = state.active.filter(row => row.profile === 'narrative').slice(0, 2); applyRound(state, makeRound(state, slots.map(row => reject(row.neutral_id))));
  assert.equal(state.consumed.size, 2); assert.equal(state.banned.size, 2); assert.equal(state.lineage.get(slots[0].neutral_id).edges[0].round_id, 'ROUND-0001'); assert.equal(state.lineage.get(slots[1].neutral_id).edges[0].round_id, 'ROUND-0001');
}

// A cap-incompatible leading reserve is skipped, recorded, and not consumed.
{
  const frame = structuredClone(input.frame), reserves = structuredClone(input.reserves);
  const counts = new Map(); for (const row of frame.items.filter(row => row.profile === 'narrative')) counts.set(row.public_source_file, (counts.get(row.public_source_file) ?? 0) + 1);
  const saturated = [...counts].find(([, count]) => count === 3)?.[0]; assert.ok(saturated);
  const slot = frame.items.find(row => row.profile === 'narrative' && row.public_source_file !== saturated); assert.ok(slot);
  const firstNarrative = reserves.find(row => row.profile === 'narrative'); firstNarrative.public_source_file = saturated;
  const state = fresh(frame, reserves); applyRound(state, makeRound(state, [reject(slot.neutral_id)]));
  const edge = state.lineage.get(slot.neutral_id).edges[0]; assert.equal(edge.skipped_incompatible_reserves[0].revision_id, firstNarrative.revision_id); assert.equal(edge.skipped_incompatible_reserves[0].reason, 'ACTIVE_FILE_TOTAL_CAP'); assert.ok(!state.consumed.has(firstNarrative.revision_id));
}

// Queue, aggregate, and release tampering all fail closed.
{
  const state = fresh(), slot = state.active[0], original = makeRound(state, [reject(slot.neutral_id)]);
  const queueTampered = cloneBundle(original), queue = JSON.parse(queueTampered.surface_queue); queue.items[0].revision_id = '0'.repeat(64); queueTampered.surface_queue = jsonBytes(queue);
  assert.throws(() => applyRound(fresh(), queueTampered), /SURFACE_QUEUE_RESOLUTION/);
  const aggregateTampered = cloneBundle(original), aggregate = JSON.parse(aggregateTampered.surface_aggregate); aggregate.items[0].evidence = 'tampered'; aggregateTampered.surface_aggregate = jsonBytes(aggregate);
  assert.throws(() => applyRound(fresh(), aggregateTampered), /SURFACE_AGGREGATE_DERIVATION/);
  const releaseTampered = cloneBundle(original), release = JSON.parse(releaseTampered.release); release.surface_queue_sha256 = '0'.repeat(64); releaseTampered.release = jsonBytes(release);
  assert.throws(() => applyRound(fresh(), releaseTampered), /ROUND_RELEASE_BINDING/);
}

// Context-stage completeness, pass-set/surface binding, canonical bytes, and the
// cross-round predecessor release chain all fail closed under bounded tampering.
{
  const state = fresh(), slot = state.active[0], valid = makeRound(state, [clean(slot.neutral_id)]);
  const missing = cloneBundle(valid); missing.context_queue = null; missing.context_records = null; missing.context_aggregate = null; assert.throws(() => applyRound(fresh(), missing), /CONTEXT_REQUIRED_FOR_SURFACE_PASS/);
  const rejected = makeRound(fresh(), [reject(slot.neutral_id)]), unexpected = cloneBundle(rejected); unexpected.context_queue = valid.context_queue; unexpected.context_records = valid.context_records; unexpected.context_aggregate = valid.context_aggregate; assert.throws(() => applyRound(fresh(), unexpected), /UNEXPECTED_CONTEXT_STAGE/);
  const surfaceBinding = cloneBundle(valid), contextQueue = JSON.parse(surfaceBinding.context_queue); contextQueue.surface_aggregate_sha256 = '0'.repeat(64); surfaceBinding.context_queue = jsonBytes(contextQueue); assert.throws(() => applyRound(fresh(), surfaceBinding), /CONTEXT_SURFACE_BINDING/);
  const two = fresh(), twoSlots = two.active.slice(0, 2), passSet = cloneBundle(makeRound(two, twoSlots.map(row => clean(row.neutral_id)))), passQueue = JSON.parse(passSet.context_queue); passQueue.items.reverse(); passSet.context_queue = jsonBytes(passQueue); assert.throws(() => applyRound(two, passSet), /CONTEXT_QUEUE_NOT_SURFACE_PASS_SET/);
  const noncanonical = cloneBundle(valid); noncanonical.context_queue = Buffer.concat([noncanonical.context_queue, Buffer.from(' ')]); assert.throws(() => applyRound(fresh(), noncanonical), /CONTEXT_QUEUE_NONCANONICAL_BYTES/);
}
{
  const state = fresh(), first = makeRound(state, [reject(state.active[0].neutral_id)]); applyRound(state, first);
  const second = cloneBundle(makeRound(state, [reject(state.active[1].neutral_id)])), release = JSON.parse(second.release); release.predecessor_release_sha256 = '0'.repeat(64); second.release = jsonBytes(release);
  assert.throws(() => applyRound(state, second), /ROUND_RELEASE_BINDING/);
}

// Exhausting every narrative reserve by repeatedly rejecting the same slot fails closed exactly.
{
  const state = fresh(), slot = state.active.find(row => row.profile === 'narrative');
  for (let index = 0; index < 78; index++) applyRound(state, makeRound(state, [reject(slot.neutral_id)]));
  assert.equal(outputDocuments(state)['RESERVE-STATE.json'].remaining_narrative_reserve_rows, 0);
  assert.throws(() => applyRound(state, makeRound(state, [reject(slot.neutral_id)])), /RESERVE_EXHAUSTED/);
}

// Replaying identical immutable round bytes yields byte-identical derived outputs.
{
  const a = fresh(), bundles = [];
  bundles.push(makeRound(a, [reject(a.active.find(row => row.profile === 'narrative').neutral_id)])); applyRound(a, bundles[0]);
  bundles.push(makeRound(a, [clean(a.active.find(row => row.profile === 'dialogue').neutral_id)])); applyRound(a, bundles[1]);
  const b = fresh(); for (const bundle of bundles) applyRound(b, cloneBundle(bundle));
  for (const name of Object.keys(outputDocuments(a))) assert.ok(jsonBytes(outputDocuments(a)[name]).equals(jsonBytes(outputDocuments(b)[name])), `${name} replay drift`);
}

// Root entries, directory symlinks, artifact symlinks, unexpected entries, and
// missing/non-contiguous on-disk round history are rejected before replay.
{
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-gap-')); fs.mkdirSync(path.join(tmp, 'ROUND-0002'));
  assert.throws(() => readRoundBundles(tmp), /ROUND_DIRECTORY_SEQUENCE/); fs.rmSync(tmp, {recursive: true, force: true});
}
{
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-file-')); fs.writeFileSync(path.join(tmp, 'ROUND-0001'), 'not a directory');
  assert.throws(() => readRoundBundles(tmp), /ROUND_ENTRY_TYPE/); fs.rmSync(tmp, {recursive: true, force: true});
}
{
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-dir-link-')), target = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-dir-target-')); fs.symlinkSync(target, path.join(tmp, 'ROUND-0001'));
  assert.throws(() => readRoundBundles(tmp), /ROUND_ENTRY_TYPE/); fs.rmSync(tmp, {recursive: true, force: true}); fs.rmSync(target, {recursive: true, force: true});
}
{
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-artifact-link-')), targetDir = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-artifact-target-')), round = path.join(tmp, 'ROUND-0001'), target = path.join(targetDir, 'target.json'); fs.mkdirSync(round); fs.writeFileSync(target, '{}\n'); fs.symlinkSync(target, path.join(round, 'SURFACE-QUEUE.json'));
  assert.throws(() => readRoundBundles(tmp), /ROUND_ARTIFACT_TYPE/); fs.rmSync(tmp, {recursive: true, force: true}); fs.rmSync(targetDir, {recursive: true, force: true});
}
{
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round-unexpected-')); fs.writeFileSync(path.join(tmp, 'README'), 'unexpected');
  assert.throws(() => readRoundBundles(tmp), /ROUND_DIRECTORY_SEQUENCE/); fs.rmSync(tmp, {recursive: true, force: true});
}

console.log(JSON.stringify({status: 'PASS', tests: ['zero rejection', 'one rejection', 'active row schema projection', 'context rejection edge/hash binding', 'OUT_OF_SCOPE reason mapping', 'same slot rejected in repeated rounds', 'simultaneous rejection', 'cap skip without consumption', 'queue/aggregate/release tampering', 'context required/unexpected/binding/pass-set/noncanonical bytes', 'forged predecessor release', 'reserve exhaustion', 'byte-identical replay', 'continuous round history', 'root ordinary file', 'directory symlink', 'artifact symlink', 'unexpected root entry']}, null, 2));
