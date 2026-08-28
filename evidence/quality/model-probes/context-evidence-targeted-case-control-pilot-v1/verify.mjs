#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildRegistry} from "./build.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {repo: null, root: path.resolve(here, "../../../..")};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--repo", "--root"].includes(flag)) {
      throw new Error("usage: node verify.mjs --repo SOURCE_REPO [--root RESEARCH_REPO]");
    }
    args[flag.slice(2)] = path.resolve(value);
  }
  if (!args.repo) throw new Error("--repo is required");
  return args;
}

const args = parseArgs(process.argv.slice(2));
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "context-evidence-registry-v1-"));
try {
  buildRegistry({...args, out: temporary});
  for (const name of ["PRIOR-EXPOSURE-REGISTRY.json", "NOVEL-FRAME.json"]) {
    const expected = fs.readFileSync(path.join(here, name));
    const actual = fs.readFileSync(path.join(temporary, name));
    if (!expected.equals(actual)) throw new Error(`${name}: deterministic rebuild differs`);
  }
  console.log("PASS deterministic registry/frame rebuild");
} finally {
  fs.rmSync(temporary, {recursive: true, force: true});
}
