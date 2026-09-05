#!/usr/bin/env node

import assert from "node:assert/strict";
import {collectExposure, makePacket, normalizedOccurrences, normalizeSource, sourceOnlyInventoryView} from "./build-screen.mjs";

assert.equal(normalizeSource("  Alpha\n beta\\t gamma  "), "Alpha beta gamma");
assert.deepEqual(normalizedOccurrences("x Alpha\n beta y Alpha beta z", "Alpha beta"), [
  {rawStart: 2, rawEnd: 13},
  {rawStart: 16, rawEnd: 26}
]);

const sourceSet = new Set();
const revisionSet = new Set();
collectExposure({items: [{source: " Alpha  beta ", revision_id: "a".repeat(64)}]}, sourceSet, revisionSet);
assert.equal(sourceSet.size, 1);
assert.equal(revisionSet.has("a".repeat(64)), true);

const guarded = sourceOnlyInventoryView({source: "safe", target: "hidden", component: "tome"}, "fixture");
assert.equal(guarded.source, "safe");
assert.throws(() => guarded.target, /access denied/u);
assert.throws(() => Object.keys(guarded), /enumeration denied/u);

const source = "Ambiguous statement here";
const fileText = `line one\nline two\nlocal text = _t[[${source}]]\nline four\nline five\n`;
const [occurrence] = normalizedOccurrences(fileText, source);
const packet = makePacket(fileText, occurrence, {relative_path: "fixture.lua"}, source);
assert(packet);
assert.equal(packet.occurrence.visible_context.includes(source), false);
assert.equal(packet.occurrence.visible_context.includes("[[SOURCE_MATCH_1]]"), true);
assert.equal(packet.occurrence.visible_context_sha256.length, 64);

console.log(JSON.stringify({status: "PASS", tests: 13}, null, 2));
