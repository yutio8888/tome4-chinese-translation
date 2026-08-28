import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function readArtifact(name) {
  const bytes = fs.readFileSync(path.join(here, name));
  return {bytes, data: JSON.parse(bytes.toString("utf8")), sha256: sha256(bytes)};
}

function readArtifactPath(artifactPath) {
  const bytes = fs.readFileSync(artifactPath);
  return {bytes, data: JSON.parse(bytes.toString("utf8")), sha256: sha256(bytes)};
}

function parseArgs(argv) {
  const args = {
    outDir: here,
    audit: path.join(here, "SOURCE-AUDIT.json"),
    frame: path.join(here, "FRAME.json")
  };
  const valueFlags = new Set(["--out-dir", "--audit", "--frame"]);
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (!valueFlags.has(flag) || !argv[index + 1]) {
      throw new Error("usage: node build-reference.mjs [--out-dir DIRECTORY] [--audit SOURCE_AUDIT] [--frame FRAME]");
    }
    if (flag === "--out-dir") args.outDir = path.resolve(argv[++index]);
    else if (flag === "--audit") args.audit = path.resolve(argv[++index]);
    else args.frame = path.resolve(argv[++index]);
  }
  return args;
}

function gcd(a, b) {
  let x = a < 0n ? -a : a;
  let y = b < 0n ? -b : b;
  while (y !== 0n) [x, y] = [y, x % y];
  return x;
}

function rational(numerator, denominator = 1n) {
  assert(denominator !== 0n, "zero rational denominator");
  let n = BigInt(numerator);
  let d = BigInt(denominator);
  if (d < 0n) [n, d] = [-n, -d];
  const divisor = gcd(n, d);
  return {n: n / divisor, d: d / divisor};
}

function add(a, b) {
  return rational(a.n * b.d + b.n * a.d, a.d * b.d);
}

function divide(a, b) {
  assert(b.n !== 0n, "division by zero rational");
  return rational(a.n * b.d, a.d * b.n);
}

function sum(values) {
  return values.reduce((total, value) => add(total, value), rational(0n));
}

function exactWeight(value) {
  assert(Number.isFinite(value) && value > 0, "invalid design weight");
  const integer = Math.round(value);
  if (Math.abs(value - integer) <= 1e-9) return rational(BigInt(integer));
  const tenth = Math.round(value * 10);
  if (Math.abs(value * 10 - tenth) <= 1e-9) return rational(BigInt(tenth), 10n);
  throw new Error(`design weight is not an allowed exact integer or one-decimal rational: ${value}`);
}

function serializeRational(value) {
  return {
    numerator: value.n.toString(),
    denominator: value.d.toString(),
    fraction: `${value.n}/${value.d}`,
    decimal: Number(value.n) / Number(value.d)
  };
}

function fraction(numerator, denominator) {
  return divide(rational(BigInt(numerator)), rational(BigInt(denominator)));
}

const args = parseArgs(process.argv.slice(2));
const contractArtifact = readArtifact("ESTIMATOR-CONTRACT.json");
const frameArtifact = readArtifactPath(args.frame);
const queueArtifact = readArtifact("AUDIT-QUEUE.json");
const auditArtifact = readArtifactPath(args.audit);
const contract = contractArtifact.data;
const frame = frameArtifact.data;
const queue = queueArtifact.data;
const audit = auditArtifact.data;

assert(contract.schema_version === "prospective-residual-estimator-contract-v3", "unexpected estimator contract schema");
assert(contract.status === "FROZEN_BEFORE_REVIEWER_INFERENCE", "estimator contract is not frozen");
assert(contract.visible_to_reviewer_routes === false && contract.reviewer_route_model_calls_made === 0, "estimator contract visibility invariant failed");
assert(frame.schema_version === "prospective-residual-audit-frame-v3" && frame.status === "FROZEN_CANDIDATE_FRAME", "unexpected frame state");
assert(queue.schema_version === "prospective-residual-audit-queue-v3" && queue.reviewer_inference_allowed === false, "unexpected queue state");
assert(audit.schema_version === "prospective-residual-source-audit-v3" && audit.status === "FROZEN_SOURCE_AUDIT", "unexpected source-audit state");
assert(audit.visible_to_reviewer_routes === false && audit.reviewer_route_model_calls_made === 0, "source-audit visibility invariant failed");
assert(queue.items.length === 40 && audit.items.length === 40, "expected 40 selected and audited items");
assert(JSON.stringify(queue.items.map(item => item.audit_id)) === JSON.stringify(audit.items.map(item => item.audit_id)), "audit coverage or order mismatch");
assert(new Set(queue.items.map(item => item.task_id)).size === 40, "sampled tasks are not unique");
assert(new Set(queue.items.map(item => item.canonical_identity.revision_uid)).size === 40, "sampled canonical revisions are not unique");

