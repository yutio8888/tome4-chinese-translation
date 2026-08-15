"""Translation-only semantic review v2 contracts and deterministic validation."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from .errors import ConfigurationError, ValidationError
from .quality import (
    compute_revision_id,
    compute_revision_uid,
    compute_tu_uid,
    compute_unit_id,
    editorial_tu_uids,
)
from .quality_claims import claim_signature, normalize_evidence
from .quality_contracts import (
    canonical_sha256,
    enum,
    exact_fields,
    integer,
    sha256,
    string,
)
from .report import atomic_write_bytes


TRANSLATION_REVIEW_SCHEMA_VERSION = 2
TRANSLATION_REVIEW_BUNDLE_CONTRACT = "tome4-translation-review-bundle-v2"
TRANSLATION_REVIEW_POLICY_CONTRACT = "tome4-translation-review-policy-v2"
TRANSLATION_REVIEW_ASSESSMENT_CONTRACT = "tome4-translation-review-assessment-v2"
TRANSLATION_REVIEW_INPUT_CONTRACT = "tome4-translation-review-input-v2"
TRANSLATION_REVIEW_NORMALIZER_CONTRACT = "tome4-translation-review-normalizer-v2"
TRANSLATION_REVIEW_RUNNER_CONTRACT = "tome4-translation-review-pi-stdio-v2"
TRANSLATION_REVIEW_CHANNEL = "semantic-observation"
TRANSLATION_REVIEW_METHOD = "blind-semantic-delta-v2"
TRANSLATION_REVIEW_PARTITION_CONTRACT = "tome4-translation-review-partition-v2"
TRANSLATION_REVIEW_INVENTORY_CONTRACT = "tome4-translation-review-inventory-v1"
TRANSLATION_REVIEW_ITEM_CONTRACT = "tome4-translation-review-item-v2"
TRANSLATION_REVIEW_POLICY_PATH = Path("i18n/review/translation-semantic-v2.json")
DEFAULT_TRANSLATION_CHARACTER_BUDGET = 24000
MAX_TRANSLATION_CHARACTER_BUDGET = 100000
MAX_TRANSLATION_REVIEW_BATCH_SIZE = 10

TRANSLATION_ITEM_FIELDS = (
    "item_id",
    "unit_id",
    "tu_uid",
    "revision_uid",
    "revision_id",
    "component",
    "ordinal",
    "section",
    "source",
    "target",
    "source_tag",
    "args_order",
    "special",
    "line",
)
MODEL_ITEM_FIELDS = ("revision_id", "assessment_state", "findings")
MODEL_FINDING_FIELDS = (
    "phenomenon",
    "meaning_change",
    "source_evidence",
    "target_evidence",
    "explanation",
)
EVALUATOR_FIELDS = (
    "kind",
    "provider",
    "model",
    "thinking",
    "runner_contract",
    "prompt_sha256",
    "policy_sha256",
    "bundle_sha256",
    "bundle_payload_sha256",
    "bundle_payload_bytes",
    "normalizer_contract",
)
ASSESSMENT_FIELDS = (
    "schema_version",
    "review_contract",
    "bundle_id",
    "bundle_sha256",
    "policy_sha256",
    "evaluator",
    "observation_digest",
    "items",
    "manual_queue",
    "assessment_id",
    "review_id",
)
INVENTORY_HEADER_FIELDS = (
    "contract",
    "item_contract",
    "tool_version",
    "version",
    "component",
    "translation_sha256",
    "item_count",
)
MEMBERSHIP_FIELDS = ("ordinal", "byte_start", "byte_end", "item_sha256")


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def write_translation_inventory(
    *,
    root: Path,
    tool_version: str,
    version: str,
    component: str,
    translation_sha256: str,
    items: list[dict[str, Any]],
) -> tuple[str, dict[int, dict[str, Any]]]:
    """Persist one content-addressed canonical inventory per component revision.

    Consumers hash the cached bytes and compare only the selected byte slices.  They
    never need to launch Lua or rebuild the full inventory for each review shard.
    """
    header = {
        "contract": TRANSLATION_REVIEW_INVENTORY_CONTRACT,
        "item_contract": TRANSLATION_REVIEW_ITEM_CONTRACT,
        "tool_version": tool_version,
        "version": version,
        "component": component,
        "translation_sha256": translation_sha256,
        "item_count": len(items),
    }
    chunks = [_canonical_json_bytes(header) + b"\n"]
    offset = len(chunks[0])
    membership: dict[int, dict[str, Any]] = {}
    for expected_ordinal, item in enumerate(items):
        if item.get("ordinal") != expected_ordinal:
            raise ValidationError(
                "translation review inventory items must use contiguous canonical ordinals"
            )
        encoded = _canonical_json_bytes(item)
        membership[expected_ordinal] = {
            "ordinal": expected_ordinal,
            "byte_start": offset,
            "byte_end": offset + len(encoded),
            "item_sha256": hashlib.sha256(encoded).hexdigest(),
        }
        chunks.append(encoded + b"\n")
        offset += len(encoded) + 1
    payload = b"".join(chunks)
    inventory_sha256 = hashlib.sha256(payload).hexdigest()
    path = (
        root
        / ".artifacts"
        / "i18n"
        / "cache"
        / "review-inventory"
        / f"{inventory_sha256}.jsonl"
    )
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise ValidationError(
                "translation review inventory cache entry is not a regular file"
            )
        try:
            existing = path.read_bytes()
        except OSError as error:
            raise ValidationError(
                "cannot read translation review inventory cache entry"
            ) from error
        if existing != payload:
            raise ValidationError(
                "translation review inventory cache entry has invalid content"
            )
    else:
        atomic_write_bytes(path, payload)
    return inventory_sha256, membership


def validate_translation_inventory_membership(
    *,
    root: Path,
    tool_version: str,
    version: str,
    component: str,
    translation_sha256: str,
    inventory_sha256: str,
    membership: Any,
    items: list[dict[str, Any]],
) -> int:
    sha256(inventory_sha256, "translation review inventory_sha256")
    path = (
        root
        / ".artifacts"
        / "i18n"
        / "cache"
        / "review-inventory"
        / f"{inventory_sha256}.jsonl"
    )
    if path.is_symlink() or not path.is_file():
        raise ValidationError(
            "translation review canonical inventory is unavailable; rebuild the bundle"
        )
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise ValidationError(
            "cannot read translation review canonical inventory"
        ) from error
    if hashlib.sha256(payload).hexdigest() != inventory_sha256:
        raise ValidationError("translation review canonical inventory digest is invalid")
    header_bytes, separator, _remaining = payload.partition(b"\n")
    if not separator:
        raise ValidationError("translation review canonical inventory has no header")
    try:
        header = json.loads(header_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(
            "translation review canonical inventory header is invalid"
        ) from error
    if not isinstance(header, dict):
        raise ValidationError("translation review canonical inventory header is invalid")
    exact_fields(header, INVENTORY_HEADER_FIELDS, "translation review inventory header")
    if header != {
        "contract": TRANSLATION_REVIEW_INVENTORY_CONTRACT,
        "item_contract": TRANSLATION_REVIEW_ITEM_CONTRACT,
        "tool_version": tool_version,
        "version": version,
        "component": component,
        "translation_sha256": translation_sha256,
        "item_count": header["item_count"],
    }:
        raise ValidationError("translation review canonical inventory identity is invalid")
    item_count = integer(
        header["item_count"], "translation review inventory item_count"
    )
    if item_count < 1:
        raise ValidationError("translation review canonical inventory is empty")
    if not isinstance(membership, list) or len(membership) != len(items):
        raise ValidationError("translation review canonical membership is invalid")
    previous_ordinal = -1
    for index, (proof, item) in enumerate(zip(membership, items)):
        where = f"translation review canonical membership[{index}]"
        if not isinstance(proof, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(proof, MEMBERSHIP_FIELDS, where)
        ordinal = integer(proof["ordinal"], f"{where}.ordinal")
        start = integer(proof["byte_start"], f"{where}.byte_start")
        end = integer(proof["byte_end"], f"{where}.byte_end")
        sha256(proof["item_sha256"], f"{where}.item_sha256")
        if ordinal != item.get("ordinal") or not previous_ordinal < ordinal < item_count:
            raise ValidationError(
                "translation review canonical membership ordinals are invalid or out of order"
            )
        previous_ordinal = ordinal
        expected = _canonical_json_bytes(item)
        if (
            start < len(header_bytes) + 1
            or end <= start
            or end >= len(payload)
            or payload[end : end + 1] != b"\n"
            or payload[start:end] != expected
            or hashlib.sha256(expected).hexdigest() != proof["item_sha256"]
        ):
            raise ValidationError(
                f"translation review item does not match canonical inventory at ordinal {ordinal}"
            )
    return item_count


def _read_policy(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except OSError as error:
        raise ConfigurationError(f"cannot read translation review policy: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ConfigurationError(f"invalid translation review policy: {path}: {error}") from error
    if not isinstance(value, dict):
        raise ConfigurationError("translation review policy must be an object")
    return value, hashlib.sha256(raw).hexdigest()


def load_translation_review_policy(root: Path) -> tuple[dict[str, Any], str]:
    policy, digest = _read_policy(root / TRANSLATION_REVIEW_POLICY_PATH)
    expected_fields = (
        "contract",
        "schema_version",
        "channel",
        "method_version",
        "assessment_states",
        "phenomena",
        "meaning_change_types",
        "phenomenon_meaning_changes",
        "default_character_budget",
        "max_character_budget",
        "max_items_per_bundle",
        "max_findings_per_item",
    )
    try:
        exact_fields(policy, expected_fields, "translation review policy")
        if (
            policy["contract"] != TRANSLATION_REVIEW_POLICY_CONTRACT
            or policy["schema_version"] != TRANSLATION_REVIEW_SCHEMA_VERSION
            or policy["channel"] != TRANSLATION_REVIEW_CHANNEL
            or policy["method_version"] != TRANSLATION_REVIEW_METHOD
        ):
            raise ValidationError("translation review policy identity is unsupported")
        states = policy["assessment_states"]
        phenomena = policy["phenomena"]
        meanings = policy["meaning_change_types"]
        if states != ["assessed", "context-insufficient"]:
            raise ValidationError("translation review assessment states are not frozen")
        if (
            not isinstance(phenomena, list)
            or not phenomena
            or not all(isinstance(value, str) and value for value in phenomena)
            or len(set(phenomena)) != len(phenomena)
        ):
            raise ValidationError("translation review phenomena are invalid")
        if (
            not isinstance(meanings, list)
            or not meanings
            or not all(isinstance(value, str) and value for value in meanings)
            or len(set(meanings)) != len(meanings)
        ):
            raise ValidationError("translation review meaning changes are invalid")
        compatibility = policy["phenomenon_meaning_changes"]
        if not isinstance(compatibility, dict) or set(compatibility) != set(phenomena):
            raise ValidationError("translation review compatibility matrix is incomplete")
        for phenomenon, allowed in compatibility.items():
            if (
                not isinstance(phenomenon, str)
                or not isinstance(allowed, list)
                or not allowed
                or not all(isinstance(value, str) and value for value in allowed)
                or len(set(allowed)) != len(allowed)
                or not set(allowed) <= set(meanings)
            ):
                raise ValidationError("translation review compatibility matrix is invalid")
        if policy["default_character_budget"] != DEFAULT_TRANSLATION_CHARACTER_BUDGET:
            raise ValidationError("translation review default character budget is not frozen")
        if policy["max_character_budget"] != MAX_TRANSLATION_CHARACTER_BUDGET:
            raise ValidationError("translation review maximum character budget is not frozen")
        if policy["max_items_per_bundle"] != MAX_TRANSLATION_REVIEW_BATCH_SIZE:
            raise ValidationError("translation review maximum item count is not frozen")
        maximum = integer(policy["max_findings_per_item"], "translation review max findings")
        if not 1 <= maximum <= 100:
            raise ValidationError("translation review max findings must be from 1 to 100")
    except ValidationError as error:
        raise ConfigurationError(str(error)) from error
    return policy, digest


def build_translation_items(
    *, version: str, component: str, ordinal: int, entry: dict[str, Any],
    editorial_to_tu: dict[tuple[str, str], tuple[str, ...]] | None = None,
) -> list[dict[str, Any]]:
    """Build one translation-review item per Pilot A TU for this occurrence.

    A one-to-many editorial (one locale key backing several structurally
    distinct strong TUs, contract §4.7) yields one item per TU so every
    quality revision can receive translation-v2 observations, matching the
    quality inventory split (infra-contract-007).  Callers renumber ordinals
    contiguously after flattening.
    """
    source = entry.get("source")
    target = entry.get("target")
    section = entry.get("section")
    source_tag = entry.get("source_tag")
    if not all(isinstance(value, str) for value in (source, target, section)):
        raise ValidationError(f"invalid canonical translation entry in component {component}")
    if source_tag is not None and not isinstance(source_tag, str):
        raise ValidationError(f"invalid source_tag in component {component}")
    unit_id = compute_unit_id(component, section, source, source_tag)
    tu_uids = editorial_tu_uids(
        component, section, source, source_tag, editorial_to_tu=editorial_to_tu
    )
    items = []
    for tu_uid in tu_uids:
        revision_uid_value = compute_revision_uid(tu_uid, source)
        revision_id = compute_revision_id(
            version, unit_id, target, entry.get("args_order"), entry.get("special"),
            tu_uid=tu_uid, revision_uid_value=revision_uid_value, source=source,
        )
        items.append({
            "item_id": "translation-" + revision_id,
            "unit_id": unit_id,
            "tu_uid": tu_uid,
            "revision_uid": revision_uid_value,
            "revision_id": revision_id,
            "component": component,
            "ordinal": ordinal,
            "section": section,
            "source": source,
            "target": target,
            "source_tag": source_tag,
            "args_order": entry.get("args_order"),
            "special": entry.get("special"),
            "line": entry.get("line"),
        })
    return items


def build_translation_item(
    *, version: str, component: str, ordinal: int, entry: dict[str, Any],
    editorial_to_tu: dict[tuple[str, str], tuple[str, ...]] | None = None,
) -> dict[str, Any]:
    """Backward-compatible single-item builder (first TU of the editorial).

    New callers should use :func:`build_translation_items`; this helper is
    kept for callers that only need the subject TU item.
    """
    return build_translation_items(
        version=version, component=component, ordinal=ordinal, entry=entry,
        editorial_to_tu=editorial_to_tu,
    )[0]


def translation_provider_item(item: dict[str, Any]) -> dict[str, Any]:
    """Return the minimal semantic input visible to the blind reviewer."""
    return {
        "revision_id": item["revision_id"],
        "source": item["source"],
        "target": item["target"],
    }


def translation_provider_payload(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": TRANSLATION_REVIEW_SCHEMA_VERSION,
        "review_contract": TRANSLATION_REVIEW_INPUT_CONTRACT,
        "bundle_id": bundle["bundle_id"],
        "channel": TRANSLATION_REVIEW_CHANNEL,
        "method_version": TRANSLATION_REVIEW_METHOD,
        "component": bundle["component"],
        "items": [translation_provider_item(item) for item in bundle["items"]],
        "constraints": bundle["constraints"],
    }


def translation_provider_message(bundle: dict[str, Any]) -> bytes:
    """Return the exact whitespace-free user message sent to Pi over stdin."""
    return _canonical_json_bytes(translation_provider_payload(bundle))


def translation_selection_sha256(items: Iterable[dict[str, Any]]) -> str:
    """Bind one ordered semantic-review selection across every emitted shard."""
    selection: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        ordinal = item.get("ordinal")
        revision_id = item.get("revision_id")
        if type(ordinal) is not int or ordinal < 0:
            raise ValidationError(
                f"translation review selection item {index} has an invalid ordinal"
            )
        if not isinstance(revision_id, str) or not revision_id:
            raise ValidationError(
                f"translation review selection item {index} has no revision_id"
            )
        selection.append({"ordinal": ordinal, "revision_id": revision_id})
    if not selection:
        raise ValidationError("translation review selection cannot be empty")
    return hashlib.sha256(_canonical_json_bytes(selection)).hexdigest()


def validate_translation_item(
    item: Any, *, version: str, component: str, where: str
) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(item, TRANSLATION_ITEM_FIELDS, where)
    if item["component"] != component:
        raise ValidationError(f"{where}.component does not match its bundle")
    for field in ("unit_id", "revision_id", "tu_uid", "revision_uid"):
        value = item[field]
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValidationError(f"{where}.{field} must be a SHA-256 digest")
    ordinal = integer(item["ordinal"], f"{where}.ordinal")
    if ordinal < 0:
        raise ValidationError(f"{where}.ordinal must be non-negative")
    for field in ("section", "source", "target"):
        string(item[field], f"{where}.{field}", empty=True)
    if item["source_tag"] is not None:
        string(item["source_tag"], f"{where}.source_tag", empty=True)
    if item["line"] is not None:
        line = integer(item["line"], f"{where}.line")
        if line < 1:
            raise ValidationError(f"{where}.line must be positive")
    expected_unit = compute_unit_id(
        component, item["section"], item["source"], item["source_tag"]
    )
    expected_revision_uid = compute_revision_uid(item["tu_uid"], item["source"])
    expected_revision = compute_revision_id(
        version,
        expected_unit,
        item["target"],
        item["args_order"],
        item["special"],
        tu_uid=item["tu_uid"],
        revision_uid_value=item["revision_uid"],
        source=item["source"],
    )
    if item["unit_id"] != expected_unit:
        raise ValidationError(f"{where}.unit_id does not match canonical identity")
    if item["revision_uid"] != expected_revision_uid:
        raise ValidationError(
            f"{where}.revision_uid does not match canonical source revision"
        )
    if item["revision_id"] != expected_revision:
        raise ValidationError(f"{where}.revision_id does not match canonical revision")
    if item["item_id"] != "translation-" + expected_revision:
        raise ValidationError(f"{where}.item_id does not match revision_id")
    return item


def translation_item_character_count(item: dict[str, Any]) -> int:
    return len(
        json.dumps(
            translation_provider_item(item),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def deduplicate_translation_revisions(
    items: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep one occurrence of each semantic revision in canonical order."""
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        revision_id = item.get("revision_id")
        if not isinstance(revision_id, str):
            raise ValidationError("translation review item has no revision_id")
        if revision_id in seen:
            continue
        seen.add(revision_id)
        unique.append(item)
    return unique


