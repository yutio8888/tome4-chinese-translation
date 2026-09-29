# batch-068：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02108
位置：mod-tome.lua:27481；section：mod-tome/data/talents/psionic/kinetic-mastery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Build telekinetic power and dump it into an adjacent creature or yourself.
		This will launch them to a targeted location in radius %d.

		Launched enemies take %0.1f Physical damage and are stunned for %d turns upon landing.
		When the target lands, creatures within radius 2 take %0.1f Physical damage and are knocked away from you.
		This talent ignores %d%% of the knockback resistance of the thrown target, which takes half damage if it resists being thrown.

		When used on yourself, you will launch in a straight line, knocking enemies flying and doing %0.1f Physical damage to each.
		You can break through %d walls while doing this.
		The damage and range increases with Mindpower.
```
译文：
```text
使用你的念动力，将其灌注到一个相邻的生物或你自己身上。
		将其投掷到 %d 码范围内的目标位置。

		被投掷的敌人落地时受到 %0.1f 物理伤害，并被震慑 %d 回合。
		目标落地时，半径 2 格内的生物受到 %0.1f 物理伤害，并被击退远离你。
		这个技能无视被投掷目标 %d%% 的击退抗性，若目标抵抗投掷则只受到一半伤害。

		对你自己使用时，你会沿直线飞出，将沿途敌人撞飞并对每个造成 %0.1f 物理伤害。
		你在此过程中能撞穿 %d 面墙壁。
		伤害和距离随精神强度提升。
```

## entry-02109
位置：mod-tome.lua:27517；section：mod-tome/data/talents/psionic/mental-discipline.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your expertise in the art of energy projection grows.
		Aura cooldowns are all reduced by %d turns. Aura damage drains energy more slowly (+%0.2f damage required to lose a point of energy).
```
译文：
```text
你增加了在灵能值运用方面的知识。
		所有光环的冷却时间减少 %d 回合。光环消耗灵能值变的更慢（消耗每点灵能值所需伤害值 +%0.2f）。
```

## entry-02110
位置：mod-tome.lua:27521；section：mod-tome/data/talents/psionic/mental-discipline.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your expertise in the art of energy absorption grows. Shield cooldowns are all reduced by %d turns, the amount of damage absorption required to gain a point of energy is reduced by %0.1f, and the maximum energy you can gain from each shield is increased by %0.1f per turn.
```
译文：
```text
你增加了在灵能值吸收方面的知识。所有护盾的冷却时间减少 %d 回合。护盾额外增加灵能值所需伤害值减少 %0.1f，每个护盾的最大能量吸收量增加 %0.1f 每回合。
```

## entry-02111
位置：mod-tome.lua:27525；section：mod-tome/data/talents/psionic/mental-discipline.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A life of the mind has had predictably good effects on your Willpower and Cunning.
		Increases Willpower and Cunning by %d.
```
译文：
```text
过着心智生活自然会对你的意志和灵巧大有裨益。
		增加 %d 点意志和灵巧。
```

## entry-02112
位置：mod-tome.lua:27533；section：mod-tome/data/talents/psionic/mentalism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Resonate with psionic, nature, and anti-magic powered objects you wear, increasing your physical and mind power by %0.1f or %d%% of the object's material level (whichever is lower).
		This effect stacks and applies for each qualifying object worn.
		Current bonus: %d
```
译文：
```text
与你装备着的具有灵能、自然或反魔力量的物品产生共鸣，增加你 %0.1f 点或 %d%% 物品材质等级数值（取较小值）的物理和精神强度。
		此效果可以叠加，并且适用于所有符合条件的已穿戴装备。
		当前加成：%d
```

## entry-02113
位置：mod-tome.lua:27540；section：mod-tome/data/talents/psionic/mentalism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Clears your mind of current mental effects, and blocks additional ones over 6 turns.  At most, %d mental effects will be affected.
```
译文：
```text
净化你当前所有的精神状态，并在接下来的 6 回合内免疫新增的精神状态。最多一共（净化和免疫）能影响 %d 种精神状态。
```

