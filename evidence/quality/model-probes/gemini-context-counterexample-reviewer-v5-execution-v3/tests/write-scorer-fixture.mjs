#!/usr/bin/env node
// Emits tests/fixtures/scorer-case.json. The rows, candidates and expected counts below
// are hand-written; only the per-row sha256 is machine-filled so the fixture satisfies
// validateReference(). Rerunning this must reproduce the checked-in bytes exactly.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {sha256,jsonBytes} from '../lib.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const row=(item_id,profile,role,atoms)=>{const x={item_id,cohort:'discovery',profile,role,atoms};return{...x,row_sha256:sha256(jsonBytes(x))}};
const reference={
  schema_version:'gemini-context-v5-sealed-reference-v5',
  mutations_authored:true,
  sample_sha256:'0'.repeat(64),
  items:[
    row('F-I001','dialogue','CONTEXT_MUTANT',[{atom_id:'F-I001-A1',claim_types:['SUBJECT'],target_spans:['alpha beta']}]),
    row('F-I002','dialogue','CONTEXT_MUTANT',[{atom_id:'F-I002-A1',claim_types:['EVENT'],target_spans:['gamma delta']}]),
    row('F-I003','narrative','SURFACE_MUTANT',[{atom_id:'F-I003-A1',claim_types:['FORMAT'],target_spans:['epsilon']}]),
    row('F-I004','narrative','SURFACE_MUTANT',[{atom_id:'F-I004-A1',claim_types:['POLARITY'],target_spans:['zeta']}]),
    row('F-I005','dialogue','CLEAN_CONTROL',[]),
    row('F-I006','narrative','CLEAN_CONTROL',[])
  ]
};
const f=(claim_type,target_span,correction='c',evidence='e')=>({verdict:'FINDING',claim_type,target_span,correction,evidence});
const raw_items=[
  // HIT: reported span "xx alpha beta yy" CONTAINS frozen span "alpha beta", claim type matches.
  // The exact duplicate is collapsed; the second, distinct finding hits the same atom, which
  // is still credited once.
  {item_id:'F-I001',candidates:[f('SUBJECT','xx alpha beta yy'),f('SUBJECT','xx alpha beta yy'),f('SUBJECT','alpha beta',' other correction')]},
  // MISS: frozen span "gamma delta" CONTAINS the reported "gamma"; reverse containment is not a hit.
  {item_id:'F-I002',candidates:[f('EVENT','gamma')]},
  // HIT: exact equality is containment.
  {item_id:'F-I003',candidates:[f('FORMAT','epsilon')]},
  // MISS: span contains the frozen span but the claim_type is not listed on the atom.
  {item_id:'F-I004',candidates:[f('SUBJECT','zeta')]},
  // CLEAN false positive.
  {item_id:'F-I005',candidates:[f('OTHER','anything')]},
  // UNCERTAIN is not a FINDING: no clean false positive here.
  {item_id:'F-I006',candidates:[{verdict:'UNCERTAIN',claim_type:'OTHER',target_span:'anything',correction:'c',evidence:'e'}]}
];
const doc={
  note:'Hand-written scorer fixture for checklist item C07. reference x raw_items -> expected.',
  span_containment_rule:'A candidate hits an atom iff verdict is FINDING, the candidate claim_type is listed on the atom, and the REPORTED target_span CONTAINS a frozen atom span. The reverse containment is not a hit.',
  reference,
  raw_items,
  expected:{items:6,unique_findings:6,context_atoms_total:2,context_hits:1,surface_atoms_total:2,surface_hits:1,clean_items_total:2,clean_with_findings:1}
};
fs.writeFileSync(path.join(here,'fixtures/scorer-case.json'),jsonBytes(doc));
console.log(JSON.stringify({written:'tests/fixtures/scorer-case.json'}));
