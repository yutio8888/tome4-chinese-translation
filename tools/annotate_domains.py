#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""领域标注脚本：按 category 与 ENTITY 启发式推导术语 domain。

只输出标注报告，不写回 TSV。
"""
from __future__ import annotations

import csv
import json
import signal
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "terminology.tsv"
OUT = ROOT / ".artifacts/i18n/terminology-audit"

# ---------- 领域体系 ----------
DOMAINS = {
    "combat":    "战斗机制：伤害类型、状态效果、战斗属性、战斗日志",
    "talents":   "技能与技能树",
    "classes":   "职业与成长",
    "resources": "角色资源",
    "items":     "装备、物品与材料",
    "creatures": "生物与种族",
    "places":    "地点、地形与世界",
    "society":   "势力、组织与人物",
    "narrative": "叙事、传说与成就",
    "ui":        "界面与交互",
    "tech":      "技术格式与内部字符串",
}

CATEGORY_DOMAIN = {
    "T.GAME.DAMAGE": "combat",
    "T.GAME.EFFECT": "combat",
    "T.GAME.STAT": "combat",
    "T.RUNTIME.LOG": "combat",
    "T.GAME.TALENT": "talents",
    "T.GAME.TALENT_CATEGORY": "talents",
    "T.GAME.CLASS": "classes",
    "T.GAME.RESOURCE": "resources",
    "T.PN.RACE": "creatures",
    "T.PN.PLACE": "places",
    "T.PN.WORLD": "places",
    "T.PN.PERSON": "society",
    "T.PN.FACTION": "society",
    "T.NARRATIVE.LORE": "narrative",
    "T.NARRATIVE.ACHIEVEMENT": "narrative",
    "T.DIALOGUE.CHAT": "narrative",
    "T.UI.LABEL": "ui",
    "T.TECH.FORMAT": "tech",
    "T.TECH.INTERNAL": "tech",
    "T.GAME.MISC": "tech",
}

# ---------- ENTITY 细分 ----------
SHOP_NAMES = {"Armoury", "Herbalist", "Library", "Runemaster", "Swordsmith", "Tanner", "Tailor"}
PLACE_ENTITY = {
    "cave", "rockwall", "exit to the worldmap", "primal trunk", "cracks", "Spacetime Tear",
    "next level",
    "previous level",
    "way to the next level",
    "way to the previous level",
}
# 物品/材料/装备类 source（entity type / subtype / name）
ITEM_SOURCES = {
    "armours", "mainhand", "offhand", "weapons", "armor", "ammo", "book", "charm",
    "potion", "scroll", "weapon", "steamgun", "staff", "tome", "light", "tinker",
    "flesh", "steamsaw", "schematic", "d.steel", "stralite", "mastercraft",
    "throwing knives", "Spellblaze Crystal", "Choker of Dread",
    "Infusion of Wild Growth", "wild infusion", "acid wave rune", "biting gale rune",
    "manasurge rune", "Viral Injector", "vial of wight ectoplasm",
    "Deflection Field", "Shocking Edge", "Ureslak's Focus", "medical injector implant",
    "medical injector", "Rod of Recall", "Recall Portal", "exploratory farportal",
    "Gloryhammer", "Ablative Armour", "Payload", "psychoportation beacon",
    "Frost Salve", "Blood-Runed Athame", "Athame", "athame",
    "Brilliant Auto-loading Orc Expeller",
    "voratun", "iron", "steel", "open door", "trap",
}
# 生物类 source
CREATURE_SOURCES = {
    "animal", "construct", "demon", "dragon", "elemental", "giant", "horror",
    "humanoid", "insect", "undead", "vermin", "void", "human", "elf", "orc",
    "halfling", "dwarf", "golem", "ghost", "troll", "natural", "reptile",
    "yeti", "krog", "ritch", "mech", "shertul", "maggot", "organic", "mechanical",
    "#rng# the Invoker", "eldritch", "dread", "dreadmaster", "radiant horror",
    "hummerhorn", "luminous horror", "vampire lord", "carrion worm mass",
    "Lone Wolf", "shivgoroth", "The Withering Thing", "The Dreaming One",
    "bloated ooze", "DESTRUCTICUS",
    "corrupted", "steamtech", "multi-hued",
}

_REQUIRED_FIELDS = ("source", "target", "category", "domain", "source_tag")
_VALUE_REQUIRED_FIELDS = ("source", "target", "category", "domain")


def _read_rows(tsv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with tsv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t", strict=True)
        fieldnames = reader.fieldnames or []
        missing = [field for field in _REQUIRED_FIELDS if field not in fieldnames]
        if missing:
            raise ValueError(
                "terminology TSV is missing required columns: "
                + ", ".join(missing)
            )
        for line, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(
                    f"terminology TSV line {line} has unexpected extra columns"
                )
            missing_values = [
                field
                for field in _VALUE_REQUIRED_FIELDS
                if row.get(field) is None
            ]
            if missing_values:
                raise ValueError(
                    f"terminology TSV line {line} is missing values for: "
                    + ", ".join(missing_values)
                )
            row["_line"] = line
            rows.append(row)
    return rows


def _infer_domain(row: dict[str, object]) -> str | None:
    category = str(row["category"])
    source = str(row["source"])
    if category != "T.GAME.ENTITY":
        return CATEGORY_DOMAIN.get(category)
    if source in SHOP_NAMES or source in PLACE_ENTITY:
        return "places"
    if source in ITEM_SOURCES:
        return "items"
    if source in CREATURE_SOURCES:
        return "creatures"
    return None


def _build_report(rows: list[dict[str, object]]) -> dict[str, object]:
    counts = {domain: 0 for domain in DOMAINS}
    annotations = []
    unmapped = []
    mismatches = []
    shop_confirmations = []

    for row in rows:
        line = int(row["_line"])
        source = str(row["source"])
        target = str(row["target"])
        category = str(row["category"])
        source_tag = str(row["source_tag"])
        declared_domain = str(row["domain"])
        inferred_domain = _infer_domain(row)

        annotation = {
            "line": line,
            "source": source,
            "target": target,
            "category": category,
            "declared_domain": declared_domain,
            "domain": inferred_domain,
        }
        annotations.append(annotation)

        if inferred_domain is None:
            reason = (
                "unmapped T.GAME.ENTITY source"
                if category == "T.GAME.ENTITY"
                else f"unmapped category: {category}"
            )
            unmapped.append(
                {
                    **annotation,
                    "source_tag": source_tag,
                    "reason": reason,
                }
            )
            continue

        counts[inferred_domain] += 1
        if declared_domain != inferred_domain:
            mismatches.append(annotation)
        if source in SHOP_NAMES:
            shop_confirmations.append(annotation)

    return {
        "domains": DOMAINS,
        "rows": annotations,
        "counts": counts,
        "unmapped_count": len(unmapped),
        "unmapped": unmapped,
        "declared_domain_mismatch_count": len(mismatches),
        "declared_domain_mismatches": mismatches,
        "advisory_count": len(mismatches),
        "blocking_count": len(unmapped),
        "shop_confirmations": shop_confirmations,
        "ok": not unmapped,
    }


def run_domain_annotation(tsv_path, output_dir):
    """Read one terminology TSV, write its annotation report, and return it."""
    tsv_path = Path(tsv_path)
    output_dir = Path(output_dir)
    report = _build_report(_read_rows(tsv_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "domain_annotation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return report


def _print_summary(report: dict[str, object], output_dir: Path) -> None:
    counts = report["counts"]
    assert isinstance(counts, dict)
    print("=== domain 统计（含 ENTITY 细分）===")
    for domain in sorted(counts):
        print(f"  {domain:<12} {counts[domain]}")

    print("\n=== 未映射（需人工）===")
    unmapped = report["unmapped"]
    assert isinstance(unmapped, list)
    for item in unmapped:
        print(
            f"  L{item['line']} {item['source']!r} → {item['target']!r} "
            f"({item['reason']})"
        )

    print("\n=== 声明 domain 与推导 domain 不同（advisory）===")
    mismatches = report["declared_domain_mismatches"]
    assert isinstance(mismatches, list)
    for item in mismatches:
        print(
            f"  L{item['line']} {item['source']!r}: "
            f"{item['declared_domain']} → {item['domain']}"
        )

    print("\nannotation written:", output_dir / "domain_annotation.json")


def main(*, tsv_path=TSV, output_dir=OUT):
    signal.alarm(60)
    try:
        output_dir = Path(output_dir)
        report = run_domain_annotation(tsv_path, output_dir)
        _print_summary(report, output_dir)
        return 0 if report["ok"] else 1
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"domain annotation failed: {error}", file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
