import pathlib,json,subprocess,hashlib,time
A=pathlib.Path('.artifacts/i18n/mechanics-rollback-20261003');files=['engine.lua','mod-tome.lua','tome-ashes-urhrok.lua','tome-cults.lua','tome-orcs.lua'];hashes={f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest() for f in files};checks=[('lint',['python3','-B','tools/i18n','lint','--strict']),('runtime-collisions',['python3','-B','tools/scan_runtime_collisions.py','--out-dir',str(A/'runtime-final')]),('runtime-classification',['python3','-B','tools/classify_runtime_keys.py']),('addon',['python3','-B','tools/i18n','build','--profile','addon','--component','tome','--require-complete']),('dlc-consumer',['python3','-B','tools/i18n','publish','--json']),('whitespace',['git','diff','--check'])];results=[]
for name,cmd in checks:
 r=subprocess.run(cmd,capture_output=True,text=True);results.append(dict(name=name,command=cmd,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr));print(name,r.returncode,flush=True)
 if r.returncode:break
assert hashes=={f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest() for f in files}
passed=len(results)==len(checks) and all(x['exit_code']==0 for x in results)
(A/'final-validation.json').write_text(json.dumps(dict(status='passed' if passed else 'failed',target_file_sha256=hashes,checks=results,scope='Bounded user-authorized rollback: no shared tooling or formal production changes. Canonical strict lint, runtime-key checks, core addon and real DLC dry-run consumer; external writes not authorized or performed.'),ensure_ascii=False,indent=2)+'\n')
raise SystemExit(0 if passed else 1)
