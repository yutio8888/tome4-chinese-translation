"""Static and semantic validation for translation locale files."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .config import Manifest
from .errors import ConfigurationError
from .locale_model import LocaleDocument
from .semantics import runtime_semantic_signature


FORMAT_CONVERSIONS = frozenset("cdeEfgGiouXxqs")
FORMAT_FLAGS = frozenset("-+ #0")
FORMAT_TAGS = frozenset(
    {
        "tformat",
        "log",
        "logSeen",
        "logCombat",
        "logPlayer",
        "logMessage",
        "delayedLogMessage",
        "say",
        "saySimple",
        "easing",
        "easingSimple",
    }
)
MARKUP_RE = re.compile(r"#[A-Za-z0-9_{}:+.\-]+#")
AT_TOKEN_RE = re.compile(r"@[A-Za-z0-9_:+.\-]+@")
TERMINOLOGY_FIELDS = (
    "source",
    "target",
    "category",
    "domain",
    "source_tag",
    "status",
    "scope",
    "notes",
)
TERMINOLOGY_REQUIRED_FIELDS = (
    "source",
    "target",
    "category",
    "domain",
    "status",
    "scope",
)

TERMINOLOGY_DOMAINS = frozenset(
    {
        "combat",
        "talents",
        "classes",
        "resources",
        "items",
        "creatures",
        "places",
        "society",
        "narrative",
        "ui",
        "tech",
    }
)
TERMINOLOGY_STATUSES = frozenset({"existing", "preferred", "review"})
TERMINOLOGY_SCOPES = frozenset({"addon", "core", "dlc", "global", "multi"})


@dataclass(frozen=True)
class FormatToken:
    raw: str
    conversion: str
    offset: int


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str
    logical_path: str
    line: int | None = None
    entry_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Policy:
    allowed_empty_targets: frozenset[str]
    allowed_format_mismatches: frozenset[str]
    allowed_runtime_collisions: frozenset[str]


def extract_format_tokens(text: str) -> tuple[FormatToken, ...]:
    tokens: list[FormatToken] = []
    index = 0
    while index < len(text):
        if text[index] != "%":
            index += 1
            continue
        if index + 1 < len(text) and text[index + 1] == "%":
            index += 2
            continue
        cursor = index + 1
        while cursor < len(text) and text[cursor] in FORMAT_FLAGS:
            cursor += 1
        while cursor < len(text) and text[cursor].isdigit():
            cursor += 1
        if cursor < len(text) and text[cursor] == ".":
            cursor += 1
            while cursor < len(text) and text[cursor].isdigit():
                cursor += 1
        if cursor < len(text) and text[cursor] in FORMAT_CONVERSIONS:
            tokens.append(
                FormatToken(
                    raw=text[index : cursor + 1],
                    conversion=text[cursor],
                    offset=index,
                )
            )
            index = cursor + 1
        else:
            index += 1
    return tuple(tokens)


def stable_entry_id(
    component: str, section: str, source: str, source_tag: str | None
) -> str:
    tag_value = "<nil>" if source_tag is None else f"<string>{source_tag}"
    payload = "\0".join((component, section, source, tag_value))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _string_set(data: dict[str, Any], key: str) -> frozenset[str]:
    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ConfigurationError(f"policy.{key} must be a string array")
    if len(value) != len(set(value)):
        raise ConfigurationError(f"policy.{key} contains duplicates")
    return frozenset(value)


def load_policy(manifest: Manifest) -> Policy:
    path = manifest.root / manifest.policy
    try:
        data = json.loads(path.read_bytes())
    except OSError as error:
        raise ConfigurationError(f"cannot read lint policy: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(f"invalid lint policy JSON: {path}: {error}") from error
    if (
        not isinstance(data, dict)
        or type(data.get("schema_version")) is not int
        or data.get("schema_version") != 1
    ):
        raise ConfigurationError("unsupported lint policy schema")
    return Policy(
        allowed_empty_targets=_string_set(data, "allowed_empty_targets"),
        allowed_format_mismatches=_string_set(data, "allowed_format_mismatches"),
        allowed_runtime_collisions=_string_set(data, "allowed_runtime_collisions"),
    )


def _format_issue(
    *,
    component: str,
    entry: dict[str, Any],
    entry_id: str,
    policy: Policy,
) -> Issue | None:
    source = entry["source"]
    target = entry["target"]
    source_tag = entry.get("source_tag")
    args_order = entry.get("args_order")
    if source_tag not in FORMAT_TAGS and args_order is None:
        return None
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)

    if args_order is None:
        expected = [token.conversion for token in source_tokens]
    elif isinstance(args_order, list) and all(
        isinstance(index, int) and not isinstance(index, bool) for index in args_order
    ):
        if len(args_order) != len(source_tokens) or any(
            index < 1 or index > len(source_tokens) for index in args_order
        ):
            expected = []
        else:
            expected = [source_tokens[index - 1].conversion for index in args_order]
    else:
        expected = []

    actual = [token.conversion for token in target_tokens]
    valid_order = (
        args_order is None
        or (
            isinstance(args_order, list)
            and all(
                isinstance(index, int) and not isinstance(index, bool)
                for index in args_order
            )
            and len(args_order) == len(source_tokens)
            and all(1 <= index <= len(source_tokens) for index in args_order)
            and sorted(args_order) == list(range(1, len(source_tokens) + 1))
        )
    )
    if valid_order and expected == actual:
        return None
    if entry_id in policy.allowed_format_mismatches:
        return None
    return Issue(
        severity="error",
        code="format-mismatch",
        message=(
            "format arguments differ: "
            f"source={[token.raw for token in source_tokens]!r}, "
            f"target={[token.raw for token in target_tokens]!r}, "
            f"args_order={args_order!r}"
        ),
        logical_path=entry["logical_path"],
        line=entry.get("line"),
        entry_id=entry_id,
    )


def _format_shape_issue(
    *,
    entry: dict[str, Any],
    entry_id: str,
    policy: Policy,
) -> Issue | None:
    source_tag = entry.get("source_tag")
    args_order = entry.get("args_order")
    if source_tag not in FORMAT_TAGS and args_order is None:
        return None
    source_tokens = extract_format_tokens(entry["source"])
    target_tokens = extract_format_tokens(entry["target"])
    if args_order is None:
        expected = [token.raw for token in source_tokens]
    elif (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    ):
        expected = [source_tokens[index - 1].raw for index in args_order]
    else:
        return None
    actual = [token.raw for token in target_tokens]
    if expected == actual or entry_id in policy.allowed_format_mismatches:
        return None
    return Issue(
        severity="warning",
        code="format-shape-difference",
        message=f"format width/precision differs: expected={expected!r}, target={actual!r}",
        logical_path=entry["logical_path"],
        line=entry.get("line"),
        entry_id=entry_id,
    )


def lint_documents(
    documents: Iterable[tuple[str, LocaleDocument]],
    policy: Policy,
    *,
    require_nonempty: bool = False,
) -> tuple[list[Issue], dict[str, Any]]:
    issues: list[Issue] = []
    component_counts: dict[str, int] = {}
    duplicate_runtime_keys = 0
    for component, document in documents:
        entries = list(document.translations)
        component_counts[component] = len(entries)
        if require_nonempty and not entries:
            issues.append(
                Issue(
                    "error",
                    "empty-translation-file",
                    "canonical translation file contains no t(...) records",
                    document.logical_path,
                )
            )
        editorial: dict[
            tuple[str, str, str | None], list[tuple[dict[str, Any], str]]
        ] = defaultdict(list)
        runtime: dict[
            tuple[str, str | None], list[tuple[dict[str, Any], str]]
        ] = defaultdict(list)
        for entry in entries:
            source = entry.get("source")
            target = entry.get("target")
            section = entry.get("section")
            source_tag = entry.get("source_tag")
            if not isinstance(source, str) or not isinstance(target, str):
                issues.append(
                    Issue(
                        "error",
                        "invalid-entry",
                        "source and target must be strings",
                        document.logical_path,
                        entry.get("line"),
                    )
                )
                continue
            if not isinstance(section, str):
                section = ""
            if source_tag is not None and not isinstance(source_tag, str):
                issues.append(
                    Issue(
                        "error",
                        "invalid-source-tag",
                        "source_tag must be a string or nil",
                        document.logical_path,
                        entry.get("line"),
                    )
                )
                continue
            semantic_signature = runtime_semantic_signature(
                entry,
                label=(
                    f"translation {document.logical_path}:"
                    f"{entry.get('line', '?')}"
                ),
            )
            entry_id = stable_entry_id(component, section, source, source_tag)
            if target == "" and entry_id not in policy.allowed_empty_targets:
                issues.append(
                    Issue(
                        "error",
                        "empty-target",
                        "translation target is empty",
                        document.logical_path,
                        entry.get("line"),
                        entry_id,
                    )
                )
            format_issue = _format_issue(
                component=component,
                entry=entry,
                entry_id=entry_id,
                policy=policy,
            )
            if format_issue:
                issues.append(format_issue)
            else:
                shape_issue = _format_shape_issue(
                    entry=entry,
                    entry_id=entry_id,
                    policy=policy,
                )
                if shape_issue:
                    issues.append(shape_issue)

            source_markup = Counter(MARKUP_RE.findall(source))
            target_markup = Counter(MARKUP_RE.findall(target))
            if source_markup != target_markup:
                issues.append(
                    Issue(
                        "warning",
                        "markup-difference",
                        f"markup tokens differ: source={dict(source_markup)}, target={dict(target_markup)}",
                        document.logical_path,
                        entry.get("line"),
                        entry_id,
                    )
                )
            source_at = Counter(AT_TOKEN_RE.findall(source))
            target_at = Counter(AT_TOKEN_RE.findall(target))
            if source_at != target_at:
                issues.append(
                    Issue(
                        "warning",
                        "at-token-difference",
                        f"@tokens differ: source={dict(source_at)}, target={dict(target_at)}",
                        document.logical_path,
                        entry.get("line"),
                        entry_id,
                    )
                )
            occurrence = (entry, semantic_signature)
            editorial[(section, source, source_tag)].append(occurrence)
            runtime[(source, source_tag)].append(occurrence)

        for key, duplicates in editorial.items():
            semantic_values = {signature for _, signature in duplicates}
            if len(duplicates) > 1 and len(semantic_values) > 1:
                section, source, source_tag = key
                entry_id = stable_entry_id(component, section, source, source_tag)
                issues.append(
                    Issue(
                        "error",
                        "editorial-collision",
                        "same editorial key has different runtime values "
                        "(target/args_order/special; "
                        f"{len(duplicates)} entries)",
                        document.logical_path,
                        duplicates[-1][0].get("line"),
                        entry_id,
                    )
                )

        for (source, source_tag), duplicates in runtime.items():
            if len(duplicates) < 2:
                continue
            duplicate_runtime_keys += 1
            semantic_values = {signature for _, signature in duplicates}
            if len(semantic_values) < 2:
                continue
            collision_id = hashlib.sha256(
                "\0".join(
                    (
                        component,
                        source,
                        "<nil>" if source_tag is None else f"<string>{source_tag}",
                    )
                )
                .encode("utf-8")
            ).hexdigest()
            if collision_id in policy.allowed_runtime_collisions:
                continue
            locations = ", ".join(
                f"{entry.get('section', '')}:{entry.get('line', '?')}"
                for entry, _ in duplicates[:5]
            )
            issues.append(
                Issue(
                    "error",
                    "runtime-collision",
                    "runtime key resolves to "
                    f"{len(semantic_values)} semantic values "
                    "(target/args_order/special); "
                    f"locations: {locations}",
                    document.logical_path,
                    duplicates[-1][0].get("line"),
                    collision_id,
                )
            )

    metrics = {
        "components": component_counts,
        "translations": sum(component_counts.values()),
        "duplicate_runtime_keys": duplicate_runtime_keys,
        "errors": sum(issue.severity == "error" for issue in issues),
        "warnings": sum(issue.severity == "warning" for issue in issues),
    }
    return issues, metrics


def lint_terminology(path: Path) -> tuple[list[Issue], dict[str, Any]]:
    issues: list[Issue] = []
    rows: list[tuple[dict[str, str], int]] = []
    record_count = 0
    read_error_line: int | None = None
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t", strict=True)
            read_error_line = 1
            if tuple(reader.fieldnames or ()) != TERMINOLOGY_FIELDS:
                issues.append(
                    Issue(
                        "error",
                        "terminology-header",
                        f"expected TSV fields {TERMINOLOGY_FIELDS!r}, got {reader.fieldnames!r}",
                        str(path),
                        1,
                    )
                )
                return issues, {"rows": 0}
            while True:
                read_error_line = reader.line_num + 1
                try:
                    row = next(reader)
                except StopIteration:
                    break
                record_count += 1
                line = reader.line_num
                missing_fields = tuple(
                    field
                    for field in TERMINOLOGY_FIELDS
                    if field not in row or row[field] is None
                )
                extra_values = [
                    value
                    for field, value in row.items()
                    if field not in TERMINOLOGY_FIELDS
                ]
                if missing_fields == ("notes",) and not extra_values:
                    # The canonical terminology has historically omitted the
                    # final delimiter when an optional notes cell is empty.
                    row["notes"] = ""
                    missing_fields = ()
                if missing_fields or extra_values:
                    extra_count = sum(
                        len(value) if isinstance(value, list) else 1
                        for value in extra_values
                    )
                    actual_count = (
                        len(TERMINOLOGY_FIELDS) - len(missing_fields) + extra_count
                    )
                    details = []
                    if missing_fields:
                        details.append(
                            "missing " + ", ".join(repr(field) for field in missing_fields)
                        )
                    if extra_count:
                        details.append(f"{extra_count} extra")
                    issues.append(
                        Issue(
                            "error",
                            "terminology-row-width",
                            f"expected {len(TERMINOLOGY_FIELDS)} TSV fields, "
                            f"got {actual_count} ({'; '.join(details)})",
                            str(path),
                            line,
                        )
                    )
                    continue
                rows.append(
                    (
                        {field: row[field] for field in TERMINOLOGY_FIELDS},
                        line,
                    )
                )
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        issues.append(
            Issue(
                "error",
                "terminology-read",
                f"cannot read terminology TSV: {error}",
                str(path),
                read_error_line,
            )
        )
        return issues, {"rows": record_count}

    contexts: dict[tuple[str, str, str], list[tuple[dict[str, str], int]]] = defaultdict(list)
    for row, line in rows:
        for field in TERMINOLOGY_REQUIRED_FIELDS:
            if not (row.get(field) or "").strip():
                issues.append(
                    Issue(
                        "error",
                        "terminology-empty-field",
                        f"terminology field {field!r} is empty",
                        str(path),
                        line,
                    )
                )
        category = row.get("category") or ""
        if category and not category.startswith("T."):
            issues.append(
                Issue(
                    "error",
                    "terminology-category",
                    f"terminology category must start with 'T.': {category!r}",
                    str(path),
                    line,
                )
            )
        domain = row.get("domain") or ""
        if domain and domain not in TERMINOLOGY_DOMAINS:
            issues.append(
                Issue(
                    "error",
                    "terminology-domain",
                    f"terminology domain must be one of "
                    f"{sorted(TERMINOLOGY_DOMAINS)}: {domain!r}",
                    str(path),
                    line,
                )
            )
        status = row.get("status") or ""
        if status and status not in TERMINOLOGY_STATUSES:
            issues.append(
                Issue(
                    "error",
                    "terminology-status",
                    f"terminology status must be one of "
                    f"{sorted(TERMINOLOGY_STATUSES)}: {status!r}",
                    str(path),
                    line,
                )
            )
        scope = row.get("scope") or ""
        if scope and scope not in TERMINOLOGY_SCOPES:
            issues.append(
                Issue(
                    "error",
                    "terminology-scope",
                    f"terminology scope must be one of "
                    f"{sorted(TERMINOLOGY_SCOPES)}: {scope!r}",
                    str(path),
                    line,
                )
            )
        key = (row.get("source") or "", row.get("source_tag") or "", row.get("scope") or "")
        contexts[key].append((row, line))

    alternative_contexts = 0
    for declarations in contexts.values():
        if len(declarations) < 2:
            continue
        targets = {(row.get("target") or "") for row, _ in declarations}
        preferred = [
            (row, line)
            for row, line in declarations
            if (row.get("status") or "") == "preferred"
        ]
        if len(targets) > 1 and len(preferred) == 1:
            # A preferred row plus historical/review alternatives is an
            # intentional migration record, not a duplicate declaration.
            alternative_contexts += 1
            continue
        first_line = declarations[0][1]
        severity = "error" if len(targets) > 1 or len(preferred) > 1 else "warning"
        for _, line in declarations[1:]:
            issues.append(
                Issue(
                    severity,
                    "terminology-duplicate",
                    f"duplicate terminology context; first declared on line {first_line}",
                    str(path),
                    line,
                )
            )
    return issues, {
        "rows": record_count,
        "contexts": len(contexts),
        "alternative_contexts": alternative_contexts,
    }
