from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from i18nlib.errors import AgentError, ValidationError
from i18nlib.config import load_manifest
from i18nlib.quality_v2 import (
    assessment_identity,
    adjudicate_v2,
    build_assessment_v2,
    build_disputes_v2,
    build_evaluator_bundles_v2,
    build_report_v2,
    canonical_sha256,
    derive_severity,
    load_anchors,
    load_impact_rules,
    load_policy_v2,
    match_assessments_v2,
    normalize_evidence,
    validate_assessment_v2,
    validate_sample_v2,
)
from i18nlib.pi_quality import _cache_key_v2, run_pi_quality_evaluator


POLICY = {
    "evaluator_ids": ["reviewer-a", "reviewer-b"],
    "tri_state_values": ["yes", "no", "unknown"],
    "defect_classes": ["semantic", "presentation", "style", "technical"],
    "phenomena": ["number", "number-range", "punctuation", "format", "other"],
    "meaning_change_types": ["omitted", "strengthened", "presentation-only", "none", "unknown"],
    "impact_fact_fields": [
        "is_defect", "is_substantive", "mechanics_context",
        "changes_rule_understanding", "can_change_player_action",
        "required_operation_info_missing", "opposite_or_different_rule",
        "recoverable_from_immediate_context", "technical_gate_confirmed",
        "runtime_broken", "single_item_display_broken",
    ],
    "critical_impact_facts": [
        "is_defect", "is_substantive", "mechanics_context",
        "changes_rule_understanding", "can_change_player_action",
        "required_operation_info_missing", "opposite_or_different_rule",
        "technical_gate_confirmed", "runtime_broken", "single_item_display_broken",
    ],
    "amplification_scopes": ["local", "systemic", "unknown"],
    "anchor_relations": ["meets", "unknown"],
    "reuse_recommendations": ["same-tag", "no-reuse"],
}

RULES = {
    "rules": [
        {"id": "block", "severity": "blocker", "category": "technical-gate", "all": {"technical_gate_confirmed": "yes", "runtime_broken": "yes"}},
        {"id": "major", "severity": "major", "category": "substantive", "all": {"is_defect": "yes", "is_substantive": "yes", "mechanics_context": "yes", "changes_rule_understanding": "yes", "can_change_player_action": "yes"}, "phenomenon_in": ["number", "number-range"]},
        {"id": "sub-minor", "severity": "minor", "category": "substantive-minor", "all": {"is_defect": "yes", "is_substantive": "yes"}},
        {"id": "style-minor", "severity": "minor", "category": "presentation-minor", "all": {"is_defect": "yes", "is_substantive": "no"}, "defect_class_in": ["presentation", "style"]},
        {"id": "note", "severity": "note", "category": "note", "all": {"is_defect": "no"}},
    ]
}


def facts(**updates: str) -> dict[str, str]:
    value = {field: "no" for field in POLICY["impact_fact_fields"]}
    value.update(updates)
    return value


class QualityV2SpanTests(unittest.TestCase):
    def test_unicode_offsets_are_code_points_and_half_open(self) -> None:
        result = normalize_evidence({"quote": "龙裔", "occurrence": 1}, "a龙裔z", where="e")
        self.assertEqual((result["start"], result["end"]), (1, 3))

    def test_duplicate_quote_uses_one_based_occurrence(self) -> None:
        result = normalize_evidence({"quote": "one", "occurrence": 2}, "one two one", where="e")
        self.assertEqual((result["state"], result["start"], result["end"]), ("exact", 8, 11))
        ambiguous = normalize_evidence({"quote": "one", "occurrence": 0}, "one one", where="e")
        self.assertEqual(ambiguous["state"], "ambiguous")

    def test_missing_and_out_of_range_enter_manual_state(self) -> None:
        self.assertEqual(normalize_evidence({"quote": "x", "occurrence": 1}, "abc", where="e")["state"], "missing")
        self.assertEqual(normalize_evidence({"quote": "a", "occurrence": 4}, "abc", where="e")["state"], "missing")

    def test_whole_item_and_omission_contracts(self) -> None:
        whole = normalize_evidence({"quote": "", "occurrence": 0, "whole_item": True}, "龙裔", where="e")
        self.assertEqual((whole["state"], whole["end"]), ("whole-item", 2))
        omitted = normalize_evidence({"quote": "", "occurrence": 0}, "目标", where="e", allow_empty_omission=True)
        self.assertEqual(omitted["state"], "missing")
        with self.assertRaises(ValidationError):
            normalize_evidence({"quote": "", "occurrence": 0}, "目标", where="e")

    def test_host_offsets_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValidationError, "host-owned"):
            normalize_evidence({"quote": "a", "occurrence": 1, "start": 0}, "a", where="e")


