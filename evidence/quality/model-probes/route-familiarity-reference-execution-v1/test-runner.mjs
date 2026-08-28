#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {clone, frozenRouteIdentities, historicalPreimageStatus, rawEvidence, readJson, sha256Bytes, sha256File, unexpectedStatusPaths, validateCandidateProvenance, validateCorrectionClaims, walkFiles} from "./correction-lib.mjs";
import {paths, requestBytes, schemaFile, shardFile, validateCandidate} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const predecessor = paths(here).predecessor;
const manifest = readJson(path.join(predecessor, "LOCAL-ROUTE-MANIFEST.json"));
const correction = readJson(path.join(here, "CORRECTION.json"));
const report = readJson(path.join(here, "RUN-REPORT.json"));
const experiment = readJson(path.join(here, "EXPERIMENT.json"));
const harnessLineage = readJson(path.join(here, "HARNESS-LINEAGE.json"));
const contract = readJson(path.join(here, "RUN-CONTRACT.json"));
const attemptLineage = readJson(path.join(here, "ATTEMPT-LINEAGE.json"));
const passed = [];
const assert = (value, message) => { if (!value) throw new Error(message); };
const test = (id, fn) => { fn(); passed.push(id); };

function expectClaimFailure(id, mutate, pattern) {
  test(id, () => {
    const input = {correction:clone(correction), report:clone(report), experiment:clone(experiment), manifest:clone(manifest), harnessLineage:clone(harnessLineage)};
    mutate(input);
    assert(validateCorrectionClaims(input).some(error => pattern.test(error)), `${id}: mutation was accepted`);
  });
}

function realCandidateProvenanceFixture() {
  const attempt = clone(attemptLineage.attempts[0]);
  const dir = path.join(here, attempt.attempt_path);
  const candidate = readJson(path.join(dir, "CANDIDATE.json"));
  const acquisition = readJson(path.join(dir, "ACQUISITION.json"));
  const contractCell = clone(contract.cells.find(cell => cell.cell_id === attempt.cell_id));
  const shardNumber = Number(attempt.shard_id.slice(-2));
  const expected = {
    qualification: contract.routes[attempt.route_key].qualification,
    run_contract_sha256: sha256File(path.join(here, "RUN-CONTRACT.json")),
    request_sha256: sha256Bytes(requestBytes(here, shardNumber)),
    prompt_sha256: sha256File(path.join(predecessor, "PROMPT.md")),
    shard_sha256: sha256File(path.join(predecessor, shardFile(shardNumber))),
    schema_sha256: sha256File(path.join(predecessor, schemaFile(shardNumber))),
    acquisition_sha256: sha256File(path.join(dir, "ACQUISITION.json")),
    raw_stdout_sha256: sha256File(path.join(dir, "RAW.stdout")),
    raw_stderr_sha256: sha256File(path.join(dir, "RAW.stderr"))
  };
  return {candidate:clone(candidate), acquisition:clone(acquisition), attemptLineage:attempt, contractCell, expected};
}

function expectCandidateProvenanceFailure(id, mutate, pattern) {
  test(id, () => {
    const input = realCandidateProvenanceFixture();
    mutate(input);
    assert(validateCandidateProvenance(input).some(error => pattern.test(error)), `${id}: mutation was accepted`);
  });
}