const approximatelyEqual = (left, right, tolerance = 1e-12) => Math.abs(left - right) <= tolerance;
const frameTaskById = new Map(frame.tasks.map(task => [task.task_id, task]));
assert(frameTaskById.size === frame.tasks.length, "frame task_id values are not unique");
const sameFamilyTasks = frame.tasks.filter(task => task.stratum === "same_family_only");
const sameFamilyCertainty = sameFamilyTasks.filter(task => task.task_inclusion_probability === 1);
const sameFamilyNoncertainty = sameFamilyTasks.filter(task => task.task_inclusion_probability < 1);
const sumTaskRevisions = tasks => tasks.reduce((total, task) => total + task.eligible_canonical_revisions, 0);
assert(sameFamilyTasks.length === 30 && sumTaskRevisions(sameFamilyTasks) === 733, "same-family frame size proof failed");
assert(sameFamilyCertainty.length === 19 && sumTaskRevisions(sameFamilyCertainty) === 717, "same-family certainty stratum proof failed");
assert(sameFamilyCertainty.every(task => task.selected === true), "a same-family certainty task was not selected");
assert(sameFamilyNoncertainty.length === 11 && sumTaskRevisions(sameFamilyNoncertainty) === 16, "same-family noncertainty frame proof failed");
assert(sameFamilyNoncertainty.filter(task => task.selected).length === 5, "same-family noncertainty design must select exactly five tasks");
for (const task of sameFamilyNoncertainty) {
  assert(approximatelyEqual(task.task_inclusion_probability, 5 * task.eligible_canonical_revisions / 16), `${task.task_id}: noncertainty PPS probability proof failed`);
}
for (const stratum of ["cross_or_mixed_family", "unknown_provenance"]) {
  const tasks = frame.tasks.filter(task => task.stratum === stratum);
  assert(tasks.length === frame.counts[stratum].eligible_tasks, `${stratum}: frame task count mismatch`);
  assert(sumTaskRevisions(tasks) === contract.population.stratum_sizes[stratum], `${stratum}: frame revision count mismatch`);
  assert(tasks.every(task => task.task_inclusion_probability === 1 && task.selected === true), `${stratum}: census proof failed`);
}
const selectedFrameTaskIds = frame.tasks.filter(task => task.selected).map(task => task.task_id).sort();
assert(selectedFrameTaskIds.length === 40, "frame must select 40 tasks");
assert(JSON.stringify(selectedFrameTaskIds) === JSON.stringify(queue.items.map(item => item.task_id).sort()), "queue tasks do not equal selected frame tasks");

const mapping = contract.reference_mapping;
const auditById = new Map(audit.items.map(item => [item.audit_id, item]));
const rows = queue.items.map(queueItem => {
  const audited = auditById.get(queueItem.audit_id);
  const reference = mapping[audited.verdict];
  const frameTask = frameTaskById.get(queueItem.task_id);
  assert(reference, `${queueItem.audit_id}: verdict is absent from reference mapping`);
  assert(frameTask?.selected === true && frameTask.stratum === queueItem.stratum, `${queueItem.audit_id}: selected frame-task binding mismatch`);
  assert(approximatelyEqual(queueItem.task_inclusion_probability, frameTask.task_inclusion_probability), `${queueItem.audit_id}: queue/frame task probability mismatch`);
  assert(approximatelyEqual(queueItem.item_probability_given_task, 1 / frameTask.eligible_canonical_revisions), `${queueItem.audit_id}: task-within revision probability mismatch`);
  const pi = queueItem.task_inclusion_probability * queueItem.item_probability_given_task;
  assert(pi > 0 && pi <= 1, `${queueItem.audit_id}: invalid inclusion probability`);
  assert(Math.abs(pi - queueItem.revision_inclusion_probability) <= 1e-12, `${queueItem.audit_id}: inclusion probability product mismatch`);
  assert(Math.abs(queueItem.design_weight - 1 / pi) <= 1e-9, `${queueItem.audit_id}: inverse-probability weight mismatch`);
  const weight = exactWeight(queueItem.design_weight);
  if (queueItem.stratum === "same_family_only" && frameTask.task_inclusion_probability < 1) {
    assert(weight.n === 16n && weight.d === 5n, `${queueItem.audit_id}: noncertainty revision weight must be 16/5`);
    assert(approximatelyEqual(pi, 5 / 16), `${queueItem.audit_id}: noncertainty revision inclusion probability must be 5/16`);
  }
  if (frameTask.task_inclusion_probability === 1) {
    assert(weight.n === BigInt(frameTask.eligible_canonical_revisions) && weight.d === 1n, `${queueItem.audit_id}: certainty/census revision weight proof failed`);
  }
  return {queueItem, audited, reference, weight};
});

