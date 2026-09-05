"""Versioned gate execution. Results are receipts, never a cross-command cache."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import stat
import subprocess
import tempfile

from . import TOOL_VERSION

VERSION = "ci-gates-v2"
PYTHON = ["python3", "-B"]
CHECKS = [
    ("01-doctor", PYTHON + ["tools/i18n", "doctor"]),
    ("02-strict-lint", PYTHON + ["tools/i18n", "lint", "--strict"]),
    ("03-test-group-registration", PYTHON + ["tools/test_groups.py", "--check"]),
    ("03-toolchain-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "toolchain"]),
    ("04-quality-facts-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "quality-facts"]),
    ("04-semantic-claim-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "semantic-claim"]),
    ("04-semantic-claims-strict-registry", PYTHON + ["tools/i18n", "claims", "check", "--registry", "evidence/quality/semantic-claim-regressions-v1.json", "--strict"]),
    ("05-contract-suite-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "contract-suite"]),
    ("05-production-shadow-surface-ledger-tests", PYTHON + ["tools/test_groups.py", "--group", "production-shadow-surface-ledger"]),
    ("06-runtime-collision-scan", PYTHON + ["tools/scan_runtime_collisions.py"]),
    ("07-runtime-key-classification", PYTHON + ["tools/classify_runtime_keys.py"]),
    ("08-terminology-static-audit", PYTHON + ["tools/audit_static.py"]),
    ("09-terminology-dynamic-audit", PYTHON + ["tools/audit_dynamic.py"]),
    ("10-domain-annotation", PYTHON + ["tools/annotate_domains.py"]),
    ("11-worktree-whitespace", ["git", "diff", "--check"]),
    ("11-staged-whitespace", ["git", "diff", "--cached", "--check"]),
    ("12-core-addon-build", PYTHON + ["tools/i18n", "build", "--profile", "addon", "--component", "tome", "--require-complete"]),
]
COVERAGE = {
    "tests/i18n/test_surface_screen_manifest.py": "05-production-shadow-surface-ledger-tests",
    "tests/i18n/test_surface_screen_result_check.py": "05-production-shadow-surface-ledger-tests",
    "tests/i18n/test_contextual_result_check.py": "05-contract-suite-unit-tests",
}


class GateError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def checks(skip_build=False):
    return copy.deepcopy(CHECKS[:-1] if skip_build else CHECKS)


def candidate(batch_id, catalog_id, base_commit, policy_sha256, revisions):
    """Both producer and replay derive this from their validated batch, not a supplied hash."""
    return {"batch_id": batch_id, "catalog_id": catalog_id, "base_commit": base_commit,
            "policy_sha256": policy_sha256, "ordered_revisions": list(revisions)}


def _git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE)


def _file_identity(path):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return ["absent"]
    if stat.S_ISLNK(mode):
        return ["symlink", os.readlink(path)]
    if not stat.S_ISREG(mode):
        raise GateError(f"gate input is not an ordinary file: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return [stat.S_IMODE(mode), h.hexdigest()]


def binding(root, selected=None, skip_build=False):
    root = Path(root).resolve()
    # Include index blobs and actual file bytes (including untracked nonignored inputs).
    # Ignored prospective/log files cannot invalidate a receipt; tracked ignored files can.
    names = sorted(set(_git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")) - {b""})
    files = {os.fsdecode(name): _file_identity(root / os.fsdecode(name)) for name in names}
    config = {name: value for name, value in files.items()
              if name.startswith(("i18n/", "terminology/")) or name == "tests/i18n/test_groups.json"}
    config["environment_sha256"] = digest(dict(os.environ))
    selected = copy.deepcopy(selected)
    return {"candidate": selected, "candidate_sha256": digest(selected),
            "worktree_sha256": digest({"files": files, "index": _git(root, "ls-files", "--stage", "-z").hex()}),
            "tool_commit": _git(root, "rev-parse", "HEAD").decode().strip(),
            "tool_version": TOOL_VERSION, "runner_version": VERSION,
            "python_version": platform.python_version(), "config_sha256": digest(config),
            "check_set_sha256": digest(checks(skip_build)), "skip_build": skip_build}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _execute(argv, root, log):
    with log.open("wb") as stream:
        try:
            return subprocess.run(argv, cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
        except OSError as error:
            stream.write(str(error).encode("utf-8", "replace"))
            return 127


def run(root, selected=None, skip_build=False, *, execute=None):
    """One invocation, one execution per ID. execute is an in-process unit-test seam only."""
    root = Path(root).resolve()
    log_root = root / ".artifacts/i18n/ci-gates"
    log_root.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="run.", dir=log_root))
    print(f"CI gate log directory: {directory}", flush=True)
    result = {"schema_version": 2, "binding": None, "coverage": COVERAGE.copy(),
              "started_at": _now(), "finished_at": None, "complete": False,
              "success": False, "checks": [], "error": None}
    execute = _execute if execute is None else execute
    try:
        result["binding"] = binding(root, selected, skip_build)
        for check_id, argv in checks(skip_build):
            log = directory / (check_id + ".log")
            start = _now()
            code = execute(argv, root, log)
            record = {"id": check_id, "argv": argv, "command": shlex.join(argv),
                      "exit_code": code, "log_path": log.relative_to(root).as_posix(),
                      "output_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
                      "started_at": start, "finished_at": _now()}
            result["checks"].append(record)
            print(f"{'PASS' if code == 0 else 'FAIL'}  {check_id} (log: {log})", flush=True)
        if result["binding"] != binding(root, selected, skip_build):
            raise GateError("gate binding changed during execution")
        result["complete"] = True
        result["success"] = all(type(item["exit_code"]) is int and item["exit_code"] == 0 for item in result["checks"])
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        result["error"] = str(error)
    finally:
        result["finished_at"] = _now()
        (directory / "results.json").write_bytes(canonical(result) + b"\n")
    print("ALL GATES PASSED" if result["success"] else "GATES FAILED", flush=True)
    return result


def _require(condition, message):
    if not condition:
        raise GateError(message)


def _hash(value, length=64):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{%d}" % length, value) is not None


def _time(value):
    _require(isinstance(value, str), "gate timestamp must be text")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise GateError("invalid gate timestamp") from error
    _require(parsed.tzinfo is not None, "gate timestamp requires timezone")
    return parsed


def validate(result, *, selected=None, expected_binding=None, require_full=True, root=None):
    """Validate production receipts against current definitions and optional live inputs."""
    return _validate(result, selected=selected, expected_binding=expected_binding,
                     require_full=require_full, root=root, historical=False)


def validate_historical(result, *, selected):
    """Replay recorded definitions, never authorize production execution or reuse."""
    return _validate(result, selected=selected, historical=True)


def _validate(result, *, selected, expected_binding=None, require_full=True, root=None,
              historical=False):
    _require(isinstance(result, dict) and set(result) == {
        "schema_version", "binding", "coverage", "started_at", "finished_at", "complete", "success", "checks", "error"}, "gate result exact schema mismatch")
    _require(type(result["schema_version"]) is int and result["schema_version"] == 2, "gate schema version mismatch")
    _require(result["complete"] is True and result["success"] is True and result["error"] is None, "gate result failed or incomplete")
    start, end = _time(result["started_at"]), _time(result["finished_at"])
    _require(start <= end, "gate result time order")
    b = result["binding"]
    _require(isinstance(b, dict) and set(b) == {"candidate", "candidate_sha256", "worktree_sha256", "tool_commit", "tool_version", "runner_version", "python_version", "config_sha256", "check_set_sha256", "skip_build"}, "gate binding exact schema mismatch")
    _require(type(b["skip_build"]) is bool and (not require_full or not b["skip_build"]), "full gate build required")
    for field in ("candidate_sha256", "worktree_sha256", "config_sha256", "check_set_sha256"):
        _require(_hash(b[field]), f"invalid gate {field}")
    _require(_hash(b["tool_commit"], 40), "invalid gate tool commit")
    _require(isinstance(b["runner_version"], str)
             and re.fullmatch(r"ci-gates-v[1-9][0-9]*", b["runner_version"]) is not None
             and (historical or b["runner_version"] == VERSION)
             and isinstance(b["tool_version"], str)
             and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", b["tool_version"]) is not None
             and isinstance(b["python_version"], str)
             and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", b["python_version"]) is not None, "invalid gate version")
    _require(b["candidate"] == selected and b["candidate_sha256"] == digest(selected), "gate candidate binding mismatch")
    if selected is not None:
        # preflight requires HEAD == batch base; replay can recheck this fact
        # without access to ignored logs or the original dirty worktree.
        _require(isinstance(selected, dict) and b["tool_commit"] == selected.get("base_commit"), "gate tool commit/batch base mismatch")
    records = result["checks"]
    _require(isinstance(records, list) and bool(records), "gate check set incomplete")
    definitions = []
    seen = set()
    for record in records:
        _require(isinstance(record, dict) and set(record) == {"id", "argv", "command", "exit_code", "log_path", "output_sha256", "started_at", "finished_at"}, "gate check exact schema mismatch")
        check_id, argv = record["id"], record["argv"]
        _require(isinstance(check_id, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", check_id) is not None,
                 "invalid gate check ID")
        _require(check_id not in seen, "duplicate gate check ID")
        seen.add(check_id)
        _require(isinstance(argv, list) and bool(argv)
                 and all(isinstance(arg, str) and bool(arg) and "\0" not in arg for arg in argv),
                 "invalid gate check argv")
        definitions.append((check_id, argv))
    _require(b["check_set_sha256"] == digest(definitions), "gate check set binding mismatch")
    if not historical:
        _require(definitions == checks(b["skip_build"]), "gate check ID/command mismatch")
    if expected_binding is not None:
        _require(b == expected_binding, "gate live binding mismatch")
    coverage = result["coverage"]
    _require(isinstance(coverage, dict) and bool(coverage)
             and all(isinstance(name, str) and bool(name.strip())
                     and isinstance(owner, str) and owner in seen for name, owner in coverage.items()),
             "invalid gate consumer coverage")
    if not historical:
        _require(coverage == COVERAGE, "gate consumer coverage mismatch")
    previous = start
    for record, (check_id, argv) in zip(records, definitions):
        _require(isinstance(record, dict) and set(record) == {"id", "argv", "command", "exit_code", "log_path", "output_sha256", "started_at", "finished_at"}, "gate check exact schema mismatch")
        _require(record["id"] == check_id and record["argv"] == argv and record["command"] == shlex.join(argv), "gate check ID/command mismatch")
        _require(type(record["exit_code"]) is int and record["exit_code"] == 0, "gate command failed")
        _require(_hash(record["output_sha256"]), "invalid gate output hash")
        path = record["log_path"]
        _require(isinstance(path, str) and re.fullmatch(r"\.artifacts/i18n/ci-gates/run\.[\w-]+/" + re.escape(check_id) + r"\.log", path) is not None, "invalid gate log path")
        a, z = _time(record["started_at"]), _time(record["finished_at"])
        _require(previous <= a <= z <= end, "gate check time order")
        previous = z
        if root is not None:
            log = Path(root) / path
            _require(not log.is_symlink() and hashlib.sha256(log.read_bytes()).hexdigest() == record["output_sha256"], "gate log hash mismatch")
    return result
