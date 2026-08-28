import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const queuePath = path.join(here, "AUDIT-QUEUE.json");
const expectedQueueSha256 = "f785989e8bddf8b06fda34915154b7b5bbe76022926b0e3462aede44e625e159";
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");

function parseArgs(argv) {
  if (argv.length === 0) return {out: path.join(here, "PUBLIC-HOLDOUT.json")};
  if (argv.length !== 2 || argv[0] !== "--out" || !argv[1]) {
    throw new Error("usage: node build-public-holdout.mjs [--out OUTPUT]");
  }
  return {out: path.resolve(argv[1])};
}

const args = parseArgs(process.argv.slice(2));
const queueBytes = fs.readFileSync(queuePath);
if (sha256(queueBytes) !== expectedQueueSha256) throw new Error("AUDIT-QUEUE.json frozen hash mismatch");
const queue = JSON.parse(queueBytes.toString("utf8"));
if (queue.schema_version !== "prospective-residual-audit-queue-v3" || queue.reviewer_inference_allowed !== false) throw new Error("unexpected audit queue state");
if (queue.items.length !== 40 || new Set(queue.items.map(item => item.audit_id)).size !== 40) throw new Error("expected 40 unique audit items");

const output = {
  schema_version: "prospective-residual-public-holdout-v3",
  status: "FROZEN_BEFORE_REVIEWER_INFERENCE",
  context_policy: "A_SOURCE_AND_TARGET_ONLY",
  item_count: 40,
  visible_fields: ["revision_id", "source", "target"],
  items: queue.items.map(item => ({
    revision_id: item.audit_id,
    source: item.source,
    target: item.target
  }))
};
fs.mkdirSync(path.dirname(args.out), {recursive: true});
fs.writeFileSync(args.out, `${JSON.stringify(output, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: output.status, out: args.out, items: output.item_count}, null, 2)}\n`);
