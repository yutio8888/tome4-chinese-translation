#!/usr/bin/env node
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {replayRound3Terminal} from './round-0003-terminal-replay.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
export function publicTerminalReplay(root=here,repo=path.resolve(here,'..','..','..','..')){return replayRound3Terminal(root,repo);}
if(import.meta.url===`file://${process.argv[1]}`)console.log(JSON.stringify(publicTerminalReplay(),null,2));
