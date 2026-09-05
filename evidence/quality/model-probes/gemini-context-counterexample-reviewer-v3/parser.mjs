import {toolSignal,validateReviewerResponse,exactKeys} from './lib.mjs';

export function parseEnvelope(raw,input){
  const errors=[];let env=null,response=null;
  try{env=JSON.parse(raw)}catch(e){return{valid:false,errors:[`envelope JSON: ${e.message}`],response:null,identity:'REQUESTED_ROUTE_ONLY_UNVERIFIED'}}
  if(!exactKeys(input,['items'])||!Array.isArray(input.items))errors.push('input schema');
  if(env?.status!=='SUCCESS')errors.push('envelope status');
  if(toolSignal(env))errors.push('recursive tool signal');
  // agy's request echo and agent/requested_model metadata are never runtime attestation.
  const attested=env?.runtime?.model_attestation;
  if(attested!=null&&attested!=='gemini-3.7-flash-high')errors.push('runtime route mismatch');
  if(env?.structured_output&&typeof env.structured_output==='object')response=env.structured_output;
  else if(typeof env?.response==='string'){try{response=JSON.parse(env.response)}catch(e){errors.push(`structured response JSON: ${e.message}`)}}
  else errors.push('missing structured response');
  const ids=(input.items??[]).map(x=>x.item_id);
  if(response)errors.push(...validateReviewerResponse(response,ids));
  if(response?.items)response.items.forEach((x,i)=>x.candidates?.forEach((c,j)=>{
    const item=input.items[i];
    if(!item||!item.target.includes(c.target_span))errors.push(`item ${i} candidate ${j}: target evidence membership`);
    // The same evidence rule applies to every arm: evidence must be a source or target substring.
    // Context supports judgment but is never accepted as candidate evidence by itself.
    if(!item||(!item.source.includes(c.evidence)&&!item.target.includes(c.evidence)))errors.push(`item ${i} candidate ${j}: evidence membership`);
  }));
  return{valid:errors.length===0,errors,response:errors.length?null:response,identity:attested==='gemini-3.7-flash-high'?'RUNTIME_MODEL_ATTESTED':'REQUESTED_ROUTE_ONLY_UNVERIFIED'};
}
