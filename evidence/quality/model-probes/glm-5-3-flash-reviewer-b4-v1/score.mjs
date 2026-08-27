import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = "/home/yun/research/tome4-agent-eval";
const outDir = path.join(root, "evidence/quality/model-probes/glm-5-3-flash-reviewer-b4-v1");
const inputPath = path.join(root, "evidence/quality/p1-batches/p1-b4-mechanics-numeric.json");
const referencePath = path.join(root, "evidence/quality/p1-batches/p1-b4-s2-verification.json");
const candidatePath = path.join(outDir, "CANDIDATE-pi-high.json");
const scorePath = path.join(outDir, "SCORE.json");
const resultPath = path.join(outDir, "RESULT.json");

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
const candidateEnvelope = JSON.parse(fs.readFileSync(candidatePath, "utf8"));
const candidate = candidateEnvelope.response;
const orderedIds = input.items.map(item => item.revision_id);
const defectIds = new Set(reference.items.filter(item => (item.verdict ?? item.decision) === "defect").map(item => item.revision_id));

const schemaErrors = [];
if (!candidateEnvelope.strict_json || !candidate || typeof candidate !== "object" || Array.isArray(candidate)) {
  schemaErrors.push("visible response is not a strict JSON object");
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
if (valid) {
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

const score = {
  schema_version: 1,
  experiment: "EXPERIMENT.json",
  candidate: "CANDIDATE-pi-high.json",
  measured: {
    valid,
    strict_json: candidateEnvelope.strict_json,
    ordered_coverage: orderedCoverage,
    schema_errors: schemaErrors,
    duration_seconds: candidateEnvelope.duration_seconds,
    route: candidateEnvelope.route,
    stop_reason: candidateEnvelope.stop_reason,
    usage: candidateEnvelope.usage,
    metrics,
    predicted_defect_ids: predictedDefectIds,
    missed_defect_ids: missedDefectIds,
    false_positive_ids: falsePositiveIds
  }
};
fs.writeFileSync(scorePath, JSON.stringify(score, null, 2) + "\n");

const result = {
  schema_version: 1,
  status: valid ? "COMPLETE" : "COMPLETE_WITH_INVALID_CANDIDATE",
  experiment: "EXPERIMENT.json",
  population: {items: 24, defect_revisions: 7, clean_revisions: 17},
  measured_run: score.measured,
  historical_b4_baselines: {
    provenance: "../non-args-reviewer-model-comparison-b4-v1/RESULT.json; recorded prior runs, not re-run here",
    codex_gpt_5_6_sol_high_baseline: {recall: 0.571429, precision: 0.666667, clean_false_positive_rate: 0.117647, balanced_accuracy: 0.726891, duration_seconds: 102.967},
    grok_4_6_cli_default_baseline: {recall: 0.428571, precision: 0.6, clean_false_positive_rate: 0.117647, balanced_accuracy: 0.655462, duration_seconds: 438.619},
    gemini_3_7_flash_high_baseline: {recall: 0.0, precision: null, clean_false_positive_rate: 0.0, balanced_accuracy: 0.5, duration_seconds: 39.092}
  },
  interpretation: valid ? {
    measured_only: "This is one GLM-5.3-Flash sample on the frozen B4 baseline prompt.",
    variance: "No repeat-run variance was measured; small metric differences must not be treated as stable model differences.",
    adjudication: "Candidate findings remain test outputs and cannot override fixed-source verification."
  } : {
    measured_only: "The candidate is invalid and receives no reviewer quality score.",
    variance: "No repeat-run variance was measured.",
    adjudication: "Candidate findings remain test outputs and cannot override fixed-source verification."
  }
};
fs.writeFileSync(resultPath, JSON.stringify(result, null, 2) + "\n");
process.stdout.write(JSON.stringify({valid, metrics, schema_errors: schemaErrors}) + "\n");
