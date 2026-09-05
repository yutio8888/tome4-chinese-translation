#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildRound3Authorization, buildRound3CandidateManifest, buildRound3SurfaceQueue, independentlyVerifyCompleted2, validateRound3SurfaceInput, AUTHORIZATION_PATH, CANDIDATE_MANIFEST_PATH, jsonBytes, PACKAGE_ROOT, ROUND3, sha256} from './round-0003-surface-input.mjs';
import {buildSurfaceQueueView} from './surface-queue-view.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..', '..', '..');
const round = path.join(here, 'rounds', ROUND3.round_id);

export function buildInputs() {
  const verified = independentlyVerifyCompleted2(here, repo);
  const authorization = jsonBytes(buildRound3Authorization(verified.rows));
  const queue = jsonBytes(buildRound3SurfaceQueue(verified.rows, authorization));
  const active = fs.readFileSync(path.join(here, 'ACTIVE-FRAME.json'));
  const view = jsonBytes(buildSurfaceQueueView({repo, queueBytes: queue, activeFrameBytes: active}));
  const viewObject = JSON.parse(view); viewObject.status = 'FROZEN_ROUND_0003_SURFACE_AUDITOR_INPUT_PENDING_REVIEW';
  return {authorization, queue, view: jsonBytes(viewObject), rows: verified.rows};
}
export function writeInputs() {
  const built = buildInputs();
  fs.mkdirSync(round, {recursive: true});
  fs.writeFileSync(path.join(repo, AUTHORIZATION_PATH), built.authorization);
  fs.writeFileSync(path.join(round, 'SURFACE-QUEUE.json'), built.queue);
  fs.writeFileSync(path.join(round, 'SURFACE-QUEUE-VIEW.json'), built.view);
  return built;
}
export function writeManifest() { const manifest = buildRound3CandidateManifest(repo); fs.writeFileSync(path.join(repo, CANDIDATE_MANIFEST_PATH), jsonBytes(manifest)); return manifest; }
function check() {
  const built = buildInputs();
  for (const [name, file, bytes] of [['authorization', path.join(repo, AUTHORIZATION_PATH), built.authorization], ['queue', path.join(round,'SURFACE-QUEUE.json'), built.queue], ['view', path.join(round,'SURFACE-QUEUE-VIEW.json'), built.view]]) if (!fs.existsSync(file) || !fs.readFileSync(file).equals(bytes)) throw Error(`ROUND3_GENERATOR_DRIFT:${name}`);
  const result = validateRound3SurfaceInput({root: here, repo, queueBytes: built.queue, viewBytes: built.view});
  const manifest = buildRound3CandidateManifest(repo);
  return {status:'PASS', item_count:result.queue.item_count, queue_sha256:sha256(built.queue), view_sha256:sha256(built.view), candidate_ref:manifest.candidate_ref, candidate_manifest_sha256:sha256(jsonBytes(manifest)), candidate_file_count:manifest.files.length, surface_auditor_call_authorized:false, round_0004_created:false};
}
if (import.meta.url === `file://${process.argv[1]}`) { const command = process.argv[2]; if (command === '--write-inputs') { const b=writeInputs(); console.log(JSON.stringify({status:'WROTE_INPUTS',item_count:b.rows.length,queue_sha256:sha256(b.queue),view_sha256:sha256(b.view)},null,2)); } else if (command === '--write-manifest') console.log(JSON.stringify(writeManifest(),null,2)); else if (command === '--check') console.log(JSON.stringify(check(),null,2)); else throw Error('usage: node generate-round-0003-surface-input.mjs --write-inputs|--write-manifest|--check'); }