## entry-02114
位置：mod-tome.lua:27542；section：mod-tome/data/talents/psionic/mentalism.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to invoke your spirit!
```
译文：
```text
没有足够的空间召唤你的投影！
```

## entry-02115
位置：mod-tome.lua:27545；section：mod-tome/data/talents/psionic/mentalism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate to project your mind from your body for %d turns.  In this state you're invisible (+%d power), can see invisible and stealthed creatures (+%d detection power), can move through walls, and do not need air to survive.
		All damage you suffer is shared with your physical body, and while in this form you may only deal damage to 'ghosts' or through an active mind link (mind damage only in the second case.)
		To return to your body, simply release control of the projection.
```
译文：
```text
激活此技能可以使你的灵魂出窍，持续 %d 回合。在此效果下，你处于隐形状态（+%d 强度），并且可以看到隐形和潜行单位（+%d 侦查强度），还可以穿过墙体，并且无需呼吸。
		你受到的所有伤害都会与身体共享，当你处于此形态下你只能对“鬼魂”类怪物造成伤害，或者通过激活一种精神通道来造成伤害。
		注：后一种情况下只能造成精神伤害。
		要回到你的身体里，只需释放灵魂体的控制即可。
```

## entry-02116
位置：mod-tome.lua:27552；section：mod-tome/data/talents/psionic/mentalism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Link minds with the target.  While your minds are linked, you'll inflict %d%% more mind damage to the target and gain telepathy for its creature type.
		Only one mindlink can be maintained at a time, and the effect will break if the target dies or goes beyond range (%d)).
		The mind damage bonus will scale with your Mindpower.
```
译文：
```text
用精神通道连接目标。当精神通道连接时，你对其造成的精神伤害增加 %d%%，同时你可以感知与目标同种类型的单位。
		在同一时间内只能激活一条精神通道，当目标死亡或超出范围（%d 码）时，通道中断。
		受精神强度影响，精神伤害按比例加成。
```

## entry-02117
位置：mod-tome.lua:27576；section：mod-tome/data/talents/psionic/nightmare.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Brings the target's inner demons to the surface.  Each turn, for %d turns, there's a %d%% chance that a demon will surface, requiring the target to make a Mental Save to keep it from manifesting.
		If the target is sleeping, the chance to save will be halved, and fear immunity will be ignored.  Otherwise, if the summoning is resisted, the effect will end early.
		The summon chance will scale with your Mindpower and the demon's life will scale with the target's rank.
		If a demon manifests the sheer terror will remove all sleep effects from the victim, but not the Inner Demons.
```
译文：
```text
使目标的心魔浮现。在 %d 回合内，每回合有 %d%% 的几率会召唤一个心魔，需要目标进行一次精神豁免鉴定，失败则心魔具现化。
		如果目标处于睡眠状态，豁免概率减半，且无视目标的恐惧免疫。若目标未处于睡眠状态且豁免鉴定成功，则心魔的效果提前结束。
		受精神强度影响，召唤几率按比例加成。
		心魔的生命值受目标分级加成。
		心魔具现化时，会移除目标身上的所有睡眠类效果，本技能除外。
```

## entry-02118
位置：mod-tome.lua:27602；section：mod-tome/data/talents/psionic/other.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Telekinetically grasp which item?
```
译文：
```text
念力之握抓握哪件物品？
```

## entry-02119
位置：mod-tome.lua:27603；section：mod-tome/data/talents/psionic/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s telekinetically seizes: %s.
```
译文：
```text
%s用念力装备了%s。
```

## entry-02120
位置：mod-tome.lua:27604；section：mod-tome/data/talents/psionic/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Telekinetically grasp a weapon or gem using mentally-directed forces, holding it aloft and bringing it to bear with the power of your mind alone.
		Note: The normal restrictions on worn equipment do not apply to this item.
