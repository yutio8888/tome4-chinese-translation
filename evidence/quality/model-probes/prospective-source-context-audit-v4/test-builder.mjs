#!/usr/bin/env node

import assert from "node:assert/strict";
import {
  assembleSourceOnlyPresentation,
  canonicalSourceOnlyBaseBytes,
  contentExposureKey,
  contextForOccurrence,
  locatorContentKey,
  makeSourceOnlyBaseFrame,
  normalizeSource,
  normalizedOccurrences,
  reconstructSourceOnlyBaseRows,
  revisionExposureKey,
  screenSourceOnlyRows,
  sha256Bytes,
  utf8Prefix,
  utf8Suffix
} from "./build.mjs";

assert.equal(normalizeSource("  alpha\\n  beta\t gamma  "), "alpha beta gamma");
assert.equal(revisionExposureKey("task", "revision"), sha256Bytes("task\0revision"));
assert.equal(contentExposureKey("alpha\n beta"), contentExposureKey(" alpha \\n beta "));
assert.equal(locatorContentKey("tome", "alpha\n beta"), sha256Bytes("tome\0alpha beta"));

function upstreamFixture(mode) {
  const membershipItems = [];
  const tasks = [];
  const terminalInputs = new Map();
  const definitions = [
    {kind: "Runtime", taskCount: 20, rowsPerTask: 3, profile: "mechanics", sourceTag: "tformat"},
    {kind: "Narrative", taskCount: 30, rowsPerTask: 2, profile: "dialogue", sourceTag: "say"}
  ];
  let ordinal = 0;
  for (const definition of definitions) {
    for (let taskIndex = 0; taskIndex < definition.taskCount; taskIndex += 1) {
      const taskId = `${definition.kind.toLowerCase()}-task-${String(taskIndex).padStart(2, "0")}`;
      const inputPath = `inputs/${taskId}.json`;
      const translationSnapshot = [];
      for (let rowIndex = 0; rowIndex < definition.rowsPerTask; rowIndex += 1) {
        const revisionKey = `${taskId}-revision-${rowIndex}`;
        const source = definition.kind === "Runtime"
          ? `If it hits ${ordinal + 1} times, this effect ends.`
          : `They remember this path ${ordinal + 1}.`;
        const membership = {
          task_id: taskId,
          original_revision_key: revisionKey,
          component: "tome",
          section: `mod-tome/data/${definition.kind.toLowerCase()}/${revisionKey}.lua`,
          source_tag: definition.sourceTag,
          profile: definition.profile,
          source_sha256: sha256Bytes(source),
          canonical_revision_id: `canonical-${ordinal}`,
          membership_sha256: `membership-${ordinal}`,
          target_sha256: `target-hash-${ordinal}`,
          pair_sha256: `pair-${ordinal}`
        };
        const terminalItem = {revision_key: revisionKey, source, target: `translation-${ordinal}`, target_sha256: `target-${ordinal}`};
        if (mode === "mutated") {
          if (ordinal % 2 === 0) {
            delete membership.target_sha256;
            delete membership.pair_sha256;
            delete terminalItem.target;
            delete terminalItem.target_sha256;
          } else {
            membership.target_sha256 = `changed-target-hash-${ordinal}`;
            membership.pair_sha256 = `changed-pair-${ordinal}`;
            terminalItem.target = `changed-translation-${ordinal}`;
            terminalItem.target_sha256 = `changed-target-${ordinal}`;
          }
          membership.canonical_revision_id = `changed-canonical-${ordinal}`;
          membership.membership_sha256 = `changed-membership-${ordinal}`;
        }
        membershipItems.push(membership);
        translationSnapshot.push(terminalItem);
        ordinal += 1;
      }
      terminalInputs.set(inputPath, {
        candidate_identity: {irrelevant: true},
        payload: {
          translation_snapshot: translationSnapshot,
          terminology_snapshot: mode === "mutated" ? [{changed: true}] : [{unchanged: true}]
        }
      });
      tasks.push({
        task_id: taskId,
        dispatches: [{role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 1, input_path: inputPath}]
      });
    }
  }
  return {membership: {items: membershipItems}, snapshot: {tasks}, terminalInputs};
}

const originalUpstream = upstreamFixture("original");
const mutatedUpstream = upstreamFixture("mutated");
const originalBaseBytes = canonicalSourceOnlyBaseBytes(originalUpstream);
const mutatedBaseBytes = canonicalSourceOnlyBaseBytes(mutatedUpstream);
assert.deepEqual(mutatedBaseBytes, originalBaseBytes, "translation-side mutation changed the source-only base");

