import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";

const root = "/home/yun/research/tome4-agent-eval";
const outDir = path.join(root, "evidence/quality/model-probes/gemini-reviewer-holdout-b7-v1");
const promptDir = path.join(root, "evidence/quality/model-probes/gemini-reviewer-prompt-search-v1");
const input = JSON.parse(fs.readFileSync(path.join(root, "evidence/quality/p1-batches/p1-b7-args-order.json"), "utf8"));
const reference = JSON.parse(fs.readFileSync(path.join(root, "evidence/quality/p1-batches/p1-b7-s2-verification.json"), "utf8"));
const schema = path.join(outDir, "REVIEWER-SCHEMA-24.json");
const variants = {
  baseline: path.join(root, "evidence/quality/model-probes/qwen3-8-27b-p1-b8/PROMPT.md"),
  A: path.join(promptDir, "PROMPT-A-SEMANTIC-SLOTS.md"),
  B: path.join(promptDir, "PROMPT-B-TWO-PASS-RECALL.md"),
  C: path.join(promptDir, "PROMPT-C-CLAIM-ATOMS.md"),
  D: path.join(promptDir, "PROMPT-D-RELATION-LEDGER.md")
};
const requested = process.argv.slice(2);
if (!requested.length || requested.some(x => !variants[x])) throw new Error("pass variants from: baseline A B C D");
const orderedIds = input.items.map(x => x.revision_id);
const defectIds = new Set(reference.items.filter(x => (x.verdict ?? x.decision) === "defect").map(x => x.revision_id));

for (const name of requested) {
  const originalPrompt = fs.readFileSync(variants[name], "utf8");
  const prompt = originalPrompt.replaceAll("21 条", "24 条").replaceAll("全部 21 条", "全部 24 条")
    + "\n输入 JSON：\n" + JSON.stringify(input);
  const started = Date.now();
  const run = spawnSync("agy", ["-p", prompt, "--model", "gemini-3.7-flash-high", "--effort", "high",
    "--disable-slash-commands", "--output-format", "json", "--print-timeout", "15m", "--mode", "plan", "--json-schema", schema],
    {cwd: "/tmp", encoding: "utf8", maxBuffer: 32 * 1024 * 1024, timeout: 20 * 60 * 1000, env: {...process.env, NO_COLOR: "1"}});
  const result = {variant: name, duration_seconds: (Date.now() - started) / 1000, exit_status: run.status};
  try {
    const envelope = JSON.parse(run.stdout);
    const candidate = envelope.structured_output ?? JSON.parse(envelope.response);
    const ids = candidate.revisions.map(x => x.revision_id);
    const predicted = new Set(candidate.revisions.filter(x => x.observation !== "OK").map(x => x.revision_id));
    let tp=0, fp=0, fn=0, tn=0;
    for (const id of orderedIds) {
      if (defectIds.has(id) && predicted.has(id)) tp++;
      else if (!defectIds.has(id) && predicted.has(id)) fp++;
      else if (defectIds.has(id)) fn++;
      else tn++;
    }
    Object.assign(result, {valid: ids.length === 24 && ids.every((id,i) => id === orderedIds[i]), tp,fp,fn,tn,
      recall: tp/(tp+fn), precision: tp+fp ? tp/(tp+fp) : null, clean_false_positive_rate: fp/(fp+tn),
      predicted_defect_ids:[...predicted], usage:envelope.usage, response:candidate});
  } catch (error) {
    Object.assign(result, {valid:false, error:String(error), stdout:run.stdout, stderr:run.stderr});
  }
  fs.writeFileSync(path.join(outDir, `RAW-${name}.json`), JSON.stringify(result,null,2)+"\n");
  process.stdout.write(JSON.stringify({...result,response:undefined})+"\n");
}
