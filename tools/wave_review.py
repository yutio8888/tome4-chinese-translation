#!/usr/bin/env python3
"""Fail-closed Phase 1 managed-wave verifier.

WAVE.json is the only CLI entry point.  Every other artifact path, identity,
task, lane, revision set, and content path is resolved from that record.
Each invocation additionally requires a 1:1 workspace_id=root map; roots must
be real worktrees in the same Git common directory, and task-owned paths are
resolved only inside the owning root.

Phase 1 intentionally supports only empty TARGET-PATCH files.  The empty path
is sufficient for the bounded no-change dry-run and is still bound to the base
commit, final candidate, workset, merge queue, and unchanged translation bytes.
Non-empty target patches are parsed strictly and then rejected; this tool does
not claim production Lua apply support.

Publication is split into prepare-publication, publish, and done.  publish
performs pre-publication identity/byte checks and an atomic exact-byte replace;
done never publishes and checks only an already-published DONE closure.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass, replace
import hashlib
import itertools
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from typing import Any, Callable, Mapping

import ai_state_check
from i18nlib.config import DEFAULT_VERSION, load_manifest
from i18nlib.errors import ConfigurationError, I18nToolError
from i18nlib.locale_model import LocaleLoader
from i18nlib.runtime import LuaRuntime


ROOT = Path(__file__).resolve().parents[1]
SHA256 = re.compile(r"^[0-9a-f]{64}$")
OID = re.compile(r"^[0-9a-f]{40}$")
WAVE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
LANE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
RUNTIME_PREFIXES = (".ai/task/", ".ai/waves/", ".ai/reviews/", ".artifacts/")
COLLATERAL_FORBIDDEN_MARKER = "phase1_collateral: forbidden"
FULL_REVIEW_PHASES = frozenset({"REVIEW", "RE_REVIEW", "FINAL_REVIEW"})
MIN_LANES = 2
MAX_LANES = 4

WAVE_KEYS = frozenset({
    "schema_id", "schema_version", "wave_id", "state", "base_commit",
    "orchestrator_agent_id", "root_workspace_id", "ordered_lane_ids", "lanes",
    "integration", "merge_queue_path", "conflict_preflight_path",
    "conflict_preflight_identity", "wave_evidence_path",
})
WAVE_LANE_KEYS = frozenset({
    "lane_id", "task_id", "workspace_id", "state_path", "spec_path",
    "workset_path", "workset_identity", "collateral_empty",
    "final_candidate_identity", "final_review_kind", "final_review_dispatch_id",
    "final_review_record", "target_patch_path", "target_patch_identity",
})
WAVE_INTEGRATION_KEYS = frozenset({
    "task_id", "workspace_id", "state_path", "spec_path", "allowed_files_path",
    "allowed_files_identity", "combined_candidate_identity", "content_diff_path",
    "content_diff_identity", "final_review_kind", "final_review_dispatch_id",
    "final_review_record",
})
MERGE_KEYS = frozenset({
    "schema_id", "schema_version", "wave_id", "base_commit", "ordered_lane_ids", "items",
})
MERGE_ITEM_KEYS = frozenset({
    "lane_id", "task_id", "target_patch_path", "target_patch_identity", "candidate_identity",
})
PREFLIGHT_KEYS = frozenset({
    "schema_id", "schema_version", "wave_id", "base_commit", "ordered_lane_ids", "sets",
    "pairwise_intersections_empty", "result",
})
PREFLIGHT_SET_KEYS = frozenset({
    "lane_id", "task_id", "call_set", "call_set_identity", "runtime_key_set",
    "runtime_key_set_identity", "term_narrative_set", "term_narrative_set_identity",
    "collateral_authorization", "collateral_authorization_identity",
})
CALL_SET_KEYS = frozenset({"schema_id", "schema_version", "lane_id", "task_id", "items"})
CALL_KEYS = frozenset({"revision_key", "section", "source", "source_tag", "args_order", "special"})
RUNTIME_SET_KEYS = CALL_SET_KEYS
RUNTIME_ITEM_KEYS = frozenset({"runtime_key", "source_tag"})
TERM_SET_KEYS = CALL_SET_KEYS
TERM_ITEM_KEYS = frozenset({"kind", "key"})
WORKSET_KEYS = frozenset({
    "schema_id", "schema_version", "lane_id", "task_id", "ordered_revision_keys", "calls",
    "primary_content_paths",
})
COLLATERAL_KEYS = frozenset({
    "schema_id", "schema_version", "lane_id", "task_id", "spec_path", "spec_identity",
    "scope_path", "scope_identity", "allowed_files_path", "allowed_files_identity",
    "primary_content_paths", "ordinary_non_collateral_paths", "collateral_paths",
})
ALLOWED_KEYS = frozenset({
    "schema_id", "schema_version", "task_id", "wave_id", "allowed_files",
    "translation_fix_paths", "wave_evidence_path",
})
CONTENT_DIFF_KEYS = frozenset({
    "schema_id", "schema_version", "wave_id", "task_id", "base_commit",
    "translation_paths", "changed_paths", "entries",
})
CONTENT_DIFF_ENTRY_KEYS = frozenset({"path", "old_content_sha256", "new_content_sha256"})
EVIDENCE_KEYS = frozenset({
    "schema_id", "schema_version", "wave_id", "base_commit", "orchestrator_agent_id",
    "wave_record_identity", "merge_queue_identity", "conflict_preflight_path",
    "conflict_preflight_identity", "lanes", "integration", "collateral_empty", "gates_result",
})
EVIDENCE_LANE_KEYS = frozenset({
    "lane_id", "task_id", "workspace_id", "final_candidate_identity", "target_patch_identity",
    "final_review_kind", "final_review_dispatch_id", "final_review_record", "done_verified",
})
EVIDENCE_INTEGRATION_KEYS = frozenset({
    "task_id", "workspace_id", "executor_agent_id", "combined_candidate_identity",
    "content_diff_path", "content_diff_identity", "final_review_kind",
    "final_review_dispatch_id", "final_review_record", "initial_git", "done_verified",
})
INITIAL_GIT_KEYS = frozenset({"head_commit", "index_tree", "worktree_tree"})
PATCH_KEYS = frozenset({
    "schema_id", "schema_version", "base_commit", "task_id", "candidate_identity",
    "ordered_revision_keys", "changes",
})
PATCH_CHANGE_KEYS = frozenset({
    "revision_key", "section", "source", "source_tag", "args_order", "special", "call_index",
    "old_target", "new_target",
})
CONTEXTUAL_PAYLOAD_KEYS = frozenset({
    "contract", "ordered_revision_keys", "translation_snapshot", "fixed_source_identity",
    "terminology_snapshot", "bounded_context", "rendered_briefing",
})


class InputError(Exception):
    """Unreadable, malformed, unsafe, or unavailable input (exit 2)."""


class ContractError(Exception):
    """Readable input that violates a managed-wave contract (exit 1)."""


@dataclass(frozen=True)
class CheckResult:
    outcome: str
    detail: str
    exit_code: int


def _exact(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or frozenset(value) != keys:
        missing = sorted(keys - frozenset(value) if isinstance(value, dict) else keys)
        extra = sorted(frozenset(value) - keys if isinstance(value, dict) else [])
        raise ContractError(f"{label} must have exactly {len(keys)} keys; missing={missing}, extra={extra}")
    return value


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty string")
    return value


def _json_string(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{label} must be a JSON string")
    return value


def _literal_version(value: dict[str, Any], schema_id: str, label: str) -> None:
    if value.get("schema_id") != schema_id or type(value.get("schema_version")) is not int or value.get("schema_version") != 1:
        raise ContractError(f"{label} must declare schema_id={schema_id!r} and integer schema_version=1")


def _hex(value: object, pattern: re.Pattern[str], label: str) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise ContractError(f"{label} has an invalid lowercase digest/OID")
    return value


def _nullable_hex(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _hex(value, SHA256, label)


def _nullable_string(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _string(value, label)


def _relative_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise InputError(f"{label} must be a normalized workspace-relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts):
        raise InputError(f"{label} escapes or is not normalized: {value!r}")
    if len(value) >= 2 and value[0].isalpha() and value[1] == ":":
        raise InputError(f"{label} must not be a drive path: {value!r}")
    return value


def _path_array(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ContractError(f"{label} must be an array")
    paths = [_relative_path(item, f"{label}[{index}]") for index, item in enumerate(value)]
    if paths != sorted(paths, key=lambda item: item.encode("utf-8")) or len(paths) != len(set(paths)):
        raise ContractError(f"{label} must be path-byte sorted and unique")
    return paths


def _string_array(value: object, label: str, *, sorted_unique: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ContractError(f"{label} must be an array of non-empty strings")
    result = list(value)
    if len(result) != len(set(result)):
        raise ContractError(f"{label} must be unique")
    if sorted_unique and result != sorted(result, key=lambda item: item.encode("utf-8")):
        raise ContractError(f"{label} must be byte-sorted")
    return result


def canonical_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContractError(f"value is not canonicalizable JSON: {error}") from error


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _validate_call(value: object, label: str) -> dict[str, Any]:
    item = _exact(value, CALL_KEYS, label)
    for key in ("revision_key", "section", "source_tag"):
        _string(item[key], f"{label}.{key}")
    _json_string(item["source"], f"{label}.source")
    canonical_bytes(item["args_order"])
    canonical_bytes(item["special"])
    return item


def _call_sort_key(item: dict[str, Any]) -> tuple[bytes, ...]:
    return (
        item["revision_key"].encode(), item["section"].encode(), item["source"].encode(),
        item["source_tag"].encode(), canonical_bytes(item["args_order"]), canonical_bytes(item["special"]),
    )


def _validate_call_set(value: object) -> dict[str, Any]:
    obj = _exact(value, CALL_SET_KEYS, "call-set/1")
    _literal_version(obj, "call-set/1", "call-set/1")
    _string(obj["lane_id"], "call-set/1.lane_id")
    _string(obj["task_id"], "call-set/1.task_id")
    if not isinstance(obj["items"], list):
        raise ContractError("call-set/1.items must be an array")
    items = [_validate_call(item, f"call-set/1.items[{index}]") for index, item in enumerate(obj["items"])]
    keys = [_call_sort_key(item) for item in items]
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise ContractError("call-set/1.items must be uniquely sorted by the canonical call key")
    return obj


def _validate_runtime_set(value: object) -> dict[str, Any]:
    obj = _exact(value, RUNTIME_SET_KEYS, "runtime-key-set/1")
    _literal_version(obj, "runtime-key-set/1", "runtime-key-set/1")
    _string(obj["lane_id"], "runtime-key-set/1.lane_id")
    _string(obj["task_id"], "runtime-key-set/1.task_id")
    if not isinstance(obj["items"], list):
        raise ContractError("runtime-key-set/1.items must be an array")
    keys: list[tuple[bytes, bytes]] = []
    for index, value_item in enumerate(obj["items"]):
        item = _exact(value_item, RUNTIME_ITEM_KEYS, f"runtime-key-set/1.items[{index}]")
        keys.append((_string(item["runtime_key"], "runtime_key").encode(), _string(item["source_tag"], "source_tag").encode()))
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise ContractError("runtime-key-set/1.items must be uniquely sorted")
    return obj


def _validate_term_set(value: object) -> dict[str, Any]:
    obj = _exact(value, TERM_SET_KEYS, "term-narrative-set/1")
    _literal_version(obj, "term-narrative-set/1", "term-narrative-set/1")
    _string(obj["lane_id"], "term-narrative-set/1.lane_id")
    _string(obj["task_id"], "term-narrative-set/1.task_id")
    if not isinstance(obj["items"], list):
        raise ContractError("term-narrative-set/1.items must be an array")
    keys: list[tuple[bytes, bytes]] = []
    for index, value_item in enumerate(obj["items"]):
        item = _exact(value_item, TERM_ITEM_KEYS, f"term-narrative-set/1.items[{index}]")
        kind = _string(item["kind"], "term kind")
        if kind not in {"term_claim", "narrative_closure"}:
            raise ContractError("term-narrative-set/1 kind is invalid")
        keys.append((kind.encode(), _string(item["key"], "term key").encode()))
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise ContractError("term-narrative-set/1.items must be uniquely sorted")
    return obj


def _validate_workset(value: object) -> dict[str, Any]:
    obj = _exact(value, WORKSET_KEYS, "lane-workset/1")
    _literal_version(obj, "lane-workset/1", "lane-workset/1")
    _string(obj["lane_id"], "lane-workset/1.lane_id")
    _string(obj["task_id"], "lane-workset/1.task_id")
    keys = _string_array(obj["ordered_revision_keys"], "lane-workset/1.ordered_revision_keys")
    if not keys:
        raise ContractError("lane-workset/1 workset must be non-empty")
    if not isinstance(obj["calls"], list):
        raise ContractError("lane-workset/1.calls must be an array")
    calls = [_validate_call(item, f"lane-workset/1.calls[{index}]") for index, item in enumerate(obj["calls"])]
    if [item["revision_key"] for item in calls] != keys:
        raise ContractError("lane-workset/1 calls must be 1:1 and in ordered_revision_keys order")
    call_identities = [
        (
            item["section"],
            item["source"],
            item["source_tag"],
            canonical_bytes(item["args_order"]),
            canonical_bytes(item["special"]),
        )
        for item in calls
    ]
    if len(call_identities) != len(set(call_identities)):
        raise ContractError("lane-workset/1 calls must identify distinct pinned Lua calls")
    _path_array(obj["primary_content_paths"], "lane-workset/1.primary_content_paths")
    return obj


def _validate_collateral(value: object) -> dict[str, Any]:
    obj = _exact(value, COLLATERAL_KEYS, "collateral-authorization/1")
    _literal_version(obj, "collateral-authorization/1", "collateral-authorization/1")
    _string(obj["lane_id"], "collateral lane_id")
    _string(obj["task_id"], "collateral task_id")
    for field in ("spec_path", "scope_path", "allowed_files_path"):
        _relative_path(obj[field], f"collateral.{field}")
    for field in ("spec_identity", "scope_identity", "allowed_files_identity"):
        _hex(obj[field], SHA256, f"collateral.{field}")
    for field in ("primary_content_paths", "ordinary_non_collateral_paths", "collateral_paths"):
        _path_array(obj[field], f"collateral.{field}")
    return obj


def _validate_allowed(value: object) -> dict[str, Any]:
    obj = _exact(value, ALLOWED_KEYS, "task-content-allowed-files/1")
    _literal_version(obj, "task-content-allowed-files/1", "task-content-allowed-files/1")
    _string(obj["task_id"], "allowed-files task_id")
    _string(obj["wave_id"], "allowed-files wave_id")
    _path_array(obj["allowed_files"], "allowed_files")
    _path_array(obj["translation_fix_paths"], "translation_fix_paths")
    if obj["wave_evidence_path"] is not None:
        _relative_path(obj["wave_evidence_path"], "wave_evidence_path")
    return obj


def _validate_content_diff(value: object) -> dict[str, Any]:
    obj = _exact(value, CONTENT_DIFF_KEYS, "integration-content-diff/1")
    _literal_version(obj, "integration-content-diff/1", "integration-content-diff/1")
    _string(obj["wave_id"], "content diff wave_id")
    _string(obj["task_id"], "content diff task_id")
    _hex(obj["base_commit"], OID, "content diff base_commit")
    paths = _path_array(obj["translation_paths"], "content diff translation_paths")
    changed = _path_array(obj["changed_paths"], "content diff changed_paths")
    if not set(changed).issubset(paths):
        raise ContractError("content diff changed_paths must be a subset of translation_paths")
    if not isinstance(obj["entries"], list):
        raise ContractError("content diff entries must be an array")
    entry_paths: list[str] = []
    for index, value_item in enumerate(obj["entries"]):
        item = _exact(value_item, CONTENT_DIFF_ENTRY_KEYS, f"content diff entries[{index}]")
        entry_paths.append(_relative_path(item["path"], "content diff entry path"))
        _hex(item["old_content_sha256"], SHA256, "old_content_sha256")
        _hex(item["new_content_sha256"], SHA256, "new_content_sha256")
    if entry_paths != changed:
        raise ContractError("content diff entries must be 1:1 and in changed_paths order")
    return obj


def _validate_patch(value: object) -> dict[str, Any]:
    obj = _exact(value, PATCH_KEYS, "target-patch/1")
    _literal_version(obj, "target-patch/1", "target-patch/1")
    _hex(obj["base_commit"], OID, "target patch base_commit")
    _string(obj["task_id"], "target patch task_id")
    _hex(obj["candidate_identity"], SHA256, "target patch candidate_identity")
    ordered = _string_array(obj["ordered_revision_keys"], "target patch ordered_revision_keys")
    if not isinstance(obj["changes"], list):
        raise ContractError("target patch changes must be an array")
    seen_revision: set[str] = set()
    seen_locator: set[tuple[bytes, ...]] = set()
    changed_keys: list[str] = []
    for index, value_item in enumerate(obj["changes"]):
        item = _exact(value_item, PATCH_CHANGE_KEYS, f"target patch changes[{index}]")
        for field in ("revision_key", "section", "source_tag"):
            _string(item[field], f"target patch change.{field}")
        for field in ("source", "old_target", "new_target"):
            _json_string(item[field], f"target patch change.{field}")
        canonical_bytes(item["args_order"])
        canonical_bytes(item["special"])
        call_index = item["call_index"]
        if call_index is not None and (type(call_index) is not int or call_index < 0):
            raise ContractError("target patch call_index must be null or a non-negative integer")
        if item["old_target"] == item["new_target"]:
            raise ContractError("target patch changes may contain only changed targets")
        revision = item["revision_key"]
        locator = (
            item["section"].encode(), item["source"].encode(), item["source_tag"].encode(),
            canonical_bytes(item["args_order"]), canonical_bytes(item["special"]),
            b"null" if call_index is None else str(call_index).encode(),
        )
        if revision in seen_revision or locator in seen_locator:
            raise ContractError("target patch contains duplicate revisions or overlapping call locators")
        seen_revision.add(revision)
        seen_locator.add(locator)
        changed_keys.append(revision)
    positions = {key: index for index, key in enumerate(ordered)}
    if any(key not in positions for key in changed_keys) or changed_keys != sorted(changed_keys, key=positions.__getitem__):
        raise ContractError("target patch changes are not an ordered subset of ordered_revision_keys")
    return obj


def _validate_merge(value: object) -> dict[str, Any]:
    obj = _exact(value, MERGE_KEYS, "merge-queue/1")
    _literal_version(obj, "merge-queue/1", "merge-queue/1")
    _string(obj["wave_id"], "merge wave_id")
    _hex(obj["base_commit"], OID, "merge base_commit")
    _string_array(obj["ordered_lane_ids"], "merge ordered_lane_ids")
    if not isinstance(obj["items"], list):
        raise ContractError("merge items must be an array")
    for index, value_item in enumerate(obj["items"]):
        item = _exact(value_item, MERGE_ITEM_KEYS, f"merge items[{index}]")
        _string(item["lane_id"], "merge lane_id")
        _string(item["task_id"], "merge task_id")
        _relative_path(item["target_patch_path"], "merge target_patch_path")
        _nullable_hex(item["target_patch_identity"], "merge target_patch_identity")
        _nullable_hex(item["candidate_identity"], "merge candidate_identity")
    return obj


def _validate_preflight(value: object) -> dict[str, Any]:
    obj = _exact(value, PREFLIGHT_KEYS, "conflict-preflight/1")
    _literal_version(obj, "conflict-preflight/1", "conflict-preflight/1")
    _string(obj["wave_id"], "preflight wave_id")
    _hex(obj["base_commit"], OID, "preflight base_commit")
    _string_array(obj["ordered_lane_ids"], "preflight ordered_lane_ids")
    if not isinstance(obj["sets"], list):
        raise ContractError("preflight sets must be an array")
    for index, value_item in enumerate(obj["sets"]):
        item = _exact(value_item, PREFLIGHT_SET_KEYS, f"preflight sets[{index}]")
        _string(item["lane_id"], "preflight lane_id")
        _string(item["task_id"], "preflight task_id")
        _validate_call_set(item["call_set"])
        _hex(item["call_set_identity"], SHA256, "call_set_identity")
        _validate_runtime_set(item["runtime_key_set"])
        _hex(item["runtime_key_set_identity"], SHA256, "runtime_key_set_identity")
        _validate_term_set(item["term_narrative_set"])
        _hex(item["term_narrative_set_identity"], SHA256, "term_narrative_set_identity")
        _validate_collateral(item["collateral_authorization"])
        _hex(item["collateral_authorization_identity"], SHA256, "collateral_authorization_identity")
    if type(obj["pairwise_intersections_empty"]) is not bool:
        raise ContractError("pairwise_intersections_empty must be a JSON boolean")
    if obj["result"] not in {"PASS", "FAIL"}:
        raise ContractError("preflight result must be PASS or FAIL")
    return obj


def _validate_wave(value: object) -> dict[str, Any]:
    obj = _exact(value, WAVE_KEYS, "wave/1")
    _literal_version(obj, "wave/1", "wave/1")
    wave_id = _string(obj["wave_id"], "wave_id")
    if WAVE_ID.fullmatch(wave_id) is None:
        raise ContractError("wave_id is not path-safe")
    if obj["state"] not in {"PLANNED", "PREFLIGHT", "DISPATCHED", "LANES_READY", "INTEGRATING", "FINAL_REVIEW", "GATED", "DONE", "WAIT_USER", "STOP"}:
        raise ContractError("wave state is invalid")
    _hex(obj["base_commit"], OID, "wave base_commit")
    _string(obj["orchestrator_agent_id"], "orchestrator_agent_id")
    root_workspace = _string(obj["root_workspace_id"], "root_workspace_id")
    ordered = _string_array(obj["ordered_lane_ids"], "ordered_lane_ids")
    lane_count = len(ordered)
    if not MIN_LANES <= lane_count <= MAX_LANES or any(
        LANE_ID.fullmatch(item) is None for item in ordered
    ):
        raise ContractError("Phase 1 requires 2 through 4 path-safe lane IDs")
    if not isinstance(obj["lanes"], list) or len(obj["lanes"]) != lane_count:
        raise ContractError("wave lanes must match ordered_lane_ids cardinality")
    workspaces: list[str] = []
    lane_ids: list[str] = []
    task_ids: list[str] = []
    for index, value_item in enumerate(obj["lanes"]):
        lane = _exact(value_item, WAVE_LANE_KEYS, f"wave lanes[{index}]")
        lane_id = _string(lane["lane_id"], "lane_id")
        task_id = _string(lane["task_id"], "lane task_id")
        workspace_id = _string(lane["workspace_id"], "lane workspace_id")
        lane_ids.append(lane_id)
        task_ids.append(task_id)
        workspaces.append(workspace_id)
        formulas = {
            "state_path": f".ai/task/{task_id}/STATE.json",
            "spec_path": f".ai/task/{task_id}/SPEC.md",
            "workset_path": f".ai/waves/{wave_id}/LANE-{lane_id}-WORKSET.json",
            "target_patch_path": f".ai/task/{task_id}/TARGET-PATCH.json",
        }
        for field, expected in formulas.items():
            _relative_path(lane[field], f"lane.{field}")
            if lane[field] != expected:
                raise ContractError(f"lane.{field} is not the WAVE-derived path")
        _nullable_hex(lane["workset_identity"], "lane workset_identity")
        if type(lane["collateral_empty"]) is not bool:
            raise ContractError("lane collateral_empty must be a JSON boolean")
        _nullable_hex(lane["final_candidate_identity"], "lane final_candidate_identity")
        if lane["final_review_kind"] not in {None, "full"}:
            raise ContractError("lane final_review_kind must be null or full")
        _nullable_string(lane["final_review_dispatch_id"], "lane final_review_dispatch_id")
        if lane["final_review_record"] is not None:
            _relative_path(lane["final_review_record"], "lane final_review_record")
        _nullable_hex(lane["target_patch_identity"], "lane target_patch_identity")
    if lane_ids != ordered:
        raise ContractError("ordered_lane_ids and lanes must be 1:1 in order")
    if len(set(task_ids)) != lane_count:
        raise ContractError("lane task_ids must be distinct")
    if len(set(workspaces)) != lane_count or root_workspace in workspaces:
        raise ContractError("lane workspaces must be distinct and different from root_workspace_id")
    integration = _exact(obj["integration"], WAVE_INTEGRATION_KEYS, "wave integration")
    for field in ("task_id", "workspace_id"):
        _nullable_string(integration[field], f"integration {field}")
    for field in ("state_path", "spec_path", "allowed_files_path", "content_diff_path", "final_review_record"):
        if integration[field] is not None:
            _relative_path(integration[field], f"integration {field}")
    for field in ("allowed_files_identity", "combined_candidate_identity", "content_diff_identity"):
        _nullable_hex(integration[field], f"integration {field}")
    if integration["final_review_kind"] not in {None, "full"}:
        raise ContractError("integration final_review_kind must be null or full")
    _nullable_string(integration["final_review_dispatch_id"], "integration final_review_dispatch_id")
    _relative_path(obj["merge_queue_path"], "merge_queue_path")
    if obj["merge_queue_path"] != f".ai/waves/{wave_id}/MERGE-QUEUE.json":
        raise ContractError("merge_queue_path is not WAVE-derived")
    _relative_path(obj["conflict_preflight_path"], "conflict_preflight_path")
    if obj["conflict_preflight_path"] != f".ai/waves/{wave_id}/CONFLICT-PREFLIGHT.json":
        raise ContractError("conflict_preflight_path is not WAVE-derived")
    _nullable_hex(obj["conflict_preflight_identity"], "conflict_preflight_identity")
    _relative_path(obj["wave_evidence_path"], "wave_evidence_path")
    if obj["wave_evidence_path"] != f"evidence/quality/p2-waves/{wave_id}-adjudication.json":
        raise ContractError("wave_evidence_path is not WAVE-derived")
    _validate_wave_phase_bindings(obj)
    return obj


def _fields_are(value: dict[str, Any], fields: tuple[str, ...], *, bound: bool) -> bool:
    return all((value[field] is not None) is bound for field in fields)


def _validate_wave_phase_bindings(wave: dict[str, Any]) -> None:
    """Reject phase labels whose frozen bindings describe another phase."""
    state = wave["state"]
    ordered = (
        "PLANNED", "PREFLIGHT", "DISPATCHED", "LANES_READY", "INTEGRATING",
        "FINAL_REVIEW", "GATED", "DONE",
    )
    if state in {"WAIT_USER", "STOP"}:
        return
    rank = ordered.index(state)
    dispatched = rank >= ordered.index("DISPATCHED")
    lanes_ready = rank >= ordered.index("LANES_READY")
    integrating = rank >= ordered.index("INTEGRATING")
    final_review = rank >= ordered.index("FINAL_REVIEW")
    gated = rank >= ordered.index("GATED")
    if (wave["conflict_preflight_identity"] is not None) is not dispatched:
        # PREFLIGHT may bind the freshly computed identity before transitioning.
        if not (state == "PREFLIGHT" and wave["conflict_preflight_identity"] is not None):
            raise ContractError("wave preflight identity binding is illegal for its state")
    lane_final_fields = (
        "final_candidate_identity", "final_review_kind", "final_review_dispatch_id",
        "final_review_record", "target_patch_identity",
    )
    for lane in wave["lanes"]:
        if (lane["workset_identity"] is not None) is not dispatched:
            if not (state == "PREFLIGHT" and lane["workset_identity"] is not None):
                raise ContractError("wave workset identity binding is illegal for its state")
        if not _fields_are(lane, lane_final_fields, bound=lanes_ready):
            raise ContractError("wave lane final bindings are illegal for its state")
        if dispatched and lane["collateral_empty"] is not True:
            raise ContractError("dispatched wave requires literal collateral_empty=true")
    integration = wave["integration"]
    integration_task_fields = (
        "task_id", "workspace_id", "state_path", "spec_path", "allowed_files_path",
        "allowed_files_identity",
    )
    integration_candidate_fields = (
        "combined_candidate_identity", "content_diff_path", "content_diff_identity",
    )
    integration_review_fields = (
        "final_review_kind", "final_review_dispatch_id", "final_review_record",
    )
    if not _fields_are(integration, integration_task_fields, bound=integrating):
        raise ContractError("wave integration task bindings are illegal for its state")
    if not _fields_are(integration, integration_candidate_fields, bound=final_review):
        raise ContractError("wave integration candidate bindings are illegal for its state")
    if not _fields_are(integration, integration_review_fields, bound=gated):
        raise ContractError("wave integration review bindings are illegal for its state")


def _validate_evidence(value: object) -> dict[str, Any]:
    obj = _exact(value, EVIDENCE_KEYS, "wave-evidence/1")
    _literal_version(obj, "wave-evidence/1", "wave-evidence/1")
    _string(obj["wave_id"], "evidence wave_id")
    _hex(obj["base_commit"], OID, "evidence base_commit")
    _string(obj["orchestrator_agent_id"], "evidence orchestrator_agent_id")
    for field in ("wave_record_identity", "merge_queue_identity", "conflict_preflight_identity"):
        _hex(obj[field], SHA256, f"evidence {field}")
    _relative_path(obj["conflict_preflight_path"], "evidence conflict_preflight_path")
    if not isinstance(obj["lanes"], list):
        raise ContractError("evidence lanes must be an array")
    for index, value_item in enumerate(obj["lanes"]):
        item = _exact(value_item, EVIDENCE_LANE_KEYS, f"evidence lanes[{index}]")
        for field in ("lane_id", "task_id", "workspace_id", "final_review_dispatch_id"):
            _string(item[field], f"evidence lane {field}")
        _relative_path(item["final_review_record"], "evidence lane final_review_record")
        _hex(item["final_candidate_identity"], SHA256, "evidence lane candidate")
        _hex(item["target_patch_identity"], SHA256, "evidence lane patch")
        if item["final_review_kind"] != "full" or type(item["done_verified"]) is not bool:
            raise ContractError("evidence lane review kind/done flag is invalid")
    integration = _exact(obj["integration"], EVIDENCE_INTEGRATION_KEYS, "evidence integration")
    for field in ("task_id", "workspace_id", "executor_agent_id", "final_review_dispatch_id"):
        _string(integration[field], f"evidence integration {field}")
    for field in ("combined_candidate_identity", "content_diff_identity"):
        _hex(integration[field], SHA256, f"evidence integration {field}")
    for field in ("content_diff_path", "final_review_record"):
        _relative_path(integration[field], f"evidence integration {field}")
    if integration["final_review_kind"] != "full" or type(integration["done_verified"]) is not bool:
        raise ContractError("evidence integration review kind/done flag is invalid")
    initial = _exact(integration["initial_git"], INITIAL_GIT_KEYS, "evidence initial_git")
    for field in INITIAL_GIT_KEYS:
        _hex(initial[field], OID, f"initial_git.{field}")
    if type(obj["collateral_empty"]) is not bool or obj["gates_result"] not in {"PASS", "FAIL"}:
        raise ContractError("evidence collateral/gates declaration is invalid")
    return obj


SCHEMA_VALIDATORS: dict[str, Callable[[object], dict[str, Any]]] = {
    "wave/1": _validate_wave,
    "merge-queue/1": _validate_merge,
    "conflict-preflight/1": _validate_preflight,
    "lane-workset/1": _validate_workset,
    "call-set/1": _validate_call_set,
    "runtime-key-set/1": _validate_runtime_set,
    "term-narrative-set/1": _validate_term_set,
    "collateral-authorization/1": _validate_collateral,
    "task-content-allowed-files/1": _validate_allowed,
    "integration-content-diff/1": _validate_content_diff,
    "wave-evidence/1": _validate_evidence,
    "target-patch/1": _validate_patch,
}


def validate_schema(value: object, schema_id: str | None = None) -> dict[str, Any]:
    """Validate one Phase 1 exact-key object; useful to fixture builders too."""
    if not isinstance(value, dict):
        raise ContractError("schema value must be an object")
    actual = value.get("schema_id")
    if schema_id is not None and actual != schema_id:
        raise ContractError(f"expected schema_id {schema_id!r}, found {actual!r}")
    validator = SCHEMA_VALIDATORS.get(actual) if isinstance(actual, str) else None
    if validator is None:
        raise ContractError(f"unsupported Phase 1 schema_id {actual!r}")
    return validator(value)


def canonical_identity(value: object, schema_id: str | None = None) -> str:
    validate_schema(value, schema_id)
    return canonical_sha256(value)


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"JSON object contains duplicate key {key!r}")
        result[key] = value
    return result


def _decode_json(raw: bytes, label: str) -> object:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InputError(f"{label} is not UTF-8: {error}") from error
    try:
        return json.loads(text, object_pairs_hook=_pairs_no_duplicates)
    except ContractError:
        raise
    except json.JSONDecodeError as error:
        raise InputError(f"{label} is not valid JSON: {error}") from error


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
        )
    except OSError as error:
        raise InputError(f"cannot run git: {error}") from error
    if check and result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ContractError(f"git {' '.join(args)} failed: {detail}")
    return result


def _repository_root(cwd: Path) -> Path:
    result = _git(cwd, "rev-parse", "--show-toplevel")
    try:
        return Path(result.stdout.decode("utf-8").strip()).resolve(strict=True)
    except (UnicodeDecodeError, OSError) as error:
        raise InputError(f"cannot resolve repository root: {error}") from error


class WaveContext:
    def __init__(
        self,
        wave_path: str | Path,
        workspace_roots: Mapping[str, str | Path] | None,
    ) -> None:
        raw_arg = str(wave_path)
        self.root = _repository_root(Path.cwd()).resolve(strict=True)
        self.wave_relative = _relative_path(raw_arg, "WAVE.json argument")
        wave_raw = self._read_at(self.root, self.wave_relative, "WAVE.json")
        wave_value = _decode_json(wave_raw, "WAVE.json")
        self.wave = validate_schema(wave_value, "wave/1")
        if wave_raw != canonical_bytes(self.wave):
            raise ContractError("WAVE.json bytes are not the canonical compact UTF-8 encoding")
        self.wave_raw = wave_raw
        expected = f".ai/waves/{self.wave['wave_id']}/WAVE.json"
        if self.wave_relative != expected:
            raise InputError(f"WAVE.json argument must be the canonical wave path {expected!r}")
        self.workspace_roots = self._resolve_workspace_roots(workspace_roots)
        self._locale_cache: dict[tuple[str, str, str], tuple[dict[str, Any], ...]] = {}

    @staticmethod
    def _git_common_dir(root: Path) -> Path:
        raw = _git(root, "rev-parse", "--git-common-dir").stdout
        try:
            value = raw.decode("utf-8").strip()
        except UnicodeDecodeError as error:
            raise InputError(f"git common-dir is not UTF-8: {error}") from error
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = root / candidate
        try:
            return candidate.resolve(strict=True)
        except OSError as error:
            raise InputError(f"cannot resolve git common-dir for {root}: {error}") from error

    def _resolve_workspace_roots(
        self, mapping: Mapping[str, str | Path] | None
    ) -> dict[str, Path]:
        if mapping is None:
            raise InputError("managed wave requires an explicit workspace_id=root mapping")
        expected_ids = {self.wave["root_workspace_id"]}
        expected_ids.update(lane["workspace_id"] for lane in self.wave["lanes"])
        integration_workspace = self.wave["integration"]["workspace_id"]
        if integration_workspace is not None:
            expected_ids.add(integration_workspace)
        if set(mapping) != expected_ids:
            missing = sorted(expected_ids - set(mapping))
            extra = sorted(set(mapping) - expected_ids)
            raise InputError(
                f"workspace root mapping must be 1:1 with WAVE workspace_ids; "
                f"missing={missing}, extra={extra}"
            )
        resolved: dict[str, Path] = {}
        seen_roots: dict[Path, str] = {}
        common_dir: Path | None = None
        for workspace_id, raw_root in mapping.items():
            if not isinstance(workspace_id, str) or not workspace_id:
                raise InputError("workspace root mapping has an invalid workspace_id")
            try:
                root = Path(raw_root).expanduser().resolve(strict=True)
            except (OSError, TypeError) as error:
                raise InputError(
                    f"workspace root for {workspace_id!r} is not an existing path: {error}"
                ) from error
            if not root.is_dir() or _repository_root(root) != root:
                raise InputError(f"workspace root for {workspace_id!r} is not a Git worktree root")
            previous = seen_roots.get(root)
            if previous is not None and previous != workspace_id:
                raise InputError(
                    f"workspace_ids {previous!r} and {workspace_id!r} resolve to the same root"
                )
            seen_roots[root] = workspace_id
            candidate_common = self._git_common_dir(root)
            if common_dir is None:
                common_dir = candidate_common
            elif candidate_common != common_dir:
                raise InputError("workspace root mapping crosses unrelated Git repositories")
            resolved[workspace_id] = root
        if resolved[self.wave["root_workspace_id"]] != self.root:
            raise InputError("root_workspace_id mapping does not resolve to the WAVE entry worktree")
        return resolved

    def root_for(self, workspace_id: str | None = None) -> Path:
        selected = self.wave["root_workspace_id"] if workspace_id is None else workspace_id
        try:
            return self.workspace_roots[selected]
        except KeyError as error:
            raise InputError(f"workspace_id {selected!r} has no trusted root mapping") from error

    @staticmethod
    def _path_at(
        root: Path, relative: str, label: str, *, must_exist: bool = True
    ) -> Path:
        relative = _relative_path(relative, label)
        candidate = root / PurePosixPath(relative)
        current = root
        for part in PurePosixPath(relative).parts:
            current = current / part
            if current.exists() or current.is_symlink():
                if current.is_symlink():
                    raise InputError(f"{label} traverses a symlink: {relative!r}")
        try:
            parent = candidate.parent.resolve(strict=True)
            parent.relative_to(root)
        except (OSError, ValueError) as error:
            raise InputError(f"{label} has no ordinary in-workspace parent: {relative!r}") from error
        if must_exist:
            try:
                resolved = candidate.resolve(strict=True)
                resolved.relative_to(root)
            except (OSError, ValueError) as error:
                raise InputError(f"{label} is not an existing workspace file: {relative!r}") from error
            if candidate.is_symlink() or not resolved.is_file():
                raise InputError(f"{label} must be an ordinary non-symlink file: {relative!r}")
            return resolved
        if candidate.exists() and (candidate.is_symlink() or not candidate.is_file()):
            raise InputError(f"{label} output is not an ordinary file: {relative!r}")
        return candidate

    @classmethod
    def _read_at(cls, root: Path, relative: str, label: str) -> bytes:
        path = cls._path_at(root, relative, label)
        try:
            return path.read_bytes()
        except OSError as error:
            raise InputError(f"cannot read {label}: {error}") from error

    def _path(
        self,
        relative: str,
        label: str,
        *,
        workspace_id: str | None = None,
        must_exist: bool = True,
    ) -> Path:
        return self._path_at(
            self.root_for(workspace_id), relative, label, must_exist=must_exist
        )

    def read_bytes(
        self, relative: str, label: str, *, workspace_id: str | None = None
    ) -> bytes:
        return self._read_at(self.root_for(workspace_id), relative, label)

    def read_schema(
        self,
        relative: str,
        schema_id: str,
        label: str,
        *,
        workspace_id: str | None = None,
    ) -> tuple[dict[str, Any], bytes]:
        raw = self.read_bytes(relative, label, workspace_id=workspace_id)
        value = _decode_json(raw, label)
        obj = validate_schema(value, schema_id)
        if raw != canonical_bytes(obj):
            raise ContractError(f"{label} bytes are not the canonical compact UTF-8 encoding")
        return obj, raw

    def read_json(
        self, relative: str, label: str, *, workspace_id: str | None = None
    ) -> dict[str, Any]:
        value = _decode_json(
            self.read_bytes(relative, label, workspace_id=workspace_id), label
        )
        if not isinstance(value, dict):
            raise ContractError(f"{label} must be a JSON object")
        return value

    def write_bytes_atomic(
        self,
        relative: str,
        raw: bytes,
        label: str,
        *,
        workspace_id: str | None = None,
    ) -> None:
        path = self._path(
            relative, label, workspace_id=workspace_id, must_exist=False
        )
        try:
            descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, path)
        except OSError as error:
            raise InputError(f"cannot write {label}: {error}") from error

    def write_canonical(
        self,
        relative: str,
        value: object,
        label: str,
        *,
        workspace_id: str | None = None,
    ) -> None:
        self.write_bytes_atomic(
            relative,
            canonical_bytes(value),
            label,
            workspace_id=workspace_id,
        )


def _ensure_git_object(ctx: WaveContext, commit: str) -> None:
    for workspace_id, root in ctx.workspace_roots.items():
        try:
            _git(root, "cat-file", "-e", f"{commit}^{{commit}}")
        except ContractError as error:
            raise ContractError(
                f"workspace {workspace_id!r} cannot resolve frozen base_commit: {error}"
            ) from error


def _git_blob(
    ctx: WaveContext,
    commit: str,
    relative: str,
    *,
    workspace_id: str | None = None,
) -> bytes:
    _relative_path(relative, "Git blob path")
    result = _git(ctx.root_for(workspace_id), "show", f"{commit}:{relative}")
    return result.stdout


def _worktree_bytes(
    ctx: WaveContext, relative: str, *, workspace_id: str | None = None
) -> bytes:
    return ctx.read_bytes(
        relative, f"worktree content {relative}", workspace_id=workspace_id
    )


def _tracked(
    ctx: WaveContext, relative: str, *, workspace_id: str | None = None
) -> bool:
    return (
        _git(
            ctx.root_for(workspace_id),
            "ls-files",
            "--error-unmatch",
            "--",
            relative,
            check=False,
        ).returncode
        == 0
    )


def _workspace_manifest(ctx: WaveContext, workspace_id: str):
    manifest_relative = f"i18n/versions/{DEFAULT_VERSION}.json"
    try:
        manifest = load_manifest(
            manifest_path=ctx.root_for(ctx.wave["root_workspace_id"])
            / manifest_relative
        )
    except ConfigurationError as error:
        raise InputError(f"cannot load pinned translation manifest: {error}") from error
    pinned_raw = _git_blob(
        ctx,
        ctx.wave["base_commit"],
        manifest_relative,
        workspace_id=ctx.wave["root_workspace_id"],
    )
    if manifest.raw_bytes != pinned_raw:
        raise ContractError("translation manifest differs from its pinned base_commit bytes")
    return replace(manifest, root=ctx.root_for(workspace_id))


def _manifest_component_for_section(manifest: Any, section: str) -> Any:
    matches = []
    for component in manifest.components:
        mounts = [source.mount for source in component.sources]
        if component.protected_source is not None:
            mounts.append(component.protected_source.mount)
        if any(section == mount or section.startswith(mount + "/") for mount in mounts):
            matches.append(component)
    if len(matches) != 1:
        raise ContractError(
            f"section {section!r} maps to {len(matches)} pinned manifest components"
        )
    return matches[0]


def _manifest_fixed_source_identity(
    ctx: WaveContext,
    worksets: list[dict[str, Any]],
    *,
    workspace_id: str,
) -> str:
    manifest = _workspace_manifest(ctx, workspace_id)
    identities: set[str] = set()
    for workset in worksets:
        for call in workset["calls"]:
            component = _manifest_component_for_section(manifest, call["section"])
            if component.source_repository is not None and component.sources:
                repository = manifest.repositories.get(component.source_repository)
                if repository is None:
                    raise ContractError(
                        f"component {component.id!r} has no pinned public repository"
                    )
                identity = f"commit:{repository.commit}"
            elif (
                component.protected_source is not None
                and component.source_baseline is not None
            ):
                identity = f"snapshot:{component.source_baseline.snapshot_sha256}"
            else:
                raise ContractError(
                    f"component {component.id!r} has no manifest-fixed source identity"
                )
            identities.add(identity)
    if len(identities) != 1:
        raise ContractError(
            "contextual candidate does not resolve to exactly one manifest-fixed source identity"
        )
    return next(iter(identities))


def _manifest_primary(
    ctx: WaveContext, workset: dict[str, Any], *, workspace_id: str
) -> list[str]:
    manifest = _workspace_manifest(ctx, workspace_id)
    located: set[str] = set()
    for call in workset["calls"]:
        section = call["section"]
        component = _manifest_component_for_section(manifest, section)
        translation = component.translation
        _relative_path(translation, "manifest component.translation")
        if not _tracked(ctx, translation, workspace_id=workspace_id):
            raise ContractError(f"pinned translation path {translation!r} is not tracked")
        ctx._path(
            translation,
            f"pinned translation path {translation}",
            workspace_id=workspace_id,
        )
        located.add(translation)
    return sorted(located, key=lambda item: item.encode("utf-8"))


def _locale_records(
    ctx: WaveContext,
    *,
    workspace_id: str,
    translation_path: str,
    revision: str,
) -> tuple[dict[str, Any], ...]:
    cache_key = (workspace_id, translation_path, revision)
    cached = ctx._locale_cache.get(cache_key)
    if cached is not None:
        return cached
    if revision == "base":
        raw = _git_blob(
            ctx,
            ctx.wave["base_commit"],
            translation_path,
            workspace_id=workspace_id,
        )
    elif revision == "current":
        raw = _worktree_bytes(ctx, translation_path, workspace_id=workspace_id)
    else:  # pragma: no cover - internal programming guard
        raise AssertionError(f"unknown locale revision {revision!r}")
    manifest = _workspace_manifest(ctx, workspace_id)
    try:
        document = LocaleLoader(LuaRuntime(manifest)).load_bytes(
            raw, logical_path=translation_path
        )
    except I18nToolError as error:
        raise ContractError(
            f"pinned Lua locale parser rejected {workspace_id}:{translation_path}:{revision}: {error}"
        ) from error
    records = tuple(
        record
        for record in document.translations
        if record.get("function_name") == "t"
    )
    ctx._locale_cache[cache_key] = records
    return records


def _record_call_identity(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record.get("section"),
        record.get("source"),
        record.get("source_tag"),
        canonical_bytes(record.get("args_order")),
        canonical_bytes(record.get("special")),
    )


def _workset_call_identity(call: dict[str, Any]) -> tuple[Any, ...]:
    return (
        call["section"],
        call["source"],
        call["source_tag"],
        canonical_bytes(call["args_order"]),
        canonical_bytes(call["special"]),
    )


@dataclass(frozen=True)
class ResolvedCall:
    revision_key: str
    source: str
    base_target: str
    current_target: str


def _resolve_workset_calls(
    ctx: WaveContext,
    workset: dict[str, Any],
    primary: list[str],
    *,
    workspace_id: str,
) -> tuple[ResolvedCall, ...]:
    if not workset["calls"]:
        raise ContractError("lane workset must not be empty")
    manifest = _workspace_manifest(ctx, workspace_id)
    by_component_path: dict[str, str] = {}
    for call in workset["calls"]:
        component = _manifest_component_for_section(manifest, call["section"])
        if component.translation not in primary:
            raise ContractError(
                f"workset revision {call['revision_key']!r} has no unique pinned translation path"
            )
        by_component_path[call["revision_key"]] = component.translation
    resolved: list[ResolvedCall] = []
    for call in workset["calls"]:
        translation_path = by_component_path[call["revision_key"]]
        expected = _workset_call_identity(call)
        targets: dict[str, str] = {}
        for revision in ("base", "current"):
            matches = [
                record
                for record in _locale_records(
                    ctx,
                    workspace_id=workspace_id,
                    translation_path=translation_path,
                    revision=revision,
                )
                if _record_call_identity(record) == expected
            ]
            if len(matches) != 1:
                raise ContractError(
                    f"workset revision {call['revision_key']!r} resolves to {len(matches)} "
                    f"pinned Lua calls in {revision} {translation_path}"
                )
            target = matches[0].get("target")
            if not isinstance(target, str):
                raise ContractError(
                    f"workset revision {call['revision_key']!r} has a non-string {revision} target"
                )
            targets[revision] = target
        resolved.append(
            ResolvedCall(
                revision_key=call["revision_key"],
                source=call["source"],
                base_target=targets["base"],
                current_target=targets["current"],
            )
        )
    return tuple(resolved)


@dataclass(frozen=True)
class LanePreflight:
    lane: dict[str, Any]
    workset: dict[str, Any]
    primary: list[str]
    scope: dict[str, Any]
    frozen_set: dict[str, Any]
    resolved_calls: tuple[ResolvedCall, ...]


@dataclass(frozen=True)
class PreflightBundle:
    merge: dict[str, Any]
    preflight: dict[str, Any]
    lanes: tuple[LanePreflight, ...]


def _merge_bound(ctx: WaveContext) -> tuple[dict[str, Any], bytes]:
    wave = ctx.wave
    merge, raw = ctx.read_schema(wave["merge_queue_path"], "merge-queue/1", "MERGE-QUEUE.json")
    if merge["wave_id"] != wave["wave_id"] or merge["base_commit"] != wave["base_commit"]:
        raise ContractError("MERGE-QUEUE wave_id/base_commit does not match WAVE")
    if merge["ordered_lane_ids"] != wave["ordered_lane_ids"] or len(merge["items"]) != len(wave["lanes"]):
        raise ContractError("MERGE-QUEUE lane order/length does not match WAVE")
    for lane, item in zip(wave["lanes"], merge["items"]):
        for field in ("lane_id", "task_id", "target_patch_path"):
            if item[field] != lane[field]:
                raise ContractError(f"MERGE-QUEUE {field} does not match WAVE lane")
    return merge, raw


def _lane_scope(
    ctx: WaveContext, lane: dict[str, Any], frozen: dict[str, Any], workset: dict[str, Any], primary: list[str]
) -> dict[str, Any]:
    collateral = frozen["collateral_authorization"]
    fields = ("lane_id", "task_id")
    if any(collateral[field] != lane[field] or collateral[field] != workset[field] for field in fields):
        raise ContractError("collateral authorization lane/task does not match WAVE workset")
    if collateral["spec_path"] != lane["spec_path"]:
        raise ContractError("collateral spec_path does not match WAVE lane")
    spec_raw = ctx.read_bytes(
        lane["spec_path"], "lane SPEC", workspace_id=lane["workspace_id"]
    )
    if hashlib.sha256(spec_raw).hexdigest() != collateral["spec_identity"]:
        raise ContractError("lane SPEC identity drift")
    try:
        spec_text = spec_raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InputError(f"lane SPEC is not UTF-8: {error}") from error
    if COLLATERAL_FORBIDDEN_MARKER not in spec_text.splitlines():
        raise ContractError(f"lane SPEC must contain the exact line {COLLATERAL_FORBIDDEN_MARKER!r}")
    if collateral["scope_path"] != f".ai/task/{lane['task_id']}/SCOPE.json":
        raise ContractError("lane scope_path is not task-derived")
    if collateral["allowed_files_path"] != collateral["scope_path"]:
        raise ContractError("Phase 1 allowed_files_path must equal scope_path")
    scope, raw = ctx.read_schema(
        collateral["scope_path"],
        "task-content-allowed-files/1",
        "lane SCOPE",
        workspace_id=lane["workspace_id"],
    )
    identity = hashlib.sha256(raw).hexdigest()
    if identity != collateral["scope_identity"] or identity != collateral["allowed_files_identity"]:
        raise ContractError("lane SCOPE/allowed-files identity drift")
    if collateral["scope_identity"] != collateral["allowed_files_identity"]:
        raise ContractError("lane scope and allowed-files identities differ")
    if scope["task_id"] != lane["task_id"] or scope["wave_id"] != ctx.wave["wave_id"]:
        raise ContractError("lane SCOPE task/wave does not match WAVE")
    if scope["wave_evidence_path"] is not None or ctx.wave["wave_evidence_path"] in scope["allowed_files"]:
        raise ContractError("lane SCOPE must not authorize wave evidence")
    if any(path.startswith(RUNTIME_PREFIXES) for path in scope["allowed_files"]):
        raise ContractError("lane task-content allowed_files contains an ignored runtime path")
    if workset["primary_content_paths"] != primary:
        raise ContractError("workset declared primary paths differ from pinned-manifest export")
    if scope["translation_fix_paths"] != primary:
        raise ContractError("lane translation_fix_paths differ from pinned-manifest export")
    if collateral["primary_content_paths"] != primary:
        raise ContractError("collateral primary paths differ from pinned-manifest export")
    if collateral["ordinary_non_collateral_paths"] != []:
        raise ContractError("Phase 1 ordinary_non_collateral_paths must be []")
    remainder = sorted(set(scope["allowed_files"]) - set(primary), key=lambda item: item.encode("utf-8"))
    if scope["allowed_files"] != primary or remainder or collateral["collateral_paths"] != remainder:
        raise ContractError("Phase 1 recomputed collateral is not empty")
    if lane["collateral_empty"] is not True:
        raise ContractError("WAVE lane collateral_empty must be literal true")
    return scope


def preflight_context(ctx: WaveContext) -> PreflightBundle:
    wave = ctx.wave
    _ensure_git_object(ctx, wave["base_commit"])
    merge, _ = _merge_bound(ctx)
    preflight, raw = ctx.read_schema(
        wave["conflict_preflight_path"], "conflict-preflight/1", "CONFLICT-PREFLIGHT.json"
    )
    identity = hashlib.sha256(raw).hexdigest()
    if wave["conflict_preflight_identity"] is None or identity != wave["conflict_preflight_identity"]:
        raise ContractError("CONFLICT-PREFLIGHT identity does not match WAVE")
    if preflight["wave_id"] != wave["wave_id"] or preflight["base_commit"] != wave["base_commit"]:
        raise ContractError("CONFLICT-PREFLIGHT wave/base does not match WAVE")
    if (
        preflight["ordered_lane_ids"] != wave["ordered_lane_ids"]
        or len(preflight["sets"]) != len(wave["lanes"])
    ):
        raise ContractError("CONFLICT-PREFLIGHT lane order/length does not match WAVE")
    lanes: list[LanePreflight] = []
    call_intersection_sets: list[set[tuple[bytes, ...]]] = []
    runtime_sets: list[set[tuple[str, str]]] = []
    term_sets: list[set[tuple[str, str]]] = []
    for lane, frozen in zip(wave["lanes"], preflight["sets"]):
        if frozen["lane_id"] != lane["lane_id"] or frozen["task_id"] != lane["task_id"]:
            raise ContractError("CONFLICT-PREFLIGHT set lane/task does not match WAVE")
        workset, workset_raw = ctx.read_schema(lane["workset_path"], "lane-workset/1", "lane workset")
        if lane["workset_identity"] is None or hashlib.sha256(workset_raw).hexdigest() != lane["workset_identity"]:
            raise ContractError("lane workset identity does not match WAVE")
        if workset["lane_id"] != lane["lane_id"] or workset["task_id"] != lane["task_id"]:
            raise ContractError("lane workset task/lane does not match WAVE")
        call_set = frozen["call_set"]
        runtime_set = frozen["runtime_key_set"]
        term_set = frozen["term_narrative_set"]
        collateral = frozen["collateral_authorization"]
        for artifact, field in (
            (call_set, "call_set_identity"), (runtime_set, "runtime_key_set_identity"),
            (term_set, "term_narrative_set_identity"), (collateral, "collateral_authorization_identity"),
        ):
            if canonical_sha256(artifact) != frozen[field]:
                raise ContractError(f"embedded {field} drift")
            if artifact["lane_id"] != lane["lane_id"] or artifact["task_id"] != lane["task_id"]:
                raise ContractError(f"embedded {field} task/lane mismatch")
        if call_set["items"] != workset["calls"]:
            raise ContractError("call-set items differ from WAVE-bound workset calls")
        primary = _manifest_primary(
            ctx, workset, workspace_id=lane["workspace_id"]
        )
        scope = _lane_scope(ctx, lane, frozen, workset, primary)
        resolved_calls = _resolve_workset_calls(
            ctx,
            workset,
            primary,
            workspace_id=lane["workspace_id"],
        )
        expected_runtime = [
            {"runtime_key": runtime_key, "source_tag": source_tag}
            for runtime_key, source_tag in sorted(
                {(call["source"], call["source_tag"]) for call in workset["calls"]},
                key=lambda item: (item[0].encode("utf-8"), item[1].encode("utf-8")),
            )
        ]
        if runtime_set["items"] != expected_runtime:
            raise ContractError(
                "runtime-key-set items are not the independently reconstructed workset runtime keys"
            )
        expected_terms = [
            {"kind": "narrative_closure", "key": revision_key}
            for revision_key in sorted(
                workset["ordered_revision_keys"], key=lambda item: item.encode("utf-8")
            )
        ]
        if term_set["items"] != expected_terms:
            raise ContractError(
                "term-narrative-set items are not the independently reconstructed workset dependencies"
            )
        call_intersection_sets.append({
            (item["section"].encode(), item["source"].encode(), item["source_tag"].encode(),
             canonical_bytes(item["args_order"]), canonical_bytes(item["special"]))
            for item in call_set["items"]
        })
        runtime_sets.append({(item["runtime_key"], item["source_tag"]) for item in runtime_set["items"]})
        term_sets.append({(item["kind"], item["key"]) for item in term_set["items"]})
        lanes.append(
            LanePreflight(
                lane, workset, primary, scope, frozen, resolved_calls
            )
        )
    intersections_empty = all(
        not left.intersection(right)
        for collections in (call_intersection_sets, runtime_sets, term_sets)
        for left, right in itertools.combinations(collections, 2)
    )
    if not intersections_empty:
        raise ContractError("recomputed Phase 1 call/runtime/term sets intersect")
    if preflight["pairwise_intersections_empty"] is not True or preflight["result"] != "PASS":
        raise ContractError("CONFLICT-PREFLIGHT declarations do not match recomputed PASS")
    return PreflightBundle(merge, preflight, tuple(lanes))


def _state_done(ctx: WaveContext, lane_or_integration: dict[str, Any]) -> dict[str, Any]:
    workspace_id = lane_or_integration["workspace_id"]
    path = ctx._path(
        lane_or_integration["state_path"],
        "wave-bound STATE",
        workspace_id=workspace_id,
    )
    result = ai_state_check.check_wave_state_context(
        path,
        task_id=lane_or_integration["task_id"],
        workspace_id=workspace_id,
        orchestrator_agent_id=ctx.wave["orchestrator_agent_id"],
        workspace_root=ctx.root_for(workspace_id),
    )
    if result.exit_code:
        if result.exit_code == 2:
            raise InputError(f"STATE checker: {result.outcome}: {result.detail}")
        raise ContractError(f"STATE checker: {result.outcome}: {result.detail}")
    return ctx.read_json(
        lane_or_integration["state_path"],
        "wave-bound STATE",
        workspace_id=workspace_id,
    )


def _contextual_envelope(
    ctx: WaveContext,
    owner: dict[str, Any],
    state: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if owner["final_review_kind"] != "full":
        raise ContractError("final review kind must be full")
    workspace_id = owner["workspace_id"]
    record_path = owner["final_review_record"]
    if not isinstance(record_path, str):
        raise ContractError("final_review_record is not bound")
    identity = owner.get("final_candidate_identity", owner.get("combined_candidate_identity"))
    record_paths: list[str] = []
    for field in ("review_records", "senior_review_records"):
        paths = state.get(field)
        if not isinstance(paths, list) or any(
            not isinstance(path, str) for path in paths
        ):
            raise ContractError(f"wave-bound STATE {field} must be a path array")
        record_paths.extend(paths)
    if len(record_paths) != len(set(record_paths)):
        raise ContractError(
            "wave-bound STATE full-completion record paths must be unique across review arrays"
        )
    dispatches = state.get("child_dispatches")
    if not isinstance(dispatches, list):
        raise ContractError("wave-bound STATE child_dispatches must be an array")
    completions: list[tuple[str, dict[str, Any], dict[str, Any] | None]] = []
    for path in record_paths:
        candidate = ctx.read_json(
            path, "STATE review record", workspace_id=workspace_id
        )
        dispatch = next(
            (
                item
                for item in dispatches
                if isinstance(item, dict)
                and item.get("dispatch_id") == candidate.get("dispatch_id")
            ),
            None,
        )
        completion_fields = [
            candidate[field] for field in ("status", "result") if field in candidate
        ]
        terminal = bool(completion_fields) and all(
            isinstance(value, str) and value in ai_state_check.COMPLETION_VALUES
            for value in completion_fields
        )
        if (
            candidate.get("task_id") == owner["task_id"]
            and candidate.get("review_contract") == "translation_contextual_v1"
            and candidate.get("review_phase") in FULL_REVIEW_PHASES
            and candidate.get("review_kind") == "full"
            and type(candidate.get("cycle")) is int
            and type(candidate.get("attempt")) is int
            and terminal
        ):
            completions.append((path, candidate, dispatch))
    if not completions:
        raise ContractError(
            "WAVE final_review_record has no STATE full completion record"
        )
    latest_key = max(
        (candidate["cycle"], candidate["attempt"])
        for _, candidate, _ in completions
    )
    latest = [
        item
        for item in completions
        if (item[1]["cycle"], item[1]["attempt"]) == latest_key
    ]
    if len(latest) != 1:
        raise ContractError(
            "STATE latest full completion at maximum (cycle, attempt) is ambiguous"
        )
    latest_path, record, dispatch = latest[0]
    if latest_path != record_path:
        raise ContractError(
            "WAVE final_review_record is not the latest STATE full completion record"
        )
    if (
        record.get("dispatch_id") != owner["final_review_dispatch_id"]
        or record.get("candidate_identity") != identity
        or record.get("result") not in {"PASS", "OK", "completed"}
        or not isinstance(dispatch, dict)
        or record.get("agent_id") != dispatch.get("agent_id")
        or dispatch.get("task_id") != owner["task_id"]
        or dispatch.get("workspace_id") != workspace_id
        or dispatch.get("parent_agent_id") != ctx.wave["orchestrator_agent_id"]
        or dispatch.get("purpose") != "translation_contextual_v1"
        or str(dispatch.get("role", "")).upper() != "REVIEWER"
        or dispatch.get("lifecycle", dispatch.get("status")) != "archived"
        or dispatch.get("archive_confirmed") is not True
    ):
        raise ContractError(
            "WAVE final review is not bound to the latest passing STATE completion dispatch"
        )
    input_path = record.get("input_path")
    if not isinstance(input_path, str):
        raise ContractError("final review record lacks input_path")
    if dispatch.get("candidate_identity") != identity or dispatch.get("input_path") != input_path:
        raise ContractError("final review dispatch candidate/input binding drift")
    envelope = ctx.read_json(
        input_path, "final contextual envelope", workspace_id=workspace_id
    )
    _exact(envelope, frozenset({"candidate_identity", "payload"}), "contextual envelope")
    _hex(envelope["candidate_identity"], SHA256, "contextual candidate_identity")
    payload = _exact(envelope["payload"], CONTEXTUAL_PAYLOAD_KEYS, "contextual payload")
    if payload["contract"] != "translation_contextual_v1":
        raise ContractError("contextual payload contract is not v1")
    keys = _string_array(payload["ordered_revision_keys"], "contextual ordered_revision_keys")
    if not isinstance(payload["translation_snapshot"], list) or not isinstance(payload["bounded_context"], list):
        raise ContractError("contextual snapshot/context must be arrays")
    snapshot_keys: list[str] = []
    for index, item in enumerate(payload["translation_snapshot"]):
        item = _exact(item, frozenset({"revision_key", "source", "target"}), f"translation_snapshot[{index}]")
        snapshot_keys.append(_string(item["revision_key"], "snapshot revision_key"))
        _json_string(item["source"], "snapshot source")
        _json_string(item["target"], "snapshot target")
    context_keys: list[str] = []
    for index, item in enumerate(payload["bounded_context"]):
        item = _exact(item, frozenset({"revision_key", "context"}), f"bounded_context[{index}]")
        context_keys.append(_string(item["revision_key"], "context revision_key"))
        if not isinstance(item["context"], str):
            raise ContractError("bounded context must be a string")
    if snapshot_keys != keys or context_keys != keys:
        raise ContractError("contextual arrays do not match ordered_revision_keys")
    for field in ("fixed_source_identity", "terminology_snapshot", "rendered_briefing"):
        if not isinstance(payload[field], str):
            raise ContractError(f"contextual payload {field} must be a string")
    recomputed = canonical_sha256(payload)
    if envelope["candidate_identity"] != recomputed or identity != recomputed:
        raise ContractError("contextual candidate identity drift")
    return record, envelope


def _lane_by_id(ctx: WaveContext, lane_id: str) -> tuple[dict[str, Any], int]:
    for index, lane in enumerate(ctx.wave["lanes"]):
        if lane["lane_id"] == lane_id:
            return lane, index
    raise InputError(f"lane_id {lane_id!r} is not bound by WAVE")


def _require_wave_state(ctx: WaveContext, *states: str) -> None:
    if ctx.wave["state"] not in states:
        expected = "/".join(states)
        raise ContractError(
            f"operation requires a legal WAVE.state={expected}, found {ctx.wave['state']}"
        )


def _lane_empty_candidate(
    ctx: WaveContext, lane_data: LanePreflight
) -> tuple[dict[str, Any], dict[str, Any]]:
    lane = lane_data.lane
    state = _state_done(ctx, lane)
    _, envelope = _contextual_envelope(ctx, lane, state)
    payload = envelope["payload"]
    expected_source_identity = _manifest_fixed_source_identity(
        ctx,
        [lane_data.workset],
        workspace_id=lane["workspace_id"],
    )
    if payload["fixed_source_identity"] != expected_source_identity:
        raise ContractError(
            "lane fixed_source_identity does not match its pinned manifest source"
        )
    for path in lane_data.scope["translation_fix_paths"]:
        if _worktree_bytes(ctx, path, workspace_id=lane["workspace_id"]) != _git_blob(
            ctx,
            ctx.wave["base_commit"],
            path,
            workspace_id=lane["workspace_id"],
        ):
            raise ContractError(
                f"lane no-change translation path differs bytewise from base_commit: {path!r}"
            )
    if payload["ordered_revision_keys"] != lane_data.workset["ordered_revision_keys"]:
        raise ContractError("final candidate revision order differs from lane workset")
    snapshots = payload["translation_snapshot"]
    if len(snapshots) != len(lane_data.resolved_calls):
        raise ContractError("final candidate snapshot length differs from lane workset")
    for snapshot, resolved in zip(snapshots, lane_data.resolved_calls):
        if (
            snapshot["revision_key"] != resolved.revision_key
            or snapshot["source"] != resolved.source
        ):
            raise ContractError(
                f"final candidate call identity drift at revision {resolved.revision_key!r}"
            )
        if not (
            snapshot["target"] == resolved.base_target == resolved.current_target
        ):
            raise ContractError(
                f"empty TARGET-PATCH would discard target drift at revision {resolved.revision_key!r}"
            )
    return state, envelope


def export_target_patch_context(ctx: WaveContext, lane_id: str) -> str:
    _require_wave_state(ctx, "LANES_READY")
    bundle = preflight_context(ctx)
    lane, index = _lane_by_id(ctx, lane_id)
    lane_data = bundle.lanes[index]
    _lane_empty_candidate(ctx, lane_data)
    patch = {
        "schema_id": "target-patch/1",
        "schema_version": 1,
        "base_commit": ctx.wave["base_commit"],
        "task_id": lane["task_id"],
        "candidate_identity": lane["final_candidate_identity"],
        "ordered_revision_keys": list(lane_data.workset["ordered_revision_keys"]),
        "changes": [],
    }
    validate_schema(patch, "target-patch/1")
    identity = canonical_sha256(patch)
    bound = lane["target_patch_identity"]
    merge_bound = bundle.merge["items"][index]["target_patch_identity"]
    if bound is not None and bound != identity:
        raise ContractError("exported empty patch identity differs from WAVE binding")
    if merge_bound is not None and merge_bound != identity:
        raise ContractError("exported empty patch identity differs from MERGE-QUEUE binding")
    ctx.write_canonical(
        lane["target_patch_path"],
        patch,
        "TARGET-PATCH output",
        workspace_id=lane["workspace_id"],
    )
    return identity


def _verify_lane_patch(
    ctx: WaveContext, bundle: PreflightBundle, lane_id: str
) -> str:
    lane, index = _lane_by_id(ctx, lane_id)
    lane_data = bundle.lanes[index]
    _lane_empty_candidate(ctx, lane_data)
    patch, raw = ctx.read_schema(
        lane["target_patch_path"],
        "target-patch/1",
        "TARGET-PATCH",
        workspace_id=lane["workspace_id"],
    )
    identity = hashlib.sha256(raw).hexdigest()
    merge_item = bundle.merge["items"][index]
    expected = {
        "base_commit": ctx.wave["base_commit"],
        "task_id": lane["task_id"],
        "candidate_identity": lane["final_candidate_identity"],
        "ordered_revision_keys": lane_data.workset["ordered_revision_keys"],
    }
    for field, value in expected.items():
        if patch[field] != value:
            raise ContractError(f"TARGET-PATCH {field} does not match WAVE-bound input")
    if lane["target_patch_identity"] != identity or merge_item["target_patch_identity"] != identity:
        raise ContractError("TARGET-PATCH identity does not match WAVE/MERGE-QUEUE")
    if merge_item["candidate_identity"] != lane["final_candidate_identity"]:
        raise ContractError("MERGE-QUEUE candidate identity does not match WAVE lane")
    if patch["changes"]:
        raise ContractError("Phase 1 does not support non-empty TARGET-PATCH apply; fail closed")
    return identity


def verify_target_patch_context(ctx: WaveContext, lane_id: str) -> str:
    _require_wave_state(ctx, "INTEGRATING")
    bundle = preflight_context(ctx)
    return _verify_lane_patch(ctx, bundle, lane_id)


def _clean_base_tree(ctx: WaveContext) -> dict[str, str]:
    base = ctx.wave["base_commit"]
    integration_workspace = ctx.wave["integration"]["workspace_id"]
    if not isinstance(integration_workspace, str):
        raise ContractError("integration workspace is not bound")
    root = ctx.root_for(integration_workspace)
    head = _git(root, "rev-parse", "HEAD").stdout.decode().strip()
    base_tree = _git(root, "rev-parse", f"{base}^{{tree}}").stdout.decode().strip()
    index_tree = _git(root, "write-tree").stdout.decode().strip()
    if head != base or index_tree != base_tree:
        raise ContractError("initial apply requires HEAD=base_commit and index_tree=base_commit^{tree}")
    if _git(root, "diff-files", "--quiet", check=False).returncode != 0:
        raise ContractError("initial apply requires tracked worktree content equal to the index tree")
    status = _git(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignored=no",
    ).stdout
    for record in status.split(b"\0"):
        if not record:
            continue
        try:
            path = record[3:].decode("utf-8")
        except UnicodeDecodeError as error:
            raise InputError(f"git status path is not UTF-8: {error}") from error
        if not path.startswith(RUNTIME_PREFIXES):
            raise ContractError(f"initial apply has unauthorized dirty/untracked path {path!r}")
    return {"head_commit": head, "index_tree": index_tree, "worktree_tree": base_tree}


def apply_target_patches_context(ctx: WaveContext) -> dict[str, str]:
    _require_wave_state(ctx, "INTEGRATING")
    bundle = preflight_context(ctx)
    _integration_apply_provenance(ctx, bundle)
    initial = _clean_base_tree(ctx)
    for lane_id in bundle.merge["ordered_lane_ids"]:
        _verify_lane_patch(ctx, bundle, lane_id)
    return initial


def _integration_scope(
    ctx: WaveContext,
    bundle: PreflightBundle,
    *,
    require_content_diff: bool = True,
) -> tuple[dict[str, Any], bytes, list[str]]:
    integration = ctx.wave["integration"]
    task_id = integration["task_id"]
    if not isinstance(task_id, str):
        raise ContractError("integration task is not bound")
    formulas = {
        "state_path": f".ai/task/{task_id}/STATE.json",
        "spec_path": f".ai/task/{task_id}/SPEC.md",
        "allowed_files_path": f".ai/task/{task_id}/SCOPE.json",
    }
    if require_content_diff:
        formulas["content_diff_path"] = (
            f".ai/task/{task_id}/INTEGRATION-CONTENT-DIFF.json"
        )
    for field, expected in formulas.items():
        if integration[field] != expected:
            raise ContractError(f"integration {field} is not task-derived")
    workspace_id = integration["workspace_id"]
    if not isinstance(workspace_id, str):
        raise ContractError("integration workspace is not bound")
    scope, raw = ctx.read_schema(
        integration["allowed_files_path"],
        "task-content-allowed-files/1",
        "integration SCOPE",
        workspace_id=workspace_id,
    )
    if hashlib.sha256(raw).hexdigest() != integration["allowed_files_identity"]:
        raise ContractError("integration allowed-files identity drift")
    primary = sorted({path for lane in bundle.lanes for path in lane.primary}, key=lambda item: item.encode("utf-8"))
    evidence = ctx.wave["wave_evidence_path"]
    allowed = sorted({*primary, evidence}, key=lambda item: item.encode("utf-8"))
    if scope["task_id"] != task_id or scope["wave_id"] != ctx.wave["wave_id"]:
        raise ContractError("integration SCOPE task/wave mismatch")
    if scope["translation_fix_paths"] != primary or scope["wave_evidence_path"] != evidence or scope["allowed_files"] != allowed:
        raise ContractError("integration SCOPE is not the exact translation/evidence union")
    spec_raw = ctx.read_bytes(
        integration["spec_path"], "integration SPEC", workspace_id=workspace_id
    )
    try:
        spec_text = spec_raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InputError(f"integration SPEC is not UTF-8: {error}") from error
    if evidence not in spec_text:
        raise ContractError("integration SPEC does not name the unique wave evidence path")
    return scope, raw, primary


def _integration_apply_provenance(
    ctx: WaveContext, bundle: PreflightBundle
) -> dict[str, Any]:
    integration = ctx.wave["integration"]
    _integration_scope(ctx, bundle, require_content_diff=False)
    workspace_id = integration["workspace_id"]
    if not isinstance(workspace_id, str):
        raise ContractError("integration workspace is not bound")
    state = ctx.read_json(
        integration["state_path"],
        "integration STATE before apply",
        workspace_id=workspace_id,
    )
    if (
        state.get("task_id") != integration["task_id"]
        or state.get("workspace_id") != workspace_id
        or state.get("orchestrator_agent_id") != ctx.wave["orchestrator_agent_id"]
    ):
        raise ContractError(
            "integration STATE task/workspace/orchestrator does not match WAVE"
        )
    dispatches = state.get("child_dispatches")
    if not isinstance(dispatches, list):
        raise ContractError("integration STATE child_dispatches must be an array")
    orchestrator = ctx.wave["orchestrator_agent_id"]
    for index, dispatch in enumerate(dispatches):
        if not isinstance(dispatch, dict):
            raise ContractError(
                f"integration child_dispatches[{index}] must be an object"
            )
        if dispatch.get("agent_id") == orchestrator:
            raise ContractError(
                "integration child agent_id must differ from orchestrator_agent_id"
            )
    matches = [
        dispatch
        for dispatch in dispatches
        if str(dispatch.get("role", "")).upper() == "EXECUTOR"
        and dispatch.get("purpose") == "integration_apply"
        and dispatch.get("task_id") == integration["task_id"]
        and dispatch.get("workspace_id") == workspace_id
        and dispatch.get("parent_agent_id") == orchestrator
        and dispatch.get("lineage_verified") is True
        and isinstance(dispatch.get("agent_id"), str)
        and bool(dispatch.get("agent_id"))
        and (
            dispatch.get("lifecycle", dispatch.get("status")) == "active"
            or (
                dispatch.get("lifecycle", dispatch.get("status")) == "archived"
                and dispatch.get("archive_confirmed") is True
            )
        )
    ]
    if len(matches) != 1:
        raise ContractError(
            "apply requires exactly one provenance-bound integration EXECUTOR dispatch"
        )
    caller_agent_id = os.environ.get("PASEO_AGENT_ID")
    if not caller_agent_id or caller_agent_id != matches[0]["agent_id"]:
        raise ContractError(
            "apply requires PASEO_AGENT_ID to equal the unique integration_apply EXECUTOR"
        )
    return state


def _render_integration_terminology_snapshot(
    lane_payloads: list[tuple[str, dict[str, Any]]],
) -> str:
    frozen = {
        "schema_id": "phase1-integration-terminology-snapshot/1",
        "lanes": [
            {
                "lane_id": lane_id,
                "terminology_snapshot": payload["terminology_snapshot"],
            }
            for lane_id, payload in lane_payloads
        ],
    }
    return canonical_bytes(frozen).decode("utf-8")


def _render_integration_briefing(
    *,
    lane_payloads: list[tuple[str, dict[str, Any]]],
    ordered_revision_keys: list[str],
    translation_snapshot: list[dict[str, str]],
    fixed_source_identity: str,
    terminology_snapshot: str,
    bounded_context: list[dict[str, str]],
) -> str:
    frozen = {
        "schema_id": "phase1-integration-contextual-briefing/1",
        "ordered_lane_ids": [lane_id for lane_id, _ in lane_payloads],
        "ordered_revision_keys": ordered_revision_keys,
        "translation_snapshot": translation_snapshot,
        "fixed_source_identity": fixed_source_identity,
        "terminology_snapshot": terminology_snapshot,
        "bounded_context": bounded_context,
        "lane_briefings": [
            {
                "lane_id": lane_id,
                "rendered_briefing": payload["rendered_briefing"],
            }
            for lane_id, payload in lane_payloads
        ],
    }
    return canonical_bytes(frozen).decode("utf-8")


def _integration_combined_candidate(
    ctx: WaveContext, bundle: PreflightBundle
) -> tuple[dict[str, Any], dict[str, Any]]:
    integration = ctx.wave["integration"]
    state = _state_done(ctx, integration)
    _, envelope = _contextual_envelope(ctx, integration, state)
    expected_keys: list[str] = []
    expected_snapshots: list[dict[str, str]] = []
    expected_contexts: list[dict[str, str]] = []
    lane_payloads: list[tuple[str, dict[str, Any]]] = []
    integration_workspace = integration["workspace_id"]
    if not isinstance(integration_workspace, str):
        raise ContractError("integration workspace is not bound")
    for lane_id in bundle.merge["ordered_lane_ids"]:
        lane, index = _lane_by_id(ctx, lane_id)
        lane_data = bundle.lanes[index]
        _, lane_envelope = _lane_empty_candidate(ctx, lane_data)
        lane_payload = lane_envelope["payload"]
        lane_payloads.append((lane_id, lane_payload))
        expected_contexts.extend(copy.deepcopy(lane_payload["bounded_context"]))
        integration_resolved = _resolve_workset_calls(
            ctx,
            lane_data.workset,
            lane_data.primary,
            workspace_id=integration_workspace,
        )
        for lane_snapshot, resolved in zip(
            lane_envelope["payload"]["translation_snapshot"], integration_resolved
        ):
            if (
                lane_snapshot["revision_key"] != resolved.revision_key
                or lane_snapshot["source"] != resolved.source
                or lane_snapshot["target"] != resolved.current_target
            ):
                raise ContractError(
                    f"integration current call drift at revision {resolved.revision_key!r}"
                )
            expected_keys.append(resolved.revision_key)
            expected_snapshots.append(
                {
                    "revision_key": resolved.revision_key,
                    "source": resolved.source,
                    "target": resolved.current_target,
                }
            )
    payload = envelope["payload"]
    if payload["ordered_revision_keys"] != expected_keys:
        raise ContractError(
            "integration envelope does not preserve the exact MERGE-QUEUE key order"
        )
    if payload["translation_snapshot"] != expected_snapshots:
        raise ContractError(
            "integration envelope source/target snapshot is not the exact lane union"
        )
    if payload["bounded_context"] != expected_contexts:
        raise ContractError(
            "integration bounded_context is not the exact MERGE-QUEUE lane-context union"
        )
    expected_source_identity = _manifest_fixed_source_identity(
        ctx,
        [lane_data.workset for lane_data in bundle.lanes],
        workspace_id=integration_workspace,
    )
    if payload["fixed_source_identity"] != expected_source_identity:
        raise ContractError(
            "integration fixed_source_identity does not match the pinned manifest source"
        )
    expected_terminology = _render_integration_terminology_snapshot(lane_payloads)
    if payload["terminology_snapshot"] != expected_terminology:
        raise ContractError(
            "integration terminology_snapshot is not the deterministic lane-input render"
        )
    expected_briefing = _render_integration_briefing(
        lane_payloads=lane_payloads,
        ordered_revision_keys=expected_keys,
        translation_snapshot=expected_snapshots,
        fixed_source_identity=expected_source_identity,
        terminology_snapshot=expected_terminology,
        bounded_context=expected_contexts,
    )
    if payload["rendered_briefing"] != expected_briefing:
        raise ContractError(
            "integration rendered_briefing is not the deterministic merged-candidate render"
        )
    return state, envelope


def verify_content_diff_context(ctx: WaveContext) -> str:
    _require_wave_state(ctx, "GATED", "DONE")
    bundle = preflight_context(ctx)
    _integration_combined_candidate(ctx, bundle)
    scope, _, primary = _integration_scope(ctx, bundle)
    integration = ctx.wave["integration"]
    artifact, raw = ctx.read_schema(
        integration["content_diff_path"],
        "integration-content-diff/1",
        "INTEGRATION-CONTENT-DIFF",
        workspace_id=integration["workspace_id"],
    )
    identity = hashlib.sha256(raw).hexdigest()
    if identity != integration["content_diff_identity"]:
        raise ContractError("integration content-diff identity does not match WAVE")
    if artifact["wave_id"] != ctx.wave["wave_id"] or artifact["task_id"] != integration["task_id"] or artifact["base_commit"] != ctx.wave["base_commit"]:
        raise ContractError("integration content-diff wave/task/base mismatch")
    if artifact["translation_paths"] != primary or artifact["translation_paths"] != scope["translation_fix_paths"]:
        raise ContractError("content-diff translation_paths do not match integration FIX scope")
    for path in primary:
        if _worktree_bytes(
            ctx, path, workspace_id=integration["workspace_id"]
        ) != _git_blob(
            ctx,
            ctx.wave["base_commit"],
            path,
            workspace_id=integration["workspace_id"],
        ):
            raise ContractError(
                f"integration no-change translation path differs bytewise from base_commit: {path!r}"
            )
    if artifact["changed_paths"] != [] or artifact["entries"] != []:
        raise ContractError(
            "Phase 1 integration content-diff changed_paths and entries must be empty"
        )
    return identity


def _changed_content_paths(ctx: WaveContext) -> set[str]:
    base = ctx.wave["base_commit"]
    workspace_id = ctx.wave["integration"]["workspace_id"]
    if not isinstance(workspace_id, str):
        raise ContractError("integration workspace is not bound")
    root = ctx.root_for(workspace_id)
    tracked = _git(root, "diff", "--name-only", "-z", base, "--").stdout
    untracked = _git(root, "ls-files", "--others", "--exclude-standard", "-z").stdout
    result: set[str] = set()
    for raw in tracked.split(b"\0") + untracked.split(b"\0"):
        if not raw:
            continue
        try:
            value = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise InputError(f"changed path is not UTF-8: {error}") from error
        relative = _relative_path(value, "changed content path")
        if relative.startswith(RUNTIME_PREFIXES):
            continue
        result.add(relative)
    return result


def _prospective_path(ctx: WaveContext) -> str:
    return f".ai/waves/{ctx.wave['wave_id']}/WAVE.DONE.prospective.json"


def _expected_prospective(ctx: WaveContext) -> tuple[dict[str, Any], bytes]:
    if ctx.wave["state"] not in {"GATED", "DONE"}:
        raise ContractError("prospective publication requires WAVE.state=GATED or DONE")
    value = copy.deepcopy(ctx.wave)
    value["state"] = "DONE"
    validate_schema(value, "wave/1")
    return value, canonical_bytes(value)


def _read_or_freeze_prospective(ctx: WaveContext) -> tuple[dict[str, Any], bytes]:
    expected, expected_raw = _expected_prospective(ctx)
    path = _prospective_path(ctx)
    candidate = ctx._path(path, "prospective DONE WAVE", must_exist=False)
    if not candidate.exists():
        if ctx.wave["state"] == "DONE":
            raise InputError("published WAVE is missing its frozen prospective bytes")
        ctx.write_bytes_atomic(path, expected_raw, "prospective DONE WAVE")
        return expected, expected_raw
    raw = ctx.read_bytes(path, "prospective DONE WAVE")
    value = validate_schema(_decode_json(raw, "prospective DONE WAVE"), "wave/1")
    if raw != canonical_bytes(value):
        raise ContractError("prospective DONE WAVE is not canonical")
    if raw != expected_raw:
        raise ContractError("prospective DONE WAVE identity/bytes differ from GATED bindings")
    return value, raw


@dataclass(frozen=True)
class FinalBindings:
    bundle: PreflightBundle
    integration_state: dict[str, Any]
    content_identity: str
    lane_states: tuple[dict[str, Any], ...]
    patch_identities: tuple[str, ...]


def _final_bindings(ctx: WaveContext) -> FinalBindings:
    _require_wave_state(ctx, "GATED", "DONE")
    bundle = preflight_context(ctx)
    lane_states: list[dict[str, Any]] = []
    patch_identities: list[str] = []
    for lane_data in bundle.lanes:
        state, _ = _lane_empty_candidate(ctx, lane_data)
        lane_states.append(state)
        patch_identities.append(
            _verify_lane_patch(ctx, bundle, lane_data.lane["lane_id"])
        )
    integration_state, _ = _integration_combined_candidate(ctx, bundle)
    content_identity = verify_content_diff_context(ctx)
    return FinalBindings(
        bundle,
        integration_state,
        content_identity,
        tuple(lane_states),
        tuple(patch_identities),
    )


def prepare_publication_context(ctx: WaveContext) -> str:
    _require_wave_state(ctx, "GATED", "DONE")
    _final_bindings(ctx)
    _, raw = _read_or_freeze_prospective(ctx)
    if ctx.wave["state"] == "DONE" and raw != ctx.wave_raw:
        raise ContractError("published WAVE bytes are not byte-identical to prospective DONE WAVE")
    return hashlib.sha256(raw).hexdigest()


def _evidence_bindings(
    ctx: WaveContext,
    prospective_raw: bytes,
    final: FinalBindings,
) -> tuple[dict[str, Any], bytes]:
    integration = ctx.wave["integration"]
    integration_workspace = integration["workspace_id"]
    evidence, evidence_raw = ctx.read_schema(
        ctx.wave["wave_evidence_path"],
        "wave-evidence/1",
        "wave evidence",
        workspace_id=integration_workspace,
    )
    merge_raw = ctx.read_bytes(ctx.wave["merge_queue_path"], "MERGE-QUEUE.json")
    if (
        evidence["wave_record_identity"] != hashlib.sha256(prospective_raw).hexdigest()
        or evidence["merge_queue_identity"] != hashlib.sha256(merge_raw).hexdigest()
    ):
        raise ContractError("wave evidence prospective/merge identities do not match frozen bytes")
    for field in ("wave_id", "base_commit", "orchestrator_agent_id"):
        if evidence[field] != ctx.wave[field]:
            raise ContractError(f"wave evidence {field} does not match WAVE")
    if (
        evidence["conflict_preflight_path"] != ctx.wave["conflict_preflight_path"]
        or evidence["conflict_preflight_identity"]
        != ctx.wave["conflict_preflight_identity"]
    ):
        raise ContractError("wave evidence preflight binding does not match WAVE")
    if len(evidence["lanes"]) != len(final.bundle.lanes):
        raise ContractError("wave evidence lane cardinality must match WAVE")
    all_agent_ids: set[str] = set()
    lane_candidates: set[str] = set()
    patch_identities = set(final.patch_identities)
    for index, (lane_data, state, patch_identity, evidence_lane) in enumerate(
        zip(
            final.bundle.lanes,
            final.lane_states,
            final.patch_identities,
            evidence["lanes"],
        )
    ):
        lane = lane_data.lane
        expected = {
            "lane_id": lane["lane_id"],
            "task_id": lane["task_id"],
            "workspace_id": lane["workspace_id"],
            "final_candidate_identity": lane["final_candidate_identity"],
            "target_patch_identity": patch_identity,
            "final_review_kind": "full",
            "final_review_dispatch_id": lane["final_review_dispatch_id"],
            "final_review_record": lane["final_review_record"],
            "done_verified": True,
        }
        if evidence_lane != expected:
            raise ContractError(f"wave evidence lane {index} does not match WAVE/STATE/patch")
        lane_candidates.add(lane["final_candidate_identity"])
        for dispatch in state["child_dispatches"]:
            agent_id = dispatch["agent_id"]
            if agent_id in all_agent_ids:
                raise ContractError(f"child agent_id {agent_id!r} appears in more than one wave task")
            all_agent_ids.add(agent_id)
    combined = integration["combined_candidate_identity"]
    if combined in lane_candidates or combined in patch_identities:
        raise ContractError("integration combined candidate reuses a lane/patch identity")
    evidence_integration = evidence["integration"]
    expected_integration = {
        "task_id": integration["task_id"],
        "workspace_id": integration_workspace,
        "combined_candidate_identity": combined,
        "content_diff_path": integration["content_diff_path"],
        "content_diff_identity": final.content_identity,
        "final_review_kind": "full",
        "final_review_dispatch_id": integration["final_review_dispatch_id"],
        "final_review_record": integration["final_review_record"],
        "done_verified": True,
    }
    for field, value in expected_integration.items():
        if evidence_integration[field] != value:
            raise ContractError(f"wave evidence integration {field} does not match WAVE/STATE")
    executor_id = evidence_integration["executor_agent_id"]
    evidence_dispatches = [
        dispatch
        for dispatch in final.integration_state["child_dispatches"]
        if str(dispatch.get("role", "")).upper() == "EXECUTOR"
        and dispatch.get("purpose") == "wave_evidence"
    ]
    if len(evidence_dispatches) != 1:
        raise ContractError(
            "wave evidence requires exactly one purpose=wave_evidence EXECUTOR dispatch"
        )
    evidence_dispatch = evidence_dispatches[0]
    prospective_identity = hashlib.sha256(prospective_raw).hexdigest()
    if (
        evidence_dispatch.get("agent_id") != executor_id
        or evidence_dispatch.get("task_id") != integration["task_id"]
        or evidence_dispatch.get("workspace_id") != integration_workspace
        or evidence_dispatch.get("parent_agent_id")
        != ctx.wave["orchestrator_agent_id"]
        or evidence_dispatch.get("lineage_verified") is not True
        or evidence_dispatch.get("wave_evidence_path")
        != ctx.wave["wave_evidence_path"]
        or evidence_dispatch.get("prospective_wave_identity")
        != prospective_identity
        or evidence_dispatch.get(
            "lifecycle", evidence_dispatch.get("status")
        )
        != "archived"
        or evidence_dispatch.get("archive_confirmed") is not True
    ):
        raise ContractError(
            "wave evidence executor is not archived and bound to task/workspace/parent/path/prospective identity"
        )
    if any(
        dispatch is not evidence_dispatch
        and dispatch.get("agent_id") == executor_id
        for dispatch in final.integration_state["child_dispatches"]
    ):
        raise ContractError(
            "wave evidence EXECUTOR agent_id is not fresh for the evidence-only dispatch"
        )
    for dispatch in final.integration_state["child_dispatches"]:
        agent_id = dispatch["agent_id"]
        if agent_id in all_agent_ids:
            raise ContractError(f"child agent_id {agent_id!r} appears in more than one wave task")
        all_agent_ids.add(agent_id)
    initial = evidence_integration["initial_git"]
    base_tree = _git(
        ctx.root_for(integration_workspace),
        "rev-parse",
        f"{ctx.wave['base_commit']}^{{tree}}",
    ).stdout.decode().strip()
    if (
        initial["head_commit"] != ctx.wave["base_commit"]
        or initial["index_tree"] != base_tree
        or initial["worktree_tree"] != base_tree
    ):
        raise ContractError("wave evidence initial_git does not prove the frozen commit/tree predicate")
    if evidence["collateral_empty"] is not True or evidence["gates_result"] != "PASS":
        raise ContractError("wave evidence collateral/gates declarations are not PASS")
    return evidence, evidence_raw


def publish_context(ctx: WaveContext) -> str:
    _require_wave_state(ctx, "GATED", "DONE")
    final = _final_bindings(ctx)
    _, prospective_raw = _read_or_freeze_prospective(ctx)
    _evidence_bindings(ctx, prospective_raw, final)
    if ctx.wave["state"] == "DONE":
        if ctx.wave_raw != prospective_raw:
            raise ContractError("published WAVE bytes differ from prospective DONE WAVE")
        return hashlib.sha256(prospective_raw).hexdigest()
    ctx.write_bytes_atomic(ctx.wave_relative, prospective_raw, "published WAVE.json")
    return hashlib.sha256(prospective_raw).hexdigest()


def done_context(ctx: WaveContext) -> None:
    _require_wave_state(ctx, "DONE")
    final = _final_bindings(ctx)
    _, prospective_raw = _read_or_freeze_prospective(ctx)
    if prospective_raw != ctx.wave_raw:
        raise ContractError("published WAVE bytes are not byte-identical to prospective DONE WAVE")
    _, evidence_raw = _evidence_bindings(ctx, prospective_raw, final)
    scope, _, _ = _integration_scope(ctx, final.bundle)
    changed = _changed_content_paths(ctx)
    unauthorized = sorted(changed - set(scope["allowed_files"]))
    if unauthorized:
        raise ContractError(f"final base-to-worktree diff contains unauthorized path {unauthorized[0]!r}")
    if ctx.wave["wave_evidence_path"] not in changed:
        raise ContractError("wave evidence path is absent from the final base-to-worktree diff")
    evidence_current = ctx.read_bytes(
        ctx.wave["wave_evidence_path"],
        "wave evidence",
        workspace_id=ctx.wave["integration"]["workspace_id"],
    )
    if evidence_current != evidence_raw:
        raise ContractError("wave evidence bytes drifted during DONE closure")


def _run(operation: Callable[[], Any], success_detail: str) -> CheckResult:
    try:
        value = operation()
    except ContractError as error:
        return CheckResult("CONTRACT_FAILED", str(error), 1)
    except InputError as error:
        return CheckResult("INPUT_ERROR", str(error), 2)
    detail = success_detail if value is None else f"{success_detail}: {value}"
    return CheckResult("PASS", detail, 0)


def preflight(
    wave_path: str | Path, workspace_roots: Mapping[str, str | Path] | None = None
) -> CheckResult:
    return _run(
        lambda: preflight_context(WaveContext(wave_path, workspace_roots)),
        "wave preflight verified",
    )


def export_target_patch(
    wave_path: str | Path,
    lane_id: str,
    workspace_roots: Mapping[str, str | Path] | None = None,
) -> CheckResult:
    return _run(
        lambda: export_target_patch_context(
            WaveContext(wave_path, workspace_roots), lane_id
        ),
        "empty target patch exported",
    )


def verify_target_patch(
    wave_path: str | Path,
    lane_id: str,
    workspace_roots: Mapping[str, str | Path] | None = None,
) -> CheckResult:
    return _run(
        lambda: verify_target_patch_context(
            WaveContext(wave_path, workspace_roots), lane_id
        ),
        "target patch verified",
    )


def apply_target_patch(
    wave_path: str | Path, workspace_roots: Mapping[str, str | Path] | None = None
) -> CheckResult:
    return _run(
        lambda: apply_target_patches_context(WaveContext(wave_path, workspace_roots)),
        "empty merge queue applied",
    )


def verify_content_diff(
    wave_path: str | Path, workspace_roots: Mapping[str, str | Path] | None = None
) -> CheckResult:
    return _run(
        lambda: verify_content_diff_context(WaveContext(wave_path, workspace_roots)),
        "integration content diff verified",
    )


def prepare_publication(
    wave_path: str | Path, workspace_roots: Mapping[str, str | Path] | None = None
) -> CheckResult:
    return _run(
        lambda: prepare_publication_context(WaveContext(wave_path, workspace_roots)),
        "prospective DONE WAVE verified",
    )


def publish(
    wave_path: str | Path, workspace_roots: Mapping[str, str | Path] | None = None
) -> CheckResult:
    return _run(
        lambda: publish_context(WaveContext(wave_path, workspace_roots)),
        "prospective DONE WAVE atomically published",
    )


def done(
    wave_path: str | Path, workspace_roots: Mapping[str, str | Path] | None = None
) -> CheckResult:
    return _run(
        lambda: done_context(WaveContext(wave_path, workspace_roots)),
        "external DONE_VERIFIED",
    )


def _parse_workspace_roots(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        workspace_id, separator, root = value.partition("=")
        if not separator or not workspace_id or not root:
            raise InputError("--workspace-root must use WORKSPACE_ID=ROOT")
        if workspace_id in result:
            raise InputError(f"duplicate --workspace-root for {workspace_id!r}")
        result[workspace_id] = root
    return result


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError(f"invalid command-line arguments: {message}")


def main(argv: list[str] | None = None) -> int:
    parser = _ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in (
        "preflight",
        "apply-target-patch",
        "verify-content-diff",
        "prepare-publication",
        "publish",
        "done",
    ):
        child = subparsers.add_parser(command)
        child.add_argument("wave", help="canonical workspace-relative .ai/waves/<wave-id>/WAVE.json")
    for command in ("export-target-patch", "verify-target-patch"):
        child = subparsers.add_parser(command)
        child.add_argument("wave", help="canonical workspace-relative .ai/waves/<wave-id>/WAVE.json")
        child.add_argument("--lane-id", required=True)
    for child in subparsers.choices.values():
        child.add_argument(
            "--workspace-root",
            action="append",
            required=True,
            metavar="WORKSPACE_ID=ROOT",
            help="trusted 1:1 workspace-id to Git-worktree-root binding; repeat for every WAVE workspace",
        )
    try:
        args = parser.parse_args(argv)
        workspace_roots = _parse_workspace_roots(args.workspace_root)
        operations: dict[str, Callable[[], CheckResult]] = {
            "preflight": lambda: preflight(args.wave, workspace_roots),
            "export-target-patch": lambda: export_target_patch(
                args.wave, args.lane_id, workspace_roots
            ),
            "verify-target-patch": lambda: verify_target_patch(
                args.wave, args.lane_id, workspace_roots
            ),
            "apply-target-patch": lambda: apply_target_patch(args.wave, workspace_roots),
            "verify-content-diff": lambda: verify_content_diff(args.wave, workspace_roots),
            "prepare-publication": lambda: prepare_publication(args.wave, workspace_roots),
            "publish": lambda: publish(args.wave, workspace_roots),
            "done": lambda: done(args.wave, workspace_roots),
        }
        result = operations[args.command]()
    except InputError as error:
        result = CheckResult("INPUT_ERROR", str(error), 2)
    stream = sys.stdout if result.exit_code == 0 else sys.stderr
    print(f"{result.outcome}: {result.detail}", file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
