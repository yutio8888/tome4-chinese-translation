#!/usr/bin/env python3
"""Function-level profile of exactly one complete, cache-off projection replay.

A diagnostic companion to ``benchmark_projection``: the same single
``queue._projection(root, commit, progress={})`` call, the same HEAD and
queue/checkpoint guards (an active checkpoint refuses to run), but with
``cProfile`` enabled around that call only.  The projection cache is forced
off for the process and the call runs inside ``projection_cache.disabled()``,
so nothing is read from or written to the cache; the queue, checkpoints and
evidence are never written.

This measures where time goes; it is not an acceptance benchmark.  cProfile
adds per-call overhead, so ``wall_s`` here is inflated relative to an
unprofiled run and must never be compared with ``benchmark_projection``
samples or used as a baseline.

``--no-profile`` runs the identical call without cProfile and writes only
``summary.json`` (kind ``projection_timing``).  The i18nlib modules are always
imported from the ``tools/`` directory that contains this script, and the
report lists every such module actually loaded with its SHA-256, so two timing
samples are comparable only when they differ in exactly the intended files.
Running a copy of ``tools/`` in which some files are an earlier revision
therefore times that earlier implementation against the same repository.

Usage::

    python3 -B tools/orchestration/profile_projection.py \\
      --root <repo> --treeish <commit> --output-dir <fresh dir> [--top 40] [--no-profile]

Writes ``<dir>/profile.pstats`` (loadable with ``pstats``) and
``<dir>/summary.json`` (identity, resources, progress, top functions by
exclusive and cumulative time, and git subprocess time).
"""
from __future__ import annotations

import argparse
import cProfile
import hashlib
import json
import os
import pstats
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from orchestration import benchmark_projection as base  # noqa: E402

KIND = "projection_profile"
TIMING_KIND = "projection_timing"
CACHE_ENVIRONMENT = ("I18N_PROJECTION_CACHE", "I18N_PROJECTION_CACHE_TRACE")


def _label(function: tuple[str, int, str], root: Path) -> str:
    filename, line, name = function
    if filename == "~":
        return name
    try:
        filename = Path(filename).resolve().relative_to(root).as_posix()
    except ValueError:
        pass
    return f"{filename}:{line}({name})"


def _rows(stats: pstats.Stats, root: Path, key: int, top: int) -> list[dict[str, Any]]:
    # stats.stats: function -> (primitive calls, total calls, tottime, cumtime, callers)
    ordered = sorted(stats.stats.items(), key=lambda item: item[1][key], reverse=True)[:top]
    return [{"function": _label(function, root), "primitive_calls": cc, "calls": nc,
             "tottime_s": round(tt, 6), "cumtime_s": round(ct, 6)}
            for function, (cc, nc, tt, ct, _callers) in ordered]


def _subprocess_time(stats: pstats.Stats) -> dict[str, Any]:
    """Time blocked in child processes, as seen from the profiled parent."""
    waits = [(function, value) for function, value in stats.stats.items()
             if function[2] in {"_communicate", "wait", "communicate"}
             and function[0].endswith("subprocess.py")]
    runs = [value for function, value in stats.stats.items()
            if function[2] == "run" and function[0].endswith("subprocess.py")]
    return {"subprocess_run_calls": sum(value[1] for value in runs),
            "subprocess_run_cumtime_s": round(sum(value[3] for value in runs), 6),
            "wait_like_cumtime_s": round(sum(value[3] for _function, value in waits), 6)}


def _loaded_implementation(root: Path) -> dict[str, str]:
    """SHA-256 of every module loaded from this harness's own ``tools/``.

    Refuses a run in which any ``i18nlib`` module, or any module from the
    measured repository's own ``tools/``, came from elsewhere, so the report
    always names the implementation that was actually timed.
    """
    repository_tools = (root / "tools").resolve()
    loaded: dict[str, str] = {}
    for name, module in sorted(sys.modules.items()):
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        path = Path(filename).resolve()
        try:
            relative = path.relative_to(TOOLS)
        except ValueError:
            if (name == "i18nlib" or name.startswith("i18nlib.") or
                    path.is_relative_to(repository_tools)):
                raise SystemExit(f"{name} was not loaded from {TOOLS}: {path}")
            continue
        loaded[relative.as_posix()] = base._file_sha256(path)
    return loaded


