import {decodeUtf8,exactKeys,parseNoDuplicate,sha256} from './lib.mjs';
const CLAIMS=new Set(['SUBJECT','REFERENT','EVENT','CONDITION','SCOPE','DIRECTION','POLARITY','OWNERSHIP','ACTION','STATE','TIMING','OMISSION','ADDITION','FORMAT','OTHER']);
const type=v=>v===null?'null':Array.isArray(v)?'array':typeof v;
export function extractAgy(stdout){
  const envelope=parseNoDuplicate(decodeUtf8(stdout,'AGY'),'AGY');
  if(!envelope||typeof envelope!=='object'||Array.isArray(envelope))throw Error('AGY_ENVELOPE_OBJECT');
  if(envelope.status!=='SUCCESS')throw Error('AGY_ENVELOPE_STATUS');
  if(!Object.hasOwn(envelope,'structured_output'))throw Error('AGY_STRUCTURED_MISSING');
  const payload=envelope.structured_output;if(!payload||typeof payload!=='object'||Array.isArray(payload))throw Error('AGY_STRUCTURED_TYPE');
  const present=Object.hasOwn(envelope,'response'),response=present?envelope.response:undefined,isString=present&&typeof response==='string';
  return{payload,envelope_metadata:{authoritative_channel:'structured_output',response_present:present,response_type:present?type(response):null,response_utf8_bytes:isString?Buffer.byteLength(response,'utf8'):null,response_sha256:isString?sha256(Buffer.from(response)):null}};
}
export function parseOutput(output,input,condition){
  const errors=[],ids=input.items.map(x=>x.item_id),field=condition==='hardened'?'evidence_quote':'evidence';
  if(!exactKeys(output,['items'])||!Array.isArray(output.items)||output.items.length!==24)return{valid:false,errors:['OUTPUT_ITEMS'],normalized:null};
  const rows=[];
  output.items.forEach((item,i)=>{
    if(!exactKeys(item,['item_id','candidates'])||item.item_id!==ids[i]||!Array.isArray(item.candidates)||item.candidates.length>4){errors.push(`ITEM:${i}`);return;}
    const row={item_id:item.item_id,candidates:[]};
    item.candidates.forEach((c,j)=>{
      if(!exactKeys(c,['verdict','claim_type','target_span','correction',field])||!['FINDING','UNCERTAIN'].includes(c.verdict)||!CLAIMS.has(c.claim_type)){errors.push(`CANDIDATE:${i}:${j}`);return;}
      for(const k of ['target_span','correction',field])if(typeof c[k]!=='string'||[...c[k]].length<1||[...c[k]].length>500)errors.push(`FIELD:${i}:${j}:${k}`);
      row.candidates.push({verdict:c.verdict,claim_type:c.claim_type,target_span:c.target_span,correction:c.correction,evidence:c[field]});
    });rows.push(row);
  });
  return{valid:errors.length===0,errors,normalized:errors.length?null:{items:rows}};
}
export function parseCapture(stdout,input,condition){try{const x=extractAgy(stdout),p=parseOutput(x.payload,input,condition);return{...p,envelope_metadata:p.valid?x.envelope_metadata:null};}catch(e){return{valid:false,errors:[e.message],normalized:null,envelope_metadata:null};}}
