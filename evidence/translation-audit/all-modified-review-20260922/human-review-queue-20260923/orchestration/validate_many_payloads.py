#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate many contextual payloads in one process, parsing each Lua file once.

`tools/contextual_anchor_preflight.py` re-reads and re-scans every scoped Lua file
on every invocation, so validating N bundles one-by-one costs N full scans. This
reuses the tool's own scanner and check helpers but shares the parse across
payloads, which keeps CPU bounded.
"""
import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools"))
import contextual_anchor_preflight as P  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(REPO))
    ap.add_argument("specs", nargs="+", help="SCOPE.json=PAYLOAD.json pairs")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    parsed_files: dict[str, str] = {}
    calls_by_scope: dict[tuple[str, str], list] = {}
    results = []
    for spec in args.specs:
        task = spec.split("=")[0]
        scope_path, payload_path = spec.split("=")[1], spec.split("=")[2]
        try:
            scope = P._read_json(Path(scope_path), "scope")
            payload = P._read_json(Path(payload_path), "payload")
            sources = P._validate_payload(payload)
            scopes, _ = P._validate_scope(scope, root)
            in_scope = []
            for anchor in scopes:
                f = anchor["file"]
                if f not in parsed_files:
                    parsed_files[f] = (root / f).read_text(encoding="utf-8")
                key = (f, anchor["section_path"])
                if key not in calls_by_scope:
                    calls_by_scope[key] = P._allowed_calls(
                        parsed_files[f], anchor["section_path"], anchor["ordered_titles"]
                    )
                in_scope.extend(calls_by_scope[key])
            missing = [s for s in sources if not any(c.source == s for c in in_scope)]
            if missing:
                results.append((task, "PREFLIGHT_FAILED", f"source absent: {missing[0]!r}"))
                continue
            problems = []
            for index, (key, source) in enumerate(zip(payload["ordered_revision_keys"], sources)):
                matches = [c for c in in_scope if c.source == source]
                orders = {c.args_order for c in matches}
                if len(orders) > 1:
                    problems.append(f"{key}: differing args_order")
                    continue
                order = next(iter(orders))
                context = payload["bounded_context"][index]["context"]
                tokens, malformed = P._tokenize_args_order_disclosures(context)
                if order is None:
                    if malformed or tokens:
                        problems.append(f"{key}: must not contain args_order=")
                else:
                    expected = f"args_order={order}"
                    if malformed or any(t != expected for t in tokens) or expected not in tokens:
                        problems.append(f"{key}: must contain exactly {expected!r}")
            results.append((task, "PREFLIGHT_FAILED" if problems else "PREFLIGHT_VERIFIED",
                            problems[0] if problems else ""))
        except (P.InputError, P.PreflightFailure, OSError, ValueError) as error:
            results.append((task, "INPUT_ERROR", str(error)))

    ok = sum(1 for _, s, _ in results if s == "PREFLIGHT_VERIFIED")
    for task, status, detail in results:
        print(f"{status:18} {task}" + (f"  {detail}" if detail else ""))
    print(f"\nverified {ok}/{len(results)}  (lua files parsed: {len(parsed_files)})")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
