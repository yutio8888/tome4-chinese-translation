# batch-065：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01988
位置：mod-tome.lua:25973；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the infusion to endure even the most grievous of wounds for %d turns.
		While Heroism is active, you will only die when reaching -%d life.
		The duration and life will increase by 1%% for every 1%% life you have lost (currently %d life, %d duration)
		If your life is below 0 when this effect wears off it will be set to 1.
```
译文：
```text
激活这个纹身可以让你忍受致死的伤害，持续 %d 回合。
		当英勇纹身激活时，你的生命值只有在降低到 -%d 生命时才会死亡。
		你每失去 1%% 生命值，持续时间和生命值下限就会增加 1%%。
		（目前 %d 生命值，%d 持续时间）
		效果结束时，如果你的生命值在 0 以下，会变为 1 点。
```

## entry-01989
位置：mod-tome.lua:25981；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
die at -%d; dur %d; cd %d
```
译文：
```text
-%d 死亡底线；持续 %d; 冷却 %d
```

## entry-01990
位置：mod-tome.lua:25997；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the rune to direct a cone of chilling stormwind doing %0.2f cold damage.
			The storm will soak enemies hit reducing their resistance to stuns by 50%% then attempt to freeze them for %d turns.
			These effects can be resisted but not saved against.
```
译文：
```text
激活这个符文，形成一股锥形寒风，造成 %0.2f 寒冷伤害。
			寒风会浸湿被击中的敌人，使其震慑抗性降低 50%%，并试图冻结他们 %d 回合。
			效果可以被抵抗，但不能被豁免。
```

## entry-01991
位置：mod-tome.lua:26015；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
regen %d%% over %d turns; mana %d; cd %d
```
译文：
```text
法力回复 +%d%%，持续 %d 回合；瞬回 %d 法力；冷却 %d
```

## entry-01992
位置：mod-tome.lua:26017；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is immune!
```
译文：
```text
%s 免疫了！
```

## entry-01993
位置：mod-tome.lua:26019；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Something has prevented the timetravel.
```
译文：
```text
某物阻止了时空旅行。
```

## entry-01994
位置：mod-tome.lua:26029；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the rune to teleport up to %d spaces within line of sight.  Afterwards you stay out of phase for %d turns. In this state all new negative status effects duration is reduced by %d%%, your defense is increased by %d and all your resistances by %d%%.
```
译文：
```text
激活符文，传送到视野内 %d 格内的指定位置。之后，你会脱离相位 %d 回合。在这种状态下，所有新的负面效果的持续时间减少 %d%%，你的闪避增加 %d，你的全体伤害抗性增加 %d%%。
```

## entry-01995
位置：mod-tome.lua:26032；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the rune to become ethereal for %d turns.
		While ethereal all damage you deal is reduced by %d%%, you gain %d%% all resistance, you move %d%% faster, and you are invisible (power %d).
```
译文：
```text
启动符文，使你变得虚幻，持续 %d 回合。
		在虚幻状态下，你造成的伤害减少 %d%%，你获得 %d%% 全体伤害抗性，你的移动速度提升 %d%%，你获得隐形 (强度 %d)。
```

## entry-01996
位置：mod-tome.lua:26043；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%d turns; %s
```
译文：
```text
%d 回合；%s
```

## entry-01997
位置：mod-tome.lua:26084；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Strip the protective barriers from your mind for %d turns, allowing in the thoughts all creatures within %d squares but reducing mind save by %d and increasing your mindpower by %d for 10 turns.
```
译文：
```text
卸除你心灵上的防护屏障 %d 回合，感应 %d 格范围内所有生物的思维；精神豁免降低 %d，精神强度提高 %d，持续 10 回合。
```

## entry-01998
位置：mod-tome.lua:26100；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：[1, 2, 3, 4, 5]；special：None

原文：
```text
Activate the rune to get a vision of the area surrounding you (%d radius) and to allow you to see invisible and stealthed creatures (power %d) for %d turns.
		Your mind will become more receptive for %d turns, allowing you to sense any %s around.
```
译文：
```text
激活这个符文可以使你查看周围环境（%d 有效范围），使你能看到隐身和潜行生物（%d 强度），持续 %d 回合。
		你的精神会变得更加敏锐 %d 回合，让你能感知到周围的任何 %s。
```

## entry-01999
位置：mod-tome.lua:26124；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the rune to become invisible (power %d) for %d turns.
		As you become invisible you fade out of phase with reality, all your damage is reduced by 40%%.
		
```
译文：
```text
激活这个符文使你变得隐形（%d 隐形等级）持续 %d 回合。
		由于你的隐形使你从现实相位中脱离，你造成的所有伤害降低 40%%。
		
