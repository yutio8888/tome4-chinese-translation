#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const [routeKey, arm, runLabel, mode] = process.argv.slice(2);
const parseExisting = mode === "--parse-existing";
const routes = {
  codex: {slug: "codex-gpt-5.6-sol-high", kind: "codex", version: "codex-cli 0.150.1"},
  claude: {slug: "claude-opus-5-high-exploratory", kind: "claude", version: "2.1.250 (Claude Code)"},
  glm: {slug: "pi-zai-cn-glm-5.3-flash-high", kind: "pi", version: "0.84.3"},
  gemini: {slug: "agy-gemini-3.7-flash-high", kind: "agy", version: "1.1.22"}
};
if (!routes[routeKey] || !["A", "B"].includes(arm) || !["1", "2"].includes(runLabel) || ![undefined, "--parse-existing"].includes(mode)) throw new Error("usage: node run.mjs codex|claude|glm|gemini A|B 1|2 [--parse-existing]");
const route = routes[routeKey];
const files = {
  input: path.join(directory, `INPUT-${arm}.json`),
  prompt: path.join(directory, "PROMPT.md"),
  schema: path.join(directory, "REVIEWER-SCHEMA.json")
};
const expectedHashes = {
  A: "d8845716b86d2b0f7dca8ada1495f724e584e4c2adab97373b3a9dd975b5b4a2",
  B: "05893599fd1fad889d0cc36811565b2693933b09d069b9f59028143b7dd9a764",
  prompt: "c4ce6c84fa674f7b2efab21afbf3584c495578821d1ca1c5b4f599a0ca1e6d25",
  schema: "b47b250e6ffc7b6b4bebc4eb96493dbf011ec8ae747416debe9c1c709bd59de9",
  reference: "7383e82ce3506f50d8a2619261867f4bc919acccaae103841dd80f3acfdffc46"
};
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
if (sha256(fs.readFileSync(files.input)) !== expectedHashes[arm]) throw new Error("input frozen hash mismatch");
if (sha256(fs.readFileSync(files.prompt)) !== expectedHashes.prompt) throw new Error("prompt frozen hash mismatch");
if (sha256(fs.readFileSync(files.schema)) !== expectedHashes.schema) throw new Error("schema frozen hash mismatch");
if (sha256(fs.readFileSync(path.join(directory, "REFERENCE.json"))) !== expectedHashes.reference) throw new Error("reference frozen hash mismatch");

const stem = `${route.slug}-${arm}${runLabel}`;
const rawPath = path.join(directory, `RAW-${stem}.stdout.txt`);
const stderrPath = path.join(directory, `RAW-${stem}.stderr.txt`);
const acquisitionPath = path.join(directory, `ACQUISITION-${stem}.json`);
const codexLastPath = path.join(directory, `RAW-${stem}.last-message.json`);
const candidatePath = path.join(directory, `CANDIDATE-${stem}.json`);
if (!parseExisting && [rawPath, stderrPath, acquisitionPath, codexLastPath, candidatePath].some(file => fs.existsSync(file))) throw new Error(`refusing to overwrite ${stem} artifacts`);
if (parseExisting && [rawPath, stderrPath, acquisitionPath].some(file => !fs.existsSync(file))) throw new Error(`${stem}: existing acquisition artifacts incomplete`);
const input = JSON.parse(fs.readFileSync(files.input, "utf8"));
const orderedIds = input.items.map(item => item.item_id);
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
  if (JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(["items"])) errors.push("top-level keys are not exactly items");
  if (!Array.isArray(response.items)) return [...errors, "items is not an array"];
  if (response.items.length !== orderedIds.length) errors.push(`expected ${orderedIds.length} items, got ${response.items.length}`);
  for (let index = 0; index < response.items.length; index += 1) {
    const item = response.items[index];
    if (!item || typeof item !== "object" || Array.isArray(item)) { errors.push(`item ${index} is not an object`); continue; }
    if (JSON.stringify(Object.keys(item).sort()) !== JSON.stringify(["evidence", "item_id", "material_issue", "verdict"])) errors.push(`item ${index} has unexpected keys`);
    if (item.item_id !== orderedIds[index]) errors.push(`item ${index} expected ${orderedIds[index]}, got ${item.item_id}`);
    if (!["OK", "FINDING", "UNCERTAIN"].includes(item.verdict)) errors.push(`item ${index} invalid verdict`);
    if (typeof item.material_issue !== "string" || !item.material_issue) errors.push(`item ${index} invalid material_issue`);
    if (typeof item.evidence !== "string" || !item.evidence) errors.push(`item ${index} invalid evidence`);
  }
  return errors;
}

