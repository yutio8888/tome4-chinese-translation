#!/usr/bin/env node
// Production entry point. The ONLY accepted argv is:  --cell <id>
//
// There is deliberately no package-root, repository-root, state, invoke, force or
// authorize parameter: the package root is this file's directory, the repository root is
// fixed relative to it, and authorization is read from the task-owned receipt at the fixed path
// .ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v3/EXECUTION-AUTHORIZATION.json.
// Nothing a caller types can widen what may run (C11).
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {runCell} from './runner.mjs';
import {gatePaths} from './gates.mjs';
export const USAGE='usage: node run.mjs --cell <id>';
export const AUTHORIZATION_PATH=gatePaths.EXECUTION_AUTHORIZATION;
// Exactly two tokens, exactly in this order, cell id non-empty and free of separators.
export function parseArgv(argv){
  if(!Array.isArray(argv)||argv.length!==2)return{ok:false,error:'ARGV_CONTRACT_EXPECTS_EXACTLY_TWO_TOKENS'};
  if(argv[0]!=='--cell')return{ok:false,error:'ARGV_CONTRACT_ONLY_FLAG_IS_CELL'};
  const cell=argv[1];
  if(typeof cell!=='string'||!/^[a-z]+-[A-D]-run-[12]-shard-[12]$/u.test(cell))return{ok:false,error:'ARGV_CONTRACT_CELL_ID'};
  return{ok:true,cell};
}
if(import.meta.url===`file://${process.argv[1]}`){
  const parsed=parseArgv(process.argv.slice(2));
  if(!parsed.ok){console.error(`${parsed.error}\n${USAGE}`);process.exit(2)}
  const root=path.dirname(fileURLToPath(import.meta.url));
  try{console.log(JSON.stringify(runCell(parsed.cell,{root}),null,2))}
  catch(e){console.error(e.message);process.exit(3)}
}
