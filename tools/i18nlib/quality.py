"""Translation quality: revision inventory, sampling, validation and reports.

Implements phase 1 of the translation quality system
(docs/translation-quality-phase-1.md, docs/translation-quality-system.md).
All outputs are derived artifacts under .artifacts/i18n/quality/runs/ and
never modify canonical Lua, terminology or release repositories.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import TOOL_VERSION
from .config import Manifest
from .errors import ConfigurationError, ValidationError
from .lint import (
    AT_TOKEN_RE,
    FORMAT_TAGS,
    MARKUP_RE,
    extract_format_tokens,
    stable_entry_id,
)
from .locale_model import LocaleLoader
from .report import atomic_write_bytes, write_json
from .workset import _plain_source, _scope_matches, _source_tag_matches

QUALITY_ROOT = "i18n/quality"
TAXONOMY_FILE = "taxonomy-v1.json"
POLICY_FILE = "policy-v1.json"
INVENTORY_CONTRACT = "tome4-quality-inventory-v1"
SAMPLE_CONTRACT = "tome4-quality-sample-v1"
ASSESSMENT_CONTRACT = "tome4-quality-assessment-v1"
ADJUDICATION_CONTRACT = "tome4-quality-adjudication-v1"
VALIDATION_CONTRACT = "tome4-quality-validation-v1"
REPORT_CONTRACT = "tome4-quality-report-v1"
IDENTITY_CONTRACT = "tome4-translation-revision-v1"
DEFAULT_SAMPLE_SEED = "tome4-quality-pilot-v1"

NEGATION_RE = re.compile(
    r"\b(?:no|not|never|none|without|unless|except|cannot|can't|won't|"
    r"don't|doesn't|didn't|isn't|aren't|hasn't|haven't|no longer|only if)\b",
    re.IGNORECASE,
)
CONDITION_RE = re.compile(
    r"\b(?:if|when|while|unless|only if|as long as|whenever)\b",
    re.IGNORECASE,
)
UNIT_WORD_RE = re.compile(
    r"\b(?:turns?|damage|radius|range|duration|chance|cooldown|seconds?|"
    r"minutes?|tiles?|yards?|meters?|percent|resistance|armou?r|mana|"
    r"stamina|life|health|speed|power)\b",
    re.IGNORECASE,
)
ASCII_WORD_RE = re.compile(r"[A-Za-z]{4,}")
SENTENCE_PUNCT_RE = re.compile(r"[.!?。！？]")
DIGIT_RE = re.compile(r"\d")
HOST_ABSOLUTE_PATH_RE = re.compile(
    r"/(?:Users|home|tmp|var|opt|usr|private|Volumes|etc|bin|sbin|dev|"
    r"mnt|media|root|run|srv|Applications)/"
)
WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\")
DOTDOT_PATH_RE = re.compile(r"(?:^|/)\.\.(?:/|$)")
LENGTH_OUTLIER_MAX_RATIO = 4.0
LENGTH_OUTLIER_MIN_RATIO = 0.25
LONG_SOURCE_LENGTH = 200
MAX_DOMAIN_HINTS = 5

_TERMINOLOGY_FIELDS = (
    "source",
    "target",
    "category",
    "domain",
    "source_tag",
    "status",
    "scope",
    "notes",
)


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    try:
        data = json.loads(resolved.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {resolved}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid {label} JSON: {resolved}: {error}") from error
    if not isinstance(data, dict):
        raise ValidationError(f"{label} root must be an object: {resolved}")
    return data


def _read_json_lines(path: Path, label: str) -> list[dict[str, Any]]:
    resolved = path.expanduser().resolve()
    try:
        lines = resolved.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {resolved}") from error
    except UnicodeDecodeError as error:
        raise ValidationError(f"invalid {label} encoding: {resolved}: {error}") from error
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationError(
                f"invalid {label} JSON at {resolved}:{line_number}: {error}"
            ) from error
        if not isinstance(record, dict):
            raise ValidationError(f"invalid {label} record at {resolved}:{line_number}")
        records.append(record)
    return records


def load_taxonomy(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / QUALITY_ROOT / TAXONOMY_FILE
    data = _read_json(path, "quality taxonomy")
    if data.get("contract") != "tome4-quality-taxonomy-v1":
        raise ConfigurationError(f"unsupported quality taxonomy: {path}")
    if data.get("schema_version") != 1:
        raise ConfigurationError(f"unsupported quality taxonomy schema: {path}")
    return data


def load_quality_policy(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / QUALITY_ROOT / POLICY_FILE
    data = _read_json(path, "quality policy")
    if data.get("contract") != "tome4-quality-policy-v1":
        raise ConfigurationError(f"unsupported quality policy: {path}")
    if data.get("schema_version") != 1:
        raise ConfigurationError(f"unsupported quality policy schema: {path}")
    return data


def _load_terminology(path: Path) -> tuple[list[dict[str, str]], str]:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        reader = csv.DictReader(text.splitlines(), delimiter="\t")
        rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        raise ValidationError(f"cannot load terminology for quality: {path}: {error}") from error
    if tuple(reader.fieldnames or ()) != _TERMINOLOGY_FIELDS:
        raise ValidationError(f"terminology header is invalid for quality: {path}")
    return rows, hashlib.sha256(raw).hexdigest()


def create_quality_run_directory(root: Path, kind: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run_directory = (
        root / ".artifacts" / "i18n" / "quality" / "runs" / f"{timestamp}-{kind}"
    )
    run_directory.mkdir(parents=True, exist_ok=False)
    return run_directory


def _write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    data = "".join(
        json.dumps(
            record, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        + "\n"
        for record in records
    ).encode("utf-8")
    atomic_write_bytes(path, data)


# ---------------------------------------------------------------------------
# Identity and structure
# ---------------------------------------------------------------------------


def compute_unit_id(
    component: str, section: str, source: str, source_tag: str | None
) -> str:
    return stable_entry_id(component, section, source, source_tag)


def compute_revision_id(
    version: str,
    unit_id: str,
    target: str,
    args_order: Any,
    special: Any,
) -> str:
    payload = {
        "identity_contract": IDENTITY_CONTRACT,
        "version": version,
        "unit_id": unit_id,
        "target": target,
        "args_order": args_order,
        "special": special,
    }
    return _canonical_sha256(payload)


def _multiset(tokens: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(tokens).items()))


def structure_signature(
    source: str, target: str, args_order: Any
) -> dict[str, Any]:
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    valid_order = (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and len(args_order) == len(source_tokens)
        and all(1 <= index <= len(source_tokens) for index in args_order)
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    )
    if valid_order:
        role_order = [source_tokens[index - 1].conversion for index in args_order]
    elif args_order is None:
        role_order = [token.conversion for token in source_tokens]
    else:
        role_order = None
    return {
        "printf": {
            "source_raw": [token.raw for token in source_tokens],
            "source_conversions": [token.conversion for token in source_tokens],
            "target_raw": [token.raw for token in target_tokens],
            "target_conversions": [token.conversion for token in target_tokens],
            "args_order": args_order,
            "role_order": role_order,
        },
        "markup": {
            "source": _multiset(MARKUP_RE.findall(source)),
            "target": _multiset(MARKUP_RE.findall(target)),
        },
        "at_tokens": {
            "source": _multiset(AT_TOKEN_RE.findall(source)),
            "target": _multiset(AT_TOKEN_RE.findall(target)),
        },
        "newlines": {"source": source.count("\n"), "target": target.count("\n")},
        "multiline": "\n" in source or "\n" in target,
    }


def _format_shape_matches(
    source: str, target: str, args_order: Any
) -> bool | None:
    """Raw-token comparison including width/precision (lint warning level)."""
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    if args_order is None:
        expected = [token.raw for token in source_tokens]
    elif (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and len(args_order) == len(source_tokens)
        and all(1 <= index <= len(source_tokens) for index in args_order)
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    ):
        expected = [source_tokens[index - 1].raw for index in args_order]
    else:
        return None
    return expected == [token.raw for token in target_tokens]


def _format_signature_matches(
    source: str, target: str, args_order: Any
) -> bool | None:
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    if args_order is None:
        expected = [token.conversion for token in source_tokens]
    elif (
        isinstance(args_order, list)
        and all(
            isinstance(index, int) and not isinstance(index, bool)
            for index in args_order
        )
        and len(args_order) == len(source_tokens)
        and all(1 <= index <= len(source_tokens) for index in args_order)
        and sorted(args_order) == list(range(1, len(source_tokens) + 1))
    ):
        expected = [source_tokens[index - 1].conversion for index in args_order]
    else:
        return None
    return expected == [token.conversion for token in target_tokens]


# ---------------------------------------------------------------------------
# Terminology index and relevant terms
# ---------------------------------------------------------------------------


def _build_term_index(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], Any, dict[str, list[int]]]:
    records: list[dict[str, Any]] = []
    for row in rows:
        source = (row.get("source") or "").strip()
        plain = _plain_source(source).strip()
        if not plain:
            continue
        records.append(
            {
                "source": source,
                "target": row.get("target") or "",
                "category": row.get("category") or "",
                "domain": row.get("domain") or "",
                "source_tag": row.get("source_tag") or "",
                "status": row.get("status") or "",
                "scope": row.get("scope") or "",
                "notes": row.get("notes") or "",
                "plain": plain,
            }
        )
    records.sort(
        key=lambda record: (
            record["plain"],
            0 if record["status"] == "preferred" else 1,
            record["source_tag"],
            record["scope"],
        )
    )
    by_plain: dict[str, list[int]] = defaultdict(list)
    for index, record in enumerate(records):
        by_plain[record["plain"]].append(index)
    matcher = None
    prefix_terms: dict[str, list[str]] = {}
    if records:
        # Longest-first alternation: Python regex alternation tries
        # alternatives left-to-right, so a shorter prefix term ('fire')
        # must never shadow a longer overlapping term ('fire damage').
        alternation = sorted(
            records, key=lambda record: (-len(record["plain"]), record["plain"])
        )
        matcher = re.compile(
            r"(?<![a-z0-9_])("
            + "|".join(re.escape(record["plain"]) for record in alternation)
            + r")(?![a-z0-9_])"
        )
        # A matched multi-word term subsumes its own boundary-respecting
        # prefix terms ('fire damage' also contains the term 'fire'); report
        # them together so term evidence stays complete (workset semantics).
        for record in records:
            plain = record["plain"]
            for other in records:
                other_plain = other["plain"]
                if len(other_plain) >= len(plain) or not plain.startswith(other_plain):
                    continue
                boundary_char = plain[len(other_plain)]
                if boundary_char.isalnum() or boundary_char == "_":
                    continue
                prefix_terms.setdefault(plain, []).append(other_plain)
    return records, matcher, by_plain, prefix_terms


def _relevant_terms_for(
    source: str,
    source_tag: str | None,
    component: str,
    term_records: list[dict[str, Any]],
    matcher: Any,
    by_plain: dict[str, list[int]],
    prefix_terms: dict[str, list[str]] | None = None,
) -> list[dict[str, Any]]:
    plain = _plain_source(source).strip()
    if not plain or matcher is None:
        return []
    matched_indices: set[int] = set()
    for match in matcher.finditer(plain):
        matched = match.group(1)
        matched_indices.update(by_plain.get(matched, ()))
        for prefix in (prefix_terms or {}).get(matched, ()):
            matched_indices.update(by_plain.get(prefix, ()))
    relevant: list[dict[str, Any]] = []
    for index in matched_indices:
        record = term_records[index]
        if not _scope_matches(record["scope"], component):
            continue
        if not _source_tag_matches(record["source_tag"], source_tag):
            continue
        relevant.append(
            {
                "source": record["source"],
                "target": record["target"],
                "category": record["category"],
                "domain": record["domain"],
                "source_tag": record["source_tag"],
                "status": record["status"],
                "scope": record["scope"],
                "notes": record["notes"],
                "match": "full" if record["plain"] == plain else "partial",
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


# ---------------------------------------------------------------------------
# Profile classification, risk flags and gate signals
# ---------------------------------------------------------------------------


def _section_matches(pattern: str, section: str) -> bool:
    """Segment-aware section pattern match.

    `pattern in section` substrings can misfire ("ui" matches
    "data/guilds/..."); requiring a contiguous path-segment sequence keeps
    patterns precise while still matching any depth.
    """
    pattern_segments = [segment for segment in pattern.split("/") if segment]
    if not pattern_segments:
        return False
    section_segments = section.split("/")
    width = len(pattern_segments)
    return any(
        section_segments[index : index + width] == pattern_segments
        for index in range(len(section_segments) - width + 1)
    )


def classify_profile(
    source: str,
    source_tag: str | None,
    section: str,
    relevant_terms: list[dict[str, Any]],
    taxonomy: dict[str, Any],
) -> tuple[str, str]:
    """Profile classification with priority: source_tag, term full match,
    section pattern, then structure fallback. Conflicting high-priority rules
    lower the confidence instead of silently overriding."""
    votes: list[tuple[str, str]] = []
    if source_tag and source_tag in taxonomy.get("source_tag_profiles", {}):
        votes.append((taxonomy["source_tag_profiles"][source_tag], "high"))
    plain = _plain_source(source).strip()
    for term in relevant_terms:
        if _plain_source(term["source"]).strip() == plain:
            category = term.get("category", "")
            if category in taxonomy.get("term_category_profiles", {}):
                votes.append((taxonomy["term_category_profiles"][category], "high"))
            break
    for rule in taxonomy.get("section_pattern_profiles", []):
        if _section_matches(rule["pattern"], section):
            votes.append((rule["profile"], rule["confidence"]))
    if votes:
        profiles = {profile for profile, _ in votes}
        if len(profiles) == 1:
            confidence = max(confidence for _, confidence in votes)
            return profiles.pop(), confidence
        return votes[0][0], "low"
    if (
        not extract_format_tokens(source)
        and len(source) <= 30
        and not SENTENCE_PUNCT_RE.search(source)
        and not MARKUP_RE.search(source)
        and not AT_TOKEN_RE.search(source)
    ):
        return "ui", "low"
    if len(source) >= LONG_SOURCE_LENGTH:
        return "narrative", "low"
    if extract_format_tokens(source) and not SENTENCE_PUNCT_RE.search(source):
        return "mechanics", "low"
    return "unknown", "low"


def _length_bin(length: int, taxonomy: dict[str, Any]) -> str:
    for bin_spec in taxonomy.get("length_bins", []):
        maximum = bin_spec.get("max")
        if maximum is None or length <= maximum:
            return bin_spec["id"]
    return "very-long"


def compute_risk_flags(
    source: str,
    target: str,
    structure: dict[str, Any],
    profile_confidence: str,
    relevant_terms: list[dict[str, Any]],
    runtime_stat: dict[str, Any],
    taxonomy: dict[str, Any],
) -> list[str]:
    whitelist = set(taxonomy.get("risk_flags", []))
    flags: list[str] = []

    def add(flag: str) -> None:
        if flag in whitelist:
            flags.append(flag)

    printf = structure["printf"]
    if printf["source_raw"]:
        add("has-printf")
    if printf["args_order"] is not None:
        add("has-args-order")
    if structure["markup"]["source"]:
        add("has-markup")
    if structure["at_tokens"]["source"]:
        add("has-at-token")
    if structure["multiline"]:
        add("multiline")
    plain = source.strip()
    if len(plain) <= 8 and " " not in plain and runtime_stat["section_count"] > 1:
        add("short-ambiguous-source")
    if len(source) >= LONG_SOURCE_LENGTH:
        add("long-source")
    if profile_confidence != "high":
        add("profile-uncertain")
    if any(term["status"] == "preferred" for term in relevant_terms):
        add("preferred-term-present")
    if any(term["status"] != "preferred" for term in relevant_terms):
        add("term-variant-or-review")
    if runtime_stat["occurrence_count"] > 1:
        add("repeated-runtime-key")
    stripped = printf["source_raw"]
    source_without_printf = source
    for raw in sorted(stripped, key=len, reverse=True):
        source_without_printf = source_without_printf.replace(raw, " ")
    if DIGIT_RE.search(source_without_printf) or UNIT_WORD_RE.search(source):
        add("source-has-number-or-unit")
    if NEGATION_RE.search(source) or CONDITION_RE.search(source):
        add("source-has-negation-or-condition")
    if len(source) >= 10 and target:
        ratio = len(target) / len(source)
        if ratio > LENGTH_OUTLIER_MAX_RATIO or ratio < LENGTH_OUTLIER_MIN_RATIO:
            add("source-target-length-outlier")
    stripped_target = MARKUP_RE.sub(" ", target)
    stripped_target = AT_TOKEN_RE.sub(" ", stripped_target)
    if len(ASCII_WORD_RE.findall(stripped_target)) >= 3:
        add("possible-untranslated-residue")
    return flags


def compute_gate_signals(
    source: str,
    target: str,
    source_tag: str | None,
    args_order: Any,
    structure: dict[str, Any],
    runtime_stat: dict[str, Any],
    cross_component_variant: bool,
) -> dict[str, Any]:
    format_applicable = source_tag in FORMAT_TAGS or args_order is not None
    return {
        "lua_load_valid": True,
        "empty_target": target == "",
        "format_signature_match": (
            _format_signature_matches(source, target, args_order)
            if format_applicable
            else None
        ),
        "format_shape_match": (
            _format_shape_matches(source, target, args_order)
            if format_applicable
            else None
        ),
        "markup_multiset_match": (
            structure["markup"]["source"] == structure["markup"]["target"]
        ),
        "at_token_multiset_match": (
            structure["at_tokens"]["source"] == structure["at_tokens"]["target"]
        ),
        "runtime_collision": runtime_stat["target_count"] > 1,
        "cross_component_variant": cross_component_variant,
        "needs_review": ["QG_CURRENT", "QG_SEVERE", "QG_CONTEXT", "QG_TERMS"],
    }


# ---------------------------------------------------------------------------
# M2: inventory
# ---------------------------------------------------------------------------


def build_inventory(
    manifest: Manifest, loader: LocaleLoader
) -> dict[str, Any]:
    taxonomy = load_taxonomy(manifest)
    terminology_rows, terminology_sha256 = _load_terminology(
        manifest.root / manifest.terminology
    )
    term_records, term_matcher, term_by_plain, term_prefixes = _build_term_index(
        terminology_rows
    )

    raw_entries: list[dict[str, Any]] = []
    runtime_stats: dict[
        tuple[str, str, str | None], dict[str, Any]
    ] = defaultdict(
        lambda: {
            "occurrence_count": 0,
            "section_count": 0,
            "target_count": 0,
            "sections": set(),
            "targets": set(),
        }
    )
    global_targets: dict[
        tuple[str, str | None], dict[str, set[str]]
    ] = defaultdict(lambda: defaultdict(set))
    for component in manifest.components:
        paths = [component.translation]
        if component.copy_fragment:
            paths.insert(0, component.copy_fragment)
        for logical_path in paths:
            document = loader.load_path(
                manifest.root / logical_path, logical_path=logical_path
            )
            for ordinal, record in enumerate(document.translations):
                source = record.get("source")
                target = record.get("target")
                section = record.get("section")
                if not all(isinstance(value, str) for value in (source, target, section)):
                    raise ValidationError(
                        f"invalid canonical translation entry in component "
                        f"{component.id}: {logical_path}"
                    )
                source_tag = record.get("source_tag")
                raw_entries.append(
                    {
                        "component": component.id,
                        "section": section,
                        "source": source,
                        "target": target,
                        "source_tag": source_tag,
                        "args_order": record.get("args_order"),
                        "special": record.get("special"),
                        "logical_path": logical_path,
                        "line": record.get("line"),
                        "ordinal": ordinal,
                    }
                )
                stat = runtime_stats[(component.id, source, source_tag)]
                stat["occurrence_count"] += 1
                stat["sections"].add(section)
                stat["targets"].add(target)
                stat["section_count"] = len(stat["sections"])
                stat["target_count"] = len(stat["targets"])
                global_targets[(source, source_tag)][component.id].add(target)

    revisions: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in raw_entries:
        unit_id = compute_unit_id(
            entry["component"], entry["section"], entry["source"], entry["source_tag"]
        )
        revision_id = compute_revision_id(
            manifest.version,
            unit_id,
            entry["target"],
            entry["args_order"],
            entry["special"],
        )
        key = (entry["component"], revision_id)
        revision = revisions.get(key)
        if revision is None:
            revision = {
                "unit_id": unit_id,
                "revision_id": revision_id,
                "version": manifest.version,
                "component": entry["component"],
                "section": entry["section"],
                "source": entry["source"],
                "target": entry["target"],
                "source_tag": entry["source_tag"],
                "args_order": entry["args_order"],
                "special": entry["special"],
                "occurrences": [],
            }
            revisions[key] = revision
        revision["occurrences"].append(
            {
                "logical_path": entry["logical_path"],
                "section": entry["section"],
                "line": entry["line"],
                "ordinal": entry["ordinal"],
            }
        )

    cross_component_variants: dict[tuple[str, str | None], bool] = {}
    for (source, source_tag), by_component in global_targets.items():
        union: set[str] = set()
        for targets in by_component.values():
            union.update(targets)
        cross_component_variants[(source, source_tag)] = (
            len(by_component) > 1 and len(union) > 1
        )

    entries: list[dict[str, Any]] = []
    for (component, revision_id), revision in sorted(revisions.items()):
        source = revision["source"]
        target = revision["target"]
        source_tag = revision["source_tag"]
        args_order = revision["args_order"]
        structure = structure_signature(source, target, args_order)
        relevant_terms = _relevant_terms_for(
            source,
            source_tag,
            component,
            term_records,
            term_matcher,
            term_by_plain,
            term_prefixes,
        )
        profile, profile_confidence = classify_profile(
            source, source_tag, revision["section"], relevant_terms, taxonomy
        )
        runtime_stat = runtime_stats[(component, source, source_tag)]
        revision["occurrences"].sort(
            key=lambda occurrence: (
                occurrence["logical_path"],
                occurrence["line"] if occurrence["line"] is not None else -1,
                occurrence["ordinal"],
            )
        )
        domains: list[str] = []
        for term in relevant_terms:
            domain = term.get("domain") or ""
            if domain and domain not in domains:
                domains.append(domain)
        entries.append(
            {
                **revision,
                "profile": profile,
                "profile_confidence": profile_confidence,
                "domain_hints": sorted(domains)[:MAX_DOMAIN_HINTS],
                "relevant_terms": relevant_terms,
                "structure": structure,
                "gate_signals": compute_gate_signals(
                    source,
                    target,
                    source_tag,
                    args_order,
                    structure,
                    runtime_stat,
                    cross_component_variants.get((source, source_tag), False),
                ),
                "risk_flags": compute_risk_flags(
                    source,
                    target,
                    structure,
                    profile_confidence,
                    relevant_terms,
                    runtime_stat,
                    taxonomy,
                ),
                "source_length_bin": _length_bin(len(source), taxonomy),
            }
        )

    inventory_sha256 = _canonical_sha256(entries)
    components: dict[str, dict[str, int]] = {}
    profiles: Counter[str] = Counter()
    length_bins: Counter[str] = Counter()
    risk_flags: Counter[str] = Counter()
    for entry in entries:
        component = entry["component"]
        bucket = components.setdefault(component, {"entries": 0, "occurrences": 0})
        bucket["entries"] += 1
        bucket["occurrences"] += len(entry["occurrences"])
        profiles[entry["profile"]] += 1
        length_bins[entry["source_length_bin"]] += 1
        for flag in entry["risk_flags"]:
            risk_flags[flag] += 1

    summary = {
        "entries": len(entries),
        "occurrences": len(raw_entries),
        "components": components,
        "profiles": dict(sorted(profiles.items())),
        "length_bins": dict(sorted(length_bins.items())),
        "risk_flags": dict(sorted(risk_flags.items())),
        "unverified_gates": ["QG_CURRENT", "QG_SEVERE", "QG_CONTEXT", "QG_TERMS"],
    }
    return {
        "schema_version": 1,
        "quality_contract": INVENTORY_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "terminology_sha256": terminology_sha256,
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(load_quality_policy(manifest)),
        "inventory_sha256": inventory_sha256,
        "entries": len(entries),
        "components": components,
        "profile_classifier_version": taxonomy.get("profile_classifier_version"),
        "risk_rule_version": taxonomy.get("risk_rule_version"),
        "summary": summary,
        "entries_list": entries,
    }


def run_inventory(manifest: Manifest, loader: LocaleLoader) -> dict[str, Any]:
    report = build_inventory(manifest, loader)
    run_directory = create_quality_run_directory(manifest.root, "inventory")
    entries = report.pop("entries_list")
    _write_jsonl(run_directory / "inventory.jsonl", entries)
    write_json(run_directory / "inventory-summary.json", report["summary"])
    manifest_report = {key: value for key, value in report.items()}
    write_json(run_directory / "inventory-manifest.json", manifest_report)
    report["run_directory"] = os_path_relative(run_directory, manifest)
    report["inventory"] = os_path_relative(run_directory / "inventory.jsonl", manifest)
    report["summary_path"] = os_path_relative(
        run_directory / "inventory-summary.json", manifest
    )
    return report


def os_path_relative(path: Path, manifest: Manifest) -> str:
    return str(path.relative_to(manifest.root))


def read_inventory_file(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    resolved = path.expanduser().resolve()
    entries = _read_json_lines(resolved, "quality inventory")
    if not entries:
        raise ValidationError(f"quality inventory is empty: {resolved}")
    for index, entry in enumerate(entries):
        if entry.get("quality_contract") not in (None, INVENTORY_CONTRACT):
            raise ValidationError(
                f"quality inventory record {index} has an unknown contract"
            )
        for field in ("unit_id", "revision_id", "component", "source"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                raise ValidationError(
                    f"quality inventory record {index} is malformed: {field}"
                )
        for field in ("section", "target"):
            if not isinstance(entry.get(field), str):
                raise ValidationError(
                    f"quality inventory record {index} is malformed: {field}"
                )
    revision_ids = [entry["revision_id"] for entry in entries]
    if len(revision_ids) != len(set(revision_ids)):
        raise ValidationError("quality inventory contains duplicate revision_id")
    return entries, {
        "entries": len(entries),
        "inventory_sha256": _canonical_sha256(entries),
    }


# ---------------------------------------------------------------------------
# M3: deterministic sampling
# ---------------------------------------------------------------------------


def _component_group(component: str, qpolicy: dict[str, Any]) -> str:
    for group, members in qpolicy.get("component_groups", {}).items():
        if component in members:
            return group
    return "auxiliary"


def _norm_source(source: str) -> str:
    return " ".join(_plain_source(source).split())


def _contrast_groups(
    entries: list[dict[str, Any]], qpolicy: dict[str, Any]
) -> list[tuple[str, list[dict[str, Any]]]]:
    max_size = int(qpolicy.get("contrast_group_max_size", 6))
    by_runtime_key: dict[tuple[str, str, str | None], list[dict[str, Any]]] = defaultdict(list)
    by_norm: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        by_runtime_key[(entry["component"], entry["source"], entry["source_tag"])].append(entry)
        by_norm[(entry["component"], _norm_source(entry["source"]))].append(entry)

    groups: list[tuple[str, list[dict[str, Any]]]] = []

    def add_group(kind: str, key: Any, members: list[dict[str, Any]]) -> None:
        members.sort(key=lambda entry: (entry["unit_id"], entry["revision_id"]))
        if len(members) > max_size:
            members = members[:max_size]
        if len(members) >= 2:
            groups.append(
                (
                    f"{kind}:{_canonical_sha256(str(key))[:12]}",
                    members,
                )
            )

    seen_keys: set[Any] = set()
    for key, members in sorted(by_runtime_key.items()):
        targets = {entry["target"] for entry in members}
        sections = {entry["section"] for entry in members}
        if len(targets) > 1:
            seen_keys.add(key)
            add_group("multi-target", key, members)
        elif len(sections) > 1:
            seen_keys.add(key)
            add_group("repeated-key", key, members)
    for key, members in sorted(by_norm.items()):
        if key in seen_keys:
            continue
        raw_sources = {entry["source"] for entry in members}
        if len(raw_sources) > 1:
            add_group("near-duplicate", key, members)
    return groups


def _entry_features(entry: dict[str, Any], qpolicy: dict[str, Any]) -> dict[str, Any]:
    enrichment = set(qpolicy.get("risk_enrichment_flags", []))
    structural = {
        "has-printf", "has-args-order", "has-markup", "has-at-token", "multiline"
    }
    flags = set(entry.get("risk_flags", []))
    term_evidence = any(
        term.get("status") in ("preferred", "existing", "review")
        for term in entry.get("relevant_terms", [])
    )
    return {
        "profile": entry.get("profile", "unknown"),
        "component_group": _component_group(entry.get("component", ""), qpolicy),
        "length_bin": entry.get("source_length_bin", "unknown"),
        "structural_risk": bool(flags & structural),
        "term_evidence": term_evidence,
        "enriched": bool(flags & enrichment),
    }


def _constraint_counts(
    selected: list[dict[str, Any]], constraints: list[dict[str, Any]]
) -> dict[str, Any]:
    counts: dict[str, Any] = {}
    for constraint in constraints:
        feature = constraint["feature"]
        if constraint.get("mode") == "each":
            per_value = {value: 0 for value in constraint["values"]}
            for entry in selected:
                value = entry["_features"][feature]
                if value in per_value:
                    per_value[value] += 1
            counts[constraint["id"]] = per_value
        else:
            values = set(constraint["values"])
            counts[constraint["id"]] = sum(
                1
                for entry in selected
                if entry["_features"][feature] in values
            )
    return counts


def _deficits(
    counts: dict[str, Any], constraints: list[dict[str, Any]]
) -> dict[str, Any]:
    deficits: dict[str, Any] = {}
    for constraint in constraints:
        count = counts[constraint["id"]]
        if constraint.get("mode") == "each":
            deficits[constraint["id"]] = {
                value: max(0, constraint["min"] - count[value])
                for value in constraint["values"]
            }
        else:
            deficits[constraint["id"]] = max(0, constraint["min"] - count)
    return deficits


def _constraint_score(
    entry: dict[str, Any], deficits: dict[str, Any], constraints: list[dict[str, Any]]
) -> int:
    score = 0
    for constraint in constraints:
        deficit = deficits[constraint["id"]]
        feature_value = entry["_features"][constraint["feature"]]
        if constraint.get("mode") == "each":
            if feature_value in deficit and deficit[feature_value] > 0:
                score += 1
        else:
            if (
                deficit > 0
                and feature_value in set(constraint["values"])
            ):
                score += 1
    return score


def _pick_for_deficits(
    pool: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
) -> dict[str, Any]:
    counts = _constraint_counts(selected, constraints)
    deficits = _deficits(counts, constraints)
    best_index = 0
    best_score = -1
    for index, entry in enumerate(pool):
        score = _constraint_score(entry, deficits, constraints)
        if score > best_score:
            best_score = score
            best_index = index
    return pool.pop(best_index)


def _select_bucket(
    pool: list[dict[str, Any]],
    target: int,
    selected: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    rng: random.Random,
) -> list[dict[str, Any]]:
    rng.shuffle(pool)
    chosen: list[dict[str, Any]] = []
    while len(chosen) < target and pool:
        chosen.append(_pick_for_deficits(pool, selected + chosen, constraints))
    return chosen


def generate_sample(
    manifest: Manifest,
    inventory_path: Path,
    size: int | None = None,
    seed: str | None = None,
) -> dict[str, Any]:
    qpolicy = load_quality_policy(manifest)
    taxonomy = load_taxonomy(manifest)
    entries, inventory_info = read_inventory_file(inventory_path)
    bucket_targets = qpolicy["pilot"]["buckets"]
    total_target = sum(bucket_targets.values())
    if size is None:
        size = total_target
    if size != total_target:
        raise ValidationError(
            f"pilot sample size must be {total_target} for policy-v1 "
            f"(got {size})"
        )
    if seed is None:
        seed = qpolicy["pilot"].get("seed", DEFAULT_SAMPLE_SEED)
    constraints = qpolicy.get("coverage_constraints", [])
    by_revision = {entry["revision_id"]: entry for entry in entries}
    for entry in entries:
        entry["_features"] = _entry_features(entry, qpolicy)

    groups = _contrast_groups(entries, qpolicy)
    rng = random.Random(seed)
    group_order = list(groups)
    rng.shuffle(group_order)

    contrast: list[dict[str, Any]] = []
    contrast_group_of: dict[str, str] = {}
    contrast_ids: set[str] = set()
    for group_id, members in group_order:
        if len(contrast) + len(members) > bucket_targets["contrast"] and contrast:
            continue
        # Contrast groups are atomic: a group whose members were already
        # claimed by an earlier overlapping group must be skipped whole,
        # never sampled partially (phase-1 doc section 6.2).
        if any(member["revision_id"] in contrast_ids for member in members):
            continue
        for member in members:
            contrast_ids.add(member["revision_id"])
            contrast_group_of[member["revision_id"]] = group_id
            contrast.append(member)
        if len(contrast) >= bucket_targets["contrast"]:
            break
    if len(contrast) < bucket_targets["contrast"]:
        # Backfill with the smallest remaining whole groups. Adding a group may
        # overshoot the bucket target, but the overshoot is bounded by the
        # smallest remaining group size (<= contrast_group_max_size) and the
        # actual bucket_counts are reported in the sample manifest, so whole
        # groups are never split to hit the exact target.
        remaining = [
            (group_id, members)
            for group_id, members in group_order
            if any(member["revision_id"] not in contrast_ids for member in members)
        ]
        remaining.sort(key=lambda item: len(item[1]))
        for group_id, members in remaining:
            if len(contrast) >= bucket_targets["contrast"]:
                break
            if any(member["revision_id"] in contrast_ids for member in members):
                continue
            for member in members:
                contrast_ids.add(member["revision_id"])
                contrast_group_of[member["revision_id"]] = group_id
                contrast.append(member)

    risk_pool = [
        entry
        for entry in entries
        if entry["revision_id"] not in contrast_ids and entry["_features"]["enriched"]
    ]

    selected: list[dict[str, Any]] = list(contrast)
    risk_selected = _select_bucket(
        risk_pool, bucket_targets["risk-enriched"], selected, constraints, rng
    )
    risk_selected_ids = {entry["revision_id"] for entry in risk_selected}
    selected.extend(risk_selected)
    # The representative bucket is a stratified random sample of the whole
    # remaining corpus (mutually exclusive with the other buckets, but not
    # restricted to non-enriched entries), per phase-1 doc section 6.1.
    representative_pool = [
        entry
        for entry in entries
        if entry["revision_id"] not in contrast_ids
        and entry["revision_id"] not in risk_selected_ids
    ]
    representative_target = size - len(contrast) - len(risk_selected)
    representative_selected = _select_bucket(
        representative_pool, representative_target, selected, constraints, rng
    )
    selected.extend(representative_selected)

    if len(selected) != size:
        raise ValidationError(
            f"cannot build a {size}-entry pilot sample: only "
            f"{len(selected)} entries are available"
        )

    counts = _constraint_counts(selected, constraints)
    unmet = []
    for constraint in constraints:
        count = counts[constraint["id"]]
        if constraint.get("mode") == "each":
            for value in constraint["values"]:
                if count[value] < constraint["min"]:
                    unmet.append(
                        {
                            "id": constraint["id"],
                            "value": value,
                            "description": constraint.get("description", ""),
                            "target_min": constraint["min"],
                            "actual": count[value],
                        }
                    )
        elif count < constraint["min"]:
            unmet.append(
                {
                    "id": constraint["id"],
                    "description": constraint.get("description", ""),
                    "target_min": constraint["min"],
                    "actual": count,
                }
            )

    bucket_counts = Counter(
        [
            "contrast"
            if entry["revision_id"] in contrast_ids
            else "risk-enriched"
            if entry["revision_id"] in risk_selected_ids
            else "representative"
            for entry in selected
        ]
    )
    ordered = sorted(
        selected, key=lambda entry: (entry["unit_id"], entry["revision_id"])
    )

    items = _build_sample_items(
        entries=entries,
        ordered=ordered,
        contrast_ids=contrast_ids,
        risk_selected_ids=risk_selected_ids,
        contrast_group_of=contrast_group_of,
        contrast=contrast,
        qpolicy=qpolicy,
    )

    identity = {
        "schema_version": 1,
        "quality_contract": SAMPLE_CONTRACT,
        "seed": seed,
        "size": size,
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "inventory_sha256": inventory_info["inventory_sha256"],
        "bucket_targets": bucket_targets,
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "revisions": [
            {"revision_id": item["revision_id"], "bucket": item["bucket"]}
            for item in items
        ],
    }
    sample_id = _canonical_sha256(identity)
    sample: dict[str, Any] = {
        **identity,
        "sample_id": sample_id,
        "unmet_constraints": unmet,
        "coverage": counts,
        "items": items,
    }
    return sample


def _build_sample_items(
    *,
    entries: list[dict[str, Any]],
    ordered: list[dict[str, Any]],
    contrast_ids: set[str],
    risk_selected_ids: set[str],
    contrast_group_of: dict[str, str],
    contrast: list[dict[str, Any]],
    qpolicy: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build the bounded context-packet items shared by sample and dry-run."""
    neighbors_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        neighbors_index[entry["component"]].append(entry)
    for component in neighbors_index:
        neighbors_index[component].sort(
            key=lambda entry: (
                entry["occurrences"][0]["logical_path"],
                entry["occurrences"][0]["line"]
                if entry["occurrences"][0]["line"] is not None
                else -1,
                entry["occurrences"][0]["ordinal"],
            )
        )
    limit = int(qpolicy.get("context_neighbor_limit", 2))
    items: list[dict[str, Any]] = []
    for index, entry in enumerate(ordered):
        revision_id = entry["revision_id"]
        bucket = (
            "contrast"
            if revision_id in contrast_ids
            else "risk-enriched"
            if revision_id in risk_selected_ids
            else "representative"
        )
        neighbors: list[dict[str, Any]] = []
        if entry["profile_confidence"] != "high":
            same = neighbors_index[entry["component"]]
            try:
                position = same.index(entry)
            except ValueError:
                position = -1
            if position >= 0:
                for neighbor in same[max(0, position - limit) : position]:
                    neighbors.append(
                        {
                            "component": neighbor["component"],
                            "section": neighbor["section"],
                            "source": neighbor["source"],
                            "target": neighbor["target"],
                            "source_tag": neighbor["source_tag"],
                        }
                    )
                for neighbor in same[position + 1 : position + 1 + limit]:
                    neighbors.append(
                        {
                            "component": neighbor["component"],
                            "section": neighbor["section"],
                            "source": neighbor["source"],
                            "target": neighbor["target"],
                            "source_tag": neighbor["source_tag"],
                        }
                    )
        items.append(
            {
                "index": index,
                "bucket": bucket,
                "contrast_group": contrast_group_of.get(revision_id),
                "contrast_siblings": [
                    member["revision_id"]
                    for member in contrast
                    if member["revision_id"] in contrast_group_of
                    and contrast_group_of[member["revision_id"]]
                    == contrast_group_of.get(revision_id)
                    and member["revision_id"] != revision_id
                ],
                "revision_id": revision_id,
                "unit_id": entry["unit_id"],
                "component": entry["component"],
                "section": entry["section"],
                "source": entry["source"],
                "target": entry["target"],
                "source_tag": entry["source_tag"],
                "args_order": entry["args_order"],
                "special": entry["special"],
                "profile": entry["profile"],
                "profile_confidence": entry["profile_confidence"],
                "domain_hints": entry["domain_hints"],
                "relevant_terms": entry["relevant_terms"],
                "structure": entry["structure"],
                "gate_signals": entry["gate_signals"],
                "risk_flags": entry["risk_flags"],
                "source_length_bin": entry["source_length_bin"],
                "context_neighbors": neighbors,
            }
        )
    return items


