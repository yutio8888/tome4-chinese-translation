"""Identity contract tests (contract/0.1-rc3 §4): frozen hash vectors,
anchor derivation, BC1/BC2, revision semantics (G10), file moves (G12),
rename events (G4) and migration matching (L1/L2)."""

from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.identity import (  # noqa: E402
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
from i18nlib.lint import stable_entry_id  # noqa: E402

from tests.i18n.identity.fixture import (  # noqa: E402
    FIXTURE_TALENTS,
    build_fixture_index,
    make_tree,
    tu_uids,
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
    """G10: source text change keeps the TU UID and changes the Revision."""

    def test_g10_revision_changes_tu_stays(self) -> None:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            ant_tu = next(
                tu
                for tu in index.tus.values()
                if tu.semantic_slot == "entity.name" and "ant" in tu.revisions[-1].source
            )
            old_revision = ant_tu.revisions[-1]
            # Change the entity name only (define_as anchor stays the same).
            files = {
                "mod-test/data/talents.lua": FIXTURE_TALENTS,
                "mod-test/data/effects.lua": """newEffect{
\tname = "BURNING",
\tdesc = _t"Burning",
\ttype = "physical",
\tsubtype = { burning=true },
}
""",
                "mod-test/data/entities.lua": """newEntity{
\tdefine_as = "BASE_NPC_ANT",
\tname = "giant ant",
\ttype = "insect", subtype = "ant",
\tkeywords = { ["insect"] = true },
}
""",
                "mod-test/data/misc.lua": """ActorStats:defineStat("Strength", "str")
""",
            }
            from tests.i18n.identity.fixture import write_fixture_tree

            write_fixture_tree(root, files)
            new_index = build_fixture_index(root)
            new_ant_tu = next(
                tu
                for tu in new_index.tus.values()
                if tu.semantic_slot == "entity.name"
                and tu.anchor_key == "BASE_NPC_ANT"
            )
            self.assertEqual(ant_tu.tu_uid, new_ant_tu.tu_uid)
            self.assertNotEqual(old_revision.revision_uid, new_ant_tu.revisions[-1].revision_uid)
            self.assertEqual(new_ant_tu.revisions[-1].source, "giant ant")
        finally:
            temporary.cleanup()


class FileMoveTests(unittest.TestCase):
    """G12: a source file move changes the section; the L1 identity absorbs it."""

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
