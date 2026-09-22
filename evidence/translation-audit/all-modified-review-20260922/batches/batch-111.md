# batch-111：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03565
位置：tome-cults.lua:2626；section：tome-cults/data/talents/demented/calamity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your touch carries an entropic curse, marking your victims for a terrible fate. Each time you deal damage to a target, they are Jinxed for 5 turns. This stacks up to 10 times, reducing saves and defense by %0.2f and critical strike chance by %0.2f%%.
			This can only be applied once per target per turn and will fade entirely if you break line of sight with your target for more than 2 turns.
```
译文：
```text
你的触碰伴随着熵之诅咒，为目标带来悲惨的命运。每当你对目标造成伤害时，目标将被厄运诅咒 5 回合。厄运可以叠加 10 层，每层减少 %0.2f 豁免和闪避，%0.2f%% 暴击率。
		每个目标每回合只能受到一层诅咒。如果在过去 2 回合里目标消失在你的视线中，所有诅咒都会消退。
```

## entry-03566
位置：tome-cults.lua:2632；section：tome-cults/data/talents/demented/calamity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you apply Jinx to an enemy, you have a %d%% chance to siphon some of their luck for yourself for 5 turns. This stacks up to 10 times, increasing saves and defense by %0.2f and critical strike chance by %0.2f%%.
		If you know Preordain, stacks beyond 6 also grant a %d%% chance for you to entirely avoid damage taken.
```
译文：
```text
每当你向敌人施加厄运诅咒，有 %d%% 几率吸取敌人的运气为你所用，持续 5 回合。这个效果最多叠加 10 层，每层增加 %0.2f 豁免和闪避，%0.2f%% 暴击率。
		如果你同时学会了命中注定，六层以上的每层幸运使你获得 %d%% 几率完全避免受到的伤害。
```

## entry-03567
位置：tome-cults.lua:2647；section：tome-cults/data/talents/demented/chronophage.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are surrounded by a vortex of entropic energy that feeds on the timelines of others. Each time you cast a spell random targets in radius 10 begin rapidly aging and decaying, reducing all stats by %d for 8 turns, stacking up to %d times.
			Up to %d stacks total will be applied to enemies each cast with a max of 2 stacks on the same target.
```
译文：
```text
吸收他人时间的熵能漩涡围绕着你。当你释放法术时，半径 10 格内的随机目标将迅速老化、凋零，所有属性降低 %d，持续 8 回合，效果可叠加 %d 层。
			每次施法可以释放最多 %d 层加速衰老，但同一目标一次最多增加 2 层效果。
```

## entry-03568
位置：tome-cults.lua:2670；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You use your bond with horrors to summon three decaying devourers for %d turns.
The decaying horrors cannot move and will attack all hostile creatures around them. They possess the talents Bloodbath, Gnashing Teeth and Frenzied Bite.
All its primary stats will be set to %d (based on your Magic stat), life rating increased by %d, and all talent levels set to %d.  Many other stats will scale with level.
Your increased damage, damage penetration, critical strike chance, and critical strike multiplier stats will all be inherited.
```
译文：
```text
你利用和恐魔的联系召唤三个持续 %d 轮的腐败的吞噬者。
		腐败的吞噬者不能移动，能攻击周围所有敌对生物。它们拥有浴血奋战、咬牙切齿和狂乱撕咬技能。
		它们的所有主属性将设为 %d（基于你的魔法属性），生命成长增加 %d，所有技能等级设为 %d。许多其他属性与技能等级相关。
		它们将继承你的伤害加成、伤害抗性穿透、暴击几率和暴击伤害系数。
```

## entry-03569
位置：tome-cults.lua:2680；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You use your bond with horrors to summon a decaying bloated horror for %d turns.
The decaying horror cannot move and will attack all hostile creatures in range of it. It possesses the talents Mind Disruption and Mind Sear.
All its primary stats will be set to %d (based on your Magic stat), life rating increased by %d, and all talent levels set to %d.  Many other stats will scale with level.
Your increased damage, damage penetration, critical strike chance, and critical strike multiplier stats will all be inherited.
		
