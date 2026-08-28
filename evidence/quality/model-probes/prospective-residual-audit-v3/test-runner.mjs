import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  EXPECTED_MODEL_AVAILABILITY,
  EXPECTED_ROUTE_VERSIONS,
  assert,
  assertExactBundle,
  assertRouteRunnable,
  candidateFromRaw,
  createPublicBundle,
  minimalEnvironment,
  readCandidateArtifact,
  readJson,
  requestBytes,
  reserveAttemptDirectory,
  routeFor,
  scanOutboundBuffers,
  validatePreflightRecord,
  validatePublicArtifacts,
  wrapInOsSandbox,
  writeNewFile
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const fixture = readJson(path.join(here, "RUNNER-FIXTURE.json"));
const passed = [];
const run = (id, callback) => { callback(); passed.push(id); };

run("PUBLIC_HASHES_AND_LEAK_SCAN", () => {
  assert(validatePublicArtifacts(here).length === 0, "public artifact validation failed");
  assert(scanOutboundBuffers([{label: "request", bytes: requestBytes(here)}]).length === 0, "public request leak scan failed");
  assert(scanOutboundBuffers([{label: "negative fixture", bytes: "/home/example/SEALED-REFERENCE.json"}]).length > 0, "leak negative fixture was not rejected");
});

run("BUNDLE_EXACTLY_FOUR_ORDINARY_FILES", () => {
  const bundle = createPublicBundle(here);
  try { assertExactBundle(bundle); }
  finally { fs.rmSync(bundle, {recursive: true}); }
});

run("OS_SANDBOX_HIDES_RESEARCH_AND_MAPS_PUBLIC_CWD", () => {
  const bundle = createPublicBundle(here);
  try {
    const plan = wrapInOsSandbox({
      bundleDirectory: bundle,
      command: "/bin/sh",
      args: ["-c", "test \"$(pwd)\" = /mnt && test \"$(find /mnt -maxdepth 1 -type f | wc -l)\" -eq 4 && test ! -e /home/yun/research/tome4-agent-eval/evidence/quality/model-probes/prospective-residual-audit-v3/SEALED-REFERENCE.json && printf SANDBOX_OK"],
      displayArgs: ["[OFFLINE_ISOLATION_PROBE]"]
    });
    const result = spawnSync(plan.command, plan.args, {cwd: "/tmp", encoding: "utf8"});
    assert(result.status === 0 && result.stdout === "SANDBOX_OK", `OS sandbox probe failed: ${result.stderr}`);
    assert(!plan.display_args.join(" ").includes(bundle), "display arguments leaked the host bundle path");
  } finally { fs.rmSync(bundle, {recursive: true}); }
});

run("OS_SANDBOX_CLI_VERSION_SMOKE", () => {
  const bundle = createPublicBundle(here);
  try {
    for (const [command, kind, expected] of [
      ["codex", "codex", "codex-cli 0.150.1"],
      ["claude", "claude", "2.1.247 (Claude Code)"],
      ["pi", "pi", "0.84.3"],
      ["agy", "agy", "1.1.22"]
    ]) {
      const plan = wrapInOsSandbox({bundleDirectory: bundle, command, args: ["--version"], displayArgs: ["--version"]});
      const result = spawnSync(plan.command, plan.args, {cwd: "/tmp", encoding: "utf8", env: minimalEnvironment(kind, "/tmp")});
      assert(result.status === 0 && result.stdout.trim() === expected, `${command}: sandboxed version smoke failed: ${result.stderr}`);
    }
  } finally { fs.rmSync(bundle, {recursive: true}); }
});

run("REFERENCE_ONLY_ROUTES_RUNNABLE_AND_LABELED", () => {
  for (const key of ["codex", "gemini"]) {
    const route = assertRouteRunnable(key);
    assert(route.decision === "REFERENCE_ONLY_UNVERIFIED" && route.evidenceTier === "REFERENCE_ONLY_UNVERIFIED", `${key}: reference-only route was not labeled`);
  }
});

run("PREFLIGHT_ROUTE_CHECK_REQUIRED_BY_RUNNER", () => {
  const contractSha256 = "a".repeat(64);
  const packageGitCommit = "b".repeat(40);
  const valid = {
    status: "GO",
    route_check_performed: true,
    review_contract_sha256: contractSha256,
    package_git_commit: packageGitCommit,
    route_versions: structuredClone(EXPECTED_ROUTE_VERSIONS),
    model_availability: structuredClone(EXPECTED_MODEL_AVAILABILITY)
  };
  assert(validatePreflightRecord({preflight: valid, contractSha256, packageGitCommit}).length === 0, "valid preflight record was rejected");
  const bypassed = {...valid, route_check_performed: false, route_versions: {}, model_availability: {}};
  const errors = validatePreflightRecord({preflight: bypassed, contractSha256, packageGitCommit});
  assert(errors.some(error => error.includes("route check")) && errors.some(error => error.includes("route versions")) && errors.some(error => error.includes("model availability")), "missing route checks did not fail closed");
});

