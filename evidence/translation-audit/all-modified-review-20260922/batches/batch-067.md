# batch-067：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02068
位置：mod-tome.lua:26903；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summons your lust for blood and destruction; especially when the odds are against you.  
		You increase your damage by 10%% + %0.1f%% per enemy you can see in line of sight of you (maximum 5 enemies, %0.1f%% bonus) for 3 turns.
		The damage bonus will increase with your Constitution.
```
译文：
```text
唤起你对鲜血与毁灭的渴望，在寡不敌众时尤其强烈。
		造成的所有伤害提高 10%%，并且你视野内每有一个敌人再提高 %0.1f%%，持续 3 回合（最多计算 5 个敌人，最高加成为 %0.1f%%）。
		伤害加成随体质提高。
```

## entry-02069
位置：mod-tome.lua:26910；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Orcs have been the prey of the other races for thousands of years, with or without justification. They have learnt to withstand things that would break weaker races.
		When your life goes below 50%% your sheer determination cleanses you of %d mental debuff(s) based on talent level and Willpower.  This can only happen once every %d turns.
		Also increases physical save by %d.
```
译文：
```text
其他种族对兽族的猎杀持续了上千年，不管是否正义。你们已经学会忍受那些会摧毁弱小种族的灾难。
		当你的生命值降低到 50%% 以下，你强大的意志移除你身上最多 %d 个精神负面效果（基于技能等级和意志）。该效果每 %d 回合最多触发一次。
		额外增加 %d 物理豁免。
```

## entry-02070
位置：mod-tome.lua:26916；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Orcs have seen countless battles, and won many of them.
		You revel in the defeat of your foes, gaining %d%% damage resistance for 2 turns each time you kill an enemy.
		The resistance will scale with talent level and your Constitution.
		Additionally, passively increase all damage penetration by %d%%.
```
译文：
```text
兽人经历过无数战斗，并赢得了其中许多场。
		每当你击杀一个敌人，都会因战胜对手而振奋，获得 %d%% 全伤害抗性，持续 2 回合。
		该抗性随技能等级和体质提高。
		此外，被动提高 %d%% 所有伤害穿透。
```

## entry-02071
位置：mod-tome.lua:26946；section：mod-tome/data/talents/misc/races.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#RED#%s reacts immediately after taking severe wounds!#LAST#
```
译文：
```text
#RED#%s在受到重伤后立即作出反应！#LAST#
```

## entry-02072
位置：mod-tome.lua:26978；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
An ogre's body is acclimated to spells and inscriptions.
		Increases spell save by %d and improves the contribution of primary stats on infusions and runes by %d%%.
		At level 5 your body is so strong you can use a two handed weapon in your main hand while still using an offhand item.
		When using a two handed weapon this way you suffer a 20%% accuracy, physical power, spellpower and mindpower penalty, decreasing by 5%% per size category above #{italic}#big#{normal}#; further, all damage procs from your weapons are reduced by 50%%.
```
译文：
```text
食人魔的身体对法术和刻印的亲和力很强。
		增加 %d 法术豁免，增加刻印的属性加成效果 %d%%。
		技能等级 5 时，你的身体变得如此强壮，能在主手持有双手武器的同时，副手持有其他副手物品。
		这样做的话，你的命中、物理、法术、精神强度会下降 20%%，体型超过#{italic}#“较大”#{normal}#时，每增加一体型，惩罚减少 5%%。同时你的武器附加伤害减少 50%%。
```

## entry-02073
位置：mod-tome.lua:26990；section：mod-tome/data/talents/misc/races.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#PURPLE#Your mastery over inscriptions is unmatched! One more inscriptions slot available to buy.
```
译文：
```text
#PURPLE#你对刻印的掌握无人能及！你可以消耗一个大系点进一步解锁一个刻印位。
```

## entry-02074
位置：mod-tome.lua:27062；section：mod-tome/data/talents/psionic/absorption.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with a forcefield, reducing all incoming damage by %d%%.
		Such a shield is very expensive to maintain, draining 5%% of your maximum psi per turn initially plus an addition 5%% for each turn it has been maintained. For example, on turn 2 it will drain 10%%.
		Current drain rate: %0.1f psi/turn
```
译文：
```text
用力场环绕自己，减少受到的所有伤害 %d%%
		维持这样的护盾代价非常昂贵：初始每回合消耗你 5%% 的最大灵能值，此后每多维持一回合再额外增加 5%%。例如第 2 回合会消耗 10%%。
		目前的灵能值消耗：每回合 %0.1f 灵能值