def generate_dry_run(
    manifest: Manifest, inventory_path: Path
) -> dict[str, Any]:
    """12 rubric try-out items that never enter the official pilot sample.

    The official 120-item sample is regenerated with its fixed seed and its
    revision ids are excluded, so dry-run items are always disjoint from it.
    """
    qpolicy = load_quality_policy(manifest)
    taxonomy = load_taxonomy(manifest)
    dry = qpolicy["dry_run"]
    entries, inventory_info = read_inventory_file(inventory_path)
    for entry in entries:
        entry["_features"] = _entry_features(entry, qpolicy)
    constraints = dry.get("coverage_constraints", [])
    target = int(dry["size"])

    official = generate_sample(manifest, inventory_path)
    official_ids = {item["revision_id"] for item in official["items"]}
    pool = [entry for entry in entries if entry["revision_id"] not in official_ids]
    by_revision = {entry["revision_id"]: entry for entry in pool}

    rng = random.Random(dry["seed"])
    contrast_ids: set[str] = set()
    contrast_group_of: dict[str, str] = {}
    contrast: list[dict[str, Any]] = []
    groups = _contrast_groups(pool, qpolicy)
    group_order = list(groups)
    rng.shuffle(group_order)
    for group_id, members in group_order:
        if len(members) > 4:
            continue
        for member in members:
            contrast_ids.add(member["revision_id"])
            contrast_group_of[member["revision_id"]] = group_id
            contrast.append(member)
        break

    selected: list[dict[str, Any]] = list(contrast)
    remaining_pool = [entry for entry in pool if entry["revision_id"] not in contrast_ids]
    filled = _select_bucket(remaining_pool, target - len(contrast), selected, constraints, rng)
    selected.extend(filled)
    if len(selected) != target:
        raise ValidationError(
            f"cannot build a {target}-item dry-run: only {len(selected)} items available"
        )

    counts = _constraint_counts(selected, constraints)
    unmet = []
    for constraint in constraints:
        count = counts[constraint["id"]]
        if constraint.get("mode") == "each":
            for value in constraint["values"]:
                if count[value] < constraint["min"]:
                    unmet.append(
                        {
                            "id": constraint["id"],
                            "value": value,
                            "description": constraint.get("description", ""),
                            "target_min": constraint["min"],
                            "actual": count[value],
                        }
                    )
        elif count < constraint["min"]:
            unmet.append(
                {
                    "id": constraint["id"],
                    "description": constraint.get("description", ""),
                    "target_min": constraint["min"],
                    "actual": count,
                }
            )

    ordered = sorted(selected, key=lambda entry: (entry["unit_id"], entry["revision_id"]))
    items = _build_sample_items(
        entries=pool,
        ordered=ordered,
        contrast_ids=contrast_ids,
        risk_selected_ids=set(),
        contrast_group_of=contrast_group_of,
        contrast=contrast,
        qpolicy=qpolicy,
    )
    identity = {
        "schema_version": 1,
        "quality_contract": dry["contract"],
        "seed": dry["seed"],
        "size": target,
        "official_sample_id": official["sample_id"],
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "inventory_sha256": inventory_info["inventory_sha256"],
        "revisions": [
            {"revision_id": item["revision_id"], "bucket": item["bucket"]}
            for item in items
        ],
    }
    sample_id = _canonical_sha256(identity)
    return {
        **identity,
        "sample_id": sample_id,
        "coverage": counts,
        "unmet_constraints": unmet,
        "items": items,
    }


