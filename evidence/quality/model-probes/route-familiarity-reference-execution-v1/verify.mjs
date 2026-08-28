#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {EXPECTED_COUNTS, rawEvidence, readJson, sha256Bytes, sha256ConcatenatedFiles, sha256File, unexpectedStatusPaths, validateCandidateProvenance, validateCorrectionClaims, walkFiles} from "./correction-lib.mjs";
import {EXECUTOR_FIXTURE_SHA256, requestBytes, schemaFile, shardFile, validateCandidate} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const predecessor = path.join(repo, "evidence/quality/model-probes/route-familiarity-reference-collection-v1");
const errors = [];
const fail = (condition, message) => { if (!condition) errors.push(message); };
const contractPath = path.join(here, "RUN-CONTRACT.json");
const contract = readJson(contractPath);
const manifest = readJson(path.join(predecessor, "LOCAL-ROUTE-MANIFEST.json"));
const correction = readJson(path.join(here, "CORRECTION.json"));
const attemptLineage = readJson(path.join(here, "ATTEMPT-LINEAGE.json"));
const harnessLineage = readJson(path.join(here, "HARNESS-LINEAGE.json"));
const report = readJson(path.join(here, "RUN-REPORT.json"));
const experiment = readJson(path.join(here, "EXPERIMENT.json"));
const historicalTestRunnerLimitation = "The contracted historical test-runner.mjs revision is hash-bound by RUN-CONTRACT.json, but its historical preimage bytes are unavailable and unverifiable in this persistent package; exact preimage reconstruction is not claimed.";

fail(contract.status === "FROZEN_PRE_INFERENCE" && contract.baseline_commit === "d94e2d51e7fe7fd8162e4c0666a2df1102e81426" && contract.cells.length === 20, "frozen contract drift");
fail(correction.attempt_lineage.sha256 === sha256File(path.join(here, correction.attempt_lineage.file)), "attempt lineage binding drift");
fail(correction.harness_lineage.sha256 === sha256File(path.join(here, correction.harness_lineage.file)), "harness lineage binding drift");
fail(report.correction.sha256 === sha256File(path.join(here, report.correction.file)), "report correction binding drift");
fail(experiment.run_report.sha256 === sha256File(path.join(here, experiment.run_report.file)), "experiment report binding drift");
errors.push(...validateCorrectionClaims({correction, report, experiment, manifest, harnessLineage}));
fail(harnessLineage.placeholder_exact_schema_bytes_marker_is_preimage_evidence === false && /producing runner preimage/u.test(harnessLineage.transport_schema_preimage_policy), "transport-schema preimage policy drift");

for (const [name, binding] of Object.entries(contract.predecessor_artifacts)) {
  const file = path.join(predecessor, name);
  fail(fs.existsSync(file) && sha256File(file) === binding.sha256 && fs.statSync(file).size === binding.size_bytes, `${name}: predecessor binding drift`);
}
const predecessorDiff = spawnSync("git", ["diff", "--exit-code", contract.baseline_commit, "--", "evidence/quality/model-probes/route-familiarity-reference-collection-v1"], {cwd:repo, encoding:"utf8"});
fail(predecessorDiff.status === 0, "predecessor package is not byte-identical to baseline");

