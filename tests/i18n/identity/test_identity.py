"""Identity contract tests (contract/0.1-rc3 §4): frozen hash vectors,
anchor derivation, BC1/BC2, revision semantics (G10), file moves (G12),
rename events (G4) and migration matching (L1/L2)."""

from __future__ import annotations

import json
import shutil
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.findings import FindingContext, build_finding_records  # noqa: E402
from i18nlib.fingerprint import RuleRegistry  # noqa: E402
from i18nlib.identity import (  # noqa: E402
    RULES_REGISTRY_RELATIVE_PATH,
    EnrichmentRecord,
    derive_anchor,
    diff_indexes,
    entity_uid,
    match_migrations,
    revision_uid,
    source_sha256,
    tu_uid_fallback,
    tu_uid_strong,
)
from i18nlib.lint import Issue, stable_entry_id  # noqa: E402
from i18nlib.merge import classify_merge  # noqa: E402
from i18nlib.snapshot import read_snapshot  # noqa: E402

from tests.i18n.identity.fixture import (  # noqa: E402
    FIXTURE_EFFECTS,
    FIXTURE_ENTITIES,
    FIXTURE_MISC,
    FIXTURE_TALENTS,
    build_fixture_index,
    loader,
    make_tree,
    tu_uids,
    write_fixture_tree,
)


class FrozenHashVectorTests(unittest.TestCase):
    """The byte-level hash formulas are frozen (contract §4.5, §15.3)."""

    def test_entity_uid_vector(self) -> None:
        self.assertEqual(
            entity_uid("tome", "talent", "T_FLAME"),
            "686381d84e21105a352075f3d327c0ed7fab33c37ef5d53fab5badbdf991e7e0",
        )

    def test_tu_uid_strong_vector(self) -> None:
        entity = entity_uid("tome", "talent", "T_FLAME")
        self.assertEqual(
            tu_uid_strong(entity, "talent.name", "default"),
            "a4fcfb6e57df7adfac8aa985488857d5bef03cc9a94bbb316a500cdefbc5d11d",
        )

    def test_tu_uid_fallback_vector(self) -> None:
        editorial = stable_entry_id("tome", "section", "Flame", None)
        self.assertEqual(
            tu_uid_fallback(editorial),
            "beddfd13679758226ba983ebf378a8d5d9c13ca772cd48c8744356764fd30fbe",
        )

    def test_revision_uid_vector(self) -> None:
        entity = entity_uid("tome", "talent", "T_FLAME")
        tu = tu_uid_strong(entity, "talent.name", "default")
        self.assertEqual(
            revision_uid(tu, source_sha256("Flame")),
            "ce9d9bc5837837921aebc68f2b3022f699e780021db8c7353c2085faa759ad7e",
        )

    def test_domain_separation(self) -> None:
        editorial = stable_entry_id("tome", "s", "x", None)
        self.assertNotEqual(
            tu_uid_fallback(editorial),
            tu_uid_strong(editorial, "slot", "default"),
        )


class AnchorDerivationTests(unittest.TestCase):
    def _record(self, kind: str, hint: dict, confidence: str = "deterministic"):
        return EnrichmentRecord(
            section="s",
            line=1,
            source="x",
            source_tag="tag",
            entity_kind=kind,
            anchor_hint=hint,
            ast_path="p",
            extraction_confidence=confidence,
        )

    def test_talent_short_name(self) -> None:
        anchor = derive_anchor(
            self._record("talent", {"name": "Flame", "short_name": "FLAME"})
        )
        self.assertIsNotNone(anchor)
        assert anchor is not None
        self.assertEqual((anchor.anchor_type, anchor.anchor_key), ("derived_short_name", "T_FLAME"))
        self.assertTrue(anchor.strong)

    def test_talent_name_fallback(self) -> None:
        anchor = derive_anchor(self._record("talent", {"name": "Burning Shock"}))
        assert anchor is not None
        self.assertEqual(anchor.anchor_key, "T_BURNING_SHOCK")

    def test_effect_name_upper(self) -> None:
        anchor = derive_anchor(self._record("effect", {"name": "Burning"}))
        assert anchor is not None
        self.assertEqual((anchor.anchor_type, anchor.anchor_key), ("effect_name", "EFF_BURNING"))

    def test_bc1_non_static_name_no_anchor(self) -> None:
        self.assertIsNone(
            derive_anchor(self._record("talent", {"name": 3, "short_name": None}))
        )
        self.assertIsNone(
            derive_anchor(
                self._record("talent", {"name": "Flame"}, confidence="nondeterministic")
            )
        )

    def test_entity_anchor_precedence(self) -> None:
        hint = {
            "define_as": "BASE_NPC_ANT",
            "base": "OTHER",
            "name": "ant",
            "type": "insect",
            "subtype": "ant",
        }
        anchor = derive_anchor(self._record("entity", hint))
        assert anchor is not None
        self.assertEqual((anchor.anchor_type, anchor.anchor_key, anchor.strong), ("define_as", "BASE_NPC_ANT", True))

    def test_entity_base_fallback_weak(self) -> None:
        anchor = derive_anchor(
            self._record(
                "entity",
                {"define_as": None, "base": "BASE_NPC_ANT", "name": "giant ant",
                 "type": "insect", "subtype": "giant"},
            )
        )
        assert anchor is not None
        self.assertEqual((anchor.anchor_type, anchor.anchor_key), ("base_fallback", "BASE_NPC_ANT"))
        self.assertFalse(anchor.strong)

    def test_entity_composite_weak(self) -> None:
        anchor = derive_anchor(
            self._record(
                "entity",
                {"define_as": None, "base": None, "name": "huge ant",
                 "type": "insect", "subtype": "huge"},
            )
        )
        assert anchor is not None
        self.assertEqual((anchor.anchor_type, anchor.anchor_key), ("composite", "huge ant|insect|huge"))
        self.assertFalse(anchor.strong)

    def test_weak_kinds_and_free(self) -> None:
        self.assertIsNotNone(derive_anchor(self._record("stat", {"stat_short_name": "str"})))
        self.assertIsNotNone(derive_anchor(self._record("achievement", {"name": "A"})))
        self.assertIsNotNone(derive_anchor(self._record("lore", {"category": "c"})))
        self.assertIsNotNone(derive_anchor(self._record("ingredient", {"name": "i"})))
        self.assertIsNone(derive_anchor(self._record("free", {})))