```
译文：
```text
你利用和恐魔的联系召唤一个持续 %d 回合的腐败的浮肿恐魔。
		腐败的恐魔不能移动，能攻击范围内的所有敌对生物。它拥有精神干扰和精神光束技能。
		它们的所有主属性将设为 %d（基于你的魔法属性），生命成长增加 %d，所有技能等级设为 %d。许多其他属性与技能等级相关。
		它们将继承你的伤害加成、伤害抗性穿透、暴击几率和暴击伤害系数。
		
```

## entry-03570
位置：tome-cults.lua:2691；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You forcefully try to turn a creature into an horror.
If the target fails a magical save against your Spellpower, its appearance turns into that of a horror for %d turns, making all other creatures hostile to it.
Enemies near the target will have their target cleared on application.
This spell does not work on horrors.
```
译文：
```text
你强行让一个生物变化为恐魔。
		如果目标生物未能通过魔法豁免，%d 回合内它的相貌将转变为恐魔，令周围其他生物与之敌对。
		目标生物周围的敌人将重新考虑其攻击目标。
		该法术对恐魔无效。
```

## entry-03571
位置：tome-cults.lua:2699；section：tome-cults/data/talents/demented/controlled-horrors.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You attune your horrors to the dead god Amakthel, increasing your summoned horrors damage by %d%%.
At talent level 3, your Decaying Devourers spell will summon 4 additional Devourers adjacent to random enemies nearby and your Bloated Horror will learn the Agony talent.
At talent level 5, victims of your Horrific Display spell will pull enemies in radius 10 1 space towards them each turn.
The damage increase is based on your Spellpower.
```
译文：
```text
你将你的恐魔和已死之神阿马克泰尔同化，增加恐魔 %d%% 伤害。
		技能等级 3 后，你的腐败的吞噬者法术将额外召唤四名吞噬者在随机敌人周围，你的浮肿恐魔将学会极度痛苦。
		技能等级 5 后，恐怖展示的受害者每回合会把范围 10 码内的敌人拉近 1 码。
伤害加成受法术强度加成。
```

## entry-03572
位置：tome-cults.lua:2762；section：tome-cults/data/talents/demented/disfigured-face.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your tongue turns into a diseased tentacle that you use to #{italic}#lick#{normal}# enemies in a cone.
		Licked creatures take %d%% tentacle damage that ignores armor and get sick, gaining a random disease for %d turns that deals %0.2f blight damage per turn and reduces strength, dexterity or constitution by %d.
		
		If at least one enemy is hit you gain %d insanity.
		
		Disease damage will increase with your Spellpower.
```
译文：
```text
你的舌头化作疫病触手，让你能 #{italic}#舔舐#{normal}# 锥形范围内的敌人。
		被舔舐的敌人受到无视护甲的 %d%% 触手伤害并获得一种持续 %d 回合的随机疾病，每回合造成 %0.2f 枯萎伤害并减少力量、敏捷或体质 %d 点。
		如果你至少命中了一名敌人，你获得 %d 疯狂值。
		疾病伤害受法术强度加成。
```

## entry-03573
位置：tome-cults.lua:2767；section：tome-cults/data/talents/demented/disfigured-face.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your face melts, exploding in a targeted gush of blood and gore dealing %0.2f darkness damage (%0.2f total) in a cone over 5 turns.
		Each turn the target will be dealt an additional %0.2f blight damage per disease.
		Damage will increase with your Spellpower.
```
译文：
```text
你的脸融化，爆炸喷射出一团血肉，对锥形范围内敌人造成 %0.2f 暗影伤害，持续 5 回合（总伤害 %0.2f）。
		每回合目标身上的每种疾病将使其受到额外 %0.2f 枯萎伤害。
		伤害受法术强度加成。
```

## entry-03574
位置：tome-cults.lua:2783；section：tome-cults/data/talents/demented/disfigured-face.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whenever you use a disfigured face power you show a glimpse of what True Horror is.
		If the affected targets fail a spell save they become frightened for 2 turns, giving them a %d%% chances to fail using talents.
		When a target becomes afraid it bolsters you to see their anguish, increasing your darkness and blight damage penetration by %d%% for 2 turns.
		The values will increase with your Spellpower.
```
译文：
```text
每次你使用该系技能时，你就能展现何为真正的恐怖。
		如果目标未能通过法术豁免，将处于 2 回合恐惧状态，使用技能有 %d%% 几率失败。
		同时，敌人的恐惧和痛苦能激励你的意志，在 2 回合内增加你 %d%% 暗影和枯萎伤害抗性穿透。
		技能效果受法术强度加成。
```

