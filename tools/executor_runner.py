#!/usr/bin/env python3
"""Fail-closed, target-bounded EXECUTOR apply and recovery runner."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Optional

ENVELOPE_VERSION = "bounded_apply_v1"
JOURNAL_VERSION = "bounded_apply_journal_v1"
PREPARATION_VERSION = "bounded_apply_preparation_v1"
JOURNAL_STATUSES = {"PREPARED", "APPLYING", "COMMITTED", "ROLLING_BACK", "ROLLED_BACK", "ROLLBACK_CONFLICT"}
PRIVILEGED_TARGET_ROOTS = {".git", ".ai", ".artifacts"}
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", re.ASCII)
HASH_RE = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
JOURNAL_KEYS = {"schema_version", "workspace_id", "dispatch_id", "envelope_hash", "candidate_id", "status", "ordered_paths", "applied_paths", "preimages", "postimages"}


def _validate_canonical_types(data: Any) -> None:
    if data is None or type(data) in (bool, int, str):
        return
    if isinstance(data, float):
        raise ValueError("canonical-json-v1 does not support floats")
    if isinstance(data, list):
        for value in data:
            _validate_canonical_types(value)
        return
    if isinstance(data, dict):
        for key, value in data.items():
            if type(key) is not str:
                raise ValueError("canonical-json-v1 dict keys must be strings")
            _validate_canonical_types(value)
        return
    raise ValueError(f"canonical-json-v1 unsupported type: {type(data)}")


def canonical_json(data: Any) -> bytes:
    _validate_canonical_types(data)
    return json.dumps(data, allow_nan=False, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def compute_hash(data: Any) -> str:
    return hashlib.sha256(canonical_json(data)).hexdigest()


def validate_identifier(identifier: Any, name: str) -> None:
    if type(identifier) is not str or IDENTIFIER_RE.fullmatch(identifier) is None:
        raise ValueError(f"invalid {name}: expected an ASCII identifier")


def validate_hash(value: Any, name: str) -> None:
    if type(value) is not str or HASH_RE.fullmatch(value) is None:
        raise ValueError(f"invalid {name}: expected 64 lowercase hex characters")


def validate_path_str(path_str: Any) -> None:
    if type(path_str) is not str:
        raise ValueError("path must be a string")
    if not path_str or "\0" in path_str:
        raise ValueError("path must be non-empty and contain no NUL")
    if os.path.isabs(path_str):
        raise ValueError("absolute paths are not allowed")
    raw_parts = path_str.split("/")
    if any(part == "" for part in raw_parts):
        raise ValueError("empty path components are not allowed")
    if any(part in (".", "..") for part in raw_parts):
        raise ValueError("dot path components are not allowed")
    if PurePosixPath(path_str).as_posix() != path_str:
        raise ValueError("path must use its unique canonical POSIX form")


def validate_target_path(path_str: Any) -> None:
    validate_path_str(path_str)
    if Path(path_str).parts[0] in PRIVILEGED_TARGET_ROOTS:
        raise ValueError(f"privileged target namespace is not allowed: {path_str}")


def validate_target_path_set(paths: list[str], name: str) -> None:
    for path in paths:
        validate_target_path(path)
    components = [(path, PurePosixPath(path).parts) for path in paths]
    for index, (path, parts) in enumerate(components):
        for other_path, other_parts in components[index + 1:]:
            shorter, longer = (parts, other_parts) if len(parts) < len(other_parts) else (other_parts, parts)
            if len(shorter) < len(longer) and longer[:len(shorter)] == shorter:
                raise ValueError(f"{name} paths must not overlap as ancestor and descendant: {path}, {other_path}")


def canonical_applied_paths(ordered: list[str], applied: list[str]) -> list[str]:
    if type(applied) is not list or any(type(path) is not str for path in applied):
        raise ValueError("journal applied_paths must be list[str]")
    if len(applied) != len(set(applied)):
        raise ValueError("journal applied_paths must not contain duplicates")
    unknown = set(applied) - set(ordered)
    if unknown:
        raise ValueError("journal applied_paths must not contain unknown paths")
    applied_set = set(applied)
    return [path for path in ordered if path in applied_set]


def _strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def load_json_strict(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8"),
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON file {path}: {exc}") from exc


def _fsync_directory(directory: Path) -> None:
    fd = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _atomic_replace_bytes(path: Path, content: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb", closefd=True) as stream:
            stream.write(content)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        os.replace(temp_path, path)
        _fsync_directory(path.parent)
    except BaseException:
        # mkstemp proved that this exact temp belongs to this call and parent.
        temp_path.unlink(missing_ok=True)
        raise


def _read_bytes_preserving_mode(path: Path) -> bytes:
    """Read an owned ordinary file without depending on its declared read bits."""
    original_mode = path.stat().st_mode & 0o777
    fd: Optional[int] = None
    widened = not original_mode & 0o400
    try:
        try:
            if widened:
                path.chmod(original_mode | 0o400)
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        finally:
            if widened:
                path.chmod(original_mode)
    except BaseException:
        if fd is not None:
            os.close(fd)
        raise
    if fd is None:
        raise OSError(f"failed to open file for verification: {path}")
    try:
        stream = os.fdopen(fd, "rb", closefd=True)
        fd = None
        with stream:
            content = stream.read()
    finally:
        if fd is not None:
            os.close(fd)
    if path.stat().st_mode & 0o777 != original_mode:
        raise OSError(f"file mode changed during verification: {path}")
    return content


def _unlink_durable(path: Path) -> None:
    path.unlink()
    _fsync_directory(path.parent)


def write_atomic_json(path: Path, data: Any) -> None:
    if type(data) is not dict or set(data) != JOURNAL_KEYS:
        raise ValueError("journal schema mismatch")
    _atomic_replace_bytes(path, canonical_json(data), 0o600)


def safe_resolve(base: Path, sub: str, *, target_file: bool = False) -> Path:
    validate_path_str(sub)
    resolved_base = base.resolve(strict=True)
    current = resolved_base
    for part in Path(sub).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink path component is not allowed: {sub}")
    resolved = current.resolve(strict=False)
    if os.path.commonpath((str(resolved_base), str(resolved))) != str(resolved_base):
        raise ValueError(f"path escapes its root: {sub}")
    if resolved.exists() and not resolved.is_file() and not resolved.is_dir():
        raise ValueError(f"special file is not allowed: {sub}")
    if target_file and resolved.exists() and not resolved.is_file():
        raise ValueError(f"target must be an ordinary file or absent: {sub}")
    return resolved


def verify_image(path: Path, expected: dict[str, Any]) -> bool:
    if expected["state"] == "absent":
        return not path.exists() and not path.is_symlink()
    if not path.exists() or path.is_symlink() or not path.is_file():
        return False
    if path.stat().st_mode & 0o777 != expected["mode"]:
        return False
    return hashlib.sha256(_read_bytes_preserving_mode(path)).hexdigest() == expected["sha256"]


class BoundedExecutor:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve(strict=True)
        self.artifacts_dir = self.repo_root / ".artifacts" / "paseo-bounded"

    def _transaction_root(self, workspace_id: str, dispatch_id: str) -> Path:
        validate_identifier(workspace_id, "workspace_id")
        validate_identifier(dispatch_id, "dispatch_id")
        relative = f".artifacts/paseo-bounded/{workspace_id}/{dispatch_id}"
        root = safe_resolve(self.repo_root, relative)
        if root.exists() and not root.is_dir():
            raise ValueError("transaction artifact root must be a directory or absent")
        return root

    def _ledger_path(self, workspace_id: str, dispatch_id: str) -> Path:
        return self._transaction_root(workspace_id, dispatch_id) / "journal.json"

    def _preparation_path(self, workspace_id: str, dispatch_id: str) -> Path:
        return self._transaction_root(workspace_id, dispatch_id) / "preparation.json"

    def _shadow_path(self, workspace_id: str, dispatch_id: str) -> Path:
        return self._transaction_root(workspace_id, dispatch_id) / "shadow"

    def _artifact_path(self, workspace_id: str, dispatch_id: str, kind: str, target_path: str) -> Path:
        if kind not in ("post", "pre"):
            raise ValueError("invalid artifact kind")
        validate_path_str(target_path)
        name = hashlib.sha256(target_path.encode("utf-8")).hexdigest()
        root = self._shadow_path(workspace_id, dispatch_id) / kind
        relative = root.relative_to(self.repo_root) / name
        artifact = safe_resolve(self.repo_root, relative.as_posix())
        return artifact

    def get_ledger(self, workspace_id: str, dispatch_id: str) -> Optional[dict[str, Any]]:
        path = self._ledger_path(workspace_id, dispatch_id)
        if path.is_symlink():
            raise ValueError("journal must not be a symlink")
        if not path.exists():
            return None
        if not path.is_file():
            raise ValueError("journal must be an ordinary file")
        journal = load_json_strict(path)
        self._validate_journal(journal)
        if journal["workspace_id"] != workspace_id or journal["dispatch_id"] != dispatch_id:
            raise ValueError("journal identity does not match its artifact path")
        return journal

    @staticmethod
    def _validate_mode(mode: Any) -> None:
        if type(mode) is not int or not 0 <= mode <= 0o777:
            raise ValueError("mode must be an integer in range 0..0o777")

    def _validate_image_schema(self, image: Any, *, edit: bool = False) -> None:
        if type(image) is not dict or image.get("state") not in ("file", "absent"):
            raise ValueError("image must be an exact file or absent object")
        if image["state"] == "absent":
            if set(image) != {"state"}:
                raise ValueError("absent image has extra or missing keys")
            return
        expected = {"state", "content_base64", "mode"} if edit else {"state", "sha256", "mode"}
        if set(image) != expected:
            raise ValueError("file image has extra or missing keys")
        self._validate_mode(image["mode"])
        if edit:
            if type(image["content_base64"]) is not str:
                raise ValueError("content_base64 must be a string")
            try:
                base64.b64decode(image["content_base64"], validate=True)
            except (ValueError, base64.binascii.Error) as exc:
                raise ValueError("content_base64 is not strict base64") from exc
        else:
            validate_hash(image["sha256"], "sha256")

    def _validate_envelope(self, envelope: Any) -> None:
        keys = {"envelope_version", "task_id", "dispatch_id", "workspace_id", "parent_lineage", "base_revision", "candidate", "preimages", "postimages", "gates", "retry_of", "envelope_hash"}
        if type(envelope) is not dict or set(envelope) != keys:
            raise ValueError("envelope schema mismatch")
        if envelope["envelope_version"] != ENVELOPE_VERSION:
            raise ValueError("unsupported envelope_version")
        for field in ("task_id", "dispatch_id", "workspace_id"):
            validate_identifier(envelope[field], field)
        validate_hash(envelope["envelope_hash"], "envelope_hash")
        if type(envelope["base_revision"]) is not str or re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", envelope["base_revision"], re.ASCII) is None:
            raise ValueError("base_revision must be 40 or 64 lowercase hex characters")
        if type(envelope["parent_lineage"]) is not list:
            raise ValueError("parent_lineage must be list[str]")
        for item in envelope["parent_lineage"]:
            validate_identifier(item, "parent_lineage item")
        if envelope["retry_of"] is not None:
            validate_identifier(envelope["retry_of"], "retry_of")
        if type(envelope["gates"]) is not list or any(type(x) is not str for x in envelope["gates"]):
            raise ValueError("gates must be list[str]")

        candidate = envelope["candidate"]
        if type(candidate) is not dict or set(candidate) != {"candidate_id", "author", "allowed_paths", "edits", "invariants"}:
            raise ValueError("candidate schema mismatch")
        validate_hash(candidate["candidate_id"], "candidate_id")
        author = candidate["author"]
        if type(author) is not dict or set(author) != {"role", "dispatch_id"}:
            raise ValueError("candidate author schema mismatch")
        if type(author["role"]) is not str or author["role"] not in {"ORCHESTRATOR", "EXECUTOR"}:
            raise ValueError("candidate author role must be ORCHESTRATOR or EXECUTOR")
        validate_identifier(author["dispatch_id"], "candidate author dispatch_id")
        allowed = candidate["allowed_paths"]
        if type(allowed) is not list or any(type(path) is not str for path in allowed):
            raise ValueError("allowed_paths must be list[str]")
        if not allowed or len(allowed) != len(set(allowed)):
            raise ValueError("allowed_paths must be non-empty and unique")
        validate_target_path_set(allowed, "allowed_paths")
        if type(candidate["invariants"]) is not list or any(type(item) is not str for item in candidate["invariants"]):
            raise ValueError("invariants must be list[str]")
        for mapping_name in ("edits", "preimages", "postimages"):
            mapping = candidate["edits"] if mapping_name == "edits" else envelope[mapping_name]
            if type(mapping) is not dict or set(mapping) != set(allowed):
                raise ValueError(f"{mapping_name} paths must exactly match allowed_paths")
            for path, image in mapping.items():
                if type(path) is not str:
                    raise ValueError(f"{mapping_name} paths must be strings")
                self._validate_image_schema(image, edit=mapping_name == "edits")

    def _validate_runtime_context(self, context: Any) -> None:
        keys = {"task_id", "workspace_id", "parent_lineage", "base_revision", "archive_receipts"}
        if type(context) is not dict or set(context) != keys:
            raise ValueError("runtime_context schema mismatch")
        validate_identifier(context["task_id"], "runtime task_id")
        validate_identifier(context["workspace_id"], "runtime workspace_id")
        if type(context["parent_lineage"]) is not list:
            raise ValueError("runtime parent_lineage must be list[str]")
        for item in context["parent_lineage"]:
            validate_identifier(item, "runtime parent_lineage item")
        if type(context["base_revision"]) is not str or re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", context["base_revision"], re.ASCII) is None:
            raise ValueError("runtime base_revision is invalid")
        receipts = context["archive_receipts"]
        if type(receipts) is not list:
            raise ValueError("archive_receipts must be a list")
        receipt_keys = {"task_id", "workspace_id", "dispatch_id", "candidate_id", "archive_confirmed"}
        for receipt in receipts:
            if type(receipt) is not dict or set(receipt) != receipt_keys:
                raise ValueError("archive receipt schema mismatch")
            for field in ("task_id", "workspace_id", "dispatch_id"):
                validate_identifier(receipt[field], f"archive receipt {field}")
            validate_hash(receipt["candidate_id"], "archive receipt candidate_id")
            if type(receipt["archive_confirmed"]) is not bool:
                raise ValueError("archive_confirmed must be a boolean")

    def _validate_journal(self, journal: Any, envelope: Optional[dict[str, Any]] = None) -> None:
        if type(journal) is not dict or set(journal) != JOURNAL_KEYS:
            raise ValueError("journal schema mismatch")
        if journal["schema_version"] != JOURNAL_VERSION:
            raise ValueError("unsupported journal schema_version")
        validate_identifier(journal["workspace_id"], "journal workspace_id")
        validate_identifier(journal["dispatch_id"], "journal dispatch_id")
        validate_hash(journal["envelope_hash"], "journal envelope_hash")
        validate_hash(journal["candidate_id"], "journal candidate_id")
        if type(journal["status"]) is not str or journal["status"] not in JOURNAL_STATUSES:
            raise ValueError("invalid journal status")
        ordered, applied = journal["ordered_paths"], journal["applied_paths"]
        if type(ordered) is not list or any(type(x) is not str for x in ordered) or not ordered or len(ordered) != len(set(ordered)):
            raise ValueError("journal ordered_paths must be a non-empty unique list[str]")
        validate_target_path_set(ordered, "journal ordered_paths")
        if applied != canonical_applied_paths(ordered, applied):
            raise ValueError("journal applied_paths must be a unique ordered subset")
        for name in ("preimages", "postimages"):
            images = journal[name]
            if type(images) is not dict or set(images) != set(ordered):
                raise ValueError(f"journal {name} paths mismatch")
            for image in images.values():
                self._validate_image_schema(image)
        if journal["status"] == "PREPARED" and applied:
            raise ValueError("PREPARED journal cannot contain applied paths")
        if journal["status"] == "COMMITTED" and applied != ordered:
            raise ValueError("COMMITTED journal must contain every ordered path")
        if journal["status"] == "ROLLED_BACK" and applied:
            raise ValueError("ROLLED_BACK journal cannot contain applied paths")
        if envelope is not None:
            expected = {"workspace_id": envelope["workspace_id"], "dispatch_id": envelope["dispatch_id"], "envelope_hash": envelope["envelope_hash"], "candidate_id": envelope["candidate"]["candidate_id"], "ordered_paths": envelope["candidate"]["allowed_paths"], "preimages": envelope["preimages"], "postimages": envelope["postimages"]}
            for field, value in expected.items():
                if journal[field] != value:
                    raise ValueError(f"journal {field} does not match envelope")

    def _verify_git_head(self, expected_revision: str) -> None:
        try:
            actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo_root, stderr=subprocess.STDOUT, text=True).strip()
        except subprocess.CalledProcessError as exc:
            raise ValueError("git rev-parse HEAD failed") from exc
        if actual != expected_revision:
            raise ValueError("git HEAD does not match base_revision")

    @staticmethod
    def _decoded_edits(envelope: dict[str, Any]) -> dict[str, Optional[tuple[bytes, int]]]:
        decoded: dict[str, Optional[tuple[bytes, int]]] = {}
        for path in envelope["candidate"]["allowed_paths"]:
            edit, post = envelope["candidate"]["edits"][path], envelope["postimages"][path]
            if edit["state"] != post["state"]:
                raise ValueError(f"edit/postimage state mismatch for {path}")
            if edit["state"] == "absent":
                decoded[path] = None
                continue
            content = base64.b64decode(edit["content_base64"], validate=True)
            if hashlib.sha256(content).hexdigest() != post["sha256"] or edit["mode"] != post["mode"]:
                raise ValueError(f"edit bytes/mode do not match postimage for {path}")
            decoded[path] = (content, edit["mode"])
        return decoded

    def _journal_factory(self, envelope: dict[str, Any]) -> Callable[[str, list[str]], dict[str, Any]]:
        ordered = list(envelope["candidate"]["allowed_paths"])

        def make(status: str, applied: list[str]) -> dict[str, Any]:
            return {"schema_version": JOURNAL_VERSION, "workspace_id": envelope["workspace_id"], "dispatch_id": envelope["dispatch_id"], "envelope_hash": envelope["envelope_hash"], "candidate_id": envelope["candidate"]["candidate_id"], "status": status, "ordered_paths": ordered, "applied_paths": canonical_applied_paths(ordered, applied), "preimages": envelope["preimages"], "postimages": envelope["postimages"]}
        return make

    def _verify_artifacts(self, envelope: dict[str, Any]) -> None:
        workspace, dispatch = envelope["workspace_id"], envelope["dispatch_id"]
        for path in envelope["candidate"]["allowed_paths"]:
            if envelope["postimages"][path]["state"] == "file" and not verify_image(self._artifact_path(workspace, dispatch, "post", path), envelope["postimages"][path]):
                raise ValueError(f"post shadow artifact mismatch for {path}")
            if envelope["preimages"][path]["state"] == "file" and not verify_image(self._artifact_path(workspace, dispatch, "pre", path), envelope["preimages"][path]):
                raise ValueError(f"preimage snapshot artifact mismatch for {path}")

    @staticmethod
    def _preparation_identity(envelope: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema_version": PREPARATION_VERSION,
            "workspace_id": envelope["workspace_id"],
            "dispatch_id": envelope["dispatch_id"],
            "envelope_hash": envelope["envelope_hash"],
            "candidate_id": envelope["candidate"]["candidate_id"],
        }

    def _validate_preparation_tree(self, envelope: dict[str, Any]) -> None:
        workspace, dispatch = envelope["workspace_id"], envelope["dispatch_id"]
        root = self._transaction_root(workspace, dispatch)
        expected_files = {Path("preparation.json")}
        expected_dirs = {Path("shadow"), Path("shadow/pre"), Path("shadow/post")}
        for path in envelope["candidate"]["allowed_paths"]:
            name = hashlib.sha256(path.encode("utf-8")).hexdigest()
            if envelope["preimages"][path]["state"] == "file":
                expected_files.add(Path("shadow/pre") / name)
            if envelope["postimages"][path]["state"] == "file":
                expected_files.add(Path("shadow/post") / name)

        for current, dir_names, file_names in os.walk(root, followlinks=False):
            current_path = Path(current)
            for name in dir_names:
                entry = current_path / name
                relative = entry.relative_to(root)
                if entry.is_symlink() or relative not in expected_dirs:
                    raise ValueError(f"unknown preparation artifact: {relative.as_posix()}")
            for name in file_names:
                entry = current_path / name
                relative = entry.relative_to(root)
                if entry.is_symlink() or not entry.is_file() or relative not in expected_files:
                    raise ValueError(f"unknown preparation artifact: {relative.as_posix()}")

        identity_path = self._preparation_path(workspace, dispatch)
        if not identity_path.is_file() or identity_path.is_symlink():
            raise ValueError("journal-less preparation lacks an ordinary identity file")
        if identity_path.stat().st_mode & 0o777 != 0o600:
            raise ValueError("journal-less preparation identity mode mismatch")
        identity = load_json_strict(identity_path)
        if identity != self._preparation_identity(envelope):
            raise ValueError("journal-less preparation identity mismatch")

        for path in envelope["candidate"]["allowed_paths"]:
            for kind, images in (("post", envelope["postimages"]), ("pre", envelope["preimages"])):
                artifact = self._artifact_path(workspace, dispatch, kind, path)
                if artifact.exists() or artifact.is_symlink():
                    if not verify_image(artifact, images[path]):
                        raise ValueError(f"existing {kind} artifact mismatch for {path}")

    def _prepare_artifacts(self, envelope: dict[str, Any], decoded: dict[str, Optional[tuple[bytes, int]]]) -> None:
        workspace, dispatch = envelope["workspace_id"], envelope["dispatch_id"]
        root = self._transaction_root(workspace, dispatch)
        if root.exists():
            self._validate_preparation_tree(envelope)
        else:
            identity = self._preparation_identity(envelope)
            _atomic_replace_bytes(self._preparation_path(workspace, dispatch), canonical_json(identity), 0o600)
        for path in envelope["candidate"]["allowed_paths"]:
            post = decoded[path]
            if post is not None:
                artifact = self._artifact_path(workspace, dispatch, "post", path)
                if not artifact.exists():
                    _atomic_replace_bytes(artifact, post[0], post[1])
            pre = envelope["preimages"][path]
            if pre["state"] == "file":
                target = safe_resolve(self.repo_root, path, target_file=True)
                artifact = self._artifact_path(workspace, dispatch, "pre", path)
                if not artifact.exists():
                    _atomic_replace_bytes(artifact, _read_bytes_preserving_mode(target), pre["mode"])
        self._verify_artifacts(envelope)

    def _reconcile(self, envelope: dict[str, Any], ledger_path: Path, make_journal: Callable[[str, list[str]], dict[str, Any]], status: str) -> list[str]:
        applied: list[str] = []
        conflicts: list[str] = []
        for path in envelope["candidate"]["allowed_paths"]:
            target = safe_resolve(self.repo_root, path, target_file=True)
            is_pre = verify_image(target, envelope["preimages"][path])
            is_post = verify_image(target, envelope["postimages"][path])
            if is_post and not is_pre:
                applied.append(path)
            elif is_pre and not is_post:
                continue
            else:
                conflicts.append(path)
        if conflicts:
            write_atomic_json(ledger_path, make_journal("ROLLBACK_CONFLICT", applied))
            raise RuntimeError(
                "targets are neither unambiguous preimages nor postimages: "
                + ", ".join(conflicts)
            )
        write_atomic_json(ledger_path, make_journal(status, applied))
        return applied

    def apply(self, envelope: dict[str, Any], runtime_context: dict[str, Any]) -> str:
        self._validate_envelope(envelope)
        self._validate_runtime_context(runtime_context)
        candidate = envelope["candidate"]
        if compute_hash({k: v for k, v in candidate.items() if k != "candidate_id"}) != candidate["candidate_id"]:
            raise ValueError("candidate_id mismatch")
        if compute_hash({k: v for k, v in envelope.items() if k != "envelope_hash"}) != envelope["envelope_hash"]:
            raise ValueError("envelope_hash mismatch")
        for field in ("task_id", "workspace_id", "parent_lineage", "base_revision"):
            if runtime_context[field] != envelope[field]:
                raise ValueError(f"runtime {field} does not match envelope")
        self._verify_git_head(envelope["base_revision"])

        # This binding check is deliberately before any journal or target write.
        decoded = self._decoded_edits(envelope)
        for path in candidate["allowed_paths"]:
            if envelope["preimages"][path] == envelope["postimages"][path]:
                raise ValueError(f"ambiguous no-op target is not allowed: {path}")
        retry_of, receipts = envelope["retry_of"], runtime_context["archive_receipts"]
        if retry_of is not None:
            expected = {"task_id": envelope["task_id"], "workspace_id": envelope["workspace_id"], "dispatch_id": retry_of, "candidate_id": candidate["candidate_id"], "archive_confirmed": True}
            if not any(receipt == expected for receipt in receipts):
                raise ValueError("retry_of lacks a matching trusted archive receipt")
        elif any(receipt["task_id"] == envelope["task_id"] and receipt["workspace_id"] == envelope["workspace_id"] and receipt["candidate_id"] == candidate["candidate_id"] for receipt in receipts):
            raise ValueError("candidate was already dispatched; retry_of is required")

        workspace, dispatch = envelope["workspace_id"], envelope["dispatch_id"]
        ledger_path = self._ledger_path(workspace, dispatch)
        make_journal = self._journal_factory(envelope)
        journal = self.get_ledger(workspace, dispatch)
        if journal is not None:
            self._validate_journal(journal, envelope)
            if journal["status"] == "COMMITTED":
                for path in candidate["allowed_paths"]:
                    if not verify_image(safe_resolve(self.repo_root, path, target_file=True), envelope["postimages"][path]):
                        raise ValueError("committed target does not match postimage")
                return "already_committed"
            if journal["status"] in ("ROLLED_BACK", "ROLLBACK_CONFLICT"):
                raise ValueError(f"cannot resume terminal journal status {journal['status']}")
            self._verify_artifacts(envelope)
            if journal["status"] == "ROLLING_BACK":
                applied = self._reconcile(envelope, ledger_path, make_journal, "ROLLING_BACK")
                self._rollback(envelope, applied, ledger_path, make_journal)
                return "ROLLED_BACK"
            applied = self._reconcile(envelope, ledger_path, make_journal, "APPLYING")
        else:
            transaction_root = self._transaction_root(workspace, dispatch)
            if transaction_root.exists():
                # Reject mismatched or unknown journal-less state before even a
                # temporary read-mode adjustment on an unreadable target.
                self._validate_preparation_tree(envelope)
            for path in candidate["allowed_paths"]:
                if not verify_image(safe_resolve(self.repo_root, path, target_file=True), envelope["preimages"][path]):
                    raise ValueError(f"target preimage mismatch: {path}")
            self._prepare_artifacts(envelope, decoded)
            write_atomic_json(ledger_path, make_journal("PREPARED", []))
            write_atomic_json(ledger_path, make_journal("APPLYING", []))
            applied = []

        try:
            for path in candidate["allowed_paths"]:
                if path in applied:
                    continue
                target = safe_resolve(self.repo_root, path, target_file=True)
                if not verify_image(target, envelope["preimages"][path]):
                    raise ValueError(f"target changed during apply: {path}")
                edit = decoded[path]
                if edit is None:
                    if target.exists():
                        _unlink_durable(target)
                else:
                    shadow = self._artifact_path(workspace, dispatch, "post", path)
                    if not verify_image(shadow, envelope["postimages"][path]):
                        raise ValueError(f"post shadow artifact mismatch for {path}")
                    _atomic_replace_bytes(target, _read_bytes_preserving_mode(shadow), edit[1])
                if not verify_image(target, envelope["postimages"][path]):
                    raise RuntimeError(f"target postimage verification failed: {path}")
                applied.append(path)
                write_atomic_json(ledger_path, make_journal("APPLYING", applied))
        except BaseException as apply_error:
            reconciled = self._reconcile(envelope, ledger_path, make_journal, "ROLLING_BACK")
            self._rollback(envelope, reconciled, ledger_path, make_journal)
            raise RuntimeError("apply failed and target transaction was rolled back") from apply_error
        write_atomic_json(ledger_path, make_journal("COMMITTED", applied))
        return "COMMITTED"

    def _rollback(self, envelope: dict[str, Any], applied: list[str], ledger_path: Path, make_journal: Callable[[str, list[str]], dict[str, Any]]) -> None:
        workspace, dispatch = envelope["workspace_id"], envelope["dispatch_id"]
        self._verify_artifacts(envelope)
        for path in reversed(list(applied)):
            target = safe_resolve(self.repo_root, path, target_file=True)
            if verify_image(target, envelope["preimages"][path]):
                applied.remove(path)
                write_atomic_json(ledger_path, make_journal("ROLLING_BACK", applied))
                continue
            if not verify_image(target, envelope["postimages"][path]):
                write_atomic_json(ledger_path, make_journal("ROLLBACK_CONFLICT", applied))
                raise RuntimeError(f"rollback conflict: {path}")
            pre = envelope["preimages"][path]
            if pre["state"] == "absent":
                if target.exists():
                    _unlink_durable(target)
            else:
                snapshot = self._artifact_path(workspace, dispatch, "pre", path)
                if not verify_image(snapshot, pre):
                    raise ValueError(f"preimage snapshot artifact mismatch for {path}")
                _atomic_replace_bytes(target, _read_bytes_preserving_mode(snapshot), pre["mode"])
            if not verify_image(target, pre):
                write_atomic_json(ledger_path, make_journal("ROLLBACK_CONFLICT", applied))
                raise RuntimeError(f"rollback did not restore preimage: {path}")
            applied.remove(path)
            write_atomic_json(ledger_path, make_journal("ROLLING_BACK", applied))
        write_atomic_json(ledger_path, make_journal("ROLLED_BACK", []))


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: executor_runner.py <envelope.json> <runtime_context.json>")
        return 2
    try:
        envelope = load_json_strict(Path(argv[1]))
        context = load_json_strict(Path(argv[2]))
        status = BoundedExecutor(Path.cwd()).apply(envelope, context)
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"Error: {exc}")
        return 1
    print(f"Status: {status}")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv))
