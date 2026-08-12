"""identity.sqlite current-state cache (contract/0.1-rc3 §10).

v0.1 keeps no unreconstructible history: the database is a pure cache
rebuildable from (snapshot.jsonl + tu_index.jsonl + translation files +
rules registry + slot registry + baseline snapshots).  Rebuild determinism
is verified by the canonical dump: INSERT statements ordered by table and
primary key, values in column order; the SHA-256 of the dump must be stable.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .baseline import Baseline
from .errors import ValidationError
from .fingerprint import FindingRecord
from .identity import ComponentIndex, Entity, Revision, TU
from .report import atomic_write_bytes

_TABLES = (
    "entities",
    "translation_units",
    "revisions",
    "findings",
    "baseline_lookup",
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS entities (
    entity_uid TEXT PRIMARY KEY,
    component TEXT NOT NULL,
    kind TEXT NOT NULL,
    anchor_key TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS translation_units (
    tu_uid TEXT PRIMARY KEY,
    entity_uid TEXT,
    semantic_slot TEXT NOT NULL,
    discriminator TEXT NOT NULL,
    editorial_id TEXT,
    identity_binding TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS revisions (
    revision_uid TEXT PRIMARY KEY,
    tu_uid TEXT NOT NULL,
    source_sha TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS findings (
    fingerprint TEXT PRIMARY KEY,
    rule_id TEXT NOT NULL,
    rule_schema_version INTEGER NOT NULL,
    tu_uid TEXT NOT NULL,
    participants TEXT NOT NULL,
    evidence_key TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS baseline_lookup (
    fingerprint TEXT PRIMARY KEY,
    baseline_file TEXT NOT NULL,
    status TEXT NOT NULL
);
"""


def _sql_literal(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _canonical_dump(connection: sqlite3.Connection) -> str:
    lines: list[str] = ["BEGIN TRANSACTION;"]
    for table in _TABLES:
        columns = [
            row[1]
            for row in connection.execute(f"PRAGMA table_info({table})")
        ]
        quoted = ", ".join(columns)
        rows = connection.execute(
            f"SELECT {quoted} FROM {table} ORDER BY {columns[0]}"
        ).fetchall()
        for row in rows:
            values = ", ".join(_sql_literal(value) for value in row)
            lines.append(f"INSERT INTO {table} ({quoted}) VALUES ({values});")
    lines.append("COMMIT;")
    return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class StorageReport:
    database: Path
    canonical_sha256: str
    tables: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "database": str(self.database),
            "canonical_sha256": self.canonical_sha256,
            "tables": dict(sorted(self.tables.items())),
        }


def identity_database_path(manifest_root: Path) -> Path:
    return manifest_root / ".artifacts" / "i18n" / "identity" / "identity.sqlite"


def load_indexes(connection: sqlite3.Connection, component: str) -> ComponentIndex:
    entities: dict[str, Entity] = {}
    for row in connection.execute(
        "SELECT entity_uid, component, kind, anchor_key FROM entities"
    ):
        entity_uid_value, component_name, kind, anchor_key = row
        entities[entity_uid_value] = Entity(
            entity_uid=entity_uid_value,
            component=component_name,
            kind=kind,
            anchor_key=anchor_key,
            anchor_type="",
            sections=frozenset(),
        )
    tus: dict[str, TU] = {}
    editorial_groups: dict[str, set[str]] = {}
    for row in connection.execute(
        "SELECT tu_uid, entity_uid, semantic_slot, discriminator, editorial_id, "
        "identity_binding FROM translation_units"
    ):
        tu_uid_value, entity_uid_value, slot, discriminator, editorial_id, binding = row
        revisions: dict[str, Revision] = {}
        for revision_row in connection.execute(
            "SELECT revision_uid, source_sha FROM revisions WHERE tu_uid = ?",
            (tu_uid_value,),
        ):
            revision_uid_value, source_sha = revision_row
            revisions[revision_uid_value] = Revision(
                revision_uid=revision_uid_value,
                source="",
                source_sha256_value=source_sha,
            )
        kind = ""
        anchor_key = None
        if entity_uid_value in entities:
            kind = entities[entity_uid_value].kind
            anchor_key = entities[entity_uid_value].anchor_key
        editorial_ids = (editorial_id,) if editorial_id is not None else ()
        tus[tu_uid_value] = TU(
            tu_uid=tu_uid_value,
            component=component,
            entity_uid=entity_uid_value,
            kind=kind,
            anchor_key=anchor_key,
            anchor_type=None,
            semantic_slot=slot,
            discriminator=discriminator,
            editorial_ids=editorial_ids,
            sections=(),
            identity_binding=binding,
            revisions=tuple(
                sorted(revisions.values(), key=lambda value: value.revision_uid)
            ),
        )
        if editorial_id is not None:
            editorial_groups.setdefault(editorial_id, set()).add(tu_uid_value)
    return ComponentIndex(
        component=component,
        source_snapshot_sha256="",
        entities=entities,
        tus=tus,
        editorial_to_tu={
            editorial_id: tuple(sorted(tu_uids))
            for editorial_id, tu_uids in sorted(editorial_groups.items())
        },
        conflicts=(),
        stats={},
    )


