# batch-075：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02389
位置：mod-tome.lua:30764；section：mod-tome/data/talents/techniques/reflexes.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You put all your focus into escaping combat for 4 turns. While under this effect you gain %d%% increased resistance to all damage, %0.1f increased stamina regeneration, immunity to stun, pin, daze and slowing effects and %d%% increased movement speed. 
Any action other than movement will cancel this effect.
```
译文：
```text
你专注逃跑 4 回合。处于此状态时增加 %d%% 所有伤害抗性，%0.1f 体力恢复，免疫震慑，定身，眩晕和减速效果并增加 %d%% 移动速度。
除移动外的任何行动将终止该效果。
```

## entry-02390
位置：mod-tome.lua:30799；section：mod-tome/data/talents/techniques/sling.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-02391
位置：mod-tome.lua:30811；section：mod-tome/data/talents/techniques/sniper.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You are being observed too closely to enter Concealment!
```
译文：
```text
你被近距离观察，不能进入 隐匿 状态！
```

## entry-02392
位置：mod-tome.lua:30812；section：mod-tome/data/talents/techniques/sniper.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enter a concealed sniping stance, increasing your weapon's attack range and vision range by %d, giving all incoming damage a %d%% chance to miss you, and causing your Headshot, Volley and Called Shots to behave as if the target was marked.
Any non-instant, non-movement action will break concealment, but the increased range and vision and damage avoidance will persist for 3 turns, with the damage avoidance decreasing in power by 33%% each turn.
This requires a bow to use, and cannot be used if there are foes in sight within range %d.
```
译文：
```text
进入隐匿的狙击状态，增加武器攻击范围和视野 %d 格，所有受到的伤害有 %d%% 几率被完全抵消，爆头、齐射和精巧射击视为目标已被标记。
所有非瞬时非移动行为将打破隐匿状态，攻击范围与视野的加成和伤害回避效果将额外持续 3 回合，伤害回避效果每回合减少 33%%。
该技能需要弓来使用；如果视野内 %d 格范围内有敌人，则不能使用。
```

## entry-02393
位置：mod-tome.lua:30818；section：mod-tome/data/talents/techniques/sniper.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire an arrow tipped with a smoke bomb inflicting %d%% damage and creating a radius %d cloud of thick, disorientating smoke. Those caught within will have their vision range reduced by %d for 5 turns.
The distraction caused by this effect reduces the cooldown of your Concealment by %d turns. If the cooldown is reduced to 0, you instantly activate Concealment regardless of whether foes are too close.
The chance for the smoke bomb to affect your targets increases with your Accuracy. This requires a bow to use.
```
译文：
```text
发射一个带着烟雾弹的箭头造成 %d%% 伤害并制造一个半径为 %d 的烟雾。被困在内的人将减少视野 %d 格 5 回合。
此效果将减少你隐匿技能 %d 回合冷却时间。如果冷却时间减到 0, 无论敌人是否太近，都可立即激活隐匿。
烟雾弹影响目标的几率受命中值加成。该技能需要弓来使用。
```

## entry-02394
位置：mod-tome.lua:30824；section：mod-tome/data/talents/techniques/sniper.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enter a calm, focused stance, increasing physical power and accuracy by %d, projectile speed by %d%% and the chance to mark targets by an additional %d%%.
This makes your shots more effective at range, increasing all damage dealt by %0.1f%% per tile travelled beyond 3, to a maximum of %0.1f%% damage at range 8.
The physical power and accuracy increase with your Dexterity. This requires a bow to use.
```
译文：
```text
进入一个平静，专注的姿态，增加 %d 物理强度和命中，抛射物速度增加 %d%% 并且标记目标的几率增加 %d%%。
这让你在射程内射击更有效：对三格外目标的距离每增加一格，伤害增加 %0.1f%%，8 格距离时达到最大值（%0.1f%%）。
物理强度和命中受敏捷值加成。该技能需要弓来使用。
```

## entry-02395
位置：mod-tome.lua:30830；section：mod-tome/data/talents/techniques/sniper.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Take aim for 1 turn, preparing a deadly shot. During the next turn, this talent will be replaced with the ability to fire a lethal shot dealing %d%% damage and marking the target.
While aiming, your intense focus causes you to shrug off %d%% incoming damage and all negative effects.
This requires a bow to use.
```
译文：
```text
瞄准 1 回合，准备射出致命的一箭。下回合，这个技能被替换成标记目标并造成 %d%% 伤害的致命攻击。
若你处于瞄准姿态，专注力让你无视受到的 %d%% 伤害和所有负面状态。
该技能需要弓来使用。
```

