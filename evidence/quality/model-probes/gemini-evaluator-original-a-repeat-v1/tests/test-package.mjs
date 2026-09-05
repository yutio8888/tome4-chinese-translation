#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {build, CELLS, checkFreeze, PROMPT_SHA256, REQUEST_BYTES, REQUEST_SHA256, SCHEMA_SHA256, splitRequest} from '../freezer.mjs';
import {checkManifest} from '../build-manifest.mjs';
import {preflight} from '../preflight.mjs';
import {jsonBytes, sha256, shaFile, treeBinding} from '../lib.mjs';
import {parseCapture, parseOutput} from '../parser.mjs';
import {interpret, metrics} from '../metrics.mjs';
import {derive, FINISH_KEYS, MAX_ATTEMPTS, PROCESS_BUDGET, START_KEYS} from '../ledger.mjs';
import {runCell} from '../runner.mjs';
import {postRun} from '../post-run.mjs';
import {GATE_PATHS, TASK} from '../gates.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'), repo = path.resolve(root, '../../../..');
const sourceRoot = 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v5';
let tests = 0;
const test = (name, fn) => { fn(); tests++; console.log(`ok ${tests} - ${name}`); };

test('freeze and static manifest rebuild byte-identically', () => { assert.deepEqual(checkFreeze(root).errors, []); assert.deepEqual(checkManifest(root), []); });
test('canonical predecessor tree binds all 80 files', () => {
  assert.deepEqual(treeBinding(repo, sourceRoot), {root: sourceRoot, file_count: 80, tree_sha256: '55dfb7bda36d2e06083c349bbb79e6b1de35e2019c1055c989633d6ef523877a'});
});
test('all three cells bind identical exact original request/schema bytes', () => {
  const built = build(root), request = fs.readFileSync(path.join(root, 'model-facing/requests/original-a.txt')), schema = fs.readFileSync(path.join(root, 'model-facing/schemas/REVIEWER-SCHEMA.json'));
  assert.equal(request.length, REQUEST_BYTES); assert.equal(sha256(request), REQUEST_SHA256); assert.equal(sha256(schema), SCHEMA_SHA256); assert.equal(sha256(splitRequest(request).promptBytes), PROMPT_SHA256);
  assert.deepEqual(built.manifest.fixed_order, CELLS); assert.equal(built.manifest.requests.length, 3); assert.equal(new Set(built.manifest.requests.map(x => x.path)).size, 1); assert.equal(new Set(built.manifest.requests.map(x => x.schema)).size, 1);
  assert.ok(request.equals(fs.readFileSync(path.join(repo, sourceRoot, 'model-facing/requests/discovery-A-run-1-shard-1.txt'))));
  assert.ok(schema.equals(fs.readFileSync(path.join(repo, sourceRoot, 'model-facing/schemas/REVIEWER-SCHEMA.json'))));
});
test('package has no sealed, reference, capture, RAW, ledger, result, or task-gate artifact', () => {
  for (const rel of ['sealed', 'execution', 'RESULT.json', 'PACKAGE_REVIEW.json', 'EXECUTION_AUTHORIZATION.json']) assert.equal(fs.existsSync(path.join(root, rel)), false);
  const names = fs.readdirSync(root, {recursive: true}).map(String); assert.equal(names.some(x => /reference|capture|raw/i.test(x)), false);
});
test('zero-state preflight is gated NO_RUN 0/0', () => {
  const value = preflight(root, repo); assert.equal(value.decision, 'NO_GO_REQUIRED_GATES'); assert.equal(value.execution_state, 'NO_RUN'); assert.equal(value.static_integrity, 'PASS'); assert.equal(value.agy_processes_spawned, 0); assert.equal(value.inference_calls_made, 0); assert.deepEqual(value.blocked_gates, ['PACKAGE_REVIEW', 'EXECUTION_AUTHORIZATION']);
});
const input = splitRequest(build(root).request).input;
const empty = {items: input.items.map(x => ({item_id: x.item_id, candidates: []}))};
const candidateOutput = (evidence, targetSpan = input.items[0].target.slice(0, 1)) => ({items: input.items.map((x, i) => ({item_id: x.item_id, candidates: i ? [] : [{verdict: 'FINDING', claim_type: 'OTHER', target_span: targetSpan, correction: '修', evidence}]}))});
test('strict parser rejects schema defects but not exact membership defects', () => {
  const nonmember = parseOutput(candidateOutput('not an exact member', 'not target'), input); assert.equal(nonmember.valid, true);
  const m = metrics(nonmember.normalized, input); assert.equal(m.evidence_membership_count, 0); assert.equal(m.target_span_membership_count, 0); assert.equal(m.status, 'DESCRIPTIVE');
  const astral = candidateOutput('😀'); assert.equal(parseOutput(astral, input).valid, true); assert.equal(metrics(parseOutput(astral, input).normalized, input).evidence_mean_character_length, 2);
  const alias = candidateOutput('x'); alias.items[0].candidates[0].evidence_quote = alias.items[0].candidates[0].evidence; delete alias.items[0].candidates[0].evidence; assert.equal(parseOutput(alias, input).valid, false);
});
test('agy envelope supports structured/response channels and rejects duplicate keys', () => {
  assert.equal(parseCapture(Buffer.from(JSON.stringify({status: 'SUCCESS', structured_output: empty})), input).valid, true);
  assert.equal(parseCapture(Buffer.from(JSON.stringify({status: 'SUCCESS', response: JSON.stringify(empty)})), input).valid, true);
  assert.equal(parseCapture(Buffer.from('{"status":"SUCCESS","status":"SUCCESS","structured_output":{"items":[]}}'), input).valid, false);
});
test('zero candidates have null rates and deterministic interpretation rules', () => {
  const zero = metrics({items: empty.items}, input); assert.equal(zero.candidate_count, 0); assert.equal(zero.evidence_membership_rate, null); assert.equal(zero.target_span_membership_rate, null); assert.equal(zero.evidence_mean_character_length, null);
  const row = rate => ({process_success: true, envelope_schema_valid: true, metrics: {candidate_count: 1, evidence_membership_rate: rate}});
  assert.equal(interpret([row(1), row(1), row(1)]), 'NOT_REPRODUCED_STOCHASTICITY_PLAUSIBLE'); assert.equal(interpret([row(0), row(0.5), row(0)]), 'CONSISTENTLY_REPRODUCED'); assert.equal(interpret([row(1), row(0), row(1)]), 'RUN_TO_RUN_VARIABILITY'); assert.equal(interpret([row(1), {...row(1), metrics: zero}, row(1)]), 'INCOMPLETE_FOR_THREE_RUN_RULE');
});
test('ledger contract fixes exact keys, ordered 3/3 budget, and one attempt', () => { assert.equal(MAX_ATTEMPTS, 1); assert.equal(PROCESS_BUDGET, 3); assert.deepEqual(START_KEYS, ['event', 'cell', 'attempt', 'started_at']); assert.deepEqual(FINISH_KEYS, ['event', 'cell', 'attempt', 'started_at', 'finished_at', 'exit_code', 'stdout_sha256', 'stderr_sha256', 'process_success', 'envelope_schema_valid', 'raw_path']); });

