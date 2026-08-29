#!/usr/bin/env python3
"""Build and verify canonical four-lane translation_contextual_v2 manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

import contextual_result_check as result_check


ROOT = Path(__file__).resolve().parents[1]
SAFE_ID = re.compile(r"^[0-9a-z][0-9a-z-]{0,31}$")
SAFE_TASK_ID = re.compile(r"^[0-9a-z][0-9a-z-]{0,127}$")
PHASES = frozenset({"REVIEW", "RE_REVIEW"})
PROMPT_TEMPLATE = (
    "任务：审核 input_path 中全部冻结 revision；按其术语、上下文及所引固定源码，仅报有证据的实质语义、机制、术语、关系或跨条一致性问题；否则判 OK。\n"
    "输入：candidate_identity=<candidate_identity>；input_path=<input_path>。全程只读；仅读该文件、其明确引用内容及 docs/paseo-translation-context-review-v2-contract.md 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n"
    "输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 revision 并回显 identity；首字节{、末字节}，无其他文字、Markdown 或围栏。"
)


def canonical_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise result_check.ContractError(
            f"value is not canonicalizable: {error}"
        ) from error


def partition(count: int) -> list[dict[str, int]]:
    if type(count) is not int or count < 4:
        raise result_check.ContractError("lane review requires at least four revisions")
    quotient, remainder = divmod(count, 4)
    offset = 0
    boundaries: list[dict[str, int]] = []
    for index in range(1, 5):
        length = quotient + (1 if index <= remainder else 0)
        boundaries.append({"index": index, "offset": offset, "length": length})
        offset += length
    return boundaries


def render_dispatch_prompt(candidate_identity: str, input_path: str) -> str:
    if not isinstance(candidate_identity, str) or not result_check.SHA256.fullmatch(candidate_identity):
        raise result_check.ContractError("prompt candidate identity is invalid")
    if not isinstance(input_path, str):
        raise result_check.ContractError("prompt input_path is invalid")
    prompt = PROMPT_TEMPLATE.replace(
        "<candidate_identity>", candidate_identity
    ).replace("<input_path>", input_path)
    if len(PROMPT_TEMPLATE.encode("utf-8")) > 800 or len(prompt.encode("utf-8")) > 800:
        raise result_check.ContractError("prompt template or instance exceeds 800 UTF-8 bytes")
    return prompt


def _safe_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value):
        raise result_check.ContractError(f"{label} is not dispatch-safe")
    return value


def _safe_task_id(value: object) -> str:
    if not isinstance(value, str) or not SAFE_TASK_ID.fullmatch(value):
        raise result_check.ContractError("task_id is not path-safe")
    return value


def _workset(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "ordered_revision_keys": payload["ordered_revision_keys"],
        "translation_snapshot": payload["translation_snapshot"],
        "fixed_source_identity": payload["fixed_source_identity"],
        "terminology_snapshot": payload["terminology_snapshot"],
        "bounded_context": payload["bounded_context"],
    }


def build_group(
    draft_payload: object, *, task_id: str, group_id: str, review_phase: str,
    cycle: int, attempt: int, dispatch_ids: list[str],
) -> tuple[dict[str, Any], list[tuple[str, dict[str, Any]]]]:
    result_check.canonical_payload_bytes(draft_payload)
    assert isinstance(draft_payload, dict)
    task_id = _safe_task_id(task_id)
    group_id = _safe_id(group_id, "group_id")
    if review_phase not in PHASES:
        raise result_check.ContractError("review_phase must be REVIEW or RE_REVIEW")
    if type(cycle) is not int or cycle < 0 or type(attempt) is not int or attempt < 1:
        raise result_check.ContractError("cycle/attempt must be non-negative/positive integers")
    if len(dispatch_ids) != 4 or len(set(dispatch_ids)) != 4:
        raise result_check.ContractError("exactly four distinct dispatch IDs are required")
    dispatch_ids = [_safe_id(item, "dispatch_id") for item in dispatch_ids]
    boundaries = partition(len(draft_payload["ordered_revision_keys"]))
    lanes: list[dict[str, Any]] = []
    envelopes: list[tuple[str, dict[str, Any]]] = []
    for boundary, dispatch_id in zip(boundaries, dispatch_ids):
        start, end = boundary["offset"], boundary["offset"] + boundary["length"]
        lane_payload = {
            **draft_payload,
            "ordered_revision_keys": draft_payload["ordered_revision_keys"][start:end],
            "translation_snapshot": draft_payload["translation_snapshot"][start:end],
            "bounded_context": draft_payload["bounded_context"][start:end],
        }
        lane_identity = hashlib.sha256(result_check.canonical_payload_bytes(lane_payload)).hexdigest()
        path = f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-{dispatch_id}.json"
        envelope = {"candidate_identity": lane_identity, "payload": lane_payload}
        render_dispatch_prompt(lane_identity, path)
        lanes.append({
            "index": boundary["index"], "dispatch_id": dispatch_id,
            "input_path": path, "candidate_identity": lane_identity,
        })
        envelopes.append((path, envelope))
    payload = {
        "contract": "translation_contextual_v2_lane_group",
        "task_id": task_id, "group_id": group_id, "review_phase": review_phase,
        "cycle": cycle, "attempt": attempt, "lane_count": 4,
        "workset": _workset(draft_payload), "lane_boundaries": boundaries,
        "lanes": lanes,
    }
    manifest = {
        "group_identity": hashlib.sha256(canonical_bytes(payload)).hexdigest(),
        "payload": payload,
    }
    return manifest, envelopes


def validate_manifest(manifest: object, *, root: Path = ROOT, manifest_path: str | None = None) -> dict[str, Any]:
    if not isinstance(manifest, dict) or set(manifest) != {"group_identity", "payload"}:
        raise result_check.ContractError("manifest must contain exactly group_identity and payload")
    identity, payload = manifest.get("group_identity"), manifest.get("payload")
    if not isinstance(identity, str) or not result_check.SHA256.fullmatch(identity) or not isinstance(payload, dict):
        raise result_check.ContractError("manifest identity/payload is invalid")
    try:
        computed_identity = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    except (TypeError, ValueError) as error:
        raise result_check.ContractError(f"manifest payload is not canonicalizable: {error}") from error
    if computed_identity != identity:
        raise result_check.ContractError("group_identity does not match manifest payload")
    expected_keys = {
        "contract", "task_id", "group_id", "review_phase", "cycle", "attempt",
        "lane_count", "workset", "lane_boundaries", "lanes",
    }
    if set(payload) != expected_keys or payload.get("contract") != "translation_contextual_v2_lane_group":
        raise result_check.ContractError("manifest payload has an invalid exact shape or contract")
    task_id = _safe_task_id(payload.get("task_id"))
    group_id = _safe_id(payload.get("group_id"), "group_id")
    if (
        payload.get("review_phase") not in PHASES
        or type(payload.get("cycle")) is not int or payload["cycle"] < 0
        or type(payload.get("attempt")) is not int or payload["attempt"] < 1
    ):
        raise result_check.ContractError("manifest stage fields are invalid")
    if manifest_path != f".ai/task/{task_id}/CONTEXTUAL-LANE-GROUP-{group_id}.json" and manifest_path is not None:
        raise result_check.ContractError("manifest path does not bind task_id/group_id")
    workset = payload.get("workset")
    if not isinstance(workset, dict) or set(workset) != {
        "ordered_revision_keys", "translation_snapshot", "fixed_source_identity",
        "terminology_snapshot", "bounded_context",
    }:
        raise result_check.ContractError("workset has an invalid exact shape")
    draft = {"contract": "translation_contextual_v2", **workset, "rendered_briefing": "lane-neutral"}
    result_check.canonical_payload_bytes(draft)
    boundaries = payload.get("lane_boundaries")
    lanes = payload.get("lanes")
    if payload.get("lane_count") != 4 or not isinstance(boundaries, list) or not isinstance(lanes, list):
        raise result_check.ContractError("lane_count and lane arrays must describe exactly four lanes")
    if boundaries != partition(len(workset["ordered_revision_keys"])) or len(lanes) != 4:
        raise result_check.ContractError("lane boundaries are not the canonical balanced partition")
    seen_dispatches: set[str] = set()
    briefings: list[str] = []
    for boundary, lane in zip(boundaries, lanes):
        if not isinstance(lane, dict) or set(lane) != {"index", "dispatch_id", "input_path", "candidate_identity"}:
            raise result_check.ContractError("lane entry has an invalid exact shape")
        index = boundary["index"]
        dispatch_id = _safe_id(lane.get("dispatch_id"), "dispatch_id")
        if dispatch_id in seen_dispatches or lane.get("index") != index:
            raise result_check.ContractError("lane indices/dispatch IDs must be ordered and unique")
        seen_dispatches.add(dispatch_id)
        expected_path = f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-{dispatch_id}.json"
        if lane.get("input_path") != expected_path:
            raise result_check.ContractError("lane input_path does not bind task/dispatch")
        render_dispatch_prompt(lane.get("candidate_identity"), expected_path)
        envelope_path = _ordinary_file(root, expected_path, "lane input_path")
        envelope_bytes = envelope_path.read_bytes()
        envelope = result_check.strict_json_bytes(envelope_bytes, label="lane envelope")
        lane_payload, candidate = result_check.validate_envelope(envelope)
        if envelope_bytes != canonical_bytes(envelope):
            raise result_check.ContractError("lane envelope bytes are not canonical compact JSON")
        start, end = boundary["offset"], boundary["offset"] + boundary["length"]
        for key in ("fixed_source_identity", "terminology_snapshot"):
            if lane_payload[key] != workset[key]:
                raise result_check.ContractError(f"lane {index} {key} drifts from workset")
        for key in ("ordered_revision_keys", "translation_snapshot", "bounded_context"):
            if lane_payload[key] != workset[key][start:end]:
                raise result_check.ContractError(f"lane {index} slice drifts from workset")
        if lane.get("candidate_identity") != candidate:
            raise result_check.ContractError("lane candidate identity does not match envelope")
        briefings.append(lane_payload["rendered_briefing"])
    if len(set(briefings)) != 1:
        raise result_check.ContractError("lane briefings must be identical and lane-neutral")
    return manifest


def _ordinary_file(root: Path, relative: str, label: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise result_check.InputError(f"{label} escapes workspace")
    candidate = root.resolve() / path
    if any((root.resolve().joinpath(*path.parts[:index])).is_symlink() for index in range(1, len(path.parts) + 1)):
        raise result_check.InputError(f"{label} traverses a symlink")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise result_check.InputError(f"{label} is not an ordinary workspace file") from error
    if not resolved.is_file():
        raise result_check.InputError(f"{label} is not an ordinary workspace file")
    return resolved


def _write_idempotent(path: Path, data: bytes, *, root: Path) -> None:
    root = root.resolve(strict=True)
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise result_check.InputError(f"publication path escapes workspace: {path}") from error
    current = root
    for component in relative.parts[:-1]:
        current /= component
        if current.is_symlink():
            raise result_check.InputError(f"publication path traverses a symlink: {current}")
        if current.exists() and not current.is_dir():
            raise result_check.InputError(f"publication parent is not a directory: {current}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or path.exists():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
            raise result_check.InputError(f"refusing to overwrite inconsistent file: {path}")
        return
    path.write_bytes(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("draft")
    build.add_argument("--task-id", required=True)
    build.add_argument("--group-id", required=True)
    build.add_argument("--review-phase", required=True, choices=sorted(PHASES))
    build.add_argument("--cycle", required=True, type=int)
    build.add_argument("--attempt", required=True, type=int)
    build.add_argument("--dispatch-id", action="append", required=True)
    build.add_argument("--root", default=str(ROOT))
    check = sub.add_parser("check")
    check.add_argument("manifest")
    check.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve()
        if args.command == "build":
            draft_bytes = Path(args.draft).read_bytes()
            if draft_bytes.startswith(b"\xef\xbb\xbf"):
                raise result_check.InputError("draft payload must not contain a UTF-8 BOM")
            draft = result_check.strict_json_bytes(draft_bytes, label="draft payload")
            manifest, envelopes = build_group(
                draft, task_id=args.task_id, group_id=args.group_id,
                review_phase=args.review_phase, cycle=args.cycle,
                attempt=args.attempt, dispatch_ids=args.dispatch_id,
            )
            manifest_rel = f".ai/task/{args.task_id}/CONTEXTUAL-LANE-GROUP-{args.group_id}.json"
            for relative, envelope in envelopes:
                _write_idempotent(root / relative, canonical_bytes(envelope), root=root)
            _write_idempotent(root / manifest_rel, canonical_bytes(manifest), root=root)
            validate_manifest(manifest, root=root, manifest_path=manifest_rel)
            print(f"MANIFEST_BUILT {manifest_rel}")
        else:
            path = _ordinary_file(root, args.manifest, "manifest")
            manifest_bytes = path.read_bytes()
            manifest = result_check.strict_json_bytes(manifest_bytes, label="manifest")
            if manifest_bytes != canonical_bytes(manifest):
                raise result_check.ContractError("manifest bytes are not canonical compact JSON")
            validate_manifest(manifest, root=root, manifest_path=Path(args.manifest).as_posix())
            print("MANIFEST_VERIFIED")
    except OSError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    except result_check.InputError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    except result_check.ContractError as error:
        print(f"MANIFEST_FAILED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
