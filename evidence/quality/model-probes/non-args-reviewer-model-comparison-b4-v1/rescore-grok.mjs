import fs from "node:fs";
import path from "node:path";
const root="/home/yun/research/tome4-agent-eval",dir=path.join(root,"evidence/quality/model-probes/non-args-reviewer-model-comparison-b4-v1");
const input=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/p1-batches/p1-b4-mechanics-numeric.json"),"utf8"));
const ref=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/p1-batches/p1-b4-s2-verification.json"),"utf8"));
const ordered=input.items.map(x=>x.revision_id), defects=new Set(ref.items.filter(x=>x.decision==="defect").map(x=>x.revision_id));
for(const file of fs.readdirSync(dir).filter(x=>x.startsWith("RAW-grok-")&&x.endsWith(".json"))){
 const old=JSON.parse(fs.readFileSync(path.join(dir,file),"utf8"));
 try{
  const wrapped=JSON.parse(old.stdout),candidate=JSON.parse(wrapped.text),ids=candidate.revisions.map(x=>x.revision_id);
  const predicted=new Set(candidate.revisions.filter(x=>x.observation!=="OK").map(x=>x.revision_id)); let tp=0,fp=0,fn=0,tn=0;
  for(const id of ordered){if(defects.has(id)&&predicted.has(id))tp++;else if(!defects.has(id)&&predicted.has(id))fp++;else if(defects.has(id))fn++;else tn++;}
  const result={route:"grok",variant:old.variant,duration_seconds:old.duration_seconds,exit_status:old.exit_status,valid:ids.length===24&&ids.every((id,i)=>id===ordered[i]),tp,fp,fn,tn,recall:tp/(tp+fn),precision:tp+fp?tp/(tp+fp):null,clean_false_positive_rate:fp/(fp+tn),predicted_defect_ids:[...predicted],response:candidate};
  fs.writeFileSync(path.join(dir,file),JSON.stringify(result,null,2)+"\n"); process.stdout.write(JSON.stringify({...result,response:undefined})+"\n");
 }catch(error){process.stdout.write(JSON.stringify({file,valid:false,error:String(error)})+"\n");}
}
