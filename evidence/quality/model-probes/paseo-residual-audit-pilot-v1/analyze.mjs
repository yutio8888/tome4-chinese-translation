import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const routeFiles = [
  "CANDIDATE-codex-gpt-5.6-sol-high.json",
  "CANDIDATE-claude-opus-5-medium-no-advisor.json",
  "CANDIDATE-claude-fable-5-medium-no-advisor.json",
  "CANDIDATE-claude-opus-5-medium-fable-advisor.json",
  "CANDIDATE-pi-zai-cn-glm-5.3-flash-high.json"
];
const rawFiles = [
  "RAW-codex-gpt-5.6-sol-high.ndjson",
  "RAW-codex-gpt-5.6-sol-high.stderr.txt",
  "RAW-claude-opus-5-medium-no-advisor.ndjson",
  "RAW-claude-fable-5-medium-no-advisor.ndjson",
  "RAW-claude-opus-5-medium-fable-advisor.ndjson",
  "RAW-pi-zai-cn-glm-5.3-flash-high.ndjson",
  "RAW-pi-zai-cn-glm-5.3-flash-high.stderr.txt"
];

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
}

function sha256(name) {
  return crypto.createHash("sha256").update(fs.readFileSync(path.join(here, name))).digest("hex");
}

const holdout = readJson("HOLDOUT.json");
const provenance = readJson("PROVENANCE-KEY.json");
const adjudication = readJson("ADJUDICATION.json");
const ids = holdout.items.map(item => item.revision_id);
const provenanceById = new Map(provenance.items.map(item => [item.revision_id, item]));
const candidates = routeFiles.map(file => ({file, value: readJson(file)}));

for (const {file, value} of candidates) {
  if (!value.valid) throw new Error(`${file} is invalid`);
  const actualIds = value.response.revisions.map(item => item.revision_id);
  if (JSON.stringify(actualIds) !== JSON.stringify(ids)) throw new Error(`${file} has wrong coverage/order`);
  if (value.route === "claude-opus-5-medium-fable-advisor") {
    const advisorIterations = value.route_metadata.result?.usage?.iterations?.filter(iteration => iteration.type === "advisor_message") ?? [];
    if (advisorIterations.length !== 1 || advisorIterations[0].model !== "claude-fable-5") {
      throw new Error("advisor route lacks exactly one claude-fable-5 advisor_message");
    }
  }
}

const claimsByRevision = new Map(adjudication.claims.map(claim => [claim.revision_id, claim]));
const unionCandidateIds = new Set();
const routeResults = [];
for (const {file, value} of candidates) {
  const candidateRevisions = value.response.revisions.filter(item => item.verdict !== "OK");
  const candidateIds = candidateRevisions.map(item => item.revision_id);
  for (const id of candidateIds) unionCandidateIds.add(id);
  const outcomes = {confirmed: 0, refuted: 0, indeterminate: 0, unreachable: 0};
  for (const id of candidateIds) {
    const claim = claimsByRevision.get(id);
    if (!claim) throw new Error(`missing adjudication for ${value.route}/${id}`);
    outcomes[claim.status] += 1;
  }
  routeResults.push({
    route: value.route,
    candidate_file: file,
    candidate_sha256: sha256(file),
    valid: value.valid,
    duration_seconds: value.duration_seconds,
    verdict_counts: value.verdict_counts,
    candidate_revision_ids: candidateIds,
    candidate_outcomes: outcomes,
    confirmed_candidate_fraction: candidateIds.length ? outcomes.confirmed / candidateIds.length : null,
    route_metadata: value.route_metadata
  });
}

const adjudicatedIds = new Set(adjudication.claims.map(claim => claim.revision_id));
if (JSON.stringify([...unionCandidateIds].sort()) !== JSON.stringify([...adjudicatedIds].sort())) {
  throw new Error("adjudication does not exactly cover the model candidate union");
}

const stratumCounts = {};
for (const item of provenance.items) {
  stratumCounts[item.stratum] ??= {
    sampled_revisions: 0,
    candidate_union_revisions: 0,
    confirmed_revisions: 0,
    refuted_candidate_revisions: 0,
    indeterminate_revisions: 0,
    unreachable_revisions: 0
  };
  stratumCounts[item.stratum].sampled_revisions += 1;
}
for (const claim of adjudication.claims) {
  const stratum = provenanceById.get(claim.revision_id)?.stratum;
  if (!stratum) throw new Error(`missing provenance for ${claim.revision_id}`);
  stratumCounts[stratum].candidate_union_revisions += 1;
  if (claim.status === "confirmed") stratumCounts[stratum].confirmed_revisions += 1;
  if (claim.status === "refuted") stratumCounts[stratum].refuted_candidate_revisions += 1;
  if (claim.status === "indeterminate") stratumCounts[stratum].indeterminate_revisions += 1;
  if (claim.status === "unreachable") stratumCounts[stratum].unreachable_revisions += 1;
}
for (const value of Object.values(stratumCounts)) {
  value.confirmed_lower_bound_fraction = value.confirmed_revisions / value.sampled_revisions;
}

const reviewerCompositionAggregate = {
  GPT_ONLY_CONTEXTUAL_REVIEWER: {
    strata: [
      "S1_GPT_MOD_GPT_REV_GPT_ORCH",
      "S2_GPT_MOD_GPT_REV_NON_GPT_ORCH",
      "S4_NON_GPT_MOD_GPT_REV"
    ]
  },
  NON_GPT_ONLY_CONTEXTUAL_REVIEWER: {
    strata: ["S3_GPT_MOD_NON_GPT_REV"]
  }
};
for (const aggregate of Object.values(reviewerCompositionAggregate)) {
  aggregate.sampled_revisions = aggregate.strata.reduce((sum, stratum) => sum + stratumCounts[stratum].sampled_revisions, 0);
  aggregate.candidate_union_revisions = aggregate.strata.reduce((sum, stratum) => sum + stratumCounts[stratum].candidate_union_revisions, 0);
  aggregate.confirmed_revisions = aggregate.strata.reduce((sum, stratum) => sum + stratumCounts[stratum].confirmed_revisions, 0);
  aggregate.refuted_candidate_revisions = aggregate.strata.reduce((sum, stratum) => sum + stratumCounts[stratum].refuted_candidate_revisions, 0);
  aggregate.confirmed_lower_bound_fraction = aggregate.confirmed_revisions / aggregate.sampled_revisions;
}

