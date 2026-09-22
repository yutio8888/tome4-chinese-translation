import pathlib,json,subprocess,hashlib,datetime,re
P=pathlib.Path(__file__).resolve().parent.relative_to(pathlib.Path.cwd().resolve())
E=pathlib.Path('evidence/quality/repair-window-7-20260922')
m=json.loads(pathlib.Path('.artifacts/i18n/repair-window/window7-20260922-migration.json').read_text())
paths=[str(E),'handoff.md','evidence/production-review-v2-lite/catalog/entries.jsonl','evidence/production-review-v2-lite/catalog/exclusions.jsonl','evidence/production-review-v2-lite/catalog/manifest.json','i18n/quality/production-review-v2-lite/catalog-v1.schema.json','i18n/quality/production-review-v2-lite/policy-v1.json',m['target_path']]
prior=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert not prior,prior
subprocess.run(['git','add','-f','--']+paths,check=True)
staged=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines()
assert staged and all(any(f==p or f.startswith(p+'/') for p in paths) for f in staged)
manifest=json.loads((P/'PACK-MANIFEST.json').read_text())
archive_map={str(E/'orchestration'/i['relative_destination']):i for i in manifest['files']}
for f,item in archive_map.items():
    assert f in staged,f
    assert hashlib.sha256(subprocess.check_output(['git','show',':'+f])).hexdigest()==item['sha256']
r=subprocess.run(['git','diff','--cached','--check'],capture_output=True,text=True)
(P/'PUBLICATION-STAGED-WHITESPACE.txt').write_text(r.stdout+r.stderr)
assert r.returncode in (0,2);exceptions=[]
for line in r.stdout.splitlines():
    match=re.match(r'(.+?):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',line)
    if not match:continue
    f,num,reason=match.groups();assert f in archive_map,line
    item=archive_map[f];data=subprocess.check_output(['git','show',':'+f]);sha=hashlib.sha256(data).hexdigest()
    assert sha==item['sha256']==hashlib.sha256(pathlib.Path(item['source']).read_bytes()).hexdigest()
    exceptions.append(dict(path=f,line=int(num),reason=reason,source=item['source'],sha256=sha,disposition='preserve exact immutable evidence bytes'))
if r.returncode:assert exceptions and len([l for l in r.stdout.splitlines() if re.match(r'.+:\d+: ',l)])==len(exceptions)
report=dict(verified=True,verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),staged_files=staged,snapshot_files=len(archive_map),all_indexed_snapshot_hashes_verified=True,raw_whitespace_exit_code=r.returncode,immutable_artifact_exceptions=exceptions,remaining_staged_whitespace_issues=0)
(P/'PUBLICATION-STAGING-VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(staged_files=len(staged),snapshot_files=len(archive_map),raw_whitespace_exit_code=r.returncode,exceptions=exceptions),ensure_ascii=False))