let command;
let args;
let lastPath = null;
if (!parseExisting && cliVersion(route.kind === "pi" ? "pi" : route.kind) !== route.version) throw new Error(`${route.slug}: unexpected CLI version`);
if (route.kind === "codex") {
  lastPath = path.join("/tmp", `source-context-${stem}-${process.pid}.json`);
  command = "codex";
  args = ["exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--json", "-o", lastPath, "-C", "/tmp", "-s", "read-only", "--output-schema", files.schema, prompt];
} else if (route.kind === "claude") {
  const cliSchema = structuredClone(schemaObject);
  delete cliSchema.$schema;
  command = "claude";
  args = ["--print", "--model", "claude-opus-5", "--effort", "high", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "project,local", "--disable-slash-commands", "--permission-mode", "plan", "--tools", "", "--json-schema", JSON.stringify(cliSchema), "--", prompt];
} else if (route.kind === "pi") {
  command = "pi";
  args = ["--provider", "zai-standard-cn", "--model", "glm-5.3-flash", "--thinking", "high", "--no-tools", "--no-session", "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-themes", "--no-context-files", "--no-approve", "--mode", "json", "--print", prompt];
} else {
  command = "agy";
  args = ["-p", prompt, "--model", "gemini-3.7-flash-high", "--effort", "high", "--disable-slash-commands", "--output-format", "json", "--print-timeout", "20m", "--mode", "plan", "--sandbox", "--json-schema", files.schema];
}

let run;
let durationSeconds;
let acquisition;
let priorCandidateSha256 = null;
if (parseExisting) {
  const rawBytes = fs.readFileSync(rawPath);
  const stderrBytes = fs.readFileSync(stderrPath);
  const acquisitionBytes = fs.readFileSync(acquisitionPath);
  acquisition = JSON.parse(acquisitionBytes.toString("utf8"));
  if (acquisition.route !== route.slug || acquisition.arm !== arm || acquisition.run !== Number(runLabel)) throw new Error(`${stem}: acquisition identity mismatch`);
  if (acquisition.raw_stdout.sha256 !== sha256(rawBytes) || acquisition.raw_stderr.sha256 !== sha256(stderrBytes)) throw new Error(`${stem}: acquisition raw hash mismatch`);
  if (route.kind === "codex") {
    const lastBytes = fs.readFileSync(codexLastPath);
    if (acquisition.codex_last_message?.sha256 !== sha256(lastBytes)) throw new Error(`${stem}: Codex last-message hash mismatch`);
  }
  if (fs.existsSync(candidatePath)) {
    const priorBytes = fs.readFileSync(candidatePath);
    const prior = JSON.parse(priorBytes.toString("utf8"));
    if (prior.valid) throw new Error(`${stem}: refusing to replace valid candidate`);
    priorCandidateSha256 = sha256(priorBytes);
  }
  run = {stdout: rawBytes.toString("utf8"), stderr: stderrBytes.toString("utf8"), status: acquisition.exit_status, signal: acquisition.signal};
  durationSeconds = acquisition.duration_seconds;
  if (run.status !== 0) throw new Error(`${stem}: cannot parse nonzero acquisition status ${run.status}`);
} else {
  const startedAtUtc = new Date().toISOString();
  const started = Date.now();
  run = spawnSync(command, args, {cwd: "/tmp", encoding: "utf8", maxBuffer: 96 * 1024 * 1024, timeout: 45 * 60 * 1000, env: {...process.env, NO_COLOR: "1", PI_SKIP_VERSION_CHECK: "1"}});
  durationSeconds = (Date.now() - started) / 1000;
  const rawBytes = Buffer.from(run.stdout ?? "", "utf8");
  const stderrBytes = Buffer.from(run.stderr ?? "", "utf8");
  fs.writeFileSync(rawPath, rawBytes);
  fs.writeFileSync(stderrPath, stderrBytes);
  let codexLastBinding = null;
  if (route.kind === "codex" && lastPath && fs.existsSync(lastPath)) {
    const lastBytes = fs.readFileSync(lastPath);
    fs.writeFileSync(codexLastPath, lastBytes);
    codexLastBinding = {sha256: sha256(lastBytes), size_bytes: lastBytes.length};
    fs.unlinkSync(lastPath);
  }
  acquisition = {
    schema_version: "source-context-exploratory-acquisition-v1",
    route: route.slug,
    arm,
    run: Number(runLabel),
    cli_version: route.version,
    started_at_utc: startedAtUtc,
    completed_at_utc: new Date().toISOString(),
    input_sha256: expectedHashes[arm],
    prompt_sha256: expectedHashes.prompt,
    schema_sha256: expectedHashes.schema,
    reference_sha256: expectedHashes.reference,
    exit_status: run.status,
    signal: run.signal ?? null,
    duration_seconds: durationSeconds,
    error: run.error ? String(run.error) : null,
    raw_stdout: {sha256: sha256(rawBytes), size_bytes: rawBytes.length},
    raw_stderr: {sha256: sha256(stderrBytes), size_bytes: stderrBytes.length},
    codex_last_message: codexLastBinding
  };
  fs.writeFileSync(acquisitionPath, `${JSON.stringify(acquisition, null, 2)}\n`);
  if (run.error) throw run.error;
  if (run.status !== 0) throw new Error(`${command} failed: status=${run.status}, signal=${run.signal}, stderr=${run.stderr}`);
}

