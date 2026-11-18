import json,random,re,subprocess,collections
d=json.load(open('/tmp/ft2/live.json'))
# exclude units whose target changed in recent batches (0480-0510): 0.3.11 source commit onward
recent=set()
for b in range(480,511):
    p=f'evidence/lite-review/batches/{b:04d}/input.json'
    try:
        for e in json.load(open(p))['entries']: recent.add(e['id'][:12])
    except Exception: pass
dead=set()
try:
    for l in open('evidence/quality/dead-key-scan-20261111/dead-keys.json'): pass
except Exception: pass
def pri(e):
    s=e['section']; src=e['source']
    if e['tag'] not in('tformat','_t'): return False
    if len(src)<40: return False
    if not re.search(r'/talents/|timed_effects|damage_types|objects|dialogs|uiset|^engine',s): return False
    return bool(re.search(r'%[ds0-9.]|chance|resist|damage|turns?|cooldown|reduc|increas|may|each|per |mana|stamina|steam|vim|psi|life',src,re.I))
pool=collections.defaultdict(list)
for e in d:
    if e['uid'] in recent: continue
    if pri(e): pool[e['comp']].append(e)
quota={'tome':30,'engine':6,'ashes-urhrok':6,'cults':9,'orcs':9}
rng=random.Random(20261118)
out=[]
for c,q in quota.items():
    P=sorted(pool[c],key=lambda e:e['uid']); out+=rng.sample(P,q)
print({c:len(pool[c]) for c in quota}, len(recent))
json.dump([e['uid'] for e in out],open('/tmp/ft2/sample-uids.json','w'))
json.dump(out,open('/tmp/ft2/sample.json','w'),ensure_ascii=False,indent=0)
for e in out: print(e['uid'],e['comp'],e['section'].split('/')[-1],repr(e['source'][:70]))
