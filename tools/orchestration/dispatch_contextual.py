#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""派发 contextual REVIEWER，使用契约第六节的官方三行 prompt 模板。

契约文件名是 paseo-translation-context-review-v2-contract.md
（不是 paseo-translation-contextual-v2-contract.md——后者不存在）。

用法：python3 -B tools/orchestration/dispatch_contextual.py <ctx.json> <children.json>
"""
import json, sys, subprocess, pathlib

PARENT = 'c62dba7e-1663-47e2-95d6-a7665ba7118c'
DOC = 'docs/paseo-translation-context-review-v2-contract.md'
assert pathlib.Path(DOC).is_file(), f'契约文档不存在：{DOC}'


def main():
    rows = json.load(open(sys.argv[1]))
    kids = []
    for r in rows:
        ci, ip = r['candidate_identity'], r['input_path']
        assert len(ci) == 64, ('candidate_identity 非 64 位', ci)
        assert ip, 'input_path 为空'
        prompt = (
            '任务：审核 input_path 中全部冻结 revision；按其术语、上下文及所引固定源码，'
            '仅报有证据的实质语义、机制、术语、关系或跨条一致性问题；否则判 OK。\n'
            f'输入：candidate_identity={ci}；input_path={ip}。全程只读；仅读该文件、'
            f'其明确引用内容及 {DOC} 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n'
            '输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 revision 并回显 identity；'
            '首字节{、末字节}，无其他文字、Markdown 或围栏。')
        n = len(prompt.encode('utf-8'))
        assert n <= 800, f'prompt {n} 字节超 800'
        o = json.loads(subprocess.run(
            ['paseo', 'run', '--background', '--provider', 'codex/gpt-5.6-sol',
             '--thinking', 'medium', '--mode', 'full-access',
             '--workspace', 'wks_420314270844170b',
             '--cwd', '/workspace/tome4-chinese-translation',
             '--label', f'task_id={r["task_id"]}', '--label', 'role=reviewer',
             '--label', 'purpose=translation_contextual_v2',
             '--label', f'candidate_identity={ci}',
             '--label', f'dispatch_id={r["dispatch_id"]}',
             '--label', f'paseo.parent-agent-id={PARENT}', '--json', prompt],
            capture_output=True, text=True).stdout)
        aid = o.get('agentId')
        assert aid, o
        kids.append({'task_id': r['task_id'], 'dispatch_id': r['dispatch_id'], 'agent_id': aid})
        print(r['task_id'], r['dispatch_id'], aid, f'({n} bytes)')
    json.dump(kids, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)


main()
