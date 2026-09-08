"""Toolchain tests: locale extract."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import EMPTY_POLICY, ROOT
import contextlib
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from i18nlib.config import load_manifest
from i18nlib.build import _lua_string
from i18nlib.errors import ExtractionError, ValidationError
from i18nlib.extract import _normalized_definitions, extract_components
from i18nlib.lint import lint_documents
from i18nlib.locale_model import LocaleLoader
from i18nlib.merge import classify_merge
from i18nlib.runtime import LuaRuntime
from i18nlib.snapshot import read_snapshot


class LuaLocaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

    def test_loader_preserves_tags_arguments_and_lines(self) -> None:
        document = self.loader.load_bytes(
            b'section "fixture/a.lua"\n'
            b't("%s has %d", "%d belongs to %s", "tformat", {2, 1})\n'
            b't("nil tag", "string nil tag", "nil")\n'
            b't("real nil", "real nil tag")\n',
            logical_path="fixture.lua",
        )
        entries = document.translations
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0]["line"], 2)
        self.assertEqual(entries[0]["args_order"], [2, 1])
        self.assertEqual(entries[1]["source_tag"], "nil")
        self.assertIsNone(entries[2]["source_tag"])

    def test_loader_preserves_empty_array_and_object_metadata(self) -> None:
        document = self.loader.load_bytes(
            b't("empty args", "empty args", "nil", {})\n'
            b't("empty special", "empty special", "nil", nil, {})\n',
            logical_path="fixture.lua",
        )
        entries = document.translations
        self.assertEqual(entries[0]["args_order"], [])
        self.assertEqual(entries[0]["special"], None)
        self.assertEqual(entries[1]["args_order"], None)
        self.assertEqual(entries[1]["special"], {})

    def test_valid_argument_reordering_passes_lint(self) -> None:
        document = self.loader.load_bytes(
            b'section "fixture/a.lua"\n'
            b't("%s has %d", "%d belongs to %s", "tformat", {2, 1})\n',
            logical_path="fixture.lua",
        )
        issues, metrics = lint_documents([("fixture", document)], EMPTY_POLICY)
        self.assertEqual(metrics["errors"], 0)
        self.assertFalse([issue for issue in issues if issue.code == "format-mismatch"])

    def test_format_loss_is_blocking(self) -> None:
        document = self.loader.load_bytes(
            b'section "fixture/a.lua"\n'
            b't("%s has %d", "%s", "tformat")\n',
            logical_path="fixture.lua",
        )
        issues, _ = lint_documents([("fixture", document)], EMPTY_POLICY)
        self.assertEqual(
            [issue.code for issue in issues if issue.severity == "error"],
            ["format-mismatch"],
        )

    def test_argument_order_must_be_a_permutation(self) -> None:
        document = self.loader.load_bytes(
            b'section "fixture/a.lua"\n'
            b't("%d plus %d", "%d plus %d", "tformat", {1, 1})\n',
            logical_path="fixture.lua",
        )
        issues, _ = lint_documents([("fixture", document)], EMPTY_POLICY)
        self.assertIn("format-mismatch", [issue.code for issue in issues])

    def test_width_change_is_reviewable_not_a_type_error(self) -> None:
        document = self.loader.load_bytes(
            b'section "fixture/a.lua"\n'
            b't("%-8.8s", "%s", "tformat")\n',
            logical_path="fixture.lua",
        )
        issues, metrics = lint_documents([("fixture", document)], EMPTY_POLICY)
        self.assertEqual(metrics["errors"], 0)
        self.assertIn("format-shape-difference", [issue.code for issue in issues])

    def test_non_format_translation_does_not_treat_prose_percent_as_argument(self) -> None:
        document = self.loader.load_bytes(
            b'section "fixture/a.lua"\n'
            b't("Gain 10% of life", "\xe8\x8e\xb7\xe5\xbe\x97 10% \xe7\x94\x9f\xe5\x91\xbd", "_t")\n',
            logical_path="fixture.lua",
        )
        issues, _ = lint_documents([("fixture", document)], EMPTY_POLICY)
        self.assertFalse([issue for issue in issues if issue.code == "format-mismatch"])

    def test_generated_lua_strings_round_trip(self) -> None:
        values = (
            "simple",
            'quote " and slash ' + "\\",
            "line one\nline two",
            "\nleading newline",
            "contains ]] and ]=] delimiters\nwithout loss",
            # 内容以 "]" 结尾时，0 级长括号会与闭合串拼出提前闭合点（value + "]]" -> "]]]"）。
            "multi line ending in a bracket\n[b]poster[/b]",
            "nested level ending in a bracket\ncontains ]=] and ends with ]",
        )
        for value in values:
            with self.subTest(value=value):
                source = (
                    'section "fixture/a.lua"\n'
                    f"t({_lua_string(value)}, {_lua_string(value)}, \"_t\")\n"
                ).encode("utf-8")
                document = self.loader.load_bytes(source, logical_path="generated.lua")
                self.assertEqual(document.translations[0]["source"], value)
                self.assertEqual(document.translations[0]["target"], value)


class ProtectedExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.broker = ROOT / "tools" / "lua" / "protected_extract.lua"

    def test_lua_broker_exports_only_redacted_extracted_text(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-protected-test-") as temporary:
            directory = Path(temporary)
            source = directory / "protected-source"
            source.mkdir()
            (source / "secret.lua").write_text(
                "Confidential extracted text", encoding="utf-8"
            )
            extractor = directory / "fake-extractor.lua"
            extractor.write_text(
                """local root = ...
