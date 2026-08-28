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
const sourceDirectory = path.join(root, "evidence/quality/model-probes/route-familiarity-runtime-expansion-v1");
const generatedNames = ["OUTBOUND-AUDIT-QUEUE.json", "LOCAL-BINDING-REGISTRY.json", "REFERENCE-SCHEMA.json", "BUILD-REPORT.json", "EXPERIMENT.json"];
const frozenInputs = {
  "FUTURE-MODEL-CANDIDATES.json": "6e8b2a3b485418fca4bdb9d777f4a7a572f0f872efdb27905e52080a23e11084",
  "TERMINAL-IDENTITY-BINDING-REGISTRY.json": "9cc58a068801a707be0eca32a2597493d8fb2b6d64e37914355ac9cd2552d436",
  "BUILD-REPORT.json": "a0eeb216c4412f0dbb0ef3fcef1302294c09ea0c757a771cc21e280fff1fda2c"
};
const frozenOutputHashes = {
  "OUTBOUND-AUDIT-QUEUE.json": "620b736996ac254c43b3c721cdbfca20f7e68d8f553b7fe21b9effa0c025b3d2",
  "LOCAL-BINDING-REGISTRY.json": "64013413c5a30956185a7a71c2b21d7960a6b2ddda55e9c709657fe10ac3a7a1",
  "REFERENCE-SCHEMA.json": "c197e30ebaaae353df58049c2f3479dc2a0c799d3633dba4e70b5db27f859f34",
  "BUILD-REPORT.json": "b0ae5be212af39f0c33f8a39661dc8a9f3d7f2a2731f392f72530977501f52cc",
  "EXPERIMENT.json": "e6a948f0d6e32dcbbc16f3482e78bd087db1476ff42c5011f7f2f263c5841201"
};
const executorFixture = path.join(root, "evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua");
const fixtureHash = "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7";
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
const sorted = value => [...value].sort((left, right) => left < right ? -1 : left > right ? 1 : 0);
const exactKeys = (value, keys, label) => assert.deepEqual(sorted(Object.keys(value)), sorted(keys), `${label}: exact keys`);
const countBy = (items, field) => Object.fromEntries(sorted(new Set(items.map(item => item[field]))).map(value => [value, items.filter(item => item[field] === value).length]));

function allStrings(value, pointer = "") {
  if (typeof value === "string") return [{pointer, value}];
  if (Array.isArray(value)) return value.flatMap((entry, index) => allStrings(entry, `${pointer}/${index}`));
  if (value && typeof value === "object") return Object.entries(value).flatMap(([key, entry]) => allStrings(entry, `${pointer}/${key}`));
  return [];
}

