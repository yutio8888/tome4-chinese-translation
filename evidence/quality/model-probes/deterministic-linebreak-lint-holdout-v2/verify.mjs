#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath, pathToFileURL} from "node:url";
import {FROZEN, buildHanStatistics, readInventory, scanRows, sha256Bytes, sha256File} from "./scanner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
if (argv.length !== 2 || argv[0] !== "--repo" || !argv[1]) throw new Error("usage: TOME_ENGINE_ROOT=... node verify.mjs --repo SOURCE_REPO");
if (!process.env.TOME_ENGINE_ROOT) throw new Error("TOME_ENGINE_ROOT must be supplied at runtime");
const repo = path.resolve(argv[1]);
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "deterministic-linebreak-holdout-v2-"));
const source = path.join(temporary, "source");
const rebuilt = path.join(temporary, "rebuilt");

const requiredJson = [
  "EXPERIMENT.json",
  "RULE-CONTRACT.json",
  "EXCLUSIONS.json",
  "SCANNER-FIXTURES.json",
  "CANDIDATES.json",
  "SOURCE-AUDIT.json",
  "RESULT.json"
];
const requiredPackage = [
  "README.md",
  ...requiredJson,
  "scanner-lib.mjs",
  "scan.mjs",
  "test-scanner.mjs",
  "verify.mjs"
];
const expectedV1Hashes = new Map([
  ["scanner-lib.mjs", "1fe7e5dbe8ddd41de9dae63614ee40198095d683b6cd486fc42653b773d1279c"],
  ["scan.mjs", "ea944f267fc7a312227f346bd6fda38513fb3725fdad33926a2cf545fa1b16b7"],
  ["RULE-CONTRACT.json", "fef9fb556adcd4b083a05213b40d483d528ef87185f6eda41e58d93f8d565b4d"],
  ["SCANNER-FIXTURES.json", "b00d56a8573efaf204e260bee055b24daa704fd38277e9562f1724ed33b25356"],
  ["CANDIDATES.json", "d048499955350a07988ee49f7e4c1a8aa26fb6ba3b115c774f09d25e45432aab"]
]);

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};
const readJson = (directory, name) => JSON.parse(fs.readFileSync(path.join(directory, name), "utf8"));
const identity = value => JSON.stringify([
  value.revision_id,
  value.revision_uid,
  value.tier,
  value.boundary.line_ordinal_zero_based,
  value.boundary.bigram,
  value.boundary.rendered,
  value.source_sha256,
  value.target_sha256
]);

