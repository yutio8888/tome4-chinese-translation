#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, validateAuditCandidate} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node validate-reserve-context.mjs RESERVE-CONTEXT-CANDIDATE-4.json RESERVE-CONTEXT-CANDIDATE-5.json RESERVE-CONTEXT-CANDIDATE-6.json");
const results = candidates.map((candidate, offset) => {
  const shard = offset + 4;
  return validateAuditCandidate(path.resolve(candidate), path.join(here, `CLEAN-AUDIT-RESERVE-CONTEXT-SHARD-${shard}.json`), "CONTEXT", shard);
});
const report = {
  schema_version: "source-context-controlled-confirmation-reserve-context-validation-v2",
  status: "PASS",
  candidates: results.map((result, offset) => ({
    shard: offset + 4,
    candidate_sha256: result.candidate_sha256,
    queue_sha256: result.queue_sha256,
    counts: result.candidate.items.reduce((acc, item) => (acc[item.verdict] += 1, acc), {CLEAN: 0, OBJECTIVE_DEFECT: 0, UNRESOLVED: 0})
  }))
};
fs.writeFileSync(path.join(here, "RESERVE-CONTEXT-CANDIDATE-VALIDATION.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