const stratumNames = Object.keys(contract.population.stratum_sizes);
for (const stratum of stratumNames) {
  const exactWeightSum = sum(rows.filter(row => row.queueItem.stratum === stratum).map(row => row.weight));
  const expectedSize = rational(BigInt(contract.population.stratum_sizes[stratum]));
  assert(exactWeightSum.n === expectedSize.n && exactWeightSum.d === expectedSize.d, `${stratum}: realized weights do not sum to the frozen stratum size`);
}
const totalWeight = sum(rows.map(row => row.weight));
assert(totalWeight.n === BigInt(contract.population.canonical_revisions) && totalWeight.d === 1n, "realized weights do not sum to the frozen population size");

const referenceItems = rows.map(row => {
  return {
    audit_id: row.queueItem.audit_id,
    canonical_revision_uid: row.queueItem.canonical_identity.revision_uid,
    stratum: row.queueItem.stratum,
    scoring_label: row.reference.binary_label,
    y: row.reference.y,
    scorable: row.reference.scorable,
    source_audit_item_sha256: sha256(JSON.stringify(row.audited)),
    design_weight_exact: serializeRational(row.weight)
  };
});
const referenceCounts = {
  items: referenceItems.length,
  scorable: referenceItems.filter(item => item.scorable).length,
  defects: referenceItems.filter(item => item.y === 1).length,
  no_defects: referenceItems.filter(item => item.y === 0).length,
  not_scorable: referenceItems.filter(item => !item.scorable).length
};
const sealedReference = {
  schema_version: "prospective-residual-sealed-reference-v3",
  status: "SEALED_BEFORE_REVIEWER_INFERENCE",
  visible_to_reviewer_routes: false,
  reviewer_route_model_calls_made: 0,
  source_audit_sha256: auditArtifact.sha256,
  audit_queue_sha256: queueArtifact.sha256,
  estimator_contract_sha256: contractArtifact.sha256,
  counts: referenceCounts,
  items: referenceItems
};
const referenceBytes = Buffer.from(`${JSON.stringify(sealedReference, null, 2)}\n`);

function summarize(selectedRows, populationSize, globalPointEstimateGatePass) {
  const confirmedWeight = sum(selectedRows.filter(row => row.audited.verdict === "CONFIRMED").map(row => row.weight));
  const missingWeight = sum(selectedRows.filter(row => ["INDETERMINATE", "UNREACHABLE"].includes(row.audited.verdict)).map(row => row.weight));
  const determinateWeight = sum(selectedRows.filter(row => ["CONFIRMED", "REFUTED"].includes(row.audited.verdict)).map(row => row.weight));
  const selectedWeight = sum(selectedRows.map(row => row.weight));
  const upperDefectWeight = add(confirmedWeight, missingWeight);
  const determinateCount = selectedRows.filter(row => ["CONFIRMED", "REFUTED"].includes(row.audited.verdict)).length;
  const confirmedCount = selectedRows.filter(row => row.audited.verdict === "CONFIRMED").length;
  const fullyDeterminate = determinateCount === selectedRows.length;
  return {
    sampled_items: selectedRows.length,
    population_revisions: populationSize,
    exact_weight_sum: serializeRational(selectedWeight),
    verdict_counts: {
      CONFIRMED: confirmedCount,
      REFUTED: selectedRows.filter(row => row.audited.verdict === "REFUTED").length,
      INDETERMINATE: selectedRows.filter(row => row.audited.verdict === "INDETERMINATE").length,
      UNREACHABLE: selectedRows.filter(row => row.audited.verdict === "UNREACHABLE").length
    },
    confirmed_weighted_total: serializeRational(confirmedWeight),
    missing_evidence_weighted_total: serializeRational(missingWeight),
    identification_bounds: {
      lower: serializeRational(divide(confirmedWeight, selectedWeight)),
      upper: serializeRational(divide(upperDefectWeight, selectedWeight))
    },
    point_estimates: {
      global_availability_gate_pass: globalPointEstimateGatePass,
      fully_determinate: fullyDeterminate,
      horvitz_thompson_known_denominator: globalPointEstimateGatePass && fullyDeterminate ? serializeRational(divide(confirmedWeight, rational(BigInt(populationSize)))) : null,
      hajek_ratio: globalPointEstimateGatePass && determinateWeight.n !== 0n ? serializeRational(divide(confirmedWeight, determinateWeight)) : null,
      unweighted_sample_rate: globalPointEstimateGatePass && determinateCount > 0 ? serializeRational(fraction(confirmedCount, determinateCount)) : null
    }
  };
}

