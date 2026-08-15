"""Translation quality: revision inventory, sampling, validation and reports.

Implements phase 1 of the translation quality system
(docs/translation-quality-phase-1.md, docs/translation-quality-system.md).
All outputs are derived artifacts under .artifacts/i18n/quality/runs/ and
never modify canonical Lua, terminology or release repositories.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import TOOL_VERSION
from .config import Manifest
from .errors import ConfigurationError, ValidationError
from .identity import revision_uid, source_sha256, tu_uid_fallback
from .lint import (
    AT_TOKEN_RE,
    FORMAT_TAGS,
    MARKUP_RE,
    extract_format_tokens,
    stable_entry_id,
)
from .locale_model import LocaleLoader
from .report import atomic_write_bytes, write_json
from .semantics import json_value_signature, runtime_semantic_signature
from .workset import _plain_source, _scope_matches, _source_tag_matches

QUALITY_ROOT = "i18n/quality"
TAXONOMY_FILE = "taxonomy-v1.json"
POLICY_FILE = "policy-v1.json"
INVENTORY_CONTRACT = "tome4-quality-inventory-v1"
SAMPLE_CONTRACT = "tome4-quality-sample-v1"
ASSESSMENT_CONTRACT = "tome4-quality-assessment-v1"
ADJUDICATION_CONTRACT = "tome4-quality-adjudication-v1"
VALIDATION_CONTRACT = "tome4-quality-validation-v1"
DRY_RUN_CONTRACT = "tome4-quality-dry-run-v1"
REPORT_CONTRACT = "tome4-quality-report-v1"
IDENTITY_CONTRACT = "tome4-translation-revision-v1"
DEFAULT_SAMPLE_SEED = "tome4-quality-pilot-v1"

_IDENTITY_CURRENT_ROOT = ".artifacts/i18n/identity/current"

_PROFILE_CONFIDENCE_ORDER = ("low", "medium", "high")
_PILOT_BUCKETS = ("representative", "risk-enriched", "contrast")
_CONSTRAINT_STRING_FEATURES = {"profile", "component_group", "length_bin"}
_CONSTRAINT_BOOL_FEATURES = {"structural_risk", "term_evidence"}
_CONSTRAINT_FEATURES = _CONSTRAINT_STRING_FEATURES | _CONSTRAINT_BOOL_FEATURES

_REQUIRED_TAXONOMY_PROFILES = frozenset(
    {"ui", "mechanics", "narrative", "unknown"}
)
_EXACT_TAXONOMY_IDS = {
    "severities": frozenset({"note", "minor", "major", "blocker"}),
    "confidence_levels": frozenset({"C0", "C1", "C2", "C3", "C4"}),
    "grades": frozenset({"Gold", "Silver", "Candidate", "Quarantine"}),
    "reuse_scopes": frozenset(
        {"general", "same-domain", "same-tag", "exact-context", "no-reuse"}
    ),
}

_SAMPLE_IDENTITY_FIELDS = {
    SAMPLE_CONTRACT: (
        "schema_version",
        "quality_contract",
        "seed",
        "size",
        "taxonomy_sha256",
        "policy_sha256",
        "manifest_sha256",
        "translation_inputs_sha256",
        "terminology_sha256",
        "inventory_tool_version",
        "inventory_sha256",
        "items_sha256",
        "bucket_targets",
        "bucket_counts",
        "revisions",
    ),
    DRY_RUN_CONTRACT: (
        "schema_version",
        "quality_contract",
        "seed",
        "size",
        "official_sample_id",
        "taxonomy_sha256",
        "policy_sha256",
        "manifest_sha256",
        "translation_inputs_sha256",
        "terminology_sha256",
        "inventory_tool_version",
        "inventory_sha256",
        "items_sha256",
        "revisions",
    ),
}

NEGATION_RE = re.compile(
    r"\b(?:no|not|never|none|without|unless|except|cannot|can't|won't|"
    r"don't|doesn't|didn't|isn't|aren't|hasn't|haven't|no longer|only if)\b",
    re.IGNORECASE,
)
CONDITION_RE = re.compile(
    r"\b(?:if|when|while|unless|only if|as long as|whenever)\b",
    re.IGNORECASE,
)
UNIT_WORD_RE = re.compile(
    r"\b(?:turns?|damage|radius|range|duration|chance|cooldown|seconds?|"
    r"minutes?|tiles?|yards?|meters?|percent|resistance|armou?r|mana|"
    r"stamina|life|health|speed|power)\b",
    re.IGNORECASE,
)
ASCII_WORD_RE = re.compile(r"[A-Za-z]{4,}")
SENTENCE_PUNCT_RE = re.compile(r"[.!?。！？]")
DIGIT_RE = re.compile(r"\d")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
HOST_ABSOLUTE_PATH_RE = re.compile(
    r"/(?:Users|home|tmp|var|opt|usr|private|Volumes|etc|bin|sbin|dev|"
    r"mnt|media|root|run|srv|Applications)/"
)
WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\")
DOTDOT_PATH_RE = re.compile(r"(?:^|/)\.\.(?:/|$)")
LENGTH_OUTLIER_MAX_RATIO = 4.0
LENGTH_OUTLIER_MIN_RATIO = 0.25
LONG_SOURCE_LENGTH = 200
MAX_DOMAIN_HINTS = 5

_TERMINOLOGY_FIELDS = (
    "source",
    "target",
    "category",
    "domain",
    "source_tag",
    "status",
    "scope",
    "notes",
)


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _translation_input_locations(
    manifest: Manifest,
) -> Iterable[tuple[str, str, str]]:
    """Yield every canonical locale input in its manifest consumption order."""
    for component in manifest.components:
        if component.copy_fragment:
            yield component.id, "copy_fragment", component.copy_fragment
        yield component.id, "translation", component.translation


def _translation_input_record(
    component: str,
    role: str,
    logical_path: str,
    sha256: str,
) -> dict[str, str]:
    return {
        "component": component,
        "role": role,
        "logical_path": logical_path,
        "sha256": sha256,
    }


def _current_translation_inputs_sha256(manifest: Manifest) -> str:
    """Hash current canonical locale bytes without loading or parsing Lua."""
    records: list[dict[str, str]] = []
    for component, role, logical_path in _translation_input_locations(manifest):
        path = manifest.root / logical_path
        try:
            raw = path.read_bytes()
        except OSError as error:
            raise ValidationError(
                "cannot read canonical translation input "
                f"{component}.{role} ({logical_path}): {error}"
            ) from error
        records.append(
            _translation_input_record(
                component,
                role,
                logical_path,
                hashlib.sha256(raw).hexdigest(),
            )
        )
    return _canonical_sha256(records)


def _sample_identity(sample: dict[str, Any]) -> dict[str, Any]:
    """Return exactly the canonical fields used to generate a sample id."""
    contract = sample.get("quality_contract")
    fields = _SAMPLE_IDENTITY_FIELDS.get(contract)
    if fields is None:
        raise ValidationError("unsupported quality sample identity contract")
    return {field: sample.get(field) for field in fields}


def _read_json(path: Path, label: str) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    try:
        data = json.loads(resolved.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {resolved}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid {label} JSON: {resolved}: {error}") from error
    if not isinstance(data, dict):
        raise ValidationError(f"{label} root must be an object: {resolved}")
    return data


def _read_json_lines(path: Path, label: str) -> list[dict[str, Any]]:
    resolved = path.expanduser().resolve()
    try:
        lines = resolved.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {resolved}") from error
    except UnicodeDecodeError as error:
        raise ValidationError(f"invalid {label} encoding: {resolved}: {error}") from error
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid {label} JSON at {resolved}:{line_number}: {error}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(f"invalid {label} record at {resolved}:{line_number}")
        records.append(record)
    return records


def _quality_taxonomy_error(path: str, requirement: str) -> None:
    raise ConfigurationError(f"quality taxonomy.{path} {requirement}")


def _validate_taxonomy_object_array(
    data: dict[str, Any], path: str, id_field: str
) -> tuple[list[dict[str, Any]], set[str]]:
    value = data.get(path)
    if not isinstance(value, list) or not value:
        _quality_taxonomy_error(path, "must be a non-empty array")

    seen_ids: dict[str, int] = {}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            _quality_taxonomy_error(item_path, "must be an object")
        item_id = item.get(id_field)
        if not isinstance(item_id, str) or not item_id:
            _quality_taxonomy_error(
                f"{item_path}.{id_field}", "must be a non-empty string"
            )
        if item_id in seen_ids:
            _quality_taxonomy_error(
                f"{item_path}.{id_field}",
                f"must be unique (duplicates quality taxonomy."
                f"{path}[{seen_ids[item_id]}].{id_field})",
            )
        seen_ids[item_id] = index
    return value, set(seen_ids)


def _validate_taxonomy_string_array(
    data: dict[str, Any], path: str
) -> tuple[list[str], set[str]]:
    value = data.get(path)
    if not isinstance(value, list) or not value:
        _quality_taxonomy_error(path, "must be a non-empty array")

    seen_values: dict[str, int] = {}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, str) or not item:
            _quality_taxonomy_error(item_path, "must be a non-empty string")
        if item in seen_values:
            _quality_taxonomy_error(
                item_path,
                f"must be unique (duplicates quality taxonomy."
                f"{path}[{seen_values[item]}])",
            )
        seen_values[item] = index
    return value, set(seen_values)


def _validate_taxonomy_profile_map(
    data: dict[str, Any], path: str, profiles: set[str]
) -> None:
    value = data.get(path)
    if not isinstance(value, dict):
        _quality_taxonomy_error(path, "must be an object")
    for key, profile in value.items():
        item_path = f"{path}[{key!r}]"
        if not isinstance(key, str) or not key:
            _quality_taxonomy_error(
                item_path, "key must be a non-empty string"
            )
        if not isinstance(profile, str) or profile not in profiles:
            _quality_taxonomy_error(
                item_path, "must reference a declared profile"
            )


def _validate_taxonomy_length_bins(data: dict[str, Any]) -> None:
    bins = data.get("length_bins")
    if not isinstance(bins, list) or not bins:
        _quality_taxonomy_error("length_bins", "must be a non-empty array")

    seen_ids: dict[str, int] = {}
    previous_maximum: int | None = None
    for index, bin_spec in enumerate(bins):
        bin_path = f"length_bins[{index}]"
        if not isinstance(bin_spec, dict):
            _quality_taxonomy_error(bin_path, "must be an object")

        bin_id = bin_spec.get("id")
        if not isinstance(bin_id, str) or not bin_id:
            _quality_taxonomy_error(
                f"{bin_path}.id", "must be a non-empty string"
            )
        if bin_id in seen_ids:
            _quality_taxonomy_error(
                f"{bin_path}.id",
                f"must be unique (duplicates quality taxonomy."
                f"length_bins[{seen_ids[bin_id]}].id)",
            )
        seen_ids[bin_id] = index

        if "max" not in bin_spec:
            _quality_taxonomy_error(f"{bin_path}.max", "is required")
        maximum = bin_spec["max"]
        if maximum is None:
            if index != len(bins) - 1:
                _quality_taxonomy_error(
                    f"{bin_path}.max", "may be null only in the last bin"
                )
            continue
        if type(maximum) is not int or maximum <= 0:
            _quality_taxonomy_error(
                f"{bin_path}.max",
                "must be an exact positive integer or null",
            )
        if previous_maximum is not None and maximum <= previous_maximum:
            _quality_taxonomy_error(
                f"{bin_path}.max",
                "must be strictly greater than the previous finite maximum",
            )
        previous_maximum = maximum

    if bins[-1]["max"] is not None:
        _quality_taxonomy_error(
            f"length_bins[{len(bins) - 1}].max", "must be null in the last bin"
        )


def _validate_quality_taxonomy(data: dict[str, Any]) -> None:
    object_arrays: dict[str, tuple[list[dict[str, Any]], set[str]]] = {}
    for path, id_field in (
        ("profiles", "id"),
        ("severities", "id"),
        ("error_codes", "code"),
        ("reuse_scopes", "id"),
        ("confidence_levels", "id"),
        ("grades", "id"),
    ):
        object_arrays[path] = _validate_taxonomy_object_array(
            data, path, id_field
        )

    string_arrays: dict[str, tuple[list[str], set[str]]] = {}
    for path in (
        "error_categories",
        "quality_vector_dimensions",
        "risk_flags",
    ):
        string_arrays[path] = _validate_taxonomy_string_array(data, path)

    profile_ids = object_arrays["profiles"][1]
    missing_profiles = _REQUIRED_TAXONOMY_PROFILES - profile_ids
    if missing_profiles:
        _quality_taxonomy_error(
            "profiles",
            "must include required ids: " + ", ".join(sorted(missing_profiles)),
        )

    for path, expected_ids in _EXACT_TAXONOMY_IDS.items():
        actual_ids = object_arrays[path][1]
        if actual_ids != expected_ids:
            _quality_taxonomy_error(
                path,
                "must contain exactly these ids: "
                + ", ".join(sorted(expected_ids)),
            )

    category_ids = string_arrays["error_categories"][1]
    severity_ids = object_arrays["severities"][1]
    for index, error_code in enumerate(object_arrays["error_codes"][0]):
        category = error_code.get("category")
        if not isinstance(category, str) or category not in category_ids:
            _quality_taxonomy_error(
                f"error_codes[{index}].category",
                "must reference a declared error category",
            )
        default_severity = error_code.get("default_severity")
        if (
            not isinstance(default_severity, str)
            or default_severity not in severity_ids
        ):
            _quality_taxonomy_error(
                f"error_codes[{index}].default_severity",
                "must reference a declared severity",
            )

    _validate_taxonomy_profile_map(data, "source_tag_profiles", profile_ids)
    _validate_taxonomy_profile_map(data, "term_category_profiles", profile_ids)

    section_rules = data.get("section_pattern_profiles")
    if not isinstance(section_rules, list):
        _quality_taxonomy_error(
            "section_pattern_profiles", "must be an array"
        )
    for index, rule in enumerate(section_rules):
        rule_path = f"section_pattern_profiles[{index}]"
        if not isinstance(rule, dict):
            _quality_taxonomy_error(rule_path, "must be an object")
        pattern = rule.get("pattern")
        if not isinstance(pattern, str) or not pattern:
            _quality_taxonomy_error(
                f"{rule_path}.pattern", "must be a non-empty string"
            )
        profile = rule.get("profile")
        if not isinstance(profile, str) or profile not in profile_ids:
            _quality_taxonomy_error(
                f"{rule_path}.profile", "must reference a declared profile"
            )
        confidence = rule.get("confidence")
        if (
            not isinstance(confidence, str)
            or confidence not in _PROFILE_CONFIDENCE_ORDER
        ):
            _quality_taxonomy_error(
                f"{rule_path}.confidence",
                "must be one of: low, medium, high",
            )

    _validate_taxonomy_length_bins(data)

    for path in ("profile_classifier_version", "risk_rule_version"):
        version = data.get(path)
        if not isinstance(version, str) or not version:
            _quality_taxonomy_error(path, "must be a non-empty string")

    error_code_ids = object_arrays["error_codes"][1]
    mergeable_codes = data.get("mergeable_codes")
    if not isinstance(mergeable_codes, list):
        _quality_taxonomy_error("mergeable_codes", "must be an array")
    seen_pairs: dict[tuple[str, str], int] = {}
    for index, pair in enumerate(mergeable_codes):
        pair_path = f"mergeable_codes[{index}]"
        if not isinstance(pair, list) or len(pair) != 2:
            _quality_taxonomy_error(
                pair_path, "must be an array of exactly two error codes"
            )
        for code_index, code in enumerate(pair):
            code_path = f"{pair_path}[{code_index}]"
            if not isinstance(code, str) or not code:
                _quality_taxonomy_error(
                    code_path, "must be a non-empty string"
                )
            if code not in error_code_ids:
                _quality_taxonomy_error(
                    code_path, "must reference a declared error code"
                )
        if pair[0] == pair[1]:
            _quality_taxonomy_error(
                f"{pair_path}[1]", f"must differ from {pair_path}[0]"
            )
        unordered_pair = tuple(sorted((pair[0], pair[1])))
        if unordered_pair in seen_pairs:
            _quality_taxonomy_error(
                pair_path,
                f"must be unique as an unordered pair (duplicates quality "
                f"taxonomy.mergeable_codes[{seen_pairs[unordered_pair]}])",
            )
        seen_pairs[unordered_pair] = index


def load_taxonomy(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / QUALITY_ROOT / TAXONOMY_FILE
    try:
        data = _read_json(path, "quality taxonomy")
    except ValidationError as error:
        raise ConfigurationError(
            f"quality taxonomy.root could not be loaded: {error}"
        ) from error
    if data.get("contract") != "tome4-quality-taxonomy-v1":
        _quality_taxonomy_error(
            "contract",
            "has unsupported quality taxonomy contract; must be "
            "'tome4-quality-taxonomy-v1'",
        )
    if (
        type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        _quality_taxonomy_error(
            "schema_version",
            "has unsupported quality taxonomy schema; must be exact integer 1",
        )
    _validate_quality_taxonomy(data)
    return data


def _quality_policy_error(path: str, requirement: str) -> None:
    raise ConfigurationError(f"quality policy.{path} {requirement}")


def _validate_quality_constraints(value: Any, path: str) -> None:
    if not isinstance(value, list):
        _quality_policy_error(path, "must be an array")

    constraint_ids: dict[str, int] = {}
    for index, constraint in enumerate(value):
        constraint_path = f"{path}[{index}]"
        if not isinstance(constraint, dict):
            _quality_policy_error(constraint_path, "must be an object")

        constraint_id = constraint.get("id")
        if not isinstance(constraint_id, str) or not constraint_id:
            _quality_policy_error(
                f"{constraint_path}.id", "must be a non-empty string"
            )
        if constraint_id in constraint_ids:
            first_index = constraint_ids[constraint_id]
            _quality_policy_error(
                f"{constraint_path}.id",
                f"must be unique (duplicates {path}[{first_index}].id)",
            )
        constraint_ids[constraint_id] = index

        mode = constraint.get("mode")
        if not isinstance(mode, str) or mode not in {"each", "any"}:
            _quality_policy_error(
                f"{constraint_path}.mode", "must be 'each' or 'any'"
            )

        feature = constraint.get("feature")
        if not isinstance(feature, str) or feature not in _CONSTRAINT_FEATURES:
            allowed = ", ".join(sorted(_CONSTRAINT_FEATURES))
            _quality_policy_error(
                f"{constraint_path}.feature", f"must be one of: {allowed}"
            )

        minimum = constraint.get("min")
        if type(minimum) is not int or minimum < 0:
            _quality_policy_error(
                f"{constraint_path}.min", "must be an exact integer >= 0"
            )

        values = constraint.get("values")
        if not isinstance(values, list) or not values:
            _quality_policy_error(
                f"{constraint_path}.values", "must be a non-empty array"
            )
        seen_values: dict[Any, int] = {}
        for value_index, item in enumerate(values):
            item_path = f"{constraint_path}.values[{value_index}]"
            try:
                hash(item)
            except TypeError:
                _quality_policy_error(item_path, "must be hashable")
            if feature in _CONSTRAINT_STRING_FEATURES:
                if not isinstance(item, str):
                    _quality_policy_error(item_path, "must be a string")
            elif type(item) is not bool:
                _quality_policy_error(item_path, "must be an exact boolean")
            if item in seen_values:
                first_index = seen_values[item]
                _quality_policy_error(
                    item_path,
                    f"must be unique (duplicates "
                    f"{constraint_path}.values[{first_index}])",
                )
            seen_values[item] = value_index

        if "description" in constraint and not isinstance(
            constraint["description"], str
        ):
            _quality_policy_error(
                f"{constraint_path}.description", "must be a string"
            )


def _validate_quality_policy(data: dict[str, Any]) -> None:
    strict_unknown_fields = data.get("strict_unknown_fields")
    if type(strict_unknown_fields) is not bool:
        _quality_policy_error(
            "strict_unknown_fields", "must be an exact boolean"
        )

    pilot = data.get("pilot")
    if not isinstance(pilot, dict):
        _quality_policy_error("pilot", "must be an object")

    pilot_seed = pilot.get("seed")
    if not isinstance(pilot_seed, str) or not pilot_seed:
        _quality_policy_error("pilot.seed", "must be a non-empty string")

    pilot_size = pilot.get("size")
    if type(pilot_size) is not int or pilot_size < 1:
        _quality_policy_error(
            "pilot.size", "must be an exact integer >= 1"
        )

    buckets = pilot.get("buckets")
    if not isinstance(buckets, dict):
        _quality_policy_error("pilot.buckets", "must be an object")
    for bucket in _PILOT_BUCKETS:
        if bucket not in buckets:
            _quality_policy_error(f"pilot.buckets.{bucket}", "is required")
    extra_buckets = sorted(set(buckets) - set(_PILOT_BUCKETS))
    if extra_buckets:
        _quality_policy_error(
            f"pilot.buckets[{extra_buckets[0]!r}]", "is not allowed"
        )
    for bucket in _PILOT_BUCKETS:
        target = buckets[bucket]
        if type(target) is not int or target < 1:
            _quality_policy_error(
                f"pilot.buckets.{bucket}",
                "must be an exact integer >= 1",
            )
    if sum(buckets.values()) != pilot_size:
        _quality_policy_error(
            "pilot.buckets", "sum must equal quality policy.pilot.size"
        )

    evaluator_ids = pilot.get("evaluator_ids")
    if not isinstance(evaluator_ids, list) or len(evaluator_ids) != 2:
        _quality_policy_error(
            "pilot.evaluator_ids", "must be an array of exactly two strings"
        )
    for index, evaluator_id in enumerate(evaluator_ids):
        if not isinstance(evaluator_id, str) or not evaluator_id:
            _quality_policy_error(
                f"pilot.evaluator_ids[{index}]", "must be a non-empty string"
            )
    if evaluator_ids[0] == evaluator_ids[1]:
        _quality_policy_error(
            "pilot.evaluator_ids[1]",
            "must differ from quality policy.pilot.evaluator_ids[0]",
        )

    method_version = pilot.get("method_version")
    if not isinstance(method_version, str) or not method_version:
        _quality_policy_error(
            "pilot.method_version", "must be a non-empty string"
        )

    dry_run = data.get("dry_run")
    if not isinstance(dry_run, dict):
        _quality_policy_error("dry_run", "must be an object")

    dry_run_seed = dry_run.get("seed")
    if not isinstance(dry_run_seed, str) or not dry_run_seed:
        _quality_policy_error("dry_run.seed", "must be a non-empty string")

    dry_run_size = dry_run.get("size")
    if type(dry_run_size) is not int or dry_run_size < 1:
        _quality_policy_error(
            "dry_run.size", "must be an exact integer >= 1"
        )

    if dry_run.get("contract") != DRY_RUN_CONTRACT:
        _quality_policy_error(
            "dry_run.contract", f"must be {DRY_RUN_CONTRACT!r}"
        )
    _validate_quality_constraints(
        dry_run.get("coverage_constraints"), "dry_run.coverage_constraints"
    )
    _validate_quality_constraints(
        data.get("coverage_constraints"), "coverage_constraints"
    )

    risk_flags = data.get("risk_enrichment_flags")
    if not isinstance(risk_flags, list):
        _quality_policy_error("risk_enrichment_flags", "must be an array")
    seen_flags: dict[str, int] = {}
    for index, flag in enumerate(risk_flags):
        flag_path = f"risk_enrichment_flags[{index}]"
        if not isinstance(flag, str) or not flag:
            _quality_policy_error(flag_path, "must be a non-empty string")
        if flag in seen_flags:
            _quality_policy_error(
                flag_path,
                f"must be unique (duplicates "
                f"quality policy.risk_enrichment_flags[{seen_flags[flag]}])",
            )
        seen_flags[flag] = index

    component_groups = data.get("component_groups")
    if not isinstance(component_groups, dict):
        _quality_policy_error("component_groups", "must be an object")
    for group in component_groups:
        if not isinstance(group, str) or not group:
            _quality_policy_error(
                f"component_groups[{group!r}]", "key must be a non-empty string"
            )
    component_paths: dict[str, str] = {}
    for group in sorted(component_groups):
        group_path = f"component_groups[{group!r}]"
        members = component_groups[group]
        if not isinstance(members, list):
            _quality_policy_error(group_path, "must be an array")
        group_members: dict[str, int] = {}
        for index, component in enumerate(members):
            component_path = f"{group_path}[{index}]"
            if not isinstance(component, str) or not component:
                _quality_policy_error(
                    component_path, "must be a non-empty string"
                )
            if component in group_members:
                _quality_policy_error(
                    component_path,
                    f"must be unique (duplicates "
                    f"{group_path}[{group_members[component]}])",
                )
            group_members[component] = index
            if component in component_paths:
                _quality_policy_error(
                    component_path,
                    f"must not also appear in {component_paths[component]}",
                )
            component_paths[component] = component_path

    context_neighbor_limit = data.get("context_neighbor_limit")
    if type(context_neighbor_limit) is not int or context_neighbor_limit < 0:
        _quality_policy_error(
            "context_neighbor_limit", "must be an exact integer >= 0"
        )

    contrast_group_max_size = data.get("contrast_group_max_size")
    if type(contrast_group_max_size) is not int or contrast_group_max_size < 2:
        _quality_policy_error(
            "contrast_group_max_size", "must be an exact integer >= 2"
        )


def load_quality_policy(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / QUALITY_ROOT / POLICY_FILE
    try:
        data = _read_json(path, "quality policy")
    except ValidationError as error:
        raise ConfigurationError(str(error)) from error
    if data.get("contract") != "tome4-quality-policy-v1":
        raise ConfigurationError(
            "unsupported quality policy contract at quality policy.contract: "
            f"{path}"
        )
    if (
        type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        raise ConfigurationError(
            "unsupported quality policy schema at quality policy.schema_version: "
            f"{path}"
        )
    _validate_quality_policy(data)
    return data


def terminology_store_sha256(path: Path) -> str:
    """Content digest for the terminology store (file or domain directory)."""
    from .terminology import terminology_store_sha256 as _impl

    return _impl(path)


def _load_terminology(path: Path) -> tuple[list[dict[str, str]], str]:
    from .terminology import load_terminology_rows, terminology_store_sha256

    return load_terminology_rows(path), terminology_store_sha256(path)


def create_quality_run_directory(root: Path, kind: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run_directory = (
        root / ".artifacts" / "i18n" / "quality" / "runs" / f"{timestamp}-{kind}"
    )
    run_directory.mkdir(parents=True, exist_ok=False)
    return run_directory


def _write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    data = "".join(
        json.dumps(
            record, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        + "\n"
        for record in records
    ).encode("utf-8")
    atomic_write_bytes(path, data)


# ---------------------------------------------------------------------------
# Identity and structure
# ---------------------------------------------------------------------------


def _load_editorial_to_tu(manifest: Manifest) -> dict[tuple[str, str], tuple[str, ...]]:
    """Load the current Pilot A identity indexes into an editorial->TU map.

    Reads `.artifacts/i18n/identity/current/<component>/` for every component
    that has a complete index trio (entities.jsonl + tu_index.jsonl +
    identity.json) and fails closed on a partial/corrupt trio (same scan
    semantics as the extract path).  Components without an index directory
    simply have no mapping (editorials fall back to the fallback-editorial
    TU scheme).
    """
    from .extract import _read_current_indexes

    current_root = manifest.root / _IDENTITY_CURRENT_ROOT
    if not current_root.is_dir():
        return {}
    mapping: dict[tuple[str, str], tuple[str, ...]] = {}
    for index in _read_current_indexes(current_root):
        for editorial_id, tu_uids in index.editorial_to_tu.items():
            mapping[(index.component, editorial_id)] = tuple(sorted(tu_uids))
    return mapping


def _identity_indexes_sha256(manifest: Manifest) -> str:
    """Deterministic digest of the current Pilot A identity indexes.

    Binds the editorial->TU mapping used to build an inventory/sample into
    the artifact identity so a stale or extended index cannot silently keep
    old artifacts current (infra-contract-007 review F6).  Components without
    an index directory contribute nothing; the empty state has a stable
    digest too.
    """
    editorial_to_tu = _load_editorial_to_tu(manifest)
    return _canonical_sha256(
        {
            "{}\0{}".format(component, editorial_id): tu_uids
            for (component, editorial_id), tu_uids in sorted(
                editorial_to_tu.items()
            )
        }
    )


def compute_unit_id(
    component: str, section: str, source: str, source_tag: str | None
) -> str:
    """Editorial identity (evidence only, Pilot A §4.5 Editorial ID).

    Kept as the editorial evidence field on inventory entries.  The quality
    identity axis is Pilot A `tu_uid`/`revision_uid` (infra-contract-007);
    `unit_id` no longer participates in revision identity.
    """
    return stable_entry_id(component, section, source, source_tag)


def compute_tu_uid(
    component: str, section: str, source: str, source_tag: str | None,
    *, editorial_to_tu: dict[tuple[str, str], tuple[str, ...]] | None = None,
) -> str:
    """Pilot A TU identity for one editorial occurrence.

    Resolves the editorial id through the identity index mapping; when the
    editorial is unmapped (or no index is available) it falls back to the
    domain-separated `tu/fallback-editorial` scheme, matching
    `build_finding_records::_bind` (findings.py).  One-to-many editorials are
    split per TU by the caller using :func:`editorial_tu_uids`.
    """
    uids = editorial_tu_uids(
        component, section, source, source_tag,
        editorial_to_tu=editorial_to_tu,
    )
    return uids[0]


def editorial_tu_uids(
    component: str, section: str, source: str, source_tag: str | None,
    *, editorial_to_tu: dict[tuple[str, str], tuple[str, ...]] | None = None,
) -> tuple[str, ...]:
    """Full TU UID set for one editorial occurrence (sorted, Pilot A).

    One editorial can legitimately back several structurally distinct strong
    TUs (contract §4.7); quality entries are then split one entry per TU.
    Unmapped editorials fall back to the single `tu/fallback-editorial` UID.
    """
    editorial_id = stable_entry_id(component, section, source, source_tag)
    if editorial_to_tu is not None:
        found = editorial_to_tu.get((component, editorial_id))
        if found:
            return tuple(sorted(found))
    return (tu_uid_fallback(editorial_id),)


def compute_revision_uid(tu_uid: str, source: str) -> str:
    """Pilot A source Revision UID (identity.py `revision_uid`)."""
    return revision_uid(tu_uid, source_sha256(source))


def compute_revision_id(
    version: str,
    unit_id: str,
    target: str,
    args_order: Any,
    special: Any,
    *,
    tu_uid: str | None = None,
    revision_uid_value: str | None = None,
    source: str | None = None,
) -> str:
    """Quality revision identity (infra-contract-007, Pilot A bridge).

    The revision binds the Pilot A unit and source revision plus the exact
    translation payload: source change -> revision_uid changes -> revision
    changes; target/args_order/special/version change -> revision changes;
    file moves and source-tag spelling changes that keep the same strong TU
    leave both tu_uid and revision_uid (and therefore this revision) stable.

    ``unit_id`` is the editorial id, kept for backward compatibility with
    callers that only carry the editorial id.  Pilot A fields are
    authoritative when provided: ``tu_uid`` defaults to the fallback TU of
    the editorial id, and ``revision_uid_value`` defaults to the Pilot A
    source revision of ``tu_uid`` against ``source`` when a source is
    available.  When neither Pilot A revision uid nor source is available
    (legacy callers) the revision uid degrades to a stable zero-source
    revision so the editorial-only call path remains deterministic.
    """
    resolved_tu_uid = tu_uid if tu_uid is not None else tu_uid_fallback(unit_id)
    if revision_uid_value is not None:
        resolved_revision_uid = revision_uid_value
    elif source is not None:
        resolved_revision_uid = revision_uid(resolved_tu_uid, source_sha256(source))
    else:
        resolved_revision_uid = revision_uid(resolved_tu_uid, source_sha256(""))
    payload = {
        "identity_contract": IDENTITY_CONTRACT,
        "version": version,
        "tu_uid": resolved_tu_uid,
        "revision_uid": resolved_revision_uid,
        "target": target,
        "args_order": args_order,
        "special": special,
    }
    return _canonical_sha256(payload)


def _multiset(tokens: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(tokens).items()))


def structure_signature(
    source: str, target: str, args_order: Any
) -> dict[str, Any]:
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    valid_order = (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and len(args_order) == len(source_tokens)
        and all(1 <= index <= len(source_tokens) for index in args_order)
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    )
    if valid_order:
        role_order = [source_tokens[index - 1].conversion for index in args_order]
    elif args_order is None:
        role_order = [token.conversion for token in source_tokens]
    else:
        role_order = None
    return {
        "printf": {
            "source_raw": [token.raw for token in source_tokens],
            "source_conversions": [token.conversion for token in source_tokens],
            "target_raw": [token.raw for token in target_tokens],
            "target_conversions": [token.conversion for token in target_tokens],
            "args_order": args_order,
            "role_order": role_order,
        },
        "markup": {
            "source": _multiset(MARKUP_RE.findall(source)),
            "target": _multiset(MARKUP_RE.findall(target)),
        },
        "at_tokens": {
            "source": _multiset(AT_TOKEN_RE.findall(source)),
            "target": _multiset(AT_TOKEN_RE.findall(target)),
        },
        "newlines": {"source": source.count("\n"), "target": target.count("\n")},
        "multiline": "\n" in source or "\n" in target,
    }


def _format_shape_matches(
    source: str, target: str, args_order: Any
) -> bool | None:
    """Raw-token comparison including width/precision (lint warning level)."""
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    if args_order is None:
        expected = [token.raw for token in source_tokens]
    elif (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and len(args_order) == len(source_tokens)
        and all(1 <= index <= len(source_tokens) for index in args_order)
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    ):
        expected = [source_tokens[index - 1].raw for index in args_order]
    else:
        return None
    return expected == [token.raw for token in target_tokens]


def _format_signature_matches(
    source: str, target: str, args_order: Any
) -> bool | None:
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    if args_order is None:
        expected = [token.conversion for token in source_tokens]
    elif (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and len(args_order) == len(source_tokens)
        and all(1 <= index <= len(source_tokens) for index in args_order)
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    ):
        expected = [source_tokens[index - 1].conversion for index in args_order]
    else:
        return None
    return expected == [token.conversion for token in target_tokens]


# ---------------------------------------------------------------------------
# Terminology index and relevant terms
# ---------------------------------------------------------------------------


def _contains_term_at_ascii_boundaries(container: str, term: str) -> bool:
    """Return whether *term* occurs with the terminology match boundaries."""
    start = container.find(term)
    while start >= 0:
        end = start + len(term)
        left_boundary = start == 0 or not (
            "a" <= container[start - 1] <= "z"
            or "0" <= container[start - 1] <= "9"
            or container[start - 1] == "_"
        )
        right_boundary = end == len(container) or not (
            "a" <= container[end] <= "z"
            or "0" <= container[end] <= "9"
            or container[end] == "_"
        )
        if left_boundary and right_boundary:
            return True
        start = container.find(term, start + 1)
    return False


def _build_term_index(
    rows: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    re.Pattern[str] | None,
    dict[str, list[int]],
    dict[str, list[str]],
]:
    records: list[dict[str, Any]] = []
    for row in rows:
        source = (row.get("source") or "").strip()
        plain = _plain_source(source).strip()
        if not plain:
            continue
        records.append(
            {
                "source": source,
                "target": row.get("target") or "",
                "category": row.get("category") or "",
                "domain": row.get("domain") or "",
                "source_tag": row.get("source_tag") or "",
                "status": row.get("status") or "",
                "scope": row.get("scope") or "",
                "notes": row.get("notes") or "",
                "plain": plain,
            }
        )
    records.sort(
        key=lambda record: (
            record["plain"],
            0 if record["status"] == "preferred" else 1,
            record["source_tag"],
            record["scope"],
        )
    )
    by_plain: dict[str, list[int]] = defaultdict(list)
    for index, record in enumerate(records):
        by_plain[record["plain"]].append(index)
    matcher = None
    nested_terms: dict[str, list[str]] = {}
    if by_plain:
        # Longest-first alternation: Python regex alternation tries
        # alternatives left-to-right, so a shorter prefix term ('fire')
        # must never shadow a longer overlapping term ('fire damage').
        unique_plains = sorted(
            by_plain, key=lambda plain: (-len(plain), plain)
        )
        matcher = re.compile(
            r"(?<![a-z0-9_])("
            + "|".join(re.escape(plain) for plain in unique_plains)
            + r")(?![a-z0-9_])"
        )
        # The longest-first matcher consumes nested terms. Precompute every
        # shorter unique term contained at the same ASCII boundaries so
        # suffix and middle matches are retained alongside prefix matches.
        for index, container in enumerate(unique_plains):
            contained = [
                term
                for term in unique_plains[index + 1 :]
                if len(term) < len(container)
                and _contains_term_at_ascii_boundaries(container, term)
            ]
            if contained:
                nested_terms[container] = contained
    return records, matcher, by_plain, nested_terms


def _relevant_terms_for(
    source: str,
    source_tag: str | None,
    component: str,
    term_records: list[dict[str, Any]],
    matcher: re.Pattern[str] | None,
    by_plain: dict[str, list[int]],
    nested_terms: dict[str, list[str]] | None = None,
) -> list[dict[str, Any]]:
    plain = _plain_source(source).strip()
    if not plain or matcher is None:
        return []
    matched_indices: set[int] = set()
    for match in matcher.finditer(plain):
        matched = match.group(1)
        matched_indices.update(by_plain.get(matched, ()))
        for nested in (nested_terms or {}).get(matched, ()):
            matched_indices.update(by_plain.get(nested, ()))
    relevant: list[dict[str, Any]] = []
    for index in matched_indices:
        record = term_records[index]
        if not _scope_matches(record["scope"], component):
            continue
        if not _source_tag_matches(record["source_tag"], source_tag):
            continue
        relevant.append(
            {
                "source": record["source"],
                "target": record["target"],
                "category": record["category"],
                "domain": record["domain"],
                "source_tag": record["source_tag"],
                "status": record["status"],
                "scope": record["scope"],
                "notes": record["notes"],
                "match": "full" if record["plain"] == plain else "partial",
            }
        )
    relevant.sort(
        key=lambda row: (
            row["source"].casefold(),
            0 if row["status"] == "preferred" else 1,
            row["source_tag"],
            row["scope"],
        )
    )
    return relevant


# ---------------------------------------------------------------------------
# Profile classification, risk flags and gate signals
# ---------------------------------------------------------------------------


def _section_matches(pattern: str, section: str) -> bool:
    """Segment-aware section pattern match.

    `pattern in section` substrings can misfire ("ui" matches
    "data/guilds/..."); requiring a contiguous path-segment sequence keeps
    patterns precise while still matching any depth.
    """
    pattern_segments = [segment for segment in pattern.split("/") if segment]
    if not pattern_segments:
        return False
    section_segments = section.split("/")
    width = len(pattern_segments)
    return any(
        section_segments[index : index + width] == pattern_segments
        for index in range(len(section_segments) - width + 1)
    )


def classify_profile(
    source: str,
    source_tag: str | None,
    section: str,
    relevant_terms: list[dict[str, Any]],
    taxonomy: dict[str, Any],
) -> tuple[str, str]:
    """Profile classification with priority: source_tag, term full match,
    section pattern, then structure fallback. Conflicting high-priority rules
    lower the confidence instead of silently overriding."""
    votes: list[tuple[str, str]] = []
    if source_tag and source_tag in taxonomy.get("source_tag_profiles", {}):
        votes.append((taxonomy["source_tag_profiles"][source_tag], "high"))
    plain = _plain_source(source).strip()
    for term in relevant_terms:
        if _plain_source(term["source"]).strip() == plain:
            category = term.get("category", "")
            if category in taxonomy.get("term_category_profiles", {}):
                votes.append((taxonomy["term_category_profiles"][category], "high"))
            break
    for rule in taxonomy.get("section_pattern_profiles", []):
        if _section_matches(rule["pattern"], section):
            votes.append((rule["profile"], rule["confidence"]))
    if votes:
        profiles = {profile for profile, _ in votes}
        if len(profiles) == 1:
            confidence = max(
                (confidence for _, confidence in votes),
                key=_PROFILE_CONFIDENCE_ORDER.index,
            )
            return profiles.pop(), confidence
        return votes[0][0], "low"
    if (
        not extract_format_tokens(source)
        and len(source) <= 30
        and not SENTENCE_PUNCT_RE.search(source)
        and not MARKUP_RE.search(source)
        and not AT_TOKEN_RE.search(source)
    ):
        return "ui", "low"
    if len(source) >= LONG_SOURCE_LENGTH:
        return "narrative", "low"
    if extract_format_tokens(source) and not SENTENCE_PUNCT_RE.search(source):
        return "mechanics", "low"
    return "unknown", "low"


def _length_bin(length: int, taxonomy: dict[str, Any]) -> str:
    for bin_spec in taxonomy.get("length_bins", []):
        maximum = bin_spec.get("max")
        if maximum is None or length <= maximum:
            return bin_spec["id"]
    return "very-long"


def compute_risk_flags(
    source: str,
    target: str,
    structure: dict[str, Any],
    profile_confidence: str,
    relevant_terms: list[dict[str, Any]],
    runtime_stat: dict[str, Any],
    taxonomy: dict[str, Any],
) -> list[str]:
    whitelist = set(taxonomy.get("risk_flags", []))
    flags: list[str] = []

    def add(flag: str) -> None:
        if flag in whitelist:
            flags.append(flag)

    printf = structure["printf"]
    if printf["source_raw"]:
        add("has-printf")
    if printf["args_order"] is not None:
        add("has-args-order")
    if structure["markup"]["source"]:
        add("has-markup")
    if structure["at_tokens"]["source"]:
        add("has-at-token")
    if structure["multiline"]:
        add("multiline")
    plain = source.strip()
    if len(plain) <= 8 and " " not in plain and runtime_stat["section_count"] > 1:
        add("short-ambiguous-source")
    if len(source) >= LONG_SOURCE_LENGTH:
        add("long-source")
    if profile_confidence != "high":
        add("profile-uncertain")
    if any(term["status"] == "preferred" for term in relevant_terms):
        add("preferred-term-present")
    if any(term["status"] != "preferred" for term in relevant_terms):
        add("term-variant-or-review")
    if runtime_stat["occurrence_count"] > 1:
        add("repeated-runtime-key")
    stripped = printf["source_raw"]
    source_without_printf = source
    for raw in sorted(stripped, key=len, reverse=True):
        source_without_printf = source_without_printf.replace(raw, " ")
    if DIGIT_RE.search(source_without_printf) or UNIT_WORD_RE.search(source):
        add("source-has-number-or-unit")
    if NEGATION_RE.search(source) or CONDITION_RE.search(source):
        add("source-has-negation-or-condition")
    if len(source) >= 10 and target:
        ratio = len(target) / len(source)
        if ratio > LENGTH_OUTLIER_MAX_RATIO or ratio < LENGTH_OUTLIER_MIN_RATIO:
            add("source-target-length-outlier")
    stripped_target = MARKUP_RE.sub(" ", target)
    stripped_target = AT_TOKEN_RE.sub(" ", stripped_target)
    if len(ASCII_WORD_RE.findall(stripped_target)) >= 3:
        add("possible-untranslated-residue")
    return flags


def compute_gate_signals(
    source: str,
    target: str,
    source_tag: str | None,
    args_order: Any,
    structure: dict[str, Any],
    runtime_stat: dict[str, Any],
    cross_component_variant: bool,
) -> dict[str, Any]:
    format_applicable = source_tag in FORMAT_TAGS or args_order is not None
    return {
        "lua_load_valid": True,
        "empty_target": target == "",
        "format_signature_match": (
            _format_signature_matches(source, target, args_order)
            if format_applicable
            else None
        ),
        "format_shape_match": (
            _format_shape_matches(source, target, args_order)
            if format_applicable
            else None
        ),
        "markup_multiset_match": (
            structure["markup"]["source"] == structure["markup"]["target"]
        ),
        "at_token_multiset_match": (
            structure["at_tokens"]["source"] == structure["at_tokens"]["target"]
        ),
        "runtime_collision": runtime_stat["semantic_value_count"] > 1,
        "cross_component_variant": cross_component_variant,
        "needs_review": ["QG_CURRENT", "QG_SEVERE", "QG_CONTEXT", "QG_TERMS"],
    }


# ---------------------------------------------------------------------------
# M2: inventory
# ---------------------------------------------------------------------------


def build_inventory(
    manifest: Manifest, loader: LocaleLoader
) -> dict[str, Any]:
    qpolicy = load_quality_policy(manifest)
    taxonomy = load_taxonomy(manifest)
    terminology_rows, terminology_sha256 = _load_terminology(
        manifest.root / manifest.terminology
    )
    term_records, term_matcher, term_by_plain, term_nested = _build_term_index(
        terminology_rows
    )

    raw_entries: list[dict[str, Any]] = []
    runtime_stats: dict[
        tuple[str, str, str | None], dict[str, Any]
    ] = defaultdict(
        lambda: {
            "occurrence_count": 0,
            "section_count": 0,
            "target_count": 0,
            "semantic_value_count": 0,
            "sections": set(),
            "targets": set(),
            "semantic_values": set(),
        }
    )
    global_semantic_values: dict[
        tuple[str, str | None], dict[str, set[str]]
    ] = defaultdict(lambda: defaultdict(set))
    translation_inputs: list[dict[str, str]] = []
    for component_id, role, logical_path in _translation_input_locations(manifest):
        document = loader.load_path(
            manifest.root / logical_path, logical_path=logical_path
        )
        translation_inputs.append(
            _translation_input_record(
                component_id,
                role,
                logical_path,
                document.sha256,
            )
        )
        for ordinal, record in enumerate(document.translations):
            source = record.get("source")
            target = record.get("target")
            section = record.get("section")
            if not all(isinstance(value, str) for value in (source, target, section)):
                raise ValidationError(
                    f"invalid canonical translation entry in component "
                    f"{component_id}: {logical_path}"
                )
            source_tag = record.get("source_tag")
            semantic_signature = runtime_semantic_signature(
                record,
                label=(
                    f"translation {logical_path}:"
                    f"{record.get('line', '?')}"
                ),
            )
            raw_entries.append(
                {
                    "component": component_id,
                    "section": section,
                    "source": source,
                    "target": target,
                    "source_tag": source_tag,
                    "args_order": record.get("args_order"),
                    "special": record.get("special"),
                    "runtime_semantic_signature": semantic_signature,
                    "logical_path": logical_path,
                    "line": record.get("line"),
                    "ordinal": ordinal,
                }
            )
            stat = runtime_stats[(component_id, source, source_tag)]
            stat["occurrence_count"] += 1
            stat["sections"].add(section)
            stat["targets"].add(target)
            stat["semantic_values"].add(semantic_signature)
            stat["section_count"] = len(stat["sections"])
            stat["target_count"] = len(stat["targets"])
            stat["semantic_value_count"] = len(stat["semantic_values"])
            global_semantic_values[(source, source_tag)][component_id].add(
                semantic_signature
            )

    editorial_to_tu = _load_editorial_to_tu(manifest)

    revisions: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in raw_entries:
        unit_id = compute_unit_id(
            entry["component"], entry["section"], entry["source"], entry["source_tag"]
        )
        tu_uids = editorial_tu_uids(
            entry["component"],
            entry["section"],
            entry["source"],
            entry["source_tag"],
            editorial_to_tu=editorial_to_tu,
        )
        for tu_uid in tu_uids:
            revision_uid_value = compute_revision_uid(tu_uid, entry["source"])
            revision_id = compute_revision_id(
                manifest.version,
                unit_id,
                entry["target"],
                entry["args_order"],
                entry["special"],
                tu_uid=tu_uid,
                revision_uid_value=revision_uid_value,
                source=entry["source"],
            )
            key = (entry["component"], tu_uid, revision_id)
            revision = revisions.get(key)
            if revision is None:
                revision = {
                    "unit_id": unit_id,
                    "tu_uid": tu_uid,
                    "revision_uid": revision_uid_value,
                    "revision_id": revision_id,
                    "version": manifest.version,
                    "component": entry["component"],
                    "section": entry["section"],
                    "source": entry["source"],
                    "target": entry["target"],
                    "source_tag": entry["source_tag"],
                    "args_order": entry["args_order"],
                    "special": entry["special"],
                    "occurrences": [],
                }
                revisions[key] = revision
            revision["occurrences"].append(
                {
                    "logical_path": entry["logical_path"],
                    "section": entry["section"],
                    "line": entry["line"],
                    "ordinal": entry["ordinal"],
                }
            )

    cross_component_variants: dict[tuple[str, str | None], bool] = {}
    for (source, source_tag), by_component in global_semantic_values.items():
        union: set[str] = set()
        for semantic_values in by_component.values():
            union.update(semantic_values)
        cross_component_variants[(source, source_tag)] = (
            len(by_component) > 1 and len(union) > 1
        )

    entries: list[dict[str, Any]] = []
    for (component, _tu_uid, revision_id), revision in sorted(revisions.items()):
        source = revision["source"]
        target = revision["target"]
        source_tag = revision["source_tag"]
        args_order = revision["args_order"]
        structure = structure_signature(source, target, args_order)
        relevant_terms = _relevant_terms_for(
            source,
            source_tag,
            component,
            term_records,
            term_matcher,
            term_by_plain,
            term_nested,
        )
        profile, profile_confidence = classify_profile(
            source, source_tag, revision["section"], relevant_terms, taxonomy
        )
        runtime_stat = runtime_stats[(component, source, source_tag)]
        revision["occurrences"].sort(
            key=lambda occurrence: (
                occurrence["logical_path"],
                occurrence["line"] if occurrence["line"] is not None else -1,
                occurrence["ordinal"],
            )
        )
        domains: list[str] = []
        for term in relevant_terms:
            domain = term.get("domain") or ""
            if domain and domain not in domains:
                domains.append(domain)
        entries.append(
            {
                **revision,
                "profile": profile,
                "profile_confidence": profile_confidence,
                "domain_hints": sorted(domains)[:MAX_DOMAIN_HINTS],
                "relevant_terms": relevant_terms,
                "structure": structure,
                "gate_signals": compute_gate_signals(
                    source,
                    target,
                    source_tag,
                    args_order,
                    structure,
                    runtime_stat,
                    cross_component_variants.get((source, source_tag), False),
                ),
                "risk_flags": compute_risk_flags(
                    source,
                    target,
                    structure,
                    profile_confidence,
                    relevant_terms,
                    runtime_stat,
                    taxonomy,
                ),
                "source_length_bin": _length_bin(len(source), taxonomy),
            }
        )

    inventory_sha256 = _canonical_sha256(entries)
    components: dict[str, dict[str, int]] = {}
    profiles: Counter[str] = Counter()
    length_bins: Counter[str] = Counter()
    risk_flags: Counter[str] = Counter()
    # Occurrence conservation (infra-contract-007 review F3): a one-to-many
    # editorial is split into one entry per TU and every TU entry carries the
    # same occurrence evidence, so summing per-entry occurrence lists would
    # double count corpus occurrences.  Count each raw occurrence exactly once
    # per component (same value as the top-level summary.occurrences).
    occurrence_counts: dict[str, int] = Counter()
    for entry in raw_entries:
        occurrence_counts[entry["component"]] += 1
    for entry in entries:
        component = entry["component"]
        bucket = components.setdefault(component, {"entries": 0, "occurrences": 0})
        bucket["entries"] += 1
        bucket["occurrences"] = occurrence_counts[component]
        profiles[entry["profile"]] += 1
        length_bins[entry["source_length_bin"]] += 1
        for flag in entry["risk_flags"]:
            risk_flags[flag] += 1

    summary = {
        "entries": len(entries),
        "occurrences": len(raw_entries),
        "components": components,
        "profiles": dict(sorted(profiles.items())),
        "length_bins": dict(sorted(length_bins.items())),
        "risk_flags": dict(sorted(risk_flags.items())),
        "unverified_gates": ["QG_CURRENT", "QG_SEVERE", "QG_CONTEXT", "QG_TERMS"],
    }
    return {
        "schema_version": 1,
        "quality_contract": INVENTORY_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "translation_inputs_sha256": _canonical_sha256(translation_inputs),
        "identity_indexes_sha256": _identity_indexes_sha256(manifest),
        "terminology_sha256": terminology_sha256,
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "inventory_sha256": inventory_sha256,
        "entries": len(entries),
        "components": components,
        "profile_classifier_version": taxonomy.get("profile_classifier_version"),
        "risk_rule_version": taxonomy.get("risk_rule_version"),
        "summary": summary,
        "entries_list": entries,
    }


def run_inventory(manifest: Manifest, loader: LocaleLoader) -> dict[str, Any]:
    report = build_inventory(manifest, loader)
    run_directory = create_quality_run_directory(manifest.root, "inventory")
    entries = report.pop("entries_list")
    _write_jsonl(run_directory / "inventory.jsonl", entries)
    write_json(run_directory / "inventory-summary.json", report["summary"])
    manifest_report = {key: value for key, value in report.items()}
    write_json(run_directory / "inventory-manifest.json", manifest_report)
    report["run_directory"] = os_path_relative(run_directory, manifest)
    report["inventory"] = os_path_relative(run_directory / "inventory.jsonl", manifest)
    report["summary_path"] = os_path_relative(
        run_directory / "inventory-summary.json", manifest
    )
    return report


def os_path_relative(path: Path, manifest: Manifest) -> str:
    return str(path.relative_to(manifest.root))


def _validate_inventory_record(entry: dict[str, Any], index: int) -> None:
    """Validate the complete record shape consumed by quality sampling."""
    label = f"quality inventory record {index}"

    def required(field: str) -> Any:
        if field not in entry:
            raise ValidationError(f"{label}.{field} is missing")
        return entry[field]

    if entry.get("quality_contract") not in (None, INVENTORY_CONTRACT):
        raise ValidationError(f"{label}.quality_contract has an unknown contract")

    for field in ("unit_id", "revision_id", "tu_uid", "revision_uid"):
        value = required(field)
        if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
            raise ValidationError(
                f"{label}.{field} must be a 64-character lowercase SHA-256 digest"
            )

    for field in ("version", "component", "source"):
        value = required(field)
        if not isinstance(value, str) or not value:
            raise ValidationError(f"{label}.{field} must be a non-empty string")

    for field in ("section", "target"):
        if not isinstance(required(field), str):
            raise ValidationError(f"{label}.{field} must be a string")

    source_tag = required("source_tag")
    if source_tag is not None and not isinstance(source_tag, str):
        raise ValidationError(f"{label}.source_tag must be a string or null")

    args_order = required("args_order")
    if args_order is not None:
        if not isinstance(args_order, list):
            raise ValidationError(f"{label}.args_order must be an array or null")
        for item_index, item in enumerate(args_order):
            if type(item) is not int:
                raise ValidationError(
                    f"{label}.args_order[{item_index}] must be an exact integer"
                )

    special = required("special")
    json_value_signature(special, label=f"{label}.special")

    occurrences = required("occurrences")
    if not isinstance(occurrences, list) or not occurrences:
        raise ValidationError(f"{label}.occurrences must be a non-empty array")
    for occurrence_index, occurrence in enumerate(occurrences):
        occurrence_label = f"{label}.occurrences[{occurrence_index}]"
        if not isinstance(occurrence, dict):
            raise ValidationError(f"{occurrence_label} must be an object")
        for field in ("logical_path", "section", "line", "ordinal"):
            if field not in occurrence:
                raise ValidationError(f"{occurrence_label}.{field} is missing")
        if not isinstance(occurrence["logical_path"], str):
            raise ValidationError(
                f"{occurrence_label}.logical_path must be a string"
            )
        if not isinstance(occurrence["section"], str):
            raise ValidationError(f"{occurrence_label}.section must be a string")
        if occurrence["line"] is not None and type(occurrence["line"]) is not int:
            raise ValidationError(
                f"{occurrence_label}.line must be an exact integer or null"
            )
        if type(occurrence["ordinal"]) is not int:
            raise ValidationError(
                f"{occurrence_label}.ordinal must be an exact integer"
            )

    profile = required("profile")
    if not isinstance(profile, str) or not profile:
        raise ValidationError(f"{label}.profile must be a non-empty string")

    profile_confidence = required("profile_confidence")
    if profile_confidence not in _PROFILE_CONFIDENCE_ORDER:
        raise ValidationError(
            f"{label}.profile_confidence must be low, medium, or high"
        )

    for field in ("domain_hints", "risk_flags"):
        values = required(field)
        if not isinstance(values, list):
            raise ValidationError(f"{label}.{field} must be an array")
        for item_index, item in enumerate(values):
            if not isinstance(item, str):
                raise ValidationError(
                    f"{label}.{field}[{item_index}] must be a string"
                )

    relevant_terms = required("relevant_terms")
    if not isinstance(relevant_terms, list):
        raise ValidationError(f"{label}.relevant_terms must be an array")
    for term_index, term in enumerate(relevant_terms):
        if not isinstance(term, dict):
            raise ValidationError(
                f"{label}.relevant_terms[{term_index}] must be an object"
            )

    for field in ("structure", "gate_signals"):
        if not isinstance(required(field), dict):
            raise ValidationError(f"{label}.{field} must be an object")

    source_length_bin = required("source_length_bin")
    if not isinstance(source_length_bin, str) or not source_length_bin:
        raise ValidationError(
            f"{label}.source_length_bin must be a non-empty string"
        )


def read_inventory_file(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    resolved = path.expanduser().resolve()
    entries = _read_json_lines(resolved, "quality inventory")
    if not entries:
        raise ValidationError(f"quality inventory is empty: {resolved}")
    for index, entry in enumerate(entries):
        _validate_inventory_record(entry, index)
    revision_ids = [entry["revision_id"] for entry in entries]
    if len(revision_ids) != len(set(revision_ids)):
        raise ValidationError("quality inventory contains duplicate revision_id")
    return entries, {
        "entries": len(entries),
        "inventory_sha256": _canonical_sha256(entries),
    }


def _inventory_manifest_error(field: str, requirement: str) -> None:
    raise ValidationError(
        f"quality inventory manifest.{field} {requirement}"
    )


def _read_inventory_manifest_preflight(
    manifest: Manifest,
    inventory_path: Path,
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
) -> dict[str, Any]:
    """Read and validate the cheap inventory companion before its JSONL."""
    try:
        companion_path = inventory_path.with_name("inventory-manifest.json")
        resolved = companion_path.expanduser().resolve()
        raw = resolved.read_bytes()
    except (OSError, RuntimeError, ValueError) as error:
        _inventory_manifest_error(
            "root", f"cannot be read: {inventory_path}: {error}"
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        _inventory_manifest_error(
            "root", f"must be UTF-8 encoded: {resolved}: {error}"
        )
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        _inventory_manifest_error(
            "root", f"must be valid JSON: {resolved}: {error}"
        )
    if not isinstance(data, dict):
        _inventory_manifest_error("root", f"must be an object: {resolved}")

    def required(field: str) -> Any:
        if field not in data:
            _inventory_manifest_error(field, "is missing")
        return data[field]

    quality_contract = required("quality_contract")
    if quality_contract != INVENTORY_CONTRACT:
        _inventory_manifest_error(
            "quality_contract", f"must equal {INVENTORY_CONTRACT!r}"
        )

    schema_version = required("schema_version")
    if type(schema_version) is not int or schema_version != 1:
        _inventory_manifest_error("schema_version", "must be exact integer 1")

    tool_version = required("tool_version")
    if tool_version != TOOL_VERSION:
        _inventory_manifest_error(
            "tool_version", "does not match the current tool version"
        )

    version = required("version")
    if not isinstance(version, str) or not version:
        _inventory_manifest_error("version", "must be a non-empty string")

    digest_fields = (
        "manifest_sha256",
        "translation_inputs_sha256",
        "identity_indexes_sha256",
        "terminology_sha256",
        "taxonomy_sha256",
        "policy_sha256",
        "inventory_sha256",
    )
    for field in digest_fields:
        value = required(field)
        if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
            _inventory_manifest_error(
                field, "must be a 64-character lowercase SHA-256 digest"
            )

    entries = required("entries")
    if type(entries) is not int or entries < 0:
        _inventory_manifest_error(
            "entries", "must be an exact non-negative integer"
        )

    for field in ("profile_classifier_version", "risk_rule_version"):
        value = required(field)
        if not isinstance(value, str) or not value:
            _inventory_manifest_error(field, "must be a non-empty string")

    expected_values = {
        "version": manifest.version,
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "identity_indexes_sha256": _identity_indexes_sha256(manifest),
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "profile_classifier_version": taxonomy["profile_classifier_version"],
        "risk_rule_version": taxonomy["risk_rule_version"],
    }
    for field, expected in expected_values.items():
        if data[field] != expected:
            _inventory_manifest_error(field, "does not match the current input")

    try:
        translation_inputs_sha256 = _current_translation_inputs_sha256(manifest)
    except ValidationError as error:
        _inventory_manifest_error(
            "translation_inputs_sha256", f"cannot be checked: {error}"
        )
    if data["translation_inputs_sha256"] != translation_inputs_sha256:
        _inventory_manifest_error(
            "translation_inputs_sha256", "does not match the current input"
        )

    terminology_path = manifest.root / manifest.terminology
    try:
        terminology_sha256 = terminology_store_sha256(terminology_path)
    except OSError as error:
        _inventory_manifest_error(
            "terminology_sha256",
            f"cannot be checked against {terminology_path}: {error}",
        )
    if data["terminology_sha256"] != terminology_sha256:
        _inventory_manifest_error(
            "terminology_sha256", "does not match the current input"
        )
    return data


def _load_inventory_bundle(
    manifest: Manifest,
    inventory_path: Path,
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load one freshness-bound inventory without changing its records."""
    inventory_manifest = _read_inventory_manifest_preflight(
        manifest, inventory_path, taxonomy, qpolicy
    )
    entries, inventory_info = read_inventory_file(inventory_path)
    if inventory_manifest["entries"] != inventory_info["entries"]:
        _inventory_manifest_error(
            "entries", "does not match the inventory JSONL"
        )
    if (
        inventory_manifest["inventory_sha256"]
        != inventory_info["inventory_sha256"]
    ):
        _inventory_manifest_error(
            "inventory_sha256", "does not match the inventory JSONL"
        )
    _validate_inventory_semantics(entries, manifest, taxonomy)
    return entries, {
        **inventory_info,
        "translation_inputs_sha256": inventory_manifest[
            "translation_inputs_sha256"
        ],
        "terminology_sha256": inventory_manifest["terminology_sha256"],
        "tool_version": inventory_manifest["tool_version"],
    }


