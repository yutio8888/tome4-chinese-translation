#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const bytes = name => fs.readFileSync(path.join(directory, name));
const json = name => JSON.parse(bytes(name).toString("utf8"));
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const experiment = json("EXPERIMENT.json");
const amendment = json("ANALYSIS-AMENDMENT.json");
const reference = json("REFERENCE.json");
const referenceById = new Map(reference.items.map(item => [item.item_id, item]));
const routes = [
  "codex-gpt-5.6-sol-high",
  "claude-opus-5-high-exploratory",
  "pi-zai-cn-glm-5.3-flash-high",
  "agy-gemini-3.7-flash-high"
];
const candidateNames = routes.flatMap(route => ["A", "B"].flatMap(arm => [1, 2].map(run => `CANDIDATE-${route}-${arm}${run}.json`)));

for (const [name, expected] of Object.entries(experiment.frozen_hashes)) {
  if (["run.mjs", "score.mjs"].includes(name)) continue;
  assert(sha256(bytes(name)) === expected, `${name}: frozen hash mismatch`);
}
assert(sha256(bytes("run.mjs")) === amendment.amendments[0].amended_run_sha256, "run.mjs: amended hash mismatch");
assert(sha256(bytes("score.mjs")) === amendment.amendments[1].amended_score_sha256, "score.mjs: amended hash mismatch");
assert(sha256(bytes("ANALYSIS-AMENDMENT.json")) === experiment.execution_outcome.analysis_amendment.sha256, "analysis amendment hash mismatch");

let strictValid = 0;
let recoveryNormalized = 0;
const expectedBindings = [];
for (const name of candidateNames) {
  const candidateBytes = bytes(name);
  const candidate = JSON.parse(candidateBytes.toString("utf8"));
  const acquisitionBytes = bytes(candidate.acquisition.file);
  const acquisition = JSON.parse(acquisitionBytes.toString("utf8"));
  assert(candidate.acquisition.sha256 === sha256(acquisitionBytes), `${name}: acquisition binding mismatch`);
  assert(acquisition.route === candidate.route && acquisition.arm === candidate.arm && acquisition.run === candidate.run, `${name}: acquisition identity mismatch`);
  const rawStem = name.slice("CANDIDATE-".length, -".json".length);
  assert(acquisition.raw_stdout.sha256 === sha256(bytes(`RAW-${rawStem}.stdout.txt`)), `${name}: RAW stdout mismatch`);
  assert(acquisition.raw_stderr.sha256 === sha256(bytes(`RAW-${rawStem}.stderr.txt`)), `${name}: RAW stderr mismatch`);
  if (candidate.route.startsWith("codex-")) assert(acquisition.codex_last_message.sha256 === sha256(bytes(`RAW-${rawStem}.last-message.json`)), `${name}: Codex last-message mismatch`);
  const scoringItems = candidate.response?.items ?? candidate.response?.verdicts;
  assert(Array.isArray(scoringItems) && scoringItems.length === 14, `${name}: missing 14 scoring items`);
  assert(scoringItems.every((item, index) => item.item_id === `E${String(index + 1).padStart(3, "0")}`), `${name}: item order mismatch`);
  if (candidate.valid) strictValid += 1;
  else {
    assert(candidate.route === "pi-zai-cn-glm-5.3-flash-high" && Object.keys(candidate.response).length === 1 && Array.isArray(candidate.response.verdicts), `${name}: unexpected invalid candidate`);
    recoveryNormalized += 1;
  }
  expectedBindings.push({file: name, sha256: sha256(candidateBytes), size_bytes: candidateBytes.length});
}
assert(strictValid === 14 && recoveryNormalized === 2, "candidate validity counts mismatch");

const adjudication = json("ATOM-ADJUDICATION.json");
assert(JSON.stringify(adjudication.candidate_hashes) === JSON.stringify(expectedBindings), "atom candidate bindings mismatch");
assert(adjudication.items.length === 224 && adjudication.items.every(item => item.lead_verified === true), "atom adjudication completeness mismatch");
for (const item of adjudication.items) {
  const truth = referenceById.get(item.item_id);
  assert(truth?.truth_class === item.truth_class, `atom truth mismatch ${item.route}/${item.arm}${item.run}/${item.item_id}`);
  assert(truth.truth_class.endsWith("CLEAN") ? item.atom_hit === null : typeof item.atom_hit === "boolean", `atom type mismatch ${item.route}/${item.arm}${item.run}/${item.item_id}`);
}

const result = json("RESULT.json");
assert(result.strict_valid_runs === 14 && result.recovery_normalized_runs === 2 && result.reference_scored_runs === 16, "result run counts mismatch");
assert(result.bindings.reference_sha256 === sha256(bytes("REFERENCE.json")), "result reference binding mismatch");
assert(result.bindings.atom_adjudication_sha256 === sha256(bytes("ATOM-ADJUDICATION.json")), "result atom binding mismatch");
assert(JSON.stringify(result.bindings.candidates) === JSON.stringify(expectedBindings), "result candidate bindings mismatch");
assert(experiment.result_bindings["ATOM-ADJUDICATION.json"] === sha256(bytes("ATOM-ADJUDICATION.json")), "experiment atom result hash mismatch");
assert(experiment.result_bindings["RESULT.json"] === sha256(bytes("RESULT.json")), "experiment result hash mismatch");

const executorFixture = path.join(directory, "..", "qwen3-8-27b-agent-roles", "executor-fixture.lua");
assert(sha256(fs.readFileSync(executorFixture)) === "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7", "executor fixture baseline mismatch");
process.stdout.write(`${JSON.stringify({status: "PASS", candidates: candidateNames.length, strict_valid: strictValid, recovery_normalized: recoveryNormalized, reference_scored: result.reference_scored_runs, atom_decisions: adjudication.items.length}, null, 2)}\n`);
