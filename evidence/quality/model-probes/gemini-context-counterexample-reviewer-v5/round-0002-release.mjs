#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repoDefault = path.resolve(here, '..', '..', '..', '..');
const packageRelative = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5';
const taskRelative = '.ai/task/research-gemini-context-counterexample-reviewer-v5';
const textCompare = (a, b) => Buffer.compare(Buffer.from(String(a)), Buffer.from(String(b)));
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');

export const ROUND2_RELEASE_PATHS = Object.freeze({
  pending: `${packageRelative}/PENDING-RELEASE.json`,
  fixture: `${packageRelative}/fixtures/ROUND-0002-RELEASE.json`,
  release: `${packageRelative}/rounds/ROUND-0002/RELEASE.json`,
  manifest: `${taskRelative}/ROUND-0002-RELEASE-IMPLEMENTATION-CANDIDATE-MANIFEST.json`,
  normal: `${taskRelative}/ROUND-0002-RELEASE-NORMAL-REVIEW-001.json`,
  senior: `${taskRelative}/ROUND-0002-RELEASE-SENIOR-REVIEW-001.json`,
  gate: `${taskRelative}/ROUND-0002-RELEASE-REVIEW-GATE-001.json`
});
export const ROUND2_RELEASE_RECEIPT_PATHS = Object.freeze({
  normal_dispatch: `${taskRelative}/ROUND-0002-RELEASE-NORMAL-DISPATCH-RECEIPT-001.json`,
  senior_dispatch: `${taskRelative}/ROUND-0002-RELEASE-SENIOR-DISPATCH-RECEIPT-001.json`,
  normal_completion: `${taskRelative}/ROUND-0002-RELEASE-NORMAL-COMPLETION-RECEIPT-001.json`,
  senior_completion: `${taskRelative}/ROUND-0002-RELEASE-SENIOR-COMPLETION-RECEIPT-001.json`
});
export const ROUND2_RELEASE_HISTORY_PATHS = Object.freeze({
  normal: `${taskRelative}/ROUND-0002-RELEASE-NORMAL-REVIEW-HISTORY-001.json`,
  senior: `${taskRelative}/ROUND-0002-RELEASE-SENIOR-REVIEW-HISTORY-001.json`
});

export const ROUND2_RELEASE_AUTHORIZATION = Object.freeze({
  authorization_id: 'V5-ROUND-0002-REPLACEMENT-RELEASE-IMPLEMENTATION-001',
  authorized_by: 'user',
  executor_agent_id: 'f77eedbb-5a3b-4ecb-98f6-32d9243a4164',
  scout_agent_id: 'd38a0e7f-249a-4df6-8d96-3a0b3d8a1929',
  scout_derivation: 'INDEPENDENTLY_VERIFIED_READ_ONLY_NO_ROLE_VIOLATION_DETECTED',
  review_routing: {normal: 'CODEX', senior: 'GEMINI_3_7_FLASH', opus_calls_authorized: false}
});

export const ROUND2_PREDECESSOR = 'bf37e1fc2f1015d6c86e0666154338df591d2f556a489b25ba775ccf7ce66119';
export const ROUND2_PRE_HASHES = Object.freeze({
  active_frame_sha256: 'c632d77064d1d80cd950de263ab3b3970820bed4102cb120900835ae279d1a85',
  lineage_sha256: '0fc604bc50220f8accd584f63d7aa5e560d88a2c8a23e43ebb94af3328b9ce7d',
  reserve_state_sha256: '123ec9dcd51c96f8843e69e163d25f9765fbdf411e77981ff65b4ecfe36d6eba',
  round_index_sha256: '036c80ebcce893be298e833f7aeb27983b95df65043dbc032cdac6480a9f243f',
  release_state_sha256: '0378c39116b0e8c30c9089784cc63baa7b7adff5dbfd2d0778dcb0aef7169921',
  experiment_sha256: '0440ccb84c6ee3689b8396e8a73d6172bb6bfc9c4a3ba60f686108a116cb0679'
});

export const ROUND2_AUDIT_ARTIFACTS = Object.freeze({
  'SURFACE-QUEUE.json': 'e8947540ff6b430fc8b69202abcb039dc34bbc996bb1fc241f671e280cd6a866',
  'SURFACE-QUEUE-VIEW.json': '5858861e071b7229cb3ca2ae6f3c6fd0ed972433dab2490c1a848bf4a2788030',
  'AUDITOR-RESPONSE-ROUND-0002-SURFACE-CALL-001.json': '6410f621356fc97af7d5773801ad0d64810f5ce93b6a8d4db3b912078585fd4a',
  'SURFACE-RECORDS.json': 'a1219a437a6e031e7a4fb7363b2ac41fe01f79ced36a7d1ec450e7dcb5e69cde',
  'SURFACE-AGGREGATE.json': '5f8d5c3f8f72caadb8bd48f14e585bfe5aa5bec97afb6305fe10b769b2f6f2d3',
  'CONTEXT-QUEUE.json': 'aa826aa0a4d9af8f23e7c6cf62509d4b6d2ae8efa2653b146fc694695e45006c',
  'CONTEXT-SOURCE-ANCHORS.json': '9df1078adffaf5cc37d99b0a100ea01b0b416dc65b3f51e43198e2fb5726457f',
  'CONTEXT-QUEUE-VIEW.json': '54adfa1d5da4d2a1ea6e991e0b69264ea83abc8542c079c4a99eeef5123f1ae4',
  'AUDITOR-RESPONSE-ROUND-0002-CONTEXT-CALL-001.json': '6f55afad6292844b221f9ece65282acf5edc66e978e177f3a23d94a782de0cfb',
  'CONTEXT-RECORDS.json': '177ff3f9fb77c795bc2e957790cac173a0efcae01580be2d74774a6f598ea1e1',
  'CONTEXT-AGGREGATE.json': '1306df81b4f7d9a5711d9e42927cd0b81ed0c5c1485af4499a74a2194996f56f'
});

export const ROUND2_EXPECTED_CORE_HASHES = Object.freeze({
  active_frame_sha256: 'e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3',
  lineage_sha256: '03d2c842fba9ddf95905c16c5170e2c23aa182680d520a3c3a16848f37cbb3d6',
  reserve_state_sha256: '4fab5ea380b0e20b8e6dc2ba0ffc98125e126791fd7c283e0e5608119c0725e0'
});

export const ROUND2_DECISIONS = Object.freeze([
  Object.freeze({neutral_id: 'V4-D-D05', stage: 'CONTEXT', verdict: 'NOT_CLEAN', reason_class: 'DIRECT_AUDIT_REJECTION', rejected_revision_id: 'a75b87d16d74dd486b47c31f243306721f640023ad5d8fa9d3708d9e60ad7548', replacement_revision_id: '5c600589afed143e424216c060b1c3783e61566739dc61a56f220a702d452621', reserve_rank: 6, profile: 'dialogue', public_source_file: 'game/modules/tome/data/chats/sorcerer-end.lua', skipped_incompatible_reserves: []}),
  Object.freeze({neutral_id: 'V4-C-D06', stage: 'SURFACE', verdict: 'OUT_OF_SCOPE_NON_PROSE', reason_class: 'OUT_OF_SCOPE_NON_PROSE', rejected_revision_id: '358d6a470b17724efda25d94a4e2a94359995915995cdc9715db603e86711614', replacement_revision_id: 'a221c30995cab3709354ed6934c0fcbe2fdfa7ec420af228d46e5e600ff930e8', reserve_rank: 7, profile: 'dialogue', public_source_file: 'game/modules/tome/data/chats/pre-charred-scar.lua', skipped_incompatible_reserves: []})
]);

