"""Small bounded evidence helpers for WP2-Lite.

The durable validator remains the existing queue replay; this module only keeps
path/byte checks shared by callers and tests, avoiding a second evidence store.
"""
from __future__ import annotations
import base64
import hashlib
import os
import stat
import subprocess
from pathlib import Path
from typing import Iterable

from . import production_review as wp1

CORE_FILES = ("manifest.json", "results.jsonl", "adjudications.jsonl", "gates.json")
MAX_TRACKED_BYTES = 128 * 1024 * 1024
PRODUCTION_PREFIXES = (
    "evidence/production-review/",
    "i18n/quality/production-review/",
    "evidence/production-review-v2-lite/",
    "i18n/quality/production-review-v2-lite/",
)
BATCH_PREFIX = "evidence/production-review-v2-lite/batches/"


def batch_relative_path(batch_id: object, *parts: str) -> str:
    """Build the one canonical repository-relative path for a batch item."""
    if (not isinstance(batch_id, str) or not batch_id or batch_id in {".", ".."}
            or "/" in batch_id or "\\" in batch_id
            or batch_id != Path(batch_id).name):
        raise wp1.ProductionReviewError("batch_id is not a single path component")
    result = [BATCH_PREFIX.rstrip("/"), batch_id]
    for part in parts:
        if (not isinstance(part, str) or not part or part in {".", ".."}
                or "/" in part or "\\" in part):
            raise wp1.ProductionReviewError("batch-relative path component is not canonical")
        result.append(part)
    return "/".join(result)


def snapshot_content_bytes(snapshot: object) -> bytes:
    """Decode and verify a self-contained source snapshot."""
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("sha256"), str):
        raise wp1.ProductionReviewError("source snapshot must carry retrievable content bytes")
    digest = snapshot["sha256"]
    if not wp1.SHA256_RE.fullmatch(digest):
        raise wp1.ProductionReviewError("source snapshot SHA-256 is invalid")
    if set(snapshot) == {"sha256", "content"} and isinstance(snapshot["content"], str):
        raw = snapshot["content"].encode("utf-8")
    elif (set(snapshot) == {"sha256", "content_base64"}
          and isinstance(snapshot["content_base64"], str)):
        try:
            raw = base64.b64decode(snapshot["content_base64"], validate=True)
        except (ValueError, TypeError, base64.binascii.Error) as error:
            raise wp1.ProductionReviewError("source snapshot content_base64 is invalid") from error
    else:
        raise wp1.ProductionReviewError("source snapshot must contain exact content bytes")
    if hashlib.sha256(raw).hexdigest() != digest:
        raise wp1.ProductionReviewError("source snapshot content SHA-256 mismatch")
    return raw