try {
  for (const name of requiredPackage) assert(fs.statSync(path.join(here, name)).isFile(), `${name} missing`);
  for (const name of requiredJson) readJson(here, name);
  for (const name of requiredPackage.filter(name => name.endsWith(".mjs"))) {
    execFileSync(process.execPath, ["--check", path.join(here, name)], {stdio: "pipe"});
  }
  const fixtureReport = JSON.parse(execFileSync(process.execPath, [path.join(here, "test-scanner.mjs")], {encoding: "utf8"}));
  assert(fixtureReport.status === "PASS" && fixtureReport.fixture_cases === 10, "scanner fixture gate drift");

  execFileSync("git", ["clone", "--no-hardlinks", "--no-checkout", repo, source], {stdio: "pipe"});
  execFileSync("git", ["-C", source, "checkout", "--detach", FROZEN.baselineCommit], {stdio: "pipe"});
  const detachedHead = execFileSync("git", ["-C", source, "rev-parse", "HEAD"], {encoding: "utf8"}).trim();
  assert(detachedHead === FROZEN.baselineCommit, "detached baseline checkout drift");

  const v1Directory = path.join(source, "evidence", "quality", "model-probes", "deterministic-linebreak-lint-v1");
  for (const [name, expected] of expectedV1Hashes) assert(sha256File(path.join(v1Directory, name)) === expected, `v1 provenance drift: ${name}`);

  const inventoryReport = JSON.parse(execFileSync("python3", ["-B", "tools/i18n", "quality", "inventory", "--json"], {
    cwd: source,
    encoding: "utf8",
    env: process.env,
    stdio: ["ignore", "pipe", "pipe"]
  }));
  assert(inventoryReport.entries === FROZEN.inventoryRows, "inventory row report drift");
  assert(inventoryReport.inventory_sha256 === FROZEN.inventoryCanonicalSha256, "inventory canonical report drift");
  assert(inventoryReport.translation_inputs_sha256 === FROZEN.translationInputsSha256, "translation-input digest drift");
  assert(inventoryReport.manifest_sha256 === FROZEN.inventoryManifestSha256, "inventory manifest digest drift");
  assert(inventoryReport.policy_sha256 === FROZEN.inventoryPolicySha256, "inventory policy digest drift");
  assert(inventoryReport.taxonomy_sha256 === FROZEN.inventoryTaxonomySha256, "inventory taxonomy digest drift");
  assert(inventoryReport.terminology_sha256 === FROZEN.inventoryTerminologySha256, "inventory terminology digest drift");
  assert(inventoryReport.tool_version === "0.5.0", "inventory tool version drift");
  const inventoryPath = path.resolve(source, inventoryReport.inventory);
  assert(path.relative(source, inventoryPath).split(path.sep)[0] !== "..", "inventory path escaped detached clone");
  const schemaPath = path.join(source, "i18n", "quality", "schemas", "inventory-v1.schema.json");
  assert(sha256File(schemaPath) === FROZEN.inventorySchemaSha256, "inventory schema digest drift");
  const inventory = readInventory(inventoryPath);
  assert(inventory.raw_sha256 === FROZEN.inventoryRawSha256, "inventory raw digest drift");
  assert(inventory.canonical_sha256 === FROZEN.inventoryCanonicalSha256, "inventory canonical digest drift");

  const statistics = buildHanStatistics(inventory.rows);
  assert(statistics.hanCharacters === FROZEN.hanCharacters, "Han corpus count drift");
  const v2RawScan = scanRows(inventory.rows, statistics);
  const v1 = await import(`${pathToFileURL(path.join(v1Directory, "scanner-lib.mjs")).href}?baseline=${FROZEN.baselineCommit}`);
  const v1Statistics = v1.buildHanStatistics(inventory.rows);
  const v1RawScan = v1.scanRows(inventory.rows, v1Statistics);
  assert(JSON.stringify(v2RawScan) === JSON.stringify(v1RawScan), "v1/v2 raw scanner behavior drift");

  execFileSync(process.execPath, [
    path.join(here, "scan.mjs"),
    "--inventory", inventoryPath,
    "--schema", schemaPath,
    "--out-dir", rebuilt
  ], {stdio: "pipe"});
  for (const name of ["CANDIDATES.json", "SOURCE-AUDIT.json", "RESULT.json"]) {
    assert(fs.readFileSync(path.join(rebuilt, name), "utf8") === fs.readFileSync(path.join(here, name), "utf8"), `${name} byte regeneration drift`);
  }

  const experiment = readJson(here, "EXPERIMENT.json");
  const exclusions = readJson(here, "EXCLUSIONS.json");
  const candidates = readJson(here, "CANDIDATES.json");
  const audit = readJson(here, "SOURCE-AUDIT.json");
  const result = readJson(here, "RESULT.json");
  assert(exclusions.exclusions.length === 5, "exclusion count drift");
  assert(new Set(exclusions.exclusions.map(identity)).size === 5, "exclusion identities are not unique");
  assert(candidates.pre_exclusion_candidates.length === 5, "pre-exclusion candidate count drift");
  assert(candidates.independent_holdout_candidates.length === 0, "independent holdout must be empty");
  assert(candidates.pre_exclusion_candidates.every(candidate => candidate.status === "CANDIDATE_NOT_GROUND_TRUTH"), "pre-exclusion candidate was promoted to ground truth");
  const registered = new Set(exclusions.exclusions.map(identity));
  assert(candidates.pre_exclusion_candidates.every(candidate => registered.has(identity(candidate))), "emitted candidate lacks exact exclusion");
  assert(new Set(candidates.pre_exclusion_candidates.map(identity)).size === registered.size, "exclusion coverage is not one-to-one");
  assert(audit.records.length === 0 && audit.counts.independent_candidates === 0 && audit.precision.denominator === 0 && audit.precision.value === null, "empty audit contract drift");
  assert(audit.candidate_artifact.sha256 === sha256File(path.join(here, "CANDIDATES.json")), "audit candidate binding drift");
  assert(audit.holdout_population_binding.ordered_identity_set_sha256 === sha256Bytes(JSON.stringify([])), "empty holdout identity binding drift");
  assert(result.status === "NO_GO_INSUFFICIENT_INDEPENDENT_CANDIDATES", "result status drift");
  assert(result.independent_evaluation.precision_denominator === 0 && result.independent_evaluation.precision === null && result.independent_evaluation.recall === null, "undefined estimand reporting drift");
  assert(result.future_threshold === null, "future threshold must remain undefined");
  assert(Object.values(result.cross_component_coverage).every(component => component.independent_candidates === 0), "cross-component shortfall drift");
  const requiredClaims = new Set([
    "independent precision/recall claims",
    "zero-false-alarm claims",
    "pooled-v1 performance claims",
    "cross-component performance claims",
    "deployment or production lint integration claims"
  ]);
  assert(requiredClaims.size === result.prohibited_claims.length && result.prohibited_claims.every(claim => requiredClaims.has(claim)), "prohibited claims drift");
  assert(JSON.stringify(experiment.prohibited_claims) === JSON.stringify(result.prohibited_claims), "experiment/result claim prohibition mismatch");

  for (const [bindingName, binding] of Object.entries(result.artifact_bindings)) {
    assert(sha256File(path.join(here, binding.logical_path)) === binding.sha256, `result binding drift: ${bindingName}`);
  }
  for (const artifact of [experiment, exclusions, candidates, audit, result]) {
    assert(artifact.model_calls_made === 0 && artifact.network_calls_made === 0, "nonzero call accounting");
  }
  const executorFixture = path.resolve(here, "../qwen3-8-27b-agent-roles/executor-fixture.lua");
  assert(sha256File(executorFixture) === "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7", "executor fixture baseline drift");

  const packageText = requiredPackage.map(name => fs.readFileSync(path.join(here, name), "utf8")).join("\n");
  const absolutePathPattern = new RegExp(["(?:/", "(?:home|Users|root|tmp|opt|var|mnt)", "/|[A-Za-z]:", "\\\\)"].join(""), "u");
  assert(!absolutePathPattern.test(packageText), "persisted local absolute path detected");
  const credentialMarkers = [
    ["OPEN", "AI_", "API", "_KEY"].join(""),
    ["ANTH", "ROPIC_", "API", "_KEY"].join(""),
    ["GOO", "GLE_", "API", "_KEY"].join(""),
    ["Authorization", ": Bearer"].join("")
  ];
  assert(credentialMarkers.every(marker => !packageText.includes(marker)), "credential marker detected");
  const executableText = requiredPackage.filter(name => name.endsWith(".mjs")).map(name => fs.readFileSync(path.join(here, name), "utf8")).join("\n");
  const networkSurfaces = [
    ["node:", "http"].join(""),
    ["node:", "https"].join(""),
    ["node:", "net"].join(""),
    ["globalThis", ".fetch"].join(""),
    ["Web", "Socket"].join("")
  ];
  assert(networkSurfaces.every(surface => !executableText.includes(surface)), "network-capable code surface detected");

  process.stdout.write(`${JSON.stringify({
    status: "PASS",
    baseline_commit: FROZEN.baselineCommit,
    inventory_rows: inventory.rows.length,
    inventory_canonical_sha256: inventory.canonical_sha256,
    v1_v2_raw_behavior: "BYTE_VALUE_EQUAL",
    fixtures: "PASS_10_OF_10",
    pre_exclusion_candidates: candidates.pre_exclusion_candidates.length,
    exact_exclusions: exclusions.exclusions.length,
    post_exclusion_independent_candidates: candidates.independent_holdout_candidates.length,
    derived_artifact_regeneration: "PASS_BYTE_FOR_BYTE",
    result_status: result.status,
    executor_fixture_sha256: sha256File(executorFixture),
    model_calls_made: 0,
    network_calls_made: 0
  }, null, 2)}\n`);
} finally {
  const expectedPrefix = path.join(os.tmpdir(), "deterministic-linebreak-holdout-v2-");
  if (path.dirname(temporary) !== os.tmpdir() || !temporary.startsWith(expectedPrefix)) throw new Error(`refusing to remove unexpected temporary path: ${temporary}`);
  fs.rmSync(temporary, {recursive: true, force: true});
}
