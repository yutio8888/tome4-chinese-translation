import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.join(here, "../controlled-mutation-ui-log-replication-v2");
const routeName = process.argv[2];
const routes = {
  codex: {slug: "codex-gpt-5.6-sol-high", kind: "codex"},
  opus: {slug: "claude-opus-5-medium-no-advisor", kind: "claude"},
  glm: {slug: "pi-zai-cn-glm-5.3-flash-high", kind: "pi"},
  gemini: {slug: "agy-gemini-3.7-flash-high", kind: "agy"}
};
if (!routes[routeName]) throw new Error("usage: node run.mjs codex|opus|glm|gemini");
const route = routes[routeName];
const files = {input: path.join(base, "HOLDOUT.json"), prompt: path.join(base, "PROMPT.md"), schema: path.join(base, "REVIEWER-SCHEMA.json")};
const expectedHashes = {input: "526627e764bc24740e43f2263e7e007e0878ce519a837fe7a9b268b287fb3448", prompt: "38fcb6158eb02ccce90a3e5fa360304754a3a0285b90bd78737b523252d1e33e", schema: "39303de09ff9c6db795cf3d898a5219793cac468af5a7ded702ae83be85bac29"};
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
for (const [name, file] of Object.entries(files)) if (sha256(file) !== expectedHashes[name]) throw new Error(`${name} frozen hash mismatch`);
const rawPath = path.join(here, `RAW-${route.slug}.json`);
const stderrPath = path.join(here, `RAW-${route.slug}.stderr.txt`);
const candidatePath = path.join(here, `CANDIDATE-${route.slug}.json`);
if ([rawPath, stderrPath, candidatePath].some(file => fs.existsSync(file))) throw new Error(`refusing to overwrite ${route.slug} artifacts`);
const input = JSON.parse(fs.readFileSync(files.input, "utf8"));
const orderedIds = input.items.map(item => item.revision_id);
const prompt = `${fs.readFileSync(files.prompt, "utf8")}\n输入 JSON：\n${JSON.stringify(input)}`;
const schemaObject = JSON.parse(fs.readFileSync(files.schema, "utf8"));
function cliVersion(command) {
  const run = spawnSync(command, ["--version"], {cwd: "/tmp", encoding: "utf8"});
  if (run.status !== 0) throw new Error(`${command} --version failed: ${run.stderr}`);
  return run.stdout.trim();
}
function validateResponse(response) {
  const errors = [];
  if (!response || typeof response !== "object" || Array.isArray(response)) return ["response is not an object"];
  if (JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(["revisions"])) errors.push("top-level keys are not exactly revisions");
  if (!Array.isArray(response.revisions)) return [...errors, "revisions is not an array"];
  if (response.revisions.length !== orderedIds.length) errors.push(`expected ${orderedIds.length} revisions, got ${response.revisions.length}`);
  for (let index = 0; index < response.revisions.length; index += 1) {
    const revision = response.revisions[index];
    if (!revision || typeof revision !== "object" || Array.isArray(revision)) { errors.push(`revision ${index} is not an object`); continue; }
    if (JSON.stringify(Object.keys(revision).sort()) !== JSON.stringify(["evidence", "observation", "revision_id", "verdict"])) errors.push(`revision ${index} has unexpected keys`);
    if (revision.revision_id !== orderedIds[index]) errors.push(`revision ${index} expected ${orderedIds[index]}, got ${revision.revision_id}`);
    if (!["OK", "FINDING", "UNCERTAIN"].includes(revision.verdict)) errors.push(`revision ${index} invalid verdict`);
    if (typeof revision.observation !== "string" || !revision.observation) errors.push(`revision ${index} invalid observation`);
    if (typeof revision.evidence !== "string" || !revision.evidence) errors.push(`revision ${index} invalid evidence`);
  }
  return errors;
}

