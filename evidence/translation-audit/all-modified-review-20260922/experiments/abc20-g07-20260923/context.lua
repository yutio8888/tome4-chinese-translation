section "tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua"

t("13%% chance to trigger a Blood Spray cast of level %d", "13%%几率触发等级%d的鲜血喷射", "tformat")
t("Reduces duration of detrimental effects by 40%", "降低负面效果的持续时间40%", "_t")
t("+2 to all Demon Seeds, Spellblaze and Demonic Pact talents", "所有恶魔种子，魔法大爆炸系和恶魔契约系技能等级+2", "_t")
t("%s (%d/%d life, level %d)", "%s (%d/%d 生命值，等级 %d)", "tformat")
t("demon seed", "恶魔种子", "_t")
t("The seed of a demon.", "恶魔的种子。", "_t")
t("Demon status: %s.", "恶魔状态：%s。", "tformat")
t("alive (%d%% life)", "存活 (%d%% 生命值)", "tformat")
t("dead (can not be summoned)", "死亡（无法召唤）", "_t")
t("#CRIMSON#You extract a %s and add it to your inventory.", "#CRIMSON#你提取了一个%s并将其收入物品栏。", "logPlayer")
t("#CRIMSON#You extract a %s and bind it to your %s.", "#CRIMSON#你提取了一个%s并将其附着于你的%s。", "logPlayer")
t("#CRIMSON#You feed vim into your %s, increasing its level to %d and healing it.", "#CRIMSON#你将活力注入你的 %s，将其等级提升到 %d，并治疗了它。", "logPlayer")
t("Demon Seed", "恶魔之种", "talent name")
t("You require a weapon and a shield to use this talent.", "你需要一把武器一个盾牌来施展这个技能。", "logPlayer")
t([[Strike a blow with your weapon for %d%% blight damage.
		If the attack hits a demonic seed tries to take hold inside your foe and you follow up with a shield strike dealing %d%% damage and dazing your target for %d turns.
		
		The seed requires a powerful host to nourish it and can only take hold in creatures that are worth experience and that are not summoned demons.
		The chance for the seed to take hold is based on the creatures rank:
		%sNormal#LAST#:  5%%
		%sElite#LAST#:  20%%
		%sRare#LAST# or %sUnique#LAST#:  50%%
		%sBoss#LAST#:  100%%
		When the host dies the seed fills with the vim of the dying creature and turns into a specific demon seed that can be used to summon that demon.
		If you already have a seed of the same time in your inventory or equipment it will instead increase its level if the host was of higher level than the seed and the demon inside will regenerate %d%% health and resurrect if it was dead.

		Higher talent levels allow for more powerful demon types.
		Implanting a seed into unique demons, if successful, will always try to grant a seed of that type, if available.]], [[对目标造成 %d%% 枯萎武器伤害。
		如果攻击命中，你会将恶魔种子植入目标体内，然后用盾牌攻击目标，造成 %d%% 盾牌伤害并眩晕 敌人 %d 回合。

		种子需要足够强大的宿主来成长，它只能寄生在值得获取经验值的生物体内，不能寄生在被召唤的恶魔体内。
		种子的存活几率基于宿主的级别：
		%s普通生物#LAST#:5%%
		%s精英生物#LAST#:20%%
		%s稀有#LAST#与%s史诗生物#LAST#:50%%
		%sBoss#LAST#:100%%
		当宿主死亡时，种子将吸收宿主的活力，成长为一个特定的恶魔种子，能用于召唤恶魔。
		如果你的背包或装备上已经有了同类的恶魔种子，且宿主等级高于恶魔的等级，它会提升种子的等级。此外，里面的恶魔会恢复 %d%% 生命值，如果已死则会被复活。

		高技能等级将带来更强大的种子。
		如果成功将种子植入史诗生物（Unique）的体内，且它有对应的恶魔种子的话，你必定会获得该恶魔种子。]], "tformat")
t("Bind Demon", "恶魔结合", "talent name")
t("Summon demon", "召唤恶魔", "_t")
t("Which seed to use:", "使用哪个恶魔种子：", "_t")
t("Not enough space to summon!", "没有足够的空间召唤！", "logPlayer")
t([[Your knowledge of demonic forces grows, allowing you to bind more seeds to you and to summon demons.
		You channel your arcane corruption through a demon seed to temporarily summon the corresponding demon for %d turns.
		Summoned demons can regen their life and resummoning them keeps the life they had when they were last used.
		If the demon dies it will not be available for summoning anymore until resurrected.
		This spell can summon demons from any seeds available in either your equipment or inventory.

		As you learn to bind more easily you can also use more seeds:
		At level 2 it lets you bind a seed to your first ring.
		At level 3 it lets you bind a seed to your shield.
		At level 4 it lets you bind a seed to your second ring.
		At level 5 it lets you bind a seed to your main body armour.
		]], [[你对恶魔力量的理解增长了，你可以将更多种子与装备结合，且可以召唤恶魔
		你能通过恶魔种子来临时召唤对应的恶魔 %d 回合。
		召唤出来的恶魔能回复生命，并且保持上一次召唤结束时的生命值。
		如果恶魔死亡，将不能再使用同一个种子进行召唤，直到它被复活为止。
		这一技能可以召唤你装备或背包里的任何恶魔种子。

		随着你对恶魔力量的了解更加深入，你能将更多的种子与你的装备结合。
		技能等级 2 时你能将种子与第一个戒指结合。
		技能等级 3 时你能将种子与盾牌结合。
		技能等级 4 时你能将种子与第二个戒指结合。
		技能等级 5 时你能将种子与护甲结合。
		]], "tformat")
t("Twisted Portal", "扭曲传送", "talent name")
t("Select a teleport location...", "选择传送位置…", "logPlayer")
t("The targetted phase door fizzles and works randomly!", "指定的相位之门失效，改为随机传送！", "logPlayer")
t([[Teleports you randomly within a small range of up to %d grids with %d precision.
		In the spot you left you will summon a random demon from your seeds for %d turns.
		If the target area is not in line of sight, there is a chance the spell will fizzle.
		This spell requires an unsummoned, alive, demon seed equiped in a worn equipment to work.
		The range will increase with your Spellpower.]], [[传到 %d 码外的一个位置，误差 %d。
		在离开的位置，你将随机召唤一个恶魔，持续 %d 回合。
		如果目标地点不在视线内，有一定几率失败。
		该技能需要你的装备上附着有至少一个未召唤的存活的恶魔种子。
		传送距离受法术强度加成。]], "tformat")
