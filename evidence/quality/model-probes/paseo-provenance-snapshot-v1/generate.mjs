#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCHEMA_VERSION = "paseo-provenance-snapshot-v1";
const CORPUS_PATTERN = /^(?:p1-b\d|p2-(?:ashes|cults|orcs)-|p2-tome-texts-b\d)/;

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i];
    const value = argv[i + 1];
    if (!key?.startsWith("--") || value === undefined) {
      throw new Error(`invalid argument sequence near ${key ?? "<end>"}`);
    }
    args[key.slice(2)] = value;
  }
  if (!args.repo || !args.agents || !args.out) {
    throw new Error("usage: node generate.mjs --repo <translation-repo> --agents <paseo-agent-dir> --out <output-dir>");
  }
  return {
    repo: path.resolve(args.repo),
    agents: path.resolve(args.agents),
    out: path.resolve(args.out),
  };
}

function sha256Buffer(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

function sha256File(file) {
  return sha256Buffer(fs.readFileSync(file));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function sortedDirEntries(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
}

function walkFiles(dir) {
  const files = [];
  for (const entry of sortedDirEntries(dir)) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walkFiles(file));
    else if (entry.isFile()) files.push(file);
  }
  return files;
}

function safeString(value) {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function safeBoolean(value) {
  return typeof value === "boolean" ? value : null;
}

function safeInteger(value) {
  return Number.isInteger(value) ? value : null;
}

function normalizedEnum(value) {
  if (typeof value !== "string" || value.length === 0) return null;
  if (value.length > 80 || /[\r\n]/.test(value)) return "OTHER_STRING";
  return value;
}

function familyFor(provider, model) {
  const haystack = `${provider ?? ""} ${model ?? ""}`.toLowerCase();
  if (/openai|codex|gpt-/.test(haystack)) return "GPT/Codex";
  if (/anthropic|claude|opus|sonnet|fable/.test(haystack)) return "Claude";
  if (/google|gemini/.test(haystack)) return "Gemini";
  if (/xai|grok/.test(haystack)) return "Grok";
  if (/z\.ai|zai|glm/.test(haystack)) return "GLM";
  if (/muse/.test(haystack)) return "Muse";
  return "Unknown";
}

function safeAgentRecord(record) {
  const provider = safeString(record?.provider);
  const model = safeString(record?.config?.model);
  const thinking = safeString(record?.config?.thinkingOptionId);
  const mode = safeString(record?.config?.modeId);
  return {
    agent_id: safeString(record?.id),
    provider,
    model,
    thinking,
    mode,
    created_at: safeString(record?.createdAt),
    family: familyFor(provider, model),
  };
}

function buildAgentIndex(agentRoot, repo) {
  const byId = new Map();
  const duplicates = [];
  for (const file of walkFiles(agentRoot).filter((item) => item.endsWith(".json"))) {
    let raw;
    try {
      raw = readJson(file);
    } catch {
      continue;
    }
    const id = safeString(raw?.id);
    if (!id) continue;
    const candidate = {
      safe: safeAgentRecord(raw),
      source_file: file,
      repo_match: path.resolve(raw?.cwd ?? "/") === repo,
    };
    const prior = byId.get(id);
    if (!prior || (!prior.repo_match && candidate.repo_match)) {
      if (prior) duplicates.push(id);
      byId.set(id, candidate);
    } else {
      duplicates.push(id);
    }
  }
  return { byId, duplicates: [...new Set(duplicates)].sort() };
}

function isContextualTask(state) {
  const contracts = Array.isArray(state.review_contracts) ? state.review_contracts : [];
  if (contracts.includes("translation_contextual_v1")) return true;
  if (state.contextual_reviewer?.purpose === "translation_contextual_v1") return true;
  return (state.child_dispatches ?? []).some(
    (dispatch) => String(dispatch.role ?? "").toLowerCase() === "reviewer"
      && dispatch.purpose === "translation_contextual_v1",
  );
}

function manifestRecord(file, logicalPath, kind) {
  const stat = fs.statSync(file);
  return {
    kind,
    logical_path: logicalPath,
    size_bytes: stat.size,
    sha256: sha256File(file),
  };
}

function fileFingerprint(file) {
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) return null;
  return { size_bytes: fs.statSync(file).size, sha256: sha256File(file) };
}

