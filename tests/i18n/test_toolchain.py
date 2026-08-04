from __future__ import annotations

import atexit
import contextlib
from dataclasses import replace
import hashlib
import io
import sys
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
TEST_FIXTURE_ROOT = ROOT / ".artifacts" / "i18n" / "test-fixtures"


def _cleanup_test_fixtures() -> None:
    shutil.rmtree(TEST_FIXTURE_ROOT, ignore_errors=True)


_cleanup_test_fixtures()
atexit.register(_cleanup_test_fixtures)

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib import TOOL_VERSION
from i18nlib.config import load_manifest
from i18nlib.build import _lua_string, build_addon_locale
from i18nlib.cli import _parser as cli_parser
from i18nlib.errors import AgentError, ValidationError
from i18nlib.git_source import GitRepository
from i18nlib.lint import (
    Policy,
    extract_format_tokens,
    lint_documents,
    lint_terminology,
    stable_entry_id,
)
from i18nlib.locale_model import LocaleLoader
from i18nlib.merge import classify_merge
from i18nlib.pi_agent import _copy_isolated_oauth_credential, run_pi_translation
from i18nlib.pi_file_review import (
    _file_review_cache_key,
    _git_worktree_snapshot,
    build_file_review_command,
    run_pi_file_review,
)
from i18nlib.pi_remediate import run_pi_remediation
from i18nlib.pi_review import _review_cache_key, _validate_findings, run_pi_review
from i18nlib.pi_quality import (
    _decode_quality_model_output,
    build_quality_evaluator_bundle,
    build_quality_evaluator_command,
    run_pi_quality_evaluator,
)
from i18nlib.pi_tmux import (
    run_tmux_file_review,
    run_tmux_remediation,
    run_tmux_review,
    run_worker_job,
)
from i18nlib.proposal import validate_proposal
from i18nlib.quality import (
    ADJUDICATION_CONTRACT,
    ASSESSMENT_CONTRACT,
    SAMPLE_CONTRACT,
    DRY_RUN_CONTRACT,
    _match_findings,
    _weighted_kappa,
    build_inventory,
    compute_revision_id,
    compute_unit_id,
    generate_sample,
    load_quality_policy,
    load_taxonomy,
    run_validation as run_quality_validation,
    structure_signature,
    validate_quality_run,
)
from i18nlib.review import (
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    _bundle_id,
    _is_public_review_path,
    _redact_absolute_paths,
    _review_index_id,
    validate_review_bundle,
)
from i18nlib.runtime import LuaRuntime
from i18nlib.snapshot import read_snapshot
from i18nlib.workset import (
    _plain_source,
    _relevant_terms,
    _resolve_manifest_path,
    create_workset,
    validate_workset_items,
)


EMPTY_POLICY = Policy(frozenset(), frozenset(), frozenset())


