#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收割交叉复核 child 输出，过 consumer validator 后落盘并归档 child。

用法：python3 -B tools/orchestration/harvest_contextual.py <batch_id>

读 /tmp/ctx_agents_<batch>.txt（每行 `<ctx-task> <agent_id>`，由 dispatch_contextual.py 写）。
validator 拒绝的输出不落盘、计入 bad；按契约须归档该 child 并以新 dispatch_id fresh retry。
归档前先读回 provider/model/thinking 作为 runtime_observation 的证据。

三处加固（runbook §35）：
  1. 外部命令查返回码——原先 `paseo logs` 失败会静默变成「无输出」；
  2. runtime metadata 取不到就报错，不再悄悄退化成空 dict；
  3. **有 bad 就以非零码退出**——原先只打印一行 `bad: [...]` 然后正常返回 0，
     编排者按退出码判断成功时会把失败当成功。
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import _orch
from contextual_result_check import validate_result_bytes

B = sys.argv[1]
rows = [l.split() for l in pathlib.Path(f'/tmp/ctx_agents_{B}.txt').read_text().splitlines() if l.strip()]
bad = []
for task, aid in rows:
    out = _orch.paseo(['logs', aid])
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
    env = pathlib.Path(f'.ai/task/{task}/CONTEXTUAL-ENVELOPE-final-full.json').read_bytes()
    if raw is None:
        print('MISSING', task); bad.append(task); continue
    try:
        assert json.loads(raw)['candidate_identity'] == json.loads(env)['candidate_identity']
        validate_result_bytes(env, raw.encode())
    except Exception as ex:
        print('INVALID', task, ex); bad.append(task); continue
    d = pathlib.Path('.ai/reviews') / task
    d.mkdir(parents=True, exist_ok=True)
    _orch.write_atomic(d / 'raw-full-000.txt', raw)
    m = _orch.paseo_json(['agent', 'inspect', aid, '--json'])
    missing = [k for k in ('Provider', 'Model', 'Thinking', 'Mode') if not m.get(k)]
    if missing:
        print('INVALID', task, f'inspect 缺 {missing}'); bad.append(task); continue
    vs = [v['verdict'] for v in json.loads(raw)['verdicts']]
    print(task, 'ACCEPTED', len(vs), 'ISSUE=', vs.count('ISSUE'),
          '|', m['Provider'], m['Model'], m['Thinking'], m['Mode'])
    # 归档以回读为准：archive 对已归档 agent 返回 rc=1，那是幂等重跑的正常情形
    try:
        _orch.paseo(['agent', 'archive', aid])
    except SystemExit:
        pass
    if _orch.paseo_json(['agent', 'inspect', aid, '--json']).get('Archived') is not True:
        print('INVALID', task, '归档后回读 Archived 不为 true'); bad.append(task); continue
print('bad:', bad)
sys.exit(1 if bad else 0)
