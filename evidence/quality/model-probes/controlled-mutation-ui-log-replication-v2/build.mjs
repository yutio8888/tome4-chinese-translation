import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const seed = "controlled-mutation-ui-log-replication-v2|2026-08-27";
const expectedSourceHead = "1666481409f4c0d63d66e84659f6b6145d8d25d0";
const selectedKeys = [
  "p2-cults-ui-logs-b2-001\0cults-ui-logs-b2-001",
  "p2-orcs-ui-logs-b1-001\0orcs-ui-logs-b1-info",
  "p2-ashes-ui-logs-b1-001\0ashes-ui-logs-b1-001",
  "p2-cults-ui-logs-b1-001\0cults-ui-logs-b1-001",
  "p2-orcs-ui-logs-b3-001\0orcs-ui-logs-b3-001",
  "p2-orcs-ui-logs-b2-001\0orcs-ui-logs-b2-001",
  "p2-cults-ui-logs-b3-001\0cults-ui-logs-b3-001",
  "p2-ashes-ui-logs-b2-001\0ashes-ui-logs-b2-001"
];
const excludedNearDuplicate = "p2-orcs-ui-logs-b1-001\0orcs-ui-logs-b1-log";
const mutationSpecs = {
  "p2-cults-ui-logs-b2-001\0cults-ui-logs-b2-001": {
    mutation_id: "RM01_SPEED_TO_DAMAGE",
    category: "effect_identity",
    before: "守护者的移动速度增加了",
    after: "守护者的伤害增加了",
    expected_claim: "The event increases the guardian's movement speed, not its damage."
  },
  "p2-ashes-ui-logs-b1-001\0ashes-ui-logs-b1-001": {
    mutation_id: "RM02_SENSE_FOUR_TO_THREE",
    category: "duration",
    before: "在 4 回合内觉察到",
    after: "在 3 回合内觉察到",
    expected_claim: "The runtime applies EFF_SENSE for 4 turns, not the stale English 3 turns."
  },
  "p2-orcs-ui-logs-b3-001\0orcs-ui-logs-b3-001": {
    mutation_id: "RM03_COMPANION_COMBAT_CONDITION_REMOVED",
    category: "condition_subject",
    before: "并且你和机械蜘蛛都必须处于非战斗状态",
    after: "并且你必须处于非战斗状态",
    expected_claim: "Both the player and the mecharachnid must be out of combat; the mutation drops the companion condition."
  },
  "p2-cults-ui-logs-b3-001\0cults-ui-logs-b3-001": {
    mutation_id: "RM04_MUTATED_HAND_TO_EMPTY_OFFHAND",
    category: "prerequisite_identity",
    before: "异变之手",
    after: "空闲的副手",
    expected_claim: "This log requires Mutated Hand; an empty offhand is a separate prerequisite and message."
  }
};

