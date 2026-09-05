#!/usr/bin/env node
import {replayRound3Context} from './round-0003-context-replay.mjs';
export function publicContextReplay(root){return replayRound3Context(root);}
if(import.meta.url===`file://${process.argv[1]}`)console.log(JSON.stringify(publicContextReplay(),null,2));
