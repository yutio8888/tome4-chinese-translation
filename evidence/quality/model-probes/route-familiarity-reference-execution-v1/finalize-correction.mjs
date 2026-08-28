#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {EXPECTED_COUNTS, frozenRouteIdentities, historicalPreimageStatus, rawEvidence, readJson, sha256ConcatenatedFiles, sha256File, walkFiles} from "./correction-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const predecessor = path.join(repo, "evidence/quality/model-probes/route-familiarity-reference-collection-v1");
const manifest = readJson(path.join(predecessor, "LOCAL-ROUTE-MANIFEST.json"));
const contract = readJson(path.join(here, "RUN-CONTRACT.json"));
const frozen = frozenRouteIdentities(manifest);
const routeKeys = {"lane-01":"codex", "lane-02":"claude", "lane-03":"gemini", "lane-04":"glm"};
const attemptsRoot = path.join(here, "attempts");

const attemptFiles = walkFiles(attemptsRoot);
const coreAttemptFiles = attemptFiles.filter(file => new Set(["ACQUISITION.json", "CALL.json", "CANDIDATE.json", "RAW.stderr", "RAW.stdout"]).has(path.basename(file)));
const attemptDirs = [...new Set(attemptFiles.filter(file => file.endsWith("/ACQUISITION.json")).map(file => path.dirname(file)))].sort();
const attempts = attemptDirs.map(relativeDir => {
  const dir = path.join(attemptsRoot, relativeDir);
  const acquisition = readJson(path.join(dir, "ACQUISITION.json"));
  const candidate = readJson(path.join(dir, "CANDIDATE.json"));
  const immutableArtifacts = fs.readdirSync(dir).sort().map(file => {
    const absolute = path.join(dir, file);
    return {file, sha256: sha256File(absolute), size_bytes: fs.statSync(absolute).size};
  });
  const isPi = acquisition.lane_id === "lane-04";
  const transportSchema = isPi ? {
    status: "SCHEMA_NOT_MODEL_FACING",
    historical_preimage: null,
    canonical_post_validation_sha256: acquisition.schema_sha256
  } : {
    status: "UNVERIFIABLE_HISTORICAL_PREIMAGE",
    historical_preimage: null,
    canonical_post_validation_sha256: acquisition.schema_sha256
  };
  const rawText = fs.readFileSync(path.join(dir, "RAW.stdout"), "utf8");
  const raw = rawEvidence(acquisition.lane_id, rawText);
  const directlyReplayable = acquisition.lane_id === "lane-01" && candidate.valid && immutableArtifacts.some(x => x.file === "RAW.last-message.json");
  return {
    attempt_path: `attempts/${relativeDir}`,
    cell_id: acquisition.cell_id,
    lane_id: acquisition.lane_id,
    route_key: acquisition.route_key,
    shard_id: acquisition.shard_id,
    attempt: acquisition.attempt,
    process_invocation: true,
    protocol_classification: isPi ? "OUT_OF_PROTOCOL_EXPLORATORY_ROUTE_MISMATCH" : "EXACT_FROZEN_ROUTE_PROCESS_INVOCATION",
    frozen_route_identity: frozen[acquisition.lane_id],
    recorded_requested_identity: {provider: acquisition.requested_provider, model: acquisition.requested_model, effort: acquisition.requested_effort},
    confirmed_runtime_identity: raw.confirmed_runtime_identity,
    response_bearing_event: raw.response_bearing_event,
    response_evidence_status: raw.response_evidence_status,
    non_synthetic_model_response_payloads: raw.non_synthetic_model_response_payloads,
    excluded_cli_generated_error_payloads: raw.excluded_cli_generated_error_payloads,
    confirmed_model_identity_event: raw.confirmed_model_identity_event,
    confirmed_provider_model_identity_event: raw.confirmed_provider_model_identity_event,
    canonical_valid_candidate: candidate.valid,
    formal_comparison_eligible: false,
    downstream_eligible: false,
    answer_quality_attribution: isPi ? false : null,
    transport_schema: transportSchema,
    historical_parser_replay: directlyReplayable ? "DIRECT_RAW_LAST_MESSAGE_REPLAY_INDEPENDENT_OF_HISTORICAL_PARSER" : "UNVERIFIABLE_HISTORICAL_PARSER_PREIMAGE",
    immutable_artifacts: immutableArtifacts
  };
});

