#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {materializeHistoricalRound1Fixture} from './historical-round1-test-fixture.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRepo = path.resolve(here, '..', '..', '..', '..');
const defaultSourceRepo = path.join(os.homedir(), 'projects', 't-engine4');
export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
const normalize = value => String(value).normalize('NFKC').replace(/\\[nrt]|\s/gu, ' ').replace(/ +/gu, ' ').trim();
const hex64 = value => typeof value === 'string' && /^[0-9a-f]{64}$/u.test(value);
const OCCURRENCE_KEYS = ['public_source_file', 'line', 'construct', 'inventory_logical_path', 'inventory_line', 'inventory_ordinal'];
const ALLOWED_CONSTRUCTS = new Set(['_t_LONG_STRING', '_t_SHORT_STRING']);
const CONTEXT_RADIUS_LINES = 3;
const ROW_KEYS = ['neutral_id', 'cohort', 'profile', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256'];
const rowIdentity = row => sha256(jsonBytes(Object.fromEntries(ROW_KEYS.map(key => [key, row[key]]))));
export const CONTEXT_SOURCE_ANCHORS_SHA256='901853d45f7994c3be1125d8557195c00749feba8735592da0d2e0533ec3f3e4';
export const CONTEXT_SOURCE_ANCHORS_AUTHORIZATION_SHA256='ba16ec282b4daedb05226e4f271cfc23223741902f319694629ae0dbd116bb1c';

export const CONTEXT_PROVENANCE = Object.freeze({
  fixed_source_commit: '624a67329fe2ad440c5b344785a9c73fcf22ae63',
  inventory_raw_sha256: '1fb97b26457ebda2b6c03be40e3fe6121639fe58046004acee62aa3dc8f6af61',
  inventory_canonical_array_sha256: '6064eba32bc43d3bf7dff40bd83b8d2183e73a5298bf5b0dcc28fb39c6b1d18a',
  inventory_manifest_sha256: '9840256d3f08ad6c1c9e8d13469df2b2c78ac6e26e69ad55d8cc582631ba0335',
  inventory_summary_sha256: 'f3f8091f157356c1582efd9202b652bf1dafaf41cd6d3653f1298f3cf277166f',
  inventory_rows: 30308,
  source_packets_sha256: '63c7c4236757c77b4723cbefd476461e75bec0811ddf894f3319a0f4ed1adea4',
  local_bindings_sha256: '203e00bc78e582e9a2da58b0422b89d44b2d3beda1c91712f207f3d2e37b2e92',
  target_bindings_sha256: 'db97c66518dfd201ef3c0e5c302b48e35afa250f622b32e49f589f98af646643',
  normalization_contract: 'NFKC; replace literal \\n/\\r/\\t or Unicode whitespace with ASCII space; collapse spaces; trim',
  context_extraction_contract: 'construct-aware exact-line extraction: occurrence.line and auditor occurrence.inventory_line equal the tight source-construct start; occurrence.construct is derived from the _t delimiter that contains the normalized queued source; the minimal inclusive source span contains it exactly once; exact file line count and three-line before/after blocks derive all bounds, truncation booleans, and sentinels',
  context_radius_lines: CONTEXT_RADIUS_LINES,
  selection_context_hash_note: 'selection context hashes bind the inherited one-line selection packet, not runtime_context; equality of raw and normalized hashes means that inherited packet was already normalization-stable and does not prove completeness'
});

const PATHS = Object.freeze({
  inventory: '.artifacts/i18n/quality/runs/20260829T095427.408942Z-inventory/inventory.jsonl',
  manifest: '.artifacts/i18n/quality/runs/20260829T095427.408942Z-inventory/inventory-manifest.json',
  summary: '.artifacts/i18n/quality/runs/20260829T095427.408942Z-inventory/inventory-summary.json',
  sourcePackets: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4/SOURCE-PACKETS.json',
  localBindings: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4/LOCAL-BINDINGS.json',
  targetBindings: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4/TARGET-BINDINGS.json',
  authorization: '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-AUDIT-AUTHORIZATION-001.json'
});
const EXPECTED = Object.freeze({
  authorization: '2e1bb1aa813365b2cd5f4adc5bfe3f263e8ca28f5cf455c7a8ac09ed8aaa9164',
  sourceAnchors: CONTEXT_SOURCE_ANCHORS_SHA256,
  sourceAnchorsAuthorization: CONTEXT_SOURCE_ANCHORS_AUTHORIZATION_SHA256,
  activeFrame: 'dd7b79438691530fe573e1b5deec0aba64e6fd7c24cf26ce6cf45f7e3a6fa440',
  surfaceQueue: '2ab071cbd21e39075573bc9e3475f7492bf3a2efa6f66ea79e590793a0e51268',
  surfaceView: '421640fd2b31d998c1a5b3832d7cb1314770a633f652bdb1ab689ffa1e3cc631',
  surfaceRecords: '53596f081abdbf12836d133b27d4b5f0eec8ff8a2d779d1b6daacc24257528ae',
  surfaceAggregate: 'e9c1026d5dffd1f2e88f911e5c897f7361131a4cd82c5e18f688b82aa0d06967'
});

function readPinned(repo, logicalPath, expectedHash) {
  const bytes = fs.readFileSync(path.join(repo, logicalPath));
  if (sha256(bytes) !== expectedHash) throw Error(`CONTEXT_PROVENANCE_HASH:${logicalPath}`);
  return bytes;
}
function canonicalDocument(bytes, label) {
  let parsed; try { parsed = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  if (!Buffer.from(bytes).equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return parsed;
}
function sourceBlob(sourceRepo, file, cache) {
  if (!cache.has(file)) cache.set(file, Buffer.from(execFileSync('git', ['-C', sourceRepo, 'show', `${CONTEXT_PROVENANCE.fixed_source_commit}:${file}`], {maxBuffer: 20 * 1024 * 1024})));
  return cache.get(file);
}

function sourceLines(blobText) {
  const lines = blobText.split('\n');
  if (lines.length > 1 && lines.at(-1) === '') lines.pop();
  return lines;
}

function deriveConstruct(text, source) {
  const normalizedSource = normalize(source), kinds = new Set();
  const longPattern = /_t\[(=*)\[/gu;
  const shortPattern = /_t\s*(["'])((?:\\.|(?!\1)[^\\])*)\1/gu;
  for (const match of text.matchAll(longPattern)) if (normalize(text.slice(match.index + match[0].length)).includes(normalizedSource)) kinds.add('_t_LONG_STRING');
  for (const match of text.matchAll(shortPattern)) if (normalize(match[2]).includes(normalizedSource)) kinds.add('_t_SHORT_STRING');
  if (kinds.size !== 1) throw Error('CONTEXT_CONSTRUCT_DELIMITER');
  return [...kinds][0];
}

function constructAwareContext(blobText, source, occurrence) {
  const lines = sourceLines(blobText), line = occurrence.line, normalizedSource = normalize(source);
  if (!Number.isInteger(line) || line < 1 || line > lines.length || !normalizedSource) throw Error('CONTEXT_SOURCE_LINE_COORDINATE');
  const suffix = normalize(lines.slice(line - 1).join('\n')), nextSuffix = normalize(lines.slice(line).join('\n'));
  if (!suffix.includes(normalizedSource) || nextSuffix.includes(normalizedSource)) throw Error('CONTEXT_OCCURRENCE_LINE_NOT_TIGHT');
  let sourceEnd = line;
  while (sourceEnd <= lines.length && !normalize(lines.slice(line - 1, sourceEnd).join('\n')).includes(normalizedSource)) sourceEnd += 1;
  if (sourceEnd > lines.length) throw Error('CONTEXT_SOURCE_SPAN_NOT_FOUND');
  const sourceText = lines.slice(line - 1, sourceEnd).join('\n'), normalizedSpan = normalize(sourceText);
  if (normalizedSpan.split(normalizedSource).length - 1 !== 1) throw Error('CONTEXT_SOURCE_SPAN_CARDINALITY');
  if (!ALLOWED_CONSTRUCTS.has(occurrence.construct) || deriveConstruct(sourceText, source) !== occurrence.construct) throw Error('CONTEXT_CONSTRUCT_BINDING');
  const beforeStart = Math.max(1, line - CONTEXT_RADIUS_LINES), afterEnd = Math.min(lines.length, sourceEnd + CONTEXT_RADIUS_LINES);
  const beforeText = lines.slice(beforeStart - 1, line - 1).join('\n'), afterText = lines.slice(sourceEnd, afterEnd).join('\n');
  if (!normalize(afterText)) throw Error('CONTEXT_TRAILING_NEIGHBORHOOD_EMPTY');
  return {
    radius_lines: CONTEXT_RADIUS_LINES,
    file_total_lines: lines.length,
    before: {line_start: beforeStart, line_end: line - 1, text: beforeText, text_sha256: sha256(Buffer.from(beforeText, 'utf8')), truncated: beforeStart > 1, sentinel: beforeStart > 1 ? '[[CONTEXT_BEFORE_TRUNCATED]]' : '[[CONTEXT_FILE_START]]'},
    source_construct: {line_start: line, line_end: sourceEnd, text: sourceText, text_sha256: sha256(Buffer.from(sourceText, 'utf8')), marked_text: `[[SOURCE_CONSTRUCT_BEGIN]]${sourceText}[[SOURCE_CONSTRUCT_END]]`, complete_source_present: true, source_truncated: false, normalized_source_occurrences: 1},
    after: {line_start: sourceEnd + 1, line_end: afterEnd, text: afterText, text_sha256: sha256(Buffer.from(afterText, 'utf8')), truncated: afterEnd < lines.length, sentinel: afterEnd < lines.length ? '[[CONTEXT_AFTER_TRUNCATED]]' : '[[CONTEXT_FILE_END]]'}
  };
}

function loadBuildInputs(repo) {
  const inventoryBytes = readPinned(repo, PATHS.inventory, CONTEXT_PROVENANCE.inventory_raw_sha256);
  const manifest = JSON.parse(readPinned(repo, PATHS.manifest, CONTEXT_PROVENANCE.inventory_manifest_sha256));
  readPinned(repo, PATHS.summary, CONTEXT_PROVENANCE.inventory_summary_sha256);
  if (manifest.inventory_sha256 !== CONTEXT_PROVENANCE.inventory_canonical_array_sha256 || manifest.summary?.entries !== CONTEXT_PROVENANCE.inventory_rows) throw Error('CONTEXT_INVENTORY_MANIFEST_BINDING');
  const inventoryLines = inventoryBytes.toString('utf8').trimEnd().split('\n');
  if (inventoryLines.length !== CONTEXT_PROVENANCE.inventory_rows) throw Error('CONTEXT_INVENTORY_COUNT');
  const inventory = inventoryLines.map((line, index) => { try { return JSON.parse(line); } catch { throw Error(`CONTEXT_INVENTORY_JSONL:${index + 1}`); } });
  const byRevision = new Map(); for (const row of inventory) { if (!byRevision.has(row.revision_id)) byRevision.set(row.revision_id, []); byRevision.get(row.revision_id).push(row); }
  const sourcePackets = JSON.parse(readPinned(repo, PATHS.sourcePackets, CONTEXT_PROVENANCE.source_packets_sha256));
  const localBindings = JSON.parse(readPinned(repo, PATHS.localBindings, CONTEXT_PROVENANCE.local_bindings_sha256));
  const targetBindings = JSON.parse(readPinned(repo, PATHS.targetBindings, CONTEXT_PROVENANCE.target_bindings_sha256));
  return {inventoryLines, byRevision, sourcePackets: new Map(sourcePackets.items.map(x => [x.neutral_id, x])), localBindings: new Map(localBindings.items.map(x => [x.neutral_id, x])), targetBindings: new Map(targetBindings.items.map(x => [x.neutral_id, x]))};
}

export function buildContextInput({repo = defaultRepo, sourceRepo = defaultSourceRepo} = {}) {
  if (execFileSync('git', ['-C', sourceRepo, 'rev-parse', `${CONTEXT_PROVENANCE.fixed_source_commit}^{commit}`], {encoding: 'utf8'}).trim() !== CONTEXT_PROVENANCE.fixed_source_commit) throw Error('CONTEXT_FIXED_SOURCE_COMMIT_UNAVAILABLE');
  const round = path.join(repo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0001');
  const root = path.dirname(path.dirname(round));
  const readRound = (name, hash) => { const bytes = fs.readFileSync(path.join(round, name)); if (sha256(bytes) !== hash) throw Error(`CONTEXT_SURFACE_HASH:${name}`); return {bytes, parsed: canonicalDocument(bytes, name.replace(/\.json$/u, ''))}; };
  const surfaceQueue = readRound('SURFACE-QUEUE.json', EXPECTED.surfaceQueue), surfaceView = readRound('SURFACE-QUEUE-VIEW.json', EXPECTED.surfaceView), surfaceRecords = readRound('SURFACE-RECORDS.json', EXPECTED.surfaceRecords), surfaceAggregate = readRound('SURFACE-AGGREGATE.json', EXPECTED.surfaceAggregate);
  const activeBytes = fs.readFileSync(path.join(root, 'ACTIVE-FRAME.json')); if (sha256(activeBytes) !== EXPECTED.activeFrame) throw Error('CONTEXT_ACTIVE_FRAME_HASH'); const active = canonicalDocument(activeBytes, 'ACTIVE_FRAME');
  const authorizationBytes = readPinned(repo, PATHS.authorization, EXPECTED.authorization), authorization = canonicalDocument(authorizationBytes, 'CONTEXT_AUTHORIZATION');
  if (authorization.authorization_id !== 'V5-ROUND-0001-CONTEXT-AUDIT-001' || authorization.status !== 'AUTHORIZED_QUEUE_VIEW_FREEZE_PENDING_INDEPENDENT_REVIEW' || authorization.scope?.context_queue_and_view_item_count !== 55 || authorization.scope?.auditor_call_started !== false || authorization.scope?.replacements_authorized !== false || authorization.scope?.release_authorized !== false || authorization.scope?.later_rounds_authorized !== false || authorization.scope?.formal_gemini_inference_authorized !== false || authorization.predecessor_release_sha256 !== null) throw Error('CONTEXT_AUTHORIZATION_SCOPE');
  if (surfaceAggregate.parsed.surface_queue_sha256 !== EXPECTED.surfaceQueue || surfaceAggregate.parsed.surface_queue_view_sha256 !== EXPECTED.surfaceView || surfaceAggregate.parsed.surface_records_sha256 !== EXPECTED.surfaceRecords || surfaceAggregate.parsed.counts?.PASS_SURFACE !== 55 || surfaceAggregate.parsed.pass_ids?.length !== 55) throw Error('CONTEXT_SURFACE_AGGREGATE_BINDING');
  if (surfaceQueue.parsed.active_frame_sha256 !== EXPECTED.activeFrame || surfaceQueue.parsed.predecessor_release_sha256 !== null || active.items?.length !== 64) throw Error('CONTEXT_PRE_ROUND_FRAME_BINDING');
  const surfaceById = new Map(surfaceQueue.parsed.items.map(x => [x.neutral_id, x])), activeById = new Map(active.items.map(x => [x.neutral_id, x]));
  const queueItems = surfaceAggregate.parsed.pass_ids.map((neutralId, index) => {
    const surfaceItem = surfaceById.get(neutralId), activeRow = activeById.get(neutralId);
    if (!surfaceItem || !activeRow || surfaceItem.revision_id !== activeRow.revision_id || surfaceItem.row_identity_sha256 !== rowIdentity(activeRow)) throw Error(`CONTEXT_PASS_RESOLUTION:${index}:${neutralId}`);
    return {neutral_id: neutralId, revision_id: surfaceItem.revision_id, row_identity_sha256: surfaceItem.row_identity_sha256};
  });
  const queue = {
    schema_version: 'gemini-context-v5-context-queue-v2', round_id: 'ROUND-0001', stage: 'CONTEXT',
    active_frame_sha256: EXPECTED.activeFrame, predecessor_release_sha256: null, fixed_source_commit: CONTEXT_PROVENANCE.fixed_source_commit,
    surface_queue_sha256: EXPECTED.surfaceQueue, surface_queue_view_sha256: EXPECTED.surfaceView, surface_records_sha256: EXPECTED.surfaceRecords, surface_aggregate_sha256: EXPECTED.surfaceAggregate,
    authorization_id: authorization.authorization_id, authorization_record_sha256: EXPECTED.authorization, items: queueItems
  };
  const queueBytes = jsonBytes(queue), trusted = loadBuildInputs(repo), blobs = new Map();
  const items = queueItems.map((queued, index) => {
    const candidates = trusted.byRevision.get(queued.revision_id); if (!candidates || candidates.length !== 1) throw Error(`CONTEXT_INVENTORY_REVISION_CARDINALITY:${queued.neutral_id}`);
    const inventoryRow = candidates[0], activeRow = activeById.get(queued.neutral_id), packet = trusted.sourcePackets.get(queued.neutral_id), local = trusted.localBindings.get(queued.neutral_id), target = trusted.targetBindings.get(queued.neutral_id);
    if (!packet || !local || !target) throw Error(`CONTEXT_TRACKED_JOIN_MISSING:${queued.neutral_id}`);
    const sourceSha = sha256(Buffer.from(inventoryRow.source, 'utf8')), targetSha = sha256(Buffer.from(inventoryRow.target, 'utf8')), normalizedSourceSha = sha256(Buffer.from(normalize(inventoryRow.source), 'utf8'));
    if (inventoryRow.revision_id !== queued.revision_id || inventoryRow.revision_uid !== activeRow.revision_uid || packet.occurrence.public_source_file !== activeRow.public_source_file || packet.source_sha256 !== sourceSha || local.source_sha256 !== sourceSha || target.source_sha256 !== sourceSha || target.source !== inventoryRow.source || target.target !== inventoryRow.target || target.target_sha256 !== targetSha || activeRow.normalized_source_sha256 !== normalizedSourceSha || local.normalized_source_sha256 !== normalizedSourceSha) throw Error(`CONTEXT_SOURCE_TARGET_BINDING:${queued.neutral_id}`);
    const inventoryOccurrence = inventoryRow.occurrences?.[0];
    if (!exactKeys(packet.occurrence, OCCURRENCE_KEYS) || !exactKeys(local.occurrence, OCCURRENCE_KEYS) || JSON.stringify(packet.occurrence) !== JSON.stringify(local.occurrence) || inventoryRow.occurrences?.length !== 1 || packet.occurrence.inventory_logical_path !== inventoryOccurrence.logical_path || packet.occurrence.inventory_line !== inventoryOccurrence.line || packet.occurrence.inventory_ordinal !== inventoryOccurrence.ordinal) throw Error(`CONTEXT_OCCURRENCE_INVENTORY:${queued.neutral_id}`);
    const blob = sourceBlob(sourceRepo, packet.occurrence.public_source_file, blobs), blobText = blob.toString('utf8'), markerCount = packet.source_context.split('[[SOURCE_MATCH_1]]').length - 1;
    if (sha256(blob) !== packet.source_artifact_sha256 || packet.source_artifact_sha256 !== local.source_artifact_sha256 || markerCount !== 1 || packet.source_match_count !== 1 || local.source_match_count !== 1) throw Error(`CONTEXT_SOURCE_PACKET_BINDING:${queued.neutral_id}`);
    const unmarked = packet.source_context.replace('[[SOURCE_MATCH_1]]', '');
    if (!normalize(blobText).includes(normalize(unmarked))) throw Error(`CONTEXT_SOURCE_EXCERPT_BYTES:${queued.neutral_id}`);
    const normalizedBlob = normalize(blobText), normalizedSource = normalize(inventoryRow.source);
    if (normalizedBlob.split(normalizedSource).length - 1 !== 1) throw Error(`CONTEXT_SOURCE_LINE_COORDINATE:${queued.neutral_id}`);
    const contextSha = sha256(Buffer.from(packet.source_context, 'utf8')), normalizedContextSha = sha256(Buffer.from(normalize(packet.source_context), 'utf8'));
    if (packet.context_sha256 !== contextSha || packet.normalized_context_sha256 !== normalizedContextSha || local.context_sha256 !== contextSha || local.selection_context_sha256 !== contextSha || activeRow.normalized_context_sha256 !== normalizedContextSha) throw Error(`CONTEXT_CONTEXT_HASH:${queued.neutral_id}`);
    const runtimeContext = constructAwareContext(blobText, inventoryRow.source, packet.occurrence);
    const occurrence = {...packet.occurrence, inventory_line: packet.occurrence.line};
    return {neutral_id: queued.neutral_id, revision_id: queued.revision_id, row_identity_sha256: queued.row_identity_sha256, source: inventoryRow.source, source_sha256: sourceSha, normalized_source_sha256: normalizedSourceSha, target: inventoryRow.target, target_sha256: targetSha, selection_context_sha256: contextSha, selection_normalized_context_sha256: normalizedContextSha, selection_context_normalization_degenerate: contextSha === normalizedContextSha, runtime_context: runtimeContext, public_source_file: packet.occurrence.public_source_file, source_artifact_sha256: packet.source_artifact_sha256, occurrence};
  });
  const anchorFiles = [], seenAnchorFiles = new Set();
  for (const item of items) if (!seenAnchorFiles.has(item.public_source_file)) {
    seenAnchorFiles.add(item.public_source_file);
    anchorFiles.push({public_source_file:item.public_source_file, source_artifact_sha256:item.source_artifact_sha256, file_total_lines:item.runtime_context.file_total_lines});
  }
  const anchors = {
    schema_version:'gemini-context-v5-context-source-anchors-v1', status:'FROZEN_IMMUTABLE_FIXED_COMMIT_SOURCE_ANCHORS', round_id:'ROUND-0001', stage:'CONTEXT',
    context_queue_sha256:sha256(queueBytes), fixed_source_commit:CONTEXT_PROVENANCE.fixed_source_commit, authorization_record_sha256:EXPECTED.authorization, item_count:items.length,
    files:anchorFiles,
    items:items.map(item=>({neutral_id:item.neutral_id,revision_id:item.revision_id,public_source_file:item.public_source_file,source_artifact_sha256:item.source_artifact_sha256,file_total_lines:item.runtime_context.file_total_lines,occurrence_line:item.occurrence.line,inventory_line:item.occurrence.inventory_line,construct:item.occurrence.construct,before_line_start:item.runtime_context.before.line_start,before_line_end:item.runtime_context.before.line_end,source_line_start:item.runtime_context.source_construct.line_start,source_line_end:item.runtime_context.source_construct.line_end,after_line_start:item.runtime_context.after.line_start,after_line_end:item.runtime_context.after.line_end}))
  };
  const anchorsBytes = jsonBytes(anchors), anchorsSha256 = sha256(anchorsBytes);
  const view = {
    schema_version: 'gemini-context-v5-context-queue-view-v3', status: 'FROZEN_CONTEXT_AUDITOR_INPUT_PENDING_INDEPENDENT_REVIEW', round_id: 'ROUND-0001', stage: 'CONTEXT', context_queue_sha256: sha256(queueBytes), context_source_anchors_sha256:anchorsSha256,
    surface_queue_sha256: EXPECTED.surfaceQueue, surface_queue_view_sha256: EXPECTED.surfaceView, surface_records_sha256: EXPECTED.surfaceRecords, surface_aggregate_sha256: EXPECTED.surfaceAggregate,
    authorization_record_sha256: EXPECTED.authorization, active_frame_sha256: EXPECTED.activeFrame, predecessor_release_sha256: null, fixed_source_commit: CONTEXT_PROVENANCE.fixed_source_commit, provenance: CONTEXT_PROVENANCE, items
  };
  return {queue, queueBytes, anchors, anchorsBytes, view, viewBytes: jsonBytes(view)};
}

export function validateFrozenContextInputBytes({surfaceQueueBytes, surfaceViewBytes, surfaceRecordsBytes, surfaceAggregateBytes, activeFrameBytes, queueBytes, anchorsBytes, viewBytes}) {
  const inputs = {surfaceQueueBytes, surfaceViewBytes, surfaceRecordsBytes, surfaceAggregateBytes, activeFrameBytes, queueBytes, anchorsBytes, viewBytes};
  for (const [name, value] of Object.entries(inputs)) if (!value) throw Error(`CONTEXT_FROZEN_INPUT_REQUIRED:${name}`);
  const actual = {surfaceQueue: sha256(surfaceQueueBytes), surfaceView: sha256(surfaceViewBytes), surfaceRecords: sha256(surfaceRecordsBytes), surfaceAggregate: sha256(surfaceAggregateBytes), activeFrame: sha256(activeFrameBytes)};
  for (const key of Object.keys(actual)) if (actual[key] !== EXPECTED[key]) throw Error(`CONTEXT_FROZEN_${key.toUpperCase()}_HASH`);
  if (sha256(anchorsBytes) !== EXPECTED.sourceAnchors) throw Error('CONTEXT_SOURCE_ANCHOR_HASH');
  const surfaceQueue = canonicalDocument(surfaceQueueBytes, 'CONTEXT_FROZEN_SURFACE_QUEUE'), aggregate = canonicalDocument(surfaceAggregateBytes, 'CONTEXT_FROZEN_SURFACE_AGGREGATE'), active = canonicalDocument(activeFrameBytes, 'CONTEXT_FROZEN_ACTIVE_FRAME'), queue = canonicalDocument(queueBytes, 'CONTEXT_QUEUE'), anchors = canonicalDocument(anchorsBytes, 'CONTEXT_SOURCE_ANCHORS'), view = canonicalDocument(viewBytes, 'CONTEXT_QUEUE_VIEW');
  const queueKeys = ['schema_version','round_id','stage','active_frame_sha256','predecessor_release_sha256','fixed_source_commit','surface_queue_sha256','surface_queue_view_sha256','surface_records_sha256','surface_aggregate_sha256','authorization_id','authorization_record_sha256','items'];
  if (!exactKeys(queue, queueKeys) || queue.schema_version !== 'gemini-context-v5-context-queue-v2' || queue.round_id !== 'ROUND-0001' || queue.stage !== 'CONTEXT' || queue.active_frame_sha256 !== EXPECTED.activeFrame || queue.predecessor_release_sha256 !== null || queue.fixed_source_commit !== CONTEXT_PROVENANCE.fixed_source_commit || queue.surface_queue_sha256 !== EXPECTED.surfaceQueue || queue.surface_queue_view_sha256 !== EXPECTED.surfaceView || queue.surface_records_sha256 !== EXPECTED.surfaceRecords || queue.surface_aggregate_sha256 !== EXPECTED.surfaceAggregate || queue.authorization_id !== 'V5-ROUND-0001-CONTEXT-AUDIT-001' || queue.authorization_record_sha256 !== EXPECTED.authorization || !Array.isArray(queue.items) || queue.items.length !== 55) throw Error('CONTEXT_QUEUE_SCHEMA_BINDING');
  const surfaceById = new Map(surfaceQueue.items.map(x => [x.neutral_id, x])), activeById = new Map(active.items.map(x => [x.neutral_id, x]));
  if (JSON.stringify(queue.items.map(x => x.neutral_id)) !== JSON.stringify(aggregate.pass_ids)) throw Error('CONTEXT_QUEUE_PASS_ORDER');
  queue.items.forEach((item, index) => { const s = surfaceById.get(item.neutral_id), a = activeById.get(item.neutral_id); if (!exactKeys(item, ['neutral_id','revision_id','row_identity_sha256']) || !s || !a || item.revision_id !== s.revision_id || item.row_identity_sha256 !== s.row_identity_sha256 || item.row_identity_sha256 !== rowIdentity(a)) throw Error(`CONTEXT_QUEUE_ITEM_RESOLUTION:${index}`); });
  const anchorKeys=['schema_version','status','round_id','stage','context_queue_sha256','fixed_source_commit','authorization_record_sha256','item_count','files','items'];
  const anchorFileKeys=['public_source_file','source_artifact_sha256','file_total_lines'], anchorItemKeys=['neutral_id','revision_id','public_source_file','source_artifact_sha256','file_total_lines','occurrence_line','inventory_line','construct','before_line_start','before_line_end','source_line_start','source_line_end','after_line_start','after_line_end'];
  if (!exactKeys(anchors,anchorKeys) || anchors.schema_version!=='gemini-context-v5-context-source-anchors-v1' || anchors.status!=='FROZEN_IMMUTABLE_FIXED_COMMIT_SOURCE_ANCHORS' || anchors.round_id!==queue.round_id || anchors.stage!=='CONTEXT' || anchors.context_queue_sha256!==sha256(queueBytes) || anchors.fixed_source_commit!==CONTEXT_PROVENANCE.fixed_source_commit || anchors.authorization_record_sha256!==EXPECTED.authorization || anchors.item_count!==55 || !Array.isArray(anchors.files) || !Array.isArray(anchors.items) || anchors.items.length!==55 || JSON.stringify(anchors.items.map(x=>x.neutral_id))!==JSON.stringify(queue.items.map(x=>x.neutral_id))) throw Error('CONTEXT_SOURCE_ANCHOR_SCHEMA');
  const anchorFileMap=new Map(); for(const file of anchors.files){if(!exactKeys(file,anchorFileKeys)||anchorFileMap.has(file.public_source_file)||typeof file.public_source_file!=='string'||!hex64(file.source_artifact_sha256)||!Number.isInteger(file.file_total_lines)||file.file_total_lines<1)throw Error('CONTEXT_SOURCE_ANCHOR_SCHEMA');anchorFileMap.set(file.public_source_file,file);}
  anchors.items.forEach((item,index)=>{const q=queue.items[index],file=anchorFileMap.get(item.public_source_file);if(!exactKeys(item,anchorItemKeys)||item.neutral_id!==q.neutral_id||item.revision_id!==q.revision_id||!file||item.source_artifact_sha256!==file.source_artifact_sha256||item.file_total_lines!==file.file_total_lines||!ALLOWED_CONSTRUCTS.has(item.construct)||!['occurrence_line','inventory_line','before_line_start','before_line_end','source_line_start','source_line_end','after_line_start','after_line_end'].every(k=>Number.isInteger(item[k])))throw Error(`CONTEXT_SOURCE_ANCHOR_SCHEMA:${index}`);});
  const viewKeys = ['schema_version','status','round_id','stage','context_queue_sha256','context_source_anchors_sha256','surface_queue_sha256','surface_queue_view_sha256','surface_records_sha256','surface_aggregate_sha256','authorization_record_sha256','active_frame_sha256','predecessor_release_sha256','fixed_source_commit','provenance','items'];
  if (!exactKeys(view, viewKeys) || view.schema_version !== 'gemini-context-v5-context-queue-view-v3' || view.status !== 'FROZEN_CONTEXT_AUDITOR_INPUT_PENDING_INDEPENDENT_REVIEW' || view.round_id !== queue.round_id || view.stage !== 'CONTEXT' || view.context_queue_sha256 !== sha256(queueBytes) || view.context_source_anchors_sha256 !== EXPECTED.sourceAnchors || view.surface_queue_sha256 !== EXPECTED.surfaceQueue || view.surface_queue_view_sha256 !== EXPECTED.surfaceView || view.surface_records_sha256 !== EXPECTED.surfaceRecords || view.surface_aggregate_sha256 !== EXPECTED.surfaceAggregate || view.authorization_record_sha256 !== EXPECTED.authorization || view.active_frame_sha256 !== EXPECTED.activeFrame || view.predecessor_release_sha256 !== null || view.fixed_source_commit !== CONTEXT_PROVENANCE.fixed_source_commit || JSON.stringify(view.provenance) !== JSON.stringify(CONTEXT_PROVENANCE) || !Array.isArray(view.items) || view.items.length !== 55) throw Error('CONTEXT_QUEUE_VIEW_SCHEMA_BINDING');
  const itemKeys = ['neutral_id','revision_id','row_identity_sha256','source','source_sha256','normalized_source_sha256','target','target_sha256','selection_context_sha256','selection_normalized_context_sha256','selection_context_normalization_degenerate','runtime_context','public_source_file','source_artifact_sha256','occurrence'];
  view.items.forEach((item, index) => {
    const q = queue.items[index], anchor = anchors.items[index];
    const runtime = item.runtime_context, before = runtime?.before, construct = runtime?.source_construct, after = runtime?.after, normalizedSource = normalize(item.source);
    if (!exactKeys(item, itemKeys) || item.neutral_id !== q.neutral_id || item.revision_id !== q.revision_id || item.row_identity_sha256 !== q.row_identity_sha256 || sha256(Buffer.from(item.source,'utf8')) !== item.source_sha256 || sha256(Buffer.from(normalize(item.source),'utf8')) !== item.normalized_source_sha256 || sha256(Buffer.from(item.target,'utf8')) !== item.target_sha256 || !hex64(item.selection_context_sha256) || !hex64(item.selection_normalized_context_sha256) || item.selection_context_normalization_degenerate !== (item.selection_context_sha256 === item.selection_normalized_context_sha256) || !hex64(item.source_artifact_sha256) || !exactKeys(item.occurrence, OCCURRENCE_KEYS) || item.public_source_file !== item.occurrence.public_source_file || !Number.isInteger(item.occurrence.line) || item.occurrence.line < 1 || item.occurrence.inventory_line !== item.occurrence.line || !Number.isInteger(item.occurrence.inventory_ordinal) || item.occurrence.inventory_ordinal < 1 || !ALLOWED_CONSTRUCTS.has(item.occurrence.construct)) throw Error(`CONTEXT_QUEUE_VIEW_ITEM:${index}`);
    if (!exactKeys(runtime, ['radius_lines','file_total_lines','before','source_construct','after']) || runtime.radius_lines !== CONTEXT_RADIUS_LINES || !Number.isInteger(runtime.file_total_lines) || runtime.file_total_lines < 1 || !exactKeys(before, ['line_start','line_end','text','text_sha256','truncated','sentinel']) || !exactKeys(construct, ['line_start','line_end','text','text_sha256','marked_text','complete_source_present','source_truncated','normalized_source_occurrences']) || !exactKeys(after, ['line_start','line_end','text','text_sha256','truncated','sentinel'])) throw Error(`CONTEXT_RUNTIME_SCHEMA:${index}`);
    const constructLines = construct.text.split('\n'), nextLineSuffix = normalize([...constructLines.slice(1), after.text].join('\n')), withoutLastSourceLine = normalize(constructLines.slice(0, -1).join('\n'));
    let derivedConstruct; try { derivedConstruct = deriveConstruct(construct.text, item.source); } catch { throw Error(`CONTEXT_RUNTIME_BINDING:${index}`); }
    const expectedBeforeStart = Math.max(1, construct.line_start - runtime.radius_lines), expectedAfterEnd = Math.min(runtime.file_total_lines, construct.line_end + runtime.radius_lines);
    const lineCountMatches = block => { const expected = block.line_end < block.line_start ? 0 : block.line_end - block.line_start + 1; return expected === 0 ? block.text === '' : block.text.split('\n').length === expected; };
    const expectedBeforeTruncated = expectedBeforeStart > 1, expectedAfterTruncated = expectedAfterEnd < runtime.file_total_lines;
    if (item.public_source_file!==anchor.public_source_file||item.source_artifact_sha256!==anchor.source_artifact_sha256||runtime.file_total_lines!==anchor.file_total_lines||item.occurrence.line!==anchor.occurrence_line||item.occurrence.inventory_line!==anchor.inventory_line||item.occurrence.construct!==anchor.construct||before.line_start!==anchor.before_line_start||before.line_end!==anchor.before_line_end||construct.line_start!==anchor.source_line_start||construct.line_end!==anchor.source_line_end||after.line_start!==anchor.after_line_start||after.line_end!==anchor.after_line_end) throw Error(`CONTEXT_SOURCE_ANCHOR_BINDING:${index}`);
    if (before.line_start !== expectedBeforeStart || before.line_end !== construct.line_start - 1 || construct.line_start !== item.occurrence.line || construct.line_start !== item.occurrence.inventory_line || construct.line_end < construct.line_start || construct.line_end >= runtime.file_total_lines || after.line_start !== construct.line_end + 1 || after.line_end !== expectedAfterEnd || !lineCountMatches(before) || !lineCountMatches(construct) || !lineCountMatches(after) || sha256(Buffer.from(before.text,'utf8')) !== before.text_sha256 || sha256(Buffer.from(construct.text,'utf8')) !== construct.text_sha256 || sha256(Buffer.from(after.text,'utf8')) !== after.text_sha256 || construct.marked_text !== `[[SOURCE_CONSTRUCT_BEGIN]]${construct.text}[[SOURCE_CONSTRUCT_END]]` || construct.complete_source_present !== true || construct.source_truncated !== false || construct.normalized_source_occurrences !== 1 || derivedConstruct !== item.occurrence.construct || normalize(construct.text).split(normalizedSource).length - 1 !== 1 || nextLineSuffix.includes(normalizedSource) || (constructLines.length > 1 && withoutLastSourceLine.includes(normalizedSource)) || !normalize(after.text) || before.truncated !== expectedBeforeTruncated || before.sentinel !== (expectedBeforeTruncated ? '[[CONTEXT_BEFORE_TRUNCATED]]' : '[[CONTEXT_FILE_START]]') || after.truncated !== expectedAfterTruncated || after.sentinel !== (expectedAfterTruncated ? '[[CONTEXT_AFTER_TRUNCATED]]' : '[[CONTEXT_FILE_END]]')) throw Error(`CONTEXT_RUNTIME_BINDING:${index}`);
  });
  return {queue: {bytes: Buffer.from(queueBytes), parsed: queue}, anchors:{bytes:Buffer.from(anchorsBytes),parsed:anchors}, view: {bytes: Buffer.from(viewBytes), parsed: view}};
}

const arg = process.argv[2], round = path.join(here, 'rounds', 'ROUND-0001');
if (import.meta.url === `file://${process.argv[1]}` && arg === '--freeze') {
  const built = buildContextInput();
  fs.writeFileSync(path.join(round, 'CONTEXT-QUEUE.json'), built.queueBytes, {flag: 'wx'});
  fs.writeFileSync(path.join(round, 'CONTEXT-SOURCE-ANCHORS.json'), built.anchorsBytes, {flag: 'wx'});
  fs.writeFileSync(path.join(round, 'CONTEXT-QUEUE-VIEW.json'), built.viewBytes, {flag: 'wx'});
  console.log(JSON.stringify({status:'FROZEN_PENDING_INDEPENDENT_REVIEW', rows:55, context_queue_sha256:sha256(built.queueBytes), context_source_anchors_sha256:sha256(built.anchorsBytes), context_queue_view_sha256:sha256(built.viewBytes)}, null, 2));
} else if (import.meta.url === `file://${process.argv[1]}` && arg === '--refreeze-view') {
  const built = buildContextInput(), queuePath = path.join(round, 'CONTEXT-QUEUE.json'), anchorsPath=path.join(round,'CONTEXT-SOURCE-ANCHORS.json'), viewPath = path.join(round, 'CONTEXT-QUEUE-VIEW.json');
  if (!fs.readFileSync(queuePath).equals(built.queueBytes)) throw Error('CONTEXT_QUEUE_MUTATION_FORBIDDEN');
  fs.writeFileSync(anchorsPath,built.anchorsBytes);
  fs.writeFileSync(viewPath, built.viewBytes);
  console.log(JSON.stringify({status:'ANCHORS_AND_VIEW_REFROZEN_PENDING_FINAL_DUAL_REREVIEW', rows:55, context_queue_sha256:sha256(built.queueBytes), context_source_anchors_sha256:sha256(built.anchorsBytes), context_queue_view_sha256:sha256(built.viewBytes)}, null, 2));
} else if (import.meta.url === `file://${process.argv[1]}` && arg === '--check') {
  const fixtureRepo = materializeHistoricalRound1Fixture();
  try {
    const historicalRoot=path.join(fixtureRepo,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5'), historicalRound=path.join(historicalRoot,'rounds','ROUND-0001');
    const queueBytes = fs.readFileSync(path.join(round, 'CONTEXT-QUEUE.json')), anchorsBytes=fs.readFileSync(path.join(round,'CONTEXT-SOURCE-ANCHORS.json')), viewBytes = fs.readFileSync(path.join(round, 'CONTEXT-QUEUE-VIEW.json'));
    validateFrozenContextInputBytes({surfaceQueueBytes:fs.readFileSync(path.join(historicalRound,'SURFACE-QUEUE.json')),surfaceViewBytes:fs.readFileSync(path.join(historicalRound,'SURFACE-QUEUE-VIEW.json')),surfaceRecordsBytes:fs.readFileSync(path.join(historicalRound,'SURFACE-RECORDS.json')),surfaceAggregateBytes:fs.readFileSync(path.join(historicalRound,'SURFACE-AGGREGATE.json')),activeFrameBytes:fs.readFileSync(path.join(historicalRoot,'ACTIVE-FRAME.json')),queueBytes,anchorsBytes,viewBytes});
    if(sha256(anchorsBytes)!==EXPECTED.sourceAnchors)throw Error('CONTEXT_SOURCE_ANCHOR_HASH');
    const releasePath=path.join(here,'rounds','ROUND-0001','RELEASE.json'), round2=path.join(here,'rounds','ROUND-0002'), activeBytes=fs.readFileSync(path.join(here,'ACTIVE-FRAME.json')),rawContextPath=path.join(here,'AUDITOR-RESPONSE-ROUND-0002-CONTEXT-CALL-001.json');
    const round2Files=['CONTEXT-AGGREGATE.json','CONTEXT-QUEUE-VIEW.json','CONTEXT-QUEUE.json','CONTEXT-RECORDS.json','CONTEXT-SOURCE-ANCHORS.json','SURFACE-AGGREGATE.json','SURFACE-QUEUE-VIEW.json','SURFACE-QUEUE.json','SURFACE-RECORDS.json'];
    const pendingPath=path.join(here,'PENDING-RELEASE.json'),pending=fs.existsSync(pendingPath)?JSON.parse(fs.readFileSync(pendingPath)):null;
    if(sha256(fs.readFileSync(releasePath))!=='bf37e1fc2f1015d6c86e0666154338df591d2f556a489b25ba775ccf7ce66119'||sha256(activeBytes)!=='c632d77064d1d80cd950de263ab3b3970820bed4102cb120900835ae279d1a85'||pending?.schema_version!=='gemini-context-v5-round-0002-pending-release-v1'||JSON.stringify(fs.readdirSync(round2).sort())!==JSON.stringify(round2Files)||sha256(fs.readFileSync(rawContextPath))!=='6f55afad6292844b221f9ece65282acf5edc66e978e177f3a23d94a782de0cfb'||sha256(fs.readFileSync(path.join(round2,'CONTEXT-RECORDS.json')))!=='177ff3f9fb77c795bc2e957790cac173a0efcae01580be2d74774a6f598ea1e1'||sha256(fs.readFileSync(path.join(round2,'CONTEXT-AGGREGATE.json')))!=='1306df81b4f7d9a5711d9e42927cd0b81ed0c5c1485af4499a74a2194996f56f')throw Error('CONTEXT_LIVE_COMPLETED_ROUND1_ROUND2_RELEASE_CANDIDATE_STATE');
    console.log(JSON.stringify({status:'PASS', historical_round:'ROUND-0001', historical_fixture:'EXACT_FROZEN_PRE_RELEASE_BYTES', rows:55, canonical:true, source_bytes_and_coordinates_verified:true, context_queue_sha256:sha256(queueBytes), context_source_anchors_sha256:sha256(anchorsBytes), context_queue_view_sha256:sha256(viewBytes), live_completed_rounds:1, live_audit_round:'ROUND-0002', live_round_0002_surface_results_materialized:true, live_round_0002_context_results_materialized:true, live_round_0002_release_implementation_review_required:true, live_real_release_created:false}, null, 2));
  } finally { fs.rmSync(fixtureRepo,{recursive:true,force:true}); }
} else if (import.meta.url === `file://${process.argv[1]}`) throw Error('usage: node context-queue-view.mjs --freeze | --refreeze-view | --check');
