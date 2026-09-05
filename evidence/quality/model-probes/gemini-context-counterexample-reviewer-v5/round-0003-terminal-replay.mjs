#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {ROUND3_CONTEXT_CALL,validateRound3ContextArtifacts} from './round-0003-context-results.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const repoDefault=path.resolve(here,'..','..','..','..');
const taskRoot='.ai/task/research-gemini-context-counterexample-reviewer-v5';
const terminalManifestPath=`${taskRoot}/ROUND-0003-TERMINALIZATION-IMPLEMENTATION-CANDIDATE-MANIFEST.json`;
export const ROUND3_TERMINAL_LIFECYCLE=Object.freeze({
  normalDispatch:`${taskRoot}/ROUND-0003-TERMINALIZATION-NORMAL-DISPATCH-RECEIPT-001.json`,
  seniorDispatch:`${taskRoot}/ROUND-0003-TERMINALIZATION-SENIOR-DISPATCH-RECEIPT-001.json`,
  normalCompletion:`${taskRoot}/ROUND-0003-TERMINALIZATION-NORMAL-COMPLETION-RECEIPT-001.json`,
  seniorCompletion:`${taskRoot}/ROUND-0003-TERMINALIZATION-SENIOR-COMPLETION-RECEIPT-001.json`,
  normalReview:`${taskRoot}/ROUND-0003-TERMINALIZATION-NORMAL-REVIEW-001.json`,
  seniorReview:`${taskRoot}/ROUND-0003-TERMINALIZATION-SENIOR-REVIEW-001.json`,
  gate:`${taskRoot}/ROUND-0003-TERMINALIZATION-REVIEW-GATE-001.json`
});
const sha256=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const jsonBytes=value=>Buffer.from(`${JSON.stringify(value,null,2)}\n`);
const exactKeys=(value,keys)=>value&&typeof value==='object'&&!Array.isArray(value)&&JSON.stringify(Object.keys(value).sort())===JSON.stringify([...keys].sort());
const timestamp=value=>typeof value==='string'&&!Number.isNaN(Date.parse(value))&&new Date(value).toISOString()===value;
function readRegular(file,label){const stat=fs.lstatSync(file);if(stat.isSymbolicLink()||!stat.isFile())throw Error(`${label}_FILE_TYPE`);return fs.readFileSync(file);}
function readCanonical(file,label){const bytes=readRegular(file,label);let value;try{value=JSON.parse(bytes);}catch{throw Error(`${label}_JSON`);}if(!bytes.equals(jsonBytes(value)))throw Error(`${label}_NONCANONICAL_BYTES`);return {bytes,value};}
function validateFrozenManifest(repo,{relative,expectedSha,expectedRef,expectedCount,label}){
  const manifest=readCanonical(path.join(repo,relative),label);
  if(sha256(manifest.bytes)!==expectedSha||manifest.value.candidate_ref!==expectedRef||!Array.isArray(manifest.value.files)||manifest.value.files.length!==expectedCount)throw Error(`${label}_BINDING`);
  const listed=manifest.value.files,sorted=[...listed].sort((a,b)=>Buffer.compare(Buffer.from(a.path),Buffer.from(b.path)));
  if(JSON.stringify(listed)!==JSON.stringify(sorted)||new Set(listed.map(item=>item.path)).size!==listed.length)throw Error(`${label}_ORDER_OR_DUPLICATE`);
  for(const item of listed){if(!exactKeys(item,['path','sha256'])||!item.path||item.path.startsWith('/')||item.path.includes('..')||!/^[0-9a-f]{64}$/u.test(item.sha256))throw Error(`${label}_ITEM`);const bytes=readRegular(path.join(repo,item.path),`${label}_LISTED_FILE`);if(sha256(bytes)!==item.sha256)throw Error(`${label}_FILE_HASH:${item.path}`);}
  const computed=sha256(Buffer.concat(listed.map(item=>Buffer.from(`${item.path}\0${item.sha256}\n`))));
  if(computed!==expectedRef)throw Error(`${label}_CANDIDATE_ROOT`);
  return {path:relative,sha256:expectedSha,candidate_ref:expectedRef,manifest_files:expectedCount,validated_files:listed.length};
}
function assertHash(root,relative,expected,label){const bytes=readRegular(path.join(root,relative),label);if(sha256(bytes)!==expected)throw Error(`${label}_HASH`);return expected;}
function recursiveRegularFiles(repo,relative){const out=[];const visit=current=>{const stat=fs.lstatSync(path.join(repo,current));if(stat.isSymbolicLink())throw Error(`ROUND3_UNAUTHORIZED_SYMLINK:${current}`);if(stat.isFile()){out.push(current);return;}if(!stat.isDirectory())throw Error(`ROUND3_UNAUTHORIZED_FILE_TYPE:${current}`);for(const name of fs.readdirSync(path.join(repo,current)))visit(path.posix.join(current,name));};visit(relative);return out;}
const terminalExclusions=[
  {path:`${taskRoot}/STATE.json`,reason:'mutable orchestration metadata'},
  {path:terminalManifestPath,reason:'self-reference'},
  {path:ROUND3_TERMINAL_LIFECYCLE.normalDispatch,reason:'future independent normal review dispatch lifecycle evidence'},
  {path:ROUND3_TERMINAL_LIFECYCLE.seniorDispatch,reason:'future independent senior review dispatch lifecycle evidence'},
  {path:ROUND3_TERMINAL_LIFECYCLE.normalCompletion,reason:'future independent normal review completion lifecycle evidence'},
  {path:ROUND3_TERMINAL_LIFECYCLE.seniorCompletion,reason:'future independent senior review completion lifecycle evidence'},
  {path:ROUND3_TERMINAL_LIFECYCLE.normalReview,reason:'future independent normal review record'},
  {path:ROUND3_TERMINAL_LIFECYCLE.seniorReview,reason:'future independent senior review record'},
  {path:ROUND3_TERMINAL_LIFECYCLE.gate,reason:'future combined terminalization review gate'}
];
function validateNoUnauthorizedArtifacts(repo){
  const context=readCanonical(path.join(repo,taskRoot,'ROUND-0003-CONTEXT-INPUT-IMPLEMENTATION-CANDIDATE-MANIFEST.json'),'ROUND3_CONTEXT_COVERAGE_MANIFEST').value;
  const terminal=readCanonical(path.join(repo,terminalManifestPath),'ROUND3_TERMINAL_COVERAGE_MANIFEST').value;
  const allowed=new Set([...context.files.map(item=>item.path),...context.exclusions.map(item=>item.path),...terminal.files.map(item=>item.path),...terminal.exclusions.map(item=>item.path)]);
  const optional=new Set(Object.values(ROUND3_TERMINAL_LIFECYCLE));
  const required=new Set([...context.files.map(item=>item.path),...context.exclusions.map(item=>item.path),...terminal.files.map(item=>item.path),`${taskRoot}/STATE.json`,terminalManifestPath]);
  const actual=[...recursiveRegularFiles(repo,taskRoot),...recursiveRegularFiles(repo,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5')];
  const unauthorized=actual.filter(item=>!allowed.has(item)),missing=[...required].filter(item=>!fs.existsSync(path.join(repo,item))),authorizedExistingInScannedRoots=[...allowed].filter(item=>(item.startsWith(`${taskRoot}/`)||item.startsWith('evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/'))&&fs.existsSync(path.join(repo,item))),optionalAbsent=[...optional].filter(item=>!fs.existsSync(path.join(repo,item)));
  if(unauthorized.length||missing.length)throw Error(`ROUND3_UNAUTHORIZED_ARTIFACT_SET:extra=${unauthorized.join(',')}:missing=${missing.join(',')}`);
  if(actual.length!==authorizedExistingInScannedRoots.length)throw Error('ROUND3_AUTHORIZED_ACTUAL_COUNT_UNIVERSE');
  return {actual_files_in_scanned_roots:actual.length,authorized_existing_files_in_scanned_roots:authorizedExistingInScannedRoots.length,authorized_path_universe:allowed.size,optional_lifecycle_absent:optionalAbsent.length,extra_files:0,missing_required_files:0};
}
function validateTerminalManifest(repo){
  const record=readCanonical(path.join(repo,terminalManifestPath),'ROUND3_TERMINAL_MANIFEST'),m=record.value;
  const keys=['schema_version','status','candidate_ref','author_paseo_agent_id','round_id','stage','review_requirement','frozen_manifest_bindings','coverage_policy','exclusions','files'];
  if(!exactKeys(m,keys)||m.schema_version!=='gemini-context-v5-round-0003-terminalization-implementation-candidate-v1'||m.status!=='PENDING_INDEPENDENT_NORMAL_AND_SENIOR_REVIEW'||m.author_paseo_agent_id!=='4ceb481a-7870-4b7e-8c6d-8279dfdb4026'||m.round_id!=='ROUND-0003'||m.stage!=='TERMINALIZATION'||m.review_requirement?.normal_review_required!==true||m.review_requirement?.senior_review_required!==true||m.review_requirement?.combined_gate_created!==false||!Array.isArray(m.files)||m.files.length!==12)throw Error('ROUND3_TERMINAL_MANIFEST_SCHEMA');
  if(JSON.stringify(m.exclusions)!==JSON.stringify(terminalExclusions))throw Error('ROUND3_TERMINAL_MANIFEST_EXCLUSIONS');
  const sorted=[...m.files].sort((a,b)=>Buffer.compare(Buffer.from(a.path),Buffer.from(b.path)));
  if(JSON.stringify(m.files)!==JSON.stringify(sorted)||new Set(m.files.map(item=>item.path)).size!==m.files.length)throw Error('ROUND3_TERMINAL_MANIFEST_ORDER_OR_DUPLICATE');
  for(const item of m.files){if(!exactKeys(item,['path','sha256'])||!item.path||item.path.startsWith('/')||item.path.includes('..')||!/^[0-9a-f]{64}$/u.test(item.sha256))throw Error('ROUND3_TERMINAL_MANIFEST_ITEM');if(sha256(readRegular(path.join(repo,item.path),'ROUND3_TERMINAL_CANDIDATE_FILE'))!==item.sha256)throw Error(`ROUND3_TERMINAL_CANDIDATE_FILE_HASH:${item.path}`);}
  const candidateRef=sha256(Buffer.concat(m.files.map(item=>Buffer.from(`${item.path}\0${item.sha256}\n`))));if(candidateRef!==m.candidate_ref)throw Error('ROUND3_TERMINAL_MANIFEST_ROOT');
  return {path:terminalManifestPath,sha256:sha256(record.bytes),candidate_ref:candidateRef,file_count:m.files.length,status:m.status};
}
const dispatchKeys=['schema_version','round_id','stage','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','candidate_file_count','agent_created_at','dispatched_at','orchestrator_authorization_scope','expected_permitted_read_only_task','completion_absent','receipt_id','role','agent_id','route','dispatch_id','cycle','opus_quota_override'];
const completionKeys=['schema_version','receipt_id','round_id','stage','role','agent_id','route','dispatch_id','dispatch_receipt_path','dispatch_receipt_sha256','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','status','lifecycle','completed_at','response_sha256','verdict','response_text'];
const reviewKeys=['schema_version','review_id','round_id','stage','role','agent_id','route','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','dispatch_id','dispatch_receipt_path','dispatch_receipt_sha256','completion_receipt_path','completion_receipt_sha256','completion_status','response_sha256','findings','repository_modified_by_review','recorded_at'];
const gateKeys=['schema_version','gate_id','round_id','stage','status','candidate_ref','candidate_manifest_path','candidate_manifest_sha256','normal_review','senior_review','terminal_decision','permitted_next_action','forbidden_actions','recorded_at','sole_writer_paseo_agent_id'];
const dispatchScope={candidate_read_only:true,exact_manifest_file_scope:true,candidate_file_mutation:false,context_input_file_mutation:false,surface_input_file_mutation:false,production_materialization:false,derived_state_mutation:false,completion_receipt:false,review_record:false,combined_gate:false,round_0003_release:false,round_0003_replacement:false,round_0004:false};
const reviewers={normal:{role:'REVIEWER',receiptRole:'NORMAL',route:'Codex gpt-5.6-sol xhigh',dispatchRoute:'CODEX',override:false},senior:{role:'SENIOR_REVIEWER',receiptRole:'SENIOR',route:'Gemini 3.7 Flash high',dispatchRoute:'GEMINI',override:true}};
function validateTerminalLifecycle(repo,manifest,terminalDecisionSha){
  const present=Object.fromEntries(Object.entries(ROUND3_TERMINAL_LIFECYCLE).map(([key,relative])=>[key,fs.existsSync(path.join(repo,relative))]));
  const dispatchPresent=[present.normalDispatch,present.seniorDispatch],finalPresent=[present.normalCompletion,present.seniorCompletion,present.normalReview,present.seniorReview,present.gate];
  if([...dispatchPresent,...finalPresent].every(value=>!value))return {phase:'ABSENT',status:'PENDING_INDEPENDENT_NORMAL_AND_SENIOR_REVIEW',decision:'NO_GO_ROUND_0003_TERMINALIZATION_REVIEW_REQUIRED'};
  if(!dispatchPresent.every(Boolean))throw Error('ROUND3_TERMINAL_PARTIAL_DISPATCH_LIFECYCLE');
  const dispatches={};
  for(const [kind,e] of Object.entries(reviewers)){
    const relative=ROUND3_TERMINAL_LIFECYCLE[`${kind}Dispatch`],record=readCanonical(path.join(repo,relative),`ROUND3_TERMINAL_${kind.toUpperCase()}_DISPATCH`),v=record.value;
    const receipt=typeof v.receipt_id==='string'&&v.receipt_id.match(new RegExp(`^V5-ROUND-0003-TERMINALIZATION-${e.receiptRole}-DISPATCH-RECEIPT-(\\d{3})$`,'u'));
    const dispatch=typeof v.dispatch_id==='string'&&v.dispatch_id.match(new RegExp(`^V5-R3-TERMINALIZATION-DISPATCH-${e.dispatchRoute}-([0-9A-F]{8})-CYCLE(\\d{3})$`,'u'));
    if(!exactKeys(v,dispatchKeys)||v.schema_version!=='gemini-context-v5-round-0003-terminalization-review-dispatch-receipt-v1'||v.round_id!=='ROUND-0003'||v.stage!=='TERMINALIZATION'||v.status!=='DISPATCHED'||v.candidate_ref!==manifest.candidate_ref||v.candidate_manifest_path!==terminalManifestPath||v.candidate_manifest_sha256!==manifest.sha256||v.candidate_file_count!==manifest.file_count||!timestamp(v.agent_created_at)||!timestamp(v.dispatched_at)||Date.parse(v.agent_created_at)>Date.parse(v.dispatched_at)||JSON.stringify(v.orchestrator_authorization_scope)!==JSON.stringify(dispatchScope)||v.expected_permitted_read_only_task!==`READ_ONLY_REVIEW_OF_EXACT_ROUND_0003_TERMINALIZATION_IMPLEMENTATION_CANDIDATE_${manifest.file_count}_FILES`||v.completion_absent!==true||v.role!==e.role||!/^[0-9a-f]{8}-[0-9a-f-]{27}$/u.test(v.agent_id)||v.route!==e.route||v.opus_quota_override!==e.override||!receipt||!dispatch||v.cycle!==Number(receipt[1])||receipt[1]!==dispatch[2]||dispatch[1]!==v.agent_id.slice(0,8).toUpperCase())throw Error(`ROUND3_TERMINAL_${kind.toUpperCase()}_DISPATCH_BINDING`);
    dispatches[kind]={path:relative,sha256:sha256(record.bytes),value:v,cycle:receipt[1]};
  }
  if(dispatches.normal.value.agent_id===dispatches.senior.value.agent_id||dispatches.normal.value.dispatch_id===dispatches.senior.value.dispatch_id)throw Error('ROUND3_TERMINAL_DISPATCH_INDEPENDENCE');
  if(finalPresent.every(value=>!value))return {phase:'DISPATCH_ONLY',status:'PENDING_REVIEW_COMPLETION',decision:'NO_GO_ROUND_0003_TERMINALIZATION_REVIEW_COMPLETION_REQUIRED',normal_dispatch_sha256:dispatches.normal.sha256,senior_dispatch_sha256:dispatches.senior.sha256};
  if(!finalPresent.every(Boolean))throw Error('ROUND3_TERMINAL_PARTIAL_FINAL_LIFECYCLE');
  const refs={};
  for(const [kind,e] of Object.entries(reviewers)){
    const completionPath=ROUND3_TERMINAL_LIFECYCLE[`${kind}Completion`],reviewPath=ROUND3_TERMINAL_LIFECYCLE[`${kind}Review`],d=dispatches[kind];
    const completion=readCanonical(path.join(repo,completionPath),`ROUND3_TERMINAL_${kind.toUpperCase()}_COMPLETION`),c=completion.value;
    if(!exactKeys(c,completionKeys)||c.schema_version!=='gemini-context-v5-round-0003-terminalization-review-completion-receipt-v1'||c.receipt_id!==`V5-ROUND-0003-TERMINALIZATION-${e.receiptRole}-COMPLETION-RECEIPT-${d.cycle}`||c.round_id!=='ROUND-0003'||c.stage!=='TERMINALIZATION'||c.role!==e.role||c.agent_id!==d.value.agent_id||c.route!==e.route||c.dispatch_id!==d.value.dispatch_id||c.dispatch_receipt_path!==d.path||c.dispatch_receipt_sha256!==d.sha256||c.candidate_ref!==manifest.candidate_ref||c.candidate_manifest_path!==terminalManifestPath||c.candidate_manifest_sha256!==manifest.sha256||c.status!=='COMPLETED_NON_ERRORED'||c.lifecycle!=='FINISHED'||!timestamp(c.completed_at)||c.response_sha256!==sha256(Buffer.from(c.response_text,'utf8'))||c.verdict!=='PASS')throw Error(`ROUND3_TERMINAL_${kind.toUpperCase()}_COMPLETION_BINDING`);
    const review=readCanonical(path.join(repo,reviewPath),`ROUND3_TERMINAL_${kind.toUpperCase()}_REVIEW`),r=review.value;
    if(!exactKeys(r,reviewKeys)||r.schema_version!=='gemini-context-v5-round-0003-terminalization-review-v1'||r.review_id!==`V5-ROUND-0003-TERMINALIZATION-${e.receiptRole}-REVIEW-${d.cycle}`||r.round_id!=='ROUND-0003'||r.stage!=='TERMINALIZATION'||r.role!==e.role||r.agent_id!==d.value.agent_id||r.route!==e.route||r.status!=='PASS'||r.candidate_ref!==manifest.candidate_ref||r.candidate_manifest_path!==terminalManifestPath||r.candidate_manifest_sha256!==manifest.sha256||r.dispatch_id!==d.value.dispatch_id||r.dispatch_receipt_path!==d.path||r.dispatch_receipt_sha256!==d.sha256||r.completion_receipt_path!==completionPath||r.completion_receipt_sha256!==sha256(completion.bytes)||r.completion_status!==c.status||r.response_sha256!==c.response_sha256||!Array.isArray(r.findings)||r.findings.length!==0||r.repository_modified_by_review!==false||!timestamp(r.recorded_at))throw Error(`ROUND3_TERMINAL_${kind.toUpperCase()}_REVIEW_BINDING`);
    refs[kind]={path:reviewPath,sha256:sha256(review.bytes),agent_id:r.agent_id,role:r.role,route:r.route,status:r.status,completion_receipt_path:completionPath,completion_receipt_sha256:sha256(completion.bytes),dispatch_receipt_path:d.path,dispatch_receipt_sha256:d.sha256,response_sha256:c.response_sha256};
  }
  const gate=readCanonical(path.join(repo,ROUND3_TERMINAL_LIFECYCLE.gate),'ROUND3_TERMINAL_REVIEW_GATE'),g=gate.value;
  if(!exactKeys(g,gateKeys)||g.schema_version!=='gemini-context-v5-round-0003-terminalization-review-gate-v1'||g.gate_id!=='V5-ROUND-0003-TERMINALIZATION-DUAL-PASS-GATE-001'||g.round_id!=='ROUND-0003'||g.stage!=='TERMINALIZATION'||g.status!=='SATISFIED_EXACT_FINAL_DUAL_PASS'||g.candidate_ref!==manifest.candidate_ref||g.candidate_manifest_path!==terminalManifestPath||g.candidate_manifest_sha256!==manifest.sha256||JSON.stringify(g.normal_review)!==JSON.stringify(refs.normal)||JSON.stringify(g.senior_review)!==JSON.stringify(refs.senior)||JSON.stringify(g.terminal_decision)!==JSON.stringify({path:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0003/TERMINAL-DECISION.json',sha256:terminalDecisionSha,decision:'NO_ROUND_0004_NEEDED_OR_AUTHORIZED'})||g.permitted_next_action!=='TERMINALIZATION_COMPLETE_NO_RELEASE_OR_ROUND_0004'||JSON.stringify(g.forbidden_actions)!==JSON.stringify(['ROUND_0003_RELEASE','ROUND_0003_REPLACEMENT','ROUND_0004','FORMAL_EXPERIMENT_INFERENCE','GIT_STAGE','GIT_HISTORY'])||!timestamp(g.recorded_at)||!/^[0-9a-f]{8}-[0-9a-f-]{27}$/u.test(g.sole_writer_paseo_agent_id))throw Error('ROUND3_TERMINAL_REVIEW_GATE_BINDING');
  return {phase:'FINAL_DUAL_PASS',status:g.status,decision:g.permitted_next_action,normal_review:refs.normal,senior_review:refs.senior,gate_path:ROUND3_TERMINAL_LIFECYCLE.gate,gate_sha256:sha256(gate.bytes)};
}
export function replayRound3Terminal(root=here,repo=repoDefault){
  const round=path.join(root,'rounds/ROUND-0003'),roundStat=fs.lstatSync(round);if(roundStat.isSymbolicLink()||!roundStat.isDirectory())throw Error('ROUND3_TERMINAL_DIRECTORY_FILE_TYPE');
  const expectedRoundFiles=['CONTEXT-AGGREGATE.json','CONTEXT-QUEUE-VIEW.json','CONTEXT-QUEUE.json','CONTEXT-RECORDS.json','CONTEXT-SOURCE-ANCHORS.json','RESULT.json','SURFACE-AGGREGATE.json','SURFACE-QUEUE-VIEW.json','SURFACE-QUEUE.json','SURFACE-RECORDS.json','TERMINAL-DECISION.json'];
  if(JSON.stringify(fs.readdirSync(round).sort())!==JSON.stringify(expectedRoundFiles))throw Error('ROUND3_TERMINAL_ARTIFACT_SET');
  for(const forbidden of ['rounds/ROUND-0004','rounds/ROUND-0003/RELEASE.json','AUDITOR-RESPONSE-ROUND-0003-CONTEXT-CALL-002.json'])if(fs.existsSync(path.join(root,forbidden)))throw Error(`ROUND3_UNAUTHORIZED_ARTIFACT:${forbidden}`);
  for(const forbidden of ['ROUND-0003-REPLACEMENT-RELEASE-AUTHORIZATION-001.json'])if(fs.existsSync(path.join(repo,taskRoot,forbidden)))throw Error(`ROUND3_UNAUTHORIZED_TASK_ARTIFACT:${forbidden}`);
  const contextManifest=validateFrozenManifest(repo,{relative:`${taskRoot}/ROUND-0003-CONTEXT-INPUT-IMPLEMENTATION-CANDIDATE-MANIFEST.json`,expectedSha:'a879250e76b38d784e552cc357cedc86a41c0d72eb9d109cea113ac8f4665e81',expectedRef:'eee2e29687da787564f4d0f0a58c5da9c5cb89fcf938af509dd7bb39dd2b8db5',expectedCount:191,label:'ROUND3_CONTEXT_FROZEN_MANIFEST'});
  const surfaceManifest=validateFrozenManifest(repo,{relative:`${taskRoot}/ROUND-0003-SURFACE-INPUT-IMPLEMENTATION-CANDIDATE-MANIFEST.json`,expectedSha:'bd1ebf4c514b8de537c0c499af7c8d889a4ec7bfc41194b9b9be2cf892a3061b',expectedRef:'876645ea61876b36a9f8b68e301e7397b86c75da7b79bb80d23f07274704ba2b',expectedCount:169,label:'ROUND3_SURFACE_FROZEN_MANIFEST'});
  const gate=readCanonical(path.join(repo,taskRoot,'ROUND-0003-CONTEXT-INPUT-REVIEW-GATE-001.json'),'ROUND3_CONTEXT_INPUT_GATE');
  if(sha256(gate.bytes)!=='8069c5b563a8a62eb29c45733e4eae1bc00844258b6da20a0827300d336e55f8')throw Error('ROUND3_CONTEXT_INPUT_GATE_HASH');
  if(gate.value.status!=='SATISFIED_EXACT_FINAL_DUAL_PASS'||gate.value.authorized_input_boundary?.payload_sha256!==ROUND3_CONTEXT_CALL.context_queue_view_sha256||JSON.stringify(gate.value.auditor_call_contract)!==JSON.stringify({call_count_allowance:1,calls_started:0,calls_remaining:1,context_audit_executed:false})||gate.value.permitted_next_action!=='GO_ROUND_0003_CONTEXT_AUDITOR_CALL_ONLY')throw Error('ROUND3_CONTEXT_INPUT_GATE_BINDING');
  const context=validateRound3ContextArtifacts({root});
  assertHash(root,'ACTIVE-FRAME.json','e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3','ROUND3_ACTIVE_FRAME');
  assertHash(root,'LINEAGE.json','03d2c842fba9ddf95905c16c5170e2c23aa182680d520a3c3a16848f37cbb3d6','ROUND3_LINEAGE');
  assertHash(root,'RESERVE-STATE.json','4fab5ea380b0e20b8e6dc2ba0ffc98125e126791fd7c283e0e5608119c0725e0','ROUND3_RESERVE_STATE');
  assertHash(root,'ROUND-INDEX.json','089a8b17dc7a21ba4f6178b77e1247bf89d420c3801ed2d9a8ee9042d6f8a375','ROUND3_ROUND_INDEX');
  assertHash(root,'RELEASE-STATE.json','30ad2ecb49626a23bed45d8a96a79664d5569ca1d1f85f6df77d23c7c3b9c334','ROUND3_RELEASE_STATE');
  assertHash(root,'rounds/ROUND-0003/SURFACE-RECORDS.json','157af1f76c6dfd055db28080e043d066b93ec5fd38afaa5aa083dd79b5eb841d','ROUND3_SURFACE_RECORDS');
  assertHash(root,'rounds/ROUND-0003/SURFACE-AGGREGATE.json','de5db2dfd18898c4f65c9b8ad2ef90821f2ba331a15ef2ac73dcccb5f9f6dc33','ROUND3_SURFACE_AGGREGATE');
  const decision=readCanonical(path.join(round,'TERMINAL-DECISION.json'),'ROUND3_TERMINAL_DECISION'),result=readCanonical(path.join(round,'RESULT.json'),'ROUND3_TERMINAL_RESULT');
  if(sha256(decision.bytes)!=='30fb37c2b4e2a748a7f199345aa7e90ea4fa595080f9f37e0fb9b1def7f9db45'||decision.value.decision!=='NO_ROUND_0004_NEEDED_OR_AUTHORIZED'||decision.value.implementation_review?.status!=='PENDING_INDEPENDENT_NORMAL_AND_SENIOR_REVIEW'||decision.value.sole_writer_paseo_agent_id!=='4ceb481a-7870-4b7e-8c6d-8279dfdb4026')throw Error('ROUND3_TERMINAL_DECISION_BINDING');
  if(sha256(result.bytes)!=='44726a9f538cb5ec3e63c64be64437fb2f0014f496b80d312647e240b8b550bd'||result.value.outcome?.current_active_replacement_heads_clean!==true||result.value.outcome?.rejections_created!==0||result.value.outcome?.replacements_created!==0||result.value.outcome?.releases_created!==0||result.value.call_accounting?.context_calls_started!==1||result.value.call_accounting?.context_calls_remaining!==0||result.value.call_accounting?.formal_gemini_experiment_inference_calls_made!==0||result.value.implementation_review?.status!=='PENDING_INDEPENDENT_NORMAL_AND_SENIOR_REVIEW')throw Error('ROUND3_TERMINAL_RESULT_BINDING');
  const terminalManifest=validateTerminalManifest(repo),reviewLifecycle=validateTerminalLifecycle(repo,terminalManifest,sha256(decision.bytes)),artifactCoverage=validateNoUnauthorizedArtifacts(repo);
  return {status:'PASS',decision:reviewLifecycle.decision,terminal_status:'TERMINAL_NO_ROUND_0004_NEEDED_OR_AUTHORIZED',released_rounds:2,last_release_sha256:'a42e2b8b4e497a26a4936558ffdf5816b45dd49b3b0e31d3eb42f969ddd0fd70',context_call_accounting:{allowance:1,started:1,remaining:0},context_counts:context.counts,raw_context_response_sha256:context.raw_response_sha256,context_records_sha256:context.context_records_sha256,context_aggregate_sha256:context.context_aggregate_sha256,terminal_decision_sha256:sha256(decision.bytes),terminal_result_sha256:sha256(result.bytes),context_manifest:contextManifest,surface_manifest:surfaceManifest,terminal_candidate_manifest:terminalManifest,no_unauthorized_artifacts:artifactCoverage,active_frame_mutated:false,lineage_mutated:false,reserve_mutated:false,round_index_mutated:false,rejection_created:false,replacement_created:false,release_created:false,round_0004_created:false,formal_experiment_inference_calls_made:0,implementation_review_status:reviewLifecycle.status,review_lifecycle:reviewLifecycle,sole_writer_paseo_agent_id:'4ceb481a-7870-4b7e-8c6d-8279dfdb4026'};
}
if(import.meta.url===`file://${process.argv[1]}`)console.log(JSON.stringify(replayRound3Terminal(),null,2));
