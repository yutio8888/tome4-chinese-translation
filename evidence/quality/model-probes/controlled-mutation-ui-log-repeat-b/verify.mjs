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
for (const record of Object.values(experiment.frozen_bytes)) if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
if (sha256("../controlled-mutation-ui-log-replication-v2/RESULT.json") !== experiment.run_a.result_sha256) throw new Error("Run A RESULT hash mismatch");
if (sha256("../controlled-mutation-ui-log-replication-v2/ADJUDICATION.json") !== experiment.run_a.adjudication_sha256) throw new Error("Run A adjudication hash mismatch");
for (const [route, expected] of Object.entries(experiment.run_a.candidate_sha256)) if (sha256(`../controlled-mutation-ui-log-replication-v2/CANDIDATE-${route}.json`) !== expected) throw new Error(`Run A ${route} candidate hash mismatch`);
const input = JSON.parse(fs.readFileSync(path.join(here, experiment.frozen_bytes.input.path), "utf8"));
if (JSON.stringify(input.items.map(item => item.revision_id)) !== JSON.stringify(["R001", "R002", "R003", "R004", "R005", "R006", "R007", "R008"])) throw new Error("input order mismatch");
const serialized = JSON.stringify(input);
for (const forbidden of ["mutation_id", "INJECTED_MUTATION", "SOURCE_VERIFIED_CONTROL", "/home/", "/Users/"]) if (serialized.includes(forbidden)) throw new Error(`input leaks ${forbidden}`);
const resultPath = path.join(here, "RESULT.json");
if (fs.existsSync(resultPath)) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "ui-log-repeat-b-"));
  try {
    const rebuilt = path.join(temporary, "RESULT.json");
    const analysis = spawnSync(process.execPath, [path.join(here, "analyze.mjs"), "--out", rebuilt], {encoding: "utf8"});
    if (analysis.status !== 0) throw new Error(`analysis rebuild failed: ${analysis.stderr}`);
    if (!fs.readFileSync(resultPath).equals(fs.readFileSync(rebuilt))) throw new Error("RESULT.json is not byte-identical to analysis rebuild");
    const result = read("RESULT.json");
    if (result.status !== "COMPLETE" || result.routes.length !== 4) throw new Error("result completion/route mismatch");
    const routes = new Map(result.routes.map(route => [route.route, route]));
    const expectedRunBHits = {
      "codex-gpt-5.6-sol-high": ["R001", "R005", "R007", "R008"],
      "claude-opus-5-medium-no-advisor": ["R001", "R005", "R008"],
      "pi-zai-cn-glm-5.3-flash-high": ["R001", "R005", "R008"],
      "agy-gemini-3.7-flash-high": ["R001", "R005", "R007", "R008"]
    };
    for (const [route, hits] of Object.entries(expectedRunBHits)) {
      if (JSON.stringify(routes.get(route)?.run_b?.hit_revision_ids) !== JSON.stringify(hits)) throw new Error(`${route} Run B hit-set mismatch`);
      if (routes.get(route).run_b.control_true_negatives !== 4) throw new Error(`${route} Run B control mismatch`);
    }
    const opus = routes.get("claude-opus-5-medium-no-advisor")?.run_b_route_metadata;
    if (JSON.stringify(opus?.initialized_models) !== JSON.stringify(["claude-opus-5"]) || JSON.stringify(opus?.actual_assistant_models) !== JSON.stringify(["claude-opus-5"])) throw new Error("Opus runtime identity mismatch");
    if (opus.fallback_event_count !== 0 || opus.fallback_block_count !== 0) throw new Error("Opus fallback detected");
    const glm = routes.get("pi-zai-cn-glm-5.3-flash-high")?.run_b_route_metadata;
    if (glm?.actual_provider !== "zai-standard-cn" || glm?.actual_model !== "glm-5.3-flash") throw new Error("GLM runtime route mismatch");
    const expectedFlips = [
      {route: "agy-gemini-3.7-flash-high", revision_id: "R007", from_detected: false, to_detected: true, direction: "miss_to_hit", from_verdict: "OK", to_verdict: "FINDING"},
      {route: "agy-gemini-3.7-flash-high", revision_id: "R008", from_detected: false, to_detected: true, direction: "miss_to_hit", from_verdict: "OK", to_verdict: "FINDING"}
    ];
    if (result.primary_comparison.agreements !== 14 || result.primary_comparison.route_mutation_comparisons !== 16 || JSON.stringify(result.primary_comparison.flips) !== JSON.stringify(expectedFlips)) throw new Error("A/B primary comparison mismatch");
    if (!result.preregistered_stop_rule.triggered || result.preregistered_stop_rule.decision !== "recommend_one_more_byte-identical_run_c") throw new Error("preregistered stop-rule decision mismatch");
  } finally { fs.rmSync(temporary, {recursive: true, force: true}); }
  process.stdout.write("verified exact Run A byte reuse, Run B route artifacts and byte-identical RESULT rebuild\n");
} else process.stdout.write("verified exact Run A input/prompt/schema/reference reuse and blinding before inference\n");
