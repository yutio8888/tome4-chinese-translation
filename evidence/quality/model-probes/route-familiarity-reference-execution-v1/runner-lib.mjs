import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {spawnSync} from "node:child_process";
import {createRequire} from "node:module";

const require = createRequire(import.meta.url);
const Ajv2020 = require("ajv/dist/2020").default;

export const BASELINE = "d94e2d51e7fe7fd8162e4c0666a2df1102e81426";
export const EXECUTOR_FIXTURE_SHA256 = "82e25a395c1c9ff16c5b487ff465bc4bc7824e7cc61bebe4e8e716c24469b4c7";
export const TIMEOUT_MS = 30 * 60 * 1000;
export const MAX_ATTEMPTS = 2;
export const ROUTES = {
  codex: {lane_id:"lane-01", slug:"codex-gpt-5.6-sol-high", kind:"codex", command:"codex", version:"codex-cli 0.150.1", model:"gpt-5.6-sol", effort:"high", qualification:"EXPLORATORY_NON_ISOLATED_REFERENCE"},
  claude: {lane_id:"lane-02", slug:"claude-opus-5-high-exploratory", kind:"claude", command:"claude", version:"2.1.250 (Claude Code)", model:"claude-opus-5", effort:"high", qualification:"EXPLORATORY_FORMAL_PURITY_NO_GO"},
  gemini: {lane_id:"lane-03", slug:"agy-gemini-3.7-flash-high", kind:"agy", command:"agy", version:"1.1.22", model:"gemini-3.7-flash-high", effort:"high", qualification:"EXPLORATORY_NON_ISOLATED_REFERENCE"},
  glm: {lane_id:"lane-04", slug:"pi-zai-cn-glm-5.3-flash-high", kind:"pi", command:"pi", version:"0.84.3", model:"glm-5.3-flash", provider:"zai-standard-cn", effort:"high", qualification:"EXPLORATORY_NON_ISOLATED_REFERENCE"}
};
export const SHARDS = [1,2,3,4,5];

export const assert = (value, message) => { if (!value) throw new Error(message); };
export const sha256Bytes = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
export const sha256File = file => sha256Bytes(fs.readFileSync(file));
export const readJson = file => JSON.parse(fs.readFileSync(file, "utf8"));
export function writeNew(file, bytes) { fs.mkdirSync(path.dirname(file), {recursive:true}); const fd=fs.openSync(file,"wx",0o600); try { fs.writeFileSync(fd,bytes); } finally { fs.closeSync(fd); } }
export const shardName = n => `SHARD-${String(n).padStart(2,"0")}`;
export const shardFile = n => `OUTBOUND-${shardName(n)}.json`;
export const schemaFile = n => `RESPONSE-SCHEMA-${shardName(n)}.json`;
export function paths(here) { const repo=path.resolve(here,"../../../.."); return {repo, predecessor:path.join(repo,"evidence/quality/model-probes/route-familiarity-reference-collection-v1")}; }

export function frozenBindings(here) {
  const {predecessor}=paths(here); const manifest=readJson(path.join(predecessor,"LOCAL-ROUTE-MANIFEST.json"));
  const names=["BUILD-REPORT.json","EXPERIMENT.json","LOCAL-ROUTE-MANIFEST.json","PROMPT.md",...SHARDS.flatMap(n=>[shardFile(n),schemaFile(n)]),"README.md","build.mjs","test-builder.mjs","verify.mjs"];
  return {manifest, files:Object.fromEntries(names.sort().map(name=>[name,{logical_path:`evidence/quality/model-probes/route-familiarity-reference-collection-v1/${name}`,sha256:sha256File(path.join(predecessor,name)),size_bytes:fs.statSync(path.join(predecessor,name)).size}]))};
}

