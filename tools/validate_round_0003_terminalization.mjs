#!/usr/bin/env node
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';

const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const modulePath=path.join(repo,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/round-0003-terminal-replay.mjs');
const {replayRound3Terminal}=await import(pathToFileURL(modulePath));
console.log(JSON.stringify(replayRound3Terminal(undefined,repo),null,2));
