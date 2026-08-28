import {jsonBytes, sha256Bytes} from "./build-target-queue.mjs";

const shaRe = /^[0-9a-f]{64}$/u;
const key = item => `${item.task_id}\0${item.original_revision_key}`;

function exactKeys(value, expected, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: expected object`);
  if (JSON.stringify(Object.keys(value).sort()) !== JSON.stringify([...expected].sort())) throw new Error(`${label}: exact field set mismatch`);
}

function parseBytes(bytes, label) {
  if (!Buffer.isBuffer(bytes)) throw new Error(`${label}: bytes missing`);
  try { return JSON.parse(bytes.toString("utf8")); } catch (error) { throw new Error(`${label}: invalid JSON: ${error.message}`); }
}

function uniqueOrderedIds(items, label) {
  const ids = items.map(item => item.audit_id);
  if (new Set(ids).size !== ids.length) throw new Error(`${label}: duplicate audit_id`);
  return ids;
}

export function verifySurfaceCandidate({surfaceQueue, candidateBytes, frozenSha256, expectedCount = 40}) {
  if (!shaRe.test(frozenSha256 ?? "") || sha256Bytes(candidateBytes) !== frozenSha256) throw new Error("surface candidate frozen hash mismatch");
  const candidate = parseBytes(candidateBytes, "surface candidate");
  exactKeys(candidate, ["schema_version", "status", "phase", "shard_id", "surface_queue_sha256", "items"], "surface candidate");
  if (candidate.schema_version !== "prospective-source-context-surface-candidate-v1" || candidate.status !== "SURFACE_CANDIDATE_COMPLETE" || candidate.phase !== "SURFACE") throw new Error("surface candidate contract");
  if (candidate.shard_id !== surfaceQueue.shard_id || candidate.surface_queue_sha256 !== sha256Bytes(jsonBytes(surfaceQueue))) throw new Error("surface candidate queue binding");
  if (!Array.isArray(candidate.items) || candidate.items.length !== expectedCount) throw new Error("surface candidate item count");
  const queueIds = uniqueOrderedIds(surfaceQueue.items, "surface queue");
  const candidateIds = uniqueOrderedIds(candidate.items, "surface candidate");
  if (JSON.stringify(candidateIds) !== JSON.stringify(queueIds)) throw new Error("surface candidate audit_ids/order mismatch");
  const axes = {SURFACE_VISIBLE_DEFECT: true, CLEAN: false, UNRESOLVED: null};
  candidate.items.forEach((item, index) => {
    exactKeys(item, ["audit_id", "label", "surface_material_defect", "reason"], `surface candidate item ${index}`);
    if (!Object.hasOwn(axes, item.label) || item.surface_material_defect !== axes[item.label] || typeof item.reason !== "string" || !item.reason) throw new Error(`surface candidate item ${index}: label/axis contract`);
  });
  return candidate;
}

export function releaseContextFromValues({auditQueue, surfaceQueue, candidateBytes, frozenSha256, expectedCount = 40}) {
  const candidate = verifySurfaceCandidate({surfaceQueue, candidateBytes, frozenSha256, expectedCount});
  const auditIndex = new Map(auditQueue.items.map(item => [item.audit_id, item]));
  if (auditIndex.size !== auditQueue.items.length) throw new Error("audit queue duplicate audit_id");
  const items = candidate.items.map(candidateItem => {
    const item = auditIndex.get(candidateItem.audit_id);
    if (!item) throw new Error(`${candidateItem.audit_id}: audit queue item missing`);
    return {audit_id: item.audit_id, source: item.source, target: item.target, source_evidence: item.source_evidence};
  });
  return {
    schema_version: "prospective-source-context-context-queue-v1",
    status: "FROZEN_CONTEXT_INPUT_AFTER_SURFACE_CANDIDATE",
    phase: "CONTEXT",
    shard_id: surfaceQueue.shard_id,
    shard_count: surfaceQueue.shard_count,
    target_bound_presentation_sha256: auditQueue.target_bound_presentation_sha256,
    surface_queue_sha256: sha256Bytes(jsonBytes(surfaceQueue)),
    surface_candidate_sha256: frozenSha256,
    surface_candidate_size_bytes: candidateBytes.length,
    item_count: items.length,
    items
  };
}

export function verifyContextCandidate({contextQueue, candidateBytes, expectedCount = 40}) {
  const candidate = parseBytes(candidateBytes, "context candidate");
  exactKeys(candidate, ["schema_version", "status", "phase", "shard_id", "context_queue_sha256", "surface_candidate_sha256", "items"], "context candidate");
  if (candidate.schema_version !== "prospective-source-context-context-candidate-v1" || candidate.status !== "CONTEXT_CANDIDATE_COMPLETE" || candidate.phase !== "CONTEXT") throw new Error("context candidate contract");
  if (candidate.shard_id !== contextQueue.shard_id || candidate.context_queue_sha256 !== sha256Bytes(jsonBytes(contextQueue)) || candidate.surface_candidate_sha256 !== contextQueue.surface_candidate_sha256) throw new Error("context candidate queue binding");
  if (!Array.isArray(candidate.items) || candidate.items.length !== expectedCount) throw new Error("context candidate item count");
  if (JSON.stringify(uniqueOrderedIds(candidate.items, "context candidate")) !== JSON.stringify(uniqueOrderedIds(contextQueue.items, "context queue"))) throw new Error("context candidate audit_ids/order mismatch");
  const axes = {
    CONTEXT_DEPENDENT_DEFECT: [false, true], SURFACE_VISIBLE_DEFECT: [true, false],
    MIXED_DEFECT: [true, true], CLEAN: [false, false]
  };
  candidate.items.forEach((item, index) => {
    exactKeys(item, ["audit_id", "label", "surface_material_defect", "context_material_contribution", "packet_sufficient", "reason", "evidence_sha256s"], `context candidate item ${index}`);
    const expected = axes[item.label];
    const unresolvedAxes = item.label === "UNRESOLVED"
      && (item.surface_material_defect === null || item.context_material_contribution === null);
    const determinateAxes = expected
      && item.surface_material_defect === expected[0]
      && item.context_material_contribution === expected[1];
    if ((!unresolvedAxes && !determinateAxes) || typeof item.packet_sufficient !== "boolean" || typeof item.reason !== "string" || !item.reason || !Array.isArray(item.evidence_sha256s) || item.evidence_sha256s.some(hash => !shaRe.test(hash))) throw new Error(`context candidate item ${index}: label/axis contract`);
    if (!item.packet_sufficient && item.label !== "UNRESOLVED") throw new Error(`context candidate item ${index}: insufficient packet must be UNRESOLVED`);
    if (["CONTEXT_DEPENDENT_DEFECT", "MIXED_DEFECT"].includes(item.label) && (!item.packet_sufficient || item.evidence_sha256s.length === 0)) throw new Error(`context candidate item ${index}: context evidence required`);
    const allowedEvidence = new Set((contextQueue.items[index]?.source_evidence?.occurrences ?? []).map(occurrence => occurrence.visible_context_sha256));
    if (item.evidence_sha256s.some(hash => !allowedEvidence.has(hash))) throw new Error(`context candidate item ${index}: evidence hash is not in the frozen packet`);
  });
  return candidate;
}

export function verifyFinalAdjudication({auditQueueBytes, surfaceQueueBytes, contextQueueBytes, surfaceCandidateBytes, contextCandidateBytes, adjudicationBytes, expectedItems = 120, expectedPerShard = 40}) {
  const auditQueue = parseBytes(auditQueueBytes, "audit queue");
  const adjudication = parseBytes(adjudicationBytes, "adjudication");
  if (!Array.isArray(auditQueue.items) || auditQueue.items.length !== expectedItems) throw new Error("audit queue item count");
  const queueIds = uniqueOrderedIds(auditQueue.items, "audit queue");
  const surfaceById = new Map();
  const contextById = new Map();
  const surfaceBindings = [];
  const contextBindings = [];
  const seenShards = new Set();
  for (let index = 0; index < 3; index += 1) {
    const surfaceQueue = parseBytes(surfaceQueueBytes[index], `surface queue ${index + 1}`);
    const contextQueue = parseBytes(contextQueueBytes[index], `context queue ${index + 1}`);
    if (seenShards.has(surfaceQueue.shard_id) || surfaceQueue.shard_id !== contextQueue.shard_id) throw new Error("candidate shard duplicate/mismatch");
    seenShards.add(surfaceQueue.shard_id);
    const surfaceHash = sha256Bytes(surfaceCandidateBytes[index]);
    const surface = verifySurfaceCandidate({surfaceQueue, candidateBytes: surfaceCandidateBytes[index], frozenSha256: surfaceHash, expectedCount: expectedPerShard});
    const context = verifyContextCandidate({contextQueue, candidateBytes: contextCandidateBytes[index], expectedCount: expectedPerShard});
    if (contextQueue.surface_candidate_sha256 !== surfaceHash) throw new Error("context queue surface candidate binding");
    surfaceBindings.push({shard_id: surface.shard_id, sha256: surfaceHash, size_bytes: surfaceCandidateBytes[index].length});
    contextBindings.push({shard_id: context.shard_id, sha256: sha256Bytes(contextCandidateBytes[index]), size_bytes: contextCandidateBytes[index].length});
    for (const item of surface.items) { if (surfaceById.has(item.audit_id)) throw new Error("surface candidate audit_id repeated across shards"); surfaceById.set(item.audit_id, item); }
    for (const item of context.items) { if (contextById.has(item.audit_id)) throw new Error("context candidate audit_id repeated across shards"); contextById.set(item.audit_id, item); }
  }
  if (JSON.stringify([...seenShards].sort()) !== JSON.stringify([1, 2, 3]) || surfaceById.size !== expectedItems || contextById.size !== expectedItems || queueIds.some(id => !surfaceById.has(id) || !contextById.has(id))) throw new Error("candidate shards not globally complete");
  exactKeys(adjudication, ["schema_version", "status", "queue_sha256", "surface_candidate_hashes", "context_candidate_hashes", "items"], "adjudication");
  if (adjudication.queue_sha256 !== sha256Bytes(auditQueueBytes)) throw new Error("adjudication queue hash mismatch");
  surfaceBindings.sort((a, b) => a.shard_id - b.shard_id); contextBindings.sort((a, b) => a.shard_id - b.shard_id);
  if (JSON.stringify(adjudication.surface_candidate_hashes) !== JSON.stringify(surfaceBindings) || JSON.stringify(adjudication.context_candidate_hashes) !== JSON.stringify(contextBindings)) throw new Error("adjudication candidate hashes mismatch");
  if (!Array.isArray(adjudication.items) || adjudication.items.length !== expectedItems || JSON.stringify(adjudication.items.map(item => item.audit_id)) !== JSON.stringify(queueIds)) throw new Error("adjudication order/coverage mismatch");
  adjudication.items.forEach((item, index) => {
    exactKeys(item, ["audit_id", "task_id", "original_revision_key", "category", "surface_candidate", "context_candidate", "final_label", "material_axis", "packet_sufficient", "determinate", "written_evidence", "lead_verified"], `adjudication item ${index}`);
    exactKeys(item.surface_candidate, ["label", "reason"], `adjudication item ${index}.surface_candidate`);
    exactKeys(item.context_candidate, ["label", "reason"], `adjudication item ${index}.context_candidate`);
    exactKeys(item.material_axis, ["surface_material_defect", "context_material_contribution"], `adjudication item ${index}.material_axis`);
    exactKeys(item.written_evidence, ["lead_basis", "material_evidence", "candidate_disagreement", "source_evidence_sha256s", "limitations"], `adjudication item ${index}.written_evidence`);
    const queueItem = auditQueue.items[index];
    for (const field of ["task_id", "original_revision_key", "category"]) if (item[field] !== queueItem[field]) throw new Error(`${item.audit_id}: adjudication ${field} mismatch`);
    const surface = surfaceById.get(item.audit_id); const context = contextById.get(item.audit_id);
    if (item.surface_candidate.label !== surface.label || item.surface_candidate.reason !== surface.reason || item.context_candidate.label !== context.label || item.context_candidate.reason !== context.reason) throw new Error(`${item.audit_id}: candidate decision mismatch`);
    if (context.surface_material_defect !== surface.surface_material_defect) throw new Error(`${item.audit_id}: context candidate changed the frozen surface axis`);
  });
  return adjudication;
}
