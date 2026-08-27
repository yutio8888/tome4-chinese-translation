import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const outIndex = process.argv.indexOf("--out");
if (outIndex !== -1 && !process.argv[outIndex + 1]) throw new Error("--out requires a path");
const outputPath = outIndex === -1 ? path.join(here, "RESULT.json") : path.resolve(process.argv[outIndex + 1]);
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
const read = file => JSON.parse(fs.readFileSync(path.join(here, file), "utf8"));
const reference = read("REFERENCE.json");
const adjudication = read("ADJUDICATION.json");
const routeFiles = {
  "codex-gpt-5.6-sol-high": {
    candidate: "CANDIDATE-codex-gpt-5.6-sol-high.json",
    candidate_sha256: "2955459f89561fd8224ac1fb27987dcbcc3e1f60cadc68335191446c5fabc607",
    raw: "RAW-codex-gpt-5.6-sol-high.json",
    raw_sha256: "63a982a5c53b9ea8c80c827219aac1bc0acbef8769e9741c599034f6d7de1c23"
  },
  "claude-opus-5-medium-no-advisor": {
    candidate: "CANDIDATE-claude-opus-5-medium-no-advisor.json",
    candidate_sha256: "9456ee1a8ad88a5d39ad24c18d0ce0c4c66057b8f9b5a13c8d8dd85f6dbb0061",
    raw: "RAW-claude-opus-5-medium-no-advisor.json",
    raw_sha256: "386e449cc71c8f7e83a40ca6e2e910cf44e8ab5547278aa6282e1ff8a54c8b96"
  },
  "pi-zai-cn-glm-5.3-flash-high": {
    candidate: "CANDIDATE-pi-zai-cn-glm-5.3-flash-high.json",
    candidate_sha256: "e5b2b86376cc8d4c05a0bb4aa1d76767d860adc62edd905c7ff4ba3c5a984823",
    raw: "RAW-pi-zai-cn-glm-5.3-flash-high.json",
    raw_sha256: "c4c0e5df5e75e984d9b8ec827e97c5d1736fd9ea5e7c395cc424a111eede3b4c"
  },
  "agy-gemini-3.7-flash-high": {
    candidate: "CANDIDATE-agy-gemini-3.7-flash-high.json",
    candidate_sha256: "7abdca39a4eb625c00a0e69761e967698275731af9d6cb3e644ad001f874df6a",
    raw: "RAW-agy-gemini-3.7-flash-high.json",
    raw_sha256: "d32eab6545ed7f3d5a51685ad7ef09fe7cecef33d2d0b5b1c02534d1a6d00cbf"
  }
};
const mutations = reference.items.filter(item => item.label === "INJECTED_MUTATION");
const controls = reference.items.filter(item => item.label === "SOURCE_VERIFIED_CONTROL");
const mutationIds = mutations.map(item => item.revision_id);
const controlIds = controls.map(item => item.revision_id);
const scores = [];
const hitSets = [];
for (const [route, files] of Object.entries(routeFiles)) {
  for (const kind of ["candidate", "raw"]) if (sha256(files[kind]) !== files[`${kind}_sha256`]) throw new Error(`${route} ${kind} hash mismatch`);
  const candidate = read(files.candidate);
  if (!candidate.valid || candidate.route !== route) throw new Error(`${route} candidate validity/identity mismatch`);
  const byId = new Map(candidate.response.revisions.map(item => [item.revision_id, item]));
  const hits = adjudication.mutation_claim_matches[route];
  const misses = mutationIds.filter(id => !hits.includes(id));
  if (JSON.stringify(misses) !== JSON.stringify(adjudication.mutation_misses[route].map(item => item.revision_id))) throw new Error(`${route} miss adjudication mismatch`);
  for (const id of hits) if (byId.get(id)?.verdict === "OK") throw new Error(`${route} ${id} claim match is OK`);
  const findingHits = hits.filter(id => byId.get(id).verdict === "FINDING");
  const uncertainHits = hits.filter(id => byId.get(id).verdict === "UNCERTAIN");
  const controlCandidates = controlIds.filter(id => byId.get(id).verdict !== "OK");
  if (JSON.stringify(controlCandidates) !== JSON.stringify(adjudication.control_candidates[route])) throw new Error(`${route} control candidate mismatch`);
  hitSets.push(new Set(hits));
  scores.push({
    route,
    candidate_artifact: files.candidate,
    candidate_sha256: files.candidate_sha256,
    raw_artifact: files.raw,
    raw_sha256: files.raw_sha256,
    route_metadata: candidate.route_metadata,
    duration_seconds: candidate.duration_seconds,
    verdict_counts: candidate.verdict_counts,
    mutation_specific_detection: {hits: hits.length, total: mutationIds.length, recall: hits.length / mutationIds.length, hit_revision_ids: hits, missed_revision_ids: misses},
    finding_only_mutation_detection: {hits: findingHits.length, total: mutationIds.length, recall: findingHits.length / mutationIds.length, hit_revision_ids: findingHits, uncertain_match_revision_ids: uncertainHits},
    source_verified_controls: {true_negatives: controlIds.length - controlCandidates.length, total: controlIds.length, specificity: (controlIds.length - controlCandidates.length) / controlIds.length, candidate_revision_ids: controlCandidates}
  });
}
const union = mutationIds.filter(id => hitSets.some(set => set.has(id)));
const consensus = mutationIds.filter(id => hitSets.every(set => set.has(id)));
const supportCounts = Object.fromEntries(mutationIds.map(id => [id, hitSets.filter(set => set.has(id)).length]));
const result = {
  schema_version: 1,
  experiment: "controlled-mutation-ui-log-replication-v2",
  status: "COMPLETE",
  scored_at: "2026-08-27",
  frozen_input_sha256: sha256("HOLDOUT.json"),
  sealed_reference_sha256: sha256("REFERENCE.json"),
  source_verification_sha256: sha256("SOURCE-VERIFICATION.json"),
  adjudication_sha256: sha256("ADJUDICATION.json"),
  design: {fresh_category: "P2 UI and combat logs", injected_mutations: mutationIds.length, directly_source_verified_controls: controlIds.length, independent_single_runs: true, route_output_exchange: false, fixture_only_baseline_repairs: 1},
  scores,
  derived: {
    mutation_union: {hits: union.length, total: mutationIds.length, recall: union.length / mutationIds.length, revision_ids: union},
    four_route_consensus: {hits: consensus.length, total: mutationIds.length, recall: consensus.length / mutationIds.length, revision_ids: consensus},
    support_count_by_mutation: supportCounts,
    unique_mutation_hits: Object.fromEntries(scores.map(score => [score.route, score.mutation_specific_detection.hit_revision_ids.filter(id => supportCounts[id] === 1)]))
  },
  interpretation: [
    "Codex matched all four injected mutations. Opus and GLM matched three; Gemini matched two. Opus R008 is a correct UNCERTAIN and therefore counts in the preregistered primary non-OK atomic-claim metric.",
    "All routes detected R001 (wrong increased attribute) and R005 (wrong prerequisite identity). Only Codex detected R007's omitted companion out-of-combat condition. Gemini also missed R008's runtime four-turn duration; Opus raised it as uncertain and GLM/Codex as findings.",
    "All four routes marked all four directly source-verified controls OK. This small replication therefore had no control contamination and no control false-positive candidates.",
    "Compared descriptively with v1, near-ceiling recall did not persist uniformly on the fresh UI/log category: Codex stayed at 100%, while GLM was 75%, Opus 75% under the primary metric and Gemini 50%. Four mutations are too few for stable ranking claims.",
    "Claude's assistant review messages all report claude-opus-5 with zero fallback events/blocks; aggregate modelUsage again contains a small Haiku auxiliary charge. agy again omits runtime model identity from its envelope."
  ],
  limitations: [
    "Only four mutations were tested and each route ran once; this is a category replication, not a stochastic variance estimate.",
    "Mutation difficulty is heterogeneous and two consensus-easy items dominate the denominator.",
    "The fixture-only Startling Shot baseline correction tests a verified clean target, not the current production translation.",
    "The experiment does not vary translation origin or test prose quality."
  ],
  next_step: "If more budget is available, repeat the same frozen eight-item input without prompt changes to estimate run-to-run variance, especially on R007/R008, before funding a reviewer-by-translation-origin factorial."
};
fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(scores.map(score => ({route: score.route, mutation_recall: score.mutation_specific_detection.recall, finding_only_recall: score.finding_only_mutation_detection.recall, control_specificity: score.source_verified_controls.specificity})), null, 2)}\n`);
