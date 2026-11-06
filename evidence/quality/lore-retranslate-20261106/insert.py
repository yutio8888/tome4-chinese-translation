import sys,os;sys.path.insert(0,'tools');sys.path.insert(0,'/tmp/gem-lore');sys.argv=['x']
import lite_review as L
from mirror import mirror
IDS=os.environ['IDS'].split()
E={u['unit_id'][:12]:L.entry(u) for u in L.units() if u['unit_id'][:12] in IDS+['1c73f145ab27']}
def lit(t):
  for d in ['[[%s]]','[=[%s]=]']:
    o=d%t
    if (']]' if d=='[[%s]]' else ']=]') not in t: yield o
for k in IDS:
  e=E[k]; new=open(f'/tmp/gem-lore/{k}/out.txt',encoding='utf-8').read()
  if not e['source'].endswith('\n'): new=new.rstrip('\n')
  jobs=[(e,new)]
  if k=='4ca4e02e13e6': jobs.append((E['1c73f145ab27'],mirror(new)))
  for e,new in jobs:
    p=e['translation_file']; s=open(p,encoding='utf-8').read()
    cur=e['target']; done=False
    for d in ['[[%s]]','[=[%s]=]','[==[%s]==]']:
      o=d%cur
      if s.count(o)==1:
        assert d.replace('%s','').strip('[]')=='' or True
        close=d.split('%s')[1]
        assert close not in new, (k,'delimiter in text')
        nd=d if not new.endswith(']') else '[=[%s]=]'
        if nd!=d: assert ']=]' not in new
        s=s.replace(o,nd%new); done=True; break
    assert done,(k,'target not found uniquely')
    open(p,'w',encoding='utf-8').write(s); print('inserted',k,p)
