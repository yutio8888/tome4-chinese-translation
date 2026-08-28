import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";
import {
  EXPECTED_BWRAP_VERSION,
  FROZEN_FILES,
  assert,
  gitPackageLineage,
  invocationPlan,
  parseClaudeRaw,
  requestBytes,
  resolveClaudeRuntimeMaterials,
  scanOutboundBuffers,
  validateCurrentHeadLineage
} from "./runner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const positiveRaw = fs.readFileSync(path.join(here, "fixtures/PASS-OPUS-ONLY.jsonl"), "utf8");
const negativeRaw = fs.readFileSync(path.join(here, "fixtures/FAIL-NON-OPUS.jsonl"), "utf8");
const positive = parseClaudeRaw(positiveRaw);
assert(positive.errors.length === 0, `positive fixture rejected: ${positive.errors.join("; ")}`);
const negative = parseClaudeRaw(negativeRaw);
assert(negative.errors.some(error => error.includes("modelUsage keys mismatch")), "negative non-Opus fixture was accepted");

const baseEvents = positiveRaw.trim().split(/\r?\n/u).map(JSON.parse);
const resultIndex = baseEvents.findIndex(event => event.type === "result");
const initIndex = baseEvents.findIndex(event => event.type === "system" && event.subtype === "init");
const assistantIndex = baseEvents.findIndex(event => event.type === "assistant");
const userIndex = baseEvents.findIndex(event => event.type === "user");
const clone = () => structuredClone(baseEvents);
const raw = events => events.map(event => JSON.stringify(event)).join("\n");
const cases = [];
const reject = (caseId, mutate, expected) => {
  const events = clone();
  mutate(events);
  const parsed = parseClaudeRaw(raw(events));
  assert(parsed.errors.some(error => error.includes(expected)), `${caseId}: expected ${expected}; got ${parsed.errors.join("; ")}`);
  cases.push(caseId);
};

