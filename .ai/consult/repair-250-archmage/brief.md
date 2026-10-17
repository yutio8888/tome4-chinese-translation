# 议题：ToME4 简中本 `Archmage` → 「元素法师」 是否应按单条修复改为「大法师」

你是三方独立评审之一。请只依据下面的实测底稿作答，不要访问网络。
可以读 /workspace/tome4-chinese-translation/mod-tome.lua 与 /workspace/t-engine4/game/modules/tome/ 自行复核。
（注意：上游源码检出在 /workspace/t-engine4，不在翻译仓；冻结 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 是它的 HEAD。）

## 待判条目
- section: `mod-tome/data/birth/classes/mage.lua`
- 源文: `Most Archmagi have been trained in the secret town of Angolwen and possess a unique spell to teleport to it directly.`
- 现译: `大多数元素法师在一个名叫安格利文的秘密小镇接受训练，并拥有一个直接传送到那里的独特技能。`

## 已有裁决与分歧（实测）
- 表层筛查（gpt 系）判 ISSUE：「Archmagi 意为大法师，却被译为『元素法师』」。
- 交叉复核判 OK（无异议）。
- 该批宿主裁决写成 `disposition=confirmed, repair_required=true`，但 conclusion 字段只有字面量
  `"repair_required"`，**没有任何论证**。该条自 2026-09-17 起滞留 repair_required 至今。

## 我（宿主）实测到的事实
1. `mod-tome.lua:3020`：`t("Archmage", "元素法师", "birth descriptor name")`
   —— 即「元素法师」是本库对 Archmage **职业名本身**的既定译名，不是本句的临时处理。
2. 全库计数（`grep -c`，mod-tome.lua）：「元素法师」24 处，「大法师」43 处。
   「大法师」的 43 处未逐条核实其对应英文，可能对应 Archmage 以外的词。
3. 上游 `data/birth/classes/mage.lua` 中 Archmage 是 mage 大类下的 subclass；
   其天赋树以四元素（火/冷/雷/地）为主干，另有 meta / temporal 等。
4. 本批另有一条既有惯例先例：`Wyrmic` 在本库定为「龙战士」（`mod-tome.lua:3169`），
   同样是「意译偏离字面」的职业名处理。

## 请回答三个问题
A. 本条应判 **confirmed（按单条改成「大法师」）**、**refuted（译文与既定职业名一致，不是本条缺陷）**，
   还是 **升级为全库术语议题（本条不改，另行走术语裁决）**？
B. 理由。若你主张改，请说明如何处理 `mod-tome.lua:3020` 的职业名本身与其余 23 处，
   以及不改它们会不会让玩家在职业选择界面与这段说明里看到两个名字。
C. 你对自己结论的把握（高/中/低）。

## 输出格式
只输出一段纯文本，首行为 `结论：confirmed` / `结论：refuted` / `结论：升级为术语议题`，
其后为理由与把握度。不要输出 JSON、不要围栏。
