#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
export const ROUND3_CONTEXT_CALL=Object.freeze({
  auditor_agent_id:'8c6aae6c-df2e-4632-9047-76a36f6d1cba',
  auditor_session_id:'01a0585c-0b37-79fd-85ef-47bd4b9d2173',
  auditor_message_id:'39be9032',
  authorized_call_number:1,
  call_count_allowance:1,
  calls_started:1,
  calls_remaining:0,
  response_path:'AUDITOR-RESPONSE-ROUND-0003-CONTEXT-CALL-001.json',
  response_sha256:'7799ee69506d5ca2328ee8fa1d5957707d2522054f16ff3aaa02361da2acaa17',
  context_queue_view_sha256:'900fe68d898303e1fcd64567119c33d6471119a5b9a5cbfc74ad41cc7dc0e44e'
});
const IDS=Object.freeze(['V4-D-D05','V4-C-D06']);
const ALLOWED=Object.freeze(['CLEAN_NO_MATERIAL_DEFECT','NOT_CLEAN']);
const sha256=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const jsonBytes=value=>Buffer.from(`${JSON.stringify(value,null,2)}\n`);
const exactKeys=(value,keys)=>value&&typeof value==='object'&&!Array.isArray(value)&&JSON.stringify(Object.keys(value).sort())===JSON.stringify([...keys].sort());

function parseNoDuplicateKeys(bytes,label){
  const text=bytes.toString('utf8');if(!Buffer.from(text).equals(bytes))throw Error(`${label}_UTF8`);let at=0;
  const ws=()=>{while(/\s/u.test(text[at]??''))at+=1;};
  const string=()=>{const start=at;if(text[at++]!=='"')throw Error(`${label}_STRING`);while(at<text.length){if(text[at]==='\\'){at+=2;continue;}if(text[at++]==='"')return JSON.parse(text.slice(start,at));}throw Error(`${label}_STRING`);};
  const value=()=>{ws();const token=text[at];if(token==='"')return string();if(token==='{'){at+=1;ws();const out={},seen=new Set();if(text[at]==='}'){at+=1;return out;}while(true){ws();const key=string();if(seen.has(key))throw Error(`${label}_DUPLICATE_KEY:${key}`);seen.add(key);ws();if(text[at++]!==':')throw Error(`${label}_OBJECT`);out[key]=value();ws();if(text[at]==='}'){at+=1;return out;}if(text[at++]!==',')throw Error(`${label}_OBJECT`);}}if(token==='['){at+=1;ws();const out=[];if(text[at]===']'){at+=1;return out;}while(true){out.push(value());ws();if(text[at]===']'){at+=1;return out;}if(text[at++]!==',')throw Error(`${label}_ARRAY`);}}for(const [literal,parsed] of [['true',true],['false',false],['null',null]])if(text.startsWith(literal,at)){at+=literal.length;return parsed;}const match=text.slice(at).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/u);if(!match)throw Error(`${label}_VALUE`);at+=match[0].length;return JSON.parse(match[0]);};
  const parsed=value();ws();if(at!==text.length)throw Error(`${label}_TRAILING_BYTES`);return parsed;
}
function readRegular(file,label){const stat=fs.lstatSync(file);if(stat.isSymbolicLink()||!stat.isFile())throw Error(`${label}_FILE_TYPE`);return fs.readFileSync(file);}
function canonical(bytes,label){const value=parseNoDuplicateKeys(bytes,label);if(!bytes.equals(jsonBytes(value)))throw Error(`${label}_NONCANONICAL_BYTES`);return value;}

export function validateRound3RawContextResponse({root=here,responseBytes,expectedResponseSha256=ROUND3_CONTEXT_CALL.response_sha256}={}){
  const round=path.join(root,'rounds/ROUND-0003');
  const raw=responseBytes??readRegular(path.join(root,ROUND3_CONTEXT_CALL.response_path),'ROUND3_CONTEXT_RAW');
  const queueBytes=readRegular(path.join(round,'CONTEXT-QUEUE.json'),'ROUND3_CONTEXT_QUEUE');
  const anchorsBytes=readRegular(path.join(round,'CONTEXT-SOURCE-ANCHORS.json'),'ROUND3_CONTEXT_ANCHORS');
  const viewBytes=readRegular(path.join(round,'CONTEXT-QUEUE-VIEW.json'),'ROUND3_CONTEXT_VIEW');
  const response=parseNoDuplicateKeys(raw,'ROUND3_CONTEXT_RAW'),queue=canonical(queueBytes,'ROUND3_CONTEXT_QUEUE'),view=canonical(viewBytes,'ROUND3_CONTEXT_VIEW');
  if(ROUND3_CONTEXT_CALL.call_count_allowance!==1||ROUND3_CONTEXT_CALL.calls_started!==1||ROUND3_CONTEXT_CALL.calls_remaining!==0)throw Error('ROUND3_CONTEXT_CALL_ALLOWANCE');
  if(sha256(raw)!==expectedResponseSha256)throw Error('ROUND3_CONTEXT_RAW_HASH');
  if(sha256(viewBytes)!==ROUND3_CONTEXT_CALL.context_queue_view_sha256||response.context_queue_view_sha256!==sha256(viewBytes))throw Error('ROUND3_CONTEXT_VIEW_BINDING');
  if(!exactKeys(response,['schema_version','context_queue_view_sha256','results'])||response.schema_version!=='gemini-context-v5-context-auditor-response-v2'||!Array.isArray(response.results)||response.results.length!==2)throw Error('ROUND3_CONTEXT_RESPONSE_SCHEMA');
  const queueIds=queue.items?.map(item=>item.neutral_id),viewIds=view.items?.map(item=>item.neutral_id),ids=response.results.map(item=>item.neutral_id);
  if(JSON.stringify(queueIds)!==JSON.stringify(IDS)||JSON.stringify(viewIds)!==JSON.stringify(IDS)||JSON.stringify(ids)!==JSON.stringify(IDS)||new Set(ids).size!==2)throw Error('ROUND3_CONTEXT_RESPONSE_ORDER_OR_DUPLICATE');
  response.results.forEach((item,index)=>{if(!exactKeys(item,['neutral_id','verdict','evidence'])||!ALLOWED.includes(item.verdict)||typeof item.evidence!=='string'||!item.evidence.trim())throw Error(`ROUND3_CONTEXT_RESPONSE_ITEM:${index}`);});
  const counts=Object.fromEntries(ALLOWED.map(verdict=>[verdict,response.results.filter(item=>item.verdict===verdict).length]));
  if(counts.CLEAN_NO_MATERIAL_DEFECT!==2||counts.NOT_CLEAN!==0)throw Error('ROUND3_CONTEXT_RESPONSE_COUNTS');
  return {rawBytes:raw,response,queueBytes,anchorsBytes,viewBytes,counts};
}

