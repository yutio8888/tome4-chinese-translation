#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");

export const SHARD_COUNT = 5;
export const SHARD_SIZE = 29;
export const QUEUE_ITEM_KEYS = Object.freeze([
  "neutral_id", "category", "profile", "source", "target", "bounded_fixed_context", "response"
]);
export const FROZEN = Object.freeze({
  inputs: {
    queue: {
      logical_path: "evidence/quality/model-probes/route-familiarity-reference-audit-v1/OUTBOUND-AUDIT-QUEUE.json",
      sha256: "620b736996ac254c43b3c721cdbfca20f7e68d8f553b7fe21b9effa0c025b3d2"
    },
    response_schema: {
      logical_path: "evidence/quality/model-probes/route-familiarity-reference-audit-v1/REFERENCE-SCHEMA.json",
      sha256: "c197e30ebaaae353df58049c2f3479dc2a0c799d3633dba4e70b5db27f859f34"
    },
    local_binding_registry: {
      logical_path: "evidence/quality/model-probes/route-familiarity-reference-audit-v1/LOCAL-BINDING-REGISTRY.json",
      sha256: "64013413c5a30956185a7a71c2b21d7960a6b2ddda55e9c709657fe10ac3a7a1"
    },
    executor_fixture: {
      logical_path: "evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua",
      sha256: "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7"
    }
  },
  counts: {items: 145, shards: 5, items_per_shard: 29, source_evidence_records: 145, populated_responses: 0},
  local_verification: {node_observed: "v22.22.1", ajv_observed: "8.17.1"}
});

export const PROMPT = `# Translation reference annotation

Review every supplied item in its given order. Compare the source and target, using bounded_fixed_context only as evidence for meaning, placeholders, runtime behavior, speaker intent, and register. Do not infer facts that the supplied fields do not support.

Assign exactly one label to every item:

- CLEAN: the target has no material translation defect supported by the supplied evidence.
- SURFACE_VISIBLE_DEFECT: a material defect is visible from source and target without relying on bounded context.
- CONTEXT_DEPENDENT_DEFECT: a material defect is established only with the bounded context.
- UNRESOLVED: the supplied evidence is insufficient for a determinate label.

For every item, provide a concise evidence statement. A defect label requires one or more bounded defect atoms. Each atom must state its kind, claim, and supporting evidence. For CONTEXT_DEPENDENT_DEFECT, source_evidence_sha256s must cite the supplied source_evidence[].sha256 for that same item; do not calculate, invent, substitute, or cite any other hash. Each source_evidence text is byte-equal to the corresponding item's bounded_fixed_context, and its lowercase SHA-256 is over the exact UTF-8 bytes of text. CLEAN must have no defect atoms, source-evidence hashes, or limitations. Surface-visible defects must have no source-evidence hashes or limitations. Context-dependent defects must have no limitations. UNRESOLVED must state a non-empty limitation.

Return exactly one JSON document conforming to the supplied response schema. Take response schema_version, status, parent_queue_sha256, and shard_file_sha256 from the response schema consts. Take shard_id, item_count, item_ids, and item order from the shard. Do not add fields or prose outside the JSON document.
`;

const SHA256_RE = /^[0-9a-f]{64}$/u;
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
export const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const fileRecord = bytes => ({sha256: sha256(bytes), size_bytes: bytes.length});
const compareCodepoints = (left, right) => left < right ? -1 : left > right ? 1 : 0;
const forbiddenIdentityPatterns = Object.freeze([
  ["historical route cell", /\bH[1-4]\b/u],
  ["provider or model identity", /\b(?:OpenAI|Anthropic|Google|Z\.ai|Codex|Claude|Gemini|GLM|Qwen|Grok|GPT[-_.]?\d)\b/iu],
  ["local absolute path", /(?:\/home\/|\/Users\/|\/tmp\/|\/private\/|\/srv\/|\/mnt\/|[A-Za-z]:[\\/](?:Users|home|work)[\\/]|\\\\[^\\]+\\[^\\]+)/u],
  ["local provenance", /(?:\bprovenance\b|local[ _-]?(?:binding|registry)|presentation[ _-]?ordinal)/iu],
  ["sealed or prior conclusion", /(?:sealed[ _-]?(?:truth|reference)|prior (?:finding|adjudication)|defect[ _-]?id|already reviewed|senior[ _-]?audit)/iu]
]);

