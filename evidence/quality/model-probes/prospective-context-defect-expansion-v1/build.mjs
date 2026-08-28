#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath, pathToFileURL} from "node:url";
import {
  buildFrozenPackage as rebuildV4,
  contentExposureKey,
  contextForOccurrence,
  locatorContentKey,
  normalizeSource,
  normalizedOccurrences,
  screenSourceOnlyRows,
  sha256Bytes
} from "../prospective-source-context-audit-v4/build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");
const v4Directory = path.resolve(here, "../prospective-source-context-audit-v4");

export const GENERATED_NAMES = Object.freeze([
  "SOURCE-EXCLUSION-REGISTRY.json",
  "SOURCE-EVIDENCE-POOL.json",
  "IDENTITY-TARGET-BINDING-REGISTRY.json",
  "FUTURE-MODEL-CANDIDATES.json",
  "BUILD-REPORT.json",
  "EXPERIMENT.json"
]);

const frozen = Object.freeze({
  production_commit: "1666481409f4c0d63d66e84659f6b6145d8d25d0",
  tome_commit: "624a67329fe2ad440c5b344785a9c73fcf22ae63",
  executor_fixture_sha256: "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7",
  terminal_manifest: {count: 58, bytes: 1664921, manifest_sha256: "6c3ce0004e25991c7228a7341402ef7b639078ba2b1211d05d253cf03df83e85"},
  inputs: {
    screen_contract: ["evidence/quality/model-probes/prospective-source-context-audit-v4/SCREEN-CONTRACT.json", "0932fb76492c609e1e4fe8a2e85b8cb8238d8342c5a0bfb3d6ce095c993a538b"],
    screen_frame: ["evidence/quality/model-probes/prospective-source-context-audit-v4/SOURCE-SCREEN-FRAME.json", "1c10e40a9e10d76a39eff6ad69e9c5a2c2d084f7cc4ae9543aa6af0893fd63cd"],
    source_packets: ["evidence/quality/model-probes/prospective-source-context-audit-v4/SOURCE-EVIDENCE-PACKETS.json", "4d2e21c2e144636d1752329263c44704909b39efeb4b837a7a41f648c9ee481d"],
    membership: ["evidence/quality/model-probes/prospective-residual-audit-v3/CANONICAL-MEMBERSHIP.json", "477c0e97f59e4f29159ed7baa16b7ef5ddb4165cbe5785ad15b667eadfda2049"],
    snapshot: ["evidence/quality/model-probes/paseo-provenance-snapshot-v1/SNAPSHOT.json", "b754183a9d1e0efa15cb1d3c16fa06a7f96f388e75707c7ba0e79f4a680f2eab"],
    prior_exposure: ["evidence/quality/model-probes/context-evidence-targeted-case-control-pilot-v1/PRIOR-EXPOSURE-REGISTRY.json", "950eb17f15faf555bc8bff53021ca4c5ec01af6474a82de98425cc75f668a866"],
    four_route_a: ["evidence/quality/model-probes/source-context-exploratory-four-route-v1/INPUT-A.json", "d8845716b86d2b0f7dca8ada1495f724e584e4c2adab97373b3a9dd975b5b4a2"],
    four_route_b: ["evidence/quality/model-probes/source-context-exploratory-four-route-v1/INPUT-B.json", "05893599fd1fad889d0cc36811565b2693933b09d069b9f59028143b7dd9a764"],
    context_queue_1: ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/CONTEXT-QUEUE-1.json", "735fe3465c60c1373ee491c80466f083958086711fa4186d7cee2111700cab60"],
    context_queue_2: ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/CONTEXT-QUEUE-2.json", "00aae61e04cbf7de07aaf618da566ca9aae2151619fafc127caf26372874e23d"],
    context_queue_3: ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/CONTEXT-QUEUE-3.json", "416da410ed6beddfc23c9b655accfbd77fd5f8506eb67c1899e31e6e45be5c1e"]
  },
  expected: {
    base_rows: 1396,
    v4_deduplicated: 656,
    v4_selected: 120,
    v4_complement: 536,
    case_control_excluded: 1,
    case_control_weak_retained: 2,
    prior_context_input_rows: 535,
    prior_context_excluded: 96,
    prior_context_weak_retained: 3,
    final_rows: 439,
    final_tasks: 34,
    profile_cells: {"narrative/dialogue": 425, dialogue: 233, narrative: 192, mechanics: 6, ui: 0, "runtime-log": 0, unknown: 8}
  }
});

const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const canonicalBytes = value => Buffer.from(JSON.stringify(value), "utf8");
const identityKey = (taskId, revisionKey) => `${taskId}\0${revisionKey}`;
const identityHash = (taskId, revisionKey) => sha256Bytes(identityKey(taskId, revisionKey));
const fileRecord = bytes => ({sha256: sha256Bytes(bytes), size_bytes: bytes.length});

