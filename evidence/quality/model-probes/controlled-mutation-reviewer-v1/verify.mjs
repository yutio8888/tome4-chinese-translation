import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoIndex = process.argv.indexOf("--repo");
if (repoIndex === -1 || !process.argv[repoIndex + 1]) throw new Error("usage: node verify.mjs --repo SOURCE_REPO");
const sourceRepo = path.resolve(process.argv[repoIndex + 1]);
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "controlled-mutation-reviewer-"));
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
try {
  const build = spawnSync(process.execPath, [
    path.join(here, "build.mjs"),
    "--repo", sourceRepo,
    "--snapshot", path.join(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json"),
    "--exclusion", path.join(here, "../paseo-residual-audit-pilot-v1/PROVENANCE-KEY.json"),
    "--out", temporary
  ], {encoding: "utf8"});
  if (build.status !== 0) throw new Error(`build failed: ${build.stderr}`);
  for (const name of ["HOLDOUT.json", "REFERENCE.json", "SOURCE-CONTROLS.json", "SAMPLING.json"]) {
    if (!fs.readFileSync(path.join(here, name)).equals(fs.readFileSync(path.join(temporary, name)))) {
      throw new Error(`${name} is not byte-identical to a clean rebuild`);
    }
  }
  const holdout = JSON.parse(fs.readFileSync(path.join(here, "HOLDOUT.json"), "utf8"));
  const reference = JSON.parse(fs.readFileSync(path.join(here, "REFERENCE.json"), "utf8"));
  const expectedIds = Array.from({length: 24}, (_, index) => `C${String(index + 1).padStart(3, "0")}`);
  if (JSON.stringify(holdout.items.map(item => item.revision_id)) !== JSON.stringify(expectedIds)) throw new Error("holdout IDs/order mismatch");
  if (reference.items.filter(item => item.label === "INJECTED_MUTATION").length !== 12) throw new Error("mutation count mismatch");
  if (reference.items.filter(item => item.label === "UNMODIFIED_CONTROL").length !== 12) throw new Error("control count mismatch");
  const serializedHoldout = JSON.stringify(holdout);
  for (const forbidden of ["task_id", "original_revision_key", "mutation_id", "INJECTED_MUTATION", "UNMODIFIED_CONTROL", "/home/", "/Users/"]) {
    if (serializedHoldout.includes(forbidden)) throw new Error(`holdout leaks forbidden marker: ${forbidden}`);
  }
  const experiment = JSON.parse(fs.readFileSync(path.join(here, "EXPERIMENT.json"), "utf8"));
  for (const record of [experiment.input, experiment.sealed_reference, experiment.source_controls, experiment.prompt, experiment.output_schema]) {
    if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
  }
  process.stdout.write("verified byte-identical 24-item build, 12/12 assignment, blinding, sanitization and frozen hashes\n");
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
