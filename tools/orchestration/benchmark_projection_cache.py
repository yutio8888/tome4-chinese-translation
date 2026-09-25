#!/usr/bin/env python3
"""Stage-2 projection cache measurement: off / cold / warm, one fresh process each.

``run`` measures exactly one ``queue.projection_and_progress_for(root, commit)``
call inside the ordinary ``batch start`` read scope, in a new process:

* ``off``  -- the cache is disabled for the call (no read, no write): the same
  complete replay every ordinary command performed before stage 2;
* ``cold`` -- the cache is on and this harness first removes this module's own
  cache files, so the call misses, replays and publishes;
* ``warm`` -- the cache is on and a file published by an earlier process must
  exist; the call must hit.  A warm run that misses is a failed sample, never
  silently timed as a replay.

It reuses ``benchmark_projection``'s identity digests, complete progress and
HEAD/queue/checkpoint guards (an active checkpoint refuses to run).  It never
writes the queue, a checkpoint or evidence.  ``compare`` checks a set of
samples against this task's frozen thresholds: identical identity/progress for
every sample, warm median wall <= 20% of off, cold median wall and median peak
RSS <= 110% of off.  Thresholds are never relaxed after seeing results.

Usage::

    python3 -B tools/orchestration/benchmark_projection_cache.py run \\
      --mode off|cold|warm --root <repo> --treeish <commit> --output <json>
    python3 -B tools/orchestration/benchmark_projection_cache.py compare \\
      --output <json> <sample.json>...
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import statistics
import sys
import time
from pathlib import Path
from typing import Any

PROCESS_STARTED = time.monotonic()
TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from orchestration import benchmark_projection as base  # noqa: E402

KIND = "projection_cache_benchmark"
SUMMARY_KIND = "projection_cache_benchmark_summary"
MODES = ("off", "cold", "warm")
WARM_FRACTION = 0.20
COLD_WALL_FRACTION = 1.10
COLD_RSS_FRACTION = 1.10


def _audit_opens(root: Path, sink: list[str], active: list[bool]) -> None:
    git_dir = str((root / ".git").resolve())

    def hook(event: str, arguments: tuple) -> None:
        if not active[0] or event != "open" or not arguments:
            return
        path = arguments[0]
        if isinstance(path, bytes):
            path = os.fsdecode(path)
        if isinstance(path, str):
            resolved = os.path.realpath(path)
            if not resolved.startswith(git_dir):
                sink.append(resolved)

    sys.addaudithook(hook)


def _own_cache_files(cache, root: Path) -> list[Path]:
    directory = cache.cache_directory(root)
    if not directory.is_dir() or directory.is_symlink():
        return []
    return [path for path in directory.iterdir()
            if cache._NAME.fullmatch(path.name) and path.is_file() and not path.is_symlink()]


def run(mode: str, root: Path, treeish: str, *, audit: bool) -> dict[str, Any]:
    commit = base._commit(root, treeish)
    if mode == "off":
        os.environ.pop("I18N_PROJECTION_CACHE", None)
    else:
        os.environ["I18N_PROJECTION_CACHE"] = "on"
    _reader, queue = base._load_modules(root)
    from i18nlib import projection_cache as cache
    imported = time.monotonic()

    head_before = base._git(root, "rev-parse", "HEAD")
    queue_before = base._queue_state(root)
    if queue_before["checkpoint_present"]:
        raise SystemExit("refusing to benchmark with an active queue checkpoint")
    removed: list[str] = []
    if mode == "cold":
        for path in _own_cache_files(cache, root):
            path.unlink()
            removed.append(path.name)
    present = sorted(path.name for path in _own_cache_files(cache, root))
    if mode == "warm" and not any(name.startswith(f"v1-{commit}-") for name in present):
        raise SystemExit("warm run needs a cache file for this commit from an earlier process")

    opened: list[str] = []
    active = [False]
    if audit:
        _audit_opens(root, opened, active)
    cache.events.clear()
    times_before = os.times()
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
    active[0] = True
    start = time.monotonic()
    with cache.entry_scope("batch", "start"):
        if mode == "off":
            with cache.disabled():
                projection, progress = queue.projection_and_progress_for(root, commit)
        else:
            projection, progress = queue.projection_and_progress_for(root, commit)
    wall = time.monotonic() - start
    active[0] = False
    times_after = os.times()
    usage_after = resource.getrusage(resource.RUSAGE_SELF)
    events = [dict(event) for event in cache.events]

    head_after = base._git(root, "rev-parse", "HEAD")
    queue_after = base._queue_state(root)
    if head_before != head_after:
        raise SystemExit(f"HEAD moved during the measurement: {head_before} -> {head_after}")
    if queue_before != queue_after:
        raise SystemExit("queue/checkpoint state changed during a read-only measurement")
    expected = {"off": [], "cold": ["miss", "stored"], "warm": ["hit"]}[mode]
    observed = [event["event"] for event in events]
    if observed != expected:
        raise SystemExit(f"{mode} run observed cache events {events}, expected {expected}")

    evidence_head, manifest, entries, overrides, reconciliation = projection
    if evidence_head != commit:
        raise SystemExit(f"projection resolved {evidence_head}, expected {commit}")
    try:
        code_identity = cache.implementation_identity()["code_sha256"]
    except cache._Skip as reason:
        code_identity = f"<unavailable: {reason}>"
    files = sorted(path for path in _own_cache_files(cache, root)
                   if path.name.startswith(f"v1-{commit}-"))
    return {
        "kind": KIND,
        "mode": mode,
        "root": str(root),
        "treeish": commit,
        "process": os.getpid(),
        "wall_s": wall,
        "import_s": imported - PROCESS_STARTED,
        "process_elapsed_s": time.monotonic() - PROCESS_STARTED,
        "self_user_s": times_after.user - times_before.user,
        "children_user_s": times_after.children_user - times_before.children_user,
        "self_sys_s": times_after.system - times_before.system,
        "children_sys_s": times_after.children_system - times_before.children_system,
        "peak_self_rss_kib": usage_after.ru_maxrss,
        "self_major_faults": usage_after.ru_majflt - usage_before.ru_majflt,
        "identity": {
            "head": evidence_head,
            "catalog_id": manifest["catalog_id"],
            "entries_n": len(entries),
            "overrides_n": len(overrides),
            "reconciliation_n": len(reconciliation),
            "entries_d": base._digest(list(entries)),
            "entries_type": type(entries).__name__,
            "entry_digests_d": base._digest(sorted(entries.digest_by_revision.items())),
            "overrides_d": base._digest(overrides),
            "reconciliation_d": base._digest(reconciliation),
        },
        "progress": progress,
        "cache_events": events,
        "cache_files_before": present,
        "cache_files_removed": removed,
        "cache_file_bytes": {path.name: path.stat().st_size for path in files},
        "implementation_code_sha256": code_identity,
        "harness_sha256": base._file_sha256(Path(__file__)),
        "opened_files": sorted(set(opened)) if audit else None,
        "head_before": head_before,
        "head_after": head_after,
        "head_unchanged": head_before == head_after,
        "queue_invariance": {"before": queue_before, "after": queue_after,
                             "unchanged": queue_before == queue_after},
        "limits": [
            "wall_s is one projection_and_progress_for call; process_elapsed_s adds start-up and imports.",
            "peak_self_rss_kib is RUSAGE_SELF.ru_maxrss of this process, not sampled RSS.",
            "OS page cache is not controlled; every mode is prepared the same way.",
        ],
    }


def compare(samples: list[dict[str, Any]]) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}

    def check(name: str, passed: bool, **evidence: Any) -> None:
        checks[name] = {"passed": bool(passed), **evidence}

    by_mode = {mode: [sample for sample in samples if sample["mode"] == mode] for mode in MODES}
    check("every_mode_sampled", all(by_mode.values()),
          counts={mode: len(items) for mode, items in by_mode.items()})
    first = samples[0]
    for field in ("root", "treeish", "implementation_code_sha256", "harness_sha256"):
        values = sorted({str(sample[field]) for sample in samples})
        check(f"same_{field}", len(values) == 1, values=values)
    identities = {json.dumps(sample["identity"], sort_keys=True) for sample in samples}
    check("identity_identical", len(identities) == 1, distinct=len(identities))
    progresses = {json.dumps(sample["progress"], sort_keys=True) for sample in samples}
    check("progress_identical", len(progresses) == 1, distinct=len(progresses))
    check("head_and_queue_unchanged", all(sample["head_unchanged"] and
                                          sample["queue_invariance"]["unchanged"]
                                          for sample in samples))

    def median(mode: str, field: str) -> float | None:
        values = [sample[field] for sample in by_mode[mode]]
        return statistics.median(values) if values else None

    stats = {mode: {field: {"median": median(mode, field),
                            "min": min((s[field] for s in by_mode[mode]), default=None),
                            "max": max((s[field] for s in by_mode[mode]), default=None),
                            "n": len(by_mode[mode])}
                    for field in ("wall_s", "process_elapsed_s", "peak_self_rss_kib")}
             for mode in MODES}
    if all(by_mode.values()):
        off_wall, off_rss = median("off", "wall_s"), median("off", "peak_self_rss_kib")
        check("warm_wall_fraction", median("warm", "wall_s") <= off_wall * WARM_FRACTION,
              warm=median("warm", "wall_s"), off=off_wall, limit=off_wall * WARM_FRACTION)
        check("cold_wall_fraction", median("cold", "wall_s") <= off_wall * COLD_WALL_FRACTION,
              cold=median("cold", "wall_s"), off=off_wall, limit=off_wall * COLD_WALL_FRACTION)
        check("cold_rss_fraction", median("cold", "peak_self_rss_kib") <= off_rss * COLD_RSS_FRACTION,
              cold=median("cold", "peak_self_rss_kib"), off=off_rss, limit=off_rss * COLD_RSS_FRACTION)
    return {"kind": SUMMARY_KIND, "root": first["root"], "treeish": first["treeish"],
            "passed": all(entry["passed"] for entry in checks.values()), "checks": checks,
            "statistics": stats,
            "thresholds": {"warm_wall_fraction": WARM_FRACTION,
                           "cold_wall_fraction": COLD_WALL_FRACTION,
                           "cold_rss_fraction": COLD_RSS_FRACTION}}


def _load_sample(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SystemExit(f"sample is not readable JSON: {path}: {error}")
    if not isinstance(value, dict) or value.get("kind") != KIND or value.get("mode") not in MODES:
        raise SystemExit(f"not a {KIND} report: {path}")
    return value


def _write(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    measure = commands.add_parser("run")
    measure.add_argument("--mode", required=True, choices=MODES)
    measure.add_argument("--root", required=True, type=Path)
    measure.add_argument("--treeish", required=True)
    measure.add_argument("--output", required=True, type=Path)
    measure.add_argument("--audit-opens", action="store_true",
                         help="record files opened during the call (outside .git)")
    summary = commands.add_parser("compare")
    summary.add_argument("--output", required=True, type=Path)
    summary.add_argument("samples", nargs="+", type=Path)
    arguments = parser.parse_args(argv)

    if arguments.command == "compare":
        report = compare([_load_sample(path) for path in arguments.samples])
        report["samples"] = [str(path) for path in arguments.samples]
        _write(arguments.output, report)
        print(json.dumps({key: report[key] for key in ("passed", "checks", "statistics")},
                         ensure_ascii=False, indent=2))
        return 0 if report["passed"] else 1

    root = arguments.root.resolve()
    if not (root / ".git").exists():
        raise SystemExit(f"--root is not a Git worktree: {root}")
    if arguments.output.exists():
        raise SystemExit(f"--output already exists; samples are never overwritten: {arguments.output}")
    base._preflight_output(arguments.output)
    report = run(arguments.mode, root, arguments.treeish, audit=arguments.audit_opens)
    _write(arguments.output, report)
    print(json.dumps({key: report[key] for key in ("mode", "wall_s", "process_elapsed_s",
                                                    "peak_self_rss_kib", "cache_events")},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
