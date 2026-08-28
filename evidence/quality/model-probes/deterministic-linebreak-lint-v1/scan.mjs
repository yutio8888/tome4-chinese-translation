#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {FROZEN, buildHanStatistics, readInventory, scanRows, sha256File} from "./scanner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const values = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  const flag = process.argv[index];
  const value = process.argv[index + 1];
  if (!value || !["--inventory", "--schema", "--out"].includes(flag) || values.has(flag)) {
    throw new Error("usage: node scan.mjs --inventory INVENTORY_JSONL --schema INVENTORY_SCHEMA [--out OUTPUT_JSON]");
  }
  values.set(flag, path.resolve(value));
}
if (!values.has("--inventory") || !values.has("--schema")) throw new Error("--inventory and --schema are required");
const out = values.get("--out") ?? path.join(here, "CANDIDATES.json");
const inventory = readInventory(values.get("--inventory"));
if (inventory.rows.length !== FROZEN.inventoryRows) throw new Error(`inventory row drift: ${inventory.rows.length}`);
if (new Set(inventory.rows.map(row => row.revision_id)).size !== inventory.rows.length) throw new Error("inventory revision IDs are not unique");
if (inventory.raw_sha256 !== FROZEN.inventoryRawSha256) throw new Error(`inventory raw hash drift: ${inventory.raw_sha256}`);
if (inventory.canonical_sha256 !== FROZEN.inventoryCanonicalSha256) throw new Error(`inventory canonical hash drift: ${inventory.canonical_sha256}`);
if (sha256File(values.get("--schema")) !== FROZEN.inventorySchemaSha256) throw new Error("inventory schema hash drift");

const statistics = buildHanStatistics(inventory.rows);
if (statistics.hanCharacters !== FROZEN.hanCharacters) throw new Error(`Han corpus size drift: ${statistics.hanCharacters}`);
const scan = scanRows(inventory.rows, statistics);
const output = {
  schema_version: "deterministic-linebreak-candidates-v1",
  experiment: "deterministic-linebreak-lint-v1",
  status: "CANDIDATES_REQUIRE_SOURCE_AUDIT",
  model_calls_made: 0,
  input_bindings: {
    production_translation_commit: FROZEN.productionCommit,
    inventory_rows: inventory.rows.length,
    inventory_raw_sha256: inventory.raw_sha256,
    inventory_canonical_sha256: inventory.canonical_sha256,
    inventory_schema_sha256: FROZEN.inventorySchemaSha256,
    rule_contract: {logical_path: "RULE-CONTRACT.json", sha256: sha256File(path.join(here, "RULE-CONTRACT.json"))}
  },
  corpus_statistics: {
    han_characters: statistics.hanCharacters,
    distinct_han_characters: statistics.characterFrequency.size,
    distinct_contiguous_han_bigrams: statistics.bigramFrequency.size
  },
  scan_counts: {
    ...scan.counts,
    candidates: scan.candidates.length,
    candidate_revisions: new Set(scan.candidates.map(candidate => candidate.revision_id)).size,
    by_tier: Object.fromEntries(["Q_QUOTED_TWO_HAN_TOKEN", "A_FREQUENT_BIGRAM", "B_LOW_SUPPORT_BIGRAM"].map(tier => [tier, scan.candidates.filter(candidate => candidate.tier === tier).length]))
  },
  candidates: scan.candidates
};
const bytes = `${JSON.stringify(output, null, 2)}\n`;
if (fs.existsSync(out)) {
  if (fs.readFileSync(out, "utf8") !== bytes) throw new Error(`existing output drift: ${out}`);
} else {
  fs.mkdirSync(path.dirname(out), {recursive: true});
  fs.writeFileSync(out, bytes, {flag: "wx"});
}
process.stdout.write(`${JSON.stringify({status: output.status, scan_counts: output.scan_counts}, null, 2)}\n`);
