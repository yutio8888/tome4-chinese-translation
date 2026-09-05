#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {FROZEN, buildHanStatistics, readInventory, scanRows, sha256Bytes, sha256File} from "./scanner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const values = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  const flag = process.argv[index];
  const value = process.argv[index + 1];
  if (!value || !["--inventory", "--schema", "--out-dir"].includes(flag) || values.has(flag)) {
    throw new Error("usage: node scan.mjs --inventory INVENTORY_JSONL --schema INVENTORY_SCHEMA [--out-dir OUTPUT_DIRECTORY]");
  }
  values.set(flag, path.resolve(value));
}
if (!values.has("--inventory") || !values.has("--schema")) throw new Error("--inventory and --schema are required");
const outDirectory = values.get("--out-dir") ?? here;

const readJson = name => JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
const exclusionsArtifact = readJson("EXCLUSIONS.json");
const inventory = readInventory(values.get("--inventory"));
if (inventory.rows.length !== FROZEN.inventoryRows) throw new Error(`inventory row drift: ${inventory.rows.length}`);
if (new Set(inventory.rows.map(row => row.revision_id)).size !== inventory.rows.length) throw new Error("inventory revision IDs are not unique");
if (inventory.raw_sha256 !== FROZEN.inventoryRawSha256) throw new Error(`inventory raw hash drift: ${inventory.raw_sha256}`);
if (inventory.canonical_sha256 !== FROZEN.inventoryCanonicalSha256) throw new Error(`inventory canonical hash drift: ${inventory.canonical_sha256}`);
if (sha256File(values.get("--schema")) !== FROZEN.inventorySchemaSha256) throw new Error("inventory schema hash drift");

const statistics = buildHanStatistics(inventory.rows);
if (statistics.hanCharacters !== FROZEN.hanCharacters) throw new Error(`Han corpus size drift: ${statistics.hanCharacters}`);
const scan = scanRows(inventory.rows, statistics);

const exclusionIdentity = value => JSON.stringify([
  value.revision_id,
  value.revision_uid,
  value.tier,
  value.boundary.line_ordinal_zero_based,
  value.boundary.bigram,
  value.boundary.rendered,
  value.source_sha256,
  value.target_sha256
]);
const exclusionByIdentity = new Map();
for (const exclusion of exclusionsArtifact.exclusions) {
  const identity = exclusionIdentity(exclusion);
  if (exclusionByIdentity.has(identity)) throw new Error(`duplicate exclusion: ${exclusion.v1_candidate_id}`);
  exclusionByIdentity.set(identity, exclusion);
}
if (exclusionByIdentity.size !== FROZEN.expectedPreExclusionCandidates) throw new Error(`exclusion registry count drift: ${exclusionByIdentity.size}`);

const excludedCandidates = [];
const independentCandidates = [];
for (const candidate of scan.candidates) {
  const exclusion = exclusionByIdentity.get(exclusionIdentity(candidate));
  if (exclusion) {
    excludedCandidates.push({
      ...candidate,
      exclusion: {v1_candidate_id: exclusion.v1_candidate_id, reason: "V1_DEVELOPMENT_IDENTITY_AND_BOUNDARY"}
    });
  } else {
    independentCandidates.push({...candidate, holdout_candidate_id: `HLB${String(independentCandidates.length + 1).padStart(3, "0")}`});
  }
}
if (scan.candidates.length !== FROZEN.expectedPreExclusionCandidates) throw new Error(`pre-exclusion candidate drift: ${scan.candidates.length}`);
if (excludedCandidates.length !== exclusionByIdentity.size) throw new Error("exclusion registry does not cover the emitted set exactly");
if (independentCandidates.length !== FROZEN.expectedPostExclusionCandidates) throw new Error(`post-exclusion candidate drift: ${independentCandidates.length}`);

const componentNames = [...new Set(inventory.rows.map(row => row.component))].sort();
const componentCoverage = Object.fromEntries(componentNames.map(component => [component, {
  inventory_rows: inventory.rows.filter(row => row.component === component).length,
  pre_exclusion_candidates: scan.candidates.filter(candidate => candidate.component === component).length,
  excluded_development_candidates: excludedCandidates.filter(candidate => candidate.component === component).length,
  independent_candidates: independentCandidates.filter(candidate => candidate.component === component).length
}]));

