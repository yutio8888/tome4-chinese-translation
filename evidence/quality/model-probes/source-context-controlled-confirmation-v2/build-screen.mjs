#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../..");
const design = JSON.parse(fs.readFileSync(path.join(here, "DESIGN-CONTRACT.json"), "utf8"));
const expectedInventorySha256 = "bf9153e83aba7318741f065d8541ae74783eebc5d4552ec38627a4313456b215";
const expectedInventoryFileSha256 = "fceec52bdc2888542024f059c842a85230d8ecb396992be43b1bf8310aef5ea3";
const outputNames = ["SOURCE-SCREEN-FRAME.json", "SOURCE-EVIDENCE-PACKETS.json", "LOCAL-SCREEN-BINDINGS.json", "SCREEN-BUILD-REPORT.json"];

const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const git = (repo, args, encoding = null) => execFileSync("git", ["-C", repo, ...args], {encoding, maxBuffer: 512 * 1024 * 1024});

function parseArgs(argv) {
  const args = {out: here};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--inventory", "--engine-repo", "--out"].includes(flag)) {
      throw new Error("usage: node build-screen.mjs --inventory INVENTORY_JSONL --engine-repo ENGINE_REPO [--out OUTPUT_DIR]");
    }
    args[flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  if (!args.inventory || !args.engineRepo) throw new Error("--inventory and --engine-repo are required");
  return args;
}

export function normalizeWithMap(value) {
  let normalized = "";
  const map = [];
  let pendingSpace = false;
  let pendingIndex = 0;
  for (let index = 0; index < value.length; index += 1) {
    const escapedWhitespace = value[index] === "\\" && ["n", "r", "t"].includes(value[index + 1]);
    if (escapedWhitespace || /\s/u.test(value[index])) {
      if (!pendingSpace && normalized.length) pendingIndex = index;
      pendingSpace = normalized.length > 0;
      if (escapedWhitespace) index += 1;
      continue;
    }
    if (pendingSpace) {
      normalized += " ";
      map.push(pendingIndex);
      pendingSpace = false;
    }
    normalized += value[index];
    map.push(index);
  }
  return {normalized, map};
}

export const normalizeSource = value => normalizeWithMap(value).normalized;

export function normalizedOccurrences(fileText, source) {
  const haystack = normalizeWithMap(fileText);
  const needle = normalizeSource(source);
  if (!needle) return [];
  const occurrences = [];
  let from = 0;
  while (true) {
    const found = haystack.normalized.indexOf(needle, from);
    if (found === -1) break;
    occurrences.push({rawStart: haystack.map[found], rawEnd: haystack.map[found + needle.length - 1] + 1});
    from = found + 1;
  }
  return occurrences;
}

function parseStructured(bytes, logicalPath) {
  const text = bytes.toString("utf8");
  const parseLines = () => text.split("\n").filter(line => line.trim()).map((line, index) => {
    try { return JSON.parse(line); } catch (error) { throw new Error(`${logicalPath}:${index + 1}: ${error.message}`); }
  });
  if (logicalPath.endsWith(".jsonl")) return parseLines();
  try {
    return JSON.parse(text);
  } catch {
    return parseLines();
  }
}

export function collectExposure(value, sourceSet, revisionSet) {
  if (Array.isArray(value)) {
    for (const entry of value) collectExposure(entry, sourceSet, revisionSet);
    return;
  }
  if (!value || typeof value !== "object") return;
  if (typeof value.source === "string" && normalizeSource(value.source)) sourceSet.add(sha256(normalizeSource(value.source)));
  if (typeof value.revision_id === "string" && /^[0-9a-f]{64}$/u.test(value.revision_id)) revisionSet.add(value.revision_id);
  for (const entry of Object.values(value)) collectExposure(entry, sourceSet, revisionSet);
}

function loadExposure(manifestPath) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const lines = manifest.records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  if (sha256(lines) !== manifest.records_manifest_sha256) throw new Error("exposure records manifest drift");
  const sourceSet = new Set();
  const revisionSet = new Set();
  for (const record of manifest.records) {
    const bytes = git(root, ["show", `${manifest.git_commit}:${record.logical_path}`]);
    if (bytes.length !== record.size_bytes || sha256(bytes) !== record.sha256) throw new Error(`${record.logical_path}: frozen exposure input drift`);
    collectExposure(parseStructured(bytes, record.logical_path), sourceSet, revisionSet);
  }
  return {manifest, sourceSet, revisionSet};
}

