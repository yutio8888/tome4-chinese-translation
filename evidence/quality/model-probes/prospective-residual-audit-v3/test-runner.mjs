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
  createRouteRuntime,
  minimalEnvironment,
  readCandidateArtifact,
  readJson,
  removeRouteRuntime,
  requestBytes,
  reserveAttemptDirectory,
  routeFor,
  runtimeEnvironment,
  scanOutboundBuffers,
  sha256File,
  validateHarnessErrataArtifacts,
  validatePreflightRecord,
  validatePublicArtifacts,
  validateRetryPreflightRecord,
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

run("RETRY_RUNTIME_MASKS_HOME_AND_IS_WRITABLE", () => {
  const bundle = createPublicBundle(here);
  const runtime = createRouteRuntime(routeFor("glm"));
  try {
    const plan = wrapInOsSandbox({
      bundleDirectory: bundle,
      runtimeDirectory: runtime,
      maskUserHome: true,
      command: "/bin/sh",
      args: ["-c", "test ! -e /home/yun/.pi && test -f /tmp/route-runtime/pi/auth.json && test -f /tmp/route-runtime/pi/models.json && touch /tmp/route-runtime/pi/write-probe && printf RETRY_SANDBOX_OK"],
      displayArgs: ["[RETRY_ISOLATION_PROBE]"]
    });
    const result = spawnSync(plan.command, plan.args, {cwd: "/tmp", encoding: "utf8", env: runtimeEnvironment("pi")});
    assert(result.status === 0 && result.stdout === "RETRY_SANDBOX_OK", `retry sandbox probe failed: ${result.stderr}`);
    assert(fs.existsSync(path.join(runtime, "pi", "write-probe")), "route runtime was not writable");
    assert(!plan.display_args.join(" ").includes(runtime), "display arguments leaked the host runtime path");
  } finally {
    fs.rmSync(bundle, {recursive: true});
    removeRouteRuntime(runtime);
  }
});

