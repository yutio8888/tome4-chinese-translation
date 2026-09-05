#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const ids=JSON.parse(fs.readFileSync(path.join(here,'SOURCE-FRAME.json'),'utf8')).items.map(x=>x.neutral_id);
const pattern='^V2-[DC]-[DN][0-9]{2}$';
for(const name of ['CLEAN-AUDIT-SCHEMA.json','MANIPULATION-CHECK-SCHEMA.json','MUTATION-AUTHOR-SCHEMA.json']){
  const schema=JSON.parse(fs.readFileSync(path.join(here,'schemas',name),'utf8'));
  const branches=schema.oneOf??[schema];
  for(const branch of branches)assert.equal(branch.properties.neutral_id.pattern,pattern,name);
}
assert.equal(ids.length,64);
assert.ok(ids.every(id=>new RegExp(pattern,'u').test(id)));
assert.ok(ids.every(id=>!/^N[0-9]{4}$/u.test(id)));
assert.ok(['N0001','N9999','V1-D-D01'].every(id=>!new RegExp(pattern,'u').test(id)));
console.log(JSON.stringify({status:'PASS',tests:['all 64 frozen v2 neutral IDs match every audit/mutation schema','v1 neutral IDs rejected']},null,2));
