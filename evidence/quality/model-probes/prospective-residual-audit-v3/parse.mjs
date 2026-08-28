import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {
  assert,
  assertRouteRunnable,
  attemptDirectory,
  candidateFromRaw,
  parseAttempt,
  readJson,
  sha256File,
  validateHarnessErrataArtifacts,
  validateReviewContract,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const attemptIndex = argv.indexOf("--attempt");
const outIndex = argv.indexOf("--out");
assert((argv.length === 3 || (argv.length === 5 && outIndex === 3)) && attemptIndex === 1, "usage: node parse.mjs codex|opus|glm|gemini --attempt N [--out CANDIDATE-NAME.json]");
const route = assertRouteRunnable(argv[0]);
const attempt = parseAttempt(argv[2]);
const out = outIndex === -1 ? "CANDIDATE.json" : argv[outIndex + 1];
assert(path.basename(out) === out && /^CANDIDATE(?:-[A-Z0-9-]+)?\.json$/u.test(out), "--out must be a CANDIDATE*.json filename inside the attempt directory");
const contractCheck = validateReviewContract(here);
assert(contractCheck.errors.length === 0, `review contract validation failed: ${contractCheck.errors.join("; ")}`);
const errata = readJson(path.join(here, "HARNESS-ERRATA-1.json"));
const errataArtifactErrors = validateHarnessErrataArtifacts(here, errata);
assert(errataArtifactErrors.length === 0, `preserved artifact validation failed: ${errataArtifactErrors.join("; ")}`);
const directory = attemptDirectory(here, route, attempt);
const callPath = path.join(directory, "CALL.json");
const rawPath = path.join(directory, "RAW.stdout");
const stderrPath = path.join(directory, "RAW.stderr");
assert(fs.existsSync(callPath) && fs.existsSync(rawPath) && fs.existsSync(stderrPath), "attempt raw envelope is incomplete");
const call = readJson(callPath);
assert(call.route === route.slug && call.attempt === attempt, "attempt identity mismatch");
assert(sha256File(rawPath) === call.raw_stdout_sha256 && sha256File(stderrPath) === call.raw_stderr_sha256, "attempt raw hash mismatch");
const holdout = readJson(path.join(here, "PUBLIC-HOLDOUT.json"));
const schema = readJson(path.join(here, "REVIEWER-SCHEMA.json"));
const candidate = candidateFromRaw({route, raw: fs.readFileSync(rawPath, "utf8"), holdout, schema, call});
if (!call.transport_success) candidate.validation_errors.unshift("transport did not complete successfully");
candidate.valid = candidate.validation_errors.length === 0;
const candidatePath = path.join(directory, out);
writeNewFile(candidatePath, `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: undefined}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 2;
