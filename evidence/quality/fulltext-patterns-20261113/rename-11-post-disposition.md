# 11 组玩家技能撞名：改名裁决（post-disposition，2026-11-13）

- **授权**：维护者对全文检索后的建议回复「同意」。范围是 `p2-talent-name-pending.json` 中玩家↔玩家的 11 组强候选，其余 12 组、ego 词缀、Clork 与潜行/隐形侦测**不在本次范围**。
- **冻结基线**：检索基线（`6ef227f93`）与 `REPORT.md` 不回写，本文件只追加处置结果。
- **定义复核**：每个对象都在固定核心源码 `624a67329fe2` 或公开 DLC 检出（来源未固定）中找到独立的 `newTalent` 定义，英文名与机制均不同，确认为不同技能。这些名称都没有术语表行。
- **命名**：使用 Gemini 4 Argon（`antigravity/gemini-4-argon`，thinking medium，agent `32059e0c`，独立本地 workspace，串行一次咨询，已归档），沿用既有纯名称流程。
  - 输入：每个对象的英文、技能树、来源、模式与机制，以及已占用名称表。
  - 输出：每组保留方及理由，每个改名对象 3 个按优先级排列的候选。
  - 主代理核实了前提（技能树、机制与描述），没有发现影响结论的事实错误，全部采用首选。
  - 原始 prompt 与答复见 `rename-11-gemini-prompt.md` 和 `rename-11-gemini.json`。
- **双向查重**：
  - 新名→其他英文：每个首选在 29,554 条有效条目的目标文和 `terminology/*.tsv` 中都是 0 次出现（按子串查）；其余候选也都是 0。
  - 原英文→全部译法：在所有有效条目中按词边界检索被改名英文（包括长文本），列出实际指代。区分以下三类：技能本身、同一对象的效果/伤害类型（合法的同名关系，同步修改）、普通词义用法（不改）。

## 逐组处置

| 组 | 保留旧名 | 改名对象 → 新名 | 同步修改的条目 | 保留理由 |
| --- | --- | --- | --- | --- |
| 重组 | Re-assemble（骷髅种族） | Realign → 身心调谐；Reform → 重聚成形；Rethread → 重编时间线 | Realign 自身说明中的动词「重组」改为「校准」；Reform 说明，以及 Shadow Mages 说明「尝试 Reform」；Rethread 说明 2 处，以及 Braid Lifelines 说明「你的 Rethread」 | 英文字面即「重新组装」；死亡界面与出生说明「重组你的骨头复活」已绑定 |
| 地震 | Earthquake（石系） | Quake（沙龙）→ 震地猛击 | 仅名称（说明中的 quake 是普通名词） | 标准对应词 |
| 无情 | Pitiless（Ashes 魔化精灵） | Brutality（暴走）→ 狂暴虐杀 | 仅名称 | Pitiless 字面即「无情」；「残暴」已被 Ashes 技能树占用 |
| 奥术充能 | Arcane Feed | Eldritch Infusion → 秘法灌注 | 仅名称 | Feed＝供给/充能，机制为持续回复法力 |
| 双重射击 | Double Shots（Orcs 枪手） | Dual Arrows（弓）→ 双箭齐发 | 仅名称 | 「Double Shots」直译即「双重射击」 |
| 肢解 | Dismember（Ashes） | Mow Down（Orcs）→ 绞肉收割 | 仅名称（tome-orcs.lua） | 标准词义 |
| 坚定意志 | Unbreakable Will（意志天赋，含日志） | Resolve（反魔法）→ 抗逆决意 | 自身效果名及「+/-」标签（physical.lua） | 名称含 Will，效果是直接无视精神效果 |
| 快速射击 | Quick Shot（时空射击） | Swift Shot（游击投石）→ 疾风投射 | 自身效果名；另一投石技能说明「使用 Swift Shot」 | 字面最直接 |
| 迅捷 | Celerity（含自身效果与「%d 迅捷」） | Quickened（夺心魔种族）→ 思维加速 | 仅名称 | 状态栏显示需要简短的双字名 |
| 烟雾弹 | Smoke Bomb（火焰炼金；NPC 同名技能共享键） | Smokescreen → 烟幕障眼 | Smokescreen Mastery → 烟幕障眼精通；伤害类型 smokescreen；「你的 Smokescreen」说明 | 字面即「烟雾弹」；说明里实体道具 smokebomb/smoke bomb 仍译「烟雾弹」 |
| 致命恐惧 | Mortal Terror（嗜血） | Terrorize（暗杀）→ 恐吓震慑 | 仅名称 | 一一对应 |

共修改 27 条（mod-tome.lua 26 条，tome-orcs.lua 1 条），全部在 lite 维护批 0508 中完成；条目清单见 `evidence/lite-review/batches/0508/maintenance.json`。没有改动英文键、技能 ID、变量或存档身份。

## 门禁与盲审

- **0508**（`dce845204`）：27 条修改。srccheck 显示源串未变，严格 lint 0 错误，完整门禁通过，已经过滤镜像推送。
- **0509**（`a7b6dd88d`）：A/B 盲审 26 个单位。A 报 1 个问题，B 报 2 个，均为被改说明里原有的措辞缺陷，主代理确认后修复：
  - Braid Lifelines 说明多出一个换行，并把「共享伤害比例受法术强度影响」误写成「伤害受法术强度影响」（B；timeline-threading.lua:203–210）；
  - Realign 说明的数量缺少量词，「治愈……生命」搭配不当（A、B 都报；finer-energy-manipulations.lua:79）。
- **0510**（`a26c89eef`）：A/B 盲审 2 个单位，ISSUE 0，收口。
- 没有新开游戏测试，没有发布新版本；公开插件仍为 v0.3.12。

## 未改动，并记录原因

- Cults 效果「Persistant Will」仍译「坚定意志」，与保留方 Unbreakable Will 同名。这是效果与技能之间的名称重合，不属于本次玩家↔玩家的 11 组，作为剩余缺口单列。
- 以下都不在本次范围：Ashes 效果子类型 seismic「地震」；ego 关键词 implacable「无情」；Anomaly Quake「异常：地震」（技能名本身带前缀）。
- lore 与其他技能说明中 brutality、resolve、realign、reform 等词的普通用法，都不指代这些技能。
- 同组之外的其余 12 组同名候选，没有获得改名授权。
