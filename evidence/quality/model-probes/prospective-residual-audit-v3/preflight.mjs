import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  EXPECTED_ROUTE_VERSIONS,
  createPublicBundle,
  readJson,
  requestBytes,
  scanOutboundBuffers,
  sha256File,
  validatePublicArtifacts,
  validateReviewContract,
  wrapInOsSandbox,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const argv = process.argv.slice(2);
const write = argv.includes("--write");
const routeCheck = true;
if (argv.some(arg => !["--write", "--route-check"].includes(arg))) throw new Error("usage: node preflight.mjs [--route-check] [--write]");
const errors = [...validatePublicArtifacts(here)];
const contractCheck = validateReviewContract(here);
errors.push(...contractCheck.errors);
const protocolHash = sha256File(path.join(here, "SOURCE-AUDIT-PROTOCOL.json"));
if (protocolHash !== "95d290e728956c0ac9efeeaa05164ba53d37e3d2a78790c7e3cf82b1b078c35b") errors.push("source audit protocol hash drift");
const leakErrors = scanOutboundBuffers([
  {label: "request", bytes: requestBytes(here)},
  {label: "schema", bytes: fs.readFileSync(path.join(here, "REVIEWER-SCHEMA.json"))},
  {label: "Codex transport schema", bytes: fs.readFileSync(path.join(here, "CODEX-TRANSPORT-SCHEMA.json"))}
]);
errors.push(...leakErrors.map(error => `outbound leak: ${error}`));

const temp = fs.mkdtempSync(path.join(os.tmpdir(), "residual-preflight-"));
try {
  const rebuilt = path.join(temp, "PUBLIC-HOLDOUT.json");
  const build = spawnSync(process.execPath, [path.join(here, "build-public-holdout.mjs"), "--out", rebuilt], {cwd: repo, encoding: "utf8"});
  if (build.status !== 0 || sha256File(rebuilt) !== sha256File(path.join(here, "PUBLIC-HOLDOUT.json"))) errors.push("public holdout byte-identical rebuild failed");
  const bundle = createPublicBundle(here, temp);
  if (fs.readdirSync(bundle).length !== 4) errors.push("public bundle does not contain exactly four files");
  const probePlan = wrapInOsSandbox({
    bundleDirectory: bundle,
    command: "/bin/sh",
    args: ["-c", "test \"$(pwd)\" = /mnt && test \"$(find /mnt -maxdepth 1 -type f | wc -l)\" -eq 4 && test ! -e /home/yun/research/tome4-agent-eval/evidence/quality/model-probes/prospective-residual-audit-v3/SEALED-REFERENCE.json && printf SANDBOX_OK"],
    displayArgs: ["[OFFLINE_ISOLATION_PROBE]"]
  });
  const probe = spawnSync(probePlan.command, probePlan.args, {cwd: "/tmp", encoding: "utf8"});
  if (probe.status !== 0 || probe.stdout !== "SANDBOX_OK") errors.push("OS isolation probe failed");
} finally { fs.rmSync(temp, {recursive: true}); }

for (const script of ["test-scorer.mjs", "test-runner.mjs"]) {
  const result = spawnSync(process.execPath, [path.join(here, script)], {cwd: repo, encoding: "utf8"});
  if (result.status !== 0) errors.push(`${script} failed: ${(result.stderr || result.stdout).trim()}`);
}
const executor = path.resolve(here, "../qwen3-8-27b-agent-roles/executor-fixture.lua");
const executorHash = sha256File(executor);
if (executorHash !== "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7") errors.push("executor fixture baseline drift");
const diff = spawnSync("git", ["diff", "--check"], {cwd: repo, encoding: "utf8"});
if (diff.status !== 0) errors.push(`git diff --check failed: ${diff.stdout || diff.stderr}`);
const packageStatus = spawnSync("git", ["status", "--short", "--untracked-files=all", "--", path.relative(repo, here)], {cwd: repo, encoding: "utf8"});
if (packageStatus.status !== 0 || packageStatus.stdout.trim()) errors.push("pre-inference package is not fully committed");
const head = spawnSync("git", ["rev-parse", "HEAD"], {cwd: repo, encoding: "utf8"});
const packageGitCommit = head.status === 0 ? head.stdout.trim() : null;
if (!packageGitCommit) errors.push("cannot resolve package Git commit");
const routeVersions = {};
const modelAvailability = {};
if (routeCheck) {
  for (const [command, expected] of Object.entries(EXPECTED_ROUTE_VERSIONS)) {
    const result = spawnSync(command, ["--version"], {cwd: "/tmp", encoding: "utf8", env: {...process.env, PI_SKIP_VERSION_CHECK: "1"}});
    routeVersions[command] = result.stdout?.trim() ?? null;
    if (result.status !== 0 || routeVersions[command] !== expected) errors.push(`${command} version drift`);
  }
  const codexModels = spawnSync("codex", ["debug", "models", "--bundled"], {cwd: "/tmp", encoding: "utf8", maxBuffer: 32 * 1024 * 1024});
  modelAvailability.codex_gpt_5_6_sol = codexModels.status === 0 && /"slug":"gpt-5\.6-sol"/u.test(codexModels.stdout);
  const piModels = spawnSync("pi", ["--list-models", "glm-5.3-flash"], {cwd: "/tmp", encoding: "utf8", env: {...process.env, PI_SKIP_VERSION_CHECK: "1"}});
  modelAvailability.pi_zai_cn_glm_5_3_flash = piModels.status === 0 && /zai-standard-cn\s+glm-5\.3-flash/u.test(piModels.stdout);
  const agyModels = spawnSync("agy", ["models"], {cwd: "/tmp", encoding: "utf8"});
  modelAvailability.agy_gemini_3_7_flash_high = agyModels.status === 0 && /^gemini-3\.7-flash-high\s/mu.test(agyModels.stdout);
  for (const [name, available] of Object.entries(modelAvailability)) if (!available) errors.push(`${name}: model unavailable`);
}
const generated = fs.existsSync(path.join(here, "attempts")) ? fs.readdirSync(path.join(here, "attempts"), {recursive: true}).filter(name => /(?:RAW|CANDIDATE|CALL)/u.test(name)) : [];
if (generated.length) errors.push("pre-inference attempt artifacts already exist");
const report = {
  schema_version: "prospective-residual-preflight-v3",
  status: errors.length ? "NO_GO" : "GO",
  route_check_performed: routeCheck,
  package_git_commit: packageGitCommit,
  review_contract_sha256: sha256File(path.join(here, "REVIEW-CONTRACT.json")),
  source_audit_protocol_sha256: protocolHash,
  executor_fixture_sha256: executorHash,
  public_bundle_file_count: 4,
  executable_routes: ["codex-gpt-5.6-sol-high", "claude-opus-5-medium-no-advisor", "pi-zai-cn-glm-5.3-flash-high", "agy-gemini-3.7-flash-high"],
  primary_verified_routes: ["claude-opus-5-medium-no-advisor", "pi-zai-cn-glm-5.3-flash-high"],
  reference_only_unverified_routes: ["codex-gpt-5.6-sol-high", "agy-gemini-3.7-flash-high"],
  route_versions: routeVersions,
  model_availability: modelAvailability,
  errors
};
if (write) writeNewFile(path.join(here, "PREFLIGHT.json"), `${JSON.stringify(report, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
if (errors.length) process.exitCode = 2;
