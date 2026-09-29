# batch-010：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00361
位置：mod-tome.lua:1457；section：mod-tome/class/interface/PlayerQuestPopup.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' completed! #WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_GREEN#任务“%s”完成！#WHITE#（按 J 键查看任务日志）
```

## entry-00362
位置：mod-tome.lua:1458；section：mod-tome/class/interface/PlayerQuestPopup.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' completed!
```
译文：
```text
#LIGHT_GREEN#任务“%s”已完成！
```

## entry-00363
位置：mod-tome.lua:1459；section：mod-tome/class/interface/PlayerQuestPopup.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' is done! #WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_GREEN#任务“%s”完成！#WHITE#（按 J 键查看任务日志）
```

## entry-00364
位置：mod-tome.lua:1460；section：mod-tome/class/interface/PlayerQuestPopup.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' done!
```
译文：
```text
#LIGHT_GREEN#任务“%s”已完成！
```

## entry-00365
位置：mod-tome.lua:1461；section：mod-tome/class/interface/PlayerQuestPopup.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#Quest '%s' is failed! #WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_RED#任务“%s”失败！#WHITE#（按 J 键查看任务日志）
```

## entry-00366
位置：mod-tome.lua:1462；section：mod-tome/class/interface/PlayerQuestPopup.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_RED#Quest '%s' failed!
```
译文：
```text
#LIGHT_RED#任务“%s”失败了！
```

## entry-00367
位置：mod-tome.lua:1524；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Healing mod#LAST#
This represents how effective healing is for you.
All healing values are multiplied by this value (including life regeneration).
It is increased by Constitution.

```
译文：
```text
#GOLD#治疗系数#LAST#
该系数表明治疗对你的生效程度。
所有治疗的基础值需要乘上这个系数（包括生命自然恢复）。
体质会增加该项属性。

```

## entry-00368
位置：mod-tome.lua:1579；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Equilibrium#LAST#
Equilibrium reflects your standing in the grand balance of nature and how easily you can access Wild Gifts.
The closer it is to 0 the more in-balance you are.
Being too far out of balance may cause your Wild Gifts to fail when called upon.

```
译文：
```text
#GOLD#失衡值#LAST#
失衡值是你保持自然平衡的能力，决定了你使用野性系技能的难易程度。
失衡值越接近于0你破坏自然平衡的量越少。
当你的失衡值过高时，你使用野性系技能时可能会失败。

```

## entry-00369
位置：mod-tome.lua:1619；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Feedback#LAST#
Feedback represents using pain as a means of psionic grounding and it can be used to power feedback abilities.
Feedback decays at the rate of 10% or 1 per turn (which ever is greater) depending on talents.
All damage you take from an outside source will increase your Feedback based on to how much of your health is lost and your level.  First level characters gain 100 Feedback when losing 50% health, while 50th level characters gain the same amount when losing 20% health.

```
译文：
```text
#GOLD#反馈值#LAST#
反馈值代表以痛苦作为灵能的定锚，可以用于驱动反馈类技能。
反馈值每回合按 10% 或 1 点（取较大者）衰减，具体衰减速率还受技能影响。
你从外界受到的所有伤害都会增加你的反馈值，增加的数值取决于你损失生命值的百分比和你的等级。1级人物在损失50%生命后获得100反馈值，而50级人物损失20%生命后获得同样多的反馈值。

```

## entry-00370
位置：mod-tome.lua:1628；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Necrotic Aura#LAST#
Represents the raw materials for creating undead minions.
It increases each time you or your minions kill something that is inside the aura radius.

```
译文：
```text
#GOLD#死灵光环#LAST#
代表召唤死灵生物的原材料。
每当你或你的随从杀死光环范围内的生物时，光环会增强。

```

## entry-00371
位置：mod-tome.lua:1656；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Inscriptions#LAST#
The people of Eyal have found a way to create herbal infusions and runes that can be inscribed on the skin of a creature.  More exotic types of inscriptions also exist.
Those inscriptions give the bearer always-accessible powers that can be used an unlimited number of times.
A simple regeneration infusion is the most common type of infusion, and the use of runes of various types is also common among arcane users.

