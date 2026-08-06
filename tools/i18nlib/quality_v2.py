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
CALIBRATION_CONTRACT = "tome4-quality-calibration-v2"
HOLDOUT_CONTRACT = "tome4-quality-holdout-v2"
EVALUATOR_BUNDLE_V2_CONTRACT = "tome4-quality-evaluator-bundle-v2"


def load_evaluator_prompt_v2(manifest: Manifest) -> str:
    prompt_path = manifest.root / "i18n" / "prompts" / "pi-quality-evaluator-v2.md"
    rubric_path = manifest.root / "i18n" / "quality" / "rubric-v2.md"
    try:
        return (
            prompt_path.read_text(encoding="utf-8")
            + "\n\n---\n\n"
            + rubric_path.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeDecodeError) as error:
        raise ConfigurationError(
            "cannot read Pi quality evaluator v2 prompt or rubric"
        ) from error


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
        "calibration_constraints", "holdout_constraints",
        "holdout_distribution_dimensions",
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
    for kind, expected_contract, expected_seed in (
        ("calibration", CALIBRATION_CONTRACT, "tome4-quality-calibration-v2"),
        ("holdout", HOLDOUT_CONTRACT, "tome4-quality-holdout-v2"),
    ):
        dataset = policy["datasets"].get(kind)
        if (
            not isinstance(dataset, dict)
            or dataset.get("contract") != expected_contract
            or dataset.get("seed") != expected_seed
            or type(dataset.get("size")) is not int
            or dataset["size"] != 32
            or type(dataset.get("boundary_enriched")) is not bool
        ):
            raise ConfigurationError(f"quality v2 policy.datasets.{kind} is invalid")
    if set(policy["tri_state_values"]) != {"yes", "no", "unknown"}:
        raise ConfigurationError("quality v2 tri_state_values must be yes/no/unknown")
    if not set(policy["critical_impact_facts"]).issubset(policy["impact_fact_fields"]):
        raise ConfigurationError("critical impact facts must be declared impact facts")
    if policy["holdout_distribution_dimensions"] != [
        "profile", "component-group", "length"
    ]:
        raise ConfigurationError("quality v2 holdout distribution dimensions are frozen")
    for group in ("calibration_constraints", "holdout_constraints"):
        seen_constraints: set[str] = set()
        for index, constraint in enumerate(policy[group]):
            if (
                not isinstance(constraint, dict)
                or set(constraint) != {"id", "min"}
                or not isinstance(constraint["id"], str)
                or not constraint["id"]
                or type(constraint["min"]) is not int
                or constraint["min"] < 1
                or constraint["id"] in seen_constraints
            ):
                raise ConfigurationError(
                    f"quality v2 policy.{group}[{index}] is invalid"
                )
            seen_constraints.add(constraint["id"])
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


