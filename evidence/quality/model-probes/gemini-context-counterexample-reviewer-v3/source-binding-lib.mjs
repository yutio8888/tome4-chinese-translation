import {normalize,sha256} from './lib.mjs';

const lineAt=(text,offset)=>1+(text.slice(0,offset).match(/\n/gu)?.length??0);
function longOpen(text,i){const m=text.slice(i).match(/^\[(=*)\[/u);return m?{eq:m[1],length:m[0].length}:null}
function skipComment(text,i){
  if(text.slice(i,i+2)!=='--')return null;
  const long=longOpen(text,i+2);
  if(long){const close=`]${long.eq}]`,end=text.indexOf(close,i+2+long.length);return end<0?text.length:end+close.length}
  const end=text.indexOf('\n',i+2);return end<0?text.length:end;
}
function decodeShort(raw,quote){
  let out='';
  for(let i=0;i<raw.length;i++){
    if(raw[i]!=='\\'){out+=raw[i];continue}
    const c=raw[++i];if(c===undefined)throw Error('unterminated escape');
    const simple={a:'\x07',b:'\b',f:'\f',n:'\n',r:'\r',t:'\t',v:'\v','\\':'\\','"':'"',"'":"'",'\n':'\n','\r':'\n'};
    if(Object.hasOwn(simple,c)){out+=simple[c];if(c==='\r'&&raw[i+1]==='\n')i++;continue}
    if(c==='x'&&/^[0-9a-fA-F]{2}$/u.test(raw.slice(i+1,i+3))){out+=String.fromCharCode(parseInt(raw.slice(i+1,i+3),16));i+=2;continue}
    if(/[0-9]/u.test(c)){const m=raw.slice(i).match(/^\d{1,3}/u)[0];out+=String.fromCharCode(Number(m));i+=m.length-1;continue}
    if(c==='z'){while(/\s/u.test(raw[i+1]??''))i++;continue}
    out+=c;
  }
  return out;
}
function parseString(text,i){
  const quote=text[i];
  if(quote==='"'||quote==="'"){
    let j=i+1;
    for(;j<text.length;j++){if(text[j]==='\\'){j++;continue}if(text[j]===quote)break}
    if(j>=text.length)return null;
    return{value:decodeShort(text.slice(i+1,j),quote),start:i,end:j+1,style:'SHORT_STRING'};
  }
  const long=longOpen(text,i);if(!long)return null;
  const close=`]${long.eq}]`,contentStart=i+long.length,end=text.indexOf(close,contentStart);if(end<0)return null;
  let value=text.slice(contentStart,end);if(value.startsWith('\r\n'))value=value.slice(2);else if(value.startsWith('\n')||value.startsWith('\r'))value=value.slice(1);
  return{value,start:i,end:end+close.length,style:'LONG_STRING'};
}
function skipSpaceAndComments(text,i){for(;;){while(/\s/u.test(text[i]??''))i++;const end=skipComment(text,i);if(end===null)return i;i=end}}
function taggedMatch(expectedTag,actualTag){return expectedTag==='_t'?actualTag==='_t':actualTag===expectedTag}
function enclosingLuaField(text,offset){const prefix=text.slice(0,offset),line=prefix.slice(prefix.lastIndexOf('\n')+1);return line.match(/(?:^|[{,])\s*([_A-Za-z][_A-Za-z0-9]*)\s*=\s*$/u)?.[1]??null}

export function extractTranslatableLuaStrings(text){
  const found=[];let i=0;
  while(i<text.length){
    const commentEnd=skipComment(text,i);if(commentEnd!==null){i=commentEnd;continue}
    const standalone=parseString(text,i);if(standalone){i=standalone.end;continue}
    const id=text.slice(i).match(/^[_A-Za-z][_A-Za-z0-9]*/u);
    if(!id){i++;continue}
    const name=id[0],start=i;i+=name.length;if(name!=='_t')continue;
    i=skipSpaceAndComments(text,i);let call=false;if(text[i]==='('){call=true;i=skipSpaceAndComments(text,i+1)}
    const first=parseString(text,i);if(!first)continue;i=first.end;
    let tag=null;if(call){let j=skipSpaceAndComments(text,i);if(text[j]===','){j=skipSpaceAndComments(text,j+1);const second=parseString(text,j);if(second)tag=second.value}}
    found.push({value:first.value,source_tag:tag??'_t',line:lineAt(text,start),construct:`_t_${call?'CALL_':''}${first.style}`,construct_start:start,string_start:first.start,string_end:first.end});
  }
  return found;
}

export function isNarrativeMetadataSourceTag(tag){
  const folded=String(tag??'').normalize('NFKC').toLowerCase().replace(/[_-]+/gu,' ').replace(/\s+/gu,' ').trim();
  return /^(?:newlore\s+)?category(?:\s+(?:metadata|identifier))?$/u.test(folded);
}

export function bindInventoryOccurrence({row,text,publicSourceFile,lineRadius=12,marker='[[SOURCE_MATCH_1]]'}){
  if(row.occurrences?.length!==1||row.occurrences[0].section!==row.section)return{ok:false,reason:'INVENTORY_OCCURRENCE_SITE_MISMATCH'};
  if(isNarrativeMetadataSourceTag(row.source_tag))return{ok:false,reason:'METADATA_IDENTIFIER_SOURCE_TAG'};
  const matches=extractTranslatableLuaStrings(text).filter(x=>x.value===row.source&&taggedMatch(row.source_tag,x.source_tag));
  if(matches.length!==1)return{ok:false,reason:matches.length?'AMBIGUOUS_TRANSLATABLE_OCCURRENCE':'NO_TRANSLATABLE_OCCURRENCE',match_count:matches.length};
  const match=matches[0];
  if(publicSourceFile.includes('/data/lore/')){
    const field=enclosingLuaField(text,match.construct_start);
    if(field!=='lore')return{ok:false,reason:field===null?'NARRATIVE_LORE_FIELD_UNRESOLVED':'NARRATIVE_LORE_FIELD_NOT_BODY',field:field??null,accepted_field:'lore'};
  }
  const lines=text.split('\n'),from=Math.max(0,match.line-1-lineRadius),to=Math.min(lines.length,match.line+lineRadius);
  const packetLines=lines.slice(from,to),boundLine=match.line-1-from,lineStart=text.lastIndexOf('\n',match.construct_start-1)+1,column=match.construct_start-lineStart;
  packetLines[boundLine]=`${packetLines[boundLine].slice(0,column)}${marker}${packetLines[boundLine].slice(column)}`;
  const sourceContext=normalize(packetLines.join('\n'));
  if((sourceContext.match(/\[\[SOURCE_MATCH_1\]\]/gu)||[]).length!==1)return{ok:false,reason:'MARKER_CARDINALITY'};
  return{ok:true,source_context:sourceContext,context_sha256:sha256(sourceContext),source_match_count:1,context_line_radius:lineRadius,occurrence:{public_source_file:publicSourceFile,line:match.line,construct:match.construct,inventory_logical_path:row.occurrences[0].logical_path,inventory_line:row.occurrences[0].line,inventory_ordinal:row.occurrences[0].ordinal}};
}
