#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const routes = ["codex-gpt-5.6-sol-high", "claude-opus-5-high-exploratory", "pi-zai-cn-glm-5.3-flash-high", "agy-gemini-3.7-flash-high"];
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const readJson = name => JSON.parse(fs.readFileSync(path.join(directory, name), "utf8"));
const candidateNames = routes.flatMap(route => ["A", "B"].flatMap(arm => [1, 2].map(run => `CANDIDATE-${route}-${arm}${run}.json`)));
const candidates = candidateNames.map(name => {
  const bytes = fs.readFileSync(path.join(directory, name));
  const candidate = JSON.parse(bytes.toString("utf8"));
  if (!candidate.valid) throw new Error(`${name}: candidate invalid`);
  return {name, bytes, candidate};
});
const reference = readJson("REFERENCE.json");
const referenceById = new Map(reference.items.map(item => [item.item_id, item]));
const adjudication = readJson("ATOM-ADJUDICATION.json");
const expectedBindings = candidates.map(({name, bytes}) => ({file: name, sha256: sha256(bytes), size_bytes: bytes.length}));
if (JSON.stringify(adjudication.candidate_hashes) !== JSON.stringify(expectedBindings)) throw new Error("atom adjudication candidate bindings mismatch");
if (!Array.isArray(adjudication.items) || adjudication.items.length !== 224) throw new Error("atom adjudication item count mismatch");
const decisionByKey = new Map();
for (const decision of adjudication.items) {
  const key = `${decision.route}\0${decision.arm}\0${decision.run}\0${decision.item_id}`;
  if (decisionByKey.has(key)) throw new Error(`duplicate adjudication ${key}`);
  const truth = referenceById.get(decision.item_id);
  if (!truth || decision.truth_class !== truth.truth_class || decision.lead_verified !== true) throw new Error(`${key}: adjudication truth binding mismatch`);
  if (["CONTEXT_DEFECT", "SURFACE_DEFECT"].includes(truth.truth_class) && typeof decision.atom_hit !== "boolean") throw new Error(`${key}: defect atom decision missing`);
  if (truth.truth_class.endsWith("CLEAN") && decision.atom_hit !== null) throw new Error(`${key}: clean atom_hit must be null`);
  if (decision.model_verdict !== "FINDING" && decision.atom_hit === true) throw new Error(`${key}: non-FINDING cannot hit atom`);
  decisionByKey.set(key, decision);
}

const runMetrics = [];
for (const {candidate} of candidates) {
  const items = candidate.response.items.map(modelItem => {
    const truth = referenceById.get(modelItem.item_id);
    const key = `${candidate.route}\0${candidate.arm}\0${candidate.run}\0${modelItem.item_id}`;
    const decision = decisionByKey.get(key);
    if (!truth || !decision || decision.model_verdict !== modelItem.verdict) throw new Error(`${key}: model/adjudication mismatch`);
    return {modelItem, truth, decision};
  });
  const inClass = truthClass => items.filter(item => item.truth.truth_class === truthClass);
  const defects = items.filter(item => item.truth.truth_class.endsWith("DEFECT"));
  const clean = items.filter(item => item.truth.truth_class.endsWith("CLEAN"));
  runMetrics.push({
    route: candidate.route,
    arm: candidate.arm,
    run: candidate.run,
    valid: true,
    context_defect_atom_hits: inClass("CONTEXT_DEFECT").filter(item => item.decision.atom_hit).length,
    context_defect_total: inClass("CONTEXT_DEFECT").length,
    surface_defect_atom_hits: inClass("SURFACE_DEFECT").filter(item => item.decision.atom_hit).length,
    surface_defect_total: inClass("SURFACE_DEFECT").length,
    all_defect_atom_hits: defects.filter(item => item.decision.atom_hit).length,
    all_defect_total: defects.length,
    context_exonerated_false_positives: inClass("CONTEXT_EXONERATED_CLEAN").filter(item => item.modelItem.verdict === "FINDING").length,
    context_exonerated_total: inClass("CONTEXT_EXONERATED_CLEAN").length,
    ordinary_clean_false_positives: inClass("ORDINARY_CLEAN").filter(item => item.modelItem.verdict === "FINDING").length,
    ordinary_clean_total: inClass("ORDINARY_CLEAN").length,
    all_clean_false_positives: clean.filter(item => item.modelItem.verdict === "FINDING").length,
    all_clean_total: clean.length,
    uncertain: items.filter(item => item.modelItem.verdict === "UNCERTAIN").length
  });
}

