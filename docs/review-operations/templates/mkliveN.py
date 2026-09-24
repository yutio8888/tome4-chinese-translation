import json,sys
# mklive275.py <out> <lane i> <agent id> <session> <createdAt> <updatedAt> <turnStartedAt>   (values copied from observed get_agent_status)
out,i,aid,sid,cr,up,ts=sys.argv[1:8];C='.artifacts/i18n/continuation-20260923'
e=json.load(open(f'{C}/review275-surface-emit.json'))[int(i)];lab=dict(e['labels'])
snap=dict(id=aid,provider='codex',cwd='/workspace/tome4-chinese-translation',workspaceId='wks_420314270844170b',model='gpt-6-sol',thinkingOptionId='medium',effectiveThinkingOptionId='medium',
 runtimeInfo=dict(provider='codex',sessionId=sid,model='gpt-6-sol',thinkingOptionId='medium',modeId='auto-review',extra=dict(collaborationMode='Default')),createdAt=cr,updatedAt=up,lastUserMessageAt=None,status='running',
 activeTurn=dict(turnId='codex-turn-0',startedAt=ts),currentModeId='auto-review',pendingPermissions=[],persistence=dict(provider='codex',sessionId=sid,metadata=dict(cwd='/workspace/tome4-chinese-translation')),
 title=f'lane-000-{i}',labels=lab,requiresAttention=False,attentionReason=None,attentionTimestamp=None)
json.dump(dict(status='running',snapshot=snap),open(out,'w'),ensure_ascii=False)
