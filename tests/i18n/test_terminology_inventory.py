# -*- coding: utf-8 -*-
"""r2 术语审核生成器（tools/audit_dynamic.py r2 inventory）的表驱动测试。

覆盖 docs/terminology-review-round-2.md 2.1/2.2/3/6/7.1 的口径：
- 候选单元去重口径 (组件, source, source_tag)；
- A/B/C 类别与 P0-P4 批次归属；
- 登记判定复用 workset._scope_matches / _source_tag_matches 语义；
- B 类自动排除规则 B-AUTO-1 与 force_manual 阈值；
- 覆盖率数学（units == registered + missing 等）与四个 artifact 的输入快照。
"""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import audit_dynamic
from i18nlib.config import load_manifest
from i18nlib.locale_model import LocaleDocument


def _tr(
    source: str, target: str = "译", tag: str | None = "nil", section: str = "s"
) -> dict[str, object]:
    return {
        "kind": "translation",
        "source": source,
        "target": target,
        "source_tag": tag,
        "args_order": None,
        "special": None,
        "line": 1,
        "section": section,
    }


def _doc(*records: dict[str, object]) -> LocaleDocument:
    return LocaleDocument(
        logical_path="fixture.lua", sha256="0" * 64, records=tuple(records)
    )


def _row(
    source: str,
    tag: str,
    scope: str = "global",
    status: str = "existing",
    notes: str = "",
) -> dict[str, object]:
    return {
        "source": source,
        "target": "译",
        "category": "T.X",
        "domain": "combat",
        "source_tag": tag,
        "status": status,
        "scope": scope,
        "notes": notes,
        "_line": 2,
    }


class UnitBuildingTests(unittest.TestCase):
    def test_unit_dedup_and_corpus_counts(self) -> None:
        docs = {
            "tome": _doc(
                _tr("Arcane", "奥术", "damage type", "a.lua"),
                _tr("Arcane", "奥术", "damage type", "b.lua"),
                _tr("Fire", "火焰", "damage type", "a.lua"),
            ),
            "orcs": _doc(_tr("Arcane", "奥术", "damage type", "a.lua")),
            "ashes-urhrok": _doc(_tr("Wolf", "狼", "entity name", "a.lua")),
        }
        units, corpus = audit_dynamic.build_candidate_units(docs)
        arcane_tome = [
            u
            for u in units
            if u["source"] == "Arcane" and u["component"] == "tome"
        ]
        self.assertEqual(len(arcane_tome), 1)
        self.assertEqual(arcane_tome[0]["occurrences"], 2)
        self.assertEqual(arcane_tome[0]["sections"], ["a.lua", "b.lua"])
        self.assertEqual(arcane_tome[0]["cross_component_count"], 2)
        self.assertEqual(corpus["Arcane"]["occurrences"], 3)
        self.assertEqual(corpus["Arcane"]["components"], ["orcs", "tome"])
        self.assertEqual(len(units), 4)  # tome×2 + orcs×1 + ashes×1

    def test_case_and_plural_variants(self) -> None:
        docs = {
            "tome": _doc(
                _tr("Fire", "火焰", "damage type"),
                _tr("fire", "火", "talent name"),
                _tr("dwarf", "矮人", "entity type"),
                _tr("dwarfs", "矮人", "entity name"),
            )
        }
        _, corpus = audit_dynamic.build_candidate_units(docs)
        self.assertEqual(corpus["Fire"]["case_variants"], 1)
        self.assertEqual(corpus["fire"]["case_variants"], 1)
        self.assertEqual(corpus["dwarf"]["plural_variants"], 1)
        self.assertEqual(corpus["Fire"]["plural_variants"], 0)