```

## entry-02075
位置：mod-tome.lua:27072；section：mod-tome/data/talents/psionic/augmented-mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You telekinetically float just off the ground.
		This allows you to slide around the battle quickly, increasing your movement speed by %d%%.
		It also makes you more vulnerable to being pushed around (-%d%% knockback resistance).
```
译文：
```text
用念力使自己漂浮。
		这使你能在战斗中快速滑行，增加你的移动速度 %d%%。
		它同样使你更容易被推开 (-%d%% 击退抗性)。
```

## entry-02076
位置：mod-tome.lua:27078；section：mod-tome/data/talents/psionic/augmented-mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Encase your body in a sheath of thought-quick forces, allowing you to control your body's movements directly without the inefficiency of dealing with crude mechanisms like nerves and muscles.
		Increases Accuracy by %d, your critical strike chance by %0.1f%% and your global speed by %d%% for %d turns.
		The duration improves with your Mindpower.
```
译文：
```text
用灵能围绕你的躯体，通过思想直接高效控制身体，而不是通过神经和肌肉。
		增加 %d 命中、%0.1f%% 暴击率和 %d%% 全局速度，持续 %d 回合。
		持续时间受精神强度加成。
```

## entry-02077
位置：mod-tome.lua:27085；section：mod-tome/data/talents/psionic/augmented-mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Briefly extend your telekinetic reach to grab an enemy, haul them towards you and daze them for 1 turn.
		Works on enemies up to %d squares away.
		The cooldown decreases, and the range increases, with additional talent points spent.
```
译文：
```text
短暂延伸你的灵能触及以抓住一名敌人，将其拖向你并使其眩晕 1 回合。
		可作用于至多 %d 格外的敌人。
		每投入额外的技能点，冷却时间下降、射程提升。
```

## entry-02078
位置：mod-tome.lua:27093；section：mod-tome/data/talents/psionic/augmented-mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You perform a precise, telekinetically-enhanced leap, landing up to %d squares from your starting point.
```
译文：
```text
使用灵能，精准地跳跃，落在距起点至多 %d 格处。
```

## entry-02079
位置：mod-tome.lua:27101；section：mod-tome/data/talents/psionic/augmented-striking.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Focus kinetic energy and strike an enemy for %d%% weapon damage as physical.
		They will be pinned to the ground for %d turns by the force of this attack.
		Any frozen creature hit by this attack will take an extra %0.2f physical damage.
		The extra damage will scale with your Mindpower.
```
译文：
```text
聚焦动能打击敌人，造成 %d%% 武器物理伤害。
		敌人将被这次攻击的力量定身 %d 回合。
		任何处于冻结状态的目标受到额外 %0.2f 物理伤害。
		额外伤害受精神强度加成。
```

## entry-02080
位置：mod-tome.lua:27111；section：mod-tome/data/talents/psionic/augmented-striking.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Focus thermal energy and strike an enemy for %d%% weapon damage as cold.
		A burst of cold will then engulf them, doing an extra %0.1f Cold damage and also freeze them for %d turns.
		If the attack freezes a pinned creature a burst of ice is summoned, circling the caster and the creature with a wall of ice for 3 turns.
		The cold burst damage will scale with your Mindpower.
```
译文：
```text
聚焦热能打击敌人造成 %d%% 寒冷武器伤害。
		之后，一股寒冰能量将爆发并吞噬他们，造成额外 %0.1f 寒冷伤害并冻结他们 %d 回合。
		如果被冻结的目标已经被定身，则会爆发寒冰能量，环绕施法者与该生物组成冰墙，持续 3 回合。
		爆发的寒冷伤害受精神强度加成。
```

## entry-02081
位置：mod-tome.lua:27179；section：mod-tome/data/talents/psionic/discharge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Unleash your subconscious on the world around you.  While active, you fire up to %d bolts each turn (one per hostile target) that deal %0.2f mind damage.  Each bolt consumes 5 Feedback.
		Feedback gains beyond your maximum allowed amount may generate extra bolts (one bolt per %d excess Feedback per target), but no more than %d extra bolts per turn. 
		This effect is a psionic channel, increasing the range of Mind Sear, Psychic Lobotomy, and Sunder Mind to 10 but will break if you move.
		The damage will scale with your Mindpower.
```
译文：
```text
将你的潜意识释放到周围的世界。当此技能激活时，每回合你最多射出 %d 个灵能值球（每个敌方目标一个），造成 %0.2f 精神伤害。每个灵能值球消耗 5 点反馈值。
		当获得的反馈值超出最大值时，你会产生额外的灵能值球（每个目标每超出 %d 反馈值产生 1 个灵能值球），但是每回合产生的额外灵能值球数量不会超过 %d。
		此技能运用了灵能通道，所以当你移动时会中断此技能。
		特别地，当你开启此技能时，心灵灼烧、心灵脑叶切除和碾碎心灵的攻击范围将变为10格。
		受精神强度影响，伤害按比例加成。
```

