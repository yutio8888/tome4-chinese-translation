import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {};
  const valueFlags = new Set(["--engine-repo", "--dlc-root"]);
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (!valueFlags.has(flag) || !argv[index + 1]) {
      throw new Error("usage: node verify-source-locators.mjs --engine-repo ENGINE_REPO --dlc-root DLC_ROOT");
    }
    const key = flag.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    args[key] = path.resolve(argv[++index]);
  }
  if (!args.engineRepo || !args.dlcRoot) throw new Error("--engine-repo and --dlc-root are required");
  return args;
}

const args = parseArgs(process.argv.slice(2));
const sha256Bytes = value => crypto.createHash("sha256").update(value).digest("hex");
const committedPath = path.join(here, "SOURCE-LOCATORS.json");
const queue = JSON.parse(fs.readFileSync(path.join(here, "AUDIT-QUEUE.json"), "utf8"));
if (!fs.existsSync(committedPath)) throw new Error("SOURCE-LOCATORS.json missing");

const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-residual-locators-v3-"));
const regeneratedPath = path.join(temporaryDirectory, "SOURCE-LOCATORS.json");
try {
  execFileSync(process.execPath, [
    path.join(here, "locate-sources.mjs"),
    "--engine-repo", args.engineRepo,
    "--dlc-root", args.dlcRoot,
    "--out", regeneratedPath
  ], {stdio: "pipe", maxBuffer: 64 * 1024 * 1024});
  const expected = fs.readFileSync(committedPath);
  const regenerated = fs.readFileSync(regeneratedPath);
  if (expected.compare(regenerated) !== 0) throw new Error("SOURCE-LOCATORS.json does not reproduce byte-for-byte");
  const result = JSON.parse(expected.toString("utf8"));
  if (result.schema_version !== "prospective-residual-source-locators-v3") throw new Error("unexpected locator schema");
  if (result.status !== "ALL_SOURCE_ARTIFACTS_LOCATED") throw new Error("source location is incomplete");
  if (result.contains_audit_verdicts !== false || result.model_calls_made !== 0) throw new Error("non-judgment invariant failed");
  if (result.items.length !== 40 || queue.items.length !== 40) throw new Error("expected 40 items");
  if (JSON.stringify(result.items.map(item => item.audit_id)) !== JSON.stringify(queue.items.map(item => item.audit_id))) throw new Error("locator order or coverage mismatch");
  const serialized = expected.toString("utf8");
  if (/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/.test(serialized)) throw new Error("local absolute path leaked");
  for (const forbidden of ["\"verdict\"", "\"audited_at_utc\"", "\"defect_id\""]) {
    if (serialized.includes(forbidden)) throw new Error(`non-judgment field leaked: ${forbidden}`);
  }
  for (const record of result.items) {
    if (record.source_occurrences !== record.occurrence_records.length) throw new Error(`${record.audit_id}: occurrence count mismatch`);
    if (!record.source_binding?.source_artifact_sha256) throw new Error(`${record.audit_id}: bound artifact hash missing`);
    for (const occurrence of record.occurrence_records) {
      if (sha256Bytes(occurrence.visible_context) !== occurrence.visible_context_sha256) throw new Error(`${record.audit_id}: visible context hash mismatch`);
    }
  }
  process.stdout.write(`${JSON.stringify({
    status: "PASS",
    source_locators_sha256: sha256Bytes(expected),
    experiment_status: result.status,
    counts: result.counts
  }, null, 2)}\n`);
} finally {
  const allowedPrefix = `${path.resolve(os.tmpdir())}${path.sep}prospective-residual-locators-v3-`;
  const resolvedTemporary = path.resolve(temporaryDirectory);
  if (!resolvedTemporary.startsWith(allowedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolvedTemporary, {recursive: true, force: true});
}
