#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {
  buildTargetQueueFromValues,
  expectedTerminalRecords,
  jsonBytes,
  OUTPUT_NAMES,
  sha256Bytes
} from "./build-target-queue.mjs";
import {
  releaseContextFromValues,
  verifyContextCandidate,
  verifyFinalAdjudication,
  verifySurfaceCandidate
} from "./candidate-validation.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = file => JSON.parse(fs.readFileSync(file, "utf8"));
const fixture = read(path.join(here, "fixtures/SYNTHETIC-TARGET-JOIN.json"));
const expected = read(path.join(here, "fixtures/SYNTHETIC-EXPECTED.json"));
const realContract = read(path.join(here, "TARGET-JOIN-CONTRACT.json"));
const clone = value => structuredClone(value);

function prepare() {
  const contract = clone(realContract);
  contract.production_translation_commit = fixture.production_translation_commit;
  contract.source_only_presentation_sha256 = fixture.source_only_presentation_sha256;
  contract.expected = {
    items: expected.items,
    tasks: expected.tasks,
    categories: [{category: "Runtime", items: 3}, {category: "Narrative", items: 3}],
    terminal_inputs: expected.terminal_inputs,
    shards: 3,
    items_per_shard: expected.items_per_shard
  };
  const frame = clone(fixture.frame);
  const packets = clone(fixture.packets);
  const membership = {production_translation_commit: fixture.production_translation_commit, items: []};
  const snapshot = {source_repo_head: fixture.production_translation_commit, tasks: []};
  const terminalFiles = new Map();
  const packetByKey = new Map(packets.categories.flatMap(category => category.packets).map(packet => [`${packet.task_id}\0${packet.original_revision_key}`, packet]));
  for (const category of frame.categories) {
    for (const item of category.items) {
      item.source_sha256 = sha256Bytes(Buffer.from(item.source, "utf8"));
      packetByKey.get(`${item.task_id}\0${item.original_revision_key}`).source_sha256 = item.source_sha256;
      const target = fixture.targets[item.task_id];
      membership.items.push({
        task_id: item.task_id,
        original_revision_key: item.original_revision_key,
        canonical_revision_id: `canonical-${item.original_revision_key}`,
        canonical_revision_uid: `revision-uid-${item.original_revision_key}`,
        canonical_unit_id: `unit-${item.original_revision_key}`,
        canonical_tu_uid: `tu-${item.original_revision_key}`,
        component: item.component,
        section: item.section,
        source_tag: item.source_tag,
        profile: item.profile,
        source_sha256: item.source_sha256,
        target_sha256: sha256Bytes(Buffer.from(target, "utf8")),
        membership_sha256: sha256Bytes(`${item.task_id}\0${item.original_revision_key}\0membership`)
      });
      const logicalPath = `synthetic/${item.task_id}.json`;
      const envelope = {payload: {translation_snapshot: [{revision_key: item.original_revision_key, source: item.source, target}]}};
      const bytes = jsonBytes(envelope);
      terminalFiles.set(logicalPath, bytes);
      snapshot.tasks.push({
        task_id: item.task_id,
        dispatches: [{
          role: "REVIEWER",
          purpose: "translation_contextual_v1",
          cycle: 1,
          input_path: logicalPath,
          input_fingerprint: {sha256: sha256Bytes(bytes), size_bytes: bytes.length}
        }]
      });
    }
  }
  const unselected = fixture.unselected_terminal;
  const unselectedSourceSha = sha256Bytes(Buffer.from(unselected.source, "utf8"));
  const unselectedTargetSha = sha256Bytes(Buffer.from(unselected.target, "utf8"));
  membership.items.push({
    task_id: unselected.task_id, original_revision_key: unselected.original_revision_key,
    canonical_revision_id: "canonical-unselected", canonical_revision_uid: "revision-uid-unselected",
    canonical_unit_id: "unit-unselected", canonical_tu_uid: "tu-unselected",
    component: unselected.component, section: unselected.section, source_tag: unselected.source_tag,
    profile: unselected.profile, source_sha256: unselectedSourceSha, target_sha256: unselectedTargetSha,
    membership_sha256: sha256Bytes("synthetic-unselected-membership")
  });
  const unselectedPath = `synthetic/${unselected.task_id}.json`;
  const unselectedBytes = jsonBytes({payload: {translation_snapshot: [{revision_key: unselected.original_revision_key, source: unselected.source, target: unselected.target}]}});
  terminalFiles.set(unselectedPath, unselectedBytes);
  snapshot.tasks.push({task_id: unselected.task_id, dispatches: [{role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 1, input_path: unselectedPath, input_fingerprint: {sha256: sha256Bytes(unselectedBytes), size_bytes: unselectedBytes.length}}]});
  const records = expectedTerminalRecords(membership, snapshot);
  const canonical = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  contract.frozen_inputs.fingerprinted_terminal_input_manifest = {
    count: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
    manifest_sha256: sha256Bytes(canonical)
  };
  return {contract, membership, snapshot, frame, packets, terminalFiles};
}

