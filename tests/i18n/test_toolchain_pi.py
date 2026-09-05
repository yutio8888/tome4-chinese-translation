"""Toolchain tests: pi."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT, TOOLS, create_workset_fixture
from tests.i18n import test_toolchain_quality_validation as quality_validation_tests
import contextlib
from dataclasses import replace
import hashlib
import io
import sys
import json
import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch
from i18nlib import TOOL_VERSION
from i18nlib.config import load_manifest
from i18nlib.errors import AgentError, ValidationError
from i18nlib.pi_agent import _copy_isolated_oauth_credential, run_pi_translation
from i18nlib.pi_file_review import (
    _git_worktree_snapshot,
    _parser as pi_file_review_parser,
    _validate_file_review_cache_options,
    build_file_review_command,
    main as pi_file_review_main,
    run_pi_file_review,
)
from i18nlib.pi_remediate import _validate_remediation, run_pi_remediation
from i18nlib.pi_review import run_pi_review
from i18nlib.pi_quality import (
    QUALITY_EVALUATOR_CACHE_CONTRACT,
    _decode_quality_model_output,
    _load_cached_assessment,
    build_quality_evaluator_bundle,
    build_quality_evaluator_command,
    run_pi_quality_evaluator,
)
from i18nlib.pi_tmux import (
    _read_status,
    execute_in_pane,
    main as pi_tmux_main,
    run_tmux_file_review,
    run_tmux_remediation,
    run_tmux_review,
    run_tmux_translation,
    run_worker_job,
    split_pane,
    worker_main,
)
from i18nlib.review import REVIEW_CONTRACT, REVIEW_SCHEMA_VERSION, _bundle_id


FAKE_TMUX_SCRIPT = """#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

log = Path(os.environ["FAKE_TMUX_LOG"])
state = Path(os.environ["FAKE_TMUX_STATE"])
with log.open("a") as handle:
    handle.write(json.dumps(sys.argv[1:]) + "\\n")
command = sys.argv[1]
if command == "has-session":
    sys.exit(0)
if command == "display-message":
    fmt = sys.argv[-1]
    if "{pane_dead}" in fmt:
        job_dir = state.read_text().strip() if state.exists() else ""
        dead = "1" if job_dir and (Path(job_dir) / "worker-status.json").exists() else "0"
        print(dead)
    elif "{session_name}" in fmt:
        print("fake-session")
    sys.exit(0)
