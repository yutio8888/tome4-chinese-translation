# batch-054：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01545
位置：mod-tome.lua:21655；section：mod-tome/data/talents/chronomancy/anomalies.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-01546
位置：mod-tome.lua:21656；section：mod-tome/data/talents/chronomancy/anomalies.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You swap locations with a random target.
```
译文：
```text
你和一个随机目标交换位置。
```

## entry-01547
位置：mod-tome.lua:21659；section：mod-tome/data/talents/chronomancy/anomalies.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
50%% chance that damage the caster takes will be warped to a set target.
		Once the maximum damage (%d) is absorbed, the time runs out, or the target dies, the shield will crumble.
```
译文：
```text
施法者所承受的伤害有 50%% 的概率转移给指定连接的目标。
		一旦吸收伤害达到上限（%d），持续时间到了或目标死亡，护盾会破碎掉。
```

## entry-01548
位置：mod-tome.lua:21679；section：mod-tome/data/talents/chronomancy/anomalies.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01549
位置：mod-tome.lua:21728；section：mod-tome/data/talents/chronomancy/anomalies.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Places between three and six talents of up to 5 targets in a radius %d ball on cooldown for up to %d turns.
```
译文：
```text
让半径 %d 范围内最多五个单位的三到六个技能进入最多 %d 回合的冷却。
```

## entry-01550
位置：mod-tome.lua:21771；section：mod-tome/data/talents/chronomancy/anomalies.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summons three to six tornados.
```
译文：
```text
召唤三到六道龙卷风。
```

## entry-01551
位置：mod-tome.lua:21790；section：mod-tome/data/talents/chronomancy/blade-threading.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Attack with your melee weapons for %d%% weapon damage as physical and temporal (warp) damage. If either attack hits you may stun, blind, pin, or confuse the target for %d turns.
		
		Blade Threading talents will freely swap to your dual-weapons when activated if you have them in your secondary slots.  Additionally you may use the Attack talent in a similar manner.
```
译文：
```text
使用近战武器攻击目标，造成 %d%% 物理和时空（扭曲）属性的武器伤害。如果任意一次攻击命中，你可以使目标震慑、致盲、定身或混乱 %d 回合。

		激活螺旋灵刃系技能时，如果副武器栏位中有双持武器，便会自动切换至它们。普通攻击技能也能以同样方式切换。
```

## entry-01552
位置：mod-tome.lua:21796；section：mod-tome/data/talents/chronomancy/blade-threading.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-01553
位置：mod-tome.lua:21802；section：mod-tome/data/talents/chronomancy/blade-threading.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the temporal shear!
```
译文：
```text
%s 抵挡了时空切变！
```

## entry-01554
位置：mod-tome.lua:21815；section：mod-tome/data/talents/chronomancy/bow-threading.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire an arrow for %d%% weapon damage and call up to 2 wardens, depending on available space, that will each fire a single arrow before returning to their timelines.
		The wardens are out of phase with normal reality and deal %d%% less damage but shoot through friendly targets. All your arrows, including arrows from Shoot and other talents, now phase through friendly targets without causing them harm.
		
		Bow Threading talents will freely swap to your bow when activated if you have one in your secondary slot. You may use the Shoot talent in a similar manner.
```
译文：
```text
发射一支灵矢造成 %d%% 武器伤害，并且根据可用空间，召唤最多两个守卫，各自发射一枚灵矢然后回到他们自己的时间线中。
		守卫处在现实位面之外，灵矢的伤害减少 %d%%，但能够穿过友好目标。同时，你发射的所有来自射击或者其他技能的箭矢，都可以穿透友军并且不会造成伤害。

		激活螺旋灵弓技能可以自由切换到你的弓（必须装备在副武器栏位上）。此外，当你使用远程攻击时也会触发这个效果。
```

## entry-01555
位置：mod-tome.lua:21833；section：mod-tome/data/talents/chronomancy/bow-threading.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-01556
位置：mod-tome.lua:21877；section：mod-tome/data/talents/chronomancy/chronomancer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Manipulate raw energy by addition or subtraction.
```
译文：
```text
通过增加或减少来操纵原始能量。
```

## entry-01557
位置：mod-tome.lua:21879；section：mod-tome/data/talents/chronomancy/chronomancer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weave the threads of fate.
```
译文：
```text
编织你的命运。
```

## entry-01558
位置：mod-tome.lua:21881；section：mod-tome/data/talents/chronomancy/chronomancer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weave the threads of spacetime.
```
译文：
```text
编织时空线。
```