function logicalRepoPath(repo, value) {
  if (typeof value !== "string" || value.length === 0) return null;
  const absolute = path.isAbsolute(value) ? path.resolve(value) : path.resolve(repo, value);
  const relative = path.relative(repo, absolute);
  if (relative.startsWith("..") || path.isAbsolute(relative)) return null;
  return relative.split(path.sep).join("/");
}

function git(repo, args) {
  return execFileSync("git", ["-C", repo, ...args], { encoding: "utf8" }).trim();
}

function commitExists(repo, commit) {
  if (!commit) return false;
  try {
    execFileSync("git", ["-C", repo, "cat-file", "-e", `${commit}^{commit}`], { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function countMap(values) {
  return Object.fromEntries(
    [...values.reduce((map, value) => map.set(value, (map.get(value) ?? 0) + 1), new Map()).entries()]
      .sort(([a], [b]) => a.localeCompare(b)),
  );
}

function modelKey(agent) {
  if (!agent || agent.family === "Unknown") return "Unknown";
  return `${agent.family} :: ${agent.provider ?? "?"} :: ${agent.model ?? "?"}`;
}

function safeDispatch(dispatch, agentIndex, repo) {
  const agentId = safeString(dispatch?.agent_id);
  const agent = agentId && agentIndex.has(agentId)
    ? agentIndex.get(agentId).safe
    : { agent_id: agentId, provider: null, model: null, thinking: null, mode: null, created_at: null, family: "Unknown" };
  const inputPath = logicalRepoPath(repo, dispatch?.input_path);
  return {
    dispatch_id: safeString(dispatch?.dispatch_id),
    role: normalizedEnum(dispatch?.role),
    purpose: normalizedEnum(dispatch?.purpose),
    cycle: safeInteger(dispatch?.cycle),
    agent,
    lifecycle: normalizedEnum(dispatch?.lifecycle),
    archive_confirmed: safeBoolean(dispatch?.archive_confirmed),
    output_valid: safeBoolean(dispatch?.output_valid),
    lineage_verified: safeBoolean(dispatch?.lineage_verified),
    candidate_identity: safeString(dispatch?.candidate_identity),
    candidate_author_agent_id: safeString(dispatch?.candidate_author_agent_id),
    input_path: inputPath,
    input_fingerprint: inputPath ? fileFingerprint(path.join(repo, inputPath)) : null,
  };
}

function roleClass(dispatch) {
  const role = String(dispatch.role ?? "").toLowerCase();
  const purpose = String(dispatch.purpose ?? "").toLowerCase();
  if (role === "executor") return "executor";
  if (role === "scout") return "scout";
  if (role === "senior" || role === "senior_reviewer" || role === "senior-reviewer" || purpose.includes("senior")) {
    return "senior_reviewer";
  }
  if (role === "reviewer" && purpose === "translation_contextual_v1") return "contextual_reviewer";
  return "other";
}

function candidateAttribution(state, dispatches, orchestrator) {
  const explicitId = safeString(state.candidate_author_agent_id);
  if (explicitId) {
    const explicit = dispatches.find((item) => item.agent.agent_id === explicitId)?.agent;
    return {
      family: explicit?.family ?? "Unknown",
      basis: "explicit_candidate_author_agent_id",
      confidence: explicit ? "explicit" : "unresolved",
      agent_ids: [explicitId],
    };
  }

  const executors = dispatches.filter((item) => roleClass(item) === "executor");
  const executorFamilies = [...new Set(executors.map((item) => item.agent.family))].sort();
  if (executors.length > 0 && executorFamilies.length === 1) {
    return {
      family: executorFamilies[0],
      basis: "all_executor_dispatches_same_family",
      confidence: "family_inferred",
      agent_ids: [...new Set(executors.map((item) => item.agent.agent_id).filter(Boolean))].sort(),
    };
  }
  if (String(state.task_id ?? "").startsWith("p1-") && state.state === "DONE" && executors.length === 0) {
    return {
      family: orchestrator.family,
      basis: "p1_done_without_executor_direct_orchestrator_fix",
      confidence: orchestrator.family === "Unknown" ? "unresolved" : "role_direct",
      agent_ids: orchestrator.agent_id ? [orchestrator.agent_id] : [],
    };
  }
  return {
    family: executorFamilies.length > 1 ? "Mixed" : "Unknown",
    basis: executors.length > 0 ? "mixed_executor_families" : "no_executor_attribution",
    confidence: "unresolved",
    agent_ids: [...new Set(executors.map((item) => item.agent.agent_id).filter(Boolean))].sort(),
  };
}

function reviewRelation(candidate, reviewerFamilies) {
  if (candidate.confidence === "unresolved" || candidate.family === "Unknown" || candidate.family === "Mixed") {
    return "unresolved";
  }
  const hasUnknown = reviewerFamilies.includes("Unknown");
  const known = reviewerFamilies.filter((family) => family !== "Unknown");
  if (known.length === 0) return "unresolved";
  const same = known.includes(candidate.family);
  if (hasUnknown && same && known.some((family) => family !== candidate.family)) {
    return "mixed_same_cross_and_unknown_family";
  }
  if (hasUnknown && same) return "mixed_same_and_unknown_family";
  if (hasUnknown) return "cross_and_unknown_family";
  if (same && known.some((family) => family !== candidate.family)) return "mixed_same_and_cross_family";
  return same ? "same_family_only" : "cross_family_only";
}

function safeReviewArtifact(file, repo, taskId) {
  const logicalPath = path.relative(repo, file).split(path.sep).join("/");
  const fingerprint = fileFingerprint(file);
  let record;
  try {
    record = readJson(file);
  } catch {
    return { logical_path: logicalPath, ...fingerprint, json_valid: false, parse_error_code: "INVALID_JSON" };
  }
  const result = record?.result;
  return {
    logical_path: logicalPath,
    ...fingerprint,
    json_valid: true,
    task_id_matches_directory: record?.task_id === taskId,
    dispatch_id: safeString(record?.dispatch_id),
    agent_id: safeString(record?.agent_id),
    review_contract: normalizedEnum(record?.review_contract),
    purpose: normalizedEnum(record?.purpose),
    review_phase: normalizedEnum(record?.review_phase ?? record?.phase),
    cycle: safeInteger(record?.cycle),
    attempt: safeInteger(record?.attempt),
    status: normalizedEnum(record?.status),
    result_type: Array.isArray(result) ? "array" : result === null ? "null" : typeof result,
    result_label: typeof result === "string" ? normalizedEnum(result) : null,
    revisions_count: Array.isArray(record?.revisions) ? record.revisions.length : safeInteger(record?.revisions_total),
    findings_count: Array.isArray(record?.findings) ? record.findings.length : null,
    observations_count: Array.isArray(record?.observations) ? record.observations.length : null,
    candidate_identity: safeString(record?.candidate_identity),
  };
}

function deliveryCommit(state) {
  return safeString(state.delivery?.commit)
    ?? safeString(state.translation_delivery?.commit)
    ?? safeString(state.commit);
}

function sourceSetDigest(records) {
  const canonical = records
    .map((record) => `${record.kind}\0${record.logical_path}\0${record.size_bytes}\0${record.sha256}\n`)
    .join("");
  return sha256Buffer(Buffer.from(canonical));
}

function taskSubsetSummary(tasks) {
  const done = tasks.filter((task) => task.state === "DONE");
  return {
    tasks: tasks.length,
    done_tasks: done.length,
    done_candidate_modifier_families: countMap(done.map((task) => task.candidate_modifier.family)),
    done_reviewer_family_composition: countMap(
      done.map((task) => task.contextual_reviewer_families.join("+") || "None"),
    ),
    done_tasks_with_gpt_reviewer: done.filter(
      (task) => task.contextual_reviewer_families.includes("GPT/Codex"),
    ).length,
    done_tasks_with_gpt_only_reviewers: done.filter(
      (task) => task.contextual_reviewer_families.length === 1
        && task.contextual_reviewer_families[0] === "GPT/Codex",
    ).length,
  };
}

function buildSnapshot({ repo, agents }) {
  const taskRoot = path.join(repo, ".ai", "task");
  const reviewRoot = path.join(repo, ".ai", "reviews");
  const { byId: agentIndex, duplicates } = buildAgentIndex(agents, repo);
  const taskSources = [];
  const reviewSources = [];
  const taskRecords = [];
  const relevantAgentIds = new Set();

  for (const entry of sortedDirEntries(taskRoot)) {
    if (!entry.isDirectory() || !CORPUS_PATTERN.test(entry.name)) continue;
    const taskDir = path.join(taskRoot, entry.name);
    const stateFile = path.join(taskDir, "STATE.json");
    if (!fs.existsSync(stateFile)) continue;
    let state;
    try {
      state = readJson(stateFile);
    } catch {
      continue;
    }
    if (!isContextualTask(state)) continue;

    const orchestratorId = safeString(state.orchestrator_agent_id);
    if (orchestratorId) relevantAgentIds.add(orchestratorId);
    const orchestrator = orchestratorId && agentIndex.has(orchestratorId)
      ? agentIndex.get(orchestratorId).safe
      : { agent_id: orchestratorId, provider: null, model: null, thinking: null, mode: null, created_at: null, family: "Unknown" };
    const rawDispatches = Array.isArray(state.child_dispatches) ? state.child_dispatches : [];
    const dispatches = rawDispatches.map((dispatch) => {
      if (safeString(dispatch.agent_id)) relevantAgentIds.add(dispatch.agent_id);
      return safeDispatch(dispatch, agentIndex, repo);
    });
    if (safeString(state.candidate_author_agent_id)) relevantAgentIds.add(state.candidate_author_agent_id);

    const taskFiles = walkFiles(taskDir);
    const taskManifestRecords = taskFiles.map((file) => manifestRecord(
      file,
      `.ai/task/${entry.name}/${path.relative(taskDir, file).split(path.sep).join("/")}`,
      "task_record",
    ));
    taskSources.push(...taskManifestRecords);

    const reviewDir = path.join(reviewRoot, entry.name);
    const reviewFiles = walkFiles(reviewDir);
    const reviewManifestRecords = reviewFiles.map((file) => manifestRecord(
      file,
      `.ai/reviews/${entry.name}/${path.relative(reviewDir, file).split(path.sep).join("/")}`,
      "review_record",
    ));
    reviewSources.push(...reviewManifestRecords);
    const reviewArtifacts = reviewFiles
      .filter((file) => file.endsWith(".json"))
      .map((file) => safeReviewArtifact(file, repo, entry.name));
    for (const artifact of reviewArtifacts) {
      if (artifact.agent_id) relevantAgentIds.add(artifact.agent_id);
    }

    const candidate = candidateAttribution(state, dispatches, orchestrator);
    const contextualReviewers = dispatches.filter((dispatch) => roleClass(dispatch) === "contextual_reviewer");
    const reviewerFamilies = [...new Set(contextualReviewers.map((item) => item.agent.family))].sort();
    const commit = deliveryCommit(state);
    taskRecords.push({
      task_id: entry.name,
      state: normalizedEnum(state.state),
      cycle: safeInteger(state.cycle),
      mode: normalizedEnum(state.mode),
      change_class: normalizedEnum(state.change_class),
      orchestrator,
      candidate_modifier: candidate,
      contextual_reviewer_families: reviewerFamilies,
      candidate_reviewer_relation: reviewRelation(candidate, reviewerFamilies),
      dispatches,
      review_artifacts: reviewArtifacts,
      delivery: {
        commit,
        commit_resolves_in_source_git: commitExists(repo, commit),
      },
      source_record_sets: {
        task_files: taskManifestRecords.length,
        task_sha256: sourceSetDigest(taskManifestRecords),
        review_files: reviewManifestRecords.length,
        review_sha256: sourceSetDigest(reviewManifestRecords),
      },
    });
  }

  taskRecords.sort((a, b) => a.task_id.localeCompare(b.task_id));
  const agentSources = [];
  for (const id of [...relevantAgentIds].sort()) {
    const indexed = agentIndex.get(id);
    if (!indexed) continue;
    agentSources.push(manifestRecord(indexed.source_file, `paseo_agent_metadata/${id}.json`, "agent_metadata"));
  }
  const manifestRecords = [...taskSources, ...reviewSources, ...agentSources]
    .sort((a, b) => a.logical_path.localeCompare(b.logical_path) || a.kind.localeCompare(b.kind));

  const done = taskRecords.filter((task) => task.state === "DONE");
  const allDispatches = taskRecords.flatMap((task) => task.dispatches);
  const dispatchClassCounts = countMap(allDispatches.map(roleClass));
  const dispatchModelCounts = {};
  const dispatchModeCounts = {};
  for (const role of ["executor", "contextual_reviewer", "scout", "senior_reviewer", "other"]) {
    const roleDispatches = allDispatches.filter((dispatch) => roleClass(dispatch) === role);
    dispatchModelCounts[role] = countMap(roleDispatches.map((dispatch) => modelKey(dispatch.agent)));
    dispatchModeCounts[role] = countMap(roleDispatches.map(
      (dispatch) => `${modelKey(dispatch.agent)} :: mode=${dispatch.agent.mode ?? "?"} :: thinking=${dispatch.agent.thinking ?? "?"}`,
    ));
  }
  const missingAgents = [...relevantAgentIds].filter((id) => !agentIndex.has(id)).sort();
  const malformedReviews = taskRecords.flatMap((task) => task.review_artifacts
    .filter((record) => !record.json_valid)
    .map((record) => record.logical_path));

  const summary = {
    contextual_tasks: taskRecords.length,
    task_states: countMap(taskRecords.map((task) => task.state ?? "null")),
    done_tasks: done.length,
    done_orchestrator_families: countMap(done.map((task) => task.orchestrator.family)),
    done_candidate_modifier_families: countMap(done.map((task) => task.candidate_modifier.family)),
    done_candidate_attribution_basis: countMap(done.map((task) => task.candidate_modifier.basis)),
    done_reviewer_family_composition: countMap(done.map((task) => task.contextual_reviewer_families.join("+") || "None")),
    done_candidate_reviewer_relation: countMap(done.map((task) => task.candidate_reviewer_relation)),
    phase_breakdown: {
      P1: taskSubsetSummary(taskRecords.filter((task) => task.task_id.startsWith("p1-"))),
      P2: taskSubsetSummary(taskRecords.filter((task) => task.task_id.startsWith("p2-"))),
    },
    done_tasks_with_multiple_executor_dispatches: done.filter(
      (task) => task.dispatches.filter((dispatch) => roleClass(dispatch) === "executor").length > 1,
    ).length,
    done_tasks_with_multiple_contextual_reviewer_dispatches: done.filter(
      (task) => task.dispatches.filter((dispatch) => roleClass(dispatch) === "contextual_reviewer").length > 1,
    ).length,
    dispatch_class_counts: dispatchClassCounts,
    dispatch_model_counts: dispatchModelCounts,
    dispatch_mode_counts: dispatchModeCounts,
    done_tasks_with_explicit_delivery_commit: done.filter((task) => task.delivery.commit).length,
    explicit_delivery_commits_resolving_in_source_git: done.filter(
      (task) => task.delivery.commit && task.delivery.commit_resolves_in_source_git,
    ).length,
    missing_agent_metadata_ids: missingAgents,
    duplicate_agent_metadata_ids: duplicates.filter((id) => relevantAgentIds.has(id)),
    malformed_review_json: malformedReviews,
  };

  const sourceHead = git(repo, ["rev-parse", "HEAD"]);
  const generatorSha256 = sha256File(fileURLToPath(import.meta.url));
  const sourceManifest = {
    schema_version: SCHEMA_VERSION,
    generator_sha256: generatorSha256,
    source_repo_head: sourceHead,
    scope: "contextual-review corpus tasks selected by documented task-id and review-contract rules",
    records: manifestRecords,
    combined_sha256: sourceSetDigest(manifestRecords),
  };
  const snapshot = {
    schema_version: SCHEMA_VERSION,
    generator_sha256: generatorSha256,
    source_repo_head: sourceHead,
    source_manifest_combined_sha256: sourceManifest.combined_sha256,
    source_policy: {
      content_copied: false,
      agent_metadata_fields: ["id", "provider", "config.model", "config.thinkingOptionId", "config.modeId", "createdAt"],
      excluded_control_plane_fields: ["persistence", "session", "native handle", "MCP server configuration", "authorization headers"],
    },
    selection: {
      task_id_pattern: CORPUS_PATTERN.source,
      contextual_rule: "review_contracts contains translation_contextual_v1, contextual_reviewer purpose matches, or historical child dispatch matches",
    },
    summary,
    tasks: taskRecords,
  };
  return { snapshot, sourceManifest };
}

function writeJson(file, value) {
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const { snapshot, sourceManifest } = buildSnapshot(args);
  fs.mkdirSync(args.out, { recursive: true });
  writeJson(path.join(args.out, "SNAPSHOT.json"), snapshot);
  writeJson(path.join(args.out, "SOURCE-MANIFEST.json"), sourceManifest);
}

const invokedFile = process.argv[1] ? path.resolve(process.argv[1]) : null;
if (invokedFile === fileURLToPath(import.meta.url)) main();

export { buildSnapshot, sourceSetDigest };