def rebuild_identity_database(
    manifest_root: Path,
    indexes: Iterable[ComponentIndex],
    baselines: Iterable[Baseline] = (),
    *,
    verify_sha256: str | None = None,
) -> StorageReport:
    """Deterministic rebuild from index files and baseline snapshots (§10.2).

    The canonical dump (INSERT statements ordered by table and primary key,
    values in column order) is computed from the connection for verification;
    the database file itself stays a real SQLite file.
    """
    database = identity_database_path(manifest_root)
    database.parent.mkdir(parents=True, exist_ok=True)
    temporary = database.with_suffix(".sqlite.tmp")
    if temporary.exists():
        temporary.unlink()
    connection = sqlite3.connect(str(temporary))
    try:
        connection.executescript(_SCHEMA)
        for index in indexes:
            for entity in index.entities.values():
                connection.execute(
                    "INSERT OR REPLACE INTO entities VALUES (?, ?, ?, ?, ?)",
                    (
                        entity.entity_uid,
                        entity.component,
                        entity.kind,
                        entity.anchor_key,
                        "active",
                    ),
                )
            for tu in index.tus.values():
                connection.execute(
                    "INSERT OR REPLACE INTO translation_units VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        tu.tu_uid,
                        tu.entity_uid,
                        tu.semantic_slot,
                        tu.discriminator,
                        tu.editorial_ids[0] if tu.editorial_ids else None,
                        tu.identity_binding,
                    ),
                )
                for revision in tu.revisions:
                    connection.execute(
                        "INSERT OR REPLACE INTO revisions VALUES (?, ?, ?)",
                        (revision.revision_uid, tu.tu_uid, revision.source_sha256_value),
                    )
        for baseline in baselines:
            for fingerprint, entry in baseline.entries.items():
                connection.execute(
                    "INSERT OR REPLACE INTO baseline_lookup VALUES (?, ?, ?)",
                    (
                        fingerprint,
                        baseline.path.name,
                        entry.status,
                    ),
                )
        connection.commit()
        dump = _canonical_dump(connection)
        tables = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in _TABLES
        }
    finally:
        connection.close()
    sha = hashlib.sha256(dump.encode("utf-8")).hexdigest()
    if verify_sha256 is not None and sha != verify_sha256:
        temporary.unlink()
        raise ValidationError(
            f"identity database rebuild is nondeterministic: "
            f"canonical dump sha256 {sha} != expected {verify_sha256}"
        )
    import os as _os

    _os.replace(temporary, database)
    return StorageReport(
        database=database, canonical_sha256=sha, tables=tables
    )


def store_findings(
    manifest_root: Path, records: Iterable[FindingRecord]
) -> None:
    database = identity_database_path(manifest_root)
    connection = sqlite3.connect(str(database))
    try:
        connection.executescript(_SCHEMA)
        for record in records:
            connection.execute(
                "INSERT OR REPLACE INTO findings VALUES (?, ?, ?, ?, ?, ?)",
                (
                    record.fingerprint,
                    record.rule_id,
                    record.rule_schema_version,
                    record.tu_uid,
                    json.dumps(
                        sorted(record.participants), ensure_ascii=False
                    ),
                    record.evidence_key,
                ),
            )
        connection.commit()
    finally:
        connection.close()
