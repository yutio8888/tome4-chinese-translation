import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "../../../..");
const argv = process.argv.slice(2);
const args = new Set(argv);
const outIndex = argv.indexOf("--out");
if (outIndex !== -1 && (!argv[outIndex + 1] || path.basename(argv[outIndex + 1]) !== argv[outIndex + 1])) throw new Error("--out requires a plain filename inside the experiment directory");
const read = name => JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const deepClone = value => structuredClone(value);
const keyOf = item => `${item.task_id}\0${item.original_revision_key}`;

function loadBundle() {
  return {
    manifest: read("MANIFEST.json"),
    manifestSchema: read("MANIFEST-SCHEMA.json"),
    experiment: read("EXPERIMENT.json"),
    armA: read("HOLDOUT-A.json"),
    armB: read("HOLDOUT-B.json"),
    reference: read("REFERENCE.json"),
    controls: read("SOURCE-CONTROLS.json"),
    verification: read("SOURCE-VERIFICATION.json"),
    contexts: read("CONTEXTS.json"),
    sampling: read("SAMPLING.json"),
    reviewerSchema: read("REVIEWER-SCHEMA.json"),
    scorerFixtures: read("SCORER-FIXTURES.json"),
    fixtures: read("PREFLIGHT-FIXTURES.json"),
    prompt: fs.readFileSync(path.join(here, "PROMPT.md"), "utf8"),
    frozen: fs.existsSync(path.join(here, "FROZEN-HASHES.json")) ? read("FROZEN-HASHES.json") : null
  };
}

function gatePass({recallNet, positiveRoutes, controlNet, maxNewControl, contamination}) {
  return recallNet >= 10 && positiveRoutes >= 3 && controlNet <= 2 && maxNewControl <= 1 && contamination === 0;
}