function fixture() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'gemini-original-a-repeat-test-'));
  const pkg = path.join(tmp, 'evidence/quality/model-probes/gemini-evaluator-original-a-repeat-v1');
  fs.mkdirSync(path.dirname(pkg), {recursive: true}); fs.cpSync(root, pkg, {recursive: true});
  fs.rmSync(path.join(pkg, 'execution'), {recursive: true, force: true}); fs.rmSync(path.join(pkg, 'RESULT.json'), {force: true});
  fs.mkdirSync(path.dirname(path.join(tmp, sourceRoot)), {recursive: true});
  fs.cpSync(path.join(repo, sourceRoot), path.join(tmp, sourceRoot), {recursive: true});
  const gateDir = path.join(tmp, '.ai/task', TASK); fs.mkdirSync(gateDir, {recursive: true});
  const manifest = shaFile(path.join(pkg, 'MANIFEST.json'));
  const review = {schema_version: 'gemini-original-a-repeat-package-review-v1', task_id: TASK, decision: 'PASS', manifest_sha256: manifest, authorized_cells: CELLS};
  fs.writeFileSync(path.join(tmp, GATE_PATHS.PACKAGE_REVIEW), jsonBytes(review));
  const authorization = {schema_version: 'gemini-original-a-repeat-execution-authorization-v1', task_id: TASK, decision: 'AUTHORIZED', manifest_sha256: manifest, package_review_sha256: shaFile(path.join(tmp, GATE_PATHS.PACKAGE_REVIEW)), authorized_cells: CELLS, agy_process_budget: 3, inference_call_budget: 3, max_attempts: 1, retries: 0};
  fs.writeFileSync(path.join(tmp, GATE_PATHS.EXECUTION_AUTHORIZATION), jsonBytes(authorization));
  return {tmp, pkg, gateHashes: [shaFile(path.join(tmp, GATE_PATHS.PACKAGE_REVIEW)), shaFile(path.join(tmp, GATE_PATHS.EXECUTION_AUTHORIZATION))]};
}

