section "tome-orcs/data/talents/steam/gunslinging.lua"

t("Strafe", "扫射", "talent name")
t("@Source@ strafes with @hisher@ steamguns!", "@Source@使用@hisher@蒸汽枪扫射！", "_t")
t("You must dual wield steamguns for this talent.", "你需要双持蒸汽枪才能使用这一技能。", "logPlayer")
t([[You have learned to fire while moving.
		In one motion, you fire your double steamguns (100%% weapon damage, 1 tile range penalty) and may then move to an adjacent tile (unless pinned to the ground or immobilized).
		This talent can be activated for up to %d consecutive turns before it goes on cooldown, and takes time according to your steamtech speed or movement speed (if you move), whichever is slower.
		When Strafe ends you may instantly reload between %d and %d ammo (based on the number of strafes you performed and your ammo capacity).]], [[你学会如何在移动中射击。
		在射击（100%% 武器伤害，射程 -1）的同时你能移动到相邻的一格。
		该技能在冷却前能激活连续 %d 个回合，消耗时间取决于蒸汽速度和移动速度较慢者。
		扫射结束后，你立刻获得 %d 到 %d 弹药（取决于扫射期间你消耗的弹药与你的弹药容量）。]], "tformat")
t("Startling Shot", "惊艳射击", "talent name")
t("Something", "某物", "_t")
t("%s misses %s shot.", "%s故意射偏了，%s那一枪没有命中目标。", "logSeen")
t([[You deliberately fire a missing shot at a target, startling it for 3 turns.
		If the target fails a mental save it instinctively recoils two steps back.
		The next shot that hits the startled creature will deal %d%% more damage.]], [[你故意朝目标射出偏离的子弹，令其惊讶 3 回合。
		若目标未通过精神豁免检定，将后退 2 步。
		下一发命中惊讶状态目标的射击将造成额外 %d%% 伤害。]], "tformat")
t("#Source# fires a retaliatory shot at #Target#!", "#Source#朝#Target#发射反击射击！", "logCombat")
t("Evasive Shots", "闪避射击", "talent name")
t([[Using small engines to augment your reflexes you are able to automatically fire retaliatory shots at your foes doing %d%% weapon damage.
		Retaliation shots are fired when you evade/are missed by a melee or ranged attack.
		This can only happen once per turn and uses shots as normal.]], [[开启引擎强化反射神经，你能进行反击射击，造成 %d%% 武器伤害。
		反击射击是当你闪避或躲闪近战、远程攻击时触发的自动射击。
		反击射击一回合只能触发一次，且照常消耗弹药。]], "tformat")
