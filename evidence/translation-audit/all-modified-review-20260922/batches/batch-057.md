# batch-057：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01666
位置：mod-tome.lua:22969；section：mod-tome/data/talents/corruptions/scourge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Corrupt the target reducing disease immunity by 100%% for 2 turns and stripping up to 2 nature sustains then strike with both your weapons dealing %d%% damage.
```
译文：
```text
腐化目标，2 回合内降低其 100%% 的疾病免疫，并最多去除其 2 个自然持续效果。然后用你的两把武器打击敌人，造成 %d%% 伤害。
```

## entry-01667
位置：mod-tome.lua:22982；section：mod-tome/data/talents/corruptions/shadowflame.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures up a bolt of shadowflame that moves toward the target and explodes into a flash of darkness and fire, doing %0.2f fire damage and %0.2f darkness damage in a radius of %d.
		The damage will increase with your Spellpower.
```
译文：
```text
向目标发射一团黑暗之炎，产生爆炸并造成 %0.2f 火焰伤害和 %0.2f 暗影伤害（%d 码半径范围内）。
		伤害受法术强度加成。
```

## entry-01668
位置：mod-tome.lua:22986；section：mod-tome/data/talents/corruptions/shadowflame.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Call upon the essence of the supreme demon overlord Urh'Rok to turn into a demon.
		While in demon form, you gain %d%% fire resistance, %d%% darkness resistance, and your global speed is increased by %d%%.
		The flames of the Fearscape will heal you while in demon form.
		The resistances and heal will increase with your Spellpower.
```
译文：
```text
召唤至高恶魔领主乌鲁洛克的本质之力，转化为恶魔。
		当你处于恶魔形态时，你增加 %d%% 火焰抗性，%d%% 暗影抗性并且全局速度提升 %d%%。
		当你处于恶魔形态时，恶魔空间的火焰会治疗你。
		抗性和治疗量受法术强度加成。
```

## entry-01669
位置：mod-tome.lua:22996；section：mod-tome/data/talents/corruptions/shadowflame.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The spell fizzles...
```
译文：
```text
法术失败了……
```

## entry-01670
位置：mod-tome.lua:23021；section：mod-tome/data/talents/corruptions/torment.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reach out and touch the blood and health of your foes. Any creatures caught in the radius 2 ball will be unable to heal above their current life value (at the time of the casting) for %d turns.
```
译文：
```text
掌控敌人的血液和肉体。在 2 码范围内，任何被鲜血禁锢攻击到的敌人的治疗或回复将不能超过施法瞬间锁定的生命值，持续 %d 回合。
```

## entry-01671
位置：mod-tome.lua:23028；section：mod-tome/data/talents/corruptions/torment.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#RED#The powerful blow energizes %s reducing their cooldowns!#LAST#
```
译文：
```text
#RED#强大的攻击使 %s 获得能量，技能冷却时间缩短了！#LAST#
```

## entry-01672
位置：mod-tome.lua:23068；section：mod-tome/data/talents/corruptions/vile-life.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#CRIMSON##Source# transfers an effect (%s) to #Target#!
```
译文：
```text
#CRIMSON##Source#将一项效果(%s)转移至#Target#！
```

## entry-01673
位置：mod-tome.lua:23108；section：mod-tome/data/talents/cunning/ambush.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the disarm!
```
译文：
```text
%s抵抗了缴械！
```

## entry-01674
位置：mod-tome.lua:23116；section：mod-tome/data/talents/cunning/ambush.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mastery of dark magic empowers you.
		You gain %d Accuracy, %d Defense, and %d%% Darkness damage penetration.
		The effects will increase with your Spellpower stat.
```
译文：
```text
你对暗影魔法的掌握使你更加强大。
		获得 %d 命中，%d 闪避，%d%% 暗影伤害抗性穿透。
		加成效果受法术强度影响。
```

## entry-01675
位置：mod-tome.lua:23139；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#YELLOW#%s (prepared, level %s)#LAST#:

```
译文：
```text
#YELLOW#%s (已准备，等级 %s)#LAST#:

```

## entry-01676
位置：mod-tome.lua:23142；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GREY#(see talent description)#LAST#

```
译文：
```text
#GREY#（查看技能介绍）#LAST#

```

## entry-01677
位置：mod-tome.lua:23156；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Cunning Tools
```
译文：
```text
机巧工具
```