reject("MODEL_USAGE_MISSING", events => { delete events[resultIndex].modelUsage; }, "modelUsage telemetry is missing");
reject("MODEL_USAGE_NULL", events => { events[resultIndex].modelUsage = {"claude-opus-5": null}; }, "not an object");
reject("MODEL_USAGE_EMPTY", events => { events[resultIndex].modelUsage = {}; }, "modelUsage keys mismatch");
reject("MODEL_USAGE_PROVIDER", events => { events[resultIndex].modelUsage["claude-opus-5"].provider = "thirdParty"; }, "provider telemetry mismatch");
reject("RESULT_ROUTING_MODEL", events => { events[resultIndex].routing_model = "claude-haiku-4-5"; }, "global model telemetry mismatch");
reject("RESULT_MODEL_ID", events => { events[resultIndex].model_id = "claude-haiku-4-5"; }, "global model telemetry mismatch");
reject("RESULT_API_PROVIDER", events => { events[resultIndex].apiProvider = "thirdParty"; }, "global provider telemetry mismatch");
reject("RESULT_UNKNOWN_TELEMETRY", events => { events[resultIndex].fixture = 0; }, "result telemetry contains unknown fields");
reject("MODEL_USAGE_TOKEN_MISSING", events => { delete events[resultIndex].modelUsage["claude-opus-5"].inputTokens; }, "token telemetry is missing");
reject("MODEL_USAGE_TOKEN_ZERO", events => { events[resultIndex].modelUsage["claude-opus-5"].outputTokens = 0; events[resultIndex].usage.output_tokens = 0; events[resultIndex].usage.iterations[0].output_tokens = 0; }, "token telemetry is zero");
reject("ITERATIONS_MISSING", events => { delete events[resultIndex].usage.iterations; }, "usage.iterations telemetry is missing");
reject("ITERATION_TOOL", events => { events[resultIndex].usage.iterations[0].type = "tool"; }, "non-message iteration");
reject("ITERATION_MODEL", events => { events[resultIndex].usage.iterations[0].model = "claude-haiku-4-5"; }, "iterations model mismatch");
reject("ITERATION_PROVIDER", events => { events[resultIndex].usage.iterations[0].provider = "thirdParty"; }, "iterations provider mismatch");
reject("ITERATION_TOKEN_MISSING", events => { delete events[resultIndex].usage.iterations[0].input_tokens; }, "iterations token telemetry is missing");
reject("ITERATION_TOTAL_MISMATCH", events => { events[resultIndex].usage.iterations[0].input_tokens = 2; }, "input_tokens total mismatch");
reject("TERMINAL_USAGE_MISSING", events => { delete events[resultIndex].usage.input_tokens; }, "terminal usage token telemetry is missing");
reject("SUBAGENT_STATS_MISSING", events => { delete events[resultIndex].subagent_stats; }, "subagent_stats telemetry is missing");
reject("SUBAGENT_NONZERO", events => { events[resultIndex].subagent_stats.requested.foreground = 1; }, "subagent telemetry is incomplete or contains activity");
reject("SUBAGENT_UNKNOWN_FIELD", events => { events[resultIndex].subagent_stats.fixture = 0; }, "subagent telemetry is incomplete or contains activity");
reject("SUBAGENT_BY_TYPE", events => { events[resultIndex].subagent_stats.by_type = {fixture: 0}; }, "subagent telemetry is incomplete or contains activity");
reject("SERVER_TELEMETRY_MISSING", events => { delete events[resultIndex].usage.server_tool_use; }, "server_tool_use telemetry is missing");
reject("SERVER_COUNTER_EXTRA", events => { events[resultIndex].usage.server_tool_use.fixture = 0; }, "server_tool_use counters are incomplete");
reject("SERVER_USE_NONZERO", events => { events[resultIndex].usage.server_tool_use.web_search_requests = 1; }, "server tool use detected");
reject("MODEL_USAGE_SEARCH_NONZERO", events => { events[resultIndex].modelUsage["claude-opus-5"].webSearchRequests = 1; }, "server-search telemetry");
reject("ASSISTANT_USAGE_SERVER_USE", events => { events[assistantIndex].message.usage = {server_tool_use: {web_search_requests: 1}}; }, "usage contains unknown or server-tool telemetry");
reject("EXPOSED_TOOL", events => { events[initIndex].tools.push("Read"); }, "exposed tools mismatch");
reject("MCP_SERVER", events => { events[initIndex].mcp_servers.push({name: "fixture"}); }, "MCP servers");
reject("SKILL_EXPOSED", events => { events[initIndex].skills.push("fixture"); }, "skills were exposed");
reject("PLUGIN_EXPOSED", events => { events[initIndex].plugins.push("fixture"); }, "plugins were exposed");
reject("INIT_API_KEY_SOURCE", events => { events[initIndex].apiKeySource = "bedrock"; }, "API key source mismatch");
reject("INIT_UNKNOWN_TELEMETRY", events => { events[initIndex].fixture = 0; }, "init telemetry contains unknown fields");
reject("WRONG_CWD", events => { events[initIndex].cwd = "/tmp"; }, "init cwd mismatch");
reject("WRONG_INIT_MODEL", events => { events[initIndex].model = "claude-haiku-4-5"; }, "initialized model mismatch");
reject("ASSISTANT_MESSAGE_MISSING", events => { delete events[assistantIndex].message; }, "assistant message telemetry is missing");
reject("ASSISTANT_MODEL_MISSING", events => { delete events[assistantIndex].message.model; }, "assistant model mismatch");
reject("WRONG_ASSISTANT_MODEL", events => { events[assistantIndex].message.model = "claude-haiku-4-5"; }, "assistant model mismatch");
reject("ASSISTANT_ROLE", events => { events[assistantIndex].message.role = "user"; }, "assistant role mismatch");
reject("ASSISTANT_MESSAGE_TYPE_MISSING", events => { delete events[assistantIndex].message.type; }, "assistant message type mismatch");
reject("ASSISTANT_UNKNOWN_BLOCK", events => { events[assistantIndex].message.content.unshift({type: "fixture"}); }, "unknown assistant content block");
reject("ASSISTANT_TEXT_SCHEMA", events => { events[assistantIndex].message.content.unshift({type: "text"}); }, "text block schema mismatch");
reject("ASSISTANT_THINKING_SCHEMA", events => { events[assistantIndex].message.content.unshift({type: "thinking", thinking: ""}); }, "thinking block schema mismatch");
reject("DUPLICATE_STRUCTURED_OUTPUT", events => { events[assistantIndex].message.content.push(structuredClone(events[assistantIndex].message.content[0])); }, "exactly one direct identified StructuredOutput");
reject("GLOBAL_NESTED_STRUCTURED_OUTPUT", events => { events[resultIndex].fixture = structuredClone(events[assistantIndex].message.content[0]); }, "exactly one direct identified StructuredOutput");
reject("STRUCTURED_OUTPUT_OUTSIDE_MESSAGE", events => { events[assistantIndex].fixture = events[assistantIndex].message.content.pop(); }, "exactly one direct identified StructuredOutput");
reject("STRUCTURED_OUTPUT_NAME_OUTSIDE_TOOL", events => { events[resultIndex].fixture = {name: "StructuredOutput"}; }, "exactly one direct identified StructuredOutput");
reject("STRUCTURED_OUTPUT_NON_DIRECT_CALLER", events => { events[assistantIndex].message.content[0].caller = {type: "agent"}; }, "caller telemetry is missing or not direct");
reject("STRUCTURED_OUTPUT_SUBAGENT_ID", events => { events[assistantIndex].message.content[0].subagent_id = "fixture"; }, "StructuredOutput block schema mismatch");
reject("DUPLICATE_RECEIPT", events => { events[userIndex].message.content.push(structuredClone(events[userIndex].message.content[0])); }, "exactly one matching StructuredOutput receipt");
reject("HIDDEN_TOOL_USE_ID", events => { events[resultIndex].fixture = {tool_use_id: "toolu_fixture"}; }, "exactly one matching StructuredOutput receipt");
reject("HIDDEN_TOOL_USE_RESULT", events => { events[resultIndex].tool_use_result = "fixture"; }, "exactly one matching StructuredOutput receipt");
reject("RECEIPT_ROLE", events => { delete events[userIndex].message.role; }, "exactly one matching StructuredOutput receipt");
reject("RECEIPT_SCHEMA_EXTRA", events => { events[userIndex].message.content[0].fixture = true; }, "receipt content/schema is invalid");
reject("RECEIPT_ACK_MISSING", events => { delete events[userIndex].tool_use_result; }, "receipt terminal acknowledgement mismatch");
reject("RECEIPT_ACK_MISMATCH", events => { events[userIndex].tool_use_result = "different"; }, "receipt terminal acknowledgement mismatch");
reject("MISMATCHED_STRUCTURED_RESULT", events => { events[resultIndex].structured_output.classifications[0].class = "ZERO"; }, "do not match");
reject("ADVISOR_SIGNAL", events => { events.splice(resultIndex, 0, {type: "system", subtype: "advisor_start"}); }, "advisor or fallback");
reject("FALLBACK_SIGNAL", events => { events.splice(resultIndex, 0, {type: "system", subtype: "model_fallback"}); }, "advisor or fallback");
reject("PROMPT_SUGGESTION_EVENT", events => { events.splice(resultIndex, 0, {type: "prompt_suggestion", suggestion: "fixture"}); }, "prompt_suggestion signal");
reject("PROMPT_SUGGESTION_CAMEL", events => { events[resultIndex].promptSuggestion = "fixture"; }, "normalized alias/tool/server signal");
reject("PARENT_TOOL_SIGNAL", events => { events[assistantIndex].parent_tool_use_id = "parent_fixture"; }, "parent tool-use");
reject("PARENT_TOOL_CAMEL", events => { events[assistantIndex].parentToolUseId = "parent_fixture"; }, "normalized alias/tool/server signal");
reject("NESTED_PARENT_TOOL_SIGNAL", events => { events[resultIndex].fixture = {parent_tool_use_id: "parent_fixture"}; }, "parent tool-use");
reject("OTHER_TOOL", events => { events[assistantIndex].message.content.unshift({type: "tool_use", id: "other", name: "Read", input: {}}); }, "exactly one direct identified StructuredOutput");
reject("HIDDEN_TOOL_EVENT", events => { events[resultIndex].fixture = {type: "web_search", query: "fixture"}; }, "non-StructuredOutput tool signal");
reject("TOOL_EXECUTION_START", events => { events[resultIndex].fixture = {type: "tool_execution_start"}; }, "normalized alias/tool/server signal");
reject("WEB_SEARCH_START", events => { events[resultIndex].fixture = {type: "web_search_start"}; }, "normalized alias/tool/server signal");
reject("MCP_SUFFIX_FAMILY", events => { events[resultIndex].fixture = {type: "mcp_transport_started"}; }, "normalized alias/tool/server signal");
reject("HIDDEN_TOOL_KEY", events => { events[resultIndex].fixture = {toolAction: {name: "Read"}}; }, "non-StructuredOutput tool signal");
reject("HIDDEN_MODEL_FIELD", events => { events[resultIndex].fixture = {model: "claude-haiku-4-5"}; }, "global model telemetry mismatch");
reject("HIDDEN_PROVIDER_FIELD", events => { events[resultIndex].fixture = {provider: "thirdParty"}; }, "global provider telemetry mismatch");
reject("UNKNOWN_EVENT", events => { events.splice(assistantIndex, 0, {type: "fixture"}); }, "unknown event kind");
reject("ASSISTANT_ORDER", events => { events.splice(userIndex, 0, {type: "rate_limit_event"}); }, "receipt/result order is invalid");
reject("RESULT_NOT_TERMINAL", events => { events.push({type: "rate_limit_event"}); }, "result event must be terminal");
reject("STRUCTURED_OUTPUT_TELEMETRY_MISSING", events => { delete events[resultIndex].structured_output; }, "structured_output telemetry is missing");
reject("TERMINAL_RESULT_MISSING", events => { delete events[resultIndex].result; }, "terminal result telemetry is missing");
reject("STOP_REASON_MISSING", events => { delete events[resultIndex].stop_reason; }, "terminal stop reason mismatch");
reject("TERMINAL_REASON_MISSING", events => { delete events[resultIndex].terminal_reason; }, "terminal reason mismatch");
reject("TERMINAL_API_STATUS_MISSING", events => { delete events[resultIndex].api_error_status; }, "API error telemetry");
reject("TERMINAL_TURNS_MISSING", events => { delete events[resultIndex].num_turns; }, "num_turns telemetry");
reject("INIT_VERSION_MISSING", events => { delete events[initIndex].claude_code_version; }, "init version mismatch");
reject("PERMISSION_DENIALS_MISSING", events => { delete events[resultIndex].permission_denials; }, "permission-denial telemetry");