def create_workset_fixture(
    manifest: object, directory: Path
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


class ManifestTests(unittest.TestCase):
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


class ReviewScopeTests(unittest.TestCase):
    def test_pi_agent_analysis_is_in_public_review_scope(self) -> None:
        self.assertTrue(_is_public_review_path("pi-agent-analysis.md"))
        self.assertFalse(_is_public_review_path("private/pi-agent-analysis.md"))

    def test_review_cli_requires_an_explicit_scope(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                cli_parser().parse_args(["review"])
        arguments = cli_parser().parse_args(
            ["review", "--scope", "code", "--scope", "translations"]
        )
        self.assertEqual(arguments.scope, ["code", "translations"])


class AddonBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

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


class FormatTests(unittest.TestCase):
    def test_printf_tokenizer_skips_literal_percent(self) -> None:
        tokens = extract_format_tokens("%0.2f damage, %d turns, %d%% chance")
        self.assertEqual([token.raw for token in tokens], ["%0.2f", "%d", "%d"])


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
    def test_current_terminology_structure_is_valid(self) -> None:
        issues, metrics = lint_terminology(ROOT / "terminology.tsv")
        self.assertGreater(metrics["rows"], 0)
        self.assertFalse([issue for issue in issues if issue.severity == "error"])


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

    def test_review_bundle_redacts_absolute_paths(self) -> None:
        redacted, count = _redact_absolute_paths(
            "path /Users/yun/projects/t-engine4/game/dlcs/file.lua"
        )
        self.assertEqual(count, 1)
        self.assertNotIn("/Users/yun", redacted)
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
                tampered = json.loads(cache_path.read_text(encoding="utf-8"))
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
            os.environ["FAKE_PI_CWD"] = str(cwd_path)
            try:
                report = run_pi_file_review(
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
                os.environ.pop("FAKE_PI_CWD", None)
            arguments = json.loads(arguments_path.read_text())
            cwd = cwd_path.read_text(encoding="utf-8")
        self.assertTrue(report["ok"])
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertEqual(report["cache_decision"], "disabled")
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

    def test_pi_file_review_cache_is_separate_from_isolated_review(self) -> None:
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
            fake_pi = directory / "fake-pi-file-review-cache"
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
            provider = f"fixture-file-cache-{directory.name}"
            prompt_sha = "fixture-prompt-sha256"
            file_key = _file_review_cache_key(
                bundle_id=bundle["bundle_id"],
                provider=provider,
                model="fixture-model",
                thinking="high",
                prompt_sha256=prompt_sha,
                strict=True,
            )
            isolated_key = _review_cache_key(
                bundle_id=bundle["bundle_id"],
                provider=provider,
                model="fixture-model",
                thinking="high",
                prompt_sha256=prompt_sha,
                strict=True,
            )
            self.assertNotEqual(file_key, isolated_key)
            first = run_pi_file_review(
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
                second = run_pi_file_review(
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
        self.assertTrue(second["pi_tools"])

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
            fake_tmux, _ = self._fake_tmux(directory)
            fake_pi = self._fake_pi_review(directory)
            report = run_tmux_file_review(
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
        self.assertTrue(report["ok"])
        self.assertEqual(report["execution"], "tmux")
        self.assertTrue(report["versioned_worktree_unchanged"])
        self.assertNotIn("--no-tools", arguments)
        self.assertEqual(arguments[arguments.index("--tools") + 1], "read,bash")

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
        records, matcher, by_plain, prefix_terms = _build_term_index(rows)
        terms = _relevant_terms_for(
            "fire damage on hit",
            "damage type",
            "tome",
            records,
            matcher,
            by_plain,
            prefix_terms,
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
        return path

    def test_sample_is_deterministic_and_satisfies_constraints(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_sample(self.manifest, path)
        second = generate_sample(self.manifest, path)
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
        from i18nlib.quality import generate_dry_run

        path = self._write_inventory(self.inventory)
        first = generate_dry_run(self.manifest, path)
        second = generate_dry_run(self.manifest, path)
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


class QualityValidationTests(unittest.TestCase):
    """Phase-1 doc section 10.4: assessment/adjudication safety checks."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.qpolicy = load_quality_policy(cls.manifest)
        cls.taxonomy = load_taxonomy(cls.manifest)
        cls.sample, cls.sample_path = cls._make_sample()

    @classmethod
    def _make_sample(cls) -> tuple[dict[str, object], Path]:
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
        sample = generate_sample(
            cls.manifest, path, seed="quality-validation-fixture"
        )
        sample_path = directory / "sample.json"
        sample_path.write_text(
            json.dumps(sample, ensure_ascii=False), encoding="utf-8"
        )
        return sample, sample_path

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

    def _valid_run(
        self,
        assessment_a: dict[str, object] | None = None,
        assessment_b: dict[str, object] | None = None,
        adjudication: dict[str, object] | None = None,
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
                strict=True,
            ),
            a,
            b,
            adjudication,
        )

    def test_clean_pilot_validates(self) -> None:
        validation, _, _, _ = self._valid_run()
        self.assertTrue(validation["ok"])
        self.assertEqual(validation["errors"], [])

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
        dry_sample = dict(self.sample)
        dry_sample["quality_contract"] = DRY_RUN_CONTRACT
        sample_path = self._write("dry-run-sample.json", dry_sample)
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
        self.assertTrue(any("unknown assessments" in error for error in validation["errors"]))

    def test_gold_with_confirmed_blocker_rejected(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
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
        adjudication = self._adjudication(self.sample, [a])
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
        adjudication = self._adjudication(self.sample, [a])
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


class QualityInventoryIntegrationTests(unittest.TestCase):
    """Phase-1 doc section 10.5: real-corpus inventory conservation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

    def test_inventory_conserves_loader_counts_and_is_deterministic(self) -> None:
        first = build_inventory(self.manifest, self.loader)
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


if __name__ == "__main__":
    unittest.main()
