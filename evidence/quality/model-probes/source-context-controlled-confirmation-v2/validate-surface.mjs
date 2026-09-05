#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes, validateAuditCandidate} from "./audit-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node validate-surface.mjs SURFACE-CANDIDATE-1.json SURFACE-CANDIDATE-2.json SURFACE-CANDIDATE-3.json");
const results = candidates.map((candidate, index) => validateAuditCandidate(
  path.resolve(candidate),
  path.join(here, `CLEAN-AUDIT-SURFACE-SHARD-${index + 1}.json`),
  "SURFACE",
  index + 1
));
const report = {
  schema_version: "source-context-controlled-confirmation-surface-candidate-validation-v2",
  status: "PASS",
  candidates: results.map((result, index) => ({shard: index + 1, candidate_sha256: result.candidate_sha256, queue_sha256: result.queue_sha256, counts: result.candidate.items.reduce((acc, item) => (acc[item.verdict] += 1, acc), {CLEAN: 0, OBJECTIVE_DEFECT: 0, UNRESOLVED: 0})}))
};
fs.writeFileSync(path.join(here, "SURFACE-CANDIDATE-VALIDATION.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
