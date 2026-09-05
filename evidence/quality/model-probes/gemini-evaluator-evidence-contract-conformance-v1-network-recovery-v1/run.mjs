#!/usr/bin/env node
import path from'node:path';import{fileURLToPath}from'node:url';import{runCell}from'./runner.mjs';import{CELL}from'./freezer.mjs';
export function parseArgv(a){return a.length===2&&a[0]==='--cell'&&a[1]===CELL?{ok:true,cell:a[1]}:{ok:false}}
if(import.meta.url===`file://${process.argv[1]}`){const a=parseArgv(process.argv.slice(2));if(!a.ok){console.error(`usage: node run.mjs --cell ${CELL}`);process.exit(2)}const root=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(root,'../../../..');try{const r=runCell(root,repo,a.cell);console.log(JSON.stringify(r,null,2));process.exitCode=r.process_success&&r.envelope_schema_valid?0:4}catch(e){console.error(e.message);process.exitCode=3}}
