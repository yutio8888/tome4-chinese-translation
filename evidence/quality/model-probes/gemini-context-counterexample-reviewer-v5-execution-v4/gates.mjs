// Exactly three blocking gates, in order. Each is a task-owned file under .ai/task/<task>/.
// Package code NEVER writes any of them (C11/C12); it only reads and verifies them.
//
//   1 PACKAGE_REVIEW          - the frozen checklist C01..C14 passed on this manifest
//   2 QUALIFICATION           - the archived route qualification evidence for this manifest
//   3 EXECUTION_AUTHORIZATION - the exact cells, route and process budget authorized to run
//
// Every gate binds manifest_sha256; gates 2 and 3 additionally bind the byte hash of their
// direct predecessor gate, so the order cannot be skipped or re-ordered.
import fs from 'node:fs';
import path from 'node:path';
import {readCanonical,shaFile,hex64,exactKeys} from './lib.mjs';
import {TASK_ID,manifestSha256} from './build-manifest.mjs';
import {PILOT_AGY_PROCESS_CEILING} from './ledger.mjs';
export const TASK_DIR=`.ai/task/${TASK_ID}`;
export const GATE_ORDER=['PACKAGE_REVIEW','QUALIFICATION','EXECUTION_AUTHORIZATION'];
export const gatePaths={
  PACKAGE_REVIEW:`${TASK_DIR}/PACKAGE-REVIEW-GATE.json`,
  QUALIFICATION:`${TASK_DIR}/QUALIFICATION-GATE.json`,
  EXECUTION_AUTHORIZATION:`${TASK_DIR}/EXECUTION-AUTHORIZATION.json`
};
export const gateStatus={
  PACKAGE_REVIEW:'SATISFIED_CHECKLIST_C01_C14_PASS',
  QUALIFICATION:'SATISFIED_NON_SCORED_ROUTE_QUALIFICATION',
  EXECUTION_AUTHORIZATION:'AUTHORIZED_EXACT_CELLS_AND_ROUTE'
};
const common=['gate','manifest_sha256','schema_version','status','task_id'];
export const gateKeys={
  PACKAGE_REVIEW:[...common,'checklist_items_passed'],
  QUALIFICATION:[...common,'predecessor_gate','qualification_evidence','reported_model'],
  EXECUTION_AUTHORIZATION:[...common,'predecessor_gate','authorized_cells','agy_process_budget','inference_call_budget','request_manifest_sha256','route_contract_sha256']
};
const schemaOf=g=>`gemini-context-v5-execution-gate-${g.toLowerCase()}-v1`;
const binding=(repoRoot,b,wantPath,label,errors)=>{
  if(!exactKeys(b,['path','sha256'])||b.path!==wantPath||!hex64(b.sha256)){errors.push(`${label}:BINDING_SHAPE`);return false}
  const p=path.join(repoRoot,wantPath);
  if(!fs.existsSync(p)||shaFile(p)!==b.sha256){errors.push(`${label}:BINDING_HASH`);return false}
  return true;
};
// through: the last gate that must be present and satisfied.
export function validateGates(root,{repoRoot,through='EXECUTION_AUTHORIZATION'}={}){
  const errors=[],present={},gates={};
  let manifest_sha256=null;
  try{manifest_sha256=manifestSha256(root)}catch{errors.push('MANIFEST_ABSENT')}
  const last=GATE_ORDER.indexOf(through);
  for(const [i,gate] of GATE_ORDER.entries()){
    const p=path.join(repoRoot,gatePaths[gate]);
    if(!fs.existsSync(p)){present[gate]=false;if(i<=last)errors.push(`${gate}:ABSENT`);continue}
    let g;try{g=readCanonical(p)}catch(e){present[gate]=false;errors.push(`${gate}:${e.message}`);continue}
    const before=errors.length;
    if(!exactKeys(g,gateKeys[gate])||g.schema_version!==schemaOf(gate)||g.task_id!==TASK_ID||g.gate!==gate||g.status!==gateStatus[gate])errors.push(`${gate}:SCHEMA_FIELDS`);
    if(g.manifest_sha256!==manifest_sha256)errors.push(`${gate}:MANIFEST_BINDING`);
    if(i>0)binding(repoRoot,g.predecessor_gate,gatePaths[GATE_ORDER[i-1]],`${gate}:PREDECESSOR`,errors);
    if(gate==='PACKAGE_REVIEW'&&!(Array.isArray(g.checklist_items_passed)&&g.checklist_items_passed.length>=14&&['C01','C07','C11','C12','C13','C14'].every(x=>g.checklist_items_passed.includes(x))))errors.push('PACKAGE_REVIEW:CHECKLIST');
    if(gate==='QUALIFICATION'){
      binding(repoRoot,g.qualification_evidence,`${path.relative(repoRoot,root).replaceAll(path.sep,'/')}/qualification/EVIDENCE.json`,'QUALIFICATION:EVIDENCE',errors);
      // C12: `reported_model` is the OPTIONAL runtime self-report copied out of the envelope.
      // Real captures do not carry one, so null is accepted; only a present, different value is
      // STOP_ROUTE. Route identity is the model listing plus the argv --model binding, checked
      // in validateQualification, not this field.
      if(g.reported_model!==null&&g.reported_model!=='gemini-3.7-flash-high')errors.push('QUALIFICATION:STOP_ROUTE');
    }
    if(gate==='EXECUTION_AUTHORIZATION'){
      if(!Array.isArray(g.authorized_cells)||!g.authorized_cells.length||new Set(g.authorized_cells).size!==g.authorized_cells.length)errors.push('EXECUTION_AUTHORIZATION:CELLS');
      // The authorized budget can never exceed SPEC 6's 4 processes, the same ceiling the ledger
      // enforces on qualification, so the two budget checks cannot disagree (C15).
      if(!Number.isInteger(g.agy_process_budget)||g.agy_process_budget<1||g.agy_process_budget>PILOT_AGY_PROCESS_CEILING||!Number.isInteger(g.inference_call_budget)||g.inference_call_budget<1||g.inference_call_budget>g.agy_process_budget)errors.push('EXECUTION_AUTHORIZATION:BUDGET');
      const rc=path.join(root,'ROUTE-CONTRACT.json'),rm=path.join(root,'frozen/REQUEST-MANIFEST.json');
      if(!fs.existsSync(rc)||g.route_contract_sha256!==shaFile(rc))errors.push('EXECUTION_AUTHORIZATION:ROUTE_CONTRACT');
      if(!fs.existsSync(rm)||g.request_manifest_sha256!==shaFile(rm))errors.push('EXECUTION_AUTHORIZATION:REQUEST_MANIFEST');
    }
    present[gate]=errors.length===before;
    gates[gate]=g;
  }
  return{valid:errors.length===0,errors,present,gates,manifest_sha256};
}
