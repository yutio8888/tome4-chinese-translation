import sys,json,datetime
from pathlib import Path
P=Path(__file__).parent
S=P/'STATE.json'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(x): S.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
s=json.loads(S.read_text());act=sys.argv[1];did=sys.argv[2]
d=next((d for d in s['child_dispatches'] if d['dispatch_id']==did),None)
if act=='intent':
 assert d is None
 v=json.load(open(sys.argv[3]));d={'dispatch_id':did,'role':v['role'],'purpose':v['purpose'],'agent_id':None,'lifecycle':'creating','archive_confirmed':False,'archive_attempts_started':0,'workspace_id':s['workspace_id'],'parent_agent_id':s['orchestrator_agent_id'],'labels':v['labels'],'created_intent_at':now(),'dispatch_intent_recorded_before_create':True}
 for k in ('candidate_identity','input_path','candidate_author_agent_id','lane_group_identity','lane_index','author_provider_resolution'): 
  if k in v:d[k]=v[k]
 s['child_dispatches'].append(d)
elif act=='bind':
 v=json.load(open(sys.argv[3]));v=v['snapshot']
 assert v['workspaceId']==s['workspace_id']
 assert v['labels']['paseo.parent-agent-id']==s['orchestrator_agent_id']
 assert all(v['labels'].get(k)==val for k,val in d['labels'].items())
 assert d['agent_id'] is None
 d.update(agent_id=v['id'],labels=v['labels'],lineage_verified=True,lifecycle='active',first_live_capture_path=sys.argv[3])
 obs={'schema_version':1,'source':'live_agent_metadata','captured_at':now(),'capture_status':'captured'}
 for dst,src in [('provider','provider'),('model','model'),('mode','currentModeId'),('thinking','thinkingOptionId')]:obs[dst]={'presence':'present','value':v[src]} if src in v else {'presence':'missing'}
 d['runtime_observation']=obs
 if d['role']=='EXECUTOR':s['executor']={'role':'EXECUTOR','agent_id':v['id']}
 elif d['role']=='REVIEWER':
  ptr={k:d[k] for k in ('role','purpose','candidate_identity','dispatch_id','input_path','agent_id')}
  if 'lane_index' in d:ptr.update({k:d[k] for k in ('lane_index','lane_group_identity')});s.setdefault('contextual_reviewers',[]).append(ptr)
  else:s['contextual_reviewers']=[ptr]
elif act=='archive-intent':
 v=json.load(open(sys.argv[3]))['snapshot'];assert v['id']==d['agent_id'];assert v.get('activeTurn') is None and v['status'] in ['idle','error','closed']
 assert d['archive_attempts_started']<2
 d.update(lifecycle='archive_pending',archive_attempts_started=d['archive_attempts_started']+1,terminal_capture_path=sys.argv[3])
elif act=='archive-confirm':
 v=json.load(open(sys.argv[3]))['snapshot'];assert v['id']==d['agent_id'];assert v['status']=='closed' and v.get('archivedAt') and v.get('activeTurn') is None
 d.update(lifecycle='archived',archive_confirmed=True,archived_at=v['archivedAt'],archive_capture_path=sys.argv[3])
else:raise ValueError(act)
s['updated_at']=now();save(s);print(act,did)