## entry-03575
位置：tome-cults.lua:2826；section：tome-cults/data/talents/demented/doom.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Weave your chosen prophecy into your speech, dooming your foe twice over. The chosen prophecy will apply instantly to your primary target whenever you cast any other prophecy at talent level %d.
		A prophecy can only be affected by one of Grand Oration, Twofold Curse or Revelation.
		
		Current prophecy: %s
```
译文：
```text
对你的听众施加双重诅咒。每当你施加其他预言时，你选择的预言将同时施加给主要目标 (技能等级 %d)。
		同一种预言只能以一种方式进行强化，隆重演说，双重诅咒或者天启。
		当前预言 : %s
```

## entry-03576
位置：tome-cults.lua:2830；section：tome-cults/data/talents/demented/doom.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
As you speak the chosen prophecy whispers from the void guide you in how to bring about the downfall of your foe. The chosen prophecy will grant one of the following effects.
		Prophecy of Madness. Each time the target uses a talent one of your talents on cooldown has its cooldown reduced by %d turns.
		Prophecy of Ruin. Each time the target takes damage you are healed for %d%% of the damage dealt.
		Prophecy of Treason: %d%% of all damage you take is redirected to a random target affected by Prophecy of Treason.
		A prophecy can only be affected by one of Grand Oration, Twofold Curse or Revelation.
	
		Current prophecy: %s
```
译文：
```text
当你宣读预言时，来自虚空的回响将指引你带来敌人的末日。你选择的预言将提供以下三种加成之一。
		疯狂预言：每次目标使用技能时，你的一个技能的冷却时间将减少 %d。
		毁灭预言：每次目标受到伤害时，你回复 %d%% 伤害值。
		背叛预言：你受到的 %d%% 伤害将转移至周围随机受背叛预言影响的目标。

		同一种预言只能以一种方式进行强化，隆重演说，双重诅咒或者天启。
		当前预言 : %s
```

## entry-03577
位置：tome-cults.lua:2843；section：tome-cults/data/talents/demented/entropy.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# pulls #Target# in!
```
译文：
```text
#Source#将#Target#拉了进来！
```

## entry-03578
位置：tome-cults.lua:2858；section：tome-cults/data/talents/demented/entropy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
On casting Entropic Gift, a radius 1 rift in spacetime will be opened underneath the target for %d turns, increasing in radius by 1 each turn to a maximum of %d.
		All caught within the rift are pulled towards the center and take %0.2f darkness and %0.2f temporal damage, plus %d%% of your total entropy each turn (currently %d).
```
译文：
```text
每次释放熵之礼物，会在目标处产生一个持续 %d 回合的一格小型黑洞，每回合半径增加 1 直到 %d。
		所有范围内的生物每回合将被拉向黑洞中心并受到 %0.2f 暗影、%0.2f 时空伤害以及你当前熵的 %d%% 的伤害（当前 %d）。
```

## entry-03579
位置：tome-cults.lua:2862；section：tome-cults/data/talents/demented/entropy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You empower your spells with dangerous levels of entropic energy, increasing your darkness and temporal damage by %d%% and resistance penetration by %d%% at the cost of suffering %0.2f entropic backlash for each non-instant spell.
```
译文：
```text
你用危险的熵能大幅强化你的法术，增加 %d%% 黑暗和时空伤害与 %d%% 抗性穿透。
			作为代价，每个非瞬间法术会带来 %0.2f 熵能反冲。
```

## entry-03580
位置：tome-cults.lua:2869；section：tome-cults/data/talents/demented/friend-of-the-worm.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Link to the summoner.
```
译文：
```text
链接到召唤者。
```

