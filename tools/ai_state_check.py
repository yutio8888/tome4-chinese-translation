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
from pathlib import Path
import re
from typing import Any

import review_evidence


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
}
PURPOSE_ROLES = {
    "normal_review": "REVIEWER",
    "translation_contextual_v1": "REVIEWER",
    "cross_review": "senior-reviewer",
    "scope_audit": "senior-reviewer",
}
COMPLETION_VALUES = frozenset({
    "completed", "completed_with_findings", "PASS", "CHANGES_REQUIRED", "FINDINGS", "OK",
})
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


def _ordinary_workspace_file(value: object, label: str) -> Path:
    """Resolve one existing ordinary, repository-relative file or fail closed."""
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty workspace-relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise InputError(f"{label} escapes the workspace: {value!r}")
    candidate = ROOT / relative
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(ROOT.resolve())
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


def _schema_valid(state: dict[str, Any]) -> tuple[bool, str]:
    children = state.get("child_dispatches")
    if children is not None and not isinstance(children, list):
        return False, "child_dispatches must be a list or null"
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


def _record_paths(state: dict[str, Any]) -> list[Path]:
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
            paths.append(_ordinary_workspace_file(item, f"{field}[{index}]"))
    return paths


def _load_records(state: dict[str, Any]) -> list[tuple[dict[str, Any], Path]]:
    loaded: list[tuple[dict[str, Any], Path]] = []
    for path in _record_paths(state):
        record = _read_json(path, f"review record {path.relative_to(ROOT)}")
        if not isinstance(record, dict):
            raise ContractError(f"review record {path.relative_to(ROOT)} must be an object")
        loaded.append((record, path))
    return loaded


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
    for contract in state["review_contracts"]:
        if contract not in covered:
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


def _canonical_payload_bytes(payload: object) -> bytes:
    if not isinstance(payload, dict) or frozenset(payload) != CONTEXTUAL_PAYLOAD_KEYS:
        raise ContractError("contextual envelope payload must have exactly the seven canonical keys")
    required_strings = ("fixed_source_identity", "terminology_snapshot", "rendered_briefing")
    if (
        payload.get("contract") != "translation_contextual_v1"
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
    for item in translations:
        if not isinstance(item, dict) or set(item) != {"revision_key", "source", "target"} or any(not isinstance(item.get(key), str) for key in item):
            raise ContractError("contextual envelope translation_snapshot must be an exact string-object array")
    for item in contexts:
        if not isinstance(item, dict) or set(item) != {"revision_key", "context"} or any(not isinstance(item.get(key), str) for key in item):
            raise ContractError("contextual envelope bounded_context must be an exact string-object array")
    if [item["revision_key"] for item in translations] != keys or [item["revision_key"] for item in contexts] != keys:
        raise ContractError("contextual envelope revision-key arrays must match ordered_revision_keys")
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContractError(f"contextual envelope payload is not canonicalizable: {error}") from error


def _has_completion_indicator(record: dict[str, Any]) -> bool:
    present = [key for key in ("status", "result") if key in record]
    return bool(present) and all(
        isinstance(record[key], str) and record[key] in COMPLETION_VALUES for key in present
    )


def _candidate_bindings_valid(
    state: dict[str, Any], records: list[tuple[dict[str, Any], dict[str, Any], Path]]
) -> tuple[bool, str]:
    required = (
        "task_id", "review_contract", "review_phase", "cycle", "attempt",
        "reviewer_role", "purpose", "agent_id", "dispatch_id",
    )
    for record, dispatch, path in records:
        relative = path.relative_to(ROOT)
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
        if record.get("purpose") == "translation_contextual_v1":
            identity, input_path = record.get("candidate_identity"), record.get("input_path")
            if not isinstance(identity, str) or not SHA256.fullmatch(identity) or not isinstance(input_path, str):
                return False, f"{relative} lacks a valid contextual identity or input_path"
            if identity != dispatch.get("candidate_identity") or input_path != dispatch.get("input_path"):
                return False, f"{relative} contextual binding does not match its dispatch"
            envelope = _read_json(_ordinary_workspace_file(input_path, "contextual input_path"), "contextual envelope")
            if not isinstance(envelope, dict) or envelope.get("candidate_identity") != identity or "payload" not in envelope:
                return False, f"{relative} contextual envelope does not match candidate_identity"
            if hashlib.sha256(_canonical_payload_bytes(envelope["payload"])).hexdigest() != identity:
                return False, f"{relative} contextual candidate_identity does not match payload"
            continue
        locator = record.get("candidate_locator")
        if not isinstance(locator, dict) or set(locator) != {"spec_path", "diff_path"}:
            return False, f"{relative} candidate_locator must have exactly spec_path and diff_path"
        spec = _ordinary_workspace_file(locator["spec_path"], "candidate_locator.spec_path")
        diff = _ordinary_workspace_file(locator["diff_path"], "candidate_locator.diff_path")
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


def _sidecar_path(spec: Path) -> tuple[Path, str]:
    path = spec.parent / "EVIDENCE-RECONCILIATION.json"
    try:
        relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
    except (OSError, ValueError) as error:
        raise InputError(f"sidecar path escapes the workspace: {path}") from error
    return path, relative


def _read_sidecar_on_disk(path: Path) -> bytes:
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise InputError(f"evidence reconciliation sidecar is not present: {path}") from error
    try:
        resolved.relative_to(ROOT.resolve())
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
) -> tuple[bool, str]:
    code_records = [
        item for item in completed
        if item[0].get("purpose") in {"normal_review", "cross_review"}
    ]
    frozen: list[tuple[dict[str, Any], Path, bytes, bytes]] = []
    for record, _, record_path in code_records:
        relative = record_path.relative_to(ROOT)
        locator = record.get("candidate_locator")
        if not isinstance(locator, dict):
            return False, f"{relative} has no candidate_locator for evidence checking"
        spec = _ordinary_workspace_file(locator["spec_path"], "candidate_locator.spec_path")
        diff = _ordinary_workspace_file(locator["diff_path"], "candidate_locator.diff_path")
        sidecar, sidecar_relative = _sidecar_path(spec)
        embedded = _new_file_entry_bytes(_read_candidate_bytes(diff, "candidate diff"), sidecar_relative)
        if embedded is None:
            continue
        evidence_result = review_evidence.check_reconciliation(embedded, root=ROOT)
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
        frozen.append((record, sidecar, embedded, _read_sidecar_on_disk(sidecar)))

    if frozen:
        latest_key = max((item[0]["cycle"], item[0]["attempt"]) for item in frozen)
        latest = [item for item in frozen if (item[0]["cycle"], item[0]["attempt"]) == latest_key]
        if len({item[1] for item in latest}) != 1:
            return False, "bound records at the latest (cycle, attempt) derive different sidecar paths"
        if any(item[2] != latest[0][2] for item in latest[1:]):
            return False, "bound records at the latest (cycle, attempt) disagree on embedded sidecar bytes"
        if latest[0][2] != latest[0][3]:
            return False, f"{latest[0][1].relative_to(ROOT)}: on-disk sidecar does not match the latest bound embedded copy"

    schema_version = state.get("schema_version")
    if (
        type(schema_version) is int
        and schema_version >= 3
        and state.get("change_class") not in {"standard", "translation_workflow", "infrastructure"}
    ):
        return False, "change_class must be one of standard, translation_workflow, infrastructure"

    if (
        type(schema_version) is int
        and schema_version >= 3
        and state.get("mode") == "review_only"
        and state.get("change_class") in {"infrastructure", "translation_workflow"}
        and (not code_records or len(frozen) != len(code_records))
    ):
        return False, "evidence_reconciliation_required"

    if type(schema_version) is int and schema_version >= 3:
        senior_paths = set(_record_paths_for_field(state, "senior_review_records"))
        for record, path in loaded:
            if path not in senior_paths or record.get("purpose") != "scope_audit":
                continue
            audit_result = review_evidence.check_audit(record, root=ROOT)
            if audit_result.exit_code:
                return False, f"{path.relative_to(ROOT)}: scope_audit: {audit_result.detail}"
    return True, "ok"