```

## entry-02000
位置：mod-tome.lua:26137；section：mod-tome/data/talents/misc/inscriptions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the infusion to endure even the most grievous of wounds for %d turns.
		While Heroism is active, you will only die when reaching -%d life.
		The duration and life will increase by 1%% for every 1%% life you have lost, to a maximum of 100%% at 0 life or less (currently %d life, %d duration)
		If your life is below 0 when this effect wears off it will be set to 1.
```
译文：
```text
激活这个纹身可以让你忍受致死的伤害，持续 %d 回合。
		当英勇纹身激活时，你的生命值只有在降低到 -%d 生命时才会死亡。
		你每失去 1%% 生命值，持续时间和生命值下限就会增加 1%%，在生命值降至 0 或更低时最多提高 100%%。
		（目前 %d 生命值，%d 持续时间）
		效果结束时，如果你的生命值在 0 以下，会变为 1 点。
```

## entry-02001
位置：mod-tome.lua:26159；section：mod-tome/data/talents/misc/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Taints are not class abilities, you must find them or learn them from other people.
```
译文：
```text
污印不是职业技能，你必须找到它们或从其他人那获得它们。
```

## entry-02002
位置：mod-tome.lua:26182；section：mod-tome/data/talents/misc/misc.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The spell fizzles...
```
译文：
```text
法术失败了……
```

## entry-02003
位置：mod-tome.lua:26200；section：mod-tome/data/talents/misc/misc.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s: Reducing duration of %s, using %s, by %d
```
译文：
```text
%s: 减少%s持续时间，依据%s减少%d回合
```

## entry-02004
位置：mod-tome.lua:26213；section：mod-tome/data/talents/misc/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Use the onboard short-range teleport of the Fortress to beam down to the surface.
	Requires being in flight above the ground of a planet.
```
译文：
```text
使用堡垒自带的短程传送装置“哔”的一下回到地面。
	需要在某个星球的空中飞行。
```

## entry-02005
位置：mod-tome.lua:26216；section：mod-tome/data/talents/misc/misc.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Fire a blast of energy
```
译文：
```text
发射能量冲击
```

## entry-02006
位置：mod-tome.lua:26217；section：mod-tome/data/talents/misc/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Use 10 Fortress energy to send a powerful blast to the ground, directly below the Fortress, heavily damaging any creatures caught inside.
	Requires being in flight above the ground of a planet.
```
译文：
```text
消耗 10 点堡垒能量，向堡垒正下方的地面发出一道强力冲击，重创位于其中的任何生物。
	需要在某个星球的空中飞行。
```

## entry-02007
位置：mod-tome.lua:26244；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Multiply yourself! (up to %d times)
```
译文：
```text
复制你自身！(最多 %d 次)
```

## entry-02008
位置：mod-tome.lua:26259；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning blow!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-02009
位置：mod-tome.lua:26273；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target with your weapon doing %d%% damage. If the attack hits, the target is knocked back up to 4 grids.  The chance improves with your Physical Power.
```
译文：
```text
使用武器打击目标造成 %d%% 伤害，如果攻击命中则可击退目标至多 4 格。击退几率受物理强度加成。
```

## entry-02010
位置：mod-tome.lua:26279；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-02011
位置：mod-tome.lua:26280；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# summons #Target#!
```
译文：
```text
#Source#召唤了#Target#！
```

## entry-02012
位置：mod-tome.lua:26285；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target doing %d%% damage. If the attack hits, the target is afflicted with a disease, inflicting %0.2f blight damage per turn for %d turns and reducing constitution by 10%% + 4.  The disease damage increases with your Strength, and the chance to apply it increases with your Physical Power.
```
译文：
```text
打击目标造成 %d%% 伤害，如果攻击命中可使目标感染疾病，造成每回合 %0.2f 枯萎伤害持续 %d 回合并降低其体质 10%%+4。疾病伤害受力量加成，附加几率受物理强度加成。
```

## entry-02013
位置：mod-tome.lua:26287；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target doing %d%% damage. If the attack hits, the target is afflicted with a disease, inflicting %0.2f blight damage per turn for %d turns and reducing dexterity by 10%% + 4.  The disease damage increases with your Strength, and the chance to apply it increases with your Physical Power.
```
译文：
```text
打击目标造成 %d%% 伤害，如果攻击命中可使目标感染疾病，造成每回合 %0.2f 枯萎伤害持续 %d 回合并降低其敏捷 10%%+4。疾病伤害受力量加成，附加几率受物理强度加成。
```

## entry-02014
位置：mod-tome.lua:26289；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target doing %d%% damage. If the attack hits, the target is afflicted with a disease, inflicting %0.2f blight damage per turn for %d turns and reducing strength by 10%% + 4.  The disease damage increases with your Strength, and the chance to apply it increases with your Physical Power.
```
译文：
```text
打击目标造成 %d%% 伤害，如果攻击命中可使目标感染疾病，造成每回合 %0.2f 枯萎伤害持续 %d 回合并降低其力量 10%%+4。疾病伤害受力量加成，附加几率受物理强度加成。
```

