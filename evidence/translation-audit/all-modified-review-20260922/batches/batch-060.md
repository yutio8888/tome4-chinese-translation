# batch-060：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01786
位置：mod-tome.lua:24035；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The battlefield is your home; death and confusion, your comfort.
```
译文：
```text
战场就是你的最终归宿，死亡和混乱是你仅有的慰藉。
```

## entry-01787
位置：mod-tome.lua:24037；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
All those in your sight must share your despair.
```
译文：
```text
强迫你视线内的生物替你分担你心中的绝望。
```

## entry-01788
位置：mod-tome.lua:24039；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Let loose the hate that has grown within.
```
译文：
```text
释放你内心激增的愤怒。
```

## entry-01789
位置：mod-tome.lua:24041；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Track and kill your prey with single-minded focus.
```
译文：
```text
你集中精神追猎并杀死你的猎物。
```

## entry-01790
位置：mod-tome.lua:24045；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Invoke the powerful force of your will.
```
译文：
```text
呼唤你意志的力量。
```

## entry-01791
位置：mod-tome.lua:24047；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of darkness to envelop your foes.
```
译文：
```text
操纵黑暗之力包围你的敌人。
```

## entry-01792
位置：mod-tome.lua:24049；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Summon shadows from the darkness to aid you.
```
译文：
```text
从黑暗中召唤阴影来协助你战斗。
```

## entry-01793
位置：mod-tome.lua:24051；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your hate becomes punishment in the minds of your foes.
```
译文：
```text
你的仇恨转变为对你敌人的精神惩罚。
```

## entry-01794
位置：mod-tome.lua:24067；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You, like your weapons, are tainted forever.
```
译文：
```text
你和你的武器一样，已被永久玷污。
```

## entry-01795
位置：mod-tome.lua:24069；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Blood is power. Let the rivers run red.
```
译文：
```text
鲜血即力量。让河水变红吧。
```

## entry-01796
位置：mod-tome.lua:24073；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Hate-powered abilities that don't belong anywhere else.
```
译文：
```text
由仇恨驱动、无法归入其他类别的各项能力。
```

## entry-01797
位置：mod-tome.lua:24080；section：mod-tome/data/talents/cursed/dark-figure.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fear radiates from your target in a radius of %d for %d turns driving all others away.
```
译文：
```text
恐惧从你的目标身上向 %d 码半径散发，持续 %d 回合，将周围所有其他生物驱离。
```

## entry-01798
位置：mod-tome.lua:24093；section：mod-tome/data/talents/cursed/dark-sustenance.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You can only gain sustenance from your foes!
```
译文：
```text
你只能从敌人身上吸取！
```

## entry-01799
位置：mod-tome.lua:24103；section：mod-tome/data/talents/cursed/dark-sustenance.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Feed Power
```
译文：
```text
吸食伤害
```

## entry-01800
位置：mod-tome.lua:24107；section：mod-tome/data/talents/cursed/dark-sustenance.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Feed Strengths
```
译文：
```text
吸食抗性
```

## entry-01801
位置：mod-tome.lua:24108；section：mod-tome/data/talents/cursed/dark-sustenance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your feeding by reducing your targeted foe's resistances, multiplying them by %0.2f and increasing your resistances by the amount drained. Resistance to "all" is not affected.
		Improves with your Mindpower.
```
译文：
```text
提高你的吸食能力，将目标的伤害抗性降低到原来的 %0.2f 倍，并将你自身相应的伤害抗性提高相同数值。
		对“所有”抗性无效。
		效果受精神强度加成。
```

## entry-01802
位置：mod-tome.lua:24125；section：mod-tome/data/talents/cursed/darkness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your eyes penetrate the darkness to find anyone that may be hiding there. This allows you to see through creeping darkness out to a radius of %d. You can also find your way through the darkness with greater speed (+%d%% movement into creeping darkness).
		You do +%d%% damage to anything that has entered your creeping dark.
```
译文：
```text
你的眼睛穿过黑暗，发现可能隐藏其中的敌人。你的视线可以穿过黑暗之雾看到 %d 码半径范围，同时你能以更快的步伐穿行于黑暗之中（在黑暗之雾中增加你 +%d%% 移动速度）。
		你对任何进入你的黑暗之雾的目标造成 +%d%% 伤害。