function validateContract(bundle, {requireHashes = false, virtualHashes = null} = {}) {
  const errors = [];
  const check = (condition, message) => { if (!condition) errors.push(message); };
  const {manifest, manifestSchema, experiment, armA, armB, reference, controls, verification, contexts, sampling, reviewerSchema, prompt, frozen} = bundle;

  check(manifest.schema_version === "runtime-source-context-manifest-v1", "manifest schema_version");
  check(["PREFLIGHT_READY", "FROZEN_FOR_INFERENCE"].includes(manifest.status), "manifest status");
  check(manifestSchema.properties?.schema_version?.const === manifest.schema_version, "manifest schema mismatch");
  check(experiment.experiment === "runtime-source-context-pilot-v1", "experiment identity");
  check(experiment.calls?.planned_total === 16 && experiment.calls?.third_run_allowed === false, "experiment call contract");
  check(JSON.stringify(manifest.routes) === JSON.stringify(["codex-gpt-5.6-sol-high", "claude-opus-5-medium-no-advisor", "pi-zai-cn-glm-5.3-flash-high", "agy-gemini-3.7-flash-high"]), "route order");

  check(armA.items?.length === 36 && armB.items?.length === 36, "holdout count");
  const idsA = armA.items?.map(item => item.revision_id) ?? [];
  const idsB = armB.items?.map(item => item.revision_id) ?? [];
  const expectedIds = Array.from({length: 36}, (_, index) => `P${String(index + 1).padStart(3, "0")}`);
  check(JSON.stringify(idsA) === JSON.stringify(expectedIds), "A item order/IDs");
  check(JSON.stringify(idsB) === JSON.stringify(expectedIds), "B item order/IDs");
  check(new Set(idsA).size === 36 && new Set(idsB).size === 36, "duplicate holdout item");
  check(armA.instructions === armB.instructions, "arm instruction drift");
  for (let index = 0; index < Math.min(armA.items?.length ?? 0, armB.items?.length ?? 0); index += 1) {
    const a = armA.items[index];
    const b = armB.items[index];
    const {source_context: sourceContext, ...bBase} = b;
    check(JSON.stringify(a) === JSON.stringify(bBase), `arm drift ${a.revision_id}`);
    check(typeof sourceContext === "string" && sourceContext.trim().length > 0, `CONTEXT_MISSING ${a.revision_id}`);
  }

  const outbound = `${prompt}\n${JSON.stringify(armA)}\n${JSON.stringify(armB)}`;
  const forbiddenPatterns = [
    [/\/(?:home|Users)\//, "outbound local absolute path"],
    [/expected_claim/i, "outbound expected_claim"],
    [/mutation_id/i, "outbound mutation_id"],
    [/REFERENCE\.json/i, "outbound reference artifact"],
    [/SOURCE-VERIFICATION\.json/i, "outbound verification artifact"],
    [/[0-9a-f]{40,64}/i, "outbound hash/commit"],
    [/p2-(?:ashes|cults|orcs|tome)-/i, "outbound task provenance"]
  ];
  for (const [pattern, label] of forbiddenPatterns) check(!pattern.test(outbound), label);
  for (const item of reference.items ?? []) {
    if (item.mutation_id) check(!outbound.includes(item.mutation_id), `leaked mutation ${item.mutation_id}`);
    if (item.expected_claim) check(!outbound.includes(item.expected_claim), `leaked expected claim ${item.revision_id}`);
  }

  check(reference.items?.length === 36 && controls.items?.length === 36 && contexts.items?.length === 36 && verification.items?.length === 36, "sealed artifact counts");
  check(JSON.stringify(reference.items?.map(item => item.revision_id)) === JSON.stringify(expectedIds), "reference order");
  check(JSON.stringify(controls.items?.map(item => item.revision_id)) === JSON.stringify(expectedIds), "source-controls order");
  check(JSON.stringify(contexts.items?.map(item => item.revision_id)) === JSON.stringify(expectedIds), "context-record order");
  const labelCounts = (reference.items ?? []).reduce((counts, item) => { counts[item.label] = (counts[item.label] ?? 0) + 1; return counts; }, {});
  check(JSON.stringify(labelCounts) === JSON.stringify({RUNTIME_CONTROL: 12, SURFACE_MUTATION: 6, RUNTIME_MUTATION: 12, SURFACE_CONTROL: 6}), "label counts");
  check(contexts.missing_count === 0, "context missing count");
  const contextById = new Map((contexts.items ?? []).map(item => [item.revision_id, item]));
  const controlById = new Map((controls.items ?? []).map(item => [item.revision_id, item]));
  for (const item of armB.items ?? []) {
    const record = contextById.get(item.revision_id);
    check(record?.visible_context_sha256 === sha256Bytes(item.source_context ?? ""), `context hash ${item.revision_id}`);
    check(record?.truncated === false, `context truncation ${item.revision_id}`);
  }
  const verificationByKey = new Map((verification.items ?? []).map(item => [keyOf(item), item]));
  check(verificationByKey.size === 36, "verification uniqueness");
  check(verification.status === "FINAL_PRE_INFERENCE", "verification status");
  for (const item of controls.items ?? []) {
    const checked = verificationByKey.get(keyOf(item));
    check(checked?.status === "CLEAN", `verification CLEAN ${item.revision_id}`);
    check(Array.isArray(checked?.evidence) && checked.evidence.length > 0, `verification evidence ${item.revision_id}`);
    check(checked?.clean_target_sha256 === sha256Bytes(item.clean_target), `clean target hash ${item.revision_id}`);
    check(checked?.visible_context_sha256 === item.context.visible_context_sha256, `verified context hash ${item.revision_id}`);
    check(checked?.source_file_sha256 === item.context.source_file_sha256, `verified source hash ${item.revision_id}`);
  }
  for (const ref of reference.items ?? []) {
    const sourceControl = controlById.get(ref.revision_id);
    if (ref.label.endsWith("MUTATION")) {
      check(typeof ref.atom_target_span === "string" && ref.atom_target_span.length > 0, `mutation atom ${ref.revision_id}`);
      check(typeof ref.claim_type === "string", `mutation claim_type ${ref.revision_id}`);
      const target = sourceControl?.presented_target ?? "";
      const first = target.indexOf(ref.atom_target_span);
      check(first !== -1 && target.indexOf(ref.atom_target_span, first + ref.atom_target_span.length) === -1, `unique mutation atom ${ref.revision_id}`);
    } else {
      check(ref.mutation_id === null && ref.atom_target_span === null && ref.claim_type === null, `control sealed fields ${ref.revision_id}`);
    }
  }

  const frame = sampling.runtime_candidate_frame;
  const frameKeys = [...(frame.mutations ?? []), ...(frame.controls ?? []), ...(frame.ordered_reserves_not_used ?? []), ...(frame.baseline_exclusions ?? []).map(item => [item.task_id, item.original_revision_key])].map(pair => pair.join("\0"));
  check(frame.eligible === 26 && frameKeys.length === 26 && new Set(frameKeys).size === 26, "runtime frame coverage");
  check((frame.controls ?? []).length === 12, "runtime control selection count");
  check((frame.ordered_reserves_not_used ?? []).length === 1, "runtime reserve count");
  check((frame.baseline_exclusions ?? []).length === 1, "runtime baseline exclusion count");
  const rankRecords = frame.control_ranks ?? [];
  check(rankRecords.length === 13, "control rank count");
  const sortedRanks = [...rankRecords].sort((left, right) => left.sha256_rank.localeCompare(right.sha256_rank));
  check(JSON.stringify(rankRecords) === JSON.stringify(sortedRanks), "control rank order");
  check(rankRecords.slice(0, 12).every(item => item.disposition === "CONTROL") && rankRecords.slice(12).every(item => item.disposition === "ORDERED_RESERVE"), "reserve boundary");

  check(reviewerSchema.properties?.revisions?.minItems === 36 && reviewerSchema.properties?.revisions?.maxItems === 36, "reviewer schema count");
  check(reviewerSchema.additionalProperties === false, "reviewer schema closure");
  check(manifest.gates?.runtime_recall?.denominator_per_run === 48 && manifest.gates?.runtime_recall?.pass_net_gain_minimum === 10, "recall gate contract");
  check(manifest.gates?.runtime_control_candidate_delta?.pass_net_gain_maximum === 2, "control gate contract");
  check(manifest.gates?.per_route_new_control_candidates?.maximum === 1, "per-route control gate");
  check(manifest.gates?.control_contamination?.maximum === 0, "contamination gate");

  if (requireHashes) {
    check(frozen?.schema_version === "runtime-source-context-frozen-hashes-v1", "frozen hashes missing");
    const actualHashes = virtualHashes ?? Object.fromEntries(Object.keys(frozen?.files ?? {}).map(name => [name, fs.existsSync(path.join(here, name)) ? sha256File(path.join(here, name)) : null]));
    for (const [name, expected] of Object.entries(frozen?.files ?? {})) check(actualHashes[name] === expected, `frozen hash drift ${name}`);
  }
  return errors;
}

function runFixtures(bundle) {
  const results = [];
  for (const fixture of bundle.fixtures.cases) {
    if (fixture.mutation.startsWith("GATE_")) {
      const numbers = fixture.mutation.slice(5).split("_").map(Number);
      const actualPass = gatePass({recallNet: numbers[0], positiveRoutes: numbers[1], controlNet: numbers[2], maxNewControl: numbers[3], contamination: numbers[4]});
      results.push({id: fixture.id, expected_pass: fixture.expected_pass, actual_pass: actualPass, ok: actualPass === fixture.expected_pass});
      continue;
    }
    const test = deepClone(bundle);
    let requireHashes = false;
    let virtualHashes = null;
    if (fixture.mutation === "DELETE_FIRST_B_CONTEXT") delete test.armB.items[0].source_context;
    if (fixture.mutation === "DUPLICATE_SECOND_ID") test.armA.items[1].revision_id = test.armA.items[0].revision_id;
    if (fixture.mutation === "CHANGE_FIRST_B_TARGET") test.armB.items[0].target += "漂移";
    if (fixture.mutation === "LEAK_EXPECTED_CLAIM_TO_PROMPT") test.prompt += `\n${test.reference.items.find(item => item.expected_claim).expected_claim}`;
    if (fixture.mutation === "PROMOTE_RESERVE_WITHOUT_REMOVAL") test.sampling.runtime_candidate_frame.controls.push(test.sampling.runtime_candidate_frame.ordered_reserves_not_used[0]);
    if (fixture.mutation === "CORRUPT_EXPECTED_PROMPT_HASH") {
      requireHashes = true;
      test.frozen = test.frozen ?? {schema_version: "runtime-source-context-frozen-hashes-v1", files: {"PROMPT.md": sha256Bytes(test.prompt)}};
      test.frozen.files["PROMPT.md"] = "0".repeat(64);
      virtualHashes = {"PROMPT.md": sha256Bytes(test.prompt)};
    }
    const errors = validateContract(test, {requireHashes, virtualHashes});
    const actualPass = errors.length === 0;
    results.push({id: fixture.id, expected_pass: fixture.expected_pass, actual_pass: actualPass, ok: actualPass === fixture.expected_pass, observed_errors: errors.slice(0, 3)});
  }
  return results;
}

function runScorerFixtures(fixtures) {
  const atomStart = fixtures.target.indexOf(fixtures.atom_target_span);
  const atomEnd = atomStart + fixtures.atom_target_span.length;
  return fixtures.cases.map(fixture => {
    const spanStart = fixture.target_span === null ? -1 : fixtures.target.indexOf(fixture.target_span);
    const overlap = spanStart >= 0 && spanStart < atomEnd && spanStart + fixture.target_span.length > atomStart;
    const detection = fixture.verdict !== "OK" && fixture.valid_claim && overlap && fixture.reported_claim_type === fixtures.claim_type ? 1 : 0;
    const findingDetection = detection && fixture.verdict === "FINDING" ? 1 : 0;
    return {id: fixture.id, detection, finding_detection: findingDetection, ok: detection === fixture.expected_detection && findingDetection === fixture.expected_finding_detection};
  });
}

const bundle = loadBundle();
const requireHashes = args.has("--require-hashes");
const errors = validateContract(bundle, {requireHashes});
let fixtureResults = [];
let scorerFixtureResults = [];
if (args.has("--fixtures")) {
  fixtureResults = runFixtures(bundle);
  scorerFixtureResults = runScorerFixtures(bundle.scorerFixtures);
}
if (args.has("--pre-inference")) {
  const generated = fs.readdirSync(here).filter(name => /^(?:RAW|CANDIDATE|FAILURE)-[AB]-run/.test(name));
  if (generated.length) errors.push(`pre-inference output artifacts already exist: ${generated.join(", ")}`);
}
if (args.has("--route-check")) {
  const expected = new Map(read("ROUTE-PREFLIGHT.json").routes.map(item => [item.cli, item.cli_version]));
  for (const [command, version] of expected) {
    const actual = execFileSync(command, ["--version"], {cwd: "/tmp", encoding: "utf8"}).trim();
    if (actual !== version) errors.push(`${command} version drift: ${actual}`);
  }
}
const fixtureFailures = fixtureResults.filter(item => !item.ok);
if (fixtureFailures.length) errors.push(`${fixtureFailures.length} fixture expectation(s) failed`);
const scorerFixtureFailures = scorerFixtureResults.filter(item => !item.ok);
if (scorerFixtureFailures.length) errors.push(`${scorerFixtureFailures.length} scorer fixture(s) failed`);

const executorFixture = path.resolve(here, "../qwen3-8-27b-agent-roles/executor-fixture.lua");
const executorHash = sha256File(executorFixture);
if (executorHash !== "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7") errors.push("executor fixture baseline drift");
try { execFileSync("git", ["diff", "--check"], {cwd: repo, encoding: "utf8"}); } catch (error) { errors.push(`git diff --check failed: ${error.stdout ?? error.message}`); }

const report = {schema_version: "runtime-source-context-preflight-report-v1", status: errors.length ? "NO_GO" : "GO", require_hashes: requireHashes, contract_errors: errors, fixtures: fixtureResults, scorer_fixtures: scorerFixtureResults, executor_fixture_sha256: executorHash};
if (outIndex !== -1) {
  const outputPath = path.join(here, argv[outIndex + 1]);
  if (fs.existsSync(outputPath)) throw new Error(`refusing to overwrite ${path.basename(outputPath)}`);
  fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`);
}
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
if (errors.length) process.exitCode = 2;
