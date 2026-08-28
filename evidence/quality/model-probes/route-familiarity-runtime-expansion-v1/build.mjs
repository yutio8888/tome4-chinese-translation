#!/usr/bin/env node

import crypto from "node:crypto";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");

export const GENERATED_NAMES = Object.freeze([
  "TERMINAL-IDENTITY-BINDING-REGISTRY.json",
  "FUTURE-MODEL-CANDIDATES.json",
  "BUILD-REPORT.json",
  "EXPERIMENT.json"
]);

const EXCLUDED_NEUTRAL_IDS = Object.freeze([
  "RFR-0019", "RFR-0021", "RFR-0076", "RFR-0077", "RFR-0078", "RFR-0113",
  "RFR-0131", "RFR-0134", "RFR-0137", "RFR-0139", "RFR-0156"
]);

export const FROZEN = Object.freeze({
  production_translation_commit: "1666481409f4c0d63d66e84659f6b6145d8d25d0",
  executor_fixture_sha256: "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7",
  inputs: {
    provenance_snapshot: ["evidence/quality/model-probes/paseo-provenance-snapshot-v1/SNAPSHOT.json", "b754183a9d1e0efa15cb1d3c16fa06a7f96f388e75707c7ba0e79f4a680f2eab"],
    canonical_membership: ["evidence/quality/model-probes/prospective-residual-audit-v3/CANONICAL-MEMBERSHIP.json", "477c0e97f59e4f29159ed7baa16b7ef5ddb4165cbe5785ad15b667eadfda2049"],
    old_120_queue: ["evidence/quality/model-probes/prospective-source-context-truth-audit-v1/AUDIT-QUEUE.json", "3f629d6eb9a7b3264582e7b860be7ac77cd038f3f8ac2df2ad9736fee64a2ebe"],
    current_439_candidates: ["evidence/quality/model-probes/prospective-context-defect-expansion-v1/FUTURE-MODEL-CANDIDATES.json", "dc11c6b71c208a4981e0934fcd09063cdc8416fc24b4983296840574a52d0b0e"],
    executor_fixture: ["evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua", "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7"]
  },
  terminal_manifest: {count: 77, bytes: 176318, manifest_sha256: "73b692e540419748e53d65b0511f93789961e5a10df30cadbf012fc81220fc34"},
  order_digests: {
    identity: "c7eea1b175a61f3589c06cb8cc18e8b99e899302cda865b36566d0e5283a6caa",
    source: "41e9461d3cd87f4f5b978b94a45903b935dff9aa71168ded0827eed80fbeccd0",
    target: "7e73c0f2544c66955ba888287ab1fca0b4a623c6d701063de8448c7790a53df1",
    context: "6381e3a167b5d55e4a464ee5d7801fe7e8c1a11c5cc7be028d2c8ef81e172606"
  },
  counts: {
    tasks: 77,
    rows: 156,
    modern_envelopes: 76,
    legacy_envelopes: 1,
    fixed_source_fields: {fixed_source_identity: 70, fixed_source_commit: 7},
    terminology_snapshot: {empty_strings: 1, non_empty_strings: 76},
    profiles: {mechanics: {tasks: 61, rows: 73}, "ui-log": {tasks: 7, rows: 7}, dialogue: {tasks: 7, rows: 61}, "unknown-text": {tasks: 2, rows: 15}},
    categories: {"Runtime-focused": {tasks: 68, rows: 80}, Dialogue: {tasks: 7, rows: 61}, "Unknown-text": {tasks: 2, rows: 15}},
    historical_route_cells: {H1: {tasks: 66, rows: 122}, H2: {tasks: 2, rows: 15}, H3: {tasks: 3, rows: 11}, H4: {tasks: 6, rows: 8}},
    path_redaction: {rows: 31, occurrences: 52},
    commit_neutralization: {rows: 15, occurrences: 15},
    dispositions: {MODEL_FACING: 145, CONTEXT_META_PROVENANCE_EXCLUDED: 11}
  },
  presentation_counts: {
    tasks: 66,
    rows: 145,
    profiles: {mechanics: {tasks: 51, rows: 63}, "ui-log": {tasks: 7, rows: 7}, dialogue: {tasks: 7, rows: 61}, "unknown-text": {tasks: 1, rows: 14}},
    categories: {"Runtime-focused": {tasks: 58, rows: 70}, Dialogue: {tasks: 7, rows: 61}, "Unknown-text": {tasks: 1, rows: 14}},
    historical_route_cells: {H1: {tasks: 56, rows: 112}, H2: {tasks: 1, rows: 14}, H3: {tasks: 3, rows: 11}, H4: {tasks: 6, rows: 8}}
  },
  presentation_marker_counts: {MAIN_GAME_ROOT: 9, DLC_ROOT: 43},
  excluded_neutral_ids: EXCLUDED_NEUTRAL_IDS,
  // These cover all four outputs externally. They are intentionally not embedded
  // in generated JSON, so no artifact depends on its own hash.
  output_hashes: {
    "TERMINAL-IDENTITY-BINDING-REGISTRY.json": "9cc58a068801a707be0eca32a2597493d8fb2b6d64e37914355ac9cd2552d436",
    "FUTURE-MODEL-CANDIDATES.json": "6e8b2a3b485418fca4bdb9d777f4a7a572f0f872efdb27905e52080a23e11084",
    "BUILD-REPORT.json": "a0eeb216c4412f0dbb0ef3fcef1302294c09ea0c757a771cc21e280fff1fda2c",
    "EXPERIMENT.json": "429ca530b95896e8e0f88021e88d8f9b33c292a96a5443b2ffb4526eb6e28eca"
  }
});

