import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";

const root = "/home/yun/research/tome4-agent-eval";
const outDir = path.join(root, "evidence/quality/model-probes/glm-5-3-flash-reviewer-b4-v1");
const inputPath = path.join(root, "evidence/quality/p1-batches/p1-b4-mechanics-numeric.json");
const promptPath = path.join(outDir, "PROMPT.md");
const schemaPath = path.join(outDir, "REVIEWER-SCHEMA.json");
const rawPath = path.join(outDir, "RAW-pi-high.ndjson");
const candidatePath = path.join(outDir, "CANDIDATE-pi-high.json");

const expectedHashes = {
  input: "9034f605bcf471bd7fce0d603ee52c6a8d5fbb9b2807e2b801b9fb52316ee332",
  prompt: "05cee8f6006f3b3ba7bf6a653753f2b8aa0a33ce063d576b5387216309f0103d",
  schema: "a006f81a00d2243bec90865b24409e45050bf8f6e473399a4df0889b6fed804f"
};

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

for (const [name, file] of Object.entries({input: inputPath, prompt: promptPath, schema: schemaPath})) {
  const actual = sha256(file);
  if (actual !== expectedHashes[name]) {
    throw new Error(`${name} hash mismatch: expected ${expectedHashes[name]}, got ${actual}`);
  }
}
if (fs.existsSync(rawPath) || fs.existsSync(candidatePath)) {
  throw new Error("refusing to overwrite an existing inference artifact");
}

const inputText = fs.readFileSync(inputPath, "utf8");
const input = JSON.parse(inputText);
const prompt = fs.readFileSync(promptPath, "utf8") + "\n输入 JSON：\n" + JSON.stringify(input);
const version = spawnSync("pi", ["--version"], {cwd: "/tmp", encoding: "utf8"});
if (version.status !== 0 || version.stdout.trim() !== "0.84.3") {
  throw new Error(`unexpected Pi version: status=${version.status}, stdout=${JSON.stringify(version.stdout)}, stderr=${JSON.stringify(version.stderr)}`);
}

const args = [
  "--provider", "zai-standard-cn",
  "--model", "glm-5.3-flash",
  "--thinking", "high",
  "--no-tools",
  "--no-session",
  "--no-extensions",
  "--no-skills",
  "--no-prompt-templates",
  "--no-themes",
  "--no-context-files",
  "--no-approve",
  "--mode", "json",
  "--print",
  prompt
];

const started = Date.now();
const run = spawnSync("pi", args, {
  cwd: "/tmp",
  encoding: "utf8",
  maxBuffer: 64 * 1024 * 1024,
  timeout: 30 * 60 * 1000,
  env: {...process.env, NO_COLOR: "1", PI_SKIP_VERSION_CHECK: "1"}
});
const durationSeconds = (Date.now() - started) / 1000;

if (run.stdout) fs.writeFileSync(rawPath, run.stdout);
if (run.error) throw run.error;
if (run.status !== 0) {
  throw new Error(`Pi failed: status=${run.status}, signal=${run.signal}, stderr=${run.stderr}`);
}

const events = run.stdout.split(/\r?\n/).filter(Boolean).map((line, index) => {
  try {
    return JSON.parse(line);
  } catch (error) {
    throw new Error(`invalid JSON event at line ${index + 1}: ${error}`);
  }
});
const messageEnds = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
if (messageEnds.length !== 1) throw new Error(`expected one assistant message_end, got ${messageEnds.length}`);
const message = messageEnds[0].message;
const visibleText = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
let response;
let strictJson = true;
let parseError = null;
try {
  response = JSON.parse(visibleText.trim());
} catch (error) {
  strictJson = false;
  parseError = String(error);
  response = null;
}
const candidate = {
  schema_version: 1,
  route: {
    harness: "pi 0.84.3",
    requested_provider: "zai-standard-cn",
    requested_model: "glm-5.3-flash",
    requested_thinking: "high",
    actual_provider: message.provider ?? null,
    actual_model: message.model ?? null
  },
  duration_seconds: durationSeconds,
  exit_status: run.status,
  strict_json: strictJson,
  parse_error: parseError,
  usage: message.usage ?? null,
  stop_reason: message.stopReason ?? null,
  response
};
fs.writeFileSync(candidatePath, JSON.stringify(candidate, null, 2) + "\n");
process.stdout.write(JSON.stringify({...candidate, response: undefined}) + "\n");
