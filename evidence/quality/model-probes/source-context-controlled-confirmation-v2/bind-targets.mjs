#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const expectedInventoryFileSha256 = "fceec52bdc2888542024f059c842a85230d8ecb396992be43b1bf8310aef5ea3";
const expectedInventorySha256 = "bf9153e83aba7318741f065d8541ae74783eebc5d4552ec38627a4313456b215";
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");

function parseArgs(argv) {
  if (argv.length !== 2 || argv[0] !== "--inventory") throw new Error("usage: node bind-targets.mjs --inventory INVENTORY_JSONL");
  return {inventory: path.resolve(argv[1])};
}

function loadInventory(file) {
  const bytes = fs.readFileSync(file);
  if (sha256(bytes) !== expectedInventoryFileSha256) throw new Error("inventory file hash mismatch");
  const rows = bytes.toString("utf8").split("\n").filter(Boolean).map(JSON.parse);
  if (rows.length !== 30308) throw new Error("inventory row count mismatch");
  return new Map(rows.map(row => [row.revision_id, row]));
}

export function buildTargetBinding(inventoryFile) {
  const screenBytes = fs.readFileSync(path.join(here, "SOURCE-SCREEN-FRAME.json"));
  const selectionBytes = fs.readFileSync(path.join(here, "AUDIT-SOURCE-SELECTION.json"));
  const bindingBytes = fs.readFileSync(path.join(here, "LOCAL-SCREEN-BINDINGS.json"));
  const screen = JSON.parse(screenBytes);
  const selection = JSON.parse(selectionBytes);
  const sourceBindings = JSON.parse(bindingBytes);
  const screenById = new Map(screen.items.map(item => [item.screen_id, item]));
  const localById = new Map(sourceBindings.items.map(item => [item.screen_id, item]));
  const inventory = loadInventory(inventoryFile);
  const ordered = [...selection.primary, ...selection.ordered_reserves];
  if (new Set(ordered.map(item => item.screen_id)).size !== 240) throw new Error("audit selection does not cover 240 unique screen items");
  const records = ordered.map((selected, index) => {
    const screenItem = screenById.get(selected.screen_id);
    const local = localById.get(selected.screen_id);
    if (!screenItem || !local) throw new Error(`${selected.screen_id}: missing screen binding`);
    const row = inventory.get(local.revision_id);
    if (!row) throw new Error(`${selected.screen_id}: inventory revision missing`);
    if (row.source !== screenItem.source || sha256(row.source) !== screenItem.source_sha256) throw new Error(`${selected.screen_id}: source drift`);
    for (const key of ["revision_uid", "tu_uid", "unit_id"]) if (row[key] !== local[key]) throw new Error(`${selected.screen_id}: ${key} drift`);
    if (typeof row.target !== "string" || !row.target.trim()) throw new Error(`${selected.screen_id}: empty target`);
    const isPrimary = index < 120;
    return {
      screen_id: selected.screen_id,
      audit_id: isPrimary ? `A${String(index + 1).padStart(3, "0")}` : null,
      reserve_ordinal: isPrimary ? null : index - 119,
      disposition: isPrimary ? "PRIMARY_CLEAN_AUDIT" : "ORDERED_RESERVE_NOT_RELEASED",
      canonical_identity: {
        revision_id: row.revision_id,
        revision_uid: row.revision_uid,
        tu_uid: row.tu_uid,
        unit_id: row.unit_id
      },
      component: row.component,
      profile: row.profile,
      section: row.section,
      source_tag: row.source_tag,
      source: row.source,
      source_sha256: sha256(row.source),
      target: row.target,
      target_sha256: sha256(row.target),
      gate_signals: row.gate_signals,
      structure: row.structure
    };
  });
  const registry = {
    schema_version: "source-context-controlled-confirmation-target-binding-registry-v2",
    status: "LOCAL_ONLY_TARGET_BOUND_AFTER_SOURCE_SELECTION_FREEZE",
    production_translation_commit: "1666481409f4c0d63d66e84659f6b6145d8d25d0",
    inventory_sha256: expectedInventorySha256,
    inventory_file_sha256: expectedInventoryFileSha256,
    source_screen_sha256: sha256(screenBytes),
    audit_source_selection_sha256: sha256(selectionBytes),
    counts: {records: 240, primary: 120, reserves: 120},
    records
  };
  const primaryRecords = records.slice(0, 120);
  const queue = {
    schema_version: "source-context-controlled-confirmation-clean-audit-surface-queue-v2",
    status: "FROZEN_SURFACE_FIRST_QUEUE_CONTEXT_WITHHELD",
    target_binding_registry_sha256: sha256(jsonBytes(registry)),
    audit_source_selection_sha256: sha256(selectionBytes),
    instructions: "Review source and target only. Report objective translation defects and structural defects. Do not infer or request source-code context in this pass.",
    items: primaryRecords.map(record => ({audit_id: record.audit_id, profile: record.profile, source: record.source, target: record.target, response: null}))
  };
  const report = {
    schema_version: "source-context-controlled-confirmation-target-bind-report-v2",
    status: "PASS",
    model_calls: 0,
    network_calls: 0,
    source_selection_frozen_before_target_binding: true,
    counts: {bound: records.length, primary: primaryRecords.length, reserves: 120, empty_targets: 0},
    hashes: {target_binding_registry: sha256(jsonBytes(registry)), surface_queue: sha256(jsonBytes(queue))}
  };
  return {"TARGET-BINDING-REGISTRY.json": registry, "CLEAN-AUDIT-SURFACE-QUEUE.json": queue, "TARGET-BIND-REPORT.json": report};
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const args = parseArgs(process.argv.slice(2));
  const outputs = buildTargetBinding(args.inventory);
  for (const [name, value] of Object.entries(outputs)) fs.writeFileSync(path.join(here, name), jsonBytes(value), {flag: "wx"});
  console.log(JSON.stringify(outputs["TARGET-BIND-REPORT.json"], null, 2));
}