assert(scanOutboundBuffers([{label: "frozen synthetic request", bytes: requestBytes(here)}]).length === 0, "frozen synthetic request failed outbound scan");
for (const text of ["claude-opus-5", "Anthropic", "provider", "model_id", "gpt-5", "Gemini", "GLM-5"]) {
  assert(scanOutboundBuffers([{label: "fixture", bytes: text}]).some(error => error.includes("model/provider provenance")), `outbound provenance fixture accepted: ${text}`);
}
for (const text of ["/root", "/tmp/probe", "/etc/passwd", "/workspace/project", "C:\\Temp\\probe.json", "R033", "P005"]) {
  assert(scanOutboundBuffers([{label: "fixture", bytes: text}]).length > 0, `outbound path/ID fixture accepted: ${text}`);
}
for (const text of ["https://json-schema.org/draft/2020-12/schema", "https://example.invalid/root/tmp"]) {
  assert(scanOutboundBuffers([{label: "fixture", bytes: text}]).length === 0, `outbound URL fixture falsely rejected: ${text}`);
}
const materials = resolveClaudeRuntimeMaterials();
assert(materials.errors.length === 0, `runtime materials invalid: ${materials.errors.join("; ")}`);
const plan = invocationPlan(here, requestBytes(here), "/tmp/fixture-runtime", materials.claudeBinary);
assert(plan.args.includes("--tmpfs") && plan.args.includes(path.dirname(os.homedir())), "sandbox plan does not mask the host HOME parent");
assert(plan.args.includes("--bind") && plan.args.includes("/run/claude-purity"), "sandbox plan does not bind a private runtime");
const bwrapVersion = spawnSync("bwrap", ["--version"], {encoding: "utf8"});
assert(bwrapVersion.status === 0 && bwrapVersion.stdout.trim() === EXPECTED_BWRAP_VERSION, "frozen bubblewrap version mismatch");