export const ROUND2_RELEASE_EXCLUSIONS = Object.freeze([
  {path: `${taskRelative}/STATE.json`, reason: 'mutable orchestration state'},
  {path: ROUND2_RELEASE_PATHS.manifest, reason: 'candidate self-reference'},
  {path: ROUND2_RELEASE_PATHS.normal, reason: 'future independent normal review'},
  {path: ROUND2_RELEASE_PATHS.senior, reason: 'future independent senior review'},
  {path: ROUND2_RELEASE_PATHS.gate, reason: 'future combined review gate'},
  ...Object.values(ROUND2_RELEASE_RECEIPT_PATHS).map(path => ({path, reason: 'dispatch/completion receipt evidence'})),
  ...Object.values(ROUND2_RELEASE_HISTORY_PATHS).map(path => ({path, reason: 'review history evidence, excluded to avoid candidate circularity'}))
]);
export const ROUND2_CANDIDATE_RECIPE = 'SHA256(concatenation in bytewise path order of repo-relative path UTF-8 bytes + NUL + lowercase raw-file SHA-256 ASCII + LF)';
export const ROUND2_MATERIALIZATION_BOUNDARIES = Object.freeze([
  'after_create_transaction',
  'after_stage_round2_release',
  'after_stage_active_frame',
  'after_stage_lineage',
  'after_stage_reserve_state',
  'after_stage_round_index',
  'after_stage_release_state',
  'after_stage_experiment',
  'after_backup_active_frame',
  'after_backup_lineage',
  'after_backup_reserve_state',
  'after_backup_round_index',
  'after_backup_release_state',
  'after_backup_experiment',
  'after_install_round2_release',
  'after_install_active_frame',
  'after_install_lineage',
  'after_install_reserve_state',
  'after_install_round_index',
  'after_install_release_state',
  'after_install_experiment',
  'after_remove_pending_release'
]);

function readCanonical(file, label) {
  const stat = fs.lstatSync(file); if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`);
  const bytes = fs.readFileSync(file); let parsed; try { parsed = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  if (!bytes.equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return {bytes, parsed};
}

function readJson(file, label) {
  const stat = fs.lstatSync(file); if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`);
  try { return JSON.parse(fs.readFileSync(file)); } catch { throw Error(`${label}_JSON`); }
}

function assertHash(file, expected, label) {
  const actual = sha256(fs.readFileSync(file)); if (actual !== expected) throw Error(`${label}_HASH:${actual}`); return actual;
}

function readReserveRow(root, decision) {
  const dialogue = readJson(path.join(root, 'INITIAL-RESERVE-DIALOGUE.json'), 'DIALOGUE_RESERVE').items;
  const row = dialogue.find(item => item.reserve_rank === decision.reserve_rank);
  if (!row || row.revision_id !== decision.replacement_revision_id || row.profile !== decision.profile || row.public_source_file !== decision.public_source_file) throw Error(`ROUND2_RESERVE_MAPPING:${decision.neutral_id}`);
  return row;
}

function deriveCoreDocuments(root) {
  for (const [name, expected] of Object.entries(ROUND2_PRE_HASHES)) {
    const filename = name === 'experiment_sha256' ? 'EXPERIMENT.json' : name.replace('_sha256', '').split('_').map(value => value.toUpperCase()).join('-') + '.json';
    assertHash(path.join(root, filename), expected, `ROUND2_PRE_${filename}`);
  }
  const active = structuredClone(readCanonical(path.join(root, 'ACTIVE-FRAME.json'), 'ACTIVE_FRAME').parsed);
  const lineage = structuredClone(readCanonical(path.join(root, 'LINEAGE.json'), 'LINEAGE').parsed);
  const reserve = structuredClone(readCanonical(path.join(root, 'RESERVE-STATE.json'), 'RESERVE_STATE').parsed);
  for (const decision of ROUND2_DECISIONS) {
    const index = active.items.findIndex(item => item.neutral_id === decision.neutral_id);
    if (index < 0 || active.items[index].revision_id !== decision.rejected_revision_id) throw Error(`ROUND2_ACTIVE_MAPPING:${decision.neutral_id}`);
    const reserveRow = readReserveRow(root, decision);
    const replacement = {...reserveRow}; delete replacement.reserve_rank;
    active.items[index] = {neutral_id: decision.neutral_id, cohort: active.items[index].cohort, ...replacement};
    const chain = lineage.items.find(item => item.neutral_id === decision.neutral_id);
    if (!chain || chain.revisions.at(-1) !== decision.rejected_revision_id) throw Error(`ROUND2_LINEAGE_HEAD:${decision.neutral_id}`);
    chain.revisions.push(decision.replacement_revision_id);
    const queue = decision.stage === 'SURFACE' ? ROUND2_AUDIT_ARTIFACTS['SURFACE-QUEUE.json'] : ROUND2_AUDIT_ARTIFACTS['CONTEXT-QUEUE.json'];
    const aggregate = decision.stage === 'SURFACE' ? ROUND2_AUDIT_ARTIFACTS['SURFACE-AGGREGATE.json'] : ROUND2_AUDIT_ARTIFACTS['CONTEXT-AGGREGATE.json'];
    chain.edges.push({edge_ordinal: chain.edges.length + 1, round_id: 'ROUND-0002', stage: decision.stage, reason_class: decision.reason_class, verdict: decision.verdict, rejected_revision_id: decision.rejected_revision_id, replacement_revision_id: decision.replacement_revision_id, reserve_rank: decision.reserve_rank, queue_sha256: queue, aggregate_sha256: aggregate, skipped_incompatible_reserves: []});
  }
  active.last_completed_round = 2; lineage.last_completed_round = 2;
  reserve.consumed_revision_ids = [...new Set([...reserve.consumed_revision_ids, ...ROUND2_DECISIONS.map(item => item.replacement_revision_id)])].sort(textCompare);
  reserve.banned_revision_ids = [...new Set([...reserve.banned_revision_ids, ...ROUND2_DECISIONS.map(item => item.rejected_revision_id)])].sort(textCompare);
  const unavailable = new Set([...reserve.unavailable_reserve_revision_ids, ...ROUND2_DECISIONS.flatMap(item => [item.rejected_revision_id, item.replacement_revision_id])]);
  const initialReserveIds = new Set(readJson(path.join(root, 'INITIAL-RESERVE-DIALOGUE.json'), 'DIALOGUE_RESERVE').items.map(item => item.revision_id));
  const initialNarrativeIds = new Set(readJson(path.join(root, 'INITIAL-RESERVE-NARRATIVE.json'), 'NARRATIVE_RESERVE').items.map(item => item.revision_id));
  reserve.unavailable_reserve_revision_ids = [...unavailable].filter(id => initialReserveIds.has(id) || initialNarrativeIds.has(id)).sort(textCompare);
  reserve.remaining_reserve_rows = reserve.initial_reserve_rows - reserve.unavailable_reserve_revision_ids.length;
  reserve.remaining_narrative_reserve_rows = reserve.initial_narrative_reserve_rows - reserve.unavailable_reserve_revision_ids.filter(id => initialNarrativeIds.has(id)).length;
  const core = {'ACTIVE-FRAME.json': active, 'LINEAGE.json': lineage, 'RESERVE-STATE.json': reserve};
  const hashes = Object.fromEntries(Object.entries(core).map(([name, doc]) => [name, sha256(jsonBytes(doc))]));
  const expected = {'ACTIVE-FRAME.json': ROUND2_EXPECTED_CORE_HASHES.active_frame_sha256, 'LINEAGE.json': ROUND2_EXPECTED_CORE_HASHES.lineage_sha256, 'RESERVE-STATE.json': ROUND2_EXPECTED_CORE_HASHES.reserve_state_sha256};
  if (JSON.stringify(hashes) !== JSON.stringify(expected)) throw Error(`ROUND2_CORE_HASH_MISMATCH:${JSON.stringify(hashes)}`);
  return core;
}