function parseArgs(argv) {
  const args = {
    snapshot: path.join(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json"),
    priorPilot: path.join(here, "../paseo-residual-audit-pilot-v1/PROVENANCE-KEY.json"),
    priorV1: path.join(here, "../controlled-mutation-reviewer-v1/SOURCE-CONTROLS.json"),
    verification: path.join(here, "SOURCE-VERIFICATION.json"),
    out: here
  };
  const allowed = new Set(["--repo", "--dlc-root", "--engine-repo", "--snapshot", "--prior-pilot", "--prior-v1", "--verification", "--out"]);
  for (let index = 0; index < argv.length; index += 1) {
    if (!allowed.has(argv[index]) || !argv[index + 1]) throw new Error("usage: node build.mjs --repo REPO --dlc-root DLC_ROOT --engine-repo ENGINE [--out DIR]");
    const key = argv[index].slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    args[key] = path.resolve(argv[++index]);
  }
  for (const key of ["repo", "dlcRoot", "engineRepo"]) if (!args[key]) throw new Error(`--${key.replace(/[A-Z]/g, c => `-${c.toLowerCase()}`)} is required`);
  return args;
}
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const rank = (...parts) => sha256Bytes([seed, ...parts].join("\0"));
function replaceExactlyOnce(target, before, after, key) {
  const first = target.indexOf(before);
  if (first === -1 || target.indexOf(before, first + before.length) !== -1) throw new Error(`${key}: mutation text must occur exactly once`);
  return `${target.slice(0, first)}${after}${target.slice(first + before.length)}`;
}
function sanitizeContext(context) {
  let value = context;
  for (const prefix of [
    "/home/yun/projects/tome4-dlcs/ashes-urhrok/",
    "/home/yun/projects/tome4-dlcs/cults/",
    "/home/yun/projects/tome4-dlcs/orcs/",
    "/home/yun/projects/t-engine4/"
  ]) value = value.replaceAll(prefix, "");
  if (/\/(?:home|Users)\//.test(value)) throw new Error("unhandled local absolute path in fixed context");
  return value;
}
function terminalDispatches(task) {
  let dispatches = task.dispatches.filter(dispatch => dispatch.role === "REVIEWER" && dispatch.purpose === "translation_contextual_v1" && dispatch.input_path);
  const withCycle = dispatches.filter(dispatch => Number.isFinite(dispatch.cycle));
  if (withCycle.length) {
    const terminalCycle = Math.max(...withCycle.map(dispatch => dispatch.cycle));
    dispatches = withCycle.filter(dispatch => dispatch.cycle === terminalCycle);
  } else if (dispatches.length) dispatches = [dispatches.at(-1)];
  return dispatches;
}

const args = parseArgs(process.argv.slice(2));
const sourceHead = execFileSync("git", ["rev-parse", "HEAD"], {cwd: args.repo, encoding: "utf8"}).trim();
if (sourceHead !== expectedSourceHead) throw new Error(`source HEAD mismatch: ${sourceHead}`);
const snapshot = JSON.parse(fs.readFileSync(args.snapshot, "utf8"));
if (snapshot.source_repo_head !== sourceHead) throw new Error("snapshot/source HEAD mismatch");
const priorPilot = JSON.parse(fs.readFileSync(args.priorPilot, "utf8"));
const priorV1 = JSON.parse(fs.readFileSync(args.priorV1, "utf8"));
const excluded = new Set([...priorPilot.items, ...priorV1.items].map(item => `${item.task_id}\0${item.original_revision_key}`));
const verification = JSON.parse(fs.readFileSync(args.verification, "utf8"));
const verificationByKey = new Map(verification.items.map(item => [`${item.task_id}\0${item.original_revision_key}`, item]));
if (verificationByKey.size !== selectedKeys.length) throw new Error("source verification item count mismatch");
const roots = {
  ashes: path.join(args.dlcRoot, "ashes-urhrok"),
  cults: path.join(args.dlcRoot, "cults"),
  orcs: path.join(args.dlcRoot, "orcs"),
  engine: args.engineRepo
};
for (const item of verification.items) {
  for (const source of item.sources) {
    const actual = sha256File(path.join(roots[source.repo], source.path));
    if (actual !== source.sha256) throw new Error(`${source.repo}/${source.path} hash mismatch`);
  }
}

const population = new Map();
for (const task of snapshot.tasks) {
  if (task.state !== "DONE" || !/^p2-(?:ashes|cults|orcs)-(?:ui|ui-logs)/.test(task.task_id)) continue;
  for (const dispatch of terminalDispatches(task)) {
    const inputPath = path.join(args.repo, dispatch.input_path);
    const envelope = JSON.parse(fs.readFileSync(inputPath, "utf8"));
    const payload = envelope.payload ?? envelope;
    const contexts = new Map(payload.bounded_context.map(entry => [entry.revision_key, entry.context]));
    for (const translation of payload.translation_snapshot) {
      const key = `${task.task_id}\0${translation.revision_key}`;
      if (excluded.has(key)) continue;
      const candidate = {
        task_id: task.task_id,
        original_revision_key: translation.revision_key,
        source: translation.source,
        historical_target: translation.target,
        fixed_context: sanitizeContext(contexts.get(translation.revision_key)),
        terminal_input: {
          dispatch_id: dispatch.dispatch_id ?? null,
          logical_path: dispatch.input_path,
          sha256: sha256File(inputPath),
          candidate_identity: dispatch.candidate_identity ?? envelope.candidate_identity ?? null
        },
        census_rank: rank("census", task.task_id, translation.revision_key)
      };
      const existing = population.get(key);
      if (existing && JSON.stringify(existing) !== JSON.stringify(candidate)) throw new Error(`conflicting terminal item ${key}`);
      population.set(key, candidate);
    }
  }
}
if (population.size !== 9) throw new Error(`expected 9 eligible UI/log revisions, got ${population.size}`);
if (!population.has(excludedNearDuplicate)) throw new Error("near-duplicate census item missing");
for (const key of population.keys()) if (!selectedKeys.includes(key) && key !== excludedNearDuplicate) throw new Error(`unregistered census exclusion: ${key}`);

const selected = selectedKeys.map(key => {
  const item = structuredClone(population.get(key));
  if (!item) throw new Error(`selected item missing: ${key}`);
  const checked = verificationByKey.get(key);
  if (sha256Bytes(item.historical_target) !== checked.historical_target_sha256) throw new Error(`${key}: historical target hash mismatch`);
  let verifiedTarget = item.historical_target;
  if (checked.baseline_adjustment) {
    if (verifiedTarget !== checked.baseline_adjustment.from) throw new Error(`${key}: baseline adjustment input mismatch`);
    verifiedTarget = checked.baseline_adjustment.to;
  }
  if (sha256Bytes(verifiedTarget) !== checked.verified_target_sha256) throw new Error(`${key}: verified target hash mismatch`);
  const mutation = mutationSpecs[key] ?? null;
  item.verified_target = verifiedTarget;
  item.label = mutation ? "INJECTED_MUTATION" : "SOURCE_VERIFIED_CONTROL";
  item.mutation = mutation;
  item.presented_target = mutation ? replaceExactlyOnce(verifiedTarget, mutation.before, mutation.after, key) : verifiedTarget;
  item.presentation_rank = rank("present", item.task_id, item.original_revision_key);
  return item;
}).sort((left, right) => left.presentation_rank.localeCompare(right.presentation_rank));
if (selected.filter(item => item.mutation).length !== 4) throw new Error("mutation count mismatch");

const holdoutItems = [];
const referenceItems = [];
const sourceControls = [];
for (const [index, item] of selected.entries()) {
  const revisionId = `R${String(index + 1).padStart(3, "0")}`;
  holdoutItems.push({revision_id: revisionId, source: item.source, target: item.presented_target, fixed_context: item.fixed_context});
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
    label: item.label,
    source: item.source,
    historical_target: item.historical_target,
    verified_target: item.verified_target,
    presented_target: item.presented_target,
    fixed_context: item.fixed_context,
    terminal_input: item.terminal_input,
    source_verification: verificationByKey.get(`${item.task_id}\0${item.original_revision_key}`),
    verified_item_sha256: sha256Bytes(JSON.stringify({source: item.source, target: item.verified_target, fixed_context: item.fixed_context}))
  });
}
const holdout = {
  schema_version: "controlled-mutation-ui-log-replication-holdout-v2",
  instructions: "Review every item independently in the given order. Historical provenance, source-verification records and mutation records are withheld.",
  items: holdoutItems
};
const reference = {schema_version: "controlled-mutation-ui-log-replication-reference-v2", visible_to_reviewers: false, items: referenceItems};
const controls = {schema_version: "controlled-mutation-ui-log-replication-controls-v2", visible_to_reviewers: false, source_repo_head: sourceHead, items: sourceControls};
const sampling = {
  schema_version: "controlled-mutation-ui-log-replication-sampling-v2",
  seed,
  source_repo_head: sourceHead,
  snapshot_sha256: sha256File(args.snapshot),
  prior_pilot_exclusion_sha256: sha256File(args.priorPilot),
  prior_v1_exclusion_sha256: sha256File(args.priorV1),
  source_verification_sha256: sha256File(args.verification),
  population_rules: "DONE P2 ashes/cults/orcs UI or UI-log terminal contextual revisions, excluding all prior pilot/v1 task-revision pairs",
  eligible_revisions: population.size,
  selected_revisions: selected.length,
  injected_mutations: 4,
  source_verified_controls: 4,
  exclusion_after_census: {
    task_id: excludedNearDuplicate.split("\0")[0],
    original_revision_key: excludedNearDuplicate.split("\0")[1],
    reason: "near-duplicate of the selected Instant Channeling info item; excluded before inference to avoid correlated duplicate evidence"
  },
  baseline_policy: "Every selected target is bound to complete fixed-source verification. One known malformed historical placeholder composition is corrected only in the experiment fixture before assignment.",
  assignment: "Four preregistered reversible objective mutations; the other four items remain source-verified controls.",
  presentation: "independent SHA-256 shuffle; task IDs, original revision keys, clean targets, labels and verification records hidden"
};
fs.mkdirSync(args.out, {recursive: true});
writeJson(path.join(args.out, "HOLDOUT.json"), holdout);
writeJson(path.join(args.out, "REFERENCE.json"), reference);
writeJson(path.join(args.out, "SOURCE-CONTROLS.json"), controls);
writeJson(path.join(args.out, "SAMPLING.json"), sampling);
process.stdout.write(`${JSON.stringify({eligible_revisions: population.size, selected_revisions: selected.length, injected_mutations: 4, source_verified_controls: 4}, null, 2)}\n`);
