#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const seed = "source-context-controlled-confirmation-v2/clean-audit-source-selection/2026-08-28";

function rank(...parts) { return sha256(parts.join("\0")); }

export function selectProfile(rows, packetById, profile, count = 60, fileCap = 5) {
  const matching = rows.filter(row => row.profile === profile);
  const byFile = new Map();
  for (const row of matching) {
    const file = packetById.get(row.screen_id).source_binding.relative_path;
    if (!byFile.has(file)) byFile.set(file, []);
    byFile.get(file).push(row);
  }
  const files = [...byFile].map(([file, items]) => ({
    file,
    file_rank: rank(seed, profile, "file", file),
    items: items.sort((a, b) =>
      b.source_only_flags.length - a.source_only_flags.length ||
      rank(seed, profile, "row", a.screen_id).localeCompare(rank(seed, profile, "row", b.screen_id)) ||
      a.screen_id.localeCompare(b.screen_id)
    )
  })).sort((a, b) => a.file_rank.localeCompare(b.file_rank) || a.file.localeCompare(b.file));
  const selected = [];
  for (let round = 0; round < fileCap && selected.length < count; round += 1) {
    for (const file of files) {
      if (selected.length === count) break;
      if (file.items[round]) selected.push(file.items[round]);
    }
  }
  if (selected.length !== count) throw new Error(`${profile}: selected ${selected.length}/${count} under file cap ${fileCap}`);
  const selectedIds = new Set(selected.map(item => item.screen_id));
  const reserves = matching.filter(item => !selectedIds.has(item.screen_id)).sort((a, b) =>
    rank(seed, profile, "reserve", a.screen_id).localeCompare(rank(seed, profile, "reserve", b.screen_id)) ||
    a.screen_id.localeCompare(b.screen_id)
  );
  return {selected, reserves, files: files.length};
}

export function buildSelection() {
  const screenBytes = fs.readFileSync(path.join(here, "SOURCE-SCREEN-FRAME.json"));
  const packetBytes = fs.readFileSync(path.join(here, "SOURCE-EVIDENCE-PACKETS.json"));
  const screen = JSON.parse(screenBytes);
  const packets = JSON.parse(packetBytes);
  const packetById = new Map(packets.items.map(item => [item.screen_id, item]));
  const dialogue = selectProfile(screen.items, packetById, "dialogue");
  const narrative = selectProfile(screen.items, packetById, "narrative");
  const primary = [...dialogue.selected, ...narrative.selected];
  const reserves = [...dialogue.reserves, ...narrative.reserves];
  const source = {
    schema_version: "source-context-controlled-confirmation-audit-source-selection-v2",
    status: "FROZEN_SOURCE_ONLY_CLEAN_AUDIT_SELECTION",
    source_screen_sha256: sha256(screenBytes),
    source_packets_sha256: sha256(packetBytes),
    selection_seed: seed,
    selection_rule: "Within each profile, rank source files by SHA-256, rank rows by descending frozen source-only flag count then SHA-256, and select round-robin for at most five rounds. Target fields are unavailable to this script.",
    counts: {primary: 120, dialogue: 60, narrative: 60, ordered_reserves: 120},
    primary: primary.map((item, index) => ({audit_ordinal: index + 1, ...item})),
    ordered_reserves: reserves.map((item, index) => ({reserve_ordinal: index + 1, ...item}))
  };
  const local = {
    schema_version: "source-context-controlled-confirmation-audit-source-local-bindings-v2",
    status: "LOCAL_ONLY_SOURCE_CONTEXT_BINDINGS",
    audit_source_selection_sha256: sha256(jsonBytes(source)),
    primary: primary.map(item => ({screen_id: item.screen_id, relative_path: packetById.get(item.screen_id).source_binding.relative_path, context_sha256: packetById.get(item.screen_id).occurrence.visible_context_sha256})),
    ordered_reserves: reserves.map(item => ({screen_id: item.screen_id, relative_path: packetById.get(item.screen_id).source_binding.relative_path, context_sha256: packetById.get(item.screen_id).occurrence.visible_context_sha256}))
  };
  const report = {
    schema_version: "source-context-controlled-confirmation-audit-source-selection-report-v2",
    status: "PASS",
    model_calls: 0,
    network_calls: 0,
    target_fields_accessed_for_selection: false,
    counts: {
      primary: primary.length,
      dialogue: dialogue.selected.length,
      narrative: narrative.selected.length,
      dialogue_source_files: new Set(local.primary.filter((_, index) => index < 60).map(item => item.relative_path)).size,
      narrative_source_files: new Set(local.primary.filter((_, index) => index >= 60).map(item => item.relative_path)).size,
      max_primary_per_source_file: Math.max(...Object.values(local.primary.reduce((acc, item) => (acc[item.relative_path] = (acc[item.relative_path] ?? 0) + 1, acc), {}))),
      ordered_reserves: reserves.length
    },
    hashes: {source_selection: sha256(jsonBytes(source)), local_bindings: sha256(jsonBytes(local))}
  };
  return {"AUDIT-SOURCE-SELECTION.json": source, "LOCAL-AUDIT-SOURCE-BINDINGS.json": local, "AUDIT-SOURCE-SELECTION-REPORT.json": report};
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const outputs = buildSelection();
  for (const [name, value] of Object.entries(outputs)) fs.writeFileSync(path.join(here, name), jsonBytes(value), {flag: "wx"});
  console.log(JSON.stringify(outputs["AUDIT-SOURCE-SELECTION-REPORT.json"], null, 2));
}
