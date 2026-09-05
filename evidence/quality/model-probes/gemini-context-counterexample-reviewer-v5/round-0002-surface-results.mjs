#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildSurfaceAggregateBytes, jsonBytes, sha256} from './round-lineage.mjs';
import {ROUND2_REVIEWED_CANDIDATE, validateFrozenRound1Files} from './round-0002-surface-input.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
export const ROUND2_SURFACE_CALL=Object.freeze({auditor_agent_id:'cdb6b356-29b8-4d55-821c-e43aac231ee4',authorized_call_number:1,call_count_allowance:1,response_path:'AUDITOR-RESPONSE-ROUND-0002-SURFACE-CALL-001.json',response_sha256:'6410f621356fc97af7d5773801ad0d64810f5ce93b6a8d4db3b912078585fd4a'});
const ALLOWED=['PASS_SURFACE','NOT_CLEAN','OUT_OF_SCOPE_NON_PROSE'];
const exactKeys=(value,keys)=>value&&typeof value==='object'&&!Array.isArray(value)&&JSON.stringify(Object.keys(value).sort())===JSON.stringify([...keys].sort());

function parseJsonNoDuplicateKeys(bytes,label){
  const text=bytes.toString('utf8');if(!Buffer.from(text).equals(bytes))throw Error(`${label}_UTF8`);let at=0;
  const whitespace=()=>{while(/\s/u.test(text[at]??''))at+=1;};
  const string=()=>{const start=at;if(text[at++]!=='"')throw Error(`${label}_STRING`);while(at<text.length){if(text[at]==='\\'){at+=2;continue;}if(text[at++]==='"')return JSON.parse(text.slice(start,at));}throw Error(`${label}_STRING`);};
  const value=()=>{whitespace();const token=text[at];if(token==='"')return string();if(token==='{'){at+=1;whitespace();const out={},seen=new Set();if(text[at]==='}'){at+=1;return out;}while(true){whitespace();const key=string();if(seen.has(key))throw Error(`${label}_DUPLICATE_KEY:${key}`);seen.add(key);whitespace();if(text[at++]!==':')throw Error(`${label}_OBJECT`);out[key]=value();whitespace();if(text[at]==='}'){at+=1;return out;}if(text[at++]!==',')throw Error(`${label}_OBJECT`);}}if(token==='['){at+=1;whitespace();const out=[];if(text[at]===']'){at+=1;return out;}while(true){out.push(value());whitespace();if(text[at]===']'){at+=1;return out;}if(text[at++]!==',')throw Error(`${label}_ARRAY`);}}for(const [literal,parsed] of [['true',true],['false',false],['null',null]])if(text.startsWith(literal,at)){at+=literal.length;return parsed;}const match=text.slice(at).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/u);if(!match)throw Error(`${label}_VALUE`);at+=match[0].length;return JSON.parse(match[0]);};
  const parsed=value();whitespace();if(at!==text.length)throw Error(`${label}_TRAILING_BYTES`);return parsed;
}

function canonical(bytes,label){const parsed=parseJsonNoDuplicateKeys(bytes,label);if(!bytes.equals(jsonBytes(parsed)))throw Error(`${label}_NONCANONICAL_BYTES`);return parsed;}

export function validateRound2RawSurfaceResponse({root=here,queueBytes,viewBytes,responseBytes=fs.readFileSync(path.join(root,ROUND2_SURFACE_CALL.response_path)),expectedResponseSha256=ROUND2_SURFACE_CALL.response_sha256}={}){
  validateFrozenRound1Files(root);const queue=canonical(queueBytes??fs.readFileSync(path.join(root,'rounds/ROUND-0002/SURFACE-QUEUE.json')),'ROUND2_QUEUE'),view=canonical(viewBytes??fs.readFileSync(path.join(root,'rounds/ROUND-0002/SURFACE-QUEUE-VIEW.json')),'ROUND2_VIEW'),response=canonical(Buffer.from(responseBytes),'ROUND2_SURFACE_RESPONSE');
  if(sha256(responseBytes)!==expectedResponseSha256)throw Error('ROUND2_SURFACE_RESPONSE_HASH');
  if(!exactKeys(response,['schema_version','queue_view_sha256','results'])||response.schema_version!=='gemini-context-v5-surface-auditor-response-v2'||response.queue_view_sha256!==ROUND2_REVIEWED_CANDIDATE.view_sha256||response.queue_view_sha256!==sha256(viewBytes??fs.readFileSync(path.join(root,'rounds/ROUND-0002/SURFACE-QUEUE-VIEW.json')))||!Array.isArray(response.results)||response.results.length!==10)throw Error('ROUND2_SURFACE_RESPONSE_SCHEMA');
  const ids=response.results.map(item=>item.neutral_id);if(new Set(ids).size!==ids.length||JSON.stringify(ids)!==JSON.stringify(queue.items.map(item=>item.neutral_id)))throw Error('ROUND2_SURFACE_RESPONSE_ORDER_OR_DUPLICATE');
  response.results.forEach((item,index)=>{if(!exactKeys(item,['neutral_id','verdict','evidence'])||!ALLOWED.includes(item.verdict)||typeof item.evidence!=='string'||!item.evidence.trim())throw Error(`ROUND2_SURFACE_RESPONSE_ITEM:${index}`);});
  const counts=Object.fromEntries(ALLOWED.map(verdict=>[verdict,response.results.filter(item=>item.verdict===verdict).length]));
  if(counts.PASS_SURFACE!==9||counts.NOT_CLEAN!==0||counts.OUT_OF_SCOPE_NON_PROSE!==1||response.results.find(item=>item.verdict==='OUT_OF_SCOPE_NON_PROSE')?.neutral_id!=='V4-C-D06')throw Error('ROUND2_SURFACE_RESPONSE_COUNTS');
  return {bytes:Buffer.from(responseBytes),parsed:response,counts,queue,view};
}

