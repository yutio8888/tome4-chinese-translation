import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,'tools')
from contextual_result_check import validate_result_bytes
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());s=json.loads((P/'STATE.json').read_text())
did=sys.argv[1];phase=sys.argv[2];cycle=int(sys.argv[3]);attempt=int(sys.argv[4])
assert all(x['archive_confirmed'] for x in s['child_dispatches'])
d=next(x for x in s['child_dispatches'] if x['dispatch_id']==did);assert d['output_valid'] and d['read_boundary_valid']
assert hashlib.sha256(Path('tome-cults.lua').read_bytes()).hexdigest()==s['current_translation_sha256']
rp=Path('.ai/reviews')/P.name/f'raw-{did}.txt';raw=rp.read_bytes();validate_result_bytes(Path(d['input_path']).read_bytes(),raw);val=json.loads(raw)
record=dict(task_id=P.name,review_contract='translation_contextual_v2',review_phase=phase,cycle=cycle,attempt=attempt,reviewer_role='REVIEWER',purpose='translation_contextual_v2',dispatch_id=did,agent_id=d['agent_id'],candidate_identity=d['candidate_identity'],input_path=d['input_path'],review_kind='full',raw_output_path=str(rp),raw_output_sha256=hashlib.sha256(raw).hexdigest(),result='FINDINGS' if any(x['verdict']=='ISSUE' for x in val['verdicts']) else 'PASS',workspace_id=s['workspace_id'],parent_agent_id=s['orchestrator_agent_id'],lineage_verified=True)
dest=rp.parent/f'{did}.json';assert not dest.exists();dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');s['review_records'].append(str(dest));s.update(state='ADJUDICATE',review_phase=phase,cycle=cycle);(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print(record['result'])
