#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {byteSort, jsonBytes, readCanonical, sha256, shaFile, walk} from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export const MANIFEST = 'MANIFEST.json';
export const DYNAMIC = ['RESULT.json', 'execution/'];
export const isDynamic = rel => DYNAMIC.some(x => x.endsWith('/') ? rel.startsWith(x) : rel === x);
export const sourcePaths = (root = here) => walk(root).filter(x => x !== MANIFEST && !isDynamic(x)).sort(byteSort);
export function buildManifest(root = here) {
  const files = sourcePaths(root).map(file => ({path: file, sha256: shaFile(path.join(root, file))}));
  return {schema_version: 'gemini-original-a-repeat-static-manifest-v1', experiment_id: 'gemini-evaluator-original-a-repeat-v1', self_excluded: MANIFEST, dynamic_artifacts_excluded: DYNAMIC, file_count: files.length, files};
}
export function checkManifest(root = here) {
  const file = path.join(root, MANIFEST);
  if (!fs.existsSync(file)) return ['MANIFEST_MISSING'];
  try { readCanonical(file); } catch (error) { return [error.message]; }
  return fs.readFileSync(file).equals(jsonBytes(buildManifest(root))) ? [] : ['MANIFEST_REBUILD_NOT_BYTE_IDENTICAL'];
}
export function writeManifest(root = here) {
  const bytes = jsonBytes(buildManifest(root)); fs.writeFileSync(path.join(root, MANIFEST), bytes);
  return {file_count: buildManifest(root).file_count, manifest_sha256: sha256(bytes)};
}
if (import.meta.url === `file://${process.argv[1]}`) {
  if (process.argv[2] === '--check') { const errors = checkManifest(); console.log(JSON.stringify({mode: 'CHECK', manifest_sha256: fs.existsSync(path.join(here, MANIFEST)) ? shaFile(path.join(here, MANIFEST)) : null, errors}, null, 2)); process.exitCode = errors.length ? 3 : 0; }
  else if (process.argv.length === 2) console.log(JSON.stringify(writeManifest(), null, 2));
  else { console.error('usage: node build-manifest.mjs [--check]'); process.exitCode = 2; }
}