function auditArtifactHashes(root) {
  const result = {};
  for (const [name, expected] of Object.entries(ROUND2_AUDIT_ARTIFACTS)) {
    const file = name.startsWith('AUDITOR-RESPONSE-') ? path.join(root, name) : path.join(root, 'rounds', 'ROUND-0002', name);
    result[name] = assertHash(file, expected, `ROUND2_AUDIT_${name}`);
  }
  const surface = readCanonical(path.join(root, 'rounds/ROUND-0002/SURFACE-AGGREGATE.json'), 'ROUND2_SURFACE_AGGREGATE').parsed;
  const context = readCanonical(path.join(root, 'rounds/ROUND-0002/CONTEXT-AGGREGATE.json'), 'ROUND2_CONTEXT_AGGREGATE').parsed;
  if (JSON.stringify(surface.reject_ids) !== JSON.stringify(['V4-C-D06']) || surface.items.find(item => item.neutral_id === 'V4-C-D06')?.verdict !== 'OUT_OF_SCOPE_NON_PROSE' || JSON.stringify(context.not_clean_ids) !== JSON.stringify(['V4-D-D05'])) throw Error('ROUND2_EXACT_REJECT_BINDING');
  return result;
}

export function deriveRound2Fixture(root = here) {
  const artifacts = auditArtifactHashes(root), core = deriveCoreDocuments(root);
  const beforeProjection = {completed_rounds: 1, active_frame_sha256: ROUND2_PRE_HASHES.active_frame_sha256, lineage_sha256: ROUND2_PRE_HASHES.lineage_sha256, reserve_state_sha256: ROUND2_PRE_HASHES.reserve_state_sha256, predecessor_release_sha256: ROUND2_PREDECESSOR};
  const afterProjection = {completed_rounds: 2, active_frame_sha256: ROUND2_EXPECTED_CORE_HASHES.active_frame_sha256, lineage_sha256: ROUND2_EXPECTED_CORE_HASHES.lineage_sha256, reserve_state_sha256: ROUND2_EXPECTED_CORE_HASHES.reserve_state_sha256, active_rows: 64, lineage_edges: 12, remaining_reserve_rows: 299, remaining_dialogue_reserve_rows: 226, remaining_narrative_reserve_rows: 73, banned_revision_ids: 12, consumed_revision_ids: 12};
  const release = {
    schema_version: 'gemini-context-v5-round-release-v4', round_id: 'ROUND-0002', predecessor_release_sha256: ROUND2_PREDECESSOR,
    release_authorization: ROUND2_RELEASE_AUTHORIZATION,
    immutable_audit_provenance: {artifact_sha256: artifacts, surface_reject_ids: ['V4-C-D06'], context_reject_ids: ['V4-D-D05'], replacement_eligibility: {OUT_OF_SCOPE_NON_PROSE: true}},
    materialization_review_policy: {mode: 'EXTERNAL_NON_CIRCULAR_GATE', candidate_manifest_path: ROUND2_RELEASE_PATHS.manifest, normal_review_path: ROUND2_RELEASE_PATHS.normal, senior_review_path: ROUND2_RELEASE_PATHS.senior, combined_gate_path: ROUND2_RELEASE_PATHS.gate, review_hashes_embedded_in_release: false},
    before_state: beforeProjection, after_state: afterProjection, decisions: ROUND2_DECISIONS
  };
  const releaseBytes = jsonBytes(release), releaseSha256 = sha256(releaseBytes);
  const roundIndex = structuredClone(readCanonical(path.join(root, 'ROUND-INDEX.json'), 'ROUND_INDEX').parsed);
  roundIndex.completed_rounds = 2; roundIndex.last_release_sha256 = releaseSha256;
  roundIndex.rounds.push({round_id: 'ROUND-0002', release_sha256: releaseSha256, surface_queue_sha256: artifacts['SURFACE-QUEUE.json'], surface_queue_view_sha256: artifacts['SURFACE-QUEUE-VIEW.json'], surface_aggregate_sha256: artifacts['SURFACE-AGGREGATE.json'], context_queue_sha256: artifacts['CONTEXT-QUEUE.json'], context_source_anchors_sha256: artifacts['CONTEXT-SOURCE-ANCHORS.json'], context_queue_view_sha256: artifacts['CONTEXT-QUEUE-VIEW.json'], context_aggregate_sha256: artifacts['CONTEXT-AGGREGATE.json']});
  const releasedRound = {round_id: 'ROUND-0002', release_sha256: releaseSha256, predecessor_release_sha256: ROUND2_PREDECESSOR, release_authorization: ROUND2_RELEASE_AUTHORIZATION, immutable_audit_provenance: release.immutable_audit_provenance, materialization_review_policy: release.materialization_review_policy, decisions: ROUND2_DECISIONS};
  const releaseState = {schema_version: 'gemini-context-v5-release-state-v4', status: 'ROUND_0002_RELEASED_ROUND_0003_AUDIT_NOT_AUTHORIZED', completed_rounds: 2, last_release_sha256: releaseSha256, released_round: releasedRound, active_frame_mutated: true, lineage_mutated: true, reserve_mutated: true, round_index_mutated: true, active_rows: 64, lineage_edges: 12, remaining_reserve_rows: 299, remaining_dialogue_reserve_rows: 226, remaining_narrative_reserve_rows: 73, banned_revision_ids: 12, consumed_revision_ids: 12, replacements_authorized: true, release_authorized: true, audits_released: true, round_0003_audit_authorized: false, qualification_authorized: false, inference_authorized: false, formal_gemini_experiment_inference_calls_made: 0, model_calls_started: 0, network_calls_made: 0};
  const experiment = {schema_version: 'gemini-context-v5-experiment-state-v4', status: releaseState.status, completed_rounds: 2, last_release_sha256: releaseSha256, released_round: releasedRound, audits_released: true, replacements_authorized: true, release_authorized: true, mutations_released: true, round_0003_audit_authorized: false, qualification_authorized: false, inference_authorized: false, formal_gemini_experiment_inference_calls_made: 0, model_calls_started: 0, network_calls_made: 0};
  const documents = {...core, 'ROUND-INDEX.json': roundIndex, 'RELEASE-STATE.json': releaseState, 'EXPERIMENT.json': experiment};
  const expectedHashes = {release_sha256: releaseSha256, ...Object.fromEntries(Object.entries(documents).map(([name, doc]) => [name.toLowerCase().replaceAll('-', '_').replace('.json', '_sha256'), sha256(jsonBytes(doc))]))};
  return {release, releaseBytes, documents, expectedHashes};
}