## entry-01559
位置：mod-tome.lua:21900；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You peer into the future, sensing creatures and traps in a radius of %d for %d turns.
		If you know Foresight you'll gain additional defense and chance to shrug off critical hits (equal to your Foresight bonuses) while Precognition is active.
```
译文：
```text
你预知未来，感知半径 %d 以内的生物和陷阱，持续 %d 回合。
		如果你学会了深谋远虑，那么在你激活这个技能的时候，你可以获得额外的闪避和无视暴击伤害几率（数值等于深谋远虑的奖励）。
```

## entry-01560
位置：mod-tome.lua:21904；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Gain %d defense and %d%% chance to shrug off critical hits.
		If you have Precognition or See the Threads active these bonuses will be added to those effects, granting additional defense and chance to shrug off critical hits.
		These bonuses scale with your Magic stat.
```
译文：
```text
获得 %d 闪避和 %d%% 几率无视暴击伤害。
		如果你激活了预知未来或者命运螺旋，那么这些技能也会拥有同样的加成，使你获得额外的闪避和无视暴击伤害几率。
		增益效果受魔力值加成。
```

## entry-01561
位置：mod-tome.lua:21910；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#Your Contingency has failed to cast %s!
```
译文：
```text
#LIGHT_RED#你的意外术没能触发%s！
```

## entry-01562
位置：mod-tome.lua:21911；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#STEEL_BLUE#Your Contingency triggered %s!
```
译文：
```text
#STEEL_BLUE#你的意外术触发了%s！
```

## entry-01563
位置：mod-tome.lua:21913；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Choose an activatable spell that affects only you, does not require a target, and does not have a fixed cooldown.  When you take damage that reduces your life below %d%% the spell will automatically cast.
		This spell will cast even if it is currently on cooldown, will not consume a turn or resources, and uses the talent level of Contingency or its own, whichever is lower.
		This effect can only occur once every %d turns and takes place after the damage is resolved.

		Current Contingency Spell: %s
```
译文：
```text
选择一个只会影响你并且不需要选中目标的非固定冷却时间主动法术。当你受到伤害并使生命值降低到 %d%% 以下时，自动释放这个技能。
		即使选择的技能处于冷却状态也可以释放  ，并且不消耗回合或资源，技能等级取意外术与所选法术两者中较低的一方。
		这个效果每 %d 回合只能触发一次，并且在伤害结算之后生效。

		当前选择技能：%s
```

## entry-01564
位置：mod-tome.lua:21923；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The timeline is too fractured to do this now.
```
译文：
```text
目前的时间线过于破碎，你现在无法这么做。
```

## entry-01565
位置：mod-tome.lua:21925；section：mod-tome/data/talents/chronomancy/chronomancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You peer into three possible futures, allowing you to explore each for %d turns.  When the effect expires, you'll choose which of the three futures becomes your present.
		If you know Foresight you'll gain additional defense and chance to shrug off critical hits (equal to your Foresight values) while See the Threads is active.
		This spell splits the timeline.  Attempting to use another spell that also splits the timeline while this effect is active will be unsuccessful.
		If you die in any thread you'll revert the timeline to the point when you first cast the spell and the effect will end.
		This spell may only be used once per zone level.
```
译文：
```text
你窥视三种可能的未来，允许你分别进行探索 %d 回合。当效果结束，你选择三者之一成为你的现在。
		如果你学会了深谋远虑，当你使用命运螺旋时，将获得额外的闪避和无视暴击伤害几率（数值等于深谋远虑的奖励）。
		这个法术会使时间线分裂。当此技能激活的时候，使用其他分裂时间线的技能将会失败。
		如果你在任何一条时间线上死亡，你将使时间线回到你使用技能的地方，并且技能效果结束。
		这个技能每个楼层只能使用一次。
```

## entry-01566
位置：mod-tome.lua:21940；section：mod-tome/data/talents/chronomancy/energy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Partially dissipates all incoming damage, reducing it by 30%%, up to a maximum of %d.
		The maximum damage reduction will scale with your Spellpower.
```
译文：
```text
分解一部分受到的伤害。减少 30%% 伤害，最多减少 %d。
		减少伤害的最大值受法术强度加成。
```

