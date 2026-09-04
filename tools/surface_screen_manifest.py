#!/usr/bin/env python3
"""Build and verify canonical translation_surface_screen_v1 screen manifests.

Batching is a fully defined algorithm over entries already ordered by
canonical entry_revision_identity:

- n=0: no dispatch (recorded as a zero-item outcome, never a manifest);
- n=1..3: one full member covering all entries;
- n=4..80: four contiguous q/r lanes (q=floor(n/4), the first r lanes q+1);
- n>80: fail closed -- the stable carry-over must be formed with
  ``split_carry_over`` BEFORE manifest construction and is never recorded as
  completed.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
from typing import Any

import surface_screen_result_check as check


ROOT = Path(__file__).resolve().parents[1]
SAFE_ID = re.compile(r"^[0-9a-z][0-9a-z-]{0,31}$")
SAFE_TASK_ID = re.compile(r"^[0-9a-z][0-9a-z-]{0,127}$")
# Surface manifest/group artifacts are initial-review only: a fresh retry
# increases attempt and uses fresh dispatch/group IDs, never a RE_REVIEW
# phase (RE_REVIEW belongs to the contextual contracts, not this one).
PHASES = frozenset({"REVIEW"})
SCREEN_LIMIT = 80
CARRY_OVER_ALGORITHM = "surface-carry-over/1"
ZERO_WORKSET_ALGORITHM = "surface-zero-workset/1"
WORKSET_KEYS = frozenset({
    "entries", "fixed_source_identity", "terminology_snapshot",
    "rules_version", "rendered_briefing",
})
GROUP_PAYLOAD_KEYS = frozenset({
    "contract", "task_id", "group_id", "review_phase", "cycle", "attempt",
    "lane_count", "workset", "lane_boundaries", "lanes",
})
ZERO_PAYLOAD_KEYS = frozenset({
    "contract", "task_id", "screen_count", "proves_no_surface_dispatch",
    "reason", "workset_identity", "algorithm",
})
CARRY_OVER_PAYLOAD_KEYS = frozenset({
    "contract", "task_id", "algorithm", "original_count", "screen_count",
    "carry_over_count", "ordered_screen_entry_revision_identities",
    "ordered_carry_over_entry_revision_identities",
})


def partition(count: int) -> list[dict[str, int]]:
    """Four contiguous balanced lanes; no empty lane; union is exactly n."""
    if type(count) is not int or not 4 <= count <= SCREEN_LIMIT:
        raise check.ContractError(
            "lane review requires between 4 and 80 entries; other counts use full or carry-over"
        )
    quotient, remainder = divmod(count, 4)
    offset = 0
    boundaries: list[dict[str, int]] = []
    for index in range(1, 5):
        length = quotient + (1 if index <= remainder else 0)
        boundaries.append({"index": index, "offset": offset, "length": length})
        offset += length
    return boundaries


def split_carry_over(entries: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Form the stable carry-over BEFORE manifest construction.

    The screen set is the first 80 entries in the frozen canonical
    entry_revision_identity order; the remainder is preserved in the same
    order for the next batch and is never recorded as completed.
    """
    if not isinstance(entries, list):
        raise check.ContractError("entries must be an array")
    if len(entries) <= SCREEN_LIMIT:
        return list(entries), []
    return list(entries[:SCREEN_LIMIT]), list(entries[SCREEN_LIMIT:])


def _envelope_keys(entries: list[dict[str, Any]]) -> list[str]:
    keys = [entry.get("entry_revision_identity") for entry in entries]
    if any(not isinstance(key, str) or not key for key in keys):
        raise check.ContractError("entries must carry entry_revision_identity strings")
    return keys  # type: ignore[return-value]


def build_zero_workset_identity() -> str:
    """Canonical, recomputable identity of the empty frozen workset/input
    snapshot that an n=0 no-dispatch outcome proves."""
    payload = {
        "schema_version": 1,
        "algorithm": ZERO_WORKSET_ALGORITHM,
        "contract": check.CONTRACT,
        "workset": {
            "entries": [], "fixed_source_identity": "",
            "terminology_snapshot": "", "rules_version": "",
            "rendered_briefing": "",
        },
    }
    return hashlib.sha256(check.canonical_bytes(payload)).hexdigest()


