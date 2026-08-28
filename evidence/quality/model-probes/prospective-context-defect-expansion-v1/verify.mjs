#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {buildPackage, GENERATED_NAMES} from "./build.mjs";
import {locatorContentKey, sha256Bytes} from "../prospective-source-context-audit-v4/build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");
const canonicalBytes = value => Buffer.from(JSON.stringify(value), "utf8");
const priorContextArtifacts = [
  ["evidence/quality/model-probes/source-context-exploratory-four-route-v1/INPUT-B.json", "05893599fd1fad889d0cc36811565b2693933b09d069b9f59028143b7dd9a764"],
  ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/CONTEXT-QUEUE-1.json", "735fe3465c60c1373ee491c80466f083958086711fa4186d7cee2111700cab60"],
  ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/CONTEXT-QUEUE-2.json", "00aae61e04cbf7de07aaf618da566ca9aae2151619fafc127caf26372874e23d"],
  ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/CONTEXT-QUEUE-3.json", "416da410ed6beddfc23c9b655accfbd77fd5f8506eb67c1899e31e6e45be5c1e"]
];
const generatedRecord = file => {
  const bytes = fs.readFileSync(file);
  return {sha256: sha256Bytes(bytes), size_bytes: bytes.length};
};

function parseArgs(argv) {
  const args = {root: defaultRoot};
  const allowed = new Set(["--root", "--production-repo", "--engine-repo", "--dlc-root"]);
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!allowed.has(flag) || !value) throw new Error("usage: node verify.mjs --production-repo REPO --engine-repo REPO --dlc-root ROOT [--root REPO]");
    args[flag.slice(2).replace(/-([a-z])/gu, (_match, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  for (const key of ["productionRepo", "engineRepo", "dlcRoot"]) if (!args[key]) throw new Error(`missing ${key}`);
  return args;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function exactKeys(value, expected, label) {
  assert.ok(value && typeof value === "object" && !Array.isArray(value), `${label}: expected object`);
  assert.deepEqual(Object.keys(value).sort(), [...expected].sort(), `${label}: exact key set`);
}

function walk(value, visitor, pointer = "") {
  if (Array.isArray(value)) return value.forEach((entry, index) => walk(entry, visitor, `${pointer}/${index}`));
  if (!value || typeof value !== "object") return;
  for (const [key, entry] of Object.entries(value)) {
    visitor(key, entry, `${pointer}/${key}`);
    walk(entry, visitor, `${pointer}/${key}`);
  }
}

function collectStrings(value, output = []) {
  if (typeof value === "string") output.push(value);
  else if (Array.isArray(value)) value.forEach(entry => collectStrings(entry, output));
  else if (value && typeof value === "object") Object.values(value).forEach(entry => collectStrings(entry, output));
  return output;
}

const escapePointerToken = value => value.replace(/~/gu, "~0").replace(/\//gu, "~1");
function collectStringLeaves(value, logicalPath, pointer = "", output = []) {
  if (typeof value === "string") output.push({logical_path: logicalPath, json_pointer: pointer, value});
  else if (Array.isArray(value)) value.forEach((entry, index) => collectStringLeaves(entry, logicalPath, `${pointer}/${index}`, output));
  else if (value && typeof value === "object") {
    for (const [key, entry] of Object.entries(value)) collectStringLeaves(entry, logicalPath, `${pointer}/${escapePointerToken(key)}`, output);
  }
  return output;
}

function matchesForSource(source, leaves) {
  const matches = [];
  for (const leaf of leaves) {
    if (leaf.value === source) matches.push({logical_path: leaf.logical_path, json_pointer: leaf.json_pointer, method: "exact_string_leaf"});
    else if (leaf.value.includes(source)) matches.push({logical_path: leaf.logical_path, json_pointer: leaf.json_pointer, method: "strict_longer_string_leaf"});
  }
  return matches;
}

function verifySourceArtifact(binding, args) {
  let bytes;
  if (binding.kind === "git_commit_blob") {
    assert.equal(binding.commit, "624a67329fe2ad440c5b344785a9c73fcf22ae63");
    bytes = execFileSync("git", ["-C", args.engineRepo, "show", `${binding.commit}:${binding.relative_path}`], {maxBuffer: 128 * 1024 * 1024});
  } else if (binding.kind === "dlc_file_sha256") {
    const subdirectories = {cults: "cults/tome-cults", orcs: "orcs/tome-orcs", "ashes-urhrok": "ashes-urhrok/tome-ashes-urhrok"};
    const registeredRoot = fs.realpathSync(path.resolve(args.dlcRoot, subdirectories[binding.component]));
    const candidate = fs.realpathSync(path.resolve(registeredRoot, binding.relative_path));
    const relative = path.relative(registeredRoot, candidate);
    assert.ok(relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative), "DLC source escaped root");
    bytes = fs.readFileSync(candidate);
  } else throw new Error(`unknown source binding ${binding.kind}`);
  assert.equal(sha256Bytes(bytes), binding.source_artifact_sha256, `${binding.component}/${binding.relative_path}: source artifact hash`);
  assert.equal(bytes.length, binding.source_artifact_size_bytes, `${binding.component}/${binding.relative_path}: source artifact size`);
}

const args = parseArgs(process.argv.slice(2));
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-context-expansion-verify-"));
try {
  buildPackage({...args, out: temporary});
  for (const name of GENERATED_NAMES) {
    const expected = fs.readFileSync(path.join(here, name));
    const actual = fs.readFileSync(path.join(temporary, name));
    assert.deepEqual(actual, expected, `${name}: deterministic rebuild differs`);
    JSON.parse(expected.toString("utf8"));
  }

  const exclusion = readJson(path.join(here, "SOURCE-EXCLUSION-REGISTRY.json"));
  const evidence = readJson(path.join(here, "SOURCE-EVIDENCE-POOL.json"));
  const bindings = readJson(path.join(here, "IDENTITY-TARGET-BINDING-REGISTRY.json"));
  const candidates = readJson(path.join(here, "FUTURE-MODEL-CANDIDATES.json"));
  const report = readJson(path.join(here, "BUILD-REPORT.json"));
  const experiment = readJson(path.join(here, "EXPERIMENT.json"));

  exactKeys(exclusion, ["schema_version", "status", "source_only", "normalization", "v4_selected_exclusions", "four_route_subset_proof", "case_control_overlay", "prior_model_facing_context_overlay"], "SOURCE-EXCLUSION-REGISTRY");
  exactKeys(evidence, ["schema_version", "status", "tome_commit", "source_order_sha256", "counts", "records"], "SOURCE-EVIDENCE-POOL");
  exactKeys(bindings, ["schema_version", "status", "production_translation_commit", "source_order_before_target_binding_sha256", "fingerprinted_terminal_input_manifest", "binding_manifest_sha256", "counts", "records"], "IDENTITY-TARGET-BINDING-REGISTRY");
  exactKeys(candidates, ["schema_version", "status", "model_calls", "network_calls", "source_order_sha256", "counts", "items"], "FUTURE-MODEL-CANDIDATES");
  assert.equal(report.status, "PASS_ZERO_INFERENCE_FREEZE_GATES");
  assert.equal(experiment.status, "FROZEN_ZERO_INFERENCE_CANDIDATE_PACKAGE");
  assert.equal(report.model_calls, 0);
  assert.equal(report.network_calls, 0);
  assert.equal(experiment.model_calls, 0);
  assert.equal(experiment.network_calls, 0);
  assert.equal(candidates.model_calls, 0);
  assert.equal(candidates.network_calls, 0);

  assert.deepEqual(report.counts, {
    source_only_base_rows: 1396,
    v4_classified_rows: 700,
    v4_locator_accepted_rows: 663,
    v4_content_deduplicated_rows: 656,
    v4_selected_exclusions: 120,
    v4_complement_rows: 536,
    case_control_exclusions: 1,
    case_control_weak_signals_retained: 2,
    prior_context_input_rows: 535,
    prior_context_exclusions: 96,
    prior_context_weak_signals_retained: 3,
    final_items: 439,
    final_tasks: 34,
    profile_cells: {"narrative/dialogue": 425, dialogue: 233, narrative: 192, mechanics: 6, ui: 0, "runtime-log": 0, unknown: 8}
  });
  assert.deepEqual(report.shortfalls.ui, {required_novel_content: true, available_rows: 0, status: "SHORTFALL", padding_allowed: false, duplicate_leave_or_name_reuse_allowed: false, rule_relaxation_allowed: false});
  assert.deepEqual(report.shortfalls["runtime-log"], {required_novel_content: true, available_rows: 0, status: "SHORTFALL", padding_allowed: false, duplicate_leave_or_name_reuse_allowed: false, rule_relaxation_allowed: false});
  assert.ok(Object.values(report.gates).every(value => value === true));
  assert.equal(exclusion.v4_selected_exclusions.counts.identities, 120);
  assert.equal(exclusion.v4_selected_exclusions.counts.component_content_keys, 120);
  assert.equal(exclusion.v4_selected_exclusions.records.length, 120);
  assert.equal(new Set(exclusion.v4_selected_exclusions.records.map(record => record.identity_sha256)).size, 120);
  assert.equal(new Set(exclusion.v4_selected_exclusions.records.map(record => record.component_content_key)).size, 120);
  assert.equal(exclusion.four_route_subset_proof.source_count, 14);
  assert.equal(exclusion.four_route_subset_proof.all_sources_in_v4_exclusions, true);
  assert.equal(exclusion.four_route_subset_proof.records.length, 14);
  const excludedIdentityHashes = new Set(exclusion.v4_selected_exclusions.records.map(record => record.identity_sha256));
  const excludedContentKeys = new Set(exclusion.v4_selected_exclusions.records.map(record => record.component_content_key));
  for (const record of exclusion.four_route_subset_proof.records) {
    assert.ok(excludedIdentityHashes.has(record.matched_v4_identity_sha256));
    assert.ok(excludedContentKeys.has(record.matched_v4_component_content_key));
  }
  assert.equal(exclusion.case_control_overlay.counts.excluded, 1);
  assert.equal(exclusion.case_control_overlay.counts.weak_non_disqualifying, 2);
  assert.deepEqual(exclusion.case_control_overlay.weak_non_disqualifying_records.map(record => record.disposition).sort(), ["SHORT_COMPLETE_SOURCE_SIGNAL_NON_DISQUALIFYING", "TARGET_ONLY_ALIAS_NON_DISQUALIFYING"]);
  const overlayExcluded = exclusion.case_control_overlay.excluded_records[0];
  assert.equal(overlayExcluded.disposition, "COMPLETE_SOURCE_MIN_12_SOURCE_ORIENTED_PRIOR_EXPOSURE");
  assert.ok(overlayExcluded.unicode_code_points >= 12);
  assert.ok(overlayExcluded.strict_longer_structured_source_evidence.length > 0 || overlayExcluded.structured_exact_pair_evidence.length > 0 || overlayExcluded.source_only_exact_alias_evidence.length > 0 || overlayExcluded.confirmed_raw_source_evidence.length > 0);

  const frozenLeaves = [];
  const frozenArtifactRecords = [];
  for (const [logicalPath, expectedSha256] of priorContextArtifacts) {
    const bytes = fs.readFileSync(path.join(args.root, logicalPath));
    assert.equal(sha256Bytes(bytes), expectedSha256, `${logicalPath}: frozen prior-context hash`);
    frozenArtifactRecords.push({logical_path: logicalPath, sha256: expectedSha256, size_bytes: bytes.length});
    collectStringLeaves(JSON.parse(bytes.toString("utf8")), logicalPath, "", frozenLeaves);
  }
  const priorContext = exclusion.prior_model_facing_context_overlay;
  assert.deepEqual(priorContext.frozen_artifacts, frozenArtifactRecords);
  assert.equal(priorContext.scanned_string_leaves, frozenLeaves.length);
  assert.deepEqual(priorContext.counts, {
    input_rows: 535,
    excluded: 96,
    excluded_tasks: 29,
    excluded_profile_cells: {"narrative/dialogue": 91, dialogue: 83, narrative: 8, mechanics: 3, ui: 0, "runtime-log": 2, unknown: 0},
    weak_non_disqualifying: 3
  });
  assert.equal(priorContext.excluded_records.length, 96);
  assert.equal(priorContext.weak_non_disqualifying_records.length, 3);
  assert.equal(new Set(priorContext.excluded_records.map(record => record.identity_sha256)).size, 96);
  assert.equal(new Set(priorContext.excluded_records.map(record => record.task_identity_sha256)).size, 29);
  for (const record of priorContext.excluded_records) {
    assert.equal(sha256Bytes(record.source), record.source_sha256);
    assert.equal([...record.source].length, record.unicode_code_points);
    assert.ok(record.unicode_code_points >= 12);
    assert.deepEqual(record.matches, matchesForSource(record.source, frozenLeaves), `${record.identity_sha256}: excluded provenance completeness`);
    assert.ok(record.matches.length > 0);
  }
  for (const record of priorContext.weak_non_disqualifying_records) {
    assert.equal(sha256Bytes(record.source), record.source_sha256);
    assert.equal([...record.source].length, record.unicode_code_points);
    assert.ok(record.unicode_code_points < 12);
    assert.deepEqual(record.matches, matchesForSource(record.source, frozenLeaves), `${record.identity_sha256}: weak provenance completeness`);
    assert.ok(record.matches.length > 0);
  }

  assert.equal(evidence.records.length, 439);
  assert.equal(bindings.records.length, 439);
  assert.equal(candidates.items.length, 439);
  assert.equal(bindings.counts.tasks, 34);
  assert.equal(bindings.counts.terminal_inputs, 58);
  assert.equal(bindings.fingerprinted_terminal_input_manifest.count, 58);
  assert.equal(bindings.fingerprinted_terminal_input_manifest.bytes, 1664921);
  assert.equal(bindings.fingerprinted_terminal_input_manifest.manifest_sha256, "6c3ce0004e25991c7228a7341402ef7b639078ba2b1211d05d253cf03df83e85");
  assert.equal(evidence.source_order_sha256, bindings.source_order_before_target_binding_sha256);
  assert.equal(candidates.source_order_sha256, bindings.source_order_before_target_binding_sha256);
  assert.equal(experiment.source_only_order_sha256, bindings.source_order_before_target_binding_sha256);

  const evidenceById = new Map(evidence.records.map(record => [record.item_id, record]));
  const bindingById = new Map(bindings.records.map(record => [record.item_id, record]));
  const candidateById = new Map(candidates.items.map(record => [record.item_id, record]));
  assert.equal(evidenceById.size, 439);
  assert.equal(bindingById.size, 439);
  assert.equal(candidateById.size, 439);
  const identities = new Set();
  const contents = new Set();
  const recordsByTerminal = new Map();
  const priorContextExcludedIdentities = new Set(priorContext.excluded_records.map(record => record.identity_sha256));
  const priorContextWeakByIdentity = new Map(priorContext.weak_non_disqualifying_records.map(record => [record.identity_sha256, record]));
  const observedShortPriorContextIdentities = new Set();
  for (const record of bindings.records) {
    exactKeys(record, ["item_id", "task_id", "original_revision_key", "canonical_identity", "component", "category", "profile", "section", "source_tag", "source", "source_sha256", "target", "target_sha256", "component_content_key", "selection_provenance", "terminal_input", "record_sha256"], record.item_id);
    assert.match(record.item_id, /^C\d{3}$/u);
    const identity = `${record.task_id}\0${record.original_revision_key}`;
    const hashedIdentity = sha256Bytes(identity);
    assert.equal(identities.has(identity), false, `${record.item_id}: duplicate identity`);
    identities.add(identity);
    assert.equal(contents.has(record.component_content_key), false, `${record.item_id}: duplicate component/content`);
    contents.add(record.component_content_key);
    assert.equal(record.component_content_key, locatorContentKey(record.component, record.source));
    assert.equal(sha256Bytes(record.source), record.source_sha256);
    assert.equal(sha256Bytes(record.target), record.target_sha256);
    assert.equal(excludedIdentityHashes.has(sha256Bytes(identity)), false, `${record.item_id}: v4 identity overlap`);
    assert.equal(excludedContentKeys.has(record.component_content_key), false, `${record.item_id}: v4 content overlap`);
    assert.equal(priorContextExcludedIdentities.has(hashedIdentity), false, `${record.item_id}: prior-context excluded identity leaked to final queue`);
    const priorMatches = matchesForSource(record.source, frozenLeaves);
    if ([...record.source].length >= 12) assert.deepEqual(priorMatches, [], `${record.item_id}: qualifying prior model-facing source overlap`);
    else if (priorMatches.length > 0) {
      const weakRecord = priorContextWeakByIdentity.get(hashedIdentity);
      assert.ok(weakRecord, `${record.item_id}: unregistered short prior-context familiarity`);
      assert.deepEqual(weakRecord.matches, priorMatches);
      observedShortPriorContextIdentities.add(hashedIdentity);
    }
    const {record_sha256, ...core} = record;
    assert.equal(record_sha256, sha256Bytes(canonicalBytes(core)));
    assert.equal(record.selection_provenance.final_ordinal, Number(record.item_id.slice(1)));
    assert.equal(record.selection_provenance.source_order_sha256, bindings.source_order_before_target_binding_sha256);
    assert.equal(record.selection_provenance.fixed_context_identity_sha256, evidenceById.get(record.item_id).fixed_context_identity_sha256);
    const packet = evidenceById.get(record.item_id).packet;
    assert.equal(sha256Bytes(canonicalBytes(packet)), evidenceById.get(record.item_id).fixed_context_identity_sha256);
    assert.equal(packet.component, record.component);
    assert.equal(packet.source_sha256, record.source_sha256);
    assert.ok([1, 2].includes(packet.source_occurrences));
    assert.equal(packet.occurrences.length, packet.source_occurrences);
    let visibleTotal = 0;
    for (const occurrence of packet.occurrences) {
      assert.ok(occurrence.lines_before <= 12 && occurrence.lines_after <= 12);
      assert.ok(occurrence.before_utf8_bytes <= 2000 && occurrence.after_utf8_bytes <= 2000);
      assert.ok(occurrence.visible_context_utf8_bytes <= 8192);
      assert.equal(Buffer.byteLength(occurrence.visible_context, "utf8"), occurrence.visible_context_utf8_bytes);
      assert.equal(sha256Bytes(occurrence.visible_context), occurrence.visible_context_sha256);
      assert.ok(occurrence.visible_context.includes(occurrence.marker));
      visibleTotal += occurrence.visible_context_utf8_bytes;
    }
    assert.equal(visibleTotal, packet.combined_visible_context_utf8_bytes);
    assert.ok(visibleTotal <= 8192);
    assert.equal(Buffer.byteLength(JSON.stringify(packet), "utf8"), packet.supplemental_json_utf8_bytes);
    assert.ok(packet.supplemental_json_utf8_bytes <= 12288);
    const candidate = candidateById.get(record.item_id);
    assert.deepEqual(candidate, {item_id: record.item_id, component: record.component, category: record.category, profile: record.profile, source: record.source, target: record.target, fixed_context: packet});
    verifySourceArtifact(packet.source_binding, args);
    const terminalKey = record.terminal_input.logical_path;
    if (!recordsByTerminal.has(terminalKey)) {
      const bytes = fs.readFileSync(path.join(args.productionRepo, terminalKey));
      assert.equal(sha256Bytes(bytes), record.terminal_input.sha256);
      assert.equal(bytes.length, record.terminal_input.size_bytes);
      recordsByTerminal.set(terminalKey, JSON.parse(bytes.toString("utf8")));
    }
    const terminalItem = recordsByTerminal.get(terminalKey).payload.translation_snapshot.find(item => item.revision_key === record.original_revision_key);
    assert.ok(terminalItem, `${record.item_id}: terminal row missing`);
    assert.equal(terminalItem.source, record.source);
    assert.equal(terminalItem.target, record.target);
  }
  assert.deepEqual([...observedShortPriorContextIdentities].sort(), [...priorContextWeakByIdentity.keys()].sort(), "short familiarity registry must exactly cover retained matches");
  assert.equal(bindings.records.length + priorContext.excluded_records.length, 535, "prior-context overlay input partition");
  assert.equal(recordsByTerminal.size <= 58, true);
  assert.equal(new Set(bindings.fingerprinted_terminal_input_manifest.records.map(record => record.logical_path)).size, 58);

  const forbiddenKeys = new Set(["task_id", "revision_key", "original_revision_key", "canonical_identity", "canonical_revision_id", "canonical_revision_uid", "canonical_unit_id", "canonical_tu_uid", "membership_sha256", "terminal_input", "terminal_input_path", "logical_path", "provider", "model", "model_name", "truth_label", "label", "defect", "defect_atom", "adjudication", "audit_id"]);
  walk(candidates, (key, _value, pointer) => assert.equal(forbiddenKeys.has(key), false, `sanitized candidate forbidden key ${pointer}`));
  const candidateText = fs.readFileSync(path.join(here, "FUTURE-MODEL-CANDIDATES.json"), "utf8");
  assert.equal(/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/u.test(candidateText), false, "sanitized candidate absolute path");
  const internalStrings = new Set(bindings.records.flatMap(record => [record.task_id, record.original_revision_key, ...Object.values(record.canonical_identity), record.terminal_input.logical_path]));
  for (const value of collectStrings(candidates)) assert.equal(internalStrings.has(value), false, `sanitized candidate leaked internal identity ${value}`);

  const candidatePresentation = sha256Bytes(canonicalBytes(candidates));
  assert.equal(candidatePresentation, report.candidate_presentation_sha256);
  assert.equal(candidatePresentation, experiment.candidate_presentation_sha256);
  for (const [name, record] of Object.entries(report.generated_output_hashes)) assert.deepEqual(generatedRecord(path.join(here, name)), record, `${name}: report hash`);
  for (const [name, record] of Object.entries(experiment.generated_artifacts)) assert.deepEqual(generatedRecord(path.join(here, name)), record, `${name}: experiment hash`);
  assert.equal(generatedRecord(path.join(args.root, "evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua")).sha256, "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7");
  for (const name of GENERATED_NAMES) assert.equal(/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/u.test(fs.readFileSync(path.join(here, name), "utf8")), false, `${name}: absolute path leaked`);

  process.stdout.write(`${JSON.stringify({status: "PASS", deterministic_outputs: GENERATED_NAMES, counts: report.counts, candidate_presentation_sha256: candidatePresentation}, null, 2)}\n`);
} finally {
  const resolved = path.resolve(temporary);
  const prefix = `${path.resolve(os.tmpdir())}${path.sep}prospective-context-expansion-verify-`;
  if (!resolved.startsWith(prefix)) throw new Error("unsafe verifier temporary cleanup");
  fs.rmSync(resolved, {recursive: true, force: true});
}
