import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const candidateName = process.argv[2];
if (!/^CANDIDATE-[AB]-run[12]-pi-zai-cn-glm-5\.3-flash-high\.json$/.test(candidateName ?? "")) throw new Error("usage: node repair-pi-candidate.mjs CANDIDATE-...pi-zai-cn-glm-5.3-flash-high.json");
const candidatePath = path.join(here, candidateName);
const original = JSON.parse(fs.readFileSync(candidatePath, "utf8"));
if (original.valid || original.response) throw new Error("candidate does not need parser repair");
const raw = fs.readFileSync(path.join(here, original.raw_artifact), "utf8");
const events = raw.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
const ends = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
if (ends.length !== 1) throw new Error(`expected one assistant message_end, got ${ends.length}`);
const body = (ends[0].message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("").trim();
const fenced = body.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/i);
if (!fenced) throw new Error("expected one outer JSON code fence");
const response = JSON.parse(fenced[1]);
const input = JSON.parse(fs.readFileSync(path.join(here, `HOLDOUT-${original.arm}.json`), "utf8"));
const orderedIds = input.items.map(item => item.revision_id);
const errors = [];
const semantic = [];
if (!response || typeof response !== "object" || Array.isArray(response) || JSON.stringify(Object.keys(response).sort()) !== JSON.stringify(["revisions"]) || !Array.isArray(response.revisions)) errors.push("invalid top-level response");
if (response.revisions?.length !== orderedIds.length) errors.push(`expected ${orderedIds.length} revisions`);
for (let index = 0; index < (response.revisions?.length ?? 0); index += 1) {
  const revision = response.revisions[index];
  const item = input.items[index];
  if (!revision || typeof revision !== "object" || Array.isArray(revision)) { errors.push(`revision ${index} invalid`); continue; }
  if (JSON.stringify(Object.keys(revision).sort()) !== JSON.stringify(["claim", "observation", "revision_id", "verdict"])) errors.push(`revision ${index} keys`);
  if (revision.revision_id !== orderedIds[index]) errors.push(`revision ${index} order`);
  if (!["OK", "FINDING", "UNCERTAIN"].includes(revision.verdict) || typeof revision.observation !== "string" || !revision.observation) errors.push(`revision ${index} verdict/observation`);
  if (revision.verdict === "OK") {
    if (revision.claim !== null) errors.push(`revision ${index} OK claim`);
    semantic.push({revision_id: revision.revision_id, valid_claim: true, reasons: []});
    continue;
  }
  const claim = revision.claim;
  const reasons = [];
  if (!claim || typeof claim !== "object" || Array.isArray(claim)) { errors.push(`revision ${index} claim`); semantic.push({revision_id: revision.revision_id, valid_claim: false, reasons: ["claim is not an object"]}); continue; }
  if (JSON.stringify(Object.keys(claim).sort()) !== JSON.stringify(["claim_type", "correction", "evidence", "target_span"])) errors.push(`revision ${index} claim keys`);
  if (typeof claim.target_span !== "string" || !claim.target_span || !["VALUE", "DIRECTION", "CONDITION", "SUBJECT", "TIMING", "SCOPE", "ACTION", "STATE", "ORDER", "OTHER"].includes(claim.claim_type) || typeof claim.correction !== "string" || !claim.correction || typeof claim.evidence !== "string" || !claim.evidence) errors.push(`revision ${index} claim fields`);
  if (!item.target.includes(claim.target_span)) reasons.push("target_span is not an exact target substring");
  if (![item.source, item.source_context].filter(value => typeof value === "string").some(value => value.includes(claim.evidence))) reasons.push("evidence is not an exact source/source_context substring");
  semantic.push({revision_id: revision.revision_id, valid_claim: reasons.length === 0, reasons});
}
const backupName = candidateName.replace(/\.json$/, "-unparsed-attempt1.json");
const backupPath = path.join(here, backupName);
if (fs.existsSync(backupPath)) throw new Error(`refusing to overwrite ${backupName}`);
fs.renameSync(candidatePath, backupPath);
const repaired = {...original, parser_repair: {kind: "strip_single_outer_json_code_fence", source_candidate_artifact: backupName, reused_raw_envelope: true, resampled: false}, valid: errors.length === 0, validation_errors: errors, claim_validation: semantic, verdict_counts: response.revisions.reduce((counts, revision) => { counts[revision.verdict] = (counts[revision.verdict] ?? 0) + 1; return counts; }, {}), response};
fs.writeFileSync(candidatePath, `${JSON.stringify(repaired, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({...repaired, response: undefined, claim_validation: undefined}, null, 2)}\n`);
if (!repaired.valid) process.exitCode = 2;
