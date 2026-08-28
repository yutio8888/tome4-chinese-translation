#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const productionCommit = "1666481409f4c0d63d66e84659f6b6145d8d25d0";
const canonicalInventorySha256 = "bf9153e83aba7318741f065d8541ae74783eebc5d4552ec38627a4313456b215";
const sourceAuditProtocolSha256 = "95d290e728956c0ac9efeeaa05164ba53d37e3d2a78790c7e3cf82b1b078c35b";
const sourceLocatorContractSha256 = "c0a8a52f2a2a99afe00881132d224ad14e2f82c91e77f61c735cb23be669313a";
const sourceLocatorsSha256 = "f58d138a42a4a09665c1ddb0ff4e4ad4be9fae7811095e962e667e3d5bfab10c";
const outputs = [
  "EXPERIMENT.json",
  "EXCLUSIONS.json",
  "CANONICAL-MEMBERSHIP.json",
  "FRAME.json",
  "AUDIT-QUEUE.json",
  "HOLDOUT-DRAFT.json",
  "BUILD-REPORT.json"
];

const argv = process.argv.slice(2);
const repoIndex = argv.indexOf("--repo");
if (repoIndex === -1 || !argv[repoIndex + 1]) throw new Error("usage: node verify.mjs --repo SOURCE_REPO");
const repo = path.resolve(argv[repoIndex + 1]);
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-residual-audit-v3-"));
const sourceWorktree = path.join(temporary, "source");
const regenerated = path.join(temporary, "regenerated");
const sha256File = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");

function findInventory(directory) {
  const matches = [];
  const visit = current => {
    for (const entry of fs.readdirSync(current, {withFileTypes: true})) {
      const absolute = path.join(current, entry.name);
      if (entry.isDirectory()) visit(absolute);
      else if (entry.isFile() && entry.name === "inventory.jsonl") matches.push(absolute);
    }
  };
  visit(path.join(directory, ".artifacts", "i18n", "quality", "runs"));
  if (matches.length !== 1) throw new Error(`expected one generated inventory, found ${matches.length}`);
  return matches[0];
}

function canonicalInventoryDigest(file) {
  const rows = fs.readFileSync(file, "utf8").trimEnd().split("\n").filter(Boolean).map(JSON.parse);
  return sha256Bytes(JSON.stringify(rows));
}

