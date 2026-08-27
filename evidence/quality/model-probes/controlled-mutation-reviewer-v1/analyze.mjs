import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const outIndex = process.argv.indexOf("--out");
const outputPath = outIndex === -1 ? path.join(here, "RESULT.json") : path.resolve(process.argv[outIndex + 1]);
if (outIndex !== -1 && !process.argv[outIndex + 1]) throw new Error("--out requires a path");
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
const read = file => JSON.parse(fs.readFileSync(path.join(here, file), "utf8"));
const reference = read("REFERENCE.json");
const adjudication = read("ADJUDICATION.json");
const routeFiles = {
  "codex-gpt-5.6-sol-high": {
    candidate: "CANDIDATE-codex-gpt-5.6-sol-high.json",
    candidate_sha256: "b58226cf93825ef7039ad45c46bb56574dd8caf7006cb7e164f66fc8e3a98dcc",
    raw: "RAW-codex-gpt-5.6-sol-high.json",
    raw_sha256: "cefaeacc319dfbe0c9c16d76c4641a8f92a1fe303410f9c7120f2103af48498d"
  },
  "claude-opus-5-medium-no-advisor": {
    candidate: "CANDIDATE-claude-opus-5-medium-no-advisor.json",
    candidate_sha256: "c308ea1f8f24513d2a2cd44d4d3a418f671e0d0e724757ce447b54e0bb6b0754",
    raw: "RAW-claude-opus-5-medium-no-advisor.json",
    raw_sha256: "645111f910ea2d319e17b002f9ac5e1fccaf4bd21ed262cd003675c426f7f737"
  },
  "pi-zai-cn-glm-5.3-flash-high": {
    candidate: "CANDIDATE-NORMALIZED-pi-zai-cn-glm-5.3-flash-high.json",
    candidate_sha256: "1cf10d7650d5d2cee92cd8e595398720453c248e972342e2f6a8479a266ad654",
    raw: "RAW-pi-zai-cn-glm-5.3-flash-high.json",
    raw_sha256: "38c5bc95a7cdc5d272ee3960e52d6ff94a117cb4fee9bf276b55ce889aa7cd3d",
    normalization: "NORMALIZATION-pi-zai-cn-glm-5.3-flash-high.json",
    normalization_sha256: "a0698b2fc37fb772014a6530e187d6fd51cfa4f2be1223b9c7bd952a0b9c1797"
  },
  "agy-gemini-3.7-flash-high": {
    candidate: "CANDIDATE-agy-gemini-3.7-flash-high.json",
    candidate_sha256: "fc4a2734c2101e5b40a78e7c93bbbea24799599ec7912acf58c0adf0449dc726",
    raw: "RAW-agy-gemini-3.7-flash-high.json",
    raw_sha256: "5e94ffca0035b4e216b7fbb492e7f11bfab0a66e6a9d09b4273072c57a689c75"
  }
};

const mutationItems = reference.items.filter(item => item.label === "INJECTED_MUTATION");
const controlItems = reference.items.filter(item => item.label === "UNMODIFIED_CONTROL");
const mutationIds = mutationItems.map(item => item.revision_id);
const controlIds = controlItems.map(item => item.revision_id);
const naturalDefectIds = adjudication.non_mutation_candidates.filter(item => item.adjudication === "confirmed_natural_defect").map(item => item.revision_id);
const cleanControlIds = controlIds.filter(id => !naturalDefectIds.includes(id));
const scores = [];
const routeHitSets = [];

for (const [route, files] of Object.entries(routeFiles)) {
  for (const kind of ["candidate", "raw", "normalization"]) {
    if (!files[kind]) continue;
    const actual = sha256(files[kind]);
    if (actual !== files[`${kind}_sha256`]) throw new Error(`${route} ${kind} hash mismatch: ${actual}`);
  }
  const candidate = read(files.candidate);
  if (!candidate.valid || candidate.route !== route) throw new Error(`${route} candidate identity/validity mismatch`);
  const byId = new Map(candidate.response.revisions.map(item => [item.revision_id, item]));
  const claimMatches = adjudication.mutation_claim_matches[route];
  const expectedMisses = mutationIds.filter(id => !claimMatches.includes(id));
  if (JSON.stringify(expectedMisses) !== JSON.stringify(adjudication.mutation_misses[route].map(item => item.revision_id))) throw new Error(`${route} adjudicated misses mismatch`);
  for (const id of claimMatches) if (byId.get(id)?.verdict === "OK") throw new Error(`${route} claim match ${id} is marked OK`);
  const findingOnlyHits = claimMatches.filter(id => byId.get(id).verdict === "FINDING");
  const uncertainHits = claimMatches.filter(id => byId.get(id).verdict === "UNCERTAIN");
  const controlCandidates = controlIds.filter(id => byId.get(id).verdict !== "OK");
  const confirmedNaturalCandidates = controlCandidates.filter(id => naturalDefectIds.includes(id));
  const falsePositiveIds = controlCandidates.filter(id => !naturalDefectIds.includes(id));
  const cleanControlTrueNegatives = cleanControlIds.filter(id => byId.get(id).verdict === "OK");
  const nonMutationClaimsOnMutants = mutationIds.filter(id => byId.get(id).verdict !== "OK" && !claimMatches.includes(id));
  routeHitSets.push(new Set(claimMatches));
  scores.push({
    route,
    candidate_artifact: files.candidate,
    candidate_sha256: files.candidate_sha256,
    raw_artifact: files.raw,
    raw_sha256: files.raw_sha256,
    normalization_artifact: files.normalization ?? null,
    route_metadata: candidate.route_metadata,
    duration_seconds: candidate.duration_seconds,
    verdict_counts: candidate.verdict_counts,
    mutation_specific_detection: {
      hits: claimMatches.length,
      total: mutationIds.length,
      recall: claimMatches.length / mutationIds.length,
      hit_revision_ids: claimMatches,
      missed_revision_ids: expectedMisses
    },
    finding_only_mutation_detection: {
      hits: findingOnlyHits.length,
      total: mutationIds.length,
      recall: findingOnlyHits.length / mutationIds.length,
      hit_revision_ids: findingOnlyHits,
      uncertain_match_revision_ids: uncertainHits
    },
    controls: {
      unmodified_candidates: controlCandidates.length,
      candidate_revision_ids: controlCandidates,
      confirmed_natural_issue_candidates: confirmedNaturalCandidates.length,
      confirmed_natural_issue_revision_ids: confirmedNaturalCandidates,
      source_refuted_false_positives: falsePositiveIds.length,
      false_positive_revision_ids: falsePositiveIds,
      post_adjudication_clean_true_negatives: cleanControlTrueNegatives.length,
      post_adjudication_clean_total: cleanControlIds.length,
      post_adjudication_clean_specificity: cleanControlTrueNegatives.length / cleanControlIds.length
    },
    non_mutation_claims_on_mutated_items: nonMutationClaimsOnMutants
  });
}

