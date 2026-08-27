import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = "/home/yun/research/tome4-agent-eval";
const outDir = path.join(root, "evidence/quality/model-probes/claude-opus-fable-5-reviewer-b4-v1");
const inputPath = path.join(root, "evidence/quality/p1-batches/p1-b4-mechanics-numeric.json");
const referencePath = path.join(root, "evidence/quality/p1-batches/p1-b4-s2-verification.json");
const scorePath = path.join(outDir, "SCORES.json");
const resultPath = path.join(outDir, "RESULT.json");
const routes = [
  {slug: "claude-opus-5-medium", artifactSlug: "claude-opus-5-medium-no-advisor", requestedModel: "claude-opus-5", expectedAdvisorModel: null, qualification: "single_model"},
  {slug: "claude-fable-5-medium", artifactSlug: "claude-fable-5-medium-no-advisor", requestedModel: "claude-fable-5", expectedAdvisorModel: null, qualification: "single_model"}
];
const advisorRoutes = [
  {slug: "claude-opus-5-medium-plus-fable-advisor", artifactSlug: "claude-opus-5-medium", requestedModel: "claude-opus-5", expectedAdvisorModel: "claude-fable-5", qualification: "composite_advisor_route"},
  {slug: "claude-fable-5-medium-plus-fable-advisor", artifactSlug: "claude-fable-5-medium", requestedModel: "claude-fable-5", expectedAdvisorModel: "claude-fable-5", qualification: "self_advisor_route"}
];

const expectedHashes = {
  input: "9034f605bcf471bd7fce0d603ee52c6a8d5fbb9b2807e2b801b9fb52316ee332",
  reference: "df16fc3702a4ffceca9a81ff86ae4583d76174e992090370eac62baaeafb3154"
};
function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}
for (const [name, file] of Object.entries({input: inputPath, reference: referencePath})) {
  const actual = sha256(file);
  if (actual !== expectedHashes[name]) throw new Error(`${name} hash mismatch: expected ${expectedHashes[name]}, got ${actual}`);
}
const input = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const reference = JSON.parse(fs.readFileSync(referencePath, "utf8"));
const orderedIds = input.items.map(item => item.revision_id);
const defectIds = new Set(reference.items.filter(item => (item.verdict ?? item.decision) === "defect").map(item => item.revision_id));

function scoreRoute(route) {
  const candidatePath = path.join(outDir, `CANDIDATE-${route.artifactSlug}.json`);
  const envelope = JSON.parse(fs.readFileSync(candidatePath, "utf8"));
  const candidate = envelope.response;
  const schemaErrors = [];
  const advisorIterations = (envelope.result_metadata.usage?.iterations ?? []).filter(iteration => iteration.type === "advisor_message");
  const advisorValid = route.expectedAdvisorModel === null
    ? advisorIterations.length === 0
    : advisorIterations.length >= 1 && advisorIterations.every(iteration => iteration.model === route.expectedAdvisorModel);
  const identityValid = envelope.route.initialized_model === route.requestedModel
    && envelope.route.actual_assistant_models.length === 1
    && envelope.route.actual_assistant_models[0] === route.requestedModel
    && envelope.fallback_events.length === 0
    && envelope.fallback_blocks.length === 0
    && advisorValid;
  if (!identityValid) schemaErrors.push("runtime model identity or fallback rule failed");
  if (!envelope.strict_json || !candidate || typeof candidate !== "object" || Array.isArray(candidate)) {
    schemaErrors.push("visible/structured response is not a strict JSON object");
  } else {
    const topKeys = Object.keys(candidate);
    if (topKeys.length !== 1 || topKeys[0] !== "revisions") schemaErrors.push("top-level keys must be exactly revisions");
    if (!Array.isArray(candidate.revisions)) {
      schemaErrors.push("revisions must be an array");
    } else {
      if (candidate.revisions.length !== 24) schemaErrors.push(`expected 24 revisions, got ${candidate.revisions.length}`);
      for (const [index, revision] of candidate.revisions.entries()) {
        if (!revision || typeof revision !== "object" || Array.isArray(revision)) {
          schemaErrors.push(`revision ${index} is not an object`);
          continue;
        }
        const keys = Object.keys(revision).sort();
        if (keys.join(",") !== "evidence,observation,revision_id") schemaErrors.push(`revision ${index} keys are invalid: ${keys.join(",")}`);
        for (const key of ["revision_id", "observation", "evidence"]) {
          if (typeof revision[key] !== "string") schemaErrors.push(`revision ${index}.${key} must be a string`);
        }
      }
    }
  }
  const ids = Array.isArray(candidate?.revisions) ? candidate.revisions.map(item => item?.revision_id) : [];
  const orderedCoverage = ids.length === orderedIds.length && ids.every((id, index) => id === orderedIds[index]);
  if (!orderedCoverage) schemaErrors.push("revision IDs do not exactly match frozen input order");
  const valid = schemaErrors.length === 0;

  let metrics = null;
  let predictedDefectIds = [];
  let missedDefectIds = [];
  let falsePositiveIds = [];
  let labelContractWarnings = [];
  if (valid) {
    labelContractWarnings = candidate.revisions
      .filter(item => item.observation.startsWith("OK") && item.observation !== "OK")
      .map(item => ({revision_id: item.revision_id, observation: item.observation}));
    const predicted = new Set(candidate.revisions.filter(item => item.observation !== "OK").map(item => item.revision_id));
    predictedDefectIds = orderedIds.filter(id => predicted.has(id));
    let tp = 0, fp = 0, fn = 0, tn = 0;
    for (const id of orderedIds) {
      if (defectIds.has(id) && predicted.has(id)) tp++;
      else if (!defectIds.has(id) && predicted.has(id)) fp++;
      else if (defectIds.has(id)) fn++;
      else tn++;
    }
    const recall = tp / (tp + fn);
    const precision = tp + fp ? tp / (tp + fp) : null;
    const cleanFalsePositiveRate = fp / (fp + tn);
    const specificity = tn / (tn + fp);
    metrics = {tp, fp, fn, tn, recall, precision, clean_false_positive_rate: cleanFalsePositiveRate, specificity, balanced_accuracy: (recall + specificity) / 2};
    missedDefectIds = orderedIds.filter(id => defectIds.has(id) && !predicted.has(id));
    falsePositiveIds = orderedIds.filter(id => !defectIds.has(id) && predicted.has(id));
  }
  return {
    qualification: route.qualification,
    valid,
    identity_valid: identityValid,
    strict_json: envelope.strict_json,
    ordered_coverage: orderedCoverage,
    validation_errors: schemaErrors,
    duration_seconds: envelope.duration_seconds,
    route: envelope.route,
    fallback_events: envelope.fallback_events,
    fallback_blocks: envelope.fallback_blocks,
    advisor_iterations: advisorIterations,
    expected_advisor_model: route.expectedAdvisorModel,
    result_metadata: envelope.result_metadata,
    metrics,
    predicted_defect_ids: predictedDefectIds,
    missed_defect_ids: missedDefectIds,
    false_positive_ids: falsePositiveIds,
    label_contract_warnings: labelContractWarnings
  };
}