class QualityV2SeverityTests(unittest.TestCase):
    def derive(self, values: dict[str, str], phenomenon: str = "number", defect_class: str = "semantic") -> dict:
        return derive_severity(values, phenomenon=phenomenon, defect_class=defect_class, rules=RULES, policy=POLICY)

    def test_rule_precedence_and_positive_negative_examples(self) -> None:
        blocker = self.derive(facts(is_defect="yes", is_substantive="yes", technical_gate_confirmed="yes", runtime_broken="yes"), phenomenon="format", defect_class="technical")
        self.assertEqual((blocker["derived_severity"], blocker["rule_id"]), ("blocker", "block"))
        major = self.derive(facts(is_defect="yes", is_substantive="yes", mechanics_context="yes", changes_rule_understanding="yes", can_change_player_action="yes"))
        self.assertEqual((major["derived_severity"], major["rule_id"]), ("major", "major"))
        minor = self.derive(facts(is_defect="yes", is_substantive="yes", mechanics_context="yes", changes_rule_understanding="yes", can_change_player_action="no"))
        self.assertEqual((minor["derived_severity"], minor["rule_id"]), ("minor", "sub-minor"))
        style = self.derive(facts(is_defect="yes", is_substantive="no"), phenomenon="punctuation", defect_class="presentation")
        self.assertEqual((style["derived_severity"], style["rule_id"]), ("minor", "style-minor"))
        note = self.derive(facts(is_defect="no"), phenomenon="punctuation", defect_class="style")
        self.assertEqual((note["derived_severity"], note["rule_id"]), ("note", "note"))

    def test_unknown_possible_major_does_not_silently_downgrade(self) -> None:
        result = self.derive(facts(is_defect="yes", is_substantive="yes", mechanics_context="yes", changes_rule_understanding="yes", can_change_player_action="unknown"))
        self.assertEqual(result["derivation_state"], "needs-adjudication")
        self.assertEqual(result["possible_rule_ids"], ["major"])

    def test_amplification_is_not_a_severity_input(self) -> None:
        base = facts(is_defect="yes", is_substantive="no")
        first = self.derive(base, phenomenon="punctuation", defect_class="style")
        second = self.derive(dict(base), phenomenon="punctuation", defect_class="style")
        self.assertEqual(first, second)

    def test_derivation_is_byte_deterministic(self) -> None:
        value = facts(is_defect="yes", is_substantive="yes")
        self.assertEqual(self.derive(value), self.derive(copy.deepcopy(value)))


