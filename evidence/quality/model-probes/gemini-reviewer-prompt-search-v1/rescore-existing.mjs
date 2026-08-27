import fs from "node:fs";
import path from "node:path";

const root = "/home/yun/research/tome4-agent-eval";
const dir = path.join(root, "evidence/quality/model-probes/gemini-reviewer-prompt-search-v1");
const input = JSON.parse(fs.readFileSync(path.join(root, "evidence/quality/p1-batches/p1-b8-args-order-census.json"), "utf8"));
const reference = JSON.parse(fs.readFileSync(path.join(root, "evidence/quality/p1-batches/p1-b8-adjudication.json"), "utf8"));
const orderedIds = input.items.map(x => x.revision_id);
const defectIds = new Set(reference.findings.map(x => x.revision_id));

for (const filename of fs.readdirSync(dir).filter(x => x.startsWith("RAW-") && x.endsWith(".json"))) {
  const old = JSON.parse(fs.readFileSync(path.join(dir, filename), "utf8"));
  if (!old.stdout) continue;
  const envelope = JSON.parse(old.stdout);
  const candidate = envelope.structured_output;
  const ids = candidate.revisions.map(x => x.revision_id);
  const predicted = new Set(candidate.revisions.filter(x => x.observation !== "OK").map(x => x.revision_id));
  let tp = 0, fp = 0, fn = 0, tn = 0;
  for (const id of orderedIds) {
    if (defectIds.has(id) && predicted.has(id)) tp++;
    else if (!defectIds.has(id) && predicted.has(id)) fp++;
    else if (defectIds.has(id)) fn++;
    else tn++;
  }
  const scored = {
    variant: old.variant,
    duration_seconds: old.duration_seconds,
    exit_status: old.exit_status,
    valid: ids.length === orderedIds.length && ids.every((id, i) => id === orderedIds[i]),
    tp, fp, fn, tn,
    recall: tp / (tp + fn),
    precision: tp + fp ? tp / (tp + fp) : null,
    clean_false_positive_rate: fp / (fp + tn),
    predicted_defect_ids: [...predicted],
    usage: envelope.usage,
    response: candidate
  };
  fs.writeFileSync(path.join(dir, filename), JSON.stringify(scored, null, 2) + "\n");
  process.stdout.write(JSON.stringify({...scored, response: undefined}) + "\n");
}
