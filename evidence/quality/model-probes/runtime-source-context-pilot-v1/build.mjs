import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const specsPath = path.join(here, "DESIGN-SPECS.json");
const specs = JSON.parse(fs.readFileSync(specsPath, "utf8"));

function parseArgs(argv) {
  const args = {
    out: here,
    snapshot: path.resolve(here, specs.source_snapshot.path),
    verification: path.join(here, "SOURCE-VERIFICATION.json"),
    draft: false
  };
  const valueFlags = new Set(["--repo", "--dlc-root", "--engine-repo", "--out", "--snapshot", "--verification"]);
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === "--draft") {
      args.draft = true;
      continue;
    }
    if (!valueFlags.has(flag) || !argv[index + 1]) {
      throw new Error("usage: node build.mjs --repo REPO --dlc-root DLC_ROOT --engine-repo ENGINE [--verification FILE] [--out DIR] [--draft]");
    }
    const key = flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    args[key] = path.resolve(argv[++index]);
  }
  for (const key of ["repo", "dlcRoot", "engineRepo"]) if (!args[key]) throw new Error(`${key} is required`);
  return args;
}

const args = parseArgs(process.argv.slice(2));
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const sha256File = file => sha256Bytes(fs.readFileSync(file));
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const keyOf = item => `${item.task_id}\0${item.original_revision_key}`;
const rank = (...parts) => sha256Bytes([specs.seed, ...parts].join("\0"));
const controlRank = ([taskId, revisionKey]) => rank("control", taskId, revisionKey);

function replaceExactlyOnce(target, before, after, key) {
  const first = target.indexOf(before);
  if (first === -1 || target.indexOf(before, first + before.length) !== -1) {
    throw new Error(`${key}: mutation before-text must occur exactly once`);
  }
  return `${target.slice(0, first)}${after}${target.slice(first + before.length)}`;
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

function listLuaFiles(root) {
  const files = [];
  const visit = directory => {
    for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(absolute);
      else if (entry.isFile() && entry.name.endsWith(".lua")) files.push(absolute);
    }
  };
  visit(root);
  return files.sort();
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
  return {normalized: normalized.trim(), map};
}

function normalizedOccurrences(fileText, source) {
  const file = normalizeWithMap(fileText);
  const needle = normalizeWithMap(source).normalized;
  const offsets = [];
  let from = 0;
  while (true) {
    const found = file.normalized.indexOf(needle, from);
    if (found === -1) break;
    offsets.push(file.map[found]);
    from = found + Math.max(1, needle.length);
  }
  return offsets;
}

