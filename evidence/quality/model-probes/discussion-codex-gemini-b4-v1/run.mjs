import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
const [phase,participant]=process.argv.slice(2);
const root="/home/yun/research/tome4-agent-eval",dir=path.join(root,"evidence/quality/model-probes/discussion-codex-gemini-b4-v1");
const schema=path.join(root,"evidence/quality/model-probes/gemini-reviewer-holdout-b7-v1/REVIEWER-SCHEMA-24.json");
const input=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/p1-batches/p1-b4-mechanics-numeric.json"),"utf8"));
const r1c=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/model-probes/non-args-reviewer-model-comparison-b4-v1/RAW-codex-baseline.json"),"utf8")).response;
const r1g=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/model-probes/gemini-reviewer-holdout-b4-v1/RAW-C.json"),"utf8")).response;
const common=`你正在参与双模型翻译审核讨论。对方意见只是待核验证据，不是权威答案；不得因对方提出问题就自动接受，也不得为维持自己原判而拒绝。逐条比较 source、target 及可用 args_order，只报告会改变机制或明确文本含义的实质问题，纯风格偏好判 OK。不要调用工具。\n最终仅输出 schema 所要求的 JSON，严格按输入顺序覆盖全部 24 条。`;
let prompt,route=participant;
if(phase==="reconsider"&&participant==="codex") prompt=common+`\n这是你自己的独立首审：\n${JSON.stringify(r1c)}\n这是 Gemini 的独立首审：\n${JSON.stringify(r1g)}\n请重新审议全部条目。对每个分歧独立核对原文后给出修订结论。\n输入：\n${JSON.stringify(input)}`;
else if(phase==="reconsider"&&participant==="gemini") prompt=common+`\n这是你自己的独立首审：\n${JSON.stringify(r1g)}\n这是 Codex 的独立首审：\n${JSON.stringify(r1c)}\n请重新审议全部条目。对每个分歧独立核对原文后给出修订结论。\n输入：\n${JSON.stringify(input)}`;
else if(phase==="synthesize"&&participant==="codex"){
 const r2c=JSON.parse(fs.readFileSync(path.join(dir,"RAW-reconsider-codex.json"),"utf8")).response;
 const r2g=JSON.parse(fs.readFileSync(path.join(dir,"RAW-reconsider-gemini.json"),"utf8")).response;
 prompt=`你是双模型审核讨论的主席。以下两份是 Codex 与 Gemini 在交换首审意见后的独立复议结果。逐条处理分歧：共识仍需核验证据；分歧时比较双方 evidence 与原始 source/target，不按多数、模型身份或更严厉的一方机械裁决。只确认有直接文本证据的实质问题；纯风格或证据不足判 OK。不要调用工具。\nCodex 复议：\n${JSON.stringify(r2c)}\nGemini 复议：\n${JSON.stringify(r2g)}\n原始输入：\n${JSON.stringify(input)}\n最终仅输出 schema JSON，按输入顺序覆盖 24 条。`; route="codex";
}else throw new Error("usage: reconsider codex|gemini OR synthesize codex");
let command,args,last;
if(route==="codex"){command="codex";last=`/tmp/discussion-${phase}-${participant}.json`;args=["exec","-m","gpt-5.6-sol","-c","model_reasoning_effort=\"high\"","--ephemeral","--ignore-rules","--skip-git-repo-check","-o",last,"-C","/tmp","-s","read-only","--output-schema",schema,prompt];}
else{command="agy";args=["-p",prompt,"--model","gemini-3.7-flash-high","--effort","high","--disable-slash-commands","--output-format","json","--print-timeout","15m","--mode","plan","--json-schema",schema];}
const started=Date.now(),run=spawnSync(command,args,{cwd:"/tmp",encoding:"utf8",maxBuffer:64*1024*1024,timeout:20*60*1000,env:{...process.env,NO_COLOR:"1"}});
const result={phase,participant,duration_seconds:(Date.now()-started)/1000,exit_status:run.status};
try{let response;if(route==="codex")response=JSON.parse(fs.readFileSync(last,"utf8"));else{const env=JSON.parse(run.stdout);response=env.structured_output??JSON.parse(env.response);result.usage=env.usage;} result.valid=response.revisions?.length===24;result.response=response;}
catch(error){Object.assign(result,{valid:false,error:String(error),stdout:run.stdout,stderr:run.stderr});}
fs.writeFileSync(path.join(dir,`RAW-${phase}-${participant}.json`),JSON.stringify(result,null,2)+"\n");
process.stdout.write(JSON.stringify({...result,response:undefined,stdout:undefined,stderr:undefined})+"\n");
