#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath, pathToFileURL} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRepoRoot = path.resolve(here, "../../../..");

const frozen = Object.freeze({
  production_commit: "1666481409f4c0d63d66e84659f6b6145d8d25d0",
  membership_path: "evidence/quality/model-probes/prospective-residual-audit-v3/CANONICAL-MEMBERSHIP.json",
  membership_sha256: "477c0e97f59e4f29159ed7baa16b7ef5ddb4165cbe5785ad15b667eadfda2049",
  frame_path: "evidence/quality/model-probes/prospective-residual-audit-v3/FRAME.json",
  frame_sha256: "7964a9b82cd9bd3cf9617aecd84550487eb23ab03a78b466d29c5dc2ab888e2c",
  snapshot_path: "evidence/quality/model-probes/paseo-provenance-snapshot-v1/SNAPSHOT.json",
  snapshot_sha256: "b754183a9d1e0efa15cb1d3c16fa06a7f96f388e75707c7ba0e79f4a680f2eab",
  raw_manifest: {
    count: 122,
    bytes: 25470879,
    sha256: "ace4cce4ba5f61e98776a6577a34c2ff7f8e5efef487e773b1104386452272b3"
  },
  input_identity_manifest: {
    count: 14,
    bytes: 543016,
    sha256: "021b7911ff9ca06e2e18cf3d45e86db6262267f8156c7527e0d692a73ada0aa6"
  },
  expected: {
    base_rows: 1396,
    base_unique_pairs: 1332,
    base_tasks: 46,
    structured_exact_pair_rows_remaining: 1343,
    structured_containment_rows_remaining: 1292,
    alias_rows_remaining: 1289,
    confirmed_input_rows_remaining: 1289,
    confirmed_input_unique_pairs_remaining: 1250,
    confirmed_input_tasks_remaining: 45,
    task_identifier_pure_rows: 6,
    task_identifier_pure_tasks: 5
  }
});

const minimumCandidateFieldCharacters = 12;

const outboundPaths = Object.freeze([
  "evidence/quality/model-probes/controlled-mutation-reviewer-v1/HOLDOUT.json",
  "evidence/quality/model-probes/controlled-mutation-ui-log-replication-v2/HOLDOUT.json",
  "evidence/quality/model-probes/paseo-residual-audit-pilot-v1/HOLDOUT.json",
  "evidence/quality/model-probes/prospective-residual-audit-v3/PUBLIC-HOLDOUT.json",
  "evidence/quality/model-probes/runtime-source-context-pilot-v1/HOLDOUT-A.json",
  "evidence/quality/model-probes/runtime-source-context-pilot-v1/HOLDOUT-B.json",
  "evidence/quality/p1-batches/p1-b4-mechanics-numeric.json",
  "evidence/quality/p1-batches/p1-b7-args-order.json",
  "evidence/quality/p1-batches/p1-b8-args-order-census.json"
]);

const identityPaths = Object.freeze([
  "evidence/quality/model-probes/controlled-mutation-reviewer-v1/SOURCE-CONTROLS.json",
  "evidence/quality/model-probes/controlled-mutation-ui-log-replication-v2/SOURCE-CONTROLS.json",
  "evidence/quality/model-probes/paseo-residual-audit-pilot-v1/PROVENANCE-KEY.json",
  "evidence/quality/model-probes/prospective-residual-audit-v3/AUDIT-QUEUE.json",
  "evidence/quality/model-probes/runtime-source-context-pilot-v1/SOURCE-CONTROLS.json"
]);

const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const pairKey = (source, target) => `${source}\0${target}`;
const pairSha256 = (source, target) => sha256Bytes(pairKey(source, target));
const taskRevisionKey = (taskId, revisionKey) => `${taskId}\0${revisionKey}`;
const taskRevisionSha256 = (taskId, revisionKey) => sha256Bytes(taskRevisionKey(taskId, revisionKey));
const jsonPointerEscape = value => String(value).replaceAll("~", "~0").replaceAll("/", "~1");

function parseArgs(argv) {
  const args = {repo: null, root: defaultRepoRoot, out: here};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--repo", "--root", "--out"].includes(flag)) {
      throw new Error("usage: node build.mjs --repo SOURCE_REPO [--root RESEARCH_REPO] [--out OUTPUT_DIR]");
    }
    args[flag.slice(2)] = path.resolve(value);
  }
  if (!args.repo) throw new Error("--repo is required");
  return args;
}

