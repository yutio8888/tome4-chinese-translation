from __future__ import annotations

import copy
import hashlib
import inspect
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import load_manifest
from i18nlib.cli_quality import _quality_stability_v2, _quality_stability_v3
from i18nlib.errors import AgentError, ConfigurationError, ValidationError
from i18nlib.pi_quality import (
    _cache_key, _cache_key_v2, _cache_key_v3,
    _register_campaign_stability_report, _update_campaign_transfer,
    run_pi_quality_evaluator,
)
from i18nlib.quality_v3 import (
    METHOD_V3,
    build_assessment_v3,
    build_evaluator_bundles_v3,
    build_stability_report_v3,
    build_report_v3,
    adjudicate_v3,
    canonical_sha256,
    derive_severity_v3,
    load_anchors_v2,
    load_evaluator_prompt_v3,
    load_policy_v3,
    load_severity_matrix,
    match_assessments_v3,
    replay_assessment_v2_as_v3,
    validate_assessment_v3,
    validate_campaign_ledger_v3,
    validate_sample_v3,
    validate_match_v3,
    validate_report_v3,
    validate_stability_report_v3,
    runner_report_semantic_identity_v3,
)


SHA = "0" * 64


def schema_accepts(instance: object, schema: dict, *, root: dict | None = None) -> bool:
    """Evaluate the strict structural subset used by the checked-in v3 schemas."""
    root = root or schema
    if "$ref" in schema:
        target = root
        for part in schema["$ref"].removeprefix("#/").split("/"):
            target = target[part]
        return schema_accepts(instance, target, root=root)
    if "const" in schema and instance != schema["const"]:
        return False
    if "enum" in schema and instance not in schema["enum"]:
        return False
    expected_type = schema.get("type")
    if expected_type is not None:
        choices = expected_type if isinstance(expected_type, list) else [expected_type]
        checks = {
            "object": lambda value: isinstance(value, dict),
            "array": lambda value: isinstance(value, list),
            "string": lambda value: isinstance(value, str),
            "integer": lambda value: type(value) is int,
            "number": lambda value: type(value) in (int, float),
            "boolean": lambda value: type(value) is bool,
            "null": lambda value: value is None,
        }
        if not any(checks[choice](instance) for choice in choices):
            return False
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            return False
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            return False
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            return False
        if "maximum" in schema and instance > schema["maximum"]:
            return False
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0) or len(instance) > schema.get("maxItems", len(instance)):
            return False
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in instance}) != len(instance):
            return False
        if isinstance(schema.get("items"), dict) and any(
            not schema_accepts(item, schema["items"], root=root) for item in instance
        ):
            return False
    if isinstance(instance, dict):
        if not set(schema.get("required", ())).issubset(instance):
            return False
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and not set(instance).issubset(properties):
            return False
        for key, value in instance.items():
            child = properties.get(key)
            if child is not None and not schema_accepts(value, child, root=root):
                return False
    return True


def sample_item(index: int, **updates: object) -> dict:
    item = {
        "args_order": None, "bucket": "random", "component": "tome",
        "context_neighbors": [], "contrast_group": None, "contrast_siblings": [],
        "domain_hints": [], "index": index, "profile": "ui",
        "profile_confidence": "high", "relevant_terms": [], "risk_flags": [],
        "section": "test.lua", "source_length_bin": "short", "source_tag": "_t",
        "special": None, "structure": {},
        "unit_id": hashlib.sha256(f"unit-{index}".encode()).hexdigest(),
        "tu_uid": hashlib.sha256(f"tu-{index}".encode()).hexdigest(),
        "revision_uid": hashlib.sha256(f"revision-uid-{index}".encode()).hexdigest(),
        "revision_id": hashlib.sha256(f"revision-{index}".encode()).hexdigest(),
        "source": f"source {index}",
        "target": f"target {index}",
        "gate_signals": {
            "lua_load_valid": True,
            "format_signature_match": True,
            "markup_multiset_match": True,
            "at_token_multiset_match": True,
            "runtime_collision": False,
            "empty_target": False,
            "format_shape_match": True,
            "cross_component_variant": False,
            "needs_review": [],
        },
    }
    item.update(updates)
    return item


def synthetic_sample(policy: dict, *, first: dict | None = None, kind: str = "calibration") -> dict:
    items = [first or sample_item(0), *(sample_item(index) for index in range(1, 32))]
    contract = f"tome4-quality-{kind}-v3"
    identity = {
        "schema_version": 3,
        "quality_contract": contract,
        "dataset_kind": kind,
        "seed": f"tome4-quality-{kind}-v2",
        "size": 32,
        "taxonomy_sha256": "1" * 64,
        "policy_v1_sha256": "2" * 64,
        "policy_v2_sha256": "3" * 64,
        "policy_v3_sha256": canonical_sha256(policy),
        "manifest_sha256": "4" * 64,
        "inventory_sha256": "5" * 64,
        "excluded_ids_sha256": "6" * 64,
        "source_sample_v2_id": "7" * 64,
        "items_sha256": canonical_sha256(items),
        "revisions": [item["revision_id"] for item in items],
    }
    return {**identity, "sample_id": canonical_sha256(identity), "coverage": {}, "items": items}


def evaluator(policy: dict, matrix: dict, anchors: dict, evaluator_id: str = "reviewer-a") -> dict:
    return {
        "kind": "model", "id": evaluator_id, "method_version": METHOD_V3,
        "provider": "fake", "model": "fake", "thinking": "none",
        "prompt_sha256": "8" * 64, "policy_sha256": canonical_sha256(policy),
        "severity_matrix_sha256": canonical_sha256(matrix),
        "anchors_sha256": canonical_sha256(anchors),
        "bundle_ids": ["9" * 64, "b" * 64],
        "bundle_sha256s": ["a" * 64, "c" * 64],
    }


def model_item(revision_id: str, findings: list[dict] | None = None, state: str = "assessed") -> dict:
    return {"revision_id": revision_id, "assessment_state": state, "findings": findings or []}


def finding(
    *,
    finding_id: str = "A-1",
    error_code: str = "ACC_NUMBER_UNIT",
    phenomenon: str = "number",
    meaning: str = "reassigned",
    source_quote: str = "source",
    target_quote: str = "target",
    source_occurrence: int = 1,
    target_occurrence: int = 1,
) -> dict:
    return {
        "finding_id": finding_id,
        "error_code": error_code,
        "phenomenon": phenomenon,
        "meaning_change": meaning,
        "source_evidence": {"quote": source_quote, "occurrence": source_occurrence},
        "target_evidence": {"quote": target_quote, "occurrence": target_occurrence},
        "explanation": "The bounded source and target visibly express different meanings.",
    }


