import fs from "node:fs";
import {spawnSync} from "node:child_process";

const [route, role] = process.argv.slice(2);
const root = "/home/yun/research/tome4-agent-eval";
const probe = `${root}/evidence/quality/model-probes`;
const schema = `${probe}/cli-comparison-v1/REVIEWER-SCHEMA.json`;

let prompt;
if (role === "reviewer") {
  prompt = fs.readFileSync(`${probe}/qwen3-8-27b-p1-b8/PROMPT.md`, "utf8")
    + "\n输入 JSON：\n"
    + fs.readFileSync(`${root}/evidence/quality/p1-batches/p1-b8-args-order-census.json`, "utf8");
} else if (role === "scout") {
  prompt = fs.readFileSync(`${probe}/qwen3-8-27b-agent-roles/SCOUT-PROMPT.md`, "utf8");
} else if (role === "executor") {
  prompt = fs.readFileSync(`${probe}/qwen3-8-27b-agent-roles/EXECUTOR-PROMPT.md`, "utf8");
} else {
  throw new Error(`unknown role: ${role}`);
}

let command;
let args;
if (route === "grok") {
  command = "grok";
  args = ["-p", prompt, "--model", "grok-4.6", "--no-subagents", "--disable-web-search", "--cwd", role === "reviewer" ? "/tmp" : root, "--output-format", "plain"];
  if (role === "reviewer") args.push("--max-turns", "1", "--tools", "", "--json-schema", fs.readFileSync(schema, "utf8"));
  if (role === "scout") args.push("--permission-mode", "plan", "--tools", "read_file,search_files,list_directory");
  if (role === "executor") args.push("--permission-mode", "acceptEdits", "--always-approve");
} else if (route === "codex") {
  command = "codex";
  args = ["exec", "-m", "gpt-5.6-sol", "-c", "model_reasoning_effort=\"high\"", "--ephemeral", "--ignore-rules", "--skip-git-repo-check", "-o", `/tmp/codex-${role}-last.txt`, "-C", role === "reviewer" ? "/tmp" : root];
  if (role === "reviewer") args.push("-s", "read-only", "--output-schema", schema);
  if (role === "scout") args.push("-s", "read-only", "--add-dir", "/home/yun/projects/t-engine4");
  if (role === "executor") args.push("--approve-for-me");
  args.push(prompt);
} else if (route === "agy") {
  command = "agy";
  args = ["-p", prompt, "--model", "gemini-3.7-flash-high", "--effort", "high", "--disable-slash-commands", "--output-format", "json", "--print-timeout", "15m"];
  if (role === "reviewer") args.push("--mode", "plan", "--json-schema", schema);
  if (role === "scout") args.push("--mode", "plan", "--add-dir", "/home/yun/projects/t-engine4");
  if (role === "executor") args.push("--mode", "accept-edits", "--dangerously-skip-permissions");
} else {
  throw new Error(`unknown route: ${route}`);
}

const started = Date.now();
const result = spawnSync(command, args, {
  cwd: role === "reviewer" ? "/tmp" : root,
  encoding: "utf8",
  maxBuffer: 32 * 1024 * 1024,
  timeout: 20 * 60 * 1000,
  env: {...process.env, NO_COLOR: "1"}
});
process.stderr.write(JSON.stringify({route, role, duration_seconds: (Date.now() - started) / 1000, status: result.status, signal: result.signal}) + "\n");
if (result.stderr) process.stderr.write(result.stderr);
if (route === "codex" && fs.existsSync(`/tmp/codex-${role}-last.txt`)) {
  process.stdout.write(fs.readFileSync(`/tmp/codex-${role}-last.txt`, "utf8"));
} else if (result.stdout && route === "agy" && role === "reviewer") {
  const envelope = JSON.parse(result.stdout);
  process.stdout.write(envelope.response ?? "");
  process.stderr.write(JSON.stringify({conversation_id: envelope.conversation_id, usage: envelope.usage, duration_seconds: envelope.duration_seconds}) + "\n");
} else if (result.stdout) {
  process.stdout.write(result.stdout);
}
if (result.error) {
  process.stderr.write(String(result.error) + "\n");
  process.exit(1);
}
process.exit(result.status ?? 1);
