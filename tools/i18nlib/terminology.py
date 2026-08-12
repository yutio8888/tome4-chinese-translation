"""Terminology store loading (single TSV file or domain directory).

Round-2 terminology review evolved the single ``terminology.tsv`` into a
domain directory (``terminology/<domain>.tsv``). All tools read through this
module so a store path may be either a single TSV or a directory of TSVs.

Directory semantics:

- files are processed in sorted file-name order;
- ``_line`` is a globally continuous 1-based line number across all files
  (header line of each file counts as 1, matching the single-file layout);
- ``_source`` records the file name each row came from;
- the content digest is the canonical SHA-256 of
  ``[{"path": <name>, "sha256": <file sha256>}, ...]`` sorted by name.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from .errors import ValidationError
from .lint import TERMINOLOGY_FIELDS, TERMINOLOGY_REQUIRED_FIELDS


def terminology_files(path: Path) -> list[Path]:
    """Return the TSV files of a store (directory) or the single file itself."""
    if path.is_dir():
        return sorted(path.glob("*.tsv"))
    return [path]


def load_terminology_rows(path: Path) -> list[dict[str, Any]]:
    """Read and structurally validate terminology without changing it.

    Accepts a single TSV file or a directory of TSVs. Each row is annotated
    with a globally continuous ``_line`` and its ``_source`` file name.
    """
    files = terminology_files(path)
    if not files:
        raise ValidationError(f"terminology store is empty: {path}")
    rows: list[dict[str, Any]] = []
    line_offset = 0
    for store_path in files:
        reader: csv.DictReader[str] | None = None
        try:
            with store_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle, delimiter="\t", strict=True)
                fieldnames = tuple(reader.fieldnames or ())
                if fieldnames != TERMINOLOGY_FIELDS:
                    raise ValidationError(
                        f"invalid terminology TSV: {store_path}: line 1: "
                        f"expected fields {TERMINOLOGY_FIELDS!r}, got {fieldnames!r}"
                    )
                for row in reader:
                    line = max(reader.line_num, 2)
                    missing = [
                        field
                        for field in TERMINOLOGY_REQUIRED_FIELDS
                        if field not in row or row[field] is None
                    ]
                    if missing:
                        raise ValidationError(
                            f"invalid terminology TSV: {store_path}: line {line}: "
                            f"missing required fields: {', '.join(missing)}"
                        )
                    empty = [
                        field
                        for field in TERMINOLOGY_REQUIRED_FIELDS
                        if not row[field].strip()
                    ]
                    if empty:
                        raise ValidationError(
                            f"invalid terminology TSV: {store_path}: line {line}: "
                            f"empty required fields: {', '.join(empty)}"
                        )
                    validated_row: dict[str, Any] = dict(row)
                    validated_row["_line"] = line_offset + line
                    validated_row["_source"] = store_path.name
                    rows.append(validated_row)
                line_offset += max(reader.line_num, 1)
        except ValidationError:
            raise
        except (OSError, UnicodeDecodeError, csv.Error) as error:
            line = max(reader.line_num if reader is not None else 1, 1)
            raise ValidationError(
                f"invalid terminology TSV: {store_path}: line {line}: {error}"
            ) from error
    return rows


def terminology_store_sha256(path: Path) -> str:
    """Content-addressed digest for a terminology file or directory.

    A single file keeps the historical raw-bytes digest; a directory uses
    the canonical JSON digest over per-file digests (sorted by file name).
    """
    files = terminology_files(path)
    if not files:
        raise ValidationError(f"terminology store is empty: {path}")
    if not path.is_dir() and len(files) == 1:
        return hashlib.sha256(files[0].read_bytes()).hexdigest()
    digest = json.dumps(
        [
            {"path": store_path.name, "sha256": hashlib.sha256(store_path.read_bytes()).hexdigest()}
            for store_path in files
        ],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(digest).hexdigest()
