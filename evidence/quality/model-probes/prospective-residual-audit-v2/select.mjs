#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const snapshotPath = path.resolve(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json");
const snapshotSha256 = "b754183a9d1e0efa15cb1d3c16fa06a7f96f388e75707c7ba0e79f4a680f2eab";
const seed = "prospective-residual-audit-v2|2026-08-27|task-first-systematic-pps-v1";
const quotas = {
  same_family_only: 30,
  cross_or_mixed_family: 8,
  unknown_provenance: 2
};
const expectedFrame = {
  same_family_only: {tasks: 35, revisions: 847},
  cross_or_mixed_family: {tasks: 8, revisions: 329},
  unknown_provenance: {tasks: 2, revisions: 94}
};
const expectedNoTerminalInput = ["p2-orcs-status-b1-001"];
const exclusionSources = [
  {
    path: "../paseo-residual-audit-pilot-v1/PROVENANCE-KEY.json",
    sha256: "e0f43d3a9a977ee52a180e4ac00fdfdb00aadbf3cae6bac1b04405153b9a74e9",
    reason: "prior natural-residual pilot"
  },
  {
    path: "../controlled-mutation-reviewer-v1/SOURCE-CONTROLS.json",
    sha256: "beece1236a6cd78e975387571b03aff97bea12ae16f9000e0353e0f35583d16c",
    reason: "prior controlled-mutation experiment"
  },
  {
    path: "../controlled-mutation-ui-log-replication-v2/SOURCE-CONTROLS.json",
    sha256: "2bd638c45dc876a209805940d57e5496634050421004fd8bf3970fdaa2330764",
    reason: "prior UI/log replication experiment"
  },
  {
    path: "../runtime-source-context-pilot-v1/SOURCE-CONTROLS.json",
    sha256: "e2a56b5a68b613e75fc1f72818dd3cc2170aa789c8b1058d10c55da58b3c038b",
    reason: "prior source-context experiment"
  }
];

function parseArgs(argv) {
  const args = {out: here};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--repo", "--out"].includes(flag)) {
      throw new Error("usage: node select.mjs --repo SOURCE_REPO [--out OUTPUT_DIR]");
    }
    args[flag.slice(2)] = path.resolve(value);
  }
  if (!args.repo) throw new Error("--repo is required");
  return args;
}

const args = parseArgs(process.argv.slice(2));
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const rank = (...parts) => sha256Bytes(parts.join("\0"));
const writeJson = (name, value) => fs.writeFileSync(path.join(args.out, name), `${JSON.stringify(value, null, 2)}\n`);
const keyOf = (taskId, revisionKey) => `${taskId}\0${revisionKey}`;

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

function provenanceStratum(task) {
  const relation = task.candidate_reviewer_relation;
  if (relation === "same_family_only") return "same_family_only";
  if (
    relation === "unresolved" ||
    task.candidate_modifier?.family === "Unknown" ||
    task.candidate_modifier?.family === "Mixed" ||
    task.contextual_reviewer_families?.includes("Unknown")
  ) return "unknown_provenance";
  return "cross_or_mixed_family";
}

function loadTerminal(task) {
  const byRevision = new Map();
  const inputs = [];
  for (const dispatch of terminalDispatches(task)) {
    const absolute = path.join(args.repo, dispatch.input_path);
    if (!fs.existsSync(absolute)) throw new Error(`${task.task_id}: missing terminal input ${dispatch.input_path}`);
    const actualSize = fs.statSync(absolute).size;
    const actualHash = sha256File(absolute);
    if (
      dispatch.input_fingerprint?.sha256 !== actualHash ||
      dispatch.input_fingerprint?.size_bytes !== actualSize
    ) throw new Error(`${task.task_id}: terminal input fingerprint drift ${dispatch.input_path}`);
    const envelope = JSON.parse(fs.readFileSync(absolute, "utf8"));
    const payload = envelope.payload ?? envelope;
    if (!Array.isArray(payload.translation_snapshot) || !Array.isArray(payload.bounded_context)) {
      throw new Error(`${task.task_id}: invalid terminal input shape`);
    }
    const contexts = new Map(payload.bounded_context.map(entry => [entry.revision_key, entry.context]));
    for (const translation of payload.translation_snapshot) {
      if (!contexts.has(translation.revision_key)) throw new Error(`${task.task_id}/${translation.revision_key}: missing fixed context`);
      const item = {
        original_revision_key: translation.revision_key,
        source: translation.source,
        target: translation.target,
        fixed_context: contexts.get(translation.revision_key)
      };
      const previous = byRevision.get(item.original_revision_key);
      if (previous && JSON.stringify(previous) !== JSON.stringify(item)) {
        throw new Error(`${task.task_id}/${item.original_revision_key}: conflicting terminal revisions`);
      }
      byRevision.set(item.original_revision_key, item);
    }
    inputs.push({
      dispatch_id: dispatch.dispatch_id,
      cycle: dispatch.cycle ?? null,
      logical_path: dispatch.input_path,
      size_bytes: actualSize,
      sha256: actualHash,
      candidate_identity: dispatch.candidate_identity ?? envelope.candidate_identity ?? null
    });
  }
  return {items: [...byRevision.values()], inputs};
}

