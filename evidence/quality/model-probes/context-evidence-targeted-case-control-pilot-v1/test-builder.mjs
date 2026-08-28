#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {
  collectExactPairs,
  collectStringLeaves,
  containedOutboundFieldMatches,
  isRawCandidateEligible,
  isTrackedRawBasename,
  pairSha256,
  rawVariants,
  taskRevisionSha256
} from "./build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const fixtures = JSON.parse(fs.readFileSync(path.join(here, "REGISTRY-FIXTURES.json"), "utf8")).cases;

assert.equal(pairSha256(fixtures.pair_hash.source, fixtures.pair_hash.target), fixtures.pair_hash.expected_sha256);
assert.equal(
  taskRevisionSha256(fixtures.task_revision_hash.task_id, fixtures.task_revision_hash.revision_key),
  fixtures.task_revision_hash.expected_sha256
);
assert.equal(collectExactPairs(fixtures.recursive_pairs.value, "fixture.json").length, fixtures.recursive_pairs.expected_pairs);
assert.deepEqual(
  rawVariants(fixtures.json_escape.value).map(item => item.bytes.toString("hex")).sort(),
  [...fixtures.json_escape.expected_hex_variants].sort()
);
for (const logicalPath of fixtures.raw_basenames.accepted) {
  assert.equal(isTrackedRawBasename(logicalPath), true, `${logicalPath} should be accepted`);
}
for (const logicalPath of fixtures.raw_basenames.rejected) {
  assert.equal(isTrackedRawBasename(logicalPath), false, `${logicalPath} should be rejected`);
}
const nestedLeaves = collectStringLeaves(fixtures.nested_outbound_containment.value, "fixture.json");
assert.equal(
  containedOutboundFieldMatches(
    "source",
    fixtures.nested_outbound_containment.candidate,
    nestedLeaves
  ).length,
  fixtures.nested_outbound_containment.expected_matches
);
assert.equal(
  containedOutboundFieldMatches(
    "target",
    fixtures.nested_outbound_containment.short_candidate,
    nestedLeaves
  ).length,
  1
);
assert.equal(containedOutboundFieldMatches("source", "", nestedLeaves).length, 0);
assert.equal(isRawCandidateEligible(fixtures.raw_character_boundary.ascii_11), false);
assert.equal(isRawCandidateEligible(fixtures.raw_character_boundary.ascii_12), true);
assert.equal(isRawCandidateEligible(fixtures.raw_character_boundary.astral_11), false);
assert.equal(isRawCandidateEligible(fixtures.raw_character_boundary.astral_12), true);

console.log("PASS registry builder fixtures (13/13)");