```
译文：
```text
用精神引导的念动力抓握一件武器或宝石，将其举起悬浮在空中，仅凭意念之力操控使用。
		请注意：通常装备物品的一些限制不适用于这样装备的物品。
```

## entry-02121
位置：mod-tome.lua:27608；section：mod-tome/data/talents/psionic/other.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source#'s mindstar telekinetically grabs #target#!
```
译文：
```text
#Source#的灵晶念力抓取了#target#！
```

## entry-02122
位置：mod-tome.lua:27609；section：mod-tome/data/talents/psionic/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s telekinetically grabs %s!
```
译文：
```text
%s念力抓取了%s！
```

## entry-02123
位置：mod-tome.lua:27610；section：mod-tome/data/talents/psionic/other.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require a telekinetically wielded weapon or gem for your psionic focus.
```
译文：
```text
你需要念力武器或者宝石来使用灵能聚焦。
```

## entry-02124
位置：mod-tome.lua:27612；section：mod-tome/data/talents/psionic/other.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Allows you to wield a physical melee or ranged weapon, a mindstar or a gem telekinetically, gaining a special effect for each.
		A gem will provide a +3 bonus to all primary stats per tier of the gem.
		A mindstar will randomly try to telekinetically grab a far away foe (10% chance and range 3 for a tier 1 mindstar, +1 range and +5% chance for each tier above 1) and pull it into melee range.
		A physical melee weapon will act as a semi independant entity, automatically attacking adjacent foes each turn, while a ranged weapon will fire at your target whenever you perform a ranged attack.
		While this talent is active, all melee and ranged attacks use 60% of your Cunning and Willpower in place of Dexterity and Strength for accuracy and damage calculations respectively.
		

		
```
译文：
```text
允许你用念力装备一件物理近战或远程武器、灵晶或宝石，不同物品会获得不同效果。
		宝石：每一级材质等级使所有主要属性增加 3 点。
		灵晶：一级材质时有 10% 几率抓取 3 格内的远处敌人；材质等级每提高一级，范围增加 1 格、几率增加 5%，并将其拉入近战范围。
		物理近战武器：作为半独立实体，每回合自动攻击相邻敌人；远程武器：每当你发动远程攻击时，自动射击你的目标。
		激活时，所有近战和远程攻击在计算命中与伤害时，分别以 60% 灵巧替代敏捷、以 60% 意志替代力量。


		
```

## entry-02125
位置：mod-tome.lua:27629；section：mod-tome/data/talents/psionic/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The telekinetically-wielded ranged weapon uses Willpower in place of Strength, and Cunning in place of Dexterity, to determine Accuracy and damage respectively.
			Combat stats:
			Range: %d
			Accuracy: %d
			Damage: %d
			APR: %d
			Crit: %0.1f%%
			Speed: %0.1f%%
```
译文：
```text
念动远程武器使用意志和灵巧来分别代替力量和敏捷，以决定命中和伤害。
			战斗属性：
			范围：%d
			命中：%d
			伤害：%d
			护甲穿透：%d
			暴击率：%0.1f%%
			攻击速度：%0.1f%%
```

## entry-02126
位置：mod-tome.lua:27644；section：mod-tome/data/talents/psionic/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The telekinetically-wielded weapon uses Willpower in place of Strength, and Cunning in place of Dexterity, to determine damage and Accuracy respectively.
			Combat stats:
			Accuracy: %d
			Damage: %d
			APR: %d
			Crit: %0.2f
			Speed: %0.2f
```
译文：
```text
念动武器使用意志和灵巧来分别代替力量和敏捷，以决定伤害和命中。
			战斗属性：
			命中：%d
			伤害：%d
			护甲穿透：%d
			暴击率：%0.2f
			速度：%0.2f
