#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import {createRequire} from "node:module";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {
  FROZEN,
  PROMPT,
  SHARD_COUNT,
  SHARD_SIZE,
  assertModelFacingHygiene,
  makeDerivationRules,
  makeManifest,
  makeResponseSchema,
  makeShards,
  sha256,
  validateManifest,
  validateQueueBindings,
  validateShardEvidence
} from "./build.mjs";

const require = createRequire(import.meta.url);

function loadAjv2020() {
  const prerequisite = "Ajv preflight failed: ajv/dist/2020 from Ajv major 8 is required; install Ajv 8 so it is resolvable before running schema-validation tests";
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

const {Ajv2020, version: ajvVersion} = loadAjv2020();
assert.match(ajvVersion, /^8\./u);
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../..");
const predecessor = path.join(root, "evidence/quality/model-probes/route-familiarity-reference-audit-v1");
const queue = JSON.parse(fs.readFileSync(path.join(predecessor, "OUTBOUND-AUDIT-QUEUE.json"), "utf8"));
const registry = JSON.parse(fs.readFileSync(path.join(predecessor, "LOCAL-BINDING-REGISTRY.json"), "utf8"));
const predecessorSchema = JSON.parse(fs.readFileSync(path.join(predecessor, "REFERENCE-SCHEMA.json"), "utf8"));
const shards = Array.from({length: SHARD_COUNT}, (_, index) => JSON.parse(fs.readFileSync(path.join(here, `OUTBOUND-SHARD-${String(index + 1).padStart(2, "0")}.json`), "utf8")));
const schemas = Array.from({length: SHARD_COUNT}, (_, index) => JSON.parse(fs.readFileSync(path.join(here, `RESPONSE-SCHEMA-SHARD-${String(index + 1).padStart(2, "0")}.json`), "utf8")));
const manifest = JSON.parse(fs.readFileSync(path.join(here, "LOCAL-ROUTE-MANIFEST.json"), "utf8"));
const report = JSON.parse(fs.readFileSync(path.join(here, "BUILD-REPORT.json"), "utf8"));
const generated = report.generated_artifacts;

validateQueueBindings(queue, registry);
assert.deepEqual(makeShards(queue), shards, "baseline shards");
assertModelFacingHygiene(shards);
assertModelFacingHygiene(PROMPT, {prompt: true});
for (const shard of shards) validateShardEvidence(shard);
for (const schema of schemas) assertModelFacingHygiene(schema, {allowLabelVocabulary: true});
validateManifest(manifest, generated);

for (const field of ["source", "target", "bounded_fixed_context"]) {
  const mutation = structuredClone(queue);
  mutation.items[0][field] = `${mutation.items[0][field]} MUTATION`;
  assert.throws(() => validateQueueBindings(mutation, registry), new RegExp(`${field} content binding drift`, "u"), `${field} mutation`);
}

for (const injection of ["H2", "OpenAI", "/home/example/private.json", "local provenance", "sealed reference"]) {
  const mutation = structuredClone(shards[0]);
  mutation.items[0].bounded_fixed_context = injection;
  assert.throws(() => assertModelFacingHygiene(mutation), /leak/u, `outbound hygiene ${injection}`);
  assert.throws(() => assertModelFacingHygiene(`${PROMPT}\n${injection}`, {prompt: true}), /leak/u, `prompt hygiene ${injection}`);
}
assert.doesNotThrow(() => assertModelFacingHygiene(`${PROMPT}\nCLEAN means no material defect.`, {prompt: true}), "label definitions are allowed");
assert.throws(() => assertModelFacingHygiene(`${PROMPT}\n{"label":"CLEAN"}`, {prompt: true}), /populated-answer structure/u);
assert.doesNotThrow(() => assertModelFacingHygiene(schemas[0], {allowLabelVocabulary: true}), "schema label vocabulary is allowed");
for (const injection of ["H3", "Anthropic", "/tmp/private.json", "local binding registry", "prior adjudication"]) {
  const schemaMutation = structuredClone(schemas[0]);
  schemaMutation.description = injection;
  assert.throws(() => assertModelFacingHygiene(schemaMutation, {allowLabelVocabulary: true}), /leak/u, `schema hygiene ${injection}`);
}

const missingEvidence = structuredClone(shards[0]); missingEvidence.source_evidence.pop();
assert.throws(() => validateShardEvidence(missingEvidence), /evidence count drift/u, "missing evidence record");
const reorderedEvidence = structuredClone(shards[0]); [reorderedEvidence.source_evidence[0], reorderedEvidence.source_evidence[1]] = [reorderedEvidence.source_evidence[1], reorderedEvidence.source_evidence[0]];
assert.throws(() => validateShardEvidence(reorderedEvidence), /item alignment drift/u, "reordered evidence records");
const tamperedEvidence = structuredClone(shards[0]); tamperedEvidence.source_evidence[0].evidence_id = "EVIDENCE-RFR-9999";
assert.throws(() => validateShardEvidence(tamperedEvidence), /item alignment drift/u, "tampered evidence identity");
const textDrift = structuredClone(shards[0]); textDrift.source_evidence[0].text += " MUTATION";
assert.throws(() => validateShardEvidence(textDrift), /text binding drift/u, "evidence text drift");
const hashDrift = structuredClone(shards[0]); hashDrift.source_evidence[0].sha256 = "0".repeat(64);
assert.throws(() => validateShardEvidence(hashDrift), /UTF-8 hash binding drift/u, "evidence hash drift");

const manifestDrift = structuredClone(manifest);
manifestDrift.lanes[1].bindings[0].shard_sha256 = "0".repeat(64);
assert.throws(() => validateManifest(manifestDrift, generated), /lane binding drift/u, "route-manifest lane drift");

const orderDrift = structuredClone(manifest);
[orderDrift.derivation_rules.evaluation_order[0], orderDrift.derivation_rules.evaluation_order[2]] = [orderDrift.derivation_rules.evaluation_order[2], orderDrift.derivation_rules.evaluation_order[0]];
assert.throws(() => validateManifest(orderDrift, generated), /ordered derivation rule drift/u, "four-route adjudication precedence drift");
const leaveOneOutDefaultDrift = structuredClone(manifest);
delete leaveOneOutDefaultDrift.derivation_rules.leave_one_route_out.default_outcome;
assert.throws(() => validateManifest(leaveOneOutDefaultDrift, generated), /ordered derivation rule drift/u, "leave-one-route-out default drift");

function evaluateLabelPattern(rules, labels, materialEvidenceConflict = false) {
  const counts = new Map();
  for (const label of labels) counts.set(label, (counts.get(label) ?? 0) + 1);
  const matches = {
    any_unresolved: labels.includes("UNRESOLVED"),
    any_material_evidence_conflict: materialEvidenceConflict,
    unanimous_or_three_of_four: labels.length === 4 && Math.max(...counts.values()) >= 3,
    two_two_split: labels.length === 4 && [...counts.values()].sort().join(",") === "2,2",
    any_non_held_out_unresolved: labels.includes("UNRESOLVED"),
    any_non_held_out_material_evidence_conflict: materialEvidenceConflict,
    three_of_three_same_label: labels.length === 3 && counts.size === 1,
    two_of_three_same_label: labels.length === 3 && Math.max(...counts.values()) === 2,
    all_distinct_labels: labels.length === 3 && counts.size === 3,
    default_outcome: true
  };
  const matchedRule = rules.evaluation_order.find(rule => matches[rule]);
  return {matchedRule, outcome: rules[matchedRule]};
}

const expectedDerivationRules = makeDerivationRules();
assert.deepEqual(manifest.derivation_rules, expectedDerivationRules, "exact ordered derivation rules");
assert.deepEqual(evaluateLabelPattern(expectedDerivationRules.leave_one_route_out, ["CLEAN", "CLEAN", "UNRESOLVED"]), {matchedRule: "any_non_held_out_unresolved", outcome: "LEAD_ADJUDICATION_REQUIRED"});
assert.deepEqual(evaluateLabelPattern(expectedDerivationRules.leave_one_route_out, ["UNRESOLVED", "UNRESOLVED", "CLEAN"]), {matchedRule: "any_non_held_out_unresolved", outcome: "LEAD_ADJUDICATION_REQUIRED"});
assert.deepEqual(evaluateLabelPattern(expectedDerivationRules.leave_one_route_out, ["CLEAN", "CLEAN", "SURFACE_VISIBLE_DEFECT"]), {matchedRule: "two_of_three_same_label", outcome: "PROVISIONAL_CONSENSUS"});
assert.deepEqual(evaluateLabelPattern(expectedDerivationRules, ["CLEAN", "CLEAN", "SURFACE_VISIBLE_DEFECT", "CONTEXT_DEPENDENT_DEFECT"]), {matchedRule: "default_outcome", outcome: "LEAD_ADJUDICATION_REQUIRED"});
assert.deepEqual(evaluateLabelPattern(expectedDerivationRules, ["CLEAN", "CLEAN", "CLEAN", "SURFACE_VISIBLE_DEFECT"], true), {matchedRule: "any_material_evidence_conflict", outcome: "LEAD_ADJUDICATION_REQUIRED"});

const clean = {label: "CLEAN", evidence: "checked", defect_atoms: [], source_evidence_sha256s: [], limitations: ""};
const atom = {kind: "ACCURACY", claim: "bounded claim", evidence: "bounded evidence"};

for (let index = 0; index < SHARD_COUNT; index += 1) {
  const schema = schemas[index];
  const shard = shards[index];
  const ids = shard.items.map(item => item.neutral_id);
  const shardBytes = fs.readFileSync(path.join(here, `OUTBOUND-SHARD-${String(index + 1).padStart(2, "0")}.json`));
  const shardHash = sha256(shardBytes);
  assert.deepEqual(schema.$defs, predecessorSchema.$defs, `${shard.shard_id}: predecessor definitions reused exactly`);
  const evidenceHashes = shard.source_evidence.map(evidence => evidence.sha256);
  assert.deepEqual(makeResponseSchema({index, shardSha256: shardHash, neutralIds: ids, evidenceSha256s: evidenceHashes, predecessorDefs: predecessorSchema.$defs}), schema, `${shard.shard_id}: baseline schema`);
  const validate = new Ajv2020({allErrors: true, strict: true}).compile(schema);
  const document = response => ({
    schema_version: "route-familiarity-reference-collection-responses-v1",
    status: "REFERENCE_COLLECTION_COMPLETE",
    parent_queue_sha256: FROZEN.inputs.queue.sha256,
    shard_id: shard.shard_id,
    shard_file_sha256: shardHash,
    item_count: SHARD_SIZE,
    item_ids: [...ids],
    items: ids.map((neutral_id, itemIndex) => ({neutral_id, response: structuredClone(itemIndex === 0 ? response : clean)}))
  });
  assert.equal(validate(document(clean)), true, `${shard.shard_id}: clean baseline`);

  const wrongShardHash = document(clean); wrongShardHash.shard_file_sha256 = "0".repeat(64);
  assert.equal(validate(wrongShardHash), false, `${shard.shard_id}: wrong shard hash`);
  const wrongParentHash = document(clean); wrongParentHash.parent_queue_sha256 = "0".repeat(64);
  assert.equal(validate(wrongParentHash), false, `${shard.shard_id}: wrong parent hash`);
  const swapped = document(clean); [swapped.items[0], swapped.items[1]] = [swapped.items[1], swapped.items[0]];
  assert.equal(validate(swapped), false, `${shard.shard_id}: swapped item order`);
  const swappedIds = document(clean); [swappedIds.item_ids[0], swappedIds.item_ids[1]] = [swappedIds.item_ids[1], swappedIds.item_ids[0]];
  assert.equal(validate(swappedIds), false, `${shard.shard_id}: swapped ID binding`);
  const short = document(clean); short.items.pop();
  assert.equal(validate(short), false, `${shard.shard_id}: 28 items`);
  const long = document(clean); long.items.push(structuredClone(long.items[0]));
  assert.equal(validate(long), false, `${shard.shard_id}: 30 items`);
  const extra = document(clean); extra.items[0].response.extra = true;
  assert.equal(validate(extra), false, `${shard.shard_id}: unknown response field`);
  const extraTop = document(clean); extraTop.extra = true;
  assert.equal(validate(extraTop), false, `${shard.shard_id}: unknown document field`);
  const unknownLabel = document({...clean, label: "UNKNOWN"});
  assert.equal(validate(unknownLabel), false, `${shard.shard_id}: unknown label`);
  const whitespaceEvidence = document({...clean, evidence: " \t\n"});
  assert.equal(validate(whitespaceEvidence), false, `${shard.shard_id}: whitespace evidence`);
  assert.equal(validate(document({...clean, defect_atoms: [atom]})), false, `${shard.shard_id}: CLEAN branch`);
  assert.equal(validate(document({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [], source_evidence_sha256s: [], limitations: ""})), false, `${shard.shard_id}: surface branch`);
  assert.equal(validate(document({label: "CONTEXT_DEPENDENT_DEFECT", evidence: "context", defect_atoms: [atom], source_evidence_sha256s: [], limitations: ""})), false, `${shard.shard_id}: context branch`);
  const contextDependent = {label: "CONTEXT_DEPENDENT_DEFECT", evidence: "context establishes the defect", defect_atoms: [atom], source_evidence_sha256s: [evidenceHashes[0]], limitations: ""};
  assert.equal(validate(document(contextDependent)), true, `${shard.shard_id}: direct positive context-dependent fixture`);
  assert.equal(validate(document({...contextDependent, source_evidence_sha256s: ["0".repeat(64)]})), false, `${shard.shard_id}: all-zero unknown evidence hash`);
  assert.equal(validate(document({...contextDependent, source_evidence_sha256s: ["f".repeat(64)]})), false, `${shard.shard_id}: unknown evidence hash`);
  assert.equal(validate(document({...contextDependent, source_evidence_sha256s: [evidenceHashes[1]]})), false, `${shard.shard_id}: another item's evidence hash`);
  assert.equal(validate(document({label: "UNRESOLVED", evidence: "insufficient", defect_atoms: [], source_evidence_sha256s: [], limitations: " \n"})), false, `${shard.shard_id}: unresolved branch`);
}

process.stdout.write(`test-builder: PASS (${SHARD_COUNT} schemas; ordered derivation precedence/default semantics; positive context-dependent fixtures; focused metadata/evidence/hash/order/count/field/branch/hygiene/binding mutations; Ajv ${ajvVersion})\n`);
