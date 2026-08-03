#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重复运行键分类：1,717 个同键多条目（全部同 target，无覆盖风险）。

分类维度：
- 键 = (component, source, source_tag)
- 桶 A 跨文件合法重复（各数据文件独立 t() 声明，ToME 惯例）
- 桶 B 同文件内冗余（同一 section 内同键多条目，可合并清理）
- 桶 C 待确认（同文件内同键但跨 source 变体等）
输出 JSON + MD 到 .artifacts/i18n/runtime-key-classification/。"""
import json
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

signal.alarm(300)
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import DEFAULT_VERSION, load_manifest  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402

OUT = ROOT / ".artifacts" / "i18n" / "runtime-key-classification"
OUT.mkdir(parents=True, exist_ok=True)

manifest = load_manifest(version=DEFAULT_VERSION)
runtime = LuaRuntime(manifest=manifest)
loader = LocaleLoader(runtime)

by_key = defaultdict(list)  # (comp, source, tag) -> [(target, section)]
for comp in manifest.components:
    if not comp.translation:
        continue
    path = manifest.root / comp.translation
    if not path.is_file():
        continue
    doc = loader.load_path(path, logical_path=str(comp.translation))
    for rec in doc.translations:
        s = rec.get("source") or ""
        t = rec.get("target") or ""
        if s:
            by_key[(comp.id, s, rec.get("source_tag"))].append(
                (t, rec.get("section") or ""))

dups = {k: v for k, v in by_key.items() if len(v) > 1}
print("duplicate keys:", len(dups))

# 分桶
bucket_a = []  # 跨文件重复（合法）
bucket_b = []  # 同文件内冗余（可合并）
bucket_c = []  # 混合（既有跨文件又有同文件内）
for (comp, s, tag), entries in sorted(dups.items()):
    sections = [sec for _, sec in entries]
    targets = {t for t, _ in entries}
    assert len(targets) == 1, (comp, s, tag, targets)  # 全同 target 前提
    same_file = len({sec for sec in sections}) < len(sections)
    if same_file:
        bucket_c.append({"component": comp, "source": s, "source_tag": tag,
                         "count": len(entries), "sections": sorted(sections),
                         "target": next(iter(targets))})
    else:
        bucket_a.append({"component": comp, "source": s, "source_tag": tag,
                         "count": len(entries),
                         "section_count": len(set(sections)),
                         "sections": sorted(set(sections))[:6],
                         "target": next(iter(targets))})

print(f"桶 A 跨文件合法重复: {len(bucket_a)}")
print(f"桶 C 含同文件冗余: {len(bucket_c)}")

# 桶 A 按 source_tag 分布
tag_dist = Counter(it["source_tag"] for it in bucket_a)
print("桶 A tag 分布:", dict(sorted(tag_dist.items(), key=lambda x: -x[1])))
# 桶 A 按 section 目录模式分布
dir_dist = Counter()
for it in bucket_a:
    for sec in it["sections"]:
        parts = sec.split("/")
        key = "/".join(parts[1:3]) if len(parts) >= 3 else sec
        dir_dist[key] += 1
print("桶 A 目录模式分布:", dict(sorted(dir_dist.items(), key=lambda x: -x[1])[:12]))

report = {
    "total_duplicate_keys": len(dups),
    "bucket_a_cross_file": bucket_a,
    "bucket_c_same_file_mixed": bucket_c,
    "bucket_a_tag_distribution": dict(sorted(tag_dist.items(), key=lambda x: -x[1])),
    "bucket_a_dir_distribution": dict(sorted(dir_dist.items(), key=lambda x: -x[1])[:15]),
}
(OUT / "classification.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

md = ["# 重复运行键分类报告", "",
      f"总重复键：{len(dups)}（全部同 target，无运行时覆盖差异）", "",
      f"## 桶 A：跨文件合法重复（{len(bucket_a)}）", "",
      "各数据文件按 ToME 惯例独立声明 `t()`，同键同译属源码结构，保留。", "",
      "tag 分布：" + ", ".join(f"{k}={v}" for k, v in sorted(tag_dist.items(), key=lambda x: -x[1])), "",
      "目录模式分布：" + ", ".join(f"{k}={v}" for k, v in sorted(dir_dist.items(), key=lambda x: -x[1])[:15]), "",
      f"## 桶 C：含同文件内冗余（{len(bucket_c)}）", "",
      "同一 section 内同键多条目（可合并清理，需人工逐条确认）：", ""]
for it in sorted(bucket_c, key=lambda x: -x["count"]):
    md.append(f"- [{it['component']}] ({it['count']}) `{it['source'][:50]}` [{it['source_tag']}]"
              f" sections: {sorted(set(it['sections']))[:4]}")
(OUT / "classification.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("report written:", OUT)
