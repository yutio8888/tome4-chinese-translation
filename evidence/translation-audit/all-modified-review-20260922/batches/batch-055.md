# batch-055：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01585
位置：mod-tome.lua:22091；section：mod-tome/data/talents/chronomancy/induced-phenomena.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reverses the polarity of your Cosmic Cycle.  If it's currently contracting, it will begin to expand, firing a homing missile at each target within the radius that deals %0.2f temporal damage.
		If it's currently expanding, it will begin to contract, braiding the lifelines of all targets within the radius for %d turns.  Braided targets take %d%% of all damage dealt to other braided targets.
		The damage will scale with your Spellpower.
```
译文：
```text
逆转你宇宙圈的极性。如果它正在收缩，它将开始膨胀，向半径范围内的每个目标发射一枚追踪飞弹，造成 %0.2f 时空伤害。
		如果它目前正在膨胀，它将开始收缩，将半径范围内所有目标的生命线编织 %d 回合。被编织目标承受对其他编织目标造成的所有伤害的 %d%%。
		伤害受法术强度加成。
```

## entry-01586
位置：mod-tome.lua:22102；section：mod-tome/data/talents/chronomancy/induced-phenomena.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Epoch
```
译文：
```text
纪元
```

## entry-01587
位置：mod-tome.lua:22116；section：mod-tome/data/talents/chronomancy/matter.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires a beam that turns matter into dust, inflicting %0.2f temporal damage and %0.2f physical (warp) damage.
		Alternatively you may target yourself, creating a field of radius %d around you that will inflict the damage over three turns.
		The damage will scale with your Spellpower.
```
译文：
```text
发射一道射线，令物质归于尘土，造成 %0.2f 时空伤害与 %0.2f 物理（扭曲）伤害。
		也可以以自己为目标，制造一个围绕自己 %d 码的领域，在 3 回合内造成伤害。
		伤害受法术强度加成。
```

## entry-01588
位置：mod-tome.lua:22122；section：mod-tome/data/talents/chronomancy/matter.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Weave matter into your flesh, becoming incredibly resilient to damage.  While active you gain %d armour, %d%% resistance to stunning, and %d%% resistance to cuts.
		The bonus to armour will scale with your Magic.
```
译文：
```text
你的血肉被改变，对伤害的抗性提高。激活时增加 %d 护甲，%d%% 震慑免疫，%d%% 流血免疫。
		护甲加成受魔力值加成。
```

## entry-01589
位置：mod-tome.lua:22128；section：mod-tome/data/talents/chronomancy/matter.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Create a tightly bound matter wall of up to a length of %d that lasts %d turns.
		If any part of this wall is dug out it will explode, causing targets in a radius of %d to bleed for %0.2f physical damage over six turns.
```
译文：
```text
制造一层坚实的物质墙，长度最多为 %d，持续 %d 回合。
		当墙壁被挖掘时，会产生半径 %d 的爆炸，范围内的目标会进入流血状态，6 回合内受到 %0.2f 物理伤害。
```

## entry-01590
位置：mod-tome.lua:22170；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mastery of spacetime reduces the cooldown of Banish, Dimensional Step, Swap, and Temporal Wake by %d, and the cooldown of Wormhole by %d.  Also improves your Spellpower for purposes of hitting targets with chronomancy effects that may cause continuum destabilization (Banish, Time Skip, etc.), as well as your chance of overcoming continuum destabilization, by %d%%.
```
译文：
```text
你的时空掌控使放逐、空间跳跃、时空交换和时空尾迹的冷却时间减少 %d 回合，使虫洞穿梭的冷却时间减少 %d 回合。当你用可能造成连续体失稳的时空技能（如放逐、时间跳跃等）命中目标时，判定所用的法术强度以及克服连续体失稳的几率均提高 %d%%。
```

## entry-01591
位置：mod-tome.lua:22183；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You begin to gather energy from other timelines. Your Spellpower will increase by %0.2f on the first turn and %0.2f more each additional turn.
		The effect ends either when you cast a spell, or after five turns.
		Eacn turn the effect is active, your Paradox will be reduced by %d.
		This spell will not break Spacetime Tuning, nor will it be broken by activating Spacetime Tuning.
