#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildPackage, canonicalSha256, containsAbsolutePath, FROZEN, parseEnvelope, presentationLeakCheck, readValidatedEnvelope, sanitizeContext, selectTerminalDispatches, sha256} from "./build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../..");
const fp = bytes => ({sha256: sha256(bytes), size_bytes: bytes.length});
const payload = (revision = "r1", context = "before source after") => ({bounded_context: [{context, revision_key: revision}], contract: "translation_contextual_v1", fixed_source_identity: `commit:${"1".repeat(40)}`, ordered_revision_keys: [revision], rendered_briefing: "bounded briefing", terminology_snapshot: "", translation_snapshot: [{revision_key: revision, source: "source", target: "target"}]});
const modern = (revision = "r1", context = "before source after") => { const value = payload(revision, context); const identity = canonicalSha256(value); return {envelope: {candidate_identity: identity, payload: value}, identity}; };
const legacy = (revision = "r1") => { const envelope = payload(revision, "legacy context"); const identity = canonicalSha256(envelope); return {envelope, identity}; };

const modernBaseline = modern();
const legacyBaseline = legacy();
assert.doesNotThrow(() => parseEnvelope(modernBaseline.envelope, "modern baseline", modernBaseline.identity));
assert.doesNotThrow(() => parseEnvelope(legacyBaseline.envelope, "legacy baseline", legacyBaseline.identity));
assert.equal(parseEnvelope(modernBaseline.envelope, "modern", modernBaseline.identity).container, "modern");
assert.equal(parseEnvelope(legacyBaseline.envelope, "legacy", legacyBaseline.identity).container, "legacy");

function mutatedModern(change) {
  const state = structuredClone(modernBaseline.envelope);
  change(state);
  return state;
}

for (const [label, change, expected] of [
  ["extra key", value => { value.extra = true; }, /schema drift/u],
  ["contract", value => { value.payload.contract = "wrong"; }, /contract must be translation_contextual_v1/u],
  ["null terminology", value => { value.payload.terminology_snapshot = null; }, /terminology_snapshot must be a string/u],
  ["empty fixed source", value => { value.payload.fixed_source_identity = ""; }, /fixed-source binding must be a non-empty string/u],
  ["empty briefing", value => { value.payload.rendered_briefing = ""; }, /rendered_briefing must be a non-empty string/u],
  ["wrong ordered type", value => { value.payload.ordered_revision_keys = "r1"; }, /ordered coverage malformed/u],
  ["null row source", value => { value.payload.translation_snapshot[0].source = null; }, /source must be a non-empty string/u],
  ["ordered drift", value => { value.payload.ordered_revision_keys = ["other"]; }, /target\/context\/order drift/u],
  ["canonical content drift", value => { value.payload.translation_snapshot[0].source = "changed source"; }, /modern candidate identity drift/u],
  ["fixed source zero fields", value => { delete value.payload.fixed_source_identity; }, /exactly one fixed-source field required/u],
  ["fixed source two fields", value => { value.payload.fixed_source_commit = "2".repeat(40); }, /exactly one fixed-source field required/u],
  ["identity drift", value => { value.candidate_identity = "2".repeat(64); }, /modern candidate identity drift/u]
]) {
  assert.doesNotThrow(() => parseEnvelope(structuredClone(modernBaseline.envelope), `${label} baseline`, modernBaseline.identity), `${label}: success baseline`);
  assert.throws(() => parseEnvelope(mutatedModern(change), label, modernBaseline.identity), expected, label);
}
assert.throws(() => parseEnvelope(modernBaseline.envelope, "dispatch drift", "3".repeat(64)), /modern candidate identity drift/u);
assert.doesNotThrow(() => parseEnvelope(structuredClone(legacyBaseline.envelope), "legacy identity baseline", legacyBaseline.identity));
assert.throws(() => parseEnvelope(legacyBaseline.envelope, "legacy identity drift", "4".repeat(64)), /legacy candidate identity drift/u);
assert.doesNotThrow(() => parseEnvelope(structuredClone(legacyBaseline.envelope), "legacy schema baseline", legacyBaseline.identity));
const legacySchemaDrift = structuredClone(legacyBaseline.envelope);
legacySchemaDrift.unexpected = true;
assert.throws(() => parseEnvelope(legacySchemaDrift, "legacy schema drift", legacyBaseline.identity), /schema drift/u);

