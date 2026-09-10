#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派发 contextual REVIEWER，使用契约第六节的官方三行 prompt 模板。

契约文件名是 paseo-translation-context-review-v2-contract.md
（不是 paseo-translation-contextual-v2-contract.md——后者不存在）。

用法：
  CLI 直派（默认）：python3 -B .../dispatch_contextual.py <ctx.json> <children.json>
  MCP 两段式：      python3 -B .../dispatch_contextual.py <ctx.json> <children.json> --emit <emit.json>
                    python3 -B .../dispatch_contextual.py <ctx.json> <children.json> --record <ids.json>
两段式的理由与语义同 dispatch_surface.py：CLI 不暴露 provider 功能开关，
提示词仍由本脚本唯一生成，崩溃安全的「意图先落盘」语义不变。

崩溃安全与幂等：与 dispatch_surface.py 同一套（runbook §35.1）——
派发前先落 status=dispatching 的意图，派发后立刻落 agent_id；
重跑跳过已 dispatched 的，遇到 dispatching 残留则停下要求人工核对。
身份一律运行时发现，不硬编码。
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _orch

DOC = 'docs/paseo-translation-context-review-v2-contract.md'

# 派发模式。默认 full-access 是历史取值，但 codex 对该模式的说明含「访问网络」，
# 曾导致 reviewer 用 curl 拉上游 master 而非钉住的 1.7.6（契约第 94 行禁止读
# 该文件与契约第六节以外的内容）。auto 是 workspace-write、默认无网络，
# 代价是可能触发权限弹窗——等待器须同时探测 PendingPermissions，
# 否则 `paseo agent wait` 会静默阻塞到超时。
MODE = (sys.argv[sys.argv.index('--mode') + 1] if '--mode' in sys.argv else 'full-access')
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


def _arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None


def record(kids_path, ids_path):
    kids = json.load(open(kids_path))
    ids = json.load(open(ids_path))
    seen = {k['agent_id'] for k in kids if k.get('agent_id')}
    done = 0
    for k in kids:
        if k.get('status') != 'dispatching':
            continue
        key = f"{k['task_id']}|{k['dispatch_id']}"
        aid = ids.get(key)
        if not aid:
            raise SystemExit(f'ids.json 缺 {key} 的 agent_id')
        if aid in seen:
            raise SystemExit(f'{key} 的 agent_id {aid} 与其他记录重复，拒绝回填')
        seen.add(aid)
        k['agent_id'] = aid
        k['status'] = 'dispatched'
        done += 1
    _orch.write_json_atomic(kids_path, kids)
    leftover = [f"{k['task_id']}|{k['dispatch_id']}" for k in kids if k.get('status') != 'dispatched']
    if leftover:
        raise SystemExit(f'仍有未完成的记录：{leftover}')
    print(f'回填 {done} 条，children.json 共 {len(kids)} 条，全部 dispatched')


def main():
    rows = json.load(open(sys.argv[1]))
    kids_path = sys.argv[2]
    if '--record' in sys.argv:
        return record(kids_path, _arg('--record'))
    emit_path = _arg('--emit')
    emit = []
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

        labels = {'task_id': task, 'role': 'reviewer',
                  'purpose': 'translation_contextual_v2',
                  'candidate_identity': ci, 'dispatch_id': did,
                  'paseo.parent-agent-id': parent}
        if emit_path:
            emit.append({'task_id': task, 'dispatch_id': did, 'key': f'{task}|{did}',
                         'provider': 'codex/gpt-5.6-sol',
                         'workspaceId': ws, 'cwd': str(_orch.ROOT),
                         'thinkingOptionId': 'medium', 'modeId': MODE,
                         'labels': labels, 'prompt': prompt})
            made += 1
            print(f'{task} {did} 待 MCP 创建 ({n} bytes)')
            continue

        o = _orch.paseo_json([
            'run', '--background', '--provider', 'codex/gpt-5.6-sol',
            '--thinking', 'medium', '--mode', MODE,
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

    if emit_path:
        _orch.write_json_atomic(emit_path, emit)
        print(f'已写出 {len(emit)} 条待创建项到 {emit_path}；'
              f'创建完成后用 --record <ids.json> 回填')
        return
    print(f'本次新派发 {made} 个，children.json 共 {len(kids)} 条')


main()
