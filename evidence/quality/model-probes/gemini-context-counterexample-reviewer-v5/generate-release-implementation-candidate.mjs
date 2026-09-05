#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {
  applyReviewedProvenanceRound,
  buildReviewedProvenanceReleaseV3Bytes,
  initialize,
  RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS,
  RELEASE_IMPLEMENTATION_CANDIDATE_RECIPE,
  RELEASE_MATERIALIZATION_REVIEW_PATHS,
  RELEASE_PROVENANCE_BINDING,
  RELEASE_EXPECTED_AUTHENTIC_HASHES,
  RELEASE_THREAT_MODEL,
  RELEASE_THREAT_MODEL_PATH,
  jsonBytes,
  outputDocuments,
  readInitialPackage,
  readReleaseProvenanceReviewGate,
  sha256,
  validateReleaseCandidateManifest
} from './round-lineage.mjs';
import {completedExperimentDocument} from './preflight.mjs';

const generatorFile = fileURLToPath(import.meta.url);
const here = path.dirname(generatorFile);
const defaultRepo = path.resolve(here, '..', '..', '..', '..');
const packageRoot = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5';
const taskRoot = '.ai/task/research-gemini-context-counterexample-reviewer-v5';
const textCompare = (a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b));
const expectedExclusionPaths = [
  `${taskRoot}/STATE.json`,
  RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest,
  RELEASE_MATERIALIZATION_REVIEW_PATHS.normal,
  RELEASE_MATERIALIZATION_REVIEW_PATHS.senior,
  RELEASE_MATERIALIZATION_REVIEW_PATHS.gate
];
export function deriveAuthenticFixtureHashes(repo) {
  const packageDir = path.join(repo, packageRoot), roundDir = path.join(packageDir, 'rounds', 'ROUND-0001');
  const artifacts = {'SURFACE-QUEUE.json': 'surface_queue', 'SURFACE-QUEUE-VIEW.json': 'surface_queue_view', 'SURFACE-RECORDS.json': 'surface_records', 'SURFACE-AGGREGATE.json': 'surface_aggregate', 'CONTEXT-QUEUE.json': 'context_queue', 'CONTEXT-SOURCE-ANCHORS.json': 'context_source_anchors', 'CONTEXT-QUEUE-VIEW.json': 'context_queue_view', 'CONTEXT-RECORDS.json': 'context_records', 'CONTEXT-AGGREGATE.json': 'context_aggregate'};
  const input = readInitialPackage(packageDir), state = initialize(structuredClone(input.frame), structuredClone(input.reserves));
  const bundle = Object.fromEntries(Object.entries(artifacts).map(([name, key]) => [key, fs.readFileSync(path.join(roundDir, name))]));
  Object.assign(bundle, {repo: false, review_repo: repo, release_authorization: {authorization_id: 'V5-ROUND-0001-REPLACEMENT-RELEASE-IMPLEMENTATION-001', authorization_path: `${taskRoot}/ROUND-0001-REPLACEMENT-RELEASE-AUTHORIZATION-001.json`, authorization_sha256: '87fca3852d57241fa9756cc8ac8269fd27bb4598ee780204bf9cbb15b7410d37', authorized_by: 'user', executor_agent_id: 'f5cc0aa8-b313-4ca7-8f92-191041de73a8'}, implementation_review_gate: readReleaseProvenanceReviewGate(repo)});
  bundle.release = buildReviewedProvenanceReleaseV3Bytes(state, bundle);
  applyReviewedProvenanceRound(state, bundle);
  const docs = outputDocuments(state);
  return {release_sha256: sha256(bundle.release), completed_experiment_sha256: sha256(jsonBytes(completedExperimentDocument(docs['RELEASE-STATE.json']))), active_frame_sha256: sha256(jsonBytes(docs['ACTIVE-FRAME.json'])), lineage_sha256: sha256(jsonBytes(docs['LINEAGE.json'])), reserve_state_sha256: sha256(jsonBytes(docs['RESERVE-STATE.json'])), round_index_sha256: sha256(jsonBytes(docs['ROUND-INDEX.json'])), release_state_sha256: sha256(jsonBytes(docs['RELEASE-STATE.json']))};
}
export function generateReleaseImplementationCandidate({fixturePath, repo = defaultRepo}) {
  if (!fixturePath || !path.isAbsolute(fixturePath)) throw Error('ABSOLUTE_FIXTURE_RESULT_PATH_REQUIRED');
  if (!path.isAbsolute(repo)) throw Error('ABSOLUTE_REPO_PATH_REQUIRED');
  const output = path.join(repo, RELEASE_MATERIALIZATION_REVIEW_PATHS.manifest);
  const excluded = new Set(RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS.map(item => item.path));
  if (RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS.length !== 5 || JSON.stringify([...excluded]) !== JSON.stringify(expectedExclusionPaths)) throw Error('CANDIDATE_EXCLUSIONS_DRIFT');
  const fixtureStat = fs.lstatSync(fixturePath);
  if (fixtureStat.isSymbolicLink() || !fixtureStat.isFile()) throw Error('FIXTURE_RESULT_FILE_TYPE');
  const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
  const fixtureHashes = {
    release_sha256: fixture.release_sha256,
    completed_experiment_sha256: fixture.completed_experiment_sha256,
    active_frame_sha256: fixture.derived_hashes?.['ACTIVE-FRAME.json'],
    lineage_sha256: fixture.derived_hashes?.['LINEAGE.json'],
    reserve_state_sha256: fixture.derived_hashes?.['RESERVE-STATE.json'],
    round_index_sha256: fixture.derived_hashes?.['ROUND-INDEX.json'],
    release_state_sha256: fixture.derived_hashes?.['RELEASE-STATE.json']
  };
  const authenticFixtureHashes = deriveAuthenticFixtureHashes(repo);
  if (JSON.stringify(authenticFixtureHashes) !== JSON.stringify(RELEASE_EXPECTED_AUTHENTIC_HASHES)) throw Error('AUTHENTIC_FIXTURE_DERIVATION_DRIFT');
  if (fixture.status !== 'PASS' || JSON.stringify(fixtureHashes) !== JSON.stringify(authenticFixtureHashes)) throw Error('FIXTURE_RESULT_HASH_MISMATCH');
  const files = [];
  function walk(relative) {
    const absolute = path.join(repo, relative), stat = fs.lstatSync(absolute);
    if (stat.isSymbolicLink()) throw Error(`CANDIDATE_SYMLINK:${relative}`);
    if (stat.isFile()) { if (!excluded.has(relative)) files.push(relative); return; }
    if (!stat.isDirectory()) throw Error(`CANDIDATE_FILE_TYPE:${relative}`);
    for (const name of fs.readdirSync(absolute).sort(textCompare)) walk(`${relative}/${name}`);
  }
  walk(packageRoot); walk(taskRoot); files.sort(textCompare);
  if (files.length !== 87) throw Error(`CANDIDATE_COVERAGE_COUNT:${files.length}`);
  const entries = files.map(relative => ({path: relative, sha256: sha256(fs.readFileSync(path.join(repo, relative)))}));
  const candidateRef = sha256(Buffer.from(entries.map(item => `${item.path}\0${item.sha256}\n`).join('')));
  const threatModelRecord = {path: RELEASE_THREAT_MODEL_PATH, sha256: sha256(fs.readFileSync(path.join(repo, RELEASE_THREAT_MODEL_PATH)))};
  const manifest = {
  schema_version: 'gemini-context-v5-round-release-implementation-candidate-v6',
  status: 'ROUND_0001_RELEASE_AUTHENTIC_PROVENANCE_HARNESS_REPAIR_PENDING_DUAL_REREVIEW',
  candidate_ref: candidateRef,
  base_candidate_ref: RELEASE_PROVENANCE_BINDING.candidate_ref,
  author_agent_id: 'a75b47e3-1906-4aee-9677-3ac3f278d2b3',
  round_id: 'ROUND-0001',
  threat_model: RELEASE_THREAT_MODEL,
  threat_model_record: threatModelRecord,
  review_history: {preserve_prior_review_records: true, superseded_findings: ['V5-RELEASE-R1-SELF-AUTH-001', 'V5-RELEASE-R1-SELF-AUTH-002', 'V5-RELEASE-R1-SELF-AUTH-003', 'PACKAGE_WIDE_COORDINATED_FORGERY_DEMANDS'], disposition: 'OUT_OF_SCOPE_UNDER_USER_CLARIFIED_NON_ADVERSARIAL_THREAT_MODEL', aborted_materialization: {candidate_ref: RELEASE_PROVENANCE_BINDING.candidate_ref, candidate_manifest_sha256: RELEASE_PROVENANCE_BINDING.candidate_manifest_sha256, gate_sha256: RELEASE_PROVENANCE_BINDING.gate_sha256, status: 'ABORTED_BEFORE_WRITES_FIXTURE_VS_PRODUCTION_PROVENANCE_HASH_MISMATCH'}},
  coverage_policy: {package_root: packageRoot, task_root: taskRoot, policy: 'ALL_REGULAR_FILES_EXCEPT_EXACT_EXCLUSIONS', reject_unlisted_relevant_files: true, reject_symlinks: true, reject_nonregular_files: true},
  expected_fixture_hashes: fixtureHashes,
  current_preflight_decision: 'NO_GO_RELEASE_IMPLEMENTATION_REVIEW_REQUIRED',
  real_materialization: {release_created: false, derived_state_mutated: false, round_0002_created: false, model_calls_started: 0, network_calls_made: 0},
  recipe: RELEASE_IMPLEMENTATION_CANDIDATE_RECIPE,
  exclusions: RELEASE_IMPLEMENTATION_CANDIDATE_EXCLUSIONS,
  files: entries
  };
  const manifestBytes = jsonBytes(manifest), manifestSha256 = sha256(manifestBytes);
  fs.writeFileSync(output, manifestBytes);
  const validated = validateReleaseCandidateManifest(repo, candidateRef, manifestSha256);
  if (validated.file_count !== 87) throw Error('GENERATED_CANDIDATE_VALIDATION_COUNT');
  return {status: 'PASS', ...validated, output: path.relative(repo, output)};
}

if (path.resolve(process.argv[1] ?? '') === generatorFile) {
  const args = process.argv.slice(2);
  if (args.length !== 1 && (args.length !== 3 || args[1] !== '--repo')) throw Error('USAGE: generate-release-implementation-candidate.mjs ABSOLUTE_FIXTURE_RESULT_PATH [--repo ABSOLUTE_REPO_PATH]');
  console.log(JSON.stringify(generateReleaseImplementationCandidate({fixturePath: args[0], repo: args.length === 3 ? args[2] : defaultRepo}), null, 2));
}