def _validate_inventory_semantics(
    entries: list[dict[str, Any]],
    manifest: Manifest,
    taxonomy: dict[str, Any],
) -> None:
    """Validate inventory identities and declared sampling dimensions."""
    if not entries:
        return
    component_ids = {component.id for component in manifest.components}
    profile_ids = {profile["id"] for profile in taxonomy["profiles"]}
    declared_risk_flags = set(taxonomy["risk_flags"])
    length_bin_ids = {bin_spec["id"] for bin_spec in taxonomy["length_bins"]}
    editorial_to_tu = _load_editorial_to_tu(manifest)

    for index, entry in enumerate(entries):
        label = f"quality inventory record {index}"
        if entry["version"] != manifest.version:
            raise ValidationError(
                f"{label}.version must equal manifest.version"
            )
        if entry["component"] not in component_ids:
            raise ValidationError(
                f"{label}.component must be declared in manifest.components"
            )

        expected_unit_id = compute_unit_id(
            entry["component"],
            entry["section"],
            entry["source"],
            entry["source_tag"],
        )
        if entry["unit_id"] != expected_unit_id:
            raise ValidationError(
                f"{label}.unit_id does not match its editorial identity fields"
            )

        expected_revision_uid = compute_revision_uid(
            entry["tu_uid"], entry["source"]
        )
        if entry["revision_uid"] != expected_revision_uid:
            raise ValidationError(
                f"{label}.revision_uid does not match its Pilot A source revision"
            )

        expected_revision_id = compute_revision_id(
            manifest.version,
            entry["unit_id"],
            entry["target"],
            entry["args_order"],
            entry["special"],
            tu_uid=entry["tu_uid"],
            revision_uid_value=entry["revision_uid"],
            source=entry["source"],
        )
        if entry["revision_id"] != expected_revision_id:
            raise ValidationError(
                f"{label}.revision_id does not match its Pilot A revision identity"
            )

        # Pilot A binding: the recorded TU must actually be one of the TUs
        # backing this editorial in the current identity index (or the
        # domain-separated fallback when the editorial is unmapped).  This
        # rejects stale or forged TU ids even when the translation files
        # themselves did not change (infra-contract-007 review F2).
        expected_tu_uids = editorial_tu_uids(
            entry["component"],
            entry["section"],
            entry["source"],
            entry["source_tag"],
            editorial_to_tu=editorial_to_tu,
        )
        if entry["tu_uid"] not in expected_tu_uids:
            raise ValidationError(
                f"{label}.tu_uid does not belong to its editorial TU set"
            )

        if entry["profile"] not in profile_ids:
            raise ValidationError(
                f"{label}.profile must be declared in quality taxonomy.profiles"
            )
        if any(flag not in declared_risk_flags for flag in entry["risk_flags"]):
            raise ValidationError(
                f"{label}.risk_flags must use only quality taxonomy.risk_flags"
            )
        if entry["source_length_bin"] not in length_bin_ids:
            raise ValidationError(
                f"{label}.source_length_bin must be declared in quality "
                "taxonomy.length_bins"
            )


