#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const frameBytes = fs.readFileSync(path.join(here, "SELECTED-BASE-FRAME.json"));
const frame = JSON.parse(frameBytes);
if (frame.status !== "FROZEN_CLEAN_BASE_FRAME_ROLE_ASSIGNMENT_PENDING" || frame.items.length !== 60) throw new Error("selected base frame mismatch");
const dialogue = frame.items.filter(item => item.profile === "dialogue");
const narrative = frame.items.filter(item => item.profile === "narrative");
if (dialogue.length !== 30 || narrative.length !== 30) throw new Error("profile frame mismatch");

const report = {
  schema_version: "source-context-controlled-confirmation-mutation-author-shard-report-v2",
  status: "FROZEN_MUTATION_AUTHOR_INPUTS_NO_ROLE_ASSIGNMENT",
  selected_base_frame_sha256: sha256(frameBytes),
  shards: []
};
for (let offset = 0; offset < 3; offset += 1) {
  const shard = offset + 1;
  const items = [...dialogue.slice(offset * 10, (offset + 1) * 10), ...narrative.slice(offset * 10, (offset + 1) * 10)];
  const queue = {
    schema_version: "source-context-controlled-confirmation-mutation-author-queue-v2",
    status: "FROZEN_PROPOSAL_INPUT_NOT_REFERENCE",
    shard,
    instructions: [
      "For each clean base, propose at most one context-required mutation and at most one surface-visible mutation; use null when no honest minimal single-atom proposal exists.",
      "A context proposal must remain objectively underdetermined from source plus mutated target alone, while the supplied mechanical source_context uniquely refutes exactly one material atom.",
      "A surface proposal must be objectively refutable from source plus mutated target without source_context.",
      "Preserve all unrelated meaning, placeholders, markup and formatting. Replace one minimal exact target span; do not rewrite the sentence or invent a second defect.",
      "Do not assign experimental roles, optimize for a desired effect, inspect other files or mention expected model behavior."
    ],
    items: items.map(item => ({
      base_ordinal: item.base_ordinal,
      audit_id: item.audit_id,
      profile: item.profile,
      source: item.source,
      target: item.target,
      source_context: item.source_context,
      response: null
    }))
  };
  const name = `MUTATION-AUTHOR-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, name), jsonBytes(queue), {flag: "wx"});
  report.shards.push({shard, file: name, sha256: sha256(jsonBytes(queue)), count: 20, dialogue: 10, narrative: 10});
}
fs.writeFileSync(path.join(here, "MUTATION-AUTHOR-SHARD-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