## entry-02015
位置：mod-tome.lua:26343；section：mod-tome/data/talents/misc/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ rushes out, claws sharp and ready!
```
译文：
```text
@Source@冲了出去，用尖利的爪子攻击！
```

## entry-02016
位置：mod-tome.lua:26356；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Pins non spiderkin for %d turns. Decays over time.
```
译文：
```text
定身所有非蜘蛛族 %d 回合。会随时间消失。
```

## entry-02017
位置：mod-tome.lua:26363；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# hurls a huge boulder at #target#!
```
译文：
```text
#Source#朝#target#投掷巨石！
```

## entry-02018
位置：mod-tome.lua:26375；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the crushing!
```
译文：
```text
%s抵抗了压碎！
```

## entry-02019
位置：mod-tome.lua:26395；section：mod-tome/data/talents/misc/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ explodes! @target@ is enveloped in searing light.
```
译文：
```text
@Source@爆炸了！@target@ 被灼热的光线覆盖了。
```

## entry-02020
位置：mod-tome.lua:26398；section：mod-tome/data/talents/misc/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ explodes! @target@ is enveloped in frost.
```
译文：
```text
@Source@爆炸了！@target@被冰霜覆盖了。
```

## entry-02021
位置：mod-tome.lua:26401；section：mod-tome/data/talents/misc/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ casts Elemental Bolt!
```
译文：
```text
@Source@释放了元素弹！
```

## entry-02022
位置：mod-tome.lua:26417；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Start to sever the lifeline of the target. After 4 turns, if the target is still in line of sight of you, its existance will be ended (%d temporal damage).
```
译文：
```text
引导法术离断目标的生命线，如果 4 回合之后目标仍然在视线内则会立即死亡(%d 时空伤害)。
```

## entry-02023
位置：mod-tome.lua:26441；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Engulfs your hands (and weapons) in a sheath of frost, dealing %0.2f cold damage per melee attack and increasing all cold damage by %d%%.
		The effects will increase with your Spellpower.
```
译文：
```text
将你的双手（及武器）笼罩在寒冰之中，每次近战攻击造成 %0.2f 冰冷伤害，并提高 %d%% 冰冷伤害。
		效果受法术强度加成。
```

## entry-02024
位置：mod-tome.lua:26456；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Calls forth a powerful beam of lightning doing %0.2f to %0.2f lightning damage (%0.2f average).
		The damage will increase with your Mindpower.
```
译文：
```text
召唤一股强烈的闪电束造成 %0.2f 至 %0.2f 伤害（平均 %0.2f）。
		伤害受精神强度加成。
```

## entry-02025
位置：mod-tome.lua:26476；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A punch to the body that deals %d%% damage, drains %d of the target's stamina per combo point, and dazes the target for %d to %d turns, depending on the amount of combo points you've accumulated.
		The daze chance will increase with your Physical Power.
		Using this talent removes your combo points.
```
译文：
```text
对目标的身体发出强烈的一击，造成 %d%% 伤害，每点连击点消耗 %d 目标体力并眩晕目标 %d 到 %d 回合（由你的连击点数决定）。
		眩晕概率受物理强度加成
		使用此技能会消耗当前所有连击点。
```

## entry-02026
位置：mod-tome.lua:26482；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When gaining a combo point, you have a %d%% chance to gain an extra combo point.  Additionally, your combo points will last %d turns longer before expiring.
		The chance of building a second combo point will improve with your Cunning.
```
译文：
```text
当获得 1 个连击点时有 %d%% 概率
		额外获得 1 个连击点。
		此外你的连击点持续时间会延长 %d 回合。
		额外连击点获得概率受灵巧加成。
```

## entry-02027
位置：mod-tome.lua:26488；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Superior cunning and training allows you to outthink and outwit your opponents' physical and mental assaults.  Increases Defense by %d and Mental Save by %d.
		The Defense bonus will scale with your Dexterity, and the save bonus with your Cunning.
```
译文：
```text
大量的训练使你能保持清醒的头脑，增加 %d 近身闪避和 %d 精神豁免。
		受敏捷影响，闪避按比例加成；
		受灵巧影响，精神豁免按比例加成。
```

## 相关术语快照
```tsv
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Out of Phase	脱离现实	T.GAME.EFFECT	combat	_t	preferred	core	传送后获得的相位状态名；统一沿用效果定义，不泛化为“传送后加成”
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
taints	污印	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	堕落系技能类型
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