def load_anchors(
    manifest: Manifest,
    *,
    policy: dict[str, Any] | None = None,
    rules: dict[str, Any] | None = None,
    taxonomy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = manifest.root / "i18n" / "quality" / ANCHORS_FILE
    anchors = _read_object(path, "quality anchors")
    _exact_fields(anchors, ("contract", "schema_version", "description", "anchors"), "quality anchors")
    if anchors["contract"] != "tome4-quality-anchors-v1" or anchors["schema_version"] != 1:
        raise ConfigurationError("unsupported quality anchors contract")
    if not isinstance(anchors["anchors"], list):
        raise ConfigurationError("quality anchors.anchors must be an array")
    policy = policy or load_policy_v2(manifest)
    rules = rules or load_impact_rules(manifest, policy)
    taxonomy = taxonomy or _read_object(
        manifest.root / "i18n" / "quality" / "taxonomy-v1.json", "quality taxonomy"
    )
    profiles = {
        item.get("id")
        for item in taxonomy.get("profiles", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    seen: set[str] = set()
    for index, anchor in enumerate(anchors["anchors"]):
        if not isinstance(anchor, dict):
            raise ConfigurationError(f"quality anchors[{index}] must be an object")
        where = f"quality anchors[{index}]"
        try:
            _exact_fields(
                anchor,
                (
                    "anchor_id", "source_contract", "sample_id", "revision_id",
                    "adjudication_validation_id", "issue_ids", "profile",
                    "phenomenon", "defect_class", "facts", "derived_severity",
                    "rule_id", "rationale",
                ),
                where,
            )
        except ValidationError as error:
            raise ConfigurationError(str(error)) from error
        anchor_id = anchor.get("anchor_id")
        if not isinstance(anchor_id, str) or not anchor_id or anchor_id in seen:
            raise ConfigurationError("quality anchor ids must be unique non-empty strings")
        seen.add(anchor_id)
        try:
            if anchor["source_contract"] != CALIBRATION_CONTRACT:
                raise ValidationError(
                    f"{where}.source_contract must be {CALIBRATION_CONTRACT}"
                )
            for field in ("sample_id", "revision_id", "adjudication_validation_id"):
                _sha(anchor[field], f"{where}.{field}")
            issue_ids = anchor["issue_ids"]
            if (
                not isinstance(issue_ids, list)
                or not issue_ids
                or len(set(issue_ids)) != len(issue_ids)
                or any(
                    not isinstance(issue_id, str)
                    or len(issue_id) != 7
                    or not issue_id.startswith("QI-")
                    or not issue_id[3:].isdigit()
                    for issue_id in issue_ids
                )
            ):
                raise ValidationError(f"{where}.issue_ids must be unique QI-NNNN ids")
            _enum(anchor["profile"], profiles, f"{where}.profile")
            phenomenon = _enum(
                anchor["phenomenon"], policy["phenomena"], f"{where}.phenomenon"
            )
            defect_class = _enum(
                anchor["defect_class"],
                policy["defect_classes"],
                f"{where}.defect_class",
            )
            facts = anchor["facts"]
            if not isinstance(facts, dict):
                raise ValidationError(f"{where}.facts must be an object")
            _exact_fields(facts, policy["impact_fact_fields"], f"{where}.facts")
            for field, value in facts.items():
                _enum(value, policy["tri_state_values"], f"{where}.facts.{field}")
            _string(anchor["rationale"], f"{where}.rationale")
            derived = derive_severity(
                facts,
                phenomenon=phenomenon,
                defect_class=defect_class,
                rules=rules,
                policy=policy,
            )
            if (
                anchor["derived_severity"] != derived["derived_severity"]
                or anchor["rule_id"] != derived["rule_id"]
            ):
                raise ValidationError(
                    f"{where} severity/rule cannot be reproduced from facts"
                )
        except ValidationError as error:
            raise ConfigurationError(str(error)) from error
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
    model_facts = finding["impact_facts"]
    if not isinstance(model_facts, dict):
        raise ValidationError(f"{where}.impact_facts must be an object")
    facts = dict(model_facts)
    gate_signals = sample_item.get("gate_signals")
    host_gate_facts: dict[str, str] | None = None
    if isinstance(gate_signals, dict):
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
        display_broken = (
            not runtime_broken
            and gate_signals.get("format_shape_match") is False
        )
        host_gate_facts = {
            "technical_gate_confirmed": "yes" if runtime_broken or display_broken else "no",
            "runtime_broken": "yes" if runtime_broken else "no",
            "single_item_display_broken": "yes" if display_broken else "no",
        }
        for field, host_value in host_gate_facts.items():
            if model_facts.get(field) == "yes" and host_value != "yes":
                raise ValidationError(
                    f"{where}.impact_facts.{field}=yes is not confirmed by deterministic gates"
                )
            facts[field] = host_value
    elif any(
        model_facts.get(field) == "yes"
        for field in (
            "technical_gate_confirmed", "runtime_broken",
            "single_item_display_broken",
        )
    ):
        raise ValidationError(
            f"{where} cannot claim a technical gate without host gate signals"
        )
    derivation = derive_severity(
        facts, phenomenon=phenomenon, defect_class=defect_class,
        rules=rules, policy=policy,
    )
    if model_facts["is_defect"] == "no" and model_facts["is_substantive"] == "yes":
        raise ValidationError(f"{where} cannot be non-defect and substantive")
    if (
        defect_class == "presentation"
        and meaning_type == "presentation-only"
        and model_facts["opposite_or_different_rule"] == "yes"
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
        "host_gate_facts": host_gate_facts,
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
    if pair == ("omission", "unit"):
        return (
            left["meaning_change"]["type"] == "omitted"
            and right["meaning_change"]["type"] == "omitted"
            and _span_identical(
                left["normalized_source_evidence"],
                right["normalized_source_evidence"],
            )
            and _span_identical(
                left["normalized_target_evidence"],
                right["normalized_target_evidence"],
            )
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
        "host_gate_facts": finding.get("host_gate_facts"),
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
    allow_identical_assessment: bool = False,
) -> dict[str, Any]:
    if left_assessment["sample_id"] != sample.get("sample_id") or right_assessment["sample_id"] != sample.get("sample_id"):
        raise ValidationError("quality v2 matching requires one sample identity")
    if (
        left_assessment["assessment_id"] == right_assessment["assessment_id"]
        and not allow_identical_assessment
    ):
        raise ValidationError("quality v2 matching requires two distinct assessments")
    if len(left_assessment["items"]) != len(sample["items"]) or len(right_assessment["items"]) != len(sample["items"]):
        raise ValidationError("quality v2 matching requires complete assessments")

    pending: list[dict[str, Any]] = []
    for sample_index, (sample_item, left_item, right_item) in enumerate(
        zip(sample["items"], left_assessment["items"], right_assessment["items"])
    ):
        revision_id = sample_item["revision_id"]
        if left_item["revision_id"] != revision_id or right_item["revision_id"] != revision_id:
            raise ValidationError("quality v2 matching found stale or out-of-order revision")
        left_findings = left_item["findings"]
        right_findings = right_item["findings"]
        manual_evidence: set[tuple[str, str, str]] = set()
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
        "sample_size": len(sample["items"]),
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
        host_gate_candidates = [
            member["normalized"].get("host_gate_facts")
            for member in issue_by_id[issue_id]["members"]
            if member["normalized"].get("host_gate_facts") is not None
        ]
        for field in (
            "technical_gate_confirmed", "runtime_broken",
            "single_item_display_broken",
        ):
            if facts.get(field) == "yes" and not any(
                candidate.get(field) == "yes" for candidate in host_gate_candidates
            ):
                raise ValidationError(
                    f"{where}.confirmed_facts.{field}=yes is not backed by a deterministic gate"
                )
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


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid {label}: {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{label} root must be an object")
    return value


def _exploratory_ids_from_loaded_inventory(
    manifest: Manifest,
    *,
    entries: list[dict[str, Any]],
    inventory_info: dict[str, Any],
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    official: dict[str, Any],
    features: dict[int, dict[str, Any]],
) -> set[str]:
    """Reproduce the v1 12-item dry-run selection without loading inventory again."""
    from .quality import (
        _constraint_counts,
        _contrast_groups,
        _select_bucket,
    )

    dry = qpolicy["dry_run"]
    official_ids = {item["revision_id"] for item in official["items"]}
    pool = [entry for entry in entries if entry["revision_id"] not in official_ids]
    rng = random.Random(dry["seed"])
    contrast: list[dict[str, Any]] = []
    group_order = list(_contrast_groups(pool, qpolicy))
    rng.shuffle(group_order)
    for _, members in group_order:
        if len(members) <= 4:
            contrast.extend(members)
            break
    selected = list(contrast)
    contrast_ids = {entry["revision_id"] for entry in contrast}
    remaining = [entry for entry in pool if entry["revision_id"] not in contrast_ids]
    selected.extend(
        _select_bucket(
            remaining,
            int(dry["size"]) - len(selected),
            selected,
            dry.get("coverage_constraints", []),
            rng,
            features,
        )
    )
    # Exercise the same constraint counter used by v1 so malformed policy cannot
    # silently yield a differently interpreted exploratory exclusion.
    _constraint_counts(selected, dry.get("coverage_constraints", []), features)
    if len(selected) != int(dry["size"]):
        raise ValidationError("cannot reproduce the exploratory quality sample")
    return {entry["revision_id"] for entry in selected}


def _atomic_sampling_units(
    entries: list[dict[str, Any]], qpolicy: dict[str, Any]
) -> list[list[dict[str, Any]]]:
    """Return contrast-connected components plus singleton inventory entries."""
    from .quality import _contrast_groups

    by_id = {entry["revision_id"]: entry for entry in entries}
    parent = {revision_id: revision_id for revision_id in by_id}

    def find(value: str) -> str:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    for _, members in _contrast_groups(entries, qpolicy):
        first = members[0]["revision_id"]
        for member in members[1:]:
            union(first, member["revision_id"])
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for revision_id, entry in by_id.items():
        grouped[find(revision_id)].append(entry)
    units = []
    for members in grouped.values():
        members.sort(key=lambda entry: (entry["unit_id"], entry["revision_id"]))
        units.append(members)
    units.sort(key=lambda members: (members[0]["unit_id"], members[0]["revision_id"]))
    return units


def _calibration_themes(entry: dict[str, Any]) -> set[str]:
    flags = set(entry.get("risk_flags", []))
    profile = entry.get("profile")
    themes: set[str] = set()
    if "source-has-number-or-unit" in flags:
        themes.add("number-unit")
    if "source-has-negation-or-condition" in flags:
        themes.add("logic")
    if entry.get("relevant_terms"):
        themes.add("terminology")
    if entry.get("context_neighbors") or entry.get("profile_confidence") != "high":
        themes.add("recoverable-context")
    if profile in {"narrative", "dialogue"}:
        themes.add("narrative-flavor")
    if profile in {"ui", "runtime-log", "term-name", "narrative", "dialogue"}:
        themes.add("presentation-style")
    if flags & {"has-printf", "has-args-order", "has-markup", "has-at-token", "multiline"}:
        themes.add("technical-structure")
    return themes


def _holdout_features(entry: dict[str, Any], qpolicy: dict[str, Any]) -> set[str]:
    from .quality import _entry_features

    base = _entry_features(entry, qpolicy)
    values = {
        f"profile:{base['profile']}",
        f"component-group:{base['component_group']}",
        f"length:{base['length_bin']}",
    }
    if base["structural_risk"]:
        values.add("structural-risk")
    if base["term_evidence"]:
        values.add("term-evidence")
    return values


def _scaled_targets(counts: Counter[str], size: int) -> dict[str, int]:
    total = sum(counts.values())
    if total <= 0:
        raise ValidationError("cannot scale an empty quality distribution")
    exact = {key: value * size / total for key, value in counts.items()}
    targets = {key: int(value) for key, value in exact.items()}
    remainder = size - sum(targets.values())
    order = sorted(counts, key=lambda key: (-(exact[key] - targets[key]), key))
    for key in order[:remainder]:
        targets[key] += 1
    return targets


def _select_atomic_units(
    units: list[list[dict[str, Any]]],
    *,
    size: int,
    seed: str,
    score_features: Any,
    minimums: dict[str, int],
    preferred_targets: dict[str, int] | None = None,
    maximums: dict[str, int] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rng = random.Random(seed)
    ranked = [(rng.random(), unit) for unit in units]
    selected: list[dict[str, Any]] = []
    selected_units: list[list[dict[str, Any]]] = []
    counts = Counter()
    observed: dict[str, set[str]] = defaultdict(set)
    remaining = list(ranked)
    feature_availability: Counter[str] = Counter()
    def _unit_feature_counts(unit: list[dict[str, Any]]) -> Counter[str]:
        coverage: Counter[str] = Counter()
        for entry in unit:
            values = score_features(entry)
            if isinstance(values, set):
                coverage.update(values)
            else:
                for feature, feature_value in values.items():
                    if feature_value:
                        coverage[feature] += 1
        return coverage

    for _, unit in ranked:
        feature_availability.update(_unit_feature_counts(unit))
    while len(selected) < size:
        capacity = size - len(selected)
        candidates = [
            (tie, unit)
            for tie, unit in remaining
            if len(unit) <= capacity
            and (
                not maximums
                or all(
                    counts[feature] + _unit_feature_counts(unit)[feature] <= maximum
                    for feature, maximum in maximums.items()
                )
            )
        ]
        if not candidates:
            raise ValidationError(f"cannot fill a {size}-item atomic quality dataset")

        def score(candidate: tuple[float, list[dict[str, Any]]]) -> tuple[float, int, float, int, float, str]:
            tie, unit = candidate
            gain = 0
            weighted_gain = 0.0
            coverage = _unit_feature_counts(unit)
            candidate_observed: dict[str, set[str]] = defaultdict(set)
            for feature, minimum in minimums.items():
                current = len(observed[feature]) if feature.endswith("-diversity") else counts[feature]
                addition = (
                    len(candidate_observed[feature] - observed[feature])
                    if feature.endswith("-diversity")
                    else coverage[feature]
                )
                deficit = max(0, minimum - current)
                useful = min(deficit, addition)
                gain += useful
                if useful:
                    weighted_gain += useful * (
                        1 / deficit + 100 / max(1, feature_availability[feature])
                    )
            distance_gain = 0.0
            if preferred_targets:
                for feature, target in preferred_targets.items():
                    current = counts[feature]
                    addition = coverage[feature]
                    distance_gain += abs(target - current) - abs(target - current - addition)
            # Prefer smaller units when gains tie so an exact final fill remains possible.
            return (
                weighted_gain, gain, distance_gain, -len(unit), -tie,
                unit[0]["revision_id"],
            )

        chosen = max(candidates, key=score)
        remaining.remove(chosen)
        unit = chosen[1]
        selected_units.append(unit)
        selected.extend(unit)
        for entry in unit:
            values = score_features(entry)
            if isinstance(values, set):
                counts.update(values)
            else:
                for feature, feature_value in values.items():
                    if feature.endswith("-diversity") and isinstance(feature_value, str):
                        observed[feature].add(feature_value)
                    elif feature_value:
                        counts[feature] += 1
    final_counts = {
        feature: len(observed[feature]) if feature.endswith("-diversity") else counts[feature]
        for feature in minimums
    }
    # Greedy multi-dimensional stratification can paint itself into a corner.
    # Deterministically repair with equal-sized unit swaps that strictly reduce
    # total constraint shortfall, preserving sample size and contrast atomicity.
    def unit_coverage(unit: list[dict[str, Any]]) -> Counter[str]:
        return _unit_feature_counts(unit)

    def shortfall(values: dict[str, int]) -> int:
        return sum(max(0, minimum - values.get(feature, 0)) for feature, minimum in minimums.items())

    current_shortfall = shortfall(final_counts)
    seen_selections = {
        tuple(sorted(entry["revision_id"] for unit in selected_units for entry in unit))
    }
    for _ in range(256):
        if current_shortfall == 0:
            break
        best: tuple[int, int, str, int, int, Counter[str], list[dict[str, Any]]] | None = None
        for candidate_index, (_, candidate) in enumerate(remaining):
            candidate_coverage = unit_coverage(candidate)
            if not any(
                final_counts.get(feature, 0) < minimum and candidate_coverage[feature]
                for feature, minimum in minimums.items()
            ):
                continue
            for victim_index, victim in enumerate(selected_units):
                if len(victim) != len(candidate):
                    continue
                victim_coverage = unit_coverage(victim)
                proposed = {
                    feature: final_counts.get(feature, 0)
                    - victim_coverage[feature]
                    + candidate_coverage[feature]
                    for feature in minimums
                }
                if maximums and any(
                    proposed.get(feature, final_counts.get(feature, 0)) > maximum
                    for feature, maximum in maximums.items()
                ):
                    continue
                improvement = current_shortfall - shortfall(proposed)
                direct_gain = sum(
                    min(
                        max(0, minimum - final_counts.get(feature, 0)),
                        candidate_coverage[feature],
                    )
                    for feature, minimum in minimums.items()
                )
                if improvement < 0 or direct_gain <= 0:
                    continue
                proposed_ids = tuple(
                    sorted(
                        entry["revision_id"]
                        for selected_index, selected_unit in enumerate(selected_units)
                        for entry in (candidate if selected_index == victim_index else selected_unit)
                    )
                )
                if proposed_ids in seen_selections:
                    continue
                key = (
                    improvement, direct_gain, candidate[0]["revision_id"],
                    -candidate_index, -victim_index, candidate_coverage, candidate,
                )
                if best is None or key[:5] > best[:5]:
                    best = key
        if best is None:
            break
        _, _, _, neg_candidate_index, neg_victim_index, candidate_coverage, candidate = best
        candidate_index, victim_index = -neg_candidate_index, -neg_victim_index
        victim = selected_units[victim_index]
        victim_coverage = unit_coverage(victim)
        selected_units[victim_index] = candidate
        remaining[candidate_index] = (remaining[candidate_index][0], victim)
        for feature in minimums:
            final_counts[feature] = (
                final_counts.get(feature, 0)
                - victim_coverage[feature]
                + candidate_coverage[feature]
            )
        current_shortfall = shortfall(final_counts)
        seen_selections.add(
            tuple(sorted(entry["revision_id"] for unit in selected_units for entry in unit))
        )
    selected = [entry for unit in selected_units for entry in unit]
    unmet = {feature: minimum - final_counts[feature] for feature, minimum in minimums.items() if final_counts[feature] < minimum}
    if unmet:
        detail = ", ".join(f"{feature}={minimums[feature] - deficit}/{minimums[feature]}" for feature, deficit in sorted(unmet.items()))
        raise ValidationError(f"quality dataset constraints are not satisfiable: {detail}")
    return selected, dict(sorted(final_counts.items()))


def _dataset_sample(
    *,
    manifest: Manifest,
    selected: list[dict[str, Any]],
    all_entries: list[dict[str, Any]],
    inventory_info: dict[str, Any],
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    v2policy: dict[str, Any],
    kind: str,
    coverage: dict[str, int],
    excluded_ids_sha256: str,
) -> dict[str, Any]:
    from .quality import _build_sample_items

    dataset = v2policy["datasets"][kind]
    selected_ids = {entry["revision_id"] for entry in selected}
    multi_units = [unit for unit in _atomic_sampling_units(selected, qpolicy) if len(unit) > 1]
    contrast_group_of: dict[str, str] = {}
    contrast: list[dict[str, Any]] = []
    for unit in multi_units:
        group_id = f"v2-contrast:{canonical_sha256([item['revision_id'] for item in unit])[:12]}"
        for entry in unit:
            contrast_group_of[entry["revision_id"]] = group_id
            contrast.append(entry)
    contrast_ids = set(contrast_group_of)
    enriched = set(qpolicy["risk_enrichment_flags"])
    risk_ids = {
        entry["revision_id"]
        for entry in selected
        if entry["revision_id"] not in contrast_ids
        and set(entry.get("risk_flags", [])) & enriched
    }
    # Keep every contrast-connected component contiguous while retaining a
    # deterministic order by each component's first canonical unit identity.
    ordered = [entry for unit in _atomic_sampling_units(selected, qpolicy) for entry in unit]
    items = _build_sample_items(
        entries=all_entries, ordered=ordered, contrast_ids=contrast_ids,
        risk_selected_ids=risk_ids, contrast_group_of=contrast_group_of,
        contrast=contrast, qpolicy=qpolicy,
    )
    identity = {
        "schema_version": 2,
        "quality_contract": dataset["contract"],
        "dataset_kind": kind,
        "seed": dataset["seed"],
        "size": dataset["size"],
        "taxonomy_sha256": canonical_sha256(taxonomy),
        "policy_v1_sha256": canonical_sha256(qpolicy),
        "policy_v2_sha256": canonical_sha256(v2policy),
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "inventory_sha256": inventory_info["inventory_sha256"],
        "excluded_ids_sha256": excluded_ids_sha256,
        "items_sha256": canonical_sha256(items),
        "revisions": [item["revision_id"] for item in items],
    }
    return {
        **identity,
        "sample_id": canonical_sha256(identity),
        "coverage": coverage,
        "items": items,
    }


def generate_calibration_holdout_v2(
    manifest: Manifest, inventory_path: Path
) -> dict[str, Any]:
    """Load inventory once and generate mutually-exclusive 32+32 v2 datasets."""
    from .quality import (
        _generate_sample_from_inventory,
        _load_sampling_inputs,
        _sampling_features,
    )

    entries, inventory_info, taxonomy, qpolicy = _load_sampling_inputs(manifest, inventory_path)
    features = _sampling_features(entries, qpolicy)
    official = _generate_sample_from_inventory(
        manifest, entries=entries, inventory_info=inventory_info,
        taxonomy=taxonomy, qpolicy=qpolicy, features=features,
    )
    exploratory_ids = _exploratory_ids_from_loaded_inventory(
        manifest, entries=entries, inventory_info=inventory_info,
        taxonomy=taxonomy, qpolicy=qpolicy, official=official, features=features,
    )
    official_ids = {item["revision_id"] for item in official["items"]}
    excluded = official_ids | exploratory_ids
    pool = [entry for entry in entries if entry["revision_id"] not in excluded]
    units = _atomic_sampling_units(pool, qpolicy)
    v2policy = load_policy_v2(manifest)
    calibration_spec = v2policy["datasets"]["calibration"]
    calibration_minimums = {
        item["id"]: item["min"] for item in v2policy["calibration_constraints"]
    }
    calibration_selected, calibration_coverage = _select_atomic_units(
        units, size=calibration_spec["size"], seed=calibration_spec["seed"],
        score_features=_calibration_themes, minimums=calibration_minimums,
    )
    calibration_ids = {entry["revision_id"] for entry in calibration_selected}
    holdout_pool = [entry for entry in pool if entry["revision_id"] not in calibration_ids]
    holdout_units = _atomic_sampling_units(holdout_pool, qpolicy)
    holdout_spec = v2policy["datasets"]["holdout"]
    from .quality import _component_group

    holdout_minimums = {
        item["id"]: item["min"]
        for item in v2policy["holdout_constraints"]
        if item["id"] in {"structural-risk", "term-evidence"}
    }
    distribution_dimensions = {
        "profile": Counter(item["profile"] for item in official["items"]),
        "component-group": Counter(
            _component_group(item["component"], qpolicy) for item in official["items"]
        ),
        "length": Counter(item["source_length_bin"] for item in official["items"]),
    }
    holdout_targets: dict[str, int] = {}
    for dimension, counts in distribution_dimensions.items():
        for value, target in _scaled_targets(counts, holdout_spec["size"]).items():
            holdout_targets[f"{dimension}:{value}"] = target
            # Preserve the formal distribution within two items per stratum.
            # Exact simultaneous marginals across three dimensions can be
            # impossible for an atomic 32-item subset.
            if dimension == "profile":
                holdout_minimums[f"{dimension}:{value}"] = target
            elif dimension == "component-group":
                holdout_minimums[f"{dimension}:{value}"] = max(1, target - 2)
            elif dimension == "length":
                holdout_minimums[f"{dimension}:{value}"] = max(1, target - 3)
    holdout_maximums = {
        feature: target
        for feature, target in holdout_targets.items()
        if feature.startswith("profile:")
    }
    holdout_selected, holdout_coverage = _select_atomic_units(
        holdout_units, size=holdout_spec["size"], seed=holdout_spec["seed"],
        score_features=lambda entry: _holdout_features(entry, qpolicy),
        minimums=holdout_minimums, preferred_targets=holdout_targets,
        maximums=holdout_maximums,
    )
    excluded_hash = canonical_sha256(sorted(excluded))
    calibration = _dataset_sample(
        manifest=manifest, selected=calibration_selected, all_entries=entries,
        inventory_info=inventory_info, taxonomy=taxonomy, qpolicy=qpolicy,
        v2policy=v2policy, kind="calibration", coverage=calibration_coverage,
        excluded_ids_sha256=excluded_hash,
    )
    holdout = _dataset_sample(
        manifest=manifest, selected=holdout_selected, all_entries=entries,
        inventory_info=inventory_info, taxonomy=taxonomy, qpolicy=qpolicy,
        v2policy=v2policy, kind="holdout", coverage=holdout_coverage,
        excluded_ids_sha256=canonical_sha256(sorted(excluded | calibration_ids)),
    )
    holdout_ids = set(holdout["revisions"])
    if calibration_ids & holdout_ids or calibration_ids & excluded or holdout_ids & excluded:
        raise ValidationError("quality v2 dataset isolation invariant failed")
    return {
        "calibration": calibration,
        "holdout": holdout,
        "official_sample_id": official["sample_id"],
        "official_revision_ids": sorted(official_ids),
        "exploratory_revision_ids": sorted(exploratory_ids),
        "inventory_entries": len(entries),
        "inventory_loads": 1,
    }


def run_calibration_v2(manifest: Manifest, inventory_path: Path) -> dict[str, Any]:
    from .quality import create_quality_run_directory
    from .report import write_json

    generated = generate_calibration_holdout_v2(manifest, inventory_path)
    run_directory = create_quality_run_directory(manifest.root, "calibration-v2")
    calibration_path = run_directory / "calibration.json"
    holdout_path = run_directory / "holdout.json"
    manifest_path = run_directory / "dataset-manifest.json"
    write_json(calibration_path, generated["calibration"])
    write_json(holdout_path, generated["holdout"])
    record = {
        "schema_version": 2,
        "quality_contract": "tome4-quality-dataset-manifest-v2",
        "calibration_id": generated["calibration"]["sample_id"],
        "holdout_id": generated["holdout"]["sample_id"],
        "official_sample_id": generated["official_sample_id"],
        "official_revision_ids": generated["official_revision_ids"],
        "exploratory_revision_ids": generated["exploratory_revision_ids"],
        "inventory_entries": generated["inventory_entries"],
        "inventory_loads": generated["inventory_loads"],
        "calibration": str(calibration_path),
        "holdout": str(holdout_path),
        "run_directory": str(run_directory),
    }
    write_json(manifest_path, record)
    record["manifest"] = str(manifest_path)
    return record


def _sample_safety(value: Any, where: str = "sample") -> None:
    from .quality import HOST_ABSOLUTE_PATH_RE, WINDOWS_PATH_RE, DOTDOT_PATH_RE

    if isinstance(value, dict):
        for key, item in value.items():
            _sample_safety(item, f"{where}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _sample_safety(item, f"{where}[{index}]")
    elif isinstance(value, str) and (
        HOST_ABSOLUTE_PATH_RE.search(value)
        or WINDOWS_PATH_RE.search(value)
        or DOTDOT_PATH_RE.search(value)
    ):
        raise ValidationError(f"{where} contains a forbidden host path")


def validate_sample_v2(sample: dict[str, Any]) -> dict[str, Any]:
    if sample.get("quality_contract") not in {CALIBRATION_CONTRACT, HOLDOUT_CONTRACT}:
        raise ValidationError("unsupported quality v2 sample contract")
    if sample.get("schema_version") != 2 or sample.get("dataset_kind") not in {"calibration", "holdout"}:
        raise ValidationError("invalid quality v2 sample header")
    items = sample.get("items")
    if not isinstance(items, list) or not items or sample.get("size") != len(items):
        raise ValidationError("quality v2 sample size/items mismatch")
    revisions = [item.get("revision_id") for item in items if isinstance(item, dict)]
    if len(revisions) != len(items) or len(revisions) != len(set(revisions)):
        raise ValidationError("quality v2 sample revisions must be complete and unique")
    if revisions != sample.get("revisions") or canonical_sha256(items) != sample.get("items_sha256"):
        raise ValidationError("quality v2 sample item identity does not match")
    identity_fields = {
        key: sample[key]
        for key in (
            "schema_version", "quality_contract", "dataset_kind", "seed", "size",
            "taxonomy_sha256", "policy_v1_sha256", "policy_v2_sha256",
            "manifest_sha256", "inventory_sha256", "excluded_ids_sha256",
            "items_sha256", "revisions",
        )
    }
    if canonical_sha256(identity_fields) != sample.get("sample_id"):
        raise ValidationError("quality v2 sample_id does not match")
    _sample_safety(sample)
    return sample


def build_evaluator_bundles_v2(
    *,
    sample: dict[str, Any],
    evaluator_id: str,
    policy: dict[str, Any],
    rules: dict[str, Any],
    anchors: dict[str, Any],
    taxonomy: dict[str, Any],
    max_items: int = 20,
) -> list[dict[str, Any]]:
    validate_sample_v2(sample)
    _enum(evaluator_id, policy["evaluator_ids"], "evaluator_id")
    if type(max_items) is not int or not 1 <= max_items <= policy["max_shard_items"]:
        raise ValidationError(f"max_items must be between 1 and {policy['max_shard_items']}")
    items = sample["items"]
    group_positions: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(items):
        group = item.get("contrast_group")
        if group is not None:
            group_positions[group].append(index)
    forbidden_cuts = {
        cut
        for positions in group_positions.values()
        for cut in range(min(positions) + 1, max(positions) + 1)
    }
    ranges: list[tuple[int, int]] = []
    start = 0
    while start < len(items):
        limit = min(len(items), start + max_items)
        allowed = [cut for cut in range(start + 1, limit + 1) if cut not in forbidden_cuts]
        if not allowed:
            raise ValidationError("a contrast group cannot fit within the shard item limit")
        end = max(allowed)
        ranges.append((start, end))
        start = end
    prompt_fields = {
        "method_version": METHOD_V2,
        "allowed_profiles": [item["id"] for item in taxonomy["profiles"]],
        "allowed_error_codes": [item["code"] for item in taxonomy["error_codes"]],
        "defect_classes": policy["defect_classes"],
        "phenomena": policy["phenomena"],
        "meaning_change_types": policy["meaning_change_types"],
        "impact_fact_fields": policy["impact_fact_fields"],
        "tri_state_values": policy["tri_state_values"],
        "amplification_scopes": policy["amplification_scopes"],
        "anchor_relations": policy["anchor_relations"],
        "reuse_recommendations": policy["reuse_recommendations"],
        "impact_rules": rules,
        "anchors": anchors,
    }
    bundles = []
    for index, (first, end) in enumerate(ranges, start=1):
        bundle = {
            "schema_version": 2,
            "quality_contract": EVALUATOR_BUNDLE_V2_CONTRACT,
            "sample_contract": sample["quality_contract"],
            "sample_id": sample["sample_id"],
            "evaluator_id": evaluator_id,
            "finding_id_prefix": "A" if evaluator_id == "reviewer-a" else "B",
            "shard_index": index,
            "shard_count": len(ranges),
            "first_sample_index": first,
            **prompt_fields,
            "items": items[first:end],
            "bundle_id": "",
        }
        bundle["bundle_id"] = canonical_sha256({key: value for key, value in bundle.items() if key != "bundle_id"})
        bundles.append(bundle)
    if [item["revision_id"] for bundle in bundles for item in bundle["items"]] != sample["revisions"]:
        raise ValidationError("quality evaluator shards do not reconstruct sample order")
    return bundles


def run_evaluator_bundles_v2(
    manifest: Manifest,
    *,
    sample_path: Path,
    evaluator_id: str,
    max_items: int = 20,
) -> dict[str, Any]:
    from .quality import create_quality_run_directory, load_taxonomy
    from .report import write_json

    sample = validate_sample_v2(read_json_object(sample_path, "quality v2 sample"))
    policy = load_policy_v2(manifest)
    rules = load_impact_rules(manifest, policy)
    taxonomy = load_taxonomy(manifest)
    anchors = load_anchors(
        manifest, policy=policy, rules=rules, taxonomy=taxonomy
    )
    bundles = build_evaluator_bundles_v2(
        sample=sample, evaluator_id=evaluator_id, policy=policy, rules=rules,
        anchors=anchors, taxonomy=taxonomy, max_items=max_items,
    )
    run_directory = create_quality_run_directory(manifest.root, "evaluator-shards-v2")
    paths = []
    for bundle in bundles:
        path = run_directory / f"shard-{bundle['shard_index']:03d}.json"
        write_json(path, bundle)
        paths.append(str(path))
    index = {
        "schema_version": 2,
        "quality_contract": "tome4-quality-evaluator-shard-index-v2",
        "sample_id": sample["sample_id"], "evaluator_id": evaluator_id,
        "max_items": max_items, "shard_count": len(bundles),
        "bundle_ids": [bundle["bundle_id"] for bundle in bundles],
        "shards": paths, "run_directory": str(run_directory),
    }
    index["index_id"] = canonical_sha256(index)
    index_path = run_directory / "shard-index.json"
    write_json(index_path, index)
    index["index"] = str(index_path)
    return index


def build_report_v2(
    *, match: dict[str, Any], adjudication_validation: dict[str, Any] | None = None
) -> dict[str, Any]:
    issues = match["issues"]
    revisions = {issue["revision_id"] for issue in issues}
    cluster_counts = Counter(issue["cluster_type"] for issue in issues)
    left_count = sum(
        member["side"] == "left" for issue in issues for member in issue["members"]
    )
    right_count = sum(
        member["side"] == "right" for issue in issues for member in issue["members"]
    )
    both = sum(
        {member["side"] for member in issue["members"]} == {"left", "right"}
        for issue in issues
    )
    union = len(issues)
    fact_fields = set()
    for issue in issues:
        for member in issue["members"]:
            fact_fields.update(member["normalized"]["impact_facts"])
    fact_metrics = {}
    for field in sorted(fact_fields):
        compared = agreed = unknown = 0
        for issue in issues:
            left_values = [member["normalized"]["impact_facts"][field] for member in issue["members"] if member["side"] == "left"]
            right_values = [member["normalized"]["impact_facts"][field] for member in issue["members"] if member["side"] == "right"]
            if len(left_values) == len(right_values) == 1 and issue["cluster_type"] in {"full-match", "partial-match"}:
                compared += 1
                agreed += left_values[0] == right_values[0]
                unknown += "unknown" in {left_values[0], right_values[0]}
        fact_metrics[field] = {
            "compared": compared, "agreed": agreed,
            "agreement_rate": agreed / compared if compared else None,
            "unknown_pairs": unknown,
        }
    derived_counts = Counter(issue["derivation"]["derived_severity"] for issue in issues)
    adjudicated_counts = Counter()
    adjudicated = 0
    if adjudication_validation is not None:
        if adjudication_validation.get("match_id") != match.get("match_id"):
            raise ValidationError("report adjudication validation match_id differs")
        adjudicated = len(adjudication_validation["items"])
        adjudicated_counts.update(
            item["derivation"]["derived_severity"]
            for item in adjudication_validation["items"]
        )
    manual_revision_count = len(
        {issue["revision_id"] for issue in issues if issue["issue_id"] in set(match["manual_queue"])}
    )
    report = {
        "schema_version": 2, "quality_contract": "tome4-quality-report-v2",
        "match_id": match["match_id"], "report_id": "",
        "item_metrics": {
            "items_total": match.get("sample_size"),
            "items_with_findings": len(revisions),
            "items_requiring_adjudication": manual_revision_count,
        },
        "issue_metrics": {
            "left_findings": left_count, "right_findings": right_count,
            "issue_union": union, "issue_intersection": both,
            "jaccard": both / union if union else 1.0,
            "cluster_counts": dict(sorted(cluster_counts.items())),
        },
        "fact_metrics": fact_metrics,
        "severity_metrics": {
            "pre_adjudication": dict(sorted(derived_counts.items())),
            "adjudicated": dict(sorted(adjudicated_counts.items())),
        },
        "human_burden": {
            "issues_requiring_adjudication": len(match["manual_queue"]),
            "issues_adjudicated": adjudicated,
            "issue_rate": len(match["manual_queue"]) / union if union else 0.0,
            "items_requiring_adjudication": manual_revision_count,
        },
    }
    report["report_id"] = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
    return report


def validate_stability_preregistration_v2(
    preregistration: dict[str, Any],
    *,
    sample: dict[str, Any],
    policy: dict[str, Any],
    rules: dict[str, Any],
    anchors: dict[str, Any],
    prompt_sha256: str,
) -> dict[str, Any]:
    _exact_fields(
        preregistration,
        (
            "contract", "schema_version", "sample_contract", "sample_id",
            "evaluators", "thresholds", "frozen_inputs",
            "connection_failure_retry_limit", "replace_content_failures",
            "preregistration_id",
        ),
        "quality stability preregistration",
    )
    if (
        preregistration["contract"]
        != "tome4-quality-stability-preregistration-v1"
        or preregistration["schema_version"] != 1
    ):
        raise ValidationError("unsupported quality stability preregistration")
    if (
        preregistration["sample_contract"] != CALIBRATION_CONTRACT
        or preregistration["sample_id"] != sample.get("sample_id")
    ):
        raise ValidationError("stability preregistration sample identity differs")
    evaluators = preregistration["evaluators"]
    if not isinstance(evaluators, list) or len(evaluators) != 2:
        raise ValidationError("stability preregistration requires two evaluators")
    received_ids = []
    for index, evaluator in enumerate(evaluators):
        where = f"quality stability preregistration.evaluators[{index}]"
        if not isinstance(evaluator, dict):
            raise ValidationError(f"{where} must be an object")
        _exact_fields(
            evaluator, ("id", "provider", "model", "thinking", "runs"), where
        )
        received_ids.append(_string(evaluator["id"], f"{where}.id"))
        for field in ("provider", "model", "thinking"):
            _string(evaluator[field], f"{where}.{field}")
        if evaluator["runs"] != 2:
            raise ValidationError(f"{where}.runs must be exact integer 2")
    if received_ids != policy["evaluator_ids"]:
        raise ValidationError("stability preregistration evaluator order differs")
    thresholds = preregistration["thresholds"]
    expected_thresholds = {
        "schema_coverage": 1.0,
        "structure_failures_max": 0,
        "finding_jaccard_min": 0.70,
        "critical_fact_agreement_min": 0.80,
        "derived_severity_agreement_min": 0.90,
    }
    if thresholds != expected_thresholds:
        raise ValidationError("stability preregistration thresholds are not frozen values")
    frozen = preregistration["frozen_inputs"]
    _exact_fields(
        frozen,
        ("policy_v2_sha256", "prompt_sha256", "rules_sha256", "anchors_sha256"),
        "quality stability preregistration.frozen_inputs",
    )
    current_policy_sha256 = canonical_sha256(policy)
    if sample.get("policy_v2_sha256") != current_policy_sha256:
        raise ValidationError("stability sample policy_v2_sha256 is stale")
    expected_frozen = {
        "policy_v2_sha256": current_policy_sha256,
        "prompt_sha256": prompt_sha256,
        "rules_sha256": canonical_sha256(rules),
        "anchors_sha256": canonical_sha256(anchors),
    }
    for field, expected in expected_frozen.items():
        _sha(frozen[field], f"quality stability preregistration.frozen_inputs.{field}")
        if frozen[field] != expected:
            raise ValidationError(f"stability preregistration {field} differs")
    if preregistration["connection_failure_retry_limit"] != 1:
        raise ValidationError("stability connection retry limit must be 1")
    if preregistration["replace_content_failures"] is not False:
        raise ValidationError("stability content failures cannot be replaced")
    expected_id = canonical_sha256(
        {key: value for key, value in preregistration.items() if key != "preregistration_id"}
    )
    if preregistration["preregistration_id"] != expected_id:
        raise ValidationError("stability preregistration_id does not match")
    return preregistration


def build_stability_report_v2(
    *,
    sample: dict[str, Any],
    assessments: tuple[dict[str, Any], dict[str, Any]],
    run_reports: tuple[dict[str, Any], dict[str, Any]],
    assessment_sha256s: tuple[str, str],
    run_report_sha256s: tuple[str, str],
    preregistration: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    left, right = assessments
    if left["evaluator"] != right["evaluator"]:
        raise ValidationError("stability assessments must use one frozen evaluator identity")
    evaluator = left["evaluator"]
    registered = next(
        (item for item in preregistration["evaluators"] if item["id"] == evaluator["id"]),
        None,
    )
    if registered is None or any(
        registered[field] != evaluator[field]
        for field in ("id", "provider", "model", "thinking")
    ):
        raise ValidationError("stability evaluator differs from preregistration")
    if run_report_sha256s[0] == run_report_sha256s[1]:
        raise ValidationError("stability requires two distinct runner reports")
    for index, (run_report, assessment_sha256) in enumerate(
        zip(run_reports, assessment_sha256s)
    ):
        where = f"quality stability run_reports[{index}]"
        expected = {
            "ok": True,
            "mode": "blind-quality-assessment-v2",
            "sample_id": sample["sample_id"],
            "evaluator_id": evaluator["id"],
            "provider": evaluator["provider"],
            "model": evaluator["model"],
            "thinking": evaluator["thinking"],
            "prompt_sha256": evaluator["prompt_sha256"],
            "rules_sha256": evaluator["rules_sha256"],
            "anchors_sha256": evaluator["anchors_sha256"],
            "bundle_ids": evaluator["bundle_ids"],
            "assessment_sha256": assessment_sha256,
            "validated_results": 1,
        }
        if any(run_report.get(field) != value for field, value in expected.items()):
            raise ValidationError(f"{where} identity or success state differs")
        if run_report.get("cache_decision") not in {"miss", "bypass"}:
            raise ValidationError(f"{where} must represent a real non-cache execution")
        shards = run_report.get("shards")
        if (
            type(shards) is not int
            or shards < 1
            or run_report.get("attempts") != shards
            or run_report.get("charged_or_possible_transfers") != shards
        ):
            raise ValidationError(f"{where} shard transfer accounting differs")
    match = match_assessments_v2(
        sample=sample,
        left_assessment=left,
        right_assessment=right,
        policy=policy,
        allow_identical_assessment=True,
    )
    issues = match["issues"]
    matched = [
        issue
        for issue in issues
        if issue["cluster_type"] in {"full-match", "partial-match"}
        and len(issue["members"]) == 2
    ]
    union = len(issues)
    finding_jaccard = len(matched) / union if union else 1.0
    critical_compared = critical_agreed = 0
    severity_compared = severity_agreed = 0
    for issue in matched:
        members = sorted(issue["members"], key=lambda item: item["side"])
        left_finding, right_finding = [item["normalized"] for item in members]
        for field in policy["critical_impact_facts"]:
            critical_compared += 1
            critical_agreed += (
                left_finding["impact_facts"][field]
                == right_finding["impact_facts"][field]
            )
        severity_compared += 1
        severity_agreed += (
            left_finding["derivation"]["derived_severity"]
            == right_finding["derivation"]["derived_severity"]
        )
    substantive_presence = []
    for assessment in assessments:
        substantive_presence.append(
            [
                any(
                    finding["impact_facts"]["is_defect"] == "yes"
                    and finding["impact_facts"]["is_substantive"] == "yes"
                    for finding in item["findings"]
                )
                for item in assessment["items"]
            ]
        )
    item_agreed = sum(
        left_value == right_value
        for left_value, right_value in zip(*substantive_presence)
    )
    thresholds = preregistration["thresholds"]
    metrics = {
        "schema_coverage": 1.0,
        "structure_failures": 0,
        "finding_jaccard": finding_jaccard,
        "critical_fact_agreement": (
            critical_agreed / critical_compared if critical_compared else 1.0
        ),
        "derived_severity_agreement": (
            severity_agreed / severity_compared if severity_compared else 1.0
        ),
        "substantive_item_agreement": item_agreed / len(sample["items"]),
        "finding_union": union,
        "finding_intersection": len(matched),
        "critical_facts_compared": critical_compared,
        "severities_compared": severity_compared,
    }
    checks = {
        "schema_coverage": metrics["schema_coverage"] >= thresholds["schema_coverage"],
        "structure_failures": metrics["structure_failures"] <= thresholds["structure_failures_max"],
        "finding_jaccard": metrics["finding_jaccard"] >= thresholds["finding_jaccard_min"],
        "critical_fact_agreement": metrics["critical_fact_agreement"] >= thresholds["critical_fact_agreement_min"],
        "derived_severity_agreement": metrics["derived_severity_agreement"] >= thresholds["derived_severity_agreement_min"],
    }
    report = {
        "schema_version": 2,
        "quality_contract": "tome4-quality-stability-report-v2",
        "sample_id": sample["sample_id"],
        "preregistration_id": preregistration["preregistration_id"],
        "evaluator": {
            key: evaluator[key] for key in ("id", "provider", "model", "thinking")
        },
        "assessment_ids": [left["assessment_id"], right["assessment_id"]],
        "assessment_sha256s": list(assessment_sha256s),
        "run_report_sha256s": list(run_report_sha256s),
        "metrics": metrics,
        "checks": checks,
        "passed": all(checks.values()),
        "report_id": "",
    }
    report["report_id"] = canonical_sha256(
        {key: value for key, value in report.items() if key != "report_id"}
    )
    return report