def run(root: Path, treeish: str, output_dir: Path, top: int, *,
        profile: bool = True) -> dict[str, Any]:
    for name in CACHE_ENVIRONMENT:
        os.environ.pop(name, None)
    # Import from this script's tools/ before base._load_modules puts the
    # repository's tools/ first on sys.path.
    from i18nlib import production_review_v2_lite_queue  # noqa: F401
    _reader, queue = base._load_modules(root)
    from i18nlib import projection_cache as cache

    profiler = cProfile.Profile()
    original = queue._projection
    calls = []

    def profiled(*args: Any, **kwargs: Any) -> Any:
        if calls:
            raise RuntimeError("profile harness measures exactly one projection")
        calls.append(1)
        with cache.disabled():
            if not profile:
                return original(*args, **kwargs)
            profiler.enable()
            try:
                return original(*args, **kwargs)
            finally:
                profiler.disable()

    queue._projection = profiled
    try:
        result = base.run(root, treeish)
    finally:
        queue._projection = original
    if calls != [1]:
        raise SystemExit("profile harness did not observe exactly one projection")
    if cache.events:
        raise SystemExit(f"projection cache was consulted during a cache-off profile: {cache.events}")
    result = dict(result)
    result["loaded_implementation"] = _loaded_implementation(root)
    result["progress_sha256"] = hashlib.sha256(json.dumps(
        result["progress"], ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    if not profile:
        result["kind"] = TIMING_KIND
        result["limits"] = list(result.get("limits", [])) + [
            "No profiler: wall_s is one unprofiled _projection call in a fresh process.",
            "The projection cache is off (environment removed and projection_cache.disabled()).",
        ]
        return result

    pstats_path = output_dir / "profile.pstats"
    profiler.dump_stats(str(pstats_path))
    stats = pstats.Stats(str(pstats_path))
    result["kind"] = KIND
    result["profile"] = {
        "pstats": pstats_path.name,
        "pstats_sha256": base._file_sha256(pstats_path),
        "total_tt_s": round(stats.total_tt, 6),
        "function_count": len(stats.stats),
        "top_tottime": _rows(stats, root, 2, top),
        "top_cumtime": _rows(stats, root, 3, top),
        "subprocess": _subprocess_time(stats),
    }
    result["limits"] = list(result.get("limits", [])) + [
        "cProfile is enabled around the single _projection call; wall_s includes its overhead "
        "and is not comparable with unprofiled benchmark samples.",
        "The projection cache is off (environment removed and projection_cache.disabled()).",
    ]
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--treeish", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--top", type=int, default=40)
    parser.add_argument("--no-profile", action="store_true",
                        help="time the same single call without cProfile; writes only summary.json")
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    if not (root / ".git").exists():
        raise SystemExit(f"--root is not a Git worktree: {root}")
    if arguments.top < 1:
        raise SystemExit("--top must be positive")
    output_dir = arguments.output_dir
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise SystemExit(f"--output-dir must be absent or an empty directory: {output_dir}")
    summary_path = output_dir / "summary.json"
    base._preflight_output(summary_path)

    report = run(root, arguments.treeish, output_dir, arguments.top,
                 profile=not arguments.no_profile)
    raw = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    summary_path.write_text(raw, encoding="utf-8")
    brief = {key: report[key] for key in ("kind", "treeish", "wall_s", "total_user_s", "peak_self_rss_kib",
                                          "progress_sha256")}
    brief["identity"] = report["identity"]
    if "profile" in report:
        brief["top_tottime"] = report["profile"]["top_tottime"][:10]
    brief["summary_sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    print(json.dumps(brief, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
