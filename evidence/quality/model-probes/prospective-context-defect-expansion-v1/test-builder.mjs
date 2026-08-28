#!/usr/bin/env node

import assert from "node:assert/strict";
import {applyPriorModelFacingContextOverlay, applySourceExposureOverlay, collectJsonStringLeaves, packetFor} from "./build.mjs";
import {
  reconstructSourceOnlyBaseRows,
  screenSourceOnlyRows,
  sha256Bytes
} from "../prospective-source-context-audit-v4/build.mjs";

const canonical = value => JSON.stringify(value);

function upstreamFixture(mutateTargets) {
  const membershipItems = [];
  const tasks = [];
  const terminalInputs = new Map();
  const definitions = [
    {kind: "Runtime", tasks: 20, perTask: 3, profile: "mechanics", sourceTag: "tformat"},
    {kind: "Narrative", tasks: 30, perTask: 2, profile: "dialogue", sourceTag: "say"}
  ];
  let ordinal = 0;
  for (const definition of definitions) {
    for (let taskIndex = 0; taskIndex < definition.tasks; taskIndex += 1) {
      const taskId = `${definition.kind.toLowerCase()}-${taskIndex}`;
      const inputPath = `fixture/${taskId}.json`;
      const translationSnapshot = [];
      for (let rowIndex = 0; rowIndex < definition.perTask; rowIndex += 1) {
        const revisionKey = `${taskId}-${rowIndex}`;
        const source = definition.kind === "Runtime" ? `If this hits ${ordinal + 1} times, it ends.` : `They remember this road ${ordinal + 1}.`;
        const membership = {task_id: taskId, original_revision_key: revisionKey, component: "tome", section: `mod-tome/data/${revisionKey}.lua`, source_tag: definition.sourceTag, profile: definition.profile, source_sha256: sha256Bytes(source), target_sha256: `target-${ordinal}`, pair_sha256: `pair-${ordinal}`};
        const terminal = {revision_key: revisionKey, source, target: `译文-${ordinal}`, target_sha256: `terminal-target-${ordinal}`};
        if (mutateTargets) {
          if (ordinal % 2 === 0) {
            delete membership.target_sha256;
            delete membership.pair_sha256;
            delete terminal.target;
            delete terminal.target_sha256;
          } else {
            membership.target_sha256 = `mutated-${ordinal}`;
            membership.pair_sha256 = `mutated-pair-${ordinal}`;
            terminal.target = `变化-${ordinal}`;
            terminal.target_sha256 = `mutated-terminal-${ordinal}`;
          }
        }
        membershipItems.push(membership);
        translationSnapshot.push(terminal);
        ordinal += 1;
      }
      terminalInputs.set(inputPath, {payload: {translation_snapshot: translationSnapshot, terminology_snapshot: mutateTargets ? [{mutated: true}] : [{original: true}]}});
      tasks.push({task_id: taskId, dispatches: [{role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 1, input_path: inputPath}]});
    }
  }
  return {membership: {items: membershipItems}, snapshot: {tasks}, terminalInputs};
}

const contract = {seed: "fixture", required_gates: {Runtime: {items: 60}, Narrative: {items: 60}, per_task_per_category_maximum: 6}};
const exposure = {revisionSet: new Set(), contentSet: new Set()};
const locate = row => {
  const fileText = `before\n${row.source}\nafter\n`;
  const rawStart = fileText.indexOf(row.source);
  return {status: "LOCATED_ACCEPTED", fileText, source_occurrences: 1, occurrences: [{rawStart, rawEnd: rawStart + row.source.length}], source_binding: {kind: "git_commit_blob", component: row.component, repository_alias: "fixture", commit: "fixture", relative_path: row.section, source_artifact_sha256: sha256Bytes(fileText), source_artifact_size_bytes: Buffer.byteLength(fileText)}};
};

