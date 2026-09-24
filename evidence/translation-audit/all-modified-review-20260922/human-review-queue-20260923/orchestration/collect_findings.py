#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect every ISSUE verdict from the v2 review records of the public bundles.

Reads the persisted raw reviewer output bound by each DONE review record and
prints one entry per finding with its source/target and observation, grouped by
bundle and ordered by revision key. Read-only; used by the ORCHESTRATOR before
independent adjudication against the frozen source.
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TASK_ROOT = REPO / ".ai" / "task"
REVIEWS = REPO / ".ai" / "reviews"


def bundle_ids():
    manifest = json.loads(
        (TASK_ROOT / "human-review-adjudication-20260923" / "V2-BUNDLES-PUBLIC.json"
         ).read_text(encoding="utf-8"))
    return sorted(manifest)


def envelope(task_id):
    return json.loads(
        (TASK_ROOT / task_id / "CONTEXTUAL-ENVELOPE-full-01.json").read_text(encoding="utf-8"))


def collect(task_id):
    env = envelope(task_id)
    payload = env["payload"]
    src = dict(zip(payload["ordered_revision_keys"], payload["translation_snapshot"]))
    _ = src
    keys = payload["ordered_revision_keys"]
    snapshot = payload["translation_snapshot"]
    # snapshot is an object array aligned to keys; source/target keys per v2 §2
    table = {}
    for entry in snapshot:
        table[entry.get("revision_key") or entry.get("key")] = entry
    state_path = TASK_ROOT / task_id / "STATE.json"
    dispatch_id = "full-01"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        ptr = (state.get("contextual_reviewers") or [{}])[0]
        dispatch_id = ptr.get("dispatch_id") or dispatch_id
    record_path = REVIEWS / task_id / f"{dispatch_id}.json"
    if not record_path.exists():
        return None
    record = json.loads(record_path.read_text(encoding="utf-8"))
    raw_path = REPO / record["raw_output_path"]
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    out = []
    for v in raw["verdicts"]:
        if v["verdict"] != "ISSUE":
            continue
        entry = table.get(v["revision_key"], {})
        out.append({
            "bundle": task_id,
            "revision_key": v["revision_key"],
            "source": entry.get("source"),
            "target": entry.get("target"),
            "observation": v["observation"],
        })
    return {"task_id": task_id, "coverage": record["coverage"], "findings": out}


def main():
    only = sys.argv[1:] or None
    all_findings = []
    bundles = bundle_ids()
    for task_id in bundles:
        if only and task_id not in only:
            continue
        result = collect(task_id)
        if result is None:
            continue
        fs = result["findings"]
        if fs:
            print(f"## {task_id}  ({result['coverage']['revisions']} revisions, {len(fs)} issues)")
            for f in fs:
                print(f"  - {f['revision_key']}")
                print(f"    src: {str(f['source'])[:160]!r}")
                print(f"    tgt: {str(f['target'])[:160]!r}")
                print(f"    obs: {f['observation']}")
        all_findings.extend(fs)
    print(f"\nTOTAL findings: {len(all_findings)}")
    print(Counter(f["bundle"] for f in all_findings))


if __name__ == "__main__":
    main()
