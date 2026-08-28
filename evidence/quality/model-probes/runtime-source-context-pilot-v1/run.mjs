import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const [armRaw, runRaw, routeName, ...rest] = process.argv.slice(2);
const arm = armRaw?.toUpperCase();
const runNumber = Number(runRaw);
const attemptIndex = rest.indexOf("--attempt");
const attempt = attemptIndex === -1 ? 1 : Number(rest[attemptIndex + 1]);
const routes = {
  codex: {slug: "codex-gpt-5.6-sol-high", kind: "codex"},
  opus: {slug: "claude-opus-5-medium-no-advisor", kind: "claude"},
  glm: {slug: "pi-zai-cn-glm-5.3-flash-high", kind: "pi"},
  gemini: {slug: "agy-gemini-3.7-flash-high", kind: "agy"}
};
if (!["A", "B"].includes(arm) || ![1, 2].includes(runNumber) || !routes[routeName] || !Number.isInteger(attempt) || attempt < 1) {
  throw new Error("usage: node run.mjs A|B 1|2 codex|opus|glm|gemini [--attempt N]");
}
const route = routes[routeName];
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
const parseModelJson = text => {
  const trimmed = text.trim();
  const fenced = trimmed.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/i);
  return JSON.parse(fenced ? fenced[1] : trimmed);
};
const normalizePiResponse = response => {
  const revisions = Array.isArray(response) ? response : response?.revisions ?? response?.items;
  if (!Array.isArray(revisions)) return response;
  return {revisions: revisions.map(item => {
    const normalized = item && typeof item === "object" && "result" in item && !("verdict" in item) ? (({result, ...rest}) => ({...rest, verdict: result}))(item) : {...item};
    if (normalized.description === "placeholder") delete normalized.description;
    return normalized;
  })};
};

const frozenPath = path.join(here, "FROZEN-HASHES.json");
if (!fs.existsSync(frozenPath)) throw new Error("FROZEN-HASHES.json missing; inference is not frozen");
const frozen = readJson(frozenPath);
for (const [name, expected] of Object.entries(frozen.files)) {
  const file = path.join(here, name);
  if (!fs.existsSync(file) || sha256File(file) !== expected) throw new Error(`${name}: frozen hash mismatch`);
}

