#!/usr/bin/env python3
"""收割 REVIEWER 输出：取 paseo logs 里最后一个合法 JSON，逐个过 consumer validator 后落盘。

用法：python3 -B tools/orchestration/harvest_reviewers.py <batch_id>
validator 拒绝的输出**不落盘**、计入 bad 列表；按契约须归档该 child 并以新 dispatch_id fresh retry
（旧 attempt 不补写 completion record）。收割后务必 `git status --short` 确认 reviewer 未写入任何文件。
"""
import json, subprocess, sys
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _orch

from pathlib import Path
sys.path.insert(0,'tools')
from surface_screen_result_check import validate_result_bytes
B=sys.argv[1]
plan=json.load(open(f'/tmp/dispatch-plan-{B}.json'))
agents=json.load(open(f'/tmp/lane_agents_{B}.json'))
def fetch(aid):
    out=_orch.paseo(['logs',aid])
    for line in reversed(out.splitlines()):
        s=line.strip()
        if s.startswith('{') and s.endswith('}'):
            try: json.loads(s); return s
            except Exception: continue
    return None
bad=[]
for task,e in plan.items():
    d=Path('.ai/reviews')/task; d.mkdir(parents=True,exist_ok=True)
    for lane in e['lanes']:
        did=lane['dispatch_id']; aid=agents[task][did]
        raw=fetch(aid)
        if raw is None: print('MISSING',task,did); bad.append((task,did)); continue
        envb=Path(lane['input_path']).read_bytes()
        try:
            assert json.loads(raw)['candidate_identity']==json.loads(envb)['candidate_identity']
            validate_result_bytes(envb, raw.encode())
        except Exception as ex:
            print('INVALID',task,did,ex); bad.append((task,did)); continue
        (d/f'raw-{did}.txt').write_text(raw)
        vs=[r['verdict'] for r in json.loads(raw)['results']]
        print(task, did, 'ACCEPTED', len(vs), 'ISSUE=', vs.count('ISSUE'))
print('bad:', bad)
