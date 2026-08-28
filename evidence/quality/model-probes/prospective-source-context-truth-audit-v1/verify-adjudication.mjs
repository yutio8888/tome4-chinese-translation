#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {verifyFinalAdjudication} from "./candidate-validation.mjs";

const argv = process.argv.slice(2);
const index = argv.indexOf("--audit-dir");
if (index === -1 || !argv[index + 1]) throw new Error("usage: node verify-adjudication.mjs --audit-dir DIR");
const directory = path.resolve(argv[index + 1]);
const read = name => fs.readFileSync(path.join(directory, name));
const adjudication = verifyFinalAdjudication({
  auditQueueBytes: read("AUDIT-QUEUE.json"),
  surfaceQueueBytes: [1, 2, 3].map(shard => read(`SURFACE-QUEUE-${shard}.json`)),
  contextQueueBytes: [1, 2, 3].map(shard => read(`CONTEXT-QUEUE-${shard}.json`)),
  surfaceCandidateBytes: [1, 2, 3].map(shard => read(`SURFACE-CANDIDATE-${shard}.json`)),
  contextCandidateBytes: [1, 2, 3].map(shard => read(`CONTEXT-CANDIDATE-${shard}.json`)),
  adjudicationBytes: read("FINAL-ADJUDICATION.json")
});
process.stdout.write(`${JSON.stringify({status: "PASS", items: adjudication.items.length}, null, 2)}\n`);
