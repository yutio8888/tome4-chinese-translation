import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";

const root = "/home/yun/research/tome4-agent-eval";
const dir = path.join(root, "evidence/quality/model-probes/gemini-reviewer-prompt-search-v1");
const inputPath = path.join(root, "evidence/quality/p1-batches/p1-b8-args-order-census.json");
const referencePath = path.join(root, "evidence/quality/p1-batches/p1-b8-adjudication.json");
const schemaPath = path.join(root, "evidence/quality/model-probes/cli-comparison-v1/REVIEWER-SCHEMA.json");
const variants = process.argv.slice(2);
if (!variants.length) throw new Error("pass one or more prompt filenames");

const input = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const reference = JSON.parse(fs.readFileSync(referencePath, "utf8"));
const defectIds = new Set(reference.findings.map(f => f.revision_id));
const orderedIds = input.items.map(x => x.revision_id);

for (const filename of variants) {
  const prompt = fs.readFileSync(path.join(dir, filename), "utf8") + "\n输入 JSON：\n" + JSON.stringify(input);
  const started = Date.now();
  const run = spawnSync("agy", [
    "-p", prompt,
    "--model", "gemini-3.7-flash-high",
    "--effort", "high",
    "--disable-slash-commands",
    "--output-format", "json",
    "--print-timeout", "15m",
    "--mode", "plan",
    "--json-schema", schemaPath
  ], {cwd: "/tmp", encoding: "utf8", maxBuffer: 32 * 1024 * 1024, timeout: 20 * 60 * 1000, env: {...process.env, NO_COLOR: "1"}});
  const duration = (Date.now() - started) / 1000;
  const record = {variant: filename, duration_seconds: duration, exit_status: run.status};
  try {
    const envelope = JSON.parse(run.stdout);
    const candidate = envelope.structured_output ?? JSON.parse(envelope.response);
    const ids = candidate.revisions.map(x => x.revision_id);
    const valid = ids.length === orderedIds.length && ids.every((id, i) => id === orderedIds[i]);
    const predicted = new Set(candidate.revisions.filter(x => x.observation !== "OK").map(x => x.revision_id));
    let tp = 0, fp = 0, fn = 0, tn = 0;
    for (const id of orderedIds) {
      if (defectIds.has(id) && predicted.has(id)) tp++;
      else if (!defectIds.has(id) && predicted.has(id)) fp++;
      else if (defectIds.has(id)) fn++;
      else tn++;
    }
    Object.assign(record, {
      valid, tp, fp, fn, tn,
      recall: tp / (tp + fn), precision: tp + fp ? tp / (tp + fp) : null,
      clean_false_positive_rate: fp / (fp + tn),
      predicted_defect_ids: [...predicted], usage: envelope.usage,
      response: candidate
    });
  } catch (error) {
    record.error = String(error);
    record.stdout = run.stdout;
    record.stderr = run.stderr;
  }
  const stem = filename.replace(/^PROMPT-/, "").replace(/\.md$/, "").toLowerCase();
  fs.writeFileSync(path.join(dir, `RAW-${stem}.json`), JSON.stringify(record, null, 2) + "\n");
  process.stdout.write(JSON.stringify({...record, response: undefined}) + "\n");
}