# ---------------------------------------------------------------------------
# M3: deterministic sampling
# ---------------------------------------------------------------------------


def _component_group(component: str, qpolicy: dict[str, Any]) -> str:
    for group, members in qpolicy.get("component_groups", {}).items():
        if component in members:
            return group
    return "auxiliary"


def _norm_source(source: str) -> str:
    return " ".join(_plain_source(source).split())


def _contrast_groups(
    entries: list[dict[str, Any]], qpolicy: dict[str, Any]
) -> list[tuple[str, list[dict[str, Any]]]]:
    max_size = int(qpolicy.get("contrast_group_max_size", 6))
    by_runtime_key: dict[tuple[str, str, str | None], list[dict[str, Any]]] = defaultdict(list)
    by_norm: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    semantic_signatures: dict[int, str] = {}
    for entry in entries:
        semantic_signatures[id(entry)] = runtime_semantic_signature(
            entry,
            label=f"quality inventory revision {entry.get('revision_id', '?')}",
        )
        by_runtime_key[(entry["component"], entry["source"], entry["source_tag"])].append(entry)
        by_norm[(entry["component"], _norm_source(entry["source"]))].append(entry)

    groups: list[tuple[str, list[dict[str, Any]]]] = []

    def add_group(kind: str, key: Any, members: list[dict[str, Any]]) -> None:
        members.sort(key=lambda entry: (entry["unit_id"], entry["revision_id"]))
        if len(members) > max_size:
            members = members[:max_size]
        if len(members) >= 2:
            groups.append(
                (
                    f"{kind}:{_canonical_sha256(str(key))[:12]}",
                    members,
                )
            )

    seen_keys: set[Any] = set()
    for key, members in sorted(by_runtime_key.items()):
        semantic_values = {
            semantic_signatures[id(entry)] for entry in members
        }
        targets = {entry["target"] for entry in members}
        sections = {entry["section"] for entry in members}
        if len(semantic_values) > 1:
            seen_keys.add(key)
            add_group(
                "multi-target" if len(targets) > 1 else "multi-value",
                key,
                members,
            )
        elif len(sections) > 1:
            seen_keys.add(key)
            add_group("repeated-key", key, members)
    for key, members in sorted(by_norm.items()):
        if key in seen_keys:
            continue
        raw_sources = {entry["source"] for entry in members}
        if len(raw_sources) > 1:
            add_group("near-duplicate", key, members)
    return groups