```
译文：
```text
你开始从其他时间线搜集能量，初始增加 %0.2f 法术强度并且每回合逐渐增加 %0.2f 法术强度。
		此效果会因为施放法术而中断，否则会在 5 回合后结束。
		当此效果激活时，每回合你的紊乱值会降低 %d 点。
		此法术不会打断时空调谐，激活时空调谐也同样不会打断此法术。
```

## entry-01592
位置：mod-tome.lua:22195；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You partially remove yourself from the timeline for 10 turns.
		This increases your resistance to all damage by %d%%, reduces the duration of all detrimental effects on you by %d%%, and reduces all damage you deal by 20%%.
		The resistance bonus, effect reduction, and damage penalty will gradually lose power over the duration of the spell.
		The effects scale with your Spellpower.
```
译文：
```text
你将部分身体移出时间线，持续 10 回合。
		增加你 %d%% 所有伤害抗性，减少 %d%% 负面状态持续时间并减少 20%% 你造成的伤害。
		抵抗加成、状态减少值和伤害惩罚会随法术持续时间的增加而逐渐减少。
		效果受法术强度加成。
```

## entry-01593
位置：mod-tome.lua:22203；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01594
位置：mod-tome.lua:22205；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The real %s... or so %s says.
```
译文：
```text
真正的%s……或者%s这样说。
```

## entry-01595
位置：mod-tome.lua:22211；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#PINK##Source# displaces some damage onto #Target#!
```
译文：
```text
#PINK##Source#将部分伤害转移至#Target#！
```

## entry-01596
位置：mod-tome.lua:22216；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You surround yourself with a radius %d distortion of gravity, knocking back and dealing %0.2f physical damage to all creatures inside it.  The effect lasts %d turns.  Deals 50%% extra damage to pinned targets, in addition to the knockback.
		The blast wave may hit targets more then once, depending on the radius and the knockback effect.
		The damage will scale with your Spellpower.
```
译文：
```text
你用 %d 码半径范围的重力扭曲场围绕自己，击退所有单位并造成 %0.2f 物理伤害。此效果持续 %d 回合。除击退效果外，还对定身状态的目标额外造成 50%% 伤害。
		这股爆炸性冲击波可能会对目标造成多次伤害，这取决于攻击半径和击退效果。
		伤害受法术强度加成。
```

## entry-01597
位置：mod-tome.lua:22230；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You convert %d%% of all non-temporal damage you receive into temporal damage spread out over %d turns.
		This damage will bypass resistance and affinity.
```
译文：
```text
你将所有受到的 %d%% 的非时空伤害转化为时空伤害，分摊到 %d 回合承受。
		造成的伤害无视抗性和伤害亲和。
```

## entry-01598
位置：mod-tome.lua:22236；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-01599
位置：mod-tome.lua:22238；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You manipulate the spacetime continuum in such a way that you switch places with another creature with in a range of %d.  The targeted creature will be confused (power %d%%) for %d turns.
		The spell's hit chance will increase with your Spellpower.
```
译文：
```text
你控制时间的流动来使你和 %d 码范围内的某个怪物交换位置。目标会混乱（%d%% 强度）%d 回合。
		法术命中率受法术强度加成。
```

## entry-01600
位置：mod-tome.lua:22242；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-01601
位置：mod-tome.lua:22255；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Destabilize
```
译文：
```text
时空失稳
```

## entry-01602
位置：mod-tome.lua:22256；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Destabilizes the target, inflicting %0.2f temporal damage per turn for 10 turns.  If the target dies while destabilized, it will explode, doing %0.2f temporal damage and %0.2f physical damage in a radius of 4.
		If the target dies while also under the effects of continuum destabilization, all explosion damage will be done as temporal damage.
		The damage will scale with your Spellpower.
```
译文：
```text
使目标所处的时空出现裂隙，每回合造成 %0.2f 时空伤害，持续 10 回合。如果目标在被标记时死亡，则会产生 4 码半径范围的时空爆炸，造成 %0.2f 时空伤害和 %0.2f 物理伤害。
		如果目标死亡时处于连续体失稳状态，则爆炸产生的所有伤害会转化为时空伤害。
		伤害受法术强度加成。
