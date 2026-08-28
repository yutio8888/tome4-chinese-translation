import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const expectedInputSha256s = {
  estimator_contract: "e638b3fbacc214f5141d65ba28a9974bd95fb2de404e6393fb7e857b61dc5d94",
  frame: "7964a9b82cd9bd3cf9617aecd84550487eb23ab03a78b466d29c5dc2ab888e2c",
  audit_queue: "f785989e8bddf8b06fda34915154b7b5bbe76022926b0e3462aede44e625e159",
  source_audit: "622b0b523c6da3fe95040cc9440a1322aa5dc9e47752eca653c83769776cb092"
};
const expectedOutputSha256s = {
  sealed_reference: "133f7f64a2f04c6dcfc4123cfc8ed2e305b4353353e4f79f382c6fb46c4c4d59",
  reference_estimates: "538de92c399fe3ad791592cdc2a51126e942195782ace8fc7c161acbf3ea4e35"
};

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertFraction(value, numerator, denominator, label) {
  assert(value?.numerator === numerator && value?.denominator === denominator && value?.fraction === `${numerator}/${denominator}`, `${label}: exact fraction mismatch`);
  assert(Math.abs(value.decimal - Number(numerator) / Number(denominator)) <= 1e-15, `${label}: decimal mismatch`);
}

const committedReferencePath = path.join(here, "SEALED-REFERENCE.json");
const committedEstimatesPath = path.join(here, "REFERENCE-ESTIMATES.json");
assert(fs.existsSync(committedReferencePath) && fs.existsSync(committedEstimatesPath), "sealed reference outputs missing");
const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-residual-reference-v3-"));

