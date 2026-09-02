#!/usr/bin/env python3
"""Strict offline validator for translation_surface_screen_v1 inputs and results.

The surface screen is a review-only funnel stage: it produces per-entry
``OK|ISSUE`` observations only.  This module enforces the exact identity
policy, canonical bytes, path safety, and strict result schema of
docs/paseo-translation-surface-screen-v1-contract.md.  It never upgrades a
surface verdict into an adjudicated finding or a repair instruction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

import contextual_result_check as strict


# Surface reuses the shared strict JSON decoder and error taxonomy so that
# BOM, duplicate-key, NaN/Infinity, fence, and trailing-byte behaviour is
# identical to the contextual contracts.  Untrusted payloads cannot select a
# validator: every entry point below pins contract
# translation_surface_screen_v1 explicitly.
InputError = strict.InputError
ContractError = strict.ContractError
strict_json_bytes = strict.strict_json_bytes


CONTRACT = "translation_surface_screen_v1"
LANE_GROUP_CONTRACT = "translation_surface_screen_v1_lane_group"
IDENTITY_RULES_V2 = "production-review-v2-lite-rules-v2"
PAYLOAD_KEYS = frozenset({
    "contract", "fixed_source_identity", "terminology_snapshot",
    "rules_version", "rendered_briefing", "entries",
})
ENTRY_KEYS = frozenset({
    "component", "normalized_path", "call_locator", "source_tag", "source",
    "target", "logical_entry_identity", "entry_revision_identity",
})
SHA256 = re.compile(r"^[0-9a-f]{64}$")
# Containment form: any embedded 64-hex identity inside free-form strings.
HEX64_CONTAINS = re.compile(r"[0-9a-f]{64}")
SOURCE_IDENTITY = re.compile(r"^(?:commit:[0-9a-f]{40}|snapshot:[0-9a-f]{64})$")
# Extractor-stable revision-key grammar.  The repository extractor's
# revision keys are SHA-256 hex digests over the call identity; equivalent
# stable locators are non-empty hierarchical tokens joined by "/" or "."
# where every token is [0-9a-zA-Z_-]+ .  Anything else — a bare ordinal, a
# raw line number, or a file:line / path:line form — fails closed.
STABLE_LOCATOR = re.compile(
    r"^(?:(?=[0-9a-f]{64}$)[0-9a-f]+|(?:[0-9A-Za-z_-]+)(?:[/.][0-9A-Za-z_-]+)+)$"
)
# Raw line / file:line forms that must never be accepted as call locators,
# including embedded ":<digits>" / ":<digits>:" suffixes and L/line prefixes.
LINE_NUMBER_LIKE = re.compile(
    r"^(?:[0-9]+|line[:\s#-]?[0-9]+|l[:\s#-]?[0-9]+)$", re.IGNORECASE
)
EMBEDDED_LINE_FORM = re.compile(
    r"(?:^|[/._-])(?:line[:\s#-]?|l[:\s#-]?|:)[0-9]+(?::[0-9]+)?$", re.IGNORECASE
)
RESULT_ROOT_KEYS = frozenset({"contract", "candidate_identity", "results"})
RESULT_ITEM_OK_KEYS = frozenset({"entry_revision_identity", "verdict"})
RESULT_ITEM_ISSUE_KEYS = frozenset({
    "entry_revision_identity", "verdict", "observation",
})
PROMPT_TEMPLATE = (
    "任务：筛查 input_path 中全部冻结 entry；只报告有证据的明显错译、标记/占位符破坏、"
    "参数顺序或格式等表层问题；否则判 OK。\n"
    "输入：candidate_identity=<candidate_identity>；input_path=<input_path>。全程只读；"
    "仅读该文件、其明确引用内容及 docs/paseo-translation-surface-screen-v1-contract.md 第六节；"
    "禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n"
    "输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 entry 并回显 identity；"
    "首字节{、末字节}，无其他文字、Markdown 或围栏。"
)


def canonical_bytes(value: object) -> bytes:
    """Canonical JSON bytes: UTF-8, sorted keys, compact, no NaN."""
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise ContractError(f"value is not canonicalizable: {error}") from error


def normalize_relative_path(value: object, *, label: str = "normalized_path") -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty string")
    if "\x00" in value or "\\" in value:
        raise ContractError(f"{label} contains a forbidden separator or NUL")
    if value.startswith("/") or value.endswith("/"):
        raise ContractError(f"{label} must be a relative POSIX path without edge separators")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ContractError(f"{label} must be normalized without . or .. segments")
    return value


def is_line_number_like(value: str) -> bool:
    return bool(LINE_NUMBER_LIKE.fullmatch(value))


def validate_call_locator(value: object, *, label: str = "call_locator") -> str:
    """Positive extractor-stable grammar; line-like and file:line forms fail."""
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty string")
    if is_line_number_like(value):
        raise ContractError(f"{label} must not be a raw line number")
    if EMBEDDED_LINE_FORM.search(value):
        raise ContractError(
            f"{label} must not embed a file:line or raw line form"
        )
    if not STABLE_LOCATOR.fullmatch(value):
        raise ContractError(
            f"{label} must be an extractor-stable revision key "
            "(64-hex digest or hierarchical token path)"
        )
    return value


def reject_path_line_locator(normalized_path: str, call_locator: str) -> None:
    """Reject a call_locator that is just the entry normalized_path followed by
    a numeric line token (``<path>/<line>``, ``<path>.<line>``,
    ``<path>:<line>``): those are raw line forms in disguise.  Hierarchical
    numeric keys unrelated to the entry path stay valid."""
    for separator in ("/", ".", ":"):
        prefix = f"{normalized_path}{separator}"
        if call_locator.startswith(prefix) and call_locator[len(prefix):].isdigit():
            raise ContractError(
                "call_locator must not be the entry normalized_path followed by "
                "a raw numeric line token"
            )


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty string")
    return value


def _typed_source_identity(value: object) -> str:
    if not isinstance(value, str) or not SOURCE_IDENTITY.fullmatch(value):
        raise ContractError("fixed_source_identity has an invalid typed form")
    return value


def logical_entry_identity(
    *, component: str, normalized_path: str, call_locator: str, source_tag: str,
) -> str:
    """SHA256(canonical({schema_version, component, normalized_path, call_locator, source_tag}))."""
    payload = {
        "schema_version": 1,
        "component": component,
        "normalized_path": normalized_path,
        "call_locator": call_locator,
        "source_tag": source_tag,
    }
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def entry_revision_identity(
    *, logical_entry_identity: str, source: str, target: str,
    fixed_source_identity: str, terminology_snapshot: str, rules_version: str,
) -> str:
    """Versioned revision identity under a stable logical entry identity."""
    if not isinstance(logical_entry_identity, str) or not SHA256.fullmatch(
        logical_entry_identity
    ):
        raise ContractError("logical_entry_identity must be 64 lowercase hexadecimal characters")
    payload = {
        "schema_version": 1,
        "logical_entry_identity": logical_entry_identity,
        "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "target_sha256": hashlib.sha256(target.encode("utf-8")).hexdigest(),
        "fixed_source_identity": fixed_source_identity,
        "rules_version": rules_version,
    }
    # Rules-v2 changes only the revision recipe.  Every envelope still binds
    # the exact terminology snapshot as required provenance; all other rules
    # strings retain the historical contract recipe byte-for-byte.
    if rules_version != IDENTITY_RULES_V2:
        payload["terminology_snapshot_sha256"] = hashlib.sha256(
            terminology_snapshot.encode("utf-8")
        ).hexdigest()
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def _validate_entry(entry: object, *, scalars: dict[str, str]) -> dict[str, str]:
    if not isinstance(entry, dict) or frozenset(entry) != ENTRY_KEYS:
        raise ContractError("surface entry must have exactly the eight canonical keys")
    for key in ("component", "call_locator", "source", "target"):
        _nonempty_string(entry[key], f"entry {key}")
    normalize_relative_path(entry["normalized_path"])
    validate_call_locator(entry["call_locator"])
    reject_path_line_locator(entry["normalized_path"], entry["call_locator"])
    if not isinstance(entry["source_tag"], str):
        raise ContractError("entry source_tag must be a string")
    for key in ENTRY_KEYS:
        if not isinstance(entry[key], str):
            raise ContractError(f"entry {key} must be a string")
    logical = logical_entry_identity(
        component=entry["component"],
        normalized_path=entry["normalized_path"],
        call_locator=entry["call_locator"],
        source_tag=entry["source_tag"],
    )
    if logical != entry["logical_entry_identity"]:
        raise ContractError("entry logical_entry_identity does not match its locator fields")
    revision = entry_revision_identity(
        logical_entry_identity=logical,
        source=entry["source"],
        target=entry["target"],
        fixed_source_identity=scalars["fixed_source_identity"],
        terminology_snapshot=scalars["terminology_snapshot"],
        rules_version=scalars["rules_version"],
    )
    if revision != entry["entry_revision_identity"]:
        raise ContractError("entry entry_revision_identity does not match the identity recipe")
    return entry  # type: ignore[return-value]


def reject_non_dispatchable_artifact(value: object, *, label: str) -> None:
    """Fail closed when a production shadow is offered to a real consumer.

    This check is called by the payload and envelope entry points used by the
    surface manifest/result tools; it is not a standalone advisory helper.
    """
    if not isinstance(value, dict):
        return
    kind = value.get("kind")
    markers = value.get("markers")
    shadow_kind = isinstance(kind, str) and (
        "shadow" in kind or kind in {"shadow_queue_policy_v1", "shadow_batch_draft_v1"}
    )
    false_marker = isinstance(markers, dict) and any(
        markers.get(key) is False
        for key in ("authoritative", "dispatchable", "promotable")
    )
    shadow_reference = "shadow_policy_id" in value or "shadow_batch_id" in value
    if shadow_kind or false_marker or shadow_reference:
        raise ContractError(f"{label} is a non-dispatchable production shadow artifact")


def validate_payload(payload: object) -> dict[str, Any]:
    """Validate one translation_surface_screen_v1 workset payload exactly."""
    reject_non_dispatchable_artifact(payload, label="surface payload")
    if not isinstance(payload, dict) or frozenset(payload) != PAYLOAD_KEYS:
        raise ContractError("surface payload must have exactly the six canonical keys")
    if payload["contract"] != CONTRACT:
        raise ContractError(f"surface payload contract must be {CONTRACT}")
    scalars = {
        "fixed_source_identity": _typed_source_identity(payload["fixed_source_identity"]),
        "terminology_snapshot": payload["terminology_snapshot"],
        "rules_version": _nonempty_string(payload["rules_version"], "rules_version"),
        "rendered_briefing": payload["rendered_briefing"],
    }
    for key in ("terminology_snapshot", "rendered_briefing"):
        if not isinstance(payload[key], str):
            raise ContractError(f"payload {key} must be a string")
    if HEX64_CONTAINS.search(payload["rendered_briefing"]):
        raise ContractError("rendered_briefing must not contain a candidate identity")
    entries = payload["entries"]
    if not isinstance(entries, list) or not entries:
        raise ContractError("surface payload entries must be a non-empty array (n=0 must not dispatch)")
    seen_logical: set[str] = set()
    previous_revision: str | None = None
    for entry in entries:
        _validate_entry(entry, scalars=scalars)
        if entry["logical_entry_identity"] in seen_logical:
            raise ContractError("surface entries must have unique logical identities")
        seen_logical.add(entry["logical_entry_identity"])
        revision = entry["entry_revision_identity"]
        if previous_revision is not None and revision <= previous_revision:
            raise ContractError(
                "surface entries must be strictly ordered by canonical entry_revision_identity"
            )
        previous_revision = revision
    return payload


def canonical_payload_bytes(payload: object) -> bytes:
    validate_payload(payload)
    return canonical_bytes(payload)


def validate_envelope(envelope: object) -> tuple[dict[str, Any], str]:
    reject_non_dispatchable_artifact(envelope, label="surface envelope")
    if isinstance(envelope, dict) and "payload" in envelope:
        reject_non_dispatchable_artifact(envelope["payload"], label="surface envelope payload")
    if not isinstance(envelope, dict) or frozenset(envelope) != {
        "candidate_identity", "payload"
    }:
        raise ContractError("surface envelope must contain exactly candidate_identity and payload")
    identity = envelope["candidate_identity"]
    if not isinstance(identity, str) or not SHA256.fullmatch(identity):
        raise ContractError("candidate_identity must be 64 lowercase hexadecimal characters")
    payload = envelope["payload"]
    canonical = canonical_payload_bytes(payload)
    if hashlib.sha256(canonical).hexdigest() != identity:
        raise ContractError("candidate_identity does not match canonical surface payload")
    assert isinstance(payload, dict)
    return payload, identity


def validate_result(result: object, envelope: object) -> dict[str, Any]:
    """Surface results are OK|ISSUE observations only; nothing else is accepted."""
    payload, identity = validate_envelope(envelope)
    if not isinstance(result, dict) or frozenset(result) != RESULT_ROOT_KEYS:
        raise ContractError("surface result must contain exactly contract, candidate_identity, results")
    if result["contract"] != CONTRACT:
        raise ContractError(f"surface result contract must be {CONTRACT}")
    if result["candidate_identity"] != identity:
        raise ContractError("surface result candidate_identity does not match envelope")
    results = result["results"]
    entries = payload["entries"]
    if not isinstance(results, list) or len(results) != len(entries):
        raise ContractError("surface result count must equal the frozen entry count")
    for index, (item, entry) in enumerate(zip(results, entries)):
        if not isinstance(item, dict):
            raise ContractError(f"results[{index}] must be an object")
        verdict = item.get("verdict")
        if verdict == "OK":
            expected = RESULT_ITEM_OK_KEYS
        elif verdict == "ISSUE":
            expected = RESULT_ITEM_ISSUE_KEYS
        else:
            raise ContractError(f"results[{index}] verdict must be OK or ISSUE")
        if frozenset(item) != expected:
            raise ContractError(f"results[{index}] has an invalid exact shape")
        if item["entry_revision_identity"] != entry["entry_revision_identity"]:
            raise ContractError(f"results[{index}] does not match the frozen entry order")
        if verdict == "ISSUE" and (
            not isinstance(item["observation"], str) or not item["observation"].strip()
        ):
            raise ContractError(f"results[{index}] ISSUE observation must be non-empty")
    return result


def validate_result_bytes(envelope_bytes: bytes, raw_output: bytes) -> dict[str, Any]:
    envelope = strict_json_bytes(envelope_bytes, label="envelope")
    if envelope_bytes != canonical_bytes(envelope):
        raise ContractError("envelope bytes must be canonical compact JSON")
    try:
        result = strict_json_bytes(raw_output, label="raw output")
    except InputError as error:
        raise ContractError(str(error)) from error
    validated = validate_result(result, envelope)
    if raw_output != canonical_bytes(validated):
        raise ContractError("raw output bytes must be canonical compact JSON without trailing bytes")
    return validated


def render_dispatch_prompt(candidate_identity: str, input_path: str) -> str:
    if not isinstance(candidate_identity, str) or not SHA256.fullmatch(candidate_identity):
        raise ContractError("prompt candidate identity is invalid")
    if not isinstance(input_path, str) or not input_path:
        raise ContractError("prompt input_path is invalid")
    prompt = PROMPT_TEMPLATE.replace(
        "<candidate_identity>", candidate_identity
    ).replace("<input_path>", input_path)
    if len(PROMPT_TEMPLATE.encode("utf-8")) > 800 or len(prompt.encode("utf-8")) > 800:
        raise ContractError("prompt template or instance exceeds 800 UTF-8 bytes")
    return prompt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("envelope")
    parser.add_argument("raw_output")
    args = parser.parse_args(argv)
    try:
        envelope_bytes = Path(args.envelope).read_bytes()
        raw_bytes = Path(args.raw_output).read_bytes()
    except OSError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    try:
        validate_result_bytes(envelope_bytes, raw_bytes)
    except InputError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    except ContractError as error:
        print(f"RESULT_FAILED: {error}")
        return 1
    print("RESULT_VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
