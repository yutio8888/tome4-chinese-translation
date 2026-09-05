#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {jsonBytes} from "./audit-lib.mjs";
import {validateManipulationCandidate} from "./manipulation-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidates = process.argv.slice(2);
if (candidates.length !== 3) throw new Error("usage: node validate-manipulation-context.mjs MANIPULATION-B-CANDIDATE-1.json MANIPULATION-B-CANDIDATE-2.json MANIPULATION-B-CANDIDATE-3.json");
const results = candidates.map((candidate, offset) => validateManipulationCandidate(path.resolve(candidate), path.join(here, `MANIPULATION-B-CONTEXT-SHARD-${offset + 1}.json`), "B_CONTEXT", offset + 1));
const report = {
  schema_version: "source-context-controlled-confirmation-manipulation-context-validation-v2",
  status: "PASS_STRUCTURAL_LEAD_ATOM_MATCH_PENDING",
  candidates: results.map((value, offset) => ({shard: offset + 1, candidate_sha256: value.candidate_sha256, queue_sha256: value.queue_sha256, counts: value.candidate.items.reduce((acc, item) => (acc[item.verdict] += 1, acc), {NO_OBJECTIVE_DEFECT_VISIBLE: 0, EXACTLY_ONE_OBJECTIVE_DEFECT: 0, MULTIPLE_OR_STRUCTURALLY_INVALID: 0, UNRESOLVED: 0})}))
};
fs.writeFileSync(path.join(here, "MANIPULATION-B-CANDIDATE-VALIDATION.json"), jsonBytes(report), {flag: "wx"});
console.log(JSON.stringify(report, null, 2));
