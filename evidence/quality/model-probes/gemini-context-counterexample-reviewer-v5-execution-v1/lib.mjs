import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
export const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
export const jsonBytes=x=>Buffer.from(`${JSON.stringify(x,null,2)}\n`);
export const byteCompare=(a,b)=>Buffer.compare(Buffer.from(String(a)),Buffer.from(String(b)));
export const shaFile=p=>sha256(fs.readFileSync(p));
export const safeRelative=p=>typeof p==='string'&&p!==''&&!path.isAbsolute(p)&&!p.includes('\0')&&path.posix.normalize(p)===p&&!p.startsWith('../');
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
export function countBy(items,key){return Object.fromEntries([...new Set(items.map(x=>x[key]))].sort().map(v=>[v,items.filter(x=>x[key]===v).length]))}
export const predecessor={
 gate:{path:'.ai/task/research-gemini-context-counterexample-reviewer-v5/ROUND-0003-TERMINALIZATION-REVIEW-GATE-001.json',sha256:'8495fd3bbe3211314607db67314360fd983d30f9455063b49d0e0a28a587d907'},
 active:{path:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/ACTIVE-FRAME.json',sha256:'e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3'},
 result:{path:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/rounds/ROUND-0003/RESULT.json',sha256:'44726a9f538cb5ec3e63c64be64437fb2f0014f496b80d312647e240b8b550bd'}
};