test("CREDENTIAL_FREE_TEST_STRUCTURE", () => {
  const source = fs.readFileSync(fileURLToPath(import.meta.url), "utf8");
  assert(!/makeRuntime\s*\(/u.test(source), "test must not construct a private live-auth runtime");
  assert(!/homedir\s*\(/u.test(source), "test must not inspect the host home");
});

test("EXACT_LANE_04_MANIFEST_IDENTITY", () => {
  const lane = manifest.lanes.find(item => item.lane_id === "lane-04");
  const frozen = frozenRouteIdentities(manifest)["lane-04"];
  assert(lane.provider === "Z.ai/GLM" && lane.model === "opencode-go/glm-5.3", "authoritative manifest lane-04 identity drift");
  assert(frozen.provider === lane.provider && frozen.model === lane.model, "frozen lane-04 identity must preserve exact manifest fields");
});

test("TEST_RUNNER_CONTRACT_HASH_WITH_UNAVAILABLE_PREIMAGE", () => {
  const binding = contract.harness["test-runner.mjs"];
  assert(binding.sha256 === "22a0d34ad91d4201c7fe18f71d22912eff211413f1cabb4f88396aa7db02c82c" && binding.size_bytes === 4189, "historical test-runner contract binding drift");
  assert(historicalPreimageStatus({binding, currentHash:"later-correction", currentSize:0, unavailable:true}) === "CONTRACT_HASH_BOUND_HISTORICAL_PREIMAGE_UNAVAILABLE", "unavailable historical preimage was overclaimed");
  assert(historicalPreimageStatus({binding, currentHash:binding.sha256, currentSize:binding.size_bytes, unavailable:true}) === "PRESERVED_EXACT_CONTRACT_PREIMAGE", "current exact contract bytes were not recognized");
});

test("NO_IGNORED_ORCHESTRATION_REFERENCE_IN_CODE", () => {
  const forbidden = new RegExp(`${["\\.ai", "task"].join("\\/")}|${["CODE", "DIFF", "REVIEW"].join("-")}`, "u");
  for (const relative of walkFiles(here).filter(file => file.endsWith(".mjs"))) {
    assert(!forbidden.test(fs.readFileSync(path.join(here, relative), "utf8")), `${relative}: ignored orchestration reference present`);
  }
});

if (process.env.RFR_SKIP_ISOLATED_FIXTURE !== "1") test("ISOLATED_SPARSE_CHECKOUT_FINALIZE_TEST_VERIFY", () => {
  const sourceRepo = path.resolve(here, "../../../..");
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "rfr-isolated-fixture-"));
  const checkout = path.join(fixtureRoot, "checkout");
  const run = (command, args, options = {}) => {
    const result = spawnSync(command, args, {cwd:checkout, encoding:"utf8", ...options});
    assert(result.status === 0, `${command} ${args.join(" ")} failed: ${result.stderr || result.stdout}`);
  };
  try {
    const cloneResult = spawnSync("git", ["clone", "-q", "--no-checkout", sourceRepo, checkout], {encoding:"utf8"});
    assert(cloneResult.status === 0, `isolated clone failed: ${cloneResult.stderr}`);
    run("git", ["sparse-checkout", "init", "--cone"]);
    run("git", ["sparse-checkout", "set", "evidence/quality/model-probes/route-familiarity-reference-collection-v1", "evidence/quality/model-probes/qwen3-8-27b-agent-roles"]);
    run("git", ["checkout", "-q", "HEAD"]);
    const isolatedHere = path.join(checkout, "evidence/quality/model-probes/route-familiarity-reference-execution-v1");
    fs.cpSync(here, isolatedHere, {recursive:true});
    assert(!fs.existsSync(path.join(checkout, ".ai")), "isolated fixture unexpectedly contains orchestration artifacts");
    const env = {...process.env, RFR_SKIP_ISOLATED_FIXTURE:"1"};
    run(process.execPath, [path.join(isolatedHere, "finalize-correction.mjs")], {env});
    run(process.execPath, [path.join(isolatedHere, "test-runner.mjs")], {env});
    run(process.execPath, [path.join(isolatedHere, "verify.mjs")], {env});
  } finally {
    fs.rmSync(fixtureRoot, {recursive:true, force:true});
  }
});

test("CANONICAL_DRAFT_2020_12_CANDIDATES", () => {
  for (const n of [3, 4, 5]) {
    const schema = readJson(path.join(predecessor, schemaFile(n)));
    assert(schema.$schema === "https://json-schema.org/draft/2020-12/schema", `shard ${n}: canonical dialect drift`);
    const attempt = n === 3 ? 2 : 1;
    const candidate = readJson(path.join(here, `attempts/codex-gpt-5.6-sol-high/SHARD-0${n}/attempt-00${attempt}/CANDIDATE.json`));
    assert(candidate.valid && validateCandidate(here, n, candidate.response).length === 0, `shard ${n}: canonical candidate invalid`);
  }
});

test("UNMODIFIED_REAL_CANDIDATE_PROVENANCE_PASSES", () => {
  assert(validateCandidateProvenance(realCandidateProvenanceFixture()).length === 0, "unmodified real candidate provenance failed");
});

for (const field of ["cell_id", "route_key", "lane_id", "route", "shard_id", "attempt", "qualification"])
  expectCandidateProvenanceFailure(`MUTATION_CANDIDATE_${field.toUpperCase()}_FAILS`, input => { input.candidate[field] = "mutated"; }, new RegExp(`candidate\\.${field}`, "u"));
expectCandidateProvenanceFailure("MUTATION_CANDIDATE_SCHEMA_VERSION_FAILS", input => { input.candidate.schema_version = "candidate-v0"; }, /candidate\.schema_version/u);
expectCandidateProvenanceFailure("MUTATION_CANDIDATE_FORMAL_SCORING_ELIGIBLE_FAILS", input => { input.candidate.formal_scoring_eligible = true; }, /candidate\.formal_scoring_eligible/u);
for (const field of ["run_contract_sha256", "request_sha256", "prompt_sha256", "shard_sha256", "schema_sha256"])
  expectCandidateProvenanceFailure(`MUTATION_CANDIDATE_${field.toUpperCase()}_FAILS`, input => { input.candidate[field] = "0".repeat(64); }, new RegExp(`candidate\\.${field}`, "u"));
