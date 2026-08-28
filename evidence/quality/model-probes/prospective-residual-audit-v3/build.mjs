#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const snapshotPath = path.resolve(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json");
const sourceAuditProtocolPath = path.join(here, "SOURCE-AUDIT-PROTOCOL.json");
const sourceLocatorContractPath = path.join(here, "SOURCE-LOCATOR-CONTRACT.json");
const snapshotSha256 = "b754183a9d1e0efa15cb1d3c16fa06a7f96f388e75707c7ba0e79f4a680f2eab";
const sourceAuditProtocolSha256 = "95d290e728956c0ac9efeeaa05164ba53d37e3d2a78790c7e3cf82b1b078c35b";
const sourceLocatorContractSha256 = "c0a8a52f2a2a99afe00881132d224ad14e2f82c91e77f61c735cb23be669313a";
const productionCommit = "1666481409f4c0d63d66e84659f6b6145d8d25d0";
const canonicalInventorySha256 = "bf9153e83aba7318741f065d8541ae74783eebc5d4552ec38627a4313456b215";
const seed = "prospective-residual-audit-v3|2026-08-27|canonical-task-first-systematic-pps-v1";
const quotas = {
  same_family_only: 24,
  cross_or_mixed_family: 14,
  unknown_provenance: 2
};
const expectedFrame = {
  same_family_only: {tasks: 30, revisions: 733},
  cross_or_mixed_family: {tasks: 14, revisions: 569},
  unknown_provenance: {tasks: 2, revisions: 94}
};
const expectedNoTerminalInput = [
  "p2-ashes-mechanics-b1-fix-001",
  "p2-ashes-status-b1-001",
  "p2-cults-mechanics-b1-fix-001",
  "p2-orcs-mechanics-b1-fix-001",
  "p2-orcs-status-b1-001"
];
const expectedResolutionExclusions = {noncanonical: 128, ambiguous: 0};
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
    if (!value || !["--repo", "--inventory", "--out"].includes(flag)) {
      throw new Error("usage: node build.mjs --repo SOURCE_REPO --inventory INVENTORY_JSONL [--out OUTPUT_DIR]");
    }
    args[flag.slice(2)] = path.resolve(value);
  }
  if (!args.repo || !args.inventory) throw new Error("--repo and --inventory are required");
  return args;
}

const args = parseArgs(process.argv.slice(2));
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const rank = (...parts) => sha256Bytes(parts.join("\0"));
const writeJson = (name, value) => fs.writeFileSync(path.join(args.out, name), `${JSON.stringify(value, null, 2)}\n`);
const itemKey = (taskId, revisionKey) => `${taskId}\0${revisionKey}`;
const exactKey = (component, source, target) => `${component}\0${source}\0${target}`;
const sourceKey = (component, source) => `${component}\0${source}`;

function readInventory(file) {
  const text = fs.readFileSync(file, "utf8");
  const rows = text.trimEnd().split("\n").filter(Boolean).map((line, index) => {
    try {
      return JSON.parse(line);
    } catch (error) {
      throw new Error(`invalid inventory JSON at line ${index + 1}: ${error.message}`);
    }
  });
  const digest = sha256Bytes(JSON.stringify(rows));
  if (digest !== canonicalInventorySha256) {
    throw new Error(`canonical inventory drift: ${digest}`);
  }
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

function componentForItem(taskId, claimedSection) {
  if (claimedSection?.startsWith("mod-tome/")) return "tome";
  if (claimedSection?.startsWith("tome-cults/")) return "cults";
  if (claimedSection?.startsWith("tome-orcs/")) return "orcs";
  if (claimedSection?.startsWith("tome-ashes-urhrok/")) return "ashes-urhrok";
  if (taskId.startsWith("p2-tome-texts-")) return "tome";
  if (taskId.startsWith("p2-orcs-")) return "orcs";
  if (taskId.startsWith("p2-cults-")) return "cults";
  if (taskId.startsWith("p2-ashes-")) return "ashes-urhrok";
  throw new Error(`${taskId}: no canonical component mapping`);
}

function normalizeSection(value) {
  let section = value.trim().replace(/[),.]+$/, "");
  if (section.startsWith("game/modules/tome/")) section = `mod-tome/${section.slice("game/modules/tome/".length)}`;
  return section;
}

