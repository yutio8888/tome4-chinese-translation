#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, loadAndBuild, OUTPUT_NAMES, sha256Bytes} from "./build-target-queue.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "../../../..");

function parseArgs(argv) {
  const args = {root: defaultRoot};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--root", "--production-repo", "--queue-dir"].includes(flag)) throw new Error("usage: node verify-target-queue.mjs --production-repo PRODUCTION --queue-dir QUEUE [--root RESEARCH]");
    args[flag.slice(2).replace(/-([a-z])/gu, (_match, letter) => letter.toUpperCase())] = path.resolve(value);
  }
  if (!args.productionRepo || !args.queueDir) throw new Error("--production-repo and --queue-dir are required");
  return args;
}

const args = parseArgs(process.argv.slice(2));
const rebuilt = loadAndBuild(args);
for (const name of OUTPUT_NAMES) {
  const tracked = fs.readFileSync(path.join(args.queueDir, name));
  const expected = jsonBytes(rebuilt[name]);
  assert.deepEqual(tracked, expected, `${name}: deterministic rebuild differs`);
  JSON.parse(tracked.toString("utf8"));
}
const report = rebuilt["TARGET-JOIN-REPORT.json"];
assert.equal(report.status, "PASS_TARGET_JOIN_GATES");
assert.equal(report.model_calls_made, 0);
assert.equal(report.network_calls_made, 0);
assert.ok(Object.values(report.gates).every(Boolean));
process.stdout.write(`${JSON.stringify({
  status: "PASS",
  target_bound_presentation_sha256: report.target_bound_presentation_sha256,
  output_hashes: Object.fromEntries(OUTPUT_NAMES.map(name => [name, sha256Bytes(jsonBytes(rebuilt[name]))]))
}, null, 2)}\n`);
