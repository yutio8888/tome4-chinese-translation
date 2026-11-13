import json,re,collections
ROOT='/workspace/tome4-chinese-translation/'
U=json.load(open(ROOT+'.artifacts/i18n/fulltext-20261113/units.json'))
live=[u for u in U if u['disposition']=='release-required']
pat=re.compile(r'^t\(',re.M)
lines_cache={}
def calls(path):
    if path in lines_cache: return lines_cache[path]
    s=open(ROOT+path,encoding='utf-8').read()
    starts=[m.start() for m in pat.finditer(s)]
    nl=[0]+[i+1 for i,c in enumerate(s) if c=='\n']
    import bisect
    res=[bisect.bisect_right(nl,p) for p in starts]
    lines_cache[path]=(s,starts,res); return lines_cache[path]
out=[];bad=0
for u in live:
    o=u['occurrence']; s,starts,res=calls(o['translation_path'])
    i=o['document_ordinal']; line=res[i] if i<len(res) else None
    out.append(dict(comp=o['component'],file=o['translation_path'],line=line,ord=i,section=o['section'],source=o['source'],target=o['target'],tag=o['source_tag'],uid=u['unit_id'][:12]))
# verify sample: source first 20 chars appear near line
s0=0
for e in out[::500]:
    s,starts,res=calls(e['file']); txt=s.split('\n')[e['line']-1] if e['line'] else ''
    if e['source'][:15].replace('\n','') not in txt and e['source'][:10] not in txt: s0+=1
print(len(out),'sample mismatches',s0,'of',len(out[::500]))
json.dump(out,open('/tmp/ft/live.json','w'),ensure_ascii=False)
