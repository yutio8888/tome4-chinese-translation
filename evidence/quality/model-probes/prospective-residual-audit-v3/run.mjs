import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  assert,
  assertExactBundle,
  assertRouteRunnable,
  createPublicBundle,
  invocationPlan,
  minimalEnvironment,
  parseAttempt,
  readJson,
  requestBytes,
  reserveAttemptDirectory,
  sha256Bytes,
  sha256File,
  validatePublicArtifacts,
  validatePreflightRecord,
  validateReviewContract,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const routeKey = argv[0];
const attemptIndex = argv.indexOf("--attempt");
assert(argv.length === 3 && attemptIndex === 1, "usage: node run.mjs codex|opus|glm|gemini --attempt N");
const route = assertRouteRunnable(routeKey);
const attempt = parseAttempt(argv[attemptIndex + 1]);
const publicErrors = validatePublicArtifacts(here);
assert(publicErrors.length === 0, `public artifact preflight failed: ${publicErrors.join("; ")}`);
const contractCheck = validateReviewContract(here);
assert(contractCheck.errors.length === 0, `review contract preflight failed: ${contractCheck.errors.join("; ")}`);
const preflightPath = path.join(here, "PREFLIGHT.json");
assert(fs.existsSync(preflightPath), "PREFLIGHT.json missing; run committed-package preflight before inference");
const preflight = readJson(preflightPath);
const head = spawnSync("git", ["rev-parse", "HEAD"], {cwd: path.resolve(here, "../../../.."), encoding: "utf8"});
assert(head.status === 0, "cannot resolve current package Git commit");
const preflightErrors = validatePreflightRecord({preflight, contractSha256: sha256File(path.join(here, "REVIEW-CONTRACT.json")), packageGitCommit: head.stdout.trim()});
assert(preflightErrors.length === 0, `PREFLIGHT.json invalid: ${preflightErrors.join("; ")}`);

const routeCommand = {codex: "codex", claude: "claude", pi: "pi", agy: "agy"}[route.kind];
const version = spawnSync(routeCommand, ["--version"], {
  cwd: "/tmp",
  encoding: "utf8",
  env: minimalEnvironment(route.kind, "/tmp")
});
assert(version.status === 0, `${route.kind} --version failed`);
const expectedVersion = {codex: "codex-cli 0.150.1", claude: "2.1.247 (Claude Code)", pi: "0.84.3", agy: "1.1.22"}[route.kind];
assert(version.stdout.trim() === expectedVersion, `${route.kind} version drift: ${version.stdout.trim()}`);

const attemptDir = reserveAttemptDirectory(here, route, attempt);
let bundleDir;
try {
  bundleDir = createPublicBundle(here);
  assertExactBundle(bundleDir);
  const request = requestBytes(bundleDir);
  const plan = invocationPlan(route, bundleDir, request);
  const startedAt = new Date();
  const started = Date.now();
  const result = spawnSync(plan.command, plan.args, {
    cwd: bundleDir,
    env: minimalEnvironment(route.kind, "/tmp"),
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
    route: route.slug,
    evidence_tier: route.evidenceTier,
    attempt,
    started_at_utc: startedAt.toISOString(),
    duration_seconds: (Date.now() - started) / 1000,
    command: plan.command,
    arguments: plan.display_args,
    environment_policy: "explicit-minimal-whitelist-v1; values and home/config paths are not recorded",
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
  if (bundleDir && path.basename(bundleDir).startsWith("residual-audit-v3-") && fs.existsSync(bundleDir)) fs.rmSync(bundleDir, {recursive: true, force: false});
}
