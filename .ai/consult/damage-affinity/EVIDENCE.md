# 议题：ToME4 简体中文本地化 —— `damage affinity` 的译名

你是本地化术语顾问。下面是**冻结的客观证据**。请只依据这些证据作答，不要臆测未列出的内容。

## 1. 机制实现（引擎源码，版本 1.7.6，commit 624a67329f）

`game/modules/tome/class/interface/Combat.lua:2351`
```lua
function _M:combatGetAffinity(type)
	if not self.damage_affinity then return 0 end
	return (self.damage_affinity.all or 0) + (self.damage_affinity[type] or 0)
end
```

`game/modules/tome/data/damage_types.lua:325-328`
```lua
-- affinity healing, we store it to apply it after damage is resolved
local affinity_heal = 0
if target.damage_affinity then
	affinity_heal = math.max(0, dam * target:combatGetAffinity(type) / 100)
end
```

`game/modules/tome/data/damage_types.lua:608-609`
```lua
if not target.dead and affinity_heal > 0 then
	target:heal(affinity_heal, src)
end
```

要点（可从上述代码直接读出）：
- `affinity_heal` 在伤害**结算之前**按原始伤害额计算，但在伤害**结算之后**才作为**治疗**施加。
- 它**不减少**这次伤害。角色照常掉血，随后回血。
- `if not target.dead` ——若这次伤害致死，治疗不会发生。

## 2. 游戏内对该机制的官方说明（英文原文）

```
#GOLD#Damage affinity: all#LAST#
All damage you receive, through any means, also heals you for this percentage of the damage.
This stacks with individual damage type affinities.
Important: Affinity healing happens after damage has been taken, it can not prevent death.
```
```
#GOLD#Damage affinity: specific#LAST#
All damage of this type that you receive, through any means, also heals you for this percentage of the damage.
Important: Affinity healing happens after damage has been taken, it can not prevent death.
```
装备对比界面的字段名：`Damage affinity(heal): `

## 3. 现行简体中文译法

`damage affinity` 一律译作「**伤害吸收**」，全库约 20 处。例：

| 英文 | 现行中文 |
|---|---|
| `Damage affinity(heal): ` | 伤害吸收（治疗）： |
| `#GOLD#Damage affinity: all#LAST#` | #GOLD#伤害吸收：全体#LAST# |
| `All damage you receive, through any means, also heals you for this percentage of the damage.` | 任何方式受到指定类型的伤害，都会按此比例治疗你。 |
| `Important: Affinity healing happens after damage has been taken, it can not prevent death.` | 注意：伤害吸收的治疗效果在伤害产生后处理，不能防止秒杀。 |
| `You gain %d%% Nature and Acid damage affinity.` | 获得 %d%% 自然和酸性伤害吸收。 |
| `increasing your darkness and light resistance and affinity by 5%%` | 获得暗影、光系抗性和伤害吸收各 5%% |
| `affinity %d%%; reduction %d; dur %d; cd %d` | 伤害吸收 %d%%; 减少 %d; 持续 %d; 冷却 %d |

## 4. 同一个中文词还承载着另一个机制

「伤害吸收」在本库中**同时**用于翻译护盾类机制的 absorb（引擎字段 `damage_shield_absorb` / `damage_shield_absorb_max`），那是**真正的吸收**——护盾替角色挡下伤害。约 8 处。例：

- 「护盾的最大伤害吸收值受精神或物理强度较高者加成。」
- 「伤害护盾，时间护盾，转移护盾：提高 %d%% 最大伤害吸收值。」
- 「有 %d%% 几率随机击碎目标身上一个临时的魔法或灵能伤害吸收护盾」
- 「一旦达到最大伤害吸收值（%d）或持续时间（%d 回合）结束……每回合回复总吸收伤害的 10%%」

## 5. `affinity` 一词在本库的非机制（散文）用法

以下场合 `affinity` 指「亲和／契合」，现译为「亲和力」等，与机制无关：

- `Thaloren have an affinity for natural elements` → 自然精灵对自然元素有亲和力
- `While Yeeks are not amphibians, they still have an affinity for water` → 虽然夺心魔不是两栖生物，但他们天生对水有种特殊的亲和力
- `He is impressed with your affinity for natural forces.` → 他对你同自然力量的亲和度感到惊讶

注意有一条同时含两种用法：
`Thaloren have an affinity for natural elements, allowing them to heal for a portion of damage taken from them.\n\t\tYou gain %d%% Nature and Acid damage affinity.`
现译：「自然精灵对自然元素有亲和力，这让它们在受到伤害时可以获得一定的治疗。\n\t\t获得 %d%% 自然和酸性伤害吸收。」

## 6. 其他语言的处理（供参考，不构成依据）

- 日文 `ja_JP`、韩文 `ko_KR`、繁体中文 `zh_hant` 亦在本仓库范围内，但本次不作为判据。

## 7. 约束条件

- 「伤害吸收」是**长期沿用**的既有术语，玩家社群、攻略、旧存档说明中已有惯性。改动成本真实存在。
- 若改，需要一次性覆盖全库约 20 处 `affinity` 条目；护盾类的 8 处「伤害吸收」是否保留原样也需一并说明。
- 译名须能自然嵌入既有句式，例如「获得 %d%% 自然和酸性 ____」「%d%% 光系 ____」「____（治疗）：」「____：全体／指定」。
- 目标读者是中文 roguelike 玩家，术语需简短、可作为界面字段名。

## 8. 请回答

1. **是否应当修改**？给出明确立场（改／不改），并说明理由中最有分量的一条。
2. 若改，**推荐译名**是什么？给 1 个首选 + 至多 2 个备选，各自说明取舍。
3. 你的推荐译名代入第 7 节列出的句式后，逐条写出实际效果，检查是否通顺。
4. 护盾类的「伤害吸收」应如何处置？
5. 若你的立场是「不改」，请说明第 4 节的一词两义冲突该如何应对。

请直接输出结论与论证，不要复述证据。用中文回答。
