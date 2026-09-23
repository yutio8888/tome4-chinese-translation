import sys,json,datetime
from pathlib import Path
sys.path.insert(0,'tools')
from contextual_lane_manifest import render_dispatch_prompt
# usage: prepare_dispatch.py review <did> <provider/model> <modeId> <thinking>
#        prepare_dispatch.py executor <did> <provider/model> <modeId> <thinking> <prompt-file>
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());kind,did,provider,mode,thinking=sys.argv[1:6]
s=json.loads((P/'STATE.json').read_text())
if kind=='review':
 path=P/f'CONTEXTUAL-ENVELOPE-{did}.json';env=json.loads(path.read_text())
 prompt=render_dispatch_prompt(env['candidate_identity'],str(path));assert len(prompt.encode())<=800
 labels=dict(task_id=P.name,role='reviewer',purpose='translation_contextual_v2',dispatch_id=did,candidate_identity=env['candidate_identity'])
 intent=dict(role='REVIEWER',purpose='translation_contextual_v2',labels=labels,candidate_identity=env['candidate_identity'],input_path=str(path),candidate_author_agent_id=s['candidate_author_agent_id'],author_provider_resolution='verified')
 title=f'W9b {did} full review'
else:
 prompt=Path(sys.argv[6]).read_text();labels=dict(task_id=P.name,role='executor',purpose='implement',dispatch_id=did)
 intent=dict(role='EXECUTOR',purpose='implement',labels=labels);title=f'W9b {did} executor'
labels['paseo.parent-agent-id']=s['orchestrator_agent_id']
params=dict(title=title,provider=provider,settings=dict(modeId=mode,thinkingOptionId=thinking),workspaceId=s['workspace_id'],initialPrompt=prompt,labels=labels,notifyOnFinish=True)
sel=dict(selected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),provider=provider,modeId=mode,thinkingOptionId=thinking,basis='user instruction 2026-09-23: reviews use gpt-6-sol and opus 5.5; executor keeps Worker Primary profile model' )
for name,obj in [('intent',intent),('parameters',params),('model-selection',sel)]:
 dest=P/f'{did}-{name}.json';assert not dest.exists();dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(P/f'{did}-prompt.txt').write_text(prompt)
print(json.dumps(params,ensure_ascii=False))
