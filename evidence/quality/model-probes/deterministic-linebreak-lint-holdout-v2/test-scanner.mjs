#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {countNewlines, scanRows} from "./scanner-lib.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const fixtures = JSON.parse(fs.readFileSync(path.join(here, "SCANNER-FIXTURES.json"), "utf8"));
const stats = {
  hanCharacters: fixtures.statistics.han_characters,
  characterFrequency: new Map(Object.entries(fixtures.statistics.character_frequency)),
  bigramFrequency: new Map(Object.entries(fixtures.statistics.bigram_frequency))
};
let passed = 0;
for (const fixture of fixtures.cases) {
  const row = {
    revision_id: fixture.id,
    revision_uid: `${fixture.id}-uid`,
    component: "fixture",
    section: `fixture/${fixture.id}`,
    source_tag: "fixture",
    profile: "unknown",
    risk_flags: [],
    occurrences: [],
    source: fixture.source,
    target: fixture.target,
    structure: {newlines: {source: countNewlines(fixture.source), target: countNewlines(fixture.target)}}
  };
  const result = scanRows([row], stats).candidates;
  if (fixture.expected_tier === null && result.length !== 0) throw new Error(`${fixture.id}: expected no candidate`);
  if (fixture.expected_tier !== null && (result.length !== 1 || result[0].tier !== fixture.expected_tier)) {
    throw new Error(`${fixture.id}: expected ${fixture.expected_tier}, got ${result.map(candidate => candidate.tier).join(",") || "none"}`);
  }
  passed += 1;
}
if (passed !== 10) throw new Error(`expected 10 fixtures, found ${passed}`);
process.stdout.write(`${JSON.stringify({status: "PASS", fixture_cases: passed}, null, 2)}\n`);
