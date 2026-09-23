import json,hashlib,subprocess,shutil,datetime
from pathlib import Path
from collections import Counter
root=Path.cwd();b='batch-f740e6898e8b430ca79f';tasks=[b,b+'-contextual-000'];cp=json.loads((root/'.artifacts/i18n/production-review-v2-lite/active-batch.json').read_text());assert cp['batch_id']==b and cp['phase']=='commit_ready';checks=cp['gates']['commands'];assert len(checks)==17 and all(c['exit_code']==0 for c in checks)
for c in checks:assert hashlib.sha256((root/c['log_path']).read_bytes()).hexdigest()==c['output_sha256']
h=root/'evidence/quality/production-batches'/f'{b}-host-evidence';assert not h.exists();snapshot=h/'orchestration';files=set()
for task in tasks:
 for section in ('.ai/task','.ai/reviews'):
  files.update(p for p in (root/section/task).rglob('*') if p.is_file())
prefix=root/'.artifacts/i18n/continuation-20260923'
for p in prefix.rglob('*'):
 if p.is_file() and not p.name.endswith('.pyc'):files.add(p)
files.add(root/'evidence/quality/production-batches'/f'{b}-source-workset.json')
for name in ['review254-surface','review254-contextual']:
 for r in json.loads((prefix/f'{name}-children.json').read_text()):
  assert r['archive_confirmed'] and r['output_valid']
  for a in r['create_attempts']:
   p=root/a['profiles_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['profiles_sha256'];files.add(p)
manifest=[]
for p in sorted(files):
 assert not p.is_symlink();rel=p.relative_to(root);data=p.read_bytes();target=snapshot/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);assert target.read_bytes()==data;manifest.append(dict(path=str(rel),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
(h/'snapshot-inventory.json').write_text(json.dumps(dict(files=manifest),ensure_ascii=False,indent=2)+'\n')
replay=[]
for task in tasks:
 r=subprocess.run(['python3','-B','tools/ai_state_check.py',str(snapshot/'.ai/task'/task/'STATE.json'),'--target','DONE','--workspace-root',str(snapshot)],text=True,capture_output=True);replay.append(dict(task=task,exit_code=r.returncode,output=r.stdout+r.stderr));assert r.returncode==0,(r.stdout,r.stderr)
(h/'SNAPSHOT-REPLAY.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n')
src=root/'.artifacts/i18n/production-review-v2-lite/prospective/evidence/production-review-v2-lite/batches'/b;dst=root/'evidence/production-review-v2-lite/batches'/b;assert not dst.exists();items=[]
for p in sorted(src.rglob('*')):
 if p.is_file():
  assert not p.is_symlink();rel=p.relative_to(src);data=p.read_bytes();q=dst/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data);assert q.read_bytes()==data;items.append(dict(path=str(q.relative_to(root)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
counts=Counter(json.loads(l)['final_state'] for l in (dst/'results.jsonl').read_text().splitlines());expected=json.loads((root/'.ai/task'/b/'HOST-FINAL-DECISIONS.json').read_text())['expected_final_states'];assert counts==expected,counts
(h/'PRODUCTION-COMMIT-READY.json').write_text(json.dumps(dict(batch_id=b,base_commit=cp['base_commit'],phase=cp['phase'],checks=checks,production_files=items,installed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),selected=80,final_states=dict(counts),supplemental_repair_revisions=0),ensure_ascii=False,indent=2)+'\n');shutil.copyfile(root/'.artifacts/i18n/adjudication-chain/review254-20260923-attempt01.json',h/'PRODUCTION-CHAIN.json')
shutil.copyfile(root/'.ai/task'/b/'HOST-SUMMARY.md',h/'summary.md')
for i in manifest:assert hashlib.sha256((snapshot/i['path']).read_bytes()).hexdigest()==i['sha256']
print(json.dumps(dict(snapshot_files=len(manifest),snapshot_bytes=sum(i['bytes'] for i in manifest),production_files=len(items),gates=len(checks),results=dict(counts),replay=[(r['task'],r['exit_code']) for r in replay]),ensure_ascii=False))
