#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派发 contextual REVIEWER，使用契约第六节的官方三行 prompt 模板。

契约文件名是 paseo-translation-context-review-v2-contract.md
（不是 paseo-translation-contextual-v2-contract.md——后者不存在）。

用法：python3 -B tools/orchestration/dispatch_contextual.py <ctx.json> <children.json>

崩溃安全与幂等：与 dispatch_surface.py 同一套（runbook §35.1）——
派发前先落 status=dispatching 的意图，派发后立刻落 agent_id；
重跑跳过已 dispatched 的，遇到 dispatching 残留则停下要求人工核对。
身份一律运行时发现，不硬编码。
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _orch

DOC = 'docs/paseo-translation-context-review-v2-contract.md'
assert (_orch.ROOT / DOC).is_file(), f'契约文档不存在：{DOC}'


def build_prompt(ci, ip):
    prompt = (
        '任务：审核 input_path 中全部冻结 revision；按其术语、上下文及所引固定源码，'
        '仅报有证据的实质语义、机制、术语、关系或跨条一致性问题；否则判 OK。\n'
        f'输入：candidate_identity={ci}；input_path={ip}。全程只读；仅读该文件、'
        f'其明确引用内容及 {DOC} 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n'
        '输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 revision 并回显 identity；'
        '首字节{、末字节}，无其他文字、Markdown 或围栏。')
    n = len(prompt.encode('utf-8'))
    assert n <= 800, f'prompt {n} 字节超 800'
    return prompt, n


def main():
    rows = json.load(open(sys.argv[1]))
    kids_path = sys.argv[2]
    parent, ws = _orch.parent_agent_id(), _orch.workspace_id()

    kids = json.load(open(kids_path)) if pathlib.Path(kids_path).is_file() else []
    by_key = {(k['task_id'], k['dispatch_id']): k for k in kids}

    made = 0
    for r in rows:
        task, did = r['task_id'], r['dispatch_id']
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

        ci, ip = r['candidate_identity'], r['input_path']
        assert len(ci) == 64, ('candidate_identity 非 64 位', ci)
        assert ip and pathlib.Path(ip).is_file(), ('input_path 不存在', ip)
        prompt, n = build_prompt(ci, ip)

        rec = {'task_id': task, 'dispatch_id': did, 'candidate_identity': ci,
               'input_path': ip, 'agent_id': None, 'status': 'dispatching'}
        by_key[key] = rec
        kids.append(rec)
        _orch.write_json_atomic(kids_path, kids)      # 意图先落盘

        o = _orch.paseo_json([
            'run', '--background', '--provider', 'codex/gpt-5.6-sol',
            '--thinking', 'medium', '--mode', 'full-access',
            '--workspace', ws, '--cwd', str(_orch.ROOT),
            '--label', f'task_id={task}', '--label', 'role=reviewer',
            '--label', 'purpose=translation_contextual_v2',
            '--label', f'candidate_identity={ci}',
            '--label', f'dispatch_id={did}',
            '--label', f'paseo.parent-agent-id={parent}', '--json', prompt])
        aid = o.get('agentId') or o.get('Id') or o.get('id') or o.get('agent_id')
        if not aid:
            raise SystemExit(f'{task} {did} 派发未返回 agent id：{json.dumps(o)[:200]}')

        rec['agent_id'] = aid
        rec['status'] = 'dispatched'
        _orch.write_json_atomic(kids_path, kids)      # 结果立刻落盘
        made += 1
        print(task, did, aid, f'({n} bytes)')

    print(f'本次新派发 {made} 个，children.json 共 {len(kids)} 条')


main()