class QualityV2RealRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.policy = load_policy_v2(cls.manifest)
        cls.rules = load_impact_rules(cls.manifest, cls.policy)

    def derive(self, values: dict[str, str], phenomenon: str, defect_class: str) -> dict:
        return derive_severity(values, phenomenon=phenomenon, defect_class=defect_class, rules=self.rules, policy=self.policy)

    def base(self, **updates: str) -> dict[str, str]:
        result = {field: "no" for field in self.policy["impact_fact_fields"]}
        result.update(updates)
        return result

    def test_versioned_configuration_loads_and_anchors_start_empty(self) -> None:
        self.assertEqual(self.policy["method_version"], "mqm-pilot-v2")
        self.assertEqual(load_anchors(self.manifest)["anchors"], [])

    def test_every_rule_has_yes_no_unknown_coverage(self) -> None:
        cases = {
            "S-FORMAT-BLOCKER-01": ("format", "technical", {"technical_gate_confirmed": "yes", "runtime_broken": "yes"}, "runtime_broken"),
            "S-FORMAT-MAJOR-01": ("format", "technical", {"technical_gate_confirmed": "yes", "single_item_display_broken": "yes"}, "single_item_display_broken"),
            "S-RULE-01": ("number-range", "semantic", {"is_defect": "yes", "is_substantive": "yes", "mechanics_context": "yes", "changes_rule_understanding": "yes", "can_change_player_action": "yes"}, "can_change_player_action"),
            "S-OPER-01": ("omission", "semantic", {"is_defect": "yes", "is_substantive": "yes", "required_operation_info_missing": "yes", "can_change_player_action": "yes"}, "required_operation_info_missing"),
            "S-REVERSE-01": ("polarity", "semantic", {"is_defect": "yes", "is_substantive": "yes", "opposite_or_different_rule": "yes", "changes_rule_understanding": "yes"}, "opposite_or_different_rule"),
            "S-SUBSTANTIVE-MINOR-01": ("ambiguity", "semantic", {"is_defect": "yes", "is_substantive": "yes"}, "is_substantive"),
            "S-PRESENTATION-MINOR-01": ("punctuation", "presentation", {"is_defect": "yes", "is_substantive": "no"}, "is_defect"),
            "S-NOTE-01": ("fluency", "style", {"is_defect": "no"}, "is_defect"),
        }
        self.assertEqual(set(cases), {rule["id"] for rule in self.rules["rules"]})
        for rule_id, (phenomenon, defect_class, updates, pivot) in cases.items():
            with self.subTest(rule=rule_id, state="yes"):
                positive = self.derive(self.base(**updates), phenomenon, defect_class)
                self.assertEqual(positive["rule_id"], rule_id)
            with self.subTest(rule=rule_id, state="no"):
                negative_updates = dict(updates)
                negative_updates[pivot] = "no" if updates[pivot] == "yes" else "yes"
                negative = self.derive(self.base(**negative_updates), phenomenon, defect_class)
                self.assertNotEqual(negative.get("rule_id"), rule_id)
            with self.subTest(rule=rule_id, state="unknown"):
                unknown_updates = dict(updates)
                unknown_updates[pivot] = "unknown"
                unknown = self.derive(self.base(**unknown_updates), phenomenon, defect_class)
                self.assertEqual(unknown["derivation_state"], "needs-adjudication")


