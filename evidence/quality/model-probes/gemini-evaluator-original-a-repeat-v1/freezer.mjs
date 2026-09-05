#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {jsonBytes, readCanonical, sha256, writeExclusive} from './lib.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
export const CELLS = ['original-a-repeat-1', 'original-a-repeat-2', 'original-a-repeat-3'];
export const REQUEST = 'model-facing/requests/original-a.txt';
export const SCHEMA = 'model-facing/schemas/REVIEWER-SCHEMA.json';
export const REQUEST_SHA256 = '364900148df5fd7649f9c932a00e2b896c5f503d03f6a2545e3c0116591c04f9';
export const REQUEST_BYTES = 7049;
export const PROMPT_SHA256 = 'c2eee0bdd41aaaf2f74ef624e9e73198da431319344997d42e9066e8d948b920';
export const SCHEMA_SHA256 = 'd9485a07b55238c783989650ad9ec9e886f279c1779ae5697985a3dd860ce0d4';

export function splitRequest(bytes) {
  const text = Buffer.from(bytes).toString('utf8');
  const inputMarker = '\n\nINPUT JSON:\n', schemaMarker = '\n\nOUTPUT SCHEMA:\n';
  const a = text.indexOf(inputMarker), b = text.indexOf(schemaMarker);
  if (a < 0 || b < a) throw Error('REQUEST_FORMAT');
  return {
    promptBytes: Buffer.from(text.slice(0, a + 1)),
    input: JSON.parse(text.slice(a + inputMarker.length, b)),
    embeddedSchema: JSON.parse(text.slice(b + schemaMarker.length))
  };
}

export function build(root = here) {
  const request = fs.readFileSync(path.join(root, REQUEST)), schema = fs.readFileSync(path.join(root, SCHEMA));
  if (request.length !== REQUEST_BYTES || sha256(request) !== REQUEST_SHA256) throw Error('REQUEST_DRIFT');
  if (sha256(schema) !== SCHEMA_SHA256) throw Error('SCHEMA_DRIFT');
  const split = splitRequest(request), schemaValue = readCanonical(path.join(root, SCHEMA));
  if (sha256(split.promptBytes) !== PROMPT_SHA256) throw Error('PROMPT_DRIFT');
  if (JSON.stringify(split.embeddedSchema) !== JSON.stringify(schemaValue)) throw Error('EMBEDDED_SCHEMA_DRIFT');
  if (!Array.isArray(split.input?.items) || split.input.items.length !== 16) throw Error('INPUT_ITEMS');
  const ids = split.input.items.map(x => x.item_id);
  if (new Set(ids).size !== 16 || ids.some((x, i) => x !== `D-I${String(i + 1).padStart(3, '0')}`)) throw Error('INPUT_ORDER');
  const requests = CELLS.map(cell => ({cell, path: REQUEST, sha256: REQUEST_SHA256, utf8_bytes: REQUEST_BYTES, prompt_sha256: PROMPT_SHA256, schema: SCHEMA, schema_sha256: SCHEMA_SHA256, item_ids: ids}));
  return {request, schema, manifest: {schema_version: 'gemini-original-a-repeat-request-manifest-v1', fixed_order: CELLS, requests}};
}

export function checkFreeze(root = here) {
  let built;
  try { built = build(root); } catch (error) { return {errors: [error.message], built: null}; }
  const file = path.join(root, 'frozen/REQUEST-MANIFEST.json'), expected = jsonBytes(built.manifest);
  if (!fs.existsSync(file)) return {errors: ['MISSING:frozen/REQUEST-MANIFEST.json'], built};
  return {errors: fs.readFileSync(file).equals(expected) ? [] : ['DRIFT:frozen/REQUEST-MANIFEST.json'], built};
}

export function freeze(root = here) {
  const built = build(root), file = path.join(root, 'frozen/REQUEST-MANIFEST.json'), bytes = jsonBytes(built.manifest);
  if (fs.existsSync(file)) { if (!fs.readFileSync(file).equals(bytes)) throw Error('FROZEN_DRIFT'); }
  else writeExclusive(file, bytes);
  return {cells: CELLS.length, request_sha256: REQUEST_SHA256, request_utf8_bytes: REQUEST_BYTES, prompt_sha256: PROMPT_SHA256, schema_sha256: SCHEMA_SHA256};
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    if (process.argv[2] === '--check') { const x = checkFreeze(); console.log(JSON.stringify({mode: 'CHECK', errors: x.errors}, null, 2)); process.exitCode = x.errors.length ? 3 : 0; }
    else if (process.argv.length === 2) console.log(JSON.stringify(freeze(), null, 2));
    else { console.error('usage: node freezer.mjs [--check]'); process.exitCode = 2; }
  } catch (error) { console.error(error.message); process.exitCode = 3; }
}
