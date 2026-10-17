# 议题：ToME4 技能名 `Arcane Combat` 的中文译名

**硬约束：候选译名必须 ≤4 个汉字。**

## 源码事实（/workspace/t-engine4/game/modules/tome/data/talents/techniques/magical-combat.lua:21）

```lua
name = "Arcane Combat",
type = {"technique/magical-combat", 1},
mode = "sustained",          -- 持续型
sustain_stamina = 20,
```

机制：开启后，近战攻击有几率**自动触发一个「允许用于 Arcane Combat」的法术**
（`talent.allow_for_arcane_combat`）。即「以近战带出法术」。
职业背景：`Arcane Blade`（战士系施法者）的核心持续技。

## 本库既定译名（不可与之冲突）

| 源文 | 现有译名 | 说明 |
|---|---|---|
| `technique/magical-combat` | 魔法格斗 | 本技能所属的技能树 |
| `Arcane Blade` | 奥术之刃 | 职业名 |
| `Arcane Cunning` | 奥术灵巧 | 同树技能 |
| `Arcane Feed` | 奥术充能 | 同树技能 |
| `Arcane Destruction` | 奥术毁灭 | 同树技能 |
| **`Arcane Combat`** | **奥术武器** | **当前译名，共 5 处** |

同树四个技能都是「奥术」+ 两字，构词高度统一。

## 问题

现译「奥术武器」把 `Combat`（战斗/格斗）译成了「武器」，两轮独立审核均判为错位。
（更正：我一度以为「造成 %d%% 奥术武器伤害」里的「武器」是译者多加的，
维护者指出这是本库/ToME4 的既定约定——`%d%%` 伤害指基于武器基础伤害的百分比伤害，
`%0.2f` 才是固定点数伤害，所以「武器」二字是必要消歧，不构成问题。）

我方初步候选：**奥术战斗**。也考虑过「奥术格斗」（呼应技能树「魔法格斗」）、
「奥术附法」「奥术连击」。

## 请回答（简短，不要长篇）

1. 你推荐哪一个？只给 1 个首选 + 至多 2 个备选，每个 ≤4 汉字。
2. 一句话理由：为什么它比「奥术武器」和我方候选「奥术战斗」更好（或为什么「奥术战斗」已经足够）。
3. 是否存在你认为必须避免的候选？为什么。
