import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const routeName = process.argv[2];
const routes = {
  codex: {slug: "codex-gpt-5.6-sol-high", kind: "codex"},
  opus: {slug: "claude-opus-5-medium-no-advisor", kind: "claude", model: "claude-opus-5"},
  fable: {slug: "claude-fable-5-medium-no-advisor", kind: "claude", model: "claude-fable-5"},
  "opus-advisor": {slug: "claude-opus-5-medium-fable-advisor", kind: "claude", model: "claude-opus-5", advisor: "fable"},
  glm: {slug: "pi-zai-cn-glm-5.3-flash-high", kind: "pi"}
};
if (!routes[routeName]) throw new Error("usage: node run.mjs codex|opus|fable|opus-advisor|glm");
const route = routes[routeName];

const files = {
  input: path.join(here, "HOLDOUT.json"),
  prompt: path.join(here, "PROMPT.md"),
  schema: path.join(here, "REVIEWER-SCHEMA.json")
};
const expectedHashes = {
  input: "301a17085582e3d5d32dfc35f920fa419d01613c4835d227f855322e2384221d",
  prompt: "d0ea8afa632e554041ad98245bfe4d5036ce702baddfdc02d22162f9e4bef63a",
  schema: "90a8b74ce6287a2a43405f93996665428fb0fff06d0ff06e71eb423fc2063536"
};
function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}
for (const [name, file] of Object.entries(files)) {
  const actual = sha256(file);
  if (actual !== expectedHashes[name]) throw new Error(`${name} hash mismatch: expected ${expectedHashes[name]}, got ${actual}`);
}

const rawPath = path.join(here, `RAW-${route.slug}.ndjson`);
const stderrPath = path.join(here, `RAW-${route.slug}.stderr.txt`);
const candidatePath = path.join(here, `CANDIDATE-${route.slug}.json`);
if ([rawPath, stderrPath, candidatePath].some(file => fs.existsSync(file))) {
  throw new Error(`refusing to overwrite an existing ${route.slug} artifact`);
}

const input = JSON.parse(fs.readFileSync(files.input, "utf8"));
const orderedIds = input.items.map(item => item.revision_id);
const prompt = `${fs.readFileSync(files.prompt, "utf8")}\n输入 JSON：\n${JSON.stringify(input)}`;
const schemaObject = JSON.parse(fs.readFileSync(files.schema, "utf8"));

function validateResponse(response) {
  const errors = [];
  if (!response || typeof response !== "object" || Array.isArray(response)) return ["response is not an object"];
  if (JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(["revisions"])) errors.push("top-level keys are not exactly revisions");
  if (!Array.isArray(response.revisions)) return [...errors, "revisions is not an array"];
  if (response.revisions.length !== orderedIds.length) errors.push(`expected ${orderedIds.length} revisions, got ${response.revisions.length}`);
  for (let index = 0; index < response.revisions.length; index += 1) {
    const revision = response.revisions[index];
    if (!revision || typeof revision !== "object" || Array.isArray(revision)) {
      errors.push(`revision ${index} is not an object`);
      continue;
    }
    if (JSON.stringify(Object.keys(revision).sort()) !== JSON.stringify(["evidence", "observation", "revision_id", "verdict"])) {
      errors.push(`revision ${index} has unexpected keys`);
    }
    if (revision.revision_id !== orderedIds[index]) errors.push(`revision ${index} expected ${orderedIds[index]}, got ${revision.revision_id}`);
    if (!["OK", "FINDING", "UNCERTAIN"].includes(revision.verdict)) errors.push(`revision ${index} has invalid verdict`);
    if (typeof revision.observation !== "string" || revision.observation.length === 0) errors.push(`revision ${index} has invalid observation`);
    if (typeof revision.evidence !== "string" || revision.evidence.length === 0) errors.push(`revision ${index} has invalid evidence`);
  }
  return errors;
}

function cliVersion(command) {
  const run = spawnSync(command, ["--version"], {cwd: "/tmp", encoding: "utf8"});
  if (run.status !== 0) throw new Error(`${command} --version failed: ${run.stderr}`);
  return run.stdout.trim();
}

let command;
let args;
let lastPath = null;
let expectedVersion;
if (route.kind === "codex") {
  expectedVersion = "codex-cli 0.150.1";
  if (cliVersion("codex") !== expectedVersion) throw new Error("unexpected Codex CLI version");
  lastPath = path.join("/tmp", `paseo-residual-${route.slug}-${process.pid}.json`);
  command = "codex";
  args = [
    "exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"",
    "--ephemeral", "--ignore-rules", "--skip-git-repo-check", "-o", lastPath,
    "-C", "/tmp", "-s", "read-only", "--output-schema", files.schema, prompt
  ];
} else if (route.kind === "claude") {
  expectedVersion = "2.1.247 (Claude Code)";
  if (cliVersion("claude") !== expectedVersion) throw new Error("unexpected Claude Code version");
  const cliSchema = structuredClone(schemaObject);
  delete cliSchema.$schema;
  command = "claude";
  args = [
    "--print", "--model", route.model, "--effort", "medium",
    "--output-format", "stream-json", "--verbose", "--no-session-persistence",
    "--safe-mode", "--setting-sources", "project,local", "--disable-slash-commands",
    "--permission-mode", "plan", "--tools", "", "--json-schema", JSON.stringify(cliSchema)
  ];
  if (route.advisor) args.push("--advisor", route.advisor);
  args.push("--", prompt);
} else {
  expectedVersion = "0.84.3";
  if (cliVersion("pi") !== expectedVersion) throw new Error("unexpected Pi version");
  command = "pi";
  args = [
    "--provider", "zai-standard-cn", "--model", "glm-5.3-flash", "--thinking", "high",
    "--no-tools", "--no-session", "--no-extensions", "--no-skills", "--no-prompt-templates",
    "--no-themes", "--no-context-files", "--no-approve", "--mode", "json", "--print", prompt
  ];
}

