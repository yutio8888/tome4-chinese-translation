"""Toolchain tests: lint."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import EMPTY_POLICY
import contextlib
from dataclasses import replace
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch
from i18nlib.config import load_manifest
from i18nlib.cli import main as cli_main
from i18nlib.errors import ConfigurationError, ValidationError
from i18nlib.lint import TERMINOLOGY_FIELDS, extract_format_tokens, lint_documents, load_policy
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.runtime import LuaRuntime


class FormatTests(unittest.TestCase):
    def test_printf_tokenizer_skips_literal_percent(self) -> None:
        tokens = extract_format_tokens("%0.2f damage, %d turns, %d%% chance")
        self.assertEqual([token.raw for token in tokens], ["%0.2f", "%d", "%d"])


class LintCommandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()

    @classmethod
    def _manifest(cls, root: Path, *, copy_fragment: str | None) -> object:
        component = replace(
            cls.base_manifest.components[0],
            id="fixture",
            translation="canonical.lua",
            copy_fragment=copy_fragment,
        )
        return replace(cls.base_manifest, root=root, components=(component,))

    @staticmethod
    def _document(
        logical_path: str, records: tuple[dict[str, object], ...]
    ) -> LocaleDocument:
        return LocaleDocument(
            logical_path=logical_path,
            sha256="0" * 64,
            records=records,
        )

    @contextlib.contextmanager
    def _patched_command(
        self, manifest: object, loader: Mock, run_directory: Path
    ) -> object:
        runtime = Mock(spec=LuaRuntime)
        with (
            patch("i18nlib.cli._inject_public_dlc_env"),
            patch("i18nlib.cli_lint._manifest", return_value=manifest),
            patch("i18nlib.cli_lint.LuaRuntime", return_value=runtime),
            patch("i18nlib.cli_lint.LocaleLoader", return_value=loader),
            patch("i18nlib.cli_lint.load_policy", return_value=EMPTY_POLICY),
            patch("i18nlib.cli_lint.lint_terminology", return_value=([], {"rows": 0})),
            patch("i18nlib.cli_lint.create_run_directory", return_value=run_directory),
            patch("i18nlib.cli_lint.write_json") as write_json,
        ):
            yield runtime, write_json

    def test_lint_policy_schema_rejects_non_integer_versions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-lint-policy-") as temporary:
            root = Path(temporary)
            manifest = replace(self.base_manifest, root=root, policy="policy.json")
            path = root / "policy.json"
            for schema_version in (True, 1.0):
                with self.subTest(schema_version=schema_version):
                    path.write_text(
                        json.dumps(
                            {
                                "schema_version": schema_version,
                                "allowed_empty_targets": [],
                                "allowed_format_mismatches": [],
                                "allowed_runtime_collisions": [],
                            }
                        ),
                        encoding="utf-8",
                    )
                    with self.assertRaisesRegex(
                        ConfigurationError, "unsupported lint policy schema"
                    ):
                        load_policy(manifest)

    def test_empty_canonical_translation_fails_with_and_without_strict(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-lint-empty-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment=None)
            empty = self._document("canonical.lua", ())

            for strict in (False, True):
                with self.subTest(strict=strict):
                    loader = Mock(spec=LocaleLoader)
                    loader.load_path.return_value = empty
                    stdout = io.StringIO()
                    stderr = io.StringIO()
                    arguments = ["lint", "--json"]
                    if strict:
                        arguments.append("--strict")
                    with (
                        self._patched_command(manifest, loader, root / "report"),
                        contextlib.redirect_stdout(stdout),
                        contextlib.redirect_stderr(stderr),
                    ):
                        exit_code = cli_main(arguments)

                    report = json.loads(stdout.getvalue())
                    self.assertEqual(exit_code, ValidationError.exit_code)
                    self.assertFalse(report["ok"])
                    self.assertEqual(report["metrics"]["translations"], 0)
                    self.assertEqual(
                        report["metrics"]["copy_fragment_translations"], 0
                    )
                    self.assertEqual(
                        report["metrics"]["copy_fragment_components"], {}
                    )
                    self.assertEqual(
                        report["metrics"][
                            "copy_fragment_duplicate_runtime_keys"
                        ],
                        0,
                    )
                    self.assertEqual(report["metrics"]["errors"], 1)
                    self.assertEqual(
                        [issue["code"] for issue in report["issues"]],
                        ["empty-translation-file"],
                    )
                    self.assertEqual(
                        report["issues"][0]["message"],
                        "canonical translation file contains no t(...) records",
                    )
                    self.assertIn("lint failed with 1 errors", stderr.getvalue())

    def test_terminology_row_width_fails_strict_lint_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-lint-terminology-width-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment=None)
            terminology = root / manifest.terminology
            terminology.write_text(
                "\t".join(TERMINOLOGY_FIELDS)
                + "\n"
                + "Valid\t有效\tT.UI.LABEL\tui\t\texisting\tglobal\t\textra\n",
                encoding="utf-8",
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = self._document(
                "canonical.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Valid",
                        "target": "有效",
                        "source_tag": None,
                        "section": "fixture.lua",
                        "line": 1,
                    },
                ),
            )
            runtime = Mock(spec=LuaRuntime)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch("i18nlib.cli._inject_public_dlc_env"),
                patch("i18nlib.cli_lint._manifest", return_value=manifest),
                patch("i18nlib.cli_lint.LuaRuntime", return_value=runtime),
                patch("i18nlib.cli_lint.LocaleLoader", return_value=loader),
                patch("i18nlib.cli_lint.load_policy", return_value=EMPTY_POLICY),
                patch(
                    "i18nlib.cli_lint.create_run_directory",
                    return_value=root / "report",
                ),
                patch("i18nlib.cli_lint.write_json"),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["lint", "--json", "--strict"])

        report = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertFalse(report["ok"])
        self.assertEqual(
            [issue["code"] for issue in report["issues"]],
            ["terminology-row-width"],
        )
        self.assertEqual(report["metrics"]["terminology"]["rows"], 1)
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_empty_synthetic_document_remains_valid_by_default(self) -> None:
        empty = self._document("generated:fixture.lua", ())

        issues, metrics = lint_documents([("fixture", empty)], EMPTY_POLICY)

        self.assertEqual(issues, [])
        self.assertEqual(metrics["translations"], 0)
        self.assertEqual(metrics["errors"], 0)

    def test_editorial_and_runtime_collisions_use_complete_semantics(self) -> None:
        document = self._document(
            "canonical.lua",
            (
                {
                    "kind": "translation",
                    "source": "Args %s %s",
                    "target": "参数 %s %s",
                    "source_tag": None,
                    "section": "fixture.lua",
                    "args_order": [1, 2],
                    "special": None,
                },
                {
                    "kind": "translation",
                    "source": "Args %s %s",
                    "target": "参数 %s %s",
                    "source_tag": None,
                    "section": "fixture.lua",
                    "args_order": [2, 1],
                    "special": None,
                },
                {
                    "kind": "translation",
                    "source": "Special",
                    "target": "特殊",
                    "source_tag": None,
                    "section": "fixture.lua",
                    "args_order": None,
                    "special": {"nested": [True]},
                },
                {
                    "kind": "translation",
                    "source": "Special",
                    "target": "特殊",
                    "source_tag": None,
                    "section": "fixture.lua",
                    "args_order": None,
                    "special": {"nested": [1]},
                },
            ),
        )

        issues, metrics = lint_documents([("fixture", document)], EMPTY_POLICY)

        self.assertEqual(
            [issue.code for issue in issues],
            [
                "editorial-collision",
                "editorial-collision",
                "runtime-collision",
                "runtime-collision",
            ],
        )
        self.assertEqual(metrics["duplicate_runtime_keys"], 2)
        self.assertTrue(
            all("target/args_order/special" in issue.message for issue in issues)
        )

    def test_noncanonical_semantics_fail_before_lint_report_write(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-lint-semantics-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment=None)
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = self._document(
                "canonical.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Invalid",
                        "target": "无效",
                        "source_tag": None,
                        "section": "fixture.lua",
                        "special": {"value": float("inf")},
                    },
                ),
            )
            sentinel = root / "old-lint.json"
            sentinel.write_bytes(b"old report\n")
            with (
                self._patched_command(manifest, loader, root / "report") as patched,
                contextlib.redirect_stderr(io.StringIO()),
            ):
                _, write_json = patched
                exit_code = cli_main(["lint", "--json"])

            self.assertEqual(exit_code, ValidationError.exit_code)
            self.assertEqual(sentinel.read_bytes(), b"old report\n")
            write_json.assert_not_called()

    def test_definition_only_copy_fragment_is_valid_and_has_zero_metrics(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-lint-copy-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment="fragment.lua")
            fragment = self._document(
                "fragment.lua",
                ({"kind": "definition", "name": "fixture"},),
            )
            canonical = self._document(
                "canonical.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Fixture",
                        "target": "测试",
                        "source_tag": None,
                        "section": "fixture.lua",
                    },
                ),
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (fragment, canonical)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                self._patched_command(manifest, loader, root / "report"),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["lint", "--strict", "--json"])

            report = json.loads(stdout.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertTrue(report["ok"])
        self.assertEqual(report["metrics"]["translations"], 1)
        self.assertEqual(report["metrics"]["components"], {"fixture": 1})
        self.assertEqual(report["metrics"]["copy_fragment_translations"], 0)
        self.assertEqual(
            report["metrics"]["copy_fragment_components"], {"fixture": 0}
        )
        self.assertEqual(
            report["metrics"]["copy_fragment_duplicate_runtime_keys"], 0
        )
        self.assertEqual(report["issues"], [])
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(root / "fragment.lua", logical_path="fragment.lua"),
                call(root / "canonical.lua", logical_path="canonical.lua"),
            ],
        )

    def test_invalid_copy_translation_fails_lint(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-lint-copy-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment="fragment.lua")
            fragment = self._document(
                "fragment.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Invalid copy target",
                        "target": "",
                        "source_tag": None,
                        "section": "copy.lua",
                        "line": 7,
                    },
                ),
            )
            canonical = self._document(
                "canonical.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Canonical",
                        "target": "规范",
                        "source_tag": None,
                        "section": "canonical.lua",
                    },
                ),
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (fragment, canonical)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                self._patched_command(manifest, loader, root / "report"),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["lint", "--json"])

            report = json.loads(stdout.getvalue())

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertFalse(report["ok"])
        self.assertEqual(report["metrics"]["translations"], 1)
        self.assertEqual(report["metrics"]["components"], {"fixture": 1})
        self.assertEqual(report["metrics"]["copy_fragment_translations"], 1)
        self.assertEqual(
            report["metrics"]["copy_fragment_components"], {"fixture": 1}
        )
        self.assertEqual(report["metrics"]["errors"], 1)
        self.assertEqual(report["metrics"]["warnings"], 0)
        self.assertEqual(
            [issue["code"] for issue in report["issues"]], ["empty-target"]
        )
        self.assertEqual(report["issues"][0]["logical_path"], "fragment.lua")
        self.assertIn("lint failed with 1 errors", stderr.getvalue())

    def test_copy_warning_is_blocking_in_strict_mode(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-lint-copy-warning-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment="fragment.lua")
            fragment = self._document(
                "fragment.lua",
                (
                    {
                        "kind": "translation",
                        "source": "#RED#Warning#LAST#",
                        "target": "警告",
                        "source_tag": None,
                        "section": "copy.lua",
                    },
                ),
            )
            canonical = self._document(
                "canonical.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Canonical",
                        "target": "规范",
                        "source_tag": None,
                        "section": "canonical.lua",
                    },
                ),
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (fragment, canonical)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                self._patched_command(manifest, loader, root / "report"),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["lint", "--strict", "--json"])

            report = json.loads(stdout.getvalue())

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertFalse(report["ok"])
        self.assertEqual(report["metrics"]["errors"], 0)
        self.assertEqual(report["metrics"]["warnings"], 1)
        self.assertEqual(
            [issue["code"] for issue in report["issues"]],
            ["markup-difference"],
        )
        self.assertIn(
            "lint failed with 0 errors and 1 warnings", stderr.getvalue()
        )

    def test_valid_copy_translation_uses_separate_metrics_without_cross_collision(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-lint-copy-valid-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment="fragment.lua")
            fragment = self._document(
                "fragment.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Shared runtime key",
                        "target": "片段译文",
                        "source_tag": None,
                        "section": "copy.lua",
                    },
                ),
            )
            canonical = self._document(
                "canonical.lua",
                (
                    {
                        "kind": "translation",
                        "source": "Shared runtime key",
                        "target": "规范译文",
                        "source_tag": None,
                        "section": "canonical.lua",
                    },
                ),
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (fragment, canonical)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                self._patched_command(manifest, loader, root / "report"),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["lint", "--strict", "--json"])

            report = json.loads(stdout.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertTrue(report["ok"])
        self.assertEqual(report["metrics"]["translations"], 1)
        self.assertEqual(report["metrics"]["components"], {"fixture": 1})
        self.assertEqual(report["metrics"]["duplicate_runtime_keys"], 0)
        self.assertEqual(report["metrics"]["copy_fragment_translations"], 1)
        self.assertEqual(
            report["metrics"]["copy_fragment_components"], {"fixture": 1}
        )
        self.assertEqual(
            report["metrics"]["copy_fragment_duplicate_runtime_keys"], 0
        )
        self.assertEqual(report["issues"], [])

    def test_copy_fragment_load_failure_fails_lint(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-lint-copy-failure-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, copy_fragment="fragment.lua")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = ValidationError(
                "fixture copy fragment load failure"
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                self._patched_command(manifest, loader, root / "report") as patched,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["lint", "--json"])

            _runtime, write_json = patched

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("fixture copy fragment load failure", stderr.getvalue())
        loader.load_path.assert_called_once_with(
            root / "fragment.lua", logical_path="fragment.lua"
        )
        write_json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
