"""FindingRecord assembly: bind lint Issues to TU identities (contract §6.3)."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .errors import ConfigurationError
from .fingerprint import (
    FindingRecord,
    RuleRegistry,
    build_evidence_key,
    finding_fingerprint,
)
from .identity import ComponentIndex, tu_uid_fallback
from .lint import Issue, stable_entry_id


def _collision_id(component: str, source: str, source_tag: str | None) -> str:
    tag_value = "<nil>" if source_tag is None else f"<string>{source_tag}"
    return hashlib.sha256(
        "\0".join((component, source, tag_value)).encode("utf-8")
    ).hexdigest()


def _editorial_id(entry: dict[str, Any], component: str) -> str:
    section = entry.get("section")
    source = entry.get("source")
    source_tag = entry.get("source_tag")
    if not isinstance(section, str):
        section = ""
    if not isinstance(source, str):
        raise ConfigurationError("translation entry has a non-string source")
    if source_tag is not None and not isinstance(source_tag, str):
        raise ConfigurationError("translation entry has a non-string source_tag")
    return stable_entry_id(component, section, source, source_tag)


@dataclass(frozen=True)
class FindingContext:
    """Per-component translation entries and identity index for binding."""

    component: str
    entries: tuple[dict[str, Any], ...]
    index: ComponentIndex | None

    @property
    def entry_by_editorial(self) -> dict[str, list[dict[str, Any]]]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for entry in self.entries:
            groups[_editorial_id(entry, self.component)].append(entry)
        return dict(groups)

    @property
    def runtime_groups(self) -> dict[str, list[dict[str, Any]]]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for entry in self.entries:
            source = entry.get("source")
            source_tag = entry.get("source_tag")
            if not isinstance(source, str):
                continue
            groups[_collision_id(self.component, source, source_tag)].append(entry)
        return dict(groups)


def _bind(
    editorial_id: str, contexts: dict[str, FindingContext]
) -> tuple[str, ...]:
    candidates: set[str] = set()
    for context in contexts.values():
        if context.index is None:
            continue
        found = context.index.editorial_to_tu.get(editorial_id)
        if found:
            candidates.update(found)
    if candidates:
        return tuple(sorted(candidates))
    return (tu_uid_fallback(editorial_id),)


def build_finding_records(
    *,
    registry: RuleRegistry,
    issues: Iterable[Issue],
    contexts: dict[str, FindingContext],
    conflicts: Iterable[Any],
) -> tuple[list[FindingRecord], dict[str, Any]]:
    """Wrap lint Issues into FindingRecords with TU bindings.

    Issues whose code is not registered produce no fingerprint Finding
    (fail closed per §9.1) but remain visible in the regular lint report.
    """
    entry_lookup: dict[str, list[dict[str, Any]]] = defaultdict(list)
    runtime_lookup: dict[str, list[dict[str, Any]]] = defaultdict(list)
    collision_meta: dict[str, tuple[str, str, str | None]] = {}
    for context in contexts.values():
        for entry in context.entries:
            entry_lookup[_editorial_id(entry, context.component)].append(entry)
        for collision_id_value, entries in context.runtime_groups.items():
            runtime_lookup[collision_id_value].extend(entries)
            first = entries[0]
            collision_meta[collision_id_value] = (
                context.component,
                first.get("source", ""),
                first.get("source_tag"),
            )

    records: list[FindingRecord] = []
    skipped: dict[str, int] = defaultdict(int)
    for issue in issues:
        rule = registry.rules.get(issue.code)
        if rule is None:
            skipped[issue.code] += 1
            continue
        if rule.subject_kind == "translation_unit":
            if issue.entry_id is None:
                skipped[issue.code] += 1
                continue
            subject = _bind(issue.entry_id, contexts)[0]
            participants = (subject,)
            evidence: str
            if rule.evidence_key_spec == "runtime-key":
                entries = runtime_lookup.get(issue.entry_id, [])
                participants = tuple(
                    sorted(
                        {
                            tu_uid
                            for entry in entries
                            for tu_uid in _bind(
                                _editorial_id(
                                    entry,
                                    collision_meta.get(issue.entry_id, ("", "", None))[0],
                                ),
                                contexts,
                            )
                        }
                    )
                ) or (subject,)
                component_name, source, source_tag = collision_meta.get(
                    issue.entry_id, ("", "", None)
                )
                evidence = build_evidence_key(
                    "runtime-key",
                    entry={"source": source, "source_tag": source_tag},
                    component=component_name,
                )
            elif rule.evidence_key_spec == "constant":
                evidence = build_evidence_key("constant")
            else:
                entries = entry_lookup.get(issue.entry_id, [])
                if not entries:
                    # Unbindable issue without entry material: fail closed
                    # instead of fabricating an evidence key.
                    skipped[issue.code] += 1
                    continue
                evidence = build_evidence_key(
                    rule.evidence_key_spec, entry=entries[0]
                )
            records.append(
                FindingRecord(
                    issue=issue,
                    rule_id=rule.rule_id,
                    rule_schema_version=rule.schema_version,
                    tu_uid=subject,
                    participants=participants,
                    evidence_key=evidence,
                    fingerprint=finding_fingerprint(
                        rule_id=rule.rule_id,
                        rule_schema_version=rule.schema_version,
                        subject_tu_uid=subject,
                        participants=participants,
                        evidence_key=evidence,
                    ),
                )
            )
        else:
            # Entity-level rules: only the duplicate-id prechecks exist in
            # Pilot A; they are produced from IdentityConflict via the
            # conflicts parameter, never from lint Issues.
            skipped[issue.code] += 1
            continue

    for conflict in conflicts:
        code = getattr(conflict, "code", None)
        if code not in ("duplicate-talent-id", "duplicate-effect-id"):
            continue
        rule = registry.rules.get(code)
        if rule is None:
            skipped[code] += 1
            continue
        component_name = getattr(conflict, "component", "")
        anchor_key = getattr(conflict, "anchor_key", "")
        context = contexts.get(component_name)
        participants: tuple[str, ...] = ()
        if context is not None and context.index is not None:
            participants = tuple(
                sorted(
                    {
                        tu.tu_uid
                        for tu in context.index.tus.values()
                        if tu.anchor_key == anchor_key and tu.anchor_type is not None
                    }
                )
            )
        if not participants:
            participants = (
                tu_uid_fallback(
                    stable_entry_id(component_name, "", anchor_key, None)
                ),
            )
        subject = participants[0]
        evidence = build_evidence_key("anchor-key", anchor_key=anchor_key)
        sites = getattr(conflict, "sites", ())
        first_site = sites[0] if sites else ("", 0)
        issue = Issue(
            severity="error",
            code=code,
            message=(
                f"duplicate {code} anchor {anchor_key!r} at "
                f"{len(sites)} definition sites: "
                + ", ".join(f"{section}:{line}" for section, line in sites[:5])
            ),
            logical_path=first_site[0] or component_name,
            line=first_site[1] or None,
            entry_id=participants[0],
        )
        records.append(
            FindingRecord(
                issue=issue,
                rule_id=rule.rule_id,
                rule_schema_version=rule.schema_version,
                tu_uid=subject,
                participants=participants,
                evidence_key=evidence,
                fingerprint=finding_fingerprint(
                    rule_id=rule.rule_id,
                    rule_schema_version=rule.schema_version,
                    subject_tu_uid=subject,
                    participants=participants,
                    evidence_key=evidence,
                ),
            )
        )

    records.sort(
        key=lambda record: (
            record.fingerprint,
            record.rule_id,
            record.tu_uid,
            record.issue.severity,
            record.issue.code,
        )
    )
    return records, {"unregistered_issues": dict(skipped)}
