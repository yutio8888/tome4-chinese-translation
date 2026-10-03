import pathlib,json,gzip,hashlib,shutil
D=pathlib.Path('.ai/task/awkward-explanations-adjust-20261003');A=pathlib.Path('.artifacts/i18n/awkward-explanations-adjust-20261003');R=pathlib.Path('.ai/reviews/awkward-explanations-adjust-20261003');O=pathlib.Path('evidence/quality/awkward-explanations-adjust-20261003');mapping=[]
def mirror(p,dest):
 dest.parent.mkdir(parents=True,exist_ok=True);encoded=p.suffix in ['.patch','.txt'];raw=p.read_bytes()
 if encoded:dest=dest.with_name(dest.name+'.gz');dest.write_bytes(gzip.compress(raw,mtime=0))
 else:dest.write_bytes(raw)
 mapping.append(dict(original_path=str(p),tracked_path=str(dest),sha256=hashlib.sha256(raw).hexdigest(),storage_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),encoding='gzip' if encoded else 'identity'))
for src,sub in [(D,'task'),(R,'reviews'),(A,'dispatch-evidence')]:
 for p in sorted(src.iterdir()):
  if p.is_file() and p.name not in ['validation-native-outputs.json','validation-runtime-build-native.json']:mirror(p,O/sub/p.name)
for r in json.load(open(A/'proposal-validation.json')):
 p=pathlib.Path(r['command'][r['command'].index('--workset')+1]);mirror(p,O/'worksets'/p.name)
for name in ['adjust-verify.py','adjust-proposals.py','adjust-freeze.py','adjust-package.py']:
 p=pathlib.Path('/tmp')/name;mirror(p,O/'helpers'/name)
(O/'ARTIFACT-MAP.json').write_text(json.dumps(dict(files=mapping,recovery='Exact bytes mirrored; decompress gzip entries to original_path in a separate audit checkout. Four Lua baselines are recoverable at BASELINE.head. Helpers document host verification; manual proposal input is an adapter, not an extractor/source-correctness claim. Never overwrite a live task during replay.'),ensure_ascii=False,indent=2)+'\n');print(len(mapping),'files mirrored')