def run_dry_run(manifest: Manifest, inventory_path: Path) -> dict[str, Any]:
    dry_run = generate_dry_run(manifest, inventory_path)
    qpolicy = load_quality_policy(manifest)
    run_directory = create_quality_run_directory(manifest.root, "dry-run")
    dry_run_path = run_directory / "dry-run.json"
    write_json(dry_run_path, dry_run)
    items = dry_run.pop("items")
    templates = []
    for evaluator_id in qpolicy["pilot"]["evaluator_ids"]:
        templates.append(
            {
                "schema_version": 1,
                "quality_contract": ASSESSMENT_CONTRACT,
                "sample_id": dry_run["sample_id"],
                "evaluator": {
                    "kind": "human",
                    "id": evaluator_id,
                    "method_version": qpolicy["pilot"]["method_version"],
                },
                "items": [
                    {
                        "revision_id": item["revision_id"],
                        "context_sufficient": None,
                        "profile_confirmed": None,
                        "findings": [],
                        "reuse_recommendation": None,
                    }
                    for item in items
                ],
            }
        )
    template_paths = []
    for template in templates:
        name = f"assessment-template-{template['evaluator']['id']}.json"
        write_json(run_directory / name, template)
        template_paths.append(name)
    dry_run["items"] = items
    manifest_report = {
        "schema_version": 1,
        "quality_contract": dry_run["quality_contract"],
        "sample_id": dry_run["sample_id"],
        "official_sample_id": dry_run["official_sample_id"],
        "seed": dry_run["seed"],
        "size": dry_run["size"],
        "coverage": dry_run["coverage"],
        "unmet_constraints": dry_run["unmet_constraints"],
        "dry_run": os_path_relative(dry_run_path, manifest),
        "assessment_templates": [
            os_path_relative(run_directory / name, manifest) for name in template_paths
        ],
        "run_directory": os_path_relative(run_directory, manifest),
    }
    write_json(run_directory / "dry-run-manifest.json", manifest_report)
    dry_run["dry_run_path"] = os_path_relative(dry_run_path, manifest)
    dry_run["run_directory"] = os_path_relative(run_directory, manifest)
    return dry_run


