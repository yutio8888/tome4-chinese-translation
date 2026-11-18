import hashlib, json, re, sys, zipfile, os, subprocess
from pathlib import Path
REPO=Path('/workspace/tome4-chinese-translation'); ROOT=Path('/workspace/tome4-dlcs')
PKG=Path('/home/paseo/tome-live/t-engine4-linux64-1.7.6/game/addons')
COMP={'ashes':('ashes-urhrok/tome-ashes-urhrok','tome-ashes-urhrok.teaa'),
      'cults':('cults/tome-cults','tome-cults.teaa'),'orcs':('orcs/tome-orcs','tome-orcs.teaa')}
sha=lambda b: hashlib.sha256(b).hexdigest()
def refs():
    out={}
    d=json.load(open(REPO/'evidence/lite-review/batches/0523/input.json'))
    for e in d['entries']:
        m=re.match(r'(/workspace/tome4-dlcs/\S+)',e['source_file'])
        if m: out.setdefault(m.group(1),set()).add('0523')
    # 0511 maintenance notes: DLC files cited
    for rel in [] and ['cults/tome-cults/data/timed_effects.lua','cults/tome-cults/data/general/objects/world-artifacts.lua',
                'orcs/tome-orcs/data/talents/steam/other.lua','orcs/tome-orcs/data/talents/steam/artillery.lua',
                'orcs/tome-orcs/data/talents/steam/turrets.lua','orcs/tome-orcs/data/talents/steam/gadgets.lua']:
        out.setdefault(str(ROOT/rel),set()).add('0511')
    return out
res={'generated':'2026-11-18','note':'Local fingerprints only. /workspace/tome4-dlcs has no .git metadata (public DLC checkout source historically unpinned); package comparison is against the locally installed t-engine4-linux64-1.7.6 addons, read-only. Hash equality is not a verification of official upstream provenance.',
     'checkout_root':str(ROOT),'git_head':None,'components':{},'files':[]}
for c,(sub,pkg) in COMP.items():
    init=ROOT/sub/'init.lua'; meta={}
    if init.exists():
        t=init.read_text(errors='replace')
        for k in ('long_name','short_name','version','addon_version','tags','weight'):
            m=re.search(r'^\s*'+k+r'\s*=\s*(.+)$',t,re.M)
            if m: meta[k]=m.group(1).strip()
        meta['init_sha256']=sha(init.read_bytes())
    p=PKG/pkg
    res['components'][c]={'checkout':str(ROOT/sub),'init':meta,'package':str(p),'package_sha256':sha(p.read_bytes()) if p.exists() else None,'package_size':p.stat().st_size if p.exists() else None}
for f,batches in sorted(refs().items()):
    fp=Path(f); c=next(k for k,(sub,_) in COMP.items() if f.startswith(str(ROOT/sub)))
    sub,pkg=COMP[c]; rel=str(fp.relative_to(ROOT/sub))
    rec={'component':c,'path':f,'batches':sorted(batches),'exists':fp.exists()}
    if fp.exists(): rec['sha256']=sha(fp.read_bytes()); rec['size']=fp.stat().st_size
    try:
        z=zipfile.ZipFile(PKG/pkg); names=z.namelist()
        cand=[n for n in names if n.rstrip('/').endswith(rel)]
        if cand:
            b=z.read(cand[0]); rec['package_member']=cand[0]; rec['package_member_sha256']=sha(b)
            rec['matches_package']= rec.get('sha256')==sha(b)
        else: rec['package_member']=None; rec['matches_package']=None
    except Exception as ex: rec['package_error']=str(ex)
    res['files'].append(rec)
fs=res['files']
res['summary']={'files':len(fs),'missing':sum(not r['exists'] for r in fs),
 'match_package':sum(r.get('matches_package') is True for r in fs),
 'differ_from_package':[r['path'] for r in fs if r.get('matches_package') is False],
 'not_in_package':[r['path'] for r in fs if r.get('matches_package') is None],
 'aggregate_sha256':sha(''.join(f"{r['path']}\t{r.get('sha256')}\n" for r in fs).encode())}
json.dump(res,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(json.dumps(res['components'],ensure_ascii=False,indent=1)); print(json.dumps(res['summary'],ensure_ascii=False,indent=1))