export function buildRound3ContextArtifacts(options={}){
  const valid=validateRound3RawContextResponse(options);
  const records={schema_version:'gemini-context-v5-context-records-v2',round_id:'ROUND-0003',stage:'CONTEXT',context_queue_sha256:sha256(valid.queueBytes),context_source_anchors_sha256:sha256(valid.anchorsBytes),context_queue_view_sha256:sha256(valid.viewBytes),items:valid.response.results};
  const recordsBytes=jsonBytes(records);
  const aggregate={schema_version:'gemini-context-v5-context-aggregate-v2',round_id:'ROUND-0003',stage:'CONTEXT',context_queue_sha256:records.context_queue_sha256,context_source_anchors_sha256:records.context_source_anchors_sha256,context_queue_view_sha256:records.context_queue_view_sha256,context_records_sha256:sha256(recordsBytes),counts:valid.counts,clean_ids:IDS,not_clean_ids:[],items:records.items};
  return {...valid,recordsBytes,aggregateBytes:jsonBytes(aggregate),aggregate};
}

export function materializeRound3ContextArtifacts({root=here}={}){
  const built=buildRound3ContextArtifacts({root}),round=path.join(root,'rounds/ROUND-0003');
  const files=[['CONTEXT-RECORDS.json',built.recordsBytes],['CONTEXT-AGGREGATE.json',built.aggregateBytes]];
  if(files.some(([name])=>fs.existsSync(path.join(round,name))))throw Error('ROUND3_CONTEXT_RESULTS_ALREADY_EXIST');
  const temps=files.map(([name,bytes])=>[path.join(round,`${name}.tmp`),path.join(round,name),bytes]);
  try{for(const [tmp,,bytes]of temps)fs.writeFileSync(tmp,bytes,{flag:'wx'});for(const [tmp,file]of temps)fs.renameSync(tmp,file);}catch(error){for(const [tmp]of temps)if(fs.existsSync(tmp))fs.unlinkSync(tmp);throw error;}
  return validateRound3ContextArtifacts({root});
}

export function validateRound3ContextArtifacts({root=here}={}){
  const built=buildRound3ContextArtifacts({root}),round=path.join(root,'rounds/ROUND-0003');
  const records=readRegular(path.join(round,'CONTEXT-RECORDS.json'),'ROUND3_CONTEXT_RECORDS'),aggregate=readRegular(path.join(round,'CONTEXT-AGGREGATE.json'),'ROUND3_CONTEXT_AGGREGATE');
  if(!records.equals(built.recordsBytes))throw Error('ROUND3_CONTEXT_RECORDS_DRIFT');
  if(!aggregate.equals(built.aggregateBytes))throw Error('ROUND3_CONTEXT_AGGREGATE_DRIFT');
  return {auditor_agent_id:ROUND3_CONTEXT_CALL.auditor_agent_id,auditor_session_id:ROUND3_CONTEXT_CALL.auditor_session_id,auditor_message_id:ROUND3_CONTEXT_CALL.auditor_message_id,raw_response_sha256:sha256(built.rawBytes),call_count_allowance:1,calls_started:1,calls_remaining:0,context_records_sha256:sha256(records),context_aggregate_sha256:sha256(aggregate),counts:built.counts,clean_ids:built.aggregate.clean_ids,not_clean_ids:built.aggregate.not_clean_ids};
}

if(import.meta.url===`file://${process.argv[1]}`){if(process.argv[2]==='--materialize')console.log(JSON.stringify(materializeRound3ContextArtifacts(),null,2));else if(process.argv[2]==='--check')console.log(JSON.stringify(validateRound3ContextArtifacts(),null,2));else throw Error('usage: --materialize|--check');}
