import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const runA = path.join(here, "../controlled-mutation-ui-log-replication-v2");
const runB = path.join(here, "../controlled-mutation-ui-log-repeat-b");
const outIndex = process.argv.indexOf("--out");
if (outIndex !== -1 && !process.argv[outIndex + 1]) throw new Error("--out requires a path");
const outputPath = outIndex === -1 ? path.join(here, "RESULT.json") : path.resolve(process.argv[outIndex + 1]);
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const read = file => JSON.parse(fs.readFileSync(file, "utf8"));
const local = file => path.join(here, file);

const experiment = read(local("EXPERIMENT.json"));
const reference = read(path.join(runA, "REFERENCE.json"));
const runDirectories = {A: runA, B: runB, C: here};
const adjudications = {
  A: read(path.join(runA, "ADJUDICATION.json")),
  B: read(path.join(runB, "ADJUDICATION.json")),
  C: read(local("ADJUDICATION.json"))
};
const runLabels = ["A", "B", "C"];

for (const [label, prior] of [["A", experiment.run_a], ["B", experiment.run_b]]) {
  if (sha256(path.join(runDirectories[label], "RESULT.json")) !== prior.result_sha256) throw new Error(`Run ${label} result hash mismatch`);
  if (sha256(path.join(runDirectories[label], "ADJUDICATION.json")) !== prior.adjudication_sha256) throw new Error(`Run ${label} adjudication hash mismatch`);
}

const routeFiles = {
  "codex-gpt-5.6-sol-high": {
    candidate: "CANDIDATE-codex-gpt-5.6-sol-high.json",
    candidate_sha256: "0ddfe928dfeb3df4d9d31ce796ca8f281fca26998c3391a6f6f1854ff678bb2a",
    raw: "RAW-codex-gpt-5.6-sol-high.json",
    raw_sha256: "c775c1b559d0c59e3419ee9c52f2076eed85c3d09f7a44095e26112e9de7d655",
    stderr: "RAW-codex-gpt-5.6-sol-high.stderr.txt",
    stderr_sha256: "1b1d2d7ce0b144018cc32a81a83753b4ac8085d260868f927468dc1eed184f1b"
  },
  "claude-opus-5-medium-no-advisor": {
    candidate: "CANDIDATE-claude-opus-5-medium-no-advisor.json",
    candidate_sha256: "6a7f8c8f2d3ab59cfd329230be243a7f8e1ec26e77dbc182e11bda4a697343f6",
    raw: "RAW-claude-opus-5-medium-no-advisor.json",
    raw_sha256: "1d5aa99a9f06b167a37e01564d988293922f903a1c1468712cc04c9b9cc9858b"
  },
  "pi-zai-cn-glm-5.3-flash-high": {
    candidate: "CANDIDATE-pi-zai-cn-glm-5.3-flash-high.json",
    candidate_sha256: "eb3f964115b7d4f6a4df2b0462876c2a6df2124d25f5474f675d6981b59ccb2b",
    raw: "RAW-pi-zai-cn-glm-5.3-flash-high.json",
    raw_sha256: "5049384475419266e6947779510c1612eb90882a8146f5280a9c5e2d98531376",
    stderr: "RAW-pi-zai-cn-glm-5.3-flash-high.stderr.txt",
    stderr_sha256: "9140ca4aa8d7e64e281509a2d2db869e878ff6e9fe0e032a28819ea02d3f57f1"
  },
  "agy-gemini-3.7-flash-high": {
    candidate: "CANDIDATE-agy-gemini-3.7-flash-high.json",
    candidate_sha256: "3a12f227ff4edb6a0a771c9214bf5766248bdb954df506942bcd9f1325e8d68f",
    raw: "RAW-agy-gemini-3.7-flash-high.json",
    raw_sha256: "f179c736636efce8401208696ab399bbbf030aeec55ef1a2e4b5b2c5e8fdfef4",
    stderr: "RAW-agy-gemini-3.7-flash-high.stderr.txt",
    stderr_sha256: "3a7f8550106d86abb322e8ed0fb30a0296c0e97c6be03d5a8033b99d16737459"
  }
};