export function buildRound2SurfaceArtifacts(options={}){
  const root=options.root??here,queueBytes=options.queueBytes??fs.readFileSync(path.join(root,'rounds/ROUND-0002/SURFACE-QUEUE.json')),viewBytes=options.viewBytes??fs.readFileSync(path.join(root,'rounds/ROUND-0002/SURFACE-QUEUE-VIEW.json')),validated=validateRound2RawSurfaceResponse({...options,root,queueBytes,viewBytes});
  const recordsBytes=jsonBytes({schema_version:'gemini-context-v5-surface-records-v2',round_id:'ROUND-0002',stage:'SURFACE',surface_queue_sha256:sha256(queueBytes),surface_queue_view_sha256:sha256(viewBytes),items:validated.parsed.results});
  const aggregateBytes=buildSurfaceAggregateBytes(queueBytes,viewBytes,recordsBytes),aggregate=canonical(aggregateBytes,'ROUND2_SURFACE_AGGREGATE');
  if(JSON.stringify(aggregate.counts)!==JSON.stringify(validated.counts)||JSON.stringify(aggregate.pass_ids)!==JSON.stringify(validated.parsed.results.filter(item=>item.verdict==='PASS_SURFACE').map(item=>item.neutral_id))||JSON.stringify(aggregate.reject_ids)!==JSON.stringify(['V4-C-D06']))throw Error('ROUND2_SURFACE_AGGREGATE_COUNTS');
  return {response:validated,recordsBytes,aggregateBytes,aggregate,contextEligibleIds:aggregate.pass_ids};
}

export function validateRound2SurfaceArtifacts({root=here}={}){
  const built=buildRound2SurfaceArtifacts({root}),round=path.join(root,'rounds/ROUND-0002'),records=fs.readFileSync(path.join(round,'SURFACE-RECORDS.json')),aggregate=fs.readFileSync(path.join(round,'SURFACE-AGGREGATE.json'));
  if(!records.equals(built.recordsBytes))throw Error('ROUND2_SURFACE_RECORDS_DRIFT');if(!aggregate.equals(built.aggregateBytes))throw Error('ROUND2_SURFACE_AGGREGATE_DRIFT');
  return {raw_response_sha256:ROUND2_SURFACE_CALL.response_sha256,surface_records_sha256:sha256(records),surface_aggregate_sha256:sha256(aggregate),counts:built.aggregate.counts,context_eligible_ids:built.contextEligibleIds};
}

export function materializeRound2SurfaceArtifacts({root=here}={}){
  const built=buildRound2SurfaceArtifacts({root}),round=path.join(root,'rounds/ROUND-0002'),records=path.join(round,'SURFACE-RECORDS.json'),aggregate=path.join(round,'SURFACE-AGGREGATE.json');
  if(fs.existsSync(records)||fs.existsSync(aggregate))throw Error('ROUND2_SURFACE_RESULTS_ALREADY_MATERIALIZED');
  const recordsTmp=`${records}.tmp`,aggregateTmp=`${aggregate}.tmp`;try{fs.writeFileSync(recordsTmp,built.recordsBytes,{flag:'wx'});fs.writeFileSync(aggregateTmp,built.aggregateBytes,{flag:'wx'});fs.renameSync(recordsTmp,records);fs.renameSync(aggregateTmp,aggregate);}catch(error){for(const file of [recordsTmp,aggregateTmp])if(fs.existsSync(file))fs.unlinkSync(file);throw error;}
  return validateRound2SurfaceArtifacts({root});
}

if(import.meta.url===`file://${process.argv[1]}`){const command=process.argv[2];if(command==='--materialize')console.log(JSON.stringify(materializeRound2SurfaceArtifacts(),null,2));else if(command==='--check')console.log(JSON.stringify(validateRound2SurfaceArtifacts(),null,2));else throw Error('usage: node round-0002-surface-results.mjs --materialize|--check');}