class QualityV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.policy = load_policy_v3(cls.manifest)
        cls.matrix = load_severity_matrix(cls.manifest, cls.policy)
        cls.anchors = load_anchors_v2(cls.manifest, policy=cls.policy, matrix=cls.matrix)

    def derive(self, **updates: object) -> dict:
        values = {
            "error_code": "ACC_NUMBER_UNIT", "phenomenon": "number",
            "meaning_change": "reassigned", "policy": self.policy,
            "matrix": self.matrix,
        }
        values.update(updates)
        return derive_severity_v3(**values)

    def test_complete_compatibility_matrix_is_deterministic(self) -> None:
        for code, phenomena in self.matrix["error_code_phenomena"].items():
            for phenomenon in self.policy["phenomena"]:
                for meaning in self.policy["meaning_change_types"]:
                    compatible = (
                        phenomenon in phenomena
                        and meaning in self.matrix["phenomenon_meaning_changes"][phenomenon]
                    )
                    arguments = {
                        "error_code": code, "phenomenon": phenomenon,
                        "meaning_change": meaning, "policy": self.policy,
                        "matrix": self.matrix,
                    }
                    if compatible:
                        first = derive_severity_v3(**arguments)
                        second = derive_severity_v3(**copy.deepcopy(arguments))
                        self.assertEqual(first, second)
                    else:
                        with self.assertRaises(ValidationError):
                            derive_severity_v3(**arguments)

    def test_observable_major_and_minor_matrix(self) -> None:
        cases = (
            ("ACC_NUMBER_UNIT", "number", "omitted"),
            ("ACC_NUMBER_UNIT", "number-range", "strengthened"),
            ("ACC_CONDITION", "condition", "weakened"),
            ("ACC_POLARITY", "polarity", "reversed"),
            ("ACC_ENTITY_ROLE", "entity-role", "reassigned"),
            ("ACC_CONDITION", "scope", "added"),
            ("ACC_CONDITION", "trigger-timing", "made-ambiguous"),
        )
        for code, phenomenon, meaning in cases:
            with self.subTest(phenomenon=phenomenon):
                result = self.derive(error_code=code, phenomenon=phenomenon, meaning_change=meaning)
                self.assertEqual((result["derived_severity"], result["derivation_state"]), ("major", "derived"))
        for code, phenomenon, meaning in (
            ("ACC_NUMBER_UNIT", "unit", "omitted"),
            ("TERM_INCONSISTENT", "terminology", "reassigned"),
            ("TERM_PROPER_NAME", "proper-name", "reassigned"),
            ("ACC_OMISSION", "omission", "omitted"),
            ("ACC_ADDITION", "addition", "added"),
            ("FLU_AMBIGUITY", "ambiguity", "made-ambiguous"),
        ):
            with self.subTest(phenomenon=phenomenon, minor=True):
                result = self.derive(error_code=code, phenomenon=phenomenon, meaning_change=meaning)
                self.assertEqual((result["derived_severity"], result["derivation_state"]), ("minor", "derived"))
        self.assertEqual(
            self.derive(phenomenon="unit", meaning_change="added")["derived_severity"], "major"
        )

    def test_every_uncertainty_is_provisional_minor_and_queued(self) -> None:
        cases = (
            ({"meaning_change": "unknown"}, "V3_MEANING_UNKNOWN"),
            ({"error_code": "ACC_MISTRANSLATION", "phenomenon": "other"}, "V3_PHENOMENON_OTHER"),
            ({"source_evidence_state": "ambiguous"}, "V3_SOURCE_EVIDENCE_AMBIGUOUS"),
            ({"source_evidence_state": "missing"}, "V3_SOURCE_EVIDENCE_MISSING"),
            ({"target_evidence_state": "ambiguous"}, "V3_TARGET_EVIDENCE_AMBIGUOUS"),
            ({"assessment_state": "context-insufficient"}, "V3_CONTEXT_INSUFFICIENT"),
        )
        for updates, reason in cases:
            with self.subTest(reason=reason):
                result = self.derive(**updates)
                self.assertEqual(result["derived_severity"], "minor")
                self.assertEqual(result["derivation_state"], "provisional")
                self.assertTrue(result["requires_adjudication"])
                self.assertIn(reason, result["reason_codes"])
                self.assertNotIn("needs-adjudication", json.dumps(result))

    def test_host_gates_have_first_priority(self) -> None:
        blocker = self.derive(gate_signals={"lua_load_valid": False})
        self.assertEqual((blocker["derived_severity"], blocker["derivation_state"]), ("blocker", "gate-derived"))
        major = self.derive(gate_signals={"format_shape_match": False})
        self.assertEqual((major["derived_severity"], major["derivation_state"]), ("major", "gate-derived"))

    def _assessment(self, sample: dict, first_findings: list[dict], evaluator_id: str = "reviewer-a") -> dict:
        items = [model_item(sample["items"][0]["revision_id"], first_findings)]
        items.extend(model_item(item["revision_id"]) for item in sample["items"][1:])
        return build_assessment_v3(
            sample_id=sample["sample_id"],
            evaluator=evaluator(self.policy, self.matrix, self.anchors, evaluator_id),
            items=items,
        )

    def _preregistration(self, sample: dict) -> dict:
        bundles = {
            evaluator_id: build_evaluator_bundles_v3(
                sample=sample, evaluator_id=evaluator_id,
                policy=self.policy, matrix=self.matrix,
            )
            for evaluator_id in self.policy["evaluator_ids"]
        }
        bundle_ids = {
            evaluator_id: [bundle["bundle_id"] for bundle in values]
            for evaluator_id, values in bundles.items()
        }
        bundle_hashes = {
            evaluator_id: [canonical_sha256(bundle) for bundle in values]
            for evaluator_id, values in bundles.items()
        }
        value = {
            "contract": "tome4-quality-stability-preregistration-v2", "schema_version": 2,
            "sample_contract": sample["quality_contract"], "sample_id": sample["sample_id"],
            "evaluators": [
                {"id": "reviewer-a", "provider": "fake", "model": "fake", "thinking": "none", "runs": 2},
                {"id": "reviewer-b", "provider": "fake", "model": "fake", "thinking": "none", "runs": 2},
            ],
            "thresholds": self.policy["stability_thresholds"],
            "frozen_inputs": {
                "calibration_sample_id": sample["sample_id"],
                "calibration_sample_sha256": canonical_sha256(sample),
                "holdout_sample_id": "b" * 64, "holdout_sample_sha256": "c" * 64,
                "policy_v3_sha256": canonical_sha256(self.policy),
                "prompt_sha256": hashlib.sha256(load_evaluator_prompt_v3(self.manifest).encode()).hexdigest(),
                "severity_matrix_sha256": canonical_sha256(self.matrix),
                "anchors_sha256": canonical_sha256(self.anchors),
                "bundle_ids_by_evaluator": bundle_ids,
                "bundle_sha256s_by_evaluator": bundle_hashes,
            },
            "external_transfer_limit": 8, "connection_failure_retry_limit": 0,
            "replace_content_failures": False, "preregistration_id": "",
        }
        value["preregistration_id"] = canonical_sha256({key: item for key, item in value.items() if key != "preregistration_id"})
        return value

    def _clearance_report(self, preregistration: dict, evaluator_id: str, *, passed: bool = True) -> dict:
        marker = "1" if evaluator_id == "reviewer-a" else "2"
        report = {
            "schema_version": 3, "quality_contract": "tome4-quality-stability-report-v3",
            "sample_id": preregistration["sample_id"],
            "preregistration_id": preregistration["preregistration_id"],
            "evaluator": {"id": evaluator_id, "provider": "fake", "model": "fake", "thinking": "none"},
            "assessment_ids": [marker * 64, marker * 64],
            "assessment_sha256s": [marker * 64, marker * 64],
            "run_report_sha256s": ["3" * 64, "4" * 64],
            "runner_report_ids": ["5" * 64, "6" * 64],
            "execution_ids": ["7" * 64, "8" * 64],
            "metrics": {
                "schema_coverage": 1.0, "structure_failures": 0,
                "raw_model": {"finding_jaccard": 1.0, "finding_union": 0, "finding_intersection": 0, "phenomenon_meaning_agreement": 1.0},
                "anchor_normalized": {"finding_jaccard": 1.0, "finding_union": 0, "finding_intersection": 0, "provisional_severity_agreement": 1.0, "manual_queue_membership_agreement": 1.0},
                "host_technical_derivation_agreement": 1.0,
            },
            "checks": {
                "schema_coverage": passed, "structure_failures": passed,
                "raw_finding_jaccard": passed, "phenomenon_meaning_agreement": passed,
                "normalized_provisional_severity_agreement": passed,
                "manual_queue_membership_agreement": passed,
                "host_technical_derivation_agreement": passed,
            },
            "passed": passed, "report_id": "",
        }
        report["report_id"] = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
        return report

    def test_positive_negative_anchor_and_no_injection(self) -> None:
        unit_item = sample_item(
            0,
            revision_id="707b03b9a627a707cbbd8684b14f6b0a25ad09b733c952dfb9791ac481494821",
            source="Turns elapse between self-loadings: ", target="自动填弹间隔：",
        )
        sample = synthetic_sample(self.policy, first=unit_item)
        unit = finding(
            phenomenon="unit", meaning="omitted",
            source_quote="Turns elapse between self-loadings: ", target_quote="自动填弹间隔：",
        )
        normalized = validate_assessment_v3(
            self._assessment(sample, [unit]), sample=sample, policy=self.policy,
            matrix=self.matrix, anchors=self.anchors,
        )
        found = normalized["items"][0]["findings"][0]
        self.assertEqual((found["derivation"]["derived_severity"], found["anchor_id"]), ("minor", "A-UNIT-MINOR-TURN-01"))
        conflict = dict(unit, phenomenon="number")
        conflict_normalized = validate_assessment_v3(
            self._assessment(sample, [conflict]), sample=sample, policy=self.policy,
            matrix=self.matrix, anchors=self.anchors,
        )["items"][0]["findings"][0]
        self.assertEqual(conflict_normalized["normalized_phenomenon"], "unit")
        self.assertTrue(conflict_normalized["derivation"]["anchor_conflict"])
        self.assertEqual(conflict_normalized["derivation"]["derived_severity"], "minor")
        clean = validate_assessment_v3(
            self._assessment(sample, []), sample=sample, policy=self.policy,
            matrix=self.matrix, anchors=self.anchors,
        )
        self.assertEqual(clean["items"][0]["findings"], [])

        negative_item = sample_item(
            0,
            revision_id="22459090528963ac39578e508f9a0a169629550ed1345fb79f3a2907d2cc876c",
            source="molten rock", target="熔岩",
        )
        negative_sample = synthetic_sample(self.policy, first=negative_item)
        false_finding = finding(
            error_code="ACC_MISTRANSLATION", phenomenon="entity-role", meaning="reassigned",
            source_quote="molten rock", target_quote="熔岩",
        )
        rejected = validate_assessment_v3(
            self._assessment(negative_sample, [false_finding]), sample=negative_sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )["items"][0]
        self.assertEqual((len(rejected["raw_findings"]), len(rejected["findings"]), len(rejected["anchor_rejections"])), (1, 0, 1))
        holdout = synthetic_sample(self.policy, first=negative_item, kind="holdout")
        retained = validate_assessment_v3(
            self._assessment(holdout, [false_finding]), sample=holdout,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )["items"][0]
        self.assertEqual(len(retained["findings"]), 1)

    def test_legacy_severity_impact_and_technical_outputs_are_rejected(self) -> None:
        sample = synthetic_sample(self.policy)
        base = finding(source_quote="source", target_quote="target")
        for field, value in (
            ("severity", "major"), ("impact_facts", {}), ("defect_class", "semantic"),
            ("amplification_scope", "local"), ("closest_anchor_id", None),
        ):
            invalid = dict(base, **{field: value})
            with self.subTest(field=field), self.assertRaisesRegex(ValidationError, "unknown fields"):
                validate_assessment_v3(
                    self._assessment(sample, [invalid]), sample=sample, policy=self.policy,
                    matrix=self.matrix, anchors=self.anchors,
                )
        technical = dict(base, error_code="TECH_FORMAT", phenomenon="other")
        with self.assertRaises(ValidationError):
            validate_assessment_v3(
                self._assessment(sample, [technical]), sample=sample, policy=self.policy,
                matrix=self.matrix, anchors=self.anchors,
            )
        wrapped_meaning = dict(
            base,
            meaning_change={"type": "reassigned", "summary": "legacy wrapper"},
        )
        with self.assertRaisesRegex(ValidationError, "meaning_change must be one of"):
            validate_assessment_v3(
                self._assessment(sample, [wrapped_meaning]), sample=sample,
                policy=self.policy, matrix=self.matrix, anchors=self.anchors,
            )
        false_whole_item = copy.deepcopy(base)
        false_whole_item["source_evidence"]["whole_item"] = False
        with self.assertRaisesRegex(ValidationError, "must be true when present"):
            validate_assessment_v3(
                self._assessment(sample, [false_whole_item]), sample=sample,
                policy=self.policy, matrix=self.matrix, anchors=self.anchors,
            )

    def test_major_minor_boundary_becomes_provisional_minor(self) -> None:
        item = sample_item(0, source="source", target="target")
        sample = synthetic_sample(self.policy, first=item)
        major = finding(phenomenon="unit", meaning="added")
        minor = finding(finding_id="B-1", phenomenon="unit", meaning="omitted")
        left = validate_assessment_v3(
            self._assessment(sample, [major], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        right = validate_assessment_v3(
            self._assessment(sample, [minor], "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        match = match_assessments_v3(sample=sample, left_assessment=left, right_assessment=right)
        self.assertEqual(len(match["manual_queue"]), 1)
        derivation = match["issues"][0]["derivation"]
        self.assertEqual((derivation["derived_severity"], derivation["derivation_state"]), ("minor", "provisional"))
        self.assertEqual(derivation["reason_codes"], ["V3_SEVERITY_BOUNDARY_DISAGREEMENT"])

    def test_split_merge_is_bounded_and_queued(self) -> None:
        item = sample_item(0, source="alpha beta", target="甲乙")
        sample = synthetic_sample(self.policy, first=item)
        left_finding = finding(source_quote="alpha beta", target_quote="甲乙")
        right_findings = [
            finding(finding_id="B-1", source_quote="alpha", target_quote="甲"),
            finding(finding_id="B-2", source_quote="beta", target_quote="乙"),
        ]
        left = validate_assessment_v3(
            self._assessment(sample, [left_finding], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        right = validate_assessment_v3(
            self._assessment(sample, right_findings, "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        match = match_assessments_v3(sample=sample, left_assessment=left, right_assessment=right)
        self.assertEqual(match["issues"][0]["cluster_type"], "split-merge")
        self.assertEqual(match["manual_queue"], ["Q3-0001"])
        self.assertEqual(match["normalized_model_counts"], {"left": 1, "right": 2})
        report = build_report_v3(match=match)
        self.assertEqual(
            (report["anchor_normalized_metrics"]["left_findings"], report["anchor_normalized_metrics"]["right_findings"]),
            (1, 2),
        )

    def test_gate_suppresses_model_clusters_but_preserves_raw_metrics(self) -> None:
        sample = synthetic_sample(self.policy, first=sample_item(0, gate_signals={
            **sample_item(0)["gate_signals"], "lua_load_valid": False,
        }))
        left = validate_assessment_v3(
            self._assessment(sample, [finding()], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        right = validate_assessment_v3(
            self._assessment(sample, [finding(finding_id="B-1")], "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        self.assertEqual(len(left["items"][0]["raw_findings"]), 1)
        self.assertEqual(left["items"][0]["findings"][0]["derivation"]["defect_class"], "semantic")
        self.assertEqual(left["items"][0]["findings"][0]["derivation"]["derived_severity"], "major")
        match = match_assessments_v3(sample=sample, left_assessment=left, right_assessment=right)
        self.assertEqual(len(match["issues"]), 1)
        self.assertEqual(match["issues"][0]["members"], [])
        self.assertEqual(match["issues"][0]["derivation"]["derived_severity"], "blocker")
        self.assertEqual(match["raw_model_counts"], {"left": 1, "right": 1})

    def test_adjudication_final_major_and_reject_counts(self) -> None:
        sample = synthetic_sample(self.policy)
        left = validate_assessment_v3(
            self._assessment(sample, [finding()], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        right = validate_assessment_v3(
            self._assessment(sample, [], "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        match = match_assessments_v3(sample=sample, left_assessment=left, right_assessment=right)
        base = {"schema_version": 3, "quality_contract": "tome4-quality-adjudication-v3", "match_id": match["match_id"], "adjudicator_id": "human"}
        confirm = adjudicate_v3(match=match, policy=self.policy, adjudication={
            **base, "items": [{"issue_id": "Q3-0001", "decision": "confirm", "severity": "major", "rationale": "confirmed"}],
        })
        confirmed_report = build_report_v3(match=match, adjudication_validation=confirm)
        self.assertEqual(confirmed_report["severity_metrics"]["final_counts"], {"major": 1})
        stale = copy.deepcopy(confirm)
        stale["items"][0]["rationale"] = "tampered"
        with self.assertRaisesRegex(ValidationError, "validation_id"):
            build_report_v3(match=match, adjudication_validation=stale)
        downgraded = copy.deepcopy(confirm)
        downgraded["items"][0]["severity"] = "minor"
        downgraded["items"][0]["final_severity"] = "minor"
        downgraded["validation_id"] = canonical_sha256({
            key: value for key, value in downgraded.items() if key != "validation_id"
        })
        with self.assertRaisesRegex(ValidationError, "cannot downgrade"):
            build_report_v3(match=match, adjudication_validation=downgraded)
        unknown = copy.deepcopy(confirm)
        unknown["items"][0]["issue_id"] = "Q3-9999"
        unknown["validation_id"] = canonical_sha256({
            key: value for key, value in unknown.items() if key != "validation_id"
        })
        with self.assertRaisesRegex(ValidationError, "unknown or duplicate"):
            build_report_v3(match=match, adjudication_validation=unknown)
        reject = adjudicate_v3(match=match, policy=self.policy, adjudication={
            **base, "items": [{"issue_id": "Q3-0001", "decision": "reject", "severity": None, "rationale": "false positive"}],
        })
        rejected_report = build_report_v3(match=match, adjudication_validation=reject)
        self.assertEqual(rejected_report["severity_metrics"]["pre_adjudication_counts"], {"major": 1})
        self.assertEqual(
            rejected_report["adjudication_validation_id"], reject["validation_id"]
        )
        self.assertEqual(rejected_report["severity_metrics"]["final_counts"], {})

    def test_report_rejects_forged_metrics_and_missing_adjudication_lineage(self) -> None:
        sample = synthetic_sample(self.policy)
        left = validate_assessment_v3(
            self._assessment(sample, [], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        right = validate_assessment_v3(
            self._assessment(sample, [], "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        match = match_assessments_v3(
            sample=sample, left_assessment=left, right_assessment=right,
        )
        report = build_report_v3(match=match)
        self.assertIsNone(report["adjudication_validation_id"])
        forged = copy.deepcopy(report)
        forged["human_burden"]["findings_rejected"] = 999
        forged["report_id"] = canonical_sha256({
            key: value for key, value in forged.items() if key != "report_id"
        })
        with self.assertRaisesRegex(ValidationError, "derived content"):
            validate_report_v3(forged, match=match)
        stale = copy.deepcopy(report)
        stale["adjudication_validation_id"] = "f" * 64
        stale["report_id"] = canonical_sha256({
            key: value for key, value in stale.items() if key != "report_id"
        })
        with self.assertRaisesRegex(ValidationError, "derived content"):
            validate_report_v3(stale, match=match)

    def test_representative_v3_schema_positive_and_negative_examples(self) -> None:
        schema_root = self.manifest.root / "i18n/quality/schemas"
        assessment_schema = json.loads(
            (schema_root / "assessment-v3.schema.json").read_text(encoding="utf-8")
        )
        sample = synthetic_sample(self.policy)
        bundles = build_evaluator_bundles_v3(
            sample=sample, evaluator_id="reviewer-a",
            policy=self.policy, matrix=self.matrix,
        )
        schema_evaluator = evaluator(self.policy, self.matrix, self.anchors)
        schema_evaluator.update(
            bundle_ids=[bundle["bundle_id"] for bundle in bundles],
            bundle_sha256s=[canonical_sha256(bundle) for bundle in bundles],
        )
        assessment = build_assessment_v3(
            sample_id=sample["sample_id"], evaluator=schema_evaluator,
            items=[model_item(item["revision_id"]) for item in sample["items"]],
        )
        self.assertTrue(schema_accepts(assessment, assessment_schema))
        duplicate_bundles = copy.deepcopy(assessment)
        duplicate_bundles["evaluator"]["bundle_ids"] *= 2
        duplicate_bundles["evaluator"]["bundle_sha256s"] *= 2
        self.assertFalse(schema_accepts(duplicate_bundles, assessment_schema))
        single_bundle = copy.deepcopy(assessment)
        single_bundle["evaluator"]["bundle_ids"] = single_bundle["evaluator"]["bundle_ids"][:1]
        single_bundle["evaluator"]["bundle_sha256s"] = single_bundle["evaluator"]["bundle_sha256s"][:1]
        single_bundle["assessment_id"] = canonical_sha256({
            key: value for key, value in single_bundle.items() if key != "assessment_id"
        })
        with self.assertRaisesRegex(ValidationError, "two unique shard identities"):
            validate_assessment_v3(
                single_bundle, sample=sample, policy=self.policy,
                matrix=self.matrix, anchors=self.anchors,
            )
        bad_finding = copy.deepcopy(assessment)
        bad_finding["items"][0]["findings"] = [finding(error_code="NOT_A_CODE")]
        self.assertFalse(schema_accepts(bad_finding, assessment_schema))

        report_schema = json.loads(
            (schema_root / "report-v3.schema.json").read_text(encoding="utf-8")
        )
        left = validate_assessment_v3(
            self._assessment(sample, [], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        right = validate_assessment_v3(
            self._assessment(sample, [], "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        match = match_assessments_v3(sample=sample, left_assessment=left, right_assessment=right)
        report = build_report_v3(match=match)
        self.assertTrue(schema_accepts(report, report_schema))
        missing_lineage = copy.deepcopy(report)
        del missing_lineage["adjudication_validation_id"]
        self.assertFalse(schema_accepts(missing_lineage, report_schema))

    def test_sample_validation_rejects_bad_frozen_fields_uniformly(self) -> None:
        sample = synthetic_sample(self.policy)
        cases = {
            "seed": lambda value: value.__setitem__("seed", "other"),
            "sha": lambda value: value.__setitem__("inventory_sha256", "BAD"),
            "item": lambda value: value["items"][0].__setitem__("index", "0"),
            "gate": lambda value: value["items"][0]["gate_signals"].__setitem__("runtime_collision", "false"),
        }
        for name, mutate in cases.items():
            value = copy.deepcopy(sample)
            mutate(value)
            with self.subTest(name=name), self.assertRaises(ValidationError):
                validate_sample_v3(value, self.policy)
        self.assertIs(validate_sample_v3(sample, self.policy), sample)

    def test_fixed_shard_size_and_two_shards(self) -> None:
        sample = synthetic_sample(self.policy)
        bundles = build_evaluator_bundles_v3(
            sample=sample, evaluator_id="reviewer-a", policy=self.policy, matrix=self.matrix
        )
        self.assertEqual((len(bundles), [len(bundle["items"]) for bundle in bundles]), (2, [20, 12]))
        with self.assertRaisesRegex(ValidationError, "frozen at 20"):
            build_evaluator_bundles_v3(
                sample=sample, evaluator_id="reviewer-a", policy=self.policy,
                matrix=self.matrix, max_items=16,
            )

    def test_match_identity_tampering_is_rejected(self) -> None:
        sample = synthetic_sample(self.policy)
        left = validate_assessment_v3(self._assessment(sample, [], "reviewer-a"), sample=sample, policy=self.policy, matrix=self.matrix, anchors=self.anchors)
        right = validate_assessment_v3(self._assessment(sample, [], "reviewer-b"), sample=sample, policy=self.policy, matrix=self.matrix, anchors=self.anchors)
        match = match_assessments_v3(sample=sample, left_assessment=left, right_assessment=right)
        tampered = copy.deepcopy(match)
        tampered["sample_id"] = "f" * 64
        with self.assertRaisesRegex(ValidationError, "match_id"):
            validate_match_v3(tampered)

        invalid_metrics = copy.deepcopy(match)
        invalid_metrics["raw_model_metrics"]["finding_jaccard"] = 2.0
        invalid_metrics["match_id"] = canonical_sha256({
            key: value for key, value in invalid_metrics.items() if key != "match_id"
        })
        with self.assertRaisesRegex(ValidationError, "from 0 to 1"):
            validate_match_v3(invalid_metrics)
        with self.assertRaises(ValidationError):
            build_report_v3(match=invalid_metrics)

        observed = finding(source_quote="source", target_quote="target")
        left = validate_assessment_v3(
            self._assessment(sample, [observed], "reviewer-a"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        observed_right = dict(observed, finding_id="B-1")
        right = validate_assessment_v3(
            self._assessment(sample, [observed_right], "reviewer-b"), sample=sample,
            policy=self.policy, matrix=self.matrix, anchors=self.anchors,
        )
        evidence_mismatch = match_assessments_v3(
            sample=sample, left_assessment=left, right_assessment=right,
        )
        evidence_mismatch["issues"][0]["members"][0]["source_evidence"]["whole_item"] = False
        evidence_mismatch["match_id"] = canonical_sha256({
            key: value for key, value in evidence_mismatch.items() if key != "match_id"
        })
        with self.assertRaisesRegex(ValidationError, "must be true when present"):
            validate_match_v3(evidence_mismatch)

    def test_campaign_ledger_consumes_failures_and_all_eight_slots(self) -> None:
        with tempfile.TemporaryDirectory(prefix="quality-v3-ledger-") as temporary:
            root = Path(temporary)
            preregistration_id = "d" * 64
            _update_campaign_transfer(root=root, preregistration_id=preregistration_id, evaluator_id="reviewer-a", round_number=1, execution_id="1" * 64, shard_index=1, bundle_id="a" * 64)
            _update_campaign_transfer(root=root, preregistration_id=preregistration_id, evaluator_id="reviewer-a", round_number=1, execution_id="1" * 64, shard_index=1, bundle_id="a" * 64, new_state="failed")
            with self.assertRaisesRegex(ValidationError, "already consumed"):
                _update_campaign_transfer(root=root, preregistration_id=preregistration_id, evaluator_id="reviewer-a", round_number=1, execution_id="2" * 64, shard_index=1, bundle_id="a" * 64)
            for evaluator_id in ("reviewer-a", "reviewer-b"):
                for round_number in (1, 2):
                    for shard_index in (1, 2):
                        if (evaluator_id, round_number, shard_index) == ("reviewer-a", 1, 1):
                            continue
                        _update_campaign_transfer(root=root, preregistration_id=preregistration_id, evaluator_id=evaluator_id, round_number=round_number, execution_id=f"{round_number}{shard_index}".ljust(64, "0"), shard_index=shard_index, bundle_id=hashlib.sha256(f"{evaluator_id}-{round_number}-{shard_index}".encode()).hexdigest())
            with self.assertRaises(ValidationError):
                _update_campaign_transfer(root=root, preregistration_id=preregistration_id, evaluator_id="reviewer-b", round_number=2, execution_id="9" * 64, shard_index=2, bundle_id="9" * 64)

    def test_campaign_ledger_rejects_wrong_bundle_identity(self) -> None:
        sample = synthetic_sample(self.policy)
        preregistration = self._preregistration(sample)
        ledger = {
            "contract": "tome4-quality-calibration-campaign-ledger-v3",
            "schema_version": 3,
            "preregistration_id": preregistration["preregistration_id"],
            "external_transfer_limit": 8,
            "transfers": [{
                "evaluator_id": "reviewer-a", "round": 1,
                "execution_id": "1" * 64, "shard_index": 1,
                "bundle_id": "f" * 64, "state": "succeeded",
            }],
            "stability_reports": {},
        }
        with self.assertRaisesRegex(ValidationError, "bundle identity"):
            validate_campaign_ledger_v3(ledger, preregistration=preregistration)

    def test_failed_stability_report_is_not_registered(self) -> None:
        sample = synthetic_sample(self.policy)
        preregistration = self._preregistration(sample)
        report = self._clearance_report(preregistration, "reviewer-a")
        report["metrics"]["raw_model"]["finding_jaccard"] = 0.0
        report["metrics"]["raw_model"]["finding_union"] = 1
        report["checks"]["raw_finding_jaccard"] = False
        report["passed"] = False
        report["report_id"] = canonical_sha256({
            key: value for key, value in report.items() if key != "report_id"
        })
        with tempfile.TemporaryDirectory(prefix="quality-v3-registration-") as temporary:
            root = Path(temporary)
            ledger_path = (
                root / ".artifacts/i18n/quality/calibration-campaigns"
                / f"{preregistration['preregistration_id']}.json"
            )
            ledger_path.parent.mkdir(parents=True)
            ledger_path.write_text(json.dumps({
                "contract": "tome4-quality-calibration-campaign-ledger-v3",
                "schema_version": 3,
                "preregistration_id": preregistration["preregistration_id"],
                "external_transfer_limit": 8,
                "transfers": [], "stability_reports": {},
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "passed=true"):
                _register_campaign_stability_report(
                    root=root, preregistration=preregistration, report=report,
                )
            self.assertEqual(json.loads(ledger_path.read_text())["stability_reports"], {})

    def test_anchor_projection_rejects_phenomenon_drift(self) -> None:
        anchors = copy.deepcopy(self.anchors)
        anchors["anchors"][0]["phenomenon"] = "polarity"
        legacy = json.loads((self.manifest.root / "i18n/quality/anchors-v1.json").read_text())
        with patch("i18nlib.quality_v3._read_object", side_effect=[anchors, legacy]), self.assertRaises(ConfigurationError):
            load_anchors_v2(self.manifest, policy=self.policy, matrix=self.matrix)

    def test_v3_cache_identity_binds_every_frozen_input_and_not_v2(self) -> None:
        base = {
            "sample_id": "sample", "evaluator_id": "reviewer-a", "provider": "p",
            "model": "m", "thinking": "t", "prompt_sha256": "1" * 64,
            "policy_sha256": "2" * 64, "severity_matrix_sha256": "3" * 64,
            "anchors_sha256": "4" * 64, "bundle_ids": ["5" * 64],
            "bundle_sha256s": ["6" * 64], "strict": True, "clearance_id": "d" * 64,
        }
        original = _cache_key_v3(**base)
        for field, replacement in (
            ("sample_id", "other"), ("evaluator_id", "reviewer-b"), ("provider", "q"),
            ("model", "n"), ("thinking", "u"), ("prompt_sha256", "7" * 64),
            ("policy_sha256", "8" * 64), ("severity_matrix_sha256", "9" * 64),
            ("anchors_sha256", "a" * 64), ("bundle_ids", ["b" * 64]),
            ("bundle_sha256s", ["c" * 64]), ("strict", False),
            ("clearance_id", "e" * 64),
        ):
            changed = dict(base)
            changed[field] = replacement
            self.assertNotEqual(original, _cache_key_v3(**changed), field)
        v2 = _cache_key_v2(
            sample_id="sample", evaluator_id="reviewer-a", provider="p", model="m",
            thinking="t", prompt_sha256="1" * 64, rules_sha256="3" * 64,
            anchors_sha256="4" * 64, bundle_ids=["5" * 64], strict=True,
        )
        v1 = _cache_key(
            bundle_id="5" * 64, provider="p", model="m", thinking="t",
            prompt_sha256="1" * 64, strict=True,
        )
        self.assertNotEqual(original, v2)
        self.assertNotEqual(original, v1)
        self.assertNotEqual(v1, v2)

    def test_v2_projection_preserves_revision_order_and_only_v3_fields(self) -> None:
        sample = synthetic_sample(self.policy)
        old_items = []
        for index, item in enumerate(sample["items"]):
            old_items.append(
                {
                    "revision_id": item["revision_id"], "context_sufficient": True,
                    "profile_confirmed": "ui", "reuse_recommendation": "same-tag",
                    "findings": [] if index else [{
                        **finding(source_quote="source", target_quote="target"),
                        "defect_class": "semantic", "defect_summary": "legacy",
                        "meaning_change": {
                            "type": "reassigned", "summary": "legacy semantic delta",
                        },
                        "impact_facts": {}, "amplification_scope": "local",
                        "closest_anchor_id": None, "anchor_relation": "unknown",
                        "body": "legacy body", "evidence_refs": [],
                    }],
                }
            )
        old = {"items": old_items}
        projected = replay_assessment_v2_as_v3(
            old, sample_v3=sample,
            evaluator_v3=evaluator(self.policy, self.matrix, self.anchors),
        )
        self.assertEqual([item["revision_id"] for item in projected["items"]], sample["revisions"])
        self.assertEqual(
            set(projected["items"][0]["findings"][0]),
            {"finding_id", "error_code", "phenomenon", "meaning_change", "source_evidence", "target_evidence", "explanation"},
        )

    def test_fake_runner_auto_selects_v3_and_merges_two_shards(self) -> None:
        sample = synthetic_sample(self.policy)
        with tempfile.TemporaryDirectory(prefix="quality-v3-runner-") as temporary:
            path = Path(temporary) / "sample.json"
            path.write_text(json.dumps(sample), encoding="utf-8")
            preregistration_path = Path(temporary) / "preregistration.json"
            preregistration_path.write_text(json.dumps(self._preregistration(sample)), encoding="utf-8")
            outputs = []
            for shard_index, subset in enumerate((sample["items"][:20], sample["items"][20:])):
                items = [model_item(item["revision_id"]) for item in subset]
                if shard_index == 1:
                    items[0] = model_item(
                        subset[0]["revision_id"],
                        [finding(
                            source_quote=subset[0]["source"],
                            target_quote=subset[0]["target"],
                        )],
                    )
                outputs.append(subprocess.CompletedProcess([], 0, json.dumps({"items": items}).encode(), b""))
            with (
                patch("i18nlib.pi_quality._run_file_review_process", side_effect=outputs),
                patch("i18nlib.pi_quality._update_campaign_transfer", return_value={}),
            ):
                report = run_pi_quality_evaluator(
                    sample_path=path, evaluator_id="reviewer-a", provider="fake",
                    model="fake", thinking="none", use_cache=False, pi_executable="fake-pi",
                    preregistration_path=preregistration_path, run_number=1,
                )
        self.assertEqual((report["mode"], report["shards"], report["findings"]), ("blind-quality-assessment-v3", 2, 1))
        self.assertEqual(len(report["bundle_sha256s"]), 2)

    def test_assessment_content_failure_marks_all_claimed_transfers_failed(self) -> None:
        sample = synthetic_sample(self.policy)
        with tempfile.TemporaryDirectory(prefix="quality-v3-content-failure-") as temporary:
            root = Path(temporary)
            sample_path = root / "sample.json"
            preregistration_path = root / "preregistration.json"
            ledger_path = root / "ledger.json"
            sample_path.write_text(json.dumps(sample), encoding="utf-8")
            preregistration_path.write_text(
                json.dumps(self._preregistration(sample)), encoding="utf-8"
            )
            outputs = []
            for shard_index, subset in enumerate((sample["items"][:20], sample["items"][20:])):
                items = [model_item(item["revision_id"]) for item in subset]
                if shard_index == 1:
                    invalid = finding(
                        source_quote=subset[0]["source"], target_quote=subset[0]["target"],
                    )
                    invalid["severity"] = "major"
                    items[0] = model_item(subset[0]["revision_id"], [invalid])
                outputs.append(subprocess.CompletedProcess(
                    [], 0, json.dumps({"items": items}).encode(), b"",
                ))
            with (
                patch("i18nlib.pi_quality._run_file_review_process", side_effect=outputs),
                patch("i18nlib.pi_quality._campaign_ledger_path", return_value=ledger_path),
                self.assertRaises(AgentError),
            ):
                run_pi_quality_evaluator(
                    sample_path=sample_path, evaluator_id="reviewer-a", provider="fake",
                    model="fake", thinking="none", use_cache=False, pi_executable="fake-pi",
                    preregistration_path=preregistration_path, run_number=1,
                )
            ledger = json.loads(ledger_path.read_text())
            self.assertEqual([entry["state"] for entry in ledger["transfers"]], ["failed", "failed"])

    def test_holdout_clearance_failures_never_call_provider(self) -> None:
        calibration = synthetic_sample(self.policy)
        holdout = synthetic_sample(self.policy, kind="holdout")
        preregistration = self._preregistration(calibration)
        preregistration["frozen_inputs"]["holdout_sample_id"] = holdout["sample_id"]
        preregistration["frozen_inputs"]["holdout_sample_sha256"] = canonical_sha256(holdout)
        preregistration["preregistration_id"] = canonical_sha256({key: value for key, value in preregistration.items() if key != "preregistration_id"})
        valid = [
            self._clearance_report(preregistration, "reviewer-a"),
            self._clearance_report(preregistration, "reviewer-b"),
        ]
        failed = self._clearance_report(preregistration, "reviewer-b", passed=False)
        tampered = copy.deepcopy(valid[1])
        tampered["passed"] = False
        cases = (("missing", None), ("single", (valid[0],)), ("failed", (valid[0], failed)), ("tampered", (valid[0], tampered)))
        transfers = [
            {
                "evaluator_id": evaluator_id, "round": round_number,
                "execution_id": hashlib.sha256(
                    f"{evaluator_id}-{round_number}".encode()
                ).hexdigest(),
                "shard_index": shard_index,
                "bundle_id": preregistration["frozen_inputs"]["bundle_ids_by_evaluator"][evaluator_id][shard_index - 1],
                "state": "succeeded",
            }
            for evaluator_id in self.policy["evaluator_ids"]
            for round_number in (1, 2)
            for shard_index in (1, 2)
        ]
        ledger = {
            "contract": "tome4-quality-calibration-campaign-ledger-v3",
            "schema_version": 3,
            "preregistration_id": preregistration["preregistration_id"],
            "external_transfer_limit": 8,
            "transfers": transfers,
            "stability_reports": {
                report["evaluator"]["id"]: report["report_id"] for report in valid
            },
        }
        with tempfile.TemporaryDirectory(prefix="quality-v3-holdout-") as temporary:
            root = Path(temporary)
            sample_path = root / "holdout.json"
            preregistration_path = root / "preregistration.json"
            sample_path.write_text(json.dumps(holdout), encoding="utf-8")
            preregistration_path.write_text(json.dumps(preregistration), encoding="utf-8")
            for name, reports in cases:
                paths = None
                if reports is not None:
                    generated = []
                    for index, report in enumerate(reports):
                        path = root / f"{name}-{index}.json"
                        path.write_text(json.dumps(report), encoding="utf-8")
                        generated.append(path)
                    paths = tuple(generated)
                with (
                    self.subTest(name=name),
                    patch("i18nlib.pi_quality._run_file_review_process") as provider,
                    patch("i18nlib.pi_quality._load_campaign_ledger", return_value=ledger),
                ):
                    with self.assertRaises(ValidationError):
                        run_pi_quality_evaluator(
                            sample_path=sample_path, evaluator_id="reviewer-a", provider="fake",
                            model="fake", thinking="none", use_cache=False, pi_executable="fake-pi",
                            preregistration_path=preregistration_path,
                            stability_report_paths=paths,
                        )
                    provider.assert_not_called()
            valid_paths = []
            for index, report in enumerate(valid):
                path = root / f"valid-{index}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                valid_paths.append(path)
            unregistered_ledger = copy.deepcopy(ledger)
            unregistered_ledger["stability_reports"] = {}
            with (
                patch("i18nlib.pi_quality._run_file_review_process") as provider,
                patch(
                    "i18nlib.pi_quality._load_campaign_ledger",
                    return_value=unregistered_ledger,
                ),
                self.assertRaisesRegex(ValidationError, "not registered"),
            ):
                run_pi_quality_evaluator(
                    sample_path=sample_path, evaluator_id="reviewer-a", provider="fake",
                    model="fake", thinking="none", use_cache=False, pi_executable="fake-pi",
                    preregistration_path=preregistration_path,
                    stability_report_paths=tuple(valid_paths),
                )
            provider.assert_not_called()
            outputs = []
            for subset in (holdout["items"][:20], holdout["items"][20:]):
                outputs.append(subprocess.CompletedProcess(
                    [], 0,
                    json.dumps({"items": [model_item(item["revision_id"]) for item in subset]}).encode(),
                    b"",
                ))
            with (
                patch("i18nlib.pi_quality._run_file_review_process", side_effect=outputs) as provider,
                patch("i18nlib.pi_quality._load_campaign_ledger", return_value=ledger),
            ):
                report = run_pi_quality_evaluator(
                    sample_path=sample_path, evaluator_id="reviewer-a", provider="fake",
                    model="fake", thinking="none", use_cache=False, pi_executable="fake-pi",
                    preregistration_path=preregistration_path,
                    stability_report_paths=tuple(valid_paths),
                )
            self.assertTrue(report["ok"])
            self.assertEqual(provider.call_count, 2)

    def test_only_stability_v3_registers_campaign_clearance(self) -> None:
        registration_call = "_register_campaign_stability_report"
        self.assertNotIn(registration_call, inspect.getsource(_quality_stability_v2))
        self.assertIn(registration_call, inspect.getsource(_quality_stability_v3))

    def test_runner_rejects_unregistered_evaluator_configuration_before_provider(self) -> None:
        sample = synthetic_sample(self.policy)
        preregistration = self._preregistration(sample)
        with tempfile.TemporaryDirectory(prefix="quality-v3-runner-identity-") as temporary:
            root = Path(temporary)
            sample_path = root / "calibration.json"
            preregistration_path = root / "preregistration.json"
            sample_path.write_text(json.dumps(sample), encoding="utf-8")
            preregistration_path.write_text(json.dumps(preregistration), encoding="utf-8")
            with patch("i18nlib.pi_quality._run_file_review_process") as provider:
                with self.assertRaisesRegex(ValidationError, "differs from preregistration"):
                    run_pi_quality_evaluator(
                        sample_path=sample_path, evaluator_id="reviewer-a", provider="other",
                        model="fake", thinking="none", use_cache=False, pi_executable="fake-pi",
                        preregistration_path=preregistration_path, run_number=1,
                    )
                provider.assert_not_called()

    def test_stability_report_checks_are_rederived_from_metrics(self) -> None:
        sample = synthetic_sample(self.policy)
        preregistration = self._preregistration(sample)
        report = self._clearance_report(preregistration, "reviewer-a")
        report["metrics"]["raw_model"]["finding_jaccard"] = 0.0
        report["metrics"]["raw_model"]["finding_union"] = 1
        report["report_id"] = canonical_sha256({
            key: value for key, value in report.items() if key != "report_id"
        })
        with self.assertRaisesRegex(ValidationError, "frozen thresholds"):
            validate_stability_report_v3(report, preregistration=preregistration)

    def test_stability_keeps_raw_and_anchor_normalized_metrics_separate(self) -> None:
        anchored = sample_item(
            0,
            revision_id="22459090528963ac39578e508f9a0a169629550ed1345fb79f3a2907d2cc876c",
            source="molten rock", target="熔岩",
        )
        sample = synthetic_sample(self.policy, first=anchored)
        false_finding = finding(
            error_code="ACC_MISTRANSLATION", phenomenon="entity-role", meaning="reassigned",
            source_quote="molten rock", target_quote="熔岩",
        )
        bundles = build_evaluator_bundles_v3(
            sample=sample, evaluator_id="reviewer-a",
            policy=self.policy, matrix=self.matrix,
        )
        stability_evaluator = evaluator(self.policy, self.matrix, self.anchors)
        stability_evaluator.update(
            prompt_sha256=hashlib.sha256(
                load_evaluator_prompt_v3(self.manifest).encode()
            ).hexdigest(),
            bundle_ids=[bundle["bundle_id"] for bundle in bundles],
            bundle_sha256s=[canonical_sha256(bundle) for bundle in bundles],
        )
        items = [model_item(sample["items"][0]["revision_id"], [false_finding])]
        items.extend(model_item(item["revision_id"]) for item in sample["items"][1:])
        raw = build_assessment_v3(
            sample_id=sample["sample_id"], evaluator=stability_evaluator, items=items,
        )
        first = validate_assessment_v3(
            raw, sample=sample, policy=self.policy, matrix=self.matrix, anchors=self.anchors
        )
        second = validate_assessment_v3(
            copy.deepcopy(raw), sample=sample, policy=self.policy, matrix=self.matrix, anchors=self.anchors
        )
        identity = first["evaluator"]
        assessment_hashes = ("b" * 64, "b" * 64)
        preregistration = self._preregistration(sample)
        reports = []
        for round_number, assessment_hash in enumerate(assessment_hashes, start=1):
            runner = {
                "ok": True, "mode": "blind-quality-assessment-v3",
                "sample_id": sample["sample_id"], "evaluator_id": identity["id"],
                "provider": identity["provider"], "model": identity["model"],
                "thinking": identity["thinking"], "prompt_sha256": identity["prompt_sha256"],
                "policy_sha256": identity["policy_sha256"],
                "severity_matrix_sha256": identity["severity_matrix_sha256"],
                "anchors_sha256": identity["anchors_sha256"],
                "bundle_ids": identity["bundle_ids"], "bundle_sha256s": identity["bundle_sha256s"],
                "assessment_sha256": assessment_hash, "validated_results": 1,
                "cache_decision": "disabled", "shards": 2, "attempts": 2,
                "charged_or_possible_transfers": 2,
                "preregistration_id": preregistration["preregistration_id"],
                "round": round_number, "execution_id": str(round_number) * 64,
                "shard_transfers": [
                    {"shard_index": index, "bundle_id": bundle_id, "state": "succeeded"}
                    for index, bundle_id in enumerate(identity["bundle_ids"], start=1)
                ],
            }
            runner["runner_report_id"] = runner_report_semantic_identity_v3(runner)
            reports.append(runner)
        ledger = {
            "contract": "tome4-quality-calibration-campaign-ledger-v3",
            "schema_version": 3, "external_transfer_limit": 8,
            "preregistration_id": preregistration["preregistration_id"],
            "transfers": [
                {"evaluator_id": "reviewer-a", "round": round_number,
                 "execution_id": str(round_number) * 64, "shard_index": shard_index,
                 "bundle_id": identity["bundle_ids"][shard_index - 1], "state": "succeeded"}
                for round_number in (1, 2)
                for shard_index in (1, 2)
            ],
            "stability_reports": {},
        }
        report = build_stability_report_v3(
            sample=sample, assessments=(first, second), run_reports=(reports[0], reports[1]),
            assessment_sha256s=assessment_hashes, run_report_sha256s=("e" * 64, "f" * 64),
            preregistration=preregistration,
            campaign_ledger=ledger,
        )
        self.assertEqual(report["metrics"]["raw_model"]["finding_union"], 1)
        self.assertEqual(report["metrics"]["anchor_normalized"]["finding_union"], 0)
        self.assertTrue(report["passed"])
        with self.assertRaisesRegex(ValidationError, "distinct registered rounds"):
            build_stability_report_v3(
                sample=sample, assessments=(first, second),
                run_reports=(reports[0], copy.deepcopy(reports[0])),
                assessment_sha256s=assessment_hashes,
                run_report_sha256s=("e" * 64, "a" * 64),
                preregistration=preregistration, campaign_ledger=ledger,
            )

    def test_prompt_excludes_subjective_and_legacy_fields(self) -> None:
        prompt = load_evaluator_prompt_v3(self.manifest)
        self.assertIn("observable", prompt)
        self.assertIn("Do not choose severity", prompt)
        self.assertIn("impact_facts", prompt)
        self.assertNotIn("can_change_player_action", prompt)


if __name__ == "__main__":
    unittest.main()
