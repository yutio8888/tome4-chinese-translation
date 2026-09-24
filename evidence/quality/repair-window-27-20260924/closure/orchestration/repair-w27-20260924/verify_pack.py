import hashlib,json,subprocess
from pathlib import Path
P=Path('.ai/task/repair-w27-20260924')
E=Path('evidence/quality/repair-window-27-20260924')
manifest=json.loads((P/'PACK-MANIFEST.json').read_text())
assert (E/'orchestration-pack-manifest.json').read_bytes()==(P/'PACK-MANIFEST.json').read_bytes()
for row in manifest['files']:
    raw=Path(row['source']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['sha256'],row['source']
    assert (E/'orchestration'/row['relative_destination']).read_bytes()==raw,row['relative_destination']
candidate=Path('.artifacts/i18n/repair-window/window27-20260924-candidate-catalog')
for file in candidate.rglob('*'):
    if file.is_file():
        destination=file.relative_to(candidate)
        assert destination.read_bytes()==file.read_bytes(),str(destination)
source=Path('.artifacts/i18n/repair-window/window27-20260924-migration.json')
migration=json.loads(source.read_text())
destination=Path('evidence/production-review-v2-lite/migrations')/(migration['migration_id']+'.json')
assert destination.read_bytes()==source.read_bytes()
commit=json.loads((P/'TRANSLATION-COMMIT.json').read_text())['translation_commit']
for name in ['mod-tome.lua','tome-ashes-urhrok.lua']:
    committed=subprocess.check_output(['git','show',commit+':'+name])
    assert committed==Path(name).read_bytes()
allowed={'handoff.md','evidence/quality/pending-user-review.md','evidence/production-review-v2-lite/catalog/entries.jsonl','evidence/production-review-v2-lite/catalog/exclusions.jsonl','evidence/production-review-v2-lite/catalog/manifest.json','i18n/quality/production-review-v2-lite/catalog-v1.schema.json','i18n/quality/production-review-v2-lite/policy-v1.json'}
modified=subprocess.check_output(['git','diff','--name-only','HEAD'],text=True).splitlines()
assert all(path in allowed or path.startswith(str(E)+'/') for path in modified),modified
replays=[]
for task in [P]:
    args=['python3','-B','tools/ai_state_check.py',str(task/'STATE.json'),'--workspace-root',str((E/'orchestration').resolve()),'--target','DONE']
    result=subprocess.run(args,capture_output=True,text=True)
    replays.append(dict(task_id=task.name,argv=args,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
report=dict(verified=all(r['exit_code']==0 for r in replays),snapshot_files=len(manifest['files']),snapshot_bytes=sum(r['bytes'] for r in manifest['files']),snapshot_hashes_verified=True,catalog_and_migration_exact_copy=True,translation_matches_commit=commit,modified_tracked_paths=modified,snapshot_replays=replays)
(P/'PACK-HOST-VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if report['verified'] else 1)
