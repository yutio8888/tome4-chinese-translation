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

    def test_v2_payload_uses_the_same_anchor_semantics(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            self._write_valid_pair(scope, payload)
            value = json.loads(payload.read_text(encoding="utf-8"))
            value["contract"] = "translation_contextual_v2"
            self._write(payload, value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
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

    def _untitled_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        temporary = tempfile.TemporaryDirectory(prefix="contextual-anchor-")
        root = Path(temporary.name)
        story = root / "story.lua"
        story.write_text(
            'section "before"\n'
            't("preceding source", "", "_t")\n'
            'section "intro"\n'
            't("intro first", "", "_t")\n'
            't("intro second", "", "_t")\n'
            'section "other"\n'
            't("neighbour source", "", "_t")\n',
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

    def _run_args_order_case(self, fourth_argument: str, context: str) -> preflight.PreflightResult:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            (root / "story.lua").write_text(
                'section "story"\n'
                't("Book [Book 9, Chapter 1] - One", "", "_t")\n'
                f't("inside", "", "_t"{fourth_argument})\n'
                't("Book [Book 9, Chapter 2] - Two", "", "_t")\n',
                encoding="utf-8",
            )
            self._write_valid_pair(scope, payload)
            value = self._payload("envelope_good.json")
            value["translation_snapshot"] = [
                {"revision_key": "r1", "source": "inside", "target": "译文"}
            ]
            value["bounded_context"] = [{"revision_key": "r1", "context": context}]
            self._write(payload, value)
            return preflight.run_preflight(scope, payload, workspace_root=root)

    def test_empty_ordered_titles_verifies_whole_untitled_section(self) -> None:
        temporary, root, scope, payload = self._untitled_workspace()
        with temporary:
            self._write(scope, self._scope(section="intro", titles=[]))
            payload_value = self._payload("envelope_good.json")
            payload_value["ordered_revision_keys"] = ["r1", "r2"]
            payload_value["translation_snapshot"] = [
                {"revision_key": "r1", "source": "intro first", "target": "首段"},
                {"revision_key": "r2", "source": "intro second", "target": "次段"},
            ]
            payload_value["bounded_context"] = [
                {"revision_key": "r1", "context": ""},
                {"revision_key": "r2", "context": ""},
            ]
            self._write(payload, payload_value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_VERIFIED")
            self.assertEqual(result.exit_code, 0)

    def test_empty_ordered_titles_fails_closed_for_titled_section(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            self._write_valid_pair(scope, payload, self._scope(titles=[]))
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_FAILED")
            self.assertEqual(result.exit_code, 1)
            self.assertIn("actual chapter-title", result.errors[0])
            self.assertIn(
                "ordered_titles=[] is only valid for untitled sections; titled sections must keep declaring explicit anchors",
                result.errors[0],
            )
            self.assertNotIn(
                "ordered_titles=[] is only valid for untitled sections, which must keep explicit anchors",
                result.errors[0],
            )

    def test_empty_ordered_titles_rejects_source_from_neighbouring_section(self) -> None:
        temporary, root, scope, payload = self._untitled_workspace()
        with temporary:
            self._write(scope, self._scope(section="intro", titles=[]))
            payload_value = self._payload("envelope_good.json")
            payload_value["translation_snapshot"] = [
                {"revision_key": "r1", "source": "neighbour source", "target": "邻段"}
            ]
            self._write(payload, payload_value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_FAILED")
            self.assertEqual(result.exit_code, 1)

    def test_empty_ordered_titles_rejects_source_from_preceding_section(self) -> None:
        temporary, root, scope, payload = self._untitled_workspace()
        with temporary:
            self._write(scope, self._scope(section="intro", titles=[]))
            payload_value = self._payload("envelope_good.json")
            payload_value["translation_snapshot"] = [
                {"revision_key": "r1", "source": "preceding source", "target": "前段"}
            ]
            self._write(payload, payload_value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_FAILED")
            self.assertEqual(result.exit_code, 1)

    def test_args_order_disclosure_verifies_matching_canonical_token(self) -> None:
        result = self._run_args_order_case(", {2,1}", "args_order={2,1}")
        self.assertEqual(result.status, "PREFLIGHT_VERIFIED")
        self.assertEqual(result.exit_code, 0)

    def test_args_order_disclosure_missing_token_fails(self) -> None:
        result = self._run_args_order_case(", {2,1}", "")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")
        self.assertIn("revision key 'r1'", result.errors[0])
        self.assertIn("args_order={2,1}", result.errors[0])

    def test_args_order_token_without_call_args_order_fails(self) -> None:
        result = self._run_args_order_case("", "args_order={2,1}")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")
        self.assertIn("revision key 'r1'", result.errors[0])
        self.assertIn("args_order=", result.errors[0])

    def test_args_order_disclosure_wrong_token_fails(self) -> None:
        result = self._run_args_order_case(", {2,1}", "args_order={1,2}")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")
        self.assertIn("args_order={2,1}", result.errors[0])

    def test_args_order_prefixed_disclosure_fails(self) -> None:
        result = self._run_args_order_case(", {2,1}", "previous_args_order={2,1}")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_args_order_correct_plus_wrong_disclosures_fail(self) -> None:
        result = self._run_args_order_case(", {2,1}", "args_order={2,1} args_order={1,2}")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_args_order_longer_value_disclosure_fails(self) -> None:
        result = self._run_args_order_case(", {2,1}", "args_order={2,1,3}")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_args_order_malformed_disclosure_fails(self) -> None:
        for context in ("args_order=wrong", "args_order={2,1"):
            with self.subTest(context=context):
                result = self._run_args_order_case(", {2,1}", context)
                self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_args_order_disclosure_with_suffix_fails(self) -> None:
        result = self._run_args_order_case(", {2,1}", "args_order={2,1}suffix")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_args_order_disclosure_with_underscore_suffix_fails(self) -> None:
        result = self._run_args_order_case(", {2,1}", "args_order={2,1}_suffix")
        self.assertEqual(result.status, "PREFLIGHT_FAILED")

    def test_args_order_explicit_nil_is_treated_as_absent(self) -> None:
        result = self._run_args_order_case(", nil", "")
        self.assertEqual(result.status, "PREFLIGHT_VERIFIED")
        _, calls = preflight._scan_lua('t("inside", "", "_t", nil)')
        self.assertIsNone(calls[0].args_order)

    def test_args_order_malformed_fourth_argument_is_input_error(self) -> None:
        for fourth_argument in (
            "identifier", "{1, {2}}", "{1.0}", "{-1}", "{0}", "{}"
        ):
            with self.subTest(fourth_argument=fourth_argument):
                with self.assertRaises(preflight.InputError):
                    preflight._scan_lua(f't("inside", "", "_t", {fourth_argument})')
                result = self._run_args_order_case(", " + fourth_argument, "")
                self.assertEqual(result.status, "INPUT_ERROR")

    def test_args_order_spaces_canonicalize_and_verify(self) -> None:
        _, calls = preflight._scan_lua('t("inside", "", "_t", { 2, 1 })')
        self.assertEqual(calls[0].args_order, "{2,1}")
        result = self._run_args_order_case(", { 2, 1 }", "args_order={2,1}")
        self.assertEqual(result.status, "PREFLIGHT_VERIFIED")

    def test_args_order_lua_separators_scan_and_verify(self) -> None:
        for fourth_argument in ("{2;1}", "{2,1,}"):
            with self.subTest(fourth_argument=fourth_argument):
                _, calls = preflight._scan_lua(
                    f't("inside", "", "_t", {fourth_argument})'
                )
                self.assertEqual(calls[0].args_order, "{2,1}")
                result = self._run_args_order_case(", " + fourth_argument, "args_order={2,1}")
                self.assertEqual(result.status, "PREFLIGHT_VERIFIED")

    def test_differing_in_window_args_order_values_fail_closed(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            (root / "story.lua").write_text(
                'section "story"\n'
                't("Book [Book 9, Chapter 1] - One", "", "_t")\n'
                't("inside", "", "_t", {2,1})\n'
                't("inside", "", "_t", {1,2})\n'
                't("Book [Book 9, Chapter 2] - Two", "", "_t")\n',
                encoding="utf-8",
            )
            self._write_valid_pair(scope, payload)
            value = self._payload("envelope_good.json")
            value["translation_snapshot"] = [
                {"revision_key": "r1", "source": "inside", "target": "译文"}
            ]
            value["bounded_context"] = [
                {"revision_key": "r1", "context": "args_order={2,1}"}
            ]
            self._write(payload, value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_FAILED")
            self.assertIn("revision key 'r1'", result.errors[0])
            self.assertIn("args_order={...}", result.errors[0])

    def test_nonempty_ordered_titles_explicit_anchor_regression_remains_verified(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            self._write_valid_pair(scope, payload)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "PREFLIGHT_VERIFIED")
            self.assertEqual(result.exit_code, 0)

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

    def test_non_array_ordered_titles_has_exact_input_error_message(self) -> None:
        temporary, root, scope, payload = self._workspace()
        with temporary:
            value = self._scope()
            value["anchor_scopes"][0]["ordered_titles"] = {}
            self._write_valid_pair(scope, payload, value)
            result = preflight.run_preflight(scope, payload, workspace_root=root)
            self.assertEqual(result.status, "INPUT_ERROR")
            self.assertEqual(result.exit_code, 2)
            self.assertEqual(result.errors, ("anchor scope ordered_titles must be an array",))

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
            't("after", {key = [=[a ) b]=]}, "")\n'
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

    def test_anchor_prose_punctuation_is_not_contract_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="anchor-contract-") as temporary:
            root = Path(temporary)
            self._copied_active_root(root)
            for relative in self.targets:
                path = root / relative
                source = path.read_text()
                path.write_text(source.replace("fails closed.", "fails closed!"))
            with patch.object(paseo_contract_check, "ROOT", root):
                self.assertEqual(paseo_contract_check.main(), 0)

    def test_contextual_live_version_cannot_be_replaced_by_history(self) -> None:
        with tempfile.TemporaryDirectory(prefix="anchor-contract-") as temporary:
            root = Path(temporary)
            self._copied_active_root(root)
            path = root / "docs/paseo-translation-context-review-v1-contract.md"
            source = path.read_text()
            path.write_text(source.replace("> 契约版本：translation-contextual/1.6。", "") + "\n## History\n> 契约版本：translation-contextual/1.6。\n")
            with patch.object(paseo_contract_check, "ROOT", root), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(paseo_contract_check.main(), 1)


if __name__ == "__main__":
    unittest.main()
