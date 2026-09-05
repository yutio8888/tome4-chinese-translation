#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = name => fs.readFileSync(path.join(here, name));
const frameBytes = read("SELECTED-BASE-FRAME.json");
const poolBytes = read("CONTEXT-MUTATION-PROPOSAL-POOL.json");
const amendmentBytes = read("DESIGN-AMENDMENT-006.json");
const p038Bytes = read("MANIPULATION-LEAD-SUPPLEMENT-001.json");
const frame = JSON.parse(frameBytes);
const pool = JSON.parse(poolBytes);
const p038 = JSON.parse(p038Bytes).proposal;
const baseByAudit = new Map(frame.items.map(item => [item.audit_id, item]));
const proposalById = new Map(pool.items.map(item => [item.proposal_id, item]));
proposalById.set("P038", {
  proposal_id: "P038",
  base_ordinal: p038.base_ordinal,
  audit_id: p038.audit_id,
  profile: p038.profile,
  source: p038.source,
  clean_target: p038.clean_target,
  mutated_target: p038.mutated_target,
  source_context: baseByAudit.get(p038.audit_id).source_context,
  proposal: {
    family: p038.family,
    claim_type: p038.claim_type,
    severity: p038.severity,
    atom: p038.atom,
    edit_span_original: p038.edit_span_original,
    edit_span_mutated: p038.edit_span_mutated,
    mutated_target: p038.mutated_target,
    surface_underdetermined: p038.surface_underdetermined,
    context_refutation: p038.context_refutation
  }
});

const acceptedIds = [
  "P001", "P002", "P004", "P005", "P007", "P010", "P011", "P012", "P016", "P017", "P018", "P021",
  "P023", "P024", "P026", "P027", "P029", "P030", "P032", "P033", "P035", "P036", "P037", "P038"
];
const familyOverrides = new Map([
  ["P007", "direction_polarity_or_ownership"],
  ["P030", "direction_polarity_or_ownership"]
]);
const accepted = acceptedIds.map(proposalId => {
  const proposal = proposalById.get(proposalId);
  if (!proposal) throw new Error(`${proposalId}: accepted proposal missing`);
  const base = baseByAudit.get(proposal.audit_id);
  if (!base || base.base_ordinal !== proposal.base_ordinal || base.source !== proposal.source || base.target !== proposal.clean_target || base.source_context !== proposal.source_context) throw new Error(`${proposalId}: accepted proposal binding mismatch`);
  return {...proposal, final_family: familyOverrides.get(proposalId) ?? proposal.proposal.family};
});
if (new Set(accepted.map(item => item.audit_id)).size !== 24) throw new Error("accepted context proposals do not use 24 unique bases");

const contextProfileCounts = accepted.reduce((acc, item) => (acc[item.profile] += 1, acc), {dialogue: 0, narrative: 0});
const familyCounts = accepted.reduce((acc, item) => (acc[item.final_family] += 1, acc), {speaker_addressee_or_agent_patient: 0, referent_or_entity_identity: 0, event_branch_condition_or_scope: 0, direction_polarity_or_ownership: 0});
if (contextProfileCounts.dialogue !== 12 || contextProfileCounts.narrative !== 12 || JSON.stringify(familyCounts) !== JSON.stringify({speaker_addressee_or_agent_patient: 3, referent_or_entity_identity: 8, event_branch_condition_or_scope: 10, direction_polarity_or_ownership: 3})) throw new Error("accepted context balance mismatch");

const authorCandidates = [];
for (let shard = 1; shard <= 3; shard += 1) authorCandidates.push(...JSON.parse(read(`MUTATION-AUTHOR-CANDIDATE-${shard}.json`)).items);
const surfaceByAudit = new Map(authorCandidates.map(item => [item.audit_id, item.surface_option]));
if ([...surfaceByAudit.values()].some(value => !value)) throw new Error("surface proposal coverage incomplete");

const contextAuditIds = new Set(accepted.map(item => item.audit_id));
const roleSeed = "source-context-controlled-confirmation-v2/final-assignment/2026-08-28/remaining-role";
const roleRank = revisionId => crypto.createHash("sha256").update(`${roleSeed}\0${revisionId}`).digest("hex");
const surfaceBases = [];
const cleanBases = [];
for (const profile of ["dialogue", "narrative"]) {
  const remaining = frame.items.filter(item => item.profile === profile && !contextAuditIds.has(item.audit_id)).sort((a, b) => roleRank(a.revision_id).localeCompare(roleRank(b.revision_id)));
  if (remaining.length !== 18) throw new Error(`${profile}: remaining base count mismatch`);
  surfaceBases.push(...remaining.slice(0, 6));
  cleanBases.push(...remaining.slice(6));
}

const publicItems = [];
const referenceItems = [];
const addPublic = (itemId, role, base, target, mutationFamily = null, proposalId = null) => {
  publicItems.push({
    item_id: itemId,
    role,
    profile: base.profile,
    audit_id: base.audit_id,
    revision_id: base.revision_id,
    relative_path: base.relative_path,
    source: base.source,
    target,
    source_context: base.source_context,
    source_sha256: base.source_sha256,
    clean_target_sha256: base.target_sha256,
    presented_target_sha256: sha256(Buffer.from(target, "utf8")),
    context_sha256: base.context_sha256,
    mutation_family: mutationFamily,
    proposal_id: proposalId
  });
};

