#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildPackage, FROZEN, GENERATED_NAMES, sha256} from "./build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../..");
const productionInput = path.join(root, ".ai/task/research-route-familiarity-runtime-expansion-v1/production-input");
const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "route-familiarity-runtime-expansion-v1-"));
const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
const cmp = (left, right) => left < right ? -1 : left > right ? 1 : 0;
const exactKeys = (value, expected, label) => assert.deepEqual(Object.keys(value).sort(cmp), [...expected].sort(cmp), `${label}: key leakage`);
const normalize = value => value.replace(/\\[nrt]/gu, " ").replace(/\s+/gu, " ").trim();
const canonical = value => value === null || typeof value !== "object" ? JSON.stringify(value) : Array.isArray(value) ? `[${value.map(canonical).join(",")}]` : `{${Object.keys(value).sort((a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b))).map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
const canonicalIdentity = value => sha256(Buffer.from(canonical(value), "utf8"));

function independentPathSpans(text) {
  const spans = [];
  const isDelimiter = char => char === undefined || /[\s"'`<>\[\],;]/u.test(char);
  const balanced = value => {
    const stack = [];
    const partners = {")": "(", "}": "{"};
    for (const char of value) {
      if (char === "(" || char === "{") stack.push(char);
      else if ((char === ")" || char === "}") && stack.pop() !== partners[char]) return false;
    }
    return stack.length === 0;
  };
  const validNeutral = (offset, token) => {
    const rules = [
      ["<MAIN_GAME_ROOT>", /^(?:game\/modules\/tome)(?:\/|$)/u],
      ["<DLC_ROOT>", /^(?:ashes-urhrok|cults|game\/dlcs|orcs)(?:\/|$)/u]
    ];
    for (const [marker, suffixRule] of rules) {
      if (!text.slice(0, offset).endsWith(marker)) continue;
      const suffix = token.slice(1).replace(/\\/gu, "/");
      return suffixRule.test(suffix) && suffix.split("/").every(component => component && component !== "." && component !== ".." && balanced(component));
    }
    return false;
  };
  let cursor = 0;
  while (cursor < text.length) {
    if (/^https?:\/\//iu.test(text.slice(cursor))) {
      let urlEnd = cursor;
      while (!isDelimiter(text[urlEnd])) urlEnd += 1;
      cursor = urlEnd;
      continue;
    }
    const previous = cursor === 0 ? "" : text[cursor - 1];
    const boundary = !previous || !/[\p{L}\p{N}_\\/]/u.test(previous);
    const unc = (text.startsWith("\\\\", cursor) || text.startsWith("//", cursor)) && boundary;
    const drive = /[A-Za-z]/u.test(text[cursor] ?? "") && text[cursor + 1] === ":" && /[\\/]/u.test(text[cursor + 2] ?? "") && boundary;
    const posix = text[cursor] === "/" && text[cursor + 1] !== "/" && boundary;
    if (!unc && !drive && !posix) { cursor += 1; continue; }
    let end = cursor + (unc ? 2 : drive ? 3 : 1);
    while (!isDelimiter(text[end])) end += 1;
    while (end > cursor && /[.;!?]/u.test(text[end - 1])) end -= 1;
    for (const [open, close] of [["(", ")"], ["{", "}"]]) {
      const segment = text.slice(cursor, end);
      let imbalance = [...segment].filter(char => char === close).length - [...segment].filter(char => char === open).length;
      while (imbalance > 0 && text[end - 1] === close) { end -= 1; imbalance -= 1; }
    }
    const token = text.slice(cursor, end);
    const first = token.slice(1).split("/")[0];
    const syntaxLike = posix && (!/^[\p{L}\p{N}._-]/u.test(first) || !balanced(first) || (!token.slice(1).includes("/") && /^[A-Za-z_][A-Za-z0-9_]*\(.*\)$/u.test(first)));
    if (syntaxLike) { cursor += 1; continue; }
    if (posix && validNeutral(cursor, token)) { cursor = end; continue; }
    spans.push({start: cursor, end, token});
    cursor = end;
  }
  return spans;
}

function independentReplacement(token) {
  const slash = token.replace(/\\/gu, "/");
  const engineDlc = slash.indexOf("/game/dlcs/");
  if (engineDlc >= 0) return `<DLC_ROOT>${slash.slice(engineDlc)}`;
  for (const rule of [{part: "/tome4-dlcs", marker: "<DLC_ROOT>"}, {part: "/t-engine4", marker: "<MAIN_GAME_ROOT>"}]) {
    const found = slash.indexOf(rule.part);
    const end = found + rule.part.length;
    if (found >= 0 && (end === slash.length || slash[end] === "/")) return rule.marker + slash.slice(end);
  }
  return null;
}

