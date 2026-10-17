# 咨询：ToME4 汉化中 `stralite` 的译名

## 问题
`stralite` 现译「蓝锆石」（blue zircon，一种宝石），但它在游戏中是**金属**。
请评估是否应改名；若应改，给出你推荐的译名与理由。

## 固定源码事实（ToME 1.7.6，commit 624a6732，公开 GPL 源码）

金属材质阶梯（装备等级 1→5）：
  iron → steel → dwarven steel → **stralite** → voratun

本库现有译名：
  iron=铁, steel=钢, d.steel=矮人钢, **stralite=蓝锆石**, voratun=沃瑞钽
  （voratun 是音译，用了金属旁的「钽」）

证明 stralite 是可冶炼、可锻造的金属：
- `New smelting techniques developed allow more stralite to be recovered from existing veins.`
  （冶炼技术、从矿脉提取）
- `Inch-thick stralite plates lock together with voratun joints.`（一英寸厚的板材）
- `lump of stralite` → 现译「蓝锆石块」（金属锭/矿石块）
- `The blade of this sword seems to have been forged of a mixture of voratun and stralite.`（锻造）
- 装备：`stralite plate armour`, `stralite mail armour`, `stralite battleaxe`,
  `stralite greatsword`, `stralite ring`, `stralite amulet`, `stralite shield`,
  `pouch of stralite shots`, `stralite steamgun`, `stralite steamsaw` 等
- `By mounting a brain in a jar in a stralite frame...`（金属框架）
- 游戏中 stralite 装备呈蓝色调（推测是原译者选「蓝」的由来）

## 现状与代价
- 影响 69 行：mod-tome.lua 50、tome-orcs.lua 18、tome-cults.lua 1
- 术语库 `terminology/items.tsv:44` 已登记为 `preferred`，备注原文：
  「高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的"蓝皓石"」
  —— 即登记者明知是金属仍选了宝石名，且曾有过另一译名「蓝皓石」被统一掉
- 改名需同步 69 行 + 术语库登记行，并通过 runtime-collision 门禁

## 候选（不限于此）
1. 维持「蓝锆石」
2. 「蓝钢」——2 字，金属，保留蓝色
3. 「斯特莱」——纯音译，与「沃瑞钽」处理一致
4. 你自己的提案

## 请回答
1. 是否构成需要修复的译名缺陷？（是/否 + 一句话理由）
2. 若是，推荐译名是什么？为什么它比其它候选好？
3. 该译名在这些实际串里读起来是否自然：
   「__板甲」「__块」「__蒸汽枪」「__戒指」「一袋__子弹」
   「新的冶炼技术让更多__从现有矿脉中提取出来」
4. 有什么我没考虑到的风险或反对理由？

请直接给出结论与理由，不超过 400 字。全程只读，不要修改任何文件。
