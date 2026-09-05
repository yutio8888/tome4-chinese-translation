import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {readCanonical, shaFile, sha256, jsonBytes, writeExclusive} from './lib.mjs';
import {CELLS, REQUEST_BYTES, REQUEST_SHA256, SCHEMA_SHA256, splitRequest} from './freezer.mjs';
import {staticChecks} from './preflight.mjs';
import {validateGates} from './gates.mjs';
import {append, capturePaths, derive, finish, MAX_ATTEMPTS, PROCESS_BUDGET, start} from './ledger.mjs';
import {parseCapture} from './parser.mjs';
import {metrics} from './metrics.mjs';

const EXPECTED = '/home/yun/.local/lib/agy-pinned/f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e/agy';
const EXPECTED_HASH = 'f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e';

export function makePlan(root, cell) {
  if (!CELLS.includes(cell)) throw Error('UNKNOWN_CELL');
  const entry = readCanonical(path.join(root, 'frozen/REQUEST-MANIFEST.json')).requests.find(x => x.cell === cell);
  const requestBytes = fs.readFileSync(path.join(root, entry.path)), schemaBytes = fs.readFileSync(path.join(root, entry.schema));
  if (requestBytes.length !== REQUEST_BYTES || sha256(requestBytes) !== REQUEST_SHA256 || sha256(schemaBytes) !== SCHEMA_SHA256) throw Error('REQUEST_OR_SCHEMA_DRIFT');
  const route = readCanonical(path.join(root, 'ROUTE-CONTRACT.json'));
  const request = requestBytes.toString('utf8'), schema = schemaBytes.toString('utf8');
  const argv = route.cli_contract.argv_template.map(x => x === '[REQUEST_BYTES]' ? request : x === '[BUNDLE_SCHEMA]' ? schema : x);
  const env = Object.fromEntries(route.environment_allowlist.filter(key => process.env[key] !== undefined).map(key => [key, process.env[key]]));
  return {request, command: route.cli_contract.executable, argv, env, timeout_ms: route.cli_contract.timeout_ms};
}

export function verifyRoute(root, plan) {
  const route = readCanonical(path.join(root, 'ROUTE-CONTRACT.json')).cli_contract;
  if (route.executable !== EXPECTED || route.executable_sha256 !== EXPECTED_HASH || route.model !== 'gemini-3.7-flash-high' || route.effort !== 'high' || route.mode !== 'plan' || plan.command !== EXPECTED) throw Error('STOP_ROUTE_CONFIG');
  if (!fs.statSync(route.executable).isFile() || shaFile(route.executable) !== EXPECTED_HASH) throw Error('STOP_ROUTE_EXECUTABLE');
  const modelAt = plan.argv.indexOf('--model');
  if (modelAt < 0 || plan.argv[modelAt + 1] !== route.model || plan.argv.filter(x => x === '--model').length !== 1) throw Error('STOP_ROUTE_ARGV_MODEL');
}

const invoke = plan => {
  const result = spawnSync(plan.command, plan.argv, {env: plan.env, encoding: null, timeout: plan.timeout_ms, maxBuffer: 16 * 1024 * 1024});
  return {exit_code: Number.isInteger(result.status) ? result.status : -1, stdout: Buffer.from(result.stdout ?? ''), stderr: Buffer.from(result.stderr ?? ''), timed_out: result.error?.code === 'ETIMEDOUT'};
};
const errorBuffer = (error, key) => Buffer.from(Buffer.isBuffer(error?.[key]) ? error[key] : typeof error?.[key] === 'string' ? error[key] : '');

export function runCell(root, repoRoot, cell, systemInvoke = invoke) {
  const integrity = staticChecks(root, repoRoot); if (integrity.length) throw Error(`STATIC_INTEGRITY:${integrity.join(',')}`);
  const gates = validateGates(root, repoRoot); if (!gates.valid) throw Error(`GATES:${gates.errors.join(',')}`);
  const state = derive(root); if (state.errors.length) throw Error(`LEDGER:${state.errors.join(',')}`);
  if (MAX_ATTEMPTS !== 1 || state.agy_processes_spawned >= PROCESS_BUDGET) throw Error('STOP_BUDGET');
  if (state.unfinished || state.terminal_failure) throw Error('STOP_PREDECESSOR_CELL');
  const expected = CELLS[state.agy_processes_spawned];
  if (cell !== expected || state.cells[cell]) throw Error('CELL_ORDER_OR_ATTEMPT_EXHAUSTED');
  const paths = capturePaths(cell);
  if (Object.values(paths).some(rel => fs.existsSync(path.join(root, rel)))) throw Error('DYNAMIC_ARTIFACT_COLLISION');
  const plan = makePlan(root, cell);
  verifyRoute(root, plan);
  const startRow = start(cell); append(root, startRow);
  let result = {exit_code: -1, stdout: Buffer.alloc(0), stderr: Buffer.alloc(0), timed_out: false};
  let parsed = {valid: false, errors: ['POST_SPAWN_EXCEPTION'], normalized: null}, rawPath = null, cellMetrics = null, postSpawnError = null;
  try {
    try {
      const observed = systemInvoke(plan);
      result = {exit_code: Number.isInteger(observed?.exit_code) ? observed.exit_code : -1, stdout: Buffer.from(observed?.stdout ?? ''), stderr: Buffer.from(observed?.stderr ?? ''), timed_out: !!observed?.timed_out};
    } catch (error) { postSpawnError = error; result.stdout = errorBuffer(error, 'stdout'); result.stderr = errorBuffer(error, 'stderr'); }
    for (const [kind, bytes] of [['stdout', result.stdout], ['stderr', result.stderr]]) try { writeExclusive(path.join(root, paths[kind]), bytes); } catch (error) { postSpawnError ??= error; }
    const processSuccess = !postSpawnError && result.exit_code === 0 && !result.timed_out;
    if (processSuccess) {
      try {
        const input = splitRequest(Buffer.from(plan.request)).input; parsed = parseCapture(result.stdout, input);
        if (parsed.valid) {
          writeExclusive(path.join(root, paths.raw), jsonBytes({schema_version: 'gemini-original-a-repeat-raw-v1', cell, request_sha256: REQUEST_SHA256, schema_sha256: SCHEMA_SHA256, normalized_output: parsed.normalized}));
          rawPath = paths.raw; cellMetrics = metrics(parsed.normalized, input);
        }
      } catch (error) { postSpawnError ??= error; parsed = {valid: false, errors: [`POST_SPAWN:${error.message}`], normalized: null}; }
    } else parsed = {valid: false, errors: [postSpawnError ? `POST_SPAWN:${postSpawnError.message}` : 'PROCESS_FAILED'], normalized: null};
  } finally {
    const processSuccess = !postSpawnError && result.exit_code === 0 && !result.timed_out;
    append(root, finish(startRow, {exit_code: result.exit_code, stdout_sha256: sha256(result.stdout), stderr_sha256: sha256(result.stderr), process_success: processSuccess, envelope_schema_valid: processSuccess && parsed.valid, raw_path: rawPath}));
  }
  return {cell, attempt: 1, process_success: !postSpawnError && result.exit_code === 0 && !result.timed_out, envelope_schema_valid: !postSpawnError && parsed.valid, errors: parsed.errors, metrics: cellMetrics, continue_authorized: !postSpawnError && parsed.valid};
}
