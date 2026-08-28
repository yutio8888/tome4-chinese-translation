import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

export const sha256Bytes = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
export const sha256File = file => sha256Bytes(fs.readFileSync(file));
export const sha256ConcatenatedFiles = (root, relativeFiles) => {
  const hash = crypto.createHash("sha256");
  for (const relative of [...relativeFiles].sort()) hash.update(fs.readFileSync(path.join(root, relative)));
  return hash.digest("hex");
};
export const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
export const clone = value => JSON.parse(JSON.stringify(value));

export function rawEvidence(laneId, rawText) {
  const trimmed = rawText.trim();
  let events = [];
  if (trimmed) {
    try {
      events = [JSON.parse(trimmed)];
    } catch {
      events = trimmed.split(/\r?\n/u).filter(Boolean).map(line => JSON.parse(line));
    }
  }
  const syntheticErrors = events.filter(event => event.type === "assistant" && event.message?.role === "assistant" &&
    (event.message.model === "<synthetic>" || event.is_api_error_message === true));
  const modelResponses = events.filter(event => {
    if (event.type === "assistant" && event.message?.role === "assistant") {
      return event.message.model !== "<synthetic>" && event.is_api_error_message !== true &&
        Array.isArray(event.message.content) && event.message.content.length > 0;
    }
    if (event.type === "item.completed" && event.item?.type === "agent_message") return typeof event.item.text === "string" && event.item.text.length > 0;
    if (event.type === "message_end" && event.message?.role === "assistant") return Array.isArray(event.message.content) && event.message.content.length > 0;
    return typeof event.response === "string" && event.response.length > 0;
  });
  const providerModel = events.find(event => event.type === "message_end" && event.message?.role === "assistant" &&
    typeof event.message.provider === "string" && typeof event.message.model === "string");
  const modelOnly = events.find(event => event.type === "system" && event.subtype === "init" && typeof event.model === "string");
  const runtimeIdentity = providerModel ? {
    provider: providerModel.message.provider,
    model: providerModel.message.model,
    effort: null,
    status: "PROVIDER_AND_MODEL_VERIFIED",
    evidence_strength: "PROVIDER_AND_MODEL_RAW_ASSISTANT_MESSAGE",
    evidence_source: ["RAW.stdout:message_end.message.provider+model"]
  } : modelOnly ? {
    provider: null,
    model: modelOnly.model,
    effort: null,
    status: "MODEL_ONLY_VERIFIED",
    evidence_strength: "MODEL_ONLY_RAW_INIT",
    evidence_source: ["RAW.stdout:system.init.model"]
  } : {
    provider: null,
    model: null,
    effort: null,
    status: "NO_CONFIRMED_RUNTIME_IDENTITY",
    evidence_strength: "NONE",
    evidence_source: []
  };
  return {
    response_bearing_event: modelResponses.length > 0,
    response_evidence_status: modelResponses.length > 0 ? "NON_SYNTHETIC_MODEL_RESPONSE_PRESENT" :
      syntheticErrors.length > 0 ? "CLI_GENERATED_SYNTHETIC_ERROR_EXCLUDED" : "NO_NON_SYNTHETIC_MODEL_RESPONSE",
    non_synthetic_model_response_payloads: modelResponses.length,
    excluded_cli_generated_error_payloads: syntheticErrors.length,
    confirmed_runtime_identity: runtimeIdentity,
    confirmed_model_identity_event: runtimeIdentity.model !== null,
    confirmed_provider_model_identity_event: runtimeIdentity.provider !== null && runtimeIdentity.model !== null
  };
}

export function parsePorcelainStatusZ(output) {
  return output.split("\0").filter(Boolean).map(entry => entry.slice(3));
}

export function unexpectedStatusPaths(output, allowedPaths) {
  return parsePorcelainStatusZ(output).filter(file => !allowedPaths.has(file));
}

export function historicalPreimageStatus({binding, currentHash, currentSize, unavailable, unresolved}) {
  const currentMatches = currentHash === binding.sha256 && currentSize === binding.size_bytes;
  if (currentMatches) return "PRESERVED_EXACT_CONTRACT_PREIMAGE";
  if (unavailable) return "CONTRACT_HASH_BOUND_HISTORICAL_PREIMAGE_UNAVAILABLE";
  if (unresolved) return "UNVERIFIABLE_HISTORICAL_PREIMAGE";
  return "SUPERSEDED_CONTRACT_HASH_ONLY";
}

export const EXPECTED_COUNTS = Object.freeze({
  planned_frozen_cells: 20,
  process_invocations: 22,
  exact_frozen_route_process_invocations: 16,
  attempted_exact_frozen_cells: 9,
  attempted_exact_frozen_cells_without_canonical_valid_candidate: 6,
  response_bearing_events: 9,
  excluded_cli_generated_error_payloads: 2,
  confirmed_model_identity_events: 8,
  confirmed_provider_model_identity_events: 6,
  canonical_valid_candidates: 3,
  out_of_protocol_process_invocations: 6,
  out_of_protocol_distinct_cells: 5,
  unverifiable_historical_transport_preimages: 16,
  schema_not_model_facing_attempts: 6,
  uncalled_exact_frozen_cells: 11
});

