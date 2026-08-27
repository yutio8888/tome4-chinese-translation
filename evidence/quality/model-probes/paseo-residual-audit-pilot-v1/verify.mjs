import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoIndex = process.argv.indexOf("--repo");
if (repoIndex === -1 || !process.argv[repoIndex + 1]) {
  throw new Error("usage: node verify.mjs --repo /path/to/source-repo");
}
const repo = path.resolve(process.argv[repoIndex + 1]);
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "paseo-residual-audit-"));
try {
  const run = spawnSync(process.execPath, [
    path.join(here, "select.mjs"),
    "--repo", repo,
    "--snapshot", path.join(here, "../paseo-provenance-snapshot-v1/SNAPSHOT.json"),
    "--out", temporary
  ], {encoding: "utf8"});
  if (run.status !== 0) throw new Error(`selection rebuild failed: ${run.stderr}`);
  for (const name of ["HOLDOUT.json", "PROVENANCE-KEY.json", "SAMPLING.json"]) {
    const expected = fs.readFileSync(path.join(here, name));
    const actual = fs.readFileSync(path.join(temporary, name));
    if (!expected.equals(actual)) throw new Error(`${name} is not byte-identical to a clean rebuild`);
  }
  const holdout = JSON.parse(fs.readFileSync(path.join(here, "HOLDOUT.json"), "utf8"));
  const expectedIds = Array.from({length: 20}, (_, index) => `H${String(index + 1).padStart(3, "0")}`);
  if (JSON.stringify(holdout.items.map(item => item.revision_id)) !== JSON.stringify(expectedIds)) {
    throw new Error("holdout IDs are not exact H001-H020 order");
  }
  const leakedKeys = new Set(["stratum", "task_id", "original_revision_key", "orchestrator_family", "candidate_modifier", "contextual_reviewer_families"]);
  for (const item of holdout.items) {
    for (const key of Object.keys(item)) if (leakedKeys.has(key)) throw new Error(`provenance key leaked into holdout: ${key}`);
  }
  const experiment = JSON.parse(fs.readFileSync(path.join(here, "EXPERIMENT.json"), "utf8"));
  const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
  for (const [name, record] of Object.entries({
    input: experiment.input,
    prompt: experiment.prompt,
    output_schema: experiment.output_schema,
    hidden_provenance: experiment.hidden_provenance
  })) {
    if (sha256(record.path) !== record.sha256) throw new Error(`${name} frozen hash mismatch`);
  }
  const candidateFiles = fs.readdirSync(here).filter(name => /^CANDIDATE-.*\.json$/.test(name)).sort();
  if (candidateFiles.length !== 5) throw new Error(`expected 5 candidates, found ${candidateFiles.length}`);
  for (const name of candidateFiles) {
    const candidate = JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
    if (!candidate.valid) throw new Error(`${name} is not valid`);
  }
  const expectedResult = fs.readFileSync(path.join(here, "RESULT.json"));
  const analysis = spawnSync(process.execPath, [path.join(here, "analyze.mjs")], {encoding: "utf8"});
  if (analysis.status !== 0) throw new Error(`analysis rebuild failed: ${analysis.stderr}`);
  const rebuiltResult = fs.readFileSync(path.join(here, "RESULT.json"));
  if (!expectedResult.equals(rebuiltResult)) throw new Error("RESULT.json is not byte-identical to an analysis rebuild");
  const result = JSON.parse(rebuiltResult);
  for (const [name, digest] of Object.entries(result.artifact_hashes.candidates)) {
    if (sha256(name) !== digest) throw new Error(`${name} result hash mismatch`);
  }
  for (const [name, digest] of Object.entries(result.artifact_hashes.raw)) {
    if (sha256(name) !== digest) throw new Error(`${name} result hash mismatch`);
  }
  if (sha256("ADJUDICATION.json") !== result.artifact_hashes.adjudication) throw new Error("adjudication result hash mismatch");
  process.stdout.write("verified byte-identical sampling/result rebuild, blinded holdout, five valid candidates and RAW hashes\n");
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
