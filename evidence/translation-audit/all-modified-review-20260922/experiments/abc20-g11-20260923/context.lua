section "tome-cults/data/talents/demented/disfigured-face.lua"

t("Diseased Tongue", "疫病之舌", "talent name")
t("Your tongue turns into a diseased tentacle that you use to #{italic}#lick#{normal}# enemies in a cone.\n\t\tLicked creatures take %d%% tentacle damage that ignores armor and get sick, gaining a random disease for %d turns that deals %0.2f blight damage per turn and reduces strength, dexterity or constitution by %d.\n\t\t\n\t\tIf at least one enemy is hit you gain %d insanity.\n\t\t\n\t\tDisease damage will increase with your Spellpower.", [[你的舌头化作疫病触手，让你能 #{italic}#舔舐#{normal}# 锥形范围内的敌人。
		被舔舐的敌人受到无视护甲的 %d%% 触手伤害并获得一种持续 %d 回合的随机疾病，每回合造成 %0.2f 枯萎伤害并减少力量、敏捷或体质 %d 点。
		如果你至少命中了一名敌人，你获得 %d 疯狂值。
		疾病伤害受法术强度加成。]], "tformat")
t("Dissolved Face", "溶解之脸", "talent name")
t([[Your face melts, exploding in a targeted gush of blood and gore dealing %0.2f darkness damage (%0.2f total) in a cone over 5 turns.
		Each turn the target will be dealt an additional %0.2f blight damage per disease.
		Damage will increase with your Spellpower.]], [[你的脸融化，爆炸喷射出一团血肉，对锥形范围内敌人造成 %0.2f 暗影伤害，持续 5 回合（总伤害 %0.2f）。
		每回合目标身上的每种疾病将使其受到额外 %0.2f 枯萎伤害。
		伤害受法术强度加成。]], "tformat")
t("Writhing Hairs", "蜿蜒之发", "talent name")
t([[For a brief moment horrific hairs grow on your head, each of them ending with a creepy eye.
		You use those eyes to gaze upon a target area, creatures caught inside partially turn to stone reducing their movement speed by %d%% and making them brittle for 7 turns.
		Brittle targets have a 35%% chance for any damage they take to be increased by %d%%.
		This cannot be saved against.
		]], [[短时间内你的头上生长出恐怖的头发，每根头发的末梢长着一只令人毛骨悚然的眼睛。
		你用这些眼睛凝视目标区域，部分石化范围内目标，降低其 %d%% 移速并使其处于 7 回合的脆弱状态。
		脆弱状态的目标每次受到伤害时有 35%% 几率增加 %d%% 伤害。
		该效果不能被豁免。
		]], "tformat")
