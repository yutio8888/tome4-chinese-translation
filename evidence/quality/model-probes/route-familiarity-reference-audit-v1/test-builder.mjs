#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import {createRequire} from "node:module";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {
  FROZEN,
  exactKeys,
  makeLocalRegistry,
  makeQueue,
  makeReferenceSchema,
  sha256,
  validateInputs
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
assert.match(ajvVersion, /^8\./u, "Ajv preflight must report major version 8");
const here = path.dirname(fileURLToPath(import.meta.url));
const queuePath = path.join(here, "OUTBOUND-AUDIT-QUEUE.json");
const schemaPath = path.join(here, "REFERENCE-SCHEMA.json");
const emittedQueue = JSON.parse(fs.readFileSync(queuePath, "utf8"));
const emittedSchema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const actualNeutralIds = emittedQueue.items.map(item => item.neutral_id);

const presentationRow = Object.freeze({
  neutral_id: "RFR-0001",
  category: "Runtime-focused",
  profile: "mechanics",
  source: "source",
  target: "target",
  bounded_fixed_context: "context"
});

function binding(overrides = {}) {
  return {
    neutral_id: "RFR-0001", task_id: "task", revision_key: "revision", profile: "mechanics", category: "Runtime-focused",
    historical_route_cell: "H1", hygiene_disposition: "MODEL_FACING", matched_hygiene_rule_ids: [],
    terminal_input: {logical_path: "input.json", sha256: "a".repeat(64), size_bytes: 1, dispatch_id: "dispatch", candidate_identity: "b".repeat(64), cycle: null, lifecycle: "archived", envelope_container: "modern", fixed_source_field: "fixed_source_commit"},
    identity_sha256: "c".repeat(64), source_sha256: sha256("source"), normalized_source_sha256: sha256("source"), target_sha256: sha256("target"), normalized_pair_sha256: "d".repeat(64),
    raw_context_sha256: sha256("context"), raw_context_size_bytes: 7, sanitized_context_sha256: sha256("context"), sanitized_context_size_bytes: 7,
    path_redaction_occurrences: 0, commit_neutralization_occurrences: 0, untouched_text_sha256: sha256("context"), ...overrides
  };
}

assert.throws(() => exactKeys({...presentationRow, route: "H1"}, Object.keys(presentationRow), "fixture"), /schema drift/u);
const queue = makeQueue({items: [presentationRow]});
assert.equal(queue.items.length, 1);
assert.deepEqual(Object.keys(queue.items[0]), ["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context", "response"]);
assert.equal(queue.items[0].response, null);
assert.equal(Object.hasOwn(queue.items[0], "historical_route_cell"), false);

const local = makeLocalRegistry(
  {items: [presentationRow]},
  {items: [binding()]},
  [binding()],
  {presentation: {}, source_binding_registry: {}, source_build_report: {}}
);
assert.equal(local.items[0].historical_route_cell, "H1");
assert.equal(local.outbound_allowed, false);
assert.equal(Object.hasOwn(queue.items[0], "task_id"), false);

assert.throws(() => makeReferenceSchema(), /binding malformed/u);
assert.throws(() => makeReferenceSchema("f".repeat(64)), /binding malformed/u);
const schema = makeReferenceSchema(sha256(fs.readFileSync(queuePath)), actualNeutralIds);
assert.deepEqual(schema, emittedSchema, "test must exercise the actual emitted schema");
assert.equal(schema.$schema, "https://json-schema.org/draft/2020-12/schema");
assert.deepEqual(schema.$defs.label.enum, ["CLEAN", "SURFACE_VISIBLE_DEFECT", "CONTEXT_DEPENDENT_DEFECT", "UNRESOLVED"]);
assert.equal(JSON.stringify(schema).includes('"label":"'), false, "schema must not populate a label");
assert.equal(schema.$defs.referenceResponse.additionalProperties, false);
assert.deepEqual(schema.$defs.referenceResponse.required, ["label", "evidence", "defect_atoms", "source_evidence_sha256s", "limitations"]);
assert.equal(schema.properties.queue_sha256.const, sha256(fs.readFileSync(queuePath)));
assert.equal(schema.properties.items.prefixItems.length, 145);
assert.equal(schema.properties.items.prefixItems[0].properties.neutral_id.const, "RFR-0001");
assert.equal(schema.properties.items.prefixItems[18].properties.neutral_id.const, "RFR-0020", "real corpus IDs must remain non-contiguous");
assert.equal(schema.properties.items.items, false);

const validateReference = new Ajv2020({allErrors: true, strict: true}).compile(emittedSchema);
const cleanResponse = {label: "CLEAN", evidence: "checked", defect_atoms: [], source_evidence_sha256s: [], limitations: ""};
const atom = {kind: "ACCURACY", claim: "bounded claim", evidence: "bounded evidence"};
function responseDocument(response = cleanResponse) {
  return {
    schema_version: "route-familiarity-reference-audit-responses-v1",
    status: "REFERENCE_AUDIT_COMPLETE",
    queue_sha256: emittedSchema.properties.queue_sha256.const,
    items: actualNeutralIds.map((neutral_id, index) => ({neutral_id, response: structuredClone(index === 0 ? response : cleanResponse)}))
  };
}
const accepts = response => validateReference(responseDocument(response));
const rejects = response => !validateReference(responseDocument(response));

