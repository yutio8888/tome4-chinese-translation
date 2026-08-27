import fs from "node:fs";import path from "node:path";import {spawnSync} from "node:child_process";
const [phase,participant]=process.argv.slice(2),root="/home/yun/research/tome4-agent-eval",dir=path.join(root,"evidence/quality/model-probes/discussion-codex-gemini-b4-v1");
const schema=path.join(root,"evidence/quality/model-probes/gemini-reviewer-holdout-b7-v1/REVIEWER-SCHEMA-24.json");
const input=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/p1-batches/p1-b4-mechanics-numeric.json"),"utf8"));
const r1c=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/model-probes/non-args-reviewer-model-comparison-b4-v1/RAW-codex-baseline.json"),"utf8")).response;
const r1g=JSON.parse(fs.readFileSync(path.join(root,"evidence/quality/model-probes/gemini-reviewer-holdout-b4-v1/RAW-C.json"),"utf8")).response;
let prompt,route=participant,schemaRequired=false;
if(phase==="discuss"&&["codex","gemini"].includes(participant)){
 const own=participant==="codex"?r1c:r1g,peer=participant==="codex"?r1g:r1c,peerName=participant==="codex"?"Gemini":"Codex";
 prompt=`你正在与 ${peerName} 讨论一批翻译审核。以下有原始条目、你的独立首审和对方首审。中间讨论不要求 JSON，也不必重述 24 条。请用自由文本集中讨论：双方分歧、对方可能正确的新证据、对方明显误报、双方共同盲点，以及你建议主席最终标记的 revision_id。逐项引用 source/target 证据；对证据不足的意见明确保留，不要为了达成一致而迎合。不要调用工具。\n你的首审：\n${JSON.stringify(own)}\n对方首审：\n${JSON.stringify(peer)}\n原始条目：\n${JSON.stringify(input)}`;
}else if(phase==="chair"&&participant==="codex"){
 const dc=fs.readFileSync(path.join(dir,"RAW-free-discuss-codex.txt"),"utf8"),dg=fs.readFileSync(path.join(dir,"RAW-free-discuss-gemini.txt"),"utf8");schemaRequired=true;
 prompt=`你是双模型审核讨论的主席。Codex 与 Gemini 已独立首审并交换了自由文本意见。讨论内容不是权威答案；逐条根据原始 source/target 裁决，避免意见传染。只确认有直接文本证据且会改变机制或明确含义的问题，纯风格或证据不足判 OK。\nCodex 首审：${JSON.stringify(r1c)}\nGemini 首审：${JSON.stringify(r1g)}\nCodex 自由讨论：\n${dc}\nGemini 自由讨论：\n${dg}\n原始条目：${JSON.stringify(input)}\n最终严格输出 schema JSON，按输入顺序覆盖全部 24 条。`;route="codex";
}else throw new Error("usage: discuss codex|gemini OR chair codex");
let command,args,last;
if(route==="codex"){command="codex";last=`/tmp/free-${phase}-${participant}.txt`;args=["exec","-m","gpt-5.6-sol","-c","model_reasoning_effort=\"high\"","--ephemeral","--ignore-rules","--skip-git-repo-check","-o",last,"-C","/tmp","-s","read-only"];if(schemaRequired)args.push("--output-schema",schema);args.push(prompt);}
else{command="agy";args=["-p",prompt,"--model","gemini-3.7-flash-high","--effort","high","--disable-slash-commands","--output-format","json","--print-timeout","15m","--mode","plan"];}
const started=Date.now(),run=spawnSync(command,args,{cwd:"/tmp",encoding:"utf8",maxBuffer:64*1024*1024,timeout:20*60*1000,env:{...process.env,NO_COLOR:"1"}});
if(phase==="discuss"){
 let text;if(route==="codex")text=fs.readFileSync(last,"utf8");else{text=JSON.parse(run.stdout).response;}fs.writeFileSync(path.join(dir,`RAW-free-discuss-${participant}.txt`),text);console.log(JSON.stringify({phase,participant,duration_seconds:(Date.now()-started)/1000,exit_status:run.status,chars:text.length}));
}else{
 const response=JSON.parse(fs.readFileSync(last,"utf8")),result={phase,participant,duration_seconds:(Date.now()-started)/1000,exit_status:run.status,valid:response.revisions?.length===24,response};fs.writeFileSync(path.join(dir,"RAW-free-chair-codex.json"),JSON.stringify(result,null,2)+"\n");console.log(JSON.stringify({...result,response:undefined}));
}
