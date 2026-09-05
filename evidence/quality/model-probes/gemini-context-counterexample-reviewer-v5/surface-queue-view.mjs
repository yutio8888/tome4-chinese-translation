#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRepo = path.resolve(here, '..', '..', '..', '..');
export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
const normalize = value => String(value).normalize('NFKC').replace(/\\[nrt]|\s/gu, ' ').replace(/ +/gu, ' ').trim();
const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;
const canonicalSha256 = value => sha256(Buffer.from(JSON.stringify(canonical(value))));
const ROW_KEYS = ['neutral_id', 'cohort', 'profile', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256'];
const rowIdentity = row => sha256(jsonBytes(Object.fromEntries(ROW_KEYS.map(key => [key, row[key]]))));
const PROVENANCE = Object.freeze({
  inventory: {
    logical_path: '.artifacts/i18n/quality/runs/20260829T095427.408942Z-inventory/inventory.jsonl',
    raw_sha256: '1fb97b26457ebda2b6c03be40e3fe6121639fe58046004acee62aa3dc8f6af61',
    canonical_array_sha256: '6064eba32bc43d3bf7dff40bd83b8d2183e73a5298bf5b0dcc28fb39c6b1d18a',
    manifest_logical_path: '.artifacts/i18n/quality/runs/20260829T095427.408942Z-inventory/inventory-manifest.json',
    manifest_raw_sha256: '9840256d3f08ad6c1c9e8d13469df2b2c78ac6e26e69ad55d8cc582631ba0335',
    summary_logical_path: '.artifacts/i18n/quality/runs/20260829T095427.408942Z-inventory/inventory-summary.json',
    summary_raw_sha256: 'f3f8091f157356c1582efd9202b652bf1dafaf41cd6d3653f1298f3cf277166f'
  },
  tracked_v4_evidence: {
    source_frame_logical_path: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4/SOURCE-FRAME.json',
    source_frame_sha256: 'bac449634a3174de08cd82080bc9e93b39a153250158c6a61e06f518a32af490',
    local_bindings_logical_path: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4/LOCAL-BINDINGS.json',
    local_bindings_sha256: '203e00bc78e582e9a2da58b0422b89d44b2d3beda1c91712f207f3d2e37b2e92',
    target_bindings_logical_path: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4/TARGET-BINDINGS.json',
    target_bindings_sha256: 'db97c66518dfd201ef3c0e5c302b48e35afa250f622b32e49f589f98af646643'
  },
  identity_contract: 'tome4-translation-revision-v1',
  revision_uid_formula: 'sha256("rev" + NUL + tu_uid + NUL + sha256(UTF8(source)))',
  revision_id_formula: 'sha256(canonical-json({identity_contract,version,tu_uid,revision_uid,target,args_order,special}))',
  normalization_contract: 'NFKC; replace literal \\n/\\r/\\t or Unicode whitespace with ASCII space; collapse spaces; trim'
});
const ROUND_0002_PROVENANCE = Object.freeze({
  fixed_source_commit: '624a67329fe2ad440c5b344785a9c73fcf22ae63',
  inventory: PROVENANCE.inventory,
  identity_contract: PROVENANCE.identity_contract,
  revision_uid_formula: PROVENANCE.revision_uid_formula,
  revision_id_formula: PROVENANCE.revision_id_formula,
  normalization_contract: PROVENANCE.normalization_contract
});

function readPinned(repo, logicalPath, expectedHash) {
  const file = path.join(repo, logicalPath), bytes = fs.readFileSync(file);
  if (sha256(bytes) !== expectedHash) throw Error(`VIEW_PROVENANCE_HASH:${logicalPath}`);
  return {file, bytes};
}

function loadTrustedRows(repo) {
  const inventory = readPinned(repo, PROVENANCE.inventory.logical_path, PROVENANCE.inventory.raw_sha256);
  const manifest = readPinned(repo, PROVENANCE.inventory.manifest_logical_path, PROVENANCE.inventory.manifest_raw_sha256);
  readPinned(repo, PROVENANCE.inventory.summary_logical_path, PROVENANCE.inventory.summary_raw_sha256);
  const manifestDoc = JSON.parse(manifest.bytes);
  if (manifestDoc.inventory_sha256 !== PROVENANCE.inventory.canonical_array_sha256 || manifestDoc.summary?.entries !== 30308) throw Error('VIEW_INVENTORY_MANIFEST_BINDING');
  const rows = inventory.bytes.toString('utf8').trimEnd().split('\n').map((line, index) => { try { return JSON.parse(line); } catch { throw Error(`VIEW_INVENTORY_JSONL:${index}`); } });
  if (rows.length !== 30308) throw Error('VIEW_INVENTORY_COUNT');
  const byRevision = new Map();
  for (const row of rows) { if (!byRevision.has(row.revision_id)) byRevision.set(row.revision_id, []); byRevision.get(row.revision_id).push(row); }
  const tracked = {};
  for (const [name, logical, hash] of [
    ['source', PROVENANCE.tracked_v4_evidence.source_frame_logical_path, PROVENANCE.tracked_v4_evidence.source_frame_sha256],
    ['local', PROVENANCE.tracked_v4_evidence.local_bindings_logical_path, PROVENANCE.tracked_v4_evidence.local_bindings_sha256],
    ['target', PROVENANCE.tracked_v4_evidence.target_bindings_logical_path, PROVENANCE.tracked_v4_evidence.target_bindings_sha256]
  ]) tracked[name] = JSON.parse(readPinned(repo, logical, hash).bytes);
  return {
    byRevision,
    tracked: Object.fromEntries(Object.entries(tracked).map(([name, doc]) => [name, {
      byNeutralId: new Map(doc.items.map(item => [item.neutral_id, item])),
      byRevisionId: new Map(doc.items.map(item => [item.revision_id, item]))
    }]))
  };
}

function revisionProof(row) {
  const sourceSha = sha256(Buffer.from(row.source, 'utf8'));
  const expectedRevisionUid = sha256(Buffer.from(`rev\0${row.tu_uid}\0${sourceSha}`, 'utf8'));
  if (row.revision_uid !== expectedRevisionUid) throw Error(`VIEW_REVISION_UID_BINDING:${row.revision_id}`);
  const payload = {identity_contract: PROVENANCE.identity_contract, version: row.version, tu_uid: row.tu_uid, revision_uid: row.revision_uid, target: row.target, args_order: row.args_order, special: row.special};
  const expectedRevisionId = canonicalSha256(payload);
  if (row.revision_id !== expectedRevisionId) throw Error(`VIEW_REVISION_TARGET_BINDING:${row.revision_id}`);
  return {sourceSha, expectedRevisionId};
}

export function buildSurfaceQueueView({repo = defaultRepo, queueBytes, activeFrameBytes} = {}) {
  if (!queueBytes || !activeFrameBytes) throw Error('VIEW_HISTORICAL_INPUT_REQUIRED');
  const rawQueue = Buffer.isBuffer(queueBytes) ? queueBytes : Buffer.from(queueBytes), queue = JSON.parse(rawQueue);
  if (!rawQueue.equals(jsonBytes(queue))) throw Error('VIEW_QUEUE_BYTES');
  const activeBytes = Buffer.isBuffer(activeFrameBytes) ? activeFrameBytes : Buffer.from(activeFrameBytes), active = JSON.parse(activeBytes);
  if (!activeBytes.equals(jsonBytes(active)) || sha256(activeBytes) !== queue.active_frame_sha256) throw Error('VIEW_ACTIVE_FRAME_BYTES');
  if (!Array.isArray(queue.items) || !Array.isArray(active.items) || queue.items.length < 1 || queue.items.length > active.items.length) throw Error('VIEW_QUEUE_COUNT');
  const trusted = loadTrustedRows(repo), activeById = new Map(active.items.map(row => [row.neutral_id, row]));
  let priorActiveIndex = -1;
  const items = queue.items.map((queued, index) => {
    const activeRow = activeById.get(queued.neutral_id), activeIndex = active.items.indexOf(activeRow);
    if (!activeRow || activeIndex <= priorActiveIndex || activeRow.revision_id !== queued.revision_id || rowIdentity(activeRow) !== queued.row_identity_sha256) throw Error(`VIEW_QUEUE_ACTIVE_ORDER:${index}`);
    priorActiveIndex = activeIndex;
    const candidates = trusted.byRevision.get(queued.revision_id);
    if (!candidates || candidates.length !== 1) throw Error(`VIEW_INVENTORY_REVISION_CARDINALITY:${queued.revision_id}`);
    const row = candidates[0], proof = revisionProof(row), source = trusted.tracked.source.byRevisionId.get(queued.revision_id), local = trusted.tracked.local.byRevisionId.get(queued.revision_id), target = source && local ? trusted.tracked.target.byNeutralId.get(queued.neutral_id) : null;
    if (Boolean(source) !== Boolean(local)) throw Error(`VIEW_TRACKED_PARTIAL_JOIN:${queued.neutral_id}`);
    const tracked = Boolean(source && local);
    if (tracked && (!target || source.neutral_id !== queued.neutral_id || local.neutral_id !== queued.neutral_id || target.neutral_id !== queued.neutral_id || source.revision_uid !== row.revision_uid || local.revision_uid !== row.revision_uid || source.source !== row.source || target.source !== row.source || target.target !== row.target)) throw Error(`VIEW_TRACKED_JOIN:${queued.neutral_id}`);
    const sourceSha = sha256(Buffer.from(row.source, 'utf8')), targetSha = sha256(Buffer.from(row.target, 'utf8')), normalizedSourceSha = sha256(Buffer.from(normalize(row.source), 'utf8'));
    if ((tracked && (source.source_sha256 !== sourceSha || local.source_sha256 !== sourceSha || target.source_sha256 !== sourceSha || target.target_sha256 !== targetSha || local.normalized_source_sha256 !== normalizedSourceSha)) || activeRow.normalized_source_sha256 !== normalizedSourceSha) throw Error(`VIEW_TEXT_HASH_BINDING:${queued.neutral_id}`);
    const common = {neutral_id: queued.neutral_id, revision_id: queued.revision_id, revision_uid: row.revision_uid, row_identity_sha256: queued.row_identity_sha256, source: row.source, source_sha256: sourceSha, normalized_source_sha256: normalizedSourceSha, target: row.target, target_sha256: targetSha, revision_binding_sha256: proof.expectedRevisionId};
    return queue.schema_version === 'gemini-context-v5-surface-queue-v3' ? {...common, revision_identity: {identity_contract: PROVENANCE.identity_contract, version: row.version, tu_uid: row.tu_uid, revision_uid: row.revision_uid, args_order: row.args_order, special: row.special}} : common;
  });
  if (queue.schema_version === 'gemini-context-v5-surface-queue-v3') return {schema_version: 'gemini-context-v5-surface-queue-view-v2', status: 'FROZEN_ROUND_0002_SURFACE_AUDITOR_INPUT_PENDING_REVIEW', round_id: queue.round_id, stage: 'SURFACE', surface_queue_sha256: sha256(rawQueue), authorization_record_path: queue.authorization_record_path, authorization_record_sha256: queue.authorization_record_sha256, active_frame_sha256: queue.active_frame_sha256, predecessor_release_sha256: queue.predecessor_release_sha256, provenance: ROUND_0002_PROVENANCE, items};
  return {schema_version: 'gemini-context-v5-surface-queue-view-v1', status: 'FROZEN_AUDITOR_VIEW_REPAIR_PENDING_REVIEW', round_id: queue.round_id, stage: 'SURFACE', surface_queue_sha256: sha256(rawQueue), authorization_record_sha256: queue.authorization_record_sha256, active_frame_sha256: queue.active_frame_sha256, predecessor_release_sha256: queue.predecessor_release_sha256, provenance: PROVENANCE, items};
}

export function validateSurfaceQueueViewBytes({repo = defaultRepo, queueBytes, activeFrameBytes, viewBytes}) {
  const bytes = Buffer.isBuffer(viewBytes) ? viewBytes : Buffer.from(viewBytes), parsed = JSON.parse(bytes);
  if (!bytes.equals(jsonBytes(parsed))) throw Error('SURFACE_QUEUE_VIEW_NONCANONICAL_BYTES');
  const expected = buildSurfaceQueueView({repo, queueBytes, activeFrameBytes});
  if (!exactKeys(parsed, Object.keys(expected)) || !bytes.equals(jsonBytes(expected))) throw Error('SURFACE_QUEUE_VIEW_BINDING');
  return {bytes, parsed};
}

const arg = process.argv[2];
const selectedRound = process.argv[3] ?? 'ROUND-0001';
const currentQueue = () => fs.readFileSync(path.join(here, 'rounds', selectedRound, 'SURFACE-QUEUE.json'));
const currentActiveFrame = () => {
  if (selectedRound !== 'ROUND-0001') return fs.readFileSync(path.join(here, 'ACTIVE-FRAME.json'));
  const initialBytes = fs.readFileSync(path.join(here, 'INITIAL-FRAME.json')), initial = JSON.parse(initialBytes);
  return jsonBytes({schema_version: 'gemini-context-v5-active-frame-v1', initial_frame_sha256: sha256(jsonBytes(initial)), last_completed_round: 0, items: initial.items});
};
if (import.meta.url === `file://${process.argv[1]}` && arg === '--print') process.stdout.write(jsonBytes(buildSurfaceQueueView({queueBytes: currentQueue(), activeFrameBytes: currentActiveFrame()})));
else if (import.meta.url === `file://${process.argv[1]}` && arg === '--check') {
  const target = path.join(here, 'rounds', selectedRound, 'SURFACE-QUEUE-VIEW.json'), bytes = fs.readFileSync(target);
  validateSurfaceQueueViewBytes({queueBytes: currentQueue(), activeFrameBytes: currentActiveFrame(), viewBytes: bytes});
  console.log(JSON.stringify({status: 'PASS', rows: JSON.parse(bytes).items.length, canonical: true, source_target_revision_bound: true, sha256: sha256(bytes)}, null, 2));
} else if (import.meta.url === `file://${process.argv[1]}`) throw Error('usage: node surface-queue-view.mjs --check|--print [ROUND-NNNN]');
