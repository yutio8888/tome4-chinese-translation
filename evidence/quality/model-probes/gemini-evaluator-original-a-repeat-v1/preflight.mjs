#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {checkManifest, sourcePaths} from './build-manifest.mjs';
import {checkFreeze, REQUEST, REQUEST_BYTES, REQUEST_SHA256, SCHEMA, SCHEMA_SHA256, CELLS} from './freezer.mjs';
import {derive} from './ledger.mjs';
import {validateGates} from './gates.mjs';
import {readCanonical, shaFile, treeBinding} from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url)), repo = path.resolve(here, '../../../..');
export function staticChecks(root = here, repoRoot = repo) {
  const errors = [...checkManifest(root).map(x => `manifest:${x}`)];
  errors.push(...checkFreeze(root).errors.map(x => `freeze:${x}`));
  const exp = readCanonical(path.join(root, 'EXPERIMENT.json'));
  try {
    const predecessor = treeBinding(repoRoot, exp.predecessor.root);
    if (predecessor.file_count !== exp.predecessor.file_count || predecessor.tree_sha256 !== exp.predecessor.tree_sha256) errors.push('PREDECESSOR_TREE_DRIFT');
  } catch (error) { errors.push(`PREDECESSOR_TREE_UNREADABLE:${error.message}`); }
  const pairs = [[REQUEST, exp.source_request.path, REQUEST_SHA256, REQUEST_BYTES], [SCHEMA, exp.source_schema.path, SCHEMA_SHA256, null]];
  for (const [local, source, hash, size] of pairs) {
    const localBytes = fs.readFileSync(path.join(root, local)), sourceBytes = fs.readFileSync(path.join(repoRoot, source));
    if (!localBytes.equals(sourceBytes) || shaFile(path.join(root, local)) !== hash || (size !== null && localBytes.length !== size)) errors.push(`STATIC_SOURCE_DRIFT:${local}`);
  }
  for (const rel of sourcePaths(root).filter(x => x.endsWith('.json'))) try { readCanonical(path.join(root, rel)); } catch (error) { errors.push(`json:${error.message}`); }
  if (fs.existsSync(path.join(root, 'sealed'))) errors.push('FORBIDDEN_SEALED_ARTIFACT');
  for (const rel of sourcePaths(root)) if (/reference|capture|raw/i.test(rel)) errors.push(`FORBIDDEN_STATIC_INPUT:${rel}`);
  return errors;
}
export function preflight(root = here, repoRoot = repo) {
  const errors = staticChecks(root, repoRoot), state = derive(root); errors.push(...state.errors.map(x => `ledger:${x}`));
  const gates = validateGates(root, repoRoot);
  return {schema_version: 'gemini-original-a-repeat-preflight-v1', decision: errors.length ? 'NO_GO_STATIC_INTEGRITY' : gates.valid ? 'GO' : 'NO_GO_REQUIRED_GATES', execution_state: state.no_run ? 'NO_RUN' : 'PARTIAL_OR_COMPLETE', static_integrity: errors.length ? 'FAIL' : 'PASS', manifest_sha256: fs.existsSync(path.join(root, 'MANIFEST.json')) ? shaFile(path.join(root, 'MANIFEST.json')) : null, registered_cells: CELLS, blocked_gates: gates.errors.filter(x => x.startsWith('MISSING:')).map(x => x.slice(8)), agy_processes_spawned: state.agy_processes_spawned, inference_calls_made: state.inference_calls_made, errors};
}
if (import.meta.url === `file://${process.argv[1]}`) { const x = preflight(); console.log(JSON.stringify(x, null, 2)); process.exitCode = x.decision === 'GO' ? 0 : 3; }
