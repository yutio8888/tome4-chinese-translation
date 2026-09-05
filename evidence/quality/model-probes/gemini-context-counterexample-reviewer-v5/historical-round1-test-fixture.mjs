import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import zlib from 'node:zlib';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const liveRepo = path.resolve(here, '..', '..', '..', '..');
const packPath = path.join(here, 'fixtures', 'ROUND-0001-PRE-RELEASE.json.gz');
const PACK_SHA256 = '6784d9e3d096e7a4c44d787d35aba2b39fcea8174b745b89a95513af37602547';
const PENDING_SHA256 = 'ce1afd35e964b4d87ddf70a13b13a7cce998befe46d5c81effce67187c7102c7';
const ACTIVE_SHA256 = 'dd7b79438691530fe573e1b5deec0aba64e6fd7c24cf26ce6cf45f7e3a6fa440';
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

function linkDependency(fixtureRepo, relativePath) {
  const source = path.join(liveRepo, relativePath), destination = path.join(fixtureRepo, relativePath);
  if (!fs.existsSync(source)) throw Error(`HISTORICAL_FIXTURE_DEPENDENCY_MISSING:${relativePath}`);
  fs.mkdirSync(path.dirname(destination), {recursive: true});
  fs.symlinkSync(source, destination, 'dir');
}

export function materializeHistoricalRound1Fixture() {
  const packBytes = fs.readFileSync(packPath);
  if (sha256(packBytes) !== PACK_SHA256) throw Error('HISTORICAL_FIXTURE_PACK_HASH');
  const pack = JSON.parse(zlib.gunzipSync(packBytes));
  if (pack.schema_version !== 'gemini-context-v5-round1-pre-release-fixture-pack-v1' || pack.status !== 'FROZEN_EXACT_HISTORICAL_TEST_FIXTURE' || pack.file_count !== 89 || pack.files?.length !== 89 || pack.source_pending_release_sha256 !== PENDING_SHA256 || pack.source_active_frame_sha256 !== ACTIVE_SHA256) throw Error('HISTORICAL_FIXTURE_PACK_SCHEMA');
  const fixtureRepo = fs.mkdtempSync(path.join(os.tmpdir(), 'v5-round1-pre-release-fixture-'));
  const seen = new Set();
  for (const entry of pack.files) {
    if (!entry || typeof entry.path !== 'string' || (!entry.path.startsWith('evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5/') && !entry.path.startsWith('.ai/task/research-gemini-context-counterexample-reviewer-v5/')) || path.posix.normalize(entry.path) !== entry.path || seen.has(entry.path)) throw Error('HISTORICAL_FIXTURE_PACK_PATH');
    seen.add(entry.path);
    const destination = path.join(fixtureRepo, entry.path);
    fs.mkdirSync(path.dirname(destination), {recursive: true});
    fs.writeFileSync(destination, Buffer.from(entry.bytes_base64, 'base64'));
  }
  linkDependency(fixtureRepo, '.artifacts');
  linkDependency(fixtureRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v4');
  linkDependency(fixtureRepo, '.ai/task/research-gemini-context-counterexample-reviewer-v4');
  const root = path.join(fixtureRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
  if (sha256(fs.readFileSync(path.join(root, 'PENDING-RELEASE.json'))) !== PENDING_SHA256 || sha256(fs.readFileSync(path.join(root, 'ACTIVE-FRAME.json'))) !== ACTIVE_SHA256 || fs.existsSync(path.join(root, 'rounds/ROUND-0001/RELEASE.json')) || fs.existsSync(path.join(root, 'rounds/ROUND-0002'))) throw Error('HISTORICAL_FIXTURE_STATE');
  return fixtureRepo;
}

export async function runHistoricalRound1Script(scriptName) {
  if (!/^[a-z0-9-]+\.mjs$/u.test(scriptName)) throw Error('HISTORICAL_FIXTURE_SCRIPT_NAME');
  const fixtureRepo = materializeHistoricalRound1Fixture();
  try {
    const script = path.join(fixtureRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5', scriptName);
    await import(`${pathToFileURL(script).href}?fixture=${crypto.randomUUID()}`);
  } finally {
    fs.rmSync(fixtureRepo, {recursive: true, force: true});
  }
}
