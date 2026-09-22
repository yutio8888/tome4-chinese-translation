import sys,json
from pathlib import Path
sys.path.insert(0,'tools')
from contextual_lane_manifest import render_dispatch_prompt
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());did=sys.argv[1]
s=json.loads((P/'STATE.json').read_text());path=P/f'CONTEXTUAL-ENVELOPE-{did}.json';env=json.loads(path.read_text())
profiles=json.loads((P/f'{did}-profiles.json').read_text())['profiles'];profile=next(x for x in profiles if x['id']=='agent_profile_mt3s8sou_fggrhfnq1gj')
author=json.loads((P/f'{did}-author-live.json').read_text())['snapshot'];assert author['id']==s['candidate_author_agent_id'] and author['provider']=='codex'
prompt=render_dispatch_prompt(env['candidate_identity'],str(path));assert len(prompt.encode())<=800
labels=dict(task_id=P.name,role='reviewer',purpose='translation_contextual_v2',dispatch_id=did,candidate_identity=env['candidate_identity']);labels['paseo.parent-agent-id']=s['orchestrator_agent_id']
intent=dict(role='REVIEWER',purpose='translation_contextual_v2',labels=labels,candidate_identity=env['candidate_identity'],input_path=str(path),candidate_author_agent_id=s['candidate_author_agent_id'])
params=dict(title=f'W6 {did} full review',provider=profile['provider']+'/'+profile['model'],settings={k:profile[k] for k in ('modeId','thinkingOptionId') if k in profile},workspaceId=s['workspace_id'],initialPrompt=prompt,labels=labels,notifyOnFinish=True)
for name,obj in [('intent',intent),('parameters',params)]:
 dest=P/f'{did}-{name}.json';assert not dest.exists();dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(P/f'{did}-prompt.txt').write_text(prompt)
print(json.dumps(params,ensure_ascii=False))
