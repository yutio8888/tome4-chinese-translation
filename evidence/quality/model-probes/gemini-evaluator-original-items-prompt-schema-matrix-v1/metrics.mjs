const prose=/[.!?。！？]|because|since|therefore|means|indicates|shows|the translation|the source|the target|因为|所以|说明|表示|译文|原文/iu;
const CONDITION_IDS=['p0-s0','p0-s2','p1-s0','p1-s2'];
const REPETITIONS=[1,2,3];
const finiteRate=value=>typeof value==='number'&&Number.isFinite(value);

export function metrics(normalized,input){
  const source=new Map(input.items.map(x=>[x.item_id,x])),all=[];
  for(const row of normalized.items)for(const c of row.candidates){
    const item=source.get(row.item_id),member=item.source.includes(c.evidence)||item.target.includes(c.evidence);
    all.push({...c,member,targetMember:item.target.includes(c.target_span),registered:c.emitted_evidence_field===c.registered_evidence_field,proxy:prose.test(c.evidence)});
  }
  const n=all.length,ev=all.filter(x=>x.member).length,ts=all.filter(x=>x.targetMember).length,reg=all.filter(x=>x.registered).length,pv=all.filter(x=>x.member&&x.proxy).length,pi=all.filter(x=>!x.member&&x.proxy).length;
  return{status:n?'DESCRIPTIVE':'UNINFORMATIVE_ZERO_CANDIDATES',candidate_count:n,evidence_membership_count:ev,evidence_membership_rate:n?ev/n:null,source_target_only_evidence_membership_count:ev,source_target_only_evidence_membership_rate:n?ev/n:null,target_span_membership_count:ts,target_span_membership_rate:n?ts/n:null,registered_field_name_count:reg,registered_field_name_rate:n?reg/n:null,evidence_mean_utf16_length:n?all.reduce((s,x)=>s+x.evidence.length,0)/n:null,explanatory_prose_proxy_membership_valid_count:pv,explanatory_prose_proxy_membership_invalid_count:pi,explanatory_prose_proxy_total_count:pv+pi};
}

export function aggregateCondition(runs){
  const informative=runs.filter(x=>x.metrics?.candidate_count>0&&finiteRate(x.metrics?.evidence_membership_rate));
  const n=runs.reduce((s,x)=>s+(x.metrics?.candidate_count??0),0),ev=runs.reduce((s,x)=>s+(x.metrics?.evidence_membership_count??0),0),rates=informative.map(x=>x.metrics.evidence_membership_rate);
  return{run_count:runs.length,informative_run_count:informative.length,candidate_count:n,evidence_membership_count:ev,micro_evidence_membership_rate:n?ev/n:null,unweighted_run_mean_evidence_membership_rate:rates.length?rates.reduce((a,b)=>a+b,0)/rates.length:null,fully_conformant_informative_run_count:informative.filter(x=>x.metrics.evidence_membership_rate===1).length,evidence_membership_rate_range:rates.length?{min:Math.min(...rates),max:Math.max(...rates),range:Math.max(...rates)-Math.min(...rates)}:null};
}

export function summarize(runs,complete){
  const conditions=Object.fromEntries(CONDITION_IDS.map(id=>{const rs=runs.filter(x=>x.condition===id);return[id,{runs:rs,aggregate:aggregateCondition(rs)}]}));
  const matrixInformative=complete&&runs.length===12&&CONDITION_IDS.every(id=>{
    const rs=conditions[id].runs;
    return rs.length===3&&REPETITIONS.every(repetition=>rs.filter(x=>x.repetition===repetition).length===1)&&rs.every(x=>x.metrics?.candidate_count>0&&finiteRate(x.metrics?.evidence_membership_rate));
  });
  const mean=id=>conditions[id].aggregate.unweighted_run_mean_evidence_membership_rate;
  const diff=(a,b)=>finiteRate(mean(a))&&finiteRate(mean(b))?mean(a)-mean(b):null;
  const nullContrasts={prompt_within_s0:null,prompt_within_s2:null,schema_within_p0:null,schema_within_p1:null,difference_in_differences:null};
  let interpretation='INCOMPLETE_MATRIX';
  if(matrixInformative){
    const vals=CONDITION_IDS.map(mean);
    if(vals.every(x=>x===vals[0]))interpretation='DESCRIPTIVE_MATRIX_NO_OBSERVED_DIFFERENCE';
    else{
      const byRepetition=(id,repetition)=>conditions[id].runs.find(x=>x.repetition===repetition)?.metrics?.evidence_membership_rate;
      const paired=REPETITIONS.every(repetition=>{const p1=byRepetition('p1-s2',repetition),p0=byRepetition('p0-s0',repetition);return finiteRate(p1)&&finiteRate(p0)&&p1>p0});
      const gain=conditions['p1-s2'].aggregate.fully_conformant_informative_run_count===3&&conditions['p0-s0'].aggregate.fully_conformant_informative_run_count<3;
      interpretation=paired&&gain?'DESCRIPTIVE_COMBINED_CONTRACT_GAIN_OBSERVED':'DESCRIPTIVE_MATRIX_MIXED';
    }
  }
  const contrasts=matrixInformative?{prompt_within_s0:diff('p1-s0','p0-s0'),prompt_within_s2:diff('p1-s2','p0-s2'),schema_within_p0:diff('p0-s2','p0-s0'),schema_within_p1:diff('p1-s2','p1-s0'),difference_in_differences:(mean('p1-s2')-mean('p0-s2'))-(mean('p1-s0')-mean('p0-s0'))}:nullContrasts;
  return{conditions,contrasts,interpretation};
}