## entry-02082
位置：mod-tome.lua:27195；section：mod-tome/data/talents/psionic/discharge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your subconscious now retaliates when you take damage.  If the attacker is within range (%d), you'll inflict mind damage equal to the Feedback gained from the attack or %0.2f, whichever is lower.
		This effect can only happen once per creature per turn.
		The damage will scale with your Mindpower.
```
译文：
```text
你的潜意识会报复那些伤害你的人。
		当攻击者在 %d 码范围内时，你会对目标造成精神伤害，伤害值为因承受此攻击而获得的反馈数值（但不超过 %0.2f）。
		此效果每回合对同一生物最多只能触发 1 次。
		受精神强度影响，伤害按比例加成。
```

## entry-02083
位置：mod-tome.lua:27202；section：mod-tome/data/talents/psionic/discharge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Focus your mind on a single target, diverting all offensive Discharge talent effects to it for %d turns.  While this effect is active, all Discharge talents gain %d%% critical power and you ignore %d%% mind resistance of your targets.
		If the target is killed, the effect will end early.
		At level level 5 your single-minded focus also resets the cooldown of Mind Storm.
		The damage bonus will scale with your Mindpower.
```
译文：
```text
将注意力集中于单体目标，将所有攻击性灵能脉冲系技能射向目标，持续 %d 回合。当此技能激活时，所有灵能脉冲系技能增加 %d%% 暴击伤害，并且你可以获得 %d%% 精神抗性穿透。
		如果目标死亡，则该技能提前中断。
		技能等级 5 时，你一心一意的注意力也会重置心灵风暴技能的冷却时间。
		受精神强度影响，暴击增益效果按比例加成。
```

## entry-02084
位置：mod-tome.lua:27213；section：mod-tome/data/talents/psionic/distortion.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Distortion Bolt
```
译文：
```text
扭曲飞弹
```

## entry-02085
位置：mod-tome.lua:27214；section：mod-tome/data/talents/psionic/distortion.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire a bolt of distortion that ignores resistance and inflicts %0.2f physical damage.  This damage will distort affected targets, decreasing physical resistance by %d%% and rendering them vulnerable to distortion effects for two turns.
		If the bolt comes in contact with a target that's already distorted, a detonation will occur, inflicting 150%% of the base damage in a radius of %d.
		Investing in this talent will increase the physical resistance reduction from all of your distortion effects.
		At talent level 5, you learn to shape your distortion effects, preventing them from hitting you or your allies.
		The damage will scale with your Mindpower.
```
译文：
```text
射出一枚无视抵抗的扭曲飞弹并造成 %0.2f 物理伤害。此技能会扭曲目标，减少对方物理抗性 %d%%，并使其在 2 回合内受到扭曲效果时会产生额外的负面影响。
		如果飞弹命中已存在扭曲效果的目标，则会在 %d 码范围内产生 150%% 基础伤害的爆炸。
		在该技能投入点数会增加你所有扭曲效果的降抗效果。
		在等级 5 时，你学会控制你的扭曲效果，防止扭曲效果攻击到你或友军。
		受精神强度影响，伤害按比例加成。
```

## entry-02086
位置：mod-tome.lua:27245；section：mod-tome/data/talents/psionic/distortion.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# pulls #Target# in!
```
译文：
```text
#Source#将#Target#拉了进来！
```

## entry-02087
位置：mod-tome.lua:27258；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#ORANGE#%s forges a dream shield to block the attack!
```
译文：
```text
#ORANGE#%s 产生了一个梦境屏障来格挡攻击！
```