def validate_source_evidence(root: Path, evidence_path: object,
                             evidence_commit: object, evidence_snapshot: object,
                             *, allow_legacy_annotation: bool = False) -> None:
    """Validate the one source-evidence grammar used by producers and replay."""
    if evidence_commit is not None or evidence_path is not None:
        if (not isinstance(evidence_path, str) or not evidence_path or
                evidence_path.startswith("/") or ".." in Path(evidence_path).parts or
                not isinstance(evidence_commit, str)):
            raise wp1.ProductionReviewError("source evidence must use a normalized repository path and commit")
        commit = evidence_commit[7:] if evidence_commit.startswith("commit:") else evidence_commit
        if (len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit) or
                wp1.surface.normalize_relative_path(evidence_path) != evidence_path):
            raise wp1.ProductionReviewError("source evidence path/commit is not normalized")
        try:
            kind = subprocess.run(["git", "cat-file", "-t", commit], cwd=root, check=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()
            blob = subprocess.run(["git", "cat-file", "-t", f"{commit}:{evidence_path}"], cwd=root,
                                  check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as error:
            raise wp1.ProductionReviewError("source evidence commit/blob cannot be verified") from error
        if kind != b"commit" or blob != b"blob":
            raise wp1.ProductionReviewError("source evidence is not a commit/blob")
        if evidence_snapshot is not None:
            # A self-contained snapshot is safe alongside a public Git
            # locator only when it is the content of that exact blob.  A
            # correctly self-hashed but unrelated snapshot is not evidence for
            # the named source location.
            if isinstance(evidence_snapshot, dict):
                snapshot_raw = snapshot_content_bytes(evidence_snapshot)
                try:
                    source_raw = subprocess.run(
                        ["git", "cat-file", "blob", f"{commit}:{evidence_path}"],
                        cwd=root, check=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE).stdout
                except (OSError, subprocess.CalledProcessError) as error:
                    raise wp1.ProductionReviewError("source evidence blob cannot be read") from error
                if snapshot_raw != source_raw:
                    raise wp1.ProductionReviewError("source snapshot does not match the named commit/blob")
            elif not allow_legacy_annotation:
                raise wp1.ProductionReviewError("source evidence snapshot must carry exact content bytes")
        return
    if isinstance(evidence_snapshot, dict):
        snapshot_content_bytes(evidence_snapshot)
        return
    raise wp1.ProductionReviewError("confirmed source evidence is required")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def ordinary_files(root: Path) -> dict[str, bytes]:
    if root.is_symlink() or not root.is_dir():
        raise wp1.ProductionReviewError("evidence root is not an ordinary directory")
    found: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode) or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise wp1.ProductionReviewError(f"evidence contains symlink/special path: {path}")
        if stat.S_ISREG(mode):
            found[path.relative_to(root).as_posix()] = path.read_bytes()
    return found


def require_core(files: dict[str, bytes]) -> None:
    missing = [name for name in CORE_FILES if name not in files]
    extra = [name for name in files if name in CORE_FILES and not isinstance(files[name], bytes)]
    if missing or extra:
        raise wp1.ProductionReviewError(f"evidence core file set mismatch: missing={missing}, extra={extra}")


def prospective_bytes(files: Iterable[bytes]) -> int:
    total = sum(len(value) for value in files)
    if total > MAX_TRACKED_BYTES:
        raise wp1.ProductionReviewError("prospective tracked evidence exceeds 128 MiB")
    return total


def prospective_tracked_bytes(root: Path, candidate_root: Path) -> int:
    """Compute conservative current production plus candidate occupancy.

    Index blobs and ordinary worktree files are both inspected.  For the same
    path the larger byte count wins, so a staged large blob cannot be hidden by
    a smaller worktree copy; untracked production files are walked directly.
    """
    existing_sizes: dict[str, int] = {}

    def production(path: str) -> bool:
        return any(path.startswith(prefix) for prefix in PRODUCTION_PREFIXES)

    def add(path: str, size: int) -> None:
        if not production(path):
            return
        if size < 0:
            raise ValueError("negative production file size")
        existing_sizes[path] = max(existing_sizes.get(path, 0), size)

    try:
        staged = subprocess.run(["git", "ls-files", "--stage", "-z", "--",
                                 "evidence/production-review", "i18n/quality/production-review",
                                 "evidence/production-review-v2-lite", "i18n/quality/production-review-v2-lite"],
                                cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        for record in staged.split(b"\0"):
            if not record:
                continue
            metadata, path_raw = record.split(b"\t", 1)
            mode_raw, object_raw, stage_raw = metadata.split()
            path = path_raw.decode("utf-8")
            if stage_raw != b"0" or mode_raw not in {b"100644", b"100755"}:
                raise ValueError("ambiguous or non-ordinary staged production entry")
            size = subprocess.run(["git", "cat-file", "-s", object_raw.decode("ascii")], cwd=root,
                                  check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
            add(path, int(size))

        # Walk actual production roots, including untracked files that Git may
        # omit from ``ls-files`` because of an ignore rule.
        for prefix in PRODUCTION_PREFIXES:
            directory = root / prefix.rstrip("/")
            if not directory.exists() and not directory.is_symlink():
                continue
            if directory.is_symlink() or not directory.is_dir():
                raise ValueError("production root is not an ordinary directory")
            for item in directory.rglob("*"):
                mode = item.lstat().st_mode
                if stat.S_ISLNK(mode) or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                    raise ValueError("non-ordinary production worktree entry")
                if stat.S_ISREG(mode):
                    add(item.relative_to(root).as_posix(), item.stat().st_size)

        # An unstaged deletion has no unambiguous prospective bytes.  A staged
        # deletion is intentional and contributes zero bytes.
        status = subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all", "--",
                                 "evidence/production-review", "i18n/quality/production-review",
                                 "evidence/production-review-v2-lite", "i18n/quality/production-review-v2-lite"],
                                cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        fields = status.split(b"\0")
        index = 0
        while index < len(fields) and fields[index]:
            record = fields[index]
            if len(record) < 4:
                raise ValueError("malformed production status")
            state = record[:2]
            record[3:].decode("utf-8")
            if "U" in state.decode("ascii", "replace"):
                raise ValueError("unmerged production worktree state")
            if state[1:2] == b"D" and state[:1] == b" ":
                raise ValueError("unstaged production deletion is ambiguous")
            index += 1
            if state[:1] in {b"R", b"C"}:
                if index >= len(fields) or not fields[index]:
                    raise ValueError("malformed production rename status")
                index += 1
        if index != len(fields) - 1:
            raise ValueError("malformed production status termination")
    except (OSError, subprocess.CalledProcessError, ValueError, UnicodeDecodeError) as error:
        raise wp1.ProductionReviewError(f"cannot enumerate actual production tree: {error}") from error

    candidate = ordinary_files(candidate_root)
    batch_id = candidate_root.name
    candidate_paths = {batch_relative_path(batch_id, *Path(path).parts) for path in candidate}
    if any(tracked == proposed or tracked.startswith(proposed + "/") or proposed.startswith(tracked + "/")
           for tracked in existing_sizes for proposed in candidate_paths):
        raise wp1.ProductionReviewError("prospective evidence collides with tracked paths")
    total = sum(existing_sizes.values()) + sum(len(raw) for raw in candidate.values())
    if total > MAX_TRACKED_BYTES:
        raise wp1.ProductionReviewError(f"prospective tracked evidence exceeds 128 MiB (bytes={total})")
    return total
