"""Bounded, content-addressed translation worksets for agents or humans."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .config import Manifest
from .errors import ValidationError
from .lint import AT_TOKEN_RE, MARKUP_RE, stable_entry_id
from .report import create_run_directory, write_json


CLASSIFICATIONS = frozenset(
    {"added", "untranslated-existing", "source-changed"}
)
WORKSET_CONTRACT = "tome4-workset-v2"
WORKSET_IDENTITY_FIELDS = (
    "schema_version",
    "tool_version",
    "resolver_contract",
    "version",
    "merge_id",
    "component",
    "entry_ids",
    "terminology_sha256",
    "manifest_sha256",
    "content_sha256",
)
WORKSET_CONSTRAINTS = (
    "Preserve source and source_tag exactly in the returned proposal.",
    "Preserve every printf argument; use args_order only for an intentional permutation.",
    "Prefer terminology rows with status=preferred in the matching source_tag and scope.",
    "Do not edit canonical Lua files directly; return structured proposals keyed by entry_id.",
)
DLC_COMPONENTS = frozenset(
    {"ashes-urhrok", "cults", "items-vault", "orcs", "possessors"}
)
ADDON_COMPONENTS = frozenset({"addon-dev", "items-vault", "possessors"})
PRINTF_RE = re.compile(r"%[-+ #0]*\d*(?:\.\d+)?[cdeEfgGiouXxqs%]")


def _plain_source(value: str) -> str:
    value = MARKUP_RE.sub(" ", value)
    value = AT_TOKEN_RE.sub(" ", value)
    value = PRINTF_RE.sub(" ", value)
    return value.casefold()


def _read_merge_report(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    try:
        data = json.loads(resolved.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read merge report: {resolved}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid merge report JSON: {resolved}: {error}") from error
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        raise ValidationError(f"unsupported merge report: {resolved}")
    if not isinstance(data.get("merge_id"), str):
        raise ValidationError(f"merge report has no merge_id: {resolved}")
    untranslated = data.get("untranslated")
    if not isinstance(untranslated, list) or not all(
        isinstance(item, dict) for item in untranslated
    ):
        raise ValidationError(f"merge report has invalid untranslated items: {resolved}")
    data["_resolved_path"] = str(resolved)
    return data


def _resolve_manifest_path(manifest: Manifest, path: Path, label: str) -> Path:
    candidate = path.expanduser()
    if not candidate.is_absolute():
        candidate = manifest.root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(manifest.root.resolve())
    except ValueError as error:
        raise ValidationError(f"{label} path must be inside the manifest root") from error
    return resolved


def _terminology_rows(path: Path) -> tuple[list[dict[str, str]], str]:
    from .terminology import load_terminology_rows, terminology_store_sha256

    return load_terminology_rows(path), terminology_store_sha256(path)


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def workset_identity(workset: dict[str, Any]) -> dict[str, Any]:
    return {field: workset.get(field) for field in WORKSET_IDENTITY_FIELDS}


def calculate_workset_id(identity: dict[str, Any]) -> str:
    return _canonical_sha256(identity)


def workset_content(workset: dict[str, Any]) -> dict[str, Any]:
    return {
        "selection": workset.get("selection"),
        "constraints": workset.get("constraints"),
        "items": workset.get("items"),
        "terminology": workset.get("terminology"),
    }


def proposal_template_for(workset: dict[str, Any]) -> dict[str, Any]:
    items = workset.get("items")
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValidationError("cannot create a proposal template from invalid items")
    workset_id = workset.get("workset_id")
    if not isinstance(workset_id, str):
        raise ValidationError("cannot create a proposal template without workset_id")
    return {
        "schema_version": 1,
        "workset_id": workset_id,
        "proposals": [
            {
                "entry_id": item.get("entry_id"),
                "source": item.get("source"),
                "source_tag": item.get("source_tag"),
                "target": "",
                "args_order": item.get("previous_args_order"),
                "special": item.get("previous_special"),
                "notes": "",
            }
            for item in items
        ],
    }


def validate_workset_items(
    component: str, items: list[dict[str, Any]]
) -> None:
    seen: set[str] = set()
    for index, item in enumerate(items):
        section = item.get("section")
        source = item.get("source")
        source_tag = item.get("source_tag")
        entry_id = item.get("entry_id")
        if (
            not isinstance(section, str)
            or not section
            or not isinstance(source, str)
            or not source
        ):
            raise ValidationError(f"workset item {index} has an invalid editorial key")
        if source_tag is not None and not isinstance(source_tag, str):
            raise ValidationError(f"workset item {index} has an invalid source_tag")
        if item.get("component") != component:
            raise ValidationError(f"workset item {index} has the wrong component")
        expected_id = stable_entry_id(component, section, source, source_tag)
        if entry_id != expected_id:
            raise ValidationError(f"workset item {index} has an invalid entry_id")
        if entry_id in seen:
            raise ValidationError(f"workset contains duplicate entry_id {entry_id}")
        seen.add(entry_id)


def validate_workset(manifest: Manifest, workset: dict[str, Any]) -> None:
    if (
        type(workset.get("schema_version")) is not int
        or workset.get("schema_version") != 1
    ):
        raise ValidationError("unsupported workset schema")
    if workset.get("tool_version") != TOOL_VERSION:
        raise ValidationError("workset was generated by a different tool version")
    if workset.get("resolver_contract") != WORKSET_CONTRACT:
        raise ValidationError("unsupported workset resolver contract")
    if workset.get("version") != manifest.version:
        raise ValidationError("workset version does not match the selected manifest")
    component = workset.get("component")
    if not isinstance(component, str):
        raise ValidationError("workset component is invalid")
    manifest.component(component)
    expected_manifest_hash = hashlib.sha256(manifest.raw_bytes).hexdigest()
    if workset.get("manifest_sha256") != expected_manifest_hash:
        raise ValidationError("workset manifest digest is stale or invalid")

    items = workset.get("items")
    if not isinstance(items, list) or not items or not all(
        isinstance(item, dict) for item in items
    ):
        raise ValidationError("workset items are invalid or empty")
    validate_workset_items(component, items)
    entry_ids = [item["entry_id"] for item in items]
    if workset.get("entry_ids") != entry_ids:
        raise ValidationError("workset entry_ids do not match its items")
    if workset.get("constraints") != list(WORKSET_CONSTRAINTS):
        raise ValidationError("workset constraints are stale or invalid")

    terminology_rows, terminology_sha256 = _terminology_rows(
        manifest.root / manifest.terminology
    )
    if workset.get("terminology_sha256") != terminology_sha256:
        raise ValidationError("workset terminology digest is stale or invalid")
    expected_terms = _relevant_terms(terminology_rows, items, component)
    if workset.get("terminology") != expected_terms:
        raise ValidationError("workset terminology context is stale or invalid")
    if workset.get("content_sha256") != _canonical_sha256(
        workset_content(workset)
    ):
        raise ValidationError("workset content digest is invalid")
    if workset.get("workset_id") != calculate_workset_id(
        workset_identity(workset)
    ):
        raise ValidationError("workset_id is invalid")

    merge_report_path = workset.get("merge_report")
    if not isinstance(merge_report_path, str):
        raise ValidationError("workset merge_report path is invalid")
    merge_report_candidate = _resolve_manifest_path(
        manifest, Path(merge_report_path), "workset merge_report"
    )
    merge_report = _read_merge_report(merge_report_candidate)
    if merge_report.get("merge_id") != workset.get("merge_id"):
        raise ValidationError("workset merge_id does not match its merge report")
    if merge_report.get("component") != component:
        raise ValidationError("workset component does not match its merge report")
    report_items = {
        item.get("entry_id"): item for item in merge_report["untranslated"]
    }
    if any(report_items.get(item["entry_id"]) != item for item in items):
        raise ValidationError("workset items do not match its merge report")


def _scope_matches(scope: str, component: str) -> bool:
    if scope in {"global", "multi"}:
        return True
    if scope == "dlc":
        return component in DLC_COMPONENTS
    if scope == "core":
        return component not in DLC_COMPONENTS
    if scope == "addon":
        return component in ADDON_COMPONENTS
    return False


def _source_tag_matches(term_tag: str, item_tag: Any) -> bool:
    if term_tag == "nil":
        return item_tag is None
    if term_tag == "":
        return item_tag == ""
    return item_tag == term_tag


def _relevant_terms(
    rows: list[dict[str, str]], items: list[dict[str, Any]], component: str
) -> list[dict[str, Any]]:
    sources = [
        (
            item.get("entry_id"),
            _plain_source(item.get("source", "")),
            item.get("source_tag"),
        )
        for item in items
        if isinstance(item.get("entry_id"), str)
        and isinstance(item.get("source"), str)
    ]
    relevant: list[dict[str, Any]] = []
    for row in rows:
        term_source = row.get("source", "").strip()
        if not term_source:
            continue
        term_tag = row.get("source_tag", "")
        if not _scope_matches(row.get("scope", ""), component):
            continue
        folded = _plain_source(term_source).casefold()
        if not folded.strip():
            continue
        boundary = re.compile(
            rf"(?<![a-z0-9_]){re.escape(folded)}(?![a-z0-9_])"
        )
        matched_ids = [
            entry_id
            for entry_id, source, source_tag in sources
            if _source_tag_matches(term_tag, source_tag) and boundary.search(source)
        ]
        if not matched_ids:
            continue
        relevant.append(
            {
                "source": term_source,
                "target": row.get("target", ""),
                "category": row.get("category", ""),
                "source_tag": row.get("source_tag", ""),
                "status": row.get("status", ""),
                "scope": row.get("scope", ""),
                "notes": row.get("notes", ""),
                "matched_entry_ids": matched_ids,
            }
        )
    relevant.sort(
        key=lambda row: (
            row["source"].casefold(),
            0 if row["status"] == "preferred" else 1,
            row["source_tag"],
            row["scope"],
        )
    )
    return relevant


def create_workset(
    manifest: Manifest,
    *,
    merge_report_path: Path,
    limit: int,
    section_prefix: str | None,
    classification: str,
) -> dict[str, Any]:
    if type(limit) is not int or limit < 1 or limit > 500:
        raise ValidationError("workset --limit must be between 1 and 500")
    if classification != "all" and classification not in CLASSIFICATIONS:
        raise ValidationError(f"unsupported workset classification: {classification}")
    merge_report = _read_merge_report(
        _resolve_manifest_path(manifest, merge_report_path, "merge report")
    )
    component = merge_report.get("component")
    if not isinstance(component, str):
        raise ValidationError("merge report component is invalid")
    manifest.component(component)
    selected: list[dict[str, Any]] = []
    for item in merge_report["untranslated"]:
        item_classification = item.get("classification")
        if classification != "all" and item_classification != classification:
            continue
        section = item.get("section")
        if section_prefix is not None and (
            not isinstance(section, str) or not section.startswith(section_prefix)
        ):
            continue
        selected.append(item)
        if len(selected) == limit:
            break
    if not selected:
        raise ValidationError("no untranslated entries match the workset selection")
    validate_workset_items(component, selected)

    terminology_path = manifest.root / manifest.terminology
    terminology_rows, terminology_sha256 = _terminology_rows(terminology_path)
    relevant_terms = _relevant_terms(terminology_rows, selected, component)
    selection = {
        "classification": classification,
        "section_prefix": section_prefix,
        "limit": limit,
        "available_after_filter": sum(
            1
            for item in merge_report["untranslated"]
            if (classification == "all" or item.get("classification") == classification)
            and (
                section_prefix is None
                or (
                    isinstance(item.get("section"), str)
                    and item["section"].startswith(section_prefix)
                )
            )
        ),
        "selected": len(selected),
    }
    constraints = list(WORKSET_CONSTRAINTS)
    content = {
        "selection": selection,
        "constraints": constraints,
        "items": selected,
        "terminology": relevant_terms,
    }
    identity_payload = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "resolver_contract": WORKSET_CONTRACT,
        "version": manifest.version,
        "merge_id": merge_report["merge_id"],
        "component": component,
        "entry_ids": [item.get("entry_id") for item in selected],
        "terminology_sha256": terminology_sha256,
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "content_sha256": _canonical_sha256(content),
    }
    workset_id = calculate_workset_id(identity_payload)
    workset: dict[str, Any] = {
        **identity_payload,
        "workset_id": workset_id,
        "merge_report": merge_report["_resolved_path"],
        **content,
    }
    run_directory = create_run_directory(manifest.root, "workset")
    output_path = run_directory / f"{workset_id}.json"
    proposal_template_path = run_directory / f"{workset_id}.proposal-template.json"
    workset["output"] = str(output_path)
    workset["proposal_template"] = str(proposal_template_path)
    workset["run_directory"] = str(run_directory)
    proposal_template = proposal_template_for(workset)
    write_json(proposal_template_path, proposal_template)
    write_json(
        output_path,
        {
            **workset,
            "merge_report": os.path.relpath(
                merge_report["_resolved_path"], manifest.root
            ),
            "output": os.path.relpath(output_path, manifest.root),
            "proposal_template": os.path.relpath(
                proposal_template_path, manifest.root
            ),
            "run_directory": os.path.relpath(run_directory, manifest.root),
        },
    )
    return workset
