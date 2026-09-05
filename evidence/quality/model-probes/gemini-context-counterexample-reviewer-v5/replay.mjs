#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {validateRound2CompletedReleaseEvidence} from './round-0002-release.mjs';
import {fileURLToPath} from 'node:url';
import {validateRound2SurfaceInput} from './round-0002-surface-input.mjs';
import {validateRound2SurfaceArtifacts} from './round-0002-surface-results.mjs';
import {validateRound2ContextInput} from './round-0002-context-input.mjs';
import {validateRound2ContextArtifacts} from './round-0002-context-results.mjs';
import {initialize, readInitialPackage, readRoundBundles, applyRound, applyReviewedProvenanceRound, outputDocuments, jsonBytes, sha256, activeFrameDocument, activeFrameSha256, rowIdentity, loadValidatedContextAuditorResponse, loadValidatedSurfaceAuditorResponse, validatePendingSurfaceArtifacts, validatePendingContextResultsDirectory} from './round-lineage.mjs';
import {CONTEXT_SOURCE_ANCHORS_AUTHORIZATION_SHA256, CONTEXT_SOURCE_ANCHORS_SHA256, validateFrozenContextInputBytes} from './context-queue-view.mjs';
import {validateRound2PendingRelease} from './round-0002-release.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const REVIEWED_SIDECAR_CANDIDATE = '05810069a709392485091907a85cd2fc13f6fddfdfee9f4b3177f1cd69cdbe6a';
const REVIEWED_SIDECAR_MANIFEST = 'a64d0708509ad11a97fecb07c6ddd796094abe162b65ba121b3cc99992a8104f';
const INTERMEDIATE_REVIEWED_CANDIDATE = 'b9df80bc7e13d90bcb6c4d807434006bcc99c3075ef6ef347b4b66490d465ea5';
const INTERMEDIATE_REVIEWED_MANIFEST = '37fb7f014b46ebba293d72aeb64cdbcafb6c7c5c4b7699897daba158ee73480a';
const INTERMEDIATE_MANIFEST_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/SURFACE-MATERIALIZATION-CANDIDATE-B9DF-MANIFEST.json';
const INTERMEDIATE_NORMAL = {path: '.ai/task/research-gemini-context-counterexample-reviewer-v5/SURFACE-INTERMEDIATE-NORMAL-REVIEW-001.json', agent_id: '82dfc9a2-11c3-47ae-bb71-4e7cda0e326b', role: 'NORMAL_REVIEWER'};
const INTERMEDIATE_SENIOR = {path: '.ai/task/research-gemini-context-counterexample-reviewer-v5/SURFACE-INTERMEDIATE-SENIOR-REVIEW-001.json', agent_id: 'e0bdbce9-3335-42c8-9c34-f09b49a8ab4a', role: 'SENIOR_REVIEWER'};
const INTERMEDIATE_GATE_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/SURFACE-INTERMEDIATE-REVIEW-GATE-001.json';
const CONTEXT_INPUT_REVIEWED_CANDIDATE = 'f4cba464e366809479257be606e3acd3e058b488bcfc80fc8d1b2e16c5f3b408';
const CONTEXT_INPUT_REVIEWED_MANIFEST = '8dd7579a704eeaa3c07e4f587aa47b32279274eacad22e1491280d61e3663137';
const CONTEXT_INPUT_MANIFEST_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-INPUT-CANDIDATE-MANIFEST.json';
const CONTEXT_INPUT_NORMAL = {path: '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-QUEUE-NORMAL-REVIEW-001.json', review_id: 'V5-CONTEXT-INPUT-NORMAL-REVIEW-001', agent_id: '94403f94-bcdd-45cd-926b-90a7233eb741', role: 'NORMAL_REVIEWER'};
const CONTEXT_INPUT_SENIOR = {path: '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-QUEUE-SENIOR-REVIEW-001.json', review_id: 'V5-CONTEXT-INPUT-SENIOR-REVIEW-001', agent_id: '9480ec23-de89-4ed3-918a-dfa3958e55d6', role: 'SENIOR_REVIEWER'};
const CONTEXT_INPUT_GATE_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-QUEUE-REVIEW-GATE-001.json';
const CONTEXT_RESULTS_REVIEWED_CANDIDATE = '0185b8fc41e58e5a4ac1428a9d9b6ee946918c475f10162acf21bf53a50d1256';
const CONTEXT_RESULTS_REVIEWED_MANIFEST = 'b91626a3e1a2d6fac820a26615341598f5746d61fbf4c67343e73990ea28c0fc';
const CONTEXT_RESULTS_MANIFEST_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-RESULTS-IMPLEMENTATION-CANDIDATE-MANIFEST.json';
const CONTEXT_RESULTS_NORMAL = {path: '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-RESULTS-NORMAL-REVIEW-001.json', review_id: 'V5-CONTEXT-RESULTS-NORMAL-REVIEW-001', agent_id: '94403f94-bcdd-45cd-926b-90a7233eb741', role: 'NORMAL_REVIEWER'};
const CONTEXT_RESULTS_SENIOR = {path: '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-RESULTS-SENIOR-REVIEW-001.json', review_id: 'V5-CONTEXT-RESULTS-SENIOR-REVIEW-001', agent_id: '9480ec23-de89-4ed3-918a-dfa3958e55d6', role: 'SENIOR_REVIEWER'};
const CONTEXT_RESULTS_GATE_PATH = '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-RESULTS-REVIEW-GATE-001.json';
const CONTEXT_RESULTS_GATE_SHA256 = 'd187a58410841f4ba01a9314e4a7e70568d2a0b3b0e2f583642df45cf995bb05';
const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());

