import pathlib,sys,subprocess,json,collections,hashlib,os
root=pathlib.Path('/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921');sys.path.insert(0,str(root));os.chdir(root)
from tools.i18nlib.config import load_manifest
from tools.i18nlib.runtime import LuaRuntime
from tools.i18nlib.locale_model import LocaleLoader
m=load_manifest();loader=LocaleLoader(LuaRuntime(m));head='7c38a53b88a1c80d7d9b209f84c518ae9f6eac00'
def git(*args):return subprocess.check_output(['git',*args])
manifest=json.loads(git('show','4110cbf:evidence/production-review-v2-lite/batches/batch-c7f8a5c77bbeaa7f3b89/manifest.json'));print('manifest_base',[(k,v) for k,v in manifest.items() if 'base' in k],flush=True)
base=manifest['base_commit'];files=[c.translation for c in m.components];components={c.translation:c.id for c in m.components}
def indexed(blob,path):
 rs=loader.load_bytes(blob,logical_path=path).translations;counts=collections.Counter();out={}
 for r in rs:
  k=(r['section'],r['source'],r['source_tag']);counts[k]+=1;out[k+(counts[k],)]=r
 return out
fields=['target','args_order','special'];events=collections.defaultdict(list);current={};base_rows={};removed=[];commits=git('rev-list','--reverse','--first-parent',base+'..'+head,'--',*files).decode().splitlines();print('commits',len(commits),flush=True)
for f in files:
 blob=git('show',base+':'+f);current[f]=indexed(blob,f);base_rows[f]=current[f].copy()
for n,c in enumerate(commits):
 changed=git('diff','--name-only',c+'^',c,'--',*files).decode().splitlines()
 for f in changed:
  nxt=indexed(git('show',c+':'+f),f);old=current[f]
  for k,r in nxt.items():
   if k not in old or any(r[x]!=old[k][x] for x in fields):events[(f,k)].append({'commit':c,'change':'added_or_identity_changed' if k not in old else 'modified','fields':[x for x in fields if k not in old or r[x]!=old[k][x]]})
  for k in old.keys()-nxt.keys():removed.append({'file':f,'key':list(k),'commit':c,'old':old[k]})
  current[f]=nxt
 if n%25==0:print('parsed',n+1,flush=True)
for f in files:
 final=indexed(git('show',head+':'+f),f)
 assert current[f]==final, 'history traversal did not reach snapshot: '+f
rows=[]
for (f,k),ev in events.items():
 if k not in current[f]:continue
 r=current[f][k];orig=base_rows[f].get(k);rows.append(dict(r,component=components[f],occurrence=k[-1],events=ev,baseline_target=orig['target'] if orig else None,net_changed=orig is None or any(orig[x]!=r[x] for x in fields)))
rows.sort(key=lambda r:(r['logical_path'],r['line'],r['occurrence']))
for i,r in enumerate(rows,1):r['audit_id']=f'entry-{i:05d}';r['snapshot_sha256']=hashlib.sha256(json.dumps({k:r[k] for k in ['logical_path','section','source','source_tag','target','args_order','special','occurrence']},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
out={'base_commit':base,'snapshot_commit':head,'first_production_batch':'batch-c7f8a5c77bbeaa7f3b89','commit_count':len(commits),'count':len(rows),'components':dict(collections.Counter(r['component'] for r in rows)),'net_changed':sum(r['net_changed'] for r in rows),'reverted_but_touched':sum(not r['net_changed'] for r in rows),'removed_occurrences':removed,'entries':rows}
pathlib.Path('/tmp/all-modified-inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['entries','removed_occurrences']},ensure_ascii=False),flush=True)