```

## entry-01603
位置：mod-tome.lua:22264；section：mod-tome/data/talents/chronomancy/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Attempts to pull the target apart at a molecular level, inflicting %0.2f temporal damage and %0.2f physical damage.  If the target ends up with low enough life (<20%%), it might be instantly killed.
		Quantum Spike deals 50%% additional damage to targets affected by temporal destabilization and/or continuum destabilization.
		The damage will scale with your Spellpower.
```
译文：
```text
试图将目标分离为分子状态，造成 %0.2f 时空伤害和 %0.2f 物理伤害，技能结束后若目标生命值不足 20%% 则可能会被立刻杀死。
		量子钉刺对受时空失稳和/或连续体失稳的目标会多造成 50%%的伤害。
		伤害受法术强度加成。
```

## entry-01604
位置：mod-tome.lua:22278；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the teleport!
```
译文：
```text
%s抵抗了传送！
```

## entry-01605
位置：mod-tome.lua:22286；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay Warp Mines in a radius of 1 that teleport enemies away from you and inflict %0.2f physical and %0.2f temporal (warp) damage.
		The mines are hidden traps (%d detection and %d disarm power based on your Magic) and last for %d turns.
		The damage caused by your Warp Mines will improve with your Spellpower.
```
译文：
```text
在半径 1 的范围里埋设地雷，将敌人传送远离你身边并造成 %0.2f 物理和 %0.2f 时空伤害。
		地雷是隐藏的陷阱（%d 侦查强度 %d 解除强度基于魔法），持续 %d 回合。
		伤害受法术强度加成。
```

## entry-01606
位置：mod-tome.lua:22292；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Learn to lay Warp Mines in a radius of 1.  Warp Mines teleport targets that trigger them either toward you or away from you depending on the type of mine used and inflict %0.2f physical and %0.2f temporal (warp) damage.
		The mines are hidden traps (%d detection and %d disarm power based on your Magic), last for %d turns, and each have a ten turn cooldown.
		Investing in this talent improves the range of all Spacetime Folding talents and the damage caused by your Warp Mines will improve with your Spellpower.
		
		Current Spacetime Folding Range: %d
```
译文：
```text
学会在半径 1 的范围内埋设时空地雷。时空地雷会根据所用地雷的类型，将触发它们的目标传送到你身边或推离你身边，并造成 %0.2f 物理和 %0.2f 时空（扭曲）伤害。
		地雷是隐藏的陷阱（侦测强度 %d、拆除强度 %d，基于你的魔法），持续 %d 回合，各有 10 回合冷却时间。
		在该技能上投入点数会提升所有时空折叠系技能的范围，时空地雷的伤害也会随你的法术强度提升。
		
		当前时空折叠范围：%d
```

## entry-01607
位置：mod-tome.lua:22311；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles on %s!
```
译文：
```text
法术在 %s 上失败了！
```

## entry-01608
位置：mod-tome.lua:22312；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s has been banished!
```
译文：
```text
#CRIMSON#%s 被放逐了！
```

## entry-01609
位置：mod-tome.lua:22314；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Randomly teleports all enemies within a radius of three.  Enemies will be teleported between %d and %d tiles from you and may be stunned, blinded, confused, or pinned for %d turns.
		The chance of teleportion will scale with your Spellpower.
```
译文：
```text
将半径 3 以内的敌人随机传送。
		敌人将会传送至距离你 %d 至 %d 码的范围内，并可能被震慑、致盲、混乱或定身 %d 回合。
		传送几率与法术强度相关。
```

## entry-01610
位置：mod-tome.lua:22319；section：mod-tome/data/talents/chronomancy/spacetime-folding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Create a radius three anti-teleport field for %d turns and daze all enemies in the area of effect for two turns.
		Enemies attempting to teleport while anchored take %0.2f physical and %0.2f temporal (warp) damage.
		The damage will scale with your Spellpower.
```
译文：
```text
制造一个半径 3 的反传送力场，持续 %d 回合，并眩晕其中所有敌人 2 回合。
		被锚定期间试图传送的敌人将受到 %0.2f 物理和 %0.2f 时空（扭曲）伤害。
		伤害受法术强度加成。
