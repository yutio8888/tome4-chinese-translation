#!/usr/bin/env node
import path from'node:path';import{fileURLToPath}from'node:url';import{runCell}from'./runner.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(root,'../../../..'),cell=process.argv[2];if(!cell){console.error('usage: node run.mjs <registered-cell>');process.exit(2);}try{const r=runCell(root,repo,cell);console.log(JSON.stringify(r,null,2));process.exitCode=r.continue_authorized?0:3;}catch(e){console.error(e.message);process.exitCode=3;}