class ClassificationTests(unittest.TestCase):
    def test_class_and_batch_by_tag(self) -> None:
        cases = (
            ("damage type", "A", "P0", False),
            ("effect subtype", "A", "P0", False),
            ("stat name", "A", "P0", False),
            ("talent category", "A", "P1", False),
            ("talent type", "A", "P1", False),
            ("entity type", "A", "P1", False),
            ("entity subtype", "A", "P3", False),
            ("faction name", "A", "P1", False),
            ("talent name", "B", "P2", False),
            ("entity name", "B", "P3", False),
            ("achievement name", "B", "P4", False),
            ("entity keyword", "B", "P1", True),  # provisional
            ("chat_demo", "B", "P4", False),
            ("dialog_portal", "B", "P4", False),
            ("_t", "C", "P4", False),
            ("tformat", "C", "P4", False),
            ("logSeen", "C", "P4", False),
            ("nil", "C", "P4", False),
            (None, "C", "P4", False),
            ("mystery-tag", "UNCLASSIFIED", "P4", False),
        )
        for tag, cls, batch, provisional in cases:
            with self.subTest(tag=tag):
                self.assertEqual(
                    audit_dynamic._unit_class_and_batch(tag),
                    (cls, batch, provisional),
                )

    def test_row_batch_assignment(self) -> None:
        cases = (
            ("damage type", "P0"),
            ("talent name", "P2"),
            ("entity name", "P3"),
            ("achievement name", "P4"),
            ("_t", "P4"),
            ("nil", "P4"),
            ("chat_demo", "P4"),
            ("no-such-tag", "UNASSIGNED"),
        )
        for tag, batch in cases:
            with self.subTest(tag=tag):
                self.assertEqual(audit_dynamic._row_batch(tag), batch)


class RegistrationSemanticsTests(unittest.TestCase):
    def test_scope_matching_for_dlc_and_core(self) -> None:
        rows = [
            _row("Arcane", "damage type", scope="dlc"),
            _row("Arcane", "damage type", scope="core"),
        ]
        docs = {
            "tome": _doc(_tr("Arcane", "奥术", "damage type")),
            "ashes-urhrok": _doc(_tr("Arcane", "奥术", "damage type")),
        }
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, rows)
        by_comp = {u["component"]: u for u in units}
        self.assertTrue(by_comp["tome"]["registered"])  # core 行匹配非 DLC
        self.assertTrue(by_comp["ashes-urhrok"]["registered"])  # dlc 行匹配 DLC
        self.assertEqual(len(by_comp["tome"]["term_rows"]), 1)
        self.assertEqual(by_comp["tome"]["term_rows"][0]["scope"], "core")

    def test_global_and_multi_match_any_component(self) -> None:
        rows = [_row("X", "talent name", scope="global")]
        docs = {"tome": _doc(_tr("X", "译", "talent name"))}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, rows)
        self.assertTrue(units[0]["registered"])

    def test_nil_row_matches_only_null_item_tag(self) -> None:
        rows = [_row("X", "nil", scope="core")]
        docs = {
            "tome": _doc(_tr("X", "译", None)),  # Lua nil
            "orcs": _doc(_tr("X", "译", "nil")),  # 字面字符串 "nil"
        }
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, rows)
        by_tag = {u["source_tag"]: u for u in units}
        self.assertTrue(by_tag[None]["registered"])
        self.assertFalse(by_tag["nil"]["registered"])

    def test_unmatched_scope_does_not_register(self) -> None:
        rows = [_row("Arcane", "damage type", scope="dlc")]
        docs = {"tome": _doc(_tr("Arcane", "奥术", "damage type"))}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, rows)
        self.assertFalse(units[0]["registered"])