def build_zero_payload(*, task_id: str) -> dict[str, Any]:
    """Identity-bound canonical artifact proving an n=0 no-dispatch outcome.

    The zero payload is a durable terminal record: it proves that no surface
    dispatch occurred because the frozen workset is empty, and it binds the
    canonical empty-workset/input snapshot identity plus the algorithm
    version so DONE can rederive both.  It never carries provider/model/
    runtime fields and is never a dispatch envelope.
    """
    task_id = _safe_task_id(task_id)
    return {
        "contract": check.CONTRACT,
        "task_id": task_id,
        "screen_count": 0,
        "proves_no_surface_dispatch": True,
        "reason": "zero/no-dispatch",
        "algorithm": ZERO_WORKSET_ALGORITHM,
        "workset_identity": build_zero_workset_identity(),
    }


def zero_artifact_path(task_id: str) -> str:
    return f".ai/task/{_safe_task_id(task_id)}/SURFACE-SCREEN-ZERO.json"


def build_carry_over_payload(
    payload: dict[str, Any], *, task_id: str,
) -> dict[str, Any]:
    """Canonical pre-manifest split/carry-over artifact for n>80.

    Binds the original ordered workset, the first-80 screen set, and the
    remaining ordered carry-over by ``entry_revision_identity`` plus counts
    and the fixed algorithm version.  It must be persisted BEFORE manifest
    construction and never marks the carry-over complete.
    """
    check.validate_payload(payload)
    task_id = _safe_task_id(task_id)
    entries = payload["entries"]
    if len(entries) <= SCREEN_LIMIT:
        raise check.ContractError(
            "carry-over artifact requires more than 80 frozen entries"
        )
    screen, carry = split_carry_over(entries)
    return {
        "contract": check.CONTRACT,
        "task_id": task_id,
        "algorithm": CARRY_OVER_ALGORITHM,
        "original_count": len(entries),
        "screen_count": len(screen),
        "carry_over_count": len(carry),
        "ordered_screen_entry_revision_identities": _envelope_keys(screen),
        "ordered_carry_over_entry_revision_identities": _envelope_keys(carry),
    }


def carry_over_artifact_path(task_id: str) -> str:
    return f".ai/task/{_safe_task_id(task_id)}/SURFACE-SCREEN-CARRY-OVER.json"


