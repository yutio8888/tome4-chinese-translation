import json, pathlib, hashlib, subprocess, shutil, sqlite3, datetime
R=pathlib.Path.cwd()
A=R/'.artifacts/i18n/continuation-20260922'
b='batch-5378d30fad3ca6f0275d'
H=R/'evidence/quality/production-batches'/f'{b}-host-evidence'
receipt=json.loads((A/'review252-finalize-timing.json').read_text())
assert receipt['exit_code']==0
assert not (R/'.artifacts/i18n/production-review-v2-lite/active-batch.json').exists()
commit=json.loads((A/'review252-evidence-commit.json').read_text())['commit']
c=sqlite3.connect(R/'.artifacts/i18n/production-review-v2-lite/queue.sqlite3')
assert c.execute('select evidence_head from meta').fetchone()[0]==commit
(H/'FINALIZE-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
cp=json.loads((A/'review252-pre-finalize-checkpoint.json').read_text())
proof=[]
for run in cp['contextual']:
 for kind in ['input','output']:
  f=pathlib.Path(run[kind+'_path'])
  target=f'evidence/production-review-v2-lite/batches/{b}/raw/contextual/004-{kind}_path.json'
  raw=subprocess.check_output(['git','show',f'{commit}:{target}'])
  assert raw==f.read_bytes()
  sha=hashlib.sha256(raw).hexdigest()
  assert sha==run[kind+'_sha256']
  proof.append(dict(runtime_path=str(f),committed_path=target,sha256=sha))
src=R/'.artifacts/i18n/production-review-v2-lite/contextual'
dst=R/'.artifacts/i18n/production-review-v2-lite/finalized-runtime-scratch'/f'{b}-contextual'
assert not dst.exists()
dst.parent.mkdir(parents=True,exist_ok=True)
shutil.move(src,dst)
(H/'RUNTIME-BOUNDARY-RECEIPT.json').write_text(json.dumps(dict(evidence_commit=commit,verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=proof,archived_directory=str(dst),reason='Preserve finalized runtime bytes while clearing the next contextual export path.'),ensure_ascii=False,indent=2)+'\n')
print('FINALIZE_RECEIPT_AND_RUNTIME_BOUNDARY_VERIFIED')