const files = {
  input: path.join(here, `HOLDOUT-${arm}.json`),
  prompt: path.join(here, "PROMPT.md"),
  schema: path.join(here, "REVIEWER-SCHEMA.json")
};
const input = readJson(files.input);
const orderedIds = input.items.map(item => item.revision_id);
const prompt = `${fs.readFileSync(files.prompt, "utf8")}\n输入 JSON：\n${JSON.stringify(input)}`;
const requestSha256 = sha256Bytes(prompt);
const outboundScan = `${fs.readFileSync(files.prompt, "utf8")}\n${JSON.stringify(input)}`;
const forbiddenPatterns = [
  [/\/(?:home|Users)\//, "local absolute path"],
  [/expected_claim/i, "expected claim"],
  [/mutation_id/i, "mutation identifier"],
  [/REFERENCE\.json/i, "sealed reference name"],
  [/SOURCE-VERIFICATION\.json/i, "verification artifact name"],
  [/[0-9a-f]{40,64}/i, "commit or content hash"]
];
for (const [pattern, label] of forbiddenPatterns) if (pattern.test(outboundScan)) throw new Error(`outbound sanitization failed: ${label}`);

const callStem = `${arm}-run${runNumber}-${route.slug}`;
const rawPath = path.join(here, `RAW-${callStem}-attempt${attempt}.json`);
const stderrPath = path.join(here, `RAW-${callStem}-attempt${attempt}.stderr.txt`);
const candidatePath = path.join(here, `CANDIDATE-${callStem}.json`);
const failurePath = path.join(here, `FAILURE-${callStem}-attempt${attempt}.json`);
for (const file of [rawPath, stderrPath, failurePath]) if (fs.existsSync(file)) throw new Error(`refusing to overwrite ${path.basename(file)}`);
if (fs.existsSync(candidatePath)) throw new Error(`refusing to overwrite ${path.basename(candidatePath)}`);

function cliVersion(command) {
  const result = spawnSync(command, ["--version"], {cwd: "/tmp", encoding: "utf8"});
  if (result.status !== 0) throw new Error(`${command} --version failed`);
  return result.stdout.trim();
}

function validateResponse(response) {
  const errors = [];
  const semantic = [];
  if (!response || typeof response !== "object" || Array.isArray(response)) return {errors: ["response is not an object"], semantic};
  if (JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(["revisions"])) errors.push("top-level keys are not exactly revisions");
  if (!Array.isArray(response.revisions)) return {errors: [...errors, "revisions is not an array"], semantic};
  if (response.revisions.length !== orderedIds.length) errors.push(`expected ${orderedIds.length} revisions, got ${response.revisions.length}`);
  for (let index = 0; index < response.revisions.length; index += 1) {
    const revision = response.revisions[index];
    const item = input.items[index];
    if (!revision || typeof revision !== "object" || Array.isArray(revision)) { errors.push(`revision ${index} is not an object`); continue; }
    if (JSON.stringify(Object.keys(revision).sort()) !== JSON.stringify(["claim", "observation", "revision_id", "verdict"])) errors.push(`revision ${index} has unexpected keys`);
    if (revision.revision_id !== orderedIds[index]) errors.push(`revision ${index} expected ${orderedIds[index]}, got ${revision.revision_id}`);
    if (!["OK", "FINDING", "UNCERTAIN"].includes(revision.verdict)) errors.push(`revision ${index} invalid verdict`);
    if (typeof revision.observation !== "string" || !revision.observation) errors.push(`revision ${index} invalid observation`);
    if (revision.verdict === "OK") {
      if (revision.claim !== null) errors.push(`revision ${index} OK claim must be null`);
      semantic.push({revision_id: revision.revision_id, valid_claim: true, reasons: []});
      continue;
    }
    const reasons = [];
    const claim = revision.claim;
    if (!claim || typeof claim !== "object" || Array.isArray(claim)) {
      errors.push(`revision ${index} non-OK claim must be an object`);
      semantic.push({revision_id: revision.revision_id, valid_claim: false, reasons: ["claim is not an object"]});
      continue;
    }
    if (JSON.stringify(Object.keys(claim).sort()) !== JSON.stringify(["claim_type", "correction", "evidence", "target_span"])) errors.push(`revision ${index} claim has unexpected keys`);
    if (typeof claim.target_span !== "string" || !claim.target_span) errors.push(`revision ${index} invalid target_span`);
    if (!["VALUE", "DIRECTION", "CONDITION", "SUBJECT", "TIMING", "SCOPE", "ACTION", "STATE", "ORDER", "OTHER"].includes(claim.claim_type)) errors.push(`revision ${index} invalid claim_type`);
    if (typeof claim.correction !== "string" || !claim.correction) errors.push(`revision ${index} invalid correction`);
    if (typeof claim.evidence !== "string" || !claim.evidence) errors.push(`revision ${index} invalid evidence`);
    if (typeof claim.target_span === "string" && !item?.target.includes(claim.target_span)) reasons.push("target_span is not an exact target substring");
    const visibleEvidence = [item?.source, item?.source_context].filter(value => typeof value === "string");
    if (typeof claim.evidence === "string" && !visibleEvidence.some(value => value.includes(claim.evidence))) reasons.push("evidence is not an exact source/source_context substring");
    semantic.push({revision_id: revision.revision_id, valid_claim: reasons.length === 0, reasons});
  }
  return {errors, semantic};
}

const schemaObject = readJson(files.schema);
let command;
let args;
let lastPath = null;
let adaptedSchemaPath = null;
let responseFormatSchemaSha256 = sha256File(files.schema);
let expectedVersion;
if (route.kind === "codex") {
  expectedVersion = "codex-cli 0.150.1";
  if (cliVersion("codex") !== expectedVersion) throw new Error("unexpected Codex CLI version");
  lastPath = path.join("/tmp", `runtime-context-${callStem}-attempt${attempt}-${process.pid}.json`);
  adaptedSchemaPath = path.join("/tmp", `runtime-context-schema-${callStem}-attempt${attempt}-${process.pid}.json`);
  const adaptedSchema = structuredClone(schemaObject);
  delete adaptedSchema.properties.revisions.items.allOf;
  const canonicalClaim = adaptedSchema.properties.revisions.items.properties.claim;
  const claimObject = canonicalClaim.oneOf.find(option => option.type === "object");
  adaptedSchema.properties.revisions.items.properties.claim = {...claimObject, type: ["object", "null"]};
  fs.writeFileSync(adaptedSchemaPath, `${JSON.stringify(adaptedSchema)}\n`);
  responseFormatSchemaSha256 = sha256File(adaptedSchemaPath);
  command = "codex";
  args = ["exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"", "--ephemeral", "--ignore-rules", "--skip-git-repo-check", "-o", lastPath, "-C", "/tmp", "-s", "read-only", "--output-schema", adaptedSchemaPath, prompt];
} else if (route.kind === "claude") {
  expectedVersion = "2.1.247 (Claude Code)";
  if (cliVersion("claude") !== expectedVersion) throw new Error("unexpected Claude Code version");
  const cliSchema = structuredClone(schemaObject);
  delete cliSchema.$schema;
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
const result = spawnSync(command, args, {cwd: "/tmp", encoding: "utf8", maxBuffer: 96 * 1024 * 1024, timeout: 30 * 60 * 1000, env: {...process.env, NO_COLOR: "1", PI_SKIP_VERSION_CHECK: "1"}});
const durationSeconds = (Date.now() - started) / 1000;
fs.writeFileSync(rawPath, result.stdout ?? "");
fs.writeFileSync(stderrPath, result.stderr ?? "");
if (adaptedSchemaPath && fs.existsSync(adaptedSchemaPath)) fs.unlinkSync(adaptedSchemaPath);
if (result.error || result.status !== 0) {
  const failure = {schema_version: "runtime-source-context-failure-v1", arm, run: runNumber, route: route.slug, attempt, request_sha256: requestSha256, duration_seconds: durationSeconds, status: result.status, signal: result.signal ?? null, error: result.error ? String(result.error) : null, raw_artifact: path.basename(rawPath), raw_sha256: sha256File(rawPath), stderr_artifact: path.basename(stderrPath), stderr_sha256: sha256File(stderrPath)};
  fs.writeFileSync(failurePath, `${JSON.stringify(failure, null, 2)}\n`);
  throw new Error(`${command} failed: status=${result.status}, signal=${result.signal}`);
}

let response = null;
let parseError = null;
let routeMetadata = {};
if (route.kind === "codex") {
  try { response = JSON.parse(fs.readFileSync(lastPath, "utf8")); } catch (error) { parseError = String(error); }
  finally { if (lastPath && fs.existsSync(lastPath)) fs.unlinkSync(lastPath); }
  routeMetadata = {harness: expectedVersion, requested_model: "gpt-5.6-sol", requested_effort: "high", session: "ephemeral"};
} else if (route.kind === "claude") {
  let events = [];
  try { events = result.stdout.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line)); } catch (error) { parseError = `event parse failed: ${error}`; }
  if (!parseError) {
    const initEvents = events.filter(event => event.type === "system" && event.subtype === "init");
    const assistantEvents = events.filter(event => event.type === "assistant" && event.message);
    const resultEvents = events.filter(event => event.type === "result");
    const terminal = resultEvents.length === 1 ? resultEvents[0] : null;
    const fallbackEvents = events.filter(event => event.type === "system" && /fallback/.test(event.subtype ?? ""));
    const fallbackBlocks = assistantEvents.flatMap(event => event.message.content ?? []).filter(block => block.type === "fallback");
    if (terminal?.structured_output && typeof terminal.structured_output === "object") response = terminal.structured_output;
    else { try { response = JSON.parse((terminal?.result ?? "").trim()); } catch (error) { parseError = String(error); } }
    routeMetadata = {harness: `Claude Code CLI ${expectedVersion.split(" ")[0]}`, requested_model: "claude-opus-5", requested_effort: "medium", requested_advisor: null, initialized_models: initEvents.map(event => event.model ?? null), actual_assistant_models: [...new Set(assistantEvents.map(event => event.message.model).filter(Boolean))], fallback_event_count: fallbackEvents.length, fallback_block_count: fallbackBlocks.length, result: terminal ? {is_error: terminal.is_error ?? null, subtype: terminal.subtype ?? null, stop_reason: terminal.stop_reason ?? null, terminal_reason: terminal.terminal_reason ?? null, usage: terminal.usage ?? null, model_usage: terminal.modelUsage ?? null, total_cost_usd: terminal.total_cost_usd ?? null, num_turns: terminal.num_turns ?? null} : null};
  }
} else if (route.kind === "pi") {
  let events = [];
  try { events = result.stdout.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line)); } catch (error) { parseError = `event parse failed: ${error}`; }
  if (!parseError) {
    const ends = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
    const message = ends.length === 1 ? ends[0].message : null;
    if (!message) parseError = `expected one assistant message_end, got ${ends.length}`;
    else {
      const body = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
      try { response = normalizePiResponse(parseModelJson(body)); } catch (error) { parseError = String(error); }
      routeMetadata = {harness: `Pi ${expectedVersion}`, requested_provider: "zai-standard-cn", requested_model: "glm-5.3-flash", requested_effort: "high", actual_provider: message.provider ?? null, actual_model: message.model ?? null, usage: message.usage ?? null, stop_reason: message.stopReason ?? null};
    }
  }
} else {
  let envelope = null;
  try { envelope = JSON.parse(result.stdout); response = envelope.structured_output ?? JSON.parse(envelope.response); } catch (error) { parseError = String(error); }
  routeMetadata = {harness: `Antigravity CLI ${expectedVersion}`, requested_model: "gemini-3.7-flash-high", requested_effort: "high", mode: "plan", sandbox: true, reported_model: envelope?.model ?? null, reported_agent: envelope?.agent ?? null, usage: envelope?.usage ?? null};
}