const candidates = {
  schema_version: "deterministic-linebreak-holdout-candidates-v2",
  experiment: "deterministic-linebreak-lint-holdout-v2",
  status: "ZERO_INDEPENDENT_CANDIDATES_AFTER_EXACT_EXCLUSION",
  model_calls_made: 0,
  network_calls_made: 0,
  input_bindings: {
    baseline_commit: FROZEN.baselineCommit,
    inventory_rows: inventory.rows.length,
    inventory_raw_sha256: inventory.raw_sha256,
    inventory_canonical_sha256: inventory.canonical_sha256,
    inventory_schema_sha256: FROZEN.inventorySchemaSha256,
    rule_contract: {logical_path: "RULE-CONTRACT.json", sha256: sha256File(path.join(here, "RULE-CONTRACT.json"))},
    exclusions: {logical_path: "EXCLUSIONS.json", sha256: sha256File(path.join(here, "EXCLUSIONS.json"))}
  },
  corpus_statistics: {
    han_characters: statistics.hanCharacters,
    distinct_han_characters: statistics.characterFrequency.size,
    distinct_contiguous_han_bigrams: statistics.bigramFrequency.size
  },
  scan_counts: {
    ...scan.counts,
    pre_exclusion_candidates: scan.candidates.length,
    pre_exclusion_candidate_revisions: new Set(scan.candidates.map(candidate => candidate.revision_id)).size,
    excluded_development_candidates: excludedCandidates.length,
    post_exclusion_independent_candidates: independentCandidates.length,
    by_tier_pre_exclusion: Object.fromEntries(["Q_QUOTED_TWO_HAN_TOKEN", "A_FREQUENT_BIGRAM", "B_LOW_SUPPORT_BIGRAM"].map(tier => [tier, scan.candidates.filter(candidate => candidate.tier === tier).length])),
    by_tier_post_exclusion: Object.fromEntries(["Q_QUOTED_TWO_HAN_TOKEN", "A_FREQUENT_BIGRAM", "B_LOW_SUPPORT_BIGRAM"].map(tier => [tier, independentCandidates.filter(candidate => candidate.tier === tier).length]))
  },
  component_coverage: componentCoverage,
  pre_exclusion_candidates: excludedCandidates,
  independent_holdout_candidates: independentCandidates
};

