#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {jsonBytes} from "./build-target-queue.mjs";
import {releaseContextFromValues} from "./candidate-validation.mjs";

const argv = process.argv.slice(2);
const args = {};
for (let index = 0; index < argv.length; index += 2) {
  const flag = argv[index]; const value = argv[index + 1];
  if (!value || !["--queue-dir", "--surface-candidate", "--surface-candidate-sha256", "--shard", "--out"].includes(flag)) throw new Error("usage: node release-context.mjs --queue-dir DIR --surface-candidate FILE --surface-candidate-sha256 SHA256 --shard 1|2|3 --out FILE");
  args[flag.slice(2).replace(/-([a-z])/gu, (_match, letter) => letter.toUpperCase())] = value;
}
const shard = Number(args.shard);
if (!args.queueDir || !args.surfaceCandidate || !args.surfaceCandidateSha256 || !args.out || ![1, 2, 3].includes(shard)) throw new Error("all release-context arguments are required");
const read = file => JSON.parse(fs.readFileSync(file, "utf8"));
const auditQueue = read(path.join(path.resolve(args.queueDir), "AUDIT-QUEUE.json"));
const surfaceQueue = read(path.join(path.resolve(args.queueDir), `SURFACE-QUEUE-${shard}.json`));
const candidateBytes = fs.readFileSync(path.resolve(args.surfaceCandidate));
const context = releaseContextFromValues({auditQueue, surfaceQueue, candidateBytes, frozenSha256: args.surfaceCandidateSha256, expectedCount: 40});
fs.writeFileSync(path.resolve(args.out), jsonBytes(context));
process.stdout.write(`${JSON.stringify({status: context.status, shard_id: shard, surface_candidate_sha256: context.surface_candidate_sha256}, null, 2)}\n`);
