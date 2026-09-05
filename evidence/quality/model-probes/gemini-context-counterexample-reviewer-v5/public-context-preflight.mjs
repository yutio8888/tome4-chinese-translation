#!/usr/bin/env node
import {runRound3ContextPreflight} from './round-0003-context-preflight.mjs';
export function publicContextPreflight(root){return runRound3ContextPreflight(root);}
if(import.meta.url===`file://${process.argv[1]}`){const result=publicContextPreflight();console.log(JSON.stringify(result,null,2));process.exitCode=result.decision==='NO_GO_ROUND_0003_CONTEXT_INPUT_REVIEW_REQUIRED'?3:4;}