export function buildPendingRelease(root = here) {
  const derived = deriveRound2Fixture(root);
  return {schema_version: 'gemini-context-v5-round-0002-pending-release-v1', status: 'ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED', round_id: 'ROUND-0002', predecessor_release_sha256: ROUND2_PREDECESSOR, authorization: ROUND2_RELEASE_AUTHORIZATION, immutable_audit_artifact_sha256: ROUND2_AUDIT_ARTIFACTS, decisions: ROUND2_DECISIONS, expected_post_state: {active_rows: 64, lineage_edges: 12, remaining_reserve_rows: 299, remaining_dialogue_reserve_rows: 226, remaining_narrative_reserve_rows: 73, banned_revision_ids: 12, consumed_revision_ids: 12}, expected_hashes: derived.expectedHashes, release_fixture_path: path.relative(root, path.join(root, 'fixtures/ROUND-0002-RELEASE.json')), release_fixture_sha256: derived.expectedHashes.release_sha256, candidate_manifest_path: ROUND2_RELEASE_PATHS.manifest, review_paths: {normal: ROUND2_RELEASE_PATHS.normal, senior: ROUND2_RELEASE_PATHS.senior, gate: ROUND2_RELEASE_PATHS.gate}, materialization: {atomic_only_after_dual_review: true, real_release_created: false, derived_state_mutated: false, pending_release_removed: false, round_0003_created: false}, current_preflight_decision: 'NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED', formal_gemini_experiment_inference_calls_made: 0, model_calls_started: 0, network_calls_made: 0};
}

function enumerateCoverage(repo) {
  const excluded = new Set(ROUND2_RELEASE_EXCLUSIONS.map(item => item.path)), files = [];
  const walk = relative => {
    const stat = fs.lstatSync(path.join(repo, relative));
    if (stat.isSymbolicLink()) throw Error(`ROUND2_CANDIDATE_SYMLINK:${relative}`);
    if (stat.isFile()) { if (!excluded.has(relative)) files.push(relative); return; }
    if (!stat.isDirectory()) throw Error(`ROUND2_CANDIDATE_FILE_TYPE:${relative}`);
    for (const name of fs.readdirSync(path.join(repo, relative)).sort(textCompare)) walk(`${relative}/${name}`);
  };
  walk(packageRelative); walk(taskRelative); return files.sort(textCompare);
}

export function generateRound2ReleaseCandidate({repo = repoDefault} = {}) {
  const root = path.join(repo, packageRelative), pending = buildPendingRelease(root), fixture = deriveRound2Fixture(root);
  fs.mkdirSync(path.dirname(path.join(repo, ROUND2_RELEASE_PATHS.fixture)), {recursive: true});
  fs.writeFileSync(path.join(repo, ROUND2_RELEASE_PATHS.fixture), fixture.releaseBytes);
  fs.writeFileSync(path.join(repo, ROUND2_RELEASE_PATHS.pending), jsonBytes(pending));
  const files = enumerateCoverage(repo).map(relative => ({path: relative, sha256: sha256(fs.readFileSync(path.join(repo, relative)))}));
  const candidateRef = sha256(Buffer.from(files.map(item => `${item.path}\0${item.sha256}\n`).join('')));
  const manifest = {schema_version: 'gemini-context-v5-round-0002-release-implementation-candidate-v1', status: 'ROUND_0002_RELEASE_IMPLEMENTATION_PENDING_INDEPENDENT_DUAL_REVIEW', round_id: 'ROUND-0002', author_agent_id: ROUND2_RELEASE_AUTHORIZATION.executor_agent_id, scout_derivation: {agent_id: ROUND2_RELEASE_AUTHORIZATION.scout_agent_id, independently_verified: true, repository_write_detected: false, role_violation_recorded: false}, threat_model: 'NON_ADVERSARIAL_REPOSITORY_WORKFLOW', coverage_policy: {package_root: packageRelative, task_root: taskRelative, policy: 'ALL_REGULAR_FILES_EXCEPT_EXACT_EXCLUSIONS'}, expected_hashes: fixture.expectedHashes, current_preflight_decision: 'NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED', real_materialization: {release_created: false, derived_state_mutated: false, pending_release_removed: false, round_0003_created: false, model_calls_started: 0, network_calls_made: 0}, recipe: ROUND2_CANDIDATE_RECIPE, exclusions: ROUND2_RELEASE_EXCLUSIONS, files, candidate_ref: candidateRef};
  fs.writeFileSync(path.join(repo, ROUND2_RELEASE_PATHS.manifest), jsonBytes(manifest));
  return validateRound2ReleaseCandidate(repo);
}

export function validateRound2ReleaseCandidate(repo = repoDefault) {
  const manifestRecord = readCanonical(path.join(repo, ROUND2_RELEASE_PATHS.manifest), 'ROUND2_RELEASE_CANDIDATE'), manifest = manifestRecord.parsed;
  const expectedKeys = ['schema_version','status','round_id','author_agent_id','scout_derivation','threat_model','coverage_policy','expected_hashes','current_preflight_decision','real_materialization','recipe','exclusions','files','candidate_ref'];
  if (JSON.stringify(Object.keys(manifest).sort()) !== JSON.stringify(expectedKeys.sort()) || manifest.schema_version !== 'gemini-context-v5-round-0002-release-implementation-candidate-v1' || manifest.status !== 'ROUND_0002_RELEASE_IMPLEMENTATION_PENDING_INDEPENDENT_DUAL_REVIEW' || manifest.round_id !== 'ROUND-0002' || manifest.author_agent_id !== ROUND2_RELEASE_AUTHORIZATION.executor_agent_id || manifest.scout_derivation?.agent_id !== ROUND2_RELEASE_AUTHORIZATION.scout_agent_id || manifest.scout_derivation?.independently_verified !== true || manifest.scout_derivation?.repository_write_detected !== false || manifest.scout_derivation?.role_violation_recorded !== false || manifest.threat_model !== 'NON_ADVERSARIAL_REPOSITORY_WORKFLOW' || manifest.current_preflight_decision !== 'NO_GO_ROUND_0002_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED' || manifest.recipe !== ROUND2_CANDIDATE_RECIPE || JSON.stringify(manifest.exclusions) !== JSON.stringify(ROUND2_RELEASE_EXCLUSIONS)) throw Error('ROUND2_RELEASE_CANDIDATE_SCHEMA');
  const fixture = deriveRound2Fixture(path.join(repo, packageRelative));
  if (JSON.stringify(manifest.expected_hashes) !== JSON.stringify(fixture.expectedHashes)) throw Error('ROUND2_RELEASE_CANDIDATE_EXPECTED_HASHES');
  const coverage = enumerateCoverage(repo); if (JSON.stringify(manifest.files.map(item => item.path)) !== JSON.stringify(coverage)) throw Error('ROUND2_RELEASE_CANDIDATE_COVERAGE');
  for (const item of manifest.files) if (!/^[0-9a-f]{64}$/u.test(item.sha256) || sha256(fs.readFileSync(path.join(repo, item.path))) !== item.sha256) throw Error(`ROUND2_RELEASE_CANDIDATE_FILE_HASH:${item.path}`);
  const candidateRef = sha256(Buffer.from(manifest.files.map(item => `${item.path}\0${item.sha256}\n`).join(''))); if (candidateRef !== manifest.candidate_ref) throw Error('ROUND2_RELEASE_CANDIDATE_ROOT');
  return {status: 'PASS', candidate_ref: candidateRef, manifest_sha256: sha256(manifestRecord.bytes), file_count: manifest.files.length, expected_hashes: manifest.expected_hashes};
}

