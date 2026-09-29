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

section "tome-cults/data/talents/demented/writhing-body.lua"

t(", #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#", "，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#", "_t")
t("You require an empty offhand to use your tentacle hand.", "你需要副手空手才能使用触手。", "logPlayer")
t("You require a weapon and an empty offhand!", "你必须有一把武器和一只空手！", "logPlayer")
t("The diseases of %s spread!", "%s的疾病在传播！", "logSeen")
t("%s resists the disease!", "%s抵抗了疫病！", "logSeen")
t([[Infects the target with a very contagious disease, doing %0.2f damage per turn for 6 turns.
		If any blight damage from non-diseases hits the target, the epidemic may activate and spread a random disease to nearby targets within a radius 2 ball.
		The chance to spread increases with the blight damage dealt and is 100%% if it is at least %d%% of the target's maximum life.
		Creatures suffering from that disease will also suffer healing reduction (%d%%) and diseases immunity reduction (%d%%).
		Epidemic is an extremely potent disease; as such, it fully ignores the target's diseases immunity.
		The damage will increase with your Spellpower, and the spread chance increases with the amount of blight damage dealt.]], [[使目标感染一种传染性极强的疾病，每回合造成 %0.2f 伤害，持续 6 回合。
		如果目标受到非疾病来源的枯萎伤害，传染病可能被触发，并将一种随机疾病传播给半径 2 的球形范围内的附近目标。
		传播几率随造成的枯萎伤害提高；当该伤害至少达到目标最大生命值的 %d%% 时，传播几率为 100%%。
		感染该疾病的生物还会受到治疗效果降低（%d%%）和疾病免疫降低（%d%%）的影响。
		传染病威力极强，会完全无视目标的疾病免疫。
		伤害随法术强度提高，传播几率随造成的枯萎伤害量提高。]], "tformat")
t("Mutated Hereragegand", "异变之手", "talent name")
t([[		Also increases Physical Power by %d, and increases weapon damage by %d%% for your tentacles attacks.

		Your tentacle hand currently has those stats%s:
		%s]], [[		同时增加 %d 点物理强度，并使触手攻击的武器伤害提高 %d%%。

		你的触手之手当前具有以下属性%s：
		%s]], "tformat")
t("Lash Outrthrthrth", "旋风鞭挞", "talent name")
t([[Spin around, extending your weapon and damaging all targets around you for %d%% weapon damage while your tentacle hand extends and hits all targets in radius 3 for %d%% tentacle damage.
		]], [[飞速旋转，伸展武器对周围单位造成 %d%% 武器伤害，并且伸展触手对 3 码内单位造成 %d%% 触手伤害。
		]], "tformat")
t("Piercing Tentacle", "穿刺触手", "talent name")
t([[You quickly extend your tentacle hand up to range %d, impaling all creatures in the way.
		Impaled creatures take %d%% tentacle damage and get sick, gaining a random disease for %d turns that deals %0.2f blight damage per turn and reduces strength, dexterity or constitution by %d.]], [[你迅速伸长触手，最远达到 %d 码，刺穿沿途所有生物。
		被刺穿的生物受到 %d%% 触手伤害，并感染一种随机疾病，持续 %d 回合；该疾病每回合造成 %0.2f 枯萎伤害，并使力量、敏捷或体质降低 %d 点。]], "tformat")
t("Tentaclesrsthrhrhrh Ground", "地下触手", "talent name")
-- untranslated text
--[==[
t("Mutated Hereragegand", "Mutated Hereragegand", "talent name")
t([[		Also increases Physical Power by %d, and increases weapon damage by %d%% for your tentacles attacks.

		Your tentacle hand currently has those stats%s:
		%s]], [[		Also increases Physical Power by %d, and increases weapon damage by %d%% for your tentacles attacks.

		Your tentacle hand currently has those stats%s:
		%s]], "tformat")
t("Lash Outrthrthrth", "Lash Outrthrthrth", "talent name")
t([[Spin around, extending your weapon and damaging all targets around you for %d%% weapon damage while your tentacle hand extends and hits all targets in radius 3 for %d%% tentacle damage.
		]], [[Spin around, extending your weapon and damaging all targets around you for %d%% weapon damage while your tentacle hand extends and hits all targets in radius 3 for %d%% tentacle damage.
		]], "tformat")
t("Piercing Tentacle", "Piercing Tentacle", "talent name")
t([[You quickly extend your tentacle hand up to range %d, impaling all creatures in the way.
		Impaled creatures take %d%% tentacle damage and get sick, gaining a random disease for %d turns that deals %0.2f blight damage per turn and reduces strength, dexterity or constitution by %d.]], [[You quickly extend your tentacle hand up to range %d, impaling all creatures in the way.
		Impaled creatures take %d%% tentacle damage and get sick, gaining a random disease for %d turns that deals %0.2f blight damage per turn and reduces strength, dexterity or constitution by %d.]], "tformat")
t("Tentaclesrsthrhrhrh Ground", "Tentaclesrsthrhrhrh Ground", "talent name")
--]==]


------------------------------------------------

section "tome-cults/data/talents/misc/misc.lua"

t("glass golem", "玻璃傀儡", "_t")
t("Self-destruction", "自爆", "talent name")
t("Self destruct in a glorious explosion of gore dealing %0.2f blight damage to all enemies in %d radius.  Your summoner must be dead to use this talent.", "自爆成一团光荣的血肉，对半径 %d 格范围内的所有敌人造成 %0.2f 枯萎伤害。这个技能只有主人死亡时能够使用。", "tformat", {2,1})
t("Teleport: Kroshkkur", "传送：克诺什库尔", "talent name")
t("#CRIMSON#Kroshkkur is destroyed, there is nothing to teleport to.", "#CRIMSON#克诺什库尔被摧毁了，无法传送到那里。", "logPlayer")
t("The spell fizzles...", "法术失败了……", "logPlayer")
t("There are creatures that could be watching you; you cannot take the risk.", "有生物可以看见你，你不能冒这个险。", "log")
t([[Allows to teleport to Kroshkkur.
	You have studied the forbidden secrets there and have been granted a special portal spell to teleport back.
	This spell must be kept secret; it should never be used within view of uninitiated witnesses.
	The spell takes time (40 turns) to activate, and you must be out of sight of any other creature when you cast it and when the teleportation takes effect.]], [[允许传送至克诺什库尔。
	你学习了那里的禁忌秘密，因此获得了传送至克诺什库尔的法术。
	该法术必须保持机密；它在有其他人在场时不能使用。
	该法术需要 40 回合生效，在此期间你需要处于任何生物视线外。]], "_t")
