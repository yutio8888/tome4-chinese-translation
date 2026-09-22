import json,sys,hashlib,os
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0,'tools/orchestration');sys.path.insert(0,'tools')
from review_lifecycle import read_native_final
from contextual_result_check import validate_result_bytes
P=Path(__file__).parent;did=sys.argv[1];s=json.loads((P/'STATE.json').read_text());d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did)
capture=json.loads((P/f'{did}-terminal.json').read_text());v=capture['snapshot'];assert v['id']==d['agent_id'] and v.get('activeTurn') is None and v['status']=='idle' and v['attentionReason']=='finished'
assert v['workspaceId']==s['workspace_id'] and v['labels']['paseo.parent-agent-id']==s['orchestrator_agent_id']
assert hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest()==s['current_translation_sha256']
provider=v['provider'];session=v['persistence']['sessionId'];prompt=(P/f'{did}-prompt.txt').read_text();cwd=str(Path.cwd())
if provider=='grok':path=Path.home()/'.grok/sessions'/quote(cwd,safe='')/session
elif provider=='claude':path=Path(os.environ.get('CLAUDE_CONFIG_DIR',str(Path.home()/'.claude')))/'projects'/cwd.replace('/','-')/(session+'.jsonl')
elif provider=='codex':
 root=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions'
 paths=list(root.glob(f'2026/09/22/*{session}.jsonl'));assert len(paths)==1,paths;path=paths[0]
else:raise ValueError(provider)
raw,proof=read_native_final(path,provider=provider,session_id=session,cwd=cwd,prompt=prompt,natural_success=True)
R=Path('.ai/reviews')/P.name;R.mkdir(exist_ok=True)
rp=R/f'raw-{did}.txt';assert not rp.exists();rp.write_bytes(raw)
(P/f'{did}-raw-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
validate_result_bytes(Path(d['input_path']).read_bytes(),raw)
d['output_valid']=True;d['raw_output_path']=str(rp);d['raw_output_sha256']=hashlib.sha256(raw).hexdigest()
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(raw.decode())