```

## entry-01803
位置：mod-tome.lua:24129；section：mod-tome/data/talents/cursed/darkness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sends a torrent of searing darkness through your foes, doing %d darkness damage. There is a 25%% chance the rushing darkness will blind them for 3 turns and cause them to lose track of their target.
		If you know the Creeping Darkness talent, a short-lived trail of darkness is left in the beam's wake. Its damage is identical to that of Creeping Darkness's.
		The damage will increase with your Mindpower. You do +%d%% damage to anything that has entered your creeping dark.
```
译文：
```text
向敌人发射一股灼热的黑暗能量，造成 %d 点黑暗伤害。黑暗能量有 25%% 概率致盲目标 3 回合并使它们丢失当前目标。
			如果你掌握黑暗之雾技能，会在射线范围内留下短暂的黑暗尾迹，其伤害等同于黑暗之雾的伤害。
			伤害受精神强度加成。你对任何进入黑暗之雾的人造成 +%d%% 伤害。
```

## entry-01804
位置：mod-tome.lua:24135；section：mod-tome/data/talents/cursed/darkness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Spawn tendrils of darkness to pursue a single target for up to 12 turns, leaving behind a trail of creeping darkness as they move. Targets seized by the tendrils are pinned for %d turns and shrouded in darkness. The darkness deals %0.2f damage per turn to those within.
		The damage will increase with your Mindpower. You do +%d%% damage to anything that has entered your creeping dark.
```
译文：
```text
召唤黑暗触手攻击某个敌人，持续12回合。当黑暗触手移动时，黑暗之雾会跟随蔓延。
			被触手抓住的敌人会被定身 %d 回合并被黑暗笼罩，每回合黑暗会造成 %0.2f 点伤害。
			伤害受精神强度加成。你对任何进入黑暗之雾的人造成 +%d%% 伤害。
```

## entry-01805
位置：mod-tome.lua:24145；section：mod-tome/data/talents/cursed/endless-hunt.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you focus your attacks on a single foe and strike them in melee for two consecutive turns, your hatred of them overcomes you and you begin to stalk them with single-minded purpose. The effect will last for %d turns, or until your prey is dead. Stalking gives you bonuses against your foe that grow each turn you hit them, and diminish each turn you don't.
		Bonus level 1: +%d Accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit
		Bonus level 2: +%d Accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit
		Bonus level 3: +%d Accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit
		The accuracy bonus improves with your Willpower, and the melee damage bonus with your Strength.
```
译文：
```text
当你连续两回合持续近战攻击同一个目标时，你将憎恨目标并追踪目标，效果持续 %d 回合或直到目标死亡。
		你每回合命中猎物都会使增益提升 1 层；未命中猎物的每回合，增益降低 1 层。
		1 重增益：+%d 命中，+%d%% 近战伤害，当目标被击中时，每回合增加 +%0.2f 仇恨值。
		2 重增益：+%d 命中，+%d%% 近战伤害，当目标被击中时，每回合增加 +%0.2f 仇恨值。
		3 重增益：+%d 命中，+%d%% 近战伤害，当目标被击中时，每回合增加 +%0.2f 仇恨值。
		命中受意志加成。
		近战伤害受力量值加成。
```

## entry-01806
位置：mod-tome.lua:24158；section：mod-tome/data/talents/cursed/endless-hunt.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Harass your stalked victim with two quick attacks for %d%% (at 0 Hate) to %d%% (at 100+ Hate) damage each. Each attack that scores a hit disrupts one talent, rune or infusion for %d turns. Your opponent will be unnerved by the attacks, reducing the damage they deal by %d%% for %d turns.

		This talent will also attack with your shield, if you have one equipped.
```
译文：
```text
用两次快速的攻击折磨你追踪的目标，每次攻击造成 %d%% （0仇恨）～ %d%% （100+仇恨）的伤害。并且每次攻击都将干扰目标某项技能、纹身或符文，持续 %d 回合。目标会因为你的攻击而气馁，它的伤害降低 %d%%，持续 %d 回合。

		如果你装备了盾牌，这一技能也会用你的盾牌攻击。