def partition_translation_items(
    items: list[dict[str, Any]], *, max_items: int, character_budget: int
) -> list[tuple[int, list[dict[str, Any]], int, bool]]:
    if type(max_items) is not int or max_items < 1:
        raise ValidationError("translation review max_items must be a positive integer")
    if (
        type(character_budget) is not int
        or not 1 <= character_budget <= MAX_TRANSLATION_CHARACTER_BUDGET
    ):
        raise ValidationError(
            "translation review character budget must be between 1 and "
            f"{MAX_TRANSLATION_CHARACTER_BUDGET}"
        )
    batches: list[tuple[int, list[dict[str, Any]], int, bool]] = []
    current: list[dict[str, Any]] = []
    current_characters = 0
    current_offset = 0

    def flush() -> None:
        nonlocal current, current_characters, current_offset
        if not current:
            return
        batches.append(
            (
                current_offset,
                current,
                current_characters,
                len(current) == 1 and current_characters > character_budget,
            )
        )
        current = []
        current_characters = 0

    for offset, item in enumerate(items):
        characters = translation_item_character_count(item)
        if current and (
            len(current) >= max_items
            or current_characters + characters > character_budget
        ):
            flush()
        if not current:
            current_offset = offset
        current.append(item)
        current_characters += characters
        if characters > character_budget:
            flush()
    flush()
    return batches


