#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  PHASE0_SCALAR_FIELDS,
  SOURCE_ONLY_FLAGS,
  buildFrozenPackage,
  classifyCategory,
  contentExposureKey,
  locatorContentKey,
  sha256Bytes
} from "./build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");
const generatedNames = [
  "SOURCE-ONLY-BASE-FRAME.json",
  "SOURCE-SCREEN-FRAME.json",
  "SOURCE-EVIDENCE-PACKETS.json",
  "SOURCE-EXPOSURE-REGISTRY.json",
  "BUILD-REPORT.json"
];

function parseArgs(argv) {
  const args = {root: defaultRoot};
  const flags = new Set(["--production-repo", "--engine-repo", "--dlc-root", "--root"]);
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!flags.has(flag) || !value) {
      throw new Error("usage: node verify.mjs --production-repo PRODUCTION_REPO --engine-repo ENGINE_REPO --dlc-root DLC_ROOT [--root RESEARCH_REPO]");
    }
    const key = flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    args[key] = path.resolve(value);
    index += 1;
  }
  if (!args.productionRepo || !args.engineRepo || !args.dlcRoot) throw new Error("--production-repo, --engine-repo and --dlc-root are required");
  return args;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function exactKeys(value, expected, label) {
  assert.deepEqual(Object.keys(value).sort(), [...expected].sort(), `${label}: field set drift`);
}

function walkKeys(value, callback, pointer = "") {
  if (Array.isArray(value)) {
    value.forEach((entry, index) => walkKeys(entry, callback, `${pointer}/${index}`));
    return;
  }
  if (!value || typeof value !== "object") return;
  for (const [key, entry] of Object.entries(value)) {
    callback(key, `${pointer}/${key}`);
    walkKeys(entry, callback, `${pointer}/${key}`);
  }
}

function fileRecord(file) {
  const bytes = fs.readFileSync(file);
  return {sha256: sha256Bytes(bytes), size_bytes: bytes.length};
}

function verifySourceArtifact(record, args, contract) {
  let bytes;
  if (record.kind === "git_commit_blob") {
    assert.equal(record.component, "tome");
    assert.equal(record.commit, contract.source_bindings.tome.commit);
    bytes = execFileSync("git", ["-C", args.engineRepo, "show", `${record.commit}:${record.relative_path}`], {maxBuffer: 128 * 1024 * 1024});
  } else if (record.kind === "dlc_file_sha256") {
    const binding = contract.source_bindings[record.component];
    assert.ok(binding && binding.read_mode === "working_tree_file_with_required_sha256");
    assert.equal(record.commit, null);
    const registeredRoot = fs.realpathSync(path.resolve(args.dlcRoot, binding.dlc_subdirectory));
    const candidate = fs.realpathSync(path.resolve(registeredRoot, record.relative_path));
    const relative = path.relative(registeredRoot, candidate);
    assert.ok(relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative), "DLC artifact escaped registered root");
    bytes = fs.readFileSync(candidate);
  } else {
    throw new Error(`unknown source artifact kind ${record.kind}`);
  }
  assert.equal(sha256Bytes(bytes), record.sha256, `${record.component}/${record.relative_path}: source hash drift`);
  assert.equal(bytes.length, record.size_bytes, `${record.component}/${record.relative_path}: source size drift`);
}