t("Doom Concordat", "末日契约", "talent name")
t("#CRIMSON#Your %s is healed!", "#CRIMSON#你的%s被治疗了！", "logPlayer")
t("#CRIMSON#Your %s is brought back to life!", "#CRIMSON#你的%s复活了！", "logPlayer")
t([[You use your demon seeds to the fullest of their potential.
		Each time you enter combat you automatically summon a random demon from your worn seeds for %d turns. Demons are only summoned if their life is over 70%% and only if not other summoned demon is from Doom Concordat.
		Each time you kill a creature a random worn demon seed with less than 100%% life will be healed for %d%% life and resurrected if it was dead and the target was an elite or more.
		In addition you feed of the arrival, departure or death of your demons, each time healing yourself for %d life.
		The healing is based on your Spellpower.]], [[你发挥你恶魔种子的全部力量。
		每当你进入战斗的时候，你将会自动从装备的种子中召唤一个随机恶魔，持续 %d 回合。恶魔只有在生命值大于 70%% 的时候才可以被召唤，且末日契约同时最多召唤一个恶魔。
		每当你杀死一个生物，你装备的不满血的随机恶魔种子将会恢复 %d%% 生命值。如果目标是精英怪以上，你可以复活一个恶魔。
		此外，每当一个恶魔降临，离开或死亡的时候，你将会受到 %d 点治疗。
		治疗量受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/demonic-strength.lua"

t("Dismember", "肢解", "talent name")
t([[Your melee attacks cripple your targets when they critically strike, lowering their movement speed by %d%% and their accuracy by %d for %d turns.
		Additionally, you gain %d%% chance to critically strike with your melee attacks.]], [[当近战攻击暴击时，致残你的目标，降低 %d%% 移动速度和 %d 命中，持续 %d 回合。
	同时，增加 %d%% 近战暴击率。]], "tformat")
t("Surge of Power", "力量之潮", "talent name")
t([[Use your stored vim to supercharge your body, recovering %d stamina and %d life.
		Additionally, you will be able to survive your HP going under 0, down to -%d HP, for the next 8 turns.
		These values will increase with your Spellpower.
		Spell criticals with this talent also effect the stamina gain.]], [[你使用体内蕴藏的活力强化自己的身体，恢复 %d 点体力值和 %d 点生命值。
	同时让你在 -%d 生命时才会死亡，此效果持续 8 回合。
	恢复值受法术强度加成。
	法术暴击也会增加这一技能恢复的体力值。]], "tformat")
t("Demonic Blood", "恶魔之血", "talent name")
t([[Demonic Blood flows through your veins, increasing your spellpower by %d and your maximum vim by %d.
		Additionally, you will recieve a bonus to all damage equal to %d%% of your current vim (Currently %d%%).]], [[你体内涌动着恶魔之血，增加 %d 点法术强度和 %d 点活力上限。
	同时获得相当于当前活力 %d%% 的全伤害加成（当前 %d%%）。]], "tformat")
t("Abyssal Shield", "深渊护盾", "talent name")
t([[Surround yourself with a defensive aura, increasing armor by %d, and inflicting %0.2f fire and %0.2f blight damage to all attacking foes.
Additionally, your vim will enhance your defences, reducing all damage by %d%% of your current vim (currently %d), but never reducing by more than half of the original damage. This will cost vim equal to 5%% of the damage blocked.
The damage will scale with your Spellpower.]], [[深渊气息围绕着你，增加 %d 点护甲，增加 %0.2f 点火焰、%0.2f 点枯萎近战反击伤害。
	同时你的活力会增强你的防御，减少相当于当前活力 %d%% 的伤害（目前为 %d 点），但不会减少超过原伤害的一半。此效果会消耗等同于 5%% 减少伤害值的活力。
	伤害值受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/doom-covenant.lua"

t("Dark Reign", "黑暗支配", "talent name")
t([[Your affinity for the shadows grow stronger.
		Whenever one of your spells deal darkness damage you have a %d%% chance to gain 8%% to all damage affinity for 8 turns.
		If you kill a creature with darkness damage this effect always triggers.
		You can only gain one stack of Dark Reign per turn.
		This effect stacks multiplicatively up to %d times.]], [[你与阴影的联系更加紧密了。
		每次你使用法术造成暗影伤害时，你有 %d%% 几率获得 8%% 全体伤害亲和，持续 8 回合。
		如果你用暗影伤害杀死一个生物，这一效果必定触发。
		你每回合最多只能获得一层黑暗支配效果。
		这个效果能叠加至最多 %d 层。]], "tformat")
t("Dread End", "黑暗终结", "talent name")
t([[You learn to use death around you to an even greater advantage. 
		Each time you kill or deal damage above %d%% of a creatures max life with non-darkness damage while Dark Reign is active the death will create a pool of dark energies of radius 1 for 5 turns.
		This pool spawns on top of a random enemy within radius %d.
		Any foes standing inside will take %0.2f darkness damage each turn.
		This effect can only happen once per turn.
		The damage increases with spellpower.
		At talent level 3 your Dark Reign buff also protects you from death until reaching %d life per stack.]], [[你学会利用死亡来获取力量。
		当黑暗支配开启，每次你使用非暗影伤害杀死生物或造成超过 %d%% 最大生命的伤害时，产生半径 1 的黑暗能量池，持续 5 回合。
		能量池将在半径 %d 范围内的随机敌人处生成。
		任何站在里面的敌人每回合将受到 %0.2f 点暗影伤害。
		这个效果每回合最多触发一次。
		伤害受法术强度加成。
		技能等级 3 或以上时，当你处于黑暗支配状态下，每一层状态使你获得 -%d 生命底限。]], "tformat")
t("Blood Pact", "鲜血契约", "talent name")
t([[Pay %d%% of your current life and gain 100%% darkness damage conversion for 1 turns.
			If Dark Reign is active you also gain %d stamina and %d vim per stack.]], [[支付 %d%% 当前生命值，1 回合内你造成的所有伤害转化为黑暗伤害。
		如果黑暗支配开启，每有一层，你获得 %d 体力与 %d 活力。]], "tformat")
t("Erupting Darkness", "黑暗爆发", "talent name")
t("raging volcano", "喷发中的火山", "_t")
t([[When Dread End creates pools of darkness you can focus your raging thoughts on them to make them erupt into volcanos.
		Up to %d pools in radius %d will erupt, producing a volcano for %d turns.
		Each turn the volcano will send out fiery boulders that deal %0.2f fire and %0.2f physical damage.
		The effects will improve with your Spellpower.]], [[当黑暗终结制造出黑暗能量池时，你能将狂怒集中于这些能量池，将其转变为火山。
		至多 %d 个能量池将会喷发（半径 %d 内），转化为火山，持续 %d 回合。
		每回合火山将喷射火焰巨石，造成 %0.2f 火焰与 %0.2f 物理伤害。
		效果受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/doom-shield.lua"

t("Osmosis Shield", "渗透护盾", "talent name")
t("You require a weapon and a shield to use this talent.", "你需要一把武器一个盾牌来施展这个技能。", "logPlayer")
t("#SLATE#(%d turned into osmosis)#LAST#", "#SLATE#(%d 转化为渗透)#LAST#", "tformat")
t([[You infuse your shield with the energies of Urh'Rok, bringing about a magical shield that heals you for the first points of all damage you receive (based on your shield's block value) over 3 turns. This effect stacks.
		Amount is 5 + %d%% of your shield block value (currently %d).
		At level 3 if a damage dealt is at least twice as high you have %d%% chance to also remove a physical detrimental effect. This effect can only happen once per turn.
		This spell disabled automatically on rest or run.
		#{bold}#Activating the shield takes no time but de-activating it does.#{normal}#
		The damage increases with spellpower.]], [[你的盾牌充满了恶魔能量，带来一层魔法护盾：在 3 回合内，你受到的所有伤害的最初几点（基于你的盾牌格挡值）将转化为治疗。此效果可以叠加。
		治疗量等于 5 + %d%% 格挡值（当前 %d 点）。
		技能等级 3 时，如果伤害在治疗量两倍以上，有 %d%% 几率额外移除一个物理负面效果。此效果每回合只能触发一次。
		在休息和跑步时，该技能自动终止。
		#{bold}#开启护盾不消耗时间，关闭护盾消耗时间。#{normal}#
		伤害受法术强度加成。]], "tformat")
t("Hardened Core", "硬化之核", "talent name")
t([[Taking example from Mal'Rok, the demon's homeworld you harden yourself.
		Increases total armour by %d%% + 10 and spellpower by %d.]], [[从恶魔家乡玛·洛克中学习，强化自身。
		增加 10 + %d%% 总护甲值，获得 %d 法术强度。]], "tformat")
t("Demonic Madness", "疯狂旋转", "talent name")
t([[You spin around madly with your shield, bashing all those around you for %d%% shield damage as darkness, confusing your foes for %d turns.
		At level 4 you also automatically block at the end.]], [[你疯狂旋转你的盾牌，攻击周围生物，造成 %d%% 暗影盾牌伤害并使其混乱 %d 回合。
		技能等级 4 时，你自动进入格挡状态。]], "tformat")
t("Blighted Shield", "枯萎之盾", "talent name")
t([[Your shield is infused with a powerful blight. Anytime you block and apply a counterstrike effect the target is also afflicted by a curse of impotence.
		Cursed creatures have all their damage decreased by %d%% for 5 turns.
		The effects will improve with your Spellpower.]], [[你的盾牌充满强大的枯萎能量。每次你格挡并附加反击状态时，目标将被虚弱诅咒感染，5 回合内降低 %d%% 伤害。
		效果受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/fearfire.lua"

t("Fearscape Shift", "炼狱之门", "talent name")
t("You can't move there.", "你不能移动至那里。", "logSeen")
t("The spell fizzles!", "法术失败了！", "logSeen")
t([[Open a gateway to the Fearscape, stepping through it to a nearby location. As you step out, a burst of fire will leave with you, dealing %0.2f demonfire damage to everyone within %d spaces and leaving flames which will deal an additional %0.2f demonfire damage over 4 turns.
		Additionally, shifting through reality enhances your awareness, allowing you to see all enemies within %d spaces for the next 3 turns.
		The damage will scale with your Spellpower and the range will increase with the talent level.]], [[开启通往恶魔空间的炼狱之门，踏入并传送到附近位置。
	当你踏出炼狱之门时，炼狱之火随之喷发，造成 %0.2f 恶魔之火伤害，伤害 %d 码内所有生物。地上的余烬会造成持续 4 回合的额外 %0.2f 恶魔之火伤害。

	穿越空间增强了你的直觉，让你能够在 4 回合内觉察到 %d 码内的所有敌对生物。

	伤害受法术强度加成，范围随技能等级增大。]], "tformat")
t("Cauterize Spirit", "灵魂焚净", "talent name")
t([[Removes all detrimental effects but causes you to burn for %d%% of your max health per effect, over 7 turns.
		This ignores all resists, defenses, and affinities.
		This does not take a turn.]], [[移除所有负面状态，但每移除一个状态，会在 7 回合内灼烧自身，受到合计 %d%% 最大生命值的伤害。
	伤害无视一切抗性、防御效果和伤害亲和。

此技能瞬发。]], "tformat")
t("Infernal Breath", "地狱吐息", "talent name")
t([[Exhale a wave of dark fire with radius %d, lasting 4 turns. Any non-demon caught in the area will take %0.2f fire damage, and flames will be left dealing a further %0.2f each turn. Demons will be healed for the same amount.
		The damage will increase with your Strength Stat, but critically hit as a spell.]], [[在 %d 码的锥形范围内，喷出持续 4 回合的暗黑火焰。
	范围内所有的非恶魔生物受到 %0.2f 火焰伤害，同时火焰会造成每回合 %0.2f 的灼烧伤害。
	恶魔受到等量的治疗。

	伤害受力量加成，该技能使用魔法暴击率。]], "tformat")
t("Maw of Urh'rok", "乌鲁洛克之口", "talent name")
t([[Your body becomes a nexus for the Fearscape, causing you to drag enemies towards you in a cone with a radius of %d, dealing %0.2f fire damage every turn.
		The damage will increase with your Spellpower.]], [[你的身体成为恶魔空间与现实的纽带，将 %d 码的锥形范围内的敌人抓过来，同时每回合造成 %0.2f 点火焰伤害。
伤害受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/heart-of-fire.lua"

t("Burning Sacrifice", "燃烧献祭", "talent name")
t([[Whenever you kill a burning enemy, you will instantly deal a melee attack against a random adjacant enemy at %d%% power. 
		Additionally, Incinerating Blows will always trigger on this attack (or your next attack), dealing %d%% of its normal damage to all enemies hit and stunning, ignoring the cooldown.
		This can only trigger once every 5 turns.]], [[每次你击杀一个燃烧的敌对生物时，会立刻对一个随机相邻敌对生物进行一次攻击，造成 %d%% 武器伤害。
	另外，焚尽强击必定被此效果触发（或者下一次攻击），对所有击中的敌对生物造成 %d%% 正常伤害并使其眩晕，无视冷却时间。
	此效果每 5 回合才能触发一次。]], "tformat")
t("Fiery Aegis", "火焰守护", "talent name")
t([[Draw in the raging fires and envelop yourself in them. Remove all burns from enemies in a radius of 5 around you, and create a shield lasting %d turns with a power of %d, increased by 15%% for each burn removed.
		When the shield ends, it releases a burst of fire in a radius of %d around you, burning all enemies for 3 turns, doing damage equal to the initial power of the shield.]], [[吸取燃烧中的烈焰，将自己包裹其中。
		除去半径 10 内的敌方生物身上的燃烧效果，同时制造一层持续 %d 轮的 %d 强度的护盾，每吸收一层燃烧效果护盾强度增加 15%%。
		当护盾效果结束时，将在半径 %d 范围内释放一次火焰爆炸，灼烧范围内的所有敌方生物 3 回合，造成等于护盾初始值的伤害。]], "tformat")
t("Devouring Flames", "吞噬之焰", "talent name")
t([[Your connection to fire nourishes you. Whenever you strike an enemy in melee, you inflict a burning curse upon them. As long as they continue to burn, you gain %0.2f health and %0.2f vim per turn.
		Each turn they remain within 10 spaces of you, all enemies with cursed flames will spread it to other burning enemies in radius 1, causing you to heal for the same amount for each enemy, as well as dealing %d fire damage on spreading.]], [[恶魔之火滋养着你。每当你的近战攻击命中敌人，便会对其施加诅咒之焰。每个受到诅咒之焰影响的敌人只要仍在燃烧，每回合都会为你恢复 %0.2f 点生命值并提供 %0.2f 点活力值。
	每回合，你半径 10 内每个受到诅咒之焰影响的敌人都有 50%% 几率，将诅咒传播给其半径 1 内尚未受诅咒的敌人，无论后者此前是否在燃烧。新受诅咒的敌人在持续燃烧期间，也会每回合为你恢复同等生命值并提供同等活力值。传播还会造成总计 %d 点火焰伤害，其中一半立即造成，另一半在接下来的 3 回合内造成。]], "tformat")
t("Blazing Rebirth", "烈焰重生", "talent name")
t("Restore yourself to full health, but take damage equal to the damage healed over %d turns. This damage is split evenly among you and all burning enemies in radius %d. Damage you take is irresistable. Damage to enemies is fire damage.", [[生命值恢复为满值，但治疗值转化为持续 %d 回合的伤害。
	伤害会平均分配给你自己和 %d 码范围内的燃烧敌对生物。
	你受到的伤害无法减免，敌对生物受到火焰伤害。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua"

t("Flame Leash", "火焰束缚", "talent name")
t([[Tendrils of flame fire from your hands in a narrow cone. Any foes caught inside will be pulled in towards you and have its movement speed reduced by %d%% for 4 turns.
		Each tendril will leave a trail of fire in its path dealing %0.2f fire damage for 4 turns.
		The damage increases with spellpower.]], [[火焰触须从你的手中伸出，在锥形范围内伸展。
		被火焰触须抓住的生物将被拉过来，同时移动速度减少 %d%%，持续 4 回合。
		每个触须会留下火焰痕迹，每回合造成 %0.2f 火焰伤害，持续 4 回合。
		伤害受法术强度加成。]], "tformat")
t("Demon Blade", "恶魔之刃", "talent name")
t([[Imbue your weapon with fire for 5 turns. During this time all your melee hits will trigger a ball of fire of radius 1 dealing %0.2f fire damage.
		This effect can only happen once per turn.
		The damage increases with spellpower.]], [[向你的武器灌输火焰之力，持续 5 回合。
		每次近战攻击时会释放一个火球，在半径 1 的范围内造成 %0.2f 火焰伤害。
		这个效果每回合只能触发一次。
		伤害受法术强度加成。]], "tformat")
t("Link of Pain", "苦痛链接", "talent name")
t("Select the source:", "选择源生物：", "logPlayer")
t("Select the victim:", "选择受害者：", "logPlayer")
t([[Using demonic forces you create a link of pain from a source creature to a victim for %d turns.
		Each time the source creature takes damage the victim takes %d%% of the damage.
		If the victim dies from the effect you gain a burst of energy, reducing all remaining cooldowns by 1.]], [[使用恶魔之力，你在源生物与牺牲生物间构造痛苦链接，持续 %d 回合。
		每次源生物受到伤害时，%d%% 伤害由牺牲生物承受。
		当牺牲生物因此效果死亡时，你将获得能量，减少所有技能冷却时间 1 回合。]], "tformat")
t("Demon Horns", "恶魔之角", "talent name")
t("You require a weapon and a shield to use this talent.", "你需要一把武器一个盾牌来施展这个技能。", "logPlayer")
t("%s resists the shield bash!", "%s抵抗了盾牌猛击！", "logSeen")
t([[Demon horns temporarily grow on your shield as you bash a foe with it for %d%% damage.
		If the attack hits the creature is impaled by the horns, causing it to bleed black blood for 50%% of the damage done as darkness over 5 turns.
		Any time you damage this foe in melee while it bleeds you get healed for %d (this can only happen once per turn).
		The healing power increases with your spellpower.]], [[你的盾牌上长出临时的恶魔之角。
		你盾击敌人造成 %d%% 伤害。
		如果攻击命中，目标将被恶魔角刺穿，流血 5 回合，合计受到额外 50%% 黑暗伤害。
		每次你攻击被恶魔角刺穿的目标时，你回复 %d 生命（每回合至多 1 次）。
		治疗效果受法术强度加成。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/npcs.lua"

t("Soul Eater", "灵魂吞噬者", "talent name")
t("#CRIMSON#%s is bound to %s will.", "#CRIMSON#%s被绑定到%s的意志。", "logSeen")
t("#PURPLE#As %s falls down you see %s reach to it, devour its essence and raise it back as a demonic husk.", "#PURPLE#当%s倒下时，你看到%s靠向它，吞噬了它的精华，并将其复活为恶魔躯壳。", "logSeen")
t("%s (demonic husk)", "%s（恶魔尸傀）", "tformat")
t([[Any nearby allied creature that is not a summon will be bound to your will.
		Each time a creature bound to your will dies it is resurrected as a demonic husk.
		Demonic husks have:
		- slow movement speed
		- more life
		- new demonic talents]], [[任何附近的友方非召唤生物将与你的意志链接。
		每次与你意志链接的生物死亡时，将会以恶魔尸傀的形式复活。
		恶魔尸傀具有如下性质：
		- 缓慢的移动速度
		- 更多生命值
		- 新的恶魔技能]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/oppression.lua"

t("Horrifying Blows", "恐惧打击", "talent name")
t([[Your successful melee hits apply a stacking effect that decreases damage done by %d%%.
		You can have up to %d stacks per target and further attacks refresh the duration, but any turn you are farther than %d spaces from the victim the fear will wear off quickly.
		At level 3 it also slows by %0.2f%% per stack.
		At level 5 you can horrify enemies in a radius of %d.
		This talent ignores saves and immunities.
		]], [[你的攻击能够惊吓目标，降低目标 %d%% 的伤害。
	此效果可以叠加 %d 次，每次攻击会刷新持续时间。但是当目标与你距离超过 %d 码，恐惧效果会迅速消退。
	技能 3 级时，每次叠加会同时减少目标 %0.2f%% 的速度。
	技能 5 级时，可以影响到 %d 码内的所有敌对生物。
	此技能无视豁免和免疫。]], "tformat")
t("Mass Hysteria", "恐惧之潮", "talent name")
t("Amplifies the power of your fear on the target by %d%% per stack and sets its duration to %d.  The amplified fear spreads to all enemies in a radius of %d.", "增强目标的恐惧，目标身上每有一次恐惧叠加，效果增强 %d%%，持续时间增大到 %d 回合。增强后的恐惧效果影响 %d 码内所有敌对生物。", "tformat")
t("Fearfeast", "恐惧盛宴", "talent name")
t("You gain %.1f turns!", "你获得了%.1f个回合！", "logPlayer")
t("You consume the fear of enemies in radius %d, healing for %d life and gaining %0.1f%% of a turn for each stack up to a max of %.1f turns.", [[汲取 %d 码内敌对生物身上的恐惧，每汲取一层恐惧，恢复 %d 生命并获得 %0.1f%% 额外回合。
	至多能获得 %.1f 个额外回合。]], "tformat")
t("Hope Wanes", "绝望碾压", "talent name")
t([[You crush the spirit of a target with at least %d fear stacks, consuming all stacks and making it unable to act for %d turns.
		This talent ignores saves and immunities.]], [[击溃已叠加至少 %d 层恐惧目标的精神，清除所有恐惧效果，使目标 %d 回合无法行动。
	此技能无视豁免和免疫。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/torture.lua"

t("Incinerating Blows", "焚尽强击", "talent name")
t([[The power of the Fearscape infuses your weapon: Your melee attacks will deal %0.2f fire damage, spread over 3 turns.
		Additionally, every time you attack, there is a %d%% chance of releasing a burst of powerful fire that will deal %0.2f fire damage to all enemies in radius %d over %d turns.
		If this talent is not on cooldown, the burst of fire will instead be radius %d, and stun all targets in addition to burning them.
		For the purposes of applying the stun, you have %d bonus spellpower.
		The damage will increase with your Spellpower.]], [[恶魔空间的力量注入你的武器：你的近战攻击会在 3 回合内造成总计 %0.2f 点火焰燃烧伤害。
	另外，每次攻击时有 %d%% 几率释放强力火焰爆发，造成总计 %0.2f 点火焰燃烧伤害；半径 %d 内的所有敌人都会受到此伤害，持续 %d 回合。
	若该技能不在冷却中，火焰爆发将改为半径 %d，并使范围内所有敌对目标同时燃烧和震慑。
	进行震慑判定时，你获得 %d 点额外法术强度。
	伤害受法术强度加成。]], "tformat")
t("Abduction", "锁魂之链", "talent name")
t("You require a two handed weapon to use this talent.", "你需要装备一把双手武器来施展这个技能。", "logPlayer")
t("Hits the target doing %d%% weapon damage. If the attack hits, you pull the target in and strike them again, dealing another %d%% weapon damage.", [[对目标攻击，造成 %d%% 武器伤害。
	如果命中，将目标抓到身边并再次攻击，造成 %d%% 武器伤害。]], "tformat")
t("Fiery Torment", "灼魂之罚", "talent name")
t([[Hits the target with your weapon doing %d%% weapon damage. If the attack hits, the target is afflicted with Fiery Torment for %d turns, reducing their fire resistance by %d%%.
		When Fiery Torment ends the victim will take %d fire damage. This damage will increase by %d%% of all damage taken while under torment.
		The damage dealt by the effect will increase with spellpower.
		Demons under fiery torment will be burned by the flames of the Fearscape.]], [[用武器攻击敌人，造成 %d%% 武器伤害。如果命中，目标受到灼魂之罚的影响，持续 %d 回合，火焰抗性降低 %d%%。
	当灼魂之罚结束，敌人会受到 %d 点火焰伤害。
	在灼魂之罚持续时间内目标受到的所有伤害，有 %d%% 会加成到火焰伤害中。
	效果的伤害会随法术强度提升。
	被灼魂之罚影响的恶魔会被恶魔空间中的火焰焚烧。]], "tformat")
t("Eternal Suffering", "无尽苦痛", "talent name")
t([[Your strikes are imbued with a vile power that extends your victim's suffering. When hitting in melee, you have a (%d%%) chance to extend the length of all negative effects and reduce the length of all positive effects on the target by %d turn(s).
		This can only trigger on any particular target once every 6 turns.]], [[你的攻击充溢着恶毒的力量，能够延长敌人的苦痛。当近战命中时，有 %d%% 几率延长对方所有的负面状态持续时间并降低所有正面状态的持续时间，增减幅度为 %d 回合。
	该效果对同一目标每 6 回合才能生效一次。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/corruptions/wrath.lua"

t("Obliterating Smash", "歼灭挥斩", "talent name")
t("You require a two handed weapon to use this talent.", "你需要装备一把双手武器来施展这个技能。", "logPlayer")
t([[Swing your weapon with incredible force, striking all enemies in a radius %d semicircle, dealing %d%% weapon damage to all targets.
		Starting from talent level 5, all targets hit will have their armour and saves reduced by %d.
		This attack can not miss.]], [[用无与伦比的力量挥动武器，打击正面半圆 %d 码范围内所有敌对生物，对所有目标造成 %d%% 武器伤害。
	技能 5 级时，被击中敌对生物的护甲和豁免会降低 %d 点。
	此攻击必中。]], "tformat")
t("Detonating Charge", "爆裂冲锋", "talent name")
t("You require a two handed weapon and being able to move to use this talent.", "你需要装备一把双手武器且可以移动，才能施展这个技能。", "logPlayer")
t("You can not do that currently.", "目前你不能这样做。", "logPlayer")
t("You are too close to build up momentum!", "距离目标太近，无法蓄势！", "logPlayer")
t([[Launch yourself toward a target. If the target is reached you get a free attack doing %d%% weapon damage.
		If the attack hits you release a massive burst of fire in radius %d, knocking away all enemies except your target and dealing %d damage.
		You must charge from at least 2 tiles away.]], [[向目标冲锋，如果到达目标位置，则攻击目标造成 %d%% 武器伤害。
	若攻击命中，将释放强烈的火焰冲击，击退 %d 码之内目标之外的所有敌对生物，并造成 %d 伤害。
	至少要从 2 码外开始冲锋。]], "tformat")
t("Voracious Blade", "饕餮之刃", "talent name")
t([[Your blade drinks in death. Whenever you score a kill with this talent off cooldown, your next %d melee attacks within 6 turns will always critically strike, and you gain %d%% critical multiplier for the duration.
		Additionally, you gain an extra %d vim per kill.]], [[你的利刃充满着对杀戮的渴望。
	在技能冷却完毕后，当杀死敌人时，接下来 6 回合内的 %d 次近战攻击必定暴击，在持续时间内，暴击系数增加 %d%%。
	另外，每次击杀时额外获得 %d 点活力。]], "tformat")
t("Destroyer", "毁灭者", "talent name")
t([[Your body overflows with the power of the Fearscape, turning you into a powerful demon for %d turns. This increases your stamina regen and physical power by %d, and your disarm and stun immunity by %d%%.
		The physical power, stamina regen, and status resistances increase with your spellpower.
		Your other talents also gain a variety of bonuses:
		-Draining Assault: Reduces cooldown by %d.
		-Reckless Strike: Gain %d%% resistance penetration for all elements for %d turns.
		-Obliterating Smash: Increases range by %d.
		-Abduction: If it hits, get an additional %d attacks at 35%% weapon damage.
		-Incinerating Blows: Increases chance of bonus damage to %d%%.
		-Fearfeast: Gain %0.1f vim per stack.
		-Maw of Urh'rok: Increases cone width by %d degrees.]], [[恶魔空间的力量充溢了你的身体，将你转换成一个强大的恶魔，持续 %d 回合。
	变身期间，体力恢复和物理强度增加 %d，缴械和震慑抗性增加 %d%%。
	物理强度、体力恢复和状态抗性加值受法术强度加成。
	变身期间，其他技能也受到强化：
	汲魂痛击：冷却时间减少 %d。
	舍身一击：增加 %d%% 全体抗性穿透，持续 %d 回合。
	歼灭挥斩：增加半径 %d。
	锁魂之链：如果命中，额外附加 %d 次 35%% 武器伤害的攻击。
	焚尽强击：增加额外伤害几率至 %d%%。
	恐惧盛宴：每汲取一层叠加的恐惧，获得 %0.1f 点活力。
	乌鲁洛克之口：角度增加 %d。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/talents/misc/races.lua"

t("race", "种族技能", "talent category")
t("doomelf", "魔化精灵", "talent type")
t("The various racial bonuses a character can have.", "角色可能拥有的各种种族加成。", "_t")
t("Haste of the Doomed", "末日加速", "talent name")
t("You must have an empty space to teleport to.", "你必须寻找一片空地进行传送。", "logPlayer")
t([[Hasten yourself out of phase, teleporting you to a specific location up to %d spaces away.
		You can activate this talent up to twice within the same turn, but the second activation will not be instant.
		Afterwards you stay out of phase for 5 turns. In this state your defense is increased by %d and all your resistances by %d%%.
		The bonus will increase with your Willpower.]], [[加速自身，以至于脱离空间，传送半径 %d。
		你在同一回合内至多连用两次该技能，且第二次使用会消耗时间。
		之后，你停留在相位外 5 回合，闪避增加 %d，全体抗性增加 %d%%。
		效果受意志加成。]], "tformat")
t("Resilience of the Doomed", "强韧", "talent name")
t([[The tortures you had to endure on the Fearscape have increased your resilience.
		All detrimental status effects last %d%% less on you and all direct critical hits (physical, mental, spells) against you have a %d%% lower critical multiplier (but always do at least normal damage).]], [[你在恶魔空间忍受的折磨让你更加强韧。
		所有负面状态持续时间减少 %d%%，所有直接暴击（物理、精神、法术）的暴击倍率降低 %d%% （但至少仍会造成普通伤害）。]], "tformat")
t("Corruption of the Doomed", "腐化形态", "talent name")
t([[Your original invisibility talent was corrupted and twisted.
		You have %d%% chance to turn into a dúathedlen for 5 turns, when hit by a blow doing at least 10%% of your total life.
		While in this form you gain the following effects:
		- you have permanent stealth (power %d)
		- your darkness damage is increased by %d%%
		- any non mind and non physical damage you deal above %d triggers a darkness explosion of radius 1 for half the damage (this can only happen once per turn)
		- when you transform the cooldowns of Haste of the Doomed and Pitiless are reset
		]], [[你原本的隐身技能被腐化扭曲了。
		当你受到一次至少为你总生命值 10%% 的伤害时，有 %d%% 几率转变成多瑟顿形态 5 回合。
		在多瑟顿形态下：
		- 你获得永久潜行 (强度 %d)
		- 你的暗影伤害增加 %d%%
		- 每当你造成超过 %d 点的非物理非精神伤害时，在半径 1 的范围内产生一次暗影爆炸，造成额外 50%% 伤害（每回合至多 1 次）。
		- 变形时重置种族技能“末日加速”与种族技能“无情”
		]], "tformat")
t("Pitiless", "无情", "talent name")
t([[You launch a mental assault on the target.
		The assult increases the cooldown of any already cooling down talents by %d, the duration of any magical, physical or mental detrimental effects by %d (max 4x duration) and decreases the duration of any magical, physical or mental beneficial effects by %d.]], [[你对目标的精神进行冲击。
		他所有正在冷却中的技能冷却时间延长 %d 回合，所有负面魔法、物理、精神效果延长 %d 回合（最多延长至原持续时间的 4 倍），所有正面魔法、物理、精神效果缩短 %d 回合。]], "tformat")

------------------------------------------------

section "tome-ashes-urhrok/data/timed_effects.lua"

t("demonic", "恶魔", "effect subtype")
t("Demon Blade", "恶魔之刃", "_t")
t("Each melee hit generates a radius 1 ball of fire dealing %0.2f damage.", "近战攻击将附加半径 1 的火球，伤害 %0.2f。", "tformat")
t("#Target# imbues its weapon with demonic fire.", "#Target#用恶魔之火给武器附魔。", "_t")
t("+Demon Blade", "+恶魔之刃", "_t")
t("#Target#'s weapon looks less threatening.", "#Target#的危险度看起来降低了。", "_t")
t("-Demon Blade", "-恶魔之刃", "_t")
t("curse", "诅咒", "effect subtype")
t("Fiery Torment", "灼魂之罚", "_t")
t("The target's fire resistance is reduced by %d%%, and the target is highly vulnerable to the flames of the fearscape. When the effect ends, the target will take %d fire damage. This damage will increase by %d%% of all damage taken while under torment", "目标的火焰抗性下降 %d%%，并且极易受到恐惧空间火焰的伤害。效果结束时将受到 %d 火焰伤害，并追加效果期间受到的总伤害的 %d%%。", "tformat")
t("#Target# is surrounded by a vile flame!", "#Target#被邪恶的火焰包围", "_t")
t("+Fiery Torment", "+灼魂之罚", "_t")
t("The black flame around #Target# dies down", "#Target#周围的邪恶火焰熄灭了", "_t")
t("-Fiery Torment", "-灼魂之罚", "_t")
t("fire", "火焰", "effect subtype")
t("Destroyer", "毁灭者", "_t")
t("The target assumes the form of a powerful demon.", "目标变形为强大的恶魔。", "tformat")
t("#Target# turns into a demon!", "#Target# 变身成恶魔！", "_t")
t("+Destroyer", "+毁灭者", "_t")
t("#Target# is no longer transformed.", "#Target#恢复了原本的形态。", "_t")
t("-Destroyer", "-毁灭者", "_t")
t("corruption", "堕落", "effect subtype")
t("Voracious Blade", "饕餮之刃", "_t")
t("Next %d melee attacks are certain to critically strike, and this unit has %d%% more critical power.", "接下来的 %d 次近战攻击必定暴击。效果期间增加 %d%% 暴击系数。", "tformat")
t("#Target#'s weapon glows with critical power!", "#Target#的武器闪耀致命的光芒！", "_t")
t("+Voracious", "+饕餮", "_t")
t("#Target#'s weapon stops glowing.", "#Target#的武器停止闪光。", "_t")
t("-Voracious", "-饕餮", "_t")
t("Raging flames", "熊熊烈焰", "_t")
t("Next melee attack will always trigger incinerating blows, and the damage from incinerating blows will be multiplied by %d%%", "接下来一次近战攻击必定触发焚尽强击，且焚尽强击伤害按 %d%% 乘算", "tformat")
t("#Target#'s weapon surges with fire!", "#Target#的武器闪耀着火花！", "_t")
t("+Revel", "+烈焰", "_t")
t("#Target#'s is no longer blazing.", "#Target#不再闪耀。", "_t")
t("-Revel", "-烈焰", "_t")
t("Devouring flames", "吞噬之焰", "_t")
t("This character's flames are feeding the source, healing them for %d per turn and giving them %d vim.", "该生物身上的火焰正向来源生物提供能量，每回合给予其 %d 生命与 %d 活力。", "tformat")
t("#Target#'s is surrounded with an all-consuming flame!", "#Target#被吞噬性的火焰环绕！", "_t")
t("+Devoured", "+吞噬", "_t")
t("-Devoured", "-吞噬", "_t")
t("Overwhelming Fear", "无尽恐惧", "_t")
t("The target is losing faith that it can defeat you, reducing its damage by %d%% and slowing it by %d%%", "目标对打败你失去信心，伤害减少 %d%%，速度减慢 %d%%", "tformat")
t("#Target# begins to fear you.", "#Target#开始畏惧你。", "_t")
t("#Target#'s shakes the fear off.", "#Target#摆脱了恐惧。", "_t")
t("Abandoned hope", "绝望", "_t")
t("The target's spirit is broken, rendering it inactive.", "目标精神破碎，不能行动。", "_t")
t("#Target#'s spirit is broken.", "#Target#的精神破碎了。", "_t")
t("+Unable to act", "+无法行动", "_t")
t("#Target# regains the will to fight.", "#Target#恢复了战斗的勇气。", "_t")
t("-Unable to act", "-无法行动", "_t")
t("Suffered", "被折磨", "_t")
t("The target has recently suffered, and cannot do so again yet.", "目标最近被折磨过，暂时不能继续折磨。", "_t")
t("#Target# suffers!", "#Target# 被折磨！", "_t")
t("+Eternal Suffering", "+永恒折磨", "_t")
t("Cleansing flames", "净化之焰", "_t")
t("The target is purified by fire, losing %0.2f%% of their max health per turn.", "目标被火焰净化，每回合损失 %0.2f%% 最大生命值的生命。", "tformat")
t("#Target# is purified by fire.", "#Target#被火焰净化。", "_t")
t("+Fire", "+火焰", "_t")
t("#Target#'s purification is complete.", "#Target#的火焰净化结束了。", "_t")
t("-Fire", "-火焰", "_t")
t("Damage from soulburn.", "来自灵魂燃烧的伤害。", "_t")
t("Blazing Rebirth", "烈焰重生", "_t")
t("The target is burning, taking %d damage per turn, split among it and burning foes in radius %d.", "目标正在燃烧，每回合损失 %d 生命值，和半径 %d 内的正在燃烧的敌人分摊。", "tformat")
t("%s loses %d health to the soulburn.", "%s 因为灵魂燃烧流失 %d 生命值。", "logSeen")
t("pin", "定身", "effect subtype")
t("Fiery Grasp", "炙炎之牢", "_t")
t("The target is pinned and on fire, taking %0.2f fire damage per turn. They are also silenced.", "目标被定身并着火，每回合受到 %0.2f 点火焰伤害，并被沉默。", "tformat")
t("The target is pinned and on fire, taking %0.2f fire damage per turn.", "目标被定身并着火，每回合受到 %0.2f 点火焰伤害。", "tformat")
t("#Target# is grabbed!", "#Target#被抓住了！", "_t")
t("+Fiery Grasp", "+炙炎之牢", "_t")
t("#Target# is released.", "#Target#解脱了。", "_t")
t("-Fiery Grasp", "-炙炎之牢", "_t")
t("arcane", "奥术", "effect subtype")
t("shield", "护盾", "effect subtype")
t("Fiery Aegis", "火焰守护", "_t")
t("The target is surrounded by a magical shield, absorbing %d/%d damage before it crumbles and dealing %d damage in a radius of %d when it does.", "目标被一层魔法护盾包围，吸收 %d/%d 伤害，护盾结束时（无论吸收耗尽还是自然到期），对周围敌方生物施加持续 3 回合的灼烧，总计造成 %d 伤害，作用半径为 %d。", "tformat")
t("A shield forms around #target#.", "#target#的周围产生了一道护盾。", "_t")
t("+Shield", "+护盾", "_t")
t("The shield around #target# crumbles.", "#target#周围的护盾消失了。", "_t")
t("-Shield", "-护盾", "_t")
t("#SLATE#(%d absorbed)#LAST#", "#SLATE#(%d 护盾吸收)#LAST#", "tformat")
t("Your shield crumbles under the damage!", "你的护盾在攻击下被打破！", "logPlayer")
t("Surge of Power", "力量之潮", "_t")
t("This unit will not die until it has less than -%d HP.", "目标直到 -%d 生命才会死去。", "tformat")
t("#Target# surges with an incredible power!", "#Target#身上涌动着力量！", "_t")
t("+Surge of Power", "+力量之潮", "_t")
t("#Target#'s surge ends.", "#Target#的力量之潮结束了。", "_t")
t("-Surge of Power", "-力量之潮", "_t")
t("Recklessness", "舍身", "_t")
t("This unit has %d%% resistance penetration.", "目标获得 %d%% 全体抗性穿透。", "tformat")
t("+Reckless", "+舍身", "_t")
t("-Reckless", "-舍身", "_t")
t("Demon Seed", "恶魔之种", "_t")
t("Infected by a demon seed. When it dies the caster has a %d%% chance to get back the matured seed.", "目标被恶魔之种感染，死亡时施法者有 %d%% 几率获得成熟的种子。", "tformat")
t("#Target# is infected by a demon seed!", "#Target#被恶魔种子感染！", "_t")
t("+Demon Seed", "+恶魔之种", "_t")
t("#Target# is free from the demon seed.", "#Target#移除了恶魔种子。", "_t")
t("-Demon Seed", "-恶魔之种", "_t")
t("heal", "治疗", "effect subtype")
t("Osmosis Regeneration", "渗透吸收", "_t")
t("You regenerate a total of %0.2f life over the duration of the effect.", "效果期间，你总计回复 %0.2f 生命。", "tformat")
t("+Osmosis Regen", "+渗透吸收", "_t")
t("-Osmosis Regen", "-渗透吸收", "_t")
t("resistance", "抵抗", "effect subtype")
t("Acidic Bath", "酸浴", "_t")
t("Gain %d%% resistance and %d%% affinity to acid.", "获得%d%% 酸性抗性与 %d%%酸性伤害亲和。", "tformat")
t("+Acidic Bath", "+酸浴", "_t")
t("-Acidic Bath", "-酸浴", "_t")
t("Plaguefire", "瘟疫之焰", "_t")
t("The target is on fire, taking %0.2f fire damage per turn. On death, the flame will explode.", "目标着火，每回合受到 %0.2f 火焰伤害。死亡时火焰会以更弱的强度传播到附近目标身上。", "tformat")
t("#Target# is on fire!", "#Target#着火了！", "_t")
t("+Burn", "+燃烧", "_t")
t("#Target# stops burning.", "#Target#身上的火熄灭了。", "_t")
t("-Burn", "-燃烧", "_t")
t("dark", "黑暗", "effect subtype")
t("Corrupted Light", "腐化之光", "_t")
t("The target is overflowing with power, increasing all damage done by %d%%.", "目标能量溢出，增加 %d%% 全体伤害。", "tformat")
t("#Target# is filled with dark power!", "#Target#充满了黑暗力量！", "_t")
t("+Corrupted Light", "+腐化之光", "_t")
t("#Target# is no longer subject to the dark power.", "#Target#的黑暗力量消退了。", "_t")
t("-Corrupted Light", "-腐化之光", "_t")
t("armour", "护甲", "effect subtype")
t("Armoured Leviathan", "重装上阵", "_t")
t("Increases your Strength and Magic stats by %d.", "增加 %d 力量与魔法。", "tformat")
t("#Target# is filled with raw power!", "#Target#充满了原始力量！", "_t")
t("+Armoured Leviathan", "+重装上阵", "_t")
t("#Target# is no longer filled with power.", "#Target#失去了力量。", "_t")
t("-Armoured Leviathan", "-重装上阵", "_t")
t("blight", "枯萎", "effect subtype")
t("Doomed Nature", "自然末日", "_t")
t("The target is affected by blight, all natural and psionic talent it tries to use has %d%% chance to fail and instead explode into %0.2f fire damage in radius 1.", "目标被枯萎力量感染，使用自然或灵能技能时有 %d%% 几率失败并释放半径 1 的火球，伤害 %0.2f。", "tformat")
t("#Target# is cut off from nature!", "#Target#与自然的联系被切断了！", "_t")
t("+Doomed Nature", "+自然末日", "_t")
t("#Target# is no longer cut off from nature.", "#Target#与自然的联系恢复了。", "_t")
t("-Doomed Nature", "-自然末日", "_t")
t("wound", "创伤", "effect subtype")
t("cut", "流血", "effect subtype")
t("bleed", "流血", "effect subtype")
t("darkness", "暗影", "effect subtype")
t("Demonic Cut", "恶魔伤口", "_t")
t("Huge demonic that bleeds, doing %0.2f darkness damage per turn. Anytime you hit it you get healed for %d.", "巨大的恶魔伤口每回合造成 %0.2f 暗影伤害。当造成该伤口的来源以近战攻击命中目标时，将会恢复 %d 生命。", "tformat")
t("#Target# starts to bleed darkness.", "#Target#流出黑暗的血液。", "_t")
t("+Demonic Cut", "+恶魔伤口", "_t")
t("#Target# stops bleeding darkness.", "#Target#的黑暗伤口愈合了。", "_t")
t("-Demonic Cut", "-恶魔伤口", "_t")
t("ritual", "仪式", "effect subtype")
t("Link of Pain", "苦痛链接", "_t")
t("When this target is damaged %d%% of the damage will also be done to an other victim.", "当目标受伤害时，牺牲生物也会承受 %d%% 的伤害。", "tformat")
t("#Target# is linked through pain.", "#Target#建立了苦痛链接。", "_t")
t("+Link of Pain", "+苦痛链接", "_t")
t("#Target# link of pain disappears.", "#Target#的苦痛链接解除了。", "_t")
t("-Link of Pain", "-苦痛链接", "_t")
t("#ORANGE##Source# shares some pain with #target#!#LAST#", "#ORANGE##Source#与#target#共享痛苦！#LAST#", "delayedLogMessage")
t("#CRIMSON#(%d linked)#LAST#", "#CRIMSON#(%d 伤害链接)#LAST#", "tformat")
t("Only Ashes Left", "唯余灰烬", "_t")
t("The target burns with darkness, taking %0.2f damage each turn until it dies or runs away.", "目标被黑暗灼烧，每回合受到 %0.2f 伤害直到死亡或离开。", "tformat")
t("#Target# burns with dark flames.", "#Target#被黑暗火焰灼烧。", "_t")
t("+Only Ashes Left", "+唯余灰烬", "_t")
t("-Only Ashes Left", "-唯余灰烬", "_t")
t("spellblaze", "魔法大爆炸", "effect subtype")
t("Shattered Mind", "精神破碎", "_t")
t("The target has %d%% chances to fail any talents use and suffers %d reduced physical, mental and spell saves.", "目标使用技能时有 %d%% 几率失败。目标全体豁免下降 %d 点。", "tformat")
t("The Spellblaze ripples through #target#!", "魔法大爆炸的力量侵袭了#target#！", "_t")
t("+Shattered Mind", "+精神破碎", "_t")
t("#Target# is no longer influenced by the Spellblaze.", "#Target#不再受魔法大爆炸影响。", "_t")
t("-Shattered Mind", "-精神破碎", "_t")
t("Dark Reign", "黑暗支配", "_t")
t([[All damage affinity increased by %d%%.
Will not die until %d life]], [[全体伤害亲和增加 %d%%。
生命值不低于 %d 时不会死亡。]], "tformat")
t("+Dark Reign", "+黑暗支配", "_t")
t("-Dark Reign", "-黑暗支配", "_t")
t("Blood Pact", "鲜血契约", "_t")
t("All damage you deal is converted to darkness.", "你的所有伤害转化为暗影伤害。", "tformat")
t("#Target# becomes an avatar of darkness!", "#Target#成为了黑暗化身！", "_t")
t("+Blood Pact", "+鲜血契约", "_t")
t("The darkness within #target# subsides.", "#target#体内的黑暗消退了。", "_t")
t("-Blood Pact", "-鲜血契约", "_t")
t("cold", "寒冷", "effect subtype")
t("Blackice", "黑冰", "_t")
t("You have %d charges.", "叠加次数：%d。", "tformat")
t("Fire and physical resistance reduced by %d%%.", "火焰和物理抗性下降%d%%。", "tformat")
t("Fire Haven", "火焰庇护", "_t")
t("The target is surrounded by a fire haven, granting 40% fire damage affinity but -15% to blight resistance.", "目标被火焰庇护围绕，获得 40% 火焰伤害亲和，但减少 15% 枯萎抗性。", "_t")
t("vim", "活力", "effect subtype")
t("Bleak Outcome", "悲惨结局", "_t")
t("Victim is tormented with impending death.  When it dies, it will restore to the source (%s) up to %d times the normal amount of Vim.", "受害者因即将到来的死亡而备受折磨。当其死亡时，将为来源（%s）恢复至多 %d 倍于正常数值的活力值。", "tformat")
t("none", "没有", "_t")
t("Grim Future", "无情未来", "_t")
t("Spellpower increased by %d.", "法术强度增加 %d。", "tformat")
t("death", "死亡", "effect subtype")
t("Blood Drinker", "饮血者", "_t")
t("Triggers Blood Drinker if this creature dies.", "这个生物死后会触发饮血者效果。", "_t")
t("%d vim regen and %d%% evasion chance.", "获得 %d 活力值恢复，%d%% 闪避率。", "tformat")
t("#Target# is drunk with blood!", "#Target#饮血狂欢！", "_t")
t("The bloodlust of #target# subsides.", "#target#的嗜血狂热消退了。", "_t")
t("affinity", "伤害亲和", "effect subtype")
t("Pain Affinity", "痛苦协调", "_t")
t("All damage affinity increased by %d%%.", "全体伤害亲和提升%d%%。", "tformat")
t("Ominous Shadow", "不祥黑影", "_t")
t("Improves/gives invisibility (power %d), converts all damage to darkness and uses your highest damage penetration and increase for darkness.", "强化或获得隐形（强度 %d）；所有伤害转化为暗影伤害，暗影伤害使用你最高的伤害加成和抗性穿透。", "tformat")
t("#Target# vanishes from sight.", "#Target#从视线中消失。", "_t")
t("+Ominous Shadow", "+不祥黑影", "_t")
t("#Target# is no longer invisible.", "#Target#不再隐形。", "_t")
t("-Ominous Shadow", "-不祥黑影", "_t")
t("Corruption of the Doomed", "腐化形态", "_t")
t("The target assumes the form of a dúathedlen.", "目标变形为多瑟顿。", "tformat")
t("#Target# turns into a dúathedlen!", "#Target#变形为多瑟顿！", "_t")
t("+Corruption of the Doomed", "+腐化形态", "_t")
t("-Corruption of the Doomed", "-腐化形态", "_t")
t("#CRIMSON#Your corruption explodes around %s!", "#CRIMSON#你的腐化在%s周围爆炸！", "logPlayer")
t("demon", "恶魔", "effect subtype")
t("seismic", "地震", "effect subtype")
t("Volcanic Skin", "火山皮肤", "_t")
t("%d charges.", "%d层充能。", "tformat")

------------------------------------------------
