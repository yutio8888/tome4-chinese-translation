import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const expectedInputSha256s = {
  source_audit_protocol: "95d290e728956c0ac9efeeaa05164ba53d37e3d2a78790c7e3cf82b1b078c35b",
  audit_queue: "f785989e8bddf8b06fda34915154b7b5bbe76022926b0e3462aede44e625e159",
  source_locators: "f58d138a42a4a09665c1ddb0ff4e4ad4be9fae7811095e962e667e3d5bfab10c",
  source_audit_decisions: "7f1ff933937a423f73329b73f7d590e32b77da0ee913cb3b4e5400a5915d087e"
};

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const committedPath = path.join(here, "SOURCE-AUDIT.json");
assert(fs.existsSync(committedPath), "SOURCE-AUDIT.json missing");
const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "prospective-residual-source-audit-v3-"));
const regeneratedPath = path.join(temporaryDirectory, "SOURCE-AUDIT.json");

try {
  execFileSync(process.execPath, [path.join(here, "build-source-audit.mjs"), "--out", regeneratedPath], {
    stdio: "pipe",
    maxBuffer: 64 * 1024 * 1024
  });
  const expected = fs.readFileSync(committedPath);
  const regenerated = fs.readFileSync(regeneratedPath);
  assert(expected.compare(regenerated) === 0, "SOURCE-AUDIT.json does not reproduce byte-for-byte");
  const audit = JSON.parse(expected.toString("utf8"));
  const queue = JSON.parse(fs.readFileSync(path.join(here, "AUDIT-QUEUE.json"), "utf8"));
  const locators = JSON.parse(fs.readFileSync(path.join(here, "SOURCE-LOCATORS.json"), "utf8"));

  assert(audit.schema_version === "prospective-residual-source-audit-v3", "unexpected source-audit schema");
  assert(audit.status === "FROZEN_SOURCE_AUDIT", "source audit is not frozen");
  assert(audit.visible_to_reviewer_routes === false && audit.sealed_reference_material === true, "source audit visibility invariant failed");
  assert(audit.reviewer_route_model_calls_made === 0, "reviewer-route inference occurred before reference freeze");
  assert(audit.codex_subagent_assistance_used === true, "subagent assistance disclosure missing");
  assert(JSON.stringify(audit.input_sha256s) === JSON.stringify(expectedInputSha256s), "frozen source-audit input hash mismatch");
  assert(audit.items.length === 40 && audit.counts.items === 40, "expected 40 audit records");
  assert(new Set(audit.items.map(item => item.audit_id)).size === 40, "audit_id values are not unique");
  assert(JSON.stringify(audit.items.map(item => item.audit_id)) === JSON.stringify(queue.items.map(item => item.audit_id)), "audit order or coverage does not match queue");
  assert(audit.counts.by_verdict.CONFIRMED === 1, "expected one confirmed item");
  assert(audit.counts.by_verdict.REFUTED === 39, "expected 39 refuted items");
  assert(audit.counts.by_verdict.INDETERMINATE === 0 && audit.counts.by_verdict.UNREACHABLE === 0, "unexpected missing or indeterminate audit evidence");
  assert(audit.counts.determinate_items === 40 && audit.counts.determinate_rate === 1, "determinate coverage is incomplete");
  assert(audit.sealed_reference_freeze_ready === true, "sealed-reference readiness flag missing");

  const confirmed = audit.items.filter(item => item.verdict === "CONFIRMED");
  assert(confirmed.length === 1 && confirmed[0].audit_id === "R033", "only R033 may be confirmed");
  assert(confirmed[0].evidence_class === "FORMAT_STRUCTURE" && confirmed[0].finding?.target_span === "包\n裹", "R033 finding binding mismatch");
  const r009 = audit.items.find(item => item.audit_id === "R009");
  assert(r009?.verdict === "REFUTED", "R009 primary verdict mismatch");
  assert(r009.audit_assistance.some(record => record.proposed_verdict === "CONFIRMED" && record.disposition === "OVERRIDDEN_AFTER_INDEPENDENT_VERIFICATION"), "R009 override trace missing");

  const locatorById = new Map(locators.items.map(item => [item.audit_id, item]));
  for (const record of audit.items) {
    const locator = locatorById.get(record.audit_id);
    assert(locator, `${record.audit_id}: locator missing`);
    assert(record.primary_adjudicator_verified === true, `${record.audit_id}: primary verification missing`);
    assert(record.source_locator.artifact === "SOURCE-LOCATORS.json", `${record.audit_id}: locator artifact mismatch`);
    assert(record.source_locator.locator_status === locator.locator_status, `${record.audit_id}: locator status mismatch`);
    assert(record.source_locator.all_occurrences_reviewed === true, `${record.audit_id}: all-occurrence review flag missing`);
    const allOrdinals = locator.occurrence_records.map(occurrence => occurrence.occurrence_ordinal);
    assert(JSON.stringify(record.source_locator.used_occurrence_ordinals) === JSON.stringify(allOrdinals), `${record.audit_id}: occurrence coverage mismatch`);
    assert(record.source_artifact_sha256 === locator.source_binding.source_artifact_sha256, `${record.audit_id}: source artifact hash mismatch`);
    assert(record.source_occurrences === locator.source_occurrences, `${record.audit_id}: source occurrence count mismatch`);
    assert(JSON.stringify(record.visible_context_sha256s) === JSON.stringify(locator.occurrence_records.map(occurrence => occurrence.visible_context_sha256)), `${record.audit_id}: visible-context hash binding mismatch`);
    assert(record.audit_assistance.every(assistance => assistance.ground_truth === false), `${record.audit_id}: assistance treated as ground truth`);
    assert(record.verdict === "CONFIRMED" ? record.finding !== null : record.finding === null, `${record.audit_id}: finding/verdict mismatch`);
  }

  const serialized = expected.toString("utf8");
  const forbiddenPatterns = [
    [/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|[A-Za-z]:\\\\)/, "local absolute path"],
    [/(?:OPENAI|ANTHROPIC|GOOGLE|ZAI)_API_KEY/, "credential variable"],
    [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, "private key"],
    [/(?:sk|AIzaSy|xai)-[A-Za-z0-9_-]{16,}/, "credential-like token"]
  ];
  for (const [pattern, label] of forbiddenPatterns) assert(!pattern.test(serialized), `${label} leaked into source audit`);

  process.stdout.write(`${JSON.stringify({
    status: "PASS",
    source_audit_sha256: sha256(expected),
    experiment_status: audit.status,
    counts: audit.counts,
    confirmed_audit_ids: confirmed.map(item => item.audit_id)
  }, null, 2)}\n`);
} finally {
  const allowedPrefix = `${path.resolve(os.tmpdir())}${path.sep}prospective-residual-source-audit-v3-`;
  const resolvedTemporary = path.resolve(temporaryDirectory);
  if (!resolvedTemporary.startsWith(allowedPrefix)) throw new Error("refusing to remove unexpected temporary directory");
  fs.rmSync(resolvedTemporary, {recursive: true, force: true});
}
