import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {scoreResponse} from "./score-lib.mjs";
import {
  assert,
  attemptDirectory,
  parseAttempt,
  readCandidateArtifact,
  readJson,
  requestBytes,
  routeFor,
  sha256Bytes,
  sha256File,
  validateReviewContract,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const expectedFlags = ["--codex-attempt", "--opus-attempt", "--glm-attempt", "--gemini-attempt"];
const values = new Map();
let out = "SCORES.json";
for (let index = 0; index < argv.length; index += 2) {
  const flag = argv[index];
  const value = argv[index + 1];
  assert(value !== undefined, `${flag}: missing value`);
  assert([...expectedFlags, "--out"].includes(flag), `unexpected score argument ${flag}`);
  assert(!values.has(flag), `duplicate score argument ${flag}`);
  values.set(flag, value);
}
for (const flag of expectedFlags) assert(values.has(flag), `${flag} is required`);
if (values.has("--out")) out = values.get("--out");
assert(path.basename(out) === out, "--out must be a plain filename inside the experiment directory");

const contractCheck = validateReviewContract(here);
assert(contractCheck.errors.length === 0, `review contract validation failed: ${contractCheck.errors.join("; ")}`);
const holdout = readJson(path.join(here, "PUBLIC-HOLDOUT.json"));
const reference = readJson(path.join(here, "SEALED-REFERENCE.json"));
const atomMap = readJson(path.join(here, "SEALED-ATOM-MAP.json"));
const selected = [
  {key: "codex", attempt: parseAttempt(values.get("--codex-attempt"))},
  {key: "opus", attempt: parseAttempt(values.get("--opus-attempt"))},
  {key: "glm", attempt: parseAttempt(values.get("--glm-attempt"))},
  {key: "gemini", attempt: parseAttempt(values.get("--gemini-attempt"))}
];
const expectedRequestSha256 = sha256Bytes(requestBytes(here));
const routeResults = [];
for (const selection of selected) {
  const route = routeFor(selection.key);
  const directory = attemptDirectory(here, route, selection.attempt);
  const candidatePath = path.join(directory, "CANDIDATE.json");
  const candidateExists = fs.existsSync(candidatePath);
  const base = {
    route: route.slug,
    transport_decision: route.decision,
    evidence_tier: route.evidenceTier,
    attempt: selection.attempt,
    candidate_artifact: candidateExists ? path.relative(here, candidatePath) : null,
    candidate_sha256: null,
    route_limitations: route.evidenceTier === "REFERENCE_ONLY_UNVERIFIED" ? ["Model file-tool isolation is not mechanically verified.", "Runtime model identity is not independently attested by the transport."] : []
  };
  if (!candidateExists) {
    routeResults.push({...base, score_status: "INVALID_NO_SCORE", request_sha256: null, validation_errors: ["selected candidate missing"], metrics: null});
    continue;
  }
  const artifact = readCandidateArtifact(candidatePath);
  base.candidate_sha256 = artifact.candidate_sha256;
  if (artifact.error) {
    routeResults.push({...base, score_status: "INVALID_NO_SCORE", request_sha256: null, validation_errors: [artifact.error], metrics: null});
    continue;
  }
  const candidate = artifact.candidate;
  const identityErrors = [];
  if (candidate.valid !== true) identityErrors.push(...(candidate.validation_errors ?? ["candidate invalid"]));
  if (candidate.route !== route.slug || candidate.attempt !== selection.attempt) identityErrors.push("candidate route/attempt mismatch");
  if (candidate.evidence_tier !== route.evidenceTier) identityErrors.push("candidate evidence-tier mismatch");
  if (candidate.request_sha256 !== expectedRequestSha256) identityErrors.push("candidate request hash mismatch");
  if (identityErrors.length) {
    routeResults.push({...base, score_status: "INVALID_NO_SCORE", request_sha256: candidate.request_sha256 ?? null, validation_errors: identityErrors, metrics: null});
    continue;
  }
  let score;
  try { score = scoreResponse({response: candidate.response, holdout, reference, atomMap}); }
  catch (error) {
    routeResults.push({...base, score_status: "INVALID_NO_SCORE", request_sha256: candidate.request_sha256, validation_errors: [`scorer failure: ${error.message}`], metrics: null});
    continue;
  }
  if (!score.valid) {
    routeResults.push({...base, score_status: "INVALID_NO_SCORE", request_sha256: candidate.request_sha256, validation_errors: score.validation_errors, metrics: null});
    continue;
  }
  routeResults.push({...base, score_status: route.evidenceTier === "PRIMARY_VERIFIED" ? "SCORED_PRIMARY" : "SCORED_REFERENCE_ONLY", request_sha256: candidate.request_sha256, validation_errors: [], metrics: score.metrics});
}
const invalidRoutes = routeResults.filter(route => route.score_status === "INVALID_NO_SCORE");
const output = {
  schema_version: "prospective-residual-scores-v3",
  experiment: "prospective-residual-audit-v3",
  status: invalidRoutes.length === 0 ? "COMPLETE_WITH_TWO_PRIMARY_AND_TWO_REFERENCE_ONLY_ROUTES" : "COMPLETE_WITH_INVALID_ROUTES_RETAINED",
  primary_verified_routes: routeResults.filter(route => route.score_status === "SCORED_PRIMARY"),
  reference_only_unverified_routes: routeResults.filter(route => route.score_status === "SCORED_REFERENCE_ONLY"),
  invalid_routes: invalidRoutes,
  route_accounting: routeResults,
  limitations: [
    "Codex and Gemini scores are auxiliary references, not primary comparable scores, because their transports do not mechanically verify the source/target-only tool boundary and runtime model identity.",
    "The frozen reference contains one positive item, so no route score supports a stable model ranking."
  ]
};
writeNewFile(path.join(here, out), `${JSON.stringify(output, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: output.status, primary_routes: output.primary_verified_routes.map(route => route.route), reference_routes: output.reference_only_unverified_routes.map(route => route.route), invalid_routes: output.invalid_routes.map(route => route.route)}, null, 2)}\n`);