const snapshot = {tasks: [
  {task_id: "case-role", dispatches: [{role: "reviewer", purpose: "translation_contextual_v1", cycle: 1, lifecycle: "closed_valid", dispatch_id: "a", input_path: "a.json", input_fingerprint: {sha256: "a".repeat(64), size_bytes: 1}, candidate_identity: "a".repeat(64)}]},
  {task_id: "case-cycle", dispatches: [
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 2, lifecycle: "closed_valid", dispatch_id: "b", input_path: "b.json", input_fingerprint: {sha256: "b".repeat(64), size_bytes: 1}, candidate_identity: "b".repeat(64)},
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 4, lifecycle: "closed_valid_transport_error", dispatch_id: "c", input_path: "c.json", input_fingerprint: {sha256: "c".repeat(64), size_bytes: 1}, candidate_identity: "c".repeat(64)},
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 3, lifecycle: "closed_valid", dispatch_id: "d", input_path: "d.json", input_fingerprint: {sha256: "d".repeat(64), size_bytes: 1}, candidate_identity: "d".repeat(64)}
  ]},
  {task_id: "case-prefer-success", dispatches: [
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: null, lifecycle: "closed_valid", dispatch_id: "e", input_path: "e.json", input_fingerprint: {sha256: "e".repeat(64), size_bytes: 1}, candidate_identity: "e".repeat(64)},
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: null, lifecycle: "closed_valid_transport_error", dispatch_id: "f", input_path: "f.json", input_fingerprint: {sha256: "f".repeat(64), size_bytes: 1}, candidate_identity: "f".repeat(64)}
  ]},
  {task_id: "case-fallback-error", dispatches: [
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: null, lifecycle: "closed_valid_transport_error", dispatch_id: "g", input_path: "g.json", input_fingerprint: {sha256: "9".repeat(64), size_bytes: 1}, candidate_identity: "9".repeat(64)},
    {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: null, lifecycle: "transport_error", dispatch_id: "h", input_path: "h.json", input_fingerprint: {sha256: "8".repeat(64), size_bytes: 1}, candidate_identity: "8".repeat(64)}
  ]}
]};
const selected = selectTerminalDispatches(snapshot, new Set());
assert.deepEqual(selected.map(item => item.dispatch_id), ["c", "h", "e", "a"]);

const guardedDispatch = {role: "REVIEWER", purpose: "translation_contextual_v1", cycle: 1, lifecycle: "closed_valid", dispatch_id: "guard", input_path: "guard.json", input_fingerprint: {sha256: "0".repeat(64), size_bytes: 1}, candidate_identity: "0".repeat(64)};
for (const key of ["agent", "provider", "model", "review_artifacts"]) Object.defineProperty(guardedDispatch, key, {enumerable: true, get() { throw new Error(`forbidden ${key} access`); }});
const guardedTask = {task_id: "guard-task", dispatches: [guardedDispatch]};
for (const key of ["agent", "provider", "model", "review_artifacts", "source_policy"]) Object.defineProperty(guardedTask, key, {enumerable: true, get() { throw new Error(`forbidden ${key} access`); }});
assert.doesNotThrow(() => selectTerminalDispatches({tasks: [guardedTask]}, new Set()));

const main = sanitizeContext("prefix(/home/user/project/t-engine4/game/modules/tome/data/file.lua),suffix");
assert.equal(main.sanitized, "prefix(<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua),suffix");
assert.equal(main.path_occurrences, 1);
const dlc = sanitizeContext("A=C:\\work\\t-engine4\\game\\dlcs\\ashes\\data\\a.lua; B[C:/work/tome4-dlcs/cults/data/b.lua]; C=\\\\server\\share\\t-engine4\\game\\modules\\tome\\data\\c.lua.");
assert.equal(dlc.sanitized, "A=<DLC_ROOT>/game/dlcs/ashes/data/a.lua; B[<DLC_ROOT>/cults/data/b.lua]; C=<MAIN_GAME_ROOT>/game/modules/tome/data/c.lua.");
assert.equal(dlc.path_occurrences, 3);
assert.equal(containsAbsolutePath(dlc.sanitized), false);
for (const [raw, expected] of [
  ["(/srv/private/a(b).lua)", /unrecognized absolute/u],
  ["/home/user/dir(1)/t-engine4/game/modules/tome/data/file.lua", null],
  ["/home/user/dir{1}/t-engine4/game/modules/tome/data/file.lua", null],
  ["/toBase(/home/user/t-engine4/game/modules/tome/data/file.lua)", null],
  ["/#/home/user/t-engine4/game/modules/tome/data/file.lua", null]
]) {
  assert.doesNotThrow(() => containsAbsolutePath("plain text baseline"), `${raw}: scanner baseline`);
  if (expected) assert.throws(() => sanitizeContext(raw), expected, raw);
  else assert.equal(containsAbsolutePath(sanitizeContext(raw).sanitized), false, raw);
}
assert.equal(sanitizeContext("/home/user/dir(1)/t-engine4/game/modules/tome/data/file.lua").sanitized, "<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua");
assert.equal(sanitizeContext("/home/user/dir{1}/t-engine4/game/modules/tome/data/file.lua").sanitized, "<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua");
assert.equal(sanitizeContext("/toBase(/home/user/t-engine4/game/modules/tome/data/file.lua)").sanitized, "/toBase(<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua)");
assert.equal(sanitizeContext("/#/home/user/t-engine4/game/modules/tome/data/file.lua").sanitized, "/#<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua");
const url = "https://example.invalid/home/user/t-engine4/game/modules/tome/data/file.lua?q=/srv/private/file";
assert.equal(sanitizeContext(url).sanitized, url);
assert.equal(containsAbsolutePath(url), false);
assert.equal(containsAbsolutePath("<MAIN_GAME_ROOT>/game/modules/tome/data/file.lua <DLC_ROOT>/cults/data/a.lua"), false);
assert.equal(containsAbsolutePath("<DLC_ROOT>/home/user/tome4-dlcs/cults/data/a.lua"), true);
assert.equal(sanitizeContext("Lua /on_merge() and markup /# remain").sanitized, "Lua /on_merge() and markup /# remain");
assert.equal(containsAbsolutePath("/single-file"), true);
assert.throws(() => sanitizeContext("/single-file"), /unrecognized absolute/u);
assert.throws(() => sanitizeContext("unknown /home/user/unrelated/file.txt remains"), /unrecognized absolute/u);
assert.throws(() => sanitizeContext("unknown(/srv/private/file.txt),remains"), /unrecognized absolute/u);
assert.throws(() => sanitizeContext("unknown C:\\private\\file.txt remains"), /absolute/u);