function readInventory(file) {
  const bytes = fs.readFileSync(file);
  if (sha256(bytes) !== expectedInventoryFileSha256) throw new Error("canonical production inventory file hash mismatch");
  const rows = bytes.toString("utf8").split("\n").filter(Boolean).map((line, index) => {
    try { return JSON.parse(line); } catch (error) { throw new Error(`inventory:${index + 1}: ${error.message}`); }
  });
  if (rows.length !== 30308) throw new Error(`inventory count mismatch: ${rows.length}`);
  return {bytes, rows};
}

export function sourceOnlyInventoryView(row, label = "inventory row") {
  const allowed = new Set(["component", "profile", "profile_confidence", "occurrences", "source", "revision_id", "revision_uid", "tu_uid", "unit_id", "section", "source_tag"]);
  return new Proxy(row, {
    get(target, property, receiver) {
      if (typeof property === "symbol") return Reflect.get(target, property, receiver);
      if (!allowed.has(property)) throw new Error(`${label}: source-screen access denied for ${property}`);
      return Reflect.get(target, property, receiver);
    },
    has(_target, property) {
      if (typeof property === "symbol") return false;
      if (!allowed.has(property)) throw new Error(`${label}: source-screen presence check denied for ${property}`);
      return Object.hasOwn(row, property);
    },
    ownKeys() {
      throw new Error(`${label}: source-screen enumeration denied`);
    }
  });
}

function sectionPath(row) {
  const prefix = "mod-tome/";
  if (!row.section.startsWith(prefix)) return null;
  const relative = row.section.slice(prefix.length);
  if (!relative || relative.includes("\0") || path.posix.normalize(relative) !== relative || relative.startsWith("../")) return null;
  return path.posix.join("game/modules/tome", relative);
}

function lineNumberAt(text, offset) {
  let line = 1;
  for (let index = 0; index < offset; index += 1) if (text[index] === "\n") line += 1;
  return line;
}

function clipBefore(lines, maxLines, maxBytes) {
  let selected = lines.slice(-maxLines);
  while (selected.length && Buffer.byteLength(selected.join("\n"), "utf8") > maxBytes) selected = selected.slice(1);
  return selected.join("\n");
}

function clipAfter(lines, maxLines, maxBytes) {
  let selected = lines.slice(0, maxLines);
  while (selected.length && Buffer.byteLength(selected.join("\n"), "utf8") > maxBytes) selected = selected.slice(0, -1);
  return selected.join("\n");
}

export function makePacket(fileText, occurrence, sourceBinding, source) {
  const lineStartOffset = fileText.lastIndexOf("\n", occurrence.rawStart - 1) + 1;
  const rawLineEnd = fileText.indexOf("\n", occurrence.rawEnd);
  const lineEndOffset = rawLineEnd === -1 ? fileText.length : rawLineEnd;
  const beforeLines = fileText.slice(0, lineStartOffset).replace(/\n$/u, "").split("\n");
  const afterLines = fileText.slice(lineEndOffset + (rawLineEnd === -1 ? 0 : 1)).split("\n");
  const prefix = fileText.slice(lineStartOffset, occurrence.rawStart);
  const suffix = fileText.slice(occurrence.rawEnd, lineEndOffset);
  const before = [clipBefore(beforeLines, 12, 2000), prefix].filter(Boolean).join(beforeLines.length ? "\n" : "");
  const after = [suffix, clipAfter(afterLines, 12, 2000)].filter(Boolean).join(afterLines.length ? "\n" : "");
  if (!before.trim() || !after.trim()) return null;
  const visible = `${before}[[SOURCE_MATCH_1]]${after}`;
  if (Buffer.byteLength(visible, "utf8") > 8192 || normalizeSource(visible).includes(normalizeSource(source))) return null;
  return {
    source_binding: sourceBinding,
    occurrence: {
      line_start: lineNumberAt(fileText, occurrence.rawStart),
      line_end: lineNumberAt(fileText, occurrence.rawEnd),
      matched_span_sha256: sha256(fileText.slice(occurrence.rawStart, occurrence.rawEnd)),
      marker: "[[SOURCE_MATCH_1]]",
      lines_before_max: 12,
      lines_after_max: 12,
      visible_context_utf8_bytes: Buffer.byteLength(visible, "utf8"),
      visible_context_sha256: sha256(visible),
      visible_context: visible
    }
  };
}

function sourceFlags(row, packet) {
  const flags = [];
  if (/\b(?:he|him|his|she|her|they|them|their|it|its|this|that|these|those|here|there|you|your)\b/iu.test(row.source)) flags.push("pronoun_or_deictic");
  if ([...row.source].length <= 160) flags.push("bounded_short_source");
  if (/\b(?:if|when|unless|until|before|after|only|except|without|not|never)\b/iu.test(row.source)) flags.push("condition_or_polarity");
  if (/\b(?:action|cond|jump|quest|faction|reaction|setEffect|removeEffect|callback|newChat|define_as|subtype|on_[a-z])\b/iu.test(packet.occurrence.visible_context)) flags.push("context_behavior_signal");
  return flags;
}

