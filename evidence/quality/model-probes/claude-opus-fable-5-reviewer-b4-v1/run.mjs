import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";

const routeName = process.argv[2];
const routes = {
  opus: {slug: "claude-opus-5-medium", model: "claude-opus-5"},
  fable: {slug: "claude-fable-5-medium", model: "claude-fable-5"}
};
if (!routes[routeName]) throw new Error("usage: node run.mjs opus|fable");
const route = routes[routeName];
const artifactSlug = `${route.slug}-no-advisor`;

const root = "/home/yun/research/tome4-agent-eval";
const outDir = path.join(root, "evidence/quality/model-probes/claude-opus-fable-5-reviewer-b4-v1");
const inputPath = path.join(root, "evidence/quality/p1-batches/p1-b4-mechanics-numeric.json");
const promptPath = path.join(outDir, "PROMPT.md");
const schemaPath = path.join(outDir, "REVIEWER-SCHEMA.json");
const rawPath = path.join(outDir, `RAW-${artifactSlug}.ndjson`);
const stderrPath = path.join(outDir, `RAW-${artifactSlug}.stderr.txt`);
const candidatePath = path.join(outDir, `CANDIDATE-${artifactSlug}.json`);

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
  if (actual !== expectedHashes[name]) throw new Error(`${name} hash mismatch: expected ${expectedHashes[name]}, got ${actual}`);
}
if ([rawPath, stderrPath, candidatePath].some(file => fs.existsSync(file))) {
  throw new Error(`refusing to overwrite an existing ${route.slug} artifact`);
}

const input = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const prompt = fs.readFileSync(promptPath, "utf8") + "\n输入 JSON：\n" + JSON.stringify(input);
const schema = fs.readFileSync(schemaPath, "utf8");
const cliSchemaObject = JSON.parse(schema);
delete cliSchemaObject.$schema;
const cliSchema = JSON.stringify(cliSchemaObject);
const version = spawnSync("claude", ["--version"], {cwd: "/tmp", encoding: "utf8"});
if (version.status !== 0 || !version.stdout.trim().startsWith("2.1.247 (Claude Code)")) {
  throw new Error(`unexpected Claude Code version: status=${version.status}, stdout=${JSON.stringify(version.stdout)}, stderr=${JSON.stringify(version.stderr)}`);
}

const args = [
  "--print",
  "--model", route.model,
  "--effort", "medium",
  "--output-format", "stream-json",
  "--verbose",
  "--no-session-persistence",
  "--safe-mode",
  "--setting-sources", "project,local",
  "--disable-slash-commands",
  "--permission-mode", "plan",
  "--tools", "",
  "--json-schema", cliSchema,
  "--",
  prompt
];
const started = Date.now();
const run = spawnSync("claude", args, {
  cwd: "/tmp",
  encoding: "utf8",
  maxBuffer: 64 * 1024 * 1024,
  timeout: 30 * 60 * 1000,
  env: {...process.env, NO_COLOR: "1"}
});
const durationSeconds = (Date.now() - started) / 1000;
if (run.stdout) fs.writeFileSync(rawPath, run.stdout);
if (run.stderr) fs.writeFileSync(stderrPath, run.stderr);
if (run.error) throw run.error;
if (run.status !== 0) throw new Error(`Claude Code failed: status=${run.status}, signal=${run.signal}, stderr=${run.stderr}`);

const events = run.stdout.split(/\r?\n/).filter(Boolean).map((line, index) => {
  try {
    return JSON.parse(line);
  } catch (error) {
    throw new Error(`invalid JSON event at line ${index + 1}: ${error}`);
  }
});
const initEvents = events.filter(event => event.type === "system" && event.subtype === "init");
const assistantEvents = events.filter(event => event.type === "assistant" && event.message);
const resultEvents = events.filter(event => event.type === "result");
if (initEvents.length !== 1) throw new Error(`expected one init event, got ${initEvents.length}`);
if (resultEvents.length !== 1) throw new Error(`expected one result event, got ${resultEvents.length}`);
const resultEvent = resultEvents[0];
const fallbackEvents = events.filter(event => event.type === "system" && /fallback/.test(event.subtype ?? ""));
const fallbackBlocks = assistantEvents.flatMap(event => event.message.content ?? []).filter(block => block.type === "fallback");
const actualModels = [...new Set(assistantEvents.map(event => event.message.model).filter(Boolean))];

let response = null;
let strictJson = true;
let parseError = null;
if (resultEvent.structured_output && typeof resultEvent.structured_output === "object") {
  response = resultEvent.structured_output;
} else {
  try {
    response = JSON.parse((resultEvent.result ?? "").trim());
  } catch (error) {
    strictJson = false;
    parseError = String(error);
  }
}

const candidate = {
  schema_version: 1,
  route: {
    harness: "Claude Code CLI 2.1.247",
    requested_model: route.model,
    requested_effort: "medium",
    setting_sources: "project,local",
    initialized_model: initEvents[0].model ?? null,
    actual_assistant_models: actualModels,
    provider: "firstParty"
  },
  duration_seconds: durationSeconds,
  exit_status: run.status,
  strict_json: strictJson,
  parse_error: parseError,
  fallback_events: fallbackEvents,
  fallback_blocks: fallbackBlocks,
  result_metadata: {
    is_error: resultEvent.is_error ?? null,
    subtype: resultEvent.subtype ?? null,
    stop_reason: resultEvent.stop_reason ?? null,
    terminal_reason: resultEvent.terminal_reason ?? null,
    usage: resultEvent.usage ?? null,
    model_usage: resultEvent.modelUsage ?? null,
    total_cost_usd: resultEvent.total_cost_usd ?? null,
    num_turns: resultEvent.num_turns ?? null,
    permission_denials: resultEvent.permission_denials ?? null,
    subagent_stats: resultEvent.subagent_stats ?? null
  },
  response
};
fs.writeFileSync(candidatePath, JSON.stringify(candidate, null, 2) + "\n");
process.stdout.write(JSON.stringify({...candidate, response: undefined, fallback_events: candidate.fallback_events.length, fallback_blocks: candidate.fallback_blocks.length}) + "\n");