const mutationIds = reference.items.filter(item => item.label === "INJECTED_MUTATION").map(item => item.revision_id);
const controlIds = reference.items.filter(item => item.label === "SOURCE_VERIFIED_CONTROL").map(item => item.revision_id);
const ordered = (ids, universe) => universe.filter(id => ids.includes(id));
const pairDefinitions = [["A", "B"], ["B", "C"], ["A", "C"]];
const pairKey = (from, to) => `${from.toLowerCase()}_to_${to.toLowerCase()}`;
const routes = [];

for (const [route, files] of Object.entries(routeFiles)) {
  for (const kind of ["candidate", "raw", ...(files.stderr ? ["stderr"] : [])]) {
    if (sha256(local(files[kind])) !== files[`${kind}_sha256`]) throw new Error(`${route} Run C ${kind} hash mismatch`);
  }
  if (sha256(path.join(runA, files.candidate)) !== experiment.run_a.candidate_sha256[route]) throw new Error(`${route} Run A candidate hash mismatch`);
  if (sha256(path.join(runB, files.candidate)) !== experiment.run_b.candidate_sha256[route]) throw new Error(`${route} Run B candidate hash mismatch`);

  const candidates = Object.fromEntries(runLabels.map(label => [label, read(path.join(runDirectories[label], files.candidate))]));
  for (const label of runLabels) {
    const candidate = candidates[label];
    if (!candidate.valid || candidate.route !== route) throw new Error(`${route} Run ${label} candidate validity/identity mismatch`);
    if (label !== "A" && candidate.run_label !== label) throw new Error(`${route} Run ${label} label mismatch`);
  }
  const byId = Object.fromEntries(runLabels.map(label => [label, new Map(candidates[label].response.revisions.map(item => [item.revision_id, item]))]));
  const hits = Object.fromEntries(runLabels.map(label => [label, ordered(adjudications[label].mutation_claim_matches[route], mutationIds)]));
  const controls = Object.fromEntries(runLabels.map(label => [label, controlIds.filter(id => byId[label].get(id)?.verdict !== "OK")]));

  for (const label of runLabels) {
    for (const id of hits[label]) if (byId[label].get(id)?.verdict === "OK") throw new Error(`${route} Run ${label} ${id} matching claim is OK`);
    const misses = mutationIds.filter(id => !hits[label].includes(id));
    const recordedMisses = ordered((adjudications[label].mutation_misses[route] ?? []).map(item => item.revision_id), mutationIds);
    if (JSON.stringify(misses) !== JSON.stringify(recordedMisses)) throw new Error(`${route} Run ${label} mutation miss adjudication mismatch`);
    if (JSON.stringify(controls[label]) !== JSON.stringify(adjudications[label].control_candidates[route])) throw new Error(`${route} Run ${label} control adjudication mismatch`);
  }

  const summary = label => {
    const findingHits = hits[label].filter(id => byId[label].get(id).verdict === "FINDING");
    const uncertainHits = hits[label].filter(id => byId[label].get(id).verdict === "UNCERTAIN");
    const sourceRefuted = (adjudications[label].source_refuted_control_candidates?.[route] ?? []).map(item => item.revision_id);
    return {
      mutation_hits: hits[label].length,
      mutation_total: mutationIds.length,
      mutation_recall: hits[label].length / mutationIds.length,
      hit_revision_ids: hits[label],
      finding_only_hits: findingHits.length,
      finding_only_revision_ids: findingHits,
      uncertain_match_revision_ids: uncertainHits,
      control_true_negatives: controlIds.length - controls[label].length,
      control_total: controlIds.length,
      control_specificity: (controlIds.length - controls[label].length) / controlIds.length,
      control_candidate_revision_ids: controls[label],
      source_refuted_control_candidate_revision_ids: sourceRefuted
    };
  };
  const runSummaries = Object.fromEntries(runLabels.map(label => [label, summary(label)]));

  const pairwise = {};
  for (const [from, to] of pairDefinitions) {
    const primaryFlips = mutationIds.flatMap(id => {
      const fromDetected = hits[from].includes(id);
      const toDetected = hits[to].includes(id);
      return fromDetected === toDetected ? [] : [{
        revision_id: id,
        from_detected: fromDetected,
        to_detected: toDetected,
        direction: fromDetected ? "hit_to_miss" : "miss_to_hit",
        from_verdict: byId[from].get(id).verdict,
        to_verdict: byId[to].get(id).verdict
      }];
    });
    const verdictFlips = mutationIds.flatMap(id => byId[from].get(id).verdict === byId[to].get(id).verdict ? [] : [{revision_id: id, from: byId[from].get(id).verdict, to: byId[to].get(id).verdict}]);
    pairwise[pairKey(from, to)] = {
      primary_agreements: mutationIds.length - primaryFlips.length,
      primary_total: mutationIds.length,
      primary_agreement_rate: (mutationIds.length - primaryFlips.length) / mutationIds.length,
      primary_flips: primaryFlips,
      mutation_verdict_flips: verdictFlips,
      control_candidate_changes: controlIds.filter(id => controls[from].includes(id) !== controls[to].includes(id))
    };
  }

  const byMutation = Object.fromEntries(mutationIds.map(id => {
    const detectedRuns = runLabels.filter(label => hits[label].includes(id));
    return [id, {detections: detectedRuns.length, runs: runLabels.length, frequency: detectedRuns.length / runLabels.length, detected_runs: detectedRuns}];
  }));
  const detectionTotal = Object.values(byMutation).reduce((sum, record) => sum + record.detections, 0);
  routes.push({
    route,
    run_c_artifacts: {
      candidate: files.candidate,
      candidate_sha256: files.candidate_sha256,
      raw: files.raw,
      raw_sha256: files.raw_sha256,
      ...(files.stderr ? {stderr: files.stderr, stderr_sha256: files.stderr_sha256} : {})
    },
    run_c_route_metadata: candidates.C.route_metadata,
    runs: runSummaries,
    three_run_detection: {
      detections: detectionTotal,
      opportunities: mutationIds.length * runLabels.length,
      rate: detectionTotal / (mutationIds.length * runLabels.length),
      by_mutation: byMutation,
      union_revision_ids: mutationIds.filter(id => runLabels.some(label => hits[label].includes(id))),
      intersection_revision_ids: mutationIds.filter(id => runLabels.every(label => hits[label].includes(id)))
    },
    pairwise_comparisons: pairwise
  });
}

