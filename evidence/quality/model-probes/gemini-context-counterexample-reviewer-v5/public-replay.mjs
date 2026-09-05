#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {checkReplay} from './replay.mjs';
import {replayRound3} from './round-0003-replay.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export function publicReplay(root = here) {
  if (fs.existsSync(path.join(root, 'rounds', 'ROUND-0003'))) return {status:'PASS', public_phase:'ROUND_0003_SURFACE_INPUT', ...replayRound3(root)};
  return checkReplay(root);
}

if (import.meta.url === `file://${process.argv[1]}`) console.log(JSON.stringify(publicReplay(), null, 2));
