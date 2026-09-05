import fs from 'node:fs';
import path from 'node:path';
import {
  applyRound,
  buildReleaseV3Bytes,
  evaluateReleaseImplementationReviewGate,
  initialize,
  jsonBytes,
  outputDocuments,
  readInitialPackage,
  readReleaseProvenanceReviewGate,
  RELEASE_AUTHORIZATION_PATH,
  RELEASE_MATERIALIZATION_REVIEW_PATHS,
  RELEASE_THREAT_MODEL,
  RELEASE_THREAT_MODEL_PATH,
  sha256,
  validateReleaseCandidateManifest
} from './round-lineage.mjs';
import {completedExperimentDocument, runPreflight} from './preflight.mjs';

const packageRelative = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5';
const releaseAuthorization = {authorization_id: 'V5-ROUND-0001-REPLACEMENT-RELEASE-IMPLEMENTATION-001', authorization_path: RELEASE_AUTHORIZATION_PATH, authorization_sha256: '87fca3852d57241fa9756cc8ac8269fd27bb4598ee780204bf9cbb15b7410d37', authorized_by: 'user', executor_agent_id: 'f5cc0aa8-b313-4ca7-8f92-191041de73a8'};
const artifactKeys = {'SURFACE-QUEUE.json': 'surface_queue', 'SURFACE-QUEUE-VIEW.json': 'surface_queue_view', 'SURFACE-RECORDS.json': 'surface_records', 'SURFACE-AGGREGATE.json': 'surface_aggregate', 'CONTEXT-QUEUE.json': 'context_queue', 'CONTEXT-SOURCE-ANCHORS.json': 'context_source_anchors', 'CONTEXT-QUEUE-VIEW.json': 'context_queue_view', 'CONTEXT-RECORDS.json': 'context_records', 'CONTEXT-AGGREGATE.json': 'context_aggregate'};

export function writeHarnessRepairReviewBoundary(repo) {
  const candidate = validateReleaseCandidateManifest(repo), manifestSha256 = candidate.manifest_sha256;
  const review = (name, role, agentId) => ({schema_version: 'gemini-context-v5-round-release-harness-repair-review-v1', review_id: `V5-ROUND-0001-RELEASE-HARNESS-REPAIR-${name.toUpperCase()}-REVIEW-001`, round_id: 'ROUND-0001', role, agent_id: agentId, status: 'PASS', candidate_ref: candidate.candidate_ref, candidate_manifest_path: RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest, candidate_manifest_sha256: manifestSha256, findings: [], recorded_at: '2026-08-31T02:00:00Z'});
  const normal = review('normal', 'NORMAL_REVIEWER', '8a195e00-0ec6-4028-ac4f-932fc278eeb4'), senior = review('senior', 'SENIOR_REVIEWER', '82131c76-affd-4613-9769-6aa4ca23db0f'), normalBytes = jsonBytes(normal), seniorBytes = jsonBytes(senior);
  fs.writeFileSync(path.join(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS.normal), normalBytes);
  fs.writeFileSync(path.join(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS.senior), seniorBytes);
  const threatModelSha256 = sha256(fs.readFileSync(path.join(repo, RELEASE_THREAT_MODEL_PATH)));
  const gate = {schema_version: 'gemini-context-v5-round-release-harness-repair-review-gate-v1', gate_id: 'V5-ROUND-0001-RELEASE-HARNESS-REPAIR-DUAL-REREVIEW-GATE-001', round_id: 'ROUND-0001', status: 'SATISFIED_FINAL_DUAL_PASS', candidate_ref: candidate.candidate_ref, candidate_manifest_path: RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest, candidate_manifest_sha256: manifestSha256, authorization: {path: RELEASE_AUTHORIZATION_PATH, sha256: releaseAuthorization.authorization_sha256, authorization_id: releaseAuthorization.authorization_id}, threat_model: {record_path: RELEASE_THREAT_MODEL_PATH, record_sha256: threatModelSha256, mode: RELEASE_THREAT_MODEL.mode}, normal_review: {path: RELEASE_MATERIALIZATION_REVIEW_PATHS.normal, sha256: sha256(normalBytes), agent_id: normal.agent_id, role: normal.role, status: 'PASS'}, senior_review: {path: RELEASE_MATERIALIZATION_REVIEW_PATHS.senior, sha256: sha256(seniorBytes), agent_id: senior.agent_id, role: senior.role, status: 'PASS'}, permitted_action: 'GO_ROUND_0001_RELEASE_MATERIALIZATION_ONLY', forbidden_scope: ['ROUND-0002_AUDIT', 'MODEL_CALL', 'NETWORK_CALL', 'QUALIFICATION', 'MUTATION', 'REFERENCE_DISCLOSURE', 'GIT_STAGE', 'GIT_HISTORY'], recorded_at: '2026-08-31T02:00:00Z'};
  fs.writeFileSync(path.join(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS.gate), jsonBytes(gate));
  const evaluated = evaluateReleaseImplementationReviewGate(repo);
  if (!evaluated.satisfied) throw Error(`TEST_MATERIALIZATION_GATE:${evaluated.reason}`);
  return evaluated.provenance;
}

export function materializeReleaseFixture(repo) {
  const root = path.join(repo, packageRelative), round = path.join(root, 'rounds', 'ROUND-0001'), input = readInitialPackage(root), state = initialize(structuredClone(input.frame), structuredClone(input.reserves));
  const before = runPreflight(root); if (before.decision !== 'GO_ROUND_0001_RELEASE_MATERIALIZATION_ONLY') throw Error(`TEST_MATERIALIZATION_PREFLIGHT:${before.decision}`);
  const bundle = Object.fromEntries(Object.entries(artifactKeys).map(([name, key]) => [key, fs.readFileSync(path.join(round, name))]));
  Object.assign(bundle, {repo: false, review_repo: repo, release_authorization: releaseAuthorization, implementation_review_gate: readReleaseProvenanceReviewGate(repo)});
  bundle.release = buildReleaseV3Bytes(state, bundle); applyRound(state, bundle);
  const docs = outputDocuments(state), experiment = completedExperimentDocument(docs['RELEASE-STATE.json']);
  fs.writeFileSync(path.join(round, 'RELEASE.json'), bundle.release);
  for (const [name, doc] of Object.entries(docs)) fs.writeFileSync(path.join(root, name), jsonBytes(doc));
  fs.writeFileSync(path.join(root, 'EXPERIMENT.json'), jsonBytes(experiment));
  fs.unlinkSync(path.join(root, 'PENDING-RELEASE.json'));
  return {release_sha256: sha256(bundle.release), completed_experiment_sha256: sha256(jsonBytes(experiment)), derived_hashes: Object.fromEntries(Object.entries(docs).map(([name, doc]) => [name, sha256(jsonBytes(doc))]))};
}
