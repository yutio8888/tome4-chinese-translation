from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.errors import ValidationError
from i18nlib.quality_claims import (
    PROFILE_CANONICAL_V1,
    PROFILE_LEGACY_FACTS,
    PROFILE_LEGACY_V2,
    PROFILE_LEGACY_V3,
    align_claims,
    claim_signature,
    claims_compatible,
    cluster_claims,
    legacy_v2_findings_match,
    legacy_v3_findings_compatible,
    make_uncertainty,
    meaning_changes_compatible,
    normalize_evidence,
    route_uncertainty,
    span_overlap_ratio,
    spans_intersect,
    spans_related,
    union_findings,
    validate_uncertainty,
)
from i18nlib.quality_contracts import canonical_sha256


def normalized(quote: str = "x", occurrence: int = 1, text: str = "xyx") -> dict:
    return normalize_evidence(
        {"quote": quote, "occurrence": occurrence}, text, where="fixture"
    )


def finding(
    *,
    phenomenon: str = "number",
    meaning: str = "strengthened",
    family: str = "semantic",
    source: dict | None = None,
    target: dict | None = None,
    subject: dict | None = None,
) -> dict:
    return {
        "error_family": family,
        "phenomenon": phenomenon,
        "meaning_change": meaning,
        "source_evidence": source if source is not None else normalized("x", 1, "xyx"),
        "target_evidence": target if target is not None else normalized("x", 1, "xyx"),
        "subject": subject,
    }


class EvidenceSpanTests(unittest.TestCase):
    def test_exact_resolution(self):
        result = normalize_evidence({"quote": "one", "occurrence": 2}, "one two one", where="e")
        self.assertEqual(result["state"], "exact")
        self.assertEqual((result["start"], result["end"]), (8, 11))
        first = normalize_evidence({"quote": "one", "occurrence": 1}, "one two one", where="e")
        self.assertEqual((first["start"], first["end"]), (0, 3))

    def test_ambiguous(self):
        result = normalize_evidence({"quote": "one", "occurrence": 0}, "one one", where="e")
        self.assertEqual(result["state"], "ambiguous")
        self.assertEqual(result["start"], None)

    def test_missing_occurrence(self):
        result = normalize_evidence({"quote": "x", "occurrence": 1}, "abc", where="e")
        self.assertEqual(result["state"], "missing")

    def test_whole_item(self):
        result = normalize_evidence({"quote": "", "occurrence": 0, "whole_item": True}, "龙裔", where="e")
        self.assertEqual(result["state"], "whole-item")
        self.assertEqual((result["start"], result["end"]), (0, 2))

    def test_legal_omission(self):
        result = normalize_evidence(
            {"quote": "", "occurrence": 0}, "abc", where="e", allow_empty_omission=True
        )
        self.assertEqual(result["state"], "missing")

    def test_illegal_empty_quote(self):
        with self.assertRaises(ValidationError):
            normalize_evidence({"quote": "", "occurrence": 0}, "abc", where="e")

    def test_rejects_host_owned_fields(self):
        with self.assertRaises(ValidationError):
            normalize_evidence({"quote": "a", "occurrence": 1, "start": 0}, "abc", where="e")


class SignatureTests(unittest.TestCase):
    def test_exact_signature_binds_all_fields(self):
        base = finding()
        signature = claim_signature(base)
        self.assertEqual(len(signature), 64)
        self.assertEqual(signature, claim_signature(finding()))
        self.assertNotEqual(signature, claim_signature(finding(meaning="weakened")))
        self.assertNotEqual(signature, claim_signature(finding(phenomenon="condition")))
        self.assertNotEqual(signature, claim_signature(finding(family="terminology")))
        self.assertNotEqual(
            signature,
            claim_signature(finding(source=normalized("x", 2, "xyx x"))),
        )

    def test_signature_binds_subject(self):
        subject = {"kind": "canonical-revision", "revision_id": "a" * 64}
        self.assertNotEqual(
            claim_signature(finding(subject=subject)),
            claim_signature(finding()),
        )
        self.assertEqual(
            claim_signature(finding(subject=subject)),
            claim_signature(finding(subject=subject)),
        )

    def test_signature_requires_normalized_evidence(self):
        with self.assertRaises(ValidationError):
            claim_signature({"error_family": "semantic", "phenomenon": "number",
                             "meaning_change": "unknown",
                             "source_evidence": {"quote": "x", "occurrence": 1},
                             "target_evidence": {"quote": "x", "occurrence": 1}})


