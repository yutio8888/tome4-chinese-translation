"""Incremental invalidation (contract/0.1-rc3 §8).

Dependency graph (§8.1), three domains (§8.2), the pure
source_git_path_to_section() mapping (§8.3) and the incremental algorithm
with whole-set canonical self-check (§8.4, constraints I1/I2).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .config import ComponentSpec
from .errors import ValidationError
from .fingerprint import FindingRecord, canonical_findings_form


@dataclass(frozen=True)
class _MountMap:
    component: ComponentSpec
    git_path: str
    mount: str

    def section_to_source(self, section: str) -> str | None:
        prefix = self.mount + "/"
        if not section.startswith(prefix):
            return None
        return self.git_path + "/" + section[len(prefix) :]

    def source_to_section(self, source: str) -> str | None:
        prefix = self.git_path + "/"
        if not source.startswith(prefix):
            return None
        return self.mount + "/" + source[len(prefix) :]


def _mount_maps(component: ComponentSpec) -> list[_MountMap]:
    return [
        _MountMap(component=component, git_path=source.git_path, mount=source.mount)
        for source in component.sources
    ]


def source_git_path_to_section(
    component: ComponentSpec, changed_git_path: str
) -> str | None:
    """§8.3: map an engine-repo Git path to a snapshot section.

    Only the manifest sources[].git_path / mount pairs are authoritative.
    Returns None when the path does not belong to the component.
    """
    normalized = PurePosixPath(changed_git_path).as_posix()
    for mapping in _mount_maps(component):
        section = mapping.source_to_section(normalized)
        if section is not None:
            return section
    return None


def section_to_source_git_path(
    component: ComponentSpec, section: str
) -> str | None:
    """Inverse mapping used by the §8.3 round-trip parity test."""
    for mapping in _mount_maps(component):
        source = mapping.section_to_source(section)
        if source is not None:
            return source
    return None


def parity_check(component: ComponentSpec, sections: Iterable[str]) -> list[str]:
    """§8.3 parity test: every real snapshot section must round-trip.

    Returns the list of sections that fail the round-trip. Note: the official
    extractor only emits sections for files that captured entries, so the
    inverse direction (all Lua files == all sections) must never be asserted.
    """
    failures: list[str] = []
    for section in sections:
        source = section_to_source_git_path(component, section)
        if source is None:
            failures.append(f"no inverse mapping: {section}")
            continue
        round_trip = source_git_path_to_section(component, source)
        if round_trip != section:
            failures.append(f"round-trip mismatch: {section} -> {source} -> {round_trip}")
    return failures


# --------------------------------------------------------------------------
# Affected-set computation per domain


@dataclass(frozen=True)
class AffectedSet:
    domain: str
    sections: frozenset[str] = frozenset()
    tu_uids: frozenset[str] = frozenset()
    rule_ids: frozenset[str] = frozenset()

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "sections": sorted(self.sections),
            "tu_uids": sorted(self.tu_uids),
            "rule_ids": sorted(self.rule_ids),
        }


def affected_for_source_domain(
    component: ComponentSpec, changed_git_paths: Iterable[str]
) -> AffectedSet:
    """Map changed Lua paths to sections of one component.

    Paths outside every mount of this component are ignored (they belong to
    other components); the caller verifies aggregate coverage across all
    components of the range.
    """
    sections: set[str] = set()
    for path in changed_git_paths:
        normalized = PurePosixPath(path).as_posix()
        if not normalized.endswith(".lua"):
            continue
        section = source_git_path_to_section(component, normalized)
        if section is not None:
            sections.add(section)
    return AffectedSet(domain="source", sections=frozenset(sections))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot hash file: {path}") from error


# --------------------------------------------------------------------------
# Incremental algorithm (§8.4)


def incremental_findings(
    *,
    previous: Iterable[FindingRecord],
    affected_tu_uids: frozenset[str],
    recomputed: Iterable[FindingRecord],
) -> tuple[FindingRecord, ...]:
    """F_new = (F_previous - findings(affected)) + recompute(affected)."""
    kept = tuple(
        record for record in previous if record.tu_uid not in affected_tu_uids
    )
    return tuple(sorted([*kept, *recomputed], key=lambda r: r.fingerprint))


def self_check(
    *,
    incremental: Iterable[FindingRecord],
    full: Iterable[FindingRecord],
    artifact_directory: Path | None = None,
) -> bool:
    """§8.4: canonical(F_new) == canonical(F_full), whole-set comparison."""
    incremental_form = canonical_findings_form(incremental)
    full_form = canonical_findings_form(full)
    if incremental_form == full_form:
        return True
    if artifact_directory is not None:
        artifact_directory.mkdir(parents=True, exist_ok=True)
        from .report import atomic_write_bytes

        atomic_write_bytes(artifact_directory / "incremental-canonical.jsonl", incremental_form)
        atomic_write_bytes(artifact_directory / "full-canonical.jsonl", full_form)
    return False
