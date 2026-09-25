"""Disposable same-commit cache of one committed queue projection.

Stage 2 of ``docs/projection-optimization-plan-20260924.md``.  A file here is
only a speed-up: it holds the result of one successful, complete, independent
replay of committed Git evidence (projection, the complete progress of that
same replay, and the Git objects the replay named).  Deleting it never loses
anything, and every failure to read or write it only costs a replay.

What it is not: not a second queue, not a coordinator checkpoint, not derived
from SQLite or an active checkpoint, not authenticated (no HMAC).  A plain
digest detects accidental damage only.

Switch: ``I18N_PROJECTION_CACHE=on`` enables it; anything else (including
unset) is off, and off neither reads nor writes nor creates the directory.
``I18N_PROJECTION_CACHE_TRACE=1`` prints one stderr line per cache decision.

Reads happen only inside ``entry_scope`` for the ordinary historical-baseline
entries in ``READ_ENTRIES``.  Every other entry — queue init/rebuild/check/
status, finalize, recover, abandon, migration — keeps its independent full
replay; ``independent()`` pins that for direct Python callers as well.  Any
successful full replay may publish while the switch is on.

A hit needs all of: the exact key (repository/worktree, resolved commit, this
format, the running implementation and runtime, and the effective Git settings
that change what the replay's own commands return), the same Git environment
rules as the publication fast path, every recorded object still present with
the same type, the commit's reachable object closure still connected, and a
strictly typed, digest-matching file.  Anything less is a miss.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import sysconfig
import tempfile
import time
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Any, Callable, Iterator

from . import git_evidence_reader
from . import production_review as wp1

MODE_ENV = "I18N_PROJECTION_CACHE"
TRACE_ENV = "I18N_PROJECTION_CACHE_TRACE"
CACHE_RELATIVE = Path(".artifacts/i18n/projection-cache-v1")
FORMAT = "production_review_v2_lite_projection_cache_v1"
MAX_COMMITS = 3
MAX_TOTAL_BYTES = 512 * 1024 * 1024
# A code/rule file modified this close to (or after) process start may differ
# from what this process already imported; refuse rather than guess.
HOT_EDIT_MARGIN_NS = 2_000_000_000
STALE_TEMP_SECONDS = 3600
# (production command, action) pairs whose historical-baseline read may hit.
READ_ENTRIES = frozenset({
    ("batch", "start"),
    ("batch", "surface-export"),
    ("batch", "surface-import"),
    ("batch", "contextual-export"),
    ("batch", "contextual-import"),
    ("batch", "adjudicate"),
    ("batch", "prepare-evidence"),
    ("repair", "preflight"),
})
CODE_ROOT = Path(__file__).resolve().parents[2]
# Known extensionless entry scripts that run as ``__main__``; fingerprinted
# like code.  Any other extensionless tools file loaded as a module is refused.
ENTRY_SCRIPTS = frozenset({Path("tools/i18n")})

_NAME = re.compile(r"v1-([0-9a-f]{40})-([0-9a-f]{32})\.json")
_TEMP_PREFIX = ".v1-tmp-"
_SHA1 = re.compile(r"[0-9a-f]{40}")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_OBJECT_TYPES = frozenset({"commit", "tree", "blob", "tag"})
_HEADER_KEYS = frozenset({"format", "key_sha256", "payload_bytes", "payload_sha256"})
_PAYLOAD_KEYS = frozenset({"key", "evidence_head", "manifest", "entries", "entry_digests",
                           "overrides", "reconciliation", "progress", "objects"})

_reads: ContextVar[str | None] = ContextVar("projection_cache_reads", default=None)
_off: ContextVar[bool] = ContextVar("projection_cache_off", default=False)

# Process-local diagnostics only; never part of any CLI stdout report.
events: list[dict[str, Any]] = []
# First implementation identity seen per code root in this process, and the
# roots whose identity has since changed (hot edit): those never use a cache.
_frozen: dict[Path, dict[str, Any]] = {}
_poisoned: set[Path] = set()


class _Skip(Exception):
    """A reason not to use the cache; never escapes this module."""


def _event(kind: str, reason: str, **fields: Any) -> None:
    record = {"event": kind, "reason": reason, **fields}
    events.append(record)
    if os.environ.get(TRACE_ENV) == "1":
        print(f"projection-cache: {kind} {reason}", file=sys.stderr)


def enabled() -> bool:
    return os.environ.get(MODE_ENV) == "on" and not _off.get()


def reads_allowed() -> bool:
    return enabled() and _reads.get() is not None


@contextmanager
def entry_scope(command: object, action: object) -> Iterator[None]:
    """Allow reads for exactly the listed entries; reset them for all others."""
    token = _reads.set(f"{command} {action}" if (command, action) in READ_ENTRIES else None)
    try:
        yield
    finally:
        _reads.reset(token)


@contextmanager
def independent() -> Iterator[None]:
    """Recovery/finalize paths: always replay; a successful replay may publish."""
    token = _reads.set(None)
    try:
        yield
    finally:
        _reads.reset(token)


@contextmanager
def disabled() -> Iterator[None]:
    """Diagnostic oracle: no cache read and no cache write whatever the switch."""
    token = _off.set(True)
    try:
        yield
    finally:
        _off.reset(token)


# --- implementation identity -------------------------------------------------

def _process_start_ns() -> int | None:
    try:
        raw = Path("/proc/self/stat").read_bytes()
        started_ticks = int(raw[raw.rindex(b")") + 2:].split()[19])
        since_boot = time.clock_gettime(time.CLOCK_BOOTTIME)
        hertz = os.sysconf("SC_CLK_TCK")
    except (OSError, ValueError, IndexError, AttributeError):
        return None
    return time.time_ns() - int((since_boot - started_ticks / hertz) * 1_000_000_000)


def _code_digest(code_root: Path, not_after_ns: int) -> str:
    """tools/**/*.py, ENTRY_SCRIPTS and every i18n/quality file: paths, sizes and bytes."""
    digest = hashlib.sha256()
    for base, wanted in ((code_root / "tools",
                          lambda path: path.name.endswith(".py") or
                          path.relative_to(code_root) in ENTRY_SCRIPTS),
                         (code_root / "i18n" / "quality", lambda path: True)):
        try:
            if not stat.S_ISDIR(base.lstat().st_mode):
                raise _Skip(f"code input is not an ordinary directory: {base}")
        except OSError as error:
            raise _Skip(f"code input unavailable: {error}") from error
        for directory, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(name for name in dirnames if name != "__pycache__")
            for name in dirnames:
                if os.path.islink(os.path.join(directory, name)):
                    raise _Skip("code input contains a symlinked directory")
            for name in sorted(filenames):
                path = Path(directory, name)
                if not wanted(path):
                    continue
                status = path.lstat()
                if not stat.S_ISREG(status.st_mode):
                    raise _Skip("code input contains a non-ordinary file")
                if status.st_mtime_ns >= not_after_ns:
                    raise _Skip("code input modified after process start")
                raw = path.read_bytes()
                digest.update(path.relative_to(code_root).as_posix().encode("utf-8") + b"\0" +
                              str(len(raw)).encode("ascii") + b"\0" +
                              hashlib.sha256(raw).digest())
    return digest.hexdigest()


def _loaded_modules(code_root: Path, not_after_ns: int) -> list[list[str]]:
    """Loaded modules outside stdlib and the fingerprinted tools tree.

    Part of the key but not frozen: a different set only means a different
    key.  Their files get the same modified-after-start refusal as code.
    """
    tools = (code_root / "tools").resolve()
    stdlib = {Path(sysconfig.get_paths()[name]).resolve() for name in ("stdlib", "platstdlib")}
    result: list[list[str]] = []
    for name, module in sorted(dict(sys.modules).items()):
        file = getattr(module, "__file__", None)
        if not isinstance(file, str):
            continue
        path = Path(file).resolve()
        if path.is_relative_to(tools):
            known = path.suffix == ".py" or path.relative_to(code_root) in ENTRY_SCRIPTS
            if not known or not path.is_file():
                raise _Skip(f"loaded tools module has no current source file: {name}")
            continue
        if any(path.is_relative_to(base) for base in stdlib):
            continue
        try:
            if path.stat().st_mtime_ns >= not_after_ns:
                raise _Skip("loaded module modified after process start")
            raw = path.read_bytes()
        except OSError as error:
            raise _Skip(f"loaded module source unreadable: {name}") from error
        result.append([name, str(path), hashlib.sha256(raw).hexdigest()])
    return result


def _runtime() -> dict[str, str]:
    git_path = shutil.which("git")
    if git_path is None:
        raise _Skip("git executable not found")
    try:
        version = subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE).stdout.decode("utf-8").strip()
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as error:
        raise _Skip("git version unavailable") from error
    return {"python": sys.version, "implementation": sys.implementation.name,
            "cache_tag": str(sys.implementation.cache_tag),
            "executable": os.path.realpath(sys.executable), "platform": sys.platform,
            "git": version, "git_path": os.path.realpath(git_path)}


def implementation_identity(code_root: Path = CODE_ROOT) -> dict[str, Any]:
    """The running implementation, or _Skip when it cannot be proven.

    The first code/runtime identity a process computes is frozen; any later
    difference (a file edited, added or removed while running) poisons the
    cache for the rest of the process instead of pairing new disk bytes with
    old code.  Any input modified after (or just before) process start is
    refused outright, since it may already differ from what was imported.
    """
    code_root = code_root.resolve()
    if code_root in _poisoned:
        raise _Skip("implementation changed during this process")
    started = _process_start_ns()
    if started is None:
        raise _Skip("process start time unavailable")
    not_after = started - HOT_EDIT_MARGIN_NS
    try:
        identity = {"code_sha256": _code_digest(code_root, not_after), "runtime": _runtime()}
    except _Skip:
        _poisoned.add(code_root)
        raise
    frozen = _frozen.setdefault(code_root, identity)
    if frozen != identity:
        _poisoned.add(code_root)
        raise _Skip("implementation changed during this process")
    return {**identity, "modules": _loaded_modules(code_root, not_after)}


# --- key, directory and Git checks -------------------------------------------

def _git_locations(root: Path) -> tuple[str, str]:
    try:
        raw = subprocess.run(["git", "rev-parse", "--absolute-git-dir", "--git-common-dir"],
                             cwd=root, check=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).stdout.decode("utf-8").splitlines()
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as error:
        raise _Skip("git directory unavailable") from error
    if len(raw) != 2:
        raise _Skip("git directory unavailable")
    return str(Path(raw[0]).resolve()), str((root / raw[1]).resolve())


def _git_settings(root: Path) -> dict[str, str]:
    """Effective settings the audited environment allows but a replay depends on.

    ``diff.renames`` decides whether ``git log --diff-filter=AM -- <path>``
    reports a directory-to-file replacement as a rename (hidden) or an
    addition (listed), which moves the located publication commit (SR-001).
    Git itself resolves it, with includes and the inherited environment the
    replay's commands see; unset stays distinct from either boolean, and any
    unreadable value refuses the cache.
    """
    try:
        completed = subprocess.run(["git", "config", "--includes", "--type=bool", "--get",
                                    "diff.renames"], cwd=root, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except OSError as error:
        raise _Skip("git settings unavailable") from error
    if completed.returncode == 1 and not completed.stdout:
        value = "unset"
    elif completed.returncode == 0 and completed.stdout in (b"true\n", b"false\n"):
        value = completed.stdout.decode("ascii").strip()
    else:
        raise _Skip("git settings unavailable")
    return {"diff.renames": value}


def replay_settings(root: Path) -> dict[str, str] | None:
    """Settings a replay is about to run with; None (never stored) if unreadable."""
    try:
        return _git_settings(root)
    except _Skip:
        return None


def _key(root: Path, commit: str, code_root: Path) -> dict[str, Any]:
    if _SHA1.fullmatch(commit) is None:
        raise _Skip("commit is not a SHA-1 object ID")
    git_dir, common_dir = _git_locations(root)
    return {"format": FORMAT, "root": str(root.resolve()), "git_dir": git_dir,
            "git_common_dir": common_dir, "commit": commit,
            "git_settings": _git_settings(root),
            "implementation": implementation_identity(code_root)}


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def _file_name(key: dict[str, Any]) -> str:
    return f"v1-{key['commit']}-{hashlib.sha256(_canonical(key)).hexdigest()[:32]}.json"


def cache_directory(root: Path) -> Path:
    return root.resolve() / CACHE_RELATIVE


def _directory(root: Path, *, create: bool) -> Path | None:
    current = root.resolve()
    for part in CACHE_RELATIVE.parts:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            if not create:
                return None
            try:
                current.mkdir(mode=0o700)
            except FileExistsError:
                pass
            mode = current.lstat().st_mode
        if not stat.S_ISDIR(mode):
            raise _Skip("cache path component is not an ordinary directory")
    return current


def _environment(root: Path, environment_ok: Callable[[Path], bool]) -> None:
    try:
        safe = environment_ok(root)
    except (wp1.ProductionReviewError, OSError, UnicodeError, ValueError) as error:
        raise _Skip("git environment check failed") from error
    if not safe:
        raise _Skip("git environment is not the plain audited case")


def _object_types(root: Path, names: list[str]) -> list[list[str]]:
    """[name, oid, type] for each name, or _Skip if any is missing."""
    if not names:
        return []
    try:
        output = subprocess.run(["git", "cat-file", "--batch-check"], cwd=root, check=True,
                                input=("\n".join(names) + "\n").encode("utf-8"),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        lines = output.decode("utf-8").split("\n")
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as error:
        raise _Skip("object check failed") from error
    if len(lines) != len(names) + 1 or lines[-1] != "":
        raise _Skip("object check output is malformed")
    result: list[list[str]] = []
    for name, line in zip(names, lines):
        parts = line.split(" ")
        if (len(parts) != 3 or _SHA1.fullmatch(parts[0]) is None or
                parts[1] not in _OBJECT_TYPES or not parts[2].isdigit()):
            raise _Skip("recorded Git object is missing or unreadable")
        result.append([name, parts[0], parts[1]])
    return result


def _connected(root: Path, commit: str) -> None:
    """Every object reachable from the commit is present (no fsck of contents)."""
    try:
        subprocess.run(["git", "rev-list", "--objects", "--quiet", commit, "--"], cwd=root,
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except (OSError, subprocess.CalledProcessError) as error:
        raise _Skip("commit object closure is not connected") from error


# --- strict encoding -------------------------------------------------------

def _json_native(value: object) -> None:
    """Only values that JSON returns with exactly the same types."""
    kind = type(value)
    if kind is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise _Skip("non-string mapping key")
            _json_native(item)
    elif kind is list:
        for item in value:
            _json_native(item)
    elif kind is float:
        if value != value or value in (float("inf"), float("-inf")):
            raise _Skip("non-finite number")
    elif kind not in (str, int, bool, type(None)):
        raise _Skip(f"value type {kind.__name__} does not round-trip")


def _optional_str(value: object) -> bool:
    return value is None or type(value) is str


def _override_row(row: object) -> bool:
    return (type(row) in (tuple, list) and len(row) == 7 and
            all(type(row[index]) is str for index in (0, 1, 2, 6)) and
            _optional_str(row[3]) and type(row[4]) is int and _optional_str(row[5]))


def _reconciliation_row(row: object) -> bool:
    return (type(row) in (tuple, list) and len(row) == 7 and
            all(type(row[index]) is str for index in (0, 1, 4, 5, 6)) and
            _optional_str(row[2]) and _optional_str(row[3]))


def _encode(key: dict[str, Any], projection: tuple, progress: dict[str, Any],
            objects: list[list[str]]) -> bytes:
    evidence_head, manifest, entries, overrides, reconciliation = projection
    if type(entries) is not wp1.VerifiedRows:
        raise _Skip("catalog rows are not verified rows")
    if not all(type(row) is tuple and _override_row(row) for row in overrides):
        raise _Skip("override rows are not the expected tuples")
    if not all(type(row) is tuple and _reconciliation_row(row) for row in reconciliation):
        raise _Skip("reconciliation rows are not the expected tuples")
    for value in (manifest, list(entries), progress):
        _json_native(value)
    digests = entries.digest_by_revision
    payload = {"key": key, "evidence_head": evidence_head, "manifest": manifest,
               "entries": list(entries),
               "entry_digests": [digests[row["entry_revision_identity"]] for row in entries],
               "overrides": [list(row) for row in overrides],
               "reconciliation": [list(row) for row in reconciliation],
               "progress": progress, "objects": objects}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(name: str) -> None:
    raise ValueError(f"non-finite JSON number {name}")


def _strict_json(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                      parse_constant=_reject_constant)


def _decode(raw: bytes, key: dict[str, Any], key_sha256: str) -> tuple[tuple, dict[str, Any], list[list[str]]]:
    newline = raw.find(b"\n")
    if newline < 0:
        raise _Skip("cache file has no header")
    try:
        header = _strict_json(raw[:newline])
    except (UnicodeDecodeError, ValueError) as error:
        raise _Skip("cache header is not strict JSON") from error
    body = raw[newline + 1:]
    if (type(header) is not dict or set(header) != _HEADER_KEYS or header["format"] != FORMAT or
            header["key_sha256"] != key_sha256 or type(header["payload_bytes"]) is not int or
            header["payload_bytes"] != len(body) or
            header["payload_sha256"] != hashlib.sha256(body).hexdigest()):
        raise _Skip("cache header, length or digest mismatch")
    try:
        payload = _strict_json(body)
    except (UnicodeDecodeError, ValueError, RecursionError) as error:
        raise _Skip("cache payload is not strict JSON") from error
    if type(payload) is not dict or set(payload) != _PAYLOAD_KEYS or payload["key"] != key:
        raise _Skip("cache payload schema or key mismatch")
    manifest, entries, digests = payload["manifest"], payload["entries"], payload["entry_digests"]
    overrides, reconciliation = payload["overrides"], payload["reconciliation"]
    progress, objects = payload["progress"], payload["objects"]
    if (payload["evidence_head"] != key["commit"] or type(manifest) is not dict or
            type(manifest.get("catalog_id")) is not str or type(progress) is not dict or
            type(entries) is not list or type(digests) is not list or len(entries) != len(digests) or
            not all(type(row) is dict and type(row.get("entry_revision_identity")) is str
                    for row in entries) or
            not all(type(digest) is str and _SHA256.fullmatch(digest) for digest in digests) or
            type(overrides) is not list or not all(type(row) is list and _override_row(row) for row in overrides) or
            type(reconciliation) is not list or
            not all(type(row) is list and _reconciliation_row(row) for row in reconciliation) or
            type(objects) is not list or
            not all(type(item) is list and len(item) == 3 and all(type(part) is str for part in item)
                    for item in objects)):
        raise _Skip("cache payload types mismatch")
    try:
        rows = wp1.VerifiedRows(entries, digests)
    except (wp1.ProductionReviewError, KeyError, TypeError) as error:
        raise _Skip("cache catalog rows are not unique verified rows") from error
    projection = (payload["evidence_head"], manifest, rows,
                  [tuple(row) for row in overrides], [tuple(row) for row in reconciliation])
    return projection, progress, objects


# --- public operations -------------------------------------------------------

def load(root: Path, commit: str, *, environment_ok: Callable[[Path], bool],
         code_root: Path = CODE_ROOT) -> tuple[tuple, dict[str, Any]] | None:
    """Return (projection, progress) for this exact commit, or None (miss)."""
    if not reads_allowed():
        return None
    try:
        _environment(root, environment_ok)
        key = _key(root, commit, code_root)
        directory = _directory(root, create=False)
        if directory is None:
            raise _Skip("no cache directory")
        path = directory / _file_name(key)
        try:
            # O_NONBLOCK: a FIFO planted under the name must not block the open;
            # fstat below still refuses anything but a regular file.
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except FileNotFoundError as error:
            raise _Skip("no cache file for this key") from error
        with os.fdopen(descriptor, "rb") as handle:
            status = os.fstat(handle.fileno())
            if not stat.S_ISREG(status.st_mode) or status.st_size > MAX_TOTAL_BYTES:
                raise _Skip("cache file is not an ordinary bounded file")
            raw = handle.read(MAX_TOTAL_BYTES + 1)
        projection, progress, objects = _decode(raw, key, hashlib.sha256(_canonical(key)).hexdigest())
        names = [item[0] for item in objects]
        if (names != sorted(set(names)) or git_evidence_reader.INCOMPLETE in names or
                _object_types(root, names) != objects):
            raise _Skip("recorded Git objects changed or disappeared")
        _connected(root, commit)
        # A hot edit during the checks above must not be paired with this hit.
        implementation_identity(code_root)
    except _Skip as reason:
        _event("miss", str(reason), commit=commit)
        return None
    except Exception as error:  # a cache fault only costs the replay
        _event("miss", f"cache read failed: {type(error).__name__}", commit=commit)
        return None
    _event("hit", "exact key and objects verified", commit=commit, file=path.name)
    return projection, progress


def store(root: Path, projection: tuple, progress: dict[str, Any], objects: set[str], *,
          settings: dict[str, str] | None, environment_ok: Callable[[Path], bool],
          code_root: Path = CODE_ROOT) -> bool:
    """Publish one successful complete replay; failures only return False.

    ``settings`` is ``replay_settings`` read just before that replay; the key
    must carry the same values, so a setting changed meanwhile is not stored.
    """
    if not enabled():
        return False
    commit = projection[0]
    temporary: Path | None = None
    try:
        if git_evidence_reader.INCOMPLETE in objects:
            raise _Skip("replay named an object that cannot be rechecked")
        _environment(root, environment_ok)
        key = _key(root, commit, code_root)
        if settings is None or key["git_settings"] != settings:
            raise _Skip("git settings changed or unreadable during the replay")
        typed = _object_types(root, sorted(objects))
        payload = _encode(key, projection, progress, typed)
        header = _canonical({"format": FORMAT, "key_sha256": hashlib.sha256(_canonical(key)).hexdigest(),
                             "payload_bytes": len(payload),
                             "payload_sha256": hashlib.sha256(payload).hexdigest()}) + b"\n"
        if len(header) + len(payload) > MAX_TOTAL_BYTES:
            raise _Skip("oversize")
        directory = _directory(root, create=True)
        assert directory is not None
        descriptor, name = tempfile.mkstemp(prefix=_TEMP_PREFIX, dir=directory)
        temporary = Path(name)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(header)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        # Recheck right before publishing: never label old code's result with
        # an identity computed from files edited during the replay.
        implementation_identity(code_root)
        final = directory / _file_name(key)
        os.replace(temporary, final)
        temporary = None
        _evict(directory, final.name)
    except _Skip as reason:
        _event("store-skipped", str(reason), commit=commit)
        return False
    except Exception as error:  # a cache fault never fails the business replay
        _event("store-skipped", f"cache write failed: {type(error).__name__}", commit=commit)
        return False
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except OSError:
                pass
    _event("stored", "complete replay published", commit=commit, file=final.name,
           bytes=len(header) + len(payload))
    return True


def _evict(directory: Path, keep: str) -> None:
    """Keep this file, then the newest commits: at most MAX_COMMITS and MAX_TOTAL_BYTES.

    Only regular files matching this module's own names are ever removed.
    """
    files: list[tuple[int, str, str, int]] = []
    now = time.time()
    with os.scandir(directory) as entries:
        for entry in entries:
            status = entry.stat(follow_symlinks=False)
            if not stat.S_ISREG(status.st_mode):
                continue
            if entry.name.startswith(_TEMP_PREFIX):
                if now - status.st_mtime > STALE_TEMP_SECONDS:
                    Path(entry.path).unlink(missing_ok=True)
                continue
            match = _NAME.fullmatch(entry.name)
            if match is not None:
                files.append((status.st_mtime_ns, entry.name, match.group(1), status.st_size))
    keep_commit = _NAME.fullmatch(keep).group(1)
    newest: dict[str, int] = {}
    for mtime, _name, commit, _size in files:
        newest[commit] = max(newest.get(commit, 0), mtime)
    ranked = sorted(newest, key=lambda commit: (commit == keep_commit, newest[commit]), reverse=True)
    kept_commits = set(ranked[:MAX_COMMITS])
    survivors: list[tuple[int, str, str, int]] = []
    for item in files:
        if item[2] in kept_commits:
            survivors.append(item)
        else:
            (directory / item[1]).unlink(missing_ok=True)
    total = sum(item[3] for item in survivors)
    for item in sorted(survivors):
        if total <= MAX_TOTAL_BYTES:
            break
        if item[1] == keep:
            continue
        (directory / item[1]).unlink(missing_ok=True)
        total -= item[3]