class QualityV2AssessmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = {"sample_id": "sample", "items": [{"revision_id": "a" * 64, "source": "3–8 damage", "target": "8点伤害"}]}
        self.evaluator = {
            "kind": "model", "id": "reviewer-a", "method_version": "mqm-pilot-v2",
            "provider": "fake", "model": "fake", "thinking": "none",
            "prompt_sha256": "1" * 64, "rules_sha256": "2" * 64,
            "anchors_sha256": "3" * 64, "bundle_ids": ["4" * 64],
        }
        self.finding = {
            "finding_id": "A-001", "error_code": "ACC_NUMBER_UNIT", "defect_class": "semantic", "phenomenon": "number-range",
            "source_evidence": {"quote": "3–8 damage", "occurrence": 1}, "target_evidence": {"quote": "8点伤害", "occurrence": 1},
            "defect_summary": "范围成为上限", "meaning_change": {"type": "strengthened", "summary": "范围丢失"},
            "impact_facts": facts(is_defect="yes", is_substantive="yes", mechanics_context="yes", changes_rule_understanding="yes", can_change_player_action="yes"),
            "amplification_scope": "local", "closest_anchor_id": None, "anchor_relation": "unknown", "body": "最低值丢失", "evidence_refs": [],
        }
        item = {"revision_id": "a" * 64, "context_sufficient": True, "profile_confirmed": "mechanics", "findings": [self.finding], "reuse_recommendation": "same-tag"}
        self.assessment = build_assessment_v2(sample_id="sample", evaluator=self.evaluator, items=[item])
        self.taxonomy = {"error_codes": [{"code": "ACC_NUMBER_UNIT"}]}
        self.anchors = {"anchors": []}

    def validate(self, value: dict | None = None) -> dict:
        return validate_assessment_v2(value or self.assessment, sample=self.sample, policy=POLICY, rules=RULES, anchors=self.anchors, taxonomy=self.taxonomy, expected_evaluator=self.evaluator)

    def test_valid_assessment_normalizes_spans_and_derives_severity(self) -> None:
        result = self.validate()
        finding = result["items"][0]["findings"][0]
        self.assertEqual(finding["normalized_source_evidence"]["end"], 10)
        self.assertEqual(finding["derivation"]["derived_severity"], "major")

    def test_unknown_and_host_severity_fields_are_rejected(self) -> None:
        value = copy.deepcopy(self.assessment)
        value["items"][0]["findings"][0]["derived_severity"] = "major"
        value["assessment_id"] = assessment_identity(value)
        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            self.validate(value)

    def test_identity_and_host_evaluator_are_bound(self) -> None:
        value = copy.deepcopy(self.assessment)
        value["evaluator"]["model"] = "other"
        value["assessment_id"] = assessment_identity(value)
        with self.assertRaisesRegex(ValidationError, "host-owned"):
            self.validate(value)
        value = copy.deepcopy(self.assessment)
        value["assessment_id"] = "0" * 64
        with self.assertRaisesRegex(ValidationError, "assessment_id"):
            self.validate(value)

    def test_logical_conflicts_are_rejected(self) -> None:
        value = copy.deepcopy(self.assessment)
        value["items"][0]["findings"][0]["impact_facts"].update(is_defect="no", is_substantive="yes")
        value["assessment_id"] = assessment_identity(value)
        with self.assertRaisesRegex(ValidationError, "non-defect"):
            self.validate(value)

    def test_legal_omission(self) -> None:
        value = copy.deepcopy(self.assessment)
        finding = value["items"][0]["findings"][0]
        finding["meaning_change"] = {"type": "omitted", "summary": "范围缺失"}
        finding["target_evidence"] = {"quote": "", "occurrence": 0}
        value["assessment_id"] = assessment_identity(value)
        result = self.validate(value)
        self.assertEqual(result["items"][0]["findings"][0]["normalized_target_evidence"]["state"], "missing")

    def test_model_cannot_self_confirm_a_technical_gate(self) -> None:
        value = copy.deepcopy(self.assessment)
        value["items"][0]["findings"][0]["impact_facts"].update(
            technical_gate_confirmed="yes", runtime_broken="yes"
        )
        value["assessment_id"] = assessment_identity(value)
        with self.assertRaisesRegex(ValidationError, "without host gate signals"):
            self.validate(value)

    def test_deterministic_gate_has_priority_over_model_facts(self) -> None:
        sample = copy.deepcopy(self.sample)
        sample["items"][0]["gate_signals"] = {
            "lua_load_valid": False, "format_signature_match": True,
            "markup_multiset_match": True, "at_token_multiset_match": True,
            "runtime_collision": False, "empty_target": False,
            "format_shape_match": True,
        }
        result = validate_assessment_v2(
            self.assessment, sample=sample, policy=POLICY, rules=RULES,
            anchors=self.anchors, taxonomy=self.taxonomy,
            expected_evaluator=self.evaluator,
        )
        finding = result["items"][0]["findings"][0]
        self.assertEqual(finding["host_gate_facts"]["runtime_broken"], "yes")
        self.assertEqual(finding["derivation"]["derived_severity"], "blocker")


