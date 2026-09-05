import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
export const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
export const jsonBytes=x=>Buffer.from(`${JSON.stringify(x,null,2)}\n`);
export const byteCompare=(a,b)=>Buffer.compare(Buffer.from(String(a)),Buffer.from(String(b)));
export const shaFile=p=>sha256(fs.readFileSync(p));
export const hex64=x=>/^[0-9a-f]{64}$/u.test(x??'');
export const exactKeys=(x,keys)=>!!x&&typeof x==='object'&&!Array.isArray(x)&&JSON.stringify(Object.keys(x).sort(byteCompare))===JSON.stringify([...keys].sort(byteCompare));
export function walk(dir,base='',out=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>byteCompare(a.name,b.name))){const rel=path.posix.join(base,e.name),p=path.join(dir,e.name),s=fs.lstatSync(p);if(s.isSymbolicLink())throw Error(`SYMLINK:${rel}`);if(e.isDirectory())walk(p,rel,out);else if(e.isFile())out.push(rel);else throw Error(`NONREGULAR:${rel}`)}return out}
export function parseNoDuplicate(text,label='JSON'){
 let i=0;const ws=()=>{while(/\s/u.test(text[i]??''))i++};
 const str=()=>{if(text[i++]!=='"')throw Error(`${label}:STRING`);let raw='"';for(;;){if(i>=text.length)throw Error(`${label}:STRING_EOF`);const c=text[i++];raw+=c;if(c==='"')break;if(c==='\\'){if(i>=text.length)throw Error(`${label}:ESCAPE_EOF`);raw+=text[i++]}else if(c<' ')throw Error(`${label}:CONTROL`)}return JSON.parse(raw)};
 const value=()=>{ws();if(text[i]==='"'){str();return}if(text[i]==='{'){object();return}if(text[i]==='['){array();return}const m=text.slice(i).match(/^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/u);if(!m)throw Error(`${label}:VALUE@${i}`);i+=m[0].length};
 const object=()=>{i++;ws();const keys=new Set();if(text[i]==='}'){i++;return}for(;;){ws();const k=str();if(keys.has(k))throw Error(`${label}:DUPLICATE_KEY:${k}`);keys.add(k);ws();if(text[i++]!==':')throw Error(`${label}:COLON`);value();ws();const c=text[i++];if(c==='}')return;if(c!==',')throw Error(`${label}:OBJECT_SEPARATOR`)}};
 const array=()=>{i++;ws();if(text[i]===']'){i++;return}for(;;){value();ws();const c=text[i++];if(c===']')return;if(c!==',')throw Error(`${label}:ARRAY_SEPARATOR`)}};
 value();ws();if(i!==text.length)throw Error(`${label}:TRAILING`);return JSON.parse(text)
}
export function readJsonSafe(p){return parseNoDuplicate(fs.readFileSync(p,'utf8'),p)}
export function readCanonical(p){const b=fs.readFileSync(p),v=parseNoDuplicate(b.toString('utf8'),p);if(!b.equals(jsonBytes(v)))throw Error(`NONCANONICAL:${p}`);return v}
export function writeExclusive(p,value){fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,Buffer.isBuffer(value)?value:jsonBytes(value),{flag:'wx'})}
// Write-once-then-verify. Unlike writeExclusive this is safe to re-run: identical bytes are
// a no-op, different bytes are a drift error. Used for deterministic artifacts that a retry
// legitimately reproduces (the synthetic request, the qualification draft/evidence).
export function writeStable(p,value){const b=Buffer.isBuffer(value)?value:jsonBytes(value);if(fs.existsSync(p)){if(!fs.readFileSync(p).equals(b))throw Error(`STABLE_WRITE_DRIFT:${p}`);return b}fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,b,{flag:'wx'});return b}
export function countBy(items,key){return Object.fromEntries([...new Set(items.map(x=>x[key]))].sort().map(v=>[v,items.filter(x=>x[key]===v).length]))}
// Byte-immutable predecessor documents (V5 terminalization frame).
export const predecessor={
 gate:{path:'.ai/task/research-gemini-context-counterexample-reviewer-v5/ROUND-0003-TERMINALIZATION-REVIEW-GATE-001.json',sha256:'8495fd3bbe3211314607db67314360fd983d30f9455063b49d0e0a28a587d907'},
 active:{path:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/ACTIVE-FRAME.json',sha256:'e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3'},
 result:{path:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0003/RESULT.json',sha256:'44726a9f538cb5ec3e63c64be64437fb2f0014f496b80d312647e240b8b550bd'}
};
// Byte-immutable predecessor trees. This package must never write into them.
export const predecessorTreeRoots=[
 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5',
 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v1',
 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v2'
];
// The immediate execution-v3 predecessor is bound separately because its complete tree is
// immutable input to this fresh retry, not one of the terminal-frame source trees.
export const predecessorExecutionV3={
 root:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v3',
 file_count:74,
 tree_sha256:'83201688dfa55420330766ef8b1c75954058cd4103ed10f4fee418979d5867c6'
};
export const originalAgyBinary={
 path:'/home/yun/.local/bin/agy',
 qualified_sha256:'d492241f19f90ea06cb9f85f7788c371dbce3386206d734ddc2c7ec84fa3ddca',
 rejected_upgraded_sha256:'f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e'
};
export const agyBinary={
 path:'/home/yun/.local/bin/agy.1788410029995956792.old',
 sha256:originalAgyBinary.qualified_sha256
};
export const routeRelocation={
 path:'ROUTE-RELOCATION-CONTRACT.json',
 original_route_sha256:'742529e3c3d1d76bbc324e66cbdae48b3286cc37d3bea8f8e4260cea4ccac8b7',
 relocated_route_sha256:'f82ac7fd532e47d670be4839dc5d7301ceee143c5d50861445088e7fe79f3a4d'
};
const routeRelocationKeys=['identity_rule','original_executable','original_route','rejected_upgraded_executable','relocated_executable','relocated_route','schema_version','status'];
const pathShaKeys=['path','sha256'];
// The relocation is deliberately narrow: historical captures keep their original route/path,
// while future spawns use only a second path containing exactly the same qualified bytes.
export function validateRouteRelocation(root,route=null){
  const errors=[];let c,r;
  try{c=readCanonical(path.join(root,routeRelocation.path))}catch(e){return{valid:false,errors:[`READ:${e.message}`],contract:null}}
  try{r=route??readCanonical(path.join(root,'ROUTE-CONTRACT.json'))}catch(e){errors.push(`ROUTE:${e.message}`)}
  if(!exactKeys(c,routeRelocationKeys)||c.schema_version!=='gemini-context-v5-execution-route-relocation-v1'||c.status!=='SAME_BYTE_RELOCATION_ONLY')errors.push('SCHEMA');
  for(const k of ['original_executable','original_route','rejected_upgraded_executable','relocated_executable','relocated_route'])if(!exactKeys(c?.[k],pathShaKeys))errors.push(`SHAPE:${k}`);
  if(c.original_route?.path!=='ROUTE-CONTRACT.json'||c.original_route?.sha256!==routeRelocation.original_route_sha256)errors.push('ORIGINAL_ROUTE');
  if(c.relocated_route?.path!=='ROUTE-CONTRACT.json'||c.relocated_route?.sha256!==routeRelocation.relocated_route_sha256)errors.push('RELOCATED_ROUTE');
  if(c.original_executable?.path!==originalAgyBinary.path||c.original_executable?.sha256!==originalAgyBinary.qualified_sha256)errors.push('ORIGINAL_EXECUTABLE');
  if(c.relocated_executable?.path!==agyBinary.path||c.relocated_executable?.sha256!==agyBinary.sha256||c.relocated_executable?.sha256!==c.original_executable?.sha256)errors.push('RELOCATED_EXECUTABLE');
  if(c.rejected_upgraded_executable?.path!==originalAgyBinary.path||c.rejected_upgraded_executable?.sha256!==originalAgyBinary.rejected_upgraded_sha256||c.rejected_upgraded_executable?.sha256===c.relocated_executable?.sha256)errors.push('REJECTED_UPGRADE');
  try{if(shaFile(path.join(root,'ROUTE-CONTRACT.json'))!==c.relocated_route?.sha256)errors.push('CURRENT_ROUTE_HASH')}catch{errors.push('CURRENT_ROUTE_HASH')}
  if(r&&(r.schema_version!=='gemini-context-v5-execution-route-v5'||r.cli_contract?.executable!==c.relocated_executable?.path||r.cli_contract?.executable_sha256!==c.relocated_executable?.sha256))errors.push('CURRENT_ROUTE_BINDING');
  return{valid:errors.length===0,errors,contract:c};
}
// The qualification and A/C runner share this frozen binding. It is deliberately called at the
// last possible point before a journal START row; a route or binary drift therefore cannot spend
// a process or leave a misleading START row behind.
export function verifyAgyExecutable(route,root=path.dirname(fileURLToPath(import.meta.url))){
  const relocation=validateRouteRelocation(root,route);
  const configured=route?.cli_contract;
  if(!relocation.valid||!configured||typeof configured.executable!=='string')throw Error('STOP_ROUTE_EXECUTABLE');
  let actual;try{actual=shaFile(configured.executable)}catch{throw Error('STOP_ROUTE_EXECUTABLE')}
  if(configured.executable!==agyBinary.path||configured.executable_sha256!==agyBinary.sha256||actual!==configured.executable_sha256)throw Error('STOP_ROUTE_EXECUTABLE');
  return{path:configured.executable,sha256:actual};
}
// tree_sha256 = sha256( concat over bytewise-sorted paths of  path NUL lowercase-file-sha256 LF ).
export function treeBinding(repoRoot,rel){const dir=path.join(repoRoot,rel),files=walk(dir).map(p=>({path:p,sha256:shaFile(path.join(dir,p))})).sort((a,b)=>byteCompare(a.path,b.path));return{root:rel,file_count:files.length,tree_sha256:sha256(Buffer.concat(files.map(x=>Buffer.from(`${x.path}\0${x.sha256}\n`))))}}
