import fs from "node:fs";
import os from "node:os";
import path from "node:path";
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
  process.stdout.write("verified byte-identical sampling rebuild and blinded 20-item holdout\n");
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