let response = null;
let parseError = null;
let routeMetadata = {};
if (route.kind === "codex") {
  try { response = JSON.parse(fs.readFileSync(codexLastPath, "utf8")); } catch (error) { parseError = String(error); }
  routeMetadata = {harness: route.version, requested_model: "gpt-5.6-sol", requested_effort: "high", session: "ephemeral", identity_status: "REQUESTED_ROUTE_ONLY_CLI_ENVELOPE_UNVERIFIED", formal_eligible: false};
} else if (route.kind === "claude") {
  let events = [];
  try { events = run.stdout.split(/\r?\n/u).filter(Boolean).map(line => JSON.parse(line)); } catch (error) { parseError = `event parse failed: ${error}`; }
  if (!parseError) {
    const initEvents = events.filter(event => event.type === "system" && event.subtype === "init");
    const assistantEvents = events.filter(event => event.type === "assistant" && event.message);
    const resultEvents = events.filter(event => event.type === "result");
    const resultEvent = resultEvents.length === 1 ? resultEvents[0] : null;
    const fallbackEvents = events.filter(event => event.type === "system" && /fallback/u.test(event.subtype ?? ""));
    const fallbackBlocks = assistantEvents.flatMap(event => event.message.content ?? []).filter(block => block.type === "fallback");
    if (resultEvent?.structured_output && typeof resultEvent.structured_output === "object") response = resultEvent.structured_output;
    else { try { response = JSON.parse((resultEvent?.result ?? "").trim()); } catch (error) { parseError = String(error); } }
    routeMetadata = {
      harness: `Claude Code CLI ${route.version.split(" ")[0]}`,
      requested_model: "claude-opus-5",
      requested_effort: "high",
      qualification: "EXPLORATORY_FORMAL_PURITY_NO_GO",
      formal_eligible: false,
      initialized_models: initEvents.map(event => event.model ?? null),
      actual_assistant_models: [...new Set(assistantEvents.map(event => event.message.model).filter(Boolean))],
      fallback_event_count: fallbackEvents.length,
      fallback_block_count: fallbackBlocks.length,
      result: resultEvent ? {is_error: resultEvent.is_error ?? null, subtype: resultEvent.subtype ?? null, stop_reason: resultEvent.stop_reason ?? null, terminal_reason: resultEvent.terminal_reason ?? null, usage: resultEvent.usage ?? null, model_usage: resultEvent.modelUsage ?? null, total_cost_usd: resultEvent.total_cost_usd ?? null, num_turns: resultEvent.num_turns ?? null} : null
    };
  }
} else if (route.kind === "pi") {
  let events = [];
  try { events = run.stdout.split(/\r?\n/u).filter(Boolean).map(line => JSON.parse(line)); } catch (error) { parseError = `event parse failed: ${error}`; }
  if (!parseError) {
    const messageEnds = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
    const message = messageEnds.length === 1 ? messageEnds[0].message : null;
    if (!message) parseError = `expected one assistant message_end, got ${messageEnds.length}`;
    else {
      const text = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
      try { response = JSON.parse(text.trim()); } catch (error) { parseError = String(error); }
      routeMetadata = {harness: `Pi ${route.version}`, requested_provider: "zai-standard-cn", requested_model: "glm-5.3-flash", requested_effort: "high", actual_provider: message.provider ?? null, actual_model: message.model ?? null, usage: message.usage ?? null, stop_reason: message.stopReason ?? null, qualification: "EXPLORATORY_AFTER_FORMAL_TRUTH_SET_NO_GO", formal_eligible: false};
    }
  }
} else {
  let envelope = null;
  try { envelope = JSON.parse(run.stdout); response = envelope.structured_output ?? JSON.parse(envelope.response); } catch (error) { parseError = String(error); }
  routeMetadata = {harness: `Antigravity CLI ${route.version}`, requested_model: "gemini-3.7-flash-high", requested_effort: "high", mode: "plan", sandbox: true, reported_model: envelope?.model ?? null, reported_agent: envelope?.agent ?? null, usage: envelope?.usage ?? null, qualification: "EXPLORATORY_COMPARATOR", formal_eligible: false};
}

