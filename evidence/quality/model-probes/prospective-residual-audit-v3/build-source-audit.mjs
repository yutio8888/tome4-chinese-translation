import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");

function readArtifact(name) {
  const bytes = fs.readFileSync(path.join(here, name));
  return {bytes, data: JSON.parse(bytes.toString("utf8")), sha256: sha256(bytes)};
}

function parseArgs(argv) {
  if (argv.length === 0) return {out: path.join(here, "SOURCE-AUDIT.json")};
  if (argv.length !== 2 || argv[0] !== "--out" || !argv[1]) {
    throw new Error("usage: node build-source-audit.mjs [--out OUTPUT]");
  }
  return {out: path.resolve(argv[1])};
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function countBy(items, field, order) {
  return Object.fromEntries(order.map(value => [value, items.filter(item => item[field] === value).length]));
}

const args = parseArgs(process.argv.slice(2));
const protocolArtifact = readArtifact("SOURCE-AUDIT-PROTOCOL.json");
const queueArtifact = readArtifact("AUDIT-QUEUE.json");
const locatorsArtifact = readArtifact("SOURCE-LOCATORS.json");
const decisionsArtifact = readArtifact("SOURCE-AUDIT-DECISIONS.json");
const protocol = protocolArtifact.data;
const queue = queueArtifact.data;
const locators = locatorsArtifact.data;
const decisions = decisionsArtifact.data;

assert(protocol.schema_version === "prospective-residual-source-audit-protocol-v3", "unexpected source-audit protocol schema");
assert(protocol.status === "FROZEN_BEFORE_SOURCE_AUDIT", "source-audit protocol is not frozen");
assert(queue.schema_version === "prospective-residual-audit-queue-v3", "unexpected audit-queue schema");
assert(queue.reviewer_inference_allowed === false, "audit queue permits premature reviewer inference");
assert(locators.schema_version === "prospective-residual-source-locators-v3", "unexpected source-locator schema");
assert(locators.status === "ALL_SOURCE_ARTIFACTS_LOCATED", "not all source artifacts are located");
assert(decisions.schema_version === "prospective-residual-source-audit-decisions-v3", "unexpected decision schema");
assert(decisions.status === "PRIMARY_ADJUDICATOR_SIGNED", "source-audit decisions are not signed");
assert(decisions.later_reviewer_route_outputs_available === false, "later reviewer-route output contaminated the audit");
assert(typeof decisions.primary_adjudicator === "string" && decisions.primary_adjudicator.trim(), "primary adjudicator missing");
assert(typeof decisions.signed_at_utc === "string" && !Number.isNaN(Date.parse(decisions.signed_at_utc)), "invalid root signing timestamp");
assert(protocol.later_reviewer_route_outputs_available_to_adjudicator === false, "protocol permits later-output contamination");

const verdictOrder = ["CONFIRMED", "REFUTED", "INDETERMINATE", "UNREACHABLE"];
const evidenceClassOrder = protocol.record_schema.evidence_class.enum;
const queueById = new Map(queue.items.map(item => [item.audit_id, item]));
const locatorById = new Map(locators.items.map(item => [item.audit_id, item]));
assert(queue.items.length === 40 && locators.items.length === 40 && decisions.items.length === 40, "source audit must cover exactly 40 items");
assert(queueById.size === 40 && locatorById.size === 40, "queue or locator audit_id values are not unique");
assert(new Set(decisions.items.map(item => item.audit_id)).size === 40, "decision audit_id values are not unique");
assert(JSON.stringify(locators.items.map(item => item.audit_id)) === JSON.stringify(queue.items.map(item => item.audit_id)), "locator order does not match queue order");
assert(JSON.stringify(decisions.items.map(item => item.audit_id)) === JSON.stringify(queue.items.map(item => item.audit_id)), "decision order does not match queue order");

const items = decisions.items.map(decision => {
  const queueItem = queueById.get(decision.audit_id);
  const locator = locatorById.get(decision.audit_id);
  assert(queueItem && locator, `${decision.audit_id}: missing queue or locator record`);
  assert(verdictOrder.includes(decision.verdict), `${decision.audit_id}: invalid verdict`);
  assert(evidenceClassOrder.includes(decision.evidence_class), `${decision.audit_id}: invalid evidence class`);
  assert(typeof decision.reason === "string" && decision.reason.trim(), `${decision.audit_id}: reason missing`);
  assert(typeof decision.audited_at_utc === "string" && !Number.isNaN(Date.parse(decision.audited_at_utc)), `${decision.audit_id}: invalid audit timestamp`);
  assert(decision.primary_adjudicator_verified === true, `${decision.audit_id}: primary verification missing`);
  assert(Array.isArray(decision.audit_assistance), `${decision.audit_id}: assistance trace missing`);
  for (const assistance of decision.audit_assistance) {
    assert(typeof assistance.agent_task_name === "string" && assistance.agent_task_name, `${decision.audit_id}: assistance task name missing`);
    assert(typeof assistance.scope === "string" && assistance.scope, `${decision.audit_id}: assistance scope missing`);
    assert(assistance.ground_truth === false, `${decision.audit_id}: assistance was incorrectly treated as ground truth`);
  }
  if (decision.verdict === "CONFIRMED") assert(decision.finding && typeof decision.finding === "object", `${decision.audit_id}: confirmed finding missing`);
  else assert(decision.finding === null, `${decision.audit_id}: non-confirmed item contains a finding`);

  const ordinals = decision.used_occurrence_ordinals;
  assert(Array.isArray(ordinals) && ordinals.length > 0, `${decision.audit_id}: used occurrence ordinals missing`);
  assert(ordinals.every((ordinal, index) => Number.isInteger(ordinal) && ordinal > 0 && (index === 0 || ordinal > ordinals[index - 1])), `${decision.audit_id}: occurrence ordinals are not strictly increasing positive integers`);
  const allOrdinals = locator.occurrence_records.map(record => record.occurrence_ordinal);
  assert(JSON.stringify(ordinals) === JSON.stringify(allOrdinals), `${decision.audit_id}: not every located occurrence was reviewed`);
  assert(locator.source_occurrences === locator.occurrence_records.length, `${decision.audit_id}: locator occurrence count mismatch`);
  assert(locator.source_binding?.source_artifact_sha256, `${decision.audit_id}: source artifact hash missing`);
  const visibleContextSha256s = ordinals.map(ordinal => {
    const occurrence = locator.occurrence_records.find(record => record.occurrence_ordinal === ordinal);
    assert(occurrence, `${decision.audit_id}: occurrence ${ordinal} missing`);
    assert(sha256(occurrence.visible_context) === occurrence.visible_context_sha256, `${decision.audit_id}: occurrence ${ordinal} visible-context hash mismatch`);
    return occurrence.visible_context_sha256;
  });

  return {
    audit_id: decision.audit_id,
    task_id: queueItem.task_id,
    stratum: queueItem.stratum,
    canonical_revision_uid: queueItem.canonical_identity.revision_uid,
    design_weight: queueItem.design_weight,
    verdict: decision.verdict,
    evidence_class: decision.evidence_class,
    source_locator: {
      artifact: "SOURCE-LOCATORS.json",
      audit_id: decision.audit_id,
      locator_status: locator.locator_status,
      used_occurrence_ordinals: [...ordinals],
      all_occurrences_reviewed: true
    },
    source_artifact_sha256: locator.source_binding.source_artifact_sha256,
    visible_context_sha256s: visibleContextSha256s,
    source_occurrences: locator.source_occurrences,
    reason: decision.reason,
    finding: decision.finding,
    audited_at_utc: decision.audited_at_utc,
    audit_assistance: decision.audit_assistance.map(assistance => ({
      ...assistance,
      agent_task_name: assistance.agent_task_name.replace(/^\/root\//, "")
    })),
    primary_adjudicator_verified: true
  };
});

const byVerdict = countBy(items, "verdict", verdictOrder);
const determinate = byVerdict.CONFIRMED + byVerdict.REFUTED;
const output = {
  schema_version: "prospective-residual-source-audit-v3",
  status: "FROZEN_SOURCE_AUDIT",
  visible_to_reviewer_routes: false,
  sealed_reference_material: true,
  reviewer_route_model_calls_made: 0,
  codex_subagent_assistance_used: items.some(item => item.audit_assistance.length > 0),
  primary_adjudicator: decisions.primary_adjudicator,
  signed_at_utc: decisions.signed_at_utc,
  input_sha256s: {
    source_audit_protocol: protocolArtifact.sha256,
    audit_queue: queueArtifact.sha256,
    source_locators: locatorsArtifact.sha256,
    source_audit_decisions: decisionsArtifact.sha256
  },
  counts: {
    items: items.length,
    by_verdict: byVerdict,
    by_evidence_class: countBy(items, "evidence_class", evidenceClassOrder),
    determinate_items: determinate,
    determinate_rate: determinate / items.length
  },
  sealed_reference_freeze_ready: true,
  known_limitation: "Codex subagents supplied preliminary fixed-source proposals. The primary experiment lead independently checked every registered source occurrence and signed all final verdicts before any v3 reviewer-route output existed.",
  items
};

fs.mkdirSync(path.dirname(args.out), {recursive: true});
fs.writeFileSync(args.out, `${JSON.stringify(output, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({status: output.status, out: args.out, counts: output.counts}, null, 2)}\n`);
