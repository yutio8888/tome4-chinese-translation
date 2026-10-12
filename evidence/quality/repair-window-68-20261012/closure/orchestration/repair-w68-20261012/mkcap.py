import json,sys
from pathlib import Path
# mkcap.py <out> <did> <agent> <session> <provider> <model> <mode> <thinking> <title> <status> <createdAt> <updatedAt> <turnStart|-> <attention|-> <attentionTs|-> <archivedAt|->
# Values are copied verbatim from the observed get_agent_status snapshot.
P=Path(__file__).parent
out,did,aid,sid,prov,model,mode,th,title,st,cr,up,ts,att,attts,arch=sys.argv[1:17]
n=lambda v:None if v=='-' else v
labels=json.loads((P/f'{did}-intent.json').read_text())['labels']
snap=dict(id=aid,provider=prov,cwd='/workspace/tome4-chinese-translation',workspaceId='wks_420314270844170b',model=model,thinkingOptionId=th,effectiveThinkingOptionId=th,
 runtimeInfo=dict(provider=prov,sessionId=None,model=None,modeId=mode) if prov=='claude' else dict(provider=prov,sessionId=sid,model=model,thinkingOptionId=th,modeId=mode),createdAt=cr,updatedAt=up,status=st,
 activeTurn=None if ts=='-' else dict(turnId='foreground-turn-1' if prov=='claude' else f'{prov}-turn-0',startedAt=ts),currentModeId=mode,pendingPermissions=[],
 persistence=dict(provider=prov,sessionId=sid,metadata=dict(cwd='/workspace/tome4-chinese-translation')),title=title,labels=labels,
 requiresAttention=att not in ('-',),attentionReason=n(att),attentionTimestamp=n(attts))
if arch!='-':snap['archivedAt']=arch
Path(out).write_text(json.dumps(dict(status=st,snapshot=snap),ensure_ascii=False)+'\n')