const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
export const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const recordFor = bytes => ({sha256: sha256(bytes), size_bytes: bytes.length});
export const compareCodepoints = (left, right) => left < right ? -1 : left > right ? 1 : 0;
const compareUtf8 = (left, right) => Buffer.compare(Buffer.from(left, "utf8"), Buffer.from(right, "utf8"));
const sortedKeys = value => Object.keys(value).sort(compareCodepoints);
const exactKeys = (value, expected, label) => {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: object required`);
  const actual = sortedKeys(value);
  const wanted = [...expected].sort(compareCodepoints);
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) throw new Error(`${label}: schema drift`);
};

export function canonicalJson(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  return `{${Object.keys(value).sort(compareUtf8).map(key => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
}

export const canonicalSha256 = value => sha256(Buffer.from(canonicalJson(value), "utf8"));

function parseArgs(argv) {
  const args = {root: defaultRoot, out: here, productionInput: ".ai/task/research-route-familiarity-runtime-expansion-v1/production-input"};
  const allowed = new Set(["--root", "--out", "--production-input"]);
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!allowed.has(flag) || !value) throw new Error("usage: node build.mjs [--root REPO] [--out DIR] [--production-input RELATIVE_ENTRY]");
    const key = flag === "--production-input" ? "productionInput" : flag.slice(2);
    args[key] = value;
  }
  if (path.isAbsolute(args.productionInput)) throw new Error("production input must use the relative read-only entry");
  args.root = path.resolve(args.root);
  args.out = path.resolve(args.out);
  return args;
}

function assertSafeRelative(value, label) {
  if (typeof value !== "string" || !value || value.includes("\0") || path.posix.isAbsolute(value) || path.posix.normalize(value) !== value || value === ".." || value.startsWith("../")) throw new Error(`${label}: unsafe relative path`);
}

function readPinned(root, name) {
  const [logicalPath, expected] = FROZEN.inputs[name];
  const bytes = fs.readFileSync(path.join(root, logicalPath));
  if (sha256(bytes) !== expected) throw new Error(`${name}: frozen input hash drift`);
  const value = logicalPath.endsWith(".json") ? JSON.parse(bytes.toString("utf8")) : null;
  return {logical_path: logicalPath, sha256: expected, size_bytes: bytes.length, value};
}

export function normalizeText(value) {
  if (typeof value !== "string") throw new Error("normalization requires string");
  return value.replace(/\\[nrt]/gu, " ").replace(/\s+/gu, " ").trim();
}

const isTransportError = lifecycle => typeof lifecycle === "string" && lifecycle.includes("transport_error");

export function selectTerminalDispatches(snapshot, excludedTaskIds) {
  if (!Array.isArray(snapshot?.tasks)) throw new Error("snapshot tasks missing");
  const selected = [];
  const seenTasks = new Set();
  for (const task of snapshot.tasks) {
    const taskId = task.task_id;
    if (typeof taskId !== "string" || !taskId) throw new Error("snapshot task_id malformed");
    if (seenTasks.has(taskId)) throw new Error(`${taskId}: duplicate snapshot task`);
    seenTasks.add(taskId);
    if (excludedTaskIds.has(taskId)) continue;
    if (!Array.isArray(task.dispatches)) throw new Error(`${taskId}: dispatches missing`);
    const eligible = [];
    for (let index = 0; index < task.dispatches.length; index += 1) {
      const dispatch = task.dispatches[index];
      const role = dispatch.role;
      const purpose = dispatch.purpose;
      const cycle = dispatch.cycle;
      const lifecycle = dispatch.lifecycle;
      const dispatchId = dispatch.dispatch_id;
      const inputPath = dispatch.input_path;
      const inputFingerprint = dispatch.input_fingerprint;
      const candidateIdentity = dispatch.candidate_identity;
      if (typeof role === "string" && role.toUpperCase() === "REVIEWER" && purpose === "translation_contextual_v1" && inputPath) {
        eligible.push({task_id: taskId, role: "REVIEWER", purpose, cycle, lifecycle, dispatch_id: dispatchId, input_path: inputPath, input_fingerprint: inputFingerprint, candidate_identity: candidateIdentity, snapshot_index: index});
      }
    }
    const finite = eligible.filter(dispatch => Number.isFinite(dispatch.cycle));
    let terminal = [];
    if (finite.length) {
      const maximum = Math.max(...finite.map(dispatch => dispatch.cycle));
      terminal = finite.filter(dispatch => dispatch.cycle === maximum);
    } else if (eligible.length) {
      terminal = [eligible.filter(dispatch => !isTransportError(dispatch.lifecycle)).at(-1) ?? eligible.at(-1)];
    }
    selected.push(...terminal);
  }
  return selected.sort((left, right) => compareCodepoints(left.task_id, right.task_id) || left.snapshot_index - right.snapshot_index);
}

const MODERN_TOP_KEYS = ["candidate_identity", "payload"];
const PAYLOAD_COMMON_KEYS = ["bounded_context", "contract", "ordered_revision_keys", "rendered_briefing", "terminology_snapshot", "translation_snapshot"];
const FIXED_SOURCE_KEYS = ["fixed_source_identity", "fixed_source_commit"];
const SHA256_RE = /^[0-9a-f]{64}$/u;

function validatePayload(payload, label) {
  const presentFixedKeys = FIXED_SOURCE_KEYS.filter(key => Object.hasOwn(payload ?? {}, key));
  if (presentFixedKeys.length !== 1) throw new Error(`${label}: exactly one fixed-source field required`);
  const fixedKey = presentFixedKeys[0];
  exactKeys(payload, [...PAYLOAD_COMMON_KEYS, fixedKey], label);
  if (payload.contract !== "translation_contextual_v1") throw new Error(`${label}: contract must be translation_contextual_v1`);
  if (typeof payload[fixedKey] !== "string" || payload[fixedKey].length === 0) throw new Error(`${label}: fixed-source binding must be a non-empty string`);
  if (typeof payload.terminology_snapshot !== "string") throw new Error(`${label}: terminology_snapshot must be a string`);
  if (typeof payload.rendered_briefing !== "string" || payload.rendered_briefing.length === 0) throw new Error(`${label}: rendered_briefing must be a non-empty string`);
  const ordered = payload.ordered_revision_keys;
  const translations = payload.translation_snapshot;
  const contexts = payload.bounded_context;
  if (!Array.isArray(ordered) || !Array.isArray(translations) || !Array.isArray(contexts) || ordered.length === 0 || ordered.length !== translations.length || ordered.length !== contexts.length) throw new Error(`${label}: ordered coverage malformed`);
  const revisions = new Set();
  const rows = [];
  for (let index = 0; index < ordered.length; index += 1) {
    const revisionKey = ordered[index];
    const translation = translations[index];
    const context = contexts[index];
    if (typeof revisionKey !== "string" || !revisionKey || revisions.has(revisionKey)) throw new Error(`${label}: duplicate or malformed ordered revision`);
    revisions.add(revisionKey);
    exactKeys(translation, ["revision_key", "source", "target"], `${label}.translation_snapshot[${index}]`);
    exactKeys(context, ["context", "revision_key"], `${label}.bounded_context[${index}]`);
    if (translation.revision_key !== revisionKey || context.revision_key !== revisionKey) throw new Error(`${label}: target/context/order drift`);
    for (const [name, value] of [["source", translation.source], ["target", translation.target], ["context", context.context]]) {
      if (typeof value !== "string" || value.length === 0) throw new Error(`${label}: ${name} must be a non-empty string`);
    }
    rows.push({revision_key: revisionKey, source: translation.source, target: translation.target, context: context.context});
  }
  return {fixed_key: fixedKey, fixed_value: payload[fixedKey], rows};
}

export function parseEnvelope(envelope, label, dispatchIdentity) {
  if (!SHA256_RE.test(dispatchIdentity ?? "")) throw new Error(`${label}: selected dispatch candidate_identity must be 64-hex`);
  if (Object.hasOwn(envelope ?? {}, "payload")) {
    exactKeys(envelope, MODERN_TOP_KEYS, `${label}.modern`);
    if (!SHA256_RE.test(envelope.candidate_identity ?? "")) throw new Error(`${label}: modern outer candidate_identity must be 64-hex`);
    const validated = validatePayload(envelope.payload, `${label}.payload`);
    const canonicalIdentity = canonicalSha256(envelope.payload);
    if (envelope.candidate_identity !== dispatchIdentity || canonicalIdentity !== dispatchIdentity) throw new Error(`${label}: modern candidate identity drift`);
    return {container: "modern", rows: validated.rows, fixed_key: validated.fixed_key, fixed_value: validated.fixed_value, canonical_identity: canonicalIdentity};
  }
  const validated = validatePayload(envelope, `${label}.legacy`);
  const canonicalIdentity = canonicalSha256(envelope);
  if (canonicalIdentity !== dispatchIdentity) throw new Error(`${label}: legacy candidate identity drift`);
  return {container: "legacy", rows: validated.rows, fixed_key: validated.fixed_key, fixed_value: validated.fixed_value, canonical_identity: canonicalIdentity};
}

export function readValidatedEnvelope(dispatch, terminalReader) {
  assertSafeRelative(dispatch.input_path, "terminal input");
  const fingerprint = dispatch.input_fingerprint;
  exactKeys(fingerprint, ["sha256", "size_bytes"], `${dispatch.task_id}: input fingerprint`);
  if (!SHA256_RE.test(fingerprint.sha256 ?? "") || !Number.isInteger(fingerprint.size_bytes) || fingerprint.size_bytes < 1) throw new Error(`${dispatch.task_id}: incomplete input fingerprint`);
  const bytes = terminalReader(dispatch.input_path);
  if (!Buffer.isBuffer(bytes) || bytes.length !== fingerprint.size_bytes || sha256(bytes) !== fingerprint.sha256) throw new Error(`${dispatch.task_id}: terminal fingerprint drift`);
  let envelope;
  try {
    envelope = JSON.parse(bytes.toString("utf8"));
  } catch {
    throw new Error(`${dispatch.task_id}: malformed envelope JSON`);
  }
  return {bytes, parsed: parseEnvelope(envelope, dispatch.task_id, dispatch.candidate_identity)};
}

const URL_RE = /https?:\/\/[^\s"'`<>\[\],;]+/giu;
const PATH_DELIMITER_RE = /[\s"'`<>\[\],;]/u;
const TRAILING_PATH_PUNCTUATION_RE = /[.;!?]+$/u;
const NEUTRAL_ROOT_PREFIXES = Object.freeze({
  "<MAIN_GAME_ROOT>": ["game/modules/tome"],
  "<DLC_ROOT>": ["ashes-urhrok", "cults", "game/dlcs", "orcs"]
});

function urlSpans(value) {
  const spans = [];
  URL_RE.lastIndex = 0;
  for (const match of value.matchAll(URL_RE)) spans.push([match.index, match.index + match[0].length]);
  return spans;
}

function validPathBoundary(value, offset) {
  const before = offset === 0 ? "" : value[offset - 1];
  return !before || !/[\p{L}\p{N}_\\/]/u.test(before);
}

function trimCandidate(value, start, rawEnd) {
  let end = rawEnd;
  while (end > start && TRAILING_PATH_PUNCTUATION_RE.test(value[end - 1])) end -= 1;
  for (const [open, close] of [["(", ")"], ["{", "}"]]) {
    let balance = 0;
    for (const char of value.slice(start, end)) {
      if (char === open) balance += 1;
      if (char === close) balance -= 1;
    }
    while (balance < 0 && value[end - 1] === close) { end -= 1; balance += 1; }
  }
  return end;
}

function candidateEnd(value, start) {
  let end = start;
  while (end < value.length && !PATH_DELIMITER_RE.test(value[end])) end += 1;
  return trimCandidate(value, start, end);
}

function balancedComponent(component) {
  for (const [open, close] of [["(", ")"], ["{", "}"]]) {
    let balance = 0;
    for (const char of component) {
      if (char === open) balance += 1;
      if (char === close && --balance < 0) return false;
    }
    if (balance !== 0) return false;
  }
  return true;
}

function validPosixCandidate(token) {
  const firstComponent = token.slice(1).split("/")[0];
  if (!/^[\p{L}\p{N}._-]/u.test(firstComponent) || !balancedComponent(firstComponent)) return false;
  if (!token.slice(1).includes("/") && /^[A-Za-z_][A-Za-z0-9_]*\(.*\)$/u.test(firstComponent)) return false;
  return true;
}

function validNeutralMarkerPath(value, slashOffset, token) {
  for (const [marker, prefixes] of Object.entries(NEUTRAL_ROOT_PREFIXES)) {
    if (!value.slice(0, slashOffset).endsWith(marker)) continue;
    const suffix = token.slice(1).replace(/\\/gu, "/");
    if (!suffix || suffix.split("/").some(component => !component || component === "." || component === ".." || !balancedComponent(component))) return false;
    return prefixes.some(prefix => suffix === prefix || suffix.startsWith(`${prefix}/`));
  }
  return false;
}

export function findAbsolutePaths(value) {
  if (typeof value !== "string") throw new Error("path scan requires string");
  const spans = urlSpans(value);
  const found = [];
  let cursor = 0;
  while (cursor < value.length) {
    const urlSpan = spans.find(([start, end]) => cursor >= start && cursor < end);
    if (urlSpan) { cursor = urlSpan[1]; continue; }
    const unc = value.startsWith("\\\\", cursor) || value.startsWith("//", cursor);
    const drive = /^[A-Za-z]:[\\/]/u.test(value.slice(cursor, cursor + 3));
    const posix = value[cursor] === "/" && !value.startsWith("//", cursor);
    if ((!unc && !drive && !posix) || !validPathBoundary(value, cursor)) { cursor += 1; continue; }
    const end = candidateEnd(value, cursor);
    const token = value.slice(cursor, end);
    if (!token || (posix && !validPosixCandidate(token))) {
      // Rejected syntax-like prefixes can contain a later real path. Advancing
      // exactly one code unit guarantees that nested candidate is reconsidered.
      cursor += 1;
      continue;
    }
    if (posix && validNeutralMarkerPath(value, cursor, token)) { cursor = end; continue; }
    found.push({start: cursor, end, token});
    cursor = end;
  }
  return found;
}

function neutralizeAbsoluteToken(token) {
  const normalized = token.replace(/\\/gu, "/");
  const engineDlc = normalized.indexOf("/game/dlcs/");
  if (engineDlc !== -1) return `<DLC_ROOT>${normalized.slice(engineDlc)}`;
  for (const [needle, marker] of [["/tome4-dlcs", "<DLC_ROOT>"], ["/t-engine4", "<MAIN_GAME_ROOT>"]]) {
    const index = normalized.indexOf(needle);
    const end = index + needle.length;
    if (index !== -1 && (end === normalized.length || normalized[end] === "/")) return `${marker}${normalized.slice(end)}`;
  }
  return null;
}

export function containsAbsolutePath(value) {
  return findAbsolutePaths(value).length > 0;
}

export function sanitizeContext(raw, fixedSourceValue = "") {
  if (typeof raw !== "string") throw new Error("context must be string");
  const paths = findAbsolutePaths(raw);
  let cursor = 0;
  let sanitized = "";
  const untouched = [];
  for (const match of paths) {
    const replacement = neutralizeAbsoluteToken(match.token);
    if (replacement === null) throw new Error(`unrecognized absolute source path: ${match.token}`);
    const rawPart = raw.slice(cursor, match.start);
    untouched.push(rawPart);
    sanitized += rawPart + replacement;
    cursor = match.end;
  }
  untouched.push(raw.slice(cursor));
  sanitized += raw.slice(cursor);
  if (containsAbsolutePath(sanitized)) throw new Error("residual absolute path after sanitation");
  const typedCommit = /^(?:commit:)?([0-9a-f]{40})$/u.exec(fixedSourceValue)?.[1] ?? null;
  const commitOccurrences = typedCommit === null ? 0 : sanitized.split(typedCommit).length - 1;
  if (typedCommit !== null) sanitized = sanitized.split(typedCommit).join("<FIXED_SOURCE_COMMIT>");
  return {
    sanitized,
    path_occurrences: paths.length,
    commit_occurrences: commitOccurrences,
    untouched_text_sha256: sha256(untouched.join("\0"))
  };
}

export function profileForTask(taskId) {
  if (taskId.includes("-ui-logs-")) return "ui-log";
  if (taskId.includes("-dialogue-")) return "dialogue";
  if (taskId.includes("p2-tome-texts")) return "unknown-text";
  if (/(?:-mechanics-|-status-|-condition-|-random-control-|-args-order-|-format-|-markup-)/u.test(taskId)) return "mechanics";
  throw new Error(`${taskId}: unclassified profile`);
}

export function historicalRouteCell(taskId) {
  if (taskId.includes("p2-tome-texts")) return "H2";
  if (/^p1-b[234]-/u.test(taskId)) return "H3";
  if (/^p1-b[5-8]-/u.test(taskId) || /^p2-cults-status-b(?:1|3)-/u.test(taskId)) return "H4";
  return "H1";
}

const categoryForProfile = profile => profile === "mechanics" || profile === "ui-log" ? "Runtime-focused" : profile === "dialogue" ? "Dialogue" : "Unknown-text";
const orderDigest = values => sha256(`${values.join("\n")}\n`);
const identityKey = row => `${row.task_id}\0${row.revision_key}`;
const normalizedPair = row => `${normalizeText(row.source)}\0${normalizeText(row.target)}`;

function cellCounts(rows, field) {
  const result = {};
  for (const value of [...new Set(rows.map(row => row[field]))].sort(compareCodepoints)) {
    const selected = rows.filter(row => row[field] === value);
    result[value] = {tasks: new Set(selected.map(row => row.task_id)).size, rows: selected.length};
  }
  return result;
}

function assertDeepEqual(actual, expected, label) {
  assert.deepEqual(actual, expected, label);
}

function assertUnique(values, label) {
  if (new Set(values).size !== values.length) throw new Error(`${label}: duplicate detected`);
}

const SCOPE_HISTORY_RE = /(?:\bout of scope\b|\bthis revision\b|\bnot part of this candidate\b)/iu;
const REVIEW_HISTORY_RE = /(?:already[- ]accepted|already reviewed|review(?:ed)? (?:once|correctly flagged)|senior[- ]audit|senior scope calibration|adjudicat)/iu;
const TYPED_ID_RE = /(?:\bRFR-\d{4}\b|\b(?:task|revision|dispatch|review)[_-]id\b|\b(?:review|senior-audit)-\d{2}\b)/iu;

export function hygieneRulesForContext(context, internalValues) {
  const rules = [];
  if ([...internalValues].some(value => value && context.includes(value))) rules.push("INTERNAL_VALUE_SUBSTRING");
  if (TYPED_ID_RE.test(context)) rules.push("TYPED_TASK_OR_REVIEW_ID");
  if (REVIEW_HISTORY_RE.test(context)) rules.push("REVIEW_OR_ADJUDICATION_HISTORY");
  if (SCOPE_HISTORY_RE.test(context)) rules.push("SCOPE_HISTORY_MARKER");
  return rules;
}

function allInternalValues(rows) {
  const values = new Set();
  for (const row of rows) {
    for (const value of [row.task_id, row.revision_key, row.terminal_input.logical_path, row.terminal_input.sha256, row.terminal_input.dispatch_id, row.terminal_input.candidate_identity]) {
      if (typeof value === "string" && value) values.add(value);
    }
  }
  return values;
}

export function assemblePackage({snapshot, membership, oldQueue, currentCandidates, terminalReader}) {
  if (!Array.isArray(membership?.items)) throw new Error("canonical membership malformed");
  const canonicalTaskIds = new Set();
  for (const item of membership.items) {
    if (typeof item.task_id !== "string" || !item.task_id) throw new Error("canonical membership task_id malformed");
    canonicalTaskIds.add(item.task_id);
  }
  const selected = selectTerminalDispatches(snapshot, canonicalTaskIds);
  const pathBindings = new Map();
  const terminalRecords = [];
  const rows = [];
  let modern = 0;
  let legacy = 0;
  const fixedSourceFields = {fixed_source_identity: 0, fixed_source_commit: 0};
  let emptyTerminologySnapshots = 0;
  for (const dispatch of selected) {
    if (!SHA256_RE.test(dispatch.candidate_identity ?? "")) throw new Error(`${dispatch.task_id}: selected dispatch candidate_identity must be 64-hex`);
    const previous = pathBindings.get(dispatch.input_path);
    if (previous !== undefined) throw new Error(`${dispatch.input_path}: duplicate or conflicting terminal binding`);
    pathBindings.set(dispatch.input_path, dispatch.task_id);
    const {bytes: envelopeBytes, parsed} = readValidatedEnvelope(dispatch, terminalReader);
    if (parsed.container === "modern") modern += 1; else legacy += 1;
    fixedSourceFields[parsed.fixed_key] += 1;
    const envelopeForMetadata = JSON.parse(envelopeBytes.toString("utf8"));
    const payloadForMetadata = envelopeForMetadata.payload ?? envelopeForMetadata;
    if (payloadForMetadata.terminology_snapshot.length === 0) emptyTerminologySnapshots += 1;
    terminalRecords.push({task_id: dispatch.task_id, dispatch_id: dispatch.dispatch_id, candidate_identity: dispatch.candidate_identity, canonical_identity: parsed.canonical_identity, cycle: dispatch.cycle, lifecycle: dispatch.lifecycle, logical_path: dispatch.input_path, sha256: dispatch.input_fingerprint.sha256, size_bytes: dispatch.input_fingerprint.size_bytes, envelope_container: parsed.container, fixed_source_field: parsed.fixed_key});
    for (const item of parsed.rows) {
      const cleaned = sanitizeContext(item.context, parsed.fixed_value);
      const profile = profileForTask(dispatch.task_id);
      rows.push({...item, task_id: dispatch.task_id, profile, category: categoryForProfile(profile), historical_route_cell: historicalRouteCell(dispatch.task_id), sanitized_context: cleaned.sanitized, path_redaction_occurrences: cleaned.path_occurrences, commit_neutralization_occurrences: cleaned.commit_occurrences, untouched_text_sha256: cleaned.untouched_text_sha256, terminal_input: terminalRecords.at(-1)});
    }
  }
  terminalRecords.sort((left, right) => compareCodepoints(left.logical_path, right.logical_path));
  const manifestCanonical = terminalRecords.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  const manifest = {records: terminalRecords, count: terminalRecords.length, bytes: terminalRecords.reduce((sum, record) => sum + record.size_bytes, 0), manifest_sha256: sha256(manifestCanonical)};

  const identities = rows.map(identityKey);
  const normalizedSources = rows.map(row => normalizeText(row.source));
  const normalizedPairs = rows.map(normalizedPair);
  assertUnique(identities, "identity");
  assertUnique(normalizedSources, "normalized source");
  assertUnique(normalizedPairs, "normalized pair");
  const oldSources = new Set(oldQueue.items.map(item => normalizeText(item.source)));
  const oldPairs = new Set(oldQueue.items.map(item => `${normalizeText(item.source)}\0${normalizeText(item.target)}`));
  const currentSources = new Set(currentCandidates.items.map(item => normalizeText(item.source)));
  const currentPairs = new Set(currentCandidates.items.map(item => `${normalizeText(item.source)}\0${normalizeText(item.target)}`));
  const overlaps = {
    old_120_normalized_source: normalizedSources.filter(value => oldSources.has(value)).length,
    old_120_normalized_pair: normalizedPairs.filter(value => oldPairs.has(value)).length,
    current_439_normalized_source: normalizedSources.filter(value => currentSources.has(value)).length,
    current_439_normalized_pair: normalizedPairs.filter(value => currentPairs.has(value)).length
  };
  if (Object.values(overlaps).some(value => value !== 0)) throw new Error(`old-pool overlap drift: ${JSON.stringify(overlaps)}`);

  const internalValues = allInternalValues(rows);
  for (let index = 0; index < rows.length; index += 1) {
    const neutralId = `RFR-${String(index + 1).padStart(4, "0")}`;
    const matchedRules = hygieneRulesForContext(rows[index].context, internalValues);
    rows[index].neutral_id = neutralId;
    rows[index].matched_hygiene_rule_ids = matchedRules;
    rows[index].hygiene_disposition = matchedRules.length === 0 ? "MODEL_FACING" : "CONTEXT_META_PROVENANCE_EXCLUDED";
  }
  const excludedIds = rows.filter(row => row.hygiene_disposition !== "MODEL_FACING").map(row => row.neutral_id);
  assertDeepEqual(excludedIds, FROZEN.excluded_neutral_ids, "meta-provenance exclusion set");

  const digests = {identity: orderDigest(identities), source: orderDigest(rows.map(row => row.source)), target: orderDigest(rows.map(row => row.target)), context: orderDigest(rows.map(row => row.context))};
  const counts = {
    tasks: new Set(rows.map(row => row.task_id)).size,
    rows: rows.length,
    modern_envelopes: modern,
    legacy_envelopes: legacy,
    fixed_source_fields: fixedSourceFields,
    terminology_snapshot: {empty_strings: emptyTerminologySnapshots, non_empty_strings: terminalRecords.length - emptyTerminologySnapshots},
    profiles: cellCounts(rows, "profile"),
    categories: cellCounts(rows, "category"),
    historical_route_cells: cellCounts(rows, "historical_route_cell"),
    path_redaction: {rows: rows.filter(row => row.path_redaction_occurrences > 0).length, occurrences: rows.reduce((sum, row) => sum + row.path_redaction_occurrences, 0)},
    commit_neutralization: {rows: rows.filter(row => row.commit_neutralization_occurrences > 0).length, occurrences: rows.reduce((sum, row) => sum + row.commit_neutralization_occurrences, 0)},
    dispositions: {MODEL_FACING: rows.filter(row => row.hygiene_disposition === "MODEL_FACING").length, CONTEXT_META_PROVENANCE_EXCLUDED: rows.filter(row => row.hygiene_disposition !== "MODEL_FACING").length}
  };
  const retainedRows = rows.filter(row => row.hygiene_disposition === "MODEL_FACING");
  const presentationCounts = {tasks: new Set(retainedRows.map(row => row.task_id)).size, rows: retainedRows.length, profiles: cellCounts(retainedRows, "profile"), categories: cellCounts(retainedRows, "category"), historical_route_cells: cellCounts(retainedRows, "historical_route_cell")};
  assertDeepEqual({count: manifest.count, bytes: manifest.bytes, manifest_sha256: manifest.manifest_sha256}, FROZEN.terminal_manifest, "terminal manifest");
  assertDeepEqual(digests, FROZEN.order_digests, "ordered binding digests");
  assertDeepEqual(counts, FROZEN.counts, "frozen internal counts");
  assertDeepEqual(presentationCounts, FROZEN.presentation_counts, "frozen presentation counts");
  return {rows, retainedRows, manifest, overlaps, digests, counts, presentationCounts, internalValues};
}

const PRESENTATION_ITEM_KEYS = ["bounded_fixed_context", "category", "neutral_id", "profile", "source", "target"];
const HEX_PROVENANCE_RE = /(?<![0-9a-f])[0-9a-f]{40,}(?![0-9a-f])/iu;
const META_PROVENANCE_RE = /(?:\b(?:task|revision|dispatch|review)[_-]id\b|\bRFR-\d{4}\b|\b(?:review|senior-audit)-\d{2}\b|already[- ]accepted|already reviewed|review(?:ed)? (?:once|correctly flagged)|senior scope calibration|adjudicat|\bout of scope\b|\bthis revision\b)/iu;
const MODEL_PROVENANCE_RE = /(?:\bprovider\b|\bmodel(?:_id)?\b|\bagent(?:_id)?\b|openai|anthropic|gemini|gpt-|claude|qwen)/iu;

export function presentationLeakCheck(presentation, internalValues) {
  exactKeys(presentation, ["counts", "items", "schema_version", "status"], "presentation");
  if (!Array.isArray(presentation.items)) throw new Error("presentation items must be an array");
  for (const [index, item] of presentation.items.entries()) {
    exactKeys(item, PRESENTATION_ITEM_KEYS, `presentation.items[${index}]`);
  }
  let stringsScanned = 0;
  const scan = (value, parentKey = null, kind = "value") => {
    if (typeof value === "string") {
      stringsScanned += 1;
      if ([...internalValues].some(internal => internal && value.includes(internal))) throw new Error("presentation internal value substring leakage");
      if (!(kind === "value" && parentKey === "neutral_id") && (TYPED_ID_RE.test(value) || META_PROVENANCE_RE.test(value))) throw new Error("presentation typed identity or review-history leakage");
      if (HEX_PROVENANCE_RE.test(value)) throw new Error("presentation hash provenance leakage");
      if (MODEL_PROVENANCE_RE.test(value)) throw new Error("presentation model provenance leakage");
      if (containsAbsolutePath(value)) throw new Error("presentation absolute path leakage");
      return;
    }
    if (Array.isArray(value)) {
      for (const item of value) scan(item);
      return;
    }
    if (value && typeof value === "object") {
      for (const [key, child] of Object.entries(value)) {
        scan(key, null, "key");
        scan(child, key, "value");
      }
    }
  };
  scan(presentation);
  return stringsScanned;
}

function writeJson(out, name, value) {
  const bytes = jsonBytes(value);
  fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, name), bytes);
  return recordFor(bytes);
}

function deriveGates(assembled, presentationScanCount, modelCalls, networkCalls) {
  const overlapValues = assembled.overlaps;
  return {
    fingerprints_exact: assembled.manifest.records.every(record => SHA256_RE.test(record.sha256) && Number.isInteger(record.size_bytes) && record.size_bytes > 0),
    dispatch_envelope_identity_exact: assembled.manifest.records.every(record => SHA256_RE.test(record.candidate_identity) && record.candidate_identity === record.canonical_identity),
    envelope_schema_exact: assembled.counts.modern_envelopes === 76 && assembled.counts.legacy_envelopes === 1 && assembled.counts.fixed_source_fields.fixed_source_identity === 70 && assembled.counts.fixed_source_fields.fixed_source_commit === 7 && assembled.counts.terminology_snapshot.empty_strings === 1 && assembled.counts.terminology_snapshot.non_empty_strings === 76,
    ordered_bindings_exact: assembled.digests.identity === FROZEN.order_digests.identity && assembled.digests.source === FROZEN.order_digests.source && assembled.digests.target === FROZEN.order_digests.target && assembled.digests.context === FROZEN.order_digests.context,
    unique_identity_source_pair: new Set(assembled.rows.map(identityKey)).size === 156 && new Set(assembled.rows.map(row => normalizeText(row.source))).size === 156 && new Set(assembled.rows.map(normalizedPair)).size === 156,
    old_120_overlap_zero: overlapValues.old_120_normalized_source === 0 && overlapValues.old_120_normalized_pair === 0,
    current_439_overlap_zero: overlapValues.current_439_normalized_source === 0 && overlapValues.current_439_normalized_pair === 0,
    internal_counts_exact: canonicalJson(assembled.counts) === canonicalJson(FROZEN.counts),
    presentation_counts_exact: canonicalJson(assembled.presentationCounts) === canonicalJson(FROZEN.presentation_counts),
    meta_provenance_exclusions_exact: JSON.stringify(assembled.rows.filter(row => row.hygiene_disposition !== "MODEL_FACING").map(row => row.neutral_id)) === JSON.stringify(FROZEN.excluded_neutral_ids),
    path_redaction_31_rows_52_occurrences: assembled.counts.path_redaction.rows === 31 && assembled.counts.path_redaction.occurrences === 52,
    commit_neutralization_15_rows_15_occurrences: assembled.counts.commit_neutralization.rows === 15 && assembled.counts.commit_neutralization.occurrences === 15,
    sanitized_presentation_hygiene: Number.isInteger(presentationScanCount) && presentationScanCount > 0,
    zero_inference: modelCalls === 0 && networkCalls === 0
  };
}

export function buildPackage(args) {
  const inputs = {};
  for (const name of Object.keys(FROZEN.inputs).sort(compareCodepoints)) inputs[name] = readPinned(args.root, name);
  // SNAPSHOT access is deliberately limited to source_repo_head plus the fields
  // selected in selectTerminalDispatches, including dispatch.candidate_identity.
  const snapshotCommit = inputs.provenance_snapshot.value.source_repo_head;
  const membershipCommit = inputs.canonical_membership.value.production_translation_commit;
  if (!/^[0-9a-f]{40}$/u.test(snapshotCommit ?? "") || snapshotCommit !== membershipCommit || membershipCommit !== FROZEN.production_translation_commit || inputs.old_120_queue.value.production_translation_commit !== membershipCommit) throw new Error("production translation commit drift");
  if (inputs.old_120_queue.value.items?.length !== 120 || inputs.current_439_candidates.value.items?.length !== 439) throw new Error("old pool count drift");
  const productionInput = path.join(args.root, args.productionInput);
  const assembled = assemblePackage({snapshot: inputs.provenance_snapshot.value, membership: inputs.canonical_membership.value, oldQueue: inputs.old_120_queue.value, currentCandidates: inputs.current_439_candidates.value, terminalReader: logicalPath => fs.readFileSync(path.join(productionInput, logicalPath))});

  const registry = {
    schema_version: "route-familiarity-runtime-expansion-binding-registry-v1",
    status: "FROZEN_INTERNAL_BINDINGS",
    production_translation_commit: FROZEN.production_translation_commit,
    disposition_rule: "MODEL_FACING only when bounded context matches no internal identity, typed ID, review/adjudication history, or scope-history rule; otherwise CONTEXT_META_PROVENANCE_EXCLUDED without prose rewriting.",
    frozen_input_manifest: Object.fromEntries(Object.entries(inputs).map(([name, input]) => [name, {logical_path: input.logical_path, sha256: input.sha256, size_bytes: input.size_bytes}])),
    terminal_input_manifest: assembled.manifest,
    order_digests: assembled.digests,
    counts: assembled.counts,
    presentation_counts: assembled.presentationCounts,
    overlap_gates: assembled.overlaps,
    items: assembled.rows.map(row => ({
      neutral_id: row.neutral_id,
      task_id: row.task_id,
      revision_key: row.revision_key,
      profile: row.profile,
      category: row.category,
      historical_route_cell: row.historical_route_cell,
      hygiene_disposition: row.hygiene_disposition,
      matched_hygiene_rule_ids: row.matched_hygiene_rule_ids,
      terminal_input: {logical_path: row.terminal_input.logical_path, sha256: row.terminal_input.sha256, size_bytes: row.terminal_input.size_bytes, dispatch_id: row.terminal_input.dispatch_id, candidate_identity: row.terminal_input.candidate_identity, cycle: row.terminal_input.cycle, lifecycle: row.terminal_input.lifecycle, envelope_container: row.terminal_input.envelope_container, fixed_source_field: row.terminal_input.fixed_source_field},
      identity_sha256: sha256(identityKey(row)),
      source_sha256: sha256(row.source),
      normalized_source_sha256: sha256(normalizeText(row.source)),
      target_sha256: sha256(row.target),
      normalized_pair_sha256: sha256(normalizedPair(row)),
      raw_context_sha256: sha256(row.context),
      raw_context_size_bytes: Buffer.byteLength(row.context, "utf8"),
      sanitized_context_sha256: sha256(row.sanitized_context),
      sanitized_context_size_bytes: Buffer.byteLength(row.sanitized_context, "utf8"),
      path_redaction_occurrences: row.path_redaction_occurrences,
      commit_neutralization_occurrences: row.commit_neutralization_occurrences,
      untouched_text_sha256: row.untouched_text_sha256
    }))
  };
  const presentation = {
    schema_version: "neutral-context-presentation-v1",
    status: "FROZEN_ZERO_INFERENCE_MODEL_FACING",
    counts: {items: assembled.presentationCounts.rows, tasks: assembled.presentationCounts.tasks, profiles: assembled.presentationCounts.profiles, categories: assembled.presentationCounts.categories},
    items: assembled.retainedRows.map(row => ({neutral_id: row.neutral_id, category: row.category, profile: row.profile, source: row.source, target: row.target, bounded_fixed_context: row.sanitized_context}))
  };
  const presentationScanCount = presentationLeakCheck(presentation, assembled.internalValues);
  const presentationMarkerCounts = {
    MAIN_GAME_ROOT: assembled.retainedRows.reduce((sum, row) => sum + row.sanitized_context.split("<MAIN_GAME_ROOT>").length - 1, 0),
    DLC_ROOT: assembled.retainedRows.reduce((sum, row) => sum + row.sanitized_context.split("<DLC_ROOT>").length - 1, 0)
  };
  assertDeepEqual(presentationMarkerCounts, FROZEN.presentation_marker_counts, "presentation neutral-root marker counts");
  const gates = deriveGates(assembled, presentationScanCount, 0, 0);
  if (!Object.values(gates).every(Boolean)) throw new Error(`derived build gate failed: ${JSON.stringify(gates)}`);
  const generated = {};
  generated[GENERATED_NAMES[0]] = writeJson(args.out, GENERATED_NAMES[0], registry);
  generated[GENERATED_NAMES[1]] = writeJson(args.out, GENERATED_NAMES[1], presentation);
  const report = {
    schema_version: "route-familiarity-runtime-expansion-build-report-v1",
    status: "PASS_ZERO_INFERENCE_FREEZE_GATES",
    model_calls: 0,
    network_calls: 0,
    counts: assembled.counts,
    presentation_counts: assembled.presentationCounts,
    overlap_gates: assembled.overlaps,
    terminal_manifest: {count: assembled.manifest.count, bytes: assembled.manifest.bytes, manifest_sha256: assembled.manifest.manifest_sha256},
    order_digests: assembled.digests,
    frozen_input_hashes: Object.fromEntries(Object.entries(inputs).map(([name, input]) => [name, input.sha256])),
    presentation_hygiene_scan: {recursive_key_value_strings: presentationScanCount},
    sanitation_summary: {path_rows: assembled.counts.path_redaction.rows, path_occurrences: assembled.counts.path_redaction.occurrences, commit_rows: assembled.counts.commit_neutralization.rows, commit_occurrences: assembled.counts.commit_neutralization.occurrences, presentation_neutral_root_markers: presentationMarkerCounts, dlc_aggregation_segment_absorbed: true},
    artifact_hash_dependency: "BUILD-REPORT hashes only registry and presentation; EXPERIMENT hashes those plus BUILD-REPORT; all four final hashes are frozen externally in build.mjs and independently checked, avoiding self-reference.",
    generated_artifacts: {...generated},
    gates
  };
  generated[GENERATED_NAMES[2]] = writeJson(args.out, GENERATED_NAMES[2], report);
  const experiment = {
    schema_version: "route-familiarity-runtime-expansion-experiment-v1",
    experiment_id: "route-familiarity-runtime-expansion-v1",
    status: "FROZEN_ZERO_INFERENCE_EXPLORATORY_POOL",
    date_frozen: "2026-08-28",
    production_translation_commit: FROZEN.production_translation_commit,
    model_calls: 0,
    network_calls: 0,
    design: "Deterministic terminal contextual-envelope expansion with hash-pinned inputs, exact typed source/target/context and candidate-identity binding, old-pool overlap exclusion, neutral historical-route strata, and a separately filtered presentation.",
    limitations: ["Every retained row has some historical model exposure.", "This is not an isolation set.", "Historical-route cells are imbalanced and are not memorization evidence.", "Later scores are exploratory reference scores unless governed by a separately frozen formal design."],
    counts: assembled.counts,
    presentation_counts: assembled.presentationCounts,
    excluded_neutral_ids: FROZEN.excluded_neutral_ids,
    frozen_input_hashes: report.frozen_input_hashes,
    terminal_manifest: report.terminal_manifest,
    order_digests: assembled.digests,
    sanitation_summary: report.sanitation_summary,
    artifact_hash_dependency: report.artifact_hash_dependency,
    generated_artifacts: {...generated},
    next_gate: "Independent normal review and different-model senior cross-review before completion."
  };
  generated[GENERATED_NAMES[3]] = writeJson(args.out, GENERATED_NAMES[3], experiment);
  return {registry, presentation, report, experiment, generated, internalRows: assembled.rows};
}

const invoked = process.argv[1] ? pathToFileURL(path.resolve(process.argv[1])).href : null;
if (invoked === import.meta.url) {
  const result = buildPackage(parseArgs(process.argv.slice(2)));
  process.stdout.write(`${JSON.stringify({status: result.report.status, counts: result.report.counts, presentation_counts: result.report.presentation_counts, terminal_manifest: result.report.terminal_manifest, order_digests: result.report.order_digests, generated_artifacts: result.generated}, null, 2)}\n`);
}
