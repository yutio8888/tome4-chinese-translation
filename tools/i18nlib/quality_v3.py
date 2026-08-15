"""Offline translation-quality evaluator v3 primitives.

v3 deliberately leaves every v1/v2 artifact untouched.  Models report only
observable semantic deltas; this module validates their small vocabulary and
derives classification, technical facts, anchors, severity and manual queues.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

from .config import Manifest
from .errors import ConfigurationError, ValidationError
from .quality_v2 import (
    canonical_sha256,
    generate_calibration_holdout_v2,
    normalize_evidence,
    read_json_object,
    _sample_safety,
    validate_sample_v2,
)


METHOD_V3 = "mqm-pilot-v3"
POLICY_V3_FILE = "policy-v3.json"
SEVERITY_MATRIX_FILE = "severity-matrix-v1.json"
ANCHORS_V2_FILE = "anchors-v2.json"
ASSESSMENT_V3_CONTRACT = "tome4-quality-assessment-v3"
CALIBRATION_V3_CONTRACT = "tome4-quality-calibration-v3"
HOLDOUT_V3_CONTRACT = "tome4-quality-holdout-v3"
EVALUATOR_BUNDLE_V3_CONTRACT = "tome4-quality-evaluator-bundle-v3"
ISSUE_CLUSTER_V3_CONTRACT = "tome4-quality-issue-cluster-v3"
ADJUDICATION_VALIDATION_V3_CONTRACT = "tome4-quality-adjudication-validation-v3"
STABILITY_REPORT_V3_CONTRACT = "tome4-quality-stability-report-v3"
FIXED_SHARD_ITEMS_V3 = 20
ERROR_CODES_V3 = (
    "ACC_MISTRANSLATION", "ACC_OMISSION", "ACC_ADDITION", "ACC_UNTRANSLATED",
    "ACC_POLARITY", "ACC_CONDITION", "ACC_NUMBER_UNIT", "ACC_ENTITY_ROLE",
    "TERM_PREFERRED", "TERM_PROPER_NAME", "TERM_INCONSISTENT",
    "FLU_AMBIGUITY", "UI_CLARITY",
)
PHENOMENA_V3 = (
    "number", "number-range", "unit", "condition", "polarity", "entity-role",
    "scope", "trigger-timing", "omission", "addition", "terminology",
    "proper-name", "ambiguity", "other",
)
MEANING_CHANGES_V3 = (
    "omitted", "added", "weakened", "strengthened", "reversed", "reassigned",
    "made-ambiguous", "unknown",
)
DEFECT_CLASSES_V3 = ("semantic", "terminology", "ui", "technical")


def _read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except OSError as error:
        raise ConfigurationError(f"cannot read {label}: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(f"invalid {label}: {path}: {error}") from error
    if not isinstance(value, dict):
        raise ConfigurationError(f"{label} root must be an object")
    return value


def _exact_fields(value: dict[str, Any], expected: Iterable[str], where: str) -> None:
    expected_set = set(expected)
    unknown = sorted(set(value) - expected_set)
    missing = sorted(expected_set - set(value))
    if unknown:
        raise ValidationError(f"{where} has unknown fields: {', '.join(unknown)}")
    if missing:
        raise ValidationError(f"{where} is missing fields: {', '.join(missing)}")


def _string(value: Any, where: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        kind = "a string" if allow_empty else "a non-empty string"
        raise ValidationError(f"{where} must be {kind}")
    return value


def _enum(value: Any, allowed: Iterable[str], where: str) -> str:
    choices = set(allowed)
    if not isinstance(value, str) or value not in choices:
        raise ValidationError(f"{where} must be one of: {', '.join(sorted(choices))}")
    return value


def _sha(value: Any, where: str) -> str:
    text = _string(value, where)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise ValidationError(f"{where} must be a lowercase SHA-256")
    return text


def load_evaluator_prompt_v3(manifest: Manifest) -> str:
    prompt = manifest.root / "i18n" / "prompts" / "pi-quality-evaluator-v3.md"
    rubric = manifest.root / "i18n" / "quality" / "rubric-v3.md"
    try:
        return prompt.read_text(encoding="utf-8") + "\n\n---\n\n" + rubric.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ConfigurationError("cannot read Pi quality evaluator v3 prompt or rubric") from error


def load_policy_v3(manifest: Manifest) -> dict[str, Any]:
    policy = _read_object(manifest.root / "i18n" / "quality" / POLICY_V3_FILE, "quality v3 policy")
    _exact_fields(
        policy,
        (
            "contract", "schema_version", "method_version", "evaluator_ids",
            "assessment_states", "derivation_states", "severities",
            "allowed_error_codes", "phenomena", "meaning_change_types",
            "span_states", "cluster_types", "max_shard_items", "datasets",
            "stability_thresholds",
        ),
        "quality v3 policy",
    )
    if policy["contract"] != "tome4-quality-policy-v3" or policy["schema_version"] != 3:
        raise ConfigurationError("unsupported quality v3 policy contract")
    if policy["method_version"] != METHOD_V3:
        raise ConfigurationError(f"quality v3 method_version must be {METHOD_V3}")
    for field in (
        "evaluator_ids", "assessment_states", "derivation_states", "severities",
        "allowed_error_codes", "phenomena", "meaning_change_types", "span_states",
        "cluster_types",
    ):
        if not isinstance(policy[field], list) or not policy[field] or len(set(policy[field])) != len(policy[field]):
            raise ConfigurationError(f"quality v3 policy.{field} must be a unique non-empty array")
    if policy["assessment_states"] != ["assessed", "context-insufficient"]:
        raise ConfigurationError("quality v3 assessment states are frozen")
    if policy["evaluator_ids"] != ["reviewer-a", "reviewer-b"]:
        raise ConfigurationError("quality v3 evaluator ids are frozen")
    if set(policy["derivation_states"]) != {"derived", "provisional", "anchor-normalized", "gate-derived"}:
        raise ConfigurationError("quality v3 derivation states are frozen")
    if policy["severities"] != ["blocker", "major", "minor"]:
        raise ConfigurationError("quality v3 severities are frozen")
    for field, expected in (
        ("allowed_error_codes", ERROR_CODES_V3),
        ("phenomena", PHENOMENA_V3),
        ("meaning_change_types", MEANING_CHANGES_V3),
    ):
        if policy[field] != list(expected):
            raise ConfigurationError(f"quality v3 policy.{field} is frozen")
    if policy["max_shard_items"] != FIXED_SHARD_ITEMS_V3:
        raise ConfigurationError("quality v3 max_shard_items is frozen at 20")
    for kind, contract in (("calibration", CALIBRATION_V3_CONTRACT), ("holdout", HOLDOUT_V3_CONTRACT)):
        dataset = policy["datasets"].get(kind)
        if (
            not isinstance(dataset, dict)
            or set(dataset) != {"contract", "seed", "size"}
            or dataset.get("contract") != contract
            or dataset.get("seed") != f"tome4-quality-{kind}-v2"
            or dataset.get("size") != 32
        ):
            raise ConfigurationError(f"quality v3 policy.datasets.{kind} is invalid")
    expected_thresholds = {
        "schema_coverage": 1.0,
        "structure_failures_max": 0,
        "raw_finding_jaccard_min": 0.70,
        "phenomenon_meaning_agreement_min": 0.90,
        "normalized_provisional_severity_agreement_min": 0.90,
        "manual_queue_membership_agreement_min": 0.90,
        "host_technical_derivation_agreement": 1.0,
    }
    if policy["stability_thresholds"] != expected_thresholds:
        raise ConfigurationError("quality v3 stability thresholds are frozen")
    return policy


def load_severity_matrix(
    manifest: Manifest, policy: dict[str, Any] | None = None
) -> dict[str, Any]:
    policy = policy or load_policy_v3(manifest)
    matrix = _read_object(
        manifest.root / "i18n" / "quality" / SEVERITY_MATRIX_FILE,
        "quality v3 severity matrix",
    )
    _exact_fields(
        matrix,
        (
            "contract", "schema_version", "description", "error_code_phenomena",
            "phenomenon_meaning_changes", "error_code_classes",
            "automatic_major_phenomena", "automatic_major_meaning_changes",
            "unit_major_meaning_changes", "provisional_reason_codes",
        ),
        "quality v3 severity matrix",
    )
    if matrix["contract"] != "tome4-quality-severity-matrix-v1" or matrix["schema_version"] != 1:
        raise ConfigurationError("unsupported quality v3 severity matrix")
    codes = set(policy["allowed_error_codes"])
    phenomena = set(policy["phenomena"])
    meanings = set(policy["meaning_change_types"])
    if set(matrix["error_code_phenomena"]) != codes or set(matrix["error_code_classes"]) != codes:
        raise ConfigurationError("quality v3 matrix must classify every allowed error code exactly once")
    if set(matrix["phenomenon_meaning_changes"]) != phenomena:
        raise ConfigurationError("quality v3 matrix must classify every phenomenon exactly once")
    for code, values in matrix["error_code_phenomena"].items():
        if not isinstance(values, list) or not values or len(values) != len(set(values)) or not set(values).issubset(phenomena):
            raise ConfigurationError(f"quality v3 matrix error code {code} is invalid")
    for phenomenon, values in matrix["phenomenon_meaning_changes"].items():
        if not isinstance(values, list) or not values or len(values) != len(set(values)) or not set(values).issubset(meanings):
            raise ConfigurationError(f"quality v3 matrix phenomenon {phenomenon} is invalid")
    for field in (
        "automatic_major_phenomena", "automatic_major_meaning_changes",
        "unit_major_meaning_changes", "provisional_reason_codes",
    ):
        if not isinstance(matrix[field], list) or len(matrix[field]) != len(set(matrix[field])):
            raise ConfigurationError(f"quality v3 matrix.{field} must be a unique array")
    if set(matrix["automatic_major_phenomena"]) != {
        "number", "number-range", "condition", "polarity", "entity-role", "scope", "trigger-timing"
    }:
        raise ConfigurationError("quality v3 automatic-major phenomena are frozen")
    if set(matrix["automatic_major_meaning_changes"]) != meanings - {"unknown"}:
        raise ConfigurationError("quality v3 automatic-major meaning changes are frozen")
    if set(matrix["unit_major_meaning_changes"]) != meanings - {"omitted", "unknown"}:
        raise ConfigurationError("quality v3 unit-major meaning changes are frozen")
    expected_provisional_reasons = {
        "V3_MEANING_UNKNOWN", "V3_PHENOMENON_OTHER",
        "V3_SOURCE_EVIDENCE_AMBIGUOUS", "V3_SOURCE_EVIDENCE_MISSING",
        "V3_TARGET_EVIDENCE_AMBIGUOUS", "V3_TARGET_EVIDENCE_MISSING",
        "V3_CONTEXT_INSUFFICIENT", "V3_SEVERITY_BOUNDARY_DISAGREEMENT",
        "V3_HOST_DERIVATION_MISMATCH",
    }
    if set(matrix["provisional_reason_codes"]) != expected_provisional_reasons:
        raise ConfigurationError("quality v3 provisional reason codes are frozen")
    return matrix


def _normalized_signature(source: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": {key: source.get(key) for key in ("state", "start", "end")},
        "target": {key: target.get(key) for key in ("state", "start", "end")},
    }


def load_anchors_v2(
    manifest: Manifest,
    *,
    policy: dict[str, Any] | None = None,
    matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_policy_v3(manifest)
    matrix = matrix or load_severity_matrix(manifest, policy)
    anchors = _read_object(manifest.root / "i18n" / "quality" / ANCHORS_V2_FILE, "quality v3 anchors")
    _exact_fields(anchors, ("contract", "schema_version", "description", "anchors"), "quality v3 anchors")
    if anchors["contract"] != "tome4-quality-anchors-v2" or anchors["schema_version"] != 2:
        raise ConfigurationError("unsupported quality v3 anchors contract")
    if not isinstance(anchors["anchors"], list) or len(anchors["anchors"]) != 6:
        raise ConfigurationError("quality v3 anchors must contain the six projected anchors")
    legacy = _read_object(
        manifest.root / "i18n" / "quality" / "anchors-v1.json",
        "quality v2 anchor lineage",
    )
    legacy_by_id = {
        anchor.get("anchor_id"): anchor
        for anchor in legacy.get("anchors", [])
        if isinstance(anchor, dict)
    }
    fields = (
        "anchor_id", "classification", "source_contract", "source_sample_id",
        "revision_id", "adjudication_validation_id", "issue_ids", "profile",
        "error_code", "phenomenon", "meaning_change", "defect_class", "severity",
        "source_evidence", "target_evidence", "evidence_signature", "rationale",
    )
    seen: set[str] = set()
    positive = negative = 0
    for index, anchor in enumerate(anchors["anchors"]):
        where = f"quality v3 anchors[{index}]"
        if not isinstance(anchor, dict):
            raise ConfigurationError(f"{where} must be an object")
        try:
            _exact_fields(anchor, fields, where)
            anchor_id = _string(anchor["anchor_id"], f"{where}.anchor_id")
            if anchor_id in seen:
                raise ValidationError("quality v3 anchor ids must be unique")
            seen.add(anchor_id)
            classification = _enum(anchor["classification"], ("positive", "negative"), f"{where}.classification")
            positive += classification == "positive"
            negative += classification == "negative"
            if anchor["source_contract"] != "tome4-quality-calibration-v2":
                raise ValidationError(f"{where}.source_contract must preserve calibration-v2 lineage")
            legacy_anchor = legacy_by_id.get(anchor_id)
            if legacy_anchor is None:
                raise ValidationError(f"{where} has no anchors-v1 lineage")
            for field in ("source_sample_id", "revision_id", "adjudication_validation_id", "evidence_signature"):
                _sha(anchor[field], f"{where}.{field}")
            if (
                not isinstance(anchor["issue_ids"], list)
                or not anchor["issue_ids"]
                or len(anchor["issue_ids"]) != len(set(anchor["issue_ids"]))
                or any(
                    not isinstance(issue_id, str)
                    or len(issue_id) != 7
                    or not issue_id.startswith("QI-")
                    or not issue_id[3:].isdigit()
                    for issue_id in anchor["issue_ids"]
                )
            ):
                raise ValidationError(f"{where}.issue_ids must be non-empty")
            code = _enum(anchor["error_code"], policy["allowed_error_codes"], f"{where}.error_code")
            phenomenon = _enum(anchor["phenomenon"], policy["phenomena"], f"{where}.phenomenon")
            meaning = _enum(anchor["meaning_change"], policy["meaning_change_types"], f"{where}.meaning_change")
            if phenomenon not in matrix["error_code_phenomena"][code] or meaning not in matrix["phenomenon_meaning_changes"][phenomenon]:
                raise ValidationError(f"{where} has an incompatible classification")
            if anchor["defect_class"] != matrix["error_code_classes"][code]:
                raise ValidationError(f"{where}.defect_class is not host-reproducible")
            if classification == "positive" and anchor["severity"] not in policy["severities"]:
                raise ValidationError(f"{where}.severity must be set for a positive anchor")
            if classification == "negative" and anchor["severity"] is not None:
                raise ValidationError(f"{where}.severity must be null for a negative anchor")
            for side in ("source_evidence", "target_evidence"):
                evidence = anchor[side]
                if not isinstance(evidence, dict) or set(evidence) != {"quote", "occurrence"}:
                    raise ValidationError(f"{where}.{side} is invalid")
                _string(evidence["quote"], f"{where}.{side}.quote")
                if type(evidence["occurrence"]) is not int or evidence["occurrence"] < 1:
                    raise ValidationError(f"{where}.{side}.occurrence must be positive")
            _string(anchor["rationale"], f"{where}.rationale")
            expected_lineage = {
                "source_contract": legacy_anchor.get("source_contract"),
                "source_sample_id": legacy_anchor.get("sample_id"),
                "revision_id": legacy_anchor.get("revision_id"),
                "adjudication_validation_id": legacy_anchor.get("adjudication_validation_id"),
                "issue_ids": legacy_anchor.get("issue_ids"),
                "profile": legacy_anchor.get("profile"),
                "defect_class": legacy_anchor.get("defect_class"),
                "rationale": legacy_anchor.get("rationale"),
                "classification": "negative" if legacy_anchor.get("derived_severity") == "note" else "positive",
                "severity": None if legacy_anchor.get("derived_severity") == "note" else legacy_anchor.get("derived_severity"),
                "phenomenon": legacy_anchor.get("phenomenon"),
            }
            if any(anchor[field] != expected for field, expected in expected_lineage.items()):
                raise ValidationError(f"{where} does not losslessly preserve anchors-v1 lineage")
        except ValidationError as error:
            raise ConfigurationError(str(error)) from error
    if set(seen) != set(legacy_by_id):
        raise ConfigurationError("quality v3 anchor ids do not exactly project anchors-v1")
    if (positive, negative) != (2, 4):
        raise ConfigurationError("quality v3 anchor projection must preserve two positive and four negative anchors")
    return anchors


def _host_gate_derivation(gate_signals: Any) -> dict[str, Any]:
    if not isinstance(gate_signals, dict):
        return {
            "runtime_broken": False,
            "single_item_display_broken": False,
            "severity": None,
            "derivation_state": None,
            "reason_codes": [],
        }
    runtime_broken = any(
        (
            gate_signals.get("lua_load_valid") is False,
            gate_signals.get("format_signature_match") is False,
            gate_signals.get("markup_multiset_match") is False,
            gate_signals.get("at_token_multiset_match") is False,
            gate_signals.get("runtime_collision") is True,
            gate_signals.get("empty_target") is True,
        )
    )
    display_broken = not runtime_broken and gate_signals.get("format_shape_match") is False
    if runtime_broken:
        return {
            "runtime_broken": True, "single_item_display_broken": False,
            "severity": "blocker", "derivation_state": "gate-derived",
            "reason_codes": ["V3_GATE_RUNTIME_BROKEN"],
        }
    if display_broken:
        return {
            "runtime_broken": False, "single_item_display_broken": True,
            "severity": "major", "derivation_state": "gate-derived",
            "reason_codes": ["V3_GATE_DISPLAY_BROKEN"],
        }
    return {
        "runtime_broken": False, "single_item_display_broken": False,
        "severity": None, "derivation_state": None, "reason_codes": [],
    }


def derive_severity_v3(
    *,
    error_code: str,
    phenomenon: str,
    meaning_change: str,
    source_evidence_state: str = "exact",
    target_evidence_state: str = "exact",
    assessment_state: str = "assessed",
    gate_signals: dict[str, Any] | None = None,
    policy: dict[str, Any],
    matrix: dict[str, Any],
    anchor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply the frozen v3 precedence without subjective impact questions."""
    code = _enum(error_code, policy["allowed_error_codes"], "error_code")
    phenomenon = _enum(phenomenon, policy["phenomena"], "phenomenon")
    meaning_change = _enum(meaning_change, policy["meaning_change_types"], "meaning_change")
    _enum(source_evidence_state, policy["span_states"], "source_evidence_state")
    _enum(target_evidence_state, policy["span_states"], "target_evidence_state")
    _enum(assessment_state, policy["assessment_states"], "assessment_state")
    if phenomenon not in matrix["error_code_phenomena"][code]:
        raise ValidationError(f"incompatible error_code/phenomenon: {code}/{phenomenon}")
    if meaning_change not in matrix["phenomenon_meaning_changes"][phenomenon]:
        raise ValidationError(f"incompatible phenomenon/meaning_change: {phenomenon}/{meaning_change}")
    gate = _host_gate_derivation(gate_signals)
    if gate["severity"] is not None:
        return {
            "defect_class": "technical", "derived_severity": gate["severity"],
            "derivation_state": gate["derivation_state"], "requires_adjudication": False,
            "reason_codes": gate["reason_codes"], "host_gate": gate,
            "anchor_id": None, "anchor_conflict": False,
        }
    if anchor is not None and anchor.get("classification") == "positive":
        conflict = any(
            (
                anchor["error_code"] != code,
                anchor["phenomenon"] != phenomenon,
                anchor["meaning_change"] != meaning_change,
            )
        )
        return {
            "defect_class": anchor["defect_class"],
            "derived_severity": anchor["severity"],
            "derivation_state": "anchor-normalized", "requires_adjudication": False,
            "reason_codes": ["V3_POSITIVE_ANCHOR"], "host_gate": gate,
            "anchor_id": anchor["anchor_id"], "anchor_conflict": conflict,
        }
    reasons: list[str] = []
    if meaning_change == "unknown":
        reasons.append("V3_MEANING_UNKNOWN")
    if phenomenon == "other":
        reasons.append("V3_PHENOMENON_OTHER")
    for side, state in (("SOURCE", source_evidence_state), ("TARGET", target_evidence_state)):
        if state == "ambiguous":
            reasons.append(f"V3_{side}_EVIDENCE_AMBIGUOUS")
        elif state == "missing":
            legal_omission = side == "TARGET" and meaning_change == "omitted"
            if not legal_omission:
                reasons.append(f"V3_{side}_EVIDENCE_MISSING")
    if assessment_state == "context-insufficient":
        reasons.append("V3_CONTEXT_INSUFFICIENT")
    if reasons:
        return {
            "defect_class": matrix["error_code_classes"][code],
            "derived_severity": "minor", "derivation_state": "provisional",
            "requires_adjudication": True, "reason_codes": reasons,
            "host_gate": gate, "anchor_id": None, "anchor_conflict": False,
        }
    major = (
        phenomenon in matrix["automatic_major_phenomena"]
        and meaning_change in matrix["automatic_major_meaning_changes"]
    ) or (
        phenomenon == "unit" and meaning_change in matrix["unit_major_meaning_changes"]
    )
    return {
        "defect_class": matrix["error_code_classes"][code],
        "derived_severity": "major" if major else "minor",
        "derivation_state": "derived", "requires_adjudication": False,
        "reason_codes": ["V3_MATRIX_MAJOR" if major else "V3_MATRIX_MINOR"],
        "host_gate": gate, "anchor_id": None, "anchor_conflict": False,
    }


