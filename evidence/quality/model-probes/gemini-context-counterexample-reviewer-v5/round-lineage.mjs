import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {buildSurfaceQueueView, validateSurfaceQueueViewBytes} from './surface-queue-view.mjs';
import {validateFrozenContextInputBytes} from './context-queue-view.mjs';
import {ROUND2_AUDIT_ARTIFACTS, ROUND2_DECISIONS, ROUND2_EXPECTED_CORE_HASHES, ROUND2_PREDECESSOR, ROUND2_PRE_HASHES, ROUND2_RELEASE_AUTHORIZATION, ROUND2_RELEASE_PATHS} from './round-0002-release.mjs';

export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const releaseTask = '.ai/task/research-gemini-context-counterexample-reviewer-v5';
export const RELEASE_AUTHORIZATION_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/ROUND-0001-REPLACEMENT-RELEASE-AUTHORIZATION-001.json';
export const RELEASE_AUTHORIZATION_SHA256 = '87fca3852d57241fa9756cc8ac8269fd27bb4598ee780204bf9cbb15b7410d37';
export const RELEASE_FINAL_REVIEW_PATHS = Object.freeze({
  manifest: `${releaseTask}/ROUND-0001-RELEASE-NONADVERSARIAL-IMPLEMENTATION-CANDIDATE-MANIFEST.json`,
  normal: `${releaseTask}/ROUND-0001-RELEASE-NONADVERSARIAL-NORMAL-REVIEW-001.json`,
  senior: `${releaseTask}/ROUND-0001-RELEASE-NONADVERSARIAL-SENIOR-REVIEW-001.json`,
  gate: `${releaseTask}/ROUND-0001-RELEASE-NONADVERSARIAL-REVIEW-GATE-001.json`
});
export const RELEASE_MATERIALIZATION_REVIEW_PATHS = Object.freeze({
  manifest: `${releaseTask}/ROUND-0001-RELEASE-HARNESS-REPAIR-IMPLEMENTATION-CANDIDATE-MANIFEST.json`,
  normal: `${releaseTask}/ROUND-0001-RELEASE-HARNESS-REPAIR-NORMAL-REVIEW-001.json`,
  senior: `${releaseTask}/ROUND-0001-RELEASE-HARNESS-REPAIR-SENIOR-REVIEW-001.json`,
  gate: `${releaseTask}/ROUND-0001-RELEASE-HARNESS-REPAIR-REVIEW-GATE-001.json`
});
export const RELEASE_THREAT_MODEL_PATH = `${releaseTask}/RELEASE-THREAT-MODEL-CLARIFICATION-001.json`;
export const RELEASE_THREAT_MODEL = Object.freeze({
  mode: 'NON_ADVERSARIAL_REPOSITORY_WORKFLOW',
  protects_against: ['ACCIDENTAL_DRIFT', 'HARNESS_OR_PARSER_ERROR', 'MISSING_EXTRA_SYMLINK_OR_NONCANONICAL_ARTIFACT', 'STALE_OR_INCONSISTENT_HASH_OR_STATE', 'UNAUTHORIZED_PHASE_ADVANCEMENT'],
  out_of_scope: ['MALICIOUS_TAMPERING', 'WHOLE_PACKAGE_REWRITE', 'REVIEWER_IDENTITY_FORGERY', 'VALIDATOR_REWRITE'],
  review_evidence_semantics: 'WORKFLOW_RECORDS_NOT_AUTHENTICITY_PROOFS'
});
export const RELEASE_IMPLEMENTATION_CANDIDATE_RECIPE = 'SHA256(concatenation in listed order of repo-relative path UTF-8 bytes + NUL + lowercase raw-file SHA-256 ASCII + LF)';
export const RELEASE_PROVENANCE_BINDING = Object.freeze({
  candidate_ref: '46d6b354b6322c5e90bceee8445d4089bd832cf00f5b615d5469508e0e50a0d2',
  candidate_manifest_sha256: '514ef8bcf797e4fb4662446fd3c6ce7f2665e1f5dcb51a2a1872049aa19f4260',
  normal_review_sha256: 'ff6d2cd2471cdd5c5a11a872b1dd3286edcb5b3cdc306a53697bb1ad0220fd85',
  senior_review_sha256: '03db068fa51b67a0b7afca36d877eabd36432459a393a5b127e258739d41905e',
  gate_sha256: '4294bc3bbea52ad343cb3927ac20f9f49d0ba99e414df177e305af2877e07c1c'
});
export const RELEASE_EXPECTED_AUTHENTIC_HASHES = Object.freeze({
  release_sha256: 'bf37e1fc2f1015d6c86e0666154338df591d2f556a489b25ba775ccf7ce66119',
  completed_experiment_sha256: '0440ccb84c6ee3689b8396e8a73d6172bb6bfc9c4a3ba60f686108a116cb0679',
  active_frame_sha256: 'c632d77064d1d80cd950de263ab3b3970820bed4102cb120900835ae279d1a85',
  lineage_sha256: '0fc604bc50220f8accd584f63d7aa5e560d88a2c8a23e43ebb94af3328b9ce7d',
  reserve_state_sha256: '123ec9dcd51c96f8843e69e163d25f9765fbdf411e77981ff65b4ecfe36d6eba',
  round_index_sha256: '036c80ebcce893be298e833f7aeb27983b95df65043dbc032cdac6480a9f243f',
  release_state_sha256: '0378c39116b0e8c30c9089784cc63baa7b7adff5dbfd2d0778dcb0aef7169921'
});
export const RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS = Object.freeze([
  {path: `${releaseTask}/STATE.json`, reason: 'mutable orchestration state excluded to avoid candidate churn'},
  {path: RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest, reason: 'self-reference excluded to avoid circular hashing'},
  {path: RELEASE_MATERIALIZATION_REVIEW_PATHS.normal, reason: 'future independent normal rereview record'},
  {path: RELEASE_MATERIALIZATION_REVIEW_PATHS.senior, reason: 'future independent senior rereview record'},
  {path: RELEASE_MATERIALIZATION_REVIEW_PATHS.gate, reason: 'future combined materialization gate'}
]);
const textCompare = (a, b) => Buffer.compare(Buffer.from(String(a)), Buffer.from(String(b)));
const hex64 = value => typeof value === 'string' && /^[0-9a-f]{64}$/u.test(value);
const uuid = value => typeof value === 'string' && /^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/u.test(value);
const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value)
  && JSON.stringify(Object.keys(value).sort(textCompare)) === JSON.stringify([...keys].sort(textCompare));

function parseJsonNoDuplicateKeys(bytes, label) {
  const text = bytes.toString('utf8'); if (!Buffer.from(text).equals(bytes)) throw Error(`${label}_UTF8`); let at = 0;
  const whitespace = () => { while (/\s/u.test(text[at] ?? '')) at += 1; };
  const string = () => { const start = at; if (text[at++] !== '"') throw Error(`${label}_STRING`); while (at < text.length) { if (text[at] === '\\') { at += 2; continue; } if (text[at++] === '"') return JSON.parse(text.slice(start, at)); } throw Error(`${label}_STRING`); };
  const value = () => {
    whitespace(); const token = text[at];
    if (token === '"') return string();
    if (token === '{') { at += 1; whitespace(); const out = {}, seen = new Set(); if (text[at] === '}') { at += 1; return out; } while (true) { whitespace(); const key = string(); if (seen.has(key)) throw Error(`${label}_DUPLICATE_KEY:${key}`); seen.add(key); whitespace(); if (text[at++] !== ':') throw Error(`${label}_OBJECT`); out[key] = value(); whitespace(); if (text[at] === '}') { at += 1; return out; } if (text[at++] !== ',') throw Error(`${label}_OBJECT`); } }
    if (token === '[') { at += 1; whitespace(); const out = []; if (text[at] === ']') { at += 1; return out; } while (true) { out.push(value()); whitespace(); if (text[at] === ']') { at += 1; return out; } if (text[at++] !== ',') throw Error(`${label}_ARRAY`); } }
    for (const [literal, parsed] of [['true', true], ['false', false], ['null', null]]) if (text.startsWith(literal, at)) { at += literal.length; return parsed; }
    const match = text.slice(at).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/u); if (!match) throw Error(`${label}_VALUE`); at += match[0].length; return JSON.parse(match[0]);
  };
  const parsed = value(); whitespace(); if (at !== text.length) throw Error(`${label}_TRAILING_BYTES`); return parsed;
}

function decodeCanonicalNoDuplicateKeys(value, label) {
  const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value), parsed = parseJsonNoDuplicateKeys(bytes, label);
  if (!bytes.equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return {bytes, parsed};
}

export const PROTOCOL = Object.freeze({
  schema: 'gemini-context-v5-round-lineage-v1',
  seed: 'gemini-context-counterexample-reviewer-v4/canonical-selection/v1',
  fixedSourceCommit: '624a67329fe2ad440c5b344785a9c73fcf22ae63',
  inventoryRawSha256: '1fb97b26457ebda2b6c03be40e3fe6121639fe58046004acee62aa3dc8f6af61',
  inventoryCanonicalSha256: '6064eba32bc43d3bf7dff40bd83b8d2183e73a5298bf5b0dcc28fb39c6b1d18a',
  totalFileCap: 3,
  cohortFileCap: 2,
  initialRows: 64,
  narrativeReserveRows: 78
});
const INHERITANCE_EXPECTED = Object.freeze({
  source_v4: {
    candidate_ref: 'de38ac3a2566af5c2d3d577867d8aec2abc4403c93ce43221427db10840c3172',
    frozen_ranked_64_frame_sha256: '064349181e3ff4e85c5f9bf02dabfafba2e4f6dca48909eeae2e84454bf9e654',
    source_frame_sha256: 'bac449634a3174de08cd82080bc9e93b39a153250158c6a61e06f518a32af490',
    ranked_same_profile_reserve_sha256: '079f79491f8bf93e022778436359638e14d6c817b07b97fdd9945cab2eed8602'
  },
  embedded: {
    initial_frame_sha256: 'a88ef998d8f212a099eb480bc673d0fee833942b6a155d537124b1fc6a8b4c47',
    dialogue_reserve_sha256: '22350e760f0948ab7185974258303c4875cfbe030a659faf877d9d1fc7bc481b',
    narrative_reserve_sha256: 'e28c169aaaedde0215dbe762b214cc9acb759968ce103f1fa5bd4bcfd4042154',
    frame_identity_sha256: 'e4a6426a9fbb6588daa50b0e0406a5e6f83af91082cb9caf3e458d12ef8047ae',
    reserve_identity_sha256: 'be72bc7b65fe14da2325ba3a198237b9cf4f09e06aaa2ec8fa6b4444fd0db2e8',
    selected_rows: 64, reserve_rows: 311, dialogue_reserve_rows: 233, narrative_reserve_rows: 78
  }
});