function sectionFromContext(context) {
  const patterns = [
    /(?:^|[;\s])section\s*=\s*([^;\s]+)/i,
    /(?:^|[;\s])section\s+((?:mod-tome|tome-[^/\s;]+)\/[^;\s]+)/i,
    /fixed_source\s*=\s*(game\/modules\/tome\/[^@;\s]+)/i,
    /(?:^|[;\s])path\s*=\s*(game\/modules\/tome\/[^;\s]+)/i,
    /pinned engine source\s+(game\/modules\/tome\/[^;\s]+)\s+at commit/i
  ];
  for (const pattern of patterns) {
    const match = context.match(pattern);
    if (match) return normalizeSection(match[1]);
  }
  return null;
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
      const fixedContext = contexts.get(translation.revision_key);
      const item = {
        original_revision_key: translation.revision_key,
        source: translation.source,
        target: translation.target,
        fixed_context: fixedContext,
        claimed_section: sectionFromContext(fixedContext)
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
    const total = active.reduce((sum, entry) => sum + entry.memberships.length, 0);
    const scale = slots / total;
    const certain = active.filter(entry => scale * entry.memberships.length >= 1);
    if (!certain.length) {
      for (const entry of active) probabilities.set(entry.task.task_id, scale * entry.memberships.length);
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
  if (sampleSize === entries.length) {
    return {probabilities, selected: new Set(entries.map(entry => entry.task.task_id)), start: null};
  }
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
if (sha256File(sourceAuditProtocolPath) !== sourceAuditProtocolSha256) throw new Error("source audit protocol hash drift");
if (sha256File(sourceLocatorContractPath) !== sourceLocatorContractSha256) throw new Error("source locator contract hash drift");
const snapshot = JSON.parse(fs.readFileSync(snapshotPath, "utf8"));
if (snapshot.source_repo_head !== productionCommit) throw new Error("snapshot production commit drift");
const inventory = readInventory(args.inventory);

const exactIndex = new Map();
const sourceIndex = new Map();
for (const row of inventory) {
  const exact = exactKey(row.component, row.source, row.target);
  if (!exactIndex.has(exact)) exactIndex.set(exact, []);
  exactIndex.get(exact).push(row);
  const sourceOnly = sourceKey(row.component, row.source);
  if (!sourceIndex.has(sourceOnly)) sourceIndex.set(sourceOnly, []);
  sourceIndex.get(sourceOnly).push(row);
}

const priorExclusions = new Map();
const exclusionRecords = [];
for (const source of exclusionSources) {
  const absolute = path.resolve(here, source.path);
  if (sha256File(absolute) !== source.sha256) throw new Error(`${source.path}: exclusion source hash drift`);
  const value = JSON.parse(fs.readFileSync(absolute, "utf8"));
  for (const item of value.items ?? []) {
    const key = itemKey(item.task_id, item.original_revision_key);
    if (!priorExclusions.has(key)) priorExclusions.set(key, {task_id: item.task_id, original_revision_key: item.original_revision_key, reasons: []});
    priorExclusions.get(key).reasons.push(source.reason);
  }
  exclusionRecords.push({
    logical_path: source.path,
    sha256: source.sha256,
    reason: source.reason,
    item_records: value.items?.length ?? 0
  });
}
if (priorExclusions.size !== 88) throw new Error(`prior item exclusion drift: ${priorExclusions.size}`);

const pools = Object.fromEntries(Object.keys(quotas).map(stratum => [stratum, []]));
const noTerminalInput = [];
const resolutionExclusions = [];
const tasksWithoutCanonicalMembership = [];
let terminalPairsAfterPriorExclusion = 0;

for (const task of snapshot.tasks) {
  if (task.state !== "DONE" || !task.task_id.startsWith("p2-")) continue;
  const terminal = loadTerminal(task);
  if (!terminal.items.length) {
    noTerminalInput.push(task.task_id);
    continue;
  }
  const memberships = [];
  for (const item of terminal.items) {
    if (priorExclusions.has(itemKey(task.task_id, item.original_revision_key))) continue;
    terminalPairsAfterPriorExclusion += 1;
    const component = componentForItem(task.task_id, item.claimed_section);
    const exactMatches = exactIndex.get(exactKey(component, item.source, item.target)) ?? [];
    let matches = exactMatches;
    if (matches.length > 1 && item.claimed_section) {
      matches = matches.filter(match => match.section === item.claimed_section);
    }
    if (matches.length !== 1) {
      let reason;
      if (!exactMatches.length) {
        reason = (sourceIndex.get(sourceKey(component, item.source)) ?? []).length
          ? "CANONICAL_TARGET_MISMATCH"
          : "NON_CANONICAL_SOURCE_SNIPPET";
      } else if (!matches.length) {
        reason = "CANONICAL_SECTION_MISMATCH";
      } else if (!item.claimed_section) {
        reason = "AMBIGUOUS_CANONICAL_PAIR_NO_SECTION";
      } else {
        reason = "AMBIGUOUS_CANONICAL_PAIR_WITHIN_SECTION";
      }
      resolutionExclusions.push({
        task_id: task.task_id,
        original_revision_key: item.original_revision_key,
        component,
        reason,
        claimed_section: item.claimed_section,
        exact_pair_candidates: exactMatches.length,
        candidates_after_section: matches.length,
        source_sha256: sha256Bytes(item.source),
        target_sha256: sha256Bytes(item.target)
      });
      continue;
    }
    const canonical = matches[0];
    const membershipCore = {
      task_id: task.task_id,
      original_revision_key: item.original_revision_key,
      component,
      canonical_revision_id: canonical.revision_id,
      canonical_revision_uid: canonical.revision_uid,
      canonical_unit_id: canonical.unit_id,
      canonical_tu_uid: canonical.tu_uid,
      section: canonical.section,
      source_tag: canonical.source_tag,
      profile: canonical.profile,
      risk_flags: canonical.risk_flags,
      source_sha256: sha256Bytes(item.source),
      target_sha256: sha256Bytes(item.target)
    };
    memberships.push({
      ...membershipCore,
      membership_sha256: sha256Bytes(JSON.stringify(membershipCore)),
      translation_occurrences: canonical.occurrences,
      source: item.source,
      target: item.target,
      fixed_context: item.fixed_context,
      claimed_section: item.claimed_section
    });
  }
  if (!memberships.length) {
    tasksWithoutCanonicalMembership.push(task.task_id);
    continue;
  }
  const stratum = provenanceStratum(task);
  pools[stratum].push({task, terminal, memberships});
}

noTerminalInput.sort();
if (JSON.stringify(noTerminalInput) !== JSON.stringify(expectedNoTerminalInput)) {
  throw new Error(`task-without-terminal-revision drift: ${noTerminalInput.join(", ")}`);
}
const noncanonicalCount = resolutionExclusions.filter(item => !item.reason.startsWith("AMBIGUOUS_")).length;
const ambiguousCount = resolutionExclusions.filter(item => item.reason.startsWith("AMBIGUOUS_")).length;
if (noncanonicalCount !== expectedResolutionExclusions.noncanonical || ambiguousCount !== expectedResolutionExclusions.ambiguous) {
  throw new Error(`canonical resolution exclusion drift: noncanonical=${noncanonicalCount}, ambiguous=${ambiguousCount}`);
}

const observedFrame = Object.fromEntries(Object.entries(pools).map(([stratum, entries]) => [stratum, {
  tasks: entries.length,
  revisions: entries.reduce((sum, entry) => sum + entry.memberships.length, 0)
}]));
if (JSON.stringify(observedFrame) !== JSON.stringify(expectedFrame)) {
  throw new Error(`candidate frame drift: ${JSON.stringify(observedFrame)}`);
}

const frameTasks = [];
const allMemberships = [];
const selectedEntries = [];
const selectionDetails = {};
for (const [stratum, entries] of Object.entries(pools)) {
  const design = systematicPps(entries, quotas[stratum], stratum);
  selectionDetails[stratum] = {
    eligible_tasks: entries.length,
    eligible_canonical_revisions: entries.reduce((sum, entry) => sum + entry.memberships.length, 0),
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
      eligible_canonical_revisions: entry.memberships.length,
      task_inclusion_probability: taskProbability,
      pps_order_rank: rank(seed, "pps-order", stratum, taskId),
      selected
    });
    for (const membership of entry.memberships) {
      allMemberships.push({
        stratum,
        task_id: taskId,
        original_revision_key: membership.original_revision_key,
        canonical_revision_id: membership.canonical_revision_id,
        canonical_revision_uid: membership.canonical_revision_uid,
        canonical_unit_id: membership.canonical_unit_id,
        canonical_tu_uid: membership.canonical_tu_uid,
        component: membership.component,
        section: membership.section,
        source_tag: membership.source_tag,
        profile: membership.profile,
        risk_flags: membership.risk_flags,
        source_sha256: membership.source_sha256,
        target_sha256: membership.target_sha256,
        membership_sha256: membership.membership_sha256
      });
    }
    if (!selected) continue;
    const rankedItems = [...entry.memberships].sort((left, right) =>
      rank(seed, "revision", taskId, left.canonical_revision_id)
        .localeCompare(rank(seed, "revision", taskId, right.canonical_revision_id))
    );
    selectedEntries.push({
      stratum,
      task: entry.task,
      terminal: entry.terminal,
      membership: rankedItems[0],
      task_probability: taskProbability,
      item_probability_given_task: 1 / rankedItems.length,
      revision_rank: rank(seed, "revision", taskId, rankedItems[0].canonical_revision_id)
    });
  }
}

if (allMemberships.length !== 1396) throw new Error(`expected 1396 canonical memberships, got ${allMemberships.length}`);
if (selectedEntries.length !== 40) throw new Error(`expected 40 selected task/revision units, got ${selectedEntries.length}`);
selectedEntries.sort((left, right) =>
  rank(seed, "presentation", left.task.task_id, left.membership.canonical_revision_id)
    .localeCompare(rank(seed, "presentation", right.task.task_id, right.membership.canonical_revision_id))
);

const auditItems = selectedEntries.map((entry, index) => {
  const auditId = `R${String(index + 1).padStart(3, "0")}`;
  const membership = entry.membership;
  const inclusionProbability = entry.task_probability * entry.item_probability_given_task;
  return {
    audit_id: auditId,
    stratum: entry.stratum,
    task_id: entry.task.task_id,
    original_revision_key: membership.original_revision_key,
    canonical_identity: {
      component: membership.component,
      revision_id: membership.canonical_revision_id,
      revision_uid: membership.canonical_revision_uid,
      unit_id: membership.canonical_unit_id,
      tu_uid: membership.canonical_tu_uid,
      section: membership.section,
      source_tag: membership.source_tag,
      membership_sha256: membership.membership_sha256
    },
    source: membership.source,
    target: membership.target,
    fixed_context: membership.fixed_context,
    profile: membership.profile,
    risk_flags: membership.risk_flags,
    translation_occurrences: membership.translation_occurrences,
    task_inclusion_probability: entry.task_probability,
    item_probability_given_task: entry.item_probability_given_task,
    revision_inclusion_probability: inclusionProbability,
    design_weight: 1 / inclusionProbability,
    revision_rank: entry.revision_rank,
    presentation_rank: rank(seed, "presentation", entry.task.task_id, membership.canonical_revision_id),
    terminal_inputs: entry.terminal.inputs,
    item_sha256: sha256Bytes(JSON.stringify({
      task_id: entry.task.task_id,
      original_revision_key: membership.original_revision_key,
      canonical_revision_id: membership.canonical_revision_id,
      source: membership.source,
      target: membership.target,
      fixed_context: membership.fixed_context
    }))
  };
});

const canonicalMembership = {
  schema_version: "prospective-residual-canonical-membership-v3",
  status: "FROZEN_PRODUCTION_COMMIT_MEMBERSHIP",
  production_translation_commit: productionCommit,
  canonical_inventory_sha256: canonicalInventorySha256,
  membership_rule: "After item-level prior-experiment exclusion, component/source/target must resolve to exactly one canonical inventory revision. Frozen bounded-context section metadata may disambiguate repeated exact pairs; unresolved records are excluded, never manually assigned.",
  counts: {
    eligible_memberships: allMemberships.length,
    eligible_tasks: new Set(allMemberships.map(item => item.task_id)).size
  },
  items: allMemberships.sort((left, right) =>
    left.task_id.localeCompare(right.task_id) || left.canonical_revision_id.localeCompare(right.canonical_revision_id)
  )
};

const frame = {
  schema_version: "prospective-residual-audit-frame-v3",
  status: "FROZEN_CANDIDATE_FRAME",
  seed,
  snapshot: {
    logical_path: "../paseo-provenance-snapshot-v1/SNAPSHOT.json",
    sha256: snapshotSha256,
    source_repo_head: snapshot.source_repo_head
  },
  canonical_inventory: {
    production_translation_commit: productionCommit,
    canonical_sha256: canonicalInventorySha256
  },
  unit: "one uniquely production-resolved canonical revision from each selected task",
  item_exclusion_policy: "Exclude only task/revision pairs exposed in prior model experiments; do not exclude untouched revisions merely because another revision from the same task was exposed.",
  canonical_membership_policy: canonicalMembership.membership_rule,
  strata: {
    same_family_only: "candidate modifier and contextual reviewer are the same known model family only",
    cross_or_mixed_family: "known cross-family or known mixed-family reviewer relation",
    unknown_provenance: "candidate or reviewer family contains unresolved, unknown or mixed candidate provenance"
  },
  quota_rule: "Census the two capped strata (14 known cross/mixed and 2 unknown), then assign the remaining 24 of 40 slots to same-family.",
  selection_method: "Within each stratum, task-first systematic PPS without replacement using eligible canonical revision count as size; certainty tasks are peeled iteratively. One canonical revision is then selected uniformly by seeded SHA-256 rank within each selected task.",
  quotas,
  counts: selectionDetails,
  tasks: frameTasks.sort((left, right) => left.stratum.localeCompare(right.stratum) || left.pps_order_rank.localeCompare(right.pps_order_rank))
};

const auditQueue = {
  schema_version: "prospective-residual-audit-queue-v3",
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
  schema_version: "prospective-residual-audit-holdout-draft-v3",
  status: "NOT_FROZEN_FOR_INFERENCE",
  context_policy: "A_SOURCE_AND_TARGET_ONLY",
  instructions: "Draft only. Reviewer inference is prohibited until the source audit, sealed reference, estimators, missingness bounds, prompt, schema, scorer, routes and fail-closed preflight are separately frozen.",
  items: auditItems.map(item => ({audit_id: item.audit_id, source: item.source, target: item.target}))
};

const exclusions = {
  schema_version: "prospective-residual-audit-exclusions-v3",
  policy: "item-level prior-experiment exclusion followed by fail-closed canonical production membership",
  source_artifacts: exclusionRecords,
  prior_experiment_item_pairs: [...priorExclusions.values()]
    .map(item => ({...item, reasons: [...new Set(item.reasons)].sort()}))
    .sort((left, right) => left.task_id.localeCompare(right.task_id) || left.original_revision_key.localeCompare(right.original_revision_key)),
  frame_exclusions: noTerminalInput.map(task_id => ({
    task_id,
    reason: "NO_TERMINAL_TRANSLATION_REVISION"
  })),
  canonical_resolution_exclusions: resolutionExclusions.sort((left, right) =>
    left.task_id.localeCompare(right.task_id) || left.original_revision_key.localeCompare(right.original_revision_key)
  ),
  tasks_without_any_canonical_membership: tasksWithoutCanonicalMembership.sort()
};

const buildReport = {
  schema_version: "prospective-residual-audit-build-report-v3",
  status: "PASS",
  production_translation_commit: productionCommit,
  canonical_inventory_sha256: canonicalInventorySha256,
  frozen_contracts: {
    source_audit_protocol_sha256: sourceAuditProtocolSha256,
    source_locator_contract_sha256: sourceLocatorContractSha256
  },
  terminal_pairs_after_prior_item_exclusion: terminalPairsAfterPriorExclusion,
  prior_experiment_item_pairs_excluded: priorExclusions.size,
  canonical_resolution: {
    eligible_unique_memberships: allMemberships.length,
    noncanonical_exclusions: noncanonicalCount,
    ambiguous_exclusions: ambiguousCount
  },
  frame: observedFrame,
  selected_items: auditItems.length,
  selected_unique_tasks: new Set(auditItems.map(item => item.task_id)).size,
  model_calls_made: 0
};

const experiment = {
  schema_version: "prospective-residual-audit-experiment-v3",
  experiment: "prospective-residual-audit-v3",
  supersedes: "prospective-residual-audit-v2",
  status: "CANDIDATE_SET_SELECTED_SOURCE_AUDIT_PENDING",
  model_calls_made: 0,
  primary_estimand: "Design-weighted confirmed residual translation-defect rate in the frozen, uniquely production-resolved eligible P2 revision frame.",
  inference_scope: "The canonical production-commit frame defined by this snapshot, item-level prior-experiment exclusions and three provenance strata only.",
  selected_units: 40,
  unique_tasks_required: 40,
  context_policy: "A_SOURCE_AND_TARGET_ONLY",
  frozen_contracts: {
    source_audit_protocol: {
      logical_path: "SOURCE-AUDIT-PROTOCOL.json",
      sha256: sourceAuditProtocolSha256
    },
    source_locator_contract: {
      logical_path: "SOURCE-LOCATOR-CONTRACT.json",
      sha256: sourceLocatorContractSha256
    }
  },
  next_gate: "Complete and freeze the uniform four-state source audit for all 40 selected items; then define the sealed reference, exact weighted estimators, missingness bounds, prompt, schema, scorer, routes and fail-closed preflight before any model call.",
  stopping_rule: "No model inference and no item replacement while status is SOURCE_AUDIT_PENDING."
};

fs.mkdirSync(args.out, {recursive: true});
writeJson("EXPERIMENT.json", experiment);
writeJson("EXCLUSIONS.json", exclusions);
writeJson("CANONICAL-MEMBERSHIP.json", canonicalMembership);
writeJson("FRAME.json", frame);
writeJson("AUDIT-QUEUE.json", auditQueue);
writeJson("HOLDOUT-DRAFT.json", holdoutDraft);
writeJson("BUILD-REPORT.json", buildReport);
process.stdout.write(`${JSON.stringify({
  status: experiment.status,
  model_calls_made: 0,
  canonical_inventory_sha256: canonicalInventorySha256,
  frame: Object.fromEntries(Object.entries(observedFrame).map(([stratum, counts]) => [stratum, {...counts, selected_tasks: quotas[stratum]}])),
  canonical_resolution_exclusions: {noncanonical: noncanonicalCount, ambiguous: ambiguousCount},
  selected_items: auditItems.length,
  selected_unique_tasks: new Set(auditItems.map(item => item.task_id)).size
}, null, 2)}\n`);