```

## entry-01807
位置：mod-tome.lua:24168；section：mod-tome/data/talents/cursed/endless-hunt.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Let hate fuel your movements. While active, you gain %d%% movement speed. The recklessness of your movement brings you bad luck (Luck -3).
		Cleave, Repel and Surge cannot be active simultaneously, and activating one will place the others in cooldown.
		Sustaining Surge while Dual Wielding grants %d additional Defense.
		Movement speed and dual-wielding Defense both increase with the Willpower stat.
```
译文：
```text
让杀意激发你敏捷的身手，提高你 %d%% 移动速度。不顾一切的移动会带给你厄运（-3 幸运）。
		分裂攻击、无所畏惧和杀意涌动不能同时开启，并且激活其中一个也会使另外两个进入冷却。
		双持武器时，杀意涌动还会提高你 %d 的闪避。
		移动速度和双持时的闪避增益受意志加成。
```

## entry-01808
位置：mod-tome.lua:24182；section：mod-tome/data/talents/cursed/fears.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instill fear in your foes within %d radius of a target location dealing %0.2f mind and %0.2f darkness damage and causing one of 4 possible fears that last for %d turns.
		The targets can save vs your Mindpower to resist the effect.
		Fear effects improve with your Mindpower.

		Possible fears are:
		#ORANGE#Paranoid:#LAST# Gives the target an %d%% chance to physically attack a nearby creature, friend or foe. If hit, their target will be afflicted with Paranoia as well.
		#ORANGE#Despair:#LAST# Reduces mind resist, mindsave, armour and defence by %d.
		#ORANGE#Terrified:#LAST# Deals %0.2f mind and %0.2f darkness damage per turn and increases cooldowns by %d%%.
		#ORANGE#Haunted:#LAST# Causes the target to suffer %0.2f mind and %0.2f darkness damage for each detrimental mental effect every turn.
		
```
译文：
```text
将恐惧注入目标 %d 半径范围内的敌人中，造成 %0.2f 精神和 %0.2f 暗影伤害，并随机造成 4 种可能的恐惧效果之一，持续 %d 回合。
		目标可以与你的精神强度对抗，以抵抗恐惧效果。
		恐惧效果受精神强度加成。

		可能的恐惧效果如下所示：
		#ORANGE#妄想症：#LAST# 目标有 %d%% 几率使用物理攻击附近的生物，不管它是敌对还是友方生物。如果击中了目标，目标也会感染妄想症。
		#ORANGE#绝望：#LAST# 精神伤害抗性，精神豁免，护甲值和闪避各降低 %d。
		#ORANGE#惊惧：#LAST# 每回合受到 %0.2f 精神和 %0.2f 暗影伤害，技能冷却时间增加 %d%%。
		#ORANGE#恶灵缠身：#LAST# 目标每有一个负面精神效果，则每回合受到 %0.2f 精神和 %0.2f 暗影伤害。
```

## entry-01809
位置：mod-tome.lua:24201；section：mod-tome/data/talents/cursed/fears.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Heighten the fears of those near to you. Any foe you attempt to inflict a fear upon and who remains in a radius of %d and in sight of you for %d (non-consecutive) turns, will take %0.2f mind and %0.2f darkness damage and gain a new fear that lasts for %d turns.
			This effect completely ignores fear resistance, but can be saved against.
```
译文：
```text
加深你周围敌人的恐惧。所有被你灌注恐惧的目标若停留在你视野内，并且和你距离不超过 %d，这样累计达到 %d 回合时，受到 %0.2f 精神和 %0.2f 暗影伤害，并获得一个新的持续 %d 回合的恐惧效果。
			这一效果无视恐惧抗性，但可以被豁免。
```

## entry-01810
位置：mod-tome.lua:24205；section：mod-tome/data/talents/cursed/fears.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Impose your tyranny on the minds of those who fear you. When a foe gains a new fear, you have a %d%% chance to increase the duration of their heightened fear and one random existing fear effect by %d turns, to a maximum of 8 turns.
		Additionally, you gain %d Mindpower and Physical power for 5 turns every time you apply a fear, stacking up to %d times.
