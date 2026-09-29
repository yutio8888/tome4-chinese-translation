# batch-061：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01826
位置：mod-tome.lua:24404；section：mod-tome/data/talents/cursed/punishments.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Madness
```
译文：
```text
疯狂
```

## entry-01827
位置：mod-tome.lua:24422；section：mod-tome/data/talents/cursed/rampage.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You attack with mindless brutality. The first critical hit inflicted while rampaging increases the rampage duration by 1.
		Rampage Bonus: Your physical damage increases by %d%%.
		Rampage Bonus: Your Physical Save increases by %d and Mental Save increases by %d.
```
译文：
```text
使你的暴走更加无情，暴走状态下的第一次暴击可延长暴走效果 1 回合。
		暴走加成：你的物理伤害增加 %d%%。
		暴走加成：你的物理豁免增加 %d，精神豁免增加 %d。
```

## entry-01828
位置：mod-tome.lua:24435；section：mod-tome/data/talents/cursed/rampage.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#F53CBE#%s slams %s!
```
译文：
```text
#F53CBE#%s 猛击了 %s！
```

## entry-01829
位置：mod-tome.lua:24437；section：mod-tome/data/talents/cursed/rampage.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#F53CBE#Your rampage is invigorated by the collosal slam! (+1 duration)
```
译文：
```text
#F53CBE#巨力猛击激发了你的暴走！（+1 持续时间）
```

## entry-01830
位置：mod-tome.lua:24447；section：mod-tome/data/talents/cursed/self-hatred.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
At the start of each turn, if you're bleeding, you gain %d hate.

You can activate this talent to use your own life for power, bleeding yourself for a small portion of your maximum life (%0.2f damage) over the next 5 turns. This bleed cannot be resisted or removed, but can be reduced by Bloodstained.
```
译文：
```text
每回合开始时，如果你正在流血，你获得 %d 仇恨。

你可以主动使用此技能，使用你的生命值换取力量，使你在5回合里受到最大生命值一小部分的流血伤害（%0.2f 伤害）。此流血效果不能被抵抗，无法被移除，但可以被血染系技能减少。
```

## entry-01831
位置：mod-tome.lua:24473；section：mod-tome/data/talents/cursed/self-hatred.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Self-Judgement
```
译文：
```text
自我审判
```

## entry-01832
位置：mod-tome.lua:24474；section：mod-tome/data/talents/cursed/self-hatred.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#CRIMSON##Target# suffers from %s from #Source#, mitigating the blow!#LAST#.
```
译文：
```text
#CRIMSON##Target# 承受了来自#Source#的 %s，降低了伤害！#LAST#。
```

## entry-01833
位置：mod-tome.lua:24478；section：mod-tome/data/talents/cursed/self-hatred.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Any direct damage that exceeds %d%% of your maximum life has the excess damage converted to a shallow wound that bleeds over the next %d turns. This bleed cannot be resisted or removed, but can be reduced by Bloodstained. Extremely powerful hits (more than %d%% of your max life) are not fully converted.

#{italic}#You can't just die. That would be too easy.#{normal}#
```
译文：
```text
任何超过你最大生命 %d%% 的直接伤害中的额外部分会变成一道浅表伤口，在接下来的 %d 回合中造成流血伤害。此流血效果不能被抵抗或去除，但强度可以被血染系技能降低。极其强力的攻击（超过 %d%% 最大生命）无法被完全转化。

#{italic}#你不能就这么死了。这太轻松了。#{normal}#
```

## entry-01834
位置：mod-tome.lua:24509；section：mod-tome/data/talents/cursed/shadows.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Your hate is too low to call another shadow!
```
译文：
```text
你的仇恨值不足，无法召唤阴影！
```

## entry-01835
位置：mod-tome.lua:24511；section：mod-tome/data/talents/cursed/shadows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While this ability is active, you will continually call up to %d level %d shadows to aid you in battle. Each shadow costs 5 hate to summon. Shadows are weak combatants that can: Use Arcane Reconstruction to heal themselves (level %d), Blindside their opponents (level %d), and Phase Door from place to place.
		Shadows ignore %d%% of the damage dealt to them by their master.
```
译文：
```text
当此技能激活时，你可以召唤 %d 个等级 %d 的阴影帮助你战斗。每个阴影需消耗 5 点仇恨值召唤。
		阴影是脆弱的战士，它们能够：使用奥术重组治疗自己（等级 %d），使用闪电突袭攻击敌人（等级 %d），使用相位之门进行传送。
		阴影无视主人对它们造成的 %d%% 伤害。
```