## entry-03581
位置：tome-cults.lua:2881；section：tome-cults/data/talents/demented/friend-of-the-worm.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You invoke a long standing pact with a fellow horror, a Worm that Walks, to help you in your travels.
		You can fully control, level, and equip it.
		Using this spell will ressurect your friendly horror if it died, giving it back %d%% life.
		Higher raw talent levels will give your horror more equipment slots:

		Level 1:  Mainhand, Offhand
		Level 2:  Body
		Level 3:  Belt
		Level 4:  Ring, Ring
		Level 5:  Ring, Ring, Trinket

		To change your horror's equipment and talents first transfer the equipment from your inventory then take control of it.
```
译文：
```text
你激活同蠕虫合体的契约，令其帮助你。
		你可以完全控制、升级、更换它的装备和技能。
		使用该法术将复活已死亡的单位，使其获得 %d%% 生命。
		原始技能等级提升将带来更多装备格：
		等级 1：主手 /副手武器
		等级 2：躯体
		等级 3：腰带
		等级 4：戒指 /戒指
		等级 5：戒指 /戒指/ 饰品

		试图改变其装备时，先将装备交给它，再切换控制。
```

## entry-03582
位置：tome-cults.lua:2906；section：tome-cults/data/talents/demented/friend-of-the-worm.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You and your Worm that Walks both teleport to an enemy in range %d and make a melee attack for %d%% damage.
			Your Worm that Walks' Blindside talent cooldown is reduced by %d.
```
译文：
```text
你和蠕虫合体同时传送至 %d 内的目标处，造成 %d%% 近战伤害。
		你的蠕虫合体的闪电突袭技能冷却时间减少 %d。
```

## entry-03583
位置：tome-cults.lua:2910；section：tome-cults/data/talents/demented/friend-of-the-worm.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You establish a powerful mental link with your Worm that Walks.
		As long as you remain within radius 3 of your worm that walks each of you gains %d%% all resistance for 5 turns.
		Additionally, your Worm that Walks permanently gains an inscription slot every 2 raw talent levels (%d).
```
译文：
```text
你和蠕虫合体建立强大的精神链接。
		只要你和它的距离不超过 3 格，你们均获得持续 5 回合的 %d%% 全体抗性。
		该技能每增加两级原始等级，你的蠕虫合体获得一个纹身位（当前：%d）。
```

## entry-03584
位置：tome-cults.lua:2917；section：tome-cults/data/talents/demented/friend-of-the-worm.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While within range 3 of your Worm that Walks you can project an aura of terror.
		At the sight of two maddening horrors fighting together all your foes in radius %d must make a physical save against your spellpower or be stunned for %d turns.

		Additionally your Shared Insanity effect will cause enemies in radius 3 to lose %d spell save and %d defense for 3 turns.
```
译文：
```text
当你处于蠕虫合体 3 格范围内时，你可以制造恐怖光环。
		看到两个疯狂恐魔并肩作战将令周围 %d 格的敌人震慑 %d 回合，除非它们的物理豁免成功对抗了你的法术强度。
		此外，你的共享疯狂效果将令 3 格内的敌人在 3 回合里失去 %d 法术豁免和 %d 闪避。
```

## entry-03585
位置：tome-cults.lua:2955；section：tome-cults/data/talents/demented/madness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Terrible visions and maddening voices fill the minds of enemies within a radius %d area, inflicting %0.2f darkness damage each turn for 5 turns. In addition, this distraction will reduce physical, spell and mindpower of those affected by %d.
The power loss caused by this spell can stack, to a maximum of %d powers.
		The effect will increase with your Spellpower.
```
译文：
```text
令半径 %d 格内的敌人的心灵里充满可怕的幻觉和疯狂的低语，5 回合内每回合受到 %0.2f 暗影伤害。同时，该效果将使其物理强度、法术强度和精神强度各降低 %d 点，该效果可叠加至最多 %d 点。
		技能效果受法术强度加成。