def _record_paths_for_field(state: dict[str, Any], field: str) -> list[Path]:
    value = state.get(field, [])
    if value is None:
        value = []
    if isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, list):
        return []
    return [
        _ordinary_workspace_file(item, f"{field}[{index}]")
        for index, item in enumerate(value)
    ]


def _reviewer_identity_valid(
    state: dict[str, Any], completed: list[tuple[dict[str, Any], dict[str, Any], Path]]
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
            return False, f"{path.relative_to(ROOT)} reviewer agent_id equals orchestrator_agent_id"
    return True, "ok"


def _children_archived(state: dict[str, Any]) -> tuple[bool, str]:
    children = state.get("child_dispatches")
    if not isinstance(children, list) or not children:
        return False, "child_dispatches cannot be null, absent, or empty with review contracts"
    if any(not isinstance(dispatch, dict) or not _archived(dispatch) for dispatch in children):
        return False, "every child dispatch must be archived and confirmed"
    return True, "ok"


def _done(state: dict[str, Any]) -> CheckResult:
    if not isinstance(state.get("task_id"), str) or not state["task_id"]:
        return _result("NEW_CONTRACT_FAILED", "schema_valid: task_id must be a non-empty string", 1)
    for name, check in (("schema_valid", _schema_valid(state)), ("review_contracts_closed", _review_contracts_closed(state))):
        if not check[0]:
            return _result("NEW_CONTRACT_FAILED", f"{name}: {check[1]}", 1)
    try:
        loaded = _load_records(state)
        completed = _completion_records(state, loaded)
        bindings = _candidate_bindings_valid(state, completed)
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"candidate_bindings_valid: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"candidate_bindings_valid: malformed JSON value ({error})", 1)
    for name, check in (("completion_records_bound", _completion_records_bound(state, completed)), ("candidate_bindings_valid", bindings)):
        if not check[0]:
            return _result("NEW_CONTRACT_FAILED", f"{name}: {check[1]}", 1)
    identity = _reviewer_identity_valid(state, completed)
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
        evidence = _evidence_checks(state, loaded, completed)
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", f"evidence_reconciliation: {error}", 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"evidence_reconciliation: malformed JSON value ({error})", 1)
    if not evidence[0]:
        return _result("NEW_CONTRACT_FAILED", f"evidence_reconciliation: {evidence[1]}", 1)
    archived = _children_archived(state)
    if not archived[0]:
        return _result("NEW_CONTRACT_FAILED", f"children_archived: {archived[1]}", 1)
    return _result("DONE_VERIFIED", "DONE predicate verified", 0)


def check_state(
    state_path: str | Path, *, target: str | None = None, manifest_path: str | Path | None = None
) -> CheckResult:
    """Check one STATE file and return a structured result without printing."""
    if target is not None and (not isinstance(target, str) or target not in {"DONE", "STOP"}):
        return _result("INPUT_ERROR", "target must be DONE or STOP", 2)
    try:
        state = _read_json(Path(state_path), "STATE")
    except InputError as error:
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
    return _done(state)


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
    try:
        args = parser.parse_args(argv)
    except InputError as error:
        result = _result("INPUT_ERROR", str(error), 2)
        print(f"{result.outcome}: {result.detail}")
        return result.exit_code
    result = check_state(args.state, target=args.target, manifest_path=args.manifest)
    print(f"{result.outcome}: {result.detail}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
