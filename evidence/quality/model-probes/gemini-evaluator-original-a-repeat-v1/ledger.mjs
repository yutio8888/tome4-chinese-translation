import fs from 'node:fs';
import path from 'node:path';
import {exactKeys, jsonBytes, parseNoDuplicate, shaFile} from './lib.mjs';
import {CELLS, REQUEST, REQUEST_SHA256, SCHEMA_SHA256, splitRequest} from './freezer.mjs';
import {parseCapture} from './parser.mjs';

export const LEDGER = 'execution/LEDGER.jsonl', MAX_ATTEMPTS = 1, PROCESS_BUDGET = 3, INFERENCE_BUDGET = 3;
export const START_KEYS = ['event', 'cell', 'attempt', 'started_at'];
export const FINISH_KEYS = ['event', 'cell', 'attempt', 'started_at', 'finished_at', 'exit_code', 'stdout_sha256', 'stderr_sha256', 'process_success', 'envelope_schema_valid', 'raw_path'];
export const start = (cell, started_at = new Date().toISOString()) => ({event: 'START', cell, attempt: 1, started_at});
export const finish = (row, values, finished_at = new Date().toISOString()) => ({event: 'FINISH', cell: row.cell, attempt: 1, started_at: row.started_at, finished_at, ...values});
export const capturePaths = cell => ({stdout: `execution/captures/${cell}.stdout.bin`, stderr: `execution/captures/${cell}.stderr.bin`, raw: `execution/RAW/${cell}.json`});

export function append(root, row) {
  const file = path.join(root, LEDGER); fs.mkdirSync(path.dirname(file), {recursive: true}); fs.appendFileSync(file, `${JSON.stringify(row)}\n`);
}

export function derive(root) {
  const file = path.join(root, LEDGER), errors = [], rows = [];
  if (fs.existsSync(file)) {
    const text = fs.readFileSync(file, 'utf8');
    if (text && !text.endsWith('\n')) errors.push('PARTIAL_LINE');
    for (const [i, line] of (text ? text.trimEnd().split('\n') : []).entries()) try { rows.push(parseNoDuplicate(line, `LEDGER:${i + 1}`)); } catch (error) { errors.push(error.message); }
  }
  const cells = {}, starts = [];
  for (const row of rows) {
    if (row.event === 'START') {
      if (!exactKeys(row, START_KEYS)) { errors.push(`START_KEYS:${row.cell ?? 'UNKNOWN'}`); continue; }
      starts.push(row);
      const expected = CELLS[starts.length - 1];
      if (row.cell !== expected || row.attempt !== 1 || cells[row.cell]) errors.push(`START_INVALID:${row.cell}`);
      else cells[row.cell] = {start: row, finish: null};
    } else if (row.event === 'FINISH') {
      if (!exactKeys(row, FINISH_KEYS)) { errors.push(`FINISH_KEYS:${row.cell ?? 'UNKNOWN'}`); continue; }
      const cell = cells[row.cell];
      if (!cell || cell.finish || row.attempt !== 1 || row.started_at !== cell.start.started_at) errors.push(`FINISH_INVALID:${row.cell}`);
      else cell.finish = row;
    } else errors.push('EVENT_INVALID');
  }
  if (starts.length > PROCESS_BUDGET) errors.push('PROCESS_BUDGET_EXCEEDED');
  let input = null;
  try { input = splitRequest(fs.readFileSync(path.join(root, REQUEST))).input; } catch (error) { errors.push(`REQUEST_FOR_CAPTURE_VALIDATION:${error.message}`); }
  for (const [cellName, cell] of Object.entries(cells)) {
    const row = cell.finish;
    if (!row) continue;
    const paths = capturePaths(cellName);
    for (const kind of ['stdout', 'stderr']) {
      const rel = paths[kind], filePath = path.join(root, rel), recorded = row[`${kind}_sha256`];
      if (!/^[0-9a-f]{64}$/u.test(recorded) || !fs.existsSync(filePath) || shaFile(filePath) !== recorded) errors.push(`CAPTURE_HASH_MISMATCH:${cellName}:${kind}`);
    }
    if (!input || !fs.existsSync(path.join(root, paths.stdout))) continue;
    const parsed = parseCapture(fs.readFileSync(path.join(root, paths.stdout)), input);
    const expectedValid = row.process_success === true && parsed.valid;
    if (typeof row.process_success !== 'boolean' || typeof row.envelope_schema_valid !== 'boolean' || row.envelope_schema_valid !== expectedValid) errors.push(`FINISH_VALIDITY_MISMATCH:${cellName}`);
    const rawFile = path.join(root, paths.raw);
    if (expectedValid) {
      const expected = jsonBytes({schema_version: 'gemini-original-a-repeat-raw-v1', cell: cellName, request_sha256: REQUEST_SHA256, schema_sha256: SCHEMA_SHA256, normalized_output: parsed.normalized});
      if (row.raw_path !== paths.raw || !fs.existsSync(rawFile) || !fs.readFileSync(rawFile).equals(expected)) errors.push(`RAW_CAPTURE_BINDING_MISMATCH:${cellName}`);
    } else if (row.raw_path !== null || fs.existsSync(rawFile)) errors.push(`UNEXPECTED_RAW:${cellName}`);
  }
  const unfinished = Object.values(cells).find(x => !x.finish);
  const terminalFailure = Object.values(cells).some(x => x.finish && (!x.finish.process_success || !x.finish.envelope_schema_valid));
  if (terminalFailure && starts.length > Object.values(cells).findIndex(x => x.finish && (!x.finish.process_success || !x.finish.envelope_schema_valid)) + 1) errors.push('START_AFTER_TERMINAL_FAILURE');
  return {errors, rows, cells, agy_processes_spawned: starts.length, inference_calls_made: starts.length, no_run: rows.length === 0, unfinished: !!unfinished, terminal_failure: terminalFailure};
}
