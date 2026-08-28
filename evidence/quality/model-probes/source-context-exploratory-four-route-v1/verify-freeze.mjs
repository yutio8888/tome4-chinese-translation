#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const experiment = JSON.parse(fs.readFileSync(path.join(directory, "EXPERIMENT.json"), "utf8"));
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
for (const [name, expected] of Object.entries(experiment.frozen_hashes)) {
  if (/PENDING/u.test(expected)) throw new Error(`${name}: pending hash in frozen experiment`);
  const actual = sha256(fs.readFileSync(path.join(directory, name)));
  if (actual !== expected) throw new Error(`${name}: frozen hash mismatch`);
}
for (const [name, expected] of Object.entries({
  "AUDIT-QUEUE.json": experiment.upstream.audit_queue_sha256,
  "FINAL-ADJUDICATION.json": experiment.upstream.final_adjudication_sha256,
  "RESULT.json": experiment.upstream.result_sha256
})) {
  const actual = sha256(fs.readFileSync(path.resolve(directory, "../prospective-source-context-truth-audit-v1", name)));
  if (actual !== expected) throw new Error(`${name}: upstream hash mismatch`);
}
const inputA = JSON.parse(fs.readFileSync(path.join(directory, "INPUT-A.json"), "utf8"));
const inputB = JSON.parse(fs.readFileSync(path.join(directory, "INPUT-B.json"), "utf8"));
if (JSON.stringify(Object.keys(inputA)) !== JSON.stringify(Object.keys(inputB))) throw new Error("A/B top-level keys differ");
if (inputA.items.length !== 14 || inputB.items.length !== 14) throw new Error("A/B item count mismatch");
for (let index = 0; index < 14; index += 1) {
  const a = inputA.items[index];
  const b = inputB.items[index];
  const withoutContext = item => ({item_id: item.item_id, source: item.source, target: item.target});
  if (JSON.stringify(withoutContext(a)) !== JSON.stringify(withoutContext(b))) throw new Error(`item ${index}: non-context A/B difference`);
  if (!Array.isArray(a.fixed_context) || a.fixed_context.length !== 0) throw new Error(`item ${index}: A context not empty`);
  if (!Array.isArray(b.fixed_context) || b.fixed_context.length === 0) throw new Error(`item ${index}: B context missing`);
}
const outbound = `${fs.readFileSync(path.join(directory, "PROMPT.md"), "utf8")}\n${JSON.stringify(inputA)}\n${JSON.stringify(inputB)}`;
for (const pattern of [/\/home\//u, /\bV1-[0-9]{3}\b/u, /\baudit_id\b/u, /\btask_id\b/u, /CONTEXT_DEFECT|SURFACE_DEFECT|CONTEXT_EXONERATED_CLEAN|ORDINARY_CLEAN/u]) {
  if (pattern.test(outbound)) throw new Error(`outbound leakage pattern ${pattern}`);
}
const reference = JSON.parse(fs.readFileSync(path.join(directory, "REFERENCE.json"), "utf8"));
if (reference.status !== "SEALED_NOT_FOR_MODEL_INPUT" || reference.items.length !== 14) throw new Error("reference contract mismatch");
for (const item of reference.items) {
  for (const removed of item.sanitization_removed_lines.flat()) {
    if (!(/^\s*--.*(?:@[A-Z0-9.-]+\.[A-Z]{2,}|copyright|general public license|<http)/iu.test(removed))) throw new Error(`${item.item_id}: overbroad sanitization removal`);
  }
}
process.stdout.write(`${JSON.stringify({status: "PASS", items: 14, outbound_truth_leakage: false, ab_only_fixed_context_differs: true}, null, 2)}\n`);
