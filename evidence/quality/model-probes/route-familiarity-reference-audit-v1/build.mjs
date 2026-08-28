#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");

export const GENERATED_NAMES = Object.freeze([
  "OUTBOUND-AUDIT-QUEUE.json",
  "LOCAL-BINDING-REGISTRY.json",
  "REFERENCE-SCHEMA.json",
  "BUILD-REPORT.json",
  "EXPERIMENT.json"
]);

export const FROZEN = Object.freeze({
  production_translation_commit: "1666481409f4c0d63d66e84659f6b6145d8d25d0",
  inputs: {
    presentation: {
      logical_path: "evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/FUTURE-MODEL-CANDIDATES.json",
      sha256: "6e8b2a3b485418fca4bdb9d777f4a7a572f0f872efdb27905e52080a23e11084"
    },
    source_binding_registry: {
      logical_path: "evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/TERMINAL-IDENTITY-BINDING-REGISTRY.json",
      sha256: "9cc58a068801a707be0eca32a2597493d8fb2b6d64e37914355ac9cd2552d436"
    },
    source_build_report: {
      logical_path: "evidence/quality/model-probes/route-familiarity-runtime-expansion-v1/BUILD-REPORT.json",
      sha256: "a0eeb216c4412f0dbb0ef3fcef1302294c09ea0c757a771cc21e280fff1fda2c"
    },
    executor_fixture: {
      logical_path: "evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua",
      sha256: "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7"
    }
  },
  counts: {
    items: 145,
    profiles: {dialogue: 61, mechanics: 63, "ui-log": 7, "unknown-text": 14},
    categories: {Dialogue: 61, "Runtime-focused": 70, "Unknown-text": 14},
    historical_route_cells: {H1: 112, H2: 14, H3: 11, H4: 8}
  }
});

const SHA256_RE = /^[0-9a-f]{64}$/u;
const QUEUE_ITEM_KEYS = Object.freeze(["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context", "response"]);
const PRESENTATION_ITEM_KEYS = Object.freeze(["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context"]);
const SOURCE_BINDING_KEYS = Object.freeze([
  "neutral_id", "task_id", "revision_key", "profile", "category", "historical_route_cell",
  "hygiene_disposition", "matched_hygiene_rule_ids", "terminal_input", "identity_sha256",
  "source_sha256", "normalized_source_sha256", "target_sha256", "normalized_pair_sha256",
  "raw_context_sha256", "raw_context_size_bytes", "sanitized_context_sha256",
  "sanitized_context_size_bytes", "path_redaction_occurrences",
  "commit_neutralization_occurrences", "untouched_text_sha256"
]);

const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
export const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const fileRecord = bytes => ({sha256: sha256(bytes), size_bytes: bytes.length});
const compareCodepoints = (left, right) => left < right ? -1 : left > right ? 1 : 0;