## entry-02088
位置：mod-tome.lua:27259；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#ORANGE#%s's dream shield has been strengthened by the attack!
```
译文：
```text
#ORANGE#%s 的梦境屏障被攻击强化了！
```

## entry-02089
位置：mod-tome.lua:27272；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Release the bellows of the forge upon your surroundings, inflicting %0.2f mind damage, %0.2f burning damage, and knocking back your enemies in a radius %d cone.
		Empty terrain may be changed (50%% chance) for %d turns into forge walls, which block movement and inflict %0.2f mind and %0.2f fire damage on nearby enemies.
		The damage and knockback chance will scale with your Mindpower.
```
译文：
```text
将梦之熔炉的风箱打开，朝向你的四周，对锥形范围内敌人造成 %0.2f 精神伤害，%0.2f 燃烧伤害并造成击退效果。锥型范围的半径为 %d 码。
		空旷的地面有 50 %%几率转化为持续 %d 回合的熔炉外壁。熔炉外壁阻挡移动，并对周围敌人造成 %0.2f 的精神伤害和 %0.2f 的火焰伤害。
		受精神强度影响，伤害和击退几率按比例加成。
```

## entry-02090
位置：mod-tome.lua:27278；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your Forge Shield talent now increases your Armour by %d, your Defense by %d, and gives you %0.2f psi when you're hit by a melee or ranged attack.
		The bonuses will scale with your Mindpower.
```
译文：
```text
你的熔炉屏障技能现在可以增加你 %d 点护甲，%d 点闪避，并且当你被近战或远程攻击击中时给予你 %0.2f 灵能值。
		受精神强度影响，增益按比例加成。
```

## entry-02091
位置：mod-tome.lua:27282；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#GOLD#%s strikes the dreamforge!
```
译文：
```text
#GOLD#%s锤击着梦境熔炉！
```

## entry-02092
位置：mod-tome.lua:27283；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#GOLD#%s begins breaking dreams!
```
译文：
```text
#GOLD#%s开始破碎梦境！
```

## entry-02093
位置：mod-tome.lua:27284；section：mod-tome/data/talents/psionic/dream-forge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The pounding forge of thought in your mind is released upon your surroundings.  Each turn that you remain stationary, you'll strike the dreamforge, inflicting mind and burning damage on enemies around you.
		The effect will build over five turns, until it reaches a maximum radius of %d, maximum mind damage of %0.2f, and maximum burning damage of %0.2f.
		At this point you'll begin breaking the dreams of enemies who hear the forge, reducing their Mental Save by %d and giving them a %d%% chance of spell failure due to the tremendous echo in their minds for %d turns.
		Broken Dreams has a %d%% chance to brainlock your enemies.
		The damage and dream breaking effect will scale with your Mindpower.
```
译文：
```text
你将脑海里锻造的冲击波向四周释放。
		每回合当你保持静止，你将会锤击梦之熔炉，对周围敌人造成精神和燃烧伤害。
		此效果将递增 5 个回合，直至 %d 码最大范围，%0.2f 最大精神伤害和 %0.2f 最大燃烧伤害。
		此刻，你将会打破那些听到熔炉声的敌人梦境，减少它们 %d 精神豁免，并且由于敲击熔炉的
		巨大回声，它们将获得一个 %d%% 的法术失败率，持续 %d 回合。
		梦境破碎有 %d%% 几率对你的敌人产生思维封锁效果。
		受精神强度影响，伤害和梦境打破效果按比例加成。
```

## entry-02094
位置：mod-tome.lua:27313；section：mod-tome/data/talents/psionic/dream-smith.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw your Dream Hammer at a distant location, inflicting %d%% weapon damage on all targets between you and it.  After reaching its destination, the Dream Hammer will return, potentially hitting targets a second time.
		Learning this talent increases the Accuracy of your Dream Hammer by %d.
```
译文：
```text
将你的梦之巨锤扔向远处，对沿途所有敌方单位造成 %d%% 武器伤害。在到达目标点后，梦之巨锤会飞回，可能再次对沿途目标造成伤害。
		学习此技能会增加梦之巨锤 %d 点命中。
```

## entry-02095
位置：mod-tome.lua:27316；section：mod-tome/data/talents/psionic/dream-smith.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Dream Crusher
```
译文：
```text
梦锤碎击
```

## entry-02096
位置：mod-tome.lua:27317；section：mod-tome/data/talents/psionic/dream-smith.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning blow!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-02097
位置：mod-tome.lua:27318；section：mod-tome/data/talents/psionic/dream-smith.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Crush your enemy with your Dream Hammer, inflicting %d%% weapon damage.  If the attack hits, the target is stunned for %d turns.
		Stun chance improves with your Mindpower.  Learning this talent increases your Physical Power for Dream Hammer damage calculations by %d and all damage with Dream Hammer attacks by %d%%.
		
