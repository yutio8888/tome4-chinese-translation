import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = file => fs.readFileSync(path.join(here, file));
const text = file => read(file).toString("utf8");
const json = file => JSON.parse(text(file));
const sha256 = file => crypto.createHash("sha256").update(read(file)).digest("hex");
const check = (condition, message) => {
  if (!condition) throw new Error(message);
};
const sameKeys = (actual, expected, label) => {
  check(JSON.stringify(Object.keys(actual).sort()) === JSON.stringify([...expected].sort()), `${label} keys mismatch`);
};
const allStrings = (values, label) => {
  check(Array.isArray(values) && values.every(value => typeof value === "string"), `${label} must be an array of strings`);
};

const experiment = json("EXPERIMENT.json");
for (const record of Object.values(experiment.frozen_inputs)) {
  check(sha256(record.path) === record.sha256, `${record.path} frozen hash mismatch`);
}

const outbound = text("PLAN-CANDIDATE.md") + text("REVIEW-PROMPT.md");
for (const forbidden of ["/home/", "/Users/"]) {
  check(!outbound.includes(forbidden), `outbound input leaks ${forbidden}`);
}

const schema = json("REVIEW-SCHEMA.json");
const raw = json("RAW-subagent-gpt-5.6-sol-high.json");
sameKeys(raw, schema.required, "raw review top-level");
check(raw.fatal_issues.length === 2, "unexpected fatal issue count");
check(raw.major_issues.length === 8, "unexpected major issue count");
check(raw.minor_issues.length === 6, "unexpected minor issue count");
for (const issue of [...raw.fatal_issues, ...raw.major_issues]) {
  sameKeys(issue, schema.$defs.issue.required, "review issue");
  check(Object.values(issue).every(value => typeof value === "string"), "review issue fields must be strings");
}
check(raw.recommended_plan.sequence.length === 4, "review plan must contain four phases");
sameKeys(raw.recommended_plan, schema.properties.recommended_plan.required, "recommended plan");
for (const phase of raw.recommended_plan.sequence) {
  sameKeys(phase, schema.properties.recommended_plan.properties.sequence.items.required, "recommended phase");
  check(Object.values(phase).every(value => typeof value === "string"), "recommended phase fields must be strings");
}
allStrings(raw.minor_issues, "minor issues");
allStrings(raw.accepted_elements, "accepted elements");
allStrings(raw.recommended_plan.analysis, "recommended analysis");
allStrings(raw.recommended_plan.stopping_rules, "recommended stopping rules");
allStrings(raw.uncertainties, "uncertainties");
for (const gate of raw.go_no_go) {
  sameKeys(gate, schema.properties.go_no_go.items.required, "go/no-go gate");
  check(Object.values(gate).every(value => typeof value === "string"), "go/no-go fields must be strings");
}

const method = json("METHOD-OVERRIDE.json");
check(method.abandoned_cli_attempts.count === 2, "CLI interruption count mismatch");
check(method.abandoned_cli_attempts.valid_results === 0, "abandoned CLI result must not be evidence");
check(method.actual_review_route.mechanism === "collaboration.spawn_agent", "unexpected review mechanism");
check(method.actual_review_route.model === "gpt-5.6-sol", "unexpected review model");
check(method.actual_review_route.reasoning_effort === "high", "unexpected reasoning effort");
check(method.actual_review_route.fork_turns === "none", "review was not context-independent");

const synthesis = json("SYNTHESIS.json");
check(synthesis.status === "COMPLETE", "synthesis is not complete");
check(synthesis.reviewer.raw_output_sha256 === sha256(synthesis.reviewer.raw_output), "synthesis raw hash mismatch");
check(synthesis.decisions.length === 14, "unexpected synthesis decision count");
const calculatedDispositions = synthesis.decisions.reduce((counts, decision) => {
  check(["ACCEPTED", "MODIFIED", "REJECTED"].includes(decision.disposition), `invalid disposition ${decision.disposition}`);
  counts[decision.disposition] += 1;
  return counts;
}, {ACCEPTED: 0, MODIFIED: 0, REJECTED: 0});
check(JSON.stringify(calculatedDispositions) === JSON.stringify(synthesis.disposition_counts), "synthesis disposition counts mismatch");
check(text("PLAN-REVISED.md").includes("操作性 reviewer × origin interaction"), "revised plan does not downgrade the origin estimand");
check(text("PLAN-REVISED.md").includes("不能把“两个 generation replicates 分别同方向”作为独立 gate"), "revised plan did not record the rejected generation gate");

const result = json("RESULT.json");
check(result.status === "COMPLETE", "result is not complete");
check(result.execution.transport === "codex_builtin_subagent", "result transport mismatch");
check(result.execution.valid_cli_results === 0, "result incorrectly counts an interrupted CLI attempt");
check(result.execution.method_override_sha256 === sha256(result.execution.method_override), "method override hash mismatch");
check(result.execution.interruption_record_sha256 === sha256(result.execution.interruption_record), "interruption record hash mismatch");
check(result.review.raw_sha256 === sha256(result.review.raw), "raw review hash mismatch");
check(result.review.fatal_issues === raw.fatal_issues.length, "result fatal count mismatch");
check(result.review.major_issues === raw.major_issues.length, "result major count mismatch");
check(result.review.minor_issues === raw.minor_issues.length, "result minor count mismatch");
check(result.synthesis.sha256 === sha256(result.synthesis.artifact), "synthesis hash mismatch");
check(result.revised_plan.sha256 === sha256(result.revised_plan.artifact), "revised plan hash mismatch");
check(result.synthesis.accepted === calculatedDispositions.ACCEPTED, "accepted count mismatch");
check(result.synthesis.modified === calculatedDispositions.MODIFIED, "modified count mismatch");
check(result.synthesis.rejected === calculatedDispositions.REJECTED, "rejected count mismatch");

for (const forbiddenResult of [
  "RAW-codex-gpt-5.6-sol-high.json",
  "RAW-codex-gpt-5.6-sol-high.stderr.txt",
  "REVIEW-codex-gpt-5.6-sol-high.json"
]) {
  check(!fs.existsSync(path.join(here, forbiddenResult)), `${forbiddenResult} must not exist after interrupted CLI attempts`);
}

process.stdout.write("verified frozen inputs, built-in subagent review, critical synthesis, revised plan and result hashes\n");
