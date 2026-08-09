from __future__ import annotations

import argparse
import copy
import contextlib
import csv
from dataclasses import replace
import hashlib
import importlib
import importlib.util
import io
import sys
import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
TEST_FIXTURE_BASE = ROOT / ".artifacts" / "i18n" / "test-fixtures"
TEST_FIXTURE_BASE.mkdir(parents=True, exist_ok=True)
_TEST_FIXTURE_DIRECTORY = tempfile.TemporaryDirectory(
    prefix="toolchain-", dir=TEST_FIXTURE_BASE
)
TEST_FIXTURE_ROOT = Path(_TEST_FIXTURE_DIRECTORY.name)

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import annotate_domains
import audit_dynamic
import audit_static
import classify_runtime_keys
import i18nlib.quality as quality_module
import review_diff
import scan_runtime_collisions
import smoke_release
from audit_static_rules import normalize_typo_pairs
from i18nlib import TOOL_VERSION
from i18nlib.config import Manifest, load_manifest
from i18nlib.context import resolve_context, validate_context_options
from i18nlib.build import _lua_string, build_addon_locale, build_full_locales
from i18nlib.cli import (
    _build as cli_build,
    _parser as cli_parser,
    _select_components,
    main as cli_main,
)
from i18nlib.errors import (
    AgentError,
    ConfigurationError,
    ExtractionError,
    ValidationError,
)
from i18nlib.extract import _normalized_definitions, extract_components
from i18nlib.git_source import GitRepository
from i18nlib.lint import (
    Policy,
    TERMINOLOGY_FIELDS,
    extract_format_tokens,
    lint_documents,
    lint_terminology,
    load_policy,
    stable_entry_id,
)
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.merge import classify_merge
from i18nlib.pi_agent import _copy_isolated_oauth_credential, run_pi_translation
from i18nlib.pi_file_review import (
    _git_worktree_snapshot,
    _parser as pi_file_review_parser,
    build_file_review_command,
    main as pi_file_review_main,
    run_pi_file_review,
)
from i18nlib.pi_remediate import _validate_remediation, run_pi_remediation
from i18nlib.pi_review import _validate_findings, run_pi_review
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
    _parser as pi_tmux_parser,
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
from i18nlib.proposal import read_json_object, validate_proposal
from i18nlib.quality import (
    ADJUDICATION_CONTRACT,
    ASSESSMENT_CONTRACT,
    SAMPLE_CONTRACT,
    DRY_RUN_CONTRACT,
    _match_findings,
    _weighted_kappa,
    build_report,
    build_inventory,
    compute_revision_id,
    compute_unit_id,
    generate_dry_run,
    generate_sample,
    load_quality_policy,
    load_taxonomy,
    run_report as run_quality_report,
    run_validation as run_quality_validation,
    structure_signature,
    validate_quality_run,
)
from i18nlib.review import (
    MAX_REVIEW_BATCH_SIZE,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    _bundle_id,
    _code_items,
    _git_diff,
    _git_status_paths,
    _is_public_review_path,
    _redact_absolute_paths,
    _review_index_id,
    _validate_findings_for_remediation,
    create_review_index,
    validate_review_bundle,
)
from i18nlib.runtime import LuaRuntime
from i18nlib.snapshot import read_snapshot
from i18nlib.workset import (
    ADDON_COMPONENTS,
    DLC_COMPONENTS,
    _plain_source,
    _relevant_terms,
    _resolve_manifest_path,
    _scope_matches,
    _source_tag_matches,
    create_workset,
    validate_workset_items,
)


EMPTY_POLICY = Policy(frozenset(), frozenset(), frozenset())
_UNSET = object()


def create_workset_fixture(
    manifest: object,
    directory: Path,
    *,
    previous_special: object = _UNSET,
) -> tuple[dict[str, object], Path, Path]:
    component = "boot"
    section = "fixture/dialog.lua"
    source = "%s has %d"
    source_tag = "tformat"
    item = {
        "entry_id": stable_entry_id(component, section, source, source_tag),
        "component": component,
        "section": section,
        "source": source,
        "source_tag": source_tag,
        "classification": "added",
        "origins": [
            {"document": "generated:fixture", "kind": "extracted", "line": 1}
        ],
    }
    if previous_special is not _UNSET:
        item["previous_special"] = previous_special
    fixture_root = TEST_FIXTURE_ROOT / directory.name
    fixture_root.mkdir(parents=True, exist_ok=True)
    merge_path = fixture_root / "merge.json"
    merge_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "merge_id": "a" * 64,
                "component": component,
                "untranslated": [item],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    workset = create_workset(
        manifest,
        merge_report_path=merge_path,
        limit=10,
        section_prefix=None,
        classification="all",
    )
    workset_path = Path(str(workset["output"]))
    proposal_path = directory / "proposal.json"
    proposal = json.loads(Path(str(workset["proposal_template"])).read_text())
    proposal["proposals"][0]["target"] = "%d 属于 %s"
    proposal["proposals"][0]["args_order"] = [2, 1]
    proposal_path.write_text(
        json.dumps(proposal, ensure_ascii=False), encoding="utf-8"
    )
    return workset, workset_path, proposal_path


class TestFixtureIsolationTests(unittest.TestCase):
    def test_import_in_child_process_uses_distinct_fixture_root(self) -> None:
        sentinel = TEST_FIXTURE_ROOT / "parent-sentinel"
        sentinel.write_text("parent fixture", encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import json\n"
                    "from tests.i18n import test_toolchain\n"
                    "print(json.dumps({\"fixture_root\": "
                    "str(test_toolchain.TEST_FIXTURE_ROOT)}))\n"
                ),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        child_fixture_root = Path(json.loads(completed.stdout)["fixture_root"])
        self.assertTrue(sentinel.is_file())
        self.assertNotEqual(child_fixture_root, TEST_FIXTURE_ROOT)
        self.assertEqual(child_fixture_root.parent, TEST_FIXTURE_BASE)


class GitRepositoryValidationTests(unittest.TestCase):
    commit = "a" * 40
    head = "b" * 40

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="git-validation-")
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name).resolve()
        with patch(
            "i18nlib.git_source.shutil.which", return_value="/usr/bin/git"
        ):
            self.repository = GitRepository(self.path)

    @staticmethod
    def _completed(
        returncode: int = 0, *, stdout: str = "", stderr: str = ""
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            ["git"], returncode, stdout=stdout, stderr=stderr
        )

    def _validation_results(
        self, status: subprocess.CompletedProcess[str] | None = None
    ) -> list[subprocess.CompletedProcess[str]]:
        results = [
            self._completed(stdout=f"{self.path}\n"),
            self._completed(stdout=f"{self.commit}\n"),
            self._completed(stdout=f"{self.head}\n"),
        ]
        if status is not None:
            results.append(status)
        return results

    @classmethod
    def _expected_calls(cls, *, include_status: bool) -> list[object]:
        calls = [
            call(["rev-parse", "--show-toplevel"], text=True),
            call(
                ["rev-parse", "--verify", f"{cls.commit}^{{commit}}"],
                text=True,
            ),
            call(["rev-parse", "--verify", "HEAD"], text=True),
        ]
        if include_status:
            calls.append(
                call(
                    ["status", "--porcelain", "--untracked-files=all"],
                    text=True,
                )
            )
        return calls

    def test_validate_rejects_failed_worktree_status(self) -> None:
        cases = (
            (
                "fatal: cannot read index\n",
                "ignored stdout\n",
                "fatal: cannot read index",
            ),
            (
                "",
                "",
                "git status exited with code 128 without an error message",
            ),
        )
        for stderr, stdout, expected_detail in cases:
            with self.subTest(stderr=stderr):
                status = self._completed(
                    128, stdout=stdout, stderr=stderr
                )
                with patch.object(
                    self.repository,
                    "_run",
                    side_effect=self._validation_results(status),
                ) as run:
                    with self.assertRaises(ConfigurationError) as raised:
                        self.repository.validate(self.commit)

                message = str(raised.exception)
                self.assertIn(str(self.path), message)
                self.assertIn(expected_detail, message)
                if stderr:
                    self.assertNotIn(stdout.strip(), message)
                self.assertEqual(
                    run.call_args_list,
                    self._expected_calls(include_status=True),
                )

    def test_validate_reports_clean_worktree(self) -> None:
        status = self._completed(stdout="")
        with patch.object(
            self.repository,
            "_run",
            side_effect=self._validation_results(status),
        ) as run:
            result = self.repository.validate(self.commit)

        self.assertEqual(result["path"], str(self.path))
        self.assertEqual(result["commit"], self.commit)
        self.assertEqual(result["head"], self.head)
        self.assertIs(result["clean"], True)
        self.assertIs(result["worktree_checked"], True)
        self.assertEqual(
            run.call_args_list, self._expected_calls(include_status=True)
        )

    def test_validate_reports_dirty_worktree(self) -> None:
        status = self._completed(stdout=" M tracked.lua\n?? new.lua\n")
        with patch.object(
            self.repository,
            "_run",
            side_effect=self._validation_results(status),
        ) as run:
            result = self.repository.validate(self.commit)

        self.assertIs(result["clean"], False)
        self.assertIs(result["worktree_checked"], True)
        self.assertEqual(
            run.call_args_list, self._expected_calls(include_status=True)
        )

    def test_validate_skips_worktree_status_when_disabled(self) -> None:
        with patch.object(
            self.repository,
            "_run",
            side_effect=self._validation_results(),
        ) as run:
            result = self.repository.validate(
                self.commit, check_worktree=False
            )

        self.assertIsNone(result["clean"])
        self.assertIs(result["worktree_checked"], False)
        self.assertEqual(
            run.call_args_list, self._expected_calls(include_status=False)
        )


class ManifestTests(unittest.TestCase):
    @staticmethod
    def _manifest_data() -> dict[str, object]:
        path = ROOT / "i18n" / "versions" / "tome-1.7.6.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _load_isolated_manifest(data: dict[str, object]) -> object:
        with tempfile.TemporaryDirectory(prefix="manifest-types-") as temporary:
            path = Path(temporary) / "tome-1.7.6.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return load_manifest(manifest_path=path)

    @staticmethod
    def _component_data(
        data: dict[str, object], component_id: str
    ) -> dict[str, object]:
        components = data["components"]
        assert isinstance(components, list)
        return next(
            component
            for component in components
            if isinstance(component, dict) and component.get("id") == component_id
        )

    def test_manifest_pins_current_release(self) -> None:
        manifest = load_manifest()
        self.assertEqual(manifest.version, "tome-1.7.6")
        self.assertEqual(
            manifest.repositories["engine"].commit,
            "624a67329fe2ad440c5b344785a9c73fcf22ae63",
        )
        self.assertEqual(manifest.component("tome").translation, "mod-tome.lua")
        self.assertTrue(manifest.component("tome").addon_eligible)
        self.assertFalse(manifest.component("boot").addon_eligible)
        self.assertEqual(
            manifest.protected_source_roots["dlc"].access,
            "lua-extractor-only",
        )
        self.assertEqual(manifest.protected_repositories, frozenset({"engine"}))
        self.assertEqual(
            {
                component.id
                for component in manifest.components
                if component.protected_source is not None
            },
            {"ashes-urhrok", "cults", "orcs"},
        )
        ashes = manifest.component("ashes-urhrok")
        self.assertIsNone(ashes.source_repository)
        self.assertEqual(ashes.sources, ())
        self.assertIsNotNone(ashes.protected_source)
        assert ashes.protected_source is not None
        self.assertEqual(ashes.protected_source.mount, "tome-ashes-urhrok")
        assert ashes.source_baseline is not None
        self.assertEqual(ashes.source_baseline.tdef_count, 999)
        self.assertEqual(
            ashes.source_baseline.kind, "protected-extraction-snapshot"
        )
        self.assertEqual(
            {
                layer.id: layer.status for layer in manifest.release_layers
            },
            {
                "core-addon": "releaseable",
                "dlc-addon": "baseline-pending",
                "legacy-lore-addon": "optional",
                "nullpack-addon": "optional",
            },
        )
        core_layer = next(
            layer for layer in manifest.release_layers if layer.id == "core-addon"
        )
        self.assertEqual(core_layer.components, ("tome",))
        self.assertEqual(core_layer.external_requirements, ())
        dlc_layer = next(
            layer for layer in manifest.release_layers if layer.id == "dlc-addon"
        )
        self.assertEqual(dlc_layer.components, ("ashes-urhrok", "cults", "orcs"))
        for component_id in ("items-vault", "possessors"):
            ignored = manifest.component(component_id)
            self.assertIsNone(ignored.protected_source)
            self.assertFalse(ignored.addon_eligible)
            self.assertTrue((manifest.root / ignored.translation).is_file())

    def test_manifest_integer_fields_reject_json_true(self) -> None:
        cases = (
            (
                "manifest.schema_version",
                lambda data: data.__setitem__("schema_version", True),
            ),
            (
                "extractor.max_stack",
                lambda data: data["extractor"].__setitem__("max_stack", True),
            ),
            (
                "source_baseline.tdef_count",
                lambda data: self._component_data(data, "ashes-urhrok")[
                    "source_baseline"
                ].__setitem__("tdef_count", True),
            ),
        )
        for field, mutate in cases:
            with self.subTest(field=field):
                data = self._manifest_data()
                mutate(data)
                with self.assertRaises(ConfigurationError) as raised:
                    self._load_isolated_manifest(data)
                self.assertIn(field, str(raised.exception))

    def test_manifest_boolean_fields_reject_strings_and_numbers(self) -> None:
        cases = (
            (
                "repositories.engine.required",
                lambda data, value: data["repositories"]["engine"].__setitem__(
                    "required", value
                ),
            ),
            (
                "extractor.preserve_duplicate_occurrences",
                lambda data, value: data["extractor"].__setitem__(
                    "preserve_duplicate_occurrences", value
                ),
            ),
            (
                "extract_by_default",
                lambda data, value: self._component_data(data, "example").__setitem__(
                    "extract_by_default", value
                ),
            ),
            (
                "addon_eligible",
                lambda data, value: self._component_data(data, "example").__setitem__(
                    "addon_eligible", value
                ),
            ),
        )
        for field, mutate in cases:
            for invalid_value in ("false", 0):
                with self.subTest(field=field, value=invalid_value):
                    data = self._manifest_data()
                    mutate(data, invalid_value)
                    with self.assertRaises(ConfigurationError) as raised:
                        self._load_isolated_manifest(data)
                    self.assertIn(field, str(raised.exception))

    def test_manifest_boolean_fields_preserve_json_false(self) -> None:
        data = self._manifest_data()
        data["repositories"]["engine"]["required"] = False
        data["extractor"]["preserve_duplicate_occurrences"] = False
        tome = self._component_data(data, "tome")
        tome["extract_by_default"] = False
        boot = self._component_data(data, "boot")
        boot["addon_eligible"] = False

        manifest = self._load_isolated_manifest(data)

        self.assertFalse(manifest.repositories["engine"].required)
        self.assertFalse(manifest.extractor.preserve_duplicate_occurrences)
        self.assertFalse(manifest.component("tome").extract_by_default)
        self.assertFalse(manifest.component("boot").addon_eligible)

    def test_pinned_official_locale_is_a_regular_blob(self) -> None:
        manifest = load_manifest()
        repository = GitRepository(manifest.repository_path("engine"))
        component = manifest.component("boot")
        assert component.official_locale is not None
        data = repository.read_blob(
            manifest.repositories["engine"].commit,
            component.official_locale,
        )
        self.assertTrue(data.startswith(b'locale "zh_hans"'))


class DoctorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()

    @classmethod
    def _manifest(cls, root: Path, copy_fragment: str) -> object:
        component = replace(
            cls.base_manifest.component("ashes-urhrok"),
            translation="canonical.lua",
            copy_fragment=copy_fragment,
        )
        return replace(
            cls.base_manifest,
            root=root,
            components=(component,),
            manual_definitions=("manual.lua",),
            terminology="terminology.tsv",
            policy="policy.json",
        )

    @staticmethod
    def _write_files(root: Path, *relative_paths: str) -> None:
        for relative_path in relative_paths:
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("-- fixture\n", encoding="utf-8")

    def test_missing_copy_fragment_fails_before_expensive_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-doctor-missing-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, "fragment.lua")
            self._write_files(
                root,
                "terminology.tsv",
                "policy.json",
                "canonical.lua",
                "manual.lua",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch("i18nlib.cli._manifest", return_value=manifest),
                patch("i18nlib.cli.LuaRuntime") as runtime_class,
                patch("i18nlib.cli.GitRepository") as repository_class,
                patch("i18nlib.cli.probe_protected_component") as protected_probe,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["doctor"])

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn(f"missing: {root / 'fragment.lua'}", stderr.getvalue())
        self.assertNotIn("not regular files:", stderr.getvalue())
        runtime_class.assert_not_called()
        repository_class.assert_not_called()
        protected_probe.assert_not_called()

    def test_missing_and_non_file_paths_are_reported_separately(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-doctor-non-file-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, "fragment.lua")
            self._write_files(
                root,
                "terminology.tsv",
                "canonical.lua",
                "manual.lua",
            )
            (root / "fragment.lua").mkdir()
            stderr = io.StringIO()

            with (
                patch("i18nlib.cli._manifest", return_value=manifest),
                patch("i18nlib.cli.LuaRuntime") as runtime_class,
                patch("i18nlib.cli.GitRepository") as repository_class,
                patch("i18nlib.cli.probe_protected_component") as protected_probe,
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["doctor"])

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(
            stderr.getvalue(),
            "ERROR: required localization files are invalid: "
            f"missing: {root / 'policy.json'}; "
            f"not regular files: {root / 'fragment.lua'}\n",
        )
        runtime_class.assert_not_called()
        repository_class.assert_not_called()
        protected_probe.assert_not_called()

    def test_declared_copy_fragment_allows_normal_doctor_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-doctor-valid-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, "fragment.lua")
            self._write_files(
                root,
                "terminology.tsv",
                "policy.json",
                "canonical.lua",
                "fragment.lua",
                "manual.lua",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch("i18nlib.cli._manifest", return_value=manifest),
                patch("i18nlib.cli.LuaRuntime") as runtime_class,
                patch("i18nlib.cli.GitRepository") as repository_class,
                patch(
                    "i18nlib.cli.probe_protected_component", return_value=True
                ) as protected_probe,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                runtime = runtime_class.return_value
                runtime.doctor.return_value = {
                    "lua_version": "Lua 5.1",
                    "luajit_version": "LuaJIT fixture",
                    "lpeg_rock_version": "0.10.2-1",
                    "lpeg_runtime_version": "0.10",
                }
                repository_class.return_value.validate.return_value = {
                    "path": "/fixture/repository",
                    "clean": True,
                }
                exit_code = cli_main(["doctor", "--json"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertTrue(json.loads(stdout.getvalue())["ok"])
        runtime.doctor.assert_called_once_with()
        repository_class.return_value.validate.assert_called()
        protected_probe.assert_called_once_with(
            manifest, runtime, manifest.components[0]
        )


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
        self.assertEqual(sum(report["counts"].values()), 12)
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
        self.assertEqual(len(report["rows"]), 693)
        self.assertEqual(sum(report["counts"].values()), 693)
        self.assertEqual(report["unmapped_count"], 0)
        self.assertEqual(report["declared_domain_mismatch_count"], 6)
        self.assertIs(report["ok"], True)


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
            terminology = root / "terminology.tsv"
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
            terminology = root / "terminology.tsv"
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
            terminology = root / "terminology.tsv"
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
            terminology = root / "terminology.tsv"
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
            terminology = root / "terminology.tsv"
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
            terminology = root / "terminology.tsv"
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


class ReviewScopeTests(unittest.TestCase):
    def _assert_review_validation_has_no_side_effects(
        self,
        manifest: Manifest,
        *,
        batch_size: object,
        include_translations: object,
        include_code: object,
        expected_error: str,
    ) -> None:
        with (
            patch("i18nlib.review.create_run_directory") as create_directory,
            patch("i18nlib.review.LuaRuntime") as runtime_class,
            patch("i18nlib.review.LocaleLoader") as loader_class,
            patch(
                "i18nlib.review._write_translation_bundles"
            ) as write_translations,
            patch("i18nlib.review._translation_items") as scan_translations,
            patch("i18nlib.review._write_code_bundles") as write_code,
            patch("i18nlib.review._code_items") as scan_code,
            patch("i18nlib.review.write_json") as write_json_mock,
            self.assertRaisesRegex(ValidationError, expected_error),
        ):
            create_review_index(
                manifest,
                batch_size=batch_size,  # type: ignore[arg-type]
                include_translations=include_translations,  # type: ignore[arg-type]
                include_code=include_code,  # type: ignore[arg-type]
            )

        create_directory.assert_not_called()
        runtime_class.assert_not_called()
        loader_class.assert_not_called()
        write_translations.assert_not_called()
        scan_translations.assert_not_called()
        write_code.assert_not_called()
        scan_code.assert_not_called()
        write_json_mock.assert_not_called()

    def test_create_review_index_rejects_non_integer_batch_size_before_side_effects(
        self,
    ) -> None:
        manifest = load_manifest()
        for batch_size in (True, 1.0, "1"):
            with self.subTest(batch_size=batch_size):
                self._assert_review_validation_has_no_side_effects(
                    manifest,
                    batch_size=batch_size,
                    include_translations=True,
                    include_code=False,
                    expected_error="review batch size must be an integer",
                )

    def test_create_review_index_rejects_out_of_range_batch_size_before_side_effects(
        self,
    ) -> None:
        manifest = load_manifest()
        for batch_size in (0, -1, MAX_REVIEW_BATCH_SIZE + 1):
            with self.subTest(batch_size=batch_size):
                self._assert_review_validation_has_no_side_effects(
                    manifest,
                    batch_size=batch_size,
                    include_translations=True,
                    include_code=False,
                    expected_error=(
                        "review batch size must be between 1 and "
                        f"{MAX_REVIEW_BATCH_SIZE}"
                    ),
                )

    def test_create_review_index_rejects_non_boolean_scopes_before_side_effects(
        self,
    ) -> None:
        manifest = load_manifest()
        invalid_values = (0, 1, "false", None)
        for parameter in ("include_translations", "include_code"):
            for invalid_value in invalid_values:
                with self.subTest(parameter=parameter, value=invalid_value):
                    arguments: dict[str, object] = {
                        "batch_size": 1,
                        "include_translations": True,
                        "include_code": True,
                    }
                    arguments[parameter] = invalid_value
                    self._assert_review_validation_has_no_side_effects(
                        manifest,
                        batch_size=arguments["batch_size"],
                        include_translations=arguments["include_translations"],
                        include_code=arguments["include_code"],
                        expected_error=f"review {parameter} must be a boolean",
                    )

    def test_create_review_index_requires_a_true_scope_before_side_effects(
        self,
    ) -> None:
        self._assert_review_validation_has_no_side_effects(
            load_manifest(),
            batch_size=1,
            include_translations=False,
            include_code=False,
            expected_error="review must include translations or code",
        )

    def test_create_review_index_accepts_batch_size_boundaries(self) -> None:
        manifest = load_manifest()
        run_directory = manifest.root / ".artifacts" / "i18n" / "review-fixture"
        for batch_size in (1, MAX_REVIEW_BATCH_SIZE):
            with (
                self.subTest(batch_size=batch_size),
                patch(
                    "i18nlib.review.create_run_directory",
                    return_value=run_directory,
                ),
                patch(
                    "i18nlib.review._write_code_bundles",
                    return_value=([], 0),
                ) as write_code,
                patch("i18nlib.review.write_json"),
            ):
                create_review_index(
                    manifest,
                    batch_size=batch_size,
                    include_translations=False,
                    include_code=True,
                )

            write_code.assert_called_once_with(
                run_directory, manifest, batch_size
            )

    def _code_review_repository(self, root: Path) -> Path:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        tracked = root / "tools" / "fixture.py"
        tracked.parent.mkdir(parents=True)
        tracked.write_text("one\ntwo\nthree\n", encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(root), "add", "tools/fixture.py"], check=True
        )
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
        return tracked

    def test_pi_agent_analysis_is_in_public_review_scope(self) -> None:
        self.assertTrue(_is_public_review_path("pi-agent-analysis.md"))
        self.assertFalse(_is_public_review_path("private/pi-agent-analysis.md"))

    def test_fixed_public_review_roots_are_in_scope(self) -> None:
        for root in (".agents", ".codex", "docs", "i18n", "tools", "tests"):
            with self.subTest(root=root):
                self.assertTrue(_is_public_review_path(root))
                self.assertTrue(_is_public_review_path(f"{root}/fixture.txt"))
        self.assertFalse(_is_public_review_path(".github/fixture.txt"))

    def test_manifest_copy_and_manual_files_enter_code_items_and_bundle(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-manifest-files-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            original = load_manifest()
            component = replace(
                original.component("engine"),
                translation="canonical.lua",
                copy_fragment="engine.copy.lua",
            )
            manifest = replace(
                original,
                root=root,
                components=(component,),
                manual_definitions=("_tdef_append.lua",),
            )
            baseline_files = {
                "engine.copy.lua": "copy baseline\n",
                "_tdef_append.lua": "manual baseline\n",
                "canonical.lua": "translation baseline\n",
                "undeclared.lua": "undeclared baseline\n",
                "tools/lua/load_locale.lua": "-- loader bridge fixture\n",
            }
            for relative, content in baseline_files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "--all"], check=True)
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
                    "manifest files",
                ],
                check=True,
            )

            (root / "engine.copy.lua").write_text("copy staged\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "engine.copy.lua"], check=True
            )
            (root / "_tdef_append.lua").write_text(
                "manual unstaged\n", encoding="utf-8"
            )
            (root / "canonical.lua").write_text(
                "translation changed\n", encoding="utf-8"
            )
            (root / "undeclared.lua").write_text(
                "undeclared changed\n", encoding="utf-8"
            )

            self.assertTrue(_is_public_review_path("engine.copy.lua", manifest))
            self.assertTrue(_is_public_review_path("_tdef_append.lua", manifest))
            self.assertFalse(_is_public_review_path("canonical.lua", manifest))
            self.assertFalse(_is_public_review_path("undeclared.lua", manifest))

            paths = _git_status_paths(root, manifest)
            items, _ = _code_items(root, manifest)
            index = create_review_index(
                manifest,
                batch_size=100,
                include_translations=False,
                include_code=True,
            )
            bundle_files: list[dict[str, object]] = []
            for bundle in index["bundles"]:
                payload = json.loads(
                    Path(bundle["path"]).read_text(encoding="utf-8")
                )
                bundle_files.extend(payload["files"])

        self.assertEqual(
            {(status, path) for status, path, _ in paths},
            {("M ", "engine.copy.lua"), (" M", "_tdef_append.lua")},
        )
        self.assertEqual(
            {item["path"] for item in items},
            {"engine.copy.lua", "_tdef_append.lua"},
        )
        self.assertEqual(
            {item["path"] for item in bundle_files},
            {"engine.copy.lua", "_tdef_append.lua"},
        )

    def test_review_cli_requires_an_explicit_scope(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                cli_parser().parse_args(["review"])
        arguments = cli_parser().parse_args(
            ["review", "--scope", "code", "--scope", "translations"]
        )
        self.assertEqual(arguments.scope, ["code", "translations"])

    def test_code_only_review_does_not_initialize_lua(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-code-only-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.write_text("changed\ntwo\nthree\n", encoding="utf-8")
            manifest = replace(load_manifest(), root=root)

            with (
                patch(
                    "i18nlib.review.LuaRuntime",
                    side_effect=AssertionError("code review initialized LuaRuntime"),
                ) as runtime_class,
                patch(
                    "i18nlib.review.LocaleLoader",
                    side_effect=AssertionError("code review initialized LocaleLoader"),
                ) as loader_class,
            ):
                index = create_review_index(
                    manifest,
                    batch_size=100,
                    include_translations=False,
                    include_code=True,
                )

            bundle = json.loads(
                Path(index["bundles"][0]["path"]).read_text(encoding="utf-8")
            )
            stored_index = json.loads(
                Path(index["index"]).read_text(encoding="utf-8")
            )

        runtime_class.assert_not_called()
        loader_class.assert_not_called()
        self.assertEqual(
            index["scope"],
            {
                "translations": False,
                "code": True,
                "protected_sources": False,
            },
        )
        self.assertEqual(len(index["bundles"]), 1)
        self.assertEqual(index["bundles"][0]["kind"], "code")
        self.assertEqual(stored_index, index)
        self.assertEqual(bundle["kind"], "code")
        self.assertEqual(
            [item["path"] for item in bundle["files"]], ["tools/fixture.py"]
        )

    def test_translation_enabled_review_initializes_one_loader_pair(self) -> None:
        manifest = load_manifest()
        run_directory = manifest.root / ".artifacts" / "i18n" / "review-fixture"
        translation_bundles = [
            {
                "bundle_id": "translation-fixture",
                "kind": "translations",
                "component": "boot",
                "offset": 0,
                "count": 1,
                "total": 1,
                "path": str(run_directory / "translation.json"),
            }
        ]
        code_bundles = [
            {
                "bundle_id": "code-fixture",
                "kind": "code",
                "offset": 0,
                "count": 1,
                "total": 1,
                "path": str(run_directory / "code.json"),
            }
        ]

        with (
            patch(
                "i18nlib.review.create_run_directory",
                return_value=run_directory,
            ) as create_directory,
            patch("i18nlib.review.LuaRuntime") as runtime_class,
            patch("i18nlib.review.LocaleLoader") as loader_class,
            patch(
                "i18nlib.review._write_translation_bundles",
                return_value=translation_bundles,
            ) as write_translations,
            patch(
                "i18nlib.review._write_code_bundles",
                return_value=(code_bundles, 0),
            ) as write_code,
            patch("i18nlib.review.write_json") as write_json_mock,
        ):
            index = create_review_index(
                manifest,
                batch_size=100,
                include_translations=True,
                include_code=True,
            )

        runtime_class.assert_called_once_with(manifest)
        loader_class.assert_called_once_with(runtime_class.return_value)
        create_directory.assert_called_once_with(manifest.root, "review")
        write_translations.assert_called_once_with(
            run_directory,
            manifest,
            loader_class.return_value,
            100,
        )
        write_code.assert_called_once_with(run_directory, manifest, 100)
        self.assertEqual(index["bundles"], translation_bundles + code_bundles)
        write_json_mock.assert_called_once_with(
            run_directory / "review-index.json", index
        )

    def test_code_review_includes_staged_only_modification(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-staged-modify-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.write_text("staged\ntwo\nthree\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/fixture.py"], check=True
            )

            items, _ = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "M ")
        self.assertIn("--- a/tools/fixture.py", items[0]["diff"])
        self.assertIn("-one", items[0]["diff"])
        self.assertIn("+staged", items[0]["diff"])
        self.assertNotIn("--- /dev/null", items[0]["diff"])

    def test_code_review_preserves_dev_null_for_staged_new_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-staged-new-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            staged = root / "tools" / "staged.py"
            staged.write_text(
                'source = "/Users/fixture/private.txt"\n', encoding="utf-8"
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/staged.py"], check=True
            )

            items, redactions = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "A ")
        self.assertIn("new file mode", items[0]["diff"])
        self.assertIn("--- /dev/null", items[0]["diff"])
        self.assertIn("+++ b/tools/staged.py", items[0]["diff"])
        self.assertNotIn("/Users/fixture", items[0]["diff"])
        self.assertIn("<redacted-absolute-path>", items[0]["diff"])
        self.assertEqual(redactions, 1)

    def test_code_review_includes_staged_only_deletion(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-staged-delete-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.unlink()
            subprocess.run(
                ["git", "-C", str(root), "add", "-u", "tools/fixture.py"],
                check=True,
            )

            items, redactions = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "D ")
        self.assertIn("deleted file mode", items[0]["diff"])
        self.assertIn("--- a/tools/fixture.py", items[0]["diff"])
        self.assertIn("+++ /dev/null", items[0]["diff"])
        self.assertIn("-one", items[0]["diff"])
        self.assertEqual(redactions, 0)

    def test_code_review_combines_staged_and_unstaged_changes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-mixed-") as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.write_text("staged\ntwo\nthree\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/fixture.py"], check=True
            )
            tracked.write_text("staged\nunstaged\nthree\n", encoding="utf-8")

            items, _ = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "MM")
        self.assertIn("-one", items[0]["diff"])
        self.assertIn("+staged", items[0]["diff"])
        self.assertIn("-two", items[0]["diff"])
        self.assertIn("+unstaged", items[0]["diff"])
        self.assertNotIn("--- /dev/null", items[0]["diff"])

    def test_code_review_synthesizes_addition_only_for_untracked_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-untracked-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            untracked = root / "tools" / "untracked.py"
            untracked.write_text("untracked\n", encoding="utf-8")

            raw_diff = _git_diff(root, "tools/untracked.py", untracked=True)
            items, redactions = _code_items(root)

        self.assertTrue(raw_diff.startswith("--- /dev/null\n"))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/untracked.py")
        self.assertEqual(items[0]["status"], "??")
        self.assertIn("--- /dev/null", items[0]["diff"])
        self.assertIn("+++ b/tools/untracked.py", items[0]["diff"])
        self.assertIn("untracked\n", items[0]["diff"])
        self.assertEqual(redactions, 0)

    def test_code_review_includes_unicode_untracked_path(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-unicode-untracked-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            untracked = root / "tools" / "中文.py"
            untracked.write_text("unicode path\n", encoding="utf-8")

            items, _ = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/中文.py")
        self.assertEqual(items[0]["status"], "??")
        self.assertIn("+++ b/tools/中文.py", items[0]["diff"])

    def test_git_status_paths_preserves_literal_rename_marker(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-literal-arrow-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            ordinary = root / "tools" / "literal -> marker.py"
            ordinary.write_text("before\n", encoding="utf-8")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "add",
                    "--",
                    "tools/literal -> marker.py",
                ],
                check=True,
            )
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
                    "literal arrow fixture",
                ],
                check=True,
            )
            ordinary.write_text("after\n", encoding="utf-8")

            paths = _git_status_paths(root)

        self.assertEqual(paths, [(" M", "tools/literal -> marker.py", None)])

    def test_code_review_includes_both_sides_of_public_rename(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-tracked-rename-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            destination = root / "tools" / "renamed.py"
            tracked.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [
                ("R ", "tools/renamed.py", "tools/fixture.py"),
            ],
        )
        self.assertEqual(len(items), 2)
        by_path = {item["path"]: item for item in items}
        self.assertEqual(set(by_path), {"tools/fixture.py", "tools/renamed.py"})
        self.assertEqual(by_path["tools/fixture.py"]["status"], "R ")
        self.assertIn("deleted file mode", by_path["tools/fixture.py"]["diff"])
        self.assertIn("--- a/tools/fixture.py", by_path["tools/fixture.py"]["diff"])
        self.assertEqual(by_path["tools/renamed.py"]["status"], "R ")
        self.assertIn("new file mode", by_path["tools/renamed.py"]["diff"])
        self.assertIn("+++ b/tools/renamed.py", by_path["tools/renamed.py"]["diff"])

    def test_code_review_keeps_rename_source_and_untracked_replacement(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-rename-replacement-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            destination = root / "tools" / "renamed.py"
            tracked.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )
            tracked.write_text("replacement\n", encoding="utf-8")

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [
                ("R ", "tools/renamed.py", "tools/fixture.py"),
                ("??", "tools/fixture.py", None),
            ],
        )
        self.assertEqual(
            [(item["status"], item["path"]) for item in items],
            [
                ("R ", "tools/renamed.py"),
                ("R ", "tools/fixture.py"),
                ("??", "tools/fixture.py"),
            ],
        )
        renamed, removed, replacement = items
        self.assertIn("+++ b/tools/renamed.py", renamed["diff"])
        self.assertIn("deleted file mode", removed["diff"])
        self.assertIn("--- a/tools/fixture.py", removed["diff"])
        self.assertIn("-one", removed["diff"])
        self.assertIn("+++ b/tools/fixture.py", replacement["diff"])
        self.assertIn("replacement\n", replacement["diff"])

    def test_code_review_keeps_public_source_when_rename_leaves_scope(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-rename-outside-scope-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            destination = root / "private" / "renamed.py"
            destination.parent.mkdir()
            tracked.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [("D ", "tools/fixture.py", None)],
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/fixture.py")
        self.assertEqual(items[0]["status"], "D ")
        self.assertIn("deleted file mode", items[0]["diff"])
        self.assertIn("--- a/tools/fixture.py", items[0]["diff"])
        self.assertNotIn("private/renamed.py", items[0]["diff"])

    def test_code_review_keeps_public_destination_when_rename_enters_scope(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-rename-into-scope-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            source = root / "private" / "fixture.py"
            source.parent.mkdir()
            tracked.rename(source)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )
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
                    "private fixture",
                ],
                check=True,
            )
            destination = root / "tools" / "renamed.py"
            source.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [("A ", "tools/renamed.py", None)],
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/renamed.py")
        self.assertEqual(items[0]["status"], "A ")
        self.assertIn("new file mode", items[0]["diff"])
        self.assertIn("+++ b/tools/renamed.py", items[0]["diff"])
        self.assertNotIn("private/fixture.py", items[0]["diff"])

    def test_git_status_paths_keeps_copy_source_and_reviews_public_copy(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-tracked-copy-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            subprocess.run(
                ["git", "-C", str(root), "config", "status.renames", "copies"],
                check=True,
            )
            destination = root / "tests" / "copied.py"
            destination.parent.mkdir()
            destination.write_bytes(tracked.read_bytes())
            tracked.write_text("one\ntwo\nthree\nsource changed\n", encoding="utf-8")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "add",
                    "tests/copied.py",
                    "tools/fixture.py",
                ],
                check=True,
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [
                ("C ", "tests/copied.py", "tools/fixture.py"),
                ("M ", "tools/fixture.py", None),
            ],
        )
        self.assertEqual(len(items), 2)
        by_path = {item["path"]: item for item in items}
        self.assertEqual(set(by_path), {"tests/copied.py", "tools/fixture.py"})
        self.assertEqual(by_path["tests/copied.py"]["status"], "C ")
        self.assertIn("+++ b/tests/copied.py", by_path["tests/copied.py"]["diff"])
        self.assertEqual(by_path["tools/fixture.py"]["status"], "M ")
        self.assertIn("+source changed", by_path["tools/fixture.py"]["diff"])

    def test_git_status_paths_preserves_tab_and_newline(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-control-paths-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            expected = [
                ("??", "tools/tab\tname.py", None),
                ("??", "tools/line\nname.py", None),
            ]
            for _, relative, _ in expected:
                (root / relative).write_text("control path\n", encoding="utf-8")

            paths = _git_status_paths(root)

        self.assertCountEqual(paths, expected)


class ReviewDiffTests(unittest.TestCase):
    TERMINOLOGY_HEADER = (
        "source\ttarget\tcategory\tsource_tag\tstatus\tscope\tnotes\n"
    ).encode("utf-8")

    @staticmethod
    def _commit_repository(root: Path, files: dict[str, bytes]) -> str:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        subprocess.run(["git", "-C", str(root), "add", "--all"], check=True)
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
                "baseline",
            ],
            check=True,
        )
        return review_diff._resolve_baseline_tree(root, "HEAD")

    @staticmethod
    def _initialize_repository(root: Path) -> str:
        return ReviewDiffTests._commit_repository(
            root,
            {
                "locale.lua": b"baseline locale\n",
                "empty.lua": b"",
            },
        )

    @staticmethod
    def _translation(
        source: str,
        target: str,
        *,
        section: str = "fixture.lua",
        source_tag: str | None = None,
        args_order: object = None,
        special: object = None,
    ) -> dict[str, object]:
        return {
            "section": section,
            "source": source,
            "target": target,
            "source_tag": source_tag,
            "args_order": args_order,
            "special": special,
            "line": 1,
        }

    def _review_manifest_fixture(
        self,
        root: Path,
        locales: tuple[tuple[str, str, bytes, bytes], ...],
        *,
        terminology: bytes | None = None,
    ) -> object:
        original = load_manifest()
        baseline_files = {
            relative: baseline
            for _, relative, baseline, _ in locales
        }
        baseline_files["tools/lua/load_locale.lua"] = (
            TOOLS / "lua" / "load_locale.lua"
        ).read_bytes()
        baseline_files["terminology.tsv"] = (
            self.TERMINOLOGY_HEADER
            if terminology is None
            else terminology
        )
        self._commit_repository(root, baseline_files)
        for _, relative, _, current in locales:
            (root / relative).write_bytes(current)
        components = tuple(
            replace(
                original.components[index],
                id=component_id,
                translation=relative,
            )
            for index, (component_id, relative, _, _) in enumerate(locales)
        )
        return replace(
            original,
            root=root,
            components=components,
            terminology="terminology.tsv",
        )

    @staticmethod
    def _run_review_diff(
        root: Path,
        manifest: object,
        output: Path,
    ) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch.object(review_diff, "ROOT", root),
            patch.object(review_diff, "load_manifest", return_value=manifest),
            patch.object(review_diff.signal, "alarm"),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = review_diff.main(
                ["--baseline", "HEAD", "--out-dir", str(output)]
            )
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def _assert_failed_run_is_clean(
        self,
        *,
        exit_code: int,
        stdout: str,
        stderr: str,
        output: Path,
    ) -> None:
        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("error: ", stderr)
        self.assertNotIn("Traceback", stderr)
        self.assertFalse(output.exists())
        self.assertEqual(
            list(output.parent.glob(f".{output.name}.staging-*")),
            [],
        )

    def test_invalid_second_current_locale_does_not_publish_first_bundle(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        changed = b'section("fixture.lua")\nt("source", "new")\n'
        invalid = b'section("broken"\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-parse-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (
                    ("first", "locale/first.lua", baseline, changed),
                    ("second", "locale/second.lua", baseline, invalid),
                ),
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("Lua locale load failed for locale/second.lua", stderr)

    def test_invalid_baseline_locale_is_controlled_and_not_published(self) -> None:
        invalid = b'section("broken"\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-baseline-parse-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", invalid, current),),
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("Lua locale load failed for locale/fixture.lua", stderr)

    def test_invalid_terminology_is_controlled_and_not_published(self) -> None:
        locale = b'section("fixture.lua")\nt("source", "target")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-terminology-parse-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", locale, locale),),
                terminology=b"source\ttarget\nsource\ttarget\n",
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("terminology header is invalid", stderr)

    def test_success_preserves_artifact_bytes_ids_and_final_paths(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-artifact-semantics-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 0, stderr)
            self.assertEqual(stderr, "")
            index_path = output / "review-index.json"
            index_bytes = index_path.read_bytes()
            index = json.loads(index_bytes)
            self.assertEqual(len(index["bundles"]), 1)
            bundle_record = index["bundles"][0]
            bundle_path = Path(bundle_record["path"])
            self.assertEqual(
                bundle_path,
                output
                / "translations"
                / "fixture"
                / f'{bundle_record["bundle_id"]}.json',
            )
            bundle_bytes = bundle_path.read_bytes()
            bundle = json.loads(bundle_bytes)

            bundle_identity = dict(bundle)
            bundle_identity.pop("bundle_id")
            self.assertEqual(
                bundle["bundle_id"], review_diff._bundle_id(bundle_identity)
            )
            index_identity = dict(index)
            index_identity.pop("review_id")
            self.assertEqual(
                index["review_id"],
                review_diff._review_index_id(index_identity),
            )
            self.assertEqual(
                bundle_bytes,
                json.dumps(bundle, ensure_ascii=False, indent=1).encode("utf-8"),
            )
            self.assertEqual(
                index_bytes,
                json.dumps(index, ensure_ascii=False, indent=1).encode("utf-8"),
            )
            self.assertNotIn(b".staging-", bundle_bytes)
            self.assertNotIn(b".staging-", index_bytes)
            self.assertEqual(
                stdout,
                "\n".join(
                    (
                        "baseline: HEAD",
                        "changed entries: 1, bundles: 1",
                        f'review_id: {index["review_id"]}',
                        f"run_dir: {output}",
                        "",
                    )
                ),
            )

    def test_staged_write_failure_leaves_no_final_or_staging_directory(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-staged-write-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            output = root / "output"
            write_json = review_diff._write_json

            def fail_on_index(path: Path, payload: dict[str, object]) -> None:
                if path.name == "review-index.json":
                    raise OSError("fixture staged index failure")
                write_json(path, payload)

            with patch.object(
                review_diff, "_write_json", side_effect=fail_on_index
            ):
                exit_code, stdout, stderr = self._run_review_diff(
                    root, manifest, output
                )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("fixture staged index failure", stderr)

    def test_existing_explicit_output_is_rejected_without_overwrite(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-existing-output-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            output = root / "output"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 2)
            self.assertEqual(stdout, "")
            self.assertNotIn("Traceback", stderr)
            self.assertIn("refusing to overwrite", stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(output.iterdir()), [sentinel])

    def test_output_parent_creation_failure_is_controlled(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-parent-failure-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            blocked_parent = root / "blocked-parent"
            blocked_parent.write_text("not a directory", encoding="utf-8")
            output = blocked_parent / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 2)
            self.assertEqual(stdout, "")
            self.assertIn("error: ", stderr)
            self.assertNotIn("Traceback", stderr)
            self.assertFalse(output.exists())

    def test_invalid_baseline_returns_nonzero_with_clear_error(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-invalid-"
        ) as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            stderr = io.StringIO()
            alarm = Mock()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff.signal, "alarm", alarm),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(["--baseline", "missing-baseline"])

        self.assertEqual(exit_code, 2)
        self.assertIn("error: cannot resolve baseline", stderr.getvalue())
        self.assertIn("as a commit or tree", stderr.getvalue())
        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_cli_rejects_out_of_range_batch_sizes_before_side_effects(self) -> None:
        invalid_sizes = (0, -1, review_diff.MAX_REVIEW_BATCH_SIZE + 1)
        for batch_size in invalid_sizes:
            with self.subTest(batch_size=batch_size), tempfile.TemporaryDirectory(
                prefix="tome4-review-diff-batch-invalid-"
            ) as temporary:
                root = Path(temporary)
                output = root / "output"
                stderr = io.StringIO()
                alarm = Mock()
                with (
                    patch.object(review_diff, "ROOT", root),
                    patch.object(
                        review_diff, "_resolve_baseline_tree"
                    ) as resolve_baseline,
                    patch.object(review_diff.signal, "alarm", alarm),
                    contextlib.redirect_stderr(stderr),
                    self.assertRaises(SystemExit) as raised,
                ):
                    review_diff.main(
                        [
                            "--baseline",
                            "missing-baseline",
                            "--batch-size",
                            str(batch_size),
                            "--out-dir",
                            str(output),
                        ]
                    )

                self.assertEqual(raised.exception.code, 2)
                self.assertIn(
                    "review batch size must be between 1 and "
                    f"{review_diff.MAX_REVIEW_BATCH_SIZE}",
                    stderr.getvalue(),
                )
                resolve_baseline.assert_not_called()
                self.assertFalse(output.exists())
                self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_cli_accepts_minimum_and_maximum_batch_sizes(self) -> None:
        manifest = load_manifest()
        component = manifest.component("example")
        manifest = replace(manifest, components=(component,))
        current_document = LocaleLoader(LuaRuntime(manifest)).load_path(
            manifest.root / component.translation,
            logical_path=component.translation,
        )
        expected_count = len(current_document.translations)
        self.assertGreater(expected_count, 0)

        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-batch-boundary-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(root, {"unrelated.txt": b"fixture\n"})
            for batch_size in (1, review_diff.MAX_REVIEW_BATCH_SIZE):
                with self.subTest(batch_size=batch_size):
                    output = root / f"output-{batch_size}"
                    stderr = io.StringIO()
                    alarm = Mock()
                    with (
                        patch.object(review_diff, "ROOT", root),
                        patch.object(
                            review_diff, "load_manifest", return_value=manifest
                        ),
                        patch.object(review_diff.signal, "alarm", alarm),
                        contextlib.redirect_stdout(io.StringIO()),
                        contextlib.redirect_stderr(stderr),
                    ):
                        exit_code = review_diff.main(
                            [
                                "--baseline",
                                "HEAD",
                                "--batch-size",
                                str(batch_size),
                                "--out-dir",
                                str(output),
                            ]
                        )

                    self.assertEqual(exit_code, 0, stderr.getvalue())
                    self.assertEqual(stderr.getvalue(), "")
                    index = json.loads(
                        (output / "review-index.json").read_text(encoding="utf-8")
                    )
                    self.assertEqual(
                        sum(bundle["count"] for bundle in index["bundles"]),
                        expected_count,
                    )
                    self.assertTrue(
                        all(
                            1 <= bundle["count"] <= batch_size
                            for bundle in index["bundles"]
                        )
                    )
                    self.assertEqual(
                        alarm.call_args_list, [call(600), call(0)]
                    )

    def test_alarm_is_cancelled_when_review_generation_raises(self) -> None:
        alarm = Mock()
        with (
            patch.object(
                review_diff, "_resolve_baseline_tree", return_value="0" * 40
            ),
            patch.object(
                review_diff,
                "load_manifest",
                side_effect=RuntimeError("fixture failure"),
            ),
            patch.object(review_diff.signal, "alarm", alarm),
            self.assertRaisesRegex(RuntimeError, "fixture failure"),
        ):
            review_diff.main(["--baseline", "HEAD"])

        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_missing_current_translation_returns_nonzero_without_output(self) -> None:
        original = load_manifest()
        component = replace(
            original.component("example"),
            id="missing-current",
            translation="locale/missing.lua",
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-missing-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(root, {"unrelated.txt": b"fixture\n"})
            manifest = replace(original, root=root, components=(component,))
            output = root / "nested" / "output"
            stderr = io.StringIO()
            alarm = Mock()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff, "load_manifest", return_value=manifest),
                patch.object(review_diff.signal, "alarm", alarm),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(
                    ["--baseline", "HEAD", "--out-dir", str(output)]
                )

            self.assertFalse(output.exists())

        self.assertEqual(exit_code, 2)
        self.assertIn("missing or not regular files", stderr.getvalue())
        self.assertIn("component 'missing-current'", stderr.getvalue())
        self.assertIn("locale/missing.lua", stderr.getvalue())
        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_translation_preflight_aggregates_all_invalid_paths(self) -> None:
        original = load_manifest()
        template = original.component("example")
        components = (
            replace(
                template,
                id="missing-alpha",
                translation="locale/missing-alpha.lua",
            ),
            replace(
                template,
                id="not-regular-beta",
                translation="locale/not-regular-beta.lua",
            ),
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-invalid-"
        ) as temporary:
            root = Path(temporary)
            (root / "locale" / "not-regular-beta.lua").mkdir(parents=True)
            manifest = replace(original, root=root, components=components)

            with self.assertRaises(review_diff.ReviewDiffError) as caught:
                review_diff._preflight_translation_paths(manifest)

        message = str(caught.exception)
        self.assertIn("component 'missing-alpha': locale/missing-alpha.lua", message)
        self.assertIn(
            "component 'not-regular-beta': locale/not-regular-beta.lua",
            message,
        )
        self.assertLess(message.index("missing-alpha"), message.index("not-regular-beta"))

    def test_cli_continues_when_all_current_translation_files_exist(self) -> None:
        original = load_manifest()
        component = original.component("example")
        manifest = replace(original, components=(component,))
        translation_path = manifest.root / component.translation
        self.assertTrue(translation_path.is_file())
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-complete-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(
                root, {component.translation: translation_path.read_bytes()}
            )
            output = root / "output"
            stderr = io.StringIO()
            alarm = Mock()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff, "load_manifest", return_value=manifest),
                patch.object(review_diff.signal, "alarm", alarm),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(
                    ["--baseline", "HEAD", "--out-dir", str(output)]
                )

            index = json.loads(
                (output / "review-index.json").read_text(encoding="utf-8")
            )

        self.assertEqual(exit_code, 0, stderr.getvalue())
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(index["bundles"], [])
        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_unreadable_baseline_blob_returns_nonzero_with_clear_error(self) -> None:
        manifest = load_manifest()
        component = manifest.component("example")
        manifest = replace(manifest, components=(component,))
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-unreadable-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(
                root,
                {component.translation: b"baseline locale\n"},
            )
            object_name = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "rev-parse",
                    f"HEAD:{component.translation}",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            object_path = (
                root / ".git" / "objects" / object_name[:2] / object_name[2:]
            )
            self.assertTrue(object_path.is_file())
            object_path.unlink()

            output = root / "output"
            stderr = io.StringIO()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff, "load_manifest", return_value=manifest),
                patch.object(review_diff.signal, "alarm"),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(
                    ["--baseline", "HEAD", "--out-dir", str(output)]
                )
            self.assertFalse((output / "review-index.json").exists())

        self.assertEqual(exit_code, 2)
        self.assertIn("error: cannot read baseline path", stderr.getvalue())

    def test_baseline_blob_preserves_content_and_empty_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-blob-"
        ) as temporary:
            root = Path(temporary)
            tree = self._initialize_repository(root)

            content = review_diff._read_baseline_blob(root, tree, "locale.lua")
            empty = review_diff._read_baseline_blob(root, tree, "empty.lua")

        self.assertEqual(content, b"baseline locale\n")
        self.assertEqual(empty, b"")

    def test_baseline_blob_returns_none_only_for_missing_path(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-missing-"
        ) as temporary:
            root = Path(temporary)
            tree = self._initialize_repository(root)

            missing = review_diff._read_baseline_blob(root, tree, "new-locale.lua")

        self.assertIsNone(missing)

    def test_baseline_git_read_failure_is_not_treated_as_missing(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-read-failure-"
        ) as temporary:
            root = Path(temporary)
            self._initialize_repository(root)

            with self.assertRaisesRegex(
                review_diff.ReviewDiffError, "cannot inspect baseline path"
            ):
                review_diff._read_baseline_blob(root, "0" * 40, "locale.lua")

    def test_new_translation_file_produces_all_bundle_items(self) -> None:
        current = [
            self._translation("first", "第一"),
            self._translation("second", "第二"),
        ]

        items = review_diff._changed_translation_items("fixture", current, None)

        self.assertEqual([item["ordinal"] for item in items], [0, 1])
        self.assertEqual([item["source"] for item in items], ["first", "second"])
        self.assertTrue(all(item["component"] == "fixture" for item in items))

    def test_target_only_change_produces_bundle_item(self) -> None:
        baseline = [self._translation("changed", "旧译")]
        current = [self._translation("changed", "新译")]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["target"], "新译")

    def test_cross_section_runtime_key_change_is_not_masked(self) -> None:
        baseline = [
            self._translation("same", "甲", section="a.lua"),
            self._translation("same", "乙", section="b.lua"),
        ]
        current = [
            self._translation("same", "乙", section="a.lua"),
            self._translation("same", "乙", section="b.lua"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(
            [
                (item["ordinal"], item["section"], item["target"])
                for item in items
            ],
            [(0, "a.lua", "乙")],
        )

    def test_section_only_move_produces_bundle_item(self) -> None:
        baseline = [self._translation("moved", "译文", section="old.lua")]
        current = [self._translation("moved", "译文", section="new.lua")]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["section"], "new.lua")

    def test_identical_duplicate_occurrences_consume_distinct_baselines(self) -> None:
        baseline = [
            self._translation("duplicate", "译文"),
            self._translation("duplicate", "译文"),
        ]
        current = [
            self._translation("duplicate", "译文"),
            self._translation("duplicate", "译文"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(items, [])

    def test_added_duplicate_occurrence_produces_one_bundle_item(self) -> None:
        baseline = [self._translation("duplicate", "译文")]
        current = [
            self._translation("duplicate", "译文"),
            self._translation("duplicate", "译文"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual([item["ordinal"] for item in items], [1])

    def test_duplicate_semantic_change_consumes_only_one_matching_baseline(self) -> None:
        baseline = [
            self._translation("duplicate", "甲"),
            self._translation("duplicate", "乙"),
        ]
        current = [
            self._translation("duplicate", "乙"),
            self._translation("duplicate", "乙"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(
            [(item["ordinal"], item["target"]) for item in items],
            [(1, "乙")],
        )

    def test_args_order_only_change_produces_bundle_item(self) -> None:
        baseline = [self._translation("changed", "译文")]
        current = [
            self._translation("changed", "译文", args_order=[2, 1])
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["args_order"], [2, 1])

    def test_special_only_change_produces_bundle_item(self) -> None:
        # Lua/JSON and revision identity distinguish these types; Python's
        # native deep equality does not because True == 1.
        baseline = [
            self._translation("changed", "译文", special={"mode": True})
        ]
        current = [
            self._translation("changed", "译文", special={"mode": 1})
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["special"], {"mode": 1})

    def test_deep_equivalent_special_is_skipped(self) -> None:
        baseline = [
            self._translation(
                "same",
                "译文",
                special={
                    "enabled": True,
                    "nested": {
                        "right": 2,
                        "items": [{"last": "b", "first": "a"}],
                    },
                },
            ),
        ]
        current = [
            self._translation(
                "same",
                "译文",
                special={
                    "nested": {
                        "items": [{"first": "a", "last": "b"}],
                        "right": 2,
                    },
                    "enabled": True,
                },
            ),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(items, [])

    def test_combined_semantic_changes_preserve_full_bundle_item(self) -> None:
        baseline = [
            self._translation(
                "changed %s %d",
                "旧译 %s %d",
                args_order=[1, 2],
                special={"wrap": False},
            )
        ]
        current_entry = self._translation(
            "changed %s %d",
            "新译 %d %s",
            args_order=[2, 1],
            special={"wrap": True},
        )

        items = review_diff._changed_translation_items(
            "fixture", [current_entry], baseline
        )

        self.assertEqual(
            items,
            [
                {
                    "item_id": review_diff._entry_id("fixture", 0, current_entry),
                    "component": "fixture",
                    "ordinal": 0,
                    "section": "fixture.lua",
                    "source": "changed %s %d",
                    "target": "新译 %d %s",
                    "source_tag": None,
                    "args_order": [2, 1],
                    "special": {"wrap": True},
                    "line": 1,
                }
            ],
        )

    def test_identical_runtime_semantics_are_skipped(self) -> None:
        baseline = [
            self._translation(
                "same",
                "译文",
                args_order=[2, 1],
                special={"wrap": True},
            )
        ]
        current = [
            self._translation(
                "same",
                "译文",
                args_order=[2, 1],
                special={"wrap": True},
            )
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(items, [])

    def test_loader_normalization_drives_semantic_comparison(self) -> None:
        manifest = load_manifest()
        loader = LocaleLoader(LuaRuntime(manifest))
        baseline = loader.load_bytes(
            b'''section("fixture.lua")
t("changed %s %d", "translation %d %s", "tformat", {1, 2}, {nested={z=2, a=1}, flags={"a", "b"}})
t("same", "translation", nil, nil, {nested={z=2, a=1}, flags={"a", "b"}})
''',
            logical_path="baseline.lua",
        )
        current = loader.load_bytes(
            b'''section("fixture.lua")
t("changed %s %d", "translation %d %s", "tformat", {2, 1}, {flags={"a", "b"}, nested={a=1, z=2}})
t("same", "translation", nil, nil, {flags={"a", "b"}, nested={a=1, z=2}})
''',
            logical_path="current.lua",
        )

        items = review_diff._changed_translation_items(
            "fixture", current.translations, baseline.translations
        )

        self.assertEqual([item["source"] for item in items], ["changed %s %d"])
        self.assertEqual(items[0]["args_order"], [2, 1])
        self.assertEqual(
            items[0]["special"],
            {"flags": ["a", "b"], "nested": {"a": 1, "z": 2}},
        )

    def test_cli_handles_missing_empty_and_unchanged_baseline_files(self) -> None:
        manifest = load_manifest()
        component = manifest.component("example")
        manifest = replace(manifest, components=(component,))
        translation_path = manifest.root / component.translation
        current_document = LocaleLoader(LuaRuntime(manifest)).load_path(
            translation_path,
            logical_path=component.translation,
        )
        expected = [
            (entry["source"], entry["target"], entry["source_tag"])
            for entry in current_document.translations
        ]
        self.assertTrue(expected)

        cases = (
            ("missing", {"unrelated.txt": b"fixture\n"}, expected),
            ("empty", {component.translation: b""}, expected),
            (
                "unchanged",
                {component.translation: translation_path.read_bytes()},
                [],
            ),
        )
        for label, baseline_files, expected_entries in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix=f"tome4-review-diff-cli-{label}-"
            ) as temporary:
                root = Path(temporary)
                self._commit_repository(root, baseline_files)
                output = root / "output"
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    patch.object(review_diff, "ROOT", root),
                    patch.object(review_diff, "load_manifest", return_value=manifest),
                    patch.object(review_diff.signal, "alarm"),
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    exit_code = review_diff.main(
                        [
                            "--baseline",
                            "HEAD",
                            "--batch-size",
                            str(review_diff.MAX_REVIEW_BATCH_SIZE),
                            "--out-dir",
                            str(output),
                        ]
                    )

                self.assertEqual(exit_code, 0, stderr.getvalue())
                self.assertEqual(stderr.getvalue(), "")
                index = json.loads(
                    (output / "review-index.json").read_text(encoding="utf-8")
                )
                items = []
                for bundle in index["bundles"]:
                    payload = json.loads(
                        Path(bundle["path"]).read_text(encoding="utf-8")
                    )
                    items.extend(payload["items"])
                actual = [
                    (item["source"], item["target"], item["source_tag"])
                    for item in items
                ]
                self.assertEqual(actual, expected_entries)
                self.assertIn(
                    f"changed entries: {len(expected_entries)}", stdout.getvalue()
                )


class PublishPreflightTests(unittest.TestCase):
    def test_direct_commit_without_apply_fails_before_dependencies(self) -> None:
        import i18nlib.publish as publish_module

        with (
            patch.object(publish_module, "build_addon_locale") as build,
            patch.object(publish_module, "_official_locale_keys") as official_keys,
            patch.object(publish_module, "_dlc_overlay_entries") as dlc_entries,
            patch.object(publish_module, "_render_addon_locale") as renderer,
            patch.object(publish_module, "subprocess") as git_subprocess,
        ):
            with self.assertRaisesRegex(
                ValidationError, "commit=True requires apply=True"
            ):
                publish_module.publish_addon(
                    None,
                    None,
                    apply=False,
                    bump=True,
                    commit=True,
                )

        build.assert_not_called()
        official_keys.assert_not_called()
        dlc_entries.assert_not_called()
        renderer.assert_not_called()
        git_subprocess.run.assert_not_called()

    def test_cli_commit_without_apply_fails_before_manifest_and_runtime(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("i18nlib.cli._inject_public_dlc_env"),
            patch("i18nlib.cli._manifest") as manifest_factory,
            patch("i18nlib.cli.LuaRuntime") as runtime_factory,
            patch("i18nlib.cli.LocaleLoader") as loader_factory,
            patch("i18nlib.cli.publish_addon") as publish,
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = cli_main(["publish", "--commit"])

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            stderr.getvalue(),
            "ERROR: publish --commit requires --apply\n",
        )
        manifest_factory.assert_not_called()
        runtime_factory.assert_not_called()
        loader_factory.assert_not_called()
        publish.assert_not_called()

    def test_release_layout_fails_before_build_loader_and_git(self) -> None:
        import i18nlib.publish as publish_module

        for missing in ("root", "locale", "init"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory(
                prefix=f"tome4-publish-missing-{missing}-"
            ) as temporary:
                addon_root = Path(temporary) / "addon"
                locale_path = addon_root / "data" / "locales" / "zh_hans.lua"
                init_path = addon_root / "init.lua"
                if missing != "root":
                    addon_root.mkdir(parents=True)
                    if missing != "locale":
                        locale_path.parent.mkdir(parents=True)
                        locale_path.write_text(
                            'locale "zh_hans"\n', encoding="utf-8"
                        )
                    if missing != "init":
                        init_path.write_text(
                            "addon_version = {0,0,1}\n", encoding="utf-8"
                        )

                manifest = Mock()
                manifest.repositories = {"addon": object()}
                manifest.repository_path.return_value = addon_root
                manifest.components = (Mock(id="tome"),)
                loader = Mock(spec=LocaleLoader)
                with (
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module, "_official_locale_keys"
                    ) as official_keys,
                    patch.object(
                        publish_module, "_dlc_overlay_entries"
                    ) as dlc_entries,
                    patch.object(
                        publish_module, "_render_addon_locale"
                    ) as renderer,
                    patch.object(publish_module, "subprocess") as git_subprocess,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"release repository (?:not found|layout mismatch)",
                    ):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=True,
                            commit=True,
                        )

                build.assert_not_called()
                official_keys.assert_not_called()
                dlc_entries.assert_not_called()
                renderer.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                git_subprocess.run.assert_not_called()

    def test_release_layout_rejects_symlink_publish_files_before_build(self) -> None:
        import i18nlib.publish as publish_module

        for symlink_name in ("locale", "init"):
            with self.subTest(symlink=symlink_name), tempfile.TemporaryDirectory(
                prefix=f"tome4-publish-symlink-{symlink_name}-"
            ) as temporary:
                addon_root = Path(temporary) / "addon"
                locale_path = addon_root / "data" / "locales" / "zh_hans.lua"
                init_path = addon_root / "init.lua"
                locale_path.parent.mkdir(parents=True)
                locale_path.write_text('locale "zh_hans"\n', encoding="utf-8")
                init_path.write_text(
                    "addon_version = {0,0,1}\n",
                    encoding="utf-8",
                )
                selected_path = locale_path if symlink_name == "locale" else init_path
                target_path = selected_path.with_name(f"real-{selected_path.name}")
                selected_path.replace(target_path)
                selected_path.symlink_to(target_path.name)
                subprocess.run(
                    ["git", "init", "-q"],
                    cwd=addon_root,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                manifest = Mock()
                manifest.repositories = {"addon": object()}
                manifest.repository_path.return_value = addon_root
                manifest.components = (Mock(id="tome"),)
                loader = Mock(spec=LocaleLoader)
                with (
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module,
                        "_official_locale_keys",
                    ) as official_keys,
                    patch.object(
                        publish_module,
                        "_dlc_overlay_entries",
                    ) as dlc_entries,
                    patch.object(
                        publish_module,
                        "_render_addon_locale",
                    ) as renderer,
                    patch.object(publish_module, "subprocess") as git_subprocess,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"publish files must be regular files, not symbolic links",
                    ):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=True,
                            commit=True,
                        )

                build.assert_not_called()
                official_keys.assert_not_called()
                dlc_entries.assert_not_called()
                renderer.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                git_subprocess.run.assert_not_called()


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


def _component_selection_document(
    logical_path: str, source: str | None = None
) -> LocaleDocument:
    records: tuple[dict[str, object], ...] = ()
    if source is not None:
        records = (
            {
                "kind": "translation",
                "section": logical_path,
                "source": source,
                "target": f"translated {source}",
                "source_tag": None,
                "args_order": None,
                "special": None,
            },
        )
    return LocaleDocument(
        logical_path=logical_path,
        sha256="0" * 64,
        records=records,
    )


class CliLightweightPreflightTests(unittest.TestCase):
    def test_unknown_components_fail_before_runtime_and_downstream_work(self) -> None:
        cases = (
            ("lint", ["lint", "--component", "missing"]),
            ("status", ["status", "--component", "missing"]),
            (
                "merge",
                [
                    "merge",
                    "--component",
                    "missing",
                    "--snapshot",
                    "unused.jsonl",
                ],
            ),
        )
        for command, arguments in cases:
            with self.subTest(command=command):
                manifest = Mock()
                manifest.component.side_effect = ConfigurationError(
                    "unknown component 'missing'"
                )
                runtime = Mock(spec=LuaRuntime)
                stdout = io.StringIO()
                stderr = io.StringIO()

                with (
                    patch("i18nlib.cli._inject_public_dlc_env"),
                    patch(
                        "i18nlib.cli._manifest", return_value=manifest
                    ) as manifest_factory,
                    patch(
                        "i18nlib.cli.load_policy"
                    ) as load_policy_mock,
                    patch(
                        "i18nlib.cli.LuaRuntime", return_value=runtime
                    ) as runtime_factory,
                    patch("i18nlib.cli.LocaleLoader") as loader_factory,
                    patch("i18nlib.cli.lint_documents") as lint_documents_mock,
                    patch("i18nlib.cli.lint_terminology") as lint_terms,
                    patch("i18nlib.cli.status_report") as build_status,
                    patch("i18nlib.cli.run_merge") as merge,
                    patch("i18nlib.cli.create_run_directory") as create_run,
                    patch("i18nlib.cli.write_json") as write_json_mock,
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    exit_code = cli_main(arguments)

                self.assertEqual(exit_code, ConfigurationError.exit_code)
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(
                    stderr.getvalue(), "ERROR: unknown component 'missing'\n"
                )
                manifest_factory.assert_called_once()
                manifest.component.assert_called_once_with("missing")
                load_policy_mock.assert_not_called()
                runtime_factory.assert_not_called()
                runtime.doctor.assert_not_called()
                loader_factory.assert_not_called()
                lint_documents_mock.assert_not_called()
                lint_terms.assert_not_called()
                build_status.assert_not_called()
                merge.assert_not_called()
                create_run.assert_not_called()
                write_json_mock.assert_not_called()

    def test_lint_policy_error_fails_after_selection_but_before_runtime(self) -> None:
        component = SimpleNamespace(id="known")
        manifest = Mock()
        manifest.component.return_value = component
        runtime = Mock(spec=LuaRuntime)
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch("i18nlib.cli._inject_public_dlc_env"),
            patch(
                "i18nlib.cli._manifest", return_value=manifest
            ) as manifest_factory,
            patch(
                "i18nlib.cli.load_policy",
                side_effect=ConfigurationError("invalid lint policy"),
            ) as load_policy_mock,
            patch(
                "i18nlib.cli.LuaRuntime", return_value=runtime
            ) as runtime_factory,
            patch("i18nlib.cli.LocaleLoader") as loader_factory,
            patch("i18nlib.cli.lint_documents") as lint_documents_mock,
            patch("i18nlib.cli.lint_terminology") as lint_terms,
            patch("i18nlib.cli.create_run_directory") as create_run,
            patch("i18nlib.cli.write_json") as write_json_mock,
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = cli_main(
                [
                    "lint",
                    "--component",
                    "known",
                    "--component",
                    "known",
                ]
            )

        self.assertEqual(exit_code, ConfigurationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "ERROR: invalid lint policy\n")
        manifest_factory.assert_called_once()
        manifest.component.assert_called_once_with("known")
        load_policy_mock.assert_called_once_with(manifest)
        runtime_factory.assert_not_called()
        runtime.doctor.assert_not_called()
        loader_factory.assert_not_called()
        lint_documents_mock.assert_not_called()
        lint_terms.assert_not_called()
        create_run.assert_not_called()
        write_json_mock.assert_not_called()

    def test_valid_commands_resolve_once_before_runtime(self) -> None:
        cases = (
            (
                "lint",
                [
                    "lint",
                    "--component",
                    "known",
                    "--component",
                    "known",
                    "--json",
                ],
                [
                    "manifest",
                    "component",
                    "policy",
                    "runtime",
                    "doctor",
                    "loader",
                    "lint-canonical",
                    "lint-copy-fragment",
                    "terminology",
                ],
            ),
            (
                "status",
                [
                    "status",
                    "--component",
                    "known",
                    "--component",
                    "known",
                    "--json",
                ],
                [
                    "manifest",
                    "component",
                    "runtime",
                    "doctor",
                    "loader",
                    "status",
                ],
            ),
            (
                "merge",
                [
                    "merge",
                    "--component",
                    "known",
                    "--snapshot",
                    "unused.jsonl",
                    "--json",
                ],
                [
                    "manifest",
                    "component",
                    "runtime",
                    "doctor",
                    "loader",
                    "merge",
                ],
            ),
        )
        for command, arguments, expected_events in cases:
            with self.subTest(command=command):
                events: list[str] = []
                component = SimpleNamespace(
                    id="known",
                    translation="known.lua",
                    copy_fragment=None,
                )
                manifest = Mock()
                manifest.root = Path("/fixture")
                manifest.version = "fixture"
                manifest.terminology = "terminology.tsv"

                def resolve_component(identifier: str) -> object:
                    events.append("component")
                    self.assertEqual(identifier, "known")
                    return component

                manifest.component.side_effect = resolve_component
                runtime = Mock(spec=LuaRuntime)
                runtime.doctor.side_effect = lambda: events.append("doctor")
                loader = Mock(spec=LocaleLoader)
                loader.load_path.return_value = _component_selection_document(
                    "known.lua", "Known"
                )

                def load_manifest_for_test(_arguments: object) -> object:
                    events.append("manifest")
                    return manifest

                def load_policy_for_test(_manifest: object) -> Policy:
                    events.append("policy")
                    return EMPTY_POLICY

                def make_runtime(_manifest: object) -> Mock:
                    events.append("runtime")
                    return runtime

                def make_loader(_runtime: object) -> Mock:
                    events.append("loader")
                    return loader

                def lint_for_test(
                    _documents: object,
                    _policy: object,
                    *,
                    require_nonempty: bool,
                ) -> tuple[list[object], dict[str, object]]:
                    events.append(
                        "lint-canonical"
                        if require_nonempty
                        else "lint-copy-fragment"
                    )
                    return (
                        [],
                        {
                            "translations": 1 if require_nonempty else 0,
                            "components": {"known": 1}
                            if require_nonempty
                            else {},
                            "duplicate_runtime_keys": 0,
                        },
                    )

                with (
                    patch("i18nlib.cli._inject_public_dlc_env"),
                    patch(
                        "i18nlib.cli._manifest",
                        side_effect=load_manifest_for_test,
                    ) as manifest_factory,
                    patch(
                        "i18nlib.cli.load_policy",
                        side_effect=load_policy_for_test,
                    ) as load_policy_mock,
                    patch(
                        "i18nlib.cli.LuaRuntime", side_effect=make_runtime
                    ) as runtime_factory,
                    patch(
                        "i18nlib.cli.LocaleLoader", side_effect=make_loader
                    ) as loader_factory,
                    patch(
                        "i18nlib.cli.lint_documents",
                        side_effect=lint_for_test,
                    ) as lint_documents_mock,
                    patch(
                        "i18nlib.cli.lint_terminology",
                        side_effect=lambda _path: (
                            events.append("terminology") or ([], {"rows": 0})
                        ),
                    ) as lint_terms,
                    patch(
                        "i18nlib.cli.status_report",
                        side_effect=lambda *_args: (
                            events.append("status") or {"components": []}
                        ),
                    ) as build_status,
                    patch(
                        "i18nlib.cli.run_merge",
                        side_effect=lambda *_args, **_kwargs: (
                            events.append("merge") or {"ok": True}
                        ),
                    ) as merge,
                    patch(
                        "i18nlib.cli.create_run_directory",
                        return_value=Path("/fixture/run"),
                    ),
                    patch("i18nlib.cli.write_json"),
                    patch("i18nlib.cli._print_json"),
                ):
                    self.assertEqual(cli_main(arguments), 0)

                self.assertEqual(events, expected_events)
                manifest_factory.assert_called_once()
                manifest.component.assert_called_once_with("known")
                runtime_factory.assert_called_once_with(manifest)
                runtime.doctor.assert_called_once_with()
                loader_factory.assert_called_once_with(runtime)
                if command == "lint":
                    load_policy_mock.assert_called_once_with(manifest)
                    self.assertEqual(lint_documents_mock.call_count, 2)
                    lint_terms.assert_called_once_with(
                        Path("/fixture/terminology.tsv")
                    )
                    build_status.assert_not_called()
                    merge.assert_not_called()
                elif command == "status":
                    load_policy_mock.assert_not_called()
                    lint_documents_mock.assert_not_called()
                    lint_terms.assert_not_called()
                    build_status.assert_called_once_with(
                        manifest, loader, [component]
                    )
                    merge.assert_not_called()
                else:
                    load_policy_mock.assert_not_called()
                    lint_documents_mock.assert_not_called()
                    lint_terms.assert_not_called()
                    build_status.assert_not_called()
                    merge.assert_called_once_with(
                        manifest,
                        loader,
                        component,
                        new_snapshot_path=Path("unused.jsonl"),
                        base_snapshot_path=None,
                    )


class ComponentSelectionTests(unittest.TestCase):
    def test_explicit_selection_deduplicates_ids_in_first_seen_order(self) -> None:
        first = SimpleNamespace(id="first")
        second = SimpleNamespace(id="second")
        manifest = Mock()
        manifest.component.side_effect = {"first": first, "second": second}.__getitem__

        selected = _select_components(
            manifest,
            ["second", "first", "second", "first"],
            default="lint",
        )

        self.assertEqual(selected, [second, first])
        self.assertEqual(
            manifest.component.call_args_list,
            [call("second"), call("first")],
        )

    def test_default_manifest_selections_are_unchanged(self) -> None:
        first = SimpleNamespace(
            id="first", extract_by_default=False, official_locale="first.lua"
        )
        second = SimpleNamespace(
            id="second", extract_by_default=True, official_locale=None
        )
        third = SimpleNamespace(
            id="third", extract_by_default=True, official_locale="third.lua"
        )
        manifest = Mock(components=(first, second, third))

        self.assertEqual(
            _select_components(manifest, [], default="extract"),
            [second, third],
        )
        self.assertEqual(
            _select_components(manifest, [], default="status"),
            [first, third],
        )
        self.assertEqual(
            _select_components(manifest, [], default="lint"),
            [first, second, third],
        )
        manifest.component.assert_not_called()

    def test_build_command_deduplicates_explicit_components_for_each_profile(
        self,
    ) -> None:
        for profile in ("full", "addon"):
            with self.subTest(profile=profile):
                first = SimpleNamespace(
                    id="first",
                    addon_eligible=True,
                    full_output="first.lua",
                )
                second = SimpleNamespace(
                    id="second",
                    addon_eligible=True,
                    full_output="second.lua",
                )
                manifest = Mock()
                manifest.component.side_effect = {
                    "first": first,
                    "second": second,
                }.__getitem__
                runtime = Mock()
                loader = Mock(spec=LocaleLoader)
                arguments = argparse.Namespace(
                    component=["second", "first", "second"],
                    profile=profile,
                    json=True,
                    require_complete=False,
                )
                full_report = {
                    "components": [],
                    "run_directory": "/artifacts/full",
                }
                addon_report = {"complete": True}

                with (
                    patch("i18nlib.cli._manifest", return_value=manifest),
                    patch("i18nlib.cli.LuaRuntime", return_value=runtime),
                    patch("i18nlib.cli.LocaleLoader", return_value=loader),
                    patch(
                        "i18nlib.cli.build_full_locales",
                        return_value=full_report,
                    ) as full_build,
                    patch(
                        "i18nlib.cli.build_addon_locale",
                        return_value=addon_report,
                    ) as addon_build,
                    patch("i18nlib.cli._print_json"),
                ):
                    self.assertEqual(cli_build(arguments), 0)

                self.assertEqual(
                    manifest.component.call_args_list,
                    [call("second"), call("first")],
                )
                runtime.doctor.assert_called_once_with()
                if profile == "full":
                    full_build.assert_called_once_with(
                        manifest, loader, [second, first]
                    )
                    addon_build.assert_not_called()
                else:
                    addon_build.assert_called_once_with(
                        manifest,
                        loader,
                        [second, first],
                        include_external_requirements=False,
                    )
                    full_build.assert_not_called()

    def test_invalid_explicit_build_selections_fail_before_runtime_and_io(
        self,
    ) -> None:
        eligible = SimpleNamespace(
            id="eligible",
            addon_eligible=True,
            full_output="eligible.lua",
        )
        no_full_output = SimpleNamespace(
            id="no-full-output",
            addon_eligible=True,
            full_output=None,
        )
        non_eligible = SimpleNamespace(
            id="non-eligible",
            addon_eligible=False,
            full_output="non-eligible.lua",
        )
        cases = (
            (
                "full invalid first",
                "full",
                [no_full_output, eligible],
                r"component 'no-full-output' has no full_output mapping",
            ),
            (
                "full invalid later",
                "full",
                [eligible, no_full_output],
                r"component 'no-full-output' has no full_output mapping",
            ),
            (
                "addon invalid first",
                "addon",
                [non_eligible, eligible],
                r"addon build requires addon-eligible components; "
                r"not eligible: non-eligible",
            ),
            (
                "addon invalid later",
                "addon",
                [eligible, non_eligible],
                r"addon build requires addon-eligible components; "
                r"not eligible: non-eligible",
            ),
        )
        for label, profile, selected, expected_error in cases:
            with self.subTest(case=label):
                manifest = Mock(components=tuple(selected))
                manifest.component.side_effect = {
                    component.id: component for component in selected
                }.__getitem__
                arguments = argparse.Namespace(
                    component=[component.id for component in selected],
                    profile=profile,
                    json=True,
                    require_complete=False,
                )
                with (
                    patch("i18nlib.cli._manifest", return_value=manifest),
                    patch("i18nlib.cli.LuaRuntime") as runtime_type,
                    patch("i18nlib.cli.LocaleLoader") as loader_type,
                    patch("i18nlib.cli.build_full_locales") as full_build,
                    patch("i18nlib.cli.build_addon_locale") as addon_build,
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build._compose_full_locale") as compose,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(ValidationError, expected_error):
                        cli_build(arguments)

                runtime_type.assert_not_called()
                loader_type.assert_not_called()
                full_build.assert_not_called()
                addon_build.assert_not_called()
                create_run_directory.assert_not_called()
                compose.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()

    def test_default_build_profile_selections_and_external_requirements_are_unchanged(
        self,
    ) -> None:
        both = SimpleNamespace(
            id="both",
            addon_eligible=True,
            full_output="both.lua",
        )
        full_only = SimpleNamespace(
            id="full-only",
            addon_eligible=False,
            full_output="full-only.lua",
        )
        addon_only = SimpleNamespace(
            id="addon-only",
            addon_eligible=True,
            full_output=None,
        )
        neither = SimpleNamespace(
            id="neither",
            addon_eligible=False,
            full_output=None,
        )
        manifest = Mock(components=(both, full_only, addon_only, neither))
        for profile, expected in (
            ("full", [both, full_only]),
            ("addon", [both, addon_only]),
        ):
            with self.subTest(profile=profile):
                runtime = Mock()
                loader = Mock(spec=LocaleLoader)
                arguments = argparse.Namespace(
                    component=[],
                    profile=profile,
                    json=True,
                    require_complete=False,
                )
                full_report = {
                    "components": [],
                    "run_directory": "/artifacts/full",
                }
                addon_report = {"complete": True}
                with (
                    patch("i18nlib.cli._manifest", return_value=manifest),
                    patch("i18nlib.cli.LuaRuntime", return_value=runtime),
                    patch("i18nlib.cli.LocaleLoader", return_value=loader),
                    patch(
                        "i18nlib.cli.build_full_locales",
                        return_value=full_report,
                    ) as full_build,
                    patch(
                        "i18nlib.cli.build_addon_locale",
                        return_value=addon_report,
                    ) as addon_build,
                    patch("i18nlib.cli._print_json"),
                ):
                    self.assertEqual(cli_build(arguments), 0)

                runtime.doctor.assert_called_once_with()
                manifest.component.assert_not_called()
                if profile == "full":
                    full_build.assert_called_once_with(manifest, loader, expected)
                    addon_build.assert_not_called()
                else:
                    addon_build.assert_called_once_with(
                        manifest,
                        loader,
                        expected,
                        include_external_requirements=True,
                    )
                    full_build.assert_not_called()

    def test_unknown_explicit_build_component_fails_before_runtime_and_io(
        self,
    ) -> None:
        known = SimpleNamespace(
            id="known",
            addon_eligible=True,
            full_output="known.lua",
        )
        for identifiers in (["missing"], ["known", "missing"]):
            with self.subTest(identifiers=identifiers):
                manifest = Mock(components=(known,))

                def resolve(component_id: str) -> object:
                    if component_id == "known":
                        return known
                    raise ConfigurationError(f"unknown component {component_id!r}")

                manifest.component.side_effect = resolve
                arguments = argparse.Namespace(
                    component=identifiers,
                    profile="full",
                    json=True,
                    require_complete=False,
                )
                with (
                    patch("i18nlib.cli._manifest", return_value=manifest),
                    patch("i18nlib.cli.LuaRuntime") as runtime_type,
                    patch("i18nlib.cli.LocaleLoader") as loader_type,
                    patch("i18nlib.cli.build_full_locales") as full_build,
                    patch("i18nlib.cli.build_addon_locale") as addon_build,
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build._compose_full_locale") as compose,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(
                        ConfigurationError, r"unknown component 'missing'"
                    ):
                        cli_build(arguments)

                runtime_type.assert_not_called()
                loader_type.assert_not_called()
                full_build.assert_not_called()
                addon_build.assert_not_called()
                create_run_directory.assert_not_called()
                compose.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()


class BuildApiComponentDeduplicationTests(unittest.TestCase):
    def _assert_full_output_preflight_failure(
        self,
        selected: list[object],
        expected_message: str,
    ) -> None:
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        loader = Mock(spec=LocaleLoader)
        with (
            patch("i18nlib.build.create_run_directory") as create_run_directory,
            patch("i18nlib.build._compose_full_locale") as compose,
            patch("i18nlib.build._assert_same_semantics") as compare,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            with self.assertRaises(ValidationError) as raised:
                build_full_locales(manifest, loader, selected)

        self.assertEqual(str(raised.exception), expected_message)
        self.assertEqual(loader.mock_calls, [])
        create_run_directory.assert_not_called()
        compose.assert_not_called()
        compare.assert_not_called()
        write_bytes.assert_not_called()
        write_json.assert_not_called()

    def test_full_build_empty_selection_retains_existing_preflight_error(
        self,
    ) -> None:
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        loader = Mock(spec=LocaleLoader)
        with (
            patch("i18nlib.build.create_run_directory") as create_run_directory,
            patch("i18nlib.build._compose_full_locale") as compose,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            with self.assertRaisesRegex(
                ValidationError, r"^no full-locale components selected$"
            ):
                build_full_locales(manifest, loader, [])

        self.assertEqual(loader.mock_calls, [])
        create_run_directory.assert_not_called()
        compose.assert_not_called()
        write_bytes.assert_not_called()
        write_json.assert_not_called()

    def test_full_build_invalid_component_fails_before_runtime_and_io(
        self,
    ) -> None:
        valid = SimpleNamespace(
            id="valid",
            translation="valid.lua",
            copy_fragment=None,
            full_output="shared-output.lua",
        )
        conflicting = SimpleNamespace(
            id="conflicting",
            translation="conflicting.lua",
            copy_fragment=None,
            full_output="shared-output.lua",
        )
        invalid = SimpleNamespace(
            id="invalid",
            translation="invalid.lua",
            copy_fragment=None,
            full_output=None,
        )
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        for selected in (
            [invalid, valid, conflicting],
            [valid, conflicting, invalid],
        ):
            with self.subTest(components=[component.id for component in selected]):
                loader = Mock(spec=LocaleLoader)
                with (
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build._compose_full_locale") as compose,
                    patch(
                        "i18nlib.build._assert_same_semantics"
                    ) as compare,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"component 'invalid' has no full_output mapping",
                    ):
                        build_full_locales(manifest, loader, selected)

                self.assertEqual(loader.mock_calls, [])
                create_run_directory.assert_not_called()
                compose.assert_not_called()
                compare.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()

    def test_full_build_rejects_exact_output_collision_before_runtime_and_io(
        self,
    ) -> None:
        alpha = SimpleNamespace(id="alpha", full_output="shared.lua")
        beta = SimpleNamespace(id="beta", full_output="shared.lua")
        expected = (
            "full_output collision (exact duplicate output path): "
            "component 'alpha' maps to 'shared.lua'; "
            "component 'beta' maps to 'shared.lua'"
        )
        for selected in ([alpha, beta], [beta, alpha]):
            with self.subTest(components=[component.id for component in selected]):
                self._assert_full_output_preflight_failure(selected, expected)

    def test_full_build_rejects_ancestor_output_collision_before_runtime_and_io(
        self,
    ) -> None:
        parent = SimpleNamespace(id="parent", full_output="locales")
        child = SimpleNamespace(id="child", full_output="locales/zh_hans.lua")
        expected = (
            "full_output collision (ancestor/descendant output paths): "
            "component 'parent' maps to 'locales'; "
            "component 'child' maps to 'locales/zh_hans.lua'"
        )
        for selected in ([parent, child], [child, parent]):
            with self.subTest(components=[component.id for component in selected]):
                self._assert_full_output_preflight_failure(selected, expected)

    def test_full_build_performs_component_work_once_in_first_seen_order(
        self,
    ) -> None:
        second = SimpleNamespace(
            id="second",
            translation="second.lua",
            copy_fragment=None,
            full_output="second-output.lua",
        )
        first = SimpleNamespace(
            id="first",
            translation="first.lua",
            copy_fragment=None,
            full_output="first-output.lua",
        )
        duplicate_second = SimpleNamespace(
            id="second",
            translation="duplicate-second.lua",
            copy_fragment=None,
            full_output="first-output.lua",
        )
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            lambda path, *, logical_path: _component_selection_document(
                logical_path, logical_path
            )
        )
        loader.load_bytes.return_value = _component_selection_document("generated")
        run_directory = Path("/artifacts/build-full")

        with (
            patch(
                "i18nlib.build._compose_full_locale",
                side_effect=lambda _manifest, component: component.id.encode(),
            ) as compose,
            patch("i18nlib.build._assert_same_semantics") as compare,
            patch(
                "i18nlib.build.create_run_directory",
                return_value=run_directory,
            ) as create_run_directory,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            report = build_full_locales(
                manifest,
                loader,
                [second, first, duplicate_second, first],
            )

        self.assertEqual(
            [item["component"] for item in report["components"]],
            ["second", "first"],
        )
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(Path("/fixture/second.lua"), logical_path="second.lua"),
                call(Path("/fixture/first.lua"), logical_path="first.lua"),
            ],
        )
        self.assertEqual(loader.load_bytes.call_count, 2)
        self.assertEqual(
            [args.args[1] for args in compose.call_args_list],
            [second, first],
        )
        self.assertEqual(compare.call_count, 2)
        create_run_directory.assert_called_once_with(
            Path("/fixture"), "build-full"
        )
        self.assertEqual(
            write_bytes.call_args_list,
            [
                call(
                    run_directory / "full" / "second-output.lua",
                    b"second",
                ),
                call(
                    run_directory / "full" / "first-output.lua",
                    b"first",
                ),
            ],
        )
        write_json.assert_called_once_with(run_directory / "build.json", report)

    def test_addon_build_performs_component_work_once_and_does_not_inflate_stats(
        self,
    ) -> None:
        def component(component_id: str, translation: str | None = None) -> object:
            return SimpleNamespace(
                id=component_id,
                addon_eligible=True,
                source_repository="engine",
                official_locale=f"official-{component_id}.lua",
                translation=translation or f"{component_id}.lua",
                copy_fragment=None,
            )

        second = component("second")
        first = component("first")
        duplicate_second = component("second", "duplicate-second.lua")
        repository_path = Mock(return_value=Path("/repository"))
        manifest = SimpleNamespace(
            root=Path("/fixture"),
            version="fixture",
            locale="zh_hans",
            repositories={"engine": SimpleNamespace(commit="a" * 40)},
            repository_path=repository_path,
            addon_external_requirements=(),
        )
        canonical = {
            "second.lua": _component_selection_document(
                "second.lua", "source second"
            ),
            "first.lua": _component_selection_document(
                "first.lua", "source first"
            ),
        }
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            lambda path, *, logical_path: canonical[logical_path]
        )
        loader.load_bytes.side_effect = (
            lambda data, *, logical_path: _component_selection_document(logical_path)
        )
        run_directory = Path("/artifacts/build-addon")
        verification = {
            "expected_runtime_keys": 2,
            "patch_runtime_keys": 2,
            "missing": 0,
            "unexpected": 0,
            "mismatched": 0,
            "redundant": 0,
        }

        with (
            patch("i18nlib.build.GitRepository") as repository,
            patch(
                "i18nlib.build._render_addon_locale", return_value=b"addon"
            ) as render,
            patch(
                "i18nlib.build._verify_overlay", return_value=verification
            ) as verify,
            patch(
                "i18nlib.build.create_run_directory",
                return_value=run_directory,
            ) as create_run_directory,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            repository.return_value.read_blob.side_effect = [
                b"official second",
                b"official first",
            ]
            report = build_addon_locale(
                manifest,
                loader,
                [second, first, duplicate_second, first],
                include_external_requirements=False,
            )

        self.assertEqual(
            [item["component"] for item in report["components"]],
            ["second", "first"],
        )
        self.assertEqual(report["new_entries"], 2)
        self.assertEqual(report["override_entries"], 0)
        self.assertEqual(report["inherited_entries"], 0)
        self.assertEqual(len(report["delta_entries"]), 2)
        self.assertEqual(repository.call_count, 2)
        self.assertEqual(repository.return_value.read_blob.call_count, 2)
        self.assertEqual(repository_path.call_count, 2)
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(Path("/fixture/second.lua"), logical_path="second.lua"),
                call(Path("/fixture/first.lua"), logical_path="first.lua"),
            ],
        )
        self.assertEqual(loader.load_bytes.call_count, 3)
        render.assert_called_once()
        verify.assert_called_once()
        create_run_directory.assert_called_once_with(
            Path("/fixture"), "build-addon"
        )
        write_bytes.assert_called_once_with(
            run_directory / "addon" / "data" / "locales" / "zh_hans.lua",
            b"addon",
        )
        write_json.assert_called_once_with(run_directory / "build.json", report)


class BuildSemanticComparisonTests(unittest.TestCase):
    @staticmethod
    def _document(special: object) -> LocaleDocument:
        return LocaleDocument(
            logical_path="fixture.lua",
            sha256="a" * 64,
            records=(
                {
                    "kind": "translation",
                    "source": "fixture source",
                    "source_tag": None,
                    "target": "fixture target",
                    "args_order": None,
                    "special": special,
                },
            ),
        )

    def test_build_comparison_rejects_bool_int_but_accepts_reordered_objects(
        self,
    ) -> None:
        from i18nlib.build import _assert_same_semantics

        expected = self._document(
            {"outer": {"enabled": True, "values": [1, {"wrapped": False}]}}
        )
        equivalent = self._document(
            {"outer": {"values": [1, {"wrapped": False}], "enabled": True}}
        )
        _assert_same_semantics([expected], equivalent, label="fixture")

        type_drift = self._document(
            {"outer": {"values": [1, {"wrapped": 0}], "enabled": True}}
        )
        with self.assertRaisesRegex(ValidationError, "changed 1 translation values"):
            _assert_same_semantics([expected], type_drift, label="fixture")

    def test_overlay_bool_int_override_is_not_redundant(self) -> None:
        from i18nlib.build import _verify_overlay

        official = self._document({"enabled": True})
        canonical = self._document({"enabled": 1})
        patch_document = self._document({"enabled": 1})

        verification = _verify_overlay(
            [official],
            [canonical],
            patch_document,
        )
        self.assertEqual(verification["mismatched"], 0)
        self.assertEqual(verification["redundant"], 0)
        self.assertEqual(verification["patch_runtime_keys"], 1)


class StatusTests(unittest.TestCase):
    @staticmethod
    def _document(*entries: dict[str, object]) -> LocaleDocument:
        return LocaleDocument(
            logical_path="fixture.lua",
            sha256="a" * 64,
            records=tuple(
                {
                    "kind": "translation",
                    "source_tag": None,
                    "target": "fixture target",
                    "args_order": None,
                    **entry,
                }
                for entry in entries
            ),
        )

    def test_status_counts_nested_bool_int_drift_as_changed(self) -> None:
        from i18nlib.status import status_report

        canonical = self._document(
            {
                "source": "deep equivalent",
                "special": {"outer": {"enabled": True, "count": 1}},
            },
            {"source": "type drift", "special": {"enabled": True}},
        )
        official = self._document(
            {
                "source": "deep equivalent",
                "special": {"outer": {"count": 1, "enabled": True}},
            },
            {"source": "type drift", "special": {"enabled": 1}},
        )
        component = Mock(
            id="fixture",
            translation="fixture.lua",
            source_repository="engine",
            official_locale="official.lua",
        )
        manifest = Mock(
            version="fixture-version",
            root=Path("/fixture"),
            repositories={"engine": Mock(commit="a" * 40)},
        )
        manifest.repository_path.return_value = Path("/unused")
        loader = Mock(spec=LocaleLoader)
        loader.load_path.return_value = canonical
        loader.load_bytes.return_value = official

        with patch("i18nlib.status.GitRepository") as repository:
            repository.return_value.read_blob.return_value = b"official"
            report = status_report(manifest, loader, [component])

        counts = report["components"][0]
        self.assertEqual(counts["identical"], 1)
        self.assertEqual(counts["changed"], 1)
        self.assertEqual(report["totals"]["changed"], 1)


class AddonBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

    def test_noneligible_selections_fail_before_build_operations(self) -> None:
        eligible = self.manifest.component("tome")
        noneligible = self.manifest.component("boot")
        cases = (
            ("mixed", [eligible, noneligible]),
            ("only noneligible", [noneligible]),
        )
        for label, components in cases:
            with self.subTest(selection=label):
                loader = Mock(spec=LocaleLoader)
                with (
                    patch("i18nlib.build.GitRepository") as repository,
                    patch("i18nlib.build._render_addon_locale") as render,
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"addon build requires addon-eligible components; "
                        r"not eligible: boot$",
                    ):
                        build_addon_locale(
                            self.manifest,
                            loader,
                            components,
                            include_external_requirements=False,
                        )

                self.assertEqual(loader.mock_calls, [])
                repository.assert_not_called()
                render.assert_not_called()
                create_run_directory.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()

    def test_explicit_core_build_omits_inherited_translations(self) -> None:
        report = build_addon_locale(
            self.manifest,
            self.loader,
            [self.manifest.component("tome")],
            include_external_requirements=False,
        )
        self.assertTrue(report["complete"])
        self.assertEqual(report["skipped"], [])
        self.assertFalse(report["external_requirements_included"])
        component = report["components"][0]
        self.assertGreater(component["inherited_entries"], 0)
        self.assertGreater(component["delta_entries"], 0)
        self.assertLess(
            component["delta_entries"], component["canonical_runtime_keys"]
        )
        self.assertEqual(
            component["override_entries"] + component["new_entries"],
            component["delta_entries"],
        )
        self.assertEqual(
            report["verification"]["patch_runtime_keys"],
            component["delta_entries"],
        )

    def test_publish_dry_run_does_not_touch_release_repository(self) -> None:
        from i18nlib.publish import publish_addon

        addon_root = self.manifest.repository_path("addon")
        locale_file = addon_root / "data" / "locales" / "zh_hans.lua"
        before = locale_file.read_bytes() if locale_file.is_file() else None
        report = publish_addon(
            self.manifest,
            self.loader,
            apply=False,
            bump=False,
            commit=False,
        )
        self.assertFalse(report["applied"])
        self.assertTrue(report["new_entries"] > 0)
        after = locale_file.read_bytes() if locale_file.is_file() else None
        self.assertEqual(before, after)

    def test_publish_bump_version_regex(self) -> None:
        from i18nlib.publish import _bump_init_version

        text = 'addon_version = {0,2,0}\n'
        updated, version = _bump_init_version(text)
        self.assertEqual(updated, "addon_version = {0,2,1}\n")
        self.assertEqual(version, "0.2.1")

    def test_publish_dlc_entries_are_official_disjoint(self) -> None:
        from i18nlib.publish import _dlc_overlay_entries, _official_locale_keys

        official = _official_locale_keys(self.manifest, self.loader)
        entries = _dlc_overlay_entries(self.manifest, self.loader, official)
        self.assertGreater(len(entries), 0)
        keys = {(e["source"], e["source_tag"]) for e in entries}
        self.assertTrue(
            keys.isdisjoint(official),
            "DLC overlay entries must not shadow official locale keys",
        )
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            count = sum(1 for e in entries if e.get("section") == component_id)
            self.assertGreater(count, 0, f"no overlay entries for {component_id}")

    def test_publish_dry_run_reports_dlc_merge(self) -> None:
        from i18nlib.publish import publish_addon

        report = publish_addon(
            self.manifest,
            self.loader,
            apply=False,
            bump=False,
            commit=False,
        )
        self.assertGreater(report["dlc_entries"], 0)
        self.assertEqual(
            report["new_entries"],
            report["delta_runtime_keys"] + report["dlc_entries"],
        )
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            self.assertGreater(report["dlc_entries_by_component"][component_id], 0)

    def test_publish_commit_rejects_staged_target_before_build_or_loader(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        cases = (
            ("committed locale", False, "data/locales/zh_hans.lua", True),
            ("committed init", True, "init.lua", True),
            ("initial repository", False, "data/locales/zh_hans.lua", False),
        )
        for label, bump, staged_relative, commit_baseline in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-publish-staged-target-"
            ) as temporary:
                manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                    Path(temporary),
                    commit_baseline=commit_baseline,
                )
                addon_root = locale_path.parents[2]
                staged_path = addon_root / staged_relative
                original_files = {
                    locale_path: locale_path.read_bytes(),
                    init_path: init_path.read_bytes(),
                }
                staged_path.write_bytes(
                    original_files[staged_path] + b"-- staged user content\n"
                )
                self._git(addon_root, "add", "--", staged_relative)
                staged_path.write_bytes(original_files[staged_path])

                index_before = self._git(addon_root, "write-tree").stdout
                index_entries_before = self._git(
                    addon_root,
                    "ls-files",
                    "--stage",
                ).stdout
                status_before = self._git(
                    addon_root,
                    "status",
                    "--porcelain=v1",
                ).stdout
                head_before = self._git(
                    addon_root,
                    "rev-parse",
                    "--verify",
                    "HEAD",
                    check=False,
                )
                loader = Mock(spec=LocaleLoader)

                with (
                    patch.dict(
                        os.environ,
                        {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                    ),
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module, "_official_locale_keys"
                    ) as official_keys,
                    patch.object(
                        publish_module, "_dlc_overlay_entries"
                    ) as dlc_entries,
                    patch.object(publish_module, "_render_addon_locale") as renderer,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"release git staged-state preflight refused:.*"
                        r"staged changes relative to HEAD",
                    ):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=bump,
                            commit=True,
                        )

                build.assert_not_called()
                official_keys.assert_not_called()
                dlc_entries.assert_not_called()
                renderer.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                self.assertEqual(
                    {path: path.read_bytes() for path in original_files},
                    original_files,
                )
                self.assertEqual(
                    self._git(addon_root, "write-tree").stdout,
                    index_before,
                )
                self.assertEqual(
                    self._git(addon_root, "ls-files", "--stage").stdout,
                    index_entries_before,
                )
                self.assertEqual(
                    self._git(addon_root, "status", "--porcelain=v1").stdout,
                    status_before,
                )
                head_after = self._git(
                    addon_root,
                    "rev-parse",
                    "--verify",
                    "HEAD",
                    check=False,
                )
                self.assertEqual(head_after.returncode, head_before.returncode)
                self.assertEqual(head_after.stdout, head_before.stdout)
                self.assertEqual(head_after.stderr, head_before.stderr)

    def test_publish_git_preflight_failures_are_controlled_before_build(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        cases = (
            (
                "launch",
                FileNotFoundError("controlled missing git"),
                r"preflight failed to start: controlled missing git",
            ),
            (
                "nonzero",
                subprocess.CompletedProcess(
                    ["git", "diff"],
                    128,
                    stdout="",
                    stderr="controlled index failure\n",
                ),
                r"preflight failed: controlled index failure",
            ),
        )
        for label, outcome, expected in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-publish-git-preflight-failure-"
            ) as temporary:
                manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                    Path(temporary)
                )
                addon_root = locale_path.parents[2]
                files_before = {
                    locale_path: locale_path.read_bytes(),
                    init_path: init_path.read_bytes(),
                }
                index_before = self._git(addon_root, "write-tree").stdout
                loader = Mock(spec=LocaleLoader)
                run_kwargs = (
                    {"side_effect": outcome}
                    if isinstance(outcome, BaseException)
                    else {"return_value": outcome}
                )

                with (
                    patch.dict(
                        os.environ,
                        {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                    ),
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module.subprocess,
                        "run",
                        **run_kwargs,
                    ),
                ):
                    with self.assertRaisesRegex(ValidationError, expected):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=True,
                            commit=True,
                        )

                build.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                self.assertEqual(
                    {path: path.read_bytes() for path in files_before},
                    files_before,
                )
                self.assertEqual(
                    self._git(addon_root, "write-tree").stdout,
                    index_before,
                )

    def test_publish_commit_excludes_preexisting_staged_changes(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)

        for bump in (False, True):
            with self.subTest(bump=bump), tempfile.TemporaryDirectory(
                prefix=f"tome4-publish-scoped-commit-{bump}-"
            ) as temporary:
                manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                    Path(temporary)
                )
                addon_root = locale_path.parents[2]
                unrelated_path = addon_root / "unrelated.txt"
                unrelated_path.write_text("baseline\n", encoding="utf-8")
                locale_mode = stat.S_IMODE(locale_path.stat().st_mode)
                init_mode = stat.S_IMODE(init_path.stat().st_mode)

                def git(*arguments: str) -> subprocess.CompletedProcess[str]:
                    return self._git(addon_root, *arguments)

                git("add", "--", "unrelated.txt")
                git("commit", "-qm", "add unrelated baseline")

                unrelated_path.write_text("staged user change\n", encoding="utf-8")
                staged_before = ["unrelated.txt"]
                git("add", "--", "unrelated.txt")
                if not bump:
                    init_path.write_text(
                        "addon_version = {0,0,1}\n-- staged user change\n",
                        encoding="utf-8",
                    )
                    git("add", "--", "init.lua")
                    staged_before.insert(0, "init.lua")
                preserved_index_before = git(
                    "ls-files",
                    "--stage",
                    "--",
                    *staged_before,
                ).stdout

                with (
                    patch.dict(
                        os.environ,
                        {
                            "TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root),
                        },
                    ),
                    patch.object(
                        publish_module,
                        "build_addon_locale",
                        return_value=build_report,
                    ),
                    patch.object(
                        publish_module, "_official_locale_keys", return_value=set()
                    ),
                    patch.object(
                        publish_module, "_dlc_overlay_entries", return_value=[]
                    ),
                ):
                    report = publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=bump,
                        commit=True,
                    )

                committed_paths = git(
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    "HEAD",
                ).stdout.splitlines()
                expected_paths = ["data/locales/zh_hans.lua"]
                if bump:
                    expected_paths.append("init.lua")
                self.assertEqual(committed_paths, expected_paths)
                self.assertEqual(
                    git("diff", "--cached", "--name-only").stdout.splitlines(),
                    staged_before,
                )
                self.assertEqual(
                    git("ls-files", "--stage", "--", *staged_before).stdout,
                    preserved_index_before,
                )
                self.assertEqual(
                    report["release_head"], git("rev-parse", "HEAD").stdout.strip()
                )
                self.assertEqual(
                    stat.S_IMODE(locale_path.stat().st_mode),
                    locale_mode,
                )
                self.assertEqual(stat.S_IMODE(init_path.stat().st_mode), init_mode)
                if bump:
                    self.assertIn(b"addon_version = {0,0,2}\r\n", init_path.read_bytes())

    @staticmethod
    def _git(
        root: Path,
        *arguments: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=check,
            capture_output=True,
            text=True,
        )

    def _isolated_publish_fixture(
        self,
        root: Path,
        *,
        commit_baseline: bool = True,
    ) -> tuple[object, Path, Path, str]:
        addon_root = (root / "addon").resolve()
        locale_path = addon_root / "data" / "locales" / "zh_hans.lua"
        init_path = addon_root / "init.lua"
        locale_path.parent.mkdir(parents=True)
        locale_text = (
            'locale "zh_hans"\n'
            'section "fixture/old.lua"\n'
            't("old source", "old target")\n'
        )
        locale_path.write_text(locale_text, encoding="utf-8")
        init_path.write_bytes(b"addon_version = {0,0,1}\r\n")
        locale_path.chmod(0o640)
        init_path.chmod(0o600)
        self._git(addon_root, "init", "-q")
        self._git(addon_root, "config", "user.name", "fixture")
        self._git(
            addon_root,
            "config",
            "user.email",
            "fixture@example.invalid",
        )
        if commit_baseline:
            self._git(
                addon_root,
                "add",
                "--",
                "data/locales/zh_hans.lua",
                "init.lua",
            )
            self._git(addon_root, "commit", "-qm", "baseline")
        repositories = dict(self.manifest.repositories)
        repositories["addon"] = replace(
            repositories["addon"],
            env="TOME4_PUBLISH_TEST_ADDON_ROOT",
            default="addon",
        )
        manifest = replace(self.manifest, root=root, repositories=repositories)
        return manifest, locale_path, init_path, locale_text

    @staticmethod
    def _publish_build_report(entry: dict[str, object]) -> dict[str, object]:
        return {
            "delta_entries": [entry],
            "components": [{"delta_entries": 1}],
            "override_entries": 0,
            "new_entries": 1,
            "verification": {"patch_runtime_keys": 1},
        }

    def test_publish_non_bump_does_not_read_init_contents(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-non-bump-read-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            original_read_snapshot = publish_module._read_file_snapshot
            snapshot_paths: list[Path] = []

            def tracked_read_snapshot(path: Path, *, label: str) -> object:
                snapshot_paths.append(path)
                return original_read_snapshot(path, label=label)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(locale_path.parents[2])},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_read_file_snapshot",
                    side_effect=tracked_read_snapshot,
                ),
            ):
                report = publish_module.publish_addon(
                    manifest,
                    self.loader,
                    apply=False,
                    bump=False,
                    commit=False,
                )

            self.assertFalse(report["applied"])
            self.assertEqual(snapshot_paths, [locale_path])
            self.assertNotIn(init_path, snapshot_paths)

    def test_publish_hash_failure_restores_locale_bytes_and_mode(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-hash-rollback-"
        ) as temporary:
            manifest, locale_path, _, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_mode = stat.S_IMODE(locale_path.stat().st_mode)
            index_before = self._git(addon_root, "write-tree").stdout
            original_atomic_replace = publish_module._atomic_replace_bytes

            def corrupt_locale_write(
                path: Path,
                data: bytes,
                mode: int,
                *,
                label: str,
            ) -> None:
                if label == "publish locale write":
                    data += b"\n-- controlled post-write corruption\n"
                original_atomic_replace(path, data, mode, label=label)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_atomic_replace_bytes",
                    side_effect=corrupt_locale_write,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish verification failed: written file hash mismatch",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=False,
                        commit=False,
                    )

            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(stat.S_IMODE(locale_path.stat().st_mode), original_mode)
            self.assertEqual(self._git(addon_root, "write-tree").stdout, index_before)
            self.assertEqual(
                list(locale_path.parent.glob(f".{locale_path.name}.*.tmp")),
                [],
            )

    def test_publish_second_file_failure_rolls_back_both_files_in_reverse(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-second-write-rollback-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_init = init_path.read_bytes()
            original_modes = {
                locale_path: stat.S_IMODE(locale_path.stat().st_mode),
                init_path: stat.S_IMODE(init_path.stat().st_mode),
            }
            index_before = self._git(addon_root, "write-tree").stdout
            original_os_replace = publish_module.os.replace
            replaced_paths: list[Path] = []
            failed_init_replace = False

            def fail_after_init_replace(source: object, target: object) -> None:
                nonlocal failed_init_replace
                original_os_replace(source, target)
                target_path = Path(target)
                replaced_paths.append(target_path)
                if target_path == init_path and not failed_init_replace:
                    failed_init_replace = True
                    raise OSError("controlled second-file replace failure")

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module.os,
                    "replace",
                    side_effect=fail_after_init_replace,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    "controlled second-file replace failure",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=False,
                    )

            self.assertEqual(replaced_paths, [locale_path, init_path, init_path, locale_path])
            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(init_path.read_bytes(), original_init)
            self.assertEqual(
                stat.S_IMODE(locale_path.stat().st_mode),
                original_modes[locale_path],
            )
            self.assertEqual(
                stat.S_IMODE(init_path.stat().st_mode),
                original_modes[init_path],
            )
            self.assertEqual(self._git(addon_root, "write-tree").stdout, index_before)

    def test_publish_failed_commit_restores_files_and_preserves_index(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-commit-failure-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            unrelated_path = addon_root / "unrelated.txt"
            unrelated_path.write_text("baseline\n", encoding="utf-8")
            self._git(addon_root, "add", "--", "unrelated.txt")
            self._git(addon_root, "commit", "-qm", "add unrelated baseline")

            original_locale = locale_path.read_bytes()
            original_init = init_path.read_bytes()
            original_modes = {
                locale_path: stat.S_IMODE(locale_path.stat().st_mode),
                init_path: stat.S_IMODE(init_path.stat().st_mode),
            }

            unrelated_path.write_text("staged unrelated change\n", encoding="utf-8")
            self._git(addon_root, "add", "--", "unrelated.txt")

            index_tree_before = self._git(addon_root, "write-tree").stdout
            index_entries_before = self._git(
                addon_root,
                "ls-files",
                "--stage",
            ).stdout
            cached_diff_before = self._git(
                addon_root,
                "diff",
                "--cached",
                "--binary",
                "--no-ext-diff",
            ).stdout
            status_before = self._git(
                addon_root,
                "status",
                "--porcelain=v1",
            ).stdout
            head_before = self._git(addon_root, "rev-parse", "HEAD").stdout

            hook_path = addon_root / ".git" / "hooks" / "pre-commit"
            hook_path.write_text(
                "#!/bin/sh\necho controlled hook failure >&2\nexit 23\n",
                encoding="utf-8",
            )
            hook_path.chmod(0o755)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"release git commit failed: controlled hook failure",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=True,
                    )

            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(init_path.read_bytes(), original_init)
            self.assertEqual(
                stat.S_IMODE(locale_path.stat().st_mode),
                original_modes[locale_path],
            )
            self.assertEqual(
                stat.S_IMODE(init_path.stat().st_mode),
                original_modes[init_path],
            )
            self.assertEqual(
                self._git(addon_root, "write-tree").stdout,
                index_tree_before,
            )
            self.assertEqual(
                self._git(addon_root, "ls-files", "--stage").stdout,
                index_entries_before,
            )
            self.assertEqual(
                self._git(
                    addon_root,
                    "diff",
                    "--cached",
                    "--binary",
                    "--no-ext-diff",
                ).stdout,
                cached_diff_before,
            )
            self.assertEqual(
                self._git(addon_root, "status", "--porcelain=v1").stdout,
                status_before,
            )
            self.assertEqual(
                self._git(addon_root, "rev-parse", "HEAD").stdout,
                head_before,
            )

    def test_publish_git_launch_failure_is_wrapped_and_rolled_back(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-git-launch-rollback-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_init = init_path.read_bytes()
            index_before = self._git(addon_root, "write-tree").stdout
            original_subprocess_run = subprocess.run

            def fail_git_commit(command: object, **kwargs: object) -> object:
                if isinstance(command, list) and command[:2] == ["git", "commit"]:
                    raise FileNotFoundError("controlled missing git")
                return original_subprocess_run(command, **kwargs)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module.subprocess,
                    "run",
                    side_effect=fail_git_commit,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"release git commit failed to start: controlled missing git",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=True,
                    )

            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(init_path.read_bytes(), original_init)
            self.assertEqual(self._git(addon_root, "write-tree").stdout, index_before)

    def test_publish_keyboard_interrupt_rolls_back_and_propagates(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        interrupt = KeyboardInterrupt("controlled publish interrupt")
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-interrupt-rollback-"
        ) as temporary:
            manifest, locale_path, _, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_mode = stat.S_IMODE(locale_path.stat().st_mode)
            original_verify = publish_module._verify_file_snapshot

            def interrupt_post_write(
                path: Path,
                expected: object,
                *,
                label: str,
            ) -> bytes:
                if label == "publish verification":
                    raise interrupt
                return original_verify(path, expected, label=label)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_verify_file_snapshot",
                    side_effect=interrupt_post_write,
                ),
            ):
                with self.assertRaises(KeyboardInterrupt) as raised:
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=False,
                        commit=False,
                    )

            self.assertIs(raised.exception, interrupt)
            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(stat.S_IMODE(locale_path.stat().st_mode), original_mode)

    def test_publish_rollback_failure_is_explicit_and_chains_original(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-rollback-failure-"
        ) as temporary:
            manifest, locale_path, _, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_atomic_replace = publish_module._atomic_replace_bytes
            loader = Mock(spec=LocaleLoader)
            loader.load_bytes.side_effect = self.loader.load_bytes
            locale_loads = 0

            def fail_post_write_load(
                path: Path,
                *,
                logical_path: str,
            ) -> LocaleDocument:
                nonlocal locale_loads
                locale_loads += 1
                if locale_loads == 2:
                    raise ValidationError("controlled post-write failure")
                return self.loader.load_path(path, logical_path=logical_path)

            def fail_rollback(
                path: Path,
                data: bytes,
                mode: int,
                *,
                label: str,
            ) -> None:
                if label == "publish rollback":
                    raise OSError("controlled rollback failure")
                original_atomic_replace(path, data, mode, label=label)

            loader.load_path.side_effect = fail_post_write_load
            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_atomic_replace_bytes",
                    side_effect=fail_rollback,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish transaction rollback failed after ValidationError:.*"
                    r"controlled rollback failure",
                ) as raised:
                    publish_module.publish_addon(
                        manifest,
                        loader,
                        apply=True,
                        bump=False,
                        commit=False,
                    )

            self.assertIsInstance(raised.exception.__cause__, ValidationError)
            self.assertIn(
                "controlled post-write failure",
                str(raised.exception.__cause__),
            )

    def test_publish_rejects_bool_int_artifact_change_before_release_writes(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": True,
        }
        build_report = self._publish_build_report(entry)
        original_renderer = publish_module._render_addon_locale

        def corrupted_renderer(
            manifest: object,
            entries: object,
            *,
            skipped: object,
        ) -> bytes:
            rendered = original_renderer(manifest, entries, skipped=skipped)
            self.assertIn(b", true)", rendered)
            return rendered.replace(b", true)", b", 1)", 1)

        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-prewrite-"
        ) as temporary:
            manifest, locale_path, init_path, locale_text = (
                self._isolated_publish_fixture(Path(temporary))
            )
            original_init = init_path.read_bytes()
            release_writes: list[Path] = []
            original_write_bytes = Path.write_bytes

            def tracked_write_bytes(path: Path, data: bytes) -> int:
                if path in (locale_path, init_path):
                    release_writes.append(path)
                return original_write_bytes(path, data)

            git_subprocess = Mock()
            git_subprocess.run.return_value = subprocess.CompletedProcess(
                ["git", "diff"],
                0,
                stdout="",
                stderr="",
            )
            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(locale_path.parents[2])},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_render_addon_locale",
                    side_effect=corrupted_renderer,
                ),
                patch.object(Path, "write_bytes", tracked_write_bytes),
                patch.object(publish_module, "subprocess", git_subprocess),
                patch.object(publish_module, "_bump_init_version") as bump_version,
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish pre-write verification failed:.*mismatched=1",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=True,
                    )

            self.assertEqual(release_writes, [])
            self.assertEqual(locale_path.read_text(encoding="utf-8"), locale_text)
            self.assertEqual(init_path.read_bytes(), original_init)
            bump_version.assert_not_called()
            git_subprocess.run.assert_called_once_with(
                [
                    "git",
                    "diff",
                    "--cached",
                    "--quiet",
                    "--",
                    "data/locales/zh_hans.lua",
                    "init.lua",
                ],
                cwd=locale_path.parents[2],
                capture_output=True,
                text=True,
            )

    def test_publish_post_write_semantic_failure_precedes_git(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)

        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-postwrite-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            original_locale = locale_path.read_bytes()
            original_locale_mode = stat.S_IMODE(locale_path.stat().st_mode)
            loader = Mock(spec=LocaleLoader)
            loader.load_bytes.side_effect = self.loader.load_bytes
            locale_loads = 0

            def load_path(path: Path, *, logical_path: str) -> LocaleDocument:
                nonlocal locale_loads
                document = self.loader.load_path(path, logical_path=logical_path)
                if path != locale_path:
                    return document
                locale_loads += 1
                if locale_loads != 2:
                    return document
                records = tuple(
                    {
                        **record,
                        "target": "renderer-preserving post-write corruption",
                    }
                    if record.get("kind") == "translation"
                    else record
                    for record in document.records
                )
                return LocaleDocument(
                    logical_path=document.logical_path,
                    sha256=document.sha256,
                    records=records,
                )

            loader.load_path.side_effect = load_path
            git_subprocess = Mock()
            git_subprocess.run.return_value = subprocess.CompletedProcess(
                ["git", "diff"],
                0,
                stdout="",
                stderr="",
            )
            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(locale_path.parents[2])},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(publish_module, "subprocess", git_subprocess),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish post-write verification failed:.*mismatched=1",
                ):
                    publish_module.publish_addon(
                        manifest,
                        loader,
                        apply=True,
                        bump=False,
                        commit=True,
                    )

            self.assertEqual(locale_loads, 2)
            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(
                stat.S_IMODE(locale_path.stat().st_mode),
                original_locale_mode,
            )
            self.assertEqual(
                init_path.read_text(encoding="utf-8"),
                "addon_version = {0,0,1}\n",
            )
            git_subprocess.run.assert_called_once_with(
                [
                    "git",
                    "diff",
                    "--cached",
                    "--quiet",
                    "--",
                    "data/locales/zh_hans.lua",
                ],
                cwd=locale_path.parents[2],
                capture_output=True,
                text=True,
            )


class SmokeReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    @staticmethod
    def _write_layout(root: Path) -> dict[str, Path]:
        paths = {
            "locale": root / "data" / "locales" / "zh_hans.lua",
            "null": root / "data" / "null_translation.lua",
            "hooks": root / "hooks" / "load.lua",
            "init": root / "init.lua",
        }
        for path in paths.values():
            path.parent.mkdir(parents=True, exist_ok=True)
        paths["locale"].write_text("-- release fixture\n", encoding="utf-8")
        paths["null"].write_text("-- null fixture\n", encoding="utf-8")
        paths["hooks"].write_text(
            'load("/data/null_translation.lua")\n', encoding="utf-8"
        )
        paths["init"].write_text(
            '-- GNU General Public License\nfor_module = "tome"\n'
            "addon_version = {0, 0, 1}\n",
            encoding="utf-8",
        )
        return paths

    @staticmethod
    def _entry(
        source: str,
        target: str,
        *,
        section: str = "ashes-urhrok",
        args_order: object = None,
        special: object = None,
    ) -> dict[str, object]:
        return {
            "kind": "translation",
            "section": section,
            "source": source,
            "target": target,
            "source_tag": None,
            "args_order": args_order,
            "special": special,
        }

    def _run_fixture(
        self,
        root: Path,
        release_entries: list[dict[str, object]],
        expected_entries: list[dict[str, object]],
        *,
        runtime_error: Exception | None = None,
    ) -> tuple[int, str, Mock, Mock, Mock]:
        paths = self._write_layout(root)
        runtime = Mock(spec=LuaRuntime)
        runtime.manifest = self.manifest

        def run_probe(
            arguments: list[object], **kwargs: object
        ) -> subprocess.CompletedProcess[str]:
            if runtime_error is not None:
                raise runtime_error
            target = Path(str(arguments[-1]))
            stdout = ""
            if target == paths["locale"]:
                stdout = "entries:6001\n"
            elif target == paths["null"]:
                stdout = "entries:401\n"
            return subprocess.CompletedProcess(arguments, 0, stdout, "")

        runtime.run.side_effect = run_probe
        runtime_factory = Mock(return_value=runtime)
        loader = Mock(spec=LocaleLoader)
        loader.load_path.return_value = LocaleDocument(
            logical_path="release",
            sha256="0" * 64,
            records=tuple(release_entries),
        )
        loader_factory = Mock(return_value=loader)
        official_keys_loader = Mock(return_value=set())
        overlay_entries_loader = Mock(return_value=expected_entries)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = smoke_release.run_release_smoke(
                self.manifest,
                root,
                runtime_factory=runtime_factory,
                loader_factory=loader_factory,
                official_keys_loader=official_keys_loader,
                overlay_entries_loader=overlay_entries_loader,
            )
        return exit_code, stdout.getvalue(), runtime, runtime_factory, loader_factory

    def test_missing_layout_files_short_circuit_before_runtime_or_reads(self) -> None:
        for missing_name in ("locale", "null", "hooks", "init"):
            with self.subTest(missing=missing_name), tempfile.TemporaryDirectory(
                prefix="tome4-smoke-layout-"
            ) as temporary:
                root = Path(temporary)
                paths = self._write_layout(root)
                paths[missing_name].unlink()
                runtime_factory = Mock(side_effect=AssertionError("runtime called"))
                loader_factory = Mock(side_effect=AssertionError("loader called"))
                text_reader = Mock(side_effect=AssertionError("read called"))
                stdout = io.StringIO()

                with contextlib.redirect_stdout(stdout):
                    exit_code = smoke_release.run_release_smoke(
                        self.manifest,
                        root,
                        runtime_factory=runtime_factory,
                        loader_factory=loader_factory,
                        text_reader=text_reader,
                    )

                self.assertEqual(exit_code, 1)
                for label in (
                    "locale file exists",
                    "null_translation exists",
                    "hooks/load.lua exists",
                    "init.lua exists",
                ):
                    self.assertIn(label, stdout.getvalue())
                runtime_factory.assert_not_called()
                loader_factory.assert_not_called()
                text_reader.assert_not_called()

    def test_configured_runtime_and_timeout_are_used_for_all_lua_smoke_checks(
        self,
    ) -> None:
        entries = [
            self._entry("ashes", "余烬"),
            self._entry("cults", "邪教", section="cults"),
            self._entry("orcs", "兽人", section="orcs"),
        ]
        with tempfile.TemporaryDirectory(prefix="tome4-smoke-runtime-") as temporary:
            root = Path(temporary)
            exit_code, stdout, runtime, runtime_factory, loader_factory = (
                self._run_fixture(root, entries, entries)
            )

        self.assertEqual(exit_code, 0, stdout)
        runtime_factory.assert_called_once_with(self.manifest)
        runtime.doctor.assert_called_once_with()
        loader_factory.assert_called_once_with(runtime)
        self.assertEqual(runtime.run.call_count, 3)
        targets = []
        for runtime_call in runtime.run.call_args_list:
            arguments = runtime_call.args[0]
            targets.append(Path(str(arguments[-1])))
            self.assertEqual(runtime_call.kwargs["cwd"], self.manifest.root)
            self.assertEqual(
                runtime_call.kwargs["timeout"],
                smoke_release._LUA_TIMEOUT_SECONDS,
            )
        self.assertEqual(
            targets,
            [
                root / "data" / "locales" / "zh_hans.lua",
                root / "data" / "null_translation.lua",
                root / "hooks" / "load.lua",
            ],
        )
        self.assertIn("SMOKE OK", stdout)
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            self.assertIn(
                f"DLC {component_id} exact runtime overlay", stdout
            )
            self.assertIn("missing=0, unexpected=0, mismatched=0", stdout)

    def test_runtime_errors_are_clean_failures_without_tracebacks(self) -> None:
        entries = [
            self._entry("ashes", "余烬"),
            self._entry("cults", "邪教", section="cults"),
            self._entry("orcs", "兽人", section="orcs"),
        ]
        for detail in ("luajit not found", "luajit command timed out after 300 seconds"):
            with self.subTest(detail=detail), tempfile.TemporaryDirectory(
                prefix="tome4-smoke-runtime-error-"
            ) as temporary:
                exit_code, stdout, _, _, _ = self._run_fixture(
                    Path(temporary),
                    entries,
                    entries,
                    runtime_error=RuntimeError(detail),
                )

            self.assertEqual(exit_code, 1)
            self.assertIn("[FAIL]", stdout)
            self.assertIn(detail, stdout)
            self.assertNotIn("Traceback", stdout)

    def test_exact_dlc_comparison_rejects_all_drift_classes(self) -> None:
        key = ("same key", None)
        expected_entry = self._entry(
            "same key",
            "正确译文",
            args_order=[2, 1],
            special={"enabled": True},
        )
        expected = {key: expected_entry}
        cases = {
            "wrong target": {
                key: {**expected_entry, "target": "错误译文"},
            },
            "wrong args_order": {
                key: {**expected_entry, "args_order": [1, 2]},
            },
            "wrong special": {
                key: {**expected_entry, "special": {"enabled": False}},
            },
            "missing": {},
            "unexpected": {
                key: expected_entry,
                ("stale extra", None): self._entry("stale extra", "旧译文"),
            },
            "bool versus int": {
                key: {**expected_entry, "special": {"enabled": 1}},
            },
        }
        expected_drift = {
            "wrong target": (0, 0, 1),
            "wrong args_order": (0, 0, 1),
            "wrong special": (0, 0, 1),
            "missing": (1, 0, 0),
            "unexpected": (0, 1, 0),
            "bool versus int": (0, 0, 1),
        }

        for label, actual in cases.items():
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-smoke-dlc-drift-"
            ) as temporary:
                comparison = smoke_release.compare_dlc_runtime_maps(
                    expected, actual
                )
                self.assertFalse(comparison.ok)
                self.assertEqual(
                    (
                        len(comparison.missing),
                        len(comparison.unexpected),
                        len(comparison.mismatched),
                    ),
                    expected_drift[label],
                )
                exit_code, stdout, _, _, _ = self._run_fixture(
                    Path(temporary),
                    list(actual.values()),
                    [expected_entry],
                )
                self.assertEqual(exit_code, 1, stdout)
                self.assertIn(
                    "[FAIL] DLC ashes-urhrok exact runtime overlay", stdout
                )

        exact = smoke_release.compare_dlc_runtime_maps(expected, dict(expected))
        self.assertTrue(exact.ok)
        self.assertEqual(
            exact.detail,
            "expected=1, actual=1, missing=0, unexpected=0, mismatched=0",
        )


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
            patch("i18nlib.cli._manifest", return_value=manifest),
            patch("i18nlib.cli.LuaRuntime", return_value=runtime),
            patch("i18nlib.cli.LocaleLoader", return_value=loader),
            patch("i18nlib.cli.load_policy", return_value=EMPTY_POLICY),
            patch("i18nlib.cli.lint_terminology", return_value=([], {"rows": 0})),
            patch("i18nlib.cli.create_run_directory", return_value=run_directory),
            patch("i18nlib.cli.write_json") as write_json,
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
                patch("i18nlib.cli._manifest", return_value=manifest),
                patch("i18nlib.cli.LuaRuntime", return_value=runtime),
                patch("i18nlib.cli.LocaleLoader", return_value=loader),
                patch("i18nlib.cli.load_policy", return_value=EMPTY_POLICY),
                patch(
                    "i18nlib.cli.create_run_directory",
                    return_value=root / "report",
                ),
                patch("i18nlib.cli.write_json"),
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
        issues, metrics = lint_terminology(ROOT / "terminology.tsv")
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


class ReviewBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    def _write_bundle(self, directory: Path, payload: dict[str, object]) -> Path:
        payload["bundle_id"] = _bundle_id(payload)
        path = directory / "bundle.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def _base(self, kind: str) -> dict[str, object]:
        return {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": self.manifest.version,
            "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            "kind": kind,
        }

    def test_review_bundle_schema_rejects_non_integer_versions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-schema-") as temporary:
            directory = Path(temporary)
            for schema_version in (True, 1.0):
                with self.subTest(schema_version=schema_version):
                    payload = self._base("translations")
                    payload["schema_version"] = schema_version
                    path = self._write_bundle(directory, payload)
                    with self.assertRaisesRegex(
                        ValidationError, "unsupported review bundle schema"
                    ):
                        validate_review_bundle(self.manifest, path)

    def test_remediation_review_schema_rejects_non_integer_versions(self) -> None:
        bundle = {
            "kind": "translations",
            "bundle_id": "bundle-schema-fixture",
            "items": [],
        }
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                review = json.loads(
                    json.dumps(
                        {
                            "schema_version": schema_version,
                            "review_contract": REVIEW_CONTRACT,
                            "bundle_id": bundle["bundle_id"],
                            "findings": [],
                        }
                    )
                )
                with self.assertRaisesRegex(
                    ValidationError, "validated review has an unsupported schema"
                ):
                    _validate_findings_for_remediation(bundle, review)

    def test_model_review_schema_rejects_non_integer_versions(self) -> None:
        bundle = {
            "kind": "translations",
            "bundle_id": "bundle-model-schema-fixture",
            "items": [],
        }
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                output = json.loads(
                    json.dumps(
                        {
                            "schema_version": schema_version,
                            "review_contract": REVIEW_CONTRACT,
                            "bundle_id": bundle["bundle_id"],
                            "findings": [],
                        }
                    )
                )
                with self.assertRaisesRegex(
                    ValidationError, "Pi review has an unsupported schema"
                ):
                    _validate_findings(bundle, output, strict=False)

    def test_translation_review_bundle_is_valid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("translations")
            payload.update(
                {
                    "component": "boot",
                    "items": [
                        {
                            "item_id": "translation-fixture",
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
            )
            path = self._write_bundle(Path(temporary), payload)
            self.assertEqual(validate_review_bundle(self.manifest, path)["kind"], "translations")

    def test_code_review_bundle_rejects_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("code")
            payload["files"] = [
                {
                    "item_id": "code-fixture",
                    "path": "/private/protected.lua",
                    "status": "M ",
                    "diff": "fixture",
                }
            ]
            path = self._write_bundle(Path(temporary), payload)
            with self.assertRaises(ValidationError):
                validate_review_bundle(self.manifest, path)

    def test_code_review_bundle_accepts_manifest_declared_files(self) -> None:
        declared = [
            component.copy_fragment
            for component in self.manifest.components
            if component.copy_fragment
        ]
        declared.extend(self.manifest.manual_definitions)
        self.assertTrue(declared)
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("code")
            payload["files"] = [
                {
                    "item_id": f"code-fixture-{index}",
                    "path": path,
                    "status": "M ",
                    "diff": "fixture",
                }
                for index, path in enumerate(declared)
            ]
            path = self._write_bundle(Path(temporary), payload)
            validated = validate_review_bundle(self.manifest, path)

        self.assertEqual(
            {item["path"] for item in validated["files"]}, set(declared)
        )

    def test_code_review_bundle_rejects_undeclared_root_lua(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("code")
            payload["files"] = [
                {
                    "item_id": "code-fixture",
                    "path": "undeclared-review-file.lua",
                    "status": "M ",
                    "diff": "fixture",
                }
            ]
            path = self._write_bundle(Path(temporary), payload)
            with self.assertRaises(ValidationError):
                validate_review_bundle(self.manifest, path)

    def test_review_bundle_redacts_absolute_paths(self) -> None:
        redacted, count = _redact_absolute_paths(
            "--- /dev/null\n"
            "+++ b/tools/new.py\n"
            "+path /Users/yun/projects/t-engine4/game/dlcs/file.lua\n"
            "--- a/tools/deleted.py\n"
            "+++ /dev/null\n"
        )
        self.assertEqual(count, 1)
        self.assertNotIn("/Users/yun", redacted)
        self.assertEqual(redacted.count("/dev/null"), 2)
        ordinary_dev_null, ordinary_count = _redact_absolute_paths("path /dev/null")
        self.assertEqual(ordinary_count, 1)
        self.assertNotIn("/dev/null", ordinary_dev_null)
        pattern, pattern_count = _redact_absolute_paths("gsub(\"([/])\")")
        self.assertEqual(pattern_count, 0)
        self.assertIn("([/])", pattern)

    def test_review_index_identity_ignores_run_local_paths(self) -> None:
        payload = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": self.manifest.version,
            "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            "scope": {"translations": False, "code": True, "protected_sources": False},
            "redacted_absolute_path_count": 0,
            "bundles": [
                {
                    "bundle_id": "bundle-fixture",
                    "kind": "code",
                    "offset": 0,
                    "count": 1,
                    "total": 1,
                    "path": "/first/run/bundle.json",
                }
            ],
            "run_directory": "/first/run",
            "index": "/first/run/review-index.json",
        }
        first = _review_index_id(payload)
        payload["run_directory"] = "/second/run"
        payload["index"] = "/second/run/review-index.json"
        payload["bundles"][0]["path"] = "/second/run/bundle.json"
        self.assertEqual(first, _review_index_id(payload))

    def test_strict_review_normalizes_host_finding_refs(self) -> None:
        bundle = self._base("code")
        bundle["files"] = [
            {
                "item_id": "code-b",
                "path": "tools/b.py",
                "status": "M ",
                "diff": "fixture",
            },
            {
                "item_id": "code-a",
                "path": "tools/a.py",
                "status": "M ",
                "diff": "fixture",
            },
        ]
        bundle["bundle_id"] = _bundle_id(bundle)
        output = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle["bundle_id"],
            "findings": [
                {
                    "finding_id": "model-b",
                    "severity": "minor",
                    "category": "code",
                    "item_id": "code-b",
                    "path": "tools/b.py",
                    "title": "B",
                    "body": "B body",
                },
                {
                    "finding_id": "model-a",
                    "severity": "major",
                    "category": "code",
                    "item_id": "code-a",
                    "path": "tools/a.py",
                    "title": "A",
                    "body": "A body",
                },
            ],
        }
        summary, normalized = _validate_findings(bundle, output, strict=True)
        self.assertEqual(summary["findings"], 2)
        self.assertEqual(
            [finding["finding_id"] for finding in normalized["findings"]],
            ["R-001", "R-002"],
        )
        self.assertEqual(
            [finding["model_finding_id"] for finding in normalized["findings"]],
            ["model-a", "model-b"],
        )
        self.assertEqual(len(normalized["decision_digest"]), 64)
        self.assertEqual(len(normalized["review_id"]), 64)

    def test_strict_review_rejects_unknown_model_fields(self) -> None:
        bundle = self._base("code")
        bundle["files"] = [
            {
                "item_id": "code-fixture",
                "path": "tools/i18n",
                "status": "M ",
                "diff": "fixture",
            }
        ]
        bundle["bundle_id"] = _bundle_id(bundle)
        output = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle["bundle_id"],
            "verdict": "approved",
            "findings": [],
        }
        with self.assertRaises(ValidationError):
            _validate_findings(bundle, output, strict=True)
        summary, normalized = _validate_findings(bundle, output, strict=False)
        self.assertEqual(summary["findings"], 0)
        self.assertNotIn("verdict", normalized)


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
                    patch("i18nlib.cli._manifest") as manifest_factory,
                    patch("i18nlib.cli.LuaRuntime") as runtime_factory,
                    patch("i18nlib.cli.LocaleLoader") as loader_factory,
                    patch("i18nlib.cli.resolve_context") as resolver,
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
            patch("i18nlib.cli._manifest", return_value=manifest) as manifest_factory,
            patch("i18nlib.cli.LuaRuntime") as runtime_factory,
            patch("i18nlib.cli.LocaleLoader") as loader_factory,
            patch("i18nlib.cli.resolve_context") as resolver,
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
                "kind": "translations",
                "component": "boot",
                "items": [
                    {
                        "item_id": "translation-fixture",
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
                "kind": "translations",
                "component": "boot",
                "items": [
                    {
                        "item_id": "translation-cache-fixture",
                        "component": "boot",
                        "section": "fixture/cache.lua",
                        "source": "Cache",
                        "target": "缓存",
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
            tmux_parser = pi_tmux_parser()
            headless_default = headless_parser.parse_args(["--bundle", str(bundle_path)])
            tmux_default = tmux_parser.parse_args(
                ["review-files", "--bundle", str(bundle_path)]
            )
            headless_explicit = headless_parser.parse_args(
                ["--bundle", str(bundle_path), "--cache"]
            )
            tmux_explicit = tmux_parser.parse_args(
                ["review-files", "--bundle", str(bundle_path), "--cache"]
            )
            headless_force = headless_parser.parse_args(
                ["--bundle", str(bundle_path), "--force"]
            )
            tmux_force = tmux_parser.parse_args(
                ["review-files", "--bundle", str(bundle_path), "--force"]
            )
            tmux_review_files_parser = next(
                action.choices["review-files"]
                for action in tmux_parser._actions
                if "review-files" in (getattr(action, "choices", None) or {})
            )
            headless_help = " ".join(headless_parser.format_help().split())
            tmux_help = " ".join(tmux_review_files_parser.format_help().split())
            self.assertFalse(headless_default.cache)
            self.assertFalse(tmux_default.cache)
            self.assertTrue(headless_explicit.cache)
            self.assertTrue(tmux_explicit.cache)
            self.assertTrue(headless_force.force)
            self.assertTrue(tmux_force.force)
            self.assertIn("--cache is rejected", headless_help)
            self.assertIn("always true for file-reading reviews", headless_help)
            self.assertIn("--cache is rejected", tmux_help)
            self.assertIn("always true for file-reading reviews", tmux_help)

            for entry_point, arguments in (
                (
                    pi_file_review_main,
                    ["--bundle", str(bundle_path), "--cache"],
                ),
                (
                    pi_tmux_main,
                    ["review-files", "--bundle", str(bundle_path), "--cache"],
                ),
            ):
                with self.subTest(entry_point=entry_point.__module__):
                    stderr = io.StringIO()
                    with contextlib.redirect_stderr(stderr):
                        exit_code = entry_point(arguments)
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
                    use_cache=tmux_explicit.cache,
                    force=False,
                    pi_executable=str(directory / "does-not-exist"),
                    tmux_executable=str(directory / "does-not-exist"),
                )

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


class PiReviewBatchTests(unittest.TestCase):
    @staticmethod
    def _load_batch_module():
        script = TOOLS / "pi-review-batch.py"
        spec = importlib.util.spec_from_file_location(
            "pi_review_batch_test", script
        )
        assert spec is not None
        assert spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        with patch("signal.alarm") as import_alarm:
            spec.loader.exec_module(module)
        return module, import_alarm.call_args_list

    def setUp(self) -> None:
        self.batch, import_alarm_calls = self._load_batch_module()
        self.assertEqual(import_alarm_calls, [])

    @staticmethod
    def _write_index(
        directory: Path, bundles: list[dict[str, str]]
    ) -> Path:
        index_path = directory / "index.json"
        index_path.write_text(
            json.dumps({"bundles": bundles}),
            encoding="utf-8",
        )
        return index_path

    def _prepare_summary_root(self, directory: Path) -> Path:
        summary_directory = directory / ".artifacts" / "i18n"
        summary_directory.mkdir(parents=True)
        self.batch.ROOT = directory
        return summary_directory / "pi-batch-summary.json"

    def test_stale_review_does_not_skip_runner_and_uses_index_ids(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pi-review-batch-test-"
        ) as temporary:
            directory = Path(temporary)
            summary_path = self._prepare_summary_root(directory)
            first_path = directory / "first" / "shared-name.json"
            second_path = directory / "second" / "shared-name.json"
            index_path = self._write_index(
                directory,
                [
                    {"bundle_id": "index-id-ok", "path": str(first_path)},
                    {
                        "bundle_id": "index-id-failed",
                        "path": str(second_path),
                    },
                ],
            )
            stale_path = (
                directory / "runs" / "stale-pi-review" / "review.json"
            )
            stale_path.parent.mkdir(parents=True)
            stale_path.write_text(
                json.dumps({"bundle_id": "index-id-ok"}),
                encoding="utf-8",
            )
            # A legacy implementation consults this glob and skips the call.
            self.batch.RUNS_GLOB = str(
                directory / "runs" / "*pi-review" / "review.json"
            )

            def fake_run(command, **_):
                returncode = 0 if command[2] == str(first_path) else 1
                return subprocess.CompletedProcess(
                    command,
                    returncode,
                    stdout=(
                        "review: fixture-review.json\n"
                        if returncode == 0
                        else ""
                    ),
                    stderr="ordinary failure",
                )

            with (
                patch.object(
                    self.batch.subprocess, "run", side_effect=fake_run
                ) as runner,
                patch.object(self.batch.signal, "alarm") as alarm,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                exit_code = self.batch.main(
                    [
                        "--index",
                        str(index_path),
                        "--workers",
                        "1",
                        "--retries",
                        "0",
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertEqual(runner.call_count, 2)
            self.assertEqual(alarm.call_args_list, [call(14400), call(0)])
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["total"], 2)
            self.assertEqual(summary["ok"], 1)
            self.assertEqual(summary["failed"], ["index-id-failed"])

    def test_force_is_forwarded_to_each_runner_call(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pi-review-batch-force-"
        ) as temporary:
            directory = Path(temporary)
            self._prepare_summary_root(directory)
            bundle_path = directory / "filename-is-not-id.json"
            index_path = self._write_index(
                directory,
                [
                    {
                        "bundle_id": "authoritative-index-id",
                        "path": str(bundle_path),
                    }
                ],
            )
            completed = subprocess.CompletedProcess(
                [], 0, stdout="review: fixture-review.json\n", stderr=""
            )
            with (
                patch.object(
                    self.batch.subprocess, "run", return_value=completed
                ) as runner,
                patch.object(self.batch.signal, "alarm"),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                exit_code = self.batch.main(
                    [
                        "--index",
                        str(index_path),
                        "--workers",
                        "1",
                        "--retries",
                        "0",
                        "--force",
                    ]
                )

            self.assertEqual(exit_code, 0)
            runner.assert_called_once_with(
                [
                    str(self.batch.PI_REVIEW),
                    "--bundle",
                    str(bundle_path),
                    "--force",
                ],
                capture_output=True,
                text=True,
                timeout=1250,
            )

    def test_empty_stdout_retries_once_then_nonempty_succeeds(self) -> None:
        cases = (
            ("empty", "", ""),
            ("whitespace", " \t\n", ""),
            ("stderr", "", "fixture stderr"),
        )
        for label, first_stdout, first_stderr in cases:
            with self.subTest(label=label):
                progress = self.batch.Progress(1)
                empty = subprocess.CompletedProcess(
                    [],
                    0,
                    stdout=first_stdout,
                    stderr=first_stderr,
                )
                success = subprocess.CompletedProcess(
                    [],
                    0,
                    stdout="opaque success response\n",
                    stderr="",
                )
                output = io.StringIO()
                with (
                    patch.object(
                        self.batch.subprocess,
                        "run",
                        side_effect=[empty, success],
                    ) as runner,
                    patch.object(self.batch.time, "sleep") as sleep,
                    contextlib.redirect_stdout(output),
                ):
                    bundle_id, ok = self.batch.run_one(
                        "index-bundle-id",
                        "/tmp/bundle.json",
                        1,
                        progress,
                    )
                progress.pump()

                self.assertEqual((bundle_id, ok), ("index-bundle-id", True))
                self.assertEqual(runner.call_count, 2)
                sleep.assert_called_once_with(10)
                self.assertEqual(
                    (progress.done, progress.ok, progress.failed),
                    (1, 1, 0),
                )
                diagnostic = output.getvalue()
                self.assertIn("empty response", diagnostic)
                if first_stderr:
                    self.assertIn(first_stderr, diagnostic)

    def test_empty_stdout_exhaustion_ticks_failure_once(self) -> None:
        cases = (
            ("empty", "", ""),
            ("whitespace", " \t\n", ""),
            ("stderr", "", "fixture stderr"),
        )
        for label, response_stdout, response_stderr in cases:
            with self.subTest(label=label):
                progress = self.batch.Progress(1)
                empty = subprocess.CompletedProcess(
                    [],
                    0,
                    stdout=response_stdout,
                    stderr=response_stderr,
                )
                output = io.StringIO()
                with (
                    patch.object(
                        self.batch.subprocess,
                        "run",
                        side_effect=[empty, empty, empty],
                    ) as runner,
                    patch.object(self.batch.time, "sleep") as sleep,
                    contextlib.redirect_stdout(output),
                ):
                    bundle_id, ok = self.batch.run_one(
                        "index-bundle-id",
                        "/tmp/bundle.json",
                        2,
                        progress,
                    )
                progress.pump()

                self.assertEqual((bundle_id, ok), ("index-bundle-id", False))
                self.assertEqual(runner.call_count, 3)
                self.assertEqual(sleep.call_args_list, [call(10), call(20)])
                self.assertEqual(
                    (progress.done, progress.ok, progress.failed),
                    (1, 0, 1),
                )
                diagnostic = output.getvalue()
                self.assertIn("empty response", diagnostic)
                if response_stderr:
                    self.assertIn(response_stderr, diagnostic)

    def test_empty_stdout_with_zero_retries_fails_batch_without_sleep(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pi-review-batch-empty-"
        ) as temporary:
            directory = Path(temporary)
            summary_path = self._prepare_summary_root(directory)
            bundle_path = directory / "bundle.json"
            index_path = self._write_index(
                directory,
                [
                    {
                        "bundle_id": "empty-response-id",
                        "path": str(bundle_path),
                    }
                ],
            )
            empty = subprocess.CompletedProcess(
                [],
                0,
                stdout="",
                stderr="fixture stderr",
            )
            output = io.StringIO()
            with (
                patch.object(
                    self.batch.subprocess, "run", return_value=empty
                ) as runner,
                patch.object(self.batch.time, "sleep") as sleep,
                patch.object(self.batch.signal, "alarm") as alarm,
                contextlib.redirect_stdout(output),
            ):
                exit_code = self.batch.main(
                    [
                        "--index",
                        str(index_path),
                        "--workers",
                        "1",
                        "--retries",
                        "0",
                    ]
                )

            self.assertEqual(exit_code, 1)
            runner.assert_called_once_with(
                [
                    str(self.batch.PI_REVIEW),
                    "--bundle",
                    str(bundle_path),
                ],
                capture_output=True,
                text=True,
                timeout=1250,
            )
            sleep.assert_not_called()
            self.assertEqual(alarm.call_args_list, [call(14400), call(0)])
            diagnostic = output.getvalue()
            self.assertIn("empty response", diagnostic)
            self.assertIn("fixture stderr", diagnostic)
            self.assertIn("[1/1] ok=0 fail=1", diagnostic)
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(
                summary,
                {
                    "index": str(index_path),
                    "total": 1,
                    "ok": 0,
                    "failed": ["empty-response-id"],
                },
            )

    def test_numeric_argument_boundaries_and_limit_zero(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="pi-review-batch-args-"
        ) as temporary:
            directory = Path(temporary)
            index_path = self._write_index(
                directory,
                [
                    {
                        "bundle_id": "not-selected",
                        "path": str(directory / "bundle.json"),
                    }
                ],
            )
            with (
                patch.object(self.batch.subprocess, "run") as runner,
                patch.object(self.batch.signal, "alarm") as alarm,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                exit_code = self.batch.main(
                    [
                        "--index",
                        str(index_path),
                        "--workers",
                        "1",
                        "--retries",
                        "0",
                        "--skip",
                        "0",
                        "--limit",
                        "0",
                    ]
                )
            self.assertEqual(exit_code, 0)
            runner.assert_not_called()
            self.assertEqual(alarm.call_args_list, [call(14400), call(0)])

            for option, value in (
                ("--workers", "0"),
                ("--retries", "-1"),
                ("--skip", "-1"),
                ("--limit", "-1"),
            ):
                with self.subTest(option=option):
                    with (
                        patch.object(self.batch.signal, "alarm") as alarm,
                        contextlib.redirect_stderr(io.StringIO()),
                    ):
                        with self.assertRaises(SystemExit) as caught:
                            self.batch.main(
                                ["--index", str(index_path), option, value]
                            )
                    self.assertEqual(caught.exception.code, 2)
                    self.assertEqual(
                        alarm.call_args_list,
                        [call(14400), call(0)],
                    )

    def test_no_sleep_after_final_failure_or_timeout(self) -> None:
        failures = (
            subprocess.CompletedProcess(
                [],
                1,
                stdout="",
                stderr="ordinary nonzero exit",
            ),
            subprocess.CompletedProcess(
                [],
                1,
                stdout="",
                stderr="validation failed: fixture",
            ),
            subprocess.TimeoutExpired("fixture", 1250),
        )
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                progress = self.batch.Progress(1)
                with (
                    patch.object(
                        self.batch.subprocess,
                        "run",
                        side_effect=[failure, failure],
                    ) as runner,
                    patch.object(self.batch.time, "sleep") as sleep,
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    bundle_id, ok = self.batch.run_one(
                        "index-bundle-id",
                        "/tmp/not-the-index-id.json",
                        1,
                        progress,
                    )
                progress.pump()

                self.assertEqual(bundle_id, "index-bundle-id")
                self.assertFalse(ok)
                self.assertEqual(runner.call_count, 2)
                sleep.assert_called_once_with(10)
                self.assertEqual(progress.done, 1)
                self.assertEqual(progress.failed, 1)


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
        bundle_path = directory / "bundle.json"
        bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
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
                            "review",
                            "--bundle",
                            "unused-bundle.json",
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
            _, bundle_path = self._review_bundle(directory)
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


class QualityConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    @classmethod
    def _current_taxonomy(cls) -> dict[str, object]:
        path = cls.manifest.root / "i18n" / "quality" / "taxonomy-v1.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @classmethod
    def _current_policy(cls) -> dict[str, object]:
        path = cls.manifest.root / "i18n" / "quality" / "policy-v1.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write_taxonomy(root: Path, taxonomy: dict[str, object]) -> None:
        path = root / "i18n" / "quality" / "taxonomy-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(taxonomy, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _write_policy(root: Path, policy: dict[str, object]) -> None:
        path = root / "i18n" / "quality" / "policy-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(policy, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _mutate_policy_path(
        policy: dict[str, object],
        path: tuple[str | int, ...],
        value: object,
        delete: object,
    ) -> None:
        parent: object = policy
        for part in path[:-1]:
            parent = parent[part]  # type: ignore[index]
        if value is delete:
            del parent[path[-1]]  # type: ignore[index]
        else:
            parent[path[-1]] = value  # type: ignore[index]

    def test_quality_taxonomy_loads_current_file_without_normalization(self) -> None:
        original = self._current_taxonomy()
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-taxonomy-valid-"
        ) as temporary:
            root = Path(temporary)
            self._write_taxonomy(root, copy.deepcopy(original))
            manifest = replace(self.manifest, root=root)
            loaded = load_taxonomy(manifest)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(loaded, original)
        self.assertEqual(canonical(loaded), canonical(original))
        with patch.object(quality_module, "_read_json", return_value=original):
            self.assertIs(load_taxonomy(self.manifest), original)

    def test_quality_taxonomy_rejects_malformed_consumed_fields(self) -> None:
        original = self._current_taxonomy()
        delete = object()
        profiles_without_ui = [
            item for item in original["profiles"] if item["id"] != "ui"  # type: ignore[index]
        ]
        severities_without_note = [
            item
            for item in original["severities"]  # type: ignore[union-attr]
            if item["id"] != "note"
        ]
        confidence_without_c4 = [
            item
            for item in original["confidence_levels"]  # type: ignore[union-attr]
            if item["id"] != "C4"
        ]
        grades_without_gold = [
            item
            for item in original["grades"]  # type: ignore[union-attr]
            if item["id"] != "Gold"
        ]
        reuse_without_no_reuse = [
            item
            for item in original["reuse_scopes"]  # type: ignore[union-attr]
            if item["id"] != "no-reuse"
        ]
        duplicate_merge_pairs = copy.deepcopy(original["mergeable_codes"])
        duplicate_merge_pairs.append(  # type: ignore[union-attr]
            list(reversed(duplicate_merge_pairs[0]))  # type: ignore[index]
        )
        cases = (
            (
                "contract-list",
                ("contract",),
                [],
                "quality taxonomy.contract",
            ),
            (
                "schema-bool",
                ("schema_version",),
                True,
                "quality taxonomy.schema_version",
            ),
            ("profiles-bool", ("profiles",), True, "quality taxonomy.profiles"),
            (
                "severities-string",
                ("severities",),
                "minor",
                "quality taxonomy.severities",
            ),
            (
                "error-codes-empty",
                ("error_codes",),
                [],
                "quality taxonomy.error_codes",
            ),
            (
                "reuse-item-list",
                ("reuse_scopes", 0),
                [],
                "quality taxonomy.reuse_scopes[0]",
            ),
            (
                "confidence-id-bool",
                ("confidence_levels", 0, "id"),
                True,
                "quality taxonomy.confidence_levels[0].id",
            ),
            (
                "grade-id-duplicate",
                ("grades", 1, "id"),
                original["grades"][0]["id"],  # type: ignore[index]
                "quality taxonomy.grades[1].id",
            ),
            (
                "required-profile-missing",
                ("profiles",),
                profiles_without_ui,
                "quality taxonomy.profiles",
            ),
            (
                "exact-severity-missing",
                ("severities",),
                severities_without_note,
                "quality taxonomy.severities",
            ),
            (
                "exact-confidence-missing",
                ("confidence_levels",),
                confidence_without_c4,
                "quality taxonomy.confidence_levels",
            ),
            (
                "exact-grade-missing",
                ("grades",),
                grades_without_gold,
                "quality taxonomy.grades",
            ),
            (
                "exact-reuse-missing",
                ("reuse_scopes",),
                reuse_without_no_reuse,
                "quality taxonomy.reuse_scopes",
            ),
            (
                "categories-item-list",
                ("error_categories", 0),
                [],
                "quality taxonomy.error_categories[0]",
            ),
            (
                "vector-string",
                ("quality_vector_dimensions",),
                "accuracy",
                "quality taxonomy.quality_vector_dimensions",
            ),
            (
                "risk-flag-duplicate",
                ("risk_flags", 1),
                original["risk_flags"][0],  # type: ignore[index]
                "quality taxonomy.risk_flags[1]",
            ),
            (
                "error-category-reference",
                ("error_codes", 0, "category"),
                "unknown-category",
                "quality taxonomy.error_codes[0].category",
            ),
            (
                "error-severity-reference",
                ("error_codes", 0, "default_severity"),
                "critical",
                "quality taxonomy.error_codes[0].default_severity",
            ),
            (
                "source-tag-map-list",
                ("source_tag_profiles",),
                [],
                "quality taxonomy.source_tag_profiles",
            ),
            (
                "source-tag-empty-key",
                ("source_tag_profiles",),
                {"": "ui"},
                "quality taxonomy.source_tag_profiles['']",
            ),
            (
                "term-profile-reference",
                ("term_category_profiles", "T.GAME.TALENT"),
                "missing-profile",
                "quality taxonomy.term_category_profiles['T.GAME.TALENT']",
            ),
            (
                "section-rules-bool",
                ("section_pattern_profiles",),
                True,
                "quality taxonomy.section_pattern_profiles",
            ),
            (
                "section-rule-item-list",
                ("section_pattern_profiles", 0),
                [],
                "quality taxonomy.section_pattern_profiles[0]",
            ),
            (
                "section-pattern-empty",
                ("section_pattern_profiles", 0, "pattern"),
                "",
                "quality taxonomy.section_pattern_profiles[0].pattern",
            ),
            (
                "section-profile-reference",
                ("section_pattern_profiles", 0, "profile"),
                "missing-profile",
                "quality taxonomy.section_pattern_profiles[0].profile",
            ),
            (
                "section-confidence",
                ("section_pattern_profiles", 0, "confidence"),
                "certain",
                "quality taxonomy.section_pattern_profiles[0].confidence",
            ),
            (
                "length-id-duplicate",
                ("length_bins", 1, "id"),
                original["length_bins"][0]["id"],  # type: ignore[index]
                "quality taxonomy.length_bins[1].id",
            ),
            (
                "length-max-bool",
                ("length_bins", 0, "max"),
                True,
                "quality taxonomy.length_bins[0].max",
            ),
            (
                "length-max-out-of-order",
                ("length_bins", 1, "max"),
                10,
                "quality taxonomy.length_bins[1].max",
            ),
            (
                "length-null-before-last",
                ("length_bins", 0, "max"),
                None,
                "quality taxonomy.length_bins[0].max",
            ),
            (
                "length-last-not-null",
                ("length_bins", 3, "max"),
                300,
                "quality taxonomy.length_bins[3].max",
            ),
            (
                "length-max-missing",
                ("length_bins", 0, "max"),
                delete,
                "quality taxonomy.length_bins[0].max",
            ),
            (
                "classifier-version-empty",
                ("profile_classifier_version",),
                "",
                "quality taxonomy.profile_classifier_version",
            ),
            (
                "risk-version-list",
                ("risk_rule_version",),
                [],
                "quality taxonomy.risk_rule_version",
            ),
            (
                "merge-pair-not-two",
                ("mergeable_codes", 0),
                ["ACC_OMISSION"],
                "quality taxonomy.mergeable_codes[0]",
            ),
            (
                "merge-pair-same",
                ("mergeable_codes", 0),
                ["ACC_OMISSION", "ACC_OMISSION"],
                "quality taxonomy.mergeable_codes[0][1]",
            ),
            (
                "merge-pair-unknown",
                ("mergeable_codes", 0),
                ["ACC_OMISSION", "UNKNOWN_CODE"],
                "quality taxonomy.mergeable_codes[0][1]",
            ),
            (
                "merge-pair-unordered-duplicate",
                ("mergeable_codes",),
                duplicate_merge_pairs,
                f"quality taxonomy.mergeable_codes["
                f"{len(duplicate_merge_pairs) - 1}]",
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-taxonomy-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(self.manifest, root=root)
            for name, field_path, value, error_path in cases:
                with self.subTest(name=name):
                    taxonomy = copy.deepcopy(original)
                    self._mutate_policy_path(
                        taxonomy, field_path, value, delete
                    )
                    self._write_taxonomy(root, taxonomy)
                    with self.assertRaises(ConfigurationError) as raised:
                        load_taxonomy(manifest)
                    self.assertIn(error_path, str(raised.exception))

    def test_quality_taxonomy_read_errors_are_configuration_errors(self) -> None:
        cases = (("missing", None), ("invalid-json", "{"), ("non-object", "[]"))
        for name, payload in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="tome4-quality-taxonomy-read-error-"
            ) as temporary:
                root = Path(temporary)
                if payload is not None:
                    path = root / "i18n" / "quality" / "taxonomy-v1.json"
                    path.parent.mkdir(parents=True)
                    path.write_text(payload, encoding="utf-8")
                with self.assertRaises(ConfigurationError) as raised:
                    load_taxonomy(replace(self.manifest, root=root))
                self.assertIn("quality taxonomy.root", str(raised.exception))

    def test_invalid_taxonomy_blocks_downstream_quality_inputs(self) -> None:
        taxonomy = self._current_taxonomy()
        taxonomy["profiles"] = True
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-taxonomy-preflight-"
        ) as temporary:
            root = Path(temporary)
            self._write_taxonomy(root, taxonomy)
            self._write_policy(root, self._current_policy())
            manifest = replace(self.manifest, root=root)
            loader = Mock(spec=LocaleLoader)

            with (
                patch.object(
                    quality_module,
                    "load_quality_policy",
                    wraps=load_quality_policy,
                ) as load_policy_mock,
                patch.object(
                    quality_module,
                    "load_taxonomy",
                    wraps=load_taxonomy,
                ) as load_taxonomy_mock,
                patch.object(
                    quality_module, "_load_terminology"
                ) as load_terminology_mock,
            ):
                with self.assertRaises(ConfigurationError):
                    build_inventory(manifest, loader)
            load_policy_mock.assert_called_once_with(manifest)
            load_taxonomy_mock.assert_called_once_with(manifest)
            load_terminology_mock.assert_not_called()
            loader.load_path.assert_not_called()

            with patch.object(
                quality_module, "read_inventory_file"
            ) as read_inventory_mock:
                with self.assertRaises(ConfigurationError):
                    generate_sample(manifest, root / "unused-inventory.jsonl")
            read_inventory_mock.assert_not_called()

    def test_invalid_policy_blocks_all_inventory_inputs(self) -> None:
        policy = copy.deepcopy(self._current_policy())
        policy["dry_run"]["coverage_constraints"][0]["values"] = [True]
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-inventory-preflight-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, policy)
            manifest = replace(self.manifest, root=root)
            loader = Mock(spec=LocaleLoader)

            with (
                patch.object(
                    quality_module, "load_taxonomy"
                ) as load_taxonomy_mock,
                patch.object(
                    quality_module, "_load_terminology"
                ) as load_terminology_mock,
            ):
                with self.assertRaises(ConfigurationError) as raised:
                    build_inventory(manifest, loader)

        self.assertIn(
            "quality policy.dry_run.coverage_constraints[0].values[0]",
            str(raised.exception),
        )
        load_taxonomy_mock.assert_not_called()
        load_terminology_mock.assert_not_called()
        loader.load_path.assert_not_called()

    def test_inventory_loads_config_once_in_preflight_order(self) -> None:
        policy = self._current_policy()
        taxonomy = self._current_taxonomy()
        component = replace(
            self.manifest.components[0],
            translation="fixture.lua",
            copy_fragment=None,
        )
        manifest = replace(self.manifest, components=(component,))
        loader = Mock(spec=LocaleLoader)
        document = LocaleDocument(
            logical_path="fixture.lua",
            sha256="0" * 64,
            records=(),
        )
        events: list[str] = []

        def tracked_policy(candidate: Manifest) -> dict[str, object]:
            self.assertIs(candidate, manifest)
            events.append("policy")
            return policy

        def tracked_taxonomy(candidate: Manifest) -> dict[str, object]:
            self.assertIs(candidate, manifest)
            events.append("taxonomy")
            return taxonomy

        def tracked_terminology(path: Path) -> tuple[list[dict[str, str]], str]:
            self.assertEqual(path, manifest.root / manifest.terminology)
            events.append("terminology")
            return [], "1" * 64

        def tracked_locale(*args: object, **kwargs: object) -> LocaleDocument:
            events.append("locale")
            return document

        loader.load_path.side_effect = tracked_locale
        with (
            patch.object(
                quality_module,
                "load_quality_policy",
                side_effect=tracked_policy,
            ) as load_policy_mock,
            patch.object(
                quality_module,
                "load_taxonomy",
                side_effect=tracked_taxonomy,
            ) as load_taxonomy_mock,
            patch.object(
                quality_module,
                "_load_terminology",
                side_effect=tracked_terminology,
            ) as load_terminology_mock,
        ):
            inventory = build_inventory(manifest, loader)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(events, ["policy", "taxonomy", "terminology", "locale"])
        load_policy_mock.assert_called_once_with(manifest)
        load_taxonomy_mock.assert_called_once_with(manifest)
        load_terminology_mock.assert_called_once_with(
            manifest.root / manifest.terminology
        )
        loader.load_path.assert_called_once_with(
            manifest.root / "fixture.lua", logical_path="fixture.lua"
        )
        self.assertEqual(inventory["policy_sha256"], canonical(policy))
        self.assertEqual(inventory["taxonomy_sha256"], canonical(taxonomy))

    def test_quality_policy_loads_current_file_without_normalization(self) -> None:
        original = self._current_policy()
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-valid-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, copy.deepcopy(original))
            manifest = replace(self.manifest, root=root)
            loaded = load_quality_policy(manifest)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(loaded, original)
        self.assertEqual(canonical(loaded), canonical(original))
        with patch.object(quality_module, "_read_json", return_value=original):
            self.assertIs(load_quality_policy(self.manifest), original)

    def test_quality_policy_rejects_malformed_consumed_fields(self) -> None:
        delete = object()
        cases = (
            ("strict-missing", ("strict_unknown_fields",), delete, "quality policy.strict_unknown_fields"),
            ("strict-int", ("strict_unknown_fields",), 1, "quality policy.strict_unknown_fields"),
            ("pilot-missing", ("pilot",), delete, "quality policy.pilot"),
            ("pilot-not-object", ("pilot",), [], "quality policy.pilot"),
            ("pilot-seed-empty", ("pilot", "seed"), "", "quality policy.pilot.seed"),
            ("pilot-size-bool", ("pilot", "size"), True, "quality policy.pilot.size"),
            ("pilot-size-string", ("pilot", "size"), "120", "quality policy.pilot.size"),
            ("pilot-size-zero", ("pilot", "size"), 0, "quality policy.pilot.size"),
            ("buckets-not-object", ("pilot", "buckets"), [], "quality policy.pilot.buckets"),
            (
                "bucket-missing",
                ("pilot", "buckets", "contrast"),
                delete,
                "quality policy.pilot.buckets.contrast",
            ),
            (
                "bucket-extra",
                ("pilot", "buckets"),
                {"representative": 60, "risk-enriched": 40, "contrast": 20, "extra": 1},
                "quality policy.pilot.buckets['extra']",
            ),
            (
                "bucket-string",
                ("pilot", "buckets", "representative"),
                "60",
                "quality policy.pilot.buckets.representative",
            ),
            (
                "bucket-bool",
                ("pilot", "buckets", "representative"),
                True,
                "quality policy.pilot.buckets.representative",
            ),
            (
                "bucket-sum",
                ("pilot", "buckets", "representative"),
                61,
                "quality policy.pilot.buckets",
            ),
            (
                "one-evaluator",
                ("pilot", "evaluator_ids"),
                ["reviewer-a"],
                "quality policy.pilot.evaluator_ids",
            ),
            (
                "empty-evaluator",
                ("pilot", "evaluator_ids"),
                ["reviewer-a", ""],
                "quality policy.pilot.evaluator_ids[1]",
            ),
            (
                "duplicate-evaluator",
                ("pilot", "evaluator_ids"),
                ["same", "same"],
                "quality policy.pilot.evaluator_ids[1]",
            ),
            (
                "method-version-empty",
                ("pilot", "method_version"),
                "",
                "quality policy.pilot.method_version",
            ),
            ("dry-run-missing", ("dry_run",), delete, "quality policy.dry_run"),
            ("dry-run-not-object", ("dry_run",), [], "quality policy.dry_run"),
            ("dry-seed-empty", ("dry_run", "seed"), "", "quality policy.dry_run.seed"),
            ("dry-size-string", ("dry_run", "size"), "12", "quality policy.dry_run.size"),
            ("dry-size-bool", ("dry_run", "size"), True, "quality policy.dry_run.size"),
            (
                "dry-contract",
                ("dry_run", "contract"),
                "wrong-contract",
                "quality policy.dry_run.contract",
            ),
            (
                "dry-constraints-missing",
                ("dry_run", "coverage_constraints"),
                delete,
                "quality policy.dry_run.coverage_constraints",
            ),
            (
                "constraints-missing",
                ("coverage_constraints",),
                delete,
                "quality policy.coverage_constraints",
            ),
            (
                "risk-flags-not-list",
                ("risk_enrichment_flags",),
                {},
                "quality policy.risk_enrichment_flags",
            ),
            (
                "risk-flag-empty",
                ("risk_enrichment_flags",),
                [""],
                "quality policy.risk_enrichment_flags[0]",
            ),
            (
                "risk-flag-duplicate",
                ("risk_enrichment_flags",),
                ["same", "same"],
                "quality policy.risk_enrichment_flags[1]",
            ),
            (
                "groups-not-object",
                ("component_groups",),
                [],
                "quality policy.component_groups",
            ),
            (
                "group-empty-name",
                ("component_groups",),
                {"": ["engine"]},
                "quality policy.component_groups['']",
            ),
            (
                "group-members-not-list",
                ("component_groups", "core"),
                "engine",
                "quality policy.component_groups['core']",
            ),
            (
                "group-member-empty",
                ("component_groups", "core"),
                [""],
                "quality policy.component_groups['core'][0]",
            ),
            (
                "group-member-duplicate",
                ("component_groups", "core"),
                ["engine", "engine"],
                "quality policy.component_groups['core'][1]",
            ),
            (
                "component-crosses-groups",
                ("component_groups",),
                {"a": ["shared"], "b": ["shared"]},
                "quality policy.component_groups['b'][0]",
            ),
            (
                "neighbor-limit-bool",
                ("context_neighbor_limit",),
                True,
                "quality policy.context_neighbor_limit",
            ),
            (
                "neighbor-limit-negative",
                ("context_neighbor_limit",),
                -1,
                "quality policy.context_neighbor_limit",
            ),
            (
                "contrast-max-float",
                ("contrast_group_max_size",),
                6.0,
                "quality policy.contrast_group_max_size",
            ),
            (
                "contrast-max-small",
                ("contrast_group_max_size",),
                1,
                "quality policy.contrast_group_max_size",
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(self.manifest, root=root)
            for name, field_path, value, error_path in cases:
                with self.subTest(name=name):
                    policy = copy.deepcopy(self._current_policy())
                    self._mutate_policy_path(policy, field_path, value, delete)
                    self._write_policy(root, policy)
                    with self.assertRaises(ConfigurationError) as raised:
                        load_quality_policy(manifest)
                    self.assertIn(error_path, str(raised.exception))

    def test_quality_policy_rejects_malformed_constraints(self) -> None:
        valid_string = {
            "id": "fixture",
            "mode": "each",
            "feature": "profile",
            "min": 0,
            "values": ["fixture-profile"],
            "description": "fixture",
        }
        cases = (
            ("root-not-list", ("coverage_constraints",), {}, "quality policy.coverage_constraints"),
            ("item-not-object", ("coverage_constraints",), [[]], "quality policy.coverage_constraints[0]"),
            (
                "id-empty",
                ("coverage_constraints",),
                [{**valid_string, "id": ""}],
                "quality policy.coverage_constraints[0].id",
            ),
            (
                "id-duplicate",
                ("coverage_constraints",),
                [valid_string, {**valid_string}],
                "quality policy.coverage_constraints[1].id",
            ),
            (
                "mode-unknown",
                ("coverage_constraints",),
                [{**valid_string, "mode": "all"}],
                "quality policy.coverage_constraints[0].mode",
            ),
            (
                "mode-unhashable",
                ("coverage_constraints",),
                [{**valid_string, "mode": []}],
                "quality policy.coverage_constraints[0].mode",
            ),
            (
                "feature-unknown",
                ("coverage_constraints",),
                [{**valid_string, "feature": "taxonomy-only"}],
                "quality policy.coverage_constraints[0].feature",
            ),
            (
                "feature-unhashable",
                ("coverage_constraints",),
                [{**valid_string, "feature": {}}],
                "quality policy.coverage_constraints[0].feature",
            ),
            (
                "min-bool",
                ("coverage_constraints",),
                [{**valid_string, "min": True}],
                "quality policy.coverage_constraints[0].min",
            ),
            (
                "min-negative",
                ("coverage_constraints",),
                [{**valid_string, "min": -1}],
                "quality policy.coverage_constraints[0].min",
            ),
            (
                "values-empty",
                ("coverage_constraints",),
                [{**valid_string, "values": []}],
                "quality policy.coverage_constraints[0].values",
            ),
            (
                "value-unhashable",
                ("coverage_constraints",),
                [{**valid_string, "values": [["nested"]]}],
                "quality policy.coverage_constraints[0].values[0]",
            ),
            (
                "value-duplicate",
                ("coverage_constraints",),
                [{**valid_string, "values": ["same", "same"]}],
                "quality policy.coverage_constraints[0].values[1]",
            ),
            (
                "string-feature-bool",
                ("coverage_constraints",),
                [{**valid_string, "values": [True]}],
                "quality policy.coverage_constraints[0].values[0]",
            ),
            (
                "bool-feature-int",
                ("coverage_constraints",),
                [
                    {
                        **valid_string,
                        "feature": "structural_risk",
                        "values": [1],
                    }
                ],
                "quality policy.coverage_constraints[0].values[0]",
            ),
            (
                "description-not-string",
                ("coverage_constraints",),
                [{**valid_string, "description": None}],
                "quality policy.coverage_constraints[0].description",
            ),
            (
                "dry-not-list",
                ("dry_run", "coverage_constraints"),
                {},
                "quality policy.dry_run.coverage_constraints",
            ),
            (
                "dry-id-empty",
                ("dry_run", "coverage_constraints"),
                [{**valid_string, "id": ""}],
                "quality policy.dry_run.coverage_constraints[0].id",
            ),
        )

        delete = object()
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-constraint-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(self.manifest, root=root)
            for name, field_path, value, error_path in cases:
                with self.subTest(name=name):
                    policy = copy.deepcopy(self._current_policy())
                    self._mutate_policy_path(policy, field_path, value, delete)
                    self._write_policy(root, policy)
                    with self.assertRaises(ConfigurationError) as raised:
                        load_quality_policy(manifest)
                    self.assertIn(error_path, str(raised.exception))

    def test_quality_policy_does_not_cross_validate_taxonomy_values(self) -> None:
        policy = copy.deepcopy(self._current_policy())
        policy["coverage_constraints"] = [
            {
                "id": "unknown-profile",
                "mode": "each",
                "feature": "profile",
                "min": 0,
                "values": ["not-in-taxonomy"],
            },
            {
                "id": "unknown-component-group",
                "mode": "any",
                "feature": "component_group",
                "min": 0,
                "values": ["not-in-component-groups"],
            },
        ]
        policy["risk_enrichment_flags"] = ["not-in-taxonomy"]
        policy["component_groups"] = {"fixture-group": ["fixture-component"]}
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-no-taxonomy-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, policy)
            loaded = load_quality_policy(replace(self.manifest, root=root))
        self.assertEqual(loaded, policy)

    def test_generate_sample_rejects_policy_before_taxonomy_or_inventory(self) -> None:
        policy = copy.deepcopy(self._current_policy())
        policy["pilot"]["evaluator_ids"] = ["reviewer-a"]
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-preflight-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, policy)
            manifest = replace(self.manifest, root=root)
            with (
                patch.object(quality_module, "load_taxonomy") as load_taxonomy_mock,
                patch.object(
                    quality_module, "read_inventory_file"
                ) as read_inventory_mock,
            ):
                with self.assertRaises(ConfigurationError) as raised:
                    generate_sample(manifest, root / "unused-inventory.jsonl")
        self.assertIn(
            "quality policy.pilot.evaluator_ids", str(raised.exception)
        )
        load_taxonomy_mock.assert_not_called()
        read_inventory_mock.assert_not_called()

    def test_quality_policy_read_errors_are_configuration_errors(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-read-error-"
        ) as temporary:
            root = Path(temporary)
            path = root / "i18n" / "quality" / "policy-v1.json"
            path.parent.mkdir(parents=True)
            manifest = replace(self.manifest, root=root)
            for name, payload in (("invalid-json", "{"), ("non-object", "[]")):
                with self.subTest(name=name):
                    path.write_text(payload, encoding="utf-8")
                    with self.assertRaises(ConfigurationError) as raised:
                        load_quality_policy(manifest)
                    self.assertIn("quality policy", str(raised.exception))

    def test_quality_config_schemas_reject_non_integer_versions(self) -> None:
        cases = (
            (
                load_taxonomy,
                "taxonomy-v1.json",
                "tome4-quality-taxonomy-v1",
                "unsupported quality taxonomy schema",
            ),
            (
                load_quality_policy,
                "policy-v1.json",
                "tome4-quality-policy-v1",
                "unsupported quality policy schema",
            ),
        )
        with tempfile.TemporaryDirectory(prefix="tome4-quality-config-") as temporary:
            root = Path(temporary)
            quality_root = root / "i18n" / "quality"
            quality_root.mkdir(parents=True)
            manifest = replace(self.manifest, root=root)
            for loader, filename, contract, message in cases:
                for schema_version in (True, 1.0):
                    with self.subTest(
                        loader=loader.__name__, schema_version=schema_version
                    ):
                        (quality_root / filename).write_text(
                            json.dumps(
                                {
                                    "schema_version": schema_version,
                                    "contract": contract,
                                }
                            ),
                            encoding="utf-8",
                        )
                        with self.assertRaisesRegex(ConfigurationError, message):
                            loader(manifest)


class QualityIdentityTests(unittest.TestCase):
    """Phase-1 doc section 10.1: identity and invalidation semantics."""

    VERSION = "tome-1.7.6"

    def test_unit_id_matches_stable_entry_id(self) -> None:
        unit_id = compute_unit_id("tome", "data/talents/a.lua", "Rune of Reflection", None)
        self.assertEqual(
            unit_id,
            stable_entry_id("tome", "data/talents/a.lua", "Rune of Reflection", None),
        )

    def test_target_change_changes_revision(self) -> None:
        unit_id = compute_unit_id("tome", "s", "source", None)
        first = compute_revision_id(self.VERSION, unit_id, "甲", None, None)
        second = compute_revision_id(self.VERSION, unit_id, "乙", None, None)
        self.assertNotEqual(first, second)

    def test_args_order_special_version_change_revision(self) -> None:
        unit_id = compute_unit_id("tome", "s", "%s has %d", "tformat")
        base = compute_revision_id(self.VERSION, unit_id, "%d 属于 %s", [2, 1], None)
        self.assertNotEqual(
            base, compute_revision_id(self.VERSION, unit_id, "%d 属于 %s", None, None)
        )
        self.assertNotEqual(
            base, compute_revision_id(self.VERSION, unit_id, "%d 属于 %s", [2, 1], {"x": 1})
        )
        self.assertNotEqual(
            base, compute_revision_id("tome-1.8.0", unit_id, "%d 属于 %s", [2, 1], None)
        )

    def test_source_section_tag_change_unit_and_revision(self) -> None:
        first = compute_unit_id("tome", "s", "source", None)
        second = compute_unit_id("tome", "s2", "source", None)
        self.assertNotEqual(first, second)
        revision_first = compute_revision_id(self.VERSION, first, "target", None, None)
        revision_second = compute_revision_id(self.VERSION, second, "target", None, None)
        self.assertNotEqual(revision_first, revision_second)
        tag_unit = compute_unit_id("tome", "s", "source", "say")
        self.assertNotEqual(first, tag_unit)

    def test_revision_identity_ignores_lines_and_ordinals(self) -> None:
        unit_id = compute_unit_id("tome", "s", "source", None)
        revision = compute_revision_id(self.VERSION, unit_id, "target", None, None)
        self.assertEqual(
            revision,
            compute_revision_id(self.VERSION, unit_id, "target", None, None),
        )
        self.assertRegex(revision, r"^[0-9a-f]{64}$")


class QualityStructureTests(unittest.TestCase):
    """Phase-1 doc section 10.2: structure and classification semantics."""

    def test_percent_percent_is_not_a_format_token(self) -> None:
        structure = structure_signature("100%% chance", "100%% 几率", None)
        self.assertEqual(structure["printf"]["source_raw"], [])
        self.assertEqual(structure["printf"]["target_raw"], [])

    def test_args_order_permutation_role_order(self) -> None:
        structure = structure_signature("%s has %d", "%d 属于 %s", [2, 1])
        self.assertEqual(structure["printf"]["source_conversions"], ["s", "d"])
        self.assertEqual(structure["printf"]["role_order"], ["d", "s"])
        self.assertEqual(structure["printf"]["target_conversions"], ["d", "s"])

    def test_markup_and_token_multisets(self) -> None:
        structure = structure_signature(
            "#GREEN#hit #RED#x#LAST#", "#GREEN#命中 #RED#x#LAST#", None
        )
        self.assertEqual(
            structure["markup"]["source"],
            {"#GREEN#": 1, "#RED#": 1, "#LAST#": 1},
        )
        self.assertEqual(structure["markup"]["source"], structure["markup"]["target"])
        self.assertEqual(structure["newlines"], {"source": 0, "target": 0})
        self.assertFalse(structure["multiline"])

    def test_invalid_args_order_yields_no_role_order(self) -> None:
        structure = structure_signature("%s has %d", "%s has %d", [1])
        self.assertIsNone(structure["printf"]["role_order"])

    def test_longer_overlapping_term_is_not_shadowed(self) -> None:
        from i18nlib.quality import _build_term_index, _relevant_terms_for

        rows = [
            {
                "source": "fire",
                "target": "火焰",
                "category": "T.GAME.DAMAGE",
                "domain": "combat",
                "source_tag": "damage type",
                "status": "preferred",
                "scope": "core",
                "notes": "",
            },
            {
                "source": "fire damage",
                "target": "火焰伤害",
                "category": "T.GAME.MISC",
                "domain": "combat",
                "source_tag": "damage type",
                "status": "existing",
                "scope": "core",
                "notes": "",
            },
        ]
        records, matcher, by_plain, nested_terms = _build_term_index(rows)
        terms = _relevant_terms_for(
            "fire damage on hit",
            "damage type",
            "tome",
            records,
            matcher,
            by_plain,
            nested_terms,
        )
        matched = [term["source"] for term in terms]
        self.assertIn("fire", matched)
        self.assertIn("fire damage", matched)
        # boundary must still prevent prefix matches inside words
        self.assertEqual(
            _relevant_terms_for(
                "fireball", "damage type", "tome", records, matcher, by_plain
            ),
            [],
        )

    def test_nested_term_index_matches_workset_at_ascii_boundaries(self) -> None:
        import re

        from i18nlib.quality import _build_term_index, _relevant_terms_for

        def term(
            source: str,
            target: str,
            *,
            source_tag: str = "_t",
            scope: str = "core",
        ) -> dict[str, str]:
            return {
                "source": source,
                "target": target,
                "category": "T.GAME.MISC",
                "domain": "combat",
                "source_tag": source_tag,
                "status": "preferred",
                "scope": scope,
                "notes": "fixture",
            }

        rows = [
            term("fire", "火焰"),
            term("fire damage", "火焰伤害"),
            term("light", "光系"),
            term("light", "光明"),
            term("light", "轻", source_tag="entity subtype"),
            term("light", "邪光", scope="dlc"),
            term("holy light", "圣光"),
            term("read", "读取"),
            term("dread", "惊骇"),
            term("Choker of Dread", "噩灵护符"),
            term("previous level", "前往上一层"),
            term("way to the previous level", "通往上一层的路"),
            term("through shadow", "穿过暗影"),
            term("passage through shadow realm", "暗影界通道"),
            term("delightful aura", "愉悦光环"),
        ]
        records, matcher, by_plain, nested_terms = _build_term_index(rows)
        self.assertIsNotNone(matcher)
        assert matcher is not None

        # Duplicate context rows remain addressable through by_plain, while
        # the expensive matcher and containment scan use each plain once.
        self.assertEqual(len(by_plain["light"]), 4)
        unique_plains = sorted(
            by_plain, key=lambda plain: (-len(plain), plain)
        )
        self.assertEqual(
            matcher.pattern,
            r"(?<![a-z0-9_])("
            + "|".join(re.escape(plain) for plain in unique_plains)
            + r")(?![a-z0-9_])",
        )

        self.assertIn("fire", nested_terms["fire damage"])
        self.assertIn("light", nested_terms["holy light"])
        self.assertIn("dread", nested_terms["choker of dread"])
        self.assertIn(
            "previous level", nested_terms["way to the previous level"]
        )
        self.assertIn(
            "through shadow", nested_terms["passage through shadow realm"]
        )
        self.assertNotIn("light", nested_terms.get("delightful aura", []))
        self.assertNotIn("read", nested_terms.get("choker of dread", []))

        expected_targets = {
            "fire damage": {"火焰", "火焰伤害"},
            "holy light": {"光系", "光明", "圣光"},
            "Choker of Dread": {"惊骇", "噩灵护符"},
            "way to the previous level": {"前往上一层", "通往上一层的路"},
            "passage through shadow realm": {"穿过暗影", "暗影界通道"},
            "delightful aura": {"愉悦光环"},
        }

        def applicable_key(row: dict[str, object]) -> tuple[object, ...]:
            return (
                row["source"],
                row["target"],
                row["category"],
                row["source_tag"],
                row["status"],
                row["scope"],
                row["notes"],
            )

        for entry_id, (source, targets) in enumerate(expected_targets.items()):
            with self.subTest(source=source):
                item = {
                    "entry_id": f"nested-{entry_id}",
                    "source": source,
                    "source_tag": "_t",
                }
                workset_terms = _relevant_terms(rows, [item], "tome")
                quality_terms = _relevant_terms_for(
                    source,
                    "_t",
                    "tome",
                    records,
                    matcher,
                    by_plain,
                    nested_terms,
                )
                self.assertEqual(
                    {term_row["target"] for term_row in quality_terms},
                    targets,
                )
                self.assertEqual(
                    {applicable_key(term_row) for term_row in quality_terms},
                    {applicable_key(term_row) for term_row in workset_terms},
                )

    def test_relevant_terms_carry_domain(self) -> None:
        from i18nlib.quality import _build_term_index, _relevant_terms_for

        rows = [
            {
                "source": "physical",
                "target": "物理",
                "category": "T.GAME.DAMAGE",
                "domain": "combat",
                "source_tag": "damage type",
                "status": "preferred",
                "scope": "core",
                "notes": "",
            }
        ]
        records, matcher, by_plain, _ = _build_term_index(rows)
        terms = _relevant_terms_for(
            "physical damage", "damage type", "tome", records, matcher, by_plain
        )
        self.assertEqual(len(terms), 1)
        self.assertEqual(terms[0]["domain"], "combat")
        self.assertEqual(terms[0]["match"], "partial")

    def test_section_patterns_are_segment_aware(self) -> None:
        from i18nlib.quality import classify_profile

        taxonomy = {
            "source_tag_profiles": {},
            "term_category_profiles": {},
            "section_pattern_profiles": [
                {"pattern": "ui", "profile": "ui", "confidence": "low"},
                {"pattern": "data/talents", "profile": "mechanics", "confidence": "high"},
            ],
        }
        # 'ui' must not match 'guilds' or 'quiz' as a bare substring;
        # punctuation keeps the source out of the structure fallback
        profile, _ = classify_profile(
            "Guild master!", None, "data/guilds/foo.lua", [], taxonomy
        )
        self.assertNotEqual(profile, "ui")
        profile, _ = classify_profile(
            "Quiz time?", None, "data/quiz/foo.lua", [], taxonomy
        )
        self.assertNotEqual(profile, "ui")
        # exact segment 'ui' still matches at any depth
        profile, confidence = classify_profile(
            "Quit", None, "data/dialogs/ui/foo.lua", [], taxonomy
        )
        self.assertEqual((profile, confidence), ("ui", "low"))
        # multi-segment patterns must appear as a contiguous segment sequence
        profile, confidence = classify_profile(
            "Bolt", None, "data/talents/mage/foo.lua", [], taxonomy
        )
        self.assertEqual((profile, confidence), ("mechanics", "high"))
        profile, _ = classify_profile(
            "Bolt", None, "data/talents_mage/foo.lua", [], taxonomy
        )
        self.assertNotEqual(profile, "mechanics")

    def test_profile_confidence_votes_use_semantic_order(self) -> None:
        from i18nlib.quality import classify_profile

        for first, second, expected in (
            ("high", "low", "high"),
            ("high", "medium", "high"),
            ("medium", "low", "medium"),
        ):
            with self.subTest(confidences=(first, second)):
                taxonomy = {
                    "source_tag_profiles": {},
                    "term_category_profiles": {},
                    "section_pattern_profiles": [
                        {
                            "pattern": "data",
                            "profile": "ui",
                            "confidence": first,
                        },
                        {
                            "pattern": "ui",
                            "profile": "ui",
                            "confidence": second,
                        },
                    ],
                }
                self.assertEqual(
                    classify_profile(
                        "Quit", None, "data/ui/foo.lua", [], taxonomy
                    ),
                    ("ui", expected),
                )

        conflicting_taxonomy = {
            "source_tag_profiles": {"talent": "mechanics"},
            "term_category_profiles": {},
            "section_pattern_profiles": [
                {"pattern": "ui", "profile": "ui", "confidence": "high"}
            ],
        }
        self.assertEqual(
            classify_profile(
                "Bolt",
                "talent",
                "data/ui/foo.lua",
                [],
                conflicting_taxonomy,
            ),
            ("mechanics", "low"),
        )

        single_vote_taxonomy = {
            "source_tag_profiles": {},
            "term_category_profiles": {},
            "section_pattern_profiles": [
                {"pattern": "ui", "profile": "ui", "confidence": "medium"}
            ],
        }
        self.assertEqual(
            classify_profile(
                "Quit", None, "data/ui/foo.lua", [], single_vote_taxonomy
            ),
            ("ui", "medium"),
        )
        self.assertEqual(
            classify_profile(
                "Quit",
                None,
                "data/dialogs/foo.lua",
                [],
                {
                    "source_tag_profiles": {},
                    "term_category_profiles": {},
                    "section_pattern_profiles": [],
                },
            ),
            ("ui", "low"),
        )


class QualitySampleOptionPreflightTests(unittest.TestCase):
    """Official sample options fail before rules, inventory, or artifacts."""

    manifest = SimpleNamespace(root=Path("/fixture-root"), raw_bytes=b"fixture")
    inventory_path = Path("unused-inventory.jsonl")

    @staticmethod
    def _policy() -> dict[str, object]:
        return {
            "pilot": {
                "buckets": {
                    "representative": 2,
                    "risk-enriched": 1,
                    "contrast": 1,
                },
                "seed": "policy-default-seed",
                "evaluator_ids": ["reviewer-a", "reviewer-b"],
                "method_version": "fixture-method-v1",
            }
        }

    @staticmethod
    def _sample(seed: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "quality_contract": SAMPLE_CONTRACT,
            "sample_id": "a" * 64,
            "items_sha256": "c" * 64,
            "seed": seed,
            "size": 4,
            "bucket_counts": {},
            "unmet_constraints": [],
            "coverage": {},
            "items": [{"revision_id": "b" * 64}],
        }

    def _assert_rejected_without_io(
        self,
        function: object,
        *,
        expected_message: str,
        **options: object,
    ) -> None:
        with (
            patch.object(quality_module, "load_quality_policy") as load_policy,
            patch.object(quality_module, "load_taxonomy") as load_taxonomy_mock,
            patch.object(quality_module, "read_inventory_file") as read_inventory,
            patch.object(
                quality_module, "_generate_sample_from_inventory"
            ) as generate_from_inventory,
            patch.object(
                quality_module, "create_quality_run_directory"
            ) as create_run_directory,
            patch.object(quality_module, "write_json") as write_json_mock,
        ):
            with self.assertRaisesRegex(ValidationError, expected_message):
                function(self.manifest, self.inventory_path, **options)

        for mocked in (
            load_policy,
            load_taxonomy_mock,
            read_inventory,
            generate_from_inventory,
            create_run_directory,
            write_json_mock,
        ):
            mocked.assert_not_called()

    def test_invalid_size_shapes_fail_without_io_for_public_paths(self) -> None:
        for function in (quality_module.generate_sample, quality_module.run_sample):
            for invalid_size in (True, 120.0, "120", 0, -1):
                with self.subTest(
                    function=function.__name__, size=invalid_size
                ):
                    self._assert_rejected_without_io(
                        function,
                        expected_message="pilot sample size must be an integer >= 1",
                        size=invalid_size,
                    )

    def test_invalid_seed_shapes_fail_without_io_for_public_paths(self) -> None:
        for function in (quality_module.generate_sample, quality_module.run_sample):
            for invalid_seed in (True, 1, 1.5, b"seed", ""):
                with self.subTest(
                    function=function.__name__, seed=invalid_seed
                ):
                    self._assert_rejected_without_io(
                        function,
                        expected_message="pilot sample seed must be a non-empty string",
                        seed=invalid_seed,
                    )

    def test_policy_size_mismatch_fails_before_later_io(self) -> None:
        for function in (quality_module.generate_sample, quality_module.run_sample):
            with self.subTest(function=function.__name__):
                policy = self._policy()
                with (
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=policy,
                    ) as load_policy,
                    patch.object(
                        quality_module, "load_taxonomy"
                    ) as load_taxonomy_mock,
                    patch.object(
                        quality_module, "read_inventory_file"
                    ) as read_inventory,
                    patch.object(
                        quality_module, "_generate_sample_from_inventory"
                    ) as generate_from_inventory,
                    patch.object(
                        quality_module, "create_quality_run_directory"
                    ) as create_run_directory,
                    patch.object(quality_module, "write_json") as write_json_mock,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"pilot sample size must be 4 for policy-v1 \(got 3\)",
                    ):
                        function(
                            self.manifest,
                            self.inventory_path,
                            size=3,
                            seed="fixture-seed",
                        )

                load_policy.assert_called_once_with(self.manifest)
                for mocked in (
                    load_taxonomy_mock,
                    read_inventory,
                    generate_from_inventory,
                    create_run_directory,
                    write_json_mock,
                ):
                    mocked.assert_not_called()

    def test_generate_sample_preserves_valid_default_and_exact_options(self) -> None:
        cases = (
            ({}, None, None, "policy-default-seed"),
            (
                {"size": 4, "seed": "explicit-seed"},
                4,
                "explicit-seed",
                "explicit-seed",
            ),
        )
        for options, expected_size, expected_seed, sample_seed in cases:
            with self.subTest(options=options):
                policy = self._policy()
                taxonomy = {"contract": "fixture-taxonomy"}
                entries: list[dict[str, object]] = []
                inventory_info = {"inventory_sha256": "c" * 64}
                sample = self._sample(sample_seed)
                with (
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=policy,
                    ) as load_policy,
                    patch.object(
                        quality_module,
                        "load_taxonomy",
                        return_value=taxonomy,
                    ) as load_taxonomy_mock,
                    patch.object(
                        quality_module,
                        "_load_inventory_bundle",
                        return_value=(entries, inventory_info),
                    ) as load_inventory_bundle,
                    patch.object(
                        quality_module,
                        "_generate_sample_from_inventory",
                        return_value=sample,
                    ) as generate_from_inventory,
                ):
                    result = quality_module.generate_sample(
                        self.manifest, self.inventory_path, **options
                    )

                self.assertIs(result, sample)
                load_policy.assert_called_once_with(self.manifest)
                load_taxonomy_mock.assert_called_once_with(self.manifest)
                load_inventory_bundle.assert_called_once_with(
                    self.manifest,
                    self.inventory_path,
                    taxonomy,
                    policy,
                )
                generate_from_inventory.assert_called_once_with(
                    self.manifest,
                    entries=entries,
                    inventory_info=inventory_info,
                    taxonomy=taxonomy,
                    qpolicy=policy,
                    size=expected_size,
                    seed=expected_seed,
                )

    def test_run_sample_loads_valid_inputs_once(self) -> None:
        cases = (
            ({}, None, None, "policy-default-seed"),
            (
                {"size": 4, "seed": "explicit-seed"},
                4,
                "explicit-seed",
                "explicit-seed",
            ),
        )
        run_directory = (
            self.manifest.root
            / ".artifacts"
            / "i18n"
            / "quality"
            / "runs"
            / "fixture-sample"
        )
        for options, expected_size, expected_seed, sample_seed in cases:
            with self.subTest(options=options):
                policy = self._policy()
                taxonomy = {"contract": "fixture-taxonomy"}
                entries: list[dict[str, object]] = []
                inventory_info = {"inventory_sha256": "c" * 64}
                sample = self._sample(sample_seed)
                with (
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=policy,
                    ) as load_policy,
                    patch.object(
                        quality_module,
                        "load_taxonomy",
                        return_value=taxonomy,
                    ) as load_taxonomy_mock,
                    patch.object(
                        quality_module,
                        "_load_inventory_bundle",
                        return_value=(entries, inventory_info),
                    ) as load_inventory_bundle,
                    patch.object(
                        quality_module,
                        "_generate_sample_from_inventory",
                        return_value=sample,
                    ) as generate_from_inventory,
                    patch.object(
                        quality_module,
                        "create_quality_run_directory",
                        return_value=run_directory,
                    ) as create_run_directory,
                    patch.object(quality_module, "write_json") as write_json_mock,
                ):
                    result = quality_module.run_sample(
                        self.manifest, self.inventory_path, **options
                    )

                self.assertEqual(result["seed"], sample_seed)
                self.assertEqual(result["items"], [{"revision_id": "b" * 64}])
                load_policy.assert_called_once_with(self.manifest)
                load_taxonomy_mock.assert_called_once_with(self.manifest)
                load_inventory_bundle.assert_called_once_with(
                    self.manifest,
                    self.inventory_path,
                    taxonomy,
                    policy,
                )
                generate_from_inventory.assert_called_once_with(
                    self.manifest,
                    entries=entries,
                    inventory_info=inventory_info,
                    taxonomy=taxonomy,
                    qpolicy=policy,
                    size=expected_size,
                    seed=expected_seed,
                )
                create_run_directory.assert_called_once_with(
                    self.manifest.root, "sample"
                )
                self.assertEqual(write_json_mock.call_count, 4)


class QualitySamplingTests(unittest.TestCase):
    """Phase-1 doc section 10.3: deterministic stratified sampling."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.qpolicy = load_quality_policy(cls.manifest)
        cls.taxonomy = load_taxonomy(cls.manifest)
        cls.inventory = cls._make_fixture_inventory()

    @classmethod
    def _entry(
        cls,
        index: int,
        *,
        component: str,
        section: str,
        source: str,
        target: str,
        source_tag: str | None = None,
        profile: str,
        length_bin: str,
        enriched: bool = False,
        term_evidence: bool = False,
        line: int = 1,
    ) -> dict[str, object]:
        unit_id = compute_unit_id(component, section, source, source_tag)
        revision_id = compute_revision_id(
            cls.manifest.version, unit_id, target, None, None
        )
        structure = structure_signature(source, target, None)
        risk_flags = ["has-printf"] if enriched else []
        terms = (
            [
                {
                    "source": "fixture",
                    "target": "固定",
                    "category": "T.GAME.TALENT",
                    "source_tag": "",
                    "status": "preferred",
                    "scope": "core",
                    "notes": "fixture term",
                    "match": "partial",
                }
            ]
            if term_evidence
            else []
        )
        return {
            "unit_id": unit_id,
            "revision_id": revision_id,
            "version": cls.manifest.version,
            "component": component,
            "section": section,
            "source": source,
            "target": target,
            "source_tag": source_tag,
            "args_order": None,
            "special": None,
            "occurrences": [
                {
                    "logical_path": f"{component}.lua",
                    "section": section,
                    "line": line,
                    "ordinal": index,
                }
            ],
            "profile": profile,
            "profile_confidence": "high",
            "domain_hints": [],
            "relevant_terms": terms,
            "structure": structure,
            "gate_signals": {
                "lua_load_valid": True,
                "empty_target": False,
                "format_signature_match": None,
                "markup_multiset_match": True,
                "at_token_multiset_match": True,
                "runtime_collision": False,
                "needs_review": [],
            },
            "risk_flags": risk_flags,
            "source_length_bin": length_bin,
        }

    @classmethod
    def _make_fixture_inventory(cls) -> list[dict[str, object]]:
        profiles = [
            "mechanics", "term-name", "ui", "runtime-log",
            "dialogue", "narrative", "unknown",
        ]
        bins = ["short", "medium", "long", "very-long"]
        components = ["tome", "engine", "boot", "cults", "orcs", "example", "addon-dev"]
        entries: list[dict[str, object]] = []
        for index in range(320):
            entries.append(
                cls._entry(
                    index,
                    component=components[index % 7],
                    section=f"data/zone-{index % 3}/file-{index % 11}.lua",
                    source=f"fixture source {index}",
                    target=f"固定译文 {index}",
                    profile=profiles[index % 7],
                    length_bin=bins[index % 4],
                    enriched=index % 3 == 0,
                    term_evidence=index % 4 == 0,
                )
            )
        # contrast groups: one multi-target triplet and two pairs
        contrast_sources = [
            ("tome", "data/contrast/a.lua", "shared runtime key", "译法甲"),
            ("tome", "data/contrast/a.lua", "shared runtime key", "译法乙"),
            ("tome", "data/contrast/a.lua", "shared runtime key", "译法丙"),
            ("cults", "data/contrast/b.lua", "near #GREEN#dup#LAST# key", "近重复一"),
            ("cults", "data/contrast/b.lua", "near dup key", "近重复二"),
            ("boot", "data/contrast/c.lua", "repeat key", "重复一"),
            ("boot", "data/contrast/d.lua", "repeat key", "重复二"),
        ]
        for index, (component, section, source, target) in enumerate(
            contrast_sources, start=1000
        ):
            entries.append(
                cls._entry(
                    index,
                    component=component,
                    section=section,
                    source=source,
                    target=target,
                    profile="dialogue",
                    length_bin="short",
                )
            )
        return entries

    def _write_inventory(self, entries: list[dict[str, object]]) -> Path:
        directory = TEST_FIXTURE_ROOT / "quality-sampling"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "inventory.jsonl"
        path.write_text(
            "\n".join(
                json.dumps(entry, ensure_ascii=False, sort_keys=True) for entry in entries
            )
            + "\n",
            encoding="utf-8",
        )
        (directory / "inventory-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "quality_contract": quality_module.INVENTORY_CONTRACT,
                    "tool_version": TOOL_VERSION,
                    "version": self.manifest.version,
                    "manifest_sha256": hashlib.sha256(
                        self.manifest.raw_bytes
                    ).hexdigest(),
                    "translation_inputs_sha256": (
                        quality_module._current_translation_inputs_sha256(
                            self.manifest
                        )
                    ),
                    "terminology_sha256": hashlib.sha256(
                        (
                            self.manifest.root / self.manifest.terminology
                        ).read_bytes()
                    ).hexdigest(),
                    "taxonomy_sha256": quality_module._canonical_sha256(
                        self.taxonomy
                    ),
                    "policy_sha256": quality_module._canonical_sha256(
                        self.qpolicy
                    ),
                    "inventory_sha256": quality_module._canonical_sha256(
                        entries
                    ),
                    "entries": len(entries),
                    "profile_classifier_version": self.taxonomy[
                        "profile_classifier_version"
                    ],
                    "risk_rule_version": self.taxonomy["risk_rule_version"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return path

    def test_inventory_manifest_preflight_and_jsonl_binding(self) -> None:
        cases = (
            ("missing", "missing", None, None, "root", False),
            ("invalid encoding", "raw", None, b"\xff", "root", False),
            ("invalid JSON", "raw", None, b"{", "root", False),
            ("non-object root", "raw", None, b"[]", "root", False),
            (
                "wrong contract",
                "set",
                "quality_contract",
                "old-contract",
                "quality_contract",
                False,
            ),
            (
                "bool schema",
                "set",
                "schema_version",
                True,
                "schema_version",
                False,
            ),
            (
                "missing tool version",
                "delete",
                "tool_version",
                None,
                "tool_version",
                False,
            ),
            (
                "old tool version",
                "set",
                "tool_version",
                "0.0.0",
                "tool_version",
                False,
            ),
            (
                "wrong version",
                "set",
                "version",
                "old-version",
                "version",
                False,
            ),
            (
                "stale manifest",
                "set",
                "manifest_sha256",
                "0" * 64,
                "manifest_sha256",
                False,
            ),
            (
                "missing translation inputs digest",
                "delete",
                "translation_inputs_sha256",
                None,
                "translation_inputs_sha256",
                False,
            ),
            (
                "stale translation inputs",
                "set",
                "translation_inputs_sha256",
                "0" * 64,
                "translation_inputs_sha256",
                False,
            ),
            (
                "stale terminology",
                "set",
                "terminology_sha256",
                "0" * 64,
                "terminology_sha256",
                False,
            ),
            (
                "stale taxonomy",
                "set",
                "taxonomy_sha256",
                "0" * 64,
                "taxonomy_sha256",
                False,
            ),
            (
                "stale policy",
                "set",
                "policy_sha256",
                "0" * 64,
                "policy_sha256",
                False,
            ),
            (
                "missing policy digest",
                "delete",
                "policy_sha256",
                None,
                "policy_sha256",
                False,
            ),
            (
                "wrong profile classifier",
                "set",
                "profile_classifier_version",
                "old-profile-classifier",
                "profile_classifier_version",
                False,
            ),
            (
                "wrong risk rules",
                "set",
                "risk_rule_version",
                "old-risk-rules",
                "risk_rule_version",
                False,
            ),
            ("bool count", "set", "entries", True, "entries", False),
            (
                "noncanonical digest",
                "set",
                "inventory_sha256",
                "A" * 64,
                "inventory_sha256",
                False,
            ),
            (
                "count mismatch",
                "set",
                "entries",
                len(self.inventory) + 1,
                "entries",
                True,
            ),
            (
                "digest mismatch",
                "set",
                "inventory_sha256",
                "0" * 64,
                "inventory_sha256",
                True,
            ),
        )
        functions = (
            generate_sample,
            generate_dry_run,
            quality_module.run_sample,
            quality_module.run_dry_run,
        )
        original_preflight = quality_module._read_inventory_manifest_preflight
        original_read_inventory = quality_module.read_inventory_file

        for name, operation, field, value, error_field, reads_jsonl in cases:
            with self.subTest(case=name):
                path = self._write_inventory(self.inventory)
                manifest_path = path.with_name("inventory-manifest.json")
                if operation == "missing":
                    manifest_path.unlink()
                elif operation == "raw":
                    manifest_path.write_bytes(value)
                else:
                    inventory_manifest = json.loads(
                        manifest_path.read_text(encoding="utf-8")
                    )
                    if operation == "delete":
                        del inventory_manifest[field]
                    else:
                        inventory_manifest[field] = value
                    manifest_path.write_text(
                        json.dumps(
                            inventory_manifest,
                            ensure_ascii=False,
                            sort_keys=True,
                        ),
                        encoding="utf-8",
                    )

                events: list[str] = []

                def tracked_preflight(*args: object) -> dict[str, object]:
                    events.append("manifest")
                    return original_preflight(*args)

                def tracked_inventory(
                    inventory_path: Path,
                ) -> tuple[list[dict[str, object]], dict[str, object]]:
                    events.append("inventory")
                    return original_read_inventory(inventory_path)

                with (
                    patch.object(
                        quality_module,
                        "_read_inventory_manifest_preflight",
                        side_effect=tracked_preflight,
                    ),
                    patch.object(
                        quality_module,
                        "read_inventory_file",
                        side_effect=tracked_inventory,
                    ) as read_inventory,
                    patch.object(
                        quality_module, "_validate_inventory_semantics"
                    ) as validate_semantics,
                    patch.object(
                        quality_module, "_generate_sample_from_inventory"
                    ) as generate_from_inventory,
                    patch.object(
                        quality_module, "_sampling_features"
                    ) as sampling_features,
                    patch.object(
                        quality_module, "create_quality_run_directory"
                    ) as create_run_directory,
                    patch.object(quality_module, "write_json") as write_json_mock,
                ):
                    for function in functions:
                        with self.subTest(case=name, function=function.__name__):
                            with self.assertRaisesRegex(
                                ValidationError,
                                rf"quality inventory manifest\.{error_field}",
                            ):
                                function(self.manifest, path)

                expected_events = (
                    ["manifest", "inventory"] * len(functions)
                    if reads_jsonl
                    else ["manifest"] * len(functions)
                )
                self.assertEqual(events, expected_events)
                self.assertEqual(
                    read_inventory.call_count,
                    len(functions) if reads_jsonl else 0,
                )
                for mocked in (
                    validate_semantics,
                    generate_from_inventory,
                    sampling_features,
                    create_run_directory,
                    write_json_mock,
                ):
                    mocked.assert_not_called()

    def test_inventory_record_contract_fails_before_sampling_helpers(self) -> None:
        cases = (
            (
                "missing source tag",
                lambda entry: entry.pop("source_tag"),
                "quality inventory record 1.source_tag",
            ),
            (
                "missing occurrence path",
                lambda entry: entry["occurrences"][0].pop("logical_path"),
                "quality inventory record 1.occurrences[0].logical_path",
            ),
            (
                "wrong occurrence line type",
                lambda entry: entry["occurrences"][0].__setitem__("line", "1"),
                "quality inventory record 1.occurrences[0].line",
            ),
            (
                "bool args order",
                lambda entry: entry.__setitem__("args_order", [True]),
                "quality inventory record 1.args_order[0]",
            ),
            (
                "bool occurrence ordinal",
                lambda entry: entry["occurrences"][0].__setitem__(
                    "ordinal", False
                ),
                "quality inventory record 1.occurrences[0].ordinal",
            ),
            (
                "empty occurrences",
                lambda entry: entry.__setitem__("occurrences", []),
                "quality inventory record 1.occurrences",
            ),
            (
                "noncanonical special",
                lambda entry: entry.__setitem__(
                    "special", {"value": float("nan")}
                ),
                "quality inventory record 1.special",
            ),
            (
                "wrong domain hint item type",
                lambda entry: entry.__setitem__("domain_hints", [1]),
                "quality inventory record 1.domain_hints[0]",
            ),
            (
                "wrong relevant term item type",
                lambda entry: entry.__setitem__("relevant_terms", ["term"]),
                "quality inventory record 1.relevant_terms[0]",
            ),
            (
                "wrong structure type",
                lambda entry: entry.__setitem__("structure", []),
                "quality inventory record 1.structure",
            ),
        )
        for function in (generate_sample, generate_dry_run):
            for name, mutate, expected_path in cases:
                with self.subTest(function=function.__name__, case=name):
                    valid = copy.deepcopy(self.inventory[0])
                    invalid = copy.deepcopy(self.inventory[1])
                    mutate(invalid)
                    path = self._write_inventory([valid, invalid])
                    with (
                        patch.object(
                            quality_module, "_generate_sample_from_inventory"
                        ) as generate_from_inventory,
                        patch.object(
                            quality_module, "_contrast_groups"
                        ) as contrast_groups,
                        patch.object(
                            quality_module, "_entry_features"
                        ) as entry_features,
                        patch.object(
                            quality_module, "_build_sample_items"
                        ) as build_sample_items,
                    ):
                        with self.assertRaises(ValidationError) as raised:
                            function(self.manifest, path)

                    self.assertIn(expected_path, str(raised.exception))
                    for mocked in (
                        generate_from_inventory,
                        contrast_groups,
                        entry_features,
                        build_sample_items,
                    ):
                        mocked.assert_not_called()

    def test_inventory_semantics_fail_before_sampling_or_output(self) -> None:
        cases = (
            (
                "wrong version",
                lambda entry: entry.__setitem__("version", "tome-old"),
                "version",
            ),
            (
                "undeclared component",
                lambda entry: entry.__setitem__("component", "undeclared"),
                "component",
            ),
            (
                "wrong unit id",
                lambda entry: entry.__setitem__("unit_id", "0" * 64),
                "unit_id",
            ),
            (
                "wrong revision id",
                lambda entry: entry.__setitem__("revision_id", "0" * 64),
                "revision_id",
            ),
            (
                "unknown profile",
                lambda entry: entry.__setitem__("profile", "undeclared"),
                "profile",
            ),
            (
                "unknown risk flag",
                lambda entry: entry.__setitem__(
                    "risk_flags", ["undeclared-risk"]
                ),
                "risk_flags",
            ),
            (
                "unknown length bin",
                lambda entry: entry.__setitem__(
                    "source_length_bin", "undeclared"
                ),
                "source_length_bin",
            ),
        )
        for function in (generate_sample, generate_dry_run):
            for name, mutate, field in cases:
                with self.subTest(function=function.__name__, case=name):
                    valid = copy.deepcopy(self.inventory[0])
                    invalid = copy.deepcopy(self.inventory[1])
                    mutate(invalid)
                    path = self._write_inventory([valid, invalid])
                    with (
                        patch.object(
                            quality_module, "_sampling_features"
                        ) as sampling_features,
                        patch.object(
                            quality_module, "_contrast_groups"
                        ) as contrast_groups,
                        patch.object(
                            quality_module, "_select_bucket"
                        ) as select_bucket,
                        patch.object(
                            quality_module, "_generate_sample_from_inventory"
                        ) as generate_from_inventory,
                        patch.object(
                            quality_module, "create_quality_run_directory"
                        ) as create_run_directory,
                        patch.object(quality_module, "write_json") as write_json_mock,
                    ):
                        with self.assertRaises(ValidationError) as raised:
                            function(self.manifest, path)

                    self.assertIn(
                        f"quality inventory record 1.{field}",
                        str(raised.exception),
                    )
                    for mocked in (
                        sampling_features,
                        contrast_groups,
                        select_bucket,
                        generate_from_inventory,
                        create_run_directory,
                        write_json_mock,
                    ):
                        mocked.assert_not_called()

    def test_inventory_semantics_accept_valid_fixture_without_mutation(self) -> None:
        entries = copy.deepcopy(self.inventory)
        expected = copy.deepcopy(entries)

        quality_module._validate_inventory_semantics(
            entries, self.manifest, self.taxonomy
        )

        self.assertEqual(entries, expected)

    def test_valid_inventory_record_contract_preserves_order_and_digest(self) -> None:
        expected = copy.deepcopy(self.inventory[:3])
        path = self._write_inventory(expected)
        loaded, info = quality_module.read_inventory_file(path)

        self.assertEqual(loaded, expected)
        self.assertEqual(
            [entry["revision_id"] for entry in loaded],
            [entry["revision_id"] for entry in expected],
        )
        self.assertEqual(
            info["inventory_sha256"], quality_module._canonical_sha256(expected)
        )

    def test_sample_is_deterministic_and_satisfies_constraints(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_sample(self.manifest, path)
        second = generate_sample(self.manifest, path)
        serialized = (
            json.dumps(first, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(serialized).hexdigest(),
            "e59acd02b8839df1de3a22334554c8e999ddd0450717b956f34e6b4d25754c3e",
        )
        self.assertEqual(
            first["sample_id"],
            "e8a266f70202a388b0c7c01686044bcc51e1f7908c05ce21d95e227c5a3259a6",
        )
        self.assertEqual(
            first["items_sha256"],
            quality_module._canonical_sha256(first["items"]),
        )
        self.assertEqual(first["sample_id"], second["sample_id"])
        self.assertEqual(first["items"], second["items"])
        self.assertEqual(first["size"], 120)
        self.assertEqual(first["unmet_constraints"], [])
        revisions = [item["revision_id"] for item in first["items"]]
        self.assertEqual(len(revisions), len(set(revisions)))
        buckets = [item["bucket"] for item in first["items"]]
        self.assertEqual(
            sum(buckets.count(bucket) for bucket in ("representative", "risk-enriched", "contrast")),
            120,
        )
        self.assertEqual(
            len({(r, b) for r, b in zip(revisions, buckets)}), 120,
        )

    def test_context_neighbors_use_identity_index_without_equality_scans(self) -> None:
        class EqualityCountingDict(dict[str, object]):
            comparisons = 0

            def __eq__(self, other: object) -> bool:
                type(self).comparisons += 1
                return super().__eq__(other)

        def entry(
            index: int, component: str, source: str, line: int
        ) -> EqualityCountingDict:
            item = EqualityCountingDict(
                self._entry(
                    index,
                    component=component,
                    section=f"data/{source}.lua",
                    source=source,
                    target=f"target {source}",
                    profile="ui",
                    length_bin="short",
                    line=line,
                )
            )
            item["profile_confidence"] = "medium"
            return item

        a_first = entry(1, "tome", "a-first", 10)
        a_before = entry(2, "tome", "a-before", 20)
        a_middle = entry(3, "tome", "a-middle", 30)
        a_after = entry(4, "tome", "a-after", 40)
        a_last = entry(5, "tome", "a-last", 50)
        b_first = entry(6, "engine", "b-first", 10)
        b_middle = entry(7, "engine", "b-middle", 20)
        b_last = entry(8, "engine", "b-last", 30)
        entries = [
            a_middle,
            b_last,
            a_first,
            b_first,
            a_last,
            a_before,
            b_middle,
            a_after,
        ]
        foreign = self._entry(
            9,
            component="tome",
            section="data/foreign.lua",
            source="foreign",
            target="foreign target",
            profile="ui",
            length_bin="short",
            line=35,
        )
        foreign["profile_confidence"] = "medium"

        items = quality_module._build_sample_items(
            entries=entries,
            ordered=[a_first, a_middle, a_last, b_middle, foreign],
            contrast_ids=set(),
            risk_selected_ids=set(),
            contrast_group_of={},
            contrast=[],
            qpolicy={"context_neighbor_limit": 2},
        )

        self.assertEqual(EqualityCountingDict.comparisons, 0)
        self.assertEqual(
            [
                [neighbor["source"] for neighbor in item["context_neighbors"]]
                for item in items
            ],
            [
                ["a-before", "a-middle"],
                ["a-first", "a-before", "a-after", "a-last"],
                ["a-middle", "a-after"],
                ["b-first", "b-last"],
                [],
            ],
        )
        self.assertEqual(
            items[1]["context_neighbors"][0],
            {
                "component": "tome",
                "section": "data/a-first.lua",
                "source": "a-first",
                "target": "target a-first",
                "source_tag": None,
            },
        )

    def test_contrast_pairs_are_never_split(self) -> None:
        path = self._write_inventory(self.inventory)
        sample = generate_sample(self.manifest, path)
        groups: dict[str, list[str]] = {}
        for item in sample["items"]:
            if item["contrast_group"]:
                groups.setdefault(item["contrast_group"], []).append(item["revision_id"])
        self.assertGreaterEqual(len(groups), 2)
        by_source: dict[str, list[str]] = {}
        for item in self.inventory:
            if item["section"].startswith("data/contrast"):
                by_source.setdefault(item["source"], []).append(item["revision_id"])
        sample_revisions = {item["revision_id"] for item in sample["items"]}
        for members in by_source.values():
            if members:
                self.assertTrue(
                    all(member in sample_revisions for member in members)
                    or all(member not in sample_revisions for member in members),
                    "contrast pair must be sampled as a whole",
                )

    def test_different_seed_changes_selection_but_keeps_constraints(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_sample(self.manifest, path, seed="seed-a")
        second = generate_sample(self.manifest, path, seed="seed-b")
        self.assertNotEqual(first["sample_id"], second["sample_id"])
        self.assertNotEqual(
            [item["revision_id"] for item in first["items"]],
            [item["revision_id"] for item in second["items"]],
        )
        self.assertEqual(second["unmet_constraints"], [])

    def test_overlapping_contrast_groups_are_never_split(self) -> None:
        # Group 1 (multi-target): A1/A2 share runtime key 'overlap key' with
        # different targets. Group 2 (near-duplicate): A1 and B1 share the
        # normalized source ('overlap key' vs 'overlap key.'). A1 is claimed by
        # whichever group is selected first; the other group must be skipped
        # whole instead of sampling its remaining member alone.
        def entry(
            index: int, source: str, target: str, section: str
        ) -> dict[str, object]:
            unit_id = compute_unit_id("tome", section, source, None)
            revision_id = compute_revision_id(
                self.manifest.version, unit_id, target, None, None
            )
            structure = structure_signature(source, target, None)
            return {
                "unit_id": unit_id,
                "revision_id": revision_id,
                "version": self.manifest.version,
                "component": "tome",
                "section": section,
                "source": source,
                "target": target,
                "source_tag": None,
                "args_order": None,
                "special": None,
                "occurrences": [
                    {
                        "logical_path": "tome.lua",
                        "section": section,
                        "line": index + 1,
                        "ordinal": index,
                    }
                ],
                "profile": "ui",
                "profile_confidence": "high",
                "domain_hints": [],
                "relevant_terms": [],
                "structure": structure,
                "gate_signals": {
                    "lua_load_valid": True,
                    "empty_target": False,
                    "format_signature_match": None,
                    "markup_multiset_match": True,
                    "at_token_multiset_match": True,
                    "runtime_collision": False,
                    "needs_review": [],
                },
                "risk_flags": [],
                "source_length_bin": "short",
            }

        entries: list[dict[str, object]] = []
        for index in range(130):
            entries.append(
                entry(index + 10, f"filler {index}", f"填充 {index}", "data/x.lua")
            )
        entries.append(entry(0, "overlap key", "译法甲", "data/contrast/a.lua"))
        entries.append(entry(1, "overlap key", "译法乙", "data/contrast/a.lua"))
        entries.append(entry(2, "overlap key ", "译法甲", "data/contrast/b.lua"))
        path = self._write_inventory(entries)
        sample = generate_sample(self.manifest, path, seed="overlap-fixture")
        sampled = {item["revision_id"] for item in sample["items"]}
        from i18nlib.quality import _contrast_groups

        loaded_entries = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        original_groups = _contrast_groups(loaded_entries, self.qpolicy)
        for _, members in original_groups:
            member_ids = {member["revision_id"] for member in members}
            if any(member in sampled for member in member_ids):
                self.assertTrue(
                    all(member in sampled for member in member_ids),
                    "a contrast group must never be split",
                )
        a1_rev = next(
            e["revision_id"]
            for e in entries
            if e["source"] == "overlap key" and e["target"] == "译法甲"
        )
        # A1 belongs to both groups, so it is always sampled with one of them
        self.assertIn(a1_rev, sampled)
        self.assertEqual(sample["size"], 120)

    def test_unmet_constraints_are_reported_not_silent(self) -> None:
        entries = [
            self._entry(
                index,
                component="tome",
                section="data/x.lua",
                source=f"only ui {index}",
                target=f"只有界面 {index}",
                profile="ui",
                length_bin="short",
            )
            for index in range(140)
        ]
        path = self._write_inventory(entries)
        sample = generate_sample(self.manifest, path)
        self.assertEqual(sample["size"], 120)
        self.assertGreaterEqual(len(sample["unmet_constraints"]), 4)
        unmet_ids = {unmet["id"] for unmet in sample["unmet_constraints"]}
        self.assertIn("profile-min", unmet_ids)
        self.assertIn("length-bin-min", unmet_ids)

    def test_wrong_sample_size_is_rejected(self) -> None:
        path = self._write_inventory(self.inventory)
        with self.assertRaises(ValidationError):
            generate_sample(self.manifest, path, size=99)

    def test_dry_run_is_deterministic_and_disjoint_from_official(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_dry_run(self.manifest, path)
        second = generate_dry_run(self.manifest, path)
        self.assertIs(type(first), dict)
        serialized = (
            json.dumps(first, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(serialized).hexdigest(),
            "8b14cc8bf55dd774dc5e20d4efdefd9973c2e38b2e77829bad0370fc5ac8c39a",
        )
        self.assertEqual(
            first["sample_id"],
            "04ee1c061b8bbd81ed85bcd90a3317a5339af82d6faeaa40cb4a69c456e57313",
        )
        self.assertEqual(
            first["items_sha256"],
            quality_module._canonical_sha256(first["items"]),
        )
        self.assertEqual(first["sample_id"], second["sample_id"])
        self.assertEqual(first["items"], second["items"])
        self.assertEqual(first["size"], 12)
        self.assertEqual(first["unmet_constraints"], [])
        official = generate_sample(self.manifest, path)
        dry_ids = {item["revision_id"] for item in first["items"]}
        official_ids = {item["revision_id"] for item in official["items"]}
        self.assertTrue(dry_ids.isdisjoint(official_ids))
        self.assertEqual(first["official_sample_id"], official["sample_id"])
        revisions = [item["revision_id"] for item in first["items"]]
        self.assertEqual(len(revisions), len(set(revisions)))

    def test_run_dry_run_reuses_loaded_policy_for_templates(self) -> None:
        path = self._write_inventory(self.inventory)
        first_policy = copy.deepcopy(self.qpolicy)
        first_policy["pilot"]["evaluator_ids"] = [
            "first-reviewer-a",
            "first-reviewer-b",
        ]
        first_policy["pilot"]["method_version"] = "first-method"
        inventory_manifest_path = path.with_name("inventory-manifest.json")
        inventory_manifest = json.loads(
            inventory_manifest_path.read_text(encoding="utf-8")
        )
        inventory_manifest["policy_sha256"] = quality_module._canonical_sha256(
            first_policy
        )
        inventory_manifest_path.write_text(
            json.dumps(inventory_manifest, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        second_policy = copy.deepcopy(self.qpolicy)
        second_policy["pilot"]["evaluator_ids"] = [
            "second-reviewer-a",
            "second-reviewer-b",
        ]
        second_policy["pilot"]["method_version"] = "second-method"
        run_directory = (
            TEST_FIXTURE_ROOT / "quality-sampling" / "dry-run-policy-reuse"
        )
        policies = iter((first_policy, second_policy))
        events: list[str] = []

        def tracked_policy(manifest: Manifest) -> dict[str, object]:
            events.append("policy")
            return next(policies)

        def tracked_taxonomy(manifest: Manifest) -> dict[str, object]:
            events.append("taxonomy")
            return load_taxonomy(manifest)

        original_read_inventory = quality_module.read_inventory_file

        def tracked_inventory(
            inventory_path: Path,
        ) -> tuple[list[dict[str, object]], dict[str, object]]:
            events.append("inventory")
            return original_read_inventory(inventory_path)

        with (
            patch.object(
                quality_module,
                "load_quality_policy",
                side_effect=tracked_policy,
            ) as load_policy,
            patch.object(
                quality_module,
                "load_taxonomy",
                side_effect=tracked_taxonomy,
            ) as load_taxonomy_mock,
            patch.object(
                quality_module,
                "read_inventory_file",
                side_effect=tracked_inventory,
            ) as read_inventory,
            patch.object(
                quality_module,
                "create_quality_run_directory",
                return_value=run_directory,
            ),
            patch.object(quality_module, "write_json") as write_json_mock,
        ):
            result = quality_module.run_dry_run(self.manifest, path)

        load_policy.assert_called_once_with(self.manifest)
        load_taxonomy_mock.assert_called_once_with(self.manifest)
        read_inventory.assert_called_once_with(path)
        self.assertEqual(events, ["policy", "taxonomy", "inventory"])
        self.assertEqual(
            result["policy_sha256"],
            quality_module._canonical_sha256(first_policy),
        )
        templates = [
            mocked_call.args[1]
            for mocked_call in write_json_mock.call_args_list
            if mocked_call.args[0].name.startswith("assessment-template-")
        ]
        self.assertEqual(
            [template["evaluator"]["id"] for template in templates],
            first_policy["pilot"]["evaluator_ids"],
        )
        self.assertEqual(
            {template["evaluator"]["method_version"] for template in templates},
            {first_policy["pilot"]["method_version"]},
        )
        self.assertTrue(
            all(template["sample_id"] == result["sample_id"] for template in templates)
        )

    def test_dry_run_loads_inputs_once_without_mutating_inventory(self) -> None:
        path = self._write_inventory(self.inventory)
        original_read_inventory = quality_module.read_inventory_file
        original_load_policy = quality_module.load_quality_policy
        original_load_taxonomy = quality_module.load_taxonomy
        original_entry_features = quality_module._entry_features
        loaded_entries: list[list[dict[str, object]]] = []
        original_revision_order: list[str] = []
        original_entry_payloads: list[str] = []

        def tracked_read_inventory(
            inventory_path: Path,
        ) -> tuple[list[dict[str, object]], dict[str, object]]:
            entries, inventory_info = original_read_inventory(inventory_path)
            loaded_entries.append(entries)
            original_revision_order.extend(entry["revision_id"] for entry in entries)
            original_entry_payloads.extend(
                json.dumps(entry, ensure_ascii=False, sort_keys=True)
                for entry in entries
            )
            return entries, inventory_info

        with (
            patch.object(
                quality_module,
                "read_inventory_file",
                side_effect=tracked_read_inventory,
            ) as read_inventory,
            patch.object(
                quality_module,
                "load_quality_policy",
                wraps=original_load_policy,
            ) as load_policy,
            patch.object(
                quality_module,
                "load_taxonomy",
                wraps=original_load_taxonomy,
            ) as load_taxonomy_mock,
            patch.object(
                quality_module,
                "_entry_features",
                wraps=original_entry_features,
            ) as entry_features,
        ):
            dry_run = generate_dry_run(self.manifest, path)

        self.assertEqual(read_inventory.call_count, 1)
        self.assertEqual(load_policy.call_count, 1)
        self.assertEqual(load_taxonomy_mock.call_count, 1)
        self.assertEqual(entry_features.call_count, len(self.inventory))
        self.assertEqual(len(loaded_entries), 1)
        self.assertEqual(len(loaded_entries[0]), len(self.inventory))
        self.assertEqual(
            [entry["revision_id"] for entry in loaded_entries[0]],
            original_revision_order,
        )
        self.assertEqual(
            [
                json.dumps(entry, ensure_ascii=False, sort_keys=True)
                for entry in loaded_entries[0]
            ],
            original_entry_payloads,
        )
        self.assertTrue(all("_features" not in entry for entry in loaded_entries[0]))
        self.assertEqual(
            dry_run["official_sample_id"],
            "e8a266f70202a388b0c7c01686044bcc51e1f7908c05ce21d95e227c5a3259a6",
        )

    def test_dry_run_does_not_cache_mutable_inventory_between_calls(self) -> None:
        path = self._write_inventory(self.inventory)
        original_read_inventory = quality_module.read_inventory_file
        loaded_entries: list[list[dict[str, object]]] = []

        def tracked_read_inventory(
            inventory_path: Path,
        ) -> tuple[list[dict[str, object]], dict[str, object]]:
            entries, inventory_info = original_read_inventory(inventory_path)
            loaded_entries.append(entries)
            return entries, inventory_info

        with patch.object(
            quality_module,
            "read_inventory_file",
            side_effect=tracked_read_inventory,
        ) as read_inventory:
            first = generate_dry_run(self.manifest, path)
            second = generate_dry_run(self.manifest, path)

        self.assertEqual(read_inventory.call_count, 2)
        self.assertEqual(first, second)
        self.assertIsNot(loaded_entries[0], loaded_entries[1])
        self.assertTrue(
            all(
                first_entry is not second_entry
                for first_entry, second_entry in zip(
                    loaded_entries[0], loaded_entries[1]
                )
            )
        )
        self.assertTrue(
            all(
                "_features" not in entry
                for entries in loaded_entries
                for entry in entries
            )
        )


class PiQualityEvaluatorTests(unittest.TestCase):
    """Blind model evaluator runner and host-owned assessment envelope."""

    @classmethod
    def setUpClass(cls) -> None:
        QualityValidationTests.setUpClass()
        cls.manifest = QualityValidationTests.manifest
        cls.taxonomy = QualityValidationTests.taxonomy
        cls.qpolicy = QualityValidationTests.qpolicy
        cls.sample = QualityValidationTests.sample
        cls.sample_path = QualityValidationTests.sample_path

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


class QualityValidationFlagPreflightTests(unittest.TestCase):
    """Validation control flags fail before any artifact I/O."""

    manifest = SimpleNamespace(
        root=Path("/fixture-root"),
        version="fixture-version",
    )
    sample_path = Path("unused-sample.json")
    assessment_path = Path("unused-assessment.json")

    def _assert_rejected_without_io(
        self,
        function: object,
        *,
        strict: object,
        dry_run: object,
        expected_message: str,
    ) -> None:
        with (
            patch.object(quality_module, "load_taxonomy") as load_taxonomy_mock,
            patch.object(
                quality_module, "load_quality_policy"
            ) as load_quality_policy_mock,
            patch.object(quality_module, "_read_json") as read_json_mock,
            patch.object(
                quality_module, "_load_sample_file"
            ) as load_sample_file_mock,
            patch.object(
                quality_module, "_load_assessment"
            ) as load_assessment_mock,
            patch.object(
                quality_module, "create_quality_run_directory"
            ) as create_run_directory,
            patch.object(quality_module, "_write_jsonl") as write_jsonl_mock,
            patch.object(quality_module, "write_json") as write_json_mock,
        ):
            with self.assertRaisesRegex(ValidationError, expected_message):
                function(
                    self.manifest,
                    sample_path=self.sample_path,
                    assessment_paths=[self.assessment_path],
                    adjudication_path=None,
                    strict=strict,
                    dry_run=dry_run,
                )

        for mocked in (
            load_taxonomy_mock,
            load_quality_policy_mock,
            read_json_mock,
            load_sample_file_mock,
            load_assessment_mock,
            create_run_directory,
            write_jsonl_mock,
            write_json_mock,
        ):
            mocked.assert_not_called()

    def test_invalid_control_flag_types_fail_before_io(self) -> None:
        cases = (
            ("strict-zero", 0, False, "strict flag must be None or an exact bool"),
            ("strict-one", 1, False, "strict flag must be None or an exact bool"),
            (
                "strict-string",
                "false",
                False,
                "strict flag must be None or an exact bool",
            ),
            (
                "strict-float",
                1.0,
                False,
                "strict flag must be None or an exact bool",
            ),
            ("dry-zero", True, 0, "dry_run flag must be an exact bool"),
            ("dry-one", True, 1, "dry_run flag must be an exact bool"),
            ("dry-none", True, None, "dry_run flag must be an exact bool"),
            (
                "dry-string",
                True,
                "false",
                "dry_run flag must be an exact bool",
            ),
        )
        functions = (
            quality_module.validate_quality_run,
            quality_module.run_validation,
        )
        for function in functions:
            for label, strict, dry_run, expected_message in cases:
                with self.subTest(function=function.__name__, case=label):
                    self._assert_rejected_without_io(
                        function,
                        strict=strict,
                        dry_run=dry_run,
                        expected_message=expected_message,
                    )

    def test_valid_control_flags_continue_into_mocked_downstream(self) -> None:
        strict_cases = (
            (None, False, False),
            (None, True, True),
            (False, True, False),
            (True, False, True),
        )
        functions = (
            quality_module.validate_quality_run,
            quality_module.run_validation,
        )
        run_directory = (
            self.manifest.root
            / ".artifacts"
            / "i18n"
            / "quality"
            / "runs"
            / "fixture-validation"
        )
        for function in functions:
            for strict, policy_default, expected_strict in strict_cases:
                for dry_run in (False, True):
                    with self.subTest(
                        function=function.__name__,
                        strict=strict,
                        policy_default=policy_default,
                        dry_run=dry_run,
                    ):
                        taxonomy = {"contract": "fixture-taxonomy"}
                        policy = {
                            "strict_unknown_fields": policy_default,
                            "pilot": {
                                "evaluator_ids": ["reviewer-a", "reviewer-b"],
                                "method_version": "fixture-method-v1",
                            },
                        }
                        sample = {
                            "quality_contract": SAMPLE_CONTRACT,
                            "sample_id": "a" * 64,
                            "items_sha256": "c" * 64,
                            "items": [{"revision_id": "b" * 64}],
                        }
                        assessment = {
                            "evaluator_id": "reviewer-a",
                            "evaluator": {
                                "id": "reviewer-a",
                                "kind": "human",
                            },
                            "items": [],
                        }
                        with (
                            patch.object(
                                quality_module,
                                "load_taxonomy",
                                return_value=taxonomy,
                            ) as load_taxonomy_mock,
                            patch.object(
                                quality_module,
                                "load_quality_policy",
                                return_value=policy,
                            ) as load_quality_policy_mock,
                            patch.object(
                                quality_module, "_read_json"
                            ) as read_json_mock,
                            patch.object(
                                quality_module,
                                "_load_sample_file",
                                return_value=sample,
                            ) as load_sample_file_mock,
                            patch.object(
                                quality_module,
                                "_load_assessment",
                                return_value=(assessment, []),
                            ) as load_assessment_mock,
                            patch.object(
                                quality_module,
                                "_validate_assessment_items",
                                return_value=(assessment, []),
                            ) as validate_assessment_items,
                            patch.object(
                                quality_module,
                                "create_quality_run_directory",
                                return_value=run_directory,
                            ) as create_run_directory,
                            patch.object(
                                quality_module, "_write_jsonl"
                            ) as write_jsonl_mock,
                            patch.object(
                                quality_module, "write_json"
                            ) as write_json_mock,
                        ):
                            result = function(
                                self.manifest,
                                sample_path=self.sample_path,
                                assessment_paths=[self.assessment_path],
                                adjudication_path=None,
                                strict=strict,
                                dry_run=dry_run,
                            )

                        self.assertIs(result["strict"], expected_strict)
                        load_taxonomy_mock.assert_called_once_with(self.manifest)
                        load_quality_policy_mock.assert_called_once_with(
                            self.manifest
                        )
                        read_json_mock.assert_not_called()
                        load_sample_file_mock.assert_called_once_with(
                            self.sample_path,
                            manifest=self.manifest,
                            taxonomy=taxonomy,
                            qpolicy=policy,
                            dry_run=dry_run,
                        )
                        self.assertIs(
                            load_assessment_mock.call_args.args[3],
                            expected_strict,
                        )
                        self.assertIs(
                            validate_assessment_items.call_args.args[3],
                            expected_strict,
                        )
                        if function is quality_module.run_validation:
                            create_run_directory.assert_called_once_with(
                                self.manifest.root, "validation"
                            )
                            write_jsonl_mock.assert_called_once()
                            write_json_mock.assert_called_once()
                        else:
                            self.assertIs(result["dry_run"], dry_run)
                            create_run_directory.assert_not_called()
                            write_jsonl_mock.assert_not_called()
                            write_json_mock.assert_not_called()


class QualityValidationTests(unittest.TestCase):
    """Phase-1 doc section 10.4: assessment/adjudication safety checks."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.qpolicy = load_quality_policy(cls.manifest)
        cls.taxonomy = load_taxonomy(cls.manifest)
        cls.sample, cls.sample_path, cls.inventory_path = cls._make_sample()
        cls.dry_sample = generate_dry_run(cls.manifest, cls.inventory_path)
        cls.dry_sample_path = TEST_FIXTURE_ROOT / "quality-validation" / "dry-run.json"
        cls.dry_sample_path.write_text(
            json.dumps(cls.dry_sample, ensure_ascii=False), encoding="utf-8"
        )

    @classmethod
    def _make_sample(cls) -> tuple[dict[str, object], Path, Path]:
        entries = [
            cls._sample_entry(index)
            for index in range(320)
        ]
        directory = TEST_FIXTURE_ROOT / "quality-validation"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "inventory.jsonl"
        path.write_text(
            "\n".join(
                json.dumps(entry, ensure_ascii=False, sort_keys=True) for entry in entries
            )
            + "\n",
            encoding="utf-8",
        )
        path.with_name("inventory-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "quality_contract": quality_module.INVENTORY_CONTRACT,
                    "tool_version": TOOL_VERSION,
                    "version": cls.manifest.version,
                    "manifest_sha256": hashlib.sha256(
                        cls.manifest.raw_bytes
                    ).hexdigest(),
                    "translation_inputs_sha256": (
                        quality_module._current_translation_inputs_sha256(
                            cls.manifest
                        )
                    ),
                    "terminology_sha256": hashlib.sha256(
                        (
                            cls.manifest.root / cls.manifest.terminology
                        ).read_bytes()
                    ).hexdigest(),
                    "taxonomy_sha256": quality_module._canonical_sha256(
                        cls.taxonomy
                    ),
                    "policy_sha256": quality_module._canonical_sha256(
                        cls.qpolicy
                    ),
                    "inventory_sha256": quality_module._canonical_sha256(
                        entries
                    ),
                    "entries": len(entries),
                    "profile_classifier_version": cls.taxonomy[
                        "profile_classifier_version"
                    ],
                    "risk_rule_version": cls.taxonomy["risk_rule_version"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        sample = generate_sample(
            cls.manifest, path, seed="quality-validation-fixture"
        )
        sample_path = directory / "sample.json"
        sample_path.write_text(
            json.dumps(sample, ensure_ascii=False), encoding="utf-8"
        )
        return sample, sample_path, path

    @classmethod
    def _sample_entry(cls, index: int) -> dict[str, object]:
        unit_id = compute_unit_id("tome", "data/v.lua", f"source {index}", None)
        revision_id = compute_revision_id(
            cls.manifest.version, unit_id, f"target {index}", None, None
        )
        structure = structure_signature(f"source {index}", f"target {index}", None)
        return {
            "unit_id": unit_id,
            "revision_id": revision_id,
            "version": cls.manifest.version,
            "component": "tome",
            "section": "data/v.lua",
            "source": f"source {index}",
            "target": f"target {index}",
            "source_tag": None,
            "args_order": None,
            "special": None,
            "occurrences": [
                {
                    "logical_path": "tome.lua",
                    "section": "data/v.lua",
                    "line": index + 1,
                    "ordinal": index,
                }
            ],
            "profile": "mechanics",
            "profile_confidence": "high",
            "domain_hints": [],
            "relevant_terms": [],
            "structure": structure,
            "gate_signals": {
                "lua_load_valid": True,
                "empty_target": False,
                "format_signature_match": None,
                "markup_multiset_match": True,
                "at_token_multiset_match": True,
                "runtime_collision": False,
                "needs_review": [],
            },
            "risk_flags": [],
            "source_length_bin": "short",
        }

    def _assessment(
        self, evaluator_id: str, sample: dict[str, object]
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "quality_contract": ASSESSMENT_CONTRACT,
            "sample_id": sample["sample_id"],
            "evaluator": {
                "kind": "human",
                "id": evaluator_id,
                "method_version": self.qpolicy["pilot"]["method_version"],
            },
            "items": [
                {
                    "revision_id": item["revision_id"],
                    "context_sufficient": True,
                    "profile_confirmed": item["profile"],
                    "findings": [],
                    "reuse_recommendation": "same-tag",
                }
                for item in sample["items"]
            ],
        }

    def _adjudication(
        self, sample: dict[str, object], assessments: list[dict[str, object]]
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "quality_contract": ADJUDICATION_CONTRACT,
            "sample_id": sample["sample_id"],
            "items": [
                {
                    "revision_id": item["revision_id"],
                    "assessment_ids": [
                        assessment["evaluator"]["id"] for assessment in assessments
                    ],
                    "context_sufficient": True,
                    "resolved_findings": [],
                    "quality_vector": {
                        "accuracy": 4,
                        "mechanics_context": 4,
                        "terminology": 4,
                        "fluency": 4,
                        "style": None,
                        "ui_render": None,
                        "corpus_consistency": 4,
                    },
                    "confidence": "C3",
                    "provisional_grade": "Gold",
                    "reuse_scope": "same-tag",
                    "rationale": "fixture adjudication",
                }
                for item in sample["items"]
            ],
        }

    def _write(self, name: str, payload: dict[str, object]) -> Path:
        path = TEST_FIXTURE_ROOT / "quality-validation" / name
        path.write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )
        return path

    def _isolated_upstream_sample(
        self, root: Path
    ) -> tuple[Manifest, dict[str, object], Path]:
        translation_path = root / "canonical.lua"
        copy_fragment_path = root / "copy-fragment.lua"
        terminology_path = root / "terminology.tsv"
        translation_path.write_bytes(b"-- canonical translation fixture\n")
        copy_fragment_path.write_bytes(b"-- copy fragment fixture\n")
        terminology_path.write_bytes(b"fixture terminology bytes\n")
        component = replace(
            self.manifest.component("tome"),
            translation="canonical.lua",
            copy_fragment="copy-fragment.lua",
        )
        manifest = replace(
            self.manifest,
            root=root,
            components=(component,),
            terminology="terminology.tsv",
        )
        sample = copy.deepcopy(self.sample)
        sample["translation_inputs_sha256"] = (
            quality_module._current_translation_inputs_sha256(manifest)
        )
        sample["terminology_sha256"] = hashlib.sha256(
            terminology_path.read_bytes()
        ).hexdigest()
        sample["inventory_tool_version"] = TOOL_VERSION
        self._resign_sample(sample)
        sample_path = root / "sample.json"
        sample_path.write_text(
            json.dumps(sample, ensure_ascii=False), encoding="utf-8"
        )
        return manifest, sample, sample_path

    @staticmethod
    def _resign_sample(payload: dict[str, object]) -> None:
        common_fields = [
            "schema_version",
            "quality_contract",
            "seed",
            "size",
            "items_sha256",
        ]
        if payload["quality_contract"] == SAMPLE_CONTRACT:
            identity_fields = common_fields + [
                "taxonomy_sha256",
                "policy_sha256",
                "manifest_sha256",
                "translation_inputs_sha256",
                "terminology_sha256",
                "inventory_tool_version",
                "inventory_sha256",
                "bucket_targets",
                "bucket_counts",
                "revisions",
            ]
        else:
            identity_fields = common_fields + [
                "official_sample_id",
                "taxonomy_sha256",
                "policy_sha256",
                "manifest_sha256",
                "translation_inputs_sha256",
                "terminology_sha256",
                "inventory_tool_version",
                "inventory_sha256",
                "revisions",
            ]
        identity = {field: payload[field] for field in identity_fields}
        payload["sample_id"] = hashlib.sha256(
            json.dumps(
                identity,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _valid_run(
        self,
        assessment_a: dict[str, object] | None = None,
        assessment_b: dict[str, object] | None = None,
        adjudication: dict[str, object] | None = None,
        strict: bool = True,
    ) -> tuple[dict[str, object], ...]:
        a = assessment_a or self._assessment("reviewer-a", self.sample)
        b = assessment_b or self._assessment("reviewer-b", self.sample)
        adjudication = adjudication or self._adjudication(self.sample, [a, b])
        a_path = self._write("assessment-a.json", a)
        b_path = self._write("assessment-b.json", b)
        adjudication_path = self._write("adjudication.json", adjudication)
        return (
            validate_quality_run(
                self.manifest,
                sample_path=self.sample_path,
                assessment_paths=[a_path, b_path],
                adjudication_path=adjudication_path,
                strict=strict,
            ),
            a,
            b,
            adjudication,
        )

    def _resolved_finding_inputs(
        self,
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        assessment_a = self._assessment("reviewer-a", self.sample)
        assessment_b = self._assessment("reviewer-b", self.sample)
        assessment_a["items"][0]["findings"] = [
            {
                "finding_id": "A-REF",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "fixture assessment finding",
                "evidence_refs": [],
            }
        ]
        adjudication = self._adjudication(
            self.sample, [assessment_a, assessment_b]
        )
        adjudication["items"][0]["resolved_findings"] = [
            {
                "finding_id": "A-REF",
                "evaluator_id": "reviewer-a",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "state": "rejected",
                "body": "",
            }
        ]
        return assessment_a, assessment_b, adjudication

    def test_clean_pilot_validates(self) -> None:
        validation, _, _, _ = self._valid_run()
        self.assertTrue(validation["ok"])
        self.assertEqual(validation["errors"], [])

    def test_upstream_byte_changes_reject_old_sample_before_assessment_io(
        self,
    ) -> None:
        cases = (
            (
                "translation",
                "canonical.lua",
                "sample translation_inputs_sha256 is stale or invalid",
            ),
            (
                "copy-fragment",
                "copy-fragment.lua",
                "sample translation_inputs_sha256 is stale or invalid",
            ),
            (
                "terminology",
                "terminology.tsv",
                "sample terminology_sha256 is stale or invalid",
            ),
        )
        for label, relative_path, expected_error in cases:
            with self.subTest(input=label), tempfile.TemporaryDirectory(
                prefix=f"quality-upstream-{label}-"
            ) as temporary:
                root = Path(temporary)
                manifest, _, sample_path = self._isolated_upstream_sample(root)
                changed_path = root / relative_path
                changed_path.write_bytes(changed_path.read_bytes() + b"-- changed\n")
                with (
                    patch.object(
                        quality_module,
                        "load_taxonomy",
                        return_value=self.taxonomy,
                    ),
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=self.qpolicy,
                    ),
                    patch.object(
                        quality_module, "_load_assessment"
                    ) as load_assessment,
                ):
                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        validate_quality_run(
                            manifest,
                            sample_path=sample_path,
                            assessment_paths=[root / "must-not-be-read.json"],
                            adjudication_path=None,
                            strict=True,
                        )
                load_assessment.assert_not_called()

    def test_sample_freshness_validation_does_not_rebuild_inventory_or_load_lua(
        self,
    ) -> None:
        with (
            patch.object(quality_module, "build_inventory") as build_inventory_mock,
            patch.object(LocaleLoader, "load_path") as load_path_mock,
        ):
            validation, _, _, _ = self._valid_run()

        self.assertTrue(validation["ok"], validation["errors"])
        build_inventory_mock.assert_not_called()
        load_path_mock.assert_not_called()

    def test_adjudication_resolved_finding_contract_table(self) -> None:
        assessment_a, assessment_b, adjudication = (
            self._resolved_finding_inputs()
        )
        validation, _, _, _ = self._valid_run(
            assessment_a=assessment_a,
            assessment_b=assessment_b,
            adjudication=adjudication,
            strict=True,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(
            validation["adjudication"]["items"][0]["resolved_findings"][0][
                "body"
            ],
            "",
        )
        validation_path = self._write(
            "validation-report-resolved-finding-valid.json", validation
        )
        report = run_quality_report(self.manifest, validation_path)
        self.assertEqual(report["sample_id"], validation["sample_id"])

        cases = (
            ("finding-missing", "field", "finding_id", _UNSET,
             ".finding_id: must be a non-empty string"),
            ("finding-null", "field", "finding_id", None,
             ".finding_id: must be a non-empty string"),
            ("finding-empty", "field", "finding_id", "",
             ".finding_id: must be a non-empty string"),
            ("finding-non-string", "field", "finding_id", 7,
             ".finding_id: must be a non-empty string"),
            ("evaluator-missing", "field", "evaluator_id", _UNSET,
             ".evaluator_id: must be a non-empty string"),
            ("evaluator-null", "field", "evaluator_id", None,
             ".evaluator_id: must be a non-empty string"),
            ("evaluator-empty", "field", "evaluator_id", "",
             ".evaluator_id: must be a non-empty string"),
            ("evaluator-non-string", "field", "evaluator_id", ["reviewer-a"],
             ".evaluator_id: must be a non-empty string"),
            ("unknown-finding", "field", "finding_id", "A-GHOST",
             "does not exist in assessment"),
            ("wrong-evaluator", "field", "evaluator_id", "reviewer-b",
             "does not exist in assessment"),
            ("cross-revision", "cross-revision", None, None,
             "does not exist in assessment"),
            ("invalid-rationale", "field", "rationale", None,
             "rationale must be a string"),
        )

        def mutate(
            assessment: dict[str, object],
            adjudicated: dict[str, object],
            mutation: str,
            field: str | None,
            value: object,
        ) -> None:
            if mutation == "cross-revision":
                finding = assessment["items"][0]["findings"].pop()
                assessment["items"][1]["findings"].append(finding)
                return
            resolved = adjudicated["items"][0]["resolved_findings"][0]
            assert field is not None
            if value is _UNSET:
                resolved.pop(field)
            else:
                resolved[field] = copy.deepcopy(value)

        for label, mutation, field, value, expected_error in cases:
            with self.subTest(case=label, path="validate"):
                assessment_a, assessment_b, adjudication = (
                    self._resolved_finding_inputs()
                )
                mutate(assessment_a, adjudication, mutation, field, value)
                invalid, _, _, _ = self._valid_run(
                    assessment_a=assessment_a,
                    assessment_b=assessment_b,
                    adjudication=adjudication,
                    strict=True,
                )
                self.assertFalse(invalid["ok"], invalid["errors"])
                self.assertIn(expected_error, "\n".join(invalid["errors"]))

            with self.subTest(case=label, path="report"):
                forged = copy.deepcopy(validation)
                normalized_assessment_a = next(
                    assessment
                    for assessment in forged["assessments"]
                    if assessment["evaluator_id"] == "reviewer-a"
                )
                mutate(
                    normalized_assessment_a,
                    forged["adjudication"],
                    mutation,
                    field,
                    value,
                )
                validation_path = self._write(
                    f"validation-report-forged-resolved-{label}.json", forged
                )
                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_adjudication_item_contract_table(self) -> None:
        cases = (
            (
                "single-valid-evaluator-subset",
                ["reviewer-a"],
                None,
                True,
                False,
                ("must exactly match valid assessment evaluator ids",),
            ),
            (
                "duplicate-evaluator-id",
                ["reviewer-a", "reviewer-b", "reviewer-a"],
                None,
                True,
                False,
                ("assessment_ids contains duplicates",),
            ),
            (
                "empty-id-array",
                [],
                None,
                True,
                False,
                ("assessment_ids must be a non-empty string array",),
            ),
            (
                "empty-id",
                ["reviewer-a", ""],
                None,
                True,
                False,
                ("assessment_ids[1]: must be a non-empty string",),
            ),
            (
                "object-id",
                ["reviewer-a", {"id": "reviewer-b"}],
                None,
                True,
                False,
                ("assessment_ids[1]: must be a non-empty string",),
            ),
            (
                "array-id",
                ["reviewer-a", ["reviewer-b"]],
                None,
                True,
                False,
                ("assessment_ids[1]: must be a non-empty string",),
            ),
            (
                "unknown-id",
                ["reviewer-a", "ghost-evaluator"],
                None,
                True,
                False,
                (
                    "must exactly match valid assessment evaluator ids",
                    "ghost-evaluator",
                ),
            ),
            (
                "empty-vector-nonstrict",
                _UNSET,
                "empty",
                False,
                False,
                ("quality_vector: missing dimensions",),
            ),
            (
                "missing-vector-dimension-nonstrict",
                _UNSET,
                "missing",
                False,
                False,
                ("quality_vector: missing dimensions ['accuracy']",),
            ),
            (
                "extra-vector-dimension-nonstrict",
                _UNSET,
                "extra",
                False,
                False,
                ("quality_vector: extra dimensions ['undeclared']",),
            ),
            (
                "boolean-vector-value",
                _UNSET,
                "boolean",
                True,
                False,
                ("quality_vector.accuracy: must be 0-4 or null",),
            ),
            (
                "float-vector-value",
                _UNSET,
                "float",
                True,
                False,
                ("quality_vector.accuracy: must be 0-4 or null",),
            ),
            (
                "valid-reversed-evaluator-order",
                ["reviewer-b", "reviewer-a"],
                None,
                True,
                True,
                (),
            ),
        )
        for (
            label,
            assessment_ids,
            vector_mutation,
            strict,
            expected_ok,
            expected_errors,
        ) in cases:
            with self.subTest(case=label):
                assessment_a = self._assessment("reviewer-a", self.sample)
                assessment_b = self._assessment("reviewer-b", self.sample)
                adjudication = self._adjudication(
                    self.sample, [assessment_a, assessment_b]
                )
                item = adjudication["items"][0]
                if assessment_ids is not _UNSET:
                    item["assessment_ids"] = copy.deepcopy(assessment_ids)
                vector = item["quality_vector"]
                if vector_mutation == "empty":
                    item["quality_vector"] = {}
                elif vector_mutation == "missing":
                    vector.pop("accuracy")
                elif vector_mutation == "extra":
                    vector["undeclared"] = 4
                elif vector_mutation == "boolean":
                    vector["accuracy"] = True
                elif vector_mutation == "float":
                    vector["accuracy"] = 4.0

                validation, _, _, _ = self._valid_run(
                    assessment_a=assessment_a,
                    assessment_b=assessment_b,
                    adjudication=adjudication,
                    strict=strict,
                )

                self.assertEqual(
                    validation["ok"], expected_ok, validation["errors"]
                )
                joined_errors = "\n".join(validation["errors"])
                for expected_error in expected_errors:
                    self.assertIn(expected_error, joined_errors)
                if expected_ok:
                    self.assertEqual(validation["errors"], [])
                    self.assertEqual(
                        validation["adjudication"]["items"][0][
                            "assessment_ids"
                        ],
                        assessment_ids,
                    )
                    self.assertEqual(
                        validation["sample_id"], self.sample["sample_id"]
                    )

    def test_dry_run_explicit_adjudication_binds_actual_assessments(self) -> None:
        cases = (
            ("one-exact", ("reviewer-a",), ("reviewer-a",), True),
            (
                "one-with-unprovided-evaluator",
                ("reviewer-a",),
                ("reviewer-a", "reviewer-b"),
                False,
            ),
            (
                "two-subset",
                ("reviewer-a", "reviewer-b"),
                ("reviewer-a",),
                False,
            ),
            (
                "two-reversed",
                ("reviewer-a", "reviewer-b"),
                ("reviewer-b", "reviewer-a"),
                True,
            ),
        )
        for label, evaluator_ids, adjudicated_ids, expected_ok in cases:
            with self.subTest(case=label):
                assessments = [
                    self._assessment(evaluator_id, self.dry_sample)
                    for evaluator_id in evaluator_ids
                ]
                assessment_paths = [
                    self._write(
                        f"assessment-dry-adjudication-{label}-{index}.json",
                        assessment,
                    )
                    for index, assessment in enumerate(assessments)
                ]
                adjudication = self._adjudication(
                    self.dry_sample, assessments
                )
                for item in adjudication["items"]:
                    item["assessment_ids"] = list(adjudicated_ids)
                adjudication_path = self._write(
                    f"adjudication-dry-{label}.json", adjudication
                )

                validation = validate_quality_run(
                    self.manifest,
                    sample_path=self.dry_sample_path,
                    assessment_paths=assessment_paths,
                    adjudication_path=adjudication_path,
                    strict=False,
                    dry_run=True,
                )

                self.assertEqual(
                    validation["ok"], expected_ok, validation["errors"]
                )
                if not expected_ok:
                    self.assertTrue(
                        any(
                            "must exactly match valid assessment evaluator ids"
                            in error
                            for error in validation["errors"]
                        ),
                        validation["errors"],
                    )

    def test_official_assessment_policy_binding_table(self) -> None:
        expected_method = self.qpolicy["pilot"]["method_version"]
        cases = (
            (
                "single-policy-evaluator-with-adjudication",
                (("reviewer-a", expected_method),),
                ("exactly two valid assessments",),
            ),
            (
                "single-typo-and-obsolete-method",
                (("reviewer-typo", "mqm-pilot-v0"),),
                ("evaluator.id", "evaluator.method_version"),
            ),
            (
                "two-with-wrong-id",
                (
                    ("reviewer-a", expected_method),
                    ("reviewer-typo", expected_method),
                ),
                ("evaluator.id",),
            ),
            (
                "two-with-wrong-method",
                (
                    ("reviewer-a", expected_method),
                    ("reviewer-b", "mqm-pilot-v0"),
                ),
                ("evaluator.method_version",),
            ),
        )
        for label, evaluator_specs, expected_errors in cases:
            with self.subTest(case=label):
                assessments = []
                assessment_paths = []
                for index, (evaluator_id, method_version) in enumerate(
                    evaluator_specs
                ):
                    assessment = self._assessment(evaluator_id, self.sample)
                    assessment["evaluator"]["method_version"] = method_version
                    assessments.append(assessment)
                    assessment_paths.append(
                        self._write(f"assessment-policy-{label}-{index}.json", assessment)
                    )
                adjudication_path = self._write(
                    f"adjudication-policy-{label}.json",
                    self._adjudication(self.sample, assessments),
                )

                validation = validate_quality_run(
                    self.manifest,
                    sample_path=self.sample_path,
                    assessment_paths=assessment_paths,
                    adjudication_path=adjudication_path,
                    strict=True,
                )

                self.assertFalse(validation["ok"])
                joined_errors = "\n".join(validation["errors"])
                for expected_error in expected_errors:
                    self.assertIn(expected_error, joined_errors)

    def test_official_assessment_order_is_irrelevant_for_validate_and_report(
        self,
    ) -> None:
        assessment_a = self._assessment("reviewer-a", self.sample)
        assessment_b = self._assessment("reviewer-b", self.sample)
        assessment_a_path = self._write("assessment-order-a.json", assessment_a)
        assessment_b_path = self._write("assessment-order-b.json", assessment_b)
        adjudication_path = self._write(
            "adjudication-order.json",
            self._adjudication(self.sample, [assessment_a, assessment_b]),
        )

        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[assessment_b_path, assessment_a_path],
            adjudication_path=adjudication_path,
            strict=True,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(
            {assessment["evaluator_id"] for assessment in validation["assessments"]},
            {"reviewer-a", "reviewer-b"},
        )
        validation_path = self._write("validation-order-valid.json", validation)
        report = run_quality_report(self.manifest, validation_path)
        self.assertEqual(report["sample_id"], validation["sample_id"])

    def test_assessment_and_adjudication_schemas_reject_non_integer_versions(
        self,
    ) -> None:
        for artifact in ("assessment", "adjudication"):
            for schema_version in (True, 1.0):
                with self.subTest(
                    artifact=artifact, schema_version=schema_version
                ):
                    if artifact == "assessment":
                        assessment = self._assessment("reviewer-a", self.sample)
                        assessment["schema_version"] = schema_version
                        validation, _, _, _ = self._valid_run(
                            assessment_a=assessment
                        )
                    else:
                        assessment_a = self._assessment(
                            "reviewer-a", self.sample
                        )
                        assessment_b = self._assessment(
                            "reviewer-b", self.sample
                        )
                        adjudication = self._adjudication(
                            self.sample, [assessment_a, assessment_b]
                        )
                        adjudication["schema_version"] = schema_version
                        validation, _, _, _ = self._valid_run(
                            assessment_a=assessment_a,
                            assessment_b=assessment_b,
                            adjudication=adjudication,
                        )
                    self.assertFalse(validation["ok"])
                    self.assertTrue(
                        any(
                            f"unsupported {artifact} schema" in error
                            for error in validation["errors"]
                        ),
                        validation["errors"],
                    )

    def test_sample_file_schema_rejects_booleans_and_floats(self) -> None:
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                sample = json.loads(json.dumps(self.sample))
                sample["schema_version"] = schema_version
                sample_path = self._write(
                    f"sample-schema-{str(schema_version).lower()}.json",
                    sample,
                )
                with self.assertRaisesRegex(
                    ValidationError, "unsupported sample schema"
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                    )

    def test_report_embedded_sample_schema_rejects_booleans_and_floats(
        self,
    ) -> None:
        validation, _, _, _ = self._valid_run()
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                payload = json.loads(json.dumps(validation))
                payload["sample"]["schema_version"] = schema_version
                validation_path = self._write(
                    f"validation-sample-schema-{str(schema_version).lower()}.json",
                    payload,
                )
                with self.assertRaisesRegex(
                    ValidationError, "quality validation sample schema is invalid"
                ):
                    run_quality_report(self.manifest, validation_path)

    def test_report_rejects_failed_validation_with_multiple_errors(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation["ok"] = False
        validation["errors"] = ["first fixture failure", "second fixture failure"]
        validation_path = self._write("validation-report-failed.json", validation)

        with self.assertRaises(ValidationError) as caught:
            run_quality_report(self.manifest, validation_path)
        self.assertIn("first fixture failure", str(caught.exception))
        self.assertIn("second fixture failure", str(caught.exception))

    def test_report_rejects_missing_or_invalid_ok(self) -> None:
        validation, _, _, _ = self._valid_run()
        cases = (("missing", None), ("string", "true"), ("integer", 1))
        for label, value in cases:
            with self.subTest(case=label):
                payload = json.loads(json.dumps(validation))
                if label == "missing":
                    payload.pop("ok")
                else:
                    payload["ok"] = value
                validation_path = self._write(
                    f"validation-report-{label}.json", payload
                )
                with self.assertRaisesRegex(
                    ValidationError, "quality validation ok flag is invalid"
                ):
                    run_quality_report(self.manifest, validation_path)

    def test_report_rejects_nonempty_errors_when_ok_is_true(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation["errors"] = ["inconsistent success"]
        validation_path = self._write(
            "validation-report-inconsistent.json", validation
        )

        with self.assertRaisesRegex(ValidationError, "inconsistent success"):
            run_quality_report(self.manifest, validation_path)

    def test_report_rejects_validation_from_stale_quality_rules(self) -> None:
        validation, _, _, _ = self._valid_run()
        for field in ("taxonomy_sha256", "policy_sha256"):
            with self.subTest(field=field):
                stale = json.loads(json.dumps(validation))
                stale[field] = "0" * 64
                validation_path = self._write(
                    f"validation-report-stale-{field}.json", stale
                )
                with self.assertRaisesRegex(
                    ValidationError, rf"{field} is stale or invalid"
                ):
                    run_quality_report(self.manifest, validation_path)

        stale_manifest = json.loads(json.dumps(validation))
        stale_manifest["sample"]["manifest_sha256"] = "0" * 64
        self._resign_sample(stale_manifest["sample"])
        stale_manifest["sample_id"] = stale_manifest["sample"]["sample_id"]
        validation_path = self._write(
            "validation-report-stale-manifest.json", stale_manifest
        )
        with self.assertRaisesRegex(
            ValidationError, "sample manifest_sha256 is stale or invalid"
        ):
            run_quality_report(self.manifest, validation_path)

    def test_report_rejects_old_validation_tool_version_before_output(
        self,
    ) -> None:
        validation, _, _, _ = self._valid_run()
        for label, value in (("missing", _UNSET), ("old", "0.0.0")):
            with self.subTest(case=label):
                payload = copy.deepcopy(validation)
                if value is _UNSET:
                    payload.pop("tool_version")
                else:
                    payload["tool_version"] = value
                validation_path = self._write(
                    f"validation-report-tool-version-{label}.json", payload
                )
                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(
                        ValidationError,
                        "tool_version does not match the current tool version",
                    ):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_report_rechecks_embedded_upstream_dependency_before_output(
        self,
    ) -> None:
        validation, _, _, _ = self._valid_run()
        payload = copy.deepcopy(validation)
        payload["sample"]["translation_inputs_sha256"] = "0" * 64
        self._resign_sample(payload["sample"])
        payload["sample_id"] = payload["sample"]["sample_id"]
        validation_path = self._write(
            "validation-report-stale-translation-inputs.json", payload
        )

        with patch.object(
            quality_module, "create_quality_run_directory"
        ) as create_run_directory:
            with self.assertRaisesRegex(
                ValidationError,
                "sample translation_inputs_sha256 is stale or invalid",
            ):
                run_quality_report(self.manifest, validation_path)
        create_run_directory.assert_not_called()

    def test_report_rechecks_embedded_full_item_payload_digest(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation["sample"]["items"][0]["context_neighbors"].append(
            {
                "component": "tome",
                "section": "data/forged-report-context.lua",
                "source": "forged report context",
                "target": "伪造报告上下文",
                "source_tag": None,
            }
        )
        validation_path = self._write(
            "validation-report-forged-item-payload.json", validation
        )

        with patch.object(
            quality_module, "create_quality_run_directory"
        ) as create_run_directory:
            with self.assertRaisesRegex(
                ValidationError, "items_sha256 does not match items"
            ):
                run_quality_report(self.manifest, validation_path)
        create_run_directory.assert_not_called()

    def test_report_accepts_successful_validation(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation_path = self._write("validation-report-valid.json", validation)

        report = run_quality_report(self.manifest, validation_path)

        self.assertEqual(report["sample_id"], validation["sample_id"])
        self.assertEqual(report["size"], len(self.sample["items"]))
        self.assertTrue((self.manifest.root / report["report_path"]).is_file())
        self.assertTrue((self.manifest.root / report["report_md"]).is_file())

    def test_report_rejects_forged_successful_assessment_identities_before_io(
        self,
    ) -> None:
        official, _, _, _ = self._valid_run()
        official_single = copy.deepcopy(official)
        official_single["assessments"] = official_single["assessments"][:1]

        official_wrong_id = copy.deepcopy(official)
        official_wrong_id["assessments"][1]["evaluator_id"] = "reviewer-typo"
        official_wrong_id["assessments"][1]["evaluator"]["id"] = "reviewer-typo"

        official_wrong_method = copy.deepcopy(official)
        official_wrong_method["assessments"][1]["evaluator"][
            "method_version"
        ] = "mqm-pilot-v0"

        official_mismatched_normalized_id = copy.deepcopy(official)
        official_mismatched_normalized_id["assessments"][1][
            "evaluator_id"
        ] = "reviewer-a"

        dry_assessment = self._assessment("reviewer-a", self.dry_sample)
        dry_assessment_path = self._write(
            "assessment-report-dry-valid.json", dry_assessment
        )
        dry_validation = validate_quality_run(
            self.manifest,
            sample_path=self.dry_sample_path,
            assessment_paths=[dry_assessment_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(dry_validation["ok"], dry_validation["errors"])

        dry_wrong_id = copy.deepcopy(dry_validation)
        dry_wrong_id["assessments"][0]["evaluator_id"] = "reviewer-typo"
        dry_wrong_id["assessments"][0]["evaluator"]["id"] = "reviewer-typo"

        dry_wrong_method = copy.deepcopy(dry_validation)
        dry_wrong_method["assessments"][0]["evaluator"][
            "method_version"
        ] = "mqm-pilot-v0"

        cases = (
            ("official-single", official_single, "exactly two assessments"),
            ("official-wrong-id", official_wrong_id, "evaluator.id"),
            (
                "official-wrong-method",
                official_wrong_method,
                "evaluator.method_version",
            ),
            (
                "official-normalized-id-mismatch",
                official_mismatched_normalized_id,
                "evaluator_id does not match",
            ),
            ("dry-wrong-id", dry_wrong_id, "evaluator.id"),
            ("dry-wrong-method", dry_wrong_method, "evaluator.method_version"),
        )
        for label, payload, expected_error in cases:
            with self.subTest(case=label):
                validation_path = self._write(
                    f"validation-report-forged-{label}.json", payload
                )
                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(ValidationError, expected_error):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_report_rejects_forged_adjudication_contract_before_io(self) -> None:
        validation, _, _, _ = self._valid_run()
        cases = (
            ("assessment-subset", "assessment", "must exactly match"),
            ("non-string-assessment", "non-string", "non-empty string"),
            ("missing-vector-dimension", "missing", "missing dimensions"),
            ("extra-vector-dimension", "extra", "extra dimensions"),
        )
        for label, mutation, expected_error in cases:
            with self.subTest(case=label):
                payload = copy.deepcopy(validation)
                item = payload["adjudication"]["items"][0]
                if mutation == "assessment":
                    item["assessment_ids"] = ["reviewer-a"]
                elif mutation == "non-string":
                    item["assessment_ids"] = [
                        "reviewer-a",
                        {"id": "reviewer-b"},
                    ]
                elif mutation == "missing":
                    item["quality_vector"].pop("accuracy")
                elif mutation == "extra":
                    payload["strict"] = False
                    item["quality_vector"]["undeclared"] = 4
                validation_path = self._write(
                    f"validation-report-forged-adjudication-{label}.json",
                    payload,
                )

                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_quality_report_cli_rejects_failure_and_accepts_success(self) -> None:
        validation, _, _, _ = self._valid_run()
        failed = {
            **validation,
            "ok": False,
            "errors": ["first fixture failure", "second fixture failure"],
        }
        failed_path = self._write("validation-report-cli-failed.json", failed)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = cli_main(
                [
                    "quality",
                    "report",
                    "--validation",
                    str(failed_path),
                    "--json",
                ]
            )
        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertNotIn("OK  quality report", stdout.getvalue())
        self.assertIn("first fixture failure", stderr.getvalue())
        self.assertIn("second fixture failure", stderr.getvalue())

        valid_path = self._write("validation-report-cli-valid.json", validation)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = cli_main(
                [
                    "quality",
                    "report",
                    "--validation",
                    str(valid_path),
                    "--json",
                ]
            )
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(json.loads(stdout.getvalue())["sample_id"], validation["sample_id"])

    def test_current_official_and_dry_run_sample_identities_validate(self) -> None:
        validation, _, _, _ = self._valid_run()
        self.assertTrue(validation["ok"])

        assessment = self._assessment("reviewer-a", self.dry_sample)
        assessment_path = self._write("assessment-valid-dry-run.json", assessment)
        dry_validation = validate_quality_run(
            self.manifest,
            sample_path=self.dry_sample_path,
            assessment_paths=[assessment_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(dry_validation["ok"])

    def test_full_item_payload_tampering_keeps_old_id_and_is_rejected(self) -> None:
        assessment_a = self._assessment("reviewer-a", self.sample)
        assessment_b = self._assessment("reviewer-b", self.sample)
        adjudication = self._adjudication(
            self.sample, [assessment_a, assessment_b]
        )
        assessment_a_path = self._write(
            "assessment-item-payload-a.json", assessment_a
        )
        assessment_b_path = self._write(
            "assessment-item-payload-b.json", assessment_b
        )
        adjudication_path = self._write(
            "adjudication-item-payload.json", adjudication
        )

        def mutate_relevant_terms(item: dict[str, object]) -> None:
            item["relevant_terms"].append(
                {
                    "source": "forged term",
                    "target": "伪造术语",
                    "status": "preferred",
                }
            )

        def mutate_gate_signals(item: dict[str, object]) -> None:
            item["gate_signals"]["needs_review"].append("forged-signal")

        def mutate_context(item: dict[str, object]) -> None:
            item["context_neighbors"].append(
                {
                    "component": "tome",
                    "section": "data/forged.lua",
                    "source": "forged context",
                    "target": "伪造上下文",
                    "source_tag": None,
                }
            )

        def mutate_risk_flags(item: dict[str, object]) -> None:
            item["risk_flags"].append("forged-risk")

        cases = (
            ("relevant-terms", mutate_relevant_terms),
            ("gate-signals", mutate_gate_signals),
            ("context-neighbors", mutate_context),
            ("risk-flags", mutate_risk_flags),
        )
        for label, mutate in cases:
            with self.subTest(field=label):
                sample = copy.deepcopy(self.sample)
                original_sample_id = sample["sample_id"]
                mutate(sample["items"][0])
                self.assertEqual(sample["sample_id"], original_sample_id)
                sample_path = self._write(
                    f"tampered-item-payload-{label}.json", sample
                )

                with self.assertRaisesRegex(
                    ValidationError, "items_sha256 does not match items"
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[
                            assessment_a_path,
                            assessment_b_path,
                        ],
                        adjudication_path=adjudication_path,
                        strict=True,
                    )

    def test_items_digest_shape_and_binding_for_both_contracts(self) -> None:
        missing = object()
        mutations = (
            (
                "missing",
                missing,
                "sample identity is missing items_sha256",
            ),
            (
                "uppercase",
                "A" * 64,
                "items_sha256 is not a SHA-256 digest",
            ),
            (
                "non-string",
                ["not", "a", "digest"],
                "items_sha256 is not a SHA-256 digest",
            ),
            (
                "mismatch",
                "0" * 64,
                "items_sha256 does not match items",
            ),
        )
        for contract_label, original, dry_run in (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        ):
            for mutation_label, value, expected_error in mutations:
                with self.subTest(
                    contract=contract_label, mutation=mutation_label
                ):
                    sample = copy.deepcopy(original)
                    if value is missing:
                        sample.pop("items_sha256")
                    else:
                        sample["items_sha256"] = value
                    sample_path = self._write(
                        f"items-digest-{contract_label}-{mutation_label}.json",
                        sample,
                    )

                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        validate_quality_run(
                            self.manifest,
                            sample_path=sample_path,
                            assessment_paths=[],
                            adjudication_path=None,
                            strict=True,
                            dry_run=dry_run,
                        )

    def test_dry_run_assessment_policy_binding_table(self) -> None:
        expected_method = self.qpolicy["pilot"]["method_version"]
        cases = (
            ("valid-policy-subset", "reviewer-b", expected_method, True, None),
            (
                "wrong-id",
                "reviewer-typo",
                expected_method,
                False,
                "evaluator.id",
            ),
            (
                "wrong-method",
                "reviewer-a",
                "mqm-pilot-v0",
                False,
                "evaluator.method_version",
            ),
        )
        for label, evaluator_id, method_version, expected_ok, expected_error in cases:
            with self.subTest(case=label):
                assessment = self._assessment(evaluator_id, self.dry_sample)
                assessment["evaluator"]["method_version"] = method_version
                assessment_path = self._write(
                    f"assessment-dry-policy-{label}.json", assessment
                )

                validation = validate_quality_run(
                    self.manifest,
                    sample_path=self.dry_sample_path,
                    assessment_paths=[assessment_path],
                    adjudication_path=None,
                    strict=True,
                    dry_run=True,
                )

                self.assertEqual(validation["ok"], expected_ok)
                if expected_error is not None:
                    self.assertTrue(
                        any(
                            expected_error in error
                            for error in validation["errors"]
                        ),
                        validation["errors"],
                    )

    def test_sample_item_identity_tampering_rejected_for_both_contracts(self) -> None:
        cases = (
            ("official-target", self.sample, False, "target", "revision_id"),
            ("official-source", self.sample, False, "source", "unit_id"),
            ("dry-run-args", self.dry_sample, True, "args_order", "revision_id"),
            ("dry-run-section", self.dry_sample, True, "section", "unit_id"),
        )
        for label, original, dry_run, field, expected_error in cases:
            with self.subTest(case=label):
                sample = json.loads(json.dumps(original))
                item = sample["items"][0]
                if field == "args_order":
                    item[field] = [1]
                else:
                    item[field] += "-tampered"
                sample_path = self._write(f"tampered-{label}.json", sample)
                with self.assertRaisesRegex(
                    ValidationError,
                    rf"{expected_error} does not match",
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_malformed_item_identity_type_raises_validation_error(self) -> None:
        for label, original, dry_run in (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        ):
            with self.subTest(contract=label):
                sample = json.loads(json.dumps(original))
                sample["items"][0]["component"] = ["not", "a", "string"]
                sample_path = self._write(f"malformed-item-{label}.json", sample)
                with self.assertRaisesRegex(
                    ValidationError, "sample item 0 component is invalid"
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_stale_sample_rule_digests_rejected_for_both_contracts(self) -> None:
        samples = (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        )
        for label, original, dry_run in samples:
            for field in (
                "manifest_sha256",
                "taxonomy_sha256",
                "policy_sha256",
                "translation_inputs_sha256",
                "terminology_sha256",
            ):
                with self.subTest(contract=label, field=field):
                    sample = json.loads(json.dumps(original))
                    sample[field] = "0" * 64
                    self._resign_sample(sample)
                    sample_path = self._write(
                        f"stale-{label}-{field}.json", sample
                    )
                    with self.assertRaisesRegex(
                        ValidationError, rf"{field} is stale or invalid"
                    ):
                        validate_quality_run(
                            self.manifest,
                            sample_path=sample_path,
                            assessment_paths=[],
                            adjudication_path=None,
                            strict=True,
                            dry_run=dry_run,
                        )

    def test_stale_inventory_tool_version_rejected_for_both_contracts(
        self,
    ) -> None:
        for label, original, dry_run in (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        ):
            with self.subTest(contract=label):
                sample = copy.deepcopy(original)
                sample["inventory_tool_version"] = "0.0.0"
                self._resign_sample(sample)
                sample_path = self._write(
                    f"stale-{label}-inventory-tool-version.json", sample
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "inventory_tool_version is stale or invalid",
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_wrong_sample_artifact_id_rejected_for_both_contracts(self) -> None:
        samples = (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        )
        for label, original, dry_run in samples:
            with self.subTest(contract=label):
                sample = json.loads(json.dumps(original))
                sample["sample_id"] = "0" * 64
                sample_path = self._write(f"wrong-id-{label}.json", sample)
                with self.assertRaisesRegex(
                    ValidationError,
                    "sample_id does not match canonical sample identity",
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_inventory_digest_is_shape_checked_and_bound_to_sample_id(self) -> None:
        malformed = json.loads(json.dumps(self.sample))
        malformed["inventory_sha256"] = "not-a-digest"
        self._resign_sample(malformed)
        malformed_path = self._write("malformed-inventory-digest.json", malformed)
        with self.assertRaisesRegex(
            ValidationError, "inventory_sha256 is not a SHA-256 digest"
        ):
            validate_quality_run(
                self.manifest,
                sample_path=malformed_path,
                assessment_paths=[],
                adjudication_path=None,
                strict=True,
            )

        unbound = json.loads(json.dumps(self.sample))
        unbound["inventory_sha256"] = "0" * 64
        unbound_path = self._write("unbound-inventory-digest.json", unbound)
        with self.assertRaisesRegex(
            ValidationError, "sample_id does not match canonical sample identity"
        ):
            validate_quality_run(
                self.manifest,
                sample_path=unbound_path,
                assessment_paths=[],
                adjudication_path=None,
                strict=True,
            )

    def test_dry_run_validation_without_adjudication(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        b = self._assessment("reviewer-b", self.sample)
        a_path = self._write("assessment-a-dry.json", a)
        b_path = self._write("assessment-b-dry.json", b)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path, b_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["dry_run"])
        self.assertEqual(validation["adjudication"], {"items": []})
        self.assertTrue(
            any("non-official" in warning for warning in validation["warnings"])
        )

    def test_dry_run_validation_runner_forwards_flag(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        a_path = self._write("assessment-runner-dry.json", a)
        report = run_quality_validation(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        validation = json.loads(
            (self.manifest.root / report["validation_path"]).read_text(encoding="utf-8")
        )
        self.assertTrue(report["ok"])
        self.assertTrue(validation["dry_run"])

    def test_official_sample_requires_adjudication(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        a_path = self._write("assessment-a-no-adjudication.json", a)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path],
            adjudication_path=None,
            strict=True,
        )
        self.assertFalse(validation["ok"])
        self.assertTrue(
            any("adjudication is required" in error for error in validation["errors"])
        )

    def test_dry_run_contract_sample_accepted_with_flag(self) -> None:
        dry_sample = self.dry_sample
        sample_path = self.dry_sample_path
        a = self._assessment("reviewer-a", dry_sample)
        a_path = self._write("assessment-a-dry-contract.json", a)
        validation = validate_quality_run(
            self.manifest,
            sample_path=sample_path,
            assessment_paths=[a_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["dry_run"])
        with self.assertRaises(ValidationError):
            validate_quality_run(
                self.manifest,
                sample_path=sample_path,
                assessment_paths=[a_path],
                adjudication_path=None,
                strict=True,
            )

    def test_policy_default_strict_rejects_unknown_fields(self) -> None:
        # policy-v1 declares strict_unknown_fields=true; validate without an
        # explicit --strict flag must still reject unknown fields.
        a = self._assessment("reviewer-a", self.sample)
        a["items"][0]["unexpected_field"] = "sneaky"
        a_path = self._write("assessment-a-strict.json", a)
        b = self._assessment("reviewer-b", self.sample)
        b_path = self._write("assessment-b-strict.json", b)
        adjudication = self._adjudication(self.sample, [a, b])
        adjudication_path = self._write("adjudication-strict.json", adjudication)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path, b_path],
            adjudication_path=adjudication_path,
            strict=None,
        )
        self.assertFalse(validation["ok"])
        self.assertTrue(any("unknown fields" in error for error in validation["errors"]))

    def test_root_and_evaluator_unknown_fields_rejected(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        a["unexpected_root"] = "sneaky"
        a_path = self._write("assessment-a-root.json", a)
        b = self._assessment("reviewer-b", self.sample)
        b["evaluator"]["unexpected_evaluator"] = "sneaky"
        b_path = self._write("assessment-b-root.json", b)
        adjudication = self._adjudication(self.sample, [a, b])
        adjudication_path = self._write("adjudication-root.json", adjudication)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path, b_path],
            adjudication_path=adjudication_path,
            strict=True,
        )
        self.assertFalse(validation["ok"])
        root_errors = [
            error for error in validation["errors"] if "unexpected_root" in error
        ]
        evaluator_errors = [
            error for error in validation["errors"]
            if "unexpected_evaluator" in error
        ]
        self.assertTrue(root_errors)
        self.assertTrue(evaluator_errors)

    def test_unknown_error_code_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][0]["findings"] = [
            {
                "finding_id": "B-001",
                "error_code": "NOT_A_CODE",
                "severity": "major",
                "source_span": "",
                "target_span": "",
                "body": "fixture",
                "evidence_refs": [],
            }
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("unknown error code" in error for error in validation["errors"]))

    def test_absolute_path_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][1]["findings"] = [
            {
                "finding_id": "B-002",
                "error_code": "ACC_MISTRANSLATION",
                "severity": "major",
                "source_span": "",
                "target_span": "",
                "body": "see /Users/yun/private/file.lua for mechanics",
                "evidence_refs": [],
            }
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("host absolute path" in error for error in validation["errors"]))

    def test_duplicate_finding_id_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][2]["findings"] = [
            {
                "finding_id": "DUP",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "one",
                "evidence_refs": [],
            },
            {
                "finding_id": "DUP",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "two",
                "evidence_refs": [],
            },
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("duplicate finding_id" in error for error in validation["errors"]))

    def test_incomplete_coverage_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"] = b["items"][:-1]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("incomplete coverage" in error for error in validation["errors"]))

    def test_sample_id_mismatch_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["sample_id"] = "0" * 64
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("sample_id does not match" in error for error in validation["errors"]))

    def test_unknown_revision_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][0]["revision_id"] = "1" * 64
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("unknown revision_id" in error for error in validation["errors"]))

    def test_adjudication_missing_assessment_rejected(self) -> None:
        adjudication = self._adjudication(self.sample, [])
        adjudication["items"][0]["assessment_ids"] = ["ghost-evaluator"]
        validation, _, _, _ = self._valid_run(adjudication=adjudication)
        self.assertFalse(validation["ok"])
        self.assertTrue(
            any(
                "must exactly match valid assessment evaluator ids" in error
                for error in validation["errors"]
            )
        )

    def test_gold_with_confirmed_blocker_rejected(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        b = self._assessment("reviewer-b", self.sample)
        a["items"][3]["findings"] = [
            {
                "finding_id": "A-003",
                "error_code": "TECH_FORMAT",
                "severity": "blocker",
                "source_span": "0:4",
                "target_span": "0:4",
                "body": "missing argument",
                "evidence_refs": [],
            }
        ]
        adjudication = self._adjudication(self.sample, [a, b])
        for item in adjudication["items"]:
            if item["revision_id"] == a["items"][3]["revision_id"]:
                item["resolved_findings"] = [
                    {
                        "finding_id": "A-003",
                        "evaluator_id": "reviewer-a",
                        "error_code": "TECH_FORMAT",
                        "severity": "blocker",
                        "state": "confirmed",
                        "body": "missing argument",
                    }
                ]
        validation, _, _, _ = self._valid_run(
            assessment_a=a, adjudication=adjudication
        )
        self.assertFalse(validation["ok"])
        self.assertTrue(
            any("confirmed blocker/major" in error for error in validation["errors"])
        )

    def test_rejected_finding_does_not_block_grade(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        b = self._assessment("reviewer-b", self.sample)
        a["items"][4]["findings"] = [
            {
                "finding_id": "A-004",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "subjective",
                "evidence_refs": [],
            }
        ]
        adjudication = self._adjudication(self.sample, [a, b])
        for item in adjudication["items"]:
            if item["revision_id"] == a["items"][4]["revision_id"]:
                item["resolved_findings"] = [
                    {
                        "finding_id": "A-004",
                        "evaluator_id": "reviewer-a",
                        "error_code": "FLU_AWKWARD",
                        "severity": "minor",
                        "state": "rejected",
                        "body": "subjective",
                        "rationale": "not a defect",
                    }
                ]
        validation, _, _, _ = self._valid_run(
            assessment_a=a, adjudication=adjudication
        )
        self.assertTrue(validation["ok"])

    def test_assessment_must_cover_all_sample_revisions(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"] = [
            item for item in b["items"] if item["revision_id"] != b["items"][0]["revision_id"]
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])


class QualityMetricsTests(unittest.TestCase):
    """Phase-1 doc section 8: agreement and finding-matching metrics."""

    @staticmethod
    def _risk_flag_metrics(
        items: list[dict[str, object]],
        finding_states: dict[str, str | None],
    ) -> dict[str, object]:
        assessments = [
            {
                "evaluator_id": evaluator_id,
                "evaluator": {
                    "kind": "human",
                    "method_version": "fixture",
                },
                "items": [
                    {
                        "revision_id": item["revision_id"],
                        "context_sufficient": True,
                        "profile_confirmed": item["profile"],
                        "findings": [],
                    }
                    for item in items
                ],
            }
            for evaluator_id in ("reviewer-a", "reviewer-b")
        ]
        adjudication_items = []
        for item in items:
            revision_id = item["revision_id"]
            state = finding_states[revision_id]
            resolved_findings = []
            if state is not None:
                resolved_findings.append(
                    {
                        "finding_id": f"finding-{revision_id}",
                        "error_code": "ACC_MISTRANSLATION",
                        "severity": "minor",
                        "state": state,
                    }
                )
            adjudication_items.append(
                {
                    "revision_id": revision_id,
                    "resolved_findings": resolved_findings,
                    "provisional_grade": "Silver",
                    "confidence": "C3",
                    "reuse_scope": "same-tag",
                }
            )
        validation = {
            "sample_id": "fixture-sample",
            "sample": {"items": items},
            "assessments": assessments,
            "adjudication": {"items": adjudication_items},
        }
        taxonomy = {
            "mergeable_codes": [],
            "error_codes": [{"code": "ACC_MISTRANSLATION"}],
        }
        return build_report(validation, taxonomy)["risk_flags"]

    def test_risk_flag_stats_distinguish_coverage_from_confirmed_hits(self) -> None:
        items = [
            {
                "revision_id": "confirmed",
                "bucket": "representative",
                "profile": "mechanics",
                "risk_flags": ["shared", "multiple"],
            },
            {
                "revision_id": "unconfirmed",
                "bucket": "risk-enriched",
                "profile": "mechanics",
                "risk_flags": [
                    "shared",
                    "unconfirmed-only",
                    "multiple",
                    "shared",
                ],
            },
            {
                "revision_id": "confirmed-no-flags",
                "bucket": "representative",
                "profile": "mechanics",
                "risk_flags": [],
            },
            {
                "revision_id": "partially-confirmed",
                "bucket": "risk-enriched",
                "profile": "mechanics",
                "risk_flags": ["multiple", "partial-only"],
            },
        ]
        states = {
            "confirmed": "confirmed",
            "unconfirmed": "rejected",
            "confirmed-no-flags": "confirmed",
            "partially-confirmed": "partially_confirmed",
        }
        risk_flags = self._risk_flag_metrics(items, states)

        self.assertEqual(risk_flags["confirmed_items"], 3)
        self.assertEqual(risk_flags["confirmed_with_any_flag"], 2)
        self.assertEqual(risk_flags["coverage"], 0.6667)
        self.assertEqual(
            risk_flags["per_flag"],
            {
                "shared": {"flagged": 2, "with_confirmed": 1},
                "multiple": {"flagged": 3, "with_confirmed": 2},
                "unconfirmed-only": {"flagged": 1, "with_confirmed": 0},
                "partial-only": {"flagged": 1, "with_confirmed": 1},
            },
        )

    def test_risk_flag_stats_are_safe_without_confirmed_items(self) -> None:
        items = [
            {
                "revision_id": "rejected",
                "bucket": "risk-enriched",
                "profile": "mechanics",
                "risk_flags": ["shared", "rejected-only", "shared"],
            },
            {
                "revision_id": "clean",
                "bucket": "representative",
                "profile": "mechanics",
                "risk_flags": ["shared", "clean-only"],
            },
        ]

        risk_flags = self._risk_flag_metrics(
            items,
            {"rejected": "rejected", "clean": None},
        )

        self.assertEqual(risk_flags["confirmed_items"], 0)
        self.assertEqual(risk_flags["confirmed_with_any_flag"], 0)
        self.assertIsNone(risk_flags["coverage"])
        self.assertEqual(
            risk_flags["per_flag"],
            {
                "shared": {"flagged": 2, "with_confirmed": 0},
                "rejected-only": {"flagged": 1, "with_confirmed": 0},
                "clean-only": {"flagged": 1, "with_confirmed": 0},
            },
        )

    def test_weighted_kappa_perfect_and_random(self) -> None:
        self.assertEqual(_weighted_kappa([0, 1, 2], [0, 1, 2], 5), 1.0)
        kappa = _weighted_kappa([0, 0, 1, 1], [1, 1, 0, 0], 3)
        self.assertIsNotNone(kappa)
        self.assertLess(kappa, 0)
        self.assertIsNone(_weighted_kappa([], [], 5))

    def test_finding_matching_requires_category_compatible_codes(self) -> None:
        left = [
            {
                "finding_id": "A-1",
                "error_code": "ACC_MISTRANSLATION",
                "severity": "major",
                "source_span": "0:5",
                "target_span": "0:5",
                "body": "",
                "evidence_refs": [],
            }
        ]
        right = [
            {
                "finding_id": "B-1",
                "error_code": "ACC_CONDITION",
                "severity": "major",
                "source_span": "0:5",
                "target_span": "0:5",
                "body": "",
                "evidence_refs": [],
            }
        ]
        mergeable = {
            ("ACC_CONDITION", "ACC_MISTRANSLATION"),
        }
        matches = _match_findings(left, right, mergeable)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][1]["finding_id"], "B-1")
        non_mergeable = {("FLU_AWKWARD", "ACC_MISTRANSLATION")}
        self.assertEqual(_match_findings(left, right, non_mergeable), [])

    def test_finding_matching_respects_span_overlap(self) -> None:
        left = [
            {
                "finding_id": "A-1",
                "error_code": "ACC_CONDITION",
                "severity": "major",
                "source_span": "0:5",
                "target_span": "0:5",
                "body": "",
                "evidence_refs": [],
            }
        ]
        right = [
            {
                "finding_id": "B-1",
                "error_code": "ACC_CONDITION",
                "severity": "major",
                "source_span": "10:20",
                "target_span": "10:20",
                "body": "",
                "evidence_refs": [],
            }
        ]
        self.assertEqual(
            _match_findings(
                left, right, {("ACC_CONDITION", "ACC_CONDITION")}
            ),
            [],
        )


class QualityRuntimeSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()
        cls.manifest = replace(
            cls.base_manifest,
            components=(
                replace(
                    cls.base_manifest.components[0],
                    id="alpha",
                    translation="alpha.lua",
                    copy_fragment=None,
                ),
                replace(
                    cls.base_manifest.components[1],
                    id="beta",
                    translation="beta.lua",
                    copy_fragment=None,
                ),
            ),
        )

    @staticmethod
    def _document(
        logical_path: str, records: tuple[dict[str, object], ...]
    ) -> LocaleDocument:
        return LocaleDocument(
            logical_path=logical_path,
            sha256="0" * 64,
            records=records,
        )

    @staticmethod
    def _record(
        source: str,
        target: str,
        section: str,
        *,
        args_order: object = None,
        special: object = None,
    ) -> dict[str, object]:
        return {
            "kind": "translation",
            "source": source,
            "target": target,
            "source_tag": None,
            "section": section,
            "args_order": args_order,
            "special": special,
        }

    def test_inventory_translation_digest_uses_loaded_bytes_in_consumption_order(
        self,
    ) -> None:
        manifest = replace(
            self.base_manifest,
            components=(
                replace(
                    self.base_manifest.components[0],
                    id="alpha",
                    copy_fragment="shared.lua",
                    translation="shared.lua",
                ),
                replace(
                    self.base_manifest.components[1],
                    id="beta",
                    copy_fragment="shared.lua",
                    translation="shared.lua",
                ),
            ),
        )
        loaded_sha256 = tuple(str(index) * 64 for index in range(1, 5))
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = tuple(
            LocaleDocument(
                logical_path="shared.lua",
                sha256=sha256,
                records=(),
            )
            for sha256 in loaded_sha256
        )

        inventory = build_inventory(manifest, loader)

        self.assertEqual(loader.load_path.call_count, 4)
        self.assertEqual(
            inventory["translation_inputs_sha256"],
            quality_module._canonical_sha256(
                [
                    {
                        "component": component,
                        "role": role,
                        "logical_path": "shared.lua",
                        "sha256": sha256,
                    }
                    for (component, role), sha256 in zip(
                        (
                            ("alpha", "copy_fragment"),
                            ("alpha", "translation"),
                            ("beta", "copy_fragment"),
                            ("beta", "translation"),
                        ),
                        loaded_sha256,
                    )
                ]
            ),
        )

    def test_inventory_and_contrast_groups_use_complete_runtime_semantics(
        self,
    ) -> None:
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            self._document(
                "alpha.lua",
                (
                    self._record(
                        "Within args %s %s",
                        "参数 %s %s",
                        "alpha/args.lua",
                        args_order=[1, 2],
                    ),
                    self._record(
                        "Within args %s %s",
                        "参数 %s %s",
                        "alpha/args.lua",
                        args_order=[2, 1],
                    ),
                    self._record(
                        "Within special",
                        "特殊",
                        "alpha/special.lua",
                        special={"nested": [True]},
                    ),
                    self._record(
                        "Within special",
                        "特殊",
                        "alpha/special.lua",
                        special={"nested": [1]},
                    ),
                    self._record(
                        "Across components",
                        "跨组件",
                        "alpha/cross.lua",
                        special={"nested": [False]},
                    ),
                ),
            ),
            self._document(
                "beta.lua",
                (
                    self._record(
                        "Across components",
                        "跨组件",
                        "beta/cross.lua",
                        special={"nested": [0]},
                    ),
                ),
            ),
        )

        inventory = build_inventory(self.manifest, loader)
        entries = inventory["entries_list"]

        within = [
            entry for entry in entries if entry["source"].startswith("Within")
        ]
        across = [
            entry for entry in entries if entry["source"] == "Across components"
        ]
        self.assertEqual(len(within), 4)
        self.assertTrue(
            all(entry["gate_signals"]["runtime_collision"] for entry in within)
        )
        self.assertEqual(len(across), 2)
        self.assertTrue(
            all(
                entry["gate_signals"]["cross_component_variant"]
                for entry in across
            )
        )
        self.assertTrue(
            all(
                not entry["gate_signals"]["runtime_collision"]
                for entry in across
            )
        )

        groups = quality_module._contrast_groups(
            entries, load_quality_policy(self.base_manifest)
        )
        multi_value_sources = {
            members[0]["source"]
            for group_id, members in groups
            if group_id.startswith("multi-value:")
        }
        self.assertEqual(
            multi_value_sources, {"Within args %s %s", "Within special"}
        )
        invalid_entry = dict(entries[0])
        invalid_entry["special"] = {"value": float("inf")}
        with self.assertRaises(ValidationError):
            quality_module._contrast_groups(
                [invalid_entry, entries[1]],
                load_quality_policy(self.base_manifest),
            )

    def test_noncanonical_inventory_semantics_fail_before_report_write(
        self,
    ) -> None:
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            self._document(
                "alpha.lua",
                (
                    self._record(
                        "Invalid",
                        "无效",
                        "alpha/invalid.lua",
                        special={"value": float("nan")},
                    ),
                ),
            ),
            self._document(
                "beta.lua",
                (self._record("Valid", "有效", "beta/valid.lua"),),
            ),
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-semantics-"
        ) as temporary:
            old_run = Path(temporary)
            old_inventory = old_run / "inventory.jsonl"
            old_manifest = old_run / "inventory-manifest.json"
            old_inventory.write_bytes(b"old inventory\n")
            old_manifest.write_bytes(b"old manifest\n")
            with patch.object(
                quality_module,
                "create_quality_run_directory",
                return_value=old_run,
            ) as create_run:
                with self.assertRaises(ValidationError):
                    quality_module.run_inventory(self.manifest, loader)

            create_run.assert_not_called()
            self.assertEqual(old_inventory.read_bytes(), b"old inventory\n")
            self.assertEqual(old_manifest.read_bytes(), b"old manifest\n")


class QualityInventoryIntegrationTests(unittest.TestCase):
    """Phase-1 doc section 10.5: real-corpus inventory conservation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

    def test_inventory_conserves_loader_counts_and_is_deterministic(self) -> None:
        with (
            patch.object(
                quality_module,
                "load_quality_policy",
                wraps=load_quality_policy,
            ) as load_policy_mock,
            patch.object(
                quality_module,
                "load_taxonomy",
                wraps=load_taxonomy,
            ) as load_taxonomy_mock,
        ):
            first = build_inventory(self.manifest, self.loader)
        load_policy_mock.assert_called_once_with(self.manifest)
        load_taxonomy_mock.assert_called_once_with(self.manifest)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(
            first["policy_sha256"], canonical(load_quality_policy(self.manifest))
        )
        self.assertEqual(
            first["taxonomy_sha256"], canonical(load_taxonomy(self.manifest))
        )
        loader_translations = 0
        for component in self.manifest.components:
            paths = [component.translation]
            if component.copy_fragment:
                paths.insert(0, component.copy_fragment)
            for logical_path in paths:
                document = self.loader.load_path(
                    self.manifest.root / logical_path, logical_path=logical_path
                )
                loader_translations += len(document.translations)
        self.assertEqual(first["summary"]["occurrences"], loader_translations)
        self.assertEqual(first["summary"]["entries"], len(first["entries_list"]))
        self.assertGreater(first["summary"]["entries"], 10000)
        second = build_inventory(self.manifest, self.loader)
        self.assertEqual(first["inventory_sha256"], second["inventory_sha256"])
        self.assertEqual(first["entries_list"], second["entries_list"])


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


class CiGatesScriptTests(unittest.TestCase):
    script = TOOLS / "ci-gates.sh"

    @staticmethod
    def _fake_environment(directory: Path) -> dict[str, str]:
        fake_python = directory / "python3"
        fake_python.write_text(
            """#!/bin/sh
if [ -n "${CI_GATES_TEST_SENTINEL:-}" ]; then
    printf 'python3 %s\n' "$*" >> "$CI_GATES_TEST_SENTINEL"
fi
printf '%s\n' "$*"
exit 17
""",
            encoding="utf-8",
        )
        fake_python.chmod(0o755)

        fake_git = directory / "git"
        fake_git.write_text(
            """#!/bin/sh
if [ -n "${CI_GATES_TEST_SENTINEL:-}" ]; then
    printf 'git %s\n' "$*" >> "$CI_GATES_TEST_SENTINEL"
fi
printf '%s\n' "$*"
exit 0
""",
            encoding="utf-8",
        )
        fake_git.chmod(0o755)

        environment = os.environ.copy()
        environment["PATH"] = f"{directory}{os.pathsep}{environment['PATH']}"
        return environment

    def _run(
        self, environment: dict[str, str], *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.script), *arguments],
            cwd=ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def _log_directory(self, stdout: str) -> Path:
        prefix = "CI gate log directory: "
        matches = [
            line[len(prefix) :]
            for line in stdout.splitlines()
            if line.startswith(prefix)
        ]
        self.assertEqual(len(matches), 1, msg=stdout)
        return Path(matches[0])

    def test_gate_logs_are_per_step_and_sequential_runs_are_isolated(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ci-gates-fakes-") as temporary:
            environment = self._fake_environment(Path(temporary))
            skip_build = self._run(environment, "--skip-build")
            with_build = self._run(environment)

        for completed in (skip_build, with_build):
            self.assertEqual(
                completed.returncode,
                1,
                msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertEqual(completed.stderr, "")

        skip_log_dir = self._log_directory(skip_build.stdout)
        build_log_dir = self._log_directory(with_build.stdout)
        self.assertNotEqual(skip_log_dir, build_log_dir)
        expected_parent = ROOT / ".artifacts" / "i18n" / "ci-gates"
        self.assertEqual(skip_log_dir.parent, expected_parent)
        self.assertEqual(build_log_dir.parent, expected_parent)

        expected_logs = {
            "01-doctor.log": "-B tools/i18n doctor\n",
            "02-strict-lint.log": "-B tools/i18n lint --strict\n",
            "03-toolchain-unit-tests.log": (
                "-m unittest -q tests/i18n/test_toolchain.py\n"
            ),
            "04-quality-facts-unit-tests.log": (
                "-m unittest -q tests/i18n/test_quality_contracts.py "
                "tests/i18n/test_quality_claims.py "
                "tests/i18n/test_dataset_registry.py "
                "tests/i18n/test_quality_v2.py "
                "tests/i18n/test_quality_v3.py "
                "tests/i18n/test_facts_study.py "
                "tests/i18n/test_facts_curation.py\n"
            ),
            "05-runtime-collision-scan.log": (
                "-B tools/scan_runtime_collisions.py\n"
            ),
            "06-runtime-key-classification.log": (
                "-B tools/classify_runtime_keys.py\n"
            ),
            "07-terminology-static-audit.log": "-B tools/audit_static.py\n",
            "08-terminology-dynamic-audit.log": "-B tools/audit_dynamic.py\n",
            "09-domain-annotation.log": "-B tools/annotate_domains.py\n",
            "10-worktree-whitespace.log": "diff --check\n",
        }
        actual_logs = {
            path.name: path.read_text(encoding="utf-8")
            for path in skip_log_dir.glob("*.log")
        }
        self.assertEqual(actual_logs, expected_logs)
        failure_paths = [
            skip_log_dir / log_name
            for log_name in expected_logs
            if log_name != "10-worktree-whitespace.log"
        ]
        self.assertEqual(len(failure_paths), len(set(failure_paths)))
        for failure_path in failure_paths:
            self.assertIn(
                f"(log: {failure_path})", skip_build.stdout
            )

        build_log = build_log_dir / "11-core-addon-build.log"
        self.assertEqual(
            build_log.read_text(encoding="utf-8"),
            "-B tools/i18n build --profile addon --component tome "
            "--require-complete\n",
        )
        self.assertIn(f"(log: {build_log})", with_build.stdout)

    def test_concurrent_runs_use_different_log_directories(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ci-gates-fakes-") as temporary:
            environment = self._fake_environment(Path(temporary))
            processes = [
                subprocess.Popen(
                    [str(self.script), "--skip-build"],
                    cwd=ROOT,
                    env=environment,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                for _ in range(2)
            ]
            results: list[tuple[int, str, str]] = []
            try:
                for process in processes:
                    stdout, stderr = process.communicate(timeout=30)
                    results.append((process.returncode, stdout, stderr))
            finally:
                for process in processes:
                    if process.poll() is None:
                        process.kill()
                        process.wait()

        for returncode, stdout, stderr in results:
            self.assertEqual(returncode, 1, msg=f"stdout:\n{stdout}\nstderr:\n{stderr}")
            self.assertEqual(stderr, "")
        log_directories = [
            self._log_directory(stdout) for _, stdout, _ in results
        ]
        self.assertEqual(len(set(log_directories)), 2)
        self.assertTrue(
            set(log_directories[0].glob("*.log")).isdisjoint(
                set(log_directories[1].glob("*.log"))
            )
        )

    def test_invalid_arguments_fail_before_any_gate_runs(self) -> None:
        cases = (
            (("--unknown",), "unknown argument: --unknown"),
            (
                ("--skip-build", "extra"),
                "expected no arguments or exactly --skip-build",
            ),
        )
        with tempfile.TemporaryDirectory(prefix="ci-gates-fakes-") as temporary:
            directory = Path(temporary)
            environment = self._fake_environment(directory)
            for index, (arguments, expected_error) in enumerate(cases):
                with self.subTest(arguments=arguments):
                    sentinel = directory / f"gate-executed-{index}"
                    case_environment = environment.copy()
                    case_environment["CI_GATES_TEST_SENTINEL"] = str(sentinel)
                    completed = self._run(case_environment, *arguments)

                    self.assertEqual(completed.returncode, 2)
                    self.assertEqual(completed.stdout, "")
                    self.assertIn(expected_error, completed.stderr)
                    self.assertIn("Usage:", completed.stderr)
                    self.assertFalse(sentinel.exists())


if __name__ == "__main__":
    unittest.main()
