import json,re,csv,glob,collections
E=json.load(open('.artifacts/i18n/term-completeness/entries.json'))
rows=[r for f in glob.glob('terminology/*.tsv') for r in csv.DictReader(open(f,newline=''),delimiter='\t')]
T={r['source'].casefold() for r in rows}
LONG=('tformat','_t','log','logSeen','logPlayer','logCombat','say','saySimple','chat','delayedLogMessage','newLore category','init.lua load_tips')
long=[x for x in E if x['tag'] in LONG and len(x['s'])>len('')+20]
def strip(s): return re.sub(r'#[A-Za-z0-9_]+#|#\{[a-z]+\}#','',s)
def cites(name,cs=True):
    p=re.compile(r'(?<![A-Za-z0-9_])'+re.escape(name)+r'(?![A-Za-z0-9_])',0 if cs else re.I)
    return [x for x in long if x['s']!=name and p.search(strip(x['s']))]
def scope(comps):
    d={'ashes-urhrok','cults','items-vault','orcs','possessors'}
    if comps<=d: return 'dlc'
    if not comps&d: return 'core'
    return 'multi'
out=[]
def add(kind,src,tag,minrefs,cs=True):
    defs=[x for x in E if x['s']==src and x['tag']==tag]
    tg=sorted({x['t'] for x in defs})
    cs_=cites(src,cs)
    if len(cs_)<minrefs: return
    tgt=tg[0]
    ok=[x for x in cs_ if tgt in x['t']]
    bad=[x for x in cs_ if tgt not in x['t']]
    out.append(dict(kind=kind,source=src,tag=tag,targets=tg,comps=sorted({x['c'] for x in defs}),scope=scope({x['c'] for x in defs}),refs=len(cs_),consistent=len(ok),
      bad_samples=[(x['c'],re.search(r'.{0,30}'+re.escape(src)+r'.{0,20}',strip(x['s']),re.I).group(0) if re.search(re.escape(src),strip(x['s']),re.I) else '',x['t'][:80]) for x in bad[:4]]))
tal=sorted({x['s'] for x in E if x['tag']=='talent name' and x['s'].casefold() not in T and ' ' in x['s']})
for s in tal: add('talent',s,'talent name',2)
ent=sorted({x['s'] for x in E if x['tag']=='entity name' and re.match(r'^[A-Z]',x['s']) and x['s'].casefold() not in T and len(x['s'])>=5})
for s in ent: add('entity',s,'entity name',3)
add('entity','losgoroth','entity name',1,cs=False)
json.dump(out,open('.artifacts/i18n/term-completeness/candidates.json','w'),ensure_ascii=False,indent=1)
for k in ('talent','entity'):
    xs=[o for o in out if o['kind']==k]
    print(k,len(xs),'fully consistent',sum(o['refs']==o['consistent'] for o in xs),'multi-target',sum(len(o['targets'])>1 for o in xs))