def make_evaluator_identity(
    *,
    provider: str,
    model: str,
    thinking: str,
    prompt_sha256: str,
    policy_sha256: str,
    bundle: dict[str, Any],
) -> dict[str, Any]:
    provider_message = translation_provider_message(bundle)
    evaluator = {
        "kind": "model",
        "provider": provider,
        "model": model,
        "thinking": thinking,
        "runner_contract": TRANSLATION_REVIEW_RUNNER_CONTRACT,
        "prompt_sha256": prompt_sha256,
        "policy_sha256": policy_sha256,
        "bundle_sha256": canonical_sha256(bundle),
        "bundle_payload_sha256": hashlib.sha256(provider_message).hexdigest(),
        "bundle_payload_bytes": len(provider_message),
        "normalizer_contract": TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
    }
    validate_evaluator_identity(evaluator, where="translation review evaluator")
    return evaluator


def validate_evaluator_identity(value: Any, *, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(value, EVALUATOR_FIELDS, where)
    if value["kind"] != "model":
        raise ValidationError(f"{where}.kind must be model")
    for field in ("provider", "model", "thinking"):
        string(value[field], f"{where}.{field}")
    if value["runner_contract"] != TRANSLATION_REVIEW_RUNNER_CONTRACT:
        raise ValidationError(f"{where}.runner_contract is unsupported")
    for field in (
        "prompt_sha256",
        "policy_sha256",
        "bundle_sha256",
        "bundle_payload_sha256",
    ):
        sha256(value[field], f"{where}.{field}")
    payload_bytes = integer(value["bundle_payload_bytes"], f"{where}.bundle_payload_bytes")
    if payload_bytes < 1:
        raise ValidationError(f"{where}.bundle_payload_bytes must be positive")
    if value["normalizer_contract"] != TRANSLATION_REVIEW_NORMALIZER_CONTRACT:
        raise ValidationError(f"{where}.normalizer_contract is unsupported")
    return value


def _strict_evidence(
    evidence: Any,
    text: str,
    *,
    where: str,
    allow_missing: bool,
) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(evidence, ("quote", "occurrence"), where)
    normalized = normalize_evidence(
        evidence, text, where=where, allow_empty_omission=allow_missing
    )
    allowed_states = {"exact"}
    if allow_missing:
        allowed_states.add("missing")
    if normalized["state"] not in allowed_states:
        raise ValidationError(
            f"{where} does not resolve to one exact span; provide a literal quote and "
            "one-based occurrence"
        )
    if normalized["state"] == "exact":
        start = normalized["start"]
        end = normalized["end"]
        if type(start) is not int or type(end) is not int or text[start:end] != (
            normalized["quote"]
        ):
            raise ValidationError(f"{where} normalized span is invalid")
    return normalized


def _reason_codes(
    *, assessment_state: str, phenomenon: str, meaning_change: str
) -> list[str]:
    reasons = ["REVIEW_REQUIRES_HOST_CONFIRMATION"]
    if assessment_state == "context-insufficient":
        reasons.append("REVIEW_CONTEXT_INSUFFICIENT")
    if phenomenon == "other":
        reasons.append("REVIEW_PHENOMENON_OTHER")
    if meaning_change == "unknown":
        reasons.append("REVIEW_MEANING_UNKNOWN")
    return reasons


def _assessment_identity(value: dict[str, Any]) -> str:
    return canonical_sha256(
        {
            key: value[key]
            for key in ASSESSMENT_FIELDS
            if key not in {"assessment_id", "review_id"}
        }
    )


def validate_translation_model_output(
    *,
    bundle: dict[str, Any],
    output: dict[str, Any],
    policy: dict[str, Any],
    policy_sha256: str,
    evaluator: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(output, dict):
        raise ValidationError("Pi translation review output must be an object")
    exact_fields(output, ("items",), "Pi translation review output")
    model_items = output["items"]
    bundle_items = bundle.get("items")
    if not isinstance(bundle_items, list) or not bundle_items:
        raise ValidationError("translation review bundle has no items")
    if not isinstance(model_items, list) or len(model_items) != len(bundle_items):
        raise ValidationError("Pi translation review must cover every bundle item")
    validate_evaluator_identity(evaluator, where="translation review evaluator")
    if evaluator["policy_sha256"] != policy_sha256:
        raise ValidationError("translation review evaluator policy digest does not match")
    if evaluator["bundle_sha256"] != canonical_sha256(bundle):
        raise ValidationError("translation review evaluator bundle digest does not match")

    normalized_items: list[dict[str, Any]] = []
    finding_keys: set[str] = set()
    total_findings = 0
    for item_index, (model_item, bundle_item) in enumerate(
        zip(model_items, bundle_items)
    ):
        where = f"Pi translation review items[{item_index}]"
        if not isinstance(model_item, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(model_item, MODEL_ITEM_FIELDS, where)
        if model_item["revision_id"] != bundle_item.get("revision_id"):
            raise ValidationError(
                f"{where}.revision_id is missing, duplicate, unknown, or out of order"
            )
        assessment_state = enum(
            model_item["assessment_state"],
            policy["assessment_states"],
            f"{where}.assessment_state",
        )
        raw_findings = model_item["findings"]
        if not isinstance(raw_findings, list):
            raise ValidationError(f"{where}.findings must be an array")
        if len(raw_findings) > policy["max_findings_per_item"]:
            raise ValidationError(f"{where}.findings exceeds the per-item maximum")
        normalized_findings: list[dict[str, Any]] = []
        for finding_index, finding in enumerate(raw_findings):
            finding_where = f"{where}.findings[{finding_index}]"
            if not isinstance(finding, dict):
                raise ValidationError(f"{finding_where} must be an object")
            exact_fields(finding, MODEL_FINDING_FIELDS, finding_where)
            phenomenon = enum(
                finding["phenomenon"], policy["phenomena"], f"{finding_where}.phenomenon"
            )
            meaning_change = enum(
                finding["meaning_change"],
                policy["meaning_change_types"],
                f"{finding_where}.meaning_change",
            )
            if meaning_change not in policy["phenomenon_meaning_changes"][phenomenon]:
                raise ValidationError(
                    f"{finding_where} phenomenon and meaning_change are incompatible"
                )
            explanation = string(finding["explanation"], f"{finding_where}.explanation")
            if len(explanation) > 12000:
                raise ValidationError(f"{finding_where}.explanation is oversized")
            source = _strict_evidence(
                finding["source_evidence"],
                bundle_item["source"],
                where=f"{finding_where}.source_evidence",
                allow_missing=False,
            )
            target = _strict_evidence(
                finding["target_evidence"],
                bundle_item["target"],
                where=f"{finding_where}.target_evidence",
                allow_missing=meaning_change == "omitted",
            )
            if target["state"] == "missing" and meaning_change != "omitted":
                raise ValidationError(
                    f"{finding_where}.target_evidence may be missing only for an omission"
                )
            subject = {
                "kind": "canonical-revision",
                "revision_id": bundle_item["revision_id"],
            }
            finding_key = claim_signature(
                {
                    "subject": subject,
                    "error_family": "semantic-observation",
                    "phenomenon": phenomenon,
                    "meaning_change": meaning_change,
                    "normalized_source_evidence": source,
                    "normalized_target_evidence": target,
                }
            )
            if finding_key in finding_keys:
                raise ValidationError(
                    f"Pi translation review contains duplicate semantic observation: {finding_key}"
                )
            finding_keys.add(finding_key)
            normalized_findings.append(
                {
                    "finding_key": finding_key,
                    "finding_id": "",
                    "finding_ref": "",
                    "item_id": bundle_item["item_id"],
                    "revision_id": bundle_item["revision_id"],
                    "phenomenon": phenomenon,
                    "meaning_change": meaning_change,
                    "source_evidence": finding["source_evidence"],
                    "target_evidence": finding["target_evidence"],
                    "normalized_source_evidence": source,
                    "normalized_target_evidence": target,
                    "explanation": explanation,
                    "disposition": "pending",
                    "severity": None,
                    "reason_codes": _reason_codes(
                        assessment_state=assessment_state,
                        phenomenon=phenomenon,
                        meaning_change=meaning_change,
                    ),
                }
            )
        normalized_findings.sort(key=lambda value: value["finding_key"])
        total_findings += len(normalized_findings)
        normalized_items.append(
            {
                "revision_id": bundle_item["revision_id"],
                "assessment_state": assessment_state,
                "findings": normalized_findings,
            }
        )

    next_ref = 1
    manual_queue: list[dict[str, Any]] = []
    for item in normalized_items:
        for finding in item["findings"]:
            finding_ref = f"R-{next_ref:03d}"
            next_ref += 1
            finding["finding_id"] = finding_ref
            finding["finding_ref"] = finding_ref
            manual_queue.append(
                {
                    "route_type": "finding",
                    "revision_id": item["revision_id"],
                    "finding_id": finding_ref,
                    "reason_codes": finding["reason_codes"],
                }
            )
        if item["assessment_state"] == "context-insufficient" and not item["findings"]:
            manual_queue.append(
                {
                    "route_type": "item",
                    "revision_id": item["revision_id"],
                    "finding_id": None,
                    "reason_codes": ["REVIEW_CONTEXT_INSUFFICIENT"],
                }
            )

    observation_digest = canonical_sha256(normalized_items)
    assessment = {
        "schema_version": TRANSLATION_REVIEW_SCHEMA_VERSION,
        "review_contract": TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
        "bundle_id": bundle["bundle_id"],
        "bundle_sha256": canonical_sha256(bundle),
        "policy_sha256": policy_sha256,
        "evaluator": evaluator,
        "observation_digest": observation_digest,
        "items": normalized_items,
        "manual_queue": manual_queue,
        "assessment_id": "",
        "review_id": "",
    }
    assessment_id = _assessment_identity(assessment)
    assessment["assessment_id"] = assessment_id
    assessment["review_id"] = assessment_id
    summary = {
        "ok": True,
        "findings": total_findings,
        "assessed_items": sum(
            item["assessment_state"] == "assessed" for item in normalized_items
        ),
        "context_insufficient_items": sum(
            item["assessment_state"] == "context-insufficient"
            for item in normalized_items
        ),
        "manual_queue": len(manual_queue),
        "semantic_channel_complete": True,
        "overall_translation_clean": False,
    }
    return summary, assessment


def revalidate_translation_assessment(
    *,
    bundle: dict[str, Any],
    assessment: dict[str, Any],
    policy: dict[str, Any],
    policy_sha256: str,
    evaluator: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(assessment, dict):
        raise ValidationError("cached translation review assessment must be an object")
    exact_fields(assessment, ASSESSMENT_FIELDS, "cached translation review assessment")
    if (
        assessment["schema_version"] != TRANSLATION_REVIEW_SCHEMA_VERSION
        or assessment["review_contract"] != TRANSLATION_REVIEW_ASSESSMENT_CONTRACT
        or assessment["bundle_id"] != bundle.get("bundle_id")
        or assessment["evaluator"] != evaluator
    ):
        raise ValidationError("cached translation review assessment identity is invalid")
    assessment_items = assessment["items"]
    if not isinstance(assessment_items, list):
        raise ValidationError("cached translation review assessment items must be an array")
    raw_items: list[dict[str, Any]] = []
    for index, item in enumerate(assessment_items):
        if not isinstance(item, dict):
            raise ValidationError(f"cached translation review item {index} is invalid")
        exact_fields(
            item,
            ("revision_id", "assessment_state", "findings"),
            f"cached translation review item {index}",
        )
        findings = item.get("findings")
        if not isinstance(findings, list):
            raise ValidationError(f"cached translation review item {index} findings are invalid")
        raw_findings: list[dict[str, Any]] = []
        for finding_index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                raise ValidationError(
                    f"cached translation review item {index} finding {finding_index} is invalid"
                )
            missing = [key for key in MODEL_FINDING_FIELDS if key not in finding]
            if missing:
                raise ValidationError(
                    f"cached translation review item {index} finding {finding_index} "
                    f"is missing fields: {', '.join(missing)}"
                )
            raw_findings.append(
                {key: finding[key] for key in MODEL_FINDING_FIELDS}
            )
        raw_items.append(
            {
                "revision_id": item["revision_id"],
                "assessment_state": item["assessment_state"],
                "findings": raw_findings,
            }
        )
    summary, expected = validate_translation_model_output(
        bundle=bundle,
        output={"items": raw_items},
        policy=policy,
        policy_sha256=policy_sha256,
        evaluator=evaluator,
    )
    if expected != assessment:
        raise ValidationError("cached translation review assessment normalization is invalid")
    return summary, expected


def iter_assessment_findings(assessment: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for item in assessment.get("items", []):
        if isinstance(item, dict):
            for finding in item.get("findings", []):
                if isinstance(finding, dict):
                    yield finding
