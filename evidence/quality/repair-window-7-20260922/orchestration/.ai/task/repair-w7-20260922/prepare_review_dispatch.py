import sys,json,hashlib,datetime
from pathlib import Path
sys.path.insert(0,'tools')
from contextual_lane_manifest import render_dispatch_prompt,validate_manifest
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());phase=sys.argv[1];cycle=int(sys.argv[2]);attempt=int(sys.argv[3]);did=sys.argv[4];s=json.loads((P/'STATE.json').read_text());profiles=json.loads((P/f'{did}-profiles.json').read_text());profile=next(p for p in profiles['profiles'] if p['id']=='agent_profile_mt3s8sou_fggrhfnq1gj');assert (profile['provider'],profile['model'],profile['modeId'],profile['thinkingOptionId'])==('codex','gpt-5.6-sol','auto-review','medium')
assert s['review_phase']==phase and s['cycle']==cycle;author=s['candidate_author_agent_id'];a=next(d for d in s['child_dispatches'] if d['agent_id']==author);assert a['role']=='EXECUTOR' and a['archive_confirmed'];v=json.loads(Path(a['first_live_capture_path']).read_text())['snapshot'];assert v['id']==author and v['provider']=='codex' and v['model']=='gpt-5.6-sol';assert a['runtime_observation']['provider']==dict(presence='present',value='codex')
laned=phase in ('REVIEW','RE_REVIEW') and len(json.loads((P/'WORKSET.json').read_text())['items'])>=4
if laned:
 mp=P/f'CONTEXTUAL-LANE-GROUP-r{cycle}a{attempt}.json';m=json.loads(mp.read_text());validate_manifest(m,manifest_path=str(mp));lane=next(l for l in m['payload']['lanes'] if l['dispatch_id']==did);ip=lane['input_path'];ci=lane['candidate_identity'];index=lane['index']
else:
 assert did==f'f{cycle}a{attempt}' if phase=='FINAL_REVIEW' else did==f'r{cycle}a{attempt}'
 ip=str(P/f'CONTEXTUAL-ENVELOPE-{did}.json');ci=json.loads(Path(ip).read_text())['candidate_identity']
prompt=render_dispatch_prompt(ci,ip)
if laned:prompt='先按输入briefing核验启动凭据；凭据未出现时留在本轮等待，不得提前审核或结束。\n'+prompt
assert len(prompt.encode())<=800,len(prompt.encode());labels=dict(task_id=P.name,role='reviewer',purpose='translation_contextual_v2',dispatch_id=did,candidate_identity=ci,**{'paseo.parent-agent-id':s['orchestrator_agent_id']});intent=dict(role='REVIEWER',purpose='translation_contextual_v2',labels=labels,candidate_identity=ci,input_path=ip,candidate_author_agent_id=author,author_provider_resolution='verified')
if laned:
 labels.update(lane_group_identity=m['group_identity'],lane_index=str(index));intent.update(lane_group_identity=m['group_identity'],lane_index=index)
params=dict(title=f'W7 {did} 译文复核',provider=profile['provider']+'/'+profile['model'],settings=dict(modeId=profile['modeId'],thinkingOptionId=profile['thinkingOptionId']),workspaceId=s['workspace_id'],initialPrompt=prompt,labels=labels,notifyOnFinish=True)
for name,obj in [('parameters',params),('intent',intent),('profile-selection',dict(profile_id=profile['id'],selected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),profile=profile,author_provider_resolution='verified',author_live_metadata_path=a['first_live_capture_path'],author_agent_id=author,budget_exception='Verified codex-authored candidate may use primary subscription provider; v2 lanes do not require different exact models.'))]:
 p=P/f'{did}-{name}.json';assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
p=P/f'{did}-prompt.txt';assert not p.exists();p.write_text(prompt);print(json.dumps(dict(dispatch_id=did,prompt_bytes=len(prompt.encode()),parameters_path=str(P/f'{did}-parameters.json')),ensure_ascii=False))