## entry-01836
位置：mod-tome.lua:24516；section：mod-tome/data/talents/cursed/shadows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instill hate in your shadows, strengthening their attacks. They gain %d%% extra Accuracy and %d%% extra damage. The fury of their attacks gives them the ability to try to Dominate their foes, increasing all damage taken by that foe for 4 turns (level %d, %d%% chance at range 1). They also gain the ability to Fade when hit, avoiding all damage until their next turn (%d turn cooldown).
```
译文：
```text
将仇恨注入你的阴影，强化他们的攻击。他们获得 %d%% 额外命中和 %d%% 额外伤害加成。
		他们疯狂的攻击可以令他们支配对手，提高被支配目标所受到的所有伤害 4 回合（等级 %d，%d%% 几率 1 码范围）。
		它们同时拥有消隐的能力，免疫所有伤害直到下一回合开始（%d 回合冷却时间）。
```

## entry-01837
位置：mod-tome.lua:24520；section：mod-tome/data/talents/cursed/shadows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Infuse magic into your shadows to give them fearsome spells. Your shadows receive a bonus of %d to their Spellpower.
		Your shadows can strike adjacent foes with Lightning (level %d, %d%% chance at range 1).
		At level 3 your shadows can sear their enemies from a distance with Flames (level %d, %d%% chance at range 2 to 6).
		At level 5 when your shadows are struck down they will attempt to Reform, becoming whole again (50%% chance).
```
译文：
```text
灌输魔力给你的阴影使它们学会可怕的法术。你的阴影获得 %d 点法术强度加成。
		你的阴影可以用闪电术攻击附近的目标（等级 %d，%d%% 几率 1 码范围）。
		等级 3 时你的阴影可以远距离使用火焰术灼烧你的敌人（等级 %d，%d%% 几率 2 到 6 码范围）。
		等级 5 时你的阴影在被击倒时有一定几率重组并重新加入战斗（50%% 几率）。
```

## entry-01838
位置：mod-tome.lua:24528；section：mod-tome/data/talents/cursed/shadows.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#PINK#The shadows converge on #Target#!
```
译文：
```text
#PINK#阴影被集中至 #Target#！
```

## entry-01839
位置：mod-tome.lua:24530；section：mod-tome/data/talents/cursed/shadows.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#PINK#The shadows form around #Target#!
```
译文：
```text
#PINK#阴影被集中至 #Target#！
```

## entry-01840
位置：mod-tome.lua:24543；section：mod-tome/data/talents/cursed/slaughter.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You slash wildly at your target for %d%% (at 0 Hate) to %d%% (at 100+ Hate) damage.
		At level 3, any wound you inflict with this carries a part of your curse, reducing the effectiveness of healing by %d%% for %d turns. The effect will stack.
		The damage multiplier increases with your Strength.

		This talent will also attack with your shield, if you have one equipped.
```
译文：
```text
野蛮的削砍你的目标造成 %d%% （0仇恨）至 %d%% （100+仇恨）伤害。
		等级 3 时攻击附带诅咒，降低目标治疗效果 %d%% 持续 %d 回合，效果可叠加。
		伤害比例受力量值加成。

		如果你装备了盾牌，这一技能也会用你的盾牌攻击。
```

## entry-01841
位置：mod-tome.lua:24567；section：mod-tome/data/talents/cursed/slaughter.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Charge through your opponents, attacking anyone near your path for %d%% (at 0 Hate) to %d%% (at 100+ Hate) damage. %s opponents may be knocked away from your path. You can attack a maximum of %d times, and can hit targets along your path more than once.
```
译文：
```text
冲过你的目标，途经的所有目标受到 %d%% （0仇恨）至 %d%% （100+仇恨）伤害。%s 体型的目标会被你弹开。你最多可以攻击 %d 次，并且你对路径上的敌人可造成不止 1 次攻击。
```

## entry-01842
位置：mod-tome.lua:24570；section：mod-tome/data/talents/cursed/slaughter.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While active, every swing of your weapon strikes strikes other adjacent enemies for %d%% (at 0 hate) to %d%% (at 100 hate) physical damage. The recklessness of your attacks brings you bad luck (luck -3).
		Cleave, Repel and Surge cannot be active simultaneously, and activating one will place the others in cooldown.
		Cleave will deal 25%% additional damage while using a two-handed weapon.
		The Cleave damage increases with your Strength.