assert.equal(independentPathSpans("punctuation(/srv/private/file.lua),tail").length, 1);
assert.equal(independentPathSpans("(/srv/private/a(b).lua)").map(item => item.token)[0], "/srv/private/a(b).lua");
assert.equal(independentPathSpans("/home/user/dir(1)/t-engine4/game/modules/tome/data/file.lua").length, 1);
assert.equal(independentPathSpans("/home/user/dir{1}/t-engine4/game/modules/tome/data/file.lua").length, 1);
assert.equal(independentPathSpans("/toBase(/home/user/t-engine4/game/modules/tome/data/file.lua)").map(item => item.token)[0], "/home/user/t-engine4/game/modules/tome/data/file.lua");
assert.equal(independentPathSpans("/#/home/user/t-engine4/game/modules/tome/data/file.lua").map(item => item.token)[0], "/home/user/t-engine4/game/modules/tome/data/file.lua");
assert.equal(independentPathSpans("C:\\private\\file.lua C:/private/file.lua \\\\server\\share\\file.lua //server/share/file.lua").length, 4);
assert.equal(independentPathSpans("/single-file").length, 1);
assert.equal(independentPathSpans("https://example.invalid/home/user/file.lua?q=/srv/private/file.lua").length, 0);
assert.equal(independentPathSpans("<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua <DLC_ROOT>/game/dlcs/a.lua").length, 0);
assert.equal(independentPathSpans("<DLC_ROOT>/home/user/tome4-dlcs/cults/data/a.lua").length, 1);
assert.equal(independentPathSpans("Lua /on_merge() and markup /# remain").length, 0);
assert.equal(independentReplacement("/srv/private/file.lua"), null);
assert.equal(independentReplacement("C:/work/t-engine4/game/modules/tome/data/file.lua"), "<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua");
assert.equal(independentReplacement("C:/work/tome4-dlcs/cults/data/file.lua"), "<DLC_ROOT>/cults/data/file.lua");

function independentlySanitize(raw, fixedSourceValue) {
  const pathSpans = independentPathSpans(raw);
  const operations = pathSpans.map(span => ({...span, replacement: independentReplacement(span.token), kind: "path"}));
  assert.equal(operations.every(operation => operation.replacement !== null), true, "independent sanitizer found unknown absolute path");
  const commit = /^(?:commit:)?([0-9a-f]{40})$/u.exec(fixedSourceValue)?.[1] ?? null;
  if (commit !== null) {
    let offset = 0;
    while ((offset = raw.indexOf(commit, offset)) !== -1) {
      operations.push({start: offset, end: offset + commit.length, replacement: "<FIXED_SOURCE_COMMIT>", kind: "commit"});
      offset += commit.length;
    }
  }
  operations.sort((left, right) => left.start - right.start);
  for (let index = 1; index < operations.length; index += 1) assert.ok(operations[index - 1].end <= operations[index].start, "replacement overlap");
  let rawCursor = 0;
  let sanitized = "";
  const pathUntouched = [];
  for (const operation of operations) {
    const rawGap = raw.slice(rawCursor, operation.start);
    sanitized += rawGap + operation.replacement;
    rawCursor = operation.end;
  }
  sanitized += raw.slice(rawCursor);
  assert.equal(independentPathSpans(sanitized).length, 0, "independent sanitizer left an absolute path");
  let pathCursor = 0;
  for (const span of pathSpans) { pathUntouched.push(raw.slice(pathCursor, span.start)); pathCursor = span.end; }
  pathUntouched.push(raw.slice(pathCursor));
  return {sanitized, pathOccurrences: pathSpans.length, commitOccurrences: operations.filter(operation => operation.kind === "commit").length, untouchedTextSha256: sha256(pathUntouched.join("\0"))};
}

function independentRules(context, internalValues) {
  const rules = [];
  if (internalValues.some(value => context.includes(value))) rules.push("INTERNAL_VALUE_SUBSTRING");
  if (/(?:\bRFR-\d{4}\b|\b(?:task|revision|dispatch|review)[_-]id\b|\b(?:review|senior-audit)-\d{2}\b)/iu.test(context)) rules.push("TYPED_TASK_OR_REVIEW_ID");
  if (/(?:already[- ]accepted|already reviewed|reviewed once|review correctly flagged|senior[- ]audit|senior scope calibration|adjudicat)/iu.test(context)) rules.push("REVIEW_OR_ADJUDICATION_HISTORY");
  if (/(?:\bout of scope\b|\bthis revision\b|\bnot part of this candidate\b)/iu.test(context)) rules.push("SCOPE_HISTORY_MARKER");
  return rules;
}