if command == "split-window":
    shell_command = sys.argv[-1]
    match = re.search(r"worker --job (\\S+)", shell_command)
    job_dir = match.group(1) if match else ""
    state.write_text(job_dir)
    subprocess.Popen(
        ["sh", "-c", shell_command],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("%99")
    sys.exit(0)
if command in ("rename-pane", "kill-pane"):
    sys.exit(0)
sys.exit(0)
"""

FAKE_PI_REVIEW_SCRIPT = """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(
    json.dumps(sys.argv[1:]), encoding="utf-8"
)
count_path_value = os.environ.get("FAKE_PI_CALL_COUNT")
if count_path_value:
    count_path = Path(count_path_value)
    count = int(count_path.read_text(encoding="utf-8")) if count_path.exists() else 0
    count_path.write_text(str(count + 1), encoding="utf-8")
bundle_path = next(Path(value[1:]) for value in sys.argv[1:] if value.startswith("@"))
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "review_contract": bundle["review_contract"],
    "bundle_id": bundle["bundle_id"],
    "findings": [],
}, ensure_ascii=False))
"""


class PiRemediationValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    @staticmethod
    def _review(item_id: str) -> dict[str, object]:
        return {
            "review_id": "review-fixture",
            "findings": [
                {
                    "finding_id": "finding-fixture",
                    "item_id": item_id,
                    "severity": "minor",
                    "category": "translation",
                    "title": "fixture",
                    "body": "fixture finding",
                }
            ],
        }

    def _translation_case(
        self,
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        item = {
            "item_id": "translation-fixture",
            "component": "boot",
            "section": "fixture/dialog.lua",
            "source": "%s has %d",
            "target": "%d 属于 %s",
            "source_tag": "tformat",
            "args_order": [2, 1],
            "special": {"nested": {"value": 1}},
        }
        bundle: dict[str, object] = {
            "kind": "translations",
            "bundle_id": "bundle-translation-fixture",
            "component": "boot",
            "items": [item],
        }
        review = self._review(item["item_id"])
        output: dict[str, object] = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "remediation_contract": "tome4-review-remediation-v1",
            "bundle_id": bundle["bundle_id"],
            "review_id": review["review_id"],
            "proposals": [
                {
                    "finding_id": "finding-fixture",
                    "item_id": item["item_id"],
                    "action": "replace-translation",
                    "source": item["source"],
                    "source_tag": item["source_tag"],
                    "original_target": item["target"],
                    "target": "%d 拥有 %s",
                    "args_order": [2, 1],
                    "special": {"nested": {"value": True}},
                    "rationale": "fixture replacement",
                }
            ],
        }
        return bundle, review, output

    def _code_case(
        self,
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        item = {
            "item_id": "code-fixture",
            "path": "tools/example.py",
            "diff": "@@ -1 +1 @@\n-old\n+new\n",
        }
        bundle: dict[str, object] = {
            "kind": "code",
            "bundle_id": "bundle-code-fixture",
            "files": [item],
        }
        review = self._review(item["item_id"])
        output: dict[str, object] = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "remediation_contract": "tome4-review-remediation-v1",
            "bundle_id": bundle["bundle_id"],
            "review_id": review["review_id"],
            "proposals": [
                {
                    "finding_id": "finding-fixture",
                    "item_id": item["item_id"],
                    "action": "patch-code",
                    "path": item["path"],
                    "patch": "Replace old with new.",
                    "rationale": "fixture patch",
                }
            ],
        }
        return bundle, review, output

    def _validate(
        self,
        bundle: dict[str, object],
        review: dict[str, object],
        output: dict[str, object],
        *,
        strict: bool,
    ) -> dict[str, object]:
        return _validate_remediation(
            bundle,
            review,
            output,
            manifest=self.manifest,
            strict=strict,
        )

    def test_valid_translation_code_and_no_change_proposals(self) -> None:
        translation = self._translation_case()
        translation_summary = self._validate(*translation, strict=True)
        self.assertEqual(translation_summary["replace_translation"], 1)
        self.assertEqual(translation_summary["lint_warnings"], 0)

        code = self._code_case()
        code_summary = self._validate(*code, strict=True)
        self.assertEqual(code_summary["patch_code"], 1)

        for bundle, review, output in (self._translation_case(), self._code_case()):
            item_id = review["findings"][0]["item_id"]
            output["proposals"] = [
                {
                    "finding_id": "finding-fixture",
                    "item_id": item_id,
                    "action": "no-change",
                    "rationale": "the finding is not actionable",
                }
            ]
            with self.subTest(kind=bundle["kind"]):
                summary = self._validate(bundle, review, output, strict=True)
                self.assertEqual(summary["no_change"], 1)

    def test_actions_must_match_bundle_kind(self) -> None:
        translation_bundle, translation_review, translation_output = (
            self._translation_case()
        )
        translation_output["proposals"] = [
            {
                "finding_id": "finding-fixture",
                "item_id": "translation-fixture",
                "action": "patch-code",
                "path": "tools/example.py",
                "patch": "fixture patch",
                "rationale": "wrong action",
            }
        ]
        code_bundle, code_review, code_output = self._code_case()
        code_output["proposals"] = [
            {
                "finding_id": "finding-fixture",
                "item_id": "code-fixture",
                "action": "replace-translation",
                "source": "source",
                "source_tag": None,
                "original_target": "target",
                "target": "replacement",
                "args_order": None,
                "special": None,
                "rationale": "wrong action",
            }
        ]
        for bundle, review, output in (
            (translation_bundle, translation_review, translation_output),
            (code_bundle, code_review, code_output),
        ):
            with self.subTest(kind=bundle["kind"]), self.assertRaisesRegex(
                ValidationError, "incompatible"
            ):
                self._validate(bundle, review, output, strict=False)

    def test_unknown_fields_are_strict_only(self) -> None:
        for location in ("root", "proposal"):
            bundle, review, output = self._translation_case()
            if location == "root":
                output["future_root"] = {"metadata": True}
            else:
                output["proposals"][0]["future_proposal"] = "metadata"
            with self.subTest(location=location, strict=True), self.assertRaises(
                ValidationError
            ):
                self._validate(bundle, review, output, strict=True)
            with self.subTest(location=location, strict=False):
                self.assertTrue(
                    self._validate(bundle, review, output, strict=False)["ok"]
                )

    def test_no_change_rejects_action_fields_only_in_strict_mode(self) -> None:
        bundle, review, output = self._translation_case()
        output["proposals"] = [
            {
                "finding_id": "finding-fixture",
                "item_id": "translation-fixture",
                "action": "no-change",
                "rationale": "no safe change",
                "target": "must be ignored only in compatibility mode",
            }
        ]
        with self.assertRaisesRegex(ValidationError, "not allowed"):
            self._validate(bundle, review, output, strict=True)
        self.assertTrue(self._validate(bundle, review, output, strict=False)["ok"])

    def test_action_specific_fields_are_required(self) -> None:
        for case_factory, missing_field in (
            (self._translation_case, "target"),
            (self._code_case, "patch"),
        ):
            bundle, review, output = case_factory()
            del output["proposals"][0][missing_field]
            with self.subTest(field=missing_field), self.assertRaisesRegex(
                ValidationError, "missing"
            ):
                self._validate(bundle, review, output, strict=False)

    def test_translation_identity_fields_are_preserved_type_sensitively(self) -> None:
        for field, value in (
            ("source", False),
            ("source_tag", 1),
            ("original_target", True),
        ):
            bundle, review, output = self._translation_case()
            output["proposals"][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(
                ValidationError, f"does not preserve {field}"
            ):
                self._validate(bundle, review, output, strict=False)

    def test_translation_lint_rejects_invalid_order_in_all_modes(self) -> None:
        for strict in (False, True):
            bundle, review, output = self._translation_case()
            output["proposals"][0]["args_order"] = [1, 1]
            output["proposals"][0]["target"] = "%s %s"
            with self.subTest(strict=strict), self.assertRaisesRegex(
                ValidationError, "failed translation lint"
            ):
                self._validate(bundle, review, output, strict=strict)

    def test_translation_args_order_rejects_boolean_indices(self) -> None:
        bundle, review, output = self._translation_case()
        output["proposals"][0]["args_order"] = [True, 1]
        with self.assertRaisesRegex(ValidationError, "invalid args_order"):
            self._validate(bundle, review, output, strict=False)

    def test_translation_lint_warnings_depend_on_strict_mode(self) -> None:
        bundle, review, output = self._translation_case()
        item = bundle["items"][0]
        item["source"] = "#RED#%02d @foo@"
        proposal = output["proposals"][0]
        proposal["source"] = item["source"]
        proposal["target"] = "%d"
        proposal["args_order"] = [1]
        with self.assertRaisesRegex(ValidationError, "strict lint warnings"):
            self._validate(bundle, review, output, strict=True)
        summary = self._validate(bundle, review, output, strict=False)
        self.assertGreaterEqual(summary["lint_warnings"], 3)
        self.assertEqual(summary["warnings"], summary["lint_warnings"])

    def test_special_rejects_non_finite_values(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf"), object()):
            bundle, review, output = self._translation_case()
            output["proposals"][0]["special"] = {"value": value}
            with self.subTest(value=value), self.assertRaisesRegex(
                ValidationError, "finite renderable"
            ):
                self._validate(bundle, review, output, strict=False)

    def test_schema_version_rejects_boolean(self) -> None:
        bundle, review, output = self._translation_case()
        output["schema_version"] = True
        with self.assertRaisesRegex(ValidationError, "unsupported schema"):
            self._validate(bundle, review, output, strict=False)

    def test_proposals_must_cover_each_finding_exactly_once(self) -> None:
        bundle, review, output = self._translation_case()
        output["proposals"] = []
        with self.assertRaisesRegex(ValidationError, "omitted findings"):
            self._validate(bundle, review, output, strict=False)

        bundle, review, output = self._translation_case()
        duplicate = dict(output["proposals"][0])
        output["proposals"].append(duplicate)
        with self.assertRaisesRegex(ValidationError, "duplicate finding_id"):
            self._validate(bundle, review, output, strict=False)

    def test_code_patch_requires_exact_safe_path_and_nonempty_text(self) -> None:
        for field, value, message in (
            ("path", "../tools/example.py", "unsafe path"),
            ("path", "C:\\tools\\example.py", "unsafe path"),
            ("path", "tools/other.py", "does not match"),
            ("patch", "   ", "invalid code patch"),
            ("rationale", "", "no rationale"),
        ):
            bundle, review, output = self._code_case()
            output["proposals"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(
                ValidationError, message
            ):
                self._validate(bundle, review, output, strict=False)

    def test_run_options_fail_before_artifact_creation(self) -> None:
        base = {
            "bundle_path": Path("unused-bundle.json"),
            "review_path": Path("unused-review.json"),
            "provider": "fixture",
            "model": "fixture-model",
            "thinking": "high",
            "timeout": 30,
            "strict": True,
            "pi_executable": "unused-pi",
        }
        cases = (
            ("provider", ""),
            ("provider", 1),
            ("model", ""),
            ("model", None),
            ("thinking", ""),
            ("thinking", False),
            ("timeout", True),
            ("timeout", 0),
            ("timeout", -1),
            ("strict", 1),
        )
        runners = (
            (run_pi_remediation, "i18nlib.pi_remediate.create_run_directory"),
            (run_tmux_remediation, "i18nlib.pi_tmux.create_run_directory"),
        )
        for runner, create_target in runners:
            for field, value in cases:
                arguments = {**base, field: value}
                with self.subTest(runner=runner.__name__, field=field), patch(
                    create_target
                ) as create_run:
                    with self.assertRaises(ValidationError):
                        runner(**arguments)
                    create_run.assert_not_called()


class PiRunOptionPreflightTests(unittest.TestCase):
    COMMON_INVALID_OPTIONS = (
        ("provider", 1),
        ("provider", " \t"),
        ("model", None),
        ("model", "\n"),
        ("thinking", False),
        ("thinking", ""),
        ("timeout", True),
        ("timeout", 1.5),
        ("timeout", "30"),
        ("strict", 1),
        ("strict", 0.0),
    )
    CACHE_INVALID_OPTIONS = (
        ("use_cache", 1),
        ("use_cache", 0.0),
        ("force", 1),
        ("force", 0.0),
    )
    TMUX_INVALID_OPTIONS = (
        ("layout", "diagonal"),
        ("layout", None),
        ("percent", 0),
        ("percent", -1),
        ("percent", 100),
        ("percent", True),
        ("percent", 35.0),
        ("keep_pane", 1),
        ("keep_pane", None),
        ("fallback", "silent"),
        ("fallback", False),
        ("session", ""),
        ("session", " \t\n"),
        ("session", 1),
    )

    def test_invalid_core_options_precede_all_runner_side_effects(self) -> None:
        common = {
            "provider": "fixture",
            "model": "fixture-model",
            "thinking": "high",
            "timeout": 30,
            "strict": True,
            "pi_executable": "unused-pi",
        }
        runners = (
            (
                run_pi_translation,
                {**common, "workset_path": Path("unused-workset.json")},
                "i18nlib.pi_agent",
                "read_json_object",
                "subprocess.run",
                (),
            ),
            (
                run_pi_review,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "use_cache": True,
                    "force": False,
                },
                "i18nlib.pi_review",
                "validate_review_bundle",
                "subprocess.run",
                self.CACHE_INVALID_OPTIONS,
            ),
            (
                run_pi_file_review,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "use_cache": False,
                    "force": False,
                },
                "i18nlib.pi_file_review",
                "validate_review_bundle",
                "_run_file_review_process",
                self.CACHE_INVALID_OPTIONS,
            ),
            (
                run_pi_quality_evaluator,
                {
                    **common,
                    "sample_path": Path("unused-sample.json"),
                    "evaluator_id": "reviewer-a",
                    "use_cache": True,
                    "force": False,
                },
                "i18nlib.pi_quality",
                "_read_json",
                "_run_file_review_process",
                (
                    *self.CACHE_INVALID_OPTIONS,
                    ("evaluator_id", 1),
                    ("evaluator_id", " \n"),
                ),
            ),
            (
                run_tmux_review,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "use_cache": True,
                    "force": False,
                },
                "i18nlib.pi_tmux",
                "validate_review_bundle",
                "execute_in_pane",
                self.CACHE_INVALID_OPTIONS,
            ),
            (
                run_tmux_file_review,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "use_cache": False,
                    "force": False,
                },
                "i18nlib.pi_tmux",
                "validate_review_bundle",
                "execute_in_pane",
                self.CACHE_INVALID_OPTIONS,
            ),
            (
                run_tmux_translation,
                {**common, "workset_path": Path("unused-workset.json")},
                "i18nlib.pi_tmux",
                "read_json_object",
                "execute_in_pane",
                (),
            ),
            (
                run_tmux_remediation,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "review_path": Path("unused-review.json"),
                },
                "i18nlib.pi_tmux",
                "validate_review_bundle",
                "execute_in_pane",
                (),
            ),
        )
        for runner, base, module, input_name, execution_name, extra_cases in runners:
            for field, value in (*self.COMMON_INVALID_OPTIONS, *extra_cases):
                arguments = {**base, field: value}
                targets = (
                    f"{module}.load_manifest",
                    f"{module}.{input_name}",
                    f"{module}.create_run_directory",
                    f"{module}._pi_environment",
                    f"{module}.{execution_name}",
                )
                with self.subTest(
                    runner=runner.__name__, field=field, value=value
                ), contextlib.ExitStack() as stack:
                    mocked_side_effects = [
                        stack.enter_context(patch(target)) for target in targets
                    ]
                    with self.assertRaises(ValidationError):
                        runner(**arguments)
                    for side_effect in mocked_side_effects:
                        side_effect.assert_not_called()

    def test_invalid_tmux_options_precede_all_runner_side_effects(self) -> None:
        common = {
            "provider": "fixture",
            "model": "fixture-model",
            "thinking": "high",
            "timeout": 30,
            "strict": True,
            "pi_executable": "unused-pi",
            "tmux_executable": "unused-tmux",
            "session": None,
            "layout": "vertical",
            "percent": 35,
            "keep_pane": True,
            "fallback": "error",
        }
        runners = (
            (
                run_tmux_review,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "use_cache": False,
                    "force": False,
                },
            ),
            (
                run_tmux_file_review,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "use_cache": False,
                    "force": False,
                },
            ),
            (
                run_tmux_remediation,
                {
                    **common,
                    "bundle_path": Path("unused-bundle.json"),
                    "review_path": Path("unused-review.json"),
                },
            ),
            (
                run_tmux_translation,
                {**common, "workset_path": Path("unused-workset.json")},
            ),
        )
        targets = (
            "i18nlib.pi_tmux.load_manifest",
            "i18nlib.pi_tmux.validate_review_bundle",
            "i18nlib.pi_tmux.read_json_object",
            "i18nlib.pi_tmux._read_review",
            "i18nlib.pi_tmux.create_run_directory",
            "i18nlib.pi_tmux.write_json",
            "i18nlib.pi_tmux._pi_environment",
            "i18nlib.pi_tmux._run_tmux",
            "i18nlib.pi_tmux.execute_in_pane",
        )
        for runner, base in runners:
            for field, value in self.TMUX_INVALID_OPTIONS:
                with self.subTest(
                    runner=runner.__name__, field=field, value=value
                ), contextlib.ExitStack() as stack:
                    side_effects = [
                        stack.enter_context(patch(target)) for target in targets
                    ]
                    with self.assertRaises(ValidationError):
                        runner(**{**base, field: value})
                    for side_effect in side_effects:
                        side_effect.assert_not_called()


class PiAgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    def test_isolated_oauth_copy_keeps_only_requested_provider(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-oauth-test-") as temporary:
            directory = Path(temporary)
            source = directory / "source-auth.json"
            target = directory / "isolated" / "auth.json"
            target.parent.mkdir()
            source.write_text(
                json.dumps(
                    {
                        "openai-codex": {
                            "type": "oauth",
                            "access": "fixture-access",
                            "refresh": "fixture-refresh",
                        },
                        "unrelated": {"type": "api_key", "key": "do-not-copy"},
                    }
                ),
                encoding="utf-8",
            )
            _copy_isolated_oauth_credential(source, target, "openai-codex")
            copied = json.loads(target.read_text(encoding="utf-8"))
            mode = target.stat().st_mode & 0o777
        self.assertEqual(set(copied), {"openai-codex"})
        self.assertEqual(mode, 0o600)

    def test_pi_runner_has_no_tools_and_validates_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-test-") as temporary:
            directory = Path(temporary)
            _, workset_path, _ = create_workset_fixture(self.manifest, directory)
            arguments_path = directory / "arguments.json"
            fake_pi = directory / "fake-pi"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(
    json.dumps(sys.argv[1:]), encoding="utf-8"
)
template_path = next(
    Path(value[1:])
    for value in sys.argv[1:]
    if value.startswith("@") and value.endswith(".proposal-template.json")
)
proposal = json.loads(template_path.read_text(encoding="utf-8"))
for item in proposal["proposals"]:
    item["target"] = item["source"]
    item["notes"] = "fixture"
proposal.pop("schema_version")
proposal.pop("workset_id")
print(json.dumps(proposal, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            previous = os.environ.get("FAKE_PI_ARGUMENTS")
            os.environ["FAKE_PI_ARGUMENTS"] = str(arguments_path)
            try:
                report = run_pi_translation(
                    workset_path=workset_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(fake_pi),
                )
            finally:
                if previous is None:
                    os.environ.pop("FAKE_PI_ARGUMENTS", None)
                else:
                    os.environ["FAKE_PI_ARGUMENTS"] = previous
            arguments = json.loads(arguments_path.read_text())
        self.assertTrue(report["ok"])
        self.assertEqual(report["normalization"], "added-deterministic-envelope")
        self.assertIn("--no-tools", arguments)
        self.assertIn("--no-context-files", arguments)
        self.assertIn("--no-session", arguments)
        self.assertNotIn("--tools", arguments)
        self.assertEqual(sum(value.startswith("@") for value in arguments), 2)
        self.assertTrue(Path(report["validated_proposal"]).is_file())

    def test_pi_reviewer_has_no_tools_and_validates_findings(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-review-test-") as temporary:
            directory = Path(temporary)
            bundle = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": self.manifest.version,
                "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
                "kind": "code",
                "selection": {"offset": 0, "count": 1, "total": 1},
                "files": [
                    {
                        "item_id": "code-fixture",
                        "path": "tools/fixture.py",
                        "status": "M ",
                        "diff": "@@ -1 +1 @@\n-old\n+new\n",
                    }
                ],
            }
            bundle["bundle_id"] = _bundle_id(bundle)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(
                json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
            )
            arguments_path = directory / "arguments.json"
            fake_pi = directory / "fake-pi-review"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(
    json.dumps(sys.argv[1:]), encoding="utf-8"
)
bundle_path = next(
    Path(value[1:]) for value in sys.argv[1:] if value.startswith("@")
)
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "review_contract": bundle["review_contract"],
    "bundle_id": bundle["bundle_id"],
    "findings": [],
}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            previous = os.environ.get("FAKE_PI_ARGUMENTS")
            os.environ["FAKE_PI_ARGUMENTS"] = str(arguments_path)
            try:
                report = run_pi_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(fake_pi),
                    use_cache=False,
                )
            finally:
                if previous is None:
                    os.environ.pop("FAKE_PI_ARGUMENTS", None)
                else:
                    os.environ["FAKE_PI_ARGUMENTS"] = previous
            arguments = json.loads(arguments_path.read_text())
        self.assertTrue(report["ok"])
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertEqual(report["cache_decision"], "disabled")
        self.assertEqual(report["mode"], "findings-only-v1")
        self.assertFalse(report["pi_tools"])
        self.assertFalse(report["pi_session"])
        self.assertFalse(report["candidate_execution"])
        self.assertEqual(report["concurrency"], 1)
        self.assertEqual(report["attempts"], 1)
        self.assertEqual(report["charged_or_possible_transfers"], 1)
        self.assertEqual(report["validated_results"], 1)
        self.assertGreaterEqual(report["elapsed_seconds"], 0)
        self.assertIn("--no-tools", arguments)
        self.assertIn("--no-context-files", arguments)
        self.assertIn("--no-session", arguments)
        self.assertNotIn("--tools", arguments)
        self.assertEqual(sum(value.startswith("@") for value in arguments), 1)
        self.assertTrue(Path(report["review"]).is_file())

    def test_pi_reviewer_reuses_exact_validated_cache_before_starting_pi(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-review-cache-test-") as temporary:
            directory = Path(temporary)
            bundle = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": self.manifest.version,
                "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
                "kind": "code",
                "selection": {"offset": 0, "count": 1, "total": 1},
                "files": [
                    {
                        "item_id": "code-cache-fixture",
                        "path": "tools/cache_fixture.py",
                        "status": "M ",
                        "diff": "@@ -1 +1 @@\n-old\n+new\n",
                    }
                ],
            }
            bundle["bundle_id"] = _bundle_id(bundle)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(
                json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
            )
            fake_pi = directory / "fake-pi-review-cache"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import sys
from pathlib import Path

bundle_path = next(Path(value[1:]) for value in sys.argv[1:] if value.startswith("@"))
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "review_contract": bundle["review_contract"],
    "bundle_id": bundle["bundle_id"],
    "findings": [],
}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            provider = f"fixture-cache-{directory.name}"
            first = run_pi_review(
                bundle_path=bundle_path,
                provider=provider,
                model="fixture-model",
                thinking="high",
                timeout=30,
                strict=True,
                pi_executable=str(fake_pi),
                use_cache=True,
            )
            cache_path = (
                ROOT
                / ".artifacts"
                / "i18n"
                / "cache"
                / "pi-review"
                / f"{first['result_cache_key']}.json"
            )
            try:
                second = run_pi_review(
                    bundle_path=bundle_path,
                    provider=provider,
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(directory / "does-not-exist"),
                    use_cache=True,
                )
                original = json.loads(cache_path.read_text(encoding="utf-8"))
                for field, value in (
                    ("cache_schema_version", True),
                    ("cache_schema_version", 1.0),
                    ("strict", 1),
                    ("strict", 1.0),
                ):
                    with self.subTest(field=field, value=value):
                        tampered_identity = json.loads(json.dumps(original))
                        tampered_identity[field] = value
                        cache_path.write_text(
                            json.dumps(tampered_identity, ensure_ascii=False),
                            encoding="utf-8",
                        )
                        with self.assertRaisesRegex(
                            AgentError, "cache entry identity is invalid"
                        ):
                            run_pi_review(
                                bundle_path=bundle_path,
                                provider=provider,
                                model="fixture-model",
                                thinking="high",
                                timeout=30,
                                strict=True,
                                pi_executable=str(directory / "does-not-exist"),
                                use_cache=True,
                            )
                tampered = json.loads(json.dumps(original))
                tampered["review"]["review_id"] = "tampered"
                cache_path.write_text(
                    json.dumps(tampered, ensure_ascii=False), encoding="utf-8"
                )
                with self.assertRaises(AgentError):
                    run_pi_review(
                        bundle_path=bundle_path,
                        provider=provider,
                        model="fixture-model",
                        thinking="high",
                        timeout=30,
                        strict=True,
                        pi_executable=str(directory / "does-not-exist"),
                        use_cache=True,
                    )
            finally:
                cache_path.unlink(missing_ok=True)
        self.assertEqual(first["cache_decision"], "miss")
        self.assertEqual(first["attempts"], 1)
        self.assertEqual(second["cache_decision"], "hit")
        self.assertEqual(second["attempts"], 0)
        self.assertEqual(second["charged_or_possible_transfers"], 0)
        self.assertEqual(second["validated_results"], 1)
        self.assertEqual(
            json.loads(Path(first["review"]).read_text(encoding="utf-8")),
            json.loads(Path(second["review"]).read_text(encoding="utf-8")),
        )

    def test_pi_file_reviewer_uses_read_bash_tools_and_validates_findings(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-file-review-test-") as temporary:
            directory = Path(temporary)
            bundle = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": self.manifest.version,
                "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
                "kind": "translations",
                "component": "boot",
                "items": [
                    {
                        "item_id": "translation-file-fixture",
                        "component": "boot",
                        "section": "fixture/file.lua",
                        "source": "%s has %d",
                        "target": "%d 属于 %s",
                        "source_tag": "tformat",
                        "args_order": [2, 1],
                        "special": None,
                    }
                ],
            }
            bundle["bundle_id"] = _bundle_id(bundle)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(
                json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
            )
            arguments_path = directory / "arguments.json"
            cwd_path = directory / "cwd.txt"
            fake_pi = directory / "fake-pi-file-review"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(
    json.dumps(sys.argv[1:]), encoding="utf-8"
)
Path(os.environ["FAKE_PI_CWD"]).write_text(os.getcwd(), encoding="utf-8")
count_path = Path(os.environ["FAKE_PI_CALL_COUNT"])
count = int(count_path.read_text(encoding="utf-8")) if count_path.exists() else 0
count_path.write_text(str(count + 1), encoding="utf-8")
bundle_path = next(
    Path(value[1:]) for value in sys.argv[1:] if value.startswith("@")
)
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "review_contract": bundle["review_contract"],
    "bundle_id": bundle["bundle_id"],
    "findings": [],
}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            previous = os.environ.get("FAKE_PI_ARGUMENTS")
            previous_count = os.environ.get("FAKE_PI_CALL_COUNT")
            call_count_path = directory / "call-count.txt"
            os.environ["FAKE_PI_ARGUMENTS"] = str(arguments_path)
            os.environ["FAKE_PI_CWD"] = str(cwd_path)
            os.environ["FAKE_PI_CALL_COUNT"] = str(call_count_path)
            try:
                first = run_pi_file_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(fake_pi),
                )
                second = run_pi_file_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(fake_pi),
                    force=True,
                )
            finally:
                if previous is None:
                    os.environ.pop("FAKE_PI_ARGUMENTS", None)
                else:
                    os.environ["FAKE_PI_ARGUMENTS"] = previous
                os.environ.pop("FAKE_PI_CWD", None)
                if previous_count is None:
                    os.environ.pop("FAKE_PI_CALL_COUNT", None)
                else:
                    os.environ["FAKE_PI_CALL_COUNT"] = previous_count
            arguments = json.loads(arguments_path.read_text())
            cwd = cwd_path.read_text(encoding="utf-8")
            call_count = int(call_count_path.read_text(encoding="utf-8"))
            report = first
        self.assertTrue(report["ok"])
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertEqual(report["cache_decision"], "disabled")
        self.assertIsNone(report["result_cache_key"])
        self.assertIn("outside the bounded bundle", report["cache_disabled_reason"])
        self.assertEqual(report["mode"], "findings-files-v1")
        self.assertTrue(report["pi_tools"])
        self.assertEqual(report["tools"], ["read,bash"])
        self.assertFalse(report["os_sandbox"])
        self.assertTrue(report["provider_credentials_inherited"])
        self.assertTrue(report["process_group_cleanup"])
        self.assertFalse(report["detached_descendants_checked"])
        self.assertFalse(report["pi_session"])
        self.assertFalse(report["candidate_execution"])
        self.assertEqual(report["concurrency"], 1)
        self.assertEqual(report["attempts"], 1)
        self.assertEqual(report["charged_or_possible_transfers"], 1)
        self.assertEqual(report["validated_results"], 1)
        self.assertEqual(call_count, 2)
        self.assertEqual(second["cache_decision"], "disabled")
        self.assertIsNone(second["result_cache_key"])
        self.assertEqual(second["attempts"], 1)
        self.assertEqual(second["charged_or_possible_transfers"], 1)
        self.assertTrue(report["versioned_worktree_unchanged"])
        self.assertEqual(
            report["versioned_worktree_snapshot_before_sha256"],
            report["versioned_worktree_snapshot_after_sha256"],
        )
        self.assertEqual(
            report["worktree_check_scope"], "tracked-and-nonignored-untracked"
        )
        self.assertFalse(report["ignored_paths_checked"])
        self.assertNotIn("--no-tools", arguments)
        self.assertEqual(arguments[arguments.index("--tools") + 1], "read,bash")
        self.assertIn("--no-context-files", arguments)
        self.assertIn("--no-session", arguments)
        self.assertIn("--no-approve", arguments)
        self.assertIn("--no-skills", arguments)
        self.assertEqual(sum(value.startswith("@") for value in arguments), 1)
        self.assertEqual(cwd, str(ROOT))
        self.assertTrue(Path(report["review"]).is_file())

    def test_pi_file_review_snapshot_detects_changes_in_dirty_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-file-snapshot-") as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            tracked = root / "tracked.txt"
            tracked.write_text("committed\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "tracked.txt"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                check=True,
            )
            tracked.write_text("dirty one\n", encoding="utf-8")
            tracked_before = _git_worktree_snapshot(root)
            tracked.write_text("dirty two\n", encoding="utf-8")
            tracked_after = _git_worktree_snapshot(root)
            untracked = root / "untracked.txt"
            untracked.write_text("untracked one\n", encoding="utf-8")
            untracked_before = _git_worktree_snapshot(root)
            untracked.write_text("untracked two\n", encoding="utf-8")
            untracked_after = _git_worktree_snapshot(root)
        self.assertNotEqual(tracked_before, tracked_after)
        self.assertNotEqual(untracked_before, untracked_after)

    def test_pi_file_review_rejects_a_changed_versioned_worktree(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-file-tamper-") as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".artifacts/\n", encoding="utf-8")
            tracked = root / "tracked.txt"
            tracked.write_text("before\n", encoding="utf-8")
            prompt = root / "i18n" / "prompts" / "pi-reviewer-files.md"
            prompt.parent.mkdir(parents=True)
            prompt.write_text("fixture prompt", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                check=True,
            )
            manifest = replace(self.manifest, root=root)
            bundle = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": manifest.version,
                "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
                "kind": "translations",
                "component": "boot",
                "items": [
                    {
                        "item_id": "translation-tamper-fixture",
                        "component": "boot",
                        "section": "fixture/dialog.lua",
                        "source": "Source",
                        "target": "译文",
                        "source_tag": "_t",
                        "args_order": None,
                        "special": None,
                    }
                ],
            }
            bundle["bundle_id"] = _bundle_id(bundle)
            bundle_path = root / "bundle.json"
            bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
            fake_pi = root / "fake-pi"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import sys
from pathlib import Path

Path("tracked.txt").write_text("after\\n", encoding="utf-8")
bundle_path = next(Path(value[1:]) for value in sys.argv[1:] if value.startswith("@"))
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "review_contract": bundle["review_contract"],
    "bundle_id": bundle["bundle_id"],
    "findings": [],
}))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            with patch("i18nlib.pi_file_review.load_manifest", return_value=manifest):
                with self.assertRaisesRegex(AgentError, "changed the worktree"):
                    run_pi_file_review(
                        bundle_path=bundle_path,
                        provider="fixture",
                        model="fixture-model",
                        thinking="high",
                        timeout=30,
                        strict=True,
                        pi_executable=str(fake_pi),
                        use_cache=False,
                    )
            reports = sorted(
                (root / ".artifacts" / "i18n" / "runs").glob(
                    "*-pi-file-review/pi-review.json"
                )
            )
            report = json.loads(reports[-1].read_text(encoding="utf-8"))
            raw_output_exists = Path(report["raw_output"]).is_file()
        self.assertFalse(report["versioned_worktree_unchanged"])
        self.assertTrue(raw_output_exists)
        self.assertIn("raw_output_sha256", report)

    def test_pi_file_reviewer_builds_code_bundle_inventory(self) -> None:
        bundle = {
            "kind": "code",
            "files": [{"item_id": "code-file-fixture"}],
        }
        arguments = build_file_review_command(
            executable="pi",
            provider="fixture",
            model="fixture-model",
            thinking="high",
            system_prompt="fixture prompt",
            bundle=bundle,
            bundle_resolved=Path("/tmp/code-bundle.json"),
        )
        self.assertNotIn("--no-tools", arguments)
        self.assertEqual(arguments[arguments.index("--tools") + 1], "read,bash")
        self.assertIn('"code-file-fixture"', arguments[-1])

    def test_pi_file_review_result_cache_is_unavailable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-file-review-cache-") as temporary:
            directory = Path(temporary)
            bundle = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": self.manifest.version,
                "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
                "kind": "translations",
                "component": "boot",
                "items": [
                    {
                        "item_id": "translation-file-cache-fixture",
                        "component": "boot",
                        "section": "fixture/file-cache.lua",
                        "source": "File cache",
                        "target": "文件缓存",
                        "source_tag": "nil",
                        "args_order": None,
                        "special": None,
                    }
                ],
            }
            bundle["bundle_id"] = _bundle_id(bundle)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(
                json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
            )
            headless_parser = pi_file_review_parser()
            headless_default = headless_parser.parse_args(["--bundle", str(bundle_path)])
            headless_explicit = headless_parser.parse_args(
                ["--bundle", str(bundle_path), "--cache"]
            )
            headless_force = headless_parser.parse_args(
                ["--bundle", str(bundle_path), "--force"]
            )
            headless_help = " ".join(headless_parser.format_help().split())
            self.assertFalse(headless_default.cache)
            self.assertTrue(headless_explicit.cache)
            self.assertTrue(headless_force.force)
            self.assertIn("--cache is rejected", headless_help)
            self.assertIn("always true for file-reading reviews", headless_help)

            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                exit_code = pi_file_review_main(
                    ["--bundle", str(bundle_path), "--cache"]
                )
            self.assertEqual(exit_code, ValidationError.exit_code)
            self.assertIn("--cache is unavailable", stderr.getvalue())

            with self.assertRaisesRegex(
                ValidationError, r"--cache is unavailable: .*outside the bounded bundle"
            ):
                run_pi_file_review(
                    bundle_path=bundle_path,
                    provider="fixture-file-cache",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(directory / "does-not-exist"),
                    use_cache=headless_explicit.cache,
                )
            with self.assertRaisesRegex(
                ValidationError, r"--cache is unavailable: .*outside the bounded bundle"
            ):
                run_tmux_file_review(
                    bundle_path=bundle_path,
                    provider="fixture-file-cache",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    use_cache=True,
                    force=False,
                    pi_executable=str(directory / "does-not-exist"),
                    tmux_executable=str(directory / "does-not-exist"),
                )

        for use_cache, force, message in (
            (True, False, r"--cache is unavailable: .*outside the bounded bundle"),
            (
                True,
                True,
                r"--cache is unavailable \(including with --force\): .*outside the bounded bundle",
            ),
        ):
            with self.subTest(use_cache=use_cache, force=force):
                with self.assertRaisesRegex(ValidationError, message):
                    _validate_file_review_cache_options(
                        use_cache=use_cache, force=force
                    )
        _validate_file_review_cache_options(use_cache=False, force=True)

    def test_pi_remediator_binds_proposals_to_findings(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-remediate-test-") as temporary:
            directory = Path(temporary)
            bundle = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": self.manifest.version,
                "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
                "kind": "translations",
                "component": "boot",
                "items": [
                    {
                        "item_id": "translation-fixture",
                        "component": "boot",
                        "section": "fixture/dialog.lua",
                        "source": "Water lair",
                        "target": "水下墓穴",
                        "source_tag": "nil",
                        "args_order": None,
                        "special": None,
                    }
                ],
            }
            bundle["bundle_id"] = _bundle_id(bundle)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(
                json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
            )
            review = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "bundle_id": bundle["bundle_id"],
                "review_id": "review-fixture",
                "findings": [
                    {
                        "finding_id": "finding-fixture",
                        "severity": "minor",
                        "category": "translation",
                        "item_id": "translation-fixture",
                        "title": "fixture",
                        "body": "fixture finding",
                    }
                ],
            }
            review_path = directory / "review.json"
            review_path.write_text(
                json.dumps(review, ensure_ascii=False), encoding="utf-8"
            )
            fake_pi = directory / "fake-pi-remediate"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import sys
from pathlib import Path

bundle_path = next(Path(value[1:]) for value in sys.argv[1:] if value.startswith("@") and "bundle" in value)
review_path = next(Path(value[1:]) for value in sys.argv[1:] if value.startswith("@") and "review" in value)
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
review = json.loads(review_path.read_text(encoding="utf-8"))
item = bundle["items"][0]
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "remediation_contract": "tome4-review-remediation-v1",
    "bundle_id": bundle["bundle_id"],
    "review_id": review["review_id"],
    "proposals": [{
        "finding_id": review["findings"][0]["finding_id"],
        "item_id": item["item_id"],
        "action": "replace-translation",
        "source": item["source"],
        "source_tag": item["source_tag"],
        "original_target": item["target"],
        "target": "水下巢穴",
        "args_order": item["args_order"],
        "special": item["special"],
        "rationale": "fixture remediation",
    }],
}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            report = run_pi_remediation(
                bundle_path=bundle_path,
                review_path=review_path,
                provider="fixture",
                model="fixture-model",
                thinking="high",
                timeout=30,
                strict=True,
                pi_executable=str(fake_pi),
            )
        self.assertTrue(report["ok"])
        self.assertEqual(report["summary"]["replace_translation"], 1)
        self.assertTrue(Path(report["remediation"]).is_file())


class PiTmuxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    def _review_bundle(self, directory: Path) -> tuple[dict[str, object], Path]:
        bundle = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": self.manifest.version,
            "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            "kind": "code",
            "selection": {"offset": 0, "count": 1, "total": 1},
            "files": [
                {
                    "item_id": "code-tmux-fixture",
                    "path": "tools/tmux_fixture.py",
                    "status": "M ",
                    "diff": "@@ -1 +1 @@\n-old\n+new\n",
                }
            ],
        }
        bundle["bundle_id"] = _bundle_id(bundle)
        bundle_path = directory / "bundle.json"
        bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
        return bundle, bundle_path

    def _legacy_translation_bundle(
        self, directory: Path
    ) -> tuple[dict[str, object], Path]:
        bundle = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": self.manifest.version,
            "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            "kind": "translations",
            "component": "boot",
            "items": [
                {
                    "item_id": "translation-tmux-fixture",
                    "component": "boot",
                    "section": "fixture/dialog.lua",
                    "source": "%s has %d",
                    "target": "%d 属于 %s",
                    "source_tag": "tformat",
                    "args_order": [2, 1],
                    "special": None,
                }
            ],
        }
        bundle["bundle_id"] = _bundle_id(bundle)
        bundle_path = directory / "translation-bundle.json"
        bundle_path.write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        return bundle, bundle_path

    def _fake_tmux(self, directory: Path) -> tuple[Path, Path]:
        fake_tmux = directory / "fake-tmux"
        fake_tmux.write_text(FAKE_TMUX_SCRIPT, encoding="utf-8")
        fake_tmux.chmod(0o700)
        tmux_log = directory / "tmux-log.jsonl"
        tmux_state = directory / "tmux-state"
        os.environ["FAKE_TMUX_LOG"] = str(tmux_log)
        os.environ["FAKE_TMUX_STATE"] = str(tmux_state)
        return fake_tmux, tmux_log

    def _fake_pi_review(self, directory: Path) -> Path:
        fake_pi = directory / "fake-pi-tmux-review"
        fake_pi.write_text(FAKE_PI_REVIEW_SCRIPT, encoding="utf-8")
        fake_pi.chmod(0o700)
        os.environ["FAKE_PI_ARGUMENTS"] = str(directory / "pi-arguments.json")
        return fake_pi

    def test_execute_in_pane_rejects_options_before_writing_job(self) -> None:
        base = {
            "run_directory": Path("unused-run-directory"),
            "title": "unused-title",
            "job": {},
            "timeout": 30,
            "tmux_executable": "unused-tmux",
            "session": "fixture-session",
            "layout": "vertical",
            "percent": 35,
            "keep_pane": True,
            "fallback": "error",
        }
        cases = (
            ("layout", "grid"),
            ("percent", 0),
            ("percent", 100),
            ("percent", False),
            ("percent", 35.0),
            ("keep_pane", 1),
            ("fallback", "ignore"),
            ("session", " \n"),
            ("session", False),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value):
                with (
                    patch("i18nlib.pi_tmux.write_json") as write_job,
                    patch("i18nlib.pi_tmux._run_tmux") as run_tmux,
                    patch("i18nlib.pi_tmux.run_worker_job") as run_worker,
                ):
                    with self.assertRaises(ValidationError):
                        execute_in_pane(**{**base, field: value})
                    write_job.assert_not_called()
                    run_tmux.assert_not_called()
                    run_worker.assert_not_called()

    def test_split_pane_validates_before_tmux(self) -> None:
        base = {
            "tmux": "unused-tmux",
            "session": "fixture-session",
            "layout": "vertical",
            "percent": 35,
            "start_directory": Path("unused-directory"),
            "command": "unused-command",
            "title": "unused-title",
        }
        cases = (
            ("layout", "square"),
            ("layout", None),
            ("percent", 0),
            ("percent", 100),
            ("percent", True),
            ("percent", "35"),
            ("session", ""),
            ("session", " \t"),
            ("session", 1),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value), patch(
                "i18nlib.pi_tmux._run_tmux"
            ) as run_tmux:
                with self.assertRaises(ValidationError):
                    split_pane(**{**base, field: value})
                run_tmux.assert_not_called()

    def test_percent_boundaries_are_accepted(self) -> None:
        for percent in (1, 99):
            completed = subprocess.CompletedProcess(
                ["tmux"], 0, stdout="%42\n", stderr=""
            )
            with self.subTest(percent=percent), patch(
                "i18nlib.pi_tmux._run_tmux", return_value=completed
            ) as run_tmux:
                pane_id = split_pane(
                    "tmux",
                    session="fixture-session",
                    layout="horizontal",
                    percent=percent,
                    start_directory=Path("unused-directory"),
                    command="unused-command",
                    title="unused-title",
                )
            self.assertEqual(pane_id, "%42")
            split_arguments = run_tmux.call_args_list[0].args[1]
            self.assertEqual(split_arguments[0:2], ["split-window", "-v"])
            self.assertEqual(
                split_arguments[split_arguments.index("-p") + 1], str(percent)
            )

    def test_pi_review_script_rejects_before_any_artifact_side_effect(self) -> None:
        runs_base = ROOT / ".artifacts" / "i18n" / "runs"
        cache_base = ROOT / ".artifacts" / "i18n" / "cache" / "pi-review"

        def observed() -> tuple[set[str], set[str]]:
            runs = (
                {
                    path.name
                    for path in runs_base.iterdir()
                    if path.name.endswith("-pi-review")
                }
                if runs_base.is_dir()
                else set()
            )
            cache = (
                {path.name for path in cache_base.iterdir()}
                if cache_base.is_dir()
                else set()
            )
            return runs, cache

        before_runs, before_cache = observed()
        completed = subprocess.run(
            [sys.executable, str(TOOLS / "pi-review")],
            capture_output=True,
            text=True,
            timeout=30,
        )
        after_runs, after_cache = observed()
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("retired", completed.stderr)
        self.assertIn("translation_contextual_v1", completed.stderr)
        self.assertEqual(after_runs, before_runs)
        self.assertEqual(after_cache, before_cache)

    def test_pi_tmux_review_entry_rejects_before_side_effects(self) -> None:
        stderr = io.StringIO()
        with (
            patch("i18nlib.pi_tmux.run_tmux_review") as runner,
            patch("i18nlib.pi_tmux.load_manifest") as load,
            patch("i18nlib.pi_tmux.validate_review_bundle") as validate_bundle,
            patch("i18nlib.pi_tmux.create_run_directory") as create_run,
            patch("i18nlib.pi_tmux.write_json") as write,
            patch("i18nlib.pi_tmux._pi_environment") as pi_environment,
            patch("i18nlib.pi_tmux._run_tmux") as run_tmux,
            patch("i18nlib.pi_tmux.execute_in_pane") as execute,
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = pi_tmux_main(["review"])
        self.assertNotEqual(exit_code, 0)
        self.assertIn("retired", stderr.getvalue())
        self.assertIn("translation_contextual_v1", stderr.getvalue())
        runner.assert_not_called()
        load.assert_not_called()
        validate_bundle.assert_not_called()
        create_run.assert_not_called()
        write.assert_not_called()
        pi_environment.assert_not_called()
        run_tmux.assert_not_called()
        execute.assert_not_called()

    def test_pi_tmux_file_review_entry_rejects_before_side_effects(self) -> None:
        stderr = io.StringIO()
        with (
            patch("i18nlib.pi_tmux.run_tmux_file_review") as runner,
            patch("i18nlib.pi_tmux.load_manifest") as load,
            patch("i18nlib.pi_tmux.validate_review_bundle") as validate_bundle,
            patch("i18nlib.pi_tmux.create_run_directory") as create_run,
            patch("i18nlib.pi_tmux.write_json") as write,
            patch("i18nlib.pi_tmux._pi_environment") as pi_environment,
            patch("i18nlib.pi_tmux._run_tmux") as run_tmux,
            patch("i18nlib.pi_tmux.execute_in_pane") as execute,
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = pi_tmux_main(["review-files"])
        self.assertNotEqual(exit_code, 0)
        self.assertIn("retired", stderr.getvalue())
        self.assertIn("translation_contextual_v1", stderr.getvalue())
        runner.assert_not_called()
        load.assert_not_called()
        validate_bundle.assert_not_called()
        create_run.assert_not_called()
        write.assert_not_called()
        pi_environment.assert_not_called()
        run_tmux.assert_not_called()
        execute.assert_not_called()

    def test_cli_invalid_percent_uses_validation_error_without_artifacts(self) -> None:
        for percent in ("0", "-1", "100"):
            stderr = io.StringIO()
            with self.subTest(percent=percent):
                with (
                    patch("i18nlib.pi_tmux.load_manifest") as load,
                    patch("i18nlib.pi_tmux.create_run_directory") as create_run,
                    patch("i18nlib.pi_tmux.write_json") as write,
                    patch("i18nlib.pi_tmux._run_tmux") as run_tmux,
                    patch("i18nlib.pi_tmux.execute_in_pane") as execute,
                    contextlib.redirect_stderr(stderr),
                ):
                    exit_code = pi_tmux_main(
                        [
                            "translate",
                            "--workset",
                            "unused-workset.json",
                            "--percent",
                            percent,
                        ]
                    )
                self.assertEqual(exit_code, ValidationError.exit_code)
                self.assertIn("integer from 1 to 99", stderr.getvalue())
                load.assert_not_called()
                create_run.assert_not_called()
                write.assert_not_called()
                run_tmux.assert_not_called()
                execute.assert_not_called()

    def test_worker_status_schema_rejects_non_integer_versions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-status-schema-") as temporary:
            directory = Path(temporary)
            path = directory / "worker-status.json"
            for schema_version in (True, 1.0):
                with self.subTest(schema_version=schema_version):
                    path.write_text(
                        json.dumps({"schema_version": schema_version}),
                        encoding="utf-8",
                    )
                    with self.assertRaisesRegex(
                        AgentError, "worker status has an unsupported schema"
                    ):
                        _read_status(directory)

    def test_worker_job_schema_rejects_non_integer_versions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-job-schema-") as temporary:
            path = Path(temporary) / "job.json"
            for schema_version in (True, 1.0):
                with self.subTest(schema_version=schema_version):
                    path.write_text(
                        json.dumps({"job_schema_version": schema_version}),
                        encoding="utf-8",
                    )
                    stderr = io.StringIO()
                    with (
                        patch("i18nlib.pi_tmux.run_worker_job") as run_worker,
                        contextlib.redirect_stderr(stderr),
                    ):
                        exit_code = worker_main(path)
                    self.assertEqual(exit_code, 125)
                    self.assertIn("unsupported worker job", stderr.getvalue())
                    run_worker.assert_not_called()

    def test_tmux_review_runs_pi_in_pane_and_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-test-") as temporary:
            directory = Path(temporary)
            _, bundle_path = self._review_bundle(directory)
            fake_tmux, tmux_log = self._fake_tmux(directory)
            fake_pi = self._fake_pi_review(directory)
            report = run_tmux_review(
                bundle_path=bundle_path,
                provider="fixture",
                model="fixture-model",
                thinking="high",
                timeout=60,
                strict=True,
                use_cache=False,
                force=False,
                pi_executable=str(fake_pi),
                tmux_executable=str(fake_tmux),
                session="fake-session",
                fallback="error",
            )
            arguments = json.loads(
                (directory / "pi-arguments.json").read_text(encoding="utf-8")
            )
            tmux_calls = [
                json.loads(line) for line in tmux_log.read_text().splitlines()
            ]
        self.assertTrue(report["ok"])
        self.assertEqual(report["execution"], "tmux")
        self.assertEqual(report["pane"], "%99")
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertEqual(report["attempts"], 1)
        self.assertEqual(report["charged_or_possible_transfers"], 1)
        self.assertEqual(report["cache_decision"], "disabled")
        self.assertTrue(Path(report["review"]).is_file())
        self.assertIn("--no-tools", arguments)
        self.assertIn("--no-session", arguments)
        self.assertIn("--no-context-files", arguments)
        self.assertEqual(sum(value.startswith("@") for value in arguments), 1)
        self.assertTrue(any(call[0] == "split-window" for call in tmux_calls))
        self.assertTrue(any(call[0] == "select-pane" for call in tmux_calls))

    def test_tmux_file_review_runs_with_read_bash_tools(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-file-test-") as temporary:
            directory = Path(temporary)
            _, bundle_path = self._review_bundle(directory)
            fake_tmux, tmux_log = self._fake_tmux(directory)
            fake_pi = self._fake_pi_review(directory)
            call_count_path = directory / "call-count.txt"
            previous_count = os.environ.get("FAKE_PI_CALL_COUNT")
            os.environ["FAKE_PI_CALL_COUNT"] = str(call_count_path)
            try:
                report = run_tmux_file_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=60,
                    strict=True,
                    pi_executable=str(fake_pi),
                    tmux_executable=str(fake_tmux),
                    session="fake-session",
                    fallback="error",
                )
                second = run_tmux_file_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=60,
                    strict=True,
                    force=True,
                    pi_executable=str(fake_pi),
                    tmux_executable=str(fake_tmux),
                    session="fake-session",
                    fallback="error",
                )
            finally:
                if previous_count is None:
                    os.environ.pop("FAKE_PI_CALL_COUNT", None)
                else:
                    os.environ["FAKE_PI_CALL_COUNT"] = previous_count
            arguments = json.loads(
                (directory / "pi-arguments.json").read_text(encoding="utf-8")
            )
            tmux_calls = [
                json.loads(line) for line in tmux_log.read_text().splitlines()
            ]
            call_count = int(call_count_path.read_text(encoding="utf-8"))
        self.assertTrue(report["ok"])
        self.assertEqual(report["execution"], "tmux")
        self.assertEqual(report["cache_decision"], "disabled")
        self.assertIsNone(report["result_cache_key"])
        self.assertIn("outside the bounded bundle", report["cache_disabled_reason"])
        self.assertTrue(report["versioned_worktree_unchanged"])
        self.assertNotIn("--no-tools", arguments)
        self.assertEqual(arguments[arguments.index("--tools") + 1], "read,bash")
        self.assertEqual(call_count, 2)
        self.assertEqual(second["cache_decision"], "disabled")
        self.assertIsNone(second["result_cache_key"])
        self.assertEqual(second["attempts"], 1)
        self.assertEqual(second["charged_or_possible_transfers"], 1)
        self.assertEqual(
            sum(call[0] == "split-window" for call in tmux_calls), 2
        )

    def test_tmux_review_cache_hit_skips_pane(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-cache-test-") as temporary:
            directory = Path(temporary)
            _, bundle_path = self._review_bundle(directory)
            fake_tmux, tmux_log = self._fake_tmux(directory)
            fake_pi = self._fake_pi_review(directory)
            provider = f"fixture-tmux-cache-{directory.name}"
            first = run_tmux_review(
                bundle_path=bundle_path,
                provider=provider,
                model="fixture-model",
                thinking="high",
                timeout=60,
                strict=True,
                use_cache=True,
                force=False,
                pi_executable=str(fake_pi),
                tmux_executable=str(fake_tmux),
                session="fake-session",
                fallback="error",
            )
            cache_path = (
                ROOT
                / ".artifacts"
                / "i18n"
                / "cache"
                / "pi-review"
                / f"{first['result_cache_key']}.json"
            )
            try:
                second = run_tmux_review(
                    bundle_path=bundle_path,
                    provider=provider,
                    model="fixture-model",
                    thinking="high",
                    timeout=60,
                    strict=True,
                    use_cache=True,
                    force=False,
                    pi_executable=str(directory / "does-not-exist"),
                    tmux_executable=str(fake_tmux),
                    session="fake-session",
                    fallback="error",
                )
            finally:
                cache_path.unlink(missing_ok=True)
            tmux_calls = [
                json.loads(line) for line in tmux_log.read_text().splitlines()
            ]
        self.assertEqual(first["cache_decision"], "miss")
        self.assertEqual(second["cache_decision"], "hit")
        self.assertEqual(second["execution"], "cache")
        self.assertIsNone(second["pane"])
        self.assertEqual(second["attempts"], 0)
        self.assertEqual(second["charged_or_possible_transfers"], 0)
        self.assertEqual(
            json.loads(Path(first["review"]).read_text(encoding="utf-8")),
            json.loads(Path(second["review"]).read_text(encoding="utf-8")),
        )
        self.assertEqual(
            sum(call[0] == "split-window" for call in tmux_calls), 1
        )

    def test_tmux_review_falls_back_to_foreground(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-foreground-test-") as temporary:
            directory = Path(temporary)
            _, bundle_path = self._review_bundle(directory)
            fake_pi = self._fake_pi_review(directory)
            previous_tmux = os.environ.pop("TMUX", None)
            previous_pane = os.environ.pop("TMUX_PANE", None)
            try:
                report = run_tmux_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=60,
                    strict=True,
                    use_cache=False,
                    force=False,
                    pi_executable=str(fake_pi),
                    session=None,
                    fallback="foreground",
                )
            finally:
                if previous_tmux is not None:
                    os.environ["TMUX"] = previous_tmux
                if previous_pane is not None:
                    os.environ["TMUX_PANE"] = previous_pane
        self.assertTrue(report["ok"])
        self.assertEqual(report["execution"], "foreground")
        self.assertIsNone(report["pane"])
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertTrue(Path(report["review"]).is_file())

    def test_tmux_remediation_runs_in_pane_and_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-remediate-test-") as temporary:
            directory = Path(temporary)
            _, bundle_path = self._legacy_translation_bundle(directory)
            review = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "bundle_id": json.loads(
                    bundle_path.read_text(encoding="utf-8")
                )["bundle_id"],
                "review_id": "review-tmux-fixture",
                "findings": [
                    {
                        "finding_id": "finding-tmux-fixture",
                        "severity": "minor",
                        "category": "translation",
                        "item_id": "translation-tmux-fixture",
                        "title": "fixture",
                        "body": "fixture finding",
                    }
                ],
            }
            review_path = directory / "review.json"
            review_path.write_text(
                json.dumps(review, ensure_ascii=False), encoding="utf-8"
            )
            fake_tmux, _ = self._fake_tmux(directory)
            fake_pi = directory / "fake-pi-tmux-remediate"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import sys
from pathlib import Path

bundle_path = next(
    Path(value[1:]) for value in sys.argv[1:]
    if value.startswith("@") and "bundle" in value
)
review_path = next(
    Path(value[1:]) for value in sys.argv[1:]
    if value.startswith("@") and "review" in value
)
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
review = json.loads(review_path.read_text(encoding="utf-8"))
item = bundle["items"][0]
print(json.dumps({
    "schema_version": bundle["schema_version"],
    "remediation_contract": "tome4-review-remediation-v1",
    "bundle_id": bundle["bundle_id"],
    "review_id": review["review_id"],
    "proposals": [{
        "finding_id": review["findings"][0]["finding_id"],
        "item_id": item["item_id"],
        "action": "replace-translation",
        "source": item["source"],
        "source_tag": item["source_tag"],
        "original_target": item["target"],
        "target": "%d 属于 %s",
        "args_order": item["args_order"],
        "special": item["special"],
        "rationale": "fixture remediation",
    }],
}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            report = run_tmux_remediation(
                bundle_path=bundle_path,
                review_path=review_path,
                provider="fixture",
                model="fixture-model",
                thinking="high",
                timeout=60,
                strict=True,
                pi_executable=str(fake_pi),
                tmux_executable=str(fake_tmux),
                session="fake-session",
                fallback="error",
            )
        self.assertTrue(report["ok"])
        self.assertEqual(report["execution"], "tmux")
        self.assertEqual(report["pane"], "%99")
        self.assertEqual(report["summary"]["replace_translation"], 1)
        self.assertTrue(Path(report["remediation"]).is_file())

    def test_tmux_worker_tees_streams_and_reports_timeout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-worker-test-") as temporary:
            directory = Path(temporary)
            fake_pi = directory / "fake-slow-pi"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import sys
import time
print("streamed stdout")
print("streamed stderr", file=sys.stderr)
sys.stderr.flush()
sys.stdout.flush()
time.sleep(30)
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            job_path = directory / "job.json"
            job_path.write_text(
                json.dumps(
                    {
                        "job_schema_version": 1,
                        "tool_version": TOOL_VERSION,
                        "kind": "review",
                        "root": str(ROOT),
                        "provider": "fixture",
                        "cwd": str(directory),
                        "argv": [str(fake_pi)],
                        "timeout_seconds": 2,
                    }
                ),
                encoding="utf-8",
            )
            status = run_worker_job(
                json.loads(job_path.read_text(encoding="utf-8")), job_path
            )
            raw = (directory / "raw-output.txt").read_text(encoding="utf-8")
            stderr = (directory / "pi-stderr.txt").read_text(encoding="utf-8")
            status_written = (directory / "worker-status.json").is_file()
        self.assertTrue(status["timed_out"])
        self.assertIn("Pi timed out", status["error"])
        self.assertIn("streamed stdout", raw)
        self.assertIn("streamed stderr", stderr)
        self.assertTrue(status_written)

    def test_tmux_worker_rejects_changed_stdin_before_starting_pi(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-tmux-stdin-test-") as temporary:
            directory = Path(temporary)
            stdin_path = directory / "provider-message.json"
            stdin_path.write_bytes(b'{"fixture":true}')
            marker = directory / "pi-started"
            fake_pi = directory / "fake-pi"
            fake_pi.write_text(
                f"#!/bin/sh\ntouch {shlex.quote(str(marker))}\n",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            job_path = directory / "job.json"
            job = {
                "job_schema_version": 1,
                "tool_version": TOOL_VERSION,
                "kind": "review",
                "root": str(ROOT),
                "provider": "fixture",
                "cwd": str(directory),
                "argv": [str(fake_pi)],
                "stdin_path": str(stdin_path),
                "stdin_sha256": "0" * 64,
                "stdin_bytes": stdin_path.stat().st_size,
                "timeout_seconds": 2,
            }
            job_path.write_text(json.dumps(job), encoding="utf-8")
            with self.assertRaisesRegex(AgentError, "stdin payload identity"):
                run_worker_job(job, job_path)
            self.assertFalse(marker.exists())


class PiQualityEvaluatorTests(unittest.TestCase):
    """Blind model evaluator runner and host-owned assessment envelope."""

    @classmethod
    def setUpClass(cls) -> None:
        quality_validation_tests.QualityValidationTests.setUpClass()
        cls.manifest = quality_validation_tests.QualityValidationTests.manifest
        cls.taxonomy = quality_validation_tests.QualityValidationTests.taxonomy
        cls.qpolicy = quality_validation_tests.QualityValidationTests.qpolicy
        cls.sample = quality_validation_tests.QualityValidationTests.sample
        cls.sample_path = quality_validation_tests.QualityValidationTests.sample_path

    def test_quality_evaluator_repairs_only_missing_outer_brace(self) -> None:
        output, normalization = _decode_quality_model_output(b'{"items": []')
        self.assertEqual(output, {"items": []})
        self.assertEqual(normalization, "added-missing-outer-brace")
        with self.assertRaises(ValidationError):
            _decode_quality_model_output(b'{"items": [}')

    def test_quality_evaluator_command_is_isolated(self) -> None:
        bundle = build_quality_evaluator_bundle(
            self.sample,
            self.taxonomy,
            evaluator_id="reviewer-a",
            method_version=self.qpolicy["pilot"]["method_version"],
        )
        command = build_quality_evaluator_command(
            executable="pi",
            provider="fixture",
            model="fixture-model",
            thinking="max",
            system_prompt="fixture prompt",
            bundle_path=Path("quality-bundle.json"),
        )
        self.assertEqual(bundle["evaluator_id"], "reviewer-a")
        self.assertEqual(len(bundle["items"]), 120)
        self.assertIn("--no-tools", command)
        self.assertIn("--no-session", command)
        self.assertIn("--no-context-files", command)
        self.assertIn("--no-skills", command)
        self.assertEqual(command[command.index("--thinking") + 1], "max")
        attachment = next(value for value in command if value.startswith("@"))
        self.assertFalse(Path(attachment[1:]).is_absolute())

    def test_quality_evaluator_cache_strict_identity_rejects_numbers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-quality-cache-") as temporary:
            directory = Path(temporary)
            cache_path = directory / "cache.json"
            output_path = directory / "assessment.json"
            bundle = {"bundle_id": "quality-cache-bundle-fixture"}
            identity = {
                "cache_contract": QUALITY_EVALUATOR_CACHE_CONTRACT,
                "cache_key": "quality-cache-key-fixture",
                "bundle_id": bundle["bundle_id"],
                "provider": "fixture",
                "model": "fixture-model",
                "thinking": "max",
                "prompt_sha256": "0" * 64,
            }
            for strict_value in (1, 1.0):
                with self.subTest(strict_value=strict_value):
                    cache_path.write_text(
                        json.dumps(
                            {
                                **identity,
                                "strict": strict_value,
                                "assessment": {},
                            }
                        ),
                        encoding="utf-8",
                    )
                    with (
                        patch(
                            "i18nlib.pi_quality._validated_assessment"
                        ) as validate_assessment,
                        self.assertRaisesRegex(
                            ValidationError,
                            "quality evaluator cache identity does not match",
                        ),
                    ):
                        _load_cached_assessment(
                            self.manifest,
                            path=cache_path,
                            cache_key=identity["cache_key"],
                            bundle=bundle,
                            sample_path=self.sample_path,
                            provider=identity["provider"],
                            model=identity["model"],
                            thinking=identity["thinking"],
                            prompt_sha256=identity["prompt_sha256"],
                            strict=True,
                            output_path=output_path,
                        )
                    validate_assessment.assert_not_called()
                    self.assertFalse(output_path.exists())

    def test_quality_evaluator_validates_complete_blind_assessment(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-pi-quality-test-") as temporary:
            directory = Path(temporary)
            fake_pi = directory / "fake-pi-quality"
            arguments_path = directory / "arguments.json"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(
    json.dumps(sys.argv[1:]), encoding="utf-8"
)
bundle_path = next(Path(value[1:]) for value in sys.argv[1:] if value.startswith("@"))
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
items = [{
    "revision_id": item["revision_id"],
    "context_sufficient": True,
    "profile_confirmed": item["profile"],
    "findings": [],
    "reuse_recommendation": "same-tag",
} for item in bundle["items"]]
print(json.dumps({"items": items}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            with patch.dict(os.environ, {"FAKE_PI_ARGUMENTS": str(arguments_path)}):
                report = run_pi_quality_evaluator(
                    sample_path=self.sample_path,
                    evaluator_id="reviewer-a",
                    provider="fixture",
                    model="fixture-model",
                    thinking="max",
                    timeout=30,
                    strict=True,
                    use_cache=False,
                    pi_executable=str(fake_pi),
                )
            assessment = json.loads(
                Path(report["assessment"]).read_text(encoding="utf-8")
            )
            arguments = json.loads(arguments_path.read_text(encoding="utf-8"))
        self.assertTrue(report["ok"])
        self.assertEqual(report["items"], 120)
        self.assertEqual(report["validated_results"], 1)
        self.assertEqual(report["blind_inputs"]["other_assessments"], False)
        self.assertEqual(assessment["evaluator"]["kind"], "model")
        self.assertEqual(assessment["evaluator"]["id"], "reviewer-a")
        self.assertEqual(assessment["evaluator"]["thinking"], "max")
        self.assertEqual(len(assessment["items"]), 120)
        self.assertNotIn("adjudication", assessment)
        self.assertIn("--no-tools", arguments)


class PiEventStreamTests(unittest.TestCase):
    """pi --mode json event stream extraction (live pane visibility)."""

    def test_extracts_final_assistant_text_from_event_stream(self) -> None:
        from i18nlib.proposal import extract_event_stream_output

        stream = (
            b'{"type":"session","version":3,"id":"s1"}\n'
            b'{"type":"agent_start"}\n'
            b'{"type":"message_start","message":{"role":"user","content":[]}}\n'
            b'{"type":"message_end","message":{"role":"user","content":[]}}\n'
            b'{"type":"message_end","message":{"role":"assistant",'
            b'"content":[{"type":"reasoning","text":"think think"},'
            b'{"type":"text","text":"review payload"}]}}\n'
            b'{"type":"agent_end"}\n'
        )
        self.assertEqual(
            extract_event_stream_output(stream, "Pi review output"),
            b"review payload",
        )

    def test_plain_output_passes_through_unchanged(self) -> None:
        from i18nlib.proposal import extract_event_stream_output

        plain = b'{"findings": []}'
        self.assertEqual(
            extract_event_stream_output(plain, "Pi review output"), plain
        )

    def test_event_stream_without_assistant_text_is_empty(self) -> None:
        from i18nlib.proposal import extract_event_stream_output

        stream = b'{"type":"session","version":3}\n{"type":"agent_end"}\n'
        self.assertEqual(
            extract_event_stream_output(stream, "Pi review output"), b""
        )


class PiPanePreviewTests(unittest.TestCase):
    """Readable line-oriented pane preview for the pi --mode json stream."""

    def _render(self, lines: list[bytes]) -> str:
        import io

        from i18nlib.pi_tmux import PaneStreamRenderer

        mirror = io.BytesIO()
        renderer = PaneStreamRenderer(mirror, use_color=False)
        for line in lines:
            renderer.feed_line(line)
        renderer.flush()
        return mirror.getvalue().decode("utf-8")

    def test_plain_lines_pass_through_unchanged(self) -> None:
        self.assertEqual(self._render([b"streamed stdout", b"streamed stderr"]),
                         "streamed stdout\nstreamed stderr\n")

    def test_status_events_become_readable_lines(self) -> None:
        output = self._render(
            [
                b'{"type":"agent_start"}',
                b'{"type":"message_end","message":{"role":"assistant","content":[]}}',
            ]
        )
        self.assertIn("[pi] agent_start", output)
        self.assertIn("[pi] message_end role=assistant", output)

    def test_deltas_are_assembled_into_complete_lines(self) -> None:
        output = self._render(
            [
                b'{"type":"message_update","assistantMessageEvent":'
                b'{"type":"thinking_start","delta":""}}',
                b'{"type":"message_update","assistantMessageEvent":'
                b'{"type":"thinking_delta","delta":"first "}}',
                b'{"type":"message_update","assistantMessageEvent":'
                b'{"type":"thinking_delta","delta":"line\\nsec"}}',
                b'{"type":"message_update","assistantMessageEvent":'
                b'{"type":"thinking_delta","delta":"ond"}}',
                b'{"type":"message_update","assistantMessageEvent":'
                b'{"type":"thinking_end","delta":""}}',
            ]
        )
        self.assertEqual(output, "first line\nsecond\n")

    def test_thinking_deltas_are_dimmed_when_colored(self) -> None:
        import io

        from i18nlib.pi_tmux import PaneStreamRenderer

        mirror = io.BytesIO()
        renderer = PaneStreamRenderer(mirror, use_color=True)
        renderer.feed_line(
            b'{"type":"message_update","assistantMessageEvent":'
            b'{"type":"thinking_start","delta":""}}'
        )
        renderer.feed_line(
            b'{"type":"message_update","assistantMessageEvent":'
            b'{"type":"thinking_delta","delta":"deep thoughts\\n"}}'
        )
        renderer.feed_line(
            b'{"type":"message_update","assistantMessageEvent":'
            b'{"type":"text_start","delta":""}}'
        )
        renderer.feed_line(
            b'{"type":"message_update","assistantMessageEvent":'
            b'{"type":"text_delta","delta":"plain answer\\n"}}'
        )
        renderer.flush()
        output = mirror.getvalue().decode("utf-8")
        self.assertIn("\x1b[2mdeep thoughts\x1b[0m", output)
        self.assertNotIn("\x1b[2mplain answer\x1b[0m", output)

    def test_message_update_lines_are_dropped_from_raw(self) -> None:
        from i18nlib.pi_tmux import _is_message_update_line

        self.assertTrue(
            _is_message_update_line(
                b'{"type":"message_update","assistantMessageEvent":{"delta":"x"}}'
            )
        )
        self.assertFalse(
            _is_message_update_line(
                b'{"type":"message_end","message":{"role":"assistant"}}'
            )
        )
        self.assertFalse(_is_message_update_line(b"plain line"))


if __name__ == "__main__":
    unittest.main()