def normalized_finding(
    finding_id: str,
    *,
    source_quote: str = "abc",
    source_start: int = 0,
    target_quote: str = "甲乙丙",
    target_start: int = 0,
    phenomenon: str = "number",
    meaning_type: str = "strengthened",
    impact: dict[str, str] | None = None,
) -> dict:
    impact = impact or facts(is_defect="yes", is_substantive="yes")
    finding = {
        "finding_id": finding_id, "error_code": "ACC_NUMBER_UNIT",
        "defect_class": "semantic", "phenomenon": phenomenon,
        "defect_summary": "summary", "meaning_change": {"type": meaning_type, "summary": "change"},
        "impact_facts": impact, "amplification_scope": "local",
        "closest_anchor_id": None, "anchor_relation": "unknown", "body": "body",
        "normalized_source_evidence": {"quote": source_quote, "occurrence": 1, "state": "exact", "start": source_start, "end": source_start + len(source_quote)},
        "normalized_target_evidence": {"quote": target_quote, "occurrence": 1, "state": "exact", "start": target_start, "end": target_start + len(target_quote)},
    }
    finding["derivation"] = derive_severity(
        impact, phenomenon=phenomenon, defect_class="semantic", rules=RULES, policy=POLICY
    )
    return finding


def matching_inputs(left_findings: list[dict], right_findings: list[dict]) -> tuple[dict, dict, dict]:
    revision = "a" * 64
    sample = {"sample_id": "sample", "items": [{"revision_id": revision, "source": "abcdefghi", "target": "甲乙丙丁戊己庚辛壬", "context_neighbors": []}]}
    base_evaluator = {"id": "reviewer-a"}
    left = {"sample_id": "sample", "assessment_id": "1" * 64, "evaluator": base_evaluator, "items": [{"revision_id": revision, "findings": left_findings}]}
    right = {"sample_id": "sample", "assessment_id": "2" * 64, "evaluator": {"id": "reviewer-b"}, "items": [{"revision_id": revision, "findings": right_findings}]}
    return sample, left, right


class QualityV2MatchingTests(unittest.TestCase):
    def match(self, left: list[dict], right: list[dict]) -> dict:
        sample, left_assessment, right_assessment = matching_inputs(left, right)
        return match_assessments_v2(sample=sample, left_assessment=left_assessment, right_assessment=right_assessment, policy={**POLICY, "mergeable_phenomena": [["number", "number-range"]]})

    def test_full_and_partial_matches(self) -> None:
        full = self.match([normalized_finding("A-1")], [normalized_finding("B-1")])
        self.assertEqual(full["issues"][0]["cluster_type"], "full-match")
        partial = self.match([normalized_finding("A-1", phenomenon="number")], [normalized_finding("B-1", phenomenon="number-range")])
        self.assertEqual(partial["issues"][0]["cluster_type"], "partial-match")

    def test_split_merge_and_ambiguous(self) -> None:
        broad = normalized_finding("A-1", source_quote="abcdef", target_quote="甲乙丙丁戊己")
        split = self.match(
            [broad],
            [
                normalized_finding("B-1", source_quote="abc", target_quote="甲乙丙"),
                normalized_finding("B-2", source_quote="def", source_start=3, target_quote="丁戊己", target_start=3),
            ],
        )
        self.assertEqual(split["issues"][0]["cluster_type"], "split-merge")
        ambiguous = self.match(
            [normalized_finding("A-1"), normalized_finding("A-2")],
            [normalized_finding("B-1"), normalized_finding("B-2")],
        )
        self.assertEqual(ambiguous["issues"][0]["cluster_type"], "ambiguous")

    def test_single_sided_and_different_spans_do_not_match(self) -> None:
        result = self.match(
            [normalized_finding("A-1", source_start=0, target_start=0)],
            [normalized_finding("B-1", source_quote="ghi", source_start=6, target_quote="庚辛壬", target_start=6)],
        )
        self.assertEqual([item["cluster_type"] for item in result["issues"]], ["left-only", "right-only"])

    def test_many_revisions_are_not_globally_compared_and_ids_are_stable(self) -> None:
        first = self.match([normalized_finding("A-1")], [normalized_finding("B-1")])
        second = self.match([copy.deepcopy(normalized_finding("A-1"))], [copy.deepcopy(normalized_finding("B-1"))])
        self.assertEqual(first, second)
        self.assertEqual(first["issues"][0]["issue_id"], "QI-0001")

    def test_ambiguous_evidence_enters_manual_queue(self) -> None:
        finding = normalized_finding("A-1")
        finding["normalized_source_evidence"].update(state="ambiguous", start=None, end=None)
        result = self.match([finding], [])
        self.assertEqual(result["manual_queue"], ["QI-0001"])


