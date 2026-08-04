#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语表静态校对审计：结构 / 同源多译 / 错别字 / 标点 / 类别边界 / 字段完整性。
输出 JSON + 可读 MD 到 .artifacts/i18n/terminology-audit/。"""
import csv
import json
import re
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

signal.alarm(120)

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "terminology.tsv"
OUT = ROOT / ".artifacts/i18n/terminology-audit"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- 错别字表（保守：仅明确错字/非常用字） ----------
TYPO_PAIRS = [
    ("白暂", "白皙"), ("痳痹", "麻痹"), ("青眯", "青睐"), ("亲睐", "青睐"),
    ("按装", "安装"), ("既使", "即使"), ("在次", "再次"), ("另人", "令人"),
    ("吩咐", "吩咐"), ("唯妙唯肖", "惟妙惟肖"), ("变挂", "变卦"), ("幅射", "辐射"),
    ("震憾", "震撼"), ("渲泄", "宣泄"), ("渲泄", "宣泄"), ("甘败下风", "甘拜下风"),
    ("迫不急待", "迫不及待"), ("一如继往", "一如既往"), ("兴高彩烈", "兴高采烈"),
    ("谈笑风声", "谈笑风生"), ("鬼鬼崇崇", "鬼鬼祟祟"), ("走头无路", "走投无路"),
    ("再接再励", "再接再厉"), ("出奇不意", "出其不意"), ("搬门弄斧", "班门弄斧"),
    ("澜", "滥"), ("掂量", "掂量"), ("望而怯步", "望而却步"), ("有持无恐", "有恃无恐"),
    ("挖墙角", "挖墙脚"), ("一诺千斤", "一诺千金"), ("貌和神离", "貌合神离"),
    ("穿流不息", "川流不息"), ("萎糜不振", "萎靡不振"), ("百练成钢", "百炼成钢"),
    ("震奋", "振奋"), ("帐蓬", "帐篷"), ("手饰", "首饰"), ("松驰", "松弛"),
    ("痉孪", "痉挛"), ("踌躇", "踌躇"), ("臃肿", "臃肿"), ("搔扰", "骚扰"),
    ("重迭", "重叠"), ("影牒", "影碟"), ("担误", "耽误"), ("搀杂", "掺杂"),
    ("编缉", "编辑"), ("精萃", "精粹"), ("装祯", "装帧"), ("布署", "部署"),
    ("砍价", "砍价"), ("既使", "即使"), ("年令", "年龄"), ("废尽心思", "费尽心思"),
    ("罗嗦", "啰嗦"), ("了望", "瞭望"), ("姆指", "拇指"), ("砂", "沙"), ("汇", "会"),
    ("溶", "熔"), ("予", "预"), ("予", "豫"), ("渲", "宣"), ("布", "部"),
]

# 保守过滤：只保留明确整词错字；单字替换类风险高，仅保留高频确定性组合
TYPO_PAIRS = [p for p in TYPO_PAIRS if len(p[0]) >= 2]

# ---------- 读取 ----------
rows = []
with TSV.open("r", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h, delimiter="\t")
    for i, r in enumerate(rd, start=2):
        r["_line"] = i
        rows.append(r)

report = {"total_rows": len(rows), "sections": {}}

# ---------- S1.1 同源多译 ----------
by_source = defaultdict(list)
for r in rows:
    by_source[r["source"]].append(r)
conflicts = []
for src, rs in sorted(by_source.items()):
    if len(rs) < 2:
        continue
    by_cat_target = {}
    for r in rs:
        key = (r["category"], r["target"])
        by_cat_target.setdefault(key, []).append(r)
    # 同类别内不同 target
    same_cat_diff_target = []
    by_cat = defaultdict(set)
    for r in rs:
        by_cat[r["category"]].add(r["target"])
    for cat, targets in sorted(by_cat.items()):
        if len(targets) > 1:
            same_cat_diff_target.append((cat, sorted(targets)))
    if same_cat_diff_target:
        conflicts.append({
            "source": src,
            "detail": [
                {"category": c, "targets": t,
                 "rows": [{"line": r["_line"], "tag": r["source_tag"], "status": r["status"],
                           "scope": r["scope"], "target": r["target"], "notes": r["notes"]}
                          for r in rs if r["category"] == c]}
                for c, t in same_cat_diff_target
            ],
        })
report["sections"]["S1.1_same_source_multi_target"] = {
    "count": len(conflicts), "items": conflicts}

# ---------- S1.2 错别字 ----------
typo_hits = []
for r in rows:
    t = r["target"]
    for bad, good in TYPO_PAIRS:
        if bad in t:
            typo_hits.append({"line": r["_line"], "source": r["source"], "target": t,
                              "bad": bad, "good": good, "category": r["category"]})
report["sections"]["S1.2_typos"] = {"count": len(typo_hits), "items": typo_hits}

# ---------- S1.3 标点格式 ----------
punct_hits = []
for r in rows:
    t = r["target"]
    problems = []
    # 半角逗号/句号/冒号/问号夹在中文间（排除 %s、数字、英文、控制标记）
    stripped = re.sub(r"#[A-Za-z0-9_{}:+.\-]+#", "", t)
    stripped = re.sub(r"%[-+ #0-9.]*[cdeEfgGiouXxqs]", "", stripped)
    stripped = re.sub(r"@[A-Za-z0-9_:+.\-]+@", "", stripped)
    if re.search(r"[\u4e00-\u9fff][,;!?][\u4e00-\u9fff]", stripped):
        problems.append("中文字符间夹半角标点")
    if re.search(r"[\u4e00-\u9fff],", stripped):
        problems.append("中文后接半角逗号")
    if re.search(r",[\u4e00-\u9fff]", stripped):
        problems.append("半角逗号后接中文")
    if re.search(r"[\u4e00-\u9fff]\.", stripped):
        problems.append("中文后接半角句点")
    if "  " in t:
        problems.append("连续空格")
    if t != t.strip() or re.search(r"\s+$", t):
        problems.append("首尾空白")
    # 控制标记配对
    tags = re.findall(r"#[A-Za-z0-9_{}:+.\-]+#", t)
    if tags:
        opens = [x for x in tags if not x.startswith("#/")]
        closes = [x for x in tags if x.startswith("#/")]
        if opens and closes and len(opens) != len(closes):
            problems.append(f"控制标记疑似不配对 ({len(opens)} open / {len(closes)} close)")
    if problems:
        punct_hits.append({"line": r["_line"], "source": r["source"], "target": t,
                           "category": r["category"], "problems": problems})
report["sections"]["S1.3_punctuation"] = {"count": len(punct_hits), "items": punct_hits}

# ---------- S1.4 类别边界 ----------
boundary = []
for r in rows:
    cat = r["category"]
    src = r["source"]
    # 专名类别但 source 是小写普通词
    if cat in ("T.PN.PERSON", "T.PN.PLACE", "T.PN.FACTION", "T.PN.RACE", "T.PN.WORLD"):
        if src and src[0].islower():
            boundary.append({"line": r["_line"], "source": src, "target": r["target"],
                             "category": cat, "note": "专名类别但 source 以小写开头"})
    # T.GAME.ENTITY 中 source 含大写专名特征（"The " 或全部大写单词）且 status=preferred
    if cat == "T.GAME.ENTITY" and r["status"] == "preferred":
        if re.search(r"\b(The|the)\s+[A-Z]", src) or re.search(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+", src):
            boundary.append({"line": r["_line"], "source": src, "target": r["target"],
                             "category": cat, "note": "ENTITY 类别含专名特征，可能应为 T.PN.*"})
report["sections"]["S1.4_category_boundary"] = {"count": len(boundary), "items": boundary}

# ---------- S1.5 字段完整性 ----------
missing_notes = [{"line": r["_line"], "source": r["source"], "target": r["target"],
                  "category": r["category"], "status": r["status"]}
                 for r in rows if not (r.get("notes") or "").strip() and r["status"] == "preferred"]
bad_scope = [{"line": r["_line"], "source": r["source"], "scope": r["scope"]}
             for r in rows if r["scope"] not in ("core", "addon", "dlc", "global", "multi")]
bad_status = [{"line": r["_line"], "source": r["source"], "status": r["status"]}
              for r in rows if r["status"] not in ("existing", "preferred", "review")]
report["sections"]["S1.5_fields"] = {
    "missing_notes_preferred": missing_notes,
    "bad_scope": bad_scope, "bad_status": bad_status,
    "counts": {"missing_notes_preferred": len(missing_notes),
               "bad_scope": len(bad_scope), "bad_status": len(bad_status)}}

# ---------- 汇总统计 ----------
cat_stat = Counter(r["category"] for r in rows)
status_stat = Counter(r["status"] for r in rows)
scope_stat = Counter(r["scope"] for r in rows)
report["stats"] = {
    "categories": dict(sorted(cat_stat.items(), key=lambda x: -x[1])),
    "status": dict(status_stat), "scope": dict(scope_stat),
}

(OUT / "audit_static.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- MD 报告 ----------
md = ["# 术语表静态校对审计报告", "",
      f"总行数：{report['total_rows']}（含表头 {report['total_rows']+1} 行）", ""]
md += ["## 统计", ""]
md.append("| category | 数量 |")
md.append("|---|---|")
for c, n in report["stats"]["categories"].items():
    md.append(f"| {c} | {n} |")
md.append("")
md.append(f"- status：{report['stats']['status']}")
md.append(f"- scope：{report['stats']['scope']}")
for sec, title in [
    ("S1.1_same_source_multi_target", "同源同类别多译冲突"),
    ("S1.2_typos", "错别字"),
    ("S1.3_punctuation", "标点/格式"),
    ("S1.4_category_boundary", "类别边界疑点"),
]:
    data = report["sections"][sec]
    md += ["", f"## {title}（{data['count']}）", ""]
    for it in data["items"]:
        if sec == "S1.1_same_source_multi_target":
            lines = sorted({r["line"] for d in it["detail"] for r in d["rows"]})
            md.append(f"- L{lines} `{it['source']}`")
            for d in it["detail"]:
                md.append(f"  - [{d['category']}] " + " / ".join(d["targets"]))
        else:
            md.append(f"- L{it['line']} `{it['source']}` → `{it['target']}`")
            if sec == "S1.3_punctuation":
                md[-1] += f"  ({'; '.join(it['problems'])})"
sec = "S1.5_fields"
md += ["", "## 字段完整性", ""]
md.append(f"- preferred 无 notes：{report['sections'][sec]['counts']['missing_notes_preferred']} 条")
md.append(f"- 非法 scope：{report['sections'][sec]['counts']['bad_scope']} 条")
md.append(f"- 非法 status：{report['sections'][sec]['counts']['bad_status']} 条")
for it in report["sections"][sec]["missing_notes_preferred"]:
    md.append(f"  - L{it['line']} `{it['source']}` → `{it['target']}` [{it['category']}]")
(OUT / "audit_static.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("static audit done:", report["total_rows"], "rows")
for sec in report["sections"]:
    c = report["sections"][sec].get("count", report["sections"][sec].get("counts", {}))
    print(f"  {sec}: {c}")
