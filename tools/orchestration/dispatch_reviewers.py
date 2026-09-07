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
from pathlib import Path

PROVIDER, THINKING, MODE = 'claude/claude-opus-5', 'medium', 'bypassPermissions'
CWD = str(Path(__file__).resolve().parents[2])

def workspace_id():
    out = subprocess.run(['paseo', 'workspace', 'ls', '--json'],
                         capture_output=True, text=True).stdout
    d = json.loads(out) if out.strip() else []
    # CLI 返回裸数组；MCP 返回 {"workspaces":[...]}。两种都兼容。
    rows = d.get('workspaces', []) if isinstance(d, dict) else d
    for w in rows:
        if w.get('cwd') == CWD:
            return w['workspaceId']
    raise SystemExit(f'找不到 cwd={CWD} 的 workspace')

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
            prompt = (
                "任务：筛查 input_path 中全部冻结 entry；只报告有证据的明显错译、标记/占位符破坏、参数顺序或格式等表层问题；否则判 OK。\n"
                f"输入：candidate_identity={ci}；input_path={ip}。全程只读；仅读该文件、其明确引用内容及 docs/paseo-translation-surface-screen-v1-contract.md 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n"
                "输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 entry 并回显 identity；首字节{、末字节}，无其他文字、Markdown 或围栏。")
            assert len(prompt.encode()) <= 800, len(prompt.encode())   # 契约上限
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
            aid = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)['agentId']
            agents.setdefault(task, {})[did] = aid
            print(task, did, aid)
    json.dump(agents, open(f'/tmp/lane_agents_{batch}.json', 'w'), indent=1)
    print('dispatched', sum(len(v) for v in agents.values()))

main()
