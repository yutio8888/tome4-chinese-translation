import json,hashlib,shutil,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
E=Path('evidence/quality/repair-window-7-20260922');C=E/'closure'
s=json.loads((P/'STATE.json').read_text());assert s['state']=='DONE' and s.get('publication_phase')=='complete' and all(d['archive_confirmed'] for d in s['child_dispatches'])
proof=json.loads((P/'PUBLICATION-CLOSURE.json').read_text());assert proof['verified']
assert not C.exists()
manifest=json.loads((P/'PACK-MANIFEST.json').read_text());base={r['relative_destination']:r for r in manifest['files']};excluded={r['path'] for r in manifest['excluded_diagnostics']}
files=[]
for source in sorted(P.rglob('*')):
    if not source.is_file() or str(source) in excluded or '__pycache__' in source.parts:continue
    relative=str(source)
    if relative in base and source.name!='STATE.json':
        assert hashlib.sha256(source.read_bytes()).hexdigest()==base[relative]['sha256'],relative
        continue
    target=C/'orchestration'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    files.append(dict(path=relative,sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bytes=source.stat().st_size))
attachments=C/'attachments';attachments.mkdir(parents=True)
for name in ['queue-2.log','queue-2-timing.json','push-1.log','push-1-timing.json']:
    source=Path('.artifacts/i18n/repair-window')/('window7-20260922-'+name);assert source.is_file();shutil.copyfile(source,attachments/source.name)
inventory=dict(schema_version=1,base_directory='../orchestration',base_manifest='../orchestration-pack-manifest.json',delta_directory='orchestration',state_path=str(P/'STATE.json'),files=files,publication_evidence_commit=proof['head'],publication_verified_at=proof['verified_at'],pause_after_window7=True)
(C/'snapshot-delta.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
probe=Path('.artifacts/i18n/repair-window/window7-20260922-closure-probe');assert not probe.exists()
for row in manifest['files']:
    source=E/'orchestration'/row['relative_destination'];assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'];target=probe/row['relative_destination'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
for row in files:
    source=C/'orchestration'/row['path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'];target=probe/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
args=['python3','-B','tools/ai_state_check.py',str(P/'STATE.json'),'--workspace-root',str(probe.resolve()),'--target','DONE'];r=subprocess.run(args,capture_output=True,text=True)
receipt=dict(verified=r.returncode==0,base_files=len(manifest['files']),delta_files=len(files),children=len(s['child_dispatches']),all_children_archived=True,argv=args,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
(C/'replay-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False));raise SystemExit(r.returncode)