## entry-01567
位置：mod-tome.lua:21946；section：mod-tome/data/talents/chronomancy/energy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You sap the target's energy and add it to your own, placing up to %d random talents on cooldown for %d turns.
		For each talent put on cooldown, you reduce the cooldown of one of your talents currently on cooldown by %d turns.
```
译文：
```text
你吸收目标的能量并化为己用，最多使 %d 个随机技能进入 %d 回合冷却。
		每使一个技能进入冷却，你减少你的一个处于冷却中的技能的冷却时间 %d 回合。
```

## entry-01568
位置：mod-tome.lua:21960；section：mod-tome/data/talents/chronomancy/fate-weaving.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you would take damage from someone else you gain one Spin, increasing your defense and saves by %d for three turns.
		This effect may occur once per turn and stacks up to three Spin (for a maximum bonus of %d).
```
译文：
```text
每当你要受到其他人造成的伤害时，你编织一层命运之丝，使你的闪避和豁免增加 %d，持续三回合。
		这个效果每回合只能触发一次，丝能叠加三层 (加成最多为 %d)。
```

## entry-01569
位置：mod-tome.lua:21987；section：mod-tome/data/talents/chronomancy/flux.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#LIGHT_BLUE##Source# converts damage to paradox!
```
译文：
```text
#LIGHT_BLUE##Source#将伤害转化为紊乱值！
```

## entry-01570
位置：mod-tome.lua:21989；section：mod-tome/data/talents/chronomancy/flux.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While active 30%% of all damage you take is converted into %0.2f Paradox per point.
		The Paradox is gained over three turns.
```
译文：
```text
当激活这个技能时，你受到的伤害有 30%% 会按每点伤害转化为 %0.2f 紊乱值。
		这些紊乱值会在三个回合内逐步获得。
```

## entry-01571
位置：mod-tome.lua:21992；section：mod-tome/data/talents/chronomancy/flux.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Attenuate
```
译文：
```text
衰减
```

## entry-01572
位置：mod-tome.lua:21993；section：mod-tome/data/talents/chronomancy/flux.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Deals %0.2f temporal damage over %d turns to all targets in a radius of %d.  Targets with Reality Smearing active will instead recover %d life over four turns.
		If a target is reduced below 20%% life while Attenuate is active it may be instantly slain.
		The damage will scale with your Spellpower.
```
译文：
```text
对范围内所有目标造成 %0.2f 点时空伤害，伤害分摊到 %d 回合内。技能半径为 %d 格。
		带有弥散现实效果的目标则改为在四回合内恢复 %d 点生命。
		衰减生效期间，若目标的生命值降至 20%% 以下，它可能会被立即杀死。
		伤害受法术强度加成。
```

## entry-01573
位置：mod-tome.lua:22001；section：mod-tome/data/talents/chronomancy/flux.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#STEEL_BLUE#Casts %s.
```
译文：
```text
#STEEL_BLUE#释放 %s。
```

## entry-01574
位置：mod-tome.lua:22004；section：mod-tome/data/talents/chronomancy/flux.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
If Twist Fate is not on cooldown minor anomalies will be held for %d turns, allowing your spell to cast as normal.  While held you may cast Twist Fate in order to trigger the anomaly and may choose the target area.
		If a second anomaly occurs while a prior one is held or the timed effect expires the first anomaly will trigger immediately, interrupting your current turn or action.
		Paradox reductions from held anomalies occur when triggered.
				
		Current Anomaly: %s
		
		%s
```
译文：
```text
若扭曲命运不在冷却中，微小异变会被延后 %d 回合，使你的法术得以正常施放。异变被延后期间，你可以施放扭曲命运来触发该异变，并选择其目标区域。
		如果已有一个异变被延后时又发生第二个异变，或延后效果到期，第一个异变会立即触发，并打断你当前的回合或行动。
		被延后异变带来的紊乱值降低会在其触发时结算。

		当前异变：%s

		%s
```

## entry-01575
位置：mod-tome.lua:22023；section：mod-tome/data/talents/chronomancy/gravity.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-01576
位置：mod-tome.lua:22025；section：mod-tome/data/talents/chronomancy/gravity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sends out a blast wave of gravity in a radius %d cone, dealing %0.2f base physical (gravity) damage and knocking back targets caught in the area.
		Targets knocked into walls or other targets take 25%% additional damage and deal 25%% damage to targets they're knocked into.
		Closer targets will be knocked back further and the damage will scale with your Spellpower.