export function validateRound2PendingRelease(root = here, repo = repoDefault) {
  const pending = readCanonical(path.join(root, 'PENDING-RELEASE.json'), 'ROUND2_PENDING_RELEASE').parsed, expected = buildPendingRelease(root);
  if (JSON.stringify(pending) !== JSON.stringify(expected)) throw Error('ROUND2_PENDING_RELEASE_BINDING');
  assertHash(path.join(root, 'fixtures/ROUND-0002-RELEASE.json'), pending.release_fixture_sha256, 'ROUND2_RELEASE_FIXTURE');
  const candidate = validateRound2ReleaseCandidate(repo);
  return {pending, candidate};
}

const REVIEW_ROLE_ROUTE = Object.freeze({normal: {role: 'REVIEWER', route: 'Codex gpt-5.6-sol xhigh'}, senior: {role: 'SENIOR_REVIEWER', route: 'Gemini 3.7 Flash high'}});

function canonicalReview(repo, relative, kind, candidate, {allowUnverifiedFixture = false} = {}) {
  const {role, route} = REVIEW_ROLE_ROUTE[kind];
  const record = readCanonical(path.join(repo, relative), `ROUND2_RELEASE_${role}_REVIEW`), value = record.parsed;
  const dispatchPath = ROUND2_RELEASE_RECEIPT_PATHS[`${kind}_dispatch`], completionPath = ROUND2_RELEASE_RECEIPT_PATHS[`${kind}_completion`];
  const dispatch = readCanonical(path.join(repo, dispatchPath), `ROUND2_RELEASE_${role}_DISPATCH_RECEIPT`).parsed;
  const completion = readCanonical(path.join(repo, completionPath), `ROUND2_RELEASE_${role}_COMPLETION_RECEIPT`).parsed;
  const keys = ['schema_version','review_id','round_id','role','agent_id','route','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','dispatch_id','completion_receipt_path','response_sha256','findings','repository_modified_by_review','recorded_at'];
  const completionKeys = ['schema_version','receipt_id','round_id','role','agent_id','route','dispatch_id','dispatch_receipt_path','dispatch_receipt_sha256','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','status','completed_at','response_sha256','verdict','response_text'];
  validateDispatchReceipt(repo, dispatchPath, kind, candidate, {allowUnverifiedFixture});
  if (dispatch.role !== role || dispatch.agent_id !== value.agent_id || dispatch.route !== route) throw Error(`ROUND2_RELEASE_${role}_DISPATCH_RECEIPT_BINDING`);
  const fixture = completion.provenance === 'UNVERIFIED_FIXTURE_ONLY';
  if (fixture && !allowUnverifiedFixture) throw Error(`ROUND2_RELEASE_${role}_COMPLETION_RECEIPT_FIXTURE_NOT_ALLOWED`);
  const cycle = dispatch.dispatch_id.match(/-(\d{3})$/u)?.[1];
  if (!cycle || (!fixture && completion.receipt_id !== `V5-ROUND-0002-RELEASE-${kind === 'normal' ? 'NORMAL' : 'SENIOR'}-COMPLETION-RECEIPT-${cycle}`)) throw Error(`ROUND2_RELEASE_${role}_COMPLETION_RECEIPT_CYCLE_BINDING`);
  if (JSON.stringify(Object.keys(completion).sort()) !== JSON.stringify(completionKeys.concat(fixture ? ['provenance'] : []).sort()) || completion.schema_version !== 'gemini-context-v5-round-0002-release-review-completion-receipt-v1' || completion.round_id !== 'ROUND-0002' || completion.role !== role || completion.agent_id !== value.agent_id || completion.route !== route || completion.dispatch_id !== dispatch.dispatch_id || completion.dispatch_receipt_path !== dispatchPath || completion.dispatch_receipt_sha256 !== sha256(fs.readFileSync(path.join(repo, dispatchPath))) || completion.candidate_ref !== candidate.candidate_ref || completion.candidate_manifest_path !== ROUND2_RELEASE_PATHS.manifest || completion.candidate_manifest_sha256 !== candidate.manifest_sha256 || completion.status !== 'COMPLETED_NON_ERRORED' || !['PASS','CHANGES_REQUIRED'].includes(completion.verdict) || !/^[0-9a-f]{64}$/u.test(completion.response_sha256) || sha256(Buffer.from(completion.response_text, 'utf8')) !== completion.response_sha256) throw Error(`ROUND2_RELEASE_${role}_COMPLETION_RECEIPT_BINDING`);
  const reviewFixture = value.provenance === 'UNVERIFIED_FIXTURE_ONLY';
  if (reviewFixture && !allowUnverifiedFixture) throw Error(`ROUND2_RELEASE_${role}_REVIEW_FIXTURE_NOT_ALLOWED`);
  if (JSON.stringify(Object.keys(value).sort()) !== JSON.stringify(keys.concat(reviewFixture ? ['provenance'] : []).sort()) || value.schema_version !== 'gemini-context-v5-round-0002-release-review-v2' || value.review_id !== `V5-ROUND-0002-RELEASE-${kind === 'normal' ? 'NORMAL' : 'SENIOR'}-REVIEW-${cycle}` || value.round_id !== 'ROUND-0002' || value.role !== role || value.agent_id !== dispatch.agent_id || value.route !== route || !['PASS','CHANGES_REQUIRED'].includes(value.status) || value.candidate_ref !== candidate.candidate_ref || value.candidate_manifest_path !== ROUND2_RELEASE_PATHS.manifest || value.candidate_manifest_sha256 !== candidate.manifest_sha256 || value.dispatch_id !== dispatch.dispatch_id || value.completion_receipt_path !== completionPath || value.response_sha256 !== completion.response_sha256 || !Array.isArray(value.findings) || value.repository_modified_by_review !== false || typeof value.recorded_at !== 'string') throw Error(`ROUND2_RELEASE_${role}_REVIEW_BINDING`);
  return {path: relative, sha256: sha256(record.bytes), agent_id: value.agent_id, role, route, status: value.status, completion_verdict: completion.verdict, dispatch_id: dispatch.dispatch_id, cycle, response_sha256: completion.response_sha256};
}

