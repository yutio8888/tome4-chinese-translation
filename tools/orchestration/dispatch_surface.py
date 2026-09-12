#!/usr/bin/env python3
"""Prepare every frozen lane, then record first live binding (see README)."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import review_lifecycle as lifecycle

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



if __name__ == '__main__':
    lifecycle.dispatch_main('surface', build_prompt, 'codex/gpt-6-astra', 'auto')
