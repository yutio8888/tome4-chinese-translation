# batch-127：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03993
位置：tome-orcs.lua:5972；section：tome-orcs/data/talents/uber/cun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Rak'Shor's Cunning (Ghoul)
```
译文：
```text
拉克·肖的狡诈（食尸鬼）
```

## entry-03994
位置：tome-orcs.lua:5997；section：tome-orcs/data/talents/uber/mag.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Spell damage done to it ripples in radius 4 doing 130% arcane damage.
```
译文：
```text
其受到的法术伤害转化为波纹，对半径 4 内的所有目标造成等同于该伤害 130% 的奥术伤害。
```

## entry-03995
位置：tome-orcs.lua:6000；section：tome-orcs/data/talents/uber/mag.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03996
位置：tome-orcs.lua:6002；section：tome-orcs/data/talents/uber/mag.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Any spell damage you deal to it will ripple around in radius 4 as 160% arcane damage.
```
译文：
```text
其受到的法术伤害转化为波纹，对半径 4 内的所有目标造成等同于该伤害 160% 的奥术伤害。
```

## entry-03997
位置：tome-orcs.lua:6019；section：tome-orcs/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Technomancers are Archmages that dabble in steam technology to enhance their already formidable arsenal of spells.
		Once this class evolution is taken, you gain the following:
		- Arcane Dynamo tinker schematic
		- Steamtech/Physics category (unlocked)
		- Steamtech/Chemistry category (locked)
		- An Automated Portable Extractor (A.P.E.)
		- One point in the Physics talent Smith and two in Mechanical and Electricity
		- Spell/Galvanic Technomancy category (locked) - deals with fire and lightning
		- Spell/Terrene Technomancy category (locked) - deals with earth and water
		- Spell/Occult Technomancy category (locked) - deals with time and arcane
		- The ability to unlock one of the three Technomancy categories for free

		Once put in a robe, the Arcane Dynamo will regenerate Steam each time mana is spent and increase Spellpower based on current steam level.

		#{bold}#As soon as this evolution is used you will need to craft the Arcane Dynamo to place in a robe to benefit from all the powers of the Technomancer.#{normal}#
```
译文：
```text
科技法师是一些特殊的元素法师，他精通于蒸汽科技，用科技的力量来强化他们已经足够强大的法术力量。
		当你选择这一项进阶职业的时候，你获得以下能力：
		- 奥术发电机插件配方
		- 蒸汽/物理系 （已解锁）
		- 蒸汽/化学系 （未解锁）
		- 一个便携式自动材料提取仪。
		- 1级铁匠技能，2级机械和电子技能。
		- 法术/科技法术：放电系 （未解锁）- 使用火焰和闪电
		- 法术/科技法术：寒岩系 （未解锁）- 使用土和水
		- 法术/科技法术：玄机系 （未解锁）- 使用时间和奥术
		- 你可以免费解锁三个科技法术系的其中之一。

		当你装备长袍的时候，奥术发电机会在你消耗法力值的时候自动产生蒸汽，并根据蒸汽等级提升法术强度。
		#{bold}#当你完成这职业进阶的时候，你应该尽快制造一个奥术发电机，装备在长袍中，以使用科技法术的力量。#{normal}#
```

## entry-03998
位置：tome-orcs.lua:6052；section：tome-orcs/data/talents/uber/str.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Earned the achievement 'Size Matters' on this character.
```
译文：
```text
当前角色解锁了“伤害很重要”成就。
```

## entry-03999
位置：tome-orcs.lua:6053；section：tome-orcs/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you deal a critical hit your embedded system activates, increasing all your primary stats except Strength by 50%% of your Strength for 6 turns.
```
译文：
```text
系统将会在你暴击时启动，在 6 回合内你的全属性（力量除外）将会增加等同于你 50%% 力量的值。
```

## entry-04000
位置：tome-orcs.lua:6060；section：tome-orcs/data/talents/uber/wil.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate a special focusing device that extends all your ranged spells and psionic powers range by 3 (only works on those with range 2 or more and up to 10 max).
		The use of this device is very strenuous, increasing fatigue by 20%% while active.
```
译文：
```text
启动一个特殊的聚焦装置来使你的所有远程魔法和精神技能射程延长 3 （仅对射程至少为 2 的技能生效，且上限为 10）。
		使用这个装置非常的费力，启动时会增加 20%% 疲劳。