## entry-02396
位置：mod-tome.lua:30835；section：mod-tome/data/talents/techniques/sniper.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire a lethal shot. This shot will bypass other enemies between you and your target, and gains 100 increased accuracy.
```
译文：
```text
射出一发致命射击。这次射击将绕过你和你的目标之间的其他敌人，并提高 100 命中。
```

## entry-02397
位置：mod-tome.lua:30841；section：mod-tome/data/talents/techniques/strength-of-the-berserker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ uses Warsqueak.
```
译文：
```text
@Source@发出吱吱的战吼。
```

## entry-02398
位置：mod-tome.lua:30842；section：mod-tome/data/talents/techniques/strength-of-the-berserker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ uses Warshout.
```
译文：
```text
@Source@发出战吼。
```

## entry-02399
位置：mod-tome.lua:30844；section：mod-tome/data/talents/techniques/strength-of-the-berserker.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Shout your warcry in a frontal cone of radius %d. Any targets caught inside will be confused (50%% confusion power) for %d turns.
```
译文：
```text
在你的正前方大吼形成 %d 码半径的扇形战争怒吼。任何在其中的目标会被混乱（50%%强度）%d 回合。
```

## entry-02400
位置：mod-tome.lua:30848；section：mod-tome/data/talents/techniques/strength-of-the-berserker.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You enter an aggressive battle rage, increasing Accuracy by %d and Physical Power by %d and making you nearly unstoppable, granting %d%% stun and pinning resistance.
		Sustaining this rage takes its toll on your body, decreasing your life by 2%% each turn, but for every 1%% of life missing you gain 0.5%% critical hit chance.
		Even when sustained, this talent is only active when foes are in sight.
		The Accuracy bonus increases with your Dexterity, and the Physical Power bonus with your Strength.
```
译文：
```text
进入狂暴的战斗状态，增加 %d 点命中和 %d 点物理强度，增加 %d%% 震慑和定身抵抗。
		同时狂暴的力量会支配你的身体，每回合损失 2%% 生命。同时，你每失去 1%% 生命，增加 0.5%% 暴击率。
		该技能只在视野内有敌人时生效。
		命中受敏捷值加成；
		物理强度受力量值加成。
```

## entry-02401
位置：mod-tome.lua:30857；section：mod-tome/data/talents/techniques/strength-of-the-berserker.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s shatters %s shield!
```
译文：
```text
#CRIMSON#%s粉碎了%s的护盾！
```

## entry-02402
位置：mod-tome.lua:30866；section：mod-tome/data/talents/techniques/strength-of-the-berserker.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Search your inner strength for a surge of power.
		For %d turns you gain %d stamina per turn and %d%% movement and attack speed.
		Only usable at 30%% or lower stamina.
		Stamina regeneration is based on your Constitution stat.
```
译文：
```text
激发你内在的力量，持续 %d 回合。
		每回合恢复 %d 体力，同时增加 %d%% 移动速度和攻击速度。
		只能在体力不高于 30%% 时使用。
		体力回复受体质加成。
```

## entry-02403
位置：mod-tome.lua:30878；section：mod-tome/data/talents/techniques/superiority.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Concentrate on the battle, ignoring some of the damage you take.
		Improves physical damage reduction by %d%% and provides a %d%% chance to shrug off critical damage for 20 turns.
```
译文：
```text
专注于战斗，忽略你所受的部分伤害。
		增加物理伤害减免 %d%% 同时有 %d%% 几率摆脱暴击伤害，持续 20 回合。
```

## entry-02404
位置：mod-tome.lua:30882；section：mod-tome/data/talents/techniques/superiority.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Take an offensive stance. As you attack your foes, you knock your target and foes adjacent to them in a frontal arc back (up to %d grids).
		This consumes stamina rapidly (-1 stamina/turn).
```
译文：
```text
采取猛攻姿态。攻击敌人时，会将目标以及正面弧线内与其相邻的敌人击退（最多 %d 格）。
		这个姿态会快速减少体力值（-1 体力/回合）。
```

## entry-02405
位置：mod-tome.lua:30899；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Specialized two-handed techniques.
```
译文：
```text
使你精通于使用双手武器战斗技能。
```

## entry-02406
位置：mod-tome.lua:30905；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Specialized weapon and shield techniques.
```
译文：
```text
使你精通于使用单手武器加盾牌的战斗技能。
```

## entry-02407
位置：mod-tome.lua:30908；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Specialized dual wielding techniques.
```
译文：
```text
使你精通于同时使用两把单手武器的战斗技能。
```