function refreshTerminal(input, taskId) {
  const task = input.snapshot.tasks.find(candidate => candidate.task_id === taskId);
  const dispatch = task.dispatches[0];
  const bytes = input.terminalFiles.get(dispatch.input_path);
  dispatch.input_fingerprint = {sha256: sha256Bytes(bytes), size_bytes: bytes.length};
  const records = expectedTerminalRecords(input.membership, input.snapshot);
  const canonical = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  input.contract.frozen_inputs.fingerprinted_terminal_input_manifest = {
    count: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
    manifest_sha256: sha256Bytes(canonical)
  };
}

function mutateEnvelope(input, taskId, callback, updateFingerprint = true) {
  const task = input.snapshot.tasks.find(candidate => candidate.task_id === taskId);
  const logicalPath = task.dispatches[0].input_path;
  const envelope = JSON.parse(input.terminalFiles.get(logicalPath).toString("utf8"));
  callback(envelope.payload.translation_snapshot);
  input.terminalFiles.set(logicalPath, jsonBytes(envelope));
  if (updateFingerprint) refreshTerminal(input, taskId);
}

const baseline = prepare();
const first = buildTargetQueueFromValues(baseline);
const second = buildTargetQueueFromValues(prepare());
assert.deepEqual(Object.keys(first).sort(), [...OUTPUT_NAMES].sort());
for (const name of OUTPUT_NAMES) assert.deepEqual(jsonBytes(first[name]), jsonBytes(second[name]), `${name}: nondeterministic`);
assert.deepEqual(first["AUDIT-QUEUE.json"].items.map(item => item.audit_id), expected.audit_ids);
assert.equal(first["TARGET-JOIN-REPORT.json"].status, "PASS_TARGET_JOIN_GATES");
for (let shard = 1; shard <= 3; shard += 1) {
  assert.deepEqual(first[`SURFACE-QUEUE-${shard}.json`].items.map(item => item.audit_id), expected.surface_shards[String(shard)]);
}
assert.equal(Object.keys(first).some(name => name.startsWith("CONTEXT-QUEUE-")), false);

const surfaceQueues = [];
const contextQueues = [];
const surfaceCandidates = [];
const contextCandidates = [];
for (let shard = 1; shard <= 3; shard += 1) {
  const surfaceQueue = first[`SURFACE-QUEUE-${shard}.json`];
  const surfaceCandidate = {
    schema_version: "prospective-source-context-surface-candidate-v1", status: "SURFACE_CANDIDATE_COMPLETE", phase: "SURFACE", shard_id: shard,
    surface_queue_sha256: sha256Bytes(jsonBytes(surfaceQueue)),
    items: surfaceQueue.items.map(item => ({audit_id: item.audit_id, label: "CLEAN", surface_material_defect: false, reason: "synthetic surface clean"}))
  };
  const surfaceBytes = jsonBytes(surfaceCandidate);
  const surfaceSha = sha256Bytes(surfaceBytes);
  assert.deepEqual(verifySurfaceCandidate({surfaceQueue, candidateBytes: surfaceBytes, frozenSha256: surfaceSha, expectedCount: 2}), surfaceCandidate);
  const contextQueue = releaseContextFromValues({auditQueue: first["AUDIT-QUEUE.json"], surfaceQueue, candidateBytes: surfaceBytes, frozenSha256: surfaceSha, expectedCount: 2});
  assert.equal(contextQueue.surface_candidate_sha256, surfaceSha);
  const contextCandidate = {
    schema_version: "prospective-source-context-context-candidate-v1", status: "CONTEXT_CANDIDATE_COMPLETE", phase: "CONTEXT", shard_id: shard,
    context_queue_sha256: sha256Bytes(jsonBytes(contextQueue)), surface_candidate_sha256: surfaceSha,
    items: contextQueue.items.map(item => ({audit_id: item.audit_id, label: "CLEAN", surface_material_defect: false, context_material_contribution: false, packet_sufficient: true, reason: "synthetic context clean", evidence_sha256s: []}))
  };
  const contextBytes = jsonBytes(contextCandidate);
  assert.deepEqual(verifyContextCandidate({contextQueue, candidateBytes: contextBytes, expectedCount: 2}), contextCandidate);
  surfaceQueues.push(jsonBytes(surfaceQueue)); contextQueues.push(jsonBytes(contextQueue)); surfaceCandidates.push(surfaceBytes); contextCandidates.push(contextBytes);
}

