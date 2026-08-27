import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
function arg(name) { const index = process.argv.indexOf(name); return index === -1 ? null : process.argv[index + 1]; }
const repo = arg("--repo"), dlcRoot = arg("--dlc-root"), engineRepo = arg("--engine-repo");
if (!repo || !dlcRoot || !engineRepo) throw new Error("usage: node verify.mjs --repo REPO --dlc-root DLC_ROOT --engine-repo ENGINE");
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "ui-log-replication-v2-"));
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
try {
  const build = spawnSync(process.execPath, [path.join(here, "build.mjs"), "--repo", repo, "--dlc-root", dlcRoot, "--engine-repo", engineRepo, "--out", temporary], {encoding: "utf8"});
  if (build.status !== 0) throw new Error(`build failed: ${build.stderr}`);
  for (const name of ["HOLDOUT.json", "REFERENCE.json", "SOURCE-CONTROLS.json", "SAMPLING.json"]) {
    if (!fs.readFileSync(path.join(here, name)).equals(fs.readFileSync(path.join(temporary, name)))) throw new Error(`${name} is not byte-identical to a clean rebuild`);
  }
  const holdout = JSON.parse(fs.readFileSync(path.join(here, "HOLDOUT.json"), "utf8"));
  const reference = JSON.parse(fs.readFileSync(path.join(here, "REFERENCE.json"), "utf8"));
  const expectedIds = Array.from({length: 8}, (_, index) => `R${String(index + 1).padStart(3, "0")}`);
  if (JSON.stringify(holdout.items.map(item => item.revision_id)) !== JSON.stringify(expectedIds)) throw new Error("holdout IDs/order mismatch");
  if (reference.items.filter(item => item.label === "INJECTED_MUTATION").length !== 4) throw new Error("mutation count mismatch");
  if (reference.items.filter(item => item.label === "SOURCE_VERIFIED_CONTROL").length !== 4) throw new Error("control count mismatch");
  const serialized = JSON.stringify(holdout);
  for (const forbidden of ["task_id", "original_revision_key", "mutation_id", "INJECTED_MUTATION", "SOURCE_VERIFIED_CONTROL", "/home/", "/Users/"]) if (serialized.includes(forbidden)) throw new Error(`holdout leaks ${forbidden}`);
  const experiment = JSON.parse(fs.readFileSync(path.join(here, "EXPERIMENT.json"), "utf8"));
  for (const record of [experiment.input, experiment.sealed_reference, experiment.source_controls, experiment.source_verification, experiment.prompt, experiment.output_schema]) if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
  const resultPath = path.join(here, "RESULT.json");
  if (fs.existsSync(resultPath)) {
    const rebuiltResult = path.join(temporary, "RESULT.json");
    const analysis = spawnSync(process.execPath, [path.join(here, "analyze.mjs"), "--out", rebuiltResult], {encoding: "utf8"});
    if (analysis.status !== 0) throw new Error(`analysis rebuild failed: ${analysis.stderr}`);
    if (!fs.readFileSync(resultPath).equals(fs.readFileSync(rebuiltResult))) throw new Error("RESULT.json is not byte-identical to a clean analysis rebuild");
    const result = JSON.parse(fs.readFileSync(resultPath, "utf8"));
    if (result.status !== "COMPLETE" || result.scores.length !== 4) throw new Error("result completion/route count mismatch");
    const opus = result.scores.find(score => score.route === "claude-opus-5-medium-no-advisor");
    if (JSON.stringify(opus?.route_metadata?.actual_assistant_models) !== JSON.stringify(["claude-opus-5"])) throw new Error("Opus actual assistant model mismatch");
    if (opus.route_metadata.fallback_event_count !== 0 || opus.route_metadata.fallback_block_count !== 0) throw new Error("Opus fallback detected");
    const glm = result.scores.find(score => score.route === "pi-zai-cn-glm-5.3-flash-high");
    if (glm?.route_metadata?.actual_provider !== "zai-standard-cn" || glm?.route_metadata?.actual_model !== "glm-5.3-flash") throw new Error("GLM actual route mismatch");
    if (result.derived.mutation_union.hits !== 4 || result.derived.four_route_consensus.hits !== 2) throw new Error("derived mutation score mismatch");
    if (result.scores.some(score => score.source_verified_controls.true_negatives !== 4)) throw new Error("control result mismatch");
    process.stdout.write("verified byte-identical 8-item and RESULT rebuild, direct source hashes, 4/4 assignment, route identities, blinding, sanitization and frozen hashes\n");
  } else {
    process.stdout.write("verified byte-identical 8-item rebuild, direct source hashes, 4/4 assignment, blinding, sanitization and frozen hashes\n");
  }
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