const globalPairwise = {};
for (const [from, to] of pairDefinitions) {
  const key = pairKey(from, to);
  const flips = routes.flatMap(route => route.pairwise_comparisons[key].primary_flips.map(flip => ({route: route.route, ...flip})));
  const verdictFlips = routes.flatMap(route => route.pairwise_comparisons[key].mutation_verdict_flips.map(flip => ({route: route.route, ...flip})));
  const controlChanges = routes.flatMap(route => route.pairwise_comparisons[key].control_candidate_changes.map(revisionId => ({route: route.route, revision_id: revisionId})));
  const total = routes.length * mutationIds.length;
  globalPairwise[key] = {route_mutation_comparisons: total, agreements: total - flips.length, agreement_rate: (total - flips.length) / total, primary_flips: flips, mutation_verdict_flips: verdictFlips, control_candidate_changes: controlChanges};
}

const runCHitSets = routes.map(route => new Set(route.runs.C.hit_revision_ids));
const mutationThreeRunFrequency = Object.fromEntries(mutationIds.map(id => {
  const detections = routes.reduce((sum, route) => sum + route.three_run_detection.by_mutation[id].detections, 0);
  return [id, {detections, opportunities: routes.length * runLabels.length, frequency: detections / (routes.length * runLabels.length)}];
}));
const controlCandidates = routes.flatMap(route => runLabels.flatMap(label => route.runs[label].control_candidate_revision_ids.map(revisionId => ({run: label, route: route.route, revision_id: revisionId, source_refuted: route.runs[label].source_refuted_control_candidate_revision_ids.includes(revisionId)}))));