t("Glimpse of True Horror", "恐怖无边", "talent name")
t([[Whenever you use a disfigured face power you show a glimpse of what True Horror is.
		If the affected targets fail a spell save they become frightened for 2 turns, giving them a %d%% chances to fail using talents.
		When a target becomes afraid it bolsters you to see their anguish, increasing your darkness and blight damage penetration by %d%% for 2 turns.
		The values will increase with your Spellpower.]], [[每次你使用该系技能时，你就能展现何为真正的恐怖。
		如果目标未能通过法术豁免，将处于 2 回合恐惧状态，使用技能有 %d%% 几率失败。
		同时，敌人的恐惧和痛苦能激励你的意志，在 2 回合内增加你 %d%% 暗影和枯萎伤害抗性穿透。
		技能效果受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/doom.lua"

t("Prophecy", "预言", "talent name")
t([[By bringing the forces of entropy to bear on a target, you prophesize their inevitable doom. Each point in this talent unlocks additional prophecies. A target can only be affected by a single prophecy at a time.
Level 1: Prophecy of Ruin. Deals %0.2f damage on falling below 75%%, 50%% or 25%% of maximum life.
Level 3: Prophecy of Treason. %d%% chance each turn to attack an ally or themselves.
Level 5: Prophecy of Madness. Increases talent cooldowns by %d%%.]], [[对目标释放熵能力量，你预言了它无可避免的末日。随着技能等级提升，你能解锁更多预言。同一目标不能同时处于两种预言下。
技能等级 1：毁灭预言。当生命值降低至最大生命的 75%%，50%% 或 25%% 下时，造成 %0.2f 伤害。
技能等级 3：背叛预言。每回合有 %d%% 几率攻击友方单位或自身。
技能等级 5：疯狂预言。增加 %d%% 技能冷却时间。]], "tformat")
t("Prophecy of Madness", "疯狂预言", "talent name")
t([[Utter a prophecy of the impending madness of your target, increasing the cooldown of all their talents by %d%% for 6 turns.
		A target can only be affected by a single prophecy at a time.]], [[对目标施加疯狂预言，增加 %d%% 技能冷却时间，持续 6 回合。
		一个目标只能同时被一个预言影响。]], "tformat")
t("Prophecy of Ruin", "毁灭预言", "talent name")
t([[Utter a prophecy of the impending demise of your target that lasts 6 turns.
		Each time their life falls below 75%%, 50%% or 25%% of maximum the power of the prophecy will echo outwards, inflicting %0.2f darkness damage to them.
		A target can only be affected by a single prophecy at a time.
		The damage increase will increase with your Spellpower.]], [[对目标施加毁灭预言，持续 6 回合。
		当生命值降低至最大生命的 75%%，50%% 或 25%% 下时，造成 %0.2f 暗影伤害。
		一个目标只能同时被一个预言影响。
		伤害受法术强度加成。]], "tformat")
t("Prophecy of Treason", "背叛预言", "talent name")
t("%s(%d treason)#LAST#", "%s(%d 背叛)#LAST#", "tformat")
t([[Utter a prophecy of the impending treachery of your target. For the next 6 turns, they will have a %d%% each turn to waste their turn attempting to attack an adjacent creature for 10%% weapon damage, or even themself if no creature is present.
		A target can only be affected by a single prophecy at a time.]], [[对目标施加背叛预言，持续 6 回合。每回合有 %d%% 几率攻击临近单位，造成10%%武器伤害，如果没有其他单位则攻击自身。
		一个目标只能同时被一个预言影响。]], "tformat")
t("Grand Oration", "隆重演说", "talent name")
t("None", "无", "_t")
t("You speak a chosen prophecy to the masses. When applying this prophecy, it will spread to all targets in radius %d.\n\t\tA prophecy can only be affected by one of Grand Oration, Twofold Curse or Revelation.\n\t\t\n\t\tCurrent prophecy: %s", [[你隆重地宣读某种预言，令其在周围 %d 格内传播。
		同一种预言只能以一种方式进行强化，隆重演说，双重诅咒或者天启。

		当前预言 : %s]], "tformat")
t("Twofold Curse", "双重诅咒", "talent name")
t("Weave your chosen prophecy into your speech, dooming your foe twice over. The chosen prophecy will apply instantly to your primary target whenever you cast any other prophecy at talent level %d.\n\t\tA prophecy can only be affected by one of Grand Oration, Twofold Curse or Revelation.\n\t\t\n\t\tCurrent prophecy: %s", [[对你的听众施加双重诅咒。每当你施加其他预言时，你选择的预言将同时施加给主要目标 (技能等级 %d)。
		同一种预言只能以一种方式进行强化，隆重演说，双重诅咒或者天启。
		当前预言 : %s]], "tformat")
t("Revelation", "天启", "talent name")
t("As you speak the chosen prophecy whispers from the void guide you in how to bring about the downfall of your foe. The chosen prophecy will grant one of the following effects.\n\t\tProphecy of Madness. Each time the target uses a talent one of your talents on cooldown has its cooldown reduced by %d turns.\n\t\tProphecy of Ruin. Each time the target takes damage you are healed for %d%% of the damage dealt.\n\t\tProphecy of Treason: %d%% of all damage you take is redirected to a random target affected by Prophecy of Treason.\n\t\tA prophecy can only be affected by one of Grand Oration, Twofold Curse or Revelation.\n\t\n\t\tCurrent prophecy: %s", [[当你宣读预言时，来自虚空的回响将指引你带来敌人的末日。你选择的预言将提供以下三种加成之一。
		疯狂预言：每次目标使用技能时，你的一个技能的冷却时间将减少 %d。
		毁灭预言：每次目标受到伤害时，你回复 %d%% 伤害值。
		背叛预言：你受到的 %d%% 伤害将转移至周围随机受背叛预言影响的目标。

		同一种预言只能以一种方式进行强化，隆重演说，双重诅咒或者天启。
		当前预言 : %s]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/entropy.lua"

t("Entropic Gift", "熵之礼物", "talent name")
t("%s's black hole", "%s的黑洞", "tformat")
t("#Source# pulls #Target# in!", "#Source#将#Target#拉了进来！", "logCombat")
t([[Your unnatural existence causes the fabric of reality to reject your presence. 25%% of all direct healing received damages you in the form of entropic backlash over 8 turns, which is irresistible and bypasses all shields, but cannot kill you.

You may activate this talent to channel your entropy onto a nearby enemy, removing all entropic backlash to inflict darkness and temporal damage equal to %d%% of your entropy over 4 turns.

The damage dealt when applying this to an enemy will increase with your Spellpower.]], [[你作为非自然的存在被现实抗拒。你受到的直接治疗的 25%% 将以熵能反冲的形式在 8 回合内伤害自身，这种伤害不可抗拒、无视所有护盾，但不会致死。
		你可以主动开启该技能，将你身上的熵转移给附近的一名敌人，除去所有熵能反冲并对其造成持续 4 回合的黑暗和时空伤害，伤害值等于你自身熵能的 %d%%。
		伤害受法术强度加成。]], "tformat")
t("Reverse Entropy", "熵能逆转", "talent name")
t([[Your knowledge of entropy allows you to defy the laws of physics, allowing you to better endure your entropic energies.
			You take %d%% less damage from your entropic backlash.
		You may activate this talent to instantly remove your current Entropy.]], [[你对熵的知识让你可以对抗物理定律，增强你对熵能的承受力。
		你从熵能反冲中受到的伤害减少 %d%%。
		你可以主动开启该技能，瞬间移除当前的熵。]], "tformat")
t("Black Hole", "黑洞", "talent name")
t([[On casting Entropic Gift, a radius 1 rift in spacetime will be opened underneath the target for %d turns, increasing in radius by 1 each turn to a maximum of %d.
		All caught within the rift are pulled towards the center and take %0.2f darkness and %0.2f temporal damage, plus %d%% of your total entropy each turn (currently %d).]], [[每次释放熵之礼物，会在目标处产生一个持续 %d 回合的一格小型黑洞，每回合半径增加 1 直到 %d。
		所有范围内的生物每回合将被拉向黑洞中心并受到 %0.2f 暗影、%0.2f 时空伤害以及你当前熵的 %d%% 的伤害（当前 %d）。]], "tformat")
t("Power Overwhelming", "能量过载", "talent name")
t("You empower your spells with dangerous levels of entropic energy, increasing your darkness and temporal damage by %d%% and resistance penetration by %d%% at the cost of suffering %0.2f entropic backlash for each non-instant spell.", [[你用危险的熵能大幅强化你的法术，增加 %d%% 黑暗和时空伤害与 %d%% 抗性穿透。
			作为代价，每个非瞬间法术会带来 %0.2f 熵能反冲。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/friend-of-the-worm.lua"

t("Worm that Walks Link", "蠕虫合体链接", "talent name")
t("Link to the summoner.", "链接到召唤者。", "_t")
t([[A bulging rotten robe seems to tear at the seams, with masses of bloated worms spilling out all around the moving form.  Two arm-like appendages, each made up of overlapping mucus-drenched maggots, grasp tightly around the handles of bile-coated waraxes.
Each swing drips pustulant fluid before it, and each droplet writhes and wriggles in the air before splashing against the ground.]], [[一件鼓鼓囊囊的长袍，长袍的缝隙里不断蠕动着浮肿的蠕虫。它有着两只臂膀一样的附属物，每只手都由重叠的蠕虫组成，各握着一柄覆有胆汁的斧子。
每次挥舞武器的时，它都会溅出尸僵毒液，每滴毒液在落到地面前都在沸腾和翻滚着。]], "_t")
t("Your worm that walks is out of sight; you cannot establish direct control.", "你的蠕虫合体在视野外。你无法建立直接控制。", "logPlayer")
t("Worm that Walks", "蠕虫合体", "talent name")
t("wtw", "蠕虫合体", "_t")
t("%s (servant of %s)", "%s (%s的仆人)", "tformat")
t("worm that walks (servant of %s)", "蠕虫合体 (%s的仆人)", "tformat")
t("Not enough space to invoke!", "没有足够的空间召唤！", "logPlayer")
t("Robe of the Worm (Improved)", "蠕虫长袍（强化版）", "_t")
t("Your friendly horror is not dead.", "你的恐魔伙伴没死。", "logPlayer")
t([[You invoke a long standing pact with a fellow horror, a Worm that Walks, to help you in your travels.
		You can fully control, level, and equip it.
		Using this spell will ressurect your friendly horror if it died, giving it back %d%% life.
		Higher raw talent levels will give your horror more equipment slots:

		Level 1:  Mainhand, Offhand
		Level 2:  Body
		Level 3:  Belt
		Level 4:  Ring, Ring
		Level 5:  Ring, Ring, Trinket

		To change your horror's equipment and talents first transfer the equipment from your inventory then take control of it.]], [[你激活同蠕虫合体的契约，令其帮助你。
		你可以完全控制、升级、更换它的装备和技能。
		使用该法术将复活已死亡的单位，使其获得 %d%% 生命。
		原始技能等级提升将带来更多装备格：
		等级 1：主手 /副手武器
		等级 2：躯体
		等级 3：腰带
		等级 4：戒指 /戒指
		等级 5：戒指 /戒指/ 饰品

		试图改变其装备时，先将装备交给它，再切换控制。]], "tformat")
t("Foul Convergence", "污秽夹击", "talent name")
t("Your friendly horror is dead.", "你的恐魔伙伴死了。", "logPlayer")
t("%s's teleport fizzles!", "%s的传送失败了！", "logSeen")
t([[You and your Worm that Walks both teleport to an enemy in range %d and make a melee attack for %d%% damage.
			Your Worm that Walks' Blindside talent cooldown is reduced by %d.]], [[你和蠕虫合体同时传送至 %d 内的目标处，造成 %d%% 近战伤害。
		你的蠕虫合体的闪电突袭技能冷却时间减少 %d。]], "tformat")
t("Shared Insanity", "共享疯狂", "talent name")
t([[You establish a powerful mental link with your Worm that Walks.
		As long as you remain within radius 3 of your worm that walks each of you gains %d%% all resistance for 5 turns.
		Additionally, your Worm that Walks permanently gains an inscription slot every 2 raw talent levels (%d).]], [[你和蠕虫合体建立强大的精神链接。
		只要你和它的距离不超过 3 格，你们均获得持续 5 回合的 %d%% 全体抗性。
		该技能每增加两级原始等级，你的蠕虫合体获得一个纹身位（当前：%d）。]], "tformat")
t("Terrible Sight", "恐怖景象", "talent name")
t("You require your worm that walk to be alive and closeby.", "你需要有一个存活的蠕虫合体伙伴在周围。", "logPlayer")
t([[While within range 3 of your Worm that Walks you can project an aura of terror.
		At the sight of two maddening horrors fighting together all your foes in radius %d must make a physical save against your spellpower or be stunned for %d turns.

		Additionally your Shared Insanity effect will cause enemies in radius 3 to lose %d spell save and %d defense for 3 turns.]], [[当你处于蠕虫合体 3 格范围内时，你可以制造恐怖光环。
		看到两个疯狂恐魔并肩作战将令周围 %d 格的敌人震慑 %d 回合，除非它们的物理豁免成功对抗了你的法术强度。
		此外，你的共享疯狂效果将令 3 格内的敌人在 3 回合里失去 %d 法术豁免和 %d 闪避。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/madness.lua"

t("Dark Whispers", "黑暗低语", "talent name")
t([[Terrible visions and maddening voices fill the minds of enemies within a radius %d area, inflicting %0.2f darkness damage each turn for 5 turns. In addition, this distraction will reduce physical, spell and mindpower of those affected by %d.
The power loss caused by this spell can stack, to a maximum of %d powers.
		The effect will increase with your Spellpower.]], [[令半径 %d 格内的敌人的心灵里充满可怕的幻觉和疯狂的低语，5 回合内每回合受到 %0.2f 暗影伤害。同时，该效果将使其物理强度、法术强度和精神强度各降低 %d 点，该效果可叠加至最多 %d 点。
		技能效果受法术强度加成。]], "tformat")
t("Hideous Visions", "惊骇幻象", "talent name")
t("hallucination", "幻象", "_t")
t([[Each time an enemy takes damage from Dark Whispers, there is a %d%% chance for one of their visions to manifest in an adjacent tile for %d turns. This vision takes no actions but the victim will deal %d%% reduced damage to all other targets until the vision is slain.
		A target cannot have more than one hallucination at a time.]], [[每次敌人受到黑暗低语的伤害时，有 %d%% 几率在相邻格子中产生持续 %d 回合的幻象。幻象不能行动，但被影响的敌人在幻象被击杀前造成的伤害降低 %d%%。
		同一敌人同时只能产生一个幻象。]], "tformat")
t("Sanity Warp", "失智冲击", "talent name")
t("When a hallucination from Hideous Visions is slain, it unleashes a psychic shriek dealing %0.2f darkness damage to enemies in radius %d.", "每当“惊骇幻象”产生的幻象被消灭时，它将释放心灵冲击，对 %d 格内的敌人造成 %0.2f 暗影伤害。", "tformat", {2,1})
t("Cacophony", "心灵尖啸", "talent name")
t("Raise your Dark Whispers in radius %d to a deafening crescendo for %d turns, applying another stack and drowning out all thought. \n\t\t\tTargets afflicted by Dark Whispers will have 20%% higher chance to spawn hallucinations, and each time they take damage from your Dark Whispers or Sanity Warp they will take an additional %d%% damage as temporal damage.\n\t\tThe damage will improve with your Spellpower.", [[使 %d 格内的黑暗低语音量提升 %d 回合，达到震耳欲聋的地步，额外施加一层低语效果，同时干扰一切思考能力。
		被黑暗低语影响的目标产生幻象的几率增加 20%%，每次受到黑暗低语或失智冲击的伤害时，会受到额外 %d%% 时空伤害。
		伤害受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/nether.lua"

t("Netherblast", "彼世冲击", "talent name")
t([[Fire a burst of unstable void energy, dealing %0.2f darkness and %0.2f temporal damage to the target. The power of this spell inflicts entropic backlash on you, causing you to take %d damage over 8 turns. This damage counts as entropy for the purpose of Entropic Gift.
		The damage will increase with your Spellpower.]], [[发射一束不稳定的虚空能量，造成 %0.2f 暗影 %0.2f 时空伤害。
		该法术会对你产生熵能反冲，在 8 回合内造成 %d 伤害。此伤害对熵之礼物而言视为熵。
		伤害受法术强度加成。]], "tformat")
t("Rift Cutter", "裂缝切割", "talent name")
t([[Fire a beam of energy that rakes across the ground, dealing %0.2f darkness damage to enemies within and leaving behind an unstable rift. After 3 turns the rift detonates, dealing %0.2f temporal damage to adjacent enemies.
		Targets cannot be struck by more than a single rift explosion at once.
		The power of this spell inflicts entropic backlash on you, causing you to take %d damage over 8 turns. This damage counts as entropy for the purpose of Entropic Gift.
		The damage will increase with your Spellpower.]], [[发射一束扫射大地的能量，造成 %0.2f 暗影伤害，并产生不稳定的裂缝。3 回合后裂缝湮灭并对周围敌人造成 %0.2f 时空伤害。
		一次湮灭不能多次伤害同一目标。
		该法术会对你产生熵能反冲，在 8 回合内造成 %d 伤害。此伤害对熵之礼物而言视为熵。
		伤害受法术强度加成。]], "tformat")
t("Spatial Distortion", "空间扭曲", "talent name")
t("Select a teleport location...", "选择传送位置…", "logPlayer")
t("The spell fizzles on %s!", "法术在 %s 上失败了！", "logSeen")
t("#CRIMSON#%s is swallowed by a portal!", "#CRIMSON#%s被传送门吞噬！", "logSeen")
t("%s resists the warp!", "%s抵抗了传送！", "logSeen")
t("entropic maw", "熵之胃", "_t")
t("Tendrils lash around the mouth of this gigantic beast, seeking prey to devour.", "卷须从怪物的嘴中伸出，正在寻找猎物。", "_t")
t([[Briefly open a radius %d rift in spacetime that teleports those within to the targeted location. Enemies will take %0.2f darkness and %0.2f temporal damage.
		The power of this spell inflicts entropic backlash on you, causing you to take %d damage over 8 turns. This damage counts as entropy for the purpose of Entropic Gift.
		The damage will improve with your Spellpower.]], [[在时空中临时打开半径 %d 的裂缝，将范围内目标传送至指定位置。
		敌人将受到 %0.2f 暗影 %0.2f 时空伤害。
		该法术会对你产生熵能反冲，在 8 回合内造成 %d 伤害。此伤害对熵之礼物而言视为熵。
		伤害受法术强度加成。]], "tformat")
t("Halo of Ruin", "毁灭光环", "talent name")
t([[Each time you cast a non-instant Demented spell, a nether spark begins orbiting around you for 10 turns, to a maximum of 5. Each spark increases your critical strike chance by %d%%, and on reaching 5 sparks your next Nether spell will consume all sparks to empower itself:
#PURPLE#Netherblast:#LAST# Becomes a deadly lance of void energy, piercing through enemies and dealing an additional %d%% damage over 5 turns.
#PURPLE#Rift Cutter:#LAST# Those in the rift will be pinned for %d turns, take %0.2f temporal damage each turn, and the rift explosion has %d increased radius.
#PURPLE#Spatial Distortion:#LAST# An Entropic Maw will be summoned at the rift's exit for %d turns, pulling in and taunting nearby targets with it's tendrils.
The damage will increase with your Spellpower.  Entropic Maw stats will increase with level and your Magic stat.]], [[每次你施放非瞬发的疯狂法术时，一朵彼世火花将环绕在你周围 10 回合，上限为 5 朵。
		每个火花增加你 %d%% 暴击率。当你拥有 5 个火花时，你的下一次虚空法术将消耗所有火花来获得强化效果。
#PURPLE#彼世冲击：#LAST# 成为穿透性虚空能量，并在 5 回合内造成额外 %d%% 伤害。
#PURPLE#裂缝切割：#LAST# 裂缝内的敌人将定身 %d 回合，每回合受到 %0.2f 时空伤害。裂缝湮灭时爆炸半径增加 %d。
#PURPLE#空间扭曲：#LAST# 裂缝出口处产生一个持续 %d 回合的熵之胃，能用触须拉近并嘲讽附近的目标。
伤害受法术强度加成。
熵之胃的属性受等级和魔法属性加成。]], "tformat")
t("Grasping Tendrils", "触须抓取", "talent name")
t("Grab a target and drag it to your side, dealing %d%% weapon damage and taunting it.", "抓住目标，将其拉到身边，造成 %d%% 武器伤害并嘲讽之。", "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/oblivion.lua"

t("Nihil", "空无", "talent name")
t("Your entropy bleeds into the world around you. On having entropic backlash applied or increased to you, %d random enemies you can see within radius 10 will be shrouded in entropic forces for 8 turns. This increases the duration of new negative effects and reduces the duration of new beneficial effects applied to the target by %d%%.", [[将你身体上的熵能向周围辐射。每当你受到熵能反冲时，在你半径 10 码内随机的 %d 个可见敌人都将被熵能侵蚀 8 回合。
		增加（减少）它们受到的新的负面（正面）效果 %d%% 的持续时间。]], "tformat")
t("Unravel Existence", "解构存在", "talent name")
t("herald of oblivion", "破灭之兆", "_t")
t("Space warps and blurs around this titanic being, as if reality itself was struggling against it.", "时空在这个巨大的生物的周围扭曲模糊，仿佛现实本身正在和它斗争。", "_t")
t("Summon", "召唤", "_t")
t([[Your Nihil unravels the existence of the target, tearing them apart with entropy.
		If 6 negative magical effects are applied before Nihil expires a Herald of Oblivion will be summoned to assist you for %d turns.
		Currently existing debuffs, Spellshocked, and Seen by Arcane Eye will not count towards this total.  Refreshing the same debuff is counted.
		The Herald will have a bonus to all attributes equal to your Magic.  Many other stats will scale with level.
		Your increased damage, damage penetration, critical strike chance, and critical strike multiplier stats will all be inherited.]], [[你的空无能解构目标的存在并通过熵能将其撕裂。
		在空无效果结束之前，如果目标身上被施加了 6 个负面魔法效果，将召唤出持续 %d 回合的破灭之兆。
		之前已有的负面效果、法术冲击、被奥术之眼观察不会计入总数。刷新同一个效果会计入总数。
		破灭之兆的全部属性点提升你魔法属性的相同数值。其他属性根据本身等级提升。
		破灭之兆会继承你的伤害加成、伤害穿透、暴击几率和暴击倍率加成。]], "tformat")
t("Erase", "抹除", "talent name")
t([[Those affected by your Nihil find themselves increasingly removed from reality, reducing all damage they deal by %d%% and causing them to take %0.2f temporal damage each turn for each negative magical effect they have.
		The damage will scale with your Spellpower.]], [[受到你空无影响的生物逐渐从现实中被抹除，造成的伤害降低 %d%%。同时目标每具有一个负面魔法效果，则每回合受到 %0.2f 时空伤害。
		伤害受到法术强度加成。]], "tformat")
t("All is Dust", "尽归尘土", "talent name")
t("%s's entropic storm", "%s的湮灭风暴", "tformat")
t("#ORCHID#The entropic storm destroys %s!#LAST#", "#ORCHID#湮灭风暴摧毁了%s!#LAST#", "tformat")
t("a projectile", "一个抛射物", "_t")
t([[Summon a radius 4 storm of all-consuming oblivion at the targeted location for %d turns, reducing those within to nothing. Targets within will take %0.2f darkness damage and %0.2f temporal damage each turn.  Walls and other terrain within the storm will be disintegrated.
		Each time the storm deals damage enemies will have any detrimental magical effect with less than 3 duration set to 3 duration, and all enemy projectiles will be destroyed.
		The damage will scale with your Spellpower.]], [[在目标区域召唤出范围 4 码、持续 %d 回合的湮灭风暴，使受到影响的物质化为虚无，每回合造成 %0.2f 暗影 %0.2f 时空伤害。
		范围内的墙壁和部分其他地形将被粉碎。
		每次受到风暴伤害时，敌人身上不足 3 回合的负面魔法效果都将重置为 3 回合。风暴范围内敌人的投射物都将被扯碎。
		伤害受到法术强度加成。]], "tformat")
t("Void Crash", "虚空撞击", "talent name")
t("Slam your weapons into the ground, creating a radius 2 explosion of void energy dealing %d%% damage split between darkness and temporal.", "用武器撞击地面，产生 2 码的虚空爆炸，造成 %d%% 虚空武器伤害（暗影时空各 50%%）。", "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/rift.lua"

t("Reality Fracture", "实境撕裂", "talent name")
t("void rift", "虚空裂隙", "_t")
t("%s (empowered)", "%s（强化）", "tformat")
t([[The sheer power of your entropy tears holes through spacetime, opening this world to the void.
On casting a Demented spell you have a 30%% chance of creating a void rift lasting %d turns in a nearby tile, which will launch void blasts each turn at a random enemy in range 7, dealing %0.2f darkness and %0.2f temporal damage.

You may activate this talent to forcibly destabilize spacetime, spawning %d void rifts around you.]], [[你强大的熵之力撕裂了时空，将这个世界与虚空相连。
当施放疯狂系法术时，你有 30%% 几率在相邻的空地里打开一个虚空裂隙，持续 %d 回合。它每回合将会对范围 7 内的一个随机敌人释放虚空轰击，造成 %0.2f 点暗影伤害和 %0.2f 点时空伤害。

你可以主动激活这个技能来强制使得时空不稳定，在你周围创造 %d 个虚空裂隙。]], "tformat")
t("Quantum Tunnelling", "量子隧道", "talent name")
t("You do not have line of sight.", "你没有视线。", "logPlayer")
t("You must target a void rift.", "你必须瞄准虚空裂隙。", "logPlayer")
t("%s's space-time folding fizzles!", "%s的时空折叠失败了！", "logSeen")
t("%s emerges from a space-time rift!", "%s从时空裂隙中出现！", "logSeen")
t([[You briefly open a tunnel through spacetime, teleporting to a void rift in range %d. This destroys the rift, granting you a shield for %d turns absorbing %d damage.
		The damage absorbed will scale with your Spellpower]], [[你短暂地在时空中打开一个通道，传送到范围 %d 内的一个虚空裂隙。这将摧毁那个虚空裂隙，使你获得一个护盾，吸收 %d 点伤害，持续 %d 回合。
		护盾吸收的伤害随法术强度提高而提高。]], "tformat", {1,3,2})
t("Pierce the Veil", "刺破境界", "talent name")
t("nether breach", "彼世裂隙", "_t")
t("temporal vortex", "时空漩涡", "_t")
t("dimensional gateway", "维度之门", "_t")
t("void skitterer", "虚空造物", "_t")
t("A bizarre creature covered in writhing tendrils, rapidly teleporting from one place to another as it closes in on its prey.", "一个布满扭动触须的怪异生物，它一边迅速在空间中传送跳跃，一边逼近猎物。", "_t")
t("Summon", "召唤", "_t")
t([[Pouring more energy into your rifts, you have a %d%% chance for each one to instead appear as a more powerful type.
#PURPLE#Nether Breach:#LAST# Fires a beam dealing %0.2f darkness damage at a random target in radius 10.
#PURPLE#Temporal Vortex:#LAST# Inflicts %0.2f temporal damage each turn to enemies in radius 4 and reduces their global speed by 30%%.
#PURPLE#Dimensional Gate:#LAST# Has a 50%% chance each turn to summon a voidling lasting %d turns; a fast melee attacker that can teleport.
The stats of your Void Skitterers will scale with your Magic stat and level.]], [[向你的裂隙注入能量，你将有 %d%% 概率让每一个裂口进化成为更强大的形态。
#PURPLE#彼世裂隙：#LAST# 向半径 10 内随机敌人发射光束，造成 %0.2f 暗影伤害。
#PURPLE#时空漩涡：#LAST# 每回合对半径 4 内的敌人造成 %0.2f 时空伤害，并使其整体速度降低 30%%。
#PURPLE#维度之门 :#LAST# 每回合有 50%% 概率召唤一个虚空造物，持续 %d 回合，是一个能传送的高速近战攻击者
你的虚空造物属性随你的等级和魔法属性提高而提高。]], "tformat")
t("Dimensional Skitter", "维度迅击", "talent name")
t("%s's Dimensional Skitter fizzles!", "%s的维度迅击失败了！", "logSeen")
t("Teleport to a target within range 10 and strike them with your fangs dealing %d%% weapon damage.", "传送到范围 10 内的一个敌人处，并用你的尖牙攻击它，造成 %d%% 武器伤害。", "tformat")
t("Zero Point Energy", "零点能量", "talent name")
t([[You draw power from the depths of the void causing your Reality Fracture to enhance any existing rifts.
#GREY#Void Rift:#LAST# Deals %d%% increased damage and projectiles explode in radius 1.
#PURPLE#Nether Breach:#LAST# Deals %d%% increased damage and chains to 3 targets.
#PURPLE#Temporal Vortex:#LAST# Deals %d%% increased damage, radius increased by 1, and slow increased to 50%%.
#PURPLE#Dimensional Gate:#LAST# Voidling Skitterers will be frenzied, increasing their global speed by %d%%.]], [[你从虚空深处汲取能量，每当你激活实境撕裂时，你可以强化任何已存在的裂隙。
#GREY#虚空裂隙 :#LAST# 造成 %d%% 额外伤害，并且投射物在半径 1 范围内爆炸。
#PURPLE#彼世裂隙：#LAST# 造成 %d%% 额外伤害，并且连锁至 3 个额外目标。
#PURPLE#时空漩涡：#LAST# 造成 %d%% 额外伤害，效果半径增加 1，并且减速效果提高至 50%%。
#PURPLE#维度之门 :#LAST# 虚空造物将会变得狂暴，增加他们 %d%% 的整体速度。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/slow-death.lua"

t("Digest", "消化", "talent name")
t("%s has no usable talents.", "%s没有可用的技能。", "logPlayer")
t("Painful Agony", "催心剖肝", "_t")
t("Choose a talent to use:", "选择一个技能使用：", "_t")
t([[Make a melee attack dealing %d%% weapon damage and attempt to snatch a foe that has %d%% life or less left and swallow it whole.
		While you digest it you gain %d insanity per turn.
		The digestion lasts for 50 turns for an elite and 25 turns for others.
		This effect's remaining duration only goes down while in combat, and its bonuses are only applied while in combat.]], [[进行一次近战攻击，造成 %d%% 近战武器伤害，生命在 %d%% 以下的敌人将会被你整个吞下并消化。
		消化过程中你每回合获得 %d 疯狂值。
		精英消化时间为50回合，其他生物消化时间为25回合。
		效果持续时间只会在战斗中降低，其加成也只在战斗中有效。]], "tformat")
t("Painful Agony", "催心剖肝", "talent name")
t([[The pain you inflict to the victim you are digesting is so intense something breaks inside it, giving you a way into its mind.
		When you digest you can steal a random talent from your victim and can use it for yourself at talent level %d.
		At talent level 5 you can choose which talent to use.
		You may not steal a talent which you already know.
		The stolen talent will not use any resources to activate.
		]], [[正在被你消化的目标承受着极大的痛苦，内部器官不断破损，让你能趁机侵入它的思维。
		你可以窃取并使用它的一个随机技能（技能等级 %d）。
		技能等级 5 时，你可以指定窃取的技能。
		你不能窃取你已知的技能。
		窃取的技能使用时不消耗资源。
		]], "tformat")
t("Inner Tentacles", "内生触手", "talent name")
t([[Your stomatch grows small tentacles inside which probe and torment your digested victim even more.
		Whenever you deal a critical strike the tentacles probe harder, feeding your more energy from the pain of your victim making you able to feed on the pain your cause to others for 3 turns.
		This effect gives you 20%% chances to leech of your attacks, healing you for %d%% of the damage done.]], [[你的胃里长出细小的触手，对消化中的目标造成更多折磨。
		每次你暴击时，触手将进一步折磨目标，为你提供更多能量，持续 3 回合。
		该效果为你的攻击提供 20%% 几率吸血，将 %d%% 伤害转化为治疗。]], "tformat")
t("Consume Whole", "完整消化", "talent name")
t("You are not digesting a creature.", "你没有在消化生物。", "logPlayer")
t([[Instantly consume what remains of your victim, healing yourself for %d life and generating %d insanity.
			Activating this will reset the cooldown of your Digest talent.
		The life healed will increase with your Spellpower.]], [[立刻消化掉当前目标，获得 %d 生命和 %d 疯狂值。
		使用该技能会立刻重置消化技能的冷却。
		生命回复受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/tentacles.lua"

t("Mutated Hand", "异变之手", "talent name")
t([[Your left hand mutates into a disgusting mass of tentacles.
		When you have your offhand empty you automatically hit your target and those on the side whenever you hit with a basic attack.
		Also increases Physical Power by %d, and increases weapon damage by %d%% for your tentacles attacks.
		Each time you make an attack with your tentacle you gain %d insanity.
		You generate a low power psionic field around you when around #{italic}#'civilized people'#{normal}# that prevents them from seeing you for the horror you are.

		Your tentacle hand currently has these stats%s:
		%s]], [[你的左手异变成为一坨恶心的触手。
		副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。
		物理强度提高 %d，触手武器伤害提高 %d%%。
		每次触手攻击时，获得 %d 疯狂值。
		附近有 #{italic}# 普通人 #{normal}# 时会自动生成微弱的心灵护盾，避免被他们发现你的恐魔形态。
		你的触手当前属性为 %s :
		%s]], "tformat")
t(", #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#", "，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#", "_t")
t("Lash Out", "旋风鞭挞", "talent name")
t("You require an empty offhand to use your tentacle hand.", "你需要副手空手才能使用触手。", "logPlayer")
t("You require a weapon and an empty offhand!", "你必须有一把武器和一只空手！", "logPlayer")
t("Spin around, extending your weapon and damaging all targets around you for %d%% weapon damage while your tentacle hand extends and hits all targets in radius 3 for %d%% tentacle damage.\n\t\t\t\t\n\t\t\t\tIf the mainhand attack hits at least one enemy you gain %d insanity.\n\t\t\t\tIf the tentacle attack hits at least one enemy you gain %d insanity.\n\t\t\n\t\t#YELLOW_GREEN#When constricting:#WHITE# Your tentacle attack is centered around your constricted target (but not your weapon attack) and only in radius 1 but it also dazes anything hit for 5 turns.", [[飞速旋转，伸展武器对周围单位造成 %d%% 武器伤害，并且伸展触手对 3 码内单位造成 %d%% 触手伤害。
		如果武器击中敌人，你获得 %d 疯狂值。
		如果触手击中敌人，你获得 %d 疯狂值。
		#YELLOW_GREEN# 当触手处于缠绕状态 :#WHITE# 你的触手攻击以被缠绕目标为中心展开，攻击范围只有 1 码（武器攻击除外），但是会使被击中单位眩晕 5 回合。]], "tformat")
t("Tendrils Eruption", "触手地狱", "talent name")
t("%s resists the slimy tendril!", "%s抵挡了黏液触手！", "logSeen")
t([[You plant your tentacle hand in the ground where it splits up and extends to a target zone of radius %d.
		The zone will erupt with many black tendrils to hit all foes caught inside dealing %d%% tentacle damage.
		Any creature hit by the tentacle must save against spell or be numbed by the attack, reducing its damage by %d%% for 5 turns.

		If at least one enemy is hit you gain %d insanity.

		#YELLOW_GREEN#When constricting:#WHITE#The tendrils pummel your constricted target for %d%% tentacle damage and if adjacent you make an additional mainhand weapon attack.  Talent cooldown reduced to 10.]], [[你的触手钻入地下，分布到 %d 码范围的目标区域。
		该区域喷发出大量黑色触手，对区域内所有敌人造成 %d%% 触手伤害。
		被触手击中的生物需要进行法术检定，检定失败将被麻痹，5 回合内伤害降低 %d%%。
		如果有敌人被触手击中，你获得 %d 疯狂值。
		#YELLOW_GREEN# 当触手处于缠绕状态 :#WHITE# 触手对缠绕对象连续突击，造成 %d%% 触手伤害。如果你与被缠绕对象相邻，则进行一次额外的主手打击。技能冷却时间缩短为 10 回合。]], "tformat")
t("Constrict", "缠绕", "talent name")
t("You require a mutated hand!", "你需要异变之手！", "logPlayer")
t("%s's tentacle fails to move %s!", "%s的触手无法移动%s！", "tformat")
t("Your constrict target has disappeared!", "你缠绕的目标消失了！", "logPlayer")
t("This target can not be moved!", "无法移动目标！", "logPlayer")
t([[You extend your tentacle to grab a distant target, pulling it to you.
		As long as Constrict stays active the target is bound by your tentacle, it can try to move away but each turn you pull it back in 1 tile.
		While constricting you cannot use your tentacle to enhance your normal attacks but you deal %d%% tentacle damage each turn to your target.
		Enemies can resist the attempt to pull them but Constrict will always work for purposes of modifying your talents.
		Your other tentacle talents may act differently when used while constricting (check their descriptions).]], [[伸展触手缠绕一个远处的目标，并向你拖拽。
		只要缠绕技能保持激活，目标就会被触手束缚；它可以尝试向远处移动，但每回合都会被你拉回一码。
		当缠绕了敌人，普通攻击不会额外附加触手攻击，但每回合对缠绕敌人造成 %d%% 触手伤害。
		敌人可以抵抗触手拖拽，但即使抵抗成功，只要缠绕技能仍处于激活状态，它仍会对你的技能产生修改效果。
		其他触手技能在缠绕状态下会发生变化，具体请查看相应技能描述。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/timethief.lua"

t("Accelerate", "窃速", "talent name")
t([[Distorting spacetime around yourself, you reduce the movement speed of all enemies in radius %d by 50%% for %d turns.
You use the siphoned speed to grant yourself incredible quickness for 1 turn, increasing movement speed by %d%%, increased by a further %d%% for each enemy slowed, to a maximum of 4.
Any actions other than movement will cancel the effect.]], [[扭曲周围时空，周围 %d 码内敌人移动速度降低 50%%，持续 %d 回合。
		你使用偷取的速度强化自身，使自己获得一回合神速状态，移动速度提高 %d%%，每减速一个敌人，额外提高 %d%%，最大个数 4 个。
		移动外的任何行动将终止加速效果。]], "tformat")
t("Switch", "偷换", "talent name")
t("Release a surge of entropy, cleansing yourself of afflictions while draining the energy from others. All enemies in range 10 will have the duration of %d beneficial effects reduced by %d turns, while you will have an equal number of detrimental effects reduced by the same duration.", "释放熵的浪潮，清除自己的灾祸，同时吸取他人的能量。10 码内所有敌人的 %d 项有益效果持续时间缩短 %d 回合。自身同等数量的有害效果持续时间缩短同等回合。", "tformat")
t("Suspend", "暂停", "talent name")
t([[You freeze yourself in time for %d turns, preventing you from taking any action but preventing any damage taken.
				Negative effects and cooldowns will decrease in duration, while beneficial effects will remain at their current duration.]], [[你在时间中凝固 %d 回合，无法行动但也无法被伤害。
		负面效果持续时间和技能冷却时间会正常扣减，正面效果持续时间不变。]], "tformat")
t("Split", "分裂", "talent name")
t("Not enough space to summon!", "没有足够的空间召唤！", "logPlayer")
t("You can't clone summons!", "你不能克隆召唤物", "logPlayer")
t("%s resists!", "%s抵抗了效果！", "logSeen")
t("#LIGHT_STEEL_BLUE#%s's Temporal Clone#LAST#", "#LIGHT_STEEL_BLUE#%s的时空克隆#LAST#", "tformat")
t("A warped image resembling the creature it appeared from, its features a flickering blur of all possible futures.", "一个扭曲的图像，类似于它模仿的生物，它展现着其所有可能的未来的模糊影像。", "_t")
t("Summon", "召唤", "_t")
t([[The target enemy will be partially removed from the normal flow of time for %d turns, inhibiting their ability to interact with the world. All damage taken will be reduced by %d%%, while all damage dealt will be reduced by %d%%.
While active, you form the frayed threads of their timeline into a temporal clone of them for the same duration, which assists you in combat. This clone is identical, but has %d%% reduced life and deals %d%% damage.]], [[将目标敌人从正常时间流部分移除，持续 %d 回合，隔绝他们与现实世界交互的能力。移除期间敌人受到的伤害降低 %d%%，造成的伤害也降低 %d%%。
		技能启动时，你从受损的时间线中召唤敌人的时空克隆体协助你战斗，持续时间与敌人移除时间相同，克隆体生命值降低 %d%%，只造成 %d%% 伤害，其他能力与本体相同。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/demented/void.lua"

t("Void Stars", "虚空之星", "talent name")
t("You must be wearing light armor for this talent.", "你必须穿着轻甲才能使用这一技能。", "logPlayer")
t("A void star appears around %s.", "一颗虚空之星在%s周围出现。", "logSeen")
t("#FIREBRICK##Target#'s void star absorbs the damage from #Source#, converting it into entropy!#LAST#", "#FIREBRICK##Target#的虚空之星吸收了来自#Source#的伤害，将其转化为熵！#LAST#", "logCombat")
t("%s(%d to entropy)", "%s（%d 熵）", "tformat")
t([[Conjure void stars that orbit you, defending you from incoming attacks. Each time an attack deals more than 10%% of your maximum life, a star will be consumed to reduce the damage taken by %d%%, of which 40%% will be dealt to you as entropic backlash.
		You regenerate 1 star every %d turns, stacking up to 4 times.
		This talent will only function in light armor.]], [[形成围绕你旋转，为你抵御伤害的虚空之星。
		每当受到超过 10%% 最大生命的伤害时，消耗一颗虚空之星，使受到的伤害减少 %d%%，自己受到等同于减免伤害 40%% 的熵能反冲。
		虚空之星每经过 %d 回合自动恢复一颗。
		此技能只有装备轻甲时生效。]], "tformat")
t("Nullmail", "虚空装甲", "talent name")
t([[Reinforce your armor with countless tiny void stars, increasing armor by %d.
Each time your void stars are fully depleted, you gain a shield absorbing the next %d damage taken within %d turns. This shield cannot trigger again until your void stars are fully restored.]], [[用无数微小的虚空之星强化护甲，护甲值提高 %d。
每次虚空之星完全消耗后，生成一个吸收 %d 伤害的护盾持续 %d 回合。在虚空之星完全恢复前无法再次生成护盾。]], "tformat")
t("Black Monolith", "黑色巨石", "talent name")
t("You must have at least 1 void star to summon a monolith.", "你必须有一颗虚空之星才能召唤巨石。", "logPlayer")
t("Not enough space to summon your monolith!", "没有足够空间，无法召唤巨石", "logPlayer")
t("void monolith", "虚无巨石", "_t")
t("This bizarre oblong shape floats in the air, defying gravity. Its form seems to subtly shift, and you feel an intense desire to move towards it.", "这个奇异的长方体无视重力漂浮在空气中。它的形态似乎正在微妙地转换着，你感受到向着它走去的强烈愿望。", "_t")
t("Summon", "召唤", "_t")
t([[Consuming a void star, you use it to summon a void monolith at the targeted location for %d turns. The monolith is very durable, and while immobile it will attempt to daze enemies within radius %d for 2 turns every half a turn using your spellpower.
			The monolith will gain %d life rating and %d%% all resist based on your Magic stat.]], [[消耗一枚虚空之星，在目标位置召唤持续 %d 回合的虚无巨石。巨石非常坚固，无法移动，每半回合对 %d 码范围内敌人施加眩晕2回合（基于本体法术强度）。
			基于你的魔法属性，巨石获得 %d 生命成长和 %d%% 全体抗性。]], "tformat")
t("Essence Reave", "精华收割", "talent name")
t("%s rends the essence of %s, restoring %d void shards!", "%s撕裂了%s的精华，恢复%d个虚空之星！", "logSeen")
t([[You rend the very essence of the target, drawing on their life and converting it to void stars. The target takes %0.2f darkness and %0.2f temporal damage, and you gain %d void star(s).
		The damage will increase with your Spellpower.]], [[撕开目标的核心部位，汲取生命转化为虚空之星。目标受到 %0.2f 黑暗和 %0.2f 时空伤害，你获得 %d 虚空之星。
		伤害随法术强度升高。]], "tformat")

------------------------------------------------