```
译文：
```text
用你的梦之巨锤碾碎敌人，造成 %d%% 武器伤害。如果攻击命中，则目标会被震慑 %d 回合。
		震慑几率受精神强度加成
		学习此技能会增加 %d 点你使用梦之巨锤时的物理强度，同时使梦之巨锤造成的所有伤害提升 %d%%。
```

## entry-02098
位置：mod-tome.lua:27324；section：mod-tome/data/talents/psionic/dream-smith.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Strike an adjacent target with a mighty blow from the forge, inflicting %d%% weapon damage.  If the attack hits, the echo of the attack will lash out at all enemies in a %d radius of the impact.
		Learning this talent adds %0.2f mind damage and %0.2f burning damage to your Dream Hammer strikes.
		The mind and fire damage will scale with your Mindpower.
```
译文：
```text
用梦之巨锤对近身目标挥出强力的一击，造成 %d%% 武器伤害。如果攻击命中，挥击所产生的回音会伤害 %d 码范围内的所有敌人。
		学习此技能会使你的梦之巨锤附加 %0.2f 精神伤害和 %0.2f 燃烧伤害。
		受精神强度影响，梦之巨锤附加的精神伤害和燃烧伤害按比例加成。
```

## entry-02099
位置：mod-tome.lua:27351；section：mod-tome/data/talents/psionic/dreaming.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You move through the dream world, reappearing at a nearby location.
		If there is a sleeping creature at the target location, you'll appear as close to them as possible, otherwise, you'll appear within %d tiles of your intended destination.
```
译文：
```text
你穿越梦境，出现在某个目标地点附近。
		如果目标位置有处于睡眠状态的生物，你会尽量出现在离它最近的地方；否则，你会出现在目标位置 %d 码范围内。
```

## entry-02100
位置：mod-tome.lua:27355；section：mod-tome/data/talents/psionic/dreaming.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Imprisons all sleeping targets within range in their dream state, effectively extending sleeping effects for as long as Dream Prison is maintainted.
		This powerful effect constantly drains %0.2f%% of your maximum Psi (excluding this talent) per turn, and is considered a psionic channel; as such it will break if you move.
		(Note that sleeping effects that happen each turn, such as Nightmare's damage and Sleep's contagion, will cease to function for the duration of the effect.)
```
译文：
```text
将范围内所有睡眠状态的目标囚禁在梦境牢笼里，在梦境牢笼维持期间有效地延长他们的睡眠效果。
		这个强大的技能每回合会持续消耗 %0.2f%% 最大灵能值（本技能除外），并且运用了灵能通道，所以当你移动时会中断此技能。
		（注意：每回合可产生的睡眠附加状态，如梦魇的伤害和入梦的传染效果，将在此效果持续过程中失效。）
```

## entry-02101
位置：mod-tome.lua:27365；section：mod-tome/data/talents/psionic/feedback.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your Feedback decay now heals you for %0.1f times the loss, and the decay rate is reduced to %d%% of the normal rate (up to %0.1f%% per turn).  As a result, you are healed for %0.2f%% of your feedback pool each turn.
		The healing effect improves with your Willpower.
```
译文：
```text
你的反馈值衰减的 %0.1f 倍会转换成治疗，同时衰减速率下降至 %d%% （每回合最多 %0.1f%%）。总而言之，每回合你将受到治疗量等于你的反馈池 %0.2f%% 的治疗。
		治疗效果受意志加成。
```

## entry-02102
位置：mod-tome.lua:27369；section：mod-tome/data/talents/psionic/feedback.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate to create a resonance field that will absorb 50%% of all damage you take (%d max absorption).  The field will not interfere with Feedback gain.
		The max absorption value will scale with your Mindpower, and the effect lasts up to ten turns.
```
译文：
```text
激活此技能可产生一个吸收所受全部伤害 50%% 的共鸣领域（最大吸收值 %d）。此领域不会干扰反馈值的增长。
		最大吸收值受精神强度加成，此技能最多维持 10 回合。
```

## entry-02103
位置：mod-tome.lua:27380；section：mod-tome/data/talents/psionic/feedback.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Use Feedback to replenish yourself.  This heals you for %d life, and restores %d stamina, %d mana, %d equilibrium, %d vim, %d positive and negative energies, %d psi energy, and %d hate.
		The heal and resource gain will improve with your Mindpower.
