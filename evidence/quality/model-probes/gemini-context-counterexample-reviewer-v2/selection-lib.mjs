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
export function assertInitialProfileAvailability(counts, minimum=32){
  for(const profile of ['dialogue','narrative']){
    const actual=counts[profile]??0;
    if(actual<minimum)throw Error(`exact shortfall: ${profile} ${actual}/${minimum} eligible source files`);
  }
}
export function takeNextSameProfile(reserve, profile, cursors, usedFiles=new Set()){
  const rows=reserve.filter(x=>x.profile===profile);
  while((cursors[profile]??0)<rows.length){
    const row=rows[cursors[profile]++];
    if(!usedFiles.has(row.file))return row;
  }
  return null;
}
