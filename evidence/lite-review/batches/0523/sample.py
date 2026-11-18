import json,random,collections
R='/workspace/tome4-chinese-translation/'
rows=json.load(open('/tmp/r5/candidates.json'))
recent=set()
for b in range(480,523):
    try:
        for e in json.load(open(R+f'evidence/lite-review/batches/{b:04d}/input.json'))['entries']: recent.add(e['unit_id'])
    except FileNotFoundError: pass
s0521=set(e['unit_id'] for e in json.load(open(R+'evidence/lite-review/batches/0521/input.json'))['entries'])
blocks0521=set((r['section'],tuple(r['block'])) for r in rows if r['uid'] in s0521)
rest=[r for r in rows if r['uid'] not in s0521]
avail=[r for r in rest if r['uid'] not in recent and (r['section'],tuple(r['block'])) not in blocks0521]
print('pool',len(rows),'uncovered',len(rest),'available',len(avail),collections.Counter(r['comp'] for r in avail))
quota={'orcs':20,'cults':20,'ashes-urhrok':12,'tome':8}
rng=random.Random(2026111804); out=[]; short={}
for c,q in quota.items():
    P=sorted([r for r in avail if r['comp']==c and (c!='tome' or 'C4' in r['cats'])],key=lambda r:r['uid']); rng.shuffle(P)
    per=collections.Counter(); blk=set(); pick=[]
    for r in P:
        k=(r['section'],tuple(r['block']))
        if k in blk or per[r['section']]>=3: continue
        pick.append(r); blk.add(k); per[r['section']]+=1
        if len(pick)==q: break
    if len(pick)<q: short[c]=(q,len(pick))
    out+=pick
print(len(out),collections.Counter(r['comp'] for r in out),collections.Counter(c for r in out for c in r['cats']),'short',short)
json.dump([r['uid'] for r in out],open('/tmp/r5/uids2.json','w'))
json.dump({'pool':len(rows),'uncovered_after_0521':len(rest),'available':len(avail),'sampled':len(out),'short':short},open('/tmp/r5/sample2-stats.json','w'))
