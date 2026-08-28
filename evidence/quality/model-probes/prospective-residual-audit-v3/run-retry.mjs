import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  assert,
  assertExactBundle,
  assertRouteRunnable,
  createPublicBundle,
  createRouteRuntime,
  invocationPlan,
  parseAttempt,
  readJson,
  removeRouteRuntime,
  requestBytes,
  reserveAttemptDirectory,
  runtimeEnvironment,
  sha256Bytes,
  sha256File,
  validatePublicArtifacts,
  validateHarnessErrataArtifacts,
  validateRetryPreflightRecord,
  validateReviewContract,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const argv = process.argv.slice(2);
const routeKey = argv[0];
const attemptIndex = argv.indexOf("--attempt");
assert(argv.length === 3 && attemptIndex === 1, "usage: node run-retry.mjs codex --attempt 2 | glm --attempt 3");
const route = assertRouteRunnable(routeKey);
const attempt = parseAttempt(argv[attemptIndex + 1]);
const allowed = {codex: 2, glm: 3};
assert(allowed[routeKey] === attempt, `${routeKey}: retry attempt is not frozen/allowed`);
assert(["codex", "pi"].includes(route.kind), `${route.slug}: retry runtime is not defined`);

const publicErrors = validatePublicArtifacts(here);
assert(publicErrors.length === 0, `public artifact retry preflight failed: ${publicErrors.join("; ")}`);
const contractCheck = validateReviewContract(here);
assert(contractCheck.errors.length === 0, `review contract retry preflight failed: ${contractCheck.errors.join("; ")}`);
const preflightPath = path.join(here, "PREFLIGHT-RETRY-1.json");
const errataPath = path.join(here, "HARNESS-ERRATA-1.json");
assert(fs.existsSync(preflightPath), "PREFLIGHT-RETRY-1.json missing; run committed retry preflight before inference");
const preflight = readJson(preflightPath);
const errata = readJson(errataPath);
const errataArtifactErrors = validateHarnessErrataArtifacts(here, errata);
assert(errataArtifactErrors.length === 0, `preserved artifact validation failed: ${errataArtifactErrors.join("; ")}`);
const head = spawnSync("git", ["rev-parse", "HEAD"], {cwd: repo, encoding: "utf8"});
assert(head.status === 0, "cannot resolve current retry package Git commit");
const preflightErrors = validateRetryPreflightRecord({
  preflight,
  contractSha256: sha256File(path.join(here, "REVIEW-CONTRACT.json")),
  errataSha256: sha256File(errataPath),
  packageGitCommit: head.stdout.trim()
});
assert(preflightErrors.length === 0, `PREFLIGHT-RETRY-1.json invalid: ${preflightErrors.join("; ")}`);

const routeCommand = {codex: "codex", pi: "pi"}[route.kind];
const version = spawnSync(routeCommand, ["--version"], {cwd: "/tmp", encoding: "utf8", env: runtimeEnvironment(route.kind)});
const expectedVersion = {codex: "codex-cli 0.150.1", pi: "0.84.3"}[route.kind];
assert(version.status === 0 && version.stdout.trim() === expectedVersion, `${route.kind} version drift: ${version.stdout.trim()}`);

let attemptDir;
let bundleDir;
let runtimeDir;
try {
  bundleDir = createPublicBundle(here);
  runtimeDir = createRouteRuntime(route);
  assertExactBundle(bundleDir);
  attemptDir = reserveAttemptDirectory(here, route, attempt);
  const request = requestBytes(bundleDir);
  const plan = invocationPlan(route, bundleDir, request, {runtimeDirectory: runtimeDir, maskUserHome: true});
  const startedAt = new Date();
  const started = Date.now();
  const result = spawnSync(plan.command, plan.args, {
    cwd: bundleDir,
    env: runtimeEnvironment(route.kind),
    encoding: null,
    maxBuffer: 96 * 1024 * 1024,
    timeout: 30 * 60 * 1000
  });
  const stdout = Buffer.isBuffer(result.stdout) ? result.stdout : Buffer.from(result.stdout ?? "");
  const stderr = Buffer.isBuffer(result.stderr) ? result.stderr : Buffer.from(result.stderr ?? "");
  const stdoutPath = path.join(attemptDir, "RAW.stdout");
  const stderrPath = path.join(attemptDir, "RAW.stderr");
  writeNewFile(stdoutPath, stdout);
  writeNewFile(stderrPath, stderr);
  const call = {
    schema_version: "prospective-residual-call-v3",
    experiment: "prospective-residual-audit-v3",
    harness_revision: "retry-1",
    retry_preflight: "PREFLIGHT-RETRY-1.json",
    route: route.slug,
    evidence_tier: route.evidenceTier,
    attempt,
    started_at_utc: startedAt.toISOString(),
    duration_seconds: (Date.now() - started) / 1000,
    command: plan.command,
    arguments: plan.display_args,
    environment_policy: "explicit-minimal-whitelist-v1; private writable route runtime; values, credentials and host paths are not recorded",
    runtime_policy: "entire user home masked; only minimal per-route authentication/config runtime writable-bound at a generic path; runtime deleted after call",
    bundle_files: ["PROMPT.md", "PUBLIC-HOLDOUT.json", "REVIEWER-SCHEMA.json", "CODEX-TRANSPORT-SCHEMA.json"],
    request_sha256: sha256Bytes(request),
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
  process.stdout.write(`${JSON.stringify({...call, arguments: undefined}, null, 2)}\n`);
  if (!call.transport_success) process.exitCode = 2;
} finally {
  if (runtimeDir && fs.existsSync(runtimeDir)) removeRouteRuntime(runtimeDir);
  if (bundleDir && path.basename(bundleDir).startsWith("residual-audit-v3-") && fs.existsSync(bundleDir)) fs.rmSync(bundleDir, {recursive: true, force: false});
}