```
译文：
```text
激活时，你的每次武器攻击都会同时攻击其他相邻敌人，造成 %d%% （0 仇恨值）到 %d%% （100 仇恨值）的物理伤害。如此不顾一切的杀戮会带给你厄运（幸运 -3）。
		分裂攻击、无所畏惧和杀意涌动不能同时开启，并且激活一个也会使另外两个进入冷却。
		当使用双手武器时，分裂攻击会造成 25%% 的额外伤害。
		分裂攻击伤害受力量值加成。
```

## entry-01843
位置：mod-tome.lua:24590；section：mod-tome/data/talents/cursed/strife.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your preternatural senses aid you in your hunt for the next victim. You sense foes in a radius of %0.1f. You will always sense a stalked victim in a radius of 10.
		Also increases stealth detection by %d and invisibility detection by %d.
		Stealth and invisibility detection improves with your Willpower
```
译文：
```text
你的超自然感官能帮助你搜寻下一个猎物。
		你能感觉到 %0.1f 码半径范围内的敌人。
		在 10 码半径范围内你总能看见被追踪的目标。
		同时增加你的侦测潜行等级 %d，侦测隐形等级 %d。
		侦测强度受意志加成。
```

## entry-01844
位置：mod-tome.lua:24604；section：mod-tome/data/talents/cursed/strife.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Rather than hide from the onslaught, you face down every threat. While active you have a %d%% chance of repelling a melee attack. The recklessness of your defense brings you bad luck (Luck -3).
		Cleave, Repel and Surge cannot be active simultaneously, and activating one will place the others in cooldown.
		Repel chance increases with your Strength and by 20%% when equipped with a shield.
```
译文：
```text
在猛烈的攻击面前，你选择直面威胁而不是躲藏。
		当技能激活时，你有 %d%% 概率抵挡一次近程攻击。不顾一切的防御会带给你厄运（-3幸运）。
		分裂攻击，无所畏惧和杀意涌动不能同时开启，并且激活其中一个也会使另外两个进入冷却。
		抵挡概率受力量加成。
		装备盾牌时，抵挡概率增加 20%%。
```

## entry-01845
位置：mod-tome.lua:24628；section：mod-tome/data/talents/gifts/antimagic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You stand in the way of magical damage. That which does not kill you will make you stronger.
		When you are hit by hostile non-physical, non-mind damage you gain %d%% resistance to that element for 7 turns.
		At talent level 3, the bonus resistance may apply to 3 elements, refreshing the duration with each element added.
		Additionally, each time you take non-physical, non-mind damage, your equilibrium will decrease and stamina increase by %0.2f.
		The effects will increase with the greater of your Mindpower or Physical power and the bonus resistance can be a mental crit.
```
译文：
```text
你选择了站在魔法的对立面。那些未能杀死你的磨难将使你更加强大。
		每次你从敌对目标那里受到一种非物理、非精神伤害时，你能增加 %d%% 对该类型伤害的抗性，持续 7 回合。
		在技能等级 3 时，你可以获得对 3 种类型的抗性，每增加一种类型时都会刷新持续时间。
		此外，每当你被非物理，非精神伤害击中时，你会降低 %0.2f 失衡值并增加等量体力值。
		技能效果受精神或物理强度较高者加成，抗性加成效果可以触发精神暴击。
```

## entry-01846
位置：mod-tome.lua:24639；section：mod-tome/data/talents/gifts/antimagic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Let out a burst of sound that silences for %d turns all those affected in a radius of %d.
		Each turn for %d turns the effected area will cause %0.2f manaburn damage to all creatures inside.
		For each creature silenced your equilibrium is reduced by %d (up to 5 times).
		The damage and apply power will increase with the greater of your Mindpower or Physical power.

		Learning this talent will let your Nature damage and penetration bonuses apply to all Manaburn damage regardless of source.
```
译文：
```text
发出一阵音爆，使范围内所有目标沉默 %d 回合，范围半径 %d 格。
		接下来 %d 回合内，受影响区域中的所有生物每回合受到 %0.2f 法力燃烧伤害。
		每沉默一个生物，你的失衡值降低 %d，最多触发 5 次。
		伤害和效果强度受精神强度与物理强度中较高者加成。

		学会这个技能，也会让你的自然伤害加成和伤害穿透属性，对所有法力燃烧伤害生效，不管这一伤害的来源是什么。
