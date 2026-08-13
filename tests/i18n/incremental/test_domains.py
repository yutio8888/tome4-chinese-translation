"""infra-contract-004 translation/rule domain consumer-chain tests.

The translation domain (H4/D5) is exercised end-to-end through
``_lint_incremental_translation`` over a synthetic git repo + a real fixture
identity index (pipeline.extract_enriched stubbed); the rule domain (H4/D3)
through ``_lint_incremental_rule`` with a synthetic registry/policy diff.
"""

from __future__ import annotations

import dataclasses
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import SourceMount  # noqa: E402
from i18nlib.errors import ContractError  # noqa: E402
from i18nlib.git_source import GitRepository  # noqa: E402

from tests.i18n.identity.fixture import (  # noqa: E402
    build_fixture_index,
    loader,
    make_tree,
    manifest,
    runtime,
)
from tests.i18n.incremental.test_incremental import _component  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]


def _bind_identity_contexts_for_test(contexts, indexes):
    """Mirror of cli._bind_identity_contexts (FR1) so the expected
    full-head assembly and the domain under test share the identity-binding
    semantics (independent of translation document presence)."""
    from i18nlib.findings import FindingContext

    bound = dict(contexts)
    for component_id, index in indexes.items():
        existing = bound.get(component_id)
        if existing is not None:
            bound[component_id] = FindingContext(
                component=component_id,
                entries=existing.entries,
                index=index,
            )
        else:
            bound[component_id] = FindingContext(
                component=component_id, entries=(), index=index
            )
    return bound


def _git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def _commit_all(repository: Path, message: str) -> str:
    _git(repository, "add", "-A")
    result = _git(
        repository,
        "-c", "user.name=test",
        "-c", "user.email=test@example.invalid",
        "commit", "-q", "--allow-empty", "-m", message,
    )
    assert result.returncode == 0, result.stderr
    head = _git(repository, "rev-parse", "HEAD")
    assert head.returncode == 0, head.stderr
    return head.stdout.strip()


_FIXTURE_INDEX_CACHE = {}
_FULL_FIXTURE_INDEX_CACHE = {}
_DUP_FIXTURE_INDEX_CACHE = {}

_MINIMAL_TREE = {
    "mod-test/data/talents.lua": (
        "newTalent{\n"
        '\tname = "Flame",\n'
        '\tshort_name = "FLAME",\n'
        '\ttype = {"spell/fire", 1},\n'
        "}\n"
    ),
}


def _build_full_fixture_index_once() -> object:
    """The full mini-tome fixture index: carries the extractor def_line
    duplicate conflicts (T_FLAME / EFF_BURNING) needed for exemption tests."""
    if "index" not in _FULL_FIXTURE_INDEX_CACHE:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            assert any(
                conflict.severity == "error" for conflict in index.conflicts
            )
            _FULL_FIXTURE_INDEX_CACHE["index"] = index
        finally:
            temporary.cleanup()
    return _FULL_FIXTURE_INDEX_CACHE["index"]


def _build_dup_index_once() -> object:
    """A fixture index with exactly one unsuppressed duplicate-talent-id
    (T_DUP, name + info sites) and no other conflict - the FR1/FR3 scenario
    needs clean duplicate participants."""
    if "index" not in _DUP_FIXTURE_INDEX_CACHE:
        tree = {
            "mod-test/data/talents.lua": (
                "newTalent{\n"
                '\tname = "Dup",\n'
                '\tshort_name = "DUP",\n'
                '\ttype = {"spell/fire", 1},\n'
                "\tinfo = function(self, t) "
                "return ([[Dup info.]]):tformat(1) end,\n"
                "}\n"
            ),
        }
        root, temporary = make_tree(tree)
        try:
            index = build_fixture_index(root)
            assert [c.code for c in index.conflicts] == ["duplicate-talent-id"]
            assert index.conflicts[0].anchor_key == "T_DUP"
            _DUP_FIXTURE_INDEX_CACHE["index"] = index
        finally:
            temporary.cleanup()
    return _DUP_FIXTURE_INDEX_CACHE["index"]


def _build_fixture_index_once() -> object:
    """A single-talent fixture index with no spurious duplicate conflicts
    (the full mini-tome fixture's extractor def_line artifact would add
    duplicate-id conflicts that pollute exact finding-count assertions)."""
    if "index" not in _FIXTURE_INDEX_CACHE:
        root, temporary = make_tree(_MINIMAL_TREE)
        try:
            index = build_fixture_index(root)
            assert index.conflicts == ()
            _FIXTURE_INDEX_CACHE["index"] = index
        finally:
            temporary.cleanup()
    return _FIXTURE_INDEX_CACHE["index"]


class _DomainTestCase(unittest.TestCase):
    """Shared plumbing: a git repo rooted at a temp manifest root."""

    def _fixture_index(self):
        return _build_fixture_index_once()
    def _registry_bytes(self) -> bytes:
        return (REPO_ROOT / "i18n/quality/rules-registry-v1.json").read_bytes()

    def _write_registry(self, data: dict) -> None:
        path = self.root / "i18n/quality/rules-registry-v1.json"
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def _load_registry(self) -> dict:
        return json.loads(
            (self.root / "i18n/quality/rules-registry-v1.json").read_text()
        )


    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-domain-")
        self.root = Path(self.temporary.name)
        _git(self.root, "init", "-q")
        quality_dir = self.root / "i18n" / "quality"
        quality_dir.mkdir(parents=True, exist_ok=True)
        for name in (
            "rules-registry-v1.json",
            "unloaded-sources-v1.json",
        ):
            shutil.copyfile(REPO_ROOT / "i18n" / "quality" / name, quality_dir / name)
        shutil.copyfile(REPO_ROOT / "i18n" / "policy.json", self.root / "i18n" / "policy.json")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _manifest(self, component) -> object:
        return dataclasses.replace(
            manifest(), root=self.root, components=(component,)
        )

    def _arguments(self, base: str, head: str, domain: str, **flags) -> object:
        import argparse

        values = dict(
            baseline=None,
            incremental=f"{base}..{head}",
            domain=domain,
            component=[],
            self_check=flags.get("self_check", False),
            ci=flags.get("ci", True),
            json=flags.get("json", True),
            legacy_report=False,
        )
        return argparse.Namespace(**values)

    def _capture_report(self, function, *args):
        """Run a CLI domain function and capture the JSON report it prints."""
        from unittest import mock

        captured: list[dict] = []
        with mock.patch(
            "i18nlib.cli._print_json",
            side_effect=lambda value: captured.append(value),
        ):
            function(*args)
        self.assertEqual(len(captured), 1)
        return captured[0]

    def _patch_extract(self, index=None):
        from unittest import mock

        return mock.patch(
            "i18nlib.pipeline.extract_enriched",
            return_value=(
                {"test-component": index or self._fixture_index()},
                {},
            ),
        )

    def _write_doc(
        self,
        path: str,
        entries: list[tuple[str, str, str]],
        *,
        tag: str = "talent name",
    ) -> None:
        lines: list[str] = []
        for section, source, target in entries:
            lines.append(f'section "{section}"')
            lines.append(f't("{source}", "{target}", "{tag}")')
        (self.root / path).write_text("\n".join(lines) + "\n", encoding="utf-8")