def run_sample(
    manifest: Manifest,
    inventory_path: Path,
    size: int | None = None,
    seed: str | None = None,
) -> dict[str, Any]:
    sample = generate_sample(manifest, inventory_path, size=size, seed=seed)
    qpolicy = load_quality_policy(manifest)
    run_directory = create_quality_run_directory(manifest.root, "sample")
    sample_path = run_directory / "sample.json"
    write_json(sample_path, sample)
    items = sample.pop("items")
    template_a = {
        "schema_version": 1,
        "quality_contract": ASSESSMENT_CONTRACT,
        "sample_id": sample["sample_id"],
        "evaluator": {
            "kind": "human",
            "id": qpolicy["pilot"]["evaluator_ids"][0],
            "method_version": qpolicy["pilot"]["method_version"],
        },
        "items": [
            {
                "revision_id": item["revision_id"],
                "context_sufficient": None,
                "profile_confirmed": None,
                "findings": [],
                "reuse_recommendation": None,
            }
            for item in items
        ],
    }
    template_b = {
        **template_a,
        "evaluator": {
            **template_a["evaluator"],
            "id": qpolicy["pilot"]["evaluator_ids"][1],
        },
    }
    write_json(run_directory / "assessment-template-a.json", template_a)
    write_json(run_directory / "assessment-template-b.json", template_b)
    manifest_report = {
        "schema_version": 1,
        "quality_contract": SAMPLE_CONTRACT,
        "sample_id": sample["sample_id"],
        "seed": sample["seed"],
        "size": sample["size"],
        "bucket_counts": sample["bucket_counts"],
        "unmet_constraints": sample["unmet_constraints"],
        "coverage": sample["coverage"],
        "sample": os_path_relative(sample_path, manifest),
        "assessment_template_a": os_path_relative(
            run_directory / "assessment-template-a.json", manifest
        ),
        "assessment_template_b": os_path_relative(
            run_directory / "assessment-template-b.json", manifest
        ),
        "run_directory": os_path_relative(run_directory, manifest),
    }
    write_json(run_directory / "sample-manifest.json", manifest_report)
    sample["items"] = items
    sample["sample_path"] = os_path_relative(sample_path, manifest)
    sample["run_directory"] = os_path_relative(run_directory, manifest)
    return sample