```

## entry-01847
位置：mod-tome.lua:24652；section：mod-tome/data/talents/gifts/antimagic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with a shield that will absorb at most %d non-physical, non-mind element damage per attack.
		Each time damage is absorbed by the shield, your equilibrium increases by 1 for every 30 points of damage and a standard Equilibrium check is made. If the check fails, the shield will crumble and Antimagic Shield will go on cooldown.
		The damage the shield can absorb will increase with your Mindpower or Physical power (whichever is greater).
```
译文：
```text
给你增加一个护盾，每次被攻击吸收最多 %d 点非物理、非精神元素伤害。
		每当护盾吸收伤害时，都会按每 30 点伤害增加 1 点失衡值，并进行一次失衡值鉴定；若鉴定失败，则护盾会破碎且技能会进入冷却状态。
		护盾的最大伤害吸收值受精神或物理强度较高者加成。
```

## entry-01848
位置：mod-tome.lua:24658；section：mod-tome/data/talents/gifts/antimagic.lua；source_tag：_t；args_order：None；special：None

原文：
```text

#GREEN#Antimagic Adept:  #LAST#4 magical sustains from the target will be removed.
```
译文：
```text

#GREEN#反魔专家：#LAST#你的奥术对撞技能还会从目标身上移除 4 个持续魔法技能。
```

## entry-01849
位置：mod-tome.lua:24660；section：mod-tome/data/talents/gifts/antimagic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Drain %d mana, %d vim, %d positive and negative energies from your target, triggering a chain reaction that explodes in a burst of arcane damage.
		The damage done is equal to 100%% of the mana drained, 200%% of the vim drained, or 400%% of the positive or negative energy drained, whichever is higher. This effect is called a manaburn.
		The effect will increase with your Mindpower or Physical power (whichever is greater).
		%s
```
译文：
```text
从目标身上吸收 %d 点法力，%d 点活力，%d 点正负能量，并触发一次链式反应，引发一次奥术对撞。
		奥术对撞造成相当于 100%% 吸收的法力值或 200%% 吸收的活力值或 400%% 吸收的正负能量的伤害，按最高值计算（称为法力燃烧）。
		效果受精神或物理强度较高者加成。
		%s
```

## entry-01850
位置：mod-tome.lua:24725；section：mod-tome/data/talents/gifts/cold-drake.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ breathes ice!
```
译文：
```text
@Source@呼出寒冰！
```

## entry-01851
位置：mod-tome.lua:24737；section：mod-tome/data/talents/gifts/corrosive-blades.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Channel acid through your psiblades, extending their reach to create a beam doing %0.1f Acid damage (which can disarm them).
		The damage increases with your Mindpower.
```
译文：
```text
在你的心灵利刃里充填酸性能量，延展攻击范围，形成一道射线，造成 %0.1f 点酸性缴械伤害。
		伤害受精神强度加成。
```

## entry-01852
位置：mod-tome.lua:24751；section：mod-tome/data/talents/gifts/corrosive-blades.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You focus on a target zone of radius 2 to make up to %d corrosive seeds appear.
		The first seed will appear at the center of the target zone, while others will appear at random spots.
		Each seed lasts %d turns and will explode when a hostile creature walks over it, knocking the creature back and dealing %0.1f Acid damage within radius 1.
		The damage will increase with your Mindpower.
```
译文：
```text
你集中精神于某块半径 2 的区域，制造至多 %d 个腐蚀之种。
		第一个种子会产生于中心处，其他的会随机出现。
		每个种子持续 %d 回合，当一个敌对生物走过腐蚀之种时，会在半径 1 的区域内引发一场爆炸，击退对方并造成 %0.1f 点酸性伤害。
		伤害受精神强度加成。
```

## entry-01853
位置：mod-tome.lua:24759；section：mod-tome/data/talents/gifts/corrosive-blades.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with natural forces, ignoring %d%% acid resistance of your targets.
		In addition, the acid will nourish your bloated oozes, giving them an additional %0.1f life regeneration per turn.
```
译文：
```text
你的周围充满了自然力量，忽略目标 %d%% 的酸性伤害抗性。
		同时酸性能量会治疗你的浮肿软泥怪，增加他们每回合 %0.1f 的生命回复。
