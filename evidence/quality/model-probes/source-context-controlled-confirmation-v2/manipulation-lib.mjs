import fs from "node:fs";
import {sha256} from "./audit-lib.mjs";

const exactKeys = (value, keys, label) => {
  const actual = Object.keys(value).sort().join(",");
  const expected = [...keys].sort().join(",");
  if (actual !== expected) throw new Error(`${label}: keys ${actual} != ${expected}`);
};
const verdicts = new Set(["NO_OBJECTIVE_DEFECT_VISIBLE", "EXACTLY_ONE_OBJECTIVE_DEFECT", "MULTIPLE_OR_STRUCTURALLY_INVALID", "UNRESOLVED"]);
const claimTypes = new Set(["ACCURACY", "ROLE_OR_REFERENT", "CONDITION_OR_SCOPE", "DIRECTION_OR_POLARITY", "FORMAT_OR_MARKUP", "TERMINOLOGY", "OTHER_OBJECTIVE"]);

export function validateManipulationCandidate(candidateFile, queueFile, expectedPass, expectedShard) {
  const candidateBytes = fs.readFileSync(candidateFile);
  const queueBytes = fs.readFileSync(queueFile);
  const candidate = JSON.parse(candidateBytes);
  const queue = JSON.parse(queueBytes);
  exactKeys(candidate, ["schema_version", "pass", "shard", "queue_sha256", "items"], "candidate");
  if (candidate.schema_version !== "source-context-controlled-confirmation-manipulation-check-candidate-v2" || candidate.pass !== expectedPass || candidate.shard !== expectedShard || candidate.queue_sha256 !== sha256(queueBytes)) throw new Error("candidate header mismatch");
  if (!Array.isArray(candidate.items) || candidate.items.length !== queue.items.length) throw new Error("candidate item count mismatch");
  for (let index = 0; index < queue.items.length; index += 1) {
    const item = candidate.items[index];
    const visible = queue.items[index];
    exactKeys(item, ["proposal_id", "verdict", "findings", "evidence", "limitations"], `${index}`);
    if (item.proposal_id !== visible.proposal_id || !verdicts.has(item.verdict) || !Array.isArray(item.findings) || typeof item.evidence !== "string" || !item.evidence.trim()) throw new Error(`${item.proposal_id}: identity/verdict/evidence invalid`);
    if (item.verdict === "NO_OBJECTIVE_DEFECT_VISIBLE" && (item.findings.length !== 0 || item.limitations !== null)) throw new Error(`${item.proposal_id}: no-defect branch invalid`);
    if (item.verdict === "EXACTLY_ONE_OBJECTIVE_DEFECT" && (item.findings.length !== 1 || item.limitations !== null)) throw new Error(`${item.proposal_id}: exactly-one branch invalid`);
    if (item.verdict === "MULTIPLE_OR_STRUCTURALLY_INVALID" && (item.findings.length < 2 || item.limitations !== null)) throw new Error(`${item.proposal_id}: multiple branch invalid`);
    if (item.verdict === "UNRESOLVED" && (item.findings.length !== 0 || typeof item.limitations !== "string" || !item.limitations.trim())) throw new Error(`${item.proposal_id}: unresolved branch invalid`);
    for (const [findingIndex, finding] of item.findings.entries()) {
      exactKeys(finding, ["claim_type", "severity", "target_span", "claim"], `${item.proposal_id}.${findingIndex}`);
      if (!claimTypes.has(finding.claim_type) || !new Set(["major", "minor"]).has(finding.severity) || typeof finding.target_span !== "string" || !visible.target.includes(finding.target_span) || typeof finding.claim !== "string" || !finding.claim.trim()) throw new Error(`${item.proposal_id}.${findingIndex}: malformed finding`);
    }
  }
  return {candidate, queue, candidate_sha256: sha256(candidateBytes), queue_sha256: sha256(queueBytes)};
}
