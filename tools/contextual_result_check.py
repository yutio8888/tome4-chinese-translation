#!/usr/bin/env python3
"""Strict offline validator for translation_contextual_v2 reviewer output."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


PAYLOAD_KEYS = frozenset({
    "contract", "ordered_revision_keys", "translation_snapshot",
    "fixed_source_identity", "terminology_snapshot", "bounded_context",
    "rendered_briefing",
})
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_IDENTITY = re.compile(r"^(?:commit:[0-9a-f]{40}|snapshot:[0-9a-f]{64})$")


class InputError(Exception):
    """The input cannot safely be read or decoded."""


class ContractError(Exception):
    """The decoded value violates translation-contextual/2.0."""


def _reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, *, label: str) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise InputError(f"{label} must not contain a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InputError(f"{label} is not UTF-8: {error}") from error
    try:
        decoder = json.JSONDecoder(
            object_pairs_hook=_reject_duplicate,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ContractError(f"non-standard JSON constant: {value}")
            ),
        )
        value, end = decoder.raw_decode(text)
    except ContractError:
        raise
    except json.JSONDecodeError as error:
        raise ContractError(f"{label} is not one strict JSON value: {error}") from error
    if end != len(text):
        raise ContractError(f"{label} has leading or trailing bytes")
    return value


def canonical_payload_bytes(payload: object) -> bytes:
    if not isinstance(payload, dict) or set(payload) != PAYLOAD_KEYS:
        raise ContractError("v2 payload must have exactly the seven canonical keys")
    if payload.get("contract") != "translation_contextual_v2":
        raise ContractError("payload contract must be translation_contextual_v2")
    for key in ("fixed_source_identity", "terminology_snapshot", "rendered_briefing"):
        if not isinstance(payload.get(key), str):
            raise ContractError(f"payload {key} must be a string")
    if not SOURCE_IDENTITY.fullmatch(payload["fixed_source_identity"]):
        raise ContractError("fixed_source_identity has an invalid typed form")
    if SHA256.search(payload["rendered_briefing"]):
        raise ContractError("rendered_briefing must not contain a candidate identity")
    keys = payload.get("ordered_revision_keys")
    translations = payload.get("translation_snapshot")
    contexts = payload.get("bounded_context")
    if (
        not isinstance(keys, list) or not keys
        or any(not isinstance(key, str) or not key for key in keys)
        or len(keys) != len(set(keys))
    ):
        raise ContractError("ordered_revision_keys must be non-empty, unique strings")
    if not isinstance(translations, list) or not isinstance(contexts, list):
        raise ContractError("translation_snapshot and bounded_context must be arrays")
    for item in translations:
        if (
            not isinstance(item, dict)
            or set(item) != {"revision_key", "source", "target"}
            or any(not isinstance(item.get(key), str) for key in item)
            or not item["source"]
        ):
            raise ContractError("translation_snapshot must contain exact string objects with non-empty source")
    for item in contexts:
        if (
            not isinstance(item, dict)
            or set(item) != {"revision_key", "context"}
            or any(not isinstance(item.get(key), str) for key in item)
        ):
            raise ContractError("bounded_context must contain exact string objects")
    if [item["revision_key"] for item in translations] != keys:
        raise ContractError("translation_snapshot order must equal ordered_revision_keys")
    if [item["revision_key"] for item in contexts] != keys:
        raise ContractError("bounded_context order must equal ordered_revision_keys")
    try:
        return json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise ContractError(f"payload is not canonicalizable: {error}") from error


def validate_envelope(envelope: object) -> tuple[dict[str, Any], str]:
    if not isinstance(envelope, dict) or set(envelope) != {"candidate_identity", "payload"}:
        raise ContractError("envelope must contain exactly candidate_identity and payload")
    identity = envelope.get("candidate_identity")
    if not isinstance(identity, str) or not SHA256.fullmatch(identity):
        raise ContractError("candidate_identity must be 64 lowercase hexadecimal characters")
    payload = envelope.get("payload")
    canonical = canonical_payload_bytes(payload)
    if hashlib.sha256(canonical).hexdigest() != identity:
        raise ContractError("candidate_identity does not match canonical payload")
    assert isinstance(payload, dict)
    return payload, identity


def validate_result(result: object, envelope: object) -> dict[str, Any]:
    payload, identity = validate_envelope(envelope)
    if not isinstance(result, dict) or set(result) != {"contract", "candidate_identity", "verdicts"}:
        raise ContractError("result must contain exactly contract, candidate_identity, and verdicts")
    if result.get("contract") != "translation_contextual_v2":
        raise ContractError("result contract must be translation_contextual_v2")
    if result.get("candidate_identity") != identity:
        raise ContractError("result candidate_identity does not match envelope")
    verdicts = result.get("verdicts")
    keys = payload["ordered_revision_keys"]
    if not isinstance(verdicts, list) or len(verdicts) != len(keys):
        raise ContractError("verdict count must equal the frozen revision count")
    for index, (item, revision_key) in enumerate(zip(verdicts, keys)):
        if not isinstance(item, dict):
            raise ContractError(f"verdicts[{index}] must be an object")
        verdict = item.get("verdict")
        expected = {"revision_key", "verdict"} if verdict == "OK" else {
            "revision_key", "verdict", "observation"
        }
        if verdict not in {"OK", "ISSUE"} or set(item) != expected:
            raise ContractError(f"verdicts[{index}] has an invalid verdict or shape")
        if item.get("revision_key") != revision_key:
            raise ContractError(f"verdicts[{index}] does not match frozen revision order")
        if verdict == "ISSUE" and (
            not isinstance(item.get("observation"), str)
            or not item["observation"].strip()
        ):
            raise ContractError(f"verdicts[{index}] ISSUE observation must be non-empty")
    return result


def validate_result_bytes(envelope_bytes: bytes, raw_output: bytes) -> dict[str, Any]:
    envelope = strict_json_bytes(envelope_bytes, label="envelope")
    try:
        canonical_envelope = json.dumps(
            envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise ContractError(f"envelope is not canonicalizable: {error}") from error
    if envelope_bytes != canonical_envelope:
        raise ContractError("envelope bytes must be canonical compact JSON")
    try:
        result = strict_json_bytes(raw_output, label="raw output")
    except InputError as error:
        raise ContractError(str(error)) from error
    validated = validate_result(result, envelope)
    try:
        compact_result = json.dumps(
            validated, ensure_ascii=False, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise ContractError(f"result is not canonicalizable: {error}") from error
    if raw_output != compact_result:
        raise ContractError("raw output bytes must be compact JSON without trailing bytes")
    return validated


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