function inclusionProbabilities(entries, sampleSize) {
  if (sampleSize > entries.length) throw new Error("sample size exceeds stratum task count");
  const probabilities = new Map();
  let active = [...entries];
  let slots = sampleSize;
  while (active.length) {
    if (slots === active.length) {
      for (const entry of active) probabilities.set(entry.task.task_id, 1);
      break;
    }
    const total = active.reduce((sum, entry) => sum + entry.terminal.items.length, 0);
    const scale = slots / total;
    const certain = active.filter(entry => scale * entry.terminal.items.length >= 1);
    if (!certain.length) {
      for (const entry of active) probabilities.set(entry.task.task_id, scale * entry.terminal.items.length);
      break;
    }
    for (const entry of certain) probabilities.set(entry.task.task_id, 1);
    const certainIds = new Set(certain.map(entry => entry.task.task_id));
    active = active.filter(entry => !certainIds.has(entry.task.task_id));
    slots -= certain.length;
  }
  const totalProbability = [...probabilities.values()].reduce((sum, value) => sum + value, 0);
  if (Math.abs(totalProbability - sampleSize) > 1e-9) throw new Error(`inclusion probabilities sum to ${totalProbability}, expected ${sampleSize}`);
  return probabilities;
}

function unitIntervalFromHash(value) {
  const numerator = Number.parseInt(value.slice(0, 13), 16);
  return numerator / 0x10000000000000;
}

function systematicPps(entries, sampleSize, stratum) {
  const probabilities = inclusionProbabilities(entries, sampleSize);
  if (sampleSize === entries.length) return {probabilities, selected: new Set(entries.map(entry => entry.task.task_id)), start: null};
  const ordered = [...entries].sort((left, right) =>
    rank(seed, "pps-order", stratum, left.task.task_id).localeCompare(rank(seed, "pps-order", stratum, right.task.task_id))
  );
  const start = unitIntervalFromHash(rank(seed, "pps-start", stratum));
  const thresholds = Array.from({length: sampleSize}, (_, index) => start + index);
  const selected = new Set();
  let cumulative = 0;
  let thresholdIndex = 0;
  for (const entry of ordered) {
    const next = cumulative + probabilities.get(entry.task.task_id);
    while (thresholdIndex < thresholds.length && thresholds[thresholdIndex] < next - 1e-12) {
      if (thresholds[thresholdIndex] >= cumulative - 1e-12) selected.add(entry.task.task_id);
      thresholdIndex += 1;
    }
    cumulative = next;
  }
  if (selected.size !== sampleSize || thresholdIndex !== sampleSize) {
    throw new Error(`${stratum}: systematic PPS selected ${selected.size}/${sampleSize}`);
  }
  return {probabilities, selected, start};
}

if (sha256File(snapshotPath) !== snapshotSha256) throw new Error("provenance snapshot hash drift");
const snapshot = JSON.parse(fs.readFileSync(snapshotPath, "utf8"));

const excludedTasks = new Map();
const exclusionRecords = [];
for (const source of exclusionSources) {
  const absolute = path.resolve(here, source.path);
  if (sha256File(absolute) !== source.sha256) throw new Error(`${source.path}: exclusion source hash drift`);
  const value = JSON.parse(fs.readFileSync(absolute, "utf8"));
  const taskIds = [...new Set((value.items ?? []).map(item => item.task_id))].sort();
  for (const taskId of taskIds) {
    if (!excludedTasks.has(taskId)) excludedTasks.set(taskId, []);
    excludedTasks.get(taskId).push(source.reason);
  }
  exclusionRecords.push({
    logical_path: source.path,
    sha256: source.sha256,
    reason: source.reason,
    item_records: value.items?.length ?? 0,
    distinct_tasks: taskIds.length
  });
}

