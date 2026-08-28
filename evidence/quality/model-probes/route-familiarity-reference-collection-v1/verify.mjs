#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import {createRequire} from "node:module";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildPackage} from "./build.mjs";

const require = createRequire(import.meta.url);

function loadAjv2020() {
  const prerequisite = "Ajv preflight failed: ajv/dist/2020 from Ajv major 8 is required; install Ajv 8 so it is resolvable before running this schema-validation gate";
  try {
    const modulePath = require.resolve("ajv/dist/2020");
    const packagePath = require.resolve("ajv/package.json");
    const packageRecord = JSON.parse(fs.readFileSync(packagePath, "utf8"));
    const major = Number.parseInt(String(packageRecord.version).split(".")[0], 10);
    if (major !== 8) throw new Error(`resolved unsupported Ajv version ${packageRecord.version}`);
    const loaded = require(modulePath);
    return {Ajv2020: loaded.default ?? loaded, version: packageRecord.version};
  } catch (error) {
    throw new Error(`${prerequisite}: ${error.message}`, {cause: error});
  }
}

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../..");
const predecessor = path.join(root, "evidence/quality/model-probes/route-familiarity-reference-audit-v1");
const generatedNames = [
  ...Array.from({length: 5}, (_, index) => `OUTBOUND-SHARD-${String(index + 1).padStart(2, "0")}.json`),
  "PROMPT.md",
  ...Array.from({length: 5}, (_, index) => `RESPONSE-SCHEMA-SHARD-${String(index + 1).padStart(2, "0")}.json`),
  "LOCAL-ROUTE-MANIFEST.json",
  "BUILD-REPORT.json",
  "EXPERIMENT.json"
];
const frozenInputs = {
  "OUTBOUND-AUDIT-QUEUE.json": "620b736996ac254c43b3c721cdbfca20f7e68d8f553b7fe21b9effa0c025b3d2",
  "REFERENCE-SCHEMA.json": "c197e30ebaaae353df58049c2f3479dc2a0c799d3633dba4e70b5db27f859f34",
  "LOCAL-BINDING-REGISTRY.json": "64013413c5a30956185a7a71c2b21d7960a6b2ddda55e9c709657fe10ac3a7a1"
};
const frozenOutputHashes = {
  "OUTBOUND-SHARD-01.json": "f3ebe42a0009cb40f280737b91258a75601f3ad6bf21e4e59a16cd10db01d75b",
  "OUTBOUND-SHARD-02.json": "0f616fd426ec3dd696e8c96328efcf9e2140a83c949d289c666ecb2f3eac63cf",
  "OUTBOUND-SHARD-03.json": "143d6929457120519065768a344fd7c3eaa23f72ff0f214496d4f88b9e0961b8",
  "OUTBOUND-SHARD-04.json": "8e7c060fb15e6978c6614294de25a9a4a8dfe7e8000e0b0cc2046f63e52fca78",
  "OUTBOUND-SHARD-05.json": "1c5f64837ccacd99ecd0b61bfafeedddfe2f6f50ffa14515318510d628bca75b",
  "PROMPT.md": "fdcdfff87553b8cdaea8fba2c92e485abbe2263a805a9f7622f0dcae6f0c827b",
  "RESPONSE-SCHEMA-SHARD-01.json": "ac6f8b8080e21c8e91a44d6092ad69a94438368fa2f1b122bdd2039042210850",
  "RESPONSE-SCHEMA-SHARD-02.json": "d6aa22d38e2e6a0123d554245d7abf361fcdbcff88153b020543d97c58227ab6",
  "RESPONSE-SCHEMA-SHARD-03.json": "1c45fbf9d8a68dfd3b05c8862ff7badc491f2bc17be43ebad55ad370b9431b23",
  "RESPONSE-SCHEMA-SHARD-04.json": "6cfcb635ab86e4bcc094fb898e9ff73958a6f7a5779eb521dc8f66210179200c",
  "RESPONSE-SCHEMA-SHARD-05.json": "602746590fa301be1050dc6faff26f9bd16c3b87673725da09ea9f088d4a6c19",
  "LOCAL-ROUTE-MANIFEST.json": "7b457d5539ecb1e89e6d7cae1a3b067e25d8f20f1d42524c8bac99ba07ba8e5d",
  "BUILD-REPORT.json": "887978aaa2626bbd458b09df6f369fac0ef6e4593433794bd5807eb655b71bbf",
  "EXPERIMENT.json": "379084af01ab32970bd43745332567c1c3826081a55bfe12851d42cceca00ca4"
};
const fixturePath = path.join(root, "evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua");
const fixtureHash = "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7";
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
const sorted = values => [...values].sort((left, right) => left < right ? -1 : left > right ? 1 : 0);
const exactKeys = (value, expected, label) => assert.deepEqual(sorted(Object.keys(value)), sorted(expected), `${label}: exact keys`);

