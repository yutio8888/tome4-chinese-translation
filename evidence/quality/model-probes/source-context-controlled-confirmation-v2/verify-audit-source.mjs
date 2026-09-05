#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildSelection} from "./select-audit-source.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf8");
const rebuilt = buildSelection();
for (const [name, value] of Object.entries(rebuilt)) assert.deepEqual(fs.readFileSync(path.join(here, name)), jsonBytes(value), `${name}: rebuild drift`);
const selection = rebuilt["AUDIT-SOURCE-SELECTION.json"];
const local = rebuilt["LOCAL-AUDIT-SOURCE-BINDINGS.json"];
const report = rebuilt["AUDIT-SOURCE-SELECTION-REPORT.json"];
assert.equal(selection.primary.length, 120);
assert.equal(selection.ordered_reserves.length, 120);
assert.equal(selection.primary.filter(item => item.profile === "dialogue").length, 60);
assert.equal(selection.primary.filter(item => item.profile === "narrative").length, 60);
assert.equal(new Set(selection.primary.map(item => item.screen_id)).size, 120);
assert.equal(new Set([...selection.primary, ...selection.ordered_reserves].map(item => item.screen_id)).size, 240);
assert.deepEqual(selection.primary.map(item => item.screen_id), local.primary.map(item => item.screen_id));
assert.equal(report.target_fields_accessed_for_selection, false);
assert.equal(report.counts.max_primary_per_source_file <= 5, true);
assert.equal(JSON.stringify(selection).includes('"target"'), false);
console.log(JSON.stringify({status: "PASS", primary: 120, reserves: 120, files: report.counts}, null, 2));