# ---------------------------------------------------------------------------
# M4/M5 support: strict validation
# ---------------------------------------------------------------------------


def _check_path_safety(value: Any, errors: list[str], where: str) -> None:
    if isinstance(value, str):
        if HOST_ABSOLUTE_PATH_RE.search(value) or WINDOWS_PATH_RE.search(value):
            errors.append(f"{where}: contains a host absolute path")
        if DOTDOT_PATH_RE.search(value):
            errors.append(f"{where}: contains a '..' path segment")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _check_path_safety(item, errors, f"{where}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _check_path_safety(item, errors, f"{where}.{key}")


def _check_unknown_fields(
    value: dict[str, Any],
    allowed: set[str],
    errors: list[str],
    where: str,
    strict: bool,
) -> None:
    if not strict:
        return
    unknown = set(value) - allowed
    if unknown:
        errors.append(f"{where}: unknown fields {sorted(unknown)}")


def _load_assessment(
    path: Path, sample: dict[str, Any], evaluator_seen: set[str], strict: bool
) -> tuple[dict[str, Any] | None, list[str]]:
    data = _read_json(path, "quality assessment")
    errors: list[str] = []
    _check_unknown_fields(
        data,
        {"schema_version", "quality_contract", "sample_id", "evaluator", "items"},
        errors,
        str(path),
        strict,
    )
    if data.get("quality_contract") != ASSESSMENT_CONTRACT:
        errors.append(f"{path}: unsupported assessment contract")
    if data.get("schema_version") != 1:
        errors.append(f"{path}: unsupported assessment schema")
    if data.get("sample_id") != sample["sample_id"]:
        errors.append(f"{path}: sample_id does not match the sample")
    evaluator = data.get("evaluator")
    if not isinstance(evaluator, dict) or not isinstance(evaluator.get("id"), str):
        errors.append(f"{path}: evaluator.id is required")
    else:
        _check_unknown_fields(
            evaluator,
            {
                "kind",
                "id",
                "method_version",
                "provider",
                "model",
                "thinking",
                "prompt_sha256",
                "bundle_id",
            },
            errors,
            f"{path}.evaluator",
            strict,
        )
        if evaluator["id"] in evaluator_seen:
            errors.append(f"{path}: duplicate evaluator id {evaluator['id']!r}")
        evaluator_seen.add(evaluator["id"])
        if evaluator.get("kind") not in ("human", "model"):
            errors.append(f"{path}: evaluator.kind must be human or model")
        if not isinstance(evaluator.get("method_version"), str):
            errors.append(f"{path}: evaluator.method_version is required")
    _check_path_safety(data, errors, str(path))
    return (data if not errors else None), errors


def _validate_assessment_items(
    assessment: dict[str, Any],
    sample: dict[str, Any],
    taxonomy: dict[str, Any],
    strict: bool,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    evaluator = assessment["evaluator"]
    errors_out: list[str] = []
    sample_revisions = {item["revision_id"] for item in sample["items"]}
    items = assessment.get("items")
    if not isinstance(items, list):
        raise ValidationError(f"assessment {evaluator['id']}: items must be an array")
    valid_codes = {code["code"] for code in taxonomy["error_codes"]}
    valid_severities = {severity["id"] for severity in taxonomy["severities"]}
    valid_profiles = {profile["id"] for profile in taxonomy["profiles"]}
    valid_reuse = {scope["id"] for scope in taxonomy["reuse_scopes"]}
    seen_revisions: set[str] = set()
    seen_findings: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        where = f"assessment {evaluator['id']} items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: not an object")
            continue
        _check_unknown_fields(
            item,
            {
                "revision_id", "context_sufficient", "profile_confirmed",
                "findings", "reuse_recommendation",
            },
            errors,
            where,
            strict,
        )
        revision_id = item.get("revision_id")
        if not isinstance(revision_id, str) or not re.fullmatch(r"[0-9a-f]{64}", revision_id):
            errors.append(f"{where}: invalid revision_id")
            continue
        if revision_id not in sample_revisions:
            errors.append(f"{where}: unknown revision_id")
            continue
        if revision_id in seen_revisions:
            errors.append(f"{where}: duplicate revision_id")
        seen_revisions.add(revision_id)
        if not isinstance(item.get("context_sufficient"), bool):
            errors.append(f"{where}: context_sufficient must be a boolean")
        profile_confirmed = item.get("profile_confirmed")
        if profile_confirmed is not None and profile_confirmed not in valid_profiles:
            errors.append(f"{where}: unknown profile {profile_confirmed!r}")
        reuse = item.get("reuse_recommendation")
        if reuse is not None and reuse not in valid_reuse:
            errors.append(f"{where}: unknown reuse scope {reuse!r}")
        findings = item.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{where}: findings must be an array")
            findings = []
        normalized_findings: list[dict[str, Any]] = []
        for finding_index, finding in enumerate(findings):
            fwhere = f"{where}.findings[{finding_index}]"
            if not isinstance(finding, dict):
                errors.append(f"{fwhere}: not an object")
                continue
            _check_unknown_fields(
                finding,
                {
                    "finding_id", "error_code", "severity", "source_span",
                    "target_span", "body", "evidence_refs",
                },
                errors,
                fwhere,
                strict,
            )
            finding_id = finding.get("finding_id")
            if not isinstance(finding_id, str) or not finding_id:
                errors.append(f"{fwhere}: finding_id is required")
            elif finding_id in seen_findings:
                errors.append(f"{fwhere}: duplicate finding_id {finding_id!r}")
            else:
                seen_findings.add(finding_id)
            code = finding.get("error_code")
            if code not in valid_codes:
                errors.append(f"{fwhere}: unknown error code {code!r}")
            severity = finding.get("severity")
            if severity not in valid_severities:
                errors.append(f"{fwhere}: unknown severity {severity!r}")
            for field in ("source_span", "target_span", "body"):
                if not isinstance(finding.get(field), str):
                    errors.append(f"{fwhere}: {field} must be a string")
            evidence = finding.get("evidence_refs")
            if not isinstance(evidence, list) or not all(
                isinstance(value, str) for value in evidence
            ):
                errors.append(f"{fwhere}: evidence_refs must be a string array")
            else:
                for ref in evidence:
                    if (
                        HOST_ABSOLUTE_PATH_RE.search(ref)
                        or WINDOWS_PATH_RE.search(ref)
                        or DOTDOT_PATH_RE.search(ref)
                    ):
                        errors.append(f"{fwhere}: unsafe evidence ref")
            normalized_findings.append(
                {
                    "finding_id": finding_id,
                    "error_code": code,
                    "severity": severity,
                    "source_span": finding.get("source_span", ""),
                    "target_span": finding.get("target_span", ""),
                    "body": finding.get("body", ""),
                    "evidence_refs": finding.get("evidence_refs", []),
                }
            )
        normalized.append(
            {
                "revision_id": revision_id,
                "context_sufficient": item.get("context_sufficient"),
                "profile_confirmed": profile_confirmed,
                "reuse_recommendation": reuse,
                "findings": normalized_findings,
            }
        )
    if seen_revisions != sample_revisions:
        missing = sorted(sample_revisions - seen_revisions)
        extra = sorted(seen_revisions - sample_revisions)
        if missing:
            errors.append(
                f"assessment {evaluator['id']}: incomplete coverage "
                f"({len(missing)} missing revisions)"
            )
        if extra:
            errors.append(f"assessment {evaluator['id']}: extra revisions {extra}")
    return {
        "evaluator_id": evaluator["id"],
        "evaluator": evaluator,
        "items": normalized,
    }, errors


def _validate_adjudication(
    adjudication: dict[str, Any],
    sample: dict[str, Any],
    assessments: list[dict[str, Any]],
    taxonomy: dict[str, Any],
    qpolicy: dict[str, Any],
    strict: bool,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    _check_unknown_fields(
        adjudication,
        {"schema_version", "quality_contract", "sample_id", "items"},
        errors,
        "adjudication",
        strict,
    )
    if adjudication.get("quality_contract") != ADJUDICATION_CONTRACT:
        errors.append("unsupported adjudication contract")
    if adjudication.get("schema_version") != 1:
        errors.append("unsupported adjudication schema")
    if adjudication.get("sample_id") != sample["sample_id"]:
        errors.append("adjudication sample_id does not match the sample")
    _check_path_safety(adjudication, errors, "adjudication")
    sample_by_revision = {item["revision_id"]: item for item in sample["items"]}
    sample_revisions = set(sample_by_revision)
    evaluator_ids = {assessment["evaluator_id"] for assessment in assessments}
    findings_by_evaluator: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for assessment in assessments:
        findings_by_evaluator[assessment["evaluator_id"]] = {
            item["revision_id"]: item["findings"] for item in assessment["items"]
        }
    valid_codes = {code["code"] for code in taxonomy["error_codes"]}
    valid_severities = {severity["id"] for severity in taxonomy["severities"]}
    valid_reuse = {scope["id"] for scope in taxonomy["reuse_scopes"]}
    valid_confidence = {level["id"] for level in taxonomy["confidence_levels"]}
    valid_grades = {grade["id"] for grade in taxonomy["grades"]}
    valid_states = {"confirmed", "partially_confirmed", "rejected", "resolved"}
    valid_vector = set(taxonomy["quality_vector_dimensions"])
    items = adjudication.get("items")
    if not isinstance(items, list):
        raise ValidationError("adjudication items must be an array")
    seen_revisions: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        where = f"adjudication items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: not an object")
            continue
        _check_unknown_fields(
            item,
            {
                "revision_id", "assessment_ids", "context_sufficient",
                "resolved_findings", "quality_vector", "confidence",
                "provisional_grade", "reuse_scope", "rationale",
            },
            errors,
            where,
            strict,
        )
        revision_id = item.get("revision_id")
        if not isinstance(revision_id, str) or not re.fullmatch(r"[0-9a-f]{64}", revision_id):
            errors.append(f"{where}: invalid revision_id")
            continue
        if revision_id not in sample_revisions:
            errors.append(f"{where}: unknown revision_id")
            continue
        if revision_id in seen_revisions:
            errors.append(f"{where}: duplicate revision_id")
        seen_revisions.add(revision_id)
        sample_item = sample_by_revision[revision_id]
        assessment_ids = item.get("assessment_ids")
        if not isinstance(assessment_ids, list) or not assessment_ids:
            errors.append(f"{where}: assessment_ids must be a non-empty array")
        else:
            unknown = [value for value in assessment_ids if value not in evaluator_ids]
            if unknown:
                errors.append(f"{where}: references unknown assessments {unknown}")
        if not isinstance(item.get("context_sufficient"), bool):
            errors.append(f"{where}: context_sufficient must be a boolean")
        vector = item.get("quality_vector")
        if not isinstance(vector, dict):
            errors.append(f"{where}: quality_vector must be an object")
        else:
            _check_unknown_fields(vector, set(valid_vector), errors, f"{where}.quality_vector", strict)
            for dimension, value in vector.items():
                if value is not None and (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value < 0
                    or value > 4
                ):
                    errors.append(
                        f"{where}.quality_vector.{dimension}: must be 0-4 or null"
                    )
        confidence = item.get("confidence")
        if confidence not in valid_confidence:
            errors.append(f"{where}: unknown confidence {confidence!r}")
        grade = item.get("provisional_grade")
        if grade not in valid_grades:
            errors.append(f"{where}: unknown grade {grade!r}")
        reuse_scope = item.get("reuse_scope")
        if reuse_scope not in valid_reuse:
            errors.append(f"{where}: unknown reuse scope {reuse_scope!r}")
        if not isinstance(item.get("rationale"), str):
            errors.append(f"{where}: rationale must be a string")
        resolved = item.get("resolved_findings")
        if not isinstance(resolved, list):
            errors.append(f"{where}: resolved_findings must be an array")
            resolved = []
        has_confirmed_major = False
        for finding_index, finding in enumerate(resolved):
            fwhere = f"{where}.resolved_findings[{finding_index}]"
            if not isinstance(finding, dict):
                errors.append(f"{fwhere}: not an object")
                continue
            _check_unknown_fields(
                finding,
                {
                    "finding_id", "evaluator_id", "error_code", "severity",
                    "state", "body", "rationale",
                },
                errors,
                fwhere,
                strict,
            )
            finding_id = finding.get("finding_id")
            evaluator_id = finding.get("evaluator_id")
            state = finding.get("state")
            if state not in valid_states:
                errors.append(f"{fwhere}: unknown state {state!r}")
            code = finding.get("error_code")
            if code not in valid_codes:
                errors.append(f"{fwhere}: unknown error code {code!r}")
            severity = finding.get("severity")
            if severity not in valid_severities:
                errors.append(f"{fwhere}: unknown severity {severity!r}")
            if severity in ("blocker", "major") and state in (
                "confirmed", "partially_confirmed"
            ):
                has_confirmed_major = True
            if not isinstance(finding.get("body"), str):
                errors.append(f"{fwhere}: body must be a string")
            if isinstance(evaluator_id, str) and isinstance(finding_id, str):
                pool = findings_by_evaluator.get(evaluator_id, {}).get(revision_id, [])
                if not any(
                    existing.get("finding_id") == finding_id for existing in pool
                ):
                    errors.append(
                        f"{fwhere}: finding_id {finding_id!r} does not exist in "
                        f"assessment {evaluator_id!r} for this revision"
                    )
        context_sufficient = item.get("context_sufficient") is True
        if grade == "Gold":
            if not context_sufficient:
                errors.append(f"{where}: Gold requires sufficient context")
            if confidence not in ("C2", "C3", "C4"):
                errors.append(f"{where}: Gold requires confidence C2 or above")
            if has_confirmed_major:
                errors.append(
                    f"{where}: Gold is not allowed with a confirmed "
                    f"blocker/major finding"
                )
            gates = sample_item.get("gate_signals", {})
            if gates.get("empty_target") is True:
                errors.append(f"{where}: Gold is not allowed for an empty target")
            if gates.get("format_signature_match") is False:
                errors.append(f"{where}: Gold is not allowed with a format mismatch")
            if gates.get("markup_multiset_match") is False:
                errors.append(f"{where}: Gold is not allowed with a markup mismatch")
            if gates.get("at_token_multiset_match") is False:
                errors.append(f"{where}: Gold is not allowed with a token mismatch")
            if gates.get("runtime_collision") is True:
                errors.append(f"{where}: Gold is not allowed with a runtime collision")
        elif grade == "Silver":
            if has_confirmed_major:
                errors.append(
                    f"{where}: Silver is not allowed with a confirmed "
                    f"blocker/major finding"
                )
            if confidence not in ("C2", "C3", "C4"):
                errors.append(f"{where}: Silver requires confidence C2 or above")
            gates = sample_item.get("gate_signals", {})
            if gates.get("empty_target") is True:
                errors.append(f"{where}: Silver is not allowed for an empty target")
            if gates.get("format_signature_match") is False:
                errors.append(f"{where}: Silver is not allowed with a format mismatch")
        normalized.append(
            {
                "revision_id": revision_id,
                "assessment_ids": assessment_ids,
                "context_sufficient": item.get("context_sufficient"),
                "resolved_findings": resolved,
                "quality_vector": vector,
                "confidence": confidence,
                "provisional_grade": grade,
                "reuse_scope": reuse_scope,
                "rationale": item.get("rationale", ""),
            }
        )
    if seen_revisions != sample_revisions:
        missing = sorted(sample_revisions - seen_revisions)
        if missing:
            errors.append(f"adjudication: incomplete coverage ({len(missing)} missing)")
    return {"items": normalized}, errors


def _load_sample_file(path: Path) -> dict[str, Any]:
    sample = _read_json(path, "quality sample")
    errors: list[str] = []
    if sample.get("quality_contract") != SAMPLE_CONTRACT:
        errors.append(f"{path}: unsupported sample contract")
    if sample.get("schema_version") != 1:
        errors.append(f"{path}: unsupported sample schema")
    items = sample.get("items")
    if not isinstance(items, list) or not items:
        errors.append(f"{path}: sample items are invalid or empty")
    _check_path_safety(sample, errors, str(path))
    if errors:
        raise ValidationError("; ".join(errors))
    sample_id = sample.get("sample_id")
    if not isinstance(sample_id, str) or not sample_id:
        raise ValidationError(f"{path}: sample has no sample_id")
    return sample


def validate_quality_run(
    manifest: Manifest,
    sample_path: Path,
    assessment_paths: list[Path],
    adjudication_path: Path,
    strict: bool | None = None,
) -> dict[str, Any]:
    taxonomy = load_taxonomy(manifest)
    qpolicy = load_quality_policy(manifest)
    # policy-v1 declares strict unknown-field behavior; the CLI --strict flag
    # overrides it, but the policy default applies when the flag is absent.
    if strict is None:
        strict = bool(qpolicy.get("strict_unknown_fields", False))
    sample = _load_sample_file(sample_path)
    sample_revisions = {item["revision_id"] for item in sample["items"]}
    revision_ids = [item["revision_id"] for item in sample["items"]]
    if len(revision_ids) != len(set(revision_ids)):
        raise ValidationError(f"{sample_path}: duplicate revision_id in sample")
    if not assessment_paths:
        raise ValidationError("at least one --assessment is required")
    if len(assessment_paths) > 2:
        raise ValidationError("pilot validation accepts at most two assessments")
    evaluator_seen: set[str] = set()
    assessments: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in assessment_paths:
        assessment, load_errors = _load_assessment(
            path, sample, evaluator_seen, strict
        )
        errors.extend(load_errors)
        if assessment is None:
            continue
        normalized, item_errors = _validate_assessment_items(
            assessment, sample, taxonomy, strict
        )
        errors.extend(item_errors)
        assessments.append(normalized)
    adjudication = _read_json(adjudication_path, "quality adjudication")
    normalized_adjudication: dict[str, Any] = {"items": []}
    try:
        normalized_adjudication, adjudication_errors = _validate_adjudication(
            adjudication, sample, assessments, taxonomy, qpolicy, strict
        )
        errors.extend(adjudication_errors)
    except ValidationError as error:
        errors.append(str(error))

    normalized_assessments = [
        {
            "evaluator_id": assessment["evaluator_id"],
            "evaluator": assessment["evaluator"],
            "items": assessment["items"],
        }
        for assessment in assessments
    ]
    validation = {
        "schema_version": 1,
        "quality_contract": VALIDATION_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "sample_id": sample["sample_id"],
        "strict": strict,
        "taxonomy_sha256": _canonical_sha256(taxonomy),
        "policy_sha256": _canonical_sha256(qpolicy),
        "errors": errors,
        "warnings": [],
        "sample": sample,
        "assessments": normalized_assessments,
        "adjudication": normalized_adjudication,
    }
    validation["ok"] = not errors
    return validation


def run_validation(
    manifest: Manifest,
    sample_path: Path,
    assessment_paths: list[Path],
    adjudication_path: Path,
    strict: bool,
) -> dict[str, Any]:
    validation = validate_quality_run(
        manifest, sample_path, assessment_paths, adjudication_path, strict
    )
    run_directory = create_quality_run_directory(manifest.root, "validation")
    _write_jsonl(
        run_directory / "normalized-assessments.jsonl",
        validation["assessments"],
    )
    _write_jsonl(
        run_directory / "normalized-adjudications.jsonl",
        validation["adjudication"].get("items", []),
    )
    write_json(run_directory / "validation.json", validation)
    summary = {
        "ok": validation["ok"],
        "strict": validation["strict"],
        "sample_id": validation["sample_id"],
        "errors": validation["errors"],
        "warnings": validation["warnings"],
        "assessments": [
            {
                "evaluator_id": assessment["evaluator_id"],
                "kind": assessment["evaluator"].get("kind"),
                "items": len(assessment["items"]),
            }
            for assessment in validation["assessments"]
        ],
        "run_directory": os_path_relative(run_directory, manifest),
        "validation_path": os_path_relative(
            run_directory / "validation.json", manifest
        ),
    }
    return summary


# ---------------------------------------------------------------------------
# M5/M6 support: report
# ---------------------------------------------------------------------------


def _profile_disagreements(
    sample: dict[str, Any], assessments: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Automatic inventory profile vs confirmed evaluator profile."""
    auto_by_revision = {
        item["revision_id"]: item.get("profile") for item in sample["items"]
    }
    by_evaluator = {
        assessment["evaluator_id"]: {
            item["revision_id"]: item for item in assessment["items"]
        }
        for assessment in assessments
    }
    disagreements: list[dict[str, Any]] = []
    for revision_id in sorted(auto_by_revision):
        auto_profile = auto_by_revision[revision_id]
        for evaluator_id, items in sorted(by_evaluator.items()):
            item = items.get(revision_id)
            if not item:
                continue
            confirmed = item.get("profile_confirmed")
            if confirmed is not None and confirmed != auto_profile:
                disagreements.append(
                    {
                        "revision_id": revision_id,
                        "auto_profile": auto_profile,
                        "confirmed_profile": confirmed,
                        "evaluator_id": evaluator_id,
                    }
                )
    return disagreements


def _span_overlap(left: str, right: str) -> bool:
    if not left or not right:
        return True
    if ":" in left and ":" in right:
        try:
            left_start, left_end = (int(part) for part in left.split(":", 1))
            right_start, right_end = (int(part) for part in right.split(":", 1))
            return left_start <= right_end and right_start <= left_end
        except ValueError:
            pass
    return left in right or right in left


def _match_findings(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
    mergeable: set[tuple[str, str]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    used: set[str] = set()
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for left_finding in left:
        best: dict[str, Any] | None = None
        for right_finding in right:
            if right_finding["finding_id"] in used:
                continue
            if left_finding["error_code"] != right_finding["error_code"]:
                pair = tuple(
                    sorted(
                        (left_finding["error_code"], right_finding["error_code"])
                    )
                )
                if pair not in mergeable:
                    continue
            if not _span_overlap(
                left_finding.get("source_span", ""),
                right_finding.get("source_span", ""),
            ):
                continue
            if not _span_overlap(
                left_finding.get("target_span", ""),
                right_finding.get("target_span", ""),
            ):
                continue
            best = right_finding
            break
        if best is not None:
            used.add(best["finding_id"])
            matches.append((left_finding, best))
    return matches


def _weighted_kappa(
    left: list[int], right: list[int], levels: int
) -> float | None:
    if len(left) != len(right) or not left:
        return None
    weight = [
        [1.0 - abs(i - j) / max(1, levels - 1) for j in range(levels)]
        for i in range(levels)
    ]
    observed = sum(weight[a][b] for a, b in zip(left, right)) / len(left)
    left_counts = Counter(left)
    right_counts = Counter(right)
    expected = sum(
        left_counts[i] * right_counts[j] * weight[i][j]
        for i in range(levels)
        for j in range(levels)
    ) / (len(left) * len(left))
    if expected >= 1.0:
        return 1.0 if observed >= 1.0 else 0.0
    return (observed - expected) / (1.0 - expected)


def build_report(
    validation: dict[str, Any], taxonomy: dict[str, Any]
) -> dict[str, Any]:
    sample = validation["sample"]
    assessments = validation["assessments"]
    adjudication = validation["adjudication"]
    items = sample["items"]
    size = len(items)
    severity_levels = ["none", "note", "minor", "major", "blocker"]
    mergeable = {
        tuple(sorted(pair)) for pair in taxonomy.get("mergeable_codes", [])
    }
    valid_codes = {code["code"] for code in taxonomy["error_codes"]}
    report: dict[str, Any] = {"sample_id": validation["sample_id"], "size": size}

    report["assessments"] = []
    for assessment in assessments:
        findings = sum(len(item["findings"]) for item in assessment["items"])
        report["assessments"].append(
            {
                "evaluator_id": assessment["evaluator_id"],
                "kind": assessment["evaluator"].get("kind"),
                "method_version": assessment["evaluator"].get("method_version"),
                "items": len(assessment["items"]),
                "findings": findings,
                "complete": len(assessment["items"]) == size,
            }
        )
    if len(assessments) < 2:
        report["agreement"] = {
            "note": "at least two assessments are required for agreement metrics"
        }
        report["distributions"] = {}
        report["calibration"] = {}
        return report

    left = assessments[0]
    right = assessments[1]
    left_by_revision = {item["revision_id"]: item for item in left["items"]}
    right_by_revision = {item["revision_id"]: item for item in right["items"]}
    adjudication_by_revision = {
        item["revision_id"]: item for item in adjudication["items"]
    }

    def substantive(item: dict[str, Any]) -> bool:
        return any(
            finding["severity"] != "note" for finding in item["findings"]
        )

    def major_or_worse(item: dict[str, Any]) -> bool:
        return any(
            finding["severity"] in ("major", "blocker")
            for finding in item["findings"]
        )

    def max_severity(item: dict[str, Any]) -> int:
        order = {name: index for index, name in enumerate(severity_levels)}
        severities = [finding["severity"] for finding in item["findings"]]
        if not severities:
            return order["none"]
        return max(order[severity] for severity in severities)

    context_agreement = 0
    defect_agreement = 0
    major_agreement = 0
    context_pairs = 0
    left_ratings: list[int] = []
    right_ratings: list[int] = []
    per_category: dict[str, dict[str, int]] = defaultdict(
        lambda: {"left": 0, "right": 0, "matched": 0}
    )
    for item in items:
        revision_id = item["revision_id"]
        left_item = left_by_revision[revision_id]
        right_item = right_by_revision[revision_id]
        context_pairs += 1
        if left_item["context_sufficient"] == right_item["context_sufficient"]:
            context_agreement += 1
        if substantive(left_item) == substantive(right_item):
            defect_agreement += 1
        if major_or_worse(left_item) == major_or_worse(right_item):
            major_agreement += 1
        left_ratings.append(max_severity(left_item))
        right_ratings.append(max_severity(right_item))
        left_findings = [
            finding for finding in left_item["findings"]
        ]
        right_findings = [
            finding for finding in right_item["findings"]
        ]
        matches = _match_findings(left_findings, right_findings, mergeable)
        matched_right = {match[1]["finding_id"] for match in matches}
        for finding in left_findings:
            per_category[finding["error_code"]]["left"] += 1
        for finding in right_findings:
            per_category[finding["error_code"]]["right"] += 1
        for left_finding, right_finding in matches:
            for code in {left_finding["error_code"], right_finding["error_code"]}:
                per_category[code]["matched"] += 1

    category_metrics: dict[str, dict[str, float]] = {}
    macro_f1_values: list[float] = []
    for code, counts in sorted(per_category.items()):
        precision = (
            counts["matched"] / counts["left"] if counts["left"] else 0.0
        )
        recall = (
            counts["matched"] / counts["right"] if counts["right"] else 0.0
        )
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
        category_metrics[code] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "left_findings": counts["left"],
            "right_findings": counts["right"],
            "matched": counts["matched"],
        }
        if counts["left"] or counts["right"]:
            macro_f1_values.append(f1)

    report["agreement"] = {
        "context_sufficient_agreement": (
            round(context_agreement / context_pairs, 4) if context_pairs else None
        ),
        "defect_presence_agreement": (
            round(defect_agreement / context_pairs, 4) if context_pairs else None
        ),
        "major_or_worse_agreement": (
            round(major_agreement / context_pairs, 4) if context_pairs else None
        ),
        "severity_weighted_kappa": _weighted_kappa(
            left_ratings, right_ratings, len(severity_levels)
        ),
        "category_metrics": category_metrics,
        "macro_f1": (
            round(sum(macro_f1_values) / len(macro_f1_values), 4)
            if macro_f1_values
            else None
        ),
    }

    resolved_codes: Counter[str] = Counter()
    resolved_severities: Counter[str] = Counter()
    confirmed_major = 0
    source_findings = 0
    context_insufficient = 0
    unmappable = 0
    for item in adjudication["items"]:
        for finding in item["resolved_findings"]:
            resolved_codes[finding["error_code"]] += 1
            resolved_severities[finding["severity"]] += 1
            if finding["error_code"] not in valid_codes:
                unmappable += 1
            if finding["state"] in ("confirmed", "partially_confirmed"):
                if finding["severity"] in ("blocker", "major"):
                    confirmed_major += 1
                if finding["error_code"].startswith("SOURCE_"):
                    source_findings += 1
                if finding["error_code"] == "CTX_INSUFFICIENT":
                    context_insufficient += 1
    report["distributions"] = {
        "adjudicated_findings": {
            "by_code": dict(sorted(resolved_codes.items())),
            "by_severity": dict(sorted(resolved_severities.items())),
            "confirmed_major_or_blocker": confirmed_major,
            "source_findings": source_findings,
            "context_insufficient": context_insufficient,
            "unmappable": unmappable,
        },
        "grades": dict(
            sorted(
                Counter(
                    item["provisional_grade"] for item in adjudication["items"]
                ).items()
            )
        ),
        "confidence": dict(
            sorted(
                Counter(item["confidence"] for item in adjudication["items"]).items()
            )
        ),
        "reuse_scopes": dict(
            sorted(
                Counter(item["reuse_scope"] for item in adjudication["items"]).items()
            )
        ),
        "buckets": dict(sorted(Counter(item["bucket"] for item in items).items())),
        "profiles": dict(sorted(Counter(item["profile"] for item in items).items())),
    }

    confirmed_by_revision = {
        item["revision_id"]: item
        for item in adjudication["items"]
        if any(
            finding["state"] in ("confirmed", "partially_confirmed")
            for finding in item["resolved_findings"]
        )
    }
    flag_stats: dict[str, dict[str, int]] = {}
    flagged_total: Counter[str] = Counter()
    flagged_confirmed: Counter[str] = Counter()
    confirmed_with_flag = 0
    for item in items:
        if item["revision_id"] not in confirmed_by_revision:
            continue
        flags = item.get("risk_flags", [])
        if flags:
            confirmed_with_flag += 1
        for flag in flags:
            flagged_total[flag] += 1
            flagged_confirmed[flag] += 1
    total_confirmed = len(confirmed_by_revision)
    for flag in flagged_total:
        flag_stats[flag] = {
            "flagged": flagged_total[flag],
            "with_confirmed": flagged_confirmed[flag],
        }
    report["risk_flags"] = {
        "confirmed_items": total_confirmed,
        "confirmed_with_any_flag": confirmed_with_flag,
        "coverage": (
            round(confirmed_with_flag / total_confirmed, 4)
            if total_confirmed
            else None
        ),
        "per_flag": flag_stats,
    }

    taxonomy_gaps: dict[str, Any] = {
        "profile_disagreements": _profile_disagreements(sample, assessments),
        "context_insufficient_items": [],
        "source_related_items": [],
    }
    for item in items:
        revision_id = item["revision_id"]
        adjudicated = adjudication_by_revision.get(revision_id)
        if not adjudicated:
            continue
        if any(
            finding["error_code"] == "CTX_INSUFFICIENT"
            and finding["state"] in ("confirmed", "partially_confirmed")
            for finding in adjudicated["resolved_findings"]
        ):
            taxonomy_gaps["context_insufficient_items"].append(revision_id)
        if any(
            finding["error_code"].startswith("SOURCE_")
            and finding["state"] in ("confirmed", "partially_confirmed")
            for finding in adjudicated["resolved_findings"]
        ):
            taxonomy_gaps["source_related_items"].append(revision_id)
    report["taxonomy_gaps"] = taxonomy_gaps

    target = {
        "assessment_coverage": 1.0,
        "major_or_worse_agreement": 0.90,
        "defect_presence_agreement": 0.80,
        "severity_weighted_kappa": 0.70,
        "unmappable_max_ratio": 0.05,
        "context_insufficient_max_ratio": 0.10,
    }
    agreement = report["agreement"]
    unmappable_ratio = unmappable / sum(resolved_codes.values()) if resolved_codes else 0.0
    context_ratio = context_insufficient / size if size else None
    report["calibration"] = {
        "assessment_coverage_met": all(
            assessment["complete"] for assessment in report["assessments"]
        ),
        "major_or_worse_agreement_met": (
            agreement.get("major_or_worse_agreement", 0) >= target["major_or_worse_agreement"]
            if agreement.get("major_or_worse_agreement") is not None
            else False
        ),
        "defect_presence_agreement_met": (
            agreement.get("defect_presence_agreement", 0)
            >= target["defect_presence_agreement"]
            if agreement.get("defect_presence_agreement") is not None
            else False
        ),
        "severity_weighted_kappa_met": (
            agreement.get("severity_weighted_kappa", 0) >= target["severity_weighted_kappa"]
            if agreement.get("severity_weighted_kappa") is not None
            else False
        ),
        "unmappable_ratio": unmappable_ratio,
        "unmappable_met": (
            unmappable_ratio is not None and unmappable_ratio < target["unmappable_max_ratio"]
        ),
        "context_insufficient_ratio": context_ratio,
        "context_insufficient_met": (
            context_ratio is not None
            and context_ratio < target["context_insufficient_max_ratio"]
        ),
    }
    return report




def build_report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 翻译质量试点报告",
        "",
        f"- sample_id：`{report.get('sample_id', '')}`",
        f"- 样本规模：{report.get('size', 0)}",
        "",
        "## 评估覆盖",
    ]
    for assessment in report.get("assessments", []):
        lines.append(
            f"- {assessment['evaluator_id']}（{assessment.get('kind')}）："
            f"{assessment['items']} 条 / findings {assessment['findings']}，"
            f"完整={'是' if assessment['complete'] else '否'}"
        )
    agreement = report.get("agreement", {})
    if "note" not in agreement:
        lines.extend(
            [
                "",
                "## 一致性",
                f"- context sufficient 一致率：{agreement.get('context_sufficient_agreement')}",
                f"- 实质缺陷有无一致率：{agreement.get('defect_presence_agreement')}",
                f"- major-or-worse 一致率：{agreement.get('major_or_worse_agreement')}",
                f"- severity 加权 κ：{agreement.get('severity_weighted_kappa')}",
                f"- error category macro-F1：{agreement.get('macro_f1')}",
            ]
        )
    distributions = report.get("distributions", {})
    if distributions:
        lines.extend(
            [
                "",
                "## 裁决后分布",
                f"- 错误按代码：{distributions.get('adjudicated_findings', {}).get('by_code')}",
                f"- 错误按严重程度：{distributions.get('adjudicated_findings', {}).get('by_severity')}",
                f"- 等级：{distributions.get('grades')}",
                f"- 置信度：{distributions.get('confidence')}",
                f"- 复用范围：{distributions.get('reuse_scopes')}",
            ]
        )
    risk = report.get("risk_flags", {})
    if risk:
        lines.extend(
            [
                "",
                "## 风险标志命中",
                f"- confirmed 条目数：{risk.get('confirmed_items')}，"
                f"其中至少一个 flag 命中：{risk.get('confirmed_with_any_flag')}",
                f"- flag 覆盖率：{risk.get('coverage')}",
            ]
        )
    calibration = report.get("calibration", {})
    if calibration:
        lines.extend(
            [
                "",
                "## 校准目标",
                f"- assessment 覆盖 100%：{'达成' if calibration.get('assessment_coverage_met') else '未达成'}",
                f"- major-or-worse ≥90%：{'达成' if calibration.get('major_or_worse_agreement_met') else '未达成'}",
                f"- 实质缺陷 ≥80%：{'达成' if calibration.get('defect_presence_agreement_met') else '未达成'}",
                f"- severity κ ≥0.70：{'达成' if calibration.get('severity_weighted_kappa_met') else '未达成'}",
                f"- 上下文不足 <10%：{'达成' if calibration.get('context_insufficient_met') else '未达成'}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def run_report(manifest: Manifest, validation_path: Path) -> dict[str, Any]:
    validation = _read_json(validation_path, "quality validation")
    if validation.get("quality_contract") != VALIDATION_CONTRACT:
        raise ValidationError(
            f"unsupported quality validation file: {validation_path}"
        )
    taxonomy = load_taxonomy(manifest)
    report = build_report(validation, taxonomy)
    run_directory = create_quality_run_directory(manifest.root, "report")
    write_json(run_directory / "report.json", report)
    markdown = build_report_markdown(report)
    (run_directory / "report.md").write_text(markdown, encoding="utf-8")
    report["report_path"] = os_path_relative(run_directory / "report.json", manifest)
    report["report_md"] = os_path_relative(run_directory / "report.md", manifest)
    report["run_directory"] = os_path_relative(run_directory, manifest)
    return report
