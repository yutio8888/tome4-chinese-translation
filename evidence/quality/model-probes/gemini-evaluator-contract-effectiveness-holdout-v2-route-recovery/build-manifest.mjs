#!/usr/bin/env node
import fs from'node:fs';import path from'node:path';import{fileURLToPath}from'node:url';import{byteSort,jsonBytes,sha256,shaFile,walk}from'./lib.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
export function staticPaths(root=here){return walk(root).filter(p=>!['MANIFEST.json','PREFLIGHT.json','RESULT.json'].includes(p)&&!p.startsWith('execution/')).sort(byteSort);}
export function buildManifest(root=here){const files=staticPaths(root).map(p=>({path:p,sha256:shaFile(path.join(root,p)),utf8_bytes:fs.statSync(path.join(root,p)).size}));return{schema_version:'gemini-evaluator-contract-effectiveness-manifest-v2',file_count:files.length,files,static_tree_sha256:sha256(Buffer.concat(files.map(x=>Buffer.from(`${x.path}\0${x.sha256}\n`))))};}
export function checkManifest(root=here){const p=path.join(root,'MANIFEST.json');if(!fs.existsSync(p))return['MISSING:MANIFEST.json'];const expected=jsonBytes(buildManifest(root));return fs.readFileSync(p).equals(expected)?[]:['MANIFEST_DRIFT'];}
if(import.meta.url===`file://${process.argv[1]}`){const p=path.join(here,'MANIFEST.json'),b=jsonBytes(buildManifest());if(process.argv.includes('--check')){const e=checkManifest();console.log(JSON.stringify({errors:e},null,2));process.exitCode=e.length?3:0;}else{fs.writeFileSync(p,b);console.log(JSON.stringify({path:'MANIFEST.json',sha256:sha256(b)},null,2));}}