```
译文：
```text
#GOLD#刻印#LAST#
埃亚尔的人们找到了制作草本纹身与符文、并将其纹刻在生物皮肤上的方法。此外，还存在一些更为奇异的刻印。
刻印给被刻印者提供一些可以无限使用的特殊能力。
最常见的一种纹身是简单的回复纹身，而各类符文在奥术施法者之中也同样常见。

```

## entry-00372
位置：mod-tome.lua:1677；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Activated Talents#LAST#
Most talents require activation (i.e. time) to use, and create a specific effect when called upon.
Specific information on each talent appears its tooltip.
```
译文：
```text
#GOLD#主动技能#LAST#
大部分技能都需要主动（花费时间）来使用，并且会在使用时产生特定的效果。
有关技能的详细信息，请参阅技能的提示框。
```

## entry-00373
位置：mod-tome.lua:1689；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Passive Talents#LAST#
When learned, passive talents permanently alter the user in some way.
The effects are always present and are usually not dispellable or removable, though other effects may counteract or negate them.
Specific information on each talent appears its tooltip.
```
译文：
```text
#GOLD#被动技能#LAST#
当你学会被动技能之后，它会以某种方式永久性的给玩家带来改变。
这些效果始终存在，通常不会被解除或移除，但是有些特殊效果可能会抵消或消除它们。
有关技能的详细信息，请参阅技能的提示框。
```

## entry-00374
位置：mod-tome.lua:1772；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Magic#LAST#
Magic defines your character's ability to manipulate the magical energy of the world. It increases your Spellpower, Spell Save, and the effect of spells and other magic items.

```
译文：
```text
#GOLD#魔法#LAST#
魔法属性影响你驾驭魔法能量的能力，提升魔法可以提高你的法术强度，提升法术豁免，并提高法术和其他魔法物品的效果。

```

## entry-00375
位置：mod-tome.lua:1782；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Cunning#LAST#
Cunning defines your character's ability to learn, think, and react. It allows you to learn many worldly abilities, and increases your Mindpower, Mental Save, and critical chance.

```
译文：
```text
#GOLD#灵巧#LAST#
灵巧决定你角色学习、思考和反应的能力。它让你能够学习许多世俗的技艺，并提升你的精神强度、精神豁免和暴击几率。

```

## entry-00376
位置：mod-tome.lua:1829；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Armour Penetration#LAST#
Armour penetration allows you to ignore a part of the target's armour (this only works for armour, not damage resistance).
This can never increase the damage you do beyond reducing armour, so it is only useful against armoured foes.

```
译文：
```text
#GOLD#护甲穿透#LAST#
护甲穿透可以让你忽视部分目标护甲值（只对护甲值有效，对伤害抗性无效）。
除了减少护甲之外，它绝不会额外提高你造成的伤害，因此只对有护甲的目标有用。

```

## entry-00377
位置：mod-tome.lua:1882；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Armour#LAST#
Armour value is a damage reduction from all incoming melee and ranged weapon attacks.
Absorbs (hardiness)% of incoming weapon damage, up to a maximum of (armour) damage absorbed.
This is countered by armour penetration and is applied before all kinds of critical damage increase, talent multipliers and damage multiplier, thus making even small amounts have greater effects.

```
译文：
```text
#GOLD#护甲值#LAST#
护甲值是受到近身或者远程武器伤害时伤害的减免量。
护甲可以吸收（护甲强度）%武器伤害，但最多吸收相当于护甲值的伤害。
此数值会因护甲穿透减少，并且这一判定作用发生在所有暴击伤害加成、技能加成和伤害加成之前。也就是说即使是很小的数值也会有更大的作用。

```

## entry-00378
位置：mod-tome.lua:1891；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Armour Hardiness#LAST#
Armour hardiness represents how much of each incoming blows the armour will affect.
Absorbs (hardiness)% of incoming weapon damage, up to a maximum of (armour) damage absorbed.

```
译文：
```text
#GOLD#护甲强度#LAST#
护甲强度表示护甲可以减免的伤害百分比。
护甲吸收（护甲强度）%武器伤害，但最多吸收相当于护甲值的伤害。

```

## entry-00379
位置：mod-tome.lua:1903；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Crits Shrug Off#LAST#
Gives a chance to ignore the bonus critical damage from any direct damage attacks (melee, spells, ranged, mind powers, ...).

