#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateRound2CompletedReleaseEvidence} from './round-0002-release.mjs';
import {AUTHORIZATION_PATH, CANDIDATE_MANIFEST_PATH, ROUND3, validateRound3CandidateManifest, validateRound3DispatchReceipts, validateRound3SurfaceInput, sha256} from './round-0003-surface-input.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repoDefault = path.resolve(here, '..', '..', '..', '..');
export function replayRound3(root = here, repo = repoDefault) {
  if (fs.existsSync(path.join(root, 'rounds', 'ROUND-0004'))) throw Error('ROUND4_FORBIDDEN');
  const releaseEvidence = validateRound2CompletedReleaseEvidence(repo);
  const round = path.join(root, 'rounds', ROUND3.round_id), roundStat = fs.lstatSync(round);
  if (roundStat.isSymbolicLink() || !roundStat.isDirectory()) throw Error('ROUND3_DIRECTORY_FILE_TYPE');
  const names = fs.readdirSync(round).sort();
  if (fs.existsSync(path.join(round, 'RELEASE.json'))) throw Error('ROUND3_RELEASE_FORBIDDEN');
  if (JSON.stringify(names) !== JSON.stringify(['SURFACE-QUEUE-VIEW.json', 'SURFACE-QUEUE.json'])) throw Error('ROUND3_PENDING_ARTIFACT_SET');
  const candidate = validateRound3CandidateManifest(repo);
  const dispatches = validateRound3DispatchReceipts(repo, candidate);
  const queuePath = path.join(round, 'SURFACE-QUEUE.json'), viewPath = path.join(round, 'SURFACE-QUEUE-VIEW.json');
  for (const [file, label] of [[queuePath,'ROUND3_QUEUE'],[viewPath,'ROUND3_VIEW']]) { const stat = fs.lstatSync(file); if (stat.isSymbolicLink() || !stat.isFile()) throw Error(`${label}_FILE_TYPE`); }
  const queueBytes = fs.readFileSync(queuePath), viewBytes = fs.readFileSync(viewPath);
  const validated = validateRound3SurfaceInput({root, repo, queueBytes, viewBytes});
  return {status:'PASS',completed_rounds:2,last_release_sha256:releaseEvidence.release_sha256 ?? ROUND3.predecessor_release_sha256,authorization_path:AUTHORIZATION_PATH,authorization_sha256:validated.authorization.sha256,queue_sha256:validated.queue_sha256,view_sha256:validated.view_sha256,item_count:validated.queue.item_count,candidate_ref:candidate.candidate_ref,candidate_manifest_path:CANDIDATE_MANIFEST_PATH,candidate_manifest_sha256:candidate.sha256,candidate_file_count:candidate.file_count,normal_dispatch_sha256:dispatches.normal.sha256,senior_dispatch_sha256:dispatches.senior.sha256,active_frame_mutated:false,lineage_mutated:false,reserve_mutated:false,round_index_mutated:false,surface_auditor_call_authorized:false,round_0003_release_created:false,round_0004_created:false};
}
if (import.meta.url === `file://${process.argv[1]}`) console.log(JSON.stringify(replayRound3(), null, 2));