export function frozenRouteIdentities(manifest) {
  return Object.fromEntries(manifest.lanes.map(lane => [lane.lane_id, {
    lane_id: lane.lane_id,
    provider: lane.provider,
    model: lane.model,
    effort: lane.effort
  }]));
}

export function validateCandidateProvenance({candidate, acquisition, attemptLineage, contractCell, expected}) {
  const errors = [];
  const fail = (condition, field, message) => { if (!condition) errors.push(`candidate.${field}: ${message}`); };
  const same = (field, authoritative, source) => {
    fail(candidate[field] === acquisition[field], field, `does not match acquisition.${field}`);
    fail(acquisition[field] === authoritative, field, `acquisition.${field} does not match ${source}`);
  };
  fail(candidate.schema_version === "route-familiarity-reference-candidate-v1", "schema_version", "unexpected candidate schema");
  same("cell_id", attemptLineage.cell_id, "attempt lineage");
  same("route_key", attemptLineage.route_key, "attempt lineage");
  same("lane_id", attemptLineage.lane_id, "attempt lineage");
  same("route", contractCell.route, "run contract cell");
  same("shard_id", attemptLineage.shard_id, "attempt lineage");
  same("attempt", attemptLineage.attempt, "attempt lineage");
  same("qualification", expected.qualification, "frozen route qualification");
  const candidatePath = `attempts/${candidate.route}/${candidate.shard_id}/attempt-${String(candidate.attempt).padStart(3, "0")}`;
  const acquisitionPath = `attempts/${acquisition.route}/${acquisition.shard_id}/attempt-${String(acquisition.attempt).padStart(3, "0")}`;
  fail(candidatePath === attemptLineage.attempt_path, "identity", "fields do not resolve to the attempt-lineage path");
  fail(acquisitionPath === attemptLineage.attempt_path, "identity", "acquisition fields do not resolve to the attempt-lineage path");
  for (const field of ["cell_id", "route_key", "lane_id", "route", "shard_id"])
    fail(candidate[field] === contractCell[field] && acquisition[field] === contractCell[field], field, "does not match run contract cell");
  fail(candidate.formal_scoring_eligible === false, "formal_scoring_eligible", "must be false");
  for (const field of ["run_contract_sha256", "request_sha256", "prompt_sha256", "shard_sha256", "schema_sha256"]) {
    fail(candidate[field] === acquisition[field], field, `does not match acquisition.${field}`);
    fail(candidate[field] === expected[field], field, "does not match actual frozen bytes");
    if (field !== "run_contract_sha256") fail(contractCell[field] === expected[field], field, "run contract cell does not match actual frozen bytes");
  }
  fail(candidate.acquisition?.file === "ACQUISITION.json", "acquisition.file", "must equal ACQUISITION.json");
  fail(candidate.acquisition?.sha256 === expected.acquisition_sha256, "acquisition.sha256", "does not hash actual ACQUISITION.json bytes");
  for (const [field, acquisitionField, filename, expectedField] of [
    ["raw_stdout_sha256", "raw_stdout", "RAW.stdout", "raw_stdout_sha256"],
    ["raw_stderr_sha256", "raw_stderr", "RAW.stderr", "raw_stderr_sha256"]
  ]) {
    fail(acquisition[acquisitionField]?.file === filename, field, `acquisition.${acquisitionField}.file must equal ${filename}`);
    fail(candidate[field] === acquisition[acquisitionField]?.sha256, field, `does not match acquisition.${acquisitionField}.sha256`);
    fail(candidate[field] === expected[expectedField], field, `does not hash actual ${filename} bytes`);
  }
  return errors;
}