const pools = Object.fromEntries(Object.keys(quotas).map(stratum => [stratum, []]));
const noTerminalInput = [];
for (const task of snapshot.tasks) {
  if (task.state !== "DONE" || !task.task_id.startsWith("p2-")) continue;
  if (excludedTasks.has(task.task_id)) continue;
  const terminal = loadTerminal(task);
  if (!terminal.items.length) {
    noTerminalInput.push(task.task_id);
    continue;
  }
  const stratum = provenanceStratum(task);
  pools[stratum].push({task, terminal});
}

const observedFrame = Object.fromEntries(Object.entries(pools).map(([stratum, entries]) => [stratum, {
  tasks: entries.length,
  revisions: entries.reduce((sum, entry) => sum + entry.terminal.items.length, 0)
}]));
if (JSON.stringify(observedFrame) !== JSON.stringify(expectedFrame)) {
  throw new Error(`candidate frame drift: ${JSON.stringify(observedFrame)}`);
}
noTerminalInput.sort();
if (JSON.stringify(noTerminalInput) !== JSON.stringify(expectedNoTerminalInput)) {
  throw new Error(`task-without-terminal-revision drift: ${noTerminalInput.join(", ")}`);
}

const frameTasks = [];
const selectedEntries = [];
const selectionDetails = {};
for (const [stratum, entries] of Object.entries(pools)) {
  const design = systematicPps(entries, quotas[stratum], stratum);
  selectionDetails[stratum] = {
    eligible_tasks: entries.length,
    eligible_revisions: entries.reduce((sum, entry) => sum + entry.terminal.items.length, 0),
    selected_tasks: design.selected.size,
    systematic_start: design.start,
    census: entries.length === quotas[stratum]
  };
  for (const entry of entries) {
    const taskId = entry.task.task_id;
    const taskProbability = design.probabilities.get(taskId);
    const selected = design.selected.has(taskId);
    frameTasks.push({
      stratum,
      task_id: taskId,
      candidate_reviewer_relation: entry.task.candidate_reviewer_relation,
      candidate_modifier_family: entry.task.candidate_modifier?.family ?? "Unknown",
      contextual_reviewer_families: entry.task.contextual_reviewer_families,
      terminal_revisions: entry.terminal.items.length,
      task_inclusion_probability: taskProbability,
      pps_order_rank: rank(seed, "pps-order", stratum, taskId),
      selected
    });
    if (!selected) continue;
    const rankedItems = [...entry.terminal.items].sort((left, right) =>
      rank(seed, "revision", taskId, left.original_revision_key)
        .localeCompare(rank(seed, "revision", taskId, right.original_revision_key))
    );
    selectedEntries.push({
      stratum,
      task: entry.task,
      terminal: entry.terminal,
      item: rankedItems[0],
      task_probability: taskProbability,
      item_probability_given_task: 1 / rankedItems.length,
      revision_rank: rank(seed, "revision", taskId, rankedItems[0].original_revision_key)
    });
  }
}

if (selectedEntries.length !== 40) throw new Error(`expected 40 selected task/revision units, got ${selectedEntries.length}`);
selectedEntries.sort((left, right) =>
  rank(seed, "presentation", left.task.task_id, left.item.original_revision_key)
    .localeCompare(rank(seed, "presentation", right.task.task_id, right.item.original_revision_key))
);

const auditItems = selectedEntries.map((entry, index) => {
  const auditId = `R${String(index + 1).padStart(3, "0")}`;
  const inclusionProbability = entry.task_probability * entry.item_probability_given_task;
  return {
    audit_id: auditId,
    stratum: entry.stratum,
    task_id: entry.task.task_id,
    original_revision_key: entry.item.original_revision_key,
    source: entry.item.source,
    target: entry.item.target,
    fixed_context: entry.item.fixed_context,
    task_inclusion_probability: entry.task_probability,
    item_probability_given_task: entry.item_probability_given_task,
    revision_inclusion_probability: inclusionProbability,
    design_weight: 1 / inclusionProbability,
    revision_rank: entry.revision_rank,
    presentation_rank: rank(seed, "presentation", entry.task.task_id, entry.item.original_revision_key),
    terminal_inputs: entry.terminal.inputs,
    item_sha256: sha256Bytes(JSON.stringify(entry.item))
  };
});