local input = assert(io.open(root .. "/secret.lua", "rb"))
local text = assert(input:read("*a"))
input:close()
print("discarded diagnostic", text)
io.stderr:write("discarded stderr")
local output = assert(io.open("i18n_list.lua", "wb"))
output:write(("section %q\\n"):format(root .. "/secret.lua"))
output:write(("tDef(1, %q, %q)\\n"):format(text, "_t"))
output:close()
""",
                encoding="utf-8",
            )
            output = directory / "extracted.lua"
            result = self.runtime.run_protected(
                [
                    self.broker,
                    "extract",
                    extractor,
                    output,
                    "dlc-fixture",
                    source,
                ],
                cwd=directory,
                timeout=30,
            )
            extracted = output.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0)
        self.assertIsNone(result.stdout)
        self.assertIsNone(result.stderr)
        self.assertIn("Confidential extracted text", extracted)
        self.assertIn('section "dlc-fixture/secret.lua"', extracted)
        self.assertNotIn(str(source), extracted)

    def test_lua_broker_fails_closed_on_parser_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-protected-test-") as temporary:
            directory = Path(temporary)
            source = directory / "protected-source"
            source.mkdir()
            extractor = directory / "fake-extractor.lua"
            extractor.write_text(
                """local root = ...
print("In file confidential.lua: parse failure")
local output = assert(io.open("i18n_list.lua", "wb"))
output:write('section "leak"\\ntDef(1, "leak", "_t")\\n')
output:close()
""",
                encoding="utf-8",
            )
            output = directory / "extracted.lua"
            result = self.runtime.run_protected(
                [
                    self.broker,
                    "extract",
                    extractor,
                    output,
                    "dlc-fixture",
                    source,
                ],
                cwd=directory,
                timeout=30,
            )
        self.assertEqual(result.returncode, 21)
        self.assertFalse(output.exists())
        self.assertFalse((directory / "i18n_list.lua").exists())

    def test_lua_broker_treats_mount_percent_as_literal(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-protected-test-") as temporary:
            directory = Path(temporary)
            source = directory / "protected-source"
            source.mkdir()
            extractor = directory / "fake-extractor.lua"
            extractor.write_text(
                """local root = ...
