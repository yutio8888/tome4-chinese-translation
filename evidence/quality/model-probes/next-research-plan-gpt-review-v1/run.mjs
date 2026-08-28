import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const files = {
  plan: path.join(here, "PLAN-CANDIDATE.md"),
  prompt: path.join(here, "REVIEW-PROMPT.md"),
  schema: path.join(here, "REVIEW-SCHEMA.json")
};
const expectedHashes = {
  plan: "f0a1ea6d2dad69dd2d53ad3ea6481c0a889e882a603688c7a2809a3f5d6cc056",
  prompt: "df129d56756cc98c156a8e250c3b9dff577ce505eb65950511d2d26b31f0eef8",
  schema: "7ba334dec692ca6a0687349ce0c24def95ea88a9c56b7ff9d485b1622fb60526"
};
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
for (const [name, file] of Object.entries(files)) if (sha256(file) !== expectedHashes[name]) throw new Error(`${name} frozen hash mismatch`);

const slug = "codex-gpt-5.6-sol-high";
const rawPath = path.join(here, `RAW-${slug}.json`);
const stderrPath = path.join(here, `RAW-${slug}.stderr.txt`);
const reviewPath = path.join(here, `REVIEW-${slug}.json`);
if ([rawPath, stderrPath, reviewPath].some(file => fs.existsSync(file))) throw new Error("refusing to overwrite independent review artifacts");

const plan = fs.readFileSync(files.plan, "utf8");
const promptTemplate = fs.readFileSync(files.prompt, "utf8");
if ((promptTemplate.match(/\{\{PLAN_CANDIDATE\}\}/g) ?? []).length !== 1) throw new Error("prompt placeholder mismatch");
const prompt = promptTemplate.replace("{{PLAN_CANDIDATE}}", plan);
const version = spawnSync("codex", ["--version"], {cwd: "/tmp", encoding: "utf8"});
if (version.status !== 0 || version.stdout.trim() !== "codex-cli 0.150.1") throw new Error(`unexpected Codex CLI version: ${version.stdout} ${version.stderr}`);
const lastPath = path.join("/tmp", `next-plan-review-${process.pid}.json`);
const args = [
  "exec",
  "-m", "gpt-5.6-sol",
  "-c", "model_reasoning_effort=\"high\"",
  "--ephemeral",
  "--ignore-rules",
  "--skip-git-repo-check",
  "-o", lastPath,
  "-C", "/tmp",
  "-s", "read-only",
  "--output-schema", files.schema,
  prompt
];
const started = Date.now();
const run = spawnSync("codex", args, {cwd: "/tmp", encoding: "utf8", maxBuffer: 64 * 1024 * 1024, timeout: 30 * 60 * 1000, env: {...process.env, NO_COLOR: "1"}});
const durationSeconds = (Date.now() - started) / 1000;
if (run.stdout) fs.writeFileSync(rawPath, run.stdout);
if (run.stderr) fs.writeFileSync(stderrPath, run.stderr);
if (run.error) throw run.error;
if (run.status !== 0) throw new Error(`codex failed: status=${run.status}, signal=${run.signal}, stderr=${run.stderr}`);

let response = null;
const validationErrors = [];
try {
  response = JSON.parse(fs.readFileSync(lastPath, "utf8"));
} catch (error) {
  validationErrors.push(`response parse failed: ${error}`);
} finally {
  if (fs.existsSync(lastPath)) fs.unlinkSync(lastPath);
}
const expectedKeys = ["accepted_elements", "fatal_issues", "go_no_go", "major_issues", "minor_issues", "overall_assessment", "recommended_plan", "uncertainties"];
if (response && JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(expectedKeys)) validationErrors.push("top-level response keys mismatch");
for (const key of ["fatal_issues", "major_issues", "minor_issues", "accepted_elements", "go_no_go", "uncertainties"]) if (response && !Array.isArray(response[key])) validationErrors.push(`${key} is not an array`);
if (response && (typeof response.overall_assessment !== "string" || !response.recommended_plan || typeof response.recommended_plan !== "object")) validationErrors.push("assessment or recommended_plan is invalid");

const candidate = {
  schema_version: 1,
  route: slug,
  route_metadata: {harness: "codex-cli 0.150.1", requested_model: "gpt-5.6-sol", requested_effort: "high", session: "ephemeral", working_directory: "/tmp", repository_context: false},
  duration_seconds: durationSeconds,
  exit_status: run.status,
  valid: validationErrors.length === 0,
  validation_errors: validationErrors,
  response
};
fs.writeFileSync(reviewPath, `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: undefined}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 2;