```

## entry-03586
位置：tome-cults.lua:2965；section：tome-cults/data/talents/demented/madness.lua；source_tag：tformat；args_order：[2, 1]；special：None

原文：
```text
When a hallucination from Hideous Visions is slain, it unleashes a psychic shriek dealing %0.2f darkness damage to enemies in radius %d.
```
译文：
```text
每当“惊骇幻象”产生的幻象被消灭时，它将释放心灵冲击，对 %d 格内的敌人造成 %0.2f 暗影伤害。
```

## entry-03587
位置：tome-cults.lua:2967；section：tome-cults/data/talents/demented/madness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Raise your Dark Whispers in radius %d to a deafening crescendo for %d turns, applying another stack and drowning out all thought. 
			Targets afflicted by Dark Whispers will have 20%% higher chance to spawn hallucinations, and each time they take damage from your Dark Whispers or Sanity Warp they will take an additional %d%% damage as temporal damage.
		The damage will improve with your Spellpower.
```
译文：
```text
使 %d 格内的黑暗低语音量提升 %d 回合，达到震耳欲聋的地步，额外施加一层低语效果，同时干扰一切思考能力。
		被黑暗低语影响的目标产生幻象的几率增加 20%%，每次受到黑暗低语或失智冲击的伤害时，会受到额外 %d%% 时空伤害。
		伤害受法术强度加成。
```

## entry-03588
位置：tome-cults.lua:2980；section：tome-cults/data/talents/demented/nether.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire a beam of energy that rakes across the ground, dealing %0.2f darkness damage to enemies within and leaving behind an unstable rift. After 3 turns the rift detonates, dealing %0.2f temporal damage to adjacent enemies.
		Targets cannot be struck by more than a single rift explosion at once.
		The power of this spell inflicts entropic backlash on you, causing you to take %d damage over 8 turns. This damage counts as entropy for the purpose of Entropic Gift.
		The damage will increase with your Spellpower.
```
译文：
```text
发射一束扫射大地的能量，造成 %0.2f 暗影伤害，并产生不稳定的裂缝。3 回合后裂缝湮灭并对周围敌人造成 %0.2f 时空伤害。
		一次湮灭不能多次伤害同一目标。
		该法术会对你产生熵能反冲，在 8 回合内造成 %d 伤害。此伤害对熵之礼物而言视为熵。
		伤害受法术强度加成。
```

## entry-03589
位置：tome-cults.lua:2988；section：tome-cults/data/talents/demented/nether.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select a teleport location...
```
译文：
```text
选择传送位置…
```

## entry-03590
位置：tome-cults.lua:2989；section：tome-cults/data/talents/demented/nether.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles on %s!
```
译文：
```text
法术在 %s 上失败了！
```

## entry-03591
位置：tome-cults.lua:2990；section：tome-cults/data/talents/demented/nether.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s is swallowed by a portal!
```
译文：
```text
#CRIMSON#%s被传送门吞噬！
```

## entry-03592
位置：tome-cults.lua:2991；section：tome-cults/data/talents/demented/nether.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the warp!
```
译文：
```text
%s抵抗了传送！
```

## entry-03593
位置：tome-cults.lua:2994；section：tome-cults/data/talents/demented/nether.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Briefly open a radius %d rift in spacetime that teleports those within to the targeted location. Enemies will take %0.2f darkness and %0.2f temporal damage.
		The power of this spell inflicts entropic backlash on you, causing you to take %d damage over 8 turns. This damage counts as entropy for the purpose of Entropic Gift.
		The damage will improve with your Spellpower.
```
译文：
```text
在时空中临时打开半径 %d 的裂缝，将范围内目标传送至指定位置。
		敌人将受到 %0.2f 暗影 %0.2f 时空伤害。
		该法术会对你产生熵能反冲，在 8 回合内造成 %d 伤害。此伤害对熵之礼物而言视为熵。
		伤害受法术强度加成。
```