class AutoExclusionTests(unittest.TestCase):
    def _units(
        self, records: tuple[tuple[str, str, str | None], ...]
    ) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
        docs = {"tome": _doc(*(_tr(src, tgt, tag) for src, tgt, tag in records))}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, [])
        return units, corpus

    def test_single_occurrence_b_unit_is_auto_excluded(self) -> None:
        units, _ = self._units((("Naga Boss", "娜迦首领", "entity name"),))
        self.assertTrue(units[0]["auto_excluded"])
        self.assertEqual(units[0]["exclusion_rule"], "B-AUTO-1")
        self.assertFalse(units[0]["force_manual"])

    def test_auto_exclusion_conditions(self) -> None:
        # (描述, 记录, 期望 auto_excluded)
        cases = (
            ("重复出现", (("Naga", "娜迦", "entity name"),) * 2, False),
            ("多译", (("Naga", "娜迦", "entity name"), ("Naga", "那迦", "entity name")), False),
            ("大小写变体", (("Fire", "火焰", "entity name"), ("fire", "火", "talent name")), False),
            ("复数变体", (("dwarf", "矮人", "entity name"), ("dwarfs", "矮人", "entity name")), False),
            ("A 类同源", (("Fire", "火焰", "entity name"), ("Fire", "火焰", "damage type")), False),
            ("跨组件", None, False),  # 单独构造
            ("单次无变体", (("Naga", "娜迦", "entity name"),), True),
        )
        for label, records, expected in cases:
            with self.subTest(label=label):
                if label == "跨组件":
                    docs = {
                        "tome": _doc(_tr("Naga", "娜迦", "entity name")),
                        "orcs": _doc(_tr("Naga", "娜迦", "entity name")),
                    }
                    units, corpus = audit_dynamic.build_candidate_units(docs)
                    audit_dynamic.annotate_units(units, corpus, [])
                else:
                    units, _ = self._units(records or ())
                self.assertEqual(
                    units[0]["auto_excluded"], expected, label
                )

    def test_force_manual_at_threshold(self) -> None:
        records = tuple(
            (_tr("Hotkey", "热键", "entity name") for _ in range(audit_dynamic.S2_2_THRESHOLD))
        )
        docs = {"tome": _doc(*records)}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, [])
        self.assertTrue(units[0]["force_manual"])
        self.assertFalse(units[0]["auto_excluded"])

    def test_registered_or_row_present_blocks_exclusion(self) -> None:
        docs = {"tome": _doc(_tr("Naga", "娜迦", "entity name"))}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, [_row("Naga", "entity name")])
        self.assertFalse(units[0]["auto_excluded"])
        self.assertTrue(units[0]["registered"])

    def test_a_class_units_never_auto_excluded(self) -> None:
        docs = {"tome": _doc(_tr("Arcane", "奥术", "damage type"))}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, [])
        self.assertEqual(units[0]["class"], "A")
        self.assertFalse(units[0]["auto_excluded"])

    def test_mechanism_key_tags_never_auto_excluded(self) -> None:
        # 技能名/成就名/叙事分类是机制关键（3.B），单次出现也不自动排除
        for tag in ("talent name", "achievement name", "newLore category"):
            with self.subTest(tag=tag):
                docs = {"tome": _doc(_tr("Naga", "娜迦", tag))}
                units, corpus = audit_dynamic.build_candidate_units(docs)
                audit_dynamic.annotate_units(units, corpus, [])
                self.assertFalse(units[0]["auto_excluded"], tag)

    def test_whitespace_sources_never_auto_excluded(self) -> None:
        docs = {"tome": _doc(_tr(" of lightning", "闪电之", "entity name"))}
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, [])
        self.assertFalse(units[0]["auto_excluded"])


class CoverageMathTests(unittest.TestCase):
    def test_totals_are_consistent(self) -> None:
        docs = {
            "tome": _doc(
                _tr("Arcane", "奥术", "damage type"),
                _tr("Naga", "娜迦", "entity name"),
                _tr("Hotkey", "热键", "entity name"),
                _tr("key", "键", "_t"),
            ),
        }
        rows = [_row("Arcane", "damage type", scope="core", status="preferred")]
        units, corpus = audit_dynamic.build_candidate_units(docs)
        audit_dynamic.annotate_units(units, corpus, rows)
        candidates = [u for u in units if u["class"] in ("A", "B", "UNCLASSIFIED")]
        self.assertEqual(len(candidates), 3)
        for unit in candidates:
            self.assertIn(unit["class"], ("A", "B"))
            self.assertNotIn(unit["batch"], (None, "UNASSIGNED"))
        totals = audit_dynamic._coverage_totals(candidates)
        self.assertEqual(totals["units"], 3)
        self.assertEqual(totals["missing"], totals["units"] - totals["registered"])
        self.assertEqual(
            totals["manual_remaining"],
            totals["missing"] - totals["auto_excluded"],
        )
        # C 类单元（_t）不进入候选
        self.assertTrue(all(u["class"] != "C" for u in candidates))


class InventoryArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()

    def test_end_to_end_writes_inventory_and_p1_workset_artifacts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-inventory-") as temporary:
            root = Path(temporary)
            translation = root / "fixture.lua"
            translation.write_text("-- fixture\n", encoding="utf-8")
            terminology = root / "terminology.tsv"
            terminology.write_text(
                "\t".join(audit_dynamic.TERMINOLOGY_FIELDS)
                + "\nArcane\t奥术\tT.GAME.DAMAGE\tcombat\tdamage type\tpreferred\tcore\tnote\n",
                encoding="utf-8",
            )
            manifest = replace(
                self.base_manifest,
                root=root,
                components=(
                    replace(self.base_manifest.components[0], id="fixture", translation="fixture.lua"),
                ),
                terminology="terminology.tsv",
            )
            docs = {
                "fixture": _doc(
                    _tr("Arcane", "奥术", "damage type"),
                    _tr("Naga", "娜迦", "entity name"),
                    _tr("Naga", "娜迦", "entity name"),
                )
            }
            rows = [
                {
                    "source": "Arcane",
                    "target": "奥术",
                    "category": "T.GAME.DAMAGE",
                    "domain": "combat",
                    "source_tag": "damage type",
                    "status": "preferred",
                    "scope": "core",
                    "notes": "note",
                    "_line": 2,
                }
            ]
            out = root / ".artifacts/i18n/terminology-review-r2"
            baseline = audit_dynamic.run_terminology_inventory(
                manifest=manifest, docs=docs, rows=rows, output_dir=out
            )
            for name in (
                "baseline.json",
                "candidate-inventory.json",
                "coverage.json",
                "exclusions.json",
                "worksets/P1-role-structure-v1.json",
            ):
                self.assertTrue((out / name).is_file(), name)
            inventory = json.loads((out / "candidate-inventory.json").read_text())
            self.assertEqual(inventory["schema_version"], 1)
            self.assertEqual(inventory["count"], 2)  # Arcane + Naga
            self.assertTrue(all(u["class"] in ("A", "B") for u in inventory["items"]))
            by_source = {u["source"]: u for u in inventory["items"]}
            self.assertTrue(by_source["Arcane"]["registered"])
            self.assertFalse(by_source["Naga"]["registered"])  # 重复出现不自动排除
            self.assertFalse(by_source["Naga"]["auto_excluded"])
            # 输入快照：SHA-256 必须与真实文件一致
            import hashlib
            self.assertEqual(
                inventory["inputs"]["terminology_sha256"],
                hashlib.sha256(terminology.read_bytes()).hexdigest(),
            )
            self.assertEqual(
                inventory["inputs"]["component_sha256"]["fixture"],
                hashlib.sha256(translation.read_bytes()).hexdigest(),
            )
            self.assertEqual(
                baseline["generator"]["source_sha256"],
                hashlib.sha256(Path(audit_dynamic.__file__).read_bytes()).hexdigest(),
            )
            self.assertEqual(baseline["summary"]["tsv_rows_review"]["total"], 1)
            self.assertEqual(baseline["summary"]["entries"], 3)
            coverage = json.loads((out / "coverage.json").read_text())
            self.assertEqual(
                coverage["by_source_tag"]["damage type"]["registered"], 1
            )
            self.assertEqual(coverage["by_source_tag"]["damage type"]["missing"], 0)
            exclusions = json.loads((out / "exclusions.json").read_text())
            self.assertEqual(exclusions["count"], 0)
            p1 = json.loads(
                (out / "worksets/P1-role-structure-v1.json").read_text()
            )
            self.assertEqual(p1["contract"], "tome4-terminology-review-workset-v1")
            self.assertEqual(p1["batch"], "P1")
            self.assertEqual(p1["summary"]["units"], 0)
            self.assertEqual(p1["sampling"]["population"], 0)

    def test_p1_workset_freezes_manual_rows_provisional_and_exclusion_sample(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-p1-workset-") as temporary:
            root = Path(temporary)
            translation = root / "fixture.lua"
            translation.write_text("-- fixture\n", encoding="utf-8")
            terminology = root / "terminology.tsv"
            terminology.write_text(
                "\t".join(audit_dynamic.TERMINOLOGY_FIELDS)
                + "\nTechnique\t格斗\tT.GAME.TALENT_CATEGORY\ttalents\ttalent type\tpreferred\tcore\tnote\n",
                encoding="utf-8",
            )
            manifest = replace(
                self.base_manifest,
                root=root,
                components=(
                    replace(
                        self.base_manifest.components[0],
                        id="fixture",
                        translation="fixture.lua",
                    ),
                ),
                terminology="terminology.tsv",
            )
            docs = {
                "fixture": _doc(
                    _tr("Technique", "格斗", "talent type"),
                    _tr("solitary", "孤立", "entity keyword"),
                    _tr("reused", "复用", "entity keyword"),
                    _tr("reused", "复用", "entity keyword"),
                )
            }
            rows = audit_dynamic.load_terminology_rows(terminology)
            out = root / ".artifacts/i18n/terminology-review-r2"
            audit_dynamic.run_terminology_inventory(
                manifest=manifest, docs=docs, rows=rows, output_dir=out
            )
            p1 = json.loads(
                (out / "worksets/P1-role-structure-v1.json").read_text()
            )
            self.assertEqual(
                p1["summary"],
                {
                    "units": 3,
                    "registered": 1,
                    "missing": 2,
                    "auto_excluded": 1,
                    "manual_remaining": 1,
                    "coverage": 0.3333,
                    "terminology_rows": 1,
                    "provisional_units": 2,
                    "exclusion_sample_size": 1,
                },
            )
            self.assertEqual(
                [item["source"] for item in p1["manual_candidates"]], ["reused"]
            )
            self.assertEqual(
                [item["source"] for item in p1["auto_exclusion_sample"]],
                ["solitary"],
            )
            self.assertEqual(p1["terminology_rows"][0]["source"], "Technique")


class ProjectionTests(unittest.TestCase):
    """长文本投影匹配器（5.3 高精度低召回策略）的表驱动测试。"""

    def _run(self, term_row: dict[str, object], records: tuple[dict[str, object], ...]) -> list[dict[str, object]]:
        docs = {"tome": _doc(*records)}
        report = audit_dynamic.run_projection(docs=docs, rows=[term_row])
        return report["candidates"]

    def _preferred(self, source: str, target: str, tag: str = "talent name") -> dict[str, object]:
        row = _row(source, tag, scope="core", status="preferred", notes="n")
        row["target"] = target
        return row

    def test_consistent_entry_is_not_a_candidate(self) -> None:
        term = self._preferred("Arcane Blade", "奥术之刃")
        candidates = self._run(
            term,
            (_tr("Arcane Blade deals damage.", "奥术之刃造成伤害。", "tformat"),),
        )
        self.assertEqual(candidates, [])

    def test_drift_is_a_candidate(self) -> None:
        term = self._preferred("Arcane Blade", "奥术之刃")
        candidates = self._run(
            term,
            (_tr("Arcane Blade deals damage.", "法术之刃造成伤害。", "tformat"),),
        )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["term_source"], "Arcane Blade")
        self.assertEqual(candidates[0]["matched"], "Arcane Blade")

    def test_word_boundary_prevents_partial_match(self) -> None:
        term = self._preferred("Fire", "火焰", tag="damage type")
        candidates = self._run(
            term,
            (_tr("Firebolt hits.", "火弹命中。", "tformat"),),
        )
        self.assertEqual(candidates, [])  # Firebolt 不是 Fire

    def test_case_sensitivity_for_proper_nouns(self) -> None:
        term = self._preferred("Fire", "火焰", tag="damage type")
        candidates = self._run(
            term,
            (_tr("the fire burns.", "火焰燃烧。", "tformat"),),
        )
        self.assertEqual(candidates, [])  # 专名大小写敏感，小写 fire 不匹配

    def test_ignorecase_for_lowercase_terms(self) -> None:
        term = self._preferred("dazed", "眩晕", tag="effect subtype")
        candidates = self._run(
            term,
            (_tr("You are Dazed!", "你被眩晕了！", "logPlayer"),),
        )
        self.assertEqual(candidates, [])  # 一致，不算候选

    def test_markup_is_stripped_from_target(self) -> None:
        term = self._preferred("Arcane Blade", "奥术之刃")
        candidates = self._run(
            term,
            (_tr("Arcane Blade hits.", "#LIGHT_BLUE#奥术之刃#WHITE#命中。", "tformat"),),
        )
        self.assertEqual(candidates, [])  # 标记内颜色名不干扰子串检查

    def test_short_terms_are_skipped(self) -> None:
        term = self._preferred("Ice", "冰", tag="damage type")
        report = audit_dynamic.run_projection(
            docs={"tome": _doc(_tr("Ice hits.", "冰击中。", "tformat"))},
            rows=[term],
        )
        self.assertEqual(report["terms"], 0)

    def test_blacklist_terms_are_skipped(self) -> None:
        term = self._preferred("Fire", "火焰", tag="damage type")
        report = audit_dynamic.run_projection(
            docs={"tome": _doc(_tr("Fire hits.", "火焰击中。", "tformat"))},
            rows=[term],
        )
        self.assertEqual(report["terms"], 0)  # Fire 在黑名单

    def test_rt_keys_are_not_scanned(self) -> None:
        term = self._preferred("Arcane Blade", "奥术之刃")
        report = audit_dynamic.run_projection(
            docs={"tome": _doc(_tr("Arcane Blade", "奥术之刃", "_t"))},
            rows=[term],
        )
        self.assertEqual(report["scanned_entries"], 0)

    def test_multiword_phrase_and_plural_forms(self) -> None:
        term = self._preferred("Sun Paladin", "太阳圣骑士")
        candidates = self._run(
            term,
            (_tr("Sun Paladins fight here.", "太阳圣骑士在此战斗。", "entity name"),),
        )
        self.assertEqual(candidates, [])  # 复数形式 + 词边界匹配，译文一致


if __name__ == "__main__":
    unittest.main()
