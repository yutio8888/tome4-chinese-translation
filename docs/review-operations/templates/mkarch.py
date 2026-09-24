import json,sys
# mkarch257.py <terminal.json> <out.json> <updatedAt> <archivedAt>  (values copied from observed get_agent_status closed snapshot)
t=json.load(open(sys.argv[1]));s=t['snapshot']
s.update(status='closed',updatedAt=sys.argv[3],archivedAt=sys.argv[4],requiresAttention=False,attentionReason=None,attentionTimestamp=None,activeTurn=None)
json.dump(dict(status='closed',snapshot=s),open(sys.argv[2],'w'),ensure_ascii=False)
