import json,collections,sys
R='/workspace/tome4-chinese-translation/'
U=json.load(open('/tmp/r4/units.json'))
live=[u for u in U if u['disposition']=='release-required']
dead=set()
for pr in json.load(open(R+'evidence/quality/dead-key-scan-20261111/pairs.json')):
    x=pr['dead']; dead.add((x['file'],x['en'],x['tag']))
def isdead(o): return (o['translation_path'],o['source'],str(o['source_tag'])) in dead or (o['translation_path']=='engine.lua' and o['source'].startswith('following chain'))
nd=0; out=[]
for u in live:
    o=u['occurrence']
    if isdead(o): nd+=1; continue
    s,t=o['source'],o['target']
    if s.count('\n')!=t.count('\n'):
        out.append(dict(uid=u['unit_id'],comp=o['component'],file=o['translation_path'],section=o['section'],tag=o['source_tag'],src_nl=s.count('\n'),tgt_nl=t.count('\n')))
print('release-required',len(live),'dead excluded',nd,'mismatch',len(out))
print(collections.Counter(e['comp'] for e in out)); print(sorted(collections.Counter(e['tgt_nl']-e['src_nl'] for e in out).items()))
print('unique uid',len(set(e['uid'] for e in out)))
json.dump(out,open('/tmp/r4/nlfamily.json','w'),ensure_ascii=False,indent=0)
json.dump([e['uid'][:12] for e in out],open('/tmp/r4/uids.json','w'))
