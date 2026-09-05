#!/usr/bin/env node
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {CELLS} from './freezer.mjs';
import {runCell} from './runner.mjs';

export function parseArgv(args) { return args.length === 2 && args[0] === '--cell' && CELLS.includes(args[1]) ? {ok: true, cell: args[1]} : {ok: false}; }
if (import.meta.url === `file://${process.argv[1]}`) {
  const parsed = parseArgv(process.argv.slice(2));
  if (!parsed.ok) { console.error(`usage: node run.mjs --cell <${CELLS.join('|')}>`); process.exit(2); }
  const root = path.dirname(fileURLToPath(import.meta.url)), repo = path.resolve(root, '../../../..');
  try { const result = runCell(root, repo, parsed.cell); console.log(JSON.stringify(result, null, 2)); process.exitCode = result.process_success && result.envelope_schema_valid ? 0 : 4; }
  catch (error) { console.error(error.message); process.exitCode = 3; }
}