export function exactKeys(value, expected, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: object required`);
  const actual = Object.keys(value).sort(compareCodepoints);
  const wanted = [...expected].sort(compareCodepoints);
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) throw new Error(`${label}: exact-key drift`);
}

function allStrings(value, pointer = "") {
  if (typeof value === "string") return [{pointer, value}];
  if (Array.isArray(value)) return value.flatMap((entry, index) => allStrings(entry, `${pointer}/${index}`));
  if (value && typeof value === "object") return Object.entries(value).flatMap(([key, entry]) => allStrings(entry, `${pointer}/${key}`));
  return [];
}

export function assertModelFacingHygiene(value, {allowLabelVocabulary = false, prompt = false} = {}) {
  for (const {pointer, value: text} of allStrings(value)) {
    for (const [label, pattern] of forbiddenIdentityPatterns) if (pattern.test(text)) throw new Error(`${pointer || "/"}: ${label} leak`);
    if (!prompt && !allowLabelVocabulary && /\b(?:CLEAN|SURFACE_VISIBLE_DEFECT|CONTEXT_DEPENDENT_DEFECT|UNRESOLVED)\b/u.test(text)) throw new Error(`${pointer || "/"}: populated or truth-label leak`);
    if (prompt && /["']label["']\s*:\s*["'](?:CLEAN|SURFACE_VISIBLE_DEFECT|CONTEXT_DEPENDENT_DEFECT|UNRESOLVED)["']/u.test(text)) throw new Error(`${pointer || "/"}: populated-answer structure`);
  }
}

function parseArgs(argv) {
  const args = {root: defaultRoot, out: here};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!new Set(["--root", "--out"]).has(flag) || !value) {
      throw new Error("usage: node build.mjs [--root REPO] [--out OUTPUT_DIR]");
    }
    args[flag.slice(2)] = path.resolve(value);
  }
  return args;
}

function readPinned(root, name) {
  const pin = FROZEN.inputs[name];
  const bytes = fs.readFileSync(path.join(root, pin.logical_path));
  if (sha256(bytes) !== pin.sha256) throw new Error(`${name}: frozen input hash drift`);
  return {
    value: pin.logical_path.endsWith(".json") ? JSON.parse(bytes.toString("utf8")) : null,
    record: {...pin, size_bytes: bytes.length}
  };
}

export function validateQueue(queue) {
  exactKeys(queue, ["schema_version", "status", "inference_allowed", "presentation_order", "response_contract", "counts", "items"], "queue");
  if (queue.schema_version !== "route-familiarity-reference-audit-queue-v1" || queue.status !== "FROZEN_ZERO_INFERENCE_UNPOPULATED" || queue.inference_allowed !== false) throw new Error("queue identity drift");
  if (!Array.isArray(queue.items) || queue.items.length !== FROZEN.counts.items) throw new Error("queue item count drift");
  const ids = new Set();
  for (let index = 0; index < queue.items.length; index += 1) {
    const item = queue.items[index];
    exactKeys(item, QUEUE_ITEM_KEYS, `queue.items[${index}]`);
    if (!/^RFR-[0-9]{4}$/u.test(item.neutral_id) || ids.has(item.neutral_id)) throw new Error(`${item.neutral_id}: malformed or duplicate neutral ID`);
    if (item.response !== null) throw new Error(`${item.neutral_id}: populated response`);
    for (const field of ["category", "profile", "source", "target", "bounded_fixed_context"]) if (typeof item[field] !== "string") throw new Error(`${item.neutral_id}: ${field} must be a string`);
    ids.add(item.neutral_id);
  }
  return queue.items;
}

export function validateQueueBindings(queue, registry) {
  const items = validateQueue(queue);
  if (!registry || !Array.isArray(registry.items) || registry.items.length !== items.length) throw new Error("local binding registry count drift");
  for (let index = 0; index < items.length; index += 1) {
    const item = items[index];
    const binding = registry.items[index];
    if (item.neutral_id !== binding.neutral_id || binding.presentation_ordinal !== index + 1) throw new Error(`${item.neutral_id}: local binding order drift`);
    for (const [field, hashField] of [["source", "source_sha256"], ["target", "target_sha256"], ["bounded_fixed_context", "bounded_fixed_context_sha256"]]) {
      if (sha256(item[field]) !== binding[hashField]) throw new Error(`${item.neutral_id}: ${field} content binding drift`);
    }
  }
}

const shardId = index => `SHARD-${String(index + 1).padStart(2, "0")}`;
const shardName = index => `OUTBOUND-${shardId(index)}.json`;
const schemaName = index => `RESPONSE-SCHEMA-${shardId(index)}.json`;

export function makeShards(queue) {
  const items = validateQueue(queue);
  return Array.from({length: SHARD_COUNT}, (_, index) => {
    const shardItems = items.slice(index * SHARD_SIZE, (index + 1) * SHARD_SIZE).map(item => ({...item}));
    if (shardItems.length !== SHARD_SIZE) throw new Error(`${shardId(index)}: shard size drift`);
    return {
      schema_version: "route-familiarity-reference-collection-shard-v1",
      status: "FROZEN_ZERO_INFERENCE_UNPOPULATED",
      parent_queue_sha256: FROZEN.inputs.queue.sha256,
      shard_id: shardId(index),
      item_count: SHARD_SIZE,
      items: shardItems,
      source_evidence: shardItems.map(item => ({
        evidence_id: `EVIDENCE-${item.neutral_id}`,
        neutral_id: item.neutral_id,
        sha256: sha256(Buffer.from(item.bounded_fixed_context, "utf8")),
        text: item.bounded_fixed_context
      }))
    };
  });
}

export function validateShardEvidence(shard) {
  if (!Array.isArray(shard.items) || !Array.isArray(shard.source_evidence) || shard.items.length !== SHARD_SIZE || shard.source_evidence.length !== SHARD_SIZE) throw new Error(`${shard.shard_id}: evidence count drift`);
  for (let index = 0; index < SHARD_SIZE; index += 1) {
    const item = shard.items[index];
    const evidence = shard.source_evidence[index];
    exactKeys(evidence, ["evidence_id", "neutral_id", "sha256", "text"], `${shard.shard_id}.source_evidence[${index}]`);
    if (evidence.evidence_id !== `EVIDENCE-${item.neutral_id}` || evidence.neutral_id !== item.neutral_id) throw new Error(`${shard.shard_id}.source_evidence[${index}]: item alignment drift`);
    if (evidence.text !== item.bounded_fixed_context) throw new Error(`${shard.shard_id}.source_evidence[${index}]: text binding drift`);
    if (!SHA256_RE.test(evidence.sha256) || evidence.sha256 !== sha256(Buffer.from(evidence.text, "utf8"))) throw new Error(`${shard.shard_id}.source_evidence[${index}]: UTF-8 hash binding drift`);
  }
}

export function makeResponseSchema({index, shardSha256, neutralIds, evidenceSha256s, predecessorDefs}) {
  if (!Number.isInteger(index) || index < 0 || index >= SHARD_COUNT || !SHA256_RE.test(shardSha256) || !Array.isArray(neutralIds) || neutralIds.length !== SHARD_SIZE || new Set(neutralIds).size !== SHARD_SIZE || !Array.isArray(evidenceSha256s) || evidenceSha256s.length !== SHARD_SIZE || evidenceSha256s.some(hash => !SHA256_RE.test(hash))) throw new Error("response schema binding malformed");
  return {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $id: `route-familiarity-reference-collection-v1/${schemaName(index)}`,
    title: `Route-familiarity reference responses ${shardId(index)}`,
    type: "object",
    additionalProperties: false,
    required: ["schema_version", "status", "parent_queue_sha256", "shard_id", "shard_file_sha256", "item_count", "item_ids", "items"],
    properties: {
      schema_version: {const: "route-familiarity-reference-collection-responses-v1"},
      status: {const: "REFERENCE_COLLECTION_COMPLETE"},
      parent_queue_sha256: {const: FROZEN.inputs.queue.sha256},
      shard_id: {const: shardId(index)},
      shard_file_sha256: {const: shardSha256},
      item_count: {const: SHARD_SIZE},
      item_ids: {const: neutralIds},
      items: {
        type: "array",
        minItems: SHARD_SIZE,
        maxItems: SHARD_SIZE,
        prefixItems: neutralIds.map((neutralId, itemIndex) => ({
          type: "object",
          $ref: "#/$defs/referenceItem",
          properties: {
            neutral_id: {const: neutralId},
            response: {
              type: "object",
              properties: {
                source_evidence_sha256s: {type: "array", items: {const: evidenceSha256s[itemIndex]}}
              }
            }
          }
        })),
        items: false
      }
    },
    $defs: structuredClone(predecessorDefs)
  };
}

function commonBindings(generated, shards) {
  return shards.map((shard, index) => ({
    shard_id: shard.shard_id,
    shard_path: shardName(index),
    shard_sha256: generated[shardName(index)].sha256,
    prompt_path: "PROMPT.md",
    prompt_sha256: generated["PROMPT.md"].sha256,
    response_schema_path: schemaName(index),
    response_schema_sha256: generated[schemaName(index)].sha256,
    item_count: SHARD_SIZE,
    neutral_ids: shard.items.map(item => item.neutral_id)
  }));
}

export function makeDerivationRules() {
  return {
    evaluation_semantics: "FIRST_MATCH_WINS_IN_EVALUATION_ORDER",
    evaluation_order: [
      "any_unresolved",
      "any_material_evidence_conflict",
      "unanimous_or_three_of_four",
      "two_two_split",
      "default_outcome"
    ],
    any_unresolved: "LEAD_ADJUDICATION_REQUIRED",
    any_material_evidence_conflict: "LEAD_ADJUDICATION_REQUIRED",
    unanimous_or_three_of_four: "PROVISIONAL_CONSENSUS",
    two_two_split: "LEAD_ADJUDICATION_REQUIRED",
    default_outcome: "LEAD_ADJUDICATION_REQUIRED",
    per_route_reference_score: "LEAVE_ONE_ROUTE_OUT_CONSENSUS_PLUS_LEAD_ADJUDICATION",
    leave_one_route_out: {
      eligible_inputs: "EXACTLY_THREE_NON_HELD_OUT_ROUTES",
      evaluation_semantics: "FIRST_MATCH_WINS_IN_EVALUATION_ORDER",
      evaluation_order: [
        "any_non_held_out_unresolved",
        "any_non_held_out_material_evidence_conflict",
        "three_of_three_same_label",
        "two_of_three_same_label",
        "all_distinct_labels",
        "default_outcome"
      ],
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
  };
}

export function makeManifest(generated, shards) {
  const bindings = commonBindings(generated, shards);
  const lane = (lane_id, provider, harness, model, qualification) => ({
    lane_id,
    provider,
    harness,
    model,
    effort: "high",
    route_availability_status: "MUST_RECHECK_BEFORE_INFERENCE",
    cli_version_status: "MUST_RECHECK_BEFORE_INFERENCE",
    runtime_identity_status: "MUST_RECHECK_BEFORE_INFERENCE",
    qualification,
    bindings: structuredClone(bindings),
    later_output_filename_templates: {
      raw: `RAW-${lane_id}-{shard_id}.json`,
      acquisition: `ACQUISITION-${lane_id}-{shard_id}.json`,
      candidate: `CANDIDATE-${lane_id}-{shard_id}.json`
    }
  });
  return {
    schema_version: "route-familiarity-reference-collection-local-route-manifest-v1",
    status: "FROZEN_PREINFERENCE_LOCAL_ONLY",
    outbound_allowed: false,
    inference_allowed: false,
    experiment_class: "EXPLORATORY_NON_ISOLATED_REFERENCE",
    parent_queue_sha256: FROZEN.inputs.queue.sha256,
    counts: {lanes: 4, shards_per_lane: SHARD_COUNT, items_per_shard: SHARD_SIZE, planned_model_calls: 20, completed_model_calls: 0, populated_responses: 0},
    lanes: [
      lane("lane-01", "OpenAI", "Codex CLI", "gpt-5.6-sol", "exploratory non-isolated reference lane"),
      lane("lane-02", "Anthropic", "Claude Code CLI", "claude-opus-5", "exploratory participation despite formal NO-GO"),
      lane("lane-03", "Google", "Antigravity CLI", "gemini-3.7-flash-high", "exploratory non-isolated reference lane"),
      lane("lane-04", "Z.ai/GLM", "Pi CLI", "opencode-go/glm-5.3", "exploratory non-isolated reference lane")
    ],
    derivation_rules: makeDerivationRules(),
    later_run_rules: [
      "Recheck and freeze actual CLI versions, model availability, and runtime identity rules immediately before inference.",
      "Run every lane on identical shard bytes, prompt bytes, response-schema bytes, item order, and output contract.",
      "Create RAW, acquisition, and candidate files only in the later execution task directory, never in this frozen package; this manifest defines filename templates only."
    ]
  };
}

export function validateManifest(manifest, generated) {
  if (manifest.outbound_allowed !== false || manifest.inference_allowed !== false || manifest.experiment_class !== "EXPLORATORY_NON_ISOLATED_REFERENCE") throw new Error("manifest local-only boundary drift");
  if (!Array.isArray(manifest.lanes) || manifest.lanes.length !== 4) throw new Error("manifest lane count drift");
  const expectedIdentities = [
    ["OpenAI", "Codex CLI", "gpt-5.6-sol"],
    ["Anthropic", "Claude Code CLI", "claude-opus-5"],
    ["Google", "Antigravity CLI", "gemini-3.7-flash-high"],
    ["Z.ai/GLM", "Pi CLI", "opencode-go/glm-5.3"]
  ];
  const baselineBindings = JSON.stringify(manifest.lanes[0].bindings);
  for (let index = 0; index < manifest.lanes.length; index += 1) {
    const lane = manifest.lanes[index];
    if (JSON.stringify([lane.provider, lane.harness, lane.model]) !== JSON.stringify(expectedIdentities[index])) throw new Error(`${lane.lane_id}: lane identity drift`);
    if (lane.effort !== "high" || lane.route_availability_status !== "MUST_RECHECK_BEFORE_INFERENCE" || lane.cli_version_status !== "MUST_RECHECK_BEFORE_INFERENCE" || lane.runtime_identity_status !== "MUST_RECHECK_BEFORE_INFERENCE") throw new Error(`${lane.lane_id}: route preflight status drift`);
    if (JSON.stringify(lane.bindings) !== baselineBindings) throw new Error(`${lane.lane_id}: lane binding drift`);
    if (!Array.isArray(lane.bindings) || lane.bindings.length !== SHARD_COUNT) throw new Error(`${lane.lane_id}: shard binding count drift`);
    for (const binding of lane.bindings) {
      for (const [pathField, hashField] of [["shard_path", "shard_sha256"], ["prompt_path", "prompt_sha256"], ["response_schema_path", "response_schema_sha256"]]) {
        if (!generated[binding[pathField]] || generated[binding[pathField]].sha256 !== binding[hashField]) throw new Error(`${lane.lane_id}: ${pathField} hash binding drift`);
      }
    }
  }
  if (JSON.stringify(manifest.derivation_rules) !== JSON.stringify(makeDerivationRules())) throw new Error("manifest ordered derivation rule drift");
  if (!manifest.later_run_rules.some(rule => /later execution task directory, never in this frozen package/u.test(rule))) throw new Error("manifest later-output boundary drift");
  if (manifest.counts.completed_model_calls !== 0 || manifest.counts.populated_responses !== 0) throw new Error("manifest zero-call drift");
}

function writeJson(out, name, value) {
  const bytes = jsonBytes(value);
  fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, name), bytes);
  return {...fileRecord(bytes), logical_path: name};
}

function writeText(out, name, value) {
  const bytes = Buffer.from(value, "utf8");
  fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, name), bytes);
  return {...fileRecord(bytes), logical_path: name};
}

export function buildPackage({root = defaultRoot, out = here} = {}) {
  const queueInput = readPinned(root, "queue");
  const schemaInput = readPinned(root, "response_schema");
  const registryInput = readPinned(root, "local_binding_registry");
  const fixtureInput = readPinned(root, "executor_fixture");
  validateQueueBindings(queueInput.value, registryInput.value);
  exactKeys(schemaInput.value.$defs, ["sha256", "label", "defectAtom", "referenceResponse", "referenceItem"], "predecessor schema definitions");
  const inputRecords = {
    queue: queueInput.record,
    response_schema: schemaInput.record,
    local_binding_registry: registryInput.record,
    executor_fixture: fixtureInput.record
  };
  const generated = {};
  const shards = makeShards(queueInput.value);
  for (const shard of shards) {
    validateShardEvidence(shard);
    assertModelFacingHygiene(shard);
  }
  assertModelFacingHygiene(PROMPT, {prompt: true});
  for (let index = 0; index < shards.length; index += 1) generated[shardName(index)] = writeJson(out, shardName(index), shards[index]);
  generated["PROMPT.md"] = writeText(out, "PROMPT.md", PROMPT);
  const schemas = shards.map((shard, index) => makeResponseSchema({
    index,
    shardSha256: generated[shardName(index)].sha256,
    neutralIds: shard.items.map(item => item.neutral_id),
    evidenceSha256s: shard.source_evidence.map(evidence => evidence.sha256),
    predecessorDefs: schemaInput.value.$defs
  }));
  for (const schema of schemas) assertModelFacingHygiene(schema, {allowLabelVocabulary: true});
  for (let index = 0; index < schemas.length; index += 1) generated[schemaName(index)] = writeJson(out, schemaName(index), schemas[index]);
  const manifest = makeManifest(generated, shards);
  validateManifest(manifest, generated);
  generated["LOCAL-ROUTE-MANIFEST.json"] = writeJson(out, "LOCAL-ROUTE-MANIFEST.json", manifest);
  const reportInputs = Object.fromEntries(Object.entries(generated).map(([name, record]) => [name, record]));
  const report = {
    schema_version: "route-familiarity-reference-collection-build-report-v1",
    status: "PASS_DETERMINISTIC_ZERO_INFERENCE_BUILD",
    model_calls: 0,
    network_calls: 0,
    frozen_inputs: inputRecords,
    counts: {...FROZEN.counts, lanes: 4, response_schemas: 5, generated_before_report: Object.keys(reportInputs).length},
    local_verification_prerequisites_observed: {...FROZEN.local_verification, ajv_policy: "system-resolved Ajv major 8 only; patch-level drift accepted"},
    generated_artifacts: reportInputs,
    gates: {
      frozen_input_hashes: "PASS",
      queue_binding_hashes: "PASS",
      contiguous_five_by_twenty_nine: "PASS",
      unchanged_seven_key_items_bytes_and_order: "PASS",
      zero_populated_responses: "PASS",
      exact_predecessor_response_definitions_plus_per_item_evidence_hash_binding: "PASS",
      shard_schema_bindings: "PASS",
      ordered_source_evidence_utf8_hash_bindings: "PASS",
      recursive_all_model_facing_artifact_hygiene: "PASS",
      provider_neutral_prompt: "PASS",
      four_lane_identical_bindings: "PASS",
      ordered_derivation_precedence_and_default_adjudication: "PASS",
      zero_model_and_network_calls: "PASS"
    },
    hash_dag: [
      "frozen inputs -> outbound shards and prompt",
      "outbound shard hashes plus predecessor response definitions -> response schemas",
      "shards plus prompt plus response schemas -> local route manifest",
      "all preceding emitted artifacts -> BUILD-REPORT.json",
      "all preceding emitted artifacts plus BUILD-REPORT.json -> EXPERIMENT.json"
    ],
    self_hashes_present: false
  };
  generated["BUILD-REPORT.json"] = writeJson(out, "BUILD-REPORT.json", report);
  const experimentInputs = Object.fromEntries(Object.entries(generated).map(([name, record]) => [name, record]));
  const experiment = {
    schema_version: "route-familiarity-reference-collection-experiment-v1",
    status: "FROZEN_ZERO_INFERENCE_COLLECTION_PACKAGE",
    experiment_class: "EXPLORATORY_NON_ISOLATED_REFERENCE",
    objective: "Freeze equal five-shard inputs and strict response contracts for a later four-lane exploratory reference collection.",
    inference: {allowed: false, model_calls: 0, network_calls: 0, route_checks_completed: false, route_check_status: "MUST_RECHECK_BEFORE_INFERENCE"},
    claims: {formally_isolated_gold_standard: false, truth_labels_populated: false, responses_populated: false, route_ranking_present: false},
    frozen_inputs: inputRecords,
    frozen_outputs: experimentInputs,
    local_verification_prerequisites_observed: {...FROZEN.local_verification, purpose: "local build/test verification only; not inference route-version checks"},
    protocol: [
      "Keep local route identities and later outputs separate from model-facing shards and prompt.",
      "Before inference, recheck and freeze every CLI version, model availability, and runtime identity rule.",
      "After later acquisition, derive provisional consensus and leave-one-route-out scores only under LOCAL-ROUTE-MANIFEST.json rules.",
      "For both four-route and leave-one-route-out derivation, apply the manifest evaluation order with first-match-wins semantics: UNRESOLVED and material-evidence-conflict adjudication triggers precede consensus, and every unmatched label pattern requires lead adjudication.",
      "Place later RAW, acquisition, and candidate outputs only in the later execution task directory, never in this frozen package.",
      "Do not describe later results as a formally isolated gold standard."
    ],
    hash_dag_terminal: true,
    self_hash_present: false
  };
  generated["EXPERIMENT.json"] = writeJson(out, "EXPERIMENT.json", experiment);
  return {shards, schemas, manifest, report, experiment, generated};
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const result = buildPackage(parseArgs(process.argv.slice(2)));
  process.stdout.write(`${JSON.stringify({status: "PASS", generated: result.generated, counts: result.report.counts}, null, 2)}\n`);
}
