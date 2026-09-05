#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256, validateAuditCandidate} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node release-context.mjs SURFACE-CANDIDATE-1.json SURFACE-CANDIDATE-2.json SURFACE-CANDIDATE-3.json");
const validations = candidates.map((candidate, index) => validateAuditCandidate(path.resolve(candidate), path.join(here, `CLEAN-AUDIT-SURFACE-SHARD-${index + 1}.json`), "SURFACE", index + 1));
const registry = JSON.parse(fs.readFileSync(path.join(here, "TARGET-BINDING-REGISTRY.json"), "utf8"));
const packets = JSON.parse(fs.readFileSync(path.join(here, "SOURCE-EVIDENCE-PACKETS.json"), "utf8"));
const packetByScreen = new Map(packets.items.map(item => [item.screen_id, item]));
const primary = registry.records.filter(record => record.disposition === "PRIMARY_CLEAN_AUDIT");
if (primary.length !== 120) throw new Error("primary target registry count mismatch");
const report = {schema_version: "source-context-controlled-confirmation-context-release-report-v2", status: "PASS", surface_candidates: validations.map((value, index) => ({shard: index + 1, sha256: value.candidate_sha256})), context_shards: []};
for (let shard = 1; shard <= 3; shard += 1) {
  const records = primary.slice((shard - 1) * 40, shard * 40);
  const queue = {
    schema_version: "source-context-controlled-confirmation-clean-audit-context-shard-v2",
    status: "FROZEN_CONTEXT_RELEASE_AFTER_SURFACE_LOCK",
    pass: "CONTEXT",
    shard,
    surface_candidate_sha256: validations[shard - 1].candidate_sha256,
    instructions: [
      "Review all 40 source/target pairs using the supplied mechanically bound fixed public-source context.",
      "CLEAN means the current target has no objective material defect after considering the packet.",
      "OBJECTIVE_DEFECT requires an exact target span and a claim directly supported by the packet.",
      "UNRESOLVED means the packet is insufficient for a material decision; explain the missing evidence.",
      "Do not make style-only findings, inspect other files, infer from model identity, or omit an item."
    ],
    items: records.map(record => {
      const packet = packetByScreen.get(record.screen_id);
      if (!packet || packet.source_sha256 !== record.source_sha256) throw new Error(`${record.audit_id}: packet binding mismatch`);
      return {audit_id: record.audit_id, profile: record.profile, source: record.source, target: record.target, source_context: packet.occurrence.visible_context, response: null};
    })
  };
  const name = `CLEAN-AUDIT-CONTEXT-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, name), jsonBytes(queue), {flag: "wx"});
  report.context_shards.push({shard, file: name, sha256: sha256(jsonBytes(queue)), count: 40});
}
fs.writeFileSync(path.join(here, "CONTEXT-RELEASE-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
