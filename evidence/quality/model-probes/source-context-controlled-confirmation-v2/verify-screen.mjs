#!/usr/bin/env node

import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {build, normalizeSource} from "./build-screen.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--inventory", "--engine-repo"].includes(flag)) throw new Error("usage: node verify-screen.mjs --inventory INVENTORY --engine-repo ENGINE_REPO");
    args[flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  if (!args.inventory || !args.engineRepo) throw new Error("--inventory and --engine-repo are required");
  return args;
}

function forbiddenWalk(value, label) {
  const forbiddenKeys = /^(?:target|target_sha256|task_id|original_revision_key|mutation|mutation_id|expected_claim|atom|truth|provider|model|adjudication)$/iu;
  function visit(node, pointer) {
    if (Array.isArray(node)) return node.forEach((entry, index) => visit(entry, `${pointer}/${index}`));
    if (!node || typeof node !== "object") return;
    for (const [key, entry] of Object.entries(node)) {
      assert.equal(forbiddenKeys.test(key), false, `${label}${pointer}/${key}: forbidden key`);
      visit(entry, `${pointer}/${key}`);
    }
  }
  visit(value, "");
}

const args = parseArgs(process.argv.slice(2));
const rebuilt = build({...args, out: here});
for (const [name, value] of Object.entries(rebuilt)) {
  const actual = fs.readFileSync(path.join(here, name));
  assert.deepEqual(actual, jsonBytes(value), `${name}: rebuild drift`);
}

const frame = rebuilt["SOURCE-SCREEN-FRAME.json"];
const packets = rebuilt["SOURCE-EVIDENCE-PACKETS.json"];
const bindings = rebuilt["LOCAL-SCREEN-BINDINGS.json"];
const report = rebuilt["SCREEN-BUILD-REPORT.json"];
assert.equal(frame.items.length, 240);
assert.equal(frame.items.filter(item => item.profile === "dialogue").length, 120);
assert.equal(frame.items.filter(item => item.profile === "narrative").length, 120);
assert.equal(new Set(frame.items.map(item => item.screen_id)).size, 240);
assert.equal(new Set(frame.items.map(item => normalizeSource(item.source))).size, 240);
assert.equal(new Set(bindings.items.map(item => item.revision_id)).size, 240);
assert.deepEqual(frame.items.map(item => item.screen_id), packets.items.map(item => item.screen_id));
assert.deepEqual(frame.items.map(item => item.screen_id), bindings.items.map(item => item.screen_id));
assert.equal(report.target_fields_accessed_for_selection, false);
assert.equal(report.selected.source_files, 50);
assert.equal(report.hashes.source_screen, sha256(jsonBytes(frame)));
assert.equal(report.hashes.source_packets, sha256(jsonBytes(packets)));
assert.equal(report.hashes.local_bindings, sha256(jsonBytes(bindings)));
forbiddenWalk(frame, "SOURCE-SCREEN-FRAME");
forbiddenWalk(packets, "SOURCE-EVIDENCE-PACKETS");
for (let index = 0; index < frame.items.length; index += 1) {
  const item = frame.items[index];
  const packet = packets.items[index];
  assert.equal(packet.source_sha256, item.source_sha256);
  assert.equal(packet.occurrence.marker, "[[SOURCE_MATCH_1]]");
  assert.equal(packet.occurrence.visible_context.includes("[[SOURCE_MATCH_1]]"), true);
  assert.equal(normalizeSource(packet.occurrence.visible_context).includes(normalizeSource(item.source)), false);
  assert.equal(Buffer.byteLength(packet.occurrence.visible_context, "utf8") <= 8192, true);
}

console.log(JSON.stringify({status: "PASS", rebuilt_files: Object.keys(rebuilt).length, items: 240, hashes: report.hashes}, null, 2));
