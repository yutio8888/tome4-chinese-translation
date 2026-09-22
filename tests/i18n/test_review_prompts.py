from pathlib import Path
import ast
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
ORCHESTRATION = ROOT / "tools/orchestration"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ORCHESTRATION))

import contextual_lane_manifest
import dispatch_contextual
import dispatch_surface
import review_prompts
import surface_screen_result_check


def contract_prompt(relative: str, marker: str) -> str:
    text = (ROOT / relative).read_text(encoding="utf-8")
    tail = text.split(marker, 1)[1]
    match = re.search(r"```text\n(.*?)\n```", tail, re.S)
    if match is None:
        raise AssertionError(f"missing formal prompt after {marker!r}")
    return match.group(1)


class ReviewPromptTests(unittest.TestCase):
    CI = "a" * 64

    def test_formal_templates_are_exactly_the_contract_templates(self):
        self.assertEqual(
            review_prompts.CONTEXTUAL_PROMPT_TEMPLATE,
            contract_prompt(
                "docs/paseo-translation-context-review-v2-contract.md",
                "固定三行 prompt：",
            ),
        )
        self.assertEqual(
            review_prompts.SURFACE_PROMPT_TEMPLATE,
            contract_prompt(
                "docs/paseo-translation-surface-screen-v1-contract.md",
                "固定三行 dispatch prompt",
            ),
        )

    def test_dispatch_entrypoints_use_the_shared_builders(self):
        self.assertIs(dispatch_contextual.build_prompt, review_prompts.build_contextual_prompt)
        self.assertIs(dispatch_surface.build_prompt, review_prompts.build_surface_prompt)

        source = (ORCHESTRATION / "dispatch_reviewers.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "review_prompts"
            for alias in node.names
        }
        calls = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertIn("build_surface_prompt", imports)
        self.assertIn("build_surface_prompt", calls)
        self.assertNotIn("candidate_identity=<candidate_identity>", source)

    def test_three_lines_and_longest_legal_actual_paths_fit(self):
        task = "t" * 128
        dispatch = "d" * 32
        cases = (
            (
                review_prompts.build_contextual_prompt,
                f".ai/task/{task}/CONTEXTUAL-ENVELOPE-{dispatch}.json",
            ),
            (
                review_prompts.build_surface_prompt,
                f".ai/task/{task}/SURFACE-SCREEN-ENVELOPE-{dispatch}.json",
            ),
        )
        for builder, path in cases:
            with self.subTest(builder=builder.__name__):
                prompt = builder(self.CI, path)
                self.assertEqual(len(prompt.splitlines()), 3)
                self.assertLessEqual(len(prompt.encode("utf-8")), review_prompts.MAX_PROMPT_BYTES)
                self.assertIn(path, prompt)

        real_consumers = (
            (contextual_lane_manifest.render_dispatch_prompt, cases[0][1]),
            (surface_screen_result_check.render_dispatch_prompt, cases[1][1]),
        )
        for renderer, path in real_consumers:
            with self.subTest(renderer=renderer.__module__):
                prompt = renderer(self.CI, path)
                self.assertEqual(len(prompt.splitlines()), 3)
                self.assertLessEqual(len(prompt.encode("utf-8")), review_prompts.MAX_PROMPT_BYTES)

    def test_over_limit_and_invalid_identity_fail_closed(self):
        with self.assertRaises(review_prompts.PromptError):
            review_prompts.build_surface_prompt(self.CI, "x" * 801)
        with self.assertRaises(review_prompts.PromptError):
            review_prompts.build_contextual_prompt("not-a-hash", "input.json")

        with self.assertRaises(contextual_lane_manifest.result_check.ContractError):
            contextual_lane_manifest.render_dispatch_prompt(self.CI, "x" * 801)
        with self.assertRaises(surface_screen_result_check.ContractError):
            surface_screen_result_check.render_dispatch_prompt(self.CI, "x" * 801)

    def test_exact_utf8_byte_boundary(self):
        builders = (
            review_prompts.build_contextual_prompt,
            review_prompts.build_surface_prompt,
        )
        for builder in builders:
            one_byte_path_size = len(builder(self.CI, "x").encode("utf-8"))
            path_size = review_prompts.MAX_PROMPT_BYTES - one_byte_path_size + 1
            with self.subTest(builder=builder.__name__):
                prompt = builder(self.CI, "x" * path_size)
                self.assertEqual(len(prompt.encode("utf-8")), review_prompts.MAX_PROMPT_BYTES)
                with self.assertRaises(review_prompts.PromptError):
                    builder(self.CI, "x" * (path_size + 1))

    def test_every_splitlines_separator_is_rejected_by_all_public_renderers(self):
        separators = ("\n", "\r", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")
        renderers = (
            (review_prompts.build_contextual_prompt, review_prompts.PromptError),
            (review_prompts.build_surface_prompt, review_prompts.PromptError),
            (contextual_lane_manifest.render_dispatch_prompt, contextual_lane_manifest.result_check.ContractError),
            (surface_screen_result_check.render_dispatch_prompt, surface_screen_result_check.ContractError),
        )
        for separator in separators:
            self.assertGreater(len(f"before{separator}after".splitlines()), 1)
            for renderer, error in renderers:
                with self.subTest(separator=ascii(separator), renderer=renderer.__module__):
                    with self.assertRaises(error):
                        renderer(self.CI, f"before{separator}after")

    def test_real_consumers_share_templates_without_changing_replay_bindings(self):
        contextual_path = ".ai/task/legacy-task/CONTEXTUAL-ENVELOPE-legacy-dispatch.json"
        surface_path = ".ai/task/legacy-task/SURFACE-SCREEN-ENVELOPE-legacy-dispatch.json"
        self.assertIs(contextual_lane_manifest.PROMPT_TEMPLATE, review_prompts.CONTEXTUAL_PROMPT_TEMPLATE)
        self.assertIs(surface_screen_result_check.PROMPT_TEMPLATE, review_prompts.SURFACE_PROMPT_TEMPLATE)
        self.assertEqual(
            contextual_lane_manifest.render_dispatch_prompt(self.CI, contextual_path),
            review_prompts.build_contextual_prompt(self.CI, contextual_path),
        )
        self.assertEqual(
            surface_screen_result_check.render_dispatch_prompt(self.CI, surface_path),
            review_prompts.build_surface_prompt(self.CI, surface_path),
        )

    def test_role_and_prompts_preserve_the_source_permission_difference(self):
        role = (ROOT / ".ai/roles/reviewer.md").read_text(encoding="utf-8")
        contextual = (ROOT / "docs/paseo-translation-context-review-v2-contract.md").read_text(encoding="utf-8")
        surface = (ROOT / "docs/paseo-translation-surface-screen-v1-contract.md").read_text(encoding="utf-8")
        self.assertIn("文件、行号和 hash 只证明来源，不扩大读取权限", role)
        self.assertIn("surface 不得据此补查源码", role)
        self.assertIn("仅可沿调用链补查冻结版本", role)
        self.assertIn("唯一可用的译文输入", contextual)
        self.assertIn("source_facts_v1.fact.terminology", contextual)
        self.assertIn("常是摘要", contextual)
        self.assertIn("不追溯改写已冻结的 prompt、candidate/hash", contextual)
        self.assertIn("唯一可用的译文", surface)
        self.assertIn("只是摘要或 hash", surface)
        self.assertIn("不自动构成译文缺陷", surface)
        self.assertIn("surface 不得借引用、provenance 或完整契约增加源码调查", surface)
        self.assertIn("不追溯改写已冻结的 prompt、candidate/hash", surface)
        self.assertIn("完整 docs/paseo-translation-context-review-v2-contract.md", review_prompts.CONTEXTUAL_PROMPT_TEMPLATE)
        self.assertIn("可沿调用链查冻结版相关源码", review_prompts.CONTEXTUAL_PROMPT_TEMPLATE)
        self.assertIn("完整 docs/paseo-translation-surface-screen-v1-contract.md", review_prompts.SURFACE_PROMPT_TEMPLATE)
        self.assertIn("禁补查源码", review_prompts.SURFACE_PROMPT_TEMPLATE)


if __name__ == "__main__":
    unittest.main()