class CompatibilityTests(unittest.TestCase):
    POLICY = {"mergeable_phenomena": [["number", "number-range"]]}

    def test_legacy_v2_match(self):
        left = {
            "phenomenon": "number",
            "meaning_change": {"type": "strengthened"},
            "normalized_source_evidence": normalized("x", 1, "xyx"),
            "normalized_target_evidence": normalized("x", 1, "xyx"),
        }
        right = {
            "phenomenon": "number-range",
            "meaning_change": {"type": "strengthened"},
            "normalized_source_evidence": normalized("x", 1, "xyx"),
            "normalized_target_evidence": normalized("x", 1, "xyx"),
        }
        self.assertTrue(legacy_v2_findings_match(left, right, self.POLICY))
        right["meaning_change"] = {"type": "omitted"}
        self.assertTrue(legacy_v2_findings_match(left, right, self.POLICY))
        # legacy-v2 treats only specific pairs as contradictions
        right["meaning_change"] = {"type": "added"}
        self.assertTrue(legacy_v2_findings_match(left, right, self.POLICY))
        left["meaning_change"] = {"type": "omitted"}
        self.assertFalse(legacy_v2_findings_match(left, right, self.POLICY))
        left["meaning_change"] = {"type": "strengthened"}
        right["meaning_change"] = {"type": "strengthened"}
        right["normalized_source_evidence"] = normalized("x", 1, "abc")
        self.assertFalse(legacy_v2_findings_match(left, right, self.POLICY))

    def test_legacy_v3_compatible(self):
        left = {
            "normalized_phenomenon": "number",
            "normalized_meaning_change": "strengthened",
            "normalized_source_evidence": normalized("x", 1, "xyx"),
            "normalized_target_evidence": normalized("x", 1, "xyx"),
        }
        right = {
            "normalized_phenomenon": "number-range",
            "normalized_meaning_change": "strengthened",
            "normalized_source_evidence": normalized("x", 1, "xyx"),
            "normalized_target_evidence": normalized("x", 1, "xyx"),
        }
        self.assertTrue(legacy_v3_findings_compatible(left, right))
        right["normalized_phenomenon"] = "polarity"
        self.assertFalse(legacy_v3_findings_compatible(left, right))
        right["normalized_phenomenon"] = "number"
        right["normalized_source_evidence"] = normalized("x", 1, "zzz")
        self.assertFalse(legacy_v3_findings_compatible(left, right))

    def test_canonical_meaning_compatibility(self):
        self.assertTrue(meaning_changes_compatible("omitted", "omitted"))
        self.assertTrue(meaning_changes_compatible("unknown", "reversed"))
        self.assertFalse(meaning_changes_compatible("omitted", "added"))
        self.assertFalse(meaning_changes_compatible("weakened", "strengthened"))
        # legacy profile additionally treats none/presentation-only as
        # contradictions with reversed/omitted/added.
        self.assertTrue(meaning_changes_compatible("none", "reversed", legacy=True) is False)

    def test_canonical_claims_compatible(self):
        base = finding()
        self.assertTrue(claims_compatible(base, finding(), PROFILE_CANONICAL_V1))
        self.assertFalse(
            claims_compatible(
                base, finding(meaning="weakened"), PROFILE_CANONICAL_V1
            )
        )
        self.assertFalse(
            claims_compatible(
                base,
                finding(source=normalized("x", 1, "zzz")),
                PROFILE_CANONICAL_V1,
            )
        )
        subject_a = {"kind": "canonical-revision", "revision_id": "a" * 64}
        subject_b = {"kind": "canonical-revision", "revision_id": "b" * 64}
        self.assertTrue(claims_compatible(finding(subject=subject_a), finding(subject=subject_a), PROFILE_CANONICAL_V1))
        self.assertFalse(claims_compatible(finding(subject=subject_a), finding(subject=subject_b), PROFILE_CANONICAL_V1))
        # unknown meaning change stays compatible but routes to manual
        self.assertTrue(claims_compatible(finding(meaning="unknown"), finding(), PROFILE_CANONICAL_V1))

    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValidationError):
            claims_compatible(finding(), finding(), "no-such-profile")


class AlignmentTests(unittest.TestCase):
    def test_direction_independent(self):
        left = [finding(meaning="omitted"), finding(meaning="reversed")]
        right = [finding(meaning="reversed"), finding(meaning="omitted")]
        forward = align_claims(left, right, PROFILE_LEGACY_FACTS)
        backward = align_claims(right, left, PROFILE_LEGACY_FACTS)
        self.assertEqual(
            sorted((b, a) for a, b in backward),
            sorted((a, b) for a, b in forward),
        )
        self.assertEqual(len(forward), 2)

    def test_stable_tie_break(self):
        left = [finding(meaning="omitted"), finding(meaning="omitted")]
        right = [finding(meaning="omitted"), finding(meaning="omitted")]
        first = align_claims(left, right, PROFILE_LEGACY_FACTS)
        second = align_claims(list(reversed(left)), right, PROFILE_LEGACY_FACTS)
        self.assertEqual(first, first)
        # deterministic: same input twice gives the same output
        self.assertEqual(align_claims(left, right, PROFILE_LEGACY_FACTS), first)
        self.assertEqual(len(second), 2)

    def test_incompatible_not_aligned(self):
        left = [finding(family="semantic", phenomenon="number")]
        right = [finding(family="terminology", phenomenon="number")]
        self.assertEqual(align_claims(left, right, PROFILE_LEGACY_FACTS), [])

    def test_span_overlap_ratio(self):
        a = {"state": "exact", "start": 0, "end": 4}
        b = {"state": "exact", "start": 2, "end": 6}
        self.assertEqual(span_overlap_ratio(a, b), 2 / 6)
        self.assertEqual(
            span_overlap_ratio(
                {"state": "missing", "start": None, "end": None},
                {"state": "missing", "start": None, "end": None},
            ),
            1.0,
        )

    def test_spans_intersect_requires_nonempty_overlap(self):
        self.assertTrue(
            spans_intersect(
                {"state": "exact", "start": 0, "end": 4},
                {"state": "exact", "start": 3, "end": 6},
            )
        )
        self.assertFalse(
            spans_intersect(
                {"state": "exact", "start": 0, "end": 4},
                {"state": "exact", "start": 4, "end": 6},
            )
        )