class RevisionSemanticsTests(unittest.TestCase):
    """G10: a talent.info source text change keeps the TU UID and changes
    the Revision (contract §13 G10: "Deals fire damage." →
    "Deals increased fire damage." under a strong talent.info binding)."""

    def test_g10_revision_changes_tu_stays(self) -> None:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            info_tu = next(
                tu
                for tu in index.tus.values()
                if tu.semantic_slot == "talent.info"
                and tu.anchor_key == "T_FLAME"
            )
            self.assertEqual(info_tu.identity_binding, "strong")
            self.assertEqual(info_tu.revisions[-1].source, "Deals %d fire damage.")
            old_revision = info_tu.revisions[-1]
            # Contract scenario: only the talent.info source text changes.
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS.replace(
                    "Deals %d fire damage.", "Deals increased fire damage."
                ),
                "mod-test/data/effects.lua": FIXTURE_EFFECTS,
                "mod-test/data/entities.lua": FIXTURE_ENTITIES,
                "mod-test/data/misc.lua": FIXTURE_MISC,
            }
            from tests.i18n.identity.fixture import write_fixture_tree

            write_fixture_tree(root, files)
            new_index = build_fixture_index(root)
            new_info_tu = next(
                tu
                for tu in new_index.tus.values()
                if tu.semantic_slot == "talent.info"
                and tu.anchor_key == "T_FLAME"
            )
            self.assertEqual(info_tu.tu_uid, new_info_tu.tu_uid)
            self.assertNotEqual(
                old_revision.revision_uid, new_info_tu.revisions[-1].revision_uid
            )
            self.assertEqual(
                new_info_tu.revisions[-1].source, "Deals increased fire damage."
            )
            # Strong slot: no fallback TU may shadow the same occurrence.
            self.assertNotIn(
                info_tu.tu_uid, tu_uids(index, binding="fallback-editorial")
            )
        finally:
            temporary.cleanup()


