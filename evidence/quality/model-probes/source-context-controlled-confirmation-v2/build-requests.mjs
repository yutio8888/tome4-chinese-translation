#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const read = name => JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
const sha = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const writeNew = (name, value) => {
  const file = path.join(here, name);
  if (fs.existsSync(file)) throw new Error(`refusing to overwrite ${name}`);
  fs.writeFileSync(file, typeof value === "string" ? value : `${JSON.stringify(value, null, 2)}\n`, {flag: "wx"});
};
const rank = item => sha(`source-context-controlled-confirmation-v2/request-order/2026-08-28\0${item.revision_id}`);
const sample = read("FINAL-SAMPLE.json");
if (sample.status !== "FROZEN_BEFORE_ROUTE_QUALIFICATION_OR_EXPERIMENTAL_INFERENCE" || sample.items.length !== 60) throw new Error("final sample not frozen/complete");
const ordered = [...sample.items].sort((a, b) => rank(a).localeCompare(rank(b)) || a.item_id.localeCompare(b.item_id));
const idMap = ordered.map((item, index) => ({neutral_id: `Q${String(index + 1).padStart(3, "0")}`, sealed_item_id: item.item_id, revision_id: item.revision_id}));
const make = arm => ({
  schema_version: `source-context-controlled-confirmation-request-${arm.toLowerCase()}-v2`,
  items: ordered.map((item, index) => ({
    neutral_id: idMap[index].neutral_id,
    source: item.source,
    target: item.target,
    ...(arm === "B" ? {source_context: item.source_context} : {})
  }))
});
const armA = make("A");
const armB = make("B");
for (let i = 0; i < 60; i += 1) {
  const a = armA.items[i], b = armB.items[i];
  const {source_context, ...bProjection} = b;
  if (JSON.stringify(a) !== JSON.stringify(bProjection)) throw new Error(`A/B drift at ${a.neutral_id}`);
  if (!b.source_context) throw new Error(`empty B context at ${b.neutral_id}`);
}
const prompt = fs.readFileSync(path.join(here, "REVIEWER-PROMPT.md"));
const schema = fs.readFileSync(path.join(here, "REVIEWER-SCHEMA.json"));
const schemaMarker = Buffer.from("\n输出 JSON Schema（逐字遵守）：\n");
const inputMarker = Buffer.from("\n输入 JSON：\n");
const requestBytes = arm => Buffer.concat([prompt, schemaMarker, schema, inputMarker, Buffer.from(JSON.stringify(arm))]);
const forbidden = [
  [/\/(?:home|Users|root|tmp|opt|var|mnt)\//u, "local absolute path"],
  [/(?:SEALED-REFERENCE|adjudicat|defect_id|model_provenance|proposal_id|audit_id|revision_id|relative_path|mutation_family|"role"\s*:)/iu, "sealed/local metadata"],
  [/[0-9a-f]{40,64}/iu, "commit or content hash"],
  [/(?:API[_-]?KEY|AUTHORIZATION\s*:\s*BEARER|credential)/iu, "credential marker"]
];
for (const [arm, value] of [["A", armA], ["B", armB]]) {
  const bytes = requestBytes(value);
  for (const [pattern, label] of forbidden) if (pattern.test(bytes.toString("utf8"))) throw new Error(`${arm}: ${label}`);
}
writeNew("OUTBOUND-A.json", armA);
writeNew("OUTBOUND-B.json", armB);
writeNew("REQUEST-A.txt", requestBytes(armA));
writeNew("REQUEST-B.txt", requestBytes(armB));
writeNew("LOCAL-ID-MAP.json", {schema_version: "source-context-controlled-confirmation-local-id-map-v2", status: "SEALED_LOCAL_ONLY", items: idMap});
writeNew("REQUEST-BUILD-REPORT.json", {
  schema_version: "source-context-controlled-confirmation-request-build-report-v2",
  status: "PASS",
  sample_sha256: sha(fs.readFileSync(path.join(here, "FINAL-SAMPLE.json"))),
  prompt_sha256: sha(prompt),
  schema_sha256: sha(schema),
  schema_embedding: {
    A_offset: requestBytes(armA).indexOf(schema),
    B_offset: requestBytes(armB).indexOf(schema),
    occurrence_count_each: 1
  },
  order_seed: "source-context-controlled-confirmation-v2/request-order/2026-08-28",
  counts: {total: 60},
  request_sha256: {A: sha(requestBytes(armA)), B: sha(requestBytes(armB))},
  arm_projection_check: "PASS_ONLY_SOURCE_CONTEXT_DIFFERS",
  outbound_scan: "PASS"
});
process.stdout.write(`${JSON.stringify({status: "PASS", request_sha256: {A: sha(requestBytes(armA)), B: sha(requestBytes(armB))}}, null, 2)}\n`);
