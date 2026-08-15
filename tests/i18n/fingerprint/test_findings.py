"""FindingRecord assembly tests: lint Issue -> TU binding -> fingerprint.

Current canonical translations are clean, so these tests inject synthetic
Issues over the mini-tome fixture to exercise the full binding path,
including the duplicate-id prechecks from IdentityConflict.
"""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.findings import FindingContext, build_finding_records  # noqa: E402
from i18nlib.fingerprint import RuleRegistry, finding_fingerprint  # noqa: E402
from i18nlib.identity import (  # noqa: E402
    RULES_REGISTRY_RELATIVE_PATH,
    tu_uid_fallback,
)
from i18nlib.lint import Issue, stable_entry_id  # noqa: E402

from tests.i18n.identity.fixture import (  # noqa: E402
    FIXTURE_EFFECTS,
    FIXTURE_MISC,
    FIXTURE_TALENTS,
    build_fixture_index,
    make_tree,
)

_ROOT = Path(__file__).resolve().parents[3]


class FindingBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root, self.temporary = make_tree()
        self.index = build_fixture_index(self.root)
        self.registry = RuleRegistry.load(_ROOT / RULES_REGISTRY_RELATIVE_PATH)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _context(self, entries) -> FindingContext:
        return FindingContext(
            component="test-component",
            entries=tuple(entries),
            index=self.index,
        )

    def test_strong_binding_uses_entity_identity(self) -> None:
        flame_tu = next(
            tu
            for tu in self.index.tus.values()
            if tu.anchor_key == "T_FLAME" and tu.semantic_slot == "talent.name"
        )
        editorial = stable_entry_id(
            "test-component", "mod-test/data/talents.lua", "Flame", "talent name"
        )
        entry = {
            "section": "mod-test/data/talents.lua",
            "source": "Flame",
            "source_tag": "talent name",
            "target": "火焰",
            "logical_path": "mod-test.lua",
            "line": 1,
        }
        issue = Issue(
            "error", "empty-target", "translation target is empty", "mod-test.lua", 1, editorial
        )
        records, report = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry])},
            conflicts=(),
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].tu_uid, flame_tu.tu_uid)
        self.assertEqual(records[0].evidence_key, "empty")
        self.assertEqual(records[0].participants, (flame_tu.tu_uid,))
        self.assertFalse(report["unregistered_issues"])

    def test_fallback_binding_for_free_strings(self) -> None:
        from i18nlib.identity import tu_uid_fallback

        editorial = stable_entry_id(
            "test-component", "mod-test/data/misc.lua", "physical", "damage type"
        )
        entry = {
            "section": "mod-test/data/misc.lua",
            "source": "physical",
            "source_tag": "damage type",
            "target": "物理",
            "logical_path": "mod-test.lua",
            "line": 2,
        }
        issue = Issue(
            "error", "empty-target", "empty", "mod-test.lua", 2, editorial
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry])},
            conflicts=(),
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].tu_uid, tu_uid_fallback(editorial))

    def test_format_mismatch_evidence_from_entry(self) -> None:
        editorial = stable_entry_id(
            "test-component", "mod-test/data/misc.lua",
            "You hit %s for %d damage.", "logPlayer",
        )
        entry = {
            "section": "mod-test/data/misc.lua",
            "source": "You hit %s for %d damage.",
            "source_tag": "logPlayer",
            "target": "你造成了伤害",
            "logical_path": "mod-test.lua",
            "line": 3,
        }
        issue = Issue(
            "error", "format-mismatch", "format arguments differ", "mod-test.lua", 3, editorial
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry])},
            conflicts=(),
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].evidence_key, "conv:s,d|")
        self.assertEqual(records[0].rule_schema_version, 1)
        self.assertEqual(len(records[0].fingerprint), 64)

    def test_unregistered_code_has_no_finding(self) -> None:
        editorial = stable_entry_id(
            "test-component", "mod-test/data/talents.lua", "Flame", "talent name"
        )
        issue = Issue(
            "warning", "markup-difference", "markup tokens differ",
            "mod-test.lua", 1, editorial,
        )
        records, report = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([])},
            conflicts=(),
        )
        self.assertEqual(records, [])
        self.assertEqual(report["unregistered_issues"].get("markup-difference"), 1)

    def test_duplicate_anchor_precheck_finding(self) -> None:
        files = {
            "mod-test/data/talents.lua": """newTalent{
\tname = "Duplicate",
\tshort_name = "DUP",
\ttype = {"spell/fire", 1},
}
newTalent{
\tname = "Duplicate Two",
\tshort_name = "DUP",
\ttype = {"spell/fire", 1},
}
""",
            "mod-test/data/effects.lua": "",
            "mod-test/data/entities.lua": "",
            "mod-test/data/misc.lua": "",
        }
        from tests.i18n.identity.fixture import write_fixture_tree

        write_fixture_tree(self.root, files)
        index = build_fixture_index(self.root)
        conflicts = [conflict for conflict in index.conflicts if conflict.severity == "error"]
        self.assertEqual(
            {conflict.code for conflict in conflicts}, {"duplicate-talent-id"}
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[],
            contexts={"test-component": self._context([])},
            conflicts=conflicts,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].rule_id, "duplicate-talent-id")
        self.assertEqual(records[0].evidence_key, "dup:T_DUP")
        self.assertGreaterEqual(len(records[0].participants), 1)

    def test_fingerprint_reproducible_across_builds(self) -> None:
        flame_tu = next(
            tu
            for tu in self.index.tus.values()
            if tu.anchor_key == "T_FLAME" and tu.semantic_slot == "talent.name"
        )
        editorial = stable_entry_id(
            "test-component", "mod-test/data/talents.lua", "Flame", "talent name"
        )
        entry = {
            "section": "mod-test/data/talents.lua",
            "source": "Flame",
            "source_tag": "talent name",
            "target": "火焰",
            "logical_path": "mod-test.lua",
            "line": 1,
        }
        issue = Issue("error", "empty-target", "empty", "mod-test.lua", 1, editorial)
        first, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry])},
            conflicts=(),
        )
        second, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry])},
            conflicts=(),
        )
        self.assertEqual(first[0].fingerprint, second[0].fingerprint)


    def test_registry_severity_is_authoritative_for_records(self) -> None:
        """R3: the Rule Registry severity wins for FindingRecords while the
        default lint Issue keeps its own severity (message/path/line/entry_id
        unchanged). format-shape-difference is a lint warning but a registry
        error in Pilot A (§9.2)."""
        rule = self.registry.rules["format-shape-difference"]
        self.assertEqual(rule.severity, "error")
        editorial = stable_entry_id(
            "test-component",
            "mod-test/data/misc.lua",
            "You hit %s for %d damage.",
            "logPlayer",
        )
        entry = {
            "section": "mod-test/data/misc.lua",
            "source": "You hit %s for %d damage.",
            "source_tag": "logPlayer",
            "target": "你命中 %2s 造成 %d 伤害",
            "logical_path": "mod-test.lua",
            "line": 3,
        }
        lint_issue = Issue(
            "warning", "format-shape-difference", "shape differs",
            "mod-test.lua", 3, editorial,
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[lint_issue],
            contexts={"test-component": self._context([entry])},
            conflicts=(),
        )
        self.assertEqual(len(records), 1)
        # The record carries the registry severity; the input lint Issue is
        # untouched (default lint output stays byte-stable).
        self.assertEqual(records[0].issue.severity, "error")
        self.assertEqual(lint_issue.severity, "warning")
        self.assertEqual(records[0].issue.message, "shape differs")
        self.assertEqual(records[0].issue.logical_path, "mod-test.lua")
        self.assertEqual(records[0].issue.line, 3)
        self.assertEqual(records[0].issue.entry_id, editorial)

    def test_r8_evidence_binds_to_the_exact_occurrence(self) -> None:
        """R8 (cycle 3): duplicated editorial ids share entry_lookup; the
        evidence must come from the occurrence the Issue actually points at
        (logical_path + line), never from the first entry in the list.
        Swapping the insertion order and changing the defective line must
        not change the defective conversion evidence/fingerprint."""
        source = "Deals %d fire damage."
        editorial = stable_entry_id(
            "test-component", "mod-test/data/talents.lua", source, "tformat"
        )
        valid = {
            "section": "mod-test/data/talents.lua",
            "source": source,
            "source_tag": "tformat",
            "target": "造成%d伤害",
            "logical_path": "mod-test.lua",
            "line": 3,
        }
        defective = {
            "section": "mod-test/data/talents.lua",
            "source": source,
            "source_tag": "tformat",
            "target": "无占位",
            "logical_path": "mod-test.lua",
            "line": 7,
        }

        def assemble(entries, defective_line):
            issue = Issue(
                "error",
                "format-mismatch",
                "format arguments differ",
                "mod-test.lua",
                defective_line,
                editorial,
            )
            records, _ = build_finding_records(
                registry=self.registry,
                issues=[issue],
                contexts={"test-component": self._context(entries)},
                conflicts=(),
            )
            return records

        first = assemble([valid, defective], 7)
        second = assemble([defective, valid], 7)
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        # Evidence is the defective conversion pair regardless of list order.
        self.assertEqual(first[0].evidence_key, "conv:d|")
        self.assertEqual(second[0].evidence_key, "conv:d|")
        self.assertEqual(first[0].fingerprint, second[0].fingerprint)
        # The line only identifies the occurrence; shifting the defective
        # occurrence's line keeps the evidence/fingerprint stable.
        defective_shifted = dict(defective, line=11)
        shifted = assemble([valid, defective_shifted], 11)
        self.assertEqual(shifted[0].evidence_key, "conv:d|")
        self.assertEqual(shifted[0].fingerprint, first[0].fingerprint)
        # An issue pointing at the valid occurrence binds the valid evidence.
        valid_records = assemble([valid, defective], 3)
        self.assertEqual(valid_records[0].evidence_key, "conv:d|d")
        self.assertNotEqual(valid_records[0].fingerprint, first[0].fingerprint)
        # Ambiguous location (no entry at that line) fails closed: no
        # fabricated evidence, no record.
        ambiguous, report = build_finding_records(
            registry=self.registry,
            issues=[
                Issue(
                    "error",
                    "format-mismatch",
                    "format arguments differ",
                    "mod-test.lua",
                    99,
                    editorial,
                )
            ],
            contexts={"test-component": self._context([valid, defective])},
            conflicts=(),
        )
        self.assertEqual(ambiguous, [])
        self.assertEqual(report["unregistered_issues"].get("format-mismatch"), 1)

    def test_duplicate_conflict_record_severity_from_registry(self) -> None:
        """R3: the conflict-generated duplicate Issue also uses the registry
        severity (not a hardcoded error)."""
        from i18nlib.identity import IdentityConflict

        conflict = IdentityConflict(
            code="duplicate-talent-id",
            severity="error",
            component="test-component",
            kind="talent",
            anchor_key="T_FLAME",
            sites=(
                ("mod-test/data/talents.lua", 1),
                ("mod-test/data/talents.lua", 5),
            ),
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[],
            contexts={"test-component": self._context([])},
            conflicts=[conflict],
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].issue.severity, "error")
        self.assertEqual(records[0].rule_id, "duplicate-talent-id")


