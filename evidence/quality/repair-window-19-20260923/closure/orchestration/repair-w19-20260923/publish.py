import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,'tools')
from contextual_result_check import validate_result_bytes
from contextual_lane_manifest import validate_manifest
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());S=P/'STATE.json';s=json.loads(S.read_text())
phase=sys.argv[1];cycle=int(sys.argv[2]);attempt=int(sys.argv[3]);R=Path('.ai/reviews')/P.name
assert all(d['archive_confirmed'] for d in s['child_dispatches'])
assert hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest()==s['current_translation_sha256']
if True:  # full stages only
 ids=[f"{'f' if phase=='FINAL_REVIEW' else 'r'}{cycle}a{attempt}"];manifest=None
else:
 assert phase in ('REVIEW','RE_REVIEW')
 mp=P/f'CONTEXTUAL-LANE-GROUP-r{cycle}a{attempt}.json';manifest=json.loads(mp.read_text());validate_manifest(manifest,manifest_path=str(mp));ids=[x['dispatch_id'] for x in manifest['payload']['lanes']]
records=[]
for did in ids:
 d=next(d for d in s['child_dispatches'] if d['dispatch_id']==did)
 assert d['archive_confirmed'] and d['lifecycle']=='archived' and d['output_valid'] and d['read_boundary_valid']
 rawpath=R/f'raw-{did}.txt';raw=rawpath.read_bytes();env=Path(d['input_path']).read_bytes();validate_result_bytes(env,raw);val=json.loads(raw)
 record=dict(task_id=P.name,review_contract='translation_contextual_v2',review_phase=phase,cycle=cycle,attempt=attempt,reviewer_role='REVIEWER',purpose='translation_contextual_v2',dispatch_id=did,agent_id=d['agent_id'],candidate_identity=d['candidate_identity'],input_path=d['input_path'],review_kind='lane' if manifest else 'full',raw_output_path=str(rawpath),raw_output_sha256=hashlib.sha256(raw).hexdigest(),result='FINDINGS' if any(v['verdict']=='ISSUE' for v in val['verdicts']) else 'PASS',workspace_id=s['workspace_id'],parent_agent_id=s['orchestrator_agent_id'],lineage_verified=True)
 if manifest:
  bound=next(b for b in manifest['payload']['lane_boundaries'] if b['index']==d['lane_index'])
  record['lane']=dict(group_id=manifest['payload']['group_id'],group_identity=manifest['group_identity'],group_manifest_path=str(mp),index=bound['index'],count=4,offset=bound['offset'],length=bound['length'])
 path=R/f'{did}.json';assert not path.exists();records.append((path,record))
for path,record in records:
 path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');s['review_records'].append(str(path))
s.update(cycle=cycle,review_phase=phase,state='ADJUDICATE')
S.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{'path':str(p),'result':r['result']} for p,r in records]))
