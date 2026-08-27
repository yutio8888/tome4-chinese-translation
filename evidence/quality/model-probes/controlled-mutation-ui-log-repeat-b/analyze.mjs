import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const runA = path.join(here, "../controlled-mutation-ui-log-replication-v2");
const outIndex = process.argv.indexOf("--out");
if (outIndex !== -1 && !process.argv[outIndex + 1]) throw new Error("--out requires a path");
const outputPath = outIndex === -1 ? path.join(here, "RESULT.json") : path.resolve(process.argv[outIndex + 1]);
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const read = file => JSON.parse(fs.readFileSync(file, "utf8"));
const local = file => path.join(here, file);
const prior = file => path.join(runA, file);
const experiment = read(local("EXPERIMENT.json"));
const reference = read(prior("REFERENCE.json"));
const adjudicationA = read(prior("ADJUDICATION.json"));
const adjudicationB = read(local("ADJUDICATION.json"));
const expectedA = {
  result: "776927907103f41947006b045da420cd1b8209cab91d0c1b2e98859631fe2776",
  adjudication: "bdb13bdc19f884736b438b175eedaf48ef0aaf6ec3b2be378191bfea4d0a1870"
};
if (sha256(prior("RESULT.json")) !== expectedA.result || sha256(prior("ADJUDICATION.json")) !== expectedA.adjudication) throw new Error("Run A result/adjudication hash mismatch");
const routeFiles = {
  "codex-gpt-5.6-sol-high": {
    candidate: "CANDIDATE-codex-gpt-5.6-sol-high.json",
    candidate_sha256: "dd4a416ff8633373bc2c6f6e3b8c92da4d25913818ac92cd39086d5b324d83ac",
    raw: "RAW-codex-gpt-5.6-sol-high.json",
    raw_sha256: "a002babdd4d1bbb2cc42444cc9afab4a31686fd917e91edafd0469f4811885e2",
    stderr: "RAW-codex-gpt-5.6-sol-high.stderr.txt",
    stderr_sha256: "aea51706f039e16bc5e32f07ef2630755c2b95bda1b28be2005dc41474a10cc4"
  },
  "claude-opus-5-medium-no-advisor": {
    candidate: "CANDIDATE-claude-opus-5-medium-no-advisor.json",
    candidate_sha256: "4fef692dc1c85f91bda6998036bf009bbe5bab1816f12bbee993693da2fb0681",
    raw: "RAW-claude-opus-5-medium-no-advisor.json",
    raw_sha256: "e881cbb83ee808cb91e079fc2fa2be9ca511affe86d0fcb221a96bb5d114908b"
  },
  "pi-zai-cn-glm-5.3-flash-high": {
    candidate: "CANDIDATE-pi-zai-cn-glm-5.3-flash-high.json",
    candidate_sha256: "e3305de0ec7fd05255c3c0f31cc2d07b57e73fe979acb2c810ab59e2a7908365",
    raw: "RAW-pi-zai-cn-glm-5.3-flash-high.json",
    raw_sha256: "4bfc7a648dffe6374431b75340f4ef4e23d71205d6cf1ea5afbe49eed5611bc3",
    stderr: "RAW-pi-zai-cn-glm-5.3-flash-high.stderr.txt",
    stderr_sha256: "9140ca4aa8d7e64e281509a2d2db869e878ff6e9fe0e032a28819ea02d3f57f1"
  },
  "agy-gemini-3.7-flash-high": {
    candidate: "CANDIDATE-agy-gemini-3.7-flash-high.json",
    candidate_sha256: "29d4638bcf42743efff8ee898e950ebff049e2c3e8e7ca7b661658831dfc5f25",
    raw: "RAW-agy-gemini-3.7-flash-high.json",
    raw_sha256: "778d56c12a835a68d3f7be2db1b1506f1cfcfb27d3f945e7e155d45aab3371ab",
    stderr: "RAW-agy-gemini-3.7-flash-high.stderr.txt",
    stderr_sha256: "3a7f8550106d86abb322e8ed0fb30a0296c0e97c6be03d5a8033b99d16737459"
  }
};
const mutationIds = reference.items.filter(item => item.label === "INJECTED_MUTATION").map(item => item.revision_id);
const controlIds = reference.items.filter(item => item.label === "SOURCE_VERIFIED_CONTROL").map(item => item.revision_id);
const ordered = (ids, universe) => universe.filter(id => ids.includes(id));
const routes = [];
const allPrimaryFlips = [];
const allVerdictFlips = [];
for (const [route, files] of Object.entries(routeFiles)) {
  for (const kind of ["candidate", "raw", ...(files.stderr ? ["stderr"] : [])]) {
    if (sha256(local(files[kind])) !== files[`${kind}_sha256`]) throw new Error(`${route} Run B ${kind} hash mismatch`);
  }
  if (sha256(prior(files.candidate)) !== experiment.run_a.candidate_sha256[route]) throw new Error(`${route} Run A candidate hash mismatch`);
  const candidateA = read(prior(files.candidate));
  const candidateB = read(local(files.candidate));
  if (!candidateA.valid || candidateA.route !== route) throw new Error(`${route} Run A candidate validity/identity mismatch`);
  if (!candidateB.valid || candidateB.route !== route || candidateB.run_label !== "B") throw new Error(`${route} Run B candidate validity/identity mismatch`);
  const byIdA = new Map(candidateA.response.revisions.map(item => [item.revision_id, item]));
  const byIdB = new Map(candidateB.response.revisions.map(item => [item.revision_id, item]));
  const hitsA = ordered(adjudicationA.mutation_claim_matches[route], mutationIds);
  const hitsB = ordered(adjudicationB.mutation_claim_matches[route], mutationIds);
  for (const [label, hits, byId] of [["A", hitsA, byIdA], ["B", hitsB, byIdB]]) {
    for (const id of hits) if (byId.get(id)?.verdict === "OK") throw new Error(`${route} Run ${label} ${id} matching claim is OK`);
  }
  const controlsA = controlIds.filter(id => byIdA.get(id)?.verdict !== "OK");
  const controlsB = controlIds.filter(id => byIdB.get(id)?.verdict !== "OK");
  if (JSON.stringify(controlsA) !== JSON.stringify(adjudicationA.control_candidates[route])) throw new Error(`${route} Run A control adjudication mismatch`);
  if (JSON.stringify(controlsB) !== JSON.stringify(adjudicationB.control_candidates[route])) throw new Error(`${route} Run B control adjudication mismatch`);
  const primaryFlips = mutationIds.flatMap(id => {
    const fromDetected = hitsA.includes(id);
    const toDetected = hitsB.includes(id);
    return fromDetected === toDetected ? [] : [{revision_id: id, from_detected: fromDetected, to_detected: toDetected, direction: fromDetected ? "hit_to_miss" : "miss_to_hit", from_verdict: byIdA.get(id).verdict, to_verdict: byIdB.get(id).verdict}];
  });
  const verdictFlips = mutationIds.flatMap(id => byIdA.get(id).verdict === byIdB.get(id).verdict ? [] : [{revision_id: id, from: byIdA.get(id).verdict, to: byIdB.get(id).verdict}]);
  allPrimaryFlips.push(...primaryFlips.map(flip => ({route, ...flip})));
  allVerdictFlips.push(...verdictFlips.map(flip => ({route, ...flip})));
  const findingHits = (hits, byId) => hits.filter(id => byId.get(id).verdict === "FINDING");
  const uncertainHits = (hits, byId) => hits.filter(id => byId.get(id).verdict === "UNCERTAIN");
  const summary = (hits, controls, byId) => ({
    mutation_hits: hits.length,
    mutation_total: mutationIds.length,
    mutation_recall: hits.length / mutationIds.length,
    hit_revision_ids: hits,
    finding_only_hits: findingHits(hits, byId).length,
    finding_only_revision_ids: findingHits(hits, byId),
    uncertain_match_revision_ids: uncertainHits(hits, byId),
    control_true_negatives: controlIds.length - controls.length,
    control_total: controlIds.length,
    control_specificity: (controlIds.length - controls.length) / controlIds.length,
    control_candidate_revision_ids: controls
  });
  const setA = new Set(hitsA);
  const setB = new Set(hitsB);
  routes.push({
    route,
    run_b_artifacts: {candidate: files.candidate, candidate_sha256: files.candidate_sha256, raw: files.raw, raw_sha256: files.raw_sha256, ...(files.stderr ? {stderr: files.stderr, stderr_sha256: files.stderr_sha256} : {})},
    run_b_route_metadata: candidateB.route_metadata,
    run_a: summary(hitsA, controlsA, byIdA),
    run_b: summary(hitsB, controlsB, byIdB),
    comparison: {
      primary_agreements: mutationIds.length - primaryFlips.length,
      primary_total: mutationIds.length,
      primary_agreement_rate: (mutationIds.length - primaryFlips.length) / mutationIds.length,
      primary_flips: primaryFlips,
      verdict_flips: verdictFlips,
      two_run_union_revision_ids: mutationIds.filter(id => setA.has(id) || setB.has(id)),
      two_run_intersection_revision_ids: mutationIds.filter(id => setA.has(id) && setB.has(id)),
      control_candidate_changes: controlIds.filter(id => controlsA.includes(id) !== controlsB.includes(id))
    }
  });
}
const runBHitSets = routes.map(route => new Set(route.run_b.hit_revision_ids));
const runBUnion = mutationIds.filter(id => runBHitSets.some(set => set.has(id)));
const runBConsensus = mutationIds.filter(id => runBHitSets.every(set => set.has(id)));
const anyControlCandidate = routes.some(route => route.run_b.control_candidate_revision_ids.length > 0);
const stopTriggered = allPrimaryFlips.length > 0 || anyControlCandidate;
const result = {
  schema_version: 1,
  experiment: "controlled-mutation-ui-log-repeat-b",
  status: "COMPLETE",
  scored_at: "2026-08-27",
  run_a_commit: "09aaaab",
  run_b_frozen_commit: "b299a27",
  frozen_input_sha256: experiment.frozen_bytes.input.sha256,
  frozen_prompt_sha256: experiment.frozen_bytes.prompt.sha256,
  frozen_schema_sha256: experiment.frozen_bytes.schema.sha256,
  sealed_reference_sha256: experiment.frozen_bytes.reference.sha256,
  source_verification_sha256: experiment.frozen_bytes.source_verification.sha256,
  run_a_result_sha256: expectedA.result,
  run_a_adjudication_sha256: expectedA.adjudication,
  run_b_adjudication_sha256: sha256(local("ADJUDICATION.json")),
  design: {byte_identical_to_run_a: true, item_order_identical: true, prompt_and_schema_identical: true, routes_and_effort_identical: true, independent_runs: true, route_output_exchange: false, injected_mutations: mutationIds.length, source_verified_controls: controlIds.length},
  routes,
  primary_comparison: {
    route_mutation_comparisons: routes.length * mutationIds.length,
    agreements: routes.length * mutationIds.length - allPrimaryFlips.length,
    agreement_rate: (routes.length * mutationIds.length - allPrimaryFlips.length) / (routes.length * mutationIds.length),
    flips: allPrimaryFlips
  },
  secondary_comparison: {mutation_verdict_flips: allVerdictFlips, control_candidate_in_either_run: routes.filter(route => route.run_a.control_candidate_revision_ids.length || route.run_b.control_candidate_revision_ids.length).map(route => route.route)},
  run_b_derived: {
    mutation_union: {hits: runBUnion.length, total: mutationIds.length, recall: runBUnion.length / mutationIds.length, revision_ids: runBUnion},
    four_route_consensus: {hits: runBConsensus.length, total: mutationIds.length, recall: runBConsensus.length / mutationIds.length, revision_ids: runBConsensus},
    support_count_by_mutation: Object.fromEntries(mutationIds.map(id => [id, runBHitSets.filter(set => set.has(id)).length]))
  },
  preregistered_stop_rule: {
    rule: experiment.preregistered_analysis.stop_rule,
    triggered: stopTriggered,
    trigger_reasons: [...(allPrimaryFlips.length ? [`${allPrimaryFlips.length} primary mutation-detection flips`] : []), ...(anyControlCandidate ? ["at least one Run B source-verified control candidate"] : [])],
    decision: stopTriggered ? "recommend_one_more_byte-identical_run_c" : "stop_repeated_inference_without_claiming_zero_variance"
  },
  interpretation: [
    "Codex, Opus and GLM reproduced their Run A mutation hit sets exactly. Gemini changed from two of four hits in Run A to four of four in Run B by detecting R007 and R008.",
    "Across 16 route-by-mutation primary comparisons, 14 agreed and two flipped, both on Gemini and both from miss to hit. This is direct evidence that the Run A Gemini 2/4 result was not stable under an identical rerun.",
    "All four routes marked all four source-verified controls OK in both runs. The observed variance affected mutation recall, not control candidates, in this small sample.",
    "Run B alone has Codex 4/4, Opus 3/4, GLM 3/4 and Gemini 4/4. Because the preregistered rule triggers on any primary flip, the next action is one more byte-identical Run C rather than a model ranking claim.",
    "Claude's assistant review messages all report claude-opus-5 with zero fallback events or blocks; aggregate modelUsage contains a small Haiku auxiliary charge. agy omits runtime model identity from its result envelope."
  ],
  limitations: [
    "Two runs over four mutations provide a variance warning, not a variance estimate or confidence interval.",
    "The two Gemini flips are directionally favorable, but cannot be separated into sampling variance versus unreported service-side behavior from this envelope.",
    "The experiment covers objective UI/log mechanism claims and does not test prose quality, translation origin or natural residual-defect prevalence.",
    "Runtime model identity for agy remains unverified because the CLI envelope reports neither model nor agent."
  ],
  next_step: "Run one more byte-identical Run C under the preregistered stop rule; then report per-item three-run detection frequency without changing the prompt or expanding the sample."
};
fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({primary_comparison: result.primary_comparison, stop_rule: result.preregistered_stop_rule, run_b: routes.map(route => ({route: route.route, hits: route.run_b.mutation_hits, controls: route.run_b.control_candidate_revision_ids}))}, null, 2)}\n`);
