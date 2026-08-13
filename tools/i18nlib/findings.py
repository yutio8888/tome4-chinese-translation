"""FindingRecord assembly: bind lint Issues to TU identities (contract §6.3)."""

from __future__ import annotations

import dataclasses
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
from .identity import ComponentIndex, UnloadedSources, tu_uid_fallback
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


_DUPLICATE_CODES = frozenset({"duplicate-talent-id", "duplicate-effect-id"})


def _filter_duplicate_conflicts(
    conflicts: Iterable[Any],
    unloaded_sources: UnloadedSources | None,
) -> tuple[list[Any], list[dict[str, Any]]]:
    """Narrow duplicate-id ERROR conflicts by the unloaded-sources registry.

    A site whose section is in the registry is a definition that is extracted
    but never loaded by the game, so it cannot collide at runtime (§4.4 BC2
    load semantics). All sites exempted -> no ERROR (listed as suppressed);
    partially exempted -> the remaining loaded sites decide, >= 2 sites keep
    the ERROR. Weak identity_conflict CONTEXT and every other code pass
    through untouched; the raw conflict list itself is never dropped.
    """
    if unloaded_sources is None:
        return list(conflicts), []
    emitted: list[Any] = []
    suppressed: list[dict[str, Any]] = []
    for conflict in conflicts:
        code = getattr(conflict, "code", None)
        if code not in _DUPLICATE_CODES:
            emitted.append(conflict)
            continue
        component_name = getattr(conflict, "component", "")
        exempted = unloaded_sources.sections_for(component_name)
        if not exempted:
            emitted.append(conflict)
            continue
        sites = tuple(getattr(conflict, "sites", ()))
        remaining = tuple(
            sorted(site for site in sites if site[0] not in exempted)
        )
        if len(remaining) >= 2:
            emitted.append(dataclasses.replace(conflict, sites=remaining))
            continue
        # Only the exemptions this conflict actually hits are reported, with
        # the registry evidence for each (the component may list more
        # unloaded sections than this conflict touches).
        hit_sections = {site[0] for site in sites} & exempted
        hit_entries = tuple(
            entry
            for entry in unloaded_sources.entries
            if entry.component == component_name and entry.section in hit_sections
        )
        suppressed.append(
            {
                "code": code,
                "component": component_name,
                "anchor_key": getattr(conflict, "anchor_key", ""),
                "sites": [list(site) for site in sites],
                "exemptions": [
                    {"section": entry.section, "evidence": entry.evidence}
                    for entry in hit_entries
                ],
                "reason": (
                    "fewer than two non-exempted definition sites remain "
                    "(exempted sections are extracted but never loaded at "
                    "runtime): "
                    + ", ".join(sorted(hit_sections))
                ),
            }
        )
    return emitted, suppressed


def build_finding_records(
    *,
    registry: RuleRegistry,
    issues: Iterable[Issue],
    contexts: dict[str, FindingContext],
    conflicts: Iterable[Any],
    unloaded_sources: UnloadedSources | None = None,
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

    conflict_list, suppressed_conflicts = _filter_duplicate_conflicts(
        list(conflicts), unloaded_sources
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
                # R8 (cycle 3): the issue belongs to one specific occurrence;
                # several entries can share the editorial id (duplicated
                # occurrences), so the evidence must come from the entry whose
                # location matches the Issue exactly (logical_path + line). A
                # missing or ambiguous match fails closed instead of silently
                # binding evidence to an unrelated occurrence (which would
                # fabricate false new/resolved fingerprints).
                matching = [
                    entry
                    for entry in entries
                    if entry.get("logical_path") == issue.logical_path
                    and entry.get("line") == issue.line
                ]
                if len(matching) != 1:
                    skipped[issue.code] += 1
                    continue
                evidence = build_evidence_key(
                    rule.evidence_key_spec, entry=matching[0]
                )
            # R3: the Rule Registry severity is authoritative for enriched
            # findings (§9); the input lint Issue keeps its own severity in
            # the default lint path, only the record's issue is re-typed.
            records.append(
                FindingRecord(
                    issue=dataclasses.replace(issue, severity=rule.severity),
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

    for conflict in conflict_list:
        code = getattr(conflict, "code", None)
        if code not in _DUPLICATE_CODES:
            continue
        rule = registry.rules.get(code)
        if rule is None:
            skipped[code] += 1
            continue
        component_name = getattr(conflict, "component", "")
        anchor_key = getattr(conflict, "anchor_key", "")
        kind = getattr(conflict, "kind", "")
        context = contexts.get(component_name)
        participants: tuple[str, ...] = ()
        if context is not None and context.index is not None:
            # R6/FR3: conflict.sites already excludes exempted (unloaded)
            # sections; participants must be strong TUs of the conflict's own
            # kind that actually occur at a loaded definition site. The
            # IdentityConflict scope is (component, kind, strong anchor), so
            # a same-anchor-key TU of another kind or a fallback-editorial TU
            # must never participate (they would pollute subject/fingerprint).
            loaded_sections = frozenset(
                site[0] for site in getattr(conflict, "sites", ())
            )
            participants = tuple(
                sorted(
                    {
                        tu.tu_uid
                        for tu in context.index.tus.values()
                        if tu.kind == kind
                        and tu.identity_binding == "strong"
                        and tu.anchor_key == anchor_key
                        and tu.anchor_type is not None
                        and (set(tu.sections) & loaded_sections)
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
            severity=rule.severity,
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
    return records, {
        "unregistered_issues": dict(skipped),
        "suppressed_conflicts": suppressed_conflicts,
    }
