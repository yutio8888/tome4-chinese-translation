"""Toolchain tests: terminology."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT
import csv
import tempfile
import unittest
from pathlib import Path
from i18nlib.lint import TERMINOLOGY_FIELDS, lint_terminology
from i18nlib.workset import _source_tag_matches


class TerminologyTests(unittest.TestCase):
    @staticmethod
    def _write_rows(
        path: Path, rows: tuple[tuple[str, ...], ...]
    ) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(TERMINOLOGY_FIELDS)
            writer.writerows(rows)

    def test_current_terminology_structure_is_valid(self) -> None:
        issues, metrics = lint_terminology(ROOT / "terminology")
        self.assertGreater(metrics["rows"], 0)
        self.assertFalse([issue for issue in issues if issue.severity == "error"])

    def test_row_width_errors_are_counted_and_excluded_from_contexts(self) -> None:
        valid = (
            "Shared source",
            "规范译文",
            "T.UI.LABEL",
            "ui",
            "",
            "existing",
            "global",
            "",
        )
        malformed = (
            "Shared source",
            "另一译文",
            "T.UI.LABEL",
            "ui",
            "",
            "existing",
            "global",
            "",
        )
        cases = (
            ("one-extra", malformed + ("extra",), 9),
            ("multiple-extra", malformed + ("extra", "more"), 10),
        )
        for label, invalid_row, actual_width in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-terminology-row-width-"
            ) as temporary:
                path = Path(temporary) / "terminology.tsv"
                self._write_rows(path, (valid, invalid_row))

                issues, metrics = lint_terminology(path)

            errors = [issue for issue in issues if issue.severity == "error"]
            self.assertEqual([issue.code for issue in errors], ["terminology-row-width"])
            self.assertEqual(errors[0].line, 3)
            self.assertIn(
                f"expected {len(TERMINOLOGY_FIELDS)} TSV fields, got {actual_width}",
                errors[0].message,
            )
            self.assertEqual(metrics["rows"], 2)
            self.assertEqual(metrics["contexts"], 1)

    def test_missing_trailing_notes_uses_canonical_compatibility(self) -> None:
        row_without_notes = (
            "Legacy empty notes",
            "旧式空备注",
            "T.UI.LABEL",
            "ui",
            "",
            "existing",
            "global",
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-terminology-legacy-notes-"
        ) as temporary:
            path = Path(temporary) / "terminology.tsv"
            self._write_rows(path, (row_without_notes,))

            issues, metrics = lint_terminology(path)

        self.assertEqual(metrics["rows"], 1)
        self.assertEqual(metrics["contexts"], 1)
        self.assertFalse([issue for issue in issues if issue.severity == "error"])

    def test_missing_middle_column_still_fails_semantic_validation(self) -> None:
        complete_row = (
            "Shifted fields",
            "错位字段",
            "T.UI.LABEL",
            "ui",
            "",
            "existing",
            "global",
            "",
        )
        row_without_source_tag = complete_row[:4] + complete_row[5:]
        with tempfile.TemporaryDirectory(
            prefix="tome4-terminology-missing-middle-"
        ) as temporary:
            path = Path(temporary) / "terminology.tsv"
            self._write_rows(path, (row_without_source_tag,))

            issues, metrics = lint_terminology(path)

        error_codes = {
            issue.code for issue in issues if issue.severity == "error"
        }
        self.assertEqual(metrics["rows"], 1)
        self.assertIn("terminology-empty-field", error_codes)
        self.assertIn("terminology-status", error_codes)

    def test_quoted_tab_and_empty_optional_fields_are_valid(self) -> None:
        row = (
            "Quoted\ttab",
            "带制表符",
            "T.TECH.INTERNAL",
            "tech",
            "",
            "preferred",
            "global",
            "",
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-terminology-quoted-tab-"
        ) as temporary:
            path = Path(temporary) / "terminology.tsv"
            self._write_rows(path, (row,))
            self.assertIn('"Quoted\ttab"', path.read_text(encoding="utf-8"))

            issues, metrics = lint_terminology(path)

        self.assertEqual(metrics["rows"], 1)
        self.assertFalse([issue for issue in issues if issue.severity == "error"])

    def test_malformed_quoted_record_is_a_controlled_read_error(self) -> None:
        valid = (
            "Valid",
            "有效",
            "T.UI.LABEL",
            "ui",
            "",
            "existing",
            "global",
            "",
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-terminology-malformed-quote-"
        ) as temporary:
            path = Path(temporary) / "terminology.tsv"
            self._write_rows(path, (valid,))
            with path.open("a", encoding="utf-8", newline="") as handle:
                handle.write('"unterminated\tfield\n')

            issues, metrics = lint_terminology(path)

        errors = [issue for issue in issues if issue.severity == "error"]
        self.assertEqual([issue.code for issue in errors], ["terminology-read"])
        self.assertEqual(errors[0].line, 3)
        self.assertIn("unexpected end of data", errors[0].message)
        self.assertEqual(metrics["rows"], 1)

    def test_unknown_status_and_scope_are_errors(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-terminology-enums-"
        ) as temporary:
            path = Path(temporary) / "terminology.tsv"
            path.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                "Bad status\t坏状态\tT.UI.LABEL\tui\t_t\tallowed\tglobal\tfixture\n"
                "Bad scope\t坏范围\tT.UI.LABEL\tui\t_t\texisting\tofficial-dlc\tfixture\n",
                encoding="utf-8",
            )
            issues, _ = lint_terminology(path)

        errors = {issue.code for issue in issues if issue.severity == "error"}
        self.assertIn("terminology-status", errors)
        self.assertIn("terminology-scope", errors)

    def test_empty_source_tag_and_notes_are_valid(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-terminology-empty-source-tag-"
        ) as temporary:
            path = Path(temporary) / "terminology.tsv"
            path.write_text(
                "source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n"
                "Empty tag\t空标签\tT.TECH.INTERNAL\ttech\t\tpreferred\tglobal\t\n",
                encoding="utf-8",
            )
            issues, metrics = lint_terminology(path)

        self.assertEqual(metrics["rows"], 1)
        self.assertFalse([issue for issue in issues if issue.severity == "error"])
        self.assertTrue(_source_tag_matches("", ""))
        self.assertFalse(_source_tag_matches("", None))
        self.assertTrue(_source_tag_matches("nil", None))
        self.assertFalse(_source_tag_matches("nil", ""))

    def test_other_terminology_fields_remain_required(self) -> None:
        fields = (
            "source",
            "target",
            "category",
            "domain",
            "source_tag",
            "status",
            "scope",
            "notes",
        )
        valid = {
            "source": "Required",
            "target": "必填",
            "category": "T.UI.LABEL",
            "domain": "ui",
            "source_tag": "",
            "status": "existing",
            "scope": "addon",
            "notes": "",
        }
        for empty_field in (
            "source",
            "target",
            "category",
            "domain",
            "status",
            "scope",
        ):
            with self.subTest(field=empty_field), tempfile.TemporaryDirectory(
                prefix="tome4-terminology-required-"
            ) as temporary:
                row = {**valid, empty_field: ""}
                path = Path(temporary) / "terminology.tsv"
                path.write_text(
                    "\t".join(fields)
                    + "\n"
                    + "\t".join(row[field] for field in fields)
                    + "\n",
                    encoding="utf-8",
                )
                issues, _ = lint_terminology(path)

            empty_issues = [
                issue
                for issue in issues
                if issue.code == "terminology-empty-field"
            ]
            self.assertTrue(empty_issues)
            self.assertIn(repr(empty_field), empty_issues[0].message)


if __name__ == "__main__":
    unittest.main()
