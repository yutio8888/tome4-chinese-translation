// The single scorer. Maps (RAW findings x sealed reference rows) to three counts.
//
// SPAN-CONTAINMENT RULE (one direction, normative):
//   A reported candidate hits a reference atom iff
//     (a) candidate.verdict === 'FINDING', AND
//     (b) candidate.claim_type is listed in atom.claim_types, AND
//     (c) SOME frozen span s in atom.target_spans satisfies
//           candidate.target_span.includes(s)
//         i.e. the REPORTED span must CONTAIN the FROZEN span.
//   The reverse containment (frozen span contains reported span) is NOT a hit.
//   Each (item, atom) pair is credited at most once, however many candidates hit it.
//   Byte-identical duplicate candidates within an item are collapsed before counting.
//
// Counts:
//   context_hits        = distinct (item, atom) hits on rows with role CONTEXT_MUTANT
//   surface_hits        = distinct (item, atom) hits on rows with role SURFACE_MUTANT
//   clean_with_findings = rows with role CLEAN_CONTROL carrying >= 1 FINDING candidate
import {sha256,jsonBytes,exactKeys} from './lib.mjs';
export const ROLES=['CONTEXT_MUTANT','SURFACE_MUTANT','CLEAN_CONTROL'];
export const CLAIM_TYPES=['SUBJECT','REFERENT','EVENT','CONDITION','SCOPE','DIRECTION','POLARITY','OWNERSHIP','ACTION','STATE','TIMING','OMISSION','ADDITION','FORMAT','OTHER'];
const roles=new Set(ROLES),claims=new Set(CLAIM_TYPES);

export function validateReference(ref,sampleDoc=null,expectedHash=null){
  const e=[];
  if(expectedHash&&sha256(jsonBytes(ref))!==expectedHash)e.push('REFERENCE_HASH');
  if(!exactKeys(ref,['items','mutations_authored','sample_sha256','schema_version'])||ref?.schema_version!=='gemini-context-v5-sealed-reference-v5'||typeof ref.mutations_authored!=='boolean'||!Array.isArray(ref.items)||!ref.items.length)return[...e,'REFERENCE_SCHEMA'];
  if(sampleDoc){if(ref.sample_sha256!==sha256(jsonBytes(sampleDoc)))e.push('REFERENCE_SAMPLE_HASH');if(ref.items.length!==(sampleDoc.items?.length??-1))e.push('REFERENCE_ITEM_COUNT')}
  const base=sampleDoc?.items??null,seen=new Set();
  ref.items.forEach((x,i)=>{
    if(!exactKeys(x,['atoms','cohort','item_id','profile','role','row_sha256'])||typeof x.item_id!=='string'||!roles.has(x.role)||!Array.isArray(x.atoms)){e.push(`REFERENCE_ITEM:${i}`);return}
    if(seen.has(x.item_id))e.push(`REFERENCE_DUPLICATE_ITEM:${x.item_id}`);seen.add(x.item_id);
    if(base&&(x.item_id!==base[i]?.item_id||x.cohort!==base[i]?.cohort||x.profile!==base[i]?.profile))e.push(`REFERENCE_SAMPLE_ALIGNMENT:${i}`);
    const row={item_id:x.item_id,cohort:x.cohort,profile:x.profile,role:x.role,atoms:x.atoms};
    if(x.row_sha256!==sha256(jsonBytes(row)))e.push(`REFERENCE_ROW_HASH:${i}`);
    if(x.role==='CLEAN_CONTROL'&&x.atoms.length)e.push(`CLEAN_ATOMS:${i}`);
    if(x.role!=='CLEAN_CONTROL'&&!x.atoms.length)e.push(`MUTANT_ATOMS:${i}`);
    if(ref.mutations_authored===false&&x.role!=='CLEAN_CONTROL')e.push(`UNAUTHORED_MUTANT:${i}`);
    const atomIds=new Set();
    x.atoms.forEach((a,j)=>{
      if(!exactKeys(a,['atom_id','claim_types','target_spans'])||typeof a.atom_id!=='string'||!a.atom_id||!Array.isArray(a.claim_types)||!a.claim_types.length||!a.claim_types.every(c=>claims.has(c))||!Array.isArray(a.target_spans)||!a.target_spans.length||!a.target_spans.every(s=>typeof s==='string'&&s)){e.push(`ATOM:${i}:${j}`);return}
      if(atomIds.has(a.atom_id))e.push(`ATOM_DUPLICATE:${i}:${a.atom_id}`);
      atomIds.add(a.atom_id);
    });
  });
  return e;
}

