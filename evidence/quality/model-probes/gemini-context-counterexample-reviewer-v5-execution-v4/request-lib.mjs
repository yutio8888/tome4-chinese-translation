import {sha256} from './lib.mjs';

export const CONTEXT_RENDER_SCHEMA='runtime-context-text-v2';
export const CONTEXT_SEGMENT_MAX_UTF8_BYTES=8192;
export const REQUEST_MAX_UTF8_BYTES=120000;
const bannedKey=/(?:reference|adjudicat|defect(?:[_-]?id)?|revision|provenance|provider|credential|token|secret|api.?key|authorization)/iu;
const explicitLeak=/(?:\/(?:home|Users|root|tmp|opt|var|mnt)\/|\[\[(?:SEALED_REFERENCE|ADJUDICATION|DEFECT_ID|MODEL_PROVENANCE|CREDENTIAL)[^\]]*\]\]|(?:sealed[_ -]?reference|adjudication(?:[_ -]?(?:result|finding|decision))?|defect[_ -]?id|model[_ -]?provenance|credential(?:s)?|authorization\s*:\s*bearer|(?:api[_-]?key|access[_-]?token|client[_-]?secret))\s*[:=])/iu;
const internalMarkers=['proposal_sha256','row_sha256','base_item_id','planned_role','public_source_file','revision_uid','normalized_context_sha256'];
const exactKeys=(x,keys)=>x&&JSON.stringify(Object.keys(x).sort())===JSON.stringify([...keys].sort());
const coordinate=(segment,key)=>Number.isInteger(segment?.[key])?String(segment[key]):'-';

