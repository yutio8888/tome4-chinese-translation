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

from audit_static_rules import normalize_typo_pairs

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT / "tools"))
from i18nlib.errors import I18nToolError  # noqa: E402
from i18nlib.terminology import load_terminology_rows  # noqa: E402
TSV = ROOT / "terminology"
OUT = ROOT / ".artifacts/i18n/terminology-audit"

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

# 保守过滤：只保留明确整词错字；排除自映射并按完整规则稳定去重
TYPO_PAIRS = normalize_typo_pairs(TYPO_PAIRS)

_REQUIRED_FIELDS = (
    "source",
    "target",
    "category",
    "source_tag",
    "status",
    "scope",
    "notes",
)
_VALUE_REQUIRED_FIELDS = ("source", "target", "category", "status", "scope")


def _read_rows(tsv_path):
    """Read terminology rows via the shared store loader (file or directory)."""
    return load_terminology_rows(Path(tsv_path))


def _build_report(rows):
    report = {"total_rows": len(rows), "sections": {}}

    # ---------- S1.1 同源多译 ----------
    by_source = defaultdict(list)
    for row in rows:
        by_source[row["source"]].append(row)
    conflicts = []
    for source, source_rows in sorted(by_source.items()):
        if len(source_rows) < 2:
            continue
        same_cat_diff_target = []
        by_category = defaultdict(set)
        for row in source_rows:
            by_category[row["category"]].add(row["target"])
        for category, targets in sorted(by_category.items()):
            if len(targets) > 1:
                same_cat_diff_target.append((category, sorted(targets)))
        if same_cat_diff_target:
            conflicts.append({
                "source": source,
                "detail": [
                    {
                        "category": category,
                        "targets": targets,
                        "rows": [
                            {
                                "line": row["_line"],
                                "tag": row["source_tag"],
                                "status": row["status"],
                                "scope": row["scope"],
                                "target": row["target"],
                                "notes": row["notes"],
                            }
                            for row in source_rows
                            if row["category"] == category
                        ],
                    }
                    for category, targets in same_cat_diff_target
                ],
            })
    report["sections"]["S1.1_same_source_multi_target"] = {
        "count": len(conflicts),
        "items": conflicts,
    }

    # ---------- S1.2 错别字 ----------
    typo_hits = []
    for row in rows:
        target = row["target"]
        for bad, good in TYPO_PAIRS:
            if bad in target:
                typo_hits.append({
                    "line": row["_line"],
                    "source": row["source"],
                    "target": target,
                    "bad": bad,
                    "good": good,
                    "category": row["category"],
                })
    report["sections"]["S1.2_typos"] = {
        "count": len(typo_hits),
        "items": typo_hits,
    }

    # ---------- S1.3 标点格式 ----------
    punctuation_hits = []
    for row in rows:
        target = row["target"]
        problems = []
        # 半角逗号/句号/冒号/问号夹在中文间（排除格式与控制标记）
        stripped = re.sub(r"#[A-Za-z0-9_{}:+.\-]+#", "", target)
        stripped = re.sub(
            r"%[-+ #0-9.]*[cdeEfgGiouXxqs]", "", stripped
        )
        stripped = re.sub(r"@[A-Za-z0-9_:+.\-]+@", "", stripped)
        if re.search(r"[\u4e00-\u9fff][,;!?][\u4e00-\u9fff]", stripped):
            problems.append("中文字符间夹半角标点")
        if re.search(r"[\u4e00-\u9fff],", stripped):
            problems.append("中文后接半角逗号")
        if re.search(r",[\u4e00-\u9fff]", stripped):
            problems.append("半角逗号后接中文")
        if re.search(r"[\u4e00-\u9fff]\.", stripped):
            problems.append("中文后接半角句点")
        if "  " in target:
            problems.append("连续空格")
        if target != target.strip() or re.search(r"\s+$", target):
            problems.append("首尾空白")
        tags = re.findall(r"#[A-Za-z0-9_{}:+.\-]+#", target)
        if tags:
            opens = [tag for tag in tags if not tag.startswith("#/")]
            closes = [tag for tag in tags if tag.startswith("#/")]
            if opens and closes and len(opens) != len(closes):
                problems.append(
                    "控制标记疑似不配对 "
                    f"({len(opens)} open / {len(closes)} close)"
                )
        if problems:
            punctuation_hits.append({
                "line": row["_line"],
                "source": row["source"],
                "target": target,
                "category": row["category"],
                "problems": problems,
            })
    report["sections"]["S1.3_punctuation"] = {
        "count": len(punctuation_hits),
        "items": punctuation_hits,
    }

    # ---------- S1.4 类别边界 ----------
    boundary = []
    proper_name_categories = (
        "T.PN.PERSON",
        "T.PN.PLACE",
        "T.PN.FACTION",
        "T.PN.RACE",
        "T.PN.WORLD",
    )
    for row in rows:
        category = row["category"]
        source = row["source"]
        if category in proper_name_categories:
            if source and source[0].islower():
                boundary.append({
                    "line": row["_line"],
                    "source": source,
                    "target": row["target"],
                    "category": category,
                    "note": "专名类别但 source 以小写开头",
                })
        if category == "T.GAME.ENTITY" and row["status"] == "preferred":
            if re.search(r"\b(The|the)\s+[A-Z]", source) or re.search(
                r"\b[A-Z][a-z]+\s+[A-Z][a-z]+", source
            ):
                boundary.append({
                    "line": row["_line"],
                    "source": source,
                    "target": row["target"],
                    "category": category,
                    "note": "ENTITY 类别含专名特征，可能应为 T.PN.*",
                })
    report["sections"]["S1.4_category_boundary"] = {
        "count": len(boundary),
        "items": boundary,
    }

    # ---------- S1.5 字段完整性 ----------
    missing_notes = [
        {
            "line": row["_line"],
            "source": row["source"],
            "target": row["target"],
            "category": row["category"],
            "status": row["status"],
        }
        for row in rows
        if not (row.get("notes") or "").strip()
        and row["status"] == "preferred"
    ]
    bad_scope = [
        {
            "line": row["_line"],
            "source": row["source"],
            "scope": row["scope"],
        }
        for row in rows
        if row["scope"] not in ("core", "addon", "dlc", "global", "multi")
    ]
    bad_status = [
        {
            "line": row["_line"],
            "source": row["source"],
            "status": row["status"],
        }
        for row in rows
        if row["status"] not in ("existing", "preferred", "review")
    ]
    field_counts = {
        "missing_notes_preferred": len(missing_notes),
        "bad_scope": len(bad_scope),
        "bad_status": len(bad_status),
    }
    report["sections"]["S1.5_fields"] = {
        "missing_notes_preferred": missing_notes,
        "bad_scope": bad_scope,
        "bad_status": bad_status,
        "counts": field_counts,
    }

    blocking_count = (
        report["sections"]["S1.2_typos"]["count"]
        + report["sections"]["S1.3_punctuation"]["count"]
        + sum(field_counts.values())
    )
    advisory_count = (
        report["sections"]["S1.1_same_source_multi_target"]["count"]
        + report["sections"]["S1.4_category_boundary"]["count"]
    )
    report["ok"] = blocking_count == 0
    report["blocking_count"] = blocking_count
    report["advisory_count"] = advisory_count

    cat_stat = Counter(row["category"] for row in rows)
    status_stat = Counter(row["status"] for row in rows)
    scope_stat = Counter(row["scope"] for row in rows)
    report["stats"] = {
        "categories": dict(sorted(cat_stat.items(), key=lambda item: -item[1])),
        "status": dict(status_stat),
        "scope": dict(scope_stat),
    }
    return report