```

## entry-04001
位置：tome-orcs.lua:6074；section：tome-orcs/data/timed_effects/floor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The target is warm from the campfire. Increasing steam regeneration by 6/turn, stun immunity by 30% and stamina regeneration by 4/turn.
```
译文：
```text
目标被营火温暖。蒸汽回复 +6，震慑免疫 +30%，体力回复 + 4。
```

## entry-04002
位置：tome-orcs.lua:6099；section：tome-orcs/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Twilit Echoes
```
译文：
```text
暮光回响
```

## entry-04003
位置：tome-orcs.lua:6103；section：tome-orcs/data/timed_effects/magical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The light damage the target has taken is echoed, slowing them by %d%%. Taking additional damage while Twilit Echoes is active will refresh and increase the slow up to a maximum of %d%%.
```
译文：
```text
目标受到的光系伤害回响了，减速 %d%%。在暮光回响期间受到更多伤害将会刷新持续时间并增加减速效果，最大叠加到 %d%%。
```

## entry-04004
位置：tome-orcs.lua:6110；section：tome-orcs/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Has summoned the starscape, slowing all creatures 67%.
```
译文：
```text
召唤星界，减速所有生物 67%。
```

## entry-04005
位置：tome-orcs.lua:6114；section：tome-orcs/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is overflowing with dark power!
```
译文：
```text
#Target# 充满了黑暗能量！
```

## entry-04006
位置：tome-orcs.lua:6121；section：tome-orcs/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is fluctuating in time!
```
译文：
```text
#Target# 在时光中波动！
```

## entry-04007
位置：tome-orcs.lua:6125；section：tome-orcs/data/timed_effects/magical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have %d charges.
```
译文：
```text
叠加次数：%d。
```

## entry-04008
位置：tome-orcs.lua:6167；section：tome-orcs/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A mind drone bores into #Target#!
```
译文：
```text
一个精神雄蜂飞入#Target#！
```

## entry-04009
位置：tome-orcs.lua:6177；section：tome-orcs/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# wakes up from the nightmare very confused!
```
译文：
```text
#Target#从噩梦中醒来，非常混乱！
```

## entry-04010
位置：tome-orcs.lua:6195；section：tome-orcs/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is cursed!
```
译文：
```text
#Target# 被诅咒了！
```

## entry-04011
位置：tome-orcs.lua:6196；section：tome-orcs/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is no longer cursed.
```
译文：
```text
#Target#不再被诅咒。
```

## entry-04012
位置：tome-orcs.lua:6227；section：tome-orcs/data/timed_effects/other.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Aiming!
```
译文：
```text
瞄准！
```

## entry-04013
位置：tome-orcs.lua:6245；section：tome-orcs/data/timed_effects/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target has been marked by a rocket pod, reducing defence by %d and negating all evasion effects.
```
译文：
```text
目标被火箭发射器锁定，降低闪避值 %d，且躲闪效果失效。
```

## entry-04014
位置：tome-orcs.lua:6269；section：tome-orcs/data/timed_effects/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target has been injected with chemicals, reducing all saves by %d.
```
译文：
```text
目标被化学药剂注射，降低所有豁免 %d。
```

## entry-04015
位置：tome-orcs.lua:6272；section：tome-orcs/data/timed_effects/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Engaged in automated repairs, preventing any action but increasing life regen by %d, all resistances by %d%% and preventing death until falling below -%d life.
```
译文：
```text
进入自动修复模式，无法行动，但生命恢复速率增加 %d，生命值回满时立即结束该模式，全部抗性提升 %d%%，死亡生命下限为 -%d。
```

## entry-04016
位置：tome-orcs.lua:6282；section：tome-orcs/data/timed_effects/other.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Rods available:

```
译文：
```text
可用放电柱：

```

## entry-04017
位置：tome-orcs.lua:6316；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Bullets shot are supercharged:  They can pass through multiple targets and have %d additional armour penetration.
```
译文：
```text
子弹处于超速状态：能够穿透多个目标，同时提高护甲穿透 %d 点。
```

## entry-04018
位置：tome-orcs.lua:6318；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Bullets shot are percussive:  When striking, they have a %d%% chance to knock back and a %d%% chance to stun.
```
译文：
```text
子弹处于冲击状态：%d%% 概率击退，%d%% 概率震慑。
```

## entry-04019
位置：tome-orcs.lua:6320；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Bullets shot are combustive:  When striking their target, they explode (radius 2) for %d fire damage.
```
译文：
```text
子弹处于爆炸状态：对 2 码范围内的敌人造成 %d 火焰伤害。
```

