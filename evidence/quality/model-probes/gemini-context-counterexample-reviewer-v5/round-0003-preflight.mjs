#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildRound3CandidateManifest, CANDIDATE_MANIFEST_PATH, ROUND3} from './round-0003-surface-input.mjs';
import {replayRound3} from './round-0003-replay.mjs';
import {jsonBytes, sha256} from './round-0003-surface-input.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..', '..', '..');
export function runRound3Preflight(root = here) {
  try {
    const replay = replayRound3(root, repo), manifestPath = path.join(repo, CANDIDATE_MANIFEST_PATH), manifestBytes = fs.readFileSync(manifestPath), manifest = JSON.parse(manifestBytes), expected = buildRound3CandidateManifest(repo);
    if (!manifestBytes.equals(jsonBytes(manifest)) || manifest.candidate_ref !== expected.candidate_ref || JSON.stringify(manifest.files) !== JSON.stringify(expected.files)) throw Error('ROUND3_CANDIDATE_MANIFEST_BINDING');
    return {decision:'NO_GO_ROUND_0003_SURFACE_INPUT_REVIEW_REQUIRED',static_integrity:'PASS',run_status:'ROUND_0003_SURFACE_INPUT_FROZEN_PENDING_INDEPENDENT_DUAL_REVIEW',...replay,candidate_ref:manifest.candidate_ref,candidate_manifest_path:CANDIDATE_MANIFEST_PATH,candidate_manifest_sha256:sha256(manifestBytes),candidate_file_count:manifest.files.length,blockers:['NORMAL_REVIEW_REQUIRED','SENIOR_REVIEW_REQUIRED','COMBINED_SURFACE_INPUT_REVIEW_GATE_REQUIRED','SURFACE_AUDITOR_CALL_NOT_AUTHORIZED','ROUND_0003_RELEASE_OR_REPLACEMENT_FORBIDDEN','ROUND_0004_FORBIDDEN']};
  } catch (error) { return {decision:'NO_GO_ROUND_0003_SURFACE_INPUT_INVALID',static_integrity:'FAIL_CLOSED',run_status:'ROUND_0003_SURFACE_INPUT_INVALID',completed_rounds:2,round_0003_release_created:false,round_0004_created:false,reason:error.code==='ENOENT'?'ROUND3_ARTIFACT_MISSING':error.message}; }
}
if (import.meta.url === `file://${process.argv[1]}`) { const result=runRound3Preflight(); console.log(JSON.stringify(result,null,2)); process.exitCode=result.decision==='NO_GO_ROUND_0003_SURFACE_INPUT_REVIEW_REQUIRED'?3:4; }