expectCandidateProvenanceFailure("MUTATION_COLLUDING_REQUEST_HASH_FAILS", input => { input.candidate.request_sha256 = input.acquisition.request_sha256 = "0".repeat(64); }, /candidate\.request_sha256.*actual frozen bytes/u);
expectCandidateProvenanceFailure("MUTATION_CANDIDATE_ACQUISITION_FILENAME_FAILS", input => { input.candidate.acquisition.file = "CALL.json"; }, /candidate\.acquisition\.file/u);
expectCandidateProvenanceFailure("MUTATION_CANDIDATE_ACQUISITION_HASH_FAILS", input => { input.candidate.acquisition.sha256 = "0".repeat(64); }, /candidate\.acquisition\.sha256/u);
expectCandidateProvenanceFailure("MUTATION_CANDIDATE_RAW_STDOUT_HASH_FAILS", input => { input.candidate.raw_stdout_sha256 = "0".repeat(64); }, /candidate\.raw_stdout_sha256/u);
expectCandidateProvenanceFailure("MUTATION_CANDIDATE_RAW_STDERR_HASH_FAILS", input => { input.candidate.raw_stderr_sha256 = "0".repeat(64); }, /candidate\.raw_stderr_sha256/u);
expectCandidateProvenanceFailure("MUTATION_ACQUISITION_RAW_STDOUT_HASH_FAILS", input => { input.acquisition.raw_stdout.sha256 = "0".repeat(64); }, /candidate\.raw_stdout_sha256/u);
expectCandidateProvenanceFailure("MUTATION_ACQUISITION_RAW_STDERR_HASH_FAILS", input => { input.acquisition.raw_stderr.sha256 = "0".repeat(64); }, /candidate\.raw_stderr_sha256/u);

test("DIRECT_CODEX_RAW_LAST_MESSAGE_REPLAY", () => {
  for (const n of [3, 4, 5]) {
    const attempt = n === 3 ? 2 : 1;
    const dir = path.join(here, `attempts/codex-gpt-5.6-sol-high/SHARD-0${n}/attempt-00${attempt}`);
    const candidate = readJson(path.join(dir, "CANDIDATE.json"));
    const replay = JSON.parse(fs.readFileSync(path.join(dir, "RAW.last-message.json"), "utf8"));
    assert(JSON.stringify(replay) === JSON.stringify(candidate.response), `shard ${n}: direct RAW replay mismatch`);
  }
});

test("RAW_RESPONSE_CLASSIFICATION_EXCLUDES_SYNTHETIC_ERRORS", () => {
  const synthetic = {type:"assistant", is_api_error_message:true, message:{role:"assistant", model:"<synthetic>", content:[{type:"text", text:"generated CLI error"}]}};
  const bothMarkers = rawEvidence("lane-02", `${JSON.stringify(synthetic)}\n`);
  assert(!bothMarkers.response_bearing_event && bothMarkers.response_evidence_status === "CLI_GENERATED_SYNTHETIC_ERROR_EXCLUDED" && bothMarkers.excluded_cli_generated_error_payloads === 1, "synthetic CLI error was counted as a model response");
  const modelMarkerOnly = clone(synthetic);
  modelMarkerOnly.is_api_error_message = false;
  assert(!rawEvidence("lane-02", `${JSON.stringify(modelMarkerOnly)}\n`).response_bearing_event, "model=<synthetic> mutation was counted");
  const errorMarkerOnly = clone(synthetic);
  errorMarkerOnly.message.model = "claude-opus-5";
  assert(!rawEvidence("lane-02", `${JSON.stringify(errorMarkerOnly)}\n`).response_bearing_event, "is_api_error_message mutation was counted");
});

test("RAW_RESPONSE_CLASSIFICATION_ACCEPTS_NON_SYNTHETIC_MODEL_PAYLOAD", () => {
  const response = {type:"assistant", is_api_error_message:false, message:{role:"assistant", model:"claude-opus-5", content:[{type:"text", text:"model response"}]}};
  const evidence = rawEvidence("lane-02", `${JSON.stringify(response)}\n`);
  assert(evidence.response_bearing_event && evidence.response_evidence_status === "NON_SYNTHETIC_MODEL_RESPONSE_PRESENT" && evidence.excluded_cli_generated_error_payloads === 0, "non-synthetic model response was excluded");
});