```

## entry-02127
位置：mod-tome.lua:27664；section：mod-tome/data/talents/psionic/projection.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fills the air around you with reactive currents of force.
		If you have a gem or mindstar in your psionically wielded slot, this will do %0.1f Physical damage to all adjacent enemies, costing %0.1f energy per creature. 
		If you have a conventional weapon in your psionically wielded slot, this will add %0.1f Physical damage to all your weapon hits, costing %0.1f energy per hit.
		When deactivated, if you have at least %d energy, a massive spike of kinetic energy is released as a range %d beam, smashing targets for up to %d physical damage and sending them flying.
		#{bold}#Activating the aura takes no time but de-activating it does.#{normal}#
		To turn off an aura without spiking it, deactivate it and target yourself. The damage will improve with your Mindpower.
		You can only have two of these auras active at once.
```
译文：
```text
将你周围的空气充满能量力场。
		如果你的灵能武器槽佩戴的是宝石或者灵晶，会对所有相邻的敌人造成 %0.1f 的物理伤害，每个生物消耗 %0.1f 能量。
		如果你的灵能武器槽佩戴的是武器，每次攻击附加 %0.1f 的物理伤害，每次攻击消耗 %0.1f 能量。
		当关闭该技能时，如果你拥有最少 %d 点能量，巨大的动能会释放为一个射程为 %d 的射线，击打目标，造成高达 %d 的物理伤害，并击飞他们。
		#{bold}#激活光环是不消耗时间的，但是关闭它则需要消耗时间。#{normal}#
		如果要关闭光环且不发射射线，关闭它并选择你自己为目标。伤害随着精神强度而增长。
		你同时只能激活两种此类光环。
```

## entry-02128
位置：mod-tome.lua:27692；section：mod-tome/data/talents/psionic/projection.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fills the air around you with crackling energy.
		If you have a gem or mindstar in your psionically wielded slot, this will do %0.1f Lightning damage to all adjacent enemies, costing %0.1f energy per creature. 
		If you have a conventional weapon in your psionically wielded slot, this will add %0.1f Lightning damage to all your weapon hits, costing %0.1f energy per hit.
		When deactivated, if you have at least %d energy, a massive spike of electrical energy jumps between up to %d nearby targets, doing up to %0.1f Lightning damage to each with a 50%% chance of dazing them.
		#{bold}#Activating the aura takes no time but de-activating it does.#{normal}#
		To turn off an aura without spiking it, deactivate it and target yourself. The damage will improve with your Mindpower.
		You can only have two of these auras active at once.
```
译文：
```text
将你周围的空气充满噼啪响的电能。
		如果你的灵能武器槽佩戴的是宝石或灵晶，会对所有相邻的敌人造成 %0.1f 的闪电伤害，每个生物消耗 %0.1f 能量。
		如果你的灵能武器槽佩戴的是武器，每次攻击附加 %0.1f 的闪电伤害，每次攻击消耗 %0.1f 能量。
		当关闭该技能时，如果你拥有最少 %d 点能量，巨大的电能会释放为在最多 %d 个邻近目标间跳跃的闪电，对每个目标造成至多 %0.1f 的闪电伤害，且 50%% 的概率令他们眩晕。
		#{bold}#激活光环是不消耗时间的，但是关闭它则需要消耗时间。#{normal}#
		如果要关闭光环且不发射射线，关闭它并选择你自己为目标。伤害随着精神强度而增长。
		你同时只能激活两种此类光环。
```

## entry-02129
位置：mod-tome.lua:27720；section：mod-tome/data/talents/psionic/psi-archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Use telekinetic forces to greatly augment the durability and tension of your bow in order to fire an arrow with velocity unmatched by even the mightiest mundane archers. Increases armor penetration by %d, and deals %d%% damage.
```
译文：
```text
使用精神灵能以增强弓的耐久和张力，使射出的箭矢拥有连最强大的普通弓手都无法企及的飞行速度。增加 %d 点护甲穿透并造成 %d%% 伤害。
```

