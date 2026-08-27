import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = file => JSON.parse(fs.readFileSync(path.join(here, file), "utf8"));
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(path.join(here, file))).digest("hex");
const experiment = read("EXPERIMENT.json");
for (const record of Object.values(experiment.frozen_bytes)) if (sha256(record.path) !== record.sha256) throw new Error(`${record.path} frozen hash mismatch`);
if (sha256("../controlled-mutation-ui-log-replication-v2/RESULT.json") !== experiment.run_a.result_sha256) throw new Error("Run A RESULT hash mismatch");
if (sha256("../controlled-mutation-ui-log-replication-v2/ADJUDICATION.json") !== experiment.run_a.adjudication_sha256) throw new Error("Run A adjudication hash mismatch");
for (const [route, expected] of Object.entries(experiment.run_a.candidate_sha256)) if (sha256(`../controlled-mutation-ui-log-replication-v2/CANDIDATE-${route}.json`) !== expected) throw new Error(`Run A ${route} candidate hash mismatch`);
const input = JSON.parse(fs.readFileSync(path.join(here, experiment.frozen_bytes.input.path), "utf8"));
if (JSON.stringify(input.items.map(item => item.revision_id)) !== JSON.stringify(["R001", "R002", "R003", "R004", "R005", "R006", "R007", "R008"])) throw new Error("input order mismatch");
const serialized = JSON.stringify(input);
for (const forbidden of ["mutation_id", "INJECTED_MUTATION", "SOURCE_VERIFIED_CONTROL", "/home/", "/Users/"]) if (serialized.includes(forbidden)) throw new Error(`input leaks ${forbidden}`);
const resultPath = path.join(here, "RESULT.json");
if (fs.existsSync(resultPath)) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "ui-log-repeat-b-"));
  try {
    const rebuilt = path.join(temporary, "RESULT.json");
    const analysis = spawnSync(process.execPath, [path.join(here, "analyze.mjs"), "--out", rebuilt], {encoding: "utf8"});
    if (analysis.status !== 0) throw new Error(`analysis rebuild failed: ${analysis.stderr}`);
    if (!fs.readFileSync(resultPath).equals(fs.readFileSync(rebuilt))) throw new Error("RESULT.json is not byte-identical to analysis rebuild");
    const result = read("RESULT.json");
    if (result.status !== "COMPLETE" || result.routes.length !== 4) throw new Error("result completion/route mismatch");
  } finally { fs.rmSync(temporary, {recursive: true, force: true}); }
  process.stdout.write("verified exact Run A byte reuse, Run B route artifacts and byte-identical RESULT rebuild\n");
} else process.stdout.write("verified exact Run A input/prompt/schema/reference reuse and blinding before inference\n");
