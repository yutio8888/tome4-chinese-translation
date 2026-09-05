import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;
const canonicalSha256 = value => sha256(Buffer.from(JSON.stringify(canonical(value))));
const normalize = value => String(value).normalize('NFKC').replace(/\\[nrt]|\s/gu, ' ').replace(/ +/gu, ' ').trim();
const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
const hex64 = value => typeof value === 'string' && /^[0-9a-f]{64}$/u.test(value);

export const PACKAGE_ROOT = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5';
export const TASK_ROOT = '.ai/task/research-gemini-context-counterexample-reviewer-v5';
export const ROUND2_AUTHORIZATION_PATH = `${TASK_ROOT}/ROUND-0002-SURFACE-AUDIT-AUTHORIZATION-001.json`;
export const ROUND2_CANDIDATE_MANIFEST_PATH = `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-IMPLEMENTATION-CANDIDATE-MANIFEST.json`;
export const ROUND2_REVIEW_PATHS = Object.freeze({
  normal: `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-NORMAL-REVIEW-001.json`,
  senior: `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-SENIOR-REVIEW-001.json`,
  gate: `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-REVIEW-GATE-001.json`
});
export const ROUND2_REPAIR_REVIEW_PATHS = Object.freeze({
  normal: `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-REPAIR-NORMAL-REREVIEW-001.json`,
  senior: `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-REPAIR-SENIOR-REREVIEW-001.json`,
  gate: `${TASK_ROOT}/ROUND-0002-SURFACE-INPUT-REPAIR-REVIEW-GATE-001.json`
});
export const ROUND2_REVIEWED_CANDIDATE = Object.freeze({
  candidate_ref: '241478ba1b304224533660e06f171b609e01b2c7c872cc7358b0efd14cc70f09',
  manifest_sha256: 'b8668b139f15279fda0b48a58fcfb482fb787ac1e1dc6a4cc71e4eb720ac22ed',
  file_count: 102,
  queue_sha256: 'e8947540ff6b430fc8b69202abcb039dc34bbc996bb1fc241f671e280cd6a866',
  view_sha256: '5858861e071b7229cb3ca2ae6f3c6fd0ed972433dab2490c1a848bf4a2788030'
});
export const ROUND2_GATE_TRANSITION_PATHS = Object.freeze([
  `${PACKAGE_ROOT}/round-0002-surface-input.mjs`,
  `${PACKAGE_ROOT}/preflight.mjs`,
  `${PACKAGE_ROOT}/test-round-0002-surface-input.mjs`
]);
export const ROUND1_HASHES = Object.freeze({
  release: 'bf37e1fc2f1015d6c86e0666154338df591d2f556a489b25ba775ccf7ce66119',
  active_frame: 'c632d77064d1d80cd950de263ab3b3970820bed4102cb120900835ae279d1a85',
  lineage: '0fc604bc50220f8accd584f63d7aa5e560d88a2c8a23e43ebb94af3328b9ce7d',
  reserve_state: '123ec9dcd51c96f8843e69e163d25f9765fbdf411e77981ff65b4ecfe36d6eba',
  round_index: '036c80ebcce893be298e833f7aeb27983b95df65043dbc032cdac6480a9f243f',
  release_state: '0378c39116b0e8c30c9089784cc63baa7b7adff5dbfd2d0778dcb0aef7169921',
  experiment: '0440ccb84c6ee3689b8396e8a73d6172bb6bfc9c4a3ba60f686108a116cb0679'
});
export const ROUND2_THREAT_MODEL = Object.freeze({
  mode: 'NON_ADVERSARIAL_REPOSITORY_WORKFLOW',
  protects_against: ['ACCIDENTAL_DRIFT', 'HARNESS_OR_PARSER_ERROR', 'MISSING_EXTRA_SYMLINK_OR_NONCANONICAL_ARTIFACT', 'STALE_OR_INCONSISTENT_HASH_OR_STATE', 'UNAUTHORIZED_PHASE_ADVANCEMENT'],
  out_of_scope: ['MALICIOUS_TAMPERING', 'WHOLE_PACKAGE_REWRITE', 'REVIEWER_IDENTITY_FORGERY', 'VALIDATOR_REWRITE'],
  review_evidence_semantics: 'WORKFLOW_RECORDS_NOT_AUTHENTICITY_PROOFS'
});
export const ROUND2_FORBIDDEN = Object.freeze([
  'SURFACE-RECORDS.json',
  'SURFACE-AGGREGATE.json',
  'CONTEXT-QUEUE.json',
  'CONTEXT-SOURCE-ANCHORS.json',
  'CONTEXT-QUEUE-VIEW.json',
  'CONTEXT-RECORDS.json',
  'CONTEXT-AGGREGATE.json',
  'RELEASE.json',
  'ROUND-0002_REPLACEMENT',
  'ROUND-0003',
  'FORMAL_GEMINI_INFERENCE',
  'MODEL_CALL',
  'NETWORK_CALL',
  'REFERENCE_DISCLOSURE',
  'GIT_STAGE',
  'GIT_HISTORY'
]);
const ROW_KEYS = ['neutral_id', 'cohort', 'profile', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256'];
export const rowIdentity = row => sha256(jsonBytes(Object.fromEntries(ROW_KEYS.map(key => [key, row[key]]))));

function readCanonicalRegular(file, label) {
  const stat = fs.lstatSync(file); if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`);
  const bytes = fs.readFileSync(file); let parsed; try { parsed = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  if (!bytes.equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return {bytes, parsed};
}

export function validateFrozenRound1Files(root) {
  const files = {
    release: 'rounds/ROUND-0001/RELEASE.json', active_frame: 'ACTIVE-FRAME.json', lineage: 'LINEAGE.json', reserve_state: 'RESERVE-STATE.json', round_index: 'ROUND-INDEX.json', release_state: 'RELEASE-STATE.json', experiment: 'EXPERIMENT.json'
  };
  for (const [key, relative] of Object.entries(files)) {
    const file = path.join(root, relative), stat = fs.lstatSync(file);
    if (stat.isSymbolicLink() || !stat.isFile() || sha256(fs.readFileSync(file)) !== ROUND1_HASHES[key]) throw Error(`ROUND1_FROZEN_HASH:${key}`);
  }
  return true;
}

export function deriveRound2QueueItems(state) {
  if (state.round !== 1 || state.lastReleaseSha256 !== ROUND1_HASHES.release) throw Error('ROUND2_PREDECESSOR_STATE');
  const replacements = new Map();
  for (const entry of state.lineage.values()) {
    if (entry.edges.length === 0) continue;
    if (entry.edges.length !== 1 || entry.revisions.length !== 2) throw Error(`ROUND2_LINEAGE_EDGE_COUNT:${entry.neutral_id}`);
    const edge = entry.edges[0];
    if (edge.round_id !== 'ROUND-0001' || edge.edge_ordinal !== 1 || edge.replacement_revision_id !== entry.revisions[1] || edge.rejected_revision_id !== entry.revisions[0]) throw Error(`ROUND2_LINEAGE_EDGE_BINDING:${entry.neutral_id}`);
    replacements.set(entry.neutral_id, edge.replacement_revision_id);
  }
  if (replacements.size !== 10) throw Error('ROUND2_REPLACEMENT_COUNT');
  const items = state.active.filter(row => replacements.has(row.neutral_id)).map(row => {
    if (replacements.get(row.neutral_id) !== row.revision_id) throw Error(`ROUND2_CURRENT_REVISION:${row.neutral_id}`);
    return {neutral_id: row.neutral_id, revision_id: row.revision_id, row_identity_sha256: rowIdentity(row)};
  });
  if (items.length !== 10) throw Error('ROUND2_ACTIVE_REPLACEMENT_COUNT');
  return items;
}

export function buildRound2Authorization(items) {
  return {
    schema_version: 'gemini-context-v5-round-0002-surface-audit-authorization-v1',
    authorization_id: 'V5-ROUND-0002-SURFACE-AUDIT-001',
    status: 'AUTHORIZED_SURFACE_INPUT_FREEZE_PENDING_INDEPENDENT_DUAL_REVIEW',
    authorized_by: 'user',
    round_id: 'ROUND-0002',
    stage: 'SURFACE',
    executor: {role: 'EXECUTOR', agent_id: '95a06041-bdb6-4d72-bd43-415d93994a49', route: 'native Codex fallback', reason: 'The user explicitly designated the current native-Codex agent as the sole writer for V5 ROUND-0002 Stage A; no Paseo EXECUTOR child is created or reused.'},
    scout: {role: 'SCOUT', agent_id: '04cbe36f-3ee3-4f54-9bba-de4a1a581ef9', status: 'COMPLETED_READ_ONLY_DESIGN_HARVESTED', write_authorized: false},
    threat_model: ROUND2_THREAT_MODEL,
    predecessor_release_sha256: ROUND1_HASHES.release,
    active_frame_sha256: ROUND1_HASHES.active_frame,
    lineage_sha256: ROUND1_HASHES.lineage,
    scope: {audit_exact_round_0001_replacements: true, item_count: 10, context_inputs_deferred_until_surface_pass_subset: true, surface_auditor_call_authorized_before_review: false, round_0002_records_or_aggregate_authorized: false, round_0002_context_authorized: false, round_0002_replacement_authorized: false, round_0002_release_authorized: false, round_0003_authorized: false, formal_gemini_inference_authorized: false, model_calls_authorized: false, network_calls_authorized: false},
    audited_replacements: items,
    required_review_gate: {status: 'REQUIRED', normal_review_path: ROUND2_REVIEW_PATHS.normal, senior_review_path: ROUND2_REVIEW_PATHS.senior, combined_gate_path: ROUND2_REVIEW_PATHS.gate},
    permitted_current_decision: 'NO_GO_ROUND_0002_SURFACE_INPUT_REVIEW_REQUIRED',
    forbidden_before_review: ROUND2_FORBIDDEN
  };
}

export function buildRound2SurfaceQueue(items, authorizationBytes) {
  return {
    schema_version: 'gemini-context-v5-surface-queue-v3', round_id: 'ROUND-0002', stage: 'SURFACE',
    active_frame_sha256: ROUND1_HASHES.active_frame, predecessor_release_sha256: ROUND1_HASHES.release,
    authorization_id: 'V5-ROUND-0002-SURFACE-AUDIT-001', authorization_record_path: ROUND2_AUTHORIZATION_PATH,
    authorization_record_sha256: sha256(authorizationBytes), scope: 'EXACT_ROUND_0001_REPLACEMENTS_ONLY', item_count: 10, items
  };
}

function validateAuthorization(repo, queue, expectedItems) {
  const record = readCanonicalRegular(path.join(repo, ROUND2_AUTHORIZATION_PATH), 'ROUND2_AUTHORIZATION');
  if (sha256(record.bytes) !== queue.authorization_record_sha256) throw Error('ROUND2_AUTHORIZATION_HASH');
  const expected = buildRound2Authorization(expectedItems);
  if (!record.bytes.equals(jsonBytes(expected))) throw Error('ROUND2_AUTHORIZATION_BINDING');
  return {path: ROUND2_AUTHORIZATION_PATH, sha256: sha256(record.bytes), record: record.parsed};
}

function validateFrozenView(queueBytes, queue, viewBytes) {
  const view = readCanonicalBuffer(viewBytes, 'ROUND2_SURFACE_VIEW');
  const topKeys = ['schema_version', 'status', 'round_id', 'stage', 'surface_queue_sha256', 'authorization_record_path', 'authorization_record_sha256', 'active_frame_sha256', 'predecessor_release_sha256', 'provenance', 'items'];
  if (!exactKeys(view.parsed, topKeys) || view.parsed.schema_version !== 'gemini-context-v5-surface-queue-view-v2' || view.parsed.status !== 'FROZEN_ROUND_0002_SURFACE_AUDITOR_INPUT_PENDING_REVIEW' || view.parsed.round_id !== 'ROUND-0002' || view.parsed.stage !== 'SURFACE' || view.parsed.surface_queue_sha256 !== sha256(queueBytes) || view.parsed.authorization_record_path !== queue.authorization_record_path || view.parsed.authorization_record_sha256 !== queue.authorization_record_sha256 || view.parsed.active_frame_sha256 !== queue.active_frame_sha256 || view.parsed.predecessor_release_sha256 !== queue.predecessor_release_sha256 || !Array.isArray(view.parsed.items) || view.parsed.items.length !== 10) throw Error('ROUND2_SURFACE_VIEW_BINDING');
  const provenance = view.parsed.provenance;
  if (!exactKeys(provenance, ['fixed_source_commit', 'inventory', 'identity_contract', 'revision_uid_formula', 'revision_id_formula', 'normalization_contract']) || provenance.fixed_source_commit !== '624a67329fe2ad440c5b344785a9c73fcf22ae63' || provenance.identity_contract !== 'tome4-translation-revision-v1' || provenance.inventory?.raw_sha256 !== '1fb97b26457ebda2b6c03be40e3fe6121639fe58046004acee62aa3dc8f6af61' || provenance.inventory?.canonical_array_sha256 !== '6064eba32bc43d3bf7dff40bd83b8d2183e73a5298bf5b0dcc28fb39c6b1d18a') throw Error('ROUND2_SURFACE_VIEW_PROVENANCE');
  const itemKeys = ['neutral_id', 'revision_id', 'revision_uid', 'row_identity_sha256', 'source', 'source_sha256', 'normalized_source_sha256', 'target', 'target_sha256', 'revision_binding_sha256', 'revision_identity'];
  view.parsed.items.forEach((item, index) => {
    const queued = queue.items[index], identity = item.revision_identity;
    if (!exactKeys(item, itemKeys) || !exactKeys(identity, ['identity_contract', 'version', 'tu_uid', 'revision_uid', 'args_order', 'special']) || item.neutral_id !== queued.neutral_id || item.revision_id !== queued.revision_id || item.row_identity_sha256 !== queued.row_identity_sha256 || item.revision_binding_sha256 !== item.revision_id || item.revision_uid !== identity.revision_uid || identity.identity_contract !== provenance.identity_contract || typeof item.source !== 'string' || typeof item.target !== 'string') throw Error(`ROUND2_SURFACE_VIEW_ITEM:${index}`);
    const sourceSha = sha256(Buffer.from(item.source, 'utf8')), targetSha = sha256(Buffer.from(item.target, 'utf8')), normalizedSourceSha = sha256(Buffer.from(normalize(item.source), 'utf8'));
    if (item.source_sha256 !== sourceSha || item.target_sha256 !== targetSha || item.normalized_source_sha256 !== normalizedSourceSha) throw Error(`ROUND2_SURFACE_VIEW_TEXT_HASH:${index}`);
    const revisionUid = sha256(Buffer.from(`rev\0${identity.tu_uid}\0${sourceSha}`, 'utf8'));
    const revisionId = canonicalSha256({identity_contract: identity.identity_contract, version: identity.version, tu_uid: identity.tu_uid, revision_uid: identity.revision_uid, target: item.target, args_order: identity.args_order, special: identity.special});
    if (revisionUid !== item.revision_uid || revisionId !== item.revision_id) throw Error(`ROUND2_SURFACE_VIEW_REVISION_IDENTITY:${index}`);
  });
  return view;
}

function readCanonicalBuffer(value, label) {
  const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value); let parsed; try { parsed = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  if (!bytes.equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return {bytes, parsed};
}

export function validateRound2SurfaceInput({root, repo, state, bundle}) {
  validateFrozenRound1Files(root);
  const inputOnly=bundle?.pending_surface_input===true&&!bundle.surface_records&&!bundle.surface_aggregate;
  const surfaceCompleted=bundle?.pending_surface_stage===true&&bundle.surface_records&&bundle.surface_aggregate;
  const contextInput=bundle?.pending_context_input===true&&bundle.context_queue&&bundle.context_source_anchors&&bundle.context_queue_view;
  const contextResults=bundle?.pending_context_results===true&&bundle.context_queue&&bundle.context_source_anchors&&bundle.context_queue_view&&bundle.context_records&&bundle.context_aggregate;
  if ((!inputOnly&&!surfaceCompleted)||(!(contextInput||contextResults)&&(bundle.context_queue||bundle.context_source_anchors||bundle.context_queue_view||bundle.context_records||bundle.context_aggregate))||bundle.release) throw Error('ROUND2_SURFACE_INPUT_ARTIFACT_SET');
  const queue = readCanonicalBuffer(bundle.surface_queue, 'ROUND2_SURFACE_QUEUE');
  const queueKeys = ['schema_version', 'round_id', 'stage', 'active_frame_sha256', 'predecessor_release_sha256', 'authorization_id', 'authorization_record_path', 'authorization_record_sha256', 'scope', 'item_count', 'items'];
  if (!exactKeys(queue.parsed, queueKeys) || queue.parsed.schema_version !== 'gemini-context-v5-surface-queue-v3' || queue.parsed.round_id !== 'ROUND-0002' || queue.parsed.stage !== 'SURFACE' || queue.parsed.active_frame_sha256 !== ROUND1_HASHES.active_frame || queue.parsed.predecessor_release_sha256 !== ROUND1_HASHES.release || queue.parsed.authorization_id !== 'V5-ROUND-0002-SURFACE-AUDIT-001' || queue.parsed.authorization_record_path !== ROUND2_AUTHORIZATION_PATH || queue.parsed.scope !== 'EXACT_ROUND_0001_REPLACEMENTS_ONLY' || queue.parsed.item_count !== 10 || !Array.isArray(queue.parsed.items) || queue.parsed.items.length !== 10) throw Error('ROUND2_SURFACE_QUEUE_BINDING');
  const expectedItems = deriveRound2QueueItems(state);
  if (JSON.stringify(queue.parsed.items) !== JSON.stringify(expectedItems)) throw Error('ROUND2_SURFACE_QUEUE_CURRENT_REPLACEMENTS');
  const authorization = validateAuthorization(repo, queue.parsed, expectedItems);
  const view = validateFrozenView(queue.bytes, queue.parsed, bundle.surface_queue_view);
  return {queue: queue.parsed, queue_bytes: queue.bytes, queue_sha256: sha256(queue.bytes), view: view.parsed, view_bytes: view.bytes, view_sha256: sha256(view.bytes), authorization};
}

export const ROUND2_CANDIDATE_EXCLUSIONS = Object.freeze([
  {path: `${TASK_ROOT}/STATE.json`, reason: 'mutable orchestration state excluded to avoid candidate churn'},
  {path: ROUND2_CANDIDATE_MANIFEST_PATH, reason: 'self-reference excluded to avoid circular hashing'},
  {path: ROUND2_REPAIR_REVIEW_PATHS.normal, reason: 'future independent repair normal rereview record'},
  {path: ROUND2_REPAIR_REVIEW_PATHS.senior, reason: 'future independent repair senior rereview record'},
  {path: ROUND2_REPAIR_REVIEW_PATHS.gate, reason: 'future combined repair review gate'}
]);

function walkRegular(repo, relativeRoot) {
  const out = [], visit = relative => {
    const dir = path.join(repo, relative), entries = fs.readdirSync(dir, {withFileTypes: true}).sort((a, b) => Buffer.compare(Buffer.from(a.name), Buffer.from(b.name)));
    for (const entry of entries) {
      const child = path.posix.join(relative, entry.name), stat = fs.lstatSync(path.join(repo, child));
      if (entry.isSymbolicLink() || stat.isSymbolicLink()) throw Error(`ROUND2_CANDIDATE_SYMLINK:${child}`);
      if (entry.isDirectory() && stat.isDirectory()) visit(child);
      else if (entry.isFile() && stat.isFile()) out.push(child);
      else throw Error(`ROUND2_CANDIDATE_NONREGULAR:${child}`);
    }
  };
  visit(relativeRoot); return out;
}

export function buildRound2CandidateManifest(repo) {
  const excluded = new Set(ROUND2_CANDIDATE_EXCLUSIONS.map(item => item.path));
  const paths = [...walkRegular(repo, TASK_ROOT), ...walkRegular(repo, PACKAGE_ROOT)].filter(file => !excluded.has(file)).sort((a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b)));
  const files = paths.map(file => ({path: file, sha256: sha256(fs.readFileSync(path.join(repo, file)))}));
  const recipeBytes = Buffer.concat(files.map(item => Buffer.from(`${item.path}\0${item.sha256}\n`)));
  return {
    schema_version: 'gemini-context-v5-round-0002-surface-input-implementation-candidate-v1',
    status: 'ROUND_0002_SURFACE_INPUT_FROZEN_PENDING_INDEPENDENT_DUAL_REVIEW',
    candidate_ref: sha256(recipeBytes),
    author_agent_id: '95a06041-bdb6-4d72-bd43-415d93994a49',
    round_id: 'ROUND-0002',
    stage: 'SURFACE_INPUT',
    threat_model: ROUND2_THREAT_MODEL,
    coverage_policy: {package_root: PACKAGE_ROOT, task_root: TASK_ROOT, policy: 'ALL_REGULAR_FILES_EXCEPT_EXACT_EXCLUSIONS', reject_unlisted_relevant_files: true, reject_symlinks: true, reject_nonregular_files: true},
    frozen_predecessor: ROUND1_HASHES,
    expected_surface_input: {item_count: 10, queue_path: `${PACKAGE_ROOT}/rounds/ROUND-0002/SURFACE-QUEUE.json`, view_path: `${PACKAGE_ROOT}/rounds/ROUND-0002/SURFACE-QUEUE-VIEW.json`},
    current_preflight_decision: 'NO_GO_ROUND_0002_SURFACE_INPUT_REVIEW_REQUIRED',
    lifecycle: {surface_auditor_called: false, surface_records_created: false, surface_aggregate_created: false, context_inputs_created: false, round_0002_replacements_created: false, round_0002_release_created: false, round_0003_created: false, model_calls_started: 0, network_calls_made: 0},
    recipe: 'SHA256(concatenation in listed order of repo-relative path UTF-8 bytes + NUL + lowercase raw-file SHA-256 ASCII + LF)',
    exclusions: ROUND2_CANDIDATE_EXCLUSIONS,
    files
  };
}

export function validateRound2CandidateManifest(repo) {
  const actual = readCanonicalRegular(path.join(repo, ROUND2_CANDIDATE_MANIFEST_PATH), 'ROUND2_CANDIDATE_MANIFEST');
  const lifecycleExists = Object.values(ROUND2_REPAIR_REVIEW_PATHS).map(relative => fs.existsSync(path.join(repo, relative)));
  if (lifecycleExists.some(Boolean)) {
    if (!lifecycleExists.every(Boolean)) throw Error('ROUND2_REPAIR_REVIEW_LIFECYCLE_PARTIAL');
    if (sha256(actual.bytes) !== ROUND2_REVIEWED_CANDIDATE.manifest_sha256 || actual.parsed.candidate_ref !== ROUND2_REVIEWED_CANDIDATE.candidate_ref || actual.parsed.files?.length !== ROUND2_REVIEWED_CANDIDATE.file_count) throw Error('ROUND2_REVIEWED_CANDIDATE_IDENTITY');
    const gate = readCanonicalRegular(path.join(repo, ROUND2_REPAIR_REVIEW_PATHS.gate), 'ROUND2_REPAIR_REVIEW_GATE');
    if (JSON.stringify(gate.parsed.transition_files?.map(item => item.path)) !== JSON.stringify(ROUND2_GATE_TRANSITION_PATHS)) throw Error('ROUND2_GATE_TRANSITION_PATHS');
    const transitions = new Map(gate.parsed.transition_files.map(item => [item.path, item.sha256]));
    for (const item of actual.parsed.files) {
      const expected = transitions.get(item.path) ?? item.sha256;
      const file = path.join(repo, item.path), stat = fs.lstatSync(file);
      if (stat.isSymbolicLink() || !stat.isFile() || sha256(fs.readFileSync(file)) !== expected) throw Error(`ROUND2_REVIEWED_CANDIDATE_FILE:${item.path}`);
    }
    const allowed = new Set([...actual.parsed.files.map(item => item.path), ...actual.parsed.exclusions.map(item => item.path)]);
    const unexpected = [...walkRegular(repo, TASK_ROOT), ...walkRegular(repo, PACKAGE_ROOT)].filter(file => !allowed.has(file));
    if (unexpected.length) throw Error(`ROUND2_REVIEWED_CANDIDATE_EXTRA:${unexpected.join(',')}`);
    return {path: ROUND2_CANDIDATE_MANIFEST_PATH, sha256: sha256(actual.bytes), candidate_ref: actual.parsed.candidate_ref, file_count: actual.parsed.files.length, reviewed_gate_transition: true, gate_path: ROUND2_REPAIR_REVIEW_PATHS.gate, gate_sha256: sha256(gate.bytes)};
  }
  const expected = buildRound2CandidateManifest(repo);
  if (!actual.bytes.equals(jsonBytes(expected))) throw Error('ROUND2_CANDIDATE_MANIFEST_BINDING');
  return {path: ROUND2_CANDIDATE_MANIFEST_PATH, sha256: sha256(actual.bytes), candidate_ref: actual.parsed.candidate_ref, file_count: actual.parsed.files.length};
}