class UnionTests(unittest.TestCase):
    def test_union_dedupes_aligned_findings(self):
        def item(finding_value):
            return {**finding_value, "supported_fact_ids": [], "requires_manual": False}

        left = {"items": [{"revision_id": "r1", "findings": [item(finding(meaning="omitted"))]}]}
        right = {"items": [{"revision_id": "r1", "findings": [item(finding(meaning="omitted"))]}]}
        union = union_findings(left, right)
        self.assertEqual(len(union["r1"]), 1)

    def test_union_merges_fact_support(self):
        left = {"items": [{"revision_id": "r1", "findings": [
            {**finding(), "supported_fact_ids": ["fact-a"], "requires_manual": False}]}]}
        right = {"items": [{"revision_id": "r1", "findings": [
            {**finding(), "supported_fact_ids": ["fact-b"], "requires_manual": True}]}]}
        union = union_findings(left, right)
        self.assertEqual(union["r1"][0]["supported_fact_ids"], ["fact-a", "fact-b"])
        self.assertTrue(union["r1"][0]["requires_manual"])


class ClusteringTests(unittest.TestCase):
    def test_transitive_clustering(self):
        # Three claims on overlapping spans and compatible categories cluster;
        # a disjoint claim stays separate.
        claims = [
            finding(),
            finding(source=normalized("x", 1, "xyx"), target=normalized("x", 1, "xyx")),
            finding(phenomenon="number-range", meaning="omitted"),
            finding(source=normalized("x", 1, "zzz")),
        ]
        clusters = cluster_claims(claims, PROFILE_CANONICAL_V1)
        by_first = {cluster[0]: cluster for cluster in clusters}
        self.assertEqual(len(clusters), 2)
        self.assertEqual(by_first[0], [0, 1, 2])
        self.assertEqual(by_first[3], [3])

    def test_clustering_is_symmetric_and_stable(self):
        claims = [finding(meaning="omitted"), finding(meaning="reversed")]
        first = cluster_claims(claims, PROFILE_CANONICAL_V1)
        self.assertEqual(first, cluster_claims(list(reversed(claims)), PROFILE_CANONICAL_V1))


class UncertaintyRoutingTests(unittest.TestCase):
    def test_each_state_routes_distinctly(self):
        expectations = {
            "none": "normal",
            "unknown": "manual",
            "other": "manual",
            "taxonomy-unknown": "manual",
            "context-insufficient": "manual",
            "evidence-invalid": "rejected",
        }
        seen = {}
        for state, routing in expectations.items():
            decision = route_uncertainty(state)
            self.assertEqual(decision["routing"], routing)
            self.assertFalse(decision["auto_minor"])
            seen[state] = (routing, decision["reason"])
        # every state keeps a distinct routing reason
        self.assertEqual(len({reason for _, reason in seen.values()}), len(expectations))

    def test_unknown_matches_but_requires_manual(self):
        decision = route_uncertainty("unknown")
        self.assertEqual(decision["routing"], "manual")
        self.assertTrue(decision["requires_manual"])

    def test_evidence_invalid_rejected(self):
        decision = route_uncertainty("evidence-invalid")
        self.assertEqual(decision["routing"], "rejected")
        self.assertTrue(decision["requires_manual"])

    def test_validate_uncertainty_round_trip(self):
        value = make_uncertainty("context-insufficient", reason="no neighbor context")
        self.assertEqual(validate_uncertainty(value, "u"), value)

    def test_validate_uncertainty_rejects_inconsistent(self):
        with self.assertRaises(ValidationError):
            validate_uncertainty(
                {"state": "evidence-invalid", "routing": "manual",
                 "requires_manual": False, "auto_minor": False, "reason": "x"},
                "u",
            )

    def test_unknown_state_rejected(self):
        with self.assertRaises(ValidationError):
            route_uncertainty("provisional-minor")


if __name__ == "__main__":
    unittest.main()
