import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultSnapshot = path.join(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json");
const defaultExclusion = path.join(here, "../paseo-residual-audit-pilot-v1/PROVENANCE-KEY.json");
const seed = "controlled-mutation-reviewer-v1|2026-08-27";
const sampleSize = 24;

const mutationSpecs = {
  "p2-cults-status-b14-001\0cults-status-b14-001": {
    mutation_id: "MU01_DIRECTION_LONGER_TO_SHORTER",
    category: "direction",
    before: "持续时间延长 %d%%",
    after: "持续时间缩短 %d%%",
    expected_claim: "New debuffs last longer, not shorter."
  },
  "p2-orcs-status-b11-001\0orcs-status-b11-001": {
    mutation_id: "MU02_HOSTILITY_SCOPE_REMOVED",
    category: "target_scope",
    before: "敌方单位的近战或远程攻击命中目标时",
    after: "任意单位的近战或远程攻击命中目标时",
    expected_claim: "Only hostile attackers can trigger the flechette; the mutation expands the trigger to any unit."
  },
  "p2-orcs-status-b2-001\0orcs-status-b2-001": {
    mutation_id: "MU03_EXCLUDED_STAT_INCLUDED",
    category: "exception_scope",
    before: "除力量外的所有属性增加 %d。",
    after: "包括力量在内的所有属性增加 %d。",
    expected_claim: "Strength is excluded by the runtime effect and must not be included."
  },
  "p2-orcs-status-b21-001\0orcs-status-b21-001": {
    mutation_id: "MU04_DURATION_THREE_TO_TWO",
    category: "duration",
    before: "眩晕 3 回合",
    after: "眩晕 2 回合",
    expected_claim: "The runtime default daze duration is 3 turns, despite the stale English status string saying 2."
  },
  "p2-orcs-status-b4-001\0orcs-status-b4-001": {
    mutation_id: "MU05_GRACE_PERIOD_FOUR_TO_ONE",
    category: "duration",
    before: "若未能在四回合内恢复视线",
    after: "若未能在一回合内恢复视线",
    expected_claim: "The out-of-sight effect lasts four turns, not one."
  },
  "p2-orcs-status-b15-001\0orcs-status-b15-001": {
    mutation_id: "MU06_REMOVAL_CONDITION_NEGATED",
    category: "condition_polarity",
    before: "命中其他敌人则效果结束",
    after: "命中其他敌人则效果不会结束",
    expected_claim: "A hit on a different actor removes the effect; the mutation negates that rule."
  },
  "p2-cults-status-b7-001\0cults-status-b7-003": {
    mutation_id: "MU07_EXTENSION_SIX_TO_THREE",
    category: "duration",
    before: "持续时间延长6回合",
    after: "持续时间延长3回合",
    expected_claim: "Detrimental effects are extended by 6 turns, not 3."
  },
  "p2-orcs-status-b7-001\0orcs-status-b7-001": {
    mutation_id: "MU08_INCLUSIVE_THRESHOLD_TO_STRICT",
    category: "threshold_boundary",
    before: "至少相当于最大生命值 8%%",
    after: "超过最大生命值 8%%",
    expected_claim: "Exactly 8% damage triggers; the mutation incorrectly makes the threshold strictly greater than 8%."
  },
  "p2-orcs-status-b25-001\0orcs-status-b25-001": {
    mutation_id: "MU09_MANUAL_TO_AUTOMATIC_FIRE",
    category: "trigger_mode",
    before: "可手动使用火箭弹幕再次发射",
    after: "每回合自动使用火箭弹幕再次发射",
    expected_claim: "Rocket Barrage is manually activated; the effect does not auto-fire it every turn."
  },
  "p2-cults-status-b5-001\0cults-status-b5-001": {
    mutation_id: "MU10_DAMAGE_BONUS_SIGN_FLIPPED",
    category: "sign",
    before: "%d 层, +%d%% 所有造成的伤害。",
    after: "%d 层, -%d%% 所有造成的伤害。",
    expected_claim: "Chaos Orbs increases all damage; the mutation changes the bonus to a penalty."
  },
  "p2-cults-status-b18-001\0cults-status-b18-001": {
    mutation_id: "MU11_DEACTIVATION_TO_EACH_TURN",
    category: "timing",
    before: "暂停结束时",
    after: "每回合",
    expected_claim: "Negative effects and cooldowns are shortened when Suspend deactivates, not every turn."
  },
  "p2-orcs-status-b19-001\0orcs-status-b19-001": {
    mutation_id: "MU12_ACCUMULATION_NEGATED",
    category: "state_accumulation",
    before: "已格挡伤害可累积至上限",
    after: "已格挡伤害无法累积",
    expected_claim: "Successive blocked damage accumulates up to max_power; the mutation denies accumulation."
  }
};

function parseArgs(argv) {
  const args = {snapshot: defaultSnapshot, exclusion: defaultExclusion, out: here};
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (!["--repo", "--snapshot", "--exclusion", "--out"].includes(flag) || !argv[index + 1]) {
      throw new Error("usage: node build.mjs --repo SOURCE_REPO [--snapshot FILE] [--exclusion FILE] [--out DIR]");
    }
    args[flag.slice(2)] = path.resolve(argv[++index]);
  }
  if (!args.repo) throw new Error("--repo is required");
  return args;
}

