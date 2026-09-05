#!/usr/bin/env node
import fs from'node:fs';import path from'node:path';import{fileURLToPath}from'node:url';import{derive,capturePaths}from'./ledger.mjs';import{CELL_ORDER,splitRequest}from'./freezer.mjs';import{readCanonical,jsonBytes,writeExclusive}from'./lib.mjs';import{metrics}from'./metrics.mjs';import{checkManifest}from'./build-manifest.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
export const INTERPRETATION_CAVEAT='All supporting cells are single unreplicated samples under unpinned decoding; rates are descriptive and do not establish causality or effectiveness.';
export function interpret(cells){
  const metric=(id,name='evidence_membership_rate')=>cells.find(x=>x.cell===id)?.metrics?.[name];
  const count=id=>cells.find(x=>x.cell===id)?.metrics?.candidate_count;
  const p=id=>metric(id)===1,f=id=>metric(id)!=null&&metric(id)<1,support=ids=>Object.fromEntries(ids.map(id=>[id,{candidate_count:count(id)??null,evidence_membership_rate:metric(id)??null,source_target_only_evidence_membership_rate:metric(id,'source_target_only_evidence_membership_rate')??null}])),out=[];
  const add=(text,ids)=>out.push({interpretation:text,supporting_cells:support(ids),caveat:INTERPRETATION_CAVEAT});
  if(p('baseline-p0-s0-a'))add('baseline passes: original behavior may be stochastic; no prompt change justified without a separately frozen replication',['baseline-p0-s0-a']);
  else if(f('baseline-p0-s0-a')){
    if(p('schema-p0-s2-a')&&p('prompt-p1-s0-a'))add('baseline fails while schema and prompt cells pass: unstated constraint/affordance dominates',['baseline-p0-s0-a','schema-p0-s2-a','prompt-p1-s0-a']);
    else if(p('schema-p0-s2-a')&&f('prompt-p1-s0-a'))add('only schema passes: schema naming/description dominates',['baseline-p0-s0-a','schema-p0-s2-a','prompt-p1-s0-a']);
    else if(p('prompt-p1-s0-a')&&f('schema-p0-s2-a'))add('only prompt passes: prose instruction dominates',['baseline-p0-s0-a','schema-p0-s2-a','prompt-p1-s0-a']);
  }
  if(p('combined-p1-s2-a')&&(f('schema-p0-s2-a')||f('prompt-p1-s0-a')))add('combined passes while one or both single-factor cells fail: prompt/schema interaction matters',['schema-p0-s2-a','prompt-p1-s0-a','combined-p1-s2-a']);
  if(f('combined-p1-s2-a'))add('combined fails: the recommended joint configuration is not yet conformant and must not be promoted',['combined-p1-s2-a']);
  const br=metric('baseline-p0-s0-a','source_target_only_evidence_membership_rate'),cr=metric('context-p0-s0-c','source_target_only_evidence_membership_rate');
  if(br!=null&&cr!=null&&br-cr>=0.10)add('context materially worse than baseline on source/target-only evidence membership: context complexity is a separate contributor',['baseline-p0-s0-a','context-p0-s0-c']);
  if(!out.length)add('otherwise: inconclusive',CELL_ORDER);
  return out;
}
export function postRun(root=here,{write=false}={}){const state=derive(root),errors=[...checkManifest(root),...state.errors];if(state.no_run)return{schema_version:'evidence-contract-result-v1',decision:'NO_RUN',effectiveness_evidence:false,agy_processes_spawned:0,inference_calls_made:0,cells:[],errors};const rm=readCanonical(path.join(root,'frozen/REQUEST-MANIFEST.json')),cells=[];for(const id of CELL_ORDER){const c=state.cells[id];if(!c)continue;const row={cell:id,process_success:c.finish?.process_success??false,envelope_schema_valid:c.finish?.envelope_schema_valid??false,metrics:null};if(row.process_success&&row.envelope_schema_valid){const raw=readCanonical(path.join(root,capturePaths(id).raw)),entry=rm.requests.find(x=>x.cell===id),input=splitRequest(fs.readFileSync(path.join(root,entry.path))).input;row.metrics=metrics(raw.normalized_output,input)}cells.push(row)}const complete=CELL_ORDER.every(id=>state.cells[id]?.finish?.process_success&&state.cells[id]?.finish?.envelope_schema_valid)&&state.agy_processes_spawned===5;const out={schema_version:'evidence-contract-result-v1',decision:errors.length?'INVALID_ARTIFACTS':complete?'DESCRIPTIVE_PILOT_COMPLETE':'PILOT_STOPPED_OR_INCOMPLETE',effectiveness_evidence:false,single_call_cells:true,universal_caveat:INTERPRETATION_CAVEAT,agy_processes_spawned:state.agy_processes_spawned,inference_calls_made:state.inference_calls_made,cells,descriptive_interpretations:complete?interpret(cells):[],errors};if(write){const p=path.join(root,'RESULT.json'),b=jsonBytes(out);if(fs.existsSync(p)){if(!fs.readFileSync(p).equals(b))throw Error('RESULT_DRIFT')}else writeExclusive(p,b)}return out}
if(import.meta.url===`file://${process.argv[1]}`){const x=postRun(here,{write:process.argv.includes('--write')});console.log(JSON.stringify(x,null,2));process.exitCode=['NO_RUN','DESCRIPTIVE_PILOT_COMPLETE'].includes(x.decision)?0:3}