const rowKeys = ['neutral_id', 'cohort', 'profile', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256'];
const reserveKeys = ['profile', 'reserve_rank', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256'];
export const rowIdentity = row => sha256(jsonBytes(Object.fromEntries(rowKeys.map(key => [key, row[key]]))));

function assertRow(row, reserve = false) {
  const keys = reserve ? reserveKeys : rowKeys;
  if (!exactKeys(row, keys)) throw Error(`ROW_KEYS:${row?.neutral_id ?? row?.revision_id ?? '<unknown>'}`);
  if (!['dialogue', 'narrative'].includes(row.profile) || typeof row.public_source_file !== 'string' || !row.public_source_file.startsWith('game/modules/tome/')) throw Error('ROW_SCOPE');
  for (const key of ['revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256']) if (!hex64(row[key])) throw Error(`ROW_HASH:${key}`);
  if (reserve) {
    if (!Number.isInteger(row.reserve_rank) || row.reserve_rank < 1) throw Error('RESERVE_RANK');
  } else if (!/^V4-[DC]-[DN]\d{2}$/u.test(row.neutral_id) || !['discovery', 'confirmation'].includes(row.cohort)) throw Error('ROW_SLOT');
}

function duplicates(values) { return values.length !== new Set(values).size; }
function quotaKey(row) { return `${row.cohort}:${row.profile}`; }
function unavailable(state) { return new Set([...state.consumed, ...state.banned].filter(id => state.reserveByRevision.has(id))); }

export function assertActiveFrame(rows) {
  rows.forEach(row => assertRow(row));
  if (duplicates(rows.map(row => row.neutral_id))) throw Error('ACTIVE_DUPLICATE_SLOT');
  for (const key of ['revision_id', 'revision_uid', 'normalized_source_sha256', 'normalized_context_sha256']) if (duplicates(rows.map(row => row[key]))) throw Error(`ACTIVE_DUPLICATE:${key}`);
  for (const profile of ['dialogue', 'narrative']) {
    const profileRows = rows.filter(row => row.profile === profile);
    for (const file of new Set(profileRows.map(row => row.public_source_file))) {
      if (profileRows.filter(row => row.public_source_file === file).length > PROTOCOL.totalFileCap) throw Error(`ACTIVE_TOTAL_CAP:${profile}:${file}`);
      for (const cohort of ['discovery', 'confirmation']) if (profileRows.filter(row => row.cohort === cohort && row.public_source_file === file).length > PROTOCOL.cohortFileCap) throw Error(`ACTIVE_COHORT_CAP:${profile}:${cohort}:${file}`);
    }
  }
}

export function initialize(frame, reserves) {
  if (!exactKeys(frame, ['schema_version', 'status', 'inventory_raw_sha256', 'inventory_canonical_array_sha256', 'fixed_source_commit', 'selection_seed', 'file_total_cap', 'cohort_file_cap', 'items'])) throw Error('INITIAL_FRAME_SCHEMA');
  if (frame.schema_version !== 'gemini-context-v5-initial-frame-v1' || frame.status !== 'FROZEN_INHERITED_FROM_V4' || frame.inventory_raw_sha256 !== PROTOCOL.inventoryRawSha256 || frame.inventory_canonical_array_sha256 !== PROTOCOL.inventoryCanonicalSha256 || frame.fixed_source_commit !== PROTOCOL.fixedSourceCommit || frame.selection_seed !== PROTOCOL.seed || frame.file_total_cap !== 3 || frame.cohort_file_cap !== 2) throw Error('INITIAL_FRAME_BINDING');
  if (!Array.isArray(frame.items) || frame.items.length !== PROTOCOL.initialRows) throw Error('INITIAL_FRAME_COUNT');
  frame.items.forEach(row => assertRow(row));
  const quotas = new Map(); for (const row of frame.items) quotas.set(quotaKey(row), (quotas.get(quotaKey(row)) ?? 0) + 1);
  for (const cohort of ['discovery', 'confirmation']) for (const profile of ['dialogue', 'narrative']) if (quotas.get(`${cohort}:${profile}`) !== 16) throw Error(`INITIAL_QUOTA:${cohort}:${profile}`);
  assertActiveFrame(frame.items);
  if (!Array.isArray(reserves)) throw Error('RESERVE_ARRAY'); reserves.forEach(row => assertRow(row, true));
  for (const profile of ['dialogue', 'narrative']) {
    const ranks = reserves.filter(row => row.profile === profile).map(row => row.reserve_rank);
    if (ranks.some((rank, index) => rank !== index + 1)) throw Error(`RESERVE_RANK_ORDER:${profile}`);
  }
  if (reserves.filter(row => row.profile === 'narrative').length !== PROTOCOL.narrativeReserveRows) throw Error('NARRATIVE_RESERVE_DRIFT');
  const all = [...frame.items, ...reserves];
  for (const key of ['revision_id', 'revision_uid', 'normalized_source_sha256', 'normalized_context_sha256']) if (duplicates(all.map(row => row[key]))) throw Error(`GLOBAL_DUPLICATE:${key}`);
  const reserveByRevision = new Map(reserves.map(row => [row.revision_id, row]));
  return {
    round: 0,
    initialFrameSha256: sha256(jsonBytes(frame)),
    active: frame.items.map(row => ({...row})),
    reserves: reserves.map(row => ({...row})),
    reserveByRevision,
    banned: new Set(), consumed: new Set(),
    lineage: new Map(frame.items.map(row => [row.neutral_id, {neutral_id: row.neutral_id, revisions: [row.revision_id], edges: []}])),
    lastReleaseSha256: null, completedRelease: null,
    roundIndex: []
  };
}

export function activeFrameDocument(state) {
  return {schema_version: 'gemini-context-v5-active-frame-v1', initial_frame_sha256: state.initialFrameSha256, last_completed_round: state.round, items: state.active};
}
export const activeFrameSha256 = state => sha256(jsonBytes(activeFrameDocument(state)));

function queueItem(row) { return {neutral_id: row.neutral_id, revision_id: row.revision_id, row_identity_sha256: rowIdentity(row)}; }
function decodeCanonical(value, label) {
  const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value);
  let parsed; try { parsed = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  if (!bytes.equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return {bytes, parsed};
}

function aggregateDocument(stage, queueBytes, recordsBytes, records, queueViewBytes = null) {
  if (stage === 'surface' && queueViewBytes) {
    const counts = Object.fromEntries(['PASS_SURFACE', 'NOT_CLEAN', 'OUT_OF_SCOPE_NON_PROSE'].map(verdict => [verdict, records.items.filter(item => item.verdict === verdict).length]));
    return {
      schema_version: 'gemini-context-v5-surface-aggregate-v2',
      round_id: records.round_id,
      stage: 'SURFACE',
      surface_queue_sha256: sha256(queueBytes),
      surface_queue_view_sha256: sha256(queueViewBytes),
      surface_records_sha256: sha256(recordsBytes),
      counts,
      pass_ids: records.items.filter(item => item.verdict === 'PASS_SURFACE').map(item => item.neutral_id),
      reject_ids: records.items.filter(item => item.verdict !== 'PASS_SURFACE').map(item => item.neutral_id),
      items: records.items
    };
  }
  return {
    schema_version: `gemini-context-v5-${stage}-aggregate-v1`,
    stage: stage.toUpperCase(),
    queue_sha256: sha256(queueBytes),
    ...(queueViewBytes ? {queue_view_sha256: sha256(queueViewBytes)} : {}),
    records_sha256: sha256(recordsBytes),
    accepted_ids: records.items.filter(item => stage === 'surface' ? item.verdict === 'PASS_SURFACE' : item.verdict === 'CLEAN_NO_MATERIAL_DEFECT').map(item => item.neutral_id),
    items: records.items
  };
}

export function buildSurfaceAggregateBytes(queueBytes, queueViewBytes, recordsBytes) {
  const records = decodeCanonical(recordsBytes, 'SURFACE_RECORDS');
  return jsonBytes(aggregateDocument('surface', queueBytes, records.bytes, records.parsed, queueViewBytes));
}

export function loadValidatedSurfaceAuditorResponse({root, binding, queueBytes, queueViewBytes}) {
  const bindingKeys = ['artifact_path', 'artifact_sha256', 'artifact_role', 'non_regenerable', 'auditor_agent_id', 'authorized_call_number', 'records_schema_version', 'item_count', 'verdict_counts', 'expected_surface_records_sha256', 'expected_surface_aggregate_sha256'];
  if (!exactKeys(binding, bindingKeys) || binding.artifact_path !== 'AUDITOR-RESPONSE-ROUND-0001-SURFACE-CALL-002.json' || binding.artifact_sha256 !== '53596f081abdbf12836d133b27d4b5f0eec8ff8a2d779d1b6daacc24257528ae' || binding.artifact_role !== 'AUTHORIZED_SURFACE_AUDITOR_RESPONSE_NOT_FORMAL_GEMINI_OUTPUT_NOT_COMPLETED_SURFACE_RECORD' || binding.non_regenerable !== true || binding.auditor_agent_id !== '12cb169c-bcf5-44e3-8182-92abe48b9f08' || binding.authorized_call_number !== 2 || binding.records_schema_version !== 'gemini-context-v5-surface-records-v2' || binding.item_count !== 64 || binding.expected_surface_records_sha256 !== binding.artifact_sha256 || binding.expected_surface_aggregate_sha256 !== 'e9c1026d5dffd1f2e88f911e5c897f7361131a4cd82c5e18f688b82aa0d06967' || !exactKeys(binding.verdict_counts, ['PASS_SURFACE', 'NOT_CLEAN', 'OUT_OF_SCOPE_NON_PROSE'])) throw Error('SURFACE_AUDITOR_RESPONSE_BINDING');
  const file = path.join(root, binding.artifact_path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('SURFACE_AUDITOR_RESPONSE_FILE_TYPE');
  const records = decodeCanonical(fs.readFileSync(file), 'SURFACE_AUDITOR_RESPONSE');
  if (sha256(records.bytes) !== binding.artifact_sha256) throw Error('SURFACE_AUDITOR_RESPONSE_HASH');
  const queue = decodeCanonical(queueBytes, 'SURFACE_QUEUE'), view = decodeCanonical(queueViewBytes, 'SURFACE_QUEUE_VIEW');
  if (!exactKeys(records.parsed, ['schema_version', 'round_id', 'stage', 'surface_queue_sha256', 'surface_queue_view_sha256', 'items']) || records.parsed.schema_version !== binding.records_schema_version || records.parsed.round_id !== queue.parsed.round_id || records.parsed.stage !== 'SURFACE' || records.parsed.surface_queue_sha256 !== sha256(queue.bytes) || records.parsed.surface_queue_view_sha256 !== sha256(view.bytes) || !Array.isArray(records.parsed.items) || records.parsed.items.length !== queue.parsed.items?.length || records.parsed.items.length !== binding.item_count) throw Error('SURFACE_AUDITOR_RESPONSE_SCHEMA');
  const allowed = new Set(['PASS_SURFACE', 'NOT_CLEAN', 'OUT_OF_SCOPE_NON_PROSE']);
  records.parsed.items.forEach((item, index) => { if (!exactKeys(item, ['neutral_id', 'verdict', 'evidence']) || item.neutral_id !== queue.parsed.items[index]?.neutral_id || !allowed.has(item.verdict) || typeof item.evidence !== 'string' || !item.evidence) throw Error(`SURFACE_AUDITOR_RESPONSE_ITEM:${index}`); });
  const counts = Object.fromEntries([...allowed].map(verdict => [verdict, records.parsed.items.filter(item => item.verdict === verdict).length]));
  if (JSON.stringify(counts) !== JSON.stringify(binding.verdict_counts)) throw Error('SURFACE_AUDITOR_RESPONSE_COUNTS');
  return {bytes: records.bytes, parsed: records.parsed, counts};
}

export function prepareSurfaceIntermediateArtifacts({root, binding, queueBytes, queueViewBytes}) {
  const response = loadValidatedSurfaceAuditorResponse({root, binding, queueBytes, queueViewBytes});
  const aggregateBytes = buildSurfaceAggregateBytes(queueBytes, queueViewBytes, response.bytes);
  if (sha256(aggregateBytes) !== binding.expected_surface_aggregate_sha256) throw Error('SURFACE_AUDITOR_RESPONSE_AGGREGATE_HASH');
  return {surface_records: response.bytes, surface_aggregate: aggregateBytes, counts: response.counts};
}

export const CONTEXT_AUDITOR_RESPONSE = Object.freeze({
  path: 'AUDITOR-RESPONSE-ROUND-0001-CONTEXT-CALL-001.json',
  sha256: 'cd3c074dbe2942fb9d730f7e49ff7fb554416a8d8095ad889edc4c704e2ef080',
  auditorAgentId: '11949533-95df-458c-8211-2ee44316fb15',
  authorizedCallNumber: 1
});

export function loadValidatedContextAuditorResponse({root, binding, queueBytes, anchorsBytes, viewBytes}) {
  const bindingKeys = ['artifact_path', 'artifact_sha256', 'artifact_role', 'non_regenerable', 'auditor_agent_id', 'authorized_call_number', 'records_schema_version', 'item_count', 'verdict_counts', 'context_queue_sha256', 'context_source_anchors_sha256', 'context_queue_view_sha256', 'expected_context_records_sha256', 'expected_context_aggregate_sha256'];
  if (!exactKeys(binding, bindingKeys) || binding.artifact_path !== CONTEXT_AUDITOR_RESPONSE.path || binding.artifact_sha256 !== CONTEXT_AUDITOR_RESPONSE.sha256 || binding.artifact_role !== 'AUTHORIZED_CONTEXT_AUDITOR_RESPONSE_NOT_FORMAL_GEMINI_OUTPUT_NOT_MATERIALIZED_CONTEXT_RECORD' || binding.non_regenerable !== true || binding.auditor_agent_id !== CONTEXT_AUDITOR_RESPONSE.auditorAgentId || binding.authorized_call_number !== CONTEXT_AUDITOR_RESPONSE.authorizedCallNumber || binding.records_schema_version !== 'gemini-context-v5-context-records-v2' || binding.item_count !== 55 || binding.expected_context_records_sha256 !== binding.artifact_sha256 || !hex64(binding.expected_context_aggregate_sha256) || !exactKeys(binding.verdict_counts, ['CLEAN_NO_MATERIAL_DEFECT', 'NOT_CLEAN']) || binding.verdict_counts.CLEAN_NO_MATERIAL_DEFECT !== 54 || binding.verdict_counts.NOT_CLEAN !== 1) throw Error('CONTEXT_AUDITOR_RESPONSE_BINDING');
  const file = path.join(root, binding.artifact_path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_AUDITOR_RESPONSE_FILE_TYPE');
  const records = decodeCanonicalNoDuplicateKeys(fs.readFileSync(file), 'CONTEXT_AUDITOR_RESPONSE');
  if (sha256(records.bytes) !== CONTEXT_AUDITOR_RESPONSE.sha256) throw Error('CONTEXT_AUDITOR_RESPONSE_HASH');
  const queue = decodeCanonical(queueBytes, 'CONTEXT_QUEUE'), anchors = decodeCanonical(anchorsBytes, 'CONTEXT_SOURCE_ANCHORS'), view = decodeCanonical(viewBytes, 'CONTEXT_QUEUE_VIEW');
  if (binding.context_queue_sha256 !== sha256(queue.bytes) || binding.context_source_anchors_sha256 !== sha256(anchors.bytes) || binding.context_queue_view_sha256 !== sha256(view.bytes)) throw Error('CONTEXT_AUDITOR_RESPONSE_INPUT_BINDING');
  const keys = ['schema_version', 'round_id', 'stage', 'context_queue_sha256', 'context_source_anchors_sha256', 'context_queue_view_sha256', 'items'];
  if (!exactKeys(records.parsed, keys) || records.parsed.schema_version !== binding.records_schema_version || records.parsed.round_id !== queue.parsed.round_id || records.parsed.stage !== 'CONTEXT' || records.parsed.context_queue_sha256 !== sha256(queue.bytes) || records.parsed.context_source_anchors_sha256 !== sha256(anchors.bytes) || records.parsed.context_queue_view_sha256 !== sha256(view.bytes) || !Array.isArray(records.parsed.items) || records.parsed.items.length !== 55 || records.parsed.items.length !== queue.parsed.items?.length) throw Error('CONTEXT_AUDITOR_RESPONSE_SCHEMA');
  const allowed = new Set(['CLEAN_NO_MATERIAL_DEFECT', 'NOT_CLEAN']);
  records.parsed.items.forEach((item, index) => { if (!exactKeys(item, ['neutral_id', 'verdict', 'evidence']) || item.neutral_id !== queue.parsed.items[index]?.neutral_id || !allowed.has(item.verdict) || typeof item.evidence !== 'string' || !item.evidence.trim()) throw Error(`CONTEXT_AUDITOR_RESPONSE_ITEM:${index}`); });
  const counts = Object.fromEntries([...allowed].map(verdict => [verdict, records.parsed.items.filter(item => item.verdict === verdict).length]));
  if (JSON.stringify(counts) !== JSON.stringify(binding.verdict_counts)) throw Error('CONTEXT_AUDITOR_RESPONSE_COUNTS');
  return {bytes: records.bytes, parsed: records.parsed, counts};
}

export function buildContextAggregateBytes(recordsBytes) {
  const records = decodeCanonicalNoDuplicateKeys(recordsBytes, 'CONTEXT_RECORDS');
  const allowed = ['CLEAN_NO_MATERIAL_DEFECT', 'NOT_CLEAN'];
  const expectedCount = records.parsed.round_id === 'ROUND-0001' ? 55 : records.parsed.round_id === 'ROUND-0002' ? 9 : null;
  if (!exactKeys(records.parsed, ['schema_version', 'round_id', 'stage', 'context_queue_sha256', 'context_source_anchors_sha256', 'context_queue_view_sha256', 'items']) || records.parsed.schema_version !== 'gemini-context-v5-context-records-v2' || records.parsed.stage !== 'CONTEXT' || !Array.isArray(records.parsed.items) || expectedCount === null || records.parsed.items.length !== expectedCount) throw Error('CONTEXT_RECORDS_V2_SCHEMA');
  records.parsed.items.forEach((item, index) => { if (!exactKeys(item, ['neutral_id', 'verdict', 'evidence']) || !allowed.includes(item.verdict) || typeof item.evidence !== 'string' || !item.evidence.trim()) throw Error(`CONTEXT_RECORDS_V2_ITEM:${index}`); });
  const counts = Object.fromEntries(allowed.map(verdict => [verdict, records.parsed.items.filter(item => item.verdict === verdict).length]));
  return jsonBytes({schema_version: 'gemini-context-v5-context-aggregate-v2', round_id: records.parsed.round_id, stage: 'CONTEXT', context_queue_sha256: records.parsed.context_queue_sha256, context_source_anchors_sha256: records.parsed.context_source_anchors_sha256, context_queue_view_sha256: records.parsed.context_queue_view_sha256, context_records_sha256: sha256(records.bytes), counts, clean_ids: records.parsed.items.filter(item => item.verdict === 'CLEAN_NO_MATERIAL_DEFECT').map(item => item.neutral_id), not_clean_ids: records.parsed.items.filter(item => item.verdict === 'NOT_CLEAN').map(item => item.neutral_id), items: records.parsed.items});
}

export function prepareContextIntermediateArtifacts({root, binding, queueBytes, anchorsBytes, viewBytes}) {
  const response = loadValidatedContextAuditorResponse({root, binding, queueBytes, anchorsBytes, viewBytes}), aggregateBytes = buildContextAggregateBytes(response.bytes);
  if (sha256(aggregateBytes) !== binding.expected_context_aggregate_sha256) throw Error('CONTEXT_AUDITOR_RESPONSE_AGGREGATE_HASH');
  return {context_records: response.bytes, context_aggregate: aggregateBytes, counts: response.counts};
}

export function validatePendingContextArtifacts({state, queueBytes, anchorsBytes, viewBytes, recordsBytes, aggregateBytes, expected = null}) {
  const before = jsonBytes({round: state.round, active: state.active, consumed: [...state.consumed], banned: [...state.banned], lineage: [...state.lineage], lastReleaseSha256: state.lastReleaseSha256, roundIndex: state.roundIndex});
  const queue = decodeCanonical(queueBytes, 'PENDING_CONTEXT_QUEUE'), anchors = decodeCanonical(anchorsBytes, 'PENDING_CONTEXT_ANCHORS'), view = decodeCanonical(viewBytes, 'PENDING_CONTEXT_VIEW'), records = decodeCanonicalNoDuplicateKeys(recordsBytes, 'PENDING_CONTEXT_RECORDS'), aggregate = decodeCanonical(aggregateBytes, 'PENDING_CONTEXT_AGGREGATE');
  if (records.parsed.context_queue_sha256 !== sha256(queue.bytes) || records.parsed.context_source_anchors_sha256 !== sha256(anchors.bytes) || records.parsed.context_queue_view_sha256 !== sha256(view.bytes) || records.parsed.items.length !== queue.parsed.items?.length || records.parsed.items.some((item, index) => item.neutral_id !== queue.parsed.items[index]?.neutral_id)) throw Error('PENDING_CONTEXT_RECORDS_BINDING');
  const expectedAggregate = buildContextAggregateBytes(records.bytes); if (!aggregate.bytes.equals(expectedAggregate)) throw Error('PENDING_CONTEXT_AGGREGATE_DERIVATION');
  const summary = {context_records_sha256: sha256(records.bytes), context_aggregate_sha256: sha256(aggregate.bytes), counts: aggregate.parsed.counts, clean_ids: aggregate.parsed.clean_ids, not_clean_ids: aggregate.parsed.not_clean_ids};
  if (expected && JSON.stringify(summary) !== JSON.stringify(expected)) throw Error('PENDING_CONTEXT_EXPECTED_BINDING');
  const after = jsonBytes({round: state.round, active: state.active, consumed: [...state.consumed], banned: [...state.banned], lineage: [...state.lineage], lastReleaseSha256: state.lastReleaseSha256, roundIndex: state.roundIndex});
  if (!before.equals(after)) throw Error('PENDING_CONTEXT_STATE_MUTATION');
  return summary;
}

export function validatePendingContextResultsDirectory({roundDir, state, expectedContext}) {
  const names = ['CONTEXT-AGGREGATE.json', 'CONTEXT-QUEUE-VIEW.json', 'CONTEXT-QUEUE.json', 'CONTEXT-RECORDS.json', 'CONTEXT-SOURCE-ANCHORS.json', 'SURFACE-AGGREGATE.json', 'SURFACE-QUEUE-VIEW.json', 'SURFACE-QUEUE.json', 'SURFACE-RECORDS.json'];
  const stat = fs.lstatSync(roundDir); if (stat.isSymbolicLink() || !stat.isDirectory()) throw Error('PENDING_CONTEXT_RESULTS_DIRECTORY_TYPE');
  const actual = fs.readdirSync(roundDir).sort(textCompare); if (JSON.stringify(actual) !== JSON.stringify(names)) throw Error('PENDING_CONTEXT_RESULTS_ARTIFACT_SET');
  const bytes = {}; for (const name of names) { const file = path.join(roundDir, name), itemStat = fs.lstatSync(file); if (itemStat.isSymbolicLink() || !itemStat.isFile()) throw Error(`PENDING_CONTEXT_RESULTS_ARTIFACT_TYPE:${name}`); bytes[name] = fs.readFileSync(file); }
  validatePendingSurfaceArtifacts({state, queueBytes: bytes['SURFACE-QUEUE.json'], queueViewBytes: bytes['SURFACE-QUEUE-VIEW.json'], recordsBytes: bytes['SURFACE-RECORDS.json'], aggregateBytes: bytes['SURFACE-AGGREGATE.json'], selfContained: true});
  return validatePendingContextArtifacts({state, queueBytes: bytes['CONTEXT-QUEUE.json'], anchorsBytes: bytes['CONTEXT-SOURCE-ANCHORS.json'], viewBytes: bytes['CONTEXT-QUEUE-VIEW.json'], recordsBytes: bytes['CONTEXT-RECORDS.json'], aggregateBytes: bytes['CONTEXT-AGGREGATE.json'], expected: expectedContext});
}

function validateStage(stage, queueValue, recordsValue, aggregateValue, state, expectedItems = null, surfaceAggregateSha256 = null, queueViewValue = null, bundleRepo = null, contextExtras = null) {
  const queue = decodeCanonical(queueValue, `${stage.toUpperCase()}_QUEUE`), records = decodeCanonical(recordsValue, `${stage.toUpperCase()}_RECORDS`), aggregate = decodeCanonical(aggregateValue, `${stage.toUpperCase()}_AGGREGATE`);
  const surfaceV2=stage==='surface'&&queue.parsed.schema_version==='gemini-context-v5-surface-queue-v2',surfaceV3=stage==='surface'&&queue.parsed.schema_version==='gemini-context-v5-surface-queue-v3',authorizedSurface=surfaceV2||surfaceV3;
  const contextV2 = stage === 'context' && queue.parsed.schema_version === 'gemini-context-v5-context-queue-v2';
  const contextV3 = stage === 'context' && queue.parsed.schema_version === 'gemini-context-v5-round-0002-context-queue-v3';
  const sidecarContext = contextV2 || contextV3;
  const historicalActiveFrameBytes = jsonBytes(activeFrameDocument(state));
  const normalizedRepo = normalizeRepoOption(bundleRepo);
  const queueView = authorizedSurface ? (normalizedRepo === false ? decodeCanonical(queueViewValue, 'SURFACE_QUEUE_VIEW') : validateSurfaceQueueViewBytes({repo: normalizedRepo, queueBytes: queue.bytes, activeFrameBytes: historicalActiveFrameBytes, viewBytes: queueViewValue})) : null;
  const queueKeys = stage === 'surface'
    ? (surfaceV2 ? ['schema_version', 'round_id', 'stage', 'active_frame_sha256', 'predecessor_release_sha256', 'authorization_id', 'authorization_record_sha256', 'authorized_candidate_ref', 'final_pass_reviewer_agent_ids', 'items'] : surfaceV3 ? ['schema_version','round_id','stage','active_frame_sha256','predecessor_release_sha256','authorization_id','authorization_record_path','authorization_record_sha256','scope','item_count','items'] : ['schema_version', 'round_id', 'stage', 'active_frame_sha256', 'predecessor_release_sha256', 'items'])
    : (contextV2
      ? ['schema_version', 'round_id', 'stage', 'active_frame_sha256', 'predecessor_release_sha256', 'fixed_source_commit', 'surface_queue_sha256', 'surface_queue_view_sha256', 'surface_records_sha256', 'surface_aggregate_sha256', 'authorization_id', 'authorization_record_sha256', 'items']
      : contextV3
        ? ['schema_version','status','round_id','stage','predecessor_release_sha256','fixed_source_commit','authorization_basis','active_frame_sha256','lineage_sha256','reserve_state_sha256','round_index_sha256','release_state_sha256','experiment_sha256','surface_queue_sha256','surface_queue_view_sha256','surface_records_sha256','surface_aggregate_sha256','items']
      : ['schema_version', 'round_id', 'stage', 'active_frame_sha256', 'predecessor_release_sha256', 'surface_aggregate_sha256', 'items']);
  if (!exactKeys(queue.parsed, queueKeys) || (!authorizedSurface && !sidecarContext && queue.parsed.schema_version !== `gemini-context-v5-${stage}-queue-v1`) || queue.parsed.stage !== stage.toUpperCase() || queue.parsed.round_id !== `ROUND-${String(state.round + 1).padStart(4, '0')}` || queue.parsed.active_frame_sha256 !== activeFrameSha256(state) || queue.parsed.predecessor_release_sha256 !== state.lastReleaseSha256) throw Error(`${stage.toUpperCase()}_QUEUE_BINDING`);
  if (surfaceV2 && (!hex64(queue.parsed.authorization_record_sha256) || !hex64(queue.parsed.authorized_candidate_ref) || !exactKeys(queue.parsed.final_pass_reviewer_agent_ids, ['normal', 'senior']) || !Object.values(queue.parsed.final_pass_reviewer_agent_ids).every(value => typeof value === 'string' && /^[0-9a-f-]{36}$/u.test(value)))) throw Error('SURFACE_QUEUE_AUTHORIZATION_BINDING');
  if(surfaceV3&&(!hex64(queue.parsed.authorization_record_sha256)||queue.parsed.authorization_id!=='V5-ROUND-0002-SURFACE-AUDIT-001'||queue.parsed.authorization_record_path!=='.ai/task/research-gemini-context-counterexample-reviewer-v5/ROUND-0002-SURFACE-AUDIT-AUTHORIZATION-001.json'||queue.parsed.scope!=='EXACT_ROUND_0001_REPLACEMENTS_ONLY'||queue.parsed.item_count!==10))throw Error('SURFACE_QUEUE_AUTHORIZATION_BINDING');
  if (stage === 'context' && queue.parsed.surface_aggregate_sha256 !== surfaceAggregateSha256) throw Error('CONTEXT_SURFACE_BINDING');
  if (contextV2 && (!contextExtras || queue.parsed.fixed_source_commit !== PROTOCOL.fixedSourceCommit || queue.parsed.surface_queue_sha256 !== sha256(contextExtras.surfaceQueueBytes) || queue.parsed.surface_queue_view_sha256 !== sha256(contextExtras.surfaceQueueViewBytes) || queue.parsed.surface_records_sha256 !== sha256(contextExtras.surfaceRecordsBytes) || !hex64(queue.parsed.authorization_record_sha256))) throw Error('CONTEXT_V2_INPUT_BINDING');
  if (contextV3 && (!contextExtras || queue.parsed.status !== 'FROZEN_CONTEXT_INPUT_PENDING_INDEPENDENT_REVIEW' || queue.parsed.fixed_source_commit !== PROTOCOL.fixedSourceCommit || queue.parsed.authorization_basis !== 'USER_AUTHORIZED_COMPLETE_ROUND_0002_AUDIT' || queue.parsed.lineage_sha256 !== ROUND2_PRE_HASHES.lineage_sha256 || queue.parsed.reserve_state_sha256 !== ROUND2_PRE_HASHES.reserve_state_sha256 || queue.parsed.round_index_sha256 !== ROUND2_PRE_HASHES.round_index_sha256 || queue.parsed.release_state_sha256 !== ROUND2_PRE_HASHES.release_state_sha256 || queue.parsed.experiment_sha256 !== ROUND2_PRE_HASHES.experiment_sha256 || queue.parsed.surface_queue_sha256 !== sha256(contextExtras.surfaceQueueBytes) || queue.parsed.surface_queue_view_sha256 !== sha256(contextExtras.surfaceQueueViewBytes) || queue.parsed.surface_records_sha256 !== sha256(contextExtras.surfaceRecordsBytes) || queue.parsed.surface_aggregate_sha256 !== surfaceAggregateSha256)) throw Error('CONTEXT_V3_INPUT_BINDING');
  const active = new Map(state.active.map(row => [row.neutral_id, row]));
  if (!Array.isArray(queue.parsed.items) || queue.parsed.items.length < 1 || duplicates(queue.parsed.items.map(item => item.neutral_id))) throw Error(`${stage.toUpperCase()}_QUEUE_ITEMS`);
  for (const item of queue.parsed.items) {
    if (!exactKeys(item, ['neutral_id', 'revision_id', 'row_identity_sha256'])) throw Error(`${stage.toUpperCase()}_QUEUE_ITEM_SCHEMA`);
    const row = active.get(item.neutral_id); if (!row || item.revision_id !== row.revision_id || item.row_identity_sha256 !== rowIdentity(row)) throw Error(`${stage.toUpperCase()}_QUEUE_RESOLUTION:${item.neutral_id}`);
  }
  if (expectedItems && JSON.stringify(queue.parsed.items) !== JSON.stringify(expectedItems)) throw Error('CONTEXT_QUEUE_NOT_SURFACE_PASS_SET');
  const recordKeys = authorizedSurface ? ['schema_version', 'round_id', 'stage', 'surface_queue_sha256', 'surface_queue_view_sha256', 'items'] : sidecarContext ? ['schema_version', 'round_id', 'stage', 'context_queue_sha256', 'context_source_anchors_sha256', 'context_queue_view_sha256', 'items'] : ['schema_version', 'round_id', 'stage', 'items'];
  const recordSchema = authorizedSurface ? 'gemini-context-v5-surface-records-v2' : sidecarContext ? 'gemini-context-v5-context-records-v2' : `gemini-context-v5-${stage}-records-v1`;
  if (!exactKeys(records.parsed, recordKeys) || records.parsed.schema_version !== recordSchema || records.parsed.round_id !== queue.parsed.round_id || records.parsed.stage !== stage.toUpperCase() || !Array.isArray(records.parsed.items) || records.parsed.items.length !== queue.parsed.items.length) throw Error(`${stage.toUpperCase()}_RECORDS_SCHEMA`);
  if (authorizedSurface && (records.parsed.surface_queue_sha256 !== sha256(queue.bytes) || records.parsed.surface_queue_view_sha256 !== sha256(queueView.bytes))) throw Error('SURFACE_RECORDS_SIDECAR_BINDING');
  if (sidecarContext && (records.parsed.context_queue_sha256 !== sha256(queue.bytes) || records.parsed.context_source_anchors_sha256 !== sha256(contextExtras.contextSourceAnchorsBytes) || records.parsed.context_queue_view_sha256 !== sha256(contextExtras.contextQueueViewBytes))) throw Error('CONTEXT_RECORDS_SIDECAR_BINDING');
  const allowed = stage === 'surface' ? ['PASS_SURFACE', 'NOT_CLEAN', 'OUT_OF_SCOPE_NON_PROSE'] : ['CLEAN_NO_MATERIAL_DEFECT', 'NOT_CLEAN'];
  records.parsed.items.forEach((item, index) => { if (!exactKeys(item, ['neutral_id', 'verdict', 'evidence']) || item.neutral_id !== queue.parsed.items[index].neutral_id || !allowed.includes(item.verdict) || typeof item.evidence !== 'string' || !item.evidence) throw Error(`${stage.toUpperCase()}_RECORD:${index}`); });
  const expectedAggregateBytes = sidecarContext ? buildContextAggregateBytes(records.bytes) : jsonBytes(aggregateDocument(stage, queue.bytes, records.bytes, records.parsed, queueView?.bytes ?? null));
  if (!aggregate.bytes.equals(expectedAggregateBytes)) throw Error(`${stage.toUpperCase()}_AGGREGATE_DERIVATION`);
  return {queue, queueView, records, aggregate, contextV2, contextV3};
}

export function validatePendingSurfaceArtifacts({repo, state, queueBytes, queueViewBytes, recordsBytes, aggregateBytes, expected = null, selfContained = false}) {
  const before = jsonBytes({round: state.round, active: state.active, consumed: [...state.consumed], banned: [...state.banned], lineage: [...state.lineage], lastReleaseSha256: state.lastReleaseSha256, roundIndex: state.roundIndex});
  const surface = validateStage('surface', queueBytes, recordsBytes, aggregateBytes, state, null, null, queueViewBytes, selfContained ? false : repo);
  const summary = {
    surface_records_sha256: sha256(surface.records.bytes),
    surface_aggregate_sha256: sha256(surface.aggregate.bytes),
    counts: surface.aggregate.parsed.counts,
    pass_ids: surface.aggregate.parsed.pass_ids,
    reject_ids: surface.aggregate.parsed.reject_ids
  };
  if (expected && JSON.stringify(summary) !== JSON.stringify(expected)) throw Error('PENDING_SURFACE_EXPECTED_BINDING');
  const after = jsonBytes({round: state.round, active: state.active, consumed: [...state.consumed], banned: [...state.banned], lineage: [...state.lineage], lastReleaseSha256: state.lastReleaseSha256, roundIndex: state.roundIndex});
  if (!before.equals(after)) throw Error('PENDING_SURFACE_STATE_MUTATION');
  return summary;
}

function skipReason(candidate, active) {
  if (active.some(row => row.revision_id === candidate.revision_id)) return 'REVISION_COLLISION';
  if (active.some(row => row.revision_uid === candidate.revision_uid)) return 'BASE_IDENTITY_COLLISION';
  if (active.some(row => row.normalized_source_sha256 === candidate.normalized_source_sha256)) return 'NORMALIZED_SOURCE_COLLISION';
  if (active.some(row => row.normalized_context_sha256 === candidate.normalized_context_sha256)) return 'NORMALIZED_CONTEXT_COLLISION';
  const same = active.filter(row => row.profile === candidate.profile && row.public_source_file === candidate.public_source_file);
  if (same.length >= PROTOCOL.totalFileCap) return 'ACTIVE_FILE_TOTAL_CAP';
  return null;
}
function cohortCapReason(candidate, cohort, active) {
  return active.filter(row => row.profile === candidate.profile && row.cohort === cohort && row.public_source_file === candidate.public_source_file).length >= PROTOCOL.cohortFileCap ? 'ACTIVE_FILE_COHORT_CAP' : null;
}

function cloneState(state) {
  const reserves = state.reserves.map(row => ({...row}));
  return {round: state.round, initialFrameSha256: state.initialFrameSha256, active: state.active.map(row => ({...row})), reserves, reserveByRevision: new Map(reserves.map(row => [row.revision_id, row])), banned: new Set(state.banned), consumed: new Set(state.consumed), lineage: new Map([...state.lineage].map(([id, chain]) => [id, structuredClone(chain)])), lastReleaseSha256: state.lastReleaseSha256, completedRelease: structuredClone(state.completedRelease), roundIndex: structuredClone(state.roundIndex)};
}

export function normalizeRepoOption(repo) { return repo === false ? false : repo == null ? undefined : repo; }

function assertReleaseProvenance(authorization, reviewGate) {
  const authorizationKeys = ['authorization_id', 'authorization_path', 'authorization_sha256', 'authorized_by', 'executor_agent_id'];
  if (!exactKeys(authorization, authorizationKeys) || authorization.authorization_id !== 'V5-ROUND-0001-REPLACEMENT-RELEASE-IMPLEMENTATION-001' || typeof authorization.authorization_path !== 'string' || !authorization.authorization_path.endsWith('/ROUND-0001-REPLACEMENT-RELEASE-AUTHORIZATION-001.json') || !hex64(authorization.authorization_sha256) || authorization.authorized_by !== 'user' || authorization.executor_agent_id !== 'f5cc0aa8-b313-4ca7-8f92-191041de73a8') throw Error('ROUND_RELEASE_AUTHORIZATION_PROVENANCE');
  const reviewKeys = ['status', 'verification_mode', 'candidate_ref', 'candidate_manifest_sha256', 'normal', 'senior', 'gate_path', 'gate_sha256'];
  const reviewerKeys = ['agent_id', 'review_path', 'review_sha256'];
  if (!exactKeys(reviewGate, reviewKeys) || reviewGate.status !== 'SATISFIED_FINAL_DUAL_PASS' || !['REPO_REVIEW_RECORDS', 'UNVERIFIED_FIXTURE_ONLY'].includes(reviewGate.verification_mode) || !hex64(reviewGate.candidate_ref) || !hex64(reviewGate.candidate_manifest_sha256) || reviewGate.gate_path !== RELEASE_FINAL_REVIEW_PATHS.gate || !hex64(reviewGate.gate_sha256)) throw Error('ROUND_RELEASE_REVIEW_PROVENANCE');
  for (const role of ['normal', 'senior']) {
    const reviewer = reviewGate[role];
    if (!exactKeys(reviewer, reviewerKeys) || !uuid(reviewer.agent_id) || reviewer.review_path !== RELEASE_FINAL_REVIEW_PATHS[role] || !hex64(reviewer.review_sha256)) throw Error(`ROUND_RELEASE_${role.toUpperCase()}_REVIEW_PROVENANCE`);
  }
  if (reviewGate.normal.agent_id === reviewGate.senior.agent_id) throw Error('ROUND_RELEASE_REVIEW_ROLE_SEPARATION');
}

function readCanonicalRegular(repo, relativePath, label) {
  const file = path.join(repo, relativePath), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`);
  return decodeCanonicalNoDuplicateKeys(fs.readFileSync(file), label);
}

function enumerateCandidateCoverage(repo, exclusions = RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS) {
  const excluded = new Set(exclusions.map(item => item.path)), roots = ['evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5', releaseTask], files = [];
  const walk = relative => {
    const absolute = path.join(repo, relative), stat = fs.lstatSync(absolute);
    if (stat.isSymbolicLink()) throw Error(`ROUND_RELEASE_CANDIDATE_SYMLINK:${relative}`);
    if (stat.isFile()) { if (!excluded.has(relative)) files.push(relative); return; }
    if (!stat.isDirectory()) throw Error(`ROUND_RELEASE_CANDIDATE_FILE_TYPE:${relative}`);
    for (const name of fs.readdirSync(absolute).sort(textCompare)) walk(`${relative}/${name}`);
  };
  roots.forEach(walk); return files.sort(textCompare);
}

function validateReleaseThreatModelRecord(repo) {
  const record = readCanonicalRegular(repo, RELEASE_THREAT_MODEL_PATH, 'ROUND_RELEASE_THREAT_MODEL');
  const keys = ['schema_version', 'decision_id', 'status', 'authorized_by', 'scope', 'protects_against', 'out_of_scope', 'finding_dispositions', 'review_history_policy', 'claims', 'recorded_at'];
  const expectedFindings = ['V5-RELEASE-R1-SELF-AUTH-001', 'V5-RELEASE-R1-SELF-AUTH-002', 'V5-RELEASE-R1-SELF-AUTH-003', 'PACKAGE_WIDE_COORDINATED_FORGERY_DEMANDS'];
  if (!exactKeys(record.parsed, keys) || record.parsed.schema_version !== 'gemini-context-v5-release-threat-model-clarification-v1' || record.parsed.decision_id !== 'V5-RELEASE-THREAT-MODEL-CLARIFICATION-001' || record.parsed.status !== 'USER_CLARIFIED_CONTROLLING_SCOPE' || record.parsed.authorized_by !== 'user' || record.parsed.scope !== RELEASE_THREAT_MODEL.mode || JSON.stringify(record.parsed.protects_against) !== JSON.stringify(RELEASE_THREAT_MODEL.protects_against) || JSON.stringify(record.parsed.out_of_scope) !== JSON.stringify(RELEASE_THREAT_MODEL.out_of_scope) || !Array.isArray(record.parsed.finding_dispositions) || JSON.stringify(record.parsed.finding_dispositions.map(item => item.finding_id)) !== JSON.stringify(expectedFindings) || record.parsed.finding_dispositions.some(item => !exactKeys(item, ['finding_id', 'disposition']) || item.disposition !== 'OUT_OF_SCOPE_UNDER_USER_CLARIFIED_NON_ADVERSARIAL_THREAT_MODEL') || record.parsed.review_history_policy !== 'PRESERVE_ALL_PRIOR_CHANGES_REQUIRED_AND_PASS_RECORDS_AS_IMMUTABLE_HISTORY' || JSON.stringify(record.parsed.claims) !== JSON.stringify({review_event_authenticity_claimed: false, malicious_tamper_resistance_claimed: false}) || typeof record.parsed.recorded_at !== 'string') throw Error('ROUND_RELEASE_THREAT_MODEL_SCHEMA');
  return {path: RELEASE_THREAT_MODEL_PATH, sha256: sha256(record.bytes)};
}

export function validateReleaseCandidateManifest(repo, expectedCandidateRef = null, expectedManifestSha256 = null, {materializedRelease = null} = {}) {
  const manifest = readCanonicalRegular(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest, 'ROUND_RELEASE_CANDIDATE_MANIFEST');
  if ((expectedCandidateRef !== null && (!hex64(expectedCandidateRef) || manifest.parsed.candidate_ref !== expectedCandidateRef)) || (expectedManifestSha256 !== null && (!hex64(expectedManifestSha256) || sha256(manifest.bytes) !== expectedManifestSha256))) throw Error('ROUND_RELEASE_CANDIDATE_MANIFEST_HASH');
  const keys = ['schema_version', 'status', 'candidate_ref', 'base_candidate_ref', 'author_agent_id', 'round_id', 'threat_model', 'threat_model_record', 'review_history', 'coverage_policy', 'expected_fixture_hashes', 'current_preflight_decision', 'real_materialization', 'recipe', 'exclusions', 'files'];
  const coveragePolicy = {package_root: 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5', task_root: releaseTask, policy: 'ALL_REGULAR_FILES_EXCEPT_EXACT_EXCLUSIONS', reject_unlisted_relevant_files: true, reject_symlinks: true, reject_nonregular_files: true};
  const realMaterialization = {release_created: false, derived_state_mutated: false, round_0002_created: false, model_calls_started: 0, network_calls_made: 0};
  const reviewHistory = {preserve_prior_review_records: true, superseded_findings: ['V5-RELEASE-R1-SELF-AUTH-001', 'V5-RELEASE-R1-SELF-AUTH-002', 'V5-RELEASE-R1-SELF-AUTH-003', 'PACKAGE_WIDE_COORDINATED_FORGERY_DEMANDS'], disposition: 'OUT_OF_SCOPE_UNDER_USER_CLARIFIED_NON_ADVERSARIAL_THREAT_MODEL', aborted_materialization: {candidate_ref: RELEASE_PROVENANCE_BINDING.candidate_ref, candidate_manifest_sha256: RELEASE_PROVENANCE_BINDING.candidate_manifest_sha256, gate_sha256: RELEASE_PROVENANCE_BINDING.gate_sha256, status: 'ABORTED_BEFORE_WRITES_FIXTURE_VS_PRODUCTION_PROVENANCE_HASH_MISMATCH'}};
  const parsed = manifest.parsed;
  const threatModelRecord = validateReleaseThreatModelRecord(repo);
  if (!exactKeys(parsed, keys) || parsed.schema_version !== 'gemini-context-v5-round-release-implementation-candidate-v6' || parsed.status !== 'ROUND_0001_RELEASE_AUTHENTIC_PROVENANCE_HARNESS_REPAIR_PENDING_DUAL_REREVIEW' || !hex64(parsed.candidate_ref) || parsed.base_candidate_ref !== RELEASE_PROVENANCE_BINDING.candidate_ref || parsed.author_agent_id !== 'a75b47e3-1906-4aee-9677-3ac3f278d2b3' || parsed.round_id !== 'ROUND-0001' || JSON.stringify(parsed.threat_model) !== JSON.stringify(RELEASE_THREAT_MODEL) || JSON.stringify(parsed.threat_model_record) !== JSON.stringify(threatModelRecord) || JSON.stringify(parsed.review_history) !== JSON.stringify(reviewHistory) || JSON.stringify(parsed.coverage_policy) !== JSON.stringify(coveragePolicy) || parsed.current_preflight_decision !== 'NO_GO_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED' || JSON.stringify(parsed.real_materialization) !== JSON.stringify(realMaterialization) || parsed.recipe !== RELEASE_IMPLEMENTATION_CANDIDATE_RECIPE || JSON.stringify(parsed.exclusions) !== JSON.stringify(RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS) || JSON.stringify(parsed.expected_fixture_hashes) !== JSON.stringify(RELEASE_EXPECTED_AUTHENTIC_HASHES)) throw Error('ROUND_RELEASE_CANDIDATE_MANIFEST_SCHEMA');
  if (!Array.isArray(parsed.files)) throw Error('ROUND_RELEASE_CANDIDATE_FILES');
  const listed = parsed.files.map((item, index) => {
    if (!exactKeys(item, ['path', 'sha256']) || !hex64(item.sha256) || typeof item.path !== 'string' || path.posix.isAbsolute(item.path) || path.posix.normalize(item.path) !== item.path || item.path.startsWith('../') || item.path.includes('/../') || (!item.path.startsWith(`${coveragePolicy.package_root}/`) && !item.path.startsWith(`${coveragePolicy.task_root}/`))) throw Error(`ROUND_RELEASE_CANDIDATE_ENTRY:${index}`);
    return item.path;
  });
  if (duplicates(listed) || JSON.stringify(listed) !== JSON.stringify([...listed].sort(textCompare))) throw Error('ROUND_RELEASE_CANDIDATE_ORDER');
  const expectedCoverage = enumerateCandidateCoverage(repo);
  const materializedRelative = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0001/RELEASE.json', pendingRelative = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/PENDING-RELEASE.json';
  const materialized = materializedRelease && fs.existsSync(path.join(repo, materializedRelative)) && !fs.existsSync(path.join(repo, pendingRelative));
  if (materialized) {
    const at = expectedCoverage.indexOf(materializedRelative); if (at < 0 || expectedCoverage.includes(pendingRelative)) throw Error('ROUND_RELEASE_CANDIDATE_MATERIALIZED_COVERAGE');
    expectedCoverage.splice(at, 1, pendingRelative); expectedCoverage.sort(textCompare);
  }
  if (JSON.stringify(listed) !== JSON.stringify(expectedCoverage)) throw Error('ROUND_RELEASE_CANDIDATE_COVERAGE');
  const mutableAfterMaterialization = new Set([
    'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/ACTIVE-FRAME.json',
    'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/EXPERIMENT.json',
    'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/LINEAGE.json',
    pendingRelative,
    'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/RELEASE-STATE.json',
    'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/RESERVE-STATE.json',
    'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/ROUND-INDEX.json'
  ]);
  for (const item of parsed.files) {
    if (materialized && mutableAfterMaterialization.has(item.path)) continue;
    const file = path.join(repo, item.path), stat = fs.lstatSync(file);
    if (stat.isSymbolicLink() || !stat.isFile() || sha256(fs.readFileSync(file)) !== item.sha256) throw Error(`ROUND_RELEASE_CANDIDATE_FILE_HASH:${item.path}`);
  }
  if (materialized) {
    const root = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5', expected = parsed.expected_fixture_hashes;
    const postHashes = new Map([
      [`${root}/ACTIVE-FRAME.json`, expected.active_frame_sha256],
      [`${root}/EXPERIMENT.json`, expected.completed_experiment_sha256],
      [`${root}/LINEAGE.json`, expected.lineage_sha256],
      [`${root}/RELEASE-STATE.json`, expected.release_state_sha256],
      [`${root}/RESERVE-STATE.json`, expected.reserve_state_sha256],
      [`${root}/ROUND-INDEX.json`, expected.round_index_sha256]
    ]);
    if (fs.existsSync(path.join(repo, pendingRelative)) || !fs.readFileSync(path.join(repo, materializedRelative)).equals(jsonBytes(materializedRelease))) throw Error('ROUND_RELEASE_CANDIDATE_MATERIALIZED_RELEASE');
    for (const [relative, expectedSha256] of postHashes) {
      const file = path.join(repo, relative), stat = fs.lstatSync(file);
      if (stat.isSymbolicLink() || !stat.isFile() || sha256(fs.readFileSync(file)) !== expectedSha256) throw Error(`ROUND_RELEASE_CANDIDATE_MATERIALIZED_HASH:${relative}`);
    }
  }
  const candidateRoot = sha256(Buffer.from(parsed.files.map(item => `${item.path}\0${item.sha256}\n`).join('')));
  if (candidateRoot !== parsed.candidate_ref) throw Error('ROUND_RELEASE_CANDIDATE_ROOT');
  return {candidate_ref: candidateRoot, manifest_sha256: sha256(manifest.bytes), file_count: parsed.files.length};
}

function validateReleaseAuthorizationRecord(repo, authorization) {
  const file = readCanonicalRegular(repo, RELEASE_AUTHORIZATION_PATH, 'ROUND_RELEASE_AUTHORIZATION');
  const keys = ['schema_version', 'authorization_id', 'status', 'authorized_by', 'round_id', 'executor', 'scout', 'scope', 'required_review_gate', 'permitted_current_decision', 'forbidden_before_review'];
  if (sha256(file.bytes) !== RELEASE_AUTHORIZATION_SHA256 || authorization.authorization_sha256 !== RELEASE_AUTHORIZATION_SHA256 || authorization.authorization_path !== RELEASE_AUTHORIZATION_PATH || !exactKeys(file.parsed, keys) || file.parsed.schema_version !== 'gemini-context-v5-round-release-implementation-authorization-v1' || file.parsed.authorization_id !== authorization.authorization_id || file.parsed.status !== 'AUTHORIZED_IMPLEMENTATION_PENDING_INDEPENDENT_DUAL_REVIEW' || file.parsed.authorized_by !== 'user' || file.parsed.round_id !== 'ROUND-0001' || file.parsed.executor?.role !== 'EXECUTOR' || file.parsed.executor?.agent_id !== authorization.executor_agent_id || file.parsed.scope?.deterministic_rejected_slot_count !== 10 || file.parsed.scope?.round_0002_audit_authorized !== false || file.parsed.scope?.model_calls_authorized !== false || file.parsed.scope?.network_calls_authorized !== false) throw Error('ROUND_RELEASE_AUTHORIZATION_FILE_BINDING');
  return file.parsed;
}

function readReleaseReviewGate(repo, {materializedRelease = null} = {}) {
  const candidate = validateReleaseCandidateManifest(repo, null, null, {materializedRelease});
  const manifestSha256 = candidate.manifest_sha256, reviewRefs = {}, reviewerAgents = [];
  for (const [name, role] of [['normal', 'NORMAL_REVIEWER'], ['senior', 'SENIOR_REVIEWER']]) {
    const review = readCanonicalRegular(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS[name], `ROUND_RELEASE_${name.toUpperCase()}_REVIEW`);
    const keys = ['schema_version', 'review_id', 'round_id', 'role', 'agent_id', 'status', 'candidate_ref', 'candidate_manifest_path', 'candidate_manifest_sha256', 'findings', 'recorded_at'];
    if (!exactKeys(review.parsed, keys) || review.parsed.schema_version !== 'gemini-context-v5-round-release-harness-repair-review-v1' || review.parsed.review_id !== `V5-ROUND-0001-RELEASE-HARNESS-REPAIR-${name.toUpperCase()}-REVIEW-001` || review.parsed.round_id !== 'ROUND-0001' || review.parsed.role !== role || !uuid(review.parsed.agent_id) || review.parsed.status !== 'PASS' || review.parsed.candidate_ref !== candidate.candidate_ref || review.parsed.candidate_manifest_path !== RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest || review.parsed.candidate_manifest_sha256 !== manifestSha256 || !Array.isArray(review.parsed.findings) || review.parsed.findings.length !== 0 || typeof review.parsed.recorded_at !== 'string') throw Error(`ROUND_RELEASE_${name.toUpperCase()}_REVIEW_SCHEMA`);
    reviewerAgents.push(review.parsed.agent_id);
    reviewRefs[name] = {path: RELEASE_MATERIALIZATION_REVIEW_PATHS[name], sha256: sha256(review.bytes), agent_id: review.parsed.agent_id, role, status: 'PASS'};
  }
  if (reviewerAgents[0] === reviewerAgents[1]) throw Error('ROUND_RELEASE_REVIEW_ROLE_SEPARATION');
  const gate = readCanonicalRegular(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS.gate, 'ROUND_RELEASE_REVIEW_GATE');
  const keys = ['schema_version', 'gate_id', 'round_id', 'status', 'candidate_ref', 'candidate_manifest_path', 'candidate_manifest_sha256', 'authorization', 'threat_model', 'normal_review', 'senior_review', 'permitted_action', 'forbidden_scope', 'recorded_at'];
  const authorization = {path: RELEASE_AUTHORIZATION_PATH, sha256: RELEASE_AUTHORIZATION_SHA256, authorization_id: 'V5-ROUND-0001-REPLACEMENT-RELEASE-IMPLEMENTATION-001'};
  const threatModelRecord = validateReleaseThreatModelRecord(repo);
  const threatModel = {record_path: threatModelRecord.path, record_sha256: threatModelRecord.sha256, mode: RELEASE_THREAT_MODEL.mode};
  const forbiddenScope = ['ROUND-0002_AUDIT', 'MODEL_CALL', 'NETWORK_CALL', 'QUALIFICATION', 'MUTATION', 'REFERENCE_DISCLOSURE', 'GIT_STAGE', 'GIT_HISTORY'];
  if (!exactKeys(gate.parsed, keys) || gate.parsed.schema_version !== 'gemini-context-v5-round-release-harness-repair-review-gate-v1' || gate.parsed.gate_id !== 'V5-ROUND-0001-RELEASE-HARNESS-REPAIR-DUAL-REREVIEW-GATE-001' || gate.parsed.round_id !== 'ROUND-0001' || gate.parsed.status !== 'SATISFIED_FINAL_DUAL_PASS' || gate.parsed.candidate_ref !== candidate.candidate_ref || gate.parsed.candidate_manifest_path !== RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest || gate.parsed.candidate_manifest_sha256 !== manifestSha256 || JSON.stringify(gate.parsed.authorization) !== JSON.stringify(authorization) || JSON.stringify(gate.parsed.threat_model) !== JSON.stringify(threatModel) || JSON.stringify(gate.parsed.normal_review) !== JSON.stringify(reviewRefs.normal) || JSON.stringify(gate.parsed.senior_review) !== JSON.stringify(reviewRefs.senior) || gate.parsed.permitted_action !== 'GO_ROUND_0001_RELEASE_MATERIALIZATION_ONLY' || JSON.stringify(gate.parsed.forbidden_scope) !== JSON.stringify(forbiddenScope) || typeof gate.parsed.recorded_at !== 'string') throw Error('ROUND_RELEASE_REVIEW_GATE_SCHEMA');
  return {
    status: 'SATISFIED_FINAL_DUAL_PASS',
    verification_mode: 'REPO_REVIEW_RECORDS',
    candidate_ref: candidate.candidate_ref,
    candidate_manifest_sha256: manifestSha256,
    normal: {agent_id: reviewRefs.normal.agent_id, review_path: reviewRefs.normal.path, review_sha256: reviewRefs.normal.sha256},
    senior: {agent_id: reviewRefs.senior.agent_id, review_path: reviewRefs.senior.path, review_sha256: reviewRefs.senior.sha256},
    gate_path: RELEASE_MATERIALIZATION_REVIEW_PATHS.gate,
    gate_sha256: sha256(gate.bytes)
  };
}

export function evaluateReleaseImplementationReviewGate(repo, {materializedRelease = null} = {}) {
  if (typeof repo !== 'string' || !path.isAbsolute(repo)) return {satisfied: false, invalid: true, reason: 'ROUND_RELEASE_REVIEW_REPO'};
  let candidate;
  try { candidate = validateReleaseCandidateManifest(repo, null, null, {materializedRelease}); }
  catch (error) { return {satisfied: false, invalid: true, reason: error.code === 'ENOENT' ? 'RELEASE_CANDIDATE_MISSING' : error.message}; }
  const paths = [RELEASE_MATERIALIZATION_REVIEW_PATHS.normal, RELEASE_MATERIALIZATION_REVIEW_PATHS.senior, RELEASE_MATERIALIZATION_REVIEW_PATHS.gate];
  const present = paths.filter(relative => fs.existsSync(path.join(repo, relative)));
  if (present.length === 0) return {satisfied: false, invalid: false, reason: 'NORMAL_SENIOR_AND_COMBINED_REVIEW_REQUIRED', candidate_ref: candidate.candidate_ref, candidate_manifest_sha256: candidate.manifest_sha256};
  if (present.length !== paths.length) return {satisfied: false, invalid: true, reason: 'RELEASE_REVIEW_RECORD_SET_PARTIAL', candidate_ref: candidate.candidate_ref, candidate_manifest_sha256: candidate.manifest_sha256};
  try {
    const provenance = readReleaseReviewGate(repo, {materializedRelease});
    return {satisfied: true, invalid: false, reason: null, provenance};
  } catch (error) {
    return {satisfied: false, invalid: true, reason: error.code === 'ENOENT' ? 'RELEASE_REVIEW_FILE_MISSING' : error.message, candidate_ref: candidate.candidate_ref, candidate_manifest_sha256: candidate.manifest_sha256};
  }
}

export function readReleaseProvenanceReviewGate(repo) {
  if (typeof repo !== 'string' || !path.isAbsolute(repo)) throw Error('ROUND_RELEASE_PROVENANCE_REPO');
  const expected = [
    [RELEASE_FINAL_REVIEW_PATHS.manifest, RELEASE_PROVENANCE_BINDING.candidate_manifest_sha256, 'ROUND_RELEASE_PROVENANCE_MANIFEST'],
    [RELEASE_FINAL_REVIEW_PATHS.normal, RELEASE_PROVENANCE_BINDING.normal_review_sha256, 'ROUND_RELEASE_PROVENANCE_NORMAL'],
    [RELEASE_FINAL_REVIEW_PATHS.senior, RELEASE_PROVENANCE_BINDING.senior_review_sha256, 'ROUND_RELEASE_PROVENANCE_SENIOR'],
    [RELEASE_FINAL_REVIEW_PATHS.gate, RELEASE_PROVENANCE_BINDING.gate_sha256, 'ROUND_RELEASE_PROVENANCE_GATE']
  ];
  const records = Object.fromEntries(expected.map(([relative, expectedSha256, label]) => {
    const record = readCanonicalRegular(repo, relative, label);
    if (sha256(record.bytes) !== expectedSha256) throw Error(`${label}_HASH`);
    return [relative, record];
  }));
  const manifest = records[RELEASE_FINAL_REVIEW_PATHS.manifest].parsed, normal = records[RELEASE_FINAL_REVIEW_PATHS.normal].parsed, senior = records[RELEASE_FINAL_REVIEW_PATHS.senior].parsed, gate = records[RELEASE_FINAL_REVIEW_PATHS.gate].parsed;
  if (manifest.candidate_ref !== RELEASE_PROVENANCE_BINDING.candidate_ref || normal.status !== 'PASS' || senior.status !== 'PASS' || normal.candidate_ref !== RELEASE_PROVENANCE_BINDING.candidate_ref || senior.candidate_ref !== RELEASE_PROVENANCE_BINDING.candidate_ref || gate.status !== 'SATISFIED_FINAL_DUAL_PASS' || gate.candidate_ref !== RELEASE_PROVENANCE_BINDING.candidate_ref || gate.normal_review?.sha256 !== RELEASE_PROVENANCE_BINDING.normal_review_sha256 || gate.senior_review?.sha256 !== RELEASE_PROVENANCE_BINDING.senior_review_sha256) throw Error('ROUND_RELEASE_PROVENANCE_CONTENT');
  const provenance = {
    status: 'SATISFIED_FINAL_DUAL_PASS',
    verification_mode: 'REPO_REVIEW_RECORDS',
    candidate_ref: RELEASE_PROVENANCE_BINDING.candidate_ref,
    candidate_manifest_sha256: RELEASE_PROVENANCE_BINDING.candidate_manifest_sha256,
    normal: {agent_id: normal.agent_id, review_path: RELEASE_FINAL_REVIEW_PATHS.normal, review_sha256: RELEASE_PROVENANCE_BINDING.normal_review_sha256},
    senior: {agent_id: senior.agent_id, review_path: RELEASE_FINAL_REVIEW_PATHS.senior, review_sha256: RELEASE_PROVENANCE_BINDING.senior_review_sha256},
    gate_path: RELEASE_FINAL_REVIEW_PATHS.gate,
    gate_sha256: RELEASE_PROVENANCE_BINDING.gate_sha256
  };
  assertReleaseProvenance({authorization_id: 'V5-ROUND-0001-REPLACEMENT-RELEASE-IMPLEMENTATION-001', authorization_path: RELEASE_AUTHORIZATION_PATH, authorization_sha256: RELEASE_AUTHORIZATION_SHA256, authorized_by: 'user', executor_agent_id: 'f5cc0aa8-b313-4ca7-8f92-191041de73a8'}, provenance);
  return provenance;
}

export function validateReleaseReviewGate(repo, provenance) {
  if (arguments.length !== 2) throw Error('ROUND_RELEASE_REVIEW_ARGUMENTS');
  if (typeof repo !== 'string' || !path.isAbsolute(repo)) throw Error('ROUND_RELEASE_REVIEW_REPO');
  const authorization = provenance?.release_authorization, embedded = provenance?.implementation_review_gate, release = provenance?.release;
  assertReleaseProvenance(authorization, embedded);
  if (embedded.verification_mode !== 'REPO_REVIEW_RECORDS') throw Error('ROUND_RELEASE_REVIEW_FIXTURE_ONLY');
  validateReleaseAuthorizationRecord(repo, authorization);
  const local = readReleaseProvenanceReviewGate(repo);
  if (JSON.stringify(local) !== JSON.stringify(embedded)) throw Error('ROUND_RELEASE_REVIEW_RECORD_DRIFT');
  if (release?.schema_version !== 'gemini-context-v5-round-release-v3' || release?.round_id !== 'ROUND-0001' || release?.predecessor_release_sha256 !== null) throw Error('ROUND_RELEASE_REVIEW_RELEASE_SCOPE');
  return {status: 'PASS', candidate_ref: embedded.candidate_ref, candidate_manifest_sha256: embedded.candidate_manifest_sha256, gate_sha256: embedded.gate_sha256};
}

function lineageDocument(state) { return {schema_version: 'gemini-context-v5-slot-lineage-v1', initial_frame_sha256: state.initialFrameSha256, last_completed_round: state.round, items: state.active.map(row => state.lineage.get(row.neutral_id))}; }
function reserveDocument(state) {
  const unavailableIds = [...unavailable(state)].sort(textCompare), consumed = [...state.consumed].sort(textCompare), banned = [...state.banned].sort(textCompare);
  return {schema_version: 'gemini-context-v5-reserve-state-v1', initial_reserve_rows: state.reserves.length, initial_narrative_reserve_rows: state.reserves.filter(row => row.profile === 'narrative').length, consumed_revision_ids: consumed, banned_revision_ids: banned, unavailable_reserve_revision_ids: unavailableIds, remaining_reserve_rows: state.reserves.length - unavailableIds.length, remaining_narrative_reserve_rows: state.reserves.filter(row => row.profile === 'narrative' && !unavailable(state).has(row.revision_id)).length, accounting: 'remaining = initial reserve minus cardinality(union(consumed reserve revisions, banned reserve revisions)); overlapping sets are subtracted once'};
}
function roundIndexDocument(state) { return {schema_version: 'gemini-context-v5-round-index-v1', completed_rounds: state.round, last_release_sha256: state.lastReleaseSha256, rounds: state.roundIndex}; }
function transitionProjection(state) { return {round: state.round, active: state.active, lineage: lineageDocument(state).items, consumed_revision_ids: [...state.consumed].sort(textCompare), banned_revision_ids: [...state.banned].sort(textCompare)}; }
function stateHashes(state, includeRoundIndex = true) { return {active_frame_sha256: sha256(jsonBytes(activeFrameDocument(state))), lineage_sha256: sha256(jsonBytes(lineageDocument(state))), reserve_state_sha256: sha256(jsonBytes(reserveDocument(state))), ...(includeRoundIndex ? {round_index_sha256: sha256(jsonBytes(roundIndexDocument(state)))} : {})}; }

function applyResolutions(state, resolution, roundId) {
  const rejected = state.active.filter(row => resolution.has(row.neutral_id));
  for (const row of rejected) state.banned.add(row.revision_id);
  const active = state.active.filter(row => !resolution.has(row.neutral_id)), blocked = unavailable(state), replacements = new Map(), decisions = [];
  for (const rejectedRow of rejected) {
    const skipped = []; let chosen = null;
    for (const candidate of state.reserves) {
      if (candidate.profile !== rejectedRow.profile || blocked.has(candidate.revision_id)) continue;
      const reason = skipReason(candidate, active) ?? cohortCapReason(candidate, rejectedRow.cohort, active);
      if (reason) { skipped.push({reserve_rank: candidate.reserve_rank, revision_id: candidate.revision_id, reason}); continue; }
      chosen = candidate; break;
    }
    if (!chosen) throw Error(`RESERVE_EXHAUSTED:${rejectedRow.neutral_id}:${rejectedRow.profile}:${rejectedRow.cohort}`);
    blocked.add(chosen.revision_id); state.consumed.add(chosen.revision_id);
    const replacement = Object.fromEntries(rowKeys.map(key => [key, key === 'neutral_id' ? rejectedRow.neutral_id : key === 'cohort' ? rejectedRow.cohort : chosen[key]]));
    active.push(replacement); replacements.set(rejectedRow.neutral_id, replacement);
    const evidence = resolution.get(rejectedRow.neutral_id), chain = state.lineage.get(rejectedRow.neutral_id), previous = chain.revisions.at(-1);
    if (previous !== rejectedRow.revision_id) throw Error(`LINEAGE_HEAD_MISMATCH:${rejectedRow.neutral_id}`);
    const reasonClass = evidence.verdict === 'OUT_OF_SCOPE_NON_PROSE' ? 'OUT_OF_SCOPE_NON_PROSE' : 'DIRECT_AUDIT_REJECTION';
    chain.revisions.push(replacement.revision_id);
    chain.edges.push({edge_ordinal: chain.edges.length + 1, round_id: roundId, stage: evidence.stage.toUpperCase(), reason_class: reasonClass, verdict: evidence.verdict, rejected_revision_id: rejectedRow.revision_id, replacement_revision_id: replacement.revision_id, reserve_rank: chosen.reserve_rank, queue_sha256: evidence.queue_sha256, aggregate_sha256: evidence.aggregate_sha256, skipped_incompatible_reserves: skipped});
    decisions.push({neutral_id: rejectedRow.neutral_id, stage: evidence.stage.toUpperCase(), verdict: evidence.verdict, reason_class: reasonClass, rejected_revision_id: rejectedRow.revision_id, replacement_revision_id: replacement.revision_id, reserve_rank: chosen.reserve_rank, skipped_incompatible_reserves: skipped});
  }
  state.active = state.active.map(row => replacements.get(row.neutral_id) ?? row);
  assertActiveFrame(state.active);
  return decisions;
}

function buildReleaseV3BytesInternal(state, bundle, unverifiedFixture, provenanceOnly = false) {
  assertReleaseProvenance(bundle.release_authorization, bundle.implementation_review_gate);
  if (unverifiedFixture) {
    if (bundle.review_repo || bundle.repo !== false || bundle.implementation_review_gate.verification_mode !== 'UNVERIFIED_FIXTURE_ONLY') throw Error('ROUND_RELEASE_UNVERIFIED_FIXTURE_BOUNDARY');
  } else {
    if (typeof bundle.review_repo !== 'string' || !path.isAbsolute(bundle.review_repo) || bundle.implementation_review_gate.verification_mode !== 'REPO_REVIEW_RECORDS') throw Error('ROUND_RELEASE_REVIEW_REPO_REQUIRED');
    const releaseProvenance = readReleaseProvenanceReviewGate(bundle.review_repo);
    if (JSON.stringify(releaseProvenance) !== JSON.stringify(bundle.implementation_review_gate)) throw Error('ROUND_RELEASE_PROVENANCE_DRIFT');
    if (!provenanceOnly) {
      const materializedRelease = bundle.release ? decodeCanonical(bundle.release, 'ROUND_RELEASE').parsed : null;
      const materializationReview = evaluateReleaseImplementationReviewGate(bundle.review_repo, {materializedRelease});
      if (!materializationReview.satisfied) throw Error(`ROUND_RELEASE_MATERIALIZATION_REVIEW_REQUIRED:${materializationReview.reason}`);
    }
  }
  const surface = validateStage('surface', bundle.surface_queue, bundle.surface_records, bundle.surface_aggregate, state, null, null, bundle.surface_queue_view, normalizeRepoOption(bundle.repo));
  const passIds = surface.aggregate.parsed.pass_ids, passItems = surface.queue.parsed.items.filter(item => passIds.includes(item.neutral_id));
  if (!passItems.length || !bundle.context_queue || !bundle.context_source_anchors || !bundle.context_queue_view || !bundle.context_records || !bundle.context_aggregate) throw Error('RELEASE_V3_EXACT_NINE_REQUIRED');
  validateFrozenContextInputBytes({surfaceQueueBytes: surface.queue.bytes, surfaceViewBytes: surface.queueView.bytes, surfaceRecordsBytes: surface.records.bytes, surfaceAggregateBytes: surface.aggregate.bytes, activeFrameBytes: jsonBytes(activeFrameDocument(state)), queueBytes: bundle.context_queue, anchorsBytes: bundle.context_source_anchors, viewBytes: bundle.context_queue_view});
  const context = validateStage('context', bundle.context_queue, bundle.context_records, bundle.context_aggregate, state, passItems, sha256(surface.aggregate.bytes), null, null, {surfaceQueueBytes: surface.queue.bytes, surfaceQueueViewBytes: surface.queueView.bytes, surfaceRecordsBytes: surface.records.bytes, contextSourceAnchorsBytes: bundle.context_source_anchors, contextQueueViewBytes: bundle.context_queue_view});
  if (!context.contextV2) throw Error('RELEASE_V3_CONTEXT_V2_REQUIRED');
  const resolution = new Map();
  surface.aggregate.parsed.items.forEach(item => { if (item.verdict !== 'PASS_SURFACE') resolution.set(item.neutral_id, {stage: 'surface', verdict: item.verdict, queue_sha256: sha256(surface.queue.bytes), aggregate_sha256: sha256(surface.aggregate.bytes)}); });
  context.aggregate.parsed.items.forEach(item => { if (item.verdict === 'NOT_CLEAN') resolution.set(item.neutral_id, {stage: 'context', verdict: item.verdict, queue_sha256: sha256(context.queue.bytes), aggregate_sha256: sha256(context.aggregate.bytes)}); });
  const preview = cloneState(state), decisions = applyResolutions(preview, resolution, surface.queue.parsed.round_id); preview.round += 1;
  const artifactSha256 = {'SURFACE-QUEUE.json': sha256(surface.queue.bytes), 'SURFACE-QUEUE-VIEW.json': sha256(surface.queueView.bytes), 'SURFACE-RECORDS.json': sha256(surface.records.bytes), 'SURFACE-AGGREGATE.json': sha256(surface.aggregate.bytes), 'CONTEXT-QUEUE.json': sha256(context.queue.bytes), 'CONTEXT-SOURCE-ANCHORS.json': sha256(bundle.context_source_anchors), 'CONTEXT-QUEUE-VIEW.json': sha256(bundle.context_queue_view), 'CONTEXT-RECORDS.json': sha256(context.records.bytes), 'CONTEXT-AGGREGATE.json': sha256(context.aggregate.bytes)};
  const auditAccounting = {authorized_surface_auditor_calls_started: 2, invalid_auditor_input_attempts: 1, valid_surface_auditor_responses: 1, valid_persisted_surface_results: 1, authorized_context_auditor_calls_started: 1, valid_context_auditor_responses: 1, valid_persisted_context_results: 1, surface_rejected_slot_count: decisions.filter(item => item.stage === 'SURFACE').length, context_rejected_slot_count: decisions.filter(item => item.stage === 'CONTEXT').length, formal_gemini_experiment_inference_calls_made: 0, network_calls_made: 0};
  const releaseDocument = {schema_version: 'gemini-context-v5-round-release-v3', round_id: surface.queue.parsed.round_id, predecessor_release_sha256: state.lastReleaseSha256, release_authorization: bundle.release_authorization, implementation_review_gate: bundle.implementation_review_gate, audit_accounting: auditAccounting, artifact_sha256: artifactSha256, before_state_sha256: sha256(jsonBytes(transitionProjection(state))), before_state_hashes: stateHashes(state), after_state_sha256: sha256(jsonBytes(transitionProjection(preview))), after_state_hashes: stateHashes(preview, false), decisions};
  if (!unverifiedFixture) validateReleaseReviewGate(bundle.review_repo, {release_authorization: bundle.release_authorization, implementation_review_gate: bundle.implementation_review_gate, release: releaseDocument});
  return jsonBytes(releaseDocument);
}

export function buildReleaseV3Bytes(state, bundle) { if (arguments.length !== 2) throw Error('ROUND_RELEASE_BUILD_ARGUMENTS'); return buildReleaseV3BytesInternal(state, bundle, false); }
export function buildReviewedProvenanceReleaseV3Bytes(state, bundle) { if (arguments.length !== 2) throw Error('ROUND_RELEASE_BUILD_ARGUMENTS'); return buildReleaseV3BytesInternal(state, bundle, false, true); }
export function buildUnverifiedReleaseV3FixtureBytes(state, bundle) { return buildReleaseV3BytesInternal(state, bundle, true); }

function applyRoundInternal(state, bundle, unverifiedFixture, provenanceOnly = false) {
  const surface = validateStage('surface', bundle.surface_queue, bundle.surface_records, bundle.surface_aggregate, state, null, null, bundle.surface_queue_view, normalizeRepoOption(bundle.repo));
  const passIds = surface.aggregate.parsed.pass_ids ?? surface.aggregate.parsed.accepted_ids;
  const passItems = surface.queue.parsed.items.filter(item => passIds.includes(item.neutral_id));
  let context = null;
  if (passItems.length) {
    if (!bundle.context_queue || !bundle.context_records || !bundle.context_aggregate) throw Error('CONTEXT_REQUIRED_FOR_SURFACE_PASS');
    const contextSchema = JSON.parse(bundle.context_queue).schema_version;
    const contextV2 = contextSchema === 'gemini-context-v5-context-queue-v2';
    const contextV3 = contextSchema === 'gemini-context-v5-round-0002-context-queue-v3';
    if (contextV2) {
      if (!bundle.context_source_anchors || !bundle.context_queue_view) throw Error('CONTEXT_V2_SIDECARS_REQUIRED');
      validateFrozenContextInputBytes({surfaceQueueBytes: surface.queue.bytes, surfaceViewBytes: surface.queueView.bytes, surfaceRecordsBytes: surface.records.bytes, surfaceAggregateBytes: surface.aggregate.bytes, activeFrameBytes: jsonBytes(activeFrameDocument(state)), queueBytes: bundle.context_queue, anchorsBytes: bundle.context_source_anchors, viewBytes: bundle.context_queue_view});
    }
    if (contextV3 && (!bundle.context_source_anchors || !bundle.context_queue_view)) throw Error('CONTEXT_V3_SIDECARS_REQUIRED');
    context = validateStage('context', bundle.context_queue, bundle.context_records, bundle.context_aggregate, state, passItems, sha256(surface.aggregate.bytes), null, null, contextV2 || contextV3 ? {surfaceQueueBytes: surface.queue.bytes, surfaceQueueViewBytes: surface.queueView.bytes, surfaceRecordsBytes: surface.records.bytes, contextSourceAnchorsBytes: bundle.context_source_anchors, contextQueueViewBytes: bundle.context_queue_view} : null);
  } else if (bundle.context_queue || bundle.context_source_anchors || bundle.context_queue_view || bundle.context_records || bundle.context_aggregate) throw Error('UNEXPECTED_CONTEXT_STAGE');
  const release = decodeCanonical(bundle.release, 'ROUND_RELEASE');
  const viewBound = surface.queueView !== null;
  const resolution = new Map();
  surface.aggregate.parsed.items.forEach(item => { if (item.verdict !== 'PASS_SURFACE') resolution.set(item.neutral_id, {stage: 'surface', verdict: item.verdict, queue_sha256: sha256(surface.queue.bytes), aggregate_sha256: sha256(surface.aggregate.bytes)}); });
  context?.aggregate.parsed.items.forEach(item => { if (item.verdict === 'NOT_CLEAN') resolution.set(item.neutral_id, {stage: 'context', verdict: item.verdict, queue_sha256: sha256(context.queue.bytes), aggregate_sha256: sha256(context.aggregate.bytes)}); });
  const preview = cloneState(state), decisions = applyResolutions(preview, resolution, surface.queue.parsed.round_id); preview.round += 1;
  const exactNine = context?.contextV2 === true;
  const round2V4 = context?.contextV3 === true && release.parsed.schema_version === 'gemini-context-v5-round-release-v4';
  if (round2V4) {
    const stripped = ROUND2_DECISIONS.map(({profile, public_source_file, ...item}) => item);
    if (JSON.stringify(decisions) !== JSON.stringify(stripped)) throw Error('ROUND2_RELEASE_DECISIONS_DERIVATION');
    const artifactSha256 = {...ROUND2_AUDIT_ARTIFACTS};
    const bound = {'SURFACE-QUEUE.json': surface.queue.bytes, 'SURFACE-QUEUE-VIEW.json': surface.queueView.bytes, 'SURFACE-RECORDS.json': surface.records.bytes, 'SURFACE-AGGREGATE.json': surface.aggregate.bytes, 'CONTEXT-QUEUE.json': context.queue.bytes, 'CONTEXT-SOURCE-ANCHORS.json': bundle.context_source_anchors, 'CONTEXT-QUEUE-VIEW.json': bundle.context_queue_view, 'CONTEXT-RECORDS.json': context.records.bytes, 'CONTEXT-AGGREGATE.json': context.aggregate.bytes};
    for (const [name, bytes] of Object.entries(bound)) if (sha256(bytes) !== artifactSha256[name]) throw Error(`ROUND2_RELEASE_ARTIFACT_BINDING:${name}`);
    const beforeState = {completed_rounds: state.round, active_frame_sha256: sha256(jsonBytes(activeFrameDocument(state))), lineage_sha256: sha256(jsonBytes(lineageDocument(state))), reserve_state_sha256: sha256(jsonBytes(reserveDocument(state))), predecessor_release_sha256: state.lastReleaseSha256};
    const previewReserve = reserveDocument(preview);
    const afterState = {completed_rounds: preview.round, active_frame_sha256: sha256(jsonBytes(activeFrameDocument(preview))), lineage_sha256: sha256(jsonBytes(lineageDocument(preview))), reserve_state_sha256: sha256(jsonBytes(previewReserve)), active_rows: preview.active.length, lineage_edges: [...preview.lineage.values()].reduce((sum, item) => sum + item.edges.length, 0), remaining_reserve_rows: previewReserve.remaining_reserve_rows, remaining_dialogue_reserve_rows: previewReserve.remaining_reserve_rows - previewReserve.remaining_narrative_reserve_rows, remaining_narrative_reserve_rows: previewReserve.remaining_narrative_reserve_rows, banned_revision_ids: preview.banned.size, consumed_revision_ids: preview.consumed.size};
    const expectedRelease = {schema_version: 'gemini-context-v5-round-release-v4', round_id: 'ROUND-0002', predecessor_release_sha256: ROUND2_PREDECESSOR, release_authorization: ROUND2_RELEASE_AUTHORIZATION, immutable_audit_provenance: {artifact_sha256: artifactSha256, surface_reject_ids: ['V4-C-D06'], context_reject_ids: ['V4-D-D05'], replacement_eligibility: {OUT_OF_SCOPE_NON_PROSE: true}}, materialization_review_policy: {mode: 'EXTERNAL_NON_CIRCULAR_GATE', candidate_manifest_path: ROUND2_RELEASE_PATHS.manifest, normal_review_path: ROUND2_RELEASE_PATHS.normal, senior_review_path: ROUND2_RELEASE_PATHS.senior, combined_gate_path: ROUND2_RELEASE_PATHS.gate, review_hashes_embedded_in_release: false}, before_state: beforeState, after_state: afterState, decisions: ROUND2_DECISIONS};
    if (!release.bytes.equals(jsonBytes(expectedRelease)) || beforeState.active_frame_sha256 !== ROUND2_PRE_HASHES.active_frame_sha256 || afterState.active_frame_sha256 !== ROUND2_EXPECTED_CORE_HASHES.active_frame_sha256 || afterState.lineage_sha256 !== ROUND2_EXPECTED_CORE_HASHES.lineage_sha256 || afterState.reserve_state_sha256 !== ROUND2_EXPECTED_CORE_HASHES.reserve_state_sha256) throw Error('ROUND2_RELEASE_V4_BINDING');
  } else if (exactNine) {
    const releaseBundle = {...bundle, release_authorization: bundle.release_authorization ?? release.parsed.release_authorization, implementation_review_gate: bundle.implementation_review_gate ?? release.parsed.implementation_review_gate};
    const expectedRelease = unverifiedFixture ? buildUnverifiedReleaseV3FixtureBytes(state, releaseBundle) : provenanceOnly ? buildReviewedProvenanceReleaseV3Bytes(state, releaseBundle) : buildReleaseV3Bytes(state, releaseBundle);
    if (!release.bytes.equals(expectedRelease)) throw Error('ROUND_RELEASE_BINDING');
    if (!unverifiedFixture) validateReleaseReviewGate(bundle.review_repo, {release_authorization: release.parsed.release_authorization, implementation_review_gate: release.parsed.implementation_review_gate, release: release.parsed});
  } else {
    const releaseKeys = ['schema_version', 'round_id', 'predecessor_release_sha256', 'surface_queue_sha256', ...(viewBound ? ['surface_queue_view_sha256'] : []), 'surface_records_sha256', 'surface_aggregate_sha256', 'context_queue_sha256', 'context_records_sha256', 'context_aggregate_sha256'];
    const releaseSchema = viewBound ? 'gemini-context-v5-round-release-v2' : 'gemini-context-v5-round-release-v1';
    if (!exactKeys(release.parsed, releaseKeys) || release.parsed.schema_version !== releaseSchema || release.parsed.round_id !== surface.queue.parsed.round_id || release.parsed.predecessor_release_sha256 !== state.lastReleaseSha256 || release.parsed.surface_queue_sha256 !== sha256(surface.queue.bytes) || (viewBound && release.parsed.surface_queue_view_sha256 !== sha256(surface.queueView.bytes)) || release.parsed.surface_records_sha256 !== sha256(surface.records.bytes) || release.parsed.surface_aggregate_sha256 !== sha256(surface.aggregate.bytes) || release.parsed.context_queue_sha256 !== (context ? sha256(context.queue.bytes) : null) || release.parsed.context_records_sha256 !== (context ? sha256(context.records.bytes) : null) || release.parsed.context_aggregate_sha256 !== (context ? sha256(context.aggregate.bytes) : null)) throw Error('ROUND_RELEASE_BINDING');
  }
  const appliedDecisions = applyResolutions(state, resolution, release.parsed.round_id);
  if (JSON.stringify(appliedDecisions) !== JSON.stringify(decisions)) throw Error('ROUND_RELEASE_DECISION_REPLAY_DRIFT');
  state.round += 1; state.lastReleaseSha256 = sha256(release.bytes);
  if (round2V4) state.completedRelease = {round_id: release.parsed.round_id, release_sha256: state.lastReleaseSha256, predecessor_release_sha256: release.parsed.predecessor_release_sha256, release_authorization: release.parsed.release_authorization, immutable_audit_provenance: release.parsed.immutable_audit_provenance, materialization_review_policy: release.parsed.materialization_review_policy, decisions: release.parsed.decisions};
  else if (exactNine) state.completedRelease = {round_id: release.parsed.round_id, release_sha256: state.lastReleaseSha256, predecessor_release_sha256: release.parsed.predecessor_release_sha256, release_authorization: release.parsed.release_authorization, implementation_review_gate: release.parsed.implementation_review_gate, audit_accounting: release.parsed.audit_accounting};
  state.roundIndex.push({round_id: release.parsed.round_id, release_sha256: state.lastReleaseSha256, surface_queue_sha256: sha256(surface.queue.bytes), ...(viewBound ? {surface_queue_view_sha256: sha256(surface.queueView.bytes)} : {}), surface_aggregate_sha256: sha256(surface.aggregate.bytes), context_queue_sha256: context ? sha256(context.queue.bytes) : null, ...((exactNine || round2V4) ? {context_source_anchors_sha256: sha256(bundle.context_source_anchors), context_queue_view_sha256: sha256(bundle.context_queue_view)} : {}), context_aggregate_sha256: context ? sha256(context.aggregate.bytes) : null});
  assertActiveFrame(state.active);
  return state;
}

export function applyRound(state, bundle) { if (arguments.length !== 2) throw Error('ROUND_RELEASE_APPLY_ARGUMENTS'); return applyRoundInternal(state, bundle, false); }
export function applyReviewedProvenanceRound(state, bundle) { if (arguments.length !== 2) throw Error('ROUND_RELEASE_APPLY_ARGUMENTS'); return applyRoundInternal(state, bundle, false, true); }
export function applyUnverifiedRoundFixture(state, bundle) { return applyRoundInternal(state, bundle, true); }

export function makeRound(state, decisions, {surfaceV2 = null, repo = null} = {}) {
  if (!Array.isArray(decisions) || !decisions.length) throw Error('DECISIONS_REQUIRED');
  const bySlot = new Map(state.active.map(row => [row.neutral_id, row]));
  const ids = decisions.map(item => item.neutral_id); if (duplicates(ids)) throw Error('DECISION_DUPLICATE_SLOT');
  const roundId = `ROUND-${String(state.round + 1).padStart(4, '0')}`;
  const base = {round_id: roundId, active_frame_sha256: activeFrameSha256(state), predecessor_release_sha256: state.lastReleaseSha256};
  if (surfaceV2 && JSON.stringify(decisions.map(item => item.neutral_id)) !== JSON.stringify(state.active.map(row => row.neutral_id))) throw Error('V2_SURFACE_QUEUE_MUST_COVER_ACTIVE_FRAME_IN_ORDER');
  const surfaceItems = decisions.map(item => { const row = bySlot.get(item.neutral_id); if (!row) throw Error(`DECISION_UNKNOWN_SLOT:${item.neutral_id}`); return queueItem(row); });
  const surfaceQueueDoc = surfaceV2
    ? {schema_version: 'gemini-context-v5-surface-queue-v2', ...base, stage: 'SURFACE', authorization_id: surfaceV2.authorization_id, authorization_record_sha256: surfaceV2.authorization_record_sha256, authorized_candidate_ref: surfaceV2.authorized_candidate_ref, final_pass_reviewer_agent_ids: surfaceV2.final_pass_reviewer_agent_ids, items: surfaceItems}
    : {schema_version: 'gemini-context-v5-surface-queue-v1', ...base, stage: 'SURFACE', items: surfaceItems};
  const surfaceQueue = jsonBytes(surfaceQueueDoc);
  const normalizedRepo = normalizeRepoOption(repo);
  const surfaceQueueView = surfaceV2 ? jsonBytes(buildSurfaceQueueView({repo: normalizedRepo, queueBytes: surfaceQueue, activeFrameBytes: jsonBytes(activeFrameDocument(state))})) : null;
  const surfaceRecordItems = decisions.map(item => ({neutral_id: item.neutral_id, verdict: item.surface_verdict, evidence: item.surface_evidence ?? 'fixture evidence'}));
  const surfaceRecordsDoc = surfaceV2
    ? {schema_version: 'gemini-context-v5-surface-records-v2', round_id: roundId, stage: 'SURFACE', surface_queue_sha256: sha256(surfaceQueue), surface_queue_view_sha256: sha256(surfaceQueueView), items: surfaceRecordItems}
    : {schema_version: 'gemini-context-v5-surface-records-v1', round_id: roundId, stage: 'SURFACE', items: surfaceRecordItems};
  const surfaceRecords = jsonBytes(surfaceRecordsDoc), surfaceAggregate = jsonBytes(aggregateDocument('surface', surfaceQueue, surfaceRecords, surfaceRecordsDoc, surfaceQueueView));
  const pass = decisions.filter(item => item.surface_verdict === 'PASS_SURFACE');
  let contextQueue = null, contextRecords = null, contextAggregate = null;
  if (pass.length) {
    const contextQueueDoc = {schema_version: 'gemini-context-v5-context-queue-v1', ...base, stage: 'CONTEXT', surface_aggregate_sha256: sha256(surfaceAggregate), items: pass.map(item => queueItem(bySlot.get(item.neutral_id)))};
    const contextRecordsDoc = {schema_version: 'gemini-context-v5-context-records-v1', round_id: roundId, stage: 'CONTEXT', items: pass.map(item => ({neutral_id: item.neutral_id, verdict: item.context_verdict, evidence: item.context_evidence ?? 'fixture direct-source evidence'}))};
    contextQueue = jsonBytes(contextQueueDoc); contextRecords = jsonBytes(contextRecordsDoc); contextAggregate = jsonBytes(aggregateDocument('context', contextQueue, contextRecords, contextRecordsDoc));
  }
  const release = jsonBytes({schema_version: surfaceV2 ? 'gemini-context-v5-round-release-v2' : 'gemini-context-v5-round-release-v1', round_id: roundId, predecessor_release_sha256: state.lastReleaseSha256, surface_queue_sha256: sha256(surfaceQueue), ...(surfaceV2 ? {surface_queue_view_sha256: sha256(surfaceQueueView)} : {}), surface_records_sha256: sha256(surfaceRecords), surface_aggregate_sha256: sha256(surfaceAggregate), context_queue_sha256: contextQueue ? sha256(contextQueue) : null, context_records_sha256: contextRecords ? sha256(contextRecords) : null, context_aggregate_sha256: contextAggregate ? sha256(contextAggregate) : null});
  return {repo: normalizedRepo, surface_queue: surfaceQueue, surface_queue_view: surfaceQueueView, surface_records: surfaceRecords, surface_aggregate: surfaceAggregate, context_queue: contextQueue, context_records: contextRecords, context_aggregate: contextAggregate, release};
}

export function outputDocuments(state, pending = null) {
  let completedReleaseState = null;
  if (state.completedRelease) {
    if (state.round === 2 && state.completedRelease.round_id === 'ROUND-0002') {
      if (state.roundIndex.length !== 2 || state.roundIndex[0]?.round_id !== 'ROUND-0001' || state.roundIndex[1]?.round_id !== 'ROUND-0002' || state.completedRelease.release_sha256 !== state.lastReleaseSha256 || state.active.length !== 64 || [...state.lineage.values()].reduce((sum, item) => sum + item.edges.length, 0) !== 12 || state.banned.size !== 12 || state.consumed.size !== 12) throw Error('COMPLETED_RELEASE_STATE_SCOPE');
      const reserve = reserveDocument(state);
      completedReleaseState = {schema_version: 'gemini-context-v5-release-state-v4', status: 'ROUND_0002_RELEASED_ROUND_0003_AUDIT_NOT_AUTHORIZED', completed_rounds: 2, last_release_sha256: state.lastReleaseSha256, released_round: state.completedRelease, active_frame_mutated: true, lineage_mutated: true, reserve_mutated: true, round_index_mutated: true, active_rows: 64, lineage_edges: 12, remaining_reserve_rows: reserve.remaining_reserve_rows, remaining_dialogue_reserve_rows: reserve.remaining_reserve_rows - reserve.remaining_narrative_reserve_rows, remaining_narrative_reserve_rows: reserve.remaining_narrative_reserve_rows, banned_revision_ids: 12, consumed_revision_ids: 12, replacements_authorized: true, release_authorized: true, audits_released: true, round_0003_audit_authorized: false, qualification_authorized: false, inference_authorized: false, formal_gemini_experiment_inference_calls_made: 0, model_calls_started: 0, network_calls_made: 0};
    } else {
    if (state.round !== 1 || state.completedRelease.round_id !== 'ROUND-0001' || state.roundIndex.length !== 1 || state.roundIndex[0]?.round_id !== 'ROUND-0001' || state.completedRelease.release_sha256 !== state.lastReleaseSha256) throw Error('COMPLETED_RELEASE_STATE_SCOPE');
    const accounting = state.completedRelease.audit_accounting, expectedAccounting = {authorized_surface_auditor_calls_started: 2, invalid_auditor_input_attempts: 1, valid_surface_auditor_responses: 1, valid_persisted_surface_results: 1, authorized_context_auditor_calls_started: 1, valid_context_auditor_responses: 1, valid_persisted_context_results: 1, surface_rejected_slot_count: 9, context_rejected_slot_count: 1, formal_gemini_experiment_inference_calls_made: 0, network_calls_made: 0};
    const feasible = accounting && Object.values(accounting).every(Number.isInteger) && Object.values(accounting).every(value => value >= 0) && accounting.invalid_auditor_input_attempts + accounting.valid_surface_auditor_responses <= accounting.authorized_surface_auditor_calls_started && accounting.valid_persisted_surface_results <= accounting.valid_surface_auditor_responses && accounting.valid_context_auditor_responses <= accounting.authorized_context_auditor_calls_started && accounting.valid_persisted_context_results <= accounting.valid_context_auditor_responses && accounting.surface_rejected_slot_count + accounting.context_rejected_slot_count === state.banned.size && state.banned.size === state.consumed.size;
    if (!feasible || JSON.stringify(accounting) !== JSON.stringify(expectedAccounting)) throw Error('COMPLETED_RELEASE_ACCOUNTING');
    completedReleaseState = {
    schema_version: 'gemini-context-v5-release-state-v3',
    status: 'ROUND_0001_RELEASED_ROUND_0002_AUDIT_NOT_AUTHORIZED',
    completed_rounds: state.round,
    last_release_sha256: state.lastReleaseSha256,
    released_round: state.completedRelease,
    completed_surface_stage_applied_to_active_state: true,
    context_input_applied_to_active_state: true,
    active_frame_mutated: true,
    lineage_mutated: true,
    reserve_mutated: true,
    banned_revision_ids_added: state.banned.size,
    consumed_revision_ids_added: state.consumed.size,
    replacements_authorized: true,
    release_authorized: true,
    audits_released: true,
    round_0002_audit_authorized: false,
    qualification_authorized: false,
    inference_authorized: false,
    authorized_surface_auditor_calls_started: accounting.authorized_surface_auditor_calls_started,
    invalid_auditor_input_attempts: accounting.invalid_auditor_input_attempts,
    valid_surface_auditor_responses: accounting.valid_surface_auditor_responses,
    valid_persisted_surface_results: accounting.valid_persisted_surface_results,
    authorized_context_auditor_calls_started: accounting.authorized_context_auditor_calls_started,
    valid_context_auditor_responses: accounting.valid_context_auditor_responses,
    valid_persisted_context_results: accounting.valid_persisted_context_results,
    formal_gemini_experiment_inference_calls_made: accounting.formal_gemini_experiment_inference_calls_made,
    network_calls_made: accounting.network_calls_made
    };
    }
  }
  return {
    'ACTIVE-FRAME.json': activeFrameDocument(state),
    'LINEAGE.json': lineageDocument(state),
    'RESERVE-STATE.json': reserveDocument(state),
    'ROUND-INDEX.json': roundIndexDocument(state),
    'RELEASE-STATE.json': pending
      ? {schema_version: 'gemini-context-v5-release-state-v2', status: pending.status, completed_rounds: state.round, last_release_sha256: state.lastReleaseSha256, pending_round: {round_id: pending.round_id, stage: pending.stage, authorization_id: pending.authorization_id, authorization_record_sha256: pending.authorization_record_sha256, authorized_candidate_ref: pending.authorized_candidate_ref, final_pass_reviewer_agent_ids: pending.final_pass_reviewer_agent_ids, surface_queue_sha256: pending.surface_queue_sha256, surface_queue_view_sha256: pending.surface_queue_view_sha256, context_authorization: pending.context_authorization, context_queue_sha256: pending.context_input_state.context_queue_sha256, context_queue_view_sha256: pending.context_input_state.context_queue_view_sha256}, sidecar_review_gate: {record_path: pending.sidecar_review_gate_record_path, record_sha256: pending.sidecar_review_gate_record_sha256, status: pending.sidecar_review_gate_status}, invalid_attempt_exclusion: pending.invalid_attempt_exclusion, validated_surface_response: pending.validated_surface_response, validated_context_response: pending.validated_context_response, implementation_candidate_binding: pending.implementation_candidate_binding, surface_intermediate_state: pending.surface_intermediate_state, context_input_state: pending.context_input_state, context_results_state: pending.context_results_state, completed_surface_stage_applied_to_active_state: false, context_input_applied_to_active_state: false, active_frame_mutated: false, lineage_mutated: false, reserve_mutated: false, banned_revision_ids_added: 0, consumed_revision_ids_added: 0, context_audit_authorized: true, context_auditor_call_started: true, context_records_materialized: pending.context_results_state.records_materialized, context_aggregate_materialized: pending.context_results_state.aggregate_materialized, replacements_authorized: false, release_authorized: false, audits_released: false, qualification_authorized: false, inference_authorized: false, authorized_surface_auditor_calls_started: pending.authorized_surface_auditor_calls_started, authorized_context_auditor_calls_started: pending.authorized_context_auditor_calls_started, invalid_auditor_input_attempts: pending.invalid_auditor_input_attempts, valid_surface_auditor_responses: pending.valid_surface_auditor_responses, valid_persisted_surface_results: pending.valid_persisted_surface_results, valid_context_auditor_responses: pending.valid_context_auditor_responses, valid_persisted_context_results: pending.valid_persisted_context_results, formal_gemini_experiment_inference_calls_made: pending.formal_gemini_experiment_inference_calls_made, network_calls_made: 0}
      : completedReleaseState ?? {schema_version: 'gemini-context-v5-release-state-v1', status: 'ZERO_INFERENCE_IMPLEMENTATION_REVIEW_PENDING', completed_rounds: state.round, last_release_sha256: state.lastReleaseSha256, review_gate: {status: 'NOT_AUTHORIZED'}, audits_authorized: false, qualification_authorized: false, inference_authorized: false, authorized_surface_auditor_calls_started: 0, formal_gemini_experiment_inference_calls_made: 0, network_calls_made: 0}
  };
}

export function readInitialPackage(here) {
  const inheritance = JSON.parse(fs.readFileSync(path.join(here, 'INHERITANCE.json')));
  if (!exactKeys(inheritance, ['schema_version', 'status', 'source_v4', 'embedded']) || inheritance.schema_version !== 'gemini-context-v5-inheritance-v1' || inheritance.status !== 'FROZEN_NO_DRIFT') throw Error('INHERITANCE_SCHEMA');
  if (JSON.stringify(inheritance.source_v4) !== JSON.stringify(INHERITANCE_EXPECTED.source_v4) || JSON.stringify(inheritance.embedded) !== JSON.stringify(INHERITANCE_EXPECTED.embedded)) throw Error('INHERITANCE_ANCHOR_DRIFT');
  const frameBytes = fs.readFileSync(path.join(here, 'INITIAL-FRAME.json')), dialogueBytes = fs.readFileSync(path.join(here, 'INITIAL-RESERVE-DIALOGUE.json')), narrativeBytes = fs.readFileSync(path.join(here, 'INITIAL-RESERVE-NARRATIVE.json'));
  if (sha256(frameBytes) !== inheritance.embedded.initial_frame_sha256 || sha256(dialogueBytes) !== inheritance.embedded.dialogue_reserve_sha256 || sha256(narrativeBytes) !== inheritance.embedded.narrative_reserve_sha256) throw Error('INHERITED_INPUT_BYTE_DRIFT');
  const frame = JSON.parse(frameBytes), dialogue = JSON.parse(dialogueBytes), narrative = JSON.parse(narrativeBytes);
  if (!exactKeys(dialogue, ['schema_version', 'profile', 'items']) || dialogue.schema_version !== 'gemini-context-v5-initial-reserve-v1' || dialogue.profile !== 'dialogue' || dialogue.items.some(row => row.profile !== 'dialogue')) throw Error('DIALOGUE_RESERVE_SCHEMA');
  if (!exactKeys(narrative, ['schema_version', 'profile', 'items']) || narrative.schema_version !== 'gemini-context-v5-initial-reserve-v1' || narrative.profile !== 'narrative' || narrative.items.some(row => row.profile !== 'narrative')) throw Error('NARRATIVE_RESERVE_SCHEMA');
  const reserves = [...dialogue.items, ...narrative.items];
  if (sha256(jsonBytes(frame.items)) !== inheritance.embedded.frame_identity_sha256 || sha256(jsonBytes(reserves)) !== inheritance.embedded.reserve_identity_sha256 || reserves.length !== inheritance.embedded.reserve_rows || dialogue.items.length !== inheritance.embedded.dialogue_reserve_rows || narrative.items.length !== inheritance.embedded.narrative_reserve_rows) throw Error('INHERITED_IDENTITY_DRIFT');
  return {frame, reserves};
}

export function readRoundBundles(roundsDir, pendingRoundId = null) {
  if (!fs.existsSync(roundsDir)) return [];
  const rootStat = fs.lstatSync(roundsDir); if (rootStat.isSymbolicLink() || !rootStat.isDirectory()) throw Error('ROUNDS_ROOT_TYPE');
  const entries = fs.readdirSync(roundsDir, {withFileTypes: true}).sort((a, b) => textCompare(a.name, b.name));
  for (const [index, entry] of entries.entries()) {
    if (entry.name !== `ROUND-${String(index + 1).padStart(4, '0')}`) throw Error(`ROUND_DIRECTORY_SEQUENCE:${entry.name}`);
    const stat = fs.lstatSync(path.join(roundsDir, entry.name)); if (entry.isSymbolicLink() || stat.isSymbolicLink() || !entry.isDirectory() || !stat.isDirectory()) throw Error(`ROUND_ENTRY_TYPE:${entry.name}`);
  }
  return entries.map(entry => {
    const name = entry.name, dir = path.join(roundsDir, name), read = filename => fs.readFileSync(path.join(dir, filename));
    const allowed = new Set(['SURFACE-QUEUE.json', 'SURFACE-QUEUE-VIEW.json', 'SURFACE-RECORDS.json', 'SURFACE-AGGREGATE.json', 'CONTEXT-QUEUE.json', 'CONTEXT-SOURCE-ANCHORS.json', 'CONTEXT-QUEUE-VIEW.json', 'CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json', 'RELEASE.json']);
    const artifacts = fs.readdirSync(dir, {withFileTypes: true});
    for (const artifact of artifacts) {
      const stat = fs.lstatSync(path.join(dir, artifact.name));
      if (!allowed.has(artifact.name)) throw Error(`ROUND_UNEXPECTED_ARTIFACT:${name}:${artifact.name}`);
      if (artifact.isSymbolicLink() || stat.isSymbolicLink() || !artifact.isFile() || !stat.isFile()) throw Error(`ROUND_ARTIFACT_TYPE:${name}:${artifact.name}`);
    }
    if (name === pendingRoundId) {
      const pendingNames = artifacts.map(artifact => artifact.name).sort(textCompare);
      const queueViewOnly = ['SURFACE-QUEUE-VIEW.json', 'SURFACE-QUEUE.json'];
      const surfaceCompleted = ['SURFACE-AGGREGATE.json', 'SURFACE-QUEUE-VIEW.json', 'SURFACE-QUEUE.json', 'SURFACE-RECORDS.json'];
      const contextInput = ['CONTEXT-QUEUE-VIEW.json', 'CONTEXT-QUEUE.json', 'CONTEXT-SOURCE-ANCHORS.json', ...surfaceCompleted];
      const contextResults = ['CONTEXT-AGGREGATE.json', 'CONTEXT-QUEUE-VIEW.json', 'CONTEXT-QUEUE.json', 'CONTEXT-RECORDS.json', 'CONTEXT-SOURCE-ANCHORS.json', ...surfaceCompleted];
      if (name !== entries.at(-1).name || (![queueViewOnly, surfaceCompleted, contextInput, contextResults].some(expected => JSON.stringify(pendingNames) === JSON.stringify(expected)))) throw Error(`PENDING_ROUND_ARTIFACTS:${name}`);
      if (JSON.stringify(pendingNames) === JSON.stringify(queueViewOnly)) return {pending_surface_input: true, root: path.dirname(roundsDir), surface_queue: read('SURFACE-QUEUE.json'), surface_queue_view: read('SURFACE-QUEUE-VIEW.json'), surface_records: null, surface_aggregate: null, context_queue: null, context_source_anchors: null, context_queue_view: null, context_records: null, context_aggregate: null, release: null};
      return {pending_surface_stage: true, pending_context_input: JSON.stringify(pendingNames) === JSON.stringify(contextInput), pending_context_results: JSON.stringify(pendingNames) === JSON.stringify(contextResults), root: path.dirname(roundsDir), surface_queue: read('SURFACE-QUEUE.json'), surface_queue_view: read('SURFACE-QUEUE-VIEW.json'), surface_records: read('SURFACE-RECORDS.json'), surface_aggregate: read('SURFACE-AGGREGATE.json'), context_queue: pendingNames.includes('CONTEXT-QUEUE.json') ? read('CONTEXT-QUEUE.json') : null, context_source_anchors: pendingNames.includes('CONTEXT-SOURCE-ANCHORS.json') ? read('CONTEXT-SOURCE-ANCHORS.json') : null, context_queue_view: pendingNames.includes('CONTEXT-QUEUE-VIEW.json') ? read('CONTEXT-QUEUE-VIEW.json') : null, context_records: pendingNames.includes('CONTEXT-RECORDS.json') ? read('CONTEXT-RECORDS.json') : null, context_aggregate: pendingNames.includes('CONTEXT-AGGREGATE.json') ? read('CONTEXT-AGGREGATE.json') : null};
    }
    const names = new Set(artifacts.map(artifact => artifact.name)), required = ['SURFACE-QUEUE.json', 'SURFACE-RECORDS.json', 'SURFACE-AGGREGATE.json', 'RELEASE.json'];
    if (required.some(filename => !names.has(filename))) throw Error(`ROUND_REQUIRED_ARTIFACT_MISSING:${name}`);
    const contextV1Names = ['CONTEXT-QUEUE.json', 'CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json'];
    const contextV2Names = ['CONTEXT-QUEUE.json', 'CONTEXT-SOURCE-ANCHORS.json', 'CONTEXT-QUEUE-VIEW.json', 'CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json'];
    const contextPresent = contextV2Names.filter(filename => names.has(filename));
    const contextMode = contextPresent.length === 0 ? 0 : contextPresent.length === contextV1Names.length && contextV1Names.every(filename => names.has(filename)) && !names.has('CONTEXT-SOURCE-ANCHORS.json') && !names.has('CONTEXT-QUEUE-VIEW.json') ? 1 : contextPresent.length === contextV2Names.length ? 2 : -1;
    if (contextMode < 0) throw Error(`ROUND_PARTIAL_CONTEXT_ARTIFACTS:${name}`);
    const queueDoc = JSON.parse(read('SURFACE-QUEUE.json')), viewRequired = ['gemini-context-v5-surface-queue-v2','gemini-context-v5-surface-queue-v3'].includes(queueDoc.schema_version);
    if (viewRequired !== names.has('SURFACE-QUEUE-VIEW.json')) throw Error(`ROUND_SURFACE_VIEW_REQUIREMENT:${name}`);
    return {root: path.dirname(roundsDir), repo: false, surface_queue: read('SURFACE-QUEUE.json'), surface_queue_view: viewRequired ? read('SURFACE-QUEUE-VIEW.json') : null, surface_records: read('SURFACE-RECORDS.json'), surface_aggregate: read('SURFACE-AGGREGATE.json'), context_queue: contextMode ? read('CONTEXT-QUEUE.json') : null, context_source_anchors: contextMode === 2 ? read('CONTEXT-SOURCE-ANCHORS.json') : null, context_queue_view: contextMode === 2 ? read('CONTEXT-QUEUE-VIEW.json') : null, context_records: contextMode ? read('CONTEXT-RECORDS.json') : null, context_aggregate: contextMode ? read('CONTEXT-AGGREGATE.json') : null, release: read('RELEASE.json')};
  }).filter(Boolean);
}
