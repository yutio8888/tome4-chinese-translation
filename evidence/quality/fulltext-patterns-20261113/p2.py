import json,collections,re
E=json.load(open('/tmp/ft/live.json'))
def kind(e):
    if e['tag']=='talent name': return 'talent'
    if e['tag']=='entity name':
        s=e['section']
        if '/npcs' in s or 'npc' in s: return 'npc'
        if '/objects' in s or 'artifact' in s: return 'object'
        return 'entity'
    if e['tag']=='damage type': return 'damage'
    if 'timed_effects' in e['section'] and e['tag']=='_t' and re.fullmatch(r"[A-Z][A-Za-z' :\-!]{1,38}",e['source']) and not e['source'].endswith('.'): return 'effect'
    return None
G=collections.defaultdict(list)
for e in E:
    k=kind(e)
    if k: G[e['target'].strip()].append(dict(kind=k,src=e['source'],file=e['file'],line=e['line'],sec=e['section']))
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
col={}
for t,L in G.items():
    srcs={norm(x['src']) for x in L}
    if len(srcs)>1: col[t]=L
print('name entries',sum(len(v) for v in G.values()),'distinct targets',len(G),'collision groups',len(col))
kinds=collections.Counter()
for t,L in col.items():
    kinds[tuple(sorted({x['kind'] for x in L}))]+=1
print(kinds.most_common(20))
json.dump(col,open('/tmp/ft/p2-col.json','w'),ensure_ascii=False,indent=0)