function truncateUtf8(text,max=CONTEXT_SEGMENT_MAX_UTF8_BYTES){
  const input=String(text),bytes=Buffer.from(input);
  if(bytes.length<=max)return{text:input,truncated:false,original_bytes:bytes.length,rendered_bytes:bytes.length};
  let end=max;
  while(end>0&&(bytes[end]&0xc0)===0x80)end--;
  const out=bytes.subarray(0,end).toString('utf8');
  return{text:out,truncated:true,original_bytes:bytes.length,rendered_bytes:Buffer.byteLength(out)};
}
function renderSegment(name,segment,{neverTruncate=false,expectedSource=null}={}){
  if(!segment||typeof segment!=='object'||typeof segment.text!=='string')throw Error(`RUNTIME_CONTEXT_SEGMENT:${name}`);
  let text=segment.text;
  if(expectedSource!==null&&!text.includes(expectedSource))text=`${text}\n[[EXACT_ITEM_SOURCE_BEGIN]]\n${expectedSource}\n[[EXACT_ITEM_SOURCE_END]]`;
  const cut=neverTruncate?{text,truncated:false,original_bytes:Buffer.byteLength(text),rendered_bytes:Buffer.byteLength(text)}:truncateUtf8(text);
  if(neverTruncate&&cut.text!==text)throw Error('SOURCE_CONSTRUCT_RENDER_TRUNCATED');
  const sentinel=typeof segment.sentinel==='string'&&segment.sentinel?segment.sentinel:'[[NO_SOURCE_SENTINEL]]';
  const renderSentinel=cut.truncated?`[[MODEL_CONTEXT_${name}_TRUNCATED_AT_${CONTEXT_SEGMENT_MAX_UTF8_BYTES}_UTF8_BYTES]]`:'[[MODEL_CONTEXT_SEGMENT_COMPLETE]]';
  return [`[${name}]`,`lines=${coordinate(segment,'line_start')}-${coordinate(segment,'line_end')}`,`bytes=${coordinate(segment,'byte_start')}-${coordinate(segment,'byte_end_exclusive')}`,`source_truncated=${segment.truncated===true?'true':'false'}`,`source_sentinel=${sentinel}`,`renderer_truncated=${cut.truncated?'true':'false'}`,`original_utf8_bytes=${cut.original_bytes}`,`rendered_utf8_bytes=${cut.rendered_bytes}`,'TEXT_BEGIN',cut.text,'TEXT_END',renderSentinel,`[/${name}]`].join('\n');
}
export function renderRuntimeContext(context,expectedSource=null){
  if(!context||typeof context!=='object'||Array.isArray(context))throw Error('RUNTIME_CONTEXT_TYPE');
  for(const k of ['before','source_construct','after'])if(!context[k]||typeof context[k]!=='object')throw Error(`RUNTIME_CONTEXT_MISSING:${k}`);
  const sc=context.source_construct;
  if(sc.complete_source_present!==true||sc.source_truncated!==false)throw Error('RUNTIME_CONTEXT_SOURCE_INCOMPLETE');
  if(expectedSource!==null&&(typeof expectedSource!=='string'||!expectedSource))throw Error('EXPECTED_SOURCE');
  const header=[`CONTEXT_RENDER_SCHEMA=${CONTEXT_RENDER_SCHEMA}`,`radius_lines=${coordinate(context,'radius_lines')}`,`file_total_lines=${coordinate(context,'file_total_lines')}`,`file_total_bytes=${coordinate(context,'file_total_bytes')}`].join('\n');
  const rendered=`${header}\n${renderSegment('BEFORE',context.before)}\n${renderSegment('SOURCE_CONSTRUCT',sc,{neverTruncate:true,expectedSource})}\n${renderSegment('AFTER',context.after)}\nCONTEXT_RENDER_END`;
  if(expectedSource!==null&&!rendered.includes(expectedSource))throw Error('RENDERED_CONTEXT_OMITS_SOURCE');
  if(/\[\[MODEL_CONTEXT_SOURCE_CONSTRUCT_TRUNCATED_/u.test(rendered)||!/\[SOURCE_CONSTRUCT\][\s\S]*renderer_truncated=false/u.test(rendered))throw Error('SOURCE_CONSTRUCT_TRUNCATION_FLAG');
  return rendered;
}
export function leakageErrors(value,at='$',errors=[]){if(Array.isArray(value))value.forEach((x,i)=>leakageErrors(x,`${at}[${i}]`,errors));else if(value&&typeof value==='object')for(const [k,v]of Object.entries(value)){if(bannedKey.test(k))errors.push(`BANNED_KEY:${at}.${k}`);leakageErrors(v,`${at}.${k}`,errors)}else if(typeof value==='string'&&explicitLeak.test(value))errors.push(`BANNED_TEXT:${at}`);return errors}
export function scanRequestBytes(bytes){const text=Buffer.isBuffer(bytes)?bytes.toString('utf8'):String(bytes),errors=[];if(explicitLeak.test(text))errors.push('BANNED_TEXT');for(const marker of internalMarkers)if(text.includes(marker))errors.push(`INTERNAL_MARKER:${marker}`);return errors}
export function buildRequest({prompt,schema,items,withContext}){
  if(typeof prompt!=='string'||!prompt.trim()||!schema||typeof schema!=='object')throw Error('PROMPT_SCHEMA');
  if(!Array.isArray(items)||items.length!==16)throw Error('SHARD_SIZE');
  const outbound={items:items.map((x,i)=>{const keys=['item_id','source','target',...(withContext?['source_context']:[])];if(!exactKeys(x,keys))throw Error(`UNSANITIZED_KEYS:${i}`);for(const k of keys)if(typeof x[k]!=='string'||!x[k])throw Error(`INVALID_FIELD:${i}:${k}`);if(withContext&&!x.source_context.includes(x.source))throw Error(`SOURCE_CONTEXT_OMITS_SOURCE:${i}`);return Object.fromEntries(keys.map(k=>[k,x[k]]))})};
  const errors=leakageErrors(outbound);if(errors.length)throw Error(`MODEL_FACING_LEAK:${errors.join(',')}`);
  const text=`${prompt.trim()}\n\nINPUT JSON:\n${JSON.stringify(outbound)}\n\nOUTPUT SCHEMA:\n${JSON.stringify(schema)}\n`,size=Buffer.byteLength(text);
  if(size>REQUEST_MAX_UTF8_BYTES)throw Error(`REQUEST_SIZE_BOUND:${size}`);
  const finalErrors=scanRequestBytes(text);if(finalErrors.length)throw Error(`FINAL_REQUEST_LEAK:${finalErrors.join(',')}`);
  return{outbound,request:Buffer.from(text),request_sha256:sha256(text),utf8_bytes:size};
}