export function exactKeys(value, expected, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: object required`);
  const actual = Object.keys(value).sort(compareCodepoints);
  const wanted = [...expected].sort(compareCodepoints);
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) throw new Error(`${label}: exact-key schema drift`);
}

function parseArgs(argv) {
  const args = {root: defaultRoot, out: here};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!new Set(["--root", "--out"]).has(flag) || !value) throw new Error("usage: node build.mjs [--root REPO] [--out OUTPUT_DIR]");
    args[flag.slice(2)] = path.resolve(value);
  }
  return args;
}

function readPinned(root, name) {
  const pin = FROZEN.inputs[name];
  const bytes = fs.readFileSync(path.join(root, pin.logical_path));
  if (sha256(bytes) !== pin.sha256) throw new Error(`${name}: frozen input hash drift`);
  const value = pin.logical_path.endsWith(".json") ? JSON.parse(bytes.toString("utf8")) : null;
  return {value, record: {...pin, size_bytes: bytes.length}};
}

function countBy(items, field) {
  return Object.fromEntries([...new Set(items.map(item => item[field]))].sort(compareCodepoints).map(value => [value, items.filter(item => item[field] === value).length]));
}

function taskCountsBy(items, field) {
  return Object.fromEntries([...new Set(items.map(item => item[field]))].sort(compareCodepoints).map(value => [value, new Set(items.filter(item => item[field] === value).map(item => item.task_id)).size]));
}

export function validateInputs(presentation, sourceRegistry) {
  exactKeys(presentation, ["schema_version", "status", "counts", "items"], "presentation");
  if (presentation.schema_version !== "neutral-context-presentation-v1" || presentation.status !== "FROZEN_ZERO_INFERENCE_MODEL_FACING") throw new Error("presentation identity drift");
  if (!Array.isArray(presentation.items) || presentation.items.length !== FROZEN.counts.items) throw new Error("presentation row count drift");
  if (!Array.isArray(sourceRegistry.items) || sourceRegistry.items.length !== 156) throw new Error("source registry row count drift");
  if (sourceRegistry.production_translation_commit !== FROZEN.production_translation_commit) throw new Error("production translation commit drift");
  const retained = sourceRegistry.items.filter(item => item.hygiene_disposition === "MODEL_FACING");
  if (retained.length !== FROZEN.counts.items) throw new Error("retained binding count drift");
  const ids = new Set();
  for (let index = 0; index < presentation.items.length; index += 1) {
    const row = presentation.items[index];
    const binding = retained[index];
    exactKeys(row, PRESENTATION_ITEM_KEYS, `presentation.items[${index}]`);
    exactKeys(binding, SOURCE_BINDING_KEYS, `sourceRegistry.items[${sourceRegistry.items.indexOf(binding)}]`);
    if (!/^RFR-[0-9]{4}$/u.test(row.neutral_id) || ids.has(row.neutral_id)) throw new Error(`${row.neutral_id}: malformed or duplicate neutral ID`);
    ids.add(row.neutral_id);
    if (row.neutral_id !== binding.neutral_id || row.category !== binding.category || row.profile !== binding.profile) throw new Error(`${row.neutral_id}: binding/order metadata drift`);
    if (sha256(row.source) !== binding.source_sha256 || sha256(row.target) !== binding.target_sha256 || sha256(row.bounded_fixed_context) !== binding.sanitized_context_sha256) throw new Error(`${row.neutral_id}: byte-exact content binding drift`);
    if (!/^H[1-4]$/u.test(binding.historical_route_cell)) throw new Error(`${row.neutral_id}: invalid historical route cell`);
    for (const field of ["identity_sha256", "source_sha256", "target_sha256", "sanitized_context_sha256"]) if (!SHA256_RE.test(binding[field])) throw new Error(`${row.neutral_id}: invalid ${field}`);
  }
  for (const [field, expected] of [["profile", FROZEN.counts.profiles], ["category", FROZEN.counts.categories]]) {
    if (JSON.stringify(countBy(presentation.items, field)) !== JSON.stringify(expected)) throw new Error(`${field} counts drift`);
  }
  if (JSON.stringify(countBy(retained, "historical_route_cell")) !== JSON.stringify(FROZEN.counts.historical_route_cells)) throw new Error("historical route-cell counts drift");
  return retained;
}

export function makeQueue(presentation) {
  return {
    schema_version: "route-familiarity-reference-audit-queue-v1",
    status: "FROZEN_ZERO_INFERENCE_UNPOPULATED",
    inference_allowed: false,
    presentation_order: "SOURCE_PRESENTATION_BYTE_ORDER",
    response_contract: {
      schema_path: "REFERENCE-SCHEMA.json#/$defs/referenceResponse",
      slot: "response",
      unfilled_value: null
    },
    counts: {
      items: presentation.items.length,
      profiles: countBy(presentation.items, "profile"),
      categories: countBy(presentation.items, "category"),
      populated_responses: 0
    },
    items: presentation.items.map(row => ({...row, response: null}))
  };
}

export function makeLocalRegistry(presentation, sourceRegistry, retained, inputRecords) {
  const sourceOrdinals = new Map(sourceRegistry.items.map((item, index) => [item.neutral_id, index + 1]));
  return {
    schema_version: "route-familiarity-reference-audit-local-binding-registry-v1",
    status: "FROZEN_LOCAL_ONLY_NO_TRUTH",
    outbound_allowed: false,
    production_translation_commit: FROZEN.production_translation_commit,
    source_package: {
      presentation: inputRecords.presentation,
      binding_registry: inputRecords.source_binding_registry,
      build_report: inputRecords.source_build_report
    },
    counts: {
      items: retained.length,
      tasks: new Set(retained.map(item => item.task_id)).size,
      profiles: countBy(retained, "profile"),
      profile_tasks: taskCountsBy(retained, "profile"),
      categories: countBy(retained, "category"),
      category_tasks: taskCountsBy(retained, "category"),
      historical_route_cells: countBy(retained, "historical_route_cell"),
      historical_route_cell_tasks: taskCountsBy(retained, "historical_route_cell")
    },
    order_binding: {
      rule: "presentation ordinal equals retained MODEL_FACING source-registry order",
      neutral_id_order_sha256: sha256(presentation.items.map(item => item.neutral_id).join("\n")),
      source_order_sha256: sha256(presentation.items.map(item => item.source).join("\0")),
      target_order_sha256: sha256(presentation.items.map(item => item.target).join("\0")),
      bounded_fixed_context_order_sha256: sha256(presentation.items.map(item => item.bounded_fixed_context).join("\0"))
    },
    items: retained.map((binding, index) => ({
      neutral_id: binding.neutral_id,
      presentation_ordinal: index + 1,
      source_registry_ordinal: sourceOrdinals.get(binding.neutral_id),
      historical_route_cell: binding.historical_route_cell,
      task_id: binding.task_id,
      revision_key: binding.revision_key,
      source_terminal_input: {
        logical_path: binding.terminal_input.logical_path,
        sha256: binding.terminal_input.sha256,
        dispatch_id: binding.terminal_input.dispatch_id,
        candidate_identity: binding.terminal_input.candidate_identity
      },
      identity_sha256: binding.identity_sha256,
      source_sha256: binding.source_sha256,
      target_sha256: binding.target_sha256,
      bounded_fixed_context_sha256: binding.sanitized_context_sha256,
      bounded_fixed_context_size_bytes: binding.sanitized_context_size_bytes
    }))
  };
}

export function makeReferenceSchema(queueSha256, neutralIds) {
  if (!SHA256_RE.test(queueSha256) || !Array.isArray(neutralIds) || neutralIds.length !== 145 || new Set(neutralIds).size !== 145 || neutralIds.some(value => !/^RFR-[0-9]{4}$/u.test(value))) throw new Error("reference schema binding malformed");
  return {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $id: "route-familiarity-reference-audit-v1/REFERENCE-SCHEMA.json",
    title: "Route-familiarity reference audit responses",
    type: "object",
    additionalProperties: false,
    required: ["schema_version", "status", "queue_sha256", "items"],
    properties: {
      schema_version: {const: "route-familiarity-reference-audit-responses-v1"},
      status: {const: "REFERENCE_AUDIT_COMPLETE"},
      queue_sha256: {const: queueSha256},
      items: {
        type: "array",
        minItems: 145,
        maxItems: 145,
        prefixItems: neutralIds.map(neutralId => ({type: "object", $ref: "#/$defs/referenceItem", properties: {neutral_id: {const: neutralId}}})),
        items: false
      }
    },
    $defs: {
      sha256: {type: "string", pattern: "^[0-9a-f]{64}$"},
      label: {enum: ["CLEAN", "SURFACE_VISIBLE_DEFECT", "CONTEXT_DEPENDENT_DEFECT", "UNRESOLVED"]},
      defectAtom: {
        type: "object",
        additionalProperties: false,
        required: ["kind", "claim", "evidence"],
        properties: {
          kind: {type: "string", enum: ["ACCURACY", "OMISSION", "ADDITION", "PLACEHOLDER_OR_MARKUP", "REGISTER_OR_DIALOGUE", "MECHANICS_OR_RUNTIME", "OTHER"]},
          claim: {type: "string", minLength: 1, maxLength: 240, pattern: "\\S"},
          evidence: {type: "string", minLength: 1, maxLength: 480, pattern: "\\S"}
        }
      },
      referenceResponse: {
        type: "object",
        additionalProperties: false,
        required: ["label", "evidence", "defect_atoms", "source_evidence_sha256s", "limitations"],
        properties: {
          label: {$ref: "#/$defs/label"},
          evidence: {type: "string", minLength: 1, maxLength: 800, pattern: "\\S"},
          defect_atoms: {type: "array", maxItems: 8, uniqueItems: true, items: {$ref: "#/$defs/defectAtom"}},
          source_evidence_sha256s: {type: "array", maxItems: 16, uniqueItems: true, items: {$ref: "#/$defs/sha256"}},
          limitations: {type: "string", maxLength: 800}
        },
        allOf: [
          {if: {properties: {label: {const: "CLEAN"}}, required: ["label"]}, then: {properties: {defect_atoms: {type: "array", maxItems: 0}, source_evidence_sha256s: {type: "array", maxItems: 0}, limitations: {type: "string", maxLength: 0}}}},
          {if: {properties: {label: {const: "SURFACE_VISIBLE_DEFECT"}}, required: ["label"]}, then: {properties: {defect_atoms: {type: "array", minItems: 1}, source_evidence_sha256s: {type: "array", maxItems: 0}, limitations: {type: "string", maxLength: 0}}}},
          {if: {properties: {label: {const: "CONTEXT_DEPENDENT_DEFECT"}}, required: ["label"]}, then: {properties: {defect_atoms: {type: "array", minItems: 1}, source_evidence_sha256s: {type: "array", minItems: 1}, limitations: {type: "string", maxLength: 0}}}},
          {if: {properties: {label: {const: "UNRESOLVED"}}, required: ["label"]}, then: {properties: {limitations: {type: "string", minLength: 1, pattern: "\\S"}}}}
        ]
      },
      referenceItem: {
        type: "object",
        additionalProperties: false,
        required: ["neutral_id", "response"],
        properties: {
          neutral_id: {type: "string", pattern: "^RFR-[0-9]{4}$"},
          response: {$ref: "#/$defs/referenceResponse"}
        }
      }
    }
  };
}

function writeArtifact(out, name, value) {
  const bytes = jsonBytes(value);
  fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, name), bytes);
  return {...fileRecord(bytes), logical_path: name};
}

export function buildPackage({root = defaultRoot, out = here} = {}) {
  const presentationInput = readPinned(root, "presentation");
  const registryInput = readPinned(root, "source_binding_registry");
  const sourceReportInput = readPinned(root, "source_build_report");
  const fixtureInput = readPinned(root, "executor_fixture");
  const inputRecords = {
    presentation: presentationInput.record,
    source_binding_registry: registryInput.record,
    source_build_report: sourceReportInput.record,
    executor_fixture: fixtureInput.record
  };
  const retained = validateInputs(presentationInput.value, registryInput.value);
  const queue = makeQueue(presentationInput.value);
  const localRegistry = makeLocalRegistry(presentationInput.value, registryInput.value, retained, inputRecords);
  const generated = {};
  generated["OUTBOUND-AUDIT-QUEUE.json"] = writeArtifact(out, "OUTBOUND-AUDIT-QUEUE.json", queue);
  generated["LOCAL-BINDING-REGISTRY.json"] = writeArtifact(out, "LOCAL-BINDING-REGISTRY.json", localRegistry);
  const schema = makeReferenceSchema(generated["OUTBOUND-AUDIT-QUEUE.json"].sha256, queue.items.map(item => item.neutral_id));
  generated["REFERENCE-SCHEMA.json"] = writeArtifact(out, "REFERENCE-SCHEMA.json", schema);
  const report = {
    schema_version: "route-familiarity-reference-audit-build-report-v1",
    status: "PASS_ZERO_INFERENCE_REFERENCE_FREEZE_GATES",
    model_calls: 0,
    network_calls: 0,
    production_translation_commit: FROZEN.production_translation_commit,
    frozen_inputs: inputRecords,
    counts: {
      items: retained.length,
      populated_responses: 0,
      profiles: countBy(retained, "profile"),
      categories: countBy(retained, "category")
    },
    generated_artifacts: generated,
    gates: {
      frozen_input_hashes: "PASS",
      source_presentation_order: "PASS",
      unique_neutral_ids: "PASS",
      byte_exact_content_bindings: "PASS",
      local_route_cell_join: "PASS",
      outbound_exact_keys: "PASS",
      outbound_response_slots_unpopulated: "PASS",
      reference_schema_unpopulated: "PASS"
    },
    artifact_hash_dependency: "BUILD-REPORT hashes the queue, local registry, and schema. EXPERIMENT hashes those plus BUILD-REPORT. No artifact contains its own hash."
  };
  generated["BUILD-REPORT.json"] = writeArtifact(out, "BUILD-REPORT.json", report);
  const experiment = {
    schema_version: "route-familiarity-reference-audit-experiment-v1",
    status: "FROZEN_ZERO_INFERENCE_REFERENCE_AUDIT_PACKAGE",
    objective: "Prepare deterministic unpopulated reference-audit inputs for all retained sanitized route-familiarity rows.",
    production_translation_commit: FROZEN.production_translation_commit,
    inference: {allowed: false, model_calls: 0, network_calls: 0},
    claims: {
      historical_route_cells_are_exposure_strata_only: true,
      isolation_claimed: false,
      generalization_claimed: false,
      memorization_claimed: false,
      truth_labels_populated: false
    },
    frozen_inputs: inputRecords,
    frozen_outputs: generated,
    protocol: [
      "Keep OUTBOUND-AUDIT-QUEUE.json separate from LOCAL-BINDING-REGISTRY.json.",
      "Fill responses only under the REFERENCE-SCHEMA.json contract after this zero-inference freeze.",
      "Never include completed reference labels in model-facing inference inputs.",
      "Join completed responses to local provenance only by neutral_id after auditing."
    ]
  };
  generated["EXPERIMENT.json"] = writeArtifact(out, "EXPERIMENT.json", experiment);
  return {queue, localRegistry, schema, report, experiment, generated};
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const result = buildPackage(parseArgs(process.argv.slice(2)));
  process.stdout.write(`${JSON.stringify({status: "PASS", generated: result.generated, counts: result.report.counts}, null, 2)}\n`);
}