function sha256Bytes(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function sha256File(file) {
  return sha256Bytes(fs.readFileSync(file));
}

function rank(...parts) {
  return sha256Bytes([seed, ...parts].join("\0"));
}

function writeJson(file, value) {
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function terminalInputs(task, sourceRepo) {
  let dispatches = task.dispatches.filter(dispatch =>
    dispatch.role === "REVIEWER" &&
    dispatch.purpose === "translation_contextual_v1" &&
    dispatch.input_path
  );
  let basis = "terminal_reviewer_dispatch";
  if (dispatches.length > 0) {
    const withCycle = dispatches.filter(dispatch => Number.isFinite(dispatch.cycle));
    if (withCycle.length > 0) {
      const terminalCycle = Math.max(...withCycle.map(dispatch => dispatch.cycle));
      dispatches = withCycle.filter(dispatch => dispatch.cycle === terminalCycle);
    } else {
      dispatches = [dispatches.at(-1)];
    }
  } else {
    const taskDir = path.join(sourceRepo, ".ai/task", task.task_id);
    const statePath = path.join(taskDir, "STATE.json");
    if (fs.existsSync(statePath)) {
      const state = JSON.parse(fs.readFileSync(statePath, "utf8"));
      if (state.contextual_input_path) {
        dispatches = [{input_path: state.contextual_input_path, dispatch_id: "STATE.contextual_input_path"}];
        basis = "state_contextual_input_path_fallback";
      }
    }
    if (dispatches.length === 0) {
      const envelopes = fs.readdirSync(taskDir).filter(name => /^CONTEXTUAL-ENVELOPE.*\.json$/.test(name));
      if (envelopes.length === 1) {
        dispatches = [{
          input_path: path.posix.join(".ai/task", task.task_id, envelopes[0]),
          dispatch_id: "unique-envelope-fallback"
        }];
        basis = "unique_contextual_envelope_fallback";
      }
    }
  }
  return {basis, dispatches};
}

function replaceExactlyOnce(target, before, after, key) {
  const first = target.indexOf(before);
  if (first === -1 || target.indexOf(before, first + before.length) !== -1) {
    throw new Error(`${key}: mutation before-text must occur exactly once`);
  }
  return `${target.slice(0, first)}${after}${target.slice(first + before.length)}`;
}

function sanitizeContext(context) {
  const sanitized = context
    .replaceAll("/home/yun/projects/tome4-dlcs/orcs/", "")
    .replaceAll("/home/yun/projects/t-engine4/", "");
  if (/\/(?:home|Users)\//.test(sanitized)) throw new Error("unhandled local absolute path in fixed context");
  return sanitized;
}

const args = parseArgs(process.argv.slice(2));
const snapshot = JSON.parse(fs.readFileSync(args.snapshot, "utf8"));
const exclusion = JSON.parse(fs.readFileSync(args.exclusion, "utf8"));
const sourceHead = execFileSync("git", ["rev-parse", "HEAD"], {cwd: args.repo, encoding: "utf8"}).trim();
if (sourceHead !== snapshot.source_repo_head) {
  throw new Error(`source HEAD mismatch: snapshot=${snapshot.source_repo_head}, repo=${sourceHead}`);
}
const excludedPairs = new Set(exclusion.items.map(item => `${item.task_id}\0${item.original_revision_key}`));

const populationByKey = new Map();
for (const task of snapshot.tasks) {
  if (task.state !== "DONE" || !/^p2-(?:ashes|cults|orcs)-(?:status|mechanics)/.test(task.task_id)) continue;
  const terminal = terminalInputs(task, args.repo);
  for (const dispatch of terminal.dispatches) {
    const absoluteInput = path.join(args.repo, dispatch.input_path);
    const envelope = JSON.parse(fs.readFileSync(absoluteInput, "utf8"));
    const payload = envelope.payload ?? envelope;
    const contexts = new Map(payload.bounded_context.map(entry => [entry.revision_key, entry.context]));
    for (const translation of payload.translation_snapshot) {
      const key = `${task.task_id}\0${translation.revision_key}`;
      if (excludedPairs.has(key)) continue;
      const item = {
        task_id: task.task_id,
        original_revision_key: translation.revision_key,
        source: translation.source,
        clean_target: translation.target,
        fixed_context: sanitizeContext(contexts.get(translation.revision_key)),
        terminal_input: {
          resolution_basis: terminal.basis,
          dispatch_id: dispatch.dispatch_id ?? null,
          logical_path: dispatch.input_path,
          sha256: sha256File(absoluteInput),
          candidate_identity: dispatch.candidate_identity ?? envelope.candidate_identity ?? null
        }
      };
      const existing = populationByKey.get(key);
      if (existing && JSON.stringify(existing) !== JSON.stringify(item)) {
        throw new Error(`conflicting terminal item: ${key}`);
      }
      populationByKey.set(key, item);
    }
  }
}

const population = [...populationByKey.values()].map(item => ({
  ...item,
  selection_rank: sha256Bytes([seed, item.task_id, item.original_revision_key].join("\0"))
})).sort((left, right) => left.selection_rank.localeCompare(right.selection_rank));
const selected = population.slice(0, sampleSize);
if (selected.length !== sampleSize) throw new Error(`expected ${sampleSize} selected items, got ${selected.length}`);

for (const [index, item] of selected.entries()) {
  const key = `${item.task_id}\0${item.original_revision_key}`;
  const shouldMutate = index % 2 === 0;
  if (shouldMutate !== Object.hasOwn(mutationSpecs, key)) {
    throw new Error(`${key}: mutation table does not match odd/even rank assignment at rank ${index + 1}`);
  }
  const mutation = mutationSpecs[key] ?? null;
  item.selection_rank_number = index + 1;
  item.label = mutation ? "INJECTED_MUTATION" : "UNMODIFIED_CONTROL";
  item.mutation = mutation;
  item.presented_target = mutation
    ? replaceExactlyOnce(item.clean_target, mutation.before, mutation.after, key)
    : item.clean_target;
  item.presentation_rank = rank("present", item.task_id, item.original_revision_key);
}

selected.sort((left, right) => left.presentation_rank.localeCompare(right.presentation_rank));
const holdoutItems = [];
const referenceItems = [];
const sourceControls = [];
for (const [index, item] of selected.entries()) {
  const revisionId = `C${String(index + 1).padStart(3, "0")}`;
  holdoutItems.push({
    revision_id: revisionId,
    source: item.source,
    target: item.presented_target,
    fixed_context: item.fixed_context
  });
  referenceItems.push({
    revision_id: revisionId,
    label: item.label,
    mutation_id: item.mutation?.mutation_id ?? null,
    category: item.mutation?.category ?? null,
    expected_claim: item.mutation?.expected_claim ?? null,
    before: item.mutation?.before ?? null,
    after: item.mutation?.after ?? null
  });
  sourceControls.push({
    revision_id: revisionId,
    task_id: item.task_id,
    original_revision_key: item.original_revision_key,
    selection_rank: item.selection_rank,
    selection_rank_number: item.selection_rank_number,
    label: item.label,
    source: item.source,
    clean_target: item.clean_target,
    presented_target: item.presented_target,
    fixed_context: item.fixed_context,
    terminal_input: item.terminal_input,
    clean_item_sha256: sha256Bytes(JSON.stringify({
      source: item.source,
      target: item.clean_target,
      fixed_context: item.fixed_context
    }))
  });
}

const holdout = {
  schema_version: "controlled-mutation-reviewer-holdout-v1",
  instructions: "Review every item independently in the given order. Historical provenance and mutation records are withheld.",
  items: holdoutItems
};
const reference = {
  schema_version: "controlled-mutation-reference-v1",
  visible_to_reviewers: false,
  labels_are_injection_records_not_claims_that_all_controls_are_naturally_clean: true,
  items: referenceItems
};
const controls = {
  schema_version: "controlled-mutation-source-controls-v1",
  visible_to_reviewers: false,
  source_repo_head: sourceHead,
  items: sourceControls
};
const sampling = {
  schema_version: "controlled-mutation-sampling-v1",
  seed,
  source_repo_head: sourceHead,
  snapshot_sha256: sha256File(args.snapshot),
  exclusion_sha256: sha256File(args.exclusion),
  population_rules: "P2 DONE ashes/cults/orcs status or mechanics terminal contextual revisions, excluding all paseo-residual-audit-pilot-v1 task/revision pairs",
  eligible_revisions: population.length,
  selected_revisions: sampleSize,
  selection: "lowest 24 SHA-256 ranks",
  assignment: "odd selection ranks receive preregistered mutations; even ranks remain unmodified controls",
  presentation: "independent SHA-256 shuffle; task IDs, original revision keys, clean targets, labels and mutation records are hidden",
  selected_population: selected.slice().sort((left, right) => left.selection_rank_number - right.selection_rank_number).map(item => ({
    selection_rank_number: item.selection_rank_number,
    task_id: item.task_id,
    original_revision_key: item.original_revision_key,
    selection_rank: item.selection_rank,
    assignment: item.label,
    mutation_id: item.mutation?.mutation_id ?? null
  }))
};

fs.mkdirSync(args.out, {recursive: true});
writeJson(path.join(args.out, "HOLDOUT.json"), holdout);
writeJson(path.join(args.out, "REFERENCE.json"), reference);
writeJson(path.join(args.out, "SOURCE-CONTROLS.json"), controls);
writeJson(path.join(args.out, "SAMPLING.json"), sampling);
process.stdout.write(JSON.stringify({
  source_repo_head: sourceHead,
  eligible_revisions: population.length,
  selected_revisions: sampleSize,
  injected_mutations: referenceItems.filter(item => item.label === "INJECTED_MUTATION").length,
  unmodified_controls: referenceItems.filter(item => item.label === "UNMODIFIED_CONTROL").length
}, null, 2) + "\n");
