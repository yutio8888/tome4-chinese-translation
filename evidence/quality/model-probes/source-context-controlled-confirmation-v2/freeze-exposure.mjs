#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../..");
const selfPrefix = "evidence/quality/model-probes/source-context-controlled-confirmation-v2/";
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const git = (args, encoding = null) => execFileSync("git", ["-C", root, ...args], {encoding, maxBuffer: 512 * 1024 * 1024});

const commit = git(["rev-parse", "HEAD"], "utf8").trim();
const paths = git(["ls-tree", "-r", "--name-only", commit, "--", "evidence/quality/model-probes"], "utf8")
  .split("\n")
  .filter(Boolean)
  .filter(name => !name.startsWith(selfPrefix))
  .filter(name => name.endsWith(".json") || name.endsWith(".jsonl"))
  .sort();

const records = paths.map(logicalPath => {
  const bytes = git(["show", `${commit}:${logicalPath}`]);
  return {logical_path: logicalPath, sha256: sha256(bytes), size_bytes: bytes.length};
});
const manifestLines = records.map(record => `${record.logical_path}\0${record.sha256}\0${record.size_bytes}\n`).join("");
const output = {
  schema_version: "source-context-controlled-confirmation-exposure-manifest-v2",
  status: "FROZEN_TRACKED_PREDECESSOR_CORPUS",
  git_commit: commit,
  selection: "All tracked .json and .jsonl files under evidence/quality/model-probes at git_commit, excluding this experiment directory.",
  interpretation: "A candidate is conservatively excluded when its revision_id or normalized source appears in a structured predecessor value. This proves only project-corpus novelty against the frozen tracked corpus.",
  records,
  counts: {
    files: records.length,
    bytes: records.reduce((sum, record) => sum + record.size_bytes, 0)
  },
  records_manifest_sha256: sha256(manifestLines)
};

fs.writeFileSync(path.join(here, "EXPOSURE-MANIFEST.json"), `${JSON.stringify(output, null, 2)}\n`, {flag: "wx"});
console.log(JSON.stringify({status: "PASS", commit, files: records.length, bytes: output.counts.bytes}, null, 2));
