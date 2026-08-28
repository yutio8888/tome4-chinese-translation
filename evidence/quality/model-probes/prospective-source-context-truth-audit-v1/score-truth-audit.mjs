#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {verifyFinalAdjudication} from "./candidate-validation.mjs";

const directory = path.dirname(fileURLToPath(import.meta.url));
const readBytes = name => fs.readFileSync(path.join(directory, name));
const readJson = name => JSON.parse(readBytes(name).toString("utf8"));
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const binding = name => {
  const bytes = readBytes(name);
  return {file: name, sha256: sha256(bytes), size_bytes: bytes.length};
};

const adjudicationBytes = readBytes("FINAL-ADJUDICATION.json");
const adjudication = verifyFinalAdjudication({
  auditQueueBytes: readBytes("AUDIT-QUEUE.json"),
  surfaceQueueBytes: [1, 2, 3].map(shard => readBytes(`SURFACE-QUEUE-${shard}.json`)),
  contextQueueBytes: [1, 2, 3].map(shard => readBytes(`CONTEXT-QUEUE-${shard}.json`)),
  surfaceCandidateBytes: [1, 2, 3].map(shard => readBytes(`SURFACE-CANDIDATE-${shard}.json`)),
  contextCandidateBytes: [1, 2, 3].map(shard => readBytes(`CONTEXT-CANDIDATE-${shard}.json`)),
  adjudicationBytes
});
const contract = readJson("AUDIT-CONTRACT.json");

const labels = ["CONTEXT_DEPENDENT_DEFECT", "SURFACE_VISIBLE_DEFECT", "MIXED_DEFECT", "CLEAN", "UNRESOLVED"];
const categories = ["Runtime", "Narrative"];
const countBy = (items, key) => Object.fromEntries(key.map(value => [value, items.filter(item => item.final_label === value).length]));
const poolStats = items => ({
  items: items.length,
  tasks: new Set(items.map(item => item.task_id)).size,
  categories: Object.fromEntries(categories.map(category => [category, items.filter(item => item.category === category).length])),
  packet_sufficient_items: items.filter(item => item.packet_sufficient).length
});
const candidateCounts = prefix => {
  const items = [1, 2, 3].flatMap(shard => readJson(`${prefix}-${shard}.json`).items);
  return Object.fromEntries(labels.map(label => [label, items.filter(item => item.label === label).length]));
};

const determinate = adjudication.items.filter(item => item.determinate);
const contextPool = adjudication.items.filter(item => item.final_label === "CONTEXT_DEPENDENT_DEFECT" && item.packet_sufficient);
const surfacePool = adjudication.items.filter(item => item.final_label === "SURFACE_VISIBLE_DEFECT");
const cleanPool = adjudication.items.filter(item => item.final_label === "CLEAN");
const stats = {
  context_cases: poolStats(contextPool),
  surface_controls: poolStats(surfacePool),
  clean_controls: poolStats(cleanPool)
};
const gate = contract.glm_pilot_gate;
const failures = [];
if (determinate.length < gate.minimum_determinate_items) failures.push(`determinate_items ${determinate.length} < ${gate.minimum_determinate_items}`);
for (const [poolName, pool] of Object.entries(stats)) {
  const minimum = gate.pools[poolName];
  if (pool.items < minimum.minimum_items) failures.push(`${poolName}.items ${pool.items} < ${minimum.minimum_items}`);
  if (pool.tasks < minimum.minimum_tasks) failures.push(`${poolName}.tasks ${pool.tasks} < ${minimum.minimum_tasks}`);
  for (const category of categories) {
    if (pool.categories[category] < minimum.minimum_per_category) failures.push(`${poolName}.${category} ${pool.categories[category]} < ${minimum.minimum_per_category}`);
  }
}

const challengerBindings = [1, 2, 3].map(shard => {
  const name = `CHALLENGER-${shard}.json`;
  const bytes = readBytes(name);
  const challenger = JSON.parse(bytes.toString("utf8"));
  const finalById = new Map(adjudication.items.map(item => [item.audit_id, item.final_label]));
  const disagreements = challenger.items.filter(item => finalById.get(item.audit_id) !== item.proposed_final_label).map(item => ({
    audit_id: item.audit_id,
    challenger_label: item.proposed_final_label,
    final_label: finalById.get(item.audit_id)
  }));
  return {
    shard_id: shard,
    sha256: sha256(bytes),
    size_bytes: bytes.length,
    items: challenger.items.length,
    matches_final: challenger.items.length - disagreements.length,
    disagreements
  };
});

const result = {
  schema_version: "prospective-source-context-truth-audit-result-v1",
  experiment: "prospective-source-context-truth-audit-v1",
  status: failures.length === 0 ? "GO_FORMAL_GLM_PILOT" : "NO_GO_INSUFFICIENT_TRUTH_SET",
  date_completed: "2026-08-28",
  measured: {
    items: adjudication.items.length,
    determinate_items: determinate.length,
    labels: countBy(adjudication.items, labels),
    categories: Object.fromEntries(categories.map(category => [category, adjudication.items.filter(item => item.category === category).length])),
    candidate_labels: {
      surface_pass: candidateCounts("SURFACE-CANDIDATE"),
      context_pass: candidateCounts("CONTEXT-CANDIDATE")
    },
    pools: stats
  },
  formal_glm_gate: {
    route_candidate: gate.route_and_evaluation.route_candidate,
    decision: failures.length === 0 ? "GO" : "NO_GO",
    failures,
    thresholds_relaxed: false,
    replacements_made: false,
    pilot_sample_generated: failures.length === 0,
    model_calls: 0,
    explanation: failures.length === 0
      ? "All pre-registered truth-set minima passed."
      : "The frozen truth set does not contain enough eligible context-dependent cases, and its surface-defect pool has no Runtime case. The formal GLM pilot must not run under the pre-registered contract."
  },
  exploratory_policy: {
    allowed_after_this_no_go: true,
    separation: "OpenAI/Codex, Claude and GLM may participate in a separately versioned exploratory experiment using frozen inputs, but those results cannot be reported as the formal GLM pilot or used to relax this gate.",
    formal_result_impact: "none"
  },
  lead_review: {
    all_items_verified: true,
    decision_method: "Independent lead review of all 120 source-target pairs and frozen packets; challenger identity, vote count and harsher label were not decision rules.",
    supplemental_evidence: binding("LEAD-SUPPLEMENTAL-EVIDENCE.json"),
    challenger_outputs: challengerBindings
  },
  bindings: {
    audit_contract: binding("AUDIT-CONTRACT.json"),
    audit_queue: binding("AUDIT-QUEUE.json"),
    final_adjudication: {file: "FINAL-ADJUDICATION.json", sha256: sha256(adjudicationBytes), size_bytes: adjudicationBytes.length},
    executor_fixture_expected_sha256: "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7"
  },
  limitations: [
    "The 120-item screen yielded only one pure context-dependent defect, so it cannot support the frozen 8-case context arm.",
    "All five determinate surface-visible defects are Narrative; the required Runtime surface control is absent.",
    "V1-010, V1-111 and V1-113 required lead-only supplemental fixed-source or terminology evidence outside the 12-line item packet; these materials are excluded from downstream model inputs.",
    "V1-076 remains unresolved because the frozen packet does not bind the identity of 'the shadow'."
  ]
};

fs.writeFileSync(path.join(directory, "RESULT.json"), `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: result.status, determinate_items: determinate.length, labels: result.measured.labels, failures}, null, 2)}\n`);
