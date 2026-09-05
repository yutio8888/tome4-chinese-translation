#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {buildSurfaceQueueView} from './surface-queue-view.mjs';
import {validateRound2CompletedReleaseEvidence} from './round-0002-release.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repoDefault = path.resolve(here, '..', '..', '..', '..');
export const PACKAGE_ROOT = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5';
export const TASK_ROOT = '.ai/task/research-gemini-context-counterexample-reviewer-v5';
export const AUTHORIZATION_PATH = `${TASK_ROOT}/ROUND-0003-SURFACE-AUDIT-AUTHORIZATION-001.json`;
export const CANDIDATE_MANIFEST_PATH = `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-IMPLEMENTATION-CANDIDATE-MANIFEST.json`;
export const REVIEW_PATHS = Object.freeze({
  normal: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-NORMAL-REVIEW-001.json`,
  senior: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-SENIOR-REVIEW-001.json`,
  gate: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-REVIEW-GATE-001.json`,
  normal_dispatch: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-NORMAL-DISPATCH-RECEIPT-001.json`,
  senior_dispatch: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-SENIOR-DISPATCH-RECEIPT-001.json`,
  normal_completion: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-NORMAL-COMPLETION-RECEIPT-001.json`,
  senior_completion: `${TASK_ROOT}/ROUND-0003-SURFACE-INPUT-SENIOR-COMPLETION-RECEIPT-001.json`
});
export const ROUND3 = Object.freeze({
  round_id: 'ROUND-0003',
  predecessor_release_sha256: 'a42e2b8b4e497a26a4936558ffdf5816b45dd49b3b0e31d3eb42f969ddd0fd70',
  active_frame_sha256: 'e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3',
  executor_agent_id: 'fb7f99a4-5e91-4f08-8bc2-ed7601b2111b',
  scout_agent_id: '54d5bec8-40e7-4783-b7bd-ab3af234a45d',
  targets: Object.freeze([
    ['V4-D-D05', '5c600589afed143e424216c060b1c3783e61566739dc61a56f220a702d452621'],
    ['V4-C-D06', 'a221c30995cab3709354ed6934c0fcbe2fdfa7ec420af228d46e5e600ff930e8']
  ])
});
export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
const rowKeys = ['neutral_id', 'cohort', 'profile', 'public_source_file', 'revision_id', 'revision_uid', 'selection_rank_sha256', 'normalized_source_sha256', 'normalized_context_sha256'];
export const rowIdentity = row => sha256(jsonBytes(Object.fromEntries(rowKeys.map(key => [key, row[key]]))));