const manifestLanes = Object.fromEntries(manifest.lanes.map(lane => [lane.lane_id, lane]));
fail(manifestLanes["lane-04"].provider === "Z.ai/GLM" && manifestLanes["lane-04"].model === "opencode-go/glm-5.3", "predecessor lane-04 exact provider/model identity drift");
const ledgerFiles = [];
const computed = {process_invocations:0, exact_frozen_route_process_invocations:0, response_bearing_events:0, excluded_cli_generated_error_payloads:0, confirmed_model_identity_events:0, confirmed_provider_model_identity_events:0, canonical_valid_candidates:0, out_of_protocol_process_invocations:0, unverifiable_historical_transport_preimages:0, schema_not_model_facing_attempts:0};
const rawIdentityByLane = Object.fromEntries(manifest.lanes.map(lane => [lane.lane_id, []]));
for (const attempt of attemptLineage.attempts) {
  computed.process_invocations++;
  if (attempt.protocol_classification === "EXACT_FROZEN_ROUTE_PROCESS_INVOCATION") computed.exact_frozen_route_process_invocations++;
  if (attempt.canonical_valid_candidate) computed.canonical_valid_candidates++;
  if (attempt.protocol_classification === "OUT_OF_PROTOCOL_EXPLORATORY_ROUTE_MISMATCH") computed.out_of_protocol_process_invocations++;
  const dir = path.join(here, attempt.attempt_path);
  const actualFiles = fs.readdirSync(dir).sort();
  fail(JSON.stringify(actualFiles) === JSON.stringify(attempt.immutable_artifacts.map(x => x.file).sort()), `${attempt.attempt_path}: immutable file set drift`);
  for (const artifact of attempt.immutable_artifacts) {
    const file = path.join(dir, artifact.file);
    ledgerFiles.push(path.relative(path.join(here, "attempts"), file));
    fail(sha256File(file) === artifact.sha256 && fs.statSync(file).size === artifact.size_bytes, `${attempt.attempt_path}/${artifact.file}: immutable hash drift`);
  }
  const acquisition = readJson(path.join(dir, "ACQUISITION.json"));
  const raw = rawEvidence(acquisition.lane_id, fs.readFileSync(path.join(dir, "RAW.stdout"), "utf8"));
  if (raw.response_bearing_event) computed.response_bearing_events++;
  computed.excluded_cli_generated_error_payloads += raw.excluded_cli_generated_error_payloads;
  if (raw.confirmed_model_identity_event) computed.confirmed_model_identity_events++;
  if (raw.confirmed_provider_model_identity_event) computed.confirmed_provider_model_identity_events++;
  rawIdentityByLane[acquisition.lane_id].push({attempt_path:attempt.attempt_path, identity:raw.confirmed_runtime_identity});
  fail(attempt.response_bearing_event === raw.response_bearing_event && attempt.response_evidence_status === raw.response_evidence_status && attempt.non_synthetic_model_response_payloads === raw.non_synthetic_model_response_payloads && attempt.excluded_cli_generated_error_payloads === raw.excluded_cli_generated_error_payloads, `${attempt.attempt_path}: response evidence not independently reproduced from RAW`);
  fail(attempt.confirmed_model_identity_event === raw.confirmed_model_identity_event && attempt.confirmed_provider_model_identity_event === raw.confirmed_provider_model_identity_event && JSON.stringify(attempt.confirmed_runtime_identity) === JSON.stringify(raw.confirmed_runtime_identity), `${attempt.attempt_path}: runtime identity not independently reproduced from RAW`);
  fail(JSON.stringify(attempt.recorded_requested_identity) === JSON.stringify({provider:acquisition.requested_provider, model:acquisition.requested_model, effort:acquisition.requested_effort}), `${attempt.attempt_path}: requested identity lineage drift`);
  const call = fs.readFileSync(path.join(dir, "CALL.json"));
  fail(call.equals(fs.readFileSync(path.join(dir, "ACQUISITION.json"))), `${attempt.attempt_path}: CALL/acquisition bytes drift`);
  fail(acquisition.run_contract_sha256 === sha256File(contractPath), `${attempt.attempt_path}: run contract binding drift`);
  const shardNumber = Number(acquisition.shard_id.slice(-2));
  const contractCell = contract.cells.find(cell => cell.cell_id === acquisition.cell_id);
  fail(Boolean(contractCell) && acquisition.request_sha256 === contractCell.request_sha256 && contractCell.request_sha256 === sha256Bytes(requestBytes(here, shardNumber)), `${attempt.attempt_path}: request binding drift`);
  for (const [filename, field] of [["RAW.stdout","raw_stdout"], ["RAW.stderr","raw_stderr"]]) fail(sha256File(path.join(dir, filename)) === acquisition[field].sha256, `${attempt.attempt_path}: ${filename} acquisition hash drift`);
  const candidate = readJson(path.join(dir, "CANDIDATE.json"));
  fail(candidate.canonical_valid_candidate === undefined, `${attempt.attempt_path}: historical candidate was rewritten`);
  const expectedProvenance = {
    qualification: contract.routes[attempt.route_key]?.qualification,
    run_contract_sha256: sha256File(contractPath),
    request_sha256: sha256Bytes(requestBytes(here, shardNumber)),
    prompt_sha256: sha256File(path.join(predecessor, "PROMPT.md")),
    shard_sha256: sha256File(path.join(predecessor, shardFile(shardNumber))),
    schema_sha256: sha256File(path.join(predecessor, schemaFile(shardNumber))),
    acquisition_sha256: sha256File(path.join(dir, "ACQUISITION.json")),
    raw_stdout_sha256: sha256File(path.join(dir, "RAW.stdout")),
    raw_stderr_sha256: sha256File(path.join(dir, "RAW.stderr"))
  };
  for (const error of validateCandidateProvenance({candidate, acquisition, attemptLineage:attempt, contractCell, expected:expectedProvenance}))
    errors.push(`${attempt.attempt_path}: ${error}`);
  if (attempt.canonical_valid_candidate) fail(candidate.valid === true && validateCandidate(here, shardNumber, candidate.response).length === 0, `${attempt.attempt_path}: canonical candidate validation drift`);
  const frozenLane = manifestLanes[acquisition.lane_id];
  fail(attempt.frozen_route_identity.provider === frozenLane.provider && attempt.frozen_route_identity.model === frozenLane.model && attempt.frozen_route_identity.effort === frozenLane.effort, `${attempt.attempt_path}: frozen route identity does not preserve manifest fields`);
  if (acquisition.lane_id === "lane-04") {
    fail(acquisition.requested_provider === "zai-standard-cn" && acquisition.requested_model === "glm-5.3-flash", `${attempt.attempt_path}: recorded Pi requested identity drift`);
    fail(attempt.protocol_classification === "OUT_OF_PROTOCOL_EXPLORATORY_ROUTE_MISMATCH" && attempt.transport_schema.status === "SCHEMA_NOT_MODEL_FACING" && attempt.answer_quality_attribution === false && attempt.downstream_eligible === false, `${attempt.attempt_path}: Pi classification drift`);
    fail(!acquisition.arguments.includes("--json-schema") && !acquisition.arguments.includes("--output-schema"), `${attempt.attempt_path}: Pi schema-facing command contradiction`);
    const events = fs.readFileSync(path.join(dir, "RAW.stdout"), "utf8").split(/\r?\n/u).filter(Boolean).map(JSON.parse);
    const user = events.find(event => event.type === "message_end" && event.message?.role === "user");
    const assistant = events.find(event => event.type === "message_end" && event.message?.role === "assistant");
    const userText = (user?.message?.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
    fail(sha256Bytes(Buffer.from(userText)) === acquisition.request_sha256, `${attempt.attempt_path}: Pi model-facing request replay drift`);
    fail(assistant?.message?.provider === "zai-standard-cn" && assistant?.message?.model === "glm-5.3-flash", `${attempt.attempt_path}: Pi RAW identity drift`);
  } else {
    fail(acquisition.requested_model === frozenLane.model, `${attempt.attempt_path}: frozen model mismatch`);
    if (acquisition.lane_id === "lane-02" && attempt.confirmed_model_identity_event) {
      const init = fs.readFileSync(path.join(dir, "RAW.stdout"), "utf8").split(/\r?\n/u).filter(Boolean).map(line => { try { return JSON.parse(line); } catch { return null; } }).find(event => event?.type === "system" && event.subtype === "init");
      fail(init?.model === "claude-opus-5", `${attempt.attempt_path}: Claude RAW model identity drift`);
    }
  }
  if (attempt.transport_schema.status === "UNVERIFIABLE_HISTORICAL_PREIMAGE") {
    computed.unverifiable_historical_transport_preimages++;
    fail(attempt.transport_schema.historical_preimage === null && attempt.transport_schema.sha256 === undefined, `${attempt.attempt_path}: fabricated transport preimage`);
  } else {
    if (attempt.transport_schema.status === "SCHEMA_NOT_MODEL_FACING") computed.schema_not_model_facing_attempts++;
    fail(acquisition.lane_id === "lane-04" && attempt.transport_schema.status === "SCHEMA_NOT_MODEL_FACING", `${attempt.attempt_path}: historical transport preimage overclaim`);
  }
  if (attempt.historical_parser_replay === "DIRECT_RAW_LAST_MESSAGE_REPLAY_INDEPENDENT_OF_HISTORICAL_PARSER") {
    const replay = JSON.parse(fs.readFileSync(path.join(dir, "RAW.last-message.json"), "utf8"));
    fail(JSON.stringify(replay) === JSON.stringify(candidate.response), `${attempt.attempt_path}: direct RAW replay drift`);
  } else fail(attempt.historical_parser_replay === "UNVERIFIABLE_HISTORICAL_PARSER_PREIMAGE", `${attempt.attempt_path}: parser provenance overclaim`);
}
fail(attemptLineage.attempt_count === attemptLineage.attempts.length && attemptLineage.file_count === ledgerFiles.length, "attempt ledger counts drift");
fail(JSON.stringify(walkFiles(path.join(here, "attempts"))) === JSON.stringify(ledgerFiles.sort()), "unreconciled immutable attempt artifact");
const coreLedgerFiles = ledgerFiles.filter(file => new Set(["ACQUISITION.json", "CALL.json", "CANDIDATE.json", "RAW.stderr", "RAW.stdout"]).has(path.basename(file)));
fail(attemptLineage.core_file_count === 110 && attemptLineage.file_count === 114 && coreLedgerFiles.length === 110, "immutable core/total artifact counts drift");
fail(attemptLineage.core_content_aggregate_sha256 === sha256ConcatenatedFiles(path.join(here, "attempts"), coreLedgerFiles) && attemptLineage.total_content_aggregate_sha256 === sha256ConcatenatedFiles(path.join(here, "attempts"), ledgerFiles), "immutable artifact aggregate hash drift");
for (const key of Object.keys(computed)) fail(computed[key] === EXPECTED_COUNTS[key], `${key}: independently computed count drift`);
const exactCells = new Set(attemptLineage.attempts.filter(a => a.protocol_classification === "EXACT_FROZEN_ROUTE_PROCESS_INVOCATION").map(a => a.cell_id));
fail(exactCells.size === EXPECTED_COUNTS.attempted_exact_frozen_cells, "attempted exact frozen cell count drift");
const outOfProtocolCells = new Set(attemptLineage.attempts.filter(a => a.protocol_classification === "OUT_OF_PROTOCOL_EXPLORATORY_ROUTE_MISMATCH").map(a => a.cell_id));
fail(outOfProtocolCells.size === EXPECTED_COUNTS.out_of_protocol_distinct_cells, "out-of-protocol distinct cell count drift");
fail(correction.frozen_cells.filter(c => c.exact_route_process_invocations > 0 && c.canonical_valid_candidates === 0).length === EXPECTED_COUNTS.attempted_exact_frozen_cells_without_canonical_valid_candidate, "attempted exact frozen cells without valid candidate count drift");
fail(correction.frozen_cells.filter(c => c.status !== "ATTEMPTED_EXACT_FROZEN_ROUTE").length === EXPECTED_COUNTS.uncalled_exact_frozen_cells, "uncalled exact frozen cell count drift");
const recomputedRouteIdentity = Object.fromEntries(manifest.lanes.map(lane => {
  const evidenced = rawIdentityByLane[lane.lane_id].filter(item => item.identity.status !== "NO_CONFIRMED_RUNTIME_IDENTITY");
  const providerModels = evidenced.filter(item => item.identity.status === "PROVIDER_AND_MODEL_VERIFIED");
  const modelOnly = evidenced.filter(item => item.identity.status === "MODEL_ONLY_VERIFIED");
  const evidenceGroup = providerModels.length ? providerModels : modelOnly;
  const first = evidenceGroup[0]?.identity;
  return [lane.lane_id, {
    provider: providerModels.length ? first.provider : null,
    model: first?.model ?? null,
    effort: null,
    status: providerModels.length ? "PROVIDER_AND_MODEL_VERIFIED" : modelOnly.length ? "MODEL_ONLY_VERIFIED" : "NO_CONFIRMED_RUNTIME_IDENTITY",
    evidence_strength: first?.evidence_strength ?? "NONE",
    confirmed_attempt_count: evidenceGroup.length,
    evidence_attempts: evidenceGroup.map(item => item.attempt_path)
  }];
}));
for (const lane of manifest.lanes) fail(JSON.stringify(correction.route_identity_comparison[lane.lane_id].confirmed_runtime_identity) === JSON.stringify(recomputedRouteIdentity[lane.lane_id]), `${lane.lane_id}: route aggregate not independently reproduced from RAW attempts`);
fail(JSON.stringify(report.route_identity_comparison) === JSON.stringify(correction.route_identity_comparison) && JSON.stringify(experiment.route_identity_comparison) === JSON.stringify(correction.route_identity_comparison), "report/experiment route identity summary drift");

for (const [name, entry] of Object.entries(harnessLineage.contract_entries)) {
  fail(entry.contract_sha256 === contract.harness[name].sha256 && entry.contract_size_bytes === contract.harness[name].size_bytes, `${name}: harness contract ledger drift`);
  const current = path.join(here, name);
  const currentMatchesContract = entry.current_sha256 === entry.contract_sha256 && fs.statSync(current).size === entry.contract_size_bytes;
  fail(entry.current_sha256 === sha256File(current) && entry.current_matches_contract === currentMatchesContract, `${name}: current harness binding drift`);
}
fail(harnessLineage.known_preserved_revisions.length === 0, "unavailable historical harness bytes were classified as preserved");
for (const name of ["runner-lib.mjs", "run.mjs", "finalize.mjs", "verify.mjs"]) fail(harnessLineage.contract_entries[name].historical_preimage_status === "UNVERIFIABLE_HISTORICAL_PREIMAGE" && !harnessLineage.contract_entries[name].current_matches_contract, `${name}: historical harness overclaim`);
const testRunnerEntry = harnessLineage.contract_entries["test-runner.mjs"];
const testRunnerHashOnly = harnessLineage.known_hash_only_revisions.find(revision => revision.file === "test-runner.mjs");
fail(testRunnerEntry.historical_preimage_status === "CONTRACT_HASH_BOUND_HISTORICAL_PREIMAGE_UNAVAILABLE" && !testRunnerEntry.current_matches_contract, "test-runner.mjs: historical harness overclaim");
fail(testRunnerHashOnly?.sha256 === testRunnerEntry.contract_sha256 && testRunnerHashOnly?.size_bytes === testRunnerEntry.contract_size_bytes && testRunnerHashOnly?.source === "RUN-CONTRACT.json" && testRunnerHashOnly?.bytes_available === false && testRunnerHashOnly?.exact_preimage_reconstruction_claimed === false, "test-runner.mjs: hash-only lineage binding drift");
fail(harnessLineage.historical_test_runner_preimage_limitation === historicalTestRunnerLimitation, "historical test-runner limitation drift");
for (const document of [correction, report, experiment]) fail(document.unresolved_provenance.includes(historicalTestRunnerLimitation), "historical test-runner limitation missing from derived report");

const taskFiles = walkFiles(here);
for (const relative of taskFiles) {
  const absolute = path.join(here, relative);
  fail(!fs.lstatSync(absolute).isSymbolicLink(), `${relative}: symlink not allowed`);
  const bytes = fs.readFileSync(absolute);
  const text = bytes.toString("utf8");
  const credentialOrPath = /(?:\/home\/yun|\/Users\/[^/]+\/|\/root\/|sk-[A-Za-z0-9_-]{16,}|sk-ant-[A-Za-z0-9_-]+|ya29\.[A-Za-z0-9_-]+|authorization\s*:\s*bearer\s+\S+|"(?:apiKey|api_key|access_token|refresh_token)"\s*:\s*"[^"\n]+"|eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)/iu;
  const sealedMaterial = /"(?:sealed_reference|defect_id|adjudication_conclusion|model_provenance)"\s*:/iu;
  const forbiddenOrchestrationReference = new RegExp(`${["\\.ai", "task"].join("\\/")}|${["CODE", "DIFF", "REVIEW"].join("-")}`, "u");
  fail(!credentialOrPath.test(text), `${relative}: credential value or host absolute path detected`);
  fail(!sealedMaterial.test(text), `${relative}: sealed material detected`);
  if (relative.endsWith(".mjs")) fail(!forbiddenOrchestrationReference.test(text), `${relative}: ignored orchestration dependency reference detected`);
  fail(!text.split("\n").slice(0, -1).some(line => /[ \t\r]$/u.test(line)), `${relative}: trailing whitespace`);
  const allowedNoNewline = new Set([
    "attempts/codex-gpt-5.6-sol-high/SHARD-03/attempt-002/RAW.last-message.json",
    "attempts/codex-gpt-5.6-sol-high/SHARD-04/attempt-001/RAW.last-message.json",
    "attempts/codex-gpt-5.6-sol-high/SHARD-05/attempt-001/RAW.last-message.json"
  ]);
  fail(bytes.length === 0 || bytes.at(-1) === 10 || allowedNoNewline.has(relative), `${relative}: missing final newline`);
}
for (const relative of taskFiles.filter(file => file.endsWith(".json"))) try { JSON.parse(fs.readFileSync(path.join(here, relative), "utf8")); } catch { errors.push(`${relative}: invalid JSON`); }

const fixture = path.join(repo, "evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua");
fail(sha256File(fixture) === EXECUTOR_FIXTURE_SHA256, "executor fixture drift");
const taskRelative = path.relative(repo, here);
const allowedDirtyPaths = new Set(taskFiles.map(relative => path.posix.join(taskRelative, relative)));
const status = spawnSync("git", ["status", "--porcelain=v1", "-z", "--untracked-files=all", "--no-renames"], {cwd:repo, encoding:"utf8"});
const unexpectedDirtyPaths = status.status === 0 ? unexpectedStatusPaths(status.stdout, allowedDirtyPaths) : ["<git-status-failed>"];
fail(status.status === 0 && unexpectedDirtyPaths.length === 0, `repository scope drift: ${unexpectedDirtyPaths.join(", ")}`);
const diff = spawnSync("git", ["diff", "--check"], {cwd:repo, encoding:"utf8"});
fail(diff.status === 0, "git diff --check failed");
if (!process.argv.includes("--skip-tests")) {
  const tests = spawnSync(process.execPath, [path.join(here, "test-runner.mjs")], {cwd:repo, encoding:"utf8"});
  fail(tests.status === 0, "credential-free focused tests failed");
}

const result = {
  schema_version: "route-familiarity-reference-verification-v3",
  status: errors.length ? "FAIL" : "PASS",
  counts: EXPECTED_COUNTS,
  formal_comparison_eligible: false,
  downstream_derivation_mechanically_blocked: true,
  predecessor_byte_identical_to_baseline: predecessorDiff.status === 0,
  immutable_attempt_artifacts_reconciled: errors.every(error => !/immutable|RAW|CALL\/acquisition/u.test(error)),
  historical_test_runner_preimage_limitation: historicalTestRunnerLimitation,
  errors
};
if (process.argv.includes("--write")) fs.writeFileSync(path.join(here, "VERIFICATION.json"), `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
if (errors.length) process.exitCode = 2;
