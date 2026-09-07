#!/usr/bin/env python3
"""收割交叉复核 child 输出，过 consumer validator 后落盘并归档 child。

用法：python3 -B tools/orchestration/harvest_contextual.py <batch_id>

读 /tmp/ctx_agents_<batch>.txt（每行 `<ctx-task> <agent_id>`，由 dispatch_contextual.py 写）。
validator 拒绝的输出不落盘、计入 bad；按契约须归档该 child 并以新 dispatch_id fresh retry。
归档前先读回 provider/model/thinking 作为 runtime_observation 的证据。
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, 'tools')
from contextual_result_check import validate_result_bytes

B = sys.argv[1]
rows = [l.split() for l in Path(f'/tmp/ctx_agents_{B}.txt').read_text().splitlines() if l.strip()]
bad = []
for task, aid in rows:
    out = subprocess.run(['paseo', 'logs', aid], capture_output=True, text=True).stdout
    raw = None
    for line in reversed(out.splitlines()):
        s = line.strip()
        if s.startswith('{') and s.endswith('}'):
            try:
                json.loads(s)
                raw = s
                break
            except Exception:
                continue
    env = Path(f'.ai/task/{task}/CONTEXTUAL-ENVELOPE-final-full.json').read_bytes()
    if raw is None:
        print('MISSING', task); bad.append(task); continue
    try:
        assert json.loads(raw)['candidate_identity'] == json.loads(env)['candidate_identity']
        validate_result_bytes(env, raw.encode())
    except Exception as ex:
        print('INVALID', task, ex); bad.append(task); continue
    d = Path('.ai/reviews') / task
    d.mkdir(parents=True, exist_ok=True)
    (d / 'raw-full-000.txt').write_text(raw)
    meta = subprocess.run(['paseo', 'agent', 'inspect', aid, '--json'],
                          capture_output=True, text=True).stdout
    m = json.loads(meta) if meta.strip().startswith('{') else {}
    vs = [v['verdict'] for v in json.loads(raw)['verdicts']]
    print(task, 'ACCEPTED', len(vs), 'ISSUE=', vs.count('ISSUE'),
          '|', m.get('Provider'), m.get('Model'), m.get('Thinking'), m.get('Mode'))
    subprocess.run(['paseo', 'agent', 'archive', aid], capture_output=True, text=True)
print('bad:', bad)
