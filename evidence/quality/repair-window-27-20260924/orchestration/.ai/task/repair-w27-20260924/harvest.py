import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,'tools/orchestration');sys.path.insert(0,'tools');sys.path.insert(0,str(Path(__file__).parent))
from review_lifecycle import read_native_final
from contextual_result_check import validate_result_bytes
from native_path import native_log
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());did=sys.argv[1];s=json.loads((P/'STATE.json').read_text());d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did)
capture=json.loads((P/f'{did}-terminal.json').read_text());v=capture['snapshot'];assert v['id']==d['agent_id'] and v.get('activeTurn') is None and v['status']=='idle' and v['attentionReason']=='finished'
assert v['workspaceId']==s['workspace_id'] and v['labels']['paseo.parent-agent-id']==s['orchestrator_agent_id']
assert {f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in ['mod-tome.lua','tome-ashes-urhrok.lua']}==s['current_translation_sha256']
provider=v['provider'];session=v['persistence']['sessionId'];prompt=(P/f'{did}-prompt.txt').read_text();cwd=str(Path.cwd())
path=native_log(provider,session,cwd)
raw,proof=read_native_final(path,provider=provider,session_id=session,cwd=cwd,prompt=prompt,natural_success=True)
R=Path('.ai/reviews')/P.name;R.mkdir(parents=True,exist_ok=True)
rp=R/f'raw-{did}.txt';assert not rp.exists();rp.write_bytes(raw)
(P/f'{did}-raw-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
validate_result_bytes(Path(d['input_path']).read_bytes(),raw)
d['output_valid']=True;d['raw_output_path']=str(rp);d['raw_output_sha256']=hashlib.sha256(raw).hexdigest()
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(raw.decode())