function validateDispatchReceipt(repo, relative, kind, candidate, {allowUnverifiedFixture = false} = {}) {
  const record = readCanonical(path.join(repo, relative), `ROUND2_RELEASE_${kind.toUpperCase()}_DISPATCH_RECEIPT`), value = record.parsed;
  const expected = kind === 'normal' ? {role:'REVIEWER', agent_ids:['d60d2518-5cff-4c4e-93f8-c94398db2f49'], route:'Codex gpt-5.6-sol xhigh', dispatch_prefixes:{'d60d2518-5cff-4c4e-93f8-c94398db2f49':'V5-R2-RELEASE-DISPATCH-CODEX-D60D2518-'}, opus_quota_override:false} : {role:'SENIOR_REVIEWER', agent_ids:['2b31c769-5bde-4929-bef1-6ac319383945','3abab1a2-eff2-4923-8cbc-f70cee2f2db4'], route:'Gemini 3.7 Flash high', dispatch_prefixes:{'2b31c769-5bde-4929-bef1-6ac319383945':'V5-R2-RELEASE-DISPATCH-GEMINI-2B31C769-','3abab1a2-eff2-4923-8cbc-f70cee2f2db4':'V5-R2-RELEASE-DISPATCH-GEMINI-3ABAB1A2-'}, opus_quota_override:true};
  const fixture = value.provenance === 'UNVERIFIED_FIXTURE_ONLY';
  if (fixture && !allowUnverifiedFixture) throw Error(`ROUND2_RELEASE_${kind.toUpperCase()}_DISPATCH_RECEIPT_FIXTURE_NOT_ALLOWED`);
  const keys = ['schema_version','receipt_id','round_id','role','agent_id','route','dispatch_id','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','status','agent_created_at','dispatched_at','orchestrator_authorization_scope','expected_permitted_read_only_task','completion_absent','opus_quota_override'];
  const cycleMatch = value.dispatch_id.match(/-(\d{3})$/u), cycle = cycleMatch?.[1];
  if (!fixture && (!cycle || value.dispatch_id !== `${expected.dispatch_prefixes[value.agent_id]}${cycle}` || value.receipt_id !== `V5-ROUND-0002-RELEASE-${kind === 'normal' ? 'NORMAL' : 'SENIOR'}-DISPATCH-RECEIPT-${cycle}`)) throw Error(`ROUND2_RELEASE_${kind.toUpperCase()}_DISPATCH_RECEIPT_CYCLE_BINDING`);
  if (JSON.stringify(Object.keys(value).sort()) !== JSON.stringify(keys.concat(fixture ? ['provenance'] : []).sort()) || value.schema_version !== 'gemini-context-v5-round-0002-release-review-dispatch-receipt-v1' || value.round_id !== 'ROUND-0002' || value.role !== expected.role || (!fixture && !expected.agent_ids.includes(value.agent_id)) || value.route !== expected.route || value.candidate_ref !== candidate.candidate_ref || value.candidate_manifest_path !== ROUND2_RELEASE_PATHS.manifest || value.candidate_manifest_sha256 !== candidate.manifest_sha256 || value.status !== 'DISPATCHED' || typeof value.agent_created_at !== 'string' || typeof value.dispatched_at !== 'string' || value.completion_absent !== true || value.opus_quota_override !== (fixture ? value.opus_quota_override : expected.opus_quota_override) || value.orchestrator_authorization_scope?.production_materialization !== false || value.orchestrator_authorization_scope?.derived_state_mutation !== false || value.orchestrator_authorization_scope?.round_0003 !== false || value.expected_permitted_read_only_task !== 'READ_ONLY_REVIEW_OF_ROUND_0002_RELEASE_IMPLEMENTATION_CANDIDATE') throw Error(`ROUND2_RELEASE_${kind.toUpperCase()}_DISPATCH_RECEIPT_BINDING`);
  return {path: relative, sha256: sha256(record.bytes), agent_id:value.agent_id, dispatch_id:value.dispatch_id, cycle, route:value.route, status:value.status};
}

export function evaluateRound2ReleaseReviewGate(repo = repoDefault, {allowUnverifiedFixture = false, candidateOverride = null} = {}) {
  let candidate; try { candidate = candidateOverride || validateRound2ReleaseCandidate(repo); } catch (error) { return {satisfied: false, invalid: true, reason: error.code === 'ENOENT' ? 'ROUND2_RELEASE_CANDIDATE_MISSING' : error.message}; }
  const paths = [ROUND2_RELEASE_PATHS.normal, ROUND2_RELEASE_PATHS.senior, ROUND2_RELEASE_PATHS.gate], present = paths.filter(relative => fs.existsSync(path.join(repo, relative)));
  const dispatchPaths = Object.values(ROUND2_RELEASE_RECEIPT_PATHS).filter(relative => relative.endsWith('DISPATCH-RECEIPT-001.json')), dispatchPresent = dispatchPaths.filter(relative => fs.existsSync(path.join(repo, relative)));
  if (!present.length && dispatchPresent.length) {
    if (dispatchPresent.length !== dispatchPaths.length) return {satisfied: false, invalid: true, reason: 'ROUND2_RELEASE_DISPATCH_SET_PARTIAL', candidate};
    try { const normal = validateDispatchReceipt(repo, ROUND2_RELEASE_RECEIPT_PATHS.normal_dispatch, 'normal', candidate, {allowUnverifiedFixture}); const senior = validateDispatchReceipt(repo, ROUND2_RELEASE_RECEIPT_PATHS.senior_dispatch, 'senior', candidate, {allowUnverifiedFixture}); if (normal.agent_id === senior.agent_id) throw Error('ROUND2_RELEASE_REVIEWER_INDEPENDENCE'); if (normal.cycle !== senior.cycle) throw Error('ROUND2_RELEASE_DISPATCH_CYCLE_MISMATCH'); return {satisfied:false, invalid:false, reason:'COMPLETION_RECEIPTS_AND_REVIEWS_REQUIRED', candidate, dispatch:{normal,senior}}; } catch (error) { return {satisfied:false, invalid:true, reason:error.message, candidate}; }
  }
  if (!present.length) return {satisfied: false, invalid: false, reason: 'NORMAL_SENIOR_AND_COMBINED_REVIEW_REQUIRED', candidate};
  if (present.length !== paths.length) return {satisfied: false, invalid: true, reason: 'ROUND2_RELEASE_REVIEW_SET_PARTIAL', candidate};
  try {
    const normal = canonicalReview(repo, ROUND2_RELEASE_PATHS.normal, 'normal', candidate, {allowUnverifiedFixture});
    const senior = canonicalReview(repo, ROUND2_RELEASE_PATHS.senior, 'senior', candidate, {allowUnverifiedFixture});
    if (normal.agent_id === senior.agent_id) throw Error('ROUND2_RELEASE_REVIEWER_INDEPENDENCE');
    if (normal.cycle !== senior.cycle) throw Error('ROUND2_RELEASE_DISPATCH_CYCLE_MISMATCH');
    if (normal.status !== 'PASS' || senior.status !== 'PASS' || normal.completion_verdict !== 'PASS' || senior.completion_verdict !== 'PASS') throw Error('ROUND2_RELEASE_REPAIR_REQUIRED_REVIEW_VERDICT');
    const gateRecord = readCanonical(path.join(repo, ROUND2_RELEASE_PATHS.gate), 'ROUND2_RELEASE_REVIEW_GATE'), gate = gateRecord.parsed;
    const keys = ['schema_version','gate_id','round_id','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','normal_review','senior_review','permitted_action','forbidden_scope','recorded_at'];
    const forbidden = ['ROUND_0003','MODEL_CALL','NETWORK_CALL','GIT_STAGE','GIT_HISTORY'];
    const gateFixture = gate.provenance === 'UNVERIFIED_FIXTURE_ONLY';
    if (gateFixture && !allowUnverifiedFixture) throw Error('ROUND2_RELEASE_REVIEW_GATE_FIXTURE_NOT_ALLOWED');
    if (JSON.stringify(Object.keys(gate).sort()) !== JSON.stringify(keys.concat(gateFixture ? ['provenance'] : []).sort()) || gate.schema_version !== 'gemini-context-v5-round-0002-release-review-gate-v1' || gate.gate_id !== 'V5-ROUND-0002-RELEASE-DUAL-PASS-GATE-001' || gate.round_id !== 'ROUND-0002' || gate.status !== 'SATISFIED_FINAL_DUAL_PASS' || gate.candidate_ref !== candidate.candidate_ref || gate.candidate_manifest_path !== ROUND2_RELEASE_PATHS.manifest || gate.candidate_manifest_sha256 !== candidate.manifest_sha256 || JSON.stringify(gate.normal_review) !== JSON.stringify(normal) || JSON.stringify(gate.senior_review) !== JSON.stringify(senior) || gate.permitted_action !== 'GO_ROUND_0002_RELEASE_ATOMIC_MATERIALIZATION_ONLY' || JSON.stringify(gate.forbidden_scope) !== JSON.stringify(forbidden) || typeof gate.recorded_at !== 'string') throw Error('ROUND2_RELEASE_REVIEW_GATE_BINDING');
    return {satisfied: true, invalid: false, reason: null, candidate, provenance: {status: gate.status, gate_path: ROUND2_RELEASE_PATHS.gate, gate_sha256: sha256(gateRecord.bytes), normal, senior}};
  } catch (error) { return {satisfied: false, invalid: true, reason: error.code === 'ENOENT' ? 'ROUND2_RELEASE_REVIEW_FILE_MISSING' : error.message, candidate}; }
}

