import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from native_path import native_log
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
did=sys.argv[1];cap=sys.argv[2] if len(sys.argv)>2 else f'{did}-terminal.json'
v=json.loads((P/cap).read_text())['snapshot']
session=v['persistence']['sessionId'];provider=v['provider'];path=native_log(provider,session,str(Path.cwd()))
calls=[]
for line in path.read_text().splitlines():
    j=json.loads(line)
    if provider=='claude' and j.get('type')=='assistant':
        calls.extend(x for x in j.get('message',{}).get('content',[]) if x.get('type')=='tool_use')
    elif provider=='codex' and j.get('type')=='response_item' and j.get('payload',{}).get('type') in ('function_call','custom_tool_call','local_shell_call'):
        calls.append(j['payload'])
out={'dispatch_id':did,'native_session':session,'native_path':str(path),'native_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tool_calls':calls}
dest=P/f'{did}-native-tools.json'
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for c in calls: print(json.dumps(c.get('input',c.get('arguments',c)),ensure_ascii=False)[:500])
print(len(calls),'calls')