class QualityV2DisputeAndAdjudicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample, self.left, self.right = matching_inputs([normalized_finding("A-1")], [])
        self.match = match_assessments_v2(
            sample=self.sample, left_assessment=self.left, right_assessment=self.right,
            policy={**POLICY, "mergeable_phenomena": [["number", "number-range"]]},
        )

    def test_dispute_is_anonymous_deterministic_and_identity_is_separate(self) -> None:
        first = build_disputes_v2(match=self.match, sample=self.sample, assessments=(self.left, self.right))
        second = build_disputes_v2(match=self.match, sample=self.sample, assessments=(self.left, self.right))
        self.assertEqual(first, second)
        dispute, identity = first
        public = json.dumps(dispute, sort_keys=True)
        self.assertNotIn("reviewer-a", public)
        self.assertNotIn("assessment_id", public)
        self.assertEqual(identity["mappings"][0]["evaluator_id"], "reviewer-a")

    def adjudication(self) -> dict:
        values = facts(is_defect="no")
        return {
            "schema_version": 2, "quality_contract": "tome4-quality-adjudication-v2",
            "match_id": self.match["match_id"], "adjudicator_id": "human-1",
            "items": [{
                "issue_id": "QI-0001", "same_issue": True, "exists": False,
                "confirmed_facts": values, "phenomenon": "number", "defect_class": "semantic",
                "derived_severity": "note", "rule_id": "note", "anchor_id": None,
                "rationale": "The candidate is not a defect.",
            }],
        }

    def test_adjudication_recomputes_severity(self) -> None:
        result = adjudicate_v2(match=self.match, adjudication=self.adjudication(), policy=POLICY, rules=RULES, anchors={"anchors": []})
        self.assertEqual(result["items"][0]["derivation"]["rule_id"], "note")
        tampered = self.adjudication()
        tampered["items"][0].update(derived_severity="major", rule_id="major")
        with self.assertRaisesRegex(ValidationError, "cannot be reproduced"):
            adjudicate_v2(match=self.match, adjudication=tampered, policy=POLICY, rules=RULES, anchors={"anchors": []})

    def test_strict_adjudication_requires_complete_ordered_manual_queue(self) -> None:
        value = self.adjudication()
        value["items"] = []
        with self.assertRaisesRegex(ValidationError, "manual queue"):
            adjudicate_v2(match=self.match, adjudication=value, policy=POLICY, rules=RULES, anchors={"anchors": []})


def synthetic_v2_sample(items: list[dict], contract: str = "tome4-quality-calibration-v2") -> dict:
    identity = {
        "schema_version": 2, "quality_contract": contract,
        "dataset_kind": "calibration" if "calibration" in contract else "holdout",
        "seed": "seed", "size": len(items), "taxonomy_sha256": "1" * 64,
        "policy_v1_sha256": "2" * 64, "policy_v2_sha256": "3" * 64,
        "manifest_sha256": "4" * 64, "inventory_sha256": "5" * 64,
        "excluded_ids_sha256": "6" * 64,
        "items_sha256": canonical_sha256(items),
        "revisions": [item["revision_id"] for item in items],
    }
    identity["sample_id"] = canonical_sha256(identity)
    return {**identity, "coverage": {}, "items": items}


