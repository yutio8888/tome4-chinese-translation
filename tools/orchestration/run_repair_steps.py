#!/usr/bin/env python3
"""Run bounded repair preflights or one migration chain with measured replay.

Every step is the ordinary production CLI action.  The wrapper contributes
only argument preflight, a process-local projection carry scope, and timing.
The CLI remains responsible for locks, input validation, SQLite validation,
transactions, and recovery artifacts.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.i18nlib import production_review as wp1  # noqa: E402
from tools.i18nlib import production_review_v2_lite_migration as migration  # noqa: E402
from tools.i18nlib import production_review_v2_lite_queue as queue  # noqa: E402
from tools.i18nlib.cli import main as cli_main  # noqa: E402

TIMING_KIND = "production_repair_step_timing_v1"
TIMING_WRITE_EXIT = 9


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_repair_steps.py", allow_abbrev=False)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight", allow_abbrev=False)
    preflight.add_argument("--batch-id", action="append", required=True)
    preflight.add_argument("--output", action="append", required=True, type=Path)
    preflight.add_argument("--timing-output", required=True, type=Path)
    preflight.add_argument("--version-manifest", default="tome-1.7.6")
    preflight.add_argument("--manifest", type=Path)

    chain = subparsers.add_parser("migration-chain", allow_abbrev=False)
    chain.add_argument("--candidate-catalog", required=True, type=Path)
    chain.add_argument("--migration-output", required=True, type=Path)
    chain.add_argument("--timing-output", required=True, type=Path)
    chain.add_argument("--recorded-at")
    chain.add_argument("--recorded-by", default="WP2L-5 EXECUTOR")

    # Queue rebuild, candidate catalog build and the migration chain all run
    # at the translation commit; the rebuild's replay serves the plan.
    publish = subparsers.add_parser("publish-chain", allow_abbrev=False)
    publish.add_argument("--candidate-catalog", required=True, type=Path)
    publish.add_argument("--migration-output", required=True, type=Path)
    publish.add_argument("--timing-output", required=True, type=Path)
    publish.add_argument("--recorded-at")
    publish.add_argument("--recorded-by", default="WP2L-5 EXECUTOR")
    publish.add_argument("--catalog-recorded-by", required=True)
    return parser


def _root() -> Path:
    configured = os.environ.get("I18N_REPOSITORY_ROOT")
    root = Path(configured).resolve() if configured else ROOT
    if not root.is_dir():
        raise SystemExit(f"ERROR: repository root is not an ordinary directory: {root}")
    return root


def _key(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _temporary(path: Path) -> Path:
    destination = _key(path)
    return destination.with_name("." + destination.name + ".tmp")


def _fresh_output(root: Path, path: Path, label: str) -> None:
    destination = migration._safe_output(root, path)
    temporary = _temporary(destination)
    runtime = _key(root / queue.RUNTIME_RELATIVE)
    for candidate in (destination, temporary):
        try:
            candidate.relative_to(runtime)
        except ValueError:
            continue
        raise SystemExit(
            f"ERROR: {label} and its temporary path must be outside "
            f"the production mutable state directory: {path}")
    if destination.exists() or destination.is_symlink():
        raise SystemExit(f"ERROR: {label} must be fresh: {path}")
    if temporary.exists() or temporary.is_symlink():
        raise SystemExit(f"ERROR: {label} temporary path is occupied: {temporary}")


def _unique_paths(paths: list[tuple[str, Path]]) -> None:
    seen: dict[Path, str] = {}
    for label, path in paths:
        key = _key(path)
        if key in seen:
            raise SystemExit(f"ERROR: output/input path collision: {seen[key]} and {label}: {path}")
        for prior, prior_label in seen.items():
            if prior in key.parents or key in prior.parents:
                raise SystemExit(
                    f"ERROR: output/input path hierarchy collision: "
                    f"{prior_label} and {label}: {path}")
        seen[key] = label


def _reject_descendant(path: Path, directory: Path, label: str) -> None:
    try:
        _key(path).relative_to(_key(directory))
    except ValueError:
        return
    raise SystemExit(f"ERROR: {label} must not be inside the candidate catalog: {path}")


def _precheck(root: Path, args: argparse.Namespace) -> list[tuple[str, list[str]]]:
    if args.command == "preflight":
        if not 1 <= len(args.batch_id) <= 3:
            raise SystemExit("ERROR: preflight requires one to three --batch-id values")
        if len(args.output) != len(args.batch_id):
            raise SystemExit("ERROR: preflight requires one --output per --batch-id")
        if len(set(args.batch_id)) != len(args.batch_id):
            raise SystemExit("ERROR: preflight batch ids must be distinct")
        for batch_id in args.batch_id:
            migration._batch_id(batch_id)
        outputs = [(f"output[{index}]", path) for index, path in enumerate(args.output)]
        outputs.append(("timing-output", args.timing_output))
        paths = [item for label, path in outputs
                 for item in ((label, path), (label + " temporary", _temporary(path)))]
        if args.manifest is not None:
            if args.manifest.is_symlink() or not args.manifest.is_file():
                raise SystemExit(f"ERROR: manifest is not an ordinary file: {args.manifest}")
            paths.append(("manifest", args.manifest))
        _unique_paths(paths)
        for label, path in outputs:
            _fresh_output(root, path, label)
        common = ["--version-manifest", args.version_manifest]
        if args.manifest is not None:
            common.extend(["--manifest", str(args.manifest)])
        return [(f"preflight:{batch_id}", [
            "production", "repair", "preflight", "--batch-id", batch_id,
            "--output", str(output), *common,
        ]) for batch_id, output in zip(args.batch_id, args.output)]

    publishing = args.command == "publish-chain"
    if publishing:
        _fresh_output(root, args.candidate_catalog, "candidate-catalog")
    elif args.candidate_catalog.is_symlink() or not args.candidate_catalog.is_dir():
        raise SystemExit(
            f"ERROR: candidate catalog is not an ordinary directory: {args.candidate_catalog}")
    outputs = [("migration-output", args.migration_output),
               ("timing-output", args.timing_output)]
    paths = [("candidate-catalog", args.candidate_catalog), *[
        item for label, path in outputs
        for item in ((label, path), (label + " temporary", _temporary(path)))]]
    _unique_paths(paths)
    _reject_descendant(args.migration_output, args.candidate_catalog, "migration-output")
    _reject_descendant(args.timing_output, args.candidate_catalog, "timing-output")
    _fresh_output(root, args.migration_output, "migration-output")
    _fresh_output(root, args.timing_output, "timing-output")
    plan = ["production", "migration", "plan", "--candidate-catalog",
            str(args.candidate_catalog), "--output", str(args.migration_output),
            "--recorded-by", args.recorded_by]
    if args.recorded_at is not None:
        plan.extend(["--recorded-at", args.recorded_at])
    shared = ["--input", str(args.migration_output), "--candidate-catalog",
              str(args.candidate_catalog)]
    steps = [("migration:plan", plan),
             ("migration:check", ["production", "migration", "check", *shared]),
             ("migration:apply", ["production", "migration", "apply", *shared])]
    if publishing:
        build = ["production", "authoritative-catalog", "build", "--output",
                 str(args.candidate_catalog), "--recorded-by", args.catalog_recorded_by]
        if args.recorded_at is not None:
            build.extend(["--recorded-at", args.recorded_at])
        steps = [("queue:rebuild", ["production", "queue", "rebuild"]),
                 ("catalog:build", build), *steps]
    return steps


@contextmanager
def _measure_projections(samples: list[float]) -> Iterator[None]:
    """Wrap the real replay implementation; never replace or shortcut it."""
    original = queue._projection

    def measured(*args: Any, **kwargs: Any):
        started = time.perf_counter()
        try:
            return original(*args, **kwargs)
        finally:
            samples.append(time.perf_counter() - started)

    queue._projection = measured
    try:
        yield
    finally:
        queue._projection = original


def _write_timing(root: Path, path: Path, report: dict[str, Any]) -> None:
    # Precheck made this destination fresh.  The ordinary safe writer supplies
    # atomic replacement/fsync behavior; checking again prevents this wrapper
    # from overwriting a file created while the chain was running.
    if path.exists() or path.is_symlink() or _temporary(path).exists() or _temporary(path).is_symlink():
        raise RuntimeError(f"timing output ceased to be fresh: {path}")
    migration._write_output(root, path, wp1.canonical_bytes(report))


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(sys.argv[1:] if argv is None else argv)
    root = _root()
    try:
        steps = _precheck(root, args)
    except wp1.ProductionReviewError as error:
        raise SystemExit(f"ERROR: {error}") from error
    samples: list[float] = []
    records: list[dict[str, Any]] = []
    failure_step: str | None = None
    started_all = time.perf_counter()
    unexpected: BaseException | None = None
    with _measure_projections(samples):
        try:
            with queue.carry_projection():
                for label, command in steps:
                    started = time.perf_counter()
                    try:
                        code = cli_main(command)
                    except BaseException as error:
                        code = 1
                        unexpected = error
                    elapsed = time.perf_counter() - started
                    records.append({"step": label, "exit_code": code,
                                    "elapsed_seconds": elapsed})
                    if code != 0:
                        failure_step = label
                        print(f"ERROR: {label} failed; remaining steps not run", file=sys.stderr)
                        break
        finally:
            elapsed_all = time.perf_counter() - started_all
    report = {
        "schema_version": 1,
        "kind": TIMING_KIND,
        "command": args.command,
        "success": failure_step is None,
        "failure_step": failure_step,
        "elapsed_seconds": elapsed_all,
        "projection_calls": len(samples),
        "projection_elapsed_seconds": sum(samples),
        "projection_samples_seconds": samples,
        "steps": records,
    }
    timing_error: Exception | None = None
    try:
        _write_timing(root, args.timing_output, report)
    except Exception as error:
        timing_error = error
        completed = ", ".join(
            f"{record['step']}(exit={record['exit_code']})" for record in records) or "none"
        print(
            "ERROR: timing report write failed after business execution; "
            f"business steps completed: {completed}; outputs or SQLite changes from completed "
            f"steps may already exist; do not blindly rerun: {error}",
            file=sys.stderr,
        )
    if unexpected is not None:
        raise unexpected
    business_code = 0 if failure_step is None else records[-1]["exit_code"]
    if timing_error is not None and business_code == 0:
        return TIMING_WRITE_EXIT
    return business_code


if __name__ == "__main__":
    raise SystemExit(main())
