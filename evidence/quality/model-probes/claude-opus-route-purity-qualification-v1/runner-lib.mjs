import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";

export const EXPERIMENT = "claude-opus-route-purity-qualification-v1";
export const ROUTE_SLUG = "claude-opus-5-medium-strict-purity";
export const EXPECTED_CLAUDE_VERSION = "2.1.247 (Claude Code)";
export const EXPECTED_CLAUDE_INIT_VERSION = "2.1.247";
export const EXPECTED_BWRAP_VERSION = "bubblewrap 0.11.1";
export const EXPECTED_MODEL = "claude-opus-5";
export const EXPECTED_PROVIDER = "firstParty";
export const SANDBOX_HOME = path.join(path.dirname(os.homedir()), "claude-purity-home");
export const SANDBOX_RUNTIME = "/run/claude-purity";
export const SANDBOX_CLAUDE_BINARY = "/opt/claude-purity/claude";
export const SANDBOX_AUTH_POLICY = "copy exactly one ordinary 0600 first-party OAuth credential file into a private 0700 ephemeral writable CLAUDE_CONFIG_DIR; mask the entire host HOME; delete the runtime after each no-model smoke or call";
export const REQUIRED_ENVIRONMENT = Object.freeze({
  CLAUDE_CODE_DISABLE_ADVISOR_TOOL: "1",
  CLAUDE_CODE_NO_MODEL_FALLBACK: "1",
  CLAUDE_CODE_DISABLE_REFUSAL_FALLBACK: "1",
  CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK: "1",
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1",
  CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION: "0"
});

export const FROZEN_FILES = Object.freeze([
  "PROMPT.md",
  "INPUT.json",
  "SCHEMA.json",
  "ROUTE-CONTRACT.json",
  "EXPERIMENT.json",
  "README.md",
  "runner-lib.mjs",
  "run.mjs",
  "parse.mjs",
  "preflight.mjs",
  "test-parser.mjs",
  "fixtures/PASS-OPUS-ONLY.jsonl",
  "fixtures/FAIL-NON-OPUS.jsonl"
]);

const NETWORK_ENVIRONMENT = [
  "LANG", "LC_ALL", "LC_CTYPE", "TZ", "TERM", "SSL_CERT_FILE", "SSL_CERT_DIR",
  "HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "NO_PROXY"
];
const SANDBOX_RUNTIME_PREFIX = "claude-opus-purity-runtime-v1-";
const PUBLIC_BUNDLE_PREFIX = "claude-opus-purity-v1-";
const AUTH_RELATIVE_PATH = path.join("claude", ".credentials.json");
const REQUIRED_PREFLIGHT_KEYS = Object.freeze([
  "schema_version", "status", "route_check_performed", "package_git_commit",
  "head_commit_at_preflight", "package_relative_path", "package_git_tree_oid",
  "package_git_blobs", "claude_version", "expected_claude_version",
  "claude_binary_sha256", "bwrap_version", "required_environment",
  "frozen_hash_manifest_sha256", "public_bundle_file_count", "synthetic_items",
  "real_experiment_samples", "executor_fixture_sha256", "fixture_test_status",
  "sandbox_smoke_status", "sandbox_host_home_hidden", "sandbox_runtime_private_writable",
  "sandbox_auth_policy", "sandbox_auth_method", "sandbox_api_provider", "errors"
]);

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

export function assertOrdinaryFile(file, label = path.basename(file)) {
  assert(fs.existsSync(file), `${label} missing`);
  const stat = fs.lstatSync(file);
  assert(stat.isFile() && !stat.isSymbolicLink(), `${label} is not an ordinary non-symlink file`);
  return stat;
}

export function writeNewFile(file, bytes) {
  const descriptor = fs.openSync(file, "wx", 0o600);
  try {
    fs.writeFileSync(descriptor, bytes);
  } finally {
    fs.closeSync(descriptor);
  }
}

export function parseAttempt(value) {
  assert(/^\d+$/u.test(value ?? ""), "--attempt requires a positive integer");
  const attempt = Number(value);
  assert(Number.isSafeInteger(attempt) && attempt > 0, "--attempt requires a positive integer");
  return attempt;
}

export function attemptDirectory(root, attempt) {
  return path.join(root, "attempts", ROUTE_SLUG, `attempt-${String(attempt).padStart(3, "0")}`);
}

export function reserveAttemptDirectory(root, attempt) {
  const routeRoot = path.join(root, "attempts", ROUTE_SLUG);
  fs.mkdirSync(routeRoot, {recursive: true});
  const directory = attemptDirectory(root, attempt);
  fs.mkdirSync(directory, {recursive: false, mode: 0o700});
  return directory;
}

export function minimalClaudeEnvironment(source = process.env) {
  const output = {};
  for (const name of NETWORK_ENVIRONMENT) {
    if (typeof source[name] === "string") output[name] = source[name];
  }
  Object.assign(output, REQUIRED_ENVIRONMENT);
  output.PATH = "/usr/bin:/bin";
  output.HOME = SANDBOX_HOME;
  output.USER = "yun";
  output.LOGNAME = "yun";
  output.SHELL = "/bin/sh";
  output.TMPDIR = "/tmp";
  output.CLAUDE_CONFIG_DIR = `${SANDBOX_RUNTIME}/claude`;
  output.XDG_CONFIG_HOME = `${SANDBOX_RUNTIME}/config`;
  output.XDG_CACHE_HOME = `${SANDBOX_RUNTIME}/cache`;
  output.XDG_DATA_HOME = `${SANDBOX_RUNTIME}/data`;
  output.XDG_STATE_HOME = `${SANDBOX_RUNTIME}/state`;
  output.XDG_RUNTIME_DIR = `${SANDBOX_RUNTIME}/runtime`;
  output.NO_COLOR = "1";
  return output;
}

export function validateEnvironment(environment) {
  const errors = [];
  for (const [name, expected] of Object.entries(REQUIRED_ENVIRONMENT)) {
    if (environment[name] !== expected) errors.push(`${name}: required value is not set`);
  }
  for (const [name, expected] of Object.entries({
    HOME: SANDBOX_HOME,
    CLAUDE_CONFIG_DIR: `${SANDBOX_RUNTIME}/claude`,
    XDG_CONFIG_HOME: `${SANDBOX_RUNTIME}/config`,
    XDG_CACHE_HOME: `${SANDBOX_RUNTIME}/cache`,
    XDG_DATA_HOME: `${SANDBOX_RUNTIME}/data`,
    XDG_STATE_HOME: `${SANDBOX_RUNTIME}/state`,
    XDG_RUNTIME_DIR: `${SANDBOX_RUNTIME}/runtime`,
    TMPDIR: "/tmp"
  })) {
    if (environment[name] !== expected) errors.push(`${name}: sandbox path mismatch`);
  }
  for (const name of ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_OAUTH_TOKEN", "DBUS_SESSION_BUS_ADDRESS"]) {
    if (Object.hasOwn(environment, name)) errors.push(`${name}: forbidden credential/session environment variable`);
  }
  return errors;
}

export function requestBytes(root) {
  const prompt = fs.readFileSync(path.join(root, "PROMPT.md"), "utf8");
  const input = readJson(path.join(root, "INPUT.json"));
  return Buffer.from(`${prompt}\n输入 JSON：\n${JSON.stringify(input)}`, "utf8");
}

