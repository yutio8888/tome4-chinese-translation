"""Toolchain tests: runtime keys."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
import contextlib
from dataclasses import replace
import importlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch
import classify_runtime_keys
import scan_runtime_collisions
from i18nlib.config import load_manifest
from i18nlib.errors import ValidationError
from i18nlib.locale_model import LocaleDocument, LocaleLoader


class RuntimeCollisionScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()

    @classmethod
    def _manifest(
        cls, root: Path, translations: tuple[tuple[str, str], ...]
    ) -> object:
        components = tuple(
            replace(
                cls.base_manifest.components[index],
                id=component_id,
                translation=translation,
            )
            for index, (component_id, translation) in enumerate(translations)
        )
        return replace(cls.base_manifest, root=root, components=components)

    @staticmethod
    def _document(
        logical_path: str,
        records: tuple[tuple[str, str | None, str], ...],
    ) -> LocaleDocument:
        return LocaleDocument(
            logical_path=logical_path,
            sha256="0" * 64,
            records=tuple(
                {
                    "kind": "translation",
                    "source": source,
                    "source_tag": source_tag,
                    "target": target,
                }
                for source, source_tag, target in records
            ),
        )

    def test_import_does_not_arm_alarm(self) -> None:
        with patch.object(scan_runtime_collisions.signal, "alarm") as alarm:
            reloaded = importlib.reload(scan_runtime_collisions)

        self.assertIs(reloaded, scan_runtime_collisions)
        alarm.assert_not_called()

    def test_input_failures_are_aggregated_without_overwriting_reports(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-collision-failure-"
        ) as temporary:
            root = Path(temporary)
            translations = (
                ("missing", "missing.lua"),
                ("directory", "directory.lua"),
                ("broken", "broken.lua"),
                ("valid", "valid.lua"),
            )
            manifest = self._manifest(root, translations)
            (root / "directory.lua").mkdir()
            (root / "broken.lua").write_text("-- fixture\n", encoding="utf-8")
            (root / "valid.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                ValidationError("fixture load failure"),
                self._document("valid.lua", (("Valid", None, "有效"),)),
            )
            output = root / "report"
            output.mkdir()
            json_path = output / "runtime-collisions.json"
            markdown_path = output / "runtime-collisions.md"
            json_path.write_bytes(b"old json\n")
            markdown_path.write_bytes(b"old markdown\n")
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(scan_runtime_collisions.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = scan_runtime_collisions.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            self.assertEqual(json_path.read_bytes(), b"old json\n")
            self.assertEqual(markdown_path.read_bytes(), b"old markdown\n")

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("runtime collision scan failed", stderr.getvalue())
        self.assertIn("3 declared translation components failed", stderr.getvalue())
        self.assertIn("missing: missing translation file", stderr.getvalue())
        self.assertIn(
            "directory: translation path is not a regular file",
            stderr.getvalue(),
        )
        self.assertIn(
            "broken: load failed (ValidationError: fixture load failure)",
            stderr.getvalue(),
        )
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(root / "broken.lua", logical_path="broken.lua"),
                call(root / "valid.lua", logical_path="valid.lua"),
            ],
        )
        self.assertEqual(
            [alarm_call.args for alarm_call in alarm.call_args_list],
            [(300,), (0,)],
        )

    def test_success_loads_each_translation_once_and_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-collision-success-"
        ) as temporary:
            root = Path(temporary)
            translations = (("alpha", "alpha.lua"), ("beta", "beta.lua"))
            manifest = self._manifest(root, translations)
            for _, relative_path in translations:
                (root / relative_path).write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                self._document("alpha.lua", (("Alpha", None, "甲"),)),
                self._document("beta.lua", (("Beta", None, "乙"),)),
            )
            output = root / "report"

            with (
                patch.object(scan_runtime_collisions.signal, "alarm") as alarm,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                exit_code = scan_runtime_collisions.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            report = json.loads(
                (output / "runtime-collisions.json").read_text(encoding="utf-8")
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["scanned_translations"], 2)
        self.assertEqual(report["collision_count"], 0)
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(root / "alpha.lua", logical_path="alpha.lua"),
                call(root / "beta.lua", logical_path="beta.lua"),
            ],
        )
        self.assertEqual(
            [alarm_call.args for alarm_call in alarm.call_args_list],
            [(300,), (0,)],
        )

    def test_none_and_string_tags_sort_and_collisions_return_nonzero(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-collision-tags-"
        ) as temporary:
            root = Path(temporary)
            translations = (("alpha", "alpha.lua"), ("beta", "beta.lua"))
            manifest = self._manifest(root, translations)
            for _, relative_path in translations:
                (root / relative_path).write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                self._document(
                    "alpha.lua",
                    (
                        ("Shared", "tag", "标签甲"),
                        ("Shared", None, "无标签甲"),
                    ),
                ),
                self._document(
                    "beta.lua",
                    (
                        ("Shared", None, "无标签乙"),
                        ("Shared", "tag", "标签乙"),
                    ),
                ),
            )
            output = root / "report"

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = scan_runtime_collisions.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            report = json.loads(
                (output / "runtime-collisions.json").read_text(encoding="utf-8")
            )
            markdown = (output / "runtime-collisions.md").read_text(
                encoding="utf-8"
            )

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["scanned_translations"], 4)
        self.assertEqual(report["collision_count"], 2)
        self.assertEqual(
            [item["source_tag"] for item in report["collisions"]],
            [None, "tag"],
        )
        self.assertLess(markdown.index("## [None]"), markdown.index("## [tag]"))
        self.assertEqual(loader.load_path.call_count, 2)

    def test_same_target_runtime_semantics_collide_and_invalid_values_preserve_reports(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-collision-semantics-"
        ) as temporary:
            root = Path(temporary)
            translations = (("alpha", "alpha.lua"), ("beta", "beta.lua"))
            manifest = self._manifest(root, translations)
            for _, relative_path in translations:
                (root / relative_path).write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                LocaleDocument(
                    logical_path="alpha.lua",
                    sha256="0" * 64,
                    records=(
                        {
                            "kind": "translation",
                            "source": "Args %s %s",
                            "target": "参数 %s %s",
                            "source_tag": None,
                            "args_order": [1, 2],
                            "special": None,
                        },
                        {
                            "kind": "translation",
                            "source": "Special",
                            "target": "特殊",
                            "source_tag": None,
                            "args_order": None,
                            "special": {"nested": [True]},
                        },
                    ),
                ),
                LocaleDocument(
                    logical_path="beta.lua",
                    sha256="0" * 64,
                    records=(
                        {
                            "kind": "translation",
                            "source": "Args %s %s",
                            "target": "参数 %s %s",
                            "source_tag": None,
                            "args_order": [2, 1],
                            "special": None,
                        },
                        {
                            "kind": "translation",
                            "source": "Special",
                            "target": "特殊",
                            "source_tag": None,
                            "args_order": None,
                            "special": {"nested": [1]},
                        },
                    ),
                ),
            )
            output = root / "report"

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = scan_runtime_collisions.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            report = json.loads(
                (output / "runtime-collisions.json").read_text(encoding="utf-8")
            )
            markdown = (output / "runtime-collisions.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(exit_code, 1)
            self.assertEqual(report["collision_count"], 2)
            for collision in report["collisions"]:
                self.assertEqual(collision["target_count"], 1)
                self.assertEqual(collision["semantic_value_count"], 2)
                self.assertEqual(len(collision["semantic_values"]), 2)
            self.assertIn('"args_order":[1,2]', markdown)
            self.assertIn('"args_order":[2,1]', markdown)
            self.assertIn('"nested":[true]', markdown)
            self.assertIn('"nested":[1]', markdown)

            json_path = output / "runtime-collisions.json"
            markdown_path = output / "runtime-collisions.md"
            json_path.write_bytes(b"old json\n")
            markdown_path.write_bytes(b"old markdown\n")
            loader.reset_mock()
            loader.load_path.side_effect = (
                LocaleDocument(
                    logical_path="alpha.lua",
                    sha256="0" * 64,
                    records=(
                        {
                            "kind": "translation",
                            "source": "Invalid",
                            "target": "无效",
                            "source_tag": None,
                            "special": {"value": float("nan")},
                        },
                    ),
                ),
                self._document("beta.lua", (("Valid", None, "有效"),)),
            )
            with contextlib.redirect_stderr(io.StringIO()):
                failed = scan_runtime_collisions.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )
            self.assertEqual(failed, ValidationError.exit_code)
            self.assertEqual(json_path.read_bytes(), b"old json\n")
            self.assertEqual(markdown_path.read_bytes(), b"old markdown\n")


class RuntimeKeyClassifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()

    @classmethod
    def _manifest(
        cls, root: Path, translations: tuple[tuple[str, str], ...]
    ) -> object:
        components = tuple(
            replace(
                cls.base_manifest.components[index],
                id=component_id,
                translation=translation,
            )
            for index, (component_id, translation) in enumerate(translations)
        )
        return replace(cls.base_manifest, root=root, components=components)

    @staticmethod
    def _document(
        logical_path: str,
        records: tuple[tuple[str, str | None, str, str], ...],
    ) -> LocaleDocument:
        return LocaleDocument(
            logical_path=logical_path,
            sha256="0" * 64,
            records=tuple(
                {
                    "kind": "translation",
                    "source": source,
                    "source_tag": source_tag,
                    "target": target,
                    "section": section,
                }
                for source, source_tag, target, section in records
            ),
        )

    def test_import_has_no_alarm_or_output_directory_side_effect(self) -> None:
        with (
            patch.object(classify_runtime_keys.signal, "alarm") as alarm,
            patch.object(classify_runtime_keys.Path, "mkdir") as mkdir,
        ):
            reloaded = importlib.reload(classify_runtime_keys)

        self.assertIs(reloaded, classify_runtime_keys)
        alarm.assert_not_called()
        mkdir.assert_not_called()

    def test_input_failures_are_aggregated_without_overwriting_reports(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-key-classifier-failure-"
        ) as temporary:
            root = Path(temporary)
            translations = (
                ("missing", "missing.lua"),
                ("directory", "directory.lua"),
                ("broken", "broken.lua"),
                ("valid", "valid.lua"),
            )
            manifest = self._manifest(root, translations)
            (root / "directory.lua").mkdir()
            (root / "broken.lua").write_text("-- fixture\n", encoding="utf-8")
            (root / "valid.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                ValidationError("fixture load failure"),
                self._document(
                    "valid.lua", (("Valid", None, "有效", "fixture/valid"),)
                ),
            )
            output = root / "report"
            output.mkdir()
            json_path = output / "classification.json"
            markdown_path = output / "classification.md"
            json_path.write_bytes(b"old json\n")
            markdown_path.write_bytes(b"old markdown\n")
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(classify_runtime_keys.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = classify_runtime_keys.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            self.assertEqual(json_path.read_bytes(), b"old json\n")
            self.assertEqual(markdown_path.read_bytes(), b"old markdown\n")

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("runtime-key classification failed", stderr.getvalue())
        self.assertIn("3 declared translation components failed", stderr.getvalue())
        self.assertIn("missing: missing translation file", stderr.getvalue())
        self.assertIn(
            "directory: translation path is not a regular file",
            stderr.getvalue(),
        )
        self.assertIn(
            "broken: load failed (ValidationError: fixture load failure)",
            stderr.getvalue(),
        )
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(root / "broken.lua", logical_path="broken.lua"),
                call(root / "valid.lua", logical_path="valid.lua"),
            ],
        )
        self.assertEqual(
            [alarm_call.args for alarm_call in alarm.call_args_list],
            [(300,), (0,)],
        )

    def test_three_buckets_and_none_tag_sort_are_reported(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-key-classifier-buckets-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("fixture", "fixture.lua"),))
            (root / "fixture.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = self._document(
                "fixture.lua",
                (
                    ("A sort", "tag", "甲", "fixture/data/a"),
                    ("A sort", "tag", "甲", "fixture/data/b"),
                    ("A sort", None, "乙", "fixture/data/c"),
                    ("A sort", None, "乙", "fixture/data/d"),
                    ("B only", None, "丙", "fixture/data/e"),
                    ("B only", None, "丙", "fixture/data/e"),
                    ("C mixed", None, "丁", "fixture/data/f"),
                    ("C mixed", None, "丁", "fixture/data/f"),
                    ("C mixed", None, "丁", "fixture/data/g"),
                ),
            )
            output = root / "report"

            with contextlib.redirect_stdout(io.StringIO()):
                report = classify_runtime_keys.run_runtime_key_classification(
                    manifest=manifest, loader=loader, output_dir=output
                )

            json_report = json.loads(
                (output / "classification.json").read_text(encoding="utf-8")
            )
            markdown = (output / "classification.md").read_text(
                encoding="utf-8"
            )

        self.assertEqual(report["total_duplicate_keys"], 4)
        self.assertEqual(report["bucket_counts"], {"A": 2, "B": 1, "C": 1})
        self.assertEqual(
            [item["source_tag"] for item in report["bucket_a_cross_file"]],
            [None, "tag"],
        )
        self.assertEqual(
            report["bucket_b_same_file_redundant"][0]["source"], "B only"
        )
        self.assertEqual(
            report["bucket_c_same_file_mixed"][0]["sections"],
            ["fixture/data/f", "fixture/data/g"],
        )
        self.assertEqual(json_report["bucket_counts"]["B"], 1)
        self.assertIn("## 桶 B：全部 occurrence 位于同一 section（1）", markdown)
        self.assertIn(
            "## 桶 C：跨 section 且至少一个 section 内重复（1）", markdown
        )
        loader.load_path.assert_called_once_with(
            root / "fixture.lua", logical_path="fixture.lua"
        )

    def test_directory_distribution_uses_sections_beyond_display_limit(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-key-classifier-sections-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("fixture", "fixture.lua"),))
            (root / "fixture.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = self._document(
                "fixture.lua",
                tuple(
                    (
                        "Many sections",
                        None,
                        "同译",
                        f"fixture/data/general/file-{index}.lua",
                    )
                    for index in range(7)
                ),
            )
            output = root / "report"

            with contextlib.redirect_stdout(io.StringIO()):
                report = classify_runtime_keys.run_runtime_key_classification(
                    manifest=manifest, loader=loader, output_dir=output
                )

        item = report["bucket_a_cross_file"][0]
        self.assertEqual(item["section_count"], 7)
        self.assertEqual(len(item["sections"]), 6)
        self.assertEqual(report["bucket_a_dir_distribution"], {"data/general": 7})

    def test_target_conflict_is_nonzero_and_preserves_old_reports(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-key-classifier-targets-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("fixture", "fixture.lua"),))
            (root / "fixture.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = self._document(
                "fixture.lua",
                (
                    ("Conflict", None, "译法甲", "fixture/data/a"),
                    ("Conflict", None, "译法乙", "fixture/data/b"),
                ),
            )
            output = root / "report"
            output.mkdir()
            json_path = output / "classification.json"
            markdown_path = output / "classification.md"
            json_path.write_bytes(b"old json\n")
            markdown_path.write_bytes(b"old markdown\n")
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(classify_runtime_keys.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = classify_runtime_keys.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            self.assertEqual(json_path.read_bytes(), b"old json\n")
            self.assertEqual(markdown_path.read_bytes(), b"old markdown\n")

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("resolve to multiple targets", stderr.getvalue())
        self.assertNotIn("全部同 target", stderr.getvalue())
        self.assertEqual(
            [alarm_call.args for alarm_call in alarm.call_args_list],
            [(300,), (0,)],
        )

    def test_same_target_semantic_conflicts_preserve_old_reports(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-runtime-key-classifier-semantics-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("fixture", "fixture.lua"),))
            (root / "fixture.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = LocaleDocument(
                logical_path="fixture.lua",
                sha256="0" * 64,
                records=(
                    {
                        "kind": "translation",
                        "source": "Args %s %s",
                        "target": "参数 %s %s",
                        "source_tag": None,
                        "section": "fixture/a.lua",
                        "args_order": [1, 2],
                        "special": None,
                    },
                    {
                        "kind": "translation",
                        "source": "Args %s %s",
                        "target": "参数 %s %s",
                        "source_tag": None,
                        "section": "fixture/b.lua",
                        "args_order": [2, 1],
                        "special": None,
                    },
                    {
                        "kind": "translation",
                        "source": "Special",
                        "target": "特殊",
                        "source_tag": None,
                        "section": "fixture/a.lua",
                        "args_order": None,
                        "special": {"nested": [False]},
                    },
                    {
                        "kind": "translation",
                        "source": "Special",
                        "target": "特殊",
                        "source_tag": None,
                        "section": "fixture/b.lua",
                        "args_order": None,
                        "special": {"nested": [0]},
                    },
                ),
            )
            output = root / "report"
            output.mkdir()
            json_path = output / "classification.json"
            markdown_path = output / "classification.md"
            json_path.write_bytes(b"old json\n")
            markdown_path.write_bytes(b"old markdown\n")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = classify_runtime_keys.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )

            self.assertEqual(exit_code, ValidationError.exit_code)
            self.assertEqual(json_path.read_bytes(), b"old json\n")
            self.assertEqual(markdown_path.read_bytes(), b"old markdown\n")
            self.assertIn("runtime semantic values", stderr.getvalue())
            self.assertIn('"args_order":[1,2]', stderr.getvalue())
            self.assertIn('"nested":[false]', stderr.getvalue())

            loader.reset_mock()
            loader.load_path.return_value = LocaleDocument(
                logical_path="fixture.lua",
                sha256="0" * 64,
                records=(
                    {
                        "kind": "translation",
                        "source": "Invalid",
                        "target": "无效",
                        "source_tag": None,
                        "section": "fixture/a.lua",
                        "special": {"value": float("nan")},
                    },
                ),
            )
            with contextlib.redirect_stderr(io.StringIO()):
                invalid_exit = classify_runtime_keys.main(
                    [], manifest=manifest, loader=loader, output_dir=output
                )
            self.assertEqual(invalid_exit, ValidationError.exit_code)
            self.assertEqual(json_path.read_bytes(), b"old json\n")
            self.assertEqual(markdown_path.read_bytes(), b"old markdown\n")


class SemanticSignatureTests(unittest.TestCase):
    def test_json_signature_is_recursive_type_sensitive_and_deterministic(
        self,
    ) -> None:
        from i18nlib.semantics import (
            json_value_signature,
            runtime_semantic_signature,
        )

        self.assertEqual(
            json_value_signature(
                {"z": [{"enabled": True, "count": 1}], "a": "汉字"}
            ),
            '{"a":"汉字","z":[{"count":1,"enabled":true}]}',
        )
        self.assertEqual(
            json_value_signature({"outer": {"b": [1, True], "a": "x"}}),
            json_value_signature({"outer": {"a": "x", "b": [1, True]}}),
        )
        for field, boolean_value, integer_value in (
            ("target", True, 1),
            ("args_order", [True], [1]),
            ("special", {"nested": [False]}, {"nested": [0]}),
        ):
            with self.subTest(field=field):
                base = {"target": "target", "args_order": None, "special": None}
                self.assertNotEqual(
                    runtime_semantic_signature(
                        {**base, field: boolean_value}
                    ),
                    runtime_semantic_signature(
                        {**base, field: integer_value}
                    ),
                )

    def test_json_signature_rejects_non_finite_and_unserializable_values(
        self,
    ) -> None:
        from i18nlib.semantics import json_value_signature

        for value in (float("nan"), {"unsupported": object()}):
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(ValidationError):
                    json_value_signature(value)


if __name__ == "__main__":
    unittest.main()
