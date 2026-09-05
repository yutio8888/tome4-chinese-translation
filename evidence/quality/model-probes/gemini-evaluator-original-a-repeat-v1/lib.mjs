import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const shaFile = file => sha256(fs.readFileSync(file));
export const jsonBytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
export const byteSort = (a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b));
export const exactKeys = (value, keys) => !!value && typeof value === 'object' && !Array.isArray(value) && JSON.stringify(Object.keys(value).sort(byteSort)) === JSON.stringify([...keys].sort(byteSort));

export function parseNoDuplicate(text, label = 'JSON') {
  let i = 0;
  const ws = () => { while (/\s/u.test(text[i] ?? '')) i++; };
  const str = () => {
    if (text[i++] !== '"') throw Error(`${label}:STRING`);
    let raw = '"';
    for (;;) {
      if (i >= text.length) throw Error(`${label}:STRING_EOF`);
      const c = text[i++]; raw += c;
      if (c === '"') break;
      if (c === '\\') { if (i >= text.length) throw Error(`${label}:ESCAPE_EOF`); raw += text[i++]; }
      else if (c < ' ') throw Error(`${label}:CONTROL`);
    }
    return JSON.parse(raw);
  };
  const val = () => {
    ws();
    if (text[i] === '"') { str(); return; }
    if (text[i] === '{') { obj(); return; }
    if (text[i] === '[') { arr(); return; }
    const match = text.slice(i).match(/^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/u);
    if (!match) throw Error(`${label}:VALUE@${i}`);
    i += match[0].length;
  };
  const obj = () => {
    i++; ws(); const keys = new Set();
    if (text[i] === '}') { i++; return; }
    for (;;) {
      ws(); const key = str();
      if (keys.has(key)) throw Error(`${label}:DUPLICATE_KEY:${key}`);
      keys.add(key); ws();
      if (text[i++] !== ':') throw Error(`${label}:COLON`);
      val(); ws(); const c = text[i++];
      if (c === '}') return;
      if (c !== ',') throw Error(`${label}:OBJECT_SEPARATOR`);
    }
  };
  const arr = () => {
    i++; ws();
    if (text[i] === ']') { i++; return; }
    for (;;) { val(); ws(); const c = text[i++]; if (c === ']') return; if (c !== ',') throw Error(`${label}:ARRAY_SEPARATOR`); }
  };
  val(); ws();
  if (i !== text.length) throw Error(`${label}:TRAILING`);
  return JSON.parse(text);
}

export function readCanonical(file) {
  const bytes = fs.readFileSync(file), value = parseNoDuplicate(bytes.toString('utf8'), file);
  if (!bytes.equals(jsonBytes(value))) throw Error(`NONCANONICAL:${file}`);
  return value;
}

export function walk(dir, base = '', out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, {withFileTypes: true}).sort((a, b) => byteSort(a.name, b.name))) {
    const rel = path.posix.join(base, entry.name), file = path.join(dir, entry.name), stat = fs.lstatSync(file);
    if (stat.isSymbolicLink()) throw Error(`SYMLINK:${rel}`);
    if (entry.isDirectory()) walk(file, rel, out);
    else if (entry.isFile()) out.push(rel);
    else throw Error(`NONREGULAR:${rel}`);
  }
  return out;
}

// Canonical tree hash: bytewise-sorted relative paths, each encoded as
// path NUL lowercase-file-sha256 LF, then SHA-256 over the concatenation.
export function treeBinding(repoRoot, rel) {
  const dir = path.join(repoRoot, rel);
  const files = walk(dir).map(file => ({path: file, sha256: shaFile(path.join(dir, file))})).sort((a, b) => byteSort(a.path, b.path));
  return {root: rel, file_count: files.length, tree_sha256: sha256(Buffer.concat(files.map(x => Buffer.from(`${x.path}\0${x.sha256}\n`))))};
}

export function writeExclusive(file, bytes) {
  fs.mkdirSync(path.dirname(file), {recursive: true});
  fs.writeFileSync(file, Buffer.isBuffer(bytes) ? bytes : jsonBytes(bytes), {flag: 'wx'});
}