// Completed state must retain the same external evidence contract as pending state.
// Authenticity beyond these persisted attestations is intentionally outside the
// NON_ADVERSARIAL_REPOSITORY_WORKFLOW threat model.
export function validateRound2CompletedReleaseEvidence(repo = repoDefault, {allowUnverifiedFixture = false} = {}) {
  const manifestRecord = readCanonical(path.join(repo, ROUND2_RELEASE_PATHS.manifest), 'ROUND2_COMPLETED_CANDIDATE_MANIFEST'), manifest = manifestRecord.parsed;
  const candidate = {candidate_ref: manifest.candidate_ref, manifest_sha256: sha256(manifestRecord.bytes), expected_hashes: manifest.expected_hashes, file_count: manifest.files.length};
  const pendingRelative = ROUND2_RELEASE_PATHS.pending;
  const transitionPaths = new Set([ROUND2_RELEASE_PATHS.release, pendingRelative, ...['ACTIVE-FRAME.json','LINEAGE.json','RESERVE-STATE.json','ROUND-INDEX.json','RELEASE-STATE.json','EXPERIMENT.json'].map(name => `${packageRelative}/${name}`)]);
  for (const item of manifest.files) {
    if (item.path === pendingRelative) { if (fs.existsSync(path.join(repo, item.path))) throw Error('ROUND2_COMPLETED_PENDING_NOT_REMOVED'); continue; }
    if (transitionPaths.has(item.path)) continue;
    if (!fs.existsSync(path.join(repo, item.path)) || sha256(fs.readFileSync(path.join(repo, item.path))) !== item.sha256) throw Error(`ROUND2_COMPLETED_CANDIDATE_FILE_DRIFT:${item.path}`);
  }
  const root = path.join(repo, packageRelative);
  assertHash(path.join(root, 'rounds/ROUND-0002/RELEASE.json'), manifest.expected_hashes.release_sha256, 'ROUND2_COMPLETED_RELEASE');
  for (const [name, expected] of Object.entries(manifest.expected_hashes)) if (name !== 'release_sha256') assertHash(path.join(root, name.replace('_sha256', '').split('_').map(value => value.toUpperCase()).join('-') + '.json'), expected, `ROUND2_COMPLETED_${name}`);
  const normalDispatch = validateDispatchReceipt(repo, ROUND2_RELEASE_RECEIPT_PATHS.normal_dispatch, 'normal', candidate, {allowUnverifiedFixture});
  const seniorDispatch = validateDispatchReceipt(repo, ROUND2_RELEASE_RECEIPT_PATHS.senior_dispatch, 'senior', candidate, {allowUnverifiedFixture});
  if (normalDispatch.agent_id === seniorDispatch.agent_id) throw Error('ROUND2_RELEASE_REVIEWER_INDEPENDENCE');
  const gate = evaluateRound2ReleaseReviewGate(repo, {candidateOverride: candidate, allowUnverifiedFixture});
  if (!gate.satisfied) throw Error(gate.reason || 'ROUND2_RELEASE_COMPLETED_EVIDENCE_REQUIRED');
  return gate.provenance;
}

export async function materializeRound2CompletedFixture(root = here) {
  const {pending} = validateRound2PendingRelease(root, path.resolve(root, '..', '..', '..', '..'));
  const derived = deriveRound2Fixture(root), tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round2-completed-fixture-'));
  const packageTmp = path.join(tmp, packageRelative); fs.cpSync(root, packageTmp, {recursive: true});
  fs.mkdirSync(path.dirname(path.join(tmp, taskRelative)), {recursive: true});
  fs.cpSync(path.join(path.resolve(root, '..', '..', '..', '..'), taskRelative), path.join(tmp, taskRelative), {recursive: true});
  const writeCompleted = () => {
    fs.writeFileSync(path.join(packageTmp, 'rounds/ROUND-0002/RELEASE.json'), derived.releaseBytes);
    for (const [name, doc] of Object.entries(derived.documents)) fs.writeFileSync(path.join(packageTmp, name), jsonBytes(doc));
    fs.rmSync(path.join(packageTmp, 'PENDING-RELEASE.json'), {force: true});
  };
  writeCompleted();
  const first = Object.fromEntries(['rounds/ROUND-0002/RELEASE.json', ...Object.keys(derived.documents)].map(name => [name, sha256(fs.readFileSync(path.join(packageTmp, name))) ]));
  writeCompleted();
  const second = Object.fromEntries(Object.keys(first).map(name => [name, sha256(fs.readFileSync(path.join(packageTmp, name))) ]));
  if (JSON.stringify(first) !== JSON.stringify(second)) throw Error('ROUND2_COMPLETED_FIXTURE_NOT_IDEMPOTENT');
  for (const [name, expected] of Object.entries(pending.expected_hashes)) {
    const file = name === 'release_sha256' ? path.join(packageTmp, 'rounds/ROUND-0002/RELEASE.json') : path.join(packageTmp, name.replace('_sha256', '').split('_').map(value => value.toUpperCase()).join('-') + '.json');
    assertHash(file, expected, `ROUND2_COMPLETED_FIXTURE_${name}`);
  }
  const {checkReplay} = await import('./replay.mjs'), {runPreflight} = await import('./preflight.mjs');
  const observed = [];
  for (let attempt = 1; attempt <= 2; attempt += 1) {
    const replayResult = checkReplay(packageTmp, {allowUnverifiedFixture: true}), preflightResult = runPreflight(packageTmp, {allowUnverifiedFixture: true});
    const documentHashes = Object.fromEntries(['ACTIVE-FRAME.json','LINEAGE.json','RESERVE-STATE.json','ROUND-INDEX.json','RELEASE-STATE.json','EXPERIMENT.json'].map(name => [name, sha256(fs.readFileSync(path.join(packageTmp, name)))]));
    observed.push({attempt, replay: replayResult, preflight: preflightResult, document_hashes: documentHashes});
  }
  if (JSON.stringify(observed[0].document_hashes) !== JSON.stringify(observed[1].document_hashes) || observed.some(item => item.preflight.decision !== 'NO_GO_ROUND_0002_RELEASE_REVIEW_INVALID' || item.preflight.static_integrity !== 'FAIL_CLOSED' || item.preflight.completed_rounds !== 2)) throw Error('ROUND2_COMPLETED_PUBLIC_REPLAY_OBSERVATION');
  return {tmp, package_root: packageTmp, expected_hashes: pending.expected_hashes, observed};
}

