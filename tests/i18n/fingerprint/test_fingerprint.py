"""Finding fingerprint tests (contract/0.1-rc3 §6): G5 stability matrix,
evidence-key normalization (§6.2) and the canonical form (§8.4)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.fingerprint import (  # noqa: E402
    FindingRecord,
    RuleRegistry,
    build_evidence_key,
    canonical_finding_json,
    canonical_findings_form,
    finding_fingerprint,
    finding_sort_key,
)
from i18nlib.lint import Issue  # noqa: E402


def _record(
    *,
    rule_id: str = "format-mismatch",
    schema_version: int = 1,
    tu_uid: str = "TU-A",
    participants: tuple[str, ...] = ("TU-A",),
    evidence_key: str = "conv:d|d",
    issue: Issue | None = None,
    fingerprint: str | None = None,
) -> FindingRecord:
    return FindingRecord(
        issue=issue
        or Issue("error", rule_id, "message", "path.lua", 7, "entry-1"),
        rule_id=rule_id,
        rule_schema_version=schema_version,
        tu_uid=tu_uid,
        participants=participants,
        evidence_key=evidence_key,
        fingerprint=(
            fingerprint
            if fingerprint is not None
            else finding_fingerprint(
                rule_id=rule_id,
                rule_schema_version=schema_version,
                subject_tu_uid=tu_uid,
                participants=participants,
                evidence_key=evidence_key,
            )
        ),
    )


class FingerprintStabilityTests(unittest.TestCase):
    """G5: the six-transformation stability matrix of §6.1."""

    def test_file_move_and_line_drift_stable(self) -> None:
        first = _record(issue=Issue("error", "format-mismatch", "m", "a.lua", 7, "e"))
        second = _record(issue=Issue("error", "format-mismatch", "m", "b.lua", 999, "e"))
        self.assertEqual(first.fingerprint, second.fingerprint)

    def test_unrelated_text_change_stable(self) -> None:
        first = _record(
            issue=Issue("error", "format-mismatch", "message one", "a.lua", 7, "e")
        )
        second = _record(
            issue=Issue("error", "format-mismatch", "message two", "a.lua", 7, "e")
        )
        self.assertEqual(first.fingerprint, second.fingerprint)

    def test_fix_removes_finding(self) -> None:
        broken = _record(evidence_key="conv:d|")
        fixed = _record(evidence_key="conv:d|d")
        self.assertNotEqual(broken.fingerprint, fixed.fingerprint)

    def test_participant_change_new_fingerprint(self) -> None:
        first = _record(participants=("TU-A",))
        second = _record(participants=("TU-B",))
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_rule_schema_bump_new_fingerprint(self) -> None:
        first = _record(schema_version=1)
        second = _record(schema_version=2)
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_rule_id_change_new_fingerprint(self) -> None:
        first = _record(rule_id="format-mismatch")
        second = _record(rule_id="empty-target", evidence_key="empty")
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_excluded_fields_do_not_enter_fingerprint(self) -> None:
        # severity and message must not participate.
        first = _record(
            issue=Issue("error", "format-mismatch", "m", "a.lua", 7, "e")
        )
        second = _record(
            issue=Issue("warning", "format-mismatch", "different", "a.lua", 7, "e")
        )
        self.assertEqual(first.fingerprint, second.fingerprint)


class EvidenceKeyTests(unittest.TestCase):
    def test_conversion_pair(self) -> None:
        self.assertEqual(
            build_evidence_key(
                "conversion-pair",
                entry={"source": "Deals %d fire damage.", "target": "造成%d伤害"},
            ),
            "conv:d|d",
        )

    def test_formatter_tag(self) -> None:
        self.assertEqual(
            build_evidence_key(
                "formatter-tag",
                entry={"source_tag": "tformat", "args_order": [2, 1]},
            ),
            "tag:tformat|args:2,1",
        )

    def test_constant(self) -> None:
        self.assertEqual(build_evidence_key("constant"), "empty")

    def test_anchor_key(self) -> None:
        self.assertEqual(
            build_evidence_key("anchor-key", anchor_key="T_FLAME"), "dup:T_FLAME"
        )

    def test_runtime_key_matches_collision_id_source(self) -> None:
        from i18nlib.lint import stable_entry_id
        import hashlib

        component = "tome"
        source = "text"
        tag = None
        collision_id = hashlib.sha256(
            "\0".join((component, source, "<nil>")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(
            build_evidence_key(
                "runtime-key",
                entry={"source": source, "source_tag": tag},
                component=component,
            ),
            "collide:" + collision_id[:16],
        )


class CanonicalFormTests(unittest.TestCase):
    def test_canonical_order_and_reproducibility(self) -> None:
        records = [
            _record(tu_uid="TU-B"),
            _record(tu_uid="TU-A"),
        ]
        first = canonical_findings_form(records)
        second = canonical_findings_form(records)
        self.assertEqual(first, second)
        text = first.decode("utf-8")
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))

    def test_canonical_field_order(self) -> None:
        record = _record()
        line = canonical_finding_json(record)
        import json

        parsed = json.loads(line)
        expected_prefix = [
            "severity", "code", "message", "logical_path", "line", "entry_id",
            "rule_id", "rule_schema_version", "tu_uid", "participants",
            "evidence_key", "fingerprint",
        ]
        keys = list(parsed)
        self.assertEqual(keys, expected_prefix)

    def test_sort_by_five_tuple(self) -> None:
        a = _record(tu_uid="TU-A", fingerprint="a" * 64)
        b = _record(tu_uid="TU-B", fingerprint="b" * 64)
        form = canonical_findings_form([b, a]).decode("utf-8")
        self.assertLess(form.find("TU-A"), form.find("TU-B"))


class RuleRegistryTests(unittest.TestCase):
    def test_pilot_a_registry_loads(self) -> None:
        registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3]
            / "i18n/quality/rules-registry-v1.json"
        )
        self.assertEqual(
            set(registry.rules),
            {
                "format-mismatch",
                "format-shape-difference",
                "empty-target",
                "runtime-collision",
                "duplicate-talent-id",
                "duplicate-effect-id",
            },
        )
        for rule in registry.rules.values():
            self.assertEqual(rule.trust_class, "A")

    def test_unregistered_rule_fails_closed(self) -> None:
        from i18nlib.errors import ContractError

        registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3]
            / "i18n/quality/rules-registry-v1.json"
        )
        with self.assertRaises(ContractError):
            registry.require("not-a-rule")


if __name__ == "__main__":
    unittest.main()