const terminalBytes = Buffer.from(JSON.stringify(modernBaseline.envelope));
const terminalDispatch = {task_id: "typed-terminal", candidate_identity: modernBaseline.identity, input_path: "typed.json", input_fingerprint: fp(terminalBytes)};
assert.doesNotThrow(() => readValidatedEnvelope(terminalDispatch, () => terminalBytes), "unmutated terminal baseline");
assert.throws(() => readValidatedEnvelope({...terminalDispatch, input_fingerprint: {sha256: "0".repeat(64), size_bytes: terminalBytes.length}}, () => terminalBytes), /terminal fingerprint drift/u);
const malformedBytes = Buffer.from("not json");
assert.throws(() => readValidatedEnvelope({...terminalDispatch, input_fingerprint: fp(malformedBytes)}, () => malformedBytes), /malformed envelope JSON/u);

const safeItem = {neutral_id: "RFR-0001", category: "Runtime-focused", profile: "mechanics", source: "safe source", target: "safe target", bounded_fixed_context: "safe context"};
const safePresentation = {schema_version: "neutral-context-presentation-v1", status: "FROZEN_ZERO_INFERENCE_MODEL_FACING", counts: {items: 1, tasks: 1, profiles: {mechanics: {tasks: 1, rows: 1}}, categories: {"Runtime-focused": {tasks: 1, rows: 1}}}, items: [safeItem]};
assert.doesNotThrow(() => presentationLeakCheck(safePresentation, new Set(["internal-task-0077"])), "unmutated presentation baseline");
for (const [field, leak, expected] of [
  ["bounded_fixed_context", "prefix internal-task-0077 suffix", /internal value substring/u],
  ["bounded_fixed_context", "prior senior-audit-01 prose", /typed identity or review-history/u],
  ["bounded_fixed_context", `hash ${"a".repeat(41)}`, /hash provenance/u],
  ["bounded_fixed_context", "provider route", /model provenance/u],
  ["source", "(/srv/private/a(b).lua)", /absolute path/u],
  ["source", "/toBase(/home/user/t-engine4/game/modules/tome/data/file.lua)", /absolute path/u],
  ["source", "/#/home/user/t-engine4/game/modules/tome/data/file.lua", /absolute path/u],
  ["bounded_fixed_context", "<DLC_ROOT>/home/user/tome4-dlcs/cults/data/a.lua", /absolute path/u],
  ["target", "C:/private/file.lua", /absolute path/u]
]) {
  const item = {...safeItem, [field]: leak};
  assert.doesNotThrow(() => presentationLeakCheck(structuredClone(safePresentation), new Set(["internal-task-0077"])), `${field}: success baseline`);
  assert.throws(() => presentationLeakCheck({...safePresentation, items: [item]}, new Set(["internal-task-0077"])), expected, `${field} gate`);
}
assert.doesNotThrow(() => presentationLeakCheck(structuredClone(safePresentation), new Set()), "recursive key baseline");
assert.throws(() => presentationLeakCheck({...safePresentation, counts: {...safePresentation.counts, ["a".repeat(41)]: 0}}, new Set()), /hash provenance/u, "recursive key scan");

const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "rfr-focused-"));
try {
  const built = buildPackage({root, out: temporaryDirectory, productionInput: ".ai/task/research-route-familiarity-runtime-expansion-v1/production-input"});
  const excluded = built.registry.items.filter(item => item.hygiene_disposition === "CONTEXT_META_PROVENANCE_EXCLUDED");
  assert.deepEqual(excluded.map(item => item.neutral_id), FROZEN.excluded_neutral_ids);
  assert.equal(built.presentation.items.length, 145);
  assert.equal(new Set(built.presentation.items.map(item => item.neutral_id)).size, 145);
  for (const neutralId of ["RFR-0077", "RFR-0078", "RFR-0156"]) {
    assert.equal(excluded.some(item => item.neutral_id === neutralId), true, `${neutralId} real-row exclusion`);
    assert.equal(built.presentation.items.some(item => item.neutral_id === neutralId), false, `${neutralId} absent from presentation`);
  }
} finally {
  fs.rmSync(temporaryDirectory, {recursive: true, force: true});
}

console.log("PASS typed envelopes, identity/fingerprint/JSON mutations, boundary path fixtures, presentation gates, and real 11-exclusion/145-retained regressions");
