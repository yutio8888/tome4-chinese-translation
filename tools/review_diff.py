#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""有界 diff 复审 bundle 生成：仅包含 origin/master..HEAD（或指定基线）改动的译文条目。

复用 tools/i18nlib/review.py 的 bundle schema（kind=translations、item_id、
terminology context、constraints），输出到 .artifacts/i18n/review-diff-*/。

用法：
  python3 -B tools/review_diff.py [--baseline origin/master] [--batch-size 50]
"""
from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

signal.alarm(600)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import DEFAULT_VERSION, load_manifest  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.review import (  # noqa: E402
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    TOOL_VERSION,
    _bundle_id,
    _entry_id,
    _relevant_terms,
    _review_index_id,
    _terminology_rows,
)
from i18nlib.runtime import LuaRuntime  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="origin/master",
                        help="git baseline revision (default: origin/master)")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--out-dir", default=None,
                        help="explicit output directory")
    args = parser.parse_args()

    manifest = load_manifest(version=DEFAULT_VERSION)
    runtime = LuaRuntime(manifest=manifest)
    loader = LocaleLoader(runtime)
    terminology_rows, terminology_sha256 = _terminology_rows(
        manifest.root / manifest.terminology)
    manifest_sha256 = __import__("hashlib").sha256(manifest.raw_bytes).hexdigest()

    run_dir = Path(args.out_dir) if args.out_dir else (
        ROOT / ".artifacts" / "i18n" / (
            "review-diff-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
    )
    run_dir.mkdir(parents=True, exist_ok=True)

    bundles = []
    changed_total = 0
    for comp in manifest.components:
        if not comp.translation:
            continue
        rel = comp.translation
        path = manifest.root / rel
        if not path.is_file():
            continue
        base = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{args.baseline}:{rel}"],
            capture_output=True,
        ).stdout
        if not base:
            continue
        doc_now = loader.load_path(path, logical_path=rel)
        with tempfile.TemporaryDirectory() as td:
            base_path = Path(td) / "base.lua"
            base_path.write_bytes(base)
            doc_base = loader.load_path(base_path, logical_path=rel)
        now_map = {
            (r.get("source"), r.get("source_tag")): r
            for r in doc_now.translations
        }
        base_map = {
            (r.get("source"), r.get("source_tag")): r.get("target")
            for r in doc_base.translations
        }
        changed = [
            (ordinal, entry)
            for ordinal, entry in enumerate(doc_now.translations)
            if base_map.get((entry.get("source"), entry.get("source_tag")))
            != entry.get("target")
        ]
        if not changed:
            continue
        changed_total += len(changed)
        items = []
        for ordinal, entry in changed:
            item = {
                "item_id": _entry_id(comp.id, ordinal, entry),
                "component": comp.id,
                "ordinal": ordinal,
                "section": entry.get("section"),
                "source": entry.get("source"),
                "target": entry.get("target"),
                "source_tag": entry.get("source_tag"),
                "args_order": entry.get("args_order"),
                "special": entry.get("special"),
                "line": entry.get("line"),
            }
            items.append(item)
        for offset in range(0, len(items), args.batch_size):
            batch = items[offset : offset + args.batch_size]
            payload = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": manifest.version,
                "manifest_sha256": manifest_sha256,
                "kind": "translations",
                "component": comp.id,
                "selection": {"offset": offset, "count": len(batch),
                              "total": len(items)},
                "items": batch,
                "terminology_sha256": terminology_sha256,
                "terminology": _relevant_terms(terminology_rows, batch, comp.id),
                "constraints": [
                    "Review only the supplied canonical translation entries.",
                    "Preserve source, source_tag, printf arguments, and control markers in any suggested fix.",
                    "Return findings only; do not rewrite files or invent missing game context.",
                ],
            }
            bundle_id = _bundle_id(payload)
            payload["bundle_id"] = bundle_id
            out = run_dir / "translations" / comp.id / f"{bundle_id}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                           encoding="utf-8")
            bundles.append({
                "bundle_id": bundle_id, "kind": "translations",
                "component": comp.id, "offset": offset, "count": len(batch),
                "total": len(items), "path": str(out),
            })

    index_payload = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "review_contract": REVIEW_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest_sha256": manifest_sha256,
        "scope": {"translations": True, "code": False},
        "redacted_absolute_path_count": 0,
        "baseline": args.baseline,
        "bundles": bundles,
    }
    review_id = _review_index_id(index_payload)
    index_payload["review_id"] = review_id
    (run_dir / "review-index.json").write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"baseline: {args.baseline}")
    print(f"changed entries: {changed_total}, bundles: {len(bundles)}")
    print(f"review_id: {review_id}")
    print(f"run_dir: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