const args = parseArgs(process.argv.slice(2));
const contract = readJson(path.join(here, "SCREEN-CONTRACT.json"));
const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-source-context-audit-v4-"));
try {
  buildFrozenPackage({...args, out: temporaryDirectory});
  for (const name of generatedNames) {
    const expected = fs.readFileSync(path.join(here, name));
    const actual = fs.readFileSync(path.join(temporaryDirectory, name));
    assert.deepEqual(actual, expected, `${name}: deterministic rebuild differs`);
    JSON.parse(expected.toString("utf8"));
  }

  const base = readJson(path.join(here, "SOURCE-ONLY-BASE-FRAME.json"));
  const frame = readJson(path.join(here, "SOURCE-SCREEN-FRAME.json"));
  const packets = readJson(path.join(here, "SOURCE-EVIDENCE-PACKETS.json"));
  const registry = readJson(path.join(here, "SOURCE-EXPOSURE-REGISTRY.json"));
  const report = readJson(path.join(here, "BUILD-REPORT.json"));
  const experiment = readJson(path.join(here, "EXPERIMENT.json"));
  assert.equal(frame.mode, "NO_INFERENCE/SOURCE_SCREEN_ONLY");
  assert.equal(frame.source_only, true);
  assert.equal(frame.model_calls_made, 0);
  assert.equal(frame.network_calls_made, 0);
  assert.equal(packets.mode, frame.mode);
  assert.equal(packets.source_only, true);
  assert.equal(registry.raw_output_tier_used, false);
  assert.equal(report.status, "PASS_SOURCE_SCREEN_GATES");
  assert.ok(Object.values(report.gates).every(value => value === true));
  assert.deepEqual(report.no_go, []);
  assert.equal(experiment.status, "NO_INFERENCE/SOURCE_SCREEN_ONLY");
  assert.equal(experiment.model_calls, 0);
  assert.equal(experiment.network_calls, 0);
  assert.equal(base.mode, "NO_INFERENCE/SOURCE_SCREEN_ONLY");
  assert.equal(base.source_only, true);
  assert.equal(base.items.length, 1396);
  assert.equal(base.counts.items, 1396);
  assert.equal(base.counts.tasks, 46);
  assert.equal(base.source_projection_sha256, sha256Bytes(Buffer.from(JSON.stringify(base.items), "utf8")));
  for (let index = 0; index < base.items.length; index += 1) {
    const item = base.items[index];
    exactKeys(item, [...PHASE0_SCALAR_FIELDS, "source_only_flags"], `source-only-base[${index}]`);
    assert.equal(sha256Bytes(item.source), item.source_sha256);
    assert.ok(item.source_only_flags.every(flag => SOURCE_ONLY_FLAGS.includes(flag)));
  }

  const forbiddenModelFacingKeys = new Set([
    "target",
    "target_sha256",
    "pair_sha256",
    "canonical_revision_id",
    "canonical_revision_uid",
    "canonical_unit_id",
    "canonical_tu_uid",
    "membership_sha256",
    "multiline",
    "args_order",
    "preferred_terms",
    "relevant_terms",
    "terminology"
  ]);
  for (const [name, value] of [["SOURCE-SCREEN-FRAME.json", frame], ["SOURCE-EVIDENCE-PACKETS.json", packets]]) {
    walkKeys(value, (key, pointer) => {
      assert.equal(forbiddenModelFacingKeys.has(key), false, `${name}${pointer}: forbidden key exposed`);
    });
    assert.equal(/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/u.test(fs.readFileSync(path.join(here, name), "utf8")), false, `${name}: local absolute path leaked`);
  }

  const frameByCategory = new Map(frame.categories.map(category => [category.category, category]));
  const packetsByCategory = new Map(packets.categories.map(category => [category.category, category]));
  assert.deepEqual([...frameByCategory.keys()], ["Runtime", "Narrative"]);
  assert.deepEqual([...packetsByCategory.keys()], ["Runtime", "Narrative"]);
  const allIdentities = new Set();
  const allContent = new Set();
  const exposedContent = new Set(registry.exposed_content_keys.map(record => record.content_key));
  const taskMaximums = [];
  for (const categoryName of ["Runtime", "Narrative"]) {
    const category = frameByCategory.get(categoryName);
    const categoryPackets = packetsByCategory.get(categoryName).packets;
    assert.equal(category.items.length, 60);
    assert.equal(categoryPackets.length, 60);
    const taskCounts = new Map();
    for (let index = 0; index < category.items.length; index += 1) {
      const item = category.items[index];
      const packet = categoryPackets[index];
      exactKeys(item, [...PHASE0_SCALAR_FIELDS, "source_only_flags"], `${categoryName}[${index}]`);
      assert.equal(sha256Bytes(item.source), item.source_sha256);
      const sourceBytes = Buffer.byteLength(item.source, "utf8");
      assert.ok(sourceBytes >= 1 && sourceBytes <= 6000);
      assert.notEqual(item.profile, "term-name");
      assert.ok(item.source_only_flags.every(flag => SOURCE_ONLY_FLAGS.includes(flag)));
      assert.equal(classifyCategory(item), categoryName);
      const identity = `${item.task_id}\0${item.original_revision_key}`;
      assert.equal(allIdentities.has(identity), false, `${identity}: category overlap or duplicate identity`);
      allIdentities.add(identity);
      const content = locatorContentKey(item.component, item.source);
      assert.equal(allContent.has(content), false, `${identity}: duplicate component/content`);
      allContent.add(content);
      assert.equal(exposedContent.has(contentExposureKey(item.source)), false, `${identity}: frozen source exposure leaked into screen`);
      taskCounts.set(item.task_id, (taskCounts.get(item.task_id) ?? 0) + 1);

      assert.equal(packet.task_id, item.task_id);
      assert.equal(packet.original_revision_key, item.original_revision_key);
      assert.equal(packet.component, item.component);
      assert.equal(packet.section, item.section);
      assert.equal(packet.source_sha256, item.source_sha256);
      assert.ok([1, 2].includes(packet.source_occurrences));
      assert.equal(packet.occurrences.length, packet.source_occurrences);
      assert.equal(packet.source_binding.component, item.component);
      assert.equal(packet.source_binding.relative_path.startsWith("/"), false);
      let visibleTotal = 0;
      for (const occurrence of packet.occurrences) {
        assert.ok(occurrence.lines_before <= 12);
        assert.ok(occurrence.lines_after <= 12);
        assert.ok(occurrence.before_utf8_bytes <= 2000);
        assert.ok(occurrence.after_utf8_bytes <= 2000);
        assert.ok(occurrence.visible_context_utf8_bytes <= 8192);
        assert.equal(Buffer.byteLength(occurrence.visible_context, "utf8"), occurrence.visible_context_utf8_bytes);
        assert.equal(sha256Bytes(occurrence.visible_context), occurrence.visible_context_sha256);
        assert.ok(occurrence.visible_context.includes(occurrence.marker));
        assert.equal(occurrence.marker, `[[SOURCE_MATCH_${occurrence.occurrence_ordinal}]]`);
        visibleTotal += occurrence.visible_context_utf8_bytes;
      }
      assert.equal(visibleTotal, packet.combined_visible_context_utf8_bytes);
      assert.ok(visibleTotal <= 8192);
      assert.equal(Buffer.byteLength(JSON.stringify(packet), "utf8"), packet.supplemental_json_utf8_bytes);
      assert.ok(packet.supplemental_json_utf8_bytes <= 12288);
    }
    const taskCount = taskCounts.size;
    assert.ok(taskCount >= contract.required_gates[categoryName].minimum_tasks);
    taskMaximums.push(...taskCounts.values());
  }
  assert.equal(allIdentities.size, 120);
  assert.equal(allContent.size, 120);
  assert.ok(Math.max(...taskMaximums) <= 6);

  const presentationPayload = {
    schema_version: "prospective-source-only-presentation-v4",
    categories: ["Runtime", "Narrative"].map(categoryName => ({
      category: categoryName,
      items: frameByCategory.get(categoryName).items,
      source_evidence_packets: packetsByCategory.get(categoryName).packets
    }))
  };
  const presentationSha256 = sha256Bytes(Buffer.from(JSON.stringify(presentationPayload), "utf8"));
  assert.equal(frame.presentation_sha256, presentationSha256);
  assert.equal(packets.presentation_sha256, presentationSha256);
  assert.equal(report.presentation_sha256, presentationSha256);
  assert.equal(experiment.frozen_hashes.source_only_presentation_sha256, presentationSha256);

  const expectedStructured = contract.frozen_inputs.tracked_model_facing_structured_inputs;
  const actualStructured = registry.tracked_model_facing_structured_input_manifest;
  assert.deepEqual(actualStructured.records, expectedStructured.records);
  assert.equal(actualStructured.count, expectedStructured.count);
  assert.equal(actualStructured.bytes, expectedStructured.bytes);
  assert.equal(actualStructured.manifest_sha256, expectedStructured.manifest_sha256);
  assert.ok(actualStructured.records.every(record => !/(?:^|\/)RAW(?:-|\.|$)/u.test(record.logical_path)));
  const tracked = new Set(execFileSync("git", ["ls-files", "-z"], {cwd: args.root, encoding: "utf8"}).split("\0").filter(Boolean));
  assert.ok(actualStructured.records.every(record => tracked.has(record.logical_path)), "structured input manifest contains an untracked path");
  for (const planned of registry.frozen_future_model_facing_structured_outputs) {
    assert.deepEqual(fileRecord(path.join(here, planned.logical_path)), {sha256: planned.sha256, size_bytes: planned.size_bytes});
  }
  assert.equal(experiment.frozen_hashes.source_screen_frame_sha256, fileRecord(path.join(here, "SOURCE-SCREEN-FRAME.json")).sha256);
  assert.equal(experiment.frozen_hashes.source_only_base_frame_sha256, fileRecord(path.join(here, "SOURCE-ONLY-BASE-FRAME.json")).sha256);
  assert.equal(experiment.frozen_hashes.source_evidence_packets_sha256, fileRecord(path.join(here, "SOURCE-EVIDENCE-PACKETS.json")).sha256);
  assert.equal(experiment.frozen_hashes.source_exposure_registry_sha256, fileRecord(path.join(here, "SOURCE-EXPOSURE-REGISTRY.json")).sha256);
  assert.equal(experiment.frozen_hashes.build_report_sha256, fileRecord(path.join(here, "BUILD-REPORT.json")).sha256);

  const artifactRecords = packets.source_artifact_manifest.records;
  const artifactKeys = new Set();
  for (const record of artifactRecords) {
    const key = `${record.component}\0${record.relative_path}`;
    assert.equal(artifactKeys.has(key), false, `${key}: duplicate source artifact manifest row`);
    artifactKeys.add(key);
    verifySourceArtifact(record, args, contract);
  }
  assert.equal(artifactRecords.length, packets.source_artifact_manifest.count);
  assert.equal(packets.tome_commit, "624a67329fe2ad440c5b344785a9c73fcf22ae63");
  for (const field of ["count", "bytes", "manifest_sha256"]) {
    assert.equal(report.fingerprinted_terminal_input_manifest[field], contract.frozen_inputs.fingerprinted_terminal_input_manifest[field]);
  }
  assert.equal(fileRecord(path.join(args.root, contract.frozen_inputs.executor_fixture.logical_path)).sha256, contract.frozen_inputs.executor_fixture.sha256);

  process.stdout.write(`${JSON.stringify({
    status: "PASS",
    deterministic_outputs: generatedNames,
    presentation_sha256: presentationSha256,
    counts: frame.counts,
    source_artifact_manifest_sha256: packets.source_artifact_manifest.manifest_sha256,
    structured_input_manifest_sha256: actualStructured.manifest_sha256
  }, null, 2)}\n`);
} finally {
  const expectedPrefix = `${path.resolve(os.tmpdir())}${path.sep}prospective-source-context-audit-v4-`;
  const resolved = path.resolve(temporaryDirectory);
  if (!resolved.startsWith(expectedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolved, {recursive: true, force: true});
}