const forbidden = [
  ["route cell", /\bH[1-4]\b/u],
  ["provenance-like hash", /\b(?:[0-9a-f]{12,64}|(?=[0-9a-f]{7,11}\b)(?=[0-9a-f]*[0-9])[0-9a-f]{7,11})\b/iu],
  ["provider/model", /\b(?:OpenAI|Anthropic|Google|Z\.ai(?:\s+CN)?|Codex|(?:Gemini|Grok|GLM|Qwen|GPT)(?:[._-]?\d[A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*)?|Claude(?:[._-](?:Opus|Sonnet|Haiku)(?:[._-]?\d[A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*)?)?|Opus)\b(?![._-])/iu],
  ["internal typed identity", /\b(?:task|revision|dispatch|review)[_ -]?(?:id|key)\b/iu],
  ["review/adjudication history", /(?:already[- ]accepted|already reviewed|review correctly flagged|senior[- ]audit|adjudicat(?:e|ed|ion)|defect[_ -]?id)/iu],
  ["local absolute path", /(?:\/home\/|\/Users\/|\/tmp\/|\/private\/|\/srv\/|\/mnt\/|[A-Za-z]:[\\/](?:Users|home|work)[\\/]|\\\\[^\\]+\\[^\\]+)/u],
  ["reference truth label", /\b(?:CLEAN|SURFACE_VISIBLE_DEFECT|CONTEXT_DEPENDENT_DEFECT|UNRESOLVED)\b/u]
];

function assertPatternRegression(label, pattern, positives, negatives) {
  for (const value of positives) assert.equal(pattern.test(value), true, `${label}: missed positive probe ${value}`);
  for (const value of negatives) assert.equal(pattern.test(value), false, `${label}: rejected negative probe ${value}`);
}

assertPatternRegression("provenance-like hash", forbidden[1][1], ["0ea3fcd", "1666481", "deadbe1", "a".repeat(40), "b".repeat(50), "c".repeat(64)], ["deadbe", "defaced", "effaced", "acceded", "deadbee", "cafebabe", "g".repeat(40), "a".repeat(65)]);
assertPatternRegression("provider/model", forbidden[2][1], ["Qwen3-8-27B", "GPT-5.6-sol", "OpenAI", "Anthropic", "Z.ai CN", "GLM-4.5", "Google", "Gemini-3.7-flash-high", "Grok-4.6", "Claude-Opus-4.1", "claude-opus-5", "Codex"], ["open air", "geminal", "glimmer", "model route", "opuscule", "Opusculum", "grokking", "qwenty", "Google-like"]);

const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "route-familiarity-reference-audit-v1-"));
try {
  buildPackage({root, out: temporaryDirectory});
  for (const name of generatedNames) {
    const committed = fs.readFileSync(path.join(here, name));
    const rebuilt = fs.readFileSync(path.join(temporaryDirectory, name));
    assert.deepEqual(rebuilt, committed, `${name}: byte-for-byte rebuild`);
    assert.equal(sha256(committed), frozenOutputHashes[name], `${name}: frozen output hash`);
    JSON.parse(committed.toString("utf8"));
  }

  for (const [name, expected] of Object.entries(frozenInputs)) assert.equal(sha256(fs.readFileSync(path.join(sourceDirectory, name))), expected, `${name}: frozen predecessor hash`);
  assert.equal(sha256(fs.readFileSync(executorFixture)), fixtureHash, "executor fixture hash");

  const sourcePresentation = readJson(path.join(sourceDirectory, "FUTURE-MODEL-CANDIDATES.json"));
  const sourceRegistry = readJson(path.join(sourceDirectory, "TERMINAL-IDENTITY-BINDING-REGISTRY.json"));
  const queue = readJson(path.join(here, "OUTBOUND-AUDIT-QUEUE.json"));
  const localRegistry = readJson(path.join(here, "LOCAL-BINDING-REGISTRY.json"));
  const schema = readJson(path.join(here, "REFERENCE-SCHEMA.json"));
  const report = readJson(path.join(here, "BUILD-REPORT.json"));
  const experiment = readJson(path.join(here, "EXPERIMENT.json"));

  exactKeys(queue, ["schema_version", "status", "inference_allowed", "presentation_order", "response_contract", "counts", "items"], "queue");
  assert.equal(queue.inference_allowed, false);
  assert.equal(queue.items.length, 145);
  assert.equal(new Set(queue.items.map(item => item.neutral_id)).size, 145);
  assert.deepEqual(queue.items.map(item => item.neutral_id), sourcePresentation.items.map(item => item.neutral_id), "presentation order");
  const allowedItemKeys = ["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context", "response"];
  for (let index = 0; index < queue.items.length; index += 1) {
    const row = queue.items[index];
    const source = sourcePresentation.items[index];
    exactKeys(row, allowedItemKeys, `queue.items[${index}]`);
    assert.equal(row.response, null, `${row.neutral_id}: response must remain unfilled`);
    for (const field of ["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context"]) assert.equal(row[field], source[field], `${row.neutral_id}: ${field} byte/order drift`);
  }
  assert.deepEqual(queue.counts, {items: 145, profiles: {dialogue: 61, mechanics: 63, "ui-log": 7, "unknown-text": 14}, categories: {Dialogue: 61, "Runtime-focused": 70, "Unknown-text": 14}, populated_responses: 0});

  for (const {pointer, value} of allStrings(queue)) for (const [label, pattern] of forbidden) assert.equal(pattern.test(value), false, `${pointer}: outbound ${label} leak`);

  assert.equal(localRegistry.items.length, 145);
  assert.equal(localRegistry.outbound_allowed, false);
  assert.deepEqual(localRegistry.items.map(item => item.neutral_id), queue.items.map(item => item.neutral_id));
  assert.deepEqual(countBy(localRegistry.items, "historical_route_cell"), {H1: 112, H2: 14, H3: 11, H4: 8});
  const retained = sourceRegistry.items.filter(item => item.hygiene_disposition === "MODEL_FACING");
  for (let index = 0; index < retained.length; index += 1) {
    const source = retained[index];
    const local = localRegistry.items[index];
    assert.equal(local.presentation_ordinal, index + 1);
    assert.equal(local.source_registry_ordinal, sourceRegistry.items.indexOf(source) + 1);
    for (const field of ["neutral_id", "historical_route_cell", "task_id", "revision_key", "identity_sha256", "source_sha256", "target_sha256"]) assert.equal(local[field], source[field], `${local.neutral_id}: local ${field} drift`);
    assert.equal(local.bounded_fixed_context_sha256, source.sanitized_context_sha256);
    assert.equal(local.bounded_fixed_context_size_bytes, source.sanitized_context_size_bytes);
    assert.equal(sha256(queue.items[index].source), local.source_sha256);
    assert.equal(sha256(queue.items[index].target), local.target_sha256);
    assert.equal(sha256(queue.items[index].bounded_fixed_context), local.bounded_fixed_context_sha256);
  }

  exactKeys(schema, ["$schema", "$id", "title", "type", "additionalProperties", "required", "properties", "$defs"], "reference schema");
  assert.equal(schema.$schema, "https://json-schema.org/draft/2020-12/schema");
  assert.equal(schema.additionalProperties, false);
  assert.deepEqual(schema.$defs.label.enum, ["CLEAN", "SURFACE_VISIBLE_DEFECT", "CONTEXT_DEPENDENT_DEFECT", "UNRESOLVED"]);
  assert.equal(new Set(schema.$defs.label.enum).size, 4);
  assert.equal(schema.$defs.referenceResponse.additionalProperties, false);
  assert.equal(schema.$defs.referenceItem.additionalProperties, false);
  assert.equal(schema.properties.items.minItems, 145);
  assert.equal(schema.properties.items.maxItems, 145);
  assert.equal(schema.properties.queue_sha256.const, frozenOutputHashes["OUTBOUND-AUDIT-QUEUE.json"]);
  assert.equal(schema.properties.items.prefixItems.length, 145);
  assert.deepEqual(schema.properties.items.prefixItems.map(item => item.properties.neutral_id.const), queue.items.map(item => item.neutral_id));
  assert.equal(schema.properties.items.items, false);
  assert.equal(schema.$defs.referenceResponse.allOf.length, 4);
  assert.equal(JSON.stringify(schema).includes('"label":"'), false, "reference schema populated a truth label");
  assert.equal(queue.items.every(item => item.response === null), true);
  const {Ajv2020} = loadAjv2020();
  const validateReference = new Ajv2020({allErrors: true, strict: true}).compile(schema);
  const cleanResponse = {label: "CLEAN", evidence: "checked", defect_atoms: [], source_evidence_sha256s: [], limitations: ""};
  assert.equal(validateReference({
    schema_version: "route-familiarity-reference-audit-responses-v1",
    status: "REFERENCE_AUDIT_COMPLETE",
    queue_sha256: frozenOutputHashes["OUTBOUND-AUDIT-QUEUE.json"],
    items: queue.items.map(item => ({neutral_id: item.neutral_id, response: cleanResponse}))
  }), true, "emitted Draft 2020-12 schema validation");

  assert.equal(report.status, "PASS_ZERO_INFERENCE_REFERENCE_FREEZE_GATES");
  assert.equal(report.model_calls, 0); assert.equal(report.network_calls, 0);
  for (const name of generatedNames.slice(0, 3)) assert.equal(report.generated_artifacts[name].sha256, frozenOutputHashes[name]);
  assert.equal(experiment.frozen_outputs["BUILD-REPORT.json"].sha256, frozenOutputHashes["BUILD-REPORT.json"]);
  assert.equal(experiment.inference.model_calls, 0); assert.equal(experiment.inference.network_calls, 0);
  assert.equal(experiment.claims.truth_labels_populated, false);

  process.stdout.write(`${JSON.stringify({status: "PASS", deterministic_outputs: generatedNames, counts: queue.counts, hashes: frozenOutputHashes}, null, 2)}\n`);
} finally {
  const expectedPrefix = `${path.resolve(os.tmpdir())}${path.sep}route-familiarity-reference-audit-v1-`;
  const resolved = path.resolve(temporaryDirectory);
  if (!resolved.startsWith(expectedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolved, {recursive: true, force: true});
}