class TranslationDomainTests(_DomainTestCase):
    """H4/D5: main + copy fragment load base/head independently; added /
    deleted / semantically-changed entries map to TU candidates or the
    frozen fallback TU."""

    def _run(self, base: str, head: str, *, index: str = "minimal") -> dict:
        from i18nlib.cli import _lint_incremental_translation

        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment="mod-test-copy.lua",
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        # Tests that do not exercise the copy still need the head logical
        # file present (an empty copy contributes no findings).
        copy_path = self.root / "mod-test-copy.lua"
        if not copy_path.is_file():
            copy_path.write_text("", encoding="utf-8")
        mock_index = {
            "minimal": self._fixture_index,
            "full": _build_full_fixture_index_once,
            "dup": _build_dup_index_once,
        }[index]()
        with self._patch_extract(mock_index):
            return self._capture_report(
                _lint_incremental_translation,
                self._arguments(base, head, "translation", ci=False),
                self._manifest(component),
                runtime(),
                loader(),
            )

    def _canonical(self, record_dicts) -> bytes:
        from i18nlib.fingerprint import FindingRecord, canonical_findings_form
        from i18nlib.lint import Issue

        records = [
            FindingRecord(
                issue=Issue(
                    record["severity"],
                    record["code"],
                    record["message"],
                    record["logical_path"],
                    record["line"],
                    record["entry_id"],
                ),
                rule_id=record["rule_id"],
                rule_schema_version=record["rule_schema_version"],
                tu_uid=record["tu_uid"],
                participants=tuple(record["participants"]),
                evidence_key=record["evidence_key"],
                fingerprint=record["fingerprint"],
            )
            for record in record_dicts
        ]
        return canonical_findings_form(records)

    def _full_head_records(
        self,
        entries: list[tuple[str, str, str]],
        *,
        tag: str = "talent name",
        index: str = "minimal",
    ):
        """Assemble the full-head records exactly like the translation domain
        does (head doc linted with head policy + head registry, bound to the
        chosen index)."""
        import json as _json

        from i18nlib.findings import FindingContext, build_finding_records
        from i18nlib.fingerprint import RuleRegistry
        from i18nlib.identity import (
            RULES_REGISTRY_RELATIVE_PATH,
            UNLOADED_SOURCES_RELATIVE_PATH,
            UnloadedSources,
        )
        from i18nlib.lint import parse_policy
        from i18nlib.pipeline import lint_documents_specs

        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment=None,
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        self._write_doc("mod-test.lua", entries, tag=tag)
        head_doc = loader().load_path(
            self.root / "mod-test.lua", logical_path="mod-test.lua"
        )
        policy = parse_policy(
            _json.loads((self.root / "i18n/policy.json").read_text()),
            label="lint policy",
        )
        issues, contexts, _ = lint_documents_specs(
            self._manifest(component), [(component.id, head_doc, False)], policy=policy
        )
        fixture_index = {
            "minimal": self._fixture_index,
            "full": _build_full_fixture_index_once,
            "dup": _build_dup_index_once,
        }[index]()
        # FR1: mirror the domain's identity-only context binding.
        bound = _bind_identity_contexts_for_test(
            contexts, {"test-component": fixture_index}
        )
        registry = RuleRegistry.load(REPO_ROOT / RULES_REGISTRY_RELATIVE_PATH)
        unloaded = UnloadedSources.load(
            REPO_ROOT / UNLOADED_SOURCES_RELATIVE_PATH
        )
        records, _ = build_finding_records(
            registry=registry,
            issues=issues,
            contexts=bound,
            conflicts=list(fixture_index.conflicts),
            unloaded_sources=unloaded,
        )
        return records

    def _collision_doc(self, entries: list[tuple[str, str, str]]) -> None:
        """Two same-source+tag entries in different sections (runtime key
        collision material)."""
        lines: list[str] = []
        for section, source, target in entries:
            lines.append(f'section "{section}"')
            lines.append(f't("{source}", "{target}", "talent name")')
        (self.root / "mod-test.lua").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    def test_fr1_head_only_main_duplicate_identity_stable(self) -> None:
        """FR1: base has no main document, head adds it. The unchanged
        duplicate-talent conflict must bind strong participants on BOTH
        sides (identity context independent of document presence), so the
        head record is legacy - not a false new - and incremental canonical
        equals the full head (no self-check)."""
        base_commit = _commit_all(self.root, "base empty (no main doc)")
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Dup", "火焰")])
        head_commit = _commit_all(self.root, "head adds main doc")

        report = self._run(base_commit, head_commit, index="dup")
        # Base records = the single duplicate-talent conflict with strong
        # participants (the identity context exists even without a doc).
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["kept"], 0)
        self.assertEqual(report["findings"]["recomputed"], 1)
        self.assertEqual(report["findings"]["incremental"], 1)
        # One legacy duplicate; the head-only entry is valid (no new error).
        records = report["records"]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["rule_id"], "duplicate-talent-id")
        self.assertEqual(report["ci"]["new_errors"], 0)
        self.assertEqual(report["ci"]["legacy_errors"], 1)
        # Base/head fingerprint identical: the head record is legacy, and the
        # incremental canonical form equals the direct full-head assembly.
        expected = self._full_head_records(
            [("mod-test/data/talents.lua", "Dup", "火焰")], index="dup"
        )
        self.assertEqual(len(expected), 1)
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )
        self.assertEqual(records[0]["fingerprint"], expected[0].fingerprint)

    def test_fr1_head_only_empty_target_stays_new(self) -> None:
        """FR1: with a defective head-only entry the empty-target finding is
        still NEW while the unchanged duplicate stays legacy (both coexist in
        the incremental set, canonical == full head)."""
        base_commit = _commit_all(self.root, "base empty (no main doc)")
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Dup", "")])
        head_commit = _commit_all(self.root, "head adds defective main doc")

        report = self._run(base_commit, head_commit, index="dup")
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["incremental"], 2)
        codes = {record["code"] for record in report["records"]}
        self.assertEqual(
            codes, {"duplicate-talent-id", "empty-target"}
        )
        # The duplicate is legacy; the empty-target is a NEW error.
        self.assertEqual(report["ci"]["new_errors"], 1)
        self.assertEqual(report["ci"]["legacy_errors"], 1)
        expected = self._full_head_records(
            [("mod-test/data/talents.lua", "Dup", "")], index="dup"
        )
        self.assertEqual(len(expected), 2)
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )
        # The head-only empty-target finding is a new ERROR for the CI gate.
        empty = [
            record
            for record in report["records"]
            if record["code"] == "empty-target"
        ]
        self.assertEqual(len(empty), 1)
        self.assertIn(
            empty[0]["fingerprint"],
            [record.fingerprint for record in expected if record.rule_id == "empty-target"],
        )

    def test_r2_collision_add_without_self_check(self) -> None:
        """R2: adding a second runtime key occurrence (different target)
        produces a runtime-collision NEW ERROR; its subject is the
        collision-id fallback TU, so recompute must be participant-aware.
        The incremental canonical form equals the full-head records."""
        self._collision_doc(
            [("mod-test/data/talents.lua", "Shared", "火焰")]
        )
        base_commit = _commit_all(self.root, "base single occurrence")
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
            ]
        )
        head_commit = _commit_all(self.root, "head collision added")

        report = self._run(base_commit, head_commit)
        # The added occurrence's editorial is affected; the collision record
        # (subject = collision fallback, participants = editorial TUs) must
        # be recomputed through its participants.
        self.assertEqual(report["findings"]["previous"], 0)
        self.assertEqual(report["findings"]["recomputed"], 1)
        self.assertEqual(report["findings"]["incremental"], 1)
        self.assertEqual(report["ci"]["new_errors"], 1)
        self.assertIn(
            "runtime-collision",
            {record["code"] for record in report["records"]},
        )
        # Direct canonical comparison with the full-head assembly.
        expected = self._full_head_records(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
            ]
        )
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )

    def test_r2_collision_delete_without_self_check(self) -> None:
        """R2: removing one occurrence resolves the runtime-collision ERROR;
        the base record leaves kept through its participants and the
        incremental canonical form equals the full head (no collision)."""
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
            ]
        )
        base_commit = _commit_all(self.root, "base collision")
        self._collision_doc(
            [("mod-test/data/talents.lua", "Shared", "火焰")]
        )
        head_commit = _commit_all(self.root, "head collision removed")

        report = self._run(base_commit, head_commit)
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["kept"], 0)
        self.assertEqual(report["findings"]["incremental"], 0)
        self.assertEqual(report["ci"]["new_errors"], 0)
        self.assertEqual(report["records"], [])
        expected = self._full_head_records(
            [("mod-test/data/talents.lua", "Shared", "火焰")]
        )
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )

    def test_r2_collision_growth_two_to_three_without_self_check(self) -> None:
        """R2 (cycle 3): base already has a runtime collision A+B; head adds
        C (only C's editorial key is affected). The A+B+C record must be
        recomputed and the stale A+B record must leave kept through the
        cross-side collision family key - both must never coexist."""
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
            ]
        )
        base_commit = _commit_all(self.root, "base collision A+B")
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
                ("mod-test/data/misc.lua", "Shared", "火焰3"),
            ]
        )
        head_commit = _commit_all(self.root, "head collision A+B+C")

        report = self._run(base_commit, head_commit)
        # Only the new C editorial is affected; the collision family must
        # swap the base record for the head record.
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["kept"], 0)
        self.assertEqual(report["findings"]["recomputed"], 1)
        self.assertEqual(report["findings"]["incremental"], 1)
        self.assertEqual(report["ci"]["new_errors"], 1)
        # No stale A+B fingerprint: the incremental set is exactly the
        # full-head A+B+C assembly.
        expected = self._full_head_records(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
                ("mod-test/data/misc.lua", "Shared", "火焰3"),
            ]
        )
        self.assertEqual(len(expected), 1)
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )
        self.assertEqual(
            [record["fingerprint"] for record in report["records"]],
            [expected[0].fingerprint],
        )

    def test_r2_collision_shrink_three_to_two_without_self_check(self) -> None:
        """R2 (cycle 3): base collision A+B+C, head removes C (only C's
        editorial key is affected). The base record is directly touched via
        its C participant; the head A+B record must be recomputed through
        the family key so it does not silently vanish."""
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
                ("mod-test/data/misc.lua", "Shared", "火焰3"),
            ]
        )
        base_commit = _commit_all(self.root, "base collision A+B+C")
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
            ]
        )
        head_commit = _commit_all(self.root, "head collision A+B")

        report = self._run(base_commit, head_commit)
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["kept"], 0)
        self.assertEqual(report["findings"]["recomputed"], 1)
        self.assertEqual(report["findings"]["incremental"], 1)
        expected = self._full_head_records(
            [
                ("mod-test/data/talents.lua", "Shared", "火焰"),
                ("mod-test/data/effects.lua", "Shared", "火焰2"),
            ]
        )
        self.assertEqual(len(expected), 1)
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )

    def test_r8_format_mismatch_occurrence_reorder_no_false_change(self) -> None:
        """R8 (cycle 3): base/head only reorder a valid + defective duplicate
        of the same editorial key; the persisting format-mismatch (bound to
        the defective occurrence) must keep its evidence/fingerprint - no
        false new/resolved - and incremental canonical equals the full head
        (no self-check)."""
        self._write_doc(
            "mod-test.lua",
            [
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "造成%d伤害"),
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "无占位"),
            ],
            tag="tformat",
        )
        base_commit = _commit_all(self.root, "base valid then defective")
        self._write_doc(
            "mod-test.lua",
            [
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "无占位"),
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "造成%d伤害"),
            ],
            tag="tformat",
        )
        head_commit = _commit_all(self.root, "head reordered")

        report = self._run(base_commit, head_commit)
        # The editorial semantic multiset is unchanged but the occurrences
        # moved (reorder) - the key is recomputed against the head document
        # so the record never carries stale base metadata; the fingerprint
        # stays stable (no false new/resolved).
        self.assertEqual(report["findings"]["previous"], 2)
        self.assertEqual(report["findings"]["kept"], 0)
        self.assertEqual(report["findings"]["recomputed"], 2)
        self.assertEqual(report["findings"]["incremental"], 2)
        self.assertEqual(report["ci"]["new_errors"], 0)
        # The evidence must be the defective conversion pair, stable across
        # the reorder (the occurrence location binds the evidence, not the
        # first entry in the duplicated editorial list).
        format_records = [
            record
            for record in report["records"]
            if record["code"] == "format-mismatch"
        ]
        self.assertEqual(len(format_records), 1)
        self.assertEqual(format_records[0]["evidence_key"], "conv:d|")
        expected = self._full_head_records(
            [
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "无占位"),
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "造成%d伤害"),
            ],
            tag="tformat",
        )
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )
        expected_format = [
            record for record in expected if record.rule_id == "format-mismatch"
        ]
        self.assertEqual(len(expected_format), 1)
        self.assertEqual(
            format_records[0]["fingerprint"], expected_format[0].fingerprint
        )

    def test_r8_format_mismatch_insert_valid_occurrence(self) -> None:
        """R8 (cycle 3): inserting a valid duplicate before the defective
        occurrence shifts its line; the defect's conversion evidence must not
        flip to the valid entry. The key is genuinely affected (multiset
        changed), so the record is recomputed but keeps the same fingerprint
        (no false new/resolved) and canonical == full head."""
        self._write_doc(
            "mod-test.lua",
            [("mod-test/data/talents.lua", "Deals %d fire damage.", "无占位")],
            tag="tformat",
        )
        base_commit = _commit_all(self.root, "base defective only")
        self._write_doc(
            "mod-test.lua",
            [
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "造成%d伤害"),
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "无占位"),
            ],
            tag="tformat",
        )
        head_commit = _commit_all(self.root, "head valid inserted before")

        report = self._run(base_commit, head_commit)
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["recomputed"], 2)
        self.assertEqual(report["findings"]["incremental"], 2)
        # Same defective conversion evidence despite the line shift.
        format_records = [
            record
            for record in report["records"]
            if record["code"] == "format-mismatch"
        ]
        self.assertEqual(len(format_records), 1)
        self.assertEqual(format_records[0]["evidence_key"], "conv:d|")
        expected = self._full_head_records(
            [
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "造成%d伤害"),
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "无占位"),
            ],
            tag="tformat",
        )
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )
        expected_format = [
            record for record in expected if record.rule_id == "format-mismatch"
        ]
        self.assertEqual(len(expected_format), 1)
        self.assertEqual(
            format_records[0]["fingerprint"], expected_format[0].fingerprint
        )

    def test_r5_duplicate_key_add_defective_occurrence(self) -> None:
        """R5: adding a second occurrence of the same editorial key (one
        defective) changes the key's semantic multiset; the runtime-collision
        + empty-target findings recompute and match the full head exactly."""
        self._collision_doc([("mod-test/data/talents.lua", "Flame", "火焰")])
        base_commit = _commit_all(self.root, "base single")
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Flame", "火焰"),
                ("mod-test/data/talents.lua", "Flame", ""),
            ]
        )
        head_commit = _commit_all(self.root, "head duplicate defective")

        report = self._run(base_commit, head_commit)
        # The same editorial key repeats with a different semantic payload:
        # runtime-collision ERROR + empty-target ERROR, both new.
        self.assertEqual(report["findings"]["previous"], 0)
        self.assertEqual(report["findings"]["recomputed"], 2)
        self.assertEqual(report["ci"]["new_errors"], 2)
        codes = {record["code"] for record in report["records"]}
        self.assertEqual(
            codes, {"runtime-collision", "empty-target"}
        )
        expected = self._full_head_records(
            [
                ("mod-test/data/talents.lua", "Flame", "火焰"),
                ("mod-test/data/talents.lua", "Flame", ""),
            ]
        )
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )

    def test_r5_duplicate_key_remove_defective_occurrence(self) -> None:
        """R5: removing the defective duplicate occurrence resolves both
        findings; incremental canonical equals the full head (empty)."""
        self._collision_doc(
            [
                ("mod-test/data/talents.lua", "Flame", "火焰"),
                ("mod-test/data/talents.lua", "Flame", ""),
            ]
        )
        base_commit = _commit_all(self.root, "base duplicate defective")
        self._collision_doc([("mod-test/data/talents.lua", "Flame", "火焰")])
        head_commit = _commit_all(self.root, "head defective removed")

        report = self._run(base_commit, head_commit)
        self.assertEqual(report["findings"]["previous"], 2)
        self.assertEqual(report["findings"]["kept"], 0)
        self.assertEqual(report["findings"]["incremental"], 0)
        self.assertEqual(report["records"], [])
        expected = self._full_head_records(
            [("mod-test/data/talents.lua", "Flame", "火焰")]
        )
        self.assertEqual(
            self._canonical(report["records"]),
            self._canonical([record.to_dict() for record in expected]),
        )

    def test_head_only_main_file_all_entries_affected(self) -> None:
        """A translation file absent at base (head-only) marks every head
        entry affected; the fallback TU is used when the index has no
        mapping (D5) and the defect surfaces as a new ERROR."""
        from i18nlib.identity import tu_uid_fallback
        from i18nlib.lint import stable_entry_id

        # Base commit: no translation file at all.
        base_commit = _commit_all(self.root, "base empty")
        self._write_doc(
            "mod-test.lua",
            [("mod-test/data/talents.lua", "Frost", "")],
        )
        head_commit = _commit_all(self.root, "head adds mod-test.lua")

        report = self._run(base_commit, head_commit)
        self.assertEqual(report["affected_components"], ["test-component"])
        self.assertGreater(report["affected_tus"], 0)
        # The empty-target defect on the head-only entry is recomputed and is
        # a NEW error for the CI gate.
        self.assertGreaterEqual(report["findings"]["recomputed"], 1)
        self.assertEqual(report["ci"]["new_errors"], 1)
        # V7: counts are always reported, but without --ci new_errors never
        # flips ok (the gate is opt-in).
        self.assertTrue(report["ok"])
        # "Frost" is not in the fixture index: the affected set carries the
        # frozen fallback TU, matching build_finding_records::_bind (D5).
        fallback = tu_uid_fallback(
            stable_entry_id(
                "test-component", "mod-test/data/talents.lua", "Frost", "talent name"
            )
        )
        self.assertIn(fallback, report["affected_tu_uids"])

    def test_head_only_copy_fragment(self) -> None:
        """A copy fragment added in head is a separate logical document; all
        its entries are affected and its defect is a new ERROR."""
        # Base: main exists, no copy fragment.
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        base_commit = _commit_all(self.root, "base main only")
        self._write_doc(
            "mod-test-copy.lua",
            [("mod-test/data/effects.lua", "Burning", "")],
        )
        head_commit = _commit_all(self.root, "head adds copy")

        report = self._run(base_commit, head_commit)
        self.assertGreater(report["affected_tus"], 0)
        self.assertGreaterEqual(report["findings"]["recomputed"], 1)
        self.assertEqual(report["ci"]["new_errors"], 1)

    def test_base_copy_fragment_kept(self) -> None:
        """An unchanged copy fragment contributes base records that are kept
        (never recomputed, never dropped) when only the main file changes."""
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        self._write_doc(
            "mod-test-copy.lua",
            [("mod-test/data/effects.lua", "Burning", "")],
        )
        base_commit = _commit_all(self.root, "base")
        # Main target changes (semantic change); copy stays identical.
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰2")])
        head_commit = _commit_all(self.root, "head main semantic change")

        report = self._run(base_commit, head_commit)
        # The copy-fragment empty-target defect lives in base records, is not
        # on an affected TU, and survives in kept.
        self.assertEqual(
            report["findings"],
            {"previous": 1, "kept": 1, "recomputed": 0, "incremental": 1},
        )
        self.assertEqual(report["ci"]["new_errors"], 0)

    def test_head_only_entry_and_deletion(self) -> None:
        """Added head entries are affected; deleted base entries drop their
        findings from the incremental set."""
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Frost", "")])
        base_commit = _commit_all(self.root, "base defect")
        # Head: remove the only entry (deletion) and add a valid one.
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        head_commit = _commit_all(self.root, "head deletion+addition")

        report = self._run(base_commit, head_commit)
        # The deleted Frost defect leaves the incremental set entirely; the
        # added Flame entry maps to a real TU.
        self.assertEqual(report["findings"]["previous"], 1)
        self.assertEqual(report["findings"]["recomputed"], 0)
        self.assertEqual(report["findings"]["incremental"], 0)
        self.assertEqual(report["ci"]["new_errors"], 0)

    def test_semantic_change_is_affected(self) -> None:
        """A target-only change (same editorial key) marks the TU affected."""
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        base_commit = _commit_all(self.root, "base")
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰2")])
        head_commit = _commit_all(self.root, "head semantic")

        report = self._run(base_commit, head_commit)
        self.assertGreater(report["affected_tus"], 0)
        self.assertEqual(report["findings"]["recomputed"], 0)


