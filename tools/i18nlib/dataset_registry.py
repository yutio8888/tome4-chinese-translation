"""Versioned dataset registry for quality datasets.

The registry is authoritative version-controlled data.  Tools only read it
and emit ``registry-fragment`` artifacts; merging a fragment into the
versioned registry is an explicit main-agent step.  The registry covers every
frozen dataset lineage: the official 120, calibration/holdout 32+32, the
exploratory set, the failed Facts pilot, random/long-text/discarded Facts
candidates, and future curation sets.
"""

from __future__ import annotations

from typing import Any, Iterable

from .errors import ValidationError
from .quality_contracts import (
    canonical_sha256,
    exact_fields,
    enum,
    read_json_object,
    relative_path,
    sha256,
    string,
)


REGISTRY_CONTRACT = "tome4-quality-dataset-registry-v1"
FRAGMENT_CONTRACT = "tome4-quality-dataset-registry-fragment-v1"
REGISTRY_FILE = "i18n/quality/dataset-registry-v1.json"

EXCLUSION_SCOPES = ("calibration", "holdout", "facts-curation")
STATUSES = ("frozen", "deprecated")
PURPOSES = (
    "official-120-pilot-sample",
    "calibration-set",
    "holdout-set",
    "exploratory-set",
    "facts-study-candidate-set",
    "facts-study-failed-pilot",
    "facts-study-final-sample",
    "curation-pool",
    "other",
)