function matchingBrace(text, openIndex) {
  let depth = 0;
  let state = "code";
  let longClose = null;
  for (let index = openIndex; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];
    if (state === "single" || state === "double") {
      if (char === "\\") index += 1;
      else if ((state === "single" && char === "'") || (state === "double" && char === "\"")) state = "code";
      continue;
    }
    if (state === "line-comment") {
      if (char === "\n") state = "code";
      continue;
    }
    if (state === "long") {
      if (text.startsWith(longClose, index)) {
        index += longClose.length - 1;
        state = "code";
      }
      continue;
    }
    if (char === "-" && next === "-") {
      const long = text.slice(index + 2).match(/^\[(=*)\[/);
      if (long) {
        longClose = `]${long[1]}]`;
        index += 1 + long[0].length;
        state = "long";
      } else {
        index += 1;
        state = "line-comment";
      }
      continue;
    }
    const long = text.slice(index).match(/^\[(=*)\[/);
    if (long) {
      longClose = `]${long[1]}]`;
      index += long[0].length - 1;
      state = "long";
      continue;
    }
    if (char === "'") {
      state = "single";
      continue;
    }
    if (char === "\"") {
      state = "double";
      continue;
    }
    if (char === "{") depth += 1;
    if (char === "}") {
      depth -= 1;
      if (depth === 0) return index + 1;
      if (depth < 0) break;
    }
  }
  return null;
}

function extractBlock(fileText, sourceOffset) {
  const constructors = ["newEffect{", "newTalent{", "newChat{", "newEntity{"];
  let start = -1;
  for (const token of constructors) start = Math.max(start, fileText.lastIndexOf(token, sourceOffset));
  let raw;
  let mode;
  if (start !== -1) {
    const open = fileText.indexOf("{", start);
    const end = matchingBrace(fileText, open);
    if (end !== null && start <= sourceOffset && sourceOffset < end) {
      raw = fileText.slice(start, end);
      mode = "enclosing_constructor";
    }
  }
  if (!raw) {
    const begin = Math.max(0, sourceOffset - Math.floor(specs.context_contract.max_chars / 2));
    raw = fileText.slice(begin, begin + specs.context_contract.max_chars);
    mode = "centered_file_window";
  }
  const originalChars = raw.length;
  let truncated = false;
  if (raw.length > specs.context_contract.max_chars) {
    const omitted = raw.length - specs.context_contract.head_chars_when_truncated - specs.context_contract.tail_chars_when_truncated;
    raw = `${raw.slice(0, specs.context_contract.head_chars_when_truncated)}\n--[[ deterministic truncation: ${omitted} omitted characters ]]\n${raw.slice(-specs.context_contract.tail_chars_when_truncated)}`;
    truncated = true;
  }
  if (/\/(?:home|Users)\//.test(raw)) throw new Error("source context contains a local absolute path");
  return {raw, mode, original_chars: originalChars, truncated};
}

const snapshot = JSON.parse(fs.readFileSync(args.snapshot, "utf8"));
if (sha256File(args.snapshot) !== specs.source_snapshot.sha256) throw new Error("snapshot hash mismatch");
if (snapshot.source_repo_head !== specs.source_snapshot.source_repo_head) throw new Error("snapshot source head mismatch");

const excluded = new Set();
for (const record of specs.exclusions) {
  const absolute = path.resolve(here, record.path);
  if (sha256File(absolute) !== record.sha256) throw new Error(`${record.path} exclusion hash mismatch`);
  const value = JSON.parse(fs.readFileSync(absolute, "utf8"));
  for (const item of value.items ?? []) excluded.add(keyOf(item));
}

const roots = {
  ashes: path.join(args.dlcRoot, "ashes-urhrok", "tome-ashes-urhrok"),
  cults: path.join(args.dlcRoot, "cults", "tome-cults"),
  orcs: path.join(args.dlcRoot, "orcs", "tome-orcs"),
  engine: args.engineRepo
};
for (const [component, root] of Object.entries(roots)) if (!fs.statSync(root).isDirectory()) throw new Error(`${component} source root missing`);
const engineHead = execFileSync("git", ["rev-parse", "HEAD"], {cwd: args.engineRepo, encoding: "utf8"}).trim();
const luaFiles = Object.fromEntries(Object.entries(roots).map(([component, root]) => [component, listLuaFiles(root)]));

function readTerminal(task, dispatch) {
  const absolute = path.join(args.repo, dispatch.input_path);
  if (!fs.existsSync(absolute)) throw new Error(`${task.task_id}: terminal input missing`);
  const actualHash = sha256File(absolute);
  if (dispatch.input_fingerprint?.sha256 && dispatch.input_fingerprint.sha256 !== actualHash) {
    throw new Error(`${task.task_id}: terminal input fingerprint mismatch`);
  }
  const envelope = JSON.parse(fs.readFileSync(absolute, "utf8"));
  return {
    envelope,
    terminal_input: {
      dispatch_id: dispatch.dispatch_id ?? null,
      logical_path: dispatch.input_path,
      sha256: actualHash,
      candidate_identity: dispatch.candidate_identity ?? envelope.candidate_identity ?? null
    }
  };
}

const runtimePopulation = new Map();
for (const task of snapshot.tasks) {
  const match = task.task_id.match(/^p2-(ashes|cults|orcs)-(?:status|mechanics)/);
  if (task.state !== "DONE" || !match) continue;
  for (const dispatch of terminalDispatches(task)) {
    const {envelope, terminal_input} = readTerminal(task, dispatch);
    const payload = envelope.payload ?? envelope;
    const contexts = new Map((payload.bounded_context ?? []).map(entry => [entry.revision_key, entry.context]));
    for (const translation of payload.translation_snapshot ?? []) {
      const candidate = {
        task_id: task.task_id,
        original_revision_key: translation.revision_key,
        component: match[1],
        source: translation.source,
        clean_target: translation.target,
        bounded_context_metadata: contexts.get(translation.revision_key) ?? "",
        terminal_input
      };
      const key = keyOf(candidate);
      if (excluded.has(key)) continue;
      const existing = runtimePopulation.get(key);
      if (existing && JSON.stringify(existing) !== JSON.stringify(candidate)) throw new Error(`${key}: conflicting terminal candidate`);
      runtimePopulation.set(key, candidate);
    }
  }
}
if (runtimePopulation.size !== 26) throw new Error(`expected 26 runtime candidates after exclusions, got ${runtimePopulation.size}`);

const surfaceTask = snapshot.tasks.find(task => task.task_id === specs.surface_task && task.state === "DONE");
if (!surfaceTask) throw new Error("surface task missing from snapshot");
const surfacePopulation = new Map();
for (const dispatch of terminalDispatches(surfaceTask)) {
  const {envelope, terminal_input} = readTerminal(surfaceTask, dispatch);
  const payload = envelope.payload ?? envelope;
  const contexts = new Map((payload.bounded_context ?? []).map(entry => [entry.revision_key, entry.context]));
  for (const translation of payload.translation_snapshot ?? []) {
    const candidate = {
      task_id: surfaceTask.task_id,
      original_revision_key: translation.revision_key,
      component: "engine",
      source: translation.source,
      clean_target: translation.target,
      bounded_context_metadata: contexts.get(translation.revision_key) ?? "",
      terminal_input
    };
    const existing = surfacePopulation.get(candidate.original_revision_key);
    if (existing && JSON.stringify(existing) !== JSON.stringify(candidate)) throw new Error(`${candidate.original_revision_key}: conflicting surface candidate`);
    surfacePopulation.set(candidate.original_revision_key, candidate);
  }
}

function locateContext(item, evidenceClass) {
  let sourceFile;
  if (evidenceClass === "runtime_source_required") {
    const matches = [];
    for (const file of luaFiles[item.component]) {
      const relative = path.relative(roots[item.component], file).split(path.sep).join("/");
      if (relative.includes("/locales/") || relative.startsWith("data/locales/")) continue;
      const text = fs.readFileSync(file, "utf8");
      if (normalizedOccurrences(text, item.source).length) matches.push(file);
    }
    if (matches.length !== 1) throw new Error(`${keyOf(item)}: expected one runtime source file, got ${matches.length}`);
    sourceFile = matches[0];
  } else {
    const match = item.bounded_context_metadata.match(/fixed_source=([^;@]+)@([0-9a-f]{7,40})/);
    if (!match) throw new Error(`${keyOf(item)}: surface fixed_source metadata missing`);
    if (!engineHead.startsWith(match[2]) && !match[2].startsWith(engineHead)) throw new Error(`${keyOf(item)}: engine commit mismatch`);
    sourceFile = path.resolve(args.engineRepo, match[1]);
    if (!sourceFile.startsWith(`${path.resolve(args.engineRepo)}${path.sep}`) || !fs.existsSync(sourceFile)) throw new Error(`${keyOf(item)}: unsafe or missing engine source path`);
  }
  const fileText = fs.readFileSync(sourceFile, "utf8");
  const occurrences = normalizedOccurrences(fileText, item.source);
  if (occurrences.length === 0) throw new Error(`${keyOf(item)}: source occurrence missing`);
  const blocks = occurrences.map(offset => extractBlock(fileText, offset));
  const blockHashes = new Set(blocks.map(block => sha256Bytes(block.raw)));
  if (blockHashes.size !== 1) throw new Error(`${keyOf(item)}: source occurrences resolve to multiple blocks`);
  const block = blocks[0];
  if (!block.raw.trim()) throw new Error(`${keyOf(item)}: CONTEXT_MISSING`);
  for (const forbidden of ["mutation_id", "expected_claim", "REFERENCE.json", "INJECTED_MUTATION", "SOURCE_VERIFIED_CONTROL"]) {
    if (block.raw.includes(forbidden)) throw new Error(`${keyOf(item)}: context leaks ${forbidden}`);
  }
  return {
    visible: block.raw,
    record: {
      component: item.component,
      relative_path: path.relative(roots[item.component], sourceFile).split(path.sep).join("/"),
      source_file_sha256: sha256File(sourceFile),
      source_occurrences: occurrences.length,
      extraction_mode: block.mode,
      original_chars: block.original_chars,
      visible_chars: block.raw.length,
      truncated: block.truncated,
      visible_context_sha256: sha256Bytes(block.raw)
    }
  };
}

const mutationByKey = new Map(specs.runtime_mutations.map(mutation => [`${mutation.task_id}\0${mutation.original_revision_key}`, mutation]));
if (mutationByKey.size !== specs.counts.runtime_mutations) throw new Error("runtime mutation key count mismatch");
const selectedRuntimeControls = new Set(specs.runtime_controls.map(([task, revision]) => `${task}\0${revision}`));
const reserves = new Set(specs.runtime_reserves.map(([task, revision]) => `${task}\0${revision}`));
const baselineExclusions = new Set(specs.runtime_baseline_exclusions.map(item => `${item.task_id}\0${item.original_revision_key}`));
const expectedRuntimeKeys = new Set([...mutationByKey.keys(), ...selectedRuntimeControls, ...reserves, ...baselineExclusions]);
if (expectedRuntimeKeys.size !== runtimePopulation.size) throw new Error("runtime selected/reserve keys do not cover the 26-candidate frame");
for (const key of expectedRuntimeKeys) if (!runtimePopulation.has(key)) throw new Error(`${key}: registered runtime candidate missing`);
const nonMutationOrder = [...specs.runtime_controls, ...specs.runtime_reserves]
  .sort((left, right) => controlRank(left).localeCompare(controlRank(right)));
if (JSON.stringify(nonMutationOrder.slice(0, specs.counts.runtime_controls)) !== JSON.stringify(specs.runtime_controls)) {
  throw new Error("runtime controls do not match the frozen SHA-256 rank rule");
}
if (JSON.stringify(nonMutationOrder.slice(specs.counts.runtime_controls)) !== JSON.stringify(specs.runtime_reserves)) {
  throw new Error("runtime reserves do not match the frozen SHA-256 rank rule");
}

const selected = [];
for (const [key, mutation] of mutationByKey) {
  const item = structuredClone(runtimePopulation.get(key));
  const context = locateContext(item, "runtime_source_required");
  item.evidence_class = "runtime_source_required";
  item.assignment = "RUNTIME_MUTATION";
  item.mutation = mutation;
  item.presented_target = replaceExactlyOnce(item.clean_target, mutation.before, mutation.after, key);
  item.context = context;
  selected.push(item);
}
for (const key of selectedRuntimeControls) {
  const item = structuredClone(runtimePopulation.get(key));
  const context = locateContext(item, "runtime_source_required");
  item.evidence_class = "runtime_source_required";
  item.assignment = "RUNTIME_CONTROL";
  item.mutation = null;
  item.presented_target = item.clean_target;
  item.context = context;
  selected.push(item);
}
for (const surfaceSpec of specs.surface_items) {
  const item = structuredClone(surfacePopulation.get(surfaceSpec.original_revision_key));
  if (!item) throw new Error(`${surfaceSpec.original_revision_key}: surface item missing`);
  const context = locateContext(item, "surface_bilingual");
  item.evidence_class = "surface_bilingual";
  item.assignment = surfaceSpec.assignment;
  item.mutation = surfaceSpec.assignment === "SURFACE_MUTATION" ? surfaceSpec : null;
  item.presented_target = item.mutation
    ? replaceExactlyOnce(item.clean_target, item.mutation.before, item.mutation.after, keyOf(item))
    : item.clean_target;
  item.context = context;
  selected.push(item);
}
if (selected.length !== specs.counts.items) throw new Error(`selected item count mismatch: ${selected.length}`);
if (new Set(selected.map(keyOf)).size !== selected.length) throw new Error("selected source item duplication");

const verification = fs.existsSync(args.verification) ? JSON.parse(fs.readFileSync(args.verification, "utf8")) : null;
if (!verification && !args.draft) throw new Error("SOURCE-VERIFICATION.json is required outside --draft mode");
const verificationByKey = new Map((verification?.items ?? []).map(item => [keyOf(item), item]));
if (verification && verificationByKey.size !== selected.length) throw new Error("source verification count mismatch");
for (const item of selected) {
  const checked = verificationByKey.get(keyOf(item));
  if (!checked) {
    if (!args.draft) throw new Error(`${keyOf(item)}: source verification missing`);
    continue;
  }
  if (checked.status !== "CLEAN") throw new Error(`${keyOf(item)}: baseline is not CLEAN`);
  if (!Array.isArray(checked.evidence) || checked.evidence.length === 0) throw new Error(`${keyOf(item)}: source verification evidence missing`);
  if (checked.clean_target_sha256 !== sha256Bytes(item.clean_target)) throw new Error(`${keyOf(item)}: clean target verification hash mismatch`);
  if (checked.visible_context_sha256 !== item.context.record.visible_context_sha256) throw new Error(`${keyOf(item)}: context verification hash mismatch`);
  if (checked.source_file_sha256 !== item.context.record.source_file_sha256) throw new Error(`${keyOf(item)}: source file verification hash mismatch`);
}

for (const item of selected) item.presentation_rank = rank("present", item.task_id, item.original_revision_key);
selected.sort((left, right) => left.presentation_rank.localeCompare(right.presentation_rank));

const armA = [];
const armB = [];
const referenceItems = [];
const sourceControls = [];
const contexts = [];
const verificationTemplate = [];
for (const [index, item] of selected.entries()) {
  const revisionId = `P${String(index + 1).padStart(3, "0")}`;
  const visible = {revision_id: revisionId, source: item.source, target: item.presented_target};
  armA.push(visible);
  armB.push({...visible, source_context: item.context.visible});
  referenceItems.push({
    revision_id: revisionId,
    evidence_class: item.evidence_class,
    label: item.assignment,
    mutation_id: item.mutation?.mutation_id ?? null,
    claim_type: item.mutation?.claim_type ?? null,
    atom_target_span: item.mutation?.after ?? null,
    clean_replacement_span: item.mutation?.before ?? null,
    expected_claim: item.mutation?.expected_claim ?? null
  });
  sourceControls.push({
    revision_id: revisionId,
    task_id: item.task_id,
    original_revision_key: item.original_revision_key,
    evidence_class: item.evidence_class,
    assignment: item.assignment,
    source: item.source,
    clean_target: item.clean_target,
    presented_target: item.presented_target,
    presentation_rank: item.presentation_rank,
    terminal_input: item.terminal_input,
    context: item.context.record,
    clean_item_sha256: sha256Bytes(JSON.stringify({source: item.source, target: item.clean_target, context: item.context.visible}))
  });
  contexts.push({revision_id: revisionId, task_id: item.task_id, original_revision_key: item.original_revision_key, ...item.context.record});
  verificationTemplate.push({
    task_id: item.task_id,
    original_revision_key: item.original_revision_key,
    status: "PENDING_REPLACE_WITH_CLEAN",
    clean_target_sha256: sha256Bytes(item.clean_target),
    visible_context_sha256: item.context.record.visible_context_sha256,
    source_file_sha256: item.context.record.source_file_sha256,
    evidence: []
  });
}

const holdoutBase = {
  schema_version: "runtime-source-context-holdout-v1",
  instructions: "Review every item independently in the given order. Historical provenance, evidence class, source-verification and mutation records are withheld."
};
const holdoutA = {...holdoutBase, items: armA};
const holdoutB = {...holdoutBase, items: armB};
const reference = {
  schema_version: "runtime-source-context-reference-v1",
  visible_to_reviewers: false,
  atom_match_contract: "non-OK verdict, exact target_span overlapping atom_target_span, and exact claim_type equality",
  items: referenceItems
};
const controls = {
  schema_version: "runtime-source-context-source-controls-v1",
  visible_to_reviewers: false,
  source_repo_head: snapshot.source_repo_head,
  engine_repo_head: engineHead,
  items: sourceControls
};
const contextRecords = {
  schema_version: "runtime-source-context-records-v1",
  extractor_contract: specs.context_contract,
  missing_count: contexts.filter(item => !item.visible_context_sha256).length,
  items: contexts
};
const sampling = {
  schema_version: "runtime-source-context-sampling-v1",
  seed: specs.seed,
  finite_benchmark_only: true,
  population_extrapolation_allowed: false,
  runtime_candidate_frame: {
    rule: "DONE P2 ashes/cults/orcs status or mechanics terminal contextual revisions, excluding all prior pilot, controlled-mutation-v1 and UI/log replication items",
    eligible: runtimePopulation.size,
    mutations: specs.runtime_mutations.map(item => [item.task_id, item.original_revision_key]),
    controls: specs.runtime_controls,
    ordered_reserves_not_used: specs.runtime_reserves,
    baseline_exclusions: specs.runtime_baseline_exclusions,
    mutation_screen: specs.runtime_selection_notes.mutation_screen,
    pre_inference_mutation_replacements: specs.runtime_selection_notes.replacements,
    control_selection: specs.runtime_selection_notes.control_rank,
    control_ranks: [...specs.runtime_controls, ...specs.runtime_reserves].map(([taskId, revisionKey]) => ({
      task_id: taskId,
      original_revision_key: revisionKey,
      sha256_rank: controlRank([taskId, revisionKey]),
      disposition: selectedRuntimeControls.has(`${taskId}\0${revisionKey}`) ? "CONTROL" : "ORDERED_RESERVE"
    }))
  },
  surface_candidate_frame: {
    rule: "first twelve frozen terminal revisions of p2-tome-texts-b10-001",
    selected: specs.surface_items.map(item => [specs.surface_task, item.original_revision_key, item.assignment])
  },
  presentation: "independent SHA-256 order over all 36 selected source items",
  exclusions: specs.exclusions
};
const manifest = {
  schema_version: "runtime-source-context-manifest-v1",
  status: verification ? "PREFLIGHT_READY" : "DRAFT",
  finite_population: {unit: "source_item", runtime_mutants: 12, runtime_controls: 12, surface_mutants: 6, surface_controls: 6, total: 36},
  arms: {
    A: {fields: ["revision_id", "source", "target"]},
    B: {fields: ["revision_id", "source", "target", "source_context"], unique_difference: "source_context"}
  },
  routes: ["codex-gpt-5.6-sol-high", "claude-opus-5-medium-no-advisor", "pi-zai-cn-glm-5.3-flash-high", "agy-gemini-3.7-flash-high"],
  runs: {per_arm: 2, request_identity: "payload, item order, prompt, model parameters and schema are identical within each arm"},
  missingness: {CONTEXT_MISSING_allowed: false, action: "no-go before inference; preserve failed version"},
  scoring: {
    unit: "item",
    detection: "non-OK, exact target_span overlap with sealed atom_target_span, exact claim_type",
    finding_only: "same atom match with FINDING",
    control_candidate: "any schema-valid non-OK item claim on a frozen clean control",
    extra_claims: "do not cancel a correct detection; report separately"
  },
  gates: {
    runtime_recall: {denominator_per_run: 48, pass_net_gain_minimum: 10, displayed_materiality_threshold: 0.20},
    route_direction: {routes_positive_minimum: 3, route_delta_strictly_positive: true},
    runtime_control_candidate_delta: {denominator_per_run: 48, pass_net_gain_maximum: 2, displayed_guardrail: 0.05},
    per_route_new_control_candidates: {maximum: 1},
    control_contamination: {maximum: 0, consequence: "no adopt-B inference for this version"},
    run_policy: "both runs must independently pass every gate; no pooling and no third run"
  },
  frozen_artifacts_required: ["EXPERIMENT.json", "ROUTE-PREFLIGHT.json", "HOLDOUT-A.json", "HOLDOUT-B.json", "REFERENCE.json", "SOURCE-CONTROLS.json", "SOURCE-VERIFICATION.json", "CONTEXTS.json", "SAMPLING.json", "PROMPT.md", "REVIEWER-SCHEMA.json", "MANIFEST-SCHEMA.json", "ADJUDICATION-SCHEMA.json", "PREFLIGHT-FIXTURES.json", "SCORER-FIXTURES.json", "build.mjs", "preflight.mjs", "freeze.mjs", "score.mjs", "run.mjs"]
};

fs.mkdirSync(args.out, {recursive: true});
writeJson(path.join(args.out, "HOLDOUT-A.json"), holdoutA);
writeJson(path.join(args.out, "HOLDOUT-B.json"), holdoutB);
writeJson(path.join(args.out, "REFERENCE.json"), reference);
writeJson(path.join(args.out, "SOURCE-CONTROLS.json"), controls);
writeJson(path.join(args.out, "CONTEXTS.json"), contextRecords);
writeJson(path.join(args.out, "SAMPLING.json"), sampling);
writeJson(path.join(args.out, "MANIFEST.json"), manifest);
if (args.draft && !verification) writeJson(path.join(args.out, "DRAFT-SOURCE-VERIFICATION.json"), {schema_version: "runtime-source-context-verification-v1", status: "DRAFT", items: verificationTemplate});

process.stdout.write(`${JSON.stringify({
  mode: args.draft ? "draft" : "final",
  runtime_candidate_frame: runtimePopulation.size,
  selected_items: selected.length,
  runtime_mutations: referenceItems.filter(item => item.label === "RUNTIME_MUTATION").length,
  runtime_controls: referenceItems.filter(item => item.label === "RUNTIME_CONTROL").length,
  surface_mutations: referenceItems.filter(item => item.label === "SURFACE_MUTATION").length,
  surface_controls: referenceItems.filter(item => item.label === "SURFACE_CONTROL").length,
  context_missing: contextRecords.missing_count,
  context_truncated: contexts.filter(item => item.truncated).length
}, null, 2)}\n`);
