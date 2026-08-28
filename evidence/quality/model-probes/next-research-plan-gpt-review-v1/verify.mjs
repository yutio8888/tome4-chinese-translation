import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const experiment = JSON.parse(fs.readFileSync(path.join(here, "EXPERIMENT.json"), "utf8"));
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
for (const record of Object.values(experiment.frozen_inputs)) if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
for (const forbidden of ["/home/", "/Users/", "sealed reference", "adjudication conclusions", "defect ID"]) {
  const outbound = fs.readFileSync(path.join(here, "PLAN-CANDIDATE.md"), "utf8") + fs.readFileSync(path.join(here, "REVIEW-PROMPT.md"), "utf8");
  if (forbidden.startsWith("/") && outbound.includes(forbidden)) throw new Error(`outbound input leaks ${forbidden}`);
}
const resultFiles = ["RAW-codex-gpt-5.6-sol-high.json", "RAW-codex-gpt-5.6-sol-high.stderr.txt", "REVIEW-codex-gpt-5.6-sol-high.json", "SYNTHESIS.json", "PLAN-REVISED.md"];
if (resultFiles.some(file => fs.existsSync(path.join(here, file)))) throw new Error("post-review verification is not installed yet");
process.stdout.write("verified frozen independent-review plan, prompt, schema, runner and outbound sanitization before inference\n");