local output = assert(io.open("i18n_list.lua", "wb"))
output:write(("section %q\\n"):format(root .. "/secret.lua"))
output:write('tDef(1, "ok", "_t")\\n')
output:close()
""",
                encoding="utf-8",
            )
            output = directory / "extracted.lua"
            result = self.runtime.run_protected(
                [
                    self.broker,
                    "extract",
                    extractor,
                    output,
                    "dlc%fixture",
                    source,
                ],
                cwd=directory,
                timeout=30,
            )
            extracted = output.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0)
        self.assertIn('section "dlc%fixture/secret.lua"', extracted)
        self.assertNotIn("i18n_list.lua", extracted)

    def test_lua_broker_rejects_stale_output_on_false_success(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-protected-test-") as temporary:
            directory = Path(temporary)
            source = directory / "protected-source"
            source.mkdir()
            extractor = directory / "fake-extractor.lua"
            extractor.write_text("os.exit(0)\n", encoding="utf-8")
            output = directory / "extracted.lua"
            output.write_text("stale output", encoding="utf-8")
            result = self.runtime.run_protected(
                [
                    self.broker,
                    "extract",
                    extractor,
                    output,
                    "dlc-fixture",
                    source,
                ],
                cwd=directory,
                timeout=30,
            )
        self.assertEqual(result.returncode, 24)
        self.assertFalse(output.exists())


class ExtractionNormalizationTests(unittest.TestCase):
    @staticmethod
    def _definition(**overrides: object) -> dict[str, object]:
        record: dict[str, object] = {
            "kind": "definition",
            "section": "fixture/dialog.lua",
            "source": "Fixture source",
            "source_tag": "_t",
            "source_line": 7,
            "logical_path": "generated:fixture/i18n_list.lua",
        }
        record.update(overrides)
        return record

    def test_valid_definitions_preserve_output_fields_and_order(self) -> None:
        records = [
            self._definition(),
            self._definition(
                section="fixture/nullable.lua",
                source="Nullable origin fields",
                source_tag=None,
                source_line=8,
                logical_path=None,
            ),
            self._definition(
                section="fixture/empty-nullable.lua",
                source="Empty nullable strings",
                source_tag="",
                source_line=9,
                logical_path="",
            ),
        ]

        normalized = _normalized_definitions(
            component="fixture",
            records=records,
            origin_kind="extracted",
        )

        self.assertEqual(
            normalized,
            [
                {
                    "component": "fixture",
                    "section": "fixture/dialog.lua",
                    "source": "Fixture source",
                    "source_tag": "_t",
                    "origin_line": 7,
                    "origin_kind": "extracted",
                    "origin_document": "generated:fixture/i18n_list.lua",
                },
                {
                    "component": "fixture",
                    "section": "fixture/nullable.lua",
                    "source": "Nullable origin fields",
                    "source_tag": None,
                    "origin_line": 8,
                    "origin_kind": "extracted",
                    "origin_document": None,
                },
                {
                    "component": "fixture",
                    "section": "fixture/empty-nullable.lua",
                    "source": "Empty nullable strings",
                    "source_tag": "",
                    "origin_line": 9,
                    "origin_kind": "extracted",
                    "origin_document": "",
                },
            ],
        )
        self.assertEqual(
            list(normalized[0]),
            [
                "component",
                "section",
                "source",
                "source_tag",
                "origin_line",
                "origin_kind",
                "origin_document",
            ],
        )

    def test_non_definition_objects_are_ignored_without_field_validation(self) -> None:
        records = [
            {},
            {
                "kind": "translation",
                "section": None,
                "source": 0,
                "source_tag": [],
                "source_line": False,
                "logical_path": {},
            },
        ]

        self.assertEqual(
            _normalized_definitions(
                component="fixture",
                records=records,
                origin_kind="extracted",
            ),
            [],
        )

    def test_component_and_origin_kind_are_validated(self) -> None:
        for value in (None, "", False, 1, [], {}):
            with self.subTest(field="component", value=value):
                with self.assertRaises(ExtractionError) as raised:
                    _normalized_definitions(
                        component=value,  # type: ignore[arg-type]
                        records=[],
                        origin_kind="extracted",
                    )
                self.assertIn("'component'", str(raised.exception))

        for value in (None, "", "generated", False, 1, [], {}):
            with self.subTest(field="origin_kind", value=value):
                with self.assertRaises(ExtractionError) as raised:
                    _normalized_definitions(
                        component="fixture",
                        records=[],
                        origin_kind=value,  # type: ignore[arg-type]
                    )
                self.assertIn("'origin_kind'", str(raised.exception))

    def test_non_object_records_raise_extraction_error_with_position(self) -> None:
        for value in (None, "definition", False, 1, [], ()):
            with self.subTest(value=value):
                with self.assertRaises(ExtractionError) as raised:
                    _normalized_definitions(
                        component="fixture",
                        records=[{"kind": "translation"}, value],
                        origin_kind="extracted",
                    )
                self.assertIn("record 2", str(raised.exception))
                self.assertIn("object", str(raised.exception))

    def test_definition_text_fields_reject_invalid_values(self) -> None:
        invalid_values = {
            "section": (None, "", False, 1, [], {}),
            "source": (None, False, 1, [], {}),
            "source_tag": (False, 1, 1.0, [], {}),
            "logical_path": (False, 1, 1.0, [], {}),
        }
        for field, values in invalid_values.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    record = self._definition(**{field: value})
                    with self.assertRaises(ExtractionError) as raised:
                        _normalized_definitions(
                            component="fixture",
                            records=[{"kind": "translation"}, record],
                            origin_kind="extracted",
                        )
                    message = str(raised.exception)
                    self.assertIn("record 2", message)
                    self.assertIn(f"'{field}'", message)

    def test_extracted_empty_source_preserves_raw_baseline_record(self) -> None:
        normalized = _normalized_definitions(
            component="fixture",
            records=[self._definition(source="")],
            origin_kind="extracted",
        )

        self.assertEqual(normalized[0]["source"], "")

        with tempfile.TemporaryDirectory(
            prefix="tome4-empty-extracted-snapshot-test-"
        ) as temporary:
            path = Path(temporary) / "snapshot.jsonl"
            records = [
                normalized[0],
                {
                    **normalized[0],
                    "source": "Translatable source",
                    "origin_line": 8,
                },
            ]
            raw = "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                for record in records
            )
            path.write_text(raw, encoding="utf-8")
            snapshot = read_snapshot(path, expected_component="fixture")

        self.assertEqual(len(snapshot.definitions), 1)
        self.assertEqual(snapshot.definitions[0].source, "Translatable source")
        self.assertEqual(
            snapshot.sha256,
            hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        )

    def test_manual_empty_source_is_rejected(self) -> None:
        with self.assertRaises(ExtractionError) as raised:
            _normalized_definitions(
                component="engine",
                records=[self._definition(source="")],
                origin_kind="manual",
            )

        self.assertIn("manual definitions", str(raised.exception))

        with tempfile.TemporaryDirectory(
            prefix="tome4-empty-manual-snapshot-test-"
        ) as temporary:
            path = Path(temporary) / "snapshot.jsonl"
            record = {
                "component": "engine",
                "section": ".always_merge",
                "source": "",
                "source_tag": None,
                "origin_line": None,
                "origin_kind": "manual",
                "origin_document": "_tdef_append.lua",
            }
            path.write_text(
                json.dumps(record, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValidationError) as snapshot_raised:
                read_snapshot(path, expected_component="engine")

        self.assertIn("snapshot source is invalid", str(snapshot_raised.exception))

    def test_extracted_source_line_requires_exact_positive_integer(self) -> None:
        for value in (None, True, False, 1.0, "1", 0, -1):
            with self.subTest(value=value):
                with self.assertRaises(ExtractionError) as raised:
                    _normalized_definitions(
                        component="fixture",
                        records=[
                            {"kind": "translation"},
                            self._definition(source_line=value),
                        ],
                        origin_kind="extracted",
                    )
                message = str(raised.exception)
                self.assertIn("record 2", message)
                self.assertIn("'source_line'", message)
                if type(value) is int and value == 0:
                    self.assertIn("only manual definitions may use 0", message)

    def test_manual_zero_line_sentinel_normalizes_to_readable_snapshot(self) -> None:
        normalized = _normalized_definitions(
            component="engine",
            records=[
                self._definition(
                    section=".always_merge",
                    source="Manual fixture",
                    source_line=0,
                    logical_path="_tdef_append.lua",
                )
            ],
            origin_kind="manual",
        )
        self.assertIsNone(normalized[0]["origin_line"])

        with tempfile.TemporaryDirectory(
            prefix="tome4-manual-snapshot-test-"
        ) as temporary:
            path = Path(temporary) / "snapshot.jsonl"
            path.write_text(
                json.dumps(normalized[0], ensure_ascii=False, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
            snapshot = read_snapshot(path, expected_component="engine")

        self.assertEqual(len(snapshot.definitions), 1)
        self.assertIsNone(snapshot.definitions[0].origin_line)
        self.assertEqual(snapshot.definitions[0].origin_kind, "manual")
        self.assertEqual(
            snapshot.definitions[0].origin_document,
            "_tdef_append.lua",
        )

    def test_manual_positive_line_is_preserved_and_other_values_fail(self) -> None:
        normalized = _normalized_definitions(
            component="engine",
            records=[self._definition(source_line=3)],
            origin_kind="manual",
        )
        self.assertEqual(normalized[0]["origin_line"], 3)

        for value in (None, True, False, 1.0, "1", -1):
            with self.subTest(value=value):
                with self.assertRaises(ExtractionError) as raised:
                    _normalized_definitions(
                        component="engine",
                        records=[self._definition(source_line=value)],
                        origin_kind="manual",
                    )
                message = str(raised.exception)
                self.assertIn("record 1", message)
                self.assertIn("'source_line'", message)
                if value == -1:
                    self.assertIn(
                        "manual definitions may use only 0",
                        message,
                    )

    def test_extract_timeout_rejects_invalid_values_before_work_or_io(self) -> None:
        component_iteration = Mock(
            side_effect=AssertionError("components must not be iterated")
        )

        class Components:
            def __iter__(self):  # type: ignore[no-untyped-def]
                return component_iteration()

        manifest = Mock()
        runtime = Mock()
        with (
            patch("i18nlib.extract.GitRepository") as git_repository,
            patch("i18nlib.extract.LocaleLoader") as locale_loader,
            patch("i18nlib.extract.create_run_directory") as create_run_directory,
            patch("i18nlib.extract.tempfile.TemporaryDirectory") as temporary_directory,
            patch("i18nlib.extract.Path.mkdir") as path_mkdir,
            patch("i18nlib.extract._patch_extractor") as patch_extractor,
            patch("i18nlib.extract._run_protected_extractor") as protected_extractor,
            patch("i18nlib.extract.atomic_write_bytes") as atomic_write,
            patch("i18nlib.extract.write_json") as write_json,
        ):
            for timeout in (True, 1.5, "1", 0, -1):
                with self.subTest(timeout=timeout):
                    with self.assertRaisesRegex(
                        ExtractionError,
                        r"^timeout must be a positive integer$",
                    ):
                        extract_components(
                            manifest,
                            runtime,
                            Components(),
                            timeout=timeout,  # type: ignore[arg-type]
                        )

        component_iteration.assert_not_called()
        self.assertEqual(manifest.mock_calls, [])
        self.assertEqual(runtime.mock_calls, [])
        for dependency in (
            git_repository,
            locale_loader,
            create_run_directory,
            temporary_directory,
            path_mkdir,
            patch_extractor,
            protected_extractor,
            atomic_write,
            write_json,
        ):
            dependency.assert_not_called()

    def test_extract_timeout_one_reaches_mocked_extractor(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-extract-timeout-test-"
        ) as temporary:
            root = Path(temporary)
            temporary_root = root / "staging"
            temporary_root.mkdir()
            output_file = root / "i18n_list.lua"
            output_file.write_bytes(b"fixture")
            component = Mock(
                id="fixture",
                source_repository=None,
                sources=(),
                protected_source=object(),
                source_baseline=None,
            )
            manifest = Mock(
                root=root,
                version="fixture-version",
                path=root / "manifest.json",
                manual_definitions=(),
            )
            manifest.extractor = Mock(
                repository="extractor",
                commit="a" * 40,
                git_path="i18n_tools",
            )
            manifest.repository_path.return_value = root / "extractor-repository"
            document = Mock(records=(self._definition(),))
            runtime = Mock()

            with (
                patch("i18nlib.extract.GitRepository"),
                patch("i18nlib.extract.LocaleLoader") as loader_class,
                patch(
                    "i18nlib.extract.create_run_directory",
                    return_value=root / "run",
                ),
                patch(
                    "i18nlib.extract.tempfile.TemporaryDirectory",
                    return_value=contextlib.nullcontext(str(temporary_root)),
                ),
                patch("i18nlib.extract._patch_extractor", return_value={}),
                patch(
                    "i18nlib.extract._run_protected_extractor",
                    return_value=(output_file, ["fixture"]),
                ) as protected_extractor,
                patch("i18nlib.extract.atomic_write_bytes"),
                patch("i18nlib.extract.write_json"),
            ):
                loader_class.return_value.load_path.return_value = document
                report = extract_components(
                    manifest,
                    runtime,
                    [component],
                    timeout=1,
                )

        self.assertTrue(report["ok"])
        self.assertEqual(report["components"][0]["component"], "fixture")
        protected_extractor.assert_called_once()
        self.assertEqual(protected_extractor.call_args.kwargs["timeout"], 1)

    def test_invalid_bridge_record_fails_before_snapshot_serialization_or_write(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-extract-validation-test-"
        ) as temporary:
            root = Path(temporary)
            component = Mock(
                id="fixture",
                source_repository=None,
                sources=(),
                protected_source=object(),
            )
            manifest = Mock(root=root)
            manifest.extractor = Mock(
                repository="extractor",
                commit="a" * 40,
                git_path="i18n_tools",
            )
            manifest.repository_path.return_value = root / "extractor-repository"
            document = Mock(records=({"kind": "definition", "section": ""},))

            with (
                patch("i18nlib.extract.GitRepository"),
                patch("i18nlib.extract.LocaleLoader") as loader_class,
                patch(
                    "i18nlib.extract.create_run_directory",
                    return_value=root / "run",
                ),
                patch("i18nlib.extract._patch_extractor", return_value={}),
                patch(
                    "i18nlib.extract._run_protected_extractor",
                    return_value=(root / "i18n_list.lua", ["fixture"]),
                ),
                patch("i18nlib.extract.json.dumps") as json_dumps,
                patch("i18nlib.extract.atomic_write_bytes") as atomic_write,
                patch("i18nlib.extract.write_json") as write_json,
            ):
                loader_class.return_value.load_path.return_value = document
                with self.assertRaises(ExtractionError) as raised:
                    extract_components(
                        manifest,
                        Mock(),
                        [component],
                        timeout=1,
                    )

        self.assertIn("record 1", str(raised.exception))
        self.assertIn("'section'", str(raised.exception))
        json_dumps.assert_not_called()
        atomic_write.assert_not_called()
        write_json.assert_not_called()


class MergeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        manifest = load_manifest()
        runtime = LuaRuntime(manifest)
        runtime.doctor()
        cls.loader = LocaleLoader(runtime)

    @staticmethod
    def _write_snapshot(
        directory: Path, name: str, definitions: list[tuple[str, str, str]]
    ) -> Path:
        path = directory / name
        records = [
            {
                "component": "fixture",
                "section": section,
                "source": source,
                "source_tag": source_tag,
                "origin_line": index + 1,
                "origin_kind": "extracted",
                "origin_document": f"generated:{name}",
            }
            for index, (section, source, source_tag) in enumerate(definitions)
        ]
        path.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )
        return path

    def test_three_way_classification_never_carries_changed_source(self) -> None:
        current = self.loader.load_bytes(
            b'section "same.lua"\n'
            b't("Keep", "Keep ZH", "_t")\n'
            b'section "old.lua"\n'
            b't("Move", "Move ZH", "_t")\n'
            b't("The old sentence is here.", "Old sentence ZH", "_t")\n'
            b't("Obsolete", "Obsolete ZH", "_t")\n',
            logical_path="fixture.lua",
        )
        with tempfile.TemporaryDirectory(prefix="tome4-merge-test-") as temporary:
            directory = Path(temporary)
            base_path = self._write_snapshot(
                directory,
                "base.jsonl",
                [
                    ("same.lua", "Keep", "_t"),
                    ("old.lua", "Move", "_t"),
                    ("old.lua", "The old sentence is here.", "_t"),
                    ("old.lua", "Obsolete", "_t"),
                ],
            )
            new_path = self._write_snapshot(
                directory,
                "new.jsonl",
                [
                    ("same.lua", "Keep", "_t"),
                    ("new.lua", "Move", "_t"),
                    ("old.lua", "The old sentence is still here.", "_t"),
                    ("old.lua", "Added", "_t"),
                ],
            )
            base = read_snapshot(base_path, expected_component="fixture")
            new = read_snapshot(new_path, expected_component="fixture")
            candidate, report = classify_merge(
                component="fixture",
                current=current,
                base_snapshot=base,
                new_snapshot=new,
            )
        self.assertEqual([entry["source"] for entry in candidate], ["Keep", "Move"])
        self.assertEqual(report["counts"]["exact_editorial"], 1)
        self.assertEqual(report["counts"]["moved_section"], 1)
        self.assertEqual(report["counts"]["untranslated"], 2)
        self.assertEqual(report["counts"]["source_changed_suggestions"], 1)
        suggestion = report["source_changed_suggestions"][0]
        self.assertEqual(suggestion["previous_target"], "Old sentence ZH")
        self.assertFalse(suggestion["automatic"])

    def test_snapshot_groups_duplicate_occurrences(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-snapshot-test-") as temporary:
            path = self._write_snapshot(
                Path(temporary),
                "duplicates.jsonl",
                [
                    ("same.lua", "Repeated", "_t"),
                    ("same.lua", "Repeated", "_t"),
                ],
            )
            snapshot = read_snapshot(path, expected_component="fixture")
        self.assertEqual(len(snapshot.definitions), 2)
        self.assertEqual(len(snapshot.groups), 1)
        self.assertEqual(len(snapshot.groups[0].occurrences), 2)


if __name__ == "__main__":
    unittest.main()