```
译文：
```text
将你的专制施加于畏惧你的敌人的心智。当一个敌人获得一个新的恐惧效果时，你有 %d%% 的几率将其强化恐惧以及另一个随机的已有恐惧效果的持续时间延长 %d 回合，最多 8 回合。
		此外，每当你恐惧一个目标，你获得 %d 精神强度和物理强度，持续 5 回合，最多叠加 %d 层。
```

## entry-01811
位置：mod-tome.lua:24211；section：mod-tome/data/talents/cursed/fears.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Panic your enemies within a range of %d for %d turns. Anyone who fails to make a mental save against your Mindpower has a %d%% chance each turn of trying to run away from you.
```
译文：
```text
使 %d 范围内的敌人惊慌失措，持续 %d 回合，任何未能通过精神豁免抵抗你的精神强度的敌人，每回合将有 %d%% 概率试图逃离你。
```

## entry-01812
位置：mod-tome.lua:24218；section：mod-tome/data/talents/cursed/force-of-will.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# was blasted into #Target#!
```
译文：
```text
#Source#撞向#Target#！
```

## entry-01813
位置：mod-tome.lua:24222；section：mod-tome/data/talents/cursed/force-of-will.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Focusing your hate, you strike your foe with unseen force for %d damage and %d knockback.
		In addition, your ability to channel force with this talent increases all critical damage by %d%% (currently: %d%%)
		Damage increases with your Mindpower.
```
译文：
```text
专注你的仇恨，你用无形的力量打击敌人造成 %d 点伤害和 %d 码击退效果。
		此外，你灌注力量的能力使你增加 %d%% 所有暴击伤害。（当前：%d%%）
		伤害受精神强度加成。
```

## entry-01814
位置：mod-tome.lua:24229；section：mod-tome/data/talents/cursed/force-of-will.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You have deflected %d incoming damage!
```
译文：
```text
你偏转了%d所受伤害！
```

## entry-01815
位置：mod-tome.lua:24230；section：mod-tome/data/talents/cursed/force-of-will.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Create a barrier that siphons hate from you at the rate of 0.2 a turn. The barrier will deflect 50%% of incoming damage with the force of your will, up to %d damage. The barrier charges at a rate of 1/%d of its maximum charge per turn.
		In addition, your ability to channel force with this talent increases all critical damage by %d%% (currently: %d%%)
		The maximum damage deflected increases with your Mindpower.
```
译文：
```text
用你的意志力折射 50%% 的伤害。你可以折射最多 %d 点伤害，护盾值每回合回复最大值的 1/%d（技能激活时-0.2仇恨值回复）。
		你灌注力量的能力使你增加 %d%% 所有暴击伤害。（当前：%d%%）
		最大伤害折射值受精神强度加成。
```

## entry-01816
位置：mod-tome.lua:24242；section：mod-tome/data/talents/cursed/force-of-will.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your fury becomes an unseen force that randomly lashes out at foes around you. For %d turns you strike %d (%d%% chance for %d) nearby target(s) within range %d doing %d damage and %d knockback. The number of extra strikes increases at higher talent levels.
		In addition, your ability to channel force with this talent increases all critical damage by %d%% (currently: %d%%)
		Damage increases with your Mindpower.
```
译文：
```text
你的愤怒变成一股无形之力，猛烈鞭笞你附近的随机敌人。在 %d 回合内，你将攻击 %d （%d%% 概率攻击 %d）个半径 %d 以内的敌人，造成 %d 点伤害并击退 %d 码。额外攻击的数目随技能等级增长。
		你灌注力量的能力使你增加 %d%% 所有暴击伤害。（当前：%d%%）
		伤害受精神强度加成。
```

## entry-01817
位置：mod-tome.lua:24273；section：mod-tome/data/talents/cursed/gestures.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#F53CBE##Source# lashes back at #Target#!
```
译文：
```text
#F53CBE##Source#反击#Target#！
```

## entry-01818
位置：mod-tome.lua:24274；section：mod-tome/data/talents/cursed/gestures.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You guard against melee damage with a sweep of your hand. So long as you can use Gestures (Requires two free or mindstar-equipped hands), you deflect up to %d damage (%0.1f%% of your best free hand melee damage) from up to %0.1f melee attack(s) each turn (based on your cunning). Deflected attacks cannot be crits.
		If Gesture of Pain is active, you also have a %0.1f%% chance to counterattack.