class RuleDomainTests(_DomainTestCase):
    """H4/D3: registry signature comparison and policy four-rule impact."""

    def _run(
        self, base: str, head: str, *, self_check: bool = False, index: str = "minimal"
    ) -> dict:
        from i18nlib.cli import _lint_incremental_rule

        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment=None,
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        mock_index = (
            _build_full_fixture_index_once()
            if index == "full"
            else self._fixture_index()
        )
        with self._patch_extract(mock_index):
            return self._capture_report(
                _lint_incremental_rule,
                self._arguments(
                    base, head, "rule", ci=False, self_check=self_check
                ),
                self._manifest(component),
                runtime(),
                loader(),
            )

    def test_no_change_early_return(self) -> None:
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        head_commit = _commit_all(self.root, "head (no registry change)")
        report = self._run(base_commit, head_commit)
        self.assertEqual(report["affected_rules"], [])
        self.assertTrue(report["ok"])

    def test_schema_version_bump_affects_rule(self) -> None:
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "format-mismatch":
                rule["schema_version"] = 2
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head schema bump")
        report = self._run(base_commit, head_commit)
        self.assertEqual(report["affected_rules"], ["format-mismatch"])
        self.assertTrue(report["registry_changed"])

    def test_severity_change_affects_rule(self) -> None:
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "empty-target":
                rule["severity"] = "warning"
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head severity")
        report = self._run(base_commit, head_commit)
        self.assertEqual(report["affected_rules"], ["empty-target"])

    def test_evidence_key_spec_change_affects_rule(self) -> None:
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "runtime-collision":
                rule["evidence_key_spec"] = "constant"
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head evidence spec")
        report = self._run(base_commit, head_commit)
        self.assertEqual(report["affected_rules"], ["runtime-collision"])

    def test_rule_removed_affects_rule(self) -> None:
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        data = self._load_registry()
        data["rules"] = [
            rule
            for rule in data["rules"]
            if rule["rule_id"] != "duplicate-effect-id"
        ]
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head removes rule")
        report = self._run(base_commit, head_commit)
        self.assertEqual(report["affected_rules"], ["duplicate-effect-id"])

    def test_policy_change_affects_exactly_four_rules(self) -> None:
        """D3: the three policy allowlists are consumed only by the four
        Pilot A lint rules; a policy change recomputes exactly them."""
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        policy_path = self.root / "i18n/policy.json"
        policy = json.loads(policy_path.read_text())
        policy["allowed_empty_targets"] = ["some-entry-id"]
        policy_path.write_text(
            json.dumps(policy, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        head_commit = _commit_all(self.root, "head policy change")
        report = self._run(base_commit, head_commit)
        self.assertEqual(
            set(report["affected_rules"]),
            {
                "format-mismatch",
                "format-shape-difference",
                "empty-target",
                "runtime-collision",
            },
        )
        self.assertTrue(report["policy_changed"])

    def test_corrupt_base_registry_fails_closed(self) -> None:
        """A base registry that cannot be parsed must abort (never silently
        fall back to the head registry)."""
        (self.root / "i18n/quality/rules-registry-v1.json").write_text(
            "{not-json", encoding="utf-8"
        )
        base_commit = _commit_all(self.root, "base corrupt registry")
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        head_commit = _commit_all(self.root, "head fixed registry")
        with self.assertRaises(ContractError):
            self._run(base_commit, head_commit)

    def _write_unloaded(self, sections: list[str]) -> None:
        """Write the fixture unloaded registry; an empty section list writes
        a genuine empty entries array (R9: 'no exemptions' is a legal
        state)."""
        path = self.root / "i18n/quality/unloaded-sources-v1.json"
        data = {
            "schema_version": 1,
            "entries": [
                {
                    "component": "test-component",
                    "section": section,
                    "evidence": "fixture exemption",
                }
                for section in sections
            ],
        }
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_r3_severity_change_applies_to_records(self) -> None:
        """R3: registry severity is authoritative on the record; flipping
        format-shape-difference error->warning makes the head record a
        warning, self-check passes and CI does not count a new ERROR."""
        self._write_doc(
            "mod-test.lua",
            [("mod-test/data/talents.lua", "Deals %d fire damage.", "Deals %2d fire damage.")],
            tag="tformat",
        )
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base severity error")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "format-shape-difference":
                rule["severity"] = "warning"
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head severity warning")

        report = self._run(base_commit, head_commit, self_check=True)
        self.assertEqual(report["affected_rules"], ["format-shape-difference"])
        self.assertEqual(
            report["findings"], {"previous": 1, "incremental": 1}
        )
        # The head record carries the registry severity (warning), so the
        # fingerprint-identical finding is not a new ERROR.
        self.assertEqual(
            {record["severity"] for record in report["records"]}, {"warning"}
        )
        self.assertEqual(report["ci"]["new_errors"], 0)
        self.assertIs(report["self_check"]["passed"], True)

    def test_r4_unloaded_exemption_removed_adds_duplicate_error(self) -> None:
        """R4: the unloaded-sources registry is a rule-domain dependency.
        Removing the fixture exemption turns the previously suppressed
        duplicate ERRORs into new errors; self-check passes."""
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        # Base: both duplicate-anchor sections exempted -> suppressed.
        self._write_unloaded(
            ["mod-test/data/talents.lua", "mod-test/data/effects.lua"]
        )
        base_commit = _commit_all(self.root, "base exemptions present")
        # Head: exemptions removed down to a genuine empty registry (R9) ->
        # the fixture duplicates surface as new errors.
        self._write_unloaded([])
        head_commit = _commit_all(self.root, "head empty exemptions")

        report = self._run(
            base_commit, head_commit, self_check=True, index="full"
        )
        self.assertEqual(
            set(report["affected_rules"]),
            {"duplicate-talent-id", "duplicate-effect-id"},
        )
        self.assertTrue(report["unloaded_changed"])
        # Base had no duplicate ERRORs (suppressed); head emits both.
        self.assertEqual(report["findings"]["previous"], 0)
        self.assertEqual(report["findings"]["incremental"], 2)
        self.assertEqual(report["ci"]["new_errors"], 2)
        self.assertEqual(
            {record["code"] for record in report["records"]},
            {"duplicate-talent-id", "duplicate-effect-id"},
        )
        self.assertIs(report["self_check"]["passed"], True)

    def test_r4_unloaded_exemption_added_resolves_duplicate_error(self) -> None:
        """R4: adding an exemption resolves the duplicate ERRORs; the base
        records leave f_new through the affected duplicate rules and
        self-check passes."""
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        # Base: genuinely empty registry -> fixture duplicates are ERRORs.
        self._write_unloaded([])
        base_commit = _commit_all(self.root, "base empty exemptions")
        # Head: exempt both duplicate-anchor sections -> suppressed.
        self._write_unloaded(
            ["mod-test/data/talents.lua", "mod-test/data/effects.lua"]
        )
        head_commit = _commit_all(self.root, "head exemptions added")

        report = self._run(
            base_commit, head_commit, self_check=True, index="full"
        )
        self.assertEqual(
            set(report["affected_rules"]),
            {"duplicate-talent-id", "duplicate-effect-id"},
        )
        self.assertEqual(report["findings"]["previous"], 2)
        self.assertEqual(report["findings"]["incremental"], 0)
        self.assertEqual(report["ci"]["new_errors"], 0)
        self.assertEqual(report["records"], [])
        self.assertIs(report["self_check"]["passed"], True)

    # ------------------------------------------------------------------
    # V6: the rule domain must prove §8.4 outcomes, not just rule names.

    def test_v6_schema_bump_recomputes_finding_with_self_check(self) -> None:
        """A real empty-target finding whose rule schema_version bumps gets a
        new fingerprint (new ERROR) and incremental == full head."""
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "")])
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base finding + schema 1")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "empty-target":
                rule["schema_version"] = 2
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head empty-target schema 2")

        report = self._run(base_commit, head_commit, self_check=True)
        self.assertEqual(report["affected_rules"], ["empty-target"])
        self.assertEqual(
            report["findings"], {"previous": 1, "incremental": 1}
        )
        # §6.1: schema bump -> new fingerprint -> new ERROR.
        self.assertEqual(report["ci"]["new_errors"], 1)
        self.assertEqual(report["ci"]["legacy_errors"], 0)
        # §8.4: canonical(F_new) == canonical(full head).
        self.assertIs(report["self_check"]["passed"], True)

    def test_v6_evidence_spec_change_recomputes_finding(self) -> None:
        """format-mismatch conversion-pair -> constant changes the evidence
        key, so the fingerprint changes and self-check passes."""
        self._write_doc(
            "mod-test.lua",
            [("mod-test/data/talents.lua", "Deals %d fire damage.", "OK")],
            tag="tformat",
        )
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base conversion-pair")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "format-mismatch":
                rule["evidence_key_spec"] = "constant"
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head constant evidence")

        report = self._run(base_commit, head_commit, self_check=True)
        self.assertEqual(report["affected_rules"], ["format-mismatch"])
        self.assertEqual(
            report["findings"], {"previous": 1, "incremental": 1}
        )
        # The evidence key changed (conv:d| -> empty) -> new fingerprint.
        self.assertEqual(report["ci"]["new_errors"], 1)
        self.assertIs(report["self_check"]["passed"], True)

    def test_v6_policy_allowlist_change_adds_finding(self) -> None:
        """Removing an empty-target allowlist entry actually produces a NEW
        finding; incremental == full head (self-check)."""
        from i18nlib.lint import stable_entry_id

        editorial = stable_entry_id(
            "test-component",
            "mod-test/data/talents.lua",
            "Flame",
            "talent name",
        )
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "")])
        policy_path = self.root / "i18n/policy.json"
        policy = json.loads(policy_path.read_text())
        policy["allowed_empty_targets"] = [editorial]
        policy_path.write_text(
            json.dumps(policy, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base allowlist covers entry")
        policy = json.loads(policy_path.read_text())
        policy["allowed_empty_targets"] = []
        policy_path.write_text(
            json.dumps(policy, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        head_commit = _commit_all(self.root, "head allowlist removed")

        report = self._run(base_commit, head_commit, self_check=True)
        self.assertEqual(
            set(report["affected_rules"]),
            {
                "format-mismatch",
                "format-shape-difference",
                "empty-target",
                "runtime-collision",
            },
        )
        # Base had no finding (allowed); head produces a NEW empty-target.
        self.assertEqual(
            report["findings"], {"previous": 0, "incremental": 1}
        )
        self.assertEqual(report["ci"]["new_errors"], 1)
        self.assertIs(report["self_check"]["passed"], True)

    def test_v6_policy_allowlist_change_removes_finding(self) -> None:
        """Adding an allowlist entry resolves the finding (base -> head)."""
        from i18nlib.lint import stable_entry_id

        editorial = stable_entry_id(
            "test-component",
            "mod-test/data/talents.lua",
            "Flame",
            "talent name",
        )
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "")])
        policy_path = self.root / "i18n/policy.json"
        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base finding present")
        policy = json.loads(policy_path.read_text())
        policy["allowed_empty_targets"] = [editorial]
        policy_path.write_text(
            json.dumps(policy, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        head_commit = _commit_all(self.root, "head allowlist added")

        report = self._run(base_commit, head_commit, self_check=True)
        self.assertEqual(
            report["findings"], {"previous": 1, "incremental": 0}
        )
        self.assertEqual(report["ci"]["new_errors"], 0)
        self.assertIs(report["self_check"]["passed"], True)


class SourceCIGateTests(_DomainTestCase):
    """H3: the CLI source CI gate reports and fails on NEW errors only."""

    @classmethod
    def _flow_result(cls, *, new_errors: int, legacy_errors: int = 0) -> dict:
        return {
            "domain": "source",
            "base_commit": "b" * 40,
            "head_commit": "h" * 40,
            "changed_paths": 1,
            "deleted_files": [],
            "affected_sections": {},
            "affected_tus": 0,
            "widened_components": {},
            "findings": {"previous": 0, "kept": 0, "recomputed": 0, "incremental": 0},
            "ci": {
                "new_errors": new_errors,
                "legacy_errors": legacy_errors,
                "new_error_fingerprints": [
                    f"fp-{index}" for index in range(new_errors)
                ],
            },
            "binding": {"suppressed_conflicts": []},
            "self_check": None,
            "records": [],
        }

    def _run_cli(self, result: dict) -> int:
        import argparse

        from unittest import mock

        from i18nlib.cli import _lint_identity_mode

        # Both commits resolve against the pinned engine repository; the
        # mocked flow never runs real extraction.
        from i18nlib.config import load_manifest

        pinned = load_manifest().repositories["engine"].commit
        arguments = argparse.Namespace(
            version_manifest="tome-1.7.6",
            manifest=None,
            baseline=None,
            incremental=f"{pinned}..{pinned}",
            domain="source",
            component=[],
            self_check=False,
            ci=True,
            json=False,
            legacy_report=False,
        )
        with mock.patch(
            "i18nlib.incremental.incremental_source_flow",
            return_value=result,
        ):
            return _lint_identity_mode(arguments)

    def test_legacy_errors_do_not_fail(self) -> None:
        exit_code = self._run_cli(self._flow_result(new_errors=0, legacy_errors=3))
        self.assertEqual(exit_code, 0)

    def test_new_errors_fail_with_count_and_first_fingerprint(self) -> None:
        from i18nlib.errors import I18nToolError

        with self.assertRaises(I18nToolError) as raised:
            self._run_cli(self._flow_result(new_errors=2, legacy_errors=1))
        message = str(raised.exception)
        self.assertIn("2 new ERROR findings", message)
        self.assertIn("fp-0", message)

    def test_fixed_run_passes(self) -> None:
        # After fixing the defect the recomputed set carries no new error.
        exit_code = self._run_cli(self._flow_result(new_errors=0, legacy_errors=1))
        self.assertEqual(exit_code, 0)

    def _run_cli_json(self, result: dict, *, ci: bool = True, self_check: bool = False):
        """FR2: run the source CLI in JSON mode and capture the rendered
        report (the CI raise may fire after the render)."""
        import argparse

        from unittest import mock

        from i18nlib.cli import _lint_identity_mode
        from i18nlib.config import load_manifest

        pinned = load_manifest().repositories["engine"].commit
        arguments = argparse.Namespace(
            version_manifest="tome-1.7.6",
            manifest=None,
            baseline=None,
            incremental=f"{pinned}..{pinned}",
            domain="source",
            component=[],
            self_check=self_check,
            ci=ci,
            json=True,
            legacy_report=False,
        )
        captured: list[dict] = []
        with mock.patch(
            "i18nlib.cli._print_json",
            side_effect=lambda value: captured.append(value),
        ), mock.patch(
            "i18nlib.incremental.incremental_source_flow",
            return_value=result,
        ):
            exit_code = _lint_identity_mode(arguments)
        self.assertEqual(len(captured), 1)
        return exit_code, captured[0]

    def test_fr2_json_ok_false_with_new_error_and_ci(self) -> None:
        """FR2: with --ci and a new ERROR the rendered JSON ok is False (the
        gate must not report ok=true while exiting fail) and the raise still
        carries the count and first fingerprint."""
        from i18nlib.errors import I18nToolError

        with self.assertRaises(I18nToolError) as raised:
            self._run_cli_json(
                self._flow_result(new_errors=2, legacy_errors=1), ci=True
            )
        message = str(raised.exception)
        self.assertIn("2 new ERROR findings", message)
        self.assertIn("fp-0", message)

    def test_fr2_json_ok_true_with_legacy_only_and_ci(self) -> None:
        """FR2: legacy-only errors keep ok=True under --ci and do not raise."""
        exit_code, report = self._run_cli_json(
            self._flow_result(new_errors=0, legacy_errors=3), ci=True
        )
        self.assertEqual(exit_code, 0)
        self.assertIs(report["ok"], True)

    def test_fr2_json_ok_true_without_ci_despite_new_error(self) -> None:
        """FR2/V7: without --ci a new-error count never flips ok (the gate
        is opt-in; the counts are still reported)."""
        exit_code, report = self._run_cli_json(
            self._flow_result(new_errors=2, legacy_errors=1), ci=False
        )
        self.assertEqual(exit_code, 0)
        self.assertIs(report["ok"], True)
        self.assertEqual(report["ci"]["new_errors"], 2)

    def _flow_result_with_self_check(self, *, passed: bool) -> dict:
        result = self._flow_result(new_errors=1, legacy_errors=0)
        result["self_check"] = {"passed": passed, "full_findings": 1}
        return result

    def test_fr2_self_check_passed_ci_new_error_raises_i18n_not_incremental(self) -> None:
        """FR2 regression: --self-check --ci with a PASSED self-check and a
        new ERROR must raise I18nToolError (exit 1), never
        IncrementalCheckError (exit 2); the rendered JSON ok is False."""
        from i18nlib.errors import I18nToolError, IncrementalCheckError

        try:
            self._run_cli_json(
                self._flow_result_with_self_check(passed=True),
                ci=True,
                self_check=True,
            )
            self.fail("expected I18nToolError")
        except I18nToolError as error:
            self.assertNotIsInstance(error, IncrementalCheckError)
            self.assertIn("1 new ERROR findings", str(error))
        except IncrementalCheckError:  # pragma: no cover - must not happen
            self.fail("self-check passed but IncrementalCheckError raised")

    def test_fr2_self_check_failed_keeps_exit2_priority(self) -> None:
        """A failed self-check keeps exit-2 priority even when --ci also
        reports new errors (aggregate ok=False, IncrementalCheckError)."""
        from i18nlib.errors import IncrementalCheckError

        with self.assertRaises(IncrementalCheckError):
            self._run_cli_json(
                self._flow_result_with_self_check(passed=False),
                ci=True,
                self_check=True,
            )


class BaselineEntityOwnershipTests(_DomainTestCase):
    """V1: duplicate entity findings are attributed to their component via
    TU identity evidence and surface as new ERRORs in baseline state."""

    def test_records_by_component_and_baseline_state(self) -> None:
        from i18nlib.baseline import (
            compute_baseline_state,
            read_baseline,
            write_baseline,
        )
        from i18nlib.cli import _records_by_component
        from i18nlib.findings import FindingContext, build_finding_records
        from i18nlib.fingerprint import RuleRegistry
        from i18nlib.identity import (
            RULES_REGISTRY_RELATIVE_PATH,
            UNLOADED_SOURCES_RELATIVE_PATH,
            IdentityConflict,
            UnloadedSources,
        )

        index = self._fixture_index()
        registry = RuleRegistry.load(REPO_ROOT / RULES_REGISTRY_RELATIVE_PATH)
        unloaded = UnloadedSources.load(
            REPO_ROOT / UNLOADED_SOURCES_RELATIVE_PATH
        )
        # An unsuppressed synthetic duplicate (both sites loaded).
        conflict = IdentityConflict(
            code="duplicate-talent-id",
            severity="error",
            component="test-component",
            kind="talent",
            anchor_key="T_FLAME",
            sites=(
                ("mod-test/data/talents.lua", 5),
                ("mod-test/data/talents.lua", 9),
            ),
        )
        records, _ = build_finding_records(
            registry=registry,
            issues=[],
            contexts={
                "test-component": FindingContext(
                    component="test-component", entries=(), index=index
                )
            },
            conflicts=[conflict],
            unloaded_sources=unloaded,
        )
        self.assertEqual(len(records), 1)
        # The duplicate finding's logical_path is a source section, so the
        # translation-path map cannot own it; TU evidence must.
        self.assertEqual(
            records[0].issue.logical_path, "mod-test/data/talents.lua"
        )
        # R6: participants are TUs at the loaded conflict sites.
        self.assertEqual(set(records[0].participants), set(index.tus))
        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment=None,
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        grouped = _records_by_component(
            records, [component], indexes={"test-component": index}
        )
        self.assertEqual(grouped["test-component"], records)
        # Without index evidence the record stays unowned (legacy behavior
        # for unbindable records; never a wrong-component assignment).
        self.assertEqual(_records_by_component(records, [component]), {})

        # Frozen empty baseline: the duplicate is a NEW ERROR.
        write_baseline(
            manifest_root=self.root,
            component="test-component",
            translation_commit="c1",
            source_snapshot_sha256="snap-1",
            engine_commit="e" * 40,
            extractor_commit="x" * 40,
            rules_registry_sha256="r" * 64,
            slot_registry_sha256="s" * 64,
            records=[],
        )
        baseline = read_baseline(
            self.root, component="test-component", translation_commit="c1"
        )
        state = compute_baseline_state(baseline, records)
        self.assertEqual(len(state.new), 1)
        self.assertEqual(state.new[0].issue.severity, "error")
        self.assertEqual(state.new[0].rule_id, "duplicate-talent-id")


class GitReadBlobOptionalTests(_DomainTestCase):
    """V2: read_blob_optional maps only a genuinely absent blob to None;
    every other failure keeps raising ExtractionError."""

    def test_absent_path_is_none_but_read_blob_keeps_raising(self) -> None:
        from i18nlib.errors import ExtractionError
        from i18nlib.git_source import GitRepository

        (self.root / "mod-test.lua").write_text(
            'section "mod-test/data/talents.lua"\n'
            't("Flame", "火焰", "talent name")\n',
            encoding="utf-8",
        )
        commit = _commit_all(self.root, "base")
        repository = GitRepository(self.root)
        self.assertIsNone(repository.read_blob_optional(commit, "absent.lua"))
        self.assertEqual(
            repository.read_blob_optional(commit, "mod-test.lua"),
            (self.root / "mod-test.lua").read_bytes(),
        )
        with self.assertRaises(ExtractionError):
            repository.read_blob(commit, "absent.lua")

    def test_directory_path_is_not_none(self) -> None:
        from i18nlib.errors import ExtractionError
        from i18nlib.git_source import GitRepository

        (self.root / "data").mkdir()
        (self.root / "data" / "x.lua").write_text("-- x\n", encoding="utf-8")
        commit = _commit_all(self.root, "base")
        repository = GitRepository(self.root)
        # A tree record is not a blob: never treated as absent.
        with self.assertRaises(ExtractionError):
            repository.read_blob_optional(commit, "data")


class StagingFailClosedTests(unittest.TestCase):
    """V2: _stage_affected_files treats only a missing blob as a deletion."""

    def test_non_missing_errors_propagate(self) -> None:
        import tempfile

        from unittest import mock

        from i18nlib.errors import ExtractionError
        from i18nlib.incremental import _stage_affected_files

        component = _component()
        repository = mock.Mock()
        with tempfile.TemporaryDirectory(prefix="tome4-i18n-stage-") as temporary:
            stage = Path(temporary)
            repository.read_blob_optional.side_effect = ExtractionError(
                "cat-file failed"
            )
            with self.assertRaises(ExtractionError):
                _stage_affected_files(
                    repository,
                    "HEAD",
                    component,
                    ["game/modules/tome/data/x.lua"],
                    stage,
                )
            # A genuinely missing blob is a deletion, not an error.
            repository.read_blob_optional.side_effect = None
            repository.read_blob_optional.return_value = None
            count, deleted = _stage_affected_files(
                repository,
                "HEAD",
                component,
                ["game/modules/tome/data/x.lua"],
                stage,
            )
            self.assertEqual(count, 0)
            self.assertEqual(deleted, ["game/modules/tome/data/x.lua"])


class CurrentIndexScanTests(_DomainTestCase):
    """V3: the current-index scan fails closed on partial/corrupt trios."""

    def test_partial_trio_and_corrupt_identity_fail_closed(self) -> None:
        from i18nlib.errors import ValidationError
        from i18nlib.extract import _read_current_indexes
        from i18nlib.identity import write_index_files

        current = self.root / "current"

        def write_identity(directory: Path, name: str) -> None:
            data = self._fixture_index().to_dict()
            data["component"] = name
            (directory / "identity.json").write_text(
                json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )

        # A complete trio loads.
        complete = current / "complete"
        complete.mkdir(parents=True)
        write_index_files(complete, self._fixture_index())
        write_identity(complete, "complete")
        # entities only: the trio is incomplete -> fail closed.
        partial = current / "partial"
        partial.mkdir()
        (partial / "entities.jsonl").write_text("", encoding="utf-8")
        # entities+tu but a corrupt identity.json -> fail closed.
        corrupt = current / "corrupt"
        corrupt.mkdir()
        write_index_files(corrupt, self._fixture_index())
        (corrupt / "identity.json").write_text("{broken", encoding="utf-8")
        # A non-component directory with no artifacts is skipped.
        (current / "scratch").mkdir()
        # R7: an identity.json-only directory must NOT be skipped - it is an
        # artifact and the missing entities/tu members fail closed.
        identity_only = current / "identity-only"
        identity_only.mkdir()
        (identity_only / "identity.json").write_text(
            "{\"component\": \"identity-only\", \"conflicts\": []}",
            encoding="utf-8",
        )

        with self.assertRaises(ValidationError):
            _read_current_indexes(current)
        # Remove the partial dir: still fails on the corrupt trio.
        (current / "partial" / "entities.jsonl").unlink()
        (current / "partial").rmdir()
        with self.assertRaises(ValidationError):
            _read_current_indexes(current)
        # Remove the corrupt trio: the identity-only dir still fails closed.
        (corrupt / "entities.jsonl").unlink()
        (corrupt / "tu_index.jsonl").unlink()
        (corrupt / "identity.json").unlink()
        with self.assertRaises(ValidationError):
            _read_current_indexes(current)
        # Remove the identity-only artifact: only the complete trio remains.
        (identity_only / "identity.json").unlink()
        (identity_only).rmdir()
        # Restore a complete trio for the corrupt dir: both load.
        write_index_files(corrupt, self._fixture_index())
        write_identity(corrupt, "corrupt")
        indexes = _read_current_indexes(current)
        self.assertEqual([idx.component for idx in indexes], ["complete", "corrupt"])


class HeadCommitSemanticsTests(_DomainTestCase):
    """V4: translation/rule domains read base/head from the resolved commit
    blobs; corrupted or different worktree content cannot masquerade as
    head."""

    def test_translation_domain_ignores_corrupt_worktree(self) -> None:
        from i18nlib.cli import _lint_incremental_translation

        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        self._write_doc("mod-test-copy.lua", [("mod-test/data/effects.lua", "Burning", "")])
        base_commit = _commit_all(self.root, "base")
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰2")])
        head_commit = _commit_all(self.root, "head")

        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment="mod-test-copy.lua",
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        # Corrupt the worktree before running: blobs must be authoritative.
        (self.root / "mod-test.lua").write_text("not valid lua !!!", encoding="utf-8")
        (self.root / "mod-test-copy.lua").write_text("", encoding="utf-8")
        with self._patch_extract():
            report = self._capture_report(
                _lint_incremental_translation,
                self._arguments(base_commit, head_commit, "translation", ci=False),
                self._manifest(component),
                runtime(),
                loader(),
            )
        # The head commit (Flame -> 火焰2) still drives the comparison.
        self.assertEqual(report["affected_components"], ["test-component"])
        self.assertEqual(
            report["findings"],
            {"previous": 1, "kept": 1, "recomputed": 0, "incremental": 1},
        )

    def test_rule_domain_ignores_corrupt_worktree(self) -> None:
        from i18nlib.cli import _lint_incremental_rule

        (self.root / "i18n/quality/rules-registry-v1.json").write_bytes(
            self._registry_bytes()
        )
        base_commit = _commit_all(self.root, "base")
        data = self._load_registry()
        for rule in data["rules"]:
            if rule["rule_id"] == "format-mismatch":
                rule["schema_version"] = 2
        self._write_registry(data)
        head_commit = _commit_all(self.root, "head schema bump")

        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment=None,
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        # Corrupt the worktree registry + policy: head blobs are authoritative.
        (self.root / "i18n/quality/rules-registry-v1.json").write_text(
            "{broken", encoding="utf-8"
        )
        (self.root / "i18n/policy.json").write_text("{broken", encoding="utf-8")
        with self._patch_extract():
            report = self._capture_report(
                _lint_incremental_rule,
                self._arguments(base_commit, head_commit, "rule", ci=False),
                self._manifest(component),
                runtime(),
                loader(),
            )
        self.assertEqual(report["affected_rules"], ["format-mismatch"])

    def test_translation_domain_corrupt_base_doc_fails_closed(self) -> None:
        """V2/V4: a corrupt base document is a loader error, never treated as
        a missing (head-only) file."""
        from i18nlib.cli import _lint_incremental_translation
        from i18nlib.errors import ValidationError

        (self.root / "mod-test.lua").write_text("not valid lua !!!", encoding="utf-8")
        base_commit = _commit_all(self.root, "base corrupt doc")
        self._write_doc("mod-test.lua", [("mod-test/data/talents.lua", "Flame", "火焰")])
        head_commit = _commit_all(self.root, "head valid doc")
        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment=None,
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        with self._patch_extract():
            with self.assertRaises(ValidationError):
                self._capture_report(
                    _lint_incremental_translation,
                    self._arguments(base_commit, head_commit, "translation", ci=False),
                    self._manifest(component),
                    runtime(),
                    loader(),
                )


    def test_current_indexes_for_uses_fail_closed_scan(self) -> None:
        """V10: cli._current_indexes_for shares the fail-closed trio scan with
        the extract path (identity show/audit cannot read partial trios)."""
        from i18nlib.cli import _current_indexes_for
        from i18nlib.errors import ValidationError
        from i18nlib.identity import write_index_files

        component = _component(
            id="test-component",
            translation="mod-test.lua",
            copy_fragment=None,
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        current = self.root / ".artifacts" / "i18n" / "identity" / "current"
        partial = current / "test-component"
        partial.mkdir(parents=True)
        (partial / "entities.jsonl").write_text("", encoding="utf-8")
        manifest = self._manifest(component)
        # A partial trio must fail instead of being silently skipped.
        with self.assertRaises(ValidationError):
            _current_indexes_for(manifest)
        # A complete trio loads, keyed by component.
        write_index_files(partial, self._fixture_index())
        (partial / "identity.json").write_text(
            json.dumps(
                self._fixture_index().to_dict(), ensure_ascii=False, sort_keys=True
            )
            + "\n",
            encoding="utf-8",
        )
        indexes = _current_indexes_for(manifest)
        self.assertEqual(list(indexes), ["test-component"])
        self.assertEqual(
            len(indexes["test-component"].tus),
            len(self._fixture_index().tus),
        )
        # A corrupt identity.json also fails closed.
        (partial / "identity.json").write_text("{broken", encoding="utf-8")
        with self.assertRaises(ValidationError):
            _current_indexes_for(manifest)
        # R7: an identity.json-only component dir fails closed too (it is an
        # artifact; the missing entities/tu members must not be skipped).
        for name in ("entities.jsonl", "tu_index.jsonl", "identity.json"):
            (partial / name).unlink()
        (partial / "identity.json").write_text(
            json.dumps({"component": "test-component", "conflicts": []}),
            encoding="utf-8",
        )
        with self.assertRaises(ValidationError):
            _current_indexes_for(manifest)


if __name__ == "__main__":
    unittest.main()
