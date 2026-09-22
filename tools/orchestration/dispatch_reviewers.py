#!/usr/bin/env python3
"""派发 translation_surface_screen_v1 的 REVIEWER child（每 lane / full 成员一个）。

用法：python3 -B tools/orchestration/dispatch_reviewers.py <batch_id>

身份来源全部运行时发现，**不得硬编码**：
  - parent agent id 取自环境变量 PASEO_AGENT_ID（即当前 ORCHESTRATOR 自己）
  - workspace id 按 cwd 匹配 `paseo workspace ls --json`
抄用别的 agent 的 id 会写错 lineage，STATE 的 DONE 检查会失败。

模型分工（用户指定，改前先确认）：REVIEWER = claude/claude-opus-5 thinking=medium。
必须显式传 --mode：claude 默认 Always Ask 会让 child 卡在权限弹窗上。
"""
import json, os, subprocess, sys
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _orch
from review_prompts import build_surface_prompt

from pathlib import Path

PROVIDER, THINKING, MODE = 'claude/claude-opus-5', 'medium', 'bypassPermissions'
CWD = str(Path(__file__).resolve().parents[2])

def workspace_id():
    return _orch.workspace_id()

def main():
    batch = sys.argv[1]
    parent = os.environ['PASEO_AGENT_ID']
    wks = workspace_id()
    plan = json.load(open(f'/tmp/dispatch-plan-{batch}.json'))
    agents = {}
    for task, e in plan.items():
        for lane in e['lanes']:
            did, ci, ip, idx = (lane['dispatch_id'], lane['candidate_identity'],
                                lane['input_path'], lane['index'])
            assert len(ci) == 64 and ip, (task, did, ci, ip)   # 空值绝不能被静默派出去
            prompt = build_surface_prompt(ci, ip)
            cmd = ['paseo', 'run', '--background', '--title', f'surface-{task}-{did}',
                   '--provider', PROVIDER, '--thinking', THINKING, '--mode', MODE,
                   '--workspace', wks, '--cwd', CWD,
                   '--label', f'task_id={task}', '--label', 'role=reviewer',
                   '--label', 'purpose=translation_surface_screen_v1',
                   '--label', f'candidate_identity={ci}', '--label', f'dispatch_id={did}',
                   '--label', f'lane_index={idx}',
                   '--label', f'paseo.parent-agent-id={parent}']
            if e['group']:
                cmd += ['--label', f"lane_group_identity={e['group']}"]
            cmd += ['--json', prompt]
            aid = _orch.paseo_json(cmd[1:])['agentId']
            agents.setdefault(task, {})[did] = aid
            print(task, did, aid)
            # 每派发一个立刻落盘：攒到最后再写，中途失败就会丢掉已建 agent 的记录
            _orch.write_atomic(f'/tmp/lane_agents_{batch}.json', json.dumps(agents, indent=1))
    print('dispatched', sum(len(v) for v in agents.values()))

main()