const attemptLineage = {
  schema_version: "route-familiarity-reference-attempt-lineage-v3",
  status: "FROZEN_CORRECTION_LEDGER",
  immutable_directory: "attempts",
  attempt_count: attempts.length,
  core_file_count: coreAttemptFiles.length,
  file_count: attempts.reduce((sum, item) => sum + item.immutable_artifacts.length, 0),
  aggregate_hash_algorithm: "SHA-256 over concatenated artifact bytes in lexicographically sorted relative-path order; relative paths are not included in the preimage.",
  core_content_aggregate_sha256: sha256ConcatenatedFiles(attemptsRoot, coreAttemptFiles),
  total_content_aggregate_sha256: sha256ConcatenatedFiles(attemptsRoot, attemptFiles),
  attempts
};
fs.writeFileSync(path.join(here, "ATTEMPT-LINEAGE.json"), `${JSON.stringify(attemptLineage, null, 2)}\n`);

const unresolvedHarnessPreimages = new Set(["runner-lib.mjs", "run.mjs", "finalize.mjs", "verify.mjs"]);
const historicalTestRunnerLimitation = "The contracted historical test-runner.mjs revision is hash-bound by RUN-CONTRACT.json, but its historical preimage bytes are unavailable and unverifiable in this persistent package; exact preimage reconstruction is not claimed.";
const contractEntries = Object.fromEntries(Object.entries(contract.harness).map(([name, binding]) => {
  const current = path.join(here, name);
  const currentHash = fs.existsSync(current) ? sha256File(current) : null;
  const currentSize = fs.existsSync(current) ? fs.statSync(current).size : null;
  return [name, {
    contract_sha256: binding.sha256,
    contract_size_bytes: binding.size_bytes,
    current_sha256: currentHash,
    current_matches_contract: currentHash === binding.sha256 && currentSize === binding.size_bytes,
    historical_preimage_status: historicalPreimageStatus({binding, currentHash, currentSize, unavailable:name === "test-runner.mjs", unresolved:unresolvedHarnessPreimages.has(name)})
  }];
}));
const harnessLineage = {
  schema_version: "route-familiarity-reference-harness-lineage-v3",
  status: "INCOMPLETE_HISTORICAL_LINEAGE_TRUTHFULLY_CLASSIFIED",
  run_contract_harness_binds_current_correction_harness: false,
  transport_schema_preimage_policy: "Exact historical transport-schema bytes require immutable exact argument bytes and the producing runner preimage; a placeholder marker is not preimage evidence.",
  placeholder_exact_schema_bytes_marker_is_preimage_evidence: false,
  historical_test_runner_preimage_limitation: historicalTestRunnerLimitation,
  contract_entries: contractEntries,
  known_preserved_revisions: [],
  known_hash_only_revisions: [
    {file:"runner-lib.mjs", sha256:"c65ff55a422d8eda8f2fc2ce8642ebeb28fad4321d04fbc326c00ac3545cb24d", source:"HARNESS-ERRATA-004.json", bytes_available:false},
    {file:"test-runner.mjs", sha256:contract.harness["test-runner.mjs"].sha256, size_bytes:contract.harness["test-runner.mjs"].size_bytes, source:"RUN-CONTRACT.json", bytes_available:false, exact_preimage_reconstruction_claimed:false}
  ],
  canonical_post_validation_binding_is_separate_from_transport_and_parser_lineage: true
};
fs.writeFileSync(path.join(here, "HARNESS-LINEAGE.json"), `${JSON.stringify(harnessLineage, null, 2)}\n`);

