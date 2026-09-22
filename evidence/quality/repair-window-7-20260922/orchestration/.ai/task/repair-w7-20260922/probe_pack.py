import json,hashlib,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
root=Path('.artifacts/i18n/repair-window/window7-20260922-snapshot-probe')
assert not root.exists()
m=json.loads((P/'PACK-MANIFEST.json').read_text())
for row in m['files']:
    raw=Path(row['source']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
    target=root/row['relative_destination'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
args=['python3','-B','tools/ai_state_check.py',str(P/'STATE.json'),'--workspace-root',str(root.resolve()),'--target','DONE']
r=subprocess.run(args,capture_output=True,text=True)
out=dict(files=len(m['files']),bytes=m['total_bytes'],argv=args,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
(P/'PACK-REPLAY-PROBE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False));raise SystemExit(r.returncode)