function sourceTrace(fixture) {
  const baseRows = reconstructSourceOnlyBaseRows(fixture);
  const screen = screenSourceOnlyRows({baseRows, exposure, locate, contract});
  const selected = ["Runtime", "Narrative"].flatMap(category => screen.selectedByCategory[category]);
  return {
    base: baseRows,
    counts: {classified: screen.classified.length, located: screen.locatorAccepted.length, deduplicated: screen.deduplicated.length},
    selection: selected.map(row => ({identity: `${row.task_id}\0${row.original_revision_key}`, category: row.category, profile: row.profile, source_sha256: row.source_sha256})),
    evidence: selected.map(row => packetFor(row))
  };
}

const originalTrace = sourceTrace(upstreamFixture(false));
const mutatedTrace = sourceTrace(upstreamFixture(true));
assert.equal(canonical(mutatedTrace), canonical(originalTrace), "target-side deletion/mutation changed source eligibility, order, categories, selection, or evidence");
assert.deepEqual(originalTrace.counts, {classified: 120, located: 120, deduplicated: 120});

const overlayRows = [
  {task_id: "task", original_revision_key: "structured-only", source: "structured-only complete source", source_sha256: sha256Bytes("structured-only complete source")},
  {task_id: "task", original_revision_key: "raw-only", source: "confirmed-RAW-only complete source", source_sha256: sha256Bytes("confirmed-RAW-only complete source")},
  {task_id: "task", original_revision_key: "both", source: "#LIGHT_GREEN#[kiss her]#WHITE#", source_sha256: sha256Bytes("#LIGHT_GREEN#[kiss her]#WHITE#")},
  {task_id: "task", original_revision_key: "exact-pair", source: "structured exact pair source", source_sha256: sha256Bytes("structured exact pair source")},
  {task_id: "task", original_revision_key: "source-alias", source: "source-only alias complete source", source_sha256: sha256Bytes("source-only alias complete source")},
  {task_id: "task", original_revision_key: "short-multiple", source: "him", source_sha256: sha256Bytes("him")},
  {task_id: "task", original_revision_key: "alias", source: "[follow him]", source_sha256: sha256Bytes("[follow him]")}
];
const priorRegistry = {exposure_pairs: [
  {source_sha256: overlayRows[0].source_sha256, memberships: [{task_id: "task", original_revision_key: "structured-only"}], longer_outbound_string_leaf_matches: [{method: "source_literal_in_longer_outbound_string_leaf"}], structured_exact_pair_matches: [], raw_literal_matches: [], explicit_input_alias_matches: []},
  {source_sha256: overlayRows[1].source_sha256, memberships: [{task_id: "task", original_revision_key: "raw-only"}], longer_outbound_string_leaf_matches: [], structured_exact_pair_matches: [], raw_literal_matches: [{field: "source", classification: "CONFIRMED_TRACKED_INPUT"}], explicit_input_alias_matches: []},
  {source_sha256: overlayRows[2].source_sha256, memberships: [{task_id: "task", original_revision_key: "both"}], longer_outbound_string_leaf_matches: [{method: "source_literal_in_longer_outbound_string_leaf"}], structured_exact_pair_matches: [], raw_literal_matches: [{field: "source", classification: "CONFIRMED_TRACKED_INPUT"}], explicit_input_alias_matches: []},
  {source_sha256: overlayRows[3].source_sha256, memberships: [{task_id: "task", original_revision_key: "exact-pair"}], longer_outbound_string_leaf_matches: [], structured_exact_pair_matches: [{logical_path: "fixture/exact.json", json_pointer: "/items/0"}], raw_literal_matches: [], explicit_input_alias_matches: []},
  {source_sha256: overlayRows[4].source_sha256, memberships: [{task_id: "task", original_revision_key: "source-alias"}], longer_outbound_string_leaf_matches: [], structured_exact_pair_matches: [], raw_literal_matches: [], explicit_input_alias_matches: [{method: "source_only_exact_alias"}]},
  {source_sha256: overlayRows[5].source_sha256, memberships: [{task_id: "task", original_revision_key: "short-multiple"}], longer_outbound_string_leaf_matches: [{method: "source_literal_in_longer_outbound_string_leaf"}], structured_exact_pair_matches: [{logical_path: "fixture/short.json", json_pointer: "/items/0"}], raw_literal_matches: [{field: "source", classification: "CONFIRMED_TRACKED_INPUT"}], explicit_input_alias_matches: [{method: "source_only_exact_alias"}, {method: "target_only_exact_alias"}]},
  {source_sha256: overlayRows[6].source_sha256, memberships: [{task_id: "task", original_revision_key: "alias"}], longer_outbound_string_leaf_matches: [], structured_exact_pair_matches: [], raw_literal_matches: [], explicit_input_alias_matches: [{method: "target_only_exact_alias"}]}
]};
const overlay = applySourceExposureOverlay(overlayRows, priorRegistry);
assert.equal(overlay.excluded.length, 5);
assert.equal(overlay.retained.length, 2);
assert.deepEqual(overlay.excluded.map(entry => entry.row.original_revision_key), ["structured-only", "raw-only", "both", "exact-pair", "source-alias"]);
assert.deepEqual([...new Set(overlay.excluded.map(entry => entry.reason))], ["COMPLETE_SOURCE_MIN_12_SOURCE_ORIENTED_PRIOR_EXPOSURE"]);
assert.deepEqual(overlay.weak.map(entry => entry.reason), ["SHORT_COMPLETE_SOURCE_SIGNAL_NON_DISQUALIFYING", "TARGET_ONLY_ALIAS_NON_DISQUALIFYING"]);
const shortSignals = overlay.weak[0].found.signal;
assert.deepEqual([shortSignals.structuredLonger.length, shortSignals.structuredExact.length, shortSignals.sourceOnlyAliases.length, shortSignals.raw.length, shortSignals.targetOnlyAliases.length], [1, 1, 1, 1, 1], "multiple weak signal classes on one short row were swallowed");

