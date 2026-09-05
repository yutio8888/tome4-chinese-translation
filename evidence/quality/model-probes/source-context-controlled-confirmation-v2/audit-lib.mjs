import crypto from "node:crypto";
import fs from "node:fs";

export const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");

function exactKeys(value, keys, label) {
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error(`${label}: keys ${actual.join(",")} != ${expected.join(",")}`);
}

export function validateAuditCandidate(candidateFile, queueFile, expectedPass, expectedShard) {
  const candidateBytes = fs.readFileSync(candidateFile);
  const queueBytes = fs.readFileSync(queueFile);
  const candidate = JSON.parse(candidateBytes);
  const queue = JSON.parse(queueBytes);
  exactKeys(candidate, ["schema_version", "pass", "shard", "queue_sha256", "items"], "candidate");
  if (candidate.schema_version !== "source-context-controlled-confirmation-clean-audit-candidate-v2") throw new Error("candidate schema_version mismatch");
  if (candidate.pass !== expectedPass || candidate.shard !== expectedShard) throw new Error("candidate pass/shard mismatch");
  if (candidate.queue_sha256 !== sha256(queueBytes)) throw new Error("candidate queue hash mismatch");
  if (!Array.isArray(queue.items) || queue.items.length === 0 || !Array.isArray(candidate.items) || candidate.items.length !== queue.items.length) throw new Error("candidate/queue item count mismatch");
  for (let index = 0; index < queue.items.length; index += 1) {
    const item = candidate.items[index];
    const visible = queue.items[index];
    exactKeys(item, ["audit_id", "verdict", "findings", "evidence", "limitations"], `items[${index}]`);
    if (item.audit_id !== visible.audit_id) throw new Error(`items[${index}]: audit_id/order mismatch`);
    if (!new Set(["CLEAN", "OBJECTIVE_DEFECT", "UNRESOLVED"]).has(item.verdict)) throw new Error(`${item.audit_id}: invalid verdict`);
    if (!Array.isArray(item.findings) || typeof item.evidence !== "string" || !item.evidence.trim()) throw new Error(`${item.audit_id}: malformed findings/evidence`);
    if (item.verdict === "CLEAN" && (item.findings.length !== 0 || item.limitations !== null)) throw new Error(`${item.audit_id}: CLEAN branch invalid`);
    if (item.verdict === "OBJECTIVE_DEFECT" && (item.findings.length === 0 || item.limitations !== null)) throw new Error(`${item.audit_id}: OBJECTIVE_DEFECT branch invalid`);
    if (item.verdict === "UNRESOLVED" && (typeof item.limitations !== "string" || !item.limitations.trim())) throw new Error(`${item.audit_id}: UNRESOLVED limitations invalid`);
    for (let findingIndex = 0; findingIndex < item.findings.length; findingIndex += 1) {
      const finding = item.findings[findingIndex];
      exactKeys(finding, ["claim_type", "severity", "target_span", "claim"], `${item.audit_id}.findings[${findingIndex}]`);
      if (!new Set(["ACCURACY", "ROLE_OR_REFERENT", "CONDITION_OR_SCOPE", "DIRECTION_OR_POLARITY", "FORMAT_OR_MARKUP", "TERMINOLOGY", "OTHER_OBJECTIVE"]).has(finding.claim_type)) throw new Error(`${item.audit_id}: invalid claim_type`);
      if (!new Set(["major", "minor"]).has(finding.severity)) throw new Error(`${item.audit_id}: invalid severity`);
      if (typeof finding.target_span !== "string" || !finding.target_span || !visible.target.includes(finding.target_span)) throw new Error(`${item.audit_id}: target_span is not exact`);
      if (typeof finding.claim !== "string" || !finding.claim.trim()) throw new Error(`${item.audit_id}: empty claim`);
    }
  }
  return {candidate, queue, candidate_sha256: sha256(candidateBytes), queue_sha256: sha256(queueBytes)};
}