export function materializeRound2Release(repo = repoDefault, {fail_after = null, allow_unverified_fixture = false} = {}) {
  if (fail_after !== null && !ROUND2_MATERIALIZATION_BOUNDARIES.includes(fail_after)) throw Error('ROUND2_MATERIALIZATION_UNKNOWN_FAILURE_BOUNDARY');
  const inject = boundary => { if (fail_after === boundary) throw Error(`ROUND2_MATERIALIZATION_INJECTED_FAILURE:${boundary}`); };
  const root = path.join(repo, packageRelative), releasePath = path.join(repo, ROUND2_RELEASE_PATHS.release), pendingPath = path.join(repo, ROUND2_RELEASE_PATHS.pending);
  if (!fs.existsSync(pendingPath) && fs.existsSync(releasePath)) {
    const manifest = readCanonical(path.join(repo, ROUND2_RELEASE_PATHS.manifest), 'ROUND2_MATERIALIZED_CANDIDATE').parsed, expected = manifest.expected_hashes;
    if (sha256(fs.readFileSync(releasePath)) !== expected.release_sha256) throw Error('ROUND2_MATERIALIZED_RELEASE_DRIFT');
    for (const [name, expectedHash] of Object.entries(expected)) if (name !== 'release_sha256') { const file = path.join(root, name.replace('_sha256', '').split('_').map(value => value.toUpperCase()).join('-') + '.json'); assertHash(file, expectedHash, `ROUND2_MATERIALIZED_${name}`); }
    const state = readCanonical(path.join(root, 'RELEASE-STATE.json'), 'ROUND2_MATERIALIZED_RELEASE_STATE').parsed;
    if (state.status !== 'ROUND_0002_RELEASED_ROUND_0003_AUDIT_NOT_AUTHORIZED' || state.completed_rounds !== 2) throw Error('ROUND2_MATERIALIZED_STATE');
    return {status: 'ALREADY_MATERIALIZED_IDEMPOTENT', expected_hashes: expected};
  }
  const {pending} = validateRound2PendingRelease(root, repo), review = evaluateRound2ReleaseReviewGate(repo, {allowUnverifiedFixture: allow_unverified_fixture});
  if (!review.satisfied) throw Error(`ROUND2_RELEASE_MATERIALIZATION_REVIEW_REQUIRED:${review.reason}`);
  const derived = deriveRound2Fixture(root), targets = new Map([[releasePath, derived.releaseBytes], ...Object.entries(derived.documents).map(([name, doc]) => [path.join(root, name), jsonBytes(doc)])]);
  let transaction = null;
  const backups = new Map(), installed = [];
  try {
    transaction = fs.mkdtempSync(path.join(root, '.round2-release-transaction-'));
    inject('after_create_transaction');
    let stageIndex = 1;
    for (const [target, bytes] of targets) {
      const staged = path.join(transaction, sha256(Buffer.from(target)));
      fs.writeFileSync(staged, bytes);
      if (sha256(fs.readFileSync(staged)) !== sha256(bytes)) throw Error('ROUND2_MATERIALIZATION_STAGE_HASH');
      inject(ROUND2_MATERIALIZATION_BOUNDARIES[stageIndex]); stageIndex += 1;
    }
    // ROUND-0002/RELEASE.json is new in the pending fixture, so only the six
    // derived documents have backup rename boundaries.  A pre-existing
    // release takes the idempotent path above and never enters this transaction.
    let backupIndex = 8;
    for (const target of targets.keys()) if (fs.existsSync(target)) {
      const backup = path.join(transaction, `backup-${sha256(Buffer.from(target))}`);
      fs.renameSync(target, backup); backups.set(target, backup);
      inject(ROUND2_MATERIALIZATION_BOUNDARIES[backupIndex]); backupIndex += 1;
    }
    let installedIndex = 0;
    for (const [target] of targets) { fs.mkdirSync(path.dirname(target), {recursive: true}); fs.renameSync(path.join(transaction, sha256(Buffer.from(target))), target); installed.push(target); inject(ROUND2_MATERIALIZATION_BOUNDARIES[backupIndex + installedIndex]); installedIndex += 1; }
    const pendingBackup = path.join(transaction, 'PENDING-RELEASE.json'); fs.renameSync(pendingPath, pendingBackup); backups.set(pendingPath, pendingBackup);
    inject(ROUND2_MATERIALIZATION_BOUNDARIES[backupIndex + installedIndex]);
    for (const [name, expected] of Object.entries(pending.expected_hashes)) { const file = name === 'release_sha256' ? releasePath : path.join(root, name.replace('_sha256', '').split('_').map(value => value.toUpperCase()).join('-') + '.json'); assertHash(file, expected, `ROUND2_MATERIALIZED_${name}`); }
    fs.rmSync(transaction, {recursive: true, force: true});
    return {status: 'ROUND_0002_RELEASED_ROUND_0003_AUDIT_NOT_AUTHORIZED', review_gate_sha256: review.provenance.gate_sha256, expected_hashes: pending.expected_hashes};
  } catch (error) {
    for (const target of installed.reverse()) fs.rmSync(target, {force: true});
    for (const [target, backup] of backups) if (fs.existsSync(backup)) fs.renameSync(backup, target);
    if (transaction) fs.rmSync(transaction, {recursive: true, force: true}); throw error;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const command = process.argv[2];
  if (command === 'generate') console.log(JSON.stringify(generateRound2ReleaseCandidate(), null, 2));
  else if (command === 'check') console.log(JSON.stringify(validateRound2PendingRelease(), null, 2));
  else if (command === 'materialize') console.log(JSON.stringify(materializeRound2Release(), null, 2));
  else throw Error('usage: node round-0002-release.mjs generate|check|materialize');
}