const FORBIDDEN_OUTBOUND = [
  {label: "Unix absolute path", pattern: /(?:^|[\s"'`({\[=:,;])\/(?:[A-Za-z0-9._~-]+(?:\/[A-Za-z0-9._~-]+)*)/mu},
  {label: "Windows drive-root path", pattern: /\b[A-Za-z]:\\[^\s"'`<>|]+/u},
  {label: "credential-shaped token", pattern: /(?:sk-ant-[A-Za-z0-9_-]{12,}|AIza[0-9A-Za-z_-]{20,}|Bearer\s+[A-Za-z0-9._~+\/-]{16,})/u},
  {label: "real experiment artifact", pattern: /(?:SEALED-|SOURCE-AUDIT|REFERENCE-ESTIMATES|defect_id|adjudication|revision_id|\b[RP]\d{3,}\b)/iu},
  {label: "model/provider provenance", pattern: /(?:claude|anthropic|opus|haiku|sonnet|openai|chatgpt|gpt(?:-|\d)|gemini|google\s+ai|z\.ai|\bglm(?:-|\d)|\bgrok\b|\bmodel(?:_name|_id|_route)?\b|\bprovider\b)/iu}
];

export function scanOutboundBuffers(buffers) {
  const errors = [];
  for (const item of buffers) {
    const text = Buffer.isBuffer(item.bytes) ? item.bytes.toString("utf8") : String(item.bytes);
    const pathScanText = text.replace(/\b[a-z][a-z0-9+.-]*:\/\/[^\s"'`<>]+/giu, "[URL]");
    for (const rule of FORBIDDEN_OUTBOUND) {
      const inspected = rule.label.includes("path") ? pathScanText : text;
      if (rule.pattern.test(inspected)) errors.push(`${item.label}: ${rule.label}`);
    }
  }
  return errors;
}

export function validateFrozenArtifacts(root) {
  const errors = [];
  const manifestPath = path.join(root, "FROZEN-HASHES.json");
  let manifest = null;
  try {
    manifest = readJson(manifestPath);
  } catch (error) {
    return {manifest: null, errors: [`FROZEN-HASHES.json: ${error.message}`]};
  }
  if (manifest.schema_version !== "claude-opus-purity-frozen-hashes-v1" || manifest.status !== "FROZEN_BEFORE_ANY_MODEL_CALL") {
    errors.push("frozen hash manifest identity/status mismatch");
  }
  const names = Object.keys(manifest.files ?? {}).sort();
  if (JSON.stringify(names) !== JSON.stringify([...FROZEN_FILES].sort())) errors.push("frozen hash manifest file set mismatch");
  for (const name of FROZEN_FILES) {
    const file = path.join(root, name);
    if (!fs.existsSync(file)) {
      errors.push(`${name}: missing`);
      continue;
    }
    const stat = fs.lstatSync(file);
    if (!stat.isFile() || stat.isSymbolicLink()) errors.push(`${name}: not an ordinary file`);
    else if (sha256File(file) !== manifest.files?.[name]) errors.push(`${name}: frozen hash mismatch`);
  }
  return {manifest, errors};
}

function findExecutable(name, source = process.env) {
  for (const directory of String(source.PATH ?? "").split(path.delimiter).filter(Boolean)) {
    const candidate = path.join(directory, name);
    try {
      fs.accessSync(candidate, fs.constants.X_OK);
      return fs.realpathSync(candidate);
    } catch {
      // Continue through the explicit PATH.
    }
  }
  return null;
}

export function resolveClaudeRuntimeMaterials(source = process.env) {
  const errors = [];
  const hostHome = os.homedir();
  const authFile = path.join(hostHome, ".claude", ".credentials.json");
  const claudeBinary = findExecutable("claude", source);
  let authStat = null;
  if (!claudeBinary) {
    errors.push("Claude executable cannot be resolved from PATH");
  } else {
    try {
      const stat = fs.lstatSync(claudeBinary);
      if (!stat.isFile() || stat.isSymbolicLink()) errors.push("resolved Claude executable is not an ordinary file");
      if ((stat.mode & 0o111) === 0) errors.push("resolved Claude executable is not executable");
    } catch (error) {
      errors.push(`resolved Claude executable cannot be inspected: ${error.message}`);
    }
  }
  try {
    authStat = fs.lstatSync(authFile);
    if (!authStat.isFile() || authStat.isSymbolicLink()) errors.push("Claude credential source is not an ordinary non-symlink file");
    if ((authStat.mode & 0o077) !== 0) errors.push("Claude credential source permissions are broader than 0600");
    if (typeof process.getuid === "function" && authStat.uid !== process.getuid()) errors.push("Claude credential source owner mismatch");
    const credentials = readJson(authFile);
    if (!isPlainObject(credentials?.claudeAiOauth)
      || typeof credentials.claudeAiOauth.accessToken !== "string"
      || typeof credentials.claudeAiOauth.refreshToken !== "string") {
      errors.push("Claude credential source is not the expected first-party OAuth record");
    }
  } catch (error) {
    errors.push(`Claude credential source unavailable: ${error.message}`);
  }
  return {
    hostHome,
    authFile,
    claudeBinary,
    claudeBinarySha256: claudeBinary && fs.existsSync(claudeBinary) ? sha256File(claudeBinary) : null,
    errors
  };
}

export function createSandboxRuntime(authFile, parent = os.tmpdir()) {
  const directory = fs.mkdtempSync(path.join(parent, SANDBOX_RUNTIME_PREFIX));
  fs.chmodSync(directory, 0o700);
  let sourceDescriptor = null;
  try {
    sourceDescriptor = fs.openSync(authFile, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
    const sourceStat = fs.fstatSync(sourceDescriptor);
    assert(sourceStat.isFile() && (sourceStat.mode & 0o077) === 0, "Claude credential source changed during secure copy");
    const claudeDirectory = path.join(directory, "claude");
    fs.mkdirSync(claudeDirectory, {mode: 0o700});
    const copiedAuth = path.join(directory, AUTH_RELATIVE_PATH);
    writeNewFile(copiedAuth, fs.readFileSync(sourceDescriptor));
    return directory;
  } catch (error) {
    if (fs.existsSync(directory)) removeSandboxRuntime(directory);
    throw error;
  } finally {
    if (sourceDescriptor !== null) fs.closeSync(sourceDescriptor);
  }
}

export function removeSandboxRuntime(directory) {
  assert(path.basename(directory).startsWith(SANDBOX_RUNTIME_PREFIX), "refusing to remove an unrecognized sandbox runtime");
  const stat = fs.lstatSync(directory);
  assert(stat.isDirectory() && !stat.isSymbolicLink(), "refusing to remove a non-directory sandbox runtime");
  fs.rmSync(directory, {recursive: true, force: false});
}

export function createPublicBundle(root, parent = os.tmpdir()) {
  const directory = fs.mkdtempSync(path.join(parent, PUBLIC_BUNDLE_PREFIX));
  for (const name of ["PROMPT.md", "INPUT.json", "SCHEMA.json"]) {
    fs.copyFileSync(path.join(root, name), path.join(directory, name), fs.constants.COPYFILE_EXCL);
  }
  return directory;
}

export function removePublicBundle(directory) {
  assert(path.basename(directory).startsWith(PUBLIC_BUNDLE_PREFIX), "refusing to remove an unrecognized bundle directory");
  const stat = fs.lstatSync(directory);
  assert(stat.isDirectory() && !stat.isSymbolicLink(), "refusing to remove a non-directory bundle");
  fs.rmSync(directory, {recursive: true, force: false});
}

function sandboxPrefix({runtimeDirectory, claudeBinary, bundleDirectory = null}) {
  assert(path.isAbsolute(runtimeDirectory), "sandbox runtime path must be absolute");
  assert(path.isAbsolute(claudeBinary), "Claude executable path must be absolute");
  const args = [
    "--die-with-parent", "--new-session", "--cap-drop", "ALL", "--ro-bind", "/", "/",
    "--tmpfs", path.dirname(os.homedir()), "--dir", SANDBOX_HOME,
    "--tmpfs", "/tmp", "--tmpfs", "/run", "--tmpfs", "/opt",
    "--dev", "/dev", "--proc", "/proc", "--bind", runtimeDirectory, SANDBOX_RUNTIME,
    "--dir", "/opt/claude-purity", "--ro-bind", claudeBinary, SANDBOX_CLAUDE_BINARY
  ];
  if (bundleDirectory) args.push("--ro-bind", bundleDirectory, "/mnt", "--chdir", "/mnt");
  else args.push("--chdir", "/tmp");
  return args;
}

export function sandboxSmoke({runtimeDirectory, claudeBinary, environment}) {
  const prefix = sandboxPrefix({runtimeDirectory, claudeBinary});
  const versionResult = spawnSandbox(prefix, [SANDBOX_CLAUDE_BINARY, "--version"], environment);
  const authResult = spawnSandbox(prefix, [SANDBOX_CLAUDE_BINARY, "auth", "status"], environment);
  const hiddenHomeResult = spawnSandbox(prefix, ["/usr/bin/test", "!", "-e", path.join(os.homedir(), "research")], environment);
  const writableRuntimeResult = spawnSandbox(prefix, ["/bin/sh", "-c", `umask 077; : > ${SANDBOX_RUNTIME}/runtime-smoke; test -f ${SANDBOX_RUNTIME}/runtime-smoke`], environment);
  let auth = null;
  try {
    auth = JSON.parse(authResult.stdout);
  } catch {
    // Report only a generic failure; never surface raw auth output.
  }
  const errors = [];
  if (versionResult.status !== 0 || versionResult.stdout.trim() !== EXPECTED_CLAUDE_VERSION) errors.push("sandboxed Claude version check failed");
  if (authResult.status !== 0 || !isPlainObject(auth)) errors.push("sandboxed Claude auth status check failed");
  if (auth && (auth.loggedIn !== true || auth.authMethod !== "claude.ai" || auth.apiProvider !== EXPECTED_PROVIDER)) {
    errors.push("sandboxed Claude auth route is not first-party OAuth");
  }
  if (hiddenHomeResult.status !== 0) errors.push("sandbox did not hide the entire host HOME");
  if (writableRuntimeResult.status !== 0) errors.push("sandbox private runtime is not writable");
  return {
    version: versionResult.status === 0 ? versionResult.stdout.trim() : null,
    authMethod: auth?.authMethod ?? null,
    apiProvider: auth?.apiProvider ?? null,
    hostHomeHidden: hiddenHomeResult.status === 0,
    runtimeWritable: writableRuntimeResult.status === 0,
    errors
  };
}

function spawnSandbox(prefix, command, environment) {
  const result = spawnSync("bwrap", [...prefix, "--", ...command], {
    cwd: "/tmp",
    env: environment,
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
    timeout: 30 * 1000
  });
  return {status: result.status, stdout: result.stdout ?? "", stderr: result.stderr ?? "", error: result.error ?? null};
}

export function invocationPlan(bundleDirectory, request, runtimeDirectory, claudeBinary) {
  const schema = readJson(path.join(bundleDirectory, "SCHEMA.json"));
  delete schema.$schema;
  const schemaText = JSON.stringify(schema);
  const leakErrors = scanOutboundBuffers([
    {label: "request", bytes: request},
    {label: "schema", bytes: schemaText}
  ]);
  assert(leakErrors.length === 0, `outbound sanitization failed: ${leakErrors.join("; ")}`);
  const args = [
    "--print", "--model", EXPECTED_MODEL, "--effort", "medium",
    "--output-format", "stream-json", "--verbose", "--safe-mode", "--tools", "",
    "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}",
    "--no-session-persistence", "--disable-slash-commands", "--prompt-suggestions", "false",
    "--permission-mode", "plan", "--json-schema", schemaText, "--", request.toString("utf8")
  ];
  const displayArgs = args.map(value => value === schemaText ? "[SCHEMA_BYTES_FROM_./SCHEMA.json]" : value === request.toString("utf8") ? "[REQUEST_BYTES]" : value);
  return {
    command: "bwrap",
    args: [
      ...sandboxPrefix({runtimeDirectory, claudeBinary, bundleDirectory}), "--", SANDBOX_CLAUDE_BINARY, ...args
    ],
    display_args: [
      "[OS_SANDBOX: entire host HOME masked; private ephemeral runtime writable; one OAuth credential file copied into runtime; synthetic bundle read-only; no local path recorded]",
      "claude", ...displayArgs
    ]
  };
}

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function parseJsonLines(raw) {
  const lines = raw.split(/\r?\n/u).filter(line => line.trim());
  return lines.map((line, index) => {
    try {
      const event = JSON.parse(line);
      if (!isPlainObject(event)) throw new Error("event is not an object");
      return event;
    } catch (error) {
      throw new Error(`line ${index + 1}: invalid JSON event: ${error.message}`);
    }
  });
}

function validateSubagentStats(stats) {
  if (!isPlainObject(stats)) return false;
  const scalarKeys = ["spawned", "started_in_background", "max_depth", "spawned_by_subagents", "completed", "failed"];
  const nestedKeys = {
    requested: ["background", "foreground", "unset"],
    killed: ["parent", "user", "system"],
    refused: ["depth_limit", "concurrency_limit", "budget"]
  };
  if (!sameKeySet(stats, [...scalarKeys, ...Object.keys(nestedKeys), "by_type"])) return false;
  for (const name of scalarKeys) {
    if (!isNonnegativeInteger(stats[name]) || stats[name] !== 0) return false;
  }
  for (const [name, requiredKeys] of Object.entries(nestedKeys)) {
    if (!isPlainObject(stats[name]) || !sameKeySet(stats[name], requiredKeys)) return false;
    if (requiredKeys.some(key => !isNonnegativeInteger(stats[name][key]) || stats[name][key] !== 0)) return false;
  }
  return isPlainObject(stats.by_type) && Object.keys(stats.by_type).length === 0;
}

function sameKeySet(value, expected) {
  return isPlainObject(value) && sameJson(Object.keys(value).sort(), [...expected].sort());
}

function keysAreSubset(value, allowed) {
  return isPlainObject(value) && Object.keys(value).every(key => allowed.includes(key));
}

function normalizedKey(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]/gu, "");
}

const INIT_ALLOWED_KEYS = [
  "type", "subtype", "cwd", "session_id", "tools", "mcp_servers", "model", "permissionMode",
  "slash_commands", "apiKeySource", "claude_code_version", "output_style", "agents", "skills", "plugins",
  "capabilities", "analytics_disabled", "product_feedback_disabled", "uuid", "messaging_socket_path",
  "fast_mode_state", "fast_mode_disabled_reason"
];
const THINKING_EVENT_ALLOWED_KEYS = ["type", "subtype", "estimated_tokens", "estimated_tokens_delta", "session_id", "uuid"];
const RATE_LIMIT_EVENT_ALLOWED_KEYS = ["type", "rate_limit_info", "session_id", "uuid"];
const RATE_LIMIT_INFO_ALLOWED_KEYS = ["status", "resetsAt", "rateLimitType", "utilization", "isUsingOverage", "unifiedWindows"];
const RATE_LIMIT_WINDOW_ALLOWED_KEYS = ["utilization", "resetsAt"];
const ASSISTANT_EVENT_ALLOWED_KEYS = ["type", "message", "parent_tool_use_id", "session_id", "uuid", "timestamp", "request_id"];
const ASSISTANT_MESSAGE_ALLOWED_KEYS = [
  "model", "id", "type", "role", "content", "stop_reason", "stop_sequence", "stop_details", "usage",
  "diagnostics", "context_management"
];
const ASSISTANT_USAGE_ALLOWED_KEYS = [
  "input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "cache_creation",
  "service_tier", "inference_geo"
];
const USER_EVENT_ALLOWED_KEYS = ["type", "message", "parent_tool_use_id", "session_id", "uuid", "timestamp", "tool_use_result"];
const RESULT_ALLOWED_KEYS = [
  "type", "subtype", "is_error", "stop_reason", "terminal_reason", "api_error_status", "num_turns",
  "structured_output", "result", "usage", "modelUsage", "permission_denials", "subagent_stats", "duration_api_ms",
  "session_id", "total_cost_usd", "fast_mode_state", "fast_mode_disabled_reason", "duration_ms", "uuid", "ttft_ms",
  "ttft_stream_ms", "time_to_request_ms", "queued_turn_count"
];
const RESULT_USAGE_ALLOWED_KEYS = [
  "input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens_details",
  "server_tool_use", "service_tier", "cache_creation", "inference_geo", "iterations", "speed"
];
const ITERATION_ALLOWED_KEYS = [
  "type", "model", "provider", "input_tokens", "output_tokens", "cache_read_input_tokens",
  "cache_creation_input_tokens", "cache_creation"
];
const MODEL_USAGE_ALLOWED_KEYS = [
  "inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens", "webSearchRequests", "costUSD",
  "contextWindow", "maxOutputTokens", "canonicalModel", "provider", "costBasis"
];
const CACHE_CREATION_ALLOWED_KEYS = ["ephemeral_5m_input_tokens", "ephemeral_1h_input_tokens"];
const OUTPUT_TOKEN_DETAILS_ALLOWED_KEYS = ["thinking_tokens"];

function isNonnegativeInteger(value) {
  return Number.isSafeInteger(value) && value >= 0;
}

function cacheCreationSchemaIsValid(value) {
  return isPlainObject(value) && keysAreSubset(value, CACHE_CREATION_ALLOWED_KEYS)
    && Object.values(value).every(isNonnegativeInteger);
}

function walkObjects(value, visitor, trail = []) {
  if (Array.isArray(value)) {
    value.forEach((child, index) => walkObjects(child, visitor, [...trail, index]));
    return;
  }
  if (!isPlainObject(value)) return;
  visitor(value, trail);
  for (const [key, child] of Object.entries(value)) walkObjects(child, visitor, [...trail, key]);
}

function collectGlobalSignals(events) {
  const toolUses = [];
  const toolResults = [];
  const forbiddenToolSignals = [];
  const parentToolSignals = [];
  const promptSuggestionSignals = [];
  const toolUseIdSignals = [];
  const toolUseResultSignals = [];
  const structuredNameSignals = [];
  const modelSignals = [];
  const canonicalModelSignals = [];
  const providerSignals = [];
  const suspiciousNormalizedSignals = [];
  walkObjects(events, (object, trail) => {
    if (object.type === "tool_use") toolUses.push({object, trail});
    if (object.type === "tool_result") toolResults.push({object, trail});
    if (typeof object.type === "string"
      && /^(?:tool_(?:call|execution)|web_(?:search|fetch)|mcp_(?:call|result)|computer_(?:use|result))$/u.test(object.type)) {
      forbiddenToolSignals.push({object, trail});
    }
    if (Object.hasOwn(object, "parent_tool_use_id") && object.parent_tool_use_id !== null) parentToolSignals.push(trail);
    if (object.type === "prompt_suggestion" || Object.hasOwn(object, "prompt_suggestion")) promptSuggestionSignals.push(trail);
    if (Object.hasOwn(object, "tool_use_id")) toolUseIdSignals.push({object, trail});
    if (Object.hasOwn(object, "tool_use_result")) toolUseResultSignals.push({object, trail});
    if (object.name === "StructuredOutput") structuredNameSignals.push({object, trail});
    for (const [key, value] of Object.entries(object)) {
      const normalized = normalizedKey(key);
      if (normalized.includes("model") && normalized !== "modelusage") {
        modelSignals.push({value, trail: [...trail, key]});
      }
      if (normalized === "canonicalmodel") canonicalModelSignals.push({value, trail: [...trail, key]});
      if (normalized.includes("provider")) providerSignals.push({value, trail: [...trail, key]});
      if (normalized.includes("prompt") && normalized.includes("suggestion")) suspiciousNormalizedSignals.push({kind: "prompt_suggestion", trail: [...trail, key]});
      if (normalized === "parenttooluseid" && key !== "parent_tool_use_id") suspiciousNormalizedSignals.push({kind: "parent_tool_use_id_alias", trail: [...trail, key]});
      if (normalized.includes("subagentid")) suspiciousNormalizedSignals.push({kind: "subagent_id", trail: [...trail, key]});
      const toolOrServerKey = (normalized.startsWith("tool") && !["tools", "tooluseid", "tooluseresult"].includes(normalized))
        || (normalized.startsWith("mcp") && normalized !== "mcpservers")
        || normalized.startsWith("websearch") || normalized.startsWith("webfetch")
        || normalized.startsWith("computeruse");
      if (toolOrServerKey && !["websearchrequests", "webfetchrequests"].includes(normalized)) {
        suspiciousNormalizedSignals.push({kind: "tool_or_server_key", trail: [...trail, key]});
      }
    }
    if (typeof object.type === "string") {
      const normalizedType = normalizedKey(object.type);
      if ((normalizedType.startsWith("tool") && !["tooluse", "toolresult"].includes(normalizedType))
        || normalizedType.startsWith("websearch") || normalizedType.startsWith("webfetch")
        || normalizedType.startsWith("mcp") || normalizedType.startsWith("computeruse")) {
        suspiciousNormalizedSignals.push({kind: "tool_or_server_type", trail: [...trail, "type"]});
      }
      if (normalizedType === "promptsuggestion") suspiciousNormalizedSignals.push({kind: "prompt_suggestion", trail: [...trail, "type"]});
    }
    for (const key of Object.keys(object)) {
      if (/^(?:toolAction|toolSummary|tool_call|tool_execution|mcp_call|web_search|web_fetch)$/iu.test(key)) {
        forbiddenToolSignals.push({object, trail: [...trail, key]});
      }
    }
  });
  return {toolUses, toolResults, forbiddenToolSignals, parentToolSignals, promptSuggestionSignals, toolUseIdSignals, toolUseResultSignals, structuredNameSignals, modelSignals, canonicalModelSignals, providerSignals, suspiciousNormalizedSignals};
}

function containsRouteControlSignal(value) {
  if (typeof value === "string") return /(?:advisor|fallback)/iu.test(value);
  if (!value || typeof value !== "object") return false;
  return Object.entries(value).some(([key, child]) => /(?:advisor|fallback)/iu.test(key) || (Array.isArray(child)
    ? child.some(containsRouteControlSignal)
    : containsRouteControlSignal(child)));
}

function sameJson(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

export function validateSyntheticResponse(response) {
  const expected = {
    classifications: [
      {id: "Q1", class: "NEGATIVE"},
      {id: "Q2", class: "ZERO"},
      {id: "Q3", class: "POSITIVE"}
    ]
  };
  return sameJson(response, expected) ? [] : ["synthetic structured response mismatch"];
}

export function parseClaudeRaw(raw) {
  const errors = [];
  let events;
  try {
    events = parseJsonLines(raw);
  } catch (error) {
    return {response: null, metadata: {}, errors: [error.message]};
  }
  const initEvents = events.filter(event => event.type === "system" && event.subtype === "init");
  const resultEvents = events.filter(event => event.type === "result");
  const assistantEvents = events.filter(event => event.type === "assistant");
  const userEvents = events.filter(event => event.type === "user");
  if (initEvents.length !== 1) errors.push(`expected one Claude init event, got ${initEvents.length}`);
  if (resultEvents.length !== 1) errors.push(`expected one Claude result event, got ${resultEvents.length}`);
  if (assistantEvents.length === 0) errors.push("expected at least one Claude assistant event");
  if (userEvents.length !== 1) errors.push(`expected one Claude receipt user event, got ${userEvents.length}`);
  const init = initEvents[0] ?? null;
  const terminal = resultEvents[0] ?? null;

  const allowedEventKinds = new Set(["system:init", "system:thinking_tokens", "rate_limit_event:", "assistant:", "user:", "result:success"]);
  const unknownEventKinds = events
    .map(event => `${String(event.type ?? "<missing>")}:${String(event.subtype ?? "")}`)
    .filter(kind => !allowedEventKinds.has(kind));
  if (unknownEventKinds.length) errors.push(`Claude unknown event kind detected: ${[...new Set(unknownEventKinds)].join(",")}`);
  const initIndex = init ? events.indexOf(init) : -1;
  const terminalIndex = terminal ? events.indexOf(terminal) : -1;
  const firstAssistantIndex = events.findIndex(event => event.type === "assistant");
  const lastAssistantIndex = events.findLastIndex(event => event.type === "assistant");
  const userIndex = userEvents.length === 1 ? events.indexOf(userEvents[0]) : -1;
  if (initIndex !== 0) errors.push("Claude init event must be first");
  if (terminalIndex !== events.length - 1) errors.push("Claude result event must be terminal");
  if (firstAssistantIndex < 1 || lastAssistantIndex < firstAssistantIndex) errors.push("Claude assistant event order is invalid");
  if (events.slice(1, firstAssistantIndex).some(event => !((event.type === "system" && event.subtype === "thinking_tokens") || event.type === "rate_limit_event"))) {
    errors.push("Claude pre-assistant event order is invalid");
  }
  if (events.slice(firstAssistantIndex, lastAssistantIndex + 1).some(event => event.type !== "assistant")) {
    errors.push("Claude assistant events must be contiguous");
  }
  if (userIndex !== lastAssistantIndex + 1 || terminalIndex !== userIndex + 1) {
    errors.push("Claude receipt/result order is invalid");
  }
  for (const event of events) {
    if (event.type === "system" && event.subtype === "thinking_tokens" && !keysAreSubset(event, THINKING_EVENT_ALLOWED_KEYS)) {
      errors.push("Claude thinking-token event telemetry contains unknown fields");
    }
    if (event.type === "rate_limit_event") {
      if (!keysAreSubset(event, RATE_LIMIT_EVENT_ALLOWED_KEYS) || !isPlainObject(event.rate_limit_info)
        || !keysAreSubset(event.rate_limit_info, RATE_LIMIT_INFO_ALLOWED_KEYS)) {
        errors.push("Claude rate-limit event telemetry contains unknown fields");
      }
      const windows = event.rate_limit_info?.unifiedWindows;
      if (windows !== undefined && (!isPlainObject(windows) || !keysAreSubset(windows, ["five_hour", "seven_day"])
        || Object.values(windows).some(window => !isPlainObject(window) || !keysAreSubset(window, RATE_LIMIT_WINDOW_ALLOWED_KEYS)))) {
        errors.push("Claude rate-limit window telemetry contains unknown fields");
      }
    }
  }

  if (init) {
    if (!keysAreSubset(init, INIT_ALLOWED_KEYS)) errors.push("Claude init telemetry contains unknown fields");
    if (!sameJson(init.tools, ["StructuredOutput"])) errors.push(`Claude exposed tools mismatch: ${JSON.stringify(init.tools)}`);
    if (!sameJson(init.mcp_servers, [])) errors.push("Claude MCP servers were exposed or telemetry is missing");
    if (init.model !== EXPECTED_MODEL) errors.push(`Claude initialized model mismatch: ${init.model ?? "<missing>"}`);
    if (init.permissionMode !== "plan") errors.push(`Claude permission mode mismatch: ${init.permissionMode ?? "<missing>"}`);
    if (!sameJson(init.slash_commands, [])) errors.push("Claude slash commands were exposed or telemetry is missing");
    if (!sameJson(init.skills, [])) errors.push("Claude skills were exposed or telemetry is missing");
    if (!sameJson(init.plugins, [])) errors.push("Claude plugins were exposed or telemetry is missing");
    if (init.apiKeySource !== "none") errors.push(`Claude init API key source mismatch: ${init.apiKeySource ?? "<missing>"}`);
    if (init.cwd !== "/mnt") errors.push(`Claude init cwd mismatch: ${init.cwd ?? "<missing>"}`);
    if (init.claude_code_version !== EXPECTED_CLAUDE_INIT_VERSION) errors.push(`Claude init version mismatch: ${init.claude_code_version ?? "<missing>"}`);
  }

  const assistantModels = [];
  const directAssistantBlocks = [];
  for (const event of assistantEvents) {
    if (!keysAreSubset(event, ASSISTANT_EVENT_ALLOWED_KEYS)) errors.push("Claude assistant event telemetry contains unknown fields");
    if (!isPlainObject(event.message)) {
      errors.push("Claude assistant message telemetry is missing");
      continue;
    }
    assistantModels.push(event.message.model ?? null);
    if (event.message.model !== EXPECTED_MODEL) errors.push(`Claude assistant model mismatch: ${event.message.model ?? "<missing>"}`);
    if (event.message.role !== "assistant") errors.push("Claude assistant role mismatch");
    if (event.message.type !== "message") errors.push("Claude assistant message type mismatch");
    if (!keysAreSubset(event.message, ASSISTANT_MESSAGE_ALLOWED_KEYS)) errors.push("Claude assistant message telemetry contains unknown fields");
    if (Object.hasOwn(event.message, "usage") && !keysAreSubset(event.message.usage, ASSISTANT_USAGE_ALLOWED_KEYS)) {
      errors.push("Claude assistant message usage contains unknown or server-tool telemetry");
    }
    if (isPlainObject(event.message.usage) && Object.hasOwn(event.message.usage, "cache_creation")
      && !cacheCreationSchemaIsValid(event.message.usage.cache_creation)) errors.push("Claude assistant cache telemetry schema mismatch");
    if (Object.hasOwn(event.message, "diagnostics") && event.message.diagnostics !== null) errors.push("Claude assistant diagnostics telemetry must be null");
    if (Object.hasOwn(event.message, "context_management") && event.message.context_management !== null) errors.push("Claude assistant context-management telemetry must be null");
    if (!Array.isArray(event.message.content) || event.message.content.length === 0) {
      errors.push("Claude assistant content telemetry is missing");
      continue;
    }
    for (const block of event.message.content) {
      directAssistantBlocks.push(block);
      if (!isPlainObject(block) || !["thinking", "text", "tool_use"].includes(block.type)) {
        errors.push(`Claude unknown assistant content block: ${block?.type ?? "<missing>"}`);
      } else if (block.type === "thinking" && (typeof block.thinking !== "string" || typeof block.signature !== "string")) {
        errors.push("Claude thinking block schema mismatch");
      } else if (block.type === "text" && typeof block.text !== "string") {
        errors.push("Claude text block schema mismatch");
      } else if (block.type === "thinking" && !sameKeySet(block, ["type", "thinking", "signature"])) {
        errors.push("Claude thinking block schema mismatch");
      } else if (block.type === "text" && !sameKeySet(block, ["type", "text"])) {
        errors.push("Claude text block schema mismatch");
      } else if (block.type === "tool_use" && !sameKeySet(block, ["type", "id", "name", "input", "caller"])) {
        errors.push("Claude StructuredOutput block schema mismatch");
      }
    }
    if (!Object.hasOwn(event, "parent_tool_use_id") || event.parent_tool_use_id !== null) errors.push("Claude assistant parent tool-use telemetry is missing or nonnull");
  }
  const globalSignals = collectGlobalSignals(events);
  if (globalSignals.modelSignals.some(signal => signal.value !== EXPECTED_MODEL)
    || globalSignals.canonicalModelSignals.some(signal => signal.value !== EXPECTED_MODEL)) {
    errors.push("Claude global model telemetry mismatch");
  }
  if (globalSignals.providerSignals.some(signal => signal.value !== EXPECTED_PROVIDER)) errors.push("Claude global provider telemetry mismatch");
  if (globalSignals.suspiciousNormalizedSignals.length) errors.push("Claude normalized alias/tool/server signal detected");
  const directToolUses = directAssistantBlocks.filter(block => block?.type === "tool_use");
  const structuredTool = directToolUses.length === 1 ? directToolUses[0] : null;
  const structuredId = directToolUses.length === 1 && globalSignals.toolUses.length === 1
    && globalSignals.toolUses[0].object === structuredTool
    && globalSignals.structuredNameSignals.length === 1 && globalSignals.structuredNameSignals[0].object === structuredTool
    && structuredTool?.name === "StructuredOutput" && typeof structuredTool?.id === "string" && structuredTool.id
    ? structuredTool.id
    : null;
  if (!structuredId) errors.push("Claude must invoke exactly one direct identified StructuredOutput tool and no other global tool_use");
  if (structuredTool && (assistantEvents.at(-1)?.message?.content?.at(-1) !== structuredTool)) errors.push("Claude StructuredOutput tool must be the final assistant block");
  if (structuredTool && !sameJson(structuredTool.caller, {type: "direct"})) errors.push("Claude StructuredOutput caller telemetry is missing or not direct");

  const receiptEvent = userEvents.length === 1 ? userEvents[0] : null;
  if (receiptEvent && !keysAreSubset(receiptEvent, USER_EVENT_ALLOWED_KEYS)) errors.push("Claude receipt event telemetry contains unknown fields");
  if (receiptEvent && (!isPlainObject(receiptEvent.message) || !sameKeySet(receiptEvent.message, ["role", "content"]))) errors.push("Claude receipt message schema mismatch");
  const receiptBlocks = Array.isArray(receiptEvent?.message?.content) ? receiptEvent.message.content : [];
  const directReceipts = receiptBlocks.filter(block => block?.type === "tool_result");
  const receipt = directReceipts.length === 1 ? directReceipts[0] : null;
  if (!receiptEvent || !isPlainObject(receiptEvent.message) || receiptEvent.message.role !== "user"
    || receiptBlocks.length !== 1 || directReceipts.length !== 1
    || globalSignals.toolResults.length !== 1 || globalSignals.toolResults[0].object !== receipt
    || globalSignals.toolUseIdSignals.length !== 1 || globalSignals.toolUseIdSignals[0].object !== receipt
    || globalSignals.toolUseResultSignals.length !== 1 || globalSignals.toolUseResultSignals[0].object !== receiptEvent
    || !structuredId || receipt?.tool_use_id !== structuredId) {
    errors.push("Claude must return exactly one matching StructuredOutput receipt");
  }
  if (receiptEvent && (!Object.hasOwn(receiptEvent, "parent_tool_use_id") || receiptEvent.parent_tool_use_id !== null)) errors.push("Claude receipt parent tool-use telemetry is missing or nonnull");
  if (receipt && (!sameKeySet(receipt, ["type", "tool_use_id", "content"]) || typeof receipt.content !== "string" || receipt.content.length === 0)) errors.push("Claude StructuredOutput receipt content/schema is invalid");
  if (receiptEvent && (typeof receiptEvent.tool_use_result !== "string" || receiptEvent.tool_use_result !== receipt?.content)) errors.push("Claude StructuredOutput receipt terminal acknowledgement mismatch");
  if (globalSignals.forbiddenToolSignals.length) errors.push("Claude non-StructuredOutput tool signal detected");
  if (globalSignals.parentToolSignals.length) errors.push("Claude subagent/parent tool-use event detected");
  if (globalSignals.promptSuggestionSignals.length) errors.push("Claude prompt_suggestion signal detected");
  if (events.some(containsRouteControlSignal)) errors.push("Claude advisor or fallback signal detected");

  let response = terminal?.structured_output ?? null;
  let parsedResult = null;
  if (!isPlainObject(response)) errors.push("Claude terminal structured_output telemetry is missing");
  if (typeof terminal?.result !== "string") {
    errors.push("Claude terminal result telemetry is missing");
  } else {
    try {
      parsedResult = JSON.parse(terminal.result);
    } catch (error) {
      errors.push(`Claude terminal result parse failed: ${error.message}`);
    }
  }
  if (structuredId && (!sameJson(structuredTool.input, response) || !sameJson(parsedResult, response))) {
    errors.push("Claude StructuredOutput input and terminal result do not match");
  }
  if (terminal && (terminal.subtype !== "success" || terminal.is_error !== false)) errors.push("Claude terminal result was not successful");
  if (terminal && !keysAreSubset(terminal, RESULT_ALLOWED_KEYS)) errors.push("Claude result telemetry contains unknown fields");
  if (terminal && terminal.stop_reason !== "tool_use") errors.push(`Claude terminal stop reason mismatch: ${terminal.stop_reason ?? "<missing>"}`);
  if (terminal && terminal.terminal_reason !== "completed") errors.push(`Claude terminal reason mismatch: ${terminal.terminal_reason ?? "<missing>"}`);
  if (terminal && terminal.api_error_status !== null) errors.push("Claude terminal API error telemetry is missing or nonnull");
  if (!isNonnegativeInteger(terminal?.num_turns) || terminal.num_turns < 1) errors.push("Claude terminal num_turns telemetry is missing or invalid");

  if (!terminal || !Object.hasOwn(terminal, "modelUsage") || !isPlainObject(terminal.modelUsage)) {
    errors.push("Claude modelUsage telemetry is missing");
  }
  const modelUsageKeys = isPlainObject(terminal?.modelUsage) ? Object.keys(terminal.modelUsage) : [];
  if (!sameJson(modelUsageKeys, ["claude-opus-5"])) {
    errors.push(`Claude modelUsage keys mismatch: ${modelUsageKeys.join(",") || "<missing>"}`);
  }
  const opusUsage = terminal?.modelUsage?.["claude-opus-5"];
  const usageTokenKeys = ["inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"];
  if (!isPlainObject(opusUsage)) {
    errors.push("Claude Opus modelUsage record is missing or not an object");
  } else {
    if (!keysAreSubset(opusUsage, MODEL_USAGE_ALLOWED_KEYS)) errors.push("Claude modelUsage contains unknown fields");
    if (opusUsage.canonicalModel !== EXPECTED_MODEL) errors.push("Claude canonical model telemetry mismatch");
    if (opusUsage.provider !== EXPECTED_PROVIDER) errors.push("Claude modelUsage provider telemetry mismatch");
    if (typeof opusUsage.webSearchRequests !== "number" || opusUsage.webSearchRequests !== 0) errors.push("Claude modelUsage server-search telemetry is missing or nonzero");
    if (usageTokenKeys.some(key => !isNonnegativeInteger(opusUsage[key]))) errors.push("Claude modelUsage token telemetry is missing or invalid");
    else if (opusUsage.outputTokens <= 0 || opusUsage.inputTokens + opusUsage.cacheReadInputTokens + opusUsage.cacheCreationInputTokens <= 0) {
      errors.push("Claude modelUsage token telemetry is zero");
    }
  }

  const iterations = terminal?.usage?.iterations;
  if (!Array.isArray(iterations) || iterations.length === 0) {
    errors.push("Claude usage.iterations telemetry is missing");
  } else {
    for (const iteration of iterations) {
      if (!isPlainObject(iteration) || iteration.type !== "message") {
        errors.push("Claude usage.iterations contains a non-message iteration");
        continue;
      }
      if (!keysAreSubset(iteration, ITERATION_ALLOWED_KEYS)) errors.push("Claude usage.iterations contains unknown fields");
      if (Object.hasOwn(iteration, "cache_creation") && !cacheCreationSchemaIsValid(iteration.cache_creation)) errors.push("Claude iteration cache telemetry schema mismatch");
      if (Object.hasOwn(iteration, "model") && iteration.model !== EXPECTED_MODEL) errors.push("Claude usage.iterations model mismatch");
      if (Object.hasOwn(iteration, "provider") && iteration.provider !== EXPECTED_PROVIDER) errors.push("Claude usage.iterations provider mismatch");
      const keys = ["input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"];
      if (keys.some(key => !isNonnegativeInteger(iteration[key]))) errors.push("Claude usage.iterations token telemetry is missing or invalid");
      else if (iteration.output_tokens <= 0 || iteration.input_tokens + iteration.cache_read_input_tokens + iteration.cache_creation_input_tokens <= 0) {
        errors.push("Claude usage.iterations token telemetry is zero");
      }
    }
  }
  const terminalTokenKeys = ["input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"];
  if (isPlainObject(terminal?.usage) && !keysAreSubset(terminal.usage, RESULT_USAGE_ALLOWED_KEYS)) errors.push("Claude terminal usage contains unknown fields");
  if (isPlainObject(terminal?.usage) && Object.hasOwn(terminal.usage, "cache_creation")
    && !cacheCreationSchemaIsValid(terminal.usage.cache_creation)) errors.push("Claude terminal cache telemetry schema mismatch");
  if (isPlainObject(terminal?.usage) && Object.hasOwn(terminal.usage, "output_tokens_details")
    && (!isPlainObject(terminal.usage.output_tokens_details)
      || !keysAreSubset(terminal.usage.output_tokens_details, OUTPUT_TOKEN_DETAILS_ALLOWED_KEYS)
      || Object.values(terminal.usage.output_tokens_details).some(value => !isNonnegativeInteger(value)))) {
    errors.push("Claude terminal output-token detail telemetry schema mismatch");
  }
  if (!isPlainObject(terminal?.usage) || terminalTokenKeys.some(key => !isNonnegativeInteger(terminal.usage[key]))) {
    errors.push("Claude terminal usage token telemetry is missing or invalid");
  } else if (Array.isArray(iterations) && iterations.length) {
    for (const key of terminalTokenKeys) {
      const total = iterations.reduce((sum, iteration) => sum + (isNonnegativeInteger(iteration?.[key]) ? iteration[key] : 0), 0);
      if (total !== terminal.usage[key]) errors.push(`Claude usage.iterations ${key} total mismatch`);
    }
    if (isPlainObject(opusUsage)) {
      const mapping = {input_tokens: "inputTokens", output_tokens: "outputTokens", cache_read_input_tokens: "cacheReadInputTokens", cache_creation_input_tokens: "cacheCreationInputTokens"};
      for (const [terminalKey, modelKey] of Object.entries(mapping)) {
        if (terminal.usage[terminalKey] !== opusUsage[modelKey]) errors.push(`Claude modelUsage ${modelKey} total mismatch`);
      }
    }
  }
  const serverToolUse = terminal?.usage?.server_tool_use;
  if (!isPlainObject(serverToolUse)) {
    errors.push("Claude server_tool_use telemetry is missing");
  } else if (!sameKeySet(serverToolUse, ["web_search_requests", "web_fetch_requests"])
    || !isNonnegativeInteger(serverToolUse.web_search_requests) || !isNonnegativeInteger(serverToolUse.web_fetch_requests)) {
    errors.push("Claude server_tool_use counters are incomplete");
  } else if (serverToolUse.web_search_requests !== 0 || serverToolUse.web_fetch_requests !== 0) {
    errors.push("Claude server tool use detected");
  }
  if (!isPlainObject(terminal?.subagent_stats)) {
    errors.push("Claude subagent_stats telemetry is missing");
  } else if (!validateSubagentStats(terminal.subagent_stats)) {
    errors.push("Claude subagent telemetry is incomplete or contains activity");
  }
  if (!Array.isArray(terminal?.permission_denials) || terminal.permission_denials.length !== 0) {
    errors.push("Claude permission-denial telemetry is missing or nonempty");
  }

  errors.push(...validateSyntheticResponse(response));
  return {
    response,
    metadata: {
      initialized_model: init?.model ?? null,
      claude_code_version: init?.claude_code_version ?? null,
      assistant_models: [...new Set(assistantModels)],
      event_count: events.length,
      assistant_event_count: assistantEvents.length,
      user_event_count: userEvents.length,
      unknown_event_kinds: [...new Set(unknownEventKinds)],
      exposed_tools: init?.tools ?? null,
      mcp_servers: init?.mcp_servers ?? null,
      global_tool_use_count: globalSignals.toolUses.length,
      global_tool_result_count: globalSignals.toolResults.length,
      global_model_field_count: globalSignals.modelSignals.length,
      global_provider_field_count: globalSignals.providerSignals.length,
      structured_output_calls: directToolUses.length,
      structured_output_receipts: directReceipts.length,
      model_usage_keys: modelUsageKeys,
      iteration_types: Array.isArray(iterations) ? [...new Set(iterations.map(iteration => iteration?.type ?? null))] : null,
      subagent_stats_present: isPlainObject(terminal?.subagent_stats),
      server_tool_use: serverToolUse ?? null,
      result_subtype: terminal?.subtype ?? null
    },
    errors: [...new Set(errors)]
  };
}

export function candidateFromRaw({raw, call}) {
  const parsed = parseClaudeRaw(raw);
  return {
    schema_version: "claude-opus-route-purity-candidate-v1",
    experiment: EXPERIMENT,
    route: ROUTE_SLUG,
    attempt: call.attempt,
    request_sha256: call.request_sha256,
    input_sha256: call.input_sha256,
    prompt_sha256: call.prompt_sha256,
    schema_sha256: call.schema_sha256,
    raw_stdout_sha256: call.raw_stdout_sha256,
    raw_stderr_sha256: call.raw_stderr_sha256,
    route_metadata: parsed.metadata,
    valid: parsed.errors.length === 0,
    qualification: parsed.errors.length === 0 ? "QUALIFIED_OPUS_ONLY" : "INVALID_ROUTE_PURITY",
    validation_errors: parsed.errors,
    response: parsed.response
  };
}

function gitRun(repo, args) {
  const result = spawnSync("git", args, {cwd: repo, encoding: "utf8"});
  return {
    status: result.status,
    stdout: (result.stdout ?? "").trim(),
    stderr: (result.stderr ?? "").trim()
  };
}

export function repositoryForPackage(root) {
  return path.resolve(root, "../../../..");
}

export function packageRelativePath(root) {
  return path.relative(repositoryForPackage(root), root).split(path.sep).join("/");
}

export function gitPackageLineage(root, commit = "HEAD") {
  const repo = repositoryForPackage(root);
  const relative = packageRelativePath(root);
  const errors = [];
  const resolved = gitRun(repo, ["rev-parse", `${commit}^{commit}`]);
  const commitOid = resolved.status === 0 && /^[0-9a-f]{40}$/u.test(resolved.stdout) ? resolved.stdout : null;
  if (!commitOid) errors.push(`cannot resolve package commit ${commit}`);
  const tree = commitOid ? gitRun(repo, ["rev-parse", `${commitOid}:${relative}`]) : {status: 1, stdout: ""};
  const treeOid = tree.status === 0 && /^[0-9a-f]{40}$/u.test(tree.stdout) ? tree.stdout : null;
  if (!treeOid) errors.push("cannot resolve package tree at commit");
  const blobs = {};
  for (const name of [...FROZEN_FILES, "FROZEN-HASHES.json"]) {
    const object = commitOid ? gitRun(repo, ["rev-parse", `${commitOid}:${relative}/${name}`]) : {status: 1, stdout: ""};
    if (object.status !== 0 || !/^[0-9a-f]{40}$/u.test(object.stdout)) {
      errors.push(`${name}: cannot resolve Git blob at package commit`);
      continue;
    }
    const type = gitRun(repo, ["cat-file", "-t", object.stdout]);
    if (type.status !== 0 || type.stdout !== "blob") errors.push(`${name}: package Git object is not a blob`);
    blobs[name] = object.stdout;
  }
  return {repo, relative, commit: commitOid, tree: treeOid, blobs, errors};
}

export function validateCurrentHeadLineage(root, preflight) {
  const errors = [];
  const repo = repositoryForPackage(root);
  const head = gitRun(repo, ["rev-parse", "HEAD"]);
  if (head.status !== 0 || !/^[0-9a-f]{40}$/u.test(head.stdout)) return ["cannot resolve current HEAD"];
  const ancestor = gitRun(repo, ["merge-base", "--is-ancestor", preflight.package_git_commit, head.stdout]);
  if (ancestor.status !== 0) errors.push("PREFLIGHT package commit is not an ancestor of current HEAD");
  const frozenNames = [...FROZEN_FILES, "FROZEN-HASHES.json"];
  for (const name of frozenNames) {
    const current = gitRun(repo, ["rev-parse", `${head.stdout}:${preflight.package_relative_path}/${name}`]);
    if (current.status !== 0 || current.stdout !== preflight.package_git_blobs?.[name]) {
      errors.push(`${name}: current HEAD blob does not descend unchanged from PREFLIGHT`);
    }
  }
  return errors;
}

export function validatePreflight(root, preflight) {
  const errors = [];
  const frozen = validateFrozenArtifacts(root);
  errors.push(...frozen.errors);
  if (!sameKeySet(preflight, REQUIRED_PREFLIGHT_KEYS)) errors.push("PREFLIGHT field set mismatch");
  if (preflight?.schema_version !== "claude-opus-route-purity-preflight-v1" || preflight?.status !== "GO") errors.push("PREFLIGHT identity/status mismatch");
  if (preflight?.route_check_performed !== true) errors.push("PREFLIGHT route check was not performed");
  if (preflight?.claude_version !== EXPECTED_CLAUDE_VERSION) errors.push("PREFLIGHT Claude version mismatch");
  if (preflight?.expected_claude_version !== EXPECTED_CLAUDE_VERSION) errors.push("PREFLIGHT expected Claude version mismatch");
  if (preflight?.frozen_hash_manifest_sha256 !== sha256File(path.join(root, "FROZEN-HASHES.json"))) errors.push("PREFLIGHT frozen manifest hash mismatch");
  if (!sameJson(preflight?.required_environment, REQUIRED_ENVIRONMENT)) errors.push("PREFLIGHT required environment mismatch");
  if (!preflight?.package_git_commit || !/^[0-9a-f]{40}$/u.test(preflight.package_git_commit)) errors.push("PREFLIGHT package Git commit is missing");
  if (preflight?.head_commit_at_preflight !== preflight?.package_git_commit) errors.push("PREFLIGHT HEAD/package commit mismatch");
  if (preflight?.package_relative_path !== packageRelativePath(root)) errors.push("PREFLIGHT package relative path mismatch");
  if (!/^[0-9a-f]{40}$/u.test(preflight?.package_git_tree_oid ?? "")) errors.push("PREFLIGHT package Git tree is missing");
  if (!sameKeySet(preflight?.package_git_blobs, [...FROZEN_FILES, "FROZEN-HASHES.json"])) errors.push("PREFLIGHT package Git blob set mismatch");
  if (preflight?.public_bundle_file_count !== 3 || preflight?.synthetic_items !== 3 || preflight?.real_experiment_samples !== 0) errors.push("PREFLIGHT synthetic bundle counts mismatch");
  if (preflight?.executor_fixture_sha256 !== "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7") errors.push("PREFLIGHT executor fixture hash mismatch");
  if (preflight?.fixture_test_status !== "PASS") errors.push("PREFLIGHT fixture status mismatch");
  if (preflight?.sandbox_smoke_status !== "PASS" || preflight?.sandbox_host_home_hidden !== true || preflight?.sandbox_runtime_private_writable !== true) errors.push("PREFLIGHT sandbox smoke/policy mismatch");
  if (preflight?.sandbox_auth_policy !== SANDBOX_AUTH_POLICY || preflight?.sandbox_auth_method !== "claude.ai" || preflight?.sandbox_api_provider !== EXPECTED_PROVIDER) errors.push("PREFLIGHT sandbox auth policy mismatch");
  if (!Array.isArray(preflight?.errors) || preflight.errors.length !== 0) errors.push("PREFLIGHT errors must be an empty array");
  const bwrap = spawnSync("bwrap", ["--version"], {encoding: "utf8"});
  if (preflight?.bwrap_version !== EXPECTED_BWRAP_VERSION) errors.push("PREFLIGHT frozen bwrap version mismatch");
  if (bwrap.status !== 0 || bwrap.stdout.trim() !== EXPECTED_BWRAP_VERSION) errors.push("current bwrap version drift");
  const materials = resolveClaudeRuntimeMaterials();
  errors.push(...materials.errors.map(error => `runtime material: ${error}`));
  if (materials.claudeBinarySha256 !== preflight?.claude_binary_sha256) errors.push("PREFLIGHT Claude binary hash mismatch");
  if (/^[0-9a-f]{40}$/u.test(preflight?.package_git_commit ?? "")) {
    const packageLineage = gitPackageLineage(root, preflight.package_git_commit);
    errors.push(...packageLineage.errors.map(error => `package lineage: ${error}`));
    if (packageLineage.tree !== preflight.package_git_tree_oid) errors.push("PREFLIGHT package Git tree mismatch");
    if (!sameJson(packageLineage.blobs, preflight.package_git_blobs)) errors.push("PREFLIGHT package Git blobs mismatch");
    errors.push(...validateCurrentHeadLineage(root, preflight));
    const repo = repositoryForPackage(root);
    const relative = packageRelativePath(root);
    const headPreflight = gitRun(repo, ["rev-parse", `HEAD:${relative}/PREFLIGHT.json`]);
    const workingPreflight = gitRun(repo, ["hash-object", path.join(root, "PREFLIGHT.json")]);
    if (headPreflight.status !== 0 || workingPreflight.status !== 0 || headPreflight.stdout !== workingPreflight.stdout) {
      errors.push("PREFLIGHT.json is not committed unchanged at current HEAD");
    }
  }
  return errors;
}
