"""Shared quality artifact contracts: canonical bytes, validation, provenance.

This module is the public contract core extracted for the offline closure
round.  Legacy modules (quality_v2, quality_v3, facts_study) keep their
original export names and re-export these implementations so historical
contracts and artifacts stay byte-identical.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from .errors import ValidationError


# ---------------------------------------------------------------------------
# Canonical JSON bytes and hashes
# ---------------------------------------------------------------------------


def canonical_json_bytes(value: Any) -> bytes:
    """Deterministic UTF-8 JSON bytes: sorted keys, compact separators."""
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def bytes_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise ValidationError(f"cannot read quality artifact input: {path}") from error


# ---------------------------------------------------------------------------
# Strict validation helpers
# ---------------------------------------------------------------------------

_SHA256_RE = re.compile(r"\A[0-9a-f]{64}\Z")


def exact_fields(value: dict[str, Any], expected: Iterable[str], where: str) -> None:
    expected_set = set(expected)
    unknown = sorted(set(value) - expected_set)
    missing = sorted(expected_set - set(value))
    if unknown:
        raise ValidationError(f"{where} has unknown fields: {', '.join(unknown)}")
    if missing:
        raise ValidationError(f"{where} is missing fields: {', '.join(missing)}")


def string(value: Any, where: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        raise ValidationError(
            f"{where} must be a {'string' if empty else 'non-empty string'}"
        )
    return value


def enum(value: Any, allowed: Iterable[str], where: str) -> str:
    allowed_set = set(allowed)
    if not isinstance(value, str) or value not in allowed_set:
        raise ValidationError(
            f"{where} must be one of: {', '.join(sorted(allowed_set))}"
        )
    return value


def sha256(value: Any, where: str) -> str:
    text = string(value, where)
    if _SHA256_RE.fullmatch(text) is None:
        raise ValidationError(f"{where} must be a lowercase SHA-256")
    return text


def boolean(value: Any, where: str) -> bool:
    if value is not True and value is not False:
        raise ValidationError(f"{where} must be boolean")
    return value


def integer(value: Any, where: str) -> int:
    if type(value) is not int:
        raise ValidationError(f"{where} must be an exact integer")
    return value


def relative_path(value: Any, where: str) -> str:
    """Repository-relative logical path: no absolute path, no '..', no ':line'."""
    text = string(value, where)
    path = Path(text)
    if path.is_absolute() or ".." in path.parts or ":" in text:
        raise ValidationError(f"{where} must be a repository-relative logical path")
    return text


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


# ---------------------------------------------------------------------------
# Structured provenance (offline-closure contract)
# ---------------------------------------------------------------------------

PROVENANCE_KINDS = frozenset(("terminology", "public-source", "versioned-context"))

LOCATOR_TYPES = frozenset(("line-range", "term-row", "context-key"))


def validate_locator(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    locator_type = enum(value.get("type"), LOCATOR_TYPES, f"{where}.type")
    if locator_type == "line-range":
        exact_fields(value, ("type", "start_line", "end_line"), where)
        start = integer(value["start_line"], f"{where}.start_line")
        end = integer(value["end_line"], f"{where}.end_line")
        if start < 1 or end < start:
            raise ValidationError(f"{where} must be a legal line range")
    elif locator_type == "term-row":
        exact_fields(value, ("type", "row"), where)
        row = integer(value["row"], f"{where}.row")
        if row < 1:
            raise ValidationError(f"{where}.row must be a positive 1-based row")
    elif locator_type == "context-key":
        exact_fields(value, ("type", "key", "value"), where)
        string(value["key"], f"{where}.key", empty=True)
        string(value["value"], f"{where}.value", empty=True)
    return value


def validate_resource(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(
        value, ("repository", "revision", "logical_path", "file_sha256"), where
    )
    string(value["repository"], f"{where}.repository")
    string(value["revision"], f"{where}.revision")
    relative_path(value["logical_path"], f"{where}.logical_path")
    if ":" in value["logical_path"]:
        raise ValidationError(f"{where}.logical_path must not embed a :line locator")
    sha256(value["file_sha256"], f"{where}.file_sha256")
    return value


def validate_provenance(value: Any, where: str) -> dict[str, Any]:
    """Structured provenance: kind + resource + locator.

    The file identity is carried by ``resource.file_sha256``; locators never
    embed ``:line`` inside ``logical_path``.
    """
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(value, ("kind", "resource", "locator"), where)
    kind = enum(value["kind"], PROVENANCE_KINDS, f"{where}.kind")
    resource = validate_resource(value["resource"], f"{where}.resource")
    locator = validate_locator(value["locator"], f"{where}.locator")
    if kind == "terminology":
        if resource["repository"] != "terminology" or resource["logical_path"] not in (
            "terminology.tsv",
            "terminology",
            "terminology/",
        ):
            raise ValidationError(
                f"{where} terminology provenance must point at terminology.tsv "
                "or the terminology/ store"
            )
        if locator["type"] not in ("term-row", "context-key"):
            raise ValidationError(
                f"{where} terminology provenance requires a term-row or context-key locator"
            )
    if kind == "public-source":
        if locator["type"] not in ("line-range", "context-key"):
            raise ValidationError(
                f"{where} public-source provenance requires a line-range or context-key locator"
            )
    if kind == "versioned-context" and locator["type"] != "context-key":
        raise ValidationError(
            f"{where} versioned-context provenance requires a context-key locator"
        )
    return {"kind": kind, "resource": resource, "locator": locator}


def make_provenance(
    *,
    kind: str,
    repository: str,
    revision: str,
    logical_path: str,
    file_sha256: str,
    locator: dict[str, Any],
) -> dict[str, Any]:
    provenance = {
        "kind": kind,
        "resource": {
            "repository": repository,
            "revision": revision,
            "logical_path": logical_path,
            "file_sha256": file_sha256,
        },
        "locator": locator,
    }
    validate_provenance(provenance, "provenance")
    return provenance


# ---------------------------------------------------------------------------
# Subject identity
# ---------------------------------------------------------------------------

SUBJECT_KINDS = frozenset(("canonical-revision", "controlled-mutation"))


def subject_identity(*, kind: str, revision_id: str, variant_target: str | None = None, mutation_kind: str | None = None, digest: str | None = None) -> dict[str, Any]:
    """Exact subject identity for claims and anchors.

    ``canonical-revision`` binds the canonical revision ID; a
    ``controlled-mutation`` additionally binds the variant target, mutation
    kind and the digest of the mutation identity contract.  Controlled
    mutations never masquerade as canonical revisions.
    """
    kind = enum(kind, SUBJECT_KINDS, "subject identity kind")
    sha256(revision_id, "subject identity revision_id")
    if kind == "canonical-revision":
        if variant_target is not None or mutation_kind is not None or digest is not None:
            raise ValidationError("canonical-revision subject carries no mutation fields")
        return {"kind": kind, "revision_id": revision_id}
    if variant_target is None or mutation_kind is None:
        raise ValidationError("controlled-mutation subject requires variant_target and mutation_kind")
    if digest is None:
        raise ValidationError("controlled-mutation subject requires a mutation digest")
    return {
        "kind": kind, "revision_id": revision_id,
        "variant_target": variant_target, "mutation_kind": mutation_kind,
        "digest": sha256(digest, "subject identity digest"),
    }


def validate_subject(value: Any, where: str = "subject") -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    if value.get("kind") == "canonical-revision":
        exact_fields(value, ("kind", "revision_id"), where)
        return subject_identity(kind="canonical-revision", revision_id=value["revision_id"])
    exact_fields(
        value, ("kind", "revision_id", "variant_target", "mutation_kind", "digest"), where
    )
    return subject_identity(
        kind=value["kind"], revision_id=value["revision_id"],
        variant_target=value["variant_target"], mutation_kind=value["mutation_kind"],
        digest=value["digest"],
    )


class ArtifactRef:
    """A reproducible reference to a frozen artifact.

    Binds the subject identity (canonical revision or controlled mutation) to
    a structured provenance resource/locator pair.  The string form is the
    canonical JSON of the reference so it can be embedded in hashes.
    """

    __slots__ = ("subject", "provenance", "_canonical")

    def __init__(self, subject: dict[str, Any], provenance: dict[str, Any]):
        self.subject = validate_subject(subject)
        self.provenance = validate_provenance(provenance, "artifact provenance")
        self._canonical = canonical_json_bytes(
            {"subject": self.subject, "provenance": self.provenance}
        )

    def sha256(self) -> str:
        return hashlib.sha256(self._canonical).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {"subject": self.subject, "provenance": self.provenance}

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ArtifactRef) and self._canonical == other._canonical

    def __hash__(self) -> int:
        return hash(self._canonical)
