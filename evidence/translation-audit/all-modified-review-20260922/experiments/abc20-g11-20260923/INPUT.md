# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03573–entry-03612 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g11-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

## 判断依据与范围

1. 原文/译文及身份以本包和 entries.json 为准；邻近译文仅来自同目录 context.lua。术语只用本包末尾子集；按 source_tag/category/语境匹配，existing 不是强制改名依据。不得读取当前翻译文件、其他实验文件、SPEC/STATE、历史报告或生产结论。
2. 游戏机制以可核验的实际源码行为为准。本体固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC使用source-access列明且哈希固定的公开快照，源码仓库/commit未固定，必须显式标注。DLC机制疑点可陈述快照内已证事实，但目标版本适用性缺口保留待确认，不将引擎commit套用DLC。缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认。英文、术语或旧译不能覆盖源码；沿袭上游的误述和翻译新增分开，不仅凭变量名猜机制。
3. 可读本INPUT、entries.json、context.lua、source-access.json及其中sections列明的本组sources文件。可在这些单文件内搜索。源码缺失已明确列在unavailable_components，不把其他组件同名代码当作它的证据。
4. 追调用链时，本体只能git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<明确相关的单文件path>；DLC只能读取source-access中dlc_additional_sources列明、哈希匹配的相关单文件。每个新增文件说明哪个已读调用/符号/require引入。禁止当前源码工作树、其他commit、整目录git grep/rg/find或历史审核查找；不能读取共享DLC快照中的locales等其他语言答案。证据不足写待确认。
5. 不把问题扩大为全局重命名或术语策略。格式结合实际显示/参数消费判断：保留source_tag、args_order、special；占位符、标记及段落/换行差异只有导致错误参数、错误显示或信息结构丢失时才算缺陷。合法排版和等价重排不算缺陷。

## 四类判定（按以下顺序合并一条内的多个claim）

- **存在问题**：至少一个有可核验证据的错误或遗漏，涉及事实、作用对象/所属关系、数量/条件/范围/时序、玩家操作、语义信息、明确适用的术语要求或运行时格式。轻微并不自动变为建议；必须解释具体哪项信息错误或丢失，不因可自行猜出原意便忽略。
- **待确认**：没有已证实问题，但有具体疑点因证据不足无法定论。指出缺哪项证据。不得把待确认当未发现问题。
- **仅建议**：没有上述问题或未决疑点，仅更自然的措辞、个人偏好、无损排版等；不得将建议计作缺陷。
- **未发现问题**：无上述三类事项。

一条同时有已证实问题和待确认claim，总判定为存在问题，但须分别列出各claim状态。若只有建议和未决claim，总判定为待确认。不同条目重复同一问题仍分别覆盖；同条重复表述不重复计claim。

## 输出

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03573 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


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

## entry-03605
位置：tome-cults.lua:3200；section：tome-cults/data/talents/demented/tentacles.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your left hand mutates into a disgusting mass of tentacles.
		When you have your offhand empty you automatically hit your target and those on the side whenever you hit with a basic attack.
		Also increases Physical Power by %d, and increases weapon damage by %d%% for your tentacles attacks.
		Each time you make an attack with your tentacle you gain %d insanity.
		You generate a low power psionic field around you when around #{italic}#'civilized people'#{normal}# that prevents them from seeing you for the horror you are.

		Your tentacle hand currently has these stats%s:
		%s
```
译文：
```text
你的左手异变成为一坨恶心的触手。
		副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。
		物理强度提高 %d，触手武器伤害提高 %d%%。
		每次触手攻击时，获得 %d 疯狂值。
		附近有 #{italic}# 普通人 #{normal}# 时会自动生成微弱的心灵护盾，避免被他们发现你的恐魔形态。
		你的触手当前属性为 %s :
		%s
```

## entry-03606
位置：tome-cults.lua:3214；section：tome-cults/data/talents/demented/tentacles.lua；source_tag：_t；args_order：None；special：None

原文：
```text
, #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#
```
译文：
```text
，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#
```

## entry-03607
位置：tome-cults.lua:3237；section：tome-cults/data/talents/demented/tentacles.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s's tentacle fails to move %s!
```
译文：
```text
%s的触手无法移动%s！
```

## entry-03608
位置：tome-cults.lua:3260；section：tome-cults/data/talents/demented/timethief.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Release a surge of entropy, cleansing yourself of afflictions while draining the energy from others. All enemies in range 10 will have the duration of %d beneficial effects reduced by %d turns, while you will have an equal number of detrimental effects reduced by the same duration.
```
译文：
```text
释放熵的浪潮，清除自己的灾祸，同时吸取他人的能量。10 码内所有敌人的 %d 项有益效果持续时间缩短 %d 回合。自身同等数量的有害效果持续时间缩短同等回合。
```

## entry-03609
位置：tome-cults.lua:3266；section：tome-cults/data/talents/demented/timethief.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03610
位置：tome-cults.lua:3280；section：tome-cults/data/talents/demented/void.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must be wearing light armor for this talent.
```
译文：
```text
你必须穿着轻甲才能使用这一技能。
```

## entry-03611
位置：tome-cults.lua:3282；section：tome-cults/data/talents/demented/void.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#FIREBRICK##Target#'s void star absorbs the damage from #Source#, converting it into entropy!#LAST#
```
译文：
```text
#FIREBRICK##Target#的虚空之星吸收了来自#Source#的伤害，将其转化为熵！#LAST#
```

## entry-03612
位置：tome-cults.lua:3284；section：tome-cults/data/talents/demented/void.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjure void stars that orbit you, defending you from incoming attacks. Each time an attack deals more than 10%% of your maximum life, a star will be consumed to reduce the damage taken by %d%%, of which 40%% will be dealt to you as entropic backlash.
		You regenerate 1 star every %d turns, stacking up to 4 times.
		This talent will only function in light armor.
```
译文：
```text
形成围绕你旋转，为你抵御伤害的虚空之星。
		每当受到超过 10%% 最大生命的伤害时，消耗一颗虚空之星，使受到的伤害减少 %d%%，自己受到等同于减免伤害 40%% 的熵能反冲。
		虚空之星每经过 %d 回合自动恢复一颗。
		此技能只有装备轻甲时生效。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Blindside	闪电突袭	T.GAME.TALENT	talents	talent name	preferred	core	技能会以极快速度瞬移至目标身边并攻击；按机制译作“闪电突袭”，不按普通动词字面译作“偷袭”
Breach	破防	T.GAME.TALENT	talents	_t	preferred	core	与技能名“破防”一致的效果/状态显示名（+破防/-破防）
Breach	破防	T.GAME.TALENT	talents	talent name	preferred	core	时空战斗系主动技能：通过降低护甲强度和震慑、定身、致盲、混乱免疫来突破防御，而非毁灭目标；不得译为“破灭”
Demented	疯狂系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业类别名
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
cleansing	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key；同 cohort 的 cleanse 运行键亦采用“洁净”；不约束其他语境
cleansing 	洁净的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的前缀名称；保留 source 尾空格；不约束技能、伤害类型、日志或叙事中的 cleansing
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demented	疯狂	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
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
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
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
tentacles	触手	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
