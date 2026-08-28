#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {FROZEN} from "./scanner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const repoIndex = argv.indexOf("--repo");
if (repoIndex === -1 || !argv[repoIndex + 1]) throw new Error("usage: node verify.mjs --repo SOURCE_REPO");
const repo = path.resolve(argv[repoIndex + 1]);
const sha256File = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "deterministic-linebreak-lint-v1-"));
const sourceWorktree = path.join(temporary, "source");
const rebuiltCandidates = path.join(temporary, "CANDIDATES.json");
let worktreeAdded = false;

function findInventory(directory) {
  const root = path.join(directory, ".artifacts", "i18n", "quality", "runs");
  const matches = [];
  const visit = current => {
    for (const entry of fs.readdirSync(current, {withFileTypes: true})) {
      const absolute = path.join(current, entry.name);
      if (entry.isDirectory()) visit(absolute);
      else if (entry.isFile() && entry.name === "inventory.jsonl") matches.push(absolute);
    }
  };
  visit(root);
  if (matches.length !== 1) throw new Error(`expected one inventory, found ${matches.length}`);
  return matches[0];
}

try {
  for (const name of ["EXPERIMENT.json", "RULE-CONTRACT.json", "SCANNER-FIXTURES.json", "CANDIDATES.json", "SOURCE-AUDIT.json", "RESULT.json"]) {
    JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
  }
  execFileSync(process.execPath, [path.join(here, "test-scanner.mjs")], {stdio: "pipe"});
  execFileSync("git", ["-C", repo, "worktree", "add", "--detach", sourceWorktree, FROZEN.productionCommit], {stdio: "pipe"});
  worktreeAdded = true;
  const report = JSON.parse(execFileSync("python3", ["-B", "tools/i18n", "quality", "inventory", "--json"], {
    cwd: sourceWorktree,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"]
  }));
  if (report.inventory_sha256 !== FROZEN.inventoryCanonicalSha256) throw new Error("inventory canonical digest drift");
  if (report.translation_inputs_sha256 !== FROZEN.translationInputsSha256) throw new Error("translation-input digest drift");
  if (report.entries !== FROZEN.inventoryRows || report.tool_version !== "0.5.0") throw new Error("inventory report drift");
  const inventory = findInventory(sourceWorktree);
  execFileSync(process.execPath, [
    path.join(here, "scan.mjs"),
    "--inventory", inventory,
    "--schema", path.join(sourceWorktree, "i18n", "quality", "schemas", "inventory-v1.schema.json"),
    "--out", rebuiltCandidates
  ], {stdio: "pipe"});
  if (fs.readFileSync(rebuiltCandidates, "utf8") !== fs.readFileSync(path.join(here, "CANDIDATES.json"), "utf8")) {
    throw new Error("candidate regeneration drift");
  }

  const candidates = JSON.parse(fs.readFileSync(path.join(here, "CANDIDATES.json"), "utf8"));
  const audit = JSON.parse(fs.readFileSync(path.join(here, "SOURCE-AUDIT.json"), "utf8"));
  const result = JSON.parse(fs.readFileSync(path.join(here, "RESULT.json"), "utf8"));
  if (candidates.candidates.length !== 5 || candidates.scan_counts.raw_han_lf_han_boundaries !== 246 || candidates.scan_counts.raw_revisions !== 89) {
    throw new Error("candidate count drift");
  }
  if (candidates.candidates.some(candidate => candidate.status !== "CANDIDATE_NOT_GROUND_TRUTH")) throw new Error("candidate was promoted before audit");
  if (audit.candidate_artifact.sha256 !== sha256File(path.join(here, "CANDIDATES.json"))) throw new Error("audit candidate binding drift");
  if (audit.records.length !== candidates.candidates.length || new Set(audit.records.map(record => record.candidate_id)).size !== audit.records.length) {
    throw new Error("source-audit coverage drift");
  }
  for (const candidate of candidates.candidates) {
    const record = audit.records.find(value => value.candidate_id === candidate.candidate_id);
    if (!record || record.revision_id !== candidate.revision_id || record.boundary !== candidate.boundary.rendered) throw new Error(`${candidate.candidate_id}: audit identity drift`);
    if (record.verdict !== "CONFIRMED_FORMAT_DEFECT" || record.primary_adjudicator_verified !== true) throw new Error(`${candidate.candidate_id}: unexpected audit verdict`);
  }
  if (result.measured_candidate_audit.confirmed_format_defects !== 5 || result.measured_candidate_audit.newly_discovered_beyond_R033 !== 4) {
    throw new Error("result candidate accounting drift");
  }
  if (result.artifact_bindings.candidates.sha256 !== sha256File(path.join(here, "CANDIDATES.json")) || result.artifact_bindings.source_audit.sha256 !== sha256File(path.join(here, "SOURCE-AUDIT.json"))) {
    throw new Error("result artifact binding drift");
  }
  const executor = path.resolve(here, "../qwen3-8-27b-agent-roles/executor-fixture.lua");
  if (sha256File(executor) !== "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7") throw new Error("executor fixture baseline drift");
  const serialized = ["EXPERIMENT.json", "RULE-CONTRACT.json", "CANDIDATES.json", "SOURCE-AUDIT.json", "RESULT.json"].map(name => fs.readFileSync(path.join(here, name), "utf8")).join("\n");
  for (const [pattern, label] of [[/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/u, "local absolute path"], [/(?:OPENAI|ANTHROPIC|GOOGLE|ZAI)_API_KEY/u, "credential variable"], [/Authorization:\s*Bearer/iu, "authorization header"]]) {
    if (pattern.test(serialized)) throw new Error(`forbidden ${label}`);
  }
  process.stdout.write(`${JSON.stringify({
    status: "PASS",
    production_translation_commit: FROZEN.productionCommit,
    inventory_canonical_sha256: FROZEN.inventoryCanonicalSha256,
    candidates_sha256: sha256File(path.join(here, "CANDIDATES.json")),
    source_audit_sha256: sha256File(path.join(here, "SOURCE-AUDIT.json")),
    confirmed_format_defects: audit.counts.confirmed_format_defects,
    known_R033_detected: candidates.candidates.some(candidate => candidate.revision_id === FROZEN.knownCalibrationRevision)
  }, null, 2)}\n`);
} finally {
  if (worktreeAdded) {
    try {
      execFileSync("git", ["-C", repo, "worktree", "remove", sourceWorktree], {stdio: "pipe"});
    } catch (error) {
      process.stderr.write(`temporary worktree cleanup failed: ${error.message}\n`);
    }
  }
  const expectedPrefix = path.join(os.tmpdir(), "deterministic-linebreak-lint-v1-");
  if (path.dirname(temporary) !== os.tmpdir() || !temporary.startsWith(expectedPrefix)) throw new Error(`refusing to remove unexpected temporary path: ${temporary}`);
  fs.rmSync(temporary, {recursive: true, force: true});
}