def validate_zero_payload(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or frozenset(value) != ZERO_PAYLOAD_KEYS:
        raise check.ContractError("zero payload must have exactly the seven canonical keys")
    if value["contract"] != check.CONTRACT or value["screen_count"] != 0:
        raise check.ContractError("zero payload must bind an empty screen set")
    _safe_task_id(value["task_id"])
    if value["proves_no_surface_dispatch"] is not True:
        raise check.ContractError("zero payload must prove literal no-dispatch")
    if value["reason"] != "zero/no-dispatch":
        raise check.ContractError("zero payload reason must be zero/no-dispatch")
    if value["algorithm"] != ZERO_WORKSET_ALGORITHM:
        raise check.ContractError("zero payload algorithm version is not supported")
    if value["workset_identity"] != build_zero_workset_identity():
        raise check.ContractError(
            "zero payload does not bind the canonical empty workset identity"
        )
    return value


def validate_carry_over_payload(
    value: object, *, entries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate a carry-over artifact, optionally against its frozen workset."""
    if not isinstance(value, dict) or frozenset(value) != CARRY_OVER_PAYLOAD_KEYS:
        raise check.ContractError(
            "carry-over payload must have exactly the eight canonical keys"
        )
    if value["contract"] != check.CONTRACT:
        raise check.ContractError(f"carry-over contract must be {check.CONTRACT}")
    _safe_task_id(value["task_id"])
    if value["algorithm"] != CARRY_OVER_ALGORITHM:
        raise check.ContractError("carry-over algorithm version is not supported")
    counts = (value["original_count"], value["screen_count"], value["carry_over_count"])
    if any(type(count) is not int or count < 0 for count in counts):
        raise check.ContractError("carry-over counts must be non-negative integers")
    if value["screen_count"] != SCREEN_LIMIT or value["original_count"] <= SCREEN_LIMIT:
        raise check.ContractError("carry-over must split more than 80 entries into 80")
    if value["screen_count"] + value["carry_over_count"] != value["original_count"]:
        raise check.ContractError("carry-over counts must not lose entries")
    screen_keys = value["ordered_screen_entry_revision_identities"]
    carry_keys = value["ordered_carry_over_entry_revision_identities"]
    if not isinstance(screen_keys, list) or not isinstance(carry_keys, list):
        raise check.ContractError("carry-over identity arrays must be arrays")
    if len(screen_keys) != value["screen_count"] or len(carry_keys) != value["carry_over_count"]:
        raise check.ContractError("carry-over identity arrays must match the counts")
    for key in (*screen_keys, *carry_keys):
        if not isinstance(key, str) or not check.SHA256.fullmatch(key):
            raise check.ContractError(
                "carry-over identities must be 64 lowercase hexadecimal characters"
            )
    if len(set(screen_keys) & set(carry_keys)):
        raise check.ContractError("carry-over and screen sets must be disjoint")
    if entries is not None:
        expected = _envelope_keys(entries)
        if screen_keys + carry_keys != expected:
            raise check.ContractError(
                "carry-over artifact does not bind the original ordered workset"
            )
    return value


def plan(entries: object) -> dict[str, Any]:
    """Return the batching decision for a validated, canonically ordered workset."""
    if not isinstance(entries, list):
        raise check.ContractError("entries must be an array")
    count = len(entries)
    if count == 0:
        return {
            "action": "no_dispatch", "screen_count": 0, "carry_over_count": 0,
            "lane_count": 0,
        }
    if count > SCREEN_LIMIT:
        screen, carry = split_carry_over(entries)
        return {
            "action": "carry_over_required",
            "screen_count": len(screen), "carry_over_count": len(carry),
            "lane_count": None,
        }
    if count <= 3:
        return {
            "action": "full", "screen_count": count, "carry_over_count": 0,
            "lane_count": 1,
        }
    return {
        "action": "lanes", "screen_count": count, "carry_over_count": 0,
        "lane_count": 4, "lane_boundaries": partition(count),
    }


def _safe_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value):
        raise check.ContractError(f"{label} is not dispatch-safe")
    return value


def _safe_task_id(value: object) -> str:
    if not isinstance(value, str) or not SAFE_TASK_ID.fullmatch(value):
        raise check.ContractError("task_id is not path-safe")
    return value


def _workset(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "entries": payload["entries"],
        "fixed_source_identity": payload["fixed_source_identity"],
        "terminology_snapshot": payload["terminology_snapshot"],
        "rules_version": payload["rules_version"],
        "rendered_briefing": payload["rendered_briefing"],
    }


def _envelope_path(task_id: str, dispatch_id: str) -> str:
    return f".ai/task/{task_id}/SURFACE-SCREEN-ENVELOPE-{dispatch_id}.json"


def build_full(
    payload: dict[str, Any], *, task_id: str, dispatch_id: str,
) -> tuple[dict[str, Any], str, list[tuple[str, dict[str, Any]]]]:
    """One full member for n=1..3: a single envelope covering every entry."""
    check.validate_payload(payload)
    if not 1 <= len(payload["entries"]) <= 3:
        raise check.ContractError("full surface screen requires between 1 and 3 entries")
    task_id = _safe_task_id(task_id)
    dispatch_id = _safe_id(dispatch_id, "dispatch_id")
    identity = hashlib.sha256(check.canonical_payload_bytes(payload)).hexdigest()
    path = _envelope_path(task_id, dispatch_id)
    check.render_dispatch_prompt(identity, path)
    envelope = {"candidate_identity": identity, "payload": payload}
    return envelope, path, [(path, envelope)]


def build_group(
    payload: dict[str, Any], *, task_id: str, group_id: str, review_phase: str,
    cycle: int, attempt: int, dispatch_ids: list[str],
) -> tuple[dict[str, Any], str, list[tuple[str, dict[str, Any]]]]:
    """Four contiguous q/r lanes plus the authoritative group manifest."""
    check.validate_payload(payload)
    task_id = _safe_task_id(task_id)
    group_id = _safe_id(group_id, "group_id")
    if review_phase not in PHASES:
        raise check.ContractError("review_phase must be REVIEW; surface retries use fresh attempt/IDs")
    if type(cycle) is not int or cycle < 0 or type(attempt) is not int or attempt < 1:
        raise check.ContractError("cycle/attempt must be non-negative/positive integers")
    if len(dispatch_ids) != 4 or len(set(dispatch_ids)) != 4:
        raise check.ContractError("exactly four distinct dispatch IDs are required")
    dispatch_ids = [_safe_id(item, "dispatch_id") for item in dispatch_ids]
    boundaries = partition(len(payload["entries"]))
    workset = _workset(payload)
    lanes: list[dict[str, Any]] = []
    envelopes: list[tuple[str, dict[str, Any]]] = []
    for boundary, dispatch_id in zip(boundaries, dispatch_ids):
        start, end = boundary["offset"], boundary["offset"] + boundary["length"]
        lane_payload = {**workset, "contract": check.CONTRACT, "entries": workset["entries"][start:end]}
        lane_identity = hashlib.sha256(check.canonical_payload_bytes(lane_payload)).hexdigest()
        path = _envelope_path(task_id, dispatch_id)
        check.render_dispatch_prompt(lane_identity, path)
        lanes.append({
            "index": boundary["index"], "dispatch_id": dispatch_id,
            "input_path": path, "candidate_identity": lane_identity,
        })
        envelopes.append((path, {"candidate_identity": lane_identity, "payload": lane_payload}))
    group_payload = {
        "contract": check.LANE_GROUP_CONTRACT,
        "task_id": task_id, "group_id": group_id, "review_phase": review_phase,
        "cycle": cycle, "attempt": attempt, "lane_count": 4,
        "workset": workset, "lane_boundaries": boundaries, "lanes": lanes,
    }
    manifest_path = f".ai/task/{task_id}/SURFACE-SCREEN-GROUP-{group_id}.json"
    manifest = {
        "group_identity": hashlib.sha256(check.canonical_bytes(group_payload)).hexdigest(),
        "payload": group_payload,
    }
    return manifest, manifest_path, envelopes


def validate_group_manifest(
    manifest: object, *, root: Path = ROOT, manifest_path: str | None = None,
) -> dict[str, Any]:
    if not isinstance(manifest, dict) or frozenset(manifest) != {"group_identity", "payload"}:
        raise check.ContractError("manifest must contain exactly group_identity and payload")
    identity, payload = manifest["group_identity"], manifest["payload"]
    if not isinstance(identity, str) or not check.SHA256.fullmatch(identity) or not isinstance(payload, dict):
        raise check.ContractError("manifest identity/payload is invalid")
    if hashlib.sha256(check.canonical_bytes(payload)).hexdigest() != identity:
        raise check.ContractError("group_identity does not match manifest payload")
    if frozenset(payload) != GROUP_PAYLOAD_KEYS or payload["contract"] != check.LANE_GROUP_CONTRACT:
        raise check.ContractError("manifest payload has an invalid exact shape or contract")
    task_id = _safe_task_id(payload["task_id"])
    group_id = _safe_id(payload["group_id"], "group_id")
    if (
        payload["review_phase"] not in PHASES
        or type(payload["cycle"]) is not int or payload["cycle"] < 0
        or type(payload["attempt"]) is not int or payload["attempt"] < 1
    ):
        raise check.ContractError("manifest stage fields are invalid")
    if manifest_path not in (None, f".ai/task/{task_id}/SURFACE-SCREEN-GROUP-{group_id}.json"):
        raise check.ContractError("manifest path does not bind task_id/group_id")
    workset = payload["workset"]
    if not isinstance(workset, dict) or frozenset(workset) != WORKSET_KEYS:
        raise check.ContractError("workset has an invalid exact shape")
    draft = {"contract": check.CONTRACT, **workset}
    check.validate_payload(draft)
    boundaries, lanes = payload["lane_boundaries"], payload["lanes"]
    if payload["lane_count"] != 4 or not isinstance(boundaries, list) or not isinstance(lanes, list):
        raise check.ContractError("lane_count and lane arrays must describe exactly four lanes")
    if boundaries != partition(len(workset["entries"])) or len(lanes) != 4:
        raise check.ContractError("lane boundaries are not the canonical balanced partition")
    seen_dispatches: set[str] = set()
    manifest_label = manifest_path or "<unbound manifest>"
    for boundary, lane in zip(boundaries, lanes):
        if not isinstance(lane, dict) or frozenset(lane) != {
            "index", "dispatch_id", "input_path", "candidate_identity"
        }:
            raise check.ContractError(
                f"{manifest_label}: lane entry has an invalid exact shape"
            )
        index = boundary["index"]
        dispatch_id = _safe_id(lane["dispatch_id"], "dispatch_id")
        if dispatch_id in seen_dispatches or lane["index"] != index:
            raise check.ContractError(
                f"{manifest_label}: lane indices/dispatch IDs must be ordered and unique"
            )
        seen_dispatches.add(dispatch_id)
        expected_path = _envelope_path(task_id, dispatch_id)
        if lane["input_path"] != expected_path:
            raise check.ContractError(
                f"{manifest_label}: lane input_path does not bind task/dispatch"
            )
        check.render_dispatch_prompt(lane["candidate_identity"], expected_path)
        envelope_path = _ordinary_file(root, expected_path, "lane input_path")
        envelope_bytes = envelope_path.read_bytes()
        envelope = check.strict_json_bytes(envelope_bytes, label="lane envelope")
        if envelope_bytes != check.canonical_bytes(envelope):
            raise check.ContractError(
                f"{manifest_label}: lane envelope bytes are not canonical compact JSON"
            )
        lane_payload, candidate = check.validate_envelope(envelope)
        start, end = boundary["offset"], boundary["offset"] + boundary["length"]
        for key in ("fixed_source_identity", "terminology_snapshot", "rules_version", "rendered_briefing"):
            if lane_payload[key] != workset[key]:
                raise check.ContractError(
                    f"{manifest_label}: lane {index} {key} drifts from the lane-neutral workset"
                )
        if lane_payload["entries"] != workset["entries"][start:end]:
            raise check.ContractError(
                f"{manifest_label}: lane {index} entry slice drifts from the workset"
            )
        if lane["candidate_identity"] != candidate:
            raise check.ContractError(
                f"{manifest_label}: lane candidate identity does not match envelope"
            )
    return manifest


def _ordinary_file(root: Path, relative: str, label: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise check.InputError(f"{label} escapes workspace")
    candidate = root.resolve() / path
    if any(
        (root.resolve().joinpath(*path.parts[:index])).is_symlink()
        for index in range(1, len(path.parts) + 1)
    ):
        raise check.InputError(f"{label} traverses a symlink")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise check.InputError(f"{label} is not an ordinary workspace file") from error
    if not resolved.is_file():
        raise check.InputError(f"{label} is not an ordinary workspace file")
    return resolved


def _write_idempotent(path: Path, data: bytes, *, root: Path) -> None:
    root = root.resolve(strict=True)
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise check.InputError(f"publication path escapes workspace: {path}") from error
    current = root
    for component in relative.parts[:-1]:
        current /= component
        if current.is_symlink():
            raise check.InputError(f"publication path traverses a symlink: {current}")
        if current.exists() and not current.is_dir():
            raise check.InputError(f"publication parent is not a directory: {current}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or path.exists():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
            raise check.InputError(f"refusing to overwrite inconsistent file: {path}")
        return
    path.write_bytes(data)


def load_draft_bytes(draft_bytes: bytes) -> dict[str, Any]:
    """Strictly validate one frozen surface-screen draft payload.

    Shared by the CLI and by the DONE-side evidence checks: the draft must
    parse strictly, carry the canonical payload shape, and its entries are
    returned in the canonical ``entry_revision_identity`` byte order used
    for every batching decision.
    """
    if draft_bytes.startswith(b"\xef\xbb\xbf"):
        raise check.InputError("draft payload must not contain a UTF-8 BOM")
    draft = check.strict_json_bytes(draft_bytes, label="draft payload")
    if not isinstance(draft, dict):
        raise check.ContractError("draft payload must be an object")
    entries = draft.get("entries")
    if not isinstance(entries, list):
        raise check.ContractError("draft payload entries must be an array")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise check.ContractError(
                f"draft entries[{index}] must be an object with the tool taxonomy; "
                "free-form drafts cannot be screened"
            )
    # Carry-over ordering is the canonical entry_revision_identity byte order.
    try:
        ordered = sorted(entries, key=lambda entry: entry.get("entry_revision_identity", ""))
    except TypeError as error:
        raise check.ContractError("draft entries must carry string entry_revision_identity values") from error
    draft["entries"] = ordered
    if not entries:
        # n=0 never dispatches and never builds an envelope; the scalar keys
        # are still validated so a zero draft cannot smuggle a foreign shape.
        if frozenset(draft) != frozenset(check.PAYLOAD_KEYS):
            raise check.ContractError("zero draft payload must have exactly the six canonical keys")
        if draft["contract"] != check.CONTRACT:
            raise check.ContractError(f"zero draft contract must be {check.CONTRACT}")
        check._typed_source_identity(draft["fixed_source_identity"])
        check._nonempty_string(draft["rules_version"], "rules_version")
        for key in ("terminology_snapshot", "rendered_briefing"):
            if not isinstance(draft[key], str):
                raise check.ContractError(f"zero draft {key} must be a string")
        return draft
    check.validate_payload(draft)
    return draft


def load_draft(path: str) -> dict[str, Any]:
    """Load and strictly validate the frozen draft stored at ``path``."""
    return load_draft_bytes(Path(path).read_bytes())


def main_impl(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    plan_command = sub.add_parser("plan")
    plan_command.add_argument("draft")
    plan_command.add_argument("--root", default=str(ROOT))
    build = sub.add_parser("build")
    build.add_argument("draft")
    build.add_argument("--task-id", required=True)
    build.add_argument("--group-id")
    build.add_argument("--review-phase", choices=sorted(PHASES), default="REVIEW")
    build.add_argument("--cycle", type=int, default=None)
    build.add_argument("--attempt", type=int, default=None)
    build.add_argument("--dispatch-id", action="append", default=None)
    build.add_argument("--root", default=str(ROOT))
    check_command = sub.add_parser("check")
    check_command.add_argument("manifest")
    check_command.add_argument("--root", default=str(ROOT))
    check_zero = sub.add_parser("check-zero")
    check_zero.add_argument("artifact")
    check_zero.add_argument("--root", default=str(ROOT))
    check_carry = sub.add_parser("check-carry-over")
    check_carry.add_argument("artifact")
    check_carry.add_argument("--draft")
    check_carry.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if args.command == "plan":
        draft = load_draft(args.draft)
        print(f"PLAN {check.canonical_bytes(plan(draft['entries'])).decode('utf-8')}")
    elif args.command == "build":
        draft = load_draft(args.draft)
        entries = draft["entries"]
        count = len(entries)
        if count == 0:
            # n=0 never dispatches: no dispatch/group/cycle/attempt inputs.
            forbidden = [
                flag for flag, given in (
                    ("--dispatch-id", bool(args.dispatch_id)),
                    ("--group-id", args.group_id is not None),
                    ("--cycle", args.cycle is not None),
                    ("--attempt", args.attempt is not None),
                    ("--review-phase", args.review_phase != "REVIEW"),
                ) if given
            ]
            if forbidden:
                raise check.ContractError(
                    "zero/no-dispatch build must not declare dispatch inputs: "
                    + ", ".join(forbidden)
                )
            zero = build_zero_payload(task_id=args.task_id)
            zero_path = zero_artifact_path(args.task_id)
            _write_idempotent(root / zero_path, check.canonical_bytes(zero), root=root)
            print(f"ZERO_RECORDED {zero_path}")
        elif count > SCREEN_LIMIT:
            carry = build_carry_over_payload(draft, task_id=args.task_id)
            carry_path = carry_over_artifact_path(args.task_id)
            _write_idempotent(root / carry_path, check.canonical_bytes(carry), root=root)
            print(
                f"CARRY_OVER_REQUIRED {carry_path} screen=80 "
                f"carry_over={carry['carry_over_count']}"
            )
            raise check.ContractError(
                "n>80 fails closed; the pre-manifest carry-over artifact is recorded "
                "and the next batch must screen it before any manifest construction"
            )
        elif count <= 3:
            if args.cycle is None or args.attempt is None:
                raise check.ContractError("dispatch build requires --cycle and --attempt")
            if args.group_id is not None:
                raise check.ContractError("full screen (n<=3) must not declare a group_id")
            if len(args.dispatch_id or []) != 1:
                raise check.ContractError("full screen requires exactly one dispatch ID")
            _, path, envelopes = build_full(
                draft, task_id=args.task_id, dispatch_id=args.dispatch_id[0],
            )
            manifest_path: str | None = None
        else:
            if args.cycle is None or args.attempt is None:
                raise check.ContractError("dispatch build requires --cycle and --attempt")
            if args.group_id is None:
                raise check.ContractError("lane screen (n>=4) requires a group_id")
            if len(args.dispatch_id or []) != 4:
                raise check.ContractError("lane screen requires exactly four dispatch IDs")
            manifest, manifest_path, envelopes = build_group(
                draft, task_id=args.task_id, group_id=args.group_id,
                review_phase=args.review_phase, cycle=args.cycle,
                attempt=args.attempt, dispatch_ids=args.dispatch_id,
            )
        # n>80 never reaches here: the carry-over branch above fails closed.
        if count == 0:
            return 0
        for relative, envelope in envelopes:
            _write_idempotent(root / relative, check.canonical_bytes(envelope), root=root)
        if manifest_path is not None:
            _write_idempotent(root / manifest_path, check.canonical_bytes(manifest), root=root)
            validate_group_manifest(manifest, root=root, manifest_path=manifest_path)
            print(f"MANIFEST_BUILT {manifest_path}")
        else:
            print(f"ENVELOPE_BUILT {path}")
    elif args.command == "check":
        path = _ordinary_file(root, args.manifest, "manifest")
        manifest_bytes = path.read_bytes()
        manifest = check.strict_json_bytes(manifest_bytes, label="manifest")
        if manifest_bytes != check.canonical_bytes(manifest):
            raise check.ContractError("manifest bytes are not canonical compact JSON")
        validate_group_manifest(
            manifest, root=root, manifest_path=Path(args.manifest).as_posix()
        )
        print("MANIFEST_VERIFIED")
    elif args.command == "check-zero":
        path = _ordinary_file(root, args.artifact, "zero artifact")
        artifact_bytes = path.read_bytes()
        artifact = check.strict_json_bytes(artifact_bytes, label="zero artifact")
        if artifact_bytes != check.canonical_bytes(artifact):
            raise check.ContractError("zero artifact bytes are not canonical compact JSON")
        validate_zero_payload(artifact)
        expected = zero_artifact_path(artifact["task_id"])
        if Path(args.artifact).as_posix() != expected:
            raise check.ContractError("zero artifact path does not bind its task_id")
        print("ZERO_VERIFIED")
    else:
        path = _ordinary_file(root, args.artifact, "carry-over artifact")
        artifact_bytes = path.read_bytes()
        artifact = check.strict_json_bytes(artifact_bytes, label="carry-over artifact")
        if artifact_bytes != check.canonical_bytes(artifact):
            raise check.ContractError("carry-over artifact bytes are not canonical compact JSON")
        entries = None
        if args.draft:
            entries = load_draft(args.draft)["entries"]
        validate_carry_over_payload(artifact, entries=entries)
        expected = carry_over_artifact_path(artifact["task_id"])
        if Path(args.artifact).as_posix() != expected:
            raise check.ContractError("carry-over artifact path does not bind its task_id")
        print("CARRY_OVER_VERIFIED")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return main_impl(argv)
    except OSError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    except check.InputError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    except check.ContractError as error:
        print(f"MANIFEST_FAILED: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