accepted.forEach((item, index) => {
  const base = baseByAudit.get(item.audit_id);
  const itemId = `C${String(index + 1).padStart(3, "0")}`;
  addPublic(itemId, "CONTEXT_MUTANT", base, item.mutated_target, item.final_family, item.proposal_id);
  referenceItems.push({item_id: itemId, role: "CONTEXT_MUTANT", proposal_id: item.proposal_id, audit_id: item.audit_id, expected_atom: item.proposal.atom, claim_type: item.proposal.claim_type, severity: item.proposal.severity, target_span: item.proposal.edit_span_mutated, family: item.final_family});
});
surfaceBases.forEach((base, index) => {
  const option = surfaceByAudit.get(base.audit_id);
  const itemId = `S${String(index + 1).padStart(3, "0")}`;
  addPublic(itemId, "SURFACE_MUTANT", base, option.mutated_target);
  referenceItems.push({item_id: itemId, role: "SURFACE_MUTANT", proposal_id: null, audit_id: base.audit_id, expected_atom: option.atom, claim_type: option.claim_type, severity: option.severity, target_span: option.edit_span_mutated, family: null});
});
cleanBases.forEach((base, index) => {
  const itemId = `K${String(index + 1).padStart(3, "0")}`;
  addPublic(itemId, "CLEAN_CONTROL", base, base.target);
  referenceItems.push({item_id: itemId, role: "CLEAN_CONTROL", proposal_id: null, audit_id: base.audit_id, expected_atom: null, claim_type: null, severity: null, target_span: null, family: null});
});

const roleCounts = publicItems.reduce((acc, item) => (acc[item.role] += 1, acc), {CONTEXT_MUTANT: 0, SURFACE_MUTANT: 0, CLEAN_CONTROL: 0});
const roleProfiles = publicItems.reduce((acc, item) => (acc[item.role][item.profile] += 1, acc), {CONTEXT_MUTANT: {dialogue: 0, narrative: 0}, SURFACE_MUTANT: {dialogue: 0, narrative: 0}, CLEAN_CONTROL: {dialogue: 0, narrative: 0}});
if (JSON.stringify(roleCounts) !== JSON.stringify({CONTEXT_MUTANT: 24, SURFACE_MUTANT: 12, CLEAN_CONTROL: 24}) || Object.values(roleProfiles).some(value => value.dialogue !== value.narrative)) throw new Error("final role balance mismatch");
if (new Set(publicItems.map(item => item.audit_id)).size !== 60 || new Set(publicItems.map(item => item.revision_id)).size !== 60) throw new Error("final sample base uniqueness failure");

const lead = {
  schema_version: "source-context-controlled-confirmation-manipulation-lead-adjudication-v2",
  status: "PASS_24_CONTEXT_MUTANTS_LOCKED",
  rule: "A-only rejects contradictions and structural inconsistencies, not specificity that is merely absent from the source. B-context must uniquely refute the registered atom. One proposal per base; final selection preserves 12/12 profiles.",
  proposal_pool_sha256: sha256(poolBytes),
  p038_supplement_sha256: sha256(p038Bytes),
  design_amendment_006_sha256: sha256(amendmentBytes),
  accepted_proposal_ids: acceptedIds,
  rejected_or_unselected_proposal_ids: [...proposalById.keys()].filter(id => !acceptedIds.includes(id)),
  counts: {accepted: acceptedIds.length, profiles: contextProfileCounts, families: familyCounts},
  family_overrides: [...familyOverrides].map(([proposal_id, final_family]) => ({proposal_id, original_family: proposalById.get(proposal_id).proposal.family, final_family, basis: proposal_id === "P007" ? "The atom fixes the object's movement destination to discard rather than the registered alternative destinations." : "The atom reverses the registered action outcome from disposing of the Blood Master to releasing him."}))
};
const sample = {
  schema_version: "source-context-controlled-confirmation-final-sample-v2",
  status: "FROZEN_BEFORE_ROUTE_QUALIFICATION_OR_EXPERIMENTAL_INFERENCE",
  selected_base_frame_sha256: sha256(frameBytes),
  manipulation_lead_adjudication_sha256: sha256(jsonBytes(lead)),
  assignment_seed: roleSeed,
  counts: {total: publicItems.length, roles: roleCounts, role_profiles: roleProfiles, context_families: familyCounts},
  items: publicItems
};
const reference = {
  schema_version: "source-context-controlled-confirmation-sealed-reference-v2",
  status: "SEALED_DO_NOT_INCLUDE_IN_MODEL_REQUESTS",
  final_sample_sha256: sha256(jsonBytes(sample)),
  items: referenceItems
};
fs.writeFileSync(path.join(here, "MANIPULATION-LEAD-ADJUDICATION.json"), jsonBytes(lead), {flag: "wx"});
fs.writeFileSync(path.join(here, "FINAL-SAMPLE.json"), jsonBytes(sample), {flag: "wx"});
fs.writeFileSync(path.join(here, "SEALED-REFERENCE.json"), jsonBytes(reference), {flag: "wx"});
console.log(JSON.stringify({status: "PASS", manipulation_lead_adjudication_sha256: sha256(jsonBytes(lead)), final_sample_sha256: sha256(jsonBytes(sample)), sealed_reference_sha256: sha256(jsonBytes(reference)), counts: sample.counts}, null, 2));
