import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const TASK_ID='research-gemini-context-counterexample-reviewer-v4';
export const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
export const shaFile=p=>sha256(fs.readFileSync(p));
export const jsonBytes=x=>Buffer.from(`${JSON.stringify(x,null,2)}\n`);
export const byteCompare=(a,b)=>Buffer.compare(Buffer.from(String(a),'utf8'),Buffer.from(String(b),'utf8'));
export const byteSort=xs=>xs.sort(byteCompare);
export const unicodeFold=x=>String(x).normalize('NFKC').toLowerCase();
export const normalize=x=>String(x).normalize('NFKC').replace(/\\[nrt]|\s/gu,' ').replace(/ +/gu,' ').trim();
export const presentationTokens=x=>(unicodeFold(normalize(x)).match(/[\p{L}\p{N}]+/gu)??[]);
export function tokenContains(haystack,needle){
  const h=Array.isArray(haystack)?haystack:presentationTokens(haystack),n=Array.isArray(needle)?needle:presentationTokens(needle);
  if(!n.length||n.length>h.length)return false;
  outer:for(let i=0;i<=h.length-n.length;i++){for(let j=0;j<n.length;j++)if(h[i+j]!==n[j])continue outer;return true}return false;
}
export const preparePresentation=value=>{const raw=String(value),normalized=normalize(value);return{raw,normalized,tokens:presentationTokens(normalized)}};
export function presentationMatchKind(candidate,presentation){
  const c=typeof candidate==='object'&&candidate?.raw!==undefined?candidate:preparePresentation(candidate),p=typeof presentation==='object'&&presentation?.raw!==undefined?presentation:preparePresentation(presentation);if(!c.raw||!p.raw)return null;
  if(c.raw===p.raw)return'RAW_EQUALITY';
  if(!c.normalized||!p.normalized)return null;
  if(c.normalized===p.normalized)return'NORMALIZED_EQUALITY';
  if(p.normalized.includes(c.normalized))return'NORMALIZED_CONTAINMENT';
  if(tokenContains(p.tokens,c.tokens))return'TOKEN_PRESENTATION';
  return null;
}
export const presentationMatch=(candidate,presentation)=>presentationMatchKind(candidate,presentation)!==null;
export function atomSpanCredit(reported,accepted){const r=normalize(reported),a=normalize(accepted);if(!r||!a)return false;if(r===a)return true;return[...r].length>=2&&[...a].length>=2&&(r.includes(a)||a.includes(r))}
export function readJson(p){return JSON.parse(fs.readFileSync(p,'utf8'))}
export function exactKeys(v,keys){return v&&typeof v==='object'&&!Array.isArray(v)&&JSON.stringify(byteSort(Object.keys(v)))===JSON.stringify(byteSort([...keys]))}
export function safeRelative(p){return typeof p==='string'&&p.length>0&&!p.includes('\0')&&!path.isAbsolute(p)&&path.posix.normalize(p)===p&&!p.startsWith('../')}
function signalKey(key){
  const canonical=String(key).replace(/([a-z\d])([A-Z])/gu,'$1_$2').replace(/[^a-z\d]+/giu,'_').toLowerCase(),compact=canonical.replace(/_/gu,'');
  return /(?:^|_)(?:tool|tools|tool_call|tool_calls|function_call|function_calls|command|commands|web|browser|mcp|subagent)(?:_|$)/u.test(canonical)||/^(?:tool|tools|toolcall|toolcalls|functioncall|functioncalls|command|commands|web|websearch|browser|mcp|mcpevent|subagent)$/u.test(compact);
}
export function toolSignal(v,key=''){
  if(signalKey(key))return true; // A signal key is forbidden even when its value is scalar, null, or empty.
  if(v&&typeof v==='object'&&!Array.isArray(v)&&typeof v.type==='string'&&/(?:tool|function|command|web|browser|mcp|subagent)[_ -]?(?:use|call|result|event)?/iu.test(v.type))return true;
  if(Array.isArray(v))return v.some(x=>toolSignal(x));
  if(v&&typeof v==='object')return Object.entries(v).some(([k,x])=>toolSignal(x,k));
  return false;
}
export function validateReviewerResponse(v,expectedIds){
  const e=[];
  if(!exactKeys(v,['items'])||!Array.isArray(v?.items))return['response schema: top level must contain only items array'];
  if(v.items.length!==expectedIds.length)e.push(`response schema: item count ${v.items.length}/${expectedIds.length}`);
  const claim=new Set(['SUBJECT','REFERENT','EVENT','CONDITION','SCOPE','DIRECTION','POLARITY','OWNERSHIP','ACTION','STATE','TIMING','OMISSION','ADDITION','FORMAT','OTHER']);
  v.items.forEach((x,i)=>{if(!exactKeys(x,['item_id','candidates']))e.push(`item ${i}: keys`);if(x?.item_id!==expectedIds[i])e.push(`item ${i}: id/order`);if(!Array.isArray(x?.candidates)||x.candidates.length>4)e.push(`item ${i}: candidates`);for(const[j,c]of(x?.candidates??[]).entries()){if(!exactKeys(c,['verdict','claim_type','target_span','correction','evidence']))e.push(`item ${i} candidate ${j}: keys`);if(!['FINDING','UNCERTAIN'].includes(c?.verdict)||!claim.has(c?.claim_type))e.push(`item ${i} candidate ${j}: enum`);for(const k of['target_span','correction','evidence'])if(typeof c?.[k]!=='string'||c[k].length<1||c[k].length>500)e.push(`item ${i} candidate ${j}: ${k}`)}});return e;
}
export function validateAuthorization(auth,{phase,candidateRoot,manifestHash,releaseHash,expectedReviewRef,expectedPath,authPath}){
  const e=[],keys=['schema_version','task_id','execution_authorized','phase','candidate_root_sha256','hash_manifest_sha256','release_state_sha256','normal_review','senior_review','review_candidate_ref','issued_at_utc'];
  if(expectedPath&&path.resolve(expectedPath)!==path.resolve(authPath??''))e.push('authorization path is not the task-owned canonical path');
  if(!exactKeys(auth,keys))e.push('authorization schema');
  if(auth.schema_version!=='gemini-context-execution-authorization-v1'||auth.task_id!==TASK_ID||auth.execution_authorized!==true)e.push('authorization identity');
  if(auth.phase!==phase||auth.candidate_root_sha256!==candidateRoot||auth.hash_manifest_sha256!==manifestHash||auth.release_state_sha256!==releaseHash)e.push('authorization binding');
  if(auth.normal_review!=='PASS'||auth.senior_review!=='PASS'||typeof auth.review_candidate_ref!=='string'||!/^[0-9a-f]{64}$/.test(auth.review_candidate_ref)||auth.review_candidate_ref!==expectedReviewRef)e.push('authorization reviews');
  if(typeof auth.issued_at_utc!=='string'||!/^\d{4}-\d\d-\d\dT/u.test(auth.issued_at_utc))e.push('authorization timestamp');return e;
}
export function qualificationExpected(response,expected){return JSON.stringify(response?.items?.map(x=>x.item_id))===JSON.stringify(expected?.ordered_ids)&&(!expected?.first_has_candidate||(response?.items?.[0]?.candidates?.length??0)>0)}
export function manifestRoot(files){return sha256(Object.entries(files).sort(([a],[b])=>byteCompare(a,b)).map(([n,h])=>`${n}\0${h}\n`).join(''))}
export function packagePath(metaUrl,...parts){return path.join(path.dirname(new URL(metaUrl).pathname),...parts)}
export const DYNAMIC_ARTIFACT_CLASSES=Object.freeze(['HASH-DAG.json','RELEASE-STATE.json','AUDIT-RELEASE-STATE.json','EXECUTION-CLI-*.json','REQUEST-*.txt','REQUEST-MAP-*.json','REQUEST-MANIFEST-*.json','RAW-*.json','RAW-*.stderr.txt','RAW-MANIFEST-*.json','CANDIDATE-*.json','SCORE-*.json','RESULT-*.json','QUALIFICATION-*.json','QUALIFICATION-*.txt','POST-RUN-*.json','SELECTION-*.json','SEALED-REFERENCE-*.json']);
export const executionArtifact=name=>path.posix.dirname(name)==='.'&&/^(?:EXECUTION-CLI-|REQUEST-|REQUEST-MAP-|REQUEST-MANIFEST-|RAW-|RAW-MANIFEST-|CANDIDATE-|RESULT-|SCORE-|QUALIFICATION-|POST-RUN-|SELECTION-|SEALED-REFERENCE-)/u.test(path.posix.basename(name));
export const dynamicArtifact=name=>['HASH-DAG.json','RELEASE-STATE.json','AUDIT-RELEASE-STATE.json'].includes(name)||executionArtifact(name);
export function walkFiles(dir,base='',out=[]){for(const x of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>byteCompare(a.name,b.name))){const rel=path.posix.join(base,x.name),p=path.join(dir,x.name);if(x.isDirectory())walkFiles(p,rel,out);else out.push(rel)}return out}
const ROOT_FROZEN=new Set(['SURFACE-AUDIT-QUEUE.json','CONTEXT-AUDIT-QUEUE.json','RELEASE-STATE.json','AUDIT-RELEASE-STATE.json']);
const SCHEMA_FILES=new Set(['AUTHORIZATION-SCHEMA.json','CLEAN-AUDIT-SCHEMA.json','MANIPULATION-CHECK-SCHEMA.json','MUTATION-AUTHOR-SCHEMA.json','REVIEWER-SCHEMA.json','SEALED-REFERENCE-SCHEMA.json']);
export const frozenAllowedArtifact=name=>path.posix.dirname(name)==='.'&&ROOT_FROZEN.has(name);
export function downstreamArtifactPath(name){
  const p=path.posix.normalize(name), parts=p.split('/');
  if(frozenAllowedArtifact(p))return false;
  if(p==='schemas'||(parts.length===2&&parts[0]==='schemas'&&SCHEMA_FILES.has(parts[1])))return false;
  return parts.some(part=>/^(?:AUDIT(?:-|\.)|SURFACE-AUDIT-|CONTEXT-AUDIT-|CLEAN-ADJUDICATION(?:\.json)?$|MUTATIONS|MANIPULATION|SAMPLE-|SEALED-REFERENCE-|REQUEST-|QUALIFICATION-|RAW-|SCORE-|RESULT(?:-|\.)|CANDIDATE-|SELECTION-|EXECUTION-CLI-|POST-RUN-)/u.test(part))
    || (parts[0]==='schemas');
}
