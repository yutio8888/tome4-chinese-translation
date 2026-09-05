#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256, validateAuditCandidate} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node release-reserve-context.mjs RESERVE-SURFACE-CANDIDATE-4.json RESERVE-SURFACE-CANDIDATE-5.json RESERVE-SURFACE-CANDIDATE-6.json");
const validations = candidates.map((candidate, offset) => {
  const shard = offset + 4;
  return validateAuditCandidate(path.resolve(candidate), path.join(here, `CLEAN-AUDIT-RESERVE-SURFACE-SHARD-${shard}.json`), "SURFACE", shard);
});
const registry = JSON.parse(fs.readFileSync(path.join(here, "TARGET-BINDING-REGISTRY.json"), "utf8"));
const packets = JSON.parse(fs.readFileSync(path.join(here, "SOURCE-EVIDENCE-PACKETS.json"), "utf8"));
const packetByScreen = new Map(packets.items.map(item => [item.screen_id, item]));
const records = registry.records
  .filter(record => record.disposition === "ORDERED_RESERVE_NOT_RELEASED" && record.profile === "narrative")
  .sort((a, b) => a.reserve_ordinal - b.reserve_ordinal);
if (records.length !== 60 || records[0].reserve_ordinal !== 61 || records.at(-1).reserve_ordinal !== 120) throw new Error("narrative reserve range mismatch");

const report = {
  schema_version: "source-context-controlled-confirmation-reserve-context-release-v2",
  status: "PASS",
  surface_candidates: validations.map((value, offset) => ({shard: offset + 4, sha256: value.candidate_sha256})),
  context_shards: []
};
for (let offset = 0; offset < 3; offset += 1) {
  const shard = offset + 4;
  const shardRecords = records.slice(offset * 20, (offset + 1) * 20);
  const queue = {
    schema_version: "source-context-controlled-confirmation-clean-audit-context-shard-v2",
    status: "FROZEN_CONTEXT_RELEASE_AFTER_RESERVE_SURFACE_LOCK",
    pass: "CONTEXT",
    shard,
    surface_candidate_sha256: validations[offset].candidate_sha256,
    instructions: [
      "Review all 20 source/target pairs using the supplied mechanically bound fixed public-source context.",
      "CLEAN means the current target has no objective material defect after considering the packet.",
      "OBJECTIVE_DEFECT requires an exact target span and a claim directly supported by the packet.",
      "UNRESOLVED means the packet is insufficient for a material decision; explain the missing evidence.",
      "Do not make style-only findings, inspect other files, infer from model identity, or omit an item."
    ],
    items: shardRecords.map(record => {
      const packet = packetByScreen.get(record.screen_id);
      if (!packet || packet.source_sha256 !== record.source_sha256) throw new Error(`${record.screen_id}: packet binding mismatch`);
      return {
        audit_id: `R${String(record.reserve_ordinal).padStart(3, "0")}`,
        profile: record.profile,
        source: record.source,
        target: record.target,
        source_context: packet.occurrence.visible_context,
        response: null
      };
    })
  };
  const name = `CLEAN-AUDIT-RESERVE-CONTEXT-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, name), jsonBytes(queue), {flag: "wx"});
  report.context_shards.push({shard, file: name, sha256: sha256(jsonBytes(queue)), count: 20});
}
fs.writeFileSync(path.join(here, "RESERVE-CONTEXT-RELEASE-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
