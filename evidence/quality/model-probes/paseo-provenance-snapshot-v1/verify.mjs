#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 2) args[argv[i]?.replace(/^--/, "")] = argv[i + 1];
  if (!args.repo || !args.agents) {
    throw new Error("usage: node verify.mjs --repo <translation-repo> --agents <paseo-agent-dir>");
  }
  return { repo: path.resolve(args.repo), agents: path.resolve(args.agents) };
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function compareFile(expected, actual) {
  const expectedBytes = fs.readFileSync(expected);
  const actualBytes = fs.readFileSync(actual);
  assert(expectedBytes.equals(actualBytes), `${path.basename(expected)} is not byte-identical to a clean rebuild`);
  return expectedBytes.toString("utf8");
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const here = path.dirname(fileURLToPath(import.meta.url));
  const temporaryRoot = fs.mkdtempSync(path.join(os.tmpdir(), "paseo-provenance-verify-"));
  try {
    execFileSync(process.execPath, [path.join(here, "generate.mjs"), "--repo", args.repo, "--agents", args.agents, "--out", temporaryRoot], {
      stdio: "inherit",
    });
    const snapshotText = compareFile(path.join(here, "SNAPSHOT.json"), path.join(temporaryRoot, "SNAPSHOT.json"));
    const manifestText = compareFile(path.join(here, "SOURCE-MANIFEST.json"), path.join(temporaryRoot, "SOURCE-MANIFEST.json"));
    const combined = `${snapshotText}\n${manifestText}`;
    for (const banned of [
      /"Authorization"\s*:/i,
      /Bearer\s+/i,
      /"sessionId"\s*:/i,
      /"nativeHandle"\s*:/i,
      /"mcpServers"\s*:/i,
      /"persistence"\s*:/i,
      /"apiKey"\s*:/i,
      /\/home\/yun\//,
    ]) {
      assert(!banned.test(combined), `tracked output contains banned pattern ${banned}`);
    }
    const snapshot = JSON.parse(snapshotText);
    const manifest = JSON.parse(manifestText);
    assert(snapshot.schema_version === "paseo-provenance-snapshot-v1", "unexpected snapshot schema");
    const generatorSha256 = crypto.createHash("sha256").update(fs.readFileSync(path.join(here, "generate.mjs"))).digest("hex");
    assert(snapshot.generator_sha256 === generatorSha256, "snapshot generator digest mismatch");
    assert(manifest.generator_sha256 === generatorSha256, "manifest generator digest mismatch");
    assert(snapshot.source_manifest_combined_sha256 === manifest.combined_sha256, "manifest digest linkage mismatch");
    assert(snapshot.summary.contextual_tasks === snapshot.tasks.length, "task count mismatch");
    assert(snapshot.summary.done_tasks === snapshot.tasks.filter((task) => task.state === "DONE").length, "DONE count mismatch");
    assert(manifest.records.length > 0, "source manifest is empty");
    process.stdout.write(
      `verified byte-identical rebuild: ${snapshot.tasks.length} tasks, ${manifest.records.length} source records\n`,
    );
  } finally {
    fs.rmSync(temporaryRoot, { recursive: true, force: true });
  }
}

main();
