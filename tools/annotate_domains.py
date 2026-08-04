#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""领域标注脚本：为术语表每行计算 domain（按 category 映射 + T.GAME.ENTITY 启发式细分）。
只输出标注清单（JSON + 待确认项），不写回 TSV。"""
import csv
import json
import signal
from collections import defaultdict
from pathlib import Path

signal.alarm(60)
ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "terminology.tsv"
OUT = ROOT / ".artifacts/i18n/terminology-audit"
OUT.mkdir(parents=True, exist_ok=True)

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
PLACE_ENTITY = {"cave", "rockwall", "exit to the worldmap", "primal trunk", "cracks", "Spacetime Tear"}
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
}

rows = []
with TSV.open("r", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h, delimiter="\t")
    for i, r in enumerate(rd, start=2):
        r["_line"] = i
        rows.append(r)

unmapped = []
confirm = []
counts = defaultdict(int)
for r in rows:
    cat = r["category"]
    src = r["source"]
    if cat == "T.GAME.ENTITY":
        if src in SHOP_NAMES:
            dom = "places"
            confirm.append((r["_line"], src, r["target"], "places", "城镇商店 → places"))
        elif src in PLACE_ENTITY:
            dom = "places"
        elif src in ITEM_SOURCES:
            dom = "items"
        elif src in CREATURE_SOURCES:
            dom = "creatures"
        else:
            dom = None
            unmapped.append((r["_line"], src, r["target"], r["source_tag"]))
    else:
        dom = CATEGORY_DOMAIN.get(cat)
        if dom is None:
            unmapped.append((r["_line"], src, r["target"], f"category={cat}"))
    r["domain"] = dom
    if dom:
        counts[dom] += 1

print("=== domain 统计（含 ENTITY 细分）===")
for d in sorted(counts):
    print(f"  {d:<12} {counts[d]}")
print("\n=== 未映射（需人工）===")
for line, src, tgt, why in unmapped:
    print(f"  L{line} {src!r} → {tgt!r} ({why})")
print("\n=== 商店确认 ===")
for line, src, tgt, dom, why in confirm:
    print(f"  L{line} {src!r} → {tgt!r} → {dom}（{why}）")

json.dump(
    {"domains": DOMAINS, "rows": [
        {"line": r["_line"], "source": r["source"], "target": r["target"],
         "category": r["category"], "domain": r["domain"]} for r in rows]},
    open(OUT / "domain_annotation.json", "w"), ensure_ascii=False, indent=1)
print("\nannotation written:", OUT / "domain_annotation.json")
