"""Semantic loading of locale Lua files through a LuaJIT bridge."""

from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .errors import ValidationError
from .runtime import LuaRuntime


@dataclass(frozen=True)
class LocaleDocument:
    logical_path: str
    sha256: str
    records: tuple[dict[str, Any], ...]

    @property
    def translations(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            record for record in self.records if record.get("kind") == "translation"
        )

    @property
    def definitions(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            record for record in self.records if record.get("kind") == "definition"
        )


class LocaleLoader:
    def __init__(self, runtime: LuaRuntime) -> None:
        self.runtime = runtime
        self.bridge = runtime.manifest.root / "tools" / "lua" / "load_locale.lua"
        if not self.bridge.is_file():
            raise ValidationError(f"locale bridge not found: {self.bridge}")

    def load_path(self, path: Path, *, logical_path: str | None = None) -> LocaleDocument:
        try:
            data = path.read_bytes()
        except OSError as error:
            raise ValidationError(f"cannot read locale file: {path}") from error
        return self.load_bytes(data, logical_path=logical_path or str(path))

    def load_bytes(self, data: bytes, *, logical_path: str) -> LocaleDocument:
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValidationError(f"locale is not UTF-8: {logical_path}: {error}") from error

        with tempfile.TemporaryDirectory(prefix="tome4-i18n-locale-") as temporary:
            temporary_path = Path(temporary)
            input_path = temporary_path / "input.lua"
            output_path = temporary_path / "records.jsonl"
            input_path.write_bytes(data)
            result = self.runtime.run(
                [self.bridge, input_path, output_path],
                cwd=self.runtime.manifest.root,
            )
            if result.returncode != 0:
                detail = result.stderr.strip() or result.stdout.strip()
                raise ValidationError(
                    f"Lua locale load failed for {logical_path}: {detail}"
                )
            try:
                lines = output_path.read_text(encoding="utf-8").splitlines()
            except OSError as error:
                raise ValidationError(
                    f"locale bridge produced no output for {logical_path}"
                ) from error

        records: list[dict[str, Any]] = []
        for line_number, line in enumerate(lines, start=1):
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValidationError(
                    f"invalid locale bridge JSON for {logical_path}:{line_number}: {error}"
                ) from error
            if not isinstance(record, dict) or not isinstance(record.get("kind"), str):
                raise ValidationError(
                    f"invalid locale bridge record for {logical_path}:{line_number}"
                )
            if record["kind"] == "translation":
                record.setdefault("source_tag", None)
                record.setdefault("args_order", None)
                record.setdefault("special", None)
                if record.get("args_order") == {}:
                    record["args_order"] = []
            elif record["kind"] == "definition":
                record.setdefault("source_tag", None)
            record["logical_path"] = logical_path
            records.append(record)
        return LocaleDocument(
            logical_path=logical_path,
            sha256=hashlib.sha256(data).hexdigest(),
            records=tuple(records),
        )


def runtime_map(
    documents: Iterable[LocaleDocument],
) -> dict[tuple[str, str | None], dict[str, Any]]:
    result: dict[tuple[str, str | None], dict[str, Any]] = {}
    for document in documents:
        for entry in document.translations:
            source = entry.get("source")
            source_tag = entry.get("source_tag")
            if isinstance(source, str) and (
                source_tag is None or isinstance(source_tag, str)
            ):
                result[(source, source_tag)] = entry
    return result