```

## entry-01854
位置：mod-tome.lua:24767；section：mod-tome/data/talents/gifts/dwarven-nature.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures %d missile-shaped rocks that you target individually at any target or targets in range.  Each missile deals %0.2f physical damage, and an additional %0.2f bleeding damage every turn for 5 turns.
		At talent level 5, you can conjure one additional missile.
		The damage will increase with your Spellpower.
```
译文：
```text
释放出 %d 个岩石飞弹，你可以为每个飞弹独立指定射程内的任意目标。每个飞弹造成 %0.2f 物理伤害和每回合 %0.2f 流血伤害，持续 5 回合。
		在等级 5 时，你可以额外释放一个飞弹。
		伤害受法术强度加成。
```

## entry-01855
位置：mod-tome.lua:24779；section：mod-tome/data/talents/gifts/dwarven-nature.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reach inside your dwarven core and summon your stone and crystaline halves to fight alongside you for %d turns.
		Your Crystaline Half will attack your foes with earthen missiles.
		Your Stone Half will taunt your foes to protect you.
		This power can not be called upon while under the effect of Deeprock Form.
		
```
译文：
```text
深入你的矮人血统，召唤岩石和水晶分身为你作战，持续 %d 回合。
		水晶分身会使用岩石飞弹攻击敌人。
		岩石分身会嘲讽敌人来保护你。
		处于深岩形态时，该技能不能使用。
		
```

## entry-01856
位置：mod-tome.lua:24819；section：mod-tome/data/talents/gifts/earthen-power.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The first time you take damage each turn, you regenerate %d%% of the damage dealt as mana (up to a maximum of %0.2f) and %d%% as equilibrium (up to %0.2f).
		Increases Physical Power by %d, increases damage done with shields by %d%%, and allows you to dual-wield shields.
		Also, all of your melee attacks will perform a shield bash in addition to their normal effects.
```
译文：
```text
每回合第一次承受伤害时，你将 %d%% 的伤害转化为法力 (至多 %0.2f 点)，%d%% 的伤害转化为失衡值 (至多回复 %0.2f)。
		增加物理强度 %d，增加盾牌伤害 %d%% , 并让你能够双持盾牌。
		同时，你的近战攻击附带一次盾牌攻击。
```

## entry-01857
位置：mod-tome.lua:24831；section：mod-tome/data/talents/gifts/earthen-power.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sharp shards of stone grow from your shields.
		When you are hit in melee, you will get a free attack against the attacker with the shards doing %d%% shield damage (as Nature).
		This effect can only happen once per turn and is not affected by counterstrike.
```
译文：
```text
尖锐的岩石碎片从盾牌生长出来。
		每次你承受近战攻击时，你能利用这些碎片反击攻击者，造成 %d%% 自然盾牌伤害。
		每回合只能反击一次，且不受反击（Counterstrike）状态影响。
```

## entry-01858
位置：mod-tome.lua:24868；section：mod-tome/data/talents/gifts/earthen-vines.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Merge with one of your stone vines, traversing it to emerge near an entangled creature (maximum range %d).
		Merging with the stone is beneficial for you, healing %0.2f life (increases with Willpower).
		This will not break Body of Stone.
```
译文：
```text
融入一条岩石藤蔓，穿行其中到达被缠绕的生物附近（最大射程 %d）。
		融入岩石藤蔓会治疗你 %0.2f 点生命值（受意志加成）。
		使用这个技能不会打破岩石身躯。
```

## entry-01859
位置：mod-tome.lua:24874；section：mod-tome/data/talents/gifts/earthen-vines.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Merge your target (within range %d) with one of your stone vines that has seized it, forcing it to traverse the vine and reappear near you.
		Merging with the stone is detrimental for the target, dealing %0.1f nature damage.
		The damage will increases with your Willpower.
```
译文：
```text
将射程 %d 内已被你的岩石藤蔓抓住的目标与藤蔓融合，使其强制穿越藤蔓，重新出现在你身边。
		与岩石融合的过程会对目标造成 %0.1f 自然伤害。
		伤害受意志加成。
```

## entry-01860
位置：mod-tome.lua:24884；section：mod-tome/data/talents/gifts/eyals-fury.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You focus the inexorable pull of nature against a single creature, eroding it and allowing it to be reclaimed by the cycle of life.
		This deals %0.1f Nature and %0.1f Acid damage to the target, and is particularly devastating against undead and constructs, dealing %d%% more damage to them.
		The damage increases with your Mindpower.
```
译文：
```text
你将自然无情的力量集中于某个目标上，腐蚀他并让他重归生命轮回。
		造成 %0.1f 点自然伤害，%0.1f 点酸性伤害，对不死族和构装生物有 %d%% 伤害加成。
		伤害受精神强度加成。
```