const originalRows = reconstructSourceOnlyBaseRows(originalUpstream);
const mutatedRows = reconstructSourceOnlyBaseRows(mutatedUpstream);
assert.deepEqual(mutatedRows, originalRows);
assert.equal(originalRows.length, 120);
assert.deepEqual(
  makeSourceOnlyBaseFrame(mutatedRows, "fixture-production-commit"),
  makeSourceOnlyBaseFrame(originalRows, "fixture-production-commit")
);

const accessGateFixture = upstreamFixture("original");
Object.defineProperty(accessGateFixture.membership.items[0], "target_sha256", {
  enumerable: true,
  get() { throw new Error("translation-side membership access"); }
});
Object.defineProperty(accessGateFixture.terminalInputs.values().next().value.payload.translation_snapshot[0], "target", {
  enumerable: true,
  get() { throw new Error("translation-side terminal access"); }
});
assert.doesNotThrow(() => reconstructSourceOnlyBaseRows(accessGateFixture));

const contract = {
  seed: "prospective-source-context-audit-v4|2026-08-28|source-only-screen-v5",
  required_gates: {
    Runtime: {items: 60, minimum_tasks: 20},
    Narrative: {items: 60, minimum_tasks: 30},
    per_task_per_category_maximum: 6
  }
};
const exposure = {revisionSet: new Set(), contentSet: new Set()};
const locate = row => {
  const fileText = `local text = ${row.source}\n`;
  const rawStart = fileText.indexOf(row.source);
  return {
    status: "LOCATED_ACCEPTED",
    fileText,
    source_occurrences: 1,
    occurrences: [{rawStart, rawEnd: rawStart + row.source.length}],
    source_binding: {
      kind: "git_commit_blob",
      component: row.component,
      repository_alias: "fixture",
      commit: "fixture-tome-commit",
      relative_path: row.section.replace("mod-tome/", "game/modules/tome/"),
      source_artifact_sha256: sha256Bytes(fileText),
      source_artifact_size_bytes: Buffer.byteLength(fileText, "utf8")
    }
  };
};

function pipelineTrace(rows) {
  const screen = screenSourceOnlyRows({baseRows: rows, exposure, locate, contract});
  const presentation = assembleSourceOnlyPresentation(screen.selectedByCategory, "fixture-tome-commit");
  return {
    counts: {
      source_size: screen.sourceSizeEligible.length,
      classified: screen.classified.length,
      exposure_eligible: screen.exposureEligible.length,
      locator_accepted: screen.locatorAccepted.length,
      deduplicated: screen.deduplicated.length
    },
    seeded_selection: ["Runtime", "Narrative"].map(category => ({
      category,
      identities: screen.selectedByCategory[category].map(row => `${row.task_id}\0${row.original_revision_key}`)
    })),
    presentation_bytes_hex: Buffer.from(JSON.stringify(presentation.presentationPayload), "utf8").toString("hex")
  };
}

const originalTrace = pipelineTrace(originalRows);
const mutatedTrace = pipelineTrace(mutatedRows);
assert.deepEqual(mutatedTrace, originalTrace, "translation-side mutation changed counts, seeded selection or presentation");
assert.deepEqual(originalTrace.counts, {
  source_size: 120,
  classified: 120,
  exposure_eligible: 120,
  locator_accepted: 120,
  deduplicated: 120
});

const source = "If it hits 3 times, this effect ends.";
const fileText = `before\n${source}\nafter\n`;
const occurrences = normalizedOccurrences(fileText, source);
assert.equal(occurrences.length, 1);
const context = contextForOccurrence(fileText, occurrences[0], 1);
assert.equal(context.visible_context.includes(source), false);
assert.equal(context.visible_context.includes("[[SOURCE_MATCH_1]]"), true);
assert.ok(context.before_utf8_bytes <= 2000 && context.after_utf8_bytes <= 2000 && context.visible_context_utf8_bytes <= 8192);

const emoji = "🙂".repeat(10);
assert.equal(Buffer.byteLength(utf8Prefix(emoji, 9), "utf8"), 8);
assert.equal(Buffer.byteLength(utf8Suffix(emoji, 9), "utf8"), 8);

console.log("PASS source-only methodology fixtures");