def validate_registry_entry(entry: Any, index: int) -> dict[str, Any]:
    where = f"registry.entries[{index}]"
    if not isinstance(entry, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(
        (
            "dataset_id", "purpose", "status", "sample_contract",
            "sample_id", "sample_sha256", "sample_reference",
            "revision_ids", "revision_ids_sha256",
            "excluded_from_calibration", "excluded_from_holdout",
            "excluded_from_facts_curation", "scope", "disposition",
        ),
        entry,
        where,
    )
    dataset_id = string(entry["dataset_id"], f"{where}.dataset_id")
    purpose = enum(entry["purpose"], PURPOSES, f"{where}.purpose")
    status = enum(entry["status"], STATUSES, f"{where}.status")
    sample_contract = string(entry["sample_contract"], f"{where}.sample_contract")
    sample_id = entry["sample_id"]
    sample_sha256 = entry["sample_sha256"]
    sample_reference = entry["sample_reference"]
    if sample_id is not None:
        sha256(sample_id, f"{where}.sample_id")
        sha256(sample_sha256, f"{where}.sample_sha256")
        if sample_reference is not None:
            raise ValidationError(f"{where} must not combine sample_id with sample_reference")
    else:
        if sample_sha256 is not None:
            raise ValidationError(f"{where}.sample_sha256 requires a sample_id")
        if not isinstance(sample_reference, dict):
            raise ValidationError(f"{where} requires a sample_reference when sample_id is null")
        exact_fields(
            sample_reference, ("logical_path", "file_sha256"), f"{where}.sample_reference"
        )
        relative_path(sample_reference["logical_path"], f"{where}.sample_reference.logical_path")
        sha256(sample_reference["file_sha256"], f"{where}.sample_reference.file_sha256")
    revision_ids = entry["revision_ids"]
    if not isinstance(revision_ids, list) or revision_ids != sorted(set(revision_ids)):
        raise ValidationError(f"{where}.revision_ids must be a sorted unique list")
    if not revision_ids:
        raise ValidationError(f"{where}.revision_ids must not be empty")
    for rid_index, revision_id in enumerate(revision_ids):
        sha256(revision_id, f"{where}.revision_ids[{rid_index}]")
    if canonical_sha256(revision_ids) != entry["revision_ids_sha256"]:
        raise ValidationError(f"{where} revision digest mismatch")
    for field in ("excluded_from_calibration", "excluded_from_holdout", "excluded_from_facts_curation"):
        if entry[field] is not True and entry[field] is not False:
            raise ValidationError(f"{where}.{field} must be boolean")
    scope = entry["scope"]
    if not isinstance(scope, dict):
        raise ValidationError(f"{where}.scope must be an object")
    exact_fields(scope, ("natural", "controlled"), f"{where}.scope")
    natural = scope["natural"]
    controlled = scope["controlled"]
    if type(natural) is not int or type(controlled) is not int or natural < 0 or controlled < 0 or natural + controlled == 0:
        raise ValidationError(f"{where}.scope must contain non-negative counts with a positive total")
    disposition = string(entry["disposition"], f"{where}.disposition")
    return {
        "dataset_id": dataset_id, "purpose": purpose, "status": status,
        "sample_contract": sample_contract, "sample_id": sample_id,
        "sample_sha256": sample_sha256, "sample_reference": sample_reference,
        "revision_ids": revision_ids,
        "revision_ids_sha256": entry["revision_ids_sha256"],
        "excluded_from_calibration": entry["excluded_from_calibration"],
        "excluded_from_holdout": entry["excluded_from_holdout"],
        "excluded_from_facts_curation": entry["excluded_from_facts_curation"],
        "scope": {"natural": natural, "controlled": controlled},
        "disposition": disposition,
    }


def validate_registry(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("registry root must be an object")
    exact_fields(
        value, ("contract", "schema_version", "entries", "registry_id"), "registry"
    )
    if value["contract"] != REGISTRY_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported dataset registry contract")
    entries = value["entries"]
    if not isinstance(entries, list) or not entries:
        raise ValidationError("registry must contain at least one entry")
    normalized = []
    dataset_ids: set[str] = set()
    sample_ids: set[str] = set()
    revision_ids: set[str] = set()
    for index, entry in enumerate(entries):
        normalized_entry = validate_registry_entry(entry, index)
        if normalized_entry["dataset_id"] in dataset_ids:
            raise ValidationError(f"duplicate registry dataset_id: {normalized_entry['dataset_id']}")
        dataset_ids.add(normalized_entry["dataset_id"])
        if normalized_entry["sample_id"] is not None:
            if normalized_entry["sample_id"] in sample_ids:
                raise ValidationError(
                    f"duplicate registry sample_id: {normalized_entry['sample_id']}"
                )
            sample_ids.add(normalized_entry["sample_id"])
        overlap = revision_ids & set(normalized_entry["revision_ids"])
        if overlap:
            raise ValidationError(
                f"registry revision sets overlap: {sorted(overlap)[:3]}"
            )
        revision_ids.update(normalized_entry["revision_ids"])
        normalized.append(normalized_entry)
    expected_id = canonical_sha256(
        {"contract": REGISTRY_CONTRACT, "schema_version": 1, "entries": normalized}
    )
    if value["registry_id"] != expected_id:
        raise ValidationError("registry_id is not canonical")
    return {"contract": REGISTRY_CONTRACT, "schema_version": 1, "entries": normalized, "registry_id": value["registry_id"]}


def load_registry(manifest: Any) -> dict[str, Any]:
    """Load and validate the versioned registry; never modifies it."""
    path = manifest.root / REGISTRY_FILE
    return validate_registry(read_json_object(path, "quality dataset registry"))


def registry_revision_ids(registry: dict[str, Any]) -> set[str]:
    return {
        revision_id
        for entry in registry["entries"]
        for revision_id in entry["revision_ids"]
    }


def excluded_revision_ids(
    registry: dict[str, Any], *, scopes: Iterable[str] = EXCLUSION_SCOPES
) -> set[str]:
    """Union of revision IDs excluded for the given scopes."""
    selected = set(scopes)
    unknown = selected - set(EXCLUSION_SCOPES)
    if unknown:
        raise ValidationError(f"unknown exclusion scope: {sorted(unknown)}")
    result: set[str] = set()
    for entry in registry["entries"]:
        for scope in ("calibration", "holdout", "facts-curation"):
            if scope in selected and entry[f"excluded_from_{scope.replace('-', '_')}"]:
                result.update(entry["revision_ids"])
    return result


def build_registry_fragment(entry: dict[str, Any]) -> dict[str, Any]:
    """Fragment for one newly frozen dataset; merged by the main agent."""
    normalized = validate_registry_entry(entry, 0)
    fragment = {
        "contract": FRAGMENT_CONTRACT, "schema_version": 1,
        "entry": normalized, "fragment_id": "",
    }
    fragment["fragment_id"] = canonical_sha256(
        {key: value for key, value in fragment.items() if key != "fragment_id"}
    )
    return fragment


def validate_registry_fragment(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("registry fragment root must be an object")
    exact_fields(value, ("contract", "schema_version", "entry", "fragment_id"), "registry fragment")
    if value["contract"] != FRAGMENT_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported registry fragment contract")
    entry = validate_registry_entry(value["entry"], 0)
    expected_id = canonical_sha256(
        {"contract": FRAGMENT_CONTRACT, "schema_version": 1, "entry": entry}
    )
    if value["fragment_id"] != expected_id:
        raise ValidationError("registry fragment_id is not canonical")
    return {**value, "entry": entry}