## entry-01861
位置：mod-tome.lua:24890；section：mod-tome/data/talents/gifts/eyals-fury.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your devotion to nature has made your body more attuned to the natural world and resistant to unnatural energies.
		You gain %d Spell save, %0.1f%% Arcane resistance, and %0.1f%% Nature damage affinity.
		You defy arcane forces, so that any time you take damage from a spell, you restore %0.1f Equilibrium each turn for %d turns.
		The effects increase with your Mindpower.
```
译文：
```text
你对自然的虔诚让你的身体更亲近自然世界，对非自然力量也更具抵抗力。
		你获得 %d 点法术豁免，%0.1f%% 奥术抗性，以及 %0.1f%% 自然伤害亲和。
		由于你和奥术力量对抗，每次你受到法术伤害时，你每回合回复 %0.1f 点失衡值，持续 %d 回合。
		效果受精神强度加成。
```

## entry-01862
位置：mod-tome.lua:24899；section：mod-tome/data/talents/gifts/eyals-fury.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You call upon the earth to create a blinding, corrosive cloud in an area of radius %d for %d turns.
		Each turn, this cloud deals %0.1f acid damage to each foe with a 25%% chance to blind and a %d%% chance of burning away one magical sustain or beneficial magical effect.
		The damage increases with your Mindpower.
```
译文：
```text
你召唤酸云覆盖半径 %d 的地面，持续 %d 回合。酸云具有腐蚀性，能致盲敌人。
		每回合，酸云对每个敌人造成 %0.1f 点酸性伤害，25%% 几率致盲，同时有 %d%% 几率除去一个有益的魔法效果或魔法持续技能。
		伤害受精神强度加成。
```

## entry-01863
位置：mod-tome.lua:24907；section：mod-tome/data/talents/gifts/eyals-fury.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You draw deeply from your connection with nature to create a radius %d storm of natural forces around you for %d turns.
		This storm moves with you and deals %0.1f Nature damage each turn to all foes it hits.
		In addtion, it will drain up to %d Mana, %d Vim, %d Positive, and %d Negative energy from each enemy within it's area every turn, while you restore Equilibrium equal to 10%% of the amount drained.
		The damage and drain increase with your Mindpower.
```
译文：
```text
你在自己周围半径 %d 的范围内制造自然力量风暴，持续 %d 回合。
		风暴会跟随你移动，每回合对每个敌人造成 %0.1f 点自然伤害。
		此外，每回合还会从范围内的每个敌人身上最多抽取 %d 点法力、%d 点活力、%d 点正能量和 %d 点负能量，同时使你的失衡值降低相当于所抽取能量的 10%%。
		伤害和吸取量受精神强度加成。
```

## entry-01864
位置：mod-tome.lua:24928；section：mod-tome/data/talents/gifts/fire-drake.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ roars!
```
译文：
```text
@Source@发出咆哮！
```

## entry-01865
位置：mod-tome.lua:24929；section：mod-tome/data/talents/gifts/fire-drake.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You let out a powerful roar that sends your foes in radius %d into utter confusion (power: %d%%) for 3 turns.
		The sound wave is so strong, your foes also take %0.2f physical damage.
		The damage improves with your Strength.
		Each point in fire drake talents also increases your fire resistance by 1%%.
```
译文：
```text
你发出一声咆哮使 %d 码半径范围内的敌人陷入彻底的混乱（强度 %d%%），持续 3 回合。
		如此强烈的咆哮使你的敌人受到 %0.2f 物理伤害。
		伤害受力量值加成。
		每点火龙系的技能可以使你增加火焰抗性 1%%。
```

## 相关术语快照
```tsv
Blindside	闪电突袭	T.GAME.TALENT	talents	talent name	preferred	core	技能会以极快速度瞬移至目标身边并攻击；按机制译作“闪电突袭”，不按普通动词字面译作“偷袭”
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Negative energy	负能量	T.GAME.RESOURCE	combat	_t	preferred	core	星空法师/死亡赞歌职业资源；与 Positive energy 正能量区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Phase Door	相位之门	T.GAME.TALENT	talents	talent name	existing	core	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
bloated ooze	浮肿软泥怪	T.GAME.ENTITY	creatures	_t	preferred	core	软泥系“有丝分裂”生成的召唤物；统一实体名及“软泥召唤”“强化吸收”等技能说明，不省略“软泥”
brutality	残暴	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