def _matching_anchor(
    *,
    anchors: dict[str, Any],
    sample: dict[str, Any],
    sample_item: dict[str, Any],
    finding: dict[str, Any],
    source_evidence: dict[str, Any],
    target_evidence: dict[str, Any],
) -> dict[str, Any] | None:
    if sample.get("dataset_kind") != "calibration":
        return None
    signature = _normalized_signature(source_evidence, target_evidence)
    for anchor in anchors["anchors"]:
        if anchor["revision_id"] != sample_item["revision_id"]:
            continue
        anchor_source = normalize_evidence(
            anchor["source_evidence"], sample_item["source"], where=f"anchor {anchor['anchor_id']} source"
        )
        anchor_target = normalize_evidence(
            anchor["target_evidence"], sample_item["target"], where=f"anchor {anchor['anchor_id']} target"
        )
        anchor_signature = _normalized_signature(anchor_source, anchor_target)
        if canonical_sha256(anchor_signature) != anchor["evidence_signature"]:
            raise ConfigurationError(f"quality v3 anchor {anchor['anchor_id']} evidence signature is stale")
        if signature != anchor_signature:
            continue
        # Negative anchors reject the same known false classification, rather
        # than every conceivable issue that happens to cover the same text.
        if anchor["classification"] == "negative" and any(
            (
                finding["error_code"] != anchor["error_code"],
                finding["phenomenon"] != anchor["phenomenon"],
                finding["meaning_change"] != anchor["meaning_change"],
            )
        ):
            continue
        return anchor
    return None


def _validate_finding_v3(
    finding: Any,
    *,
    sample: dict[str, Any],
    sample_item: dict[str, Any],
    assessment_state: str,
    policy: dict[str, Any],
    matrix: dict[str, Any],
    anchors: dict[str, Any],
    where: str,
) -> dict[str, Any]:
    if not isinstance(finding, dict):
        raise ValidationError(f"{where} must be an object")
    _exact_fields(
        finding,
        (
            "finding_id", "error_code", "phenomenon", "meaning_change",
            "source_evidence", "target_evidence", "explanation",
        ),
        where,
    )
    _string(finding["finding_id"], f"{where}.finding_id")
    code = _enum(finding["error_code"], policy["allowed_error_codes"], f"{where}.error_code")
    phenomenon = _enum(finding["phenomenon"], policy["phenomena"], f"{where}.phenomenon")
    meaning_type = _enum(
        finding["meaning_change"], policy["meaning_change_types"],
        f"{where}.meaning_change",
    )
    _string(finding["explanation"], f"{where}.explanation")
    source = normalize_evidence(finding["source_evidence"], sample_item["source"], where=f"{where}.source_evidence")
    target = normalize_evidence(
        finding["target_evidence"], sample_item["target"],
        where=f"{where}.target_evidence", allow_empty_omission=meaning_type == "omitted",
    )
    anchor = _matching_anchor(
        anchors=anchors, sample=sample, sample_item=sample_item, finding=finding,
        source_evidence=source, target_evidence=target,
    )
    if anchor is not None and anchor["classification"] == "negative":
        # Compatibility is still validated first: anchors cannot rescue invalid
        # model output or turn it into an adjudication item.
        derive_severity_v3(
            error_code=code, phenomenon=phenomenon, meaning_change=meaning_type,
            source_evidence_state=source["state"], target_evidence_state=target["state"],
            assessment_state=assessment_state,
            policy=policy, matrix=matrix,
        )
        return {
            **finding, "normalized_source_evidence": source,
            "normalized_target_evidence": target, "accepted": False,
            "anchor_decision": "rejected", "anchor_id": anchor["anchor_id"],
            "normalized_error_code": code,
            "normalized_phenomenon": phenomenon,
            "normalized_meaning_change": meaning_type,
            "derivation": None,
        }
    derivation = derive_severity_v3(
        error_code=code, phenomenon=phenomenon, meaning_change=meaning_type,
        source_evidence_state=source["state"], target_evidence_state=target["state"],
        assessment_state=assessment_state,
        policy=policy, matrix=matrix, anchor=anchor,
    )
    return {
        **finding, "normalized_source_evidence": source,
        "normalized_target_evidence": target, "accepted": True,
        "anchor_decision": "normalized" if anchor is not None else "none",
        "anchor_id": anchor["anchor_id"] if anchor is not None else None,
        "normalized_error_code": anchor["error_code"] if anchor is not None else code,
        "normalized_phenomenon": anchor["phenomenon"] if anchor is not None else phenomenon,
        "normalized_meaning_change": anchor["meaning_change"] if anchor is not None else meaning_type,
        "derivation": derivation,
    }


def assessment_identity_v3(assessment: dict[str, Any]) -> str:
    return canonical_sha256(
        {
            "schema_version": assessment.get("schema_version"),
            "quality_contract": assessment.get("quality_contract"),
            "sample_id": assessment.get("sample_id"),
            "evaluator": assessment.get("evaluator"),
            "items": assessment.get("items"),
        }
    )


