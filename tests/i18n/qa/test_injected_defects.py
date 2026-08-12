"""QA gate G6: injected placeholder defects are detected 100% and clean
class-A ERROR rules produce zero false positives over the fixture."""

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
from i18nlib.lint import Issue, lint_documents, load_policy  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402

from tests.i18n.identity.fixture import build_fixture_index, make_tree  # noqa: E402

_ROOT = Path(__file__).resolve().parents[3]


class InjectedDefectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root, self.temporary = make_tree()
        self.index = build_fixture_index(self.root)
        self.registry = RuleRegistry.load(_ROOT / RULES_REGISTRY_RELATIVE_PATH)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _lint_entries(self, entries):
        """Run the real lint_documents over synthetic translations."""
        from i18nlib.config import load_manifest

        manifest = load_manifest()
        policy = load_policy(manifest)
        # Build a minimal document-like object list via lint_documents' inputs:
        # (component, document); we reuse the entries' logical paths.
        class FakeDocument:
            translations = tuple(entries)
            logical_path = "generated:qa/test.lua"

        issues, _ = lint_documents(
            [("test-component", FakeDocument())], policy, require_nonempty=False
        )
        return issues

    def _records(self, issues, entries):
        context = FindingContext(
            component="test-component",
            entries=tuple(entries),
            index=self.index,
        )
        records, _ = build_finding_records(
            registry=self.registry,
            issues=issues,
            contexts={"test-component": context},
            conflicts=(),
        )
        return records

    def test_placeholder_defect_detected(self) -> None:
        """A %d dropped in the target must be a format-mismatch ERROR."""
        entry = {
            "section": "mod-test/data/misc.lua",
            "source": "You hit %s for %d damage.",
            "source_tag": "logPlayer",
            "target": "你造成了伤害",
            "logical_path": "generated:qa/test.lua",
            "line": 1,
        }
        issues = self._lint_entries([entry])
        codes = {issue.code for issue in issues}
        self.assertIn("format-mismatch", codes)
        records = self._records(issues, [entry])
        format_records = [r for r in records if r.rule_id == "format-mismatch"]
        self.assertEqual(len(format_records), 1)
        self.assertEqual(format_records[0].evidence_key, "conv:s,d|")

    def test_clean_entry_no_false_positive(self) -> None:
        entry = {
            "section": "mod-test/data/misc.lua",
            "source": "You hit %s for %d damage.",
            "source_tag": "logPlayer",
            "target": "你对目标造成%d点%s伤害",
            "args_order": [2, 1],
            "logical_path": "generated:qa/test.lua",
            "line": 1,
        }
        issues = self._lint_entries([entry])
        self.assertEqual(
            [issue for issue in issues if issue.severity == "error"], []
        )
        records = self._records(issues, [entry])
        self.assertEqual(
            [r for r in records if r.rule_id in ("format-mismatch",)],
            [],
        )

    def test_empty_target_detected(self) -> None:
        entry = {
            "section": "mod-test/data/talents.lua",
            "source": "Flame",
            "source_tag": "talent name",
            "target": "",
            "logical_path": "generated:qa/test.lua",
            "line": 1,
        }
        issues = self._lint_entries([entry])
        records = self._records(issues, [entry])
        self.assertEqual(
            [record.rule_id for record in records if record.rule_id == "empty-target"],
            ["empty-target"],
        )


if __name__ == "__main__":
    unittest.main()
