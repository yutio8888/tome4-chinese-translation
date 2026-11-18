import json,random,collections
rows=json.load(open('/tmp/r5/candidates.json'))
quota={'tome':28,'orcs':12,'ashes-urhrok':10,'cults':10}
rng=random.Random(2026111803)
rare={'C3':0,'C2':1,'C1':2,'C4':3}
out=[]
for c,q in quota.items():
    P=sorted([r for r in rows if r['comp']==c],key=lambda r:r['uid']); rng.shuffle(P)
    P.sort(key=lambda r:(r['same_recent_section'],min(rare[k] for k in r['cats'])))
    per=collections.Counter(); pick=[]
    for r in P:
        if per[r['section']]>=3: continue
        pick.append(r); per[r['section']]+=1
        if len(pick)==q: break
    out+=pick
print(len(out),collections.Counter(r['comp'] for r in out),collections.Counter(c for r in out for c in r['cats']),'recent-section',sum(r['same_recent_section'] for r in out))
json.dump([r['uid'] for r in out],open('/tmp/r5/uids.json','w'))
json.dump(out,open('/tmp/r5/sample.json','w'),ensure_ascii=False,indent=0)
