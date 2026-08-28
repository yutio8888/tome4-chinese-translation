import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const prelim = process.argv.includes("--prelim");
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const read = name => JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
const frozen = read("FROZEN-HASHES.json");
for (const [name, expected] of Object.entries(frozen.files)) if (sha256File(path.join(here, name)) !== expected) throw new Error(`${name}: frozen hash mismatch`);

const manifest = read("MANIFEST.json");
const reference = read("REFERENCE.json");
const controls = read("SOURCE-CONTROLS.json");
const sourceVerification = read("SOURCE-VERIFICATION.json");
const armInputs = {A: read("HOLDOUT-A.json"), B: read("HOLDOUT-B.json")};
const routes = manifest.routes;
const routeAliases = {
  "codex-gpt-5.6-sol-high": "codex-gpt-5.6-sol-high",
  "claude-opus-5-medium-no-advisor": "claude-opus-5-medium-no-advisor",
  "pi-zai-cn-glm-5.3-flash-high": "pi-zai-cn-glm-5.3-flash-high",
  "agy-gemini-3.7-flash-high": "agy-gemini-3.7-flash-high"
};
const referenceById = new Map(reference.items.map(item => [item.revision_id, item]));
const controlsById = new Map(controls.items.map(item => [item.revision_id, item]));
const inputByArmId = Object.fromEntries(Object.entries(armInputs).map(([arm, input]) => [arm, new Map(input.items.map(item => [item.revision_id, item]))]));
const semanticByCandidate = new Map();
const calls = [];

function occurrences(haystack, needle) {
  const offsets = [];
  let from = 0;
  while (needle && from <= haystack.length) {
    const found = haystack.indexOf(needle, from);
    if (found === -1) break;
    offsets.push(found);
    from = found + Math.max(1, needle.length);
  }
  return offsets;
}

function overlapsAtom(target, targetSpan, atom) {
  const atomOffsets = occurrences(target, atom);
  if (atomOffsets.length !== 1) throw new Error(`sealed atom is not unique: ${atom}`);
  const atomStart = atomOffsets[0];
  const atomEnd = atomStart + atom.length;
  return occurrences(target, targetSpan).some(start => start < atomEnd && start + targetSpan.length > atomStart);
}

for (const arm of ["A", "B"]) {
  for (const run of [1, 2]) {
    for (const route of routes) {
      const stem = `${arm}-run${run}-${routeAliases[route]}`;
      const name = `CANDIDATE-${stem}.json`;
      if (!fs.existsSync(path.join(here, name))) throw new Error(`${name} missing`);
      const candidate = read(name);
      if (!candidate.valid || candidate.arm !== arm || candidate.run !== run || candidate.route !== route) throw new Error(`${name}: invalid identity/status`);
      if (candidate.input_sha256 !== sha256File(path.join(here, `HOLDOUT-${arm}.json`))) throw new Error(`${name}: input hash mismatch`);
      if (candidate.prompt_sha256 !== sha256File(path.join(here, "PROMPT.md")) || candidate.schema_sha256 !== sha256File(path.join(here, "REVIEWER-SCHEMA.json"))) throw new Error(`${name}: prompt/schema hash mismatch`);
      const raw = path.join(here, candidate.raw_artifact);
      const stderr = path.join(here, candidate.stderr_artifact);
      if (!fs.existsSync(raw) || sha256File(raw) !== candidate.raw_sha256) throw new Error(`${name}: raw hash mismatch`);
      if (!fs.existsSync(stderr) || sha256File(stderr) !== candidate.stderr_sha256) throw new Error(`${name}: stderr hash mismatch`);
      const semantic = new Map(candidate.claim_validation.map(item => [item.revision_id, item]));
      semanticByCandidate.set(name, semantic);
      const byId = new Map(candidate.response.revisions.map(item => [item.revision_id, item]));
      const itemScores = [];
      for (const id of armInputs[arm].items.map(item => item.revision_id)) {
        const response = byId.get(id);
        const ref = referenceById.get(id);
        const visible = inputByArmId[arm].get(id);
        const validClaim = response.verdict === "OK" || semantic.get(id)?.valid_claim === true;
        let atomMatch = false;
        if (ref.label.endsWith("MUTATION") && response.verdict !== "OK" && validClaim) {
          atomMatch = response.claim.claim_type === ref.claim_type && overlapsAtom(visible.target, response.claim.target_span, ref.atom_target_span);
        }
        itemScores.push({revision_id: id, evidence_class: ref.evidence_class, label: ref.label, verdict: response.verdict, valid_claim: validClaim, atom_match: atomMatch, detection: atomMatch ? 1 : 0, finding_detection: atomMatch && response.verdict === "FINDING" ? 1 : 0});
      }
      calls.push({arm, run, route, candidate_artifact: name, candidate_sha256: sha256File(path.join(here, name)), raw_artifact: candidate.raw_artifact, raw_sha256: candidate.raw_sha256, request_sha256: candidate.request_sha256, duration_seconds: candidate.duration_seconds, route_metadata: candidate.route_metadata, verdict_counts: candidate.verdict_counts, item_scores: itemScores, response_by_id: byId});
    }
  }
}

