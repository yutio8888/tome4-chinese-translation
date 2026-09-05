#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {checkManifest} from './build-manifest.mjs';
import {CELLS, REQUEST, REQUEST_BYTES, REQUEST_SHA256, SCHEMA_SHA256, splitRequest} from './freezer.mjs';
import {capturePaths, derive} from './ledger.mjs';
import {interpret, metrics} from './metrics.mjs';
import {jsonBytes, readCanonical, shaFile, treeBinding, writeExclusive} from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url)), repo = path.resolve(here, '../../../..');
export const POWER_CAVEAT = 'Three runs can reveal observed run-to-run variation but have low power: uniform outcomes do not establish determinism or exclude stochastic/sample-dependent behavior.';
export const CACHE_CAVEAT = 'The three calls may share provider-side caching, infrastructure, or hidden state and therefore are not asserted to be statistically independent.';
export const ROUTE_CAVEAT = 'Route attestation is local-tier only: the package verifies the pinned executable hash and requested argv model immediately before spawn, not the provider-side served model identity.';
export function postRun(root = here, repoRoot = repo, {write = false} = {}) {
  const state = derive(root), errors = [...checkManifest(root), ...state.errors], exp = readCanonical(path.join(root, 'EXPERIMENT.json'));
  try {
    const predecessor = treeBinding(repoRoot, exp.predecessor.root);
    if (predecessor.file_count !== exp.predecessor.file_count || predecessor.tree_sha256 !== exp.predecessor.tree_sha256) errors.push('PREDECESSOR_TREE_DRIFT');
  } catch (error) { errors.push(`PREDECESSOR_TREE_UNREADABLE:${error.message}`); }
  const bindings = {predecessor_tree_sha256: exp.predecessor.tree_sha256, predecessor_file_count: exp.predecessor.file_count, request_sha256: REQUEST_SHA256, request_utf8_bytes: REQUEST_BYTES, schema_sha256: SCHEMA_SHA256, manifest_sha256: shaFile(path.join(root, 'MANIFEST.json'))};
  const caveats = {three_run_power: POWER_CAVEAT, caching_and_non_independence: CACHE_CAVEAT, route_attestation: ROUTE_CAVEAT};
  if (state.no_run) return {schema_version: 'gemini-original-a-repeat-result-v1', decision: errors.length ? 'INVALID_ARTIFACTS' : 'NO_RUN', effectiveness_evidence: false, bindings, caveats, agy_processes_spawned: 0, inference_calls_made: 0, runs: [], interpretation: 'INCOMPLETE_FOR_THREE_RUN_RULE', artifacts: {}, errors};
  const input = splitRequest(fs.readFileSync(path.join(root, REQUEST))).input, runs = [], artifacts = {ledger: {path: 'execution/LEDGER.jsonl', sha256: shaFile(path.join(root, 'execution/LEDGER.jsonl'))}};
  for (const [index, cell] of CELLS.entries()) {
    const entry = state.cells[cell], finish = entry?.finish;
    const previousFinish = index ? state.cells[CELLS[index - 1]]?.finish : null;
    const gap = previousFinish && entry?.start ? Date.parse(entry.start.started_at) - Date.parse(previousFinish.finished_at) : null;
    let runMetrics = null;
    if (finish?.process_success && finish.envelope_schema_valid && finish.raw_path) {
      try { runMetrics = metrics(readCanonical(path.join(root, finish.raw_path)).normalized_output, input); } catch (error) { errors.push(`${cell}:${error.message}`); }
    }
    runs.push({cell, attempted: !!entry, process_success: finish?.process_success ?? false, envelope_schema_valid: finish?.envelope_schema_valid ?? false, timing: entry ? {started_at: entry.start.started_at, finished_at: finish?.finished_at ?? null, gap_from_previous_finish_ms: Number.isFinite(gap) ? gap : null} : null, metrics: runMetrics});
    for (const [kind, rel] of Object.entries(capturePaths(cell))) if (fs.existsSync(path.join(root, rel))) artifacts[`${cell}:${kind}`] = {path: rel, sha256: shaFile(path.join(root, rel))};
  }
  const classification = interpret(runs), complete = state.agy_processes_spawned === 3 && runs.every(x => x.process_success && x.envelope_schema_valid);
  const output = {schema_version: 'gemini-original-a-repeat-result-v1', decision: errors.length ? 'INVALID_ARTIFACTS' : complete ? 'DESCRIPTIVE_REPEAT_COMPLETE' : 'REPEAT_STOPPED', effectiveness_evidence: false, bindings, caveats, agy_processes_spawned: state.agy_processes_spawned, inference_calls_made: state.inference_calls_made, runs, interpretation: classification, historical_bound_observation: complete ? {predecessor_decision: 'NO_GO_A_PARSE_INVALID'} : null, artifacts, errors};
  if (write) {
    const file = path.join(root, 'RESULT.json'), bytes = jsonBytes(output);
    if (fs.existsSync(file)) { if (!fs.readFileSync(file).equals(bytes)) throw Error('RESULT_DRIFT'); }
    else writeExclusive(file, bytes);
  }
  return output;
}
if (import.meta.url === `file://${process.argv[1]}`) { const result = postRun(here, repo, {write: process.argv.includes('--write')}); console.log(JSON.stringify(result, null, 2)); process.exitCode = ['NO_RUN', 'DESCRIPTIVE_REPEAT_COMPLETE'].includes(result.decision) ? 0 : 3; }
