import json,random,re,collections,sys
R='/workspace/tome4-chinese-translation/'
d=json.load(open('/tmp/r3/live.json'))
recent=set(); recent_secs=set()
for b in range(480,517):
    p=R+f'evidence/lite-review/batches/{b:04d}/input.json'
    try:
        for e in json.load(open(p))['entries']:
            recent.add(e['id'][:12])
            if b>=511: recent_secs.add(e['section'])
    except Exception: pass
dead=set()
for pr in json.load(open(R+'evidence/quality/dead-key-scan-20261111/pairs.json')):
    x=pr['dead']; dead.add((x['file'],x['en'],x['tag']))
dead.add(('engine.lua','following chain...','log'))  # deleted engine log (report.md:89); matched by source below
def isdead(e):
    if (e['file'],e['source'],str(e['tag'])) in dead: return True
    return e['file']=='engine.lua' and e['source'].startswith('following chain')
def pri(e):
    s=e['section']; src=e['source']
    if e['tag'] not in('tformat','_t'): return False
    if len(src)<40: return False
    if not re.search(r'/talents/|timed_effects|damage_types|objects|dialogs|uiset|^engine',s): return False
    return bool(re.search(r'%[ds0-9.]|chance|resist|immun|damage|turns?|duration|cooldown|reduc|increas|may|each|per |if |unless|while|mana|stamina|steam|vim|psi|life|equilibrium|positive|negative|hate|insanity|paradox',src,re.I))
pool=collections.defaultdict(list); nd=0
for e in d:
    if e['uid'] in recent: continue
    if isdead(e): nd+=1; continue
    if e['section'] in recent_secs: continue   # avoid sections/templates of 0511-0516
    if pri(e): pool[e['comp']].append(e)
quota={'tome':28,'engine':4,'ashes-urhrok':8,'cults':10,'orcs':10}
rng=random.Random(2026111802)
out=[]
for c,q in quota.items():
    P=sorted(pool[c],key=lambda e:e['uid'])
    # at most 2 per section to spread coverage
    rng.shuffle(P); per=collections.Counter(); pick=[]
    for e in P:
        if per[e['section']]>=2: continue
        pick.append(e); per[e['section']]+=1
        if len(pick)==q: break
    out+=pick
print({c:len(pool[c]) for c in quota}, 'recent',len(recent),'dead_excluded',nd,'recent_secs',len(recent_secs))
json.dump([e['uid'] for e in out],open('/tmp/r3/sample-uids.json','w'))
json.dump(out,open('/tmp/r3/sample.json','w'),ensure_ascii=False,indent=0)
print(len(out)); print(collections.Counter(e['comp'] for e in out))