for (const arm of ["A", "B"]) {
  const requestHashes = new Set(calls.filter(call => call.arm === arm).map(call => call.request_sha256));
  if (requestHashes.size !== 1) throw new Error(`${arm}: requests are not byte-identical across routes/runs`);
}
const allCandidateNames = new Set(calls.map(call => call.candidate_artifact));
const unexpectedCandidates = fs.readdirSync(here).filter(name => /^CANDIDATE-[AB]-run/.test(name) && !/-unparsed-attempt1\.json$/.test(name) && !allCandidateNames.has(name));
if (unexpectedCandidates.length) throw new Error(`unexpected candidate artifacts: ${unexpectedCandidates.join(", ")}`);

const runtimeMutants = reference.items.filter(item => item.label === "RUNTIME_MUTATION").map(item => item.revision_id);
const runtimeControls = reference.items.filter(item => item.label === "RUNTIME_CONTROL").map(item => item.revision_id);
const surfaceMutants = reference.items.filter(item => item.label === "SURFACE_MUTATION").map(item => item.revision_id);
const surfaceControls = reference.items.filter(item => item.label === "SURFACE_CONTROL").map(item => item.revision_id);
const rawControlCandidates = [];
for (const call of calls) {
  for (const id of runtimeControls) {
    const itemScore = call.item_scores.find(item => item.revision_id === id);
    if (itemScore.verdict === "OK" || !itemScore.valid_claim) continue;
    const response = call.response_by_id.get(id);
    rawControlCandidates.push({candidate_key: `${call.arm}|${call.run}|${call.route}|${id}`, arm: call.arm, run: call.run, route: call.route, revision_id: id, verdict: response.verdict, claim: response.claim, observation: response.observation});
  }
}

let adjudication = null;
let adjudicationByKey = new Map();
if (!prelim) {
  if (!fs.existsSync(path.join(here, "ADJUDICATION.json"))) throw new Error("ADJUDICATION.json required for final scoring");
  adjudication = read("ADJUDICATION.json");
  if (adjudication.schema_version !== "runtime-source-context-adjudication-v1" || adjudication.status !== "FINAL") throw new Error("adjudication identity/status");
  adjudicationByKey = new Map(adjudication.control_candidates.map(item => [item.candidate_key, item]));
  if (adjudicationByKey.size !== adjudication.control_candidates.length) throw new Error("duplicate adjudication candidate key");
  const expectedKeys = rawControlCandidates.map(item => item.candidate_key).sort();
  const actualKeys = [...adjudicationByKey.keys()].sort();
  if (JSON.stringify(expectedKeys) !== JSON.stringify(actualKeys)) throw new Error("adjudication does not cover exactly all valid runtime control candidates");
}

function scoredControlSet(call) {
  if (prelim) return new Set(rawControlCandidates.filter(item => item.arm === call.arm && item.run === call.run && item.route === call.route).map(item => item.revision_id));
  return new Set(rawControlCandidates.filter(item => item.arm === call.arm && item.run === call.run && item.route === call.route && ["SOURCE_REFUTED", "CONTROL_CONTAMINATION"].includes(adjudicationByKey.get(item.candidate_key).classification)).map(item => item.revision_id));
}
function callFor(arm, run, route) { return calls.find(call => call.arm === arm && call.run === run && call.route === route); }
function detected(call, ids) { return new Set(call.item_scores.filter(item => ids.includes(item.revision_id) && item.detection).map(item => item.revision_id)); }
function findingDetected(call, ids) { return new Set(call.item_scores.filter(item => ids.includes(item.revision_id) && item.finding_detection).map(item => item.revision_id)); }