const routeSets = Object.fromEntries(routeResults.map(route => [route.route, new Set(route.candidate_revision_ids)]));
const pairwise = [];
for (let leftIndex = 0; leftIndex < routeResults.length; leftIndex += 1) {
  for (let rightIndex = leftIndex + 1; rightIndex < routeResults.length; rightIndex += 1) {
    const left = routeResults[leftIndex].route;
    const right = routeResults[rightIndex].route;
    pairwise.push({
      left,
      right,
      shared_candidate_revision_ids: [...routeSets[left]].filter(id => routeSets[right].has(id))
    });
  }
}

const pureOpus = routeSets["claude-opus-5-medium-no-advisor"];
const advisorOpus = routeSets["claude-opus-5-medium-fable-advisor"];
const advisorComparison = {
  pure_opus_candidate_revision_ids: [...pureOpus],
  advisor_candidate_revision_ids: [...advisorOpus],
  removed_by_advisor: [...pureOpus].filter(id => !advisorOpus.has(id)),
  added_by_advisor: [...advisorOpus].filter(id => !pureOpus.has(id)),
  confirmed_removed_by_advisor: [...pureOpus].filter(id => !advisorOpus.has(id) && claimsByRevision.get(id)?.status === "confirmed")
};

const result = {
  schema_version: "paseo-residual-audit-result-v1",
  status: "COMPLETE_EXPLORATORY_PILOT",
  experiment_commit: "3570b34",
  source_repo_head: provenance.source_repo_head,
  holdout: {
    items: ids.length,
    sha256: sha256("HOLDOUT.json"),
    no_candidate_revisions_not_independently_adjudicated: ids.length - unionCandidateIds.size
  },
  artifact_hashes: {
    adjudication: sha256("ADJUDICATION.json"),
    candidates: Object.fromEntries(routeFiles.map(file => [file, sha256(file)])),
    raw: Object.fromEntries(rawFiles.map(file => [file, sha256(file)]))
  },
  candidate_union: {
    revision_ids: [...unionCandidateIds].sort(),
    revisions: unionCandidateIds.size,
    claims: adjudication.claims.length,
    outcomes: adjudication.claims.reduce((counts, claim) => {
      counts[claim.status] = (counts[claim.status] ?? 0) + 1;
      return counts;
    }, {}),
    confirmed_revision_ids: adjudication.claims.filter(claim => claim.status === "confirmed").map(claim => claim.revision_id),
    interpretation: "Only the model candidate union was source-adjudicated. Confirmed counts are lower bounds, not an estimate that all other revisions are clean."
  },
  route_results: routeResults,
  pairwise_candidate_overlap: pairwise,
  advisor_comparison: advisorComparison,
  provenance_strata: stratumCounts,
  reviewer_composition_aggregate: reviewerCompositionAggregate,
  historical_chain_of_confirmed_revisions: adjudication.claims.filter(claim => claim.status === "confirmed").map(claim => {
    const item = provenanceById.get(claim.revision_id);
    return {
      revision_id: claim.revision_id,
      stratum: item.stratum,
      task_id: item.task_id,
      orchestrator_family: item.orchestrator_family,
      candidate_modifier_family: item.candidate_modifier.family,
      contextual_reviewer_families: item.contextual_reviewer_families
    };
  }),
  conclusions: [
    "One source-confirmed residual semantic relation defect was found in 20 sampled terminal revisions.",
    "The confirmed revision came from the GPT-modifier/Grok-reviewer cross-family stratum; none was confirmed in the 15 sampled GPT-only-reviewer revisions.",
    "This pilot therefore does not support the narrow claim that GPT-only historical review left more detectable residual defects, but its sample, topic imbalance and candidate-union-only adjudication are far too weak to refute systemic bias.",
    "Codex and pure Opus independently converged on the sole confirmed revision. Pure Opus also produced one source-scope false positive; Fable produced one terminology false positive; GLM and the Opus+Fable Advisor composite produced no candidates.",
    "Advisor removed both pure-Opus candidates, including the confirmed one, so it reduced false positives and true findings together rather than improving the pilot result."
  ],
  limitations: [
    "No independent human reviewer or sealed natural-defect reference exists.",
    "The current GPT/Codex research agent performed post-inference source-constrained adjudication.",
    "Only three model-nominated revisions were adjudicated; 17 no-candidate revisions remain unverified.",
    "Five revisions per provenance stratum cannot support stable rates or significance tests.",
    "Strata differ in task age, content category, batch size, context quality and workflow, and original translation generators remain unknown.",
    "Historical repeated reviews within a task are correlated and are not independent samples."
  ],
  next_experiment: "Run a preregistered controlled-mutation reviewer-by-translation-origin experiment with objective mutation labels, because this natural pilot cannot identify causal same-family preference without original generator provenance or independent ground truth."
};

fs.writeFileSync(path.join(here, "RESULT.json"), `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(JSON.stringify({
  status: result.status,
  candidate_union: result.candidate_union,
  provenance_strata: result.provenance_strata,
  advisor_comparison: result.advisor_comparison
}, null, 2) + "\n");
