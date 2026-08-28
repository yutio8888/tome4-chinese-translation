import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const queuePath = path.join(here, "AUDIT-QUEUE.json");
const contractPath = path.join(here, "SOURCE-LOCATOR-CONTRACT.json");

function parseArgs(argv) {
  const args = {out: path.join(here, "SOURCE-LOCATORS.json")};
  const valueFlags = new Set(["--engine-repo", "--dlc-root", "--out"]);
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (!valueFlags.has(flag) || !argv[index + 1]) {
      throw new Error("usage: node locate-sources.mjs --engine-repo ENGINE_REPO --dlc-root DLC_ROOT [--out FILE]");
    }
    const key = flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    args[key] = path.resolve(argv[++index]);
  }
  if (!args.engineRepo || !args.dlcRoot) {
    throw new Error("--engine-repo and --dlc-root are required");
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
const toPosix = value => value.split(path.sep).join("/");

function assertSafeRelative(relativePath, label) {
  if (typeof relativePath !== "string" || !relativePath || relativePath.includes("\0") || path.posix.isAbsolute(relativePath)) {
    throw new Error(`${label}: unsafe relative path`);
  }
  const normalized = path.posix.normalize(relativePath);
  if (normalized !== relativePath || normalized === ".." || normalized.startsWith("../")) {
    throw new Error(`${label}: relative path traversal`);
  }
}

function isInside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

function normalizeWithMap(value) {
  let normalized = "";
  const map = [];
  let pendingSpace = false;
  let pendingIndex = 0;
  for (let index = 0; index < value.length; index += 1) {
    const escapedWhitespace = value[index] === "\\" && ["n", "r", "t"].includes(value[index + 1]);
    if (escapedWhitespace || /\s/.test(value[index])) {
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

function normalizedOccurrences(fileText, source) {
  const haystack = normalizeWithMap(fileText);
  const needle = normalizeWithMap(source).normalized;
  if (!needle) return [];
  const occurrences = [];
  let from = 0;
  while (true) {
    const found = haystack.normalized.indexOf(needle, from);
    if (found === -1) break;
    const rawStart = haystack.map[found];
    const rawEnd = haystack.map[found + needle.length - 1] + 1;
    occurrences.push({rawStart, rawEnd});
    from = found + 1;
  }
  return occurrences;
}

function lineStarts(text) {
  const starts = [0];
  for (let index = 0; index < text.length; index += 1) if (text[index] === "\n") starts.push(index + 1);
  return starts;
}

function lineIndexAt(starts, offset) {
  let low = 0;
  let high = starts.length;
  while (low + 1 < high) {
    const middle = Math.floor((low + high) / 2);
    if (starts[middle] <= offset) low = middle;
    else high = middle;
  }
  return low;
}

function contextForOccurrence(fileText, starts, occurrence) {
  const startLineIndex = lineIndexAt(starts, occurrence.rawStart);
  const endLineIndex = lineIndexAt(starts, Math.max(occurrence.rawStart, occurrence.rawEnd - 1));
  const lineWindowStart = starts[Math.max(0, startLineIndex - 12)];
  const afterLineIndex = Math.min(starts.length, endLineIndex + 13);
  const lineWindowEnd = afterLineIndex < starts.length ? starts[afterLineIndex] : fileText.length;
  const maximumChars = 12000;
  let contextStart = lineWindowStart;
  let contextEnd = lineWindowEnd;
  let truncated = false;
  if (contextEnd - contextStart > maximumChars) {
    truncated = true;
    const matchedLength = occurrence.rawEnd - occurrence.rawStart;
    if (matchedLength > maximumChars) throw new Error("complete source span exceeds context cap");
    const remaining = maximumChars - matchedLength;
    const desiredBefore = Math.floor(remaining / 2);
    contextStart = Math.max(lineWindowStart, occurrence.rawStart - desiredBefore);
    contextEnd = Math.min(lineWindowEnd, contextStart + maximumChars);
    if (contextEnd < occurrence.rawEnd) {
      contextEnd = occurrence.rawEnd;
      contextStart = Math.max(lineWindowStart, contextEnd - maximumChars);
    }
  }
  const visibleContext = fileText.slice(contextStart, contextEnd);
  const matchedSpan = fileText.slice(occurrence.rawStart, occurrence.rawEnd);
  return {
    line_start: startLineIndex + 1,
    line_end: endLineIndex + 1,
    column_start: occurrence.rawStart - starts[startLineIndex] + 1,
    matched_span_sha256: sha256Bytes(matchedSpan),
    matched_chars: matchedSpan.length,
    context_start_line: lineIndexAt(starts, contextStart) + 1,
    context_end_line: lineIndexAt(starts, Math.max(contextStart, contextEnd - 1)) + 1,
    extraction_mode: truncated ? "line_window_12_then_deterministic_char_cap" : "line_window_12",
    visible_chars: visibleContext.length,
    truncated,
    visible_context: visibleContext,
    visible_context_sha256: sha256Bytes(visibleContext)
  };
}

function gitOutput(repo, commandArgs, encoding = "utf8") {
  return execFileSync("git", ["-C", repo, ...commandArgs], {encoding, maxBuffer: 64 * 1024 * 1024});
}

const queue = readJson(queuePath);
const contract = readJson(contractPath);
if (queue.schema_version !== "prospective-residual-audit-queue-v3") throw new Error("unexpected queue schema");
if (queue.reviewer_inference_allowed !== false) throw new Error("queue unexpectedly permits inference");
if (!Array.isArray(queue.items) || queue.items.length !== contract.expected_items) throw new Error("queue item count mismatch");
if (new Set(queue.items.map(item => item.audit_id)).size !== queue.items.length) throw new Error("duplicate audit_id");

const engineCommit = contract.bindings.tome.commit;
try {
  const objectType = gitOutput(args.engineRepo, ["cat-file", "-t", `${engineCommit}^{commit}`]).trim();
  if (objectType !== "commit") throw new Error(`unexpected object type ${objectType}`);
} catch (error) {
  throw new Error(`fixed engine commit unavailable: ${error.message}`);
}

function bindSource(item) {
  const component = item.canonical_identity?.component;
  const section = item.canonical_identity?.section;
  const binding = contract.bindings[component];
  if (!binding) return {status: "UNSUPPORTED_COMPONENT", error: `no binding for component ${component ?? "null"}`};
  if (typeof section !== "string" || !section.startsWith(binding.section_prefix)) {
    return {status: "SOURCE_BINDING_FAILED", error: "canonical section does not match registered component prefix"};
  }
  const sectionRelative = section.slice(binding.section_prefix.length);
  try {
    assertSafeRelative(sectionRelative, item.audit_id);
  } catch (error) {
    return {status: "SOURCE_BINDING_FAILED", error: error.message};
  }

  if (binding.read_mode === "git_commit_blob") {
    const relativePath = path.posix.join(binding.repository_prefix, sectionRelative);
    try {
      assertSafeRelative(relativePath, item.audit_id);
      const buffer = gitOutput(args.engineRepo, ["show", `${binding.commit}:${relativePath}`], null);
      return {
        status: "BOUND",
        buffer,
        source_binding: {
          kind: "git_commit_blob",
          repository_alias: binding.repository_alias,
          commit: binding.commit,
          relative_path: relativePath,
          source_artifact_sha256: sha256Bytes(buffer),
          source_artifact_size_bytes: buffer.length
        }
      };
    } catch (error) {
      return {status: "SOURCE_FILE_MISSING", error: `fixed git blob unavailable: ${error.message}`};
    }
  }

  if (binding.read_mode === "working_tree_file_with_required_sha256") {
    const registeredRoot = path.resolve(args.dlcRoot, binding.dlc_subdirectory);
    const candidate = path.resolve(registeredRoot, sectionRelative);
    try {
      if (!fs.statSync(registeredRoot).isDirectory()) throw new Error("registered DLC root is not a directory");
      const realRoot = fs.realpathSync(registeredRoot);
      const realCandidate = fs.realpathSync(candidate);
      if (!isInside(realRoot, realCandidate)) throw new Error("DLC file escapes registered root");
      if (!fs.statSync(realCandidate).isFile()) throw new Error("registered DLC source is not a file");
      const buffer = fs.readFileSync(realCandidate);
      return {
        status: "BOUND",
        buffer,
        source_binding: {
          kind: "dlc_file_sha256",
          repository_alias: binding.repository_alias,
          commit: null,
          relative_path: toPosix(sectionRelative),
          source_artifact_sha256: sha256Bytes(buffer),
          source_artifact_size_bytes: buffer.length,
          provenance_note: "DLC repository commit is not frozen; this exact public file hash is the binding."
        }
      };
    } catch (error) {
      return {status: "SOURCE_FILE_MISSING", error: `DLC file unavailable: ${error.message}`};
    }
  }
  return {status: "SOURCE_BINDING_FAILED", error: `unsupported read mode ${binding.read_mode}`};
}

const records = [];
for (const item of queue.items) {
  const bound = bindSource(item);
  const base = {
    audit_id: item.audit_id,
    task_id: item.task_id,
    original_revision_key: item.original_revision_key,
    canonical_component: item.canonical_identity?.component ?? null,
    canonical_section: item.canonical_identity?.section ?? null,
    canonical_revision_uid: item.canonical_identity?.revision_uid ?? null,
    source_sha256: sha256Bytes(item.source),
    target_sha256: sha256Bytes(item.target),
    source_binding: bound.source_binding ?? null
  };
  if (bound.status !== "BOUND") {
    records.push({...base, locator_status: bound.status, source_occurrences: 0, occurrence_records: [], locator_error: bound.error});
    continue;
  }
  const fileText = bound.buffer.toString("utf8");
  if (Buffer.from(fileText, "utf8").compare(bound.buffer) !== 0) {
    records.push({...base, locator_status: "SOURCE_BINDING_FAILED", source_occurrences: 0, occurrence_records: [], locator_error: "source artifact is not canonical UTF-8"});
    continue;
  }
  const occurrences = normalizedOccurrences(fileText, item.source);
  const starts = lineStarts(fileText);
  const occurrenceRecords = occurrences.map((occurrence, index) => ({
    occurrence_ordinal: index + 1,
    ...contextForOccurrence(fileText, starts, occurrence)
  }));
  const locatorStatus = occurrences.length === 0
    ? "SOURCE_NOT_FOUND"
    : occurrences.length === 1
      ? "LOCATED_UNIQUE"
      : "LOCATED_MULTIPLE";
  records.push({
    ...base,
    locator_status: locatorStatus,
    match_contract: "complete_source_whitespace_normalized_literal_substring_v1",
    source_occurrences: occurrences.length,
    occurrence_records: occurrenceRecords,
    locator_error: occurrences.length === 0 ? "complete selected source not found under normalized literal matching" : null
  });
}

const counts = records.reduce((result, record) => {
  result[record.locator_status] = (result[record.locator_status] ?? 0) + 1;
  return result;
}, {});
const output = {
  schema_version: "prospective-residual-source-locators-v3",
  status: records.every(record => ["LOCATED_UNIQUE", "LOCATED_MULTIPLE"].includes(record.locator_status))
    ? "ALL_SOURCE_ARTIFACTS_LOCATED"
    : "SOURCE_LOCATION_INCOMPLETE",
  contains_audit_verdicts: false,
  model_calls_made: 0,
  queue_sha256: sha256File(queuePath),
  locator_contract_sha256: sha256File(contractPath),
  counts: {items: records.length, by_locator_status: counts},
  items: records
};

const serialized = `${JSON.stringify(output, null, 2)}\n`;
if (/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/.test(serialized)) throw new Error("refusing to write a local absolute path");
for (const forbidden of ["\"verdict\"", "\"audited_at_utc\"", "\"defect_id\""]) {
  if (serialized.includes(forbidden)) throw new Error(`non-judgment contract violation: ${forbidden}`);
}
fs.mkdirSync(path.dirname(args.out), {recursive: true});
fs.writeFileSync(args.out, serialized);
process.stdout.write(`${JSON.stringify({output: path.basename(args.out), status: output.status, counts: output.counts}, null, 2)}\n`);
