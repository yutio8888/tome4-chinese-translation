#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {jsonBytes, sha256} from './round-lineage.mjs';
import {buildSurfaceQueueView} from './surface-queue-view.mjs';
import {buildRound2Authorization, buildRound2CandidateManifest, buildRound2SurfaceQueue, deriveRound2QueueItems, ROUND1_HASHES, ROUND2_AUTHORIZATION_PATH, ROUND2_CANDIDATE_MANIFEST_PATH, validateFrozenRound1Files, validateRound2CandidateManifest} from './round-0002-surface-input.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..', '..', '..');
const round2 = path.join(here, 'rounds', 'ROUND-0002');

function completedRound1State() {
  validateFrozenRound1Files(here);
  const active = JSON.parse(fs.readFileSync(path.join(here, 'ACTIVE-FRAME.json'))), lineage = JSON.parse(fs.readFileSync(path.join(here, 'LINEAGE.json')));
  if (active.last_completed_round !== 1 || lineage.last_completed_round !== 1 || active.initial_frame_sha256 !== lineage.initial_frame_sha256 || active.items.length !== 64 || lineage.items.length !== 64) throw Error('ROUND2_GENERATOR_COMPLETED_STATE');
  return {round: 1, lastReleaseSha256: ROUND1_HASHES.release, active: active.items, lineage: new Map(lineage.items.map(item => [item.neutral_id, item]))};
}

export function buildInputs() {
  const state = completedRound1State(), items = deriveRound2QueueItems(state);
  const authorization = jsonBytes(buildRound2Authorization(items));
  const queue = jsonBytes(buildRound2SurfaceQueue(items, authorization));
  const activeFrame = fs.readFileSync(path.join(here, 'ACTIVE-FRAME.json'));
  const view = jsonBytes(buildSurfaceQueueView({repo, queueBytes: queue, activeFrameBytes: activeFrame}));
  return {items, authorization, queue, view};
}

export function writeInputs() {
  const built = buildInputs();
  fs.mkdirSync(round2, {recursive: true});
  fs.writeFileSync(path.join(repo, ROUND2_AUTHORIZATION_PATH), built.authorization);
  fs.writeFileSync(path.join(round2, 'SURFACE-QUEUE.json'), built.queue);
  fs.writeFileSync(path.join(round2, 'SURFACE-QUEUE-VIEW.json'), built.view);
  return built;
}

export function writeManifest() {
  const bytes = jsonBytes(buildRound2CandidateManifest(repo));
  fs.writeFileSync(path.join(repo, ROUND2_CANDIDATE_MANIFEST_PATH), bytes);
  return JSON.parse(bytes);
}

function check() {
  const built = buildInputs();
  for (const [label, file, expected] of [
    ['authorization', path.join(repo, ROUND2_AUTHORIZATION_PATH), built.authorization],
    ['queue', path.join(round2, 'SURFACE-QUEUE.json'), built.queue],
    ['view', path.join(round2, 'SURFACE-QUEUE-VIEW.json'), built.view]
  ]) if (!fs.readFileSync(file).equals(expected)) throw Error(`ROUND2_GENERATOR_DRIFT:${label}`);
  const completed=fs.existsSync(path.join(round2,'SURFACE-RECORDS.json'))&&fs.existsSync(path.join(round2,'SURFACE-AGGREGATE.json'));
  const candidate=completed?{candidate_ref:'241478ba1b304224533660e06f171b609e01b2c7c872cc7358b0efd14cc70f09',sha256:'b8668b139f15279fda0b48a58fcfb482fb787ac1e1dc6a4cc71e4eb720ac22ed',file_count:102}:validateRound2CandidateManifest(repo);
  if(completed&&sha256(fs.readFileSync(path.join(repo,ROUND2_CANDIDATE_MANIFEST_PATH)))!==candidate.sha256)throw Error('ROUND2_REVIEWED_CANDIDATE_IDENTITY');
  return {status: 'PASS', item_count: built.items.length, queue_sha256: sha256(built.queue), view_sha256: sha256(built.view), candidate_ref: candidate.candidate_ref, candidate_manifest_sha256: candidate.sha256, candidate_file_count: candidate.file_count, surface_results_materialized:completed};
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const command = process.argv[2];
  if (command === '--write-inputs') {
    const built = writeInputs(); console.log(JSON.stringify({status: 'WROTE_INPUTS', item_count: built.items.length, queue_sha256: sha256(built.queue), view_sha256: sha256(built.view)}, null, 2));
  } else if (command === '--write-manifest') {
    const manifest = writeManifest(); console.log(JSON.stringify({status: 'WROTE_MANIFEST', candidate_ref: manifest.candidate_ref, file_count: manifest.files.length}, null, 2));
  } else if (command === '--check') console.log(JSON.stringify(check(), null, 2));
  else throw Error('usage: node generate-round-0002-surface-input.mjs --write-inputs|--write-manifest|--check');
}
