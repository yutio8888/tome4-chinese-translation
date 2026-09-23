section "tome-orcs/data/talents/celestial/reflection.lua"

t("Diffraction Pulse", "衍射脉冲", "talent name")
t("Create a distortion at the target tile, knocking back all projectiles and changing their direction to face away if possible.", "在目标所在地创造一个地块，击退所有的飞行物如果可能的话还会改变他们的方向。", "_t")
t("Mirror Wall", "反射镜墙", "talent name")
t("mirror wall", "镜像之墙", "_t")
t("Creates a wall %d units long for %d turns, reflecting all projectiles that hit it and blocking sight.", "创造一堵墙长 %d 持续 %d 回合，反射所有击中此墙的飞行物并且阻挡视线。", "tformat")
t("Spatial Prism", "空间棱镜", "talent name")
t("Target a projectile in mid-flight to clone it and target that projectile independently. You gain ownership over the new projectile.", "选择一个飞行中的抛射物，复制它，并指定新抛射物的目标。你获得新的抛射物所有权。", "_t")
t("Mirror Self", "自我镜像", "talent name")
t("Mirror Image (%s)", "镜像 (%s)", "tformat")
t("A cloned image of you.", "你的克隆影像。", "_t")
t("Mirror Self", "自我镜像", "_t")
t("Summons a clone for %d turns which casts all the spells you cast, dealing %d%% damage and having %d%% health. Additionally, all light damage the clone deals becomes darkness damage and all darkness damage becomes light damage.", "召唤一个持续 %d 回合能施放你所有法术的镜像，造成 %d%% 的伤害和拥有 %d%% 生命值。此外，镜像造成的所有光伤害转换为暗影伤害，所有暗影伤害转换为光伤害。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/celestial/sol.lua"

t("Solar Orb", "日光球", "talent name")
t("Solar Orb", "日光球", "_t")
t("Fire out an orb of light that deals %0.2f light damage and then returns, dealing the same amount of damage again and reducing the cooldown by half (%d) when it reaches you. The damage will increase with your spellpower. The ball will travel at most %d distance to return to you.", "发射一个光球造成 %0.2f 的光伤害然后折返，再次造成相同的伤害并且当回到你身上的时候减少一半 (%d) 的冷却时间。伤害受法术强度加成。球体最多飞行 %d 然后折回你。", "tformat")
t("Solar Wind", "太阳风", "talent name")
t("While sustained, this ability speeds up outgoing projectiles by %d%% while slowing incoming projectiles by %d%%. The increase and decrease improve with your spellpower", "开启时，增加发射出去的抛射物 %d%% 速度，减少射向你的抛射物 %d%% 速度。增加和减少随着你的法术强度提高。", "tformat")
t("Lucent Wrath", "光之愤怒", "talent name")
t("After %d turns, the target area in (radius %d) is blasted with a beam of light, dealing %0.2f damage and lighting the area", "%d 回合后，一道光束轰击半径 %d 的目标区域，造成 %0.2f 点伤害并照亮该区域。", "tformat")
t("Lightspeed", "光速", "talent name")
t("%s moves at light speed!", "%s光速移动！", "logSeen")
t("Instantly gain %d%% percent of a turn.", "立刻获得 %d%% 的回合进度。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/celestial/void.lua"

t("Nebula Spear", "星云之矛", "talent name")
t("Fire out a spear of cosmic energies. If it hits an enemy it deals %0.2f damage, otherwise it explodes in a thin cone of radius %d at the end of its range, blocked by enemies, which deals %0.2f to %0.2f damage depending on how much the enemies block.", "发射一支宇宙能量长矛。若击中敌人，造成 %0.2f 点伤害；否则会在射程终点爆炸，形成半径 %d 的狭窄锥形区域。该效果会被敌人阻挡，并根据阻挡程度造成 %0.2f 到 %0.2f 点伤害。", "tformat")
t("Crescent Wave", "新月波动", "talent name")
t("Fires out a projectile in a clockwise arc. If it hits an enemy it deals %0.2f damage and roots them for one turn. If another projectile damages them within %d turns, they take half that damage and are rooted again.", "沿顺时针弧线发射一个投射物。若击中敌人，造成 %0.2f 点伤害并将其定身 1 回合。若另一个投射物在 %d 回合内对其造成伤害，该敌人会受到该次伤害的一半并再次被定身。", "_t")
t("Twilit Echoes", "暮光回响", "talent name")
t([[The target feels the echoes of all your light and dark damage for %d turns. 

Light damage slows the target by %0.2f%% per point of damage dealt for %d turns, up to a maximum of %d%% at %d damage.
Dark damage creates an effect at the tile for %d turns which deals %d%% of the damage dealt each turn. It will be refreshed as long as the target continues taking damage from it or another source while Twilit Echoes is active, dealing its remaining damage over the new duration as well as the new damage.]], [[目标会感受到你造成的所有光系和暗影伤害的回响，持续 %d 回合。

每造成 1 点光系伤害，目标便会减速 %0.2f%%，持续 %d 回合；减速上限为 %d%%，造成 %d 点伤害时达到上限。
暗影伤害会在目标所在格产生一个持续 %d 回合的效果，每回合造成该次伤害的 %d%%。在暮光回响生效期间，只要目标继续受到此效果或其他来源的伤害，该地块效果就会刷新；剩余伤害和新伤害会一并分摊到新的持续时间内。]], "tformat")
t("Starscape", "星界领域", "talent name")
t("This spell cannot be cast here.", "该技能不能在这里使用。", "logPlayer")
t("Summons the starscape in the surrounding area in a radius of %d. For %d turns, this area exists outside normal time, and in zero gravity. In addition to the effects of zero gravity, Movement of projectiles and other creatures is three times as slow. Spells and attacks cannot escape the radius until the effect ends.", "在 %d 范围内召唤一片星界领域。%d 回合内，这个区域存在于正常时间之外，且重力为零。除了零重力之外，抛射物和生物的活动比平时慢 3 倍。法术和攻击不能逃脱范围，直到效果结束。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/misc/npcs.lua"

t("Petrifying Gaze", "石化凝视", "talent name")
t([[Gaze at your foes and turn them to stone for %d turns.
		Stoned creatures are unable to act or regen life, and are very brittle.
		If a stoned creature is hit by an attack that deals more than 30%% of its life, it will shatter and be destroyed.
		Stoned creatures are highly resistant to fire and lightning, and somewhat resistant to physical attacks.
		This spell may fail against creatures resistant to being stunned, that are specifically immune to stoning, or certain bosses.]], [[凝视敌人，将其石化 %d 回合。
		被石化的生物无法行动或恢复生命，而且非常脆弱。
		如果一次攻击对被石化生物造成超过其生命值 30%% 的伤害，它就会碎裂并被摧毁。
		被石化生物对火焰和闪电具有极高抗性，对物理攻击也具有一定抗性。
		此法术可能无法作用于具有震慑抵抗、石化免疫的生物或某些首领。]], "tformat")
t("Gnashing Maw", "撕咬", "talent name")
t([[Hits the target with your weapon, doing %d%% damage. If the attack hits, the target's Accuracy is reduced by %d for %d turns.
		Accuracy reduction chance increases with your Physical Power.]], [[用武器攻击目标，造成 %d%% 伤害。若攻击命中，目标的命中降低 %d 点，持续 %d 回合。
		命中削减的成功几率受物理强度加成。]], "tformat")
t("Sandrush", "潜沙突袭", "talent name")
t("@Source@ dives in the sand!", "@Source@潜入沙中！", "_t")
t("You are too close to build up momentum!", "距离目标太近，无法蓄势！", "logPlayer")
t([[Dive into the sand and rush towards your target at up to range %d, gaining a free attack if you reach it.
		At the exit point, up to 9 sand pits will appear that last for %d turns (based on your Strength).
		You must rush from at least 2 tiles away.]], [[潜入沙中，朝最远 %d 码内的目标突进；若能抵达目标，则获得一次免费攻击。
		在跃出点生成最多 9 个沙坑，持续 %d 回合（受力量影响）。
		必须与目标至少相距 2 格才能发动突进。]], "tformat")
t("Ritch Larva Infect", "里奇幼虫寄生", "talent name")
t("@Source@ stings with her ovipositor!", "@Source@使用产卵器刺入敌人！", "_t")
t([[Sting the target with your ovipositor, injecting %d larvae into it to finish their hatching process.
		Over a 5 turn gestation period, the larvae will feed on the victim internally, dealing %0.2f to %0.2f physical damage each turn (increasing as they grow).
		After the gestation period is complete, each larva will rip itself free of its host, dealing %0.2f physical and %0.2f fire damage.
		]], [[用你的产卵器蜇目标一下，将 %d 个幼虫注入目标体内以完成他们的孵化流程。
		在一个 5 回合的发育周期内，幼虫们会以受害者的血肉为食，每回合造成 %0.2f 到 %0.2f 的物理伤害（随着他们的成长增多）。
		在发育期结束后，幼虫会从寄主体内钻出，每个幼虫造成 %0.2f 物理和 %0.2f 火焰伤害。
		]], "tformat")
t("Slumbering...", "沉睡中…", "talent name")
t("@Source@ enters a deep slumber.", "@Source@进入深睡眠。", "_t")
t("#STEEL_BLUE#%s slumbers...", "#STEEL_BLUE#%s睡着了……", "saySimple")
t("#CRIMSON#%s awakens!", "#CRIMSON#%s醒来了！", "saySimple")
t("The Dead God slumbers. For now.", "已死之神正在沉睡。起码现在是这样。", "_t")
t("Tentacle Spawn", "衍生触手", "talent name")
t("@Source@ spawns a tentacle near @target@.", "@Source@在@target@身旁召唤了触手。", "_t")
t("You cannot summon; you are suppressed!", "你不能召唤，你被压制了！", "logPlayer")
t("Not enough space to summon!", "没有足够的空间召唤！", "logPlayer")
t("#ORCHID#%s summons a %s...", "#ORCHID#%s召唤了一个%s……", "logCombat")
t("#ORCHID#%s summons a %s...", "#ORCHID#%s召唤了一个%s……", "saySimple")
t("The Dead God wishes to tickle you...", "已死之神想要逗逗你……", "_t")
t("Curse of Amakthel", "阿马克泰尔的诅咒", "talent name")
t([[Create a circle of cursed ground (radius %d) for %d turns. Any foes inside will be cursed, all new negative effects on them will have their duration doubled.
		]], [[创造一片诅咒之地（半径 %d 码）%d 回合。任何陷入其中的敌人都会被诅咒，任何他们新得到的负面状态的持续时间都会翻倍。
		]], "tformat")
t("Temporal Ripples", "时空涟漪", "talent name")
t([[Creates a circle of radius %d of altered time for %d turns. Any damage your foes take while standing in it will heal the attacker for 200%% of the damage dealt.
		]], [[创造一片半径 %d 码的时间错乱之地 %d 回合。任何站在其中的敌人受到的伤害都会治疗攻击者 200%% 伤害数额的生命。
		]], "tformat")
t("Saw Storm", "锯刃风暴", "talent name")
t([[Summon a storm of swirling sawblades to slice your foes, inflicting %d physical damage and bleeding to anyone who approaches for %d turns.
		The damage and duration will increase with your Mindpower.]], [[召唤由旋转锯刃组成的风暴撕裂敌人，对所有靠近者造成 %d 点物理伤害并使其流血。风暴持续 %d 回合。
		伤害和持续时间随精神强度提高。]], "tformat")
t("Razor Saw", "剃刀飞锯", "talent name")
t([[Launches a sawblade with intense power doing %0.2f physical damage to all targets in line.
		The damage will increase with Mindpower]], [[发射一个动能十足的锯刃，对一条线内的所有目标造成 %0.2f 物理伤害。
		伤害会随着你的精神强度增长。]], "tformat")
t("Rocket Dash", "火箭突进", "talent name")
t("@Source@ rockets forward!", "@Source@使用火箭突进向前！", "_t")
t([[Dash forward using rockets.
		If the spot is reached and occupied, you will perform a free melee attack against the target there.
		This attack does 130% weapon damage.
		You must dash from at least 2 tiles away.]], [[使用火箭向前突进。
		如果目标地点已被占据，那么你对那里的目标进行一次近战攻击。
		攻击会造成 130% 武器伤害。
		你必须至少突进 2 码。]], "_t")
t("Mind Controlled Yeti", "精神控制的雪人", "talent name")

------------------------------------------------

section "tome-orcs/data/talents/misc/races.lua"

t("race", "种族技能", "talent category")
t("yeti", "雪人", "talent type")
t("The various racial bonuses a character can have.", "角色可能拥有的各种种族加成。", "_t")
t("Algid Rage", "寒冰之怒", "talent name")
t([[Your yeti is attuned to the cold climates.
		For 5 turns all damage you deal has %d%% chance to encase the target in an iceblock for 3 turns.
		While Algid Rage is up you easily pierce through iceblocks, reducing the damage they absorb by 50%%.
		The bonus will increase with your Willpower.]], [[你的雪人早已适应寒冷的环境。
		在 5 回合中你造成的所有伤害都有 %d%% 几率把目标冻在冰块中 3 回合。
		在寒冰之怒生效中你可以轻松地穿透冰块，减少 50%% 他们所吸收的伤害。
		数值会随着你的意志提升。]], "tformat")
t("Thick Fur", "厚实毛皮", "talent name")
t("Your yeti's fur acts like a shield, providing %d%% cold resistance, %d%% physical resistance and %d magical save.", "你厚实的雪人毛皮能像盾牌一样保护你，为你提供 %d%% 寒冷抗性，%d%% 物理抗性和 %d 魔法豁免。", "tformat")
t("Resilient Body", "坚韧身躯", "talent name")
t([[Your yeti's body is very resilient to detrimental effects.
		Each time you are hit by a physical, magical, or mental detrimental effect your body reacts with a burst of healing.
		This effect heals for %d and can only occur up to 3 times per turn.
		It increases with your Constitution stat.]], [[你的雪人身躯面对负面状态十分坚韧。
		每当你被一个负面的物理，魔法或精神状态击中时，你的身体会反射性地触发恢复之力。
		这个效果会治疗你 %d 生命值，且每回合最多触发 3 次。
		治疗值会受体质值加成。]], "tformat")
t("Mindwave", "脑波冲击", "talent name")
t([[You willingly fry a few parts of your yeti's brain to trigger a huge psionic blast in cone of radius %d.
		Any foes caught in the blast will suffer %0.2f mind damage and be confused (35%% power) for %d turns.
		The damage will increase with your Constitution and the apply power will be the highest of your mind, spell, or physical power.]], [[你主动烧灼雪人大脑的一小部分，向半径 %d 的锥形范围释放强大的灵能冲击。
		冲击范围内的所有敌人受到 %0.2f 点精神伤害，并陷入混乱（35%% 强度）%d 回合。
		伤害随体质提高；效果强度取你的精神强度、法术强度或物理强度中的最高值。]], "tformat")
t("whitehooves", "白蹄", "talent type")
t("Whitehooves", "白蹄", "talent name")
t([[Improves your undead body, increasing Strength and Magic by %d.
		Each time you move you gain a charge (up to %d) of death momentum, increasing your movement speed by 20%%.
		Each turn spent not moving you lose a charge.]], [[强化你的死灵身躯，增加 %d 的力量和魔力。
		每次移动时获得 1 层死亡动量（最多 %d 层），使移动速度提高 20%%。
		每个未移动的回合会失去 1 层死亡动量。]], "tformat")
t("Dead Hide", "亡者之皮", "talent name")
t("Your undead skin hardens under stress. Each charge of death momentum also increases all flat damage resistance by %d.", "你的死灵皮肤在重压之下会变得更加坚硬。每层死亡动量都会使所有固定伤害减免提高 %d。", "tformat")
t("Lifeless Rush", "无生突袭", "talent name")
t([[You summon your undead energies to instantly build up death momentum to its maximum possible charges.
		The effect will only start to decrease after %d turns.
		In addition, the death momentum effect also grants +%d%% to all damage per charge.]], [[你唤起死灵之力，瞬间将死亡动量叠加至最大层数。
		死亡动量只会在 %d 回合后开始衰减。
		此外，每层死亡动量还会使所有伤害提高 +%d%%。]], "tformat")
t("Essence Drain", "吸取精华", "talent name")
t([[You send a wave of darkness at your foe, dealing %0.2f darkness damage.
		The darkness will drain a part of its life essence (only works on living targets) to increase the duration before the next charge of death momentum is used by %d.
		Only usable when you have the death momentum effect.
		The damage scales with your Magic stat.]], [[你向敌人释放一波黑暗能量，造成 %0.2f 暗影伤害。
		黑暗会吸取目标的一部分生命精华（只对活物有效），使下一层死亡动量被消耗前的持续时间延长 %d 回合。
		只能在你拥有死亡动量效果时使用。
		伤害随魔力提高。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/psionic/action-at-a-distance.lua"

t("Condensate", "冷凝", "talent name")
t([[Condensate hot steam around your foes in radius %d, burning them for %0.2f fire damage and applying the wet effect for 4 turns, halving their stun resistances.
		The damage will increase with your Mindpower.]], [[在半径 %d 内的敌人周围凝聚炽热蒸汽，造成 %0.2f 点火焰伤害并施加 4 回合的浸湿效果，使其震慑抗性减半。
		伤害随精神强度提高。]], "tformat")
t("Solidify Air", "固化空气", "talent name")
t("solid air", "固化空气", "_t")
t("a piece of solidified air", "一块固化的空气", "_t")
t([[You concentrate your will in a cone in front of you, condensing the air into a tangible, solid form.
		Any creatures caught inside take %0.2f physical damage.
		Any places with no creatures will be filled with solid air, blocking the way for %d turns.
		The damage will increase with your Mindpower.]], [[你集中精神力把你前方的锥形空间内的空气凝聚成固态。
		任何陷入其中的生物都会受到 %0.2f 的物理伤害。
		任何没被生物占据的地方会被固化空气占满，阻路 %d 回合。
		伤害受精神强度加成。]], "tformat")
t("Superconduction", "超导", "talent name")
t([[Call a streak of lightning on your target, dealing %0.2f to %0.2f lightning damage.
		If it is wet the lightning propagates to all foes in radius %d, doing the same damage to each.
		All affected foes are seared for 4 turns, reducing their fire resistance by %d%% and and mind save by %d.
		The damage will increase with your Mindpower.]], [[召唤一道闪电劈向你的目标，造成 %0.2f 到 %0.2f 闪电伤害。
		如果目标被浸湿了，那么闪电扩散，对半径 %d 码内的所有单位造成同样的伤害。
		所有被劈中的单位都会被烧焦 4 回合，降低他们的火焰抗性 %d%% 和精神豁免 %d。
		伤害受精神强度加成。]], "tformat")
t("Negative Biofeedback", "负反馈", "talent name")
t([[Any time you deal damage with a psionic ability you incur a negative biofeedback in your foes, stacking up to %d times for 5 turns.
		Each stack reduces their physical save by %d, defense and armour by %d.
		This effect may only occur once per turn.]], [[每当你使用精神技能造成伤害时，你对你的敌人施加一个负反馈，能叠加至 %d 层并持续 5 回合。
		每层都会降低他们 %d 的物理豁免和 %d 的防御与护甲。
		这个效果每回合只能触发一次。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/psionic/gestalt.lua"

t("Gestalt", "格式塔", "talent name")
t([[You let your mind tap into your steam generators for energy, increasing your Mindpower in proportion to your steam level: %d when at full steam and 0 when at 0 steam.
		Using a psionic talent will feedback into your generators, increasing your Steam power by %d for your next steamtech talent.
		Using a steamtech talent will feedback into psionic focus, increasing your psi level by %d.
		The effects increase with your Willpower.]], [[你让心灵从蒸汽发动机中汲取能量，按照当前蒸汽值的比例提高精神强度：蒸汽全满时提高 %d 点，蒸汽为 0 时不提高。
		使用灵能技能会向发动机反馈，为你的下一个蒸汽科技技能提高 %d 点蒸汽强度。
		使用蒸汽科技技能会向灵能焦点反馈，使你的灵能值提高 %d 点。
		效果随意志提高。]], "tformat")
t("Improved Gestalt", "强化格式塔", "talent name")
t([[When you use a steamtech talent while Gestalt is active you drain some residual power to form a psionic shield.
		The shield forms for 3 turns and absorbs %d damage.
		The effects increase with your Mindpower.]], [[每当你在格式塔激活状态中使用蒸汽技能时，你会吸取一些残留的力量来形成一个精神护盾。
		这个护盾持续 3 回合，并能吸收 %d 伤害。
		效果受精神强度加成。]], "tformat")
t("Instant Channeling", "瞬间引导", "talent name")
t("You must have either a psionic damage shield active or Improved Gestalt available to use this talent.", "你必须在格式塔处于激活状态，并且有一个精神护盾或强化格式塔不在冷却中时，才能使用这一技能。", "logPlayer")
t([[Instantly channel all of your remaining steam to replenish your psi energies and either enhance your active psionic damage shield or trigger a new one.
		The (new or existing) shield duration is increased by 3 turns and its power is boosted by %d%% of the steam used.
		You restore psi equal to %d%% of the steam used.
		This talent requires Gestalt to be active and either an active psionic damage shield or Improved Gestalt off cooldown.]], [[瞬间引导你剩余的所有蒸汽来补充你的灵能并充能或制造一个新的精神护盾。
		护盾的持续时间会增加 3 回合，并能多吸收 %d%% 消耗的蒸汽数额的伤害。
		你回复等同于 %d%% 所消耗的蒸汽数额的灵能。
		此技能需要格式塔处于激活状态，并且有一个精神护盾或强化格式塔不在冷却中。]], "tformat")
t("Forced Gestalt", "强制格式塔", "talent name")
t([[Temporarily expand your mind to force your Gestalt upon your foes in a radius of 5. Up to %d foe(s) will be affected.
		The Gestalt will drain each affected foe's powers (physical power, mind power, spell power and steam power) by %d for 5 turns.
		Your own powers will be increased in return by the drained amount (reduced for each additional foe).
		In addition for 5 turns you can sense creatures beyond your sight, even through walls in radius %d.
		The effects improve with your Mindpower.]], [[暂时延伸你的心灵以使你的格式塔笼罩你周围半径 5 码内的敌人，最多可影响 %d 个敌人。
		格式塔会吸收每个被影响敌人的力量（物理强度，精神强度，法术强度，蒸汽强度）%d 点，持续 5 回合。
		你自身的力量会增加所吸取的数额（每多吸收一个额外的敌人，效果都会衰减）。
		除此之外，在 5 回合内你可以超脱视线的感知半径 %d 码内的生物。
		效果受精神强度加成。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/spells/occult-technomancy.lua"

t("Metaphasic Spin", "相位旋转", "talent name")
t("You need an arcane dynamo to cast this spell.", "你需要奥术发电机才能释放这一法术。", "logPlayer")
t("Select the steamsaw to use?", "使用哪把蒸汽链锯？", "_t")
t([[You imbue a steamsaw with arcane and temporal forces, making it spin very fast around your waist (ignoring requirements).
		The saw spins so fast it it disturbs spacetime around you, increasing your spellpower by up to %d, your spell critical chance by up to %d and your mana regen by up to %0.1f (depending on steamsaw tier).
		Any successful melee attack against you also triggers an automatic steamsaw attack that cannot miss dealing %d%% weapon damage as occult damage (arcane and temporal).
		The steamsaw used will provide its bonus as if it was worn, but you can not Block with it.
		Increases steamsaws weapon damage by %d%% and uses Magic instead of Strength to determine their damage.
		If using Aether Avatar, all Occult Technomancy spells become usable for its duration and all occult damage becomes pure arcane.

		#{italic}#When you first learn this talent you also learn the Steamsaw tinker creation if you didn't already know it.#{normal}#
		]], [[你把奥术和时空能量注入一把蒸汽链锯，让它绕着你的腰飞速旋转（无视装备需求）。
		这把链锯旋转的速度是那么快，它扰乱了你周围的时空。最多增加你 %d 的法术强度，%d 的法术暴击率，和 %0.1f 的法力值恢复（基于蒸汽链锯的材质等级）
		任何对你的成功的近战攻击都会触发一次必定命中的自动的蒸汽链锯反击，造成 %d%% 玄机（奥术和时空）武器伤害。
		使用这种方法装备的蒸汽链锯会提供装备它所提供的属性加成，但你不能使用它来格挡。
		增加蒸汽链锯的武器伤害 %d%%，并在使用蒸汽链锯时用魔力值代替力量值计算伤害。
		如果你激活了以太之体，所有科技法术：玄机系的技能都可以在其持续期间使用，并且所有玄机伤害都会转化为纯净的奥术伤害。

		#{italic}#当你第一次学会这一技能的时候，如果你还没有掌握蒸汽链锯的配方，你还会同时学会这一配方。#{normal}#
		]], "tformat")
t("Reality Breach", "现实切裂", "talent name")
t("You need to activate Metatemporal Spinner to cast this spell.", "你需要开启相位旋转才能释放这一法术。", "logPlayer")
t("#Source# annihilates '#Target#'!", "#Source#毁灭了'#Target#'！", "logCombat")
t([[Spin your saw at incredible speeds for an instant, fully breaking reality in a 3-wide beam in front of you.
		Any creatures caught by the beam take %0.2f occult damage and are untethered from reality, reducing their global speed by %d%% and the speed of any projectiles they fire by %d%% for 4 turns.
		At level 3 any projectiles caught in the beam are instantly annihilated.
		At level 5 the beam is so strong that all creatures caught inside are knocked back 3 tiles.
		The breach is so deep that the beam will always have the maximum possible length it can.
		The damage will increase with your Spellpower.]], [[让你的链锯以难以置信的速度飞速旋转，撕裂周围的现实，在你面前产生一条宽度为 3 的射线。
		所有被射线击中的生物将会受到 %0.2f 玄机伤害，并且进入脱离现实的状态。它们的整体速度降低 %d%%，发射的一切抛射物也会被减速 %d%%，持续 4 回合。
		技能等级 3 时，射线范围内的所有抛射物也会被立刻摧毁。
		技能等级 5 时，这一射线的力量是如此强大，所有被击中的生物都会被击退 3 码。
		这道裂隙是如此之深，射线总会延伸至其可能达到的最大长度。
		伤害受法术强度加成。]], "tformat")
t("Ethereal Steam", "虚幻蒸汽", "talent name")
t([[You reach out through the aether to all creatures in sight that were slowed by Reality Breach or Congeal Time.
		For each target you create a link of arcane infused steam to it that lasts %d turns.
		Any time the target uses a talent one of your cooling down spells is reduced by 1 (prioritizing Technomancy spells).
		Each turn the link is up the target and any creature inside the link takes %0.2f occult damage.
		As long as at least one link is up, the cooldown of your Metaphasic Spin spell is set to 6 turns instead of 30.
		The damage will increase with your Spellpower.]], [[你通过以太触及视野内所有被现实切裂或时间凝固减速的生物。
		你会为每个目标建立一条注入奥术能量的蒸汽链接，持续 %d 回合。
		每当目标使用技能时，你一个正在冷却的法术便会减少 1 回合冷却时间（优先选择科技法术）。
		链接存在期间，每回合目标和链接线上的所有生物都会受到 %0.2f 玄机伤害。
		只要至少有一条链接存在，相位旋转的冷却时间就会设为 6 回合，而非 30 回合。
		伤害随法术强度提高。]], "tformat")
t("Metaphasic Echoes", "相位回响", "talent name")
t("You can only cast this spell on the turn after Reality Breach.", "你只能在施放现实切裂后的下一回合施放此法术。", "logPlayer")
t([[Using your sheer arcane power you keep breaches in spacetime open for %d turns.
		Each turn they are open you project an occult clone of your saw along each breach, damaging any creature caught for %d%% occult weapon damage.
		The saw cuts both in a physical and arcane way, reducing the duration of a random beneficial effect on each target by %d each time.
		Each target can only be affected once per turn.
		This spell is only usable for one turn after casting Reality Breach but any Reality Breach cast during its duration is also recorded inside.]], [[你调动强大的奥术力量，在时空中切开的裂缝会保持开放，持续 %d 回合。
		在这一裂缝打开的每一回合里，从裂缝中会投射一个你链锯的玄机克隆，对所有击中的生物造成 %d%% 玄机武器伤害。
		这一链锯会在物理和奥术的意义上切裂敌人，每次击中会降低目标身上一个随机增益效果的持续时间 %d 回合。
		每个目标每回合只会被这一效果影响一次。
		此法术只能在施放现实切裂后的下一回合使用，但它持续期间施放的任何现实切裂也会被记录其中。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/artillery.lua"

t("Rocket Pod", "火箭发射器", "talent name")
t([[You equip an automated, shoulder mounted rocket launcher. Each turn it will launch rockets at up to %d enemies in weapon range, dealing %d%% steamgun damage as fire.
		The rockets will pass harmlessly through allies, but on-hit effects triggered by them only deal 50%% of their usual damage.]], [[你装备一具自动肩扛式火箭发射器。每回合，它会向武器射程内最多 %d 个敌人发射火箭，造成相当于蒸汽枪伤害 %d%% 的火焰伤害。
		火箭会无害地穿过盟友，但它们触发的命中效果只造成通常伤害的 50%%。]], "tformat")
t("Incendiary Powder", "燃烧粉末", "talent name")
t([[Augment your rockets with highly flammable materials, causing them to burn targets for %0.2f fire damage over 3 turns. Subsequent shots against burning targets refresh the effect of the duration (but do not stack) and inflict %0.2f additional fire damage.
Targets affected by this burning that fall below 25%% life enter a state of panic, giving them a %d%% chance each turn to flee in terror from you.
The fire damage will increase with your Steampower.]], [[用高度易燃的物质强化你的火箭，让它们可以引燃目标，在 3 回合内造成 %0.2f 火焰伤害。继续击中被引燃的目标会刷新效果的持续时间（但不能叠加），并造成 %0.2f 额外火焰伤害。
被这一燃烧效果影响的目标若生命值降低到 25%% 以下，将会陷入恐慌的状态，他们每回合有 %d%% 的几率在恐慌中逃离你。
火焰伤害受蒸汽强度加成。]], "tformat")
t("Lock On", "目标锁定", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t([[Lock on to your target with your rocket pod for 5 turns.
While locked on your regular rocket pod attacks are disabled. However, each turn you automatically fire a rocket barrage dealing %d%% increased damage at your target.
Marked targets also lose %d defense and cannot benefit from concealment or evasion.
The defense loss will increase with your Steampower.]], [[让你的火箭发射器锁定目标 5 回合。
当你锁定目标的时候，自动火箭发射将会被暂停。然而，每回合你会朝目标发射火箭弹幕，造成额外 %d%% 的伤害。
被标记的目标还会失去 %d 点闪避，且无法从隐蔽或躲闪中受益。
闪避降低值随蒸汽强度提高。]], "tformat")
t("Death From Above", "死亡天降", "talent name")
t([[You use your rocket pods to launch yourself into the air for 3 turns, firing a radius 2 barrage of rockets that deal %d%% steamgun damage as fire in radius 2. 
		While flying you gain %d%% movement speed, %d%% chance to evade melee and ranged attacks, and can reactivate this talent at will to repeat the rocket barrage.
		Using any talent other than Rocket Barrage will end this effect immediately.]], [[你启动火箭发射器，将自己发射到天空中，持续 3 回合，同时发射范围为 2 的火箭弹幕，在 2 码半径内造成 %d%% 火焰蒸汽枪伤害。
		当处在飞行状态的时候，你获得 %d%% 移动速度，%d%% 几率躲闪近战和远程攻击，并且可以重新激活这个技能，再次发射火箭弹幕。使用任何火箭弹幕之外的技能都会提前终止这一效果。]], "tformat")
t("Rocket Barrage", "火箭弹幕", "talent name")
t("Fires a barrage of rockets in radius 2, dealing %d%% steamgun damage as fire.", "发射火箭弹幕，在 2 码半径内造成 %d%% 火焰蒸汽枪伤害。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/automated-butchery.lua"

t("Continuous Butchery", "无尽屠戮", "talent name")
t("You require a steamsaw for this talent.", "你需要一把蒸汽链锯才能使用这一技能。", "logPlayer")
t([[You attune your saws to a specific target for 5 turns.
		Each time you strike this target all damage done with steamsaws (including by other talents) is increased by +%d%%.
		If you strike any other foe the bonus ends.
		#{italic}#Metal your foes to death!#{normal}#]], [[将链锯调校至一个指定目标，持续 5 回合。
		每次用链锯命中该目标时，链锯造成的所有伤害（包括其他技能）提高 %d%%。
		若你命中任何其他敌人，加成效果结束。
		#{italic}#切碎他们！！#{normal}#]], "tformat")
t("Explosive Saw", "爆炸飞锯", "talent name")
t([[You send a saw mounted on an automated steam propulsor to assault a foe, dealing %0.2f physical damage each turn for 4 turns and silencing it.
		At the end of the duration, the saw explodes for %0.2f fire damage and flies back, pulling the target up to %d tiles towards you.
		The damage will increase with your Steampower.]], [[你用自动蒸汽弹射器向敌人发射一把链锯，造成 %0.2f 物理伤害并沉默敌人，持续 4 回合。
		持续时间结束后，链锯爆炸，造成 %0.2f 的火焰伤害并飞回，将目标向你的位置拉扯 %d 格。
		伤害受蒸汽强度加成。]], "tformat")
t("Mow Down", "肢解", "talent name")
t([[When you kill a foe with a melee strike you quickly throw some of their remains in your steam engine, instantly regenerating %d steam.
		When you deal a critical melee strike you also have a %d%% chance to cut a part of your foe and use it in your steam engine.
		When either of those happens this strikes fear in all foes in radius 4 of the victim, brainlocking them for %d turns.
		#{italic}#To the meat grinder!#{normal}#]], [[当你用近战攻击杀死敌人时，会迅速将其部分残骸扔进蒸汽引擎，立即恢复 %d 点蒸汽。
		当你的近战攻击造成暴击时，也有 %d%% 几率切下敌人的部分躯体并扔进蒸汽引擎。
		任一情况发生时，受害者半径 4 格内的所有敌人都会陷入恐惧，并被思维封锁 %d 回合。
		#{italic}#变成肉酱吧！！#{normal}#]], "tformat")
t("Tech Overload", "系统过载", "talent name")
t([[You override all security measures of your tinkers, allowing you to reset the cooldown of %d of most of your steamtech talents of tier %d or less and instantly increases your steam level by %d%% of the maximum.
		In addition for 6 turns your maximum steam capacity is doubled, but steam regeneration is halved.
		#{italic}#Master of Tech, Master of Death!#{normal}#]], [[你开启全部插件的超频模式，重置最多 %d 个蒸汽科技技能（%d 层级或以下）的冷却时间，直接恢复 %d%% 蒸汽值。
		在 6 回合内，蒸汽值最大值翻倍，但是恢复值减半。
		#{italic}#科技至尊、死亡之主！！#{normal}#]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/avoidance.lua"

t("Automated Cloak Tessellation", "披风护甲", "talent name")
t("@Source@ tessellates @hisher@ cloak!", "@Source@在@hisher@披风上布满金属！", "_t")
t("You require a cloak to use this talent.", "你需要有披风才能使用这一技能。", "logPlayer")
t([[You tessellate your cloak with small pieces of metal, providing %d damage reduction against all attacks.
		The myriad metal scraps also help against incoming projectiles, providing a %d%% chance of deflecting them to a nearby spot.]], [[在披风上布满小块金属，对所有攻击提供 %d 的伤害减免。
	大量的金属碎片同时对远程打击提供偏移抵抗，有 %d%% 的概率将投射物反射至附近的其他位置。]], "tformat")
t("Cloak Gesture", "披风花招", "talent name")
t("@Source@ weaves @hisher@ cloak!", "@Source@挥舞@hisher@披风！", "_t")
t([[With a gesture of your cloak, you drop a small incendiary device in front of you, creating a wall of thick steam of %d length that burns creatures passing it for %0.2f fire damage and blocks sight for 5 turns.
		At level 5 the action is so perfect that your foes even lose track of you entirely.
		Damage increases with your steampower.]], [[在抖动披风的同时，在面前扔下一个小型的爆燃设备，产生一堵长度为 %d 的浓密蒸汽墙。对穿越的生物造成 %0.2f 的火焰伤害，并且阻挡生物视线。效果持续 5 回合。
	技能等级 5 时，敌人会完全丧失你的行踪，仇恨丢失。
	伤害受蒸汽强度加成。]], "tformat")
t("Embedded Restoration Systems", "嵌入式回复系统", "talent name")
t("#LIGHT_BLUE#%s's embedded restoration system activate.", "#LIGHT_BLUE#%s的内置恢复系统启动了。", "logSeen")
t("%s activates %s cloak's restoration systems!", "%s激活了%s披风的恢复系统！", "logSeen")
t("%s deactivates %s cloak's restoration systems.", "%s关闭了%s披风的恢复系统。", "logSeen")
t([[Your cloak is lined with an automated health system that activate when no enemies are visible.
		When it triggers, you will be healed for %d life.
		At talent level 3, it will also remove one detrimental physical effect.
		The system can only trigger once every %d turns.]], [[为披风加装嵌入式回复系统，周围没有可见敌人时自动触发，回复 %d 生命值。
	技能等级 3 时，同时会消除一个物理负面效果。
	该系统每 %d 回合自动触发一次。]], "tformat")
t("Cloaking Device", "隐形装置", "talent name")
t([[Trigger an array of small mirrors to appear all over your cloak.
		The mirrors are positioned to reflect all light shining on you, granting %d stealth power for 10 turns.
		Stealth power increases with your steampower.]], [[在披风上布满细小的反射镜阵列，反射照射到你身上的所有光线，让你直接潜形。
		获得 %d 潜行强度，持续 10 回合。
		潜行强度受蒸汽强度加成。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/battlefield-management.lua"

t("Saw Wheels", "链锯轮滑", "talent name")
t("You require a steamsaw for this talent.", "你需要一把蒸汽链锯才能使用这一技能。", "logPlayer")
t([[Firmly plant your steamsaws in the ground, using them to propel yourself very quickly (+%d%% movement speed).
		Any foes on either side of your movement get wrecked by the saws, knocking them 3 tiles away from you.
		Attacking or using any talent will break this effect.
		When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage to all foes around you. To do full damage you need to have moved at least 5 times, otherwise damage is lower (or null for no movement).
		#{italic}#The wheels of death! Amazing!#{normal}#]], [[把链锯深深插入地面，作为履带，增强自己的行动能力（移动速度增加 %d%%）。
		在你移动路线两侧的敌人被链锯割断，被击退 3 码。
		攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成 %d%% 武器伤害。你需要至少移动五次来达到最高伤害，否则伤害会降低。若不移动则没有伤害。
		#{italic}#冲锋！死亡之轮！！#{normal}#]], "tformat")
t("Grinding Shield", "利齿护盾", "talent name")
t([[Spin your saws wildly around you to create a wall of steamy sawteeth.
		All melee damage against you is reduced by %d%%, you have %d%% chance to evade projectiles and you can never take a blow that deals more than %d%% of your max life.
		#{italic}#Split their bones on the saws of death!#{normal}#]], [[围绕自身快速旋转链锯，形成一堵链锯齿形成的墙壁。
		所有近战伤害降低 %d%%，有 %d%% 的概率回避投射物，并且受到的一击伤害不会超过最大生命值的 %d%%。
		#{italic}#用死亡链锯拆了他们的骨头！！#{normal}#]], "tformat")
t("Punishment", "惩戒", "talent name")
t("#CRIMSON#%s unleashes a punishing strike for %d%% bonus damage!", "#CRIMSON#%s释放一次惩罚打击，造成%d%%额外伤害！", "logSeen")
t([[Slam your saws into your target, dealing 100%% weapon damage + %d%% per physical, magical, or mental effect on them (up to 7 effects).
			Sustains are not effects.
		#{italic}#The Metal Punisher!#{normal}#]], [[用链锯猛力拍击目标，造成 100%% + 每个物理、魔法或者精神状态 %d%% 加成的伤害（最多 7 个）。
		持续技能不视作状态。
		#{italic}# 钢铁惩戒！！#{normal}#]], "tformat")
t("Battlefield Veteran", "战场老兵", "talent name")
t([[You have lived through many battles, and your experience makes you a gritty veteran.
		Saw Wheels end of effect attack increased by %d%%.
		Grinding Shield lets you live below your normal limits, up to -%d life.
		Punishment has a %d%% chance to have its cooldown reduced by 1 for each effect.
		#{italic}#Domination for all!#{normal}#]], [[你是一名坚毅的老兵，经历了大量战争仍然能够幸存，有着丰富的战斗经验。
		链锯轮滑效果结束时的攻击伤害提高 %d%%。
		利齿护盾让你超越生存下限，在 -%d 的生命下仍然生存。
		惩戒有 %d%% 的几率：目标每具备一个效果，惩戒的冷却时间就减少 1 回合。
		#{italic}#一切尽在掌控！！#{normal}#]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/blacksmith.lua"

t("Massive Physique", "强壮体魄", "talent name")
t([[Working iron has honed your body into an amazing shape, granting %d strength and constitution.
		At talent level 5, you are so incredibly built that you gain one size category.]], [[长期打铁，让你的身体格外强壮，增加 %d 力量和体质。
		技能等级 5 时，你的肌肉是如此巨大，体型增大一个等级。]], "tformat")
t("Endless Endurance", "永不疲倦", "talent name")
t([[Working long hours at a forge has made you incredibly slow to tire and given you endless vitality.
		Your healing factor is increased by %d%% and your life regeneration by %0.2f.
		Stopping you is nearly impossible; your pinning resistance is increased by %d%%.]], [[长时间的锻造工作让你拥有不可思议的持久力和无尽的活力。
		你的治疗系数增加 %d%%，生命恢复增加 %0.2f。
		你力大无穷，很难被阻止，定身抗性增加 %d%%。]], "tformat")
t("Life in the Flames", "浴火而生", "talent name")
t([[Slaving for many years at the forge has made you more resilient to physical pain and fire burns.
		Your fire resistance is increased by %d%% and your physical resistance by %d%%.
		At talent level 5, you are so accustomed to the flames that you become immune to the fireburn effect.]], [[长时间的锻造工作让你对疼痛和火焰的忍耐力提高。
		火焰抗性增加 %d%%，物理抗性增加 %d%%。
		技能等级 5 时，你对火焰抗性极高，从而免疫燃烧状态。]], "tformat")
t("Craftsman's Eye", "匠师之眼", "talent name")
t([[You can easily see the weak points in your enemy's defenses. After all, you know to look for the same flaws in your own work.
		This grants %d armour penetration and %d%% critical strike multiplier.
		At talent level 5, you can also fight stealthed and invisible creatures without penalty.]], [[你能够像找到自己工作的错误一样轻易发现敌人防御的弱点。
		获得 %d 的护甲穿透和 %d%% 的暴击伤害加成。
		技能等级 5 时，能够自如的与潜行和隐形生物战斗，无视减免。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/butchery.lua"

t("Steamsaw Mastery", "链锯掌握", "talent name")
t("Increases weapon damage by %d%% and Physical Power by 30 when using steamsaws.", "使用链锯时，提高 %d%% 武器伤害和 30 物理强度。", "tformat")
t("Overheat Saws", "过热链锯", "talent name")
t("You require two steamsaws for this talent.", "你需要两把蒸汽链锯才能使用这一技能。", "logPlayer")
t([[Channel hot steam around your saws, burning foes you strike in melee for %0.2f fire damage over 3 turns (which can stack)!
		#{italic}#Hot, steamy maiming!#{normal}#]], [[用蒸汽包裹链锯，对近战攻击命中的目标在 3 回合内造成 %0.2f 点火焰伤害（可以叠加）。
		#{italic}#滚烫的蒸汽，死吧！#{normal}#]], "tformat")
t("Tempest of Metal", "金属狂怒", "talent name")
t([[Continuously swing your steamsaws around you, dealing %d%% weapon damage to adjacent foes each time you attack.
		Your chaotic motions make it difficult for anything to hit you, granting %d%% chance to completely negate all damage.
		Damage avoidance chance increases with Steampower.
		#{italic}#Make the metal talk!#{normal}#]], [[持续挥舞你的链锯，每次你攻击时对周围敌人造成 %d%% 武器伤害。
		你狂乱的动作使你很难被命中，%d%% 几率无视伤害。
		伤害无效概率随蒸汽强度提高。
		#{italic}#感受金属之怒吧！！#{normal}#]], "tformat")
t("Overcharge Saws", "链锯过载", "talent name")
t([[You temporarily overcharge the saw motors, increasing the effective talent level of all saw talents by %d%% for %d turns.
		#{italic}#The pain shall never stop!#{normal}#]], [[链锯引擎临时进入过载模式，增加 %d%% 的链锯相关技能有效等级，持续 %d 回合。
		#{italic}#无尽地痛苦#{normal}#]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/chemical-warfare.lua"

t("Miasma Engine", "瘴气引擎", "talent name")
t([[You repurpose your steam engine to emit a cloud of toxic, corrosive chemicals around you.
		Each time you use a non-instant steamtech talent, you create a radius 3 cloud of miasma for 5 turns. All enemies within the miasma have %d%% reduced healing and %d%% chance to fail talent usage.
		Each time miasma is reapplied the failure chance increases, up to %d%% after 5 reapplications.
		The first time each turn a target affected by miasma is hit by a melee or ranged attack the miasma seeps into their wounds, dealing an additional %0.2f acid damage.
		Miasma duration does not increase on re-apply.
		When a creature survives the miasma it becomes immune to it for 9 turns.]], [[你使用你的蒸汽机，在你的周围产生一股有毒且有腐蚀性的化学物质形成的云雾。
		每当你使用一个非瞬发的蒸汽科技技能的时候，你会在周围产生半径为 3 码的瘴气，持续 5 回合。所有被包裹入瘴气的敌人治疗效果减少 %d%%，且会有 %d%% 的几率使用技能失败。
		瘴气效果叠加的时候，这一技能使用失败的几率也会上升，最多叠加五次，达到 %d%%。
		当被瘴气影响的目标每回合第一次被近战或远程攻击击中的时候，瘴气会渗入他们的伤口，造成 %0.2f 额外的酸性伤害。
		瘴气效果叠加的时候，持续时间不会叠加。
		当一个生物在瘴气效果中存活下来后，它会免疫瘴气效果 9 回合。]], "tformat")
t("Caustic Dispersal", "腐蚀扩散", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t("You fire a toxic shell that explodes in radius %d, dealing %d%% weapon damage as acid and leaving behind a cloud of miasma for %d turns that inherits all effects from your Miasma Engine.", "你发射一枚毒气弹，在半径 %d 码范围内爆炸，造成 %d%% 酸性武器伤害，并留下一团瘴气，持续 %d 回合。瘴气效果继承你瘴气引擎技能的一切效果。", "tformat")
t("Smogscreen", "蔽目毒云", "talent name")
t("You become difficult to target through the thick smog generated by your Miasma Engine. While surrounded by miasma you have a %d%% chance to entirely avoid damage, increased by %d%% per stack.", "在瘴气引擎产生的浓雾中，敌人更难锁定你。被瘴气包围时，你有 %d%% 几率完全避免伤害；每层瘴气使该几率提高 %d%%。", "tformat")
t("Fumigate", "毒气熏杀", "talent name")
t("You require a steamgun and an active miasma cloud for this talent.", "你需要一把蒸汽枪和一个活跃的瘴气云雾才能使用这一技能。", "logPlayer")
t([[You consume all Miasma Engine stacks you have to fire a blast of corrosive death through your steamgun, dealing %d%% weapon damage as acid in a radius %d cone with a %d%% chance to remove a random beneficial physical or mental effect. For every stack beyond the first the damage dealt is increased by 50%% and there is a %d%% chance to remove an additional effect.
		This attack ignores all enemy armour, and you must have at least 1 stack of Miasma Engine to use this talent.]], [[你消耗所有瘴气引擎的叠加效果，并用你的蒸汽枪发射出毁灭性的腐蚀爆炸，在 %d 码范围的扇形区域内造成 %d%% 酸性武器伤害，并有 %d%% 的几率移除一个随机的有益物理或精神效果。你瘴气引擎叠加的层数每超过一层，则增加 50%% 伤害，并有 %d%% 几率额外移除一个效果。
		这一攻击无视敌人护甲，你至少需要有一层瘴气引擎效果才能使用这个技能。]], "tformat", {2,1,3,4})

------------------------------------------------

section "tome-orcs/data/talents/steam/demolition.lua"

t("Grenade Launcher", "榴弹发射器", "talent name")
t([[You mount a grenade launcher on your steamgun that launches high explosive rounds. Each time you make a basic attack with your steamgun or a heavy weapon, you fire a grenade at the target that explodes for %d%% steamgun damage in radius %d.
		This talent also reinforces the armor of you and your minions to give you immunity to your own grenades.
		You can only fire a single grenade once every 9 turns.]], [[你在蒸汽枪上安装一个发射高爆弹的榴弹发射器。每当你用蒸汽枪进行普通攻击或使用重装武器攻击时，都会向目标发射一枚榴弹，造成 %d%% 蒸汽枪伤害，作用半径 %d 码。
		此技能还会强化你和随从的护甲，使你与随从免疫你自己发射的榴弹。
		每 9 回合只能发射一枚榴弹。]], "tformat")
t("Reactive Armor", "反应式装甲", "talent name")
t([[You line your armor with explosive plating that detonates when struck. On taking a melee or ranged hit that deals more than 8%% of your maximum life a plate detonates, reducing the damage taken by %d%% and triggering a basic grenade attack in a radius %d cone projected at the target dealing %d%% of its usual damage.
		This cannot trigger more than once per turn.
		Blocking an attack with your shield will also trigger the retaliation damage, if it has not already triggered this turn.
		You have up to 3 plates at a time, and regain one every %d turns.]], [[你在你的护甲上嵌入爆炸物装甲层，在被攻击的时候会发生爆炸。在近战或远程攻击对你造成超过最大生命值 8%% 的伤害的时候，装甲层会发生爆炸，降低所受到的伤害 %d%% 并在目标方向 %d 码范围的扇形区域内触发一次手榴弹攻击，造成平常的手榴弹 %d%% 的伤害。
		每回合最多触发一次该效果。
		如果该回合内没有触发过这一效果，使用盾牌格挡攻击也可以触发这样的反击伤害。
		你最多同时能有 3 层护甲层，每 %d 回合会补充一层。]], "tformat")
t("Sapper", "爆破工兵", "talent name")
t([[You load advanced grenades into your launcher.
	Incendiary Grenade: Deals fire damage over 3 turns, increasing damage taken by %d%%.
	Chemical Grenade: Deals acid damage and slows targets by %d%% for 3 turns.
	Shock Grenade: Deals lightning damage and shocks targets for %d turns, reducing stun and pin resistance by 50%%.
	In addition, your turrets now explode when destroyed, dealing %0.2f physical damage to enemies in radius 3.
	You can only choose a single type of grenade at a time.]], [[你往你的发射器内装入高级榴弹。
		燃烧榴弹：在 3 回合内造成火焰伤害，增加所受到的伤害 %d%%。
		化学榴弹：造成酸性伤害，减速目标 %d%%，持续 3 回合。
		震荡榴弹：造成闪电伤害，震撼目标 %d 回合，使目标震慑和定身抗性减少50%%。
		另外，你的炮台被摧毁的时候会引发爆炸，对半径 3 码内的敌人造成 %0.2f 物理伤害。
		你只能同时激活一种榴弹类型。]], "tformat")
t("Barrage", "榴弹轰炸", "talent name")
t("You require a steamgun and an empty grenade launcher for this talent.", "你需要一把蒸汽枪和一个空的榴弹发射器才能使用这一技能。", "logPlayer")
t([[You load a magazine of %d grenades into your launcher, causing your next %d shots to fire a random grenade type in place of your usual Grenade Launcher, dealing 50%% of the usual grenade damage.
		While the magazine is loaded your attack speed is increased by %d%%.
		Your Grenade Launcher talent must be on cooldown to use this talent, and the magazine will only last for 6 turns.]], [[你往发射器中装入一组 %d 发榴弹，让你接下来的 %d 次射击时会从榴弹发射器中发射一枚随机类型的榴弹，造成 50%% 榴弹伤害。
		当你装入榴弹后，你的攻击速度提高 %d%%。
		你的榴弹发射器技能必须处于冷却状态才能使用该技能。装入的榴弹最多持续 6 回合。]], "tformat")
t("Incendiary Grenade", "燃烧榴弹", "talent name")
t("Enhance your grenade with an incendiary agent that burns through armor, dealing fire damage over 3 turns and increasing damage taken while burning by %d%%.", "用高度易燃物质强化榴弹，烧蚀敌人护甲，3回合内造成火焰伤害，在目标燃烧时增加所受到的伤害 %d%%。", "tformat")
t("Chemical Grenade", "化学榴弹", "talent name")
t("Enhance your grenade with incapacitating chemicals that deal acid damage and reduce global speed by %d%% for 3 turns.", "用致残化学物质强化榴弹，造成酸性伤害，降低目标整体速度 %d%%，持续 3 回合。", "tformat")
t("Shock Grenade", "震荡榴弹", "talent name")
t("Enhance your grenade with an electrical charge, causing it to deal lightning damage and shock targets for %d turns, reducing stun and pin resistance by 50%%.", "用电力弹药强化榴弹，造成闪电伤害，震撼敌人 %d 回合，震慑和定身抗性降低50%%。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/elusiveness.lua"

t("Slip Away", "身如游鱼", "talent name")
t([[Using small steam motors to enhance your movements, you are able to slip past up to %d foes in a line.
		After passing the targets, you will quickly run %d tiles away.]], [[用小型喷射引擎强化你的机动性，可以穿过直线上连续的 %d 个敌人。
	穿越后，会急速前进 %d 码。]], "tformat")
t("Agile Gunner", "动若脱兔", "talent name")
t([[The thrill of the hunt invigorates you. For each foe in radius %d around you, you gain 20%% movement speed (up to %d%%).
		Current bonus: %d%%.]], [[被猎杀的危险令你激动不已。
		半径 %d 内每有一个敌人，你获得 20%% 移动速度（最多 %d%%）。
		当前加成：%d%%。]], "tformat")
t("Awesome Toss", "致命翻转", "talent name")
t("You require two steamguns for this talent.", "你需要两把蒸汽枪才能使用这一技能。", "logPlayer")
t([[In an awesome feat of agility and technological prowess, you toss both of your steamguns in the air, causing them to spin madly for 3 turns.
		Each turn, they will fire twice at random targets in range, dealing %d%% weapon damage.
		While the guns are airborne, you are disarmed and cannot attack.
		The spectacle is so distracting that your foes have a hard time concentrating on you, increasing all of your resistances by %d%%.]], [[在惊人的灵巧和科技力量下，你将你的蒸汽枪翻转指向天空，持续旋转 3 回合。
		每回合，蒸汽枪将随机射击 2 次，造成 %d%% 武器伤害。
		效果持续期间，你视为被缴械，不能攻击。
		这场表演如此引人注目，你的敌人都被吸引，使你的伤害抗性增加 %d%%。]], "tformat")
t("Dazzling Jump", "炫目大跳", "talent name")
t("%s seems immune to the powerful kick.", "%s对强力的踢腿免疫。", "logSeen")
t([[While your foes are distracted by your Awesome Toss, you use powerful steam motors to jump into the air and kick a target %d tiles away.
		The impact is so great that it ripples outwards, slowing all creatures in radius 3 by %d%% for 4 turns while the reaction force propels you %d tiles backwards.]], [[当你的敌人被致命翻转吸引时，你启动强力的蒸汽引擎，跳向空中，将目标踢走 %d 码。
		这次攻击冲击力非常大，半径 3 以内所有生物将被减速 %d%%，持续 4 回合。
		反冲力也让你后退 %d 码。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/engineering.lua"

t("Emergency Steam Purge", "紧急蒸汽排出", "talent name")
t([[You open all steam valves at once, releasing a radius %d wave of superheated steam around yourself which deals %0.2f fire damage (but can not be a critical hit).
		If you had at least 35 steam, the vapours will be so hot that they can burn sensory organs, blinding affected creatures for %d turns.
		The effects scale with your current steam value; at 1 steam they are only 15%% as effective as at 50 or more (current factor %d%%).]], [[你打开所有蒸汽阀，释放半径 %d 的蒸汽冲击波，造成 %0.2f 火焰伤害。（这一技能无法暴击）
		若你有至少 35 点蒸汽，气体的温度将变得极高，能烧伤感知器官，令受影响的生物目盲 %d 回合。
		效果受当前蒸汽值加成。1 点蒸汽值时，强度仅为 50 或更高点蒸汽值的 15%%。
		当前强度系数 %d%%。]], "tformat")
t("Innovation", "创新", "talent name")
t([[Your knowledge of physical laws allows you to use and improve equipment in ways their creators never dreamed.
		Increases all stats, saves, armour, and defense bonuses by %d%% on equipment that is crafted by a master or powered by steamtech.]], [[你对物理学的了解令你能以全新的方式改进装备。
		增加大师制作或者蒸汽科技的装备提供的属性、豁免、护甲和闪避 %d%%。]], "tformat")
t("Supercharge Tinkers", "插件超频", "talent name")
t([[Using a huge amount of steam, you temporarily supercharge your tinkers and other steam-powered talents.
		For %d turns, you gain %d steampower and %d%% steamtech critical chance.]], [[消耗大量蒸汽，令所有配件和蒸汽技能超频工作 %d 回合。
		超频期间，你获得 %d 蒸汽强度和 %d%% 蒸汽技能暴击率。]], "tformat")
t("Last Engineer Standing", "背水一战", "talent name")
t([[Sometimes, being a master tinker requires taking risks; yours are more calculated than others.
		Gain %d cunning, %d physical save, %d%% resistance to self-inflicted damage, and %d%% chance to avoid being critically hit.]], [[成为大师意味着你经历了更多危险，你的计算力也超越凡人。
		增加 %d 灵巧，%d 物理豁免，%d%% 自身伤害抗性，%d%% 几率避免暴击。]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/furnace.lua"

t("Furnace", "熔炉", "talent name")
t([[You add a portable furnace to your steam generators.
		While it is active your fire and physical damage increases by %d%% and your fire and physical resistance penetration by %d%%.
		#{italic}#Burninate all with awesome Steam power!#{normal}#
		]], [[你往蒸汽制造机中安装一个便携式熔炉。
		熔炉激活时，你的物理和火焰伤害增加 %d%%，物理和火焰抗性穿透增加 %d%%。
		#{italic}#用蒸汽烧尽一切！#{normal}#
		]], "tformat")
t("Molten Metal", "融化金属", "talent name")
t([[While Furnace is on your armour is so hot from the furnace it dissipates parts of all energy based attacks against you.
		All non physical, non mind damage is reduced by %d (current %d).
		Each turn this happens you gain a molten point (up to 10), decreasing the efficiency of the reduction by 25%%.
		Molten points are removed upon running or resting.
		#{italic}#Hot liquid metal, the fun!#{normal}#
		]], [[你的护甲温度极高，能驱散部分能量攻击。
		所有非物理、非精神伤害降低 %d 点（当前 %d）。
		每回合该效果触发时，你获得 1 点融化点数（最多 10 点），使减伤效率降低 25%%。
		奔跑或休息时会清除融化点数。
		#{italic}#火热的液态金属，乐趣无穷！#{normal}#
		]], "tformat")
t("Furnace Vent", "通风孔", "talent name")
t([[Open the vents on your furnace, creating a conic blast dealing up to %0.2f fire damage at 10 molten points (currently %0.2f).
		All molten points are consumed.
		The damage will increase with your Steampower.
		#{italic}#By fire be purged!#{normal}#
		]], [[打开熔炉通风孔，制造锥形爆风；拥有 10 点融化点数时最多造成 %0.2f 火焰伤害（当前 %0.2f 点）。
		消耗所有融化点数。
		伤害随蒸汽强度提高。
		#{italic}#让火焰净化一切！#{normal}#
		]], "tformat")
t("Melting Point", "熔点", "talent name")
t([[When you reach 10 molten points your armour overheats, reaching temperatures so high that they cauterize up to %d detrimental physical effects on you.
		A special medical injector injects you with a fire immunity serum at that precise moment to make you immune to the burning effect.
		When this happens all molten points are consumed and trigger a Furnace Vent at the creature that triggered the last molten point.
		This effect drains 15 steam when triggered, and will not trigger if steam is too low.
		#{italic}#It's only a flesh burn!#{normal}#
		]], [[当你达到 10 点融化点数时，你的护甲过热，温度极高，以至于 %d 个负面物理状态被高温驱散。
		同时，一个特殊的医疗注射器会为你注射火焰免疫血清，令你免疫烧伤效果。
		该效果触发时，消耗所有融化点数，并自动对最后一次提供融化点数的生物触发一次通风孔效果。
		该效果将消耗 15 点蒸汽。蒸汽不足时不能触发。
		#{italic}#只是肉体在燃烧！#{normal}#
		]], "tformat")

------------------------------------------------

section "tome-orcs/data/talents/steam/gadgets.lua"

t("Autoloader", "自动填弹器", "talent name")
t([[You link your weapons and shield to your steam generators, using them to load ammunition and improve the power of your weapons. 
		Each time you fire your Steamgun, you have a %d%% chance to reload 1 Heavy Weapon ammo.
		Each time you fire a Heavy Weapon you reload %d ammo.
		Each time you raise your shield to block, you reload 1 Heavy Weapon ammo.
		This also increases weapon damage by %d%% and Physical Power by 30 when using steamguns or heavy weapons.
		In addition, your steamgun and heavy weapon shots now bypass friendly targets harmlessly.]], [[你将武器和盾牌连接到蒸汽机，使用它们来为你的武器填充弹药，并强化武器的能力。
		每当你使用蒸汽枪射击的时候，有 %d%% 的几率填充一枚重装武器的弹药。
		每当你使用重装武器射击的时候，会填充 %d 枚弹药。
		每当你使用盾牌格挡的时候，会填充一枚重装武器的弹药。
		这一技能也会在你使用蒸汽枪或重装武器的时候提升武器伤害 %d%%，提升物理强度 30。
		另外，你的蒸汽枪和重装武器射击可以安全地穿过友方目标。]], "tformat")
t("Exoskeleton", "机械外骨骼", "talent name")
t("#STEEL_BLUE#(%d exoskeleton)#LAST#", "#STEEL_BLUE#(%d外骨骼)#LAST#", "tformat")
t([[Current exoskeleton life: %d/%d
		You craft a set of steam powered armor that fits over your regular armor, enhancing your defense. The armor has %d life, and 50%% of all damage taken is redirected to it.
		Your powered armour repairs 5%% of it’s maximum life each turn, and each time you spend steam it will be repaired for %d%% of the steam cost.
		The armor's maximum life will increase with your Steampower.]], [[当前机械外骨骼生命值：%d / %d
		你制造一台蒸汽驱动的机械外骨骼，可以装载在你平常的护甲外面，增强你的防御能力。机械外骨骼具有 %d 生命值，你受到的所有伤害的 50%% 会转移到它身上。
		你的机械外骨骼每回合会修复 5%% 的最大生命值，每当你消耗蒸汽的时候，他也会修复相当于蒸汽值消耗 %d%% 的生命值。
		外骨骼的最大生命值受蒸汽强度加成。]], "tformat")
t("Hypervision Goggles", "强化视觉护目镜", "talent name")
t([[Enhance your vision for %d turns, giving you vision of all targets in range %d, even through walls. While the goggles are active you also spot flaws in your opponent's defenses, increasing your resistance penetration by %d%%.
In addition, the goggles passively increase your stealth, invisibility and trap detection by %d.]], [[强化你的视觉，持续 %d 回合。你将能看到半径 %d 码范围内的所有目标，该效果可以穿墙。当护目镜激活的时候，你也能注意到敌人防御上的弱点，增加你的抗性穿透 %d%%。
此外，护目镜会被动地增加你 %d 潜行、隐形和陷阱侦测能力。]], "tformat")
t("AED", "电击除颤器", "talent name")
t([[Prepare a defensive device that stores an electrical charge for 8 turns.
If your life falls below 0 while the AED is active it will activate to shock you back into life, negating the triggering attack, restoring %d life and dealing %0.2f lightning damage in radius %d that dazes affected enemies for 3 turns.
If the AED does not activate, the cooldown is reduced by 15 turns.
The healing and damage will increase with your Steampower.]], [[准备好一个防御性的设备，其电力可以持续 8 回合。
当你的生命值降到 0 点以下的时候，电击除颤器会启动，把你救活，取消这一致死的攻击，恢复 %d 点生命值，并在半径 %d 码范围内造成 %0.2f 闪电伤害，眩晕目标 3 回合。
如果电击除颤器没有启动，其冷却时间会减少 15 回合。
生命值恢复量和伤害受蒸汽强度加成。]], "tformat", {1,3,2})

------------------------------------------------

section "tome-orcs/data/talents/steam/gunner-training.lua"

t("Steamgun Mastery", "蒸汽枪掌握", "talent name")
t([[Increases weapon damage by %d%% and Physical Power by 30 when using steamguns.
		Also, increases your reload rate by %d.]], [[当你使用蒸汽枪时，增加 30 物理强度和 %d%% 武器伤害。
		你的装填弹药速率增加 %d。]], "tformat")
t("Double Shots", "双重射击", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t("%s resists!", "%s抵抗了效果！", "logSeen")
t([[In an overpowering display of marksmanship, you fire your steamgun(s) twice in rapid succession.
Each shot (targeted separately) deals %d%% damage and stuns its target for %d turns.
		The stun chance increases with your Steampower.]], [[你快速地射击两次，每次射击造成 %d%% 伤害，并震慑目标 %d 回合。
		震慑成功率受蒸汽强度加成。]], "tformat")
t("Uncanny Reload", "神秘装填", "talent name")
t([[You focus on managing your steamgun ammo for %d turns.
		While the effect lasts your attacks do not consume shots.]], [[你集中精力于蒸汽枪弹药 %d 回合。
		效果持续期间不消耗弹药。]], "tformat")
t("Static Shot", "静电射击", "talent name")
t([[You fire a special, electrically charged shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it bursts into electrified shrapnel within radius %d, which shocks each target hit and deals %d%% weapon damage as lightning.
		Shocked targets lose up to %d non-magical effects (for the first shot that hits).
		This talent does not use ammo.]], [[你用蒸汽枪向射程内的一处位置发射特殊的带电射击。
		每发子弹抵达目标位置时，都会爆裂成电化弹片，波及半径 %d 格，电击命中的每个目标，并造成 %d%% 武器伤害的闪电伤害。
		被电击的目标失去至多 %d 个非魔法效果（仅第一发命中时生效）。
		本技能不消耗弹药。]], "tformat")

------------------------------------------------

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