const validationErrors = parseError ? [parseError] : validateResponse(response);
const routeWarnings = [];
let identityStatus = routeMetadata.identity_status ?? "UNASSESSED";
let requestedRouteLabelEligible = false;
if (route.kind === "claude") {
  const initializedMatch = JSON.stringify(routeMetadata.initialized_models) === JSON.stringify(["claude-opus-5"]);
  const assistantMatch = JSON.stringify(routeMetadata.actual_assistant_models) === JSON.stringify(["claude-opus-5"]);
  const fallbackFree = routeMetadata.fallback_event_count === 0 && routeMetadata.fallback_block_count === 0;
  if (!initializedMatch) routeWarnings.push("Claude initialized model differs from requested singleton");
  if (!assistantMatch) routeWarnings.push("Claude assistant message model differs from requested singleton");
  if (!fallbackFree) routeWarnings.push("Claude fallback telemetry present");
  identityStatus = initializedMatch && assistantMatch && fallbackFree ? "ASSISTANT_STREAM_OPUS_VERIFIED_FORMAL_PURITY_STILL_NO_GO" : "MIXED_OR_FALLBACK_EXPLORATORY_ROUTE";
  requestedRouteLabelEligible = initializedMatch && assistantMatch && fallbackFree;
}
if (route.kind === "pi") {
  const match = routeMetadata.actual_provider === "zai-standard-cn" && routeMetadata.actual_model === "glm-5.3-flash";
  if (!match) validationErrors.push("Pi actual route mismatch");
  identityStatus = match ? "PROVIDER_AND_MODEL_VERIFIED" : "PROVIDER_OR_MODEL_MISMATCH";
  requestedRouteLabelEligible = match;
}
if (route.kind === "agy") {
  if (!routeMetadata.reported_model) {
    routeWarnings.push("Antigravity envelope does not report runtime model identity");
    identityStatus = "REQUESTED_ROUTE_ONLY_ENVELOPE_UNVERIFIED";
  } else if (routeMetadata.reported_model === "gemini-3.7-flash-high") {
    identityStatus = "ENVELOPE_MODEL_VERIFIED";
    requestedRouteLabelEligible = true;
  } else {
    routeWarnings.push(`Antigravity reported unexpected model ${routeMetadata.reported_model}`);
    identityStatus = "ENVELOPE_MODEL_MISMATCH";
  }
}
if (route.kind === "codex") {
  routeWarnings.push("Codex CLI fixes the requested model but its retained envelope does not independently attest runtime identity");
  identityStatus = "REQUESTED_ROUTE_ONLY_CLI_ENVELOPE_UNVERIFIED";
}
routeMetadata.identity_status = identityStatus;
const candidate = {
  schema_version: "source-context-exploratory-candidate-v1",
  route: route.slug,
  arm,
  run: Number(runLabel),
  input_sha256: expectedHashes[arm],
  prompt_sha256: expectedHashes.prompt,
  schema_sha256: expectedHashes.schema,
  reference_sha256: expectedHashes.reference,
  route_metadata: routeMetadata,
  acquisition: {file: path.basename(acquisitionPath), sha256: sha256(fs.readFileSync(acquisitionPath)), size_bytes: fs.statSync(acquisitionPath).size},
  reparsed_from_existing_raw: parseExisting,
  prior_candidate_sha256: priorCandidateSha256,
  duration_seconds: durationSeconds,
  exit_status: run.status,
  valid: validationErrors.length === 0,
  exploratory_score_eligible: validationErrors.length === 0,
  requested_route_label_eligible: requestedRouteLabelEligible,
  formal_eligible: false,
  validation_errors: validationErrors,
  route_warnings: routeWarnings,
  verdict_counts: response?.items?.reduce((counts, item) => { counts[item.verdict] = (counts[item.verdict] ?? 0) + 1; return counts; }, {}) ?? null,
  response
};
fs.writeFileSync(candidatePath, `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: undefined}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 2;
