import json,sys,os,hashlib
from pathlib import Path
from urllib.parse import quote
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
did=sys.argv[1]
v=json.loads((P/f'{did}-terminal.json').read_text())['snapshot']
session=v['persistence']['sessionId'];provider=v['provider']
if provider=='claude':
    path=Path(os.environ.get('CLAUDE_CONFIG_DIR',str(Path.home()/'.claude')))/'projects'/str(Path.cwd()).replace('/','-')/(session+'.jsonl')
elif provider=='codex':
    paths=list((Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions/2026/09/22').glob('*'+session+'.jsonl'))
    assert len(paths)==1
    path=paths[0]
elif provider=='grok':
    path=Path.home()/'.grok/sessions'/quote(str(Path.cwd()),safe='')/session/'chat_history.jsonl'
else:
    raise ValueError(provider)
calls=[]
for line in path.read_text().splitlines():
    j=json.loads(line)
    if provider=='claude' and j.get('type')=='assistant':
        calls.extend(x for x in j.get('message',{}).get('content',[]) if x.get('type')=='tool_use')
    elif provider=='codex' and j.get('type')=='response_item' and j.get('payload',{}).get('type') in ('function_call','custom_tool_call'):
        calls.append(j['payload'])
    elif provider=='grok' and j.get('type')=='assistant':
        calls.extend(j.get('tool_calls',[]))
out={'dispatch_id':did,'native_session':session,'native_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tool_calls':calls}
dest=P/f'{did}-native-tools.json'
if dest.exists():assert json.loads(dest.read_text())==out
else:dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