## entry-03594
位置：tome-cults.lua:3001；section：tome-cults/data/talents/demented/nether.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you cast a non-instant Demented spell, a nether spark begins orbiting around you for 10 turns, to a maximum of 5. Each spark increases your critical strike chance by %d%%, and on reaching 5 sparks your next Nether spell will consume all sparks to empower itself:
#PURPLE#Netherblast:#LAST# Becomes a deadly lance of void energy, piercing through enemies and dealing an additional %d%% damage over 5 turns.
#PURPLE#Rift Cutter:#LAST# Those in the rift will be pinned for %d turns, take %0.2f temporal damage each turn, and the rift explosion has %d increased radius.
#PURPLE#Spatial Distortion:#LAST# An Entropic Maw will be summoned at the rift's exit for %d turns, pulling in and taunting nearby targets with it's tendrils.
The damage will increase with your Spellpower.  Entropic Maw stats will increase with level and your Magic stat.
```
译文：
```text
每次你施放非瞬发的疯狂法术时，一朵彼世火花将环绕在你周围 10 回合，上限为 5 朵。
		每个火花增加你 %d%% 暴击率。当你拥有 5 个火花时，你的下一次虚空法术将消耗所有火花来获得强化效果。
#PURPLE#彼世冲击：#LAST# 成为穿透性虚空能量，并在 5 回合内造成额外 %d%% 伤害。
#PURPLE#裂缝切割：#LAST# 裂缝内的敌人将定身 %d 回合，每回合受到 %0.2f 时空伤害。裂缝湮灭时爆炸半径增加 %d。
#PURPLE#空间扭曲：#LAST# 裂缝出口处产生一个持续 %d 回合的熵之胃，能用触须拉近并嘲讽附近的目标。
伤害受法术强度加成。
熵之胃的属性受等级和魔法属性加成。
```

## entry-03595
位置：tome-cults.lua:3019；section：tome-cults/data/talents/demented/oblivion.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your entropy bleeds into the world around you. On having entropic backlash applied or increased to you, %d random enemies you can see within radius 10 will be shrouded in entropic forces for 8 turns. This increases the duration of new negative effects and reduces the duration of new beneficial effects applied to the target by %d%%.
```
译文：
```text
将你身体上的熵能向周围辐射。每当你受到熵能反冲时，在你半径 10 码内随机的 %d 个可见敌人都将被熵能侵蚀 8 回合。
		增加（减少）它们受到的新的负面（正面）效果 %d%% 的持续时间。
```

## entry-03596
位置：tome-cults.lua:3049；section：tome-cults/data/talents/demented/oblivion.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Slam your weapons into the ground, creating a radius 2 explosion of void energy dealing %d%% damage split between darkness and temporal.
```
译文：
```text
用武器撞击地面，产生 2 码的虚空爆炸，造成 %d%% 虚空武器伤害（暗影时空各 50%%）。
```

## entry-03597
位置：tome-cults.lua:3084；section：tome-cults/data/talents/demented/rift.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (empowered)
```
译文：
```text
%s（强化）
```

## entry-03598
位置：tome-cults.lua:3093；section：tome-cults/data/talents/demented/rift.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-03599
位置：tome-cults.lua:3097；section：tome-cults/data/talents/demented/rift.lua；source_tag：tformat；args_order：[1, 3, 2]；special：None

原文：
```text
You briefly open a tunnel through spacetime, teleporting to a void rift in range %d. This destroys the rift, granting you a shield for %d turns absorbing %d damage.
		The damage absorbed will scale with your Spellpower
```
译文：
```text
你短暂地在时空中打开一个通道，传送到范围 %d 内的一个虚空裂隙。这将摧毁那个虚空裂隙，使你获得一个护盾，吸收 %d 点伤害，持续 %d 回合。
		护盾吸收的伤害随法术强度提高而提高。
```

## entry-03600
位置：tome-cults.lua:3107；section：tome-cults/data/talents/demented/rift.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Pouring more energy into your rifts, you have a %d%% chance for each one to instead appear as a more powerful type.
#PURPLE#Nether Breach:#LAST# Fires a beam dealing %0.2f darkness damage at a random target in radius 10.
#PURPLE#Temporal Vortex:#LAST# Inflicts %0.2f temporal damage each turn to enemies in radius 4 and reduces their global speed by 30%%.
#PURPLE#Dimensional Gate:#LAST# Has a 50%% chance each turn to summon a voidling lasting %d turns; a fast melee attacker that can teleport.
The stats of your Void Skitterers will scale with your Magic stat and level.
```
译文：
```text
向你的裂隙注入能量，你将有 %d%% 概率让每一个裂口进化成为更强大的形态。
#PURPLE#彼世裂隙：#LAST# 向半径 10 内随机敌人发射光束，造成 %0.2f 暗影伤害。
#PURPLE#时空漩涡：#LAST# 每回合对半径 4 内的敌人造成 %0.2f 时空伤害，并使其整体速度降低 30%%。
#PURPLE#维度之门 :#LAST# 每回合有 50%% 概率召唤一个虚空造物，持续 %d 回合，是一个能传送的高速近战攻击者
你的虚空造物属性随你的等级和魔法属性提高而提高。
```

## entry-03601
位置：tome-cults.lua:3117；section：tome-cults/data/talents/demented/rift.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s's Dimensional Skitter fizzles!
```
译文：
```text
%s的维度迅击失败了！
```