const contextRows = [
  {task_id: "task", original_revision_key: "exact", source: "complete exact source", source_sha256: sha256Bytes("complete exact source")},
  {task_id: "task", original_revision_key: "longer", source: "complete nested source", source_sha256: sha256Bytes("complete nested source")},
  {task_id: "task", original_revision_key: "short-context", source: "tiny", source_sha256: sha256Bytes("tiny")},
  {task_id: "task", original_revision_key: "clean", source: "not previously present", source_sha256: sha256Bytes("not previously present")}
];
const contextArtifacts = [{logical_path: "fixture/a~b.json", value: {"a/b": ["complete exact source", "prefix complete nested source suffix", "tiny"]}}];
assert.deepEqual(collectJsonStringLeaves(contextArtifacts[0].value).map(leaf => leaf.json_pointer), ["/a~1b/0", "/a~1b/1", "/a~1b/2"]);
const contextOverlay = applyPriorModelFacingContextOverlay(contextRows, contextArtifacts);
assert.deepEqual(contextOverlay.excluded.map(entry => entry.row.original_revision_key), ["exact", "longer"]);
assert.deepEqual(contextOverlay.excluded.flatMap(entry => entry.matches.map(match => match.method)), ["exact_string_leaf", "strict_longer_string_leaf"]);
assert.deepEqual(contextOverlay.weak.map(entry => entry.row.original_revision_key), ["short-context"]);
assert.deepEqual(contextOverlay.retained.map(row => row.original_revision_key), ["short-context", "clean"]);

const twoOccurrenceRow = {
  component: "tome",
  source_sha256: sha256Bytes("needle"),
  locator: {
    fileText: `prefix needle middle needle suffix`,
    source_occurrences: 2,
    occurrences: [{rawStart: 7, rawEnd: 13}, {rawStart: 21, rawEnd: 27}],
    source_binding: {kind: "git_commit_blob", component: "tome", repository_alias: "fixture", commit: "fixture", relative_path: "fixture.lua", source_artifact_sha256: sha256Bytes("prefix needle middle needle suffix"), source_artifact_size_bytes: 33}
  }
};
const boundedPacket = packetFor(twoOccurrenceRow);
assert.equal(boundedPacket.source_occurrences, 2);
assert.ok(boundedPacket.supplemental_json_utf8_bytes <= 12288);

process.stdout.write("PASS corrected residual, target-invariance, exposure-overlay, and bounded packet fixtures\n");
