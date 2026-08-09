"""Normalized extraction snapshot model."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

from .errors import ValidationError
from .lint import stable_entry_id


_ORIGIN_KINDS = frozenset({"extracted", "manual"})


@dataclass(frozen=True)
class Definition:
    component: str
    section: str
    source: str
    source_tag: str | None
    origin_line: int | None
    origin_kind: str
    origin_document: str | None
    ordinal: int

    @property
    def editorial_key(self) -> tuple[str, str, str | None]:
        return self.section, self.source, self.source_tag

    @property
    def runtime_key(self) -> tuple[str, str | None]:
        return self.source, self.source_tag

    @property
    def entry_id(self) -> str:
        return stable_entry_id(
            self.component, self.section, self.source, self.source_tag
        )

    def origin_dict(self) -> dict[str, Any]:
        return {
            "line": self.origin_line,
            "kind": self.origin_kind,
            "document": self.origin_document,
        }


@dataclass(frozen=True)
class DefinitionGroup:
    definition: Definition
    occurrences: tuple[Definition, ...]

    @property
    def editorial_key(self) -> tuple[str, str, str | None]:
        return self.definition.editorial_key

    @property
    def runtime_key(self) -> tuple[str, str | None]:
        return self.definition.runtime_key

    @property
    def entry_id(self) -> str:
        return self.definition.entry_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "component": self.definition.component,
            "section": self.definition.section,
            "source": self.definition.source,
            "source_tag": self.definition.source_tag,
            "origins": [occurrence.origin_dict() for occurrence in self.occurrences],
        }


@dataclass(frozen=True)
class Snapshot:
    path: Path
    sha256: str
    component: str
    definitions: tuple[Definition, ...]
    groups: tuple[DefinitionGroup, ...]

    @cached_property
    def editorial_keys(self) -> frozenset[tuple[str, str, str | None]]:
        return frozenset(group.editorial_key for group in self.groups)

    @cached_property
    def runtime_keys(self) -> frozenset[tuple[str, str | None]]:
        return frozenset(group.runtime_key for group in self.groups)


def _nullable_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(f"{label} must be a string or null")
    return value


def read_snapshot(path: Path, *, expected_component: str | None = None) -> Snapshot:
    resolved = path.expanduser().resolve()
    try:
        data = resolved.read_bytes()
    except OSError as error:
        raise ValidationError(f"cannot read extraction snapshot: {resolved}") from error
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValidationError(f"snapshot is not UTF-8: {resolved}: {error}") from error

    definitions: list[Definition] = []
    component_name: str | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid snapshot JSON at {resolved}:{line_number}: {error}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(
                f"snapshot record is not an object at {resolved}:{line_number}"
            )
        component = record.get("component")
        section = record.get("section")
        source = record.get("source")
        if not isinstance(component, str) or not component:
            raise ValidationError(
                f"snapshot component is invalid at {resolved}:{line_number}"
            )
        if component_name is None:
            component_name = component
        elif component != component_name:
            raise ValidationError(
                f"snapshot mixes components at {resolved}:{line_number}"
            )
        if not isinstance(section, str) or not section:
            raise ValidationError(
                f"snapshot section is invalid at {resolved}:{line_number}"
            )
        if not isinstance(source, str):
            raise ValidationError(
                f"snapshot source is invalid at {resolved}:{line_number}"
            )
        origin_line = record.get("origin_line")
        if origin_line is not None and (
            not isinstance(origin_line, int)
            or isinstance(origin_line, bool)
            or origin_line < 1
        ):
            raise ValidationError(
                f"snapshot origin_line is invalid at {resolved}:{line_number}"
            )
        origin_kind = record.get("origin_kind")
        if not isinstance(origin_kind, str) or origin_kind not in _ORIGIN_KINDS:
            raise ValidationError(
                f"snapshot origin_kind is invalid at {resolved}:{line_number}"
            )
        source_tag = _nullable_string(
            record.get("source_tag"),
            f"snapshot source_tag at {resolved}:{line_number}",
        )
        origin_document = _nullable_string(
            record.get("origin_document"),
            f"snapshot origin_document at {resolved}:{line_number}",
        )
        if not source:
            if origin_kind == "extracted":
                # Empty extracted records belong to the byte-level baseline,
                # but are not translatable definitions for semantic consumers.
                continue
            raise ValidationError(
                f"snapshot source is invalid at {resolved}:{line_number}"
            )
        definitions.append(
            Definition(
                component=component,
                section=section,
                source=source,
                source_tag=source_tag,
                origin_line=origin_line,
                origin_kind=origin_kind,
                origin_document=origin_document,
                ordinal=len(definitions),
            )
        )
    if not definitions or component_name is None:
        raise ValidationError(f"snapshot contains no definitions: {resolved}")
    if expected_component is not None and component_name != expected_component:
        raise ValidationError(
            f"snapshot component mismatch: expected {expected_component}, got {component_name}"
        )

    grouped: dict[tuple[str, str, str | None], list[Definition]] = {}
    for definition in definitions:
        grouped.setdefault(definition.editorial_key, []).append(definition)
    groups = tuple(
        DefinitionGroup(definition=occurrences[0], occurrences=tuple(occurrences))
        for occurrences in grouped.values()
    )
    return Snapshot(
        path=resolved,
        sha256=hashlib.sha256(data).hexdigest(),
        component=component_name,
        definitions=tuple(definitions),
        groups=groups,
    )
