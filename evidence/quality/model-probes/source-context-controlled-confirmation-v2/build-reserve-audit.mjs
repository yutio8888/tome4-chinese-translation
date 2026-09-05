#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const registryBytes = fs.readFileSync(path.join(here, "TARGET-BINDING-REGISTRY.json"));
const localBytes = fs.readFileSync(path.join(here, "LOCAL-AUDIT-SOURCE-BINDINGS.json"));
const registry = JSON.parse(registryBytes);
const local = JSON.parse(localBytes);
const localByScreen = new Map(local.ordered_reserves.map(item => [item.screen_id, item]));

const records = registry.records
  .filter(record => record.disposition === "ORDERED_RESERVE_NOT_RELEASED" && record.profile === "narrative")
  .sort((a, b) => a.reserve_ordinal - b.reserve_ordinal);
if (records.length !== 60 || records[0].reserve_ordinal !== 61 || records.at(-1).reserve_ordinal !== 120) throw new Error("narrative reserve range mismatch");

const report = {
  schema_version: "source-context-controlled-confirmation-reserve-audit-build-v2",
  status: "FROZEN_ORDERED_NARRATIVE_RESERVE_AUDIT",
  reason: "The primary clean audit can supply at most 26 narrative bases under the frozen two-items-per-source-file cap; ordered narrative reserves are audited before clean lock and before inference.",
  registry_sha256: sha256(registryBytes),
  local_bindings_sha256: sha256(localBytes),
  reserve_range: {first: 61, last: 120, count: 60},
  shards: []
};

for (let offset = 0; offset < 3; offset += 1) {
  const shard = offset + 4;
  const shardRecords = records.slice(offset * 20, (offset + 1) * 20);
  const queue = {
    schema_version: "source-context-controlled-confirmation-clean-audit-surface-shard-v2",
    status: "FROZEN_SURFACE_FIRST_ORDERED_RESERVE_AUDIT",
    pass: "SURFACE",
    shard,
    instructions: [
      "Review all 20 source/target pairs using only the visible source and target.",
      "CLEAN means no objective material bilingual or structural defect is visible.",
      "OBJECTIVE_DEFECT requires an exact target span and a surface-decidable claim.",
      "UNRESOLVED means a material question requires context; explain what is missing.",
      "Do not inspect context or other files, make style-only findings, or omit an item."
    ],
    items: shardRecords.map(record => ({
      audit_id: `R${String(record.reserve_ordinal).padStart(3, "0")}`,
      profile: record.profile,
      source: record.source,
      target: record.target,
      response: null
    }))
  };
  const name = `CLEAN-AUDIT-RESERVE-SURFACE-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, name), jsonBytes(queue), {flag: "wx"});
  report.shards.push({shard, file: name, sha256: sha256(jsonBytes(queue)), first_id: queue.items[0].audit_id, last_id: queue.items.at(-1).audit_id, count: 20});
}

const binding = {
  schema_version: "source-context-controlled-confirmation-reserve-audit-binding-v2",
  status: "LOCAL_ONLY_NO_MODEL_EXPOSURE",
  items: records.map(record => {
    const localRecord = localByScreen.get(record.screen_id);
    if (!localRecord) throw new Error(`${record.screen_id}: local reserve binding missing`);
    return {
      audit_id: `R${String(record.reserve_ordinal).padStart(3, "0")}`,
      screen_id: record.screen_id,
      reserve_ordinal: record.reserve_ordinal,
      revision_id: record.canonical_identity.revision_id,
      relative_path: localRecord.relative_path,
      context_sha256: localRecord.context_sha256
    };
  })
};
fs.writeFileSync(path.join(here, "LOCAL-RESERVE-AUDIT-BINDINGS.json"), jsonBytes(binding), {flag: "wx"});
report.local_binding_sha256 = sha256(jsonBytes(binding));
fs.writeFileSync(path.join(here, "RESERVE-AUDIT-BUILD-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
