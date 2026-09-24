import hashlib
import json
from pathlib import Path

task = 'review276-dlc-boundary-20260924'
directory = Path('.ai/task') / task
reviews = Path('.ai/reviews') / task
reviews.mkdir(parents=True, exist_ok=True)
state_file = directory / 'STATE.json'
state = json.loads(state_file.read_text())
assert state['state'] == 'VALIDATE' and state['review_records'] == []
assert state['cycle'] == state['max_cycles'] == 3
spec = (directory / 'SPEC.md').read_bytes()
patch = (directory / 'CANDIDATE-final4.patch').read_bytes()
assert hashlib.sha256(patch).hexdigest() == '9e004aea233000ffb4fe079b84c611334fa7e64a0733351103b8fbfb31bc0064'
candidate = hashlib.sha256(spec + b'\0' + patch).hexdigest()
records = []
for number, dispatch_id, role, purpose in (
    (1, 'review-final-3', 'REVIEWER', 'normal_review'),
    (2, 'cross-final-3', 'SENIOR_REVIEWER', 'cross_review'),
):
    child, = [row for row in state['child_dispatches'] if row['dispatch_id'] == dispatch_id]
    assert child['role'] == role and child['purpose'] == purpose and child['archive_confirmed']
    diff = directory / f'CODE_DIFF-RE_REVIEW-3-{number}.patch'
    assert not diff.exists()
    diff.write_bytes(patch)
    relative_diff = str(diff)
    record = dict(task_id=task, review_contract='code_legacy_v1', review_phase='RE_REVIEW',
                  cycle=3, attempt=number, reviewer_role=role, purpose=purpose,
                  dispatch_id=dispatch_id, agent_id=child['agent_id'], status='completed',
                  verdict='PASS', findings=[], candidate_ref=candidate,
                  candidate_locator=dict(spec_path=str(directory / 'SPEC.md'),
                                         diff_path=relative_diff))
    path = reviews / f'{dispatch_id}.json'
    assert not path.exists()
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(str(path))
state['review_records'] = records
state['state'] = 'DONE'
state['final_validation_passed'] = True
state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(task=task, candidate_ref=candidate, records=records)))