const FORBIDDEN=[[/\/(?:home|Users|root|tmp|opt|var|mnt)\//u,"local absolute path"],[/(?:SEALED|adjudicat|defect_id|model_provenance|LOCAL-ROUTE-MANIFEST)/iu,"sealed/local field"],[/(?:API[_-]?KEY|AUTHORIZATION\s*:\s*BEARER|credential)/iu,"credential marker"]];
export function requestBytes(here,n) { const {predecessor}=paths(here); return Buffer.concat([fs.readFileSync(path.join(predecessor,"PROMPT.md")),Buffer.from("\nINPUT JSON:\n"),fs.readFileSync(path.join(predecessor,shardFile(n)))]); }
export function outboundFiles(here,n) { const {predecessor}=paths(here); return [{name:"PROMPT.md",bytes:fs.readFileSync(path.join(predecessor,"PROMPT.md"))},{name:shardFile(n),bytes:fs.readFileSync(path.join(predecessor,shardFile(n)))},{name:schemaFile(n),bytes:fs.readFileSync(path.join(predecessor,schemaFile(n)))}]; }
export function scanOutbound(items) { const errors=[]; for(const item of items) for(const [pattern,label] of FORBIDDEN) if(pattern.test(item.bytes.toString("utf8"))) errors.push(`${item.name}: ${label}`); return errors; }
export function makeBundle(here,n) { const dir=fs.mkdtempSync(path.join(os.tmpdir(),"rfr-bundle-")); for(const item of outboundFiles(here,n)) writeNew(path.join(dir,item.name),item.bytes); assert(scanOutbound(outboundFiles(here,n)).length===0,"outbound sanitization failure"); return dir; }

function copySecret(source,dest) { const stat=fs.lstatSync(source); assert(stat.isFile()&&!stat.isSymbolicLink(),"route auth is unavailable or unsafe"); fs.mkdirSync(path.dirname(dest),{recursive:true,mode:0o700}); fs.copyFileSync(source,dest,fs.constants.COPYFILE_EXCL); fs.chmodSync(dest,0o600); }
export function makeRuntime(route) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),"rfr-runtime-")); fs.chmodSync(root,0o700); fs.mkdirSync(path.join(root,"home"),{mode:0o700}); fs.mkdirSync(path.join(root,"tmp"),{mode:0o700}); fs.mkdirSync(path.join(root,"bin"),{mode:0o700});
  const host=os.homedir(); const home=path.join(root,"home");
  if(route.kind==="codex") copySecret(path.join(host,".codex","auth.json"),path.join(home,".codex","auth.json"));
  if(route.kind==="claude") copySecret(path.join(host,".claude",".credentials.json"),path.join(home,".claude",".credentials.json"));
  if(route.kind==="agy") copySecret(path.join(host,".gemini","antigravity-cli","antigravity-oauth-token"),path.join(home,".gemini","antigravity-cli","antigravity-oauth-token"));
  if(route.kind==="pi") {
    const auth=readJson(path.join(host,".pi","agent","auth.json")); const models=readJson(path.join(host,".pi","agent","models.json"));
    assert(auth[route.provider]?.type==="api_key","Pi route auth unavailable"); const provider=structuredClone(models.providers?.[route.provider]); assert(provider,"Pi route config unavailable"); delete provider.apiKey; provider.models=provider.models.filter(m=>m.id===route.model); assert(provider.models.length===1,"Pi model unavailable");
    writeNew(path.join(home,".pi","agent","auth.json"),`${JSON.stringify({[route.provider]:auth[route.provider]})}\n`); writeNew(path.join(home,".pi","agent","models.json"),`${JSON.stringify({providers:{[route.provider]:provider}})}\n`);
  }
  if(["claude","agy"].includes(route.kind)) writeNew(path.join(root,"bin",route.command),"");
  return root;
}
export function removeTemp(dir,prefix) { assert(path.dirname(dir)===os.tmpdir()&&path.basename(dir).startsWith(prefix),`unsafe temporary cleanup ${dir}`); fs.rmSync(dir,{recursive:true,force:false}); }
export function envFor(route) { const names=["PATH","LANG","LC_ALL","LC_CTYPE","TZ","TERM","SSL_CERT_FILE","SSL_CERT_DIR","HTTPS_PROXY","HTTP_PROXY","ALL_PROXY","NO_PROXY"]; const env={}; for(const n of names) if(typeof process.env[n]==="string") env[n]=process.env[n]; env.PATH=`/tmp/route-runtime/bin:${env.PATH??"/usr/local/bin:/usr/bin:/bin"}`; env.HOME="/tmp/route-runtime/home"; env.TMPDIR="/tmp/route-runtime/tmp"; env.XDG_CONFIG_HOME="/tmp/route-runtime/home/.config"; env.XDG_CACHE_HOME="/tmp/route-runtime/home/.cache"; env.XDG_STATE_HOME="/tmp/route-runtime/home/.local/state"; env.NO_COLOR="1"; if(route.kind==="pi") {env.PI_SKIP_VERSION_CHECK="1";env.PI_TELEMETRY="0";} return env; }

