"""FindingRecord assembly tests: lint Issue -> TU binding -> fingerprint.

Current canonical translations are clean, so these tests inject synthetic
Issues over the mini-tome fixture to exercise the full binding path,
including the duplicate-id prechecks from IdentityConflict.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.findings import FindingContext, build_finding_records  # noqa: E402
from i18nlib.fingerprint import RuleRegistry  # noqa: E402
from i18nlib.identity import RULES_REGISTRY_RELATIVE_PATH  # noqa: E402
from i18nlib.lint import Issue, stable_entry_id  # noqa: E402

from tests.i18n.identity.fixture import build_fixture_index, make_tree  # noqa: E402

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


if __name__ == "__main__":
    unittest.main()
