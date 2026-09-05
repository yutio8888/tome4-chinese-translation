#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const parentBytes = fs.readFileSync(path.join(here, "CLEAN-AUDIT-SURFACE-QUEUE.json"));
const parent = JSON.parse(parentBytes);
if (parent.items.length !== 120) throw new Error("surface parent queue must contain 120 items");
const report = {schema_version: "source-context-controlled-confirmation-audit-shard-report-v2", status: "PASS", parent_queue_sha256: sha256(parentBytes), shards: []};
for (let shard = 1; shard <= 3; shard += 1) {
  const items = parent.items.slice((shard - 1) * 40, shard * 40);
  const queue = {
    schema_version: "source-context-controlled-confirmation-clean-audit-surface-shard-v2",
    status: "FROZEN_SURFACE_ONLY_CONTEXT_WITHHELD",
    pass: "SURFACE",
    shard,
    parent_queue_sha256: sha256(parentBytes),
    instructions: [
      "Review all 40 source/target pairs in order using only visible bilingual evidence.",
      "CLEAN means no objective material translation or structural defect is decidable from source and target.",
      "OBJECTIVE_DEFECT requires one or more exact target spans and concise objective claims.",
      "UNRESOLVED is only for a material question that cannot be decided from source/target alone; explain the limitation.",
      "Do not infer fixed-source behavior, request repository context, propose style-only rewrites, or omit an item."
    ],
    items
  };
  const name = `CLEAN-AUDIT-SURFACE-SHARD-${shard}.json`;
  fs.writeFileSync(path.join(here, name), jsonBytes(queue), {flag: "wx"});
  report.shards.push({shard, file: name, sha256: sha256(jsonBytes(queue)), first_id: items[0].audit_id, last_id: items.at(-1).audit_id, count: items.length});
}
fs.writeFileSync(path.join(here, "AUDIT-SHARD-BUILD-REPORT.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
