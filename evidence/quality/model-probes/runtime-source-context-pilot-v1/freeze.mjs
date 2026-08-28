import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const output = path.join(here, "FROZEN-HASHES.json");
if (fs.existsSync(output)) throw new Error("refusing to overwrite FROZEN-HASHES.json");
const forbidden = fs.readdirSync(here).filter(name => /^(?:RAW|CANDIDATE|FAILURE)-[AB]-run/.test(name));
if (forbidden.length) throw new Error("cannot freeze after inference artifacts exist");
const files = [
  "ADJUDICATION-SCHEMA.json",
  "CONTEXTS.json",
  "DESIGN-SPECS.json",
  "EXPERIMENT.json",
  "HOLDOUT-A.json",
  "HOLDOUT-B.json",
  "MANIFEST-SCHEMA.json",
  "MANIFEST.json",
  "PREFLIGHT-FIXTURES.json",
  "PROMPT.md",
  "REFERENCE.json",
  "REVIEWER-SCHEMA.json",
  "ROUTE-PREFLIGHT.json",
  "SAMPLING.json",
  "SCORER-FIXTURES.json",
  "SOURCE-CONTROLS.json",
  "SOURCE-VERIFICATION.json",
  "build.mjs",
  "freeze.mjs",
  "preflight.mjs",
  "run.mjs",
  "score.mjs"
];
const sha256 = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
for (const name of files) if (!fs.existsSync(path.join(here, name))) throw new Error(`${name} missing`);
const frozen = {schema_version: "runtime-source-context-frozen-hashes-v1", frozen_at: "2026-08-27", files: Object.fromEntries(files.map(name => [name, sha256(path.join(here, name))]))};
fs.writeFileSync(output, `${JSON.stringify(frozen, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(frozen, null, 2)}\n`);
