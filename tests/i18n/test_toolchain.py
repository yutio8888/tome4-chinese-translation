from __future__ import annotations

import atexit
import contextlib
import hashlib
import io
import sys
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path


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
from i18nlib.pi_agent import run_pi_translation
from i18nlib.pi_remediate import run_pi_remediation
from i18nlib.pi_review import _validate_findings, run_pi_review
from i18nlib.pi_tmux import run_tmux_remediation, run_tmux_review, run_worker_job
from i18nlib.proposal import validate_proposal
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


if __name__ == "__main__":
    unittest.main()