class TalentInfoSlotTests(unittest.TestCase):
    """Coverage matrix for the talent.info slot (contract-pilot-a-g10):
    strong-deterministic / captured-nondeterministic-fallback /
    not-captured. All three states run the real patched extractor."""

    def _sidecar(self, root: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in (root / "i18n_enrichment.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        ]

    def test_matrix_strong_deterministic_tformat(self) -> None:
        """(template):tformat(args) is captured once as a strong talent.info."""
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            records = self._sidecar(root)
            matches = [
                record
                for record in records
                if record.get("source") == "Deals %d fire damage."
            ]
            # Exactly one record for the occurrence (no strong+fallback dual).
            self.assertEqual(len(matches), 1)
            record = matches[0]
            self.assertEqual(record["ast_path"], "newTalent.info")
            self.assertEqual(record["entity_kind"], "talent")
            self.assertEqual(record["source_tag"], "tformat")
            self.assertEqual(
                record["extraction_confidence"], "deterministic"
            )
            self.assertEqual(record["anchor_hint"]["name"], "Flame")
            info_tu = next(
                tu
                for tu in index.tus.values()
                if tu.semantic_slot == "talent.info"
                and tu.anchor_key == "T_FLAME"
            )
            self.assertEqual(info_tu.identity_binding, "strong")
            self.assertEqual(
                info_tu.tu_uid,
                tu_uid_strong(
                    entity_uid("test-component", "talent", "T_FLAME"),
                    "talent.info",
                    "default",
                ),
            )
            # The locales write keeps the legacy tag: the tDef entry is
            # unchanged (snapshot byte-stability, contract-pilot-a-g10 p1).
            definition = next(
                definition
                for definition in read_snapshot(
                    root / "snapshot.jsonl",
                    expected_component="test-component",
                ).definitions
                if definition.source == "Deals %d fire damage."
            )
            self.assertEqual(definition.source_tag, "tformat")
        finally:
            temporary.cleanup()

    def test_matrix_strong_deterministic_direct_t(self) -> None:
        """info = _t[[...]] is reclassified from the generic _t capture."""
        root, temporary = make_tree(
            {
                "mod-test/data/talents.lua": (
                    "newTalent{\n"
                    '\tname = "Teleport: Angolwen",\n'
                    '\ttype = {"spell/other", 1},\n'
                    "\tinfo = _t[[Allows a mage to teleport to Angolwen.]]\n"
                    "}\n"
                ),
                "mod-test/data/effects.lua": "",
                "mod-test/data/entities.lua": "",
                "mod-test/data/misc.lua": "",
            }
        )
        try:
            index = build_fixture_index(root)
            records = self._sidecar(root)
            matches = [
                record
                for record in records
                if record.get("source") == "Allows a mage to teleport to Angolwen."
            ]
            self.assertEqual(len(matches), 1)
            record = matches[0]
            self.assertEqual(record["ast_path"], "newTalent.info")
            self.assertEqual(record["entity_kind"], "talent")
            # The _t occurrence keeps its original locales tag.
            self.assertEqual(record["source_tag"], "_t")
            info_tu = next(
                tu
                for tu in index.tus.values()
                if tu.semantic_slot == "talent.info"
            )
            self.assertEqual(info_tu.identity_binding, "strong")
            self.assertEqual(info_tu.anchor_key, "T_TELEPORT:_ANGOLWEN")
        finally:
            temporary.cleanup()

    def test_matrix_captured_nondeterministic_fallback(self) -> None:
        """Runtime-computed info keeps its _t literal as a fallback capture."""
        root, temporary = make_tree(
            {
                "mod-test/data/talents.lua": (
                    "newTalent{\n"
                    '\tname = "Beyond the Flesh",\n'
                    '\ttype = {"psionic/other", 1},\n'
                    "\tinfo = function(self, t)\n"
                    "\t\tlocal base = _t[[Allows you to wield a weapon.]]\n"
                    "\t\treturn base\n"
                    "\tend,\n"
                    "}\n"
                ),
                "mod-test/data/effects.lua": "",
                "mod-test/data/entities.lua": "",
                "mod-test/data/misc.lua": "",
            }
        )
        try:
            index = build_fixture_index(root)
            records = self._sidecar(root)
            matches = [
                record
                for record in records
                if record.get("source") == "Allows you to wield a weapon."
            ]
            # Still exactly one record; it stays a generic free _t capture.
            self.assertEqual(len(matches), 1)
            record = matches[0]
            self.assertEqual(record["ast_path"], "_t")
            self.assertEqual(record["entity_kind"], "free")
            self.assertIsNone(record["anchor_hint"])
            tu = next(
                tu
                for tu in index.tus.values()
                if tu.revisions
                and tu.revisions[-1].source == "Allows you to wield a weapon."
            )
            self.assertEqual(tu.identity_binding, "fallback-editorial")
            self.assertEqual(tu.semantic_slot, "UNKNOWN:_t")
            self.assertNotIn(
                tu.tu_uid, tu_uids(index, binding="strong")
            )
        finally:
            temporary.cleanup()

    def test_matrix_not_captured_plain_string(self) -> None:
        """info = "plain string" produces no tDef, no record and no TU."""
        root, temporary = make_tree(
            {
                "mod-test/data/talents.lua": (
                    "newTalent{\n"
                    '\tname = "Psi Pool",\n'
                    '\ttype = {"base/class", 1},\n'
                    '\tinfo = "Allows you to have an energy pool.",\n'
                    "}\n"
                ),
                "mod-test/data/effects.lua": "",
                "mod-test/data/entities.lua": "",
                "mod-test/data/misc.lua": "",
            }
        )
        try:
            index = build_fixture_index(root)
            self.assertNotIn(
                "Allows you to have an energy pool.",
                {
                    definition.source
                    for definition in read_snapshot(
                        root / "snapshot.jsonl",
                        expected_component="test-component",
                    ).definitions
                },
            )
            self.assertNotIn(
                "Allows you to have an energy pool.",
                {
                    record.get("source")
                    for record in self._sidecar(root)
                },
            )
            self.assertNotIn(
                "Allows you to have an energy pool.",
                {
                    tu.revisions[-1].source
                    for tu in index.tus.values()
                    if tu.revisions
                },
            )
        finally:
            temporary.cleanup()



class FileMoveTests(unittest.TestCase):
    """G12: a source file move changes the section; the L1 identity absorbs it."""

    @staticmethod
    def _flame_fingerprints(index, snapshot) -> list[str]:
        """Finding fingerprint for the Flame talent-name entry (empty target)."""
        definition = next(
            definition
            for definition in snapshot.definitions
            if definition.source == "Flame" and definition.source_tag == "talent name"
        )
        entry = {
            "section": definition.section,
            "source": definition.source,
            "source_tag": definition.source_tag,
            "target": "",
            "logical_path": "mod-test.lua",
            "line": definition.origin_line or 1,
        }
        issue = Issue(
            "error",
            "empty-target",
            "empty",
            "mod-test.lua",
            definition.origin_line or 1,
            definition.entry_id,
        )
        registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3] / RULES_REGISTRY_RELATIVE_PATH
        )
        records, _ = build_finding_records(
            registry=registry,
            issues=[issue],
            contexts={
                "test-component": FindingContext(
                    component="test-component",
                    entries=(entry,),
                    index=index,
                )
            },
            conflicts=(),
        )
        return sorted(record.fingerprint for record in records)

    def test_g12_move_section_only(self) -> None:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            flame_tu = next(
                tu
                for tu in index.tus.values()
                if tu.anchor_key == "T_FLAME" and tu.semantic_slot == "talent.name"
            )
            flame_uid = flame_tu.tu_uid
            base_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            base_fingerprints = self._flame_fingerprints(index, base_snapshot)
            base_entity_uid = flame_tu.entity_uid
            base_revision = flame_tu.revisions[-1].revision_uid
            moved = root / "mod-test" / "data" / "talents" / "spells.lua"
            moved.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(root / "mod-test/data/talents.lua", moved)
            new_index = build_fixture_index(root)
            moved_flame = next(
                tu
                for tu in new_index.tus.values()
                if tu.anchor_key == "T_FLAME" and tu.semantic_slot == "talent.name"
            )
            self.assertEqual(flame_uid, moved_flame.tu_uid)
            self.assertIn(
                "mod-test/data/talents/spells.lua", moved_flame.sections
            )
            self.assertNotEqual(flame_tu.sections, moved_flame.sections)
            # Contract §5 L1 / G12: the move keeps Entity UID, TU UID,
            # Revision UID and any related Finding fingerprint stable.
            self.assertEqual(base_entity_uid, moved_flame.entity_uid)
            self.assertEqual(
                base_entity_uid,
                entity_uid("test-component", "talent", "T_FLAME"),
            )
            self.assertEqual(base_revision, moved_flame.revisions[-1].revision_uid)
            moved_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            moved_fingerprints = self._flame_fingerprints(new_index, moved_snapshot)
            self.assertEqual(base_fingerprints, moved_fingerprints)
            self.assertTrue(base_fingerprints)
        finally:
            temporary.cleanup()


