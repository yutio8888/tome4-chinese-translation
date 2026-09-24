#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build every re-split public bundle envelope in a single process.

Parsing the four Lua files once and reusing the scan (instead of one full parse
per bundle) keeps the CPU cost of preflight/build bounded.
"""
import functools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v2_bundle as B  # noqa: E402

B.scan_file = functools.lru_cache(maxsize=None)(B.scan_file)

FIXED = "commit:624a67329fe2ad440c5b344785a9c73fcf22ae63"
REPO_FILES = None


def main(suffixes):
    out = {}
    for suffix in suffixes:
        packet = os.path.join(HERE, f"BUNDLE-PUBLIC-{suffix}.json")
        task_dir = os.path.normpath(os.path.join(HERE, "..", f"ctx2-pub-{suffix}"))
        identity, n, terms, files, anchors = B.build(
            packet, task_dir, "full-01", FIXED, os.path.join(B.REPO, "terminology"), "CONTEXTUAL"
        )
        out[f"ctx2-pub-{suffix}"] = {
            "run": "PUBLIC",
            "candidate_identity": identity,
            "input_path": f".ai/task/ctx2-pub-{suffix}/CONTEXTUAL-ENVELOPE-full-01.json",
            "count": n,
            "prompt_bytes": 0,
        }
        print(f"ctx2-pub-{suffix}: n={n} terms={terms} files={files} anchors={anchors} id={identity[:16]}")
    json.dump(out, open(os.path.join(HERE, "V2-BUNDLES-PUBLIC-NEW.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    suffix_list = sys.argv[1:]
    if not suffix_list:
        suffix_list = sorted(
            f[:-5].split("-")[-1]
            for f in os.listdir(HERE)
            if f.startswith("BUNDLE-PUBLIC-") and not f.endswith("z.json") and f[-5] != "a"
        )
        suffix_list = [s for s in suffix_list]
    main(suffix_list)
