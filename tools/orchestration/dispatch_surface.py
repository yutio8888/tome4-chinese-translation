#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派发 surface reviewer 并在派发时记录 agent_id（不靠事后翻日志反推）。

用法：python3 -B tools/orchestration/dispatch_surface.py <plan.json> <children.json>
"""
import json, sys, subprocess

PARENT = 'c62dba7e-1663-47e2-95d6-a7665ba7118c'
CONTRACT = 'translation_surface_screen_v1'
DOC = 'docs/paseo-translation-surface-screen-v1-contract.md'


def main():
    plan = json.load(open(sys.argv[1]))
    kids = []
    for task, v in sorted(plan.items()):
        for l in v['lanes']:
            ci, ip = l['candidate_identity'], l['input_path']
            assert len(ci) == 64, ('candidate_identity 非 64 位', l['dispatch_id'], ci)
            assert ip, ('input_path 为空', l['dispatch_id'])
            prompt = (
                '任务：筛查 input_path 中全部冻结 entry；只报告有证据的明显错译、标记/占位符破坏、'
                '参数顺序或格式等表层问题；否则判 OK。\n'
                f'输入：candidate_identity={ci}；input_path={ip}。全程只读；仅读该文件、'
                f'其明确引用内容及 {DOC} 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n'
                '输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 entry 并回显 identity；'
                '首字节{、末字节}，无其他文字、Markdown 或围栏。')
            assert len(prompt.encode('utf-8')) <= 800, ('prompt 超 800 字节', len(prompt.encode('utf-8')))
            cmd = ['paseo', 'run', '--background', '--provider', 'claude/claude-opus-5',
                   '--thinking', 'medium', '--mode', 'bypassPermissions',
                   '--workspace', 'wks_420314270844170b',
                   '--cwd', '/workspace/tome4-chinese-translation',
                   '--label', f'task_id={task}', '--label', 'role=reviewer',
                   '--label', f'purpose={CONTRACT}', '--label', f'candidate_identity={ci}',
                   '--label', f'dispatch_id={l["dispatch_id"]}',
                   '--label', f'paseo.parent-agent-id={PARENT}', '--json', prompt]
            r = subprocess.run(cmd, capture_output=True, text=True)
            o = json.loads(r.stdout)
            aid = o.get('agentId') or o.get('Id') or o.get('id') or o.get('agent_id')
            assert aid, ('派发未返回 agent id', r.stdout[:200])
            kids.append({'task_id': task, 'dispatch_id': l['dispatch_id'], 'agent_id': aid})
            print(f'{task} {l["dispatch_id"]} {aid}')
    json.dump(kids, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print('派发', len(kids), '个')


main()