def _validate_evaluator_v3(value: Any, policy: dict[str, Any], where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    fields = (
        "kind", "id", "method_version", "provider", "model", "thinking",
        "prompt_sha256", "policy_sha256", "severity_matrix_sha256",
        "anchors_sha256", "bundle_ids", "bundle_sha256s",
    )
    _exact_fields(value, fields, where)
    if value["kind"] != "model" or value["method_version"] != METHOD_V3:
        raise ValidationError(f"{where} is not a model {METHOD_V3} evaluator")
    _enum(value["id"], policy["evaluator_ids"], f"{where}.id")
    for field in ("provider", "model", "thinking"):
        _string(value[field], f"{where}.{field}")
    for field in ("prompt_sha256", "policy_sha256", "severity_matrix_sha256", "anchors_sha256"):
        _sha(value[field], f"{where}.{field}")
    for field in ("bundle_ids", "bundle_sha256s"):
        if (
            not isinstance(value[field], list)
            or len(value[field]) != 2
            or len(set(value[field])) != 2
        ):
            raise ValidationError(f"{where}.{field} must contain two unique shard identities")
        for index, item in enumerate(value[field]):
            _sha(item, f"{where}.{field}[{index}]")
    if len(value["bundle_ids"]) != len(value["bundle_sha256s"]):
        raise ValidationError(f"{where} bundle id/hash counts differ")
    return value


def validate_assessment_v3(
    assessment: dict[str, Any],
    *,
    sample: dict[str, Any],
    policy: dict[str, Any],
    matrix: dict[str, Any],
    anchors: dict[str, Any],
    expected_evaluator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(assessment, dict):
        raise ValidationError("quality v3 assessment must be an object")
    _exact_fields(
        assessment,
        ("schema_version", "quality_contract", "sample_id", "assessment_id", "evaluator", "items"),
        "quality v3 assessment",
    )
    if assessment["schema_version"] != 3 or assessment["quality_contract"] != ASSESSMENT_V3_CONTRACT:
        raise ValidationError("unsupported quality v3 assessment contract")
    if assessment["sample_id"] != sample.get("sample_id"):
        raise ValidationError("quality v3 assessment sample_id does not match")
    evaluator = _validate_evaluator_v3(assessment["evaluator"], policy, "quality v3 assessment.evaluator")
    if expected_evaluator is not None and evaluator != expected_evaluator:
        raise ValidationError("quality v3 assessment evaluator identity is host-owned and does not match")
    sample_items = sample.get("items")
    items = assessment["items"]
    if not isinstance(sample_items, list) or not sample_items:
        raise ValidationError("quality v3 sample has no items")
    if not isinstance(items, list) or len(items) != len(sample_items):
        raise ValidationError("quality v3 assessment must cover every sample item")
    normalized_items = []
    finding_ids: set[str] = set()
    for index, (item, sample_item) in enumerate(zip(items, sample_items)):
        where = f"quality v3 assessment.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(item, ("revision_id", "assessment_state", "findings"), where)
        if item["revision_id"] != sample_item.get("revision_id"):
            raise ValidationError(f"{where}.revision_id is missing, duplicate, or out of order")
        state = _enum(item["assessment_state"], policy["assessment_states"], f"{where}.assessment_state")
        if not isinstance(item["findings"], list):
            raise ValidationError(f"{where}.findings must be an array")
        raw_findings = []
        accepted = []
        rejected = []
        for finding_index, finding in enumerate(item["findings"]):
            normalized = _validate_finding_v3(
                finding, sample=sample, sample_item=sample_item, assessment_state=state,
                policy=policy, matrix=matrix, anchors=anchors,
                where=f"{where}.findings[{finding_index}]",
            )
            finding_id = normalized["finding_id"]
            if finding_id in finding_ids:
                raise ValidationError(f"duplicate quality v3 finding_id: {finding_id}")
            finding_ids.add(finding_id)
            raw_findings.append(normalized)
            (accepted if normalized["accepted"] else rejected).append(normalized)
        normalized_items.append(
            {
                **item,
                "raw_findings": raw_findings,
                "findings": accepted,
                "anchor_rejections": rejected,
                "host_gate_derivation": _host_gate_derivation(sample_item.get("gate_signals")),
            }
        )
    if assessment["assessment_id"] != assessment_identity_v3(assessment):
        raise ValidationError("quality v3 assessment_id does not match canonical content")
    return {**assessment, "items": normalized_items}


def build_assessment_v3(*, sample_id: str, evaluator: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    assessment = {
        "schema_version": 3,
        "quality_contract": ASSESSMENT_V3_CONTRACT,
        "sample_id": sample_id,
        "assessment_id": "",
        "evaluator": evaluator,
        "items": items,
    }
    assessment["assessment_id"] = assessment_identity_v3(assessment)
    return assessment


def replay_assessment_v2_as_v3(
    assessment_v2: dict[str, Any],
    *,
    sample_v3: dict[str, Any],
    evaluator_v3: dict[str, Any],
) -> dict[str, Any]:
    """Losslessly replay the v3-visible subset of a historical v2 run.

    This is deliberately an offline migration helper, not a reinterpretation
    of the v2 artifact.  Legacy host-owned fields are discarded and only
    findings already emitted by the model are projected.
    """
    v2_items = assessment_v2.get("items")
    if not isinstance(v2_items, list) or len(v2_items) != len(sample_v3.get("items", [])):
        raise ValidationError("historical v2 assessment cannot cover the v3 sample")
    if [item.get("revision_id") for item in v2_items] != sample_v3.get("revisions"):
        raise ValidationError("historical v2 assessment revision order differs from v3")
    projected = []
    for item in v2_items:
        findings = []
        for finding in item.get("findings", []):
            findings.append(
                {
                    "finding_id": finding["finding_id"],
                    "error_code": finding["error_code"],
                    "phenomenon": finding["phenomenon"],
                    "meaning_change": finding["meaning_change"]["type"],
                    "source_evidence": finding["source_evidence"],
                    "target_evidence": finding["target_evidence"],
                    "explanation": finding["body"],
                }
            )
        projected.append(
            {
                "revision_id": item["revision_id"],
                "assessment_state": "assessed" if item.get("context_sufficient", True) else "context-insufficient",
                "findings": findings,
            }
        )
    return build_assessment_v3(
        sample_id=sample_v3["sample_id"], evaluator=evaluator_v3, items=projected
    )


def project_sample_v3(
    sample_v2: dict[str, Any], *, policy_v3: dict[str, Any]
) -> dict[str, Any]:
    validate_sample_v2(sample_v2)
    kind = sample_v2["dataset_kind"]
    if kind not in ("calibration", "holdout"):
        raise ValidationError("quality v3 projection accepts calibration/holdout v2 only")
    identity = {
        "schema_version": 3,
        "quality_contract": policy_v3["datasets"][kind]["contract"],
        "dataset_kind": kind,
        "seed": sample_v2["seed"],
        "size": sample_v2["size"],
        "taxonomy_sha256": sample_v2["taxonomy_sha256"],
        "policy_v1_sha256": sample_v2["policy_v1_sha256"],
        "policy_v2_sha256": sample_v2["policy_v2_sha256"],
        "policy_v3_sha256": canonical_sha256(policy_v3),
        "manifest_sha256": sample_v2["manifest_sha256"],
        "inventory_sha256": sample_v2["inventory_sha256"],
        "excluded_ids_sha256": sample_v2["excluded_ids_sha256"],
        "source_sample_v2_id": sample_v2["sample_id"],
        "items_sha256": sample_v2["items_sha256"],
        "revisions": sample_v2["revisions"],
    }
    return {
        **identity,
        "sample_id": canonical_sha256(identity),
        "coverage": sample_v2["coverage"],
        "items": sample_v2["items"],
    }


def validate_sample_v3(sample: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(sample, dict):
        raise ValidationError("quality v3 sample must be an object")
    fields = {
        "schema_version", "quality_contract", "dataset_kind", "seed", "size",
        "taxonomy_sha256", "policy_v1_sha256", "policy_v2_sha256", "policy_v3_sha256",
        "manifest_sha256", "inventory_sha256", "excluded_ids_sha256", "source_sample_v2_id",
        "items_sha256", "revisions", "sample_id", "coverage", "items",
    }
    _exact_fields(sample, fields, "quality v3 sample")
    if sample["schema_version"] != 3 or sample["quality_contract"] not in {CALIBRATION_V3_CONTRACT, HOLDOUT_V3_CONTRACT}:
        raise ValidationError("unsupported quality v3 sample contract")
    kind = sample["dataset_kind"]
    expected_contract = CALIBRATION_V3_CONTRACT if kind == "calibration" else HOLDOUT_V3_CONTRACT if kind == "holdout" else None
    if sample["quality_contract"] != expected_contract:
        raise ValidationError("quality v3 sample dataset kind/contract differ")
    expected_dataset = policy["datasets"][kind] if policy is not None else {
        "contract": expected_contract, "seed": f"tome4-quality-{kind}-v2", "size": 32,
    }
    if sample["seed"] != expected_dataset["seed"]:
        raise ValidationError("quality v3 sample seed is not the frozen value")
    if sample["size"] != expected_dataset["size"] or not isinstance(sample["items"], list) or len(sample["items"]) != 32:
        raise ValidationError("quality v3 calibration/holdout samples must have 32 items")
    for field in (
        "taxonomy_sha256", "policy_v1_sha256", "policy_v2_sha256", "policy_v3_sha256",
        "manifest_sha256", "inventory_sha256", "excluded_ids_sha256", "source_sample_v2_id",
        "items_sha256", "sample_id",
    ):
        _sha(sample[field], f"quality v3 sample.{field}")
    if not isinstance(sample["coverage"], dict) or any(
        not isinstance(key, str) or not key or type(value) is not int or value < 0
        for key, value in sample["coverage"].items()
    ):
        raise ValidationError("quality v3 sample.coverage must map names to non-negative integers")
    item_fields = {
        "args_order", "bucket", "component", "context_neighbors", "contrast_group",
        "contrast_siblings", "domain_hints", "gate_signals", "index", "profile",
        "profile_confidence", "relevant_terms", "revision_id", "revision_uid",
        "risk_flags", "section", "source", "source_length_bin", "source_tag",
        "special", "structure", "target", "tu_uid", "unit_id",
    }
    gate_fields = {
        "at_token_multiset_match", "cross_component_variant", "empty_target",
        "format_shape_match", "format_signature_match", "lua_load_valid",
        "markup_multiset_match", "needs_review", "runtime_collision",
    }
    for index, item in enumerate(sample["items"]):
        where = f"quality v3 sample.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(item, item_fields, where)
        for field in ("revision_id", "revision_uid", "tu_uid", "unit_id"):
            _sha(item[field], f"{where}.{field}")
        for field in ("bucket", "component", "profile", "profile_confidence", "section", "source", "source_length_bin", "source_tag", "target"):
            _string(item[field], f"{where}.{field}", allow_empty=field in {"source_tag", "target"})
        if type(item["index"]) is not int or item["index"] != index:
            raise ValidationError(f"{where}.index must equal its sample position")
        for field in ("context_neighbors", "contrast_siblings", "domain_hints", "relevant_terms", "risk_flags"):
            if not isinstance(item[field], list):
                raise ValidationError(f"{where}.{field} must be an array")
        if item["contrast_group"] is not None and not isinstance(item["contrast_group"], str):
            raise ValidationError(f"{where}.contrast_group must be a string or null")
        if item["args_order"] is not None and not isinstance(item["args_order"], list):
            raise ValidationError(f"{where}.args_order must be an array or null")
        if item["special"] is not None and not isinstance(item["special"], (str, dict, list)):
            raise ValidationError(f"{where}.special has an invalid type")
        if not isinstance(item["structure"], dict):
            raise ValidationError(f"{where}.structure must be an object")
        gate = item["gate_signals"]
        if not isinstance(gate, dict):
            raise ValidationError(f"{where}.gate_signals must be an object")
        _exact_fields(gate, gate_fields, f"{where}.gate_signals")
        for field in gate_fields - {"needs_review"}:
            if gate[field] is not None and type(gate[field]) is not bool:
                raise ValidationError(f"{where}.gate_signals.{field} must be boolean or null")
        if not isinstance(gate["needs_review"], list) or any(not isinstance(value, str) for value in gate["needs_review"]):
            raise ValidationError(f"{where}.gate_signals.needs_review must be an array of strings")
    revisions = [item["revision_id"] for item in sample["items"]]
    if not isinstance(sample["revisions"], list) or any(not isinstance(value, str) for value in sample["revisions"]):
        raise ValidationError("quality v3 sample.revisions must be an array of SHA-256 strings")
    for index, revision in enumerate(sample["revisions"]):
        _sha(revision, f"quality v3 sample.revisions[{index}]")
    if revisions != sample["revisions"] or len(set(revisions)) != len(revisions):
        raise ValidationError("quality v3 sample revisions are incomplete, duplicated, or out of order")
    if canonical_sha256(sample["items"]) != sample["items_sha256"]:
        raise ValidationError("quality v3 sample item identity does not match")
    if policy is not None and sample["policy_v3_sha256"] != canonical_sha256(policy):
        raise ValidationError("quality v3 sample policy_v3_sha256 is stale")
    identity_keys = fields - {"sample_id", "coverage", "items"}
    identity = {key: sample[key] for key in identity_keys}
    if canonical_sha256(identity) != sample["sample_id"]:
        raise ValidationError("quality v3 sample_id does not match")
    _sample_safety(sample)
    return sample


def generate_calibration_holdout_v3(manifest: Manifest, inventory_path: Path) -> dict[str, Any]:
    generated = generate_calibration_holdout_v2(manifest, inventory_path)
    policy = load_policy_v3(manifest)
    return {
        "calibration": project_sample_v3(generated["calibration"], policy_v3=policy),
        "holdout": project_sample_v3(generated["holdout"], policy_v3=policy),
        "source_v2": generated,
    }


def run_calibration_v3(manifest: Manifest, inventory_path: Path) -> dict[str, Any]:
    from .quality import create_quality_run_directory
    from .report import write_json

    generated = generate_calibration_holdout_v3(manifest, inventory_path)
    run_directory = create_quality_run_directory(manifest.root, "calibration-v3")
    paths = {}
    for kind in ("calibration", "holdout"):
        path = run_directory / f"{kind}.json"
        write_json(path, generated[kind])
        paths[kind] = str(path)
    index = {
        "schema_version": 3,
        "quality_contract": "tome4-quality-dataset-index-v3",
        "calibration_id": generated["calibration"]["sample_id"],
        "holdout_id": generated["holdout"]["sample_id"],
        "source_sample_v2_ids": [
            generated["calibration"]["source_sample_v2_id"],
            generated["holdout"]["source_sample_v2_id"],
        ],
        "revisions_unchanged": all(
            generated[kind]["revisions"] == generated["source_v2"][kind]["revisions"]
            for kind in ("calibration", "holdout")
        ),
        "paths": paths,
        "run_directory": str(run_directory),
    }
    index["index_id"] = canonical_sha256(index)
    index_path = run_directory / "dataset-index.json"
    write_json(index_path, index)
    index["index"] = str(index_path)
    return index


def _shard_ranges(items: list[dict[str, Any]], max_items: int) -> list[tuple[int, int]]:
    groups: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(items):
        if item.get("contrast_group") is not None:
            groups[item["contrast_group"]].append(index)
    forbidden = {cut for positions in groups.values() for cut in range(min(positions) + 1, max(positions) + 1)}
    result = []
    start = 0
    while start < len(items):
        limit = min(len(items), start + max_items)
        allowed = [cut for cut in range(start + 1, limit + 1) if cut not in forbidden]
        if not allowed:
            raise ValidationError("a contrast group cannot fit within the shard item limit")
        end = max(allowed)
        result.append((start, end))
        start = end
    return result


def build_evaluator_bundles_v3(
    *,
    sample: dict[str, Any],
    evaluator_id: str,
    policy: dict[str, Any],
    matrix: dict[str, Any],
    max_items: int = FIXED_SHARD_ITEMS_V3,
) -> list[dict[str, Any]]:
    validate_sample_v3(sample, policy)
    _enum(evaluator_id, policy["evaluator_ids"], "evaluator_id")
    if max_items != FIXED_SHARD_ITEMS_V3:
        raise ValidationError("quality v3 shard size is frozen at 20")
    ranges = _shard_ranges(sample["items"], FIXED_SHARD_ITEMS_V3)
    if len(sample["items"]) == 32 and len(ranges) != 2:
        raise ValidationError("quality v3 32-item samples must produce exactly two shards")
    bundles = []
    for index, (first, end) in enumerate(ranges, start=1):
        bundle = {
            "schema_version": 3,
            "quality_contract": EVALUATOR_BUNDLE_V3_CONTRACT,
            "sample_contract": sample["quality_contract"],
            "sample_id": sample["sample_id"],
            "evaluator_id": evaluator_id,
            "finding_id_prefix": "A" if evaluator_id == "reviewer-a" else "B",
            "shard_index": index,
            "shard_count": len(ranges),
            "first_sample_index": first,
            "method_version": METHOD_V3,
            "assessment_states": policy["assessment_states"],
            "allowed_error_codes": policy["allowed_error_codes"],
            "phenomena": policy["phenomena"],
            "meaning_change_types": policy["meaning_change_types"],
            "compatibility_matrix": {
                "error_code_phenomena": matrix["error_code_phenomena"],
                "phenomenon_meaning_changes": matrix["phenomenon_meaning_changes"],
            },
            "items": sample["items"][first:end],
            "bundle_id": "",
        }
        bundle["bundle_id"] = canonical_sha256({key: value for key, value in bundle.items() if key != "bundle_id"})
        bundles.append(bundle)
    if [item["revision_id"] for bundle in bundles for item in bundle["items"]] != sample["revisions"]:
        raise ValidationError("quality v3 shards do not reconstruct sample order")
    return bundles


def run_evaluator_bundles_v3(
    manifest: Manifest, *, sample_path: Path, evaluator_id: str
) -> dict[str, Any]:
    from .quality import create_quality_run_directory
    from .report import write_json

    policy = load_policy_v3(manifest)
    matrix = load_severity_matrix(manifest, policy)
    sample = validate_sample_v3(read_json_object(sample_path, "quality v3 sample"), policy)
    bundles = build_evaluator_bundles_v3(
        sample=sample, evaluator_id=evaluator_id, policy=policy, matrix=matrix
    )
    run_directory = create_quality_run_directory(manifest.root, "evaluator-shards-v3")
    paths = []
    hashes = []
    for bundle in bundles:
        path = run_directory / f"shard-{bundle['shard_index']:03d}.json"
        write_json(path, bundle)
        paths.append(str(path))
        hashes.append(canonical_sha256(bundle))
    index = {
        "schema_version": 3, "quality_contract": "tome4-quality-evaluator-shard-index-v3",
        "sample_id": sample["sample_id"], "evaluator_id": evaluator_id,
        "max_items": FIXED_SHARD_ITEMS_V3, "shard_count": len(bundles),
        "bundle_ids": [bundle["bundle_id"] for bundle in bundles],
        "bundle_sha256s": hashes, "shards": paths, "run_directory": str(run_directory),
    }
    index["index_id"] = canonical_sha256(index)
    index_path = run_directory / "shard-index.json"
    write_json(index_path, index)
    index["index"] = str(index_path)
    return index


def _evidence_scope(finding: dict[str, Any]) -> tuple[Any, ...]:
    source = finding["normalized_source_evidence"]
    target = finding["normalized_target_evidence"]
    return (source.get("start"), source.get("end"), target.get("start"), target.get("end"))


def _spans_related(left: dict[str, Any], right: dict[str, Any]) -> bool:
    for side in ("normalized_source_evidence", "normalized_target_evidence"):
        a, b = left[side], right[side]
        if a["state"] not in {"exact", "whole-item"} or b["state"] not in {"exact", "whole-item"}:
            if a["state"] == b["state"] == "missing" and not a.get("quote") and not b.get("quote"):
                continue
            return False
        if max(a["start"], b["start"]) >= min(a["end"], b["end"]):
            return False
    return True


def _findings_compatible(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if not _spans_related(left, right):
        return False
    lp, rp = left["normalized_phenomenon"], right["normalized_phenomenon"]
    compatible = lp == rp or frozenset((lp, rp)) in {
        frozenset(("number", "number-range")),
        frozenset(("terminology", "proper-name")),
        frozenset(("omission", "unit")),
        frozenset(("ambiguity", "other")),
    }
    return compatible


def _member_v3(side: str, finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "side": side,
        "finding_id": finding["finding_id"],
        "error_code": finding["normalized_error_code"],
        "phenomenon": finding["normalized_phenomenon"],
        "meaning_change": finding["normalized_meaning_change"],
        "source_evidence": finding["normalized_source_evidence"],
        "target_evidence": finding["normalized_target_evidence"],
        "derivation": finding["derivation"],
        "anchor_decision": finding["anchor_decision"],
        "anchor_id": finding["anchor_id"],
    }


def _pair_derivation(left: dict[str, Any], right: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    ld, rd = left["derivation"], right["derivation"]
    boundary = {ld["derived_severity"], rd["derived_severity"]} == {"major", "minor"}
    classifications_agree = (
        left["normalized_phenomenon"] == right["normalized_phenomenon"]
        and left["normalized_meaning_change"] == right["normalized_meaning_change"]
        and left["normalized_error_code"] == right["normalized_error_code"]
    )
    provisional = ld["requires_adjudication"] or rd["requires_adjudication"] or boundary
    if boundary:
        result = {
            "defect_class": ld["defect_class"] if ld["defect_class"] == rd["defect_class"] else "semantic",
            "derived_severity": "minor", "derivation_state": "provisional",
            "requires_adjudication": True,
            "reason_codes": ["V3_SEVERITY_BOUNDARY_DISAGREEMENT"],
            "anchor_id": None, "anchor_conflict": False,
        }
    elif provisional:
        reasons = sorted(set(ld["reason_codes"] + rd["reason_codes"]))
        result = {
            "defect_class": ld["defect_class"], "derived_severity": "minor",
            "derivation_state": "provisional", "requires_adjudication": True,
            "reason_codes": reasons, "anchor_id": ld.get("anchor_id") or rd.get("anchor_id"),
            "anchor_conflict": ld.get("anchor_conflict", False) or rd.get("anchor_conflict", False),
        }
    elif ld["derived_severity"] == rd["derived_severity"]:
        result = dict(ld)
    else:
        # blocker/major differences can only originate in inconsistent host
        # inputs, which are not an evaluator judgment and must be surfaced.
        result = {
            "defect_class": "technical", "derived_severity": "minor",
            "derivation_state": "provisional", "requires_adjudication": True,
            "reason_codes": ["V3_HOST_DERIVATION_MISMATCH"],
            "anchor_id": None, "anchor_conflict": False,
        }
    manual = result["requires_adjudication"] or not classifications_agree
    return result, manual


def _multi_derivation(findings: list[dict[str, Any]]) -> dict[str, Any]:
    derivations = [finding["derivation"] for finding in findings]
    severities = {item["derived_severity"] for item in derivations}
    if severities == {"major", "minor"}:
        reasons = ["V3_SEVERITY_BOUNDARY_DISAGREEMENT"]
    elif any(item["requires_adjudication"] for item in derivations):
        reasons = sorted(
            set(reason for item in derivations for reason in item["reason_codes"])
        )
    elif len(severities) == 1:
        return dict(derivations[0])
    else:
        reasons = ["V3_HOST_DERIVATION_MISMATCH"]
    return {
        "defect_class": derivations[0]["defect_class"],
        "derived_severity": "minor",
        "derivation_state": "provisional",
        "requires_adjudication": True,
        "reason_codes": reasons,
        "anchor_id": next((item.get("anchor_id") for item in derivations if item.get("anchor_id")), None),
        "anchor_conflict": any(item.get("anchor_conflict", False) for item in derivations),
    }


def match_assessments_v3(
    *,
    sample: dict[str, Any],
    left_assessment: dict[str, Any],
    right_assessment: dict[str, Any],
    allow_identical_assessment: bool = False,
) -> dict[str, Any]:
    if left_assessment["sample_id"] != sample["sample_id"] or right_assessment["sample_id"] != sample["sample_id"]:
        raise ValidationError("quality v3 matching requires one sample identity")
    if left_assessment["assessment_id"] == right_assessment["assessment_id"] and not allow_identical_assessment:
        raise ValidationError("quality v3 matching requires two distinct assessments")
    pending = []
    raw_counts = Counter({"left": 0, "right": 0})
    normalized_counts = Counter({"left": 0, "right": 0})
    anchor_counts = Counter({"rejections": 0, "normalizations": 0})
    for sample_index, (sample_item, left_item, right_item) in enumerate(
        zip(sample["items"], left_assessment["items"], right_assessment["items"])
    ):
        revision = sample_item["revision_id"]
        if left_item["revision_id"] != revision or right_item["revision_id"] != revision:
            raise ValidationError("quality v3 matching found stale or out-of-order revision")
        raw_counts["left"] += len(left_item["raw_findings"])
        raw_counts["right"] += len(right_item["raw_findings"])
        normalized_counts["left"] += len(left_item["findings"])
        normalized_counts["right"] += len(right_item["findings"])
        anchor_counts["rejections"] += len(left_item["anchor_rejections"]) + len(right_item["anchor_rejections"])
        anchor_counts["normalizations"] += sum(
            finding["anchor_decision"] == "normalized"
            for finding in left_item["findings"] + right_item["findings"]
        )
        left = list(left_item["findings"])
        right = list(right_item["findings"])
        gate = left_item["host_gate_derivation"]
        if gate != right_item["host_gate_derivation"]:
            raise ValidationError("quality v3 host technical derivation differs between evaluators")
        if gate["severity"] is not None:
            # Gate truth is host-owned and completely precedes model issue
            # clustering.  Model findings remain in the normalized assessment
            # and raw metrics, but cannot be relabelled as technical findings.
            pending.append(
                {
                    "sample_index": sample_index, "revision_id": revision,
                    "cluster_type": "full-match", "members": [],
                    "derivation": {
                        "defect_class": "technical", "derived_severity": gate["severity"],
                        "derivation_state": "gate-derived", "requires_adjudication": False,
                        "reason_codes": gate["reason_codes"], "anchor_id": None,
                        "anchor_conflict": False,
                    },
                    "manual": False, "sort_start": -2,
                }
            )
            continue
        adjacency: dict[tuple[str, int], set[tuple[str, int]]] = defaultdict(set)
        for left_index, left_finding in enumerate(left):
            for right_index, right_finding in enumerate(right):
                if _findings_compatible(left_finding, right_finding):
                    left_node, right_node = ("left", left_index), ("right", right_index)
                    adjacency[left_node].add(right_node)
                    adjacency[right_node].add(left_node)
        nodes = [
            *(("left", index) for index in range(len(left))),
            *(("right", index) for index in range(len(right))),
        ]
        seen: set[tuple[str, int]] = set()
        for node in nodes:
            if node in seen:
                continue
            queue = deque([node])
            seen.add(node)
            component = []
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbor in sorted(adjacency[current]):
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
            left_findings = [left[index] for side, index in component if side == "left"]
            right_findings = [right[index] for side, index in component if side == "right"]
            all_findings = [*left_findings, *right_findings]
            if len(left_findings) == len(right_findings) == 1:
                exact = _evidence_scope(left_findings[0]) == _evidence_scope(right_findings[0])
                cluster_type = "full-match" if exact else "partial-match"
                derivation, manual = _pair_derivation(left_findings[0], right_findings[0])
            elif left_findings and right_findings and (len(left_findings) == 1 or len(right_findings) == 1):
                cluster_type = "split-merge"
                derivation, manual = _multi_derivation(all_findings), True
            elif left_findings and right_findings:
                cluster_type = "ambiguous"
                derivation, manual = _multi_derivation(all_findings), True
            elif left_findings:
                cluster_type = "left-only"
                derivation, manual = left_findings[0]["derivation"], True
            else:
                cluster_type = "right-only"
                derivation, manual = right_findings[0]["derivation"], True
            members = [
                *(_member_v3("left", finding) for finding in left_findings),
                *(_member_v3("right", finding) for finding in right_findings),
            ]
            starts = [
                finding["normalized_source_evidence"].get("start")
                for finding in all_findings
                if finding["normalized_source_evidence"].get("start") is not None
            ]
            pending.append(
                {
                    "sample_index": sample_index, "revision_id": revision,
                    "cluster_type": cluster_type, "members": members,
                    "derivation": derivation, "manual": manual,
                    "sort_start": min(starts) if starts else -1,
                }
            )
    pending.sort(key=lambda item: (item["sample_index"], item["sort_start"], item["cluster_type"]))
    issues = []
    manual_queue = []
    for index, pending_issue in enumerate(pending, start=1):
        issue = {
            "issue_id": f"Q3-{index:04d}",
            "revision_id": pending_issue["revision_id"],
            "cluster_type": pending_issue["cluster_type"],
            "members": pending_issue["members"],
            "derivation": pending_issue["derivation"],
            "requires_adjudication": pending_issue["manual"],
        }
        issues.append(issue)
        if pending_issue["manual"]:
            manual_queue.append(issue["issue_id"])
    raw_pairs, raw_union = _finding_pairs_for_stability(
        left_assessment, right_assessment, raw=True
    )
    raw_classification_agreement = sum(
        left["phenomenon"] == right["phenomenon"]
        and left["meaning_change"] == right["meaning_change"]
        for left, right in raw_pairs
    )
    artifact = {
        "schema_version": 3, "quality_contract": ISSUE_CLUSTER_V3_CONTRACT,
        "sample_id": sample["sample_id"], "sample_size": len(sample["items"]),
        "assessment_ids": [left_assessment["assessment_id"], right_assessment["assessment_id"]],
        "match_id": "", "issues": issues, "manual_queue": manual_queue,
        "raw_model_counts": dict(sorted(raw_counts.items())),
        "normalized_model_counts": dict(sorted(normalized_counts.items())),
        "raw_model_metrics": {
            "finding_union": raw_union,
            "finding_intersection": len(raw_pairs),
            "finding_jaccard": len(raw_pairs) / raw_union if raw_union else 1.0,
            "phenomenon_meaning_agreement": (
                raw_classification_agreement / len(raw_pairs) if raw_pairs else 1.0
            ),
        },
        "anchor_counts": dict(sorted(anchor_counts.items())),
    }
    artifact["match_id"] = canonical_sha256({key: value for key, value in artifact.items() if key != "match_id"})
    return artifact


def _validate_derivation_artifact(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    base = {
        "defect_class", "derived_severity", "derivation_state", "requires_adjudication",
        "reason_codes", "anchor_id", "anchor_conflict",
    }
    if set(value) not in (base, base | {"host_gate"}):
        _exact_fields(value, base, where)
    _enum(value["defect_class"], DEFECT_CLASSES_V3, f"{where}.defect_class")
    _enum(value["derived_severity"], ("blocker", "major", "minor"), f"{where}.derived_severity")
    _enum(value["derivation_state"], ("derived", "provisional", "anchor-normalized", "gate-derived"), f"{where}.derivation_state")
    if type(value["requires_adjudication"]) is not bool or type(value["anchor_conflict"]) is not bool:
        raise ValidationError(f"{where} boolean fields are invalid")
    if not isinstance(value["reason_codes"], list) or not value["reason_codes"] or any(not isinstance(code, str) for code in value["reason_codes"]):
        raise ValidationError(f"{where}.reason_codes must be a non-empty string array")
    if value["anchor_id"] is not None and not isinstance(value["anchor_id"], str):
        raise ValidationError(f"{where}.anchor_id must be a string or null")
    if "host_gate" in value and not isinstance(value["host_gate"], dict):
        raise ValidationError(f"{where}.host_gate must be an object")
    return value


def validate_match_v3(match: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(match, dict):
        raise ValidationError("quality v3 match must be an object")
    _exact_fields(
        match,
        (
            "schema_version", "quality_contract", "sample_id", "sample_size",
            "assessment_ids", "match_id", "issues", "manual_queue", "raw_model_counts",
            "normalized_model_counts", "raw_model_metrics", "anchor_counts",
        ),
        "quality v3 match",
    )
    if match["schema_version"] != 3 or match["quality_contract"] != ISSUE_CLUSTER_V3_CONTRACT:
        raise ValidationError("unsupported quality v3 match contract")
    _sha(match["sample_id"], "quality v3 match.sample_id")
    if type(match["sample_size"]) is not int or match["sample_size"] != 32:
        raise ValidationError("quality v3 match.sample_size must be 32")
    if not isinstance(match["assessment_ids"], list) or len(match["assessment_ids"]) != 2:
        raise ValidationError("quality v3 match.assessment_ids must contain two identities")
    for index, value in enumerate(match["assessment_ids"]):
        _sha(value, f"quality v3 match.assessment_ids[{index}]")
    for field in ("raw_model_counts", "normalized_model_counts"):
        counts = match[field]
        if not isinstance(counts, dict) or set(counts) != {"left", "right"} or any(type(value) is not int or value < 0 for value in counts.values()):
            raise ValidationError(f"quality v3 match.{field} is invalid")
    metrics = match["raw_model_metrics"]
    _exact_fields(metrics, ("finding_union", "finding_intersection", "finding_jaccard", "phenomenon_meaning_agreement"), "quality v3 match.raw_model_metrics")
    union = metrics["finding_union"]
    intersection = metrics["finding_intersection"]
    if any(type(value) is not int or value < 0 for value in (union, intersection)):
        raise ValidationError("quality v3 match raw finding counts must be non-negative integers")
    for field in ("finding_jaccard", "phenomenon_meaning_agreement"):
        value = metrics[field]
        if type(value) not in (int, float) or not 0 <= value <= 1:
            raise ValidationError(f"quality v3 match.raw_model_metrics.{field} must be from 0 to 1")
    raw_left = match["raw_model_counts"]["left"]
    raw_right = match["raw_model_counts"]["right"]
    expected_union = raw_left + raw_right - intersection
    expected_jaccard = intersection / union if union else 1.0
    if (
        intersection > min(raw_left, raw_right)
        or union != expected_union
        or metrics["finding_jaccard"] != expected_jaccard
    ):
        raise ValidationError("quality v3 match raw finding metrics are mathematically inconsistent")
    if intersection == 0 and metrics["phenomenon_meaning_agreement"] != 1.0:
        raise ValidationError("quality v3 empty raw intersection must have full classification agreement")
    anchors = match["anchor_counts"]
    if not isinstance(anchors, dict) or set(anchors) != {"normalizations", "rejections"} or any(type(value) is not int or value < 0 for value in anchors.values()):
        raise ValidationError("quality v3 match.anchor_counts is invalid")
    if not isinstance(match["issues"], list) or not isinstance(match["manual_queue"], list):
        raise ValidationError("quality v3 match issues/manual_queue must be arrays")
    queued = []
    member_identities: set[tuple[str, str]] = set()
    for index, issue in enumerate(match["issues"], start=1):
        where = f"quality v3 match.issues[{index - 1}]"
        if not isinstance(issue, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(issue, ("issue_id", "revision_id", "cluster_type", "members", "derivation", "requires_adjudication"), where)
        if issue["issue_id"] != f"Q3-{index:04d}":
            raise ValidationError(f"{where}.issue_id is stale or out of order")
        _sha(issue["revision_id"], f"{where}.revision_id")
        _enum(issue["cluster_type"], ("full-match", "partial-match", "split-merge", "left-only", "right-only", "ambiguous"), f"{where}.cluster_type")
        if type(issue["requires_adjudication"]) is not bool or not isinstance(issue["members"], list):
            raise ValidationError(f"{where} queue/member fields are invalid")
        for member_index, member in enumerate(issue["members"]):
            member_where = f"{where}.members[{member_index}]"
            if not isinstance(member, dict):
                raise ValidationError(f"{member_where} must be an object")
            _exact_fields(member, ("side", "finding_id", "error_code", "phenomenon", "meaning_change", "source_evidence", "target_evidence", "derivation", "anchor_decision", "anchor_id"), member_where)
            _enum(member["side"], ("left", "right"), f"{member_where}.side")
            _string(member["finding_id"], f"{member_where}.finding_id")
            _enum(member["error_code"], ERROR_CODES_V3, f"{member_where}.error_code")
            _enum(member["phenomenon"], PHENOMENA_V3, f"{member_where}.phenomenon")
            _enum(
                member["meaning_change"], MEANING_CHANGES_V3,
                f"{member_where}.meaning_change",
            )
            _enum(member["anchor_decision"], ("none", "normalized"), f"{member_where}.anchor_decision")
            identity = (member["side"], member["finding_id"])
            if identity in member_identities:
                raise ValidationError(f"{member_where} duplicates an evaluator finding")
            member_identities.add(identity)
            for evidence_field in ("source_evidence", "target_evidence"):
                evidence = member[evidence_field]
                evidence_where = f"{member_where}.{evidence_field}"
                if not isinstance(evidence, dict) or set(evidence) not in (
                    {"quote", "occurrence", "state", "start", "end"},
                    {"quote", "occurrence", "whole_item", "state", "start", "end"},
                ):
                    raise ValidationError(f"{evidence_where} has an invalid normalized shape")
                _string(evidence["quote"], f"{evidence_where}.quote", allow_empty=True)
                if type(evidence["occurrence"]) is not int or evidence["occurrence"] < 0:
                    raise ValidationError(f"{evidence_where}.occurrence is invalid")
                _enum(evidence["state"], ("exact", "ambiguous", "missing", "whole-item"), f"{evidence_where}.state")
                if "whole_item" in evidence and evidence["whole_item"] is not True:
                    raise ValidationError(f"{evidence_where}.whole_item must be true when present")
                if (evidence["state"] == "whole-item") != (evidence.get("whole_item") is True):
                    raise ValidationError(f"{evidence_where}.whole_item and state differ")
                if evidence["start"] is not None and type(evidence["start"]) is not int:
                    raise ValidationError(f"{evidence_where}.start is invalid")
                if evidence["end"] is not None and type(evidence["end"]) is not int:
                    raise ValidationError(f"{evidence_where}.end is invalid")
            _validate_derivation_artifact(member["derivation"], f"{member_where}.derivation")
        derivation = _validate_derivation_artifact(issue["derivation"], f"{where}.derivation")
        if issue["requires_adjudication"]:
            queued.append(issue["issue_id"])
    if match["manual_queue"] != queued or len(set(match["manual_queue"])) != len(match["manual_queue"]):
        raise ValidationError("quality v3 match.manual_queue does not exactly follow issue order")
    expected_id = canonical_sha256({key: value for key, value in match.items() if key != "match_id"})
    if match["match_id"] != expected_id:
        raise ValidationError("quality v3 match_id does not match canonical content")
    return match


def validate_adjudication_validation_v3(
    validation: dict[str, Any], *, match: dict[str, Any]
) -> dict[str, Any]:
    validate_match_v3(match)
    if not isinstance(validation, dict):
        raise ValidationError("quality v3 adjudication validation must be an object")
    _exact_fields(validation, ("schema_version", "quality_contract", "match_id", "adjudicator_id", "strict", "items", "validation_id"), "quality v3 adjudication validation")
    if validation["schema_version"] != 3 or validation["quality_contract"] != ADJUDICATION_VALIDATION_V3_CONTRACT:
        raise ValidationError("unsupported quality v3 adjudication validation contract")
    if validation["match_id"] != match["match_id"] or type(validation["strict"]) is not bool:
        raise ValidationError("quality v3 adjudication validation identity is invalid")
    _string(validation["adjudicator_id"], "quality v3 adjudication validation.adjudicator_id")
    if not isinstance(validation["items"], list):
        raise ValidationError("quality v3 adjudication validation.items must be an array")
    expected = match["manual_queue"]
    received = []
    issues = {issue["issue_id"]: issue for issue in match["issues"]}
    for index, item in enumerate(validation["items"]):
        where = f"quality v3 adjudication validation.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(item, ("issue_id", "decision", "severity", "rationale", "final_severity"), where)
        issue_id = _string(item["issue_id"], f"{where}.issue_id")
        if issue_id not in expected or issue_id in received:
            raise ValidationError("quality v3 adjudication validation contains unknown or duplicate issues")
        received.append(issue_id)
        decision = _enum(item["decision"], ("reject", "confirm"), f"{where}.decision")
        _string(item["rationale"], f"{where}.rationale")
        if decision == "reject":
            if item["severity"] is not None or item["final_severity"] is not None:
                raise ValidationError(f"{where} rejected severity must be null")
        else:
            severity = _enum(item["severity"], ("blocker", "major", "minor"), f"{where}.severity")
            if item["final_severity"] != severity:
                raise ValidationError(f"{where}.final_severity differs from confirmed severity")
            original = issues[issue_id]["derivation"]["derived_severity"]
            rank = {"minor": 0, "major": 1, "blocker": 2}
            if rank[severity] < rank[original]:
                raise ValidationError(f"{where}.severity cannot downgrade a confirmed finding")
    if validation["strict"] and received != expected:
        raise ValidationError("strict quality v3 adjudication validation must cover the queue in order")
    expected_id = canonical_sha256({key: value for key, value in validation.items() if key != "validation_id"})
    if validation["validation_id"] != expected_id:
        raise ValidationError("quality v3 validation_id does not match canonical content")
    return validation


def build_disputes_v3(
    *, match: dict[str, Any], sample: dict[str, Any], seed: str = "tome4-quality-disputes-v3"
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_match_v3(match)
    if match.get("sample_id") != sample.get("sample_id"):
        raise ValidationError("quality v3 dispute sample identity differs")
    by_revision = {item["revision_id"]: item for item in sample["items"]}
    rng = random.Random(seed)
    public = []
    mappings = []
    issue_by_id = {issue["issue_id"]: issue for issue in match["issues"]}
    for issue_id in match["manual_queue"]:
        issue = issue_by_id[issue_id]
        labels = list(issue["members"])
        rng.shuffle(labels)
        candidates = []
        for index, member in enumerate(labels, start=1):
            label = f"candidate-{index}"
            candidates.append({key: value for key, value in member.items() if key != "side"})
            candidates[-1]["candidate_id"] = label
            mappings.append({"issue_id": issue_id, "candidate_id": label, "side": member["side"]})
        sample_item = by_revision[issue["revision_id"]]
        public.append(
            {
                "issue_id": issue_id, "revision_id": issue["revision_id"],
                "source": sample_item["source"], "target": sample_item["target"],
                "context_neighbors": sample_item.get("context_neighbors", []),
                "cluster_type": issue["cluster_type"], "candidates": candidates,
            }
        )
    dispute = {
        "schema_version": 3, "quality_contract": "tome4-quality-dispute-v3",
        "match_id": match["match_id"], "dispute_id": "", "seed": seed, "items": public,
    }
    dispute["dispute_id"] = canonical_sha256({key: value for key, value in dispute.items() if key != "dispute_id"})
    identity = {
        "schema_version": 3, "quality_contract": "tome4-quality-dispute-identity-v3",
        "dispute_id": dispute["dispute_id"], "mapping_id": "", "mappings": mappings,
    }
    identity["mapping_id"] = canonical_sha256({key: value for key, value in identity.items() if key != "mapping_id"})
    return dispute, identity


def adjudicate_v3(
    *, match: dict[str, Any], adjudication: dict[str, Any], policy: dict[str, Any], strict: bool = True
) -> dict[str, Any]:
    validate_match_v3(match)
    if not isinstance(adjudication, dict):
        raise ValidationError("quality v3 adjudication must be an object")
    _exact_fields(
        adjudication,
        ("schema_version", "quality_contract", "match_id", "adjudicator_id", "items"),
        "quality v3 adjudication",
    )
    if adjudication["schema_version"] != 3 or adjudication["quality_contract"] != "tome4-quality-adjudication-v3":
        raise ValidationError("unsupported quality v3 adjudication contract")
    if adjudication["match_id"] != match.get("match_id"):
        raise ValidationError("quality v3 adjudication match_id does not match")
    _string(adjudication["adjudicator_id"], "quality v3 adjudication.adjudicator_id")
    if not isinstance(adjudication["items"], list):
        raise ValidationError("quality v3 adjudication.items must be an array")
    expected = list(match["manual_queue"])
    received = [item.get("issue_id") for item in adjudication["items"] if isinstance(item, dict)]
    if strict and received != expected:
        raise ValidationError("strict quality v3 adjudication must cover the manual queue in order")
    issues = {issue["issue_id"]: issue for issue in match["issues"]}
    seen = set()
    normalized = []
    for index, item in enumerate(adjudication["items"]):
        where = f"quality v3 adjudication.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(item, ("issue_id", "decision", "severity", "rationale"), where)
        issue_id = item["issue_id"]
        if issue_id not in issues or issue_id in seen or issue_id not in expected:
            raise ValidationError(f"{where}.issue_id is unknown, duplicate, or not queued")
        seen.add(issue_id)
        decision = _enum(item["decision"], ("reject", "confirm"), f"{where}.decision")
        _string(item["rationale"], f"{where}.rationale")
        if decision == "reject":
            if item["severity"] is not None:
                raise ValidationError(f"{where}.severity must be null when rejected")
            final_severity = None
        else:
            final_severity = _enum(item["severity"], policy["severities"], f"{where}.severity")
            original = issues[issue_id]["derivation"]["derived_severity"]
            rank = {"minor": 0, "major": 1, "blocker": 2}
            if rank[final_severity] < rank[original]:
                raise ValidationError(f"{where}.severity cannot downgrade a confirmed finding")
        normalized.append({**item, "final_severity": final_severity})
    validation = {
        "schema_version": 3,
        "quality_contract": ADJUDICATION_VALIDATION_V3_CONTRACT,
        "match_id": match["match_id"], "adjudicator_id": adjudication["adjudicator_id"],
        "strict": strict, "items": normalized, "validation_id": "",
    }
    validation["validation_id"] = canonical_sha256({key: value for key, value in validation.items() if key != "validation_id"})
    return validate_adjudication_validation_v3(validation, match=match)


def _report_content_v3(
    *, match: dict[str, Any], adjudication_validation: dict[str, Any] | None
) -> dict[str, Any]:
    validate_match_v3(match)
    issues = match["issues"]
    manual = set(match["manual_queue"])
    matched = [issue for issue in issues if len(issue["members"]) == 2]
    raw_left = match.get("raw_model_counts", {}).get("left", 0)
    raw_right = match.get("raw_model_counts", {}).get("right", 0)
    normalized_left = match["normalized_model_counts"]["left"]
    normalized_right = match["normalized_model_counts"]["right"]
    anchor_conflicts = sum(
        member["derivation"].get("anchor_conflict", False)
        for issue in issues for member in issue["members"]
    )
    adjudicated = rejected = 0
    decisions: dict[str, dict[str, Any]] = {}
    if adjudication_validation is not None:
        validate_adjudication_validation_v3(adjudication_validation, match=match)
        adjudicated = len(adjudication_validation["items"])
        rejected = sum(item["decision"] == "reject" for item in adjudication_validation["items"])
        decisions = {item["issue_id"]: item for item in adjudication_validation["items"]}
    pre_counts = Counter(issue["derivation"]["derived_severity"] for issue in issues)
    pre_provisional = sum(issue["derivation"]["derivation_state"] == "provisional" for issue in issues)
    final_counts: Counter[str] = Counter()
    remaining_provisional = 0
    for issue in issues:
        decision = decisions.get(issue["issue_id"])
        if decision is not None and decision["decision"] == "reject":
            continue
        final_counts[
            decision["final_severity"] if decision is not None else issue["derivation"]["derived_severity"]
        ] += 1
        if issue["derivation"]["derivation_state"] == "provisional" and decision is None:
            remaining_provisional += 1
    return {
        "schema_version": 3, "quality_contract": "tome4-quality-report-v3",
        "match_id": match["match_id"],
        "adjudication_validation_id": (
            adjudication_validation["validation_id"]
            if adjudication_validation is not None else None
        ),
        "raw_model_metrics": {
            "left_findings": raw_left, "right_findings": raw_right,
            **match.get("raw_model_metrics", {}),
        },
        "anchor_normalized_metrics": {
            "left_findings": normalized_left, "right_findings": normalized_right,
            "issue_union": len(issues), "matched_issues": len(matched),
            "negative_anchor_rejections": match.get("anchor_counts", {}).get("rejections", 0),
            "positive_anchor_normalizations": match.get("anchor_counts", {}).get("normalizations", 0),
            "anchor_conflicts": anchor_conflicts,
        },
        "severity_metrics": {
            "pre_adjudication_counts": dict(sorted(pre_counts.items())),
            "final_counts": dict(sorted(final_counts.items())),
            "pre_adjudication_provisional": pre_provisional,
            "remaining_provisional": remaining_provisional,
        },
        "human_burden": {
            "issues_requiring_adjudication": len(manual),
            "items_requiring_adjudication": len({issue["revision_id"] for issue in issues if issue["issue_id"] in manual}),
            "issues_adjudicated": adjudicated, "findings_rejected": rejected,
        },
    }


def build_report_v3(
    *, match: dict[str, Any], adjudication_validation: dict[str, Any] | None = None
) -> dict[str, Any]:
    content = _report_content_v3(
        match=match, adjudication_validation=adjudication_validation,
    )
    report = {**content, "report_id": canonical_sha256(content)}
    return validate_report_v3(
        report, match=match, adjudication_validation=adjudication_validation,
    )


def validate_report_v3(
    report: dict[str, Any], *, match: dict[str, Any],
    adjudication_validation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_match_v3(match)
    if not isinstance(report, dict):
        raise ValidationError("quality v3 report must be an object")
    _exact_fields(report, ("schema_version", "quality_contract", "match_id", "adjudication_validation_id", "report_id", "raw_model_metrics", "anchor_normalized_metrics", "severity_metrics", "human_burden"), "quality v3 report")
    if report["schema_version"] != 3 or report["quality_contract"] != "tome4-quality-report-v3" or report["match_id"] != match["match_id"]:
        raise ValidationError("quality v3 report identity is invalid")
    expected_metric_fields = {
        "raw_model_metrics": {"left_findings", "right_findings", "finding_union", "finding_intersection", "finding_jaccard", "phenomenon_meaning_agreement"},
        "anchor_normalized_metrics": {"left_findings", "right_findings", "issue_union", "matched_issues", "negative_anchor_rejections", "positive_anchor_normalizations", "anchor_conflicts"},
        "human_burden": {"issues_requiring_adjudication", "items_requiring_adjudication", "issues_adjudicated", "findings_rejected"},
    }
    for field, expected in expected_metric_fields.items():
        value = report[field]
        if not isinstance(value, dict) or set(value) != expected or any(type(item) not in (int, float) for item in value.values()):
            raise ValidationError(f"quality v3 report.{field} is invalid")
    _exact_fields(report["severity_metrics"], ("pre_adjudication_counts", "final_counts", "pre_adjudication_provisional", "remaining_provisional"), "quality v3 report.severity_metrics")
    for field in ("pre_adjudication_counts", "final_counts"):
        counts = report["severity_metrics"][field]
        if not isinstance(counts, dict) or any(key not in {"blocker", "major", "minor"} or type(value) is not int or value < 0 for key, value in counts.items()):
            raise ValidationError(f"quality v3 report.severity_metrics.{field} is invalid")
    for field in ("pre_adjudication_provisional", "remaining_provisional"):
        if type(report["severity_metrics"][field]) is not int or report["severity_metrics"][field] < 0:
            raise ValidationError(f"quality v3 report.severity_metrics.{field} is invalid")
    expected_content = _report_content_v3(
        match=match, adjudication_validation=adjudication_validation,
    )
    expected = {**expected_content, "report_id": canonical_sha256(expected_content)}
    if report != expected:
        raise ValidationError("quality v3 report derived content or lineage differs")
    return report


def _validate_bundle_identity_map_v3(value: Any, where: str) -> dict[str, list[str]]:
    if not isinstance(value, dict) or set(value) != {"reviewer-a", "reviewer-b"}:
        raise ValidationError(f"{where} must contain reviewer-a and reviewer-b exactly")
    for evaluator_id, identities in value.items():
        if (
            not isinstance(identities, list)
            or len(identities) != 2
            or len(set(identities)) != 2
        ):
            raise ValidationError(f"{where}.{evaluator_id} must contain two unique identities")
        for index, identity in enumerate(identities):
            _sha(identity, f"{where}.{evaluator_id}[{index}]")
    return value


def validate_stability_preregistration_v3(
    preregistration: dict[str, Any],
    *,
    sample: dict[str, Any],
    policy: dict[str, Any],
    matrix: dict[str, Any],
    anchors: dict[str, Any],
    prompt_sha256: str,
    bundle_ids_by_evaluator: dict[str, list[str]],
    bundle_sha256s_by_evaluator: dict[str, list[str]],
) -> dict[str, Any]:
    _exact_fields(
        preregistration,
        (
            "contract", "schema_version", "sample_contract", "sample_id", "evaluators",
            "thresholds", "frozen_inputs", "connection_failure_retry_limit",
            "replace_content_failures", "external_transfer_limit", "preregistration_id",
        ),
        "quality v3 stability preregistration",
    )
    if preregistration["contract"] != "tome4-quality-stability-preregistration-v2" or preregistration["schema_version"] != 2:
        raise ValidationError("unsupported quality v3 stability preregistration")
    if preregistration["sample_contract"] != CALIBRATION_V3_CONTRACT or preregistration["sample_id"] != sample["sample_id"]:
        raise ValidationError("quality v3 preregistration sample identity differs")
    if preregistration["thresholds"] != policy["stability_thresholds"]:
        raise ValidationError("quality v3 stability thresholds are not frozen values")
    evaluators = preregistration["evaluators"]
    if not isinstance(evaluators, list) or len(evaluators) != 2:
        raise ValidationError("quality v3 stability preregistration requires two evaluators")
    if [item.get("id") for item in evaluators] != policy["evaluator_ids"]:
        raise ValidationError("quality v3 preregistration evaluator order differs")
    for index, evaluator in enumerate(evaluators):
        _exact_fields(evaluator, ("id", "provider", "model", "thinking", "runs"), f"quality v3 evaluators[{index}]")
        if evaluator["runs"] != 2:
            raise ValidationError("quality v3 preregistration requires two runs per evaluator")
        for field in ("id", "provider", "model", "thinking"):
            _string(evaluator[field], f"quality v3 evaluators[{index}].{field}")
    frozen = preregistration["frozen_inputs"]
    _exact_fields(
        frozen,
        (
            "calibration_sample_id", "calibration_sample_sha256",
            "holdout_sample_id", "holdout_sample_sha256",
            "policy_v3_sha256", "prompt_sha256",
            "severity_matrix_sha256", "anchors_sha256",
            "bundle_ids_by_evaluator", "bundle_sha256s_by_evaluator",
        ),
        "quality v3 stability frozen_inputs",
    )
    expected = {
        "calibration_sample_id": sample["sample_id"],
        "calibration_sample_sha256": canonical_sha256(sample),
        "holdout_sample_id": frozen.get("holdout_sample_id"),
        "holdout_sample_sha256": frozen.get("holdout_sample_sha256"),
        "policy_v3_sha256": canonical_sha256(policy),
        "prompt_sha256": prompt_sha256,
        "severity_matrix_sha256": canonical_sha256(matrix),
        "anchors_sha256": canonical_sha256(anchors),
        "bundle_ids_by_evaluator": bundle_ids_by_evaluator,
        "bundle_sha256s_by_evaluator": bundle_sha256s_by_evaluator,
    }
    _sha(frozen.get("holdout_sample_id"), "quality v3 frozen_inputs.holdout_sample_id")
    _sha(frozen.get("holdout_sample_sha256"), "quality v3 frozen_inputs.holdout_sample_sha256")
    _validate_bundle_identity_map_v3(
        frozen.get("bundle_ids_by_evaluator"),
        "quality v3 frozen_inputs.bundle_ids_by_evaluator",
    )
    _validate_bundle_identity_map_v3(
        frozen.get("bundle_sha256s_by_evaluator"),
        "quality v3 frozen_inputs.bundle_sha256s_by_evaluator",
    )
    if frozen != expected:
        raise ValidationError("quality v3 preregistration frozen inputs differ")
    if (
        preregistration["external_transfer_limit"] != 8
        or preregistration["connection_failure_retry_limit"] != 0
        or preregistration["replace_content_failures"] is not False
    ):
        raise ValidationError("quality v3 preregistration failure semantics differ")
    expected_id = canonical_sha256({key: value for key, value in preregistration.items() if key != "preregistration_id"})
    if preregistration["preregistration_id"] != expected_id:
        raise ValidationError("quality v3 preregistration_id does not match")
    return preregistration


def _finding_pairs_for_stability(
    left: dict[str, Any], right: dict[str, Any], *, raw: bool
) -> tuple[list[tuple[dict[str, Any], dict[str, Any]]], int]:
    pairs = []
    union = 0
    for left_item, right_item in zip(left["items"], right["items"]):
        left_findings = left_item["raw_findings"] if raw else left_item["findings"]
        right_findings = right_item["raw_findings"] if raw else right_item["findings"]
        used = set()
        for lf in left_findings:
            matches = [i for i, rf in enumerate(right_findings) if i not in used and _spans_related(lf, rf)]
            if matches:
                index = matches[0]
                used.add(index)
                pairs.append((lf, right_findings[index]))
            union += 1
        union += len(right_findings) - len(used)
    return pairs, union


def runner_report_semantic_identity_v3(report: dict[str, Any]) -> str:
    fields = (
        "mode", "sample_id", "evaluator_id", "provider", "model", "thinking",
        "prompt_sha256", "policy_sha256", "severity_matrix_sha256", "anchors_sha256",
        "bundle_ids", "bundle_sha256s", "assessment_sha256", "preregistration_id",
        "round", "execution_id", "shard_transfers",
    )
    return canonical_sha256({field: report.get(field) for field in fields})


def validate_runner_report_v3(
    runner: dict[str, Any], *, sample: dict[str, Any], evaluator: dict[str, Any],
    assessment_sha256: str, preregistration: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(runner, dict) or runner.get("ok") is not True:
        raise ValidationError("quality v3 runner report must be a successful object")
    expected = {
        "mode": "blind-quality-assessment-v3", "sample_id": sample["sample_id"],
        "evaluator_id": evaluator["id"], "provider": evaluator["provider"],
        "model": evaluator["model"], "thinking": evaluator["thinking"],
        "prompt_sha256": evaluator["prompt_sha256"], "policy_sha256": evaluator["policy_sha256"],
        "severity_matrix_sha256": evaluator["severity_matrix_sha256"],
        "anchors_sha256": evaluator["anchors_sha256"], "bundle_ids": evaluator["bundle_ids"],
        "bundle_sha256s": evaluator["bundle_sha256s"], "assessment_sha256": assessment_sha256,
        "validated_results": 1, "preregistration_id": preregistration["preregistration_id"],
    }
    if any(runner.get(field) != value for field, value in expected.items()):
        raise ValidationError("quality v3 runner report identity differs")
    if runner.get("cache_decision") != "disabled":
        raise ValidationError("quality v3 calibration requires cache to be disabled")
    if runner.get("round") not in (1, 2):
        raise ValidationError("quality v3 runner report round must be 1 or 2")
    _sha(runner.get("execution_id"), "quality v3 runner report.execution_id")
    transfers = runner.get("shard_transfers")
    if not isinstance(transfers, list) or len(transfers) != len(evaluator["bundle_ids"]):
        raise ValidationError("quality v3 runner report shard transfer count differs")
    for index, transfer in enumerate(transfers, start=1):
        if not isinstance(transfer, dict):
            raise ValidationError("quality v3 runner report shard transfer must be an object")
        _exact_fields(transfer, ("shard_index", "bundle_id", "state"), f"quality v3 runner report.shard_transfers[{index - 1}]")
        if transfer != {"shard_index": index, "bundle_id": evaluator["bundle_ids"][index - 1], "state": "succeeded"}:
            raise ValidationError("quality v3 stability requires every registered shard transfer to succeed")
    if runner.get("attempts") != len(transfers) or runner.get("charged_or_possible_transfers") != len(transfers):
        raise ValidationError("quality v3 runner report transfer accounting differs")
    expected_semantic = runner_report_semantic_identity_v3(runner)
    if runner.get("runner_report_id") != expected_semantic:
        raise ValidationError("quality v3 runner report semantic identity is stale")
    return runner


def validate_campaign_ledger_v3(
    ledger: dict[str, Any], *, preregistration: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(ledger, dict):
        raise ValidationError("quality v3 calibration campaign ledger must be an object")
    _exact_fields(
        ledger,
        (
            "contract", "schema_version", "preregistration_id",
            "external_transfer_limit", "transfers", "stability_reports",
        ),
        "quality v3 calibration campaign ledger",
    )
    if (
        ledger["contract"] != "tome4-quality-calibration-campaign-ledger-v3"
        or ledger["schema_version"] != 3
        or ledger["preregistration_id"] != preregistration["preregistration_id"]
        or ledger["external_transfer_limit"] != 8
        or not isinstance(ledger["transfers"], list)
        or not isinstance(ledger["stability_reports"], dict)
        or len(ledger["transfers"]) > 8
    ):
        raise ValidationError("quality v3 calibration campaign ledger header is invalid")
    bundle_ids_by_evaluator = _validate_bundle_identity_map_v3(
        preregistration.get("frozen_inputs", {}).get("bundle_ids_by_evaluator"),
        "quality v3 calibration campaign bundle ids",
    )
    seen = set()
    execution_by_run: dict[tuple[str, int], str] = {}
    for index, entry in enumerate(ledger["transfers"]):
        where = f"quality v3 calibration campaign ledger.transfers[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(entry, ("evaluator_id", "round", "execution_id", "shard_index", "bundle_id", "state"), where)
        _enum(entry["evaluator_id"], ("reviewer-a", "reviewer-b"), f"{where}.evaluator_id")
        if entry["round"] not in (1, 2) or entry["shard_index"] not in (1, 2):
            raise ValidationError(f"{where} is outside the frozen campaign")
        _sha(entry["execution_id"], f"{where}.execution_id")
        _sha(entry["bundle_id"], f"{where}.bundle_id")
        _enum(entry["state"], ("claimed", "succeeded", "failed"), f"{where}.state")
        expected_bundle_id = bundle_ids_by_evaluator[entry["evaluator_id"]][entry["shard_index"] - 1]
        if entry["bundle_id"] != expected_bundle_id:
            raise ValidationError(f"{where} bundle identity differs from preregistration")
        run_key = (entry["evaluator_id"], entry["round"])
        prior_execution = execution_by_run.setdefault(run_key, entry["execution_id"])
        if entry["execution_id"] != prior_execution:
            raise ValidationError(f"{where} execution identity differs within one run")
        key = (entry["evaluator_id"], entry["round"], entry["shard_index"])
        if key in seen:
            raise ValidationError(f"{where} duplicates a consumed campaign slot")
        seen.add(key)
    if any(
        evaluator_id not in {"reviewer-a", "reviewer-b"}
        or not isinstance(report_id, str)
        for evaluator_id, report_id in ledger["stability_reports"].items()
    ):
        raise ValidationError("quality v3 calibration campaign stability registrations are invalid")
    for evaluator_id, report_id in ledger["stability_reports"].items():
        _sha(report_id, f"quality v3 calibration campaign ledger.stability_reports.{evaluator_id}")
    return ledger


def build_stability_report_v3(
    *,
    sample: dict[str, Any],
    assessments: tuple[dict[str, Any], dict[str, Any]],
    run_reports: tuple[dict[str, Any], dict[str, Any]],
    assessment_sha256s: tuple[str, str],
    run_report_sha256s: tuple[str, str],
    preregistration: dict[str, Any],
    campaign_ledger: dict[str, Any],
) -> dict[str, Any]:
    left, right = assessments
    if left["evaluator"] != right["evaluator"]:
        raise ValidationError("quality v3 stability assessments must use one frozen evaluator identity")
    evaluator = left["evaluator"]
    registered = next((item for item in preregistration["evaluators"] if item["id"] == evaluator["id"]), None)
    if registered is None or any(registered[field] != evaluator[field] for field in ("id", "provider", "model", "thinking")):
        raise ValidationError("quality v3 stability evaluator differs from preregistration")
    validate_campaign_ledger_v3(campaign_ledger, preregistration=preregistration)
    semantic_ids = []
    execution_ids = []
    rounds = []
    for index, (runner, assessment_sha) in enumerate(zip(run_reports, assessment_sha256s)):
        validate_runner_report_v3(
            runner, sample=sample, evaluator=evaluator, assessment_sha256=assessment_sha,
            preregistration=preregistration,
        )
        semantic_ids.append(runner["runner_report_id"])
        execution_ids.append(runner["execution_id"])
        rounds.append(runner["round"])
        entries = campaign_ledger.get("transfers", [])
        matching = [
            entry for entry in entries
            if entry.get("evaluator_id") == evaluator["id"]
            and entry.get("round") == runner["round"]
            and entry.get("execution_id") == runner["execution_id"]
        ]
        expected_transfers = [
            {
                "evaluator_id": evaluator["id"], "round": runner["round"],
                "execution_id": runner["execution_id"], "shard_index": shard_index,
                "bundle_id": bundle_id, "state": "succeeded",
            }
            for shard_index, bundle_id in enumerate(evaluator["bundle_ids"], start=1)
        ]
        if sorted(matching, key=lambda item: item["shard_index"]) != expected_transfers:
            raise ValidationError("quality v3 runner report is not backed by completed campaign ledger slots")
    if rounds != [1, 2] or len(set(execution_ids)) != 2 or len(set(semantic_ids)) != 2:
        raise ValidationError("quality v3 stability requires two distinct registered rounds and executions")
    raw_pairs, raw_union = _finding_pairs_for_stability(left, right, raw=True)
    normalized_pairs, normalized_union = _finding_pairs_for_stability(left, right, raw=False)
    phenomenon_meaning_agreed = sum(
        lf["phenomenon"] == rf["phenomenon"]
        and lf["meaning_change"] == rf["meaning_change"]
        for lf, rf in raw_pairs
    )
    provisional_pairs = [
        (lf, rf) for lf, rf in normalized_pairs
        if lf["derivation"]["derivation_state"] == "provisional"
        or rf["derivation"]["derivation_state"] == "provisional"
    ]
    provisional_agreed = sum(
        lf["derivation"]["derived_severity"] == rf["derivation"]["derived_severity"]
        for lf, rf in provisional_pairs
    )
    def finding_map(assessment: dict[str, Any]) -> dict[tuple[Any, ...], dict[str, Any]]:
        return {
            (item["revision_id"], *_evidence_scope(finding)): finding
            for item in assessment["items"] for finding in item["findings"]
        }
    left_map, right_map = finding_map(left), finding_map(right)
    all_scopes = set(left_map) | set(right_map)
    left_manual = {
        scope for scope in all_scopes
        if scope not in right_map
        or (scope in left_map and left_map[scope]["derivation"]["requires_adjudication"])
    }
    right_manual = {
        scope for scope in all_scopes
        if scope not in left_map
        or (scope in right_map and right_map[scope]["derivation"]["requires_adjudication"])
    }
    manual_union = left_manual | right_manual
    gate_agreed = sum(
        li["host_gate_derivation"] == ri["host_gate_derivation"]
        for li, ri in zip(left["items"], right["items"])
    ) / len(sample["items"])
    metrics = {
        "schema_coverage": 1.0,
        "structure_failures": 0,
        "raw_model": {
            "finding_jaccard": len(raw_pairs) / raw_union if raw_union else 1.0,
            "finding_union": raw_union, "finding_intersection": len(raw_pairs),
            "phenomenon_meaning_agreement": phenomenon_meaning_agreed / len(raw_pairs) if raw_pairs else 1.0,
        },
        "anchor_normalized": {
            "finding_jaccard": len(normalized_pairs) / normalized_union if normalized_union else 1.0,
            "finding_union": normalized_union, "finding_intersection": len(normalized_pairs),
            "provisional_severity_agreement": provisional_agreed / len(provisional_pairs) if provisional_pairs else 1.0,
            "manual_queue_membership_agreement": len(left_manual & right_manual) / len(manual_union) if manual_union else 1.0,
        },
        "host_technical_derivation_agreement": gate_agreed,
    }
    thresholds = preregistration["thresholds"]
    checks = {
        "schema_coverage": metrics["schema_coverage"] >= thresholds["schema_coverage"],
        "structure_failures": metrics["structure_failures"] <= thresholds["structure_failures_max"],
        "raw_finding_jaccard": metrics["raw_model"]["finding_jaccard"] >= thresholds["raw_finding_jaccard_min"],
        "phenomenon_meaning_agreement": metrics["raw_model"]["phenomenon_meaning_agreement"] >= thresholds["phenomenon_meaning_agreement_min"],
        "normalized_provisional_severity_agreement": metrics["anchor_normalized"]["provisional_severity_agreement"] >= thresholds["normalized_provisional_severity_agreement_min"],
        "manual_queue_membership_agreement": metrics["anchor_normalized"]["manual_queue_membership_agreement"] >= thresholds["manual_queue_membership_agreement_min"],
        "host_technical_derivation_agreement": metrics["host_technical_derivation_agreement"] == thresholds["host_technical_derivation_agreement"],
    }
    report = {
        "schema_version": 3, "quality_contract": "tome4-quality-stability-report-v3",
        "sample_id": sample["sample_id"], "preregistration_id": preregistration["preregistration_id"],
        "evaluator": {key: evaluator[key] for key in ("id", "provider", "model", "thinking")},
        "assessment_ids": [left["assessment_id"], right["assessment_id"]],
        "assessment_sha256s": list(assessment_sha256s),
        "run_report_sha256s": list(run_report_sha256s),
        "runner_report_ids": semantic_ids,
        "execution_ids": execution_ids,
        "metrics": metrics, "checks": checks, "passed": all(checks.values()), "report_id": "",
    }
    report["report_id"] = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
    return validate_stability_report_v3(report, preregistration=preregistration)


def validate_stability_report_v3(
    report: dict[str, Any], *, preregistration: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValidationError("quality v3 stability report must be an object")
    _exact_fields(report, ("schema_version", "quality_contract", "sample_id", "preregistration_id", "evaluator", "assessment_ids", "assessment_sha256s", "run_report_sha256s", "runner_report_ids", "execution_ids", "metrics", "checks", "passed", "report_id"), "quality v3 stability report")
    if report["schema_version"] != 3 or report["quality_contract"] != STABILITY_REPORT_V3_CONTRACT:
        raise ValidationError("unsupported quality v3 stability report contract")
    if report["preregistration_id"] != preregistration.get("preregistration_id"):
        raise ValidationError("quality v3 stability report preregistration identity differs")
    _sha(report["sample_id"], "quality v3 stability report.sample_id")
    if report["sample_id"] != preregistration.get("sample_id"):
        raise ValidationError("quality v3 stability report sample identity differs")
    evaluator = report["evaluator"]
    if not isinstance(evaluator, dict):
        raise ValidationError("quality v3 stability report.evaluator must be an object")
    _exact_fields(evaluator, ("id", "provider", "model", "thinking"), "quality v3 stability report.evaluator")
    for field in evaluator:
        _string(evaluator[field], f"quality v3 stability report.evaluator.{field}")
    registered = next((item for item in preregistration.get("evaluators", []) if item.get("id") == evaluator["id"]), None)
    if registered is None or any(registered.get(field) != evaluator[field] for field in evaluator):
        raise ValidationError("quality v3 stability report evaluator differs from preregistration")
    for field in ("assessment_ids", "assessment_sha256s", "run_report_sha256s", "runner_report_ids", "execution_ids"):
        values = report[field]
        if not isinstance(values, list) or len(values) != 2:
            raise ValidationError(f"quality v3 stability report.{field} must contain two identities")
        for index, value in enumerate(values):
            _sha(value, f"quality v3 stability report.{field}[{index}]")
    for field in ("runner_report_ids", "execution_ids"):
        if len(set(report[field])) != 2:
            raise ValidationError(f"quality v3 stability report.{field} must be distinct")
    metrics = report["metrics"]
    if not isinstance(metrics, dict):
        raise ValidationError("quality v3 stability report.metrics must be an object")
    _exact_fields(metrics, ("schema_coverage", "structure_failures", "raw_model", "anchor_normalized", "host_technical_derivation_agreement"), "quality v3 stability report.metrics")
    _exact_fields(metrics["raw_model"], ("finding_jaccard", "finding_union", "finding_intersection", "phenomenon_meaning_agreement"), "quality v3 stability report.metrics.raw_model")
    _exact_fields(metrics["anchor_normalized"], ("finding_jaccard", "finding_union", "finding_intersection", "provisional_severity_agreement", "manual_queue_membership_agreement"), "quality v3 stability report.metrics.anchor_normalized")
    ratios = (
        metrics["schema_coverage"], metrics["host_technical_derivation_agreement"],
        metrics["raw_model"]["finding_jaccard"],
        metrics["raw_model"]["phenomenon_meaning_agreement"],
        metrics["anchor_normalized"]["finding_jaccard"],
        metrics["anchor_normalized"]["provisional_severity_agreement"],
        metrics["anchor_normalized"]["manual_queue_membership_agreement"],
    )
    if any(type(value) not in (int, float) or not 0 <= value <= 1 for value in ratios):
        raise ValidationError("quality v3 stability report ratios must be finite values from 0 to 1")
    counts = (
        metrics["structure_failures"],
        metrics["raw_model"]["finding_union"],
        metrics["raw_model"]["finding_intersection"],
        metrics["anchor_normalized"]["finding_union"],
        metrics["anchor_normalized"]["finding_intersection"],
    )
    if any(type(value) is not int or value < 0 for value in counts):
        raise ValidationError("quality v3 stability report counts must be non-negative integers")
    for group_name in ("raw_model", "anchor_normalized"):
        group = metrics[group_name]
        union = group["finding_union"]
        intersection = group["finding_intersection"]
        expected_jaccard = intersection / union if union else 1.0
        if intersection > union or group["finding_jaccard"] != expected_jaccard:
            raise ValidationError(
                f"quality v3 stability report.metrics.{group_name} Jaccard is inconsistent"
            )
    checks = report["checks"]
    expected_checks = {
        "schema_coverage", "structure_failures", "raw_finding_jaccard",
        "phenomenon_meaning_agreement", "normalized_provisional_severity_agreement",
        "manual_queue_membership_agreement", "host_technical_derivation_agreement",
    }
    if not isinstance(checks, dict) or set(checks) != expected_checks or any(type(value) is not bool for value in checks.values()):
        raise ValidationError("quality v3 stability report.checks must be booleans")
    thresholds = preregistration["thresholds"]
    derived_checks = {
        "schema_coverage": metrics["schema_coverage"] >= thresholds["schema_coverage"],
        "structure_failures": metrics["structure_failures"] <= thresholds["structure_failures_max"],
        "raw_finding_jaccard": metrics["raw_model"]["finding_jaccard"] >= thresholds["raw_finding_jaccard_min"],
        "phenomenon_meaning_agreement": metrics["raw_model"]["phenomenon_meaning_agreement"] >= thresholds["phenomenon_meaning_agreement_min"],
        "normalized_provisional_severity_agreement": metrics["anchor_normalized"]["provisional_severity_agreement"] >= thresholds["normalized_provisional_severity_agreement_min"],
        "manual_queue_membership_agreement": metrics["anchor_normalized"]["manual_queue_membership_agreement"] >= thresholds["manual_queue_membership_agreement_min"],
        "host_technical_derivation_agreement": metrics["host_technical_derivation_agreement"] == thresholds["host_technical_derivation_agreement"],
    }
    if checks != derived_checks:
        raise ValidationError("quality v3 stability report checks do not match frozen thresholds")
    if type(report["passed"]) is not bool or report["passed"] != all(report["checks"].values()):
        raise ValidationError("quality v3 stability report passed flag differs from checks")
    expected_id = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
    if report["report_id"] != expected_id:
        raise ValidationError("quality v3 stability report_id does not match canonical content")
    return report


def validate_holdout_clearance_v3(
    *, sample: dict[str, Any], preregistration: dict[str, Any],
    stability_reports: tuple[dict[str, Any], dict[str, Any]], policy: dict[str, Any],
    matrix: dict[str, Any], anchors: dict[str, Any], prompt_sha256: str,
    campaign_ledger: dict[str, Any],
) -> str:
    validate_sample_v3(sample, policy)
    if sample["dataset_kind"] != "holdout":
        raise ValidationError("quality v3 holdout clearance requires a holdout sample")
    if preregistration.get("contract") != "tome4-quality-stability-preregistration-v2":
        raise ValidationError("quality v3 holdout preregistration contract differs")
    _exact_fields(
        preregistration,
        ("contract", "schema_version", "sample_contract", "sample_id", "evaluators", "thresholds", "frozen_inputs", "external_transfer_limit", "connection_failure_retry_limit", "replace_content_failures", "preregistration_id"),
        "quality v3 holdout preregistration",
    )
    if (
        preregistration["schema_version"] != 2
        or preregistration["sample_contract"] != CALIBRATION_V3_CONTRACT
        or preregistration["thresholds"] != policy["stability_thresholds"]
        or preregistration["external_transfer_limit"] != 8
        or preregistration["connection_failure_retry_limit"] != 0
        or preregistration["replace_content_failures"] is not False
        or [item.get("id") for item in preregistration.get("evaluators", [])] != policy["evaluator_ids"]
    ):
        raise ValidationError("quality v3 holdout preregistration semantics differ")
    for index, evaluator in enumerate(preregistration["evaluators"]):
        _exact_fields(evaluator, ("id", "provider", "model", "thinking", "runs"), f"quality v3 holdout preregistration.evaluators[{index}]")
        if evaluator["runs"] != 2:
            raise ValidationError("quality v3 holdout preregistration requires two runs per evaluator")
        for field in ("id", "provider", "model", "thinking"):
            _string(evaluator[field], f"quality v3 holdout preregistration.evaluators[{index}].{field}")
    expected_preregistration_id = canonical_sha256(
        {key: value for key, value in preregistration.items() if key != "preregistration_id"}
    )
    if preregistration.get("preregistration_id") != expected_preregistration_id:
        raise ValidationError("quality v3 holdout preregistration_id is stale")
    frozen = preregistration.get("frozen_inputs")
    if not isinstance(frozen, dict):
        raise ValidationError("quality v3 holdout preregistration has no frozen inputs")
    _exact_fields(frozen, ("calibration_sample_id", "calibration_sample_sha256", "holdout_sample_id", "holdout_sample_sha256", "policy_v3_sha256", "prompt_sha256", "severity_matrix_sha256", "anchors_sha256", "bundle_ids_by_evaluator", "bundle_sha256s_by_evaluator"), "quality v3 holdout preregistration.frozen_inputs")
    _validate_bundle_identity_map_v3(
        frozen.get("bundle_ids_by_evaluator"),
        "quality v3 holdout preregistration.frozen_inputs.bundle_ids_by_evaluator",
    )
    _validate_bundle_identity_map_v3(
        frozen.get("bundle_sha256s_by_evaluator"),
        "quality v3 holdout preregistration.frozen_inputs.bundle_sha256s_by_evaluator",
    )
    if (
        frozen.get("holdout_sample_id") != sample["sample_id"]
        or frozen.get("holdout_sample_sha256") != canonical_sha256(sample)
        or frozen.get("policy_v3_sha256") != canonical_sha256(policy)
        or frozen.get("prompt_sha256") != prompt_sha256
        or frozen.get("severity_matrix_sha256") != canonical_sha256(matrix)
        or frozen.get("anchors_sha256") != canonical_sha256(anchors)
    ):
        raise ValidationError("quality v3 holdout sample differs from preregistration")
    if len(stability_reports) != 2:
        raise ValidationError("quality v3 holdout requires two stability reports")
    validate_campaign_ledger_v3(campaign_ledger, preregistration=preregistration)
    expected_slots = {
        (evaluator_id, round_number, shard_index)
        for evaluator_id in policy["evaluator_ids"]
        for round_number in (1, 2)
        for shard_index in (1, 2)
    }
    completed_slots = {
        (entry["evaluator_id"], entry["round"], entry["shard_index"])
        for entry in campaign_ledger["transfers"] if entry["state"] == "succeeded"
    }
    if completed_slots != expected_slots or len(campaign_ledger["transfers"]) != 8:
        raise ValidationError("quality v3 holdout campaign ledger is not fully successful")
    evaluator_ids = []
    report_ids = []
    for report in stability_reports:
        validate_stability_report_v3(report, preregistration=preregistration)
        if report["passed"] is not True:
            raise ValidationError("quality v3 holdout stability clearance did not pass")
        evaluator_ids.append(report["evaluator"].get("id"))
        report_ids.append(report["report_id"])
    if evaluator_ids != policy["evaluator_ids"] or len(set(report_ids)) != 2:
        raise ValidationError("quality v3 holdout requires reviewer-a and reviewer-b clearance in order")
    if campaign_ledger["stability_reports"] != dict(zip(evaluator_ids, report_ids)):
        raise ValidationError("quality v3 holdout stability reports are not registered by the campaign")
    return canonical_sha256(
        {
            "preregistration_id": preregistration["preregistration_id"],
            "holdout_sample_id": sample["sample_id"],
            "stability_report_ids": report_ids,
        }
    )
