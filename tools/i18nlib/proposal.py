"""Validate structured translation proposals without applying them."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .build import _lua_value
from .config import Manifest
from .errors import ValidationError
from .lint import Issue, lint_documents, load_policy
from .locale_model import LocaleDocument
from .report import create_run_directory, write_json
from .workset import validate_workset


PROPOSAL_FIELDS = frozenset(
    {"entry_id", "source", "source_tag", "target", "args_order", "special", "notes"}
)
PROPOSAL_ROOT_FIELDS = frozenset({"schema_version", "workset_id", "proposals"})
MAX_JSON_BYTES = 16 * 1024 * 1024


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def decode_json_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        raise ValidationError(f"invalid {label} JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{label} JSON root must be an object")
    return value


def extract_event_stream_output(raw: bytes, label: str) -> bytes:
    """Extract the final assistant text from a pi `--mode json` event stream.

    pi buffers `--mode text` output until completion, which makes tmux panes
    look dead for minutes. `--mode json` streams one JSON event per line
    (message_start/message_update/message_end) in real time, so the pane shows
    live progress; the final assistant `message_end` carries the complete text.
    Plain non-event output (fixtures, older runs) is returned unchanged.
    """
    saw_event = False
    text_parts: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            # plain JSON output (fixtures, non-event lines) is not a stream
            continue
        saw_event = True
        if event.get("type") != "message_end":
            continue
        message = event.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        parts = [
            block["text"]
            for block in content
            if (
                isinstance(block, dict)
                and block.get("type") == "text"
                and isinstance(block.get("text"), str)
            )
        ]
        if parts:
            text_parts = parts
    if not saw_event:
        return raw
    return "\n".join(text_parts).encode("utf-8")


def read_json_object(path: Path, label: str) -> tuple[Path, dict[str, Any], bytes]:
    resolved = path.expanduser().resolve()
    try:
        if resolved.stat().st_size > MAX_JSON_BYTES:
            raise ValidationError(
                f"{label} exceeds the {MAX_JSON_BYTES}-byte input limit: {resolved}"
            )
        raw = resolved.read_bytes()
        value = decode_json_object(raw, label)
    except ValidationError:
        raise
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {resolved}") from error
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValidationError(f"unsupported {label} schema: {resolved}")
    return resolved, value, raw


def _proposal_issue(
    severity: str,
    code: str,
    message: str,
    logical_path: str,
    entry_id: str | None = None,
) -> Issue:
    return Issue(
        severity=severity,
        code=code,
        message=message,
        logical_path=logical_path,
        entry_id=entry_id,
    )


def validate_proposal(
    manifest: Manifest,
    *,
    workset_path: Path,
    proposal_path: Path,
    allow_partial: bool,
    strict: bool,
) -> dict[str, Any]:
    workset_resolved, workset, _workset_raw = read_json_object(
        workset_path, "workset"
    )
    proposal_resolved, proposal, proposal_raw = read_json_object(
        proposal_path, "proposal"
    )
    validate_workset(manifest, workset)
    workset_id = workset.get("workset_id")
    if not isinstance(workset_id, str) or proposal.get("workset_id") != workset_id:
        raise ValidationError("proposal workset_id does not match the supplied workset")
    root_unknown_fields = set(proposal) - PROPOSAL_ROOT_FIELDS
    if root_unknown_fields:
        raise ValidationError(
            f"proposal has unknown root fields: {sorted(root_unknown_fields)!r}"
        )
    component = workset.get("component")
    if not isinstance(component, str):
        raise ValidationError("workset component is invalid")
    workset_items = workset.get("items")
    proposals = proposal.get("proposals")
    if not isinstance(workset_items, list) or not all(
        isinstance(item, dict) for item in workset_items
    ):
        raise ValidationError("workset items are invalid")
    if not isinstance(proposals, list) or not all(
        isinstance(item, dict) for item in proposals
    ):
        raise ValidationError("proposal.proposals must be an object array")
    if not proposals:
        raise ValidationError("proposal.proposals must contain at least one item")

    items_by_id = {
        item.get("entry_id"): item
        for item in workset_items
        if isinstance(item.get("entry_id"), str)
    }
    issues: list[Issue] = []
    seen_ids: set[str] = set()
    normalized: list[dict[str, Any]] = []
    logical_path = str(proposal_resolved)
    for index, item in enumerate(proposals):
        unknown_fields = set(item) - PROPOSAL_FIELDS
        if unknown_fields:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-unknown-field",
                    f"proposal {index} has unknown fields: {sorted(unknown_fields)!r}",
                    logical_path,
                )
            )
        entry_id = item.get("entry_id")
        if not isinstance(entry_id, str) or entry_id not in items_by_id:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-entry-id",
                    f"proposal {index} does not name an item in the workset",
                    logical_path,
                    entry_id if isinstance(entry_id, str) else None,
                )
            )
            continue
        if entry_id in seen_ids:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-duplicate",
                    "entry_id appears more than once",
                    logical_path,
                    entry_id,
                )
            )
            continue
        seen_ids.add(entry_id)
        source_item = items_by_id[entry_id]
        source = item.get("source")
        source_tag = item.get("source_tag")
        target = item.get("target")
        if source != source_item.get("source"):
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-source-changed",
                    "proposal source does not exactly match the workset",
                    logical_path,
                    entry_id,
                )
            )
        if source_tag != source_item.get("source_tag"):
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-source-tag-changed",
                    "proposal source_tag does not exactly match the workset",
                    logical_path,
                    entry_id,
                )
            )
        if not isinstance(target, str) or not target:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-empty-target",
                    "proposal target must be a non-empty string",
                    logical_path,
                    entry_id,
                )
            )
            target = target if isinstance(target, str) else ""
        if "\x00" in target:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-nul",
                    "proposal target contains a NUL byte",
                    logical_path,
                    entry_id,
                )
            )
        notes = item.get("notes", "")
        if not isinstance(notes, str):
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-notes",
                    "proposal notes must be a string",
                    logical_path,
                    entry_id,
                )
            )
            notes = ""
        args_order = item.get("args_order")
        special = item.get("special")
        expected_special = source_item.get("previous_special")
        if special != expected_special:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-special-changed",
                    "proposal special must preserve the workset template value",
                    logical_path,
                    entry_id,
                )
            )
        if args_order is not None and not (
            isinstance(args_order, list)
            and all(
                isinstance(value, int) and not isinstance(value, bool)
                for value in args_order
            )
        ):
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-args-order",
                    "proposal args_order must be null or an integer array",
                    logical_path,
                    entry_id,
                )
            )
        try:
            _lua_value(args_order)
            _lua_value(special)
        except ValidationError as error:
            issues.append(
                _proposal_issue(
                    "error",
                    "proposal-lua-value",
                    str(error),
                    logical_path,
                    entry_id,
                )
            )
        normalized.append(
            {
                "entry_id": entry_id,
                "component": component,
                "section": source_item.get("section", ""),
                "source": source_item.get("source"),
                "source_tag": source_item.get("source_tag"),
                "target": target,
                "args_order": args_order,
                "special": special,
                "notes": notes,
            }
        )

    missing_ids = set(items_by_id) - seen_ids
    if missing_ids and not allow_partial:
        issues.append(
            _proposal_issue(
                "error",
                "proposal-incomplete",
                f"proposal omits {len(missing_ids)} workset entries",
                logical_path,
            )
        )

    synthetic_records = tuple(
        {
            "kind": "translation",
            "function_name": "t",
            "section": item["section"],
            "source": item["source"],
            "target": item["target"],
            "source_tag": item["source_tag"],
            "args_order": item["args_order"],
            "special": item["special"],
            "line": None,
            "logical_path": logical_path,
        }
        for item in normalized
        if isinstance(item.get("source"), str)
        and isinstance(item.get("target"), str)
        and item["target"]
    )
    synthetic = LocaleDocument(
        logical_path=logical_path,
        sha256=hashlib.sha256(proposal_raw).hexdigest(),
        records=synthetic_records,
    )
    lint_issues, lint_metrics = lint_documents(
        [(component, synthetic)], load_policy(manifest)
    )
    issues.extend(lint_issues)

    terminology = workset.get("terminology", [])
    if isinstance(terminology, list):
        proposals_by_id = {item["entry_id"]: item for item in normalized}
        for term in terminology:
            if not isinstance(term, dict) or term.get("status") != "preferred":
                continue
            preferred_target = term.get("target")
            matched_ids = term.get("matched_entry_ids")
            if not isinstance(preferred_target, str) or not isinstance(matched_ids, list):
                continue
            for entry_id in matched_ids:
                normalized_item = proposals_by_id.get(entry_id)
                if normalized_item is None:
                    continue
                if preferred_target not in normalized_item["target"]:
                    issues.append(
                        _proposal_issue(
                            "warning",
                            "preferred-term-missing",
                            f"preferred term target {preferred_target!r} is absent",
                            logical_path,
                            entry_id,
                        )
                    )

    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    ok = errors == 0 and (not strict or warnings == 0)
    proposal_id = hashlib.sha256(
        workset_id.encode("ascii")
        + b"\0"
        + json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    run_directory = create_run_directory(manifest.root, "proposal")
    report: dict[str, Any] = {
        "schema_version": 1,
        "tool_version": TOOL_VERSION,
        "ok": ok,
        "strict": strict,
        "allow_partial": allow_partial,
        "version": manifest.version,
        "component": component,
        "workset": str(workset_resolved),
        "workset_id": workset_id,
        "proposal": str(proposal_resolved),
        "proposal_id": proposal_id,
        "coverage": {
            "workset_items": len(items_by_id),
            "proposed": len(seen_ids),
            "missing": len(missing_ids),
        },
        "lint": lint_metrics,
        "errors": errors,
        "warnings": warnings,
        "issues": [issue.to_dict() for issue in issues],
        "normalized_proposals": normalized,
        "run_directory": str(run_directory),
    }
    report_path = run_directory / "proposal-validation.json"
    report["report"] = str(report_path)
    if ok:
        validated_path = run_directory / f"{proposal_id}.validated.json"
        report["validated_proposal"] = str(validated_path)
        write_json(
            validated_path,
            {
                "schema_version": 1,
                "workset_id": workset_id,
                "proposal_id": proposal_id,
                "proposals": normalized,
            },
        )
    write_json(report_path, report)
    return report
