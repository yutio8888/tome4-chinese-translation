"""Render a traceable findings ledger from explicit adjudication mappings."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = {"opus-01": "Opus", "sol-01": "Sol", "gemini-01": "Gemini",
         "reference-blind-01": "独立盲审"}
STATES = {"ISSUE": "问题", "ADVISORY": "建议", "PENDING": "待确认"}


def main():
    ref = json.loads((ROOT / "REFERENCE.json").read_text())
    mapping = json.loads((ROOT / "ANON-MAPPING-HOST-ONLY.json").read_text())
    original = {o["observation_id"]: o for o in mapping["observations"]}
    lines = ["# 归并问题清单（暂定源码裁决）", "",
             "来源为三位参赛reviewer的28项观察及独立盲审的8项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据固定源码的暂定核验结果，非人工金标准。译文尚未修改。", "",
             "每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。", "",
             "| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |",
             "|---|---|---|---|---|---|"]
    ledger = []
    for did, defect in ref["canonical_defects"].items():
        sources = [original[oid] for oid, decision in ref["observations"].items() if did in decision["defects"]]
        per_arm = {}
        for arm in ["opus-01", "sol-01", "gemini-01"]:
            per_arm[arm] = "；".join(o["claim_id"] + "（原" + STATES[o["original_assertion"]] + "）"
                                  for o in sources if o["origin"] == arm) or "未提出此缺陷"
        evidence = defect["evidence"].replace("|", "\\|").replace("\n", " ")
        lines.append("| " + " | ".join([did, defect["entry_id"], *per_arm.values(), evidence]) + " |")
        ledger.append({"defect_id": did, **defect, "status": "confirmed_provisional",
                       "sources": [{"origin": o["origin"], "claim_id": o["claim_id"],
                                    "original_assertion": o["original_assertion"],
                                    "observation_id": o["observation_id"]} for o in sources],
                       "action": "recorded_for_later_translation_or_upstream_fix_no_change_applied"})
    lines += ["", "以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。", "",
              "| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |", "|---|---|---|---|---|"]
    for oid, decision in ref["observations"].items():
        if decision["status"] == "confirmed":
            continue
        o = original[oid]
        source = NAMES[o["origin"]] + " " + o["claim_id"] + "（原" + STATES[o["original_assertion"]] + "）"
        rationale = decision["rationale"].replace("|", "\\|").replace("\n", " ")
        lines.append("| " + " | ".join([oid, source, o["entry_id"], decision["status"], rationale]) + " |")
    lines += ["", "原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。", ""]
    (ROOT / "MERGED-FINDINGS.md").write_text("\n".join(lines))
    (ROOT / "MERGED-FINDINGS.json").write_text(json.dumps({
        "reference_status": ref["status"], "source_observation_count": len(original),
        "confirmed_defects": ledger,
        "observation_decisions": ref["observations"]}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()

