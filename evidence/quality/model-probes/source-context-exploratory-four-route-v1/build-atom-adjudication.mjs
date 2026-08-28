#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const routes = [
  "codex-gpt-5.6-sol-high",
  "claude-opus-5-high-exploratory",
  "pi-zai-cn-glm-5.3-flash-high",
  "agy-gemini-3.7-flash-high"
];
const proposalFiles = {
  "codex-gpt-5.6-sol-high": "PROPOSED-ATOMS-codex.json",
  "claude-opus-5-high-exploratory": "PROPOSED-ATOMS-claude.json",
  "pi-zai-cn-glm-5.3-flash-high": "PROPOSED-ATOMS-glm.json"
};
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const readJson = name => JSON.parse(fs.readFileSync(path.join(directory, name), "utf8"));
const reference = readJson("REFERENCE.json");
const referenceById = new Map(reference.items.map(item => [item.item_id, item]));
const candidateNames = routes.flatMap(route => ["A", "B"].flatMap(arm => [1, 2].map(run => `CANDIDATE-${route}-${arm}${run}.json`)));
const proposalByKey = new Map();

for (const [route, file] of Object.entries(proposalFiles)) {
  const proposal = readJson(file);
  const proposalItems = Array.isArray(proposal) ? proposal : proposal.items;
  const proposalRoute = Array.isArray(proposal) ? proposal[0]?.route : (proposal.route ?? proposalItems?.[0]?.route);
  if (proposalRoute !== route || !Array.isArray(proposalItems) || proposalItems.length !== 56) throw new Error(`${file}: unexpected route or item count`);
  for (const item of proposalItems) {
    const key = `${item.route}\0${item.arm}\0${item.run}\0${item.item_id}`;
    if (item.reviewer_verified !== true || proposalByKey.has(key)) throw new Error(`${file}: invalid or duplicate proposal ${key}`);
    proposalByKey.set(key, item);
  }
}

function geminiDecision(candidate, modelItem, truth) {
  if (truth.truth_class.endsWith("CLEAN")) {
    return {
      atom_hit: null,
      rationale: modelItem.verdict === "FINDING"
        ? "reference 将该条裁定为 CLEAN 且无 material atom；模型 FINDING 是 clean false positive，atom_hit 依约为 null。"
        : "reference 将该条裁定为 CLEAN 且无 material atom；atom_hit 依约为 null。"
    };
  }
  if (modelItem.verdict !== "FINDING") {
    return {atom_hit: false, rationale: `模型未以 FINDING 识别已登记 material atom：${truth.material_atom}`};
  }
  return {
    atom_hit: false,
    rationale: `模型 FINDING 指向“${modelItem.material_issue}”，没有识别已登记 material atom：${truth.material_atom}`
  };
}

const candidateHashes = [];
const items = [];
for (const name of candidateNames) {
  const bytes = fs.readFileSync(path.join(directory, name));
  const candidate = JSON.parse(bytes.toString("utf8"));
  const modelItems = candidate.response?.items ?? candidate.response?.verdicts;
  if (!Array.isArray(modelItems) || modelItems.length !== 14) throw new Error(`${name}: no 14-item scoring content`);
  candidateHashes.push({file: name, sha256: sha256(bytes), size_bytes: bytes.length});
  for (const modelItem of modelItems) {
    const truth = referenceById.get(modelItem.item_id);
    if (!truth) throw new Error(`${name}: unknown item ${modelItem.item_id}`);
    const key = `${candidate.route}\0${candidate.arm}\0${candidate.run}\0${modelItem.item_id}`;
    const proposal = candidate.route === "agy-gemini-3.7-flash-high"
      ? geminiDecision(candidate, modelItem, truth)
      : proposalByKey.get(key);
    if (!proposal) throw new Error(`${name}: missing proposal ${key}`);
    if (proposal.truth_class && proposal.truth_class !== truth.truth_class) throw new Error(`${name}: proposal truth mismatch ${key}`);
    if (proposal.model_verdict && proposal.model_verdict !== modelItem.verdict) throw new Error(`${name}: proposal verdict mismatch ${key}`);
    if (truth.truth_class.endsWith("DEFECT") && typeof proposal.atom_hit !== "boolean") throw new Error(`${name}: defect atom decision missing ${key}`);
    if (truth.truth_class.endsWith("CLEAN") && proposal.atom_hit !== null) throw new Error(`${name}: clean atom decision must be null ${key}`);
    if (modelItem.verdict !== "FINDING" && proposal.atom_hit === true) throw new Error(`${name}: non-FINDING cannot hit ${key}`);
    items.push({
      route: candidate.route,
      arm: candidate.arm,
      run: candidate.run,
      item_id: modelItem.item_id,
      truth_class: truth.truth_class,
      model_verdict: modelItem.verdict,
      atom_hit: proposal.atom_hit,
      rationale: proposal.rationale,
      lead_verified: true
    });
  }
}

if (items.length !== 224) throw new Error(`expected 224 decisions, got ${items.length}`);
const result = {
  schema_version: "source-context-exploratory-atom-adjudication-v1",
  status: "LEAD_ATOM_ADJUDICATION_COMPLETE",
  candidate_hashes: candidateHashes,
  items
};
fs.writeFileSync(path.join(directory, "ATOM-ADJUDICATION.json"), `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({items: items.length, atom_hits: items.filter(item => item.atom_hit === true).length, clean_findings: items.filter(item => item.truth_class.endsWith("CLEAN") && item.model_verdict === "FINDING").length}, null, 2)}\n`);