const gitFixture = fs.mkdtempSync(path.join(os.tmpdir(), "claude-purity-git-lineage-v1-"));
try {
  const packageRoot = path.join(gitFixture, "evidence", "quality", "model-probes", "fixture-package");
  for (const name of [...FROZEN_FILES, "FROZEN-HASHES.json"]) {
    const destination = path.join(packageRoot, name);
    fs.mkdirSync(path.dirname(destination), {recursive: true});
    fs.copyFileSync(path.join(here, name), destination);
  }
  const git = args => spawnSync("git", args, {cwd: gitFixture, encoding: "utf8"});
  assert(git(["init", "-q"]).status === 0, "git lineage fixture init failed");
  assert(git(["config", "user.email", "fixture@example.invalid"]).status === 0, "git lineage fixture email failed");
  assert(git(["config", "user.name", "Fixture"]).status === 0, "git lineage fixture name failed");
  assert(git(["add", "."]).status === 0 && git(["commit", "-qm", "frozen package"]).status === 0, "git lineage fixture commit failed");
  const lineage = gitPackageLineage(packageRoot);
  assert(lineage.errors.length === 0, `git package lineage fixture failed: ${lineage.errors.join("; ")}`);
  const record = {package_git_commit: lineage.commit, package_relative_path: lineage.relative, package_git_blobs: lineage.blobs};
  assert(validateCurrentHeadLineage(packageRoot, record).length === 0, "git lineage rejected its package commit");
  fs.writeFileSync(path.join(gitFixture, "UNRELATED"), "fixture\n", {flag: "wx"});
  assert(git(["add", "UNRELATED"]).status === 0 && git(["commit", "-qm", "unrelated descendant"]).status === 0, "git lineage descendant commit failed");
  assert(validateCurrentHeadLineage(packageRoot, record).length === 0, "git lineage rejected unchanged descendant");
  fs.appendFileSync(path.join(packageRoot, "PROMPT.md"), "fixture drift\n");
  assert(git(["add", "."]).status === 0 && git(["commit", "-qm", "frozen drift"]).status === 0, "git lineage drift commit failed");
  assert(validateCurrentHeadLineage(packageRoot, record).some(error => error.includes("PROMPT.md")), "git lineage accepted a changed frozen blob");
} finally {
  assert(path.basename(gitFixture).startsWith("claude-purity-git-lineage-v1-"), "refusing unsafe fixture cleanup");
  fs.rmSync(gitFixture, {recursive: true, force: false});
}

process.stdout.write(`${JSON.stringify({status: "PASS", positive_fixtures: 1, negative_file_fixtures: 1, generated_negative_cases: cases.length, git_lineage_cases: 3}, null, 2)}\n`);
