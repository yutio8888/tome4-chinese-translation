#!/usr/bin/env python3
"""Prepare every frozen lane, then record first live binding (see README)."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import review_lifecycle as lifecycle

DOC = 'docs/paseo-translation-context-review-v2-contract.md'


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
    return prompt



if __name__ == '__main__':
    lifecycle.dispatch_main('contextual', build_prompt, 'claude/claude-opus-5', 'bypassPermissions')