```

## entry-01611
位置：mod-tome.lua:22329；section：mod-tome/data/talents/chronomancy/spacetime-weaving.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-01612
位置：mod-tome.lua:22330；section：mod-tome/data/talents/chronomancy/spacetime-weaving.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# folds space with with #target#!
```
译文：
```text
#Source#折叠了与#target#之间的空间！
```

## entry-01613
位置：mod-tome.lua:22332；section：mod-tome/data/talents/chronomancy/spacetime-weaving.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# resists #target#'s space-time folding!
```
译文：
```text
#Source#抵抗了#target#的时空折叠！
```

## entry-01614
位置：mod-tome.lua:22350；section：mod-tome/data/talents/chronomancy/spacetime-weaving.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fold the space between yourself and a second point within a range of %d, creating a pair of wormholes.  Any creature stepping on either wormhole will be teleported near the other (radius %d accuracy).  
		The wormholes will last %d turns and must be placed at least two tiles apart.
		The chance of teleporting enemies will scale with your Spellpower.
```
译文：
```text
你创造一对虫洞，使你所在之处和 %d 码范围内一点的空间重叠。  任何踏入虫洞的生物会被传送至另一个虫洞附近 (精度半径 %d)。
		虫洞持续 %d 回合并且至少相距两码。
		传送敌人的几率受法术强度加成。
```

## entry-01615
位置：mod-tome.lua:22372；section：mod-tome/data/talents/chronomancy/speed-control.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#STEEL_BLUE#%s has stopped time!#LAST#
```
译文：
```text
#STEEL_BLUE#%s 停止了时间！#LAST#
```

## entry-01616
位置：mod-tome.lua:22380；section：mod-tome/data/talents/chronomancy/spellbinding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Empowers the selected chronomancy spell, increasing spellpower when casting it by %d%%.
		Each spell can only be spellbound in one way at a time.
		
		Current Empowered Spell: %s
```
译文：
```text
使指定的时空系法术在施放时法术强度增加 %d%%。
		每个法术同时只能附加一种时空绑定效果。
		
		当前能量增幅法术：%s
```

## entry-01617
位置：mod-tome.lua:22388；section：mod-tome/data/talents/chronomancy/spellbinding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Extends the duration of the selected chronomancy spell by %d%%.
		Each spell can only be spellbound in one way at a time.
		
		Current Extended Spell: %s
```
译文：
```text
将选定时空法术的持续时间延长 %d%%。
		每个法术同时只能通过一种方式获得时空增效。
		
		当前延展法术：%s
```

## entry-01618
位置：mod-tome.lua:22396；section：mod-tome/data/talents/chronomancy/spellbinding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reduces the cooldown of the selected chronomancy spell by %d%%.
		Each spell can only be spellbound in one way at a time.
		
		Current Matrix Spell: %s
```
译文：
```text
减少指定时空系法术 %d%% 的冷却时间。
		每个法术同时只能附加一种时空绑定效果。
		
		当前矩阵加速法术：%s
```

## entry-01619
位置：mod-tome.lua:22404；section：mod-tome/data/talents/chronomancy/spellbinding.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reduces the casting speed of the selected chronomancy spell by %d%%.
		Each spell can only be spellbound in one way at a time.
		
		Current Quickened Spell: %s
```
译文：
```text
减少指定时空系法术 %d%% 的施法时间。
		每个法术同时只能附加一种时空绑定效果。
		
		当前迅捷施法法术：%s
```

## entry-01620
位置：mod-tome.lua:22442；section：mod-tome/data/talents/chronomancy/temporal-archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a shot that phases out of time and space allowing it to virtually ignore armor.  The shot will deal %d%% weapon damage as temporal damage to its target.
```
译文：
```text
你射出一枚脱离了时间与空间的子弹，这使它几乎可以无视护甲。此次射击会对目标造成 %d%% 时空武器伤害。
```

## entry-01621
位置：mod-tome.lua:22446；section：mod-tome/data/talents/chronomancy/temporal-archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You focus your aim, increasing your critical damage multiplier by %d%% and your physical and spell critical strike chance by %d%%
		The effect will scale with your Spellpower.
```
译文：
```text
集中你的注意力瞄准，增加你的暴击加成 %d%% 并提高你的物理和法术暴击率 %d%%。
		效果随法术强度提高。