const serialize = value => `${JSON.stringify(value, null, 2)}\n`;
const candidateBytes = serialize(candidates);
const sourceAudit = {
  schema_version: "deterministic-linebreak-holdout-source-audit-v2",
  experiment: "deterministic-linebreak-lint-holdout-v2",
  status: "COMPLETE_EMPTY_AUDIT_BOUND_TO_ZERO_CANDIDATE_HOLDOUT",
  model_calls_made: 0,
  network_calls_made: 0,
  candidate_artifact: {logical_path: "CANDIDATES.json", sha256: sha256Bytes(candidateBytes)},
  holdout_population_binding: {
    independent_candidate_count: independentCandidates.length,
    ordered_identity_set_sha256: sha256Bytes(JSON.stringify(independentCandidates.map(candidate => [candidate.revision_id, candidate.boundary.rendered])))
  },
  audit_scope: "Every emitted independent holdout candidate would be audited against fixed source and context. The bound set is empty, so there are no scored records.",
  provenance_boundary: "No v1 source-audit verdict or development adjudication is copied, relabeled, pooled, or scored as holdout evidence.",
  records: [],
  counts: {independent_candidates: 0, audited: 0, confirmed_format_defects: 0, refuted: 0, indeterminate: 0},
  precision: {denominator: 0, value: null, status: "UNDEFINED_ZERO_DENOMINATOR"}
};
const auditBytes = serialize(sourceAudit);
const result = {
  schema_version: "deterministic-linebreak-lint-holdout-result-v2",
  experiment: "deterministic-linebreak-lint-holdout-v2",
  status: "NO_GO_INSUFFICIENT_INDEPENDENT_CANDIDATES",
  model_calls_made: 0,
  network_calls_made: 0,
  frozen_input: {
    baseline_commit: FROZEN.baselineCommit,
    inventory_rows: inventory.rows.length,
    inventory_raw_sha256: inventory.raw_sha256,
    inventory_canonical_sha256: inventory.canonical_sha256,
    inventory_schema_sha256: FROZEN.inventorySchemaSha256,
    translation_inputs_sha256: FROZEN.translationInputsSha256,
    inventory_manifest_sha256: FROZEN.inventoryManifestSha256,
    inventory_policy_sha256: FROZEN.inventoryPolicySha256,
    inventory_taxonomy_sha256: FROZEN.inventoryTaxonomySha256,
    inventory_terminology_sha256: FROZEN.inventoryTerminologySha256
  },
  measured_scan: {
    raw_han_lf_han_boundaries: scan.counts.raw_han_lf_han_boundaries,
    raw_revisions: scan.counts.raw_revisions,
    pre_exclusion_candidates: scan.candidates.length,
    exactly_excluded_v1_development_candidates: excludedCandidates.length,
    post_exclusion_independent_candidates: independentCandidates.length
  },
  independent_evaluation: {
    audited_candidates: 0,
    precision_denominator: 0,
    precision: null,
    recall: null,
    status: "NOT_ESTIMABLE_FROM_ZERO_INDEPENDENT_EMISSIONS"
  },
  cross_component_coverage: componentCoverage,
  cross_component_shortfall: "All five pre-exclusion emissions are exposed Tome development candidates. Every component has zero independent emissions; cross-component performance is not evaluated.",
  prohibited_claims: [
    "independent precision/recall claims",
    "zero-false-alarm claims",
    "pooled-v1 performance claims",
    "cross-component performance claims",
    "deployment or production lint integration claims"
  ],
  decision: "Do not authorize deployment. A future warning-only gate requires a separately versioned preregistration on an unseen future snapshot.",
  future_threshold: null,
  artifact_bindings: {
    experiment: {logical_path: "EXPERIMENT.json", sha256: sha256File(path.join(here, "EXPERIMENT.json"))},
    rule_contract: {logical_path: "RULE-CONTRACT.json", sha256: sha256File(path.join(here, "RULE-CONTRACT.json"))},
    exclusions: {logical_path: "EXCLUSIONS.json", sha256: sha256File(path.join(here, "EXCLUSIONS.json"))},
    scanner_fixtures: {logical_path: "SCANNER-FIXTURES.json", sha256: sha256File(path.join(here, "SCANNER-FIXTURES.json"))},
    scanner_library: {logical_path: "scanner-lib.mjs", sha256: sha256File(path.join(here, "scanner-lib.mjs"))},
    scanner_entrypoint: {logical_path: "scan.mjs", sha256: sha256File(path.join(here, "scan.mjs"))},
    candidates: {logical_path: "CANDIDATES.json", sha256: sha256Bytes(candidateBytes)},
    source_audit: {logical_path: "SOURCE-AUDIT.json", sha256: sha256Bytes(auditBytes)}
  }
};

const outputs = new Map([
  ["CANDIDATES.json", candidateBytes],
  ["SOURCE-AUDIT.json", auditBytes],
  ["RESULT.json", serialize(result)]
]);
fs.mkdirSync(outDirectory, {recursive: true});
for (const [name, bytes] of outputs) {
  const output = path.join(outDirectory, name);
  if (fs.existsSync(output)) {
    if (fs.readFileSync(output, "utf8") !== bytes) throw new Error(`existing output drift: ${output}`);
  } else {
    fs.writeFileSync(output, bytes, {flag: "wx"});
  }
}
process.stdout.write(`${JSON.stringify({
  status: result.status,
  inventory_rows: inventory.rows.length,
  pre_exclusion_candidates: scan.candidates.length,
  exact_exclusions: excludedCandidates.length,
  post_exclusion_independent_candidates: independentCandidates.length,
  output_hashes: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha256Bytes(bytes)]))
}, null, 2)}\n`);
