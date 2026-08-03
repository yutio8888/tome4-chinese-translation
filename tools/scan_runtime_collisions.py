#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨组件同 (source, source_tag) 多译扫描。

ToME4 翻译运行时按 (component, source, source_tag) 键匹配；同键多条目在
引擎加载多个 locale 文件时会发生覆盖（后加载者胜出）。组件内同键不同
target 已由 lint 的 runtime-collision（error）覆盖；本脚本补充扫描
**跨组件**同键多译，输出 JSON + Markdown 报告，供维护
docs/runtime-key-collisions.md 档案。

用法：python3 -B tools/scan_runtime_collisions.py [--out-dir .artifacts/i18n]
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
from collections import defaultdict
from pathlib import Path

signal.alarm(300)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import DEFAULT_VERSION, load_manifest  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default=str(ROOT / ".artifacts" / "i18n"),
                        help="report output directory")
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(version=DEFAULT_VERSION)
    runtime = LuaRuntime(manifest=manifest)
    loader = LocaleLoader(runtime)

    by_key: dict[tuple[str, str | None], list[dict[str, str]]] = defaultdict(list)
    for comp in manifest.components:
        if not comp.translation:
            continue
        path = manifest.root / comp.translation
        if not path.is_file():
            continue
        doc = loader.load_path(path, logical_path=str(comp.translation))
        for rec in doc.translations:
            source = rec.get("source") or ""
            target = rec.get("target") or ""
            tag = rec.get("source_tag")
            by_key[(source, tag)].append(
                {
                    "component": comp.id,
                    "target": target,
                    "section": rec.get("section") or "",
                    "line": rec.get("line"),
                }
            )

    collisions = []
    for (source, tag), entries in sorted(by_key.items()):
        components = {e["component"] for e in entries}
        targets = {e["target"] for e in entries}
        if len(components) > 1 and len(targets) > 1:
            variants = {}
            for e in entries:
                variants.setdefault(e["component"], set()).add(e["target"])
            collisions.append(
                {
                    "source": source,
                    "source_tag": tag,
                    "entry_count": len(entries),
                    "components": sorted(components),
                    "target_count": len(targets),
                    "targets": sorted(targets),
                    "variants": {
                        comp: sorted(v) for comp, v in sorted(variants.items())
                    },
                }
            )

    report = {
        "scanned_translations": sum(
            len(loader.load_path(manifest.root / c.translation,
                                 logical_path=str(c.translation)).translations)
            for c in manifest.components if c.translation
            and (manifest.root / c.translation).is_file()
        ),
        "collision_count": len(collisions),
        "collisions": collisions,
    }
    json_path = out_dir / "runtime-collisions.json"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# 跨组件同 TAG 多译扫描报告", "",
          f"扫描时间：{__import__('datetime').datetime.now().isoformat(timespec='seconds')}",
          f"译文条目：{report['scanned_translations']}；冲突：{report['collision_count']} 条", ""]
    for it in collisions:
        md.append(f"## [{it['source_tag']}] {it['source']!r}（{it['entry_count']} 条）")
        for comp, ts in it["variants"].items():
            for t in ts:
                md.append(f"- {comp}：{t}")
        md.append("")
    md_path = out_dir / "runtime-collisions.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"runtime collisions: {report['collision_count']}")
    print(f"  json: {json_path}")
    print(f"  md:   {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