try {
  execFileSync(process.execPath, [path.join(here, "build-reference.mjs"), "--out-dir", temporaryDirectory], {
    stdio: "pipe",
    maxBuffer: 64 * 1024 * 1024
  });
  const committedReference = fs.readFileSync(committedReferencePath);
  const committedEstimates = fs.readFileSync(committedEstimatesPath);
  const regeneratedReference = fs.readFileSync(path.join(temporaryDirectory, "SEALED-REFERENCE.json"));
  const regeneratedEstimates = fs.readFileSync(path.join(temporaryDirectory, "REFERENCE-ESTIMATES.json"));
  assert(committedReference.compare(regeneratedReference) === 0, "SEALED-REFERENCE.json does not reproduce byte-for-byte");
  assert(committedEstimates.compare(regeneratedEstimates) === 0, "REFERENCE-ESTIMATES.json does not reproduce byte-for-byte");
  assert(sha256(committedReference) === expectedOutputSha256s.sealed_reference, "sealed reference frozen hash mismatch");
  assert(sha256(committedEstimates) === expectedOutputSha256s.reference_estimates, "reference estimates frozen hash mismatch");

  const contractBytes = fs.readFileSync(path.join(here, "ESTIMATOR-CONTRACT.json"));
  const frameBytes = fs.readFileSync(path.join(here, "FRAME.json"));
  const queueBytes = fs.readFileSync(path.join(here, "AUDIT-QUEUE.json"));
  const auditBytes = fs.readFileSync(path.join(here, "SOURCE-AUDIT.json"));
  assert(sha256(contractBytes) === expectedInputSha256s.estimator_contract, "estimator contract frozen hash mismatch");
  assert(sha256(frameBytes) === expectedInputSha256s.frame, "frame frozen hash mismatch");
  assert(sha256(queueBytes) === expectedInputSha256s.audit_queue, "audit queue frozen hash mismatch");
  assert(sha256(auditBytes) === expectedInputSha256s.source_audit, "source audit frozen hash mismatch");

  const contract = JSON.parse(contractBytes.toString("utf8"));
  const queue = JSON.parse(queueBytes.toString("utf8"));
  const audit = JSON.parse(auditBytes.toString("utf8"));
  const reference = JSON.parse(committedReference.toString("utf8"));
  const estimates = JSON.parse(committedEstimates.toString("utf8"));
  assert(contract.status === "FROZEN_BEFORE_REVIEWER_INFERENCE" && contract.visible_to_reviewer_routes === false, "estimator contract freeze invariant failed");
  assert(contract.prevalence_estimators.uncertainty.variance_status === "NOT_ESTIMABLE_UNDER_FROZEN_DESIGN", "variance no-go status missing");
  assert(contract.prevalence_estimators.uncertainty.confidence_interval === null, "prohibited confidence interval registered");
  assert(reference.schema_version === "prospective-residual-sealed-reference-v3", "unexpected reference schema");
  assert(reference.status === "SEALED_BEFORE_REVIEWER_INFERENCE" && reference.visible_to_reviewer_routes === false, "reference sealing invariant failed");
  assert(reference.reviewer_route_model_calls_made === 0, "reviewer route ran before reference freeze");
  assert(reference.source_audit_sha256 === expectedInputSha256s.source_audit, "reference source-audit binding mismatch");
  assert(reference.audit_queue_sha256 === expectedInputSha256s.audit_queue, "reference queue binding mismatch");
  assert(reference.estimator_contract_sha256 === expectedInputSha256s.estimator_contract, "reference estimator binding mismatch");
  assert(reference.counts.items === 40 && reference.counts.scorable === 40, "reference coverage mismatch");
  assert(reference.counts.defects === 1 && reference.counts.no_defects === 39 && reference.counts.not_scorable === 0, "reference class counts mismatch");
  assert(JSON.stringify(reference.items.map(item => item.audit_id)) === JSON.stringify(queue.items.map(item => item.audit_id)), "reference order or coverage mismatch");
  assert(new Set(reference.items.map(item => item.audit_id)).size === 40, "reference audit_id values are not unique");
  const defects = reference.items.filter(item => item.y === 1);
  assert(defects.length === 1 && defects[0].audit_id === "R033" && defects[0].scoring_label === "DEFECT", "R033 unique-defect binding mismatch");
  const allowedReferenceItemKeys = ["audit_id", "canonical_revision_uid", "stratum", "scoring_label", "y", "scorable", "source_audit_item_sha256", "design_weight_exact"];
  for (const [index, item] of reference.items.entries()) {
    assert(JSON.stringify(Object.keys(item)) === JSON.stringify(allowedReferenceItemKeys), `${item.audit_id}: sealed reference is not minimal`);
    assert(item.source_audit_item_sha256 === sha256(JSON.stringify(audit.items[index])), `${item.audit_id}: source-audit item hash mismatch`);
    const expectedLabel = audit.items[index].verdict === "CONFIRMED" ? "DEFECT" : audit.items[index].verdict === "REFUTED" ? "NO_DEFECT" : "NOT_SCORABLE";
    assert(item.scoring_label === expectedLabel, `${item.audit_id}: reference label does not match source audit`);
  }
  const serializedReference = committedReference.toString("utf8");
  for (const forbiddenField of ["finding", "reason", "evidence_class", "defect_id", "target_span", "source_audit_verdict"]) {
    assert(!serializedReference.includes(`\"${forbiddenField}\"`), `sealed reference leaked ${forbiddenField}`);
  }

  assert(estimates.schema_version === "prospective-residual-reference-estimates-v3", "unexpected estimates schema");
  assert(estimates.status === "FROZEN_BEFORE_REVIEWER_INFERENCE" && estimates.visible_to_reviewer_routes === false, "estimate freeze invariant failed");
  assert(estimates.reviewer_route_model_calls_made === 0, "reviewer route ran before estimator freeze");
  assert(JSON.stringify(estimates.input_sha256s) === JSON.stringify({...expectedInputSha256s, sealed_reference: expectedOutputSha256s.sealed_reference}), "estimate input binding mismatch");
  assertFraction(estimates.overall.exact_weight_sum, "1396", "1", "overall weight sum");
  assertFraction(estimates.overall.confirmed_weighted_total, "16", "5", "HT confirmed total");
  assertFraction(estimates.overall.identification_bounds.lower, "4", "1745", "lower bound");
  assertFraction(estimates.overall.identification_bounds.upper, "4", "1745", "upper bound");
  assert(estimates.overall.point_estimates.global_availability_gate_pass === true, "point-estimate availability gate should pass");
  assert(estimates.overall.point_estimates.fully_determinate === true, "point-estimate availability mismatch");
  assertFraction(estimates.overall.point_estimates.horvitz_thompson_known_denominator, "4", "1745", "HT rate");
  assertFraction(estimates.overall.point_estimates.hajek_ratio, "4", "1745", "Hajek rate");
  assertFraction(estimates.overall.point_estimates.unweighted_sample_rate, "1", "40", "unweighted sample rate");
  assertFraction(estimates.by_stratum.same_family_only.point_estimates.horvitz_thompson_known_denominator, "16", "3665", "same-family rate");
  assertFraction(estimates.by_stratum.cross_or_mixed_family.point_estimates.horvitz_thompson_known_denominator, "0", "1", "cross-or-mixed rate");
  assertFraction(estimates.by_stratum.unknown_provenance.point_estimates.horvitz_thompson_known_denominator, "0", "1", "unknown-provenance rate");
  assert(estimates.feasibility_gates.determinate.pass === true, "determinate gate should pass");
  assertFraction(estimates.feasibility_gates.determinate.exact_rate, "1", "1", "determinate gate rate");
  assert(estimates.feasibility_gates.provenance_classifiable.pass === true && estimates.feasibility_gates.provenance_classifiable.unknown_items_retained === 2, "provenance gate mismatch");
  assertFraction(estimates.feasibility_gates.provenance_classifiable.exact_unweighted_rate, "19", "20", "provenance gate rate");
  assertFraction(estimates.feasibility_gates.provenance_classifiable.exact_design_weighted_share, "651", "698", "weighted provenance share");
  assert(estimates.feasibility_gates.origin_pilot_budget_priority.pass === false && estimates.feasibility_gates.origin_pilot_budget_priority.decision === "DEFER_ORIGIN_PILOT", "origin-pilot budget gate mismatch");

  const missingFixtureAudit = JSON.parse(auditBytes.toString("utf8"));
  for (const item of missingFixtureAudit.items.slice(0, 5)) {
    item.verdict = "INDETERMINATE";
    item.finding = null;
    item.reason = "Synthetic verifier fixture: missing reference outcome.";
  }
  missingFixtureAudit.counts.by_verdict = {CONFIRMED: 1, REFUTED: 34, INDETERMINATE: 5, UNREACHABLE: 0};
  missingFixtureAudit.counts.determinate_items = 35;
  missingFixtureAudit.counts.determinate_rate = 0.875;
  const missingFixtureAuditPath = path.join(temporaryDirectory, "SOURCE-AUDIT-MISSING-FIXTURE.json");
  const missingFixtureOutputDirectory = path.join(temporaryDirectory, "missing-fixture-output");
  fs.writeFileSync(missingFixtureAuditPath, `${JSON.stringify(missingFixtureAudit, null, 2)}\n`);
  execFileSync(process.execPath, [
    path.join(here, "build-reference.mjs"),
    "--out-dir", missingFixtureOutputDirectory,
    "--audit", missingFixtureAuditPath
  ], {stdio: "pipe", maxBuffer: 64 * 1024 * 1024});
  const missingFixtureEstimates = JSON.parse(fs.readFileSync(path.join(missingFixtureOutputDirectory, "REFERENCE-ESTIMATES.json"), "utf8"));
  assert(missingFixtureEstimates.feasibility_gates.determinate.pass === false, "synthetic 35/40 determinate gate should fail");
  for (const [scope, summary] of [["overall", missingFixtureEstimates.overall], ...Object.entries(missingFixtureEstimates.by_stratum)]) {
    assert(summary.point_estimates.global_availability_gate_pass === false, `${scope}: failed global availability gate was not propagated`);
    assert(summary.point_estimates.horvitz_thompson_known_denominator === null, `${scope}: HT point estimate leaked below 90% determinate`);
    assert(summary.point_estimates.hajek_ratio === null, `${scope}: Hajek point estimate leaked below 90% determinate`);
    assert(summary.point_estimates.unweighted_sample_rate === null, `${scope}: unweighted point estimate leaked below 90% determinate`);
    assert(summary.identification_bounds.lower !== null && summary.identification_bounds.upper !== null, `${scope}: missing-evidence bounds were suppressed`);
  }

  const brokenFrame = JSON.parse(frameBytes.toString("utf8"));
  const brokenTask = brokenFrame.tasks.find(task => task.stratum === "same_family_only" && task.task_inclusion_probability < 1);
  assert(brokenTask, "design-proof fixture task missing");
  brokenTask.task_inclusion_probability += 0.01;
  const brokenFramePath = path.join(temporaryDirectory, "FRAME-BROKEN-FIXTURE.json");
  fs.writeFileSync(brokenFramePath, `${JSON.stringify(brokenFrame, null, 2)}\n`);
  let brokenFrameRejected = false;
  try {
    execFileSync(process.execPath, [
      path.join(here, "build-reference.mjs"),
      "--out-dir", path.join(temporaryDirectory, "broken-frame-output"),
      "--frame", brokenFramePath
    ], {stdio: "pipe", maxBuffer: 64 * 1024 * 1024});
  } catch {
    brokenFrameRejected = true;
  }
  assert(brokenFrameRejected, "broken PPS design fixture was not rejected");

  for (const [name, bytes] of [["SEALED-REFERENCE.json", committedReference], ["REFERENCE-ESTIMATES.json", committedEstimates], ["ESTIMATOR-CONTRACT.json", contractBytes]]) {
    const serialized = bytes.toString("utf8");
    const forbiddenPatterns = [
      [/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/, "local absolute path"],
      [/(?:OPENAI|ANTHROPIC|GOOGLE|ZAI)_API_KEY/, "credential variable"],
      [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, "private key"],
      [/(?:sk|AIzaSy|xai)-[A-Za-z0-9_-]{16,}/, "credential-like token"]
    ];
    for (const [pattern, label] of forbiddenPatterns) assert(!pattern.test(serialized), `${name}: ${label} leaked`);
  }

  process.stdout.write(`${JSON.stringify({
    status: "PASS",
    output_sha256s: expectedOutputSha256s,
    weighted_prevalence: estimates.overall.point_estimates.horvitz_thompson_known_denominator,
    unweighted_sample_rate: estimates.overall.point_estimates.unweighted_sample_rate,
    origin_pilot_budget_priority: estimates.feasibility_gates.origin_pilot_budget_priority
  }, null, 2)}\n`);
} finally {
  const allowedPrefix = `${path.resolve(os.tmpdir())}${path.sep}prospective-residual-reference-v3-`;
  const resolvedTemporary = path.resolve(temporaryDirectory);
  if (!resolvedTemporary.startsWith(allowedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolvedTemporary, {recursive: true, force: true});
}
