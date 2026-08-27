import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = file => JSON.parse(fs.readFileSync(path.join(here, file), "utf8"));
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
const experiment = read("EXPERIMENT.json");

for (const record of Object.values(experiment.frozen_bytes)) {
  if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
}
for (const [label, prior] of [["Run A", experiment.run_a], ["Run B", experiment.run_b]]) {
  if (sha256(`${prior.directory}/RESULT.json`) !== prior.result_sha256) throw new Error(`${label} RESULT hash mismatch`);
  if (sha256(`${prior.directory}/ADJUDICATION.json`) !== prior.adjudication_sha256) throw new Error(`${label} adjudication hash mismatch`);
  for (const [route, expected] of Object.entries(prior.candidate_sha256)) {
    if (sha256(`${prior.directory}/CANDIDATE-${route}.json`) !== expected) throw new Error(`${label} ${route} candidate hash mismatch`);
  }
}
const input = JSON.parse(fs.readFileSync(path.join(here, experiment.frozen_bytes.input.path), "utf8"));
if (JSON.stringify(input.items.map(item => item.revision_id)) !== JSON.stringify(["R001", "R002", "R003", "R004", "R005", "R006", "R007", "R008"])) throw new Error("input order mismatch");
const serialized = JSON.stringify(input);
for (const forbidden of ["mutation_id", "INJECTED_MUTATION", "SOURCE_VERIFIED_CONTROL", "/home/", "/Users/"]) {
  if (serialized.includes(forbidden)) throw new Error(`input leaks ${forbidden}`);
}
if (fs.existsSync(path.join(here, "RESULT.json"))) throw new Error("post-inference verification is not installed yet");
process.stdout.write("verified exact Run A byte reuse, frozen Runs A/B hashes and blinding before Run C inference\n");