function parseArgs(argv) {
  const args = {root: defaultRoot, out: here};
  const allowed = new Set(["--root", "--out", "--production-repo", "--engine-repo", "--dlc-root"]);
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!allowed.has(flag) || !value) throw new Error("usage: node build.mjs --production-repo REPO --engine-repo REPO --dlc-root ROOT [--root REPO] [--out DIR]");
    args[flag.slice(2).replace(/-([a-z])/gu, (_match, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  for (const key of ["productionRepo", "engineRepo", "dlcRoot"]) if (!args[key]) throw new Error(`--${key.replace(/[A-Z]/gu, letter => `-${letter.toLowerCase()}`)} is required`);
  return args;
}

function assertSafeRelative(value, label) {
  if (typeof value !== "string" || !value || value.includes("\0") || path.posix.isAbsolute(value) || path.posix.normalize(value) !== value || value === ".." || value.startsWith("../")) {
    throw new Error(`${label}: unsafe relative path`);
  }
}

function assertInside(root, candidate, label) {
  const relative = path.relative(root, candidate);
  if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) throw new Error(`${label}: escaped root`);
}

function assertNoAbsolutePaths(bytes, label) {
  if (/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/u.test(bytes.toString("utf8"))) throw new Error(`${label}: absolute path leaked`);
}

function readFrozen(root, name) {
  const [logicalPath, expectedSha256] = frozen.inputs[name];
  const bytes = fs.readFileSync(path.join(root, logicalPath));
  if (sha256Bytes(bytes) !== expectedSha256) throw new Error(`${logicalPath}: frozen hash drift`);
  return {logical_path: logicalPath, sha256: expectedSha256, size_bytes: bytes.length, value: JSON.parse(bytes.toString("utf8"))};
}

function gitOutput(repo, args, encoding = "utf8") {
  return execFileSync("git", ["-C", repo, ...args], {encoding, maxBuffer: 128 * 1024 * 1024});
}

function decodeUtf8(buffer, label) {
  try {
    return new TextDecoder("utf-8", {fatal: true}).decode(buffer);
  } catch (error) {
    throw new Error(`${label}: invalid UTF-8: ${error.message}`);
  }
}

export function makeLocator(args, bindings) {
  const cache = new Map();
  return row => {
    const cacheKey = `${row.component}\0${row.section}\0${row.source}`;
    if (cache.has(cacheKey)) return cache.get(cacheKey);
    const binding = bindings[row.component];
    let result;
    try {
      if (!binding || !row.section.startsWith(binding.section_prefix)) throw new Error("source binding unavailable or section prefix mismatch");
      const sectionRelative = row.section.slice(binding.section_prefix.length);
      assertSafeRelative(sectionRelative, "source section");
      let bytes;
      let sourceBinding;
      if (binding.read_mode === "git_commit_blob") {
        const relativePath = path.posix.join(binding.repository_prefix, sectionRelative);
        assertSafeRelative(relativePath, "Tome source path");
        bytes = gitOutput(args.engineRepo, ["show", `${binding.commit}:${relativePath}`], null);
        sourceBinding = {kind: "git_commit_blob", component: row.component, repository_alias: binding.repository_alias, commit: binding.commit, relative_path: relativePath, source_artifact_sha256: sha256Bytes(bytes), source_artifact_size_bytes: bytes.length};
      } else if (binding.read_mode === "working_tree_file_with_required_sha256") {
        const registeredRoot = fs.realpathSync(path.resolve(args.dlcRoot, binding.dlc_subdirectory));
        const candidate = fs.realpathSync(path.resolve(registeredRoot, sectionRelative));
        assertInside(registeredRoot, candidate, "DLC source");
        if (!fs.statSync(candidate).isFile()) throw new Error("DLC source is not a file");
        bytes = fs.readFileSync(candidate);
        sourceBinding = {kind: "dlc_file_sha256", component: row.component, repository_alias: binding.repository_alias, commit: null, relative_path: sectionRelative.split(path.sep).join("/"), source_artifact_sha256: sha256Bytes(bytes), source_artifact_size_bytes: bytes.length};
      } else {
        throw new Error("unsupported source read mode");
      }
      const fileText = decodeUtf8(bytes, sourceBinding.relative_path);
      const occurrences = normalizedOccurrences(fileText, row.source);
      result = {status: occurrences.length === 0 ? "SOURCE_NOT_FOUND" : occurrences.length <= 2 ? "LOCATED_ACCEPTED" : "LOCATED_TOO_MANY", fileText, source_binding: sourceBinding, source_occurrences: occurrences.length, occurrences};
    } catch (error) {
      result = {status: "SOURCE_BINDING_FAILED", error: error.message, source_occurrences: 0, occurrences: []};
    }
    cache.set(cacheKey, result);
    return result;
  };
}

export function packetFor(row, sideByteCap = 2000) {
  const occurrences = row.locator.occurrences.map((occurrence, index) => contextForOccurrence(row.locator.fileText, occurrence, index + 1, sideByteCap));
  const packet = {
    component: row.component,
    source_sha256: row.source_sha256,
    source_binding: row.locator.source_binding,
    source_occurrences: occurrences.length,
    occurrences
  };
  const visibleTotal = occurrences.reduce((sum, occurrence) => sum + occurrence.visible_context_utf8_bytes, 0);
  const base = {...packet, combined_visible_context_utf8_bytes: visibleTotal};
  let measured = 0;
  for (let attempt = 0; attempt < 8; attempt += 1) {
    const next = Buffer.byteLength(JSON.stringify({...base, supplemental_json_utf8_bytes: measured}), "utf8");
    if (next === measured) break;
    measured = next;
  }
  const finalPacket = {...base, supplemental_json_utf8_bytes: measured};
  if (Buffer.byteLength(JSON.stringify(finalPacket), "utf8") !== measured) throw new Error("source packet byte accounting failed to converge");
  if (visibleTotal > 8192 || measured > 12288) {
    if (sideByteCap === 0) throw new Error("source packet cap cannot be met");
    return packetFor(row, Math.max(0, sideByteCap - 128));
  }
  return finalPacket;
}

function terminalDispatches(task) {
  let dispatches = task.dispatches.filter(dispatch => dispatch.role === "REVIEWER" && dispatch.purpose === "translation_contextual_v1" && dispatch.input_path);
  const withCycle = dispatches.filter(dispatch => Number.isFinite(dispatch.cycle));
  if (withCycle.length) {
    const terminalCycle = Math.max(...withCycle.map(dispatch => dispatch.cycle));
    dispatches = withCycle.filter(dispatch => dispatch.cycle === terminalCycle);
  } else if (dispatches.length) dispatches = [dispatches.at(-1)];
  return dispatches;
}

function loadTargetInputs(productionRepo, membership, snapshot) {
  const tasks = new Map(snapshot.tasks.map(task => [task.task_id, task]));
  const taskIds = [...new Set(membership.items.map(item => item.task_id))].sort();
  const expectedByPath = new Map();
  for (const taskId of taskIds) {
    const task = tasks.get(taskId);
    if (!task) throw new Error(`${taskId}: provenance task missing`);
    for (const dispatch of terminalDispatches(task)) {
      assertSafeRelative(dispatch.input_path, "terminal input");
      const record = {task_id: taskId, logical_path: dispatch.input_path, sha256: dispatch.input_fingerprint?.sha256, size_bytes: dispatch.input_fingerprint?.size_bytes};
      if (!/^[0-9a-f]{64}$/u.test(record.sha256 ?? "") || !Number.isInteger(record.size_bytes)) throw new Error(`${taskId}: terminal fingerprint missing`);
      const previous = expectedByPath.get(record.logical_path);
      if (previous && JSON.stringify(previous) !== JSON.stringify(record)) throw new Error(`${record.logical_path}: conflicting terminal record`);
      expectedByPath.set(record.logical_path, record);
    }
  }
  const records = [...expectedByPath.values()].sort((a, b) => a.logical_path.localeCompare(b.logical_path));
  const index = new Map();
  for (const record of records) {
    const bytes = fs.readFileSync(path.join(productionRepo, record.logical_path));
    if (bytes.length !== record.size_bytes || sha256Bytes(bytes) !== record.sha256) throw new Error(`${record.logical_path}: terminal fingerprint drift`);
    const envelope = JSON.parse(bytes.toString("utf8"));
    if (!Array.isArray(envelope.payload?.translation_snapshot)) throw new Error(`${record.logical_path}: translation_snapshot missing`);
    for (const item of envelope.payload.translation_snapshot) {
      const keys = Object.keys(item).sort();
      if (JSON.stringify(keys) !== JSON.stringify(["revision_key", "source", "target"])) throw new Error(`${record.logical_path}: terminal item schema drift`);
      const key = identityKey(record.task_id, item.revision_key);
      if (index.has(key)) throw new Error(`${key}: duplicate terminal identity`);
      index.set(key, {...item, terminal_input: {logical_path: record.logical_path, sha256: record.sha256, size_bytes: record.size_bytes}});
    }
  }
  const manifestCanonical = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  const manifest = {records: records.map(({logical_path, sha256, size_bytes}) => ({logical_path, sha256, size_bytes})), count: records.length, bytes: records.reduce((sum, record) => sum + record.size_bytes, 0), manifest_sha256: sha256Bytes(manifestCanonical)};
  for (const field of ["count", "bytes", "manifest_sha256"]) if (manifest[field] !== frozen.terminal_manifest[field]) throw new Error(`terminal manifest ${field} drift`);
  return {index, manifest};
}

function sourceSpecificExposure(record) {
  const structuredLonger = record.longer_outbound_string_leaf_matches.filter(match => match.method === "source_literal_in_longer_outbound_string_leaf");
  const structuredExact = record.structured_exact_pair_matches ?? [];
  const raw = record.raw_literal_matches.filter(match => match.field === "source" && match.classification === "CONFIRMED_TRACKED_INPUT");
  const sourceOnlyAliases = record.explicit_input_alias_matches.filter(match => match.method === "source_only_exact_alias");
  const targetOnlyAliases = record.explicit_input_alias_matches.filter(match => match.method === "target_only_exact_alias");
  return {structuredLonger, structuredExact, sourceOnlyAliases, raw, targetOnlyAliases};
}

export function applySourceExposureOverlay(rows, priorRegistry) {
  const byIdentity = new Map();
  for (const record of priorRegistry.exposure_pairs) {
    const signal = sourceSpecificExposure(record);
    for (const membership of record.memberships) byIdentity.set(identityKey(membership.task_id, membership.original_revision_key), {record, signal});
  }
  const excluded = [];
  const weak = [];
  const retained = [];
  for (const row of rows) {
    const found = byIdentity.get(identityKey(row.task_id, row.original_revision_key));
    if (!found || found.record.source_sha256 !== row.source_sha256) {
      retained.push(row);
      continue;
    }
    const characters = [...row.source].length;
    const sourceSignals = [found.signal.structuredLonger, found.signal.structuredExact, found.signal.sourceOnlyAliases, found.signal.raw];
    const qualifying = characters >= 12 && sourceSignals.some(matches => matches.length > 0);
    if (qualifying) excluded.push({row, found, characters, reason: "COMPLETE_SOURCE_MIN_12_SOURCE_ORIENTED_PRIOR_EXPOSURE"});
    else {
      retained.push(row);
      const hasShortSourceSignal = characters < 12 && sourceSignals.some(matches => matches.length > 0);
      if (hasShortSourceSignal || found.signal.targetOnlyAliases.length > 0) {
        weak.push({row, found, characters, reason: hasShortSourceSignal ? "SHORT_COMPLETE_SOURCE_SIGNAL_NON_DISQUALIFYING" : "TARGET_ONLY_ALIAS_NON_DISQUALIFYING"});
      }
    }
  }
  return {retained, excluded, weak};
}

const escapePointerToken = value => value.replace(/~/gu, "~0").replace(/\//gu, "~1");

export function collectJsonStringLeaves(value, pointer = "", output = []) {
  if (typeof value === "string") output.push({json_pointer: pointer, value});
  else if (Array.isArray(value)) value.forEach((entry, index) => collectJsonStringLeaves(entry, `${pointer}/${index}`, output));
  else if (value && typeof value === "object") {
    for (const [key, entry] of Object.entries(value)) collectJsonStringLeaves(entry, `${pointer}/${escapePointerToken(key)}`, output);
  }
  return output;
}

export function applyPriorModelFacingContextOverlay(rows, artifacts) {
  const leaves = artifacts.flatMap(artifact => collectJsonStringLeaves(artifact.value).map(leaf => ({logical_path: artifact.logical_path, ...leaf})));
  const excluded = [];
  const weak = [];
  const retained = [];
  for (const row of rows) {
    const matches = [];
    for (const leaf of leaves) {
      if (leaf.value === row.source) matches.push({logical_path: leaf.logical_path, json_pointer: leaf.json_pointer, method: "exact_string_leaf"});
      else if (leaf.value.includes(row.source)) matches.push({logical_path: leaf.logical_path, json_pointer: leaf.json_pointer, method: "strict_longer_string_leaf"});
    }
    const characters = [...row.source].length;
    const entry = {row, characters, matches};
    if (matches.length > 0 && characters >= 12) excluded.push({...entry, reason: "COMPLETE_SOURCE_MIN_12_PRIOR_MODEL_FACING_CONTEXT"});
    else {
      retained.push(row);
      if (matches.length > 0) weak.push({...entry, reason: "SHORT_COMPLETE_SOURCE_PRIOR_CONTEXT_NON_DISQUALIFYING"});
    }
  }
  return {retained, excluded, weak, string_leaf_count: leaves.length};
}

function profileCounts(rows) {
  return {
    "narrative/dialogue": rows.filter(row => row.profile === "narrative" || row.profile === "dialogue").length,
    dialogue: rows.filter(row => row.profile === "dialogue").length,
    narrative: rows.filter(row => row.profile === "narrative").length,
    mechanics: rows.filter(row => row.profile === "mechanics").length,
    ui: rows.filter(row => row.profile === "ui").length,
    "runtime-log": rows.filter(row => row.profile === "runtime-log").length,
    unknown: rows.filter(row => row.profile === "unknown").length
  };
}

function provenanceEvidence(matches) {
  return matches.map(match => ({method: match.method ?? null, field: match.field ?? null, classification: match.classification ?? null, logical_path: match.logical_path, json_pointer: match.json_pointer ?? null}));
}

function buildExclusionRegistry({selectedRows, fourRouteA, fourRouteB, overlay, priorExposureRecord, priorContextOverlay, priorContextArtifacts}) {
  const selectedIdentity = new Map(selectedRows.map(row => [identityKey(row.task_id, row.original_revision_key), row]));
  const selectedContent = new Map(selectedRows.map(row => [locatorContentKey(row.component, row.source), row]));
  if (selectedIdentity.size !== 120 || selectedContent.size !== 120) throw new Error("v4 selected exclusion cardinality drift");
  if (fourRouteA.items.length !== 14 || fourRouteB.items.length !== 14) throw new Error("four-route input count drift");
  for (let index = 0; index < 14; index += 1) if (fourRouteA.items[index].source !== fourRouteB.items[index].source) throw new Error(`four-route A/B source mismatch at ${index}`);
  const subset = fourRouteA.items.map((item, index) => {
    const matches = selectedRows.filter(row => normalizeSource(row.source) === normalizeSource(item.source));
    if (matches.length !== 1) throw new Error(`four-route source ${index + 1}: expected exactly one v4 exclusion`);
    const row = matches[0];
    return {four_route_item_ordinal: index + 1, source_sha256: sha256Bytes(item.source), normalized_source_sha256: contentExposureKey(item.source), matched_v4_identity_sha256: identityHash(row.task_id, row.original_revision_key), matched_v4_component_content_key: locatorContentKey(row.component, row.source)};
  });
  const overlayRecord = entry => ({
    identity_sha256: identityHash(entry.row.task_id, entry.row.original_revision_key),
    source_sha256: entry.row.source_sha256,
    unicode_code_points: entry.characters,
    disposition: entry.reason,
    strict_longer_structured_source_evidence: provenanceEvidence(entry.found.signal.structuredLonger),
    structured_exact_pair_evidence: provenanceEvidence(entry.found.signal.structuredExact),
    source_only_exact_alias_evidence: provenanceEvidence(entry.found.signal.sourceOnlyAliases),
    confirmed_raw_source_evidence: provenanceEvidence(entry.found.signal.raw),
    target_only_alias_evidence: provenanceEvidence(entry.found.signal.targetOnlyAliases)
  });
  const priorContextRecord = entry => ({
    identity_sha256: identityHash(entry.row.task_id, entry.row.original_revision_key),
    task_identity_sha256: sha256Bytes(entry.row.task_id),
    source: entry.row.source,
    source_sha256: entry.row.source_sha256,
    unicode_code_points: entry.characters,
    profile: entry.row.profile,
    disposition: entry.reason,
    matches: entry.matches
  });
  return {
    schema_version: "prospective-context-defect-source-exclusion-registry-v1",
    status: "FROZEN_SOURCE_EXCLUSIONS",
    source_only: true,
    normalization: "v4 normalize_source: whitespace and literal escaped n/r/t collapse to one ASCII space; trim edges",
    v4_selected_exclusions: {
      identity_key_rule: "sha256(task_id + NUL + original_revision_key)",
      component_content_key_rule: "sha256(component + NUL + normalize_source(source))",
      counts: {identities: selectedIdentity.size, component_content_keys: selectedContent.size},
      records: selectedRows.map(row => ({identity_sha256: identityHash(row.task_id, row.original_revision_key), component_content_key: locatorContentKey(row.component, row.source), source_sha256: row.source_sha256}))
    },
    four_route_subset_proof: {input_a_sha256: frozen.inputs.four_route_a[1], input_b_sha256: frozen.inputs.four_route_b[1], source_count: subset.length, all_sources_in_v4_exclusions: true, records: subset},
    case_control_overlay: {
      registry_sha256: priorExposureRecord.sha256,
      rule: "Exclude a complete source of at least 12 Unicode code points with strict-longer structured source, structured exact pair, source-only exact alias, or CONFIRMED_TRACKED_INPUT RAW source evidence; retain every shorter signal and target-only alias as weak evidence.",
      counts: {excluded: overlay.excluded.length, weak_non_disqualifying: overlay.weak.length},
      excluded_records: overlay.excluded.map(overlayRecord),
      weak_non_disqualifying_records: overlay.weak.map(overlayRecord)
    },
    prior_model_facing_context_overlay: {
      rule: "Scan every JSON string leaf; exclude complete sources of at least 12 Unicode code points on exact equality or literal containment in a strictly longer leaf. Current targets do not participate.",
      frozen_artifacts: priorContextArtifacts.map(record => ({logical_path: record.logical_path, sha256: record.sha256, size_bytes: record.size_bytes})),
      scanned_string_leaves: priorContextOverlay.string_leaf_count,
      counts: {
        input_rows: priorContextOverlay.retained.length + priorContextOverlay.excluded.length,
        excluded: priorContextOverlay.excluded.length,
        excluded_tasks: new Set(priorContextOverlay.excluded.map(entry => entry.row.task_id)).size,
        excluded_profile_cells: profileCounts(priorContextOverlay.excluded.map(entry => entry.row)),
        weak_non_disqualifying: priorContextOverlay.weak.length
      },
      excluded_records: priorContextOverlay.excluded.map(priorContextRecord),
      weak_non_disqualifying_records: priorContextOverlay.weak.map(priorContextRecord)
    }
  };
}

function writeOutput(out, name, value) {
  const bytes = jsonBytes(value);
  assertNoAbsolutePaths(bytes, name);
  fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, name), bytes);
  return fileRecord(bytes);
}

