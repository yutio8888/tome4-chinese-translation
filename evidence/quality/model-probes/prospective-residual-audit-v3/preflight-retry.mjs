import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  EXPECTED_MODEL_AVAILABILITY,
  EXPECTED_ROUTE_VERSIONS,
  createPublicBundle,
  createRouteRuntime,
  readJson,
  removeRouteRuntime,
  routeFor,
  runtimeEnvironment,
  sha256File,
  validateHarnessErrataArtifacts,
  validatePublicArtifacts,
  validateReviewContract,
  wrapInOsSandbox,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const argv = process.argv.slice(2);
const write = argv.includes("--write");
if (argv.some(arg => arg !== "--write")) throw new Error("usage: node preflight-retry.mjs [--write]");
const errors = [...validatePublicArtifacts(here)];
const contractCheck = validateReviewContract(here);
errors.push(...contractCheck.errors);
const errataPath = path.join(here, "HARNESS-ERRATA-1.json");
const errata = readJson(errataPath);
errors.push(...validateHarnessErrataArtifacts(here, errata));
const attemptRoot = path.join(here, "attempts");
const actualAttemptFiles = fs.existsSync(attemptRoot)
  ? fs.readdirSync(attemptRoot, {recursive: true}).map(name => path.join("attempts", name)).filter(name => fs.lstatSync(path.join(here, name)).isFile()).sort()
  : [];
const expectedAttemptFiles = (errata.preserved_artifacts ?? []).map(binding => binding.logical_path).filter(name => name.startsWith("attempts/")).sort();
if (JSON.stringify(actualAttemptFiles) !== JSON.stringify(expectedAttemptFiles)) errors.push("pre-retry attempt artifact set is not exactly frozen");
for (const target of [
  path.join(attemptRoot, routeFor("codex").slug, "attempt-002"),
  path.join(attemptRoot, routeFor("glm").slug, "attempt-003")
]) if (fs.existsSync(target)) errors.push(`${path.relative(here, target)}: retry target already exists`);

for (const script of ["test-scorer.mjs", "test-runner.mjs"]) {
  const result = spawnSync(process.execPath, [path.join(here, script)], {cwd: repo, encoding: "utf8"});
  if (result.status !== 0) errors.push(`${script} failed: ${(result.stderr || result.stdout).trim()}`);
}
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "residual-retry-preflight-"));
try {
  const bundle = createPublicBundle(here, temp);
  for (const [key, command, expected] of [
    ["codex", "codex", EXPECTED_ROUTE_VERSIONS.codex],
    ["glm", "pi", EXPECTED_ROUTE_VERSIONS.pi]
  ]) {
    const route = routeFor(key);
    const runtime = createRouteRuntime(route, temp);
    try {
      const args = command === "pi" ? ["--list-models", "glm-5.3-flash"] : ["--version"];
      const plan = wrapInOsSandbox({bundleDirectory: bundle, runtimeDirectory: runtime, maskUserHome: true, command, args, displayArgs: ["[RETRY_ROUTE_SMOKE]"]});
      const result = spawnSync(plan.command, plan.args, {cwd: "/tmp", encoding: "utf8", env: runtimeEnvironment(route.kind)});
      if (command === "codex" && (result.status !== 0 || result.stdout.trim() !== expected)) errors.push("Codex retry runtime smoke failed");
      if (command === "pi" && (result.status !== 0 || !/zai-standard-cn\s+glm-5\.3-flash/u.test(result.stdout))) errors.push("Pi retry runtime/model smoke failed");
    } finally { removeRouteRuntime(runtime); }
  }
} finally { fs.rmSync(temp, {recursive: true}); }

const executor = path.resolve(here, "../qwen3-8-27b-agent-roles/executor-fixture.lua");
const executorHash = sha256File(executor);
if (executorHash !== "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7") errors.push("executor fixture baseline drift");
const diff = spawnSync("git", ["diff", "--check"], {cwd: repo, encoding: "utf8"});
if (diff.status !== 0) errors.push(`git diff --check failed: ${diff.stdout || diff.stderr}`);
const packageStatus = spawnSync("git", ["status", "--short", "--untracked-files=all", "--", path.relative(repo, here)], {cwd: repo, encoding: "utf8"});
if (packageStatus.status !== 0 || packageStatus.stdout.trim()) errors.push("retry package is not fully committed");
const head = spawnSync("git", ["rev-parse", "HEAD"], {cwd: repo, encoding: "utf8"});
const packageGitCommit = head.status === 0 ? head.stdout.trim() : null;
if (!packageGitCommit) errors.push("cannot resolve retry package Git commit");

const routeVersions = {};
for (const [command, expected] of Object.entries(EXPECTED_ROUTE_VERSIONS)) {
  const result = spawnSync(command, ["--version"], {cwd: "/tmp", encoding: "utf8", env: {...process.env, PI_SKIP_VERSION_CHECK: "1"}});
  routeVersions[command] = result.stdout?.trim() ?? null;
  if (result.status !== 0 || routeVersions[command] !== expected) errors.push(`${command} version drift`);
}
const modelAvailability = {};
const codexModels = spawnSync("codex", ["debug", "models", "--bundled"], {cwd: "/tmp", encoding: "utf8", maxBuffer: 32 * 1024 * 1024});
modelAvailability.codex_gpt_5_6_sol = codexModels.status === 0 && /"slug":"gpt-5\.6-sol"/u.test(codexModels.stdout);
const piModels = spawnSync("pi", ["--list-models", "glm-5.3-flash"], {cwd: "/tmp", encoding: "utf8", env: {...process.env, PI_SKIP_VERSION_CHECK: "1"}});
modelAvailability.pi_zai_cn_glm_5_3_flash = piModels.status === 0 && /zai-standard-cn\s+glm-5\.3-flash/u.test(piModels.stdout);
const agyModels = spawnSync("agy", ["models"], {cwd: "/tmp", encoding: "utf8"});
modelAvailability.agy_gemini_3_7_flash_high = agyModels.status === 0 && /^gemini-3\.7-flash-high\s/mu.test(agyModels.stdout);
if (JSON.stringify(modelAvailability) !== JSON.stringify(EXPECTED_MODEL_AVAILABILITY)) errors.push("retry model availability drift");

const report = {
  schema_version: "prospective-residual-retry-preflight-v3-1",
  status: errors.length ? "NO_GO" : "GO",
  route_check_performed: true,
  package_git_commit: packageGitCommit,
  review_contract_sha256: sha256File(path.join(here, "REVIEW-CONTRACT.json")),
  harness_errata_sha256: sha256File(errataPath),
  executor_fixture_sha256: executorHash,
  allowed_route_attempts: {codex: 2, glm: 3},
  prohibited_reruns: {opus: 1, gemini: 1},
  route_versions: routeVersions,
  model_availability: modelAvailability,
  errors
};
if (write) writeNewFile(path.join(here, "PREFLIGHT-RETRY-1.json"), `${JSON.stringify(report, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
if (errors.length) process.exitCode = 2;