```
译文：
```text
#GOLD#暴击摆脱#LAST#
有几率完全忽略任何直接伤害攻击（近战、法术、远程、精神力量……）所造成的额外暴击伤害。

```

## entry-00380
位置：mod-tome.lua:1923；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Physical saving throw#LAST#
Increases chance to shrug off physically-induced effects.  Also reduces duration of detrimental physical effects by up to 5% per point, depending on the power of the opponent's effect.

```
译文：
```text
#GOLD#物理豁免#LAST#
增加你摆脱物理引发效果的几率。此外，每点最多减少 5% 不良物理状态的持续时间，具体取决于对方效果的强度。

```

## entry-00381
位置：mod-tome.lua:1945；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Physical critical chance#LAST#
Each time you deal damage with a physical ability you may have a chance to perform a critical hit that deals extra damage.
Some talents allow you to increase this percentage, and it may be modified by your weapon.
It is improved by Cunning.

```
译文：
```text
#GOLD#物理暴击#LAST#
每次以物理技能造成伤害时你都有一定几率暴击造成额外伤害。
一些技能可以提高这个几率，它也可能受你的武器影响。
灵巧属性可以提升这个几率。

```

## entry-00382
位置：mod-tome.lua:1954；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Spellpower#LAST#
Your spellpower represents how powerful your magical spells are.  It is opposed by your opponent's spell save.
In addition, when your spells inflict temporary detrimental effects, every point your opponent's save exceeds your spellpower will reduce the duration of the effect by 5%.

```
译文：
```text
#GOLD#法术强度#LAST#
你的法术强度决定了你施放法术技能的威力。敌人用法术豁免对抗你的法术强度。
另外当你的法术造成临时性负面效果时，敌人的相应豁免每超过法术强度一点将减少5%持续时间。

```

## entry-00383
位置：mod-tome.lua:1961；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Spell critical chance#LAST#
Each time you deal damage with a spell you may have a chance to perform a critical hit that deals extra damage.
Some talents allow you to increase this percentage.
It is improved by Cunning.

```
译文：
```text
#GOLD#法术暴击#LAST#
每次以法术造成伤害时你都有一定几率暴击造成额外伤害。
一些技能可以提高这个几率。
提升灵巧属性值可以提高法术暴击率。

```

## entry-00384
位置：mod-tome.lua:1977；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Spellcooldown#LAST#
Spell cooldown represents how fast your spells will come off of cooldown.
The lower it is, the more often you'll be able to use your spell talents and runes.

```
译文：
```text
#GOLD#法术冷却时间#LAST#
法术冷却时间反映了你的法术需要多久才能脱离冷却。
它的数值越低，你越可以频繁的使用法术和符文技能。

```

## entry-00385
位置：mod-tome.lua:1991；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Mental critical chance#LAST#
Each time you deal damage with a mental attack you may have a chance to perform a critical hit that deals extra damage.
Some talents allow you to increase this percentage.
It is improved by Cunning.

```
译文：
```text
#GOLD#精神暴击#LAST#
每次以精神攻击造成伤害时你都有一定几率暴击造成额外伤害。
一些技能可以提高这个几率。
提升灵巧属性值可以提高精神暴击。

```

## entry-00386
位置：mod-tome.lua:2057；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Damage resistance: by speed#LAST#
All damage you receive, through any means, is decreased by this percentage, which increases as your total movement speed (global times movement) decreases.
This is applied after normal damage type resistances.

```
译文：
```text
#GOLD#伤害抗性：速度#LAST#
所有类型任何方式对你造成的伤害按此值减免，随着你的总体移动速度（全局速度×移动速度）减少而增加。
该效果在常规伤害类型抗性之后生效。

```

## entry-00387
位置：mod-tome.lua:2069；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Damage affinity: all#LAST#
All damage you receive, through any means, also heals you for this percentage of the damage.
This stacks with individual damage type affinities.
Important: Affinity healing happens after damage has been taken, it can not prevent death.

```
译文：
```text
#GOLD#伤害亲和：全体#LAST#
任何方式对你造成的所有类型伤害，都会按此比例治疗你。
可以与独立类型的伤害亲和效果叠加。
注意：伤害亲和的治疗在伤害结算之后才生效，不能防止死亡。

