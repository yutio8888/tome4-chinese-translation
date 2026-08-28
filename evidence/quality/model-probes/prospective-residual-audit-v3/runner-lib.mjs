import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {validateResponse} from "./score-lib.mjs";

export const PUBLIC_FILES = ["PROMPT.md", "PUBLIC-HOLDOUT.json", "REVIEWER-SCHEMA.json", "CODEX-TRANSPORT-SCHEMA.json"];

export const PUBLIC_HASHES = {
  "PUBLIC-HOLDOUT.json": "912ac6a90161a2e2bd55b356196a6be9163640f830e816939f6793b8f5fe6c5d",
  "PROMPT.md": "056691a183a3200453211e1ddaacf79459fca762cf15d77dfb27bffa29cb6e1d",
  "REVIEWER-SCHEMA.json": "e1850c53d183c606781dd6505fcffbc5fd4ecd6fc1069ebc3cb59c137439de1b",
  "CODEX-TRANSPORT-SCHEMA.json": "ef1ccf4f12a38a59f3d709a70d5bff74777323b18f23e433ab6f2928ce3a418c"
};

export const ROUTES = {
  codex: {key: "codex", slug: "codex-gpt-5.6-sol-high", decision: "REFERENCE_ONLY_UNVERIFIED", evidenceTier: "REFERENCE_ONLY_UNVERIFIED", kind: "codex"},
  opus: {key: "opus", slug: "claude-opus-5-medium-no-advisor", decision: "GO", evidenceTier: "PRIMARY_VERIFIED", kind: "claude"},
  glm: {key: "glm", slug: "pi-zai-cn-glm-5.3-flash-high", decision: "GO", evidenceTier: "PRIMARY_VERIFIED", kind: "pi"},
  gemini: {key: "gemini", slug: "agy-gemini-3.7-flash-high", decision: "REFERENCE_ONLY_UNVERIFIED", evidenceTier: "REFERENCE_ONLY_UNVERIFIED", kind: "agy"}
};

export const EXPECTED_ROUTE_VERSIONS = {
  bwrap: "bubblewrap 0.11.1",
  codex: "codex-cli 0.150.1",
  claude: "2.1.247 (Claude Code)",
  pi: "0.84.3",
  agy: "1.1.22"
};

export const EXPECTED_MODEL_AVAILABILITY = {
  codex_gpt_5_6_sol: true,
  pi_zai_cn_glm_5_3_flash: true,
  agy_gemini_3_7_flash_high: true
};

export function assert(condition, message) {
  if (!condition) throw new Error(message);
}

