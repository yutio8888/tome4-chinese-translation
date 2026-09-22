globalThis.dispatchW7Executor = async function(tools, did) {
  if (!/^[a-z0-9-]+$/.test(did)) throw Error('bad dispatch id');
  const P='.ai/task/repair-w7-20260922';
  const run=async cmd=>{const r=await tools.exec_command({cmd,max_output_tokens:5000,yield_time_ms:1000});if(r.session_id||r.exit_code!==0)throw Error(JSON.stringify(r));return r.output;};
  const write=async(name,obj)=>{const path=P+'/'+did+'-'+name+'.json';await run('test ! -e '+path);await tools.apply_patch('*** Begin Patch\n*** Add File: '+path+'\n'+JSON.stringify(obj,null,2).split('\n').map(l=>'+'+l).join('\n')+'\n*** End Patch');};
  const profiles=await tools.mcp__paseo__list_profiles({}); await write('profiles',profiles.structuredContent);
  const p=profiles.structuredContent.profiles.find(p=>p.id==='legacy_favorite:codex:gpt-5.6-luna');
  const params=JSON.parse(await run('cat '+P+'/'+did+'-parameters.json'));
  if(params.provider!==p.provider+'/'+p.model||params.settings.modeId!==p.modeId||params.settings.thinkingOptionId!==p.thinkingOptionId)throw Error('profile mismatch');
  await write('profile-selection',{profile_id:p.id,profile:p,selection_basis:'Fresh primary EXECUTOR profile for bounded implementation'});
  await run('python3 -B '+P+'/lifecycle.py intent '+did+' '+P+'/'+did+'-intent.json');
  const result=await tools.mcp__paseo__create_agent(params);await write('create',{parameters:params,response:result.structuredContent,profile_id:p.id});
  const agentId=result.structuredContent.agentId;const live=await tools.mcp__paseo__get_agent_status({agentId});await write('live',live.structuredContent);
  await run('python3 -B '+P+'/lifecycle.py bind '+did+' '+P+'/'+did+'-live.json');
  const v=live.structuredContent.snapshot;if(v.model!==p.model||v.provider!==p.provider||v.currentModeId!==p.modeId||v.thinkingOptionId!==p.thinkingOptionId)throw Error('actual runtime mismatch');
  return {dispatch_id:did,agent_id:agentId,session:v.persistence.sessionId};
};