def _render_markdown(report):
    md = [
        "# 术语表静态校对审计报告",
        "",
        f"总行数：{report['total_rows']}（含表头 {report['total_rows'] + 1} 行）",
        "",
        "## 统计",
        "",
        "| category | 数量 |",
        "|---|---|",
    ]
    for category, count in report["stats"]["categories"].items():
        md.append(f"| {category} | {count} |")
    md.append("")
    md.append(f"- status：{report['stats']['status']}")
    md.append(f"- scope：{report['stats']['scope']}")
    for section, title in [
        ("S1.1_same_source_multi_target", "同源同类别多译冲突"),
        ("S1.2_typos", "错别字"),
        ("S1.3_punctuation", "标点/格式"),
        ("S1.4_category_boundary", "类别边界疑点"),
    ]:
        data = report["sections"][section]
        md += ["", f"## {title}（{data['count']}）", ""]
        for item in data["items"]:
            if section == "S1.1_same_source_multi_target":
                lines = sorted({
                    row["line"]
                    for detail in item["detail"]
                    for row in detail["rows"]
                })
                md.append(f"- L{lines} `{item['source']}`")
                for detail in item["detail"]:
                    md.append(
                        f"  - [{detail['category']}] "
                        + " / ".join(detail["targets"])
                    )
            else:
                md.append(
                    f"- L{item['line']} `{item['source']}` → `{item['target']}`"
                )
                if section == "S1.3_punctuation":
                    md[-1] += f"  ({'; '.join(item['problems'])})"
    section = "S1.5_fields"
    md += ["", "## 字段完整性", ""]
    counts = report["sections"][section]["counts"]
    md.append(
        f"- preferred 无 notes：{counts['missing_notes_preferred']} 条"
    )
    md.append(f"- 非法 scope：{counts['bad_scope']} 条")
    md.append(f"- 非法 status：{counts['bad_status']} 条")
    for item in report["sections"][section]["missing_notes_preferred"]:
        md.append(
            f"  - L{item['line']} `{item['source']}` → `{item['target']}` "
            f"[{item['category']}]"
        )
    return "\n".join(md) + "\n"


def run_static_audit(tsv_path, output_dir):
    """Read one terminology TSV, write both reports, and return the report."""
    tsv_path = Path(tsv_path)
    output_dir = Path(output_dir)
    rows = _read_rows(tsv_path)
    report = _build_report(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit_static.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (output_dir / "audit_static.md").write_text(
        _render_markdown(report), encoding="utf-8"
    )
    return report


def _print_summary(report):
    print("static audit done:", report["total_rows"], "rows")
    for section in report["sections"]:
        count = report["sections"][section].get(
            "count", report["sections"][section].get("counts", {})
        )
        print(f"  {section}: {count}")


def main(*, tsv_path=TSV, output_dir=OUT):
    signal.alarm(120)
    try:
        report = run_static_audit(tsv_path, output_dir)
        _print_summary(report)
        return 0 if report["ok"] else 1
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"static audit failed: {error}", file=sys.stderr)
        return 2
    except I18nToolError as error:
        print(f"static audit failed: {error}", file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
