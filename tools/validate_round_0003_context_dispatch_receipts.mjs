#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const repoDefault=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const task='.ai/task/research-gemini-context-counterexample-reviewer-v5';
const manifestPath=`${task}/ROUND-0003-CONTEXT-INPUT-IMPLEMENTATION-CANDIDATE-MANIFEST.json`;
const lifecycle={
  normalDispatch:`${task}/ROUND-0003-CONTEXT-INPUT-NORMAL-DISPATCH-RECEIPT-001.json`,
  seniorDispatch:`${task}/ROUND-0003-CONTEXT-INPUT-SENIOR-DISPATCH-RECEIPT-001.json`,
  normalCompletion:`${task}/ROUND-0003-CONTEXT-INPUT-NORMAL-COMPLETION-RECEIPT-001.json`,
  seniorCompletion:`${task}/ROUND-0003-CONTEXT-INPUT-SENIOR-COMPLETION-RECEIPT-001.json`,
  normalReview:`${task}/ROUND-0003-CONTEXT-INPUT-NORMAL-REVIEW-001.json`,
  seniorReview:`${task}/ROUND-0003-CONTEXT-INPUT-SENIOR-REVIEW-001.json`,
  gate:`${task}/ROUND-0003-CONTEXT-INPUT-REVIEW-GATE-001.json`
};
const candidateRef='eee2e29687da787564f4d0f0a58c5da9c5cb89fcf938af509dd7bb39dd2b8db5';
const manifestSha='a879250e76b38d784e552cc357cedc86a41c0d72eb9d109cea113ac8f4665e81';
const contextViewPath='evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0003/CONTEXT-QUEUE-VIEW.json';
const contextViewSha='900fe68d898303e1fcd64567119c33d6471119a5b9a5cbfc74ad41cc7dc0e44e';
const dispatchKeys=['schema_version','round_id','stage','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','agent_created_at','dispatched_at','orchestrator_authorization_scope','expected_permitted_read_only_task','completion_absent','receipt_id','role','agent_id','route','dispatch_id','opus_quota_override'];
const completionKeys=['schema_version','receipt_id','round_id','stage','role','agent_id','route','dispatch_id','dispatch_receipt_path','dispatch_receipt_sha256','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','status','lifecycle','completed_at','response_sha256','verdict','response_text'];
const reviewKeys=['schema_version','review_id','round_id','stage','role','agent_id','route','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','dispatch_id','dispatch_receipt_path','dispatch_receipt_sha256','completion_receipt_path','completion_receipt_sha256','completion_status','response_sha256','findings','repository_modified_by_review','recorded_at'];
const gateKeys=['schema_version','gate_id','round_id','stage','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','normal_review','senior_review','authorized_input_boundary','auditor_call_contract','permitted_next_action','forbidden_before_valid_auditor_output','recorded_at','sole_writer_agent_id'];
const scope={candidate_read_only:true,production_materialization:false,derived_state_mutation:false,context_auditor_call:false,round_0003_release:false,round_0003_replacement:false,round_0004:false};
const expected={normal:{role:'REVIEWER',route:'Codex gpt-5.6-sol xhigh',receiptRole:'NORMAL',dispatchRoute:'CODEX',override:false},senior:{role:'SENIOR_REVIEWER',route:'Gemini 3.7 Flash high',receiptRole:'SENIOR',dispatchRoute:'GEMINI',override:true}};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const jsonBytes=v=>Buffer.from(`${JSON.stringify(v,null,2)}\n`);
const exact=(v,k)=>v&&typeof v==='object'&&!Array.isArray(v)&&JSON.stringify(Object.keys(v).sort())===JSON.stringify([...k].sort());
function regular(repo,relative,label){const file=path.join(repo,relative),stat=fs.lstatSync(file);if(stat.isSymbolicLink()||!stat.isFile())throw Error(`${label}_FILE_TYPE`);const bytes=fs.readFileSync(file);let value;try{value=JSON.parse(bytes);}catch{throw Error(`${label}_JSON`);}if(!bytes.equals(jsonBytes(value)))throw Error(`${label}_NONCANONICAL`);return {bytes,value};}
function timestamp(v){return typeof v==='string'&&!Number.isNaN(Date.parse(v))&&new Date(v).toISOString()===v;}
function validateDispatches(repo){
  const manifest=regular(repo,manifestPath,'ROUND3_CONTEXT_MANIFEST');
  if(sha(manifest.bytes)!==manifestSha||manifest.value.candidate_ref!==candidateRef||manifest.value.files?.length!==191)throw Error('ROUND3_CONTEXT_MANIFEST_BINDING');
  if(sha(Buffer.from(manifest.value.files.map(x=>`${x.path}\0${x.sha256}\n`).join('')))!==candidateRef)throw Error('ROUND3_CONTEXT_CANDIDATE_ROOT');
  for(const item of manifest.value.files){const stat=fs.lstatSync(path.join(repo,item.path));if(stat.isSymbolicLink()||!stat.isFile()||sha(fs.readFileSync(path.join(repo,item.path)))!==item.sha256)throw Error(`ROUND3_CONTEXT_CANDIDATE_FILE_HASH:${item.path}`);}
  const out={};
  for(const [kind,e] of Object.entries(expected)){
    const relative=lifecycle[`${kind}Dispatch`],record=regular(repo,relative,`ROUND3_CONTEXT_${kind.toUpperCase()}_DISPATCH`),v=record.value;
    const receipt=typeof v.receipt_id==='string'&&v.receipt_id.match(new RegExp(`^V5-ROUND-0003-CONTEXT-INPUT-${e.receiptRole}-DISPATCH-RECEIPT-(\\d{3})$`,'u'));
    const dispatch=typeof v.dispatch_id==='string'&&v.dispatch_id.match(new RegExp(`^V5-R3-CONTEXT-INPUT-DISPATCH-${e.dispatchRoute}-([0-9A-F]{8})-(\\d{3})$`,'u'));
    if(!exact(v,dispatchKeys)||v.schema_version!=='gemini-context-v5-round-0003-context-input-review-dispatch-receipt-v1'||v.round_id!=='ROUND-0003'||v.stage!=='CONTEXT_INPUT'||v.status!=='DISPATCHED'||v.candidate_ref!==candidateRef||v.candidate_manifest_path!==manifestPath||v.candidate_manifest_sha256!==manifestSha||!timestamp(v.agent_created_at)||!timestamp(v.dispatched_at)||Date.parse(v.agent_created_at)>Date.parse(v.dispatched_at)||JSON.stringify(v.orchestrator_authorization_scope)!==JSON.stringify(scope)||v.expected_permitted_read_only_task!=='READ_ONLY_REVIEW_OF_ROUND_0003_CONTEXT_INPUT_IMPLEMENTATION_CANDIDATE'||v.completion_absent!==true||v.role!==e.role||!/^[0-9a-f-]{36}$/u.test(v.agent_id)||v.route!==e.route||v.opus_quota_override!==e.override||!receipt||!dispatch||receipt[1]!==dispatch[2]||dispatch[1]!==v.agent_id.slice(0,8).toUpperCase())throw Error(`ROUND3_CONTEXT_${kind.toUpperCase()}_DISPATCH_BINDING`);
    out[kind]={path:relative,sha256:sha(record.bytes),value:v,cycle:receipt[1]};
  }
  if(out.normal.value.agent_id===out.senior.value.agent_id||out.normal.value.dispatch_id===out.senior.value.dispatch_id)throw Error('ROUND3_CONTEXT_DISPATCH_INDEPENDENCE');
  return out;
}
function validateFinal(repo,dispatches){
  const refs={};
  for(const [kind,e] of Object.entries(expected)){
    const cap=kind[0].toUpperCase()+kind.slice(1),completionPath=lifecycle[`${kind}Completion`],reviewPath=lifecycle[`${kind}Review`];
    const completion=regular(repo,completionPath,`ROUND3_CONTEXT_${kind.toUpperCase()}_COMPLETION`),c=completion.value,d=dispatches[kind];
    if(!exact(c,completionKeys)||c.schema_version!=='gemini-context-v5-round-0003-context-input-review-completion-receipt-v1'||c.receipt_id!==`V5-ROUND-0003-CONTEXT-INPUT-${e.receiptRole}-COMPLETION-RECEIPT-${d.cycle}`||c.round_id!=='ROUND-0003'||c.stage!=='CONTEXT_INPUT'||c.role!==e.role||c.agent_id!==d.value.agent_id||c.route!==e.route||c.dispatch_id!==d.value.dispatch_id||c.dispatch_receipt_path!==d.path||c.dispatch_receipt_sha256!==d.sha256||c.candidate_ref!==candidateRef||c.candidate_manifest_path!==manifestPath||c.candidate_manifest_sha256!==manifestSha||c.status!=='COMPLETED_NON_ERRORED'||c.lifecycle!=='FINISHED'||!timestamp(c.completed_at)||c.response_sha256!==sha(Buffer.from(c.response_text,'utf8'))||c.verdict!=='PASS')throw Error(`ROUND3_CONTEXT_${kind.toUpperCase()}_COMPLETION_BINDING`);
    const review=regular(repo,reviewPath,`ROUND3_CONTEXT_${kind.toUpperCase()}_REVIEW`),r=review.value;
    if(!exact(r,reviewKeys)||r.schema_version!=='gemini-context-v5-round-0003-context-input-review-v1'||r.review_id!==`V5-ROUND-0003-CONTEXT-INPUT-${e.receiptRole}-REVIEW-${d.cycle}`||r.round_id!=='ROUND-0003'||r.stage!=='CONTEXT_INPUT'||r.role!==e.role||r.agent_id!==d.value.agent_id||r.route!==e.route||r.status!=='PASS'||r.candidate_ref!==candidateRef||r.candidate_manifest_path!==manifestPath||r.candidate_manifest_sha256!==manifestSha||r.dispatch_id!==d.value.dispatch_id||r.dispatch_receipt_path!==d.path||r.dispatch_receipt_sha256!==d.sha256||r.completion_receipt_path!==completionPath||r.completion_receipt_sha256!==sha(completion.bytes)||r.completion_status!=='COMPLETED_NON_ERRORED'||r.response_sha256!==c.response_sha256||!Array.isArray(r.findings)||r.findings.length!==0||r.repository_modified_by_review!==false||!timestamp(r.recorded_at))throw Error(`ROUND3_CONTEXT_${kind.toUpperCase()}_REVIEW_BINDING`);
    refs[kind]={path:reviewPath,sha256:sha(review.bytes),agent_id:r.agent_id,role:r.role,route:r.route,status:r.status,completion_receipt_path:completionPath,completion_receipt_sha256:sha(completion.bytes),completion_status:c.status,completion_verdict:c.verdict,dispatch_receipt_path:d.path,dispatch_receipt_sha256:d.sha256,dispatch_id:d.value.dispatch_id,cycle:d.cycle,response_sha256:c.response_sha256};
  }
  const gate=regular(repo,lifecycle.gate,'ROUND3_CONTEXT_GATE'),g=gate.value;
  if(!exact(g,gateKeys)||g.schema_version!=='gemini-context-v5-round-0003-context-input-review-gate-v1'||g.gate_id!=='V5-ROUND-0003-CONTEXT-INPUT-DUAL-PASS-GATE-001'||g.round_id!=='ROUND-0003'||g.stage!=='CONTEXT_INPUT'||g.status!=='SATISFIED_EXACT_FINAL_DUAL_PASS'||g.candidate_ref!==candidateRef||g.candidate_manifest_path!==manifestPath||g.candidate_manifest_sha256!==manifestSha||JSON.stringify(g.normal_review)!==JSON.stringify(refs.normal)||JSON.stringify(g.senior_review)!==JSON.stringify(refs.senior)||JSON.stringify(g.authorized_input_boundary)!==JSON.stringify({payload_path:contextViewPath,payload_sha256:contextViewSha,item_count:2,exact_raw_view_bytes_only:true})||JSON.stringify(g.auditor_call_contract)!==JSON.stringify({call_count_allowance:1,calls_started:0,calls_remaining:1,context_audit_executed:false})||g.permitted_next_action!=='GO_ROUND_0003_CONTEXT_AUDITOR_CALL_ONLY'||!Array.isArray(g.forbidden_before_valid_auditor_output)||!timestamp(g.recorded_at)||!/^[0-9a-f-]{36}$/u.test(g.sole_writer_agent_id))throw Error('ROUND3_CONTEXT_GATE_BINDING');
  const view=regular(repo,contextViewPath,'ROUND3_CONTEXT_VIEW');if(sha(view.bytes)!==contextViewSha||view.value.items?.length!==2)throw Error('ROUND3_CONTEXT_AUTHORIZED_INPUT_BOUNDARY');
  for(const forbidden of ['AUDITOR-RESPONSE-ROUND-0003-CONTEXT-CALL-001.json','rounds/ROUND-0003/CONTEXT-RECORDS.json','rounds/ROUND-0003/CONTEXT-AGGREGATE.json','rounds/ROUND-0003/RELEASE.json','rounds/ROUND-0004'])if(fs.existsSync(path.join(repo,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5',forbidden)))throw Error(`ROUND3_CONTEXT_UNAUTHORIZED_LATER_ARTIFACT:${forbidden}`);
  return {status:'PASS',decision:g.permitted_next_action,candidate_ref:candidateRef,candidate_manifest_sha256:manifestSha,candidate_file_count:191,normal_review:refs.normal,senior_review:refs.senior,gate_path:lifecycle.gate,gate_sha256:sha(gate.bytes),context_auditor_call_count_allowance:1,context_auditor_calls_started:0,context_auditor_calls_remaining:1,context_auditor_call_authorized:true,context_results_created:false,round_0003_release_or_replacement_created:false,round_0004_created:false};
}
export function validateRound3ContextReviewLifecycle(repo=repoDefault){const dispatches=validateDispatches(repo),later=['normalCompletion','seniorCompletion','normalReview','seniorReview','gate'].map(k=>fs.existsSync(path.join(repo,lifecycle[k])));if(later.every(x=>!x))return {status:'PASS',decision:'NO_GO_ROUND_0003_CONTEXT_INPUT_REVIEW_REQUIRED',candidate_ref:candidateRef,candidate_manifest_sha256:manifestSha,candidate_file_count:191,completion_absent:true};if(!later.every(Boolean))throw Error('ROUND3_CONTEXT_PARTIAL_FINAL_LIFECYCLE');return validateFinal(repo,dispatches);}
export const validateRound3ContextDispatchReceipts=validateRound3ContextReviewLifecycle;
if(import.meta.url===`file://${process.argv[1]}`)console.log(JSON.stringify(validateRound3ContextReviewLifecycle(process.argv[2]?path.resolve(process.argv[2]):repoDefault),null,2));
