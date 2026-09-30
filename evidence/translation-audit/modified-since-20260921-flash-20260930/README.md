# 09-21 以来已修改译文的 Gemini 快速复核（2026-09-30）

## 范围

- 基线 `7c38a53b`（上一轮全量已修改译文审计 `all-modified-review-20260922` 的冻结点）到 `9643e84c`，
  first-parent 57 次提交，净变更 **1190** 条：tome 586、orcs 315、cults 144、ashes-urhrok 118、engine 14、boot 8、possessors 5。
- 清单由 `inventory-recipe.py`（沿用上轮脚本，只改基线与终点）生成；`inventory.json` 只保留定位字段与快照哈希，
  原文与译文可由固定提交重建。

## 方法

1. **Gemini 初审**：Paseo → pi → `cpa/gemini-3.8-flash-high`，thinking=high，只读，纯文本作答。
   80 批（每批最多 30 条、约 30KB，长 lore 单条成批），3 路并发；每份结果校验批次回显与条目集合，
   不符即作废重派（q33、q56、q78 各重派一次）。覆盖 1190/1190，报 ISSUE 的条目 **119** 个。原始结论见 `gemini-reports/`。
2. **交叉核验**：宿主直接核验 13 个短条目（`HOST-VERDICTS.md` 前半），其余疑点分 41 包交
   Paseo → `claude/claude-opus-5-5`（medium）逐子项核验，允许只读查术语库、用户裁决、同文前后文与固定 commit 源码。
   结果见 `cross-reports/`。宿主抽查了机制类结论（如 crusader.lua 半径 1 攻击无 friendlyfire=false、Rapid Fire 需弓或投石索），未发现需推翻的结论。
3. 全部子 agent 均已归档；复核期间工作树无任何译文改动。

## 结果

| 分档 | 子项 | 条目 |
| --- | --- | --- |
| confirmed | 161 | **83**（tome 30、cults 24、orcs 22、ashes 6、engine 1） |
| advisory | 38 | 32 |
| refuted | 45 | 34 |

逐条清单见 [`CONFIRMED.md`](CONFIRMED.md)，修正片段在对应 cross 报告中。

主要驳回原因：Gemini 看不到术语库与既有裁决（Conclave＝孔克雷夫、stralite＝斯莱特、Epoch＝亚伯契、
draining physical＝生命汲取、Eldritch eye 保留音译），以及译文按实现校准而非按英文（驱散至多两项、失眠机制、心灵射击随机目标）。

需系列同步的项：Elvala 回忆录 8 章标题「时任……领袖」与正文矛盾，建议统一为
「摘自埃尔瓦拉最高议会领袖艾伦尼恩·加威尔的回忆录」。

## 状态

模型结论经宿主采纳为 confirmed，但**尚未修复**，也不是正式生产 `DONE_VERIFIED`。是否开修复窗口由用户决定。