function priority(row) {
  const flags = new Set(row.source_only_flags);
  if (flags.has("context_behavior_signal") && flags.has("pronoun_or_deictic")) return 0;
  if (flags.has("context_behavior_signal") && flags.has("bounded_short_source")) return 1;
  if (flags.has("pronoun_or_deictic") && flags.has("bounded_short_source")) return 2;
  if (flags.has("condition_or_polarity")) return 3;
  return 4;
}

function select(rows, profile, count, fileCap, seed) {
  const fileCounts = new Map();
  const selected = [];
  const ordered = rows.filter(row => row.profile === profile).sort((a, b) =>
    priority(a) - priority(b) ||
    sha256(`${seed}\0${profile}\0${a.revision_id}`).localeCompare(sha256(`${seed}\0${profile}\0${b.revision_id}`)) ||
    a.revision_id.localeCompare(b.revision_id)
  );
  for (const row of ordered) {
    const file = row.packet.source_binding.relative_path;
    if ((fileCounts.get(file) ?? 0) >= fileCap) continue;
    selected.push(row);
    fileCounts.set(file, (fileCounts.get(file) ?? 0) + 1);
    if (selected.length === count) break;
  }
  if (selected.length !== count) {
    const uniqueFiles = new Set(ordered.map(row => row.packet.source_binding.relative_path)).size;
    throw new Error(`${profile}: source screen only selected ${selected.length}/${count}; eligible_rows=${ordered.length}; unique_files=${uniqueFiles}; file_cap=${fileCap}`);
  }
  return selected;
}

function writeOutputs(out, outputs) {
  fs.mkdirSync(out, {recursive: true});
  for (const name of outputNames) fs.writeFileSync(path.join(out, name), jsonBytes(outputs[name]), {flag: "wx"});
}