function readBoundReviewRecord(repo, binding, label) {
  if (!exactKeys(binding, ['path', 'sha256', 'agent_id', 'status']) || binding.status !== 'PASS') throw Error(`${label}_BINDING_SCHEMA`);
  const file = path.join(repo, binding.path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`);
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== binding.sha256) throw Error(`${label}_HASH`);
  let record; try { record = JSON.parse(bytes); } catch { throw Error(`${label}_JSON`); }
  return record;
}

export function validateSidecarReviewGate(repo, pending) {
  if (pending.sidecar_review_gate_record_path !== '.ai/task/research-gemini-context-counterexample-reviewer-v5/SIDECAR-REVIEW-GATE-001.json') throw Error('SIDECAR_REVIEW_GATE_PATH');
  const gatePath = path.join(repo, pending.sidecar_review_gate_record_path), gateStat = fs.lstatSync(gatePath);
  if (gateStat.isSymbolicLink() || !gateStat.isFile()) throw Error('SIDECAR_REVIEW_GATE_FILE_TYPE');
  const gateBytes = fs.readFileSync(gatePath); if (sha256(gateBytes) !== pending.sidecar_review_gate_record_sha256) throw Error('SIDECAR_REVIEW_GATE_HASH');
  let gate; try { gate = JSON.parse(gateBytes); } catch { throw Error('SIDECAR_REVIEW_GATE_JSON'); }
  const gateKeys = ['schema_version', 'gate_id', 'status', 'candidate_ref', 'candidate_manifest_sha256', 'predecessor_review_record', 'normal_final_review', 'senior_final_review', 'authorized_input_boundary', 'permitted_next_action', 'forbidden_before_valid_auditor_output', 'surface_audit_executed', 'recorded_at'];
  const forbidden = ['SURFACE-RECORDS.json', 'SURFACE-AGGREGATE.json', 'RELEASE.json', 'CONTEXT-QUEUE.json', 'CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json', 'FURTHER_ROUNDS', 'QUALIFICATION', 'MUTATION', 'REFERENCE', 'FORMAL_GEMINI_INFERENCE'];
  if (!exactKeys(gate, gateKeys) || gate.schema_version !== 'gemini-context-v5-sidecar-review-gate-v1' || gate.status !== 'SATISFIED_FINAL_DUAL_PASS' || pending.sidecar_review_gate_status !== gate.status || gate.candidate_ref !== REVIEWED_SIDECAR_CANDIDATE || gate.candidate_manifest_sha256 !== REVIEWED_SIDECAR_MANIFEST || gate.permitted_next_action !== 'SURFACE_AUDITOR_CONSUME_IMMUTABLE_QUEUE_AND_VIEW_ONLY' || JSON.stringify(gate.forbidden_before_valid_auditor_output) !== JSON.stringify(forbidden) || gate.surface_audit_executed !== false) throw Error('SIDECAR_REVIEW_GATE_SCHEMA');
  if (!exactKeys(gate.authorized_input_boundary, ['round_id', 'stage', 'surface_queue_sha256', 'surface_queue_view_sha256', 'authorization_record_sha256']) || gate.authorized_input_boundary.round_id !== pending.round_id || gate.authorized_input_boundary.stage !== 'SURFACE' || gate.authorized_input_boundary.surface_queue_sha256 !== pending.surface_queue_sha256 || gate.authorized_input_boundary.surface_queue_view_sha256 !== pending.surface_queue_view_sha256 || gate.authorized_input_boundary.authorization_record_sha256 !== pending.authorization_record_sha256) throw Error('SIDECAR_REVIEW_GATE_INPUT_BOUNDARY');
  if (!exactKeys(gate.predecessor_review_record, ['path', 'sha256', 'status']) || gate.predecessor_review_record.path !== '.ai/task/research-gemini-context-counterexample-reviewer-v5/SIDECAR-REVIEW-001.json' || gate.predecessor_review_record.sha256 !== '26b4ba1d65113a2f7fb5544cfa1f7bb53bc2f032c5064749f6d1fa1264d59eee' || gate.predecessor_review_record.status !== 'CHANGES_REQUIRED_REPAIR_CYCLE_1_PENDING_REREVIEW') throw Error('SIDECAR_REVIEW_GATE_PREDECESSOR');
  const predecessorBytes = fs.readFileSync(path.join(repo, gate.predecessor_review_record.path)), predecessor = JSON.parse(predecessorBytes);
  if (sha256(predecessorBytes) !== gate.predecessor_review_record.sha256 || predecessor.status !== gate.predecessor_review_record.status || predecessor.candidate_ref !== 'c0c582ec3ab8093335c716f6577669a224abd0325559452a389fe7e4240cb01a') throw Error('SIDECAR_REVIEW_GATE_PREDECESSOR_BINDING');
  const expected = [
    ['NORMAL_REVIEW', gate.normal_final_review, 'NORMAL_REVIEWER', '82dfc9a2-11c3-47ae-bb71-4e7cda0e326b'],
    ['SENIOR_REVIEW', gate.senior_final_review, 'SENIOR_REVIEWER', 'e0bdbce9-3335-42c8-9c34-f09b49a8ab4a']
  ];
  for (const [label, binding, role, agentId] of expected) {
    const review = readBoundReviewRecord(repo, binding, label), reviewKeys = ['schema_version', 'review_id', 'role', 'agent_id', 'status', 'candidate_ref', 'candidate_manifest_sha256', 'surface_queue_sha256', 'surface_queue_view_sha256', 'findings', 'recorded_at'];
    if (!exactKeys(review, reviewKeys) || review.schema_version !== 'gemini-context-v5-sidecar-final-review-v1' || review.role !== role || review.agent_id !== agentId || binding.agent_id !== agentId || review.status !== 'PASS' || binding.status !== review.status || review.candidate_ref !== REVIEWED_SIDECAR_CANDIDATE || review.candidate_manifest_sha256 !== REVIEWED_SIDECAR_MANIFEST || review.surface_queue_sha256 !== pending.surface_queue_sha256 || review.surface_queue_view_sha256 !== pending.surface_queue_view_sha256 || !Array.isArray(review.findings) || review.findings.length !== 0) throw Error(`${label}_CONTENT`);
  }
  return {satisfied: true, candidate_ref: gate.candidate_ref, gate_sha256: sha256(gateBytes)};
}

export function evaluateSidecarReviewGate(repo, pending) {
  try { return {decision: 'GO', ...validateSidecarReviewGate(repo, pending)}; }
  catch (error) { return {decision: 'NO_GO', satisfied: false, reason: error.code === 'ENOENT' ? 'SIDECAR_REVIEW_RECORD_MISSING' : error.message}; }
}

export function validateIntermediateCandidateBinding(repo, pending) {
  const binding = pending.implementation_candidate_binding, keys = ['candidate_ref', 'manifest_path', 'manifest_sha256', 'normal_reviewer_agent_id', 'senior_reviewer_agent_id', 'normal_review_path', 'senior_review_path', 'review_gate_path'];
  if (!exactKeys(binding, keys) || binding.candidate_ref !== INTERMEDIATE_REVIEWED_CANDIDATE || binding.manifest_path !== INTERMEDIATE_MANIFEST_PATH || binding.manifest_sha256 !== INTERMEDIATE_REVIEWED_MANIFEST || binding.normal_reviewer_agent_id !== INTERMEDIATE_NORMAL.agent_id || binding.senior_reviewer_agent_id !== INTERMEDIATE_SENIOR.agent_id || binding.normal_review_path !== INTERMEDIATE_NORMAL.path || binding.senior_review_path !== INTERMEDIATE_SENIOR.path || binding.review_gate_path !== INTERMEDIATE_GATE_PATH) throw Error('INTERMEDIATE_CANDIDATE_BINDING');
  const file = path.join(repo, binding.manifest_path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('INTERMEDIATE_CANDIDATE_MANIFEST_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== INTERMEDIATE_REVIEWED_MANIFEST) throw Error('INTERMEDIATE_CANDIDATE_MANIFEST_HASH');
  const manifest = JSON.parse(bytes);
  if (manifest.schema_version !== 5 || manifest.candidate_ref !== INTERMEDIATE_REVIEWED_CANDIDATE || !Array.isArray(manifest.files) || manifest.files.length !== 35 || manifest.exclusions?.includes('.ai/task/research-gemini-context-counterexample-reviewer-v5/STATE.json') !== true || manifest.exclusions?.includes('.ai/task/research-gemini-context-counterexample-reviewer-v5/SIDECAR-CANDIDATE-MANIFEST.json') !== true) throw Error('INTERMEDIATE_CANDIDATE_MANIFEST_SCHEMA');
  const files = manifest.files, sorted = [...files].sort((a, b) => Buffer.compare(Buffer.from(a.path), Buffer.from(b.path)));
  if (JSON.stringify(files) !== JSON.stringify(sorted) || new Set(files.map(item => item.path)).size !== files.length || files.some(item => !exactKeys(item, ['path', 'sha256']) || typeof item.path !== 'string' || item.path.startsWith('/') || item.path.includes('..') || !/^[0-9a-f]{64}$/u.test(item.sha256))) throw Error('INTERMEDIATE_CANDIDATE_MANIFEST_FILES');
  const candidate = sha256(Buffer.concat(files.map(item => Buffer.from(`${item.path}\0${item.sha256}\n`))));
  if (candidate !== INTERMEDIATE_REVIEWED_CANDIDATE) throw Error('INTERMEDIATE_CANDIDATE_MANIFEST_ROOT');
  return {candidate_ref: candidate, manifest_sha256: sha256(bytes)};
}

function readIntermediateReview(repo, binding, expected) {
  if (!exactKeys(binding, ['path', 'sha256', 'agent_id', 'status']) || binding.status !== 'PASS' || binding.path !== expected.path || binding.agent_id !== expected.agent_id || !/^[0-9a-f]{64}$/u.test(binding.sha256)) throw Error('INTERMEDIATE_REVIEW_BINDING_SCHEMA');
  const file = path.join(repo, binding.path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('INTERMEDIATE_REVIEW_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== binding.sha256) throw Error('INTERMEDIATE_REVIEW_HASH');
  const review = JSON.parse(bytes), keys = ['schema_version', 'review_id', 'role', 'agent_id', 'status', 'candidate_ref', 'candidate_manifest_sha256', 'surface_queue_sha256', 'surface_queue_view_sha256', 'expected_surface_records_sha256', 'expected_surface_aggregate_sha256', 'findings', 'recorded_at'];
  if (!bytes.equals(jsonBytes(review))) throw Error('INTERMEDIATE_REVIEW_NONCANONICAL_BYTES');
  if (!exactKeys(review, keys) || review.schema_version !== 'gemini-context-v5-surface-intermediate-final-review-v1' || review.role !== expected.role || review.agent_id !== expected.agent_id || review.status !== 'PASS' || review.candidate_ref !== INTERMEDIATE_REVIEWED_CANDIDATE || review.candidate_manifest_sha256 !== INTERMEDIATE_REVIEWED_MANIFEST || !Array.isArray(review.findings) || review.findings.length !== 0) throw Error('INTERMEDIATE_REVIEW_CONTENT');
  return review;
}

export function validateIntermediateReviewGate(repo, pending) {
  validateIntermediateCandidateBinding(repo, pending);
  const binding = pending.surface_intermediate_state.implementation_review_gate;
  if (!exactKeys(binding, ['status', 'record_path', 'record_sha256']) || binding.status !== 'SATISFIED_FINAL_DUAL_PASS' || binding.record_path !== INTERMEDIATE_GATE_PATH || !/^[0-9a-f]{64}$/u.test(binding.record_sha256)) throw Error('INTERMEDIATE_REVIEW_GATE_BINDING');
  const file = path.join(repo, binding.record_path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('INTERMEDIATE_REVIEW_GATE_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== binding.record_sha256) throw Error('INTERMEDIATE_REVIEW_GATE_HASH');
  const gate = JSON.parse(bytes), keys = ['schema_version', 'gate_id', 'status', 'candidate_ref', 'candidate_manifest_sha256', 'normal_final_review', 'senior_final_review', 'surface_bindings', 'permitted_state', 'recorded_at'];
  if (!bytes.equals(jsonBytes(gate))) throw Error('INTERMEDIATE_REVIEW_GATE_NONCANONICAL_BYTES');
  if (!exactKeys(gate, keys) || gate.schema_version !== 'gemini-context-v5-surface-intermediate-review-gate-v1' || gate.status !== 'SATISFIED_FINAL_DUAL_PASS' || gate.permitted_state !== 'SURFACE_STAGE_COMPLETED_PENDING_CONTEXT_AUDIT' || gate.candidate_ref !== INTERMEDIATE_REVIEWED_CANDIDATE || gate.candidate_manifest_sha256 !== INTERMEDIATE_REVIEWED_MANIFEST) throw Error('INTERMEDIATE_REVIEW_GATE_SCHEMA');
  const expectedBindings = {surface_queue_sha256: pending.surface_queue_sha256, surface_queue_view_sha256: pending.surface_queue_view_sha256, auditor_response_artifact_path: pending.validated_surface_response.artifact_path, auditor_response_artifact_sha256: pending.validated_surface_response.artifact_sha256, expected_surface_records_sha256: pending.validated_surface_response.expected_surface_records_sha256, expected_surface_aggregate_sha256: pending.validated_surface_response.expected_surface_aggregate_sha256};
  if (!exactKeys(gate.surface_bindings, Object.keys(expectedBindings)) || JSON.stringify(gate.surface_bindings) !== JSON.stringify(expectedBindings)) throw Error('INTERMEDIATE_REVIEW_GATE_SURFACE_BINDING');
  const normal = readIntermediateReview(repo, gate.normal_final_review, INTERMEDIATE_NORMAL), senior = readIntermediateReview(repo, gate.senior_final_review, INTERMEDIATE_SENIOR);
  for (const review of [normal, senior]) if (review.candidate_ref !== gate.candidate_ref || review.candidate_manifest_sha256 !== gate.candidate_manifest_sha256 || review.surface_queue_sha256 !== pending.surface_queue_sha256 || review.surface_queue_view_sha256 !== pending.surface_queue_view_sha256 || review.expected_surface_records_sha256 !== pending.validated_surface_response.expected_surface_records_sha256 || review.expected_surface_aggregate_sha256 !== pending.validated_surface_response.expected_surface_aggregate_sha256) throw Error('INTERMEDIATE_REVIEW_CANDIDATE_BINDING');
  return {satisfied: true, candidate_ref: gate.candidate_ref, gate_sha256: sha256(bytes)};
}

function validateContextInputCandidateManifest(repo) {
  const file = path.join(repo, CONTEXT_INPUT_MANIFEST_PATH), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_INPUT_CANDIDATE_MANIFEST_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== CONTEXT_INPUT_REVIEWED_MANIFEST) throw Error('CONTEXT_INPUT_CANDIDATE_MANIFEST_HASH');
  const manifest = JSON.parse(bytes);
  if (!bytes.equals(jsonBytes(manifest)) || manifest.schema_version !== 1 || manifest.candidate_ref !== CONTEXT_INPUT_REVIEWED_CANDIDATE || !Array.isArray(manifest.files) || manifest.files.length !== 28 || manifest.exclusions?.includes('.ai/task/research-gemini-context-counterexample-reviewer-v5/STATE.json') !== true || manifest.exclusions?.includes(CONTEXT_INPUT_MANIFEST_PATH) !== true) throw Error('CONTEXT_INPUT_CANDIDATE_MANIFEST_SCHEMA');
  const files = manifest.files, sorted = [...files].sort((a, b) => Buffer.compare(Buffer.from(a.path), Buffer.from(b.path)));
  if (JSON.stringify(files) !== JSON.stringify(sorted) || new Set(files.map(item => item.path)).size !== files.length || files.some(item => !exactKeys(item, ['path', 'sha256']) || typeof item.path !== 'string' || item.path.startsWith('/') || item.path.includes('..') || !/^[0-9a-f]{64}$/u.test(item.sha256))) throw Error('CONTEXT_INPUT_CANDIDATE_MANIFEST_FILES');
  if (sha256(Buffer.concat(files.map(item => Buffer.from(`${item.path}\0${item.sha256}\n`)))) !== CONTEXT_INPUT_REVIEWED_CANDIDATE) throw Error('CONTEXT_INPUT_CANDIDATE_MANIFEST_ROOT');
  return manifest;
}

function readContextInputReview(repo, binding, expected, pending) {
  if (!exactKeys(binding, ['path', 'sha256', 'agent_id', 'role', 'status']) || binding.path !== expected.path || binding.agent_id !== expected.agent_id || binding.role !== expected.role || binding.status !== 'PASS' || !/^[0-9a-f]{64}$/u.test(binding.sha256)) throw Error('CONTEXT_INPUT_REVIEW_BINDING_SCHEMA');
  const file = path.join(repo, binding.path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_INPUT_REVIEW_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== binding.sha256) throw Error('CONTEXT_INPUT_REVIEW_HASH');
  const review = JSON.parse(bytes), keys = ['schema_version', 'review_id', 'role', 'agent_id', 'status', 'candidate_ref', 'candidate_manifest_sha256', 'round_id', 'context_queue_sha256', 'context_source_anchors_sha256', 'context_queue_view_sha256', 'context_source_anchors_authorization_sha256', 'findings', 'recorded_at'];
  if (!bytes.equals(jsonBytes(review))) throw Error('CONTEXT_INPUT_REVIEW_NONCANONICAL_BYTES');
  if (!exactKeys(review, keys) || review.schema_version !== 'gemini-context-v5-context-input-final-review-v1' || review.review_id !== expected.review_id || review.role !== expected.role || review.agent_id !== expected.agent_id || review.status !== 'PASS' || review.candidate_ref !== CONTEXT_INPUT_REVIEWED_CANDIDATE || review.candidate_manifest_sha256 !== CONTEXT_INPUT_REVIEWED_MANIFEST || review.round_id !== pending.round_id || review.context_queue_sha256 !== pending.context_input_state.context_queue_sha256 || review.context_source_anchors_sha256 !== pending.context_input_state.context_source_anchors_sha256 || review.context_queue_view_sha256 !== pending.context_input_state.context_queue_view_sha256 || review.context_source_anchors_authorization_sha256 !== pending.context_input_state.context_source_anchors_authorization_sha256 || !Array.isArray(review.findings) || review.findings.length !== 0 || typeof review.recorded_at !== 'string') throw Error('CONTEXT_INPUT_REVIEW_CONTENT');
  return review;
}

export function validateContextInputReviewGate(repo, pending) {
  validateContextInputCandidateManifest(repo);
  const binding = pending.context_input_state?.implementation_review_gate;
  if (!exactKeys(binding, ['status', 'record_path', 'record_sha256']) || binding.status !== 'SATISFIED_FINAL_DUAL_PASS' || binding.record_path !== CONTEXT_INPUT_GATE_PATH || !/^[0-9a-f]{64}$/u.test(binding.record_sha256)) throw Error('CONTEXT_INPUT_REVIEW_GATE_BINDING');
  const file = path.join(repo, binding.record_path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_INPUT_REVIEW_GATE_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== binding.record_sha256) throw Error('CONTEXT_INPUT_REVIEW_GATE_HASH');
  const gate = JSON.parse(bytes), keys = ['schema_version', 'gate_id', 'status', 'candidate_ref', 'candidate_manifest_sha256', 'normal_final_review', 'senior_final_review', 'authorized_input_boundary', 'auditor_payload', 'permitted_next_action', 'forbidden_before_valid_auditor_output', 'context_audit_executed', 'recorded_at'];
  const forbidden = ['CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json', 'RELEASE.json', 'FURTHER_ROUNDS', 'REPLACEMENTS', 'QUALIFICATION', 'MUTATION', 'REFERENCE', 'FORMAL_GEMINI_INFERENCE'];
  if (!bytes.equals(jsonBytes(gate))) throw Error('CONTEXT_INPUT_REVIEW_GATE_NONCANONICAL_BYTES');
  if (!exactKeys(gate, keys) || gate.schema_version !== 'gemini-context-v5-context-input-review-gate-v1' || gate.gate_id !== 'V5-CONTEXT-INPUT-DUAL-REVIEW-GATE-001' || gate.status !== 'SATISFIED_FINAL_DUAL_PASS' || gate.candidate_ref !== CONTEXT_INPUT_REVIEWED_CANDIDATE || gate.candidate_manifest_sha256 !== CONTEXT_INPUT_REVIEWED_MANIFEST || gate.permitted_next_action !== 'GO_CONTEXT_AUDITOR_INPUT_ONLY' || JSON.stringify(gate.forbidden_before_valid_auditor_output) !== JSON.stringify(forbidden) || gate.context_audit_executed !== false || typeof gate.recorded_at !== 'string') throw Error('CONTEXT_INPUT_REVIEW_GATE_SCHEMA');
  const expectedBoundary = {round_id: pending.round_id, stage: 'CONTEXT', context_queue_sha256: pending.context_input_state.context_queue_sha256, context_source_anchors_sha256: pending.context_input_state.context_source_anchors_sha256, context_queue_view_sha256: pending.context_input_state.context_queue_view_sha256, context_authorization_sha256: pending.context_authorization.record_sha256, context_source_anchors_authorization_sha256: pending.context_input_state.context_source_anchors_authorization_sha256};
  if (!exactKeys(gate.authorized_input_boundary, Object.keys(expectedBoundary)) || JSON.stringify(gate.authorized_input_boundary) !== JSON.stringify(expectedBoundary)) throw Error('CONTEXT_INPUT_REVIEW_GATE_INPUT_BOUNDARY');
  const expectedPayload = {path: `rounds/${pending.round_id}/CONTEXT-QUEUE-VIEW.json`, sha256: pending.context_input_state.context_queue_view_sha256};
  if (!exactKeys(gate.auditor_payload, Object.keys(expectedPayload)) || JSON.stringify(gate.auditor_payload) !== JSON.stringify(expectedPayload)) throw Error('CONTEXT_INPUT_REVIEW_GATE_AUDITOR_PAYLOAD');
  const normal = readContextInputReview(repo, gate.normal_final_review, CONTEXT_INPUT_NORMAL, pending), senior = readContextInputReview(repo, gate.senior_final_review, CONTEXT_INPUT_SENIOR, pending);
  for (const review of [normal, senior]) if (review.candidate_ref !== gate.candidate_ref || review.candidate_manifest_sha256 !== gate.candidate_manifest_sha256) throw Error('CONTEXT_INPUT_REVIEW_CANDIDATE_BINDING');
  return {satisfied: true, candidate_ref: gate.candidate_ref, gate_sha256: sha256(bytes), permitted_next_action: gate.permitted_next_action};
}

export function evaluateContextInputReviewGate(repo, pending) {
  try { return {decision: 'GO_CONTEXT_AUDITOR_INPUT_ONLY', ...validateContextInputReviewGate(repo, pending)}; }
  catch (error) { return {decision: 'NO_GO', satisfied: false, reason: error.code === 'ENOENT' ? 'CONTEXT_INPUT_REVIEW_RECORD_MISSING' : error.message}; }
}

function validateContextResultsCandidateManifest(repo) {
  const file = path.join(repo, CONTEXT_RESULTS_MANIFEST_PATH), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_RESULTS_CANDIDATE_MANIFEST_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== CONTEXT_RESULTS_REVIEWED_MANIFEST) throw Error('CONTEXT_RESULTS_CANDIDATE_MANIFEST_HASH');
  const manifest = JSON.parse(bytes);
  if (!bytes.equals(jsonBytes(manifest)) || manifest.schema_version !== 1 || manifest.candidate_ref !== CONTEXT_RESULTS_REVIEWED_CANDIDATE || manifest.status !== 'CONTEXT_RESULTS_IMPLEMENTATION_PENDING_INDEPENDENT_DUAL_REVIEW' || !Array.isArray(manifest.files) || manifest.files.length !== 28 || manifest.exclusions?.includes('.ai/task/research-gemini-context-counterexample-reviewer-v5/STATE.json') !== true || manifest.exclusions?.includes(CONTEXT_RESULTS_MANIFEST_PATH) !== true) throw Error('CONTEXT_RESULTS_CANDIDATE_MANIFEST_SCHEMA');
  const files = manifest.files, sorted = [...files].sort((a, b) => Buffer.compare(Buffer.from(a.path), Buffer.from(b.path)));
  if (JSON.stringify(files) !== JSON.stringify(sorted) || new Set(files.map(item => item.path)).size !== files.length || files.some(item => !exactKeys(item, ['path', 'sha256']) || typeof item.path !== 'string' || item.path.startsWith('/') || item.path.includes('..') || !/^[0-9a-f]{64}$/u.test(item.sha256))) throw Error('CONTEXT_RESULTS_CANDIDATE_MANIFEST_FILES');
  if (sha256(Buffer.concat(files.map(item => Buffer.from(`${item.path}\0${item.sha256}\n`)))) !== CONTEXT_RESULTS_REVIEWED_CANDIDATE) throw Error('CONTEXT_RESULTS_CANDIDATE_MANIFEST_ROOT');
  return manifest;
}

function readContextResultsReview(repo, binding, expected, pending) {
  if (!exactKeys(binding, ['path', 'sha256', 'agent_id', 'role', 'status']) || binding.path !== expected.path || binding.agent_id !== expected.agent_id || binding.role !== expected.role || binding.status !== 'PASS' || !/^[0-9a-f]{64}$/u.test(binding.sha256)) throw Error('CONTEXT_RESULTS_REVIEW_BINDING_SCHEMA');
  const file = path.join(repo, binding.path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_RESULTS_REVIEW_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== binding.sha256) throw Error('CONTEXT_RESULTS_REVIEW_HASH');
  const review = JSON.parse(bytes), keys = ['schema_version', 'review_id', 'role', 'agent_id', 'status', 'candidate_ref', 'candidate_manifest_path', 'candidate_manifest_sha256', 'round_id', 'context_queue_sha256', 'context_source_anchors_sha256', 'context_queue_view_sha256', 'durable_response_path', 'durable_response_sha256', 'expected_context_records_sha256', 'expected_context_aggregate_sha256', 'verdict_counts', 'findings', 'recorded_at'];
  const responsePath = `evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/${pending.validated_context_response.artifact_path}`;
  if (!bytes.equals(jsonBytes(review))) throw Error('CONTEXT_RESULTS_REVIEW_NONCANONICAL_BYTES');
  if (!exactKeys(review, keys) || review.schema_version !== 'gemini-context-v5-context-results-final-review-v1' || review.review_id !== expected.review_id || review.role !== expected.role || review.agent_id !== expected.agent_id || review.status !== 'PASS' || review.candidate_ref !== CONTEXT_RESULTS_REVIEWED_CANDIDATE || review.candidate_manifest_path !== CONTEXT_RESULTS_MANIFEST_PATH || review.candidate_manifest_sha256 !== CONTEXT_RESULTS_REVIEWED_MANIFEST || review.round_id !== pending.round_id || review.context_queue_sha256 !== pending.context_input_state.context_queue_sha256 || review.context_source_anchors_sha256 !== pending.context_input_state.context_source_anchors_sha256 || review.context_queue_view_sha256 !== pending.context_input_state.context_queue_view_sha256 || review.durable_response_path !== responsePath || review.durable_response_sha256 !== pending.validated_context_response.artifact_sha256 || review.expected_context_records_sha256 !== pending.validated_context_response.expected_context_records_sha256 || review.expected_context_aggregate_sha256 !== pending.validated_context_response.expected_context_aggregate_sha256 || JSON.stringify(review.verdict_counts) !== JSON.stringify(pending.validated_context_response.verdict_counts) || !Array.isArray(review.findings) || review.findings.length !== 0 || typeof review.recorded_at !== 'string') throw Error('CONTEXT_RESULTS_REVIEW_CONTENT');
  return review;
}

export function validateContextResultsReviewGate(repo, pending) {
  validateContextResultsCandidateManifest(repo);
  const binding = pending.context_results_state?.implementation_review_gate;
  if (!exactKeys(binding, ['status', 'record_path', 'record_sha256']) || binding.status !== 'SATISFIED_FINAL_DUAL_PASS' || binding.record_path !== CONTEXT_RESULTS_GATE_PATH || binding.record_sha256 !== CONTEXT_RESULTS_GATE_SHA256) throw Error('CONTEXT_RESULTS_REVIEW_GATE_BINDING');
  const file = path.join(repo, binding.record_path), stat = fs.lstatSync(file);
  if (stat.isSymbolicLink() || !stat.isFile()) throw Error('CONTEXT_RESULTS_REVIEW_GATE_FILE_TYPE');
  const bytes = fs.readFileSync(file); if (sha256(bytes) !== CONTEXT_RESULTS_GATE_SHA256) throw Error('CONTEXT_RESULTS_REVIEW_GATE_HASH');
  const gate = JSON.parse(bytes), keys = ['schema_version', 'gate_id', 'status', 'candidate_ref', 'candidate_manifest_path', 'candidate_manifest_sha256', 'normal_final_review', 'senior_final_review', 'authorized_results_boundary', 'permitted_next_action', 'authorized_materialization', 'forbidden_after_materialization', 'context_results_materialized', 'recorded_at'];
  const forbidden = ['RELEASE.json', 'FURTHER_ROUNDS', 'REPLACEMENTS', 'QUALIFICATION', 'MUTATION', 'REFERENCE', 'FORMAL_GEMINI_INFERENCE'];
  if (!bytes.equals(jsonBytes(gate))) throw Error('CONTEXT_RESULTS_REVIEW_GATE_NONCANONICAL_BYTES');
  if (!exactKeys(gate, keys) || gate.schema_version !== 'gemini-context-v5-context-results-review-gate-v1' || gate.gate_id !== 'V5-CONTEXT-RESULTS-DUAL-REVIEW-GATE-001' || gate.status !== 'SATISFIED_FINAL_DUAL_PASS' || gate.candidate_ref !== CONTEXT_RESULTS_REVIEWED_CANDIDATE || gate.candidate_manifest_path !== CONTEXT_RESULTS_MANIFEST_PATH || gate.candidate_manifest_sha256 !== CONTEXT_RESULTS_REVIEWED_MANIFEST || gate.permitted_next_action !== 'GO_CONTEXT_RESULTS_MATERIALIZATION_ONLY' || JSON.stringify(gate.authorized_materialization) !== JSON.stringify(['CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json']) || JSON.stringify(gate.forbidden_after_materialization) !== JSON.stringify(forbidden) || gate.context_results_materialized !== false || typeof gate.recorded_at !== 'string') throw Error('CONTEXT_RESULTS_REVIEW_GATE_SCHEMA');
  const expectedBoundary = {round_id: pending.round_id, stage: 'CONTEXT', real_input_artifact_count: 7, materialized_artifact_count: 9, context_queue_sha256: pending.context_input_state.context_queue_sha256, context_source_anchors_sha256: pending.context_input_state.context_source_anchors_sha256, context_queue_view_sha256: pending.context_input_state.context_queue_view_sha256, durable_response_path: `evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/${pending.validated_context_response.artifact_path}`, durable_response_sha256: pending.validated_context_response.artifact_sha256, expected_context_records_sha256: pending.validated_context_response.expected_context_records_sha256, expected_context_aggregate_sha256: pending.validated_context_response.expected_context_aggregate_sha256, verdict_counts: pending.validated_context_response.verdict_counts};
  if (!exactKeys(gate.authorized_results_boundary, Object.keys(expectedBoundary)) || JSON.stringify(gate.authorized_results_boundary) !== JSON.stringify(expectedBoundary)) throw Error('CONTEXT_RESULTS_REVIEW_GATE_RESULTS_BOUNDARY');
  const normal = readContextResultsReview(repo, gate.normal_final_review, CONTEXT_RESULTS_NORMAL, pending), senior = readContextResultsReview(repo, gate.senior_final_review, CONTEXT_RESULTS_SENIOR, pending);
  for (const review of [normal, senior]) if (review.candidate_ref !== gate.candidate_ref || review.candidate_manifest_sha256 !== gate.candidate_manifest_sha256) throw Error('CONTEXT_RESULTS_REVIEW_CANDIDATE_BINDING');
  return {satisfied: true, candidate_ref: gate.candidate_ref, gate_sha256: sha256(bytes), permitted_next_action: gate.permitted_next_action};
}

export function evaluateContextResultsReviewGate(repo, pending) {
  try { return {decision: 'GO_CONTEXT_RESULTS_MATERIALIZATION_ONLY', ...validateContextResultsReviewGate(repo, pending)}; }
  catch (error) { return {decision: 'NO_GO', satisfied: false, reason: error.code === 'ENOENT' ? 'CONTEXT_RESULTS_REVIEW_RECORD_MISSING' : error.message}; }
}
export function replay(root = here) {
  if (arguments.length > 1) throw Error('ROUND_RELEASE_RUNTIME_PIN_OVERRIDE_FORBIDDEN');
  const {frame, reserves} = readInitialPackage(root); const state = initialize(frame, reserves);
  const repo = path.resolve(root, '..', '..', '..', '..'), reviewRepoAvailable = fs.existsSync(path.join(repo, '.ai', 'task', 'research-gemini-context-counterexample-reviewer-v5'));
  const pendingPath = path.join(root, 'PENDING-RELEASE.json');
  const pendingBytes = fs.existsSync(pendingPath) ? fs.readFileSync(pendingPath) : null;
  const pending = pendingBytes ? JSON.parse(pendingBytes) : null;
  if (pendingBytes && !pendingBytes.equals(jsonBytes(pending))) throw Error('PENDING_RELEASE_NONCANONICAL_BYTES');
  const pendingRound2Release = pending?.schema_version === 'gemini-context-v5-round-0002-pending-release-v1';
  const roundsDir = path.join(root, 'rounds');
  const round2Dir = path.join(roundsDir, 'ROUND-0002');
  const inferredRound2SurfaceInput = !pending && fs.existsSync(round2Dir) && !fs.existsSync(path.join(round2Dir, 'RELEASE.json')) ? 'ROUND-0002' : null;
  const bundles = readRoundBundles(roundsDir, pending?.round_id ?? inferredRound2SurfaceInput), pendingSurface = bundles.find(bundle => bundle.pending_surface_stage) ?? null, pendingRound2SurfaceInput = bundles.find(bundle => bundle.pending_surface_input) ?? null;
  for (const bundle of bundles.filter(item => !item.pending_surface_stage && !item.pending_surface_input)) {
    const reviewed = reviewRepoAvailable ? {...bundle, review_repo: repo} : bundle;
    const release = JSON.parse(bundle.release);
    // ROUND-0001's v3 release is the only release that consumes the strict
    // repository-review provenance path.  Later releases are ordinary round
    // bundles; applyRound owns their schema-specific validation (including
    // ROUND-0002 context-v3/release-v4).
    if (release.schema_version === 'gemini-context-v5-round-release-v3') {
      if (!reviewRepoAvailable) throw Error('ROUND_RELEASE_REVIEW_REPO_REQUIRED');
      applyReviewedProvenanceRound(state, reviewed);
    } else {
      applyRound(state, reviewed);
    }
  }
  if (pendingRound2Release) {
    if (!pendingSurface?.pending_context_results || state.round !== 1 || state.lastReleaseSha256 !== pending.predecessor_release_sha256) throw Error('ROUND2_PENDING_RELEASE_PREDECESSOR_STATE');
    validateRound2SurfaceInput({root, repo, state, bundle: pendingSurface});
    validateRound2SurfaceArtifacts({root});
    validateRound2ContextInput({root, repo, queueBytes: pendingSurface.context_queue, anchorsBytes: pendingSurface.context_source_anchors, viewBytes: pendingSurface.context_queue_view});
    validateRound2ContextArtifacts({root});
    validateRound2PendingRelease(root, repo);
  } else if (pending) validatePendingSurface(root, repo, state, pending, pendingSurface);
  if (pendingRound2SurfaceInput) validateRound2SurfaceInput({root, repo, state, bundle: pendingRound2SurfaceInput});
  if (!pending && inferredRound2SurfaceInput === 'ROUND-0002' && pendingSurface) {
    validateRound2SurfaceInput({root, repo, state, bundle: pendingSurface});
    validatePendingSurfaceArtifacts({repo, state, queueBytes: pendingSurface.surface_queue, queueViewBytes: pendingSurface.surface_queue_view, recordsBytes: pendingSurface.surface_records, aggregateBytes: pendingSurface.surface_aggregate, selfContained: true});
    validateRound2SurfaceArtifacts({root});
    if(pendingSurface.pending_context_input||pendingSurface.pending_context_results)validateRound2ContextInput({root,repo,queueBytes:pendingSurface.context_queue,anchorsBytes:pendingSurface.context_source_anchors,viewBytes:pendingSurface.context_queue_view});
    if(pendingSurface.pending_context_results)validateRound2ContextArtifacts({root});
  }
  return outputDocuments(state, pendingRound2Release ? null : pending);
}

export function validatePendingSurface(root, repo, state, pending, pendingSurface = null) {
  const pendingKeys = ['schema_version', 'status', 'round_id', 'stage', 'authorization_id', 'authorization_record_path', 'authorization_record_sha256', 'authorized_candidate_ref', 'final_pass_reviewer_agent_ids', 'active_frame_sha256', 'predecessor_release_sha256', 'surface_queue_sha256', 'surface_queue_view_sha256', 'sidecar_review_gate_record_path', 'sidecar_review_gate_record_sha256', 'sidecar_review_gate_status', 'invalid_attempt_exclusion', 'validated_surface_response', 'validated_context_response', 'implementation_candidate_binding', 'surface_intermediate_state', 'context_authorization', 'context_input_state', 'context_results_state', 'allowed_next_transition', 'surface_audit_retry_input_authorized', 'forbidden_after_context_input_freeze', 'authorized_surface_auditor_calls_started', 'authorized_context_auditor_calls_started', 'invalid_auditor_input_attempts', 'valid_surface_auditor_responses', 'valid_persisted_surface_results', 'valid_context_auditor_responses', 'valid_persisted_context_results', 'formal_gemini_experiment_inference_calls_made', 'network_calls_made'];
  const forbidden = ['RELEASE.json', 'FURTHER_ROUNDS', 'REPLACEMENTS', 'QUALIFICATION', 'MUTATION', 'REFERENCE', 'FORMAL_GEMINI_INFERENCE'];
  const materialized = pending.context_results_state?.records_materialized === true && pending.context_results_state?.aggregate_materialized === true;
  const expectedStatus = materialized ? 'CONTEXT_RESULTS_MATERIALIZED_PENDING_REPLACEMENT_RELEASE_AUTHORIZATION' : 'CONTEXT_RESULTS_DUAL_PASS_PENDING_MATERIALIZATION';
  const expectedTransition = materialized ? 'NO_GO_REPLACEMENT_RELEASE_NOT_AUTHORIZED' : 'GO_CONTEXT_RESULTS_MATERIALIZATION_ONLY';
  if (JSON.stringify(Object.keys(pending).sort()) !== JSON.stringify([...pendingKeys].sort()) || pending.schema_version !== 'gemini-context-v5-pending-context-input-v1' || pending.status !== expectedStatus || pending.round_id !== `ROUND-${String(state.round + 1).padStart(4, '0')}` || pending.stage !== 'CONTEXT' || pending.authorization_record_path !== '.ai/task/research-gemini-context-counterexample-reviewer-v5/AUDIT-AUTHORIZATION-001.json' || pending.active_frame_sha256 !== activeFrameSha256(state) || pending.predecessor_release_sha256 !== state.lastReleaseSha256 || pending.allowed_next_transition !== expectedTransition || pending.surface_audit_retry_input_authorized !== true || JSON.stringify(pending.forbidden_after_context_input_freeze) !== JSON.stringify(forbidden) || pending.authorized_surface_auditor_calls_started !== 2 || pending.authorized_context_auditor_calls_started !== 1 || pending.invalid_auditor_input_attempts !== 1 || pending.valid_surface_auditor_responses !== 1 || pending.valid_persisted_surface_results !== 1 || pending.valid_context_auditor_responses !== 1 || pending.valid_persisted_context_results !== (materialized ? 1 : 0) || pending.formal_gemini_experiment_inference_calls_made !== 0 || pending.network_calls_made !== 0) throw Error('PENDING_RELEASE_BINDING');
  validateSidecarReviewGate(repo, pending);
  validateIntermediateCandidateBinding(repo, pending);
  const exclusion = pending.invalid_attempt_exclusion, exclusionKeys = ['record_path', 'record_sha256', 'status', 'failure_class', 'excluded_verdict_count', 'all_verdicts_non_adjudicative'];
  if (!exclusion || JSON.stringify(Object.keys(exclusion).sort()) !== JSON.stringify(exclusionKeys.sort()) || exclusion.record_path !== '.ai/task/research-gemini-context-counterexample-reviewer-v5/INVALID-AUDIT-ATTEMPT-001.json' || exclusion.record_sha256 !== '629f31e9a5692f1378c191fb3b49cc4cb4ca8ba8683bf21fa560c60a5645170f' || exclusion.status !== 'INVALID_AUDITOR_INPUT' || exclusion.failure_class !== 'HARNESS_INPUT_DEFECT' || exclusion.excluded_verdict_count !== 64 || exclusion.all_verdicts_non_adjudicative !== true) throw Error('INVALID_ATTEMPT_EXCLUSION_SCHEMA');
  const invalidPath = path.join(repo, exclusion.record_path), invalidBytes = fs.readFileSync(invalidPath), invalid = JSON.parse(invalidBytes);
  if (sha256(invalidBytes) !== exclusion.record_sha256 || invalid.status !== exclusion.status || invalid.failure_class !== exclusion.failure_class || invalid.adjudication?.excluded_verdict_count !== exclusion.excluded_verdict_count || invalid.adjudication?.all_verdicts_non_adjudicative !== true || invalid.formal_gemini_experiment_inference_calls_made !== 0) throw Error('INVALID_ATTEMPT_EXCLUSION_BINDING');
  const queueBytes = fs.readFileSync(path.join(root, 'rounds', pending.round_id, 'SURFACE-QUEUE.json')), queue = JSON.parse(queueBytes);
  if (!queueBytes.equals(jsonBytes(queue)) || sha256(queueBytes) !== pending.surface_queue_sha256) throw Error('PENDING_SURFACE_QUEUE_BYTES');
  const queueKeys = ['schema_version', 'round_id', 'stage', 'active_frame_sha256', 'predecessor_release_sha256', 'authorization_id', 'authorization_record_sha256', 'authorized_candidate_ref', 'final_pass_reviewer_agent_ids', 'items'];
  const expectedItems = state.active.map(row => ({neutral_id: row.neutral_id, revision_id: row.revision_id, row_identity_sha256: rowIdentity(row)}));
  if (JSON.stringify(Object.keys(queue).sort()) !== JSON.stringify([...queueKeys].sort()) || queue.schema_version !== 'gemini-context-v5-surface-queue-v2' || queue.round_id !== pending.round_id || queue.stage !== 'SURFACE' || queue.active_frame_sha256 !== pending.active_frame_sha256 || queue.predecessor_release_sha256 !== pending.predecessor_release_sha256 || queue.authorization_id !== pending.authorization_id || queue.authorization_record_sha256 !== pending.authorization_record_sha256 || queue.authorized_candidate_ref !== pending.authorized_candidate_ref || JSON.stringify(queue.final_pass_reviewer_agent_ids) !== JSON.stringify(pending.final_pass_reviewer_agent_ids) || JSON.stringify(queue.items) !== JSON.stringify(expectedItems)) throw Error('PENDING_SURFACE_QUEUE_BINDING');
  const viewPath = path.join(root, 'rounds', pending.round_id, 'SURFACE-QUEUE-VIEW.json'), viewStat = fs.lstatSync(viewPath);
  if (viewStat.isSymbolicLink() || !viewStat.isFile()) throw Error('PENDING_SURFACE_QUEUE_VIEW_TYPE');
  const viewBytes = fs.readFileSync(viewPath), response = pending.validated_surface_response;
  if (response.verdict_counts?.PASS_SURFACE !== 55 || response.verdict_counts?.NOT_CLEAN !== 9 || response.verdict_counts?.OUT_OF_SCOPE_NON_PROSE !== 0) throw Error('VALIDATED_SURFACE_RESPONSE_BINDING');
  loadValidatedSurfaceAuditorResponse({root, binding: response, queueBytes, queueViewBytes: viewBytes});
  const viewParsed = JSON.parse(viewBytes);
  if (!viewBytes.equals(jsonBytes(viewParsed)) || sha256(viewBytes) !== pending.surface_queue_view_sha256) throw Error('PENDING_SURFACE_QUEUE_VIEW_HASH');
  const intermediate = pending.surface_intermediate_state, intermediateKeys = ['schema_version', 'status', 'artifact_mode', 'authorized_by_user', 'authorized_artifacts', 'records_materialized', 'aggregate_materialized', 'context_audit_authorized', 'replacements_authorized', 'release_authorized', 'implementation_review_gate'];
  if (!exactKeys(intermediate, intermediateKeys) || intermediate.schema_version !== 'gemini-context-v5-surface-intermediate-state-v1' || intermediate.authorized_by_user !== true || JSON.stringify(intermediate.authorized_artifacts) !== JSON.stringify(['SURFACE-RECORDS.json', 'SURFACE-AGGREGATE.json']) || intermediate.context_audit_authorized !== false || intermediate.replacements_authorized !== false || intermediate.release_authorized !== false) throw Error('SURFACE_INTERMEDIATE_STATE_SCHEMA');
  if (intermediate.status === 'IMPLEMENTATION_REVIEW_REQUIRED' && intermediate.artifact_mode === 'QUEUE_VIEW_ONLY' && intermediate.records_materialized === false && intermediate.aggregate_materialized === false) {
    if (pending.status !== 'SURFACE_INTERMEDIATE_IMPLEMENTATION_REVIEW_REQUIRED_NOT_MATERIALIZED' || pendingSurface || !exactKeys(intermediate.implementation_review_gate, ['status', 'record_path', 'record_sha256']) || intermediate.implementation_review_gate.status !== 'REQUIRED' || intermediate.implementation_review_gate.record_path !== INTERMEDIATE_GATE_PATH || intermediate.implementation_review_gate.record_sha256 !== null) throw Error('SURFACE_INTERMEDIATE_PRE_REVIEW_STATE');
    return;
  }
  if (intermediate.status !== 'SATISFIED_DUAL_PASS_SURFACE_STAGE_COMPLETED_PENDING_CONTEXT_AUDIT' || intermediate.artifact_mode !== 'SURFACE_STAGE_FOUR_FILES' || intermediate.records_materialized !== true || intermediate.aggregate_materialized !== true || !(pendingSurface?.pending_context_input || pendingSurface?.pending_context_results)) throw Error('SURFACE_INTERMEDIATE_MATERIALIZED_STATE');
  validateIntermediateReviewGate(repo, pending);
  const summary = validatePendingSurfaceArtifacts({repo, state, queueBytes: pendingSurface.surface_queue, queueViewBytes: pendingSurface.surface_queue_view, recordsBytes: pendingSurface.surface_records, aggregateBytes: pendingSurface.surface_aggregate, selfContained: true});
  if (summary.surface_records_sha256 !== response.expected_surface_records_sha256 || summary.surface_aggregate_sha256 !== response.expected_surface_aggregate_sha256 || JSON.stringify(summary.counts) !== JSON.stringify(response.verdict_counts) || summary.pass_ids.length !== 55 || summary.reject_ids.length !== 9) throw Error('SURFACE_INTERMEDIATE_ARTIFACT_BINDING');
  const authorization = pending.context_authorization, authorizationKeys = ['authorization_id','record_path','record_sha256','status','executor_agent_id','scout_agent_id'];
  if (!exactKeys(authorization, authorizationKeys) || authorization.authorization_id !== 'V5-ROUND-0001-CONTEXT-AUDIT-001' || authorization.record_path !== '.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-AUDIT-AUTHORIZATION-001.json' || authorization.record_sha256 !== '2e1bb1aa813365b2cd5f4adc5bfe3f263e8ca28f5cf455c7a8ac09ed8aaa9164' || authorization.status !== 'AUTHORIZED_QUEUE_VIEW_FREEZE_PENDING_INDEPENDENT_REVIEW' || authorization.executor_agent_id !== '9971457a-0885-4da2-a305-9396072223d9' || authorization.scout_agent_id !== '68e8bf27-89ea-423b-a1cd-7c7fd4f2811d') throw Error('CONTEXT_AUTHORIZATION_BINDING');
  const authorizationPath = path.join(repo, authorization.record_path), authorizationStat = fs.lstatSync(authorizationPath);
  if (authorizationStat.isSymbolicLink() || !authorizationStat.isFile()) throw Error('CONTEXT_AUTHORIZATION_FILE_TYPE');
  const authorizationBytes = fs.readFileSync(authorizationPath), authorizationRecord = JSON.parse(authorizationBytes);
  if (!authorizationBytes.equals(jsonBytes(authorizationRecord)) || sha256(authorizationBytes) !== authorization.record_sha256 || authorizationRecord.authorization_id !== authorization.authorization_id || authorizationRecord.status !== authorization.status || authorizationRecord.transition_executor?.agent_id !== authorization.executor_agent_id || authorizationRecord.scout?.agent_id !== authorization.scout_agent_id || authorizationRecord.scope?.context_queue_and_view_item_count !== 55 || authorizationRecord.scope?.auditor_call_started !== false || authorizationRecord.scope?.context_records_created !== false || authorizationRecord.scope?.context_aggregate_created !== false || authorizationRecord.scope?.replacements_authorized !== false || authorizationRecord.scope?.release_authorized !== false || authorizationRecord.scope?.later_rounds_authorized !== false || authorizationRecord.scope?.formal_gemini_inference_authorized !== false || authorizationRecord.predecessor_release_sha256 !== null) throw Error('CONTEXT_AUTHORIZATION_CONTENT');
  const contextState = pending.context_input_state, contextStateKeys = ['schema_version','status','item_count','context_queue_sha256','context_source_anchors_sha256','context_source_anchors_authorization_path','context_source_anchors_authorization_sha256','context_queue_view_sha256','source_bytes_and_coordinates_verified','self_contained_v5_replay','auditor_call_started','context_records_materialized','context_aggregate_materialized','implementation_review_gate'];
  if (!exactKeys(contextState, contextStateKeys) || contextState.schema_version !== 'gemini-context-v5-context-input-state-v2' || contextState.status !== 'SATISFIED_FINAL_DUAL_PASS' || contextState.item_count !== 55 || contextState.context_source_anchors_sha256!==CONTEXT_SOURCE_ANCHORS_SHA256 || contextState.context_source_anchors_authorization_path!=='.ai/task/research-gemini-context-counterexample-reviewer-v5/CONTEXT-SOURCE-ANCHORS-AUTHORIZATION-001.json' || contextState.context_source_anchors_authorization_sha256!==CONTEXT_SOURCE_ANCHORS_AUTHORIZATION_SHA256 || contextState.source_bytes_and_coordinates_verified !== true || contextState.self_contained_v5_replay !== true || contextState.auditor_call_started !== true || contextState.context_records_materialized !== materialized || contextState.context_aggregate_materialized !== materialized) throw Error('CONTEXT_INPUT_STATE');
  validateContextInputReviewGate(repo, pending);
  const anchorAuthorizationPath=path.join(repo,contextState.context_source_anchors_authorization_path),anchorAuthorizationStat=fs.lstatSync(anchorAuthorizationPath);if(anchorAuthorizationStat.isSymbolicLink()||!anchorAuthorizationStat.isFile())throw Error('CONTEXT_SOURCE_ANCHOR_AUTHORIZATION_TYPE');
  const anchorAuthorizationBytes=fs.readFileSync(anchorAuthorizationPath),anchorAuthorization=JSON.parse(anchorAuthorizationBytes);if(!anchorAuthorizationBytes.equals(jsonBytes(anchorAuthorization))||sha256(anchorAuthorizationBytes)!==CONTEXT_SOURCE_ANCHORS_AUTHORIZATION_SHA256||anchorAuthorization.authorization_id!=='V5-ROUND-0001-CONTEXT-SOURCE-ANCHORS-001'||anchorAuthorization.status!=='AUTHORIZED_IMMUTABLE_SOURCE_ANCHORS_PENDING_FINAL_DUAL_REREVIEW'||anchorAuthorization.original_context_authorization_sha256!==authorization.record_sha256||anchorAuthorization.context_queue_sha256!==contextState.context_queue_sha256||anchorAuthorization.context_source_anchors_sha256!==CONTEXT_SOURCE_ANCHORS_SHA256||anchorAuthorization.fixed_source_commit!=='624a67329fe2ad440c5b344785a9c73fcf22ae63'||anchorAuthorization.scope?.pending_artifact_count!==7||anchorAuthorization.scope?.auditor_call_started!==false)throw Error('CONTEXT_SOURCE_ANCHOR_AUTHORIZATION_BINDING');
  const frozen = validateFrozenContextInputBytes({surfaceQueueBytes: pendingSurface.surface_queue, surfaceViewBytes: pendingSurface.surface_queue_view, surfaceRecordsBytes: pendingSurface.surface_records, surfaceAggregateBytes: pendingSurface.surface_aggregate, activeFrameBytes: jsonBytes(activeFrameDocument(state)), queueBytes: pendingSurface.context_queue, anchorsBytes:pendingSurface.context_source_anchors, viewBytes: pendingSurface.context_queue_view});
  if (sha256(frozen.queue.bytes) !== contextState.context_queue_sha256 || sha256(frozen.anchors.bytes)!==contextState.context_source_anchors_sha256 || sha256(frozen.view.bytes) !== contextState.context_queue_view_sha256) throw Error('CONTEXT_INPUT_HASH_BINDING');
  const contextResponse = loadValidatedContextAuditorResponse({root, binding: pending.validated_context_response, queueBytes: frozen.queue.bytes, anchorsBytes: frozen.anchors.bytes, viewBytes: frozen.view.bytes});
  if (contextResponse.counts.CLEAN_NO_MATERIAL_DEFECT !== 54 || contextResponse.counts.NOT_CLEAN !== 1) throw Error('CONTEXT_AUDITOR_RESPONSE_VERDICT_COUNTS');
  const results = pending.context_results_state, resultsKeys = ['schema_version', 'status', 'artifact_mode', 'authorized_artifacts_after_review', 'expected_context_records_sha256', 'expected_context_aggregate_sha256', 'records_materialized', 'aggregate_materialized', 'active_frame_mutated', 'lineage_mutated', 'reserve_mutated', 'completed_rounds_mutated', 'replacements_authorized', 'release_authorized', 'implementation_review_gate'];
  const expectedResultsStatus = materialized ? 'CONTEXT_RESULTS_MATERIALIZED_PENDING_REPLACEMENT_RELEASE_AUTHORIZATION' : 'SATISFIED_DUAL_PASS_PENDING_MATERIALIZATION';
  const expectedArtifactMode = materialized ? 'CONTEXT_RESULTS_NINE_FILES' : 'SEVEN_INPUTS_GATE_SATISFIED';
  if (!exactKeys(results, resultsKeys) || results.schema_version !== 'gemini-context-v5-pending-context-results-state-v1' || results.status !== expectedResultsStatus || results.artifact_mode !== expectedArtifactMode || JSON.stringify(results.authorized_artifacts_after_review) !== JSON.stringify(['CONTEXT-RECORDS.json', 'CONTEXT-AGGREGATE.json']) || results.expected_context_records_sha256 !== pending.validated_context_response.expected_context_records_sha256 || results.expected_context_aggregate_sha256 !== pending.validated_context_response.expected_context_aggregate_sha256 || results.records_materialized !== materialized || results.aggregate_materialized !== materialized || results.active_frame_mutated !== false || results.lineage_mutated !== false || results.reserve_mutated !== false || results.completed_rounds_mutated !== false || results.replacements_authorized !== false || results.release_authorized !== false) throw Error('CONTEXT_RESULTS_STATE');
  validateContextResultsReviewGate(repo, pending);
  if (!materialized) {
    if (!pendingSurface.pending_context_input || pendingSurface.pending_context_results) throw Error('CONTEXT_RESULTS_PRE_MATERIALIZATION_ARTIFACT_SET');
    return;
  }
  if (!pendingSurface.pending_context_results || pendingSurface.pending_context_input) throw Error('CONTEXT_RESULTS_MATERIALIZED_ARTIFACT_SET');
  const expectedContext = {context_records_sha256: pending.validated_context_response.expected_context_records_sha256, context_aggregate_sha256: pending.validated_context_response.expected_context_aggregate_sha256, counts: pending.validated_context_response.verdict_counts, clean_ids: contextResponse.parsed.items.filter(item => item.verdict === 'CLEAN_NO_MATERIAL_DEFECT').map(item => item.neutral_id), not_clean_ids: contextResponse.parsed.items.filter(item => item.verdict === 'NOT_CLEAN').map(item => item.neutral_id)};
  validatePendingContextResultsDirectory({roundDir: path.join(root, 'rounds', pending.round_id), state, expectedContext});
}
export function checkReplay(root = here, {allowUnverifiedFixture = false} = {}) {
  if (arguments.length > 2) throw Error('ROUND_RELEASE_RUNTIME_PIN_OVERRIDE_FORBIDDEN');
  const docs = replay(root);
  for (const [name, doc] of Object.entries(docs)) {
    const target = path.join(root, name); if (!fs.existsSync(target) || !fs.readFileSync(target).equals(jsonBytes(doc))) throw Error(`DETERMINISTIC_REPLAY_DRIFT:${name}`);
  }
  if (docs['ROUND-INDEX.json'].completed_rounds === 2 && fs.existsSync(path.join(root, 'rounds', 'ROUND-0002', 'RELEASE.json')) && JSON.parse(fs.readFileSync(path.join(root, 'rounds', 'ROUND-0002', 'RELEASE.json'))).schema_version === 'gemini-context-v5-round-release-v4') validateRound2CompletedReleaseEvidence(path.resolve(root, '..', '..', '..', '..'), {allowUnverifiedFixture});
  return {status: 'PASS', completed_rounds: docs['ROUND-INDEX.json'].completed_rounds, byte_identical_outputs: true};
}

const arg = process.argv[2], rootIndex = process.argv.indexOf('--root'), cliRoot = rootIndex >= 0 ? path.resolve(process.argv[rootIndex + 1] ?? '') : here;
if (import.meta.url === `file://${process.argv[1]}` && arg === '--check') {
  console.log(JSON.stringify(checkReplay(cliRoot), null, 2));
} else if (import.meta.url === `file://${process.argv[1]}` && arg === '--print') {
  const name = process.argv[3], docs = replay(cliRoot); if (!Object.hasOwn(docs, name)) throw Error('unknown output'); process.stdout.write(jsonBytes(docs[name]));
} else if (import.meta.url === `file://${process.argv[1]}` && arg === '--write-release-state') {
  const doc = replay(cliRoot)['RELEASE-STATE.json']; fs.writeFileSync(path.join(cliRoot, 'RELEASE-STATE.json'), jsonBytes(doc));
  console.log(JSON.stringify({status:'WROTE_DERIVED_RELEASE_STATE', sha256:sha256(jsonBytes(doc))}, null, 2));
} else if (import.meta.url === `file://${process.argv[1]}`) throw Error('usage: node replay.mjs --check [--root PACKAGE] | --print OUTPUT.json [--root PACKAGE] | --write-release-state [--root PACKAGE]');
