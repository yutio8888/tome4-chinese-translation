import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  EXPERIMENT,
  EXPECTED_BWRAP_VERSION,
  REQUIRED_ENVIRONMENT,
  ROUTE_SLUG,
  SANDBOX_AUTH_POLICY,
  assert,
  assertOrdinaryFile,
  createPublicBundle,
  createSandboxRuntime,
  invocationPlan,
  minimalClaudeEnvironment,
  parseAttempt,
  readJson,
  removePublicBundle,
  removeSandboxRuntime,
  requestBytes,
  reserveAttemptDirectory,
  resolveClaudeRuntimeMaterials,
  sandboxSmoke,
  sha256Bytes,
  sha256File,
  validateEnvironment,
  validatePreflight,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
assert(argv.length === 2 && argv[0] === "--attempt", "usage: node run.mjs --attempt N");
const attempt = parseAttempt(argv[1]);
const preflightPath = path.join(here, "PREFLIGHT.json");
assertOrdinaryFile(preflightPath, "PREFLIGHT.json");
const preflight = readJson(preflightPath);
const preflightErrors = validatePreflight(here, preflight);
assert(preflightErrors.length === 0, `PREFLIGHT invalid: ${preflightErrors.join("; ")}`);

const environment = minimalClaudeEnvironment();
const environmentErrors = validateEnvironment(environment);
assert(environmentErrors.length === 0, `required environment invalid: ${environmentErrors.join("; ")}`);
const bwrap = spawnSync("bwrap", ["--version"], {encoding: "utf8"});
assert(bwrap.status === 0 && bwrap.stdout.trim() === EXPECTED_BWRAP_VERSION, `bubblewrap version drift: ${bwrap.stdout?.trim() || "<unavailable>"}`);
const materials = resolveClaudeRuntimeMaterials();
assert(materials.errors.length === 0, `runtime material invalid: ${materials.errors.join("; ")}`);
assert(materials.claudeBinarySha256 === preflight.claude_binary_sha256, "Claude binary drift after PREFLIGHT");

let bundleDir = null;
let runtimeDir = null;
let attemptDir = null;
try {
  runtimeDir = createSandboxRuntime(materials.authFile, os.tmpdir());
  const smoke = sandboxSmoke({runtimeDirectory: runtimeDir, claudeBinary: materials.claudeBinary, environment});
  assert(smoke.errors.length === 0, `sandbox smoke drift: ${smoke.errors.join("; ")}`);
  assert(smoke.version === preflight.claude_version && smoke.authMethod === preflight.sandbox_auth_method && smoke.apiProvider === preflight.sandbox_api_provider, "sandbox route drift after PREFLIGHT");
  bundleDir = createPublicBundle(here);
  const request = requestBytes(bundleDir);
  const plan = invocationPlan(bundleDir, request, runtimeDir, materials.claudeBinary);
  attemptDir = reserveAttemptDirectory(here, attempt);
  const startedAt = new Date();
  const started = Date.now();
  const result = spawnSync(plan.command, plan.args, {
    cwd: bundleDir,
    env: environment,
    encoding: null,
    maxBuffer: 32 * 1024 * 1024,
    timeout: 10 * 60 * 1000
  });
  const stdout = Buffer.isBuffer(result.stdout) ? result.stdout : Buffer.from(result.stdout ?? "");
  const stderr = Buffer.isBuffer(result.stderr) ? result.stderr : Buffer.from(result.stderr ?? "");
  writeNewFile(path.join(attemptDir, "RAW.stdout"), stdout);
  writeNewFile(path.join(attemptDir, "RAW.stderr"), stderr);
  const call = {
    schema_version: "claude-opus-route-purity-call-v1",
    experiment: EXPERIMENT,
    route: ROUTE_SLUG,
    attempt,
    started_at_utc: startedAt.toISOString(),
    duration_seconds: (Date.now() - started) / 1000,
    command: plan.command,
    arguments: plan.display_args,
    environment_policy: "fixed sanitized environment; entire host HOME masked; private ephemeral runtime; no environment values, credentials or local paths recorded",
    required_environment_names: Object.keys(REQUIRED_ENVIRONMENT).sort(),
    sandbox_auth_policy: SANDBOX_AUTH_POLICY,
    package_git_commit: preflight.package_git_commit,
    package_git_tree_oid: preflight.package_git_tree_oid,
    package_git_blobs: preflight.package_git_blobs,
    bundle_files: ["PROMPT.md", "INPUT.json", "SCHEMA.json"],
    request_sha256: sha256Bytes(request),
    input_sha256: sha256File(path.join(here, "INPUT.json")),
    prompt_sha256: sha256File(path.join(here, "PROMPT.md")),
    schema_sha256: sha256File(path.join(here, "SCHEMA.json")),
    frozen_hash_manifest_sha256: sha256File(path.join(here, "FROZEN-HASHES.json")),
    preflight_sha256: sha256File(preflightPath),
    claude_binary_sha256: materials.claudeBinarySha256,
    raw_stdout: "RAW.stdout",
    raw_stdout_sha256: sha256Bytes(stdout),
    raw_stderr: "RAW.stderr",
    raw_stderr_sha256: sha256Bytes(stderr),
    exit_status: result.status,
    signal: result.signal ?? null,
    spawn_error: result.error ? String(result.error) : null,
    transport_success: !result.error && result.status === 0
  };
  writeNewFile(path.join(attemptDir, "CALL.json"), `${JSON.stringify(call, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({...call, arguments: undefined, package_git_blobs: "[FROZEN_BLOB_MAP]"}, null, 2)}\n`);
  if (!call.transport_success) process.exitCode = 2;
} finally {
  if (bundleDir && fs.existsSync(bundleDir)) removePublicBundle(bundleDir);
  if (runtimeDir && fs.existsSync(runtimeDir)) removeSandboxRuntime(runtimeDir);
}
