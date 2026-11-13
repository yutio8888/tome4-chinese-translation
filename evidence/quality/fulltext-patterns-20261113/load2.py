import json,collections
ROOT='/workspace/tome4-chinese-translation/'
E=json.load(open('/tmp/ft/live.json'))
files={}
def lines(p):
    if p not in files: files[p]=open(ROOT+p,encoding='utf-8').read().split('\n')
    return files[p]
def esc(s): return s.replace('\\','\\\\').replace('"','\\"')
seen=collections.Counter(); miss=0
idx={}
for e in sorted(E,key=lambda e:(e['file'],e['ord'])):
    L=lines(e['file']); key=e['source'].split('\n')[0]
    cands=[]
    for form in ('t("'+esc(key), 't([['+key, 't([=['+key, 't([==['+key):
        k=(e['file'],form[:80])
        if k not in idx: idx[k]=[i+1 for i,l in enumerate(L) if l.startswith(form[:80])]
        cands+=idx[k]
    cands=sorted(set(cands))
    n=seen[(e['file'],key)]; seen[(e['file'],key)]+=1
    e['line']=cands[min(n,len(cands)-1)] if cands else None
    if not cands: miss+=1
print('unlocated',miss,'of',len(E))
json.dump(E,open('/tmp/ft/live.json','w'),ensure_ascii=False)
