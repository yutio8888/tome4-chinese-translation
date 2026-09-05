#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";
import {validateManipulationCandidate} from "./manipulation-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node release-manipulation-context.mjs MANIPULATION-A-CANDIDATE-1.json MANIPULATION-A-CANDIDATE-2.json MANIPULATION-A-CANDIDATE-3.json");
const validations = candidates.map((candidate, offset) => validateManipulationCandidate(path.resolve(candidate), path.join(here, `MANIPULATION-A-ONLY-SHARD-${offset + 1}.json`), "A_ONLY", offset + 1));
const poolBytes = fs.readFileSync(path.join(here, "CONTEXT-MUTATION-PROPOSAL-POOL.json"));
const pool = JSON.parse(poolBytes);
const byId = new Map(pool.items.map(item => [item.proposal_id, item]));
const report = {
  schema_version: "source-context-controlled-confirmation-manipulation-context-release-v2",
  status: "PASS_A_ONLY_LOCKED_CONTEXT_RELEASED",
  proposal_pool_sha256: sha256(poolBytes),
  a_only_candidates: validations.map((value, offset) => ({shard: offset + 1, sha256: value.candidate_sha256, counts: value.candidate.items.reduce((acc, item) => (acc[item.verdict] += 1, acc), {NO_OBJECTIVE_DEFECT_VISIBLE: 0, EXACTLY_ONE_OBJECTIVE_DEFECT: 0, MULTIPLE_OR_STRUCTURALLY_INVALID: 0, UNRESOLVED: 0})})),
  shards: []
};
for (let offset = 0; offset < 3; offset += 1) {
  const shard = offset + 1;
  const aQueue = validations[offset].queue;
  const queue = {
    schema_version: "source-context-controlled-confirmation-manipulation-check-queue-v2",
    status: "FROZEN_B_CONTEXT_AFTER_A_ONLY_LOCK",
    pass: "B_CONTEXT",
    shard,
    a_only_candidate_sha256: validations[offset].candidate_sha256,
    instructions: [
      "Judge the supplied source and mutated target using only the supplied mechanical source_context. Do not inspect other files or expected atoms.",
      "NO_OBJECTIVE_DEFECT_VISIBLE means the packet does not objectively refute the target.",
      "EXACTLY_ONE_OBJECTIVE_DEFECT means the packet uniquely supports one material defect; report the exact target span and claim.",
      "MULTIPLE_OR_STRUCTURALLY_INVALID means two or more material defects or a broken structure are supported.",
      "UNRESOLVED means the packet is insufficient for a material decision; explain the missing evidence."
    ],
    items: aQueue.items.map(visible => {
      const item = byId.get(visible.proposal_id);
      if (!item || item.source !== visible.source || item.mutated_target !== visible.target) throw new Error(`${visible.proposal_id}: pool/A binding mismatch`);
      return {proposal_id: item.proposal_id, profile: item.profile, source: item.source, target: item.mutated_target, source_context: item.source_context, response: null};
    })
  };
  const filename = `MANIPULATION-B-CONTEXT-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, filename), jsonBytes(queue), {flag: "wx"});
  report.shards.push({shard, file: filename, sha256: sha256(jsonBytes(queue)), count: queue.items.length, first_id: queue.items[0].proposal_id, last_id: queue.items.at(-1).proposal_id});
}
fs.writeFileSync(path.join(here, "MANIPULATION-CONTEXT-RELEASE-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
