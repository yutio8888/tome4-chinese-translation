import json,collections,csv,glob,re
E=json.load(open('.artifacts/i18n/term-completeness/entries.json'))
rows=[]
for f in sorted(glob.glob('terminology/*.tsv')):
    with open(f,newline='') as fh:
        for r in csv.DictReader(fh,delimiter='\t'): r['_f']=f;rows.append(r)
tsrc=collections.defaultdict(list)
for r in rows: tsrc[r['source']].append(r)
tsrc_ci={k.casefold() for k in tsrc}
NAME_TAGS=['talent name','talent type','talent category','damage type','effect subtype','birth descriptor name','faction name','stat name','resource','entity type','entity subtype','achievement name','newLore category','entity name']
# long text corpus for references
long=[x for x in E if x['tag'] in ('tformat','_t','log','logSeen','logPlayer','logCombat','say','saySimple','chat') and len(x['s'])>40]
blob='\n'.join(x['s'] for x in long)
def refs(name):
    if len(name)<4: return 0
    return len(re.findall(r'(?<![A-Za-z])'+re.escape(name)+r'(?![A-Za-z])',blob))
res={}
for tag in NAME_TAGS:
    srcs=collections.defaultdict(set)
    for x in E:
        if x['tag']==tag: srcs[x['s']].add(x['t'])
    cov=[s for s in srcs if s in tsrc]; covci=[s for s in srcs if s.casefold() in tsrc_ci]
    unc=[s for s in srcs if s.casefold() not in tsrc_ci]
    multi=[s for s in unc if len(srcs[s])>1]
    res[tag]=dict(distinct=len(srcs),covered_exact=len(cov),covered_ci=len(covci),uncovered=len(unc),uncovered_multi_target=len(multi))
    if tag in ('talent name','talent type','damage type','effect subtype','faction name','birth descriptor name','entity subtype','entity type'):
        r=sorted(((refs(s),s,sorted(srcs[s])) for s in unc),reverse=True)
        res[tag]['uncovered_referenced_ge3']=sum(1 for n,_,_ in r if n>=3)
        res[tag]['top_uncovered_by_refs']=[(n,s,t) for n,s,t in r[:15]]
        res[tag]['uncovered_multi_examples']=[(s,sorted(srcs[s])) for s in multi[:8]]
json.dump(res,open('.artifacts/i18n/term-completeness/coverage.json','w'),ensure_ascii=False,indent=1)
for k,v in res.items(): print(k,{a:b for a,b in v.items() if not isinstance(b,list)})
print('term rows',len(rows),'distinct term sources',len(tsrc))
print(collections.Counter(r['category'] for r in rows).most_common())
