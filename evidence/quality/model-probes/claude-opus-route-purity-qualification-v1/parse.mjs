import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {
  EXPERIMENT,
  REQUIRED_ENVIRONMENT,
  ROUTE_SLUG,
  SANDBOX_AUTH_POLICY,
  assert,
  assertOrdinaryFile,
  attemptDirectory,
  candidateFromRaw,
  invocationPlan,
  parseAttempt,
  readJson,
  requestBytes,
  resolveClaudeRuntimeMaterials,
  sha256Bytes,
  sha256File,
  validateFrozenArtifacts,
  validatePreflight,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
assert(argv.length === 2 && argv[0] === "--attempt", "usage: node parse.mjs --attempt N");
const attempt = parseAttempt(argv[1]);
const directory = attemptDirectory(here, attempt);
assert(fs.existsSync(directory), "attempt directory missing");
const directoryStat = fs.lstatSync(directory);
assert(directoryStat.isDirectory() && !directoryStat.isSymbolicLink(), "attempt path is not an ordinary non-symlink directory");
const callPath = path.join(directory, "CALL.json");
const stdoutPath = path.join(directory, "RAW.stdout");
const stderrPath = path.join(directory, "RAW.stderr");
const preflightPath = path.join(here, "PREFLIGHT.json");
const frozenPath = path.join(here, "FROZEN-HASHES.json");
for (const file of [callPath, stdoutPath, stderrPath, preflightPath, frozenPath]) assertOrdinaryFile(file);
assert(!fs.existsSync(path.join(directory, "CANDIDATE.json")), "CANDIDATE.json already exists; candidates are immutable");

const frozen = validateFrozenArtifacts(here);
assert(frozen.errors.length === 0, `frozen artifacts invalid: ${frozen.errors.join("; ")}`);
const preflight = readJson(preflightPath);
const preflightErrors = validatePreflight(here, preflight);
assert(preflightErrors.length === 0, `PREFLIGHT invalid: ${preflightErrors.join("; ")}`);
const call = readJson(callPath);
const requiredCallKeys = [
  "schema_version", "experiment", "route", "attempt", "started_at_utc", "duration_seconds",
  "command", "arguments", "environment_policy", "required_environment_names", "sandbox_auth_policy",
  "package_git_commit", "package_git_tree_oid", "package_git_blobs", "bundle_files", "request_sha256",
  "input_sha256", "prompt_sha256", "schema_sha256", "frozen_hash_manifest_sha256", "preflight_sha256",
  "claude_binary_sha256", "raw_stdout", "raw_stdout_sha256", "raw_stderr", "raw_stderr_sha256",
  "exit_status", "signal", "spawn_error", "transport_success"
];
assert(call !== null && typeof call === "object" && !Array.isArray(call), "CALL is not an object");
assert(JSON.stringify(Object.keys(call).sort()) === JSON.stringify(requiredCallKeys.sort()), "CALL field set mismatch");
assert(call.schema_version === "claude-opus-route-purity-call-v1" && call.experiment === EXPERIMENT && call.route === ROUTE_SLUG, "CALL identity mismatch");
assert(call.attempt === attempt, "CALL attempt mismatch");
assert(typeof call.started_at_utc === "string" && !Number.isNaN(Date.parse(call.started_at_utc)), "CALL start time invalid");
assert(typeof call.duration_seconds === "number" && Number.isFinite(call.duration_seconds) && call.duration_seconds >= 0, "CALL duration invalid");
assert(call.command === "bwrap", "CALL command mismatch");
assert(call.environment_policy === "fixed sanitized environment; entire host HOME masked; private ephemeral runtime; no environment values, credentials or local paths recorded", "CALL environment policy mismatch");
assert(JSON.stringify(call.required_environment_names) === JSON.stringify(Object.keys(REQUIRED_ENVIRONMENT).sort()), "CALL required environment names mismatch");
assert(call.sandbox_auth_policy === SANDBOX_AUTH_POLICY, "CALL sandbox auth policy mismatch");
assert(call.package_git_commit === preflight.package_git_commit && call.package_git_tree_oid === preflight.package_git_tree_oid, "CALL package lineage mismatch");
assert(JSON.stringify(call.package_git_blobs) === JSON.stringify(preflight.package_git_blobs), "CALL package blob lineage mismatch");
assert(JSON.stringify(call.bundle_files) === JSON.stringify(["PROMPT.md", "INPUT.json", "SCHEMA.json"]), "CALL bundle file set mismatch");
assert(call.request_sha256 === sha256Bytes(requestBytes(here)), "CALL request hash mismatch");
assert(call.input_sha256 === sha256File(path.join(here, "INPUT.json")), "CALL input hash mismatch");
assert(call.prompt_sha256 === sha256File(path.join(here, "PROMPT.md")), "CALL prompt hash mismatch");
assert(call.schema_sha256 === sha256File(path.join(here, "SCHEMA.json")), "CALL schema hash mismatch");
assert(call.frozen_hash_manifest_sha256 === sha256File(frozenPath) && call.frozen_hash_manifest_sha256 === preflight.frozen_hash_manifest_sha256, "CALL frozen manifest lineage mismatch");
assert(call.preflight_sha256 === sha256File(preflightPath), "CALL PREFLIGHT hash mismatch");
assert(call.claude_binary_sha256 === preflight.claude_binary_sha256, "CALL Claude binary lineage mismatch");
const materials = resolveClaudeRuntimeMaterials();
assert(materials.errors.length === 0 && materials.claudeBinarySha256 === call.claude_binary_sha256, "current Claude runtime does not match CALL lineage");
const expectedDisplay = invocationPlan(here, requestBytes(here), "/tmp/lineage-only-runtime", materials.claudeBinary).display_args;
assert(JSON.stringify(call.arguments) === JSON.stringify(expectedDisplay), "CALL displayed argument contract mismatch");
assert(call.transport_success === true && call.exit_status === 0 && call.signal === null && call.spawn_error === null, "transport did not succeed; preserve RAW/CALL and use a new attempt for retry");
assert(call.raw_stdout === "RAW.stdout" && call.raw_stderr === "RAW.stderr", "CALL RAW path contract mismatch");
assert(call.raw_stdout_sha256 === sha256File(stdoutPath), "RAW.stdout hash mismatch");
assert(call.raw_stderr_sha256 === sha256File(stderrPath), "RAW.stderr hash mismatch");
const candidate = candidateFromRaw({raw: fs.readFileSync(stdoutPath, "utf8"), call});
writeNewFile(path.join(directory, "CANDIDATE.json"), `${JSON.stringify(candidate, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...candidate, response: candidate.response ? "[SYNTHETIC_RESPONSE]" : null}, null, 2)}\n`);
if (!candidate.valid) process.exitCode = 3;
