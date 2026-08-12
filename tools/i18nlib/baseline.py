"""Frozen baseline snapshots and CI gate (contract/0.1-rc3 §7)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .errors import ValidationError
from .fingerprint import FindingRecord
from .report import atomic_write_bytes, write_json


BASELINE_DIRECTORY_NAME = "baselines"


@dataclass(frozen=True)
class BaselineEntry:
    fingerprint: str
    rule_id: str
    tu_uid: str
    severity: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "fingerprint": self.fingerprint,
            "rule_id": self.rule_id,
            "tu_uid": self.tu_uid,
            "severity": self.severity,
            "status": self.status,
        }


@dataclass(frozen=True)
class Baseline:
    path: Path
    translation_commit: str
    meta: dict[str, Any]
    entries: dict[str, BaselineEntry]
    sha256: str

    @property
    def fingerprints(self) -> frozenset[str]:
        return frozenset(self.entries)


def baseline_directory(manifest_root: Path) -> Path:
    return manifest_root / "i18n" / BASELINE_DIRECTORY_NAME


def baseline_paths(
    manifest_root: Path, *, component: str, translation_commit: str
) -> tuple[Path, Path]:
    directory = baseline_directory(manifest_root)
    base = directory / f"{component}-{translation_commit}"
    return base.with_suffix(".jsonl"), base.with_suffix(".meta.json")


def write_baseline(
    *,
    manifest_root: Path,
    component: str,
    translation_commit: str,
    source_snapshot_sha256: str,
    engine_commit: str,
    extractor_commit: str,
    rules_registry_sha256: str,
    slot_registry_sha256: str,
    records: Iterable[FindingRecord],
) -> Baseline:
    entries = [
        BaselineEntry(
            fingerprint=record.fingerprint,
            rule_id=record.rule_id,
            tu_uid=record.tu_uid,
            severity=record.issue.severity,
            status="legacy_unreviewed",
        )
        for record in records
    ]
    entries.sort(key=lambda entry: entry.fingerprint)
    seen: set[str] = set()
    for entry in entries:
        if entry.fingerprint in seen:
            raise ValidationError(
                f"duplicate fingerprint while freezing baseline: {entry.fingerprint}"
            )
        seen.add(entry.fingerprint)
    jsonl_path, meta_path = baseline_paths(
        manifest_root, component=component, translation_commit=translation_commit
    )
    jsonl_bytes = b"".join(
        (
            json.dumps(entry.to_dict(), ensure_ascii=False, sort_keys=True) + "\n"
        ).encode("utf-8")
        for entry in entries
    )
    # §7.1 frozen meta format: no additional keys (the jsonl digest is
    # recomputed on read, never stored in the frozen meta).
    meta = {
        "schema_version": 1,
        "component": component,
        "translation_commit": translation_commit,
        "source_snapshot_sha256": source_snapshot_sha256,
        "engine_commit": engine_commit,
        "extractor_commit": extractor_commit,
        "rules_registry_sha256": rules_registry_sha256,
        "slot_registry_sha256": slot_registry_sha256,
    }
    atomic_write_bytes(jsonl_path, jsonl_bytes)
    write_json(meta_path, meta)
    return read_baseline(
        manifest_root, component=component, translation_commit=translation_commit
    )


def read_baseline(
    manifest_root: Path, *, component: str, translation_commit: str
) -> Baseline:
    jsonl_path, meta_path = baseline_paths(
        manifest_root, component=component, translation_commit=translation_commit
    )
    try:
        meta_raw = json.loads(meta_path.read_bytes())
    except OSError as error:
        raise ValidationError(
            f"cannot read baseline meta for {component}@{translation_commit}: {error}"
        ) from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid baseline meta JSON: {meta_path}") from error
    if not isinstance(meta_raw, dict):
        raise ValidationError(f"baseline meta is not an object: {meta_path}")
    try:
        jsonl_bytes = jsonl_path.read_bytes()
        entries_text = jsonl_bytes.decode("utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read baseline snapshot: {jsonl_path}") from error
    except UnicodeDecodeError as error:
        raise ValidationError(f"baseline snapshot is not UTF-8: {jsonl_path}") from error
    entries: dict[str, BaselineEntry] = {}
    for line_number, line in enumerate(entries_text.splitlines(), start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid baseline JSON at {jsonl_path}:{line_number}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(
                f"baseline record {line_number} is not an object"
            )
        if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
            raise ValidationError(
                f"baseline record {line_number} has an unsupported schema_version"
            )
        try:
            entry = BaselineEntry(
                fingerprint=record["fingerprint"],
                rule_id=record["rule_id"],
                tu_uid=record["tu_uid"],
                severity=record["severity"],
                status=record["status"],
            )
        except KeyError as error:
            raise ValidationError(
                f"baseline record {line_number} is missing {error}"
            ) from error
        if entry.fingerprint in entries:
            raise ValidationError(
                f"duplicate fingerprint in baseline: {entry.fingerprint}"
            )
        entries[entry.fingerprint] = entry
    return Baseline(
        path=jsonl_path,
        translation_commit=translation_commit,
        meta=meta_raw,
        entries=entries,
        sha256=hashlib.sha256(jsonl_bytes).hexdigest(),
    )


def validate_baseline_environment(
    baseline: Baseline,
    *,
    source_snapshot_sha256: str,
    engine_commit: str,
    extractor_commit: str,
    rules_registry_sha256: str,
    slot_registry_sha256: str,
) -> None:
    """A baseline whose generation environment cannot be rebuilt is invalid (§7.1)."""
    expected = {
        "source_snapshot_sha256": source_snapshot_sha256,
        "engine_commit": engine_commit,
        "extractor_commit": extractor_commit,
        "rules_registry_sha256": rules_registry_sha256,
        "slot_registry_sha256": slot_registry_sha256,
    }
    mismatches = {
        key: (baseline.meta.get(key), value)
        for key, value in expected.items()
        if baseline.meta.get(key) != value
    }
    if mismatches:
        raise ValidationError(
            f"baseline {baseline.path} was generated in an unreproducible "
            f"environment; refusing CI judgement: {mismatches!r}"
        )


@dataclass(frozen=True)
class BaselineState:
    new: tuple[FindingRecord, ...]
    legacy: tuple[FindingRecord, ...]
    resolved: tuple[BaselineEntry, ...]
    legacy_on_touched_tu: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "new": [record.to_dict() for record in self.new],
            "legacy": [record.to_dict() for record in self.legacy],
            "resolved": [entry.to_dict() for entry in self.resolved],
            "legacy_on_touched_tu": list(self.legacy_on_touched_tu),
        }


def compute_baseline_state(
    baseline: Baseline,
    current: Iterable[FindingRecord],
    *,
    touched_tu_uids: frozenset[str] = frozenset(),
) -> BaselineState:
    """§7.2: new/resolved are computed per run, never written to the baseline."""
    current_by_fingerprint = {record.fingerprint: record for record in current}
    new_records = [
        record
        for fingerprint, record in sorted(current_by_fingerprint.items())
        if fingerprint not in baseline.entries
    ]
    legacy_records = [
        current_by_fingerprint[fingerprint]
        for fingerprint, entry in sorted(baseline.entries.items())
        if fingerprint in current_by_fingerprint
    ]
    resolved_entries = [
        entry
        for fingerprint, entry in sorted(baseline.entries.items())
        if fingerprint not in current_by_fingerprint
    ]
    # §7.3 B1 advisory: legacy finding on a TU whose text was touched.
    legacy_on_touched = sorted(
        fingerprint
        for fingerprint, record in current_by_fingerprint.items()
        if fingerprint in baseline.entries and record.tu_uid in touched_tu_uids
    )
    return BaselineState(
        new=tuple(new_records),
        legacy=tuple(legacy_records),
        resolved=tuple(resolved_entries),
        legacy_on_touched_tu=tuple(legacy_on_touched),
    )


def ci_gate(state: BaselineState) -> tuple[bool, dict[str, int]]:
    """§7.4: new ERROR fails; new WARNING reports; legacy stays technical debt."""
    new_errors = sum(1 for record in state.new if record.issue.severity == "error")
    new_warnings = sum(1 for record in state.new if record.issue.severity != "error")
    legacy_errors = sum(1 for record in state.legacy if record.issue.severity == "error")
    legacy_warnings = sum(
        1 for record in state.legacy if record.issue.severity != "error"
    )
    return new_errors == 0, {
        "new_errors": new_errors,
        "new_warnings": new_warnings,
        "legacy_errors": legacy_errors,
        "legacy_warnings": legacy_warnings,
        "resolved": len(state.resolved),
    }
