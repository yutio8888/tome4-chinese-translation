#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256, validateAuditCandidate} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const registryBytes = fs.readFileSync(path.join(here, "TARGET-BINDING-REGISTRY.json"));
const localBytes = fs.readFileSync(path.join(here, "LOCAL-AUDIT-SOURCE-BINDINGS.json"));
const packetBytes = fs.readFileSync(path.join(here, "SOURCE-EVIDENCE-PACKETS.json"));
const registry = JSON.parse(registryBytes);
const local = JSON.parse(localBytes);
const packets = JSON.parse(packetBytes);
const localByScreen = new Map([...local.primary, ...local.ordered_reserves].map(item => [item.screen_id, item]));
const packetByScreen = new Map(packets.items.map(item => [item.screen_id, item]));

const pairs = [];
for (let shard = 1; shard <= 3; shard += 1) {
  pairs.push({
    shard,
    surface: validateAuditCandidate(path.join(here, `SURFACE-CANDIDATE-${shard}.json`), path.join(here, `CLEAN-AUDIT-SURFACE-SHARD-${shard}.json`), "SURFACE", shard),
    context: validateAuditCandidate(path.join(here, `CONTEXT-CANDIDATE-${shard}.json`), path.join(here, `CLEAN-AUDIT-CONTEXT-SHARD-${shard}.json`), "CONTEXT", shard)
  });
}
for (let shard = 4; shard <= 6; shard += 1) {
  pairs.push({
    shard,
    surface: validateAuditCandidate(path.join(here, `RESERVE-SURFACE-CANDIDATE-${shard}.json`), path.join(here, `CLEAN-AUDIT-RESERVE-SURFACE-SHARD-${shard}.json`), "SURFACE", shard),
    context: validateAuditCandidate(path.join(here, `RESERVE-CONTEXT-CANDIDATE-${shard}.json`), path.join(here, `CLEAN-AUDIT-RESERVE-CONTEXT-SHARD-${shard}.json`), "CONTEXT", shard)
  });
}

const surfaceById = new Map(pairs.flatMap(pair => pair.surface.candidate.items).map(item => [item.audit_id, item]));
const contextById = new Map(pairs.flatMap(pair => pair.context.candidate.items).map(item => [item.audit_id, item]));
const audited = registry.records.flatMap(record => {
  const auditId = record.audit_id ?? (record.profile === "narrative" && record.reserve_ordinal >= 61 ? `R${String(record.reserve_ordinal).padStart(3, "0")}` : null);
  if (!auditId || !surfaceById.has(auditId) || !contextById.has(auditId)) return [];
  const surface = surfaceById.get(auditId);
  const context = contextById.get(auditId);
  const localRecord = localByScreen.get(record.screen_id);
  const packet = packetByScreen.get(record.screen_id);
  if (!localRecord || !packet || packet.source_sha256 !== record.source_sha256 || localRecord.context_sha256 !== packet.occurrence.visible_context_sha256) throw new Error(`${auditId}: binding mismatch`);
  const clean = surface.verdict === "CLEAN" && context.verdict === "CLEAN";
  return [{
    audit_id: auditId,
    screen_id: record.screen_id,
    source_set: record.disposition === "PRIMARY_CLEAN_AUDIT" ? "PRIMARY" : "ORDERED_NARRATIVE_RESERVE",
    reserve_ordinal: record.reserve_ordinal,
    profile: record.profile,
    relative_path: localRecord.relative_path,
    revision_id: record.canonical_identity.revision_id,
    source_sha256: record.source_sha256,
    target_sha256: record.target_sha256,
    context_sha256: localRecord.context_sha256,
    surface_verdict: surface.verdict,
    context_verdict: context.verdict,
    lead_adjudication: clean ? "CLEAN_NO_MATERIAL_DEFECT" : "EXCLUDED_NOT_CLEAN_IN_BOTH_PASSES",
    lead_basis: clean
      ? "Independent surface and fixed-source-context passes both returned CLEAN; binding and schema validators passed."
      : "Conservative clean-lock rule excludes any item with an OBJECTIVE_DEFECT or UNRESOLVED verdict in either pass; no lead false-positive override is permitted."
  }];
});
if (audited.length !== 180) throw new Error(`audited item count ${audited.length} != 180`);
const eligible = audited.filter(item => item.lead_adjudication === "CLEAN_NO_MATERIAL_DEFECT");
const counts = audited.reduce((acc, item) => {
  acc.audited[item.profile] += 1;
  if (item.lead_adjudication === "CLEAN_NO_MATERIAL_DEFECT") acc.eligible[item.profile] += 1;
  else acc.excluded[item.profile] += 1;
  return acc;
}, {audited: {dialogue: 0, narrative: 0}, eligible: {dialogue: 0, narrative: 0}, excluded: {dialogue: 0, narrative: 0}});

const adjudication = {
  schema_version: "source-context-controlled-confirmation-clean-adjudication-v2",
  status: "CLEAN_LOCK_COMPLETE_NO_MUTATION_ASSIGNMENT",
  policy: "Accept only CLEAN/CLEAN consensus. Exclude every disagreement, objective defect and unresolved item without lead override.",
  amendment_sha256: sha256(fs.readFileSync(path.join(here, "DESIGN-AMENDMENT-005.json"))),
  inputs: {
    target_binding_registry_sha256: sha256(registryBytes),
    local_audit_bindings_sha256: sha256(localBytes),
    source_evidence_packets_sha256: sha256(packetBytes),
    candidates: pairs.flatMap(pair => [
      {shard: pair.shard, pass: "SURFACE", sha256: pair.surface.candidate_sha256},
      {shard: pair.shard, pass: "CONTEXT", sha256: pair.context.candidate_sha256}
    ])
  },
  counts,
  items: audited
};
const pool = {
  schema_version: "source-context-controlled-confirmation-clean-eligible-pool-v2",
  status: "FROZEN_CLEAN_ELIGIBLE_POOL",
  clean_adjudication_sha256: sha256(jsonBytes(adjudication)),
  count: eligible.length,
  profile_counts: counts.eligible,
  items: eligible
};
fs.writeFileSync(path.join(here, "CLEAN-ADJUDICATION.json"), jsonBytes(adjudication), {flag: "wx"});
fs.writeFileSync(path.join(here, "CLEAN-ELIGIBLE-POOL.json"), jsonBytes(pool), {flag: "wx"});
console.log(JSON.stringify({status: "PASS", counts, clean_adjudication_sha256: sha256(jsonBytes(adjudication)), clean_eligible_pool_sha256: sha256(jsonBytes(pool))}, null, 2));
