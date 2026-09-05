import fs from 'node:fs';
import path from 'node:path';
import {exactKeys, readCanonical, shaFile} from './lib.mjs';
import {CELLS} from './freezer.mjs';

export const TASK = 'research-gemini-evaluator-original-a-repeat-v1';
export const GATE_PATHS = {PACKAGE_REVIEW: `.ai/task/${TASK}/PACKAGE_REVIEW.json`, EXECUTION_AUTHORIZATION: `.ai/task/${TASK}/EXECUTION_AUTHORIZATION.json`};

export function validateGates(root, repoRoot) {
  const errors = [], gates = {}, manifest = shaFile(path.join(root, 'MANIFEST.json'));
  for (const [name, rel] of Object.entries(GATE_PATHS)) {
    const file = path.join(repoRoot, rel);
    if (!fs.existsSync(file)) { errors.push(`MISSING:${name}`); continue; }
    try { gates[name] = readCanonical(file); } catch (error) { errors.push(`${name}:${error.message}`); }
  }
  const review = gates.PACKAGE_REVIEW;
  if (review && (!exactKeys(review, ['schema_version', 'task_id', 'decision', 'manifest_sha256', 'authorized_cells']) || review.schema_version !== 'gemini-original-a-repeat-package-review-v1' || review.task_id !== TASK || review.decision !== 'PASS' || review.manifest_sha256 !== manifest || JSON.stringify(review.authorized_cells) !== JSON.stringify(CELLS))) errors.push('PACKAGE_REVIEW_INVALID');
  const auth = gates.EXECUTION_AUTHORIZATION;
  if (auth && (!exactKeys(auth, ['schema_version', 'task_id', 'decision', 'manifest_sha256', 'package_review_sha256', 'authorized_cells', 'agy_process_budget', 'inference_call_budget', 'max_attempts', 'retries']) || auth.schema_version !== 'gemini-original-a-repeat-execution-authorization-v1' || auth.task_id !== TASK || auth.decision !== 'AUTHORIZED' || auth.manifest_sha256 !== manifest || auth.package_review_sha256 !== (review ? shaFile(path.join(repoRoot, GATE_PATHS.PACKAGE_REVIEW)) : null) || JSON.stringify(auth.authorized_cells) !== JSON.stringify(CELLS) || auth.agy_process_budget !== 3 || auth.inference_call_budget !== 3 || auth.max_attempts !== 1 || auth.retries !== 0)) errors.push('EXECUTION_AUTHORIZATION_INVALID');
  return {valid: errors.length === 0, errors, gates};
}
