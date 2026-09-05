#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {runPreflight} from './preflight.mjs';
import {runRound3Preflight} from './round-0003-preflight.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export function publicPreflight(root = here) {
  if (fs.existsSync(path.join(root, 'rounds', 'ROUND-0003'))) return runRound3Preflight(root);
  return runPreflight(root);
}

if (import.meta.url === `file://${process.argv[1]}`) { const result = publicPreflight(); console.log(JSON.stringify(result, null, 2)); process.exitCode = result.decision?.startsWith('GO_') ? 0 : 3; }
