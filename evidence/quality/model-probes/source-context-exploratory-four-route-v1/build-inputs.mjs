#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const refresh = process.argv.includes("--refresh");
const upstream = path.resolve(directory, "../prospective-source-context-truth-audit-v1");
const expected = {
  "AUDIT-QUEUE.json": "3f629d6eb9a7b3264582e7b860be7ac77cd038f3f8ac2df2ad9736fee64a2ebe",
  "FINAL-ADJUDICATION.json": "455f0e3b744795617ce058e58e4adb3d331428ee5afbad97a01521822bae159c",
  "RESULT.json": "d4165fc353987db14893eda04da06e4321bd963e7618659ca1ca8f410b4e3593"
};
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const readUpstream = name => {
  const bytes = fs.readFileSync(path.join(upstream, name));
  if (sha256(bytes) !== expected[name]) throw new Error(`${name}: frozen upstream hash mismatch`);
  return JSON.parse(bytes.toString("utf8"));
};
const queue = readUpstream("AUDIT-QUEUE.json");
const adjudication = readUpstream("FINAL-ADJUDICATION.json");
readUpstream("RESULT.json");
const queueById = new Map(queue.items.map(item => [item.audit_id, item]));
const finalById = new Map(adjudication.items.map(item => [item.audit_id, item]));

const selected = [
  {audit_id: "V1-106", truth_class: "CONTEXT_DEFECT", atom: "固定前文明确对象是尸体和死灵仪式；animate 是使尸体复生为亡灵仆从，译成“唤醒”误述行动性质。"},
  {audit_id: "V1-065", truth_class: "SURFACE_DEFECT", atom: "immediate（迫切、当前优先）被译成“最大”（程度排名）。"},
  {audit_id: "V1-071", truth_class: "SURFACE_DEFECT", atom: "遗漏水晶球是旅行手段，并把对持有多元水晶球的惊讶推测改为确定否认。"},
  {audit_id: "V1-077", truth_class: "SURFACE_DEFECT", atom: "technically 的限定被反向译成“真正的结束”。"},
  {audit_id: "V1-100", truth_class: "SURFACE_DEFECT", atom: "imploded（向内坍爆）被改成体内发生爆裂，破坏与 exploded 的死亡方式区分。"},
  {audit_id: "V1-102", truth_class: "SURFACE_DEFECT", atom: "遗漏说话者曾在荒野遇见该学徒的既往相遇关系。"},
  {audit_id: "V1-003", truth_class: "CONTEXT_EXONERATED_CLEAN", atom: null},
  {audit_id: "V1-005", truth_class: "CONTEXT_EXONERATED_CLEAN", atom: null},
  {audit_id: "V1-011", truth_class: "CONTEXT_EXONERATED_CLEAN", atom: null},
  {audit_id: "V1-026", truth_class: "CONTEXT_EXONERATED_CLEAN", atom: null}
];
const selectedIds = new Set(selected.map(item => item.audit_id));
const usedTasks = new Set(selected.map(item => queueById.get(item.audit_id)?.task_id));
const seed = "source-context-exploratory-four-route-v1|ordinary-clean-v1";
const rank = value => sha256(Buffer.from(`${seed}\0${value}`, "utf8"));
for (const category of ["Runtime", "Narrative"]) {
  const candidates = adjudication.items
    .filter(item => item.category === category && item.final_label === "CLEAN" && item.packet_sufficient)
    .filter(item => item.surface_candidate.label === "CLEAN" && item.context_candidate.label === "CLEAN")
    .filter(item => !selectedIds.has(item.audit_id) && !usedTasks.has(item.task_id))
    .sort((left, right) => rank(left.audit_id).localeCompare(rank(right.audit_id)));
  let added = 0;
  for (const item of candidates) {
    if (usedTasks.has(item.task_id)) continue;
    selected.push({audit_id: item.audit_id, truth_class: "ORDINARY_CLEAN", atom: null});
    selectedIds.add(item.audit_id);
    usedTasks.add(item.task_id);
    added += 1;
    if (added === 2) break;
  }
  if (added !== 2) throw new Error(`${category}: unable to select two ordinary clean controls`);
}