## entry-01678
位置：mod-tome.lua:23168；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Intricate Tools
```
译文：
```text
精密工具
```

## entry-01679
位置：mod-tome.lua:23180；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Master Artificer
```
译文：
```text
诡计大师
```

## entry-01680
位置：mod-tome.lua:23182；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You become a master of your craft, allowing you to focus on a single tool (#YELLOW#currently %s#LAST#) to greatly improve its capabilities:

%s
The effects depend on this talent's level.
Mastering a new tool places it (and its special effects, as appropriate) on cooldown.
```
译文：
```text
你成为工具大师，能集中强化一件工具 (#YELLOW#当前选择 %s#LAST#) 来改善其性能：

%s
效果取决于技能等级。
掌握一件新工具会使该工具（及其相应的特殊效果）进入冷却。
```

## entry-01681
位置：mod-tome.lua:23192；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# strikes #target# with hidden blades!
```
译文：
```text
#Source#使用隐藏的刀片击中了#target#！
```

## entry-01682
位置：mod-tome.lua:23193；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Melee criticals trigger an extra unarmed attack, inflicting %d%% damage. 4 turn cooldown.
```
译文：
```text
近战暴击触发额外 %d%% 伤害徒手攻击，4 回合冷却。
```

## entry-01683
位置：mod-tome.lua:23194；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：_t；args_order：None；special：None

原文：
```text
not prepared
```
译文：
```text
未装备
```

## entry-01684
位置：mod-tome.lua:23195；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You conceal spring loaded blades within your equipment. On scoring a critical strike, you follow up with your blades for %d%% damage (as an unarmed attack).
This talent has a cooldown.
#YELLOW#Prepared with: %s#LAST#
```
译文：
```text
你将刀片隐藏在装备中，当你造成暴击时，刀片自动弹出，造成 %d%% 徒手武器伤害。
该技能有冷却时间。
#YELLOW#准备于：%s#LAST#
```

## entry-01685
位置：mod-tome.lua:23202；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# strikes at a vital spot on #target#!
```
译文：
```text
#Source#攻向#target#的要害！
```

## entry-01686
位置：mod-tome.lua:23209；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Prepare a potion that restores %d life, %d stamina, and cures %d negative physical effects. 20 turn cooldown.
```
译文：
```text
准备药剂，回复 %d 生命，%d 体力，解除 %d 项物理负面状态。20 回合冷却。
```

## entry-01687
位置：mod-tome.lua:23210；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Imbibe a potent mixture of energizing and restorative substances, restoring %d life, %d stamina and curing %d detrimental physical effects.  The restorative effects improve with your Cunning.
	#YELLOW#Prepared with: %s#LAST#
```
译文：
```text
饮用强效恢复药酒，使用后回复 %d 生命、%d 体力并解除 %d 项物理负面效果。该效果受灵巧加成。
	#YELLOW#准备于：%s#LAST#
```

## entry-01688
位置：mod-tome.lua:23217；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a smokebomb creating a radius 2 cloud of smoke, lasting %d turns, that blocks sight and reduces enemies' vision by %d. 15 turn cooldown.
```
译文：
```text
投掷一枚烟雾弹，生成半径 2 的烟云，持续 %d 回合，阻挡视线并使敌人视野降低 %d。15 回合冷却。
```

## entry-01689
位置：mod-tome.lua:23218；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a vial of volatile liquid that explodes in a radius %d cloud of smoke lasting %d turns.  The smoke blocks line of sight, and enemies within will have their vision range reduced by %d.
		Use of this talent will not break stealth, and creatures affected by the smokes can never prevent you from activating stealth, even if their proximity would normally forbid it.
		#YELLOW#Prepared with: %s#LAST#
```
译文：
```text
扔出烟雾弹，产生半径 %d 的烟雾，持续 %d 回合。烟雾阻挡视野，所有烟雾中的敌人视野下降 %d。
		使用该技能不解除潜行。被烟雾影响的生物不能阻止你潜行。
		#YELLOW#准备于：%s#LAST#
```

## entry-01690
位置：mod-tome.lua:23223；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Smokescreen Mastery
```
译文：
```text
烟雾弹精通
```

## entry-01691
位置：mod-tome.lua:23227；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the sedation!
```
译文：
```text
%s抵抗了睡眠！
```

## entry-01692
位置：mod-tome.lua:23229；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire a poisoned dart from a silent, concealed launcher on your person that deals %0.2f physical damage and puts the target (living only) to sleep for 4 turns, rendering them unable to act. Every %d points of damage the target takes brings it closer to waking by 1 turn.
This can be used without breaking stealth.
#YELLOW#Prepared with: %s#LAST#
```
译文：
```text
从身上隐蔽的无声发射器中射出毒镖，造成 %0.2f 物理伤害，并使目标（仅限活物）沉睡 4 回合，期间无法行动。目标每受到 %d 点伤害，距离苏醒便提前 1 回合。
使用该技能不解除潜行。
#YELLOW#准备于：%s#LAST#
```

## entry-01693
位置：mod-tome.lua:23235；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your darts ignore poison and sleep immunity and waking targets are slowed by %d%% for 4 turns.
```
译文：
```text
你的飞镖无视中毒免疫和睡眠免疫，且使目标醒来后减速 %d%% 4 回合。
```

## entry-01694
位置：mod-tome.lua:23236；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The sleeping poison of your Dart Launcher becomes potent enough to ignore immunity, and upon waking the target is slowed by %d%% for 4 turns.
```
译文：
```text
你的飞镖发射器的睡眠毒素强效到足以无视免疫，且使目标醒来后减速 %d%% 4 回合。
```

## entry-01695
位置：mod-tome.lua:23239；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot move!
```
译文：
```text
你无法移动！
```

## entry-01696
位置：mod-tome.lua:23240；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# throws a grappling hook at #target#!
```
译文：
```text
#Source#朝#target#扔出钩爪！
```

## entry-01697
位置：mod-tome.lua:23241；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source#'s grappling hook latches onto #target#!
```
译文：
```text
#Source#的钩爪命中了#target#！
```

## entry-01698
位置：mod-tome.lua:23242；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# is dragged towards #target#!
```
译文：
```text
#Source#被拉向#target#！
```

## entry-01699
位置：mod-tome.lua:23243；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Target# is dragged towards #source#!
```
译文：
```text
#Target#被拉向#source#！
```

## entry-01700
位置：mod-tome.lua:23246；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s uses a grappling hook to pull %s %s!
```
译文：
```text
%s使用钩爪来拉动%s向%s！
```

## entry-01701
位置：mod-tome.lua:23247；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must anchor the hook to something solid.
```
译文：
```text
你需要将钩爪固定在某个坚固的物体上。
```

## entry-01702
位置：mod-tome.lua:23249；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Toss out a grappling hook to a target within range %d.  If this strikes either a wall or a creature that is immovable or larger than you, you will pull yourself towards it, otherwise, you will drag the target towards you.  Creatures struck by the hook will be pinned for 2 turns.
		Your grapple target must be at least 2 tiles from you.
#YELLOW#Prepared with: %s#LAST#
```
译文：
```text
朝 %d 格范围内的目标发射钩爪，如果目标是墙壁、目标不能移动或目标体型比你大，你将被拉过去，否则将目标拉过来。之后，目标将被定身 2 回合。
		钩爪至少要发射到两格外。
#YELLOW#准备于：%s#LAST#
```

## entry-01703
位置：mod-tome.lua:23255；section：mod-tome/data/talents/cunning/artifice.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your grappling hook deals %d%% unarmed damage when it hits, plus a further %0.2f physical and %0.2f nature damage over 4 turns.
```
译文：
```text
被钩爪击中的生物受到 %d%% 徒手伤害，在 4 回合内受到 %0.2f 流血伤害和 %0.2f 自然毒素伤害。
```

## entry-01704
位置：mod-tome.lua:23280；section：mod-tome/data/talents/cunning/called-shots.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Employ a specialized sniping shot at a target.
		This shot is focused on precision at long range and deals base %d%% ranged damage with a bonus that increases with distance.
		The ranged bonus is %d%% (penalty) at point blank range, while at your maximum range of %d it is %d%%.
		This shot will bypass other enemies between you and your target.
```
译文：
```text
对敌人进行一次特殊的射击。
		这个技能专注于精准的远程狙击，造成 %d%% 的基础远程伤害以及受距离加成的额外伤害。
		在零距离，伤害加成（惩罚）为 %d%%，在最大射程（%d 格），伤害加成为 %d%%。
		这个射击将会穿过你和目标间的其他敌人。
```

## entry-01705
位置：mod-tome.lua:23288；section：mod-tome/data/talents/cunning/called-shots.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning shot!
```
译文：
```text
%s抵抗了震慑！
```

## 相关术语快照
```tsv
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fearscape	恶魔空间	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
potion	药水	T.GAME.ENTITY	items	entity type	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
