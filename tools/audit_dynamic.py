#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语表动态校对审计：术语 vs 30,170 条规范译文。
- S2.1 术语使用率：preferred 术语的 (source, source_tag) 在对应 scope 组件译文中是否存在、target 是否一致
- S2.2 高频未录候选：译文中高复用英文 source 未收录术语表
- S2.3 译文多译：同一英文 source 在译文中出现多译但术语表未记录语境区分
输出 JSON + MD 到 .artifacts/i18n/terminology-audit/。"""
import csv
import json
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

signal.alarm(300)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from i18nlib.config import load_manifest, DEFAULT_VERSION  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402

OUT = ROOT / ".artifacts/i18n/terminology-audit"
OUT.mkdir(parents=True, exist_ok=True)

manifest = load_manifest(version=DEFAULT_VERSION)
runtime = LuaRuntime(manifest=manifest)
loader = LocaleLoader(runtime)

# 组件 scope 映射：术语 scope -> 组件集（global = 全部组件）
SCOPE_COMPONENTS = {
    "core": ["tome", "engine", "boot", "items-vault", "possessors", "addon-dev", "example", "example-realtime"],
    "dlc": ["ashes-urhrok", "cults", "orcs"],
    "global": None,  # 全部
    "addon": None,
    "multi": None,
}

docs = {}
for comp in manifest.components:
    if not comp.translation:
        continue
    path = manifest.root / comp.translation
    if not path.is_file():
        print(f"skip missing {comp.id}: {path}")
        continue
    try:
        docs[comp.id] = loader.load_path(path, logical_path=str(comp.translation))
    except Exception as exc:  # noqa: BLE001
        print(f"load failed {comp.id}: {exc}")

# 聚合译文条目
entries = []  # (component, source, source_tag, target)
by_source = defaultdict(list)  # source -> [(comp, tag, target)]
for comp, doc in docs.items():
    for rec in doc.translations:
        src = rec.get("source") or ""
        tgt = rec.get("target") or ""
        tag = rec.get("source_tag")
        if not src or not tgt:
            continue
        entries.append((comp, src, tag, tgt))
        by_source[src].append((comp, tag, tgt))

# 读术语表
rows = []
with (ROOT / "terminology.tsv").open("r", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h, delimiter="\t")
    for i, r in enumerate(rd, start=2):
        r["_line"] = i
        rows.append(r)
term_sources = {r["source"] for r in rows}

report = {"entries": len(entries), "components": sorted(docs.keys())}

# ---------- S2.1 preferred 术语使用率 ----------
unused = []
mismatch = []
for r in rows:
    if r["status"] != "preferred":
        continue
    comps = SCOPE_COMPONENTS.get(r["scope"])
    if comps is None:
        comps = list(docs.keys())
    relevant = [e for e in entries if e[0] in comps]
    # 精确匹配 (source, source_tag)
    tag = r["source_tag"] if r["source_tag"] != "nil" else None
    hits = [e for e in relevant if e[1] == r["source"] and e[2] == tag]
    if not hits:
        # 退而求其次：source 匹配（忽略 tag）
        hits = [e for e in relevant if e[1] == r["source"]]
    if not hits:
        # source 都不存在：术语可能过时
        unused.append({"line": r["_line"], "source": r["source"], "target": r["target"],
                       "category": r["category"], "tag": r["source_tag"], "scope": r["scope"]})
        continue
    # target 一致性：术语 target 是否出现在译文 target 中（允许术语是条目 target 的子串或相等）
    tgt_set = {e[3] for e in hits}
    term_t = r["target"]
    if not any(term_t == t or (len(term_t) >= 4 and term_t in t) for t in tgt_set):
        mismatch.append({"line": r["_line"], "source": r["source"], "target": term_t,
                         "category": r["category"], "tag": r["source_tag"], "scope": r["scope"],
                         "found_targets": sorted(tgt_set)[:8]})
report["s2_1"] = {
    "unused_count": len(unused), "unused": unused,
    "mismatch_count": len(mismatch), "mismatch": mismatch,
}

# ---------- S2.2 高频未录候选 ----------
src_counts = Counter(e[1] for e in entries)
candidates = []
for src, n in src_counts.most_common():
    if n < 15:
        break
    if src in term_sources:
        continue
    if len(src) > 60 or len(src) < 3:
        continue
    tags = sorted({e[2] for e in by_source[src]})
    tgts = sorted({e[2] for e in by_source[src]})
    candidates.append({"source": src, "count": n, "tags": tags[:4], "targets": tgts[:3]})
report["s2_2"] = {"count": len(candidates), "items": candidates}

# ---------- S2.3 译文多译（术语表未记录） ----------
multi = []
for src, es in sorted(by_source.items()):
    if src in term_sources:
        continue  # 术语表已有记录（含多行语境区分）
    variants = {}
    for comp, tag, tgt in es:
        variants.setdefault(tgt, []).append((comp, tag))
    if len(variants) >= 2:
        # 过滤：长句、数字/占位符为主
        if len(src) > 50:
            continue
        multi.append({
            "source": src, "count": len(es),
            "variants": [{"target": t, "places": sorted({f"{c}" for c, _ in v})[:6],
                          "tags": sorted({str(tag) for _, tag in v})[:4]}
                         for t, v in sorted(variants.items())],
        })
# 只保留最显著的前 200 条
multi.sort(key=lambda x: -x["count"])
report["s2_3"] = {"count": len(multi), "items": multi[:200]}

(OUT / "audit_dynamic.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

md = ["# 术语表动态校对审计报告", "",
      f"译文条目总数：{report['entries']}；组件：{', '.join(report['components'])}", "",
      "## S2.1 preferred 术语使用率", "",
      f"- 术语 source 在对应组件译文中完全不存在（可能过时）：{len(unused)} 条", ""]
for it in unused:
    md.append(f"  - L{it['line']} `{it['source']}` → `{it['target']}` [{it['category']} @ {it['scope']}]")
md += ["", f"- source 存在但译文 target 与术语 target 不一致：{len(mismatch)} 条", ""]
for it in mismatch:
    md.append(f"  - L{it['line']} `{it['source']}` → 术语 `{it['target']}`；译文：{' / '.join(it['found_targets'][:4])}")
md += ["", "## S2.2 高频未录候选（译文出现 ≥15 次）", f"共 {len(candidates)} 条", ""]
for it in candidates:
    md.append(f"- ({it['count']}) `{it['source']}` → {' / '.join(it['targets'][:3])}")
md += ["", "## S2.3 译文多译（术语表未记录语境区分）", f"共 {len(multi)} 条（显示前 200）", ""]
for it in multi[:200]:
    vs = "；".join(f"`{v['target']}`[{','.join(v['tags'])}]" for v in it["variants"])
    md.append(f"- ({it['count']}) `{it['source']}` → {vs}")
(OUT / "audit_dynamic.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("dynamic audit done:", report["entries"], "entries")
print("  unused:", len(unused), "| mismatch:", len(mismatch), "| candidates:", len(candidates), "| multi:", len(multi))