```

## entry-01622
位置：mod-tome.lua:22470；section：mod-tome/data/talents/chronomancy/temporal-combat.lua；source_tag：tformat；args_order：[1, 3, 2, 4, 5]；special：None

原文：
```text
When you hit with Weapon Folding you have a %d%% chance of dealing an additional %0.2f physical (gravity) damage to enemies in a radius of %d.
		Affected targets may also be slowed, decreasing their global speed speed by %d%% for %d turns
		This effect has a cooldown.  If it triggers while on cooldown it will reduce the cooldown of Fold Fate and Fold Warp by one turn.
```
译文：
```text
当你用武器折叠命中时，有 %d%% 几率在半径 %d 内对敌人造成额外 %0.2f 物理（重力）伤害。
		受影响的生物还可能被减速，使其全局速度降低 %d%%，持续 %d 回合。
		这个效果有冷却时间。当处于冷却状态被触发时，会减少扭曲折叠和命运折叠 1 回合冷却时间。
```

## entry-01623
位置：mod-tome.lua:22486；section：mod-tome/data/talents/chronomancy/temporal-combat.lua；source_tag：tformat；args_order：[1, 3, 2, 4, 5, 8, 6, 7, 9, 11, 10, 12, 13]；special：None

原文：
```text
You now have a %d%% chance to Fold Fate, Gravity, or Warp into your Weapon Folding damage.
		
		Fold Fate: Deals %0.2f temporal damage to enemies in a radius of %d.  Affected targets may lose %d%% physical and temporal resistance for %d turns.
		Fold Warp: Deals %0.2f physical and %0.2f temporal damage to enemies in a radius of %d.  Affected targets may be stunned, blinded, confused, or pinned for %d turns.
		Fold Gravity: Deals %0.2f physical damage to enemies in a radius of %d.  Affected targets will be slowed (%d%%) for %d turns.
		
		Each Fold has an eight turn cooldown.  If an effect would be triggered while on cooldown it will reduce the cooldown of the other two Folds by one turn.
```
译文：
```text
你现在有 %d%% 几率将命运、重力或扭曲之力折叠进武器折叠伤害中。
		命运折叠：对半径 %d 内的敌人造成 %0.2f 点时空伤害，并可能使其物理和时空抗性降低 %d%%，持续 %d 回合。
		扭曲折叠：对半径 %d 内的敌人造成 %0.2f 点物理伤害和 %0.2f 点时空伤害，并可能使其震慑、致盲、混乱或定身 %d 回合。
		重力折叠：对半径 %d 内的敌人造成 %0.2f 点物理伤害，并使其减速 %d%%，持续 %d 回合。
		每项效果有 8 回合冷却时间。
		当处于冷却中的效果被触发时，将减少另外两个效果的冷却 1 回合。
```

## entry-01624
位置：mod-tome.lua:22509；section：mod-tome/data/talents/chronomancy/temporal-hounds.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A trained hound that appears to be all at once a little puppy and a toothless old dog.
```
译文：
```text
一条受训的猎犬，它看起来同时既是一只小狗崽，又是一条掉牙的老狗。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cosmic Cycle	宇宙圈	T.GAME.TALENT	talents	talent name	preferred	core	时空系天赋名及机制称谓；描述中统一不用“宇宙轮回”
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Epoch	亚伯契	T.PN.PERSON	society	nil	preferred	core	时空位面具名实体专名；同名天赋及神器 Epoch's Curve 均沿用音译，不按普通名词“纪元”处理
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Paradox	紊乱值	T.GAME.RESOURCE	resources	_t	existing	core	
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Temporal Wake	时空尾迹	T.GAME.TALENT	talents	talent name	preferred	core	传送经过路径留下的时空尾迹；Wake 指尾迹而非“苏醒”
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
chronomancy	时空	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
gravity	重力	T.GAME.DAMAGE	combat	damage type	existing	core	
knockback	击退	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Knockback Resistance；战斗日志“%s抵抗了击退！”
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
paradox	紊乱	T.GAME.TALENT	talents	talent type	preferred	core	时空技能类别名；资源数值在其他语境使用“紊乱值”
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