```
译文：
```text
在半径 %d 码的锥形范围内释放一股爆炸性的重力冲击波，造成 %0.2f 物理（重力）伤害并击退范围内目标。
		被击飞至墙上或其他单位的目标受到额外 25%% 伤害，并对被击中的单位造成 25%% 伤害。
		离你越近的目标将会被击飞得更远。受法术强度影响，伤害按比例加成。
```

## entry-01577
位置：mod-tome.lua:22032；section：mod-tome/data/talents/chronomancy/gravity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creates a gravity spike in a radius of %d that moves all targets towards the spell's center and inflicts %0.2f physical (gravity) damage.
		Each target moved beyond the first increases the damage by %0.2f (up to a maximum of %0.2f bonus damage).
		Targets take reduced damage the further they are from the epicenter (20%% less per tile).
		The damage dealt will scale with your Spellpower.
```
译文：
```text
在半径 %d 范围内制造一个重力钉刺，将所有目标牵引至法术中心，造成 %0.2f 物理（重力）伤害。
		从第二个单位起，每牵引一个单位将会使伤害增加 %0.2f (最多增加 %0.2f 额外伤害)。
		离法术中心越远，目标受到的伤害越少（每格减少 20%%）。
		受法术强度影响，伤害按比例加成。
```

## entry-01578
位置：mod-tome.lua:22044；section：mod-tome/data/talents/chronomancy/gravity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases local gravity in a radius of %d for %d turns, dealing %0.2f physical (gravity) damage as well as decreasing the global speed of all affected targets by %d%%.
		The damage done will scale with your Spellpower.
```
译文：
```text
增加半径 %d 范围内的重力 %d 回合，造成 %0.2f 物理（重力）伤害，并降低所有目标的全局速度 %d%%。
		受法术强度影响，伤害按比例加成。
```

## entry-01579
位置：mod-tome.lua:22060；section：mod-tome/data/talents/chronomancy/guardian.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#STEEL_BLUE##Source# shares damage with %s guardian!
```
译文：
```text
#STEEL_BLUE##Source#和%s的守卫共享伤害！
```

## entry-01580
位置：mod-tome.lua:22068；section：mod-tome/data/talents/chronomancy/guardian.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#ORCHID#%s has recovered!#LAST#
```
译文：
```text
#ORCHID#%s恢复了！#LAST#
```

## entry-01581
位置：mod-tome.lua:22072；section：mod-tome/data/talents/chronomancy/guardian.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Warden's Focus
```
译文：
```text
守卫者专注
```

## entry-01582
位置：mod-tome.lua:22074；section：mod-tome/data/talents/chronomancy/guardian.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must pick a focus target.
```
译文：
```text
你必须选择一个集中目标。
```

## entry-01583
位置：mod-tome.lua:22075；section：mod-tome/data/talents/chronomancy/guardian.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Attack the target with either your ranged or melee weapons for %d%% weapon damage.  For the next %d turns random targeting, such as from Blink Blade and Warden's Call, will focus on this target.
		Attacks against this target gain %d%% critical chance and critical strike power while you take %d%% less damage from all enemies whose rank is lower then that of your focus target.
```
译文：
```text
使用你的远程或者近战武器对目标造成 %d%% 武器伤害。  在接下来的 %d 回合中，你的随机目标技能，比如闪烁灵刃和守卫召唤将会集中命中目标。
		对这个目标的攻击获得 %d%% 额外的暴击几率和暴击加成，同时其他分级低于目标的单位对你造成的伤害减少 %d%%。
```

## entry-01584
位置：mod-tome.lua:22089；section：mod-tome/data/talents/chronomancy/induced-phenomena.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must have Cosmic Cycle active to use this talent.
```
译文：
```text
你必须开启宇宙圈才能使用这一技能。
```

## 相关术语快照
```tsv
Cosmic Cycle	宇宙圈	T.GAME.TALENT	talents	talent name	preferred	core	时空系天赋名及机制称谓；描述中统一不用“宇宙轮回”
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Out of Phase	脱离现实	T.GAME.EFFECT	combat	_t	preferred	core	传送后获得的相位状态名；统一沿用效果定义，不泛化为“传送后加成”
Paradox	紊乱值	T.GAME.RESOURCE	resources	_t	existing	core	
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
gravity	重力	T.GAME.DAMAGE	combat	damage type	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
paradox	紊乱	T.GAME.TALENT	talents	talent type	preferred	core	时空技能类别名；资源数值在其他语境使用“紊乱值”
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
