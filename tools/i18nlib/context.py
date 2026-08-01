"""Bounded translation and terminology context resolver."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from . import TOOL_VERSION
from .config import ComponentSpec, Manifest
from .errors import ValidationError
from .lint import stable_entry_id
from .locale_model import LocaleLoader
from .report import create_run_directory, write_json
from .workset import _canonical_sha256, _relevant_terms, _terminology_rows


def resolve_context(
    manifest: Manifest,
    loader: LocaleLoader,
    component: ComponentSpec,
    *,
    section_prefix: str | None,
    query: str | None,
    limit: int,
) -> dict[str, Any]:
    if limit < 1 or limit > 500:
        raise ValidationError("context --limit must be between 1 and 500")
    if section_prefix is None and (query is None or not query.strip()):
        raise ValidationError("context requires --section or --query")
    folded_query = query.casefold() if query else None
    document = loader.load_path(
        manifest.root / component.translation,
        logical_path=component.translation,
    )
    items: list[dict[str, Any]] = []
    available = 0
    for entry in document.translations:
        section = entry.get("section")
        source = entry.get("source")
        target = entry.get("target")
        source_tag = entry.get("source_tag")
        if not isinstance(section, str) or not isinstance(source, str) or not isinstance(target, str):
            continue
        if section_prefix is not None and not section.startswith(section_prefix):
            continue
        if folded_query is not None and (
            folded_query not in source.casefold()
            and folded_query not in target.casefold()
        ):
            continue
        available += 1
        if len(items) >= limit:
            continue
        items.append(
            {
                "entry_id": stable_entry_id(
                    component.id, section, source, source_tag
                ),
                "component": component.id,
                "section": section,
                "source": source,
                "target": target,
                "source_tag": source_tag,
                "args_order": entry.get("args_order"),
                "special": entry.get("special"),
                "line": entry.get("line"),
            }
        )

    terminology_rows, terminology_sha256 = _terminology_rows(
        manifest.root / manifest.terminology
    )
    relevant_terms = _relevant_terms(terminology_rows, items, component.id)
    content = {
        "items": items,
        "terminology": relevant_terms,
    }
    identity: dict[str, Any] = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "resolver_contract": "tome4-context-v2",
        "version": manifest.version,
        "component": component.id,
        "canonical_sha256": document.sha256,
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "terminology_sha256": terminology_sha256,
        "selection": {
            "section_prefix": section_prefix,
            "query": query,
            "limit": limit,
            "available": available,
            "selected": len(items),
        },
        "entry_ids": [item["entry_id"] for item in items],
        "content_sha256": _canonical_sha256(content),
    }
    context_id = hashlib.sha256(
        json.dumps(
            identity,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    result: dict[str, Any] = {
        **identity,
        "context_id": context_id,
        **content,
    }
    run_directory = create_run_directory(manifest.root, "context")
    output_path = run_directory / f"{context_id}.json"
    result["output"] = str(output_path)
    result["run_directory"] = str(run_directory)
    write_json(output_path, result)
    return result