let worktreeAdded = false;
try {
  execFileSync("git", ["-C", repo, "worktree", "add", "--detach", sourceWorktree, productionCommit], {stdio: "pipe"});
  worktreeAdded = true;
  const inventoryReport = JSON.parse(execFileSync(
    "python3",
    ["-B", "tools/i18n", "quality", "inventory", "--json"],
    {cwd: sourceWorktree, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"]}
  ));
  const inventoryPath = findInventory(sourceWorktree);
  if (inventoryReport.inventory_sha256 !== canonicalInventorySha256) throw new Error("inventory command canonical digest drift");
  if (inventoryReport.tool_version !== "0.5.0") throw new Error(`inventory tool version drift: ${inventoryReport.tool_version}`);
  if (inventoryReport.translation_inputs_sha256 !== "051423b82b6594b42d9777f2e9f487e49014e7a82401187bd09c14d9d181c4da") {
    throw new Error("translation input digest drift");
  }
  if (canonicalInventoryDigest(inventoryPath) !== canonicalInventorySha256) throw new Error("generated inventory canonical digest drift");

  fs.mkdirSync(regenerated);
  execFileSync(process.execPath, [
    path.join(here, "build.mjs"),
    "--repo", repo,
    "--inventory", inventoryPath,
    "--out", regenerated
  ], {stdio: "pipe"});
  for (const name of outputs) {
    const tracked = path.join(here, name);
    const rebuilt = path.join(regenerated, name);
    if (sha256File(tracked) !== sha256File(rebuilt)) throw new Error(`${name}: regeneration drift`);
    JSON.parse(fs.readFileSync(tracked, "utf8"));
  }

  const experiment = JSON.parse(fs.readFileSync(path.join(here, "EXPERIMENT.json"), "utf8"));
  const exclusions = JSON.parse(fs.readFileSync(path.join(here, "EXCLUSIONS.json"), "utf8"));
  const membership = JSON.parse(fs.readFileSync(path.join(here, "CANONICAL-MEMBERSHIP.json"), "utf8"));
  const frame = JSON.parse(fs.readFileSync(path.join(here, "FRAME.json"), "utf8"));
  const audit = JSON.parse(fs.readFileSync(path.join(here, "AUDIT-QUEUE.json"), "utf8"));
  const holdout = JSON.parse(fs.readFileSync(path.join(here, "HOLDOUT-DRAFT.json"), "utf8"));
  const report = JSON.parse(fs.readFileSync(path.join(here, "BUILD-REPORT.json"), "utf8"));
  const auditProtocolPath = path.join(here, "SOURCE-AUDIT-PROTOCOL.json");
  const locatorContractPath = path.join(here, "SOURCE-LOCATOR-CONTRACT.json");
  const sourceLocatorsPath = path.join(here, "SOURCE-LOCATORS.json");
  const auditProtocol = JSON.parse(fs.readFileSync(auditProtocolPath, "utf8"));
  const locatorContract = JSON.parse(fs.readFileSync(locatorContractPath, "utf8"));
  const sourceLocators = JSON.parse(fs.readFileSync(sourceLocatorsPath, "utf8"));

  if (sha256File(auditProtocolPath) !== sourceAuditProtocolSha256) throw new Error("source audit protocol hash drift");
  if (sha256File(locatorContractPath) !== sourceLocatorContractSha256) throw new Error("source locator contract hash drift");
  if (sha256File(sourceLocatorsPath) !== sourceLocatorsSha256) throw new Error("source locators hash drift");
  if (auditProtocol.status !== "FROZEN_BEFORE_SOURCE_AUDIT" || auditProtocol.later_reviewer_route_outputs_available_to_adjudicator !== false || auditProtocol.replacement_allowed !== false) {
    throw new Error("source audit protocol gate");
  }
  if (JSON.stringify(Object.keys(auditProtocol.verdicts).sort()) !== JSON.stringify(["CONFIRMED", "INDETERMINATE", "REFUTED", "UNREACHABLE"])) {
    throw new Error("source audit verdict contract");
  }
  for (const field of ["audit_id", "verdict", "evidence_class", "source_locator", "source_artifact_sha256", "visible_context_sha256s", "source_occurrences", "reason", "audited_at_utc", "audit_assistance", "primary_adjudicator_verified"]) {
    if (!auditProtocol.required_record_per_item.includes(field)) throw new Error(`source audit required field missing: ${field}`);
  }
  if (JSON.stringify(auditProtocol.record_schema?.evidence_class?.enum) !== JSON.stringify(["RUNTIME_SOURCE_REQUIRED", "FIXED_SOURCE_CONTEXT", "TERMINOLOGY_CONTRACT", "FORMAT_STRUCTURE", "SURFACE_BILINGUAL"])) {
    throw new Error("source audit evidence class contract drift");
  }
  if (auditProtocol.record_schema?.source_locator?.artifact !== "SOURCE-LOCATORS.json" || auditProtocol.record_schema?.primary_adjudicator_verified?.final_value !== true) {
    throw new Error("source audit record binding contract drift");
  }
  if (!auditProtocol.record_schema?.visible_context_sha256s?.binding?.includes("used_occurrence_ordinals")) {
    throw new Error("source audit occurrence hash binding missing");
  }
  if (!auditProtocol.locator_to_verdict_rules?.LOCATED_MULTIPLE?.includes("Review every occurrence") || auditProtocol.locator_to_verdict_rules?.SOURCE_NOT_FOUND !== "Use UNREACHABLE unless a separately frozen fixed-source binding already exists; do not search a new unregistered corpus after seeing the item.") {
    throw new Error("source audit locator-to-verdict contract drift");
  }
  if (!auditProtocol.audit_assistance_policy?.not_ground_truth || !auditProtocol.audit_assistance_policy?.prohibited) {
    throw new Error("source audit assistance policy missing");
  }
  if (locatorContract.status !== "FROZEN_BEFORE_SOURCE_LOCATION" || locatorContract.expected_items !== 40) throw new Error("source locator contract gate");
  if (locatorContract.locator.multiple_occurrences !== "Record every occurrence. Do not choose one occurrence or infer equivalence mechanically.") {
    throw new Error("source locator multiple-occurrence policy drift");
  }
  if (sourceLocators.status !== "ALL_SOURCE_ARTIFACTS_LOCATED" || sourceLocators.contains_audit_verdicts !== false || sourceLocators.model_calls_made !== 0) {
    throw new Error("source locator output gate");
  }
  if (sourceLocators.queue_sha256 !== sha256File(path.join(here, "AUDIT-QUEUE.json")) || sourceLocators.locator_contract_sha256 !== sourceLocatorContractSha256) {
    throw new Error("source locator input binding drift");
  }
  if (sourceLocators.items.length !== 40 || sourceLocators.items.some(item => !["LOCATED_UNIQUE", "LOCATED_MULTIPLE"].includes(item.locator_status))) {
    throw new Error("source locator coverage gate");
  }
  if (experiment.frozen_contracts?.source_audit_protocol?.sha256 !== sourceAuditProtocolSha256 || experiment.frozen_contracts?.source_locator_contract?.sha256 !== sourceLocatorContractSha256) {
    throw new Error("experiment frozen contract binding drift");
  }

  if (experiment.model_calls_made !== 0 || audit.reviewer_inference_allowed !== false || report.model_calls_made !== 0) {
    throw new Error("inference gate is open");
  }
  if (audit.items.length !== 40 || new Set(audit.items.map(item => item.task_id)).size !== 40) {
    throw new Error("selected units are not 40 unique tasks");
  }
  if (new Set(audit.items.map(item => item.canonical_identity.revision_id)).size !== 40) {
    throw new Error("selected canonical revisions are not unique");
  }
  if (membership.items.length !== 1396 || new Set(membership.items.map(item => item.canonical_revision_id)).size !== 1396) {
    throw new Error("canonical membership is not 1396 unique production revisions");
  }
  if (holdout.items.length !== 40 || holdout.status !== "NOT_FROZEN_FOR_INFERENCE") throw new Error("holdout draft contract");
  if (frame.tasks.filter(item => item.selected).length !== 40) throw new Error("frame selected count");
  if (exclusions.prior_experiment_item_pairs.length !== 88) throw new Error("prior item exclusion count");
  if (exclusions.canonical_resolution_exclusions.length !== 128) throw new Error("canonical resolution exclusion count");
  if (exclusions.canonical_resolution_exclusions.some(item => item.reason.startsWith("AMBIGUOUS_"))) {
    throw new Error("ambiguous item survived canonical context resolution");
  }

  const probabilitySumByStratum = {};
  for (const task of frame.tasks) {
    probabilitySumByStratum[task.stratum] = (probabilitySumByStratum[task.stratum] ?? 0) + task.task_inclusion_probability;
  }
  for (const [stratum, expected] of Object.entries({same_family_only: 24, cross_or_mixed_family: 14, unknown_provenance: 2})) {
    if (Math.abs(probabilitySumByStratum[stratum] - expected) > 1e-9) {
      throw new Error(`${stratum}: inclusion probabilities do not sum to quota`);
    }
  }
  for (const item of audit.items) {
    if (!(item.revision_inclusion_probability > 0 && item.revision_inclusion_probability <= 1)) {
      throw new Error(`${item.audit_id}: invalid inclusion probability`);
    }
    if (Math.abs(item.design_weight * item.revision_inclusion_probability - 1) > 1e-9) {
      throw new Error(`${item.audit_id}: invalid design weight`);
    }
    const member = membership.items.find(candidate =>
      candidate.task_id === item.task_id &&
      candidate.original_revision_key === item.original_revision_key &&
      candidate.canonical_revision_id === item.canonical_identity.revision_id
    );
    if (!member || member.membership_sha256 !== item.canonical_identity.membership_sha256) {
      throw new Error(`${item.audit_id}: selected item is not in frozen canonical membership`);
    }
  }

  const serialized = [...outputs, "SOURCE-AUDIT-PROTOCOL.json", "SOURCE-LOCATOR-CONTRACT.json", "SOURCE-LOCATORS.json"]
    .map(name => fs.readFileSync(path.join(here, name), "utf8")).join("\n");
  const forbidden = [
    [/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/, "local absolute path"],
    [/(?:OPENAI|ANTHROPIC|GOOGLE|ZAI)_API_KEY/, "credential variable"],
    [/Authorization:\s*Bearer/i, "authorization header"]
  ];
  for (const [pattern, label] of forbidden) if (pattern.test(serialized)) throw new Error(`forbidden ${label}`);

  process.stdout.write(`${JSON.stringify({
    status: "GO_FOR_SOURCE_AUDIT_ONLY",
    inference_allowed: false,
    production_translation_commit: productionCommit,
    canonical_inventory_sha256: canonicalInventorySha256,
    eligible_canonical_revisions: membership.items.length,
    selected_items: audit.items.length,
    selected_unique_tasks: new Set(audit.items.map(item => item.task_id)).size,
    output_hashes: Object.fromEntries(outputs.map(name => [name, sha256File(path.join(here, name))])),
    frozen_source_contract_hashes: {
      source_audit_protocol: sourceAuditProtocolSha256,
      source_locator_contract: sourceLocatorContractSha256,
      source_locators: sourceLocatorsSha256
    }
  }, null, 2)}\n`);
} finally {
  if (worktreeAdded) {
    try {
      execFileSync("git", ["-C", repo, "worktree", "remove", sourceWorktree], {stdio: "pipe"});
    } catch (error) {
      process.stderr.write(`temporary worktree cleanup failed: ${error.message}\n`);
    }
  }
  const expectedPrefix = `${path.join(os.tmpdir(), "prospective-residual-audit-v3-")}`;
  if (path.dirname(temporary) !== os.tmpdir() || !temporary.startsWith(expectedPrefix)) {
    throw new Error(`refusing to remove unexpected temporary path: ${temporary}`);
  }
  fs.rmSync(temporary, {recursive: true, force: true});
}
