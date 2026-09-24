import json,sys
from pathlib import Path
# usage: mkcap.py <did> terminal <updatedAt> <lastUserMessageAt> <attentionTimestamp>
#        mkcap.py <did> archived <archivedAt>
P=Path(__file__).parent;did,kind=sys.argv[1:3]
if kind=='terminal':
 v=json.loads((P/f'{did}-live.json').read_text());s=v['snapshot'];u,l,a=sys.argv[3:6]
 s.update(status='idle',activeTurn=None,updatedAt=u,lastUserMessageAt=l,requiresAttention=True,attentionReason='finished',attentionTimestamp=a)
 if s['provider']=='codex':
  s['persistence']['nativeHandle']=s['persistence']['sessionId']
  s['persistence']['metadata'].update(provider=s['provider'],title=s['title'],threadId=s['persistence']['sessionId'],modeId=s['currentModeId'],model=s['model'],thinkingOptionId=s['thinkingOptionId'],asyncQuestions=[])
 v['status']='idle'
else:
 v=json.loads((P/f'{did}-terminal.json').read_text());s=v['snapshot'];a=sys.argv[3]
 s.update(status='closed',updatedAt=a,requiresAttention=False,attentionReason=None,attentionTimestamp=None,archivedAt=a,activeTurn=None);v['status']='closed'
(P/f'{did}-{kind}.json').write_text(json.dumps(v,ensure_ascii=False)+'\n');print(kind,did)
