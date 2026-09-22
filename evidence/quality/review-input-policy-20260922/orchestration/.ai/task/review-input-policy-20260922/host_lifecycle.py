"""Task-local orchestration only; consumes explicit captures, never creates agents."""
import sys,json,datetime
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tools/orchestration'))
import review_lifecycle as L
D=Path('.ai/task/review-input-policy-20260922')
def read(p): return json.loads(Path(p).read_text())
def save(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def capture(p):
 x=read(p); return x.get('structuredContent',x)
a,did,cp=sys.argv[1:4];state=read(D/'STATE.json');s=capture(cp)['snapshot'];cs=state['child_dispatches']; matches=[x for x in cs if x['dispatch_id']==did]
assert s['workspaceId']==state['workspace_id'] and s['cwd']==str(Path.cwd())
assert s['labels']['task_id']==state['task_id'] and s['labels']['dispatch_id']==did and s['labels']['paseo.parent-agent-id']==state['orchestrator_agent_id']
if a=='bind':
 assert not matches
 role={'executor':'EXECUTOR','reviewer':'REVIEWER','senior-reviewer':'senior-reviewer'}[s['labels']['role']]
 obs=L.observation(s,L.now()); c=dict(role=role,purpose=s['labels']['purpose'],dispatch_id=did,agent_id=s['id'],workspace_id=s['workspaceId'],parent_agent_id=state['orchestrator_agent_id'],lineage_verified=True,labels=s['labels'],lifecycle='active',archive_confirmed=False,archive_attempts_started=0,runtime_observation=obs)
 if role!='EXECUTOR': c.update(candidate_author_agent_id=state['candidate_author_agent_id'],author_provider_resolution='verified',candidate_ref=state['candidate_ref'])
 cs.append(c); state[{'EXECUTOR':'executor','REVIEWER':'reviewer','senior-reviewer':'senior_reviewer'}[role]]={k:c[k] for k in ['role','purpose','agent_id']}
else:
 assert len(matches)==1;c=matches[0];assert c['agent_id']==s['id'] and c['labels']==s['labels']
 if a=='harvest':
  L.terminal(s);assert s['attentionReason']=='finished' and s['status']=='idle'
  args=read(sys.argv[4])['parameters']; assert args['labels']==c['labels']
  provider,session=L.native_identity(s)
  raw,proof=L.read_native_final(sys.argv[5],provider=provider,session_id=session,cwd=str(Path.cwd()),prompt=args['initialPrompt'],natural_success=True)
  L.immutable(D/(did+'.raw'),raw);save(D/(did+'-native-proof.json'),proof)
  c.update(lifecycle='terminal',raw_output_path=str(D/(did+'.raw')),raw_output_sha256=L.digest(raw),output_valid=bool(raw.strip()))
  if c['role']=='EXECUTOR':state['state']='VALIDATE'
  print(raw.decode())
 elif a=='archive-intent':
  L.terminal(s);assert c['lifecycle']=='terminal' and c['archive_attempts_started']<2
  c['archive_attempts_started']+=1
 elif a=='archive-confirm':
  assert L.is_archived(s);c.update(lifecycle='archived',archive_confirmed=True,archived_at=s['archivedAt'])
 else:raise ValueError(a)
state['updated_at']=L.now();save(D/'STATE.json',state)