class QualityV2ShardingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.policy = load_policy_v2(cls.manifest)
        cls.rules = load_impact_rules(cls.manifest, cls.policy)
        cls.anchors = load_anchors(cls.manifest)
        from i18nlib.quality import load_taxonomy
        cls.taxonomy = load_taxonomy(cls.manifest)

    def item(self, index: int, group: str | None = None) -> dict:
        return {
            "index": index, "revision_id": f"{index + 1:064x}",
            "source": f"source {index}", "target": f"目标 {index}",
            "contrast_group": group, "profile": "ui",
        }

    def test_shards_preserve_order_size_and_contrast_atomicity(self) -> None:
        items = [self.item(index) for index in range(25)]
        for index in (18, 19, 20):
            items[index]["contrast_group"] = "g"
        sample = synthetic_v2_sample(items)
        bundles = build_evaluator_bundles_v2(
            sample=sample, evaluator_id="reviewer-a", policy=self.policy,
            rules=self.rules, anchors=self.anchors, taxonomy=self.taxonomy,
            max_items=20,
        )
        self.assertEqual([len(bundle["items"]) for bundle in bundles], [18, 7])
        self.assertEqual(
            [item["revision_id"] for bundle in bundles for item in bundle["items"]],
            sample["revisions"],
        )
        locations = {
            item["contrast_group"]: bundle["shard_index"]
            for bundle in bundles for item in bundle["items"]
            if item.get("contrast_group")
        }
        self.assertEqual(locations, {"g": 2})

    def test_sample_path_boundary_and_identity(self) -> None:
        sample = synthetic_v2_sample([self.item(0)])
        self.assertIs(validate_sample_v2(sample), sample)
        unsafe = copy.deepcopy(sample)
        unsafe["items"][0]["source"] = "/Users/example/secret"
        unsafe["items_sha256"] = canonical_sha256(unsafe["items"])
        identity = {
            key: unsafe[key]
            for key in (
                "schema_version", "quality_contract", "dataset_kind", "seed", "size",
                "taxonomy_sha256", "policy_v1_sha256", "policy_v2_sha256",
                "manifest_sha256", "inventory_sha256", "excluded_ids_sha256",
                "items_sha256", "revisions",
            )
        }
        unsafe["sample_id"] = canonical_sha256(identity)
        with self.assertRaisesRegex(ValidationError, "forbidden host path"):
            validate_sample_v2(unsafe)

    def test_cache_identity_binds_all_v2_inputs(self) -> None:
        base = {
            "sample_id": "s", "evaluator_id": "reviewer-a", "provider": "p",
            "model": "m", "thinking": "t", "prompt_sha256": "1" * 64,
            "rules_sha256": "2" * 64, "anchors_sha256": "3" * 64,
            "bundle_ids": ["4" * 64, "5" * 64], "strict": True,
        }
        original = _cache_key_v2(**base)
        for field, replacement in (
            ("sample_id", "other"), ("evaluator_id", "reviewer-b"),
            ("provider", "q"), ("model", "n"), ("thinking", "u"),
            ("prompt_sha256", "6" * 64), ("rules_sha256", "7" * 64),
            ("anchors_sha256", "8" * 64), ("bundle_ids", ["9" * 64]),
            ("strict", False),
        ):
            changed = dict(base)
            changed[field] = replacement
            self.assertNotEqual(original, _cache_key_v2(**changed), field)

    def test_v2_prompt_declares_complete_model_owned_item_contract(self) -> None:
        prompt = (
            Path(__file__).resolve().parents[2]
            / "i18n" / "prompts" / "pi-quality-evaluator-v2.md"
        ).read_text(encoding="utf-8")
        for field in (
            '"revision_id"', '"context_sufficient"', '"profile_confirmed"',
            '"findings"', '"reuse_recommendation"', '"finding_id"',
            '"impact_facts"', '"evidence_refs"',
        ):
            self.assertIn(field, prompt)
        self.assertIn("All eleven `impact_facts` fields are required", prompt)
        self.assertIn("Finding IDs must be unique across shards", prompt)

    def test_fake_runner_merges_shards_into_one_assessment(self) -> None:
        items = [self.item(index) for index in range(21)]
        sample = synthetic_v2_sample(items)
        with tempfile.TemporaryDirectory(prefix="quality-v2-runner-") as temporary:
            sample_path = Path(temporary) / "sample.json"
            sample_path.write_text(json.dumps(sample), encoding="utf-8")
            outputs = []
            for subset in (items[:20], items[20:]):
                model_items = [
                    {
                        "revision_id": item["revision_id"],
                        "context_sufficient": True, "profile_confirmed": "ui",
                        "findings": [], "reuse_recommendation": None,
                    }
                    for item in subset
                ]
                outputs.append(
                    subprocess.CompletedProcess(
                        [], 0, json.dumps({"items": model_items}).encode(), b""
                    )
                )
            with patch(
                "i18nlib.pi_quality._run_file_review_process", side_effect=outputs
            ):
                report = run_pi_quality_evaluator(
                    sample_path=sample_path, evaluator_id="reviewer-a",
                    provider="fake", model="fake", thinking="none",
                    use_cache=False, pi_executable="fake-pi",
                )
        self.assertTrue(report["ok"])
        self.assertEqual(
            (report["shards"], report["items"], report["findings"]), (2, 21, 0)
        )
        self.assertEqual(len(report["shard_artifacts"]), 2)
        self.assertTrue(all(item["parsed_output"] for item in report["shard_artifacts"]))

    def test_fake_runner_format_failure_preserves_raw_and_report(self) -> None:
        sample = synthetic_v2_sample([self.item(0)])
        with tempfile.TemporaryDirectory(prefix="quality-v2-failure-") as temporary:
            root = Path(temporary)
            sample_path = root / "sample.json"
            sample_path.write_text(json.dumps(sample), encoding="utf-8")
            run_directory = root / "run"
            run_directory.mkdir()
            malformed = subprocess.CompletedProcess([], 0, b"not-json", b"")
            with (
                patch("i18nlib.pi_quality.create_run_directory", return_value=run_directory),
                patch("i18nlib.pi_quality._run_file_review_process", return_value=malformed),
            ):
                with self.assertRaises(AgentError):
                    run_pi_quality_evaluator(
                        sample_path=sample_path, evaluator_id="reviewer-a",
                        provider="fake", model="fake", thinking="none",
                        use_cache=False, pi_executable="fake-pi",
                    )
            report = json.loads((run_directory / "pi-quality-evaluator.json").read_text())
            self.assertEqual(report["failed_shard"], 1)
            self.assertTrue(Path(report["raw_outputs"][0]).is_file())


class QualityV2ReportTests(unittest.TestCase):
    def test_report_has_item_issue_fact_severity_and_burden_metrics(self) -> None:
        sample, left, right = matching_inputs(
            [normalized_finding("A-1")], [normalized_finding("B-1")]
        )
        match = match_assessments_v2(
            sample=sample, left_assessment=left, right_assessment=right,
            policy={**POLICY, "mergeable_phenomena": [["number", "number-range"]]},
        )
        report = build_report_v2(match=match)
        self.assertEqual(report["issue_metrics"]["jaccard"], 1.0)
        self.assertEqual(report["human_burden"]["issues_requiring_adjudication"], 0)
        self.assertEqual(report["item_metrics"]["items_total"], 1)
        self.assertIn("is_defect", report["fact_metrics"])
        self.assertIn("minor", report["severity_metrics"]["pre_adjudication"])


if __name__ == "__main__":
    unittest.main()
