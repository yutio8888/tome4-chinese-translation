globalThis.archiveW7Child = async function(tools,did,agentId) {
  if(!/^[a-z0-9-]+$/.test(did))throw Error('bad dispatch id');
  const P='.ai/task/repair-w7-20260922';
  const run=async cmd=>{const r=await tools.exec_command({cmd,max_output_tokens:2500,yield_time_ms:1000});if(r.session_id||r.exit_code!==0)throw Error(JSON.stringify(r));return r.output;};
  const write=async(name,obj)=>{const path=P+'/'+did+'-'+name+'.json';await run('test ! -e '+path);await tools.apply_patch('*** Begin Patch\n*** Add File: '+path+'\n'+JSON.stringify(obj,null,2).split('\n').map(l=>'+'+l).join('\n')+'\n*** End Patch');};
  const before=await tools.mcp__paseo__get_agent_status({agentId});await write('before-archive',before.structuredContent);
  await run('git status --short');await run('git diff --stat');
  await run('python3 -B '+P+'/lifecycle.py archive-intent '+did+' '+P+'/'+did+'-before-archive.json');
  const result=await tools.mcp__paseo__archive_agent({agentId});await write('archive-response',result);
  const after=await tools.mcp__paseo__get_agent_status({agentId});await write('archived',after.structuredContent);
  await run('python3 -B '+P+'/lifecycle.py archive-confirm '+did+' '+P+'/'+did+'-archived.json');
  return {dispatch_id:did,agent_id:agentId,archive_confirmed:true};
};