run("ATTEMPT_LOCK_AND_OVERWRITE_REJECTED", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "residual-runner-test-"));
  try {
    const directory = reserveAttemptDirectory(root, routeFor("opus"), 1);
    let locked = false;
    try { reserveAttemptDirectory(root, routeFor("opus"), 1); } catch { locked = true; }
    assert(locked, "attempt directory was overwritten");
    const file = path.join(directory, "CANDIDATE.json");
    writeNewFile(file, "first");
    let refused = false;
    try { writeNewFile(file, "second"); } catch { refused = true; }
    assert(refused && fs.readFileSync(file, "utf8") === "first", "candidate overwrite was not refused");
  } finally { fs.rmSync(root, {recursive: true}); }
});

run("CANDIDATE_READ_FAILURE_IS_ROUTE_LOCAL", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "residual-candidate-read-test-"));
  try {
    const malformedPath = path.join(root, "malformed.json");
    const validPath = path.join(root, "valid.json");
    writeNewFile(malformedPath, "{");
    writeNewFile(validPath, JSON.stringify({valid: true}));
    const results = [malformedPath, validPath].map(readCandidateArtifact);
    assert(results[0].candidate === null && results[0].candidate_sha256 !== null && results[0].error?.includes("candidate parse failure"), "malformed candidate did not become a local read failure");
    assert(results[1].error === null && results[1].candidate?.valid === true, "valid candidate was not readable after a neighboring malformed candidate");
  } finally { fs.rmSync(root, {recursive: true}); }
});

