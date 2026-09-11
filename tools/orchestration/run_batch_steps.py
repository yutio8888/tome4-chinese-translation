#!/usr/bin/env python3
"""Run a declared sequence of production batch actions in one process.

Each action is dispatched through the ordinary CLI entry point, so every step
validates the active batch exactly as it does when run on its own.  The only
thing shared across steps is one replay of the evidence commit, and
`queue.projection_for` re-resolves that commit before every reuse — a HEAD that
moves mid-sequence replays instead of reusing a stale value.

Running the same steps as separate `tools/i18n production batch <action>`
processes stays valid and is the fallback whenever this wrapper is in doubt:
the active checkpoint, not this process, is the recovery authority, so a step
that fails here leaves exactly the state it would leave on its own.

Usage:
  run_batch_steps.py surface-import=/tmp/idx.json contextual-export
  run_batch_steps.py adjudicate=/tmp/adj.json prepare-evidence
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib import production_review_v2_lite_queue as queue  # noqa: E402
from i18nlib.cli import main as cli_main  # noqa: E402

# Only actions that are safe to chain: each one leaves a checkpoint the next
# step re-validates.  Steps that move HEAD or close the batch are deliberately
# absent — run those on their own.
TAKES_INPUT = {"surface-import", "contextual-import", "adjudicate"}
NO_INPUT = {"surface-export", "contextual-export", "prepare-evidence"}


def parse(tokens: list[str]) -> list[list[str]]:
    if not tokens:
        raise SystemExit("usage: run_batch_steps.py <action>[=<input>] ...")
    steps = []
    for token in tokens:
        action, separator, value = token.partition("=")
        if action in TAKES_INPUT:
            if not separator or not value:
                raise SystemExit(f"ERROR: {action} requires =<input path>")
            if not Path(value).is_file():
                raise SystemExit(f"ERROR: {action} input is not a file: {value}")
            steps.append(["production", "batch", action, "--input", value])
        elif action in NO_INPUT:
            if separator:
                raise SystemExit(f"ERROR: {action} takes no input")
            steps.append(["production", "batch", action])
        else:
            raise SystemExit(
                f"ERROR: {action} is not chainable; run it on its own "
                f"(chainable: {sorted(TAKES_INPUT | NO_INPUT)})")
    return steps


def main(argv: list[str] | None = None) -> int:
    steps = parse(list(sys.argv[1:] if argv is None else argv))
    with queue.carry_projection():
        for step in steps:
            label = step[2]
            started = time.monotonic()
            code = cli_main(step)
            print(f"--- {label}: exit={code} elapsed={time.monotonic() - started:.1f}s",
                  file=sys.stderr)
            if code != 0:
                print(f"ERROR: {label} failed; remaining steps not run", file=sys.stderr)
                return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