function cellCounts(items, field) {
  const result = {};
  for (const value of [...new Set(items.map(item => item[field]))].sort(cmp)) {
    const selected = items.filter(item => item[field] === value);
    result[value] = {tasks: new Set(selected.map(item => item.task_id)).size, rows: selected.length};
  }
  return result;
}

function independentTerminalSelection(snapshot, excludedTaskIds) {
  assert.ok(Array.isArray(snapshot?.tasks), "snapshot tasks missing");
  const selected = [];
  const taskIds = new Set();
  for (const task of snapshot.tasks) {
    assert.equal(typeof task.task_id, "string"); assert.ok(task.task_id.length > 0);
    assert.equal(taskIds.has(task.task_id), false, `${task.task_id}: duplicate snapshot task`);
    taskIds.add(task.task_id);
    if (excludedTaskIds.has(task.task_id)) continue;
    assert.ok(Array.isArray(task.dispatches), `${task.task_id}: dispatches missing`);
    const eligible = task.dispatches.flatMap((dispatch, snapshotIndex) =>
      typeof dispatch.role === "string" && dispatch.role.toUpperCase() === "REVIEWER" && dispatch.purpose === "translation_contextual_v1" && dispatch.input_path
        ? [{task_id: task.task_id, dispatch_id: dispatch.dispatch_id, role: "REVIEWER", purpose: dispatch.purpose, cycle: dispatch.cycle, lifecycle: dispatch.lifecycle, logical_path: dispatch.input_path, sha256: dispatch.input_fingerprint?.sha256, size_bytes: dispatch.input_fingerprint?.size_bytes, candidate_identity: dispatch.candidate_identity, snapshot_index: snapshotIndex}]
        : []);
    const finite = eligible.filter(dispatch => Number.isFinite(dispatch.cycle));
    if (finite.length) {
      const lastCycle = Math.max(...finite.map(dispatch => dispatch.cycle));
      selected.push(...finite.filter(dispatch => dispatch.cycle === lastCycle));
    } else if (eligible.length) {
      selected.push(eligible.filter(dispatch => !(typeof dispatch.lifecycle === "string" && dispatch.lifecycle.includes("transport_error"))).at(-1) ?? eligible.at(-1));
    }
  }
  return selected.sort((left, right) => cmp(left.task_id, right.task_id) || left.snapshot_index - right.snapshot_index);
}

function independentProfile(taskId) {
  if (taskId.includes("-ui-logs-")) return "ui-log";
  if (taskId.includes("-dialogue-")) return "dialogue";
  if (taskId.includes("p2-tome-texts")) return "unknown-text";
  if (/(?:-mechanics-|-status-|-condition-|-random-control-|-args-order-|-format-|-markup-)/u.test(taskId)) return "mechanics";
  throw new Error(`${taskId}: independently unclassified profile`);
}

const independentCategory = profile => profile === "mechanics" || profile === "ui-log" ? "Runtime-focused" : profile === "dialogue" ? "Dialogue" : "Unknown-text";

function independentRouteCell(taskId) {
  if (taskId.includes("p2-tome-texts")) return "H2";
  if (/^p1-b[234]-/u.test(taskId)) return "H3";
  if (/^p1-b[5-8]-/u.test(taskId) || /^p2-cults-status-b(?:1|3)-/u.test(taskId)) return "H4";
  return "H1";
}

function assertSafeLogicalPath(value) {
  assert.equal(typeof value, "string"); assert.ok(value.length > 0);
  assert.equal(value.includes("\0"), false);
  assert.equal(path.posix.isAbsolute(value), false);
  assert.equal(path.posix.normalize(value), value);
  assert.notEqual(value, ".."); assert.equal(value.startsWith("../"), false);
}