## entry-02130
位置：mod-tome.lua:27776；section：mod-tome/data/talents/psionic/psi-fighting.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s shatters %s shield!
```
译文：
```text
#CRIMSON#%s粉碎了%s的护盾！
```

## entry-02131
位置：mod-tome.lua:27790；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Absorb damage and gain energy.
```
译文：
```text
吸收伤害并获得能量。
```

## entry-02132
位置：mod-tome.lua:27792；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Project energy to damage foes.
```
译文：
```text
投射能量以伤害敌人。
```

## entry-02133
位置：mod-tome.lua:27794；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Wield melee weapons with mentally-manipulated forces.
```
译文：
```text
用意志力来控制近战武器。
```

## entry-02134
位置：mod-tome.lua:27802；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Pull energy from your surroundings.
```
译文：
```text
从你周围吸收能量。
```

## entry-02135
位置：mod-tome.lua:27806；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Various psionic talents.
```
译文：
```text
多种灵能技能。
```

## entry-02136
位置：mod-tome.lua:27816；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Distort reality with your mental energy.
```
译文：
```text
使用你的精神力量扭曲现实。
```

## entry-02137
位置：mod-tome.lua:27818；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Call the dream-forge hammer to smite your foes.
```
译文：
```text
召唤梦之巨锤碾碎你的敌人。
```

## entry-02138
位置：mod-tome.lua:27820；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Manifest your enemies nightmares.
```
译文：
```text
将敌人的噩梦具现化。
```

## entry-02139
位置：mod-tome.lua:27822；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Directly attack your opponents minds.
```
译文：
```text
直接攻击敌人的心灵。
```

## entry-02140
位置：mod-tome.lua:27824；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Force enemies into a deep sleep.
```
译文：
```text
使敌人进入昏睡。
```

## entry-02141
位置：mod-tome.lua:27826；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Nothing exists outside the minds ability to perceive it.
```
译文：
```text
没有任何事物能逃脱精神力量的感知。
```

## entry-02142
位置：mod-tome.lua:27828；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Manifest your thoughts as psionic summons.
```
译文：
```text
使你的思维具象化形成灵能召唤术。
```

## entry-02143
位置：mod-tome.lua:27832；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Manipulate the sleep cycles of yourself and your enemies.
```
译文：
```text
操纵你自己和敌人的睡眠。
```

## entry-02144
位置：mod-tome.lua:27834；section：mod-tome/data/talents/psionic/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Various mind based effects.
```
译文：
```text
许多精神系技能效果。
```

## entry-02145
位置：mod-tome.lua:27849；section：mod-tome/data/talents/psionic/psychic-assault.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Inflicts %0.2f mind damage and cripples the target's higher mental functions, reducing cunning by %d and confusing (%d%% power) the target for %d turns.
		The damage, cunning penalty, and confusion power will scale with your Mindpower.
```
译文：
```text
造成 %0.2f 精神伤害，并严重损害目标的高级心智功能，降低 %d 灵巧并混乱目标（%d%% 强度），持续 %d 回合。
		受精神强度影响，伤害、灵巧降幅和混乱强度按比例加成。
```

## entry-02146
位置：mod-tome.lua:27885；section：mod-tome/data/talents/psionic/slumber.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You feel it unwise to travel to the dreamscape in such a fragile form.
```
译文：
```text
你感觉以如此脆弱的形态前往梦境并不明智。
```

## entry-02147
位置：mod-tome.lua:27888；section：mod-tome/data/talents/psionic/slumber.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The spell fizzles...
```
译文：
```text
法术失败了……
```

## 相关术语快照
```tsv
Accuracy:	命中：	T.GAME.STAT	combat	_t	existing	core	带冒号的界面标签
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
dreamscape	梦境空间	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
ghost	幽灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	
knockback	击退	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Knockback Resistance；战斗日志“%s抵抗了击退！”
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
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
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
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
