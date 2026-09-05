"""Toolchain tests: quality reports."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
import unittest
from i18nlib.quality import _match_findings, _weighted_kappa, build_report


class QualityMetricsTests(unittest.TestCase):
    """Phase-1 doc section 8: agreement and finding-matching metrics."""

    @staticmethod
    def _risk_flag_metrics(
        items: list[dict[str, object]],
        finding_states: dict[str, str | None],
    ) -> dict[str, object]:
        assessments = [
            {
                "evaluator_id": evaluator_id,
                "evaluator": {
                    "kind": "human",
                    "method_version": "fixture",
                },
                "items": [
                    {
                        "revision_id": item["revision_id"],
                        "context_sufficient": True,
                        "profile_confirmed": item["profile"],
                        "findings": [],
                    }
                    for item in items
                ],
            }
            for evaluator_id in ("reviewer-a", "reviewer-b")
        ]
        adjudication_items = []
        for item in items:
            revision_id = item["revision_id"]
            state = finding_states[revision_id]
            resolved_findings = []
            if state is not None:
                resolved_findings.append(
                    {
                        "finding_id": f"finding-{revision_id}",
                        "error_code": "ACC_MISTRANSLATION",
                        "severity": "minor",
                        "state": state,
                    }
                )
            adjudication_items.append(
                {
                    "revision_id": revision_id,
                    "resolved_findings": resolved_findings,
                    "provisional_grade": "Silver",
                    "confidence": "C3",
                    "reuse_scope": "same-tag",
                }
            )
        validation = {
            "sample_id": "fixture-sample",
            "sample": {"items": items},
            "assessments": assessments,
            "adjudication": {"items": adjudication_items},
        }
        taxonomy = {
            "mergeable_codes": [],
            "error_codes": [{"code": "ACC_MISTRANSLATION"}],
        }
        return build_report(validation, taxonomy)["risk_flags"]

    def test_risk_flag_stats_distinguish_coverage_from_confirmed_hits(self) -> None:
        items = [
            {
                "revision_id": "confirmed",
                "bucket": "representative",
                "profile": "mechanics",
                "risk_flags": ["shared", "multiple"],
            },
            {
                "revision_id": "unconfirmed",
                "bucket": "risk-enriched",
                "profile": "mechanics",
                "risk_flags": [
                    "shared",
                    "unconfirmed-only",
                    "multiple",
                    "shared",
                ],
            },
            {
                "revision_id": "confirmed-no-flags",
                "bucket": "representative",
                "profile": "mechanics",
                "risk_flags": [],
            },
            {
                "revision_id": "partially-confirmed",
                "bucket": "risk-enriched",
                "profile": "mechanics",
                "risk_flags": ["multiple", "partial-only"],
            },
        ]
        states = {
            "confirmed": "confirmed",
            "unconfirmed": "rejected",
            "confirmed-no-flags": "confirmed",
            "partially-confirmed": "partially_confirmed",
        }
        risk_flags = self._risk_flag_metrics(items, states)

        self.assertEqual(risk_flags["confirmed_items"], 3)
        self.assertEqual(risk_flags["confirmed_with_any_flag"], 2)
        self.assertEqual(risk_flags["coverage"], 0.6667)
        self.assertEqual(
            risk_flags["per_flag"],
            {
                "shared": {"flagged": 2, "with_confirmed": 1},
                "multiple": {"flagged": 3, "with_confirmed": 2},
                "unconfirmed-only": {"flagged": 1, "with_confirmed": 0},
                "partial-only": {"flagged": 1, "with_confirmed": 1},
            },
        )

    def test_risk_flag_stats_are_safe_without_confirmed_items(self) -> None:
        items = [
            {
                "revision_id": "rejected",
                "bucket": "risk-enriched",
                "profile": "mechanics",
                "risk_flags": ["shared", "rejected-only", "shared"],
            },
            {
                "revision_id": "clean",
                "bucket": "representative",
                "profile": "mechanics",
                "risk_flags": ["shared", "clean-only"],
            },
        ]

        risk_flags = self._risk_flag_metrics(
            items,
            {"rejected": "rejected", "clean": None},
        )

        self.assertEqual(risk_flags["confirmed_items"], 0)
        self.assertEqual(risk_flags["confirmed_with_any_flag"], 0)
        self.assertIsNone(risk_flags["coverage"])
        self.assertEqual(
            risk_flags["per_flag"],
            {
                "shared": {"flagged": 2, "with_confirmed": 0},
                "rejected-only": {"flagged": 1, "with_confirmed": 0},
                "clean-only": {"flagged": 1, "with_confirmed": 0},
            },
        )

    def test_weighted_kappa_perfect_and_random(self) -> None:
        self.assertEqual(_weighted_kappa([0, 1, 2], [0, 1, 2], 5), 1.0)
        kappa = _weighted_kappa([0, 0, 1, 1], [1, 1, 0, 0], 3)
        self.assertIsNotNone(kappa)
        self.assertLess(kappa, 0)
        self.assertIsNone(_weighted_kappa([], [], 5))

    def test_finding_matching_requires_category_compatible_codes(self) -> None:
        left = [
            {
                "finding_id": "A-1",
                "error_code": "ACC_MISTRANSLATION",
                "severity": "major",
                "source_span": "0:5",
                "target_span": "0:5",
                "body": "",
                "evidence_refs": [],
            }
        ]
        right = [
            {
                "finding_id": "B-1",
                "error_code": "ACC_CONDITION",
                "severity": "major",
                "source_span": "0:5",
                "target_span": "0:5",
                "body": "",
                "evidence_refs": [],
            }
        ]
        mergeable = {
            ("ACC_CONDITION", "ACC_MISTRANSLATION"),
        }
        matches = _match_findings(left, right, mergeable)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][1]["finding_id"], "B-1")
        non_mergeable = {("FLU_AWKWARD", "ACC_MISTRANSLATION")}
        self.assertEqual(_match_findings(left, right, non_mergeable), [])

    def test_finding_matching_respects_span_overlap(self) -> None:
        left = [
            {
                "finding_id": "A-1",
                "error_code": "ACC_CONDITION",
                "severity": "major",
                "source_span": "0:5",
                "target_span": "0:5",
                "body": "",
                "evidence_refs": [],
            }
        ]
        right = [
            {
                "finding_id": "B-1",
                "error_code": "ACC_CONDITION",
                "severity": "major",
                "source_span": "10:20",
                "target_span": "10:20",
                "body": "",
                "evidence_refs": [],
            }
        ]
        self.assertEqual(
            _match_findings(
                left, right, {("ACC_CONDITION", "ACC_CONDITION")}
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