export function validateCorrectionClaims({correction, report, experiment, manifest, harnessLineage}) {
  const errors = [];
  const fail = (condition, message) => { if (!condition) errors.push(message); };
  const frozen = frozenRouteIdentities(manifest);
  fail(JSON.stringify(correction.counts) === JSON.stringify(EXPECTED_COUNTS), "correction count classification drift");
  fail(report.status === "INCOMPLETE_HISTORICAL_EXECUTION_RECORD", "report completion status drift");
  fail(report.formal_comparison_eligible === false, "report.formal_comparison_eligible must remain false");
  for (const key of ["reference_derivation_performed", "adjudication_performed", "scoring_performed"])
    fail(report[key] === false, `report.${key} must remain false`);
  fail(experiment.formal_comparison_eligible === false, "experiment.formal_comparison_eligible must remain false");
  for (const key of ["reference_derived", "adjudicated", "scored", "formal_gold_standard", "four_route_consensus"])
    fail(experiment.claims?.[key] === false, `experiment.claims.${key} must remain false`);
  fail(correction.downstream_derivation.mechanically_blocked === true, "correction.downstream_derivation.mechanically_blocked must remain true");
  for (const key of ["four_route_consensus_eligible", "reference_derivation_eligible", "scoring_eligible", "adjudication_eligible", "formal_comparison_eligible"])
    fail(correction.downstream_derivation[key] === false, `correction.downstream_derivation.${key} must remain false`);
  const lane04 = correction.frozen_cells.filter(cell => cell.lane_id === "lane-04");
  fail(lane04.length === 5 && lane04.every(cell => cell.status === "UNEXECUTED_EXACT_FROZEN_ROUTE"), "lane-04 frozen cells must remain unexecuted");
  fail(frozen["lane-04"].provider === "Z.ai/GLM" && frozen["lane-04"].model === "opencode-go/glm-5.3", "lane-04 authoritative manifest identity drift");
  fail(JSON.stringify(correction.route_identity_comparison["lane-04"].requested_frozen_identity) === JSON.stringify(frozen["lane-04"]), "lane-04 frozen route comparison identity drift");
  fail(lane04.every(cell => JSON.stringify(cell.frozen_identity) === JSON.stringify(frozen["lane-04"])), "lane-04 frozen cell identity drift");
  const expectedRuntime = {
    "lane-01": {provider:null, model:null, effort:null, status:"NO_CONFIRMED_RUNTIME_IDENTITY", evidence_strength:"NONE", confirmed_attempt_count:0, evidence_attempts:[]},
    "lane-02": {provider:null, model:"claude-opus-5", effort:null, status:"MODEL_ONLY_VERIFIED", evidence_strength:"MODEL_ONLY_RAW_INIT", confirmed_attempt_count:2, evidence_attempts:["attempts/claude-opus-5-high-exploratory/SHARD-02/attempt-001", "attempts/claude-opus-5-high-exploratory/SHARD-02/attempt-002"]},
    "lane-03": {provider:null, model:null, effort:null, status:"NO_CONFIRMED_RUNTIME_IDENTITY", evidence_strength:"NONE", confirmed_attempt_count:0, evidence_attempts:[]},
    "lane-04": {provider:"zai-standard-cn", model:"glm-5.3-flash", effort:null, status:"PROVIDER_AND_MODEL_VERIFIED", evidence_strength:"PROVIDER_AND_MODEL_RAW_ASSISTANT_MESSAGE", confirmed_attempt_count:6, evidence_attempts:["attempts/pi-zai-cn-glm-5.3-flash-high/SHARD-01/attempt-001", "attempts/pi-zai-cn-glm-5.3-flash-high/SHARD-02/attempt-001", "attempts/pi-zai-cn-glm-5.3-flash-high/SHARD-03/attempt-001", "attempts/pi-zai-cn-glm-5.3-flash-high/SHARD-03/attempt-002", "attempts/pi-zai-cn-glm-5.3-flash-high/SHARD-04/attempt-001", "attempts/pi-zai-cn-glm-5.3-flash-high/SHARD-05/attempt-001"]}
  };
  for (const laneId of Object.keys(expectedRuntime)) {
    fail(JSON.stringify(correction.route_identity_comparison[laneId].requested_frozen_identity) === JSON.stringify(frozen[laneId]), `${laneId} requested frozen identity drift`);
    fail(JSON.stringify(correction.route_identity_comparison[laneId].confirmed_runtime_identity) === JSON.stringify(expectedRuntime[laneId]), `${laneId} confirmed runtime identity drift`);
  }
  fail(correction.route_identity_comparison["lane-04"].classification === "OUT_OF_PROTOCOL_EXPLORATORY_ROUTE_MISMATCH", "lane-04 protocol classification drift");
  fail(correction.pi_calls.every(call => call.transport_schema_status === "SCHEMA_NOT_MODEL_FACING" && call.answer_quality_attribution === false && call.downstream_eligible === false), "Pi transport/attribution classification drift");
  const unresolved = new Set(["runner-lib.mjs", "run.mjs", "finalize.mjs", "verify.mjs"]);
  for (const name of unresolved) fail(harnessLineage.contract_entries[name]?.historical_preimage_status === "UNVERIFIABLE_HISTORICAL_PREIMAGE" && harnessLineage.contract_entries[name]?.current_matches_contract === false, `${name}: harness lineage overclaim`);
  const testRunner = harnessLineage.contract_entries["test-runner.mjs"];
  fail(testRunner?.historical_preimage_status === "CONTRACT_HASH_BOUND_HISTORICAL_PREIMAGE_UNAVAILABLE" && testRunner?.current_matches_contract === false, "test-runner.mjs: harness lineage overclaim");
  fail(harnessLineage.known_preserved_revisions.length === 0, "unavailable historical harness bytes were classified as preserved");
  return errors;
}

export function walkFiles(root) {
  const out = [];
  const walk = dir => {
    for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
      const absolute = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(absolute);
      else if (entry.isFile()) out.push(path.relative(root, absolute));
    }
  };
  walk(root);
  return out.sort();
}
