#!/usr/bin/env python3
"""派发 translation_contextual_v2 的交叉复核 child，并落成 .ai/task 布局。

用法：python3 -B tools/orchestration/dispatch_contextual.py <batch_id>

前置：`production batch contextual-export` 已跑过（checkpoint 的 contextual refs 为权威）。
本脚本按 refs 逐 run 建 `.ai/task/<ctx-task>/CONTEXTUAL-ENVELOPE-final-full.json`，
派发 child，并把 `<task> <agent_id>` 写入 /tmp/ctx_agents_<batch>.txt 供 write_states.py 使用。

顺序陷阱：`contextual-import` 会先要求对应 task 的 STATE 已 DONE_VERIFIED，
所以必须 harvest → archive → write_states.py → ai_state_check → 才能 import。

模型分工（用户指定）：交叉复核 = codex/gpt-5.6-sol thinking=medium，--mode full-access。
"""
import json, os, subprocess, sys
from pathlib import Path

PROVIDER, THINKING, MODE = 'codex/gpt-5.6-sol', 'medium', 'full-access'
_here = Path(__file__).resolve()
_root = _here.parents[2] if len(_here.parents) > 2 and (_here.parents[2] / 'AGENTS.md').exists() else Path.cwd()
CWD = str(_root)
CHECKPOINT = '.artifacts/i18n/production-review-v2-lite/active-batch.json'

def workspace_id():
    out = subprocess.run(['paseo', 'workspace', 'ls', '--json'],
                         capture_output=True, text=True).stdout
    d = json.loads(out) if out.strip() else []
    rows = d.get('workspaces', []) if isinstance(d, dict) else d
    for w in rows:
        if w.get('cwd') == CWD:
            return w['workspaceId']
    raise SystemExit(f'找不到 cwd={CWD} 的 workspace')

def main():
    batch = sys.argv[1]
    parent = os.environ['PASEO_AGENT_ID']
    wks = workspace_id()
    ck = json.load(open(CHECKPOINT))
    assert ck['batch_id'] == batch, (ck['batch_id'], batch)
    lines = []
    for ref in ck['contextual'] or []:
        task = ref['task_id']
        dest = Path('.ai/task') / task / 'CONTEXTUAL-ENVELOPE-final-full.json'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(Path(ref['input_path']).read_bytes())
        ci = json.loads(dest.read_bytes())['candidate_identity']
        ip = str(dest)
        assert len(ci) == 64 and ip and ci == ref['candidate_identity']
        prompt = (
            "任务：审核 input_path 中全部冻结 revision；按其术语、上下文及所引固定源码，仅报有证据的实质语义、机制、术语、关系或跨条一致性问题；否则判 OK。\n"
            f"输入：candidate_identity={ci}；input_path={ip}。全程只读；仅读该文件、其明确引用内容及 docs/paseo-translation-context-review-v2-contract.md 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n"
            "输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 revision 并回显 identity；首字节{、末字节}，无其他文字、Markdown 或围栏。")
        assert len(prompt.encode()) <= 800, len(prompt.encode())
        cmd = ['paseo', 'run', '--background', '--title', f'contextual-{task}-full-000',
               '--provider', PROVIDER, '--thinking', THINKING, '--mode', MODE,
               '--workspace', wks, '--cwd', CWD,
               '--label', f'task_id={task}', '--label', 'role=reviewer',
               '--label', 'purpose=translation_contextual_v2',
               '--label', f'candidate_identity={ci}', '--label', 'dispatch_id=full-000',
               '--label', f'paseo.parent-agent-id={parent}', '--json', prompt]
        aid = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)['agentId']
        lines.append(f'{task} {aid}')
        print(task, 'full-000', aid)
    Path(f'/tmp/ctx_agents_{batch}.txt').write_text('\n'.join(lines) + '\n')
    print('dispatched', len(lines))

main()
