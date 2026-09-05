#!/usr/bin/env python3
"""Offline closure checker for persisted Paseo STATE records.

This checker deliberately makes no Paseo, git, or network calls.  It verifies
only the persisted closure claims and their immutable, workspace-local inputs.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any

import review_evidence
import contextual_lane_manifest
import contextual_result_check
import surface_screen_manifest
import surface_screen_result_check


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / ".ai" / "legacy-cohort-manifest.json"
CANONICAL_STATES = frozenset({
    "PLAN", "IMPLEMENT", "VALIDATE", "REVIEW", "ADJUDICATE", "FIX",
    "RE_REVIEW", "FINAL_REVIEW", "FINAL_VALIDATE", "DONE", "STOP", "WAIT_USER",
})
ROLE_ALIASES = {
    "EXECUTOR": "EXECUTOR", "executor": "EXECUTOR",
    "REVIEWER": "REVIEWER", "reviewer": "REVIEWER",
    "SCOUT": "SCOUT", "scout": "SCOUT",
    "senior-reviewer": "senior-reviewer", "SENIOR_REVIEWER": "senior-reviewer",
}
KNOWN_REVIEW_CONTRACTS = {
    "code_legacy_v1": frozenset({"normal_review", "cross_review"}),
    "translation_contextual_v1": frozenset({"translation_contextual_v1"}),
    "translation_contextual_v2": frozenset({"translation_contextual_v2"}),
    "translation_surface_screen_v1": frozenset({"translation_surface_screen_v1"}),
}
PURPOSE_ROLES = {
    "normal_review": "REVIEWER",
    "translation_contextual_v1": "REVIEWER",
    "translation_contextual_v2": "REVIEWER",
    "translation_surface_screen_v1": "REVIEWER",
    "cross_review": "senior-reviewer",
    "scope_audit": "senior-reviewer",
}
COMPLETION_VALUES = frozenset({
    "completed", "completed_with_findings", "PASS", "CHANGES_REQUIRED", "FINDINGS", "OK",
})
SUCCESSFUL_COMPLETION_VALUES = frozenset({"completed", "PASS", "OK"})
CODE_DIFF_NAME = re.compile(r"^CODE_DIFF-([A-Za-z0-9_]+)-(\d+)-(\d+)\.patch$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_IDENTITY = re.compile(r"^(?:commit:[0-9a-f]{40}|snapshot:[0-9a-f]{64})$")
CITED_REVIEW_PATH = re.compile(
    r"(?<![A-Za-z0-9_./-])\.ai/reviews/[^/\s]+/"
    r"(?:review-[0-9]{2}|senior-audit-[0-9]{2})\.json(?![A-Za-z0-9_.-])"
)
CONTEXTUAL_PAYLOAD_KEYS = frozenset({
    "contract", "ordered_revision_keys", "translation_snapshot",
    "fixed_source_identity", "terminology_snapshot", "bounded_context",
    "rendered_briefing",
})
CONTEXTUAL_REVIEW_KINDS = frozenset({"full", "closure"})
CLOSURE_REASONS = frozenset({
    "changed_target", "open_finding", "shared_runtime_key",
    "narrative_or_term_claim", "extra_touched_target",
})


@dataclass(frozen=True)
class CheckResult:
    outcome: str
    detail: str
    exit_code: int


class InputError(Exception):
    """An unreadable, malformed, unsafe, or otherwise unusable input."""


class ContractError(Exception):
    """A readable JSON value that violates the new-contract schema."""


def _result(outcome: str, detail: str, exit_code: int) -> CheckResult:
    return CheckResult(outcome, detail, exit_code)


def _read_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_bytes().decode("utf-8"))
    except OSError as error:
        raise InputError(f"cannot read {label}: {error}") from error
    except UnicodeDecodeError as error:
        raise InputError(f"{label} is not UTF-8: {error}") from error
    except json.JSONDecodeError as error:
        raise InputError(f"{label} is not valid JSON: {error}") from error


def _ordinary_workspace_file(
    value: object, label: str, *, root: Path = ROOT
) -> Path:
    """Resolve one existing ordinary, repository-relative file or fail closed."""
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty workspace-relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise InputError(f"{label} escapes the workspace: {value!r}")
    root = root.resolve()
    candidate = root / relative
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise InputError(f"{label} is not an existing workspace file: {value!r}") from error
    if candidate.is_symlink() or not resolved.is_file():
        raise InputError(f"{label} must name an ordinary file: {value!r}")
    return resolved


def _normalize_role(value: object) -> str | None:
    return ROLE_ALIASES.get(value) if isinstance(value, str) else None


def _lifecycle(dispatch: dict[str, Any]) -> object:
    if "lifecycle" in dispatch and "status" in dispatch:
        return None
    return dispatch.get("lifecycle", dispatch.get("status"))


def _archived(dispatch: dict[str, Any]) -> bool:
    return _lifecycle(dispatch) == "archived" and dispatch.get("archive_confirmed") is True


def _is_json_value(value: object) -> bool:
    if value is None or isinstance(value, (str, bool)):
        return True
    if type(value) is int:
        return True
    if type(value) is float:
        return math.isfinite(value)
    if isinstance(value, list):
        return all(_is_json_value(item) for item in value)
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and _is_json_value(item)
            for key, item in value.items()
        )
    return False


def _runtime_observation_valid(value: object) -> tuple[bool, str]:
    fields = {"provider", "model", "mode", "thinking"}
    expected = {
        "schema_version", "source", "captured_at", "capture_status", *fields,
    }
    if not isinstance(value, dict) or set(value) != expected:
        return False, "must be an exact runtime_observation object"
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        return False, "schema_version must be integer 1"
    if value["source"] != "live_agent_metadata":
        return False, "source must be live_agent_metadata"
    if not isinstance(value["captured_at"], str) or not value["captured_at"]:
        return False, "captured_at must be a non-empty string"
    if value["capture_status"] != "captured":
        return False, "capture_status must be captured"
    for field in fields:
        observation = value[field]
        if not isinstance(observation, dict):
            return False, f"{field} must be a FieldObservation object"
        presence = observation.get("presence")
        if presence == "missing" and set(observation) == {"presence"}:
            continue
        if (
            presence == "present"
            and set(observation) == {"presence", "value"}
            and _is_json_value(observation["value"])
        ):
            continue
        return False, f"{field} must be exact present/value or missing form"
    return True, "ok"


def _runtime_observation_placement_valid(value: object) -> tuple[bool, str]:
    """Allow observations only on direct dispatches and ignore their raw-value subtrees."""
    def walk(node: object, path: tuple[object, ...]) -> tuple[bool, str]:
        if isinstance(node, dict):
            for key, item in node.items():
                if key == "runtime_observation":
                    direct_dispatch = (
                        len(path) == 2
                        and path[0] == "child_dispatches"
                        and type(path[1]) is int
                    )
                    if not direct_dispatch:
                        return False, f"runtime_observation is forbidden at STATE path {path!r}"
                    valid, detail = _runtime_observation_valid(item)
                    if not valid:
                        return False, f"runtime_observation {detail}"
                    continue
                valid, detail = walk(item, (*path, key))
                if not valid:
                    return valid, detail
        elif isinstance(node, list):
            for index, item in enumerate(node):
                valid, detail = walk(item, (*path, index))
                if not valid:
                    return valid, detail
        return True, "ok"

    return walk(value, ())


def _contains_key(value: object, needle: str) -> bool:
    if isinstance(value, dict):
        return needle in value or any(_contains_key(item, needle) for item in value.values())
    if isinstance(value, list):
        return any(_contains_key(item, needle) for item in value)
    return False


def _schema_valid(state: dict[str, Any]) -> tuple[bool, str]:
    placement = _runtime_observation_placement_valid(state)
    if not placement[0]:
        return placement
    children = state.get("child_dispatches")
    if children is not None and not isinstance(children, list):
        return False, "child_dispatches must be a list or null"
    orchestrator_agent_id = state.get("orchestrator_agent_id")
    seen_ids: set[str] = set()
    for index, dispatch in enumerate(children or []):
        if not isinstance(dispatch, dict):
            return False, f"child_dispatches[{index}] must be an object"
        dispatch_id = dispatch.get("dispatch_id")
        if not isinstance(dispatch_id, str) or not dispatch_id:
            return False, f"dispatch {dispatch_id!r} must have a non-empty string dispatch_id"
        if dispatch_id in seen_ids:
            return False, f"duplicate dispatch_id {dispatch_id!r}"
        seen_ids.add(dispatch_id)
        agent_id = dispatch.get("agent_id")
        if not isinstance(agent_id, str) or not agent_id:
            return False, f"dispatch {dispatch_id!r} must have a non-empty string agent_id"
        if agent_id == orchestrator_agent_id:
            return False, (
                f"dispatch {dispatch_id!r} agent_id must differ from "
                "orchestrator_agent_id"
            )
        if "purpose" in dispatch and (
            not isinstance(dispatch["purpose"], str) or not dispatch["purpose"]
        ):
            return False, f"dispatch {dispatch_id!r} purpose must be a non-empty string when present"
        if "lifecycle" in dispatch and "status" in dispatch:
            return False, f"dispatch {dispatch_id!r} has both lifecycle and status"
        if _normalize_role(dispatch.get("role")) is None:
            return False, f"dispatch {dispatch_id!r} has unknown role {dispatch.get('role')!r}"
    return True, "ok"


def _strict_manifest(path: Path) -> frozenset[str]:
    raw = _read_json(path, "adoption-boundary manifest")
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "unsupported_tasks"}:
        raise ValueError("manifest must have exactly schema_version and unsupported_tasks")
    tasks = raw.get("unsupported_tasks")
    if type(raw.get("schema_version")) is not int or raw.get("schema_version") != 1 or not isinstance(tasks, list):
        raise ValueError("manifest schema_version must be 1 and unsupported_tasks must be an array")
    if any(not isinstance(task_id, str) or not task_id for task_id in tasks):
        raise ValueError("manifest unsupported_tasks must contain non-empty task-id strings")
    if tasks != sorted(tasks) or len(tasks) != len(set(tasks)):
        raise ValueError("manifest unsupported_tasks must be lexically sorted and unique")
    return frozenset(tasks)


def _record_paths(state: dict[str, Any], *, root: Path = ROOT) -> list[Path]:
    paths: list[Path] = []
    for field in ("review_records", "senior_review_records"):
        value = state.get(field, [])
        if value is None:
            value = []
        if isinstance(value, dict):  # Reader-only compatibility with old mappings.
            value = list(value.values())
        if not isinstance(value, list):
            raise ContractError(f"{field} must be an array (or legacy mapping)")
        for index, item in enumerate(value):
            paths.append(_ordinary_workspace_file(item, f"{field}[{index}]", root=root))
    return paths


def _load_records(
    state: dict[str, Any], *, root: Path = ROOT
) -> list[tuple[dict[str, Any], Path]]:
    loaded: list[tuple[dict[str, Any], Path]] = []
    for path in _record_paths(state, root=root):
        record = _read_json(path, f"review record {path.relative_to(root)}")
        if not isinstance(record, dict):
            raise ContractError(f"review record {path.relative_to(root)} must be an object")
        if _contains_key(record, "runtime_observation"):
            raise ContractError(
                f"review record {path.relative_to(root)} forbids runtime_observation at any depth"
            )
        loaded.append((record, path))
    return loaded


def _stop_records_forbid_runtime_observation(
    state: dict[str, Any], *, root: Path = ROOT
) -> tuple[bool, str]:
    """Best-effort STOP audit without making review records a STOP prerequisite."""
    for field in ("review_records", "senior_review_records"):
        locators = state.get(field, [])
        if isinstance(locators, dict):
            locators = list(locators.values())
        if not isinstance(locators, list):
            continue
        for index, locator in enumerate(locators):
            try:
                path = _ordinary_workspace_file(
                    locator, f"{field}[{index}]", root=root
                )
                record = _read_json(
                    path, f"review record {path.relative_to(root)}"
                )
            except (ContractError, InputError, OSError, ValueError):
                continue
            if isinstance(record, dict) and _contains_key(
                record, "runtime_observation"
            ):
                return False, (
                    f"review record {path.relative_to(root)} forbids "
                    "runtime_observation at any depth"
                )
    return True, "ok"


def _dispatches(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    children = state.get("child_dispatches")
    if not isinstance(children, list):
        return {}
    return {
        entry["dispatch_id"]: entry
        for entry in children
        if isinstance(entry, dict) and isinstance(entry.get("dispatch_id"), str)
    }


def _completion_records(
    state: dict[str, Any], records: list[tuple[dict[str, Any], Path]]
) -> list[tuple[dict[str, Any], dict[str, Any], Path]]:
    contracts = state.get("review_contracts")
    if not isinstance(contracts, list):
        return []
    dispatches = _dispatches(state)
    result: list[tuple[dict[str, Any], dict[str, Any], Path]] = []
    for record, path in records:
        dispatch_id = record.get("dispatch_id")
        dispatch = dispatches.get(dispatch_id) if isinstance(dispatch_id, str) else None
        contract = record.get("review_contract")
        purpose = record.get("purpose")
        allowed_purposes = (
            KNOWN_REVIEW_CONTRACTS.get(contract)
            if isinstance(contract, str)
            else None
        )
        if (
            contract in contracts
            and allowed_purposes is not None
            and isinstance(purpose, str)
            and purpose in allowed_purposes
            and dispatch is not None
            and dispatch.get("purpose") == purpose
            and PURPOSE_ROLES.get(purpose) == _normalize_role(dispatch.get("role"))
            and PURPOSE_ROLES.get(purpose) == _normalize_role(record.get("reviewer_role"))
            and isinstance(record.get("dispatch_id"), str)
            and bool(record.get("dispatch_id"))
            and isinstance(record.get("agent_id"), str)
            and bool(record.get("agent_id"))
            and isinstance(dispatch.get("dispatch_id"), str)
            and bool(dispatch.get("dispatch_id"))
            and isinstance(dispatch.get("agent_id"), str)
            and bool(dispatch.get("agent_id"))
            and record.get("agent_id") == dispatch.get("agent_id")
        ):
            result.append((record, dispatch, path))
    return result


def _review_contracts_closed(state: dict[str, Any]) -> tuple[bool, str]:
    contracts = state.get("review_contracts")
    if not isinstance(contracts, list) or not contracts or any(not isinstance(x, str) or not x for x in contracts):
        return False, "review_contracts must be a non-empty array of strings"
    if len(contracts) != len(set(contracts)):
        return False, "review_contracts must be unique"
    if {"translation_contextual_v1", "translation_contextual_v2"} <= set(contracts):
        return False, "translation_contextual_v1 and translation_contextual_v2 cannot be mixed"
    if "translation_surface_screen_v1" in contracts and {"translation_contextual_v1", "translation_contextual_v2"} & set(contracts):
        return False, "translation_surface_screen_v1 cannot be mixed with contextual review contracts"
    if "translation_contextual_v2" in contracts and (
        type(state.get("schema_version")) is not int or state["schema_version"] < 5
    ):
        return False, "translation_contextual_v2 requires schema_version >= 5"
    if "translation_surface_screen_v1" in contracts and (
        type(state.get("schema_version")) is not int or state["schema_version"] < 5
    ):
        return False, "translation_surface_screen_v1 requires schema_version >= 5"
    unknown = [contract for contract in contracts if contract not in KNOWN_REVIEW_CONTRACTS]
    if unknown:
        return False, f"unknown review_contract {unknown[0]!r}"
    if state.get("pending_review_contracts") != []:
        return False, "pending_review_contracts must be []"
    completed = state.get("completed_review_contracts")
    if (
        not isinstance(completed, list)
        or any(not isinstance(contract, str) for contract in completed)
        or set(completed) != set(contracts)
    ):
        return False, "completed_review_contracts must be set-equal to review_contracts"
    return True, "ok"


def _completion_records_bound(
    state: dict[str, Any], records: list[tuple[dict[str, Any], dict[str, Any], Path]]
) -> tuple[bool, str]:
    covered = {record.get("review_contract") for record, _, _ in records}
    # The surface zero/no-dispatch artifact is the honest n=0 terminal: the
    # contract is closed by the bound artifact exactly when it has no records.
    zero_terminal = (
        isinstance(state.get("surface_zero_path"), str)
        and "translation_surface_screen_v1" in state.get("review_contracts", [])
        and not any(
            record.get("review_contract") == "translation_surface_screen_v1"
            for record, _, _ in records
        )
    )
    for contract in state["review_contracts"]:
        if contract not in covered and not (contract == "translation_surface_screen_v1" and zero_terminal):
            return False, f"no bound completion record for contract {contract!r}"
    for _, dispatch, _ in records:
        if not _archived(dispatch):
            return False, f"completion dispatch {dispatch.get('dispatch_id')!r} is not archived and confirmed"
    return True, "ok"


def candidate_ref(spec_bytes: bytes, diff_bytes: bytes) -> str:
    """Return SHA256(SPEC raw bytes + NUL + CODE_DIFF raw bytes)."""
    return hashlib.sha256(spec_bytes + b"\0" + diff_bytes).hexdigest()


def _read_candidate_bytes(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise InputError(f"cannot read {label}: {error}") from error


def _canonical_contextual_payload_bytes(payload: object, *, expected_contract: str) -> bytes:
    if not isinstance(payload, dict) or frozenset(payload) != CONTEXTUAL_PAYLOAD_KEYS:
        raise ContractError("contextual envelope payload must have exactly the seven canonical keys")
    required_strings = ("fixed_source_identity", "terminology_snapshot", "rendered_briefing")
    if (
        payload.get("contract") != expected_contract
        or any(not isinstance(payload.get(key), str) for key in required_strings)
        or not isinstance(payload.get("ordered_revision_keys"), list)
        or any(not isinstance(item, str) for item in payload["ordered_revision_keys"])
        or not isinstance(payload.get("translation_snapshot"), list)
        or not isinstance(payload.get("bounded_context"), list)
    ):
        raise ContractError("contextual envelope payload has non-canonical field types")
    if not SOURCE_IDENTITY.fullmatch(payload["fixed_source_identity"]):
        raise ContractError("contextual envelope fixed_source_identity has an invalid typed form")
    if SHA256.search(payload["rendered_briefing"]):
        raise ContractError("contextual envelope rendered_briefing embeds a candidate identity")
    keys = payload["ordered_revision_keys"]
    translations = payload["translation_snapshot"]
    contexts = payload["bounded_context"]
    if expected_contract == "translation_contextual_v2" and (
        not keys or len(keys) != len(set(keys)) or any(not item for item in keys)
    ):
        raise ContractError("contextual v2 envelope revision keys must be non-empty and unique")
    for item in translations:
        if not isinstance(item, dict) or set(item) != {"revision_key", "source", "target"} or any(not isinstance(item.get(key), str) for key in item):
            raise ContractError("contextual envelope translation_snapshot must be an exact string-object array")
        if expected_contract == "translation_contextual_v2" and not item["source"]:
            raise ContractError("contextual v2 envelope sources must be non-empty")
    for item in contexts:
        if not isinstance(item, dict) or set(item) != {"revision_key", "context"} or any(not isinstance(item.get(key), str) for key in item):
            raise ContractError("contextual envelope bounded_context must be an exact string-object array")
    if [item["revision_key"] for item in translations] != keys or [item["revision_key"] for item in contexts] != keys:
        raise ContractError("contextual envelope revision-key arrays must match ordered_revision_keys")
    try:
        options = {
            "ensure_ascii": False,
            "sort_keys": True,
            "separators": (",", ":"),
        }
        if expected_contract == "translation_contextual_v2":
            options["allow_nan"] = False
        return json.dumps(payload, **options).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContractError(f"contextual envelope payload is not canonicalizable: {error}") from error


def _canonical_payload_bytes(payload: object) -> bytes:
    """Backward-compatible v1 wrapper; untrusted payloads cannot select a contract."""
    return _canonical_contextual_payload_bytes(
        payload, expected_contract="translation_contextual_v1"
    )


def _has_completion_indicator(record: dict[str, Any]) -> bool:
    present = [key for key in ("status", "result") if key in record]
    return bool(present) and all(
        isinstance(record[key], str) and record[key] in COMPLETION_VALUES for key in present
    )


def _has_successful_completion(record: dict[str, Any]) -> bool:
    if "result" in record:
        return record["result"] in SUCCESSFUL_COMPLETION_VALUES
    return record.get("status") in SUCCESSFUL_COMPLETION_VALUES


def _translation_convergence_enabled(state: dict[str, Any]) -> bool:
    contracts = state.get("review_contracts")
    return (
        type(state.get("schema_version")) is int
        and state["schema_version"] >= 4
        and state.get("mode") == "implement"
        and isinstance(contracts, list)
        and "translation_contextual_v1" in contracts
    )


def _contextual_payload(
    record: dict[str, Any], *, root: Path
) -> dict[str, Any]:
    envelope = _read_json(
        _ordinary_workspace_file(
            record.get("input_path"), "contextual input_path", root=root
        ),
        "contextual envelope",
    )
    if not isinstance(envelope, dict) or not isinstance(envelope.get("payload"), dict):
        raise ContractError("contextual envelope payload must be an object")
    return envelope["payload"]


def _surface_payload(
    record: dict[str, Any], *, root: Path
) -> dict[str, Any]:
    envelope = _read_json(
        _ordinary_workspace_file(
            record.get("input_path"), "surface input_path", root=root
        ),
        "surface envelope",
    )
    if not isinstance(envelope, dict) or not isinstance(envelope.get("payload"), dict):
        raise ContractError("surface envelope payload must be an object")
    return envelope["payload"]


def _surface_entry_keys(entries: list[dict[str, Any]]) -> list[str]:
    keys = [entry.get("entry_revision_identity") for entry in entries]
    if any(not isinstance(key, str) or not key for key in keys):
        raise ContractError("surface entries must carry entry_revision_identity strings")
    return keys  # type: ignore[return-value]


def _translation_convergence_valid(
    state: dict[str, Any],
    loaded: list[tuple[dict[str, Any], Path]],
    bound_records: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *,
    root: Path = ROOT,
) -> tuple[bool, str]:
    """Validate schema-4 translation full/closure/full convergence records."""
    if not _translation_convergence_enabled(state):
        return True, "ok"

    cycle = state.get("cycle")
    max_cycles = state.get("max_cycles", 3)
    if type(cycle) is not int or cycle < 0:
        return False, "cycle must be a non-negative integer"
    if type(max_cycles) is not int or max_cycles < 1:
        return False, "max_cycles must be a positive integer (default 3)"
    if max_cycles > 3 and state.get("max_cycles_user_authorized") is not True:
        return False, "max_cycles greater than 3 requires literal max_cycles_user_authorized=true"
    if cycle > max_cycles:
        return False, "cycle must not exceed max_cycles"

    contextual = [
        item for item in loaded
        if item[0].get("review_contract") == "translation_contextual_v1"
        and item[0].get("purpose") == "translation_contextual_v1"
        and _has_completion_indicator(item[0])
    ]
    if not contextual:
        return False, "no bound contextual terminal records"
    bound_paths = [
        path for record, _, path in bound_records
        if record.get("review_contract") == "translation_contextual_v1"
        and record.get("purpose") == "translation_contextual_v1"
    ]
    for _, path in contextual:
        if path not in bound_paths:
            return False, f"{path.relative_to(root)} contextual terminal record is not dispatch-bound"

    enriched: list[
        tuple[dict[str, Any], Path, tuple[int, int], dict[str, Any]]
    ] = []
    for record, path in contextual:
        relative = path.relative_to(root)
        kind = record.get("review_kind")
        if kind not in CONTEXTUAL_REVIEW_KINDS:
            return False, f"{relative} review_kind must be full or closure"
        phase = record.get("review_phase")
        if phase not in {"REVIEW", "RE_REVIEW", "FINAL_REVIEW"}:
            return False, f"{relative} has an invalid contextual review_phase"
        record_cycle, attempt = record.get("cycle"), record.get("attempt")
        if (
            type(record_cycle) is not int or record_cycle < 0
            or type(attempt) is not int or attempt < 1
        ):
            return False, f"{relative} cycle/attempt must be non-negative/positive integers"
        if record_cycle > max_cycles:
            return False, f"{relative} contextual record cycle must not exceed max_cycles"
        if record_cycle > cycle:
            return False, f"{relative} contextual record cycle must not exceed STATE.cycle"
        payload = _contextual_payload(record, root=root)
        keys = payload.get("ordered_revision_keys")
        if not isinstance(keys, list) or not keys or len(keys) != len(set(keys)):
            return False, f"{relative} contextual workset keys must be non-empty and unique"
        enriched.append((record, path, (record_cycle, attempt), payload))

    ordered = sorted(enriched, key=lambda item: item[2])
    for earlier, later in zip(ordered, ordered[1:]):
        if earlier[2] == later[2]:
            return False, "contextual terminal (cycle, attempt) tuples must be unique"

    initial_record, _, initial_key, initial_payload = ordered[0]
    if (
        initial_key[0] != 0
        or initial_record.get("review_phase") != "REVIEW"
        or initial_record.get("review_kind") != "full"
    ):
        return False, "earliest contextual terminal record must be REVIEW/full at cycle 0"

    for index, (record, path, record_key, _) in enumerate(ordered[1:-1], start=1):
        phase, kind = record.get("review_phase"), record.get("review_kind")
        if phase == "RE_REVIEW" and kind in CONTEXTUAL_REVIEW_KINDS:
            continue
        if phase == "FINAL_REVIEW" and kind == "full" and not _has_successful_completion(record):
            has_higher_cycle_repair = any(
                later_record.get("review_phase") == "RE_REVIEW"
                and later_record.get("review_kind") in CONTEXTUAL_REVIEW_KINDS
                and later_key[0] > record_key[0]
                for later_record, _, later_key, _ in ordered[index + 1:-1]
            )
            if has_higher_cycle_repair:
                continue
        return False, (
            f"{path.relative_to(root)} intervening contextual terminal record must be "
            "RE_REVIEW/full, RE_REVIEW/closure, or an unsuccessful FINAL_REVIEW/full "
            "followed by a higher-cycle RE_REVIEW"
        )

    full_keys = initial_payload["ordered_revision_keys"]
    full_sources = {
        item["revision_key"]: item["source"]
        for item in initial_payload["translation_snapshot"]
    }

    full_records = [item for item in enriched if item[0].get("review_kind") == "full"]
    for _, path, _, payload in full_records:
        relative = path.relative_to(root)
        if payload["ordered_revision_keys"] != full_keys:
            return False, f"{relative} full review does not cover the original ordered workset"
        sources = [item["source"] for item in payload["translation_snapshot"]]
        if sources != [full_sources[key] for key in full_keys]:
            return False, f"{relative} full review sources drift from the original workset"

    for record, path, record_key, payload in enriched:
        if record.get("review_kind") != "closure":
            continue
        relative = path.relative_to(root)
        if record.get("review_phase") != "RE_REVIEW":
            return False, f"{relative} closure review is only valid in RE_REVIEW"
        inclusion = record.get("inclusion")
        if not isinstance(inclusion, list) or not inclusion:
            return False, f"{relative} closure inclusion must be a non-empty array"
        inclusion_keys: list[str] = []
        for index, entry in enumerate(inclusion):
            if not isinstance(entry, dict) or set(entry) != {"revision_key", "reasons"}:
                return False, f"{relative} inclusion[{index}] must have exactly revision_key and reasons"
            revision_key, reasons = entry.get("revision_key"), entry.get("reasons")
            if (
                not isinstance(revision_key, str) or not revision_key
                or not isinstance(reasons, list) or not reasons
                or any(not isinstance(reason, str) or reason not in CLOSURE_REASONS for reason in reasons)
                or len(reasons) != len(set(reasons))
            ):
                return False, f"{relative} inclusion[{index}] has an invalid key or reasons"
            inclusion_keys.append(revision_key)
        closure_keys = payload["ordered_revision_keys"]
        if closure_keys != inclusion_keys:
            return False, f"{relative} closure keys do not equal ordered inclusion keys"
        closure_key_set = set(closure_keys)
        if [key for key in full_keys if key in closure_key_set] != closure_keys:
            return False, f"{relative} closure keys are not an ordered subset of the full workset"
        closure_sources = [item["source"] for item in payload["translation_snapshot"]]
        if closure_sources != [full_sources.get(key) for key in closure_keys]:
            return False, f"{relative} closure sources drift from the full workset"
        earlier_full = [item for item in full_records if item[2] < record_key]
        if not earlier_full:
            return False, f"{relative} closure has no earlier full review"
        parent_key = max(item[2] for item in earlier_full)
        parent = [item for item in earlier_full if item[2] == parent_key]
        if len(parent) != 1:
            return False, f"{relative} latest earlier full review is not unique"
        parent_identity = record.get("parent_candidate_identity")
        if (
            not isinstance(parent_identity, str)
            or not SHA256.fullmatch(parent_identity)
            or parent_identity != parent[0][0].get("candidate_identity")
        ):
            return False, f"{relative} parent_candidate_identity does not bind the latest earlier full review"

    latest_record, _, latest_key, _ = ordered[-1]
    if (
        latest_record.get("review_phase") != "FINAL_REVIEW"
        or latest_record.get("review_kind") != "full"
        or not _has_successful_completion(latest_record)
    ):
        return False, "latest contextual terminal record must be a successful FINAL_REVIEW/full"
    if latest_key[0] != cycle:
        return False, "latest FINAL_REVIEW/full cycle must equal STATE.cycle"
    return True, "ok"


def _v2_enabled(state: dict[str, Any]) -> bool:
    return (
        type(state.get("schema_version")) is int
        and state["schema_version"] >= 5
        and isinstance(state.get("review_contracts"), list)
        and "translation_contextual_v2" in state["review_contracts"]
    )


def _v2_pointer_valid(
    state: dict[str, Any], contextual: list[tuple[dict[str, Any], dict[str, Any], Path]],
) -> tuple[bool, str]:
    if "contextual_reviewer" in state:
        return False, "v2 forbids singular contextual_reviewer"
    pointers = state.get("contextual_reviewers")
    if not isinstance(pointers, list) or not pointers:
        return False, "v2 contextual_reviewers must be a non-empty array"
    terminal = sorted(
        contextual,
        key=lambda item: (
            item[0].get("cycle", -1), item[0].get("attempt", -1),
            item[0].get("lane", {}).get("index", 0)
            if isinstance(item[0].get("lane"), dict) else 0,
        ),
    )
    latest_record, latest_dispatch, _ = terminal[-1]
    if latest_record.get("review_kind") == "lane":
        stage = [
            item for item in terminal
            if (item[0].get("cycle"), item[0].get("attempt"))
            == (latest_record.get("cycle"), latest_record.get("attempt"))
        ]
    else:
        stage = [(latest_record, latest_dispatch, terminal[-1][2])]
    if len(pointers) != len(stage):
        return False, "contextual_reviewers must point to every member of the current stage"
    expected_common = {"role", "purpose", "candidate_identity", "dispatch_id", "input_path", "agent_id"}
    for index, (pointer, (record, dispatch, _)) in enumerate(zip(pointers, stage)):
        if not isinstance(pointer, dict):
            return False, f"contextual_reviewers[{index}] must be an object"
        lane = record.get("lane")
        expected_keys = expected_common | ({"lane_group_identity", "lane_index"} if isinstance(lane, dict) else set())
        if set(pointer) != expected_keys:
            return False, f"contextual_reviewers[{index}] has an invalid exact shape"
        expected = {
            "role": "REVIEWER", "purpose": "translation_contextual_v2",
            "candidate_identity": record.get("candidate_identity"),
            "dispatch_id": record.get("dispatch_id"), "input_path": record.get("input_path"),
            "agent_id": record.get("agent_id"),
        }
        if isinstance(lane, dict):
            expected.update({"lane_group_identity": lane.get("group_identity"), "lane_index": lane.get("index")})
        if pointer != expected or dispatch.get("agent_id") != pointer.get("agent_id"):
            return False, f"contextual_reviewers[{index}] does not bind the current dispatch"
    return True, "ok"


def _creation_lane_label_matches(value: object, index: int) -> bool:
    """Accept only exact transport strings or historical JSON integer labels."""
    if type(value) is int:
        return 1 <= value <= 4 and value == index
    return type(value) is str and value in ("1", "2", "3", "4") and value == str(index)


def _claim_lane_group_identifiers(
    group_id: str,
    group_identity: str,
    group_manifest_path: str,
    *,
    used_group_ids: set[str],
    used_group_identities: set[str],
    used_group_manifest_paths: set[str],
) -> tuple[bool, str]:
    for value, used, label in (
        (group_id, used_group_ids, "group_id"),
        (group_identity, used_group_identities, "group_identity"),
        (group_manifest_path, used_group_manifest_paths, "group_manifest_path"),
    ):
        if value in used:
            return False, f"lane {label} must not be reused across stages"
    used_group_ids.add(group_id)
    used_group_identities.add(group_identity)
    used_group_manifest_paths.add(group_manifest_path)
    return True, "ok"


def _translation_v2_convergence_valid(
    state: dict[str, Any], loaded: list[tuple[dict[str, Any], Path]],
    bound_records: list[tuple[dict[str, Any], dict[str, Any], Path]], *, root: Path = ROOT,
) -> tuple[bool, str]:
    if not _v2_enabled(state):
        return True, "ok"
    contextual_loaded = [
        (record, path) for record, path in loaded
        if record.get("review_contract") == "translation_contextual_v2"
        and record.get("purpose") == "translation_contextual_v2"
        and _has_completion_indicator(record)
    ]
    contextual = [
        item for item in bound_records
        if item[0].get("review_contract") == "translation_contextual_v2"
        and item[0].get("purpose") == "translation_contextual_v2"
    ]
    if not contextual_loaded or len(contextual_loaded) != len(contextual):
        return False, "every v2 terminal record must be dispatch-bound"
    pointer = _v2_pointer_valid(state, contextual)
    if not pointer[0]:
        return pointer
    if state.get("mode") == "review_only":
        if len(contextual) != 1:
            return False, "review-only v2 requires exactly one full record"
        record = contextual[0][0]
        if record.get("review_kind") != "full" or "lane" in record:
            return False, "review-only v2 permits only a single full review"
        return True, "ok"
    if state.get("mode") != "implement":
        return False, "v2 mode must be implement or review_only"
    cycle = state.get("cycle")
    max_cycles = state.get("max_cycles", 3)
    if type(cycle) is not int or cycle < 0 or type(max_cycles) is not int or max_cycles < 1:
        return False, "cycle/max_cycles have invalid values"
    if max_cycles > 3 and state.get("max_cycles_user_authorized") is not True:
        return False, "max_cycles greater than 3 requires literal max_cycles_user_authorized=true"
    if cycle > max_cycles:
        return False, "cycle must not exceed max_cycles"

    enriched: list[tuple[dict[str, Any], dict[str, Any], Path, tuple[int, int, int], dict[str, Any]]] = []
    for record, dispatch, path in contextual:
        relative = path.relative_to(root)
        phase, kind = record.get("review_phase"), record.get("review_kind")
        record_cycle, attempt = record.get("cycle"), record.get("attempt")
        if phase not in {"REVIEW", "RE_REVIEW", "FINAL_REVIEW"} or kind not in {"full", "closure", "lane"}:
            return False, f"{relative} has an invalid v2 phase/review_kind"
        if type(record_cycle) is not int or record_cycle < 0 or type(attempt) is not int or attempt < 1:
            return False, f"{relative} cycle/attempt have invalid values"
        if record_cycle > cycle or record_cycle > max_cycles:
            return False, f"{relative} cycle exceeds STATE bounds"
        member = 0
        if kind == "lane":
            lane = record.get("lane")
            if not isinstance(lane, dict) or set(lane) != {
                "group_id", "group_identity", "group_manifest_path", "index",
                "count", "offset", "length",
            }:
                return False, f"{relative} lane has an invalid exact shape"
            member = lane.get("index")
            if type(member) is not int:
                return False, f"{relative} lane index must be an integer"
        elif "lane" in record:
            return False, f"{relative} non-lane record must not contain lane"
        payload = _contextual_payload(record, root=root)
        enriched.append((record, dispatch, path, (record_cycle, attempt, member), payload))

    coordinates = [item[3] for item in enriched]
    if len(coordinates) != len(set(coordinates)):
        return False, "v2 terminal three-dimensional coordinates must be unique"
    stages: dict[tuple[int, int], list[tuple[dict[str, Any], dict[str, Any], Path, tuple[int, int, int], dict[str, Any]]]] = {}
    for item in enriched:
        stages.setdefault(item[3][:2], []).append(item)
    used_group_ids: set[str] = set()
    used_group_identities: set[str] = set()
    used_group_manifest_paths: set[str] = set()
    stage_info: list[tuple[tuple[int, int], str, str, list[str], list[str], str, str]] = []
    # stage tuple, coverage kind, identity, keys, sources, phase, fixed source identity
    for stage_key in sorted(stages):
        members = sorted(stages[stage_key], key=lambda item: item[3][2])
        kinds = {item[0]["review_kind"] for item in members}
        phases = {item[0]["review_phase"] for item in members}
        if len(kinds) != 1 or len(phases) != 1:
            return False, "v2 stage must not mix review kinds or phases"
        kind, phase = next(iter(kinds)), next(iter(phases))
        if kind != "lane":
            if len(members) != 1 or members[0][3][2] != 0:
                return False, "full/closure stage must contain one member ordinal 0"
            payload = members[0][4]
            identity = members[0][0].get("candidate_identity")
            coverage_kind = "full" if kind == "full" else "closure"
            stage_info.append((stage_key, coverage_kind, str(identity), payload["ordered_revision_keys"], [x["source"] for x in payload["translation_snapshot"]], phase, payload["fixed_source_identity"]))
            continue
        if phase == "FINAL_REVIEW":
            return False, "FINAL_REVIEW forbids lane review"
        if len(members) != 4 or [item[3][2] for item in members] != [1, 2, 3, 4]:
            return False, "lane stage must contain exactly members 1..4"
        agents = [item[0].get("agent_id") for item in members]
        dispatch_ids = [item[0].get("dispatch_id") for item in members]
        if len(set(agents)) != 4 or len(set(dispatch_ids)) != 4:
            return False, "lane stage requires four distinct agents and dispatches"
        first_lane = members[0][0]["lane"]
        group_tuple = (first_lane["group_id"], first_lane["group_identity"], first_lane["group_manifest_path"])
        claimed = _claim_lane_group_identifiers(
            *group_tuple,
            used_group_ids=used_group_ids,
            used_group_identities=used_group_identities,
            used_group_manifest_paths=used_group_manifest_paths,
        )
        if not claimed[0]:
            return claimed
        manifest_path = _ordinary_workspace_file(
            first_lane["group_manifest_path"], "group_manifest_path", root=root
        )
        manifest_bytes = manifest_path.read_bytes()
        manifest = contextual_result_check.strict_json_bytes(
            manifest_bytes, label="lane manifest"
        )
        if manifest_bytes != contextual_lane_manifest.canonical_bytes(manifest):
            return False, "lane manifest bytes are not canonical compact JSON"
        contextual_lane_manifest.validate_manifest(
            manifest, root=root, manifest_path=first_lane["group_manifest_path"]
        )
        manifest_payload = manifest["payload"]
        if (
            manifest.get("group_identity") != first_lane["group_identity"]
            or manifest_payload.get("task_id") != state.get("task_id")
            or manifest_payload.get("group_id") != first_lane["group_id"]
            or manifest_payload.get("review_phase") != phase
            or (manifest_payload.get("cycle"), manifest_payload.get("attempt")) != stage_key
        ):
            return False, "lane manifest does not bind its stage"
        boundaries = manifest_payload["lane_boundaries"]
        manifest_lanes = manifest_payload["lanes"]
        for index, (item, boundary, manifest_lane) in enumerate(zip(members, boundaries, manifest_lanes), 1):
            record, dispatch = item[0], item[1]
            lane = record["lane"]
            if (
                (lane["group_id"], lane["group_identity"], lane["group_manifest_path"])
                != group_tuple or lane["count"] != 4
                or (lane["index"], lane["offset"], lane["length"])
                != (boundary["index"], boundary["offset"], boundary["length"])
                or record.get("dispatch_id") != manifest_lane["dispatch_id"]
                or record.get("input_path") != manifest_lane["input_path"]
                or record.get("candidate_identity") != manifest_lane["candidate_identity"]
                or dispatch.get("lane_group_identity") != lane["group_identity"]
                or dispatch.get("lane_index") != index
            ):
                return False, f"lane {index} record/dispatch/manifest binding mismatch"
            labels = dispatch.get("labels")
            if (
                not isinstance(labels, dict)
                or labels.get("lane_group_identity") != lane["group_identity"]
                or not _creation_lane_label_matches(labels.get("lane_index"), index)
            ):
                return False, f"lane {index} creation labels do not bind group/index"
        workset = manifest_payload["workset"]
        stage_info.append((stage_key, "lane_group", manifest["group_identity"], workset["ordered_revision_keys"], [x["source"] for x in workset["translation_snapshot"]], phase, workset["fixed_source_identity"]))

    stage_info.sort(key=lambda item: item[0])
    origin = stage_info[0]
    if origin[0][0] != 0 or origin[5] != "REVIEW" or origin[1] not in {"full", "lane_group"}:
        return False, "earliest v2 stage must be cycle-0 REVIEW/full or REVIEW/lane_group"
    origin_keys, origin_sources, origin_source_identity = origin[3], origin[4], origin[6]
    if len(origin_keys) < 4 and origin[1] == "lane_group":
        return False, "worksets smaller than four revisions must use full"
    for stage in stage_info:
        if stage[1] in {"full", "lane_group"} and (
            stage[3] != origin_keys or stage[4] != origin_sources
            or stage[6] != origin_source_identity
        ):
            return False, "full-coverage stage drifts from origin keys/source"
    for index, stage in enumerate(stage_info[1:-1], 1):
        record_stage = stages[stage[0]]
        if stage[5] == "RE_REVIEW" and stage[1] in {"full", "closure", "lane_group"}:
            continue
        if stage[5] == "FINAL_REVIEW" and stage[1] == "full" and not _has_successful_completion(record_stage[0][0]):
            if any(later[5] == "RE_REVIEW" and later[0][0] > stage[0][0] for later in stage_info[index + 1:-1]):
                continue
        return False, "invalid intervening v2 stage"
    for stage in stage_info:
        if stage[1] != "closure":
            continue
        record = stages[stage[0]][0][0]
        if stage[5] != "RE_REVIEW":
            return False, "v2 closure is only valid in RE_REVIEW"
        if "parent_candidate_identity" in record:
            return False, "v2 closure forbids parent_candidate_identity"
        inclusion = record.get("inclusion")
        if not isinstance(inclusion, list) or not inclusion:
            return False, "v2 closure inclusion must be non-empty"
        inclusion_keys: list[str] = []
        for entry in inclusion:
            if not isinstance(entry, dict) or set(entry) != {"revision_key", "reasons"}:
                return False, "v2 closure inclusion has an invalid shape"
            reasons = entry.get("reasons")
            if not isinstance(entry.get("revision_key"), str) or not entry["revision_key"] or not isinstance(reasons, list) or not reasons or len(reasons) != len(set(reasons)) or any(reason not in CLOSURE_REASONS for reason in reasons):
                return False, "v2 closure inclusion has invalid reasons"
            inclusion_keys.append(entry.get("revision_key"))
        if inclusion_keys != stage[3] or [key for key in origin_keys if key in set(inclusion_keys)] != inclusion_keys:
            return False, "v2 closure is not an ordered origin subset"
        expected_sources = [source for key, source in zip(origin_keys, origin_sources) if key in set(inclusion_keys)]
        if stage[4] != expected_sources:
            return False, "v2 closure source drift"
        earlier = [candidate for candidate in stage_info if candidate[0] < stage[0] and candidate[1] in {"full", "lane_group"}]
        if not earlier:
            return False, "v2 closure has no earlier full-coverage stage"
        parent = max(earlier, key=lambda item: item[0])
        if record.get("parent_review_kind") != parent[1] or record.get("parent_coverage_identity") != parent[2]:
            return False, "v2 closure parent coverage binding mismatch"
    latest = stage_info[-1]
    latest_record = stages[latest[0]][0][0]
    if latest[5] != "FINAL_REVIEW" or latest[1] != "full" or not _has_successful_completion(latest_record):
        return False, "latest v2 stage must be a successful FINAL_REVIEW/full"
    if latest[0][0] != cycle:
        return False, "latest v2 FINAL_REVIEW/full cycle must equal STATE.cycle"
    return True, "ok"


def _surface_enabled(state: dict[str, Any]) -> bool:
    return (
        type(state.get("schema_version")) is int
        and state["schema_version"] >= 5
        and isinstance(state.get("review_contracts"), list)
        and "translation_surface_screen_v1" in state["review_contracts"]
    )


def _load_records_for_stop(
    state: dict[str, Any], *, root: Path = ROOT,
) -> list[tuple[dict[str, Any], Path]]:
    """Tolerant record load for STOP (C4-03, C5-03).

    STOP historically ignores unavailable, malformed, or non-object review
    records (they can close nothing), so this loader skips them instead of
    failing; well-formed records still participate in the all-source surface
    activity predicate so persisted surface records cannot be closed by STOP
    even when child_dispatches were relabeled or deleted.  C5-03: every path
    is handled independently — one unavailable, malformed, or non-object
    locator must not discard the other records (an empty load could hide
    persisted surface activity from the STOP predicate), so each locator is
    resolved and parsed on its own and every valid record is retained."""
    loaded: list[tuple[dict[str, Any], Path]] = []
    for field in ("review_records", "senior_review_records"):
        locators = state.get(field, [])
        if isinstance(locators, dict):  # Reader-only legacy mapping.
            locators = list(locators.values())
        if not isinstance(locators, list):
            continue
        for index, locator in enumerate(locators):
            try:
                path = _ordinary_workspace_file(
                    locator, f"{field}[{index}]", root=root
                )
                record = _read_json(
                    path, f"review record {path.relative_to(root)}"
                )
            except (ContractError, InputError, OSError, TypeError, ValueError):
                continue
            if isinstance(record, dict):
                loaded.append((record, path))
    return loaded


def _surface_activity_present(
    state: dict[str, Any], loaded: list[tuple[dict[str, Any], Path]],
) -> bool:
    """Detect surface activity from persisted facts, never from the STATE
    contract list alone: any surface-purpose child dispatch, any surface
    completion record, or any surface terminal binding activates the
    fail-closed surface checks even when the contract was removed from
    ``review_contracts`` or the schema_version was downgraded (C3-01)."""
    markers = (
        "surface_zero_path", "surface_carry_over_path",
        "surface_screen_input_path", "surface_evidence_binding",
    )
    if any(state.get(marker) is not None for marker in markers):
        return True
    children = state.get("child_dispatches")
    if isinstance(children, list) and any(
        isinstance(item, dict)
        and item.get("purpose") == "translation_surface_screen_v1"
        for item in children
    ):
        return True
    return any(
        record.get("purpose") == "translation_surface_screen_v1"
        or record.get("review_contract") == "translation_surface_screen_v1"
        for record, _ in loaded
    )


SURFACE_SAFE_ID = re.compile(r"^[0-9a-z][0-9a-z-]{0,31}$")
SURFACE_SAFE_TASK_ID = re.compile(r"^[0-9a-z][0-9a-z-]{0,127}$")
# Surface evidence reconciliation is independent of the code/contextual
# sidecar terminals: DONE rederives an immutable binding over the exact
# terminal artifact bytes (zero artifact, or the stage envelopes and raw
# outputs) and fails closed on any drift.
SURFACE_EVIDENCE_BINDING_ALGORITHM = "surface-evidence-binding/1"
SURFACE_EVIDENCE_BINDING_KEYS = frozenset({
    "algorithm", "task_id", "terminal", "artifact_sha256",
})


def _surface_safe(value: object, label: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise ContractError(f"{label} is not dispatch-safe")
    return value


def _surface_envelope_path(task_id: str, dispatch_id: str) -> str:
    return f".ai/task/{task_id}/SURFACE-SCREEN-ENVELOPE-{dispatch_id}.json"


def _surface_stage_info(
    state: dict[str, Any],
    surface: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *,
    root: Path = ROOT,
) -> tuple[bool, str]:
    """Build the ordered whole-screen stage list from dispatch-bound records."""
    global _SURFACE_LAST_STAGE_PAYLOAD
    _SURFACE_LAST_STAGE_PAYLOAD = None
    enriched: list[
        tuple[dict[str, Any], dict[str, Any], Path, tuple[int, int, int], list[str], list[str], dict[str, Any]]
    ] = []
    task_id = state.get("task_id")
    for record, dispatch, path in surface:
        relative = path.relative_to(root)
        phase, kind = record.get("review_phase"), record.get("review_kind")
        record_cycle, attempt = record.get("cycle"), record.get("attempt")
        if phase not in {"REVIEW"} or kind not in {"full", "lane"}:
            return False, f"{relative} has an invalid surface phase/review_kind"
        if type(record_cycle) is not int or record_cycle < 0 or type(attempt) is not int or attempt < 1:
            return False, f"{relative} cycle/attempt have invalid values"
        # Records themselves carry the identity binding fields and must agree
        # with STATE and their dispatch exactly (P2-DIRECT-LINEAGE surface form).
        if (
            record.get("workspace_id") != state.get("workspace_id")
            or record.get("parent_agent_id") != state.get("orchestrator_agent_id")
            or record.get("lineage_verified") is not True
            or dispatch.get("workspace_id") != state.get("workspace_id")
            or dispatch.get("parent_agent_id") != state.get("orchestrator_agent_id")
            or dispatch.get("lineage_verified") is not True
        ):
            return False, f"{relative} record/dispatch lineage does not equal STATE"
        record_dispatch_id = record.get("dispatch_id")
        try:
            _surface_safe(task_id, "task_id", SURFACE_SAFE_TASK_ID)
            _surface_safe(record_dispatch_id, "surface dispatch_id", SURFACE_SAFE_ID)
        except ContractError as error:
            return False, f"{relative} {error}"
        expected_input = _surface_envelope_path(task_id, record_dispatch_id)
        if record.get("input_path") != expected_input:
            return False, f"{relative} input_path does not equal the task/dispatch-derived envelope path"
        if not _has_successful_completion(record):
            return False, f"{relative} surface terminal record must be a successful completion"
        member = 0
        if kind == "lane":
            lane = record.get("lane")
            if not isinstance(lane, dict) or set(lane) != {
                "group_id", "group_identity", "group_manifest_path", "index",
                "count", "offset", "length",
            }:
                return False, f"{relative} lane has an invalid exact shape"
            member = lane.get("index")
            if type(member) is not int:
                return False, f"{relative} lane index must be an integer"
        elif "lane" in record:
            return False, f"{relative} non-lane record must not contain lane"
        payload = _surface_payload(record, root=root)
        entries = payload.get("entries")
        if not isinstance(entries, list) or not entries:
            return False, f"{relative} surface payload must contain frozen entries"
        enriched.append(
            (record, dispatch, path, (record_cycle, attempt, member),
             _surface_entry_keys(entries), [entry.get("source") for entry in entries],
             payload)
        )

    coordinates = [item[3] for item in enriched]
    if len(coordinates) != len(set(coordinates)):
        return False, "surface terminal three-dimensional coordinates must be unique"
    stages: dict[tuple[int, int], list[tuple[dict[str, Any], dict[str, Any], Path, tuple[int, int, int], list[str], list[str], dict[str, Any]]]] = {}
    for item in enriched:
        stages.setdefault(item[3][:2], []).append(item)
    used_group_ids: set[str] = set()
    used_group_identities: set[str] = set()
    used_group_manifest_paths: set[str] = set()
    stage_info: list[tuple[tuple[int, int], str, str, list[str], list[str], str]] = []
    stage_payloads: dict[tuple[int, int], dict[str, Any]] = {}
    for stage_key in sorted(stages):
        members = sorted(stages[stage_key], key=lambda item: item[3][2])
        kinds = {item[0]["review_kind"] for item in members}
        phases = {item[0]["review_phase"] for item in members}
        if len(kinds) != 1 or len(phases) != 1:
            return False, "surface stage must not mix review kinds or phases"
        kind, phase = next(iter(kinds)), next(iter(phases))
        if kind != "lane":
            if len(members) != 1 or members[0][3][2] != 0:
                return False, "full surface stage must contain one member ordinal 0"
            if not 1 <= len(members[0][4]) <= 3:
                return False, "full surface stage must cover between 1 and 3 entries"
            record = members[0][0]
            stage_info.append(
                (stage_key, "full", str(record.get("candidate_identity")), members[0][4], members[0][5], phase)
            )
            # C4-01: keep the complete canonical envelope payload for the
            # terminal draft comparison.
            stage_payloads[stage_key] = members[0][6]
            continue
        if len(members) != 4 or [item[3][2] for item in members] != [1, 2, 3, 4]:
            return False, "surface lane stage must contain exactly members 1..4"
        agents = [item[0].get("agent_id") for item in members]
        dispatch_ids = [item[0].get("dispatch_id") for item in members]
        if len(set(agents)) != 4 or len(set(dispatch_ids)) != 4:
            return False, "surface lane stage requires four distinct agents and dispatches"
        first_lane = members[0][0]["lane"]
        group_tuple = (first_lane["group_id"], first_lane["group_identity"], first_lane["group_manifest_path"])
        for value, used, label in (
            (group_tuple[0], used_group_ids, "group_id"),
            (group_tuple[1], used_group_identities, "group_identity"),
            (group_tuple[2], used_group_manifest_paths, "group_manifest_path"),
        ):
            if value in used:
                return False, f"surface lane {label} must not be reused across stages"
            used.add(value)
        manifest_path = _ordinary_workspace_file(
            first_lane["group_manifest_path"], "group_manifest_path", root=root
        )
        manifest_bytes = manifest_path.read_bytes()
        try:
            manifest = surface_screen_result_check.strict_json_bytes(
                manifest_bytes, label="surface lane manifest"
            )
            if manifest_bytes != surface_screen_result_check.canonical_bytes(manifest):
                raise surface_screen_result_check.ContractError(
                    "surface lane manifest bytes are not canonical compact JSON"
                )
            surface_screen_manifest.validate_group_manifest(
                manifest, root=root, manifest_path=first_lane["group_manifest_path"]
            )
        except surface_screen_result_check.InputError as error:
            raise InputError(str(error)) from error
        except surface_screen_result_check.ContractError as error:
            return False, f"surface lane manifest is invalid: {error}"
        manifest_payload = manifest["payload"]
        if (
            manifest.get("group_identity") != first_lane["group_identity"]
            or manifest_payload.get("task_id") != state.get("task_id")
            or manifest_payload.get("group_id") != first_lane["group_id"]
            or manifest_payload.get("review_phase") != phase
            or (manifest_payload.get("cycle"), manifest_payload.get("attempt")) != stage_key
        ):
            return False, "surface lane manifest does not bind its stage"
        boundaries = manifest_payload["lane_boundaries"]
        manifest_lanes = manifest_payload["lanes"]
        for index, (item, boundary, manifest_lane) in enumerate(zip(members, boundaries, manifest_lanes), 1):
            record, dispatch = item[0], item[1]
            lane = record["lane"]
            if (
                (lane["group_id"], lane["group_identity"], lane["group_manifest_path"]) != group_tuple
                or lane["count"] != 4
                or (lane["index"], lane["offset"], lane["length"])
                != (boundary["index"], boundary["offset"], boundary["length"])
                or record.get("dispatch_id") != manifest_lane["dispatch_id"]
                or record.get("input_path") != manifest_lane["input_path"]
                or record.get("candidate_identity") != manifest_lane["candidate_identity"]
                or dispatch.get("lane_group_identity") != lane["group_identity"]
                or dispatch.get("lane_index") != index
            ):
                return False, f"surface lane {index} record/dispatch/manifest binding mismatch"
            labels = dispatch.get("labels")
            if (
                not isinstance(labels, dict)
                or labels.get("lane_group_identity") != lane["group_identity"]
                or not _creation_lane_label_matches(labels.get("lane_index"), index)
            ):
                return False, f"surface lane {index} creation labels do not bind group/index"
        workset = manifest_payload["workset"]
        stage_info.append(
            (stage_key, "lane_group", manifest["group_identity"],
             _surface_entry_keys(workset["entries"]),
             [entry.get("source") for entry in workset["entries"]], phase)
        )
        # C4-01: keep the lane group manifest's whole workset for the
        # terminal draft comparison.
        stage_payloads[stage_key] = workset
    stage_info.sort(key=lambda item: item[0])
    if stage_info:
        _SURFACE_LAST_STAGE_PAYLOAD = stage_payloads[stage_info[-1][0]]
    return True, "ok" if not stage_info else _surface_stage_info_packed(stage_info)


def _surface_stage_info_packed(
    stage_info: list[tuple[tuple[int, int], str, str, list[str], list[str], str]],
) -> str:
    # Publish the ordered stage list through the module-global side channel;
    # the tuple-returning contract of _surface_stage_info stays (bool, str).
    global _SURFACE_LAST_STAGE_INFO
    _SURFACE_LAST_STAGE_INFO = stage_info
    return "ok"


_SURFACE_LAST_STAGE_INFO: list[tuple[tuple[int, int], str, str, list[str], list[str], str]] | None = None
# C4-01 side channel: the complete canonical payload semantics of the last
# validated surface stage — the full envelope payload, or the lane group
# manifest's whole workset — so the terminal predicate can compare the bound
# frozen input draft against everything the screen was actually built from,
# not only entry identity keys.
_SURFACE_LAST_STAGE_PAYLOAD: dict[str, Any] | None = None


def _surface_input_draft(
    state: dict[str, Any], *, root: Path,
) -> tuple[dict[str, Any] | None, str]:
    """Reread and strictly validate the unified actual frozen input draft
    bound by ``surface_screen_input_path`` (C3-02).

    Every surface terminal — zero, full, and lane — must bind exactly one
    immutable canonical draft path and bytes/hash; this helper rederives the
    validated draft (entries in canonical identity order) so the terminal
    predicate can compare real coverage against the real input instead of a
    recomputable constant."""
    locator = state.get("surface_screen_input_path")
    if not isinstance(locator, str) or not locator:
        return None, (
            "every surface terminal must bind surface_screen_input_path to "
            "its actual frozen input draft"
        )
    try:
        draft_file = _ordinary_workspace_file(
            locator, "surface_screen_input_path", root=root
        )
    except (ContractError, InputError) as error:
        return None, f"surface_screen_input_path: {error}"
    draft_bytes = draft_file.read_bytes()
    try:
        draft = surface_screen_manifest.load_draft_bytes(draft_bytes)
        if draft_bytes != surface_screen_result_check.canonical_bytes(draft):
            raise surface_screen_result_check.ContractError(
                "frozen input draft bytes are not canonical compact JSON"
            )
    except surface_screen_result_check.ContractError as error:
        return None, f"surface input draft is invalid: {error}"
    except surface_screen_result_check.InputError as error:
        raise InputError(str(error)) from error
    return draft, ""


def _surface_evidence_binding_valid(
    state: dict[str, Any],
    surface_records: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *,
    terminal: str,
    task_id: str,
    root: Path = ROOT,
) -> tuple[bool, str]:
    """Verify the immutable surface-specific evidence reconciliation binding.

    The binding is an exact map from terminal artifact locators to their
    SHA-256; DONE rederives it from the current bytes so any drift — and any
    omission or extra artifact — fails closed.  It never borrows the
    code/contextual sidecar reconciliation terminals.
    """
    binding = state.get("surface_evidence_binding")
    if not isinstance(binding, dict) or frozenset(binding) != SURFACE_EVIDENCE_BINDING_KEYS:
        return False, "surface tasks must bind an exact surface_evidence_binding object"
    if binding["algorithm"] != SURFACE_EVIDENCE_BINDING_ALGORITHM:
        return False, "surface_evidence_binding algorithm is not supported"
    if binding["task_id"] != task_id:
        return False, "surface_evidence_binding task_id does not match STATE"
    if binding["terminal"] != terminal:
        return False, "surface_evidence_binding terminal does not match the surface outcome"
    locators: list[str] = []
    # C3-02: every terminal also binds its actual frozen input draft by real
    # bytes; a constant empty identity is never accepted as evidence.
    draft_locator = state.get("surface_screen_input_path")
    if not isinstance(draft_locator, str) or not draft_locator:
        return False, (
            "surface_evidence_binding requires the unified "
            "surface_screen_input_path binding the actual frozen input draft"
        )
    locators.append(draft_locator)
    if terminal == "zero":
        zero_locator = state.get("surface_zero_path")
        if not isinstance(zero_locator, str):
            return False, "surface_evidence_binding requires a bound surface_zero_path"
        locators.append(zero_locator)
    else:
        for record, _, _ in surface_records:
            for key in ("input_path", "raw_output_path"):
                locator = record.get(key)
                if not isinstance(locator, str) or not locator:
                    return False, f"surface_evidence_binding requires a record {key}"
                locators.append(locator)
        carry_locator = state.get("surface_carry_over_path")
        if carry_locator is not None:
            if not isinstance(carry_locator, str):
                return False, "surface_carry_over_path must be a workspace-relative string"
            locators.append(carry_locator)
    recomputed: dict[str, str] = {}
    for locator in locators:
        try:
            artifact = _ordinary_workspace_file(
                locator, "surface evidence artifact", root=root
            )
        except (ContractError, InputError) as error:
            return False, f"surface evidence artifact: {error}"
        recomputed[locator] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if binding["artifact_sha256"] != recomputed:
        return False, "surface_evidence_binding does not match the current terminal artifact bytes"
    return True, "ok"


def _surface_orphan_group_manifest(
    state: dict[str, Any], group_identity: object, *, root: Path,
) -> tuple[dict[str, Any], str] | None:
    """Locate a failed lane attempt's group manifest by its immutable
    group_identity (C4-02).

    Orphan failed surface children publish no completion record, so the
    group manifest — always written before dispatch — is the only persisted
    source of their group id/path and attempt.  Malformed candidate manifests
    fail closed; a missing manifest means the attempt's group artifacts were
    destroyed or its manifest path was reused, both of which fail closed."""
    if not isinstance(group_identity, str) or not SHA256.fullmatch(group_identity):
        return None
    task_id = state.get("task_id")
    if not isinstance(task_id, str) or not SURFACE_SAFE_TASK_ID.fullmatch(task_id):
        return None
    directory = root / ".ai" / "task" / task_id
    if not directory.is_dir():
        return None
    for candidate in sorted(directory.glob("SURFACE-SCREEN-GROUP-*.json")):
        relative = candidate.relative_to(root).as_posix()
        raw = _ordinary_workspace_file(
            relative, "orphan surface group manifest", root=root
        ).read_bytes()
        try:
            manifest = surface_screen_result_check.strict_json_bytes(
                raw, label="surface group manifest"
            )
            if raw != surface_screen_result_check.canonical_bytes(manifest):
                raise surface_screen_result_check.ContractError(
                    "surface group manifest bytes are not canonical compact JSON"
                )
            surface_screen_manifest.validate_group_manifest(
                manifest, root=root, manifest_path=relative
            )
        except surface_screen_result_check.InputError as error:
            raise InputError(str(error)) from error
        except surface_screen_result_check.ContractError as error:
            raise ContractError(
                f"surface group manifest {relative} is invalid: {error}"
            ) from error
        if manifest.get("group_identity") == group_identity:
            return manifest, relative
    return None


def _surface_retry_history_valid(
    state: dict[str, Any],
    surface: list[tuple[dict[str, Any], dict[str, Any], Path]],
    successful: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *,
    root: Path = ROOT,
) -> tuple[bool, str]:
    """Validate the complete surface retry history (C3-05, C4-02, C5-01, C5-02).

    Failed attempts — including orphan failed surface children that were
    dispatched but never published a completion record — followed by a
    successful stage must have monotonically increasing attempts, and every
    failed child identity — dispatch_id, agent_id, and lane
    group_id/group_identity/group manifest path — must stay fresh: no failed
    identity may be reused by the successful stage or by a later failed
    attempt (C5-01: the four members of one failed lane stage share one
    group tuple, but any of the three group identifiers reused between two
    distinct failed stages, or between a failed and the successful stage,
    fails closed).  SR-01: orphan and record-bound members of one failed
    stage claim their shared group tuple in one per-stage map keyed by
    (cycle, attempt), so a partially orphaned failed stage stays legal.
    Orphan lane children recover their group/attempt state
    from the group manifest bound by their persisted lane_group_identity;
    orphan full children carry no persisted attempt and are enforced for
    identity freshness only.  C5-02: orphan reconstruction also recognizes
    the persisted surface signals already on the dispatch — its
    lane_group_identity, or the canonical task/dispatch-derived
    SURFACE-SCREEN envelope input path — even when purpose was deleted or
    relabeled; this inference stays strictly bounded to surface retry
    reconstruction and never becomes a generalized purpose heuristic."""
    failed = [item for item in surface if not _has_successful_completion(item[0])]
    # C4-02, C5-02: reconstruct orphan failed children from child_dispatches
    # — any surface child without a bound surface completion record is a
    # failed attempt and joins the retry history.  Besides the surface
    # purpose, only signals already persisted on the dispatch itself qualify:
    # the lane_group_identity of a failed lane attempt, or the canonical
    # task-derived SURFACE-SCREEN envelope input path, so purpose deletion or
    # relabeling cannot hide a dispatched surface child from this history.
    children = state.get("child_dispatches")
    bound_ids = {item[0].get("dispatch_id") for item in surface}
    task_id = state.get("task_id")

    def is_surface_orphan(dispatch: dict[str, Any]) -> bool:
        if dispatch.get("purpose") == "translation_surface_screen_v1":
            return True
        group_identity = dispatch.get("lane_group_identity")
        if isinstance(group_identity, str) and group_identity:
            return True
        dispatch_id, input_path = dispatch.get("dispatch_id"), dispatch.get("input_path")
        return (
            isinstance(task_id, str)
            and SURFACE_SAFE_TASK_ID.fullmatch(task_id) is not None
            and isinstance(dispatch_id, str) and bool(dispatch_id)
            and isinstance(input_path, str)
            and input_path == _surface_envelope_path(task_id, dispatch_id)
        )

    orphans = [
        dispatch for dispatch in (children if isinstance(children, list) else [])
        if isinstance(dispatch, dict)
        and is_surface_orphan(dispatch)
        and dispatch.get("dispatch_id") not in bound_ids
    ]
    if not failed and not orphans:
        return True, "ok"
    if not successful:
        return False, (
            "surface retry history records failed attempts without a successful "
            "terminal stage"
        )

    def stage_key(item: tuple[dict[str, Any], dict[str, Any], Path]) -> tuple[int, int]:
        record = item[0]
        return (record["cycle"], record["attempt"])

    def group_markers(record: dict[str, Any]) -> set[str]:
        lane = record.get("lane")
        if not isinstance(lane, dict):
            return set()
        return {
            f"{key}={lane[key]}"
            for key in ("group_id", "group_identity", "group_manifest_path")
            if lane.get(key) is not None
        }

    used_dispatches: set[str] = set()
    used_agents: set[str] = set()
    used_groups: set[str] = set()
    orphan_attempts: set[tuple[int, int]] = set()
    # C5-01/SR-01: one shared per-stage claim map keyed by (cycle, attempt)
    # for both reconstructed orphan members and record-bound failed members;
    # members of one failed stage share one group tuple across the
    # orphan/record boundary, while distinct failed stages never do.
    failed_stage_groups: dict[tuple[int, int], set[str]] = {}
    for dispatch in orphans:
        dispatch_id = dispatch.get("dispatch_id")
        agent_id = dispatch.get("agent_id")
        if not isinstance(dispatch_id, str) or not dispatch_id or \
                not isinstance(agent_id, str) or not agent_id:
            return False, (
                "orphan failed surface children must carry dispatch/agent identities"
            )
        if dispatch_id in used_dispatches or agent_id in used_agents:
            return False, "orphan failed surface children must use fresh dispatch/agent identities"
        used_dispatches.add(dispatch_id)
        used_agents.add(agent_id)
        group_identity = dispatch.get("lane_group_identity")
        if group_identity is None:
            continue
        located = _surface_orphan_group_manifest(state, group_identity, root=root)
        if located is None:
            return False, (
                "an orphan failed surface lane child's group manifest cannot be "
                "located by its bound lane_group_identity; destroyed or reused "
                "group artifacts fail closed"
            )
        manifest, manifest_path = located
        payload = manifest["payload"]
        attempt_key = (payload["cycle"], payload["attempt"])
        orphan_attempts.add(attempt_key)
        markers = {
            f"group_id={payload['group_id']}",
            f"group_identity={group_identity}",
            f"group_manifest_path={manifest_path}",
        }
        claimed = failed_stage_groups.setdefault(attempt_key, set())
        overlap = markers & (used_groups - claimed)
        if overlap:
            return False, (
                "an orphan failed surface stage must not reuse an earlier failed "
                f"attempt's lane group identity/path: {sorted(overlap)[0]}"
            )
        claimed |= markers
        used_groups |= markers

    attempts = {stage_key(item) for item in surface} | orphan_attempts
    previous_attempt: int | None = None
    for _, attempt in sorted(attempts):
        if previous_attempt is not None and attempt <= previous_attempt:
            return False, "surface retry attempts must increase monotonically across attempts"
        previous_attempt = attempt
    failed_keys = {stage_key(item) for item in failed} | orphan_attempts
    if failed_keys and max(failed_keys) >= min(stage_key(item) for item in successful):
        return False, "every failed surface attempt must precede the successful stage"

    for record, _, _ in failed:
        if record["dispatch_id"] in used_dispatches or record["agent_id"] in used_agents:
            return False, "failed surface retry attempts must use fresh dispatch/agent identities"
        used_dispatches.add(record["dispatch_id"])  # type: ignore[arg-type]
        used_agents.add(record["agent_id"])  # type: ignore[arg-type]
        markers = group_markers(record)
        claimed = failed_stage_groups.setdefault(
            (record["cycle"], record["attempt"]), set()
        )
        # C5-01: the four members of one failed lane stage may share one
        # group tuple, but group_id, group_identity, and group_manifest_path
        # must never be reused between two distinct failed stages (reuse
        # against the successful stage is enforced below).
        overlap = markers & (used_groups - claimed)
        if overlap:
            return False, (
                "a failed surface stage must not reuse an earlier failed "
                f"attempt's lane group identity/path: {sorted(overlap)[0]}"
            )
        claimed |= markers
        used_groups |= markers
    for record, _, _ in successful:
        if record["dispatch_id"] in used_dispatches or record["agent_id"] in used_agents:
            return False, (
                "the successful surface stage must not reuse a failed attempt's "
                "dispatch/agent identity"
            )
        overlap = group_markers(record) & used_groups
        if overlap:
            return False, (
                "the successful surface stage must not reuse a failed attempt's "
                f"lane group identity/path: {sorted(overlap)[0]}"
            )
    return True, "ok"


def _translation_surface_convergence_valid(
    state: dict[str, Any], loaded: list[tuple[dict[str, Any], Path]],
    bound_records: list[tuple[dict[str, Any], dict[str, Any], Path]], *, root: Path = ROOT,
) -> tuple[bool, str]:
    """Validate translation_surface_screen_v1 terminals honestly.

    Surface is review_only with its own independent whole-screen terminal: it
    never borrows the implement RE_REVIEW/FINAL_REVIEW convergence of the
    contextual contracts.  The terminal predicate records surface completion
    only: the complete frozen screen set ran under this contract with an
    OK|ISSUE result and evidence binding per entry; it never claims deep
    review or repair completion.
    """
    global _SURFACE_LAST_STAGE_INFO
    global _SURFACE_LAST_STAGE_PAYLOAD
    _SURFACE_LAST_STAGE_INFO = None
    _SURFACE_LAST_STAGE_PAYLOAD = None
    if not _surface_enabled(state):
        # C3-01: surface checks activate from any persisted surface activity,
        # not only from review_contracts — removing the contract or
        # downgrading the schema can never silently bypass them.
        if _surface_activity_present(state, loaded):
            return False, (
                "translation_surface_screen_v1 activity exists (surface dispatch, "
                "completion record, or terminal binding) but the contract was "
                "removed or the schema downgraded; DONE fails closed"
            )
        return True, "ok"
    mode = state.get("mode")
    if mode != "review_only":
        return False, "translation_surface_screen_v1 is review_only; implement repair is a separate task"
    if state.get("change_class") != "translation_workflow":
        return False, "surface review_only tasks must use change_class=translation_workflow"
    task_id = state.get("task_id")
    if not isinstance(task_id, str) or not SURFACE_SAFE_TASK_ID.fullmatch(task_id):
        return False, "surface task_id must be dispatch-safe for artifact paths"

    surface_loaded = [
        (record, path) for record, path in loaded
        if record.get("review_contract") == "translation_surface_screen_v1"
        and record.get("purpose") == "translation_surface_screen_v1"
        and _has_completion_indicator(record)
    ]
    surface = [
        item for item in bound_records
        if item[0].get("review_contract") == "translation_surface_screen_v1"
        and item[0].get("purpose") == "translation_surface_screen_v1"
    ]

    # Identity-bound zero/no-dispatch artifact: proves n=0 without any surface
    # dispatch.  When present, no dispatch-bound surface record may exist.
    zero_locator = state.get("surface_zero_path")
    if zero_locator is not None:
        if surface_loaded or surface:
            return False, "a zero/no-dispatch surface terminal must not carry dispatch-bound surface records"
        children = state.get("child_dispatches")
        if isinstance(children, list) and any(
            isinstance(item, dict)
            and item.get("purpose") == "translation_surface_screen_v1"
            for item in children
        ):
            return False, "a zero/no-dispatch surface terminal must not coexist with surface dispatches"
        if not isinstance(zero_locator, str):
            return False, "surface_zero_path must be a workspace-relative string"
        try:
            zero_file = _ordinary_workspace_file(zero_locator, "surface_zero_path", root=root)
        except (ContractError, InputError) as error:
            return False, f"surface_zero_path: {error}"
        expected_zero = surface_screen_manifest.zero_artifact_path(task_id)
        if zero_locator != expected_zero:
            return False, "surface_zero_path must equal the task-derived zero artifact path"
        zero_bytes = zero_file.read_bytes()
        try:
            zero_value = surface_screen_result_check.strict_json_bytes(
                zero_bytes, label="surface zero artifact"
            )
            if zero_bytes != surface_screen_result_check.canonical_bytes(zero_value):
                raise surface_screen_result_check.ContractError(
                    "zero artifact bytes are not canonical compact JSON"
                )
            surface_screen_manifest.validate_zero_payload(zero_value)
            # Rederive the canonical empty workset/input snapshot identity.
            if zero_value.get("workset_identity") != surface_screen_manifest.build_zero_workset_identity():
                return False, "surface zero artifact does not bind the canonical empty workset identity"
        except surface_screen_result_check.ContractError as error:
            return False, f"surface zero artifact is invalid: {error}"
        if state.get("surface_carry_over_path") is not None:
            return False, "a zero/no-dispatch surface terminal must not bind a carry-over artifact"
        # C3-02: reread the actual frozen input draft.  A zero terminal must
        # bind a really empty draft by real bytes, never a constant empty
        # identity.
        draft, draft_detail = _surface_input_draft(state, root=root)
        if draft is None:
            return False, draft_detail
        if draft["entries"]:
            return False, (
                "a zero/no-dispatch surface terminal must bind an actually "
                "empty frozen input draft"
            )
        binding = _surface_evidence_binding_valid(
            state, surface, terminal="zero", task_id=task_id, root=root,
        )
        if not binding[0]:
            return False, binding[1]
        return True, "ok"

    if not surface_loaded or len(surface_loaded) != len(surface):
        return False, "every surface terminal record must be dispatch-bound"

    # C3-05: validate the complete retry history before the terminal stage.
    successful = [item for item in surface if _has_successful_completion(item[0])]
    retry_ok = _surface_retry_history_valid(state, surface, successful, root=root)
    if not retry_ok[0]:
        return False, retry_ok[1]
    stages_ok = _surface_stage_info(state, successful, root=root)
    if not stages_ok[0]:
        return False, stages_ok[1]
    stage_info = _SURFACE_LAST_STAGE_INFO or []
    if len(stage_info) != 1:
        return False, "review-only surface permits exactly one whole-screen stage"
    origin = stage_info[0]
    if origin[0][0] != 0 or origin[5] != "REVIEW" or origin[1] not in {"full", "lane_group"}:
        return False, "the surface stage must be a cycle-0 REVIEW full or lane_group covering the whole screen set"

    # C3-02: reread the unified actual frozen input draft for every
    # whole-screen terminal.  Coverage is compared against the real draft:
    # exact equality for n<=80, and first-80 plus a mandatory validated
    # carry-over artifact for n>80, so deleting the carry binding can never
    # reclassify an n=85 workset as a whole n=80 screen.
    draft, draft_detail = _surface_input_draft(state, root=root)
    if draft is None:
        return False, draft_detail
    draft_keys = _surface_entry_keys(draft["entries"])
    carry_locator = state.get("surface_carry_over_path")
    if len(draft_keys) > surface_screen_manifest.SCREEN_LIMIT:
        if carry_locator is None:
            return False, (
                "the frozen input draft exceeds the 80-entry screen limit; a bound "
                "validated carry-over artifact is mandatory, and deleting the carry "
                "binding can never reclassify it as a whole screen"
            )
        if not isinstance(carry_locator, str):
            return False, "surface_carry_over_path must be a workspace-relative string"
        try:
            carry_file = _ordinary_workspace_file(carry_locator, "surface_carry_over_path", root=root)
        except (ContractError, InputError) as error:
            return False, f"surface_carry_over_path: {error}"
        expected_carry = surface_screen_manifest.carry_over_artifact_path(task_id)
        if carry_locator != expected_carry:
            return False, "surface_carry_over_path must equal the task-derived carry-over artifact path"
        carry_bytes = carry_file.read_bytes()
        try:
            carry_value = surface_screen_result_check.strict_json_bytes(
                carry_bytes, label="surface carry-over artifact"
            )
            if carry_bytes != surface_screen_result_check.canonical_bytes(carry_value):
                raise surface_screen_result_check.ContractError(
                    "carry-over artifact bytes are not canonical compact JSON"
                )
            # Strict carry-over validation: algorithm version, counts,
            # disjointness and path binding are rechecked here; the complete
            # original ordered frozen identity set is bound below.
            surface_screen_manifest.validate_carry_over_payload(carry_value)
        except surface_screen_result_check.ContractError as error:
            return False, f"surface carry-over artifact is invalid: {error}"
        if carry_value.get("task_id") != task_id:
            return False, "carry-over artifact task_id does not bind STATE.task_id"
        # Omissions/extras: the ordered concatenation of the screen and
        # carry-over identity arrays must equal the complete validated frozen
        # input draft exactly.
        try:
            surface_screen_manifest.validate_carry_over_payload(
                carry_value, entries=draft["entries"]
            )
        except surface_screen_result_check.ContractError as error:
            return False, f"carry-over artifact does not bind the original frozen workset: {error}"
        if origin[3] != carry_value.get("ordered_screen_entry_revision_identities"):
            return False, "the screen stage does not cover exactly the recorded first-80 screen set"
    else:
        if carry_locator is not None:
            return False, (
                "a carry-over artifact is bound but the frozen input draft does "
                "not exceed the screen limit"
            )
        if origin[3] != draft_keys:
            return False, "the screen stage does not cover exactly the frozen input draft workset"
    # C4-01: the terminal must bind complete canonical payload semantics, not
    # only entry identity keys: a full stage's envelope payload equals the
    # whole frozen draft; a lane stage's manifest whole workset equals the
    # exact draft (or first-80) projection including all shared scalars and
    # the unbound rendered_briefing.
    if origin[1] == "full":
        if _SURFACE_LAST_STAGE_PAYLOAD != draft:
            return False, (
                "the full surface envelope payload does not equal the frozen "
                "input draft (all shared scalars, briefing, and entries)"
            )
    else:
        workset = _SURFACE_LAST_STAGE_PAYLOAD
        screen_entries = (
            draft["entries"][:surface_screen_manifest.SCREEN_LIMIT]
            if len(draft_keys) > surface_screen_manifest.SCREEN_LIMIT
            else draft["entries"]
        )
        if (
            not isinstance(workset, dict)
            or workset.get("entries") != screen_entries
            or any(
                workset.get(key) != draft[key]
                for key in ("fixed_source_identity", "terminology_snapshot",
                            "rules_version", "rendered_briefing")
            )
        ):
            return False, (
                "the lane group whole workset does not equal the frozen input "
                "draft projection (all shared scalars, briefing, and entries)"
            )
    binding = _surface_evidence_binding_valid(
        state, surface, terminal="whole_screen", task_id=task_id, root=root,
    )
    if not binding[0]:
        return False, binding[1]
    return True, "ok"


def _candidate_bindings_valid(
    state: dict[str, Any], records: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *, root: Path = ROOT,
) -> tuple[bool, str]:
    required = (
        "task_id", "review_contract", "review_phase", "cycle", "attempt",
        "reviewer_role", "purpose", "agent_id", "dispatch_id",
    )
    for record, dispatch, path in records:
        relative = path.relative_to(root)
        if any(record.get(key) in (None, "") for key in required):
            return False, f"{relative} is missing a required completion field"
        if record.get("task_id") != state.get("task_id"):
            return False, f"{relative} task_id does not match STATE"
        if not _has_completion_indicator(record):
            return False, f"{relative} has no valid terminal status/result"
        review_phase = record.get("review_phase")
        record_cycle = record.get("cycle")
        record_attempt = record.get("attempt")
        if (
            not isinstance(review_phase, str)
            or type(record_cycle) is not int
            or type(record_attempt) is not int
        ):
            return False, f"{relative} phase/cycle/attempt have invalid types"
        if record.get("purpose") in {"translation_contextual_v1", "translation_contextual_v2"}:
            identity, input_path = record.get("candidate_identity"), record.get("input_path")
            if not isinstance(identity, str) or not SHA256.fullmatch(identity) or not isinstance(input_path, str):
                return False, f"{relative} lacks a valid contextual identity or input_path"
            if identity != dispatch.get("candidate_identity") or input_path != dispatch.get("input_path"):
                return False, f"{relative} contextual binding does not match its dispatch"
            envelope = _read_json(
                _ordinary_workspace_file(input_path, "contextual input_path", root=root),
                "contextual envelope",
            )
            if not isinstance(envelope, dict) or envelope.get("candidate_identity") != identity or "payload" not in envelope:
                return False, f"{relative} contextual envelope does not match candidate_identity"
            contract = record["purpose"]
            if hashlib.sha256(_canonical_contextual_payload_bytes(
                envelope["payload"], expected_contract=contract
            )).hexdigest() != identity:
                return False, f"{relative} contextual candidate_identity does not match payload"
            if contract == "translation_contextual_v2":
                dispatch_id = record["dispatch_id"]
                labels = dispatch.get("labels")
                if (
                    dispatch.get("lineage_verified") is not True
                    or not isinstance(state.get("orchestrator_agent_id"), str)
                    or not state["orchestrator_agent_id"]
                    or dispatch.get("parent_agent_id") != state["orchestrator_agent_id"]
                    or not isinstance(state.get("workspace_id"), str)
                    or not state["workspace_id"]
                    or dispatch.get("workspace_id") != state["workspace_id"]
                    or not isinstance(labels, dict)
                    or labels.get("task_id") != state.get("task_id")
                    or labels.get("role") != "reviewer"
                    or labels.get("purpose") != "translation_contextual_v2"
                    or labels.get("candidate_identity") != identity
                    or labels.get("dispatch_id") != dispatch_id
                ):
                    return False, f"{relative} v2 dispatch lacks exact workspace/direct-lineage labels"
                try:
                    contextual_lane_manifest.render_dispatch_prompt(identity, input_path)
                except contextual_result_check.ContractError as error:
                    return False, f"{relative} v2 dispatch prompt is invalid: {error}"
                expected_raw = f".ai/reviews/{state['task_id']}/raw-{dispatch_id}.txt"
                raw_path = record.get("raw_output_path")
                raw_hash = record.get("raw_output_sha256")
                if raw_path != expected_raw or not isinstance(raw_hash, str) or not SHA256.fullmatch(raw_hash):
                    return False, f"{relative} raw output path/hash does not bind task/dispatch"
                raw_file = _ordinary_workspace_file(raw_path, "raw_output_path", root=root)
                raw_bytes = raw_file.read_bytes()
                if hashlib.sha256(raw_bytes).hexdigest() != raw_hash:
                    return False, f"{relative} raw output hash drift"
                try:
                    envelope_bytes = _ordinary_workspace_file(
                        input_path, "contextual input_path", root=root
                    ).read_bytes()
                    contextual_result_check.validate_result_bytes(
                        envelope_bytes,
                        raw_bytes,
                    )
                except contextual_result_check.InputError as error:
                    raise InputError(str(error)) from error
                except contextual_result_check.ContractError as error:
                    return False, f"{relative} raw output is invalid: {error}"
            continue
        if record.get("purpose") == "translation_surface_screen_v1":
            identity, input_path = record.get("candidate_identity"), record.get("input_path")
            if not isinstance(identity, str) or not SHA256.fullmatch(identity) or not isinstance(input_path, str):
                return False, f"{relative} lacks a valid surface identity or input_path"
            if identity != dispatch.get("candidate_identity") or input_path != dispatch.get("input_path"):
                return False, f"{relative} surface binding does not match its dispatch"
            envelope_file = _ordinary_workspace_file(input_path, "surface input_path", root=root)
            envelope_bytes = envelope_file.read_bytes()
            envelope = _read_json(envelope_file, "surface envelope")
            if (
                not isinstance(envelope, dict)
                or frozenset(envelope) != {"candidate_identity", "payload"}
                or envelope.get("candidate_identity") != identity
            ):
                return False, f"{relative} surface envelope does not match candidate_identity"
            try:
                surface_screen_result_check.canonical_payload_bytes(envelope.get("payload"))
            except surface_screen_result_check.ContractError as error:
                return False, f"{relative} surface payload is invalid: {error}"
            if envelope_bytes != surface_screen_result_check.canonical_bytes(envelope):
                return False, f"{relative} surface envelope bytes are not canonical compact JSON"
            dispatch_id = record["dispatch_id"]
            labels = dispatch.get("labels")
            if (
                dispatch.get("lineage_verified") is not True
                or not isinstance(state.get("orchestrator_agent_id"), str)
                or not state["orchestrator_agent_id"]
                or dispatch.get("parent_agent_id") != state["orchestrator_agent_id"]
                or not isinstance(state.get("workspace_id"), str)
                or not state["workspace_id"]
                or dispatch.get("workspace_id") != state["workspace_id"]
                or not isinstance(labels, dict)
                or labels.get("task_id") != state.get("task_id")
                or labels.get("role") != "reviewer"
                or labels.get("purpose") != "translation_surface_screen_v1"
                or labels.get("candidate_identity") != identity
                or labels.get("dispatch_id") != dispatch_id
            ):
                return False, f"{relative} surface dispatch lacks exact workspace/direct-lineage labels"
            # The record itself persists the same workspace/direct-parent
            # lineage binding as STATE and its dispatch.
            if (
                record.get("workspace_id") != state.get("workspace_id")
                or record.get("parent_agent_id") != state.get("orchestrator_agent_id")
                or record.get("lineage_verified") is not True
            ):
                return False, f"{relative} surface record lacks STATE-equal workspace/parent/lineage fields"
            # Safe identifiers and the exact task/dispatch-derived envelope path.
            if (
                not isinstance(state.get("task_id"), str)
                or not SURFACE_SAFE_TASK_ID.fullmatch(state["task_id"])
                or not isinstance(dispatch_id, str)
                or not SURFACE_SAFE_ID.fullmatch(dispatch_id)
                or input_path != _surface_envelope_path(state["task_id"], dispatch_id)
            ):
                return False, f"{relative} surface identity/path is not exactly task/dispatch-derived"
            try:
                surface_screen_result_check.render_dispatch_prompt(identity, input_path)
            except surface_screen_result_check.ContractError as error:
                return False, f"{relative} surface dispatch prompt is invalid: {error}"
            expected_raw = f".ai/reviews/{state['task_id']}/raw-{dispatch_id}.txt"
            raw_path = record.get("raw_output_path")
            raw_hash = record.get("raw_output_sha256")
            if raw_path != expected_raw or not isinstance(raw_hash, str) or not SHA256.fullmatch(raw_hash):
                return False, f"{relative} surface raw output path/hash does not bind task/dispatch"
            raw_file = _ordinary_workspace_file(raw_path, "raw_output_path", root=root)
            raw_bytes = raw_file.read_bytes()
            if hashlib.sha256(raw_bytes).hexdigest() != raw_hash:
                return False, f"{relative} surface raw output hash drift"
            try:
                surface_screen_result_check.validate_result_bytes(envelope_bytes, raw_bytes)
            except surface_screen_result_check.InputError as error:
                raise InputError(str(error)) from error
            except surface_screen_result_check.ContractError as error:
                return False, f"{relative} surface raw output is invalid: {error}"
            continue
        locator = record.get("candidate_locator")
        if not isinstance(locator, dict) or set(locator) != {"spec_path", "diff_path"}:
            return False, f"{relative} candidate_locator must have exactly spec_path and diff_path"
        spec = _ordinary_workspace_file(
            locator["spec_path"], "candidate_locator.spec_path", root=root
        )
        diff = _ordinary_workspace_file(
            locator["diff_path"], "candidate_locator.diff_path", root=root
        )
        match = CODE_DIFF_NAME.fullmatch(diff.name)
        if not match:
            return False, f"{relative} diff_path has an invalid CODE_DIFF filename"
        phase, cycle, attempt = match.group(1), int(match.group(2)), int(match.group(3))
        if (phase, cycle, attempt) != (review_phase, record_cycle, record_attempt):
            return False, f"{relative} phase/cycle/attempt does not match diff filename"
        if candidate_ref(
            _read_candidate_bytes(spec, "candidate SPEC"),
            _read_candidate_bytes(diff, "candidate diff"),
        ) != record.get("candidate_ref"):
            return False, f"{relative} candidate_ref does not match SPEC/NUL/diff bytes"
    return True, "ok"


def _patch_lines(diff_bytes: bytes) -> list[bytes]:
    return diff_bytes.splitlines(keepends=True)


def _new_file_entry_bytes(diff_bytes: bytes, sidecar_relative: str) -> bytes | None:
    """Parse strict textual new-file blocks and reconstruct the requested file."""
    lines = _patch_lines(diff_bytes)
    starts = [index for index, line in enumerate(lines) if line.startswith(b"diff --git ")]
    if not starts:
        return None
    sidecar_token = sidecar_relative.encode("utf-8")
    sidecar_starts = [
        start for start in starts
        if any(
            token in {b"a/" + sidecar_token, b"b/" + sidecar_token}
            for token in lines[start].rstrip(b"\r\n").split()[2:]
        )
    ]
    if not sidecar_starts:
        return None
    if len(sidecar_starts) > 1:
        raise ContractError(f"candidate diff contains duplicate new-file entries for {sidecar_relative}")
    sidecar_index = sidecar_starts[0]
    sidecar_end = next(
        (start for start in starts if start > sidecar_index), len(lines)
    )
    header = lines[sidecar_index].rstrip(b"\r\n")
    match = re.fullmatch(rb"diff --git a/([^\s]+) b/([^\s]+)", header)
    if match is None or match.group(1) != match.group(2):
        raise ContractError("candidate diff has a non-canonical diff --git path pair")
    try:
        path = match.group(1).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractError("candidate diff path is not UTF-8") from error
    if path != sidecar_relative:
        raise ContractError(f"sidecar entry path does not match {sidecar_relative}")

    body = lines[sidecar_index + 1:sidecar_end]
    if any(line.endswith(b"\r\n") for line in body):
        raise ContractError(f"new-file entry {path} uses CRLF line endings")
    new_file_markers = [index for index, line in enumerate(body) if line.startswith(b"new file mode ")]
    if not new_file_markers:
        raise ContractError("sidecar path appears in diff without new file mode")
    if len(new_file_markers) != 1:
        raise ContractError(f"new-file entry {path} has duplicate new file mode headers")
    if not re.fullmatch(rb"new file mode [0-7]{6}", body[new_file_markers[0]].rstrip(b"\n")):
        raise ContractError(f"new-file entry {path} has an invalid new file mode")
    index_headers = [index for index, line in enumerate(body) if line.startswith(b"index ")]
    if len(index_headers) > 1:
        raise ContractError(f"new-file entry {path} has duplicate index headers")
    if index_headers and not re.fullmatch(
        rb"index [0-9a-f]{4,64}\.{2}[0-9a-f]{4,64}(?: [0-7]{6})?", body[index_headers[0]].rstrip(b"\n")
    ):
        raise ContractError(f"new-file entry {path} has an invalid index header")
    old_headers = [index for index, line in enumerate(body) if line.rstrip(b"\n") == b"--- /dev/null"]
    new_headers = [index for index, line in enumerate(body) if line.rstrip(b"\n") == (b"+++ b/" + path.encode("utf-8"))]
    if (
        len(old_headers) != 1
        or len(new_headers) != 1
        or new_file_markers[0] >= old_headers[0]
        or old_headers[0] >= new_headers[0]
        or (index_headers and not (new_file_markers[0] < index_headers[0] < old_headers[0]))
    ):
        raise ContractError(f"new-file entry {path} must have /dev/null and matching b/ headers")
    hunk_indices = [index for index, line in enumerate(body) if line.startswith(b"@@ ")]
    if len(hunk_indices) != 1:
        raise ContractError(f"new-file entry {path} must contain exactly one hunk")
    hunk_index = hunk_indices[0]
    hunk_header = body[hunk_index].rstrip(b"\n")
    hunk_match = re.fullmatch(rb"@@ -(\d+),(\d+) \+(\d+)(?:,(\d+))? @@(?:.*)", hunk_header)
    if hunk_match is None:
        raise ContractError(f"new-file entry {path} has an invalid hunk header")
    old_start, old_count, new_start, new_count = hunk_match.groups()
    old_start, old_count, new_start = int(old_start), int(old_count), int(new_start)
    new_count = int(new_count) if new_count is not None else 1
    if old_start != 0 or old_count != 0 or new_start not in {0, 1}:
        raise ContractError(f"new-file entry {path} has a non-empty old range")
    if any(index > hunk_index and line.startswith(b"@@ ") for index, line in enumerate(body)):
        raise ContractError(f"new-file entry {path} has more than one hunk")
    prefix = body[:hunk_index]
    allowed_prefix = {new_file_markers[0], *old_headers, *new_headers, *index_headers}
    for index, line in enumerate(prefix):
        stripped = line.rstrip(b"\n")
        if index in allowed_prefix:
            continue
        raise ContractError(f"new-file entry {path} has an unexpected header line")
    content = bytearray()
    added_count = 0
    previous_added = False
    previous_added_terminated = True
    for line in body[hunk_index + 1:]:
        stripped = line[:-1] if line.endswith(b"\n") else line
        if stripped == b"\\ No newline at end of file":
            if not line.endswith(b"\n") or not previous_added:
                raise ContractError(f"new-file entry {path} has a misplaced newline marker")
            if content.endswith(b"\n"):
                del content[-1:]
            previous_added = False
            previous_added_terminated = True
            continue
        if not line.startswith(b"+"):
            raise ContractError(f"new-file entry {path} hunk contains a non-added line")
        if previous_added and not previous_added_terminated:
            raise ContractError(f"new-file entry {path} has an unmarked unterminated added line")
        content.extend(line[1:])
        added_count += 1
        previous_added = True
        previous_added_terminated = line.endswith(b"\n")
    if previous_added and not previous_added_terminated:
        raise ContractError(f"new-file entry {path} has an unmarked unterminated added line")
    if added_count != new_count:
        raise ContractError(f"new-file entry {path} hunk line count does not match its header")
    return bytes(content)


def _sidecar_path(spec: Path, *, root: Path = ROOT) -> tuple[Path, str]:
    path = spec.parent / "EVIDENCE-RECONCILIATION.json"
    try:
        relative = path.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, ValueError) as error:
        raise InputError(f"sidecar path escapes the workspace: {path}") from error
    return path, relative


def _read_sidecar_on_disk(path: Path, *, root: Path = ROOT) -> bytes:
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise InputError(f"evidence reconciliation sidecar is not present: {path}") from error
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise InputError(f"evidence reconciliation sidecar escapes the workspace: {path}") from error
    if path.is_symlink() or not resolved.is_file():
        raise InputError(f"evidence reconciliation sidecar must be an ordinary file: {path}")
    try:
        return path.read_bytes()
    except OSError as error:
        raise InputError(f"cannot read evidence reconciliation sidecar {path}: {error}") from error


def _cited_review_paths(raw: bytes) -> set[str]:
    return set(CITED_REVIEW_PATH.findall(raw.decode("utf-8", errors="replace")))


def _evidence_checks(
    state: dict[str, Any],
    loaded: list[tuple[dict[str, Any], Path]],
    completed: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *,
    root: Path = ROOT,
) -> tuple[bool, str]:
    code_records = [
        item for item in completed
        if item[0].get("purpose") in {"normal_review", "cross_review"}
    ]
    frozen: list[tuple[dict[str, Any], Path, bytes, bytes]] = []
    for record, _, record_path in code_records:
        relative = record_path.relative_to(root)
        locator = record.get("candidate_locator")
        if not isinstance(locator, dict):
            return False, f"{relative} has no candidate_locator for evidence checking"
        spec = _ordinary_workspace_file(
            locator["spec_path"], "candidate_locator.spec_path", root=root
        )
        diff = _ordinary_workspace_file(
            locator["diff_path"], "candidate_locator.diff_path", root=root
        )
        sidecar, sidecar_relative = _sidecar_path(spec, root=root)
        embedded = _new_file_entry_bytes(_read_candidate_bytes(diff, "candidate diff"), sidecar_relative)
        if embedded is None:
            continue
        evidence_result = review_evidence.check_reconciliation(embedded, root=root)
        if evidence_result.exit_code:
            return False, f"{relative}: evidence_reconciliation: {evidence_result.detail}"
        try:
            parsed = json.loads(embedded.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            return False, f"{relative}: evidence sidecar bytes are not valid UTF-8 JSON ({error})"
        if parsed.get("task_id") != state.get("task_id"):
            return False, f"{relative}: evidence sidecar task_id does not match STATE"
        cited = _cited_review_paths(_read_candidate_bytes(spec, "candidate SPEC"))
        cited.update(_cited_review_paths(_read_candidate_bytes(diff, "candidate diff")))
        source_reviews = parsed.get("source_reviews") if isinstance(parsed, dict) else None
        if not isinstance(source_reviews, list) or any(path not in source_reviews for path in cited):
            missing = sorted(path for path in cited if not isinstance(source_reviews, list) or path not in source_reviews)
            return False, f"{relative}: evidence citation is not listed in source_reviews: {missing[0]!r}"
        frozen.append(
            (record, sidecar, embedded, _read_sidecar_on_disk(sidecar, root=root))
        )

    if frozen:
        latest_key = max((item[0]["cycle"], item[0]["attempt"]) for item in frozen)
        latest = [item for item in frozen if (item[0]["cycle"], item[0]["attempt"]) == latest_key]
        if len({item[1] for item in latest}) != 1:
            return False, "bound records at the latest (cycle, attempt) derive different sidecar paths"
        if any(item[2] != latest[0][2] for item in latest[1:]):
            return False, "bound records at the latest (cycle, attempt) disagree on embedded sidecar bytes"
        if latest[0][2] != latest[0][3]:
            return False, f"{latest[0][1].relative_to(root)}: on-disk sidecar does not match the latest bound embedded copy"

    schema_version = state.get("schema_version")
    if (
        type(schema_version) is int
        and schema_version >= 3
        and state.get("change_class") not in {"standard", "translation_workflow", "infrastructure"}
    ):
        return False, "change_class must be one of standard, translation_workflow, infrastructure"

    # translation_workflow review-only work divides into two honest shapes:
    # code-contextual review (needs the sidecar discipline above) and the
    # schema-5 surface screen, whose reviewers never read source review
    # records, so a code-contextual completion terminal cannot exist there.
    # A surface task under translation_workflow reconciles by its own strict
    # immutable terminal binding instead (checked in the surface convergence
    # predicate) — but real code records are never waived: when any code
    # record exists, the sidecar discipline applies exactly as usual.
    surface_contract_active = (
        isinstance(state.get("review_contracts"), list)
        and "translation_surface_screen_v1" in state["review_contracts"]
    )
    surface_waives_empty_code_records = (
        surface_contract_active
        and state.get("change_class") == "translation_workflow"
        and not code_records
    )
    if (
        type(schema_version) is int
        and schema_version >= 3
        and state.get("mode") == "review_only"
        and state.get("change_class") in {"infrastructure", "translation_workflow"}
        and (not code_records or len(frozen) != len(code_records))
        and not surface_waives_empty_code_records
    ):
        return False, "evidence_reconciliation_required"

    if type(schema_version) is int and schema_version >= 3:
        senior_paths = set(
            _record_paths_for_field(state, "senior_review_records", root=root)
        )
        for record, path in loaded:
            if path not in senior_paths or record.get("purpose") != "scope_audit":
                continue
            audit_result = review_evidence.check_audit(record, root=root)
            if audit_result.exit_code:
                return False, f"{path.relative_to(root)}: scope_audit: {audit_result.detail}"
    return True, "ok"


def _record_paths_for_field(
    state: dict[str, Any], field: str, *, root: Path = ROOT
) -> list[Path]:
    value = state.get(field, [])
    if value is None:
        value = []
    if isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, list):
        return []
    return [
        _ordinary_workspace_file(item, f"{field}[{index}]", root=root)
        for index, item in enumerate(value)
    ]


def _reviewer_identity_valid(
    state: dict[str, Any], completed: list[tuple[dict[str, Any], dict[str, Any], Path]],
    *, root: Path = ROOT,
) -> tuple[bool, str]:
    schema_version = state.get("schema_version")
    orchestrator = state.get("orchestrator_agent_id")
    if type(schema_version) is int and schema_version >= 3:
        if not isinstance(orchestrator, str) or not orchestrator:
            return False, "orchestrator_agent_id must be a non-empty string for schema_version >= 3"
    elif "orchestrator_agent_id" not in state:
        return True, "ok"
    elif not isinstance(orchestrator, str) or not orchestrator:
        return False, "orchestrator_agent_id must be a non-empty string when present"
    for record, _, path in completed:
        if record.get("agent_id") == orchestrator:
            return False, f"{path.relative_to(root)} reviewer agent_id equals orchestrator_agent_id"
    return True, "ok"


def _children_archived(state: dict[str, Any], *, root: Path = ROOT) -> tuple[bool, str]:
    children = state.get("child_dispatches")
    if not isinstance(children, list) or not children:
        # The surface zero/no-dispatch terminal is the one honest n=0 closure
        # with no children; verify its bound artifact before accepting that.
        if children == [] and isinstance(state.get("surface_zero_path"), str) \
                and isinstance(state.get("review_contracts"), list) \
                and "translation_surface_screen_v1" in state["review_contracts"]:
            try:
                zero_file = _ordinary_workspace_file(
                    state["surface_zero_path"], "surface_zero_path", root=root
                )
            except (ContractError, InputError):
                return False, "children_archived: an empty surface task must bind a verifiable zero artifact"
            zero_value = _read_json(zero_file, "surface zero artifact")
            if not isinstance(zero_value, dict) or zero_value.get("proves_no_surface_dispatch") is not True \
                    or zero_value.get("screen_count") != 0:
                return False, "children_archived: the bound zero artifact does not prove a no-dispatch terminal"
            return True, "ok"
        return False, "child_dispatches cannot be null, absent, or empty with review contracts"
    if any(not isinstance(dispatch, dict) or not _archived(dispatch) for dispatch in children):
        return False, "every child dispatch must be archived and confirmed"
    return True, "ok"


def _done(state: dict[str, Any], *, root: Path = ROOT) -> CheckResult:
    if not isinstance(state.get("task_id"), str) or not state["task_id"]:
        return _result("NEW_CONTRACT_FAILED", "schema_valid: task_id must be a non-empty string", 1)
    for name, check in (("schema_valid", _schema_valid(state)), ("review_contracts_closed", _review_contracts_closed(state))):
        if not check[0]:
            return _result("NEW_CONTRACT_FAILED", f"{name}: {check[1]}", 1)
    try:
        loaded = _load_records(state, root=root)
        completed = _completion_records(state, loaded)
        bindings = _candidate_bindings_valid(state, completed, root=root)
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"candidate_bindings_valid: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"candidate_bindings_valid: malformed JSON value ({error})", 1)
    for name, check in (("completion_records_bound", _completion_records_bound(state, completed)), ("candidate_bindings_valid", bindings)):
        if not check[0]:
            return _result("NEW_CONTRACT_FAILED", f"{name}: {check[1]}", 1)
    try:
        convergence = _translation_convergence_valid(
            state, loaded, completed, root=root
        )
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"translation_convergence: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result(
            "NEW_CONTRACT_FAILED",
            f"translation_convergence: malformed JSON value ({error})",
            1,
        )
    if not convergence[0]:
        return _result("NEW_CONTRACT_FAILED", f"translation_convergence: {convergence[1]}", 1)
    try:
        v2_convergence = _translation_v2_convergence_valid(
            state, loaded, completed, root=root
        )
    except contextual_result_check.ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"translation_v2_convergence: {error}", 1)
    except contextual_result_check.InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"translation_v2_convergence: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"translation_v2_convergence: malformed JSON value ({error})", 1)
    if not v2_convergence[0]:
        return _result("NEW_CONTRACT_FAILED", f"translation_v2_convergence: {v2_convergence[1]}", 1)
    try:
        surface_convergence = _translation_surface_convergence_valid(
            state, loaded, completed, root=root
        )
    except surface_screen_result_check.ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"translation_surface_convergence: {error}", 1)
    except surface_screen_result_check.InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"translation_surface_convergence: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result(
            "NEW_CONTRACT_FAILED",
            f"translation_surface_convergence: malformed JSON value ({error})",
            1,
        )
    if not surface_convergence[0]:
        return _result("NEW_CONTRACT_FAILED", f"translation_surface_convergence: {surface_convergence[1]}", 1)
    identity = _reviewer_identity_valid(state, completed, root=root)
    if not identity[0]:
        return _result("NEW_CONTRACT_FAILED", f"reviewer_identity: {identity[1]}", 1)
    if any(dispatch.get("lineage_verified") is not True for _, dispatch, _ in completed):
        return _result("NEW_CONTRACT_FAILED", "computed_lineage_verified: a bound dispatch lacks literal lineage_verified=true", 1)
    mode = state.get("mode")
    if not isinstance(mode, str) or mode not in {"implement", "review_only"}:
        return _result("NEW_CONTRACT_FAILED", "schema_valid: mode must be implement or review_only", 1)
    if mode == "implement" and state.get("final_validation_passed") is not True:
        return _result("NEW_CONTRACT_FAILED", "final_validation_passed: implement task lacks literal true", 1)
    if state.get("open_accepted_findings") != []:
        return _result("NEW_CONTRACT_FAILED", "no_open_findings: open_accepted_findings must be []", 1)
    if state.get("deferred_findings") != []:
        return _result("NEW_CONTRACT_FAILED", "no_deferred_findings: deferred_findings must be []", 1)
    try:
        evidence = _evidence_checks(state, loaded, completed, root=root)
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"evidence_reconciliation: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"evidence_reconciliation: malformed JSON value ({error})", 1)
    if not evidence[0]:
        return _result("NEW_CONTRACT_FAILED", f"evidence_reconciliation: {evidence[1]}", 1)
    archived = _children_archived(state, root=root)
    if not archived[0]:
        return _result("NEW_CONTRACT_FAILED", f"children_archived: {archived[1]}", 1)
    return _result("DONE_VERIFIED", "DONE predicate verified", 0)


def check_state(
    state_path: str | Path,
    *,
    target: str | None = None,
    manifest_path: str | Path | None = None,
    workspace_root: str | Path | None = None,
) -> CheckResult:
    """Check one STATE file and return a structured result without printing."""
    if target is not None and (not isinstance(target, str) or target not in {"DONE", "STOP"}):
        return _result("INPUT_ERROR", "target must be DONE or STOP", 2)
    try:
        root = (
            Path(workspace_root).resolve(strict=True)
            if workspace_root is not None
            else ROOT.resolve()
        )
        if not root.is_dir():
            raise InputError("workspace_root must be an existing directory")
        state_file = Path(state_path)
        if workspace_root is not None and not state_file.is_absolute():
            state_file = root / state_file
        state = _read_json(state_file, "STATE")
    except (InputError, OSError) as error:
        return _result("INPUT_ERROR", str(error), 2)
    if not isinstance(state, dict) or not isinstance(state.get("task_id"), str) or not state["task_id"]:
        return _result("INPUT_ERROR", "STATE task_id must be a non-empty string", 2)
    try:
        unsupported = _strict_manifest(Path(manifest_path) if manifest_path is not None else DEFAULT_MANIFEST)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except ValueError as error:
        return _result("MANIFEST_INVALID", str(error), 1)
    if state["task_id"] in unsupported:
        return _result("UNSUPPORTED_LEGACY", "task is outside the B-prime new-contract adoption boundary", 3)
    schema = _schema_valid(state)
    if not schema[0]:
        return _result("NEW_CONTRACT_FAILED", f"schema_valid: {schema[1]}", 1)
    state_name = state.get("state")
    if not isinstance(state_name, str) or state_name not in CANONICAL_STATES:
        return _result("NEW_CONTRACT_FAILED", "schema_valid: state must be a known persisted workflow state", 1)
    if target is None:
        if state_name not in {"DONE", "STOP"}:
            return _result("INPUT_ERROR", "non-terminal STATE requires --target DONE or STOP", 2)
        target = state_name
    if target == "STOP":
        review_observations = _stop_records_forbid_runtime_observation(
            state, root=root
        )
        if not review_observations[0]:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"review_records: {review_observations[1]}",
                1,
            )
        # C4-03: STOP must apply the same persisted all-source surface
        # activity predicate as DONE, so deleting or relabeling
        # child_dispatches can never close partial surface records, terminal
        # bindings, or artifacts.  The review-only surface funnel has exactly
        # two terminals — the whole-screen stage or the zero/no-dispatch
        # artifact — and any persisted surface activity belongs in DONE (or
        # WAIT_USER when abandoned), not STOP.  Record loading stays tolerant
        # of unavailable or malformed records, matching STOP's established
        # narrow semantics for everything that is not surface activity.
        if _surface_activity_present(state, _load_records_for_stop(state, root=root)):
            return _result(
                "NEW_CONTRACT_FAILED",
                "STOP cannot close a dispatched surface screen: persisted "
                "surface activity (surface dispatch, completion record, or "
                "terminal binding) requires the surface terminal predicate; "
                "finish the whole-screen stage, record the zero/no-dispatch "
                "artifact, or wait in WAIT_USER",
                1,
            )
        children = state.get("child_dispatches")
        if children == [] or (
            isinstance(children, list)
            and all(isinstance(item, dict) and _archived(item) for item in children)
        ):
            return _result("STOP_VERIFIED", "STOP archive predicate verified", 0)
        return _result(
            "NEW_CONTRACT_FAILED",
            "STOP requires no children or every child archived with literal archive_confirmed=true",
            1,
        )
    return _done(state, root=root)


def check_wave_state_context(
    state_path: str | Path,
    *,
    task_id: str,
    workspace_id: str,
    orchestrator_agent_id: str,
    workspace_root: str | Path,
    manifest_path: str | Path | None = None,
) -> CheckResult:
    """Verify DONE plus the direct-child context required by a managed wave.

    The ordinary serial checker deliberately remains backwards compatible: old
    STATE records do not acquire wave-only fields.  A wave checker calls this
    stricter entry point after resolving the STATE path from WAVE.json.
    """
    closed = check_state(
        state_path,
        target="DONE",
        manifest_path=manifest_path,
        workspace_root=workspace_root,
    )
    if closed.exit_code:
        return closed
    try:
        state = _read_json(Path(state_path), "wave-bound STATE")
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    if not isinstance(state, dict):
        return _result("NEW_CONTRACT_FAILED", "wave_context: STATE must be an object", 1)
    if state.get("state") != "DONE":
        return _result(
            "NEW_CONTRACT_FAILED",
            "wave_context: managed-wave closure requires persisted STATE.state=DONE",
            1,
        )
    if state.get("task_id") != task_id:
        return _result("NEW_CONTRACT_FAILED", "wave_context: task_id does not match WAVE", 1)
    if state.get("workspace_id") != workspace_id:
        return _result("NEW_CONTRACT_FAILED", "wave_context: workspace_id does not match WAVE", 1)
    if state.get("orchestrator_agent_id") != orchestrator_agent_id:
        return _result(
            "NEW_CONTRACT_FAILED",
            "wave_context: orchestrator_agent_id does not match WAVE",
            1,
        )
    children = state.get("child_dispatches")
    if not isinstance(children, list):
        return _result("NEW_CONTRACT_FAILED", "wave_context: child_dispatches must be an array", 1)
    seen_agents: set[str] = set()
    for index, dispatch in enumerate(children):
        if not isinstance(dispatch, dict):
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}] must be an object",
                1,
            )
        if dispatch.get("workspace_id") != workspace_id:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}].workspace_id does not match its task",
                1,
            )
        if dispatch.get("task_id") != task_id:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}].task_id does not match its task",
                1,
            )
        if dispatch.get("parent_agent_id") != orchestrator_agent_id:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}].parent_agent_id does not match WAVE",
                1,
            )
        purpose = dispatch.get("purpose")
        if not isinstance(purpose, str) or not purpose:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}].purpose must be a non-empty string",
                1,
            )
        if dispatch.get("lineage_verified") is not True:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}] lacks literal lineage_verified=true",
                1,
            )
        if str(dispatch.get("role", "")).lower() == "orchestrator":
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}] is a forbidden lane orchestrator",
                1,
            )
        agent_id = dispatch.get("agent_id")
        if not isinstance(agent_id, str) or not agent_id:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: child_dispatches[{index}].agent_id must be non-empty",
                1,
            )
        if agent_id in seen_agents:
            return _result(
                "NEW_CONTRACT_FAILED",
                f"wave_context: duplicate child agent_id {agent_id!r}",
                1,
            )
        seen_agents.add(agent_id)
    return _result("DONE_VERIFIED", "DONE and managed-wave context verified", 0)


def validate(path: str | Path, target: str | None = None) -> CheckResult:
    """Compatibility-friendly programmatic entry point."""
    return check_state(path, target=target)


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError(f"invalid command-line arguments: {message}")


def main(argv: list[str] | None = None) -> int:
    parser = _ArgumentParser(description=__doc__)
    parser.add_argument("state", help="path to STATE.json")
    parser.add_argument("--target", choices=("DONE", "STOP"))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--workspace-root")
    try:
        args = parser.parse_args(argv)
    except InputError as error:
        result = _result("INPUT_ERROR", str(error), 2)
        print(f"{result.outcome}: {result.detail}")
        return result.exit_code
    result = check_state(
        args.state,
        target=args.target,
        manifest_path=args.manifest,
        workspace_root=args.workspace_root,
    )
    print(f"{result.outcome}: {result.detail}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