export function plan(route,n,request,bundle,runtime) {
  const schema=schemaFile(n); const exactSchemaText=fs.readFileSync(path.join(bundle,schema),"utf8"); const compatibilitySchema=JSON.parse(exactSchemaText); delete compatibilitySchema.$schema; delete compatibilitySchema.$id; delete compatibilitySchema.title; delete compatibilitySchema.$defs.referenceResponse.allOf; compatibilitySchema.properties.items.items={"$ref":"#/$defs/referenceItem"}; delete compatibilitySchema.properties.items.prefixItems; delete compatibilitySchema.properties.item_ids.const; compatibilitySchema.properties.item_ids.type="array"; compatibilitySchema.properties.item_ids.minItems=29; compatibilitySchema.properties.item_ids.maxItems=29; compatibilitySchema.properties.item_ids.items={type:"string"}; const normalizeTransport=value=>{if(!value||typeof value!=="object")return;delete value.uniqueItems;if(value.const!==undefined&&!value.type)value.type=Number.isInteger(value.const)?"integer":typeof value.const;if(value.enum&&!value.type)value.type="string";for(const child of Object.values(value))if(Array.isArray(child))child.forEach(normalizeTransport);else normalizeTransport(child);};normalizeTransport(compatibilitySchema);const compatibilitySchemaText=JSON.stringify(compatibilitySchema); let args;
  if(route.kind==="codex"){writeNew(path.join(runtime,"transport-schema.json"),`${compatibilitySchemaText}\n`);const disabled=["shell_tool","unified_exec","apps","browser_use","browser_use_external","browser_use_full_cdp_access","computer_use","multi_agent","multi_agent_v2","plugins","plugin_sharing","remote_plugin","skill_search","view_image","image_generation","hooks","goals","tool_suggest","tool_call_mcp_elicitation","workspace_dependencies"].flatMap(x=>["--disable",x]);args=[...disabled,"-a","never","exec","-m",route.model,"-c",`model_reasoning_effort=\"${route.effort}\"`,"--ephemeral","--ignore-user-config","--ignore-rules","--skip-git-repo-check","-C","/mnt","-s","read-only","--output-schema","/tmp/route-runtime/transport-schema.json","--json","-o","/tmp/route-runtime/last-message.json",request.toString("utf8")];}
  else if(route.kind==="claude") args=["--print","--model",route.model,"--effort",route.effort,"--output-format","stream-json","--verbose","--no-session-persistence","--safe-mode","--restricted","--strict-mcp-config","--mcp-config","{\"mcpServers\":{}}","--disable-slash-commands","--permission-mode","plan","--tools","","--json-schema",compatibilitySchemaText,"--",request.toString("utf8")];
  else if(route.kind==="pi") args=["--provider",route.provider,"--model",route.model,"--thinking",route.effort,"--no-tools","--no-session","--no-extensions","--no-skills","--no-prompt-templates","--no-themes","--no-context-files","--no-approve","--mode","json","--print","--",request.toString("utf8")];
  else args=["-p",request.toString("utf8"),"--model",route.model,"--effort",route.effort,"--disable-slash-commands","--output-format","json","--print-timeout","25m","--mode","plan","--sandbox","--json-schema",compatibilitySchemaText];
  return {args,display_args:args.map(x=>x===request.toString("utf8")?"[REQUEST_BYTES]":x===exactSchemaText?"[EXACT_SCHEMA_BYTES]":x===compatibilitySchemaText?"[SCHEMA_COMPATIBILITY_VIEW: annotations/allOf removed and prefixItems generalized; canonical post-validation unchanged]":x)};
}
function resolveExecutable(name){for(const dir of (process.env.PATH??"").split(path.delimiter)){const file=path.join(dir,name);try{if(fs.statSync(file).isFile()||fs.lstatSync(file).isSymbolicLink())return fs.realpathSync(file);}catch{}}throw new Error(`${name}: executable unavailable`);}
export function sandboxCommand(route,bundle,runtime,args) { const privateExe=["claude","agy"].includes(route.kind)?["--ro-bind",resolveExecutable(route.command),`/tmp/route-runtime/bin/${route.command}`]:[]; return {command:"bwrap",args:["--die-with-parent","--new-session","--cap-drop","ALL","--ro-bind","/","/","--dev","/dev","--proc","/proc","--tmpfs",os.homedir(),"--ro-bind",bundle,"/mnt","--tmpfs","/tmp","--dir","/tmp/route-runtime","--bind",runtime,"/tmp/route-runtime",...privateExe,"--chdir","/mnt","--",route.command,...args]}; }