## entry-03602
位置：tome-cults.lua:3120；section：tome-cults/data/talents/demented/rift.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You draw power from the depths of the void causing your Reality Fracture to enhance any existing rifts.
#GREY#Void Rift:#LAST# Deals %d%% increased damage and projectiles explode in radius 1.
#PURPLE#Nether Breach:#LAST# Deals %d%% increased damage and chains to 3 targets.
#PURPLE#Temporal Vortex:#LAST# Deals %d%% increased damage, radius increased by 1, and slow increased to 50%%.
#PURPLE#Dimensional Gate:#LAST# Voidling Skitterers will be frenzied, increasing their global speed by %d%%.
```
译文：
```text
你从虚空深处汲取能量，每当你激活实境撕裂时，你可以强化任何已存在的裂隙。
#GREY#虚空裂隙 :#LAST# 造成 %d%% 额外伤害，并且投射物在半径 1 范围内爆炸。
#PURPLE#彼世裂隙：#LAST# 造成 %d%% 额外伤害，并且连锁至 3 个额外目标。
#PURPLE#时空漩涡：#LAST# 造成 %d%% 额外伤害，效果半径增加 1，并且减速效果提高至 50%%。
#PURPLE#维度之门 :#LAST# 虚空造物将会变得狂暴，增加他们 %d%% 的整体速度。
```

## entry-03603
位置：tome-cults.lua:3162；section：tome-cults/data/talents/demented/slow-death.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Choose a talent to use:
```
译文：
```text
选择一个技能使用：
```

## entry-03604
位置：tome-cults.lua:3171；section：tome-cults/data/talents/demented/slow-death.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The pain you inflict to the victim you are digesting is so intense something breaks inside it, giving you a way into its mind.
		When you digest you can steal a random talent from your victim and can use it for yourself at talent level %d.
		At talent level 5 you can choose which talent to use.
		You may not steal a talent which you already know.
		The stolen talent will not use any resources to activate.
		
```
译文：
```text
正在被你消化的目标承受着极大的痛苦，内部器官不断破损，让你能趁机侵入它的思维。
		你可以窃取并使用它的一个随机技能（技能等级 %d）。
		技能等级 5 时，你可以指定窃取的技能。
		你不能窃取你已知的技能。
		窃取的技能使用时不消耗资源。
		
```

## 相关术语快照
```tsv
Blindside	闪电突袭	T.GAME.TALENT	talents	talent name	preferred	core	技能会以极快速度瞬移至目标身边并攻击；按机制译作“闪电突袭”，不按普通动词字面译作“偷袭”
Breach	破防	T.GAME.TALENT	talents	_t	preferred	core	与技能名“破防”一致的效果/状态显示名（+破防/-破防）
Breach	破防	T.GAME.TALENT	talents	talent name	preferred	core	时空战斗系主动技能：通过降低护甲强度和震慑、定身、致盲、混乱免疫来突破防御，而非毁灭目标；不得译为“破灭”
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Demented	疯狂系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业类别名
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mind Sear	心灵灼烧	T.GAME.TALENT	talents	talent name	preferred	core	sear 指灼烧；技能机制虽为射线，名称不增译“光束”
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demented	疯狂	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
entropy	熵	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
entropy	熵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mainhand	主手	T.GAME.ENTITY	items	nil	existing	core	
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nether	彼世	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
offhand	副手	T.GAME.ENTITY	items	nil	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
prophecy	预言	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