function fileManifest(root, logicalPaths) {
  const records = [...logicalPaths].sort().map(logicalPath => {
    const absolute = path.join(root, logicalPath);
    if (!fs.statSync(absolute).isFile()) throw new Error(`not a regular file: ${logicalPath}`);
    return {
      logical_path: logicalPath,
      sha256: sha256File(absolute),
      size_bytes: fs.statSync(absolute).size
    };
  });
  const canonical = records.map(record =>
    `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`
  ).join("");
  return {
    records,
    count: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0),
    sha256: sha256Bytes(canonical)
  };
}

function assertManifest(actual, expected, label) {
  for (const field of ["count", "bytes", "sha256"]) {
    if (actual[field] !== expected[field]) {
      throw new Error(`${label} ${field} drift: expected ${expected[field]}, got ${actual[field]}`);
    }
  }
}

function isTrackedRawBasename(logicalPath) {
  const basename = path.basename(logicalPath);
  return basename.startsWith("RAW-") || basename === "RAW.stdout" || basename === "RAW.stderr";
}

function trackedRawPaths(root) {
  const output = execFileSync("git", ["ls-files", "-z", "--", "evidence/quality/model-probes"], {
    cwd: root,
    encoding: "utf8",
    maxBuffer: 32 * 1024 * 1024
  });
  return output.split("\0").filter(Boolean).filter(logicalPath =>
    isTrackedRawBasename(logicalPath) && fs.statSync(path.join(root, logicalPath)).isFile()
  ).sort();
}

function collectExactPairs(value, logicalPath) {
  const pairs = [];
  function visit(node, pointer) {
    if (Array.isArray(node)) {
      node.forEach((entry, index) => visit(entry, `${pointer}/${index}`));
      return;
    }
    if (!node || typeof node !== "object") return;
    if (typeof node.source === "string" && typeof node.target === "string") {
      pairs.push({
        source: node.source,
        target: node.target,
        logical_path: logicalPath,
        json_pointer: pointer || "/"
      });
    }
    for (const [key, entry] of Object.entries(node)) {
      visit(entry, `${pointer}/${jsonPointerEscape(key)}`);
    }
  }
  visit(value, "");
  return pairs;
}

function collectStringLeaves(value, logicalPath) {
  const leaves = [];
  function visit(node, pointer, parentKey) {
    if (typeof node === "string") {
      leaves.push({value: node, logical_path: logicalPath, json_pointer: pointer, key: parentKey});
      return;
    }
    if (Array.isArray(node)) {
      node.forEach((entry, index) => visit(entry, `${pointer}/${index}`, String(index)));
      return;
    }
    if (!node || typeof node !== "object") return;
    for (const [key, entry] of Object.entries(node)) {
      visit(entry, `${pointer}/${jsonPointerEscape(key)}`, key);
    }
  }
  visit(value, "", null);
  return leaves;
}

function unicodeCharacterLength(value) {
  return [...value].length;
}

function isRawCandidateEligible(value) {
  return unicodeCharacterLength(value) >= minimumCandidateFieldCharacters;
}

function containedOutboundFieldMatches(field, value, leaves) {
  if (!value.length) return [];
  const candidateCharacters = unicodeCharacterLength(value);
  return leaves.filter(leaf =>
    unicodeCharacterLength(leaf.value) > candidateCharacters && leaf.value.includes(value)
  ).map(leaf => ({
    method: `${field}_literal_in_longer_outbound_string_leaf`,
    logical_path: leaf.logical_path,
    json_pointer: leaf.json_pointer,
    key: leaf.key,
    candidate_characters: candidateCharacters,
    container_characters: unicodeCharacterLength(leaf.value)
  }));
}