assert.equal(accepts(cleanResponse), true);
assert.equal(rejects({...cleanResponse, defect_atoms: [atom]}), true);
assert.equal(accepts({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [atom], source_evidence_sha256s: [], limitations: ""}), true);
assert.equal(rejects({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [], source_evidence_sha256s: [], limitations: ""}), true);
assert.equal(accepts({label: "CONTEXT_DEPENDENT_DEFECT", evidence: "context", defect_atoms: [atom], source_evidence_sha256s: ["e".repeat(64)], limitations: ""}), true);
assert.equal(rejects({label: "CONTEXT_DEPENDENT_DEFECT", evidence: "context", defect_atoms: [atom], source_evidence_sha256s: [], limitations: ""}), true);
assert.equal(accepts({label: "UNRESOLVED", evidence: "insufficient", defect_atoms: [], source_evidence_sha256s: [], limitations: "missing source evidence"}), true);
assert.equal(rejects({label: "UNRESOLVED", evidence: "insufficient", defect_atoms: [], source_evidence_sha256s: [], limitations: ""}), true);
assert.equal(rejects({label: "MIXED_DEFECT", evidence: "x", defect_atoms: [atom], source_evidence_sha256s: [], limitations: ""}), true);
assert.equal(rejects({...cleanResponse, extra: true}), true);
assert.equal(rejects({...cleanResponse, evidence: " \t\n"}), true, "whitespace-only response evidence");
assert.equal(rejects({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [{...atom, claim: " \t"}], source_evidence_sha256s: [], limitations: ""}), true, "whitespace-only atom claim");
assert.equal(rejects({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [{...atom, evidence: "\n "}], source_evidence_sha256s: [], limitations: ""}), true, "whitespace-only atom evidence");
assert.equal(rejects({label: "UNRESOLVED", evidence: "insufficient", defect_atoms: [], source_evidence_sha256s: [], limitations: " \n"}), true, "whitespace-only unresolved limitations");
assert.equal(rejects({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [{...atom, claim: "x".repeat(241)}], source_evidence_sha256s: [], limitations: ""}), true, "atom claim upper bound");
assert.equal(rejects({label: "SURFACE_VISIBLE_DEFECT", evidence: "visible", defect_atoms: [{...atom, evidence: "x".repeat(481)}], source_evidence_sha256s: [], limitations: ""}), true, "atom evidence upper bound");

const wrongHash = responseDocument(); wrongHash.queue_sha256 = "0".repeat(64);
assert.equal(validateReference(wrongHash), false, "wrong queue hash");
const wrongOrder = responseDocument(); [wrongOrder.items[0], wrongOrder.items[1]] = [wrongOrder.items[1], wrongOrder.items[0]];
assert.equal(validateReference(wrongOrder), false, "wrong neutral-ID order");

const profileDefinitions = [["dialogue", "Dialogue", 61], ["mechanics", "Runtime-focused", 63], ["ui-log", "Runtime-focused", 7], ["unknown-text", "Unknown-text", 14]];
const fixtureProfiles = profileDefinitions.flatMap(([profile, category, count]) => Array.from({length: count}, () => ({profile, category})));
const fixturePresentation = {schema_version: "neutral-context-presentation-v1", status: "FROZEN_ZERO_INFERENCE_MODEL_FACING", counts: {}, items: Array.from({length: FROZEN.counts.items}, (_, index) => ({...presentationRow, ...fixtureProfiles[index], neutral_id: actualNeutralIds[index]}))};
const cells = ["H1", "H2", "H3", "H4"].flatMap(cell => Array(FROZEN.counts.historical_route_cells[cell]).fill(cell));
const fixtureBindings = fixturePresentation.items.map((row, index) => binding({neutral_id: row.neutral_id, task_id: `task-${index}`, revision_key: `revision-${index}`, profile: row.profile, category: row.category, historical_route_cell: cells[index]}));
const excludedBindings = Array.from({length: 11}, (_, index) => binding({neutral_id: `RFR-X${String(index).padStart(3, "0")}`, task_id: `excluded-task-${index}`, revision_key: `excluded-revision-${index}`, hygiene_disposition: "CONTEXT_META_PROVENANCE_EXCLUDED"}));
const fixtureRegistry = {production_translation_commit: FROZEN.production_translation_commit, items: [...fixtureBindings, ...excludedBindings]};
assert.equal(validateInputs(fixturePresentation, fixtureRegistry).length, 145);
const targetMutation = structuredClone(fixturePresentation); targetMutation.items[7].target = "mutated";
assert.throws(() => validateInputs(targetMutation, fixtureRegistry), /content binding drift/u);
const orderMutation = structuredClone(fixturePresentation); [orderMutation.items[0], orderMutation.items[1]] = [orderMutation.items[1], orderMutation.items[0]];
assert.throws(() => validateInputs(orderMutation, fixtureRegistry), /binding\/order metadata drift/u);

process.stdout.write("test-builder: PASS (queue isolation, exact bindings, and Ajv Draft 2020-12 response regressions)\n");
