#!/usr/bin/env python3
"""One-projection benchmark for the production-review queue replay.

Every invocation is a fresh process that calls
``queue._projection(root, pinned_commit, progress={})`` exactly once.  It never
rebuilds, replaces or writes the queue database or checkpoint, and it never
pre-seeds a cache.  The identical harness measures the pre-implementation
baseline and the candidate, so identity, complete progress and resource
accounting share one algorithm and are directly comparable.

Resource accounting is deliberately split:

* ``wall_s`` is monotonic wall time around the single projection call.
* ``self_*``/``children_*`` and the ``total_*`` sums come from ``os.times()``.
* ``peak_self_rss_kib`` is ``RUSAGE_SELF.ru_maxrss`` (never sampled RSS, never
  self plus children).

``--compare`` checks the same normalized root, the eight identity fields, the
complete progress report, the frozen RSS/time thresholds and the
run-invariance records against a baseline produced by this same script, and
exits non-zero on any mismatch.  ``--compare`` and ``--output`` are validated
before the projection runs, so a bad argument never costs a full replay and an
existing report is never truncated.

Usage::

    python3 -B tools/orchestration/benchmark_projection.py \
      --root <repo> --treeish <commit> --output <json> [--compare <baseline.json>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Frozen acceptance limits (see SPEC/PLAN): both candidate samples must be
# <= 4 GiB and <= 35% of the same-harness baseline; wall and total user time
# each <= 110% of that baseline.  These are never relaxed after seeing results.
RSS_LIMIT_KIB = 4 * 1024 * 1024
RSS_BASELINE_FRACTION = 0.35
TIME_BASELINE_FRACTION = 1.10

IDENTITY_FIELDS = (
    "head", "catalog_id", "entries_n", "overrides_n", "reconciliation_n",
    "entries_d", "overrides_d", "reconciliation_d",
)
IMPLEMENTATION_FILES = (
    "tools/i18nlib/git_evidence_reader.py",
    "tools/i18nlib/production_review_v2_lite_queue.py",
    "tools/i18nlib/production_review_v2_lite_progress.py",
)
QUEUE_RELATIVE = Path(".artifacts/i18n/production-review-v2-lite")
DATABASE_NAME = "queue.sqlite3"
CHECKPOINT_NAME = "active-batch.json"


def _digest(value: object) -> str:
    """The queue's own identity digest recipe: sha256 of the repr bytes."""
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.decode("ascii").strip()


def _commit(root: Path, treeish: str) -> str:
    resolved = _git(root, "rev-parse", "--verify", f"{treeish}^{{commit}}")
    if len(resolved) != 40 or any(ch not in "0123456789abcdef" for ch in resolved):
        raise SystemExit(f"treeish did not resolve to a commit: {treeish!r}")
    return resolved


def _queue_state(root: Path) -> dict[str, object]:
    """Read-only fingerprint of the queue database and checkpoint."""
    database = root / QUEUE_RELATIVE / DATABASE_NAME
    checkpoint = root / QUEUE_RELATIVE / CHECKPOINT_NAME
    state: dict[str, object] = {
        "database_present": database.is_file() and not database.is_symlink(),
        "checkpoint_present": checkpoint.exists() or checkpoint.is_symlink(),
    }
    if state["database_present"]:
        state["database_sha256"] = _file_sha256(database)
        from i18nlib import production_review_v2_lite_queue as queue
        overrides, reconciliation, meta = queue.business_rows(database)
        state["business_digest"] = _digest([list(overrides), list(reconciliation), list(meta)])
        state["overrides_n"] = len(overrides)
        state["reconciliation_n"] = len(reconciliation)
    return state