const frame = {
  schema_version: "prospective-residual-audit-frame-v2",
  status: "FROZEN_CANDIDATE_FRAME",
  seed,
  snapshot: {
    logical_path: "../paseo-provenance-snapshot-v1/SNAPSHOT.json",
    sha256: snapshotSha256,
    source_repo_head: snapshot.source_repo_head
  },
  unit: "one terminal revision from each selected task",
  task_exclusion_policy: "Exclude the entire task if any of its revisions appeared in a prior model experiment or item-level reference.",
  strata: {
    same_family_only: "candidate modifier and contextual reviewer are the same known model family only",
    cross_or_mixed_family: "known cross-family or known mixed-family reviewer relation",
    unknown_provenance: "candidate or reviewer family contains unresolved, unknown or mixed candidate provenance"
  },
  selection_method: "Within each stratum, task-first systematic PPS without replacement using terminal revision count as size; certainty tasks are peeled iteratively. One revision is then selected uniformly by seeded SHA-256 rank within each selected task.",
  quotas,
  counts: selectionDetails,
  tasks: frameTasks.sort((left, right) => left.stratum.localeCompare(right.stratum) || left.pps_order_rank.localeCompare(right.pps_order_rank))
};

const auditQueue = {
  schema_version: "prospective-residual-audit-queue-v2",
  status: "SOURCE_AUDIT_PENDING",
  reviewer_inference_allowed: false,
  context_policy_for_later_model_review: "A_SOURCE_AND_TARGET_ONLY",
  source_audit_policy: "Before any reviewer output, audit all 40 items at equal depth against fixed public source and classify confirmed, refuted, indeterminate or unreachable. Do not replace an item after selection.",
  counts: {
    items: auditItems.length,
    tasks: new Set(auditItems.map(item => item.task_id)).size,
    by_stratum: Object.fromEntries(Object.keys(quotas).map(stratum => [stratum, auditItems.filter(item => item.stratum === stratum).length]))
  },
  items: auditItems
};

const holdoutDraft = {
  schema_version: "prospective-residual-audit-holdout-draft-v2",
  status: "NOT_FROZEN_FOR_INFERENCE",
  context_policy: "A_SOURCE_AND_TARGET_ONLY",
  instructions: "Draft only. Reviewer inference is prohibited until the source audit, sealed reference, prompt, schema, scorer, routes and preflight are separately frozen.",
  items: auditItems.map(item => ({audit_id: item.audit_id, source: item.source, target: item.target}))
};

const exclusions = {
  schema_version: "prospective-residual-audit-exclusions-v2",
  policy: "task-level exclusion for every prior model-experiment exposure",
  source_artifacts: exclusionRecords,
  excluded_distinct_tasks: excludedTasks.size,
  frame_exclusions: noTerminalInput.map(task_id => ({
    task_id,
    reason: "The frozen terminal contextual reviewer input contains no translation revision, so the task cannot supply the registered sampling unit."
  })),
  tasks: [...excludedTasks.entries()].sort(([left], [right]) => left.localeCompare(right)).map(([task_id, reasons]) => ({
    task_id,
    reasons: [...new Set(reasons)].sort()
  }))
};

const experiment = {
  schema_version: "prospective-residual-audit-experiment-v2",
  experiment: "prospective-residual-audit-v2",
  status: "CANDIDATE_SET_SELECTED_SOURCE_AUDIT_PENDING",
  model_calls_made: 0,
  primary_estimand: "Design-weighted confirmed residual translation-defect rate in the frozen eligible P2 terminal-revision frame.",
  inference_scope: "The frame defined by this snapshot, task-level prior-experiment exclusions and three provenance strata only.",
  selected_units: 40,
  unique_tasks_required: 40,
  context_policy: "A_SOURCE_AND_TARGET_ONLY",
  next_gate: "Complete and freeze the uniform source audit for all 40 selected items; then define the sealed reference, exact weighted estimators, missingness bounds, prompt, schema, scorer, routes and fail-closed preflight before any model call.",
  stopping_rule: "No model inference and no item replacement while status is SOURCE_AUDIT_PENDING."
};

fs.mkdirSync(args.out, {recursive: true});
writeJson("EXPERIMENT.json", experiment);
writeJson("EXCLUSIONS.json", exclusions);
writeJson("FRAME.json", frame);
writeJson("AUDIT-QUEUE.json", auditQueue);
writeJson("HOLDOUT-DRAFT.json", holdoutDraft);
process.stdout.write(`${JSON.stringify({
  status: experiment.status,
  model_calls_made: 0,
  frame: Object.fromEntries(Object.entries(observedFrame).map(([stratum, counts]) => [stratum, {...counts, selected_tasks: quotas[stratum]}])),
  selected_items: auditItems.length,
  selected_unique_tasks: new Set(auditItems.map(item => item.task_id)).size,
  outputs: ["EXPERIMENT.json", "EXCLUSIONS.json", "FRAME.json", "AUDIT-QUEUE.json", "HOLDOUT-DRAFT.json"]
}, null, 2)}\n`);