const runScores = [];
for (const run of [1, 2]) {
  const routeScores = [];
  let hitsA = 0;
  let hitsB = 0;
  let controlsA = 0;
  let controlsB = 0;
  let positiveRoutes = 0;
  let maxNewControls = 0;
  for (const route of routes) {
    const callA = callFor("A", run, route);
    const callB = callFor("B", run, route);
    const hitA = detected(callA, runtimeMutants);
    const hitB = detected(callB, runtimeMutants);
    const findingA = findingDetected(callA, runtimeMutants);
    const findingB = findingDetected(callB, runtimeMutants);
    const controlA = scoredControlSet(callA);
    const controlB = scoredControlSet(callB);
    const newControls = [...controlB].filter(id => !controlA.has(id));
    const routeNet = hitB.size - hitA.size;
    if (routeNet > 0) positiveRoutes += 1;
    maxNewControls = Math.max(maxNewControls, newControls.length);
    hitsA += hitA.size;
    hitsB += hitB.size;
    controlsA += controlA.size;
    controlsB += controlB.size;
    routeScores.push({route, runtime_mutants: {A_hits: hitA.size, B_hits: hitB.size, net: routeNet, A_ids: [...hitA], B_ids: [...hitB], A_finding_only: [...findingA], B_finding_only: [...findingB]}, runtime_controls: {A_candidates: controlA.size, B_candidates: controlB.size, net: controlB.size - controlA.size, A_ids: [...controlA], B_ids: [...controlB], new_B_ids: newControls}, surface_negative_control: {A_mutation_hits: [...detected(callA, surfaceMutants)], B_mutation_hits: [...detected(callB, surfaceMutants)], A_control_non_ok: surfaceControls.filter(id => callA.response_by_id.get(id).verdict !== "OK"), B_control_non_ok: surfaceControls.filter(id => callB.response_by_id.get(id).verdict !== "OK")}});
  }
  const contamination = prelim ? null : adjudication.control_candidates.filter(item => item.classification === "CONTROL_CONTAMINATION").length;
  const gates = {
    runtime_recall_net_at_least_10: hitsB - hitsA >= 10,
    at_least_three_positive_routes: positiveRoutes >= 3,
    runtime_control_net_at_most_2: controlsB - controlsA <= 2,
    per_route_new_controls_at_most_1: maxNewControls <= 1,
    zero_control_contamination: prelim ? null : contamination === 0
  };
  runScores.push({run, runtime_recall: {A_hits: hitsA, B_hits: hitsB, denominator: 48, A_rate: hitsA / 48, B_rate: hitsB / 48, net_hits: hitsB - hitsA, delta: (hitsB - hitsA) / 48}, route_direction: {positive_routes: positiveRoutes, required: 3}, runtime_control_candidates: {A: controlsA, B: controlsB, denominator: 48, net: controlsB - controlsA, max_new_B_in_any_route: maxNewControls}, control_contamination_count: contamination, gates, pass: prelim ? null : Object.values(gates).every(Boolean), route_scores: routeScores});
}

const publicCalls = calls.map(({response_by_id, item_scores, ...call}) => ({...call, item_scores}));
const base = {
  schema_version: "runtime-source-context-scores-v1",
  experiment: "runtime-source-context-pilot-v1",
  status: prelim ? "PRELIMINARY_AWAITING_CONTROL_ADJUDICATION" : "COMPLETE",
  scored_at: "2026-08-27",
  frozen_hashes_sha256: sha256File(path.join(here, "FROZEN-HASHES.json")),
  sealed_reference_sha256: sha256File(path.join(here, "REFERENCE.json")),
  source_verification_sha256: sha256File(path.join(here, "SOURCE-VERIFICATION.json")),
  request_identity: Object.fromEntries(["A", "B"].map(arm => [arm, [...new Set(calls.filter(call => call.arm === arm).map(call => call.request_sha256))][0]])),
  calls: publicCalls,
  raw_runtime_control_candidates: rawControlCandidates,
  run_scores: runScores
};
if (prelim) {
  const out = path.join(here, "SCORES-PRELIM.json");
  if (fs.existsSync(out)) throw new Error("refusing to overwrite SCORES-PRELIM.json");
  fs.writeFileSync(out, `${JSON.stringify(base, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({status: base.status, control_candidates_requiring_adjudication: rawControlCandidates.length, run_scores: runScores}, null, 2)}\n`);
} else {
  const scoresPath = path.join(here, "SCORES.json");
  const resultPath = path.join(here, "RESULT.json");
  if (fs.existsSync(scoresPath) || fs.existsSync(resultPath)) throw new Error("refusing to overwrite final scores/results");
  const finalScores = {...base, adjudication_sha256: sha256File(path.join(here, "ADJUDICATION.json"))};
  fs.writeFileSync(scoresPath, `${JSON.stringify(finalScores, null, 2)}\n`);
  const adoptB = runScores.every(run => run.pass);
  const failures = fs.readdirSync(here).filter(name => /^FAILURE-[AB]-run/.test(name)).sort();
  const result = {schema_version: "runtime-source-context-result-v1", experiment: "runtime-source-context-pilot-v1", status: "COMPLETE", completed_at: "2026-08-27", measured: {calls: 16, harness_failures_and_retries: failures, runtime_mutants: 12, runtime_controls: 12, surface_mutants: 6, surface_controls: 6, run_scores: runScores}, decision: {adopt_B_as_default_for_later_phases: adoptB, rule: "Both runs must independently pass every registered gate; no pooling and no third run."}, artifacts: {scores: "SCORES.json", scores_sha256: sha256File(scoresPath), adjudication: "ADJUDICATION.json", adjudication_sha256: finalScores.adjudication_sha256, frozen_hashes: "FROZEN-HASHES.json", frozen_hashes_sha256: base.frozen_hashes_sha256}, interpretation: [], limitations: ["The estimand is limited to this frozen 12-item runtime-mutant benchmark.", "Surface items are negative controls and runtime controls are guardrails, not additional primary recall units.", "Route and run observations are repeated measurements, not independent draws from a defined model superpopulation."]};
  fs.writeFileSync(resultPath, `${JSON.stringify(result, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({status: result.status, adopt_B_as_default_for_later_phases: adoptB, run_scores: runScores}, null, 2)}\n`);
}