function collectTaskRevisionRecords(value, logicalPath) {
  const records = [];
  function visit(node, pointer) {
    if (Array.isArray(node)) {
      node.forEach((entry, index) => visit(entry, `${pointer}/${index}`));
      return;
    }
    if (!node || typeof node !== "object") return;
    if (typeof node.task_id === "string" && typeof node.original_revision_key === "string") {
      records.push({
        task_id: node.task_id,
        original_revision_key: node.original_revision_key,
        logical_path: logicalPath,
        json_pointer: pointer || "/"
      });
    }
    for (const [key, entry] of Object.entries(node)) {
      visit(entry, `${pointer}/${jsonPointerEscape(key)}`);
    }
  }
  visit(value, "");
  return records;
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

function reconstructRows(sourceRepo, membership, snapshot) {
  const taskIndex = new Map(snapshot.tasks.map(task => [task.task_id, task]));
  const taskIds = [...new Set(membership.items.map(item => item.task_id))].sort();
  const terminalPairs = new Map();
  const terminalInputs = new Map();

  for (const taskId of taskIds) {
    const task = taskIndex.get(taskId);
    if (!task) throw new Error(`${taskId}: missing from provenance snapshot`);
    for (const dispatch of terminalDispatches(task)) {
      const logicalPath = dispatch.input_path;
      const absolute = path.join(sourceRepo, logicalPath);
      if (!fs.existsSync(absolute)) throw new Error(`${taskId}: missing terminal input ${logicalPath}`);
      const bytes = fs.readFileSync(absolute);
      const actual = {size_bytes: bytes.length, sha256: sha256Bytes(bytes)};
      if (
        actual.size_bytes !== dispatch.input_fingerprint?.size_bytes ||
        actual.sha256 !== dispatch.input_fingerprint?.sha256
      ) throw new Error(`${taskId}: terminal input fingerprint drift ${logicalPath}`);
      terminalInputs.set(logicalPath, {logical_path: logicalPath, ...actual});
      const envelope = JSON.parse(bytes.toString("utf8"));
      const payload = envelope.payload ?? envelope;
      if (!Array.isArray(payload.translation_snapshot)) {
        throw new Error(`${taskId}: terminal input lacks translation_snapshot`);
      }
      for (const item of payload.translation_snapshot) {
        const key = taskRevisionKey(taskId, item.revision_key);
        const pair = {source: item.source, target: item.target};
        const previous = terminalPairs.get(key);
        if (previous && pairKey(previous.source, previous.target) !== pairKey(pair.source, pair.target)) {
          throw new Error(`${taskId}/${item.revision_key}: conflicting terminal source/target`);
        }
        terminalPairs.set(key, pair);
      }
    }
  }

  const rows = membership.items.map(item => {
    const key = taskRevisionKey(item.task_id, item.original_revision_key);
    const pair = terminalPairs.get(key);
    if (!pair) throw new Error(`${item.task_id}/${item.original_revision_key}: terminal pair missing`);
    if (sha256Bytes(pair.source) !== item.source_sha256 || sha256Bytes(pair.target) !== item.target_sha256) {
      throw new Error(`${item.task_id}/${item.original_revision_key}: membership content hash mismatch`);
    }
    return {
      ...item,
      source: pair.source,
      target: pair.target,
      pair_sha256: pairSha256(pair.source, pair.target),
      task_revision_sha256: taskRevisionSha256(item.task_id, item.original_revision_key)
    };
  });
  return {rows, terminalInputs: [...terminalInputs.values()].sort((a, b) => a.logical_path.localeCompare(b.logical_path))};
}

function rawVariants(value) {
  const literal = Buffer.from(value);
  const escapedText = JSON.stringify(value).slice(1, -1);
  const variants = new Map();
  const add = (text, encoding) => {
    const hex = Buffer.from(text).toString("hex");
    if (!variants.has(hex)) variants.set(hex, {bytes: Buffer.from(text), encodings: []});
    variants.get(hex).encodings.push(encoding);
  };
  add(value, "literal_utf8");
  add(escapedText, "json_escaped_utf8");
  return [...variants.values()];
}

function countOccurrences(haystack, needle) {
  if (!needle.length) return 0;
  let count = 0;
  let offset = 0;
  while ((offset = haystack.indexOf(needle, offset)) !== -1) {
    count += 1;
    offset += Math.max(1, needle.length);
  }
  return count;
}

function firstOffset(haystack, needle) {
  return haystack.indexOf(needle);
}

function assertCount(actual, expected, label) {
  if (actual !== expected) throw new Error(`${label}: expected ${expected}, got ${actual}`);
}

function buildRegistry({root, repo, out}) {
  const readFrozenJson = (logicalPath, expectedSha256) => {
    const absolute = path.join(root, logicalPath);
    const actual = sha256File(absolute);
    if (actual !== expectedSha256) throw new Error(`${logicalPath}: hash drift ${actual}`);
    return JSON.parse(fs.readFileSync(absolute, "utf8"));
  };

  const membership = readFrozenJson(frozen.membership_path, frozen.membership_sha256);
  const frame = readFrozenJson(frozen.frame_path, frozen.frame_sha256);
  const snapshot = readFrozenJson(frozen.snapshot_path, frozen.snapshot_sha256);
  if (membership.production_translation_commit !== frozen.production_commit) throw new Error("membership production commit drift");
  if (frame.canonical_inventory?.production_translation_commit !== frozen.production_commit) throw new Error("frame production commit drift");
  if (snapshot.source_repo_head !== frozen.production_commit) throw new Error("snapshot production commit drift");

  const inputIdentityPaths = [...outboundPaths, ...identityPaths].sort();
  const inputIdentityManifest = fileManifest(root, inputIdentityPaths);
  assertManifest(inputIdentityManifest, frozen.input_identity_manifest, "input/identity manifest");
  const rawManifest = fileManifest(root, trackedRawPaths(root));
  assertManifest(rawManifest, frozen.raw_manifest, "RAW manifest");

  const {rows, terminalInputs} = reconstructRows(repo, membership, snapshot);
  const basePairs = new Map();
  for (const row of rows) {
    if (!basePairs.has(row.pair_sha256)) basePairs.set(row.pair_sha256, []);
    basePairs.get(row.pair_sha256).push(row);
  }
  assertCount(rows.length, frozen.expected.base_rows, "base rows");
  assertCount(basePairs.size, frozen.expected.base_unique_pairs, "base unique pairs");
  assertCount(new Set(rows.map(row => row.task_id)).size, frozen.expected.base_tasks, "base tasks");

  const parsedInputs = new Map(inputIdentityPaths.map(logicalPath => [
    logicalPath,
    JSON.parse(fs.readFileSync(path.join(root, logicalPath), "utf8"))
  ]));
  const outboundPairEvidence = [];
  const outboundStringLeaves = [];
  for (const logicalPath of outboundPaths) {
    const parsed = parsedInputs.get(logicalPath);
    outboundPairEvidence.push(...collectExactPairs(parsed, logicalPath));
    outboundStringLeaves.push(...collectStringLeaves(parsed, logicalPath));
  }
  const outboundPairIndex = new Map();
  for (const evidence of outboundPairEvidence) {
    const hash = pairSha256(evidence.source, evidence.target);
    if (!outboundPairIndex.has(hash)) outboundPairIndex.set(hash, []);
    outboundPairIndex.get(hash).push({logical_path: evidence.logical_path, json_pointer: evidence.json_pointer});
  }

  const allTaskRevisionRecords = [];
  const allInputTexts = new Map();
  for (const logicalPath of inputIdentityPaths) {
    allTaskRevisionRecords.push(...collectTaskRevisionRecords(parsedInputs.get(logicalPath), logicalPath));
    allInputTexts.set(logicalPath, fs.readFileSync(path.join(root, logicalPath), "utf8"));
  }
  const taskRevisionIndex = new Map();
  for (const record of allTaskRevisionRecords) {
    const key = taskRevisionKey(record.task_id, record.original_revision_key);
    if (!taskRevisionIndex.has(key)) taskRevisionIndex.set(key, []);
    taskRevisionIndex.get(key).push({logical_path: record.logical_path, json_pointer: record.json_pointer});
  }

  const identityMatchesByRow = new Map();
  const structuredExposedPairs = new Set(outboundPairIndex.keys());
  for (const row of rows) {
    const matches = [];
    const direct = taskRevisionIndex.get(taskRevisionKey(row.task_id, row.original_revision_key)) ?? [];
    for (const evidence of direct) matches.push({method: "task_plus_revision", ...evidence});
    const tokens = [
      ["canonical_revision_id", row.canonical_revision_id],
      ["canonical_revision_uid", row.canonical_revision_uid],
      ["source_sha256", row.source_sha256],
      ["target_sha256", row.target_sha256],
      ["pair_sha256", row.pair_sha256],
      ["task_revision_sha256", row.task_revision_sha256]
    ];
    for (const [method, token] of tokens) {
      for (const [logicalPath, text] of allInputTexts) {
        if (text.includes(token)) matches.push({method, logical_path: logicalPath});
      }
    }
    if (matches.length) {
      identityMatchesByRow.set(row.membership_sha256, matches);
      structuredExposedPairs.add(row.pair_sha256);
    }
  }

  const afterStructured = rows.filter(row => !structuredExposedPairs.has(row.pair_sha256));
  assertCount(afterStructured.length, frozen.expected.structured_exact_pair_rows_remaining, "rows after structured exact-pair/identity exposure");

  const structuredContainmentByPair = new Map();
  for (const [hash, pairRows] of basePairs) {
    if (structuredExposedPairs.has(hash)) continue;
    const representative = pairRows[0];
    const matches = [
      ...containedOutboundFieldMatches("source", representative.source, outboundStringLeaves),
      ...containedOutboundFieldMatches("target", representative.target, outboundStringLeaves)
    ];
    if (matches.length) structuredContainmentByPair.set(hash, matches);
  }
  const afterStructuredContainment = afterStructured.filter(row =>
    !structuredContainmentByPair.has(row.pair_sha256)
  );
  assertCount(
    afterStructuredContainment.length,
    frozen.expected.structured_containment_rows_remaining,
    "rows after longer outbound string-leaf containment exposure"
  );

  const inputSources = new Map();
  const inputTargets = new Map();
  for (const evidence of outboundPairEvidence) {
    if (!inputSources.has(evidence.source)) inputSources.set(evidence.source, []);
    if (!inputTargets.has(evidence.target)) inputTargets.set(evidence.target, []);
    inputSources.get(evidence.source).push({logical_path: evidence.logical_path, json_pointer: evidence.json_pointer});
    inputTargets.get(evidence.target).push({logical_path: evidence.logical_path, json_pointer: evidence.json_pointer});
  }
  const aliasEvidenceByPair = new Map();
  for (const [hash, pairRows] of basePairs) {
    if (structuredExposedPairs.has(hash)) continue;
    const representative = pairRows[0];
    const matches = [];
    for (const evidence of inputSources.get(representative.source) ?? []) matches.push({method: "source_only_exact_alias", ...evidence});
    for (const evidence of inputTargets.get(representative.target) ?? []) matches.push({method: "target_only_exact_alias", ...evidence});
    if (matches.length) aliasEvidenceByPair.set(hash, matches);
  }
  const afterAliases = afterStructuredContainment.filter(row => !aliasEvidenceByPair.has(row.pair_sha256));
  assertCount(afterAliases.length, frozen.expected.alias_rows_remaining, "rows after explicit input aliases");

  const rawBytes = new Map(rawManifest.records.map(record => [
    record.logical_path,
    fs.readFileSync(path.join(root, record.logical_path))
  ]));
  const remainingPairs = new Map();
  const rawScanRows = afterStructured.filter(row => !aliasEvidenceByPair.has(row.pair_sha256));
  for (const row of rawScanRows) {
    if (!remainingPairs.has(row.pair_sha256)) remainingPairs.set(row.pair_sha256, row);
  }
  const rawHitsByPair = new Map();
  for (const [hash, row] of remainingPairs) {
    const hits = [];
    for (const field of ["source", "target"]) {
      const value = row[field];
      if (!isRawCandidateEligible(value)) continue;
      for (const variant of rawVariants(value)) {
        for (const [logicalPath, bytes] of rawBytes) {
          const occurrences = countOccurrences(bytes, variant.bytes);
          if (!occurrences) continue;
          const anchors = outboundStringLeaves.filter(leaf => leaf.value.includes(value)).map(leaf => ({
            logical_path: leaf.logical_path,
            json_pointer: leaf.json_pointer,
            key: leaf.key
          }));
          hits.push({
            field,
            encodings: variant.encodings,
            logical_path: logicalPath,
            occurrences,
            first_byte_offset: firstOffset(bytes, variant.bytes),
            classification: anchors.length ? "CONFIRMED_TRACKED_INPUT" : "UNRESOLVED_RAW_LITERAL",
            classification_reason: anchors.length
              ? "The same candidate field is a literal substring of a string leaf in a frozen outbound input artifact."
              : "Literal occurrence exists in RAW, but the tracked corpus does not structurally prove it was model input rather than output/reasoning.",
            outbound_input_anchors: anchors
          });
        }
      }
    }
    if (hits.length) rawHitsByPair.set(hash, hits);
  }

  const confirmedRawPairs = new Set([...rawHitsByPair].filter(([, hits]) =>
    hits.some(hit => hit.classification === "CONFIRMED_TRACKED_INPUT")
  ).map(([hash]) => hash));
  const anyRawPairs = new Set(rawHitsByPair.keys());
  const confirmedRows = afterAliases.filter(row => !confirmedRawPairs.has(row.pair_sha256));
  const failClosedRows = afterAliases.filter(row => !anyRawPairs.has(row.pair_sha256));
  assertCount(confirmedRows.length, frozen.expected.confirmed_input_rows_remaining, "confirmed-input novel rows");
  assertCount(new Set(confirmedRows.map(row => row.pair_sha256)).size, frozen.expected.confirmed_input_unique_pairs_remaining, "confirmed-input novel unique pairs");
  assertCount(new Set(confirmedRows.map(row => row.task_id)).size, frozen.expected.confirmed_input_tasks_remaining, "confirmed-input novel tasks");

  const baseTasks = [...new Set(rows.map(row => row.task_id))].sort();
  const taskIdentifierPureTasks = baseTasks.filter(taskId =>
    [...allInputTexts.values()].every(text => !text.includes(taskId))
  );
  const taskIdentifierPureTaskSet = new Set(taskIdentifierPureTasks);
  const taskIdentifierPureRows = failClosedRows.filter(row => taskIdentifierPureTaskSet.has(row.task_id));
  assertCount(taskIdentifierPureRows.length, frozen.expected.task_identifier_pure_rows, "task-identifier-pure rows");
  assertCount(taskIdentifierPureTasks.length, frozen.expected.task_identifier_pure_tasks, "task-identifier-pure tasks");

  const exposurePairs = new Set([
    ...structuredExposedPairs,
    ...structuredContainmentByPair.keys(),
    ...aliasEvidenceByPair.keys(),
    ...anyRawPairs
  ]);
  const exposureEntries = [...exposurePairs].filter(hash => basePairs.has(hash)).sort().map(hash => {
    const pairRows = basePairs.get(hash);
    const representative = pairRows[0];
    return {
      pair_sha256: hash,
      source_sha256: representative.source_sha256,
      target_sha256: representative.target_sha256,
      memberships: pairRows.map(row => ({
        task_id: row.task_id,
        original_revision_key: row.original_revision_key,
        canonical_revision_id: row.canonical_revision_id,
        canonical_revision_uid: row.canonical_revision_uid,
        membership_sha256: row.membership_sha256,
        identity_matches: identityMatchesByRow.get(row.membership_sha256) ?? []
      })).sort((a, b) => a.task_id.localeCompare(b.task_id) || a.canonical_revision_id.localeCompare(b.canonical_revision_id)),
      structured_exact_pair_matches: outboundPairIndex.get(hash) ?? [],
      longer_outbound_string_leaf_matches: structuredContainmentByPair.get(hash) ?? [],
      explicit_input_alias_matches: aliasEvidenceByPair.get(hash) ?? [],
      raw_literal_matches: rawHitsByPair.get(hash) ?? [],
      excluded_from_confirmed_tracked_input_frame:
        structuredExposedPairs.has(hash) || structuredContainmentByPair.has(hash) ||
        aliasEvidenceByPair.has(hash) || confirmedRawPairs.has(hash),
      excluded_from_fail_closed_any_raw_frame:
        structuredExposedPairs.has(hash) || structuredContainmentByPair.has(hash) ||
        aliasEvidenceByPair.has(hash) || anyRawPairs.has(hash)
    };
  });

  const registry = {
    schema_version: "prior-exposure-registry-v1",
    status: "NO_INFERENCE/FRAME_BUILD_ONLY",
    scope: "Novelty against the frozen, Git-tracked artifact corpus listed by the two manifests; no claim about deleted, untracked, external, or unsaved model interactions.",
    production_translation_commit: frozen.production_commit,
    pair_hash_rule: "sha256(UTF8(source + NUL + target))",
    task_revision_hash_rule: "sha256(UTF8(task_id + NUL + original_revision_key))",
    structured_containment_rule: {
      candidate_requirement: "non-empty string; no length floor beyond non-empty",
      character_count: "Unicode code points",
      match: "Any non-empty candidate source or target is excluded when it is a literal substring of a strictly longer string leaf in a frozen outbound input JSON artifact.",
      rationale: "Known structured outbound input is direct exposure evidence even for short fields; strict longer-than excludes equality, which is handled by exact-pair/alias rules."
    },
    raw_rule: {
      tracked_path_rule: "git ls-files under evidence/quality/model-probes whose basename starts with RAW- or equals RAW.stdout or RAW.stderr",
      minimum_candidate_field_characters: minimumCandidateFieldCharacters,
      variants: ["literal UTF-8", "JSON-escaped UTF-8 without surrounding quotes"],
      confirmed_tier: "RAW hit plus literal-substring anchor in a frozen outbound input string leaf",
      fail_closed_tier: "any remaining RAW literal/JSON-escaped hit, including unresolved output/reasoning context"
    },
    inputs: {
      canonical_membership: {logical_path: frozen.membership_path, sha256: frozen.membership_sha256},
      frame: {logical_path: frozen.frame_path, sha256: frozen.frame_sha256},
      provenance_snapshot: {logical_path: frozen.snapshot_path, sha256: frozen.snapshot_sha256},
      terminal_reviewer_inputs: {count: terminalInputs.length, records: terminalInputs},
      outbound_paths: outboundPaths,
      identity_paths: identityPaths,
      input_identity_manifest: inputIdentityManifest,
      raw_manifest: rawManifest
    },
    counts: {
      base: {rows: rows.length, unique_pairs: basePairs.size, tasks: baseTasks.length},
      structured_exact_pair_and_identity: {
        rows_remaining: afterStructured.length,
        exposed_rows: rows.length - afterStructured.length,
        exposed_unique_pairs: [...structuredExposedPairs].filter(hash => basePairs.has(hash)).length,
        outbound_exact_pairs_total: outboundPairIndex.size
      },
      longer_outbound_string_leaf_containment: {
        rows_remaining: afterStructuredContainment.length,
        newly_exposed_rows: afterStructured.length - afterStructuredContainment.length,
        newly_exposed_unique_pairs: structuredContainmentByPair.size
      },
      explicit_input_alias: {
        rows_remaining: afterAliases.length,
        newly_exposed_rows: afterStructuredContainment.length - afterAliases.length,
        newly_exposed_unique_pairs: [...aliasEvidenceByPair].filter(([hash]) =>
          !structuredContainmentByPair.has(hash)
        ).length,
        total_matched_unique_pairs_including_earlier_containment: aliasEvidenceByPair.size
      },
      raw_literal_scan: {
        scan_population: "Pairs remaining after structured exact-pair/identity and explicit exact-field aliases; earlier longer-leaf containment pairs remain in this scan so their RAW evidence is retained.",
        candidate_pairs_with_any_hit: anyRawPairs.size,
        confirmed_tracked_input_pairs: confirmedRawPairs.size,
        unresolved_only_pairs: [...anyRawPairs].filter(hash => !confirmedRawPairs.has(hash)).length,
        literal_match_records: [...rawHitsByPair.values()].reduce((sum, hits) => sum + hits.length, 0)
      },
      confirmed_tracked_input_novel: {
        rows: confirmedRows.length,
        unique_pairs: new Set(confirmedRows.map(row => row.pair_sha256)).size,
        tasks: new Set(confirmedRows.map(row => row.task_id)).size
      },
      fail_closed_any_raw_literal_novel: {
        rows: failClosedRows.length,
        unique_pairs: new Set(failClosedRows.map(row => row.pair_sha256)).size,
        tasks: new Set(failClosedRows.map(row => row.task_id)).size
      },
      task_purity: {
        task_identifier_pure_rows: taskIdentifierPureRows.length,
        task_identifier_pure_tasks: taskIdentifierPureTasks.length
      }
    },
    task_purity: {
      rule: "A final-frame membership is task-identifier-pure only when its task_id is absent as a literal from every frozen input/identity artifact.",
      rows: taskIdentifierPureRows.map(row => ({
        task_id: row.task_id,
        original_revision_key: row.original_revision_key,
        pair_sha256: row.pair_sha256,
        membership_sha256: row.membership_sha256
      })),
      tasks: taskIdentifierPureTasks
    },
    exposure_pairs: exposureEntries,
    limitations: [
      "This registry proves novelty only relative to its frozen tracked manifests.",
      "Structured containment is a conservative exposure signal: a sufficiently long exact field embedded in a larger outbound string leaf is excluded even when the surrounding leaf is a prompt or serialized envelope.",
      "Literal matching cannot prove absence from provider memory or from artifacts that were never saved or tracked.",
      "Model/provider provenance appears in logical artifact names and must be removed before any external transmission."
    ]
  };

  const pairGroups = new Map();
  for (const row of failClosedRows) {
    if (!pairGroups.has(row.pair_sha256)) pairGroups.set(row.pair_sha256, []);
    pairGroups.get(row.pair_sha256).push(row);
  }
  const novelItems = [...pairGroups].sort(([left], [right]) => left.localeCompare(right)).map(([hash, pairRows]) => {
    const representative = pairRows[0];
    return {
      pair_sha256: hash,
      source: representative.source,
      target: representative.target,
      source_sha256: representative.source_sha256,
      target_sha256: representative.target_sha256,
      profiles: [...new Set(pairRows.map(row => row.profile))].sort(),
      risk_flags: [...new Set(pairRows.flatMap(row => row.risk_flags ?? []))].sort(),
      memberships: pairRows.map(row => ({
        stratum: row.stratum,
        task_id: row.task_id,
        original_revision_key: row.original_revision_key,
        canonical_revision_id: row.canonical_revision_id,
        canonical_revision_uid: row.canonical_revision_uid,
        canonical_unit_id: row.canonical_unit_id,
        canonical_tu_uid: row.canonical_tu_uid,
        component: row.component,
        section: row.section,
        source_tag: row.source_tag,
        profile: row.profile,
        risk_flags: row.risk_flags,
        membership_sha256: row.membership_sha256
      })).sort((a, b) => a.task_id.localeCompare(b.task_id) || a.canonical_revision_id.localeCompare(b.canonical_revision_id))
    };
  });
  const novelFrame = {
    schema_version: "context-evidence-novel-frame-v1",
    status: "NO_INFERENCE/FRAME_BUILD_ONLY",
    novelty_tier: "FAIL_CLOSED_ANY_RAW_LITERAL_NOVEL",
    unit: "one exact source/target pair; memberships preserve every canonical task/revision row",
    source_registry: {
      logical_path: "PRIOR-EXPOSURE-REGISTRY.json",
      sha256: null
    },
    counts: {
      canonical_rows: failClosedRows.length,
      unique_pairs: novelItems.length,
      tasks: new Set(failClosedRows.map(row => row.task_id)).size,
      task_identifier_pure_rows: taskIdentifierPureRows.length,
      task_identifier_pure_tasks: taskIdentifierPureTasks.length
    },
    task_purity: {
      rule: registry.task_purity.rule,
      rows: registry.task_purity.rows,
      tasks: taskIdentifierPureTasks
    },
    items: novelItems,
    limitation: "Novel only against the tracked corpus frozen in PRIOR-EXPOSURE-REGISTRY.json; this is not an unqualified never-seen claim."
  };

  fs.mkdirSync(out, {recursive: true});
  const finalRegistryText = `${JSON.stringify(registry, null, 2)}\n`;
  novelFrame.source_registry.sha256 = sha256Bytes(finalRegistryText);
  fs.writeFileSync(path.join(out, "PRIOR-EXPOSURE-REGISTRY.json"), finalRegistryText);
  fs.writeFileSync(path.join(out, "NOVEL-FRAME.json"), `${JSON.stringify(novelFrame, null, 2)}\n`);
  return {registry, novelFrame};
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  buildRegistry(parseArgs(process.argv.slice(2)));
}

export {
  buildRegistry,
  collectExactPairs,
  collectStringLeaves,
  collectTaskRevisionRecords,
  containedOutboundFieldMatches,
  fileManifest,
  isRawCandidateEligible,
  isTrackedRawBasename,
  pairSha256,
  rawVariants,
  taskRevisionSha256
};
