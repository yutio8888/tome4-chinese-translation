async function dispatchW7Review(tools, phase, cycle, attempt, ids) {
  const P = '.ai/task/repair-w7-20260922';
  const q = s => "'" + s.replaceAll("'", "'\\''") + "'";
  const run = async cmd => {
    const r = await tools.exec_command({cmd, yield_time_ms:1000, max_output_tokens:6000});
    if (r.session_id) throw Error('Resume original local session '+r.session_id);
    if (r.exit_code !== 0) throw Error(r.output);
    return r.output;
  };
  const write = async (path, obj) => {
    await run('test ! -e '+q(path));
    await tools.apply_patch('*** Begin Patch\n*** Add File: '+path+'\n'+JSON.stringify(obj,null,2).split('\n').map(l=>'+'+l).join('\n')+'\n*** End Patch');
  };
  const created=[];
  for (const did of ids) {
    if (!/^[a-z0-9-]+$/.test(did)) throw Error('Unsafe dispatch id');
    const profiles=await tools.mcp__paseo__list_profiles({});
    await write(P+'/'+did+'-profiles.json',profiles.structuredContent);
    await run('python3 -B '+P+'/prepare_review_dispatch.py '+q(phase)+' '+cycle+' '+attempt+' '+q(did));
    const params=JSON.parse(await run('cat '+q(P+'/'+did+'-parameters.json')));
    await run('python3 -B '+P+'/lifecycle.py intent '+q(did)+' '+q(P+'/'+did+'-intent.json'));
    const reply=await tools.mcp__paseo__create_agent(params);
    await write(P+'/'+did+'-create.json',{parameters:params,response:reply.structuredContent});
    const aid=reply.structuredContent.agentId;
    const live=await tools.mcp__paseo__get_agent_status({agentId:aid});
    await write(P+'/'+did+'-live.json',live.structuredContent);
    await run('python3 -B '+P+'/lifecycle.py bind '+q(did)+' '+q(P+'/'+did+'-live.json'));
    const s=live.structuredContent.snapshot;
    if(s.provider!=='codex'||s.model!=='gpt-5.6-sol'||s.currentModeId!=='auto-review'||s.thinkingOptionId!=='medium') throw Error('Unexpected actual reviewer runtime; reconcile this child');
    created.push({dispatch_id:did,agent_id:aid,session:s.persistence.sessionId});
  }
  if (ids.length===4) await run('python3 -B '+P+'/release_review.py '+q(phase)+' '+cycle+' '+attempt);
  return created;
}

globalThis.dispatchW7Review = dispatchW7Review;
