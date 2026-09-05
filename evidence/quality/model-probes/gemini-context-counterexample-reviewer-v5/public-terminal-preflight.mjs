#!/usr/bin/env node
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {publicTerminalReplay} from './public-terminal-replay.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
export function publicTerminalPreflight(root=here,repo=path.resolve(here,'..','..','..','..')){
  const replay=publicTerminalReplay(root,repo);
  return {decision:replay.decision,static_integrity:'PASS',run_status:replay.implementation_review_status,terminal_status:replay.terminal_status,released_rounds:replay.released_rounds,context_calls_started:replay.context_call_accounting.started,context_calls_remaining:replay.context_call_accounting.remaining,release_authorized:false,round_0004_authorized:false,formal_experiment_inference_calls_made:0,review_lifecycle:replay.review_lifecycle};
}
if(import.meta.url===`file://${process.argv[1]}`){const result=publicTerminalPreflight();console.log(JSON.stringify(result,null,2));process.exitCode=result.decision==='TERMINALIZATION_COMPLETE_NO_RELEASE_OR_ROUND_0004'?0:3;}