const routeSummaries = routes.map(route => {
  const runs = runMetrics.filter(item => item.route === route);
  const arm = name => runs.filter(item => item.arm === name);
  const sum = (values, field) => values.reduce((total, item) => total + item[field], 0);
  const paired = [1, 2].map(run => {
    const a = runs.find(item => item.arm === "A" && item.run === run);
    const b = runs.find(item => item.arm === "B" && item.run === run);
    return {
      run,
      context_defect_atom_delta_B_minus_A: b.context_defect_atom_hits - a.context_defect_atom_hits,
      surface_defect_atom_delta_B_minus_A: b.surface_defect_atom_hits - a.surface_defect_atom_hits,
      context_exonerated_fp_delta_B_minus_A: b.context_exonerated_false_positives - a.context_exonerated_false_positives,
      all_clean_fp_delta_B_minus_A: b.all_clean_false_positives - a.all_clean_false_positives
    };
  });
  return {
    route,
    arm_A: {
      context_defect_atom_hits: sum(arm("A"), "context_defect_atom_hits"), context_defect_opportunities: 2,
      surface_defect_atom_hits: sum(arm("A"), "surface_defect_atom_hits"), surface_defect_opportunities: 10,
      context_exonerated_false_positives: sum(arm("A"), "context_exonerated_false_positives"), context_exonerated_opportunities: 8,
      all_clean_false_positives: sum(arm("A"), "all_clean_false_positives"), all_clean_opportunities: 16
    },
    arm_B: {
      context_defect_atom_hits: sum(arm("B"), "context_defect_atom_hits"), context_defect_opportunities: 2,
      surface_defect_atom_hits: sum(arm("B"), "surface_defect_atom_hits"), surface_defect_opportunities: 10,
      context_exonerated_false_positives: sum(arm("B"), "context_exonerated_false_positives"), context_exonerated_opportunities: 8,
      all_clean_false_positives: sum(arm("B"), "all_clean_false_positives"), all_clean_opportunities: 16
    },
    paired_deltas: paired
  };
});

const result = {
  schema_version: "source-context-exploratory-four-route-result-v1",
  experiment: "source-context-exploratory-four-route-v1",
  status: "EXPLORATORY_COMPLETE_NOT_FORMAL",
  valid_runs: runMetrics.filter(item => item.valid).length,
  expected_runs: 16,
  run_metrics: runMetrics,
  route_summaries: routeSummaries,
  interpretation_guardrails: [
    "Only one context-dependent defect is present; context-hit counts are repeated observations of one case, not population recall.",
    "The set is deliberately case-enriched and cannot rank general translation quality.",
    "Claude is an exploratory comparator whose formal purity qualification remains NO-GO.",
    "Gemini runtime identity remains limited if the Antigravity envelope does not report it.",
    "This result cannot replace or modify prospective-source-context-truth-audit-v1/RESULT.json."
  ],
  bindings: {
    reference_sha256: sha256(fs.readFileSync(path.join(directory, "REFERENCE.json"))),
    atom_adjudication_sha256: sha256(fs.readFileSync(path.join(directory, "ATOM-ADJUDICATION.json"))),
    candidates: expectedBindings
  }
};
fs.writeFileSync(path.join(directory, "RESULT.json"), `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: result.status, valid_runs: result.valid_runs, route_summaries: result.route_summaries}, null, 2)}\n`);
