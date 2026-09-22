import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
s=json.loads((P/'STATE.json').read_text());stages={}
for path in s['review_records']:
    record=json.loads(Path(path).read_text())
    if record.get('review_contract')!='translation_contextual_v2':continue
    raw=Path(record['raw_output_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==record['raw_output_sha256']
    obj=json.loads(raw);key=(record['review_phase'],record['cycle'],record['attempt'])
    st=stages.setdefault(key,dict(phase=key[0],cycle=key[1],attempt=key[2],kind='lane_group' if record['review_kind']=='lane' else record['review_kind'],members=[],raw_ok=0,raw_issue=0))
    st['members'].append(dict(dispatch_id=record['dispatch_id'],record=path,raw=record['raw_output_path'],result=record['result']))
    for v in obj['verdicts']:st['raw_ok' if v['verdict']=='OK' else 'raw_issue']+=1
out=dict(task_id=P.name,stages=list(stages.values()),senior_review_records=s['senior_review_records'],candidate_author_agent_id=s['candidate_author_agent_id'],cycle=s['cycle'],max_cycles=s['max_cycles'],current_translation_sha256=s['current_translation_sha256'],child_count=len(s['child_dispatches']),all_children_archived=all(d['archive_confirmed'] for d in s['child_dispatches']),pause_after_window7=True)
(P/'REVIEW-SUMMARY.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
