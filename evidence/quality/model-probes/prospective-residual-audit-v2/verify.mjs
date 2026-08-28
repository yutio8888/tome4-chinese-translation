#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const repoIndex = argv.indexOf("--repo");
if (repoIndex === -1 || !argv[repoIndex + 1]) throw new Error("usage: node verify.mjs --repo SOURCE_REPO");
const repo = path.resolve(argv[repoIndex + 1]);
const outputs = ["EXPERIMENT.json", "EXCLUSIONS.json", "FRAME.json", "AUDIT-QUEUE.json", "HOLDOUT-DRAFT.json"];
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-residual-audit-v2-"));
const sha256File = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");

try {
  execFileSync(process.execPath, [path.join(here, "select.mjs"), "--repo", repo, "--out", temporary], {stdio: "pipe"});
  for (const name of outputs) {
    const tracked = path.join(here, name);
    const regenerated = path.join(temporary, name);
    if (sha256File(tracked) !== sha256File(regenerated)) throw new Error(`${name}: regeneration drift`);
    JSON.parse(fs.readFileSync(tracked, "utf8"));
  }
  const experiment = JSON.parse(fs.readFileSync(path.join(here, "EXPERIMENT.json"), "utf8"));
  const invalidation = JSON.parse(fs.readFileSync(path.join(here, "INVALIDATION.json"), "utf8"));
  const frame = JSON.parse(fs.readFileSync(path.join(here, "FRAME.json"), "utf8"));
  const audit = JSON.parse(fs.readFileSync(path.join(here, "AUDIT-QUEUE.json"), "utf8"));
  const holdout = JSON.parse(fs.readFileSync(path.join(here, "HOLDOUT-DRAFT.json"), "utf8"));
  if (experiment.model_calls_made !== 0 || audit.reviewer_inference_allowed !== false) throw new Error("inference gate is open");
  if (invalidation.status !== "INVALIDATED_BEFORE_SOURCE_AUDIT" || invalidation.model_calls_made !== 0 || invalidation.source_audit_records_made !== 0) throw new Error("v2 invalidation contract");
  if (audit.items.length !== 40 || new Set(audit.items.map(item => item.task_id)).size !== 40) throw new Error("selected units are not 40 unique tasks");
  if (new Set(audit.items.map(item => `${item.task_id}\0${item.original_revision_key}`)).size !== 40) throw new Error("duplicate selected revision");
  if (holdout.items.length !== 40 || holdout.status !== "NOT_FROZEN_FOR_INFERENCE") throw new Error("holdout draft contract");
  if (frame.tasks.filter(item => item.selected).length !== 40) throw new Error("frame selected count");
  const probabilitySumByStratum = {};
  for (const task of frame.tasks) probabilitySumByStratum[task.stratum] = (probabilitySumByStratum[task.stratum] ?? 0) + task.task_inclusion_probability;
  for (const [stratum, expected] of Object.entries({same_family_only: 30, cross_or_mixed_family: 8, unknown_provenance: 2})) {
    if (Math.abs(probabilitySumByStratum[stratum] - expected) > 1e-9) throw new Error(`${stratum}: inclusion probabilities do not sum to quota`);
  }
  for (const item of audit.items) {
    if (!(item.revision_inclusion_probability > 0 && item.revision_inclusion_probability <= 1)) throw new Error(`${item.audit_id}: invalid inclusion probability`);
    if (Math.abs(item.design_weight * item.revision_inclusion_probability - 1) > 1e-9) throw new Error(`${item.audit_id}: invalid design weight`);
  }
  const serialized = outputs.map(name => fs.readFileSync(path.join(here, name), "utf8")).join("\n");
  const forbidden = [
    [/\/(?:home|Users)\//, "local absolute path"],
    [/(?:OPENAI|ANTHROPIC|GOOGLE|ZAI)_API_KEY/, "credential variable"],
    [/Authorization:\s*Bearer/i, "authorization header"]
  ];
  for (const [pattern, label] of forbidden) if (pattern.test(serialized)) throw new Error(`forbidden ${label}`);
  process.stdout.write(`${JSON.stringify({
    status: "INVALIDATED_BEFORE_SOURCE_AUDIT",
    inference_allowed: false,
    selected_items: 40,
    selected_unique_tasks: 40,
    output_hashes: Object.fromEntries(outputs.map(name => [name, sha256File(path.join(here, name))]))
  }, null, 2)}\n`);
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
