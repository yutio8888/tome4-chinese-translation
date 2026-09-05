"""Toolchain tests: dynamic audit."""

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
import audit_dynamic
from i18nlib.config import load_manifest
from i18nlib.errors import ValidationError
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.workset import _scope_matches


class DynamicAuditTests(unittest.TestCase):
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
    def _document(logical_path: str, source: str, target: str) -> LocaleDocument:
        return LocaleDocument(
            logical_path=logical_path,
            sha256="0" * 64,
            records=(
                {
                    "kind": "translation",
                    "source": source,
                    "target": target,
                    "source_tag": None,
                },
            ),
        )

    @staticmethod
    def _write_terminology(path: Path, rows: str = "") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\t".join(audit_dynamic.TERMINOLOGY_FIELDS) + "\n" + rows,
            encoding="utf-8",
        )

    def _assert_terminology_preflight_failure(
        self, manifest: object, expected: str
    ) -> str:
        output = manifest.root / ".artifacts/i18n/terminology-audit"
        legacy_root = manifest.root / "legacy-module-root"
        with (
            patch.object(audit_dynamic, "ROOT", legacy_root),
            patch.object(audit_dynamic, "OUT", legacy_root / "report"),
            patch.object(audit_dynamic, "LuaRuntime") as runtime,
            patch.object(audit_dynamic, "LocaleLoader") as loader_class,
            patch.object(audit_dynamic, "load_translation_documents") as load_docs,
            self.assertRaises(ValidationError) as caught,
        ):
            audit_dynamic.run_dynamic_audit(manifest=manifest)

        message = str(caught.exception)
        self.assertIn(str(manifest.root / manifest.terminology), message)
        self.assertIn(expected, message)
        self.assertFalse(output.exists())
        self.assertFalse(legacy_root.exists())
        runtime.assert_not_called()
        loader_class.assert_not_called()
        load_docs.assert_not_called()
        return message

    def test_manifest_defaults_and_explicit_overrides(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-manifest-inputs-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(
                self._manifest(root, (("fixture", "fixture.lua"),)),
                terminology="config/custom-terminology.tsv",
            )
            translation = root / "fixture.lua"
            translation.write_text("-- fixture\n", encoding="utf-8")
            self._write_terminology(
                root / manifest.terminology,
                "Arcane\t奥术\tT.GAME.DAMAGE\tcombat\tnil\tpreferred\tglobal\tfixture\n",
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = self._document(
                "fixture.lua", "Arcane", "奥术"
            )
            output = root / ".artifacts/i18n/terminology-audit"
            legacy_root = root / "legacy-module-root"

            with (
                patch.object(audit_dynamic, "ROOT", legacy_root),
                patch.object(audit_dynamic, "OUT", legacy_root / "report"),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                report = audit_dynamic.run_dynamic_audit(
                    manifest=manifest, loader=loader
                )

            self.assertTrue((output / "audit_dynamic.json").is_file())
            self.assertTrue((output / "audit_dynamic.md").is_file())
            self.assertFalse(legacy_root.exists())
            self.assertEqual(report["entries"], 1)
            self.assertEqual(report["s2_1"]["unused_count"], 0)

            (root / manifest.terminology).write_text(
                "wrong\theader\n", encoding="utf-8"
            )
            terminology = root / "override" / "terms.tsv"
            self._write_terminology(terminology)
            override_output = root / "override-report"

            with contextlib.redirect_stdout(io.StringIO()):
                audit_dynamic.run_dynamic_audit(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=override_output,
                )

            self.assertTrue((override_output / "audit_dynamic.json").is_file())

        self.assertEqual(loader.load_path.call_count, 2)
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(translation, logical_path="fixture.lua"),
                call(translation, logical_path="fixture.lua"),
            ],
        )

    def test_invalid_terminology_fails_before_all_downstream_io(self) -> None:
        cases = (
            ("missing", None, "line 1", "No such file or directory"),
            ("invalid-utf8", b"\xff", "line 1", "invalid start byte"),
            ("wrong-header", "target\tsource\n", "line 1", "expected fields"),
            (
                "empty-required",
                "\t".join(audit_dynamic.TERMINOLOGY_FIELDS)
                + "\n\t奥术\tT.GAME.DAMAGE\tcombat\tnil\tpreferred\tglobal\tfixture\n",
                "line 2",
                "empty required fields: source",
            ),
        )
        for name, content, line, detail in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix=f"tome4-dynamic-audit-invalid-terminology-{name}-"
            ) as temporary:
                root = Path(temporary)
                manifest = replace(
                    self._manifest(root, (("fixture", "fixture.lua"),)),
                    terminology=f"inputs/{name}.tsv",
                )
                path = root / manifest.terminology
                if content is not None:
                    path.parent.mkdir(parents=True)
                    if isinstance(content, bytes):
                        path.write_bytes(content)
                    else:
                        path.write_text(content, encoding="utf-8")
                message = self._assert_terminology_preflight_failure(
                    manifest, line
                )
                self.assertIn(detail, message)

    def test_main_controls_invalid_terminology_exit_without_downstream_io(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-main-invalid-terminology-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("fixture", "fixture.lua"),))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch.object(audit_dynamic.signal, "alarm") as alarm,
                patch.object(audit_dynamic, "LuaRuntime") as runtime,
                patch.object(audit_dynamic, "LocaleLoader") as loader_class,
                patch.object(
                    audit_dynamic, "load_translation_documents"
                ) as load_docs,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = audit_dynamic.main(manifest=manifest)

            self.assertFalse(
                (root / ".artifacts/i18n/terminology-audit").exists()
            )

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("dynamic audit failed:", stderr.getvalue())
        self.assertIn(str(root / manifest.terminology), stderr.getvalue())
        self.assertIn("line 1", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        runtime.assert_not_called()
        loader_class.assert_not_called()
        load_docs.assert_not_called()
        self.assertEqual(alarm.call_args_list, [call(300), call(0)])

    def _run_s2_3_fixture(
        self,
        records: tuple[tuple[str, str | None, str], ...],
        terminology_rows: tuple[tuple[str, str], ...] = (),
    ) -> tuple[dict[str, object], dict[str, object], str]:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-s2-3-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("fixture", "fixture.lua"),))
            translation = root / "fixture.lua"
            translation.write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = LocaleDocument(
                logical_path="fixture.lua",
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
            terminology = root / "terminology" / "fixture.tsv"
            terminology.parent.mkdir(parents=True, exist_ok=True)
            terminology.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                + "".join(
                    f"{source}\t{target}\tT.FIXTURE\tfixture\tnil\tallowed\tglobal\tfixture\n"
                    for source, target in terminology_rows
                ),
                encoding="utf-8",
            )
            output = root / "report"

            with contextlib.redirect_stdout(io.StringIO()):
                report = audit_dynamic.run_dynamic_audit(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=output,
                )

            json_report = json.loads(
                (output / "audit_dynamic.json").read_text(encoding="utf-8")
            )
            markdown = (output / "audit_dynamic.md").read_text(encoding="utf-8")

        return report, json_report, markdown

    def test_cli_missing_translation_returns_nonzero_without_report(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-missing-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("missing", "missing.lua"),))
            self._write_terminology(root / manifest.terminology)
            loader = Mock(spec=LocaleLoader)
            output = root / "report"
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(audit_dynamic.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = audit_dynamic.main(
                    manifest=manifest, loader=loader, output_dir=output
                )

            self.assertFalse(output.exists())

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("dynamic audit failed", stderr.getvalue())
        self.assertIn("1 declared translation component failed", stderr.getvalue())
        self.assertIn("missing: missing translation file", stderr.getvalue())
        self.assertEqual(
            [alarm_call.args for alarm_call in alarm.call_args_list],
            [(300,), (0,)],
        )
        loader.load_path.assert_not_called()

    def test_controlled_loader_error_aborts_without_report(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-loader-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("broken", "broken.lua"),))
            self._write_terminology(root / manifest.terminology)
            translation = root / "broken.lua"
            translation.write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = ValidationError("fixture load failure")
            output = root / "report"

            with self.assertRaises(audit_dynamic.DynamicAuditLoadError) as caught:
                audit_dynamic.run_dynamic_audit(
                    manifest=manifest, loader=loader, output_dir=output
                )

            self.assertFalse(output.exists())

        self.assertIn("broken: load failed", str(caught.exception))
        self.assertIn("ValidationError", str(caught.exception))
        self.assertIn("fixture load failure", str(caught.exception))
        loader.load_path.assert_called_once_with(
            translation, logical_path="broken.lua"
        )

    def test_multiple_translation_failures_are_reported_together(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-multiple-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(
                root,
                (
                    ("missing", "missing.lua"),
                    ("broken-one", "broken-one.lua"),
                    ("broken-two", "broken-two.lua"),
                ),
            )
            self._write_terminology(root / manifest.terminology)
            (root / "broken-one.lua").write_text("-- fixture\n", encoding="utf-8")
            (root / "broken-two.lua").write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                ValidationError("fixture read failure"),
                ValidationError("fixture parse failure"),
            )
            output = root / "report"

            with self.assertRaises(audit_dynamic.DynamicAuditLoadError) as caught:
                audit_dynamic.run_dynamic_audit(
                    manifest=manifest, loader=loader, output_dir=output
                )

            self.assertFalse(output.exists())

        self.assertEqual(
            [failure.component for failure in caught.exception.failures],
            ["missing", "broken-one", "broken-two"],
        )
        self.assertIn(
            "3 declared translation components failed", str(caught.exception)
        )
        self.assertIn(
            "broken-one: load failed (ValidationError: fixture read failure)",
            str(caught.exception),
        )
        self.assertIn(
            "broken-two: load failed (ValidationError: fixture parse failure)",
            str(caught.exception),
        )
        self.assertEqual(loader.load_path.call_count, 2)

    def test_unexpected_loader_errors_propagate_without_report(self) -> None:
        for error in (
            RuntimeError("fixture runtime failure"),
            AssertionError("fixture assertion failure"),
        ):
            with self.subTest(error_type=type(error).__name__):
                with tempfile.TemporaryDirectory(
                    prefix="tome4-dynamic-audit-unexpected-"
                ) as temporary:
                    root = Path(temporary)
                    manifest = self._manifest(root, (("broken", "broken.lua"),))
                    self._write_terminology(root / manifest.terminology)
                    translation = root / "broken.lua"
                    translation.write_text("-- fixture\n", encoding="utf-8")
                    loader = Mock(spec=LocaleLoader)
                    loader.load_path.side_effect = error
                    output = root / "report"

                    with self.assertRaises(type(error)) as caught:
                        audit_dynamic.run_dynamic_audit(
                            manifest=manifest, loader=loader, output_dir=output
                        )

                    self.assertIs(caught.exception, error)
                    self.assertFalse(output.exists())
                    loader.load_path.assert_called_once_with(
                        translation, logical_path="broken.lua"
                    )

    def test_invalid_utf8_is_reported_as_component_load_failure(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-encoding-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("broken", "broken.lua"),))
            self._write_terminology(root / manifest.terminology)
            (root / "broken.lua").write_bytes(b"\xff")
            loader = LocaleLoader.__new__(LocaleLoader)
            output = root / "report"

            with self.assertRaises(audit_dynamic.DynamicAuditLoadError) as caught:
                audit_dynamic.run_dynamic_audit(
                    manifest=manifest, loader=loader, output_dir=output
                )

            self.assertFalse(output.exists())

        self.assertIn("broken: load failed (ValidationError", str(caught.exception))
        self.assertIn("locale is not UTF-8: broken.lua", str(caught.exception))

    def test_import_does_not_arm_alarm(self) -> None:
        with patch.object(audit_dynamic.signal, "alarm") as alarm:
            reloaded = importlib.reload(audit_dynamic)

        self.assertIs(reloaded, audit_dynamic)
        alarm.assert_not_called()

    def test_complete_load_writes_original_reports(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-complete-"
        ) as temporary:
            root = Path(temporary)
            translations = (("alpha", "alpha.lua"), ("beta", "beta.lua"))
            manifest = self._manifest(root, translations)
            for _, relative_path in translations:
                (root / relative_path).write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                self._document("alpha.lua", "Arcane", "奥术"),
                self._document("beta.lua", "Other", "其他"),
            )
            terminology = root / "terminology" / "fixture.tsv"
            terminology.parent.mkdir(parents=True, exist_ok=True)
            terminology.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                "Arcane\t奥术\tT.GAME.DAMAGE\tcombat\tnil\tpreferred\tglobal\tfixture\n",
                encoding="utf-8",
            )
            output = root / "report"
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch.object(audit_dynamic.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = audit_dynamic.main(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=output,
                )

            report = json.loads(
                (output / "audit_dynamic.json").read_text(encoding="utf-8")
            )
            markdown = (output / "audit_dynamic.md").read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertIn("dynamic audit done: 2 entries", stdout.getvalue())
        self.assertEqual(report["entries"], 2)
        self.assertEqual(report["components"], ["alpha", "beta"])
        self.assertEqual(report["s2_1"]["unused_count"], 0)
        self.assertEqual(report["s2_1"]["mismatch_count"], 0)
        self.assertTrue(markdown.startswith("# 术语表动态校对审计报告\n"))
        self.assertEqual(
            [alarm_call.args for alarm_call in alarm.call_args_list],
            [(300,), (0,)],
        )
        self.assertEqual(loader.load_path.call_count, 2)

    def test_dlc_scope_uses_workset_component_group(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-dlc-scope-"
        ) as temporary:
            root = Path(temporary)
            translations = (
                ("items-vault", "items-vault.lua"),
                ("possessors", "possessors.lua"),
            )
            manifest = self._manifest(root, translations)
            for _, relative_path in translations:
                (root / relative_path).write_text("-- fixture\n", encoding="utf-8")
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                self._document("items-vault.lua", "Vault term", "宝库术语"),
                self._document("possessors.lua", "Possessor term", "附身术语"),
            )
            terminology = root / "terminology" / "fixture.tsv"
            terminology.parent.mkdir(parents=True, exist_ok=True)
            terminology.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                "Vault term\t宝库术语\tT.GAME.ENTITY\titems\tnil\tpreferred\tdlc\tfixture\n"
                "Possessor term\t附身术语\tT.GAME.ENTITY\tcreatures\tnil\tpreferred\tdlc\tfixture\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stdout(io.StringIO()):
                report = audit_dynamic.run_dynamic_audit(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=root / "report",
                )

        self.assertEqual(report["s2_1"]["unused_count"], 0)
        for component in ("items-vault", "possessors"):
            self.assertTrue(_scope_matches("dlc", component))

    def test_s2_1_distinguishes_nil_and_empty_source_tags(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-source-tags-"
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
                        "source": "Needs nil",
                        "target": "nil target",
                        "source_tag": "",
                    },
                    {
                        "kind": "translation",
                        "source": "Needs empty",
                        "target": "empty target",
                        "source_tag": None,
                    },
                ),
            )
            terminology = root / "terminology" / "fixture.tsv"
            terminology.parent.mkdir(parents=True, exist_ok=True)
            terminology.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                "Needs nil\tnil target\tT.TECH.INTERNAL\ttech\tnil\tpreferred\tglobal\tfixture\n"
                "Needs empty\tempty target\tT.TECH.INTERNAL\ttech\t\tpreferred\tglobal\tfixture\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stdout(io.StringIO()):
                report = audit_dynamic.run_dynamic_audit(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=root / "report",
                )

        self.assertEqual(report["s2_1"]["unused_count"], 2)
        self.assertEqual(report["s2_1"]["mismatch_count"], 0)

    def test_s2_1_only_filters_candidates_from_matching_source(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-source-index-"
        ) as temporary:
            root = Path(temporary)
            translations = (("tome", "tome.lua"), ("cults", "cults.lua"))
            manifest = self._manifest(root, translations)
            for _, relative_path in translations:
                (root / relative_path).write_text("-- fixture\n", encoding="utf-8")

            unrelated = tuple(
                {
                    "kind": "translation",
                    "source": f"Unrelated source {index}",
                    "target": "无关译文",
                    "source_tag": None,
                }
                for index in range(1000)
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.side_effect = (
                LocaleDocument(
                    logical_path="tome.lua",
                    sha256="0" * 64,
                    records=unrelated
                    + (
                        {
                            "kind": "translation",
                            "source": "Indexed",
                            "target": "前缀规范术语后缀",
                            "source_tag": None,
                        },
                    ),
                ),
                LocaleDocument(
                    logical_path="cults.lua",
                    sha256="0" * 64,
                    records=(
                        {
                            "kind": "translation",
                            "source": "Indexed",
                            "target": "空标签译文",
                            "source_tag": "",
                        },
                    ),
                ),
            )
            terminology = root / "terminology" / "fixture.tsv"
            terminology.parent.mkdir(parents=True, exist_ok=True)
            terminology.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                "Missing first\t未使用甲\tT.FIXTURE\tfixture\tnil\tpreferred\tglobal\tfixture\n"
                "Indexed\t规范术语\tT.FIXTURE\tfixture\tnil\tpreferred\tcore\tfixture\n"
                "Indexed\t期望甲译\tT.FIXTURE\tfixture\t\tpreferred\tdlc\tfixture\n"
                "Missing second\t未使用乙\tT.FIXTURE\tfixture\tnil\tpreferred\tglobal\tfixture\n"
                "Indexed\t期望乙译\tT.FIXTURE\tfixture\t\tpreferred\tdlc\tfixture\n",
                encoding="utf-8",
            )
            scope_impl = audit_dynamic._scope_matches
            source_tag_impl = audit_dynamic._source_tag_matches

            with (
                patch.object(
                    audit_dynamic, "_scope_matches", wraps=scope_impl
                ) as scope_matches,
                patch.object(
                    audit_dynamic, "_source_tag_matches", wraps=source_tag_impl
                ) as source_tag_matches,
                # r2 inventory 有自己的调用序列与独立测试，不影响 S2.1 语义断言
                patch.object(audit_dynamic, "run_terminology_inventory") as inventory,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                report = audit_dynamic.run_dynamic_audit(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=root / "report",
                )

        self.assertEqual(report["entries"], 1002)
        self.assertEqual(scope_matches.call_count, 6)
        self.assertEqual(
            scope_matches.call_args_list,
            [
                call("core", "tome"),
                call("core", "cults"),
                call("dlc", "tome"),
                call("dlc", "cults"),
                call("dlc", "tome"),
                call("dlc", "cults"),
            ],
        )
        self.assertEqual(
            source_tag_matches.call_args_list,
            [call("nil", None), call("", ""), call("", "")],
        )
        self.assertEqual(
            [item["source"] for item in report["s2_1"]["unused"]],
            ["Missing first", "Missing second"],
        )
        self.assertEqual(
            [item["target"] for item in report["s2_1"]["mismatch"]],
            ["期望甲译", "期望乙译"],
        )
        self.assertEqual(
            [item["found_targets"] for item in report["s2_1"]["mismatch"]],
            [["空标签译文"], ["空标签译文"]],
        )

    def test_s2_2_separates_and_stably_sorts_tags_and_targets(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-dynamic-audit-candidate-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, (("candidate", "candidate.lua"),))
            translation = root / "candidate.lua"
            translation.write_text("-- fixture\n", encoding="utf-8")
            source = "Repeated candidate"
            records = tuple(
                {
                    "kind": "translation",
                    "source": source,
                    "target": target,
                    "source_tag": source_tag,
                }
                for source_tag, target in (
                    ("tag-z", "target-e"),
                    (None, "target-b"),
                    ("", "target-c"),
                    ("tag-a", "target-a"),
                    ("tag-b", "target-d"),
                    ("tag-y", "target-f"),
                )
                * 3
            )
            loader = Mock(spec=LocaleLoader)
            loader.load_path.return_value = LocaleDocument(
                logical_path="candidate.lua",
                sha256="0" * 64,
                records=records,
            )
            terminology = root / "terminology" / "fixture.tsv"
            terminology.parent.mkdir(parents=True, exist_ok=True)
            terminology.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n",
                encoding="utf-8",
            )
            output = root / "report"

            with contextlib.redirect_stdout(io.StringIO()):
                report = audit_dynamic.run_dynamic_audit(
                    manifest=manifest,
                    loader=loader,
                    terminology_path=terminology,
                    output_dir=output,
                )

            json_text = (output / "audit_dynamic.json").read_text(
                encoding="utf-8"
            )
            json_report = json.loads(json_text)
            markdown = (output / "audit_dynamic.md").read_text(encoding="utf-8")

        self.assertEqual(report["s2_2"]["count"], 1)
        candidate = report["s2_2"]["items"][0]
        self.assertEqual(candidate["source"], source)
        self.assertEqual(candidate["count"], 18)
        self.assertEqual(candidate["tags"], [None, "", "tag-a", "tag-b"])
        self.assertEqual(candidate["targets"], ["target-a", "target-b", "target-c"])
        self.assertEqual(json_report, report)
        self.assertIsNone(json_report["s2_2"]["items"][0]["tags"][0])
        self.assertNotIn("target-a", candidate["tags"])
        self.assertNotIn("tag-a", candidate["targets"])
        self.assertEqual(report["s2_1"]["unused_count"], 0)
        self.assertEqual(report["s2_1"]["mismatch_count"], 0)
        self.assertEqual(
            [variant["target"] for variant in report["s2_3"]["items"][0]["variants"]],
            ["target-a", "target-b", "target-c", "target-d", "target-e", "target-f"],
        )
        self.assertIn(
            "- (18) `Repeated candidate` → target-a / target-b / target-c",
            markdown,
        )

    def test_s2_3_reports_partially_covered_source_and_missing_target(self) -> None:
        report, _, _ = self._run_s2_3_fixture(
            (
                ("Partial", None, "target-recorded"),
                ("Partial", "context", "target-unrecorded"),
            ),
            (("Partial", "target-recorded"),),
        )

        self.assertEqual(report["s2_3"]["count"], 1)
        item = report["s2_3"]["items"][0]
        self.assertEqual(item["source"], "Partial")
        self.assertEqual(item["terminology_targets"], ["target-recorded"])
        self.assertEqual(item["unrecorded_targets"], ["target-unrecorded"])

    def test_s2_3_skips_fully_covered_multi_target_source(self) -> None:
        report, _, _ = self._run_s2_3_fixture(
            (
                ("Complete", None, "target-a"),
                ("Complete", "context", "target-b"),
            ),
            (("Complete", "target-a"), ("Complete", "target-b")),
        )

        self.assertEqual(report["s2_3"], {"count": 0, "items": []})

    def test_s2_3_reports_source_absent_from_terminology(self) -> None:
        report, _, _ = self._run_s2_3_fixture(
            (
                ("Unrecorded", None, "target-b"),
                ("Unrecorded", "context", "target-a"),
            )
        )

        self.assertEqual(report["s2_3"]["count"], 1)
        item = report["s2_3"]["items"][0]
        self.assertEqual(item["source"], "Unrecorded")
        self.assertEqual(item["terminology_targets"], [])
        self.assertEqual(item["unrecorded_targets"], ["target-a", "target-b"])

    def test_s2_3_preserves_and_stably_sorts_distinct_tags(self) -> None:
        report, json_report, markdown = self._run_s2_3_fixture(
            (
                ("Tagged", "None", "target-a"),
                ("Tagged", None, "target-a"),
                ("Tagged", "tag-a", "target-a"),
                ("Tagged", "", "target-a"),
                ("Tagged", None, "target-b"),
            )
        )

        variant = report["s2_3"]["items"][0]["variants"][0]
        self.assertEqual(variant["tags"], [None, "", "None", "tag-a"])
        self.assertEqual(json_report, report)
        self.assertIsNone(
            json_report["s2_3"]["items"][0]["variants"][0]["tags"][0]
        )
        self.assertIn('`target-a`[<nil>,"",None,tag-a]', markdown)


if __name__ == "__main__":
    unittest.main()