run("ROUTE_RUNTIMES_ARE_MINIMAL", () => {
  const codexRuntime = createRouteRuntime(routeFor("codex"));
  const piRuntime = createRouteRuntime(routeFor("glm"));
  try {
    assert(JSON.stringify(fs.readdirSync(codexRuntime).sort()) === JSON.stringify(["codex", "xdg"]), "Codex runtime root is not minimal");
    assert(JSON.stringify(fs.readdirSync(path.join(codexRuntime, "codex")).sort()) === JSON.stringify(["auth.json"]), "Codex runtime contains non-auth files");
    assert(JSON.stringify(fs.readdirSync(piRuntime).sort()) === JSON.stringify(["pi", "xdg"]), "Pi runtime root is not minimal");
    assert(JSON.stringify(fs.readdirSync(path.join(piRuntime, "pi")).sort()) === JSON.stringify(["auth.json", "models.json"]), "Pi runtime contains unexpected files");
    const piAuth = readJson(path.join(piRuntime, "pi", "auth.json"));
    const piModels = readJson(path.join(piRuntime, "pi", "models.json"));
    assert(JSON.stringify(Object.keys(piAuth)) === JSON.stringify(["zai-standard-cn"]), "Pi runtime auth is not provider-minimal");
    assert(JSON.stringify(Object.keys(piModels.providers)) === JSON.stringify(["zai-standard-cn"]), "Pi runtime models are not provider-minimal");
    assert(!Object.hasOwn(piModels.providers["zai-standard-cn"], "apiKey"), "Pi runtime model definition retained an apiKey field");
    assert(JSON.stringify(piModels.providers["zai-standard-cn"].models.map(model => model.id)) === JSON.stringify(["glm-5.3-flash"]), "Pi runtime model list is not route-minimal");
  } finally {
    removeRouteRuntime(codexRuntime);
    removeRouteRuntime(piRuntime);
  }
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

run("RETRY_PREFLIGHT_ALLOWED_ATTEMPTS_REQUIRED", () => {
  const contractSha256 = "c".repeat(64);
  const errataSha256 = "d".repeat(64);
  const packageGitCommit = "e".repeat(40);
  const valid = {
    schema_version: "prospective-residual-retry-preflight-v3-1",
    status: "GO",
    route_check_performed: true,
    review_contract_sha256: contractSha256,
    harness_errata_sha256: errataSha256,
    package_git_commit: packageGitCommit,
    route_versions: structuredClone(EXPECTED_ROUTE_VERSIONS),
    model_availability: structuredClone(EXPECTED_MODEL_AVAILABILITY),
    allowed_route_attempts: {codex: 2, glm: 3}
  };
  assert(validateRetryPreflightRecord({preflight: valid, contractSha256, errataSha256, packageGitCommit}).length === 0, "valid retry preflight was rejected");
  const broadened = {...valid, allowed_route_attempts: {codex: 2, opus: 2, glm: 3, gemini: 2}};
  assert(validateRetryPreflightRecord({preflight: broadened, contractSha256, errataSha256, packageGitCommit}).some(error => error.includes("allowed attempts")), "broadened retry preflight was accepted");
});

run("ERRATA_ARTIFACT_CONSUMER_HASH_LOCK", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "residual-errata-lock-test-"));
  try {
    const initial = path.join(root, "PREFLIGHT.json");
    const raw = path.join(root, "RAW.stdout");
    writeNewFile(initial, "initial");
    writeNewFile(raw, "raw");
    const errata = {
      schema_version: "prospective-residual-harness-errata-v3-1",
      status: "FROZEN_BEFORE_RETRY_INFERENCE",
      initial_preflight: {logical_path: "PREFLIGHT.json", sha256: sha256File(initial)},
      preserved_artifacts: [{logical_path: "RAW.stdout", sha256: sha256File(raw)}]
    };
    assert(validateHarnessErrataArtifacts(root, errata).length === 0, "valid errata artifact bindings were rejected");
    fs.appendFileSync(raw, "drift");
    assert(validateHarnessErrataArtifacts(root, errata).some(error => error.includes("hash mismatch")), "consumer did not reject preserved artifact drift");
  } finally { fs.rmSync(root, {recursive: true}); }
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

run("CLAUDE_STRUCTURED_OUTPUT_RESULT_ACCEPTED", () => {
  const toolUseId = "toolu_fixture";
  const raw = [
    {type: "system", subtype: "init", tools: ["StructuredOutput"], mcp_servers: [], model: "claude-opus-5", permissionMode: "plan", slash_commands: []},
    {type: "assistant", message: {model: "claude-opus-5", content: [{type: "tool_use", id: toolUseId, name: "StructuredOutput", input: fixtureResponse}]}, parent_tool_use_id: null},
    {type: "user", message: {content: [{type: "tool_result", tool_use_id: toolUseId, content: "Structured output submitted"}]}, parent_tool_use_id: null},
    {type: "result", subtype: "success", is_error: false, structured_output: fixtureResponse, modelUsage: {"claude-opus-5": {}}, usage: {server_tool_use: {web_search_requests: 0}}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("opus"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === true, `StructuredOutput result was rejected: ${candidate.validation_errors.join("; ")}`);
});

run("CLAUDE_STRUCTURED_RESULT_NESTED_TOOL_REJECTED", () => {
  const toolUseId = "toolu_fixture_nested";
  const raw = [
    {type: "system", subtype: "init", tools: ["StructuredOutput"], mcp_servers: [], model: "claude-opus-5", permissionMode: "plan", slash_commands: []},
    {type: "assistant", message: {model: "claude-opus-5", content: [{type: "tool_use", id: toolUseId, name: "StructuredOutput", input: fixtureResponse}]}, parent_tool_use_id: null},
    {type: "user", message: {content: [{type: "tool_result", tool_use_id: toolUseId, content: [{type: "tool_use", name: "Read"}]}]}, parent_tool_use_id: null},
    {type: "result", subtype: "success", is_error: false, structured_output: fixtureResponse, modelUsage: {"claude-opus-5": {}}, usage: {server_tool_use: {web_search_requests: 0}}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("opus"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.includes("Claude non-StructuredOutput tool signal detected"), "nested tool in StructuredOutput result was accepted");
});

run("CLAUDE_DUPLICATE_STRUCTURED_RESULTS_REJECTED", () => {
  const toolUseId = "toolu_fixture_duplicate";
  const resultBlock = {type: "tool_result", tool_use_id: toolUseId, content: "Structured output submitted"};
  const raw = [
    {type: "system", subtype: "init", tools: ["StructuredOutput"], mcp_servers: [], model: "claude-opus-5", permissionMode: "plan", slash_commands: []},
    {type: "assistant", message: {model: "claude-opus-5", content: [{type: "tool_use", id: toolUseId, name: "StructuredOutput", input: fixtureResponse}]}, parent_tool_use_id: null},
    {type: "user", message: {content: [resultBlock, resultBlock]}, parent_tool_use_id: null},
    {type: "result", subtype: "success", is_error: false, structured_output: fixtureResponse, modelUsage: {"claude-opus-5": {}}, usage: {server_tool_use: {web_search_requests: 0}}}
  ].map(event => JSON.stringify(event)).join("\n");
  const candidate = candidateFromRaw({route: routeFor("opus"), raw, holdout, schema, call: fakeCall});
  assert(candidate.valid === false && candidate.validation_errors.includes("Claude must return exactly one matching StructuredOutput result"), "duplicate StructuredOutput results were accepted");
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