// referenceRows: the sealed reference rows for exactly the items in this cell.
export function scoreCell(responseItems,referenceRows){
  if(!Array.isArray(responseItems))throw Error('RESPONSE_ITEMS');
  const byId=new Map(referenceRows.map(x=>[x.item_id,x])),seen=new Set(),hits=new Set(),findingItems=new Set();
  let unique=0;
  for(const out of responseItems){
    if(seen.has(out.item_id))throw Error(`DUPLICATE_ITEM:${out.item_id}`);
    seen.add(out.item_id);
    const r=byId.get(out.item_id);
    if(!r)throw Error(`UNKNOWN_ITEM:${out.item_id}`);
    const dedupe=new Set();
    for(const c of out.candidates??[]){
      if(c.verdict!=='FINDING')continue;
      const key=JSON.stringify([c.claim_type,c.target_span,c.correction,c.evidence]);
      if(dedupe.has(key))continue;
      dedupe.add(key);
      unique++;
      findingItems.add(out.item_id);
      for(const a of r.atoms)if(a.claim_types.includes(c.claim_type)&&a.target_spans.some(s=>String(c.target_span).includes(s)))hits.add(`${out.item_id} ${a.atom_id}`);
    }
  }
  if(seen.size!==referenceRows.length)throw Error(`ITEM_COVERAGE:${seen.size}/${referenceRows.length}`);
  const roleOf=id=>byId.get(id).role,count=role=>[...hits].filter(k=>roleOf(k.split(' ')[0])===role).length;
  return{
    items:seen.size,
    unique_findings:unique,
    context_atoms_total:referenceRows.filter(x=>x.role==='CONTEXT_MUTANT').reduce((n,x)=>n+x.atoms.length,0),
    context_hits:count('CONTEXT_MUTANT'),
    surface_atoms_total:referenceRows.filter(x=>x.role==='SURFACE_MUTANT').reduce((n,x)=>n+x.atoms.length,0),
    surface_hits:count('SURFACE_MUTANT'),
    clean_items_total:referenceRows.filter(x=>x.role==='CLEAN_CONTROL').length,
    clean_with_findings:referenceRows.filter(x=>x.role==='CLEAN_CONTROL'&&findingItems.has(x.item_id)).length
  };
}

// Deterministic SCORES document. Same inputs -> byte-identical bytes.
export function scoresDocument({reference_sha256,sample_sha256,cells}){
  const rows=[...cells].sort((a,b)=>a.cell<b.cell?-1:a.cell>b.cell?1:0);
  const sum=k=>rows.reduce((n,x)=>n+x.score[k],0);
  return{
    schema_version:'gemini-context-v5-scores-v5',
    pilot_result_is_not_experimental_evidence:true,
    sample_sha256,
    reference_sha256,
    cells:rows.map(x=>({cell:x.cell,protocol:x.protocol,raw_path:x.raw_path,raw_sha256:x.raw_sha256,score:x.score})),
    totals_by_protocol:Object.fromEntries([...new Set(rows.map(x=>x.protocol))].sort().map(p=>{
      const xs=rows.filter(x=>x.protocol===p);
      return[p,{cells:xs.length,context_hits:xs.reduce((n,x)=>n+x.score.context_hits,0),surface_hits:xs.reduce((n,x)=>n+x.score.surface_hits,0),clean_with_findings:xs.reduce((n,x)=>n+x.score.clean_with_findings,0)}];
    })),
    totals:{cells:rows.length,context_hits:sum('context_hits'),surface_hits:sum('surface_hits'),clean_with_findings:sum('clean_with_findings')}
  };
}
