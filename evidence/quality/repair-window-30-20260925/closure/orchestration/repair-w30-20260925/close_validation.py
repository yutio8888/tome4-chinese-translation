import json,hashlib,subprocess,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());s=json.loads((P/'STATE.json').read_text())
assert json.loads((P/'FINAL-GATES-timing.json').read_text())['exit_code']==0
line=(P/'FINAL-GATES.log').read_text().splitlines()[0];gate_dir=Path(line.split(': ',1)[1]).resolve().relative_to(Path.cwd().resolve());path=gate_dir/'results.json';g=json.loads(path.read_text())
assert g['complete'] is True and g['success'] is True and g['binding']['skip_build'] is False and len(g['checks'])==17
for check in g['checks']:assert check['exit_code']==0 and hashlib.sha256(Path(check['log_path']).read_bytes()).hexdigest()==check['output_sha256']
assert {f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in ['tome-ashes-urhrok.lua']}==s['current_translation_sha256']
assert all(d['archive_confirmed'] for d in s['child_dispatches'])
assert s['completed_review_contracts']==['translation_contextual_v2'] and not s['pending_review_contracts']
assert not s['open_accepted_findings'] and not s['deferred_findings']
receipt=dict(verified=True,checks=17,all_log_hashes_verified=True,translation_sha256=s['current_translation_sha256'],results_path=str(path),results_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),strict_build=True)
(P/'HOST-GATES-VERIFIED.json').write_text(json.dumps(receipt,indent=2)+'\n')
s.update(state='DONE',final_validation_passed=True,final_gate_results_path=str(path),final_gate_results_sha256=receipt['results_sha256'])
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
r=subprocess.run(['python3','-B','tools/ai_state_check.py',str(P/'STATE.json'),'--target','DONE'],capture_output=True,text=True)
(P/'DONE-check.json').write_text(json.dumps(dict(argv=r.args,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr),indent=2)+'\n');print(r.stdout,r.stderr);assert r.returncode==0
shutil.copyfile(P/'STATE.json',P/'STATE-review-validation-checkpoint.json')