const result = {
  schema_version: 1,
  experiment: "controlled-mutation-ui-log-repeat-c",
  status: "COMPLETE",
  scored_at: "2026-08-27",
  run_a_commit: "09aaaab",
  run_b_frozen_commit: "b299a27",
  run_c_frozen_commit: "4d1e592",
  authorization_record_commit: "d412172",
  frozen_input_sha256: experiment.frozen_bytes.input.sha256,
  frozen_prompt_sha256: experiment.frozen_bytes.prompt.sha256,
  frozen_schema_sha256: experiment.frozen_bytes.schema.sha256,
  sealed_reference_sha256: experiment.frozen_bytes.reference.sha256,
  source_verification_sha256: experiment.frozen_bytes.source_verification.sha256,
  run_a_result_sha256: experiment.run_a.result_sha256,
  run_a_adjudication_sha256: experiment.run_a.adjudication_sha256,
  run_b_result_sha256: experiment.run_b.result_sha256,
  run_b_adjudication_sha256: experiment.run_b.adjudication_sha256,
  run_c_adjudication_sha256: sha256(local("ADJUDICATION.json")),
  design: {
    byte_identical_across_runs: true,
    item_order_identical: true,
    prompt_and_schema_identical: true,
    routes_and_effort_identical: true,
    independent_runs: true,
    route_output_exchange: false,
    injected_mutations: mutationIds.length,
    source_verified_controls: controlIds.length,
    completed_runs: runLabels.length
  },
  routes,
  pairwise_primary_comparisons: globalPairwise,
  three_run_derived: {
    mutation_detection_frequency_across_all_route_runs: mutationThreeRunFrequency,
    control_candidate_occurrences: controlCandidates,
    control_candidate_opportunities: routes.length * controlIds.length * runLabels.length,
    source_refuted_control_candidates: controlCandidates.filter(item => item.source_refuted).length
  },
  run_c_derived: {
    mutation_union: {hits: mutationIds.filter(id => runCHitSets.some(set => set.has(id))).length, total: mutationIds.length, revision_ids: mutationIds.filter(id => runCHitSets.some(set => set.has(id)))},
    four_route_consensus: {hits: mutationIds.filter(id => runCHitSets.every(set => set.has(id))).length, total: mutationIds.length, revision_ids: mutationIds.filter(id => runCHitSets.every(set => set.has(id)))},
    support_count_by_mutation: Object.fromEntries(mutationIds.map(id => [id, runCHitSets.filter(set => set.has(id)).length]))
  },
  preregistered_completion_rule: {
    rule: experiment.preregistered_analysis.completion_rule,
    satisfied: true,
    decision: "stop_repeated_inference_under_this_design"
  },
  interpretation: [
    "Codex detected all four mutations in all three runs (12/12 route-mutation-run opportunities). Opus detected 8/12, GLM 10/12 and Gemini 10/12; these descriptive totals are not a population ranking.",
    "R001 and R005 were detected in all 12 route-runs. R007 was detected in 6/12 and R008 in 10/12, showing that the two harder UI/runtime mutations drive the observed instability.",
    "Between Runs B and C, Opus changed R008 from a correct UNCERTAIN to OK, while GLM changed R007 from OK to FINDING. Gemini retained its Run B R007/R008 hits in Run C.",
    "Gemini raised R003 only in Run C. Direct source verification refutes that control claim: an existing EFF_PSI_DAMAGE_SHIELD is active by definition, and the target preserves the required boolean grouping. This is the only control candidate across 48 route-control-run opportunities.",
    "Claude's Run C assistant review messages all report claude-opus-5 with zero fallback events or blocks; aggregate modelUsage still contains a small Haiku auxiliary charge. agy still omits runtime model identity from its envelope."
  ],
  limitations: [
    "Three runs over four heterogeneous mutations provide direct per-item frequencies but no reliable confidence interval or population-level model ranking.",
    "The route-run observations may not be independent because service-side model revisions and sampling controls are not fully exposed.",
    "The benchmark covers objective UI/log mechanism claims and does not measure prose quality, translation-origin preference or natural residual-defect prevalence.",
    "Runtime model identity for agy remains unverified because the CLI envelope reports neither model nor agent."
  ],
  next_step: "Stop repeated inference for this eight-item design. Any further variance study, larger sample or reviewer-by-origin comparison should be a newly preregistered experiment with fresh frozen inputs."
};

fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({routes: routes.map(route => ({route: route.route, run_hits: Object.fromEntries(runLabels.map(label => [label, route.runs[label].mutation_hits])), three_run_detections: route.three_run_detection.detections, controls: Object.fromEntries(runLabels.map(label => [label, route.runs[label].control_candidate_revision_ids]))})), pairwise: globalPairwise, completion: result.preregistered_completion_rule}, null, 2)}\n`);
