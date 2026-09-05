#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readCanonical,jsonBytes,sha256,writeExclusive,shaFile,byteCompare} from './lib.mjs';
import {mutationGate} from './mutation-gate.mjs';
import {buildRequest,renderRuntimeContext,CONTEXT_RENDER_SCHEMA,REQUEST_MAX_UTF8_BYTES} from './request-lib.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const roles={CONTEXT_MUTANT:6,SURFACE_MUTANT:4,CLEAN_CONTROL:6};
function exact(x,keys){return x&&JSON.stringify(Object.keys(x).sort(byteCompare))===JSON.stringify([...keys].sort(byteCompare))}

export function buildFrozenArtifacts({bases,plan,props,design,schema,prompts,routeSha256='0'.repeat(64)}){
  const byProp=new Map(props.items.map(x=>[x.item_id,x])),byRole=new Map(plan.items.map(x=>[x.item_id,x])),counters={discovery:0,confirmation:0};
  const samples=bases.items.map(b=>{
    const a=byRole.get(b.item_id),p=byProp.get(b.item_id),item_id=`${b.cohort==='discovery'?'D':'C'}-I${String(++counters[b.cohort]).padStart(3,'0')}`;
    if(!a)throw Error(`ASSIGNMENT_MISSING:${b.item_id}`);
    const exact_source_appended=!b.runtime_context.source_construct.text.includes(b.source),source_context=renderRuntimeContext(b.runtime_context,b.source);
    if(!source_context.includes(b.source))throw Error(`SOURCE_CONTEXT_OMITS_SOURCE:${b.item_id}`);
    return{item_id,base_item_id:b.item_id,cohort:b.cohort,profile:b.profile,role:a.planned_role,source:b.source,target:p?.mutated_target??b.target,source_context,exact_source_appended,source_sha256:b.source_sha256,original_target_sha256:b.target_sha256,context_sha256:b.normalized_context_sha256};
  });
  const exactSourceAppendCount=samples.filter(x=>x.exact_source_appended).length;if(exactSourceAppendCount!==7)throw Error(`EXACT_SOURCE_APPEND_COUNT:${exactSourceAppendCount}`);
  const sampleDoc={schema_version:'gemini-context-v5-frozen-samples-v4',context_render_schema:CONTEXT_RENDER_SCHEMA,exact_source_appended_count:exactSourceAppendCount,items:samples};
  const sampleSha=sha256(jsonBytes(sampleDoc));
  const reference={schema_version:'gemini-context-v5-sealed-reference-v4',sample_sha256:sampleSha,items:samples.map(s=>{const p=byProp.get(s.base_item_id),x={item_id:s.item_id,cohort:s.cohort,profile:s.profile,role:s.role,atoms:p?[{atom_id:`${s.item_id}-A1`,claim_types:[p.claim_type],target_spans:[p.edit_mutated]}]:[]};return{...x,row_sha256:sha256(jsonBytes(x))}})};
  const referenceSha=sha256(jsonBytes(reference)),schemaSha=sha256(jsonBytes(schema));
  const promptHashes=Object.fromEntries(Object.entries(prompts).sort((a,b)=>byteCompare(a[0],b[0])).map(([p,v])=>[p,sha256(Buffer.from(v))]));
  const requests=[];
  for(const cohort of ['discovery','confirmation'])for(const protocol of ['A','B','C','D'])for(const run of [1,2])for(const shard of [1,2]){
    const def=design.protocols[protocol],rows=samples.filter(x=>x.cohort===cohort).slice((shard-1)*16,shard*16),clean=rows.map(x=>({item_id:x.item_id,source:x.source,target:x.target,...(def.context?{source_context:x.source_context}:{})})),built=buildRequest({prompt:prompts[def.prompt],schema,items:clean,withContext:def.context}),name=`${cohort}-${protocol}-run-${run}-shard-${shard}.txt`,rel=`model-facing/requests/${name}`;
    requests.push({cohort,protocol,route:'agy-gemini-3.7-flash-high',run,shard,item_ids:clean.map(x=>x.item_id),with_context:def.context,prompt_path:def.prompt,prompt_sha256:promptHashes[def.prompt],schema_path:'model-facing/schemas/REVIEWER-SCHEMA.json',schema_sha256:schemaSha,sample_sha256:sampleSha,reference_sha256:referenceSha,path:rel,sha256:built.request_sha256,utf8_bytes:built.utf8_bytes,bytes:built.request});
  }
  if(requests.length!==32)throw Error('REQUEST_COUNT');
  return{sampleDoc,reference,requests,manifest:{schema_version:'gemini-context-v5-request-manifest-v4',context_render_schema:CONTEXT_RENDER_SCHEMA,exact_source_appended_count:exactSourceAppendCount,request_max_utf8_bytes:REQUEST_MAX_UTF8_BYTES,route_contract_sha256:routeSha256,sample_sha256:sampleSha,reference_sha256:referenceSha,schema_sha256:schemaSha,prompt_hashes:promptHashes,requests:requests.map(({bytes,...x})=>x)}};
}
function commitExact(p,bytes){const b=Buffer.isBuffer(bytes)?bytes:jsonBytes(bytes);if(fs.existsSync(p)){if(!fs.readFileSync(p).equals(b))throw Error(`FREEZE_EXISTING_DRIFT:${p}`);return}writeExclusive(p,b)}
export function validateFrozenSeam(root,built){
  const errors=[];
  for(const [rel,obj] of [['frozen/SAMPLES.json',built.sampleDoc],['sealed/REFERENCE.json',built.reference],['frozen/REQUEST-MANIFEST.json',built.manifest]])if(!fs.existsSync(path.join(root,rel))||!fs.readFileSync(path.join(root,rel)).equals(jsonBytes(obj)))errors.push(`FROZEN_BYTES:${rel}`);
  for(const r of built.requests)if(!fs.existsSync(path.join(root,r.path))||!fs.readFileSync(path.join(root,r.path)).equals(r.bytes))errors.push(`REQUEST_BYTES:${r.path}`);
  if(built.reference.sample_sha256!==sha256(jsonBytes(built.sampleDoc)))errors.push('REFERENCE_SAMPLE_HASH');
  return errors;
}
export function validateFrozenArtifactsOnDisk(root=here){
  try{
    const bases=readCanonical(path.join(root,'frozen/BASES.json')),plan=readCanonical(path.join(root,'frozen/ASSIGNMENT-PLAN.json')),props=readCanonical(path.join(root,'sealed/MUTATION-PROPOSALS.json')),design=readCanonical(path.join(root,'DESIGN-CONTRACT.json')),schema=readCanonical(path.join(root,'model-facing/schemas/REVIEWER-SCHEMA.json')),prompts=Object.fromEntries([...new Set(Object.values(design.protocols).map(x=>x.prompt))].map(rel=>[rel,fs.readFileSync(path.join(root,rel),'utf8')])),routeSha256=shaFile(path.join(root,'ROUTE-CONTRACT.json')),built=buildFrozenArtifacts({bases,plan,props,design,schema,prompts,routeSha256});
    return validateFrozenSeam(root,built);
  }catch(e){return[`FROZEN_REGEN:${e.message}`]}
}
export function freeze(root=here,options={}){
  if(!options.skipMutationGate){const mg=mutationGate(root,options.mutationOptions);if(mg.status!=='PASS')throw Error(`MUTATION_GATE:${mg.errors?.join(',')}`)}
  const bases=options.bases??readCanonical(path.join(root,'frozen/BASES.json')),plan=options.plan??readCanonical(path.join(root,'frozen/ASSIGNMENT-PLAN.json')),props=options.props??readCanonical(path.join(root,'sealed/MUTATION-PROPOSALS.json')),design=readCanonical(path.join(root,'DESIGN-CONTRACT.json')),schemaPath=path.join(root,'model-facing/schemas/REVIEWER-SCHEMA.json'),schema=readCanonical(schemaPath),prompts=Object.fromEntries([...new Set(Object.values(design.protocols).map(x=>x.prompt))].map(rel=>[rel,fs.readFileSync(path.join(root,rel),'utf8')])),routeSha256=shaFile(path.join(root,'ROUTE-CONTRACT.json')),built=buildFrozenArtifacts({bases,plan,props,design,schema,prompts,routeSha256});
  commitExact(path.join(root,'frozen/SAMPLES.json'),built.sampleDoc);commitExact(path.join(root,'sealed/REFERENCE.json'),built.reference);for(const r of built.requests)commitExact(path.join(root,r.path),r.bytes);commitExact(path.join(root,'frozen/REQUEST-MANIFEST.json'),built.manifest);
  const seam=validateFrozenSeam(root,built);if(seam.length)throw Error(seam.join(','));
  return{samples:64,requests:32,reference_sha256:built.manifest.reference_sha256,max_request_utf8_bytes:Math.max(...built.manifest.requests.map(x=>x.utf8_bytes)),request_bound_utf8_bytes:REQUEST_MAX_UTF8_BYTES};
}
if(import.meta.url===`file://${process.argv[1]}`){try{console.log(JSON.stringify(freeze(),null,2))}catch(e){console.error(e.message);process.exitCode=3}}
