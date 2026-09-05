const PROFILES=['dialogue','narrative'];
const COHORTS=['discovery','confirmation'];

export function groupByProfileSourceFile(rows){
  const grouped={dialogue:new Map(),narrative:new Map()};
  for(const row of rows){
    if(!grouped[row.profile])continue;
    if(!grouped[row.profile].has(row.public_source_file))grouped[row.profile].set(row.public_source_file,[]);
    grouped[row.profile].get(row.public_source_file).push(row);
  }
  return grouped;
}
export function isAcceptedProfileSection(profile,section){
  if(profile==='dialogue')return /^mod-tome\/data\/chats\/[^/]+\.lua$/u.test(section);
  if(profile==='narrative'){
    if(!/^mod-tome\/data\/(?:lore\/[^/]+|texts\/[^/]+\.lua)$/u.test(section))return false;
    if(section.startsWith('mod-tome/data/texts/')){
      const basename=section.slice(section.lastIndexOf('/')+1).toLowerCase();
      return !basename.includes('tutorial')&&/^(?:intro-|message-)/u.test(basename);
    }
    return true;
  }
  return false;
}
export function capRankedUniverse(rankedRows,fileCap=3){
  if(!Number.isInteger(fileCap)||fileCap<1)throw Error('invalid file cap');
  const counts=new Map(),kept=[];
  for(const row of rankedRows){const n=counts.get(row.public_source_file)??0;if(n<fileCap){kept.push(row);counts.set(row.public_source_file,n+1)}}
  return kept;
}
function compatible(row,cohort,active,{totalFileCap=3,cohortFileCap=2}={}){
  const total=active.filter(x=>x.profile===row.profile&&x.public_source_file===row.public_source_file).length;
  const inCohort=active.filter(x=>x.profile===row.profile&&x.cohort===cohort&&x.public_source_file===row.public_source_file).length;
  return total<totalFileCap&&inCohort<cohortFileCap;
}
export function selectAlternatingCohorts(rankedRows,{perCohort=16,totalFileCap=3,cohortFileCap=2}={}){
  const selected=[],used=new Set();
  for(let slot=0;slot<perCohort*COHORTS.length;slot++){
    const cohort=COHORTS[slot%2];
    const row=rankedRows.find(x=>!used.has(x.revision_id)&&compatible(x,cohort,selected,{totalFileCap,cohortFileCap}));
    if(!row)throw Error(`exact shortfall: ${row?.profile??rankedRows[0]?.profile??'unknown'}/${cohort} ${selected.filter(x=>x.cohort===cohort).length}/${perCohort}`);
    used.add(row.revision_id);selected.push({...row,cohort});
  }
  return selected;
}
export function replaceRejectedRows({selected,reserve,rejectedRevisionIds,rejectionHistory=[],priorLedger=[],totalFileCap=3,cohortFileCap=2}){
  const banned=new Set(rejectedRevisionIds),usedReserve=new Set(),ledger=[];
  const initialIds=new Set(selected.map(x=>x.revision_id));
  const byRevision=new Map([...selected,...reserve].map(x=>[x.revision_id,x]));
  const chains=new Map();
  for(const x of rejectionHistory){if(!byRevision.has(x.revision_id))throw Error('rejected-base ledger contains unknown revision');if(!chains.has(x.neutral_id))chains.set(x.neutral_id,[]);chains.get(x.neutral_id).push(x.revision_id)}
  for(const [neutral,chain] of chains){const base=selected.find(x=>x.neutral_id===neutral);if(!base||chain[0]!==base.revision_id||new Set(chain).size!==chain.length)throw Error(`invalid rejection lineage for ${neutral}`)}
  const predecessorNext=new Map();for(const x of priorLedger){if(x.neutral_id&&x.rejected_revision_id&&x.replacement_revision_id)predecessorNext.set(`${x.neutral_id}\0${x.rejected_revision_id}`,x.replacement_revision_id)}
  if([...banned].some(id=>!initialIds.has(id)&&!reserve.some(x=>x.revision_id===id)))throw Error('rejected-base ledger contains unknown revision');

  // Freeze the retained frame first.  Replacement candidates must be checked
  // against every retained slot, including slots later in frozen slot order.
  const active=selected
    .filter(slot=>!banned.has(slot.revision_id))
    .map(slot=>({...slot,neutral_id:slot.neutral_id,cohort:slot.cohort,profile:slot.profile}));
  const output=selected.map(slot=>slot);
  for(let slotIndex=0;slotIndex<selected.length;slotIndex++){
    const slot=selected[slotIndex]; let current=slot;
    while(banned.has(current.revision_id)){
      const skipped=[]; let chosen=-1;
      const expectedNext=predecessorNext.get(`${slot.neutral_id}\0${current.revision_id}`);
      for(let i=0;i<reserve.length;i++){
        const candidate=reserve[i];
        if(candidate.profile!==slot.profile||usedReserve.has(i))continue;
        if(expectedNext&&candidate.revision_id!==expectedNext){skipped.push({reserve_rank:candidate.reserve_rank??i+1,revision_id:candidate.revision_id,public_source_file:candidate.public_source_file,reason:'LINEAGE_ORDER'});continue}
        let reason=null;
        if(banned.has(candidate.revision_id)&&!expectedNext)reason='GLOBALLY_BANNED_REVISION';
        else if(active.some(x=>x.revision_id===candidate.revision_id))reason='REVISION_COLLISION';
        else if((candidate.revision_uid||candidate.unit_id)!=null&&active.some(x=>(x.revision_uid||x.unit_id)===(candidate.revision_uid||candidate.unit_id)))reason='BASE_IDENTITY_COLLISION';
        else if(active.some(x=>x.normalized_source===candidate.normalized_source))reason='NORMALIZED_SOURCE_COLLISION';
        else if(active.some(x=>x.selection_context===candidate.selection_context))reason='NORMALIZED_CONTEXT_COLLISION';
        else if(!compatible(candidate,slot.cohort,active,{totalFileCap,cohortFileCap}))reason='ACTIVE_FILE_CAP';
        if(reason){skipped.push({reserve_rank:candidate.reserve_rank??i+1,revision_id:candidate.revision_id,public_source_file:candidate.public_source_file,reason});continue}
        chosen=i;break;
      }
      if(chosen<0)throw Error(`exact shortfall: ${slot.profile}/${slot.cohort} replacement reserve exhausted for ${slot.neutral_id}`);
      const candidate=reserve[chosen];usedReserve.add(chosen);const row={...candidate,neutral_id:slot.neutral_id,cohort:slot.cohort,profile:slot.profile};
      const priorEntry=expectedNext&&priorLedger.find(x=>x.neutral_id===slot.neutral_id&&x.rejected_revision_id===current.revision_id);ledger.push(priorEntry?{...priorEntry}: {neutral_id:slot.neutral_id,cohort:slot.cohort,profile:slot.profile,rejected_revision_id:current.revision_id,replacement_revision_id:candidate.revision_id,replacement_file:candidate.public_source_file,reserve_rank:candidate.reserve_rank??chosen+1,skipped_incompatible_reserves:skipped});
      current=row;
      if(!banned.has(current.revision_id)){active.push(current);output[slotIndex]=current}
    }
  }
  return{selected:output,ledger,usedReserveIndices:usedReserve};
}
export function assertFrameCaps(rows,totalFileCap=3,cohortFileCap=2){
  for(const profile of PROFILES){
    const p=rows.filter(x=>x.profile===profile),files=new Set(p.map(x=>x.public_source_file));
    for(const file of files){if(p.filter(x=>x.public_source_file===file).length>totalFileCap)throw Error(`active total file cap: ${profile}:${file}`);for(const cohort of COHORTS)if(p.filter(x=>x.cohort===cohort&&x.public_source_file===file).length>cohortFileCap)throw Error(`active cohort file cap: ${profile}:${cohort}:${file}`)}
  }
}
export function concentration(rows){
  const m=new Map();for(const x of rows)m.set(x.public_source_file,(m.get(x.public_source_file)??0)+1);
  const entries=[...m].map(([public_source_file,count])=>({public_source_file,count})).sort((a,b)=>b.count-a.count||Buffer.compare(Buffer.from(a.public_source_file),Buffer.from(b.public_source_file)));
  return{rows:rows.length,distinct_files:m.size,max_rows_per_file:entries[0]?.count??0,top_files:entries.slice(0,10)};
}
export function remainingRejectionTolerance(initialReserveRows,consumedRows,globallyBannedReserveRows=0){if(!Number.isInteger(initialReserveRows)||!Number.isInteger(consumedRows)||!Number.isInteger(globallyBannedReserveRows)||initialReserveRows<0||consumedRows<0||globallyBannedReserveRows<0||consumedRows+globallyBannedReserveRows>initialReserveRows)throw Error('invalid reserve accounting');return initialReserveRows-consumedRows-globallyBannedReserveRows}