```
译文：
```text
使用反馈值来补充自己。治疗 %d 生命值并回复 %d 点耐力，%d 点法力，%d 点失衡值，%d 点活力，%d 点正能量和负能量，%d 点灵能值及 %d 点仇恨值。
		增益效果受精神强度加成。
```

## entry-02104
位置：mod-tome.lua:27393；section：mod-tome/data/talents/psionic/finer-energy-manipulations.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Manipulate forces on the molecular level to realign, rebalance, and synergize equipment you wear to your form and function.
		The accuracy and damage of any weapon will act as if it were %d higher. (Mindstars cannot be manipulated in this way because they are already in an ideal natural state.)
		Your total armour will increase by %d and your fatigue will decrease by %d for each body armour and shield worn.
		The effects increase with your Mindpower.
```
译文：
```text
操纵力量从分子层面重组、平衡、磨砺你的装备。
		你装备的每一件武器都会提升 %d 的命中和伤害。灵晶不能被调整，因为他们已经是完美的自然形态。
		你所穿的躯干护甲与所持的盾牌，每有一件便增加你 %d 护甲，同时减少 %d 疲劳。
		该技能效果受精神强度影响。
```

## entry-02105
位置：mod-tome.lua:27402；section：mod-tome/data/talents/psionic/finer-energy-manipulations.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Matter is energy, as any good Mindslayer knows. Unfortunately, the various bonds and particles involved are just too numerous and complex to make the conversion feasible in most cases. The ordered, crystalline structure of a gem, however, make it possible to transform a small percentage of its matter into usable energy.
		This talent consumes one gem and grants %d psi per turn for between 5 and 13 turns, depending on the quality of the gem used.
		This process also creates a resonance field that provides the (imbued) effects of the gem to you while this effect lasts.
```
译文：
```text
任何优秀的心灵杀手都知道，物质就是能量。遗憾的是，大多数物质由于分子成分的复杂性无法转换。然而，宝石有序的晶体结构使得部分物质转化为能量成为可能。
		这个技能消耗一个宝石，在 5~13 回合内，每回合获得 %d 灵能值，持续回合取决于所用的宝石品质。
		在持续时间内同时获得一个共振领域提供宝石的效果。
```

## entry-02106
位置：mod-tome.lua:27408；section：mod-tome/data/talents/psionic/finer-energy-manipulations.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
By carefully synchronizing your mind to the resonant frequencies of your psionic focus, you strengthen its effects.
		For conventional weapons, this increases the percentage of your willpower and cunning that is used in place of strength and dexterity for all weapon attacks, from 60%% to %d%%.
		For mindstars, this increases the chance to pull enemies to you by +%d%%.
		For gems, this increases the bonus stats by %d.
```
译文：
```text
通过小心的同步你的精神和灵能聚焦的共振频率，强化灵能聚焦的效果
		对于武器，提升你的意志和灵巧来代替力量和敏捷的百分比，从 60%% 到 %d%%.
		对于灵晶，提升 %d%% 将敌人抓取过来的几率。
		对于宝石，提升 %d 额外全属性。
```

## entry-02107
位置：mod-tome.lua:27420；section：mod-tome/data/talents/psionic/focus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Focus energies into a beam to lash all creatures in a line with physical force, doing %d Physical damage and knocking them off balance (-15%% damage penalty) for 2 turns.
		The damage will scale with your Mindpower.
```
译文：
```text
汇聚能量形成一道光束，鞭笞一条直线上的所有生物，造成 %d 点物理伤害并使它们失去平衡两轮（-15%% 伤害）。
		伤害受精神强度加成。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mind Sear	心灵灼烧	T.GAME.TALENT	talents	talent name	preferred	core	sear 指灼烧；技能机制虽为射线，名称不增译“光束”
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Mindslayer	心灵杀手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Psychic Lobotomy	心灵脑叶切除	T.GAME.TALENT	talents	talent name	preferred	core	与技能日志中的 lobotomy 统一
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
cleanse	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key，与 cleansing keyword 同一 cohort；不约束动作、技能说明或其他语境
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
inscriptions	刻印	T.GAME.TALENT_CATEGORY	talents	talent category	preferred	global	统一核心和兽人战役的技能类别译法；具体类型仍使用“纹身/符文”
knockback	击退	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Knockback Resistance；战斗日志“%s抵抗了击退！”
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
offhand	副手	T.GAME.ENTITY	items	nil	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