export function sha256Bytes(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

export function sha256File(file) {
  return sha256Bytes(fs.readFileSync(file));
}

export function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

export function readCandidateArtifact(file) {
  let candidateSha256 = null;
  try { candidateSha256 = sha256File(file); }
  catch (error) { return {candidate: null, candidate_sha256: null, error: `candidate read/hash failure: ${error.message}`}; }
  try { return {candidate: readJson(file), candidate_sha256: candidateSha256, error: null}; }
  catch (error) { return {candidate: null, candidate_sha256: candidateSha256, error: `candidate parse failure: ${error.message}`}; }
}

export function writeNewFile(file, bytes) {
  const descriptor = fs.openSync(file, "wx", 0o600);
  try {
    fs.writeFileSync(descriptor, bytes);
  } finally {
    fs.closeSync(descriptor);
  }
}

export function routeFor(key) {
  const route = ROUTES[key];
  assert(route, `unknown route ${key ?? "<missing>"}`);
  return route;
}

export function assertRouteRunnable(key) {
  const route = routeFor(key);
  assert(["GO", "REFERENCE_ONLY_UNVERIFIED"].includes(route.decision), `${route.slug}: invocation is prohibited`);
  return route;
}

export function parseAttempt(value) {
  assert(/^\d+$/.test(value ?? ""), "--attempt requires a positive integer");
  const attempt = Number(value);
  assert(Number.isSafeInteger(attempt) && attempt > 0, "--attempt requires a positive integer");
  return attempt;
}

export function attemptDirectory(root, route, attempt) {
  return path.join(root, "attempts", route.slug, `attempt-${String(attempt).padStart(3, "0")}`);
}

export function reserveAttemptDirectory(root, route, attempt) {
  const routeRoot = path.join(root, "attempts", route.slug);
  fs.mkdirSync(routeRoot, {recursive: true});
  const directory = attemptDirectory(root, route, attempt);
  fs.mkdirSync(directory, {recursive: false, mode: 0o700});
  return directory;
}

export function validatePublicArtifacts(root) {
  const errors = [];
  for (const [name, expected] of Object.entries(PUBLIC_HASHES)) {
    const file = path.join(root, name);
    if (!fs.existsSync(file)) errors.push(`${name}: missing`);
    else if (sha256File(file) !== expected) errors.push(`${name}: frozen hash mismatch`);
  }
  if (errors.length) return errors;
  const holdout = readJson(path.join(root, "PUBLIC-HOLDOUT.json"));
  if (holdout.schema_version !== "prospective-residual-public-holdout-v3") errors.push("holdout schema identity mismatch");
  if (holdout.item_count !== 40 || holdout.items?.length !== 40) errors.push("holdout must contain 40 items");
  const orderedIds = holdout.items?.map(item => item.revision_id) ?? [];
  if (JSON.stringify(orderedIds) !== JSON.stringify(Array.from({length: 40}, (_, index) => `R${String(index + 1).padStart(3, "0")}`))) errors.push("holdout order/IDs mismatch");
  for (const [index, item] of (holdout.items ?? []).entries()) {
    if (JSON.stringify(Object.keys(item).sort()) !== JSON.stringify(["revision_id", "source", "target"])) errors.push(`holdout item ${index} has non-public fields`);
    if (typeof item.source !== "string" || typeof item.target !== "string") errors.push(`holdout item ${index} source/target type mismatch`);
  }
  const canonicalSchema = readJson(path.join(root, "REVIEWER-SCHEMA.json"));
  const expectedCodexSchema = structuredClone(canonicalSchema);
  delete expectedCodexSchema.properties?.revisions?.items?.allOf;
  const codexSchema = readJson(path.join(root, "CODEX-TRANSPORT-SCHEMA.json"));
  if (JSON.stringify(codexSchema) !== JSON.stringify(expectedCodexSchema)) errors.push("Codex transport schema is not the frozen mechanical allOf removal");
  return errors;
}

export function validateReviewContract(root) {
  const errors = [];
  let contract;
  try { contract = readJson(path.join(root, "REVIEW-CONTRACT.json")); }
  catch (error) { return {contract: null, errors: [`REVIEW-CONTRACT.json: ${error.message}`]}; }
  if (contract.schema_version !== "prospective-residual-review-contract-v3" || contract.status !== "FROZEN_PRE_INFERENCE") errors.push("review contract identity/status mismatch");
  for (const binding of [
    ...Object.values(contract.public_request ?? {}).filter(value => value && typeof value === "object" && value.logical_path),
    ...Object.values(contract.sealed_inputs ?? {}),
    ...Object.values(contract.scoring ?? {}).filter(value => value && typeof value === "object" && value.logical_path),
    ...Object.values(contract.harness ?? {}).filter(value => value && typeof value === "object" && value.logical_path)
  ]) {
    const file = path.join(root, binding.logical_path);
    if (!fs.existsSync(file)) errors.push(`${binding.logical_path}: contract-bound file missing`);
    else if (sha256File(file) !== binding.sha256) errors.push(`${binding.logical_path}: contract-bound hash mismatch`);
  }
  const decisions = new Map((contract.routes ?? []).map(route => [route.key, route.transport_decision]));
  for (const route of Object.values(ROUTES)) if (decisions.get(route.key) !== route.decision) errors.push(`${route.key}: route decision mismatch`);
  return {contract, errors};
}

export function validatePreflightRecord({preflight, contractSha256, packageGitCommit}) {
  const errors = [];
  if (preflight?.status !== "GO") errors.push("PREFLIGHT status is not GO");
  if (preflight?.route_check_performed !== true) errors.push("PREFLIGHT route check was not performed");
  if (preflight?.review_contract_sha256 !== contractSha256) errors.push("PREFLIGHT contract hash drift");
  if (preflight?.package_git_commit !== packageGitCommit) errors.push("PREFLIGHT package Git commit drift");
  if (JSON.stringify(preflight?.route_versions ?? null) !== JSON.stringify(EXPECTED_ROUTE_VERSIONS)) errors.push("PREFLIGHT route versions are incomplete or drifted");
  if (JSON.stringify(preflight?.model_availability ?? null) !== JSON.stringify(EXPECTED_MODEL_AVAILABILITY)) errors.push("PREFLIGHT model availability is incomplete or drifted");
  return errors;
}

export function validateRetryPreflightRecord({preflight, contractSha256, errataSha256, packageGitCommit}) {
  const errors = [];
  if (preflight?.schema_version !== "prospective-residual-retry-preflight-v3-1" || preflight?.status !== "GO") errors.push("retry PREFLIGHT status/identity is not GO");
  if (preflight?.route_check_performed !== true) errors.push("retry PREFLIGHT route check was not performed");
  if (preflight?.review_contract_sha256 !== contractSha256) errors.push("retry PREFLIGHT contract hash drift");
  if (preflight?.harness_errata_sha256 !== errataSha256) errors.push("retry PREFLIGHT errata hash drift");
  if (preflight?.package_git_commit !== packageGitCommit) errors.push("retry PREFLIGHT package Git commit drift");
  if (JSON.stringify(preflight?.route_versions ?? null) !== JSON.stringify(EXPECTED_ROUTE_VERSIONS)) errors.push("retry PREFLIGHT route versions are incomplete or drifted");
  if (JSON.stringify(preflight?.model_availability ?? null) !== JSON.stringify(EXPECTED_MODEL_AVAILABILITY)) errors.push("retry PREFLIGHT model availability is incomplete or drifted");
  if (JSON.stringify(preflight?.allowed_route_attempts ?? null) !== JSON.stringify({codex: 2, glm: 3})) errors.push("retry PREFLIGHT allowed attempts drift");
  return errors;
}

export function validateHarnessErrataArtifacts(root, errata) {
  const errors = [];
  if (errata?.schema_version !== "prospective-residual-harness-errata-v3-1" || errata?.status !== "FROZEN_BEFORE_RETRY_INFERENCE") errors.push("harness errata identity/status mismatch");
  const bindings = [errata?.initial_preflight, ...(errata?.preserved_artifacts ?? [])].filter(Boolean);
  for (const binding of bindings) {
    const file = path.join(root, binding.logical_path);
    if (!fs.existsSync(file)) {
      errors.push(`${binding.logical_path}: preserved artifact missing`);
      continue;
    }
    const stat = fs.lstatSync(file);
    if (!stat.isFile() || stat.isSymbolicLink()) errors.push(`${binding.logical_path}: preserved artifact is not an ordinary file`);
    else if (sha256File(file) !== binding.sha256) errors.push(`${binding.logical_path}: preserved artifact hash mismatch`);
  }
  return errors;
}

const FORBIDDEN_OUTBOUND = [
  {label: "local absolute path", pattern: /(?:\/(?:home|Users)\/|[A-Za-z]:\\Users\\)/u},
  {label: "sealed artifact name", pattern: /(?:SEALED-(?:REFERENCE|ATOM-MAP)|SOURCE-AUDIT|REFERENCE-ESTIMATES|ESTIMATOR-CONTRACT)/iu},
  {label: "sealed/adjudication field", pattern: /(?:audit_id|design_weight|inclusion_probability|provenance_(?:stratum|class)|adjudication|defect_id)/iu},
  {label: "sealed verdict", pattern: /(?:\bCONFIRMED\b|\bREFUTED\b|\bINDETERMINATE\b|\bUNREACHABLE\b)/u}
];

export function scanOutboundBuffers(buffers) {
  const errors = [];
  for (const item of buffers) {
    const text = Buffer.isBuffer(item.bytes) ? item.bytes.toString("utf8") : String(item.bytes);
    for (const forbidden of FORBIDDEN_OUTBOUND) {
      if (forbidden.pattern.test(text)) errors.push(`${item.label}: ${forbidden.label}`);
    }
  }
  return errors;
}

export function requestBytes(root) {
  const prompt = fs.readFileSync(path.join(root, "PROMPT.md"), "utf8");
  const holdout = readJson(path.join(root, "PUBLIC-HOLDOUT.json"));
  return Buffer.from(`${prompt}\n输入 JSON：\n${JSON.stringify(holdout)}`, "utf8");
}

export function createPublicBundle(root, parent = os.tmpdir()) {
  const directory = fs.mkdtempSync(path.join(parent, "residual-audit-v3-"));
  for (const name of PUBLIC_FILES) fs.copyFileSync(path.join(root, name), path.join(directory, name), fs.constants.COPYFILE_EXCL);
  assertExactBundle(directory);
  return directory;
}

export function assertExactBundle(directory) {
  const names = fs.readdirSync(directory).sort();
  assert(JSON.stringify(names) === JSON.stringify([...PUBLIC_FILES].sort()), `bundle entries mismatch: ${names.join(", ")}`);
  for (const name of names) {
    const stat = fs.lstatSync(path.join(directory, name));
    assert(stat.isFile() && !stat.isSymbolicLink(), `${name}: bundle entry is not an ordinary file`);
    assert(sha256File(path.join(directory, name)) === PUBLIC_HASHES[name], `${name}: bundle hash mismatch`);
  }
  return true;
}

const COMMON_ENV = ["PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "LC_CTYPE", "TZ", "TERM", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "NO_PROXY", "XDG_CONFIG_HOME", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS"];
const ROUTE_ENV = {
  codex: ["CODEX_HOME"],
  claude: ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_OAUTH_TOKEN", "CLAUDE_CONFIG_DIR"],
  pi: ["ZAI_CODING_CN_API_KEY", "ZAI_API_KEY", "PI_CODING_AGENT_DIR", "PI_PACKAGE_DIR"],
  agy: []
};

export function minimalEnvironment(kind, tmpdir, source = process.env) {
  const output = {};
  for (const name of [...COMMON_ENV, ...(ROUTE_ENV[kind] ?? [])]) if (typeof source[name] === "string") output[name] = source[name];
  output.TMPDIR = tmpdir;
  output.NO_COLOR = "1";
  if (kind === "pi") {
    output.PI_SKIP_VERSION_CHECK = "1";
    output.PI_TELEMETRY = "0";
  }
  return output;
}

export function createRouteRuntime(route, parent = os.tmpdir()) {
  assert(["codex", "pi"].includes(route.kind), `${route.slug}: no writable runtime is defined`);
  const directory = fs.mkdtempSync(path.join(parent, "residual-route-runtime-v3-"));
  fs.chmodSync(directory, 0o700);
  fs.mkdirSync(path.join(directory, "xdg"), {mode: 0o700});
  if (route.kind === "codex") {
    const codex = path.join(directory, "codex");
    fs.mkdirSync(codex, {mode: 0o700});
    const source = path.join(os.homedir(), ".codex", "auth.json");
    const stat = fs.lstatSync(source);
    assert(stat.isFile() && !stat.isSymbolicLink(), "Codex auth source is not an ordinary file");
    const destination = path.join(codex, "auth.json");
    fs.copyFileSync(source, destination, fs.constants.COPYFILE_EXCL);
    fs.chmodSync(destination, 0o600);
  } else {
    const pi = path.join(directory, "pi");
    fs.mkdirSync(pi, {mode: 0o700});
    const sourceAuth = readJson(path.join(os.homedir(), ".pi", "agent", "auth.json"));
    const sourceModels = readJson(path.join(os.homedir(), ".pi", "agent", "models.json"));
    assert(sourceAuth["zai-standard-cn"]?.type === "api_key", "Pi Z.ai CN credential is unavailable");
    const provider = structuredClone(sourceModels.providers?.["zai-standard-cn"]);
    assert(provider && Array.isArray(provider.models) && provider.models.some(model => model.id === "glm-5.3-flash"), "Pi GLM route definition is unavailable");
    delete provider.apiKey;
    writeNewFile(path.join(pi, "auth.json"), `${JSON.stringify({"zai-standard-cn": sourceAuth["zai-standard-cn"]})}\n`);
    writeNewFile(path.join(pi, "models.json"), `${JSON.stringify({providers: {"zai-standard-cn": provider}})}\n`);
  }
  return directory;
}

export function removeRouteRuntime(directory) {
  assert(path.basename(directory).startsWith("residual-route-runtime-v3-"), "refusing to remove an unrecognized runtime directory");
  const stat = fs.lstatSync(directory);
  assert(stat.isDirectory() && !stat.isSymbolicLink(), "refusing to remove a non-directory runtime");
  fs.rmSync(directory, {recursive: true, force: false});
}

export function runtimeEnvironment(kind, source = process.env) {
  const output = minimalEnvironment(kind, "/tmp", source);
  delete output.DBUS_SESSION_BUS_ADDRESS;
  output.XDG_RUNTIME_DIR = "/tmp/route-runtime/xdg";
  if (kind === "codex") output.CODEX_HOME = "/tmp/route-runtime/codex";
  if (kind === "pi") output.PI_CODING_AGENT_DIR = "/tmp/route-runtime/pi";
  return output;
}

export function invocationPlan(route, bundleDirectory, request, sandboxOptions = {}) {
  const schemaText = fs.readFileSync(path.join(bundleDirectory, "REVIEWER-SCHEMA.json"), "utf8");
  const codexSchemaText = fs.readFileSync(path.join(bundleDirectory, "CODEX-TRANSPORT-SCHEMA.json"), "utf8");
  const scanErrors = scanOutboundBuffers([
    {label: "user request", bytes: request},
    {label: "response schema", bytes: schemaText},
    {label: "Codex transport schema", bytes: codexSchemaText}
  ]);
  assert(scanErrors.length === 0, `outbound sanitization failed: ${scanErrors.join("; ")}`);
  if (route.kind === "codex") {
    const disabledFeatures = ["shell_tool", "unified_exec", "apps", "browser_use", "browser_use_external", "browser_use_full_cdp_access", "computer_use", "multi_agent", "multi_agent_v2", "plugins", "plugin_sharing", "remote_plugin", "skill_search", "view_image", "image_generation", "hooks", "goals", "tool_suggest", "tool_call_mcp_elicitation", "workspace_dependencies"];
    const featureArgs = disabledFeatures.flatMap(feature => ["--disable", feature]);
    return wrapInOsSandbox({
      ...sandboxOptions,
      bundleDirectory,
      command: "codex",
      args: [...featureArgs, "-a", "never", "exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "-C", "/mnt", "-s", "read-only", "--output-schema", "CODEX-TRANSPORT-SCHEMA.json", "--json", request.toString("utf8")],
      displayArgs: [...featureArgs, "-a", "never", "exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "-C", "/mnt", "-s", "read-only", "--output-schema", "CODEX-TRANSPORT-SCHEMA.json", "--json", "[REQUEST_BYTES]"]
    });
  }
  if (route.kind === "claude") {
    const cliSchema = JSON.parse(schemaText);
    delete cliSchema.$schema;
    return wrapInOsSandbox({
      ...sandboxOptions,
      bundleDirectory,
      command: "claude",
      args: ["--print", "--model", "claude-opus-5", "--effort", "medium", "--output-format", "stream-json", "--verbose", "--safe-mode", "--tools", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--no-session-persistence", "--disable-slash-commands", "--prompt-suggestions", "false", "--permission-mode", "plan", "--json-schema", JSON.stringify(cliSchema), "--", request.toString("utf8")],
      displayArgs: ["--print", "--model", "claude-opus-5", "--effort", "medium", "--output-format", "stream-json", "--verbose", "--safe-mode", "--tools", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--no-session-persistence", "--disable-slash-commands", "--prompt-suggestions", "false", "--permission-mode", "plan", "--json-schema", "[SCHEMA_BYTES_FROM_./REVIEWER-SCHEMA.json]", "--", "[REQUEST_BYTES]"]
    });
  }
  if (route.kind === "pi") {
    return wrapInOsSandbox({
      ...sandboxOptions,
      bundleDirectory,
      command: "pi",
      args: ["--provider", "zai-standard-cn", "--model", "glm-5.3-flash", "--thinking", "high", "--no-tools", "--no-session", "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-themes", "--no-context-files", "--no-approve", "--mode", "json", "--print", "--", request.toString("utf8")],
      displayArgs: ["--provider", "zai-standard-cn", "--model", "glm-5.3-flash", "--thinking", "high", "--no-tools", "--no-session", "--no-extensions", "--no-skills", "--no-prompt-templates", "--no-themes", "--no-context-files", "--no-approve", "--mode", "json", "--print", "--", "[REQUEST_BYTES]"]
    });
  }
  assert(route.kind === "agy", `unsupported runnable route kind ${route.kind}`);
  return wrapInOsSandbox({
    ...sandboxOptions,
    bundleDirectory,
    command: "agy",
    args: ["-p", request.toString("utf8"), "--model", "gemini-3.7-flash-high", "--effort", "high", "--disable-slash-commands", "--output-format", "json", "--print-timeout", "15m", "--mode", "plan", "--sandbox", "--json-schema", "REVIEWER-SCHEMA.json"],
    displayArgs: ["-p", "[REQUEST_BYTES]", "--model", "gemini-3.7-flash-high", "--effort", "high", "--disable-slash-commands", "--output-format", "json", "--print-timeout", "15m", "--mode", "plan", "--sandbox", "--json-schema", "REVIEWER-SCHEMA.json"]
  });
}

export function wrapInOsSandbox({bundleDirectory, command, args, displayArgs = args, runtimeDirectory = null, maskUserHome = false}) {
  if (runtimeDirectory !== null) {
    const stat = fs.lstatSync(runtimeDirectory);
    assert(stat.isDirectory() && !stat.isSymbolicLink(), "runtime bind source is not an ordinary directory");
  }
  const privateMounts = maskUserHome
    ? ["--tmpfs", os.homedir()]
    : ["--tmpfs", path.join(os.homedir(), "research")];
  const runtimeMount = runtimeDirectory === null ? [] : ["--dir", "/tmp/route-runtime", "--bind", runtimeDirectory, "/tmp/route-runtime"];
  return {
    command: "bwrap",
    args: [
      "--die-with-parent",
      "--new-session",
      "--cap-drop", "ALL",
      "--ro-bind", "/", "/",
      "--dev", "/dev",
      "--proc", "/proc",
      "--ro-bind", bundleDirectory, "/mnt",
      "--tmpfs", "/tmp",
      ...privateMounts,
      ...runtimeMount,
      "--chdir", "/mnt",
      "--",
      command,
      ...args
    ],
    display_args: [
      maskUserHome
        ? "[OS_SANDBOX: host filesystem read-only; user home hidden; route runtime private+writable; public bundle read-only at /mnt; cwd /mnt]"
        : "[OS_SANDBOX: host filesystem read-only; research root hidden; public bundle read-only at /mnt; cwd /mnt]",
      command,
      ...displayArgs
    ]
  };
}

function parseJsonLines(raw) {
  const lines = raw.split(/\r?\n/u).filter(line => line.trim());
  return lines.map((line, index) => {
    try { return JSON.parse(line); }
    catch (error) { throw new Error(`line ${index + 1}: invalid JSON event: ${error.message}`); }
  });
}

function unwrapJsonText(text) {
  const trimmed = text.trim();
  const fenced = trimmed.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/iu);
  return JSON.parse(fenced ? fenced[1] : trimmed);
}

function hasToolSignal(value) {
  if (!value || typeof value !== "object") return false;
  if (["tool_call", "tool_use", "tool_result", "tool_execution_start", "tool_execution_end"].includes(value.type)) return true;
  if (typeof value.type === "string" && /tool_(?:call|use|result|execution)/u.test(value.type)) return true;
  return Object.values(value).some(child => Array.isArray(child) ? child.some(hasToolSignal) : hasToolSignal(child));
}

function hasForbiddenClaudeToolSignal(value, allowedStructuredOutputIds = new Set()) {
  if (!value || typeof value !== "object") return false;
  if (value.type === "tool_use" && value.name === "StructuredOutput") return false;
  if (value.type === "tool_result" && allowedStructuredOutputIds.has(value.tool_use_id)) {
    return Object.entries(value).some(([key, child]) => !["type", "tool_use_id"].includes(key) && (Array.isArray(child)
      ? child.some(item => hasForbiddenClaudeToolSignal(item, allowedStructuredOutputIds))
      : hasForbiddenClaudeToolSignal(child, allowedStructuredOutputIds)));
  }
  if (["tool_call", "tool_use", "tool_result", "tool_execution_start", "tool_execution_end"].includes(value.type)) return true;
  if (typeof value.type === "string" && /tool_(?:call|use|result|execution)/u.test(value.type)) return true;
  return Object.values(value).some(child => Array.isArray(child)
    ? child.some(item => hasForbiddenClaudeToolSignal(item, allowedStructuredOutputIds))
    : hasForbiddenClaudeToolSignal(child, allowedStructuredOutputIds));
}

const CODEX_ALLOWED_TOP_LEVEL_EVENT_TYPES = new Set([
  "thread.started",
  "turn.started",
  "item.started",
  "item.updated",
  "item.completed",
  "turn.completed",
  "turn.failed",
  "error"
]);

function codexTopLevelExplicitSignal(event) {
  if (!CODEX_ALLOWED_TOP_LEVEL_EVENT_TYPES.has(event.type)) return `type=${event.type ?? "<missing>"}`;
  const signalPattern = /(?:^|[_.-])(?:tool|command|shell|file|read|write|edit|web|browser|mcp|subagent|computer)(?:[_.-]|$)/iu;
  for (const field of ["name", "tool", "tool_name", "kind", "subtype"]) {
    if (typeof event[field] === "string" && signalPattern.test(event[field])) return `${field}=${event[field]}`;
  }
  for (const field of ["command", "path", "url", "query", "server", "web_search", "mcp", "subagent", "computer"]) {
    if (Object.hasOwn(event, field) && event[field] != null && event[field] !== false) return `${field}=present`;
  }
  return null;
}

export function parseCodexRaw(raw) {
  const errors = [];
  let events = [];
  try { events = parseJsonLines(raw); }
  catch (error) { return {response: null, metadata: {}, errors: [error.message]}; }
  const threadStarts = events.filter(event => event.type === "thread.started");
  const turnStarts = events.filter(event => event.type === "turn.started");
  const terminals = events.filter(event => event.type === "turn.completed");
  if (threadStarts.length !== 1) errors.push(`expected one Codex thread.started, got ${threadStarts.length}`);
  if (turnStarts.length !== 1) errors.push(`expected one Codex turn.started, got ${turnStarts.length}`);
  if (terminals.length !== 1) errors.push(`expected one Codex turn.completed, got ${terminals.length}`);
  const allItems = events.map(event => event.item).filter(Boolean);
  const completedItems = events.filter(event => event.type === "item.completed").map(event => event.item).filter(Boolean);
  const agentMessages = completedItems.filter(item => item.type === "agent_message" && typeof item.text === "string");
  if (agentMessages.length !== 1) errors.push(`expected one completed Codex agent_message, got ${agentMessages.length}`);
  const failed = events.filter(event => event.type === "turn.failed" || event.type === "error");
  if (failed.length) errors.push("Codex turn failure event detected");
  const topLevelSignals = events.map(codexTopLevelExplicitSignal).filter(Boolean);
  if (topLevelSignals.length) errors.push(`Codex explicit top-level tool signal detected: ${[...new Set(topLevelSignals)].join(",")}`);
  const allowedItemTypes = new Set(["reasoning", "agent_message"]);
  const disallowedItemTypes = [...new Set(allItems.map(item => item.type).filter(type => !allowedItemTypes.has(type)))];
  if (disallowedItemTypes.length) errors.push(`Codex non-review item use detected: ${disallowedItemTypes.join(",")}`);
  const reportedModels = [...new Set(events.flatMap(event => [event.model, event.item?.model]).filter(Boolean))];
  if (reportedModels.some(model => model !== "gpt-5.6-sol")) errors.push(`Codex reported model mismatch: ${reportedModels.join(",")}`);
  let response = null;
  if (agentMessages.length) {
    try { response = unwrapJsonText(agentMessages.at(-1).text); }
    catch (error) { errors.push(`Codex agent message parse failed: ${error.message}`); }
  }
  const terminal = terminals[0] ?? null;
  if (terminal && (!terminal.usage || typeof terminal.usage !== "object")) errors.push("Codex turn usage missing");
  return {
    response,
    metadata: {
      requested_model: "gpt-5.6-sol",
      requested_effort: "high",
      runtime_identity_verified: false,
      isolation_class: "REFERENCE_ONLY_UNVERIFIED",
      reported_models: reportedModels,
      tool_telemetry_complete: false,
      observed_tool_signal: disallowedItemTypes.length > 0 || topLevelSignals.length > 0,
      completed_item_types: [...new Set(completedItems.map(item => item.type))],
      usage: terminal?.usage ?? null
    },
    errors
  };
}

export function parseClaudeRaw(raw) {
  const errors = [];
  let events = [];
  try { events = parseJsonLines(raw); }
  catch (error) { return {response: null, metadata: {}, errors: [error.message]}; }
  const init = events.filter(event => event.type === "system" && event.subtype === "init");
  const assistant = events.filter(event => event.type === "assistant" && event.message);
  const terminals = events.filter(event => event.type === "result");
  if (init.length !== 1) errors.push(`expected one Claude init event, got ${init.length}`);
  if (terminals.length !== 1) errors.push(`expected one Claude result event, got ${terminals.length}`);
  const first = init[0];
  if (first) {
    if (JSON.stringify(first.tools) !== JSON.stringify(["StructuredOutput"])) errors.push(`Claude exposed tools mismatch: ${JSON.stringify(first.tools)}`);
    if (!Array.isArray(first.mcp_servers) || first.mcp_servers.length !== 0) errors.push("Claude MCP servers were exposed");
    if (first.model !== "claude-opus-5") errors.push(`Claude initialized model mismatch: ${first.model}`);
    if (first.permissionMode !== "plan") errors.push(`Claude permission mode mismatch: ${first.permissionMode}`);
    if (!Array.isArray(first.slash_commands) || first.slash_commands.length !== 0) errors.push("Claude slash commands were exposed");
  }
  const assistantModels = [...new Set(assistant.map(event => event.message.model).filter(Boolean))];
  if (JSON.stringify(assistantModels) !== JSON.stringify(["claude-opus-5"])) errors.push(`Claude assistant model mismatch: ${assistantModels.join(",")}`);
  const blocks = assistant.flatMap(event => event.message.content ?? []);
  const toolBlocks = blocks.filter(block => block.type === "tool_use");
  const structuredOutputIds = new Set(toolBlocks.filter(block => block.name === "StructuredOutput").map(block => block.id).filter(Boolean));
  const toolResultBlocks = events.flatMap(event => event.message?.content ?? []).filter(block => block.type === "tool_result");
  if (toolBlocks.length !== 1 || toolBlocks[0]?.name !== "StructuredOutput") errors.push("Claude must invoke exactly one StructuredOutput tool and no other tool");
  if (toolResultBlocks.length !== 1 || !structuredOutputIds.has(toolResultBlocks[0]?.tool_use_id)) errors.push("Claude must return exactly one matching StructuredOutput result");
  if (events.some(event => hasForbiddenClaudeToolSignal(event, structuredOutputIds))) errors.push("Claude non-StructuredOutput tool signal detected");
  if (events.some(event => event.parent_tool_use_id != null)) errors.push("Claude subagent/parent tool-use event detected");
  if (events.some(event => /advisor/iu.test(`${event.type ?? ""} ${event.subtype ?? ""}`)) || blocks.some(block => /advisor/iu.test(`${block.type ?? ""} ${block.name ?? ""}`))) errors.push("Claude advisor signal detected");
  if (events.some(event => event.type === "system" && /fallback/iu.test(event.subtype ?? "")) || blocks.some(block => block.type === "fallback")) errors.push("Claude fallback detected");
  const terminal = terminals[0];
  if (terminal && (terminal.is_error === true || terminal.subtype !== "success")) errors.push("Claude terminal result was not successful");
  const subagents = terminal?.subagent_stats;
  if (subagents && (subagents.spawned !== 0 || subagents.spawned_by_subagents !== 0)) errors.push("Claude subagent spawn detected");
  const modelUsage = terminal?.modelUsage ?? terminal?.model_usage ?? {};
  const usedModels = Object.keys(modelUsage);
  if (usedModels.some(model => model !== "claude-opus-5")) errors.push(`Claude non-Opus/advisor model usage detected: ${usedModels.join(",")}`);
  const serverUse = terminal?.usage?.server_tool_use ?? {};
  if (Object.values(serverUse).some(value => typeof value === "number" && value !== 0)) errors.push("Claude server tool use detected");
  let response = terminal?.structured_output ?? toolBlocks[0]?.input ?? null;
  if (!response && typeof terminal?.result === "string") {
    try { response = unwrapJsonText(terminal.result); }
    catch (error) { errors.push(`Claude terminal result parse failed: ${error.message}`); }
  }
  return {
    response,
    metadata: {
      initialized_model: first?.model ?? null,
      assistant_models: assistantModels,
      exposed_tools: first?.tools ?? null,
      mcp_server_count: first?.mcp_servers?.length ?? null,
      structured_output_calls: toolBlocks.length,
      fallback_detected: errors.includes("Claude fallback detected"),
      used_models: usedModels,
      result_subtype: terminal?.subtype ?? null,
      stop_reason: terminal?.stop_reason ?? null,
      usage: terminal?.usage ?? null
    },
    errors
  };
}

export function parsePiRaw(raw) {
  const errors = [];
  let events = [];
  try { events = parseJsonLines(raw); }
  catch (error) { return {response: null, metadata: {}, errors: [error.message]}; }
  if (events.some(hasToolSignal)) errors.push("Pi tool event or block detected");
  const ends = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
  if (ends.length !== 1) errors.push(`expected one Pi assistant message_end, got ${ends.length}`);
  const message = ends[0]?.message;
  if (message && (message.provider !== "zai-standard-cn" || message.model !== "glm-5.3-flash")) errors.push(`Pi actual route mismatch: ${message.provider ?? "null"}/${message.model ?? "null"}`);
  if (message && message.stopReason !== "stop") errors.push(`Pi stop reason mismatch: ${message.stopReason ?? "null"}`);
  let response = null;
  if (message) {
    const body = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
    try { response = unwrapJsonText(body); }
    catch (error) { errors.push(`Pi response parse failed: ${error.message}`); }
  }
  return {
    response,
    metadata: {
      actual_provider: message?.provider ?? null,
      actual_model: message?.model ?? null,
      stop_reason: message?.stopReason ?? null,
      usage: message?.usage ?? null,
      tool_signal_count: events.filter(hasToolSignal).length
    },
    errors
  };
}

export function parseAgyRaw(raw, expectedSchema) {
  const errors = [];
  let envelope = null;
  try { envelope = JSON.parse(raw); }
  catch (error) { return {response: null, metadata: {}, errors: [`agy envelope parse failed: ${error.message}`]}; }
  if (envelope.status !== "SUCCESS") errors.push(`agy status mismatch: ${envelope.status ?? "null"}`);
  if (!expectedSchema || JSON.stringify(envelope.json_schema ?? null) !== JSON.stringify(expectedSchema)) errors.push("agy returned schema mismatch");
  const reportedModel = envelope.model ?? null;
  if (reportedModel !== null && reportedModel !== "gemini-3.7-flash-high") errors.push(`agy reported model mismatch: ${reportedModel}`);
  const response = envelope.structured_output ?? null;
  if (!response || typeof response !== "object" || Array.isArray(response)) errors.push("agy structured_output is not an object");
  const hasToolCallsProperty = Object.hasOwn(envelope, "tool_calls");
  const explicitToolEvents = Array.isArray(envelope.tool_calls) ? envelope.tool_calls.length : null;
  if (hasToolCallsProperty && (!Array.isArray(envelope.tool_calls) || envelope.tool_calls.length > 0)) errors.push("agy explicit tool calls detected");
  for (const field of ["tool_events", "commands", "web_search", "mcp", "subagents"]) {
    if (!Object.hasOwn(envelope, field)) continue;
    const value = envelope[field];
    if (!(Array.isArray(value) && value.length === 0) && value != null && value !== false) errors.push(`agy explicit ${field} signal detected`);
  }
  if (envelope.fallback != null || envelope.fallback_model != null) errors.push("agy fallback signal detected");
  if (envelope.agent != null || (Array.isArray(envelope.subagents) && envelope.subagents.length > 0)) errors.push("agy agent/subagent signal detected");
  return {
    response,
    metadata: {
      requested_model: "gemini-3.7-flash-high",
      requested_effort: "high",
      runtime_identity_verified: false,
      isolation_class: "REFERENCE_ONLY_UNVERIFIED",
      reported_model: reportedModel,
      reported_agent: envelope.agent ?? null,
      tool_telemetry_complete: false,
      explicit_tool_call_count: explicitToolEvents,
      response_contains_internal_tool_action_text: typeof envelope.response === "string" && /"toolAction"|"toolSummary"/u.test(envelope.response),
      usage: envelope.usage ?? null,
      duration_seconds: envelope.duration_seconds ?? null
    },
    errors
  };
}

export function candidateFromRaw({route, raw, holdout, schema, call}) {
  const parsed = route.kind === "codex" ? parseCodexRaw(raw)
    : route.kind === "claude" ? parseClaudeRaw(raw)
      : route.kind === "pi" ? parsePiRaw(raw)
        : parseAgyRaw(raw, schema);
  const orderedIds = holdout.items.map(item => item.revision_id);
  const schemaErrors = parsed.response ? validateResponse(parsed.response, orderedIds) : ["response unavailable"];
  const errors = [...parsed.errors, ...schemaErrors];
  return {
    schema_version: "prospective-residual-candidate-v3",
    experiment: "prospective-residual-audit-v3",
    route: route.slug,
    evidence_tier: route.evidenceTier,
    attempt: call.attempt,
    request_sha256: call.request_sha256,
    input_sha256: PUBLIC_HASHES["PUBLIC-HOLDOUT.json"],
    prompt_sha256: PUBLIC_HASHES["PROMPT.md"],
    schema_sha256: PUBLIC_HASHES["REVIEWER-SCHEMA.json"],
    transport_schema_sha256: route.kind === "codex" ? PUBLIC_HASHES["CODEX-TRANSPORT-SCHEMA.json"] : PUBLIC_HASHES["REVIEWER-SCHEMA.json"],
    raw_stdout_sha256: call.raw_stdout_sha256,
    raw_stderr_sha256: call.raw_stderr_sha256,
    route_metadata: parsed.metadata,
    valid: errors.length === 0,
    validation_errors: errors,
    response: parsed.response
  };
}

export function validateResponseShape(response, orderedIds) {
  return validateResponse(response, orderedIds);
}
