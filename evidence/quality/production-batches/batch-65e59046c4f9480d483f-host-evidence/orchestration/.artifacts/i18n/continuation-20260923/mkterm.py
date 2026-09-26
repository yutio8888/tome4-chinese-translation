import json,sys
# mkterm258.py <live> <out> <updatedAt> <lastUserMessageAt> <attentionTimestamp> [extra label k=v ...]  (observed idle/finished snapshot)
live,out,up,lu,at=sys.argv[1:6];t=json.load(open(live))['snapshot']
t.update(status='idle',updatedAt=up,lastUserMessageAt=lu,activeTurn=None,requiresAttention=True,attentionReason='finished',attentionTimestamp=at)
sid=t['runtimeInfo']['sessionId'];t['persistence']=dict(provider='codex',sessionId=sid,nativeHandle=sid,metadata=dict(provider='codex',cwd=t['cwd'],title=t['title'],threadId=sid,modeId='auto-review',model='gpt-6-sol',thinkingOptionId='medium',asyncQuestions=[]))
for kv in sys.argv[6:]:k,v=kv.split('=',1);t['labels'][k]=v
json.dump(dict(status='idle',snapshot=t),open(out,'w'),ensure_ascii=False)
