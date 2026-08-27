import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const slug = "pi-zai-cn-glm-5.3-flash-high";
const rawPath = path.join(here, `RAW-${slug}.json`);
const originalCandidatePath = path.join(here, `CANDIDATE-${slug}.json`);
const normalizedCandidatePath = path.join(here, `CANDIDATE-NORMALIZED-${slug}.json`);
const normalizationPath = path.join(here, `NORMALIZATION-${slug}.json`);
const expectedRawHash = "38c5bc95a7cdc5d272ee3960e52d6ff94a117cb4fee9bf276b55ce889aa7cd3d";
const expectedOriginalCandidateHash = "4ea6745255a87f97933036ab28112f1f094f091dd64e4bdd9c121c7b075df03b";

const sha256Buffer = buffer => crypto.createHash("sha256").update(buffer).digest("hex");
const rawBuffer = fs.readFileSync(rawPath);
const originalCandidateBuffer = fs.readFileSync(originalCandidatePath);
if (sha256Buffer(rawBuffer) !== expectedRawHash) throw new Error("GLM RAW hash mismatch");
if (sha256Buffer(originalCandidateBuffer) !== expectedOriginalCandidateHash) throw new Error("original GLM candidate hash mismatch");
if (fs.existsSync(normalizedCandidatePath) || fs.existsSync(normalizationPath)) throw new Error("refusing to overwrite normalization artifacts");

const events = rawBuffer.toString("utf8").split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
const messageEnds = events.filter(event => event.type === "message_end" && event.message?.role === "assistant");
if (messageEnds.length !== 1) throw new Error(`expected one assistant message_end, got ${messageEnds.length}`);
const message = messageEnds[0].message;
if (message.provider !== "zai-standard-cn" || message.model !== "glm-5.3-flash") throw new Error("actual GLM route mismatch");
const responseText = (message.content ?? []).filter(block => block.type === "text").map(block => block.text).join("");
const originalResponse = JSON.parse(responseText.trim());
const response = structuredClone(originalResponse);
const changes = [];
for (const revision of response.revisions ?? []) {
  const extraKeys = Object.keys(revision).filter(key => !["revision_id", "verdict", "observation", "evidence"].includes(key));
  if (revision.revision_id === "C016" && JSON.stringify(extraKeys) === JSON.stringify(["vision"]) && revision.vision === "") {
    delete revision.vision;
    changes.push({
      revision_id: "C016",
      operation: "drop_empty_unrecognized_field",
      field: "vision",
      original_value: "",
      semantic_fields_changed: false
    });
  } else if (extraKeys.length) {
    throw new Error(`${revision.revision_id} contains an unregistered extra field: ${extraKeys.join(",")}`);
  }
}
if (changes.length !== 1) throw new Error(`expected exactly one registered normalization, got ${changes.length}`);
const expectedIds = Array.from({length: 24}, (_, index) => `C${String(index + 1).padStart(3, "0")}`);
if (JSON.stringify(response.revisions?.map(revision => revision.revision_id)) !== JSON.stringify(expectedIds)) throw new Error("normalized response ID/order mismatch");
for (const revision of response.revisions) {
  if (JSON.stringify(Object.keys(revision).sort()) !== JSON.stringify(["evidence", "observation", "revision_id", "verdict"])) throw new Error(`${revision.revision_id} canonical key mismatch`);
  if (!["OK", "FINDING", "UNCERTAIN"].includes(revision.verdict)) throw new Error(`${revision.revision_id} invalid verdict`);
  if (!revision.observation || !revision.evidence) throw new Error(`${revision.revision_id} missing text`);
}

const originalCandidate = JSON.parse(originalCandidateBuffer.toString("utf8"));
const normalizedCandidate = {
  ...originalCandidate,
  valid: true,
  validation_errors: [],
  normalization: path.basename(normalizationPath),
  response
};
const normalization = {
  schema_version: 1,
  route: slug,
  classification: "schema-output compatibility repair",
  resampled: false,
  raw_sha256: expectedRawHash,
  original_candidate_sha256: expectedOriginalCandidateHash,
  original_candidate_valid: false,
  original_validation_errors: originalCandidate.validation_errors,
  changes,
  policy: "The original RAW is authoritative and preserved. Only the single empty unrecognized key is removed; revision identity, verdict, observation and evidence are byte-for-byte values parsed from that RAW."
};
fs.writeFileSync(normalizedCandidatePath, `${JSON.stringify(normalizedCandidate, null, 2)}\n`);
fs.writeFileSync(normalizationPath, `${JSON.stringify(normalization, null, 2)}\n`);
process.stdout.write(`normalized one empty GLM compatibility field without resampling; RAW sha256=${expectedRawHash}\n`);