const union = mutationIds.filter(id => routeHitSets.some(set => set.has(id)));
const consensus = mutationIds.filter(id => routeHitSets.every(set => set.has(id)));
const supportCounts = Object.fromEntries(mutationIds.map(id => [id, routeHitSets.filter(set => set.has(id)).length]));
const result = {
  schema_version: 1,
  experiment: "controlled-mutation-reviewer-v1",
  status: "COMPLETE",
  scored_at: "2026-08-27",
  frozen_input_sha256: sha256("HOLDOUT.json"),
  sealed_reference_sha256: sha256("REFERENCE.json"),
  adjudication_sha256: sha256("ADJUDICATION.json"),
  design: {
    injected_mutations: mutationIds.length,
    unmodified_controls: controlIds.length,
    post_adjudication_clean_controls: cleanControlIds.length,
    natural_defects_discovered_in_controls: naturalDefectIds,
    independent_single_runs: true,
    route_output_exchange: false
  },
  scores,
  derived: {
    mutation_union: {hits: union.length, total: mutationIds.length, recall: union.length / mutationIds.length, revision_ids: union},
    four_route_consensus: {hits: consensus.length, total: mutationIds.length, recall: consensus.length / mutationIds.length, revision_ids: consensus},
    support_count_by_mutation: supportCounts,
    unique_mutation_hits: Object.fromEntries(scores.map(score => [score.route, score.mutation_specific_detection.hit_revision_ids.filter(id => supportCounts[id] === 1)]))
  },
  natural_control_finding: adjudication.non_mutation_candidates[0],
  interpretation: [
    "Codex and GLM matched all 12 injected mutation claims. Opus matched 11/12 when its correct C023 UNCERTAIN is counted under the preregistered non-OK atomic-claim metric; Gemini matched 11/12.",
    "Ten mutations were detected by all four routes. C005 was missed only by Opus; C023 was missed only by Gemini. No route had a unique injected-mutation hit.",
    "The unmodified C008 control contains a source-confirmed natural defect. Codex raised it as FINDING and Opus raised the same atomic claim as UNCERTAIN; it is not a false positive and is excluded from the clean-control denominator.",
    "All four routes produced zero source-refuted control false positives and marked all 11 post-adjudication clean controls OK.",
    "C008 is a concrete historical terminal-review false negative in a GPT/Codex-modified and GPT/Codex-reviewed Paseo task, but one item cannot establish the prevalence or direction of a systematic GPT-family bias.",
    "Claude's complete-task assistant messages all report claude-opus-5 with zero fallback events or blocks. Claude Code's aggregate modelUsage also lists a small Haiku auxiliary charge; it is disclosed as harness overhead and not treated as a reviewer message.",
    "The agy envelope does not expose a runtime model or agent identity. Its route identity is therefore supported by the frozen gemini-3.7-flash-high request, the immediately preceding model-availability check and the preserved RAW, not by an envelope-reported model field."
  ],
  limitations: [
    "One independent run per route does not estimate variance.",
    "Injected mechanism defects do not estimate the natural residual-defect rate or prose quality.",
    "The unmodified controls were historical terminal revisions, not independently proven clean controls; source adjudication found one contaminated control.",
    "The mutation categories have one or two examples each, so per-category rates are descriptive only.",
    "This experiment does not vary translation origin and therefore cannot test reviewer-by-origin self-preference.",
    "Claude Code reports auxiliary Haiku usage despite every assistant review message being Opus, and agy omits runtime identity from its envelope; these harness-level facts limit claims of perfectly isolated model execution."
  ],
  route_policy: {
    "active_for_this_experiment": Object.keys(routeFiles),
    "retired_for_budget": ["claude-fable-5-medium-no-advisor", "claude-opus-5-medium-fable-advisor"],
    "historical_results_preserved": true
  },
  next_gate: "Before funding a full reviewer-by-translation-origin factorial, repair the control-construction rule with direct FIREBURN-style primitive tracing and run a small fresh-category replication to estimate variance and contamination."
};
fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(scores.map(score => ({route: score.route, mutation_recall: score.mutation_specific_detection.recall, finding_only_recall: score.finding_only_mutation_detection.recall, control_candidates: score.controls.unmodified_candidates, false_positives: score.controls.source_refuted_false_positives})), null, 2)}\n`);