class RenameEventTests(unittest.TestCase):
    """G4/G4b: English renames produce rename_candidate events."""

    def test_g4_rename_candidate(self) -> None:
        root, temporary = make_tree()
        try:
            base = build_fixture_index(root)
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS.replace(
                    'name = "Burning Shock",\n\tshort_name = "BURNING_SHOCK",',
                    'name = "Burning Stun",\n\tshort_name = "BURNING_STUN",',
                ),
                "mod-test/data/effects.lua": """newEffect{
\tname = "BURNING",
\tdesc = _t"Burning",
\ttype = "physical",
\tsubtype = { burning=true },
}
""",
                "mod-test/data/entities.lua": """newEntity{
\tdefine_as = "BASE_NPC_ANT",
\tname = "ant",
\ttype = "insect", subtype = "ant",
}
""",
                "mod-test/data/misc.lua": "",
            }
            from tests.i18n.identity.fixture import write_fixture_tree

            write_fixture_tree(root, files)
            new = build_fixture_index(root)
            events = diff_indexes(base=base, new=new)
            renames = [event for event in events if event.kind == "rename_candidate"]
            self.assertEqual(len(renames), 1)
            event = renames[0]
            self.assertEqual(event.old_anchor_key, "T_BURNING_SHOCK")
            self.assertEqual(event.new_anchor_key, "T_BURNING_STUN")
            # ratio("Burning Shock", "Burning Stun") == 0.72 (contract G4)
            self.assertAlmostEqual(event.similarity, 0.72, places=2)
            self.assertGreaterEqual(event.similarity, 0.68)
        finally:
            temporary.cleanup()

    def test_g4b_rename_with_despace(self) -> None:
        root, temporary = make_tree()
        try:
            base = build_fixture_index(root)
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS.replace(
                    'name = "Flame Bolt",\n\tshort_name = "FLAME_BOLT",',
                    'name = "Flamebolt",\n\tshort_name = "FLAMEBOLT",',
                ),
                "mod-test/data/effects.lua": """newEffect{
\tname = "BURNING",
\tdesc = _t"Burning",
\ttype = "physical",
\tsubtype = { burning=true },
}
""",
                "mod-test/data/entities.lua": """newEntity{
\tdefine_as = "BASE_NPC_ANT",
\tname = "ant",
\ttype = "insect", subtype = "ant",
}
""",
                "mod-test/data/misc.lua": "",
            }
            from tests.i18n.identity.fixture import write_fixture_tree

            write_fixture_tree(root, files)
            new = build_fixture_index(root)
            events = diff_indexes(base=base, new=new)
            renames = [event for event in events if event.kind == "rename_candidate"]
            self.assertEqual(len(renames), 1)
            self.assertAlmostEqual(renames[0].similarity, 0.8421, places=3)
        finally:
            temporary.cleanup()

    def _merge_report(
        self,
        *,
        old_name: str,
        old_short: str,
        new_name: str,
        new_short: str,
        old_target: str,
    ) -> dict:
        """Run classify_merge over the rename fixture with indexes (G4/G4b)."""
        root, temporary = make_tree()
        try:
            base = build_fixture_index(root)
            base_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            current = loader().load_bytes(
                (
                    'section "mod-test/data/talents.lua"\n'
                    f't("{old_name}", "{old_target}", "talent name")\n'
                    'section "mod-test/data/misc.lua"\n'
                    't("You hit %s for %d damage.", "OK", "logPlayer")\n'
                ).encode("utf-8"),
                logical_path="fixture.lua",
            )
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS.replace(
                    f'name = "{old_name}",\n\tshort_name = "{old_short}",',
                    f'name = "{new_name}",\n\tshort_name = "{new_short}",',
                ),
                "mod-test/data/effects.lua": FIXTURE_EFFECTS,
                "mod-test/data/entities.lua": FIXTURE_ENTITIES,
                "mod-test/data/misc.lua": FIXTURE_MISC,
            }
            write_fixture_tree(root, files)
            new = build_fixture_index(root)
            new_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            _, report = classify_merge(
                component="test-component",
                current=current,
                base_snapshot=base_snapshot,
                new_snapshot=new_snapshot,
                base_index=base,
                new_index=new,
            )
            return report
        finally:
            temporary.cleanup()

    def test_g4_rename_merge_suggestion_is_not_automatic(self) -> None:
        """G4 merge output: L2 rename suggestion carries automatic=False."""
        report = self._merge_report(
            old_name="Burning Shock",
            old_short="BURNING_SHOCK",
            new_name="Burning Stun",
            new_short="BURNING_STUN",
            old_target="燃烧冲击",
        )
        renames = [
            event
            for event in report["identity"]["identity_events"]
            if event["kind"] == "rename_candidate"
        ]
        self.assertEqual(len(renames), 1)
        self.assertEqual(renames[0]["old_anchor_key"], "T_BURNING_SHOCK")
        self.assertEqual(renames[0]["new_anchor_key"], "T_BURNING_STUN")
        # ratio("Burning Shock", "Burning Stun") == 0.72 (contract G4).
        self.assertAlmostEqual(renames[0]["similarity"], 0.72, places=2)
        # The L2 identity match is reachable and carries the rename event.
        l2 = [
            match
            for match in report["identity"]["identity_matches"].values()
            if match["source"] == "Burning Stun"
        ]
        self.assertEqual(len(l2), 1)
        self.assertEqual(l2[0]["level"], "L2")
        self.assertEqual(l2[0]["event"]["kind"], "rename_candidate")
        self.assertEqual(l2[0]["event"]["old_anchor_key"], "T_BURNING_SHOCK")
        self.assertEqual(l2[0]["event"]["new_anchor_key"], "T_BURNING_STUN")
        self.assertEqual(l2[0]["similarity"], renames[0]["similarity"])
        self.assertIsNotNone(l2[0]["tu_uid"])
        # The L2 migration suggestion carries the old curated translation and
        # is never auto-applied (contract §5: rename_candidate automatic=False).
        renamed = [
            suggestion
            for suggestion in report["source_changed_suggestions"]
            if suggestion["source"] == "Burning Stun"
        ]
        self.assertEqual(len(renamed), 1)
        self.assertEqual(renamed[0]["match_level"], "L2")
        self.assertEqual(renamed[0]["classification"], "source-changed")
        self.assertIs(renamed[0]["automatic"], False)
        self.assertEqual(renamed[0]["previous_source"], "Burning Shock")
        self.assertEqual(renamed[0]["previous_source_tag"], "talent name")
        self.assertEqual(renamed[0]["previous_target"], "燃烧冲击")
        self.assertIsNotNone(renamed[0]["event"])
        self.assertEqual(renamed[0]["event"]["kind"], "rename_candidate")
        for suggestion in report["source_changed_suggestions"]:
            self.assertIs(suggestion["automatic"], False)
        # The untranslated entry surfaces the same non-automatic suggestion.
        renamed_untranslated = [
            entry
            for entry in report["untranslated"]
            if entry.get("source") == "Burning Stun"
        ]
        self.assertEqual(len(renamed_untranslated), 1)
        self.assertEqual(
            renamed_untranslated[0]["classification"], "source-changed"
        )
        self.assertIs(renamed_untranslated[0]["automatic"], False)
        # The old curated translation is preserved, never silently dropped.
        obsolete = [
            entry for entry in report["obsolete"] if entry["source"] == "Burning Shock"
        ]
        self.assertEqual(len(obsolete), 1)
        self.assertEqual(obsolete[0]["classification"], "obsolete-or-unextracted")

    def test_g4b_rename_merge_suggestion_is_not_automatic(self) -> None:
        """G4b merge output: despace rename also carries L2 + automatic=False."""
        report = self._merge_report(
            old_name="Flame Bolt",
            old_short="FLAME_BOLT",
            new_name="Flamebolt",
            new_short="FLAMEBOLT",
            old_target="火焰箭",
        )
        renames = [
            event
            for event in report["identity"]["identity_events"]
            if event["kind"] == "rename_candidate"
        ]
        self.assertEqual(len(renames), 1)
        self.assertEqual(renames[0]["old_anchor_key"], "T_FLAME_BOLT")
        self.assertEqual(renames[0]["new_anchor_key"], "T_FLAMEBOLT")
        # ratio("Flame Bolt", "Flamebolt") == 0.8421 (contract G4b).
        self.assertAlmostEqual(renames[0]["similarity"], 0.8421, places=3)
        l2 = [
            match
            for match in report["identity"]["identity_matches"].values()
            if match["source"] == "Flamebolt"
        ]
        self.assertEqual(len(l2), 1)
        self.assertEqual(l2[0]["level"], "L2")
        self.assertEqual(l2[0]["event"]["kind"], "rename_candidate")
        self.assertEqual(l2[0]["event"]["old_anchor_key"], "T_FLAME_BOLT")
        self.assertEqual(l2[0]["event"]["new_anchor_key"], "T_FLAMEBOLT")
        self.assertEqual(l2[0]["similarity"], renames[0]["similarity"])
        self.assertIsNotNone(l2[0]["tu_uid"])
        renamed = [
            suggestion
            for suggestion in report["source_changed_suggestions"]
            if suggestion["source"] == "Flamebolt"
        ]
        self.assertEqual(len(renamed), 1)
        self.assertEqual(renamed[0]["match_level"], "L2")
        self.assertEqual(renamed[0]["classification"], "source-changed")
        self.assertIs(renamed[0]["automatic"], False)
        self.assertEqual(renamed[0]["previous_source"], "Flame Bolt")
        self.assertEqual(renamed[0]["previous_source_tag"], "talent name")
        self.assertEqual(renamed[0]["previous_target"], "火焰箭")
        self.assertIsNotNone(renamed[0]["event"])
        self.assertEqual(renamed[0]["event"]["kind"], "rename_candidate")
        for suggestion in report["source_changed_suggestions"]:
            self.assertIs(suggestion["automatic"], False)
        renamed_untranslated = [
            entry
            for entry in report["untranslated"]
            if entry.get("source") == "Flamebolt"
        ]
        self.assertEqual(len(renamed_untranslated), 1)
        self.assertEqual(
            renamed_untranslated[0]["classification"], "source-changed"
        )
        self.assertIs(renamed_untranslated[0]["automatic"], False)
        obsolete = [
            entry for entry in report["obsolete"] if entry["source"] == "Flame Bolt"
        ]
        self.assertEqual(len(obsolete), 1)
        self.assertEqual(obsolete[0]["classification"], "obsolete-or-unextracted")

    def test_rename_unmatched_slot_falls_back_to_legacy_suggestion(self) -> None:
        """F3/R2-001: a rename whose new slot has no old definition must not
        emit an empty L2 match; the group falls back to L5 and still surfaces
        a source-changed suggestion through the legacy heuristic."""
        base_entities = """newEntity{
\tdefine_as = "BASE_NPC_ANT",
\tname = "ant",
\ttype = "insect", subtype = "ant",
}
newEntity{
\tname = "huge ant",
\ttype = "insect",
\tsubtype = "huge",
\tkeywords = { ["colossal"]=true, ["enormous"]=true },
}
"""
        new_entities = """newEntity{
\tdefine_as = "BASE_NPC_ANT2",
\tname = "ant",
\tkeywords = { ["colossal beast"]=true },
}
"""
        root, temporary = make_tree()
        try:
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS,
                "mod-test/data/effects.lua": "",
                "mod-test/data/entities.lua": base_entities,
                "mod-test/data/misc.lua": FIXTURE_MISC,
            }
            write_fixture_tree(root, files)
            base = build_fixture_index(root)
            base_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            current = loader().load_bytes(
                (
                    'section "mod-test/data/entities.lua"\n'
                    't("colossal", "COL", "entity keyword")\n'
                    't("enormous", "ENO", "entity keyword")\n'
                ).encode("utf-8"),
                logical_path="fixture.lua",
            )
            files["mod-test/data/entities.lua"] = new_entities
            write_fixture_tree(root, files)
            new = build_fixture_index(root)
            new_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            # The rename event fires on the shared name slot; the new keyword
            # slot has no definition on the old entity (resolve -> None).
            renames = [
                event
                for event in diff_indexes(base=base, new=new)
                if event.kind == "rename_candidate"
            ]
            self.assertEqual(len(renames), 1)
            self.assertEqual(renames[0].old_anchor_key, "BASE_NPC_ANT")
            self.assertEqual(renames[0].new_anchor_key, "BASE_NPC_ANT2")
            keyword_group = next(
                group
                for group in new_snapshot.groups
                if group.definition.source == "colossal beast"
            )
            matches, _ = match_migrations(
                base_index=base,
                new_index=new,
                untranslated_groups=[keyword_group],
                base_snapshot=base_snapshot,
            )
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0].level, "L5")
            self.assertIsNone(matches[0].previous_definition)
            # The merge report carries the legacy source-changed suggestion
            # (previous_target from the old curated translation), never lost.
            _, report = classify_merge(
                component="test-component",
                current=current,
                base_snapshot=base_snapshot,
                new_snapshot=new_snapshot,
                base_index=base,
                new_index=new,
            )
            self.assertEqual(
                [
                    match["level"]
                    for match in report["identity"]["identity_matches"].values()
                    if match["source"] == "colossal beast"
                ],
                ["L5"],
            )
            suggestion = [
                suggestion
                for suggestion in report["source_changed_suggestions"]
                if suggestion["source"] == "colossal beast"
            ]
            self.assertEqual(len(suggestion), 1)
            self.assertEqual(suggestion[0]["classification"], "source-changed")
            self.assertIs(suggestion[0]["automatic"], False)
            self.assertEqual(suggestion[0]["previous_source"], "colossal")
            self.assertEqual(
                suggestion[0]["previous_source_tag"], "entity keyword"
            )
            self.assertEqual(suggestion[0]["previous_target"], "COL")
        finally:
            temporary.cleanup()

    def test_rename_two_old_entities_to_one_new_never_l2(self) -> None:
        """FR-001: two old entities each uniquely matching the same new
        entity must not emit an L2 match (multi-to-one is ambiguous); the
        group falls back to L5/legacy without carrying an arbitrary old
        translation."""
        base_entities = """newEntity{
\tdefine_as = "BASE_NPC_ANT",
\tkeywords = { ["colossal"]=true },
}
newEntity{
\tdefine_as = "BASE_NPC_ANT3",
\tkeywords = { ["colossal best"]=true },
}
"""
        new_entities = """newEntity{
\tdefine_as = "BASE_NPC_ANT2",
\tkeywords = { ["colossal beast"]=true },
}
"""
        root, temporary = make_tree()
        try:
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS,
                "mod-test/data/effects.lua": "",
                "mod-test/data/entities.lua": base_entities,
                "mod-test/data/misc.lua": FIXTURE_MISC,
            }
            write_fixture_tree(root, files)
            base = build_fixture_index(root)
            base_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            current = loader().load_bytes(
                (
                    'section "mod-test/data/entities.lua"\n'
                    't("colossal", "COL", "entity keyword")\n'
                    't("colossal best", "COLBEST", "entity keyword")\n'
                ).encode("utf-8"),
                logical_path="fixture.lua",
            )
            files["mod-test/data/entities.lua"] = new_entities
            write_fixture_tree(root, files)
            new = build_fixture_index(root)
            new_snapshot = read_snapshot(
                root / "snapshot.jsonl", expected_component="test-component"
            )
            # Both old entities uniquely match the same new entity: two
            # rename_candidate events sharing one new_entity_uid.
            renames = [
                event
                for event in diff_indexes(base=base, new=new)
                if event.kind == "rename_candidate"
            ]
            self.assertEqual(len(renames), 2)
            new_uid = next(
                uid
                for uid, entity in new.entities.items()
                if entity.anchor_key == "BASE_NPC_ANT2"
            )
            self.assertEqual(
                {event.new_entity_uid for event in renames}, {new_uid}
            )
            group = next(
                group
                for group in new_snapshot.groups
                if group.definition.source == "colossal beast"
            )
            matches, _ = match_migrations(
                base_index=base,
                new_index=new,
                untranslated_groups=[group],
                base_snapshot=base_snapshot,
            )
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0].level, "L5")
            self.assertIsNone(matches[0].previous_definition)
            _, report = classify_merge(
                component="test-component",
                current=current,
                base_snapshot=base_snapshot,
                new_snapshot=new_snapshot,
                base_index=base,
                new_index=new,
            )
            self.assertEqual(
                [
                    match["level"]
                    for match in report["identity"]["identity_matches"].values()
                    if match["source"] == "colossal beast"
                ],
                ["L5"],
            )
            # No L2 match anywhere: multi-to-one must not resolve to an
            # arbitrary old translation.
            self.assertEqual(
                [
                    match["source"]
                    for match in report["identity"]["identity_matches"].values()
                    if match["level"] == "L2"
                ],
                [],
            )
            # The legacy heuristic takes over deterministically (best ratio:
            # "colossal best" 0.963 over "colossal" 0.727).
            suggestion = [
                suggestion
                for suggestion in report["source_changed_suggestions"]
                if suggestion["source"] == "colossal beast"
            ]
            self.assertEqual(len(suggestion), 1)
            self.assertIsNone(suggestion[0].get("match_level"))
            self.assertEqual(suggestion[0]["classification"], "source-changed")
            self.assertEqual(suggestion[0]["previous_source"], "colossal best")
            self.assertEqual(suggestion[0]["previous_target"], "COLBEST")
            self.assertIs(suggestion[0]["automatic"], False)
        finally:
            temporary.cleanup()