test('mocked three-cell run continues membership/zero metrics, enforces order and budget, preserves gates, cleans temp', () => {
  const f = fixture(); let calls = 0;
  try {
    const outputs = [candidateOutput('not an exact member', 'not target'), empty, candidateOutput(input.items[0].source.slice(0, 2))];
    assert.throws(() => runCell(f.pkg, f.tmp, CELLS[1], () => { calls++; return {}; }), /CELL_ORDER/); assert.equal(calls, 0);
    for (let i = 0; i < 3; i++) {
      const result = runCell(f.pkg, f.tmp, CELLS[i], () => { calls++; return {exit_code: 0, stdout: Buffer.from(JSON.stringify({status: 'SUCCESS', structured_output: outputs[i]})), stderr: Buffer.alloc(0), timed_out: false}; });
      assert.equal(result.envelope_schema_valid, true); assert.equal(result.continue_authorized, true);
    }
    assert.equal(calls, 3); assert.throws(() => runCell(f.pkg, f.tmp, CELLS[2], () => { calls++; return {}; }), /STOP_BUDGET/); assert.equal(calls, 3);
    const state = derive(f.pkg); assert.equal(state.rows.length, 6); assert.equal(state.agy_processes_spawned, 3);
    for (let i = 0; i < 6; i += 2) { assert.deepEqual(Object.keys(state.rows[i]).sort(), [...START_KEYS].sort()); assert.deepEqual(Object.keys(state.rows[i + 1]).sort(), [...FINISH_KEYS].sort()); }
    const result = postRun(f.pkg, f.tmp), again = postRun(f.pkg, f.tmp); assert.deepEqual(result, again); assert.equal(result.decision, 'DESCRIPTIVE_REPEAT_COMPLETE'); assert.equal(result.interpretation, 'INCOMPLETE_FOR_THREE_RUN_RULE'); assert.equal(result.effectiveness_evidence, false);
    assert.deepEqual(f.gateHashes, [shaFile(path.join(f.tmp, GATE_PATHS.PACKAGE_REVIEW)), shaFile(path.join(f.tmp, GATE_PATHS.EXECUTION_AUTHORIZATION))]);
  } finally { fs.rmSync(f.tmp, {recursive: true, force: true}); }
  assert.equal(fs.existsSync(f.tmp), false);
});
test('predecessor drift fails closed in static preflight', () => {
  const f = fixture();
  try {
    fs.appendFileSync(path.join(f.tmp, sourceRoot, 'README.md'), '\ncorruption\n');
    const value = preflight(f.pkg, f.tmp); assert.equal(value.decision, 'NO_GO_STATIC_INTEGRITY'); assert.ok(value.errors.includes('PREDECESSOR_TREE_DRIFT'));
    const result = postRun(f.pkg, f.tmp); assert.equal(result.decision, 'INVALID_ARTIFACTS'); assert.ok(result.errors.includes('PREDECESSOR_TREE_DRIFT'));
  } finally { fs.rmSync(f.tmp, {recursive: true, force: true}); }
  assert.equal(fs.existsSync(f.tmp), false);
});
test('ledger capture hash corruption invalidates derived state and result', () => {
  const f = fixture();
  try {
    runCell(f.pkg, f.tmp, CELLS[0], () => ({exit_code: 0, stdout: Buffer.from(JSON.stringify({status: 'SUCCESS', structured_output: empty})), stderr: Buffer.alloc(0), timed_out: false}));
    fs.appendFileSync(path.join(f.pkg, 'execution/captures/original-a-repeat-1.stdout.bin'), Buffer.from('x'));
    assert.ok(derive(f.pkg).errors.includes('CAPTURE_HASH_MISMATCH:original-a-repeat-1:stdout'));
    assert.equal(postRun(f.pkg, f.tmp).decision, 'INVALID_ARTIFACTS');
  } finally { fs.rmSync(f.tmp, {recursive: true, force: true}); }
  assert.equal(fs.existsSync(f.tmp), false);
});
test('canonical RAW corruption breaks stdout-to-RAW binding', () => {
  const f = fixture();
  try {
    runCell(f.pkg, f.tmp, CELLS[0], () => ({exit_code: 0, stdout: Buffer.from(JSON.stringify({status: 'SUCCESS', structured_output: empty})), stderr: Buffer.alloc(0), timed_out: false}));
    fs.appendFileSync(path.join(f.pkg, 'execution/RAW/original-a-repeat-1.json'), Buffer.from(' '));
    assert.ok(derive(f.pkg).errors.includes('RAW_CAPTURE_BINDING_MISMATCH:original-a-repeat-1'));
    assert.equal(postRun(f.pkg, f.tmp).decision, 'INVALID_ARTIFACTS');
  } finally { fs.rmSync(f.tmp, {recursive: true, force: true}); }
  assert.equal(fs.existsSync(f.tmp), false);
});
test('malformed first response gets FINISH and blocks every later cell without retry', () => {
  const f = fixture(); let calls = 0;
  try {
    const result = runCell(f.pkg, f.tmp, CELLS[0], () => { calls++; return {exit_code: 0, stdout: Buffer.from('{}'), stderr: Buffer.alloc(0), timed_out: false}; });
    assert.equal(result.envelope_schema_valid, false); assert.equal(calls, 1); assert.equal(derive(f.pkg).rows.at(-1).event, 'FINISH');
    assert.throws(() => runCell(f.pkg, f.tmp, CELLS[1], () => { calls++; return {}; }), /STOP_PREDECESSOR_CELL/); assert.equal(calls, 1);
  } finally { fs.rmSync(f.tmp, {recursive: true, force: true}); }
  assert.equal(fs.existsSync(f.tmp), false);
});
test('post-spawn exception still gets FINISH and consumes sole attempt', () => {
  const f = fixture();
  try { const result = runCell(f.pkg, f.tmp, CELLS[0], () => { throw Error('mock network'); }); assert.equal(result.process_success, false); assert.equal(derive(f.pkg).rows.at(-1).event, 'FINISH'); }
  finally { fs.rmSync(f.tmp, {recursive: true, force: true}); }
  assert.equal(fs.existsSync(f.tmp), false);
});
console.log(`1..${tests}`);
