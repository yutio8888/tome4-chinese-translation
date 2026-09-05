#!/usr/bin/env node
// Reconstruct the run from the ledger alone, re-derive every RAW from the captured
// stdout bytes, score, and report. NO_RUN is returned only when execution/ is empty (C13).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readCanonical,shaFile,sha256,jsonBytes,writeExclusive} from './lib.mjs';
import {checkManifest} from './build-manifest.mjs';
import {validateGates} from './gates.mjs';
import {validateQualification} from './qualification.mjs';
import {deriveState,executionEmpty,isQualificationCell} from './ledger.mjs';
import {deriveRaw,capturePaths,rawPath,requestEntry} from './runner.mjs';
import {validateReference,scoreCell,scoresDocument} from './scorer.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),defaultRepo=path.resolve(here,'../../../..');
// C08: the runner view, rebuilt from ledger rows only. No STATE.json, no mtimes.
export function reconstruct(root=here,{repoRoot=defaultRepo}={}){
  const state=deriveState(root),cells=[],errors=[...state.errors];
  for(const [cell,c] of Object.entries(state.cells)){
    // The two qualification cells share this ledger (C15) but are not execution cells: they are
    // verified by validateQualification and are never scored or authorized as run cells.
    if(isQualificationCell(cell))continue;
    const view={cell,attempt_numbers:c.attempt_numbers,successful_attempt:c.successful_attempt,ambiguous:c.ambiguous,next_attempt:c.next_attempt,blocked_reason:c.blocked_reason,raw_path:null,raw_sha256:null,exit:null,success:false};
    const last=c.attempts[c.attempts.length-1];
    view.exit=last?.exit??null;
    for(const a of c.attempts){
      const cap=capturePaths(cell,a.attempt);
      if(a.state==='STARTED_NO_FINISH'){continue}
      for(const [k,p] of [['stdout',cap.stdout],['stderr',cap.stderr]]){
        const abs=path.join(root,p);
        if(!fs.existsSync(abs))errors.push(`CAPTURE_MISSING:${p}`);
        else if(shaFile(abs)!==a[`${k}_sha256`])errors.push(`CAPTURE_HASH:${p}`);
      }
      const rp=path.join(root,rawPath(cell,a.attempt));
      if(a.state!=='FINISHED_SUCCESS'&&fs.existsSync(rp))errors.push(`RAW_FOR_FAILED_ATTEMPT:${cell}:${a.attempt}`);
    }
    if(c.successful_attempt!==null){
      try{const d=deriveRaw(root,cell,c.successful_attempt,{repoRoot});view.raw_path=d.raw_path;view.raw_sha256=d.raw_sha256;view.success=true;if(!d.parsed.valid)errors.push(`RAW_PARSE:${cell}:${d.parsed.errors.join(',')}`)}
      catch(e){errors.push(`RAW_DERIVE:${cell}:${e.message}`)}
    }
    cells.push(view);
  }
  cells.sort((a,b)=>a.cell<b.cell?-1:a.cell>b.cell?1:0);
  return{no_run:state.no_run,started_rows:state.started_rows,finished_rows:state.finished_rows,agy_processes_spawned:state.agy_processes_spawned,inference_calls_made:state.inference_calls_made,cells,errors};
}
const report=(decision,x)=>({schema_version:'gemini-context-v5-execution-post-run-v1',decision,pilot_result_is_not_experimental_evidence:true,...x});
export function postRun(root=here,{repoRoot=defaultRepo,write=false}={}){
  const mErrors=checkManifest(root);
  if(executionEmpty(root))return report('NO_RUN',{execution_state:'NO_RUN',agy_processes_spawned:0,inference_calls_made:0,cells:[],errors:mErrors.map(x=>`manifest:${x}`)});
  const errors=[...mErrors.map(x=>`manifest:${x}`)],g=validateGates(root,{repoRoot});
  errors.push(...g.errors.map(x=>`gates:${x}`));
  const q=validateQualification(root,{repoRoot});
  if(!q.valid)errors.push(...q.errors.map(x=>`qualification:${x}`));
  const rec=reconstruct(root,{repoRoot});
  errors.push(...rec.errors);
  // C15: both counters come from the ledger's START rows (qualification rows included).
  const {agy_processes_spawned,inference_calls_made}=rec;
  const auth=g.gates?.EXECUTION_AUTHORIZATION;
  if(auth&&agy_processes_spawned>auth.agy_process_budget)errors.push(`STOP_BUDGET:${agy_processes_spawned}/${auth.agy_process_budget}`);
  for(const c of rec.cells)if(auth&&!auth.authorized_cells.includes(c.cell))errors.push(`UNAUTHORIZED_CELL:${c.cell}`);
  const base={execution_state:'PARTIAL_OR_COMPLETE',agy_processes_spawned,inference_calls_made,cells:rec.cells};
  if(errors.length)return report('INVALID_ARTIFACTS',{...base,errors});
  let scores;
  try{
    const samples=readCanonical(path.join(root,'frozen/SAMPLES.json')),ref=readCanonical(path.join(root,'sealed/REFERENCE.json')),m=readCanonical(path.join(root,'frozen/REQUEST-MANIFEST.json'));
    errors.push(...validateReference(ref,samples,m.reference_sha256).map(x=>`reference:${x}`));
    if(shaFile(path.join(root,'frozen/SAMPLES.json'))!==m.sample_sha256)errors.push('SAMPLE_BINDING');
    const byId=new Map(ref.items.map(x=>[x.item_id,x])),scored=[];
    for(const c of rec.cells){
      if(!c.success)continue;
      const entry=requestEntry(root,c.cell),raw=readCanonical(path.join(root,c.raw_path));
      scored.push({cell:c.cell,protocol:entry.protocol,raw_path:c.raw_path,raw_sha256:c.raw_sha256,score:scoreCell(raw.structured_output.items,entry.item_ids.map(id=>byId.get(id)))});
    }
    scores=scoresDocument({reference_sha256:m.reference_sha256,sample_sha256:m.sample_sha256,cells:scored});
  }catch(e){errors.push(`SCORING:${e.message}`)}
  if(errors.length)return report('INVALID_ARTIFACTS',{...base,errors});
  const complete=auth&&auth.authorized_cells.every(x=>rec.cells.find(c=>c.cell===x)?.success)&&agy_processes_spawned===auth.agy_process_budget&&inference_calls_made===auth.inference_call_budget;
  if(write){
    const b=jsonBytes(scores),p=path.join(root,'SCORES.json');
    if(fs.existsSync(p)){if(!fs.readFileSync(p).equals(b))return report('INVALID_ARTIFACTS',{...base,errors:['SCORES_DRIFT']})}else writeExclusive(p,b);
  }
  return report(complete?'PILOT_COMPLETE':'PILOT_INCOMPLETE',{...base,errors:[],scores_sha256:sha256(jsonBytes(scores)),scores});
}
if(import.meta.url===`file://${process.argv[1]}`){const r=postRun(here,{write:process.argv.includes('--write')});console.log(JSON.stringify(r,null,2));process.exitCode=['NO_RUN','PILOT_COMPLETE'].includes(r.decision)?0:3}