const queue = first["AUDIT-QUEUE.json"];
const surfaceById = new Map(surfaceCandidates.flatMap(bytes => JSON.parse(bytes).items).map(item => [item.audit_id, item]));
const contextById = new Map(contextCandidates.flatMap(bytes => JSON.parse(bytes).items).map(item => [item.audit_id, item]));
const adjudication = {
  schema_version: "prospective-source-context-truth-adjudication-v1", status: "LEAD_ADJUDICATION_COMPLETE", queue_sha256: sha256Bytes(jsonBytes(queue)),
  surface_candidate_hashes: surfaceCandidates.map((bytes, index) => ({shard_id: index + 1, sha256: sha256Bytes(bytes), size_bytes: bytes.length})),
  context_candidate_hashes: contextCandidates.map((bytes, index) => ({shard_id: index + 1, sha256: sha256Bytes(bytes), size_bytes: bytes.length})),
  items: queue.items.map(item => ({
    audit_id: item.audit_id, task_id: item.task_id, original_revision_key: item.original_revision_key, category: item.category,
    surface_candidate: {label: surfaceById.get(item.audit_id).label, reason: surfaceById.get(item.audit_id).reason},
    context_candidate: {label: contextById.get(item.audit_id).label, reason: contextById.get(item.audit_id).reason},
    final_label: "CLEAN", material_axis: {surface_material_defect: false, context_material_contribution: false}, packet_sufficient: true, determinate: true,
    written_evidence: {lead_basis: "synthetic verified", material_evidence: "", candidate_disagreement: "", source_evidence_sha256s: [], limitations: ""}, lead_verified: true
  }))
};
assert.deepEqual(verifyFinalAdjudication({auditQueueBytes: jsonBytes(queue), surfaceQueueBytes: surfaceQueues, contextQueueBytes: contextQueues, surfaceCandidateBytes: surfaceCandidates, contextCandidateBytes: contextCandidates, adjudicationBytes: jsonBytes(adjudication), expectedItems: 6, expectedPerShard: 2}), adjudication);
const badFinal = clone(adjudication); badFinal.items[0].task_id = "wrong-task";
assert.throws(() => verifyFinalAdjudication({auditQueueBytes: jsonBytes(queue), surfaceQueueBytes: surfaceQueues, contextQueueBytes: contextQueues, surfaceCandidateBytes: surfaceCandidates, contextCandidateBytes: contextCandidates, adjudicationBytes: jsonBytes(badFinal), expectedItems: 6, expectedPerShard: 2}), /adjudication task_id mismatch/u);
assert.throws(() => releaseContextFromValues({auditQueue: queue, surfaceQueue: first["SURFACE-QUEUE-1.json"], candidateBytes: surfaceCandidates[0], frozenSha256: "0".repeat(64), expectedCount: 2}), /frozen hash mismatch/u);

const fingerprintDrift = prepare();
mutateEnvelope(fingerprintDrift, "task-r1", rows => { rows[0].target += "漂移"; }, false);
assert.throws(() => buildTargetQueueFromValues(fingerprintDrift), /terminal fingerprint drift/u);

const targetMismatch = prepare();
mutateEnvelope(targetMismatch, "task-r1", rows => { rows[0].target += "冲突"; });
assert.throws(() => buildTargetQueueFromValues(targetMismatch), /target hash mismatch/u);

const duplicateTerminal = prepare();
mutateEnvelope(duplicateTerminal, "task-r1", rows => { rows.push(clone(rows[0])); });
assert.throws(() => buildTargetQueueFromValues(duplicateTerminal), /duplicate identity/u);

const missingTerminal = prepare();
mutateEnvelope(missingTerminal, "task-r1", rows => { rows.splice(0, 1); });
assert.throws(() => buildTargetQueueFromValues(missingTerminal), /terminal target missing/u);

const duplicateMembership = prepare();
duplicateMembership.membership.items.push(clone(duplicateMembership.membership.items[0]));
assert.throws(() => buildTargetQueueFromValues(duplicateMembership), /canonical membership: duplicate identity/u);

const missingPacket = prepare();
missingPacket.packets.categories[0].packets.splice(0, 1);
assert.throws(() => buildTargetQueueFromValues(missingPacket), /packet count drift|source evidence missing/u);

const unselectedFingerprintDrift = prepare();
mutateEnvelope(unselectedFingerprintDrift, "task-unselected", rows => { rows[0].target += "漂移"; }, false);
assert.throws(() => buildTargetQueueFromValues(unselectedFingerprintDrift), /terminal fingerprint drift/u);

process.stdout.write("PASS synthetic target-link fixtures\n");