```
译文：
```text
你通过手势来防御近战伤害。只要你能使用手势（要求两只手都可用于手势，每只手须为空手或装备灵晶），你最多偏移 %d 点伤害（你的单手最大伤害的 %0.1f%%），每回合最多触发 %0.1f 次（基于你的灵巧）。成功防御的攻击不会暴击。
		如果痛苦手势被激活，你将有 %0.1f%% 的概率发动反击。
```

## entry-01819
位置：mod-tome.lua:24313；section：mod-tome/data/talents/cursed/one-with-shadows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your awareness extends to your shadows.
		You always know exactly where your shadows are and can perceive any foe within %d tiles of their vision.
```
译文：
```text
你的意识延伸到阴影上。
		你能清晰的感知到阴影的位置，同时还能感知到阴影视野 %d 码范围内的敌人。
```

## entry-01820
位置：mod-tome.lua:24317；section：mod-tome/data/talents/cursed/one-with-shadows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You empathy with your shadows causes the line between you and your shadows to blur.
		You lose %d%% light resistance, but gain %d%% darkness resistance and affinity. You also gain %0.2f%% all resistance for each shadow in your party.
```
译文：
```text
你与阴影之间的共鸣，使彼此的界限逐渐模糊。
		你的光系伤害抗性变化 %d%%，并获得 %d%% 暗影伤害抗性和伤害亲和。你的队伍里每有一个阴影，就获得 %0.2f%% 所有伤害抗性。
```

## entry-01821
位置：mod-tome.lua:24321；section：mod-tome/data/talents/cursed/one-with-shadows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Observers find it difficult to tell you and your shadows apart.
		You can target a shadow in radius %d and instantly trade places with it.
		%d random negative physical or magical effects are transferred from you to the chosen shadow in the process.
```
译文：
```text
现在，其他人很难分清你和阴影。
		 你能选择半径 %d 范围内的一个阴影并和它交换位置。
		同时至多 %d 个随机负面物理或魔法效果会被转移至选择的阴影身上。
```

## entry-01822
位置：mod-tome.lua:24352；section：mod-tome/data/talents/cursed/predator.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While shrouded in cursed miasma you gain stealth (%d power) and %d physical power.
		The stealth power and physical power will increase with your mindpower.
```
译文：
```text
当你被包裹在诅咒瘴气中时，你获得潜行 (%d 强度)，并获得 %d 物理强度。
		潜行强度和物理强度受精神强度加成。
```

## entry-01823
位置：mod-tome.lua:24366；section：mod-tome/data/talents/cursed/primal-magic.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Selects a displacement location...
```
译文：
```text
选择一个转移目标…
```

## entry-01824
位置：mod-tome.lua:24370；section：mod-tome/data/talents/cursed/primal-magic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Years of magic have permeated your skin leaving it resistant to the physical world. Your armor is increased by %d.
		The bonus will increase with the Magic stat.
```
译文：
```text
魔法渗透进你的皮肤，使之能抵御外部世界的侵蚀。护甲值增加 %d。
		增益效果受魔力值加成。
```

## entry-01825
位置：mod-tome.lua:24398；section：mod-tome/data/talents/cursed/punishments.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sear your hatred into the mind of a target, dealing escalating Mind damage each turn over %d turns. The victim will suffer %0.1f damage on the first turn, slowly increasing up to %0.1f damage on the last, dealing %d Mind damage in total. Re-applying the effect resets the damage escalation. The victim has a 25%% chance of suffering Brainlock each turn from the unbearable pain.

The damage increases with your Mindpower.
```
译文：
```text
将你的憎恨灼入目标的心智，在 %d 回合内每回合造成不断升级的精神伤害。第一回合会造成 %0.1f 点精神伤害并在最后 1 回合增加至 %0.1f 点，总计 %d 点精神伤害。重复施加这一效果会把伤害值重置为初始伤害值。
被影响的敌人每回合有 25%% 概率附加思维封锁效果。

伤害受精神强度加成。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
knockback	击退	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Knockback Resistance；战斗日志“%s抵抗了击退！”
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
