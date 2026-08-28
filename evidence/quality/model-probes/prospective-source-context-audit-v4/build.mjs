#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath, pathToFileURL} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");

export const PHASE0_SCALAR_FIELDS = Object.freeze([
  "task_id",
  "original_revision_key",
  "component",
  "section",
  "source_tag",
  "profile",
  "source",
  "source_sha256"
]);

export const SOURCE_ONLY_FLAGS = Object.freeze([
  "has-printf",
  "has-at-token",
  "short-ambiguous-source",
  "profile-uncertain",
  "repeated-runtime-key",
  "source-has-number-or-unit",
  "source-has-negation-or-condition"
]);

const runtimeProfiles = new Set(["mechanics", "runtime-log", "ui", "unknown"]);
const narrativeProfiles = new Set(["narrative", "dialogue"]);
const printfRe = /%(?:\d+\$)?[-+ #0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?[hlLzjt]*[cdiouxXeEfgGaAspq]/g;
const atTokenRe = /@[A-Za-z][A-Za-z0-9_:-]*@/u;
const digitRe = /\d/u;
const unitWordRe = /\b(?:turns?|rounds?|tiles?|spaces?|meters?|metres?|feet|seconds?|minutes?|hours?|days?|percent|percentage|points?|levels?|stacks?|charges?|times?|radius|range|distance|cooldown|energy|mana|stamina|vim|equilibrium|paradox|hate|psi|souls?|life|health|damage|armor|armour|power)\b/iu;
const negationRe = /\b(?:no|not|never|neither|nor|none|without|cannot|can't|won't|isn't|aren't|doesn't|don't|didn't|unless)\b/iu;
const conditionRe = /\b(?:if|when|whenever|while|until|unless|only if|as long as|provided that|otherwise|below|above|at least|at most|more than|less than)\b/iu;
export const pronounDemonstrativeRe = /\b(?:he|him|his|himself|she|her|hers|herself|they|them|their|theirs|themselves|it|its|itself|this|that|these|those|here|there|such|former|latter)\b/iu;

const sourceTagProfiles = Object.freeze({
  tformat: "mechanics",
  log: "runtime-log",
  logSeen: "runtime-log",
  logCombat: "runtime-log",
  logPlayer: "runtime-log",
  logMessage: "runtime-log",
  delayedLogMessage: "runtime-log",
  say: "dialogue",
  saySimple: "dialogue",
  easing: "ui",
  chat: "dialogue",
  lore: "narrative"
});

export const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const canonicalBytes = value => Buffer.from(JSON.stringify(value), "utf8");
export const revisionExposureKey = (taskId, originalRevisionKey) => sha256Bytes(`${taskId}\0${originalRevisionKey}`);
export const contentExposureKey = source => sha256Bytes(normalizeSource(source));
export const locatorContentKey = (component, source) => sha256Bytes(`${component}\0${normalizeSource(source)}`);

function parseArgs(argv) {
  const args = {root: defaultRoot, out: here};
  const flags = new Set(["--production-repo", "--engine-repo", "--dlc-root", "--root", "--out"]);
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!flags.has(flag) || !value) {
      throw new Error("usage: node build.mjs --production-repo PRODUCTION_REPO --engine-repo ENGINE_REPO --dlc-root DLC_ROOT [--root RESEARCH_REPO] [--out OUTPUT_DIR]");
    }
    const key = flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    args[key] = path.resolve(value);
    index += 1;
  }
  if (!args.productionRepo || !args.engineRepo || !args.dlcRoot) throw new Error("--production-repo, --engine-repo and --dlc-root are required");
  return args;
}

function assertPlainObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label}: expected object`);
}

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

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function jsonPointerEscape(value) {
  return String(value).replaceAll("~", "~0").replaceAll("/", "~1");
}

export function normalizeWithMap(value) {
  if (typeof value !== "string") throw new Error("normalizeWithMap expects a string");
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

export function normalizeSource(value) {
  return normalizeWithMap(value).normalized;
}

export function normalizedOccurrences(fileText, source) {
  const haystack = normalizeWithMap(fileText);
  const needle = normalizeSource(source);
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

function phase0Proxy(value, allowed, label) {
  assertPlainObject(value, label);
  return new Proxy(value, {
    get(target, property, receiver) {
      if (typeof property === "symbol") return Reflect.get(target, property, receiver);
      if (!allowed.has(property)) throw new Error(`${label}: Phase-0 access denied for ${property}`);
      return Reflect.get(target, property, receiver);
    },
    has(_target, property) {
      if (typeof property === "symbol") return false;
      if (!allowed.has(property)) throw new Error(`${label}: Phase-0 presence check denied for ${property}`);
      return Object.hasOwn(value, property);
    },
    ownKeys() {
      throw new Error(`${label}: Phase-0 enumeration denied`);
    }
  });
}

function inferredSectionProfiles(section) {
  const normalized = `/${section.toLowerCase()}/`;
  const profiles = new Set();
  if (normalized.includes("/data/talents/")) profiles.add("mechanics");
  if (normalized.includes("/data/chats/") || normalized.includes("/dialogs/")) profiles.add("dialogue");
  if (normalized.includes("/data/lore/") || normalized.includes("/texts/") || normalized.includes("/lore/")) profiles.add("narrative");
  if (normalized.includes("/ui/") || normalized.includes("/interface/")) profiles.add("ui");
  return profiles;
}

function isProfileUncertain(row) {
  if (row.profile === "unknown") return true;
  const tagVote = row.source_tag ? sourceTagProfiles[row.source_tag] : null;
  if (tagVote) return tagVote !== row.profile;
  const sectionVotes = inferredSectionProfiles(row.section);
  return sectionVotes.size !== 1 || !sectionVotes.has(row.profile);
}

function stripPrintf(source) {
  return source.replace(printfRe, " ");
}

function computeSourceOnlyFlags(row, aggregate) {
  const flags = [];
  printfRe.lastIndex = 0;
  if (printfRe.test(row.source)) flags.push("has-printf");
  if (atTokenRe.test(row.source)) flags.push("has-at-token");
  const plain = row.source.trim();
  const sections = aggregate.sectionsBySource.get(row.source) ?? new Set();
  if ([...plain].length <= 8 && !/\s/u.test(plain) && sections.size > 1) flags.push("short-ambiguous-source");
  if (isProfileUncertain(row)) flags.push("profile-uncertain");
  if ((aggregate.rowsBySource.get(row.source) ?? 0) > 1) flags.push("repeated-runtime-key");
  if (digitRe.test(stripPrintf(row.source)) || unitWordRe.test(row.source)) flags.push("source-has-number-or-unit");
  if (negationRe.test(row.source) || conditionRe.test(row.source)) flags.push("source-has-negation-or-condition");
  return SOURCE_ONLY_FLAGS.filter(flag => flags.includes(flag));
}

function decorateSourceOnlyRows(rawRows) {
  const aggregate = {rowsBySource: new Map(), sectionsBySource: new Map()};
  for (const row of rawRows) {
    aggregate.rowsBySource.set(row.source, (aggregate.rowsBySource.get(row.source) ?? 0) + 1);
    if (!aggregate.sectionsBySource.has(row.source)) aggregate.sectionsBySource.set(row.source, new Set());
    aggregate.sectionsBySource.get(row.source).add(`${row.component}\0${row.section}`);
  }
  const rows = rawRows.map(row => ({...row, source_only_flags: computeSourceOnlyFlags(row, aggregate)}));
  rows.sort((a, b) =>
    a.task_id.localeCompare(b.task_id) ||
    a.original_revision_key.localeCompare(b.original_revision_key) ||
    a.component.localeCompare(b.component) ||
    a.section.localeCompare(b.section)
  );
  return rows;
}

function terminalDispatches(task) {
  let dispatches = task.dispatches.filter(dispatch =>
    dispatch.role === "REVIEWER" &&
    dispatch.purpose === "translation_contextual_v1" &&
    dispatch.input_path
  );
  const withCycle = dispatches.filter(dispatch => Number.isFinite(dispatch.cycle));
  if (withCycle.length) {
    const terminalCycle = Math.max(...withCycle.map(dispatch => dispatch.cycle));
    dispatches = withCycle.filter(dispatch => dispatch.cycle === terminalCycle);
  } else if (dispatches.length) {
    dispatches = [dispatches.at(-1)];
  }
  return dispatches;
}

function terminalSourceRows(taskId, envelope, label) {
  const envelopeView = phase0Proxy(envelope, new Set(["payload"]), `${label}.envelope`);
  const payload = phase0Proxy(envelopeView.payload, new Set(["translation_snapshot"]), `${label}.payload`);
  if (!Array.isArray(payload.translation_snapshot)) throw new Error(`${label}: translation_snapshot missing`);
  return payload.translation_snapshot.map((entry, index) => {
    const item = phase0Proxy(entry, new Set(["revision_key", "source"]), `${label}.translation_snapshot[${index}]`);
    if (typeof item.revision_key !== "string" || !item.revision_key || typeof item.source !== "string") {
      throw new Error(`${label}: malformed source-only terminal item`);
    }
    return {task_id: taskId, original_revision_key: item.revision_key, source: item.source};
  });
}

export function reconstructSourceOnlyBaseRows({membership, snapshot, terminalInputs}) {
  assertPlainObject(membership, "canonical membership");
  assertPlainObject(snapshot, "provenance snapshot");
  if (!Array.isArray(membership.items) || !Array.isArray(snapshot.tasks)) throw new Error("source-only base inputs malformed");
  const taskIndex = new Map(snapshot.tasks.map(task => [task.task_id, task]));
  const membershipViews = membership.items.map((item, index) => phase0Proxy(
    item,
    new Set(["task_id", "original_revision_key", "component", "section", "source_tag", "profile", "source_sha256"]),
    `membership.items[${index}]`
  ));
  const taskIds = [...new Set(membershipViews.map(item => item.task_id))].sort();
  const terminalSourceIndex = new Map();
  for (const taskId of taskIds) {
    const task = taskIndex.get(taskId);
    if (!task) throw new Error(`${taskId}: missing provenance task`);
    const dispatches = terminalDispatches(task);
    if (!dispatches.length) throw new Error(`${taskId}: missing terminal contextual input`);
    for (const dispatch of dispatches) {
      const envelope = terminalInputs.get(dispatch.input_path);
      if (!envelope) throw new Error(`${taskId}: terminal input not loaded ${dispatch.input_path}`);
      for (const row of terminalSourceRows(taskId, envelope, `${taskId}/${dispatch.input_path}`)) {
        const key = `${row.task_id}\0${row.original_revision_key}`;
        const previous = terminalSourceIndex.get(key);
        if (previous !== undefined && previous !== row.source) throw new Error(`${key}: conflicting terminal sources`);
        terminalSourceIndex.set(key, row.source);
      }
    }
  }
  const rawRows = [];
  for (let index = 0; index < membershipViews.length; index += 1) {
    const item = membershipViews[index];
    const key = `${item.task_id}\0${item.original_revision_key}`;
    const source = terminalSourceIndex.get(key);
    if (source === undefined) throw new Error(`${key}: terminal source missing`);
    const row = {
      task_id: item.task_id,
      original_revision_key: item.original_revision_key,
      component: item.component,
      section: item.section,
      source_tag: item.source_tag ?? null,
      profile: item.profile,
      source,
      source_sha256: item.source_sha256
    };
    for (const field of PHASE0_SCALAR_FIELDS) {
      if (field === "source_tag") continue;
      if (typeof row[field] !== "string" || !row[field]) throw new Error(`${key}: invalid ${field}`);
    }
    if (sha256Bytes(source) !== row.source_sha256) throw new Error(`${key}: source hash mismatch`);
    rawRows.push(row);
  }
  return decorateSourceOnlyRows(rawRows);
}

export function canonicalSourceOnlyBaseBytes(inputs) {
  return canonicalBytes(reconstructSourceOnlyBaseRows(inputs));
}

export function makeSourceOnlyBaseFrame(baseRows, productionTranslationCommit) {
  return {
    schema_version: "prospective-source-only-base-frame-v4",
    status: "FROZEN_SOURCE_ONLY_BASE",
    mode: "NO_INFERENCE/SOURCE_SCREEN_ONLY",
    source_only: true,
    production_translation_commit: productionTranslationCommit,
    source_projection_sha256: sha256Bytes(canonicalBytes(baseRows)),
    counts: {items: baseRows.length, tasks: new Set(baseRows.map(row => row.task_id)).size},
    items: baseRows
  };
}

export function classifyCategory(row) {
  if (runtimeProfiles.has(row.profile) && row.source_only_flags.length > 0) return "Runtime";
  if (narrativeProfiles.has(row.profile) && (row.source_only_flags.length >= 4 || pronounDemonstrativeRe.test(row.source))) return "Narrative";
  return null;
}

export function collectStructuredExposures(value, logicalPath) {
  const sourceRecords = [];
  const revisionRecords = [];
  const deniedTraversalKeys = /^(?:target(?:_|$)|pair_sha256$|canonical_|membership_sha256$|risk_flags$|args_order$|multiline$|preferred_terms?$|relevant_terms?$|terminology$)/u;
  function visit(node, pointer) {
    if (Array.isArray(node)) {
      node.forEach((entry, index) => visit(entry, `${pointer}/${index}`));
      return;
    }
    if (!node || typeof node !== "object") return;
    if (typeof node.source === "string" && normalizeSource(node.source)) {
      sourceRecords.push({
        content_key: contentExposureKey(node.source),
        logical_path: logicalPath,
        json_pointer: pointer || "/"
      });
    }
    if (typeof node.task_id === "string" && typeof node.original_revision_key === "string") {
      revisionRecords.push({
        revision_key: revisionExposureKey(node.task_id, node.original_revision_key),
        logical_path: logicalPath,
        json_pointer: pointer || "/"
      });
    }
    for (const key of Object.keys(node)) {
      if (deniedTraversalKeys.test(key)) continue;
      visit(node[key], `${pointer}/${jsonPointerEscape(key)}`);
    }
  }
  visit(value, "");
  return {sourceRecords, revisionRecords};
}

function manifestForRecords(root, expectedRecords) {
  const records = [...expectedRecords].sort((a, b) => a.logical_path.localeCompare(b.logical_path)).map(expected => {
    const absolute = path.join(root, expected.logical_path);
    const bytes = fs.readFileSync(absolute);
    const actual = {logical_path: expected.logical_path, sha256: sha256Bytes(bytes), size_bytes: bytes.length};
    if (actual.sha256 !== expected.sha256 || actual.size_bytes !== expected.size_bytes) {
      throw new Error(`${expected.logical_path}: frozen structured input drift`);
    }
    return actual;
  });
  const canonical = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  return {
    records,
    count: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
    manifest_sha256: sha256Bytes(canonical)
  };
}

function loadFingerprintedTerminalInputs(productionRepo, membership, snapshot) {
  const taskIndex = new Map(snapshot.tasks.map(task => [task.task_id, task]));
  const taskIds = [...new Set(membership.items.map((item, index) => {
    const view = phase0Proxy(item, new Set(["task_id"]), `membership.items[${index}].terminal-manifest`);
    return view.task_id;
  }))].sort();
  const expectedByPath = new Map();
  for (const taskId of taskIds) {
    const task = taskIndex.get(taskId);
    if (!task) throw new Error(`${taskId}: missing provenance task`);
    for (const dispatch of terminalDispatches(task)) {
      const record = {
        logical_path: dispatch.input_path,
        sha256: dispatch.input_fingerprint?.sha256,
        size_bytes: dispatch.input_fingerprint?.size_bytes
      };
      if (typeof record.sha256 !== "string" || !Number.isInteger(record.size_bytes)) {
        throw new Error(`${taskId}: terminal input fingerprint missing`);
      }
      const previous = expectedByPath.get(record.logical_path);
      if (previous && JSON.stringify(previous) !== JSON.stringify(record)) throw new Error(`${record.logical_path}: conflicting input fingerprints`);
      expectedByPath.set(record.logical_path, record);
    }
  }
  const records = [...expectedByPath.values()].sort((a, b) => a.logical_path.localeCompare(b.logical_path));
  const terminalInputs = new Map();
  for (const record of records) {
    assertSafeRelative(record.logical_path, "terminal input");
    const bytes = fs.readFileSync(path.join(productionRepo, record.logical_path));
    if (bytes.length !== record.size_bytes || sha256Bytes(bytes) !== record.sha256) {
      throw new Error(`${record.logical_path}: fingerprinted terminal input drift`);
    }
    terminalInputs.set(record.logical_path, JSON.parse(bytes.toString("utf8")));
  }
  const canonical = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
  return {
    terminalInputs,
    manifest: {
      records,
      count: records.length,
      bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
      manifest_sha256: sha256Bytes(canonical)
    }
  };
}

function groupExposureRecords(records, keyName) {
  const groups = new Map();
  for (const record of records) {
    const key = record[keyName];
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({logical_path: record.logical_path, json_pointer: record.json_pointer});
  }
  return [...groups].sort(([a], [b]) => a.localeCompare(b)).map(([key, evidence]) => ({
    [keyName]: key,
    evidence: evidence.sort((a, b) => a.logical_path.localeCompare(b.logical_path) || a.json_pointer.localeCompare(b.json_pointer))
  }));
}

function buildExposureIndex(root, frozenManifest) {
  const manifest = manifestForRecords(root, frozenManifest.records);
  if (
    manifest.count !== frozenManifest.count ||
    manifest.bytes !== frozenManifest.bytes ||
    manifest.manifest_sha256 !== frozenManifest.manifest_sha256
  ) throw new Error("tracked structured model-facing input manifest drift");
  const sourceRecords = [];
  const revisionRecords = [];
  for (const record of manifest.records) {
    const parsed = JSON.parse(fs.readFileSync(path.join(root, record.logical_path), "utf8"));
    const collected = collectStructuredExposures(parsed, record.logical_path);
    sourceRecords.push(...collected.sourceRecords);
    revisionRecords.push(...collected.revisionRecords);
  }
  const exposedContent = groupExposureRecords(sourceRecords, "content_key");
  const exposedRevisions = groupExposureRecords(revisionRecords, "revision_key");
  return {
    manifest,
    sourceRecords,
    revisionRecords,
    exposedContent,
    exposedRevisions,
    contentSet: new Set(exposedContent.map(record => record.content_key)),
    revisionSet: new Set(exposedRevisions.map(record => record.revision_key))
  };
}

function gitOutput(repo, args, encoding = "utf8") {
  return execFileSync("git", ["-C", repo, ...args], {encoding, maxBuffer: 128 * 1024 * 1024});
}

function decodeCanonicalUtf8(buffer, label) {
  try {
    return new TextDecoder("utf-8", {fatal: true}).decode(buffer);
  } catch (error) {
    throw new Error(`${label}: source artifact is not canonical UTF-8: ${error.message}`);
  }
}

function bindSource(row, args, bindings) {
  const binding = bindings[row.component];
  if (!binding) return {status: "UNSUPPORTED_COMPONENT", error: `no binding for ${row.component}`};
  if (!row.section.startsWith(binding.section_prefix)) return {status: "SOURCE_BINDING_FAILED", error: "section prefix mismatch"};
  const sectionRelative = row.section.slice(binding.section_prefix.length);
  try {
    assertSafeRelative(sectionRelative, `${row.task_id}/${row.original_revision_key}`);
  } catch (error) {
    return {status: "SOURCE_BINDING_FAILED", error: error.message};
  }
  if (binding.read_mode === "git_commit_blob") {
    const relativePath = path.posix.join(binding.repository_prefix, sectionRelative);
    try {
      assertSafeRelative(relativePath, `${row.task_id}/${row.original_revision_key}`);
      const buffer = gitOutput(args.engineRepo, ["show", `${binding.commit}:${relativePath}`], null);
      return {
        status: "BOUND",
        fileText: decodeCanonicalUtf8(buffer, relativePath),
        source_binding: {
          kind: "git_commit_blob",
          component: row.component,
          repository_alias: binding.repository_alias,
          commit: binding.commit,
          relative_path: relativePath,
          source_artifact_sha256: sha256Bytes(buffer),
          source_artifact_size_bytes: buffer.length
        }
      };
    } catch (error) {
      return {status: "SOURCE_FILE_MISSING", error: error.message};
    }
  }
  if (binding.read_mode === "working_tree_file_with_required_sha256") {
    try {
      const registeredRoot = path.resolve(args.dlcRoot, binding.dlc_subdirectory);
      if (!fs.statSync(registeredRoot).isDirectory()) throw new Error("registered DLC root is not a directory");
      const candidate = path.resolve(registeredRoot, sectionRelative);
      const realRoot = fs.realpathSync(registeredRoot);
      const realCandidate = fs.realpathSync(candidate);
      if (!isInside(realRoot, realCandidate)) throw new Error("DLC source escapes registered root");
      if (!fs.statSync(realCandidate).isFile()) throw new Error("DLC source is not a file");
      const buffer = fs.readFileSync(realCandidate);
      return {
        status: "BOUND",
        fileText: decodeCanonicalUtf8(buffer, sectionRelative),
        source_binding: {
          kind: "dlc_file_sha256",
          component: row.component,
          repository_alias: binding.repository_alias,
          commit: null,
          relative_path: toPosix(sectionRelative),
          source_artifact_sha256: sha256Bytes(buffer),
          source_artifact_size_bytes: buffer.length
        }
      };
    } catch (error) {
      return {status: "SOURCE_FILE_MISSING", error: error.message};
    }
  }
  return {status: "SOURCE_BINDING_FAILED", error: `unsupported read mode ${binding.read_mode}`};
}

function locateRow(row, args, bindings, cache) {
  const cacheKey = `${row.component}\0${row.section}\0${row.source}`;
  if (cache.has(cacheKey)) return cache.get(cacheKey);
  const bound = bindSource(row, args, bindings);
  if (bound.status !== "BOUND") {
    const failed = {...bound, source_occurrences: 0, occurrences: []};
    cache.set(cacheKey, failed);
    return failed;
  }
  const occurrences = normalizedOccurrences(bound.fileText, row.source);
  const result = {
    ...bound,
    status: occurrences.length === 0 ? "SOURCE_NOT_FOUND" : occurrences.length <= 2 ? "LOCATED_ACCEPTED" : "LOCATED_TOO_MANY",
    source_occurrences: occurrences.length,
    occurrences
  };
  cache.set(cacheKey, result);
  return result;
}

function hashRank(parts) {
  return sha256Bytes(parts.join("\0"));
}

export function taskFirstRoundRobin(rows, category, seed, limit = 60, cap = 6) {
  const byTask = new Map();
  for (const row of rows) {
    if (!byTask.has(row.task_id)) byTask.set(row.task_id, []);
    byTask.get(row.task_id).push(row);
  }
  const tasks = [...byTask].map(([taskId, taskRows]) => ({
    taskId,
    rank: hashRank([seed, category, "task", taskId]),
    rows: taskRows.sort((a, b) =>
      hashRank([seed, category, "row", a.task_id, a.original_revision_key]).localeCompare(hashRank([seed, category, "row", b.task_id, b.original_revision_key])) ||
      a.original_revision_key.localeCompare(b.original_revision_key) ||
      a.section.localeCompare(b.section)
    )
  })).sort((a, b) => a.rank.localeCompare(b.rank) || a.taskId.localeCompare(b.taskId));
  const selected = [];
  for (let round = 0; round < cap && selected.length < limit; round += 1) {
    for (const task of tasks) {
      if (selected.length >= limit) break;
      if (task.rows[round]) selected.push(task.rows[round]);
    }
  }
  if (selected.length < limit) throw new Error(`${category}: only ${selected.length}/${limit} rows available under task cap ${cap}`);
  return selected;
}

export function screenSourceOnlyRows({baseRows, exposure, locate, contract}) {
  const sourceSizeEligible = baseRows.filter(row => {
    const bytes = Buffer.from(row.source, "utf8");
    const canonicalUtf8 = new TextDecoder("utf-8", {fatal: true}).decode(bytes) === row.source;
    return canonicalUtf8 && bytes.length >= 1 && bytes.length <= 6000 && row.profile !== "term-name";
  });
  const classified = sourceSizeEligible.map(row => ({...row, category: classifyCategory(row)})).filter(row => row.category);
  const exposureEligible = classified.filter(row =>
    !exposure.revisionSet.has(revisionExposureKey(row.task_id, row.original_revision_key)) &&
    !exposure.contentSet.has(contentExposureKey(row.source))
  );
  const located = exposureEligible.map(row => ({...row, locator: locate(row)}));
  const locatorAccepted = located.filter(row => row.locator.status === "LOCATED_ACCEPTED" && [1, 2].includes(row.locator.source_occurrences));
  const byContent = new Map();
  const representativeOrder = (a, b) =>
    a.task_id.localeCompare(b.task_id) ||
    a.original_revision_key.localeCompare(b.original_revision_key) ||
    a.section.localeCompare(b.section) ||
    a.category.localeCompare(b.category);
  for (const row of [...locatorAccepted].sort(representativeOrder)) {
    const key = locatorContentKey(row.component, row.source);
    if (!byContent.has(key)) byContent.set(key, row);
  }
  const deduplicated = [...byContent.values()];
  const selectedByCategory = {};
  for (const category of ["Runtime", "Narrative"]) {
    selectedByCategory[category] = taskFirstRoundRobin(
      deduplicated.filter(row => row.category === category),
      category,
      contract.seed,
      contract.required_gates[category].items,
      contract.required_gates.per_task_per_category_maximum
    );
  }
  return {sourceSizeEligible, classified, exposureEligible, located, locatorAccepted, deduplicated, selectedByCategory};
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

export function utf8Prefix(value, maximumBytes) {
  if (Buffer.byteLength(value, "utf8") <= maximumBytes) return value;
  let result = "";
  let bytes = 0;
  for (const character of value) {
    const width = Buffer.byteLength(character, "utf8");
    if (bytes + width > maximumBytes) break;
    result += character;
    bytes += width;
  }
  return result;
}

export function utf8Suffix(value, maximumBytes) {
  if (Buffer.byteLength(value, "utf8") <= maximumBytes) return value;
  const characters = [...value];
  let result = "";
  let bytes = 0;
  for (let index = characters.length - 1; index >= 0; index -= 1) {
    const width = Buffer.byteLength(characters[index], "utf8");
    if (bytes + width > maximumBytes) break;
    result = characters[index] + result;
    bytes += width;
  }
  return result;
}

export function contextForOccurrence(fileText, occurrence, ordinal, sideByteCap = 2000) {
  const starts = lineStarts(fileText);
  const startLineIndex = lineIndexAt(starts, occurrence.rawStart);
  const endLineIndex = lineIndexAt(starts, Math.max(occurrence.rawStart, occurrence.rawEnd - 1));
  const beforeStart = starts[Math.max(0, startLineIndex - 12)];
  const afterEndIndex = Math.min(starts.length, endLineIndex + 13);
  const afterEnd = afterEndIndex < starts.length ? starts[afterEndIndex] : fileText.length;
  const before = utf8Suffix(fileText.slice(beforeStart, occurrence.rawStart), sideByteCap);
  const after = utf8Prefix(fileText.slice(occurrence.rawEnd, afterEnd), sideByteCap);
  const marker = `[[SOURCE_MATCH_${ordinal}]]`;
  const visibleContext = `${before}${marker}${after}`;
  const beforeBytes = Buffer.byteLength(before, "utf8");
  const afterBytes = Buffer.byteLength(after, "utf8");
  const visibleBytes = Buffer.byteLength(visibleContext, "utf8");
  if (beforeBytes > 2000 || afterBytes > 2000 || visibleBytes > 8192) throw new Error("context byte cap failure");
  return {
    occurrence_ordinal: ordinal,
    line_start: startLineIndex + 1,
    line_end: endLineIndex + 1,
    column_start: occurrence.rawStart - starts[startLineIndex] + 1,
    matched_span_sha256: sha256Bytes(fileText.slice(occurrence.rawStart, occurrence.rawEnd)),
    marker,
    lines_before: Math.min(12, startLineIndex),
    lines_after: Math.min(12, Math.max(0, starts.length - endLineIndex - 1)),
    before_utf8_bytes: beforeBytes,
    after_utf8_bytes: afterBytes,
    visible_context_utf8_bytes: visibleBytes,
    visible_context_sha256: sha256Bytes(visibleContext),
    visible_context: visibleContext
  };
}

function makePacket(selected, sideByteCap = 2000) {
  const occurrences = selected.locator.occurrences.map((occurrence, index) =>
    contextForOccurrence(selected.locator.fileText, occurrence, index + 1, sideByteCap)
  );
  const packet = {
    task_id: selected.task_id,
    original_revision_key: selected.original_revision_key,
    component: selected.component,
    section: selected.section,
    source_sha256: selected.source_sha256,
    source_binding: selected.locator.source_binding,
    source_occurrences: occurrences.length,
    occurrences
  };
  const visibleTotal = occurrences.reduce((sum, occurrence) => sum + occurrence.visible_context_utf8_bytes, 0);
  if (visibleTotal > 8192) throw new Error(`${selected.task_id}/${selected.original_revision_key}: combined visible context cap exceeded`);
  const withVisibleTotal = {...packet, combined_visible_context_utf8_bytes: visibleTotal};
  let supplementalBytes = 0;
  for (let attempt = 0; attempt < 8; attempt += 1) {
    const measured = Buffer.byteLength(JSON.stringify({...withVisibleTotal, supplemental_json_utf8_bytes: supplementalBytes}), "utf8");
    if (measured === supplementalBytes) break;
    supplementalBytes = measured;
  }
  const finalPacket = {...withVisibleTotal, supplemental_json_utf8_bytes: supplementalBytes};
  if (Buffer.byteLength(JSON.stringify(finalPacket), "utf8") !== supplementalBytes) throw new Error("supplemental JSON byte accounting did not converge");
  if (supplementalBytes > 12288 && sideByteCap > 0) return makePacket(selected, Math.max(0, sideByteCap - 128));
  if (supplementalBytes > 12288) throw new Error(`${selected.task_id}/${selected.original_revision_key}: supplemental JSON cap cannot be met`);
  return finalPacket;
}

function frameItem(row) {
  return {
    task_id: row.task_id,
    original_revision_key: row.original_revision_key,
    component: row.component,
    section: row.section,
    source_tag: row.source_tag,
    profile: row.profile,
    source: row.source,
    source_sha256: row.source_sha256,
    source_only_flags: row.source_only_flags
  };
}

function sourceArtifactManifest(packets) {
  const recordsByKey = new Map();
  for (const packet of packets) {
    const binding = packet.source_binding;
    const key = `${binding.component}\0${binding.relative_path}`;
    const record = {
      kind: binding.kind,
      component: binding.component,
      repository_alias: binding.repository_alias,
      commit: binding.commit,
      relative_path: binding.relative_path,
      sha256: binding.source_artifact_sha256,
      size_bytes: binding.source_artifact_size_bytes
    };
    const previous = recordsByKey.get(key);
    if (previous && JSON.stringify(previous) !== JSON.stringify(record)) throw new Error(`${key}: conflicting source artifact binding`);
    recordsByKey.set(key, record);
  }
  const records = [...recordsByKey.values()].sort((a, b) => a.component.localeCompare(b.component) || a.relative_path.localeCompare(b.relative_path));
  const canonical = records.map(record =>
    `${record.kind}\0${record.component}\0${record.repository_alias}\0${record.commit ?? ""}\0${record.relative_path}\0${record.sha256}\0${record.size_bytes}\n`
  ).join("");
  return {
    records,
    count: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
    manifest_sha256: sha256Bytes(canonical)
  };
}

export function assembleSourceOnlyPresentation(selectedByCategory, tomeCommit) {
  const categoryFrameItems = Object.fromEntries(Object.entries(selectedByCategory).map(([category, rows]) => [category, rows.map(frameItem)]));
  const categoryPackets = Object.fromEntries(Object.entries(selectedByCategory).map(([category, rows]) => [category, rows.map(row => makePacket(row))]));
  const presentationPayload = {
    schema_version: "prospective-source-only-presentation-v4",
    categories: ["Runtime", "Narrative"].map(category => ({
      category,
      items: categoryFrameItems[category],
      source_evidence_packets: categoryPackets[category]
    }))
  };
  return {
    categoryFrameItems,
    categoryPackets,
    presentationPayload,
    presentationSha256: sha256Bytes(canonicalBytes(presentationPayload)),
    sourceManifest: sourceArtifactManifest(Object.values(categoryPackets).flat()),
    tomeCommit
  };
}

function assertNoAbsolutePaths(bytes, label) {
  const text = bytes.toString("utf8");
  if (/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/u.test(text)) throw new Error(`${label}: local absolute path leaked`);
}

function writeOutput(out, name, value) {
  const bytes = jsonBytes(value);
  assertNoAbsolutePaths(bytes, name);
  fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, name), bytes);
  return {logical_name: name, sha256: sha256Bytes(bytes), size_bytes: bytes.length};
}

export function buildFrozenPackage(args) {
  const root = path.resolve(args.root ?? defaultRoot);
  const out = path.resolve(args.out ?? here);
  const contractPath = path.join(here, "SCREEN-CONTRACT.json");
  const contract = JSON.parse(fs.readFileSync(contractPath, "utf8"));
  if (contract.mode !== "NO_INFERENCE/SOURCE_SCREEN_ONLY" || contract.inference_allowed !== false) throw new Error("screen contract mode drift");
  const readFrozen = record => {
    const absolute = path.join(root, record.logical_path);
    const actual = sha256File(absolute);
    if (actual !== record.sha256) throw new Error(`${record.logical_path}: frozen hash drift ${actual}`);
    return absolute;
  };
  const membershipPath = readFrozen(contract.frozen_inputs.canonical_membership);
  const snapshotPath = readFrozen(contract.frozen_inputs.provenance_snapshot);
  readFrozen(contract.frozen_inputs.source_locator_contract);
  readFrozen(contract.frozen_inputs.executor_fixture);
  const expectedCommit = contract.source_bindings.tome.commit;
  const objectType = gitOutput(args.engineRepo, ["cat-file", "-t", `${expectedCommit}^{commit}`]).trim();
  if (objectType !== "commit") throw new Error("fixed Tome commit unavailable");

  const exposure = buildExposureIndex(root, contract.frozen_inputs.tracked_model_facing_structured_inputs);
  const membership = JSON.parse(fs.readFileSync(membershipPath, "utf8"));
  const snapshot = JSON.parse(fs.readFileSync(snapshotPath, "utf8"));
  if (membership.production_translation_commit !== contract.production_translation_commit) throw new Error("canonical membership production commit drift");
  if (snapshot.source_repo_head !== contract.production_translation_commit) throw new Error("provenance snapshot production commit drift");
  const loadedTerminal = loadFingerprintedTerminalInputs(args.productionRepo, membership, snapshot);
  if (contract.frozen_inputs.fingerprinted_terminal_input_manifest) {
    const expected = contract.frozen_inputs.fingerprinted_terminal_input_manifest;
    for (const field of ["count", "bytes", "manifest_sha256"]) {
      if (loadedTerminal.manifest[field] !== expected[field]) throw new Error(`fingerprinted terminal input manifest ${field} drift`);
    }
  }
  const baseRows = reconstructSourceOnlyBaseRows({membership, snapshot, terminalInputs: loadedTerminal.terminalInputs});
  if (baseRows.length !== 1396) throw new Error(`source-only base row count drift: ${baseRows.length}`);
  const sourceOnlyBaseFrame = makeSourceOnlyBaseFrame(baseRows, contract.production_translation_commit);
  const locatorCache = new Map();
  const screen = screenSourceOnlyRows({
    baseRows,
    exposure,
    locate: row => locateRow(row, args, contract.source_bindings, locatorCache),
    contract
  });
  const {sourceSizeEligible, classified, exposureEligible, located, locatorAccepted, deduplicated, selectedByCategory} = screen;
  const presentation = assembleSourceOnlyPresentation(selectedByCategory, expectedCommit);
  const {categoryFrameItems, categoryPackets, presentationSha256, sourceManifest} = presentation;
  const allSelected = Object.values(selectedByCategory).flat();
  const sourceScreenFrame = {
    schema_version: "prospective-source-screen-frame-v4",
    status: "FROZEN_SOURCE_ONLY_PRESENTATION",
    mode: "NO_INFERENCE/SOURCE_SCREEN_ONLY",
    source_only: true,
    model_calls_made: 0,
    network_calls_made: 0,
    presentation_sha256: presentationSha256,
    source_exposure_registry: "SOURCE-EXPOSURE-REGISTRY.json",
    counts: {
      items: allSelected.length,
      tasks: new Set(allSelected.map(row => row.task_id)).size,
      Runtime: {items: selectedByCategory.Runtime.length, tasks: new Set(selectedByCategory.Runtime.map(row => row.task_id)).size},
      Narrative: {items: selectedByCategory.Narrative.length, tasks: new Set(selectedByCategory.Narrative.map(row => row.task_id)).size}
    },
    categories: ["Runtime", "Narrative"].map(category => ({
      category,
      item_count: categoryFrameItems[category].length,
      task_count: new Set(categoryFrameItems[category].map(row => row.task_id)).size,
      items: categoryFrameItems[category]
    }))
  };
  const sourceEvidencePackets = {
    schema_version: "prospective-source-evidence-packets-v4",
    status: "FROZEN_SOURCE_ONLY_EVIDENCE",
    mode: "NO_INFERENCE/SOURCE_SCREEN_ONLY",
    source_only: true,
    presentation_sha256: presentationSha256,
    tome_commit: expectedCommit,
    source_artifact_manifest: sourceManifest,
    categories: ["Runtime", "Narrative"].map(category => ({category, packets: categoryPackets[category]}))
  };
  const frameBytes = jsonBytes(sourceScreenFrame);
  const packetsBytes = jsonBytes(sourceEvidencePackets);
  const baseFrameBytes = jsonBytes(sourceOnlyBaseFrame);
  const plannedOutputs = [
    {logical_path: "SOURCE-SCREEN-FRAME.json", role: "source_only_screen_items", sha256: sha256Bytes(frameBytes), size_bytes: frameBytes.length},
    {logical_path: "SOURCE-EVIDENCE-PACKETS.json", role: "fixed_public_source_context", sha256: sha256Bytes(packetsBytes), size_bytes: packetsBytes.length}
  ];
  const exposureRegistry = {
    schema_version: "prospective-source-exposure-registry-v4",
    status: "FROZEN_STRUCTURED_SOURCE_ONLY_EXPOSURE",
    mode: "NO_INFERENCE/SOURCE_SCREEN_ONLY",
    key_contract: {
      revision_key: "sha256(task_id + NUL + original_revision_key)",
      content_key: "sha256(normalize_source(source))",
      normalization: "actual whitespace and literal escaped n/r/t collapse to one ASCII space; leading and trailing whitespace removed"
    },
    raw_output_tier_used: false,
    tracked_model_facing_structured_input_manifest: exposure.manifest,
    counts: {
      source_field_records: exposure.sourceRecords.length,
      unique_content_keys: exposure.exposedContent.length,
      task_revision_records: exposure.revisionRecords.length,
      unique_revision_keys: exposure.exposedRevisions.length
    },
    exposed_content_keys: exposure.exposedContent,
    exposed_revision_keys: exposure.exposedRevisions,
    frozen_future_model_facing_structured_outputs: plannedOutputs,
    limitation: "This registry covers only the frozen Git-tracked structured outbound-input manifest. It makes no claim about untracked, deleted, external or provider-side content."
  };

  const locatorCounts = {};
  for (const row of located) locatorCounts[row.locator.status] = (locatorCounts[row.locator.status] ?? 0) + 1;
  const selectedTaskMaximum = Math.max(...["Runtime", "Narrative"].flatMap(category => {
    const counts = new Map();
    for (const row of selectedByCategory[category]) counts.set(row.task_id, (counts.get(row.task_id) ?? 0) + 1);
    return [...counts.values()];
  }));
  const buildReport = {
    schema_version: "prospective-source-context-build-report-v4",
    status: "PASS_SOURCE_SCREEN_GATES",
    mode: "NO_INFERENCE/SOURCE_SCREEN_ONLY",
    presentation_sha256: presentationSha256,
    source_only_base_frame_sha256: sha256Bytes(baseFrameBytes),
    counts: {
      source_only_base_rows: baseRows.length,
      source_only_base_tasks: new Set(baseRows.map(row => row.task_id)).size,
      source_size_and_non_term_rows: sourceSizeEligible.length,
      classified_rows: classified.length,
      classified_Runtime: classified.filter(row => row.category === "Runtime").length,
      classified_Narrative: classified.filter(row => row.category === "Narrative").length,
      rows_after_structured_source_exposure: exposureEligible.length,
      eligible_Runtime_after_structured_source_exposure: exposureEligible.filter(row => row.category === "Runtime").length,
      eligible_Narrative_after_structured_source_exposure: exposureEligible.filter(row => row.category === "Narrative").length,
      structured_source_exposure_exclusions: classified.length - exposureEligible.length,
      locator_statuses: locatorCounts,
      locator_accepted_rows: locatorAccepted.length,
      content_deduplicated_rows: deduplicated.length,
      content_duplicate_rows_removed: locatorAccepted.length - deduplicated.length,
      selected_items: allSelected.length,
      selected_tasks: new Set(allSelected.map(row => row.task_id)).size,
      selected_Runtime_tasks: new Set(selectedByCategory.Runtime.map(row => row.task_id)).size,
      selected_Narrative_tasks: new Set(selectedByCategory.Narrative.map(row => row.task_id)).size,
      selected_task_per_category_maximum: selectedTaskMaximum,
      selected_one_occurrence: allSelected.filter(row => row.locator.source_occurrences === 1).length,
      selected_two_occurrences: allSelected.filter(row => row.locator.source_occurrences === 2).length,
      selected_source_artifacts: sourceManifest.count
    },
    frozen_input_hashes: {
      canonical_membership_sha256: contract.frozen_inputs.canonical_membership.sha256,
      provenance_snapshot_sha256: contract.frozen_inputs.provenance_snapshot.sha256,
      fingerprinted_terminal_input_manifest_sha256: loadedTerminal.manifest.manifest_sha256,
      source_locator_contract_sha256: contract.frozen_inputs.source_locator_contract.sha256,
      tracked_structured_input_manifest_sha256: exposure.manifest.manifest_sha256,
      executor_fixture_sha256: contract.frozen_inputs.executor_fixture.sha256
    },
    fingerprinted_terminal_input_manifest: {
      count: loadedTerminal.manifest.count,
      bytes: loadedTerminal.manifest.bytes,
      manifest_sha256: loadedTerminal.manifest.manifest_sha256
    },
    source_artifact_manifest_sha256: sourceManifest.manifest_sha256,
    gates: {
      Runtime_items_60: selectedByCategory.Runtime.length === 60,
      Runtime_tasks_at_least_20: new Set(selectedByCategory.Runtime.map(row => row.task_id)).size >= 20,
      Narrative_items_60: selectedByCategory.Narrative.length === 60,
      Narrative_tasks_at_least_30: new Set(selectedByCategory.Narrative.map(row => row.task_id)).size >= 30,
      task_per_category_at_most_6: selectedTaskMaximum <= 6,
      mutually_exclusive_identity: new Set(allSelected.map(row => `${row.task_id}\0${row.original_revision_key}`)).size === allSelected.length,
      no_term_name: allSelected.every(row => row.profile !== "term-name"),
      no_duplicate_component_content: new Set(allSelected.map(row => locatorContentKey(row.component, row.source))).size === allSelected.length,
      locator_occurrences_one_or_two: allSelected.every(row => [1, 2].includes(row.locator.source_occurrences)),
      raw_output_tier_unused: true,
      model_calls_zero: true,
      network_calls_zero: true
    },
    no_go: [],
    next_gate: "NO-GO for inference: this package freezes only the source-only screen and fixed public-source presentation."
  };
  if (Object.values(buildReport.gates).some(value => value !== true)) throw new Error("one or more source screen gates failed");

  const outputs = [];
  outputs.push(writeOutput(out, "SOURCE-ONLY-BASE-FRAME.json", sourceOnlyBaseFrame));
  outputs.push(writeOutput(out, "SOURCE-SCREEN-FRAME.json", sourceScreenFrame));
  outputs.push(writeOutput(out, "SOURCE-EVIDENCE-PACKETS.json", sourceEvidencePackets));
  outputs.push(writeOutput(out, "SOURCE-EXPOSURE-REGISTRY.json", exposureRegistry));
  outputs.push(writeOutput(out, "BUILD-REPORT.json", buildReport));
  return {outputs, report: buildReport, base: sourceOnlyBaseFrame, frame: sourceScreenFrame, packets: sourceEvidencePackets, registry: exposureRegistry};
}

const invokedPath = process.argv[1] ? pathToFileURL(path.resolve(process.argv[1])).href : null;
if (invokedPath === import.meta.url) {
  const args = parseArgs(process.argv.slice(2));
  const result = buildFrozenPackage(args);
  process.stdout.write(`${JSON.stringify({status: result.report.status, presentation_sha256: result.report.presentation_sha256, counts: result.report.counts, outputs: result.outputs}, null, 2)}\n`);
}
