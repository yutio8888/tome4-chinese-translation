import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const shaFile = file => sha256(fs.readFileSync(file));
export const gitBlobOid = bytes => crypto.createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex');
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
export const byteSort = (a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b));
export const exactKeys = (value, keys) => !!value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort(byteSort)) === JSON.stringify([...keys].sort(byteSort));
export function decodeUtf8(value, label='UTF8') { try { return new TextDecoder('utf-8', {fatal:true}).decode(Buffer.from(value)); } catch { throw Error(`${label}:INVALID_UTF8`); } }

export function parseNoDuplicate(text, label='JSON') {
  let i=0; const ws=()=>{while(/\s/u.test(text[i]??''))i++;};
  const str=()=>{if(text[i++]!=='"')throw Error(`${label}:STRING`);let raw='"';for(;;){if(i>=text.length)throw Error(`${label}:STRING_EOF`);const c=text[i++];raw+=c;if(c==='"')break;if(c==='\\'){if(i>=text.length)throw Error(`${label}:ESCAPE_EOF`);raw+=text[i++];}else if(c<' ')throw Error(`${label}:CONTROL`);}return JSON.parse(raw);};
  const val=()=>{ws();if(text[i]==='"'){str();return;}if(text[i]==='{'){obj();return;}if(text[i]==='['){arr();return;}const m=text.slice(i).match(/^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/u);if(!m)throw Error(`${label}:VALUE@${i}`);i+=m[0].length;};
  const obj=()=>{i++;ws();const keys=new Set();if(text[i]==='}'){i++;return;}for(;;){ws();const key=str();if(keys.has(key))throw Error(`${label}:DUPLICATE_KEY:${key}`);keys.add(key);ws();if(text[i++]!==':')throw Error(`${label}:COLON`);val();ws();const c=text[i++];if(c==='}')return;if(c!==',')throw Error(`${label}:OBJECT_SEPARATOR`);}};
  const arr=()=>{i++;ws();if(text[i]===']'){i++;return;}for(;;){val();ws();const c=text[i++];if(c===']')return;if(c!==',')throw Error(`${label}:ARRAY_SEPARATOR`);}};
  val();ws();if(i!==text.length)throw Error(`${label}:TRAILING`);return JSON.parse(text);
}
export function readCanonical(file){const b=fs.readFileSync(file),v=parseNoDuplicate(decodeUtf8(b,file),file);if(!b.equals(jsonBytes(v)))throw Error(`NONCANONICAL:${file}`);return v;}
export function walk(dir,base='',out=[]){if(!fs.existsSync(dir))return out;for(const e of fs.readdirSync(dir,{withFileTypes:true}).sort((a,b)=>byteSort(a.name,b.name))){const rel=path.posix.join(base,e.name),p=path.join(dir,e.name),s=fs.lstatSync(p);if(s.isSymbolicLink())throw Error(`SYMLINK:${rel}`);if(e.isDirectory())walk(p,rel,out);else if(e.isFile())out.push(rel);else throw Error(`NONREGULAR:${rel}`);}return out;}
export function treeBinding(repoRoot,rel){const dir=path.join(repoRoot,rel),files=walk(dir).map(p=>({path:p,sha256:shaFile(path.join(dir,p))})).sort((a,b)=>byteSort(a.path,b.path));return{root:rel,file_count:files.length,tree_sha256:sha256(Buffer.concat(files.map(x=>Buffer.from(`${x.path}\0${x.sha256}\n`))))};}
function gitDir(repoRoot){const dot=path.join(repoRoot,'.git'),s=fs.statSync(dot);if(s.isDirectory())return dot;const m=/^gitdir: (.+)\n?$/u.exec(fs.readFileSync(dot,'utf8'));if(!m)throw Error('GITDIR_FORMAT');return path.resolve(repoRoot,m[1]);}
export function readGitIndex(repoRoot){const b=fs.readFileSync(path.join(gitDir(repoRoot),'index'));if(b.subarray(0,4).toString()!=='DIRC')throw Error('GIT_INDEX_SIGNATURE');const version=b.readUInt32BE(4),count=b.readUInt32BE(8);if(![2,3].includes(version))throw Error(`GIT_INDEX_VERSION:${version}`);let at=12;const entries=new Map();for(let n=0;n<count;n++){const start=at;if(at+62>b.length)throw Error('GIT_INDEX_TRUNCATED');const oid=b.subarray(at+40,at+60).toString('hex'),flags=b.readUInt16BE(at+60),stage=(flags>>>12)&3;at+=62;if(version===3&&(flags&0x4000))at+=2;const end=b.indexOf(0,at);if(end<0)throw Error('GIT_INDEX_PATH');const name=decodeUtf8(b.subarray(at,end),'GIT_INDEX_PATH');at=end+1;while((at-start)%8)at++;if(stage===0)entries.set(name,oid);}return entries;}
export function trackedCleanErrors(repoRoot,paths){let index;try{index=readGitIndex(repoRoot);}catch(e){return[`GIT_INDEX:${e.message}`];}const errors=[];for(const rel of paths){const file=path.join(repoRoot,rel),oid=index.get(rel);if(!oid)errors.push(`EVIDENCE_UNTRACKED:${rel}`);else if(!fs.existsSync(file)||gitBlobOid(fs.readFileSync(file))!==oid)errors.push(`EVIDENCE_NOT_CLEAN:${rel}`);}return errors;}
export function writeExclusive(file,bytes){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,Buffer.isBuffer(bytes)?bytes:jsonBytes(bytes),{flag:'wx'});}