class MigrationMatcherTests(unittest.TestCase):
    def test_match_migrations_requires_indexes(self) -> None:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            from i18nlib.identity import match_migrations
            from i18nlib.snapshot import read_snapshot

            snapshot = read_snapshot(root / "snapshot.jsonl", expected_component="test-component")
            groups = [group for group in snapshot.groups]
            matches, events = match_migrations(
                base_index=index,
                new_index=index,
                untranslated_groups=groups,
                base_snapshot=snapshot,
            )
            # Every group with a strong TU present on both sides is L1.
            self.assertTrue(any(match.level == "L1" for match in matches))
            self.assertTrue(all(match.level in ("L1", "L3", "L5") for match in matches))
        finally:
            temporary.cleanup()


class CoalescingTests(unittest.TestCase):
    def test_effect_subtypes_coalesce_into_one_tu(self) -> None:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            effect_tus = [
                tu
                for tu in index.tus.values()
                if tu.kind == "effect" and tu.semantic_slot == "effect.subtype"
            ]
            burning = [tu for tu in effect_tus if tu.anchor_key == "EFF_BURNING"]
            self.assertEqual(len(burning), 1)
            self.assertEqual(
                {revision.source for revision in burning[0].revisions},
                {"burning", "fire"},
            )
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()


class UnknownSlotBindingTests(unittest.TestCase):
    """§4.6: an unregistered ast_path resolves to UNKNOWN and must never
    participate in strong binding, even with a strong anchor."""

    def test_unknown_slot_falls_back_to_editorial(self) -> None:
        import json

        from i18nlib.identity import (
            SLOT_REGISTRY_RELATIVE_PATH,
            SlotRegistry,
            build_component_index,
            parse_enrichment_records,
            tu_uid_fallback,
        )
        from i18nlib.lint import stable_entry_id
        from i18nlib.snapshot import read_snapshot

        root, temporary = make_tree()
        try:
            registry = SlotRegistry.load(
                Path(__file__).resolve().parents[3] / SLOT_REGISTRY_RELATIVE_PATH
            )
            snapshot_path = root / "snapshot.jsonl"
            snapshot_path.write_bytes(
                json.dumps(
                    {
                        "component": "test-component",
                        "section": "mod-test/data/talents.lua",
                        "source": "Flame",
                        "source_tag": "talent name",
                        "origin_line": 2,
                        "origin_kind": "extracted",
                        "origin_document": None,
                    },
                    sort_keys=True,
                ).encode("utf-8")
                + b"\n"
            )
            snapshot = read_snapshot(
                snapshot_path, expected_component="test-component"
            )
            # Strong anchor material (talent hint) but an ast_path that is
            # not registered in the slot registry.
            record = {
                "schema_version": 1,
                "section": "mod-test/data/talents.lua",
                "line": 2,
                "source": "Flame",
                "source_tag": "talent name",
                "entity_kind": "talent",
                "anchor_hint": {
                    "name": "Flame",
                    "short_name": "FLAME",
                    "type": ["spell/fire", 1],
                    "def_line": 1,
                },
                "ast_path": "newTalent.not_registered",
                "extraction_confidence": "deterministic",
            }
            index = build_component_index(
                component="test-component",
                snapshot=snapshot,
                enrichment_records=parse_enrichment_records(
                    [record], source_label="test"
                ),
                slot_registry=registry,
            )
            self.assertEqual(index.stats["strong_tus"], 0)
            self.assertEqual(len(index.tus), 1)
            tu = next(iter(index.tus.values()))
            self.assertEqual(tu.identity_binding, "fallback-editorial")
            self.assertTrue(tu.semantic_slot.startswith("UNKNOWN:"))
            self.assertIsNone(tu.entity_uid)
            editorial = stable_entry_id(
                "test-component", "mod-test/data/talents.lua", "Flame", "talent name"
            )
            self.assertEqual(tu.tu_uid, tu_uid_fallback(editorial))
            self.assertEqual(index.stats["entities"], 0)
        finally:
            temporary.cleanup()
