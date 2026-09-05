#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, sha256} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const poolBytes = fs.readFileSync(path.join(here, "CLEAN-ELIGIBLE-POOL.json"));
const registryBytes = fs.readFileSync(path.join(here, "TARGET-BINDING-REGISTRY.json"));
const packetBytes = fs.readFileSync(path.join(here, "SOURCE-EVIDENCE-PACKETS.json"));
const amendmentBytes = fs.readFileSync(path.join(here, "DESIGN-AMENDMENT-005.json"));
const pool = JSON.parse(poolBytes);
const registry = JSON.parse(registryBytes);
const packets = JSON.parse(packetBytes);
const recordByAudit = new Map(registry.records.flatMap(record => {
  const auditId = record.audit_id ?? (record.profile === "narrative" && record.reserve_ordinal >= 61 ? `R${String(record.reserve_ordinal).padStart(3, "0")}` : null);
  return auditId ? [[auditId, record]] : [];
}));
const packetByScreen = new Map(packets.items.map(item => [item.screen_id, item]));
const seed = "source-context-controlled-confirmation-v2/final-assignment/2026-08-28/selection";
const rank = revisionId => crypto.createHash("sha256").update(`${seed}\0${revisionId}`).digest("hex");
const familyFingerprint = source => source.normalize("NFKC").toLowerCase()
  .replace(/\b(?:one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million)\b|\d+/gu, "#")
  .replace(/[^\p{L}#]+/gu, " ")
  .trim();

const selected = [];
const fileCounts = new Map();
const fingerprints = new Set();
for (const profile of ["dialogue", "narrative"]) {
  const ranked = pool.items.filter(item => item.profile === profile).sort((a, b) => rank(a.revision_id).localeCompare(rank(b.revision_id)));
  for (const item of ranked) {
    const record = recordByAudit.get(item.audit_id);
    const packet = packetByScreen.get(item.screen_id);
    if (!record || !packet || packet.source_sha256 !== item.source_sha256 || packet.occurrence.visible_context_sha256 !== item.context_sha256) throw new Error(`${item.audit_id}: selection binding mismatch`);
    const fingerprint = familyFingerprint(record.source);
    if (fileCounts.get(item.relative_path) >= 3 || fingerprints.has(fingerprint)) continue;
    selected.push({
      base_ordinal: 0,
      audit_id: item.audit_id,
      screen_id: item.screen_id,
      source_set: item.source_set,
      reserve_ordinal: item.reserve_ordinal,
      profile: item.profile,
      relative_path: item.relative_path,
      revision_id: item.revision_id,
      source: record.source,
      target: record.target,
      source_context: packet.occurrence.visible_context,
      source_sha256: item.source_sha256,
      target_sha256: item.target_sha256,
      context_sha256: item.context_sha256,
      source_family_fingerprint_sha256: sha256(Buffer.from(fingerprint, "utf8")),
      selection_rank: rank(item.revision_id),
      role: null,
      mutation_id: null
    });
    fileCounts.set(item.relative_path, (fileCounts.get(item.relative_path) ?? 0) + 1);
    fingerprints.add(fingerprint);
    if (selected.filter(value => value.profile === profile).length === 30) break;
  }
  if (selected.filter(value => value.profile === profile).length !== 30) throw new Error(`${profile}: could not select 30 clean bases`);
}
selected.forEach((item, index) => { item.base_ordinal = index + 1; });
const profileCounts = selected.reduce((acc, item) => (acc[item.profile] += 1, acc), {dialogue: 0, narrative: 0});
const actualFileMax = Math.max(...fileCounts.values());
if (new Set(selected.map(item => item.revision_id)).size !== 60 || new Set(selected.map(item => item.source_sha256)).size !== 60 || new Set(selected.map(item => item.context_sha256)).size !== 60 || fingerprints.size !== 60) throw new Error("selected-base uniqueness failure");
if (actualFileMax > 3) throw new Error("selected-base file cap failure");

const frame = {
  schema_version: "source-context-controlled-confirmation-selected-base-frame-v2",
  status: "FROZEN_CLEAN_BASE_FRAME_ROLE_ASSIGNMENT_PENDING",
  selection_seed: seed,
  inputs: {
    clean_eligible_pool_sha256: sha256(poolBytes),
    target_binding_registry_sha256: sha256(registryBytes),
    source_evidence_packets_sha256: sha256(packetBytes),
    design_amendment_005_sha256: sha256(amendmentBytes)
  },
  rules: {
    profile_count_each: 30,
    max_items_per_source_file: 3,
    exact_source_family_fingerprint_unique: true,
    source_family_fingerprint: "NFKC lowercase; replace ASCII number tokens and English number words with #; remove non-letter/non-# runs; exact equality forbidden."
  },
  counts: {total: selected.length, profiles: profileCounts, source_files: fileCounts.size, actual_max_items_per_source_file: actualFileMax},
  items: selected
};
fs.writeFileSync(path.join(here, "SELECTED-BASE-FRAME.json"), jsonBytes(frame), {flag: "wx"});
console.log(JSON.stringify({status: "PASS", selected_base_frame_sha256: sha256(jsonBytes(frame)), counts: frame.counts}, null, 2));
