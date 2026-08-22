from __future__ import annotations

import contextlib
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
FIXTURES = ROOT / "tests" / "i18n" / "fixtures" / "provenance"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import contextual_anchor_preflight as preflight
import paseo_contract_check


class ContextualAnchorPreflightTests(unittest.TestCase):
    scope_path = FIXTURES / "scope_bad.json"

    @staticmethod
    def _payload(name: str) -> dict[str, object]:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def _run_fixture(self, payload_name: str) -> preflight.PreflightResult:
        return preflight.run_preflight(
            self.scope_path, FIXTURES / payload_name, workspace_root=ROOT
        )

    def test_cults_b3_wrong_chapter_regression_fails(self) -> None:
        result = self._run_fixture("envelope_bad_wrong_chapter.json")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")
        self.assertEqual(result.exit_code, 1)

    def test_cults_b3_declared_chapter_passes(self) -> None:
        result = self._run_fixture("envelope_good.json")
        self.assertEqual(result.status, "PREFLIGHT_VERIFIED")
        self.assertEqual(result.exit_code, 0)

    def test_cults_b3_undeclared_later_chapter_fails(self) -> None:
        result = self._run_fixture("envelope_bad_undeclared_later_chapter.json")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")
        self.assertEqual(result.exit_code, 1)

    def test_lua_long_bracket_sources_decode_with_delimiters_and_newline_rule(self) -> None:
        text = (
            'section "story"\n'
            't([[\nfirst\n]], "", "_t")\n'
            't([=[\r\nsecond]=], "", "_t")\n'
            't([==[third]==], "", "_t")\n'
        )
        sections, calls = preflight._scan_lua(text)
        self.assertEqual([section.path for section in sections], ["story"])
        self.assertEqual([call.source for call in calls], ["first\n", "second", "third"])

    def test_quoted_string_physical_line_escapes_normalize_lf_and_crlf(self) -> None:
        text = (
            't("line\\' + "\n" + 'feed", "", "_t")\n'
            't("crlf\\' + "\r\n" + 'next", "", "_t")\n'
        )
        _, calls = preflight._scan_lua(text)
        self.assertEqual([call.source for call in calls], ["line\nfeed", "crlf\nnext"])

    def test_member_calls_are_not_global_translation_or_section_calls(self) -> None:
        text = (
            'obj.section("not a section")\n'
            'obj . -- still a member call\n'
            '  t(computed)\n'
            'section "story"\n'
            'obj.t("not a translation")\n'
            'obj:t("not a method translation")\n'
            't("real source", "", "_t")\n'
        )
        sections, calls = preflight._scan_lua(text)
        self.assertEqual([section.path for section in sections], ["story"])
        self.assertEqual([call.source for call in calls], ["real source"])

    def test_body_chapter_mention_without_title_delimiter_does_not_bound_window(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            (root / "story.lua").write_text(
                'section "story"\n'
                't("Book [Book 9, Chapter 1] - One", "", "_t")\n'
                't("body mentions [Book 9, Chapter 2] without the title delimiter", "", "_t")\n'
                't("still inside", "", "_t")\n'
                't("Book [Book 9, Chapter 2] - Two", "", "_t")\n',
                encoding="utf-8",
            )
            self._write_valid_pair(scope, payload)
            value = self._payload("envelope_good.json")
            value["translation_snapshot"] = [
                {"revision_key": "r1", "source": "still inside", "target": "仍在章节内"}
            ]
            self._write(payload, value)
            self.assertFalse(
                preflight._is_chapter_title(
                    "body mentions [Book 9, Chapter 2] without the title delimiter"
                )
            )
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_VERIFIED")

    def _workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        temporary = tempfile.TemporaryDirectory(prefix="contextual-anchor-")
        root = Path(temporary.name)
        story = root / "story.lua"
        story.write_text(
            'section "story"\n'
            't("Book [Book 9, Chapter 1] - One", "", "_t")\n'
            't("inside", "", "_t")\n'
            't("Book [Book 9, Chapter 2] - Two", "", "_t")\n'
            't("outside", "", "_t")\n',
            encoding="utf-8",
        )
        scope = root / "SCOPE.json"
        payload = root / "PAYLOAD.json"
        return temporary, root, scope, payload

    @staticmethod
    def _scope(*, file: str = "story.lua", section: str = "story", titles: list[str] | None = None) -> dict[str, object]:
        return {
            "schema_version": 1,
            "allowed_files": [file],
            "anchor_scopes": [
                {
                    "file": file,
                    "section_path": section,
                    "ordered_titles": (
                        titles
                        if titles is not None
                        else ["Book [Book 9, Chapter 1] - One"]
                    ),
                }
            ],
        }

    @staticmethod
    def _write(path: Path, value: object) -> None:
        path.write_text(json.dumps(value), encoding="utf-8")

    def _write_valid_pair(self, scope: Path, payload: Path, scope_value: dict[str, object] | None = None) -> None:
        self._write(scope, scope_value or self._scope())
        self._write(payload, self._payload("envelope_good.json") | {
            "translation_snapshot": [{"revision_key": "r1", "source": "inside", "target": "译文"}]
        })

    def test_scope_schema_rejects_duplicates_and_missing_anchor(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            cases = []
            duplicate_file = self._scope()
            duplicate_file["allowed_files"] = ["story.lua", "story.lua"]
            cases.append(duplicate_file)
            duplicate_scope = self._scope()
            duplicate_scope["anchor_scopes"] = copy.deepcopy(duplicate_scope["anchor_scopes"]) * 2
            cases.append(duplicate_scope)
            duplicate_title = self._scope(titles=["Book [Book 9, Chapter 1] - One"] * 2)
            cases.append(duplicate_title)
            wrong_version_type = self._scope()
            wrong_version_type["schema_version"] = True
            cases.append(wrong_version_type)
            missing_anchor = self._scope(titles=["Book [Book 9, Chapter 99] - Missing"])
            cases.append(missing_anchor)
            for value in cases:
                with self.subTest(scope=value):
                    self._write_valid_pair(scope, payload, value)
                    result = preflight.run_preflight(scope, payload, workspace_root=root)
                    self.assertIn(result.status, {"INPUT_ERROR", "PREFLIGHT_FAILED"})

    def test_empty_scope_collections_are_exact_input_errors(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            for field in ("allowed_files", "anchor_scopes"):
                with self.subTest(field=field):
                    value = self._scope()
                    value[field] = []
                    self._write_valid_pair(scope, payload, value)
                    result = preflight.run_preflight(scope, payload, workspace_root=root)
                    self.assertEqual(result.status, "INPUT_ERROR")
                    self.assertEqual(result.exit_code, 2)

            value = self._scope(titles=[])
            self._write_valid_pair(scope, payload, value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")
            self.assertEqual(result.exit_code, 2)

    def test_anchor_scope_file_omitted_from_allowed_files_is_exact_input_error(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            other = root / "other.lua"
            other.write_text(
                'section "other"\n'
                't("other source", "", "_t")\n',
                encoding="utf-8",
            )
            value = self._scope()
            value["anchor_scopes"] = [
                {
                    "file": "other.lua",
                    "section_path": "other",
                    "ordered_titles": ["Book [Book 9, Chapter 1] - One"],
                }
            ]
            self._write_valid_pair(scope, payload, value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")
            self.assertEqual(result.exit_code, 2)

    def test_payload_source_in_allowed_undeclared_file_fails_preflight(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            other = root / "other.lua"
            other.write_text(
                'section "other"\n'
                't("only in other", "", "_t")\n',
                encoding="utf-8",
            )
            value = self._scope()
            value["allowed_files"] = ["story.lua", "other.lua"]
            self._write(scope, value)
            payload_value = self._payload("envelope_good.json") | {
                "translation_snapshot": [
                    {"revision_key": "r1", "source": "only in other", "target": "译文"}
                ]
            }
            self._write(payload, payload_value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_FAILED")
            self.assertEqual(result.exit_code, 1)

    def test_duplicate_actual_chapter_titles_fail_preflight(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            self._write(scope, self._scope())
            (root / "story.lua").write_text(
                'section "story"\n'
                't("Book [Book 9, Chapter 1] - One", "", "_t")\n'
                't("Book [Book 9, Chapter 1] - One", "", "_t")\n'
                't("inside", "", "_t")\n',
                encoding="utf-8",
            )
            payload_value = self._payload("envelope_good.json")
            payload_value["translation_snapshot"] = [
                {
                    "revision_key": "r1",
                    "source": "Book [Book 9, Chapter 1] - One",
                    "target": "译文",
                }
            ]
            self._write(payload, payload_value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_FAILED")
            self.assertEqual(result.exit_code, 1)

    def test_section_mismatch_and_ordering_fail_closed(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            for value in (
                self._scope(section="not-story"),
                self._scope(
                    titles=[
                        "Book [Book 9, Chapter 2] - Two",
                        "Book [Book 9, Chapter 1] - One",
                    ]
                ),
            ):
                with self.subTest(scope=value):
                    self._write_valid_pair(scope, payload, value)
                    result = preflight.run_preflight(scope, payload, workspace_root=root)
                    self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_unsafe_and_nonordinary_paths_are_input_errors(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            for raw_path in ("../story.lua", str((root / "story.lua").resolve()), "missing.lua"):
                with self.subTest(path=raw_path):
                    self._write_valid_pair(scope, payload, self._scope(file=raw_path))
                    result = preflight.run_preflight(scope, payload, workspace_root=root)
                    self.assertEqual(result.status, "INPUT_ERROR")
            link = root / "story-link.lua"
            link.symlink_to(root / "story.lua")
            self._write_valid_pair(scope, payload, self._scope(file="story-link.lua"))
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")
            self._write_valid_pair(scope, payload, self._scope(file="."))
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")

    def test_payload_shape_and_dynamic_lua_are_input_errors(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            self._write_valid_pair(scope, payload)
            invalid = self._payload("envelope_good.json")
            invalid["extra"] = "no"
            self._write(payload, invalid)
            self.assertEqual(
                preflight.run_preflight(scope, payload, workspace_root=root).status,
                "INPUT_ERROR",
            )
            self._write_valid_pair(scope, payload)
            invalid = self._payload("envelope_good.json")
            invalid["translation_snapshot"] = [{"revision_key": "r1", "source": 3, "target": "x"}]
            self._write(payload, invalid)
            self.assertEqual(
                preflight.run_preflight(scope, payload, workspace_root=root).status,
                "INPUT_ERROR",
            )
            (root / "story.lua").write_text(
                'section "story"\nt(title, "", "_t")\n', encoding="utf-8"
            )
            self._write_valid_pair(scope, payload)
            self.assertEqual(
                preflight.run_preflight(scope, payload, workspace_root=root).status,
                "INPUT_ERROR",
            )

    def test_real_t_call_requires_complete_literal_first_argument_and_balance(self) -> None:
        cases = (
            't("x" .. suffix, "", "_t")',
            't("x" suffix, "", "_t")',
            't("x", "unterminated, "_t")',
            't("x", {"nested"}, "_t"',
        )
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(preflight.InputError):
                    preflight._scan_lua(text)

        text = (
            't("before") .. t("Book [Book 9, Chapter 1] - Found", -- comment\n'
            '  "", [[_t]])\n'
            't("after", {key = [=[a ) b]=]}, "", "_t")\n'
            'value ... t("after ellipsis")\n'
        )
        _, calls = preflight._scan_lua(text)
        self.assertEqual(
            [call.source for call in calls],
            [
                "before",
                "Book [Book 9, Chapter 1] - Found",
                "after",
                "after ellipsis",
            ],
        )

    def test_decimal_escapes_aggregate_utf8_bytes_and_use_ascii_digits(self) -> None:
        _, calls = preflight._scan_lua(
            't("\\226\\128\\156", "", "_t")\n'
            't("\\195\\169", "", "_t")\n'
            't("é", "", "_t")\n'
        )
        self.assertEqual([call.source for call in calls], ["“", "é", "é"])
        for text in (
            't("\\255", "", "_t")',
            't("\\١٢٣", "", "_t")',
        ):
            with self.subTest(text=text):
                with self.assertRaises(preflight.InputError):
                    preflight._scan_lua(text)

    def test_nul_and_value_error_paths_are_structured_input_errors(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            self._write_valid_pair(scope, payload, self._scope(file="story\x00.lua"))
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")
            self.assertEqual(result.exit_code, 2)
            self._write_valid_pair(scope, payload)
            result = preflight.run_preflight(str(scope) + "\x00", payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")
            self.assertEqual(result.exit_code, 2)

    def test_cli_statuses_and_exit_codes(self) -> None:
        script = TOOLS / "contextual_anchor_preflight.py"
        cases = (
            ("envelope_good.json", 0, "PREFLIGHT_VERIFIED"),
            ("envelope_bad_wrong_chapter.json", 1, "PREFLIGHT_FAILED"),
        )
        for payload_name, expected_code, expected_status in cases:
            with self.subTest(payload=payload_name):
                completed = subprocess.run(
                    [sys.executable, "-B", str(script), str(self.scope_path), str(FIXTURES / payload_name)],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(completed.returncode, expected_code)
                self.assertIn(expected_status, completed.stdout + completed.stderr)
        usage = subprocess.run(
            [sys.executable, "-B", str(script)], cwd=ROOT, check=False, capture_output=True, text=True
        )
        self.assertEqual(usage.returncode, 2)
        self.assertIn("INPUT_ERROR", usage.stderr)

    def test_scanner_is_offline_and_does_not_import_locale_or_lua_runtime(self) -> None:
        source = (TOOLS / "contextual_anchor_preflight.py").read_text(encoding="utf-8")
        for forbidden in ("LocaleLoader", "luajit", "LuaJIT", "subprocess", "os.system"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)


class ContextualAnchorContractGuardTests(unittest.TestCase):
    targets = (
        ".ai/roles/orchestrator.md",
        "docs/paseo-orchestration-v2-contract.md",
    )

    def _copied_active_root(self, temporary_root: Path) -> None:
        for relative in paseo_contract_check.ACTIVE_FILES:
            destination = temporary_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text((ROOT / relative).read_text(encoding="utf-8"), encoding="utf-8")

    def test_anchor_contract_clauses_are_complete_and_unique(self) -> None:
        for relative in self.targets:
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(document=relative):
                for clause in paseo_contract_check.CONTEXTUAL_ANCHOR_PREFLIGHT_MARKERS:
                    self.assertEqual(paseo_contract_check.REQUIRED_MARKERS[relative].count(clause), 1)
                    self.assertEqual(text.count(clause), 1)

    def test_deleting_or_mutating_each_anchor_clause_fails_the_guard(self) -> None:
        for relative in self.targets:
            for clause in paseo_contract_check.CONTEXTUAL_ANCHOR_PREFLIGHT_MARKERS:
                for replacement in ("", clause[:-1] + "!"):
                    with self.subTest(document=relative, clause=clause[:28], replacement=replacement):
                        with tempfile.TemporaryDirectory(prefix="anchor-contract-guard-") as temporary:
                            temporary_root = Path(temporary)
                            self._copied_active_root(temporary_root)
                            mutated = temporary_root / relative
                            source = mutated.read_text(encoding="utf-8")
                            mutated.write_text(source.replace(clause, replacement, 1), encoding="utf-8")
                            with (
                                patch.object(paseo_contract_check, "ROOT", temporary_root),
                                contextlib.redirect_stderr(io.StringIO()),
                            ):
                                self.assertEqual(paseo_contract_check.main(), 1)


if __name__ == "__main__":
    unittest.main()
