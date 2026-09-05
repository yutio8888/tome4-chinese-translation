#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node validate-mutation-authors.mjs MUTATION-AUTHOR-CANDIDATE-1.json MUTATION-AUTHOR-CANDIDATE-2.json MUTATION-AUTHOR-CANDIDATE-3.json");
const isSupplement = candidates.every(candidate => path.basename(candidate).startsWith("MUTATION-SUPPLEMENT-CANDIDATE-"));
const exactKeys = (value, keys, label) => {
  const actual = Object.keys(value).sort().join(",");
  const expected = [...keys].sort().join(",");
  if (actual !== expected) throw new Error(`${label}: keys ${actual} != ${expected}`);
};
const contextFamilies = new Set(["speaker_addressee_or_agent_patient", "referent_or_entity_identity", "event_branch_condition_or_scope", "direction_polarity_or_ownership"]);
const claimTypes = new Set(["ACCURACY", "ROLE_OR_REFERENT", "CONDITION_OR_SCOPE", "DIRECTION_OR_POLARITY", "TERMINOLOGY", "OTHER_OBJECTIVE"]);
const baseKeys = ["mutated_target", "edit_span_original", "edit_span_mutated", "claim_type", "severity", "atom", "minimality"];
const validateOption = (option, visible, kind, label) => {
  if (option === null) return;
  const extra = kind === "context" ? ["family", "surface_underdetermined", "context_refutation"] : ["surface_refutation"];
  exactKeys(option, [...baseKeys, ...extra], label);
  for (const key of ["mutated_target", "edit_span_original", "edit_span_mutated", "atom", "minimality", ...extra.filter(value => value !== "family")]) if (typeof option[key] !== "string" || !option[key].trim()) throw new Error(`${label}: ${key} empty`);
  if (!claimTypes.has(option.claim_type) || !new Set(["major", "minor"]).has(option.severity)) throw new Error(`${label}: claim/severity invalid`);
  if (kind === "context" && !contextFamilies.has(option.family)) throw new Error(`${label}: context family invalid`);
  const occurrences = visible.target.split(option.edit_span_original).length - 1;
  if (occurrences !== 1) throw new Error(`${label}: original edit span must occur exactly once, got ${occurrences}`);
  const expected = visible.target.replace(option.edit_span_original, option.edit_span_mutated);
  if (option.mutated_target !== expected || option.mutated_target === visible.target) throw new Error(`${label}: mutation is not the declared single replacement`);
};

const results = candidates.map((candidatePath, offset) => {
  const shard = offset + 1;
  const candidateBytes = fs.readFileSync(path.resolve(candidatePath));
  const queueBytes = fs.readFileSync(path.join(here, `MUTATION-AUTHOR-SHARD-${shard}.json`));
  const candidate = JSON.parse(candidateBytes);
  const queue = JSON.parse(queueBytes);
  exactKeys(candidate, ["schema_version", "shard", "queue_sha256", "items"], `candidate ${shard}`);
  if (candidate.schema_version !== "source-context-controlled-confirmation-mutation-author-candidate-v2" || candidate.shard !== shard || candidate.queue_sha256 !== sha256(queueBytes)) throw new Error(`candidate ${shard}: header mismatch`);
  if (!Array.isArray(candidate.items) || candidate.items.length !== 20) throw new Error(`candidate ${shard}: item count mismatch`);
  for (let index = 0; index < 20; index += 1) {
    const item = candidate.items[index];
    const visible = queue.items[index];
    exactKeys(item, ["base_ordinal", "audit_id", "context_option", "surface_option"], `${shard}.items[${index}]`);
    if (item.base_ordinal !== visible.base_ordinal || item.audit_id !== visible.audit_id) throw new Error(`${shard}.items[${index}]: identity/order mismatch`);
    validateOption(item.context_option, visible, "context", `${item.audit_id}.context_option`);
    validateOption(item.surface_option, visible, "surface", `${item.audit_id}.surface_option`);
  }
  return {
    shard,
    candidate_sha256: sha256(candidateBytes),
    queue_sha256: sha256(queueBytes),
    context_proposals: candidate.items.filter(item => item.context_option !== null).length,
    surface_proposals: candidate.items.filter(item => item.surface_option !== null).length,
    candidate
  };
});
const report = {
  schema_version: isSupplement ? "source-context-controlled-confirmation-mutation-supplement-validation-v2" : "source-context-controlled-confirmation-mutation-author-validation-v2",
  status: "PASS_STRUCTURAL_ONLY_MANIPULATION_CHECK_PENDING",
  candidates: results.map(({candidate, ...result}) => result),
  totals: {
    context_proposals: results.reduce((sum, result) => sum + result.context_proposals, 0),
    surface_proposals: results.reduce((sum, result) => sum + result.surface_proposals, 0)
  }
};
fs.writeFileSync(path.join(here, isSupplement ? "MUTATION-SUPPLEMENT-CANDIDATE-VALIDATION.json" : "MUTATION-AUTHOR-CANDIDATE-VALIDATION.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
