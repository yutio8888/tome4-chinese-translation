#!/usr/bin/env python3
"""Canonical three-line prompts for managed translation reviews."""

from __future__ import annotations

import re


MAX_PROMPT_BYTES = 800
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_LINE_SEPARATORS = frozenset("\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029")

CONTEXTUAL_PROMPT_TEMPLATE = (
    "任务：审冻结 revision；仅报有据的语义/机制/术语/关系/跨条问题，否则 OK。\n"
    "输入：candidate_identity=<candidate_identity>；input_path=<input_path>。只读；可读输入、精确引用及完整 docs/paseo-translation-context-review-v2-contract.md；可沿调用链查冻结版相关源码，仅限输入指定位置；禁从 / 或无关目录全盘搜索，禁读其他 .ai/task/、.ai/reviews/、旧 finding、当前译文/术语库。\n"
    "输出：仅回第六节紧凑 JSON，按序全覆盖、回显 identity；首{末}，无文字/围栏。"
)

SURFACE_PROMPT_TEMPLATE = (
    "任务：筛查冻结 entry；仅报有据的明显错译、标记/占位符、参数顺序或格式问题，否则 OK。\n"
    "输入：candidate_identity=<candidate_identity>；input_path=<input_path>。只读禁写；仅读该输入、精确引用、完整 docs/paseo-translation-surface-screen-v1-contract.md；禁补查源码；禁读其他 .ai/task/、.ai/reviews/、先前 finding、当前译文/术语库。\n"
    "输出：仅回第六节紧凑 JSON，按序全覆盖、回显 identity；证据不足仅写 observation；首{末}，无其他文字/Markdown/围栏。"
)


class PromptError(ValueError):
    """The formal prompt cannot be rendered within its frozen boundary."""


def _render(template: str, candidate_identity: str, input_path: str) -> str:
    if not isinstance(candidate_identity, str) or not _SHA256.fullmatch(candidate_identity):
        raise PromptError("prompt candidate identity is invalid")
    if not isinstance(input_path, str) or not input_path:
        raise PromptError("prompt input_path is invalid")
    if any(character in _LINE_SEPARATORS for character in input_path):
        raise PromptError("prompt input_path contains a line separator")
    prompt = template.replace(
        "<candidate_identity>", candidate_identity
    ).replace("<input_path>", input_path)
    try:
        template_size = len(template.encode("utf-8"))
        prompt_size = len(prompt.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise PromptError("prompt is not valid UTF-8 text") from error
    if template_size > MAX_PROMPT_BYTES or prompt_size > MAX_PROMPT_BYTES:
        raise PromptError(
            f"prompt template or instance exceeds {MAX_PROMPT_BYTES} UTF-8 bytes"
        )
    return prompt


def build_contextual_prompt(candidate_identity: str, input_path: str) -> str:
    return _render(CONTEXTUAL_PROMPT_TEMPLATE, candidate_identity, input_path)


def build_surface_prompt(candidate_identity: str, input_path: str) -> str:
    return _render(SURFACE_PROMPT_TEMPLATE, candidate_identity, input_path)