const determinateCount = rows.filter(row => ["CONFIRMED", "REFUTED"].includes(row.audited.verdict)).length;
const globalPointEstimateGatePass = 10 * determinateCount >= 9 * rows.length;
const overallSummary = summarize(rows, contract.population.canonical_revisions, globalPointEstimateGatePass);
const byStratum = Object.fromEntries(stratumNames.map(stratum => [
  stratum,
  summarize(rows.filter(row => row.queueItem.stratum === stratum), contract.population.stratum_sizes[stratum], globalPointEstimateGatePass)
]));
const knownProvenanceRows = rows.filter(row => row.queueItem.stratum !== "unknown_provenance");
const confirmedRows = rows.filter(row => row.audited.verdict === "CONFIRMED");
const determinateRate = fraction(determinateCount, rows.length);
const provenanceRate = fraction(knownProvenanceRows.length, rows.length);
const weightedProvenanceShare = divide(sum(knownProvenanceRows.map(row => row.weight)), totalWeight);
const determinatePass = globalPointEstimateGatePass;
const provenancePass = 10 * knownProvenanceRows.length >= 9 * rows.length;
const distinctConfirmedTasks = new Set(confirmedRows.map(row => row.queueItem.task_id)).size;
const originPilotPriorityPass = confirmedRows.length >= 4 && distinctConfirmedTasks >= 4 && determinatePass && provenancePass;

const estimates = {
  schema_version: "prospective-residual-reference-estimates-v3",
  status: "FROZEN_BEFORE_REVIEWER_INFERENCE",
  visible_to_reviewer_routes: false,
  reviewer_route_model_calls_made: 0,
  input_sha256s: {
    estimator_contract: contractArtifact.sha256,
    frame: frameArtifact.sha256,
    audit_queue: queueArtifact.sha256,
    source_audit: auditArtifact.sha256,
    sealed_reference: sha256(referenceBytes)
  },
  overall: overallSummary,
  by_stratum: byStratum,
  feasibility_gates: {
    determinate: {
      exact_rate: serializeRational(determinateRate),
      threshold: ">= 9/10",
      pass: determinatePass
    },
    provenance_classifiable: {
      exact_unweighted_rate: serializeRational(provenanceRate),
      exact_design_weighted_share: serializeRational(weightedProvenanceShare),
      threshold: ">= 9/10 on 40 sampled units",
      unknown_items_retained: rows.length - knownProvenanceRows.length,
      pass: provenancePass
    },
    origin_pilot_budget_priority: {
      confirmed_items: confirmedRows.length,
      distinct_confirmed_tasks: distinctConfirmedTasks,
      threshold: ">= 4 confirmed items across >= 4 distinct tasks, with both preceding gates passing",
      pass: originPilotPriorityPass,
      decision: originPilotPriorityPass ? "PRIORITIZE_SEPARATELY_FROZEN_ORIGIN_PILOT" : "DEFER_ORIGIN_PILOT"
    }
  },
  uncertainty_statement: contract.prevalence_estimators.uncertainty,
  reviewer_scoring_status: "CONTRACT_FROZEN; ROUTE OUTPUT SCORER AND PREFLIGHT STILL REQUIRED",
  interpretation_limits: [
    "The identification bounds are not confidence intervals.",
    "No design-based confidence interval is reported from this single systematic-PPS realization.",
    "The unweighted 1/40 result describes the sample only; it is not the finite-frame prevalence estimate.",
    "Stratum contrasts are descriptive and cannot identify a reviewer-family causal effect.",
    "The origin-pilot gate is a budget-priority rule, not a scientific null-hypothesis test."
  ]
};
const estimateBytes = Buffer.from(`${JSON.stringify(estimates, null, 2)}\n`);

fs.mkdirSync(args.outDir, {recursive: true});
fs.writeFileSync(path.join(args.outDir, "SEALED-REFERENCE.json"), referenceBytes);
fs.writeFileSync(path.join(args.outDir, "REFERENCE-ESTIMATES.json"), estimateBytes);
process.stdout.write(`${JSON.stringify({
  status: estimates.status,
  sealed_reference_sha256: sha256(referenceBytes),
  reference_estimates_sha256: sha256(estimateBytes),
  overall: estimates.overall,
  feasibility_gates: estimates.feasibility_gates
}, null, 2)}\n`);