function strings(value, pointer = "") {
  if (typeof value === "string") return [{pointer, value}];
  if (Array.isArray(value)) return value.flatMap((entry, index) => strings(entry, `${pointer}/${index}`));
  if (value && typeof value === "object") return Object.entries(value).flatMap(([key, entry]) => strings(entry, `${pointer}/${key}`));
  return [];
}

const outboundForbidden = [
  ["historical route cell", /\bH[1-4]\b/u],
  ["provider/model identity", /\b(?:OpenAI|Anthropic|Google|Z\.ai|Codex|Claude|Gemini|GLM|Qwen|Grok|GPT[-_.]?\d)\b/iu],
  ["local absolute path", /(?:\/home\/|\/Users\/|\/tmp\/|\/private\/|\/srv\/|\/mnt\/|[A-Za-z]:[\\/](?:Users|home|work)[\\/]|\\\\[^\\]+\\[^\\]+)/u],
  ["local provenance", /(?:\bprovenance\b|local[ _-]?(?:binding|registry)|presentation[ _-]?ordinal)/iu],
  ["sealed/prior conclusion", /(?:sealed[ _-]?(?:truth|reference)|prior (?:finding|adjudication)|defect[ _-]?id|already reviewed|senior[ _-]?audit)/iu]
];

function scanOutbound(value, {allowLabelVocabulary = false, prompt = false} = {}) {
  for (const {pointer, value: text} of strings(value)) {
    for (const [label, pattern] of outboundForbidden) assert.equal(pattern.test(text), false, `${pointer || "/"}: outbound ${label}`);
    if (!prompt && !allowLabelVocabulary) assert.equal(/\b(?:CLEAN|SURFACE_VISIBLE_DEFECT|CONTEXT_DEPENDENT_DEFECT|UNRESOLVED)\b/u.test(text), false, `${pointer || "/"}: populated label`);
    if (prompt) assert.equal(/["']label["']\s*:\s*["'](?:CLEAN|SURFACE_VISIBLE_DEFECT|CONTEXT_DEPENDENT_DEFECT|UNRESOLVED)["']/u.test(text), false, `${pointer || "/"}: populated-answer structure`);
  }
}

const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "route-familiarity-reference-collection-v1-"));
try {
  buildPackage({root, out: temporaryDirectory});
  for (const name of generatedNames) {
    const committed = fs.readFileSync(path.join(here, name));
    const rebuilt = fs.readFileSync(path.join(temporaryDirectory, name));
    assert.deepEqual(rebuilt, committed, `${name}: byte-for-byte rebuild`);
    assert.equal(sha256(committed), frozenOutputHashes[name], `${name}: frozen output hash`);
    if (name.endsWith(".json")) JSON.parse(committed.toString("utf8"));
  }
  assert.deepEqual(sorted(fs.readdirSync(temporaryDirectory)), sorted(generatedNames), "deterministic generated filename set");

  for (const [name, expected] of Object.entries(frozenInputs)) assert.equal(sha256(fs.readFileSync(path.join(predecessor, name))), expected, `${name}: frozen input hash`);
  assert.equal(sha256(fs.readFileSync(fixturePath)), fixtureHash, "executor fixture hash");

  const queue = readJson(path.join(predecessor, "OUTBOUND-AUDIT-QUEUE.json"));
  const predecessorSchema = readJson(path.join(predecessor, "REFERENCE-SCHEMA.json"));
  const shards = Array.from({length: 5}, (_, index) => readJson(path.join(here, `OUTBOUND-SHARD-${String(index + 1).padStart(2, "0")}.json`)));
  const concatenated = shards.flatMap(shard => shard.items);
  assert.deepEqual(concatenated, queue.items, "five contiguous shards concatenate to exact queue rows/order");
  assert.equal(concatenated.length, 145);
  assert.equal(new Set(concatenated.map(item => item.neutral_id)).size, 145);
  for (let index = 0; index < concatenated.length; index += 1) {
    assert.equal(Buffer.from(JSON.stringify(concatenated[index]), "utf8").equals(Buffer.from(JSON.stringify(queue.items[index]), "utf8")), true, `${concatenated[index].neutral_id}: predecessor item record bytes/order unchanged`);
  }
  for (let shardIndex = 0; shardIndex < shards.length; shardIndex += 1) {
    const shard = shards[shardIndex];
    exactKeys(shard, ["schema_version", "status", "parent_queue_sha256", "shard_id", "item_count", "items", "source_evidence"], shard.shard_id);
    assert.equal(shard.parent_queue_sha256, frozenInputs["OUTBOUND-AUDIT-QUEUE.json"]);
    assert.equal(shard.shard_id, `SHARD-${String(shardIndex + 1).padStart(2, "0")}`);
    assert.equal(shard.item_count, 29); assert.equal(shard.items.length, 29);
    for (const item of shard.items) {
      exactKeys(item, ["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context", "response"], item.neutral_id);
      assert.equal(item.response, null, `${item.neutral_id}: zero response`);
    }
    assert.equal(shard.source_evidence.length, 29, `${shard.shard_id}: source evidence count`);
    for (let itemIndex = 0; itemIndex < 29; itemIndex += 1) {
      const item = shard.items[itemIndex];
      const evidence = shard.source_evidence[itemIndex];
      exactKeys(evidence, ["evidence_id", "neutral_id", "sha256", "text"], `${shard.shard_id}: evidence ${itemIndex}`);
      assert.equal(evidence.evidence_id, `EVIDENCE-${item.neutral_id}`);
      assert.equal(evidence.neutral_id, item.neutral_id);
      assert.equal(Buffer.from(evidence.text, "utf8").equals(Buffer.from(item.bounded_fixed_context, "utf8")), true, `${item.neutral_id}: exact UTF-8 text bytes`);
      assert.match(evidence.sha256, /^[0-9a-f]{64}$/u);
      assert.equal(evidence.sha256, sha256(Buffer.from(evidence.text, "utf8")), `${item.neutral_id}: source evidence hash`);
    }
    scanOutbound(shard);
  }

  const prompt = fs.readFileSync(path.join(here, "PROMPT.md"), "utf8");
  scanOutbound(prompt, {prompt: true});
  for (const label of ["CLEAN", "SURFACE_VISIBLE_DEFECT", "CONTEXT_DEPENDENT_DEFECT", "UNRESOLVED"]) assert.match(prompt, new RegExp(`(?:^|\\W)${label}(?:$|\\W)`, "u"), `${label}: prompt definition present`);

  const {Ajv2020, version: ajvVersion} = loadAjv2020();
  const schemas = Array.from({length: 5}, (_, index) => readJson(path.join(here, `RESPONSE-SCHEMA-SHARD-${String(index + 1).padStart(2, "0")}.json`)));
  for (let index = 0; index < schemas.length; index += 1) {
    const schema = schemas[index];
    const shard = shards[index];
    scanOutbound(schema, {allowLabelVocabulary: true});
    exactKeys(schema, ["$schema", "$id", "title", "type", "additionalProperties", "required", "properties", "$defs"], `${shard.shard_id} schema`);
    assert.equal(schema.$schema, "https://json-schema.org/draft/2020-12/schema");
    assert.equal(schema.additionalProperties, false);
    assert.deepEqual(schema.$defs, predecessorSchema.$defs, `${shard.shard_id}: exact predecessor response definitions`);
    assert.equal(schema.properties.parent_queue_sha256.const, frozenInputs["OUTBOUND-AUDIT-QUEUE.json"]);
    assert.equal(schema.properties.shard_id.const, shard.shard_id);
    assert.equal(schema.properties.shard_file_sha256.const, frozenOutputHashes[`OUTBOUND-SHARD-${String(index + 1).padStart(2, "0")}.json`]);
    assert.equal(schema.properties.item_count.const, 29);
    const ids = shard.items.map(item => item.neutral_id);
    assert.deepEqual(schema.properties.item_ids.const, ids);
    assert.deepEqual(schema.properties.items.prefixItems.map(entry => entry.properties.neutral_id.const), ids);
    assert.deepEqual(schema.properties.items.prefixItems.map(entry => entry.properties.response.properties.source_evidence_sha256s.items.const), shard.source_evidence.map(evidence => evidence.sha256));
    assert.equal(schema.properties.items.minItems, 29); assert.equal(schema.properties.items.maxItems, 29); assert.equal(schema.properties.items.items, false);
    const validate = new Ajv2020({allErrors: true, strict: true}).compile(schema);
    const response = {label: "CLEAN", evidence: "checked", defect_atoms: [], source_evidence_sha256s: [], limitations: ""};
    const document = firstResponse => ({
      schema_version: "route-familiarity-reference-collection-responses-v1",
      status: "REFERENCE_COLLECTION_COMPLETE",
      parent_queue_sha256: frozenInputs["OUTBOUND-AUDIT-QUEUE.json"],
      shard_id: shard.shard_id,
      shard_file_sha256: frozenOutputHashes[`OUTBOUND-SHARD-${String(index + 1).padStart(2, "0")}.json`],
      item_count: 29,
      item_ids: ids,
      items: ids.map((neutral_id, itemIndex) => ({neutral_id, response: structuredClone(itemIndex === 0 ? firstResponse : response)}))
    });
    assert.equal(validate(document(response)), true, `${shard.shard_id}: Ajv baseline document`);
    const contextDependent = {label: "CONTEXT_DEPENDENT_DEFECT", evidence: "bounded context establishes defect", defect_atoms: [{kind: "ACCURACY", claim: "bounded claim", evidence: "bounded evidence"}], source_evidence_sha256s: [shard.source_evidence[0].sha256], limitations: ""};
    assert.equal(validate(document(contextDependent)), true, `${shard.shard_id}: context-dependent expected hash`);
    for (const badHash of ["0".repeat(64), "f".repeat(64), shard.source_evidence[1].sha256]) {
      assert.equal(validate(document({...contextDependent, source_evidence_sha256s: [badHash]})), false, `${shard.shard_id}: reject non-item evidence hash`);
    }
  }

  const manifest = readJson(path.join(here, "LOCAL-ROUTE-MANIFEST.json"));
  assert.equal(manifest.outbound_allowed, false); assert.equal(manifest.inference_allowed, false);
  assert.equal(manifest.lanes.length, 4); assert.equal(manifest.counts.completed_model_calls, 0); assert.equal(manifest.counts.populated_responses, 0);
  const expectedRoutes = [["OpenAI", "gpt-5.6-sol"], ["Anthropic", "claude-opus-5"], ["Google", "gemini-3.7-flash-high"], ["Z.ai/GLM", "opencode-go/glm-5.3"]];
  const baselineBindings = JSON.stringify(manifest.lanes[0].bindings);
  for (let index = 0; index < 4; index += 1) {
    const lane = manifest.lanes[index];
    assert.deepEqual([lane.provider, lane.model], expectedRoutes[index]);
    assert.equal(JSON.stringify(lane.bindings), baselineBindings, `${lane.lane_id}: identical bindings`);
    for (const status of [lane.route_availability_status, lane.cli_version_status, lane.runtime_identity_status]) assert.equal(status, "MUST_RECHECK_BEFORE_INFERENCE");
    for (const binding of lane.bindings) {
      assert.equal(binding.shard_sha256, frozenOutputHashes[binding.shard_path]);
      assert.equal(binding.prompt_sha256, frozenOutputHashes[binding.prompt_path]);
      assert.equal(binding.response_schema_sha256, frozenOutputHashes[binding.response_schema_path]);
    }
  }
  assert.deepEqual(manifest.derivation_rules, {
    evaluation_semantics: "FIRST_MATCH_WINS_IN_EVALUATION_ORDER",
    evaluation_order: ["any_unresolved", "any_material_evidence_conflict", "unanimous_or_three_of_four", "two_two_split", "default_outcome"],
    any_unresolved: "LEAD_ADJUDICATION_REQUIRED",
    any_material_evidence_conflict: "LEAD_ADJUDICATION_REQUIRED",
    unanimous_or_three_of_four: "PROVISIONAL_CONSENSUS",
    two_two_split: "LEAD_ADJUDICATION_REQUIRED",
    default_outcome: "LEAD_ADJUDICATION_REQUIRED",
    per_route_reference_score: "LEAVE_ONE_ROUTE_OUT_CONSENSUS_PLUS_LEAD_ADJUDICATION",
    leave_one_route_out: {
      eligible_inputs: "EXACTLY_THREE_NON_HELD_OUT_ROUTES",
      evaluation_semantics: "FIRST_MATCH_WINS_IN_EVALUATION_ORDER",
      evaluation_order: ["any_non_held_out_unresolved", "any_non_held_out_material_evidence_conflict", "three_of_three_same_label", "two_of_three_same_label", "all_distinct_labels", "default_outcome"],
      any_non_held_out_unresolved: "LEAD_ADJUDICATION_REQUIRED",
      any_non_held_out_material_evidence_conflict: "LEAD_ADJUDICATION_REQUIRED",
      three_of_three_same_label: "PROVISIONAL_CONSENSUS",
      two_of_three_same_label: "PROVISIONAL_CONSENSUS",
      all_distinct_labels: "LEAD_ADJUDICATION_REQUIRED",
      default_outcome: "LEAD_ADJUDICATION_REQUIRED",
      held_out_exclusions: ["label", "evidence", "unresolved_state", "all_judgment_artifacts"],
      exclusion_applies_to: ["consensus", "conflict_detection", "lead_adjudication_inputs"]
    },
    score_classification: "NON_ISOLATED_EXPLORATORY",
    union_and_consensus: "DERIVED_OUTPUTS_NOT_MEASURED_MODEL_CALLS"
  });
  assert.equal(manifest.later_run_rules.some(rule => /later execution task directory, never in this frozen package/u.test(rule)), true, "later outputs excluded from frozen package");
  for (const entry of fs.readdirSync(here)) assert.equal(/^(?:RAW|ACQUISITION|CANDIDATE)-/u.test(entry), false, `${entry}: no later-run placeholder files`);

  const report = readJson(path.join(here, "BUILD-REPORT.json"));
  const experiment = readJson(path.join(here, "EXPERIMENT.json"));
  assert.equal(report.model_calls, 0); assert.equal(report.network_calls, 0);
  assert.equal(experiment.inference.model_calls, 0); assert.equal(experiment.inference.network_calls, 0);
  assert.equal(experiment.claims.responses_populated, false); assert.equal(experiment.claims.truth_labels_populated, false);
  assert.equal(Object.hasOwn(report.generated_artifacts, "BUILD-REPORT.json"), false, "report has no self hash");
  assert.equal(Object.hasOwn(report.generated_artifacts, "EXPERIMENT.json"), false, "report does not hash descendant");
  assert.equal(Object.hasOwn(experiment.frozen_outputs, "EXPERIMENT.json"), false, "experiment has no self hash");
  assert.equal(experiment.frozen_outputs["BUILD-REPORT.json"].sha256, frozenOutputHashes["BUILD-REPORT.json"]);
  for (const [name, record] of Object.entries(report.generated_artifacts)) assert.equal(record.sha256, frozenOutputHashes[name], `${name}: report hash DAG binding`);
  for (const [name, record] of Object.entries(experiment.frozen_outputs)) assert.equal(record.sha256, frozenOutputHashes[name], `${name}: experiment hash DAG binding`);

  process.stdout.write(`${JSON.stringify({status: "PASS", node: process.version, ajv: ajvVersion, counts: {queue_items: 145, shards: 5, items_per_shard: 29, schemas_compiled: 5, lanes: 4, responses: 0, model_calls: 0, network_calls: 0}, hashes: frozenOutputHashes}, null, 2)}\n`);
} finally {
  const expectedPrefix = `${path.resolve(os.tmpdir())}${path.sep}route-familiarity-reference-collection-v1-`;
  const resolved = path.resolve(temporaryDirectory);
  if (!resolved.startsWith(expectedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolved, {recursive: true, force: true});
}