export function buildPackage(args) {
  const root = path.resolve(args.root ?? defaultRoot);
  const out = path.resolve(args.out ?? here);
  const inputs = Object.fromEntries(Object.keys(frozen.inputs).map(name => [name, readFrozen(root, name)]));
  const screenContract = inputs.screen_contract.value;
  if (screenContract.production_translation_commit !== frozen.production_commit || screenContract.source_bindings.tome.commit !== frozen.tome_commit) throw new Error("v4 production/source commit contract drift");
  if (gitOutput(args.engineRepo, ["cat-file", "-t", `${frozen.tome_commit}^{commit}`]).trim() !== "commit") throw new Error("fixed Tome commit unavailable");
  if (gitOutput(args.productionRepo, ["cat-file", "-t", `${frozen.production_commit}^{commit}`]).trim() !== "commit") throw new Error("production commit object unavailable");

  const v4Temporary = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-context-v4-rebuild-"));
  let rebuilt;
  try {
    rebuilt = rebuildV4({...args, root, out: v4Temporary});
    for (const name of ["SOURCE-ONLY-BASE-FRAME.json", "SOURCE-SCREEN-FRAME.json", "SOURCE-EVIDENCE-PACKETS.json", "SOURCE-EXPOSURE-REGISTRY.json", "BUILD-REPORT.json"]) {
      if (!fs.readFileSync(path.join(v4Temporary, name)).equals(fs.readFileSync(path.join(v4Directory, name)))) throw new Error(`${name}: v4 deterministic rebuild drift`);
    }
  } finally {
    const resolved = path.resolve(v4Temporary);
    if (!resolved.startsWith(`${path.resolve(os.tmpdir())}${path.sep}prospective-context-v4-rebuild-`)) throw new Error("unsafe temporary directory cleanup");
    fs.rmSync(resolved, {recursive: true, force: true});
  }

  const baseRows = rebuilt.base.items;
  const exposure = {revisionSet: new Set(rebuilt.registry.exposed_revision_keys.map(record => record.revision_key)), contentSet: new Set(rebuilt.registry.exposed_content_keys.map(record => record.content_key))};
  const screen = screenSourceOnlyRows({baseRows, exposure, locate: makeLocator(args, screenContract.source_bindings), contract: screenContract});
  const selectedRows = rebuilt.frame.categories.flatMap(category => category.items).map(item => {
    const row = screen.deduplicated.find(candidate => identityKey(candidate.task_id, candidate.original_revision_key) === identityKey(item.task_id, item.original_revision_key));
    if (!row) throw new Error("tracked v4 selection not found in reconstructed screen");
    return row;
  });
  const selectedIdentities = new Set(selectedRows.map(row => identityKey(row.task_id, row.original_revision_key)));
  const selectedContent = new Set(selectedRows.map(row => locatorContentKey(row.component, row.source)));
  const complement = screen.deduplicated.filter(row => !selectedIdentities.has(identityKey(row.task_id, row.original_revision_key)) && !selectedContent.has(locatorContentKey(row.component, row.source)));
  const sourceOrderSha256 = sha256Bytes(canonicalBytes(complement.map(row => ({task_id: row.task_id, original_revision_key: row.original_revision_key, component: row.component, category: row.category, profile: row.profile, source_sha256: row.source_sha256, source_evidence_sha256: sha256Bytes(canonicalBytes(packetFor(row)))}))));
  const overlay = applySourceExposureOverlay(complement, inputs.prior_exposure.value);
  const priorContextArtifacts = [inputs.four_route_b, inputs.context_queue_1, inputs.context_queue_2, inputs.context_queue_3];
  const priorContextOverlay = applyPriorModelFacingContextOverlay(overlay.retained, priorContextArtifacts);
  const finalRows = priorContextOverlay.retained;
  const finalSourceOrderSha256 = sha256Bytes(canonicalBytes(finalRows.map(row => ({task_id: row.task_id, original_revision_key: row.original_revision_key, component: row.component, category: row.category, profile: row.profile, source_sha256: row.source_sha256, source_evidence_sha256: sha256Bytes(canonicalBytes(packetFor(row)))}))));

  const expected = frozen.expected;
  const counts = profileCounts(finalRows);
  const measuredGate = {base_rows: baseRows.length, v4_deduplicated: screen.deduplicated.length, v4_selected: selectedRows.length, v4_complement: complement.length, case_control_excluded: overlay.excluded.length, case_control_weak_retained: overlay.weak.length, prior_context_input_rows: overlay.retained.length, prior_context_excluded: priorContextOverlay.excluded.length, prior_context_weak_retained: priorContextOverlay.weak.length, final_rows: finalRows.length, final_tasks: new Set(finalRows.map(row => row.task_id)).size, profile_cells: counts};
  if (JSON.stringify(measuredGate) !== JSON.stringify(expected)) throw new Error(`corrected residual count/profile gate failed: ${JSON.stringify(measuredGate)}`);

  const exclusionRegistry = buildExclusionRegistry({selectedRows, fourRouteA: inputs.four_route_a.value, fourRouteB: inputs.four_route_b.value, overlay, priorExposureRecord: inputs.prior_exposure, priorContextOverlay, priorContextArtifacts});
  const membership = inputs.membership.value;
  const snapshot = inputs.snapshot.value;
  if (membership.production_translation_commit !== frozen.production_commit || snapshot.source_repo_head !== frozen.production_commit) throw new Error("production commit contract drift");
  const membershipIndex = new Map();
  for (const item of membership.items) {
    const key = identityKey(item.task_id, item.original_revision_key);
    if (membershipIndex.has(key)) throw new Error(`${key}: duplicate canonical membership`);
    membershipIndex.set(key, item);
  }
  const terminal = loadTargetInputs(args.productionRepo, membership, snapshot);

  const evidenceRecords = [];
  const bindingRecords = [];
  const modelItems = [];
  for (let index = 0; index < finalRows.length; index += 1) {
    const row = finalRows[index];
    const itemId = `C${String(index + 1).padStart(3, "0")}`;
    const key = identityKey(row.task_id, row.original_revision_key);
    const member = membershipIndex.get(key);
    const target = terminal.index.get(key);
    if (!member || !target) throw new Error(`${key}: target binding missing`);
    if (target.source !== row.source || member.source_sha256 !== row.source_sha256 || sha256Bytes(target.source) !== row.source_sha256) throw new Error(`${key}: source binding mismatch`);
    const targetSha256 = sha256Bytes(target.target);
    if (!target.target || targetSha256 !== member.target_sha256) throw new Error(`${key}: target binding hash mismatch`);
    for (const field of ["component", "section", "source_tag", "profile"]) if ((member[field] ?? null) !== (row[field] ?? null)) throw new Error(`${key}: membership ${field} mismatch`);
    const packet = packetFor(row);
    const packetSha256 = sha256Bytes(canonicalBytes(packet));
    evidenceRecords.push({item_id: itemId, fixed_context_identity_sha256: packetSha256, packet});
    const recordCore = {
      item_id: itemId,
      task_id: row.task_id,
      original_revision_key: row.original_revision_key,
      canonical_identity: {revision_id: member.canonical_revision_id, revision_uid: member.canonical_revision_uid, unit_id: member.canonical_unit_id, tu_uid: member.canonical_tu_uid, membership_sha256: member.membership_sha256},
      component: row.component,
      category: row.category,
      profile: row.profile,
      section: row.section,
      source_tag: row.source_tag,
      source: row.source,
      source_sha256: row.source_sha256,
      target: target.target,
      target_sha256: targetSha256,
      component_content_key: locatorContentKey(row.component, row.source),
      selection_provenance: {v4_complete_residual_ordinal: complement.indexOf(row) + 1, final_ordinal: index + 1, source_order_sha256: finalSourceOrderSha256, fixed_context_identity_sha256: packetSha256},
      terminal_input: target.terminal_input
    };
    bindingRecords.push({...recordCore, record_sha256: sha256Bytes(canonicalBytes(recordCore))});
    modelItems.push({item_id: itemId, component: row.component, category: row.category, profile: row.profile, source: row.source, target: target.target, fixed_context: packet});
  }

  const sourceEvidencePool = {schema_version: "prospective-context-defect-source-evidence-pool-v1", status: "FROZEN_FIXED_PUBLIC_SOURCE_EVIDENCE", tome_commit: frozen.tome_commit, source_order_sha256: finalSourceOrderSha256, counts: {items: evidenceRecords.length, source_artifacts: new Set(evidenceRecords.map(record => `${record.packet.source_binding.component}\0${record.packet.source_binding.relative_path}`)).size}, records: evidenceRecords};
  const bindingCanonical = bindingRecords.map(record => `${record.item_id}\0${record.record_sha256}\n`).join("");
  const bindingRegistry = {schema_version: "prospective-context-defect-identity-target-binding-registry-v1", status: "FROZEN_INTERNAL_BINDINGS", production_translation_commit: frozen.production_commit, source_order_before_target_binding_sha256: finalSourceOrderSha256, fingerprinted_terminal_input_manifest: terminal.manifest, binding_manifest_sha256: sha256Bytes(bindingCanonical), counts: {items: bindingRecords.length, tasks: new Set(bindingRecords.map(record => record.task_id)).size, terminal_inputs: terminal.manifest.count}, records: bindingRecords};
  const candidatePayload = {schema_version: "prospective-context-defect-future-model-candidates-v1", status: "FROZEN_NO_INFERENCE", model_calls: 0, network_calls: 0, source_order_sha256: finalSourceOrderSha256, counts: {items: modelItems.length, profile_cells: counts, shortfalls: {ui: {requested_cell: "ui", available: 0, disposition: "SHORTFALL_NO_PADDING_OR_RULE_RELAXATION"}, "runtime-log": {requested_cell: "runtime-log", available: 0, disposition: "SHORTFALL_NO_PADDING_OR_RULE_RELAXATION"}}}, items: modelItems};
  const candidatePresentationSha256 = sha256Bytes(canonicalBytes(candidatePayload));

  const outputHashes = {};
  outputHashes["SOURCE-EXCLUSION-REGISTRY.json"] = writeOutput(out, "SOURCE-EXCLUSION-REGISTRY.json", exclusionRegistry);
  outputHashes["SOURCE-EVIDENCE-POOL.json"] = writeOutput(out, "SOURCE-EVIDENCE-POOL.json", sourceEvidencePool);
  outputHashes["IDENTITY-TARGET-BINDING-REGISTRY.json"] = writeOutput(out, "IDENTITY-TARGET-BINDING-REGISTRY.json", bindingRegistry);
  outputHashes["FUTURE-MODEL-CANDIDATES.json"] = writeOutput(out, "FUTURE-MODEL-CANDIDATES.json", candidatePayload);
  const report = {
    schema_version: "prospective-context-defect-expansion-build-report-v1",
    status: "PASS_ZERO_INFERENCE_FREEZE_GATES",
    model_calls: 0,
    network_calls: 0,
    production_translation_commit: frozen.production_commit,
    source_only_order_before_target_binding_sha256: finalSourceOrderSha256,
    v4_complement_order_sha256: sourceOrderSha256,
    candidate_presentation_sha256: candidatePresentationSha256,
    counts: {source_only_base_rows: baseRows.length, v4_classified_rows: screen.classified.length, v4_locator_accepted_rows: screen.locatorAccepted.length, v4_content_deduplicated_rows: screen.deduplicated.length, v4_selected_exclusions: selectedRows.length, v4_complement_rows: complement.length, case_control_exclusions: overlay.excluded.length, case_control_weak_signals_retained: overlay.weak.length, prior_context_input_rows: overlay.retained.length, prior_context_exclusions: priorContextOverlay.excluded.length, prior_context_weak_signals_retained: priorContextOverlay.weak.length, final_items: finalRows.length, final_tasks: new Set(finalRows.map(row => row.task_id)).size, profile_cells: counts},
    shortfalls: {
      ui: {required_novel_content: true, available_rows: counts.ui, status: "SHORTFALL", padding_allowed: false, duplicate_leave_or_name_reuse_allowed: false, rule_relaxation_allowed: false},
      "runtime-log": {required_novel_content: true, available_rows: counts["runtime-log"], status: "SHORTFALL", padding_allowed: false, duplicate_leave_or_name_reuse_allowed: false, rule_relaxation_allowed: false}
    },
    frozen_input_hashes: Object.fromEntries(Object.entries(inputs).map(([name, record]) => [name, record.sha256])),
    generated_output_hashes: outputHashes,
    gates: {v4_byte_rebuild_exact: true, base_rows_1396: true, v4_rules_reapplied: true, v4_120_identity_and_content_exclusions: true, four_route_14_subset_of_120: true, case_control_one_excluded: true, case_control_two_weak_signals_retained: true, prior_context_four_artifacts_hash_pinned: true, prior_context_96_excluded_with_provenance: true, prior_context_three_short_weak_signals_retained: true, residual_439_rows_34_tasks: true, corrected_profile_cells_exact: true, ui_zero_machine_readable: true, runtime_log_zero_machine_readable: true, target_binding_after_source_order_freeze: true, terminal_manifest_58_exact: true, production_commit_contract_exact: true, fixed_tome_commit_exact: true, source_packet_caps_preserved: true, model_calls_zero: true, network_calls_zero: true}
  };
  outputHashes["BUILD-REPORT.json"] = writeOutput(out, "BUILD-REPORT.json", report);
  const experiment = {
    schema_version: "prospective-context-defect-expansion-experiment-v1",
    experiment_id: "prospective-context-defect-expansion-v1",
    status: "FROZEN_ZERO_INFERENCE_CANDIDATE_PACKAGE",
    date_frozen: "2026-08-28",
    production_translation_commit: frozen.production_commit,
    tome_source_commit: frozen.tome_commit,
    model_calls: 0,
    network_calls: 0,
    methodology: "Complete residual complement of the frozen v4 source-only screen, followed by the source-oriented case-control overlay and a hash-pinned all-string-leaf scan of four actual prior model-facing context inputs; no sampling, padding, target-informed eligibility, or truth-informed ranking.",
    counts: {case_control_input_rows: complement.length, case_control_excluded: overlay.excluded.length, prior_context_input_rows: overlay.retained.length, prior_context_excluded: priorContextOverlay.excluded.length, final_items: finalRows.length, final_tasks: new Set(finalRows.map(row => row.task_id)).size, profile_cells: counts},
    shortfall_cells: ["ui", "runtime-log"],
    frozen_input_hashes: Object.fromEntries(Object.entries(inputs).map(([name, record]) => [name, record.sha256])),
    source_only_order_sha256: finalSourceOrderSha256,
    candidate_presentation_sha256: candidatePresentationSha256,
    generated_artifacts: {...outputHashes},
    next_gate: "Independent normal and senior code review before any inference."
  };
  outputHashes["EXPERIMENT.json"] = writeOutput(out, "EXPERIMENT.json", experiment);
  return {outputs: outputHashes, report, experiment, sourceEvidencePool, bindingRegistry, candidatePayload, exclusionRegistry};
}

const invokedPath = process.argv[1] ? pathToFileURL(path.resolve(process.argv[1])).href : null;
if (invokedPath === import.meta.url) {
  const result = buildPackage(parseArgs(process.argv.slice(2)));
  process.stdout.write(`${JSON.stringify({status: result.report.status, counts: result.report.counts, outputs: result.outputs}, null, 2)}\n`);
}