function jsonLines(raw){return raw.split(/\r?\n/u).filter(x=>x.trim()).map(JSON.parse);}
function unwrap(text){const t=text.trim();const m=t.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/iu);return JSON.parse(m?m[1]:t);}
function toolSignal(v){if(!v||typeof v!=="object")return false;if(typeof v.type==="string"&&/(?:tool|command|web|browser|mcp|subagent)/iu.test(v.type))return true;return Object.values(v).some(x=>Array.isArray(x)?x.some(toolSignal):toolSignal(x));}
export function parseRaw(route,raw,lastMessage=null){const errors=[];let response=null,identity={};try{
  if(route.kind==="codex"){const ev=jsonLines(raw);const agents=ev.filter(e=>e.type==="item.completed"&&e.item?.type==="agent_message");if(agents.length!==1)errors.push(`expected one Codex agent message, got ${agents.length}`);if(ev.some(e=>e.item&&!["reasoning","agent_message"].includes(e.item.type)))errors.push("Codex tool/non-message item detected");response=lastMessage?JSON.parse(lastMessage):unwrap(agents.at(-1)?.item?.text??"");identity={requested_model:route.model,reported_models:[...new Set(ev.flatMap(e=>[e.model,e.item?.model]).filter(Boolean))],runtime_identity_status:"REQUESTED_ROUTE_ONLY_CLI_ENVELOPE_UNVERIFIED",usage:ev.find(e=>e.type==="turn.completed")?.usage??null};}
  else if(route.kind==="claude"){const ev=jsonLines(raw),init=ev.filter(e=>e.type==="system"&&e.subtype==="init"),asst=ev.filter(e=>e.type==="assistant"&&e.message),res=ev.filter(e=>e.type==="result");const models=[...new Set(asst.map(e=>e.message.model).filter(Boolean))];if(init.length!==1||res.length!==1)errors.push("Claude init/result cardinality mismatch");if(init[0]?.model!==route.model||JSON.stringify(models)!==JSON.stringify([route.model]))errors.push("Claude runtime model mismatch");if(ev.some(e=>e.type==="system"&&/fallback/u.test(e.subtype??"")))errors.push("Claude fallback detected");const structured=asst.flatMap(e=>e.message.content??[]).filter(b=>b.type==="tool_use"&&b.name==="StructuredOutput");const forbidden=asst.flatMap(e=>e.message.content??[]).filter(b=>b.type==="tool_use"&&b.name!=="StructuredOutput");if(forbidden.length)errors.push("Claude non-structured tool detected");response=res[0]?.structured_output??structured.at(-1)?.input??unwrap(res[0]?.result??"");identity={initialized_model:init[0]?.model??null,assistant_models:models,model_usage:Object.keys(res[0]?.modelUsage??res[0]?.model_usage??{}),fallback:false,runtime_identity_status:errors.some(e=>/model|fallback/u.test(e))?"MISMATCH":"ASSISTANT_STREAM_OPUS_VERIFIED_FORMAL_PURITY_STILL_NO_GO",qualification:route.qualification,usage:res[0]?.usage??null};}
  else if(route.kind==="pi"){const ev=jsonLines(raw);if(ev.some(toolSignal))errors.push("Pi tool signal detected");const ends=ev.filter(e=>e.type==="message_end"&&e.message?.role==="assistant");if(ends.length!==1)errors.push("Pi assistant message cardinality mismatch");const m=ends[0]?.message;if(m?.provider!==route.provider||m?.model!==route.model)errors.push("Pi runtime identity mismatch");response=unwrap((m?.content??[]).filter(b=>b.type==="text").map(b=>b.text).join(""));identity={actual_provider:m?.provider??null,actual_model:m?.model??null,runtime_identity_status:errors.some(e=>/identity/u.test(e))?"MISMATCH":"PROVIDER_AND_MODEL_VERIFIED",usage:m?.usage??null};}
  else {const env=JSON.parse(raw);if(env.status!=="SUCCESS")errors.push(`agy status ${env.status}`);if(env.model!=null&&env.model!==route.model)errors.push("agy runtime model mismatch");if(Array.isArray(env.tool_calls)&&env.tool_calls.length)errors.push("agy tool calls detected");response=env.structured_output??unwrap(env.response??"");identity={reported_model:env.model??null,runtime_identity_status:env.model===route.model?"ENVELOPE_MODEL_VERIFIED":"REQUESTED_ROUTE_ONLY_ENVELOPE_UNVERIFIED",usage:env.usage??null};}
}catch(e){errors.push(`parse failure: ${e.message}`);}return {response,identity,errors};}