## entry-04020
位置：tome-orcs.lua:6336；section：tome-orcs/data/timed_effects/physical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# uses a pain suppressor salve.
```
译文：
```text
#Target# 使用了痛苦压制药剂。
```

## entry-04021
位置：tome-orcs.lua:6342；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Provides a frost aura, giving you +%d%% cold, nature and darkness affinity.
```
译文：
```text
提供寒霜光环，使你获得 +%d%% 寒冷、自然和暗影伤害亲和。
```

## entry-04022
位置：tome-orcs.lua:6348；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Provides a frost aura, giving you +%d%% fire, light, and lightning affinity.
```
译文：
```text
提供烈火光环，使你获得 +%d%% 火焰、光系和闪电伤害亲和。
```

## entry-04023
位置：tome-orcs.lua:6354；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Provides a frost aura, giving you +%d%% blight, mind and acid affinity.
```
译文：
```text
提供静水光环，使你获得 +%d%% 枯萎、精神和酸性伤害亲和。
```

## entry-04024
位置：tome-orcs.lua:6360；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases all saves by %d and healing factor by %d%%.
```
译文：
```text
增加全豁免 %d，增加治疗系数 %d%%  。
```

## entry-04025
位置：tome-orcs.lua:6385；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 for %0.2f physical damage (increasing) each turn
```
译文：
```text
 ，每回合受到 %0.2f 物理伤害（随回合递增）
```

## entry-04026
位置：tome-orcs.lua:6386；section：tome-orcs/data/timed_effects/physical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is #ORANGE#INFESTED#LAST# with ritch larvae!
```
译文：
```text
#Target# 被里奇幼虫#ORANGE#寄生#LAST#！
```

## entry-04027
位置：tome-orcs.lua:6389；section：tome-orcs/data/timed_effects/physical.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
A %s #ORANGE#BURSTS OUT#LAST# of %s%s!
```
译文：
```text
一个%s从%s体内#ORANGE#爆出#LAST#%s！
```

## entry-04028
位置：tome-orcs.lua:6404；section：tome-orcs/data/timed_effects/physical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The saw embedded in #Target# flies back its source.
```
译文：
```text
#Target#身上的链锯飞回主人的方向。
```

## entry-04029
位置：tome-orcs.lua:6406；section：tome-orcs/data/timed_effects/physical.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
The saw drags #Source# towards #Target#!
```
译文：
```text
链锯将#Source#拖向#Target#！
```

## entry-04030
位置：tome-orcs.lua:6429；section：tome-orcs/data/timed_effects/physical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have %d charges.
```
译文：
```text
叠加次数：%d。
```

## entry-04031
位置：tome-orcs.lua:6435；section：tome-orcs/data/timed_effects/physical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s blood turn into molten iron.
```
译文：
```text
#Target#的血液变成了融化的铁水。
```

## entry-04032
位置：tome-orcs.lua:6436；section：tome-orcs/data/timed_effects/physical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# no longer has molten iron blood.
```
译文：
```text
#Target#的血液不再是融化的铁水。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Twilit Echoes	暮光回响	T.GAME.TALENT	talents	talent name	preferred	dlc	Embers of Rage 黄昏系技能；光系伤害造成减速，暗影伤害生成可由后续伤害刷新的地块效果，统一重复运行时键及状态说明
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
chemistry	化学	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
galvanic	放电	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
galvanic technomancy	科技法术：放电	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mechanical	机械	T.GAME.ENTITY	creatures	entity type	existing	dlc	Embers of Rage 实体类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
occult technomancy	科技法术：玄机	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
physics	物理	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
schematic	配方	T.GAME.ENTITY	items	nil	preferred	dlc	Embers of Rage 工匠物学习配方；统一实体子类型、说明、学习日志和配方物品名，不使用孤立的“设计图”
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamtech	蒸汽科技	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
technomancy	科技法术	T.GAME.EFFECT	combat	effect subtype	existing	dlc	
terrene	寒岩	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage 的土与寒冷复合伤害类型；与“科技法术：寒岩”及技能描述统一，不按普通形容词直译
terrene technomancy	科技法术：寒岩	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
