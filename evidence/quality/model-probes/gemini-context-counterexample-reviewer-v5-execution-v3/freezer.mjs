#!/usr/bin/env node
// Deterministic renderer/freezer: 64 frozen bases -> 64 samples, 1 sealed reference,
// 32 request byte streams, 1 REQUEST-MANIFEST.json. No mutation authoring exists in v3,
// so every reference row is a clean control with zero atoms.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readCanonical,jsonBytes,sha256,shaFile,writeExclusive,byteCompare} from './lib.mjs';
import {buildRequest,renderRuntimeContext,CONTEXT_RENDER_SCHEMA,REQUEST_MAX_UTF8_BYTES} from './request-lib.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
export const EXACT_SOURCE_APPENDED_COUNT=7;
export const cellId=x=>`${x.cohort}-${x.protocol}-run-${x.run}-shard-${x.shard}`;
export function allCells(){const out=[];for(const cohort of['discovery','confirmation'])for(const protocol of['A','B','C','D'])for(const run of[1,2])for(const shard of[1,2])out.push({cohort,protocol,run,shard});return out}

export function buildFrozenArtifacts({bases,design,schema,prompts,routeSha256='0'.repeat(64)}){
  const counters={discovery:0,confirmation:0};
  const samples=bases.items.map(b=>{
    const item_id=`${b.cohort==='discovery'?'D':'C'}-I${String(++counters[b.cohort]).padStart(3,'0')}`;
    const exact_source_appended=!b.runtime_context.source_construct.text.includes(b.source),source_context=renderRuntimeContext(b.runtime_context,b.source);
    if(!source_context.includes(b.source))throw Error(`SOURCE_CONTEXT_OMITS_SOURCE:${b.item_id}`);
    return{item_id,base_item_id:b.item_id,cohort:b.cohort,profile:b.profile,source:b.source,target:b.target,source_context,exact_source_appended,source_sha256:b.source_sha256,target_sha256:b.target_sha256,context_sha256:b.normalized_context_sha256};
  });
  const appended=samples.filter(x=>x.exact_source_appended).length;if(appended!==EXACT_SOURCE_APPENDED_COUNT)throw Error(`EXACT_SOURCE_APPEND_COUNT:${appended}`);
  const sampleDoc={schema_version:'gemini-context-v5-frozen-samples-v5',context_render_schema:CONTEXT_RENDER_SCHEMA,exact_source_appended_count:appended,items:samples};
  const sampleSha=sha256(jsonBytes(sampleDoc));
  const reference={schema_version:'gemini-context-v5-sealed-reference-v5',mutations_authored:false,sample_sha256:sampleSha,items:samples.map(s=>{const x={item_id:s.item_id,cohort:s.cohort,profile:s.profile,role:'CLEAN_CONTROL',atoms:[]};return{...x,row_sha256:sha256(jsonBytes(x))}})};
  const referenceSha=sha256(jsonBytes(reference)),schemaSha=sha256(jsonBytes(schema));
  const promptHashes=Object.fromEntries(Object.entries(prompts).sort((a,b)=>byteCompare(a[0],b[0])).map(([p,v])=>[p,sha256(Buffer.from(v))]));
  const requests=[];
  for(const c of allCells()){
    const def=design.protocols[c.protocol],rows=samples.filter(x=>x.cohort===c.cohort).slice((c.shard-1)*16,c.shard*16),
      clean=rows.map(x=>({item_id:x.item_id,source:x.source,target:x.target,...(def.context?{source_context:x.source_context}:{})})),
      built=buildRequest({prompt:prompts[def.prompt],schema,items:clean,withContext:def.context}),rel=`model-facing/requests/${cellId(c)}.txt`;
    requests.push({cell:cellId(c),cohort:c.cohort,protocol:c.protocol,route:'agy-gemini-3.7-flash-high',run:c.run,shard:c.shard,item_ids:clean.map(x=>x.item_id),with_context:def.context,prompt_path:def.prompt,prompt_sha256:promptHashes[def.prompt],schema_path:'model-facing/schemas/REVIEWER-SCHEMA.json',schema_sha256:schemaSha,sample_sha256:sampleSha,reference_sha256:referenceSha,path:rel,sha256:built.request_sha256,utf8_bytes:built.utf8_bytes,bytes:built.request});
  }
  if(requests.length!==32)throw Error('REQUEST_COUNT');
  if(new Set(requests.flatMap(x=>x.item_ids)).size!==64)throw Error('REQUEST_ITEM_UNION');
  return{sampleDoc,reference,requests,manifest:{schema_version:'gemini-context-v5-request-manifest-v5',context_render_schema:CONTEXT_RENDER_SCHEMA,exact_source_appended_count:appended,request_max_utf8_bytes:REQUEST_MAX_UTF8_BYTES,route_contract_sha256:routeSha256,sample_sha256:sampleSha,reference_sha256:referenceSha,schema_sha256:schemaSha,prompt_hashes:promptHashes,requests:requests.map(({bytes,...x})=>x)}};
}
export function buildFromRoot(root=here){
  const bases=readCanonical(path.join(root,'frozen/BASES.json')),design=readCanonical(path.join(root,'DESIGN-CONTRACT.json')),
    schema=readCanonical(path.join(root,'model-facing/schemas/REVIEWER-SCHEMA.json')),
    prompts=Object.fromEntries([...new Set(Object.values(design.protocols).map(x=>x.prompt))].map(rel=>[rel,fs.readFileSync(path.join(root,rel),'utf8')]));
  return buildFrozenArtifacts({bases,design,schema,prompts,routeSha256:shaFile(path.join(root,'ROUTE-CONTRACT.json'))});
}
const frozenTargets=[['frozen/SAMPLES.json','sampleDoc'],['sealed/REFERENCE.json','reference'],['frozen/REQUEST-MANIFEST.json','manifest']];
// Deterministic: two independent builds must be byte-identical; if the frozen
// artifacts already exist on disk, their bytes must equal the rebuild exactly.
// F8: the freeze is all-or-none. A tree where some frozen targets exist and others do not is a
// partial freeze: the request bytes a gate was authored against are no longer fully on disk.
// `freeze()` itself passes allowPartial, because a resumed freeze legitimately starts partial.
export function freezeState(root,built){
  const targets=[...frozenTargets.map(([rel])=>rel),...built.requests.map(r=>r.path)];
  const present=targets.filter(rel=>fs.existsSync(path.join(root,rel)));
  return{targets:targets.length,present:present.length,partial:present.length>0&&present.length<targets.length,missing:targets.filter(rel=>!fs.existsSync(path.join(root,rel)))};
}
export function checkFreeze(root=here,{allowPartial=false}={}){
  const errors=[];let a,b;
  try{a=buildFromRoot(root);b=buildFromRoot(root)}catch(e){return{errors:[`BUILD:${e.message}`],built:null}}
  for(const [rel,key] of frozenTargets)if(!jsonBytes(a[key]).equals(jsonBytes(b[key])))errors.push(`NONDETERMINISTIC:${rel}`);
  for(let i=0;i<a.requests.length;i++)if(!a.requests[i].bytes.equals(b.requests[i].bytes))errors.push(`NONDETERMINISTIC:${a.requests[i].path}`);
  if(a.requests.length!==32)errors.push('REQUEST_COUNT');
  if(a.manifest.exact_source_appended_count!==EXACT_SOURCE_APPENDED_COUNT)errors.push('EXACT_SOURCE_APPENDED_COUNT');
  for(const r of a.requests){if(r.utf8_bytes>REQUEST_MAX_UTF8_BYTES)errors.push(`REQUEST_SIZE_BOUND:${r.path}`);if(sha256(r.bytes)!==r.sha256||r.bytes.length!==r.utf8_bytes)errors.push(`REQUEST_HASH:${r.path}`)}
  for(const [rel,key] of frozenTargets){const p=path.join(root,rel);if(fs.existsSync(p)&&!fs.readFileSync(p).equals(jsonBytes(a[key])))errors.push(`FROZEN_BYTES:${rel}`)}
  for(const r of a.requests){const p=path.join(root,r.path);if(fs.existsSync(p)&&!fs.readFileSync(p).equals(r.bytes))errors.push(`REQUEST_BYTES:${r.path}`)}
  const fs_=freezeState(root,a);
  if(fs_.partial&&!allowPartial)errors.push(`FREEZE_PARTIAL:${fs_.present}/${fs_.targets}:${fs_.missing.slice(0,3).join(',')}`);
  return{errors,built:a,freeze_state:fs_};
}
// Present only when all frozen artifacts already exist (post-freeze integrity).
export function validateFrozenOnDisk(root=here){
  const errors=[],built=buildFromRoot(root);
  for(const [rel,key] of frozenTargets){const p=path.join(root,rel);if(!fs.existsSync(p)||!fs.readFileSync(p).equals(jsonBytes(built[key])))errors.push(`FROZEN_BYTES:${rel}`)}
  for(const r of built.requests){const p=path.join(root,r.path);if(!fs.existsSync(p)||!fs.readFileSync(p).equals(r.bytes))errors.push(`REQUEST_BYTES:${r.path}`)}
  return errors;
}
function commitExact(p,bytes){const b=Buffer.isBuffer(bytes)?bytes:jsonBytes(bytes);if(fs.existsSync(p)){if(!fs.readFileSync(p).equals(b))throw Error(`FREEZE_EXISTING_DRIFT:${p}`);return}writeExclusive(p,b)}
export function freeze(root=here){
  const {errors,built}=checkFreeze(root,{allowPartial:true});if(errors.length)throw Error(`FREEZE_CHECK:${errors.join(',')}`);
  commitExact(path.join(root,'frozen/SAMPLES.json'),built.sampleDoc);commitExact(path.join(root,'sealed/REFERENCE.json'),built.reference);
  for(const r of built.requests)commitExact(path.join(root,r.path),r.bytes);
  commitExact(path.join(root,'frozen/REQUEST-MANIFEST.json'),built.manifest);
  const left=validateFrozenOnDisk(root);if(left.length)throw Error(left.join(','));
  return{samples:64,requests:32,reference_sha256:built.manifest.reference_sha256,max_request_utf8_bytes:Math.max(...built.manifest.requests.map(x=>x.utf8_bytes)),request_bound_utf8_bytes:REQUEST_MAX_UTF8_BYTES};
}
if(import.meta.url===`file://${process.argv[1]}`){
  try{
    if(process.argv.includes('--check')){const r=checkFreeze();console.log(JSON.stringify({mode:'CHECK',requests:r.built?.requests.length??0,exact_source_appended_count:r.built?.manifest.exact_source_appended_count??null,max_request_utf8_bytes:r.built?Math.max(...r.built.requests.map(x=>x.utf8_bytes)):null,freeze_state:r.freeze_state?{...r.freeze_state,missing:r.freeze_state.missing.length>5?[...r.freeze_state.missing.slice(0,5),`... and ${r.freeze_state.missing.length-5} more`]:r.freeze_state.missing}:null,errors:r.errors},null,2));process.exitCode=r.errors.length?3:0}
    else console.log(JSON.stringify(freeze(),null,2));
  }catch(e){console.error(e.message);process.exitCode=3}
}
