#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateRound2CompletedReleaseEvidence} from './round-0002-release.mjs';
import {AUTHORIZATION_PATH,ROUND3,validateRound3SurfaceInput,sha256} from './round-0003-surface-input.mjs';
import {validateRound3SurfaceArtifacts} from './round-0003-surface-results.mjs';
import {CONTEXT_CANDIDATE_PATH,validateRound3ContextCandidate,validateRound3ContextInput} from './round-0003-context-input.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),repoDefault=path.resolve(here,'..','..','..','..');
const EXPECTED_FILES=['CONTEXT-QUEUE-VIEW.json','CONTEXT-QUEUE.json','CONTEXT-SOURCE-ANCHORS.json','SURFACE-AGGREGATE.json','SURFACE-QUEUE-VIEW.json','SURFACE-QUEUE.json','SURFACE-RECORDS.json'];
const STAGE_A_GATE='.ai/task/research-gemini-context-counterexample-reviewer-v5/ROUND-0003-SURFACE-INPUT-REVIEW-GATE-001.json',STAGE_A_GATE_SHA='3fe57f2693477a32b7293fb715037894fd6771a2870818497846c1512d15b95c';
function regular(file,label){const stat=fs.lstatSync(file);if(stat.isSymbolicLink()||!stat.isFile())throw Error(`${label}_FILE_TYPE`);return fs.readFileSync(file);}
export function replayRound3Context(root=here,repo=repoDefault){
  if(fs.existsSync(path.join(root,'rounds/ROUND-0004')))throw Error('ROUND4_FORBIDDEN');
  const release=validateRound2CompletedReleaseEvidence(repo),round=path.join(root,'rounds/ROUND-0003'),stat=fs.lstatSync(round);if(stat.isSymbolicLink()||!stat.isDirectory())throw Error('ROUND3_DIRECTORY_FILE_TYPE');
  const names=fs.readdirSync(round).sort();if(JSON.stringify(names)!==JSON.stringify(EXPECTED_FILES))throw Error('ROUND3_CONTEXT_PENDING_ARTIFACT_SET');if(fs.existsSync(path.join(round,'RELEASE.json')))throw Error('ROUND3_RELEASE_FORBIDDEN');
  const gate=regular(path.join(repo,STAGE_A_GATE),'ROUND3_STAGE_A_GATE');if(sha256(gate)!==STAGE_A_GATE_SHA)throw Error('ROUND3_STAGE_A_GATE_HASH');const gateValue=JSON.parse(gate);if(gateValue.permitted_next_action!=='GO_ROUND_0003_SURFACE_AUDITOR_CALL_ONLY'||gateValue.authorized_input_boundary?.payload_sha256!=='f1f35c1a1c28638c706630b45422efa6b94380b8ff89397fecef78c4f3e6ca0b')throw Error('ROUND3_STAGE_A_GATE_BINDING');
  const surfaceInput=validateRound3SurfaceInput({root,repo,queueBytes:regular(path.join(round,'SURFACE-QUEUE.json'),'ROUND3_QUEUE'),viewBytes:regular(path.join(round,'SURFACE-QUEUE-VIEW.json'),'ROUND3_VIEW')});
  const surface=validateRound3SurfaceArtifacts({root}),context=validateRound3ContextInput({root,repo}),candidate=validateRound3ContextCandidate(repo);
  return {status:'PASS',completed_rounds:2,last_release_sha256:release.release_sha256??ROUND3.predecessor_release_sha256,public_phase:'ROUND_0003_CONTEXT_INPUT',authorization_path:AUTHORIZATION_PATH,authorization_sha256:surfaceInput.authorization.sha256,stage_a_gate_sha256:STAGE_A_GATE_SHA,surface_queue_sha256:surfaceInput.queue_sha256,surface_queue_view_sha256:surfaceInput.view_sha256,raw_surface_response_sha256:surface.raw_response_sha256,surface_records_sha256:surface.surface_records_sha256,surface_aggregate_sha256:surface.surface_aggregate_sha256,surface_item_count:2,surface_counts:surface.counts,surface_calls_started:1,surface_calls_remaining:0,context_queue_sha256:context.context_queue_sha256,context_source_anchors_sha256:context.context_source_anchors_sha256,context_queue_view_sha256:context.context_queue_view_sha256,context_item_count:context.item_count,context_source_file_count:context.source_file_count,candidate_ref:candidate.candidate_ref,candidate_manifest_path:CONTEXT_CANDIDATE_PATH,candidate_manifest_sha256:candidate.sha256,candidate_file_count:candidate.file_count,active_frame_mutated:false,lineage_mutated:false,reserve_mutated:false,round_index_mutated:false,context_auditor_call_authorized:false,context_auditor_calls_started:0,context_records_created:false,context_aggregate_created:false,round_0003_release_created:false,round_0004_created:false};
}
if(import.meta.url===`file://${process.argv[1]}`)console.log(JSON.stringify(replayRound3Context(),null,2));
