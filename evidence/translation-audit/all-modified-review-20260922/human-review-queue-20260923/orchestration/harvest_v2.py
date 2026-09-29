#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest and validate v2 contextual results from raw agent logs.

The reviewer output should be a single compact JSON object, but agents sometimes
emit prose, heredocs, fenced fragments or a follow-up partial object, and key
order is not fixed. This walks back from every candidate start and keeps the
object that is contract, identity and coverage exact for its envelope.
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def _extract(text, brace_index):
    depth = 0
    instr = False
    esc = False
    for k in range(brace_index, len(text)):
        ch = text[k]
        if instr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                instr = False
            continue
        if ch == '"':
            instr = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[brace_index : k + 1]
    return None


def objects(text):
    """Every balanced object reachable by walking back from a payload marker."""
    starts = set()
    for pattern in (r'\{\s*"', r'"candidate_identity"', r'"contract"', r'"verdicts"'):
        for m in re.finditer(pattern, text):
            start = m.start()
            while start > 0 and text[start] != "{":
                start -= 1
            if text[start] == "{":
                starts.add(start)
    out = []
    seen = set()
    for start in sorted(starts):
        piece = _extract(text, start)
        if piece is None or piece in seen:
            continue
        seen.add(piece)
        out.append(piece)
    return out


def validate(obj_text, envelope):
    try:
        d = json.loads(obj_text)
    except ValueError:
        return None
    if not isinstance(d, dict) or set(d) != {"contract", "candidate_identity", "verdicts"}:
        return None
    if d["contract"] != "translation_contextual_v2":
        return None
    keys = envelope["payload"]["ordered_revision_keys"]
    if d["candidate_identity"] != envelope["candidate_identity"]:
        return None
    verdicts = d["verdicts"]
    if not isinstance(verdicts, list) or len(verdicts) != len(keys):
        return None
    for index, v in enumerate(verdicts):
        if not isinstance(v, dict) or v.get("revision_key") != keys[index]:
            return None
        if v.get("verdict") not in ("OK", "ISSUE"):
            return None
        allowed = {"revision_key", "verdict"} | ({"observation"} if v["verdict"] == "ISSUE" else set())
        if set(v) != allowed:
            return None
        if v["verdict"] == "ISSUE" and not str(v.get("observation", "")).strip():
            return None
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task_ids", nargs="+")
    ap.add_argument("--reviews-root", default=str(REPO / ".ai" / "reviews"))
    ap.add_argument("--task-root", default=str(REPO / ".ai" / "task"))
    ap.add_argument("--dispatch-id", default="full-01")
    args = ap.parse_args()

    ok = 0
    for tid in args.task_ids:
        raw_path = Path(args.reviews_root) / tid / f"raw-{args.dispatch_id}.txt"
        env_path = Path(args.task_root) / tid / f"CONTEXTUAL-ENVELOPE-{args.dispatch_id}.json"
        if not raw_path.exists() or not env_path.exists():
            print(f"MISSING            {tid}")
            continue
        envelope = json.loads(env_path.read_text(encoding="utf-8"))
        text = raw_path.read_text(encoding="utf-8", errors="replace")
        found = [v for v in (validate(o, envelope) for o in objects(text)) if v]
        if not found:
            print(f"INVALID            {tid}  (no contract/identity/coverage-exact object)")
            continue
        best = found[0]
        out_path = Path(args.reviews_root) / tid / f"parsed-{args.dispatch_id}.json"
        out_path.write_text(json.dumps(best, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        issues = [v["revision_key"] for v in best["verdicts"] if v["verdict"] == "ISSUE"]
        print(f"VALID              {tid}  revisions={len(best['verdicts'])} issues={len(issues)} {issues}")
        ok += 1
    print(f"\nvalid {ok}/{len(args.task_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
