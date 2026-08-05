"""Offline translation-quality evaluator v2 primitives.

The v2 contract separates model-supplied defect facts from host-derived
severity.  This module intentionally does not reinterpret any v1 artifact.
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

QUALITY_V2_POLICY = "policy-v2.json"
IMPACT_RULES_FILE = "impact-rules-v1.json"
ANCHORS_FILE = "anchors-v1.json"
ASSESSMENT_V2_CONTRACT = "tome4-quality-assessment-v2"
METHOD_V2 = "mqm-pilot-v2"
DERIVATION_STATES = {"derived", "needs-adjudication"}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def bytes_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise ValidationError(f"cannot read quality v2 input: {path}") from error


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
        suffix = "a string" if allow_empty else "a non-empty string"
        raise ValidationError(f"{where} must be {suffix}")
    return value


def _enum(value: Any, allowed: Iterable[str], where: str) -> str:
    allowed_set = set(allowed)
    if not isinstance(value, str) or value not in allowed_set:
        raise ValidationError(
            f"{where} must be one of: {', '.join(sorted(allowed_set))}"
        )
    return value


def _sha(value: Any, where: str) -> str:
    text = _string(value, where)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise ValidationError(f"{where} must be a lowercase SHA-256")
    return text


def load_policy_v2(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / "i18n" / "quality" / QUALITY_V2_POLICY
    policy = _read_object(path, "quality v2 policy")
    if policy.get("contract") != "tome4-quality-policy-v2":
        raise ConfigurationError("unsupported quality v2 policy contract")
    if type(policy.get("schema_version")) is not int or policy["schema_version"] != 2:
        raise ConfigurationError("quality v2 policy schema_version must be exact integer 2")
    required_arrays = (
        "evaluator_ids", "tri_state_values", "defect_classes", "phenomena",
        "meaning_change_types", "impact_fact_fields", "critical_impact_facts",
        "amplification_scopes", "anchor_relations", "reuse_recommendations",
        "span_states", "cluster_types", "mergeable_phenomena",
    )
    for field in required_arrays:
        if not isinstance(policy.get(field), list) or not policy[field]:
            raise ConfigurationError(f"quality v2 policy.{field} must be a non-empty array")
    for field in ("contracts", "datasets"):
        if not isinstance(policy.get(field), dict) or not policy[field]:
            raise ConfigurationError(f"quality v2 policy.{field} must be an object")
    if policy.get("method_version") != METHOD_V2:
        raise ConfigurationError(f"quality v2 method_version must be {METHOD_V2}")
    if type(policy.get("max_shard_items")) is not int or not 1 <= policy["max_shard_items"] <= 20:
        raise ConfigurationError("quality v2 max_shard_items must be an integer from 1 to 20")
    if set(policy["tri_state_values"]) != {"yes", "no", "unknown"}:
        raise ConfigurationError("quality v2 tri_state_values must be yes/no/unknown")
    if not set(policy["critical_impact_facts"]).issubset(policy["impact_fact_fields"]):
        raise ConfigurationError("critical impact facts must be declared impact facts")
    merge_pairs: set[tuple[str, str]] = set()
    for index, pair in enumerate(policy["mergeable_phenomena"]):
        if not isinstance(pair, list) or len(pair) != 2:
            raise ConfigurationError(
                f"quality v2 mergeable_phenomena[{index}] must have two values"
            )
        if any(item not in policy["phenomena"] for item in pair) or pair[0] == pair[1]:
            raise ConfigurationError(
                f"quality v2 mergeable_phenomena[{index}] is invalid"
            )
        normalized = tuple(sorted(pair))
        if normalized in merge_pairs:
            raise ConfigurationError("quality v2 mergeable phenomena must be unique")
        merge_pairs.add(normalized)
    return policy


def load_impact_rules(manifest: Manifest, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    if policy is None:
        policy = load_policy_v2(manifest)
    path = manifest.root / "i18n" / "quality" / IMPACT_RULES_FILE
    rules = _read_object(path, "quality impact rules")
    if rules.get("contract") != "tome4-quality-impact-rules-v1":
        raise ConfigurationError("unsupported quality impact rules contract")
    if type(rules.get("schema_version")) is not int or rules["schema_version"] != 1:
        raise ConfigurationError("quality impact rules schema_version must be 1")
    entries = rules.get("rules")
    if not isinstance(entries, list) or not entries:
        raise ConfigurationError("quality impact rules.rules must be non-empty")
    seen: set[str] = set()
    for index, rule in enumerate(entries):
        if not isinstance(rule, dict):
            raise ConfigurationError(f"quality impact rules.rules[{index}] must be an object")
        unknown = set(rule) - {
            "id", "severity", "category", "all", "phenomenon_in", "defect_class_in"
        }
        if unknown:
            raise ConfigurationError(
                f"quality impact rule {index} has unknown fields: {', '.join(sorted(unknown))}"
            )
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id or rule_id in seen:
            raise ConfigurationError("quality impact rule ids must be unique non-empty strings")
        seen.add(rule_id)
        if rule.get("severity") not in {"blocker", "major", "minor", "note"}:
            raise ConfigurationError(f"quality impact rule {rule_id} has invalid severity")
        conditions = rule.get("all")
        if not isinstance(conditions, dict) or not conditions:
            raise ConfigurationError(f"quality impact rule {rule_id}.all must be non-empty")
        for fact, expected in conditions.items():
            if fact not in policy["impact_fact_fields"] or expected not in policy["tri_state_values"]:
                raise ConfigurationError(f"quality impact rule {rule_id} has invalid fact condition")
        for selector, declared in (
            ("phenomenon_in", policy["phenomena"]),
            ("defect_class_in", policy["defect_classes"]),
        ):
            if selector in rule:
                values = rule[selector]
                if not isinstance(values, list) or not values or not set(values).issubset(declared):
                    raise ConfigurationError(f"quality impact rule {rule_id}.{selector} is invalid")
    return rules


def load_anchors(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / "i18n" / "quality" / ANCHORS_FILE
    anchors = _read_object(path, "quality anchors")
    _exact_fields(anchors, ("contract", "schema_version", "description", "anchors"), "quality anchors")
    if anchors["contract"] != "tome4-quality-anchors-v1" or anchors["schema_version"] != 1:
        raise ConfigurationError("unsupported quality anchors contract")
    if not isinstance(anchors["anchors"], list):
        raise ConfigurationError("quality anchors.anchors must be an array")
    seen: set[str] = set()
    for index, anchor in enumerate(anchors["anchors"]):
        if not isinstance(anchor, dict):
            raise ConfigurationError(f"quality anchors[{index}] must be an object")
        anchor_id = anchor.get("anchor_id")
        if not isinstance(anchor_id, str) or not anchor_id or anchor_id in seen:
            raise ConfigurationError("quality anchor ids must be unique non-empty strings")
        seen.add(anchor_id)
    return anchors


def assessment_identity(assessment: dict[str, Any]) -> str:
    return canonical_sha256(
        {
            "schema_version": assessment.get("schema_version"),
            "quality_contract": assessment.get("quality_contract"),
            "sample_id": assessment.get("sample_id"),
            "evaluator": assessment.get("evaluator"),
            "items": assessment.get("items"),
        }
    )


def normalized_evidence_identity(evidence: dict[str, Any]) -> tuple[Any, ...]:
    return (
        evidence["state"], evidence.get("start"), evidence.get("end"),
        evidence.get("quote", ""),
    )


def normalize_evidence(
    evidence: Any,
    text: str,
    *,
    where: str,
    allow_empty_omission: bool = False,
) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        raise ValidationError(f"{where} must be an object")
    allowed = {"quote", "occurrence", "whole_item"}
    unknown = sorted(set(evidence) - allowed)
    if unknown:
        raise ValidationError(f"{where} has host-owned or unknown fields: {', '.join(unknown)}")
    if "quote" not in evidence or "occurrence" not in evidence:
        raise ValidationError(f"{where} requires quote and occurrence")
    quote = _string(evidence["quote"], f"{where}.quote", allow_empty=True)
    occurrence = evidence["occurrence"]
    if type(occurrence) is not int or occurrence < 0:
        raise ValidationError(f"{where}.occurrence must be an exact non-negative integer")
    whole_item = evidence.get("whole_item", False)
    if whole_item is not False and whole_item is not True:
        raise ValidationError(f"{where}.whole_item must be true when present")
    if whole_item:
        if quote or occurrence != 0:
            raise ValidationError(f"{where} whole-item evidence requires empty quote and occurrence 0")
        return {"quote": "", "occurrence": 0, "whole_item": True, "state": "whole-item", "start": 0, "end": len(text)}
    if not quote:
        if allow_empty_omission and occurrence == 0:
            return {"quote": "", "occurrence": 0, "state": "missing", "start": None, "end": None}
        raise ValidationError(f"{where} empty quote requires whole_item or a legal omission")
    starts: list[int] = []
    position = 0
    while True:
        position = text.find(quote, position)
        if position < 0:
            break
        starts.append(position)
        position += max(1, len(quote))
    if occurrence == 0:
        return {"quote": quote, "occurrence": 0, "state": "ambiguous" if len(starts) > 1 else "missing", "start": None, "end": None}
    if occurrence > len(starts):
        return {"quote": quote, "occurrence": occurrence, "state": "missing", "start": None, "end": None}
    start = starts[occurrence - 1]
    return {"quote": quote, "occurrence": occurrence, "state": "exact", "start": start, "end": start + len(quote)}


def derive_severity(
    facts: dict[str, str],
    *,
    phenomenon: str,
    defect_class: str,
    rules: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    if set(facts) != set(policy["impact_fact_fields"]):
        missing = sorted(set(policy["impact_fact_fields"]) - set(facts))
        unknown = sorted(set(facts) - set(policy["impact_fact_fields"]))
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unknown:
            detail.append("unknown " + ", ".join(unknown))
        raise ValidationError("impact facts do not match policy: " + "; ".join(detail))
    for field, value in facts.items():
        _enum(value, policy["tri_state_values"], f"impact_facts.{field}")
    _enum(phenomenon, policy["phenomena"], "phenomenon")
    _enum(defect_class, policy["defect_classes"], "defect_class")

    possible_higher: list[str] = []
    for rule in rules["rules"]:
        if "phenomenon_in" in rule and phenomenon not in rule["phenomenon_in"]:
            continue
        if "defect_class_in" in rule and defect_class not in rule["defect_class_in"]:
            continue
        state = "true"
        supporting: list[str] = []
        for field, expected in rule["all"].items():
            actual = facts[field]
            if actual == "unknown":
                state = "unknown"
            elif actual != expected:
                state = "false"
                break
            else:
                supporting.append(f"{field}={actual}")
        if state == "false":
            continue
        if state == "unknown":
            possible_higher.append(rule["id"])
            continue
        if possible_higher:
            return {
                "derived_severity": "needs-adjudication",
                "derivation_state": "needs-adjudication",
                "rule_id": None,
                "supporting_facts": [],
                "possible_rule_ids": possible_higher,
            }
        selectors = []
        if "phenomenon_in" in rule:
            selectors.append(f"phenomenon={phenomenon}")
        if "defect_class_in" in rule:
            selectors.append(f"defect_class={defect_class}")
        return {
            "derived_severity": rule["severity"],
            "derivation_state": "derived",
            "rule_id": rule["id"],
            "rule_category": rule["category"],
            "supporting_facts": supporting + selectors,
            "possible_rule_ids": [],
        }
    if possible_higher:
        return {
            "derived_severity": "needs-adjudication",
            "derivation_state": "needs-adjudication",
            "rule_id": None,
            "supporting_facts": [],
            "possible_rule_ids": possible_higher,
        }
    return {
        "derived_severity": "needs-adjudication",
        "derivation_state": "needs-adjudication",
        "rule_id": None,
        "supporting_facts": [],
        "possible_rule_ids": [],
    }


def _validate_evaluator(
    evaluator: Any, policy: dict[str, Any], where: str
) -> dict[str, Any]:
    if not isinstance(evaluator, dict):
        raise ValidationError(f"{where} must be an object")
    fields = (
        "kind", "id", "method_version", "provider", "model", "thinking",
        "prompt_sha256", "rules_sha256", "anchors_sha256", "bundle_ids",
    )
    _exact_fields(evaluator, fields, where)
    if evaluator["kind"] != "model":
        raise ValidationError(f"{where}.kind must be model")
    _enum(evaluator["id"], policy["evaluator_ids"], f"{where}.id")
    if evaluator["method_version"] != METHOD_V2:
        raise ValidationError(f"{where}.method_version must be {METHOD_V2}")
    for field in ("provider", "model", "thinking"):
        _string(evaluator[field], f"{where}.{field}")
    for field in ("prompt_sha256", "rules_sha256", "anchors_sha256"):
        _sha(evaluator[field], f"{where}.{field}")
    bundle_ids = evaluator["bundle_ids"]
    if not isinstance(bundle_ids, list) or not bundle_ids:
        raise ValidationError(f"{where}.bundle_ids must be a non-empty array")
    if len(bundle_ids) != len(set(bundle_ids)):
        raise ValidationError(f"{where}.bundle_ids must be unique")
    for index, bundle_id in enumerate(bundle_ids):
        _sha(bundle_id, f"{where}.bundle_ids[{index}]")
    return evaluator


def _validate_finding(
    finding: Any,
    *,
    sample_item: dict[str, Any],
    policy: dict[str, Any],
    rules: dict[str, Any],
    taxonomy: dict[str, Any],
    anchor_ids: set[str],
    where: str,
) -> dict[str, Any]:
    if not isinstance(finding, dict):
        raise ValidationError(f"{where} must be an object")
    fields = (
        "finding_id", "error_code", "defect_class", "phenomenon",
        "source_evidence", "target_evidence", "defect_summary", "meaning_change",
        "impact_facts", "amplification_scope", "closest_anchor_id",
        "anchor_relation", "body", "evidence_refs",
    )
    _exact_fields(finding, fields, where)
    _string(finding["finding_id"], f"{where}.finding_id")
    error_codes = {item["code"] for item in taxonomy["error_codes"]}
    _enum(finding["error_code"], error_codes, f"{where}.error_code")
    defect_class = _enum(finding["defect_class"], policy["defect_classes"], f"{where}.defect_class")
    phenomenon = _enum(finding["phenomenon"], policy["phenomena"], f"{where}.phenomenon")
    if phenomenon == "other" and len(finding.get("body", "").strip()) < 8:
        raise ValidationError(f"{where}.body must explain phenomenon=other")
    _string(finding["defect_summary"], f"{where}.defect_summary")
    _string(finding["body"], f"{where}.body")
    meaning = finding["meaning_change"]
    if not isinstance(meaning, dict):
        raise ValidationError(f"{where}.meaning_change must be an object")
    _exact_fields(meaning, ("type", "summary"), f"{where}.meaning_change")
    meaning_type = _enum(meaning["type"], policy["meaning_change_types"], f"{where}.meaning_change.type")
    _string(meaning["summary"], f"{where}.meaning_change.summary")
    source_evidence = normalize_evidence(
        finding["source_evidence"], sample_item["source"], where=f"{where}.source_evidence"
    )
    target_evidence = normalize_evidence(
        finding["target_evidence"], sample_item["target"],
        where=f"{where}.target_evidence", allow_empty_omission=meaning_type == "omitted",
    )
    if target_evidence["quote"] == "" and target_evidence["state"] == "missing":
        if meaning_type != "omitted" or not source_evidence["quote"]:
            raise ValidationError(f"{where} has an invalid omission evidence contract")
    facts = finding["impact_facts"]
    if not isinstance(facts, dict):
        raise ValidationError(f"{where}.impact_facts must be an object")
    derivation = derive_severity(
        facts, phenomenon=phenomenon, defect_class=defect_class,
        rules=rules, policy=policy,
    )
    if facts["is_defect"] == "no" and facts["is_substantive"] == "yes":
        raise ValidationError(f"{where} cannot be non-defect and substantive")
    if (
        defect_class == "presentation"
        and meaning_type == "presentation-only"
        and facts["opposite_or_different_rule"] == "yes"
    ):
        raise ValidationError(f"{where} has contradictory presentation and rule facts")
    _enum(finding["amplification_scope"], policy["amplification_scopes"], f"{where}.amplification_scope")
    anchor_id = finding["closest_anchor_id"]
    if anchor_id is not None:
        _string(anchor_id, f"{where}.closest_anchor_id")
        if anchor_id not in anchor_ids:
            raise ValidationError(f"{where}.closest_anchor_id is not a declared anchor")
    _enum(finding["anchor_relation"], policy["anchor_relations"], f"{where}.anchor_relation")
    refs = finding["evidence_refs"]
    if not isinstance(refs, list) or any(not isinstance(item, str) for item in refs):
        raise ValidationError(f"{where}.evidence_refs must be an array of strings")
    return {
        **finding,
        "normalized_source_evidence": source_evidence,
        "normalized_target_evidence": target_evidence,
        "derivation": derivation,
    }


def validate_assessment_v2(
    assessment: dict[str, Any],
    *,
    sample: dict[str, Any],
    policy: dict[str, Any],
    rules: dict[str, Any],
    anchors: dict[str, Any],
    taxonomy: dict[str, Any],
    expected_evaluator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(assessment, dict):
        raise ValidationError("quality v2 assessment must be an object")
    _exact_fields(
        assessment,
        ("schema_version", "quality_contract", "sample_id", "assessment_id", "evaluator", "items"),
        "quality v2 assessment",
    )
    if type(assessment["schema_version"]) is not int or assessment["schema_version"] != 2:
        raise ValidationError("quality v2 assessment.schema_version must be exact integer 2")
    if assessment["quality_contract"] != ASSESSMENT_V2_CONTRACT:
        raise ValidationError("unsupported quality v2 assessment contract")
    if assessment["sample_id"] != sample.get("sample_id"):
        raise ValidationError("quality v2 assessment sample_id does not match")
    evaluator = _validate_evaluator(assessment["evaluator"], policy, "quality v2 assessment.evaluator")
    if expected_evaluator is not None and evaluator != expected_evaluator:
        raise ValidationError("quality v2 assessment evaluator identity is host-owned and does not match")
    sample_items = sample.get("items")
    items = assessment["items"]
    if not isinstance(sample_items, list) or not sample_items:
        raise ValidationError("quality v2 sample has no items")
    if not isinstance(items, list) or len(items) != len(sample_items):
        raise ValidationError("quality v2 assessment must cover every sample item")
    anchor_ids = {item["anchor_id"] for item in anchors["anchors"]}
    normalized_items: list[dict[str, Any]] = []
    finding_ids: set[str] = set()
    for index, (item, sample_item) in enumerate(zip(items, sample_items)):
        where = f"quality v2 assessment.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(
            item,
            ("revision_id", "context_sufficient", "profile_confirmed", "findings", "reuse_recommendation"),
            where,
        )
        if item["revision_id"] != sample_item.get("revision_id"):
            raise ValidationError(f"{where}.revision_id is missing, duplicate, or out of order")
        if type(item["context_sufficient"]) is not bool:
            raise ValidationError(f"{where}.context_sufficient must be boolean")
        if item["profile_confirmed"] is not None:
            _string(item["profile_confirmed"], f"{where}.profile_confirmed")
        if item["reuse_recommendation"] is not None:
            _enum(item["reuse_recommendation"], policy["reuse_recommendations"], f"{where}.reuse_recommendation")
        if not isinstance(item["findings"], list):
            raise ValidationError(f"{where}.findings must be an array")
        normalized_findings = []
        for finding_index, finding in enumerate(item["findings"]):
            normalized = _validate_finding(
                finding, sample_item=sample_item, policy=policy, rules=rules,
                taxonomy=taxonomy, anchor_ids=anchor_ids,
                where=f"{where}.findings[{finding_index}]",
            )
            finding_id = normalized["finding_id"]
            if finding_id in finding_ids:
                raise ValidationError(f"duplicate quality v2 finding_id: {finding_id}")
            finding_ids.add(finding_id)
            if not item["context_sufficient"]:
                critical = [normalized["impact_facts"][field] for field in policy["critical_impact_facts"]]
                span_states = {
                    normalized["normalized_source_evidence"]["state"],
                    normalized["normalized_target_evidence"]["state"],
                }
                if all(value != "unknown" for value in critical) and not normalized["evidence_refs"] and "exact" not in span_states:
                    raise ValidationError(f"{where} claims fully known critical facts without evidence")
            normalized_findings.append(normalized)
        normalized_items.append({**item, "findings": normalized_findings})
    expected_id = assessment_identity(assessment)
    if assessment["assessment_id"] != expected_id:
        raise ValidationError("quality v2 assessment_id does not match canonical content")
    return {**assessment, "items": normalized_items}


def build_assessment_v2(
    *, sample_id: str, evaluator: dict[str, Any], items: list[dict[str, Any]]
) -> dict[str, Any]:
    assessment = {
        "schema_version": 2,
        "quality_contract": ASSESSMENT_V2_CONTRACT,
        "sample_id": sample_id,
        "assessment_id": "",
        "evaluator": evaluator,
        "items": items,
    }
    assessment["assessment_id"] = assessment_identity(assessment)
    return assessment


def _span_related(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["state"] == "whole-item" or right["state"] == "whole-item":
        return left["state"] == right["state"]
    if left["state"] != "exact" or right["state"] != "exact":
        return False
    return left["start"] <= right["end"] and right["start"] <= left["end"]


def _span_identical(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["state"] == right["state"]
        and left.get("start") == right.get("start")
        and left.get("end") == right.get("end")
    )


def _meaning_compatible(left: str, right: str) -> bool:
    if left == right or "unknown" in {left, right}:
        return True
    contradictions = {
        frozenset(("omitted", "added")),
        frozenset(("weakened", "strengthened")),
        frozenset(("none", "reversed")),
        frozenset(("none", "omitted")),
        frozenset(("none", "added")),
        frozenset(("presentation-only", "reversed")),
        frozenset(("presentation-only", "omitted")),
        frozenset(("presentation-only", "added")),
    }
    return frozenset((left, right)) not in contradictions


def _phenomenon_compatible(
    left: dict[str, Any], right: dict[str, Any], policy: dict[str, Any]
) -> bool:
    left_value = left["phenomenon"]
    right_value = right["phenomenon"]
    if left_value == right_value:
        return True
    pair = tuple(sorted((left_value, right_value)))
    declared = {tuple(sorted(item)) for item in policy["mergeable_phenomena"]}
    if pair not in declared:
        return False
    if pair == ("ambiguity", "fluency"):
        return _span_identical(
            left["normalized_source_evidence"],
            right["normalized_source_evidence"],
        ) and _span_identical(
            left["normalized_target_evidence"],
            right["normalized_target_evidence"],
        )
    return True


def findings_match(
    left: dict[str, Any], right: dict[str, Any], policy: dict[str, Any]
) -> bool:
    if not _span_related(
        left["normalized_source_evidence"], right["normalized_source_evidence"]
    ):
        return False
    left_target = left["normalized_target_evidence"]
    right_target = right["normalized_target_evidence"]
    if left_target["state"] == "missing" and right_target["state"] == "missing":
        target_related = not left_target.get("quote") and not right_target.get("quote")
    else:
        target_related = _span_related(left_target, right_target)
    if not target_related:
        return False
    if not _phenomenon_compatible(left, right, policy):
        return False
    return _meaning_compatible(
        left["meaning_change"]["type"], right["meaning_change"]["type"]
    )


def _full_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["phenomenon"] == right["phenomenon"]
        and left["meaning_change"]["type"] == right["meaning_change"]["type"]
        and _span_identical(
            left["normalized_source_evidence"], right["normalized_source_evidence"]
        )
        and _span_identical(
            left["normalized_target_evidence"], right["normalized_target_evidence"]
        )
    )


def _member(side: str, finding: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "error_code": finding["error_code"],
        "defect_class": finding["defect_class"],
        "phenomenon": finding["phenomenon"],
        "source_evidence": finding["normalized_source_evidence"],
        "target_evidence": finding["normalized_target_evidence"],
        "meaning_change": finding["meaning_change"],
        "impact_facts": finding["impact_facts"],
        "amplification_scope": finding["amplification_scope"],
        "closest_anchor_id": finding["closest_anchor_id"],
        "anchor_relation": finding["anchor_relation"],
        "defect_summary": finding["defect_summary"],
        "body": finding["body"],
        "derivation": finding["derivation"],
    }
    normalized["issue_key"] = canonical_sha256(
        {
            "phenomenon": normalized["phenomenon"],
            "source": normalized["source_evidence"],
            "target": normalized["target_evidence"],
            "meaning_change": normalized["meaning_change"]["type"],
        }
    )
    return {"side": side, "finding_id": finding["finding_id"], "normalized": normalized}


def _cluster_fact_state(
    cluster_type: str,
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
) -> tuple[str, dict[str, Any]]:
    if not left or not right:
        finding = (left or right)[0]
        return "single-sided", {
            "derived_severity": "needs-adjudication",
            "derivation_state": "needs-adjudication",
            "rule_id": None,
            "supporting_facts": [],
            "possible_rule_ids": [finding["derivation"].get("rule_id")]
            if finding["derivation"].get("rule_id") else [],
        }
    if cluster_type in {"split-merge", "ambiguous"}:
        return "needs-adjudication", {
            "derived_severity": "needs-adjudication",
            "derivation_state": "needs-adjudication",
            "rule_id": None,
            "supporting_facts": [],
            "possible_rule_ids": [],
        }
    left_finding, right_finding = left[0], right[0]
    if (
        left_finding["impact_facts"] == right_finding["impact_facts"]
        and left_finding["derivation"] == right_finding["derivation"]
    ):
        state = (
            "needs-adjudication"
            if left_finding["derivation"]["derivation_state"] == "needs-adjudication"
            else "agreed"
        )
        return state, left_finding["derivation"]
    return "conflict", {
        "derived_severity": "needs-adjudication",
        "derivation_state": "needs-adjudication",
        "rule_id": None,
        "supporting_facts": [],
        "possible_rule_ids": sorted(
            {
                rule_id
                for finding in (left_finding, right_finding)
                for rule_id in [finding["derivation"].get("rule_id")]
                if rule_id
            }
        ),
    }


def match_assessments_v2(
    *,
    sample: dict[str, Any],
    left_assessment: dict[str, Any],
    right_assessment: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    if left_assessment["sample_id"] != sample.get("sample_id") or right_assessment["sample_id"] != sample.get("sample_id"):
        raise ValidationError("quality v2 matching requires one sample identity")
    if left_assessment["assessment_id"] == right_assessment["assessment_id"]:
        raise ValidationError("quality v2 matching requires two distinct assessments")
    if len(left_assessment["items"]) != len(sample["items"]) or len(right_assessment["items"]) != len(sample["items"]):
        raise ValidationError("quality v2 matching requires complete assessments")

    pending: list[dict[str, Any]] = []
    manual_evidence: set[tuple[str, str, str]] = set()
    for sample_index, (sample_item, left_item, right_item) in enumerate(
        zip(sample["items"], left_assessment["items"], right_assessment["items"])
    ):
        revision_id = sample_item["revision_id"]
        if left_item["revision_id"] != revision_id or right_item["revision_id"] != revision_id:
            raise ValidationError("quality v2 matching found stale or out-of-order revision")
        left_findings = left_item["findings"]
        right_findings = right_item["findings"]
        eligible_left = []
        eligible_right = []
        for side, findings, eligible in (
            ("left", left_findings, eligible_left),
            ("right", right_findings, eligible_right),
        ):
            for finding in findings:
                states = {
                    finding["normalized_source_evidence"]["state"],
                    finding["normalized_target_evidence"]["state"],
                }
                legal_omission = (
                    finding["meaning_change"]["type"] == "omitted"
                    and finding["normalized_target_evidence"]["state"] == "missing"
                    and not finding["normalized_target_evidence"].get("quote")
                    and finding["normalized_source_evidence"]["state"] == "exact"
                )
                if states.issubset({"exact", "whole-item"}) or legal_omission:
                    eligible.append(finding)
                else:
                    manual_evidence.add((revision_id, side, finding["finding_id"]))

        adjacency: dict[tuple[str, int], set[tuple[str, int]]] = defaultdict(set)
        for left_index, left in enumerate(eligible_left):
            for right_index, right in enumerate(eligible_right):
                if findings_match(left, right, policy):
                    left_node = ("left", left_index)
                    right_node = ("right", right_index)
                    adjacency[left_node].add(right_node)
                    adjacency[right_node].add(left_node)
        nodes = [*(('left', index) for index in range(len(eligible_left))), *(('right', index) for index in range(len(eligible_right)))]
        seen: set[tuple[str, int]] = set()
        for node in nodes:
            if node in seen:
                continue
            queue = deque([node])
            seen.add(node)
            component: list[tuple[str, int]] = []
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbor in sorted(adjacency[current]):
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
            left = [eligible_left[index] for side, index in component if side == "left"]
            right = [eligible_right[index] for side, index in component if side == "right"]
            if len(left) == 1 and len(right) == 1:
                cluster_type = "full-match" if _full_match(left[0], right[0]) else "partial-match"
            elif left and right and (len(left) == 1 or len(right) == 1):
                cluster_type = "split-merge"
            elif left and right:
                cluster_type = "ambiguous"
            elif left:
                cluster_type = "left-only"
            else:
                cluster_type = "right-only"
            fact_state, derivation = _cluster_fact_state(cluster_type, left, right)
            members = [*(_member("left", item) for item in left), *(_member("right", item) for item in right)]
            span_starts = [
                member["normalized"]["source_evidence"].get("start")
                for member in members
                if member["normalized"]["source_evidence"].get("start") is not None
            ]
            pending.append(
                {
                    "sample_index": sample_index,
                    "revision_id": revision_id,
                    "cluster_type": cluster_type,
                    "members": members,
                    "fact_state": fact_state,
                    "derivation": derivation,
                    "sort_start": min(span_starts) if span_starts else -1,
                }
            )
        for revision, side, finding_id in sorted(manual_evidence):
            if revision != revision_id:
                continue
            findings = left_findings if side == "left" else right_findings
            finding = next(item for item in findings if item["finding_id"] == finding_id)
            pending.append(
                {
                    "sample_index": sample_index,
                    "revision_id": revision_id,
                    "cluster_type": f"{side}-only",
                    "members": [_member(side, finding)],
                    "fact_state": "needs-adjudication",
                    "derivation": {
                        "derived_severity": "needs-adjudication", "derivation_state": "needs-adjudication",
                        "rule_id": None, "supporting_facts": [], "possible_rule_ids": [],
                    },
                    "sort_start": -1,
                }
            )

    pending.sort(
        key=lambda issue: (
            issue["sample_index"], issue["sort_start"], issue["cluster_type"],
            [(member["side"], member["finding_id"]) for member in issue["members"]],
        )
    )
    issues = []
    manual_queue = []
    for index, issue in enumerate(pending, start=1):
        normalized = {
            "issue_id": f"QI-{index:04d}",
            "revision_id": issue["revision_id"],
            "cluster_type": issue["cluster_type"],
            "members": issue["members"],
            "fact_state": issue["fact_state"],
            "derivation": issue["derivation"],
        }
        issues.append(normalized)
        if issue["fact_state"] != "agreed":
            manual_queue.append(normalized["issue_id"])
    artifact = {
        "schema_version": 1,
        "quality_contract": "tome4-quality-issue-cluster-v1",
        "sample_id": sample["sample_id"],
        "assessment_ids": [left_assessment["assessment_id"], right_assessment["assessment_id"]],
        "match_id": "",
        "issues": issues,
        "manual_queue": manual_queue,
    }
    artifact["match_id"] = canonical_sha256({key: value for key, value in artifact.items() if key != "match_id"})
    return artifact


def build_disputes_v2(
    *,
    match: dict[str, Any],
    sample: dict[str, Any],
    assessments: tuple[dict[str, Any], dict[str, Any]],
    seed: str = "tome4-quality-disputes-v2",
) -> tuple[dict[str, Any], dict[str, Any]]:
    if match["sample_id"] != sample.get("sample_id"):
        raise ValidationError("dispute match and sample identities differ")
    by_revision = {item["revision_id"]: item for item in sample["items"]}
    assessment_by_side = {"left": assessments[0], "right": assessments[1]}
    public_items: list[dict[str, Any]] = []
    mappings: list[dict[str, Any]] = []
    manual = set(match["manual_queue"])
    for issue in match["issues"]:
        if issue["issue_id"] not in manual:
            continue
        candidates = []
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for member in issue["members"]:
            grouped[member["side"]].append(member)
        sides = sorted(grouped)
        random.Random(f"{seed}:{issue['issue_id']}").shuffle(sides)
        for position, side in enumerate(sides):
            label = "X" if position == 0 else "Y"
            candidates.append(
                {
                    "label": label,
                    "findings": [member["normalized"] for member in grouped[side]],
                }
            )
            assessment = assessment_by_side[side]
            mappings.append(
                {
                    "issue_id": issue["issue_id"], "label": label,
                    "assessment_id": assessment["assessment_id"],
                    "evaluator_id": assessment["evaluator"]["id"],
                    "finding_ids": [member["finding_id"] for member in grouped[side]],
                }
            )
        sample_item = by_revision[issue["revision_id"]]
        public_items.append(
            {
                "issue_id": issue["issue_id"], "revision_id": issue["revision_id"],
                "source": sample_item["source"], "target": sample_item["target"],
                "context_neighbors": sample_item.get("context_neighbors", []),
                "cluster_type": issue["cluster_type"], "candidates": candidates,
            }
        )
    dispute = {
        "schema_version": 1, "quality_contract": "tome4-quality-dispute-v1",
        "match_id": match["match_id"], "dispute_id": "", "seed": seed,
        "items": public_items,
    }
    dispute["dispute_id"] = canonical_sha256({key: value for key, value in dispute.items() if key != "dispute_id"})
    identity = {
        "schema_version": 1, "quality_contract": "tome4-quality-dispute-identity-v1",
        "dispute_id": dispute["dispute_id"], "mapping_id": "", "mappings": mappings,
    }
    identity["mapping_id"] = canonical_sha256({key: value for key, value in identity.items() if key != "mapping_id"})
    return dispute, identity


def adjudicate_v2(
    *,
    match: dict[str, Any],
    adjudication: dict[str, Any],
    policy: dict[str, Any],
    rules: dict[str, Any],
    anchors: dict[str, Any],
    strict: bool = True,
) -> dict[str, Any]:
    if not isinstance(adjudication, dict):
        raise ValidationError("quality v2 adjudication must be an object")
    _exact_fields(
        adjudication,
        ("schema_version", "quality_contract", "match_id", "adjudicator_id", "items"),
        "quality v2 adjudication",
    )
    if adjudication["schema_version"] != 2 or adjudication["quality_contract"] != "tome4-quality-adjudication-v2":
        raise ValidationError("unsupported quality v2 adjudication contract")
    if adjudication["match_id"] != match.get("match_id"):
        raise ValidationError("quality v2 adjudication match_id does not match")
    _string(adjudication["adjudicator_id"], "quality v2 adjudication.adjudicator_id")
    items = adjudication["items"]
    if not isinstance(items, list):
        raise ValidationError("quality v2 adjudication.items must be an array")
    expected = list(match["manual_queue"])
    received = [item.get("issue_id") for item in items if isinstance(item, dict)]
    if strict and received != expected:
        raise ValidationError("strict quality v2 adjudication must cover the manual queue in order")
    issue_by_id = {issue["issue_id"]: issue for issue in match["issues"]}
    anchor_ids = {item["anchor_id"] for item in anchors["anchors"]}
    normalized = []
    seen: set[str] = set()
    for index, item in enumerate(items):
        where = f"quality v2 adjudication.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(
            item,
            ("issue_id", "same_issue", "exists", "confirmed_facts", "phenomenon", "defect_class", "derived_severity", "rule_id", "anchor_id", "rationale"),
            where,
        )
        issue_id = item["issue_id"]
        if issue_id not in issue_by_id or issue_id in seen:
            raise ValidationError(f"{where}.issue_id is unknown or duplicated")
        seen.add(issue_id)
        if type(item["same_issue"]) is not bool or type(item["exists"]) is not bool:
            raise ValidationError(f"{where} same_issue/exists must be booleans")
        _string(item["rationale"], f"{where}.rationale")
        facts = item["confirmed_facts"]
        phenomenon = _enum(item["phenomenon"], policy["phenomena"], f"{where}.phenomenon")
        defect_class = _enum(item["defect_class"], policy["defect_classes"], f"{where}.defect_class")
        if not item["same_issue"] and len(issue_by_id[issue_id]["members"]) > 1:
            derived = {
                "derived_severity": "needs-adjudication", "derivation_state": "needs-adjudication",
                "rule_id": None, "supporting_facts": [], "possible_rule_ids": [],
            }
        else:
            derived = derive_severity(facts, phenomenon=phenomenon, defect_class=defect_class, rules=rules, policy=policy)
        if not item["exists"] and facts.get("is_defect") != "no":
            raise ValidationError(f"{where} exists=false requires is_defect=no")
        if item["derived_severity"] != derived["derived_severity"] or item["rule_id"] != derived["rule_id"]:
            raise ValidationError(f"{where} severity/rule cannot be reproduced from confirmed facts")
        anchor_id = item["anchor_id"]
        if anchor_id is not None and anchor_id not in anchor_ids:
            raise ValidationError(f"{where}.anchor_id is not declared")
        normalized.append({**item, "derivation": derived})
    validation = {
        "schema_version": 2,
        "quality_contract": "tome4-quality-adjudication-validation-v2",
        "match_id": match["match_id"],
        "adjudicator_id": adjudication["adjudicator_id"],
        "strict": strict,
        "items": normalized,
        "validation_id": "",
    }
    validation["validation_id"] = canonical_sha256({key: value for key, value in validation.items() if key != "validation_id"})
    return validation
