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
  run_batch_steps.py rollover-chain --limit 80

`rollover-chain` is the one sanctioned exception to the no-closing-steps rule:
a queue rebuild followed by the next batch start, both at the closure HEAD with
no active batch in between.  The rebuild hands its replay to the start, which
re-resolves the commit before reusing it.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib import production_review_v2_lite_queue as queue  # noqa: E402
from i18nlib.cli import main as cli_main  # noqa: E402
from orchestration import make_adjudication as adjudication  # noqa: E402

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
        elif action == "contextual-export" and separator:
            if not value or not Path(value).is_file():
                raise SystemExit(f"ERROR: {action} requires an existing source workset")
            steps.append(["production", "batch", action, "--source-workset", value])
        elif action in NO_INPUT:
            if separator:
                raise SystemExit(f"ERROR: {action} takes no input")
            steps.append(["production", "batch", action])
        else:
            raise SystemExit(
                f"ERROR: {action} is not chainable; run it on its own "
                f"(chainable: {sorted(TAKES_INPUT | NO_INPUT)})")
    return steps


def contextual_adjudication_chain(tokens):
    parser = argparse.ArgumentParser(prog='run_batch_steps.py contextual-adjudication-chain',
                                     allow_abbrev=False)
    for name in ('input', 'spec', 'output', 'source-root'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args(tokens)
    configured_root = os.environ.get('I18N_REPOSITORY_ROOT')
    root = Path(configured_root).resolve() if configured_root else ROOT
    label = 'chain-input-precheck'
    try:
        index_raw = adjudication.facts.ordinary_bytes(args.input)
        index = adjudication.facts.strict_json(index_raw)
        if (not isinstance(index, dict) or not index or
                any(not key.isdecimal() or not isinstance(value, str) or not value
                    for key, value in index.items())):
            raise ValueError('contextual index requires run keys and raw file paths')
        # The CLI still consumes the real index and raw files. Recheck these
        # bytes before and after import; decisions/workset use their frozen read.
        inputs = {args.input: index_raw}
        for value in index.values():
            inputs[Path(value)] = adjudication.facts.ordinary_bytes(value)
        frozen = adjudication.freeze_inputs(args.spec)
        adjudication.fresh_output(root, args.output)
        with queue.carry_projection():
            for label, step in (
                ('contextual-import', ['production', 'batch', 'contextual-import', '--input', str(args.input)]),
                ('generate-adjudication', None),
                ('adjudicate', ['production', 'batch', 'adjudicate', '--input', str(args.output)]),
                ('prepare-evidence', ['production', 'batch', 'prepare-evidence']),
            ):
                started = time.monotonic()
                if label in {'contextual-import', 'generate-adjudication'}:
                    for path, raw in inputs.items():
                        if adjudication.facts.ordinary_bytes(path) != raw:
                            raise ValueError(f'chain input bytes drifted: {path}')
                if step is None:
                    adjudication.generate(root, args.spec, args.output,
                                          source_root=args.source_root, frozen=frozen)
                    code = 0
                else:
                    code = cli_main(step)
                print(f'--- {label}: exit={code} elapsed={time.monotonic() - started:.1f}s',
                      file=sys.stderr)
                if code != 0:
                    print(f'ERROR: {label} failed; remaining steps not run', file=sys.stderr)
                    return code
    except (OSError, ValueError, KeyError, TypeError, adjudication.wp1.ProductionReviewError) as error:
        print(f'ERROR: {label} failed; remaining steps not run: {error}', file=sys.stderr)
        return 1
    return 0


def rollover_chain(tokens):
    parser = argparse.ArgumentParser(prog='run_batch_steps.py rollover-chain', allow_abbrev=False)
    parser.add_argument('--limit', required=True, type=int)
    args = parser.parse_args(tokens)
    if args.limit < 1:
        raise SystemExit('ERROR: --limit must be positive')
    steps = (('queue-rebuild', ['production', 'queue', 'rebuild']),
             ('batch-start', ['production', 'batch', 'start', '--limit', str(args.limit)]))
    with queue.carry_projection():
        for label, step in steps:
            started = time.monotonic()
            code = cli_main(step)
            print(f"--- {label}: exit={code} elapsed={time.monotonic() - started:.1f}s",
                  file=sys.stderr)
            if code != 0:
                print(f"ERROR: {label} failed; remaining steps not run", file=sys.stderr)
                return code
    return 0


def main(argv: list[str] | None = None) -> int:
    tokens = list(sys.argv[1:] if argv is None else argv)
    if tokens and tokens[0] == "contextual-adjudication-chain":
        return contextual_adjudication_chain(tokens[1:])
    if tokens and tokens[0] == "rollover-chain":
        return rollover_chain(tokens[1:])
    steps = parse(tokens)
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