## entry-02408
位置：mod-tome.lua:30911；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Ability to shoot.
```
译文：
```text
基础射击技能。
```

## entry-02409
位置：mod-tome.lua:30913；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Specialized bow techniques.
```
译文：
```text
提升使用弓的攻击效果。
```

## entry-02410
位置：mod-tome.lua:30915；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Specialized sling techniques.
```
译文：
```text
提升使用投石索的攻击效果。
```

## entry-02411
位置：mod-tome.lua:30917；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Generic archery techniques.
```
译文：
```text
通用射击技巧。
```

## entry-02412
位置：mod-tome.lua:30918；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：talent type；args_order：None；special：None

原文：
```text
archery prowess
```
译文：
```text
箭术造诣
```

## entry-02413
位置：mod-tome.lua:30921；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Specialized archery techniques that result from honed training.
```
译文：
```text
经过千锤百炼的箭术技巧。
```

## entry-02414
位置：mod-tome.lua:30923；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Advanced combat techniques.
```
译文：
```text
高阶战斗技巧。
```

## entry-02415
位置：mod-tome.lua:30925；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Advanced combat tactics.
```
译文：
```text
高阶战斗策略。
```

## entry-02416
位置：mod-tome.lua:30927；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Master the warcries to improve yourself and weaken others.
```
译文：
```text
提升战吼效果，强化你自身的能力或削弱敌人。
```

## entry-02417
位置：mod-tome.lua:30929；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Delight in the act of battle and the spilling of blood.
```
译文：
```text
你渴望鲜血并沉浸在战斗的狂热中。
```

## entry-02418
位置：mod-tome.lua:30931；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Control the battlefield using various techniques.
```
译文：
```text
运用各种技巧控制战场。
```

## entry-02419
位置：mod-tome.lua:30933；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Generic combat oriented techniques.
```
译文：
```text
通用格斗技巧。
```

## entry-02420
位置：mod-tome.lua:30936；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Teaches to use various armours, weapons and improves health.
```
译文：
```text
使你学会使用不同的护甲和武器，并提升血量。
```

## entry-02421
位置：mod-tome.lua:30938；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The blending together of magic and melee prowess.
```
译文：
```text
结合魔法和近身格斗的技巧。
```

## entry-02422
位置：mod-tome.lua:30940；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Training and techniques to improve mobility and evade your enemies.  On the battlefield, positioning is paramount.
```
译文：
```text
强化闪避和移动能力，确保你始终处于战斗的上风。
```

## entry-02423
位置：mod-tome.lua:30946；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Master the art of throwing knives to fight from a distance.
```
译文：
```text
掌握飞刀投掷的技艺，以远距离作战。
```

## entry-02424
位置：mod-tome.lua:30950；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Training in the use of bows and slings.
```
译文：
```text
训练使用弓箭和投石索的技术。
```

## entry-02425
位置：mod-tome.lua:30968；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Unarmed Boxing techniques that may not be practiced in massive armor or while a weapon or shield is equipped.
```
译文：
```text
徒手拳击格斗技术，你不能装备板甲、武器和盾牌。
```

## entry-02426
位置：mod-tome.lua:30970；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Finishing moves that use combo points and may not be practiced in massive armor or while a weapon or shield is equipped.
```
译文：
```text
使用你累积的连击点数发动致命的终结一击，你不能装备板甲、武器和盾牌。
```

## entry-02427
位置：mod-tome.lua:30972；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Grappling techniques that may not be practiced in massive armor or while a weapon or shield is equipped.
```
译文：
```text
抓取敌人的技巧，你不能装备板甲、武器和盾牌。
```

## entry-02428
位置：mod-tome.lua:30976；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Teaches various martial arts techniques that may not be practiced in massive armor or while a weapon or shield is equipped.
```
译文：
```text
高级徒手格斗技能，不能装备板甲、武器和盾牌。
```

## 相关术语快照
```tsv
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Cancel	取消	T.UI.LABEL	ui	_t	preferred	global	通用界面按钮（42 处）；对话框/菜单取消操作
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Warshout	战争怒吼	T.GAME.TALENT	talents	talent name	existing	core	
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
armours	护甲	T.GAME.ENTITY	items	nil	existing	core	复数实体类别
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
throwing knives	飞刀	T.GAME.ENTITY	items	talent type	preferred	core	灵巧系远程投掷武器类别；在技能说明中与普通匕首 knives 并列
throwing knives	飞刀	T.GAME.ENTITY	items	tformat	preferred	core	技能机制说明中的投掷匕首；沿用飞刀类别名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