def _entry_features(entry: dict[str, Any], qpolicy: dict[str, Any]) -> dict[str, Any]:
    enrichment = set(qpolicy.get("risk_enrichment_flags", []))
    structural = {
        "has-printf", "has-args-order", "has-markup", "has-at-token", "multiline"
    }
    flags = set(entry.get("risk_flags", []))
    term_evidence = any(
        term.get("status") in ("preferred", "existing", "review")
        for term in entry.get("relevant_terms", [])
    )
    return {
        "profile": entry.get("profile", "unknown"),
        "component_group": _component_group(entry.get("component", ""), qpolicy),
        "length_bin": entry.get("source_length_bin", "unknown"),
        "structural_risk": bool(flags & structural),
        "term_evidence": term_evidence,
        "enriched": bool(flags & enrichment),
    }


def _sampling_features(
    entries: list[dict[str, Any]], qpolicy: dict[str, Any]
) -> dict[int, dict[str, Any]]:
    """Compute per-call sampling features without modifying inventory entries."""
    return {id(entry): _entry_features(entry, qpolicy) for entry in entries}


def _constraint_counts(
    selected: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    features: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    counts: dict[str, Any] = {}
    for constraint in constraints:
        feature = constraint["feature"]
        if constraint.get("mode") == "each":
            per_value = {value: 0 for value in constraint["values"]}
            for entry in selected:
                value = features[id(entry)][feature]
                if value in per_value:
                    per_value[value] += 1
            counts[constraint["id"]] = per_value
        else:
            values = set(constraint["values"])
            counts[constraint["id"]] = sum(
                1
                for entry in selected
                if features[id(entry)][feature] in values
            )
    return counts


def _deficits(
    counts: dict[str, Any], constraints: list[dict[str, Any]]
) -> dict[str, Any]:
    deficits: dict[str, Any] = {}
    for constraint in constraints:
        count = counts[constraint["id"]]
        if constraint.get("mode") == "each":
            deficits[constraint["id"]] = {
                value: max(0, constraint["min"] - count[value])
                for value in constraint["values"]
            }
        else:
            deficits[constraint["id"]] = max(0, constraint["min"] - count)
    return deficits


def _constraint_score(
    entry: dict[str, Any],
    deficits: dict[str, Any],
    constraints: list[dict[str, Any]],
    features: dict[int, dict[str, Any]],
) -> int:
    score = 0
    for constraint in constraints:
        deficit = deficits[constraint["id"]]
        feature_value = features[id(entry)][constraint["feature"]]
        if constraint.get("mode") == "each":
            if feature_value in deficit and deficit[feature_value] > 0:
                score += 1
        else:
            if (
                deficit > 0
                and feature_value in set(constraint["values"])
            ):
                score += 1
    return score


def _pick_for_deficits(
    pool: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    features: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    counts = _constraint_counts(selected, constraints, features)
    deficits = _deficits(counts, constraints)
    best_index = 0
    best_score = -1
    for index, entry in enumerate(pool):
        score = _constraint_score(entry, deficits, constraints, features)
        if score > best_score:
            best_score = score
            best_index = index
    return pool.pop(best_index)


def _select_bucket(
    pool: list[dict[str, Any]],
    target: int,
    selected: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    rng: random.Random,
    features: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    rng.shuffle(pool)
    chosen: list[dict[str, Any]] = []
    while len(chosen) < target and pool:
        chosen.append(
            _pick_for_deficits(pool, selected + chosen, constraints, features)
        )
    return chosen


def _validate_official_sample_options(
    size: int | None, seed: str | None
) -> None:
    """Validate public official-sample options before any quality I/O."""
    if size is not None and (type(size) is not int or size < 1):
        raise ValidationError("pilot sample size must be an integer >= 1")
    if seed is not None and (not isinstance(seed, str) or not seed):
        raise ValidationError("pilot sample seed must be a non-empty string")


def _load_sampling_inputs(
    manifest: Manifest, inventory_path: Path
) -> tuple[
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    """Load the rules and inventory once for either sampling workflow."""
    qpolicy = load_quality_policy(manifest)
    taxonomy = load_taxonomy(manifest)
    entries, inventory_info = _load_inventory_bundle(
        manifest, inventory_path, taxonomy, qpolicy
    )
    return entries, inventory_info, taxonomy, qpolicy


def _generate_sample_from_inventory(
    manifest: Manifest,
    *,
    entries: list[dict[str, Any]],
    inventory_info: dict[str, Any],
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    size: int | None = None,
    seed: str | None = None,
    features: dict[int, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Generate the official sample from one loaded inventory."""
    bucket_targets = qpolicy["pilot"]["buckets"]
    total_target = sum(bucket_targets.values())
    if size is None:
        size = total_target
    if size != total_target:
        raise ValidationError(
            f"pilot sample size must be {total_target} for policy-v1 "
            f"(got {size})"
        )
    if seed is None:
        seed = qpolicy["pilot"].get("seed", DEFAULT_SAMPLE_SEED)
    constraints = qpolicy.get("coverage_constraints", [])
    if features is None:
        features = _sampling_features(entries, qpolicy)

    groups = _contrast_groups(entries, qpolicy)
    rng = random.Random(seed)
    group_order = list(groups)
    rng.shuffle(group_order)

    contrast: list[dict[str, Any]] = []
    contrast_group_of: dict[str, str] = {}
    contrast_ids: set[str] = set()
    for group_id, members in group_order:
        if len(contrast) + len(members) > bucket_targets["contrast"] and contrast:
            continue
        # Contrast groups are atomic: a group whose members were already
        # claimed by an earlier overlapping group must be skipped whole,
        # never sampled partially (phase-1 doc section 6.2).
        if any(member["revision_id"] in contrast_ids for member in members):
            continue
        for member in members:
            contrast_ids.add(member["revision_id"])
            contrast_group_of[member["revision_id"]] = group_id
            contrast.append(member)
        if len(contrast) >= bucket_targets["contrast"]:
            break
    if len(contrast) < bucket_targets["contrast"]:
        # Backfill with the smallest remaining whole groups. Adding a group may
        # overshoot the bucket target, but the overshoot is bounded by the
        # smallest remaining group size (<= contrast_group_max_size) and the
        # actual bucket_counts are reported in the sample manifest, so whole
        # groups are never split to hit the exact target.
        remaining = [
            (group_id, members)
            for group_id, members in group_order
            if any(member["revision_id"] not in contrast_ids for member in members)
        ]
        remaining.sort(key=lambda item: len(item[1]))
        for group_id, members in remaining:
            if len(contrast) >= bucket_targets["contrast"]:
                break
            if any(member["revision_id"] in contrast_ids for member in members):
                continue
            for member in members:
                contrast_ids.add(member["revision_id"])
                contrast_group_of[member["revision_id"]] = group_id
                contrast.append(member)

    risk_pool = [
        entry
        for entry in entries
        if entry["revision_id"] not in contrast_ids
        and features[id(entry)]["enriched"]
    ]

    selected: list[dict[str, Any]] = list(contrast)
    risk_selected = _select_bucket(
        risk_pool,
        bucket_targets["risk-enriched"],
        selected,
        constraints,
        rng,
        features,
    )
    risk_selected_ids = {entry["revision_id"] for entry in risk_selected}
    selected.extend(risk_selected)
    # The representative bucket is a stratified random sample of the whole
    # remaining corpus (mutually exclusive with the other buckets, but not
    # restricted to non-enriched entries), per phase-1 doc section 6.1.
    representative_pool = [
        entry
        for entry in entries
        if entry["revision_id"] not in contrast_ids
        and entry["revision_id"] not in risk_selected_ids
    ]
    representative_target = size - len(contrast) - len(risk_selected)
    representative_selected = _select_bucket(
        representative_pool,
        representative_target,
        selected,
        constraints,
        rng,
        features,
    )
    selected.extend(representative_selected)

    if len(selected) != size:
        raise ValidationError(
            f"cannot build a {size}-entry pilot sample: only "
            f"{len(selected)} entries are available"
        )

    counts = _constraint_counts(selected, constraints, features)
    unmet = []
    for constraint in constraints:
        count = counts[constraint["id"]]
        if constraint.get("mode") == "each":
            for value in constraint["values"]:
                if count[value] < constraint["min"]:
                    unmet.append(
                        {
                            "id": constraint["id"],
                            "value": value,
                            "description": constraint.get("description", ""),
                            "target_min": constraint["min"],
                            "actual": count[value],
                        }
                    )
        elif count < constraint["min"]:
            unmet.append(
                {
                    "id": constraint["id"],
                    "description": constraint.get("description", ""),
                    "target_min": constraint["min"],
                    "actual": count,
                }
            )

    bucket_counts = Counter(
        [
            "contrast"
            if entry["revision_id"] in contrast_ids
            else "risk-enriched"
            if entry["revision_id"] in risk_selected_ids
            else "representative"
            for entry in selected
        ]
    )
    ordered = sorted(
        selected, key=lambda entry: (entry["unit_id"], entry["revision_id"])
    )

    items = _build_sample_items(
        entries=entries,
        ordered=ordered,
        contrast_ids=contrast_ids,
        risk_selected_ids=risk_selected_ids,
        contrast_group_of=contrast_group_of,
        contrast=contrast,
        qpolicy=qpolicy,
    )

    identity = _sample_identity(
        {
            "schema_version": 1,
            "quality_contract": SAMPLE_CONTRACT,
            "seed": seed,
            "size": size,
            "taxonomy_sha256": _canonical_sha256(taxonomy),
            "policy_sha256": _canonical_sha256(qpolicy),
            "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
            "translation_inputs_sha256": inventory_info[
                "translation_inputs_sha256"
            ],
            "terminology_sha256": inventory_info["terminology_sha256"],
            "inventory_tool_version": inventory_info["tool_version"],
            "inventory_sha256": inventory_info["inventory_sha256"],
            "items_sha256": _canonical_sha256(items),
            "bucket_targets": bucket_targets,
            "bucket_counts": dict(sorted(bucket_counts.items())),
            "revisions": [
                {"revision_id": item["revision_id"], "bucket": item["bucket"]}
                for item in items
            ],
        }
    )
    sample_id = _canonical_sha256(identity)
    sample: dict[str, Any] = {
        **identity,
        "sample_id": sample_id,
        "unmet_constraints": unmet,
        "coverage": counts,
        "items": items,
    }
    return sample


def _prepare_official_sample(
    manifest: Manifest,
    inventory_path: Path,
    *,
    size: int | None,
    seed: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load official-sample inputs once, with cheap failures first."""
    _validate_official_sample_options(size, seed)
    qpolicy = load_quality_policy(manifest)
    total_target = sum(qpolicy["pilot"]["buckets"].values())
    if size is not None and size != total_target:
        raise ValidationError(
            f"pilot sample size must be {total_target} for policy-v1 "
            f"(got {size})"
        )
    taxonomy = load_taxonomy(manifest)
    entries, inventory_info = _load_inventory_bundle(
        manifest, inventory_path, taxonomy, qpolicy
    )
    sample = _generate_sample_from_inventory(
        manifest,
        entries=entries,
        inventory_info=inventory_info,
        taxonomy=taxonomy,
        qpolicy=qpolicy,
        size=size,
        seed=seed,
    )
    return sample, qpolicy


def generate_sample(
    manifest: Manifest,
    inventory_path: Path,
    size: int | None = None,
    seed: str | None = None,
) -> dict[str, Any]:
    sample, _ = _prepare_official_sample(
        manifest,
        inventory_path,
        size=size,
        seed=seed,
    )
    return sample


def _build_sample_items(
    *,
    entries: list[dict[str, Any]],
    ordered: list[dict[str, Any]],
    contrast_ids: set[str],
    risk_selected_ids: set[str],
    contrast_group_of: dict[str, str],
    contrast: list[dict[str, Any]],
    qpolicy: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build the bounded context-packet items shared by sample and dry-run."""
    neighbors_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        neighbors_index[entry["component"]].append(entry)
    for component in neighbors_index:
        neighbors_index[component].sort(
            key=lambda entry: (
                entry["occurrences"][0]["logical_path"],
                entry["occurrences"][0]["line"]
                if entry["occurrences"][0]["line"] is not None
                else -1,
                entry["occurrences"][0]["ordinal"],
            )
        )
    neighbor_positions: dict[str, dict[int, int]] = {}
    for component, same in neighbors_index.items():
        positions: dict[int, int] = {}
        for position, entry in enumerate(same):
            positions.setdefault(id(entry), position)
        neighbor_positions[component] = positions
    limit = int(qpolicy.get("context_neighbor_limit", 2))
    items: list[dict[str, Any]] = []
    for index, entry in enumerate(ordered):
        revision_id = entry["revision_id"]
        bucket = (
            "contrast"
            if revision_id in contrast_ids
            else "risk-enriched"
            if revision_id in risk_selected_ids
            else "representative"
        )
        neighbors: list[dict[str, Any]] = []
        if entry["profile_confidence"] != "high":
            same = neighbors_index[entry["component"]]
            position = neighbor_positions.get(entry["component"], {}).get(
                id(entry), -1
            )
            if position >= 0:
                for neighbor in same[max(0, position - limit) : position]:
                    neighbors.append(
                        {
                            "component": neighbor["component"],
                            "section": neighbor["section"],
                            "source": neighbor["source"],
                            "target": neighbor["target"],
                            "source_tag": neighbor["source_tag"],
                        }
                    )
                for neighbor in same[position + 1 : position + 1 + limit]:
                    neighbors.append(
                        {
                            "component": neighbor["component"],
                            "section": neighbor["section"],
                            "source": neighbor["source"],
                            "target": neighbor["target"],
                            "source_tag": neighbor["source_tag"],
                        }
                    )
        items.append(
            {
                "index": index,
                "bucket": bucket,
                "contrast_group": contrast_group_of.get(revision_id),
                "contrast_siblings": [
                    member["revision_id"]
                    for member in contrast
                    if member["revision_id"] in contrast_group_of
                    and contrast_group_of[member["revision_id"]]
                    == contrast_group_of.get(revision_id)
                    and member["revision_id"] != revision_id
                ],
                "revision_id": revision_id,
                "unit_id": entry["unit_id"],
                "tu_uid": entry["tu_uid"],
                "revision_uid": entry["revision_uid"],
                "component": entry["component"],
                "section": entry["section"],
                "source": entry["source"],
                "target": entry["target"],
                "source_tag": entry["source_tag"],
                "args_order": entry["args_order"],
                "special": entry["special"],
                "profile": entry["profile"],
                "profile_confidence": entry["profile_confidence"],
                "domain_hints": entry["domain_hints"],
                "relevant_terms": entry["relevant_terms"],
                "structure": entry["structure"],
                "gate_signals": entry["gate_signals"],
                "risk_flags": entry["risk_flags"],
                "source_length_bin": entry["source_length_bin"],
                "context_neighbors": neighbors,
            }
        )
    return items


def _prepare_dry_run(
    manifest: Manifest, inventory_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load dry-run inputs once and return the sample with its policy.

    The official 120-item sample is regenerated with its fixed seed and its
    revision ids are excluded, so dry-run items are always disjoint from it.
    """
    entries, inventory_info, taxonomy, qpolicy = _load_sampling_inputs(
        manifest, inventory_path
    )
    dry = qpolicy["dry_run"]
    constraints = dry.get("coverage_constraints", [])
    target = int(dry["size"])
    features = _sampling_features(entries, qpolicy)

    official = _generate_sample_from_inventory(
        manifest,
        entries=entries,
        inventory_info=inventory_info,
        taxonomy=taxonomy,
        qpolicy=qpolicy,
        features=features,
    )
    official_ids = {item["revision_id"] for item in official["items"]}
    pool = [entry for entry in entries if entry["revision_id"] not in official_ids]

    rng = random.Random(dry["seed"])
    contrast_ids: set[str] = set()
    contrast_group_of: dict[str, str] = {}
    contrast: list[dict[str, Any]] = []
    groups = _contrast_groups(pool, qpolicy)
    group_order = list(groups)
    rng.shuffle(group_order)
    for group_id, members in group_order:
        if len(members) > 4:
            continue
        for member in members:
            contrast_ids.add(member["revision_id"])
            contrast_group_of[member["revision_id"]] = group_id
            contrast.append(member)
        break

    selected: list[dict[str, Any]] = list(contrast)
    remaining_pool = [entry for entry in pool if entry["revision_id"] not in contrast_ids]
    filled = _select_bucket(
        remaining_pool,
        target - len(contrast),
        selected,
        constraints,
        rng,
        features,
    )
    selected.extend(filled)
    if len(selected) != target:
        raise ValidationError(
            f"cannot build a {target}-item dry-run: only {len(selected)} items available"
        )

    counts = _constraint_counts(selected, constraints, features)
    unmet = []
    for constraint in constraints:
        count = counts[constraint["id"]]
        if constraint.get("mode") == "each":
            for value in constraint["values"]:
                if count[value] < constraint["min"]:
                    unmet.append(
                        {
                            "id": constraint["id"],
                            "value": value,
                            "description": constraint.get("description", ""),
                            "target_min": constraint["min"],
                            "actual": count[value],
                        }
                    )
        elif count < constraint["min"]:
            unmet.append(
                {
                    "id": constraint["id"],
                    "description": constraint.get("description", ""),
                    "target_min": constraint["min"],
                    "actual": count,
                }
            )

    ordered = sorted(selected, key=lambda entry: (entry["unit_id"], entry["revision_id"]))
    items = _build_sample_items(
        entries=pool,
        ordered=ordered,
        contrast_ids=contrast_ids,
        risk_selected_ids=set(),
        contrast_group_of=contrast_group_of,
        contrast=contrast,
        qpolicy=qpolicy,
    )
    identity = _sample_identity(
        {
            "schema_version": 1,
            "quality_contract": dry["contract"],
            "seed": dry["seed"],
            "size": target,
            "official_sample_id": official["sample_id"],
            "taxonomy_sha256": _canonical_sha256(taxonomy),
            "policy_sha256": _canonical_sha256(qpolicy),
            "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
            "translation_inputs_sha256": inventory_info[
                "translation_inputs_sha256"
            ],
            "terminology_sha256": inventory_info["terminology_sha256"],
            "inventory_tool_version": inventory_info["tool_version"],
            "inventory_sha256": inventory_info["inventory_sha256"],
            "items_sha256": _canonical_sha256(items),
            "revisions": [
                {"revision_id": item["revision_id"], "bucket": item["bucket"]}
                for item in items
            ],
        }
    )
    sample_id = _canonical_sha256(identity)
    dry_run = {
        **identity,
        "sample_id": sample_id,
        "coverage": counts,
        "unmet_constraints": unmet,
        "items": items,
    }
    return dry_run, qpolicy


def generate_dry_run(
    manifest: Manifest, inventory_path: Path
) -> dict[str, Any]:
    """12 rubric try-out items that never enter the official pilot sample."""
    dry_run, _ = _prepare_dry_run(manifest, inventory_path)
    return dry_run


def run_dry_run(manifest: Manifest, inventory_path: Path) -> dict[str, Any]:
    dry_run, qpolicy = _prepare_dry_run(manifest, inventory_path)
    run_directory = create_quality_run_directory(manifest.root, "dry-run")
    dry_run_path = run_directory / "dry-run.json"
    write_json(dry_run_path, dry_run)
    items = dry_run.pop("items")
    templates = []
    for evaluator_id in qpolicy["pilot"]["evaluator_ids"]:
        templates.append(
            {
                "schema_version": 1,
                "quality_contract": ASSESSMENT_CONTRACT,
                "sample_id": dry_run["sample_id"],
                "evaluator": {
                    "kind": "human",
                    "id": evaluator_id,
                    "method_version": qpolicy["pilot"]["method_version"],
                },
                "items": [
                    {
                        "revision_id": item["revision_id"],
                        "context_sufficient": None,
                        "profile_confirmed": None,
                        "findings": [],
                        "reuse_recommendation": None,
                    }
                    for item in items
                ],
            }
        )
    template_paths = []
    for template in templates:
        name = f"assessment-template-{template['evaluator']['id']}.json"
        write_json(run_directory / name, template)
        template_paths.append(name)
    dry_run["items"] = items
    manifest_report = {
        "schema_version": 1,
        "quality_contract": dry_run["quality_contract"],
        "sample_id": dry_run["sample_id"],
        "official_sample_id": dry_run["official_sample_id"],
        "seed": dry_run["seed"],
        "size": dry_run["size"],
        "coverage": dry_run["coverage"],
        "unmet_constraints": dry_run["unmet_constraints"],
        "dry_run": os_path_relative(dry_run_path, manifest),
        "assessment_templates": [
            os_path_relative(run_directory / name, manifest) for name in template_paths
        ],
        "run_directory": os_path_relative(run_directory, manifest),
    }
    write_json(run_directory / "dry-run-manifest.json", manifest_report)
    dry_run["dry_run_path"] = os_path_relative(dry_run_path, manifest)
    dry_run["run_directory"] = os_path_relative(run_directory, manifest)
    return dry_run


def run_sample(
    manifest: Manifest,
    inventory_path: Path,
    size: int | None = None,
    seed: str | None = None,
) -> dict[str, Any]:
    sample, qpolicy = _prepare_official_sample(
        manifest,
        inventory_path,
        size=size,
        seed=seed,
    )
    run_directory = create_quality_run_directory(manifest.root, "sample")
    sample_path = run_directory / "sample.json"
    write_json(sample_path, sample)
    items = sample.pop("items")
    template_a = {
        "schema_version": 1,
        "quality_contract": ASSESSMENT_CONTRACT,
        "sample_id": sample["sample_id"],
        "evaluator": {
            "kind": "human",
            "id": qpolicy["pilot"]["evaluator_ids"][0],
            "method_version": qpolicy["pilot"]["method_version"],
        },
        "items": [
            {
                "revision_id": item["revision_id"],
                "context_sufficient": None,
                "profile_confirmed": None,
                "findings": [],
                "reuse_recommendation": None,
            }
            for item in items
        ],
    }
    template_b = {
        **template_a,
        "evaluator": {
            **template_a["evaluator"],
            "id": qpolicy["pilot"]["evaluator_ids"][1],
        },
    }
    write_json(run_directory / "assessment-template-a.json", template_a)
    write_json(run_directory / "assessment-template-b.json", template_b)
    manifest_report = {
        "schema_version": 1,
        "quality_contract": SAMPLE_CONTRACT,
        "sample_id": sample["sample_id"],
        "seed": sample["seed"],
        "size": sample["size"],
        "bucket_counts": sample["bucket_counts"],
        "unmet_constraints": sample["unmet_constraints"],
        "coverage": sample["coverage"],
        "sample": os_path_relative(sample_path, manifest),
        "assessment_template_a": os_path_relative(
            run_directory / "assessment-template-a.json", manifest
        ),
        "assessment_template_b": os_path_relative(
            run_directory / "assessment-template-b.json", manifest
        ),
        "run_directory": os_path_relative(run_directory, manifest),
    }
    write_json(run_directory / "sample-manifest.json", manifest_report)
    sample["items"] = items
    sample["sample_path"] = os_path_relative(sample_path, manifest)
    sample["run_directory"] = os_path_relative(run_directory, manifest)
    return sample


# ---------------------------------------------------------------------------
# M4/M5 support: strict validation
# ---------------------------------------------------------------------------


def _check_path_safety(value: Any, errors: list[str], where: str) -> None:
    if isinstance(value, str):
        if HOST_ABSOLUTE_PATH_RE.search(value) or WINDOWS_PATH_RE.search(value):
            errors.append(f"{where}: contains a host absolute path")
        if DOTDOT_PATH_RE.search(value):
            errors.append(f"{where}: contains a '..' path segment")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _check_path_safety(item, errors, f"{where}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _check_path_safety(item, errors, f"{where}.{key}")


def _check_unknown_fields(
    value: dict[str, Any],
    allowed: set[str],
    errors: list[str],
    where: str,
    strict: bool,
) -> None:
    if not strict:
        return
    unknown = set(value) - allowed
    if unknown:
        errors.append(f"{where}: unknown fields {sorted(unknown)}")


def _check_evaluator_policy_identity(
    evaluator: dict[str, Any],
    qpolicy: dict[str, Any],
    errors: list[str],
    where: str,
) -> None:
    evaluator_id = evaluator.get("id")
    allowed_ids = qpolicy["pilot"]["evaluator_ids"]
    if isinstance(evaluator_id, str) and evaluator_id not in allowed_ids:
        errors.append(
            f"{where}.id: {evaluator_id!r} is not declared in "
            "quality policy.pilot.evaluator_ids"
        )

    method_version = evaluator.get("method_version")
    expected_method = qpolicy["pilot"]["method_version"]
    if not isinstance(method_version, str):
        errors.append(f"{where}.method_version is required")
    elif method_version != expected_method:
        errors.append(
            f"{where}.method_version: {method_version!r} does not match "
            f"quality policy.pilot.method_version {expected_method!r}"
        )


def _load_assessment(
    path: Path,
    sample: dict[str, Any],
    evaluator_seen: set[str],
    strict: bool,
    qpolicy: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    data = _read_json(path, "quality assessment")
    errors: list[str] = []
    _check_unknown_fields(
        data,
        {"schema_version", "quality_contract", "sample_id", "evaluator", "items"},
        errors,
        str(path),
        strict,
    )
    if data.get("quality_contract") != ASSESSMENT_CONTRACT:
        errors.append(f"{path}: unsupported assessment contract")
    if (
        type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        errors.append(f"{path}: unsupported assessment schema")
    if data.get("sample_id") != sample["sample_id"]:
        errors.append(f"{path}: sample_id does not match the sample")
    evaluator = data.get("evaluator")
    if not isinstance(evaluator, dict) or not isinstance(evaluator.get("id"), str):
        errors.append(f"{path}: evaluator.id is required")
    else:
        _check_unknown_fields(
            evaluator,
            {
                "kind",
                "id",
                "method_version",
                "provider",
                "model",
                "thinking",
                "prompt_sha256",
                "bundle_id",
            },
            errors,
            f"{path}.evaluator",
            strict,
        )
        if evaluator["id"] in evaluator_seen:
            errors.append(f"{path}: duplicate evaluator id {evaluator['id']!r}")
        evaluator_seen.add(evaluator["id"])
        if evaluator.get("kind") not in ("human", "model"):
            errors.append(f"{path}: evaluator.kind must be human or model")
        _check_evaluator_policy_identity(
            evaluator,
            qpolicy,
            errors,
            f"{path}: evaluator",
        )
    _check_path_safety(data, errors, str(path))
    return (data if not errors else None), errors


def _validate_assessment_items(
    assessment: dict[str, Any],
    sample: dict[str, Any],
    taxonomy: dict[str, Any],
    strict: bool,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    evaluator = assessment["evaluator"]
    errors_out: list[str] = []
    sample_revisions = {item["revision_id"] for item in sample["items"]}
    items = assessment.get("items")
    if not isinstance(items, list):
        raise ValidationError(f"assessment {evaluator['id']}: items must be an array")
    valid_codes = {code["code"] for code in taxonomy["error_codes"]}
    valid_severities = {severity["id"] for severity in taxonomy["severities"]}
    valid_profiles = {profile["id"] for profile in taxonomy["profiles"]}
    valid_reuse = {scope["id"] for scope in taxonomy["reuse_scopes"]}
    seen_revisions: set[str] = set()
    seen_findings: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        where = f"assessment {evaluator['id']} items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: not an object")
            continue
        _check_unknown_fields(
            item,
            {
                "revision_id", "context_sufficient", "profile_confirmed",
                "findings", "reuse_recommendation",
            },
            errors,
            where,
            strict,
        )
        revision_id = item.get("revision_id")
        if not isinstance(revision_id, str) or not re.fullmatch(r"[0-9a-f]{64}", revision_id):
            errors.append(f"{where}: invalid revision_id")
            continue
        if revision_id not in sample_revisions:
            errors.append(f"{where}: unknown revision_id")
            continue
        if revision_id in seen_revisions:
            errors.append(f"{where}: duplicate revision_id")
        seen_revisions.add(revision_id)
        if not isinstance(item.get("context_sufficient"), bool):
            errors.append(f"{where}: context_sufficient must be a boolean")
        profile_confirmed = item.get("profile_confirmed")
        if profile_confirmed is not None and profile_confirmed not in valid_profiles:
            errors.append(f"{where}: unknown profile {profile_confirmed!r}")
        reuse = item.get("reuse_recommendation")
        if reuse is not None and reuse not in valid_reuse:
            errors.append(f"{where}: unknown reuse scope {reuse!r}")
        findings = item.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{where}: findings must be an array")
            findings = []
        normalized_findings: list[dict[str, Any]] = []
        for finding_index, finding in enumerate(findings):
            fwhere = f"{where}.findings[{finding_index}]"
            if not isinstance(finding, dict):
                errors.append(f"{fwhere}: not an object")
                continue
            _check_unknown_fields(
                finding,
                {
                    "finding_id", "error_code", "severity", "source_span",
                    "target_span", "body", "evidence_refs",
                },
                errors,
                fwhere,
                strict,
            )
            finding_id = finding.get("finding_id")
            if not isinstance(finding_id, str) or not finding_id:
                errors.append(f"{fwhere}: finding_id is required")
            elif finding_id in seen_findings:
                errors.append(f"{fwhere}: duplicate finding_id {finding_id!r}")
            else:
                seen_findings.add(finding_id)
            code = finding.get("error_code")
            if code not in valid_codes:
                errors.append(f"{fwhere}: unknown error code {code!r}")
            severity = finding.get("severity")
            if severity not in valid_severities:
                errors.append(f"{fwhere}: unknown severity {severity!r}")
            for field in ("source_span", "target_span", "body"):
                if not isinstance(finding.get(field), str):
                    errors.append(f"{fwhere}: {field} must be a string")
            evidence = finding.get("evidence_refs")
            if not isinstance(evidence, list) or not all(
                isinstance(value, str) for value in evidence
            ):
                errors.append(f"{fwhere}: evidence_refs must be a string array")
            else:
                for ref in evidence:
                    if (
                        HOST_ABSOLUTE_PATH_RE.search(ref)
                        or WINDOWS_PATH_RE.search(ref)
                        or DOTDOT_PATH_RE.search(ref)
                    ):
                        errors.append(f"{fwhere}: unsafe evidence ref")
            normalized_findings.append(
                {
                    "finding_id": finding_id,
                    "error_code": code,
                    "severity": severity,
                    "source_span": finding.get("source_span", ""),
                    "target_span": finding.get("target_span", ""),
                    "body": finding.get("body", ""),
                    "evidence_refs": finding.get("evidence_refs", []),
                }
            )
        normalized.append(
            {
                "revision_id": revision_id,
                "context_sufficient": item.get("context_sufficient"),
                "profile_confirmed": profile_confirmed,
                "reuse_recommendation": reuse,
                "findings": normalized_findings,
            }
        )
    if seen_revisions != sample_revisions:
        missing = sorted(sample_revisions - seen_revisions)
        extra = sorted(seen_revisions - sample_revisions)
        if missing:
            errors.append(
                f"assessment {evaluator['id']}: incomplete coverage "
                f"({len(missing)} missing revisions)"
            )
        if extra:
            errors.append(f"assessment {evaluator['id']}: extra revisions {extra}")
    return {
        "evaluator_id": evaluator["id"],
        "evaluator": evaluator,
        "items": normalized,
    }, errors


def _validate_adjudication_item_contract(
    item: dict[str, Any],
    evaluator_ids: set[str],
    vector_dimensions: set[str],
    errors: list[str],
    where: str,
) -> None:
    assessment_ids = item.get("assessment_ids")
    if not isinstance(assessment_ids, list) or not assessment_ids:
        errors.append(
            f"{where}: assessment_ids must be a non-empty string array"
        )
    else:
        string_ids: list[str] = []
        duplicate_ids: set[str] = set()
        seen_ids: set[str] = set()
        for index, evaluator_id in enumerate(assessment_ids):
            if not isinstance(evaluator_id, str) or not evaluator_id:
                errors.append(
                    f"{where}.assessment_ids[{index}]: must be a non-empty "
                    "string"
                )
                continue
            string_ids.append(evaluator_id)
            if evaluator_id in seen_ids:
                duplicate_ids.add(evaluator_id)
            seen_ids.add(evaluator_id)
        if duplicate_ids:
            errors.append(
                f"{where}: assessment_ids contains duplicates "
                f"{sorted(duplicate_ids)!r}"
            )
        actual_ids = set(string_ids)
        missing_ids = sorted(evaluator_ids - actual_ids)
        extra_ids = sorted(actual_ids - evaluator_ids)
        if missing_ids or extra_ids:
            errors.append(
                f"{where}: assessment_ids must exactly match valid assessment "
                f"evaluator ids (missing={missing_ids!r}, extra={extra_ids!r})"
            )

    vector = item.get("quality_vector")
    if not isinstance(vector, dict):
        errors.append(f"{where}: quality_vector must be an object")
        return

    actual_dimensions = set(vector)
    missing_dimensions = sorted(vector_dimensions - actual_dimensions)
    extra_dimensions = sorted(
        actual_dimensions - vector_dimensions,
        key=lambda value: (type(value).__name__, repr(value)),
    )
    if missing_dimensions:
        errors.append(
            f"{where}.quality_vector: missing dimensions "
            f"{missing_dimensions!r}"
        )
    if extra_dimensions:
        errors.append(
            f"{where}.quality_vector: extra dimensions "
            f"{extra_dimensions!r}"
        )
    for dimension, value in vector.items():
        if value is not None and (
            type(value) is not int or value < 0 or value > 4
        ):
            errors.append(
                f"{where}.quality_vector.{dimension}: must be 0-4 or null"
            )


def _validate_adjudication(
    adjudication: dict[str, Any],
    sample: dict[str, Any],
    assessments: list[dict[str, Any]],
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    strict: bool,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    _check_unknown_fields(
        adjudication,
        {"schema_version", "quality_contract", "sample_id", "items"},
        errors,
        "adjudication",
        strict,
    )
    if adjudication.get("quality_contract") != ADJUDICATION_CONTRACT:
        errors.append("unsupported adjudication contract")
    if (
        type(adjudication.get("schema_version")) is not int
        or adjudication.get("schema_version") != 1
    ):
        errors.append("unsupported adjudication schema")
    if adjudication.get("sample_id") != sample["sample_id"]:
        errors.append("adjudication sample_id does not match the sample")
    _check_path_safety(adjudication, errors, "adjudication")
    sample_by_revision = {item["revision_id"]: item for item in sample["items"]}
    sample_revisions = set(sample_by_revision)
    evaluator_ids = {assessment["evaluator_id"] for assessment in assessments}
    findings_by_evaluator: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for assessment in assessments:
        findings_by_evaluator[assessment["evaluator_id"]] = {
            item["revision_id"]: item["findings"] for item in assessment["items"]
        }
    valid_codes = {code["code"] for code in taxonomy["error_codes"]}
    valid_severities = {severity["id"] for severity in taxonomy["severities"]}
    valid_reuse = {scope["id"] for scope in taxonomy["reuse_scopes"]}
    valid_confidence = {level["id"] for level in taxonomy["confidence_levels"]}
    valid_grades = {grade["id"] for grade in taxonomy["grades"]}
    valid_states = {"confirmed", "partially_confirmed", "rejected", "resolved"}
    vector_dimensions = set(taxonomy["quality_vector_dimensions"])
    items = adjudication.get("items")
    if not isinstance(items, list):
        raise ValidationError("adjudication items must be an array")
    seen_revisions: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        where = f"adjudication items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: not an object")
            continue
        _check_unknown_fields(
            item,
            {
                "revision_id", "assessment_ids", "context_sufficient",
                "resolved_findings", "quality_vector", "confidence",
                "provisional_grade", "reuse_scope", "rationale",
            },
            errors,
            where,
            strict,
        )
        revision_id = item.get("revision_id")
        if not isinstance(revision_id, str) or not re.fullmatch(r"[0-9a-f]{64}", revision_id):
            errors.append(f"{where}: invalid revision_id")
            continue
        if revision_id not in sample_revisions:
            errors.append(f"{where}: unknown revision_id")
            continue
        if revision_id in seen_revisions:
            errors.append(f"{where}: duplicate revision_id")
        seen_revisions.add(revision_id)
        sample_item = sample_by_revision[revision_id]
        assessment_ids = item.get("assessment_ids")
        _validate_adjudication_item_contract(
            item,
            evaluator_ids,
            vector_dimensions,
            errors,
            where,
        )
        if not isinstance(item.get("context_sufficient"), bool):
            errors.append(f"{where}: context_sufficient must be a boolean")
        vector = item.get("quality_vector")
        confidence = item.get("confidence")
        if confidence not in valid_confidence:
            errors.append(f"{where}: unknown confidence {confidence!r}")
        grade = item.get("provisional_grade")
        if grade not in valid_grades:
            errors.append(f"{where}: unknown grade {grade!r}")
        reuse_scope = item.get("reuse_scope")
        if reuse_scope not in valid_reuse:
            errors.append(f"{where}: unknown reuse scope {reuse_scope!r}")
        if not isinstance(item.get("rationale"), str):
            errors.append(f"{where}: rationale must be a string")
        resolved = item.get("resolved_findings")
        if not isinstance(resolved, list):
            errors.append(f"{where}: resolved_findings must be an array")
            resolved = []
        has_confirmed_major = False
        for finding_index, finding in enumerate(resolved):
            fwhere = f"{where}.resolved_findings[{finding_index}]"
            if not isinstance(finding, dict):
                errors.append(f"{fwhere}: not an object")
                continue
            _check_unknown_fields(
                finding,
                {
                    "finding_id", "evaluator_id", "error_code", "severity",
                    "state", "body", "rationale",
                },
                errors,
                fwhere,
                strict,
            )
            finding_id = finding.get("finding_id")
            evaluator_id = finding.get("evaluator_id")
            reference_ids_valid = True
            if not isinstance(finding_id, str) or not finding_id:
                errors.append(
                    f"{fwhere}.finding_id: must be a non-empty string"
                )
                reference_ids_valid = False
            if not isinstance(evaluator_id, str) or not evaluator_id:
                errors.append(
                    f"{fwhere}.evaluator_id: must be a non-empty string"
                )
                reference_ids_valid = False
            state = finding.get("state")
            if state not in valid_states:
                errors.append(f"{fwhere}: unknown state {state!r}")
            code = finding.get("error_code")
            if code not in valid_codes:
                errors.append(f"{fwhere}: unknown error code {code!r}")
            severity = finding.get("severity")
            if severity not in valid_severities:
                errors.append(f"{fwhere}: unknown severity {severity!r}")
            if severity in ("blocker", "major") and state in (
                "confirmed", "partially_confirmed"
            ):
                has_confirmed_major = True
            if not isinstance(finding.get("body"), str):
                errors.append(f"{fwhere}: body must be a string")
            if "rationale" in finding and not isinstance(
                finding.get("rationale"), str
            ):
                errors.append(f"{fwhere}: rationale must be a string")
            if reference_ids_valid:
                pool = findings_by_evaluator.get(evaluator_id, {}).get(revision_id, [])
                if not any(
                    existing.get("finding_id") == finding_id for existing in pool
                ):
                    errors.append(
                        f"{fwhere}: finding_id {finding_id!r} does not exist in "
                        f"assessment {evaluator_id!r} for this revision"
                    )
        context_sufficient = item.get("context_sufficient") is True
        if grade == "Gold":
            if not context_sufficient:
                errors.append(f"{where}: Gold requires sufficient context")
            if confidence not in ("C2", "C3", "C4"):
                errors.append(f"{where}: Gold requires confidence C2 or above")
            if has_confirmed_major:
                errors.append(
                    f"{where}: Gold is not allowed with a confirmed "
                    f"blocker/major finding"
                )
            gates = sample_item.get("gate_signals", {})
            if gates.get("empty_target") is True:
                errors.append(f"{where}: Gold is not allowed for an empty target")
            if gates.get("format_signature_match") is False:
                errors.append(f"{where}: Gold is not allowed with a format mismatch")
            if gates.get("markup_multiset_match") is False:
                errors.append(f"{where}: Gold is not allowed with a markup mismatch")
            if gates.get("at_token_multiset_match") is False:
                errors.append(f"{where}: Gold is not allowed with a token mismatch")
            if gates.get("runtime_collision") is True:
                errors.append(f"{where}: Gold is not allowed with a runtime collision")
        elif grade == "Silver":
            if has_confirmed_major:
                errors.append(
                    f"{where}: Silver is not allowed with a confirmed "
                    f"blocker/major finding"
                )
            if confidence not in ("C2", "C3", "C4"):
                errors.append(f"{where}: Silver requires confidence C2 or above")
            gates = sample_item.get("gate_signals", {})
            if gates.get("empty_target") is True:
                errors.append(f"{where}: Silver is not allowed for an empty target")
            if gates.get("format_signature_match") is False:
                errors.append(f"{where}: Silver is not allowed with a format mismatch")
        normalized.append(
            {
                "revision_id": revision_id,
                "assessment_ids": assessment_ids,
                "context_sufficient": item.get("context_sufficient"),
                "resolved_findings": resolved,
                "quality_vector": vector,
                "confidence": confidence,
                "provisional_grade": grade,
                "reuse_scope": reuse_scope,
                "rationale": item.get("rationale", ""),
            }
        )
    if seen_revisions != sample_revisions:
        missing = sorted(sample_revisions - seen_revisions)
        if missing:
            errors.append(f"adjudication: incomplete coverage ({len(missing)} missing)")
    return {"items": normalized}, errors


def _validate_sample_identity(
    sample: dict[str, Any],
    manifest: Manifest,
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    *,
    label: str,
) -> list[str]:
    errors: list[str] = []
    contract = sample.get("quality_contract")
    identity = _sample_identity(sample)
    editorial_to_tu = _load_editorial_to_tu(manifest)
    for field in _SAMPLE_IDENTITY_FIELDS[contract]:
        if field not in sample:
            errors.append(f"{label}: sample identity is missing {field}")

    seed = sample.get("seed")
    if not isinstance(seed, str) or not seed:
        errors.append(f"{label}: sample seed is invalid")
    size = sample.get("size")
    if isinstance(size, bool) or not isinstance(size, int) or size < 1:
        errors.append(f"{label}: sample size is invalid")

    current_digests: dict[str, str | None] = {
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "translation_inputs_sha256": None,
        "terminology_sha256": None,
    }
    try:
        current_digests[
            "translation_inputs_sha256"
        ] = _current_translation_inputs_sha256(manifest)
    except ValidationError as error:
        errors.append(
            f"{label}: sample translation_inputs_sha256 cannot be checked: "
            f"{error}"
        )
    terminology_path = manifest.root / manifest.terminology
    try:
        from .terminology import terminology_store_sha256

        current_digests["terminology_sha256"] = terminology_store_sha256(
            terminology_path
        )
    except OSError as error:
        errors.append(
            f"{label}: sample terminology_sha256 cannot be checked against "
            f"{terminology_path}: {error}"
        )
    for field, expected in current_digests.items():
        value = sample.get(field)
        if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
            errors.append(f"{label}: sample {field} is not a SHA-256 digest")
        elif expected is not None and value != expected:
            errors.append(f"{label}: sample {field} is stale or invalid")

    inventory_tool_version = sample.get("inventory_tool_version")
    if inventory_tool_version != TOOL_VERSION:
        errors.append(
            f"{label}: sample inventory_tool_version is stale or invalid"
        )
    inventory_digest = sample.get("inventory_sha256")
    if (
        not isinstance(inventory_digest, str)
        or SHA256_RE.fullmatch(inventory_digest) is None
    ):
        errors.append(f"{label}: sample inventory_sha256 is not a SHA-256 digest")

    items = sample.get("items")
    items_digest = sample.get("items_sha256")
    if not isinstance(items_digest, str) or SHA256_RE.fullmatch(items_digest) is None:
        errors.append(f"{label}: sample items_sha256 is not a SHA-256 digest")
    elif isinstance(items, list) and items_digest != _canonical_sha256(items):
        errors.append(f"{label}: sample items_sha256 does not match items")

    derived_revisions: list[dict[str, Any]] = []
    item_identities_valid = isinstance(items, list) and bool(items)
    if isinstance(items, list):
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{label}: sample item {index} is not an object")
                item_identities_valid = False
                continue
            identity_fields = (
                "unit_id",
                "revision_id",
                "tu_uid",
                "revision_uid",
                "component",
                "section",
                "source",
                "source_tag",
                "target",
                "args_order",
                "special",
                "bucket",
            )
            missing_fields = [field for field in identity_fields if field not in item]
            if missing_fields:
                errors.append(
                    f"{label}: sample item {index} identity is missing "
                    + ", ".join(missing_fields)
                )
                item_identities_valid = False

            unit_id = item.get("unit_id")
            revision_id = item.get("revision_id")
            tu_uid = item.get("tu_uid")
            revision_uid_value = item.get("revision_uid")
            bucket = item.get("bucket")
            if not isinstance(unit_id, str) or SHA256_RE.fullmatch(unit_id) is None:
                errors.append(
                    f"{label}: sample item {index} unit_id is not a SHA-256 digest"
                )
                item_identities_valid = False
            if not isinstance(revision_id, str) or SHA256_RE.fullmatch(revision_id) is None:
                errors.append(
                    f"{label}: sample item {index} revision_id is not a SHA-256 digest"
                )
                item_identities_valid = False
            if not isinstance(tu_uid, str) or SHA256_RE.fullmatch(tu_uid) is None:
                errors.append(
                    f"{label}: sample item {index} tu_uid is not a SHA-256 digest"
                )
                item_identities_valid = False
            if (
                not isinstance(revision_uid_value, str)
                or SHA256_RE.fullmatch(revision_uid_value) is None
            ):
                errors.append(
                    f"{label}: sample item {index} revision_uid is not a SHA-256 digest"
                )
                item_identities_valid = False
            if not isinstance(bucket, str) or not bucket:
                errors.append(f"{label}: sample item {index} bucket is invalid")
                item_identities_valid = False

            component = item.get("component")
            section = item.get("section")
            source = item.get("source")
            source_tag = item.get("source_tag")
            unit_materials_valid = True
            if not isinstance(component, str) or not component:
                errors.append(f"{label}: sample item {index} component is invalid")
                unit_materials_valid = False
                item_identities_valid = False
            if not isinstance(section, str):
                errors.append(f"{label}: sample item {index} section is invalid")
                unit_materials_valid = False
                item_identities_valid = False
            if not isinstance(source, str) or not source:
                errors.append(f"{label}: sample item {index} source is invalid")
                unit_materials_valid = False
                item_identities_valid = False
            if source_tag is not None and not isinstance(source_tag, str):
                errors.append(f"{label}: sample item {index} source_tag is invalid")
                unit_materials_valid = False
                item_identities_valid = False
            if "source_tag" not in item:
                unit_materials_valid = False

            expected_unit_id: str | None = None
            if unit_materials_valid:
                expected_unit_id = compute_unit_id(
                    component, section, source, source_tag
                )
                if unit_id != expected_unit_id:
                    errors.append(
                        f"{label}: sample item {index} unit_id does not match "
                        "its editorial identity"
                    )
                    item_identities_valid = False

            target = item.get("target")
            args_order = item.get("args_order")
            revision_materials_valid = (
                expected_unit_id is not None
                and isinstance(tu_uid, str)
                and SHA256_RE.fullmatch(tu_uid) is not None
            )
            if not isinstance(target, str):
                errors.append(f"{label}: sample item {index} target is invalid")
                revision_materials_valid = False
                item_identities_valid = False
            if args_order is not None and not (
                isinstance(args_order, list)
                and all(
                    isinstance(value, int) and not isinstance(value, bool)
                    for value in args_order
                )
            ):
                errors.append(f"{label}: sample item {index} args_order is invalid")
                revision_materials_valid = False
                item_identities_valid = False
            if "target" not in item or "args_order" not in item or "special" not in item:
                revision_materials_valid = False
            if revision_materials_valid:
                expected_revision_uid = compute_revision_uid(tu_uid, source)
                if revision_uid_value != expected_revision_uid:
                    errors.append(
                        f"{label}: sample item {index} revision_uid does not match "
                        "its Pilot A source revision"
                    )
                    item_identities_valid = False
                expected_tu_uids = editorial_tu_uids(
                    component,
                    section,
                    source,
                    source_tag,
                    editorial_to_tu=editorial_to_tu,
                )
                if tu_uid not in expected_tu_uids:
                    errors.append(
                        f"{label}: sample item {index} tu_uid does not belong "
                        "to its editorial TU set"
                    )
                    item_identities_valid = False
                expected_revision_id = compute_revision_id(
                    manifest.version,
                    expected_unit_id,
                    target,
                    args_order,
                    item.get("special"),
                    tu_uid=tu_uid,
                    revision_uid_value=revision_uid_value,
                    source=source,
                )
                if revision_id != expected_revision_id:
                    errors.append(
                        f"{label}: sample item {index} revision_id does not match "
                        "its Pilot A revision identity"
                    )
                    item_identities_valid = False
            derived_revisions.append(
                {"revision_id": revision_id, "bucket": bucket}
            )
        if isinstance(size, int) and not isinstance(size, bool) and size != len(items):
            errors.append(f"{label}: sample size does not match items")

    revisions = sample.get("revisions")
    revisions_valid = isinstance(revisions, list) and bool(revisions)
    if not revisions_valid:
        errors.append(f"{label}: sample revisions are invalid or empty")
    else:
        for index, revision in enumerate(revisions):
            if not isinstance(revision, dict) or set(revision) != {
                "revision_id",
                "bucket",
            }:
                errors.append(f"{label}: sample revision {index} is malformed")
                revisions_valid = False
                continue
            revision_id = revision.get("revision_id")
            bucket = revision.get("bucket")
            if not isinstance(revision_id, str) or SHA256_RE.fullmatch(revision_id) is None:
                errors.append(
                    f"{label}: sample revision {index} revision_id is not a SHA-256 digest"
                )
                revisions_valid = False
            if not isinstance(bucket, str) or not bucket:
                errors.append(f"{label}: sample revision {index} bucket is invalid")
                revisions_valid = False
        if isinstance(size, int) and not isinstance(size, bool) and size != len(revisions):
            errors.append(f"{label}: sample size does not match revisions")
    if revisions_valid and item_identities_valid and revisions != derived_revisions:
        errors.append(f"{label}: sample revisions do not match items")

    if item_identities_valid:
        revision_ids = [revision["revision_id"] for revision in derived_revisions]
        if len(revision_ids) != len(set(revision_ids)):
            errors.append(f"{label}: duplicate revision_id in sample")

    pilot_buckets = qpolicy["pilot"]["buckets"]
    if contract == SAMPLE_CONTRACT:
        if item_identities_valid:
            unknown_buckets = sorted(
                {
                    revision["bucket"]
                    for revision in derived_revisions
                    if revision["bucket"] not in pilot_buckets
                }
            )
            if unknown_buckets:
                errors.append(
                    f"{label}: sample has unknown buckets: "
                    + ", ".join(unknown_buckets)
                )
        if sample.get("bucket_targets") != pilot_buckets:
            errors.append(f"{label}: sample bucket_targets do not match current policy")
        bucket_counts = sample.get("bucket_counts")
        if not isinstance(bucket_counts, dict) or any(
            not isinstance(bucket, str)
            or isinstance(count, bool)
            or not isinstance(count, int)
            or count < 0
            for bucket, count in (
                bucket_counts.items() if isinstance(bucket_counts, dict) else ()
            )
        ):
            errors.append(f"{label}: sample bucket_counts are invalid")
        elif item_identities_valid:
            expected_counts = dict(
                sorted(Counter(revision["bucket"] for revision in derived_revisions).items())
            )
            if bucket_counts != expected_counts:
                errors.append(f"{label}: sample bucket_counts do not match items")
        expected_size = sum(pilot_buckets.values())
        if isinstance(size, int) and not isinstance(size, bool) and size != expected_size:
            errors.append(f"{label}: sample size does not match current policy")
    elif contract == DRY_RUN_CONTRACT:
        if item_identities_valid:
            unknown_buckets = sorted(
                {
                    revision["bucket"]
                    for revision in derived_revisions
                    if revision["bucket"] not in {"contrast", "representative"}
                }
            )
            if unknown_buckets:
                errors.append(
                    f"{label}: dry-run sample has unknown buckets: "
                    + ", ".join(unknown_buckets)
                )
        official_sample_id = sample.get("official_sample_id")
        if (
            not isinstance(official_sample_id, str)
            or SHA256_RE.fullmatch(official_sample_id) is None
        ):
            errors.append(
                f"{label}: sample official_sample_id is not a SHA-256 digest"
            )
        dry_policy = qpolicy["dry_run"]
        if seed != dry_policy["seed"]:
            errors.append(f"{label}: dry-run seed does not match current policy")
        if size != int(dry_policy["size"]):
            errors.append(f"{label}: dry-run size does not match current policy")
        if contract != dry_policy["contract"]:
            errors.append(f"{label}: dry-run contract does not match current policy")

    sample_id = sample.get("sample_id")
    if not isinstance(sample_id, str) or SHA256_RE.fullmatch(sample_id) is None:
        errors.append(f"{label}: sample_id is not a SHA-256 digest")
    elif sample_id != _canonical_sha256(identity):
        errors.append(f"{label}: sample_id does not match canonical sample identity")
    return errors


def _load_sample_file(
    path: Path,
    *,
    manifest: Manifest,
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    dry_run: bool = False,
) -> dict[str, Any]:
    sample = _read_json(path, "quality sample")
    errors: list[str] = []
    allowed_contracts = (SAMPLE_CONTRACT, DRY_RUN_CONTRACT) if dry_run else (SAMPLE_CONTRACT,)
    if sample.get("quality_contract") not in allowed_contracts:
        errors.append(f"{path}: unsupported sample contract")
    schema_version = sample.get("schema_version")
    if type(schema_version) is not int or schema_version != 1:
        errors.append(f"{path}: unsupported sample schema")
    items = sample.get("items")
    if not isinstance(items, list) or not items:
        errors.append(f"{path}: sample items are invalid or empty")
    _check_path_safety(sample, errors, str(path))
    contract = sample.get("quality_contract")
    if isinstance(contract, str) and contract in _SAMPLE_IDENTITY_FIELDS:
        errors.extend(
            _validate_sample_identity(
                sample,
                manifest,
                taxonomy,
                qpolicy,
                label=str(path),
            )
        )
    if errors:
        raise ValidationError("; ".join(errors))
    return sample


def _validate_quality_run_flags(strict: bool | None, dry_run: bool) -> None:
    if strict is not None and type(strict) is not bool:
        raise ValidationError(
            "quality validation strict flag must be None or an exact bool"
        )
    if type(dry_run) is not bool:
        raise ValidationError(
            "quality validation dry_run flag must be an exact bool"
        )


def validate_quality_run(
    manifest: Manifest,
    sample_path: Path,
    assessment_paths: list[Path],
    adjudication_path: Path | None,
    strict: bool | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    _validate_quality_run_flags(strict, dry_run)
    taxonomy = load_taxonomy(manifest)
    qpolicy = load_quality_policy(manifest)
    # policy-v1 declares strict unknown-field behavior; the CLI --strict flag
    # overrides it, but the policy default applies when the flag is absent.
    if strict is None:
        strict = bool(qpolicy.get("strict_unknown_fields", False))
    sample = _load_sample_file(
        sample_path,
        manifest=manifest,
        taxonomy=taxonomy,
        qpolicy=qpolicy,
        dry_run=dry_run,
    )
    warnings: list[str] = []
    if dry_run and sample.get("quality_contract") == SAMPLE_CONTRACT:
        warnings.append(
            "dry-run validation is using the official sample contract; "
            "this result is non-official and cannot satisfy the adjudicated pilot gate"
        )
    sample_revisions = {item["revision_id"] for item in sample["items"]}
    revision_ids = [item["revision_id"] for item in sample["items"]]
    if len(revision_ids) != len(set(revision_ids)):
        raise ValidationError(f"{sample_path}: duplicate revision_id in sample")
    if not assessment_paths:
        raise ValidationError("at least one --assessment is required")
    if len(assessment_paths) > 2:
        raise ValidationError("pilot validation accepts at most two assessments")
    evaluator_seen: set[str] = set()
    assessments: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in assessment_paths:
        assessment, load_errors = _load_assessment(
            path, sample, evaluator_seen, strict, qpolicy
        )
        errors.extend(load_errors)
        if assessment is None:
            continue
        normalized, item_errors = _validate_assessment_items(
            assessment, sample, taxonomy, strict
        )
        errors.extend(item_errors)
        assessments.append(normalized)

    if not dry_run:
        expected_evaluator_ids = set(qpolicy["pilot"]["evaluator_ids"])
        actual_evaluator_ids = {
            assessment["evaluator_id"] for assessment in assessments
        }
        if len(assessments) != len(expected_evaluator_ids):
            errors.append(
                "official pilot validation requires exactly two valid assessments"
            )
        if actual_evaluator_ids != expected_evaluator_ids:
            errors.append(
                "official pilot assessment evaluator ids must exactly match "
                "quality policy.pilot.evaluator_ids; expected "
                f"{sorted(expected_evaluator_ids)!r}, got "
                f"{sorted(actual_evaluator_ids)!r}"
            )
    normalized_adjudication: dict[str, Any] = {"items": []}
    if adjudication_path is not None:
        adjudication = _read_json(adjudication_path, "quality adjudication")
        try:
            normalized_adjudication, adjudication_errors = _validate_adjudication(
                adjudication, sample, assessments, taxonomy, qpolicy, strict
            )
            errors.extend(adjudication_errors)
        except ValidationError as error:
            errors.append(str(error))
    elif not dry_run:
        errors.append("an adjudication is required for the official pilot sample")

    normalized_assessments = [
        {
            "evaluator_id": assessment["evaluator_id"],
            "evaluator": assessment["evaluator"],
            "items": assessment["items"],
        }
        for assessment in assessments
    ]
    validation = {
        "schema_version": 1,
        "quality_contract": VALIDATION_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "sample_id": sample["sample_id"],
        "dry_run": dry_run,
        "strict": strict,
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "errors": errors,
        "warnings": warnings,
        "sample": sample,
        "assessments": normalized_assessments,
        "adjudication": normalized_adjudication,
    }
    validation["ok"] = not errors
    return validation


def run_validation(
    manifest: Manifest,
    sample_path: Path,
    assessment_paths: list[Path],
    adjudication_path: Path | None,
    strict: bool | None,
    dry_run: bool = False,
) -> dict[str, Any]:
    validation = validate_quality_run(
        manifest, sample_path, assessment_paths, adjudication_path, strict,
        dry_run=dry_run,
    )
    run_directory = create_quality_run_directory(manifest.root, "validation")
    _write_jsonl(
        run_directory / "normalized-assessments.jsonl",
        validation["assessments"],
    )
    if validation["adjudication"].get("items"):
        _write_jsonl(
            run_directory / "normalized-adjudications.jsonl",
            validation["adjudication"].get("items", []),
        )
    write_json(run_directory / "validation.json", validation)
    summary = {
        "ok": validation["ok"],
        "strict": validation["strict"],
        "sample_id": validation["sample_id"],
        "errors": validation["errors"],
        "warnings": validation["warnings"],
        "assessments": [
            {
                "evaluator_id": assessment["evaluator_id"],
                "kind": assessment["evaluator"].get("kind"),
                "items": len(assessment["items"]),
            }
            for assessment in validation["assessments"]
        ],
        "run_directory": os_path_relative(run_directory, manifest),
        "validation_path": os_path_relative(
            run_directory / "validation.json", manifest
        ),
    }
    return summary


# ---------------------------------------------------------------------------
# M5/M6 support: report
# ---------------------------------------------------------------------------


def _profile_disagreements(
    sample: dict[str, Any], assessments: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Automatic inventory profile vs confirmed evaluator profile."""
    auto_by_revision = {
        item["revision_id"]: item.get("profile") for item in sample["items"]
    }
    by_evaluator = {
        assessment["evaluator_id"]: {
            item["revision_id"]: item for item in assessment["items"]
        }
        for assessment in assessments
    }
    disagreements: list[dict[str, Any]] = []
    for revision_id in sorted(auto_by_revision):
        auto_profile = auto_by_revision[revision_id]
        for evaluator_id, items in sorted(by_evaluator.items()):
            item = items.get(revision_id)
            if not item:
                continue
            confirmed = item.get("profile_confirmed")
            if confirmed is not None and confirmed != auto_profile:
                disagreements.append(
                    {
                        "revision_id": revision_id,
                        "auto_profile": auto_profile,
                        "confirmed_profile": confirmed,
                        "evaluator_id": evaluator_id,
                    }
                )
    return disagreements


def _span_overlap(left: str, right: str) -> bool:
    if not left or not right:
        return True
    if ":" in left and ":" in right:
        try:
            left_start, left_end = (int(part) for part in left.split(":", 1))
            right_start, right_end = (int(part) for part in right.split(":", 1))
            return left_start <= right_end and right_start <= left_end
        except ValueError:
            pass
    return left in right or right in left


def _match_findings(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
    mergeable: set[tuple[str, str]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    used: set[str] = set()
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for left_finding in left:
        best: dict[str, Any] | None = None
        for right_finding in right:
            if right_finding["finding_id"] in used:
                continue
            if left_finding["error_code"] != right_finding["error_code"]:
                pair = tuple(
                    sorted(
                        (left_finding["error_code"], right_finding["error_code"])
                    )
                )
                if pair not in mergeable:
                    continue
            if not _span_overlap(
                left_finding.get("source_span", ""),
                right_finding.get("source_span", ""),
            ):
                continue
            if not _span_overlap(
                left_finding.get("target_span", ""),
                right_finding.get("target_span", ""),
            ):
                continue
            best = right_finding
            break
        if best is not None:
            used.add(best["finding_id"])
            matches.append((left_finding, best))
    return matches


def _weighted_kappa(
    left: list[int], right: list[int], levels: int
) -> float | None:
    if len(left) != len(right) or not left:
        return None
    weight = [
        [1.0 - abs(i - j) / max(1, levels - 1) for j in range(levels)]
        for i in range(levels)
    ]
    observed = sum(weight[a][b] for a, b in zip(left, right)) / len(left)
    left_counts = Counter(left)
    right_counts = Counter(right)
    expected = sum(
        left_counts[i] * right_counts[j] * weight[i][j]
        for i in range(levels)
        for j in range(levels)
    ) / (len(left) * len(left))
    if expected >= 1.0:
        return 1.0 if observed >= 1.0 else 0.0
    return (observed - expected) / (1.0 - expected)


def build_report(
    validation: dict[str, Any], taxonomy: dict[str, Any]
) -> dict[str, Any]:
    sample = validation["sample"]
    assessments = validation["assessments"]
    adjudication = validation["adjudication"]
    items = sample["items"]
    size = len(items)
    severity_levels = ["none", "note", "minor", "major", "blocker"]
    mergeable = {
        tuple(sorted(pair)) for pair in taxonomy.get("mergeable_codes", [])
    }
    valid_codes = {code["code"] for code in taxonomy["error_codes"]}
    report: dict[str, Any] = {"sample_id": validation["sample_id"], "size": size}

    report["assessments"] = []
    for assessment in assessments:
        findings = sum(len(item["findings"]) for item in assessment["items"])
        report["assessments"].append(
            {
                "evaluator_id": assessment["evaluator_id"],
                "kind": assessment["evaluator"].get("kind"),
                "method_version": assessment["evaluator"].get("method_version"),
                "items": len(assessment["items"]),
                "findings": findings,
                "complete": len(assessment["items"]) == size,
            }
        )
    if len(assessments) < 2:
        report["agreement"] = {
            "note": "at least two assessments are required for agreement metrics"
        }
        report["distributions"] = {}
        report["calibration"] = {}
        return report

    left = assessments[0]
    right = assessments[1]
    left_by_revision = {item["revision_id"]: item for item in left["items"]}
    right_by_revision = {item["revision_id"]: item for item in right["items"]}
    adjudication_by_revision = {
        item["revision_id"]: item for item in adjudication["items"]
    }

    def substantive(item: dict[str, Any]) -> bool:
        return any(
            finding["severity"] != "note" for finding in item["findings"]
        )

    def major_or_worse(item: dict[str, Any]) -> bool:
        return any(
            finding["severity"] in ("major", "blocker")
            for finding in item["findings"]
        )

    def max_severity(item: dict[str, Any]) -> int:
        order = {name: index for index, name in enumerate(severity_levels)}
        severities = [finding["severity"] for finding in item["findings"]]
        if not severities:
            return order["none"]
        return max(order[severity] for severity in severities)

    context_agreement = 0
    defect_agreement = 0
    major_agreement = 0
    context_pairs = 0
    left_ratings: list[int] = []
    right_ratings: list[int] = []
    per_category: dict[str, dict[str, int]] = defaultdict(
        lambda: {"left": 0, "right": 0, "matched": 0}
    )
    for item in items:
        revision_id = item["revision_id"]
        left_item = left_by_revision[revision_id]
        right_item = right_by_revision[revision_id]
        context_pairs += 1
        if left_item["context_sufficient"] == right_item["context_sufficient"]:
            context_agreement += 1
        if substantive(left_item) == substantive(right_item):
            defect_agreement += 1
        if major_or_worse(left_item) == major_or_worse(right_item):
            major_agreement += 1
        left_ratings.append(max_severity(left_item))
        right_ratings.append(max_severity(right_item))
        left_findings = [
            finding for finding in left_item["findings"]
        ]
        right_findings = [
            finding for finding in right_item["findings"]
        ]
        matches = _match_findings(left_findings, right_findings, mergeable)
        matched_right = {match[1]["finding_id"] for match in matches}
        for finding in left_findings:
            per_category[finding["error_code"]]["left"] += 1
        for finding in right_findings:
            per_category[finding["error_code"]]["right"] += 1
        for left_finding, right_finding in matches:
            for code in {left_finding["error_code"], right_finding["error_code"]}:
                per_category[code]["matched"] += 1

    category_metrics: dict[str, dict[str, float]] = {}
    macro_f1_values: list[float] = []
    for code, counts in sorted(per_category.items()):
        precision = (
            counts["matched"] / counts["left"] if counts["left"] else 0.0
        )
        recall = (
            counts["matched"] / counts["right"] if counts["right"] else 0.0
        )
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
        category_metrics[code] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "left_findings": counts["left"],
            "right_findings": counts["right"],
            "matched": counts["matched"],
        }
        if counts["left"] or counts["right"]:
            macro_f1_values.append(f1)

    report["agreement"] = {
        "context_sufficient_agreement": (
            round(context_agreement / context_pairs, 4) if context_pairs else None
        ),
        "defect_presence_agreement": (
            round(defect_agreement / context_pairs, 4) if context_pairs else None
        ),
        "major_or_worse_agreement": (
            round(major_agreement / context_pairs, 4) if context_pairs else None
        ),
        "severity_weighted_kappa": _weighted_kappa(
            left_ratings, right_ratings, len(severity_levels)
        ),
        "category_metrics": category_metrics,
        "macro_f1": (
            round(sum(macro_f1_values) / len(macro_f1_values), 4)
            if macro_f1_values
            else None
        ),
    }

    resolved_codes: Counter[str] = Counter()
    resolved_severities: Counter[str] = Counter()
    confirmed_major = 0
    source_findings = 0
    context_insufficient = 0
    unmappable = 0
    for item in adjudication["items"]:
        for finding in item["resolved_findings"]:
            resolved_codes[finding["error_code"]] += 1
            resolved_severities[finding["severity"]] += 1
            if finding["error_code"] not in valid_codes:
                unmappable += 1
            if finding["state"] in ("confirmed", "partially_confirmed"):
                if finding["severity"] in ("blocker", "major"):
                    confirmed_major += 1
                if finding["error_code"].startswith("SOURCE_"):
                    source_findings += 1
                if finding["error_code"] == "CTX_INSUFFICIENT":
                    context_insufficient += 1
    report["distributions"] = {
        "adjudicated_findings": {
            "by_code": dict(sorted(resolved_codes.items())),
            "by_severity": dict(sorted(resolved_severities.items())),
            "confirmed_major_or_blocker": confirmed_major,
            "source_findings": source_findings,
            "context_insufficient": context_insufficient,
            "unmappable": unmappable,
        },
        "grades": dict(
            sorted(
                Counter(
                    item["provisional_grade"] for item in adjudication["items"]
                ).items()
            )
        ),
        "confidence": dict(
            sorted(
                Counter(item["confidence"] for item in adjudication["items"]).items()
            )
        ),
        "reuse_scopes": dict(
            sorted(
                Counter(item["reuse_scope"] for item in adjudication["items"]).items()
            )
        ),
        "buckets": dict(sorted(Counter(item["bucket"] for item in items).items())),
        "profiles": dict(sorted(Counter(item["profile"] for item in items).items())),
    }

    confirmed_by_revision = {
        item["revision_id"]: item
        for item in adjudication["items"]
        if any(
            finding["state"] in ("confirmed", "partially_confirmed")
            for finding in item["resolved_findings"]
        )
    }
    flagged_total: Counter[str] = Counter()
    flagged_confirmed: Counter[str] = Counter()
    confirmed_with_any_flag = 0
    for item in items:
        flags = tuple(dict.fromkeys(item.get("risk_flags", [])))
        for flag in flags:
            flagged_total[flag] += 1
        if item["revision_id"] not in confirmed_by_revision:
            continue
        if flags:
            confirmed_with_any_flag += 1
        for flag in flags:
            flagged_confirmed[flag] += 1
    total_confirmed = len(confirmed_by_revision)
    flag_stats = {
        flag: {
            "flagged": flagged,
            "with_confirmed": flagged_confirmed[flag],
        }
        for flag, flagged in sorted(flagged_total.items())
    }
    report["risk_flags"] = {
        "confirmed_items": total_confirmed,
        "confirmed_with_any_flag": confirmed_with_any_flag,
        "coverage": (
            round(confirmed_with_any_flag / total_confirmed, 4)
            if total_confirmed
            else None
        ),
        "per_flag": flag_stats,
    }

    taxonomy_gaps: dict[str, Any] = {
        "profile_disagreements": _profile_disagreements(sample, assessments),
        "context_insufficient_items": [],
        "source_related_items": [],
    }
    for item in items:
        revision_id = item["revision_id"]
        adjudicated = adjudication_by_revision.get(revision_id)
        if not adjudicated:
            continue
        if any(
            finding["error_code"] == "CTX_INSUFFICIENT"
            and finding["state"] in ("confirmed", "partially_confirmed")
            for finding in adjudicated["resolved_findings"]
        ):
            taxonomy_gaps["context_insufficient_items"].append(revision_id)
        if any(
            finding["error_code"].startswith("SOURCE_")
            and finding["state"] in ("confirmed", "partially_confirmed")
            for finding in adjudicated["resolved_findings"]
        ):
            taxonomy_gaps["source_related_items"].append(revision_id)
    report["taxonomy_gaps"] = taxonomy_gaps

    target = {
        "assessment_coverage": 1.0,
        "major_or_worse_agreement": 0.90,
        "defect_presence_agreement": 0.80,
        "severity_weighted_kappa": 0.70,
        "unmappable_max_ratio": 0.05,
        "context_insufficient_max_ratio": 0.10,
    }
    agreement = report["agreement"]
    unmappable_ratio = unmappable / sum(resolved_codes.values()) if resolved_codes else 0.0
    context_ratio = context_insufficient / size if size else None
    report["calibration"] = {
        "assessment_coverage_met": all(
            assessment["complete"] for assessment in report["assessments"]
        ),
        "major_or_worse_agreement_met": (
            agreement.get("major_or_worse_agreement", 0) >= target["major_or_worse_agreement"]
            if agreement.get("major_or_worse_agreement") is not None
            else False
        ),
        "defect_presence_agreement_met": (
            agreement.get("defect_presence_agreement", 0)
            >= target["defect_presence_agreement"]
            if agreement.get("defect_presence_agreement") is not None
            else False
        ),
        "severity_weighted_kappa_met": (
            agreement.get("severity_weighted_kappa", 0) >= target["severity_weighted_kappa"]
            if agreement.get("severity_weighted_kappa") is not None
            else False
        ),
        "unmappable_ratio": unmappable_ratio,
        "unmappable_met": (
            unmappable_ratio is not None and unmappable_ratio < target["unmappable_max_ratio"]
        ),
        "context_insufficient_ratio": context_ratio,
        "context_insufficient_met": (
            context_ratio is not None
            and context_ratio < target["context_insufficient_max_ratio"]
        ),
    }
    return report




def build_report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 翻译质量试点报告",
        "",
        f"- sample_id：`{report.get('sample_id', '')}`",
        f"- 样本规模：{report.get('size', 0)}",
        "",
        "## 评估覆盖",
    ]
    for assessment in report.get("assessments", []):
        lines.append(
            f"- {assessment['evaluator_id']}（{assessment.get('kind')}）："
            f"{assessment['items']} 条 / findings {assessment['findings']}，"
            f"完整={'是' if assessment['complete'] else '否'}"
        )
    agreement = report.get("agreement", {})
    if "note" not in agreement:
        lines.extend(
            [
                "",
                "## 一致性",
                f"- context sufficient 一致率：{agreement.get('context_sufficient_agreement')}",
                f"- 实质缺陷有无一致率：{agreement.get('defect_presence_agreement')}",
                f"- major-or-worse 一致率：{agreement.get('major_or_worse_agreement')}",
                f"- severity 加权 κ：{agreement.get('severity_weighted_kappa')}",
                f"- error category macro-F1：{agreement.get('macro_f1')}",
            ]
        )
    distributions = report.get("distributions", {})
    if distributions:
        lines.extend(
            [
                "",
                "## 裁决后分布",
                f"- 错误按代码：{distributions.get('adjudicated_findings', {}).get('by_code')}",
                f"- 错误按严重程度：{distributions.get('adjudicated_findings', {}).get('by_severity')}",
                f"- 等级：{distributions.get('grades')}",
                f"- 置信度：{distributions.get('confidence')}",
                f"- 复用范围：{distributions.get('reuse_scopes')}",
            ]
        )
    risk = report.get("risk_flags", {})
    if risk:
        lines.extend(
            [
                "",
                "## 风险标志命中",
                f"- confirmed 条目数：{risk.get('confirmed_items')}，"
                f"其中至少一个 flag 命中：{risk.get('confirmed_with_any_flag')}",
                f"- flag 覆盖率：{risk.get('coverage')}",
            ]
        )
    calibration = report.get("calibration", {})
    if calibration:
        lines.extend(
            [
                "",
                "## 校准目标",
                f"- assessment 覆盖 100%：{'达成' if calibration.get('assessment_coverage_met') else '未达成'}",
                f"- major-or-worse ≥90%：{'达成' if calibration.get('major_or_worse_agreement_met') else '未达成'}",
                f"- 实质缺陷 ≥80%：{'达成' if calibration.get('defect_presence_agreement_met') else '未达成'}",
                f"- severity κ ≥0.70：{'达成' if calibration.get('severity_weighted_kappa_met') else '未达成'}",
                f"- 上下文不足 <10%：{'达成' if calibration.get('context_insufficient_met') else '未达成'}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def _validate_report_input(
    manifest: Manifest,
    validation_path: Path,
    validation: dict[str, Any],
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
) -> None:
    """Reject failed, incomplete, or stale validation artifacts."""
    if (
        type(validation.get("schema_version")) is not int
        or validation.get("schema_version") != 1
    ):
        raise ValidationError(
            f"unsupported quality validation schema: {validation_path}"
        )
    if validation.get("quality_contract") != VALIDATION_CONTRACT:
        raise ValidationError(
            f"unsupported quality validation file: {validation_path}"
        )

    validation_errors = validation.get("errors")
    if not isinstance(validation_errors, list) or not all(
        isinstance(error, str) for error in validation_errors
    ):
        raise ValidationError("quality validation errors are invalid")
    ok = validation.get("ok")
    if type(ok) is not bool:
        raise ValidationError("quality validation ok flag is invalid")
    if not ok or validation_errors:
        detail = "; ".join(validation_errors[:5])
        suffix = f": {detail}" if detail else ""
        raise ValidationError(
            f"quality validation did not succeed: {validation_path}{suffix}"
        )

    tool_version = validation.get("tool_version")
    if tool_version != TOOL_VERSION:
        raise ValidationError(
            "quality validation tool_version does not match the current tool version"
        )
    if validation.get("version") != manifest.version:
        raise ValidationError(
            "quality validation version does not match the selected manifest"
        )
    warnings = validation.get("warnings")
    if not isinstance(warnings, list) or not all(
        isinstance(warning, str) for warning in warnings
    ):
        raise ValidationError("quality validation warnings are invalid")
    if type(validation.get("dry_run")) is not bool:
        raise ValidationError("quality validation dry_run flag is invalid")
    if type(validation.get("strict")) is not bool:
        raise ValidationError("quality validation strict flag is invalid")

    expected_digests = {
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
    }
    for field, expected in expected_digests.items():
        if validation.get(field) != expected:
            raise ValidationError(
                f"quality validation {field} is stale or invalid"
            )

    sample_id = validation.get("sample_id")
    if not isinstance(sample_id, str) or SHA256_RE.fullmatch(sample_id) is None:
        raise ValidationError("quality validation sample_id is invalid")
    sample = validation.get("sample")
    if not isinstance(sample, dict):
        raise ValidationError("quality validation sample is invalid")
    if sample.get("sample_id") != sample_id:
        raise ValidationError(
            "quality validation sample_id does not match its sample"
        )
    sample_contract = sample.get("quality_contract")
    allowed_sample_contracts = (
        (SAMPLE_CONTRACT, DRY_RUN_CONTRACT)
        if validation["dry_run"]
        else (SAMPLE_CONTRACT,)
    )
    if sample_contract not in allowed_sample_contracts:
        raise ValidationError(
            "quality validation has an unsupported sample contract"
        )
    sample_schema = sample.get("schema_version")
    if type(sample_schema) is not int or sample_schema != 1:
        raise ValidationError("quality validation sample schema is invalid")
    items = sample.get("items")
    if not isinstance(items, list) or not items or not all(
        isinstance(item, dict) for item in items
    ):
        raise ValidationError("quality validation sample items are invalid or empty")
    sample_errors = _validate_sample_identity(
        sample,
        manifest,
        taxonomy,
        qpolicy,
        label="quality validation sample",
    )
    if sample_errors:
        raise ValidationError("; ".join(sample_errors))

    assessments = validation.get("assessments")
    if (
        not isinstance(assessments, list)
        or not 1 <= len(assessments) <= 2
        or not all(isinstance(assessment, dict) for assessment in assessments)
    ):
        raise ValidationError("quality validation assessments are invalid or empty")

    expected_evaluator_ids = set(qpolicy["pilot"]["evaluator_ids"])
    if not validation["dry_run"] and len(assessments) != len(
        expected_evaluator_ids
    ):
        raise ValidationError(
            "official quality validation must contain exactly two assessments"
        )

    actual_evaluator_ids: set[str] = set()
    for index, assessment in enumerate(assessments):
        where = f"quality validation assessments[{index}]"
        normalized_evaluator_id = assessment.get("evaluator_id")
        if not isinstance(normalized_evaluator_id, str):
            raise ValidationError(f"{where}.evaluator_id is invalid")
        evaluator = assessment.get("evaluator")
        if not isinstance(evaluator, dict):
            raise ValidationError(f"{where}.evaluator is invalid")
        evaluator_id = evaluator.get("id")
        if not isinstance(evaluator_id, str):
            raise ValidationError(f"{where}.evaluator.id is invalid")
        if normalized_evaluator_id != evaluator_id:
            raise ValidationError(
                f"{where}.evaluator_id does not match {where}.evaluator.id"
            )

        identity_errors: list[str] = []
        _check_evaluator_policy_identity(
            evaluator,
            qpolicy,
            identity_errors,
            f"{where}.evaluator",
        )
        if identity_errors:
            raise ValidationError(identity_errors[0])
        if evaluator_id in actual_evaluator_ids:
            raise ValidationError(
                f"{where}.evaluator.id duplicates another assessment"
            )
        actual_evaluator_ids.add(evaluator_id)

    if (
        not validation["dry_run"]
        and actual_evaluator_ids != expected_evaluator_ids
    ):
        raise ValidationError(
            "official quality validation assessment evaluator ids must exactly "
            "match quality policy.pilot.evaluator_ids"
        )
    adjudication = validation.get("adjudication")
    if not isinstance(adjudication, dict) or not isinstance(
        adjudication.get("items"), list
    ):
        raise ValidationError("quality validation adjudication is invalid")
    adjudication_items = adjudication["items"]
    if not validation["dry_run"] and not adjudication_items:
        raise ValidationError("quality validation adjudication is empty")
    if adjudication_items:
        adjudication_envelope = {
            "schema_version": 1,
            "quality_contract": ADJUDICATION_CONTRACT,
            "sample_id": sample_id,
            "items": adjudication_items,
        }
        try:
            _, adjudication_errors = _validate_adjudication(
                adjudication_envelope,
                sample,
                assessments,
                taxonomy,
                qpolicy,
                validation["strict"],
            )
        except ValidationError as error:
            raise ValidationError(
                f"quality validation adjudication is invalid: {error}"
            ) from error
        except (
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            raise ValidationError(
                "quality validation adjudication references invalid "
                "assessment data"
            ) from error
        if adjudication_errors:
            raise ValidationError(
                "quality validation adjudication is invalid: "
                + "; ".join(adjudication_errors)
            )


def run_report(manifest: Manifest, validation_path: Path) -> dict[str, Any]:
    validation = _read_json(validation_path, "quality validation")
    taxonomy = load_taxonomy(manifest)
    qpolicy = load_quality_policy(manifest)
    _validate_report_input(
        manifest,
        validation_path,
        validation,
        taxonomy,
        qpolicy,
    )
    try:
        report = build_report(validation, taxonomy)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as error:
        raise ValidationError(
            f"quality validation structure is invalid: {validation_path}"
        ) from error
    run_directory = create_quality_run_directory(manifest.root, "report")
    write_json(run_directory / "report.json", report)
    markdown = build_report_markdown(report)
    (run_directory / "report.md").write_text(markdown, encoding="utf-8")
    report["report_path"] = os_path_relative(run_directory / "report.json", manifest)
    report["report_md"] = os_path_relative(run_directory / "report.md", manifest)
    report["run_directory"] = os_path_relative(run_directory, manifest)
    return report
