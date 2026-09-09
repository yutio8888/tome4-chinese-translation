#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派发 surface reviewer，派发前后各落一次盘（不靠事后翻日志反推 agent）。

用法：python3 -B tools/orchestration/dispatch_surface.py <plan.json> <children.json>
环境：TOME_ORCH_PARENT_AGENT_ID、TOME_PASEO_WORKSPACE

崩溃安全（runbook §35.1）：原实现把 kids 攒在内存里、循环结束才写文件，
中途任何一次失败都会让「已经建出来的 agent」失去记录，只能事后翻日志反推。
现在每个 lane 派发**之前**先写一条 status=dispatching 的意图记录，
派发**之后**立刻改写成 dispatched 并带上 agent_id。
任何时刻中断，children.json 都能说明哪些 lane 已经有、或可能有在跑的 agent。

重跑幂等：已 dispatched 的 lane 直接跳过；遇到 dispatching 残留则停下来要求人工核对，
因为那正是「可能已经建了 agent 但没记下 id」的状态，盲目重跑会产生重复 agent。
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _orch

CONTRACT = 'translation_surface_screen_v1'
DOC = 'docs/paseo-translation-surface-screen-v1-contract.md'


def build_prompt(ci, ip):
    prompt = (
        '任务：筛查 input_path 中全部冻结 entry；只报告有证据的明显错译、标记/占位符破坏、'
        '参数顺序或格式等表层问题；否则判 OK。\n'
        f'输入：candidate_identity={ci}；input_path={ip}。全程只读；仅读该文件、'
        f'其明确引用内容及 {DOC} 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n'
        '输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 entry 并回显 identity；'
        '首字节{、末字节}，无其他文字、Markdown 或围栏。')
    n = len(prompt.encode('utf-8'))
    assert n <= 800, ('prompt 超 800 字节', n)
    return prompt


def main():
    plan_path, kids_path = sys.argv[1], sys.argv[2]
    plan = json.load(open(plan_path))
    parent, ws = _orch.parent_agent_id(), _orch.workspace_id()

    kids = json.load(open(kids_path)) if pathlib.Path(kids_path).is_file() else []
    by_key = {(k['task_id'], k['dispatch_id']): k for k in kids}

    made = 0
    for task, v in sorted(plan.items()):
        for l in v['lanes']:
            did = l['dispatch_id']
            key = (task, did)
            prev = by_key.get(key)
            if prev and prev.get('status') == 'dispatched':
                print(f'{task} {did} 已派发，跳过 {prev["agent_id"]}')
                continue
            if prev and prev.get('status') == 'dispatching':
                raise SystemExit(
                    f'{task} {did} 上次派发中途中断，可能已存在 agent。\n'
                    f'先 `paseo agent ls` 按 dispatch_id={did} 标签核对，确认后手工补 agent_id '
                    '或归档残留 agent，不要盲目重跑（会建出重复 agent）。')

            ci, ip = l['candidate_identity'], l['input_path']
            assert len(ci) == 64, ('candidate_identity 非 64 位', did, ci)
            assert ip and pathlib.Path(ip).is_file(), ('input_path 不存在', did, ip)

            rec = {'task_id': task, 'dispatch_id': did, 'candidate_identity': ci,
                   'input_path': ip, 'agent_id': None, 'status': 'dispatching'}
            by_key[key] = rec
            kids.append(rec)
            _orch.write_json_atomic(kids_path, kids)      # 意图先落盘

            o = _orch.paseo_json([
                'run', '--background', '--provider', 'claude/claude-opus-5',
                '--thinking', 'medium', '--mode', 'bypassPermissions',
                '--workspace', ws, '--cwd', str(_orch.ROOT),
                '--label', f'task_id={task}', '--label', 'role=reviewer',
                '--label', f'purpose={CONTRACT}', '--label', f'candidate_identity={ci}',
                '--label', f'dispatch_id={did}',
                '--label', f'paseo.parent-agent-id={parent}',
                '--json', build_prompt(ci, ip)])
            aid = o.get('agentId') or o.get('Id') or o.get('id') or o.get('agent_id')
            if not aid:
                raise SystemExit(f'{task} {did} 派发未返回 agent id：{json.dumps(o)[:200]}')

            rec['agent_id'] = aid
            rec['status'] = 'dispatched'
            _orch.write_json_atomic(kids_path, kids)      # 结果立刻落盘
            made += 1
            print(f'{task} {did} {aid}')

    print(f'本次新派发 {made} 个，children.json 共 {len(kids)} 条')


main()