const frozenCells = manifest.lanes.flatMap(lane => lane.bindings.map(binding => {
  const exact = attempts.filter(a => a.lane_id === lane.lane_id && a.shard_id === binding.shard_id && a.protocol_classification === "EXACT_FROZEN_ROUTE_PROCESS_INVOCATION");
  const related = attempts.filter(a => a.lane_id === lane.lane_id && a.shard_id === binding.shard_id && a.protocol_classification.startsWith("OUT_OF_PROTOCOL"));
  return {
    cell_id: `${lane.lane_id}-${binding.shard_id.slice(-2)}`,
    lane_id: lane.lane_id,
    route_key: routeKeys[lane.lane_id],
    shard_id: binding.shard_id,
    frozen_identity: frozen[lane.lane_id],
    status: lane.lane_id === "lane-04" ? "UNEXECUTED_EXACT_FROZEN_ROUTE" : exact.length ? "ATTEMPTED_EXACT_FROZEN_ROUTE" : "UNCALLED_EXACT_FROZEN_ROUTE",
    exact_route_process_invocations: exact.length,
    canonical_valid_candidates: exact.filter(attempt => attempt.canonical_valid_candidate).length,
    related_out_of_protocol_process_invocations: related.map(a => a.attempt_path)
  };
}));
const piCalls = attempts.filter(a => a.lane_id === "lane-04").map(a => ({
  attempt_path: a.attempt_path,
  classification: a.protocol_classification,
  transport_schema_status: a.transport_schema.status,
  response_bearing_event: a.response_bearing_event,
  confirmed_model_identity_event: a.confirmed_model_identity_event,
  confirmed_provider_model_identity_event: a.confirmed_provider_model_identity_event,
  answer_quality_attribution: false,
  downstream_eligible: false
}));
const routeIdentityComparison = Object.fromEntries(manifest.lanes.map(lane => {
  const laneAttempts = attempts.filter(attempt => attempt.lane_id === lane.lane_id);
  const evidenced = laneAttempts.filter(attempt => attempt.confirmed_runtime_identity.status !== "NO_CONFIRMED_RUNTIME_IDENTITY");
  const providerModels = evidenced.filter(attempt => attempt.confirmed_runtime_identity.status === "PROVIDER_AND_MODEL_VERIFIED");
  const modelOnly = evidenced.filter(attempt => attempt.confirmed_runtime_identity.status === "MODEL_ONLY_VERIFIED");
  const evidenceGroup = providerModels.length ? providerModels : modelOnly;
  const first = evidenceGroup[0]?.confirmed_runtime_identity;
  const confirmedRuntime = {
    provider: providerModels.length ? first.provider : null,
    model: first?.model ?? null,
    effort: null,
    status: providerModels.length ? "PROVIDER_AND_MODEL_VERIFIED" : modelOnly.length ? "MODEL_ONLY_VERIFIED" : "NO_CONFIRMED_RUNTIME_IDENTITY",
    evidence_strength: first?.evidence_strength ?? "NONE",
    confirmed_attempt_count: evidenceGroup.length,
    evidence_attempts: evidenceGroup.map(attempt => attempt.attempt_path)
  };
  return [lane.lane_id, {
    requested_frozen_identity: frozen[lane.lane_id],
    confirmed_runtime_identity: confirmedRuntime,
    classification: lane.lane_id === "lane-04" ? "OUT_OF_PROTOCOL_EXPLORATORY_ROUTE_MISMATCH" :
      confirmedRuntime.status === "MODEL_ONLY_VERIFIED" ? "REQUESTED_FROZEN_IDENTITY_WITH_MODEL_ONLY_RUNTIME_EVIDENCE" : "REQUESTED_FROZEN_IDENTITY_RUNTIME_UNVERIFIED"
  }];
}));
const correction = {
  schema_version: "route-familiarity-reference-evidence-correction-v3",
  status: "COMPLETE_CORRECTION_OF_INCOMPLETE_HISTORICAL_RECORD",
  counts: EXPECTED_COUNTS,
  terminology: {process_invocation:"A CLI child process was started; this does not imply a provider/model call.", response_bearing_event:"The preserved RAW envelope contains at least one non-synthetic model-response payload. CLI-generated assistant errors marked model=<synthetic> or is_api_error_message=true are excluded.", confirmed_model_identity_event:"The preserved RAW envelope directly identifies a runtime model; a requested model alone is not confirmation.", confirmed_provider_model_identity_event:"The preserved RAW envelope directly identifies both runtime provider and runtime model."},
  route_identity_comparison: routeIdentityComparison,
  frozen_cells: frozenCells,
  pi_calls: piCalls,
  downstream_derivation: {mechanically_blocked:true, four_route_consensus_eligible:false, reference_derivation_eligible:false, scoring_eligible:false, adjudication_eligible:false, formal_comparison_eligible:false},
  attempt_lineage: {file:"ATTEMPT-LINEAGE.json", sha256:sha256File(path.join(here, "ATTEMPT-LINEAGE.json"))},
  harness_lineage: {file:"HARNESS-LINEAGE.json", sha256:sha256File(path.join(here, "HARNESS-LINEAGE.json"))},
  unresolved_provenance: ["Most historical transport-schema preimages are unavailable.", "Historical parser-producing runner-lib revisions are unavailable.", "The frozen run-contract hashes do not bind the current runner-lib.mjs, run.mjs, finalize.mjs, test-runner.mjs, or verify.mjs.", historicalTestRunnerLimitation]
};
fs.writeFileSync(path.join(here, "CORRECTION.json"), `${JSON.stringify(correction, null, 2)}\n`);

