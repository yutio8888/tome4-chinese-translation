#!/usr/bin/env node
import path from'node:path';import{spawnSync}from'node:child_process';import{fileURLToPath}from'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));for(const script of['rebuild-canonical-frame.mjs','freeze-exposure.mjs','build-pool.mjs']){const p=spawnSync(process.execPath,[path.join(here,script)],{cwd:here,encoding:'utf8',maxBuffer:128*1024*1024});if(p.status!==0)throw Error(`${script} failed\n${p.stdout}\n${p.stderr}`);process.stdout.write(p.stdout)}