export function build(args) {
  const exposure = loadExposure(path.join(here, "EXPOSURE-MANIFEST.json"));
  const inventory = readInventory(args.inventory);
  const cache = new Map();
  const counts = {inventory: inventory.rows.length, profile_eligible: 0, exposure_excluded: 0, locator_rejected: 0, packet_rejected: 0, eligible: 0};
  const eligible = [];
  for (let inventoryIndex = 0; inventoryIndex < inventory.rows.length; inventoryIndex += 1) {
    const row = sourceOnlyInventoryView(inventory.rows[inventoryIndex], `inventory[${inventoryIndex}]`);
    if (row.component !== "tome" || !["dialogue", "narrative"].includes(row.profile) || row.profile_confidence !== "high") continue;
    if (!Array.isArray(row.occurrences) || row.occurrences.length !== 1) continue;
    const codepoints = [...row.source].length;
    if (codepoints < design.frame.source_rules.unicode_codepoints_min || codepoints > design.frame.source_rules.unicode_codepoints_max) continue;
    counts.profile_eligible += 1;
    const sourceHash = sha256(normalizeSource(row.source));
    if (exposure.sourceSet.has(sourceHash) || exposure.revisionSet.has(row.revision_id)) { counts.exposure_excluded += 1; continue; }
    const relativePath = sectionPath(row);
    if (!relativePath) { counts.locator_rejected += 1; continue; }
    let bound = cache.get(relativePath);
    if (!bound) {
      try {
        const buffer = git(args.engineRepo, ["show", `${design.fixed_tome_source_commit}:${relativePath}`]);
        bound = {
          fileText: new TextDecoder("utf-8", {fatal: true}).decode(buffer),
          sourceBinding: {
            kind: "git_commit_blob",
            component: "tome",
            repository_alias: "t-engine4",
            commit: design.fixed_tome_source_commit,
            relative_path: relativePath,
            source_artifact_sha256: sha256(buffer),
            source_artifact_size_bytes: buffer.length
          }
        };
      } catch { bound = null; }
      cache.set(relativePath, bound);
    }
    if (!bound) { counts.locator_rejected += 1; continue; }
    const occurrences = normalizedOccurrences(bound.fileText, row.source);
    if (occurrences.length !== 1) { counts.locator_rejected += 1; continue; }
    const packet = makePacket(bound.fileText, occurrences[0], bound.sourceBinding, row.source);
    if (!packet) { counts.packet_rejected += 1; continue; }
    eligible.push({
      revision_id: row.revision_id,
      revision_uid: row.revision_uid,
      tu_uid: row.tu_uid,
      unit_id: row.unit_id,
      component: row.component,
      profile: row.profile,
      section: row.section,
      source_tag: row.source_tag,
      source: row.source,
      source_sha256: sha256(row.source),
      normalized_source_sha256: sourceHash,
      packet,
      source_only_flags: []
    });
    eligible.at(-1).source_only_flags = sourceFlags(eligible.at(-1), packet);
  }
  counts.eligible = eligible.length;
  const selected = [
    ...select(eligible, "dialogue", 120, design.frame.source_screen_file_cap, design.frame.source_screen_seed),
    ...select(eligible, "narrative", 120, design.frame.source_screen_file_cap, design.frame.source_screen_seed)
  ];
  selected.sort((a, b) => a.profile.localeCompare(b.profile) || a.revision_id.localeCompare(b.revision_id));
  const selectedWithIds = selected.map((row, index) => ({...row, screen_id: `SC${String(index + 1).padStart(3, "0")}`}));
  const screenItems = selectedWithIds.map(row => ({
    screen_id: row.screen_id,
    component: row.component,
    profile: row.profile,
    source: row.source,
    source_sha256: row.source_sha256,
    source_only_flags: row.source_only_flags
  }));
  const packets = selectedWithIds.map(row => ({screen_id: row.screen_id, source_sha256: row.source_sha256, ...row.packet}));
  const bindings = selectedWithIds.map(row => ({
    screen_id: row.screen_id,
    revision_id: row.revision_id,
    revision_uid: row.revision_uid,
    tu_uid: row.tu_uid,
    unit_id: row.unit_id,
    component: row.component,
    profile: row.profile,
    section: row.section,
    source_tag: row.source_tag,
    source_sha256: row.source_sha256,
    normalized_source_sha256: row.normalized_source_sha256,
    source_binding_sha256: sha256(JSON.stringify(row.packet.source_binding)),
    context_sha256: row.packet.occurrence.visible_context_sha256
  }));
  const frame = {
    schema_version: "source-context-controlled-confirmation-source-screen-v2",
    status: "FROZEN_SOURCE_ONLY_PROJECT_CORPUS_NOVEL_SCREEN",
    production_translation_commit: design.production_translation_commit,
    inventory_sha256: expectedInventorySha256,
    inventory_file_sha256: expectedInventoryFileSha256,
    exposure_manifest_sha256: sha256(fs.readFileSync(path.join(here, "EXPOSURE-MANIFEST.json"))),
    selection_seed: design.frame.source_screen_seed,
    counts: {items: screenItems.length, dialogue: 120, narrative: 120},
    items: screenItems
  };
  const packetOutput = {
    schema_version: "source-context-controlled-confirmation-source-packets-v2",
    status: "FROZEN_MECHANICAL_FIXED_SOURCE_PACKETS",
    source_screen_sha256: sha256(jsonBytes(frame)),
    items: packets
  };
  const bindingOutput = {
    schema_version: "source-context-controlled-confirmation-local-screen-bindings-v2",
    status: "LOCAL_ONLY_NO_TARGETS_READ_OR_STORED",
    source_screen_sha256: sha256(jsonBytes(frame)),
    inventory_sha256: expectedInventorySha256,
    inventory_file_sha256: expectedInventoryFileSha256,
    items: bindings
  };
  const preReport = {
    schema_version: "source-context-controlled-confirmation-screen-build-report-v2",
    status: "PASS",
    inference_allowed: false,
    target_fields_accessed_for_selection: false,
    counts,
    selected: {items: 240, dialogue: 120, narrative: 120, unique_revisions: new Set(bindings.map(item => item.revision_id)).size, unique_sources: new Set(bindings.map(item => item.normalized_source_sha256)).size, source_files: new Set(packets.map(item => item.source_binding.relative_path)).size},
    hashes: {
      design_contract: sha256(fs.readFileSync(path.join(here, "DESIGN-CONTRACT.json"))),
      exposure_manifest: sha256(fs.readFileSync(path.join(here, "EXPOSURE-MANIFEST.json"))),
      source_screen: sha256(jsonBytes(frame)),
      source_packets: sha256(jsonBytes(packetOutput)),
      local_bindings: sha256(jsonBytes(bindingOutput))
    }
  };
  return {"SOURCE-SCREEN-FRAME.json": frame, "SOURCE-EVIDENCE-PACKETS.json": packetOutput, "LOCAL-SCREEN-BINDINGS.json": bindingOutput, "SCREEN-BUILD-REPORT.json": preReport};
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const args = parseArgs(process.argv.slice(2));
  const outputs = build(args);
  writeOutputs(args.out, outputs);
  console.log(JSON.stringify(outputs["SCREEN-BUILD-REPORT.json"], null, 2));
}
