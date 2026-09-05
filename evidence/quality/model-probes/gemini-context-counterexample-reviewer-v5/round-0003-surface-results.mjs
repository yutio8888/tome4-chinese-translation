#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {buildSurfaceAggregateBytes, jsonBytes, sha256} from './round-lineage.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
export const ROUND3_SURFACE_CALL=Object.freeze({
  auditor_agent_id:'216516d5-3b1c-4ec4-b0f6-8d0e984bf698',
  auditor_session_id:'01a05826-b038-7d29-b437-c5c3e3f19578',
  authorized_call_number:1,call_count_allowance:1,calls_started:1,calls_remaining:0,
  response_path:'AUDITOR-RESPONSE-ROUND-0003-SURFACE-CALL-001.json',
  response_sha256:'59dcb66b519ee97e97b421b21405c1a0aee943f41c798c30cf5d150e8c4352e1',
  queue_view_sha256:'f1f35c1a1c28638c706630b45422efa6b94380b8ff89397fecef78c4f3e6ca0b'
});
const IDS=Object.freeze(['V4-D-D05','V4-C-D06']),ALLOWED=Object.freeze(['PASS_SURFACE','NOT_CLEAN','OUT_OF_SCOPE_NON_PROSE']);
const exactKeys=(value,keys)=>value&&typeof value==='object'&&!Array.isArray(value)&&JSON.stringify(Object.keys(value).sort())===JSON.stringify([...keys].sort());
function parseNoDuplicates(bytes,label){
  const text=bytes.toString('utf8');if(!Buffer.from(text).equals(bytes))throw Error(`${label}_UTF8`);let at=0;
  const ws=()=>{while(/\s/u.test(text[at]??''))at++;};
  const str=()=>{const start=at;if(text[at++]!=='"')throw Error(`${label}_STRING`);while(at<text.length){if(text[at]==='\\'){at+=2;continue;}if(text[at++]==='"')return JSON.parse(text.slice(start,at));}throw Error(`${label}_STRING`);};
  const value=()=>{ws();const token=text[at];if(token==='"')return str();if(token==='{'){at++;ws();const out={},seen=new Set();if(text[at]==='}'){at++;return out;}while(true){ws();const key=str();if(seen.has(key))throw Error(`${label}_DUPLICATE_KEY:${key}`);seen.add(key);ws();if(text[at++]!==':')throw Error(`${label}_OBJECT`);out[key]=value();ws();if(text[at]==='}'){at++;return out;}if(text[at++]!==',')throw Error(`${label}_OBJECT`);}}if(token==='['){at++;ws();const out=[];if(text[at]===']'){at++;return out;}while(true){out.push(value());ws();if(text[at]===']'){at++;return out;}if(text[at++]!==',')throw Error(`${label}_ARRAY`);}}for(const [literal,parsed]of[['true',true],['false',false],['null',null]])if(text.startsWith(literal,at)){at+=literal.length;return parsed;}const match=text.slice(at).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/u);if(!match)throw Error(`${label}_VALUE`);at+=match[0].length;return JSON.parse(match[0]);};
  const parsed=value();ws();if(at!==text.length)throw Error(`${label}_TRAILING_BYTES`);return parsed;
}
function readRegular(file,label){const stat=fs.lstatSync(file);if(stat.isSymbolicLink()||!stat.isFile())throw Error(`${label}_FILE_TYPE`);return fs.readFileSync(file);}
function canonical(bytes,label){const value=parseNoDuplicates(bytes,label);if(!bytes.equals(jsonBytes(value)))throw Error(`${label}_NONCANONICAL_BYTES`);return value;}
export function validateRound3RawSurfaceResponse({root=here,responseBytes,queueBytes,viewBytes}={}){
  const round=path.join(root,'rounds/ROUND-0003');
  const raw=responseBytes??readRegular(path.join(root,ROUND3_SURFACE_CALL.response_path),'ROUND3_SURFACE_RAW');
  const qBytes=queueBytes??readRegular(path.join(round,'SURFACE-QUEUE.json'),'ROUND3_SURFACE_QUEUE');
  const vBytes=viewBytes??readRegular(path.join(round,'SURFACE-QUEUE-VIEW.json'),'ROUND3_SURFACE_VIEW');
  const response=parseNoDuplicates(raw,'ROUND3_SURFACE_RAW'),queue=canonical(qBytes,'ROUND3_SURFACE_QUEUE'),view=canonical(vBytes,'ROUND3_SURFACE_VIEW');
  if(sha256(raw)!==ROUND3_SURFACE_CALL.response_sha256)throw Error('ROUND3_SURFACE_RAW_HASH');
  if(sha256(vBytes)!==ROUND3_SURFACE_CALL.queue_view_sha256||response.queue_view_sha256!==sha256(vBytes))throw Error('ROUND3_SURFACE_VIEW_BINDING');
  if(!exactKeys(response,['schema_version','queue_view_sha256','results'])||response.schema_version!=='gemini-context-v5-surface-auditor-response-v2'||!Array.isArray(response.results)||response.results.length!==2)throw Error('ROUND3_SURFACE_RESPONSE_SCHEMA');
  if(JSON.stringify(queue.items.map(x=>x.neutral_id))!==JSON.stringify(IDS)||JSON.stringify(response.results.map(x=>x.neutral_id))!==JSON.stringify(IDS)||new Set(response.results.map(x=>x.neutral_id)).size!==2)throw Error('ROUND3_SURFACE_RESPONSE_ORDER');
  response.results.forEach((item,index)=>{if(!exactKeys(item,['neutral_id','verdict','evidence'])||!ALLOWED.includes(item.verdict)||typeof item.evidence!=='string'||!item.evidence.trim())throw Error(`ROUND3_SURFACE_RESPONSE_ITEM:${index}`);});
  const counts=Object.fromEntries(ALLOWED.map(verdict=>[verdict,response.results.filter(x=>x.verdict===verdict).length]));
  if(counts.PASS_SURFACE!==2||counts.NOT_CLEAN!==0||counts.OUT_OF_SCOPE_NON_PROSE!==0)throw Error('ROUND3_SURFACE_RESPONSE_COUNTS');
  return {rawBytes:raw,response,queueBytes:qBytes,queue,viewBytes:vBytes,view,counts};
}
export function buildRound3SurfaceArtifacts(options={}){
  const valid=validateRound3RawSurfaceResponse(options);
  const recordsBytes=jsonBytes({schema_version:'gemini-context-v5-surface-records-v2',round_id:'ROUND-0003',stage:'SURFACE',surface_queue_sha256:sha256(valid.queueBytes),surface_queue_view_sha256:sha256(valid.viewBytes),items:valid.response.results});
  const aggregateBytes=buildSurfaceAggregateBytes(valid.queueBytes,valid.viewBytes,recordsBytes),aggregate=canonical(aggregateBytes,'ROUND3_SURFACE_AGGREGATE');
  if(JSON.stringify(aggregate.counts)!==JSON.stringify(valid.counts)||JSON.stringify(aggregate.pass_ids)!==JSON.stringify(IDS)||aggregate.reject_ids.length!==0)throw Error('ROUND3_SURFACE_AGGREGATE_BINDING');
  return {...valid,recordsBytes,aggregateBytes,aggregate};
}
export function materializeRound3SurfaceArtifacts(options={}){const root=options.root??here,round=path.join(root,'rounds/ROUND-0003'),built=buildRound3SurfaceArtifacts({...options,root}),files=[['SURFACE-RECORDS.json',built.recordsBytes],['SURFACE-AGGREGATE.json',built.aggregateBytes]];if(files.some(([name])=>fs.existsSync(path.join(round,name))))throw Error('ROUND3_SURFACE_RESULTS_ALREADY_EXIST');for(const [name,bytes]of files)fs.writeFileSync(path.join(round,name),bytes,{flag:'wx'});return validateRound3SurfaceArtifacts({root});}
export function validateRound3SurfaceArtifacts({root=here}={}){const built=buildRound3SurfaceArtifacts({root}),round=path.join(root,'rounds/ROUND-0003'),records=readRegular(path.join(round,'SURFACE-RECORDS.json'),'ROUND3_SURFACE_RECORDS'),aggregate=readRegular(path.join(round,'SURFACE-AGGREGATE.json'),'ROUND3_SURFACE_AGGREGATE');if(!records.equals(built.recordsBytes)||!aggregate.equals(built.aggregateBytes))throw Error('ROUND3_SURFACE_ARTIFACT_DRIFT');return {auditor_agent_id:ROUND3_SURFACE_CALL.auditor_agent_id,auditor_session_id:ROUND3_SURFACE_CALL.auditor_session_id,raw_response_sha256:ROUND3_SURFACE_CALL.response_sha256,calls_started:1,calls_remaining:0,surface_records_sha256:sha256(records),surface_aggregate_sha256:sha256(aggregate),counts:built.counts,context_eligible_ids:built.aggregate.pass_ids};}
if(import.meta.url===`file://${process.argv[1]}`){if(process.argv[2]==='--materialize')console.log(JSON.stringify(materializeRound3SurfaceArtifacts(),null,2));else if(process.argv[2]==='--check')console.log(JSON.stringify(validateRound3SurfaceArtifacts(),null,2));else throw Error('usage: --materialize|--check');}