const validation = parseError ? {errors: [parseError], semantic: []} : validateResponse(response);
if (route.kind === "claude") {
  if (JSON.stringify(routeMetadata.initialized_models) !== JSON.stringify(["claude-opus-5"])) validation.errors.push("Claude initialized model mismatch");
  if (JSON.stringify(routeMetadata.actual_assistant_models) !== JSON.stringify(["claude-opus-5"])) validation.errors.push("Claude actual assistant model mismatch");
  if (routeMetadata.fallback_event_count !== 0 || routeMetadata.fallback_block_count !== 0) validation.errors.push("Claude fallback detected");
}
if (route.kind === "pi" && (routeMetadata.actual_provider !== "zai-standard-cn" || routeMetadata.actual_model !== "glm-5.3-flash")) validation.errors.push("Pi actual route mismatch");
const candidate = {schema_version: "runtime-source-context-candidate-v1", arm, run: runNumber, route: route.slug, attempt, request_sha256: requestSha256, input_sha256: sha256File(files.input), prompt_sha256: sha256File(files.prompt), schema_sha256: sha256File(files.schema), response_format_schema_sha256: responseFormatSchemaSha256, schema_adapter: route.kind === "codex" ? "drop unsupported item-level allOf and express claim nullability as type=[object,null]; prompt and local verdict/claim validator remain binding" : null, raw_artifact: path.basename(rawPath), raw_sha256: sha256File(rawPath), stderr_artifact: path.basename(stderrPath), stderr_sha256: sha256File(stderrPath), route_metadata: routeMetadata, duration_seconds: durationSeconds, exit_status: result.status, valid: validation.errors.length === 0, validation_errors: validation.errors, claim_validation: validation.semantic, verdict_counts: response?.revisions?.reduce((counts, revision) => { counts[revision.verdict] = (counts[revision.verdict] ?? 0) + 1; return counts; }, {}) ?? null, response};
fs.writeFileSync(candidatePath, `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: undefined, claim_validation: undefined}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 2;
