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

const experiment = json("EXPERIMENT.json");
for (const record of Object.values(experiment.frozen_inputs)) {
  check(sha256(record.path) === record.sha256, `${record.path} frozen hash mismatch`);
}

const outbound = ["PLAN-UNDER-REVIEW.md", "REVIEW-PROMPT.md", "REVIEW-SCHEMA.json", "SUBAGENT-TASK.md"]
  .map(text)
  .join("\n");
for (const forbidden of ["/home/", "/Users/", "95a6328c", "b77d337d", "d1e9515", "078c558"]) {
  check(!outbound.includes(forbidden), `outbound input leaks ${forbidden}`);
}
check(!text("PLAN-UNDER-REVIEW.md").includes("经独立 GPT-5.6 Sol"), "reviewer provenance was not removed from the plan");
check(experiment.route.mechanism === "collaboration.spawn_agent", "unexpected route mechanism");
check(experiment.route.model === "gpt-5.6-sol", "unexpected route model");
check(experiment.route.reasoning_effort === "high", "unexpected route effort");
check(experiment.route.fork_turns === "none", "review route is not fresh");

const postReview = [experiment.output.raw, experiment.output.adjudication, experiment.output.result];
if (postReview.every(file => !fs.existsSync(path.join(here, file)))) {
  process.stdout.write("verified frozen v2 re-review inputs, sanitization, route and pre-inference state\n");
  process.exit(0);
}

check(postReview.every(file => fs.existsSync(path.join(here, file))), "post-review artifact set is incomplete");
const schema = json("REVIEW-SCHEMA.json");
const raw = json(experiment.output.raw);
const expectedTop = [...schema.required].sort();
check(JSON.stringify(Object.keys(raw).sort()) === JSON.stringify(expectedTop), "raw review top-level schema mismatch");
check(schema.properties.overall_verdict.enum.includes(raw.overall_verdict), "invalid overall verdict");
for (const collection of [raw.fatal_issues, raw.major_issues, raw.cross_phase_issues]) {
  check(Array.isArray(collection), "issue collection is not an array");
  for (const issue of collection) {
    check(JSON.stringify(Object.keys(issue).sort()) === JSON.stringify([...schema.$defs.issue.required].sort()), "issue schema mismatch");
  }
}
check(raw.phase_assessments.length === 4, "expected exactly four phase assessments");
for (const phase of raw.phase_assessments) {
  check(schema.properties.phase_assessments.items.properties.verdict.enum.includes(phase.verdict), "invalid phase verdict");
}
for (const gate of raw.gate_audit) {
  check(schema.properties.gate_audit.items.properties.verdict.enum.includes(gate.verdict), "invalid gate verdict");
}

const adjudication = json(experiment.output.adjudication);
const result = json(experiment.output.result);
check(adjudication.status === "COMPLETE", "adjudication is incomplete");
check(adjudication.raw_sha256 === sha256(experiment.output.raw), "adjudication raw hash mismatch");
check(result.status === "COMPLETE", "result is incomplete");
check(result.raw_sha256 === sha256(experiment.output.raw), "result raw hash mismatch");
check(result.adjudication_sha256 === sha256(experiment.output.adjudication), "result adjudication hash mismatch");
if (result.final_plan) check(result.final_plan_sha256 === sha256(result.final_plan), "result final-plan hash mismatch");

process.stdout.write("verified frozen v2 inputs, subagent review, local adjudication and result hashes\n");