const orderSeed = "source-context-exploratory-four-route-v1|presentation-order-v1";
selected.sort((left, right) => sha256(Buffer.from(`${orderSeed}\0${left.audit_id}`)).localeCompare(sha256(Buffer.from(`${orderSeed}\0${right.audit_id}`))));
const sanitizeContext = text => {
  const removedLines = [];
  const keptLines = [];
  for (const line of text.split(/\r?\n/u)) {
    const publicEmailHeader = /^\s*--.*\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/iu.test(line);
    const licenseHeader = /^\s*--.*(?:copyright|general public license|<http)/iu.test(line);
    if (publicEmailHeader || licenseHeader) removedLines.push(line);
    else keptLines.push(line);
  }
  return {text: keptLines.join("\n"), removedLines};
};
const inputA = {schema_version: "source-context-exploratory-input-v1", items: []};
const inputB = {schema_version: "source-context-exploratory-input-v1", items: []};
const reference = {schema_version: "source-context-exploratory-reference-v1", status: "SEALED_NOT_FOR_MODEL_INPUT", items: []};
selected.forEach((selection, index) => {
  const itemId = `E${String(index + 1).padStart(3, "0")}`;
  const queueItem = queueById.get(selection.audit_id);
  const finalItem = finalById.get(selection.audit_id);
  if (!queueItem || !finalItem) throw new Error(`${selection.audit_id}: upstream item missing`);
  const expectedLabel = selection.truth_class.endsWith("DEFECT") ? finalItem.final_label : "CLEAN";
  if (selection.truth_class === "CONTEXT_DEFECT" && finalItem.final_label !== "CONTEXT_DEPENDENT_DEFECT") throw new Error(`${selection.audit_id}: context truth mismatch`);
  if (selection.truth_class === "SURFACE_DEFECT" && finalItem.final_label !== "SURFACE_VISIBLE_DEFECT") throw new Error(`${selection.audit_id}: surface truth mismatch`);
  if (selection.truth_class.endsWith("CLEAN") && finalItem.final_label !== "CLEAN") throw new Error(`${selection.audit_id}: clean truth mismatch`);
  const base = {item_id: itemId, source: queueItem.source, target: queueItem.target, fixed_context: []};
  const sanitized = queueItem.source_evidence.occurrences.map(occurrence => sanitizeContext(occurrence.visible_context.replaceAll(occurrence.marker, "[SOURCE_MATCH]")));
  const context = sanitized.map(value => value.text);
  inputA.items.push(base);
  inputB.items.push({...base, fixed_context: context});
  reference.items.push({
    item_id: itemId,
    audit_id: selection.audit_id,
    task_id: queueItem.task_id,
    category: queueItem.category,
    truth_class: selection.truth_class,
    final_label: expectedLabel,
    material_atom: selection.atom,
    lead_basis: finalItem.written_evidence.lead_basis,
    context_sha256s: queueItem.source_evidence.occurrences.map(occurrence => occurrence.visible_context_sha256),
    sanitized_context_sha256s: context.map(value => sha256(Buffer.from(value, "utf8"))),
    sanitization_removed_lines: sanitized.map(value => value.removedLines)
  });
});

const outputs = {"INPUT-A.json": inputA, "INPUT-B.json": inputB, "REFERENCE.json": reference};
for (const [name, value] of Object.entries(outputs)) {
  const bytes = Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
  const target = path.join(directory, name);
  if (fs.existsSync(target)) {
    if (!fs.readFileSync(target).equals(bytes)) {
      if (!refresh) throw new Error(`${name}: refusing to overwrite non-identical frozen bytes`);
      fs.writeFileSync(target, bytes);
    }
  } else {
    fs.writeFileSync(target, bytes);
  }
  process.stdout.write(`${name} sha256=${sha256(bytes)} bytes=${bytes.length}\n`);
}
process.stdout.write(`${JSON.stringify({items: selected.length, truth_classes: Object.groupBy(reference.items, item => item.truth_class)}, (_key, value) => Array.isArray(value) && value[0]?.item_id ? value.length : value, 2)}\n`);
