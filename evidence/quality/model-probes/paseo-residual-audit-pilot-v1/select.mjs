import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultSnapshot = path.join(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json");
const seed = "paseo-residual-audit-pilot-v1|2026-08-27|task-first-v1";
const perStratum = 5;

function parseArgs(argv) {
  const args = {snapshot: defaultSnapshot, out: here};
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (!["--repo", "--snapshot", "--out"].includes(flag) || !argv[i + 1]) {
      throw new Error("usage: node select.mjs --repo /path/to/source-repo [--snapshot SNAPSHOT.json] [--out DIR]");
    }
    args[flag.slice(2)] = path.resolve(argv[++i]);
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

function stableRank(...parts) {
  return sha256Bytes(parts.join("\0"));
}

function writeJson(file, value) {
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function provenanceStratum(task) {
  const modifier = task.candidate_modifier?.family;
  const reviewers = task.contextual_reviewer_families ?? [];
  const orchestrator = task.orchestrator?.family;
  if (modifier === "GPT/Codex" && reviewers.length === 1 && reviewers[0] === "GPT/Codex") {
    return orchestrator === "GPT/Codex"
      ? "S1_GPT_MOD_GPT_REV_GPT_ORCH"
      : "S2_GPT_MOD_GPT_REV_NON_GPT_ORCH";
  }
  if (modifier === "GPT/Codex" && reviewers.length === 1 && !["GPT/Codex", "Unknown"].includes(reviewers[0])) {
    return "S3_GPT_MOD_NON_GPT_REV";
  }
  if (!["GPT/Codex", "Mixed", "Unknown"].includes(modifier) && reviewers.length === 1 && reviewers[0] === "GPT/Codex") {
    return "S4_NON_GPT_MOD_GPT_REV";
  }
  return null;
}

function selectTerminalInputs(task, sourceRepo) {
  let dispatches = task.dispatches.filter(dispatch =>
    dispatch.role === "REVIEWER" &&
    dispatch.purpose === "translation_contextual_v1" &&
    dispatch.input_path
  );
  let resolutionBasis = "terminal_reviewer_dispatch";
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
        dispatches = [{
          dispatch_id: "STATE.contextual_input_path",
          cycle: state.cycle ?? null,
          candidate_identity: state.candidate_identity ?? null,
          input_path: state.contextual_input_path
        }];
        resolutionBasis = "state_contextual_input_path_fallback";
      }
    }
    if (dispatches.length === 0) {
      const envelopes = fs.readdirSync(taskDir)
        .filter(name => /^CONTEXTUAL-ENVELOPE.*\.json$/.test(name));
      if (envelopes.length === 1) {
        dispatches = [{
          dispatch_id: "unique-envelope-fallback",
          cycle: null,
          candidate_identity: null,
          input_path: path.posix.join(".ai/task", task.task_id, envelopes[0])
        }];
        resolutionBasis = "unique_contextual_envelope_fallback";
      }
    }
  }
  if (dispatches.length === 0) return null;

  const byRevision = new Map();
  const inputs = [];
  for (const dispatch of dispatches) {
    const absoluteInput = path.join(sourceRepo, dispatch.input_path);
    if (!fs.existsSync(absoluteInput)) throw new Error(`missing contextual input: ${dispatch.input_path}`);
    const envelope = JSON.parse(fs.readFileSync(absoluteInput, "utf8"));
    const payload = envelope.payload ?? envelope;
    if (!Array.isArray(payload.translation_snapshot) || !Array.isArray(payload.bounded_context)) {
      throw new Error(`invalid contextual input shape: ${dispatch.input_path}`);
    }
    const contexts = new Map(payload.bounded_context.map(entry => [entry.revision_key, entry.context]));
    for (const translation of payload.translation_snapshot) {
      if (!translation.revision_key || typeof translation.source !== "string" || typeof translation.target !== "string") {
        throw new Error(`invalid translation snapshot entry: ${dispatch.input_path}`);
      }
      if (!contexts.has(translation.revision_key)) {
        throw new Error(`missing bounded context for ${translation.revision_key}: ${dispatch.input_path}`);
      }
      const item = {
        original_revision_key: translation.revision_key,
        source: translation.source,
        target: translation.target,
        fixed_context: contexts.get(translation.revision_key)
      };
      const existing = byRevision.get(item.original_revision_key);
      if (existing && JSON.stringify(existing) !== JSON.stringify(item)) {
        throw new Error(`conflicting terminal snapshots for ${task.task_id}/${item.original_revision_key}`);
      }
      byRevision.set(item.original_revision_key, item);
    }
    inputs.push({
      dispatch_id: dispatch.dispatch_id,
      cycle: dispatch.cycle ?? null,
      logical_path: dispatch.input_path,
      sha256: sha256File(absoluteInput),
      candidate_identity: dispatch.candidate_identity ?? envelope.candidate_identity ?? null,
      wrapper: envelope.payload ? "outer_envelope" : "bare_payload"
    });
  }
  return {resolution_basis: resolutionBasis, inputs, items: [...byRevision.values()]};
}

const args = parseArgs(process.argv.slice(2));
const snapshot = JSON.parse(fs.readFileSync(args.snapshot, "utf8"));
const sourceHead = execFileSync("git", ["rev-parse", "HEAD"], {cwd: args.repo, encoding: "utf8"}).trim();
if (sourceHead !== snapshot.source_repo_head) {
  throw new Error(`source HEAD mismatch: snapshot=${snapshot.source_repo_head}, repo=${sourceHead}`);
}