t("Call of Amakthel", "阿马克泰尔的呼唤", "talent name")
t("%s is pulled in!", "%s 被拉了进去！", "logSeen")
t("Pull all foes within radius 10 2 grids towards you.", "将10码范围内所有的目标朝你拉近2格。", "_t")
t("Crumble", "瓦解", "talent name")
t([[Fire a blast of darkness at an enemy dealing %0.2f damage and destroying any walls in radius 3 around them.
		The damage will increase with your Spellpower.]], "发射黑暗能量，对目标造成 %0.2f 伤害并破坏 3 格范围内的墙壁。伤害受法术强度加成。", "tformat")
t("Blightlash", "枯萎鞭挞", "talent name")
t("You require an empty offhand to use your tentacle hand.", "你需要副手空手才能使用触手。", "logPlayer")
t("You require a weapon and an empty offhand!", "你必须有一把武器和一只空手！", "logPlayer")
t("Lash an enemy within range 10 with your tentacle, dealing %d%% blight damage.", "用触手打击 10 码范围内的一个敌人，造成 %d%% 枯萎伤害。", "tformat")
t("Twisted Evolution", "扭曲进化", "talent name")
t([[Evolve %d allies within radius 10 in random ways for 5 turns.
		#ORCHID#Speed:#LAST# Increases global speed by %d%%.
		#ORCHID#Form:#LAST# Increases all stats by %d.
		#ORCHID#Power:#LAST# Increases all damage by %d%%.]], [[以随机方式进化 10 格范围内至多 %d 名友方单位，持续 5 回合。
		#ORCHID#速度：#LAST# 增加 %d%% 整体速度。
		#ORCHID#形态：#LAST# 增加 %d 全属性。
		#ORCHID#力量：#LAST# 增加 %d%% 伤害。]], "tformat")
t("golem", "傀儡", "talent category")
t("glass", "玻璃", "talent type")
t("Glass Golem basic capacity.", "玻璃傀儡的基础能力。", "_t")
t("Glass Splinters", "玻璃碎片", "talent name")
t("%s resists the splinters!", "%s 抵抗了玻璃碎片！", "logSeen")
t([[Smash your target with a splintering glass attack doing %d%% arcane weapon damage.
		If this attack hits the target will have glass splinters for 6 turns.
		Each turn the target will bleed for 8%% of the attack damage. The splinters are very painful and if the target moves it will instantly take %d%% of the attack damage.
		At level 5 the target suffers so much it has 15%% chances to fail using talents.]], [[使用玻璃碎片攻击敌人，造成 %d%% 奥术武器伤害。
		如果攻击命中，目标将被玻璃碎片扎 6 回合。
		每回合目标将受到 8%% 攻击伤害的流血伤害。
		同时每当目标移动时，受到 %d%% 攻击伤害。
		技能等级 5 后，目标有 15%% 几率使用技能失败。]], "tformat")
t("Throw Pebble", "投掷鹅卵石", "talent name")
t("something", "某物", "_t")
t("#Source# expertly hurls a pebble at #target#!", "#Source#朝#target#投掷鹅卵石！", "logCombat")
t([[Throw a pebble at your target, dealing %0.2f physical damage.
		The damage will increase with your Strength.]], [[朝目标扔石头，造成 %0.2f 物理伤害。
		伤害受力量加成。]], "tformat")
t("Netherforce", "彼世之力", "talent name")
t([[Smash the target with the force of the void dealing %0.2f darkness and %0.2f temporal damage to the target and knocking them back 8 spaces.
		The power of this spell inflicts entropic backlash on you, causing you to take %d damage over 8 turns. This damage counts as entropy for the purpose of Entropic Gift.
		The damage will increase with your Spellpower.]], [[用虚空之力攻击目标，造成 %0.2f 暗影 %0.2f 时空伤害并击退 8 格。
		该法术会产生熵能反冲，让你在 8 回合内受到 %d 伤害。此伤害对熵之礼物而言视为熵。
		伤害受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-cults/data/talents/misc/races.lua"

t("race", "种族技能", "talent category")
t("drem", "德瑞姆", "talent type")
t("The various racial bonuses a character can have.", "角色可能拥有的各种种族加成。", "_t")
t("Frenzy", "狂热", "talent name")
t([[Enter a killing frenzy for 3 turns.
		During the frenzy the first time you use a class talent it has no cooldown (but does if used twice).
		This does not work for inscriptions, talents that take no turn to use, passives, or talents with fixed cooldowns.
		]], [[进入杀戮狂热状态 3 回合。
		狂热状态下，  你使用的第一个职业技能不进入冷却（再次使用将进入冷却。）
		该效果对纹身、符文、被动技能、瞬间技能以及固定冷却时间技能无效。
		]], "tformat")
t("Spikeskin", "尖刺皮肤", "talent name")
t([[Your skin grows small spikes coated in dark blight.
		When you are hit in melee the attacker starts bleeding black blood for 5 turns that deals %0.2f darkness damage each turn. This effect may only happen once per turn.
		You are empowered by the sight of the black blood, for each bleeding creature in radius 2 you gain 5%% all resistances, limited to %d creatures.
		The damage will scale with your Magic stat.]], [[你的皮肤生长出被黑暗和枯萎力量覆盖的尖刺。
		当你被近战攻击命中时，攻击者开始流出黑血，持续 5 回合，每回合造成 %0.2f 暗影伤害。该效果每回合只能触发一次。
		同时，目睹黑血会使你受到强化：2 格范围内每个可见的流着黑血的生物，都使你获得 5%% 全部抗性，最多计 %d 个生物。
		伤害随魔法属性提升。]], "tformat")
t("Faceless", "无面", "talent name")
t([[Your faceless visage is puzzling and emotionless, allowing you to more easily resist mind tricks.
		You gain %d mental save, %d%% confusion immunity.]], [[你无面孔的脸没有情感，令人困惑。这让你更容易抵抗精神冲击。
		你获得 %d 精神豁免，%d%% 混乱免疫。]], "tformat")
t("From Below It Devours", "自深渊吞噬万物", "talent name")
t("Not enough space to summon!", "没有足够的空间召唤！", "logPlayer")
t("hungering mouth", "饥饿巨口", "_t")
t("\"From below, it devours.\"", "\"来自深渊，吞噬一切\"", "_t")
t([[Your affinity with things that dwell deep beneath the surface allows you to summon a hungering mouth.
		The mouth has %d bonus life, lasts for %d turns, and deals no damage.
		Each turn the mouth will draw all enemies in radius 10 2 spaces towards itself.
		Its bonus life depends on your Constitution stat and talent level.  Many other stats will scale with level.]], [[你同地下深处某物的联系让你能召唤一只饥饿巨口。
		每回合它将周围 10 码内所有敌人朝自身拉近 2 码。
		它有 %d 额外生命，存在 %d 回合，不造成伤害。
		它的额外生命取决于你的体质和技能等级。许多其他属性受等级影响。]], "tformat")
t("\
For Drems this effect activates as long as the hungering mouth summoned by From Below It Devours is alive.", "\
对于德瑞姆，这一效果在“自深渊吞噬万物”召唤的饥饿巨口仍然存活时持续生效。", "_t")
t("krog", "克罗格", "talent type")
t("Wrath of the Wilds", "自然之怒", "talent name")
t([[You unleash the wrath of the wilds for 5 turns.
		When you deal damage to a creature while wrath is active you have %d%% chance (100%% for the first creature hit each turn) to stun them for 3 turns.
		This effect can only stun a creature once per turn.
		Chance scales with your Constitution and apply power is the highest or your physical or mind power.]], [[你释放持续 5 回合的自然的愤怒。
		愤怒状态下，每当你造成伤害时有 %d%% （每回合攻击的第一个生物 100%%）几率震慑 3 回合。
		每个敌人每回合只能被该技能震慑一次。
		震慑几率受体质影响，强度由物理或精神强度中较高一项决定。]], "tformat")
t("Drake-Infused Blood", "灌输龙血", "talent name")
t("You must kill more enemies before you can use this talent!", "你需要杀死更多敌人才能使用该技能！", "logPlayer")
t("#GREEN#You can now change your elemental drake aspect", "#GREEN#你现在可以切换你的龙血类型了。", "say")
t("Fire Drake / Fire Resistance", "火龙 / 火焰抗性", "_t")
t("Cold Drake / Cold Resistance", "冰龙 / 寒冷抗性", "_t")
t("Storm Drake / Lightning Resistance", "风暴龙 / 闪电抗性", "_t")
t("Sand Drake / Physical Resistance (1/3rd values)", "沙龙 / 物理抗性（1/3数值）", "_t")
t("Wild Drake / Nature Resistance", "自然龙 / 自然抗性", "_t")
t("Acid Drake / Acid Resistance", "酸龙 / 酸性抗性", "_t")
t("Never mind", "算了。", "_t")
t("#LAST# #{italic}#(current)#{normal}#", "#LAST# #{italic}#（当前）#{normal}#", "_t")
t("Drake Aspect", "龙血类型", "_t")
t("Choose an aspect to bring forth:", "选择你使用的龙血类型：", "_t")
t([[Since ziguranth removed those filthy magic runes from your body you have needed an alternative form of power to sustain your body. Thanks to drake blood you have found that power.
		Your blood hardens yourself, passively increasing stun resistance by %d%%, %s resistance by %d%% and dealing %d %s damage on melee attacks.
		You can activate this talent to change which drake aspect to bring forth, altering the elemental type of the bonus.
		The resistance and damage scales with your Willpower.

		Changing your aspect requires combat experience, you may only do so after slaying 100 enemies (current %d).

		When you learn this talent you become so strong you can wield any type of one handed weapon in your offhand.]], [[伊格兰斯除去了你身体内部肮脏的魔法符文，此后你需要另一种力量来维持你的身体。多亏了龙血，你找到了这种力量。
		龙血强化了你，使你获得 %d%% 震慑抗性，%d%% %s 伤害抗性，%d %s 近战附加伤害。
		你可以主动开启该技能来改变龙血类型，进而改变相应元素。
		抗性和附加伤害受意志值加成。

		改变龙血类型需要战斗经验，你必须杀死 100 个敌人后才能使用（当前 %d）。

		当你学会该技能时，你变得如此强大，以至于能双持任何单手武器。]], "tformat", {1,3,2,4,5,6})
t("Fuel Pain", "升华痛苦", "talent name")
t([[Your body is used to pain. When you take a hit of 20%% or more of your max life one of your inscriptions is taken off cooldown and infusion saturation is removed.
		This effect has a cooldown of %d turns.]], [[你的身体习惯于痛苦。每次你受到最大生命 20%% 或以上的伤害时，你的一个纹身将立刻冷却完毕，并移除符文饱和效果。
		该效果冷却时间为 %d 回合。]], "tformat")
t("Drakeblood Strike", "龙血打击", "talent name")
t([[You were created by ziguranth for one purpose only, to wage war on magic!
			Strike your target dealing %d%% %s weapon damage and silencing them for %d turns.
			The damage type will change with your drake aspect.
			The chance to silence will increase with the highest of your physical or mind power.]], [[你被伊格制造的唯一理由：对魔法作战！
		打击你的敌人，造成 %d%% %s 武器伤害，并沉默它们 %d 回合。
		伤害类型根据龙血的类型而决定。
		沉默的几率受物理强度或精神强度的最高值加成。]], "tformat")
t("parasite", "寄生", "talent type")
t("The various racial bonuses a character can have.. when its head is cut off and replaced with a parasite.", "一个角色可以学习的各种种族技能……当它的头被寄生兽取代的时候。", "_t")
t("Take a Bite", "咬一口", "talent name")
t("#Source# tries to bite #target#!", "#Source#试图咬#target#！", "logCombat")
t("%s resists!", "%s抵抗了效果！", "logSeen")
t([[You try to bite off your foe with your #{italic}#head#{normal}# for %d%% blight weapon damage.
		If the target falls under 20%% life you have %d%% chances to outright kill it (bosses are immune).
		Whenever you succesfully bite a foe you regenerate %0.1f life per turn for 5 turns.
		Instant kill chances and regeneration increase with your Constitution stat and weapon damage increases with the highest of your Strength, Dexterity or Magic stat.]], [[你尝试用 #{italic}#头#{normal}# 咬你的敌人造成 %d%% 枯萎武器伤害。
		如果目标被咬后生命不足 20%%，你有 %d%% 几率直接杀死它（对 boss 无效）。
		你咬中以后 5 回合内每回合回复 %0.1f 生命。
		秒杀几率和生命回复受体质加成，武器伤害受力量敏捷魔法中最高值影响。]], "tformat")
t("Ultra Instinct", "终极本能", "talent name")
t([[Without the distraction of #{bold}#thoughts#{normal}# or #{bold}#self#{normal}# your body reacts faster and better to aggressions.
		Increases global speed by %d%%.]], [[没有 #{bold}#思维#{normal}# 和 #{bold}#自我#{normal}# 的干扰，你的身体全凭本能行动，反应速度更快。
		整体速度增加 %d%%。]], "tformat")
t("Corrupting Influence", "堕落影响", "talent name")
t([[The parasite corruption seeps into your body, strengthening it.
		Increases blight, darkness, temporal and acid resistances by %d%% but decreases nature and light resistances by %d%%.]], [[寄生在你身体里的堕落力量渗入你的身体，给予你强化。
		增加 %d%% 枯萎、黑暗、时空和酸性伤害抗性，同时减少 %d%% 自然和光系伤害抗性。]], "tformat")
t("Horror Shell", "恐惧外壳", "talent name")
t([[Creates a shell around you, absorbing %d damage. Lasts for 10 turns.
		The total damage the shield can absorb increases with your Constitution.]], [[在你身边制造一层持续 10 回合吸收 %d 伤害的外壳。
		吸收量受体质加成。]], "tformat")

------------------------------------------------

section "tome-cults/data/timed_effects.lua"

t("other", "其他", "effect subtype")
t("Fight your foe! If anything wrong happens, the Fortress will pull you out.", "攻击敌人！如果出了什么问题，堡垒会把你送出去。", "_t")
t("frenzy", "狂乱", "effect subtype")
t("Frenzy", "狂热", "_t")
t("Class talents have no cooldown the first time they are used.", "第一次使用的职业技能不进入冷却。", "_t")
t("bleed", "流血", "effect subtype")
t("Black Blood Bleeding", "黑血横流", "_t")
t("Black blood sips from every pore, dealing %0.2f darkness damage per turn.", "黑血横流，每回合造成 %0.2f 暗影伤害。", "tformat")
t("#Target# starts to bleed black blood.", "#Target#开始流出黑血。", "_t")
t("#Target# stops bleeding black blood.", "#Target#不再流出黑血。", "_t")
t("blood", "血", "effect subtype")
t("Spikeskin", "尖刺皮肤", "_t")
t("Empowered by the sight of black blood, granting %d%% all resistances.", "目睹黑血时受到强化，获得 %d%% 全部抗性。", "tformat")
t("slime", "史莱姆", "effect subtype")
t("corrupted", "腐化", "effect subtype")
t("Slimy Tendril", "黏稠触须", "_t")
t("Caught in a slimy tendril, reducing all damage by %d%%.", "被触须抓住，造成的所有伤害降低 %d%%。", "tformat")
t("#Target# is caught by a slimy tendril.", "#Target#被黏稠触须捕获。", "_t")
t("#Target# is free from the tendril.", "#Target#逃脱黏稠触须。", "_t")
t("Tentacle Constriction", "触手缠绕", "_t")
t("Caught by a tentacle from %s that deals %d%% tentacle damage and pulls you 1 space towards them each turn.", "被 %s 的触手缠绕，每回合造成 %d%% 触手伤害并将你拉近一码。", "tformat")
t("#Target# is constricted by a tentacle.", "#Target#被触手缠绕。", "_t")
t("#Target# is free from the tentacle constriction.", "#Target#逃脱了触手缠绕。", "_t")
t("Carrion Feet", "蠕动之足", "_t")
t("Caught disgusting worms, reducing all damage by %d%%.", "被恶心的蠕虫抓住，造成的伤害减少 %d%%。", "tformat")
t("#Target# is caught in gore.", "#Target#被血肉覆盖。", "_t")
t("#Target# is free from the gore.", "#Target#不再被血肉覆盖。", "_t")
t("growth", "生长", "effect subtype")
t("massive", "巨型", "effect subtype")
t("Overgrowth", "过度生长", "_t")
t("Can walk through walls and quake every turn, %d%% more damage and %d%% more resistances.", "能够穿过墙壁，并在移动时引发地震；造成的伤害增加 %d%%，全部抗性增加 %d%%。", "tformat")
t("#Target# suddently grows.", "#Target#突然变大。", "_t")
t("#Target# shrinks back.", "#Target#缩小了。", "_t")
t("corruption", "堕落", "effect subtype")
t("slow", "减速", "effect subtype")
t("Decaying Guts", "腐烂内脏", "_t")
t("Reduces global action speed by %d%%.", "全局速度下降 %d%%。", "tformat")
t("#Target# is covered in decaying guts.", "#Target#被腐烂内脏覆盖。", "_t")
t("#Target# is free from the decaying guts.", "#Target#摆脱了腐烂内脏。", "_t")
t("miscellaneous", "杂项", "effect subtype")
t("Worm that Walks out of sight", "蠕虫合体在视野外", "_t")
t("The Worm that Walks is out of sight of the alchemist; direct control will be lost!", "蠕虫合体在主人的视野外；无法直接控制它！", "_t")
t("#LIGHT_RED##Target# is out of sight of its master; direct control will break!", "#LIGHT_RED##Target#在主人视野外；直接控制中断了！", "_t")
t("+Out of sight", "+视野外", "_t")
t("#LIGHT_RED#You lost sight of your worm that wakls for too long; direct control is broken!", "#LIGHT_RED#蠕虫合体脱离你视野时间过长，控制被中断了！", "logPlayer")
t("worm that walks out of sight", "蠕虫合体在视野外", "_t")
t("Shared Insanity", "共享疯狂", "_t")
t("Linked to their horror ally gaining %d%% all damage resistance.", "和恐魔建立链接，获得 %d%% 全部抗性。", "tformat")
t("#Target# links closer to his ally!", "#Target#与盟友联结！", "_t")
t("#Target# no longer seems to be in sync with his ally.", "#Target#不再和盟友同步。", "_t")
t("Terrible Sight", "恐怖景象", "_t")
t("Terrified of the horror duo attacking them reducing defense and spell save by %d.", "因两只恐魔的现身而惊恐，闪避和法术豁免降低 %d。", "tformat")
t("#Target# is terrified of the horrors attacking him!", "#Target#因攻击他的恐魔惊恐！", "_t")
t("#Target# is no longer afraid of the horrors attacking him.", "#Target#不再因恐魔而惊恐。", "_t")
t("chaos", "混沌", "effect subtype")
t("damage", "伤害", "effect subtype")
t("insanity", "疯狂", "effect subtype")
t("Chaos Orbs", "混沌之球", "_t")
t("%d stacks, +%d%% to all damage dealt.", "%d 层，+%d%% 所有造成的伤害。", "tformat")
t("horror", "恐怖", "effect subtype")
t("blight", "枯萎", "effect subtype")
t("Putrescent Pustule", "腐败脓包", "_t")
t("%d pustules increasing resistance by %d%%.", "%d 脓包，增加 %d%% 全部抗性。", "tformat")
t("eat", "吞食", "effect subtype")
t("digest", "消化", "effect subtype")
t("Digesting", "消化中", "_t")
t("Digesting %s.", "消化%s中。", "tformat")
t("#Target# swallows a foe.", "#Target#吞噬了敌人。", "_t")
t("#Target# has finished digesting.", "#Target#消化完成。", "_t")
t("The victim in your stomach seems to still be alive: '#CRIMSON#%s'", "你体内的猎物似乎仍然活着：'#CRIMSON#%s'", "logPlayer")
t("The victim in your stomach finally dies from the painful agony.", "你体内的猎物在痛苦中死去了。", "logPlayer")
t("pain", "痛苦", "effect subtype")
t("torture", "折磨", "effect subtype")
t("tentacles", "触手", "effect subtype")
t("leech", "吸血", "effect subtype")
t("Inner Tentacles", "内部触手", "_t")
t("Life leech %d%% chance, %d%% power.", "%d%% 吸血几率，%d%% 强度。", "tformat")
t("#Target# is empowered by the pain of its victim.", "#Target#被牺牲者的痛苦强化。", "_t")
t("#Target# is less powerfull.", "#Target#的力量减弱了。", "_t")
t("morph", "变形", "effect subtype")
t("Horrific Display", "恐魔具现化", "_t")
t("Appearance changed to an horror, everything is hostile to it.", "外貌变化为恐魔，令其他人和它敌对。", "tformat")
t("#PURPLE##Target# turns into an horror.", "#PURPLE##Target#变成了恐魔。", "_t")
t("#Target# is back to normal.", "#Target#恢复了正常。", "_t")
t("%s is pulled in!", "%s 被拉了进去！", "logSeen")
t("darkness", "暗影", "effect subtype")
t("gore", "血肉", "effect subtype")
t("Dissolved Face", "溶解之脸", "_t")
t("Blood and gore cover the target, dealing %0.2f darkness damage and %0.2f blight damage per disease.", "目标被血肉覆盖，每回合每种疾病额外造成 %0.2f 暗影和 %0.2f 枯萎伤害。", "tformat")
t("#Target# is covered in gore.", "#Target#被血肉覆盖。", "_t")
t("#Target# is no longer covered in gore.", "#Target#不再被血肉覆盖。", "_t")
t("fear", "恐惧", "effect subtype")
t("Glimpse of True Horror", "一瞥真惧", "_t")
t("Target briefly saw what True Horror means, deeply scaring it. %d%% chances to fail using a talent.", "目标被真正的恐惧吓倒，%d%% 几率使用技能失败。", "tformat")
t("#Target# saw true horror.", "#Target#看到了真正的恐怖。", "_t")
t("#Target# is less afraid.", "#Target#不再那么恐惧了。", "_t")
t("Empowered by the fear of its foes, darkness and blight damage penetration increased by %d%%.", "被敌人的恐惧强化，获得 %d%% 暗影和枯萎抗性穿透。", "tformat")
t("#Target# is empowered by the fear of #hisher# foes.", "#Target#被#hisher#敌人的恐惧强化。", "_t")
t("stone", "石", "effect subtype")
t("Writhing Hairs", "蜿蜒之发", "_t")
t("Half turned to stone, reducing movement speed by %d%% and 35%% chances to shatter on damage, increasing damge taken by %d%%.", "半石化中，移动速度降低 %d%%，受到伤害时有 35%% 几率碎裂，使该次伤害降低至原伤害的 %d%%。", "tformat")
t("#Target# is half-turned to stone.", "#Target#被半石化。", "_t")
t("#Target# looks less like a statue.", "#Target#不再被石化。", "_t")
t("temporal", "时空", "effect subtype")
t("Split", "分裂", "_t")
t("Faded from time, reducing damage taken by %d%% and all damage dealt by %d%%.", "从时间线上消失，减少 %d%% 受到的伤害和 %d%% 造成的伤害。", "tformat")
t("#Target# is removed from the timeline!", "#Target#被从时间线上移除！", "_t")
t("+Split", "+分裂", "_t")
t("#Target# returns to normal time.", "#Target#返回正常时间。", "_t")
t("-Split", "-分裂", "_t")
t("Halo of Ruin", "毁灭光环", "_t")
t("Increases spell critical chance by %d%%. At 5 stacks, next Nether spell is empowered.", "增加法术暴击率 %d%%，在 5 层时，下一个彼世法术获得加成。", "tformat")
t("%d Halo of Ruin", "%d 毁灭光环", "tformat")
t("Voidburn", "虚空灼烧", "_t")
t("The target has been seared by the void, taking %0.2f darkness and %0.2f temporal damage each turn.", "目标被虚空灼烧，每回合受到 %0.2f 暗影和 %0.2f 时空伤害。", "tformat")
t("#Target# is ignited by voidfire!", "#Target#被虚空之火点燃", "_t")
t("+Voidburn", "+虚空灼烧", "_t")
t("#Target# is no longer ignited.", "#Target#不再被点燃。", "_t")
t("-Voidburn", "-虚空灼烧", "_t")
t("Dark Whispers", "黑暗低语", "_t")
t("The target is being driven mad by the void, taking %0.2f darkness damage per turn and reducing all powers by %d.", "目标被虚空压迫至疯狂，每回合受到 %0.2f 点暗影伤害并且降低 %d 点全部强度。", "tformat")
t("#Target# is haunted by the void!", "#Target#被虚空折磨！", "_t")
t("+Dark Whispers", "+黑暗低语", "_t")
t("#Target#'s whispers fade.", "#Target#的低语消退了。", "_t")
t("-Dark Whispers", "-黑暗低语", "_t")
t("Hideous Visions", "惊骇幻象", "_t")
t("The target is being distracted by a hallucination, reducing all damage dealt to non-hallucinations targets by %d%%.", "目标被幻觉所困，降低其对非幻觉单位造成的伤害 %d%%。", "tformat")
t("Cacophony", "心灵尖啸", "_t")
t("The target is overwhelmed by voices from the void, giving them a 20%% higher chance to spawn hallucinations from Dark Whispers and causing them to take an additional %d%% temporal damage from Dark Whispers and Hideous Visions.", "目标被虚空之声淹没，让他们从黑暗低语中产生幻觉的几率增加 20%%，并使他们从黑暗低语和失智冲击中受到额外 %d%% 时空伤害。", "tformat")
t("#Target#'s mind is shattered by the void!", "#Target#的精神被虚空粉碎！", "_t")
t("+Cacophony", "+心灵尖啸", "_t")
t("#Target# seems more focused.", "#Target#恢复了理智。", "_t")
t("-Cacophony", "-心灵尖啸", "_t")
t("Entropic Wasting", "熵能衰竭", "_t")
t("The target is wasting away from entropic forces, taking %0.2f damage per turn.", "目标正因熵之力而衰竭，每回合受到 %0.2f 伤害。", "tformat")
t("#Target# is wasting away!", "#Target#正在逐渐衰竭！", "_t")
t("+Entropic Wasting", "+熵能衰竭", "_t")
t("#Target#'s is no longer wasting away.", "#Target# 不再被消耗。", "_t")
t("-Entropic Wasting", "-熵能衰竭", "_t")
t("#{bold}##LIGHT_STEEL_BLUE#%s loses %d health to the entropy.#{normal}##LAST##", "#{bold}##LIGHT_STEEL_BLUE#%s受熵能影响流失%d生命值。#{normal}##LAST##", "logSeen")
t("#{bold}##RED#%s loses %d health and is almost overcome by the entropy!#{normal}##LAST##", "#{bold}##RED#%s受熵能影响流失%d生命值，并几乎被熵能吞噬！#{normal}##LAST##", "logSeen")
t("Entropic Gift", "熵之礼物", "_t")
t("The full force of entropy has been brought to bear on the target, inflicting %0.2f darkness and %0.2f temporal damage each turn.", "全部熵之力都施加于目标身上，每回合造成 %0.2f 暗影和 %0.2f 时空伤害。", "tformat")
t("#Target# is consumed by entropy!", "#Target#被熵能吞噬！", "_t")
t("+Entropic Gift", "+熵之礼物", "_t")
t("#Target# has survived the entropic gift.", "#Target#从熵能中存活。", "_t")
t("-Entropic Gift", "-熵之礼物", "_t")
t("prophecy", "预言", "effect subtype")
t("Prophecy of Madness", "疯狂预言", "_t")
t("The target is doomed to madness. All talent cooldowns are increased by %d%%.", "目标注定陷入疯狂。所有技能冷却时间增加 %d%%。", "tformat")
t("#Target# is doomed to madness!", "#Target#被预言逼疯！", "_t")
t("+Prophecy of Madness", "+疯狂预言", "_t")
t("#Target# is free from the prophecy.", "#Target#脱离预言的影响。", "_t")
t("-Prophecy of Madness", "-疯狂预言", "_t")
t("%s talent '%s%s' is energized by the revelation!", "启示使%s技能'%s%s'的冷却时间缩短了！", "logSeen")
t("Prophecy of Ruin", "毁灭预言", "_t")
t("The target is doomed to ruin.  On falling below 75%%, 50%% or 25%% life all enemies in radius %d will take %0.2f darkness damage", "目标被诅咒进入毁灭状态。当生命值降低至 75%%, 50%% 或 25%% 时，%d 格内敌人将受到 %0.2f 暗影伤害。", "tformat")
t("#Target# is doomed to ruin!", "#Target#被预言毁灭！", "_t")
t("+Prophecy of Ruin", "+毁灭预言", "_t")
t("-Prophecy of Ruin", "-毁灭预言", "_t")
t("Prophecy of Treason", "背叛预言", "_t")
t("The target is doomed to treason. Each turn they have a %d%% chance to attack an adjacent creature.  If no creatures are adjacent they will attack themself.", "目标被诅咒进入背叛状态。每回合按 %d%% 的速率累积背叛进度；若目标抵抗，该回合的累积速率减半（而非完全阻止）。当累积进度达到阈值时，目标会攻击一个相邻生物；若无相邻生物则攻击自身，触发后进度减少 100（而非清零），超出阈值的部分会保留并继续累积。", "tformat")
t("#Target# is doomed to treason!", "#Target#因预言背叛！", "_t")
t("+Prophecy of Treason", "+背叛预言", "_t")
t("-Prophecy of Treason", "-背叛预言", "_t")
t("#F53CBE#%s struggles to resist the prophecy.", "#F53CBE#%s试图抵抗预言。", "logSeen")
t("#F53CBE#%s succumbs to the prophecy, attacking %s!", "#F53CBE#%s屈服于预言，攻击了%s！", "logSeen")
t("#F53CBE#%s succumbs to the prophecy, striking themself!", "#F53CBE#%s屈服于预言，攻击了自己！", "logSeen")
t("Mark of Treason", "背叛印记", "_t")
t("When this target is damaged %d%% of the damage will also be done to the source of this effect.", "当目标受到伤害时，效果来源也受到目标所受伤害的 %d%%。", "tformat")
t("#Target# is linked through the prophecy.", "#Target#被预言联结。", "_t")
t("+Mark of Treason", "+背叛印记", "_t")
t("#Target# prophetic link disappears.", "#Target#的预言联结消失了。", "_t")
t("-Mark of Treason", "-背叛印记", "_t")
t("#ORANGE#The wounds of #Source# appear on #target#!#LAST#", "#ORANGE##Source#身上的创伤出现在#target#身上！#LAST#", "delayedLogMessage")
t("#CRIMSON#(%d linked)#LAST#", "#CRIMSON#(%d 伤害链接)#LAST#", "tformat")
t("Nihil", "空无", "_t")
t([[The target is engulfed in entropy, reducing the duration of new beneficial effects and increasing the duration of new negative effects by %d%%.
This effect will fade in 2 turns if the source is not in line of sight.]], [[目标被熵覆盖，仅缩短新施加的非“其他”类有益状态并延长新施加的非“其他”类负面状态 %d%% 持续时间（不影响“其他”类效果）。
若效果来源不在视野内，则该效果会在 2 回合后消失。]], "tformat")
t("#Target# is wreathed in entropy.", "#Target#被熵覆盖。", "_t")
t("#Target# is free of the entropy.", "#Target#脱离熵影响。", "_t")
t("#LIGHT_RED#A void annihilator manifests from %s!", "#LIGHT_RED#一个虚空歼灭者从%s的身上出现了！", "logSeen")
t("Atrophy", "衰亡", "_t")
t([[The target's mind and body is wasting away, reducing all stats by %d.
This effect will fade in 2 turns if the source is not in line of sight.]], [[目标的身体和精神迅速老化、凋零，所有属性降低 %d。
若效果来源不在视野内，则该效果会在 2 回合后消失。]], "tformat")
t("#Target# is wasting away.", "#Target#开始凋零。", "_t")
t("#Target# regains their strength.", "#Target#恢复了力量。", "_t")
t("speed", "速度", "effect subtype")
t("Temporal Feast", "时空盛宴", "_t")
t("Increases spellcast speed by %d%%.", "施法速度增加%d%%。", "tformat")
t("%d Temporal Feast", "%d 时空盛宴", "tformat")
t("Void Rift", "虚空裂隙", "_t")
t("The target has %d active void rift(s).", "目标拥有 %d 个激活的虚空裂隙。", "tformat")
t("%d Void Rifts", "%d 虚空裂隙", "tformat")
t("Accelerate", "窃速", "_t")
t("Moving at extreme speed (%d%% faster).  Any action other than movement will cancel it.", "超高速移动（移动速度增加%d%%）。所有非移动的操作都会取消这一效果。", "tformat")
t("#Target# is moving at extreme speed!", "#Target#走得飞快！", "_t")
t("+Accelerate", "+窃速", "_t")
t("#Target# slows down.", "#Target#速度减慢了。", "_t")
t("-Accelerate", "-窃速", "_t")
t("Suspend", "暂停", "_t")
t("The target is removed from the normal time stream, unable to act but unable to take any damage. Each turn, beneficial effects decrease in duration.", "目标从常规时间流中移除，无法行动，免疫伤害。每回合有益效果正常衰减。", "_t")
t("#Target# is removed from time!", "#Target#被从时间中移除！", "_t")
t("+Suspend", "+暂停", "_t")
t("#Target# is returned to normal time.", "#Target#返回了正常时间。", "_t")
t("-Suspend", "-暂停", "_t")
t("The target is removed from the normal time stream, unable to act but unable to take any damage. Each turn, negative effects and cooldowns will decrease in duration.", "目标从常规时间流中移除，无法行动，免疫伤害。暂停结束时，非“其他”类且不会在无时间状态下自行衰减的负面效果，以及技能冷却时间会缩短。", "_t")
t("Jinxed", "不幸", "_t")
t([[The target has %d reduced saves and defense, and %d%% reduced critical chance.
This effect will fade in 2 turns if the source is not in line of sight.]], [[目标豁免和闪避降低 %d，暴击率降低 %d%%。
若效果来源不在视野内，则该效果会在 2 回合后消失。]], "_t")
t([[The target has %d reduced saves and defense, %d%% reduced critical chance, and %d%% chance to fail talent use.
This effect will fade in 2 turns if the source is not in line of sight.]], [[目标豁免和闪避降低 %d，暴击率降低 %d%%，使用技能有 %d%% 几率失败。
若效果来源不在视野内，则该效果会在 2 回合后消失。]], "_t")
t("%d Jinx", "%d 不幸", "tformat")
t("Fortune", "幸运", "_t")
t("The target has %d increased saves and defense, and %d%% increased critical chance.", "目标豁免和闪避增加 %d（仅 1 层时实际降低，2 层起才如数增加），暴击率增加 %d%%（始终增加）。", "_t")
t("The target has %d increased saves and defense, %d%% increased critical chance, and %d%% chance to avoid all damage.", "目标豁免和闪避增加 %d，暴击率增加 %d%%，有 %d%% 几率闪避所有伤害。", "_t")
t("Unravelling", "解构", "_t")
t("The target is being erased from reality. Each time a magical effect is applied, they will take %0.2f darkness damage and %0.2f temporal damage. If 5 effects are applied, a powerful void horror will appear.", "目标正被从现实中抹去。每当一个负面魔法效果施加到目标身上，它就会受到 %0.2f 暗影和 %0.2f 时空伤害。当施加了 5 个负面魔法效果后，强大的虚空恐魔将出现。", "tformat")
t("#Target# is being erased from reality!", "#Target#被从现实中移除！", "_t")
t("#Target# has survived the unraveling.", "#Target#从解构效果中存活。", "_t")
t("Fatebreaker", "打破宿命", "_t")
t("The target has tied itself to the fate of another. If it dies, it's chosen target will die in it's place and it will be healed by %d for each stack of Fortune and Jinx.", "目标将自身的命运和另一个人相连，当它死亡时，选择的目标将代替它死亡。此时，自身的幸运层数和所选目标身上的不幸层数会被消耗；若所选目标有不幸，则按其层数治疗，否则按自身的幸运层数治疗，每层恢复 %d 点生命。", "tformat")
t("#Target# intertwines it's fate!", "#Target#的命运被联结！", "_t")
t("#Target#'s fate is no longer linked to another.", "#Target#的命运不再被联结。", "_t")
t("Redirecting all damage as temporal and darkness to %s.", "所有伤害转为时空和暗影类型，转移至 %s。", "tformat")
t("Decaying Ground", "腐朽之地", "_t")
t("All cooldowns increased by %d%%.", "所有技能冷却时间增加 %d%%。", "tformat")
t("#Target# is caught in decaying ground.", "#Target#被腐朽之地覆盖。", "_t")
t("#Target# is free from the decaying ground.", "#Target#脱离腐朽之地。", "_t")
t("disease", "疾病", "effect subtype")
t("Crippling Disease", "残废恶疾", "_t")
t("The target is infected by a disease, reducing its speed by %d%% and doing %0.2f blight damage per turn.", "目标被疾病感染，速度降低 %d%%，每轮受到 %0.2f 枯萎伤害。", "tformat")
t("#Target# is afflicted by a crippling disease!", "#Target#被残废恶疾感染！", "_t")
t("#Target# is free from the crippling disease.", "#Target#脱离残废恶疾影响。", "_t")
t("Defiled Blood", "污血", "_t")
t("Covered in defiled blood, healing the source for %d%% of all damage done.", "被污血覆盖的目标对效果来源造成伤害时，效果来源恢复该伤害的 %d%%。", "tformat")
t("#Target# is covered in black blood!", "#Target#被黑血覆盖！", "_t")
t("#Target# is clear from the black blood.", "#Target#脱离黑血影响。", "_t")
t("teleport", "传送", "effect subtype")
t("Teleport: Kroshkkur", "传送：克诺什库尔", "_t")
t("The target is waiting to be recalled back to Kroshkkur.", "目标在等待传送至克诺什库尔。", "_t")
t("#CRIMSON#Kroshkkur is destroyed, there is nothing to teleport to.", "#CRIMSON#克诺什库尔被摧毁了，无法传送到那里。", "log")
t("There are creatures that could be watching you; you cannot take the risk of teleporting to Kroshkkur.", "周围有敌对生物能看到你，你不能冒险在这个时候传送至克诺什库尔。", "log")
t("You are yanked out of this place!", "你“呼”的一下被带离了这个地方！", "logPlayer")
t("Space restabilizes around you.", "你周围的空间稳定了下来。", "logPlayer")
t("book", "书", "effect subtype")
t("Forbidden Tome", "禁忌之书", "_t")
t("Slowly transfered to a Forbidden Tome.", "正在被缓慢转移到禁忌之书。", "_t")
t("#Target# is entering a Forbidden Tome!", "#Target#正在进入禁忌之书！", "_t")
t("#Target# enters a Forbidden Tome!", "#Target#进入了禁忌之书！", "_t")
t("Inside Forbidden Tome: \"Home, Horrific Home\" for %d turns.", "进入禁忌之书中：\"家，可怕的家 \" %d 回合。", "tformat")
t("Forbidden Tome Cooldown", "禁忌之书冷却", "_t")
t("Unable to enter Forbidden Tomes.", "无法进入禁忌之书。", "_t")
t("Wrath of the Wilds", "自然之怒", "_t")
t("%d%% chance to stun any foes hit.", "%d%% 几率震慑被击中的敌人；每回合第一次符合条件的命中必定触发震慑，不受该几率限制；之后的命中按该几率判定，且同一目标每回合最多被震慑一次。", "tformat")
t("protection", "保护", "effect subtype")
t("Warborn", "为战而生", "_t")
t("Reduces all damage taken by %d%%.", "减少 %d%%所有受到的伤害。", "tformat")
t("opness", "无比强大", "effect subtype")
t("Awoken", "觉醒", "_t")
t([[True power is revealed!

All debuffs removed and all talent cooldowns reset on application.

Each turn a radius 2 explosion will occur in a random space dealing %0.2f darkness and temporal damage and destroying any diggable walls.]], [[真正的力量正被揭示！

施加该效果时，移除所有负面效果（“其他”类效果除外）并重置所有技能冷却时间。

每回合，一个半径 2 码的爆炸会在一个随机空间爆发，造成 %0.2f 暗影和时空伤害，并摧毁所有可挖掘的墙。]], "tformat")
t("entropy", "熵", "effect subtype")
t("Total Collapse", "完全崩溃", "_t")
t("Your body can not function properly here, it is slowly wasting away. Each turn you take %0.2f void damage and any new debuff on you lasts %d%% longer. Each turn those penalties increase until the effect is removed.", "你的身体无法正常运转，被逐渐损耗。每回合你受到 %0.2f 虚空伤害，任何新施加的负面效果（“其他”类效果除外）持续时间延长 %d%%。每回合这些惩罚都会增长，直到效果结束。", "tformat")
t("threat", "威胁", "effect subtype")
t("Save Kroshkkur", "拯救克诺什库尔", "_t")
t("Kroshkkur is still under threat from %s.", "克诺什库尔仍处于 %s 威胁中。", "tformat")
t("#CRIMSON#You waited too long, Kroshkkur has been destroyed by %s!", "#CRIMSON#你等得太久了，克诺什库尔被%s摧毁了！", "say")
t("Covered in Gastric Fluids", "被胃液覆盖", "_t")
t("Reduces all damage taken by %d%% and remove all detrimental effects on application.", "降低所有受到的伤害 %d%%。施加该效果的时候会解除所有负面效果。", "tformat")
t("debilitate", "虚弱", "effect subtype")
t("Reduces all damage done by %d%% and increase all detrimental effects durations by 6 turns on application.", "降低所有造成的伤害 %d%%。施加该效果的时候会将所有负面效果持续时间延长6回合。", "tformat")
t("blind", "致盲", "effect subtype")
t("Blinded", "致盲", "_t")
t("The target is blinded, unable to see anything.", "目标被致盲，什么都看不见。", "_t")
t("#Target# loses sight!", "#Target#失明了！", "_t")
t("+Blind", "+致盲", "_t")
t("#Target# recovers sight.", "#Target#恢复了视力。", "_t")
t("-Blind", "-致盲", "_t")
t("confusion", "混乱", "effect subtype")
t("madness", "疯狂", "effect subtype")
t("Lost in a weird place", "迷失在奇怪的地方", "_t")
t("The target is starting to get mad (%d stacks), reducing mind damage resistance by %d%%, mental save by %d, confusion resistance by %d%%, generating %0.1f insanity per turn.", "目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，%d%% 混乱免疫，每回合获得 %0.1f 疯狂值。", "tformat")
t("wound", "创伤", "effect subtype")
t("cut", "流血", "effect subtype")
t("fail", "失败", "effect subtype")
t("Glass Splinters", "玻璃碎片", "_t")
t("Nasty glass splinters that make you bleed, doing %0.2f arcane damage per turn. Deals %0.2f arcane damage on move. Talents have %d%% chances to fail.", "令人讨厌的玻璃碎片令你流血，每回合造成 %0.2f 奥术伤害。行走时造成 %0.2f 奥术伤害。技能失败率增加 %d%%。", "tformat")
t("#Target# starts to bleed due to glass splinters.", "#Target#因为玻璃碎片开始流血。", "_t")
t("#Target# stops bleeding.", "#Target#停止流血。", "_t")
t("will", "意志", "effect subtype")
t("domination", "支配", "effect subtype")
t("Persistant Will", "坚定意志", "_t")
t("Convinced that arcane users are filth to be destroyed.", "相信奥术使用者应该被消灭。", "tformat")
t("#PURPLE##Target# is convinced arcane users must be destroyed.", "#PURPLE##Target#相信奥术使用者应该被消灭。", "_t")
t("#Target# looks more kindly toward arcane users.", "#Target#不再痛恨奥术使用者。", "_t")
t("Twisted Evolution: Speed", "扭曲进化：速度", "_t")
t("The target is evolved increasing its global speed by %d%%.", "目标进化了，整体速度增加 %d%%。", "tformat")
t("#Target# is evolved and acting faster!", "#Target#进化了，速度更快了！", "_t")
t("#Target# is no longer evolved to move faster.", "#Target#解除了进化，速度减慢了。", "_t")
t("Twisted Evolution: Form", "扭曲进化：形体", "_t")
t("The target is evolved increasing all its stats by %d.", "目标进化了，全属性增加%d。", "tformat")
t("#Target#'s body is evolved!", "#Target#的身体进化了！", "_t")
t("#Target#'s body' is no longer evolved.", "#Target#的身体解除进化。", "_t")
t("Twisted Evolution: Power", "扭曲进化：力量", "_t")
t("The target is evolved increasing its damage by %d%%.", "目标进化了，全伤害增加 %d%%。", "tformat")
t("#Target# is evolved to deal more damage!", "#Target#进化了，伤害增加！", "_t")
t("#Target# is no longer evolved to deal more damage.", "#Target#解除进化，伤害降低。", "_t")
t("Shoes of Moving Slowly", "缓步之靴", "_t")
t("Stay put, increasing your armour and defense by %d.", "原地不动，增加 %d 护甲和防御。", "tformat")
t("Entropic Feedback", "熵能反馈", "_t")
t("The target healing is distorted by entropy for %d%% of the healing done over 8 turns.", "目标的 %d%% 治疗将被熵扭曲，并在 8 回合内造成等量伤害。", "tformat")
t("#Target# is enveloped with entropic forces!", "#Target#被熵能覆盖！", "_t")
t("#Target# is no longer enveloped by entropic forces.", "#Target#不再被熵能覆盖。", "_t")
t("armor", "护甲", "effect subtype")
t("Horrific Fortress", "恐怖堡垒", "_t")
t("All damages except physical reduced by %d as long as %s is alive.", "只要%s还存活，受到的所有非物理伤害降低 %d 点。", "tformat", {2,1})
t("#Target# is bolstered at the sight of the horror!", "#Target#在恐魔的视线中被强化了！", "_t")
t("#Target# is less armoured.", "#Target#的护甲降低了。", "_t")
-- untranslated text
--[==[
t("S.M.A.C.K.", "S.M.A.C.K.", "_t")
--]==]


------------------------------------------------