const started = Date.now();
const run = spawnSync(command, args, {
  cwd: "/tmp",
  encoding: "utf8",
  maxBuffer: 64 * 1024 * 1024,
  timeout: 30 * 60 * 1000,
  env: {...process.env, NO_COLOR: "1", PI_SKIP_VERSION_CHECK: "1"}
});
const durationSeconds = (Date.now() - started) / 1000;
if (run.stdout) fs.writeFileSync(rawPath, run.stdout);
if (run.stderr) fs.writeFileSync(stderrPath, run.stderr);
if (run.error) throw run.error;
if (run.status !== 0) throw new Error(`${command} failed: status=${run.status}, signal=${run.signal}, stderr=${run.stderr}`);

let response = null;
let routeMetadata = {};
let parseError = null;
if (route.kind === "codex") {
  try {
    response = JSON.parse(fs.readFileSync(lastPath, "utf8"));
  } catch (error) {
    parseError = String(error);
  } finally {
    if (lastPath && fs.existsSync(lastPath)) fs.unlinkSync(lastPath);
  }
  routeMetadata = {
    harness: expectedVersion,
    requested_model: "gpt-5.6-sol",
    requested_effort: "high",
    session: "ephemeral"
  };
} else {
  let events = [];
  try {
    events = run.stdout.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
  } catch (error) {
    parseError = `event parse failed: ${error}`;
  }
  if (route.kind === "claude" && !parseError) {
    const initEvents = events.filter(event => event.type === "system" && event.subtype === "init");
    const assistantEvents = events.filter(event => event.type === "assistant" && event.message);
    const resultEvents = events.filter(event => event.type === "result");
    const resultEvent = resultEvents.length === 1 ? resultEvents[0] : null;
    const fallbackEvents = events.filter(event => event.type === "system" && /fallback/.test(event.subtype ?? ""));
    const fallbackBlocks = assistantEvents.flatMap(event => event.message.content ?? []).filter(block => block.type === "fallback");
    if (resultEvent?.structured_output && typeof resultEvent.structured_output === "object") {
      response = resultEvent.structured_output;
    } else {
      try {
        response = JSON.parse((resultEvent?.result ?? "").trim());
      } catch (error) {
        parseError = String(error);
      }
    }
    routeMetadata = {
      harness: `Claude Code CLI ${expectedVersion.split(" ")[0]}`,
      requested_model: route.model,
      requested_effort: "medium",
      requested_advisor: route.advisor === "fable" ? "claude-fable-5" : null,
      initialized_models: initEvents.map(event => event.model ?? null),
      actual_assistant_models: [...new Set(assistantEvents.map(event => event.message.model).filter(Boolean))],
      fallback_event_count: fallbackEvents.length,
      fallback_block_count: fallbackBlocks.length,
      result: resultEvent ? {
        is_error: resultEvent.is_error ?? null,
        subtype: resultEvent.subtype ?? null,
        stop_reason: resultEvent.stop_reason ?? null,
        terminal_reason: resultEvent.terminal_reason ?? null,
        usage: resultEvent.usage ?? null,
        model_usage: resultEvent.modelUsage ?? null,
        total_cost_usd: resultEvent.total_cost_usd ?? null,
        num_turns: resultEvent.num_turns ?? null,
        permission_denials: resultEvent.permission_denials ?? null
      } : null
    };
  } else if (route.kind === "pi" && !parseError) {
    const messageEnds = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
    const message = messageEnds.length === 1 ? messageEnds[0].message : null;
    if (!message) {
      parseError = `expected one assistant message_end, got ${messageEnds.length}`;
    } else {
      const visibleText = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
      try {
        response = JSON.parse(visibleText.trim());
      } catch (error) {
        parseError = String(error);
      }
      routeMetadata = {
        harness: `Pi ${expectedVersion}`,
        requested_provider: "zai-standard-cn",
        requested_model: "glm-5.3-flash",
        requested_effort: "high",
        actual_provider: message.provider ?? null,
        actual_model: message.model ?? null,
        usage: message.usage ?? null,
        stop_reason: message.stopReason ?? null
      };
    }
  }
}

const validationErrors = parseError ? [parseError] : validateResponse(response);
if (route.kind === "claude") {
  if (routeMetadata.initialized_models?.length !== 1 || routeMetadata.initialized_models[0] !== route.model) {
    validationErrors.push("Claude initialized model mismatch");
  }
  if (JSON.stringify(routeMetadata.actual_assistant_models) !== JSON.stringify([route.model])) {
    validationErrors.push("Claude actual assistant model mismatch");
  }
  if (routeMetadata.fallback_event_count !== 0 || routeMetadata.fallback_block_count !== 0) {
    validationErrors.push("Claude fallback detected");
  }
}
if (route.kind === "pi" && routeMetadata.actual_model !== "glm-5.3-flash") {
  validationErrors.push(`Pi actual model mismatch: ${routeMetadata.actual_model}`);
}

const candidate = {
  schema_version: 1,
  route: route.slug,
  route_metadata: routeMetadata,
  duration_seconds: durationSeconds,
  exit_status: run.status,
  valid: validationErrors.length === 0,
  validation_errors: validationErrors,
  verdict_counts: response?.revisions?.reduce((counts, revision) => {
    counts[revision.verdict] = (counts[revision.verdict] ?? 0) + 1;
    return counts;
  }, {}) ?? null,
  response
};
fs.writeFileSync(candidatePath, `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: undefined}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 2;