```

## entry-00388
位置：mod-tome.lua:2078；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Damage affinity: specific#LAST#
All damage of this type that you receive, through any means, also heals you for this percentage of the damage.
Important: Affinity healing happens after damage has been taken, it can not prevent death.

```
译文：
```text
#GOLD#伤害亲和：指定#LAST#
任何方式对你造成的此类型伤害，都会按此比例治疗你。
注意：伤害亲和的治疗在伤害结算之后才生效，不能防止死亡。

```

## entry-00389
位置：mod-tome.lua:2085；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Status resistance#LAST#
Most bad status effects can be avoided by having an appropriate immunity, represented by a percent chance to completely avoid the effect in question.  This chance is applied in addition to any saving throws or other checks that may apply.

```
译文：
```text
#GOLD#状态免疫#LAST#
大部分负面状态效果可以被特定的免疫来抵消，以百分比表示你完全免疫该效果的几率。这一几率会与任何适用的豁免或其他判定叠加计算。

```

## entry-00390
位置：mod-tome.lua:2206；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Stealth#LAST#
To use stealth one must possess the 'Stealth' talent.
Stealth allows you to try to hide from any creatures that would otherwise see you.
Even if they have seen you they will have a harder time hitting you.
Any creature can try to see through your stealth.

```
译文：
```text
#GOLD#潜行#LAST#
要使用潜行角色必须具有潜行技能。
潜行让你可以尝试躲避那些本来能看见你的生物。
就算他们发现了你，也更难击中你。
任何生物都可以尝试识破你的潜行。

```

## entry-00391
位置：mod-tome.lua:2222；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Invisibility#LAST#
Invisible creatures are magically removed from the sight of all others. They can only be see by creatures that can see invisible.

```
译文：
```text
#GOLD#隐形#LAST#
隐形生物通过魔法从所有其他生物的视线中消失。他们只能被有侦测隐形能力的生物发现。

```

## entry-00392
位置：mod-tome.lua:2270；section：mod-tome/class/interface/TooltipsData.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Shield Block Value#LAST#
The base amount of damage a shield will block when actively used in defense.
Mind damage cannot be blocked. Against other damage types you gain a 50%% bonus to the block value if the shield used grants resistance to that damage type.

```
译文：
```text
#GOLD#盾牌格挡值#LAST#
盾牌在主动用于防御时所能阻挡的基础伤害量。
精神伤害无法被格挡。面对其他伤害类型时，如果所用盾牌提供该类型的抗性，你的格挡值会获得 50%% 加成。

```

## entry-00393
位置：mod-tome.lua:2281；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Roguelike)
```
译文：
```text
%s（永久死亡模式）
```

## entry-00394
位置：mod-tome.lua:2282；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Exploration mode)
```
译文：
```text
%s（探索模式）
```

## entry-00395
位置：mod-tome.lua:2283；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Nightmare (Adventure) difficulty)
```
译文：
```text
%s (噩梦难度（冒险模式）)
```

## entry-00396
位置：mod-tome.lua:2284；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Nightmare (Roguelike) difficulty)
```
译文：
```text
%s (噩梦难度（永久死亡模式）)
```

## entry-00397
位置：mod-tome.lua:2285；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Insane (Adventure) difficulty)
```
译文：
```text
%s (疯狂难度（冒险模式）)
```

## entry-00398
位置：mod-tome.lua:2286；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Insane (Roguelike) difficulty)
```
译文：
```text
%s (疯狂难度（永久死亡模式）)
```

## entry-00399
位置：mod-tome.lua:2287；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Madness (Adventure) difficulty)
```
译文：
```text
%s (绝望难度（冒险模式）)
```

## entry-00400
位置：mod-tome.lua:2288；section：mod-tome/class/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Madness (Roguelike) difficulty)
```
译文：
```text
%s (绝望难度（永久死亡模式）)
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
grounding 	绝缘的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的绝缘前缀；保留 source 尾空格；不约束灵能 grounding、接地导线或其他语境
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
inscriptions	刻印	T.GAME.TALENT_CATEGORY	talents	talent category	preferred	global	统一核心和兽人战役的技能类别译法；具体类型仍使用“纹身/符文”
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