function canonical(file, label) {
  const stat = fs.lstatSync(file); if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`);
  const bytes = fs.readFileSync(file); let parsed; try { parsed = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  if (!bytes.equals(jsonBytes(parsed))) throw Error(`${label}_NONCANONICAL_BYTES`);
  return {bytes, parsed};
}
function readJson(file, label) { return canonical(file, label).parsed; }
function roundDir(root) { return path.join(root, 'rounds', ROUND3.round_id); }
function buildRound3View(repo, queueBytes, activeFrameBytes) { const view = buildSurfaceQueueView({repo, queueBytes, activeFrameBytes}); view.status = 'FROZEN_ROUND_0003_SURFACE_AUDITOR_INPUT_PENDING_REVIEW'; return view; }

export function independentlyVerifyCompleted2(root = here, repo = repoDefault) {
  const release = canonical(path.join(root, 'rounds/ROUND-0002/RELEASE.json'), 'ROUND2_RELEASE');
  const active = canonical(path.join(root, 'ACTIVE-FRAME.json'), 'ACTIVE_FRAME');
  if (sha256(release.bytes) !== ROUND3.predecessor_release_sha256 || sha256(active.bytes) !== ROUND3.active_frame_sha256 || active.parsed.last_completed_round !== 2 || active.parsed.items.length !== 64) throw Error('ROUND3_PREDECESSOR_OR_ACTIVE_HASH');
  const evidence = validateRound2CompletedReleaseEvidence(repo);
  if (evidence?.release_sha256 && evidence.release_sha256 !== ROUND3.predecessor_release_sha256) throw Error('ROUND3_EXTERNAL_RELEASE_EVIDENCE');
  const rows = ROUND3.targets.map(([neutral_id, revision_id]) => active.parsed.items.find(row => row.neutral_id === neutral_id && row.revision_id === revision_id));
  if (rows.some(row => !row) || active.parsed.items.indexOf(rows[0]) >= active.parsed.items.indexOf(rows[1])) throw Error('ROUND3_ACTIVE_HEAD_ORDER');
  return {active: active.parsed, rows};
}

export function buildRound3Authorization(items) {
  return {
    schema_version: 'gemini-context-v5-round-0003-surface-audit-authorization-v1',
    authorization_id: 'V5-ROUND-0003-SURFACE-AUDIT-001', status: 'AUTHORIZED_SURFACE_INPUT_FREEZE_PENDING_INDEPENDENT_DUAL_REVIEW', authorized_by: 'user', round_id: ROUND3.round_id, stage: 'SURFACE',
    executor: {role: 'EXECUTOR', agent_id: ROUND3.executor_agent_id, route: 'normal Codex sole-writer', sole_writer: true},
    scout: {role: 'SCOUT', agent_id: ROUND3.scout_agent_id, status: 'COMPLETED_READ_ONLY_INDEPENDENTLY_VERIFIED', write_authorized: false},
    temporary_review_route: {normal: 'Codex', senior: 'Gemini 3.7 Flash', opus_enabled: false},
    predecessor_release_sha256: ROUND3.predecessor_release_sha256, active_frame_sha256: ROUND3.active_frame_sha256,
    scope: {audit_only_round_0002_replacements: true, item_count: 2, surface_auditor_call_authorized: false, historical_verdicts_or_evidence_disclosed: false, rejected_revisions_disclosed: false, ranks_lineage_reserve_disclosed: false, review_model_reference_disclosed: false, round_0003_release_authorized: false, round_0003_replacement_authorized: false, round_0004_authorized: false, context_authorized: false, model_calls_authorized: false, network_calls_authorized: false},
    audited_replacements: items.map(row => ({neutral_id: row.neutral_id, revision_id: row.revision_id, row_identity_sha256: rowIdentity(row)})),
    required_review_gate: {status: 'REQUIRED', normal_review_path: REVIEW_PATHS.normal, senior_review_path: REVIEW_PATHS.senior, combined_gate_path: REVIEW_PATHS.gate},
    permitted_current_decision: 'NO_GO_ROUND_0003_SURFACE_INPUT_REVIEW_REQUIRED'
  };
}

export function buildRound3SurfaceQueue(items, authorizationBytes) {
  return {schema_version: 'gemini-context-v5-surface-queue-v3', round_id: ROUND3.round_id, stage: 'SURFACE', active_frame_sha256: ROUND3.active_frame_sha256, predecessor_release_sha256: ROUND3.predecessor_release_sha256, authorization_id: 'V5-ROUND-0003-SURFACE-AUDIT-001', authorization_record_path: AUTHORIZATION_PATH, authorization_record_sha256: sha256(authorizationBytes), scope: 'EXACT_ROUND_0002_REPLACEMENTS_ONLY', item_count: 2, items: items.map(row => ({neutral_id: row.neutral_id, revision_id: row.revision_id, row_identity_sha256: rowIdentity(row)}))};
}

function validateAuthorization(repo, queue, expectedItems) {
  const record = canonical(path.join(repo, AUTHORIZATION_PATH), 'ROUND3_AUTHORIZATION'), expected = buildRound3Authorization(expectedItems);
  if (sha256(record.bytes) !== queue.authorization_record_sha256 || !record.bytes.equals(jsonBytes(expected))) throw Error('ROUND3_AUTHORIZATION_BINDING');
  return {path: AUTHORIZATION_PATH, sha256: sha256(record.bytes), record: record.parsed};
}
export function validateRound3SurfaceInput({root = here, repo = repoDefault, queueBytes, viewBytes} = {}) {
  const verified = independentlyVerifyCompleted2(root, repo), queue = JSON.parse(queueBytes), queueCanonical = Buffer.from(queueBytes);
  if (!queueCanonical.equals(jsonBytes(queue))) throw Error('ROUND3_SURFACE_QUEUE_NONCANONICAL');
  const expectedItems = verified.rows.map(row => ({neutral_id: row.neutral_id, revision_id: row.revision_id, row_identity_sha256: rowIdentity(row)}));
  const keys = ['schema_version','round_id','stage','active_frame_sha256','predecessor_release_sha256','authorization_id','authorization_record_path','authorization_record_sha256','scope','item_count','items'];
  if (!exactKeys(queue, keys) || queue.schema_version !== 'gemini-context-v5-surface-queue-v3' || queue.round_id !== ROUND3.round_id || queue.stage !== 'SURFACE' || queue.active_frame_sha256 !== ROUND3.active_frame_sha256 || queue.predecessor_release_sha256 !== ROUND3.predecessor_release_sha256 || queue.authorization_id !== 'V5-ROUND-0003-SURFACE-AUDIT-001' || queue.authorization_record_path !== AUTHORIZATION_PATH || queue.scope !== 'EXACT_ROUND_0002_REPLACEMENTS_ONLY' || queue.item_count !== 2 || JSON.stringify(queue.items) !== JSON.stringify(expectedItems)) throw Error('ROUND3_SURFACE_QUEUE_BINDING');
  const authorization = validateAuthorization(repo, queue, verified.rows);
  const view = JSON.parse(viewBytes), viewCanonical = Buffer.from(viewBytes);
  const expectedView = buildRound3View(repo, queueCanonical, canonical(path.join(root, 'ACTIVE-FRAME.json'), 'ACTIVE_FRAME').bytes);
  if (!viewCanonical.equals(jsonBytes(view)) || !viewCanonical.equals(jsonBytes(expectedView))) throw Error('ROUND3_SURFACE_VIEW_BINDING');
  return {queue, queue_bytes: queueCanonical, queue_sha256: sha256(queueCanonical), view, view_bytes: viewCanonical, view_sha256: sha256(viewCanonical), authorization};
}

const ROUND3_MANIFEST_KEYS = ['schema_version','status','candidate_ref','author_agent_id','round_id','stage','predecessor_release_sha256','active_frame_sha256','coverage_policy','expected_surface_input','current_preflight_decision','lifecycle','recipe','exclusions','files'];
const ROUND3_RECEIPT_KEYS = ['schema_version','round_id','stage','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','agent_created_at','dispatched_at','orchestrator_authorization_scope','expected_permitted_read_only_task','completion_absent','receipt_id','role','agent_id','route','dispatch_id','opus_quota_override'];
const ROUND3_DISPATCH_EXPECTATIONS = Object.freeze({
  normal: {path: REVIEW_PATHS.normal_dispatch, role:'REVIEWER', route:'Codex gpt-5.6-sol xhigh', receipt_role:'NORMAL', dispatch_route:'CODEX', opus_quota_override:false},
  senior: {path: REVIEW_PATHS.senior_dispatch, role:'SENIOR_REVIEWER', route:'Gemini 3.7 Flash high', receipt_role:'SENIOR', dispatch_route:'GEMINI', opus_quota_override:true}
});
const ROUND3_RECEIPT_SCOPE = Object.freeze({candidate_read_only:true, production_materialization:false, derived_state_mutation:false, surface_auditor_call:false, round_0003_release:false, round_0003_replacement:false, round_0004:false});
const UUID_SHAPE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/u;
function canonicalTimestamp(value) { return typeof value === 'string' && !Number.isNaN(Date.parse(value)) && new Date(value).toISOString() === value; }

export function validateRound3CandidateManifest(repo = repoDefault) {
  const actual = canonical(path.join(repo, CANDIDATE_MANIFEST_PATH), 'ROUND3_CANDIDATE_MANIFEST');
  const manifest = actual.parsed, expected = buildRound3CandidateManifest(repo);
  if (!exactKeys(manifest, ROUND3_MANIFEST_KEYS) || manifest.schema_version !== expected.schema_version || manifest.status !== expected.status || manifest.round_id !== ROUND3.round_id || manifest.stage !== 'SURFACE_INPUT' || manifest.author_agent_id !== ROUND3.executor_agent_id || manifest.predecessor_release_sha256 !== ROUND3.predecessor_release_sha256 || manifest.active_frame_sha256 !== ROUND3.active_frame_sha256 || manifest.current_preflight_decision !== 'NO_GO_ROUND_0003_SURFACE_INPUT_REVIEW_REQUIRED' || manifest.recipe !== expected.recipe || JSON.stringify(manifest.coverage_policy) !== JSON.stringify(expected.coverage_policy) || JSON.stringify(manifest.expected_surface_input) !== JSON.stringify(expected.expected_surface_input) || JSON.stringify(manifest.lifecycle) !== JSON.stringify(expected.lifecycle) || JSON.stringify(manifest.exclusions) !== JSON.stringify(expected.exclusions)) throw Error('ROUND3_CANDIDATE_MANIFEST_SCHEMA');
  if (!actual.bytes.equals(jsonBytes(manifest)) || !Array.isArray(manifest.files) || manifest.files.length !== expected.files.length || JSON.stringify(manifest.files) !== JSON.stringify(expected.files)) throw Error('ROUND3_CANDIDATE_MANIFEST_COVERAGE');
  if (manifest.candidate_ref !== expected.candidate_ref || sha256(Buffer.from(manifest.files.map(item => `${item.path}\0${item.sha256}\n`).join(''))) !== manifest.candidate_ref) throw Error('ROUND3_CANDIDATE_MANIFEST_ROOT');
  return {path:CANDIDATE_MANIFEST_PATH, sha256:sha256(actual.bytes), candidate_ref:manifest.candidate_ref, file_count:manifest.files.length, manifest};
}

export function validateRound3DispatchReceipts(repo = repoDefault, candidate = validateRound3CandidateManifest(repo)) {
  const receipts = {};
  for (const [kind, expected] of Object.entries(ROUND3_DISPATCH_EXPECTATIONS)) {
    const label = `ROUND3_${kind.toUpperCase()}_DISPATCH`;
    const record = canonical(path.join(repo, expected.path), label), value = record.parsed;
    const receiptMatch = typeof value.receipt_id === 'string' && value.receipt_id.match(new RegExp(`^V5-ROUND-0003-SURFACE-INPUT-${expected.receipt_role}-DISPATCH-RECEIPT-(\\d{3})$`, 'u'));
    const dispatchMatch = typeof value.dispatch_id === 'string' && value.dispatch_id.match(new RegExp(`^V5-R3-SURFACE-INPUT-DISPATCH-${expected.dispatch_route}-([0-9A-F]{8})-(\\d{3})$`, 'u'));
    if (!exactKeys(value, ROUND3_RECEIPT_KEYS) || value.schema_version !== 'gemini-context-v5-round-0003-surface-input-review-dispatch-receipt-v1' || value.round_id !== ROUND3.round_id || value.stage !== 'SURFACE_INPUT' || value.status !== 'DISPATCHED' || value.candidate_ref !== candidate.candidate_ref || value.candidate_manifest_path !== candidate.path || value.candidate_manifest_sha256 !== candidate.sha256 || !canonicalTimestamp(value.agent_created_at) || !canonicalTimestamp(value.dispatched_at) || Date.parse(value.agent_created_at) > Date.parse(value.dispatched_at) || JSON.stringify(value.orchestrator_authorization_scope) !== JSON.stringify(ROUND3_RECEIPT_SCOPE) || value.expected_permitted_read_only_task !== 'READ_ONLY_REVIEW_OF_ROUND_0003_SURFACE_INPUT_IMPLEMENTATION_CANDIDATE' || value.completion_absent !== true || value.role !== expected.role || !UUID_SHAPE.test(value.agent_id) || value.route !== expected.route || value.opus_quota_override !== expected.opus_quota_override || !receiptMatch || !dispatchMatch || receiptMatch[1] !== dispatchMatch[2] || dispatchMatch[1] !== value.agent_id.slice(0, 8).toUpperCase()) throw Error(`${label}_BINDING`);
    receipts[kind] = {path:expected.path, sha256:sha256(record.bytes), receipt:value};
  }
  if (receipts.normal.receipt.agent_id === receipts.senior.receipt.agent_id || receipts.normal.receipt.receipt_id === receipts.senior.receipt.receipt_id || receipts.normal.receipt.dispatch_id === receipts.senior.receipt.dispatch_id || receipts.normal.receipt.role === receipts.senior.receipt.role || receipts.normal.receipt.route === receipts.senior.receipt.route) throw Error('ROUND3_DISPATCH_INDEPENDENCE');
  return receipts;
}

function walkRegular(repo, relativeRoot) { const out = []; const visit = relative => { const dir = path.join(repo, relative), entries = fs.readdirSync(dir, {withFileTypes: true}).sort((a,b) => Buffer.compare(Buffer.from(a.name), Buffer.from(b.name))); for (const entry of entries) { const child = path.posix.join(relative, entry.name), stat = fs.lstatSync(path.join(repo, child)); if (entry.isSymbolicLink() || stat.isSymbolicLink()) throw Error(`ROUND3_CANDIDATE_SYMLINK:${child}`); if (stat.isDirectory()) visit(child); else if (stat.isFile()) out.push(child); else throw Error(`ROUND3_CANDIDATE_NONREGULAR:${child}`); } }; visit(relativeRoot); return out; }
export const CANDIDATE_EXCLUSIONS = Object.freeze([{path: `${TASK_ROOT}/STATE.json`, reason: 'mutable orchestration state'}, {path: CANDIDATE_MANIFEST_PATH, reason: 'self-reference'}, ...Object.values(REVIEW_PATHS).map((path, index) => ({path, reason: index < 2 ? 'future independent review' : index === 2 ? 'future combined gate' : 'future dispatch/completion receipt'}))]);
export function buildRound3CandidateManifest(repo = repoDefault) { const excluded = new Set(CANDIDATE_EXCLUSIONS.map(item => item.path)); const files = [...walkRegular(repo, TASK_ROOT), ...walkRegular(repo, PACKAGE_ROOT)].filter(file => !excluded.has(file)).sort((a,b) => Buffer.compare(Buffer.from(a),Buffer.from(b))).map(file => ({path: file, sha256: sha256(fs.readFileSync(path.join(repo,file)))})); const candidate_ref = sha256(Buffer.from(files.map(item => `${item.path}\0${item.sha256}\n`).join(''))); return {schema_version:'gemini-context-v5-round-0003-surface-input-implementation-candidate-v1',status:'ROUND_0003_SURFACE_INPUT_FROZEN_PENDING_INDEPENDENT_DUAL_REVIEW',candidate_ref,author_agent_id:ROUND3.executor_agent_id,round_id:ROUND3.round_id,stage:'SURFACE_INPUT',predecessor_release_sha256:ROUND3.predecessor_release_sha256,active_frame_sha256:ROUND3.active_frame_sha256,coverage_policy:{package_root:PACKAGE_ROOT,task_root:TASK_ROOT,policy:'ALL_REGULAR_FILES_EXCEPT_EXACT_EXCLUSIONS',reject_unlisted_relevant_files:true,reject_symlinks:true,reject_nonregular_files:true},expected_surface_input:{item_count:2,queue_path:`${PACKAGE_ROOT}/rounds/ROUND-0003/SURFACE-QUEUE.json`,view_path:`${PACKAGE_ROOT}/rounds/ROUND-0003/SURFACE-QUEUE-VIEW.json`},current_preflight_decision:'NO_GO_ROUND_0003_SURFACE_INPUT_REVIEW_REQUIRED',lifecycle:{surface_auditor_called:false,surface_records_created:false,context_created:false,round_0003_release_created:false,round_0004_created:false,model_calls_started:0,network_calls_made:0},recipe:'SHA256(concatenation in listed order of repo-relative path UTF-8 bytes + NUL + lowercase raw-file SHA-256 ASCII + LF)',exclusions:CANDIDATE_EXCLUSIONS,files}; }

if (import.meta.url === `file://${process.argv[1]}`) { const command = process.argv[2]; if (command === '--check') { const root = here, round = roundDir(root), queue = canonical(path.join(round,'SURFACE-QUEUE.json'),'ROUND3_QUEUE').bytes, view = canonical(path.join(round,'SURFACE-QUEUE-VIEW.json'),'ROUND3_VIEW').bytes; console.log(JSON.stringify(validateRound3SurfaceInput({root,queueBytes:queue,viewBytes:view}),null,2)); } else throw Error('usage: node round-0003-surface-input.mjs --check'); }