def _shared_name_entities(count: int) -> str:
    # Each entity has a distinct define_as strong anchor; they share the
    # ``name`` source string "ant" but live on separate anchor anchors, so
    # §4.7 keeps them as distinct strong TUs that share one editorial id.
    lines = []
    for tag in ("BASE_NPC_ANT", "BASE_NPC_BUG", "BASE_NPC_OMEGA")[:count]:
        lines.append(
            "newEntity{\n\t"
            f"define_as = \"{tag}\",\n\t"
            "name = \"ant\",\n\t"
            "type = \"insect\", subtype = \"ant\",\n}\n"
        )
    return "".join(lines)


class OneToManyParticipantBindingTests(unittest.TestCase):
    """infra-contract-006: one editorial id can back several distinct
    strong TUs (e.g. two newEntity share one (component,section,source,
    source_tag) but distinct define_as anchors -- §4.7 keeps them distinct).
    Every non runtime-key translation_unit rule must bind the *full* TU set
    as participants so §6.1 'participant entities change -> new fingerprint'
    holds. The runtime-key subject stays the collision fallback."""

    def setUp(self) -> None:
        self.root, self.temporary = make_tree()
        self.index = build_fixture_index(self.root)
        self.registry = RuleRegistry.load(_ROOT / RULES_REGISTRY_RELATIVE_PATH)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _context(self, entries, index=None) -> FindingContext:
        return FindingContext(
            component="test-component",
            entries=tuple(entries),
            index=index if index is not None else self.index,
        )

    def _index_with(self, entities_lua: str, root=None):
        from tests.i18n.identity.fixture import write_fixture_tree
        target = root if root is not None else self.root
        write_fixture_tree(
            target,
            {
                "mod-test/data/entities.lua": entities_lua,
                "mod-test/data/talents.lua": FIXTURE_TALENTS,
                "mod-test/data/effects.lua": FIXTURE_EFFECTS,
                "mod-test/data/misc.lua": FIXTURE_MISC,
            },
        )
        return build_fixture_index(target)

    def test_shared_editorial_id_binds_all_participants(self) -> None:
        index = self._index_with(_shared_name_entities(2))
        multi = {
            eid: tuple(sorted(set(tus)))
            for eid, tus in index.editorial_to_tu.items()
            if len(set(tus)) > 1
        }
        self.assertTrue(multi, "fixture must yield a shared editorial id")
        editorial = stable_entry_id(
            "test-component", "mod-test/data/entities.lua", "ant", "entity name"
        )
        self.assertIn(editorial, multi, "ant-name editorial must be a shared one")
        expected = multi[editorial]
        # The two-strong-anchor "ant" name lives at entities.lua line 2,6,10
        # for the two-entity fixture (tab-indented); the "name = \"ant\""
        # occurrences sit at lines 2 and 6.
        entry = {
            "section": next(
                tu.sections[0]
                for tu in index.tus.values()
                if editorial in tu.editorial_ids
            ),
            "source": "ant",
            "source_tag": "entity name",
            "target": "",
            "logical_path": "mod-test.lua",
            "line": 2,
        }
        eid_entry = stable_entry_id(
            "test-component", entry["section"], "ant", "entity name"
        )
        self.assertEqual(set(index.editorial_to_tu.get(eid_entry, ())), set(expected))
        issue = Issue(
            "error", "empty-target", "empty", "mod-test.lua", 2, eid_entry
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry], index=index)},
            conflicts=(),
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].participants, expected)
        self.assertEqual(records[0].tu_uid, expected[0])
        # Fingerprint is reproducible on a second identical build.
        second, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry], index=index)},
            conflicts=(),
        )
        self.assertEqual(second[0].fingerprint, records[0].fingerprint)

    def test_participant_change_emits_new_fingerprint(self) -> None:
        """SS6.1: binding the full sharing TU set is what makes a
        participant-set change visible.

        Adding a third distinct strong TU (BASE_NPC_OMEGA) that shares the
        editorial id sorts AFTER the two-entity subject, so the sorted-first
        subject stays byte-identical across 2 -> 3 while the participant set
        grows. Under the pre-006 binding (participants = (subject,)) the
        singleton fingerprints on both sides are IDENTICAL (subject +
        evidence unchanged) so the change is invisible -- exactly the bug the
        fix removes. Under infra-contract-006 the full-participant
        fingerprints DIFFER, surfacing the change as new/stale.
        """
        editorial = stable_entry_id(
            "test-component", "mod-test/data/entities.lua", "ant", "entity name"
        )
        index_two = self._index_with(_shared_name_entities(2))
        sharing_two = tuple(sorted(set(index_two.editorial_to_tu[editorial])))
        self.assertEqual(len(sharing_two), 2)
        index_three = self._index_with(_shared_name_entities(3))
        sharing_three = tuple(sorted(set(index_three.editorial_to_tu[editorial])))
        self.assertEqual(len(sharing_three), 3)
        # The added OMEGA TU sorts AFTER the two-entity subject, so the
        # sorted-first subject is byte-identical across 2 -> 3.
        self.assertEqual(sharing_two[0], sharing_three[0])

        entry = {
            "section": next(
                tu.sections[0]
                for tu in index_three.tus.values()
                if editorial in tu.editorial_ids
            ),
            "source": "ant",
            "source_tag": "entity name",
            "target": "",
            "logical_path": "mod-test.lua",
            "line": 2,
        }
        issue = Issue("error", "empty-target", "empty", "mod-test.lua", 2, editorial)

        def build(index):
            records, _ = build_finding_records(
                registry=self.registry,
                issues=[issue],
                contexts={"test-component": self._context([entry], index=index)},
                conflicts=(),
            )
            self.assertEqual(len(records), 1)
            return records[0]

        rec_two = build(index_two)
        self.assertEqual(rec_two.participants, sharing_two)
        rec_three = build(index_three)
        self.assertEqual(rec_three.participants, sharing_three)
        # Subject stays stable (the SS6.1 case the fix exists for).
        self.assertEqual(rec_two.tu_uid, rec_three.tu_uid)
        # Pre-006 (participants = (subject,)) would NOT surface this change:
        # the singleton fingerprints are identical, so the ONLY reason the
        # fingerprint changes here is the full-participant binding.
        singleton_two = finding_fingerprint(
            rule_id=rec_two.rule_id,
            rule_schema_version=rec_two.rule_schema_version,
            subject_tu_uid=rec_two.tu_uid,
            participants=(rec_two.tu_uid,),
            evidence_key=rec_two.evidence_key,
        )
        singleton_three = finding_fingerprint(
            rule_id=rec_three.rule_id,
            rule_schema_version=rec_three.rule_schema_version,
            subject_tu_uid=rec_three.tu_uid,
            participants=(rec_three.tu_uid,),
            evidence_key=rec_three.evidence_key,
        )
        self.assertEqual(singleton_two, singleton_three)
        # infra-contract-006: the real (full-participant) fingerprints differ.
        self.assertNotEqual(rec_two.fingerprint, rec_three.fingerprint)

    def test_runtime_key_subject_is_collision_fallback(self) -> None:
        """infra-contract-006: runtime-collision keeps the collision-fallback
        as the subject even when the aggregated participants resolve to real
        sharing TUs. The subject must NOT become sorted(participants)[0]; the
        fallback fingerprint input stays stable."""
        index = self._index_with(_shared_name_entities(2))
        eids = {
            eid for eid, tus in index.editorial_to_tu.items() if len(set(tus)) == 2
        }
        editorial = stable_entry_id(
            "test-component", "mod-test/data/entities.lua", "ant", "entity name"
        )
        self.assertIn(editorial, eids)
        tu = next(t for t in index.tus.values() if editorial in t.editorial_ids)
        source = "ant"
        tag = "entity name"
        collision_id = hashlib.sha256(
            "\0".join(
                ("test-component", source, f"<string>{tag}")
            ).encode("utf-8")
        ).hexdigest()
        entry = {
            "section": tu.sections[0],
            "source": source,
            "source_tag": tag,
            "target": "x",
            "logical_path": "mod-test.lua",
            "line": 2,
        }
        issue = Issue(
            "error", "runtime-collision", "collide", "mod-test.lua", 2, collision_id
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=[issue],
            contexts={"test-component": self._context([entry], index=index)},
            conflicts=(),
        )
        self.assertEqual(len(records), 1)
        fallback = tu_uid_fallback(collision_id)
        self.assertEqual(records[0].tu_uid, fallback)
        # The subject is the fallback collision id, not a member of the real
        # participant TU set (participants are real sharing-TU uids resolved
        # from the entering entries; the subject deliberately diverges).
        self.assertNotEqual(records[0].tu_uid, records[0].participants[0])


if __name__ == "__main__":
    unittest.main()
