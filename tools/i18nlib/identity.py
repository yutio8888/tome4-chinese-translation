"""Entity / TU / Revision identity model (contract/0.1-rc3).

Frozen hash formulas (§4.5), EntityAnchor derivation (§4.4), Slot Registry
resolution (§4.6), discriminator policy (§4.7), TU index build, the v0.1
event contract (§4.8) and the MigrationMatcher levels (§5).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

from .errors import ConfigurationError, ContractError, ValidationError
from .lint import stable_entry_id
from .snapshot import Definition, Snapshot

SLOT_REGISTRY_RELATIVE_PATH = "i18n/quality/slot-registry-v1.json"
RULES_REGISTRY_RELATIVE_PATH = "i18n/quality/rules-registry-v1.json"
UNLOADED_SOURCES_RELATIVE_PATH = "i18n/quality/unloaded-sources-v1.json"

# --------------------------------------------------------------------------
# Frozen hash formulas (§4.5)


def entity_uid(component: str, kind: str, anchor_key: str) -> str:
    payload = "\0".join(("entity", component, kind, anchor_key))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def tu_uid_strong(entity: str, semantic_slot: str, discriminator: str) -> str:
    payload = "\0".join(("tu/strong", entity, semantic_slot, discriminator))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def tu_uid_fallback(editorial_id: str) -> str:
    payload = "\0".join(("tu/fallback-editorial", editorial_id))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def source_sha256(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def revision_uid(tu_uid: str, source_sha256_value: str) -> str:
    payload = "\0".join(("rev", tu_uid, source_sha256_value))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Slot Registry (§4.6)


@dataclass(frozen=True)
class SlotRegistry:
    path: Path
    slots: dict[str, str]

    @classmethod
    def load(cls, path: Path) -> "SlotRegistry":
        try:
            data = json.loads(path.read_bytes())
        except OSError as error:
            raise ContractError(f"cannot read slot registry: {path}") from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ContractError(
                f"invalid slot registry JSON: {path}: {error}"
            ) from error
        if not isinstance(data, dict):
            raise ConfigurationError("slot registry root must be an object")
        if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            raise ConfigurationError("unsupported slot registry schema")
        slots_data = data.get("slots")
        if not isinstance(slots_data, list) or not slots_data:
            raise ConfigurationError("slot registry 'slots' must be a non-empty array")
        slots: dict[str, str] = {}
        for index, entry in enumerate(slots_data):
            label = f"slot-registry slots[{index}]"
            if not isinstance(entry, dict):
                raise ConfigurationError(f"{label} must be an object")
            ast_path = entry.get("ast_path")
            semantic_slot = entry.get("semantic_slot")
            if not isinstance(ast_path, str) or not ast_path:
                raise ConfigurationError(f"{label}.ast_path must be a non-empty string")
            if not isinstance(semantic_slot, str) or not semantic_slot:
                raise ConfigurationError(
                    f"{label}.semantic_slot must be a non-empty string"
                )
            discriminator = entry.get("discriminator", "default")
            if discriminator not in ("default", "structural"):
                raise ConfigurationError(
                    f"{label}.discriminator must be 'default' or 'structural'"
                )
            if discriminator == "structural":
                raise ConfigurationError(
                    f"{label}: structural discriminators are not available in v0.1"
                )
            if ast_path in slots:
                raise ConfigurationError(f"{label}: duplicate ast_path {ast_path!r}")
            slots[ast_path] = semantic_slot
        return cls(path=path, slots=slots)

    def resolve(self, ast_path: str | None, source_tag: str | None) -> str:
        if ast_path:
            slot = self.slots.get(ast_path)
            if slot is not None:
                return slot
            return "UNKNOWN:" + ast_path
        return "UNKNOWN:" + (source_tag if source_tag is not None else "<nil>")


# --------------------------------------------------------------------------
# Enrichment sidecar records (§4.3)


@dataclass(frozen=True)
class EnrichmentRecord:
    section: str
    line: int
    source: str
    source_tag: str | None
    entity_kind: str
    anchor_hint: dict[str, Any]
    ast_path: str | None
    extraction_confidence: str

    @property
    def key(self) -> tuple[str, str, str | None, int]:
        return self.section, self.source, self.source_tag, self.line

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "section": self.section,
            "line": self.line,
            "source": self.source,
            "source_tag": self.source_tag,
            "entity_kind": self.entity_kind,
            "anchor_hint": self.anchor_hint,
            "ast_path": self.ast_path,
            "extraction_confidence": self.extraction_confidence,
        }


def _read_enrichment(path: Path) -> list[EnrichmentRecord]:
    try:
        text = path.read_bytes().decode("utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read enrichment sidecar: {path}") from error
    except UnicodeDecodeError as error:
        raise ValidationError(f"enrichment sidecar is not UTF-8: {path}") from error
    raw_records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid enrichment JSON at {path}:{line_number}: {error}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(
                f"enrichment record at {path}:{line_number} must be an object"
            )
        raw_records.append(record)
    return parse_enrichment_records(raw_records, source_label=str(path))


def parse_enrichment_records(
    raw_records: Iterable[dict[str, Any]], *, source_label: str
) -> list[EnrichmentRecord]:
    records: list[EnrichmentRecord] = []
    for position, record in enumerate(raw_records, start=1):
        label = f"enrichment record {position} ({source_label})"
        if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
            raise ValidationError(f"{label} has an unsupported schema_version")
        section = record.get("section")
        source = record.get("source")
        if not isinstance(section, str) or not section:
            raise ValidationError(f"{label}.section must be a non-empty string")
        if not isinstance(source, str):
            raise ValidationError(f"{label}.source must be a string")
        line_value = record.get("line")
        if type(line_value) is not int or line_value < 1:
            raise ValidationError(f"{label}.line must be a positive integer")
        source_tag = record.get("source_tag")
        if source_tag is not None and not isinstance(source_tag, str):
            raise ValidationError(f"{label}.source_tag must be a string or null")
        entity_kind = record.get("entity_kind")
        if not isinstance(entity_kind, str) or not entity_kind:
            raise ValidationError(f"{label}.entity_kind must be a non-empty string")
        anchor_hint = record.get("anchor_hint")
        if anchor_hint is not None and not isinstance(anchor_hint, dict):
            raise ValidationError(f"{label}.anchor_hint must be an object or null")
        ast_path = record.get("ast_path")
        if ast_path is not None and not isinstance(ast_path, str):
            raise ValidationError(f"{label}.ast_path must be a string or null")
        confidence = record.get("extraction_confidence")
        if confidence not in ("deterministic", "nondeterministic"):
            raise ValidationError(
                f"{label}.extraction_confidence must be "
                "'deterministic' or 'nondeterministic'"
            )
        records.append(
            EnrichmentRecord(
                section=section,
                line=line_value,
                source=source,
                source_tag=source_tag,
                entity_kind=entity_kind,
                anchor_hint=anchor_hint or {},
                ast_path=ast_path,
                extraction_confidence=confidence,
            )
        )
    if not records:
        raise ValidationError(f"enrichment sidecar is empty: {source_label}")
    return records


# --------------------------------------------------------------------------
# EntityAnchor derivation (§4.4)


_TALENT_ANCHOR_RE = re.compile(r"[ ']")


@dataclass(frozen=True)
class EntityAnchor:
    anchor_type: str
    anchor_key: str
    strong: bool


def _static_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _first_base(base: Any) -> str | None:
    if isinstance(base, str) and base:
        return base
    if isinstance(base, list):
        for item in base:
            if isinstance(item, str) and item:
                return item
    return None


def _derived_talent_short_name(short_name: str | None, name: str) -> str:
    base = short_name if short_name else name
    return "T_" + _TALENT_ANCHOR_RE.sub("_", base.upper())


_WEAK_NAME_KINDS = frozenset({"birth", "gem", "ingredient", "faction"})


def derive_anchor(record: EnrichmentRecord) -> EntityAnchor | None:
    """BC1: non-static anchor material yields no anchor (do not guess)."""
    if record.extraction_confidence != "deterministic":
        return None
    hint = record.anchor_hint
    kind = record.entity_kind
    if kind == "talent":
        name = _static_string(hint.get("name"))
        if name is None:
            return None
        short_name = _static_string(hint.get("short_name"))
        return EntityAnchor(
            "derived_short_name",
            _derived_talent_short_name(short_name, name),
            strong=True,
        )
    if kind == "effect":
        name = _static_string(hint.get("name"))
        if name is None:
            return None
        return EntityAnchor("effect_name", "EFF_" + name.upper(), strong=True)
    if kind == "talent_type":
        type_value = _static_string(hint.get("type"))
        if type_value is None:
            return None
        return EntityAnchor("type_string", type_value, strong=True)
    if kind == "entity":
        define_as = _static_string(hint.get("define_as"))
        if define_as is not None:
            return EntityAnchor("define_as", define_as, strong=True)
        base_first = _first_base(hint.get("base"))
        if base_first is not None:
            return EntityAnchor("base_fallback", base_first, strong=False)
        name = _static_string(hint.get("name"))
        type_value = _static_string(hint.get("type"))
        subtype = _static_string(hint.get("subtype"))
        if name is not None and type_value is not None and subtype is not None:
            return EntityAnchor(
                "composite", "|".join((name, type_value, subtype)), strong=False
            )
        return None
    if kind == "stat":
        short_name = _static_string(hint.get("stat_short_name"))
        if short_name is None:
            return None
        return EntityAnchor("stat_short_name", short_name, strong=True)
    if kind == "achievement":
        name = _static_string(hint.get("name"))
        if name is None:
            return None
        return EntityAnchor("achievement_name", name, strong=True)
    if kind in _WEAK_NAME_KINDS:
        name = _static_string(hint.get("name"))
        if name is None:
            return None
        return EntityAnchor(f"{kind}_name", name, strong=False)
    if kind == "lore":
        category = _static_string(hint.get("category"))
        if category is None:
            return None
        return EntityAnchor("lore_category", category, strong=False)
    return None  # free / module_meta / unknown kinds: no fabricated identity


# --------------------------------------------------------------------------
# Index model


@dataclass(frozen=True)
class Revision:
    revision_uid: str
    source: str
    source_sha256_value: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_uid": self.revision_uid,
            "source": self.source,
            "source_sha256": self.source_sha256_value,
        }


@dataclass(frozen=True)
class TU:
    tu_uid: str
    component: str
    entity_uid: str | None
    kind: str
    anchor_key: str | None
    anchor_type: str | None
    semantic_slot: str
    discriminator: str
    editorial_ids: tuple[str, ...]
    sections: tuple[str, ...]
    identity_binding: str
    revisions: tuple[Revision, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "tu_uid": self.tu_uid,
            "component": self.component,
            "entity_uid": self.entity_uid,
            "kind": self.kind,
            "anchor_key": self.anchor_key,
            "anchor_type": self.anchor_type,
            "semantic_slot": self.semantic_slot,
            "discriminator": self.discriminator,
            "editorial_ids": list(self.editorial_ids),
            "sections": list(self.sections),
            "identity_binding": self.identity_binding,
            "revisions": [revision.to_dict() for revision in self.revisions],
        }


@dataclass(frozen=True)
class Entity:
    entity_uid: str
    component: str
    kind: str
    anchor_key: str
    anchor_type: str
    sections: frozenset[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_uid": self.entity_uid,
            "component": self.component,
            "kind": self.kind,
            "anchor_key": self.anchor_key,
            "anchor_type": self.anchor_type,
            "sections": sorted(self.sections),
        }


@dataclass(frozen=True)
class IdentityConflict:
    code: str
    severity: str
    component: str
    kind: str
    anchor_key: str
    sites: tuple[tuple[str, int], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "component": self.component,
            "kind": self.kind,
            "anchor_key": self.anchor_key,
            "sites": [list(site) for site in self.sites],
        }


@dataclass(frozen=True)
class ComponentIndex:
    component: str
    source_snapshot_sha256: str
    entities: dict[str, Entity]
    tus: dict[str, TU]
    # Editorial ids are text-based and can legitimately map to several TUs
    # (the same text under different strong entities). Values are sorted.
    editorial_to_tu: dict[str, tuple[str, ...]]
    conflicts: tuple[IdentityConflict, ...]
    stats: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "component": self.component,
            "source_snapshot_sha256": self.source_snapshot_sha256,
            "entities": [
                entity.to_dict()
                for entity in sorted(
                    self.entities.values(), key=lambda value: value.entity_uid
                )
            ],
            "tus": [
                tu.to_dict()
                for tu in sorted(self.tus.values(), key=lambda value: value.tu_uid)
            ],
            "conflicts": [conflict.to_dict() for conflict in self.conflicts],
            "stats": dict(sorted(self.stats.items())),
        }


@dataclass(frozen=True)
class _OccurrenceIdentity:
    definition: Definition
    record: EnrichmentRecord | None
    anchor: EntityAnchor | None
    semantic_slot: str
    entity_uid_value: str | None
    tu_uid_value: str
    identity_binding: str


def _def_site(record: EnrichmentRecord) -> tuple[str, int]:
    hint = record.anchor_hint or {}
    line = hint.get("def_line")
    if type(line) is int and line >= 1:
        return record.section, line
    return record.section, record.line


def _conflict_code(kind: str, strong: bool) -> tuple[str, str]:
    if strong:
        if kind == "talent":
            return "duplicate-talent-id", "error"
        if kind == "effect":
            return "duplicate-effect-id", "error"
        return "identity_conflict", "context"
    return "identity_conflict", "context"


def build_component_index(
    *,
    component: str,
    snapshot: Snapshot,
    enrichment_records: Iterable[EnrichmentRecord],
    slot_registry: SlotRegistry,
) -> ComponentIndex:
    """Join snapshot definitions with the enrichment sidecar and resolve identity."""
    if snapshot.component != component:
        raise ValidationError(
            f"snapshot component mismatch: expected {component}, "
            f"got {snapshot.component}"
        )
    records = list(enrichment_records)
    # Empty extracted sources belong to the byte-level snapshot baseline but are
    # not translatable definitions (mirrors Snapshot.read semantics).
    records = [record for record in records if record.source]
    pending: dict[tuple[str, str, str | None, int], list[EnrichmentRecord]] = (
        defaultdict(list)
    )
    for record in records:
        pending[record.key].append(record)

    occurrences: list[_OccurrenceIdentity] = []
    unmatched_extracted = 0
    for definition in snapshot.definitions:
        if definition.origin_kind != "extracted":
            editorial_id = stable_entry_id(
                component, definition.section, definition.source, definition.source_tag
            )
            occurrences.append(
                _OccurrenceIdentity(
                    definition=definition,
                    record=None,
                    anchor=None,
                    semantic_slot="UNKNOWN:manual",
                    entity_uid_value=None,
                    tu_uid_value=tu_uid_fallback(editorial_id),
                    identity_binding="fallback-editorial",
                )
            )
            continue
        bucket = pending.get(
            (definition.section, definition.source, definition.source_tag, definition.origin_line),
            [],
        )
        if not bucket:
            unmatched_extracted += 1
            continue
        record = bucket.pop(0)
        if record.extraction_confidence == "deterministic":
            anchor = derive_anchor(record)
        else:
            anchor = None
        semantic_slot = slot_registry.resolve(record.ast_path, record.source_tag)
        editorial_id = stable_entry_id(
            component, definition.section, definition.source, definition.source_tag
        )
        if (
            anchor is not None
            and anchor.strong
            and not semantic_slot.startswith("UNKNOWN:")
        ):
            # §4.6: UNKNOWN slots never participate in strong binding; a
            # strong anchor without a registered slot is not a stable identity.
            uid = entity_uid(component, record.entity_kind, anchor.anchor_key)
            tu = tu_uid_strong(uid, semantic_slot, "default")
            occurrences.append(
                _OccurrenceIdentity(
                    definition=definition,
                    record=record,
                    anchor=anchor,
                    semantic_slot=semantic_slot,
                    entity_uid_value=uid,
                    tu_uid_value=tu,
                    identity_binding="strong",
                )
            )
        else:
            occurrences.append(
                _OccurrenceIdentity(
                    definition=definition,
                    record=record,
                    anchor=anchor,
                    semantic_slot=semantic_slot,
                    entity_uid_value=None,
                    tu_uid_value=tu_uid_fallback(editorial_id),
                    identity_binding="fallback-editorial",
                )
            )

    leftover = [record for bucket in pending.values() for record in bucket]
    if unmatched_extracted or leftover:
        raise ValidationError(
            f"enrichment join mismatch for {component}: "
            f"{unmatched_extracted} snapshot definitions without enrichment, "
            f"{len(leftover)} enrichment records without snapshot definition"
        )

    # BC2 duplicate-anchor detection (per component+kind, distinct def sites).
    strong_sites: dict[tuple[str, str, str], set[tuple[str, int]]] = defaultdict(set)
    weak_sites: dict[tuple[str, str, str, str], set[tuple[str, int]]] = defaultdict(set)
    for occurrence in occurrences:
        record = occurrence.record
        anchor = occurrence.anchor
        if record is None or anchor is None:
            continue
        site = _def_site(record)
        if anchor.strong:
            strong_sites[(component, record.entity_kind, anchor.anchor_key)].add(site)
        else:
            weak_sites[
                (component, record.entity_kind, anchor.anchor_type, anchor.anchor_key)
            ].add(site)
    conflicts: list[IdentityConflict] = []
    for (component_name, kind, anchor_key), sites in sorted(
        strong_sites.items(), key=lambda item: item[0]
    ):
        if len(sites) < 2:
            continue
        code, severity = _conflict_code(kind, strong=True)
        conflicts.append(
            IdentityConflict(
                code=code,
                severity=severity,
                component=component_name,
                kind=kind,
                anchor_key=anchor_key,
                sites=tuple(sorted(sites)),
            )
        )
    for (component_name, kind, anchor_type, anchor_key), sites in sorted(
        weak_sites.items(), key=lambda item: item[0]
    ):
        if len(sites) < 2:
            continue
        conflicts.append(
            IdentityConflict(
                code="identity_conflict",
                severity="context",
                component=component_name,
                kind=kind,
                anchor_key=f"{anchor_type}:{anchor_key}",
                sites=tuple(sorted(sites)),
            )
        )

    # Group occurrences into TUs (coalesce without structural evidence, §4.7).
    tu_groups: dict[str, list[_OccurrenceIdentity]] = defaultdict(list)
    entity_sections: dict[str, set[str]] = defaultdict(set)
    entity_meta: dict[str, tuple[str, str, str]] = {}
    for occurrence in occurrences:
        tu_groups[occurrence.tu_uid_value].append(occurrence)
        if (
            occurrence.entity_uid_value is not None
            and occurrence.anchor is not None
            and occurrence.record is not None
        ):
            entity_sections[occurrence.entity_uid_value].add(occurrence.definition.section)
            entity_meta[occurrence.entity_uid_value] = (
                occurrence.record.entity_kind,
                occurrence.anchor.anchor_key,
                occurrence.anchor.anchor_type,
            )

    entities: dict[str, Entity] = {}
    for uid, sections in sorted(entity_sections.items()):
        kind, anchor_key, anchor_type = entity_meta[uid]
        entities[uid] = Entity(
            entity_uid=uid,
            component=component,
            kind=kind,
            anchor_key=anchor_key,
            anchor_type=anchor_type,
            sections=frozenset(sections),
        )

    tus: dict[str, TU] = {}
    editorial_groups: dict[str, set[str]] = defaultdict(set)
    for tu_uid_value, group in sorted(tu_groups.items()):
        first = group[0]
        editorial_ids: list[str] = []
        sections: set[str] = set()
        revisions: dict[str, Revision] = {}
        for occurrence in group:
            definition = occurrence.definition
            editorial_id = stable_entry_id(
                component, definition.section, definition.source, definition.source_tag
            )
            editorial_ids.append(editorial_id)
            sections.add(definition.section)
            sha = source_sha256(definition.source)
            revision = revision_uid(tu_uid_value, sha)
            revisions[revision] = Revision(
                revision_uid=revision, source=definition.source, source_sha256_value=sha
            )
        for editorial_id in editorial_ids:
            editorial_groups[editorial_id].add(tu_uid_value)
        record = first.record
        tus[tu_uid_value] = TU(
            tu_uid=tu_uid_value,
            component=component,
            entity_uid=first.entity_uid_value,
            kind=record.entity_kind if record is not None else "free",
            anchor_key=first.anchor.anchor_key if first.anchor is not None else None,
            anchor_type=first.anchor.anchor_type if first.anchor is not None else None,
            semantic_slot=first.semantic_slot,
            discriminator="default",
            editorial_ids=tuple(dict.fromkeys(editorial_ids)),
            sections=tuple(sorted(sections)),
            identity_binding=first.identity_binding,
            revisions=tuple(
                sorted(revisions.values(), key=lambda value: value.revision_uid)
            ),
        )

    strong_count = sum(
        1 for tu in tus.values() if tu.identity_binding == "strong"
    )
    fallback_count = len(tus) - strong_count
    unknown_count = sum(
        1
        for occurrence in occurrences
        if occurrence.record is not None
        and (
            occurrence.record.extraction_confidence != "deterministic"
            or derive_anchor(occurrence.record) is None
        )
        and occurrence.identity_binding == "fallback-editorial"
    )
    return ComponentIndex(
        component=component,
        source_snapshot_sha256=snapshot.sha256,
        entities=entities,
        tus=tus,
        editorial_to_tu={
            editorial_id: tuple(sorted(tu_uids))
            for editorial_id, tu_uids in sorted(editorial_groups.items())
        },
        conflicts=tuple(conflicts),
        stats={
            "definitions": len(snapshot.definitions),
            "occurrences_bound": len(occurrences),
            "entities": len(entities),
            "tus": len(tus),
            "strong_tus": strong_count,
            "fallback_tus": fallback_count,
            "unknown_fallback_occurrences": unknown_count,
            "conflicts": len(conflicts),
        },
    )


def write_index_files(directory: Path, index: ComponentIndex) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    entities_path = directory / "entities.jsonl"
    tu_index_path = directory / "tu_index.jsonl"
    entities_bytes = b"".join(
        (
            json.dumps(entity.to_dict(), ensure_ascii=False, sort_keys=True)
            + "\n"
        ).encode("utf-8")
        for entity in sorted(index.entities.values(), key=lambda value: value.entity_uid)
    )
    tu_bytes = b"".join(
        (json.dumps(tu.to_dict(), ensure_ascii=False, sort_keys=True) + "\n").encode(
            "utf-8"
        )
        for tu in sorted(index.tus.values(), key=lambda value: value.tu_uid)
    )
    from .report import atomic_write_bytes

    atomic_write_bytes(entities_path, entities_bytes)
    atomic_write_bytes(tu_index_path, tu_bytes)
    return entities_path, tu_index_path


def _read_conflicts(path: Path, component: str) -> tuple[IdentityConflict, ...]:
    """Restore IdentityConflict records from a dumped identity.json (H1).

    Fail closed: a missing, corrupt, schema-mismatched or component-
    mismatched file raises ValidationError instead of silently yielding no
    conflicts (which would make the duplicate-id precheck disappear from
    baseline/incremental/report consumers).
    """
    try:
        text = path.read_bytes().decode("utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read identity conflicts file: {path}") from error
    except UnicodeDecodeError as error:
        raise ValidationError(f"identity conflicts file is not UTF-8: {path}") from error
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValidationError(
            f"invalid identity conflicts JSON at {path}: {error}"
        ) from error
    if not isinstance(data, dict):
        raise ValidationError(f"identity conflicts root must be an object: {path}")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValidationError(
            f"identity conflicts file has an unsupported schema_version: {path}"
        )
    if data.get("component") != component:
        raise ValidationError(
            f"identity conflicts component mismatch: expected {component!r}, "
            f"got {data.get('component')!r} in {path}"
        )
    raw_conflicts = data.get("conflicts")
    if not isinstance(raw_conflicts, list):
        raise ValidationError(
            f"identity conflicts 'conflicts' must be an array: {path}"
        )
    conflicts: list[IdentityConflict] = []
    _duplicate_kinds = {
        "duplicate-talent-id": "talent",
        "duplicate-effect-id": "effect",
    }
    for index, record in enumerate(raw_conflicts):
        label = f"identity conflict {index} ({path})"
        if not isinstance(record, dict):
            raise ValidationError(f"{label} must be an object")
        code = record.get("code")
        severity = record.get("severity")
        record_component = record.get("component")
        kind = record.get("kind")
        anchor_key = record.get("anchor_key")
        if not isinstance(code, str) or not code:
            raise ValidationError(f"{label}.code must be a non-empty string")
        # Closed model matching the producer (build_component_index): only
        # the three BC2 codes exist; code/severity/kind combinations are
        # bound, so a typo or an impossible pairing can never be silently
        # ignored by the finding layer.
        expected_kind = _duplicate_kinds.get(code)
        if code == "identity_conflict":
            if severity != "context":
                raise ValidationError(
                    f"{label}: identity_conflict must have severity 'context'"
                )
        elif expected_kind is None:
            raise ValidationError(
                f"{label}.code is not a known BC2 conflict code: {code!r}"
            )
        else:
            if severity != "error":
                raise ValidationError(
                    f"{label}: {code} must have severity 'error'"
                )
            if kind != expected_kind:
                raise ValidationError(
                    f"{label}: {code} requires kind {expected_kind!r}, "
                    f"got {kind!r}"
                )
        if record_component != component:
            raise ValidationError(
                f"{label}.component mismatch: expected {component!r}, "
                f"got {record_component!r}"
            )
        if not isinstance(kind, str) or not kind:
            raise ValidationError(f"{label}.kind must be a non-empty string")
        if not isinstance(anchor_key, str) or not anchor_key:
            raise ValidationError(f"{label}.anchor_key must be a non-empty string")
        raw_sites = record.get("sites")
        if not isinstance(raw_sites, list):
            raise ValidationError(f"{label}.sites must be an array")
        sites: list[tuple[str, int]] = []
        for site_index, site in enumerate(raw_sites):
            site_label = f"{label}.sites[{site_index}]"
            if (
                not isinstance(site, list)
                or len(site) != 2
                or not isinstance(site[0], str)
                or not site[0]
                or type(site[1]) is not int
                or site[1] < 1
            ):
                raise ValidationError(
                    f"{site_label} must be a [section, line] pair "
                    "with a non-empty section and a positive line"
                )
            sites.append((site[0], site[1]))
        if len(sites) < 2:
            raise ValidationError(
                f"{label} needs at least two definition sites, got {len(sites)}"
            )
        if len(set(sites)) != len(sites):
            raise ValidationError(f"{label}.sites contains duplicate sites")
        conflicts.append(
            IdentityConflict(
                code=code,
                severity=severity,
                component=component,
                kind=kind,
                anchor_key=anchor_key,
                sites=tuple(sorted(sites)),
            )
        )
    return tuple(conflicts)


def read_index_files(
    *,
    component: str,
    entities_path: Path,
    tu_index_path: Path,
    conflicts_path: Path | None = None,
) -> ComponentIndex:
    entities: dict[str, Entity] = {}
    try:
        lines = entities_path.read_bytes().decode("utf-8").splitlines()
    except OSError as error:
        raise ValidationError(f"cannot read entities index: {entities_path}") from error
    for line_number, line in enumerate(lines, start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid entities index JSON at {entities_path}:{line_number}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(f"entities index record {line_number} is not an object")
        try:
            entity = Entity(
                entity_uid=record["entity_uid"],
                component=record["component"],
                kind=record["kind"],
                anchor_key=record["anchor_key"],
                anchor_type=record["anchor_type"],
                sections=frozenset(record["sections"]),
            )
        except KeyError as error:
            raise ValidationError(
                f"entities index record {line_number} is missing {error}"
            ) from error
        if entity.entity_uid in entities:
            raise ValidationError(f"duplicate entity in entities index: {entity.entity_uid}")
        entities[entity.entity_uid] = entity

    tus: dict[str, TU] = {}
    editorial_groups: dict[str, set[str]] = defaultdict(set)
    try:
        lines = tu_index_path.read_bytes().decode("utf-8").splitlines()
    except OSError as error:
        raise ValidationError(f"cannot read TU index: {tu_index_path}") from error
    for line_number, line in enumerate(lines, start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid TU index JSON at {tu_index_path}:{line_number}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(f"TU index record {line_number} is not an object")
        try:
            revisions = tuple(
                Revision(
                    revision_uid=item["revision_uid"],
                    source=item["source"],
                    source_sha256_value=item["source_sha256"],
                )
                for item in record["revisions"]
            )
            tu = TU(
                tu_uid=record["tu_uid"],
                component=record["component"],
                entity_uid=record["entity_uid"],
                kind=record["kind"],
                anchor_key=record["anchor_key"],
                anchor_type=record["anchor_type"],
                semantic_slot=record["semantic_slot"],
                discriminator=record["discriminator"],
                editorial_ids=tuple(record["editorial_ids"]),
                sections=tuple(record["sections"]),
                identity_binding=record["identity_binding"],
                revisions=revisions,
            )
        except (KeyError, TypeError) as error:
            raise ValidationError(
                f"TU index record {line_number} is invalid: {error}"
            ) from error
        if tu.tu_uid in tus:
            raise ValidationError(f"duplicate TU in TU index: {tu.tu_uid}")
        tus[tu.tu_uid] = tu
        for editorial_id in tu.editorial_ids:
            editorial_groups[editorial_id].add(tu.tu_uid)

    conflicts: tuple[IdentityConflict, ...] = ()
    if conflicts_path is not None:
        conflicts = _read_conflicts(conflicts_path, component)
    return ComponentIndex(
        component=component,
        source_snapshot_sha256="",
        entities=entities,
        tus=tus,
        editorial_to_tu={
            editorial_id: tuple(sorted(tu_uids))
            for editorial_id, tu_uids in sorted(editorial_groups.items())
        },
        conflicts=conflicts,
        stats={
            "definitions": 0,
            "occurrences_bound": 0,
            "entities": len(entities),
            "tus": len(tus),
            "strong_tus": sum(1 for tu in tus.values() if tu.identity_binding == "strong"),
            "fallback_tus": sum(
                1 for tu in tus.values() if tu.identity_binding == "fallback-editorial"
            ),
            "unknown_fallback_occurrences": 0,
            "conflicts": len(conflicts),
        },
    )


# --------------------------------------------------------------------------
# Unloaded-sources registry (§4.4 BC2 load semantics, H1)
#
# A section listed here is extracted by the official extractor but never
# loaded by the game's load() entry points, so a strong anchor defined only
# there cannot collide at runtime. The registry is a manually verified
# exemption list (no second Lua parse; see contract §15 / migration-004).


@dataclass(frozen=True)
class UnloadedSourceEntry:
    component: str
    section: str
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "component": self.component,
            "section": self.section,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class UnloadedSources:
    path: Path
    entries: tuple[UnloadedSourceEntry, ...]

    def sections_for(self, component: str) -> frozenset[str]:
        return frozenset(
            entry.section for entry in self.entries if entry.component == component
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        *,
        path: Path | None = None,
        label: str = "unloaded-sources registry",
    ) -> "UnloadedSources":
        if not isinstance(data, dict):
            raise ValidationError(f"{label} root must be an object")
        if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            raise ValidationError(f"{label}: unsupported schema")
        raw_entries = data.get("entries")
        if not isinstance(raw_entries, list):
            raise ValidationError(f"{label} 'entries' must be an array")
        # R9 (cycle 3): an empty array is a legal "no exemptions right now"
        # state; only a missing/non-array key, a bad schema or a malformed
        # entry stays fail-closed.
        entries: list[UnloadedSourceEntry] = []
        seen: set[tuple[str, str]] = set()
        for index, entry in enumerate(raw_entries):
            entry_label = f"{label} entries[{index}]"
            if not isinstance(entry, dict):
                raise ValidationError(f"{entry_label} must be an object")
            component = entry.get("component")
            section = entry.get("section")
            evidence = entry.get("evidence")
            if not isinstance(component, str) or not component:
                raise ValidationError(f"{entry_label}.component must be a non-empty string")
            if not isinstance(section, str) or not section:
                raise ValidationError(f"{entry_label}.section must be a non-empty string")
            if not isinstance(evidence, str) or not evidence:
                raise ValidationError(f"{entry_label}.evidence must be a non-empty string")
            if (component, section) in seen:
                raise ValidationError(
                    f"{entry_label}: duplicate (component, section) pair"
                )
            seen.add((component, section))
            entries.append(
                UnloadedSourceEntry(
                    component=component, section=section, evidence=evidence
                )
            )
        return cls(path=path or Path(label), entries=tuple(entries))

    @classmethod
    def load(cls, path: Path) -> "UnloadedSources":
        try:
            data = json.loads(path.read_bytes())
        except OSError as error:
            raise ValidationError(
                f"cannot read unloaded-sources registry: {path}"
            ) from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValidationError(
                f"invalid unloaded-sources registry JSON: {path}: {error}"
            ) from error
        return cls.from_dict(data, path=path, label=str(path))


# --------------------------------------------------------------------------
# Event contract (§4.8)


@dataclass(frozen=True)
class IdentityEvent:
    kind: str  # unchanged | rename_candidate | deleted | created | ambiguous | hint
    component: str
    entity_kind: str
    section: str | None
    old_anchor_key: str | None
    new_anchor_key: str | None
    old_entity_uid: str | None
    new_entity_uid: str | None
    similarity: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "component": self.component,
            "entity_kind": self.entity_kind,
            "section": self.section,
            "old_anchor_key": self.old_anchor_key,
            "new_anchor_key": self.new_anchor_key,
            "old_entity_uid": self.old_entity_uid,
            "new_entity_uid": self.new_entity_uid,
            "similarity": (
                round(self.similarity, 6) if self.similarity is not None else None
            ),
        }


def _entity_slot_sources(index: ComponentIndex, entity: Entity) -> dict[str, str]:
    """Latest source text per semantic slot for an entity (same slot -> TU)."""
    slots: dict[str, str] = {}
    for tu in index.tus.values():
        if tu.entity_uid != entity.entity_uid or not tu.revisions:
            continue
        source = tu.revisions[-1].source
        slots.setdefault(tu.semantic_slot, source)
    return slots


def diff_indexes(
    *,
    base: ComponentIndex,
    new: ComponentIndex,
    threshold: float = 0.68,
) -> list[IdentityEvent]:
    if base.component != new.component:
        raise ValidationError("cannot diff indexes of different components")
    events: list[IdentityEvent] = []
    kinds = sorted(
        {entity.kind for entity in base.entities.values()}
        | {entity.kind for entity in new.entities.values()}
    )
    component = base.component
    for kind in kinds:
        base_kind = {
            uid: entity for uid, entity in base.entities.items() if entity.kind == kind
        }
        new_kind = {
            uid: entity for uid, entity in new.entities.items() if entity.kind == kind
        }
        for uid in sorted(base_kind.keys() & new_kind.keys()):
            events.append(
                IdentityEvent(
                    kind="unchanged",
                    component=component,
                    entity_kind=kind,
                    section=(
                        sorted(new_kind[uid].sections)[0]
                        if new_kind[uid].sections
                        else None
                    ),
                    old_anchor_key=base_kind[uid].anchor_key,
                    new_anchor_key=new_kind[uid].anchor_key,
                    old_entity_uid=uid,
                    new_entity_uid=uid,
                    similarity=None,
                )
            )
        gone = {
            uid: base_kind[uid] for uid in sorted(set(base_kind) - set(new_kind))
        }
        appeared = {
            uid: new_kind[uid] for uid in sorted(set(new_kind) - set(base_kind))
        }
        for old_uid, old in gone.items():
            old_sections = old.sections
            old_slots = _entity_slot_sources(base, old)
            candidates: list[tuple[str, Entity, float, str]] = []
            for new_uid, current in appeared.items():
                if not (old_sections & current.sections):
                    continue
                new_slots = _entity_slot_sources(new, current)
                shared = sorted(set(old_slots) & set(new_slots))
                if not shared:
                    continue
                best_ratio = max(
                    SequenceMatcher(
                        None, old_slots[slot], new_slots[slot], autojunk=False
                    ).ratio()
                    for slot in shared
                )
                if best_ratio >= threshold:
                    candidates.append((new_uid, current, best_ratio, shared[0]))
            if len(candidates) == 1:
                new_uid, current, ratio, slot = candidates[0]
                events.append(
                    IdentityEvent(
                        kind="rename_candidate",
                        component=component,
                        entity_kind=kind,
                        section=sorted(old_sections & current.sections)[0] or None,
                        old_anchor_key=old.anchor_key,
                        new_anchor_key=current.anchor_key,
                        old_entity_uid=old_uid,
                        new_entity_uid=new_uid,
                        similarity=ratio,
                    )
                )
            elif len(candidates) > 1:
                for new_uid, current, ratio, slot in candidates:
                    events.append(
                        IdentityEvent(
                            kind="ambiguous",
                            component=component,
                            entity_kind=kind,
                            section=sorted(old_sections & current.sections)[0] or None,
                            old_anchor_key=old.anchor_key,
                            new_anchor_key=current.anchor_key,
                            old_entity_uid=old_uid,
                            new_entity_uid=new_uid,
                            similarity=ratio,
                        )
                    )
                # Default resolution: deleted + created.
                events.append(
                    IdentityEvent(
                        kind="deleted",
                        component=component,
                        entity_kind=kind,
                        section=sorted(old_sections)[0] if old_sections else None,
                        old_anchor_key=old.anchor_key,
                        new_anchor_key=None,
                        old_entity_uid=old_uid,
                        new_entity_uid=None,
                        similarity=None,
                    )
                )
            else:
                # Hint: same section, semantic similarity without structural match.
                for new_uid, current in appeared.items():
                    if not (old_sections & current.sections):
                        continue
                    old_sources = list(old_slots.values())
                    new_sources = list(_entity_slot_sources(new, current).values())
                    if not old_sources or not new_sources:
                        continue
                    ratio = max(
                        SequenceMatcher(None, a, b, autojunk=False).ratio()
                        for a in old_sources
                        for b in new_sources
                    )
                    if ratio >= threshold:
                        events.append(
                            IdentityEvent(
                                kind="hint",
                                component=component,
                                entity_kind=kind,
                                section=sorted(old_sections & current.sections)[0] or None,
                                old_anchor_key=old.anchor_key,
                                new_anchor_key=current.anchor_key,
                                old_entity_uid=old_uid,
                                new_entity_uid=new_uid,
                                similarity=ratio,
                            )
                        )
                events.append(
                    IdentityEvent(
                        kind="deleted",
                        component=component,
                        entity_kind=kind,
                        section=sorted(old_sections)[0] if old_sections else None,
                        old_anchor_key=old.anchor_key,
                        new_anchor_key=None,
                        old_entity_uid=old_uid,
                        new_entity_uid=None,
                        similarity=None,
                    )
                )
        for new_uid in sorted(appeared):
            current = appeared[new_uid]
            events.append(
                IdentityEvent(
                    kind="created",
                    component=component,
                    entity_kind=kind,
                    section=sorted(current.sections)[0] if current.sections else None,
                    old_anchor_key=None,
                    new_anchor_key=current.anchor_key,
                    old_entity_uid=None,
                    new_entity_uid=new_uid,
                    similarity=None,
                )
            )
    events.sort(
        key=lambda event: (
            event.component,
            event.entity_kind,
            event.kind,
            event.old_entity_uid or "",
            event.new_entity_uid or "",
        )
    )
    return events


# --------------------------------------------------------------------------
# MigrationMatcher (§5)


@dataclass(frozen=True)
class MigrationMatch:
    level: str  # L1 | L2 | L3 | L4 | L5
    group: Any  # DefinitionGroup of the new snapshot
    tu_uid: str | None
    event: IdentityEvent | None
    previous_definition: Definition | None
    similarity: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "entry_id": self.group.entry_id,
            "component": self.group.definition.component,
            "section": self.group.definition.section,
            "source": self.group.definition.source,
            "source_tag": self.group.definition.source_tag,
            "tu_uid": self.tu_uid,
            "event": self.event.to_dict() if self.event is not None else None,
            "previous_source": (
                self.previous_definition.source
                if self.previous_definition is not None
                else None
            ),
            "similarity": (
                round(self.similarity, 6) if self.similarity is not None else None
            ),
        }


def _resolve_previous_definition(
    base_index: ComponentIndex,
    base_snapshot: Snapshot,
    old_entity_uid: str,
    semantic_slot: str,
    discriminator: str,
) -> Definition | None:
    """Resolve the unique old definition for an L2 rename match.

    The old entity (event.old_entity_uid) is matched in the base index by the
    new TU's semantic slot; the single base TU's editorial ids are then
    resolved against the base snapshot. Ambiguity or absence yields None so
    the caller keeps the L5 fallback semantics.
    """
    candidates = [
        tu
        for tu in base_index.tus.values()
        if tu.entity_uid == old_entity_uid
        and tu.semantic_slot == semantic_slot
        and tu.discriminator == discriminator
    ]
    if len(candidates) != 1:
        return None
    editorial_ids = set(candidates[0].editorial_ids)
    by_key: dict[tuple[str, str, str | None], Definition] = {}
    for definition in base_snapshot.definitions:
        if definition.entry_id in editorial_ids:
            by_key.setdefault(definition.editorial_key, definition)
    if len(by_key) != 1:
        return None
    return next(iter(by_key.values()))


def match_migrations(
    *,
    base_index: ComponentIndex | None,
    new_index: ComponentIndex | None,
    untranslated_groups: Iterable[Any],
    base_snapshot: Snapshot | None,
    threshold: float = 0.68,
) -> tuple[list[MigrationMatch], list[IdentityEvent]]:
    """L1-L5 matching for untranslated groups (contract §5)."""
    groups = list(untranslated_groups)
    matches: list[MigrationMatch] = []
    events: list[IdentityEvent] = []
    if base_index is None or new_index is None or base_snapshot is None:
        # Legacy path: L3 only (the existing source-changed heuristic).
        for group in groups:
            matches.append(
                MigrationMatch(
                    level="L3",
                    group=group,
                    tu_uid=None,
                    event=None,
                    previous_definition=None,
                    similarity=None,
                )
            )
        return matches, events

    events = diff_indexes(base=base_index, new=new_index, threshold=threshold)
    # L2 matches the *new* TU (which carries the new Entity UID). Rename
    # events are indexed by their new entity UID; several old entities can
    # each uniquely match the same new entity (multi-to-one), which is
    # ambiguous for L2 and must never resolve to an arbitrary event
    # (finding FR-001): only a single rename_candidate per new UID qualifies.
    rename_events_by_new: dict[str, list[IdentityEvent]] = defaultdict(list)
    for event in events:
        if event.kind == "rename_candidate" and event.new_entity_uid is not None:
            rename_events_by_new[event.new_entity_uid].append(event)
    base_tus = base_index.tus
    base_by_key = {d.editorial_key: d for d in base_snapshot.definitions}

    for group in groups:
        editorial_id = group.entry_id
        candidates = new_index.editorial_to_tu.get(editorial_id, ())
        tu_uid = candidates[0] if len(candidates) == 1 else None
        tu = new_index.tus.get(tu_uid) if tu_uid is not None else None
        if tu is not None and tu.identity_binding == "strong":
            if tu.tu_uid in base_tus:
                # L1: same Entity UID + slot + discriminator (absorbs moves).
                matches.append(
                    MigrationMatch(
                        level="L1",
                        group=group,
                        tu_uid=tu.tu_uid,
                        event=None,
                        previous_definition=None,
                        similarity=None,
                    )
                )
                continue
            # L2: anchor changed with structural evidence (rename event).
            rename_candidates = rename_events_by_new.get(tu.entity_uid, ())
            if len(rename_candidates) == 1:
                event = rename_candidates[0]
                previous_definition = _resolve_previous_definition(
                    base_index,
                    base_snapshot,
                    event.old_entity_uid,
                    tu.semantic_slot,
                    tu.discriminator,
                )
                if previous_definition is not None:
                    matches.append(
                        MigrationMatch(
                            level="L2",
                            group=group,
                            tu_uid=tu.tu_uid,
                            event=event,
                            previous_definition=previous_definition,
                            similarity=event.similarity,
                        )
                    )
                    continue
            # No unique resolvable previous definition (old entity lacks the
            # slot / ambiguity / several old entities map to this new entity):
            # fall through to L5 so the legacy heuristic can still surface a
            # source-changed suggestion for this group.
            matches.append(
                MigrationMatch(
                    level="L5",
                    group=group,
                    tu_uid=tu.tu_uid,
                    event=None,
                    previous_definition=None,
                    similarity=None,
                )
            )
            continue
        # Fallback-editorial: L3 (same section) vs L4 (cross section hint).
        same_section = [
            definition
            for definition in base_snapshot.definitions
            if definition.section == group.definition.section
        ]
        best: Definition | None = None
        best_ratio = 0.0
        for definition in same_section:
            ratio = SequenceMatcher(
                None, definition.source, group.definition.source, autojunk=False
            ).ratio()
            if ratio > best_ratio:
                best = definition
                best_ratio = ratio
        if best is not None and best_ratio >= threshold:
            matches.append(
                MigrationMatch(
                    level="L3",
                    group=group,
                    tu_uid=None,
                    event=None,
                    previous_definition=best,
                    similarity=best_ratio,
                )
            )
            continue
        cross_best: Definition | None = None
        cross_ratio = 0.0
        for definition in base_by_key.values():
            ratio = SequenceMatcher(
                None, definition.source, group.definition.source, autojunk=False
            ).ratio()
            if ratio > cross_ratio:
                cross_best = definition
                cross_ratio = ratio
        if cross_best is not None and cross_ratio >= threshold:
            matches.append(
                MigrationMatch(
                    level="L4",
                    group=group,
                    tu_uid=None,
                    event=None,
                    previous_definition=cross_best,
                    similarity=cross_ratio,
                )
            )
            continue
        matches.append(
            MigrationMatch(
                level="L5",
                group=group,
                tu_uid=None,
                event=None,
                previous_definition=None,
                similarity=None,
            )
        )
    return matches, events