t("Trick Shot", "魔术射击", "talent name")
t([[Your cunning and dexterity allow you to fire incredible trick shots that can hit multiple targets.
		You precisely aim your trick shot to ricochet amongst foes you can see so that whenever it hits something solid (creature or solid wall), it will bounce towards the next closest foe.
		It may ricochet up to %d times (or until it misses) within range 5 of your first target and will not target the same foe twice.
		Your shot deals %d%% weapon damage on its first strike, but loses %d%% damage and %d(%d%%) accuracy with each bounce.]], [[你的灵敏让你能射出同时击中多个敌人的子弹。
		你精确地瞄准敌人，子弹命中后将弹射至其他目标上。
		子弹最多弹射 %d 次，只能在第一个目标周围 5 码范围内弹射，不会命中同一个目标两次。
		第一次命中将造成 %d%% 武器伤害，之后每次弹射下降 %d%% 伤害和 %d （%d%%）命中。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/heavy-weapons.lua"

t("Heavy Weapons", "重装武器", "talent name")
t([[You gain the ability to equip one of 3 heavy weapons listed below, temporarily granting you a special attack. Heavy weapons are significantly more powerful than a steamgun, but require heavy ammunition to fire. You can store up to %d ammunition at a time, and regenerate 1 every 3 turns while a heavy weapon is not equipped.
		
		#AQUAMARINE#Flamethrower#LAST#: An incendiary device which projects streams of liquid flame at your foes. Deals %d%% steamgun fire damage over 3 turns to those in radius 5. The flamethrower ignores armor, always hits, and counts as a steamgun shot for the purpose of on-hits.
		#AQUAMARINE#Shockstaff#LAST#: An electrically charged baton wielded in close combat. Deals %d%% lightning damage to enemies in a frontal arc, as well as reducing the damage they deal by %d%% for 3 turns. This counts as a melee attack but triggers ammunition on-hit effects. All shockstaff attacks will also make a shield attack for the same damage as lightning. You can charge up to your steamgun's range to make shockstaff attacks.
		#AQUAMARINE#Boltgun#LAST#: A multi-barreled steamgun that launches efficient, chemical infused bolts. Fires twice for %d%% steamgun acid damage and generates %d steam per hit.
		
		The damage dealt by your Heavy Weapons is based off your currently equipped ammunition, and are treated as Steamguns for the purposes of weapon mastery talents and other effects.
		Firing your Steamgun will immediately unequip your heavy weapon.		
		]], [[你可以装备下列 3 种重装武器之一，临时获得一种特殊攻击。重装武器远比蒸汽枪强大，但需要重装弹药才能开火。你最多可以储存 %d 发弹药；未装备重装武器时，每 3 回合恢复 1 发。

		#AQUAMARINE#火焰喷射器#LAST#：向敌人喷射液态火焰的燃烧装置。对半径 5 格内的目标在 3 回合内造成相当于 %d%% 蒸汽枪武器伤害的火焰伤害。火焰喷射器无视护甲、必定命中，并按蒸汽枪射击计算命中触发效果。
		#AQUAMARINE#电击棒#LAST#：近战使用的带电棍棒。对正面弧形范围内的敌人造成 %d%% 武器伤害的闪电伤害，并使其造成的伤害降低 %d%%，持续 3 回合。此攻击视为近战攻击，但会触发弹药的命中效果。所有电击棒攻击还会发动一次盾牌攻击，造成等量的闪电伤害。你可以从不超过蒸汽枪射程的距离发起冲锋，然后用电击棒攻击。
		#AQUAMARINE#爆矢枪#LAST#：发射高效化学灌注弹矢的多管蒸汽枪。连续射击两次，每次造成相当于 %d%% 蒸汽枪武器伤害的酸性伤害；每次命中产生 %d 点蒸汽。

		重装武器造成的伤害以当前装备的弹药为基础；在武器掌握技能和其他效果的判定中，它们均视为蒸汽枪。
		使用蒸汽枪射击会立即卸下重装武器。]], "tformat")
t("Flamethrower", "火焰喷射器", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t("You require heavy ammunition to use this talent.", "你需要重装武器弹药才能使用这一技能。", "logPlayer")
t([[You replace your steamgun and attack with an incendiary device that projects streams of liquid flame at your foes.
		
		Deals %d%% steamgun damage as fire over 3 turns to enemies in radius 5.

		These attacks cannot miss and ignore armor.]], [[你将你的蒸汽枪替换成一把强大的蒸汽动力的喷火器，将你的敌人化为灰烬。

		在 5 码范围内，在 3 回合内造成 %d%% 火焰蒸汽枪伤害。

		这一攻击必定命中目标，无视护甲。]], "tformat")
t("Flame Jet", "火焰喷射", "talent name")
t("You are disarmed.", "你被缴械了。", "logPlayer")
t("You require heavy ammunition to fire your flamethrower.", "你需要重装武器弹药才能使用火焰喷射器。", "logPlayer")
t("Fire a jet of flame, dealing %d%% weapon damage as fire over 3 turns.", "发射一团火焰，在 3 回合内造成相当于 %d%% 武器伤害的火焰伤害。", "tformat")
t("Shockstaff", "电击棒", "talent name")
t("You require heavy ammunition to power your shockstaff.", "你需要重装武器弹药才能使用电击棒。", "logPlayer")
t([[You replace your steamgun and attack with a lightning-charged staff to engage in close combat.
		
		Deals %d%% steamgun damage as lightning to enemies in a frontal arc, as well as reducing the damage they deal by %d%% for 3 turns. This counts as a melee attack but triggers ammunition on-hit effects. All shockstaff attacks will also make a shield slam for the same damage as lightning. 

		You can charge up to your steamgun's range to make shockstaff attacks.]], [[你将你的蒸汽枪替换成一根通了强电的电棍，用于进行近战格斗。

		在前方造成 %d%% 闪电蒸汽枪伤害，并降低他们所造成的伤害 %d%%，持续 3 回合。这一效果视作近战攻击，但可以触发弹药的命中效果。所有电击棒伤害也会附加一次盾牌攻击，造成同样的闪电伤害。

		你可以冲刺进行电击棒攻击，冲刺范围等于蒸汽枪射程。]], "tformat")
t("Stormstrike", "暴风打击", "talent name")
t([[Sweep your shockstaff, striking all enemies in a frontal arc for %d%% weapon damage as lightning and reducing their damage dealt by %d%% for 3 turns.
		If you have a shield, you will also strike them.
		While active this replaces your normal melee attack.]], [[挥舞电击棒，攻击正面所有敌人，造成 %d%% 闪电武器伤害，降低他们所造成的伤害 %d%%，持续 3 回合。
		如果你装备了盾牌，你还会附加一次盾击。
		该效果持续期间会取代你的普通近战攻击。]], "tformat")
t("Boltgun", "爆矢枪", "talent name")
t("You require heavy ammunition to fire your boltgun.", "你需要重装武器弹药才能使用爆矢枪。", "logPlayer")
t([[You replace your steamgun and attack with a multi-barreled bolt launcher, firing deadly chemical-infused flechettes.
		
		Each attack fires twice for %d%% weapon damage as acid and generates %d steam per hit.]], [[你把你的蒸汽枪替换成一把多管重型枪械，发射注入了致命的化学物质的子弹。

		每次攻击造成两次 %d%% 酸性武器伤害，击中恢复 %d 蒸汽。]], "tformat")
t("Flechette Burst", "毒弹爆射", "talent name")
t("%s resists the disarm!", "%s抵抗了缴械！", "logSeen")
t("Fire two chemical flechettes, dealing %d%% weapon damage as acid and generating %d steam per hit.", "发射两枚化学毒弹，造成 %d%% 酸性武器伤害，每次击中恢复 %d 蒸汽。", "tformat")
t("Heavy Weapon Expertise", "重装武器精通", "talent name")
t("You require heavy ammunition and a heavy weapon to use this talent.", "你需要重装武器弹药和重装武器才能使用这一技能。", "logPlayer")
t("%s resists the stunning blow!", "%s抵抗了震慑打击！", "logSeen")
t("%s resists the stunning shock!", "%s抵抗了震慑打击！", "logSeen")
t([[Your advanced training unlocks specialised techniques, triggering an effect based on your current heavy weapon at the cost of 1 heavy weapon ammunition.
#AQUAMARINE#Flamethrower#LAST#: Sweep your flamethrower across the ground, dealing %d%% steamgun damage as fire and raising a length 7 wall of fire for 5 turns. Those inside the wall take %0.2f fire damage and have their fire resistance reduced by %d%% for 2 turns.
#AQUAMARINE#Shockstaff#LAST#: Slam your staff into the target, creating a radius 3 shockwave that deals %d%% shockstaff damage as lightning and stuns those within for %d turns.
#AQUAMARINE#Boltgun#LAST#: Fire %d boltgun shots dealing %d%% steamgun damage as acid and disarming the target for 5 turns.
The damage dealt by the fire wall and the chance to apply effects will increase with your Steampower.]], [[你通过特殊训练解锁了新的重装武器战技。你现在可以消耗 1 重装武器弹药，根据你现在装备的重装武器类型，触发以下的效果。
#AQUAMARINE#喷火器#LAST#: 用喷火器扫射地面，造成 %d%% 火焰蒸汽枪伤害，并产生一道长度为 7 的火墙，持续 5 回合。在火墙内的敌人会受到 %0.2f 的火焰伤害，且它们的火焰伤害抗性会降低 %d%%，持续 2 回合。
#AQUAMARINE#电击棒#LAST#: 用电棒猛击目标，在 3 码范围内产生冲击波，造成 %d%% 闪电电击棒伤害，并震慑敌人 %d 回合。
#AQUAMARINE#爆矢枪#LAST#: 发射 %d 枚爆矢枪子弹，造成 %d%% 酸性蒸汽枪伤害，并缴械目标 5 回合。
火墙造成的伤害，以及造成异常状态的几率，受蒸汽强度加成。]], "tformat")
t("Automated Defenses", "自动防御系统", "talent name")
t([[You augment your shield with your heavy weapon technology, causing an effect when you Block with a heavy weapon equipped.
#AQUAMARINE#Flamethrower#LAST#: Vent choking, burning smoke in an area of the same radius as your flamethrower. Enemies caught within take %d%% shield damage as fire and are silenced for %d turns.
#AQUAMARINE#Shockstaff#LAST#: Sheathe your shield in lightning and attack all enemies in radius 3, dealing %d%% shield damage as lightning and gaining a barrier absorbing an amount of damage equal to 100%% of the highest damage dealt for 6 turns.
#AQUAMARINE#Boltgun#LAST#: Fire a blast of flechettes from your shield at all enemies in radius 7, dealing %d%% shield damage as acid. %d flechettes remain embedded in each target for 6 turns, and when struck by a melee or ranged attack a flechette will detonate and cause acid damage equal to 50%% of the shield damage dealt.
These attacks will not trigger Counterstrike.
The chance to silence will increase with your Steampower.]], [[你使用重装武器技术强化你的盾牌，在你装备重装武器的时候进行格挡，会触发以下的特殊效果。
#AQUAMARINE#喷火器#LAST#: 在火焰喷射器攻击半径范围内，释放出燃烧的呛人浓烟。被击中的敌人会受到 %d%% 火焰盾牌伤害，并被沉默 %d 回合。
#AQUAMARINE#电击棒#LAST#: 将盾牌注入闪电，攻击半径 3 码范围内的所有敌人，造成 %d%% 闪电盾牌伤害，并获得相当于最高伤害值 100%% 的伤害吸收护盾，持续 6 回合。
#AQUAMARINE#爆矢枪#LAST#: 从盾牌中发射出一团镖弹，攻击 7 码半径范围内的所有敌人，造成 %d%% 酸性盾牌伤害。目标身上会插满 %d 枚毒镖，持续 6 回合。被插毒镖的敌人受到近战或远程攻击的时候，毒镖会爆炸，造成相当于盾牌造成的伤害 50%% 的酸性伤害。
这些攻击不会触发反击效果。
沉默几率受蒸汽强度加成。]], "tformat")
t("Safety Override", "武器过载", "talent name")
t("%s resists the stun!", "%s抵抗了震慑！", "logSeen")
t("%s slams into something solid, emitting a pulse of stunning lightning!", "%s击中了某物，放出一股震慑闪电冲击！", "logSeen")
t([[Push your heavy weapon beyond its normal limits to trigger a powerful effect. This will immediately disable your heavy weapon and expends all remaining ammunition.
#AQUAMARINE#Flamethrower#LAST#: Detonate your fuel tanks, creating a radius 4 explosion that launches you to a chosen tile in range %d. Enemies caught within the explosion take %0.2f fire damage, and further fire damage equal to %d%% of their current burning damage from the volatile fuel.
#AQUAMARINE#Shockstaff#LAST#: Drive your staff into the ground, discharging all remaining power to deal %d%% shockstaff damage as lightning in radius %d. Those struck will be knocked back %d tiles, and if they strike a wall they will emit a static pulse dealing %0.2f lightning damage in radius 1 and stunning them for 5 turns.
#AQUAMARINE#Boltgun#LAST#: Overcharge your boltgun, firing a single deadly bolt dealing %d%% steamgun damage as acid in a piercing line. For each negative physical, magical, or mental effect on the target, they take an additional %d%% damage (to a maximum of %d%%) and the duration of each negative effect is increased by %d turns.]], [[让你的重装武器突破正常极限，触发一个强大的效果。这会立即停用重装武器，并消耗所有剩余弹药。
#AQUAMARINE#火焰喷射器#LAST#: 引爆燃料箱，制造半径 4 的爆炸，将你抛至距离 %d 内的指定格。爆炸范围内的敌人受到 %0.2f 点火焰伤害；不稳定燃料还会使其额外受到相当于当前燃烧伤害 %d%% 的火焰伤害。
#AQUAMARINE#电击棒#LAST#: 将电击棒砸入地面，释放所有剩余能量，造成相当于 %d%% 电击棒伤害的闪电伤害，半径为 %d。受击目标会被击退 %d 格；若撞上墙壁，便会释放一道半径 1 的静电脉冲，造成 %0.2f 点闪电伤害，并震慑其 5 回合。
#AQUAMARINE#爆矢枪#LAST#: 超载爆矢枪，射出一枚致命弹矢，对直线上的目标造成相当于 %d%% 蒸汽枪伤害的酸性伤害。目标每有一种物理、魔法或精神负面效果，便额外受到 %d%% 伤害（最多 %d%%），且每种负面效果的持续时间增加 %d 回合。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/inscriptions.lua"

t("\
Its effects scale with your %s stat.", "\
效果随你的%s属性提升。", "tformat")
t("Implant: Steam Generator", "植入物：蒸汽制造机", "talent name")
t([[Steam generator that permanently creates %0.1f steam per turn.
		Can be activated for an instant burst of %d steam.]], [[蒸汽制造机每回合制造 %0.1f 点蒸汽。
		能直接使用，立即制造 %d 蒸汽。]], "tformat")
t("steam %d", "蒸汽 %d", "tformat")
t("Implant: Medical Injector", "植入物：医疗注射器", "talent name")
t("#LIGHT_BLUE#Medical injector selected to be used first by salves.", "#LIGHT_BLUE#已将医疗注射器设为药剂的首选注射器。", "saySimple")
t("This medical injector will now be used first if available when using medical salves.", "使用医疗药剂时，如果可用，将优先使用此医疗注射器。", "logPlayer")
t("Medical injector allows using therapeutics with %d%% efficiency and cooldown mod of %d%%.", "医疗注射器能以 %d%% 的效率使用药剂，冷却修正为 %d%%。", "tformat")
t("efficiency %d%% / cooldown %d%%", "效率 %d%% / 冷却时间 %d%%", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/magnetism.lua"

t("Static Shock", "静电震击", "talent name")
t([[Using your Block talent surrounds you and your minions in a static barrier for 4 turns, increasing all resistances by %d%%. If an enemy deals damage to you or your minions, the barrier will shock them for %d%% of your shield damage.
		This effect cannot damage the same target more than once per turn, and will not interact with Counterstrike.
You now also use your Cunning in place of Strength when equipping shields as well as when calculating shield damage.]], [[当你使用格挡技能的时候，你会在自己和召唤物身边产生一个静电屏障，增加所有抗性 %d%%，持续 4 回合。如果有敌人此时攻击你或召唤物，屏障会电击它们，造成 %d%% 你的盾牌伤害。
		这一效果每回合最多只能对一个目标伤害一次，并且不会消耗反击效果。
你装备盾牌和计算盾牌攻击伤害的时候，用灵巧代替力量要求。]], "tformat")
t("Magnetic Field", "磁性力场", "talent name")
t("You require a shield for this talent.", "你需要一面盾牌才能使用这一技能。", "logPlayer")
t("#Source# shatters '#Target#'.", "#Source#击碎了'#Target#'。", "logCombat")
t([[You project a powerful blast of magnetic energy from your shield in radius %d around you. Enemies caught within are knocked back %d tiles and take %d%% shield damage as lightning, and any projectiles will be destroyed.
		While this talent is not on cooldown, you also project a magnetic field from your shield, reducing the speed of incoming projectiles by %d%% and your chance to be critically hit by %d%%.]], [[你从盾牌中发射出强大的磁性能量冲击波，半径为 %d 码范围。所有被击中的敌人会被击退 %d 码，并受到 %d%% 闪电盾牌伤害。所有的抛射物也会被摧毁。
		当这一技能不处于冷却时间的时候，你会从盾牌中发射出一个磁性力场，降低所有瞄准你的抛射物速度 %d%%，并且你被暴击的几率降低 %d%%。]], "tformat")
t("Capacitor Discharge", "电力放出", "talent name")
t([[Mount capacitors to your shield that dampen the impact of attacks, increasing block value by %d%% and storing 100%% of the damage blocked as an electrical charge (to a maximum of %d).
Activating this ability discharges blocked damage, firing a bolt of lightning dealing %d%% shield damage as lightning to the first target, then projecting a bolt of lightning that arcs to %d other targets dealing lightning damage equal to the stored amount.
If at maximum charge, this also dazes for 2 turns and the shield strike is a guarenteed critical hit.
The maximum damage you can absorb will increase with your Steampower.]], [[将电容器放置在你的盾牌上，它们可以减弱攻击的影响。增加 %d%% 的格挡值，并将 100%% 格挡的伤害转化为电力充能（最多充能 %d 点）。
启动这一技能将会放出格挡的伤害，并发射出一道闪电冲击，对第一个目标造成 %d%% 闪电盾牌伤害，并产生一股电弧，对最多 %d 个其他目标产生相当于你存储的伤害量的伤害。
如果你的伤害充能满了，被击中的目标还会被眩晕 2 回合，且盾牌攻击必定暴击。
你能够吸收的最大伤害量受蒸汽强度加成。]], "tformat")
t("Lightning Web", "闪电之网", "talent name")
t("lightning web", "闪电之网", "_t")
t([[Project a radius 3 electric field from your shield lasting %d turns. Enemies within this field will take an automatic shield strike for %d%% lightning damage each turn, while allies will gain flat damage reduction equal to %d%% (%d) of block value.
		All damage reduced by this effect will be stored for Capacitor Discharge.]], [[从盾牌投射一道半径 3 码、持续 %d 回合的电场。电场内的敌人每回合会自动受到一次盾牌攻击，造成 %d%% 闪电盾牌伤害；盟友则获得相当于格挡值 %d%%（%d）的固定伤害减免。
		此效果减免的全部伤害都会为“电力放出”储存。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/mecharachnid.lua"

t("disarmed", "被缴械", "_t")
t("no ammo", "没有弹药", "_t")
t("bad ammo", "弹药错误", "_t")
t("incompatible missile launcher", "导弹发射器不兼容", "_t")
t("incompatible ammo", "弹药不兼容", "_t")
t("no shooter", "没有发射器", "_t")
t("Mecharachnid Link", "机械蜘蛛链接", "talent name")
t("Link to the summoner.", "链接到召唤者。", "_t")
t("Self-destruction", "自爆", "talent name")
t([[The mecharachnid self-destructs, destroying itself and generating a blast of fire in a radius of %d, doing %0.2f fire damage.
		This spell is only usable when the mecharachnid's master is dead.]], [[机械蜘蛛引爆自己，摧毁机械蜘蛛并在 %d 码范围内产生一个火焰爆炸，造成 %0.2f 火焰伤害。
		这个技能只有机械蜘蛛的主人死亡时能够使用。]], "tformat")
t("A heavily armored mechachnical spider, armed to the teeth with advanced weaponry.", "一只身披重甲、以先进武器武装到牙齿的机械蜘蛛。", "_t")
t("Your mecharachnid is out of sight; you cannot establish direct control.", "你的机械蜘蛛在视野外，你无法建立直接控制。", "logPlayer")
t("Mecharachnid", "机械蜘蛛", "talent name")
t("mecharachnid", "机械蜘蛛", "_t")
t("%s (servant of %s)", "%s (%s的仆人)", "tformat")
t("mecharachnid (servant of %s)", "机械蜘蛛 (%s的仆人)", "tformat")
t("Not enough space to invoke!", "没有足够的空间召唤！", "logPlayer")
t("Your mecharachnid is not dead.", "你的机械蜘蛛没有死。", "logPlayer")
t([[You build a mighty mechanical arachnid to assist you in combat. You can equip the mecharachnid with 2 steamguns, ammunition, and armor of your choice.
If your mecharachnid is dead, this will resurrect it with %d%% of its maximum life. Your mecharachnid is automatically rebuilt at full life when combat ends.
Your mecharachnid has level %d Steamgun Mastery, Combat Accuracy and Armor Training. The mecharachnid uses Dexterity instead of Strength to equip armor.
The mecharachnid has an inbuilt teleportation device that will recall it to you when combat ends if it is not nearby.]], [[你建造一台强大的机械蜘蛛，和你并肩作战。你可以给机械蜘蛛装备 2 把蒸汽枪，弹药，以及任何你喜欢的护甲。
如果机械蜘蛛死了，这一技能会重建它，并恢复它 %d%% 的最大生命值。你的机械蜘蛛会在战斗结束后快速重建，恢复全部生命值。
你的机械蜘蛛获得 %d 级蒸汽枪掌握、强化命中和重甲训练技能。机械蜘蛛使用敏捷代替力量装备护甲。
机械蜘蛛带有一个内置的传送装置，如果在战斗结束后它不在你的附近，会自动传送到你的身边。]], "tformat")
t("Stormcoil Generator", "风暴线圈发电机", "talent name")
t("You equip your mecharachnid with a stormcoil generator, a mechanical device that projects a powerful electrical field. On taking a hit greater than 15%% of its maximum life, the excess damage will be reduced by %d%% and converted into energy, giving your mecharachnid %d%% increased global speed for 2 turns.", "你给机械蜘蛛装备风暴线圈发电机，这一装置可以产生强大的电力场。当受到超过最大生命值 15%% 的伤害的时候，超过的伤害将会被降低 %d%%，并被转化为能量，增加机械蜘蛛 %d%% 的整体速度，持续 2 回合。", "tformat")
t("Mecharachnid Chassis", "机械蜘蛛底盘", "talent name")
t("Assault", "强袭", "_t")
t("Armament", "武装", "_t")
t("#LIGHT_RED#You must not be in combat to change the chassis.", "#LIGHT_RED#你必须在战斗外才能切换底盘。", "logPlayer")
t("#LIGHT_RED#Your mecharachnid must not be in combat to change its chassis.", "#LIGHT_RED#你的机械蜘蛛必须在战斗外才能切换底盘。", "logPlayer")
t("#LIGHT_RED#Your mecharachnid is already in chassis %s.", "#LIGHT_RED#你的机械蜘蛛已经处于%s底盘。", "logPlayer")
t("Mecharachnid chassis changed to: #GOLD#%s", "机械蜘蛛底盘切换为：#GOLD#%s", "logPlayer")
t("You require your mecharachnid to be adjacent, and must be out of combat.", "你需要你的机械蜘蛛与你相邻，并且你和机械蜘蛛都必须处于非战斗状态。", "logPlayer")
t([[You craft a new chassis for your mecharachnid, allowing you to tailor it to different situations. Each chassis grants the mecharachnid a new talent category, the ability to attach a weapon to their tail, as well as granting them %d class talent points to spend in a new category based off their chassis.

		You can choose from the 2 chassis below by activating this talent outside of combat (default chassis: Assault)
		- Assault: An armored chassis focused on close combat and defenses, specialising in wielding a steamsaw.
		- Armament: A heavily armed chassis focused on ranged combat, specialising in wielding an additional steamgun.

		Tail weapons do not attack by default, and are instead used for special talents.]], [[为机械蜘蛛打造一具新底盘，使其能够适应不同情况。每种底盘都会赋予机械蜘蛛一个新技能大系，使其可以在尾部安装武器，并提供 %d 点职业技能点，用于学习该底盘提供的新大系技能。

		在战斗外激活此技能，可以从以下两种底盘中选择（默认底盘：强袭）：
		- 强袭：专注近战与防御的装甲底盘，擅长使用蒸汽链锯。
		- 武装：专注远程战斗的重火力底盘，擅长额外使用一把蒸汽枪。

		尾部武器默认不会自动攻击，而是用于施展特殊技能。]], "tformat")
t("Mecharachnid Piloting", "驾驶机械蜘蛛", "talent name")
t("You require your mecharachnid to be adjacent.", "你需要你的机械蜘蛛在你身边。", "logPlayer")
t("Leap into your mecharachnid, assuming direct control of it for %d turns. While piloting it, all damage dealt is increased by %d%%, resistances are increased by %d%%, and all of its talents cooldown twice as fast.", "跳入机械蜘蛛，直接控制它 %d 回合。当控制它的时候，它所造成的所有伤害增加 %d%%，抗性增加 %d%%，所有技能冷却时间减半。", "tformat")
t("steamtech", "蒸汽科技", "talent category")
t("armament", "武装", "talent type")
t("Ranged combat mecharachnid abilities.", "机械蜘蛛的远程战斗技能。", "_t")
t("assault", "强袭", "talent type")
t("Close combat mecharachnid abilities.", "机械蜘蛛的近身战斗技能。", "_t")
t("Overrun", "超速撞击", "talent name")
t("You require a tail-mounted steamsaw for this talent.", "你必须要尾部安装蒸汽链锯才能使用这一技能。", "logPlayer")
t("Your mecharachnid cannot do that currently.", "你的机械蜘蛛目前不能这么做。", "logPlayer")
t("#Source# provokes #Target# to attack it.", "#Source#强制#Target#攻击它。", "logCombat")
t([[You rush to the target and strike with your tailsaw, dealing %d%% damage and taunting enemies within radius %d.
		You now also use your Dexterity in place of Strength when equipping Steamsaws as well as when calculating weapon damage, and have your Steamsaw damage increased by %d%% and Physical Power by %d.]], [[你冲向敌人，用尾部蒸汽链锯进行攻击，造成 %d%% 伤害，并嘲讽半径 %d 码内的所有敌人。
		装备蒸汽链锯的时候，你使用敏捷代替力量值计算装备需求和计算武器伤害，并且增加你蒸汽链锯的伤害 %d%%，物理强度 %d。]], "tformat")
t("Defensive Protocol", "防御协议", "talent name")
t("Enhancements to your mecharachnid combat skill increases your melee and ranged evasion by %d%%, and causes you to automatically strike adjacent enemies with your tailsaw for %d%% damage each turn.", "强化机械蜘蛛的近身战斗能力，增加 %d%% 概率躲闪近战和远程攻击，你每回合会自动用尾部的蒸汽链锯打击临近的敌人，造成 %d%% 伤害。", "tformat")
t("Pincer Strike", "钢爪钳制", "talent name")
t("#Target# resists the pincer strike from #Source#!", "#Target#抵抗了#Source#的钢爪钳制！", "logCombat")
t("You strike the target with your tailsaw for %d%% damage. If this hits, you attempt to clamp them with your pincers for %d turns. This pins, reduces their attack, spell and mind speed by %d%%, and lets you make a free, unavoidable strike with your tailsaw against them each turn for %d%% damage. This ends if you move more than 1 tile from the target.", "你用尾部蒸汽链锯攻击目标，造成 %d%% 伤害。若命中，你会尝试用钳爪将目标钳制 %d 回合，使其定身，并使其攻击、法术和精神速度降低 %d%%。在此期间，你每回合都会用尾部蒸汽链锯对其发动一次额外且无法闪避的攻击，造成 %d%% 伤害。若你与目标的距离超过 1 格，该效果结束。", "tformat")
t("Automated Repair System", "自动修复系统", "talent name")
t([[On falling below 0 life, you engage an automated repair mode. While in this mode you cannot act, but can survive below -%d life, heal for %0.1f life each turn and have all resistances increased by %d%%. This will last until you are destroyed or until you are fully healed.
		This effect has a cooldown.]], [[当生命值降低到 0 点以下的时候，你会启动自动修理模式。在自动修理模式下，你不能活动，生命值下限为 -%d，每回合恢复 %0.1f 生命值，并且所有抗性增加 %d%%。这一效果直到你的生命值完全恢复或者你被摧毁才会终止。
		这一效果具有冷却时间。]], "tformat")
t("Gauss Cannon", "电磁炮", "talent name")
t("You require a tail-mounted steamgun for this talent.", "你必须要尾部安装蒸汽枪才能使用这一技能。", "logPlayer")
t([[Fire a charged shot at the farthest target with your tail-mounted steamgun that pierces through your enemies, ignoring armor and dealing %d%% weapon damage as lightning.
		This takes no time to use.]], [[用尾部蒸汽枪发射充能射击，攻击离你最远的敌人，击穿路径上所有敌人，无视护甲，造成 %d%% 闪电武器伤害。
		使用这一技能不需要消耗时间。]], "tformat")
t("Magnetic Accelerator", "磁性加速", "talent name")
t("You must have an empty space to leap to.", "你必须有一块空地才能跳跃过去。", "logPlayer")
t([[Improved power output increases the speed of your projectiles by %d%%, critical damage by %d%%, and allows you to automatically reload each turn.
		In addition, you can instantly activate this talent to gain a sudden burst of speed, moving to a tile in range %d.]], [[增强你的能量输出，你的抛射物速度加快 %d%%，暴击伤害增加 %d%%，你每回合会自动填弹。
		另外，你可以主动激活这一技能，获得超人的移动速度，立刻移动到 %d 码范围内的某个格子内。]], "tformat")
t("Haywire Missiles", "导弹乱射", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t([[Fires a barrage of charged missiles from your tail-mounted steamgun at a radius %d area, dealing %d%% steamgun damage as lightning as well as dazing those within for 2 turns.
		The daze chance increases with your Accuracy.]], [[从尾部蒸汽枪向半径 %d 格的区域发射一轮充能导弹，造成相当于 %d%% 蒸汽枪伤害的闪电伤害，并使区域内目标眩晕 2 回合。
		眩晕几率随命中提高。]], "tformat")
t("Advanced Targeting System", "高级瞄准", "talent name")
t([[Enhancements to your targeting systems give all ranged attacks a %d%% chance to trigger an immediate shot from your tail-mounted steamgun for 100%% damage as lightning.
		In addition, your physical and lightning resistance penetration is increased by %d%%.]], [[强化你的瞄准能力，你的所有远程攻击有 %d%% 几率触发一次尾部蒸汽枪的射击，造成 100%% 闪电武器伤害。
		另外，你的物理和闪电伤害抗性穿透增加 %d%%。]], "tformat")
t("Tail Attachment", "尾部武器", "talent name")
t("%s mounts %s to its tail.", "%s将%s装备到尾部。", "logSeen")
t("Attach which item?", "装备哪一件物品？", "_t")
t("Attach the chosen weapon to your tail.", "将选择的武器装备到尾部。", "_t")

------------------------------------------------

section "tome-orcs/data/talents/steam/mechstar.lua"

t("Metalstar", "金属灵晶", "talent name")
t([[Quickly aggregate particles of metal around your mindstar and focus psionic energies into it.
		The metal explodes like shrapnel, knocking back (%d away) and dazing (%d duration) all foes in radius %d.]], [[迅速将金属粒子聚集到灵晶周围，并把灵能集中其中。
		金属如弹片般爆裂，将所有敌人击退 %d 格、眩晕 %d 回合，作用半径为 %d 格。]], "tformat")
t("Bloodstar", "血液灵晶", "talent name")
t([[When you fire your metalstar, your also establish a psionic bloodlink with the shrapnel still inside for %d turns.
		Each turn the victims are drained for %0.2f physical damage, half of which heals you (each additional victim healing is reduced by half).
		If the victim move more than twice away from the radius of Metalstar (currently %d) the effect stops.
		This damage does not break daze and increases with your Steampower.]], [[每次你使用灵晶射击时，你将与灵晶碎片建立血液灵能联系，持续 %d 回合。
		每回合目标将受到 %0.2f 物理伤害，一半伤害值将转化为治疗。
		每增加一名额外目标，其带来的治疗量进一步减半。
		当目标距离超过金属灵晶范围（当前 %d）的两倍时，效果中止。
		该伤害不会打断眩晕效果，受蒸汽强度加成。]], "tformat")
t("Steamstar", "蒸汽灵晶", "talent name")
t([[Your bloodstar effect also burns part of your victim's flesh, dealing %0.2f fire damage.
		The intensity of the fire generates steam which you psionically absorb through gestalt, providing %d steam each turn (each additional victim steam generation is reduced by 66%%).
		This damage does not break daze and increases with your Steampower.]], [[你的血液灵晶效果同时造成 %0.2f 火焰伤害。
		火焰同时产生蒸汽，每回合提供 %d 蒸汽，从每个额外目标处获得的蒸汽数量减少 66%%。
		该伤害不会打断眩晕效果，受蒸汽强度加成。]], "tformat")
t("Deathstar", "死亡灵晶", "talent name")
t("When you use a shoot class talent to hit a creature affected by bloodstar an other shoot talent will have its current cooldown reduced by %d turns.", "每次你使用射击类技能命中一个被血液灵晶影响的目标时，随机另一项冷却中的射击类技能冷却时间减少 %d 回合。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/other.lua"

t("Medical Injector", "医疗注射器", "talent name")
t("Medical Urgency Vest", "医疗急救背心", "talent name")
t("#LIGHT_BLUE#Medical Urgency Vest selected to be used first by salves.", "#LIGHT_BLUE#已将医疗急救背心设置为药剂的首选注射器。", "saySimple")
t("This medical injector will now be used first if available when using medical salves.", "使用医疗药剂时，如果可用，将优先使用此医疗注射器。", "logPlayer")
t("The medical urgency vest allows using therapeutics with %d%% efficiency and cooldown mod of %d%%.", "医疗急救背心能以 %d%% 的效率使用药物，冷却时间修正为 %d%%。", "tformat")
t("Life Support", "生命支持系统", "talent name")
t("#LIGHT_BLUE#Life Support Suit selected to be used first by salves.", "#LIGHT_BLUE#已将生命支持服设置为药剂的首选注射器。", "saySimple")
t("The life support suit allows using therapeutics with %d%% efficiency and cooldown mod of %d%%.", "生命支持服能以 %d%% 的效率使用药物，冷却时间修正为 %d%%。", "tformat")
t("Create Tinker", "制造道具", "talent name")
t("Allows you to create tinkers.", "使用该技能来制造药剂、附着物等道具。", "_t")
t("Weapon Automaton: One Handed", "武装机器人：单手模式", "talent name")
t("You cannot use %s without a one handed melee weapon in your inventory!", "你的物品栏里面没有单手武器，无法使用%s！", "logPlayer")
t("Select a weapon for your Automaton", "选择用于武装机器人的武器", "_t")
t("Weapon Automaton: %s", "武装机器人：%s", "tformat")
t("An Automaton wielding a chosen weapon.", "手握武器的武装机器人。", "_t")
t("#F53CBE#%s runs out of power.", "#F53CBE#%s能量耗尽。", "logSeen")
t("Summon", "召唤", "_t")
t([[Deploy a Weapon Automaton based on a selected one handed melee item.  The Automaton will wield the selected weapon and drop it when it times out or is destroyed.  Aside from the weapon selected, the Automaton will scale off Tinker talent levels, your own stats, and other things that will be described in this tooltip at some point.  
		]], [[以选定的单手近战物品为基础部署一个武装机器人。机器人会使用所选武器，并在持续时间结束或被摧毁时掉落该武器。除所选武器外，机器人的强度还会随工匠技能等级、你的属性，以及将来某天会写进这段说明里的其他因素提升。
		]], "tformat")
t("Hand Cannon", "手炮", "talent name")
t("You have no ammo!", "你没有子弹！", "logPlayer")
t([[Fires your ammo at an enemy in range %d for %d%% weapon damage.  If this tinker is made of voratun you will fire an additional shot.
			This shot is a ranged melee attack but will use the ranged procs of your ammo as well.]], [[向在 %d 码范围内的一个敌人开火造成 %d%% 的武器伤害。如果手炮是由沃瑞钽钢制作的，你能多一次额外的射击。射击是远程攻击将会触发弹药特效。]], "tformat")
t("Fatal Attractor", "致命诱饵", "talent name")
t("Not enough space to summon!", "没有足够的空间召唤！", "logPlayer")
t("fatal attractor", "致命诱敌装置", "_t")
t("A psionic contraption that reflects damage and forces things to attack it.", "一个反射伤害并迫使物体攻击的灵能装置。", "_t")
t([[Quickly create a psionic-enhanced metal contraption that lures all your foes to it and reflects %d%% of the damage it takes to its attackers.
		The contraption will have %d life and last 5 turns.
		Damage, life, resists, and armor scale with your Steampower.]], [[快速制造一个灵能强化的金属装置，吸引所有敌人攻击它，并将其所受伤害的 %d%% 反弹给攻击者。
该装置拥有 %d 点生命值，持续 5 回合。
其伤害、生命值、抗性和护甲随你的蒸汽强度提升。]], "tformat")
t("Rocket Boots", "火箭靴", "talent name")
t([[Activate the rocket boots, firing huge flames from your boots increasing your movement speed by %d%%.
		Each movement will leave a trail of flames doing %0.2f fire damage for 4 turns.
		Doing any other actions will break the effect.
		#{italic}#Burninate them all!#{normal}#]], [[激活火箭靴，从你的靴子上发射巨大的火焰，增加你的移动速度 %d%%。
每次移动都会留下一道火焰持续 4 回合的伤害为 %0.2f 的火焰。
做任何其他行动都会打断效果。
#{italic}#烧毁他们 !#{normal}#]], "tformat")
t("Iron Grip", "铁腕", "talent name")
t("%s resists the iron grip!", "%s抵抗了铁腕抓取！", "logSeen")
t([[Activate the pistons to crush your target for %d turns and dealing %d%% unarmed melee damage.
		While the target is held it can not move and its armour and defense are reduced by %d.
		#{italic}#Crush their bones!#{normal}#]], [[激活活塞碾压你的目标 %d 回合，并造成 %d%% 的徒手伤害。
被碾压的目标会被定身，且其护甲和闪避减少 %d。
#{italic}#压碎他们的骨头 !#{normal}#]], "tformat")
t("Spring Grapple", "弹簧飞爪", "talent name")
t("%s resists the pin!", "%s抵抗了定身！", "logSeen")
t("Grab the target and pull them towards you, striking for %d%% unarmed melee damage, and if you hit, pinning them for %d turns.", [[抓住目标把目标向你拉拢，造成 %d%% 的徒手伤害，如果命中，目标定身 %d 回合。]], "tformat")
t("Toxic Cannister Launcher", "毒罐发射装置", "talent name")
t("toxic cannister", "毒罐", "_t")
t("A smelly cannister.", "一个放出气味的罐子。", "_t")
t([[Launch a cannister filled with toxic gas at a location.
		Every 2 turns the cannister emits a poison cloud of radius 3 around it each turn.
		The poison does %0.2f nature damage over 5 turns.
		The cannister has %d life and lasts 8 turns. When it ends or is destroyed a last cloud is created.
		Damage, life, resists, and armor scale with your Steampower.
		Damage and penetration are inherited from the creator.]], [[发射一个充满有毒气体的罐子。
每 2 回合在此周围发出一个半径为 3 码的毒雾。
毒雾在 5 回合内造成 %0.2f 的自然伤害。
发生器有 %d 点生命值持续 8 回合。当它被摧毁或持续时间结束会发出最后一片毒雾。
伤害，生命值，抗性和护甲值取决于你的蒸汽强度。
从创造者处继承伤害和穿透。]], "tformat")
t("Steam Powered Armour", "蒸汽动力装甲", "talent name")
t([[Activate the armour's active defense system.
		A flow of electricity covers your armour to attenuate the force of energy attacks while small steam engines move key pieces of the armour to attenuate physical attacks.
		All damage except mind damage is reduced by a flat %d.
		In addition the electric power of the armour sometimes leaks, each turn there is a 50%% chance to produce a electrical arc toward a foe, dealing %0.2f to %0.2f lightning damage to all foes in radius 1.
		The effects increase with your Steampower.]], [[激活护甲的主动防御系统。
电流覆盖护甲，削弱能量攻击的威力；与此同时，小型蒸汽引擎会移动护甲的关键部件，以削弱物理攻击。
除精神伤害外，所有伤害都会固定减少 %d 点。
此外，护甲的电力有时会泄漏：每回合有 50%% 几率向一名敌人放出电弧，对其半径 1 内的所有敌人造成 %0.2f 至 %0.2f 点闪电伤害。
效果随蒸汽强度提升。]], "tformat")
t("Viral Needlegun", "病毒针枪", "talent name")
t([[You fire a cone of blighted needles, hitting everything in a frontal cone of radius %d for %0.2f physical damage.
		Each creature hit has a %d%% chance of being infected by a random disease, doing %0.2f blight damage and reducing either Constitution, Strength or Dexterity by %d for 20 turns.
		The damage and disease effects increase with your Steampower.]], [[你射出一片枯萎的针，打击 %d 码锥形范围内的目标，造成 %0.2f 的物理伤害。
每个命中目标都有 %d%% 几率感染一种随机疾病，造成 %0.2f 枯萎伤害同时降低体质，力量或敏捷 %d 点持续 20 回合。
		伤害和疾病效果受蒸汽强度加成。]], "tformat")
t("Sand Shredder", "砂土粉碎", "talent name")
t("%s shreds through sandwalls!", "%s 挖开沙墙！", "logSeen")
t("You shred pieces of sandwalls. Brrrmmm!.", "你碎裂了沙墙。布鲁——！", "_t")
t("Flamethrower", "火焰喷射器", "talent name")
t([[Throw a cone of flame with radius %d
		The damage will increase with your Steampower.]], [[在 %d 码范围内放出锥形火焰
		伤害受蒸汽强度加成。]], "tformat")
t("Mass Repair", "大规模修复", "talent name")
t([[Throw a cone of healing with radius %d, healing other mechanical creatures (steam spiders) for %d.
		The healing will increase with your Steampower.]], [[释放一片锥形半径 %d 码的修理器，修复机械生物（蒸汽蜘蛛）%d 生命值。
　　治疗量受蒸汽强度加成。]], "tformat")
t("Arcane Disruption Wave", "奥术干扰波", "talent name")
t([[Let out a technopsionic wave that silences for %d turns all those affected in a radius of %d, including the user.
		The silence chance will increase with your Steampower.]], [[制造一道科技灵能波，使所有受影响者（包括使用者）沉默 %d 回合，作用半径为 %d 格。
沉默几率随蒸汽强度提高。]], "tformat")
t("Mind Crush", "精神碾压", "talent name")
t("%s resists the mental assault!", "%s抵抗了精神攻击！", "logSeen")
t([[Shatters the mind of your victim, giving you full control over its actions for 6 turns.
		When the effect ends, you pull out your mind and the victim's body collapses, dead.
		This effect does not work on rares, bosses, or undead.
		.]], [[粉碎你的受害者的内心，给你完全控制其行为 6 回合。
　　当效果结束时，你抽出了自己的思维，受害者的身体会崩溃，死亡。
　　稀有怪、boss、亡灵不受控制。]], "tformat")
t("Shocking Touch", "电击之触", "talent name")
t([[Touch a creature to release a nasty electrical charge into them, doing %0.2f lightning damage.
		If this tinker is above tier 1, the electricity can arc to another target up to 2 tiles away.
		The number of enemies hit is at most the tinker tier.
		The damage increases with your Steampower.]], [[触碰一个生物，将猛烈的电流注入其体内，造成 %0.2f 点闪电伤害。
如果这件蒸汽工具高于 1 级，电流可以跳向最远 2 格内的另一个目标。
命中的敌人数量最多等于蒸汽工具的等级。
伤害随蒸汽强度提高。]], "tformat")
t("Flash Powder", "闪光粉", "talent name")
t("%s resists the blinding light!", "%s抵抗了致盲！", "logSeen")
t([[Throw a handful of dust that rapidly oxidises, releasing a blinding light.
		Creatures in a cone of radius %d are blinded for %d turns.
		The blindness effect is applied with your Steampower.]], [[扔一把尘土，迅速氧化，释放出眩目的光芒。
		致盲锥形半径 %d 码内的生物 %d 回合。
		致盲强度受蒸汽强度加成。]], "tformat")
t("Itching Powder", "痒痒粉", "talent name")
t("%s resists the itching powder!", "%s 抵抗了痒痒粉！", "logSeen")
t([[Throw a handful of dust that is very itchy to touch.
		Creatures in a cone of radius %d are itchy for %d turns, causing them to fail talents %d%% of the time.
		The itchiness effect is applied with your Steampower.]], [[释放一把痒痒粉。
		锥形半径 %d 码内的生物 %d 回合内很痒，导致它们释放技能 %d%% 几率失败。
		致痒强度受蒸汽强度加成。]], "tformat")
t("Thunder Grenade", "闪电榴弹", "talent name")
t("%s resists the explosion!", "%s 抵抗了爆炸！", "logSeen")
t([[Throw a grenade at your foes, dealing %0.2f physical damage in radius %d.
		Creatures hit will also be stunned for %d turns.
		The stun effect is applied with your Steampower.]], [[向你的敌人投掷手榴弹，造成 %0.2f 物理伤害，半径 %d 码。
　　目标也会震慑 %d 回合。
　　震慑强度受蒸汽强度加成。]], "tformat")
t("Project Saw", "发射链锯", "talent name")
t([[You activate hidden springs to project a saw towards your foes.
		Any creature caught in the beam takes %0.2f physical damage and bleeds for half more in 5 turns.
		The damage increases with your Steampower.]], [[你启动隐藏的弹簧，向敌人射出一片锯刃。
任何被光束命中的生物都会受到 %0.2f 点物理伤害，并在 5 回合内额外受到相当于一半伤害的流血伤害。
伤害随蒸汽强度提高。]], "tformat")
t("Voltaic Bolt", "闪电球", "talent name")
t([[Fires a bolt of lightning, doing %0.2f lightning damage.
		The damage will increase with your Steampower.]], [[释放一个闪电球，造成 %0.2f 闪电伤害。
伤害受蒸汽强度加成。]], "tformat")
t("Voltaic Sentry", "伏特守卫", "talent name")
t("volatic sentry", "伏特守卫", "_t")
t("A strange device. Your hair stands on end when you approach.", "一个奇怪的装置。当你走近时，你的头发竖起来了。", "_t")
t([[Place an electrically charged sentry device at a location.
		Every turn it will fire a bolt of electricity at a nearby enemy.
		The bolts do %0.2f lightning damage.
		The sentry has %d life and lasts 10 turns.
		Damage, life, resists, and armor scale with your Steampower.
		Damage and penetration are inherited from the creator.]], [[在指定位置放置一个带电的哨兵装置。
它每回合会向附近的敌人发射一道电流，造成 %0.2f 点闪电伤害。
哨兵拥有 %d 点生命，持续 10 回合。
伤害、生命、抗性和护甲随你的蒸汽强度提高。
伤害和抗性穿透继承自创造者。]], "tformat")
t("Explosive Shell", "爆炸弹", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t([[You fire a special explosive shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it does normal steamgun damage and explodes within radius %d, which does %0.2f physical damage.
		This talent does not use ammo as it is the ammo.]], [[你使用蒸汽枪在射程内制造一场特殊的爆炸。
　　当每一个弹片击中它的目标，造成正常蒸汽枪伤害和半径 %d 码内的爆炸，造成 %0.2f 的物理伤害，
　　这个技能不使用弹药。]], "tformat")
t("Flare Shell", "闪光弹", "talent name")
t([[You fire a special explosive shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it does normal steamgun damage and explodes within radius %d, which lights up the area and blinds for %d turns.
		This talent does not use ammo as it is the ammo.]], [[你用蒸汽枪向射程内的一处地点发射特殊爆炸弹。
每发子弹命中目标时都会造成正常蒸汽枪伤害，并在半径 %d 格内爆炸，照亮该区域并致盲其中的生物 %d 回合。
这个技能本身就是弹药，因此不消耗弹药。]], "tformat")
t("Incendiary Shell", "燃烧弹", "talent name")
t("clusterbomb", "集束炸弹", "_t")
t([[You fire a special explosive shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it does normal steamgun damage and releases %d explosive charges in a radius of 2.
		These charges will shortly explode for %0.2f fire damage in a radius of 1.
		This talent does not use ammo as it is the ammo.]], [[你用蒸汽枪向射程内的一处地点发射特殊爆炸弹。
每发子弹命中目标时都会造成正常蒸汽枪伤害，并在半径 2 格内释放 %d 枚爆炸装药。
这些装药很快就会爆炸，对半径 1 格内的目标造成 %0.2f 点火焰伤害。
这个技能本身就是弹药，因此不消耗弹药。]], "tformat")
t("Solid Shell", "固实弹", "talent name")
t("%s is knocked back!", "%s 被击退！", "logSeen")
t("%s resists the knockback!", "%s抵抗了击退！", "logSeen")
t([[You fire a special solid shot with your steamgun(s) at a target for %d%% physical weapon damage.
		The weight of the shot will knock the target back %d tiles.
		This talent does not use ammo as it is the ammo.]], [[你使用蒸汽枪发射特殊实心弹，造成 %d%% 物理武器伤害。
		弹头的重量会将目标击退 %d 格。
		这个技能本身就是弹药，因此不消耗弹药。]], "tformat")
t("Impaler Shell", "穿刺弹", "talent name")
t([[You fire a special stake shot with your steamgun(s) at a target for %d%% physical weapon damage.
		The weight of the shot will knock the target back 2 tiles and they will be pinned for %d turns.
		This talent does not use ammo as it is the ammo.]], [[你使用蒸汽枪发射特殊尖桩弹，造成 %d%% 物理武器伤害。
		弹头的重量会将目标击退 2 格，并使其定身 %d 回合。
		这个技能本身就是弹药，因此不消耗弹药。]], "tformat")
t("Saw Shell", "链锯弹", "talent name")
t([[You fire a special steamsaw shot with your steamgun(s) at a target for %d%% physical weapon damage.
		The steamsaw will cut into the target, doing %d%% physical weapon damage over 5 turns.
		This talent does not use ammo as it is the ammo.]], [[你使用蒸汽枪发射特殊蒸汽链锯弹，造成 %d%% 物理武器伤害。
		蒸汽链锯会切入目标，在 5 回合内造成 %d%% 物理武器伤害。
		这个技能本身就是弹药，因此不消耗弹药。]], "tformat")
t("Hook Shell", "钩链弹", "talent name")
t("%s resists the pull!", "%s抵抗了拖动！", "logSeen")
t([[You fire a special hook shot with your steamgun(s) at a target creature or location.
		If you target a creature, they are pulled up to %d tiles towards you.
		If you target an empty tile, you are pulled up to %d tiles towards it.
		This talent does not use ammo as it is the ammo.]], [[你使用蒸汽枪发射特殊弹药打击目标或某处
如果你的目标是一个生物，他们被拉向你 %d 码
如果你的目标是一个空地，你会被拉向空地 %d 码
这个技能不使用弹药。]], "tformat")
t("Magnetic Shell", "磁性弹", "talent name")
t([[You fire a special magnetic shot with your steamgun(s) at a target for normal weapon damage.
		The shot will magnetise the target for %d turns. This lowers their defense and increases fatigue by %d.
		This talent does not use ammo as it is the ammo.
		Effect strength scales with Steampower.]], [[你用蒸汽枪向目标发射特殊磁化弹，造成正常武器伤害。
子弹会使目标磁化 %d 回合，降低其闪避并增加 %d 点疲劳。
这个技能本身就是弹药，因此不消耗弹药。
效果强度随蒸汽强度提高。]], "tformat")
t("Voltaic Shell", "伏特弹", "talent name")
t([[You fire a special voltaic shot with your steamgun(s) at a target for 100%% weapon damage as lightning.
		The shot will release powerful electrical currents at up to %d nearby enemies. 
		Each bolt does %0.2f lightning damage.
		This talent does not use ammo as it is the ammo.
		Bolt damage scales with Steampower.]], [[你使用蒸汽枪发射特殊弹药打击目标造成 100%% 闪电武器伤害。
这将释放强大的电流，打击周围 %d 的敌人。
每个闪电球造成 %0.2f 的闪电伤害
这个技能不使用弹药
闪电球伤害受蒸汽强度加成。]], "tformat")
t("Antimagic Shell", "反魔弹", "talent name")
t([[You fire a special antimagic shot with your steamgun(s) at a target for 100%% normal weapon damage.
		The shot will release antimagic sap on the target, doing %0.2f arcane resource burn damage.
		This talent does not use ammo as it is the ammo.
		Sap damage scales with Steampower.]], [[你使用蒸汽枪发射特殊弹药打击目标造成 100%% 武器伤害。
造成 %0.2f 奥术燃烧。
这个技能不使用弹药。
奥术燃烧伤害取决于蒸汽强度。]], "tformat")
t("Botanical Shell", "植物弹", "talent name")
t([[You fire a special botanical shot with your steamgun(s) at a target for 100%% weapon damage as nature.
		The shot will release spores which grow into Nourishing Moss in a radius of %d for %d turns.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss has vampiric properties and heals the user for %d%% of the damage done.
		This talent does not use ammo as it is the ammo.
		Moss damage scales with Steampower.]], [[你使用蒸汽枪发射特殊弹药打击目标造成 100%% 自然武器伤害。
将释放孢子生长成半径 %d 的苔藓 %d 回合。
每回合苔藓造成 %0.2f 自然伤害对半径内的每一个敌人。
这种苔藓有吸血特性，伤害的 %d%% 治愈使用者。
这个技能不使用弹药
苔藓伤害受蒸汽强度加成。]], "tformat")
t("Corrosive Shell", "腐蚀弹", "talent name")
t([[You fire a special corrosive shot with your steamgun(s) at a target for %d%% weapon damage as acid.
		The acid released by the shot will also corrode the target, reducing its accuracy, defense and armour by %d.
		This talent does not use ammo as it is the ammo.
		Corrosion strength scales with Steampower.]], [[你用蒸汽枪向目标发射一枚特殊腐蚀弹，造成 %d%% 酸性武器伤害。
弹丸释放的酸液还会腐蚀目标，使其命中、闪避和护甲降低 %d 点。
此技能不会消耗弹药，因为弹丸本身就是弹药。
腐蚀强度随蒸汽强度提升。]], "tformat")
t("Toxic Shell", "毒气弹", "talent name")
t("%s resists the toxin!", "%s 抵抗了剧毒！", "logSeen")
t([[You fire a special toxic shot with your steamgun(s) at a target for 100%% weapon damage as blight.
		The shot will release heavy metals into the target, inflicting %0.2f blight damage per turn and reducing their global speed by %d%% for %d turns.
		This talent does not use ammo as it is the ammo.
		Toxin strength scales with Steampower.]], [[你使用蒸汽枪发射特殊弹药打击目标造成 100%% 枯萎武器伤害。
向目标释放重金属，造成每回合 %0.2f 枯萎伤害，并且降低整体速度 %d%% %d 回合。
这个技能不使用弹药。
枯萎伤害受蒸汽强度加成。]], "tformat")
t("Moss Tread", "苔藓之踏", "talent name")
t([[For %d turns, you lay down Grasping Moss where you walk or stand.
		The moss is placed automatically every step and lasts %d turns.
		Each turn the moss deals %0.2f nature damage to each foe standing on it.
		This moss is very thick and sticky causing all foes passing through it have their movement speed reduced by %d%% and have a %d%% chance to be pinned to the ground for 4 turns.
		The damage scales with your Steampower.]], [[在 %d 回合内，你会在走过或停留的位置铺下缠绕苔藓。
每走一步都会自动铺下苔藓，持续 %d 回合。
苔藓每回合对站在其上的每个敌人造成 %0.2f 自然伤害。
苔藓极其浓密黏稠，所有穿过它的敌人移动速度降低 %d%%，并有 %d%% 几率被定身 4 回合。
伤害随蒸汽强度提升。]], "tformat")
t("Arcane Dynamo", "奥术发电机", "talent name")
t([[Allows the use of Technomancy spells.
		Grants a magical steam reserve that regenerates %d steam per 10 mana spent.
		Grants Spellpower based on current steam level (currently %d; %d%% steam filled).
		Outside of combat, you relax and let your steam reserve slowly wither away.
		#{italic}#Metal Arcane Power!#{normal}#]], [[允许使用科技法术，
		获得一个魔法的蒸汽储备，每消耗10点法力值获得 %d 蒸汽。
		根据当前蒸汽等级获得法术强度（目前 %d；充满了 %d%% 蒸汽）
		在战斗外，你放松了控制，蒸汽储备会逐渐消退。
		#{italic}#金属奥术力量！#{normal}#]], "tformat")

------------------------------------------------
