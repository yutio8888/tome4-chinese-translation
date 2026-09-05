export function groupByProfileSourceFile(rows){
  const grouped={dialogue:new Map(),narrative:new Map()};
  for(const row of rows){
    const profile=grouped[row.profile];
    if(!profile)continue;
    if(!profile.has(row.public_source_file))profile.set(row.public_source_file,[]);
    profile.get(row.public_source_file).push(row);
  }
  return grouped;
}
export function isAcceptedProfileSection(profile,section){
  if(profile==='dialogue')return /^mod-tome\/data\/chats\/[^/]+\.lua$/u.test(section);
  if(profile==='narrative'){
    if(!/^mod-tome\/data\/(?:lore\/[^/]+|texts\/[^/]+\.lua)$/u.test(section))return false;
    if(section.startsWith('mod-tome/data/texts/')){
      const basename=section.slice(section.lastIndexOf('/')+1).toLowerCase();
      if(basename.includes('tutorial'))return false;
        return /^(?:intro-|message-)/u.test(basename);
    }
    return true;
  }
  return false;
}
export function assertInitialProfileAvailability(counts, minimum=32){
  for(const profile of ['dialogue','narrative']){
    const actual=counts[profile]??0;
    if(actual<minimum)throw Error(`exact shortfall: ${profile} ${actual}/${minimum} eligible source files`);
  }
}
export function assertNarrativeReserveTarget(narrativeFiles, selected=32, minimumReserve=50){
  const reserve=narrativeFiles-selected;
  if(reserve<minimumReserve)throw Error(`exact shortfall: narrative reserve ${Math.max(0,reserve)}/${minimumReserve} files after ${selected} selected files`);
  return reserve;
}
export function remainingRejectionTolerance(preRankingReserve, consumedReserveEntries){
  if(!Number.isInteger(preRankingReserve)||!Number.isInteger(consumedReserveEntries)||preRankingReserve<0||consumedReserveEntries<0||consumedReserveEntries>preRankingReserve)throw Error('invalid reserve accounting');
  return preRankingReserve-consumedReserveEntries;
}
export function takeNextSameProfile(reserve, profile, cursors, usedFiles=new Set()){
  const rows=reserve.filter(x=>x.profile===profile);
  while((cursors[profile]??0)<rows.length){
    const row=rows[cursors[profile]++];
    if(!usedFiles.has(row.file))return row;
  }
  return null;
}