const measured = Object.fromEntries(routes.map(route => [route.slug, scoreRoute(route)]));
const advisorAssisted = Object.fromEntries(advisorRoutes.map(route => [route.slug, scoreRoute(route)]));
const scores = {schema_version: 1, experiment: "EXPERIMENT.json", measured, advisor_assisted: advisorAssisted};
fs.writeFileSync(scorePath, JSON.stringify(scores, null, 2) + "\n");
const allValid = [...Object.values(measured), ...Object.values(advisorAssisted)].every(item => item.valid);
const result = {
  schema_version: 1,
  status: allValid ? "COMPLETE" : "COMPLETE_WITH_INVALID_CANDIDATE",
  experiment: "EXPERIMENT.json",
  population: {items: 24, defect_revisions: 7, clean_revisions: 17},
  measured_runs: measured,
  advisor_assisted_runs: advisorAssisted,
  historical_b4_baselines: {
    provenance: "../non-args-reviewer-model-comparison-b4-v1/RESULT.json; recorded prior runs, not re-run here",
    codex_gpt_5_6_sol_high_baseline: {recall: 0.571429, precision: 0.666667, clean_false_positive_rate: 0.117647, balanced_accuracy: 0.726891, duration_seconds: 102.967},
    grok_4_6_cli_default_baseline: {recall: 0.428571, precision: 0.6, clean_false_positive_rate: 0.117647, balanced_accuracy: 0.655462, duration_seconds: 438.619},
    gemini_3_7_flash_high_baseline: {recall: 0.0, precision: null, clean_false_positive_rate: 0.0, balanced_accuracy: 0.5, duration_seconds: 39.092}
  },
  interpretation: {
    measured_only: "One full B4 run was attempted per requested Claude model at medium effort.",
    advisor_routes: "Advisor-assisted envelopes are reported as composite routes, not attributed to the main model alone.",
    fallback_rule: "Fallback output is retained as route evidence but is never scored as the requested model.",
    variance: "No repeat-run variance was measured; small metric differences must not be treated as stable model differences.",
    adjudication: "Candidate findings remain test outputs and cannot override fixed-source verification."
  }
};
fs.writeFileSync(resultPath, JSON.stringify(result, null, 2) + "\n");
process.stdout.write(JSON.stringify({
  measured: Object.fromEntries(Object.entries(measured).map(([name, item]) => [name, {valid: item.valid, metrics: item.metrics, validation_errors: item.validation_errors}])),
  advisor_assisted: Object.fromEntries(Object.entries(advisorAssisted).map(([name, item]) => [name, {valid: item.valid, metrics: item.metrics, validation_errors: item.validation_errors}]))
}) + "\n");
