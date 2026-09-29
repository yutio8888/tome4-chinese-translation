#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-bundle the remaining public bundles under a character budget.

Bundles ctx2-pub-01..03 are already reviewed and frozen; their packets and
revision sets are left untouched. Bundles 04..28 are re-split into parts
`<i><letter>` (e.g. 09a, 09b) so that each part stays under a bounded
source+target character budget, which keeps the v2 envelope near the size
observed in production bundles (<= ~80 KB).
"""
import json
import os
import shutil
import string
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.join(BASE, "ctx2-pub-%s")
BUDGET = 20000
CAP = 18
FROZEN = {1, 2, 3}
KEEP_PACKET_PREFIX = "BUNDLE-PUBLIC-"


def chars(rev):
    return len(rev["source"]) + len(rev.get("target") or "")


def split(revs):
    parts, cur, size = [], [], 0
    for rev in revs:
        c = chars(rev)
        if cur and (size + c > BUDGET or len(cur) >= CAP):
            parts.append(cur)
            cur, size = [], 0
        cur.append(rev)
        size += c
    if cur:
        parts.append(cur)
    return parts


def main(dry):
    plan = {}
    for i in range(4, 29):
        src = os.path.join(BASE, f"{KEEP_PACKET_PREFIX}{i:02d}.json")
        packet = json.load(open(src, encoding="utf-8"))
        groups = split(packet["revisions"])
        for j, group in enumerate(groups):
            suffix = f"{i:02d}{string.ascii_lowercase[j]}"
            plan[suffix] = group
    for suffix, group in sorted(plan.items()):
        print(f"ctx2-pub-{suffix}: {len(group)} revisions, {sum(chars(r) for r in group)} chars")
    print(f"total parts: {len(plan)}")
    if dry:
        return
    for suffix, group in plan.items():
        dst = os.path.join(BASE, f"{KEEP_PACKET_PREFIX}{suffix}.json")
        json.dump({"schema_version": 1, "revisions": group}, open(dst, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    for i in range(4, 29):
        d = TASK % f"{i:02d}"
        if os.path.isdir(d):
            shutil.rmtree(d)
        p = os.path.join(BASE, f"{KEEP_PACKET_PREFIX}{i:02d}.json")
        if os.path.exists(p):
            os.remove(p)


if __name__ == "__main__":
    main("--dry" in sys.argv)
