import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,'tools/orchestration');sys.path.insert(0,str(Path(__file__).parent))
from review_lifecycle import read_native_final
from native_path import native_log
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
did=sys.argv[1]
v=json.loads((P/f'{did}-terminal.json').read_text())['snapshot']
assert v['activeTurn'] is None and v['status']=='idle' and v['attentionReason']=='finished'
s=json.loads((P/'STATE.json').read_text());d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did)
assert v['id']==d['agent_id'] and d['role']=='EXECUTOR'
assert v['workspaceId']==s['workspace_id'] and v['labels']['paseo.parent-agent-id']==s['orchestrator_agent_id']
session=v['persistence']['sessionId'];prompt=(P/f'{did}-prompt.txt').read_text()
raw,proof=read_native_final(native_log(v['provider'],session,str(Path.cwd())),provider=v['provider'],session_id=session,cwd=str(Path.cwd()),prompt=prompt,natural_success=True)
dest=P/f'{did}-report.raw';assert not dest.exists();dest.write_bytes(raw)
(P/f'{did}-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
d.update(output_valid=True,raw_output_path=str(dest),raw_output_sha256=hashlib.sha256(raw).hexdigest())
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(raw.decode())