const strata = [
  "S1_GPT_MOD_GPT_REV_GPT_ORCH",
  "S2_GPT_MOD_GPT_REV_NON_GPT_ORCH",
  "S3_GPT_MOD_NON_GPT_REV",
  "S4_NON_GPT_MOD_GPT_REV"
];
const pools = Object.fromEntries(strata.map(name => [name, []]));
for (const task of snapshot.tasks) {
  if (task.state !== "DONE" || !task.task_id.startsWith("p2-")) continue;
  const stratum = provenanceStratum(task);
  if (!stratum) continue;
  const terminal = selectTerminalInputs(task, args.repo);
  if (!terminal || terminal.items.length === 0) continue;
  pools[stratum].push({
    task,
    terminal,
    task_rank: stableRank(seed, "task", task.task_id)
  });
}

const selected = [];
const population = {};
for (const stratum of strata) {
  const pool = pools[stratum].sort((left, right) => left.task_rank.localeCompare(right.task_rank));
  if (pool.length < perStratum) throw new Error(`${stratum} has only ${pool.length} eligible tasks`);
  const chosenIds = new Set(pool.slice(0, perStratum).map(entry => entry.task.task_id));
  population[stratum] = pool.map((entry, index) => ({
    task_id: entry.task.task_id,
    task_rank: entry.task_rank,
    rank_within_stratum: index + 1,
    terminal_revisions: entry.terminal.items.length,
    selected: chosenIds.has(entry.task.task_id)
  }));
  for (const entry of pool.slice(0, perStratum)) {
    const item = [...entry.terminal.items].sort((left, right) =>
      stableRank(seed, "item", entry.task.task_id, left.original_revision_key)
        .localeCompare(stableRank(seed, "item", entry.task.task_id, right.original_revision_key))
    )[0];
    selected.push({stratum, ...entry, item});
  }
}

selected.sort((left, right) =>
  stableRank(seed, "order", left.task.task_id, left.item.original_revision_key)
    .localeCompare(stableRank(seed, "order", right.task.task_id, right.item.original_revision_key))
);

const holdoutItems = [];
const provenanceItems = [];
for (const [index, entry] of selected.entries()) {
  const revisionId = `H${String(index + 1).padStart(3, "0")}`;
  holdoutItems.push({
    revision_id: revisionId,
    source: entry.item.source,
    target: entry.item.target,
    fixed_context: entry.item.fixed_context
  });
  provenanceItems.push({
    revision_id: revisionId,
    stratum: entry.stratum,
    task_id: entry.task.task_id,
    original_revision_key: entry.item.original_revision_key,
    orchestrator_family: entry.task.orchestrator.family,
    candidate_modifier: entry.task.candidate_modifier,
    contextual_reviewer_families: entry.task.contextual_reviewer_families,
    candidate_reviewer_relation: entry.task.candidate_reviewer_relation,
    terminal_input_resolution: entry.terminal.resolution_basis,
    terminal_inputs: entry.terminal.inputs,
    item_sha256: sha256Bytes(JSON.stringify(entry.item))
  });
}

const holdout = {
  schema_version: "paseo-residual-audit-holdout-v1",
  instructions: "Review every item in order. Provenance and historical decisions are intentionally withheld.",
  items: holdoutItems
};
const provenance = {
  schema_version: "paseo-residual-audit-provenance-key-v1",
  visible_to_reviewers: false,
  source_repo_head: sourceHead,
  snapshot_sha256: sha256File(args.snapshot),
  items: provenanceItems
};
const sampling = {
  schema_version: "paseo-residual-audit-sampling-v1",
  seed,
  unit: "task first, then one terminal revision per selected task",
  source_repo_head: sourceHead,
  snapshot_sha256: sha256File(args.snapshot),
  selection_rules: {
    task_scope: "P2 tasks with state DONE in Paseo provenance snapshot v1",
    strata: {
      S1_GPT_MOD_GPT_REV_GPT_ORCH: "GPT/Codex candidate modifier, GPT/Codex-only contextual reviewer, GPT/Codex orchestrator",
      S2_GPT_MOD_GPT_REV_NON_GPT_ORCH: "GPT/Codex candidate modifier, GPT/Codex-only contextual reviewer, non-GPT orchestrator",
      S3_GPT_MOD_NON_GPT_REV: "GPT/Codex candidate modifier, one known non-GPT contextual reviewer family",
      S4_NON_GPT_MOD_GPT_REV: "one known non-GPT candidate modifier family, GPT/Codex-only contextual reviewer"
    },
    exclusions: "mixed/unknown modifier or reviewer composition; non-DONE/P1 tasks; tasks without a resolvable terminal contextual input",
    task_selection: `lowest ${perStratum} SHA-256 ranks per stratum`,
    item_selection: "lowest SHA-256 rank among terminal revisions in each selected task",
    presentation_order: "SHA-256 shuffle across all selected task/revision pairs",
    reviewer_blinding: "HOLDOUT.json omits task IDs, revision keys, model families, prior findings, prior verdicts and strata"
  },
  counts: Object.fromEntries(strata.map(name => [name, {
    eligible_tasks: population[name].length,
    selected_tasks: perStratum
  }])),
  population
};

fs.mkdirSync(args.out, {recursive: true});
writeJson(path.join(args.out, "HOLDOUT.json"), holdout);
writeJson(path.join(args.out, "PROVENANCE-KEY.json"), provenance);
writeJson(path.join(args.out, "SAMPLING.json"), sampling);
process.stdout.write(JSON.stringify({
  source_repo_head: sourceHead,
  holdout_items: holdoutItems.length,
  counts: sampling.counts,
  outputs: ["HOLDOUT.json", "PROVENANCE-KEY.json", "SAMPLING.json"]
}, null, 2) + "\n");
