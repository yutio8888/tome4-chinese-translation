#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""File-level allowed-files scope check for a Paseo task.

Confirmed-safe, orthogonal item from the P0-3 redesign (see
.ai/task/paseo-provenance-schema-redesign-001/DESIGN.md §4): checks that a set of
changed paths (an EXECUTOR diff, a review candidate diff, etc.) is a subset of the
task's declared allowed_files list. Deliberately does not touch section/anchor-level
provenance (blocked pending the provenance redesign) or STATE schema/DONE closure
(blocked pending the schema decision) - this only answers "did the diff touch files
outside what SPEC authorized."

SCOPE.json format (new, gitignored like the rest of .ai/task/):
    {"allowed_files": ["tome-cults.lua", "docs/foo.md"]}

Usage:
    python3 -B tools/check_allowed_files.py --task-id <id> [--paths PATH [PATH ...]]
    python3 -B tools/check_allowed_files.py --task-id <id>   # reads `git diff --name-only`

Exit code 0 = all changed paths are allowed; 1 = at least one path is out of scope,
or the task has no SCOPE.json (fail closed, not fail open).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_allowed_files(task_id: str) -> list[str]:
    scope_path = ROOT / ".ai" / "task" / task_id / "SCOPE.json"
    if not scope_path.is_file():
        raise FileNotFoundError(
            f"no SCOPE.json for task {task_id!r} at {scope_path} "
            "(fail-closed: a task with no declared allowed_files cannot pass this check)"
        )
    data = json.loads(scope_path.read_text(encoding="utf-8"))
    allowed = data.get("allowed_files")
    if not isinstance(allowed, list) or not allowed:
        raise ValueError(f"{scope_path}: allowed_files must be a non-empty list")
    return [str(p) for p in allowed]


def changed_paths_from_git() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    staged = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    paths = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    paths.update(line.strip() for line in staged.stdout.splitlines() if line.strip())
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="explicit changed paths to check; defaults to `git diff --name-only HEAD` + staged",
    )
    args = parser.parse_args()

    try:
        allowed = load_allowed_files(args.task_id)
    except (FileNotFoundError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    changed = args.paths if args.paths is not None else changed_paths_from_git()
    if not changed:
        print("OK: no changed paths to check")
        return 0

    allowed_set = set(allowed)
    out_of_scope = [p for p in changed if p not in allowed_set]

    if out_of_scope:
        print(f"FAIL: {len(out_of_scope)} changed path(s) outside allowed_files for task {args.task_id!r}:", file=sys.stderr)
        for p in out_of_scope:
            print(f"  - {p}", file=sys.stderr)
        print(f"allowed_files: {allowed}", file=sys.stderr)
        return 1

    print(f"OK: all {len(changed)} changed path(s) are within allowed_files for task {args.task_id!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
