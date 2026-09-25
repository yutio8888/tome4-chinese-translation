#!/usr/bin/env python3
"""Stage-1 projection measurement: one replay with non-overlapping segments.

This harness reuses ``benchmark_projection.run`` unchanged: one fresh process,
exactly one ``queue._projection(root, pinned_commit, progress={})`` call, the
same identity digests, complete progress and HEAD/queue/checkpoint invariance
guards.  It adds only what stage 1 of the projection optimisation plan asks
for, and only for the duration of that single call:

* exclusive (self) wall time per segment -- catalog, migration, publication,
  batch, progress and the projection's own inline remainder (head/tree reads,
  historical manifest checks, topo order and the winner summary).  A wrapped
  function's time excludes every nested wrapped call, so the segments never
  overlap and their sum equals the projection wall time up to timer overhead;
* the number and wall time of ``git`` subprocesses by subcommand.  Git time
  happens *inside* the segments above and is reported separately; it must not
  be added to them.

The original ``benchmark_projection`` thresholds (PERF-1) are not used or
changed.  ``--compare`` applies this task's own rule: identical identity digests
(full content and order of entries/overrides/reconciliation) and complete
progress, and candidate wall time and peak RSS each at most 110% of a baseline
produced by this same harness on the same root and commit.

Usage::

    python3 -B tools/orchestration/benchmark_projection_stage1.py \
      --root <repo> --treeish <commit> --output <json> [--compare <baseline.json>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from orchestration import benchmark_projection as base  # noqa: E402

KIND = "projection_benchmark_stage1"
WALL_FRACTION = 1.10
RSS_FRACTION = 1.10
IMPLEMENTATION_FILES = (
    "tools/i18nlib/git_evidence_reader.py",
    "tools/i18nlib/production_review_v2_lite_queue.py",
    "tools/i18nlib/production_review_v2_lite_migration.py",
    "tools/i18nlib/production_review_v2_lite_progress.py",
    "tools/orchestration/benchmark_projection.py",
    "tools/orchestration/benchmark_projection_stage1.py",
)
# (segment, module key, attribute).  Anything not listed stays in the
# projection's own inline remainder.
SEGMENTS = (
    ("catalog", "queue", "_catalog_view"),
    ("catalog", "queue", "_catalog_from_tree"),
    ("migration", "queue", "_validated_migration_edges"),
    ("migration", "migration", "reconciliation_rows_for_tree"),
    ("migration", "queue", "_migration_chain"),
    ("migration", "queue", "_unchanged_rows_through_chain"),
    ("publication", "queue", "_publication_commit"),
    ("publication", "queue", "_migration_publication_commit"),
    ("batch", "queue", "_batch_rows"),
    ("progress", "progress", "observe"),
    ("progress", "progress", "report"),
)
INLINE = "projection_inline_and_summary"


class Segments:
    """Exclusive wall time per segment, active only inside one projection."""

    def __init__(self) -> None:
        self.active = False
        self.exclusive: dict[str, float] = defaultdict(float)
        self.calls: Counter[str] = Counter()
        self._stack: list[float] = []
        self.git_calls: Counter[str] = Counter()
        self.git_wall: dict[str, float] = defaultdict(float)

    def wrap(self, segment: str, function: Callable[..., Any]) -> Callable[..., Any]:
        def measured(*args: Any, **kwargs: Any) -> Any:
            if not self.active:
                return function(*args, **kwargs)
            started = time.perf_counter()
            self._stack.append(0.0)
            try:
                return function(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - started
                nested = self._stack.pop()
                self.exclusive[segment] += elapsed - nested
                self.calls[segment] += 1
                if self._stack:
                    self._stack[-1] += elapsed
        measured.__wrapped__ = function  # type: ignore[attr-defined]
        return measured

    def root(self, function: Callable[..., Any]) -> Callable[..., Any]:
        inner = self.wrap(INLINE, function)

        def projection(*args: Any, **kwargs: Any) -> Any:
            if self.active:
                raise RuntimeError("stage-1 harness measures exactly one projection")
            self.active = True
            try:
                return inner(*args, **kwargs)
            finally:
                self.active = False
        return projection

    def git(self, run: Callable[..., Any]) -> Callable[..., Any]:
        def counted(*args: Any, **kwargs: Any) -> Any:
            argv = args[0] if args else kwargs.get("args")
            if not self.active or not isinstance(argv, (list, tuple)) or not argv or argv[0] != "git":
                return run(*args, **kwargs)
            subcommand = str(argv[1]) if len(argv) > 1 else ""
            started = time.perf_counter()
            try:
                return run(*args, **kwargs)
            finally:
                self.git_calls[subcommand] += 1
                self.git_wall[subcommand] += time.perf_counter() - started
        return counted

    def report(self) -> dict[str, Any]:
        segments = {name: round(value, 6) for name, value in sorted(self.exclusive.items())}
        return {
            "segments_exclusive_s": segments,
            "segments_sum_s": round(sum(self.exclusive.values()), 6),
            "segment_calls": dict(sorted(self.calls.items())),
            "git_calls": dict(sorted(self.git_calls.items())),
            "git_calls_total": sum(self.git_calls.values()),
            "git_wall_s": {name: round(value, 6) for name, value in sorted(self.git_wall.items())},
            "git_wall_total_s": round(sum(self.git_wall.values()), 6),
            "notes": [
                "segments are exclusive and non-overlapping; their sum is the projection wall time",
                "git_* is time spent inside the segments; never add it to them",
            ],
        }


@contextmanager
def instrumented(root: Path) -> Iterator[Segments]:
    """Install the wrappers for this process; always restore the originals."""
    _reader, queue = base._load_modules(root)
    from i18nlib import production_review_v2_lite_migration as migration
    from i18nlib.production_review_v2_lite_progress import Progress
    modules = {"queue": queue, "migration": migration, "progress": Progress}
    segments = Segments()
    originals: list[tuple[Any, str, Any]] = []

    def replace(owner: Any, name: str, value: Any) -> None:
        originals.append((owner, name, getattr(owner, name)))
        setattr(owner, name, value)

    try:
        for segment, key, name in SEGMENTS:
            owner = modules[key]
            replace(owner, name, segments.wrap(segment, getattr(owner, name)))
        replace(queue, "_projection", segments.root(queue._projection))
        replace(subprocess, "run", segments.git(subprocess.run))
        yield segments
    finally:
        for owner, name, value in reversed(originals):
            setattr(owner, name, value)


def _implementation(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for relative in IMPLEMENTATION_FILES:
        path = root / relative
        hashes[relative] = base._file_sha256(path) if path.is_file() else "<missing>"
    return hashes


def run(root: Path, treeish: str, label: str) -> dict[str, Any]:
    with instrumented(root) as segments:
        result = base.run(root, treeish)
    result = dict(result)
    result["kind"] = KIND
    result["label"] = label
    result["implementation"] = _implementation(root)
    result["stage1"] = segments.report()
    return result


def compare(candidate: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}

    def check(name: str, passed: bool, **evidence: Any) -> None:
        checks[name] = {"passed": bool(passed), **evidence}

    check("same_root", candidate["root"] == baseline["root"],
          candidate=candidate["root"], baseline=baseline["root"])
    check("same_treeish", candidate["treeish"] == baseline["treeish"],
          candidate=candidate["treeish"], baseline=baseline["treeish"])
    for field in base.IDENTITY_FIELDS:
        left, right = candidate["identity"][field], baseline["identity"][field]
        check(f"identity_{field}", left == right, candidate=left, baseline=right)
    check("progress_identical", candidate["progress"] == baseline["progress"])
    check("wall_fraction", candidate["wall_s"] <= baseline["wall_s"] * WALL_FRACTION,
          candidate=candidate["wall_s"], baseline=baseline["wall_s"],
          limit=baseline["wall_s"] * WALL_FRACTION)
    check("peak_self_rss_fraction",
          candidate["peak_self_rss_kib"] <= baseline["peak_self_rss_kib"] * RSS_FRACTION,
          candidate=candidate["peak_self_rss_kib"], baseline=baseline["peak_self_rss_kib"],
          limit=baseline["peak_self_rss_kib"] * RSS_FRACTION)
    check("head_unchanged", bool(candidate["head_unchanged"]))
    check("queue_unchanged", bool(candidate["queue_invariance"]["unchanged"]))
    return {"passed": all(entry["passed"] for entry in checks.values()), "checks": checks,
            "thresholds": {"wall_fraction": WALL_FRACTION, "rss_fraction": RSS_FRACTION}}


def _load_compare(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"--compare file does not exist: {path}")
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SystemExit(f"--compare file is not readable JSON: {path}: {error}")
    if not isinstance(baseline, dict) or baseline.get("kind") != KIND:
        raise SystemExit(f"--compare file is not a {KIND} report")
    return baseline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--treeish", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--label", default="")
    parser.add_argument("--compare", type=Path, default=None)
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    if not (root / ".git").exists():
        raise SystemExit(f"--root is not a Git worktree: {root}")
    baseline = _load_compare(arguments.compare) if arguments.compare is not None else None
    if arguments.output.exists():
        raise SystemExit(f"--output must be fresh: {arguments.output}")
    base._preflight_output(arguments.output)

    report = run(root, arguments.treeish, arguments.label)
    if baseline is not None:
        report["comparison"] = compare(report, baseline)
        report["baseline"] = {"path": str(arguments.compare), "label": baseline.get("label"),
                              "wall_s": baseline["wall_s"],
                              "peak_self_rss_kib": baseline["peak_self_rss_kib"],
                              "implementation": baseline.get("implementation")}
    raw = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.write_text(raw, encoding="utf-8")
    summary = {key: report[key] for key in ("label", "wall_s", "peak_self_rss_kib")}
    summary["stage1"] = {key: report["stage1"][key] for key in
                         ("segments_exclusive_s", "segments_sum_s", "git_calls_total", "git_wall_total_s")}
    summary["report_sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if baseline is not None:
        summary["comparison_passed"] = report["comparison"]["passed"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if baseline is not None and not report["comparison"]["passed"]:
        failed = [name for name, entry in report["comparison"]["checks"].items() if not entry["passed"]]
        print(f"FAILED comparison checks: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
