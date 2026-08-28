#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");

export const OUTPUT_NAMES = Object.freeze([
  "TARGET-BINDING-REGISTRY.json",
  "AUDIT-QUEUE.json",
  "SURFACE-QUEUE-1.json",
  "SURFACE-QUEUE-2.json",
  "SURFACE-QUEUE-3.json",
  "TARGET-JOIN-REPORT.json"
]);

const frameItemFields = Object.freeze([
  "task_id", "original_revision_key", "component", "section", "source_tag",
  "profile", "source", "source_sha256", "source_only_flags"
]);

export const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const canonicalBytes = value => Buffer.from(JSON.stringify(value), "utf8");
const identityKey = (taskId, revisionKey) => `${taskId}\0${revisionKey}`;

function assertObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: expected object`);
}

function exactKeys(value, expected, label) {
  assertObject(value, label);
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) throw new Error(`${label}: exact field set mismatch`);
}

function assertString(value, label, allowEmpty = false) {
  if (typeof value !== "string" || (!allowEmpty && !value)) throw new Error(`${label}: expected non-empty string`);
}

function assertSafeRelative(value, label) {
  assertString(value, label);
  if (value.includes("\0") || path.posix.isAbsolute(value) || path.posix.normalize(value) !== value || value === ".." || value.startsWith("../")) {
    throw new Error(`${label}: unsafe relative path`);
  }
}

function assertInside(root, candidate, label) {
  const relative = path.relative(root, candidate);
  if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) throw new Error(`${label}: escaped root`);
}

export function terminalDispatches(task) {
  let dispatches = task.dispatches.filter(dispatch =>
    dispatch.role === "REVIEWER" &&
    dispatch.purpose === "translation_contextual_v1" &&
    dispatch.input_path
  );
  const withCycle = dispatches.filter(dispatch => Number.isFinite(dispatch.cycle));
  if (withCycle.length) {
    const terminalCycle = Math.max(...withCycle.map(dispatch => dispatch.cycle));
    dispatches = withCycle.filter(dispatch => dispatch.cycle === terminalCycle);
  } else if (dispatches.length) {
    dispatches = [dispatches.at(-1)];
  }
  return dispatches;
}

function uniqueIndex(rows, keyOf, label) {
  const index = new Map();
  for (const row of rows) {
    const key = keyOf(row);
    if (index.has(key)) throw new Error(`${label}: duplicate identity ${key}`);
    index.set(key, row);
  }
  return index;
}

export function expectedTerminalRecords(membership, snapshot) {
  if (!Array.isArray(membership.items) || !Array.isArray(snapshot.tasks)) throw new Error("upstream membership/snapshot shape");
  const taskIndex = uniqueIndex(snapshot.tasks, task => task.task_id, "snapshot tasks");
  const taskIds = [...new Set(membership.items.map(item => item.task_id))].sort();
  const byPath = new Map();
  for (const taskId of taskIds) {
    const task = taskIndex.get(taskId);
    if (!task) throw new Error(`${taskId}: missing provenance task`);
    if (!Array.isArray(task.dispatches)) throw new Error(`${taskId}: dispatches missing`);
    const dispatches = terminalDispatches(task);
    if (!dispatches.length) throw new Error(`${taskId}: terminal contextual input missing`);
    for (const dispatch of dispatches) {
      assertSafeRelative(dispatch.input_path, `${taskId}: terminal input`);
      const record = {
        task_id: taskId,
        logical_path: dispatch.input_path,
        sha256: dispatch.input_fingerprint?.sha256,
        size_bytes: dispatch.input_fingerprint?.size_bytes
      };
      if (!/^[0-9a-f]{64}$/u.test(record.sha256 ?? "") || !Number.isInteger(record.size_bytes) || record.size_bytes < 1) {
        throw new Error(`${taskId}: terminal fingerprint missing`);
      }
      const previous = byPath.get(record.logical_path);
      if (previous && JSON.stringify(previous) !== JSON.stringify(record)) throw new Error(`${record.logical_path}: conflicting terminal binding`);
      byPath.set(record.logical_path, record);
    }
  }
  return [...byPath.values()].sort((a, b) => a.logical_path.localeCompare(b.logical_path));
}

function terminalManifest(records) {
  const canonical = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  return {
    records: records.map(({logical_path, sha256, size_bytes}) => ({logical_path, sha256, size_bytes})),
    count: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
    manifest_sha256: sha256Bytes(canonical)
  };
}

function verifyManifest(actual, expected) {
  for (const field of ["count", "bytes", "manifest_sha256"]) {
    if (actual[field] !== expected[field]) throw new Error(`terminal manifest ${field} drift`);
  }
}

function loadTerminalRows(records, terminalFiles) {
  const rows = [];
  for (const record of records) {
    const bytes = terminalFiles.get(record.logical_path);
    if (!Buffer.isBuffer(bytes)) throw new Error(`${record.logical_path}: terminal file missing`);
    if (bytes.length !== record.size_bytes || sha256Bytes(bytes) !== record.sha256) throw new Error(`${record.logical_path}: terminal fingerprint drift`);
    let envelope;
    try {
      envelope = JSON.parse(bytes.toString("utf8"));
    } catch (error) {
      throw new Error(`${record.logical_path}: invalid JSON: ${error.message}`);
    }
    assertObject(envelope, record.logical_path);
    assertObject(envelope.payload, `${record.logical_path}.payload`);
    if (!Array.isArray(envelope.payload.translation_snapshot)) throw new Error(`${record.logical_path}: translation_snapshot missing`);
    envelope.payload.translation_snapshot.forEach((item, index) => {
      exactKeys(item, ["revision_key", "source", "target"], `${record.logical_path}.translation_snapshot[${index}]`);
      assertString(item.revision_key, `${record.logical_path}: revision_key`);
      assertString(item.source, `${record.logical_path}: source`, true);
      assertString(item.target, `${record.logical_path}: target`, true);
      rows.push({...item, task_id: record.task_id, terminal_input: {
        logical_path: record.logical_path,
        sha256: record.sha256,
        size_bytes: record.size_bytes
      }});
    });
  }
  return uniqueIndex(rows, row => identityKey(row.task_id, row.revision_key), "terminal rows");
}

function fileRecord(value) {
  const bytes = jsonBytes(value);
  return {sha256: sha256Bytes(bytes), size_bytes: bytes.length};
}

function bindingHash(record) {
  return sha256Bytes([
    record.audit_id, record.category, record.task_id, record.original_revision_key,
    record.source_sha256, record.target_sha256, record.membership_sha256,
    record.terminal_input.logical_path, record.terminal_input.sha256,
    String(record.terminal_input.size_bytes)
  ].join("\0"));
}

function itemHash(item) {
  return sha256Bytes(canonicalBytes(item));
}

function validatePacket(packet, frameItem, label) {
  for (const field of ["task_id", "original_revision_key", "component", "section", "source_sha256", "source_binding", "source_occurrences", "occurrences"]) {
    if (!Object.hasOwn(packet, field)) throw new Error(`${label}: packet field ${field} missing`);
  }
  for (const field of ["task_id", "original_revision_key", "component", "section", "source_sha256"]) {
    if (packet[field] !== frameItem[field]) throw new Error(`${label}: packet ${field} mismatch`);
  }
}

function verifyOutputSchemas(contract, outputs) {
  const registry = outputs["TARGET-BINDING-REGISTRY.json"];
  const queue = outputs["AUDIT-QUEUE.json"];
  exactKeys(registry, contract.outputs.target_binding_registry_top_fields, "TARGET-BINDING-REGISTRY");
  registry.records.forEach((record, index) => exactKeys(record, contract.outputs.target_binding_record_fields, `binding record ${index}`));
  registry.records.forEach((record, index) => exactKeys(record.terminal_input, ["logical_path", "sha256", "size_bytes"], `binding record ${index}.terminal_input`));
  exactKeys(queue, contract.outputs.audit_queue_top_fields, "AUDIT-QUEUE");
  queue.items.forEach((item, index) => {
    exactKeys(item, contract.outputs.audit_queue_item_fields, `audit item ${index}`);
    exactKeys(item.canonical_identity, ["revision_id", "revision_uid", "unit_id", "tu_uid", "membership_sha256"], `audit item ${index}.canonical_identity`);
  });
  const queueIds = queue.items.map(item => item.audit_id);
  const surfaceIds = [];
  for (let shard = 1; shard <= contract.expected.shards; shard += 1) {
    const surface = outputs[`SURFACE-QUEUE-${shard}.json`];
    exactKeys(surface, ["schema_version", "status", "phase", "shard_id", "shard_count", "target_bound_presentation_sha256", "item_count", "queue_item_sha256s", "next_gate", "items"], `SURFACE-QUEUE-${shard}`);
    if (surface.items.length !== contract.expected.items_per_shard) throw new Error(`shard ${shard}: item count`);
    surface.items.forEach((item, index) => exactKeys(item, contract.outputs.surface_item_fields, `surface ${shard}/${index}`));
    if (surface.item_count !== surface.items.length || surface.queue_item_sha256s.length !== surface.items.length) throw new Error(`shard ${shard}: surface manifest count`);
    surfaceIds.push(...surface.items.map(item => item.audit_id));
  }
  if (surfaceIds.length !== queueIds.length || new Set(surfaceIds).size !== surfaceIds.length || !queueIds.every(id => surfaceIds.includes(id))) throw new Error("surface shards are not globally disjoint and complete");
}

export function buildTargetQueueFromValues({contract, membership, snapshot, frame, packets, terminalFiles}) {
  if (contract.status !== "FROZEN_BEFORE_TARGET_LINK" || contract.model_calls_allowed !== 0 || contract.network_calls_allowed !== 0) throw new Error("target-join contract gate");
  if (membership.production_translation_commit !== contract.production_translation_commit || snapshot.source_repo_head !== contract.production_translation_commit) throw new Error("production commit drift");
  if (frame.presentation_sha256 !== contract.source_only_presentation_sha256 || packets.presentation_sha256 !== contract.source_only_presentation_sha256) throw new Error("source-only presentation drift");

  const membershipIndex = uniqueIndex(membership.items, item => identityKey(item.task_id, item.original_revision_key), "canonical membership");
  const terminalRecords = expectedTerminalRecords(membership, snapshot);
  const terminalManifestValue = terminalManifest(terminalRecords);
  verifyManifest(terminalManifestValue, contract.frozen_inputs.fingerprinted_terminal_input_manifest);
  const terminalIndex = loadTerminalRows(terminalRecords, terminalFiles);

  if (!Array.isArray(frame.categories) || !Array.isArray(packets.categories)) throw new Error("source presentation category shape");
  const expectedCategories = contract.expected.categories.map(entry => entry.category);
  if (JSON.stringify(frame.categories.map(entry => entry.category)) !== JSON.stringify(expectedCategories) || JSON.stringify(packets.categories.map(entry => entry.category)) !== JSON.stringify(expectedCategories)) throw new Error("category order drift");
  const packetRows = packets.categories.flatMap(category => category.packets);
  const packetIndex = uniqueIndex(packetRows, item => identityKey(item.task_id, item.original_revision_key), "source evidence packets");
  const selected = [];
  for (let categoryIndex = 0; categoryIndex < frame.categories.length; categoryIndex += 1) {
    const category = frame.categories[categoryIndex];
    const expectedCategory = contract.expected.categories[categoryIndex];
    if (category.items.length !== expectedCategory.items) throw new Error(`${category.category}: item count drift`);
    for (const item of category.items) {
      exactKeys(item, frameItemFields, `${category.category}: frame item`);
      selected.push({category: category.category, item});
    }
  }
  if (selected.length !== contract.expected.items || new Set(selected.map(({item}) => item.task_id)).size !== contract.expected.tasks) throw new Error("selected count drift");
  uniqueIndex(selected, ({item}) => identityKey(item.task_id, item.original_revision_key), "selected frame");
  if (packetIndex.size !== selected.length) throw new Error("packet count drift");

  const queueItems = [];
  const bindingRecords = [];
  selected.forEach(({category, item}, index) => {
    const key = identityKey(item.task_id, item.original_revision_key);
    const member = membershipIndex.get(key);
    const terminal = terminalIndex.get(key);
    const packet = packetIndex.get(key);
    if (!member) throw new Error(`${key}: membership missing`);
    if (!terminal) throw new Error(`${key}: terminal target missing`);
    if (!packet) throw new Error(`${key}: source evidence missing`);
    validatePacket(packet, item, key);
    if (terminal.source !== item.source || sha256Bytes(Buffer.from(terminal.source, "utf8")) !== item.source_sha256 || member.source_sha256 !== item.source_sha256) throw new Error(`${key}: source hash mismatch`);
    if (terminal.target.length === 0) throw new Error(`${key}: empty target`);
    const targetSha256 = sha256Bytes(Buffer.from(terminal.target, "utf8"));
    if (targetSha256 !== member.target_sha256) throw new Error(`${key}: target hash mismatch`);
    for (const field of ["component", "section", "source_tag", "profile"]) {
      if ((member[field] ?? null) !== (item[field] ?? null)) throw new Error(`${key}: membership ${field} mismatch`);
    }
    const auditId = `V1-${String(index + 1).padStart(3, "0")}`;
    const core = {
      audit_id: auditId,
      category,
      task_id: item.task_id,
      original_revision_key: item.original_revision_key,
      canonical_identity: {
        revision_id: member.canonical_revision_id,
        revision_uid: member.canonical_revision_uid,
        unit_id: member.canonical_unit_id,
        tu_uid: member.canonical_tu_uid,
        membership_sha256: member.membership_sha256
      },
      component: item.component,
      section: item.section,
      source_tag: item.source_tag,
      profile: item.profile,
      source: item.source,
      source_sha256: item.source_sha256,
      target: terminal.target,
      target_sha256: targetSha256,
      source_only_flags: item.source_only_flags,
      source_evidence: packet
    };
    queueItems.push({...core, item_sha256: itemHash(core)});
    const binding = {
      audit_id: auditId,
      category,
      task_id: item.task_id,
      original_revision_key: item.original_revision_key,
      canonical_revision_id: member.canonical_revision_id,
      membership_sha256: member.membership_sha256,
      source_sha256: item.source_sha256,
      target_sha256: targetSha256,
      terminal_input: terminal.terminal_input
    };
    bindingRecords.push({...binding, binding_sha256: bindingHash(binding)});
  });

  const targetPresentation = {
    schema_version: "prospective-source-context-target-bound-presentation-v1",
    categories: expectedCategories.map(category => ({
      category,
      items: queueItems.filter(item => item.category === category).map(item => ({
        revision_id: item.audit_id,
        source: item.source,
        target: item.target,
        source_evidence: item.source_evidence
      }))
    }))
  };
  const targetBoundPresentationSha256 = sha256Bytes(canonicalBytes(targetPresentation));
  const bindingCanonical = bindingRecords.map(record => [
    record.audit_id, record.category, record.task_id, record.original_revision_key,
    record.source_sha256, record.target_sha256, record.membership_sha256,
    record.terminal_input.logical_path, record.terminal_input.sha256,
    String(record.terminal_input.size_bytes)
  ].join("\0") + "\n").join("");

  const outputs = {};
  outputs["TARGET-BINDING-REGISTRY.json"] = {
    schema_version: "prospective-source-context-target-binding-registry-v1",
    status: "FROZEN_TARGET_BINDING",
    production_translation_commit: contract.production_translation_commit,
    source_only_presentation_sha256: contract.source_only_presentation_sha256,
    target_bound_presentation_sha256: targetBoundPresentationSha256,
    fingerprinted_terminal_input_manifest: terminalManifestValue,
    binding_manifest_sha256: sha256Bytes(bindingCanonical),
    counts: {items: bindingRecords.length, tasks: new Set(bindingRecords.map(item => item.task_id)).size, terminal_inputs: terminalRecords.length},
    records: bindingRecords
  };
  outputs["AUDIT-QUEUE.json"] = {
    schema_version: "prospective-source-context-truth-audit-queue-v1",
    status: "FROZEN_TARGET_BOUND_NO_INFERENCE",
    reviewer_inference_allowed: false,
    production_translation_commit: contract.production_translation_commit,
    source_only_presentation_sha256: contract.source_only_presentation_sha256,
    target_bound_presentation_sha256: targetBoundPresentationSha256,
    counts: {items: queueItems.length, tasks: new Set(queueItems.map(item => item.task_id)).size, Runtime: queueItems.filter(item => item.category === "Runtime").length, Narrative: queueItems.filter(item => item.category === "Narrative").length},
    surface_visible_fields: contract.outputs.surface_item_fields,
    context_visible_fields: contract.outputs.context_item_fields,
    items: queueItems
  };
  for (let shard = 1; shard <= contract.expected.shards; shard += 1) {
    const shardItems = queueItems.filter((_item, index) => index % contract.expected.shards === shard - 1);
    outputs[`SURFACE-QUEUE-${shard}.json`] = {
      schema_version: "prospective-source-context-surface-queue-v1",
      status: "FROZEN_SURFACE_CANDIDATE_INPUT",
      phase: "SURFACE",
      shard_id: shard,
      shard_count: contract.expected.shards,
      target_bound_presentation_sha256: targetBoundPresentationSha256,
      item_count: shardItems.length,
      queue_item_sha256s: shardItems.map(item => item.item_sha256),
      next_gate: "Freeze the complete exact-schema surface candidate by byte SHA-256 before releasing the matching context queue.",
      items: shardItems.map(item => ({audit_id: item.audit_id, source: item.source, target: item.target}))
    };
  }
  verifyOutputSchemas(contract, outputs);
  const outputHashes = Object.fromEntries(Object.entries(outputs).map(([name, value]) => [name, fileRecord(value)]));
  outputs["TARGET-JOIN-REPORT.json"] = {
    schema_version: "prospective-source-context-target-join-report-v1",
    status: "PASS_TARGET_JOIN_GATES",
    model_calls_made: 0,
    network_calls_made: 0,
    production_translation_commit: contract.production_translation_commit,
    source_only_presentation_sha256: contract.source_only_presentation_sha256,
    target_bound_presentation_sha256: targetBoundPresentationSha256,
    binding_manifest_sha256: outputs["TARGET-BINDING-REGISTRY.json"].binding_manifest_sha256,
    counts: {items: queueItems.length, tasks: new Set(queueItems.map(item => item.task_id)).size, terminal_inputs: terminalRecords.length, surface_shards: 3, context_shards_released: 0, items_per_shard: contract.expected.items_per_shard},
    output_hashes: outputHashes,
    gates: {
      frozen_inputs_verified: true,
      production_commit_exact: true,
      terminal_manifest_exact: true,
      terminal_fingerprints_exact: true,
      four_way_identity_cardinality_one: true,
      source_hashes_exact: true,
      target_hashes_exact: true,
      presentation_order_preserved: true,
      exact_output_schemas: true,
      surface_shards_disjoint_and_complete: true,
      context_shards_absent_before_release: true,
      model_calls_zero: true,
      network_calls_zero: true
    },
    no_go: []
  };
  exactKeys(outputs["TARGET-JOIN-REPORT.json"], ["schema_version", "status", "model_calls_made", "network_calls_made", "production_translation_commit", "source_only_presentation_sha256", "target_bound_presentation_sha256", "binding_manifest_sha256", "counts", "output_hashes", "gates", "no_go"], "TARGET-JOIN-REPORT");
  if (JSON.stringify(Object.keys(outputs).sort()) !== JSON.stringify([...OUTPUT_NAMES].sort())) throw new Error("bind output set drift");
  return outputs;
}

function readFrozen(root, record) {
  const absolute = path.resolve(root, record.logical_path);
  assertInside(root, absolute, record.logical_path);
  const bytes = fs.readFileSync(absolute);
  if (sha256Bytes(bytes) !== record.sha256) throw new Error(`${record.logical_path}: frozen hash drift`);
  return JSON.parse(bytes.toString("utf8"));
}

export function loadAndBuild({root = defaultRoot, productionRepo, contractPath = path.join(here, "TARGET-JOIN-CONTRACT.json")}) {
  const contract = JSON.parse(fs.readFileSync(contractPath, "utf8"));
  const membership = readFrozen(root, contract.frozen_inputs.canonical_membership);
  const snapshot = readFrozen(root, contract.frozen_inputs.provenance_snapshot);
  const frame = readFrozen(root, contract.frozen_inputs.source_screen_frame);
  const packets = readFrozen(root, contract.frozen_inputs.source_evidence_packets);
  readFrozen(root, contract.frozen_inputs.source_screen_contract);
  const terminalFiles = new Map();
  for (const record of expectedTerminalRecords(membership, snapshot)) {
    const absolute = path.resolve(productionRepo, record.logical_path);
    assertInside(productionRepo, absolute, record.logical_path);
    terminalFiles.set(record.logical_path, fs.readFileSync(absolute));
  }
  return buildTargetQueueFromValues({contract, membership, snapshot, frame, packets, terminalFiles});
}

export function writeOutputs(out, outputs) {
  fs.mkdirSync(out, {recursive: true});
  for (const name of OUTPUT_NAMES) fs.writeFileSync(path.join(out, name), jsonBytes(outputs[name]));
}

function parseArgs(argv) {
  const args = {root: defaultRoot};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--root", "--production-repo", "--out"].includes(flag)) throw new Error("usage: node build-target-queue.mjs --production-repo PRODUCTION --out OUTPUT [--root RESEARCH]");
    args[flag.slice(2).replace(/-([a-z])/gu, (_match, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  if (!args.productionRepo || !args.out) throw new Error("--production-repo and --out are required");
  return args;
}

const invoked = process.argv[1] ? pathToFileURL(path.resolve(process.argv[1])).href : null;
if (invoked === import.meta.url) {
  const args = parseArgs(process.argv.slice(2));
  const outputs = loadAndBuild(args);
  writeOutputs(args.out, outputs);
  process.stdout.write(`${JSON.stringify({status: outputs["TARGET-JOIN-REPORT.json"].status, outputs: OUTPUT_NAMES}, null, 2)}\n`);
}
