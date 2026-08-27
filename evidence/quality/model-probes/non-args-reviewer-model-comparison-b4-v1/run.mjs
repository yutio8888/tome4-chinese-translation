import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";

const [route,name]=process.argv.slice(2);
const root="/home/yun/research/tome4-agent-eval";
const outDir=path.join(root,"evidence/quality/model-probes/non-args-reviewer-model-comparison-b4-v1");
const promptDir=path.join(root,"evidence/quality/model-probes/gemini-reviewer-prompt-search-v1");
const input=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/p1-batches/p1-b4-mechanics-numeric.json"),"utf8"));
const reference=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/p1-batches/p1-b4-s2-verification.json"),"utf8"));
const schemaPath=path.join(root,"evidence/quality/model-probes/gemini-reviewer-holdout-b7-v1/REVIEWER-SCHEMA-24.json");
const prompts={baseline:path.join(root,"evidence/quality/model-probes/qwen3-8-27b-p1-b8/PROMPT.md"),A:path.join(promptDir,"PROMPT-A-SEMANTIC-SLOTS.md"),B:path.join(promptDir,"PROMPT-B-TWO-PASS-RECALL.md"),C:path.join(promptDir,"PROMPT-C-CLAIM-ATOMS.md"),D:path.join(promptDir,"PROMPT-D-RELATION-LEDGER.md")};
if(!["grok","codex"].includes(route)||!prompts[name])throw new Error("usage: run.mjs grok|codex baseline|A|B|C|D");
const prompt=fs.readFileSync(prompts[name],"utf8").replaceAll("21 条","24 条").replaceAll("全部 21 条","全部 24 条")+"\n输入 JSON：\n"+JSON.stringify(input);
let command,args,lastPath;
if(route==="grok"){
  command="grok"; args=["-p",prompt,"--model","grok-4.6","--no-subagents","--disable-web-search","--cwd","/tmp","--output-format","plain","--max-turns","1","--tools","","--json-schema",fs.readFileSync(schemaPath,"utf8")];
}else{
  command="codex"; lastPath=`/tmp/codex-b4-${name}-last.json`; args=["exec","-m","gpt-5.6-sol","-c","model_reasoning_effort=\"high\"","--ephemeral","--ignore-rules","--skip-git-repo-check","-o",lastPath,"-C","/tmp","-s","read-only","--output-schema",schemaPath,prompt];
}
const started=Date.now();
const run=spawnSync(command,args,{cwd:"/tmp",encoding:"utf8",maxBuffer:64*1024*1024,timeout:20*60*1000,env:{...process.env,NO_COLOR:"1"}});
const result={route,variant:name,duration_seconds:(Date.now()-started)/1000,exit_status:run.status};
try{
  const text=route==="codex"&&fs.existsSync(lastPath)?fs.readFileSync(lastPath,"utf8"):run.stdout;
  const parsed=JSON.parse(text); const candidate=parsed.revisions ? parsed : JSON.parse(parsed.text); const orderedIds=input.items.map(x=>x.revision_id);
  const defectIds=new Set(reference.items.filter(x=>(x.verdict??x.decision)==="defect").map(x=>x.revision_id));
  const ids=candidate.revisions.map(x=>x.revision_id); const predicted=new Set(candidate.revisions.filter(x=>x.observation!=="OK").map(x=>x.revision_id));
  let tp=0,fp=0,fn=0,tn=0; for(const id of orderedIds){if(defectIds.has(id)&&predicted.has(id))tp++;else if(!defectIds.has(id)&&predicted.has(id))fp++;else if(defectIds.has(id))fn++;else tn++;}
  Object.assign(result,{valid:ids.length===24&&ids.every((id,i)=>id===orderedIds[i]),tp,fp,fn,tn,recall:tp/(tp+fn),precision:tp+fp?tp/(tp+fp):null,clean_false_positive_rate:fp/(fp+tn),predicted_defect_ids:[...predicted],response:candidate});
}catch(error){Object.assign(result,{valid:false,error:String(error),stdout:run.stdout,stderr:run.stderr});}
fs.writeFileSync(path.join(outDir,`RAW-${route}-${name}.json`),JSON.stringify(result,null,2)+"\n");
process.stdout.write(JSON.stringify({...result,response:undefined,stdout:undefined,stderr:undefined})+"\n");
