#!/usr/bin/env node
// The single package identity artifact.
//
// MANIFEST.json = { path, lowercase sha256 } for every source file in this package,
// in bytewise path order, with MANIFEST.json itself excluded (self-exclusion is what
// makes rebuilding it from the tree byte-identical -- there is no hash-of-hashes DAG,
// no CANDIDATE-IDENTITY, and no separate candidate root).
//
// Files produced by a later phase (requests, frozen samples, sealed reference,
// qualification captures, execution journals, scores) are NOT package source and are
// listed under generated_prefixes; the checker ignores exactly those paths.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {sha256,shaFile,jsonBytes,walk,byteCompare,readCanonical,hex64,exactKeys} from './lib.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
export const MANIFEST_PATH='MANIFEST.json';
export const EXPERIMENT_ID='gemini-context-counterexample-reviewer-v5-execution-v5';
export const TASK_ID='research-gemini-context-counterexample-reviewer-v5-execution-v5';
export const SCHEMA='gemini-context-v5-execution-manifest-v1';
export const RECIPE='per file: { path, lowercase sha256 }; array sorted bytewise by path; MANIFEST.json self-excluded; generated_prefixes excluded';
// Every qualification artifact is dynamic in execution-v5. Fresh qualification begins with
// no ledger, capture, request, draft, evidence, or inherited provenance contract.
export const GENERATED_PREFIXES=['SCORES.json','PILOT-RESULT.json','PILOT.md','execution/','frozen/REQUEST-MANIFEST.json','frozen/SAMPLES.json','model-facing/requests/','qualification/','sealed/REFERENCE.json'].sort(byteCompare);
export const MANIFEST_KEYS=['experiment_id','file_count','files','generated_prefixes','recipe','schema_version','self_excluded','task_id'];
export const isGenerated=rel=>GENERATED_PREFIXES.some(p=>p.endsWith('/')?rel.startsWith(p):rel===p);
export function sourcePaths(root=here){return walk(root).filter(x=>x!==MANIFEST_PATH&&!isGenerated(x)).sort(byteCompare)}
export function buildManifest(root=here){
  const files=sourcePaths(root).map(p=>({path:p,sha256:shaFile(path.join(root,p))}));
  return{schema_version:SCHEMA,experiment_id:EXPERIMENT_ID,task_id:TASK_ID,recipe:RECIPE,self_excluded:MANIFEST_PATH,generated_prefixes:GENERATED_PREFIXES,file_count:files.length,files};
}
// C02: rebuilding the manifest from the tree must be byte-identical to the checked-in file.
export function checkManifest(root=here){
  const errors=[],p=path.join(root,MANIFEST_PATH);
  if(!fs.existsSync(p))return['MANIFEST_ABSENT'];
  let onDisk;try{onDisk=readCanonical(p)}catch(e){return[`MANIFEST_PARSE:${e.message}`]}
  if(!exactKeys(onDisk,MANIFEST_KEYS)||onDisk.schema_version!==SCHEMA||onDisk.experiment_id!==EXPERIMENT_ID||onDisk.task_id!==TASK_ID||onDisk.recipe!==RECIPE||onDisk.self_excluded!==MANIFEST_PATH||JSON.stringify(onDisk.generated_prefixes)!==JSON.stringify(GENERATED_PREFIXES))errors.push('MANIFEST_SCHEMA');
  if(!Array.isArray(onDisk.files)||onDisk.file_count!==onDisk.files?.length||!onDisk.files?.every(x=>exactKeys(x,['path','sha256'])&&hex64(x.sha256)))errors.push('MANIFEST_FILE_ROWS');
  else{
    const listed=onDisk.files.map(x=>x.path);
    if(JSON.stringify(listed)!==JSON.stringify([...listed].sort(byteCompare)))errors.push('MANIFEST_ORDER');
    const actual=new Set(sourcePaths(root));
    for(const x of onDisk.files){if(!actual.has(x.path))errors.push(`MANIFEST_LISTS_MISSING_FILE:${x.path}`);else if(shaFile(path.join(root,x.path))!==x.sha256)errors.push(`MANIFEST_HASH_DRIFT:${x.path}`)}
    for(const a of actual)if(!listed.includes(a))errors.push(`UNLISTED_FILE:${a}`);
  }
  let rebuilt;try{rebuilt=jsonBytes(buildManifest(root))}catch(e){return[...errors,`REBUILD:${e.message}`]}
  if(!fs.readFileSync(p).equals(rebuilt))errors.push('MANIFEST_REBUILD_NOT_BYTE_IDENTICAL');
  return errors;
}
export const manifestSha256=(root=here)=>shaFile(path.join(root,MANIFEST_PATH));
export function writeManifest(root=here){const b=jsonBytes(buildManifest(root));fs.writeFileSync(path.join(root,MANIFEST_PATH),b);return{file_count:buildManifest(root).file_count,manifest_sha256:sha256(b)}}
if(import.meta.url===`file://${process.argv[1]}`){
  const rest=process.argv.slice(2);
  if(rest.length===1&&rest[0]==='--check'){const errors=checkManifest();console.log(JSON.stringify({mode:'CHECK',manifest_sha256:fs.existsSync(path.join(here,MANIFEST_PATH))?manifestSha256():null,errors},null,2));process.exitCode=errors.length?3:0}
  else if(rest.length===0){console.log(JSON.stringify({mode:'WRITE',...writeManifest()},null,2))}
  else{console.error('usage: node build-manifest.mjs [--check]');process.exitCode=2}
}