let command, args, lastPath = null, expectedVersion;
if (route.kind === "codex") {
  expectedVersion = "codex-cli 0.150.1";
  if (cliVersion("codex") !== expectedVersion) throw new Error("unexpected Codex CLI version");
  lastPath = path.join("/tmp", `ui-log-repeat-c-${route.slug}-${process.pid}.json`);
  command = "codex";
  args = ["exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"", "--ephemeral", "--ignore-rules", "--skip-git-repo-check", "-o", lastPath, "-C", "/tmp", "-s", "read-only", "--output-schema", files.schema, prompt];
} else if (route.kind === "claude") {
  expectedVersion = "2.1.247 (Claude Code)";
  if (cliVersion("claude") !== expectedVersion) throw new Error("unexpected Claude Code version");
  const cliSchema = structuredClone(schemaObject); delete cliSchema.$schema;
  command = "claude";
  args = ["--print", "--model", "claude-opus-5", "--effort", "medium", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--setting-sources", "project,local", "--disable-slash-commands", "--permission-mode", "plan", "--tools", "", "--json-schema", JSON.stringify(cliSchema), "--", prompt];
} else if (route.kind === "pi") {
  expectedVersion = "0.84.3";
  if (cliVersion("pi") !== expectedVersion) throw new Error("unexpected Pi version");
  command = "pi";
  args = ["--provider", "zai-standard-cn", "--model", "glm-5.3-flash", "--thinking", "high", "--no-tools", "--no-session", "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-themes", "--no-context-files", "--no-approve", "--mode", "json", "--print", prompt];
} else {
  expectedVersion = "1.1.22";
  if (cliVersion("agy") !== expectedVersion) throw new Error("unexpected Antigravity CLI version");
  command = "agy";
  args = ["-p", prompt, "--model", "gemini-3.7-flash-high", "--effort", "high", "--disable-slash-commands", "--output-format", "json", "--print-timeout", "15m", "--mode", "plan", "--sandbox", "--json-schema", files.schema];
}
const started = Date.now();
const run = spawnSync(command, args, {cwd: "/tmp", encoding: "utf8", maxBuffer: 64 * 1024 * 1024, timeout: 30 * 60 * 1000, env: {...process.env, NO_COLOR: "1", PI_SKIP_VERSION_CHECK: "1"}});
const durationSeconds = (Date.now() - started) / 1000;
if (run.stdout) fs.writeFileSync(rawPath, run.stdout);
if (run.stderr) fs.writeFileSync(stderrPath, run.stderr);
if (run.error) throw run.error;
if (run.status !== 0) throw new Error(`${command} failed: status=${run.status}, signal=${run.signal}, stderr=${run.stderr}`);

let response = null, parseError = null, routeMetadata = {};
if (route.kind === "codex") {
  try { response = JSON.parse(fs.readFileSync(lastPath, "utf8")); } catch (error) { parseError = String(error); } finally { if (lastPath && fs.existsSync(lastPath)) fs.unlinkSync(lastPath); }
  routeMetadata = {harness: expectedVersion, requested_model: "gpt-5.6-sol", requested_effort: "high", session: "ephemeral"};
} else if (route.kind === "claude") {
  let events = [];
  try { events = run.stdout.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line)); } catch (error) { parseError = `event parse failed: ${error}`; }
  if (!parseError) {
    const initEvents = events.filter(event => event.type === "system" && event.subtype === "init");
    const assistantEvents = events.filter(event => event.type === "assistant" && event.message);
    const resultEvents = events.filter(event => event.type === "result");
    const resultEvent = resultEvents.length === 1 ? resultEvents[0] : null;
    const fallbackEvents = events.filter(event => event.type === "system" && /fallback/.test(event.subtype ?? ""));
    const fallbackBlocks = assistantEvents.flatMap(event => event.message.content ?? []).filter(block => block.type === "fallback");
    if (resultEvent?.structured_output && typeof resultEvent.structured_output === "object") response = resultEvent.structured_output;
    else { try { response = JSON.parse((resultEvent?.result ?? "").trim()); } catch (error) { parseError = String(error); } }
    routeMetadata = {harness: `Claude Code CLI ${expectedVersion.split(" ")[0]}`, requested_model: "claude-opus-5", requested_effort: "medium", requested_advisor: null, initialized_models: initEvents.map(event => event.model ?? null), actual_assistant_models: [...new Set(assistantEvents.map(event => event.message.model).filter(Boolean))], fallback_event_count: fallbackEvents.length, fallback_block_count: fallbackBlocks.length, result: resultEvent ? {is_error: resultEvent.is_error ?? null, subtype: resultEvent.subtype ?? null, stop_reason: resultEvent.stop_reason ?? null, terminal_reason: resultEvent.terminal_reason ?? null, usage: resultEvent.usage ?? null, model_usage: resultEvent.modelUsage ?? null, total_cost_usd: resultEvent.total_cost_usd ?? null, num_turns: resultEvent.num_turns ?? null} : null};
  }
} else if (route.kind === "pi") {
  let events = [];
  try { events = run.stdout.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line)); } catch (error) { parseError = `event parse failed: ${error}`; }
  if (!parseError) {
    const messageEnds = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
    const message = messageEnds.length === 1 ? messageEnds[0].message : null;
    if (!message) parseError = `expected one assistant message_end, got ${messageEnds.length}`;
    else {
      const text = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
      try { response = JSON.parse(text.trim()); } catch (error) { parseError = String(error); }
      routeMetadata = {harness: `Pi ${expectedVersion}`, requested_provider: "zai-standard-cn", requested_model: "glm-5.3-flash", requested_effort: "high", actual_provider: message.provider ?? null, actual_model: message.model ?? null, usage: message.usage ?? null, stop_reason: message.stopReason ?? null};
    }
  }
} else {
  let envelope = null;
  try { envelope = JSON.parse(run.stdout); response = envelope.structured_output ?? JSON.parse(envelope.response); } catch (error) { parseError = String(error); }
  routeMetadata = {harness: `Antigravity CLI ${expectedVersion}`, requested_model: "gemini-3.7-flash-high", requested_effort: "high", mode: "plan", sandbox: true, reported_model: envelope?.model ?? null, reported_agent: envelope?.agent ?? null, usage: envelope?.usage ?? null};
}
const validationErrors = parseError ? [parseError] : validateResponse(response);
if (route.kind === "claude") {
  if (JSON.stringify(routeMetadata.initialized_models) !== JSON.stringify(["claude-opus-5"])) validationErrors.push("Claude initialized model mismatch");
  if (JSON.stringify(routeMetadata.actual_assistant_models) !== JSON.stringify(["claude-opus-5"])) validationErrors.push("Claude actual assistant model mismatch");
  if (routeMetadata.fallback_event_count !== 0 || routeMetadata.fallback_block_count !== 0) validationErrors.push("Claude fallback detected");
}
if (route.kind === "pi" && (routeMetadata.actual_provider !== "zai-standard-cn" || routeMetadata.actual_model !== "glm-5.3-flash")) validationErrors.push("Pi actual route mismatch");
const candidate = {schema_version: 1, run_label: "C", route: route.slug, route_metadata: routeMetadata, duration_seconds: durationSeconds, exit_status: run.status, valid: validationErrors.length === 0, validation_errors: validationErrors, verdict_counts: response?.revisions?.reduce((counts, revision) => { counts[revision.verdict] = (counts[revision.verdict] ?? 0) + 1; return counts; }, {}) ?? null, response};
fs.writeFileSync(candidatePath, `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: undefined}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 2;
