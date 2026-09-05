#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const frameBytes = fs.readFileSync(path.join(here, "SELECTED-BASE-FRAME.json"));
const frame = JSON.parse(frameBytes);
const baseByAudit = new Map(frame.items.map(item => [item.audit_id, item]));
const candidateInputs = [];
for (const source of ["PRIMARY", "SUPPLEMENT"]) {
  for (let shard = 1; shard <= 3; shard += 1) {
    const filename = source === "PRIMARY" ? `MUTATION-AUTHOR-CANDIDATE-${shard}.json` : `MUTATION-SUPPLEMENT-CANDIDATE-${shard}.json`;
    const bytes = fs.readFileSync(path.join(here, filename));
    candidateInputs.push({source, shard, filename, sha256: sha256(bytes), candidate: JSON.parse(bytes)});
  }
}
const dedup = new Map();
for (const input of candidateInputs) {
  for (const item of input.candidate.items) {
    if (!item.context_option) continue;
    const base = baseByAudit.get(item.audit_id);
    if (!base || base.base_ordinal !== item.base_ordinal) throw new Error(`${item.audit_id}: mutation/base binding mismatch`);
    const key = sha256(Buffer.from(`${item.audit_id}\0${item.context_option.mutated_target}`, "utf8"));
    if (!dedup.has(key)) dedup.set(key, {base, option: item.context_option, sources: []});
    dedup.get(key).sources.push({source: input.source, shard: input.shard, candidate_sha256: input.sha256});
  }
}
const proposals = [...dedup.values()].sort((a, b) => a.base.base_ordinal - b.base.base_ordinal || a.option.mutated_target.localeCompare(b.option.mutated_target)).map((value, index) => ({
  proposal_id: `P${String(index + 1).padStart(3, "0")}`,
  base_ordinal: value.base.base_ordinal,
  audit_id: value.base.audit_id,
  profile: value.base.profile,
  relative_path: value.base.relative_path,
  revision_id: value.base.revision_id,
  source: value.base.source,
  clean_target: value.base.target,
  mutated_target: value.option.mutated_target,
  source_context: value.base.source_context,
  proposal: value.option,
  proposal_sources: value.sources
}));
if (proposals.length < 24) throw new Error(`only ${proposals.length} unique context proposals`);
const pool = {
  schema_version: "source-context-controlled-confirmation-context-mutation-proposal-pool-v2",
  status: "FROZEN_BEFORE_A_ONLY_MANIPULATION_CHECK",
  selected_base_frame_sha256: sha256(frameBytes),
  candidate_inputs: candidateInputs.map(({candidate, ...input}) => input),
  count: proposals.length,
  items: proposals
};
fs.writeFileSync(path.join(here, "CONTEXT-MUTATION-PROPOSAL-POOL.json"), jsonBytes(pool), {flag: "wx"});

const sizes = [Math.ceil(proposals.length / 3), Math.ceil(proposals.length / 3), proposals.length - 2 * Math.ceil(proposals.length / 3)];
let cursor = 0;
const report = {
  schema_version: "source-context-controlled-confirmation-manipulation-a-only-build-v2",
  status: "FROZEN_A_ONLY_CONTEXT_NOT_RELEASED",
  proposal_pool_sha256: sha256(jsonBytes(pool)),
  shards: []
};
for (let shard = 1; shard <= 3; shard += 1) {
  const items = proposals.slice(cursor, cursor + sizes[shard - 1]);
  cursor += sizes[shard - 1];
  const queue = {
    schema_version: "source-context-controlled-confirmation-manipulation-check-queue-v2",
    status: "FROZEN_A_ONLY_NO_CONTEXT_OR_EXPECTED_ATOM",
    pass: "A_ONLY",
    shard,
    instructions: [
      "Judge the supplied source and mutated target only. Do not inspect context, other files or expected claims.",
      "NO_OBJECTIVE_DEFECT_VISIBLE means the pair is materially plausible or underdetermined on its face; style preferences do not count.",
      "EXACTLY_ONE_OBJECTIVE_DEFECT means one material bilingual or structural defect is objectively decidable from this pair alone.",
      "MULTIPLE_OR_STRUCTURALLY_INVALID means two or more material defects or a broken placeholder/markup/format structure are visible.",
      "UNRESOLVED is only for a material ambiguity you cannot classify; explain what evidence is missing."
    ],
    items: items.map(item => ({proposal_id: item.proposal_id, profile: item.profile, source: item.source, target: item.mutated_target, response: null}))
  };
  const filename = `MANIPULATION-A-ONLY-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, filename), jsonBytes(queue), {flag: "wx"});
  report.shards.push({shard, file: filename, sha256: sha256(jsonBytes(queue)), count: items.length, first_id: items[0].proposal_id, last_id: items.at(-1).proposal_id});
}
fs.writeFileSync(path.join(here, "MANIPULATION-A-ONLY-BUILD-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify({...report, proposal_count: proposals.length}, null, 2));