try {
  buildPackage({root, out: temporaryDirectory, productionInput: ".ai/task/research-route-familiarity-runtime-expansion-v1/production-input"});
  for (const name of GENERATED_NAMES) {
    const expected = fs.readFileSync(path.join(here, name));
    const rebuilt = fs.readFileSync(path.join(temporaryDirectory, name));
    assert.deepEqual(rebuilt, expected, `${name}: byte rebuild differs`);
    JSON.parse(expected.toString("utf8"));
  }
  const registry = readJson(path.join(here, GENERATED_NAMES[0]));
  const presentation = readJson(path.join(here, GENERATED_NAMES[1]));
  const report = readJson(path.join(here, GENERATED_NAMES[2]));
  const experiment = readJson(path.join(here, GENERATED_NAMES[3]));
  assert.equal(report.status, "PASS_ZERO_INFERENCE_FREEZE_GATES");
  assert.equal(experiment.status, "FROZEN_ZERO_INFERENCE_EXPLORATORY_POOL");
  for (const [name, [logicalPath, expectedHash]] of Object.entries(FROZEN.inputs)) {
    assert.equal(sha256(fs.readFileSync(path.join(root, logicalPath))), expectedHash, `${name}: frozen input hash`);
    assert.equal(report.frozen_input_hashes[name], expectedHash, `${name}: report input hash`);
  }
  const snapshot = readJson(path.join(root, FROZEN.inputs.provenance_snapshot[0]));
  const membership = readJson(path.join(root, FROZEN.inputs.canonical_membership[0]));
  assert.ok(Array.isArray(membership.items), "canonical membership items missing");
  const canonicalTaskIds = new Set();
  for (const item of membership.items) {
    assert.equal(typeof item.task_id, "string"); assert.ok(item.task_id.length > 0);
    canonicalTaskIds.add(item.task_id);
  }
  const independentlySelected = independentTerminalSelection(snapshot, canonicalTaskIds);
  assert.equal(independentlySelected.length, FROZEN.terminal_manifest.count, "independent terminal selection count");
  const selectedByPath = new Map();
  for (const selected of independentlySelected) {
    assertSafeLogicalPath(selected.logical_path);
    assert.equal(typeof selected.dispatch_id, "string"); assert.ok(selected.dispatch_id.length > 0);
    assert.match(selected.sha256 ?? "", /^[0-9a-f]{64}$/u);
    assert.ok(Number.isInteger(selected.size_bytes) && selected.size_bytes > 0);
    assert.match(selected.candidate_identity ?? "", /^[0-9a-f]{64}$/u);
    assert.equal(selectedByPath.has(selected.logical_path), false, `${selected.logical_path}: duplicate selected path`);
    selectedByPath.set(selected.logical_path, selected);
  }
  assert.equal(registry.terminal_input_manifest.records.length, independentlySelected.length);
  for (const terminal of registry.terminal_input_manifest.records) {
    const selected = selectedByPath.get(terminal.logical_path);
    assert.ok(selected, `${terminal.logical_path}: registry terminal absent from independent selection`);
    for (const field of ["task_id", "dispatch_id", "logical_path", "sha256", "size_bytes", "candidate_identity"]) assert.equal(terminal[field], selected[field], `${terminal.logical_path}: independently selected ${field} drift`);
  }
  assert.deepEqual(registry.counts, FROZEN.counts);
  assert.deepEqual(registry.presentation_counts, FROZEN.presentation_counts);
  assert.deepEqual(registry.order_digests, FROZEN.order_digests);
  assert.deepEqual({count: registry.terminal_input_manifest.count, bytes: registry.terminal_input_manifest.bytes, manifest_sha256: registry.terminal_input_manifest.manifest_sha256}, FROZEN.terminal_manifest);

  const rawRows = new Map();
  let manifestCanonical = "";
  let manifestBytes = 0;
  let terminalIdentityChecks = 0;
  let terminalFingerprintChecks = 0;
  let typedEnvelopeChecks = 0;
  let orderedRowChecks = 0;
  let independentlyModernEnvelopes = 0;
  let independentlyLegacyEnvelopes = 0;
  const fixedSourceFields = {fixed_source_identity: 0, fixed_source_commit: 0};
  let emptyTerminologySnapshots = 0;
  for (const terminal of registry.terminal_input_manifest.records) {
    const bytes = fs.readFileSync(path.join(productionInput, terminal.logical_path));
    assert.equal(sha256(bytes), terminal.sha256, "independent terminal fingerprint hash");
    assert.equal(bytes.length, terminal.size_bytes, "independent terminal fingerprint size");
    terminalFingerprintChecks += 1;
    manifestCanonical += `${terminal.logical_path}\0${terminal.sha256}\0${terminal.size_bytes}\n`;
    manifestBytes += bytes.length;
    const envelope = JSON.parse(bytes.toString("utf8"));
    const modern = Object.hasOwn(envelope, "payload");
    if (modern) independentlyModernEnvelopes += 1; else independentlyLegacyEnvelopes += 1;
    assert.equal(terminal.envelope_container, modern ? "modern" : "legacy", "recorded envelope container drift");
    if (modern) {
      exactKeys(envelope, ["candidate_identity", "payload"], "modern envelope");
      assert.equal(envelope.candidate_identity, terminal.candidate_identity, "outer/dispatch identity drift");
    }
    const payload = modern ? envelope.payload : envelope;
    const fixedKeys = ["fixed_source_identity", "fixed_source_commit"].filter(key => Object.hasOwn(payload, key));
    assert.equal(fixedKeys.length, 1, "fixed-source field cardinality");
    assert.equal(terminal.fixed_source_field, fixedKeys[0], "recorded fixed-source field drift");
    exactKeys(payload, ["bounded_context", "contract", fixedKeys[0], "ordered_revision_keys", "rendered_briefing", "terminology_snapshot", "translation_snapshot"], "typed payload");
    assert.equal(payload.contract, "translation_contextual_v1");
    assert.equal(typeof payload[fixedKeys[0]], "string"); assert.ok(payload[fixedKeys[0]].length > 0);
    assert.equal(typeof payload.terminology_snapshot, "string");
    assert.equal(typeof payload.rendered_briefing, "string"); assert.ok(payload.rendered_briefing.length > 0);
    const independentlyCanonicalIdentity = canonicalIdentity(payload);
    assert.equal(independentlyCanonicalIdentity, terminal.candidate_identity, "canonical dispatch identity drift");
    assert.equal(terminal.canonical_identity, terminal.candidate_identity, "recorded canonical identity drift");
    terminalIdentityChecks += 1;
    typedEnvelopeChecks += 1;
    fixedSourceFields[fixedKeys[0]] += 1;
    if (payload.terminology_snapshot.length === 0) emptyTerminologySnapshots += 1;
    assert.ok(Array.isArray(payload.ordered_revision_keys) && payload.ordered_revision_keys.length > 0);
    assert.equal(payload.translation_snapshot.length, payload.ordered_revision_keys.length);
    assert.equal(payload.bounded_context.length, payload.ordered_revision_keys.length);
    for (let index = 0; index < payload.ordered_revision_keys.length; index += 1) {
      const revision = payload.ordered_revision_keys[index];
      const translation = payload.translation_snapshot[index];
      const bounded = payload.bounded_context[index];
      assert.equal(typeof revision, "string"); assert.ok(revision.length > 0);
      exactKeys(translation, ["revision_key", "source", "target"], "translation row");
      exactKeys(bounded, ["context", "revision_key"], "context row");
      assert.equal(translation.revision_key, revision); assert.equal(bounded.revision_key, revision);
      for (const value of [translation.source, translation.target, bounded.context]) { assert.equal(typeof value, "string"); assert.ok(value.length > 0); }
      const rowKey = `${terminal.task_id}\0${revision}`;
      assert.equal(rawRows.has(rowKey), false, `${rowKey}: duplicate independent raw row`);
      rawRows.set(rowKey, {source: translation.source, target: translation.target, context: bounded.context, fixedSourceValue: payload[fixedKeys[0]]});
      orderedRowChecks += 1;
    }
  }
  assert.equal(manifestBytes, FROZEN.terminal_manifest.bytes);
  assert.equal(sha256(manifestCanonical), FROZEN.terminal_manifest.manifest_sha256);

  const internalValues = [];
  for (const binding of registry.items) for (const value of [binding.task_id, binding.revision_key, binding.terminal_input.logical_path, binding.terminal_input.sha256, binding.terminal_input.dispatch_id, binding.terminal_input.candidate_identity]) if (value && !internalValues.includes(value)) internalValues.push(value);
  assert.equal(rawRows.size, 156, "independently parsed row count");
  const independentlySanitizedById = new Map();
  let pathRows = 0; let pathOccurrences = 0; let commitRows = 0; let commitOccurrences = 0;
  const identities = []; const sources = []; const targets = []; const contexts = [];
  for (const binding of registry.items) {
    const selected = selectedByPath.get(binding.terminal_input.logical_path);
    assert.ok(selected, `${binding.neutral_id}: row terminal absent from independent selection`);
    assert.equal(binding.task_id, selected.task_id, `${binding.neutral_id}: row task_id drift`);
    for (const field of ["dispatch_id", "logical_path", "sha256", "size_bytes", "candidate_identity"]) assert.equal(binding.terminal_input[field], selected[field], `${binding.neutral_id}: row terminal ${field} drift`);
    const raw = rawRows.get(`${binding.task_id}\0${binding.revision_key}`);
    assert.ok(raw, "independent raw binding missing");
    assert.equal(sha256(raw.source), binding.source_sha256);
    assert.equal(sha256(raw.target), binding.target_sha256);
    assert.equal(sha256(raw.context), binding.raw_context_sha256);
    assert.equal(Buffer.byteLength(raw.context, "utf8"), binding.raw_context_size_bytes);
    const checked = independentlySanitize(raw.context, raw.fixedSourceValue);
    independentlySanitizedById.set(binding.neutral_id, checked.sanitized);
    assert.equal(sha256(checked.sanitized), binding.sanitized_context_sha256);
    assert.equal(Buffer.byteLength(checked.sanitized, "utf8"), binding.sanitized_context_size_bytes);
    assert.equal(checked.pathOccurrences, binding.path_redaction_occurrences);
    assert.equal(checked.commitOccurrences, binding.commit_neutralization_occurrences);
    assert.equal(checked.untouchedTextSha256, binding.untouched_text_sha256);
    if (checked.pathOccurrences) pathRows += 1; pathOccurrences += checked.pathOccurrences;
    if (checked.commitOccurrences) commitRows += 1; commitOccurrences += checked.commitOccurrences;
    const rules = independentRules(raw.context, internalValues);
    assert.deepEqual(rules, binding.matched_hygiene_rule_ids);
    assert.equal(binding.hygiene_disposition, rules.length ? "CONTEXT_META_PROVENANCE_EXCLUDED" : "MODEL_FACING");
    const derivedProfile = independentProfile(binding.task_id);
    assert.equal(binding.profile, derivedProfile, `${binding.task_id}: independent profile drift`);
    assert.equal(binding.category, independentCategory(derivedProfile), `${binding.task_id}: independent category drift`);
    assert.equal(binding.historical_route_cell, independentRouteCell(binding.task_id), `${binding.task_id}: independent H-cell drift`);
    identities.push(`${binding.task_id}\0${binding.revision_key}`); sources.push(raw.source); targets.push(raw.target); contexts.push(raw.context);
  }
  assert.deepEqual({rows: pathRows, occurrences: pathOccurrences}, {rows: 31, occurrences: 52});
  assert.deepEqual({rows: commitRows, occurrences: commitOccurrences}, {rows: 15, occurrences: 15});
  const excluded = registry.items.filter(item => item.hygiene_disposition !== "MODEL_FACING").map(item => item.neutral_id);
  assert.deepEqual(excluded, FROZEN.excluded_neutral_ids);

  const retainedBindings = registry.items.filter(item => item.hygiene_disposition === "MODEL_FACING");
  assert.equal(presentation.items.length, 145); assert.equal(new Set(presentation.items.map(item => item.neutral_id)).size, 145);
  assert.deepEqual(presentation.items.map(item => item.neutral_id), retainedBindings.map(item => item.neutral_id));
  exactKeys(presentation, ["counts", "items", "schema_version", "status"], "complete presentation");
  for (let index = 0; index < presentation.items.length; index += 1) {
    const item = presentation.items[index]; const binding = retainedBindings[index];
    exactKeys(item, ["neutral_id", "category", "profile", "source", "target", "bounded_fixed_context"], `presentation[${index}]`);
    assert.equal(sha256(item.source), binding.source_sha256); assert.equal(sha256(item.target), binding.target_sha256); assert.equal(sha256(item.bounded_fixed_context), binding.sanitized_context_sha256);
    assert.equal(item.bounded_fixed_context, independentlySanitizedById.get(binding.neutral_id), "independent sanitized presentation drift");
  }
  let presentationStringsScanned = 0;
  let presentationHygiene = true;
  const independentlyScanPresentation = (value, parentKey = null, kind = "value") => {
    if (typeof value === "string") {
      presentationStringsScanned += 1;
      const noInternal = !internalValues.some(internal => value.includes(internal));
      const noMeta = kind === "value" && parentKey === "neutral_id" || !/(?:\bRFR-\d{4}\b|\b(?:task|revision|dispatch|review)[_-]id\b|\b(?:review|senior-audit)-\d{2}\b|already[- ]accepted|already reviewed|reviewed once|review correctly flagged|senior scope calibration|adjudicat|\bout of scope\b|\bthis revision\b)/iu.test(value);
      const noHash = !/(?<![0-9a-f])[0-9a-f]{40,}(?![0-9a-f])/iu.test(value);
      const noModel = !/(?:\bprovider\b|\bmodel(?:_id)?\b|\bagent(?:_id)?\b|openai|anthropic|gemini|gpt-|claude|qwen)/iu.test(value);
      const noPath = independentPathSpans(value).length === 0;
      presentationHygiene &&= noInternal && noMeta && noHash && noModel && noPath;
      assert.equal(noInternal, true, `${parentKey ?? kind}: internal substring`); assert.equal(noMeta, true, `${parentKey ?? kind}: meta provenance`); assert.equal(noHash, true, `${parentKey ?? kind}: hash provenance`); assert.equal(noModel, true, `${parentKey ?? kind}: model provenance`); assert.equal(noPath, true, `${parentKey ?? kind}: residual absolute path`);
      return;
    }
    if (Array.isArray(value)) { for (const child of value) independentlyScanPresentation(child); return; }
    if (value && typeof value === "object") for (const [key, child] of Object.entries(value)) {
      independentlyScanPresentation(key, null, "key");
      independentlyScanPresentation(child, key, "value");
    }
  };
  independentlyScanPresentation(presentation);
  assert.equal(presentationStringsScanned, report.presentation_hygiene_scan.recursive_key_value_strings, "recursive presentation scan count");
  const independentMarkerCounts = {
    MAIN_GAME_ROOT: presentation.items.reduce((sum, item) => sum + item.bounded_fixed_context.split("<MAIN_GAME_ROOT>").length - 1, 0),
    DLC_ROOT: presentation.items.reduce((sum, item) => sum + item.bounded_fixed_context.split("<DLC_ROOT>").length - 1, 0)
  };
  assert.deepEqual(independentMarkerCounts, FROZEN.presentation_marker_counts, "independent neutral-root marker counts");
  assert.equal(presentation.items.some(item => item.bounded_fixed_context.includes("<DLC_ROOT>/tome4-dlcs/")), false, "DLC aggregation segment survived sanitation");
  const independentSanitationSummary = {path_rows: pathRows, path_occurrences: pathOccurrences, commit_rows: commitRows, commit_occurrences: commitOccurrences, presentation_neutral_root_markers: independentMarkerCounts, dlc_aggregation_segment_absorbed: true};
  assert.deepEqual(report.sanitation_summary, independentSanitationSummary);
  assert.deepEqual(experiment.sanitation_summary, independentSanitationSummary);
  for (const id of ["RFR-0077", "RFR-0078", "RFR-0156"]) assert.equal(presentation.items.some(item => item.neutral_id === id), false, `${id}: real regression`);

  const independentCounts = {
    tasks: new Set(registry.items.map(item => item.task_id)).size, rows: registry.items.length,
    modern_envelopes: independentlyModernEnvelopes,
    legacy_envelopes: independentlyLegacyEnvelopes,
    fixed_source_fields: fixedSourceFields,
    terminology_snapshot: {empty_strings: emptyTerminologySnapshots, non_empty_strings: registry.terminal_input_manifest.records.length - emptyTerminologySnapshots},
    profiles: cellCounts(registry.items, "profile"), categories: cellCounts(registry.items, "category"), historical_route_cells: cellCounts(registry.items, "historical_route_cell"),
    path_redaction: {rows: pathRows, occurrences: pathOccurrences}, commit_neutralization: {rows: commitRows, occurrences: commitOccurrences},
    dispositions: {MODEL_FACING: retainedBindings.length, CONTEXT_META_PROVENANCE_EXCLUDED: excluded.length}
  };
  const independentPresentationCounts = {tasks: new Set(retainedBindings.map(item => item.task_id)).size, rows: retainedBindings.length, profiles: cellCounts(retainedBindings, "profile"), categories: cellCounts(retainedBindings, "category"), historical_route_cells: cellCounts(retainedBindings, "historical_route_cell")};
  assert.deepEqual(independentCounts, FROZEN.counts); assert.deepEqual(independentPresentationCounts, FROZEN.presentation_counts);
  const digest = values => sha256(`${values.join("\n")}\n`);
  const independentOrderDigests = {identity: digest(identities), source: digest(sources), target: digest(targets), context: digest(contexts)};
  assert.deepEqual(independentOrderDigests, FROZEN.order_digests);
  assert.equal(new Set(identities).size, 156); assert.equal(new Set(sources.map(normalize)).size, 156); assert.equal(new Set(sources.map((source, index) => `${normalize(source)}\0${normalize(targets[index])}`)).size, 156);

  const oldQueue = readJson(path.join(root, FROZEN.inputs.old_120_queue[0]));
  const currentPool = readJson(path.join(root, FROZEN.inputs.current_439_candidates[0]));
  const overlap = pool => ({source: sources.filter(source => new Set(pool.items.map(item => normalize(item.source))).has(normalize(source))).length, pair: sources.filter((source, index) => new Set(pool.items.map(item => `${normalize(item.source)}\0${normalize(item.target)}`)).has(`${normalize(source)}\0${normalize(targets[index])}`)).length});
  const oldOverlap = overlap(oldQueue); const currentOverlap = overlap(currentPool);
  assert.deepEqual(oldOverlap, {source: 0, pair: 0}); assert.deepEqual(currentOverlap, {source: 0, pair: 0});

  const independentGates = {
    fingerprints_exact: terminalFingerprintChecks === 77 && independentlySelected.length === 77 && manifestBytes === FROZEN.terminal_manifest.bytes && sha256(manifestCanonical) === FROZEN.terminal_manifest.manifest_sha256,
    dispatch_envelope_identity_exact: terminalIdentityChecks === 77 && independentlySelected.length === 77 && registry.terminal_input_manifest.records.every(record => /^[0-9a-f]{64}$/u.test(record.candidate_identity)),
    envelope_schema_exact: typedEnvelopeChecks === 77 && orderedRowChecks === 156 && independentCounts.modern_envelopes === 76 && independentCounts.legacy_envelopes === 1 && fixedSourceFields.fixed_source_identity === 70 && fixedSourceFields.fixed_source_commit === 7 && emptyTerminologySnapshots === 1 && registry.terminal_input_manifest.records.length - emptyTerminologySnapshots === 76,
    ordered_bindings_exact: orderedRowChecks === 156 && canonical(independentOrderDigests) === canonical(FROZEN.order_digests),
    unique_identity_source_pair: new Set(identities).size === 156 && new Set(sources.map(normalize)).size === 156 && new Set(sources.map((source, index) => `${normalize(source)}\0${normalize(targets[index])}`)).size === 156,
    old_120_overlap_zero: oldOverlap.source === 0 && oldOverlap.pair === 0,
    current_439_overlap_zero: currentOverlap.source === 0 && currentOverlap.pair === 0,
    internal_counts_exact: canonical(independentCounts) === canonical(FROZEN.counts),
    presentation_counts_exact: canonical(independentPresentationCounts) === canonical(FROZEN.presentation_counts),
    meta_provenance_exclusions_exact: canonical(excluded) === canonical(FROZEN.excluded_neutral_ids),
    path_redaction_31_rows_52_occurrences: pathRows === 31 && pathOccurrences === 52,
    commit_neutralization_15_rows_15_occurrences: commitRows === 15 && commitOccurrences === 15,
    sanitized_presentation_hygiene: presentationHygiene && presentation.items.length === 145 && presentationStringsScanned === report.presentation_hygiene_scan.recursive_key_value_strings,
    zero_inference: report.model_calls === 0 && report.network_calls === 0 && experiment.model_calls === 0 && experiment.network_calls === 0
  };
  assert.deepEqual(report.gates, independentGates); assert.ok(Object.values(independentGates).every(Boolean));

  const actualHashes = Object.fromEntries(GENERATED_NAMES.map(name => [name, sha256(fs.readFileSync(path.join(here, name)))]));
  assert.deepEqual(actualHashes, FROZEN.output_hashes, "all four externally frozen output hashes");
  assert.deepEqual(report.generated_artifacts, Object.fromEntries(GENERATED_NAMES.slice(0, 2).map(name => [name, {sha256: actualHashes[name], size_bytes: fs.statSync(path.join(here, name)).size}])));
  assert.deepEqual(experiment.generated_artifacts, Object.fromEntries(GENERATED_NAMES.slice(0, 3).map(name => [name, {sha256: actualHashes[name], size_bytes: fs.statSync(path.join(here, name)).size}])));
  const fixture = fs.readFileSync(path.join(root, FROZEN.inputs.executor_fixture[0])); assert.equal(sha256(fixture), FROZEN.executor_fixture_sha256);
  process.stdout.write(`${JSON.stringify({status: "PASS", deterministic_outputs: GENERATED_NAMES, counts: registry.counts, presentation_counts: registry.presentation_counts, terminal_manifest: FROZEN.terminal_manifest, order_digests: registry.order_digests, output_hashes: actualHashes}, null, 2)}\n`);
} finally {
  const expectedPrefix = `${path.resolve(os.tmpdir())}${path.sep}route-familiarity-runtime-expansion-v1-`;
  const resolved = path.resolve(temporaryDirectory);
  if (!resolved.startsWith(expectedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolved, {recursive: true, force: true});
}
