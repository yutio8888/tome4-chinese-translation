import json,hashlib
from pathlib import Path

P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
R=Path('.ai/reviews')/P.name
checkpoint=P/'STATE-review-validation-checkpoint.json'
s=json.loads(checkpoint.read_text())
assert s['state']=='DONE' and s['final_validation_passed'] is True
assert all(d['archive_confirmed'] for d in s['child_dispatches'])
assert not (P/'PACK-MANIFEST.json').exists()
commit=json.loads((P/'TRANSLATION-COMMIT.json').read_text())['translation_commit']
files=[]
excluded=[]
destinations=set()
def add(source,dest=None):
    assert source.is_file() and not source.is_symlink()
    relative=str(dest or source)
    assert relative not in destinations,relative
    destinations.add(relative)
    raw=source.read_bytes()
    files.append(dict(source=str(source),relative_destination=relative,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
for source in sorted(P.rglob('*')):
    if not source.is_file():
        continue
    relative=source.relative_to(P)
    if source.name=='STATE.json':
        add(checkpoint,source)
    elif source.name=='BASELINE-records.json' or source.name.startswith('BEFORE-FIX-') or relative.parts[0]=='baseline' or '__pycache__' in relative.parts:
        excluded.append(dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),reason='Regenerable full baseline/intermediate translation copy or bytecode; exact accepted changes, baseline commit, frozen inputs and validations are retained.'))
    else:
        add(source)
for source in sorted(R.rglob('*')):
    if source.is_file():
        add(source)
# superseded STOP task repair-w10-20260923 (max_cycles not converged) is archived alongside
O=Path('.ai/task/repair-w10-20260923');OR=Path('.ai/reviews/repair-w10-20260923')
assert json.loads((O/'STATE.json').read_text())['state']=='STOP'
cand=O/'CANDIDATE-FINAL-mod-tome.lua'
assert hashlib.sha256(cand.read_bytes()).hexdigest()==hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest()
for source in sorted(O.rglob('*')):
    if not source.is_file():
        continue
    relative=source.relative_to(O)
    if source==cand or source.name=='BASELINE-records.json' or relative.parts[0]=='baseline' or '__pycache__' in relative.parts:
        excluded.append(dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),reason='Superseded task: full baseline copy, bytecode, or full candidate mod-tome.lua copy byte-identical to the translation commit.'))
    else:
        add(source)
for source in sorted(OR.rglob('*')):
    if source.is_file():
        add(source)
old_gates=Path((O/'FINAL-GATES.log').read_text().splitlines()[0].split(': ',1)[1]).resolve().relative_to(Path.cwd().resolve())/'results.json'
gate_paths=[s['final_gate_results_path'],str(old_gates)]+[r['results_path'] for r in s.get('prior_gate_runs',[])]
for value in dict.fromkeys(gate_paths):
    result_path=Path(value)
    result=json.loads(result_path.read_text())
    add(result_path)
    for row in result['checks']:
        log=Path(row['log_path'])
        assert hashlib.sha256(log.read_bytes()).hexdigest()==row['output_sha256']
        add(log)
manifest=dict(schema_version=1,snapshot_meaning='Immutable review-validation checkpoint before publication child; preserves accepted reviews, rejected attempts, source adjudication, scope audit, all gate runs and all confirmed archives.',translation_commit=commit,files=files,total_bytes=sum(x['bytes'] for x in files),excluded_diagnostics=excluded)
(P/'PACK-MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(files=len(files),bytes=manifest['total_bytes'],excluded=len(excluded))))
