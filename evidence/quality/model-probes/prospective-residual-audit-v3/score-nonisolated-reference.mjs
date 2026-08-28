import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {scoreResponse} from "./score-lib.mjs";
import {assert, readJson, sha256Bytes, sha256File, writeNewFile} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidateRelative = "attempts/claude-opus-5-medium-no-advisor/attempt-001/CANDIDATE-PARSER-FIX-1.json";
const candidatePath = path.join(here, candidateRelative);
const candidate = readJson(candidatePath);

assert(candidate.schema_version === "prospective-residual-candidate-v3", "candidate schema drift");
assert(candidate.experiment === "prospective-residual-audit-v3", "candidate experiment drift");
assert(candidate.route === "claude-opus-5-medium-no-advisor", "candidate route drift");
assert(candidate.attempt === 1, "candidate attempt drift");
assert(candidate.request_sha256 === "1ae147448209b8f31e27dd1089b7363c546dfcea336fe1debaecf3ae357135c9", "candidate request drift");
assert(candidate.valid === false, "candidate is no longer the frozen route-invalid artifact");
assert(candidate.validation_errors?.length === 1, "unexpected candidate validation-error count");
assert(
  candidate.validation_errors[0] === "Claude non-Opus/advisor model usage detected: claude-haiku-4-5-20251001,claude-opus-5",
  "unexpected candidate validation error"
);

const holdout = readJson(path.join(here, "PUBLIC-HOLDOUT.json"));
const reference = readJson(path.join(here, "SEALED-REFERENCE.json"));
const atomMap = readJson(path.join(here, "SEALED-ATOM-MAP.json"));
const score = scoreResponse({response: candidate.response, holdout, reference, atomMap});
assert(score.valid, `response cannot be reference-scored: ${score.validation_errors.join("; ")}`);

const output = {
  schema_version: "prospective-residual-posthoc-reference-score-v1",
  experiment: "prospective-residual-audit-v3",
  status: "SCORED_POSTHOC_REFERENCE_ONLY_NONISOLATED",
  authorized_at_utc: "2026-08-28",
  scoring_subject: "the response content in a mixed-model Claude envelope",
  route_label_prohibited: true,
  primary_ranking_eligible: false,
  reason: "The user explicitly requested a reference score even without an isolation/purity guarantee. This additive score does not alter the frozen primary route result.",
  limitations: [
    "The envelope reports both claude-haiku-4-5-20251001 and claude-opus-5 usage, so this is not an Opus-only score.",
    "The original frozen route remains INVALID_NO_SCORE for primary-route accounting.",
    "This post-hoc reference score is descriptive and cannot enter a cross-tier model ranking."
  ],
  source_bindings: {
    candidate: {logical_path: candidateRelative, sha256: sha256File(candidatePath)},
    response_sha256: sha256Bytes(Buffer.from(JSON.stringify(candidate.response), "utf8")),
    public_holdout_sha256: sha256File(path.join(here, "PUBLIC-HOLDOUT.json")),
    sealed_reference_sha256: sha256File(path.join(here, "SEALED-REFERENCE.json")),
    sealed_atom_map_sha256: sha256File(path.join(here, "SEALED-ATOM-MAP.json"))
  },
  reported_models: candidate.route_metadata.used_models,
  score_status: "SCORED_POSTHOC_REFERENCE_ONLY_NONISOLATED",
  metrics: score.metrics
};

const outputPath = path.join(here, "REFERENCE-SCORE-NONISOLATED.json");
const outputBytes = `${JSON.stringify(output, null, 2)}\n`;
let verifiedExisting = false;
if (fs.existsSync(outputPath)) {
  assert(fs.readFileSync(outputPath, "utf8") === outputBytes, "existing post-hoc reference score does not match deterministic recomputation");
  verifiedExisting = true;
} else {
  writeNewFile(outputPath, outputBytes);
}
process.stdout.write(`${JSON.stringify({
  status: output.status,
  verified_existing: verifiedExisting,
  atom_recall: output.metrics.primary_atom_detection.recall.fraction,
  unweighted_confusion: output.metrics.binary_nomination_unweighted,
  weighted_balanced_accuracy: output.metrics.binary_nomination_weighted.balanced_accuracy
}, null, 2)}\n`);
