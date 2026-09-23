import pathlib,json,subprocess,hashlib,datetime,re
b='batch-8963e835a427bdbf7ae1';A=pathlib.Path('.artifacts/i18n/continuation-20260923');H=pathlib.Path('evidence/quality/production-batches')/(b+'-host-evidence');paths=[f'evidence/production-review-v2-lite/batches/{b}',str(H),f'evidence/quality/production-batches/{b}-source-workset.json']
prior=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines(); assert all(any(f==p or f.startswith(p+'/') for p in paths) for f in prior)
subprocess.run(['git','add','-f','--']+paths,check=True)
staged=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert staged and all(any(f==p or f.startswith(p+'/') for p in paths) for f in staged)
for item in json.loads((H/'snapshot-inventory.json').read_text())['files']:
 f=str(H/'orchestration'/item['path']); assert f in staged; assert hashlib.sha256(subprocess.check_output(['git','show',':'+f])).hexdigest()==item['sha256']
r=subprocess.run(['git','diff','--cached','--check'],capture_output=True,text=True);(A/'review263-staged-whitespace.txt').write_text(r.stdout+r.stderr)
assert r.returncode in (0,2);exceptions=[];manifest={i['path']:i for i in json.loads((H/'snapshot-inventory.json').read_text())['files']}
for line in r.stdout.splitlines():
 m=re.match(r'(.+?):(\d+): (trailing whitespace\.|new blank line at EOF\.)$',line)
 if not m:continue
 f,lineno,why=m.groups();prefix=str(H/'orchestration')+'/';assert f.startswith(prefix),line;original=f[len(prefix):];assert original in manifest,original
 data=subprocess.check_output(['git','show',':'+f]);sha=hashlib.sha256(data).hexdigest();assert sha==manifest[original]['sha256']==hashlib.sha256(pathlib.Path(original).read_bytes()).hexdigest();exceptions.append(dict(path=f,line=int(lineno),reason=why,original=original,sha256=sha,disposition='preserve exact archived evidence bytes; do not rewrite frozen input or original log'))
if r.returncode:assert exceptions and len([l for l in r.stdout.splitlines() if re.match(r'.+:\d+: ',l)])==len(exceptions)
(A/'review263-staging-verification.json').write_text(json.dumps(dict(verified=True,verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),staged_files=staged,raw_whitespace_exit_code=r.returncode,immutable_artifact_exceptions=exceptions,remaining_staged_whitespace_issues=0),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(staged_files=len(staged),raw_whitespace_exit_code=r.returncode,archival_exceptions=exceptions),ensure_ascii=False))