const report = {
  schema_version: "route-familiarity-reference-execution-report-v3",
  status: "INCOMPLETE_HISTORICAL_EXECUTION_RECORD",
  historical_attempts_completely_preserved: true,
  experiment_completed: false,
  formal_comparison_eligible: false,
  counts: EXPECTED_COUNTS,
  response_bearing_event_definition: correction.terminology.response_bearing_event,
  excluded_cli_generated_error_payloads: attempts.filter(attempt => attempt.excluded_cli_generated_error_payloads > 0).map(attempt => attempt.attempt_path),
  invalid_or_uncalled_frozen_cells: frozenCells.filter(c => c.canonical_valid_candidates === 0).map(c => c.cell_id),
  canonical_valid_candidates: attempts.filter(a => a.canonical_valid_candidate).map(a => a.attempt_path),
  out_of_protocol_calls: piCalls.map(c => c.attempt_path),
  route_identity_comparison: routeIdentityComparison,
  correction: {file:"CORRECTION.json", sha256:sha256File(path.join(here, "CORRECTION.json"))},
  attempt_lineage: correction.attempt_lineage,
  harness_lineage: correction.harness_lineage,
  reference_derivation_performed: false,
  adjudication_performed: false,
  scoring_performed: false,
  downstream_derivation_mechanically_blocked: true,
  unresolved_provenance: correction.unresolved_provenance
};
fs.writeFileSync(path.join(here, "RUN-REPORT.json"), `${JSON.stringify(report, null, 2)}\n`);
const experiment = {
  schema_version: "route-familiarity-reference-execution-experiment-v3",
  status: report.status,
  experiment_class: "EXPLORATORY_INCOMPLETE_HISTORICAL_EXECUTION_RECORD",
  baseline_commit: contract.baseline_commit,
  planned_frozen_cells: 20,
  formal_comparison_eligible: false,
  counts: EXPECTED_COUNTS,
  response_bearing_event_definition: correction.terminology.response_bearing_event,
  excluded_cli_generated_error_payloads: report.excluded_cli_generated_error_payloads,
  correction: report.correction,
  run_report: {file:"RUN-REPORT.json", sha256:sha256File(path.join(here, "RUN-REPORT.json"))},
  route_identity_comparison: routeIdentityComparison,
  claims: {reference_derived:false, adjudicated:false, scored:false, formal_gold_standard:false, four_route_consensus:false},
  downstream_derivation_mechanically_blocked: true,
  unresolved_provenance: correction.unresolved_provenance
};
fs.writeFileSync(path.join(here, "EXPERIMENT.json"), `${JSON.stringify(experiment, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: report.status, counts: EXPECTED_COUNTS}, null, 2)}\n`);