export function validateCandidate(here,n,response){const errors=[];if(!response||typeof response!=="object")return ["response unavailable"];try{const schema=readJson(path.join(paths(here).predecessor,schemaFile(n)));const ajv=new Ajv2020({allErrors:true,strict:false});const validate=ajv.compile(schema);if(!validate(response))errors.push(...validate.errors.map(e=>`${e.instancePath||"/"} ${e.message}`));const shard=readJson(path.join(paths(here).predecessor,shardFile(n)));const ids=shard.items.map(i=>i.neutral_id);if(JSON.stringify(response.item_ids)!==JSON.stringify(ids)||JSON.stringify(response.items?.map(i=>i.neutral_id))!==JSON.stringify(ids))errors.push("neutral ID order mismatch");}catch(e){errors.push(`schema validation failure: ${e.message}`);}return errors;}

export function attemptDir(here,route,n,attempt){return path.join(here,"attempts",route.slug,shardName(n),`attempt-${String(attempt).padStart(3,"0")}`);}
export function preflightCommands(route){return route.kind==="codex"?[["--version"],["debug","models","--bundled"]]:route.kind==="pi"?[["--version"],["--list-models",route.model]]:route.kind==="agy"?[["--version"],["models"]]:[["--version"]];}
export function runOfflineProbe(route,args,runtime,bundle){const cmd=sandboxCommand(route,bundle,runtime,args);return spawnSync(cmd.command,cmd.args,{cwd:"/tmp",env:envFor(route),encoding:"utf8",maxBuffer:32*1024*1024,timeout:120000});}
