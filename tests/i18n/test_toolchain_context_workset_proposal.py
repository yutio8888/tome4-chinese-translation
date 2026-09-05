"""Toolchain tests: context workset proposal."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import create_workset_fixture
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import i18nlib.quality as quality_module
from i18nlib.config import load_manifest
from i18nlib.context import resolve_context, validate_context_options
from i18nlib.cli import main as cli_main
from i18nlib.errors import ConfigurationError, ValidationError
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.proposal import read_json_object, validate_proposal
from i18nlib.workset import (
    ADDON_COMPONENTS,
    DLC_COMPONENTS,
    _plain_source,
    _relevant_terms,
    _resolve_manifest_path,
    _scope_matches,
    _source_tag_matches,
    validate_workset_items,
)


class ContextPreflightTests(unittest.TestCase):
    def test_resolver_rejects_invalid_options_before_any_io(self) -> None:
        cases = (
            (
                "boolean limit",
                {"section_prefix": "", "query": None, "limit": True},
                r"^context --limit must be an integer between 1 and 500$",
            ),
            (
                "float limit",
                {"section_prefix": "", "query": None, "limit": 1.0},
                r"^context --limit must be an integer between 1 and 500$",
            ),
            (
                "string limit",
                {"section_prefix": "", "query": None, "limit": "1"},
                r"^context --limit must be an integer between 1 and 500$",
            ),
            (
                "non-string section",
                {"section_prefix": [], "query": None, "limit": 1},
                r"^context --section must be a string or None$",
            ),
            (
                "non-string query",
                {"section_prefix": "", "query": 1, "limit": 1},
                r"^context --query must be a string or None$",
            ),
            (
                "missing query",
                {"section_prefix": None, "query": None, "limit": 1},
                r"^context requires --section or --query$",
            ),
            (
                "empty query",
                {"section_prefix": None, "query": "", "limit": 1},
                r"^context requires --section or --query$",
            ),
            (
                "blank query",
                {"section_prefix": None, "query": " \t\n", "limit": 1},
                r"^context requires --section or --query$",
            ),
        )
        for label, options, expected_error in cases:
            with self.subTest(case=label):
                loader = Mock(spec=LocaleLoader)
                with (
                    patch("i18nlib.context._terminology_rows") as terminology_rows,
                    patch("i18nlib.context.create_run_directory") as create_run,
                    patch("i18nlib.context.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(ValidationError, expected_error):
                        resolve_context(
                            object(),
                            loader,
                            object(),
                            **options,
                        )

                self.assertEqual(loader.mock_calls, [])
                terminology_rows.assert_not_called()
                create_run.assert_not_called()
                write_json.assert_not_called()

    def test_valid_boundaries_and_empty_section_preserve_context_output(
        self,
    ) -> None:
        manifest = SimpleNamespace(
            root=Path("/fixture"),
            terminology="terminology.tsv",
            version="fixture-version",
            raw_bytes=b"fixture manifest",
        )
        component = SimpleNamespace(
            id="fixture-component",
            translation="canonical.lua",
        )
        document = LocaleDocument(
            logical_path="canonical.lua",
            sha256="a" * 64,
            records=(
                {
                    "kind": "translation",
                    "section": "alpha.lua",
                    "source": "First source",
                    "target": "第一条",
                    "source_tag": "_t",
                    "args_order": None,
                    "special": None,
                    "line": 1,
                },
                {
                    "kind": "translation",
                    "section": "beta.lua",
                    "source": "Second source",
                    "target": "第二条",
                    "source_tag": None,
                    "args_order": None,
                    "special": None,
                    "line": 2,
                },
            ),
        )

        for limit, expected_selected in ((1, 1), (500, 2)):
            with self.subTest(limit=limit):
                validate_context_options(
                    section_prefix="",
                    query=" \t",
                    limit=limit,
                )
                loader = Mock(spec=LocaleLoader)
                loader.load_path.return_value = document
                run_directory = Path("/artifacts/context-run")
                with (
                    patch(
                        "i18nlib.context._terminology_rows",
                        return_value=([], "b" * 64),
                    ),
                    patch(
                        "i18nlib.context.create_run_directory",
                        return_value=run_directory,
                    ),
                    patch("i18nlib.context.write_json") as write_json,
                ):
                    result = resolve_context(
                        manifest,
                        loader,
                        component,
                        section_prefix="",
                        query=None,
                        limit=limit,
                    )

                self.assertEqual(
                    result["selection"],
                    {
                        "section_prefix": "",
                        "query": None,
                        "limit": limit,
                        "available": 2,
                        "selected": expected_selected,
                    },
                )
                self.assertEqual(len(result["items"]), expected_selected)
                self.assertEqual(result["terminology"], [])
                self.assertEqual(result["resolver_contract"], "tome4-context-v2")
                self.assertEqual(result["run_directory"], str(run_directory))
                self.assertEqual(
                    result["output"],
                    str(run_directory / f"{result['context_id']}.json"),
                )
                write_json.assert_called_once_with(
                    Path(result["output"]), result
                )

    def test_cli_invalid_options_fail_before_manifest_and_runtime(self) -> None:
        cases = (
            (
                [
                    "context",
                    "--component",
                    "tome",
                    "--section",
                    "",
                    "--limit",
                    "0",
                ],
                "ERROR: context --limit must be between 1 and 500\n",
            ),
            (
                ["context", "--component", "tome"],
                "ERROR: context requires --section or --query\n",
            ),
        )
        for arguments, expected_stderr in cases:
            with self.subTest(arguments=arguments):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    patch("i18nlib.cli._inject_public_dlc_env"),
                    patch("i18nlib.cli_review._manifest") as manifest_factory,
                    patch("i18nlib.cli_review.LuaRuntime") as runtime_factory,
                    patch("i18nlib.cli_review.LocaleLoader") as loader_factory,
                    patch("i18nlib.cli_review.resolve_context") as resolver,
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    exit_code = cli_main(arguments)

                self.assertEqual(exit_code, ValidationError.exit_code)
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(stderr.getvalue(), expected_stderr)
                manifest_factory.assert_not_called()
                runtime_factory.assert_not_called()
                loader_factory.assert_not_called()
                resolver.assert_not_called()

    def test_cli_unknown_component_fails_before_runtime_doctor(self) -> None:
        manifest = Mock()
        manifest.component.side_effect = ConfigurationError(
            "unknown component 'missing'"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("i18nlib.cli._inject_public_dlc_env"),
            patch("i18nlib.cli_review._manifest", return_value=manifest) as manifest_factory,
            patch("i18nlib.cli_review.LuaRuntime") as runtime_factory,
            patch("i18nlib.cli_review.LocaleLoader") as loader_factory,
            patch("i18nlib.cli_review.resolve_context") as resolver,
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = cli_main(
                ["context", "--component", "missing", "--query", "term"]
            )

        self.assertEqual(exit_code, ConfigurationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "ERROR: unknown component 'missing'\n")
        manifest_factory.assert_called_once()
        manifest.component.assert_called_once_with("missing")
        runtime_factory.assert_not_called()
        loader_factory.assert_not_called()
        resolver.assert_not_called()


class WorksetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    def test_control_tokens_do_not_trigger_terminology_matches(self) -> None:
        self.assertEqual(
            _plain_source("#LIGHT_BLUE##{underline}#%s#LAST##{normal}#").strip(),
            "",
        )

    def test_terminology_matches_source_tag_and_component_scope(self) -> None:
        items = [
            {
                "entry_id": "entity",
                "source": "dread",
                "source_tag": "entity name",
            },
            {
                "entry_id": "log",
                "source": "The dread attacks.",
                "source_tag": "log",
            },
        ]
        rows = [
            {
                "source": "dread",
                "target": "噩灵",
                "category": "T.GAME.ENTITY",
                "source_tag": "entity name",
                "status": "preferred",
                "scope": "core",
                "notes": "",
            },
            {
                "source": "dread",
                "target": "惊骇",
                "category": "T.GAME.ENTITY",
                "source_tag": "entity name",
                "status": "preferred",
                "scope": "dlc",
                "notes": "",
            },
        ]
        core_terms = _relevant_terms(rows, items, "tome")
        dlc_terms = _relevant_terms(rows, items, "orcs")
        self.assertEqual([term["target"] for term in core_terms], ["噩灵"])
        self.assertEqual(core_terms[0]["matched_entry_ids"], ["entity"])
        self.assertEqual([term["target"] for term in dlc_terms], ["惊骇"])

    def test_scope_groups_and_unknown_scope(self) -> None:
        self.assertEqual(
            DLC_COMPONENTS,
            frozenset(
                {"ashes-urhrok", "cults", "items-vault", "orcs", "possessors"}
            ),
        )
        self.assertEqual(
            ADDON_COMPONENTS,
            frozenset({"addon-dev", "items-vault", "possessors"}),
        )
        for component in ("tome", "items-vault", "possessors"):
            self.assertTrue(_scope_matches("global", component))
            self.assertTrue(_scope_matches("multi", component))
        for component in ADDON_COMPONENTS:
            self.assertTrue(_scope_matches("addon", component))
        self.assertFalse(_scope_matches("addon", "tome"))
        self.assertTrue(_scope_matches("core", "addon-dev"))
        self.assertFalse(_scope_matches("core", "items-vault"))
        for component in ("tome", "items-vault", "unknown-component"):
            self.assertFalse(_scope_matches("unsupported", component))

    def test_multi_term_is_visible_in_workset_and_quality(self) -> None:
        row = {
            "source": "shared term",
            "target": "共享术语",
            "category": "T.UI.LABEL",
            "domain": "ui",
            "source_tag": "_t",
            "status": "preferred",
            "scope": "multi",
            "notes": "fixture",
        }
        item = {
            "entry_id": "shared",
            "source": "A shared term appears.",
            "source_tag": "_t",
        }
        for component in ("tome", "orcs"):
            self.assertEqual(
                [term["target"] for term in _relevant_terms([row], [item], component)],
                ["共享术语"],
            )

        records, matcher, by_plain, nested_terms = quality_module._build_term_index(
            [row]
        )
        for component in ("tome", "orcs"):
            terms = quality_module._relevant_terms_for(
                "A shared term appears.",
                "_t",
                component,
                records,
                matcher,
                by_plain,
                nested_terms,
            )
            self.assertEqual([term["target"] for term in terms], ["共享术语"])

    def test_nil_and_empty_source_tags_are_distinct(self) -> None:
        self.assertTrue(_source_tag_matches("nil", None))
        self.assertFalse(_source_tag_matches("nil", ""))
        self.assertTrue(_source_tag_matches("", ""))
        self.assertFalse(_source_tag_matches("", None))
        self.assertTrue(_source_tag_matches("literal", "literal"))
        self.assertFalse(_source_tag_matches("literal", "other"))

        rows = [
            {
                "source": "tagged",
                "target": "nil target",
                "category": "T.TECH.INTERNAL",
                "domain": "tech",
                "source_tag": "nil",
                "status": "preferred",
                "scope": "global",
                "notes": "fixture",
            },
            {
                "source": "tagged",
                "target": "empty target",
                "category": "T.TECH.INTERNAL",
                "domain": "tech",
                "source_tag": "",
                "status": "preferred",
                "scope": "global",
                "notes": "fixture",
            },
        ]
        items = [
            {"entry_id": "nil", "source": "tagged", "source_tag": None},
            {"entry_id": "empty", "source": "tagged", "source_tag": ""},
        ]
        terms = _relevant_terms(rows, items, "tome")
        matched = {
            term["target"]: term["matched_entry_ids"] for term in terms
        }
        self.assertEqual(matched["nil target"], ["nil"])
        self.assertEqual(matched["empty target"], ["empty"])

    def test_workset_items_reject_empty_editorial_keys(self) -> None:
        base = {
            "entry_id": "unused",
            "component": "boot",
            "section": "fixture/dialog.lua",
            "source": "Source text",
            "source_tag": "_t",
        }
        for field in ("section", "source"):
            item = {**base, field: ""}
            with self.subTest(field=field), self.assertRaises(ValidationError):
                validate_workset_items("boot", [item])

    def test_workset_merge_report_path_must_stay_in_manifest_root(self) -> None:
        outside = self.manifest.root.parent / "outside-merge-report.json"
        with self.assertRaisesRegex(ValidationError, "inside the manifest root"):
            _resolve_manifest_path(self.manifest, outside, "workset merge_report")


class ProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    def _create_fixture(
        self, directory: Path
    ) -> tuple[dict[str, object], Path, Path]:
        return create_workset_fixture(self.manifest, directory)

    def test_json_object_schema_rejects_non_integer_versions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-schema-") as temporary:
            path = Path(temporary) / "proposal.json"
            for schema_version in (True, 1.0):
                with self.subTest(schema_version=schema_version):
                    path.write_text(
                        json.dumps({"schema_version": schema_version}),
                        encoding="utf-8",
                    )
                    with self.assertRaisesRegex(
                        ValidationError, "unsupported proposal schema"
                    ):
                        read_json_object(path, "proposal")

    def test_valid_proposal_is_content_addressed_and_linted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = self._create_fixture(Path(temporary))
            report = validate_proposal(
                self.manifest,
                workset_path=workset_path,
                proposal_path=proposal_path,
                allow_partial=False,
                strict=True,
            )
        self.assertTrue(report["ok"])
        self.assertEqual(report["coverage"]["proposed"], 1)
        self.assertEqual(report["errors"], 0)
        self.assertEqual(report["warnings"], 0)
        self.assertTrue(Path(report["validated_proposal"]).is_file())

    def test_changed_source_and_missing_format_argument_are_blocking(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = self._create_fixture(Path(temporary))
            proposal = json.loads(proposal_path.read_text())
            proposal["proposals"][0]["source"] = "tampered"
            proposal["proposals"][0]["target"] = "%s"
            proposal["proposals"][0]["args_order"] = None
            proposal_path.write_text(
                json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
            )
            report = validate_proposal(
                self.manifest,
                workset_path=workset_path,
                proposal_path=proposal_path,
                allow_partial=False,
                strict=False,
            )
        codes = {issue["code"] for issue in report["issues"]}
        self.assertFalse(report["ok"])
        self.assertIn("proposal-source-changed", codes)
        self.assertIn("format-mismatch", codes)
        self.assertNotIn("validated_proposal", report)

    def test_proposal_cannot_invent_special_runtime_options(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = self._create_fixture(Path(temporary))
            proposal = json.loads(proposal_path.read_text())
            proposal["proposals"][0]["special"] = {"invented": True}
            proposal_path.write_text(
                json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
            )
            report = validate_proposal(
                self.manifest,
                workset_path=workset_path,
                proposal_path=proposal_path,
                allow_partial=False,
                strict=False,
            )
        codes = {issue["code"] for issue in report["issues"]}
        self.assertFalse(report["ok"])
        self.assertIn("proposal-special-changed", codes)

    def test_proposal_special_rejects_nested_bool_int_type_drift(self) -> None:
        previous_special = {"outer": {"enabled": True, "values": [1, False]}}
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = create_workset_fixture(
                self.manifest,
                Path(temporary),
                previous_special=previous_special,
            )
            proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
            proposal["proposals"][0]["special"] = {
                "outer": {"enabled": 1, "values": [1, 0]}
            }
            proposal_path.write_text(
                json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
            )
            report = validate_proposal(
                self.manifest,
                workset_path=workset_path,
                proposal_path=proposal_path,
                allow_partial=False,
                strict=False,
            )

        codes = {issue["code"] for issue in report["issues"]}
        self.assertFalse(report["ok"])
        self.assertIn("proposal-special-changed", codes)

    def test_proposal_special_accepts_deep_equivalent_reordered_objects(self) -> None:
        previous_special = {
            "outer": {
                "enabled": True,
                "values": [1, {"wrapped": False, "label": "值"}],
            }
        }
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = create_workset_fixture(
                self.manifest,
                Path(temporary),
                previous_special=previous_special,
            )
            proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
            proposal["proposals"][0]["special"] = {
                "outer": {
                    "values": [1, {"label": "值", "wrapped": False}],
                    "enabled": True,
                }
            }
            proposal_path.write_text(
                json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
            )
            report = validate_proposal(
                self.manifest,
                workset_path=workset_path,
                proposal_path=proposal_path,
                allow_partial=False,
                strict=True,
            )

        self.assertTrue(report["ok"], report["issues"])
        self.assertEqual(report["errors"], 0)
        self.assertEqual(report["warnings"], 0)

    def test_proposal_args_order_still_rejects_boolean_indices(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = self._create_fixture(Path(temporary))
            proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
            proposal["proposals"][0]["args_order"] = [True, 1]
            proposal_path.write_text(
                json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
            )
            report = validate_proposal(
                self.manifest,
                workset_path=workset_path,
                proposal_path=proposal_path,
                allow_partial=False,
                strict=False,
            )

        codes = {issue["code"] for issue in report["issues"]}
        self.assertFalse(report["ok"])
        self.assertIn("proposal-args-order", codes)

    def test_tampered_workset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-proposal-test-") as temporary:
            _, workset_path, proposal_path = self._create_fixture(Path(temporary))
            workset = json.loads(workset_path.read_text())
            workset["items"][0]["source"] = "tampered"
            tampered_path = Path(temporary) / "tampered-workset.json"
            tampered_path.write_text(
                json.dumps(workset, ensure_ascii=False), encoding="utf-8"
            )
            with self.assertRaises(ValidationError):
                validate_proposal(
                    self.manifest,
                    workset_path=tampered_path,
                    proposal_path=proposal_path,
                    allow_partial=False,
                    strict=False,
                )


if __name__ == "__main__":
    unittest.main()
