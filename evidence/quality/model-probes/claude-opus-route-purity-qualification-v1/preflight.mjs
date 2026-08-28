import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  EXPECTED_CLAUDE_VERSION,
  EXPECTED_BWRAP_VERSION,
  EXPECTED_PROVIDER,
  REQUIRED_ENVIRONMENT,
  SANDBOX_AUTH_POLICY,
  createPublicBundle,
  createSandboxRuntime,
  gitPackageLineage,
  invocationPlan,
  minimalClaudeEnvironment,
  packageRelativePath,
  removePublicBundle,
  removeSandboxRuntime,
  requestBytes,
  resolveClaudeRuntimeMaterials,
  sandboxSmoke,
  scanOutboundBuffers,
  sha256File,
  validateEnvironment,
  validateFrozenArtifacts,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const argv = process.argv.slice(2);
const write = argv.includes("--write");
if (argv.some(argument => argument !== "--write")) throw new Error("usage: node preflight.mjs [--write]");
const errors = [];
const frozen = validateFrozenArtifacts(here);
errors.push(...frozen.errors);

const environment = minimalClaudeEnvironment();
errors.push(...validateEnvironment(environment));
const materials = resolveClaudeRuntimeMaterials();
errors.push(...materials.errors.map(error => `runtime material: ${error}`));
const bwrap = spawnSync("bwrap", ["--version"], {encoding: "utf8"});
const bwrapVersion = bwrap.status === 0 ? bwrap.stdout.trim() : null;
if (bwrapVersion !== EXPECTED_BWRAP_VERSION) errors.push(`bubblewrap version drift: ${bwrapVersion ?? "<unavailable>"}`);

errors.push(...scanOutboundBuffers([
  {label: "request", bytes: requestBytes(here)},
  {label: "schema", bytes: fs.readFileSync(path.join(here, "SCHEMA.json"))}
]).map(error => `outbound leak: ${error}`));

let bundle = null;
let runtime = null;
let smoke = {version: null, authMethod: null, apiProvider: null, hostHomeHidden: false, runtimeWritable: false, errors: ["sandbox smoke was not run"]};
try {
  bundle = createPublicBundle(here, os.tmpdir());
  const expectedFiles = ["INPUT.json", "PROMPT.md", "SCHEMA.json"];
  if (JSON.stringify(fs.readdirSync(bundle).sort()) !== JSON.stringify(expectedFiles)) errors.push("synthetic public bundle file set mismatch");
  if (materials.errors.length === 0 && bwrapVersion) {
    runtime = createSandboxRuntime(materials.authFile, os.tmpdir());
    smoke = sandboxSmoke({runtimeDirectory: runtime, claudeBinary: materials.claudeBinary, environment});
    errors.push(...smoke.errors);
    const plan = invocationPlan(bundle, requestBytes(bundle), runtime, materials.claudeBinary);
    if (plan.command !== "bwrap") errors.push("OS sandbox wrapper missing");
    if (plan.display_args.some(argument => /(?:\/home\/|[A-Za-z]:\\Users\\|sk-ant-)/u.test(argument))) errors.push("displayed call leaks a credential or local absolute path");
  }
} finally {
  if (bundle && fs.existsSync(bundle)) removePublicBundle(bundle);
  if (runtime && fs.existsSync(runtime)) removeSandboxRuntime(runtime);
}

const fixtureTest = spawnSync(process.execPath, [path.join(here, "test-parser.mjs")], {cwd: repo, encoding: "utf8"});
if (fixtureTest.status !== 0) errors.push(`parser fixtures failed: ${(fixtureTest.stderr || fixtureTest.stdout).trim()}`);
const executor = path.resolve(here, "../qwen3-8-27b-agent-roles/executor-fixture.lua");
const executorHash = sha256File(executor);
if (executorHash !== "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7") errors.push("executor fixture baseline drift");
const diffCheck = spawnSync("git", ["diff", "--check"], {cwd: repo, encoding: "utf8"});
if (diffCheck.status !== 0) errors.push(`git diff --check failed: ${diffCheck.stdout || diffCheck.stderr}`);
const packageStatus = spawnSync("git", ["status", "--short", "--untracked-files=all", "--", path.relative(repo, here)], {cwd: repo, encoding: "utf8"});
if (packageStatus.status !== 0 || packageStatus.stdout.trim()) errors.push("frozen package is not fully committed");
const lineage = gitPackageLineage(here);
errors.push(...lineage.errors.map(error => `package lineage: ${error}`));
if (fs.existsSync(path.join(here, "PREFLIGHT.json"))) errors.push("PREFLIGHT.json already exists; preflight records are immutable");
if (fs.existsSync(path.join(here, "attempts"))) errors.push("attempt artifacts already exist before preflight");

const report = {
  schema_version: "claude-opus-route-purity-preflight-v1",
  status: errors.length === 0 ? "GO" : "NO_GO",
  route_check_performed: true,
  package_git_commit: lineage.commit,
  head_commit_at_preflight: lineage.commit,
  package_relative_path: packageRelativePath(here),
  package_git_tree_oid: lineage.tree,
  package_git_blobs: lineage.blobs,
  claude_version: smoke.version,
  expected_claude_version: EXPECTED_CLAUDE_VERSION,
  claude_binary_sha256: materials.claudeBinarySha256,
  bwrap_version: bwrapVersion,
  required_environment: REQUIRED_ENVIRONMENT,
  frozen_hash_manifest_sha256: sha256File(path.join(here, "FROZEN-HASHES.json")),
  public_bundle_file_count: 3,
  synthetic_items: 3,
  real_experiment_samples: 0,
  executor_fixture_sha256: executorHash,
  fixture_test_status: fixtureTest.status === 0 ? "PASS" : "FAIL",
  sandbox_smoke_status: smoke.errors.length === 0 ? "PASS" : "FAIL",
  sandbox_host_home_hidden: smoke.hostHomeHidden,
  sandbox_runtime_private_writable: smoke.runtimeWritable,
  sandbox_auth_policy: SANDBOX_AUTH_POLICY,
  sandbox_auth_method: smoke.authMethod,
  sandbox_api_provider: smoke.apiProvider === EXPECTED_PROVIDER ? smoke.apiProvider : null,
  errors
};
if (write) {
  if (errors.length) throw new Error(`refusing to write NO_GO preflight: ${errors.join("; ")}`);
  writeNewFile(path.join(here, "PREFLIGHT.json"), `${JSON.stringify(report, null, 2)}\n`);
}
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
if (errors.length) process.exitCode = 2;