const holdout = readJson(path.join(here, "PUBLIC-HOLDOUT.json"));
const schema = readJson(path.join(here, "REVIEWER-SCHEMA.json"));
const fakeCall = {attempt: 1, request_sha256: "0".repeat(64), raw_stdout_sha256: "1".repeat(64), raw_stderr_sha256: "2".repeat(64)};
const fixtureResponse = {revisions: holdout.items.map(item => ({revision_id: item.revision_id, verdict: "NO_DEFECT", observation: "NO_DEFECT", evidence: "fixture"}))};
run("INVALID_PI_CANDIDATE_REJECTED", () => {
  const raw = `${JSON.stringify({type: "message_end", message: {role: "assistant", provider: "zai-standard-cn", model: "glm-5.3-flash", content: [{type: "text", text: "{bad"}]}})}\n`;
  const candidate = candidateFromRaw({route: routeFor("glm"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false, "invalid Pi candidate was accepted");
});

run("CODEX_REFERENCE_PARSER_VALID_BUT_UNVERIFIED", () => {
  const raw = [
    {type: "thread.started", thread_id: "fixture"},
    {type: "turn.started"},
    {type: "item.completed", item: {type: "agent_message", text: JSON.stringify(fixtureResponse)}},
    {type: "turn.completed", usage: {input_tokens: 1, output_tokens: 1}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("codex"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === true && candidate.evidence_tier === "REFERENCE_ONLY_UNVERIFIED", "Codex reference candidate was not accepted/labeled");
  assert(candidate.route_metadata.runtime_identity_verified === false, "Codex identity was incorrectly marked verified");
});

run("AGY_REFERENCE_PARSER_VALID_BUT_UNVERIFIED", () => {
  const raw = JSON.stringify({status: "SUCCESS", structured_output: fixtureResponse, response: JSON.stringify(fixtureResponse), json_schema: schema});
  const candidate = candidateFromRaw({route: routeFor("gemini"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === true && candidate.evidence_tier === "REFERENCE_ONLY_UNVERIFIED", "agy reference candidate was not accepted/labeled");
  assert(candidate.route_metadata.runtime_identity_verified === false && candidate.route_metadata.tool_telemetry_complete === false, "agy limitations were not retained");
});

run("CODEX_TOOL_ITEM_REFERENCE_REJECTED", () => {
  const raw = [
    {type: "thread.started", thread_id: "fixture"},
    {type: "turn.started"},
    {type: "item.completed", item: {type: "command_execution", command: "pwd"}},
    {type: "item.completed", item: {type: "agent_message", text: JSON.stringify(fixtureResponse)}},
    {type: "turn.completed", usage: {input_tokens: 1, output_tokens: 1}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("codex"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.some(error => error.includes("non-review item")), "Codex tool item was not rejected");
});

run("CODEX_STARTED_TOOL_ITEM_REFERENCE_REJECTED", () => {
  const raw = [
    {type: "thread.started", thread_id: "fixture"},
    {type: "turn.started"},
    {type: "item.started", item: {type: "command_execution", command: "pwd"}},
    {type: "item.completed", item: {type: "agent_message", text: JSON.stringify(fixtureResponse)}},
    {type: "turn.completed", usage: {input_tokens: 1, output_tokens: 1}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("codex"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.some(error => error.includes("non-review item")), "Codex started tool item was not rejected");
});

for (const [caseId, explicitEvent] of [
  ["CODEX_TOP_LEVEL_TOOL_CALL_REJECTED", {type: "tool_call", name: "shell"}],
  ["CODEX_TOP_LEVEL_WEB_SEARCH_REJECTED", {type: "web_search", query: "fixture"}],
  ["CODEX_TOP_LEVEL_MCP_CALL_REJECTED", {type: "mcp_call", server: "fixture"}]
]) {
  run(caseId, () => {
    const raw = [
      {type: "thread.started", thread_id: "fixture"},
      {type: "turn.started"},
      explicitEvent,
      {type: "item.completed", item: {type: "agent_message", text: JSON.stringify(fixtureResponse)}},
      {type: "turn.completed", usage: {input_tokens: 1, output_tokens: 1}}
    ].map(event => JSON.stringify(event)).join("\n");
    const candidate = candidateFromRaw({route: routeFor("codex"), raw, holdout, schema, call: fakeCall});
    assert(candidate.valid === false && candidate.validation_errors.some(error => error.includes("explicit top-level tool signal")), `${caseId}: explicit Codex top-level signal was not rejected`);
  });
}

run("CLAUDE_TOP_LEVEL_TOOL_RESULT_REJECTED", () => {
  const raw = [
    {type: "system", subtype: "init", tools: ["StructuredOutput"], mcp_servers: [], model: "claude-opus-5", permissionMode: "plan", slash_commands: []},
    {type: "assistant", message: {model: "claude-opus-5", content: [{type: "tool_use", name: "StructuredOutput", input: fixtureResponse}]}, parent_tool_use_id: null},
    {type: "tool_result", name: "Read"},
    {type: "result", subtype: "success", is_error: false, structured_output: fixtureResponse, modelUsage: {"claude-opus-5": {}}, usage: {server_tool_use: {web_search_requests: 0}}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("opus"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.includes("Claude non-StructuredOutput tool signal detected"), "Claude top-level tool result was not rejected");
});

run("AGY_SCHEMA_MISMATCH_REFERENCE_REJECTED", () => {
  const wrongSchema = structuredClone(schema);
  wrongSchema.properties.revisions.maxItems = 39;
  const raw = JSON.stringify({status: "SUCCESS", structured_output: fixtureResponse, response: JSON.stringify(fixtureResponse), json_schema: wrongSchema});
  const candidate = candidateFromRaw({route: routeFor("gemini"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.includes("agy returned schema mismatch"), "agy schema mismatch was not rejected");
});

run("AGY_NONARRAY_TOOL_CALLS_REJECTED", () => {
  const raw = JSON.stringify({status: "SUCCESS", structured_output: fixtureResponse, response: JSON.stringify(fixtureResponse), json_schema: schema, tool_calls: {name: "Read"}});
  const candidate = candidateFromRaw({route: routeFor("gemini"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.includes("agy explicit tool calls detected"), "agy non-array tool_calls was not rejected");
});

run("WRONG_ORDER_CANDIDATE_REJECTED", () => {
  const revisions = holdout.items.map(item => ({revision_id: item.revision_id, verdict: "NO_DEFECT", observation: "NO_DEFECT", evidence: "fixture"}));
  [revisions[0], revisions[1]] = [revisions[1], revisions[0]];
  const raw = `${JSON.stringify({type: "message_end", message: {role: "assistant", provider: "zai-standard-cn", model: "glm-5.3-flash", content: [{type: "text", text: JSON.stringify({revisions})}]}})}\n`;
  const candidate = candidateFromRaw({route: routeFor("glm"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false, "wrong-order candidate was accepted");
});

assert(JSON.stringify(passed.sort()) === JSON.stringify(fixture.cases.map(item => item.case_id).sort()), "runner fixture coverage mismatch");
process.stdout.write(`${JSON.stringify({status: "PASS", fixture_cases: passed.length}, null, 2)}\n`);
