import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = file => JSON.parse(fs.readFileSync(path.join(here, file), "utf8"));
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
const experiment = read("EXPERIMENT.json");

for (const record of Object.values(experiment.frozen_bytes)) {
  if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
}
for (const [label, prior] of [["Run A", experiment.run_a], ["Run B", experiment.run_b]]) {
  if (sha256(`${prior.directory}/RESULT.json`) !== prior.result_sha256) throw new Error(`${label} RESULT hash mismatch`);
  if (sha256(`${prior.directory}/ADJUDICATION.json`) !== prior.adjudication_sha256) throw new Error(`${label} adjudication hash mismatch`);
  for (const [route, expected] of Object.entries(prior.candidate_sha256)) {
    if (sha256(`${prior.directory}/CANDIDATE-${route}.json`) !== expected) throw new Error(`${label} ${route} candidate hash mismatch`);
  }
}
const input = JSON.parse(fs.readFileSync(path.join(here, experiment.frozen_bytes.input.path), "utf8"));
if (JSON.stringify(input.items.map(item => item.revision_id)) !== JSON.stringify(["R001", "R002", "R003", "R004", "R005", "R006", "R007", "R008"])) throw new Error("input order mismatch");
const serialized = JSON.stringify(input);
for (const forbidden of ["mutation_id", "INJECTED_MUTATION", "SOURCE_VERIFIED_CONTROL", "/home/", "/Users/"]) {
  if (serialized.includes(forbidden)) throw new Error(`input leaks ${forbidden}`);
}
const resultPath = path.join(here, "RESULT.json");
if (fs.existsSync(resultPath)) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "ui-log-repeat-c-"));
  try {
    const rebuilt = path.join(temporary, "RESULT.json");
    const analysis = spawnSync(process.execPath, [path.join(here, "analyze.mjs"), "--out", rebuilt], {encoding: "utf8"});
    if (analysis.status !== 0) throw new Error(`analysis rebuild failed: ${analysis.stderr}`);
    if (!fs.readFileSync(resultPath).equals(fs.readFileSync(rebuilt))) throw new Error("RESULT.json is not byte-identical to analysis rebuild");
    const result = read("RESULT.json");
    if (result.status !== "COMPLETE" || result.routes.length !== 4) throw new Error("result completion/route mismatch");
    const routes = new Map(result.routes.map(route => [route.route, route]));
    const expectedRunHits = {
      "codex-gpt-5.6-sol-high": {A: 4, B: 4, C: 4, total: 12},
      "claude-opus-5-medium-no-advisor": {A: 3, B: 3, C: 2, total: 8},
      "pi-zai-cn-glm-5.3-flash-high": {A: 3, B: 3, C: 4, total: 10},
      "agy-gemini-3.7-flash-high": {A: 2, B: 4, C: 4, total: 10}
    };
    for (const [route, expected] of Object.entries(expectedRunHits)) {
      const actual = routes.get(route);
      for (const label of ["A", "B", "C"]) if (actual?.runs?.[label]?.mutation_hits !== expected[label]) throw new Error(`${route} Run ${label} hit count mismatch`);
      if (actual.three_run_detection.detections !== expected.total) throw new Error(`${route} three-run detection total mismatch`);
    }
    const opus = routes.get("claude-opus-5-medium-no-advisor")?.run_c_route_metadata;
    if (JSON.stringify(opus?.initialized_models) !== JSON.stringify(["claude-opus-5"]) || JSON.stringify(opus?.actual_assistant_models) !== JSON.stringify(["claude-opus-5"])) throw new Error("Opus runtime identity mismatch");
    if (opus.fallback_event_count !== 0 || opus.fallback_block_count !== 0) throw new Error("Opus fallback detected");
    const glm = routes.get("pi-zai-cn-glm-5.3-flash-high")?.run_c_route_metadata;
    if (glm?.actual_provider !== "zai-standard-cn" || glm?.actual_model !== "glm-5.3-flash") throw new Error("GLM runtime route mismatch");
    const geminiControls = routes.get("agy-gemini-3.7-flash-high")?.runs?.C;
    if (JSON.stringify(geminiControls?.control_candidate_revision_ids) !== JSON.stringify(["R003"]) || JSON.stringify(geminiControls?.source_refuted_control_candidate_revision_ids) !== JSON.stringify(["R003"])) throw new Error("Gemini R003 control adjudication mismatch");
    const expectedBCFlips = [
      {route: "claude-opus-5-medium-no-advisor", revision_id: "R008", from_detected: true, to_detected: false, direction: "hit_to_miss", from_verdict: "UNCERTAIN", to_verdict: "OK"},
      {route: "pi-zai-cn-glm-5.3-flash-high", revision_id: "R007", from_detected: false, to_detected: true, direction: "miss_to_hit", from_verdict: "OK", to_verdict: "FINDING"}
    ];
    const bc = result.pairwise_primary_comparisons.b_to_c;
    if (bc.agreements !== 14 || bc.route_mutation_comparisons !== 16 || JSON.stringify(bc.primary_flips) !== JSON.stringify(expectedBCFlips)) throw new Error("B/C primary comparison mismatch");
    const frequencies = result.three_run_derived.mutation_detection_frequency_across_all_route_runs;
    const expectedFrequencies = {R001: 12, R005: 12, R007: 6, R008: 10};
    for (const [id, detections] of Object.entries(expectedFrequencies)) if (frequencies[id]?.detections !== detections || frequencies[id]?.opportunities !== 12) throw new Error(`${id} three-run frequency mismatch`);
    if (!result.preregistered_completion_rule.satisfied || result.preregistered_completion_rule.decision !== "stop_repeated_inference_under_this_design") throw new Error("completion-rule decision mismatch");
  } finally {
    fs.rmSync(temporary, {recursive: true, force: true});
  }
  process.stdout.write("verified exact A/B/C byte reuse, Run C route artifacts and byte-identical three-run RESULT rebuild\n");
} else {
  process.stdout.write("verified exact Run A byte reuse, frozen Runs A/B hashes and blinding before Run C inference\n");
}