test("UNSCOPED_STATUS_REJECTS_OUT_OF_SCOPE_UNTRACKED_PATH", () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), "rfr-status-fixture-"));
  try {
    assert(spawnSync("git", ["init", "-q"], {cwd:fixture}).status === 0, "temporary git init failed");
    fs.writeFileSync(path.join(fixture, "allowed.txt"), "allowed\n");
    fs.writeFileSync(path.join(fixture, "out-of-scope.txt"), "unexpected\n");
    const status = spawnSync("git", ["status", "--porcelain=v1", "-z", "--untracked-files=all", "--no-renames"], {cwd:fixture, encoding:"utf8"});
    assert(status.status === 0, "temporary git status failed");
    const unexpected = unexpectedStatusPaths(status.stdout, new Set(["allowed.txt"]));
    assert(JSON.stringify(unexpected) === JSON.stringify(["out-of-scope.txt"]), "out-of-scope untracked path was not detected");
  } finally {
    fs.rmSync(fixture, {recursive:true, force:true});
  }
});

expectClaimFailure("MUTATION_ROUTE_CLASSIFICATION_FAILS", input => { input.correction.route_identity_comparison["lane-04"].classification = "FROZEN_ROUTE_IDENTITY_NO_RECORDED_DRIFT"; }, /protocol classification/u);
expectClaimFailure("MUTATION_ROUTE_IDENTITY_FAILS", input => { input.correction.route_identity_comparison["lane-04"].confirmed_runtime_identity.model = "glm-5.3"; }, /confirmed runtime identity/u);
expectClaimFailure("MUTATION_UNVERIFIED_ROUTE_IDENTITY_FAILS", input => { input.correction.route_identity_comparison["lane-01"].confirmed_runtime_identity.model = "gpt-5.6-sol"; }, /confirmed runtime identity/u);
expectClaimFailure("MUTATION_MODEL_ONLY_PROVIDER_FAILS", input => { input.correction.route_identity_comparison["lane-02"].confirmed_runtime_identity.provider = "Anthropic"; }, /confirmed runtime identity/u);
expectClaimFailure("MUTATION_FROZEN_ROUTE_PROVIDER_FAILS", input => { input.correction.route_identity_comparison["lane-04"].requested_frozen_identity.provider = "opencode-go"; }, /frozen route comparison identity|requested frozen identity/u);
expectClaimFailure("MUTATION_FROZEN_CELL_MODEL_FAILS", input => { input.correction.frozen_cells.find(cell => cell.lane_id === "lane-04").frozen_identity.model = "glm-5.3"; }, /frozen cell identity/u);
expectClaimFailure("MUTATION_TRANSPORT_STATUS_FAILS", input => { input.correction.pi_calls[0].transport_schema_status = "PROVABLE_CANONICAL_HISTORICAL_PREIMAGE"; }, /transport\/attribution/u);
expectClaimFailure("MUTATION_HARNESS_LINEAGE_FAILS", input => { input.harnessLineage.contract_entries["runner-lib.mjs"].historical_preimage_status = "PRESERVED_EXACT_CONTRACT_PREIMAGE"; }, /harness lineage overclaim/u);
expectClaimFailure("MUTATION_TEST_RUNNER_PREIMAGE_STATUS_FAILS", input => { input.harnessLineage.contract_entries["test-runner.mjs"].historical_preimage_status = "SUPERSEDED_CONTRACT_HASH_ONLY"; }, /harness lineage overclaim/u);
expectClaimFailure("MUTATION_DOWNSTREAM_MECHANICAL_BLOCK_FAILS", input => { input.correction.downstream_derivation.mechanically_blocked = false; }, /mechanically_blocked/u);
for (const field of ["four_route_consensus_eligible", "reference_derivation_eligible", "scoring_eligible", "adjudication_eligible", "formal_comparison_eligible"])
  expectClaimFailure(`MUTATION_CORRECTION_${field.toUpperCase()}_FAILS`, input => { input.correction.downstream_derivation[field] = true; }, new RegExp(`correction\\.downstream_derivation\\.${field}`, "u"));
for (const field of ["formal_comparison_eligible", "reference_derivation_performed", "adjudication_performed", "scoring_performed"])
  expectClaimFailure(`MUTATION_REPORT_${field.toUpperCase()}_FAILS`, input => { input.report[field] = true; }, new RegExp(`report\\.${field}`, "u"));
expectClaimFailure("MUTATION_EXPERIMENT_FORMAL_COMPARISON_ELIGIBLE_FAILS", input => { input.experiment.formal_comparison_eligible = true; }, /experiment\.formal_comparison_eligible/u);
for (const field of ["reference_derived", "adjudicated", "scored", "formal_gold_standard", "four_route_consensus"])
  expectClaimFailure(`MUTATION_EXPERIMENT_CLAIM_${field.toUpperCase()}_FAILS`, input => { input.experiment.claims[field] = true; }, new RegExp(`experiment\\.claims\\.${field}`, "u"));

process.stdout.write(`${JSON.stringify({status:"PASS", cases:passed}, null, 2)}\n`);
