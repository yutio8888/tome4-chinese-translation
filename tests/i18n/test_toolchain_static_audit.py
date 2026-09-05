"""Toolchain tests: static audit."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT, TOOLS
import contextlib
import importlib
import importlib.util
import io
import sys
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch
import annotate_domains
import audit_static
from audit_static_rules import normalize_typo_pairs


class StaticAuditTests(unittest.TestCase):
    columns = (
        "source",
        "target",
        "category",
        "domain",
        "source_tag",
        "status",
        "scope",
        "notes",
    )

    @classmethod
    def _row(cls, **overrides: str) -> dict[str, str]:
        row = {
            "source": "fixture source",
            "target": "测试译文",
            "category": "T.GAME.DAMAGE",
            "domain": "combat",
            "source_tag": "fixture tag",
            "status": "existing",
            "scope": "core",
            "notes": "fixture note",
        }
        row.update(overrides)
        return row

    @classmethod
    def _write_tsv(
        cls, path: Path, rows: list[dict[str, str]]
    ) -> None:
        lines = ["\t".join(cls.columns)]
        lines.extend(
            "\t".join(row.get(column, "") for column in cls.columns)
            for row in rows
        )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _run_fixture(
        self, rows: list[dict[str, str]]
    ) -> tuple[int, dict[str, object], str, str, list[object]]:
        with tempfile.TemporaryDirectory(prefix="static-audit-") as temporary:
            directory = Path(temporary)
            tsv_path = directory / "terminology.tsv"
            output_dir = directory / "reports"
            self._write_tsv(tsv_path, rows)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch.object(audit_static.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = audit_static.main(
                    tsv_path=tsv_path, output_dir=output_dir
                )
            json_path = output_dir / "audit_static.json"
            markdown_path = output_dir / "audit_static.md"
            self.assertTrue(json_path.is_file())
            self.assertTrue(markdown_path.is_file())
            report = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")
            return (
                exit_code,
                report,
                markdown,
                stderr.getvalue(),
                alarm.call_args_list,
            )

    def test_module_import_has_no_audit_side_effects(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "_audit_static_import_probe", TOOLS / "audit_static.py"
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        with (
            patch("signal.alarm") as alarm,
            patch.object(Path, "mkdir") as mkdir,
            patch.object(Path, "open") as path_open,
            patch.object(Path, "read_text") as read_text,
            patch.object(Path, "write_text") as write_text,
        ):
            spec.loader.exec_module(module)

        alarm.assert_not_called()
        mkdir.assert_not_called()
        path_open.assert_not_called()
        read_text.assert_not_called()
        write_text.assert_not_called()

    def test_typo_rules_exclude_short_terms_and_self_mappings(self) -> None:
        self.assertEqual(
            normalize_typo_pairs(
                [("予", "预"), ("吩咐", "吩咐"), ("渲泄", "宣泄")]
            ),
            [("渲泄", "宣泄")],
        )

    def test_typo_rules_deduplicate_exact_pairs_stably(self) -> None:
        self.assertEqual(
            normalize_typo_pairs(
                [
                    ("渲泄", "宣泄"),
                    ("既使", "即使"),
                    ("渲泄", "宣泄"),
                    ("按装", "安装"),
                    ("既使", "即使"),
                ]
            ),
            [("渲泄", "宣泄"), ("既使", "即使"), ("按装", "安装")],
        )

    def test_typo_rules_retain_same_bad_with_different_corrections(self) -> None:
        self.assertEqual(
            normalize_typo_pairs(
                [("同词", "建议甲"), ("同词", "建议乙"), ("同词", "建议甲")]
            ),
            [("同词", "建议甲"), ("同词", "建议乙")],
        )

    def test_advisory_findings_do_not_fail_the_audit(self) -> None:
        rows = [
            self._row(source="shared source", target="译文甲"),
            self._row(source="shared source", target="译文乙"),
            self._row(
                source="lowercase name",
                target="名字",
                category="T.PN.PERSON",
            ),
        ]
        exit_code, report, markdown, stderr, alarm_calls = self._run_fixture(
            rows
        )

        self.assertEqual(exit_code, 0)
        self.assertIs(report["ok"], True)
        self.assertEqual(report["blocking_count"], 0)
        self.assertEqual(report["advisory_count"], 2)
        self.assertEqual(stderr, "")
        self.assertTrue(markdown.startswith("# 术语表静态校对审计报告\n"))
        self.assertEqual(alarm_calls, [call(120), call(0)])

    def test_each_blocking_finding_fails_after_reports_are_written(self) -> None:
        cases = (
            (
                "typo",
                self._row(target="按装"),
                "S1.2_typos",
                "count",
            ),
            (
                "punctuation",
                self._row(target="中文,文本"),
                "S1.3_punctuation",
                "count",
            ),
            (
                "missing preferred notes",
                self._row(status="preferred", notes=""),
                "S1.5_fields",
                "missing_notes_preferred",
            ),
            (
                "bad scope",
                self._row(scope="invalid"),
                "S1.5_fields",
                "bad_scope",
            ),
            (
                "bad status",
                self._row(status="invalid"),
                "S1.5_fields",
                "bad_status",
            ),
        )
        for label, row, section, count_key in cases:
            with self.subTest(finding=label):
                exit_code, report, _, stderr, alarm_calls = self._run_fixture(
                    [row]
                )

                self.assertEqual(exit_code, 1)
                self.assertIs(report["ok"], False)
                self.assertEqual(report["blocking_count"], 1)
                self.assertEqual(report["advisory_count"], 0)
                if section == "S1.5_fields":
                    self.assertEqual(
                        report["sections"][section]["counts"][count_key], 1
                    )
                else:
                    self.assertEqual(
                        report["sections"][section][count_key], 1
                    )
                self.assertEqual(stderr, "")
                self.assertEqual(alarm_calls, [call(120), call(0)])

    def test_input_and_output_failures_are_clean(self) -> None:
        with tempfile.TemporaryDirectory(prefix="static-audit-io-") as temporary:
            directory = Path(temporary)
            valid_tsv = directory / "terminology.tsv"
            self._write_tsv(valid_tsv, [self._row()])
            output_file = directory / "not-a-directory"
            output_file.write_text("fixture", encoding="utf-8")
            cases = (
                (directory / "missing.tsv", directory / "missing-report"),
                (valid_tsv, output_file),
            )
            for tsv_path, output_dir in cases:
                with self.subTest(tsv_path=tsv_path, output_dir=output_dir):
                    stderr = io.StringIO()
                    with (
                        patch.object(audit_static.signal, "alarm") as alarm,
                        contextlib.redirect_stderr(stderr),
                    ):
                        exit_code = audit_static.main(
                            tsv_path=tsv_path, output_dir=output_dir
                        )

                    self.assertNotEqual(exit_code, 0)
                    self.assertIn("static audit failed:", stderr.getvalue())
                    self.assertNotIn("Traceback", stderr.getvalue())
                    self.assertEqual(
                        alarm.call_args_list, [call(120), call(0)]
                    )

    def test_static_audit_generates_reports_with_normalized_findings(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "audit_static.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=130,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        self.assertIn("static audit done:", completed.stdout)

        report_dir = ROOT / ".artifacts" / "i18n" / "terminology-audit"
        json_path = report_dir / "audit_static.json"
        markdown_path = report_dir / "audit_static.md"
        self.assertTrue(json_path.is_file())
        self.assertTrue(markdown_path.is_file())

        report = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertGreater(report["total_rows"], 0)
        self.assertIs(report["ok"], True)
        self.assertEqual(report["blocking_count"], 0)
        self.assertGreater(report["advisory_count"], 0)
        typo_items = report["sections"]["S1.2_typos"]["items"]
        finding_keys = [
            (item["line"], item["bad"], item["good"]) for item in typo_items
        ]
        self.assertEqual(len(finding_keys), len(set(finding_keys)))
        self.assertTrue(all(item["bad"] != item["good"] for item in typo_items))
        self.assertTrue(
            markdown_path.read_text(encoding="utf-8").startswith(
                "# 术语表静态校对审计报告\n"
            )
        )


class DomainAnnotationTests(unittest.TestCase):
    columns = (
        "source",
        "target",
        "category",
        "domain",
        "source_tag",
        "status",
        "scope",
        "notes",
    )

    @classmethod
    def _row(cls, **overrides: str) -> dict[str, str]:
        row = {
            "source": "fixture entity",
            "target": "测试实体",
            "category": "T.GAME.ENTITY",
            "domain": "items",
            "source_tag": "entity name",
            "status": "existing",
            "scope": "global",
            "notes": "fixture note",
        }
        row.update(overrides)
        return row

    @classmethod
    def _write_tsv(
        cls, path: Path, rows: list[dict[str, str]]
    ) -> None:
        lines = ["\t".join(cls.columns)]
        lines.extend(
            "\t".join(row.get(column, "") for column in cls.columns)
            for row in rows
        )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _run_fixture(
        self, rows: list[dict[str, str]]
    ) -> tuple[int, dict[str, object], str, str, list[object]]:
        with tempfile.TemporaryDirectory(
            prefix="domain-annotation-"
        ) as temporary:
            directory = Path(temporary)
            tsv_path = directory / "terminology.tsv"
            output_dir = directory / "reports"
            self._write_tsv(tsv_path, rows)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                patch.object(annotate_domains.signal, "alarm") as alarm,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = annotate_domains.main(
                    tsv_path=tsv_path, output_dir=output_dir
                )
            json_path = output_dir / "domain_annotation.json"
            self.assertTrue(json_path.is_file())
            report = json.loads(json_path.read_text(encoding="utf-8"))
            return (
                exit_code,
                report,
                stdout.getvalue(),
                stderr.getvalue(),
                alarm.call_args_list,
            )

    def test_module_import_has_no_annotation_side_effects(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "_annotate_domains_import_probe", TOOLS / "annotate_domains.py"
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        with (
            patch("signal.alarm") as alarm,
            patch.object(Path, "mkdir") as mkdir,
            patch.object(Path, "open") as path_open,
            patch.object(Path, "read_text") as read_text,
            patch.object(Path, "write_text") as write_text,
        ):
            spec.loader.exec_module(module)

        alarm.assert_not_called()
        mkdir.assert_not_called()
        path_open.assert_not_called()
        read_text.assert_not_called()
        write_text.assert_not_called()

    def test_new_entity_sources_map_to_their_declared_domains(self) -> None:
        expected = {
            "voratun": "items",
            "iron": "items",
            "steel": "items",
            "open door": "items",
            "trap": "items",
            "cleansing ": "items",
            "cleansing": "items",
            "cleanse": "items",
            "grounding ": "items",
            "insulating ": "items",
            "corrupted": "creatures",
            "steamtech": "creatures",
            "multi-hued": "creatures",
            "next level": "places",
            "previous level": "places",
            "way to the next level": "places",
            "way to the previous level": "places",
        }
        rows = [
            self._row(source=source, domain=domain)
            for source, domain in expected.items()
        ]

        exit_code, report, _, stderr, alarm_calls = self._run_fixture(rows)

        actual = {row["source"]: row["domain"] for row in report["rows"]}
        self.assertEqual(exit_code, 0)
        self.assertEqual(actual, expected)
        self.assertEqual(report["unmapped_count"], 0)
        self.assertEqual(report["declared_domain_mismatch_count"], 0)
        self.assertEqual(sum(report["counts"].values()), 17)
        self.assertIs(report["ok"], True)
        self.assertEqual(stderr, "")
        self.assertEqual(alarm_calls, [call(60), call(0)])

    def test_unknown_entity_fails_after_report_is_written(self) -> None:
        exit_code, report, _, stderr, alarm_calls = self._run_fixture(
            [self._row(source="unknown fixture entity")]
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["unmapped_count"], 1)
        self.assertEqual(report["blocking_count"], 1)
        self.assertEqual(
            report["unmapped"][0]["source"], "unknown fixture entity"
        )
        self.assertIsNone(report["rows"][0]["domain"])
        self.assertIs(report["ok"], False)
        self.assertEqual(stderr, "")
        self.assertEqual(alarm_calls, [call(60), call(0)])

    def test_declared_domain_mismatch_is_advisory_only(self) -> None:
        exit_code, report, _, stderr, alarm_calls = self._run_fixture(
            [
                self._row(
                    source="physical",
                    category="T.GAME.DAMAGE",
                    domain="items",
                    source_tag="damage type",
                )
            ]
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["unmapped_count"], 0)
        self.assertEqual(report["declared_domain_mismatch_count"], 1)
        self.assertEqual(report["advisory_count"], 1)
        mismatch = report["declared_domain_mismatches"][0]
        self.assertEqual(mismatch["declared_domain"], "items")
        self.assertEqual(mismatch["domain"], "combat")
        self.assertIs(report["ok"], True)
        self.assertEqual(stderr, "")
        self.assertEqual(alarm_calls, [call(60), call(0)])

    def test_input_output_and_tsv_failures_are_clean(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="domain-annotation-io-"
        ) as temporary:
            directory = Path(temporary)
            valid_tsv = directory / "terminology.tsv"
            malformed_tsv = directory / "malformed.tsv"
            output_file = directory / "not-a-directory"
            self._write_tsv(valid_tsv, [self._row(source="iron")])
            malformed_tsv.write_text(
                "source\ttarget\nfixture\t测试\n", encoding="utf-8"
            )
            output_file.write_text("fixture", encoding="utf-8")
            cases = (
                (directory / "missing.tsv", directory / "missing-report"),
                (valid_tsv, output_file),
                (malformed_tsv, directory / "malformed-report"),
            )
            for tsv_path, output_dir in cases:
                with self.subTest(tsv_path=tsv_path, output_dir=output_dir):
                    stdout = io.StringIO()
                    stderr = io.StringIO()
                    with (
                        patch.object(
                            annotate_domains.signal, "alarm"
                        ) as alarm,
                        contextlib.redirect_stdout(stdout),
                        contextlib.redirect_stderr(stderr),
                    ):
                        exit_code = annotate_domains.main(
                            tsv_path=tsv_path, output_dir=output_dir
                        )

                    self.assertEqual(exit_code, 2)
                    self.assertIn(
                        "domain annotation failed:", stderr.getvalue()
                    )
                    self.assertNotIn("Traceback", stderr.getvalue())
                    self.assertNotIn("Traceback", stdout.getvalue())
                    self.assertEqual(alarm.call_args_list, [call(60), call(0)])

    def test_real_terminology_is_fully_mapped(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "annotate_domains.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=70,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        self.assertIn("annotation written:", completed.stdout)
        report_path = (
            ROOT
            / ".artifacts"
            / "i18n"
            / "terminology-audit"
            / "domain_annotation.json"
        )
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(len(report["domains"]), 11)
        self.assertEqual(len(report["rows"]), 720)
        self.assertEqual(sum(report["counts"].values()), 720)
        self.assertEqual(report["unmapped_count"], 0)
        self.assertEqual(report["declared_domain_mismatch_count"], 6)
        self.assertIs(report["ok"], True)


if __name__ == "__main__":
    unittest.main()