def _load_modules(root: Path):
    tools = str(root / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    from i18nlib import git_evidence_reader as reader
    from i18nlib import production_review_v2_lite_queue as queue
    return reader, queue


def _implementation_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for relative in IMPLEMENTATION_FILES:
        path = root / relative
        hashes[relative] = _file_sha256(path) if path.is_file() else "<missing>"
    return hashes


def run(root: Path, treeish: str) -> dict[str, object]:
    commit = _commit(root, treeish)
    reader, queue = _load_modules(root)
    if queue.git_evidence_reader is not reader:
        raise SystemExit("queue and reader modules disagree on the evidence reader")

    head_before = _git(root, "rev-parse", "HEAD")
    queue_before = _queue_state(root)
    if queue_before["checkpoint_present"]:
        raise SystemExit("refusing to benchmark with an active queue checkpoint")

    progress: dict[str, object] = {}
    times_before = os.times()
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
    start = time.monotonic()
    projection = queue._projection(root, commit, progress=progress)
    wall = time.monotonic() - start
    times_after = os.times()
    usage_after = resource.getrusage(resource.RUSAGE_SELF)

    head_after = _git(root, "rev-parse", "HEAD")
    queue_after = _queue_state(root)
    if head_before != head_after:
        raise SystemExit(f"HEAD moved during the projection: {head_before} -> {head_after}")
    if queue_before != queue_after:
        raise SystemExit("queue/checkpoint state changed during a read-only projection")

    evidence_head, manifest, entries, overrides, reconciliation = projection
    if evidence_head != commit:
        raise SystemExit(f"projection resolved {evidence_head}, expected {commit}")

    self_user = times_after.user - times_before.user
    self_sys = times_after.system - times_before.system
    children_user = times_after.children_user - times_before.children_user
    children_sys = times_after.children_system - times_before.children_system
    children_usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    result: dict[str, object] = {
        "kind": "projection_benchmark",
        "root": str(root.resolve()),
        "treeish": commit,
        "process": os.getpid(),
        "wall_s": wall,
        "self_user_s": self_user,
        "children_user_s": children_user,
        "total_user_s": self_user + children_user,
        "self_sys_s": self_sys,
        "children_sys_s": children_sys,
        "total_sys_s": self_sys + children_sys,
        "peak_self_rss_kib": usage_after.ru_maxrss,
        "peak_children_rss_kib": children_usage.ru_maxrss,
        "self_major_faults": usage_after.ru_majflt - usage_before.ru_majflt,
        "identity": {
            "head": evidence_head,
            "catalog_id": manifest["catalog_id"],
            "entries_n": len(entries),
            "overrides_n": len(overrides),
            "reconciliation_n": len(reconciliation),
            "entries_d": _digest(list(entries)),
            "overrides_d": _digest(overrides),
            "reconciliation_d": _digest(reconciliation),
        },
        "progress": progress,
        "implementation": _implementation_hashes(root),
        "head_before": head_before,
        "head_after": head_after,
        "head_unchanged": head_before == head_after,
        "queue_invariance": {"before": queue_before, "after": queue_after, "unchanged": queue_before == queue_after},
        "limits": [
            "wall/user/sys are measured once around exactly one _projection call; no rebuild or replace.",
            "peak_self_rss_kib is RUSAGE_SELF.ru_maxrss, not sampled RSS and not self+children.",
            "compare thresholds are frozen before implementation and never relaxed afterwards.",
        ],
    }
    return result


def compare(candidate: dict[str, object], baseline: dict[str, object]) -> dict[str, object]:
    checks: dict[str, dict[str, object]] = {}

    def check(name: str, passed: bool, **evidence) -> None:
        checks[name] = {"passed": bool(passed), **evidence}

    # ``root`` is already the run-normalized absolute root in both reports.
    check("same_root", candidate["root"] == baseline["root"],
          candidate=candidate["root"], baseline=baseline["root"])
    check("same_treeish", candidate["treeish"] == baseline["treeish"],
          candidate=candidate["treeish"], baseline=baseline["treeish"])

    for field in IDENTITY_FIELDS:
        left = candidate["identity"][field]
        right = baseline["identity"][field]
        check(f"identity_{field}", left == right, candidate=left, baseline=right)

    check("progress_identical", candidate["progress"] == baseline["progress"],
          candidate=candidate["progress"], baseline=baseline["progress"])

    rss = candidate["peak_self_rss_kib"]
    baseline_rss = baseline["peak_self_rss_kib"]
    check("peak_self_rss_kib_limit", rss <= RSS_LIMIT_KIB, candidate=rss, limit=RSS_LIMIT_KIB)
    check("peak_self_rss_kib_fraction", rss <= baseline_rss * RSS_BASELINE_FRACTION,
          candidate=rss, baseline=baseline_rss, limit=baseline_rss * RSS_BASELINE_FRACTION)
    check("wall_fraction", candidate["wall_s"] <= baseline["wall_s"] * TIME_BASELINE_FRACTION,
          candidate=candidate["wall_s"], baseline=baseline["wall_s"],
          limit=baseline["wall_s"] * TIME_BASELINE_FRACTION)
    check("total_user_fraction", candidate["total_user_s"] <= baseline["total_user_s"] * TIME_BASELINE_FRACTION,
          candidate=candidate["total_user_s"], baseline=baseline["total_user_s"],
          limit=baseline["total_user_s"] * TIME_BASELINE_FRACTION)

    check("head_unchanged", bool(candidate["head_unchanged"]))
    check("queue_unchanged", bool(candidate["queue_invariance"]["unchanged"]))

    return {
        "passed": all(entry["passed"] for entry in checks.values()),
        "checks": checks,
        "thresholds": {
            "peak_self_rss_kib": RSS_LIMIT_KIB,
            "rss_baseline_fraction": RSS_BASELINE_FRACTION,
            "time_baseline_fraction": TIME_BASELINE_FRACTION,
        },
    }


def _load_compare(path: Path) -> dict[str, object]:
    """Read and type-check the comparison baseline before any measurement."""
    if not path.is_file():
        raise SystemExit(f"--compare file does not exist: {path}")
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SystemExit(f"--compare file is not readable JSON: {path}: {error}")
    if not isinstance(baseline, dict) or baseline.get("kind") != "projection_benchmark":
        raise SystemExit("--compare file is not a projection_benchmark report")
    return baseline


def _preflight_output(path: Path) -> None:
    """Reject obviously unusable output paths before spending a replay on them.

    A disposable probe file checks directory writability without touching any
    existing report, so a failed argument never truncates prior output.
    """
    if path.exists():
        if not path.is_file():
            raise SystemExit(f"--output is not a regular file: {path}")
        if not os.access(path, os.W_OK):
            raise SystemExit(f"--output is not writable: {path}")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle, name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".probe", dir=str(path.parent))
    except OSError as error:
        raise SystemExit(f"--output directory is not usable: {path.parent}: {error}")
    os.close(handle)
    Path(name).unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--treeish", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--compare", type=Path, default=None,
                        help="baseline JSON produced by this script; exit non-zero on mismatch")
    arguments = parser.parse_args(argv)

    root = arguments.root.resolve()
    if not (root / ".git").exists():
        raise SystemExit(f"--root is not a Git worktree: {root}")

    baseline = _load_compare(arguments.compare) if arguments.compare is not None else None
    _preflight_output(arguments.output)

    result = run(root, arguments.treeish)
    report = dict(result)
    if baseline is not None:
        report["comparison"] = compare(result, baseline)
        report["baseline"] = {
            "path": str(arguments.compare),
            "wall_s": baseline["wall_s"],
            "total_user_s": baseline["total_user_s"],
            "peak_self_rss_kib": baseline["peak_self_rss_kib"],
        }

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if baseline is not None and not report["comparison"]["passed"]:
        failed = [name for name, entry in report["comparison"]["checks"].items() if not entry["passed"]]
        print(f"FAILED comparison checks: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
