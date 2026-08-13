"""H1 consumer-chain tests: identity.json conflict restoration through
read_index_files (with fail-closed schema/component validation), the
unloaded-sources registry loader, and duplicate-id ERROR exemption at the
finding layer (infra-contract-004)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.errors import ValidationError  # noqa: E402
from i18nlib.findings import FindingContext, build_finding_records  # noqa: E402
from i18nlib.fingerprint import RuleRegistry  # noqa: E402
from i18nlib.identity import (  # noqa: E402
    RULES_REGISTRY_RELATIVE_PATH,
    ComponentIndex,
    IdentityConflict,
    TU,
    UnloadedSourceEntry,
    UnloadedSources,
    read_index_files,
    write_index_files,
)
from i18nlib.lint import Issue  # noqa: E402


def _conflict(**overrides) -> IdentityConflict:
    defaults = dict(
        code="duplicate-talent-id",
        severity="error",
        component="tome",
        kind="talent",
        anchor_key="T_DUP",
        sites=(("mod-tome/data/a.lua", 10), ("mod-tome/data/b.lua", 20)),
    )
    defaults.update(overrides)
    return IdentityConflict(**defaults)


class ReadIndexFilesConflictsTests(unittest.TestCase):
    """H1: conflicts are restored strictly from identity.json."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-conflicts-")
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_index(self, index) -> None:
        write_index_files(self.root, index)
        (self.root / "identity.json").write_text(
            json.dumps(index.to_dict(), ensure_ascii=False, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )

    def test_conflicts_round_trip_through_identity_json(self) -> None:
        from i18nlib.identity import TU, tu_uid_fallback

        empty_tu = TU(
            tu_uid=tu_uid_fallback("x" * 64),
            component="tome",
            entity_uid=None,
            kind="free",
            anchor_key=None,
            anchor_type=None,
            semantic_slot="UNKNOWN:_t",
            discriminator="default",
            editorial_ids=(),
            sections=("mod-tome/data/a.lua",),
            identity_binding="fallback-editorial",
            revisions=(),
        )
        index = type(
            "Index",
            (),
            {
                "component": "tome",
                "source_snapshot_sha256": "s" * 64,
                "entities": {},
                "tus": {"t": empty_tu},
                "editorial_to_tu": {},
                "conflicts": (_conflict(),),
                "stats": {"conflicts": 1, "tus": 1},
                "to_dict": lambda self: {
                    "schema_version": 1,
                    "component": self.component,
                    "source_snapshot_sha256": self.source_snapshot_sha256,
                    "entities": [],
                    "tus": [self.tus["t"].to_dict()],
                    "conflicts": [
                        conflict.to_dict() for conflict in self.conflicts
                    ],
                    "stats": dict(self.stats),
                },
            },
        )()
        self._write_index(index)
        restored = read_index_files(
            component="tome",
            entities_path=self.root / "entities.jsonl",
            tu_index_path=self.root / "tu_index.jsonl",
            conflicts_path=self.root / "identity.json",
        )
        self.assertEqual(len(restored.conflicts), 1)
        conflict = restored.conflicts[0]
        self.assertEqual(conflict.code, "duplicate-talent-id")
        self.assertEqual(conflict.anchor_key, "T_DUP")
        self.assertEqual(conflict.sites, (("mod-tome/data/a.lua", 10), ("mod-tome/data/b.lua", 20)))
        # Weak CONTEXT conflicts survive the round trip untouched.
        self.assertEqual(restored.stats["conflicts"], 1)

    def test_conflicts_path_none_keeps_legacy_empty(self) -> None:
        from i18nlib.identity import TU, tu_uid_fallback

        empty_tu = TU(
            tu_uid=tu_uid_fallback("y" * 64),
            component="tome",
            entity_uid=None,
            kind="free",
            anchor_key=None,
            anchor_type=None,
            semantic_slot="UNKNOWN:_t",
            discriminator="default",
            editorial_ids=(),
            sections=("mod-tome/data/a.lua",),
            identity_binding="fallback-editorial",
            revisions=(),
        )
        index = type(
            "Index",
            (),
            {
                "component": "tome",
                "source_snapshot_sha256": "s" * 64,
                "entities": {},
                "tus": {"t": empty_tu},
                "editorial_to_tu": {},
                "conflicts": (_conflict(),),
                "stats": {"conflicts": 1, "tus": 1},
                "to_dict": lambda self: {
                    "schema_version": 1,
                    "component": self.component,
                    "source_snapshot_sha256": self.source_snapshot_sha256,
                    "entities": [],
                    "tus": [self.tus["t"].to_dict()],
                    "conflicts": [
                        conflict.to_dict() for conflict in self.conflicts
                    ],
                    "stats": dict(self.stats),
                },
            },
        )()
        self._write_index(index)
        # Old callers (merge etc.) pass no conflicts_path -> empty conflicts,
        # exactly as before the consumer-chain fix.
        legacy = read_index_files(
            component="tome",
            entities_path=self.root / "entities.jsonl",
            tu_index_path=self.root / "tu_index.jsonl",
        )
        self.assertEqual(legacy.conflicts, ())

    def test_component_mismatch_fails_closed(self) -> None:
        self._write_index(
            type(
                "Index",
                (),
                {
                    "component": "tome",
                    "source_snapshot_sha256": "s" * 64,
                    "entities": {},
                    "tus": {},
                    "editorial_to_tu": {},
                    "conflicts": (),
                    "stats": {"conflicts": 0},
                    "to_dict": lambda self: {
                        "component": self.component,
                        "source_snapshot_sha256": self.source_snapshot_sha256,
                        "entities": [],
                        "tus": [],
                        "conflicts": [],
                        "stats": dict(self.stats),
                    },
                },
            )()
        )
        with self.assertRaises(ValidationError):
            read_index_files(
                component="orcs",
                entities_path=self.root / "entities.jsonl",
                tu_index_path=self.root / "tu_index.jsonl",
                conflicts_path=self.root / "identity.json",
            )

    def test_missing_file_fails_closed(self) -> None:
        with self.assertRaises(ValidationError):
            read_index_files(
                component="tome",
                entities_path=self.root / "entities.jsonl",
                tu_index_path=self.root / "tu_index.jsonl",
                conflicts_path=self.root / "identity.json",
            )

    def test_corrupt_json_fails_closed(self) -> None:
        (self.root / "identity.json").write_text("{not json", encoding="utf-8")
        with self.assertRaises(ValidationError):
            read_index_files(
                component="tome",
                entities_path=self.root / "entities.jsonl",
                tu_index_path=self.root / "tu_index.jsonl",
                conflicts_path=self.root / "identity.json",
            )

    def test_bad_conflict_record_fails_closed(self) -> None:
        (self.root / "identity.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "component": "tome",
                    "conflicts": [
                        {
                            "code": "duplicate-talent-id",
                            "severity": "error",
                            "component": "tome",
                            "kind": "talent",
                            "anchor_key": "T_DUP",
                            "sites": [["mod-tome/data/a.lua", 0]],  # bad line
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValidationError):
            read_index_files(
                component="tome",
                entities_path=self.root / "entities.jsonl",
                tu_index_path=self.root / "tu_index.jsonl",
                conflicts_path=self.root / "identity.json",
            )

    def test_missing_or_wrong_schema_version_fails_closed(self) -> None:
        (self.root / "identity.json").write_text(
            json.dumps({"component": "tome", "conflicts": []}),
            encoding="utf-8",
        )
        with self.assertRaises(ValidationError):
            read_index_files(
                component="tome",
                entities_path=self.root / "entities.jsonl",
                tu_index_path=self.root / "tu_index.jsonl",
                conflicts_path=self.root / "identity.json",
            )
        (self.root / "identity.json").write_text(
            json.dumps(
                {"schema_version": 2, "component": "tome", "conflicts": []}
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValidationError):
            read_index_files(
                component="tome",
                entities_path=self.root / "entities.jsonl",
                tu_index_path=self.root / "tu_index.jsonl",
                conflicts_path=self.root / "identity.json",
            )


class UnloadedSourcesRegistryTests(unittest.TestCase):
    """H1: the registry is schema-validated and fail-closed."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-unloaded-")
        self.root = Path(self.temporary.name)
        self.path = self.root / "unloaded-sources-v1.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write(self, data) -> None:
        self.path.write_text(json.dumps(data) + "\n", encoding="utf-8")

    def test_load_and_sections_for(self) -> None:
        self._write(
            {
                "schema_version": 1,
                "entries": [
                    {
                        "component": "tome",
                        "section": "mod-tome/data/a.lua",
                        "evidence": "commented out load()",
                    },
                    {
                        "component": "orcs",
                        "section": "tome-orcs/data/b.lua",
                        "evidence": "never loaded",
                    },
                ],
            }
        )
        registry = UnloadedSources.load(self.path)
        self.assertEqual(
            registry.sections_for("tome"),
            frozenset({"mod-tome/data/a.lua"}),
        )
        self.assertEqual(
            registry.sections_for("orcs"),
            frozenset({"tome-orcs/data/b.lua"}),
        )
        self.assertEqual(registry.sections_for("cults"), frozenset())

    def test_missing_fails_closed(self) -> None:
        with self.assertRaises(ValidationError):
            UnloadedSources.load(self.path)

    def test_corrupt_json_fails_closed(self) -> None:
        self.path.write_text("{broken", encoding="utf-8")
        with self.assertRaises(ValidationError):
            UnloadedSources.load(self.path)

    def test_bad_schema_fails_closed(self) -> None:
        self._write({"schema_version": 2, "entries": []})
        with self.assertRaises(ValidationError):
            UnloadedSources.load(self.path)

    def test_empty_entries_is_legal(self) -> None:
        """R9 (cycle 3): an empty entries array is a legal 'no exemptions
        right now' state, not a corrupt registry."""
        self._write({"schema_version": 1, "entries": []})
        registry = UnloadedSources.load(self.path)
        self.assertEqual(registry.entries, ())
        self.assertEqual(registry.sections_for("tome"), frozenset())

    def test_missing_entries_key_fails_closed(self) -> None:
        self._write({"schema_version": 1})
        with self.assertRaises(ValidationError):
            UnloadedSources.load(self.path)

    def test_non_array_entries_fails_closed(self) -> None:
        self._write({"schema_version": 1, "entries": {"tome": "x"}})
        with self.assertRaises(ValidationError):
            UnloadedSources.load(self.path)

    def test_duplicate_pair_fails_closed(self) -> None:
        self._write(
            {
                "schema_version": 1,
                "entries": [
                    {"component": "tome", "section": "a.lua", "evidence": "e1"},
                    {"component": "tome", "section": "a.lua", "evidence": "e2"},
                ],
            }
        )
        with self.assertRaises(ValidationError):
            UnloadedSources.load(self.path)

    def test_real_registry_has_two_entries(self) -> None:
        real = Path(__file__).resolve().parents[3] / "i18n/quality/unloaded-sources-v1.json"
        registry = UnloadedSources.load(real)
        self.assertEqual(len(registry.entries), 2)
        self.assertEqual(
            registry.sections_for("tome"),
            frozenset({"mod-tome/data/talents/psionic/mental-discipline.lua"}),
        )
        self.assertEqual(
            registry.sections_for("orcs"),
            frozenset({"tome-orcs/data/talents/celestial/crepescula.lua"}),
        )


class DuplicateConflictExemptionTests(unittest.TestCase):
    """H1: duplicate-id ERROR findings honor the unloaded-sources registry."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3] / RULES_REGISTRY_RELATIVE_PATH
        )

    def _records(self, conflicts, unloaded_sources=None):
        records, report = build_finding_records(
            registry=self.registry,
            issues=[],
            contexts={},
            conflicts=conflicts,
            unloaded_sources=unloaded_sources,
        )
        return records, report

    def test_raw_conflicts_produce_errors_without_registry(self) -> None:
        records, report = self._records([_conflict()])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].rule_id, "duplicate-talent-id")
        self.assertEqual(records[0].evidence_key, "dup:T_DUP")
        self.assertEqual(report["suppressed_conflicts"], [])

    def test_fully_exempted_conflict_is_suppressed(self) -> None:
        registry = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/a.lua",
                    evidence="commented out load()",
                ),
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/b.lua",
                    evidence="never referenced",
                ),
            ),
        )
        records, report = self._records([_conflict()], unloaded_sources=registry)
        self.assertEqual(records, [])
        self.assertEqual(len(report["suppressed_conflicts"]), 1)
        suppressed = report["suppressed_conflicts"][0]
        self.assertEqual(suppressed["code"], "duplicate-talent-id")
        self.assertEqual(suppressed["anchor_key"], "T_DUP")
        self.assertEqual(suppressed["component"], "tome")
        # V5: the hit exemptions are reported with the registry evidence.
        self.assertEqual(
            suppressed["exemptions"],
            [
                {
                    "section": "mod-tome/data/a.lua",
                    "evidence": "commented out load()",
                },
                {
                    "section": "mod-tome/data/b.lua",
                    "evidence": "never referenced",
                },
            ],
        )
        self.assertIn("mod-tome/data/a.lua", suppressed["reason"])
        self.assertIn("mod-tome/data/b.lua", suppressed["reason"])

    def test_suppressed_exemptions_only_hit_sections(self) -> None:
        """A component may list more unloaded sections than this conflict
        touches; only the hit sections (with evidence) are reported."""
        registry = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/a.lua",
                    evidence="commented out load()",
                ),
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/unrelated.lua",
                    evidence="never referenced",
                ),
            ),
        )
        records, report = self._records([_conflict()], unloaded_sources=registry)
        self.assertEqual(records, [])
        suppressed = report["suppressed_conflicts"][0]
        self.assertEqual(
            suppressed["exemptions"],
            [
                {
                    "section": "mod-tome/data/a.lua",
                    "evidence": "commented out load()",
                }
            ],
        )
        self.assertNotIn("unrelated.lua", suppressed["reason"])

    def test_partially_exempted_keeps_error_with_remaining_sites(self) -> None:
        registry = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/a.lua",
                    evidence="unloaded",
                ),
            ),
        )
        conflict = _conflict(
            sites=(
                ("mod-tome/data/a.lua", 10),
                ("mod-tome/data/b.lua", 20),
                ("mod-tome/data/c.lua", 30),
            )
        )
        records, report = self._records([conflict], unloaded_sources=registry)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].rule_id, "duplicate-talent-id")
        # Only the non-exempted sites stay in the finding message.
        self.assertIn("mod-tome/data/b.lua", records[0].issue.message)
        self.assertIn("mod-tome/data/c.lua", records[0].issue.message)
        self.assertNotIn("mod-tome/data/a.lua", records[0].issue.message)
        self.assertEqual(report["suppressed_conflicts"], [])

    def test_partial_exemption_below_two_sites_is_suppressed(self) -> None:
        registry = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/a.lua",
                    evidence="unloaded",
                ),
            ),
        )
        conflict = _conflict(
            sites=(("mod-tome/data/a.lua", 10), ("mod-tome/data/b.lua", 20))
        )
        # Three sites, two exempted -> one remaining -> no ERROR (BC2 needs >= 2).
        conflict = _conflict(
            sites=(
                ("mod-tome/data/a.lua", 10),
                ("mod-tome/data/c.lua", 30),
                ("mod-tome/data/b.lua", 20),
            )
        )
        registry_all = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome", section="mod-tome/data/a.lua", evidence="u"
                ),
                UnloadedSourceEntry(
                    component="tome", section="mod-tome/data/c.lua", evidence="u"
                ),
            ),
        )
        records, report = self._records([conflict], unloaded_sources=registry_all)
        self.assertEqual(records, [])
        self.assertEqual(len(report["suppressed_conflicts"]), 1)

    def test_weak_context_conflicts_never_filtered(self) -> None:
        registry = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/a.lua",
                    evidence="unloaded",
                ),
            ),
        )
        weak = _conflict(
            code="identity_conflict",
            severity="context",
            anchor_key="base_fallback:BASE_X",
        )
        records, report = self._records([weak], unloaded_sources=registry)
        # Weak conflicts never enter the finding pipeline regardless of the
        # registry; the raw conflict itself is not suppressed anywhere.
        self.assertEqual(records, [])
        self.assertEqual(report["suppressed_conflicts"], [])

    def test_unloaded_sources_registry_does_not_change_fingerprint(self) -> None:
        """The exemption is a presence filter; a surviving ERROR keeps the
        frozen fingerprint formula (only sites in the message text, which is
        excluded from the fingerprint)."""
        registry = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="tome",
                    section="mod-tome/data/a.lua",
                    evidence="unloaded",
                ),
            ),
        )
        raw_records, _ = self._records([_conflict()])
        exempted_records, _ = self._records(
            [
                _conflict(
                    sites=(
                        ("mod-tome/data/a.lua", 10),
                        ("mod-tome/data/b.lua", 20),
                        ("mod-tome/data/c.lua", 30),
                    )
                )
            ],
            unloaded_sources=registry,
        )
        self.assertEqual(len(raw_records), 1)
        self.assertEqual(len(exempted_records), 1)
        # Same anchor -> same evidence key -> same fingerprint; the site
        # narrowing only shows up in the (fingerprint-excluded) message.
        self.assertEqual(raw_records[0].fingerprint, exempted_records[0].fingerprint)


class ReadIndexConflictsClosedModelTests(unittest.TestCase):
    """V9: _read_conflicts enforces the closed BC2 model per field."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-closed-")
        self.root = Path(self.temporary.name)
        self.path = self.root / "identity.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _read(self, conflict: dict) -> None:
        # Valid empty entities/tu index files so the conflicts validation is
        # what actually gets exercised (not an early missing-file failure).
        (self.root / "entities.jsonl").write_text("", encoding="utf-8")
        (self.root / "tu_index.jsonl").write_text("", encoding="utf-8")
        self.path.write_text(
            json.dumps(
                {"schema_version": 1, "component": "tome", "conflicts": [conflict]}
            ),
            encoding="utf-8",
        )
        read_index_files(
            component="tome",
            entities_path=self.root / "entities.jsonl",
            tu_index_path=self.root / "tu_index.jsonl",
            conflicts_path=self.path,
        )

    def _valid(self, **overrides) -> dict:
        conflict = {
            "code": "duplicate-talent-id",
            "severity": "error",
            "component": "tome",
            "kind": "talent",
            "anchor_key": "T_DUP",
            "sites": [["mod-tome/data/a.lua", 10], ["mod-tome/data/b.lua", 20]],
        }
        conflict.update(overrides)
        return conflict

    def test_typo_code_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(self._valid(code="duplicate-talent-idd"))

    def test_duplicate_talent_requires_talent_kind(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(self._valid(kind="effect"))

    def test_duplicate_effect_requires_effect_kind(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(
                self._valid(
                    code="duplicate-effect-id",
                    kind="talent",
                    anchor_key="EFF_DUP",
                )
            )

    def test_duplicate_requires_error_severity(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(self._valid(severity="context"))

    def test_identity_conflict_requires_context_severity(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(
                self._valid(
                    code="identity_conflict",
                    severity="error",
                    kind="entity",
                    anchor_key="base_fallback:BASE_X",
                )
            )

    def test_single_site_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(self._valid(sites=[["mod-tome/data/a.lua", 10]]))

    def test_duplicate_sites_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self._read(
                self._valid(
                    sites=[
                        ["mod-tome/data/a.lua", 10],
                        ["mod-tome/data/a.lua", 10],
                    ]
                )
            )

    def test_valid_weak_conflict_passes(self) -> None:
        self._read(
            self._valid(
                code="identity_conflict",
                severity="context",
                kind="entity",
                anchor_key="base_fallback:BASE_X",
                sites=[["mod-tome/data/a.lua", 10], ["mod-tome/data/b.lua", 20]],
            )
        )


class PartialExemptionParticipantTests(unittest.TestCase):
    """R6: a partially exempted duplicate ERROR must only participate in TUs
    that occur at loaded definition sites (an unloaded-only info TU must not
    shape subject/fingerprint)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3] / RULES_REGISTRY_RELATIVE_PATH
        )
        cls.unloaded = UnloadedSources(
            path=Path("unloaded"),
            entries=(
                UnloadedSourceEntry(
                    component="test-component",
                    section="mod-test/data/talents/c.lua",
                    evidence="not loaded",
                ),
            ),
        )

    def _talent(self, name: str, short: str, info: bool) -> str:
        body = (
            "newTalent{\n"
            f'\tname = "{name}",\n'
            f'\tshort_name = "{short}",\n'
            '\ttype = {"spell/fire", 1},\n'
        )
        if info:
            body += (
                "\tinfo = function(self, t) "
                "return ([[Shared info.]]):tformat(1) end,\n"
            )
        return body + "}\n"

    def _records(self, index) -> list:
        conflicts = [
            conflict
            for conflict in index.conflicts
            if conflict.anchor_key == "T_SHARED"
        ]
        self.assertEqual(len(conflicts), 1)
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[],
            contexts={
                "test-component": FindingContext(
                    component="test-component", entries=(), index=index
                )
            },
            conflicts=conflicts,
            unloaded_sources=self.unloaded,
        )
        return records

    def test_partial_exemption_excludes_unloaded_only_tu(self) -> None:
        from tests.i18n.identity.fixture import build_fixture_index, make_tree

        files = {
            "mod-test/data/talents/a.lua": self._talent("Alpha", "SHARED", False),
            "mod-test/data/talents/b.lua": self._talent("Beta", "SHARED", False),
            "mod-test/data/talents/c.lua": self._talent("Gamma", "SHARED", True),
        }
        root, temporary = make_tree(files)
        try:
            index = build_fixture_index(root)
        finally:
            temporary.cleanup()
        # The unloaded-only info TU exists in the full index.
        info_tu = next(
            tu
            for tu in index.tus.values()
            if tu.anchor_key == "T_SHARED" and tu.semantic_slot == "talent.info"
        )
        self.assertEqual(info_tu.sections, ("mod-test/data/talents/c.lua",))
        records = self._records(index)
        # Two loaded sites survive the exemption -> ERROR, without the
        # unloaded-only info TU in participants.
        self.assertEqual(len(records), 1)
        self.assertNotIn(info_tu.tu_uid, records[0].participants)
        # Subject/fingerprint equal the loaded-only assembly (a+b only).
        files_ab = {
            "mod-test/data/talents/a.lua": self._talent("Alpha", "SHARED", False),
            "mod-test/data/talents/b.lua": self._talent("Beta", "SHARED", False),
        }
        root_ab, temporary_ab = make_tree(files_ab)
        try:
            index_ab = build_fixture_index(root_ab)
        finally:
            temporary_ab.cleanup()
        records_ab = self._records(index_ab)
        self.assertEqual(len(records_ab), 1)
        self.assertEqual(records[0].participants, records_ab[0].participants)
        self.assertEqual(records[0].tu_uid, records_ab[0].tu_uid)
        self.assertEqual(records[0].fingerprint, records_ab[0].fingerprint)


class ConflictParticipantScopeTests(unittest.TestCase):
    """FR3: duplicate participants must follow the IdentityConflict scope
    (component, kind, strong anchor): a same-anchor_key TU of another kind or
    a fallback-editorial TU must never participate."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3] / RULES_REGISTRY_RELATIVE_PATH
        )

    def _tu(
        self,
        tu_uid: str,
        kind: str,
        anchor_key: str,
        *,
        binding: str = "strong",
        sections: tuple[str, ...] = ("mod-tome/data/a.lua",),
    ) -> TU:
        return TU(
            tu_uid=tu_uid,
            component="tome",
            entity_uid=None,
            kind=kind,
            anchor_key=anchor_key,
            anchor_type="derived_short_name" if binding == "strong" else None,
            semantic_slot="talent.name" if kind == "talent" else "effect.name",
            discriminator="default",
            editorial_ids=(),
            sections=sections,
            identity_binding=binding,
            revisions=(),
        )

    def _index(self, tus: list[TU]) -> ComponentIndex:
        return ComponentIndex(
            component="tome",
            source_snapshot_sha256="",
            entities={},
            tus={tu.tu_uid: tu for tu in tus},
            editorial_to_tu={},
            conflicts=(),
            stats={},
        )

    def _records(self, index) -> list:
        conflict = IdentityConflict(
            code="duplicate-talent-id",
            severity="error",
            component="tome",
            kind="talent",
            anchor_key="T_DUP",
            sites=(
                ("mod-tome/data/a.lua", 10),
                ("mod-tome/data/b.lua", 20),
            ),
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[],
            contexts={
                "tome": FindingContext(component="tome", entries=(), index=index)
            },
            conflicts=[conflict],
        )
        return records

    def test_kind_and_binding_scope_excludes_noise(self) -> None:
        loaded = ("mod-tome/data/a.lua",)
        talent_a = self._tu("talent-a", "talent", "T_DUP")
        talent_b = self._tu("talent-b", "talent", "T_DUP")
        # Same anchor text but another kind, strong, in the loaded section.
        effect_noise = self._tu("effect-noise", "effect", "T_DUP")
        # Same kind/anchor but fallback-editorial binding.
        fallback_noise = self._tu(
            "fallback-noise", "talent", "T_DUP", binding="fallback-editorial"
        )
        # Same kind/anchor but only in an unloaded section.
        unloaded_noise = self._tu(
            "unloaded-noise", "talent", "T_DUP", sections=("mod-tome/data/c.lua",)
        )
        noisy = self._index(
            [talent_a, talent_b, effect_noise, fallback_noise, unloaded_noise]
        )
        clean = self._index([talent_a, talent_b])
        noisy_records = self._records(noisy)
        clean_records = self._records(clean)
        self.assertEqual(len(noisy_records), 1)
        self.assertEqual(len(clean_records), 1)
        # Only the two strong talent TUs participate.
        self.assertEqual(
            set(noisy_records[0].participants), {"talent-a", "talent-b"}
        )
        # Subject and fingerprint identical to the noise-free index.
        self.assertEqual(noisy_records[0].participants, clean_records[0].participants)
        self.assertEqual(noisy_records[0].tu_uid, clean_records[0].tu_uid)
        self.assertEqual(
            noisy_records[0].fingerprint, clean_records[0].fingerprint
        )
        self.assertEqual(loaded, ("mod-tome/data/a.lua",))


if __name__ == "__main__":
    unittest.main()
