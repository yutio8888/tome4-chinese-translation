section "tome-orcs/data/general/objects/generic-world-artifacts.lua"

t("potion", "药水", "entity type")
t("potion", "药水", "entity subtype")
t("Blood of Undeath", "不死之血", "entity name")
t("crimson phial", "猩红的药瓶", "_t")
t("This vial of corrupted blood reeks of death and decay. Yet somehow you feel drawn to it... Is it the tentalizing notion of eternal life? Or power? You can not tell, but the urge to drink it is great.", "这瓶腐败的血散发着死亡和腐烂的气味。但不知怎的，你觉得被它吸引了……这，就是永恒生命的具象化吗？还是强大的力量？你说不出来，但你充满了想喝它的冲动。", "_t")
t("quaff the Blood of Undeath to prepare your body for undeath", "喝下不死之血，让自己的身体为不死做好准备", "_t")
t("%s quaffs the %s!", "%s 大口喝下 %s！", "logSeen")
t("#CRIMSON#You feel the Blood of Undeath rushing through your veins. Your can feel your life wither away a little (-50 maximum life, -120 minimum life).", "#CRIMSON#你感受到不死之血在你的血管里流淌。你的生命渐渐流逝了（-50最大生命值，-120生命值下限）。", "logPlayer")
t("#CRIMSON#The Blood of Undeath strengthens your undead body (-60 maximum life, -140 minimum life).", "#CRIMSON#不死之血强化了你的不死之躯（-60最大生命值，-140生命值下限）。", "logPlayer")

------------------------------------------------

section "tome-orcs/data/general/objects/tinkers/chemistry.lua"

t("crude", "粗糙", "_t")
t("good", "良好", "_t")
t("well-made", "精致", "_t")
t("mastercraft", "大师级", "_t")
t("perfect", "完美", "_t")
t("%s poison groove", "%s 淬毒凹槽", "tformat")
t("Deals stacking poison damage.", "造成可叠加的毒素伤害。", "_t")
t("applies a stacking poison dealing %d damage per turn", "造成可叠加的毒素，每回合造成%d伤害。", "tformat")
t("%s viral injector", "%s 病毒注射器", "tformat")
t("Infects targets with a stat reducing disease.", "使目标感染削减属性的疾病。", "_t")
t("injects a simple virus dealing %d blight damage on hit and lowering the victims highest stat", "注入病毒，命中时造成%d枯萎伤害，并降低目标最高的属性", "tformat")
t("%s winterchill edge", "%s 寒冬之刃", "tformat")
t("Deals cold damage and slows.", "造成寒冷伤害并减速。", "_t")
t("chills your foe dealing %d damage and slowing them by one tenth of a turn", "冷冻你的敌人，造成%d伤害，并减速他们十分之一个回合。", "tformat")
t("%s acid groove", "%s 酸液之槽", "tformat")
t("Deals acid damage that also reduces armour.", "造成酸性伤害并降低护甲。", "_t")
t("splashes acid on your target dealing %d damage and reducing their armor", "朝敌人喷溅酸液，造成%d伤害，并降低护甲。", "tformat")
t("Brain Cap", "脑帽", "entity name")
t("HEAD", "头部", "entity on slot")
t("Brain Flare", "脑耀", "entity name")
t("CLOAK", "斗篷", "entity on slot")
t("%s waterproof coating", "%s 防水涂层", "tformat")
t("%s fireproof coating", "%s 防火涂层", "tformat")
t("HANDS", "手部", "entity on slot")
t("%s flash powder", "%s 闪光粉", "tformat")
t("%s itching powder", "%s 痒痒粉", "tformat")
t("armor", "护甲", "entity type")
t("cloak", "斗篷", "entity subtype")
t("Rogue's Gallery", "盗贼画廊", "entity name")
t("action packed cloak", "便于行动的斗篷", "_t")
t("Lined with reactive mechanisms, this cloak is equipped for any situation you might possibly encounter, and several you couldn't possibly encounter!", "内衬各种机械装置，这件披风包含着让你可以应对任何你有可能或不可能遇到的情况的特殊装备！", "_t")
t("On falling below 20% of your max life, releases a cloud of smoke, confusing nearby enemies and giving you stealth and a chance to avoid incoming damage for 5 turns.", "生命掉落至20%以下时，释放一阵烟雾，混乱周围生物，令你潜行并有一定几率免疫伤害，持续5回合。", "_t")
t("cause the next damage you deal to inflict crippling poison (does not recharge until used), dealing minor poison damage and causing your target to have a 10% chance to fail all talents", "令你下一次造成的伤害施加致残毒素（触发前不会再次充能）；该毒素造成少量毒素伤害，并使目标使用任何技能时有 10% 的几率失败。", "_t")
t("BODY", "躯体", "entity on slot")
t("%s rustproof coating", "%s 防锈涂层", "tformat")
t("%d%% chance to avoid a detrimental acid subtype effect.", "%d%% 几率避免酸性负面效果。", "tformat")
t("BELT", "腰带", "entity on slot")
t("%s alchemist's helper", "%s 炼金助手", "tformat")
t("LITE", "灯具", "entity on slot")
t("%s black light emitter", "%s 黑光发射装置", "tformat")

------------------------------------------------

section "tome-orcs/data/general/objects/world-artifacts.lua"

t("Medical Urgency Vest", "医疗急救背心", "entity name")
t("medical armour", "医疗装甲", "_t")
t("This light leather armour features a special medical injector.", "这件轻型皮甲配有一个特殊的医疗注射器。", "_t")
t("Steam Powered Boots", "蒸汽动力鞋", "entity name")
t("Boots. But with steam power!", "蒸汽动力！", "_t")
t("Generate %d steam each time you walk.", "每当你移动时，获得%d蒸汽。", "tformat")
t("The more steam the better!", "蒸汽越多越好！", "_t")
t("Steam Powered Helm", "蒸汽动力头盔", "entity name")
t("A Helmet. But with steam power!", "蒸汽动力！", "_t")
t("Steam Powered Gauntlets", "蒸汽动力手套", "entity name")
t("Gauntlets. But with steam power!", "蒸汽动力！", "_t")
t("Anti-Gravity Boots", "反重力鞋", "entity name")
t("overheating steel greaves", "过热的钢制护胫", "_t")
t([[These boots seem to have been made by a... creative individual who seems to have decided that launching yourself through the air via rocketry qualifies as "anti-gravity".
They look like they will work, though.
Probably.
If you're very careful.]], [[这套鞋子似乎是被一位具有……创造力的大师制造出来的，他似乎认为用火箭将你发射到空中就是“反重力”了。
看上去这套鞋子能用，大概。
确实有可能。
只要你非常非常小心。]], "_t")
t("These boots have a %d%% chance to fail to operate properly (reduced by Cunning).", "火箭靴有%d%%几率失败（随灵巧降低）。", "tformat")
t("jump to a nearby location within range %d, blasting everything within radius 2 (%d burning fire damage, 2 tile knockback) of the jump point and within radius 3 (%d burning fire damage, 3 tile knockback) of the landing point (damage based on Cunning)", "跳向半径%d码范围内的地点，轰炸起跳点附近半径2码范围内的所有敌人 (%d 火焰燃烧伤害，击退2格)以及落地点附近半径3码范围的所有敌人 (%d 火焰燃烧伤害，击退3格)（伤害随灵巧值提升）", "tformat")
t("#LIGHT_RED#You see no place to land near there.", "#LIGHT_RED#附近没有可以着陆的地点。", "logPlayer")
t("#Source# ignites %s %s, creating a #LIGHT_RED#blast of fire#LAST# that %s!", "#Source#点燃了%s%s，创造出一股#LIGHT_RED#火焰爆炸#LAST#%s！", "logCombat")
t("engulfs %s spectacularly", "，壮观的火焰吞没了%s", "tformat")
t("launches %s in the air", "，将%s送上天空", "tformat")
t("#Source# lands in a #LIGHT_RED#firey explosion#LAST#!", "#Source#引发了#LIGHT_RED#火焰爆炸#LAST#！", "logCombat")
t("Assassin's Surprise", "暗杀奇袭", "entity name")
t("glistening steel gauntlets", "闪耀光辉的铁手套", "_t")
t("These steel gauntlets feature a hidden contraption embedded in the left index finger that fires poisonous bolts.", "这对钢铁手套的左手食指中藏有一个能发射毒箭的精巧机关。", "_t")
t("fire a poisonous bolt out to range %d that deals %d nature damage and afflicts the target with crippling poison (%d%% fail chance) that deals %d addition nature damage over %d turns (damage based on Cunning)", "发射一支射程最远为 %d 码的毒箭，造成 %d 点自然伤害，并导致目标被致残毒素（%d%% 行动失败几率），在 %d 回合内造成 %d 点额外自然伤害（伤害受灵巧值加成）", "tformat", {1,2,3,5,4})
t("#Source# fires a bolt of #GREEN#poison#LAST# at #target# from %s %s!", "#Source#使用%s%s朝#target#发射#GREEN#毒液#LAST#！", "logCombat")
t("something", "某物", "_t")
t("Nacrush's Decimator", "纳克拉什的屠杀者", "entity name")
t("unwieldy gun", "笨重的枪", "_t")
t("Nacrush was known for a tendency towards overkill.", "纳克拉什因其滥杀而闻名。", "_t")
t("Knocks you back when fired.", "开火时击退自己。", "_t")
t("#Source# recoils from the shot.", "#Source#被反冲力击退。", "logCombat")
t("Signal", "信号枪", "entity name")
t("red barreled steamgun", "红色枪管的蒸汽枪", "_t")
t("An odd, stubby gun with a large, red barrel.", "一把奇特、粗短的枪，装有红色的枪管。", "_t")
t("Glacia", "冰川", "entity name")
t("frozen gun", "冰冻的枪", "_t")
t("Strange coils encircle this extremely cold gun.", "奇怪的线圈环绕着这把极其冰冷的枪。", "_t")
t("deal cold damage equal to 100 + the higher of your steam or spellpower, and attempt to freeze the target (20% chance).", "造成100+蒸汽强度或法术强度较高项的寒冷伤害，并有20%几率冰冻目标。", "_t")
t("Tinkerer's Twinblaster", "工程师的双重爆破", "entity name")
t("two barreled steamgun", "双管蒸汽枪", "_t")
t([[This gun seems to be some experiment in firing multiple shots simultaneously.
The design is somewhat rudimentary, but it seems to work.]], [[这把枪使用了实验性的技术一次射出多发子弹。
设计尚未成熟，但似乎还算能用。]], "_t")
t("Flashpoint", "燃点", "entity name")
t("overheated gun", "过热的枪", "_t")
t("\"Have you ever looked at some guys and thought 'you know, I really wish they were on fire right now', but you didn't feel like walking all the way over there? Well, there's now a better way!\"", "你是否曾经看到一些人并且想：“你知道吗，我真的想要烧死这些人”，但是你又不想大费周章，现在有了一个更加方便的方法！", "_t")
t("S.H. Spear", "S.H.长矛", "entity name")
t("engraved steamgun", "被雕刻的蒸汽枪", "_t")
t([[This gun is engraved with a strange material which focuses mental powers.
It seems like your mind will operate even faster with this equipped.]], [[这把枪被一种能强化精神力量的神秘物质雕刻。
装备着它，你的大脑似乎更加灵敏了。]], "_t")
t("Dreamweaver", "梦想编织者", "entity name")
t("shimmering steamgun", "闪光蒸汽枪", "_t")
t("This isn't so much a gun, as it is the idea of a gun.  You'll be able to remember it pretty easily if you lose it.", "这并不能算是一把枪，因为它只是一把枪的概念。当你丢掉它时你就记住它了。", "_t")
t("throw the gun and cause it to explode, dealing by %d mind damage (based on Cunning and Willpower) to all targets in an area, attempting to put them to sleep, and disarming yourself for 3 turns", "将枪扔出去引发爆炸，对范围内的所有敌人造成%d精神伤害（基于灵巧和意志），并试图催眠它们。你自己会被缴械3回合", "tformat")
t("%s tosses %s %s!", "%s投掷了%s%s！", "logSeen")
t("%s resists the sleep!", "%s抵抗了睡眠！", "logSeen")
t("Thoughtcaster", "思维施法者", "entity name")
t("crystalline handgun", "透明的手枪", "_t")
t("From body, mind. From mind, body.", "从物质中诞生意识。从意识中诞生物质。", "_t")
t("deal %0.2f mind damage (based on Mindpower) in a radius 1 around the target", "对目标周围半径 1 码内的敌人造成 %0.2f 点精神伤害（基于精神强度）", "tformat")
t("On hitting with a mindstar, deal physical damage equal to your steampower in radius 1 around the target.", "用灵晶命中时，在半径1范围内造成等于蒸汽强度的物理伤害。", "_t")
t("Spider's Fangs", "蜘蛛毒牙", "entity name")
t("pouch of envenomed shots", "一袋有毒的弹丸", "_t")
t("A dedicated technician seems to have built pockets of spider venom into these rounds. It's not clear how happy the spiders were about this.", "一位热心的技师似乎将成吨的蜘蛛毒液注入了这些子弹里。不知道蜘蛛对此有多么高兴。", "_t")
t("(cooling down: %d turns)", "(冷却时间：%d 回合)", "tformat")
t("Ready to trigger!", "可以触发！", "_t")
t("bursts into an cloud of spydric poison, pinning those inside (with a 10 turn cooldown)", "爆发一阵具有定身效果的毒云，10回合冷却", "_t")
t("Scattermind", "破碎意志", "entity name")
t("shattered mindstar", "破碎的灵晶", "_t")
t("A linen pouch of jagged mindstar fragments, each radiating a palpable sense of confusion and pain. They must have made up an impressive whole originally, before some cretin turned it to bits.", "一个亚麻布袋中装着锯齿状的灵晶碎片，让人清晰的感受到混乱和痛苦。在某个混蛋把它打成碎片之前，它一定是一个令人无法忘怀的整体。", "_t")
t("strike the target with one of Mind Sear, Psychic Lobotomy, or Sunder Mind, at random.", "随机使用以下技能之一打击目标：心灵灼烧、心灵脑叶切除或碾碎心灵。", "_t")
t("Thundercrack", "雷电打击", "entity name")
t("pouch of copper shots", "一袋铜制弹丸", "_t")
t("Through a combination of magic and airborne probes, these shots incite powerful bolts of lightning to strike your target from above, frying them and those around them!", "这些弹药通过魔法和探针从天空引导强力的闪电冲击你的目标，灼烧目标及周边的单位！", "_t")
t("a bolt of lightning strikes your target, dealing lightning damage to them and fire damage to those around them.", "一道闪电击中目标，造成闪电伤害，并对周围生物造成火焰伤害。", "_t")
t("Vindicator", "维序者", "entity name")
t("engraved gun", "雕花的枪", "_t")
t("\"Pesky undead plaguing your village? Necromancers ransacking your burial grounds? The Vindicator is the solution to all your woes!\"", "恼人的不死族在你的村庄传播瘟疫？死灵法师搜刮你的墓地？维序者可以解决一切。", "_t")
t("release a burst of light dealing damage equal to your cunning plus your magic in a ball of radius 2. If the target is undead, the damage and radius are doubled.", "在半径2范围内造成等于灵巧加魔法的光明伤害。若目标为不死族，伤害和半径加倍。", "_t")
t("Overburst", "强力爆裂", "entity name")
t("wide barreled steamgun", "粗管蒸汽枪", "_t")
t("\"Have you ever fired a shot into a group of monsters and thought 'there must be a better way?' Well now, there is!\"", "你曾经试过向一群怪兽中发射一粒粒弹药，然后觉得一定有更好的方法？好了，这就是了。", "_t")
t("Release a burst of shrapnel, dealing physical damage equal to your steampower in a cone from the target of radius 4.", "释放榴弹，在半径4锥形范围内造成等于蒸汽强度的物理伤害。", "_t")
t("Murderfang's Surekill", "屠牙的必杀", "entity name")
t([["Murderfang came over yesterday, raving about this idea for a steamgun he had. He described it in great detail, everything, except for how it would actually work.
What do you even grip it by? Insisted I make it though, left some design notes.
They all just say 'make it really flashy'.
 
-Pizurk, Master Tinker]], [[屠牙昨天跑来，兴奋地嚷嚷着他的一个蒸汽枪点子。他把一切细节都讲得天花乱坠，唯独没说这东西究竟该怎么运作。
这玩意儿到底该从哪儿握住？不过他硬是要我造出来，还留了些设计笔记。
那些笔记上全都只写着“弄得炫一点”。

——工匠大师皮兹鲁克]], "_t")
t("Burst apart, dealing physical damage equal to 25% of the original damage in a ball of radius 1.", "产生爆炸，在半径1范围内造成25%原伤害值的伤害。", "_t")
t("The Long-Arm", "长手", "entity name")
t("long barreled gun", "长管蒸汽枪", "_t")
t("This gun has an absurdly long barrel. You wonder for whom it may have been designed.", "这把枪的枪管长的出奇。你好奇这杆枪到底是为谁设计。", "_t")
t("Focus your aim on a target, marking them for death - reducing their ranged defense by %d and their resistances by %d%%", "凝神瞄准一个目标，将其标记为必杀对象——使其远程闪避降低 %d、所有抗性降低 %d%%", "tformat")
t("#Source# takes aim at #target# using %s!", "#Source#使用%s瞄准#target#！", "logCombat")
t("Annihilator", "歼灭者", "entity name")
t("gigantic many barreled gun", "巨大的多管蒸汽枪", "_t")
t("This gun features a wheel with several barrels attached and seems to be powered by an engine. It looks... impressive.", "这把枪的转轮上附有多支枪管，看起来由引擎驱动。看起来令人印象深刻。", "_t")
t("Fire rate increases while firing, up to 5 shots per turn. Resets after 5 turns without firing.", "攻击频率随着射击而增加，一回合最多射5次。5回合未射击则效果消失。", "_t")
t("50% chance to reload 1 ammo", "50% 几率装填1发弹药", "_t")
t("The Shotgonne", "火枪", "entity name")
t("huge gun", "巨型枪", "_t")
t([[This huge steamgun can be loaded with more than one bullet so that multiple shots can be fired in a nasty cone of death.
It also seems to have been carefully balanced to work like a dual gun set.]], [[这把巨大的蒸汽枪一次能装填多发子弹，并以锥形弹幕射出。
它似乎经过了精心配重，使用起来如同一对双枪。]], "_t")
t("When fired, shoots up to 4 extra shots at random foes with a radius 4 cone centered on the target.", "发射时，在半径4的锥形范围内随机射出至多额外4发子弹。", "_t")
t("Cloak of Daggers", "匕首披风", "entity name")
t("bladed cloak", "布满刀刃的披风", "_t")
t("This cloak seems to incorporate a series of blades attached to various spring mechanisms.  Apparently the designer believed that the best defense was an active one.", "这件披风上布满了刀刃和机关。显然制作者认为“最好的防御就是进攻”。", "_t")
t("Has a 50%% chance each turn to slash an adjacent enemy for %d physical damage (based on Cunning), making them bleed.", "每回合有50%%几率打击邻近的敌人，造成%d物理伤害（基于灵巧），并造成目标流血。", "tformat")
t("#Source#'s %s #GOLD#lashes out#LAST#, cutting #Target#!", "#Source#的%s#GOLD#向外割去#LAST#，切开了#Target#！", "logCombat")
t("Jetpack", "飞行背包", "entity name")
t("a jetpack", "飞行背包", "_t")
t("Finally.", "终于。", "_t")
t("Therapeutic Platemail", "医疗型板甲", "entity name")
t("heated armor", "加热的板甲", "_t")
t("This thick sealed armor utilizes a ventilation system to heal your wounds using a heated mist.", "这个厚重的板甲配备有通风设备，可以使用加热的薄雾来治疗你。", "_t")
t("cleanse up to 3 poisons or wounds detrimental effects", "清除最多3个毒素和流血负面效果。", "_t")
t("Titan", "泰坦", "entity name")
t("A gun sure to turn all to ash. As long as its nearby.", "一把只要出现在附近，就会把一切化为灰烬的枪。", "_t")
t("Golden Gun", "金枪", "entity name")
t("golden gun", "金色的枪", "_t")
t("every third hit always crits.", "第三下攻击必定暴击。", "_t")
t("Cautery Sword", "灼烧之剑", "entity name")
t("searing sword", "炽热的剑", "_t")
t("This sword is equipped with a heated core to add a bit of extra pain to the wounds.", "这把剑的炽热核心可以让敌人的伤口感到更加疼痛。", "_t")
t("inflict fire damage based on steampower", "造成基于蒸汽强度的火焰伤害", "_t")
t("Stimulus", "兴奋剂", "entity name")
t("injector", "注射器", "entity subtype")
t("autosyringe", "自动注射器", "_t")
t("This injecting unit is complemented by a belt of tiny vials, containing some sickly yellow liquid. The papers describe the contents as 'invigorating' and 'increasing the combat potency.'", "这个注射单元附带一排小药瓶，里面装着某种令人不适的黄色液体。文件将其中液体描述为“提振精神”和“提高作战能力”。", "_t")
t("inject yourself with painkillers, reducing all incoming damage by 5. Stacks up to 5 times. When the effect ends, lose 5% of your max life per stack", "为自己注射镇痛剂，使受到的所有伤害降低 5 点。最多叠加 5 次。效果结束时，每层使你损失 5% 最大生命值。", "_t")
t("Qog's Essentials", "寇格的精华", "entity name")
t("strange injector", "奇怪的注射器", "_t")
t("A hypospray full of ...something. There is no telling what you're injecting yourself with.", "一个无针注射器，里面装满了*某种*液体。你完全不知道你给自己注射了什么。", "_t")
t("Gain a random beneficial effect", "获得一个随机增益效果", "_t")
t("Deflector", "偏转", "entity name")
t("vibrating shield", "颤动的盾牌", "_t")
t("The front plate of this shield vibrates at all times, covering some strange assembly you can't quite make sense of.", "这面盾牌的正面装甲始终在振动，遮盖着某种你怎么也看不明白的奇怪装置。", "_t")
t("Knocks melee attackers away. Distance scales with damage incoming.", "击退近战攻击者。距离和其造成的伤害有关。", "_t")
t("Skysmasher", "破天", "entity name")
t("rocket powered maul", "火箭锤", "_t")
t("The discovery of rockets has proved incredibly dangerous. It is not always clear for whom.", "火箭的发明被证明为极其危险。尚不清楚对谁。", "_t")
t("Nimbus of Enlightenment", "启蒙灵气", "entity name")
t("elaborate cap", "精致的帽子", "_t")
t([[They are out to get you.
This is not real this is not real this is not real.]], [[他们要来害你。
这不是真的 这不是真的 这不是真的。]], "_t")
t([[By all accounts, just an ordinary cooking pot with an array of antennae haphazardly soldered onto it. An attached manual contains nothing but fifty pages of deranged gibberish, nonsensical diagrams and lines upon lines of numbers with no apparent pattern or reason to them. 

Putting this on your head may not be the best idea.]], [[不论怎么看，这都只是一口普通的烹饪锅，上面胡乱焊着一排天线。附带的手册有整整 50 页，却只有癫狂的胡言乱语、毫无意义的图示，以及一行又一行看不出任何规律或理由的数字。

把它戴在头上或许不是个好主意。]], "_t")
t("%s's Shadow", "%s的阴影", "tformat")
t([[itshereitshereitshereitshere
itshereitshereitshereitshere
itshereitshereitshereitshere
itshereitshereitshereitshere]], [[它在这里它在这里它在这里它在这里
它在这里它在这里它在这里它在这里
它在这里它在这里它在这里它在这里
它在这里它在这里它在这里它在这里]], "_t")
t("#F53CBE#%s's shadow awakens!", "#F53CBE#%s的阴影觉醒了！", "logSeen")
t("Pressurizer", "稳压器", "entity name")
t("heavy lined cloak", "沉重的披风", "_t")
t("This cloak hides and protects a series of powerful steam compressors.", "这件斗篷隐藏并保护着一套蒸汽压缩机。", "_t")
t("Eastern Wood Hat", "东方森林之帽", "entity name")
t("worn leather hat", "破损的皮帽", "_t")
t("This hat was made from materials from a forest whose name is long since lost, far in the east. It is said to have belonged to one of the first gunslingers.", "这顶皮帽的材料来自于遥远的树林，人们早已遗忘了树林的名字。据说它的主人曾是最早的枪手之一。", "_t")
t("Steamcatcher", "蒸汽捕捉器", "entity name")
t("pipe coated leather hat", "管道覆盖的帽子", "_t")
t("There's an old saying that most of your body heat escapes through your head. It's not true of body heat, but strangely, is actually true of steam.", "传说人体热量大部分从头部散失。对于体热来说并不是这样，但奇怪的是，蒸汽是从头部散失的。", "_t")
t("On taking fire damage: Gain 5% of the damage as steam.", "受到的火焰伤害5%转化为蒸汽。", "_t")
t("Shoes of Moving Quickly", "疾行之鞋", "entity name")
t("rocket powered boots", "火箭动力靴", "_t")
t("Accurately? Less so.", "精确吗？并不。", "_t")
t("You move 3 spaces at once.", "一次走3格。", "_t")
t("Band of Protection", "守护腰带", "entity name")
t("reinforced belt", "强化的腰带", "_t")
t("This belt utilizes an enchanted gem to focus a burst of steam into a powerful barrier.", "这条腰带利用一颗附魔宝石，将喷涌的蒸汽聚集为一道强力屏障。", "_t")
t("generate a personal shield that absorbs up to %d damage and damages attackers striking the wearer for %d fire damage while it lasts (based on Cunning)", "产生护盾，吸收%d伤害。在护盾破裂前，所有攻击穿戴者的人会受到%d火焰伤害（基于灵巧值）", "tformat")
t("%s summons a barrier of steam from %s %s!", "%s使用%s%s召唤出蒸汽屏障！", "logSeen")
t("Viletooth", "恶毒锯齿", "entity name")
t("rusted steamsaw", "生锈的蒸汽锯", "_t")
t("This aged looking saw is very rusty, and you think you see a thin layer of... something... on its blades.", "这个上了年头的链锯严重生锈，而且你发现锯刃上有一层薄薄的*东西*。", "_t")
t("may infect the target with a random disease", "可能触发随机疾病", "_t")
t("Mirrorazor", "镜面剃刀", "entity name")
t("rippling portal", "泛起波纹的传送门", "_t")
t([[The experiment of a mad chronomancer, this strange device is a portal into a backwards universe!
That is, everything there spins the opposite direction.
I guess it probably grinds things pretty well.]], [[这是一个疯狂的时空法师的实验，这个奇怪的装置是进入反向宇宙的入口！
也就是说，那里的一切都朝相反的方向旋转。
我想它可能磨得很好。]], "_t")
t("scroll", "卷轴", "_t")
t("This parchment contains some lore.", "这张卷轴里包含了一些手札。", "_t")
t("time-warped paper scrap", "被时间扭曲的纸片", "_t")
t("It came a long way away!", "它远道而来！", "_t")
t("Screw that!", "去他的！", "_t")
t("Oh, for the love of...  You're way too busy to deal with this nonsense.  You rev up Mirrorazor again, re-syncing it with the Mirror Universe, and toss the note back in.  A different note flies out the other side, miraculously not torn to shreds by the massive difference in planetary rotations.", "哦，拜托……你忙得根本没空理会这些胡言乱语。你再次启动镜面剃刀，让它与镜像宇宙重新同步，然后把纸条扔了回去。另一张纸条从另一侧飞出，竟奇迹般地没有被两颗行星巨大的自转速度差撕成碎片。", "_t")
t("#LIGHT_BLUE#Mirrorazor shudders as a note falls out from a different timeline!", "#LIGHT_BLUE#镜面剃刀颤动着，从里面抛出了一张来自另一条时间线的纸片！", "saySimple")
t("5 turns after use, mirror yourself across the map (centered around the location you were standing when activated).", "使用后5回合，将自己镜像到地图上（以激活时所站的位置为中心）。", "_t")
t("Razorlock", "连锁刀片", "entity name")
t("interlocked steamsaws", "连锁在一起的蒸汽锯", "_t")
t([[This intricate set of steamsaws lock together in a nearly indecipherable system.
They sure seem sharp though.]], "这套蒸汽链锯以奇特的方式锁在一起，看上去非常锋利。", "_t")
t("Ramroller", "剃刀平台", "entity name")
t("a... chariot?", "一个……战车？", "_t")
t("\"So we were thinking. You know what's better than saws? Really BIG saws. Unfortunately, no one could lift them. So we came up with an innovative new solution: Mount them on a motorized platform, allowing easy transportation and unparalleled cutting power!\"", "我们曾经这么想：你知道比锯子更好的是什么吗？巨大的锯子。可惜没人能够拿得动它们。所以我们想了一个新颖的主意：将他们安装在一个移动的平台上，以便让我们方便的运输，并获得无与伦比的切割能力。", "_t")
t("Moving builds up a stacking movement speed (caps at 25%) and damage bonus (caps at double). Hitting removes the bonus.", "移动会叠加移动速度加成（最高 25%）和伤害加成（最高使伤害翻倍）。命中目标后加成消失。", "_t")
t("Overcutter", "超级切割者", "entity name")
t("enormous steamsaw", "大型的蒸汽锯", "_t")
t("Earlier steamsaws were notably not meant to be used with one hand.", "显然早期的蒸汽锯不是为单手使用设计的。", "_t")
t("Turbocutter", "涡轮切割者", "entity name")
t("red striped steamsaw", "红色条纹的蒸汽锯", "_t")
t("\"Have you ever thought your steamsaws were just too slow? Well, have I got the thing for you...\"", "你曾经觉得你的蒸汽锯太慢了吗？那么，我有你需要的东西", "_t")
t("Increases the speed bonus from Saw Wheels by 25%.", "链锯轮提供的速度加成提高 25%。", "_t")
t("Whipsnap", "鞭笞", "entity name")
t("spring loaded steamsaw", "弹簧式蒸汽锯", "_t")
t("\"Sick of your pesky enemies hitting you with weapons? Well, with the new spring loaded Whipsnap, you can quickly put a stop to that!\"", "你是否已经厌倦了恼人的敌人用武器攻击你？那么，使用装载了弹簧的鞭笞，你可以迅速制止这一切！", "_t")
t("Pinwheel", "风车", "entity name")
t("spike tipped steamsaw", "尖端装刺的蒸汽锯", "_t")
t("\"Create new, exciting connections in other people's lives, such as between their feet and the floor!\"", "在他人的生命中建立全新，有趣的连接，比如他们的脚和地板！", "_t")
t("15% chance to pin the target", "15% 几率定身", "_t")
t("Frostbite", "霜咬", "entity name")
t("icy steamsaw", "冰冷的蒸汽锯", "_t")
t("Fashioned from magical ice, and perfect for carving ice - especially ice with someone else inside it.", "由魔法冰制成，非常适合雕刻冰块——尤其是里面冻着人的冰块。", "_t")
t("The Lumberator", "播种机", "entity name")
t("vined coated steamsaw", "爬满藤蔓的蒸汽链锯", "_t")
t("\"Spread the wonders of nature even quicker than ever with this seed injecting steamsaw! Your former enemies will be freshly grown trees before you even know it!\"", "这台能够注射种子的蒸汽锯可以更快的传播自然的奇迹。在你意识到之前，你的敌人体内将会长出一棵树！", "_t")
t("summon a treant (5 turn cooldown)", "召唤一个树人（5回合冷却）", "_t")
t("You cannot summon; you are suppressed!", "你不能召唤，你被压制了！", "logPlayer")
t("Not enough space to invoke!", "没有足够的空间召唤！", "logPlayer")
t("treant", "树人", "_t")
t("A very strong near-sentient tree, which has become hostile to other living things.", "一棵极为强壮的半智慧树木，对其他生物充满了敌意。", "_t")
t("Summon", "召唤", "_t")
t("Grinder", "绞肉机", "entity name")
t("bloody steamsaw", "染血的蒸汽锯", "_t")
t("Originally a kitchen implement used by the giants to saw through tough, frozen carcasses. Something is especially sinister about this example though.", "起初这个锯子只是被巨人们用来切割坚硬、冰冻的尸体。不过这个例子似乎有一些非常邪恶的暗示。", "_t")
t("On Taking Damage: Blindside the attacker (range 6).", "受伤触发：闪电突袭（范围 6）。", "_t")
t("Overclocked Radius", "超频半径", "entity name")
t("distorted steamsaw", "扭曲的蒸汽锯", "_t")
t([[Faced with the petty quandaries of 'conventional physics', some mad tinker must have coated this sawblade with a fine sheathe of dilated time to maximize its speed.
 
There were ...side effects.]], [[面对“传统物理学”的小小难题，某位疯狂的工匠一定给这片锯刃覆上了一层细薄的膨胀时间，以将速度提升到极致。

不过……它产生了一些副作用。]], "_t")
t("Attack speed increases with paradox, up to 250% at 1000 paradox.", "攻击速度随紊乱值增加，1000紊乱时为250%。", "_t")
t("increase paradox by a random amount", "随机增加紊乱值", "_t")
t("increase paradox by a drastic amount with a chance to do an anomaly (%d%% chance). If anomaly triggers, halve paradox.", "大量增加紊乱值，并有一定几率触发异常(%d%% 几率)。如果触发了异常，紊乱值减半。", "tformat")
t("Heartrend", "心脏切割", "entity name")
t([[There is an attached note.
 
'I've spilt the heartsblood of my work, feeling it pound, like a heart, in my palms.
Some people just can't let go until they've bled dry.']], [[上面粘着一页笔记。

'我将我的心血之作分离，感受它的跳动，像心脏一样跳动，在我的手心里。
总有些人不到血流尽，不撒手。']], "_t")
t([[All damage dealt by or to you (that is over 1% of max life) bleeds for an additional 20% of the damage as physical damage (ignores most status resistances).
While you are bleeding, Heartrend's damage increases and it gains lifesteal.]], [[你受到与造成的所有超过1%总生命的伤害将触发流血效果，无视大部分状态免疫，造成额外20%物理伤害。
当你处于流血状态时，心脏切割伤害增加并具有吸血效果。]], "_t")
t("If bleed damage per turn is greater than 5% of max life, attacks cleave.", "若每回合流血伤害超过最大生命值的 5%，攻击将变为劈击。", "_t")
t("Dethzaw", "死忘链据", "entity name")
t("fiery steamsaw", "火焰蒸汽锯", "_t")
t([[Grushgore the Destroyer was absolutely enthralled when he discovered steamsaws. He immediately kidnapped several tinkerers and forced them to create this for him.
His naming skills have not improved.]], [[毁灭者格鲁什戈尔发现蒸汽链锯时十分激动，他立刻抓了几个工程师，强迫他们为他做了这个。
他的取名技巧从没有得到提高。]], "_t")
t("deal a melee attack against all other enemies in a circle around you", "对周围一圈敌人进行近战攻击。", "_t")
t("Galen's Flowing Robe", "盖伦的科技法袍", "entity name")
t("ample robe", "宽大的法袍", "_t")
t("This robe was worn by the Technomancer Galen, infused with technomancy enchantments it is said to react to techno-spells!", "这身法袍曾由科技法师盖伦穿着，并被注入了科技法术附魔；据说它会对科技法术产生反应！", "_t")
t([[20% chance when casting a technomancy spell (or 10% chance when casting a normal spell) to power-up the internal defense circuits of the robe.
The circuit will do one of:
#AQUAMARINE#if more than one foe is in melee range#LAST#: teleport away all foes
#AQUAMARINE#if below 50% life#LAST#: increase all resistances by 20% for 5 turns
#AQUAMARINE#if below 20 steam#LAST#: supercharge the arcane dynamo to produce 4 more steam per 10 mana spent for 5 turns
#AQUAMARINE#otherwise#LAST#: reset the cooldown of the spell with the highest remaining cooldown
]], [[当你释放科技法术的时候，你有20%几率（释放普通法术的时候几率为10%）激活长袍内部的防御电路。
防御电路会带来以下效果之一：
#AQUAMARINE#如果近战范围内有超过一个敌人#LAST#：将所有敌人传送走
#AQUAMARINE#如果生命值在50%以下#LAST#：提升所有抗性20%，持续5回合
#AQUAMARINE#如果蒸汽值低于20#LAST#：超载奥术发电机，每10点法力值额外产生4蒸汽，持续5回合
#AQUAMARINE#其他情况#LAST#：重置目前剩余冷却时间最长的法术的冷却时间
]], "_t")
t("#PURPLE#%s activates and teleports away all nearby creatures!", "#PURPLE#%s启动，传送走了周围的所有生物！", "logSeen")
t("#PURPLE#%s activates and increases %s's resistances!", "#PURPLE#%s启动，增加了%s的抗性！", "logSeen")
t("#PURPLE#%s activates and increases %s's arcane dynamo power!", "#PURPLE#%s启动，增强了%s的奥术发电机的能力！", "logSeen")
t("#PURPLE#%s activates and resets %s's %s cooldown!", "#PURPLE#%s启动，重置了%s的%s冷却时间！", "logSeen")
t("Galen's Will", "盖伦的意志", "entity name")
t("aether-infused steamsaw", "以太灌注的蒸汽链锯", "_t")
t("Saws made of metal? That is no good for a discerning Technomancer so Galen made a saw out of pure arcane forces!", "金属制作的链锯？挑剔的科技法师可不会满足于此，所以盖伦用纯奥术力量制造了一把链锯！", "_t")
t("Increases the steam your arcane dynamo generate per 10 points of mana by 2.", "增加你的奥术发电机产生的蒸汽量，每消耗10点法力值产生的蒸汽量增加2。", "_t")
t("Eye of the Lost", "迷失之眼", "entity name")
t("pale mindstar", "苍白的灵晶", "_t")
t("A strange aura surrounds this mindstar. You feel a presence, but it is obscured, as if it refuses to be found.", "灵晶周围有一层奇怪的领域。你能感觉到某个存在，但它被遮蔽了，就像它不愿意被察觉到一样。", "_t")
t("reduces mental save", "减少精神豁免", "_t")
t("see all other beings around you for 5 turns", "看到你周围所有的生物5回合", "_t")
t("Brass Goggles", "铜制护目镜", "entity name")
t("classy goggles", "经典的护目镜", "_t")
t("No self respecting craftsman would be caught without them!", "没有任何一个自爱的工匠会被人发现没有佩戴它！", "_t")
t("X-Ray Goggles", "X射线护目镜", "entity name")
t("pitch black goggles", "漆黑的护目镜", "_t")
t("How do these even work?", "这玩意到底怎么用？", "_t")
t("see everything. EVERYTHING. For 5 turns, anyway", "看到所有东西。*所有东西*。当然，只有5回合。", "_t")
t("Laser Powered Giant Smasher", "激光驱动巨型粉碎器", "entity name")
t("radiant hammer", "光辉的锤子", "_t")
t("The Laser Powered Giant Smasher, nicknamed the Gloryhammer. You can feel it vibrating with untold power in your hands.", "激光驱动的巨型粉碎器，绰号“光荣之锤”。你能感觉到它在你的手中以无穷的力量震动。", "_t")
t("#PURPLE#You feel the power of the Gloryhammer course through you! It has become fully empowered!", "#PURPLE#你感受到光荣之锤的力量环绕着你！它的力量被完全释放了！", "logPlayer")
-- untranslated text
--[==[
t("%s", "%s", "tformat")
--]==]


------------------------------------------------

section "tome-orcs/data/ingredients.lua"

t("metal", "金属", "ingredient type")
t("lump of iron", "铁块", "ingredient name")
t("lump of steel", "钢块", "ingredient name")
t("lump of dwarven steel", "矮人钢块", "ingredient name")
t("lump of stralite", "斯莱特块", "ingredient name")
t("lump of voratun", "沃瑞钽块", "ingredient name")
t("herbs", "草药", "ingredient type")
t("stack of herbs (viperweed)", "一束植物（蛇草）", "ingredient name")
t("stack of herbs (sessali)", "一束植物（延龄草）", "ingredient name")
t("stack of herbs (bilberry)", "一束植物（越桔）", "ingredient name")
t("stack of herbs (burdock)", "一束植物（牛蒡）", "ingredient name")
t("stack of herbs (goldleaf)", "一束植物（金叶）", "ingredient name")
t("misc", "杂项", "ingredient type")
t("brain in a jar", "瓶中脑", "ingredient name")
t("mechanical core", "机械核", "ingredient name")
t("primal core", "原始之核", "ingredient name")
t("metal", "金属", "entity type")
t("lump of iron", "铁块", "entity name")
t("A lump of iron.", "一块铁。", "_t")
t("lump of steel", "钢块", "entity name")
t("A lump of steel.", "一块钢。", "_t")
t("lump of dwarven steel", "矮人钢块", "entity name")
t("A lump of dwarven steel.", "一块矮人钢。", "_t")
t("lump of stralite", "斯莱特块", "entity name")
t("A lump of stralite.", "一块斯莱特。", "_t")
t("lump of voratun", "沃瑞钽块", "entity name")
t("A lump of voratun.", "一块沃瑞钽。", "_t")
t("herbs", "草药", "entity type")
t("stack of herbs (viperweed)", "一束植物（蛇草）", "entity name")
t("A stack of herbs.", "一束草药。", "_t")
t("stack of herbs (sessali)", "一束植物（延龄草）", "entity name")
t("stack of herbs (bilberry)", "一束植物（越桔）", "entity name")
t("stack of herbs (burdock)", "一束植物（牛蒡）", "entity name")
t("stack of herbs (goldleaf)", "一束植物（金叶）", "entity name")
t("misc", "杂项", "entity type")
t("brain in a jar", "瓶中脑", "entity name")
t("A still living brain of a powerful psionic creature.", "强大灵能生物的大脑，依然存活着。", "_t")
t("mechanical core", "机械核", "entity name")
t("The core unit of the Automated Defense System.", "自动防御系统的核心元件。", "_t")
t("primal core", "原始之核", "entity name")
t("The core wood of a great tree.", "伟大树木的核心之木。", "_t")

------------------------------------------------

section "tome-orcs/data/lore/emporium.lua"

t("vaporous emporium", "蒸汽商场", "newLore category")
t("a large poster", "一个大型海报", "_t")
t([[#{bold}#CLOGGING NO MORE!#{normal}#
If steam-vent congestion ails you, avail yourself of:
 
#{italic}#[An illustration depicts a rectangular glass bottle, labelled "DR. RAGLUK's DECLOGGING DRAUGHT".]#{normal}#
 
MADE WITH LOVE, CARE, AND THE PUREST MINERALS FROM THE STEAM QUARRY
 
Just one capful will cleanse your pores, flushing toxins out with the steam!
 
ALSO EFFECTIVE FOR: Headaches, nausea, ennui, fatigue, aches and pains, and general malaise!
 
#{italic}#[A disclaimer occupies the bottom margin of the poster, in print so small you doubt the giants would be able to read it.]#{normal}#
 
WARNING: This product has been determined by the Council of Health Authority to be correlated with the following conditions: Inverse vertigo, increased hair flammability, non-vaporous sweating, night terrors, liver dysphoria, headaches, miner's lung, brainlock, day terrors, mitosis, visions of a great butchered being, miner's elbow, skeletal emancipation, gastrointestinal infamy, brittle kidney, pinaciphobia, decreased global speed, teleportitis, miner's tongue, merged nostrils, an ancient and foul curse, lowered steam pressure, fat burning (literal), ocular feathering, Orcish body odor, arcane disruption, gravity loss, bloodlock, malfeasance, rectal carpeting, nihilism, mid-evening terrors, knee rust, and minor clogging of the pores.]], [[#{bold}#不再堵塞！#{normal}#

如果蒸汽孔阻塞困扰你，请用这个来帮你：

#{italic}#【一幅插图描绘着一个长方形的玻璃瓶，标签上写着“拉格卢克博士的清淤药水”。】#{normal}#

用爱、关怀和蒸汽矿场最纯净的矿物质制成！

只要一瓶盖的量就能清洁你的气孔，和蒸汽一道排出毒素！

也对以下症状有效：头痛、恶心、倦怠、疲劳、各种疼痛，以及广泛性的不适！

#{italic}#【一个备注占据了海报的底部边缘，印刷字体太小以致于你怀疑巨人们能不能看到。】#{normal}#

警告：经卫生理事局评议，此产品与以下症状有相关性：反转性眩晕、毛发可燃性增加、非蒸汽性出汗、夜间惊恐发作、肝火、头痛、尘肺病、脑锁、日间惊恐发作、有丝分裂、关于巨大被宰割物的幻觉、矿工肘、关节松脱、肠胃糜烂、肾脆症、尖端恐惧症、整体速度下降、随机传送症、矿工舌、鼻孔合并、某个古老又邪恶的诅咒、低蒸汽压、脂肪燃烧（字面意义）、眼部羽化、兽人体味、奥术干扰、重力丧失、血锁、渎职、直肠沉积、虚无主义、傍晚惊恐发作、膝盖生锈，以及气孔的轻微堵塞。]], "_t")
t("tattered poster", "破烂的海报", "_t")
t([[CLOSING SALE
for
KALTOR's FIREARMS, ARMOR, AND OTHER MARTIAL SUNDRIES
 
It is with a heavy heart that I must announce our closing.  After over twenty years of service, I am shutting my doors - the people of the Atmos Tribe apparently wish to trust the Guard with their well-being, and the Guard chooses to maintain the weapons it already has rather than purchase things like the #{italic}#BRILLIANT AUTO-LOADING ORC EXPELLER#{normal}# (only 30 gold!), or the #{italic}#PRESSURE-ENHANCED SLASHPROOF COMBAT SUIT#{normal}# (only 450 gold!).  I even offered discount options such as the #{italic}#LIL SURPRISE#{normal}# (now only 15 gold!), and yet the city would have none of it.  It would seem my services, and my talents, are simply not wanted.
 
Even if you have no fear of the orcish tribes, ritch swarms, and other assorted threats that lurk just outside our city walls, please consider purchasing some of my wares.  They are truly beautiful displays of craftsmanship, and would do well as a desk sculpture or (if properly disarmed) a child's toy.  If nothing else, you will be ensuring that a once-proud artisan with great love and respect for his craft need not resort to begging on the streets.]], [[卡托尔的军火、护甲和军用杂货店即将停业

我心情沉重地宣布我们店的停业。二十年的经营后，我要关门了————气之部族的居民显然想要用他们的全身心信任守卫们，而守卫们却想维持原来的配备，而不是去购置像是“#{italic}#光辉灿烂的自动装填的兽人驱除器#{normal}#”（仅售30金币！）或者是“#{italic}#增压的防挥砍的战斗服#{normal}#”（仅售450金币！）。我甚至推出了像是“#{italic}#小小大惊喜#{normal}#”（现在仅售15金币！）这样的优惠，但是这个城市不愿意买任何一件。看上去我的竭诚服务和才华横溢真的没人需要。

即使你们一点也不怕那些兽人部落、里奇虫群和在我们城市外游荡的各种威胁，请还是考虑一下要不要买我的一些东西。它们确实美丽得体现了匠人精神，而且可以做好的书桌摆设品或者是孩子的玩具（如果做好了保险措施的话）。如果你愿意伸出援手的话，你可以让一个热爱又尊重他的作品，曾经自豪的工艺大师不再被迫流落街头乞讨。]], "_t")
t("ornately-painted poster", "绘制精美的海报", "_t")
t([[Stylish.  Elegant.  Exclusive.

#{bold}#EXTINCTION#{normal}#, a new line from Faerlhing's Weavings, the finest name in fashion.

Steel drakes can no longer be found in the wild - our pens contain the ONLY living ones in Var'Eyal, and possibly the last generation to not be marred by inbreeding-induced deformities.  When you wear our wonderful coats, dresses, boots, or corsets to a party, meeting, or other get-together, the others won't just notice the unique, metallic sheen matched with unparalleled flexibility unique to their scales.  They'll know that they CANNOT imitate your look.  That it's a look their children will NEVER have.  That YOU have made your mark on ecological history, and reaped the fashionable, comfortable benefits.  And steel drake scales are not known to decay naturally, so proof of your impeccable taste will live far longer than the species they were taken from.

Place your orders now.  Open bidding will run for 30 days, after which point orders will be handled on a first-come, first-serve basis.

Other fashions come and go.  #{bold}#EXTINCTION#{normal}# is forever.
]], [[新潮。优雅。独特。

#{bold}#绝灭#{normal}#，费尔荷纺织厂的新一批生产品，时尚界最响亮的名字。

在野外再也不能发现钢化幼龙了————我们的兽栏里有着瓦·埃亚尔最后活着的一批，也可能是最后一代不被近交缺陷所玷污的龙了。当您穿着我们美妙的外套、连衣裙、靴子或是塑身衣去参加派对、会议或是其他集会，其他人不仅仅会注意到那特别的金属质感，以及搭配着鳞片的那无可比拟的弹性特质。他们还会知道，自己不能模仿您的样子。这是一种他们的孩子永远不会再有的样子。您在生态史上有浓墨重彩的一笔，独占了这时尚又舒适的好处。而且钢化幼龙的鳞片从未有自然老化的纪录，因此您独特品味的证明会比用于制衣的物种还要久存。

立刻预订吧。公开拍卖将会进行30天，在这之后预订会遵循先到先得的原则。

潮流如过客，#{bold}#绝灭#{normal}#恒久远。
]], "_t")
t("official-looking poster", "看上去很官方的海报", "_t")
t([[#{bold}#KEEP THE PRESSURE UP!#{normal}#
#{italic}#An announcement on power consumption, paid for by the Council of Geothermal Authority#{normal}#

As per our previous announcements, the geothermal vents of the Steam Quarry have begun to taper off in output.  While our geologists and military consider all available options for finding new vents (or alternative sources of steam power), we need YOUR cooperation to keep the pipes from running dry!  Here's how you can help make sure we have enough steam for everyone:

-Cook the old-fashioned way - with flame magic, or a firewood stove.  Flash-steamers, although certainly a convenient way of preparing food, are VERY inefficient.  For a free handbook on delicious and easy-to-learn recipes for a conventional or pyromancy-based stove, simply come to the Council of Geothermal Authority offices and take one from the lobby.

-Remember to shut off your appliances when you're done with them!  A full 5% of our power usage is estimated to be from washing machines, mills, carousels, generator-powered lighting, and other such devices left plugged in when not in use.  When you are done using an appliance, make sure it has been deactivated; to be completely sure, our experts recommend shutting off the valve entirely, then disconnecting the appliance and placing a standard cap over the output pipe.

-Have your pipes checked regularly.  Leaking valves and loose fittings can consume tremendous amounts of steam pressure; you are only required to have your home steam-pipes inspected every three years, but additional inspections are available at no charge (once every six months).  Volunteering for these inspections can reduce your geothermal consumption, and fees, dramatically.

-Use your own steam!  With regular exercise and a good diet, you can create your own power by wearing a collection suit, and plug the pressurized reserve tanks into your home intake valves to reduce the amount of power drawn from the geothermal system by over 40% (depending on personal production).  Short-term use of declogging tonics may help, but long-term use is generally ill-advised.

-Do NOT pressurize tanks from the tap and sell them to others!  This is a violation of Council law, punishable by a fine of up to 3,000 gold and up to four years in prison, per tank.

Thank you for helping ensure we ALL have power, while we work on curing this shortage!]], [[#{bold}#保持蒸汽压力！#{normal}#

#{italic}#地热能源理事局关于能源消耗的通知#{normal}#

我们之前的通知表明了蒸汽矿场地热出气口的输出在逐渐减少。在我们的地质学家和军方正在考虑其他寻找新出气口（或其他替代性蒸汽能源）的方案时，我们需要你们的合作来防止管道枯竭！为了大家都有足够蒸汽用，您可以通过以下的方法做出贡献：

- 用老式方法烹饪 —— 用火焰魔法或是烧柴的炉子。闪蒸炉尽管是准备食物的快捷方式，不过确实能源效率很低。如您需要免费的《传统或魔法炉子，美味易学的食谱手册》，请到地热能源理事局办事处的大堂领取一份。

- 当您用完蒸汽设备后请记得关闭！据统计，我们足足5%的能源消耗来源于用完洗衣机、磨坊、旋转木马、蒸动灯和其他类似设备不拔插头。当您用完设备后，请确认断气；如果要完全确定，我们的专家建议把气阀给全关掉，然后断开与设备的连接，把一个标配的盖子放在出气管上。

- 经常检查您的管道。泄漏的阀门和松散的接头会消耗大量的蒸汽气压；您家里的蒸汽阀只需要每三年检查一次，但是附加的检查是免费的（每六个月一次）。自愿报名这些检查会让地热消耗和费用大大减轻。

- 用您自体的蒸汽！只要定期锻炼，合理安排膳食，您只要穿着收集服就可以自己供能，然后把上面的压缩储存箱接在家里的进气阀上就可以减少40%来自地热系统的消耗（根据个人生产量而不同）。短期使用清淤药水可能有助于提高产量，但不建议长期使用。

- 请勿从地热系统的气管里装气卖给他人！这违反了理事局制定的相关法律，违者每违法售出一罐将遭受最高3000金币罚金，并处四年监禁。

感谢您为保证大家都能用上能源而出力，与此同时我们也在着手解决能源短缺的问题！]], "_t")
t("hastily-written poster", "匆匆写就的海报", "_t")
t([[KALTOR's FIREARMS, ARMOR, AND OTHER MARTIAL SUNDRIES
is
OPEN FOR BUSINESS AGAIN!
 
The orcish hordes are upon us!  Although I am not normally one for gloating, I feel I must take this opportunity to say:
 
#{bold}#I TOLD YOU SO, YOU INGRATES#{normal}#
 
Do you see the need for my wonderful devices of self-defense NOW?  Do you see why I toiled so thoughtfully and tirelessly to make such exquisite contraptions that could've saved so many lives, if you'd only been willing to pay what I was asking for them, only a tiny fraction of what they were worth?  Does the USELESS City Guard see why they should have been purchasing my newest, improved models, such as the #{italic}#BRILLIANT AUTO-LOADING ORC EXPELLER#{normal}# (only 600 gold!  Get yours now!  Protect your family!) instead of abusing my built-to-last craftsmanship to keep my original production run around for over a decade?
 
Don't make the same mistake twice!  Purchase the #{italic}#LIL SURPRISE#{normal}# for merely 150 gold!  What's that?  You can't afford that entry-level price?  I guess you should've bought it while I was still making them!  Don't want to get your guts torn out by a little green-skinned savage?  My old price for the #{italic}#PRESSURE-ENHANCED SLASHPROOF COMBAT SUIT#{normal}# was a steal at 700 gold - if you want one now, I'm sure your life is worth at least 3800 gold to you.  It utilizes your own vents to power tiny motors hidden in its joints, granting an unparalleled combination of fortitude and mobility; guaranteed to protect you from ANY sort of harm those savages can dish out, without slowing you down!  Notice all those dead guardsmen around?  Notice how they AREN'T wearing a #{italic}#PRESSURE-ENHANCED SLASHPROOF COMBAT SUIT#{normal}#, despite my desperate recommendations?  Don't let that be you or your loved ones!
 
I'm sure you have your doubts as to the efficacy of my lovingly-made armaments; for a free demonstration of the quality and effectiveness of my goods, you are invited to try to take them by force.  I dare you - and that includes the City Guard, should they have any delusions about confiscating them for the public good.  The public has dug their own grave, and I will not pull them up simply out of charity; after all, they have offered me no such charity in the past.
 
#{italic}#[An address is listed at the bottom of this poster.  You could attempt to raid this store, if you wanted, but the owner's armed to the teeth - it's unlikely it'll be worth the risk.]#{normal}#
]], [[卡托尔的军火、护甲和军用杂货店
重新开业了！！

兽人部队正威胁着我们！虽然我一般情况下也不是个幸灾乐祸的人，但是借这个机会我必须说一下：

#{bold}#我早就告诉过你们了，你们这些忘恩负义的人！#{normal}#

你们如今看到了对于我这些绝妙的自我防御设备的需求了吗？你们能看出，为什么我要殚精竭虑地做这些可以拯救无数性命的奇特精妙的装置。而你们曾经只需要付出我要求的价钱，仅仅是它们实际价值的一小部分？那些没用的城市守卫有没有看出，他们早应该买我的最新的、升级的型号，比如说“#{italic}#光辉灿烂的自动装填的兽人驱除器#{normal}#”（仅售600金币！马上为自己弄一件！守护你的家庭！）而不是滥用我那产品经久耐用的工艺，让我之前生产的产品在市面上流通了超过十年？

别再犯第二次错误了！只用150金币买下“#{italic}#小小大惊喜#{normal}#”吧！啥？你付不起这个入门级别的费用？我猜你早应该在我正在做它们的时候买下！你不想让你们的肠子被一个绿皮小个子野蛮人拉出来吧？我给“#{italic}#增压的防挥砍的战斗服#{normal}#”定的原价700金币，简直就是你们对我的偷窃——如果你现在想要一件，我确定你的生命对于你自己来说至少值3800金币。它充分利用了你的排气孔来为战斗服中微小的马达供能，提供了无可比拟的防御性和机动性的平衡；保证能保护你免受那些野蛮人能扔出的任何种类的攻击，同时又不会让你的速度慢下来！注意到附近那些死掉的守卫吗？注意到尽管我强烈推荐过，但他们仍然没有穿着“#{italic}#增压的防挥砍的战斗服#{normal}#”？别让那种惨死发生在你或者是你爱的人身上！

我敢肯定，你们对我那些用心制作的工艺品的效用一定有疑问；作为对我的商品的质量和效能的免费展示，欢迎你们来抢走它们。我向你们挑战 —— 城市守卫也包括在内，如果他们妄想着打着公众利益的旗号强征这些产品的话。这一切都是因为他们自掘坟墓，我可不会因此而大发善心；毕竟，他们过去没有给我这种善心。

#{italic}#[在这个海报的底部列出了一个地址。如果你想的话，你可以试着去抢这个商店，但是店主武装到牙齿 —— 可能不太值得冒着风险去抢劫货物。]#{normal}#
]], "_t")

------------------------------------------------

section "tome-orcs/data/lore/gem.lua"

t("strange black disk (1)", "奇怪的黑色碟片 (1)", "_t")
t([["...thing on? Okay, good. This is Haze Commander Parmor of the Geothermal Exploratory Mole, on a mission to..."  She sighs. " 'Find the Loyalist and arrange for our safe transport to his refuge, offering him his previous terms of agreement.' Which is Council-speak for 'flee in terror to the only thing that could bail us out of this mess, and bring the Eye with us.' Personally, I'm not keen on putting our fates in the hands of some nutter who lives underground and..." Indistinct grumbling. "...not even my damn job, I didn't sign up to be some politician's valet--"

#{italic}#(You hear a door opening, and another voice speaks.)#{normal}#

"Captain, the tea-maker isn't working!  Get someone on that, post-haste!"

#{italic}#(The door closes.)#{normal}#

"...Yeah, Councillor Tantalos is getting his tea as soon as he can un-kick the hornet's nest that got us into this chaos.  Moving on...  departure was on time, projected journey to the Loyalist's last known position is underway, making a tunnel there from right under the palace.  All systems functioning, except for the tea-maker, and I can't give a slag about that.  End log."]], [[“……什么事？好，好的。这里是地热探测鼹鼠GEM，阴霾指挥官帕默，我们正在执行的任务是…”她叹了一口气“上面写着，‘寻找忠诚者，将我们安全地运送到他的避难所，并向他提供我们之前在协议中许诺的东西。’如果不用官腔的话，就是‘在恐惧中逃跑，逃向唯一能够把我们从这篇混乱中解救出来的家伙那里，别忘了把“眼睛”带走。’从个人角度，我可不想把我们的命运，交到某个生活在地底下的狂人手里，而且…”含糊不清的抱怨“…这根本他妈的不是我的工作，我可不是某些政治家的仆人——”

#{italic}#（你听到了开门的声音，有另一个人的声音响起）#{normal}#

“船长，沏茶机坏了！快叫人来处理，马上！”

#{italic}#（关门声）#{normal}#

“……是的，坦塔洛斯议员还他妈的想喝茶，要不是他刚刚给我们捅了个大马蜂窝，把我们搞的一团糟。继续……我们的出发时间很准时，正在准备前往忠诚者的上一个位置，我们将会从宫殿下方挖一条隧道过去。所有系统工作正常，除了沏茶机，去你妈的沏茶机。日志结束。”]], "_t")
t("strange black disk (2)", "奇怪的黑色碟片 (2)", "_t")
t([["...for posterity!  Let's make sure future generations can hear the moments of history being made!" You hear the voice of Councillor Tantalos again... and then you hear a very strange voice, one that's all too clear. Even with the device playing it, it sounds like it's coming from inside your own head.#{normal}#

"Yes, yes, good idea. This is an important day, for both of us - no, for Eyal...  You've brought what I asked for so long ago, then?"

"Of course!  It's just--  bring the cart around here!"  (Clanking and grinding.)  "Open it up, if you wish."

"No need.  I can feel its power, it's so familiar and yet so new...  This could only be the Eye of Amakthel Himself!  It's beautiful, and all will know its beauty..."

"Er...  splendid, I assume!  This is the beginning of a long and beautiful partnership between the Atmos and...  your people!  Shall I go back up and tell them we're ready for them, and you're ready to handle the Orc situation? They're, ah, rather eager to come down here--"

"GO FORTH, MY HERALD. TELL THEM ALL ARE WELCOME."

"Wh-what are you--"  #{italic}#Screams in the background.  Gurgling.  Crashing.  A distant, bestial roar.#{normal}#

"AMAKTHEL WILL REWARD YOU FOR YOUR SERVICE AS YOU DESERVE." More crashing.  "YOU SHALL BE BLESSED WITH A BETTER NEW FORM.  A BETTER NEW MIND.  ALL YOUR PEOPLE ARE WELCOME TO..."

#{italic}#(You hear Parmor's voice again.)#{normal}#  "Slag it, RUN!  Grab everything and--"  (The recording ends.)
]], [[“……为了繁荣！让我们用声音记录下，这个值得被子孙后代铭记的，改变历史的时刻！”你又听到了坦塔洛斯议员的声音……但你还听到了另一个奇怪的声音，一个清晰的声音。尽管是机器在播放着声音，但这段声音就像是从你的脑海里传来的一样。#{normal}#

“是的，是的，这是一个好主意。这将会是一个重要的日子，对我们——不，对整个埃亚尔都值得铭记……那么，你今天把我一直以来都要的东西带来了？”

“当然了！它就在——来啊，把车推上来！”（叮叮当当的声音）“如果您乐意的话，请你亲自打开看一下。”

“不用了。我能感受到它的力量，多么熟悉而又新鲜的力量……这只能是阿马克泰尔本人的眼睛！它是多么的令人沉醉啊，很快，所有人都会感受到它的美丽…”

“呃……太棒了，我保证！这将会是气之部族和……你的人民之间漫长而友好的友谊的开始！我这就回去告诉他们，我们已经准备好了，并且你也准备好处理兽人问题了，对吧？他们，啊，一定会很愿意亲自来这里——”

“去吧。我的传令官。告诉他们，我十分欢迎你们。”

“你，你在——” #{italic}#传来一声声尖叫。血液流淌之声。猛烈的撞击声。然后是一阵遥远的，野兽般的咆哮。#{normal}#

“这是阿马克泰尔在亲自奖励你对他的服侍，是你所应得的荣耀。”更多的撞击声。“这是神给你的祝福。一具更美好的全新的身躯。一个更美好的全新心智。你的人民都可以得到这份…”

#{italic}#（你听到了帕默的声音。）#{normal}#  “操，大家快跑！带上所有东西，快——”（纪录终止了）
]], "_t")
t("strange black disk (3)", "奇怪的黑色碟片 (3)", "_t")
t([[#{italic}#(You hear loud, mechanical rumbling; in the distance, you hear sounds of struggling and bludgeoning, swords slicing through flesh, steamguns being fired, and shouts of pain from giant and horror alike.  Parmor sounds panicked.)#{normal}#

"Mayday, mayday, we are bailing out!  Tantalos is gone, and we are NOT going back for him!  Scrap the tunnel to the Palace of Fumes, scrap the entire damn council, we're getting as far away from here as we can--"  Loud hissing.  "MOTHER OF--!"  Grunts, squishing, slashing.  "Flooring it all the way to the damn Sunwall, we're taking the first farportal off this continent whether those tinies like it or not!  Guess this technically counts as treason, mutiny, whatever, but if the Council's hearing this, BLOW IT OUT YOUR STEAM-HOLES, WE'D RATHER LIVE!  Altitude rising, surface approaching, this is H.C. Parmor signing off--"]], [[#{italic}#（你听到了巨大的，机械的轰鸣声。在远处，你听到挣扎和殴打的声音，听到利刃刺破血肉，蒸汽枪的枪声，以及巨人和恐魔发出的痛苦怒吼。帕默的声音听起来惊慌失措。）#{normal}#

“求救，求救，我们在撤离！坦塔洛斯完蛋了，我们绝对不会再回去救他的！去你妈的烟雾宫殿的隧道，去你妈的天杀的议会，我们必须赶紧跑，越远越好——”巨大的嘶嘶声。“狗娘——！”撞击声，挤压声，破碎声。“给我朝太阳堡垒前进，我们要使用这个大陆上的第一个远行传送门，不管你们这些家伙喜不喜欢！我可不管这是不是什么叛国、谋反，去他妈的，如果你们议会在听着的话，放你娘的蒸汽孔，老子只想活下去！海拔上升，准备接近地面，这里是 H.C. 帕默，播报完毕——”]], "_t")
t("erratic scribblings", "潦草的字迹", "_t")
t("why is it down there why is it ANYWHERE", "它为什么会在下面？它为什么会出现在任何地方？", "_t")
t("If anyone finds this, tell the Jarsovi brothers their father lov", "如果有人能找到这张纸，请告诉贾索维兄弟，他们的父亲爱…", "_t")
t("Too many of them.  Couldn't pull more Atmos back in, wasn't safe, couldn't tell them from the others.  Hope we've got enough fuel to get us to the surface.", "他们太多了！我们没法救回更多的同胞，这太危险了，已经没法把他们和那些家伙分开了。希望还有足够的燃料让我们可以钻出地面。", "_t")
t("What have we done...  why didn't I stop it?", "我们到底做了什么…为什么我没有阻止这一切！", "_t")
t("nothing living should have that many", "任何生物都不应该有这么多只…", "_t")
t("so that's what it looks like.  what THEY look like.  now I see why so many depictions were destroyed", "所以这就是它的样子。这就是它们的样子。我现在知道为什么，有关它们的记录都被摧毁了。", "_t")
-- untranslated text
--[==[
t("G.E.M", "G.E.M", "newLore category")
--]==]


------------------------------------------------

section "tome-orcs/data/lore/misc.lua"

t("sunwall observatory", "太阳堡垒瞭望台", "newLore category")
t("an astronomer's journal", "观星者的日志", "_t")
t([[The strange movement on the far side of Wintertide continues - a shadow here, a tiny speck or flash of light there.  Still obscured and difficult to identify.  Obfuscating magic is likely at work, but whether it's on our end or Wintertide's, I cannot say.

The nebula behind the Neira constellation continues its slow fading.  Star Gerlyk-P is gone now too, and by most current models, Amakthel-N will be next.  If the last century is any indication, the rate of disappearances is accelerating...  this is most worrying, but what may be more worrying is that Star Quekjora-B has reappeared in an abrupt flash of light, powerful enough to illuminate the night sky for a brief moment.  It is oscillating between green and purple now, a far cry from its original glow of pale orange, and does not quite seem to be spherical...  I can feel its power from here just like I can Shandral or our two moons, dimly but growing stronger.  It's impossible to meaningfully speculate on something so unprecedented, so I will not write my theories down here, but none of them are reassuring.

Aside from these phenomena, all is normal.  The cracks on Mal'Rok and the other Spellblaze-blasted planets in other systems are still slowly fading, and the lights on more distant worlds continue to twinkle.  Stars outside the Neira constellation remain steady, or decay according to standard astronomical models.]], [[在霜华之月背侧，奇怪的运动还在持续——这里是一处阴影，那里是一个小小的斑点或闪光。影像模糊不清，难以分辨。可能是因为某种魔法的干扰，但这到底是在我们这一端，还是霜华之月的那一端，我也没法判断。

尼耶拉星座的星云继续着它慢慢消散的过程。盖里克-P星消失了，根据目前的模型计算，阿马克泰尔-N将会成为下一颗消失的星星。根据这个世纪以来的记录，星星消失的速度正在加快……这是十分令人焦虑的情形，但更让人焦虑的是奎克久拉-B星重新出现，化成了一团爆发性的闪光，这强大的亮光将整个夜空都照亮了一小段时间。它的颜色现在在正在绿色和紫色之间震荡，和它原来淡橙色的亮光完全不同，而且，它看起来甚至已经不像是球形……我甚至在这里就能感受到它的力量，就像我感受到的山德拉和我们的两个月亮的力量一样，虽然朦胧，却变得越来越强大。我们完全没有办法对这样史无前例的事件进行任何有意义的解释，所以我不准备在这里写下我的理论，但这些假说每一个都让我充满忧虑。

除了这些奇怪的现象之外，星空中的一切其他东西都很正常。玛·洛克以及其他星系里被魔法大爆炸轰击的行星上的裂缝，仍在慢慢消散。来自更加遥远星球的光亮正在闪烁。尼耶拉星座之外的群星仍然保持稳定，或者按照标准天文学模型的解释慢慢消失。]], "_t")
t("ureslak's lair", "乌瑞斯拉克的巢穴", "newLore category")
t("a note lying in a puddle", "水坑里的纸条", "_t")
t([[If you think I'd just leave my plans lying around for anyone to find them, you're an even greater buffoon than Rak'Shor's followers.  You, unlike them, are of no use to me.  [b]Die.[/b]

[i](The bottom half of the paper is illegibly smudged, on account of water dripping onto it from a stalactite above, but has the approximate shape of an explosive-rune trap.  You drop the note, wary of any lingering power it might still have.)[/i] ]], [[如果你以为我会把我的计划写在纸条上，让其他人找到它们，你就是比拉克肖的追随者还要可笑的小丑。不过你和他们不一样，你对我没有任何用处。[b]去死吧！[/b]

[i](这张纸的下半部被弄脏了，难以辨认，看来是上方的钟乳石柱滴下的水弄潮了这张纸。但你可以依稀看到一个爆炸符文陷阱的形状。你赶紧把纸条扔在了地上，生怕在它上面还有什么挥之不去的力量。)[/i] ]], "_t")
t("var'eyal", "瓦·埃亚尔", "newLore category")
t("dropped demonic orders", "掉在地上的恶魔指令", "_t")
t([[I'm not going to lie to you: things aren't going great.  Between the Doomelf escape incidents, the deaths of Khulmanar and a great deal of our more expensive combatants at the hands of the Anomaly, and the disappearance of the First Duathedlen, we've been set back pretty far this year.  As such, your orders are simple: lay low.  Stay out of sight, and conduct passive observation until we can get a foothold and a new plan.

And regarding the First Duathedlen - quit your murmuring right now.  I've seen his track record, and I know most of you know it too, which is why we can safely say that despite his... nature, his loyalty is [b]not[/b] in question - we can assume his abrupt cessation of communication is a necessary part of his investigations, and not him going rogue.  If you see him, tell us of his whereabouts, but do not interfere.

[i](The letter is signed with an unreadable but formal-looking demonic seal.)[/i] ]], [[我准备实话实说：事情的进展并不顺利。除了魔化精灵的逃亡事件之外，还有库马纳的死，我们众多精英卫兵在那场异常中的牺牲，以及第一位多瑟顿的失踪…我们今年的损失已经够严重了。所以，给你们的命令很简单：保持低调。远离敌人的视线，进行被动的观察，直到我们可以获得一个新的立足点，开展新的计划。

还有，有关第一位多瑟顿的事情——你现在就别抱怨这些了。我看到过他的记录，我知道你们大部分人也都看过，这就是为什么我可以放心的说，尽管他的…本性如此，但他的忠诚是[b]无可挑剔[/b]的——我们可以假定，他的突然失联是他进行的调查的一个重要组成部分，而并不是他叛逃了。如果你看到了他，请告诉我们他的位置，但千万不要干涉他的行动。

[i]（这封信是用一个难以辨认，但看起来很正式的恶魔印章签署的。）[/i] ]], "_t")
t("bootlegger's complaint letter", "私酒贩的抱怨信", "_t")
t([[Look, I know the whole point of this market was to make a place for ANY sort of open trade, without the Allied Kingdoms' scryers breathing down our necks, and I know it's not exactly feasible to set up another portal off the continent...  but do you have any idea how bad it is for business to have the slavers using this with us?  Nobody's going to want to have a nice mug of unregulated-strength ale or pick up a shiny new stolen necklace when, not ten yards away, some helpless person is being led away in chains and wailing in misery.

I'm telling you, ditch the slaves and you'll be bringing in ten times as many patrons for everything else.  Whatever your boss is paying you for the slaves, you'll make more than that - and if you're using the manual labor for yourself, just use the excess funds to buy golems!  Win-win decision, in my opinion.]], [[听着，我知道这个市场建立的目的是为了为[b]任何[/b]自由贸易提供平台，而不会被联合王国的探子抓个正着。我也知道，在这个大陆上建立另一座传送门并不可行……但你知道，让这些奴隶贩子会给我们的生意带来多坏的影响吗？如果在不到十码之外，就有一个无助的人被镣铐拖着，发出痛苦的哀嚎，我想是没有客户会愿意在这种环境下美美品尝一大杯不受管制的烈酒，或者仔细挑选闪闪发光的赃物项链的。

我告诉你，只要放弃那些奴隶的生意，你们在其他任何领域，都会迎来现在十倍那么多的顾客。不管你的老板因为奴隶的事情给你多少钱，你肯定可以赚得更多——如果是你自己需要更多劳力的话，干嘛不用这些多赚来的钱买点炼金傀儡呢！依我看，这是双赢的选择。]], "_t")
t("wand-smuggler's apology letter", "魔杖走私犯的道歉信", "_t")
t([[My sincerest apologies, Admiral.  I received the conjuration wands in bulk, and I had no idea that several of them were merely wands of trap destruction - testing each one would have drained some charge from each, providing an inferior product.

I will be retrieving what portion of the cheerblossom I can get from my deceptive supplier, or her head - whichever you would prefer.  At that point, I will ask that you please consider revoking my banishment from your marketplace.]], [[我很抱歉，海军上将。我上周进货了大量的魔咒魔杖，但我也不知道，这里面居然有几个是陷阱拆除魔杖——你看，如果我每个都亲自测试一下的话，就会消耗它的充能，降低产品的品质，对吧。

那个骗了我的该死的供货商，我会亲自从她那里，拿到你想要的鼓舞之花，或者干脆把她的项上人头拿来——你想要哪个都行。看在我的诚意的份上，请可怜可怜我，撤回把我赶出市场的决定吧。]], "_t")
t("slaver's inquiry", "奴隶贩子的提议", "_t")
t([[The anti-scrying nexus you folk set up here is damn impressive, as is the time-release pseudo-rune powered by it - hard to find a spare spot on my skin for it, but I can feel it working for a few days after I'm back in Maj'Eyal.  Great for making sure we can get away from the West portal and disperse without the A.K. catching on or tracking us to a common point of convergence.

Got a proposal, though.  With a few little tweaks, I could make one that doesn't require the bearer's consent to use.  You aren't the only ones buying slaves from me, and when I get a customer who wants them taken right back to the West, we have to do the anti-scrying enchantments ourselves.  I don't know if you've noticed, but proper mages still aren't easy to come by - I barely made a profit last time I did it.

Say the word, and I'll send over the temporary rune design so you can set the nexus to recognize it.  No charge from me - if you accept it, it'll pay for itself.

[i](You assume the elaborate, glowing shape below is an Ogric equivalent to a signature.)[/i] ]], [[老兄，你们设置的反侦测水晶真他妈够劲的，还有这个被它驱动的延时释放的伪符文——我的皮肤上没有什么空位了，但我能感受到，这玩意儿在我回马基埃亚尔之后几天都能用。这肯定能保证，我们可以安心从西部的传送门逃走，绝对不会被联合王国抓到，他们也肯定没法追踪我们的痕迹。

现在，我现在有一个想法。只要稍微整一下，我就可以让这玩意儿不需要使用者的意愿就能工作。你不是唯一一个从我这里买奴隶的人，要是你想把他们带回西部去的话，我们可得好好做点反侦测的准备。我不知道你有没有注意到，但合格的法师如今还是很难请到——上次，我差点把老本都给赔光了。

只要你一句话，我就把这个临时的符文设计发给你，你设置好水晶就能用了。我不收你的钱——只要你愿意用，这笔投入很快就能回本。

[i]（你猜想，下面画着的这个精心设计的，闪闪发光的图案，在食人魔文化里有着和签名一样的用途。）[/i] ]], "_t")
t("STOP BLOWING OUR COVER", "别再暴露我们的身份了！", "_t")
t([[We get it: it's our fault the farportal mailing system isn't perfect.  Our people are still working on undoing that jury-rigged configuration that keeps your portal from transporting anything that isn't living - and if we get it wrong, that means people start getting teleported into walls again.  It's already a damn miracle you can get through the portal without coming out naked on the other side, let alone still carrying your backpacks and all their contents.

In the meantime: we're still losing a few letters going through the mailing system, and the lost ones could end up teleported to pretty much anywhere.  They could end up ten feet from the portal, or they could end up right in some A.K. busybody's hands, or they could just warp themselves right up Urh'Rok's nose for all we know.  Likewise, anything written on those notes could end up exactly where you don't want them, wherever that might be.

My point is, when you're writing those letters, write them like King Tolak's looking over your left shoulder and your grandmother's looking over your right - or at least show SOME semblance of subtlety.  Don't complain about the prices of "illegal potions," complain about "extra-strength medicine."  Don't ask about safety accommodations for "slaves," ask about "private servants."  And please, for the love of Linaniil, [i]stop calling the farportal a farportal![/i]  The A.K. doesn't even know we [i]have[/i] this thing yet, and we don't want to give them any ideas on where or how to start looking.  Call it a courier, or a pack golem, or a trained uruivellas for all I care.

-Korbek

PS: Yes, I'm breaking my own rules with this letter - you idiots clearly don't understand subtlety, so I can't assume you'd understand a subtly-written letter.  Yes, I'm aware there's a chance this letter could end up in enemy hands.  No, the irony of that situation would not be lost on me.  Yes, I will hurt whoever thinks they're clever by bringing up any of the preceding.]], [[我们知道：远行传送门邮递系统并不完美这件事当然是我们的过错。我们还在努力修复那个让传送门无法传送任何非活物的临时配置——如果我们搞砸了的话，那么很快就会又有人被传送到墙里了。你能够这样穿过远行传送门，而不是裸体出现在另一边，包里的东西都完好无损，已经他妈的是一件奇迹了，好不好。

与此同时：我们的邮递系统仍然会丢失几封信，这些丢失的邮件可能会出现在任何地方。据我所知，可能会出现在传送门十英尺以内的地方，也有可能出现在某个联合王国好事者的手里，还有可能出现在乌鲁洛克的鼻子底下，都有可能。也就是说，你写的每一封信都有可能出现在你最不希望出现的地方，不管那是多么遥远的地方，明白吗。

我想说的就是，当你写信的时候，请你想象一下，托拉克国王就在你左边看着，你奶奶站在你右边看着——或者，至少你得明白什么叫隐晦一点，好吗？别再抱怨“非法药剂”的价格了，你能说“大力药”吗？别再讨论使用“奴隶”的安全设施了，可以用“私人仆人”这词吗？还有，拜托，为了莱娜尼尔的爱，[i]别再把远行传送门叫做远行传送门了，好吗！[/i]联合王国甚至还不知道我们[i]有[/i]这个东西，可以不要再给他们侦查的线索了吗？随便你叫他什么，快递员，邮递傀儡，训练好的乌尔维拉斯，随你怎么说都行，拜托了。

——库贝克

注：是的，我知道我自己这份信打破了规则——你们这些白痴连隐晦的重要性都不知道，我怎么指望能用一份隐晦的信让你们明白？是的，我知道这份信也有可能落到敌人手里。不，别指望你能用这个场景的讽刺性来笑话我。是的，谁敢列出以上我所说的任何一条，来显示自己很聪明，我就打烂你的嘴。]], "_t")
t("severed hand", "断手", "_t")
t([[[i](You see here a rotting human hand in a black leather glove, severed at the wrist.  It is still clutching a cracked artifact resembling an Orb of Many Ways, with a note folded up between the orb and its palm.)[/i]

"Drew the short straw" for the calibration [i]my entire ass.[/i]  That cheat used translocation magic and everyone there knew it.  If there's one thing I miss about the Ziguranth, it's that with them around, you only had to watch for sleight-of-hand and wear a mind-caging cap to avoid getting ripped off.

Speaking of ripoffs, why are we trusting this corpse-lover anyway? I guess it WOULD cost more to make a fake this convincing than we paid for it, but...  why would Tannen have made a portal that only works on the living, then used it to pay off a necromancer, [i]the only type of person who'd call that a downside?[/i]

Well, I guess that's what made him a [i]mad[/i] alchemist, and not some rich potion-brewer living comfortably.  Not like anyone can ask him now, except for who we got this altar from.

Anyway...  Korbek, if you're reading this, it means those crotch-heights screwed up again.  Send them back the orb, and hopefully it'll tell them what they need (well, as far as I'm concerned, [i]hopefully[/i] it'll blow them apart).  You got the calibration right on your end, and your poorly-disguised thugs are doing just fine (and stop with the illusions, it's just insulting, we don't care who or what you are as long as your gold glitters).  We just need to get the signal lock straight on our side, and we'll be able to fill the order you sent over, and then some.

Seriously, though, I'm writing this note so even if I get killed from this, I'm doing you a favor.  If I'm dead, I'd appreciate you showing your gratitude by making sure that ankle-biting son-of-a-ritch has played his last game of musical straws.
]], [[[i]（你看到了一只被黑色皮手套包裹的腐烂的人手，手腕被切断了。它的手里拿着一个破碎的神器，样子就像是多元水晶球，水晶球和它的手掌之间夹着一张纸条。）[/i]

“抽到签的人负责矫正传送门”[i]我的屁股[/i]。大家都知道，那个作弊的家伙肯定使用了换位魔法。如果说我有什么怀念伊格兰斯的地方的话，那就是如果他们还在，你只要能看穿那些家伙的手上功夫，戴上一顶抗精神攻击的帽子，就不会被人狠宰一通。

说到宰人，我们干嘛要信任那个恋尸癖？我知道，如果真的是造假的话，以我们所付的代价，这造假的成本未免也太高了，但是……为什么泰恩在制作了一个只能用来传输活物的传送门之后，把它交给了一个死灵法师来偿债，[i]这是世界上唯一一个会把这件事看做致命缺陷的家伙？[/i]

好吧，我知道，这就是为什么他是一个[i]疯狂炼金师[/i]，而不是一个安居乐业的普通药水贩子。而且，除了我们拿到传送祭坛的那个家伙，也没有人能亲自去问他。

不管怎么样……库贝克，如果你读到这份信的话，说明那些缩头缩脑的死矮子又搞砸了。把水晶球交回给他们，希望这里面能够记录下他们所需要的信息（好吧，如果要我说的话，[i]希望这东西把他们全炸死[/i]）。你那边的校准没有问题，并且你那些伪装地很差的暴徒干的也不错（别再放幻术了，这简直是一种侮辱。只要你们肯出钱，我们根本不关心你是谁或者是什么。）我们只需要把我们这边的信号锁调准，就可以完成你送过来的请求，甚至更多。

不过，说真的，我写这份信，是为了确保即使我在这个过程中死了，我也能够为你做一些事。如果我真的死了，希望你确保那个里奇养的小瘪三，是最后一次在抽签的时候玩他有趣的出千游戏了。对此，我会非常感激的。
]], "_t")
t("?...secar", "？……族种", "newLore category")
t("stnaiG maetS :84 retpahC ,seicepS eht fo tnemssessA s'tonyarG ralohcS", "人巨汽蒸——章八十四第——查调的种人于关特诺雷格者学博", "_t")
t([[.elpoep sih yduts ot ecneserp ym detseuqer eh dna ,htiw railimafnu erew elpoep sih seiceps eht lla fo weivrevo cisab a mih evig ot sgnitirw ym nwohs saw flesmih sorysaK rolicnuoC dnarG ,yletanutroF  .tsaE eht ot latrop eht esu ot nailivic a rof elbissopmi ylraen s'ti ,yaw rehto eht kool ot sdraug eht ebirb ot dlog hguone htiw tnahcrem a ro ,kaloT gniK fo evitaler doolb a ,nezitic llawnuS a er'uoy sselnu taht smees ti - hcraeser ym tcudnoc ot em rof reisae yna ti edam ytimixorp eht taht toN  !seson ruo rednu thgir ylraen gnidih saw noitazilivic decnavda na hcus kniht oT

.maets dezirusserp fo tsrub ro maerts a stime ,hctaw ot gnitrecnocsid rehtar gnieb ot noitidda ni ,hcihw ,ylediw dnetsid ro tuhs laes ot meht lliw nac yeht tub ,lla ta gnihton ro tsim eltneg a rehtie time dna elbisivni ylraen era yeht tser ta ;siht revo lortnoc suoicsnoc detimil evah yehT  .maets dezirusserp gnittime fo elbapac era hcihw stnev dna serop suoremun sah niks rieht - deman era yeht hcihw rof ,maets rieht ylniatrec tsomla si tiart lacisyhp gnihsiugnitsid tsom riehT  .(arakiaD fo stnaig gnorts ylevitpeced tey ,ylgnag eht ot tsartnoc ni) edis ykcots eht no ylthgils dna llat teef 01-8 yeht erew ,ekil kool dluow snamuh tahw ot ralimis ylgnikirts era stnaiG maetS

.ti htiw hcum os hsilpmocca ot meht rof ysae os ti edam taht ytilauq evitiutni siht si ti spahrep ;gnihtaerb sa stnaiG maetS eht ot yllarutan sa semoc taht tnemtsujda dna noitnetta seriuqer dohtem siht tub ,retaw liob ot ecanruf a gnisu yb deveihca eb yllaciteroeht nac tceffe ralimis A  .snoitpartnoc xelpmoc erom dna erom ereht morf dna ,renaelc-enots dezirusserp fo tros a derevocsid yeht ,ereht morf ;eltsihw elpmis a saw "hcet-maets" fo tib tsrif eht taht mialc yeht ,sretsasid rehto dna serif lanoisacco ot tsol neeb evah stxet tsedlo 'stnaig eht hguohtlA  .snoitpartnoc cillatem fo yarra ediw a etarepo dna rewop ot maets siht esu ot woh tuo derugif evah yeht ,ylsuoinegni rehtaR

 (.scrO neeb evah yltnecer tsuj litnu srobhgien ylno rieht sa gniees ,weiv elbadnatsrednu yleritne na si sihT)  .tnasaelpnu dna hsiroob eb ot "secar ressel" eht dnif ylerem ot demialc ot ekops I somtA rehto eht fo tsom ,sredistuo ot od dluoc noitnevretni sselerac rieht tahw dna ,meht ot od dluoc dlrow edistuo eht tahw htob fo raef ot eud saw siht smialc sorysaK rolicnuoC dnarG elihw ;muminim a ot secar rehto htiw snoitcaretni rieht tpek evah yehT  .meht detacidare evah dluow ylerus ti taht rebmun ni wef os dna detartnecnoc os erew yeht rof ,yleritne meht dessim ezalbllepS eht taht meht rof etanutrof ylurt si ti ;sega rof sniatnuom krolC eht ni neddih evah ebirT somtA eht fo stnaiG maetS ehT

.detsat reve evah I ehtnisba tseb eht ekam ot woh denrael evah yeht taht eton laiceps ekam tsum I leef I ,esnes retaerg a ni elpoep somtA eht no stcelfer ti woh yas tonnac I hguohtlA  .("devlovni lla rof gnissarabme ylpeed saw" em llet ylno dluow sorysaK hcihw ,ramalgarT gniK rednu doirep feirb a morf edisa) tropsdoolb dna ycarcomed neewteb esimorpmoc tnerappa na yb nesohc si ,ylgnidrocca ,tnemnrevog riehT  .stnev s'eno morf maets erom tuo ecrof ot elba gnieb ylpmis RO noitcurtsnoc tneiciffe erom hguorht lufrewop erom edam eb nac hcet-maets taht tcaf eht ot gniwo spahrep ,stiusrup lautcelletni sa hcum sa yltcaxe tsomla ssentif lacisyhp eulav yeht taht si ees ot elba saw I gniton htrow thgisni repeed ylno eht ;yats feirb ym gnirud yteicos siht ezylana ylluf ot epoh ton dluoc I  .evitcepsrep hserf emos snezitic sih tnarg ot smodgniK deillA dna llawnuS eht htiw edart nepo nugeb sah ohw ,sorysaK ot gnidrocca ,ytilaer ot noitcennocsid dna yrtsihpos fo niarts a deretsof osla sah ti ,poleved yteicos rieht tel ot ecaep meht nevig sah noitalosi siht elihW

.emoc ot ega na rof su htiw seilla gnirudne eb lliw yeht taht derusne sah [b]SNEVAEH EHT FO REGAVAR TNEDUPMI ,SUTALOMMI[/b] reednammoc ot stpmetta s'redael rieht gnitrawht dna noillebeR kurK eht gnihsurc ni pleh riehT  .sevlesmeht rof seitic rieht ees ot dewolla eb noos lliw flesym naht rehto sredistuo spahrep dna ,nosrep ni meht fo erom teem ot ytinutroppo eht niag noos lliw ew ,spihsria morf deppord stcurtsnoc aiv enod llits si somtA eht htiw tcatnoc ruo fo tsom hguohtla ,esac eht revetahW  ?sesoprup lasopsid rof latropraf yrotarolpxe na gnisu tuoba gnihtemos - layE'jaM fo oreH eht htiw gniteem a degnarra sah eh rof ,regnol yna em ynapmocca tonnac eh em sllet sorysaK  .siht naht erom nrael ot hguone gnol rof meht yduts ot elba ton saw I ,salA]], [[。人族的他究研自亲我请邀他，在现。族种多众些那的悉熟不所人族的他上界世个这解了以用，书的我过读经曾人本长议斯罗西卡，是的运幸。会机的东远往通门送传古远用使何任有没乎几，民平的样这我像，则否。面一开网兵卫赂贿钱的够足用能，商富的贯万缠腰是者或，戚亲的人本王国克拉托，民公的垒堡阳太是你非除——便方么什供提究研的我给有没并，近接的样这间之们我，而然！明文的达发度高个一样这着藏然竟，下底皮眼的们我在就，吧看想想

。安不人令为颇来起看景场的样这，汽蒸压高团一或流气股一出放，口气排张扩或闭封动主以可也们他，是但。到不看也么什脆干者或，雾薄的柔轻到看稀依能只，的见可不是常通为行气排的们他，候时的息休在；制控动主的限有行进为行的气排对以可们他。汽蒸的压高出排中从以可，口风通和孔毛多许有上肤皮的们他——因原的人巨汽蒸为名命被们他是就这，汽蒸的上身们他是征特貌外的性志标具最们他。比对的明鲜了成形人巨的壮强地料意人出但高瘦些那拉卡岱与这，胖矮显稍材身，尺英01-8高身们他，似相地人惊类人与来起看人巨汽蒸

。西东的多样这现实汽蒸用地松轻此如以可们他让，觉感的观直种这为因是正，许或。单简样一吸呼同如都说来人巨汽蒸于对切一这而，汽蒸制控、注关细仔者作操要需种这过不，果效的似类到达，汽蒸生产以可也水热加来子炉用使，上理原。置装的杂复越来原列系一了明发渐逐后然，法方的面表体物洁清汽蒸压加用使了明发们他，后之此在。子哨的单简种一是只”技科汽蒸“的早最，称声们他，了毁摧害灾的他其和灾火的然偶被录记字文的早最们人巨些这管尽。法方的置装属金的样各种各纵操和动驱来汽蒸股这用使了到想地妙巧当相们他

（法看种这的们他解理以可全完我，人兽是就居邻的一唯们他，前之久不到直到虑考）。已而快不人令又野粗又”族种等下“些那得觉是只们他，法说的人的族部之气他其从我照按但，响影的样怎来带人的界世面外给会能可明发的慎谨不们他怕害也，胁威的成造们它对能可界世部外怕害既们他为因是这，法说的长议斯罗西卡照按。度限低最到低降动互的间之族种他其与将力尽们他。们他绝灭全完会怕恐害灾的样这，少稀么这是又口人，中集此如境环存生的们他到虑考，响影的炸爆大法魔到受未从们他，是的运幸；纪世个几了匿藏中脉山克拉克在人巨汽蒸的族部之气

。术技的酒艾苦的好最的过尝所我造酿着握掌还们他，句一提别特要必有还我得觉我，质品要重种某的人族部之气了映反否是这道知不我管尽。（“的尬尴当相是都说来员人关相有所对事件这”，我诉告只斯罗西卡，期时暂短的治统玛拉格拉特王国了除）的来出拔选度制的成而合结技竞腥血和制体主民由种某过通是，府政的们他，此因。量力体肉的大强，的汽蒸多更出喷中孔气排从够能于自来以可[b]也[/b]，计设的效高巧精于源来以可仅不，量力的技科汽蒸的们他，为因是这许也。要重样同求追的慧智对和的看壮健体身将们他是就，素因层深的中会社们他，的到意注够能一唯我，此因。会社的们他析分入深够能间时有没并，会机的里这在留停暂短有只我于由。角视新全的题问待看些一来带人族的他给能望希，易贸放开的间之国王合联与垒堡阳太和了始开近最他，此因。想思的实现离脱，辩诡导倡中会社们他了长助也时同这，间空平和的要需所展发会社们他了给绝隔的界外和管尽，法说的斯罗西卡照按

。友盟的愧无之当中间时段一来未们我是会将们他，明证们我向经已，献贡的出作所中[b]者虐肆空天的耻无，地动天撼[/b]占强袖领的们他止阻及以，乱叛克鲁克碎粉在们他。市城的丽美们他问访自亲可许被，者访来的外之我了除有会还来未，许也。会机的触接面对面们他多更和得获会就快很们我，置装的来下掉上艇飞从是就，道渠的通沟的一唯间之族部之气和人分部大们我管尽，样怎管不？理清圾垃行进来门送传古远险探用使关有是像好——会聚场一了好排安经已间之雄英的尔亚埃·基马和他为因，了我陪再能不他，我诉告斯罗西卡。了些这有只现发的我以所，间时的长够足们他究研会机有没我，唉]], "_t")
t("races...?", "种族……？", "newLore category")
t("Scholar Graynot's Assessment of the Species, Chapter 48: Steam Giants", "博学者格雷诺特关于人种的调查——第四十八章——蒸汽巨人", "_t")
t([[To think such an advanced civilization was hiding nearly right under our noses!  Not that the proximity made it any easier for me to conduct my research - it seems that unless you're a Sunwall citizen, a blood relative of King Tolak, or a merchant with enough gold to bribe the guards to look the other way, it's nearly impossible for a civilian to use the portal to the East.  Fortunately, Grand Councilor Kasyros himself was shown my writings to give him a basic overview of all the species his people were unfamiliar with, and he requested my presence to study his people.

Steam Giants are strikingly similar to what humans would look like, were they 8-10 feet tall and slightly on the stocky side (in contrast to the gangly, yet deceptively strong giants of Daikara).  Their most distinguishing physical trait is almost certainly their steam, for which they are named - their skin has numerous pores and vents which are capable of emitting pressurized steam.  They have limited conscious control over this; at rest they are nearly invisible and emit either a gentle mist or nothing at all, but they can will them to seal shut or distend widely, which, in addition to being rather disconcerting to watch, emits a stream or burst of pressurized steam.

Rather ingeniously, they have figured out how to use this steam to power and operate a wide array of metallic contraptions.  Although the giants' oldest texts have been lost to occasional fires and other disasters, they claim that the first bit of "steam-tech" was a simple whistle; from there, they discovered a sort of pressurized stone-cleaner, and from there more and more complex contraptions.  A similar effect can theoretically be achieved by using a furnace to boil water, but this method requires attention and adjustment that comes as naturally to the Steam Giants as breathing; perhaps it is this intuitive quality that made it so easy for them to accomplish so much with it.

The Steam Giants of the Atmos Tribe have hidden in the Clork mountains for ages; it is truly fortunate for them that the Spellblaze missed them entirely, for they were so concentrated and so few in number that it surely would have eradicated them.  They have kept their interactions with other races to a minimum; while Grand Councilor Kasyros claims this was due to fear of both what the outside world could do to them, and what their careless intervention could do to outsiders, most of the other Atmos I spoke to claimed to merely find the "lesser races" to be boorish and unpleasant.  (This is an entirely understandable view, seeing as their only neighbors until just recently have been Orcs.) 

While this isolation has given them peace to let their society develop, it has also fostered a strain of sophistry and disconnection to reality, according to Kasyros, who has begun open trade with the Sunwall and Allied Kingdoms to grant his citizens some fresh perspective.  I could not hope to fully analyze this society during my brief stay; the only deeper insight worth noting I was able to see is that they value physical fitness almost exactly as much as intellectual pursuits, perhaps owing to the fact that steam-tech can be made more powerful through more efficient construction OR simply being able to force out more steam from one's vents.  Their government, accordingly, is chosen by an apparent compromise between democracy and bloodsport (aside from a brief period under King Traglamar, which Kasyros would only tell me "was deeply embarassing for all involved").  Although I cannot say how it reflects on the Atmos people in a greater sense, I feel I must make special note that they have learned how to make the best absinthe I have ever tasted.

Alas, I was not able to study them for long enough to learn more than this.  Kasyros tells me he cannot accompany me any longer, for he has arranged a meeting with the Hero of Maj'Eyal - something about using an exploratory farportal for disposal purposes?  Whatever the case, although most of our contact with the Atmos is still done via constructs dropped from airships, we will soon gain the opportunity to meet more of them in person, and perhaps outsiders other than myself will soon be allowed to see their cities for themselves.  Their help in crushing the Kruk Rebellion and thwarting their leader's attempts to commandeer [b]IMMOLATUS, IMPUDENT RAVAGER OF THE HEAVENS[/b] has ensured that they will be enduring allies with us for an age to come.]], [[想想看吧，就在我们的眼皮底下，竟然藏着这样一个高度发达的文明！然而，我们之间这样的接近，并没有给我的研究提供什么方便——除非你是太阳堡垒的公民，托拉克国王本人的亲戚，或者是腰缠万贯的富商，能用足够的钱贿赂卫兵网开一面。否则，像我这样的平民，几乎没有任何使用远行传送门通往远东的机会。幸运的是，卡西罗斯议长本人曾经读过我的书，用以了解这个世界上他的族人所不熟悉的那些众多种族。现在，他邀请我亲自研究他的族人。

蒸汽巨人看起来与人类惊人地相似，他们身高8-10英尺，身材稍显矮胖，这与岱卡拉那些瘦高但出人意料地强壮的巨人形成了鲜明的对比。他们最具标志性的外貌特征是他们身上的蒸汽，这就是他们被命名为蒸汽巨人的原因——他们的皮肤上有许多毛孔和通风口，可以从中排出高压的蒸汽。他们可以对排气的行为进行有限的主动控制；在休息的时候，他们的排气行为通常是不可见的，只能依稀看到轻柔的薄雾，或者干脆什么也看不到。但是，他们也可以主动封闭或扩张排气口，放出一股气流或一团高压蒸汽，这样的场景看起来颇为令人不安。

他们相当巧妙地想到了使用这股蒸汽来驱动和操纵各种各样的金属装置的方法。尽管这些巨人们最早的文字记录被偶然的火灾和其他的灾害摧毁了，他们声称，最早的“蒸汽科技”只是一种简单的哨子。在此之后，他们发明了使用加压蒸汽清洁物体表面的方法，然后逐渐发明了一系列越来越复杂的装置。原理上，使用炉子来加热水也可以产生蒸汽，达到类似的效果，不过这种需要操作者仔细关注、控制蒸汽，而这一切对于蒸汽巨人来说都如同呼吸一样简单。或许，正是因为这种直观的感觉，让他们可以如此轻松地用蒸汽实现这样多的东西。

气之部族的蒸汽巨人在克拉克山脉中藏匿了几个世纪；幸运的是，他们从未受到魔法大爆炸的影响，考虑到他们的生存环境如此集中，人口又是这么稀少，这样的灾害恐怕会完全灭绝他们。他们尽力将与其他种族之间的互动降低到最低限度。按照卡西罗斯议长的说法，这是因为他们既害怕外部世界可能对它们造成的威胁，也害怕他们不谨慎的发明可能会给外面世界的人带来怎样的影响，但按照我从其他气之部族的人的说法，他们只是觉得那些“下等种族”又粗野又令人不快而已。（考虑到直到不久之前，他们唯一的邻居就是兽人，我完全可以理解他们的这种看法）

按照卡西罗斯的说法，尽管和外界的隔绝给了他们社会发展所需要的和平空间，这同时也助长了他们社会中倡导诡辩，脱离现实的思想。因此，他最近开始了和太阳堡垒与联合王国之间的开放贸易，希望能给他的族人带来一些看待问题的全新视角。由于我只有短暂停留在这里的机会，并没有时间能够深入分析他们的社会。因此，我唯一能够注意到的，他们社会中的深层因素，就是他们将身体健壮看的和对智慧的追求同样重要。也许这是因为，他们的蒸汽科技的力量，不仅可以来源于精巧高效的设计，[b]也[/b]可以来自于能够从排气孔中喷出更多蒸汽的，强大的肉体力量。因此，他们的政府，是通过某种由民主体制和血腥竞技结合而成的制度选拔出来的（除了国王特拉格拉玛统治的短暂时期，卡西罗斯只告诉我，“这件事对所有相关人员来说都是相当尴尬的”）。尽管我不知道这是否反映了气之部族人的某种重要品质，我觉得我还有必要特别提一句，他们还掌握着酿造我所尝过的最好的苦艾酒的技术。

唉，我没有机会研究他们足够长的时间，所以我的发现只有这些了。卡西罗斯告诉我，他不能再陪我了，因为他和马基·埃亚尔的英雄之间已经安排好了一场聚会——好像是有关使用探险远行传送门来进行垃圾清理？不管怎样，尽管我们大部分人和气之部族之间唯一的沟通的渠道，就是从飞艇上掉下来的装置，我们很快就会获得和更多他们面对面接触的机会。也许，未来还会有除了我之外的来访者，被许可亲自访问他们美丽的城市。他们在粉碎克鲁克叛乱，以及阻止他们的领袖强占[b]撼天动地，无耻的天空肆虐者[/b]中所作出的贡献，已经向我们证明，他们将会是我们未来一段时间中当之无愧的盟友。]], "_t")
t("Scholar Graynot's Assessment of the Species, Chapter 83: Wei...", "博学者格雷诺特关于人种的调查——第八十三章——Wei……", "_t")
t("(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)", "（当时空异常从另一条世界线拉入这条纸条的时候，这张纸条突然着火了。你还没来得及看完标题，这张纸条已经被烧得一干二净。）", "_t")

------------------------------------------------

section "tome-orcs/data/lore/palace-fumes.lua"

t("palace of fumes", "烟雾宫殿", "newLore category")
t("a reminder", "一个公示", "_t")
t([[A Reminder to Our Constituents:

Any votes for an individual candidate for office cease to be valid once the primaries are over, and the field has been narrowed down to two (or rarely three, in a close race) candidates.  At this point, you cannot vote for your candidate; instead, a competition will be held, after which its victor will be awarded with the position.  The vote you are submitting now determines how they will be competing.  While we cannot enforce how or why you vote, we request that you respect the spirit of our system, and select a competition which reflects the candidates' capability to handle the responsibilities of the Chief Councilor position.]], [[敬告广大选民：
初选结束后，任何向个人的投票将会不再有效，名额会被削减到两名（如果票数接近，有时会是三名）候选人。在那个时候，您将不能为您的候选人投票；相对应的，将会举行一个比赛，胜利者会获得职位。您现在的投票将会决定他们竞争的方式。我们不能强制要求您投票的方式或动机，但我们仍然请求您尊重我们体制的精神，选择一个能够反映出候选人作为议长履行职责的能力的合适的比赛项目。]], "_t")
t("a wrinkled pamphlet", "一本起皱的小册子", "_t")
t([[A Plea from the Volunteer's Bureau of Gaming:

Once again, we find ourselves faced with an election for the competition of Chief Councilor.  While this is the most prestigious position in our government, it should not be forgotten that is also arguably the most complex, and the one bearing the greatest responsibility for the fate of our people.  A Chief Councilor's duties require not only cautious, reasoned foresight, but a quick wit to get emergencies under control in little time; yet, he or she must be aware of the precedent set or the unintended consequences of such decisive action, never acting rashly or out of ill temper.  Such a leader would wield our citizens and our military like a drunkard with a glass bottle, not caring if his weapon is shattered in the process. He or she must be able to develop creative solutions to problems but be open to outside advice, to be a character judge capable of selecting his or her most valuable acquaintances and a persuader to convince them to do the tasks for which they are most suited...  suffice to say, there are a great many mental skills required.  Accordingly, the competition should be one that tests all these skills.

This election, we are formally endorsing the board game [i]Automobiles and Automatons v9.8,[/i] a refined variant of the game introduced last year in a competition for the Marshall of the City Guard.  Its "oil-punk" science-fantasy setting, although perhaps easy to brush off as irrelevant to our reality, has its own consistent internal rules, forcing its players to learn a new status quo and work with it, as our leaders must be willing to learn from ongoing events and rapidly adapt to them; yet, since the game has been out for a year already and there are already numerous books about strategies for it, it also tests our candidates' long-term memory, as our leaders must be able to remember our history, to repeat our ancestors' successes but not their failures.  The rules of v9.8 are somewhat, but not entirely, different from those of previous versions, making these strategy books only partially accurate, just as our ancestors' wisdom only reflected the world they lived in, not the increasingly different one of the present.

v9.8 uses the "Crumbling Divide" map, providing a barrier that eliminates the possibility of an aggressive player gaining an early victory, tests the players' ability to plan in the long term, and yet due to the presence of non-player foes on either side, they still must be able to make plans in the short-term that will ensure their survival and leave them in an advantageous position when the barrier fades.  Non-player foes follow a predictable set of rules, eliminating luck as a factor, and our necropsychs have found a method of copying the same spiritual consciousness into two figurines, meaning that both players will be using identical sets of Negotiator figurines to demonstrate their diplomatic finesse.  (As always, the figurines are designed to release their spirits after no more than one month, ensuring that this process is as humane as possible to the deceased.)

The consumer edition of this game, v6.0, has won countless awards for its engaging and challenging play, with special attention given to the diverse array of viable strategies and skills tested by it.  Both sides agreed it was a fair game in the Marshall's election, as v1.0; v9.8 is unlikely to disappoint as a method of selecting our next leader.  Vote for [i]Automobiles and Automatons v9.8[/i] this year, and you will not be let down by its winner.]], [[游戏志愿者局的请愿：

又一次，我们面临着选举议长的比赛了。这是政府中最有名望的职位，但也别忘了它可以说是最复杂的职位，承担着我们人民命运的最大责任。一个议长不仅需要谨慎而理性的远见，也需要在短期内解决紧急事态的急智；并且，他或她必须明白这些决定的先例以及非预期后果，行动既不冒进也不出于心血来潮。否则，这样的领袖会像是一个醉鬼拿着玻璃瓶那样，轻率地对待我们的人民和军队，而不关心那武器是否会破碎。他或她必须能创造性地解决问题，同时包容外界的建议，还要做一个知人者，能选出他或她身边最具价值的人才，以及一个说客，能说服这些人去做他们最适合的工作……可以说，成为议长需要很多精神上的技能。因此，这个竞赛必须要考验所有这些技能。

这次选举，我们隆重推出桌面游戏[i]汽车与机器人第9.8版[/i]，一款去年曾用于选出城市卫兵团长的游戏的改良版。它基于“石油朋克”的科幻设定，或许会被认为与现实不符而被人忽略，但它有着它严谨的内部规则，会迫使其玩家学习新的环境并掌握它，就像我们的领袖们也必须愿意从正在进行的事件中学习并迅速适应它们；并且，由于这个游戏已经推出了一年，有无数关于游戏策略的书已经被出版，玩这个游戏也能测试候选人的长时记忆，因为我们的领袖必须得以史为鉴知兴衰。9.8版本的规则和之前的版本略有不同，但却并非完全不同。这样，那些策略书籍仅仅是部分准确的，就像我们祖先的智慧只能反映他们所处的时代，而不是面临巨变的今日。

9.8版本使用“破碎两极”地图，地图中有一个结界，这消除了那些具有侵略性的玩家获得快速胜利的可能性，测试了玩家们长期谋划的能力，而且因为两侧都有非玩家敌人，他们仍然要有短期计划，以保证生存，并在结界消散后占据优势。非玩家的敌人遵循可预测的规则，排除了运气因素，我们的通灵师也找出了一个把相同意识复制到两个模型中的办法，这意味着双方玩家都会使用相同的谈判者模型来体现他们的外交手腕。（和往常一样，这个模型被设计成在使用后一个月内解放里面的灵魂，以确保这一过程对于亡者来说尽量人道。）

这一游戏的消费者版本，6.0版，以它令人沉浸又富于挑战的游戏性已获得了无数奖项，尤其因它不同类型的多变策略，以及其对多种技能的综合考验备受瞩目。在1.0版本的游戏用于选出卫兵队长时，双方都同意游戏是公平的；作为选出我们下一个领袖的方式，9.8版本绝对不会令人失望。今年，投[i]汽车与机器人第9.8版[/i]一票吧，你不会为它的胜者而失望的。]], "_t")
t("a fading poster", "一个发旧的海报", "_t")
t([[Councilor Tantalos, unlike that cowardly wimp Chief Councilor Kasyros, knows just what to do to solve the steam shortages, and isn't afraid to do it!  Even though he can't reveal his plan yet for security reasons, the Geothermal Authority and our military's highest generals have assured us that his plan would work, without requiring us to ration steam usage or regulate our appliances; let's see Tantalos show that old geezer what-for, and end this drought for good!

VOTE FISTICUFFS]], [=[坦塔洛斯议员，不像卡西罗斯议长那位懦弱的窝囊废。他知道该如何解决蒸汽短缺的问题，也不怕去执行这一方案！即使由于安全原因，他现在还不能公布计划，地热局和我们军队高级将领已经向我们保证，他的计划一定会奏效，我们再也无需节省蒸汽用量或是管控我们的器具；让我们看看坦塔洛斯怎样让那个老东西难堪，并永远结束蒸汽枯竭！

[b]请投肉搏战[/b]]=], "_t")
t("Kasyros' resignation speech", "卡西罗斯的辞职演说", "_t")
t([[My fellow councilors,

In this time of increasing vent-drought, it is tempting for us to seek the easy way out.  I understand that at this point, I am powerless to prevent our new Chief Councillor's plans to take the promising vents under the Kruk orcs, but should we fail, you may be tempted to compensate by approaching that...  entity who called itself "the Loyalist."  I am of the opinion that this would be a foolish decision.

Do you remember the Official Histories' record of when we first interacted with the lesser races?  They spoke of them as an entertaining, jovial bunch, friends and companions with our own people.  How naive we were back then...  but when our ancestors saw their true nature, the brutality they were capable of, they recorded these acts in detail.  They did not, however, explicitly tell us not to trust the Orcs.  They did not explicitly tell us that they are pests to be avoided, or a scourge to be eradicated, or a pitiful, fallen reminder of why letting the lesser races use our discoveries will only end in tragedy.  They simply recorded what they learned, and allowed future generations to come to those conclusions themselves, compared with their own observations - and in our grandparents' case, by unfortunate personal experience.  Even through the distress and feelings of betrayal at the time, even though opinions ran in every direction from fury to sorrow at the lesser races' barbarism, not one of the Councilors responsible for recording events gave in to editorialism.  Perhaps we would be in a better situation if they had, so we would have not repeated their mistake of trust, but they stayed fair nonetheless.

Going even further back, they spoke of relations with our now-distant kin, the Sturmos Tribe.  Though the records describe a strained relationship, the mentions of their boorish behavior are recorded in a matter-of-fact nature, and interspersed with the mentions of their advanced metallurgy techniques and other such valuable things we gained from cooperating with them.  Although their current state of Great Firestorm-induced exile to the mountains of Maj'Eyal makes it a rather moot point, the fact still stands that if we were somehow in a position to trade with them, we could rely on the Official Histories for a trustworthy indication of, at a minimum, how they [i]used[/i] to behave.

The examples go on; the Official Histories have remained dispassionate and fair, and a reliable metric for making decisions.  Not once did our forefathers allow their biases to influence their recordings.  Not once did a fervent political movement manage to compromise their integrity.  Not one chapter of these texts can be safely and fully discredited as the subjective, unfair writings of a dominant political party, or the deluded ramblings of a movement influenced by some banal philosophical fad.

(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)

My point is, the Official Histories have a very well-proven track record.  Every single time but once, they have given a solid analysis of the evidence.  Every single time but once, they have refrained from outright suggesting a course of action.  And only once have they allowed something as subjective as a gut feeling into their reports.

Do you know what they say about the meeting with the Loyalist?  After a brief description of the events of the meeting - a strange creature approaching the Council of the time, demonstrating its power by using a small wand to blast a hole halfway to Eyal's core (a wand which he then handed them as though it were a child's cheaply-made toy), stating it could offer us a source of near-infinite energy in return for a rather inconvenient magical artifact.  When they turned it down, the creature gave a speech recorded in verbatim detail: "It hardly matters.  I have all the time in the world to wait for your people to trip over their own hubris and shatter.  If you will not allow me to save you, then I need only sift through the shards of your ruined cities to find it."

Our forefathers say this creature gave them a means of contacting it again, but outright refuse to say what it was; the only reason we still know how to reach it is the yearly messages dropped on the Palace's front steps.  After mentioning that, they wrote this:

"Do not trust this Loyalist.  When we look upon him, we feel something deep within us, older than ourselves, telling us that he is simply... [i]wrong[/i].  His intentions with the Eye, an artifact with incredible power that we have yet to successfully harness, cannot be good for anyone, least of all ourselves.  Never give him the Eye, and continue our work of trying to find a means of destroying it.  Never accept any other deal he offers.  If you are ever unfortunate enough to see him as well, you will immediately understand why we say this."

Perhaps political discourse has gotten a bit...  muddier in recent years.  With the bickering and sniping of modern-day debates, it can be hard to believe that past Councilors had ideas other than their careers in mind, that a vehement display of emotion would be something other than political posturing.  But even if those Councilors were just as petty and selfish as we are, they did not let it affect the Official Histories, not once.

I intend to trust the only advice our ancestors gave us in the Official Histories.  I beg of you all to do so as well.]], [[议员同志们，在这一出气口枯竭加剧的时期，一个简易的解决方法是极具诱惑性的。我明白，目前我已经无力阻止我们的新议长去夺取克鲁克兽人地盘底下的那些有前景的出气口，但是一旦我们失败了，你们也许会试图去接近那个……自称“忠诚者”的个体来补救这一切。我个人认为这会是个愚蠢的决定。

你们还记得，在正史中我们第一次与那些下等种族接触时的记载吗？上面写着，它们是一群有趣又快活的人，是我们的朋友和同伴。我们那时可真是天真啊……但是当我们的祖先们看到了他们的真实本性和他们潜在的残暴之后，祖先们把这些详尽记录下来。然而他们没有明确地告诉我们不要信任兽人。他们没有直接告诉我们这个种族是要远离的害虫，或是一个要消灭的祸害，也没有留下一个可悲的警示，告诉我们让那些下等种族使用我们的发明创造只会导致悲剧。祖先们只是把他们学到的记录下来，让后人对照自己的观察结果，得出自己的结论————这是我们的祖父母辈以不幸的个人经验而体会到的。即使他们悲伤着，感觉到被背叛，即使思绪万千，对下等种族的野蛮感到震怒又哀怜，当时那些负责记录事件的议员们，没有一个抒发个人观点。或许，假如他们愿意表达这种观点，我们可能会处于一个更好的处境，不会再重复他们轻信的错误，不过无论如何，他们仍然保持了公正的记述。

再往前追溯，祖先们谈论过与我们今日的远亲风暴部族。尽管这些纪录中描述了我们与他们紧张的关系，对他们本性中的粗野举动的记述确实完全实事求是的。而且，记录中还提到了关于他们先进冶金技术的论述，以及其他和他们合作获得的好处。尽管一场巨大的火风暴后，他们至今流亡于马基埃亚尔的群山中，让与他们打交道的想法不太可能实现，但如果我们一旦有机会与他们交易，正史还是提供了一个可靠的指示，至少，也能告诉我们他们[i]曾经[/i]如何。

这样的例子还有许多；正史一直以来都是冷静而不偏不倚的，是做决定的一个可靠标尺。前人们从来不让个人的偏见影响他们的纪录。这一纪录的诚实也从来未在狂热的政治运动中妥协。在这些文字中，没有一个章节可以被论定为某个优势政党的主观臆断，或是受某个陈腐的哲学思潮影响的胡言乱语。

（显然，特拉格拉玛王短暂的仁政除外，但是要明白这是特例，不值得进一步讨论。）

我认为正史对以往的事情有非常可靠的纪录。除了一次以外，他们都对证据进行了可靠的分析；除了一次以外，他们都克制住自己，没有直接给出行动方案。只有这一次，他们在报告中透露出了本能感受这样主观的东西。

你们知道他们怎样描述与“忠诚者”的会面吗？简短地讨论了几件事后，那个奇怪的生物接近了当时的议会，用一根小小的魔杖，炸出一个半途通往埃亚尔核心的洞，来展示他的力量（它接下来把这个魔杖随意地交给了议会成员，就像把它当是儿童的劣质玩具），声称它可以为我们提供一个近乎无穷的能源，而他只需要一个令人感到不便的魔法古物为交换。在他们拒绝后，那个生物发表了看法，原文如下：“这不怎么要紧。我有世界上所有的时间等待你们的人民因为自己的骄傲摔得粉身碎骨。如果你不让我来拯救你们的话，我只需要从你们文明的废墟中找到它。”

我们的祖先写下，这个生物给了他们再次与它联络的方式，但祖先们拒绝了写下这一联络方式是什么；我们仍然知道怎样与它联系的原因，在于在一条在烟雾宫殿前门留下的年度总结信息。在提到这以后，他们写道：

“别相信这个‘忠诚者’。当我们抬头看他时，我们感觉到在自己内心深处，有一种比自己要古老的存在，告诉我们他是……[i]错误的[/i]。他对于‘眼’，一个有我们至今没有成功掌控的强大力量的古物，抱着意图，这不可能对任何人有好处。永远别给他‘眼’，而且要继续找到一种销毁‘眼’的方法。永远别接受他给出的其他交易。如果你们有一天也不幸地要见他，你们会立即明白为什么我们这么说。”

或许这几年，政治争端变得有些……令人头脑混乱了。今日的辩论中到处都是口角和中伤，让人很难相信，过去的议员们脑海里会考虑超越他们职业生涯以外的东西，那种激昂的感情表达也不仅仅是政治上的装腔作势。不过即使那些议员们像我们一样器量狭小而自私，他们也未曾影响过正史的记录，一次也没有。

我想要信任祖先们在正史中给出的唯一建议。我也请求你们都这样。]], "_t")
t("excerpts from a Council meeting transcript (1)", "一份议会文字记录片段 (1)", "_t")
t([[The Steam Council has been called to order, with Chief Councilor Tantalos presiding.  

TANTALOS: "Greetings, my fellow- heh, now [i]lesser[/i] Councilors!  It is my pleasure to finally lead the proceedings.  The agenda for today..." Ruffles through papers. "Is irrelevant, for I have a solution to every malady mentioned therein.  The first order--"

KASYROS: "With all due respect, Chief Councilor, the agenda--"

TANTALOS: "Is.  [i]Irrelevant.[/i]  Tormak?  You've been scrying on potential sources of geothermal energy, would you care to inform the others where you see the most potential?"

TORMAK: Sighs. "Right under the Kruk orcs, unfortunately.  It's a promising source for sure, the magma powering it hasn't drained out like it has under us, but digging there would...  well, we all know how quickly they turned construction tools into weapons to rival our own.  If we went in there with the state-of-the-art mining equipment necessary to--"

TANTALOS: Laughter. "Mining equipment!  What manner of fool do you take me for?  Palaquie, tell me what's going through the minds of those silly little waist-height warriors, rummaging through the mainland for Orcish rebels." Holds up hand to silence Councilor Emeritus Kasyros. "This IS relevant, I assure you."

PALAQUIE: "Discontent...  revolving around hidden, long-fermented resentment. Some want the Kruk exterminated, others imprisoned.  Neither can afford direct intervention, but some form of support will assuredly be available."

TANTALOS: "So, with the right negotiation, we can get these tinies, who have [i]endless[/i] experience fighting Orcs, to assist us and make any sort of action in Kruk territory more manageable.  At a bare minimum, we can obtain weaponry that has long proved sufficient for slashing Orcish throats...  although we'll need it custom-fit for our size, naturally."

PALAQUIE: "They have a race whose armor would work.  A tight fit, but sufficient."

TANTALOS: "Even better!  And...  Kasyros, I'm going to let [i]you[/i] tell me what the people care about most.  I'm sure your bruises are adequate reminders of the citizens' will?"

KASYROS: [Statement was deemed excessively profane and stricken from the record by 4-2 vote.]

TANTALOS: "Such undignified conduct!  All because you can't accept that the public wants their steam back.  More than they want those filthy little greenskins around, more than they fear getting their hands dirty, more than they want [i]your[/i] way of doing things.  So!  It's resolved that we have much to gain from this, it's resolved that we have or can obtain the means to carry it out, and it's resolved that it is what the voting public desires.  I see no need for further debate.  Nashal, I'd like to speak to you after this about a wand.  Meeting adjourned."

[At this time, Councilor Kasyros gave a lengthy speech before officially resigning from the Council.  It has been recorded in a separate document.] ]], [[在坦塔洛斯议长的主持下，蒸汽议会正式开会。

坦塔洛斯：“你们好啊，我的同……哈，现在是[i]下级[/i]议员们！这是我的荣幸，能够终于主事。今日的议程……”翻动手中的文件。“无关紧要，因为我已经为所有要解决的问题有了一个对应的方案。首先————”

卡西罗斯：“尊敬的议长，议程————”

坦塔洛斯：“这件事[i]无关紧要[/i]。托马克？你一直在占卜潜在的地热能源，你能告诉大家哪里最有潜力吗？”

托马克：叹气。“不幸的是，就在克鲁克兽人的地盘底下。那确实是个有潜力的源头，提供能源的岩浆可不像我们地盘底下的都枯竭了，但是在那里挖掘会……好吧，我们都知道他们能多快的把建筑工具变成能威胁我们的武器。如果我们把能用来开采的最新式采矿工具带过去————”

坦塔洛斯：大笑。“采矿工具！你把我当成是怎样的傻瓜？帕拉奎，告诉我那些在大陆上到处搜寻兽人反叛者的齐腰高的小傻战士们在想什么。”举起手打断荣誉终身议员卡西罗斯。“我向你保证，这确实相关。”

帕拉奎：“不满……以及隐藏的，长期发酵的怒火。有些人想消灭克鲁克兽人，也有人想监禁他们。不论是那种，我们都没法直接介入，不过确实可以提供某种支持。”

坦塔洛斯：“那么，在恰当的协商后，我们可以让那些有[i]无数[/i]兽人作战经验的小东西，来协助我们，让在克鲁克兽人境内的一切行动更易掌控。最少，我们可以取得那些已被长期证明能割断兽人喉咙的武器装备……自然，我们确实得想法子改成我们的尺寸。”

帕拉奎：“他们有个种族，护甲可以给我们用。穿起来有点紧，但是足够了。”

坦塔洛斯：“那就更好了！还有……卡西罗斯，我想让[i]你[/i]告诉我人民最在意什么。我敢肯定，你身上的伤痕一定能提醒你，公民们的意志是什么，对吧？”

卡西罗斯：[这一表述被视作过分的亵渎，以4比2的投票，通过从记录中削除。]

坦塔洛斯：“真是不成体统的发言啊！只是你们不能接受群众想要回他们的蒸汽。比起想要那些狡猾的小绿人们在身边，比起他们害怕把自己的手弄脏，比起想要以[i]你们[/i]的方法做事，更想要蒸汽。所以！这决定了我们从这方案里获益良多，决定了我们有或能找到解决困难的方式，也决定了这是选民们想要的。我看不需要进一步讨论了。纳沙尔，之后我想跟你讨论一个魔杖的事情。散会。”

[同时，卡西罗斯议员也在从议会正式辞职时做了一个不短的演讲。演讲被另一个文件记载。] ]], "_t")
t("excerpts from a Council meeting transcript (2)", "一个议会文字记录片段 (2)", "_t")
t([[(Ink has been spilled on this transcript - you can only read certain passages.)

???: "[...]ame me for this!  YOUR mechanics examined that airship, YOUR equipment was used to repair it, and it's YOUR fault it went down!"

NASHAL: "Yes, and I told you to call the attack off the moment I heard the news - the Loyalist's wand as a fire-support tool was far too valuable to conduct the invasion without it.  But no, Palaquie had to insist on going right then--"

PALAQUIE: "My visions do not lie.  It was the best way forward.  Our odds of success at that point, low as they were, were still better than if we had let Pendor's inflexible, time-dependent plan sit and--"

PENDOR: "DON'T YOU EVEN START, YOU YETI-LOVI--[...]"

[...]

Motion made to record the statement that Councilor Pendor would not know decent equipment if it shot or stabbed him in the face passed, 3-1, with Councilor Tantalos abstaining.

Motion made to record the statement that Councilor Tormak's robes smell of absinthe and vagrants passed, 3-1, with Councilor Tantalos abstaining.

Motion made to begin an official inquiry passed 3-1, with Councilor Tantalos abstaining.  The first order of business at the next session will be determining whether or not Councilor Nashal's state-of-the-art mining and extracting equipment is capable of extracting her head from her--

[...]

TANTALOS: "If you are all quite finished with this rubbish...  How bad is the situation, exactly?  I want details and facts, not blame."

TORMAK: "You don't want blame because this whole thing was YOUR idea!  It's YOUR fault we--"

Motion to censure Councilor Tantalos for defenestrating Councilor Tormak has failed, 1-1 (tie broken by Chief Councilor status), with Palaquie, Nashal, and Pendor abstaining.

[...]

TANTALOS: "So, a few wastrels in the marketplace are gone, and the Kruk have moved on to the mainland.  As far as I am concerned, they are not presently our responsibility - these 'Allied Kingdoms' and 'Sunwall' folk can deal with them.  Thanks to Pendor's scouts, we have a weapon we can point at the Kruk Pride homeland as a deterrent, which should buy us even more time.  We should use this time to bolster our defenses...  and consider additional options.  Meeting adjourned."

PALAQUIE: "Additional options?"

TANTALOS: "The meeting has been adjourned.  You should be training our necropsychs, Councilor."]], [[（墨水被洒在这个记录上————你只能读到一些段落。）

？？？：“[……]怪我！那架飞船是你的机械师检查的，是在用你的设备修理它，也是因为你的错它才坠落！”

纳沙尔：“是吗，我在听到那个消息时也告诉你了要取消攻击————忠诚者的魔杖作为火力支援工具太珍贵了，我们进攻的时候绝对离不了它。但不，帕拉奎非要坚持当即出发————”

帕拉奎：“我眼前的景象不会作假。那是前进最好的方法。我们那时的成功几率虽然低，还是强于假如让潘多尔做主，用那个不灵活，依靠时机的方案————”

潘多尔：“你再说一句看看，你这个恋雪人————[……]”

[……]

记录下“潘多尔议员不知道什么是优良的设备，除非亲自射到或者刺到他脸上”的表述的动议以3比1的投票通过，议员坦塔洛斯弃权。

记录下“托马克议员的长袍闻起来有苦艾酒和流浪汉的味道”的表述的动议以3比1的投票通过，议员坦塔洛斯弃权。

进行官方调查的动议以3比1的投票通过，议员坦塔洛斯弃权。接下来进行调查的第一部分，将会决定是否纳沙尔议员的最新式采矿和提取工具能够将她的头从她的————

[……]

坦塔洛斯：“如果你们都闹够了……到底情况有多糟糕？我想要细节和事实，而不是抱怨。”

托马克：“你不想要抱怨是因为整件事都是你的主意！这是你的错所以我们————”

谴责坦塔洛斯议员把托马克议员扔出窗外的动议未被通过（1比1，平局被议长否决），议员帕拉奎、纳沙尔和潘多尔弃权。

[……]

坦塔洛斯：“所以，商场里的那些饭桶死了，克鲁克兽人已经开始在大陆行动。据我所知，这目前不是我们应当担心的————那些“联合王国”和“太阳堡垒”的家伙们可以对付。多亏了潘多尔的斥候，我们有了一个武器，可以作为一个威慑力量对准克鲁克部落的老家，这会给我们争取更多的时间。我们应该用这段时间加强守备……并考虑其他方案。散会。”

帕拉奎：“其他方案？”

坦塔洛斯：“已经休会了。你现在应该去训练我们的通灵师，议员。”]], "_t")
t("excerpts from a Council meeting transcript (3)", "一个议会文字记录片段 (3)", "_t")
t([[TANTALOS: "Tell the others of the unfortunate developments, Palaquie."

PALAQUIE: "The Kruk Orcs, under %s, appear to have pushed to the last bastion of the Sunwall forces...  none of my visions predict this ending favorably for anyone of non-Orcish descent.  With the Sunwall gone, there will be no further distractions for the Kruk.  In short, the Sunwall are doomed - and we are next."

TANTALOS: "Where there's a will, Palaquie, there's a way.  What of the Migratory Leviathan?  Nashal, do you have any idea where--"

NASHAL: "About that...  Kasyros stole it when everything started going to slag.  We'd take it back, but he's using it to evacuate civilians.  We'd end up using too many bullets on our own people that belong in the Kruk Orcs."

TANTALOS: "Unfortunate, but we'll surely be able to convict him of treason once this all blows over.  Pendor, you've been working with our marksmen - how are they doing?"

PENDOR: "Scared scrapless, Your Honor, but they're learning quick.  I managed to snatch up some newer Flameshot rifles from Kaltor's surplus, and our Retaliators are as strong as ever."

TANTALOS: "Splendid to hear.  And what of that backup weapon you had mentioned - what was that name again, #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF-#{normal}#"

TORMAK: "It's gone.  The mages I sent with Pendor's runners...  their invisibility spells were inadequate.  The Orcs found them...  if it's any consolation, they don't appear to have realized what the keys are for, or what it's capable of.  I'm...  I'm sorry."

Lengthy pause.

TANTALOS: "...I think it's time."  Removes a briefcase from behind the podium, and opens it to show the other Councilors its contents, before closing it and holding it again.  Councilors Palaquie, Tormak, and Nashal audibly gasp.  Motion to strike all description of its contents from the record passed, 3-2.

TORMAK: "You can't be serious!  How is that going to make the situation BETTER?"

PALAQUIE: "It cannot."

NASHAL: "I can't agree with this, Councilor Tantalos, your predecessor had a point--"

TANTALOS: Pounds fist, breaking podium.  "That doddering old coward knew NOTHING!"  Pause; sighs.  "None of us do.  All we know is, this eye's almost certainly useful for more than making declogging draught from its tears, and the person who wants it is the type of person who casually digs holes to the center of Eyal.  We've tried everything; the time for a last resort has come, and we are in dire need of a miracle.  This... 'Loyalist' is the only possible source of miracles around, and if infinite energy and blasting holes through the planet are within his capabilities, then disposing of these barbarians should be quite simple."

PALAQUIE: "If our ancestors are to believed, this could result in a fate worse than our own destruction--"

TANTALOS: "Would everyone who doesn't have any #{italic}#better#{normal}# ideas cease their jabbering before I cease it #{italic}#for them?#{normal}#"

[Silence.]

TANTALOS: "As I thought.  Nashal, prepare the G.E.M. and a retinue of guards and mechanics.  There is business I must attend to.  Meeting adjourned."]], [[坦塔洛斯：“告诉大家现在的不利形势，帕拉奎。”

帕拉奎：“克鲁克兽人，在%s的带领下，看上去已经攻到太阳堡垒军的最后一个堡垒了……我的各个预测景象都不会倾向于任何非兽人血统的一方获取胜利。太阳堡垒陷落后，对于克鲁克兽人就没有什么阻碍了。简而言之，太阳堡垒气数已尽————而我们是下一个。”

坦塔洛斯：“帕拉奎，有志者事竟成。“迁徙的利维坦”怎么样了？纳沙尔，你知不知道它在————”

纳沙尔：“那个啊……在事态变得糟糕的时候，卡西罗斯偷走了它。我们想要把它夺回来，但是他正在用它撤离平民。如果那样的话，我们会把大量本应用在克鲁克兽人身上的子弹，射向我们自己的人民的。”

坦塔洛斯：“真不走运，不过一切结束后我们一定能定他叛国罪。潘多尔，你最近在训练我们的枪手吧————他们怎样了？”

潘多尔：“那群废物们吓得不轻，尊敬的议长，但是他们进步得很快。我从卡尔托剩下的货物中收集了一些新式的喷火步枪，而我们的复仇者部队处在巅峰状态。”

坦塔洛斯：“听起来真不错。那个你提到过的备用武器————叫什么来着，#{bold}#毁天灭地、无礼的贯穿者————#{normal}#”

托马克：“它不见了。那些我派给潘多尔的传令兵的法师……他们的隐形咒语不准。兽人们找到了他们……若这算是一点安慰，他们似乎还没意识到钥匙是做什么用的，也不知道那些武器能做什么。我……我很抱歉。”

漫长的沉默。

坦塔洛斯：“……我认为是时候了。”从讲台后拿出一个手提箱，打开给其他议员看里面的东西，又合上它把它收起来。帕拉奎、托马克和纳沙尔议员都发出喘气声。清除有关箱子里东西的记录的动议以3比2通过。

托马克：“你别开玩笑吧！这东西怎么能改善现在的情况？”

帕拉奎：“它不能。”

纳沙尔：“我不能同意这样做，坦塔洛斯议员，您的前任的观点确实有道理————”

坦塔洛斯：挥拳砸桌子，把讲台砸烂了。“那个走不稳路的老懦夫什么也不知道！”停顿；叹气。“我们也都不知道。我们知道的是，这个眼的作用肯定不仅仅是用它的泪水来做清淤药水，而想要它的人，是那种可以随心所欲挖出通向埃亚尔地心的洞的人。我们已经试过了所有方案；最后挣扎的时刻来临了，我们相当渴望一个奇迹。这个……“忠诚者”是我们身边唯一可能的奇迹来源，如果无限能源和在星球中间穿洞在他的能力限度之内，那么把那群野蛮人赶走应该非常简单。”

帕拉奎：“如果我们的祖先可信的话，这可能比我们自身的毁灭更糟糕————”

坦塔洛斯：“你们这些想不出#{italic}#更好#{normal}#主意的人能不能闭上叽叽喳喳的嘴，在我来#{italic}#帮你们#{normal}#闭上之前？”

[沉默。]

坦塔洛斯：“这就对了。纳沙尔，准备好GEM，随从的守卫和机械师。我还有要做的事情。散会。”]], "tformat")

------------------------------------------------

section "tome-orcs/data/lore/primal-forest.lua"

t("primal forest", "原始森林", "newLore category")
t("a warning sign", "警告标牌", "_t")
t([[WARNING - READ THIS!

---

This forest is the site of a massive and ongoing ecological disaster.  As far as I can tell (and as a Mender, I have at least [i]some[/i] clue of what I'm talking about), Eyal's trying to fight off an infection, and the infection's fighting back for all it's worth.  Given the indiscriminate hostility of the local treants, we can assume the infection's winning, if only slightly; it's concentrated most of its power into a handful of crystalline avatars at the top of the great tree.  Best case scenario, Eyal's pushing them out like splinters, and destroying these avatars will eliminate the problem; worst case, the tree is already infected down to its roots, and these avatars are its spores, growing until they're ready to leave the tree and spread elsewhere.  I came to destroy these crystals myself, but I wasn't counting on the treants turning on me as well; since you're reading this, congratulations!  This is your responsibility now.

My advice?  Head through the portal to Shatur and call for backup.  I don't have that option, as that'd require incriminating myself by admitting that I was in Var'Eyal without a pass (you wouldn't judge me if you knew how much the trolls were paying for cheerblossom).  I can assure you that the others there are considerably more dedicated and competent than I am, even if only as a group; together, they'll be able to control this infection and treat the wounds it's left behind.  If you go in alone, you'll likely get ripped apart by the treants before you can even reach the trunk - and more are waking up every passing minute.  Unless you're the Hero of Maj'Eyal or Garkul's reanimated corpse, you'll be walking into your own grave.  Let the professionals handle this.

If you insist on going in, though, here's what I know:

-The treants, unfortunately, are no longer concerned with discerning friend from foe.  Anything not stemming from Nature is a potential source of the infection in their eyes, and must be purged before they can slumber once more.  I know that saying "please" isn't exactly sufficient for asking you not to defend yourself...  just try to keep the damage to a minimum, so they can heal the land once ravaged by this sickness.  If you want to avoid them, get off the ground level and into the canopy as soon as you can; they won't animate if they don't see anything on the forest floor to attack.  Also, do NOT try to take a core sample!  Trust me on this - as much as I wanted to know how deep the infection had spread, whether it was all the way through the tree or if it had pushed it all to the top, it attracted the treants to me like Shaloren to a stupid decision.  

-The destructive agent in question is a group of animated arcane crystals, of the type previously documented in the Scintillating Caverns.  The exact processes involved in their formation are still unclear, but it's a safe assumption that they're connected to the massive surge of blight introduced by the Spellblaze, and proof that even now, the damage is most likely worse than we can ever be sure of.  Expect to take powerful blasts of every kind of magic if you're not exceptionally evasive; fortunately, although they frequently teleport, they are completely immobile between blinks.  If one teleports near you, either take cover, or destroy it before it can reposition itself.

-The consequences of letting this go unchecked would be disastrous.  Even if this great tree's growth IS a sign of the planet successfully fighting the infection off by pushing it out, the crystalline avatars could simply climb down, bury themselves, and sicken Eyal once more.  And if Eyal's losing...  as much as I loathe to say it, perhaps those Shaloren pyromaniacs could do some good for once in their all-too-long lives, and cauterize the area down to the roots.  Provided, of course, that they can figure out how to do so without blowing up the sun.

I wish you luck, and thank you for doing what I cannot.  There are reasons why this is a risk I cannot afford to take, but it's probably best for both of us that you assume I'm a coward.  It's not too far from the truth.

With unending gratitude,
(This is where I would sign my name, were I an utter moron.)

PS: If you wouldn't mind doing me a personal favor, please destroy any written articles you find.  They spilled out of my bag as I fled; I'm already a coward, and I'd rather not be a litterer as well.]], [[[b]警告——请注意！[/b]

---

这座森林正经受着一场巨大的生态灾难。对此，我能说的就是，埃亚尔的力量正在这里对抗某种外界的感染，而这种外界的感染也正在全力反击回去（我是一名修复者，请相信我能说这些还是[i]有点根据[/i]的）。看看旁边这些不分青红皂白地胡乱攻击的狂暴的树人，你就能看出，这种感染的力量目前占着上风，尽管这一优势十分微小。这种感染的力量，大部分集中在面前这棵巨树的树冠中的几个水晶化身里面。在最好的情况下，埃亚尔正在把它们像插进身体的碎片一样推出来，只要摧毁这些化身，就可以完全解决这个问题；而最坏的情况下，这棵树已经被一直感染到根部了，而这些化身只是这种感染的孢子，它们正在慢慢生长，准备离开这棵巨树，将感染传播到世界的每个角落。我本来是想来摧毁这些水晶的，但我没想到，这些树人也对我发起了攻击。既然你已经看到了这里，恭喜你！现在解决这件事就是你的责任了。

你问我的建议是什么？赶紧从传送门跑回夏特尔，找人来帮忙吧。我可不能这么干，因为这样等于让我不打自招地承认，我在没有通行证的情况下混进了瓦·埃亚尔（如果你知道那群巨魔愿意为鼓舞之花掏多少钱，你肯定不会指责我的）。我可以向你保证，他们绝对比我更加尽责，更加专业，而且他们还是团队行动。这样的话，他们一定有办法控制这里的感染，愈合它所留下的创口。如果你就这么一个人冲进去，估计你在走到那棵巨树的树干之前，就已经被狂暴的树人们群殴致死了——而且，你每在这里继续待下去，就会不断有更多树人醒来。除非你是马基·埃亚尔的英雄，或者是加库尔的复活尸体，否则你简直就是自寻死路。还是让专业人士来干这事吧。

如果你不听我的话坚持要进去的话，那么，我来告诉你我知道的事情：

——不幸的是，那些树人现在已经完全失去了分辨敌我的能力。他们把一切不来源于自然的东西都视作潜在的感染源，只有把你们完全消灭干净，他们才会安心入睡。我知道，在这里说一堆“请”字是绝对没法让你放弃自卫的念头的……不过，请你还是尽量把你所造成的破坏降低到最低限度，这样的话他们还有机会治愈这片饱受摧残的土地。如果你想要避免和它们交战，请你尽快离开地面，爬到大树的树冠上去。因为它们只会在看到周围地上有东西的时候才会活动起来。另外，[b]不要[/b]试图取一份树芯样本！请相信我——虽然我也很想知道这种感染到底扩散到了多么深的地方；到底是已经侵入了树干，还是正在被推到树冠的地方。只要你一取出样本，周围的树人就会跟永恒精灵看到干蠢事的机会一样，争先恐后地围过来。

——目前看来，造成了这种破坏的罪魁祸首，是一群会动的奥术水晶，有记载说它们曾经在闪光洞穴中出现过。它们到底是在什么样的状况下如何形成的，目前我们尚不知晓。但是我们有理由推断，它们与魔法大爆炸中所涌出的大量的枯萎能量息息相关。这向我们证明，即使到了现在，魔法大爆炸的破坏仍然比我们想象中的要更加严重。如果你没有高超的躲避技巧，请做好被各种强大魔法轮番轰炸的准备；不过，幸运的是，尽管他们可以经常进行传送，但是他们在传送的间隔中无法移动。因此，如果有一个奥术水晶传送到了你的身边，建议你要么找个掩体躲起来，要么就在它再次传送之前赶紧干掉它。

——如果我们再不采取行动的话，后果将会是不堪设想的。尽管这棵巨树的形成本身就是这颗星球试着对抗这种感染，将感染推出自己的身体的举措。但这些水晶化身仍然可以轻松地从树冠上爬下，埋入土中，再一次让埃亚尔陷入疾病。如果埃亚尔输了的话……尽管我不想这么说，但恐怕只能说，那些老不死的永恒精灵纵火狂，大概还能做一些他们生命中为数不多的对社会有益的事情，把这块地方一直烧灼到根部。当然，这还要建立在他们能够想到一个不需要炸掉太阳的解决方案的前提之上。

祝你好运，感谢你能帮我做到这些我做不到的事情。我不能亲自冒这样的险，也是有自己的苦衷的，但你干脆直接把我当成一个懦夫好了，这对我们两个人都比较好。反正，这和真实的情况区别也不大。

无上感激，
（如果我是一个十足的白痴，我就会在这里写下我的名字）

另：如果你不介意帮我做一些小事的话，请帮我销毁掉你所找到的所有文本。那些纸是在我匆忙逃跑的时候从我的包里掉出来的。我已经是一个懦夫了，可不想再成为一个乱丢垃圾的人。]], "_t")
t("a pamphlet 'Eyal Needs You!'", "一本小册子 《埃亚尔需要你！》", "_t")
t([[EYAL NEEDS YOU!

The damage left in the Scintillating Caverns, in Norgos' Lair, and in countless other places has only now become clear, after the Hero of Maj'Eyal made them safe to explore once more.  Now that peace has been brought to these lands, Eyal is beginning to heal - but with the arrival of our magic-using cousins from the East and the Allied Kingdoms' growing acceptance of magic, the balance may once more tip towards ruin - but YOUR help can keep Eyal healthy!  Join the Menders, and start helping the planet today!

LEARNING AND OBSERVING

Our founders, once Guardians of Shatur, have always known the importance of maintaining a balanced ecosystem.  Do your hobbies include birdwatching, exploring the wilderness, and taking in the sights of natural flora?  We can provide you with a list of animals, plants, and fungi of interest; simply go out and write down where you explored, when, and how many of these species you saw.  Our experienced naturalists can use this information to track migration patterns and monitor the spread or decline of those species, allowing us to take action if one becomes endangered or invasive; already, they're working to restore the balance disrupted by the Hero of Maj'Eyal's constant slaying of local wildlife.  Change is inherent to the natural order; our experts know to only step in if a change would drastically and destructively hurt the ecosystem.  Nature solves most of its problems on its own, but occasionally we may need to hold its hand (particularly in response to mutations caused by unchecked use of arcane magic).  If you'd like to learn more about the natural order, we have a diverse community of knowledgeable naturalists who are happy to answer questions or provide a more thorough education.

REPAIRING AND HEALING

Volunteers who prefer a more hands-on approach can expect to start making a difference right away, by joining our reclamation and decontamination efforts.  It's no secret that the Hero of Maj'Eyal's many battles took their unfortunate toll; many places are still littered with magic-contaminated objects or bodies, and in some places the ground itself has been polluted by the residual effects of these spells.  (This is, of course, to say nothing of the trees burned down, etc. by beasts and ne'er-do-wells trying to stop the Hero!)  You can help by destroying dangerously magical objects, planting trees, slaying ecologically-disruptive beasts (such as Norgos), and participating in cleansing rituals to speed up the healing process.

ABILITY, RESPONSIBILITY, AND ACCEPTANCE

The wilds of Eyal are a dangerous place; we do not expect our scholars to go into them defenseless!  For those who are already accustomed to use of the arcane, our partnership with the Living Fossils allows us to identify safe and responsible methods of using magic, and provide them with an introduction to the ways of Nature, and those who are already adept with Nature can always hone their skills with our veteran members.  If you have no ability with either, you're in luck!  We're eager to show you how to accept Nature's favors to defend yourself.  Anyone can learn to summon loyal beasts or channel wyrmic strength if they're willing to try!  These abilities can be used without giving up your attunement to the arcane, but you may find that you don't need your spells anymore, once you've seen how effective Nature's power is.  We will never force you to give up magic, but if you happen to be looking for a greater commitment, speak to your instructor about following the path of the oozemancer.
]], [[[b]埃亚尔需要你！[/b]

在马基·埃亚尔的英雄扫清了闪光洞穴、诺尔格斯巢穴、和世界各处数不清的场所，让人们可以在那些安全的地方探索之后，人们终于开始正视魔法大爆炸对那里所造成的伤害。尽管这些地方现在已经变得和平，埃亚尔正在逐渐恢复——但是，由于我们那些使用魔法的东部同胞的到来，以及联合王国越来越接受奥术魔法使用的影响，自然和魔法之间的平衡被渐渐破坏，世界濒临毁灭的边缘——但是，[b]你的[/b]帮助可以让埃亚尔保持健康！请加入修复者，从今天开始，帮助这颗星球吧！

[b]学习与观察[/b]

我们的创始人曾是夏特尔的守护者，他们一直深切了解有关维持一个平衡的生态系统的重要性。你喜欢观鸟，探索大自然，欣赏多姿多彩的植物吗？我们可以向你提供一系列有关各种奇珍异兽、以及奇特的植物和真菌的列表。只要你在四处探索，记录下各种观察到的生物的分布和数量。我们那些富有经验的自然学家可以使用这些信息来追踪这些生物迁徙的模式，观察它们的扩散和消亡。这样，如果有一种生物濒临灭绝或受到入侵，我们就可以立即采取行动。现在，我们正在修复那些因为马基·埃亚尔的英雄对自然生物的杀戮，而遭到破坏的各地脆弱的生态平衡。改变是自然重要的组成部分，因此我们的专家只会在生态系统面临毁灭性严重威胁的时候，才会选择介入。大自然能够自己解决它大部分的问题，但有时，我们也需要亲自向大自然伸出援手，例如应对那些因为不恰当的奥术魔法使用造成的变异物种。如果你想要更多了解大自然的秩序和平衡，我们有一个多元化的，知识渊博的自然学家群体。他们十分乐意回答你的各种问题，乃至向你提供深入的教育。

[b]修复与治疗[/b]

对于那些更加喜欢亲自动手的志愿者，你们可以加入我们的修复和净化事业，立刻给这个世界带来改变。马基·埃亚尔的英雄的众多战斗也带来了许多不幸的损失，这并不是一个秘密。许多地方到处都是被魔法污染的物件和尸体，还有些地方的土地仍然被残留的魔法所污染。当然，更不用说，还有那些野兽和不负责任的蠢货试图阻止英雄的时候，被他们烧毁的森林！你可以通过摧毁危险的魔法物品，重新种植树木，杀死那些破坏生态的野兽（比如诺尔格斯）以及参加我们的净化仪式，来加快这个世界愈合的进程。

[b]能力、责任与认可[/b]

埃亚尔的野外是一个危险的场所；我们可不希望我们的学者手无寸铁地走进荒野！对于那些已经习惯于使用奥术魔法的人，我们和那些活化石的合作，让我们可以辨别出正确和理性的使用魔法的做法，并向你们展示自然之道的基础。对于那些已经精通自然力量的人，你们可以和我们的老成员之间相互切磋，磨练技巧。如果你两者都不了解的话，那么你就走运了！我们十分乐意向你展示如何使用自然的力量来保护自己。只要你愿意尝试，每个人都有机会掌握召唤忠诚野兽的能力，或是引导巨龙的力量！这些能力在你不放弃奥术魔法的情况下，也可以尽情使用。但是我想，当你见到大自然的力量是多么有效而强大的时候，你就再也不想使用你过去使用的那些魔法了。我们绝不会强迫你放弃魔法，但是，如果你想要追求更多献身于自然事业的话，也可以和我们的导师交谈，我们向你介绍软泥使的力量。]], "_t")
t("'On Tolerance'", "《有关容忍》", "_t")
t([[We recognize that times are changing.  Within a year, the Allied Kingdoms have gone from begrudgingly tolerating magic to openly embracing it, due to the influence of our rediscovered allies in the East.  Furthermore, if the reports are to be believed, the ecosystem of Var'Eyal remains healthy and intact, despite millennia of continuous magic-use.  Therefore, our views and approach must change with the times; we are not ignorant to new knowledge.

At this point, it should go without saying that reckless use of magic is a dire threat to...  everything, more or less.  Eyal has yet to fully recover from even the rampant necromancy of the Age of Dusk, let alone the Spellblaze itself.  Eliminating all use of magic is the only way to be safe from this situation repeating...  but it is possible that lesser uses of arcane magic do not have any inherent corrupting or harmful effect, judging from the Sun Paladins and Anorithil.  They have, contrary to our long-held beliefs, managed to use magic responsibly and safely.  We are not so blind as to deny that this is an incredible reassurance.  That said, this proves nothing about the most terrible potential of magic.  Maybe no Sun Paladin or Anorithil has yet sunk to the depths of depravity of the Age of Dusk sorcerers, or the tragically reckless mages responsible for the Spellblaze, but that is no indication that their magic does not have the potential for abuse.  

Fortunately, there is an alternative available!  With the proper respect, care, and concentration given to Nature, one can be rewarded with powers rivaling or besting the popular uses of magic.  On the civilian level, summoned fireflies can replace magical lighting, regeneration salves can replace healing spells, and accelerated crop growth makes for a far more nutritious diet than conjured foodstuffs.  For martial purposes, there's very little that can stand up to the powers of Nature.  An experienced disciple of Eyal can summon loyal beasts faster than any mage can blast them, crush spellswords of all types with draconic might, or dissolve a necromancer's army in a tide of corrosive ooze.  And if the disciple in question is familiar with the practices of the Ziguranth...  We do not condone their approach to defending nature, but their techniques speak for themselves when facing a hostile mage.  The best part about these abilities, though, is that they are self-limiting!  There is no potential for a runaway chain reaction, or a lone megalomaniac destroying much of Eyal.  The planet willingly gives us its power, and is conscious enough to take it away if we start abusing its gifts.  Even the most powerful of Wilders cannot abuse their power to the perverse degree that a necromancer can.

Thus, we're putting our efforts into two areas.  The first is advocacy of Natural alternatives to magic, talking to spellcasters to determine what they use magic for and figuring out ways to use Nature's abilities to do the same task just as well (if not more so).  We've continued the Ziguranth efforts to make all-natural replacements for Ogric runes (we predict that life expectancy is now only reduced by 40% with our newest mixtures), developed fertilizing recipes that outperform arcane methods of producing food, created wells near desert settlements otherwise dependent on water magic, and developed so many other techniques and applications that make magic just as obsolete as it is hazardous.  The second is minimizing the harm done by the arcane, by educating spellcasters on the safe, responsible, and Nature-conscious use of magic.  Not every spellcaster is evil, and in fact, some may enrich the lives of those around them!  Runic magic is at least somewhat self-limiting, and we are working with the Living Fossils guild in hopes of developing a new type of magic, one inherently linked to and limited by Nature.  Their stone-wardens have maintained perfect harmony with Nature despite constant use of the arcane; if this is truly the way forward, then we shall welcome it with open arms.
]], [[我们必须承认，现在世道变了。在不到一年的时间里，在东方重新发现的那些盟友的影响之下，联合王国已经开始从不情愿地容忍魔法，迅速转变为公开接受魔法的使用。此外，如果那些报导确认属实的话，尽管在那里的人们长期使用魔法长达几千年，瓦·埃亚尔的生态系统仍然健康而完整。因此，我们绝不能对新知识一无所知，我们的观点和方法必须随着时代而改变。

事到如今，鲁莽使用魔法会对……几乎世间一切构成严重威胁，应当已经不言而喻。黄昏纪里死灵魔法的猖獗使用，对埃亚尔所造成的影响至今还没有恢复，更不用说魔法大爆炸的影响了。消除所有魔法的使用，看起来是避免这种状况重演的唯一方法……但是，从太阳骑士和星月术士的情况来看，少量使用奥术魔法，本身并不会对世界带来任何腐蚀和有害的影响。与我们长期以来的信念相反，他们成功地，安全而负责任地控制了魔法的使用。我们绝不能盲目地否认，这对我们是一种难以置信的安慰。尽管如此，这并不否认，魔法仍然可能造成极其可怕的后果。可以说，太阳骑士和星月术士，远远没有堕落到黄昏纪法师那样邪恶的程度过，也并不像那些引发魔法大爆炸的法师一样，鲁莽到可悲。但是这并不能表明，他们的魔法没有遭到滥用的可能性。

幸运的是，我们还有另一种选择！只要给予大自然足够的尊重，关心和专注，人们就可以获得和普遍应用的魔法匹敌，乃至更强的力量。在民用领域，召唤萤火虫可以替代魔法灯笼，治疗药剂可以替代治疗魔法，而加速谷物成熟的技术做出来的菜肴，可比法师制作的魔法食品对身体健康多了。在军用领域，很少有人能够抵挡自然强大的力量。那些埃亚尔忠实的学徒，可以比法师的火球速度更快地召唤忠诚的兽群，用巨龙的力量粉碎各种类型的魔法战士，或是用一股腐蚀性的粘液，瞬间融解死灵法师的军团。另外，如果那些学徒还了解那些伊格兰斯曾经使用过的力量的话……我们不能容忍他们为了保卫自然做出的一系列举措，但他们的技术在面对敌对法师的时候，总是能够脱颖而出。有关这些自然能力，最重要的一点是，它们是会进行自我约束的！他们绝对不会像奥术魔法一样，引发一场失控的连锁反应，在妄自尊大的狂妄中给埃亚尔大部分的地方带来毁灭。这颗星球自愿给予了我们力量，当我们开始滥用它们的时候，它就会有意识的从我们的身边拿走。即使是最强大的野性系能力者，也不会像死灵法师一样，把他们的力量滥用到如此反常的程度。

因此，我们目前的事业有两个主要的目标。第一个目标是推广使用自然力量代替法术的方法。我们要和那些法师交谈，知道他们用魔法来做什么，然后想办法用自然的力量来达成同样的目标，乃至做的更好。我们继续伊格兰斯把食人魔的符文替换成纯天然产品的努力（现在，使用我们的新技术，预计只会减少40%的寿命），发展新的肥料技术，让它们远远超出使用奥术力量生产食物的方法，还有在沙漠地区创造水井，让那些地方不再只能依靠水魔法。我们创造了各种各样其他使用自然力量的技术与应用，让过去那些使用魔法的方法看上去既落后又危险。第二个目标是最大限度地减少奥术魔法造成的危害，我们会教育法师，如何安全地、负责任地、有保护自然的意识地去使用魔法。并不是每个法师都是邪恶的，他们中的许多人，都可以给他们身边人的生活带来好处！符文魔法就是某种意义上有自我限制能力的魔法，我们也在和那个活化石组织合作，希望能够开发出一种新的魔法，一种和自然联结，受自然约束的魔法。那些岩石守卫就是这样的例子，他们经常使用奥术力量，却仍然和自然之间保持着完美的平和。如果这就是我们前进的道路，我们将张开双臂欢迎它。]], "_t")
t("a leaf-bound journal", "一本被树叶包裹的笔记", "_t")
t([[[i](You see here a leaf-bound journal; the moment you open it, it begins to wither and crumble.  You manage to rip out one page; it is still disintegrating, but slowly enough that you can read it before it turns to dust.)[/i]

Another vandalized poster.  Calling us traitors, collaborators, declaring themselves the True Ziguranth.  Fools, the lot of them.

When I established the Menders, it wasn't because I thought the arrival of a handful of magic-users who also happen to be decent people disproved anything taught in Zigur or my childhood in Shatur.  It wasn't because I suddenly forgot that anything derived from arcane magic, no matter whether or not it's wrapped up in some mumbo-jumbo about the heavens, carries the risk of mutating into something that could put the Spellblaze to shame.  It was because those maniacs had ignored the shifting political tides for so long that they found themselves sliding into irrelevance, then went and skipped directly over irrelevance into pariahdom with that foolhardy assassination attempt.  They can blame the Far East all they want, but that was only the last nail in the coffin, alongside widespread acceptance of runes and alchemists operating openly across the continent.

I can appreciate their dedication.  I can appreciate their frustration, and how seeing the world treating magic-use as normal would just make them want to get more violent - but the fact is, the raid on Zigur was a mercy kill, preventing the fanatics from making us look even worse in the public eye.  We are long past the point where intimidation can get us anywhere - so we need to try a new approach.  If reminding the world of the horrors of magic isn't working anymore, the Spellblaze and the Age of Dusk being too faded from public memory, then we need to remind them of the wonders of Nature instead, wonders they can see for themselves, today.  If the public won't believe that magic is evil, they can believe that Nature is better.  If we can't make magic taboo, we can make magic obsolete...  and all of this gathers support we'd otherwise lack, curious minds waiting to be taught the beauty of Nature and warned of the hazards of the arcane.

So maybe the old guard's been overrun with Thaloren, youths, and others who care a great deal more about loving nature than hating magic.  I don't see why this is a problem - making Nature stronger will make it more capable of resisting the damage magic may inflict.  We've allowed the idea of supporting Nature over magic to survive the Allied Kingdoms' treaty with the Gates of Morning, the raid on Zigur, and the attacks on Ziguranth patrols.  We've established ourselves as a selfless, charitable organization working for the good of all, a reputation that will grant us significantly more credibility than our previous public image of a band of crazed fanatics.

Perhaps most meaningfully of all, there are [i]far[/i] more Menders now than there were Ziguranth in the last century.  These allies will help us support Nature to an incredible degree, and we've started offering volunteer courses in classical anti-magic training, allowing them to further refine our techniques for dealing with rogue mages.  If and when arcane magic causes another catastrophe, these allies will rally behind us as we defend Nature from those who threaten it...  And, who knows, maybe we actually CAN teach mages to show a sane level of restraint without wiping them all out.  I'm keeping my eyes open for ways to make that happen, no matter how unlikely they may be.

In the meantime, paying off Stone Warden trainers and buying enough mindstars and herbal infusions for our initiates isn't cheap.  I'm not proud of what I'm doing to pay the bills, and am fully aware of what it'd do to the organization if someone saw me, but this is the fastest and easiest money I've ever made.  Ten minutes of concentration, a few hours to re-establish my equilibrium, and I can grow enough cheerblossom to cover our expenses for a week.]], [[[i]（你看到了一本被书页包裹的笔记；当你打开它的时候，它就开始慢慢枯萎、碎裂。你努力撕下了一页，它仍然在慢慢分解，但是分解的速度慢到你能够读完，才最终化成了尘土。）[/i]

又有一张海报被他们毁坏了。他们称我们为叛徒、通敌者，宣称自己才是真正的伊格兰斯。他们这群傻瓜。

我建立修复者的理由，并不是因为那些碰巧上是好人的魔法使用者的到来，就能颠覆我过去在夏特尔和伊格的时候所受到的一切教育。这也不是因为我已经遗忘了，任何从奥术魔法之中产生的力量，不管是否被他们包裹在有关天空的一系列繁文缛节里，仍然有着被人扭曲，产生比魔法大爆炸更加可怕的灾难的危险性。这一切都是因为，那群疯子一直以来都无视着政治潮流中发生的巨大转变，不知道自己已经变成了无关紧要的局外人。然后，他们那场莽撞的暗杀行动，彻底让他们的地位从局外人成为了贱民。他们尽管可以把他们所遭受的不幸都归咎于远东的人，但这只是他们棺材板上的最后一颗钉子而已，而没有意识到早在更早之前，符文已经在这片大地上广泛使用，炼金术师在各处公开营业了。

我很欣赏他们的奉献精神。我也很能理解他们的挫败感，他们看到，这个世界越来越将魔法的使用看做稀松平常的事，而变得越来越暴力——但是，实际上，伊格被摧毁对我们来说可以说是一种安乐死，这避免了那些狂热分子进一步在公众面前破坏我们的形象。我们早就应该知道，光靠暴力威慑是不能解决一切问题的——因此，我们必须尝试一种新的办法。既然黄昏纪和魔法大爆炸这样的过去，早就已经在公众的视野之中淡忘。过去警告世人魔法的恐怖的方法，已经不再能够起到作用。那么，我们应该改为向他们展示大自然中那些他们今天就能亲眼目睹的奇迹。既然公众已经不相信魔法是邪恶的了，我们应该向他们展现，自然是更好的。如果我们不能让魔法成为禁忌，我们可以让魔法成为一种过时的技术……而这一切可以吸引无数我们过去所忽视的支持者，我们将可以在他们充满好奇心的心灵中展现自然的美好，并警告奥术魔法带来的恐怖。

所以，那些过去的守护者，现在已经被自然精灵，年轻人，还有更多比起对魔法的痛恨，更关心对自然的热爱的人所代替。我不认为这里有什么问题——让自然的势力更加强大，才能抵挡魔法所造成的伤害。我们高举着“自然胜过魔法”的旗号，从联合王国与晨曦之门的条约、对伊格的袭击，以及对伊格兰斯巡逻队的搜捕中幸存下来。我们建立了一个无私的慈善组织，为所有人的利益而工作。这一声誉，比起过去一群狂热的极端分子的公众形象，在大众面前更加可信地多。

另外，最重要的是，我们招募的修复者的数量，已经[i]远远超过[/i]伊格兰斯一个世纪里招募的成员的数量。这些盟友对我们在保护自然事业上的支持达到了一个难以相信的程度。我们已经开始了向他们提供传统的反魔法训练的志愿课程，让他们进一步锤炼自己对抗游荡法师的能力。如果奥术魔法造成了另一次灾难，这些盟友将会追随我们成为我们保护自然免受威胁的坚强后盾……另外，谁知道呢，也许我们[b]真的可以[/b]教会那些法师，学会一点理性的克制，而不需要把他们全部杀光。我会一直寻求实现这种目标的方法，不管它的可能性有多么渺茫。

与此同时，支付岩石守卫训练师的工资，以及给我们的新成员购买足够的灵晶和草本纹身的价格可不便宜。我知道我支付账目的方法不太光彩，我也知道如果被人看到这事，我的组织会受到多么坏的影响，但是这是我能找到的赚钱最快最容易的方法了。只要十分钟的专注，再花上几个小时来恢复我的失衡值，我种出的鼓舞之花就足够支付我们一个礼拜的开销了。]], "_t")

------------------------------------------------

section "tome-orcs/data/quests/amakthel.lua"

t("The Dead God Awaits", "已死之神在等待", "_t")
t("Deep within Eyal you found a huge cavern containing some of the remains of the great dead god Amakthel...", "在埃亚尔的深处，你找到了一个巨大的山洞，那里面深埋着已死的巨神阿马克泰尔的遗骸。", "_t")
t("Along with what appears to be a living Sher'tul that seems to be trying to resurrect him.", "在那里，还有一个活生生的夏·图尔人，它试图复活这尊古神。", "_t")
t("It must be stopped at all cost, the Prides only just got their freedom back, you can not allow anything to take it away again!", "必须不惜一切代价阻止他的可怕行径，部落的自由来之不易，任何人都无法再次夺走它！", "_t")
t("The Sher'tul Priest has been taken care of, Amakthel will keep on sleeping forever now. The Prides and the world are safe.", "夏·图尔祭司已经被妥善处置，阿马克泰尔将永久继续沉睡。部落和世界的和平得到了确保。", "_t")
t("#LIGHT_GREEN#You have won the game!.#WHITE#", "#LIGHT_GREEN#你通关了！#WHITE#", "_t")
t("#CRIMSON#You feel as if your Rod of Recall is working again in this area.", "#CRIMSON#你感觉到你的召回之杖可以继续在这个区域运作了。", "log")
t("Orc Warrior", "兽人战士", "_t")
t("Winner", "游戏胜利", "_t")
t("#GOLD#Well done! You have won the Tales of Maj'Eyal: Embers of Rage!#WHITE#", "#GOLD#干得不错！你通关了马基·埃亚尔的传说：余烬怒火#WHITE#", "_t")
t("You have thwarted the Steam Giants' genocidal plans, and avenged those killed in the attack on Kruk Pride.  Their desperate pact with the High Priest did nothing to stop you; the priest and his god lay dead at your feet, and you have ensured they will #{italic}#stay#{normal}# dead for the foreseeable future.", "你挫败了蒸汽巨人灭绝你们的邪恶计划，并为那些在他们残忍袭击中丧生的部落同胞复仇。他们绝望中与夏·图尔祭司订立的邪恶契约也未能阻止你，祭司和他的神倒在你的脚下，你已经确保他们在可预见的将来会#{italic}#一直#{normal}#长眠下去。", "_t")
t("The humans, elves, and halflings will not be able to hurt your people again.  By destroying the farportal and denying King Tolak's army its glorious battle, you have ensured the safety of your people from the Allied Kingdoms, and by storming the Gates of Morning you have eliminated the last bearers of the West's hateful aggression in Var'Eyal.", "无论是人类、精灵还是半身人，都再也无法伤害你的族人。你摧毁了远行传送门，使托拉克国王的军队失去了这场光荣的战斗，从而确保族人免受联合王国侵害。你攻下晨曦之门，也消灭了西方在瓦·埃亚尔施行可恨侵略的最后一批爪牙。", "_t")
t("For now, peace reigns.  You know that this will not last forever.  You may have repelled its vanguard, but the Kar'Haïb Dominion bides its time waiting for a weakness it can exploit; the smugglers' portals from Maj'Eyal remain undiscovered, and while neither you nor King Tolak has any remaining desire to take the other's continent, the fear of invasion will linger in the backs of your minds.", "眼下，和平降临了。但你知道这不会永远持续下去。虽然你击退了卡尔·亥巴帝国的先锋，它却仍在等待可乘之机；走私者们从马基·埃亚尔通往这里的传送门依然没有被发现。即使你和托拉克国王都已无意夺取对方的大陆，对入侵的恐惧仍会萦绕在你们心底。", "_t")
t("  The messages of the Lost City give you cause to remain ever vigilant for the threats they warned of, including their authors, and you wonder what your people will do now that their struggle to escape eradication, one that has defined them for their entire recorded history, has ceased to be a concern.", "  来自失落之城的消息让你充满警醒，无论是那些他们警告的恐怖威胁，还是他们本身。你想知道，当你的人民所极力摆脱的灭亡威胁：那个镌刻在你们整个历史中的威胁，现在已经不复存在的时候，你们的人民又将何去何从。", "_t")
t("Regardless...  You just killed a god and gave your people the first chance to relax in thousands of years.  It's been a pretty good day.", "不管怎样…你杀死了一个神，而你的人民在数千年的征战中终于有了放松的机会。多么愉快的一天。", "_t")
t("You may continue playing and enjoy the rest of the world.  Your soldiers may want to speak with you outside...", "你可以继续游戏，享受这个世界。你的士兵在外面，有些话要说……", "_t")
-- untranslated text
--[==[
t("", "", "_t")
--]==]


------------------------------------------------

section "tome-orcs/data/quests/kruk-invasion.lua"

t("Homeland", "家园", "_t")
t("The giants have breached the mountain-side of Kruk pride!", "巨人们已经进犯了克鲁克部族的靠山侧！", "_t")
t("They are invading the town just when most of our forces are outside.", "他们进攻了城镇，而我们的部队却还在外面。", "_t")
t([[Only you and few others are left to close the breach by collapsing the tunnel from the inside.
]], [[只有你和少量同伴还留在这里，必须炸毁他们的隧道，封锁突破口。
]], "_t")
t("#LIGHT_GREEN#* You have collapsed the tunnel, saving the Pride. For now.#WHITE#", "#LIGHT_GREEN#* 你成功炸毁了隧道，挽救了部落的燃眉之急。#WHITE#", "_t")
t("#LIGHT_GREY#* You must place the bomb at the end of the tunnel to destroy it.#WHITE#", "#LIGHT_GREY#* 你必须在隧道尽头安装炸弹来炸毁它。#WHITE#", "_t")
t("Cave Detonator", "洞穴炸弹", "_t")
t("This bomb was tailored to crumble the tunnel used by the Steam Giants to invade Kruk Pride.", "这枚炸弹是为粉碎蒸汽巨人用来入侵克鲁克部落的隧道而特制的。", "_t")
t([[You place the detonator, you have 220 turns to get out or be destroyed by the explosion.
Use your #{bold}##GOLD#Rod of Recall#LAST##{normal}#!]], [[你成功安装了炸弹，将于220回合后爆炸。你需要在爆炸前离开。
使用 #{bold}##GOLD#回归之杖#LAST##{normal}#！]], "_t")
t("#LIGHT_GREEN#Kruk Pride is safe for now. Now is time for revenge!", "#LIGHT_GREEN#克鲁克部落安全了。现在是复仇的时刻！", "saySimple")

------------------------------------------------

section "tome-orcs/data/talents/celestial/cosmic.lua"

t("Lunar Orb", "月光之球", "talent name")
t("Fires out a bolt of cosmic energy in the target direction. The projectile continues until it hits a wall or the edge of the map, dealing %0.2f dark damage to enemies hit and restoring %d negative energy. The negative energy gained is reduced by 25%% per enemy hit, restoring a maximum of %d. Enemies hit will become aware of you.", "向目标方向射出一道宇宙能量。直到碰到墙或者到达地图边缘，对敌人造成 %0.2f 的暗影伤害并回复 %d 负能量。负能量回复量最大为 %d，每击中一个敌人将少回复 25%% 的负能量，被击中的敌人将注意到你。", "tformat")
t("Astral Path", "星光大道", "talent name")
t("The spell fizzles: there are no available spots to teleport to.", "法术失败了：周围没有可供传送到的区域。", "logSeen")
t([[Fire an orb of negative energy towards a spot within range %d.
		When the orb reaches its destination, it will teleport you to its location.
		The speed of the projectile (%d%%) increases with your movement speed]], [[在 %d 码内发射一个负能量球。
		当负能量球到达目的地时，会将你传送到其位置。
		其飞行速度 (%d%%) 受你的移动速度加成。]], "tformat")
t("Galactic Pulse", "银河脉冲", "talent name")
t([[Sends out a slow-moving spiral of cosmic energy towards a target location within range 8.
		As the cosmic energy moves, it pulls in targets adjacent to it, dealing %0.2f darkness damage and granting you 1 negative energy per hit.]], [[在 8 码内发出一个缓慢移动的螺旋宇宙能量。
		当它移动时，会把相邻的目标拉向它，造成 %0.2f 暗影伤害并每击中一次回复 1 点负能量。]], "tformat")
t("Supernova", "超新星", "talent name")
t([[Expend all of your negative energy to create a massive burst of dark energy (radius %d) at a target location within range %d.
		This deals %0.2f darkness damage and pins targets hit for %d turns.
		The damage and pin chance increase with your spellpower, and the damage, radius and pin duration all increase with negative energy and talent level]], [[消耗你所有的负能量，在目标位置制造一次半径 %d 的大规模暗能量爆发，施法距离为 %d 码。
		造成 %0.2f 点暗影伤害，并使命中的目标定身 %d 回合。
		伤害和定身几率受法术强度加成；伤害、半径和定身持续时间均受负能量和技能等级加成。]], "tformat")

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

section "tome-orcs/data/talents/steam/steam.lua"

t("Steam Pool", "蒸汽能量池", "talent name")
t("Allows you to have a steam pool. Steam is used to use most steamtech equipments and powers.", "让你有一个蒸汽池。蒸汽用于大多数蒸汽技术装备和能力。", "_t")
t("inscriptions", "刻印", "talent category")
t("implants", "植入体", "talent type")
t("Steamtech directly embedded on the skin.", "直接嵌入皮肤的蒸汽技术。", "_t")
t("steamtech", "蒸汽科技", "talent category")
t("other", "其他", "talent type")
t("Tinkers with stuff.", "制造东西。", "_t")
t("physics", "物理", "talent type")
t("Learn the mechanical side of steamtech.", "学习机械方面的蒸汽技术。", "_t")
t("chemistry", "化学", "talent type")
t("Learn the chemistry side of steamtech.", "学习化学方面的蒸汽技术。", "_t")
t("blacksmith", "铁匠", "talent type")
t("All this metalworking has improved you.", "这些金属加工经验使你得到了提升。", "_t")
t("engineering", "工程师", "talent type")
t("You don't just know how tinkering works, you know all the interesting details too!", "你不仅懂得蒸汽工艺的运作原理，还掌握了其中所有有趣的细节！", "_t")
t("butchery", "屠杀", "talent type")
t("Strap saws to your arms and rush into battle!", "挥舞链锯，冲进战场！", "_t")
t("sawmaiming", "链锯", "talent type")
t("Use steam powered saws to their maximum efficiency! Maim! Cut! Shred!", "最大限度使用蒸汽动力链锯！致残！切裂！肢解！", "_t")
t("battlefield management", "战地控制", "talent type")
t("Use steam powered saws to maneuver around the battlefield, gaining strategic advantage.", "使用蒸汽动力链锯在战场上机动，获得战略优势。", "_t")
t("battle machinery", "战术机械", "talent type")
t("Use steam powered engines to tilt the battle in your favour.", "使用蒸汽动力引擎使战斗向你有利的方向倾斜。", "_t")
t("automated butchery", "自动化屠杀", "talent type")
t("Improve your saws and tinkers with automated processes to help shred your foes.", "利用自动化流程改进你的链锯和蒸汽工具，助你撕碎敌人。", "_t")
t("furnace", "熔炉", "talent type")
t("Harness the power of fire.", "掌握火焰的力量。", "_t")
t("gunner training", "枪支训练", "talent type")
t("Use steam powered guns to rain bullets of death on your foes!  (Learning these talents allow you to fire two steamguns at once.)", "用蒸汽枪向你的敌人发射致命的子弹！（学习这些技能可以让你同时用两把蒸汽枪开火。）", "_t")
t("gunslinging", "枪手", "talent type")
t("Use advanced marksmanship to confound and overwhelm your foes!  (Learning these talents allow you to fire two steamguns at once.)", "使用先进的射击技巧来迷惑和压倒你的敌人！（学习这些技能可以让你同时用两把蒸汽枪开火。）", "_t")
t("bullets mastery", "子弹掌握", "talent type")
t("Use various kinds of technology to temporarily enhance your bullets.  (Learning these talents allow you to fire two steamguns at once.)", "使用各种技术暂时强化你的子弹。（学习这些技能可以让你同时用两把蒸汽枪开火。）", "_t")
t("avoidance", "闪避", "talent type")
t("Using various enhancements of your cloak you are able to manage incoming damage.", "利用斗篷的各种强化效果，你能够化解所受伤害。", "_t")
t("elusiveness", "飘忽身法", "talent type")
t("Incredible feats of slipperiness!", "令人难以置信的滑溜身法！", "_t")
t("automation", "自动化", "talent type")
t("Use small automated devices to control the battlefield.", "使用小型自动设备掌控战场。", "_t")
t("psytech gunnery", "灵能射击", "talent type")
t("Meld your psionic powers with awesome steamtech! For mayhem!", "将你的灵能与超棒的蒸汽科技融合！为了混乱！", "_t")
t("thoughts of iron", "钢铁意志", "talent type")
t("Apply some of your formidable willpower through steam devices.", "通过蒸汽装置运用你强大的意志力。", "_t")
t("mechstar", "机械灵晶", "talent type")
t("Control your mindstar and infuse it with steamtech.", "掌握你的灵晶，并用蒸汽科技强化它。", "_t")
t("dread", "惊骇", "talent type")
t("Behold the mechanized horrors.", "见识这些机械化的恐怖造物吧。", "_t")
t("magnetism", "磁力", "talent type")
t("Use the power of electricity to supercharge your shield.", "使用电力的力量超载你的盾牌。", "_t")
t("demolition", "爆破", "talent type")
t("The use of high explosives.", "使用高爆炸药的能力。", "_t")
t("gadgets", "工具", "talent type")
t("Cunning devices to augment your combat skill.", "用来增强你战斗能力的灵巧装置。", "_t")
t("heavy weapons", "重装武器", "talent type")
t("Wield powerful steamtech tools of destruction.", "装备用来毁灭的强大蒸汽科技工具。", "_t")
t("turrets", "炮台", "talent type")
t("Deploy steam powered turrets to assist you in combat.", "部署蒸汽驱动的炮台，在战斗中为你提供协助。", "_t")
t("The various kinds of turrets.", "各种类型的炮台。", "_t")
t("artillery", "火炮", "talent type")
t("Advanced explosive weaponry.", "高级爆炸武器。", "_t")
t("mecharachnid", "机械蜘蛛", "talent type")
t("Build and deploy a powerful mechanical arachnid to assist you.", "建造和部署强大的机械蜘蛛来帮助你。", "_t")
t("chemical warfare", "化学武器", "talent type")
t("Unleash toxic steamtech weaponry on your enemies.", "对你的敌人释放剧毒的蒸汽武器。", "_t")
t("#VIOLET#EUREKA!", "#VIOLET#我发现了！", "log")
t("#VIOLET#EUREKA!#WHITE# Schematic learnt: #LIGHT_BLUE#%s", "#VIOLET#我发现了！#WHITE# 已学习配方：#LIGHT_BLUE#%s", "saySimple")
t("This talent is required for the following tinkers (you still need to learn/find the schematics):", "该技能是制造下列附着物的必要条件（你仍然需要找到/学会相应配方）：", "_t")
t(" #LIGHT_BLUE#(known)#LAST#", " #LIGHT_BLUE#（已学会）#LAST#", "_t")
t("#{italic}#* ...perhaps more to discover...#{normal}#", "#{italic}#* ……可能还可以找到更多……#{normal}#", "_t")

------------------------------------------------

section "tome-orcs/data/talents/steam/turrets.lua"

t("Deploy Turret", "部署炮台", "talent name")
t([[You are able to deploy turrets, stationary constructs that defend you in combat. Turrets last 10 turns, have a 20 turn cooldown, and deploying a turret places the others on a 5 turn cooldown.
You learn new turrets as you invest in this talent.

At raw talent level 1 you can use Steamgun turrets, which fire at a random target nearby for %d%% steamgun damage. These shots bypass allies.
At raw talent level 3 you can use Flame turrets, which deal fire damage to enemies in a radius 3 cone. Flame turrets gain %d bonus armor and 30%% resistance to all damage.
At raw talent level 4 you can use Medic turrets, which emit a healing mist that restores %d life to allies and reduces the duration of newly applied detrimental effects by %d%%.
This talent also increases the Dexterity, Constitution and Cunning of all Turrets by %d.

All turrets gain bonus armor equal to 1/2 your level, are immune to all detrimental effects, and inherit your increased damage, resistance penetration, Steampower, Physical Power, and Accuracy.
The stat bonus as well as the damage and healing dealt by Flame and Medic Turrets will increase with your Steampower.]], [[你可以部署炮台——在战斗中保护你的固定式构装体。炮台持续 10 回合，技能冷却时间为 20 回合；部署一种炮台会使其他炮台技能进入 5 回合冷却。
随着你投入更多技能点，你会学会新的炮台。

原始技能等级 1 时，你可以使用蒸汽枪炮台。它会随机向附近一个目标开火，造成 %d%% 蒸汽枪伤害；这些射击可以越过友军。
原始技能等级 3 时，你可以使用火焰炮台。它会对半径 3 的锥形范围内敌人造成火焰伤害；火焰炮台获得 %d 点额外护甲和 30%% 全伤害抗性。
原始技能等级 4 时，你可以使用医疗炮台。它会释放治疗雾气，为盟友恢复 %d 点生命，并使新施加的负面效果持续时间缩短 %d%%。
该技能还使所有炮台的敏捷、体质和灵巧各提高 %d 点。

所有炮台获得等于你等级一半的额外护甲，免疫所有负面效果，并继承你的伤害加成、抗性穿透、蒸汽强度、物理强度和命中。
上述属性加成，以及火焰炮台造成的伤害和医疗炮台提供的治疗量，都会随你的蒸汽强度提高。]], "tformat")
t("Steamgun Turret", "蒸汽枪炮台", "talent name")
t("Not enough space to summon!", "没有足够的空间召唤！", "logPlayer")
t("steamgun turret", "蒸汽枪炮台", "_t")
t("An automated turret equipped with a steamgun.", "一个装备蒸汽枪的自动炮台。", "_t")
t("Turret", "炮台", "_t")
t("Deploy a turret mounted with a steamgun that fires at foes within range for %d%% steamgun damage. The turret gains +%d Dexterity, Constitution and Cunning and %0.2f Steamgun Mastery.", "部署一个装备蒸汽枪的炮台，会自动射击射程内的敌人，造成 %d%% 蒸汽枪伤害。炮台具有 +%d 额外敏捷、体质、灵巧值和 %0.2f 蒸汽枪精通。", "tformat")
t("Rocket Launcher", "火箭发射器", "talent name")
t("You require a steamgun for this talent.", "你需要一把蒸汽枪才能使用这一技能。", "logPlayer")
t("Fire a missile dealing steamgun damage as fire in radius 2.", "发射导弹，在 2 码范围内造成火焰蒸汽枪伤害。", "tformat")
t("Dual Steamgun", "炮台双枪", "talent name")
t("Gain a second steamgun that deals %d%% damage.", "获得第二把蒸汽枪，这把枪可以造成 %d%% 伤害。", "tformat")
t("Flame Turret", "火焰炮台", "talent name")
t("flame turret", "火焰炮台", "_t")
t("An automated turret equiped with a flamethrower.", "一个装备火焰喷射器的自动炮台。", "_t")
t("Deploy a turret mounted with a flamethrower, scorching nearby targets. The turret gains +%d Dexterity, Constitution and Cunning.", "部署一个装备喷火器的炮台，会灼烧周围的敌人。炮台具有 +%d 额外敏捷、体质和灵巧值。", "tformat")
t("Flamethrower", "火焰喷射器", "talent name")
t([[Throw a cone of flame with radius %d, dealing %0.2f fire damage.
		The damage will increase with your Steampower.]], [[喷射出半径 %d 码扇形的火焰，造成 %0.2f 火焰伤害。
		伤害受蒸汽强度加成。]], "tformat")
t("Flame Vortex", "火焰旋涡", "talent name")
t([[Project a radius %d vortex of superheated air, dealing %0.2f fire damage and pulling targets towards you.
		The damage will increase with your Steampower.]], [[在半径 %d 码范围内喷出灼热空气构成的漩涡，造成 %0.2f 火焰伤害，把所有敌人拉近你。
		伤害受蒸汽强度加成。]], "tformat")
t("Medic Turret", "医疗炮台", "talent name")
t("medic turret", "医疗炮台", "_t")
t("An automated turret emitting a healing mist.", "一个可以喷射治疗迷雾的自动炮台。", "_t")
t("Deploy a turret that emits a healing mist in radius 3. The turret gains +%d Dexterity, Constitution and Cunning.", "部署一个在 3 码范围内喷出治疗之雾的炮台。炮台具有 +%d 额外敏捷、体质和灵巧值。", "tformat")
t("Overclock", "炮台超载", "talent name")
t([[Send a surge of power into all turrets in sight, extending their duration by %d turns and granting them a charged shield absorbing %d damage for 10 turns. While the shield holds, each turn the turret will project a bolt of lightning dealing %0.2f lightning damage to a random enemy in radius 6, with a 25%% chance to daze.
		The effects will increase with your Steampower.]], [[向视野内所有炮台注入能量，增加他们 %d 回合的持续时间，并且让他们获得一个吸收 %d 伤害的护盾，持续 10 回合。在护盾消失之前，每个炮台都会向半径 6 码内的随机敌人发射闪电弹，造成 %0.2f 闪电伤害，并有 25%% 的几率眩晕敌人。
		这一效果随蒸汽强度提升。]], "tformat")
t("Upgrade", "炮台升级", "talent name")
t([[Upgrade the target turret, granting it %d%% increased maximum life and enhanced abilities based on type:
		Steamgun: Gains a second steamgun dealing %d%% damage, and every 3 turns will fire a rocket dealing %d%% steamgun damage as fire in radius 2.
		Flame: Increases damage by %d%%, range by %d, and every 3 turns will project a vortex of superheated air that drags targets within range %d towards the turret as well as dealing normal flamethrower damage.
		Medic: Increases healing on affected targets by %d%%, and has a %d%% chance to cleanse a negative effect each turn.]], [[升级目标炮台，使其获得 %d%% 最大生命值，并根据其类型，获得以下的特殊能力：
		蒸汽枪炮台：获得第二把造成 %d%% 伤害的蒸汽枪，每 3 回合会发射一枚火箭，在 2 码半径内造成 %d%% 火焰蒸汽枪伤害。
		火焰炮台：增加 %d%% 伤害和 %d 射程，每过 3 回合，会在 %d 码范围内喷出灼热蒸汽的漩涡，将所有敌人拉向炮台，并造成标准喷火伤害。
		医疗炮台：增加对目标的治疗量 %d%%，且每回合有 %d%% 几率清除目标身上一个负面效果。]], "tformat")
t("Hunker Down", "炮台守卫", "talent name")
t("guardian turret", "守卫炮台", "_t")
t("An advanced turret equipped with dual steamguns.", "一个装备双蒸汽枪的高级炮台。", "_t")
t([[Deploy a defensive emplacement around you, summoning 2 guardian turrets in adjacent tiles for %d turns. Guardian turrets redirect %d%% of all damage taken by other adjacent allies (other than fellow guardian turrets) to themselves, and each is armed with a powerful turret capable of firing piercing bullets.
			Guardian Turrets gain %0.2f ranks in Steamgun Mastery based on your Hunker Down talent level.]], [[进入守备模式，在身边召唤 2 个守卫炮台，持续 %d 回合。守卫炮台会将身边盟友（不包括其他守卫炮台）所受到所有伤害的 %d%% 转移到自己身上，并且它们装备有强力的电磁炮，可以发射贯穿敌人的子弹。
		守卫炮台具有 %0.2f 蒸汽枪精通技能，技能等级取决于你炮台守卫技能等级。]], "tformat")
t("Gauss Cannon", "电磁炮", "talent name")
t("Fire your twin-linked gauss cannons, dealing 100%% steamgun damage as lightning in a piercing beam that bypasses all armor. This does not harm friendly targets.", "发射你的双联电磁炮，在一条贯穿直线上造成 100%% 闪电蒸汽枪伤害，无视护甲。这一效果不会伤害友好目标。", "tformat")

------------------------------------------------

section "tome-orcs/data/talents/uber/str.lua"

t("Pain Enhancement System", "痛苦强化系统", "talent name")
t("Earned the achievement 'Size Matters' on this character.", "当前角色解锁了“伤害很重要”成就。", "_t")
t("When you deal a critical hit your embedded system activates, increasing all your primary stats except Strength by 50%% of your Strength for 6 turns.", "系统将会在你暴击时启动，在 6 回合内你的全属性（力量除外）将会增加等同于你 50%% 力量的值。", "tformat")

------------------------------------------------

section "tome-orcs/data/timed_effects/physical.lua"

t("technique", "技巧", "effect subtype")
t("Strafing", "扫射中", "_t")
t("The target is moving while shooting, and will reload %sammo when finished strafing.", "目标在移动中射击，效果结束后恢复 %s 弹药。", "tformat")
t("%s reloads.", "%s 装载弹药。", "logSeen")
t("Startled", "惊讶", "_t")
t("The target is startled after being strangely missed by a shot. The next shot it takes will deal %d%% more damage.", "目标因一发子弹莫名其妙地没有命中而受到惊吓。下一发命中它的子弹将额外造成 %d%% 伤害。", "tformat")
t("steamtech", "蒸汽科技", "effect subtype")
t("Iron Grip", "铁腕", "_t")
t("The target has been crushed, pinning it and reducing defense and armour by %d.", "目标被碾压，处于定身状态，护甲和闪避下降 %d。", "tformat")
t("#Target# is crushed by the iron grip.", "#Target# 被铁腕碾压。", "_t")
t("+Iron Grip", "+铁腕", "_t")
t("#Target# is free from the iron grip.", "#Target#从铁腕中脱离。", "_t")
t("-Iron Grip", "-铁腕", "_t")
t("Bullet Mastery: Overheated", "子弹掌握：过热", "_t")
t("Bullets shot are overheated:  When striking their target, they set it on fire for %d fire damage over 5 turns", "发射的子弹处于过热状态：命中目标时会将其点燃，在 5 回合内造成 %d 点火焰伤害。", "tformat")
t("#Target# tweaks some of %s bullets.", "#Target#调整了%s弹药。", "tformat")
t("+Bullet Mastery", "+子弹掌握", "_t")
t("Bullet Mastery: Supercharged", "子弹掌握：超速", "_t")
t("Bullets shot are supercharged:  They can pass through multiple targets and have %d additional armour penetration.", "子弹处于超速状态：能够穿透多个目标，同时提高护甲穿透 %d 点。", "tformat")
t("Bullet Mastery: Percussive", "子弹掌握：冲击", "_t")
t("Bullets shot are percussive:  When striking, they have a %d%% chance to knock back and a %d%% chance to stun.", "子弹处于冲击状态：%d%% 概率击退，%d%% 概率震慑。", "tformat")
t("Bullet Mastery: Combustive", "子弹掌握：爆炸", "_t")
t("Bullets shot are combustive:  When striking their target, they explode (radius 2) for %d fire damage.", "子弹处于爆炸状态：对 2 码范围内的敌人造成 %d 火焰伤害。", "tformat")
t("Uncanny Reload", "神秘装填", "_t")
t("Firing steamguns does not consume shots.", "蒸汽枪不消耗子弹。", "tformat")
t("#Target# is focuses on firing.", "#Target# 集中精力开火。", "_t")
t("+Uncanny Reload", "+神秘装填", "_t")
t("#Target# is less focused.", "#Target#不再集中精力。", "_t")
t("-Uncanny Reload", "-神秘装填", "_t")
t("Cloak", "斗篷", "_t")
t("The target is wrapped in a cloak of shadow, granting sealth.", "目标被暗影披风包裹，获得潜行能力。", "_t")
t("#Target# disappears from sight.", "#Target# 从视线中消失了。", "_t")
t("+Cloak", "+斗篷", "_t")
t("#Target# re-appears.", "#Target# 重新出现了。", "_t")
t("-Cloak", "-斗篷", "_t")
t("nature", "自然", "effect subtype")
t("Pain Suppressor Salve", "痛苦压制药剂", "_t")
t("Fight to the brink of death, can not die before going under -%d life (but life under 0 is not shown) and increases all resistances by %d%%.", "获得 -%d 生命下限（但生命值低于0时不会显示），全部抗性提高 %d%%。", "tformat")
t("#Target# uses a pain suppressor salve.", "#Target# 使用了痛苦压制药剂。", "_t")
t("+Pain Suppressor", "+痛苦压制", "_t")
t("#Target# is not affected anymore by the salve.", "#Target# 不再受药剂影响。", "_t")
t("-Pain Suppressor", "-痛苦压制", "_t")
t("frost", "冰冻", "effect subtype")
t("Frost Salve", "寒霜药剂", "_t")
t("Provides a frost aura, giving you +%d%% cold, nature and darkness affinity.", "提供寒霜光环，使你获得 +%d%% 寒冷、自然和暗影伤害亲和。", "tformat")
t("#Target# uses a frost salve.", "#Target#使用了寒霜药剂。", "_t")
t("+Frost Salve", "+寒霜药剂", "_t")
t("-Frost Salve", "-寒霜药剂", "_t")
t("fire", "火焰", "effect subtype")
t("Fiery Salve", "烈火药剂", "_t")
t("Provides a frost aura, giving you +%d%% fire, light, and lightning affinity.", "提供烈火光环，使你获得 +%d%% 火焰、光系和闪电伤害亲和。", "tformat")
t("#Target# uses a fiery salve.", "#Target# 使用了烈火药剂。", "_t")
t("+Fiery Salve", "+烈火药剂", "_t")
t("-Fiery Salve", "-烈火药剂", "_t")
t("water", "水", "effect subtype")
t("Water Salve", "静水药剂", "_t")
t("Provides a frost aura, giving you +%d%% blight, mind and acid affinity.", "提供静水光环，使你获得 +%d%% 枯萎、精神和酸性伤害亲和。", "tformat")
t("#Target# uses a water salve.", "#Target# 使用了静水药剂。", "_t")
t("+Water Salve", "+静水药剂", "_t")
t("-Water Salve", "-静水药剂", "_t")
t("tech", "科技", "effect subtype")
t("Unstoppable Force Salve", "势不可挡药剂", "_t")
t("Increases all saves by %d and healing factor by %d%%.", "增加全豁免 %d，增加治疗系数 %d%%  。", "tformat")
t("#Target# uses an unstoppable force salve.", "#Target# 使用了势不可挡药剂。", "_t")
t("+Unstoppable Force", "+势不可挡", "_t")
t("-Unstoppable Force", "-势不可挡", "_t")
t("slow", "减速", "effect subtype")
t("Slow Talents", "技能减速", "_t")
t("Attacking, casting and mind speed have been reduced by %d%%.", "攻击，施法和精神速度下降 %d%%。", "tformat")
t("Supercharge Tinkers", "插件超频", "_t")
t("Increases steampower by %d and steam crit by %d%%.", "获得 %d 蒸汽强度和 %d%% 蒸汽技能暴击率。", "tformat")
t("#Target# supercharges all tinkers.", "#Target# 超频了所有配件。", "_t")
t("+Supercharge Tinkers", "+插件超频", "_t")
t("#Target#'s supercharge is fading.", "#Target#的超频正在消退。", "_t")
t("-Supercharge Tinkers", "-插件超频", "_t")
t("Overcharge Saws", "链锯过载", "_t")
t("Increases all saws talent levels by %d%%.", "增加 %d%% 链锯相关技能有效等级。", "tformat")
t("#Target# overcharges saw motors.", "#Target# 超频了链锯引擎。", "_t")
t("+Overcharge Saws", "+链锯过载", "_t")
t("#Target#'s saw motors are back to normal.", "#Target#的链锯引擎恢复常态。", "_t")
t("-Overcharge Saws", "-链锯过载", "_t")
t("ice", "寒冰", "effect subtype")
t("Algid Rage", "寒冰之怒", "_t")
t("You have %d%% chances to encase your foes in iceblocks.", "你造成伤害时有 %d%% 几率将敌人封入冰块 3 回合；效果持续期间，冰块吸收的伤害降低 50%。", "tformat")
t("disease", "疾病", "effect subtype")
t("Larvae Infestation", "里奇幼虫寄生", "_t")
t("The target has been impregnated with %d developing ritch larvae which are feeding on it%s.  After a %d turn gestation period, each will burst out violently, dealing %0.2f physical and %0.2f fire damage to its host.", "目标被 %d 个里奇幼虫寄生%s。在%d回合的发育期结束后，每个幼虫都会从寄主体内猛烈破体而出，对宿主造成 %0.2f 物理和 %0.2f 火焰伤害；即使效果提前解除，幼虫仍可能以较低强度破体而出并生成幼虫。", "tformat")
t(" for %0.2f physical damage (increasing) each turn", " ，每回合受到 %0.2f 物理伤害（随回合递增）", "tformat")
t("#Target# is #ORANGE#INFESTED#LAST# with ritch larvae!", "#Target# 被里奇幼虫#ORANGE#寄生#LAST#！", "_t")
t("+Larvae Infestation", "+里奇幼虫寄生", "_t")
t("developing ", "正在生长的", "_t")
t("A %s #ORANGE#BURSTS OUT#LAST# of %s%s!", "一个%s从%s体内#ORANGE#爆出#LAST#%s！", "logSeen")
t(" but is crushed", "，但被粉碎了", "_t")
t("Tech Overload", "系统过载", "_t")
t("Doubles your maximum steam and stops steam regeneration.", "最大蒸汽值翻倍，并将蒸汽回复减半。", "tformat")
t("Continuous Butchery", "无尽屠戮", "_t")
t("Increases steamsaw damage multiplier by %d%%.", "当前使蒸汽链锯伤害增加 %d%%；每回合首次近战命中指定目标时提高此加成，命中其他敌人则效果结束。", "tformat")
t("wound", "创伤", "effect subtype")
t("cut", "流血", "effect subtype")
t("bleed", "流血", "effect subtype")
t("Explosive Saw", "爆炸飞锯", "_t")
t("Target is being assailed by an automated saw blade that cuts its flesh for %0.2f physical damage each turn%s. When the effect expires, the saw will explode for %0.2f fire damage and fly back to its source, pulling the target with it (up to %d tiles).", "你被飞锯击伤，每回合受到 %0.2f 物理伤害 %s。仅当持续时间自然结束且施加者仍在场时，飞锯才会爆炸，造成 %0.2f 火焰伤害并飞回其来源；仅当你可被击退时，才会被拉向施加者（最多 %d 格）。", "tformat")
t(" and silences it", "并被沉默", "_t")
t("sil", "沉默", "_t")
t("#Target# is assailed by an automated saw blade.", "#Target#被链锯切割。", "_t")
t("+Explosive Wounds", "+爆炸伤口", "_t")
t("The saw embedded in #Target# flies back its source.", "#Target#身上的链锯飞回主人的方向。", "_t")
t("-Explosive Wounds", "-爆炸伤口", "_t")
t("The saw drags #Source# towards #Target#!", "链锯将#Source#拖向#Target#！", "logCombat")
t("resistance", "抵抗", "effect subtype")
t("Subcutaneous Metallisation", "金属内皮", "_t")
t("All damage reduced by %d.", "全伤害减免%d。", "tformat")
t("#Target# internal structure metallises.", "#Target# 内在结构金属化。", "_t")
t("+Subcutaneous Metallisation", "+金属内皮", "_t")
t("#Target# internal structure returns to normal.", "#Target# 内在结构恢复正常。", "_t")
t("-Subcutaneous Metallisation", "-金属内皮", "_t")
t("power", "强度", "effect subtype")
t("Pain Enhancement System", "痛苦强化系统", "_t")
t("All stats increased by %d.", "除力量外的所有属性增加 %d。", "tformat")
t("#Target# revels in the pain.", "#Target# 在苦痛中狂欢。", "_t")
t("+Pain Enhancement System", "+痛苦强化系统", "_t")
t("#Target# no longer feels strong.", "#Target# 不再强壮。", "_t")
t("-Pain Enhancement System", "-痛苦强化系统", "_t")
t("pin", "定身", "effect subtype")
t("Net Projector", "束网弹射器", "_t")
t("The target has been pinned by an electrified net, reducing all resistances by %d%%.", "目标被带电的网定身，所有抗性降低 %d%%。", "tformat")
t("#Target# is trapped by the net.", "#Target# 被网住了。", "_t")
t("+Net Projector", "+束网弹射器", "_t")
t("#Target# is free from the net.", "#Target#从网中脱离了。", "_t")
t("-Net Projector", "-束网弹射器", "_t")
t("Molten Point", "融化点数", "_t")
t("You have %d charges.", "叠加次数：%d。", "tformat")
t("steam", "蒸汽", "effect subtype")
t("Pressure-enhanced Slashproof Combat Suit", "压力强化型防斩击作战服", "_t")
t("psionic", "灵能", "effect subtype")
t("Molten Iron Blood", "铁水血液", "_t")
t("All resistances increased by %d%%, all new detrimental effects reduced by %d%%, %0.2f fire splash damage.", "全部抗性提高 %d%%，新施加的负面效果持续时间缩短 %d%%，近战命中持有者的生物受到 %0.2f 点火焰伤害。", "tformat")
t("#Target#'s blood turn into molten iron.", "#Target#的血液变成了融化的铁水。", "_t")
t("#Target# no longer has molten iron blood.", "#Target#的血液不再是融化的铁水。", "_t")
t("Seared", "烧焦", "_t")
t("Fire resistance decreased by %d%% and mind save by %d.", "火焰抗性下降 %d%%，精神豁免下降 %d。", "tformat")
t("#Target# is seared.", "#Target# 烧焦了。", "_t")
t("#Target# is no longer seared.", "#Target# 不再烧焦。", "_t")
t("awesome", "惊人", "effect subtype")
t("Awesome Toss", "致命翻转", "_t")
t("All resistances increased by %d%%, randomly attacks two foes each turn at random.", "全部抗性提高 %d%%，两把蒸汽枪每回合各自随机选择一名敌人攻击（可能攻击同一目标），持有者被缴械。", "tformat")
t("#Target# tosses steamguns in the air, awesome!", "#Target#将蒸汽枪抛向空中，太帅了！", "_t")
t("#Target# somehow catches the falling steamguns.", "#Target# 接住了蒸汽枪。", "_t")
t("Marked for Death", "死亡标记", "_t")
t("Ranged defense reduced by %d, takes %d%% extra damage from all sources.", "远程闪避减少 %d，受到额外 %d%% 伤害。", "tformat")
t("#Target# is marked!", "#Target# 被标记了！", "_t")
t("+Marked for Death", "+死亡标记", "_t")
t("powder", "粉末", "effect subtype")
t("Itching Powder", "痒痒粉", "_t")
t("The target is very itchy, causing their actions to fail.", "太痒了，技能有几率施放失败。", "tformat")
t("#Target# is very itching!", "#Target# 非常痒！", "_t")
t("+Itching Powder", "+痒痒粉", "_t")
t("#Target# regains their concentration.", "#Target#恢复了注意力。", "_t")
t("-Itching Powder", "-痒痒粉", "_t")
t("Smoke Cover", "烟雾覆盖", "_t")
t("%d%% chance to fully absorb any damaging actions, %d stealth value.", "%d%% 几率吸收伤害，%d 潜行强度。", "tformat")
t("#Target# is hiding in smoke.", "#Target# 在烟雾中隐藏。", "_t")
t("+Smoke Cover", "+烟雾覆盖", "_t")
t("#Target# is no longer hiding in smoke.", "#Target# 不再隐藏于烟雾中。", "_t")
t("-Smoke Cover", "-烟雾覆盖", "_t")
t("Magnetised", "磁化", "_t")
t("The target has been magnetised, reducing defense by %d and increasing fatigue by %d.", "目标被磁化，闪避下降 %d，疲劳增加 %d。", "tformat")
t("#Target# is magnetised.", "#Target# 被磁化了。", "_t")
t("+Magnetised", "+磁化", "_t")
t("#Target# is free from the magnetism.", "#Target# 从磁化中解脱。", "_t")
t("-Magnetised", "-磁化", "_t")
t("blood", "血", "effect subtype")
t("drain", "吸血", "effect subtype")
t("heal", "治疗", "effect subtype")
t("Bloodstar", "血液灵晶", "_t")
t("Continuously drain blood, dealing %0.2f physical damage per turn and healing the caster for half of it.", "持续汲取目标的鲜血，每回合造成 %0.2f 点物理伤害；若施加者距离过远、死亡或不在场，链接立即断开且本回合不造成伤害；造成伤害后，施加者获得相当于该伤害一半的治疗，同回合每多一个目标，治疗量在前一目标基础上再减半。", "tformat")
t("#Target# is caught in the bloodstar.", "#Target# 被血液灵晶抓住了。", "_t")
t("#Target# is free from the bloodstar.", "#Target# 从血液灵晶中解脱。", "_t")
t("Heartrended", "心脏切割", "_t")
t("Vicious cut that bleeds, doing %0.2f physical damage per turn.", "恶毒的伤口在流血，每回合造成 %0.2f 物理伤害。", "tformat")
t("#Target# starts to bleed.", "#Target#开始流血。", "_t")
t("+Bleeds", "+流血", "_t")
t("#Target# stops bleeding.", "#Target#停止流血。", "_t")
t("-Bleeds", "-流血", "_t")
t("poison", "毒素", "effect subtype")
t("blight", "枯萎", "effect subtype")
t("Metal Poisoning", "金属中毒", "_t")
t("The target is poisoned with heavy metals, taking %0.2f blight damage per turn and decreasing their global speed by %d%%.", "目标重金属中毒，每回合受到 %0.2f 枯萎伤害，整体速度下降 %d%%。", "tformat")
t("#Target# is poisoned!", "#Target#中毒了！", "_t")
t("+Metal Poisoning", "+金属中毒", "_t")
t("#Target# is no longer poisoned.", "#Target#中毒效果消失。", "_t")
t("-Metal Poisoning", "-金属中毒", "_t")
t("moss", "苔藓", "effect subtype")
t("Moss Tread", "苔藓之踏", "_t")
t("You lay moss where you walk.", "成功自行移动到新位置后，会在该处铺设缠绕苔藓；站在其上的敌人会受到自然伤害、移动减速，并可能被定身。", "tformat")
t("+Moss", "+苔藓", "_t")
t("-Moss", "-苔藓", "_t")
t("Stimulus", "兴奋剂", "_t")
t("Resisting pain, reducing all incoming damage by %0.2f. When the effect ends, take %d un-resistable damage.", "抵抗疼痛，受到的伤害减少 %0.2f。效果结束后受到 %d 点无法抵抗的伤害。", "tformat")
t("maimed", "被致残", "effect subtype")
t("To The Arms", "切臂", "_t")
t("Damage reduced by %d%%.", "伤害减少 %d%%。", "tformat")
t("#Target# is suffering and fails to concentrate on dealing damage.", "#Target# 忍受痛苦，不能集中精力制造伤害。", "_t")
t("#Target# is suffering less.", "#Target#的痛苦减轻了。", "_t")
t("acid", "酸性", "effect subtype")
t("Acid Burn", "酸液灼烧", "_t")
t("The target has been splashed with acid, taking %0.2f acid damage per turn.", "目标被酸液溅射，每回合受到 %0.2f 酸性伤害。", "tformat")
t("#Target# is covered in acid!", "#Target#被酸液覆盖！", "_t")
t("#Target# is free from the acid.", "#Target#身上的酸液消失了。", "_t")
t("lightning", "闪电", "effect subtype")
t("Static Shield", "静电力场", "_t")
t("The target is surrounded by a static shield, increasing all resistances by %d%% and causing attacks against them to trigger a shield attack for %d%% damage as lightning.", "目标被静电力场包围，增加全部抗性 %d%%；受到攻击时，将使用原施放者的盾牌造成 %d%% 伤害的闪电反击，且同一攻击者每回合最多触发一次。", "tformat")
t("A static shield forms around #target#.", "静电力场环绕着#target#。", "_t")
t("+Static Shield", "+静电力场", "_t")
t("The static shield around #target# crumbles.", "#target#周围的静电力场破碎了。", "_t")
t("-Static Shield", "-静电力场", "_t")
t("Lightning Web", "闪电之网", "_t")
t("The target is surrounded by a crackling web of lightning, reducing all damage taken by %d.", "目标被闪电之网覆盖，减少所受到的所有伤害 %d。", "tformat")
t("#LIGHT_BLUE#(%d lightning web)#LAST#", "#LIGHT_BLUE#(%d闪电之网)#LAST#", "tformat")
t("Incendiary Grenade", "燃烧榴弹", "_t")
t("The target is burning for %d fire damage each turn and taking %d%% increased damage from all sources.", "目标被点燃，每回合受到 %d 火焰伤害，所受到的所有伤害增加 %d%%。", "tformat")
t("Healing Mist", "治愈之雾", "_t")
t("Newly applied status effects durations are reduced by %d%%.", "新施加的负面效果持续时间缩短 %d%%。", "tformat")
t("#ORCHID#%s has recovered!#LAST#", "#ORCHID#%s恢复了！#LAST#", "logSeen")
t("shield", "护盾", "effect subtype")
t("Overclock", "炮台超载", "_t")
t("The target is surrounded by a charged shield, absorbing %d/%d damage before it crumbles. While this holds, they will project a bolt of lightning against a random enemy within range 7 each turn for %0.2f lightning damage.", "目标被充能护盾覆盖，在破碎前可以吸收 %d/%d 伤害。当护盾存在时，他们每回合会朝 6 码范围内的随机敌人发射闪电弹，造成 %0.2f 闪电伤害。", "tformat")
t("#target# surges with power!", "#target#力量强化！", "_t")
t("+Overclock", "+炮台超载", "_t")
t("#target# looks less powerful.", "#target#力量消退了。", "_t")
t("-Overclock", "-炮台超载", "_t")
t("#SLATE#(%d absorbed)#LAST#", "#SLATE#(%d 护盾吸收)#LAST#", "tformat")
t("Your shield crumbles under the damage!", "你的护盾在攻击下被打破！", "logPlayer")
t("sense", "感知", "effect subtype")
t("Hypervision Goggles", "强化视觉护目镜", "_t")
t("Improves senses, allowing the detection of enemies in radius %d and increasing resistance penetration by %d%%.", "强化感知，侦测半径 %d 码范围内的所有敌人，增加抗性穿透 %d%%。", "tformat")
t("AED", "电击除颤器", "_t")
t("If life is brought below 0, cancels the attack, heals for %d and deals %0.2f lightning damage in radius %d as well as dazing for 2 turns.", "若生命值降至 0 以下，则取消此次攻击、恢复 %d 点生命值，并在 %d 格范围内造成 %0.2f 点闪电伤害，同时使目标眩晕 3 回合。", "tformat", {1,3,2})
t("#Target# prepares their AED!", "#Target#准备电击除颤器！", "_t")
t("+AED", "+电击除颤器", "_t")
t("#Target#'s AED deactivates.", "#Target#的电击除颤器解除了。", "_t")
t("-AED", "-电击除颤器", "_t")
t("%s's AED triggers!", "%s的电击除颤器触发了！", "logSeen")
t("Burning Phosphorous", "燃烧的磷", "_t")
t("The target is covered in burning chemicals, taking %0.2f fire damage each turn. Subsequent shots deal %0.2f fire damage, and if they fall below 25%% life they have a %d%% chance to panic.", "目标被燃烧的化学物质所覆盖，每回合受到 %0.2f 火焰伤害。之后的射击会立即造成 %0.2f 火焰伤害；施加者死亡后，该效果会在目标下次行动时结束。若目标生命值低于 25%% 且能够行动，则有 %d%% 的几率慌乱逃跑。", "tformat")
t("#F53CBE#%s resists the fear.", "#F53CBE#%s抵抗恐惧。", "logSeen")
t("#F53CBE#%s panics and flees from %s!", "#F53CBE#%s恐惧，试图逃离%s！", "logSeen")
t("#F53CBE#%s panics but fails to flee from %s!", "#F53CBE#%s恐惧，未能逃离%s！", "logSeen")
t("Scorched", "灼烧", "_t")
t("Fire resistance decreased by %d%%.", "火焰伤害抗性降低%d%%。", "tformat")
t("#Target# is scorched.", "#Target#被火焰灼烧。", "_t")
t("#Target# is no longer scorched.", "#Target#不再被灼烧。", "_t")
t("grapple", "抓取", "effect subtype")
t("Pincer Strike", "钢爪钳制", "_t")
t("The target is grappled by %s, pinning them, reducing attack, spell and mind speed by %d%% and subjecting them to an automatic tailsaw strike each turn for %d%% damage.", "目标被 %s 抓取，被定身，降低战斗、法术和精神速度 %d%%，并每回合受到一次自动的尾部链锯打击，造成 %d%% 伤害。", "tformat")
t("%s clamps its pincers down on #Target#!", "%s使用钢爪钳制#Target#！", "tformat")
t("+Pincer Strike", "+钢爪钳制", "_t")
t("#Target# is free from %s's pincers.", "#Target#脱离%s的钢爪。", "tformat")
t("-Pincer Strike", "-钢爪钳制", "_t")
t("#Source# #LIGHT_RED#strikes down at#LAST# #Target#!", "#Source# #LIGHT_RED#打击#LAST# #Target#！", "logCombat")
t("Reactive Armor", "反应式装甲", "_t")
t("Next melee or ranged attack that deals more than 8%% of maximum life is reduced by %d%% and triggers a radius %d conal explosion dealing %d%% steamgun damage. %d stacks remaining.", "下一次受到的近战或远程攻击若造成至少相当于最大生命值 8%% 的伤害，则会降低 %d%% 伤害，并触发一次半径为 %d 的扇形爆炸，造成 %d%% 蒸汽枪伤害。每回合最多触发一次。剩余 %d 层叠加。", "tformat")
t("#LIGHT_BLUE#(%d reactive armor)#LAST#", "#LIGHT_BLUE#(%d 反应式装甲)#LAST#", "tformat")
t("Grenade Barrage", "榴弹轰炸", "_t")
t("Attack speed increased by %d%%. Next %d shot(s) trigger a grenade.", "攻击速度增加 %d%%。接下来使用射击、火焰喷射、暴风打击或毒弹爆射中的任意技能 %d 次会触发榴弹射击。", "tformat")
t("#Target# loads a magazine of grenades.", "#Target#装载一大包榴弹。", "_t")
t("+Grenade Barrage", "+榴弹轰炸", "_t")
t("Miasma Adaptation", "适应瘴气", "_t")
t("Immune to miasma engine effects.", "免疫瘴气引擎效果。", "_t")
t("Miasma Engine", "瘴气引擎", "_t")
t("The target is surrounded by a toxic cloud or radius %d. Enemies within will suffer %d%% talent failure, %d%% reduced healing, and take %0.2f additional acid damage from melee and ranged attacks.", "目标被半径为 %d 的瘴气毒云包围。被困在其中的敌人会有 %d%% 的技能失败几率，降低%d%% 治疗效果，并且在受到近战和远程攻击的时候受到 %0.2f 额外酸性伤害。", "tformat")
t("Smogscreen", "蔽目毒云", "_t")
t("%d%% chance to fully absorb any damaging actions.", "%d%% 几率完全吸收任何伤害。", "tformat")
t("Miasma", "瘴气", "_t")
t("Affected by toxic chemicals. Has %d%% talent failure, %d%% reduced healing, and takes %0.2f additional acid damage from melee and ranged attacks.", "被有毒化学物质影响。%d%% 技能失败率，降低 %d%% 治疗效果，每回合第一次被带有武器类型的近战或远程攻击命中时，受到额外 %0.2f 酸性伤害。", "tformat")
t("Death From Above", "死亡天降", "_t")
t("Hovering in place, gaining %d%% evasion, %d%% movement speed and launching a powerful rocket barrage each turn.", "目标悬浮在空中，获得 %d%% 躲闪概率，%d%% 移动速度；可手动使用火箭弹幕再次发射，使用其他任何技能会立即结束该效果。", "tformat")
t("#Target# takes flight!", "#Target#起飞！", "_t")
t("+Death From Above", "+死亡天降", "_t")
t("#Target# lands.", "#Target# 落地。", "_t")
t("-Death From Above", "-死亡天降", "_t")
t("Corrosive Flechette", "腐蚀性毒镖", "_t")
t("%d corrosive flechettes are embedded in the target. Each melee and ranged attack against them will cause a flechette to burst for %0.2f acid damage", "目标体内嵌有 %d 枚腐蚀性毒镖。敌方单位的近战或远程攻击命中目标时，其中一枚毒镖会爆裂，造成 %0.2f 点酸性伤害。", "tformat")

------------------------------------------------

section "tome-orcs/data/tinkers/therapeutics.lua"

t("Healing Salve", "治疗药剂", "_t")
t([[A powerful healing salve.
To be used with the medical injector implant.]], [[一个强大的治疗药剂。
需通过医疗注射器植入体使用。]], "_t")
t("Pain Suppressor Salve", "痛苦压制药剂", "_t")
t([[A powerful salve that steels your body for a while, letting you survive below 0 life while increasing resistances.
To be used with the medical injector implant.]], [[一种能暂时强化你身体的强力药剂，它可以让你在 0 生命值以下时仍然存活，并提升你的伤害抗性。
需通过医疗注射器植入体使用。]], "_t")
t("Frost Salve", "寒霜药剂", "_t")
t([[A powerful salve that can clean physical detrimental effects from your body and grant a frost aura (cold, darkness and nature affinity).
To be used with the medical injector implant.]], [[一个可以清除你身上的负面物理效果并获得一个寒霜光环（增加寒冷、暗影和自然伤害亲和）的强大药剂。
需通过医疗注射器植入体使用。]], "_t")
t("Fiery Salve", "烈火药剂", "_t")
t([[A powerful salve that can clean magical detrimental effects from your body and grant a fiery aura (fire, light and lightning affinity).
To be used with the medical injector implant.]], [[一个可以清除你身上的负面魔法效果并获得一个烈火光环（火焰、光系、闪电伤害亲和）的强大药剂。
需通过医疗注射器植入体使用。]], "_t")
t("Water Salve", "静水药剂", "_t")
t([[A powerful salve that can clean mental detrimental effects from your body and grant a water aura (blight, mind and acid affinity).
To be used with the medical injector implant.]], [[一个可以清除你身上的负面精神效果并获得一个静水光环（枯萎、精神、酸性伤害亲和）的强大药剂。
需通过医疗注射器植入体使用。]], "_t")
t("Unstoppable Force Salve", "势不可挡药剂", "_t")
t([[A powerful salve that makes you more resilient to physical, mental and magic effects and grants increased healing.
To be used with the medical injector implant.]], [[一个增强你对物理、精神和魔法效果的抵抗能力并增加你的治疗效果的强大药剂。
需通过医疗注射器植入体使用。]], "_t")
t("frost salve", "寒霜药剂", "_t")
t("fiery salve", "烈火药剂", "_t")
t("water salve", "静水药剂", "_t")
t("Poison Groove", "淬毒凹槽", "_t")
t("Poison grooves can be attached to weapons to apply a stacking poison on attacks.  While this is ideal for stacking simple damage, you can't help but wonder if you could inflict stronger effects with more knowledge..", "淬毒凹槽可以安装在武器上，使攻击施加可叠加的中毒效果。虽然它很适合不断叠加简单伤害，但你不禁想，掌握更多知识后是否能施加更强大的效果……", "_t")
t("Viral Injector", "病毒注射器", "_t")
t("Viral grooves allow your weapons to apply an infectious agent on contact, dealing immediate blight damage and reducing their highest stat.  While this strain is effective it lacks the ability to spread or adapt to its hosts weaknesses.  Perhaps there are better methods to be found.", "病毒之槽可以让你的武器攻击附带病毒效果，立即造成枯萎伤害并降低他们最高的数值。尽管这个方法行之有效，但它缺乏传播和适应宿主的弱点的能力。或许还有更好的方法…", "_t")
t("Life Support Suit", "生命支持服", "_t")
t("Apply your extensive therapeutics knowledge to try and defeat death itself!", "应用你广泛的医疗知识，击败死亡本身！", "_t")
t("unstoppable force salve", "势不可挡药剂", "_t")
t("fire opal", "火蛋白石", "_t")
t("pearl", "珍珠", "_t")
t("diamond", "钻石", "_t")
t("bloodstone", "血滴石", "_t")
t("Second Skin", "第二皮肤", "_t")
t("Not only does it help seal wounds, protecting you from bleeding and enhancing your healing, it also protects from armour chafe!", "它不仅能封住伤口、防止流血并增强治疗效果，还能防止盔甲擦伤皮肤！", "_t")
t("Air Recycler", "空气循环装置", "_t")
t("Helps keep your airway open and lets you hold your breath longer.", "有助于保持呼吸道畅通，并让你屏息更久。", "_t")
t("Moss Tread", "苔藓之踏", "_t")
t("Where you walk nature grows! Well moss. Sticky moss.", "你走到哪里，哪里就一片绿荫…虽然那是粘粘的苔藓。", "_t")
t("Fungal Web", "真菌之网", "_t")
t("This mesh of fungal threads absorbs nutrients for salves to provide you with added healing!", "这层真菌丝网能为药剂吸收养分，从而为你提供额外治疗！", "_t")

------------------------------------------------

section "tome-orcs/data/zones/gates-of-morning/grids.lua"

t("floor", "地板", "entity type")
t("floor", "地板", "entity subtype")
t("old road", "古老的路", "entity name")
t("rockwall", "岩石墙", "entity type")
t("grass", "草地", "entity subtype")
t("Sunwall mountain", "太阳堡垒群山", "entity name")
t("Way into the caves", "通往洞穴的道路", "entity name")
t("Farportal: Last Hope", "远行传送门：最后的希望", "entity name")
t([[A farportal is a way to travel incredible distances in the blink of an eye. They usually require an external item to use. You have no idea if it is even two-way.
This one seems to go near the town of Last Hope in Maj'Eyal.]], [[远行传送门能让人眨眼间跨越难以想象的距离。它们通常需要借助外部物品才能使用。你甚至不知道它是否能双向通行。
这座传送门似乎通往马基·埃亚尔最后的希望城附近。]], "_t")
t("#VIOLET#You enter the swirling portal and in the blink of an eye you set foot on the outskirts of Last Hope, with no trace of the portal...", "#VIOLET#你进入了传送漩涡，一眨眼功夫你回到了最后的希望的郊外，传送的踪迹再不可寻……", "_t")
t("wall", "墙壁", "entity type")
t("cracks", "裂缝", "entity subtype")
t("huge crack in the floor", "地面上的巨大裂缝", "entity name")

------------------------------------------------

section "tome-orcs/overload/mod/class/OrcCampaign.lua"

t("Steam", "蒸汽", "_t")
t("Your reserve of steam. Steam is used to power most technological things. It is very hard to increase your maximum steam, but it regenerates quickly.", "你的蒸汽存量。蒸汽用于驱动各种技术产品。很难提升你的最大蒸汽储量，但蒸汽可以被快速补充。", "_t")
t("Tail", "尾巴", "_t")
t("Object held in your tail. It can be a steamgun or steamsaw.", "在你尾巴上装备的物品。可以装备蒸汽枪或蒸汽链锯。", "_t")
t("SteamTech", "蒸汽科技", "_t")
t("Steampower: #00ff00#%s", "蒸汽强度：#00ff00#%s", "tformat")
t("Crit. chance: #00ff00#%s", "暴击率：#00ff00#%s", "tformat")
t("Steam speed : #00ff00#%s", "蒸汽速度：#00ff00#%s", "tformat")
t("Powered by ", "力量来源", "_t")
t("steamtech", "蒸汽科技", "_t")
t("%+d #LAST#(%+d eff.)", "%+d#LAST#(%+d有效值)", "_t")
t("Steampower: ", "蒸汽强度：", "_t")
t("Steam crit. chance: ", "蒸汽暴击几率：", "_t")
t("Steamtech Speed: ", "蒸汽速度：", "_t")
t("Steam each turn: ", "每回合蒸汽回复：", "_t")
t("Maximum steam: ", "蒸汽容量：", "_t")
t("You may not shoot while using a heavy weapon.", "使用重装武器的时候，你无法使用普通射击。", "logPlayer")
t("lost tinker", "迷路的工匠", "_t")
t("Please help me! I am afraid I lost myself in this place while testing some new steamtech. I know there is a recall portal left around here by a friend, but I have fought too many battles, and I fear I will not make it. Would you help me?", "帮帮我！我在测试某种蒸汽科技，结果在这地方迷路了。我有个朋友给我留下了一个传送门，不过我打了太多仗，恐怕靠我自己是到不了那里了，你能帮我一下吗？", "_t")
t("%s, the experimenting tinker", "%s，实验的工匠", "_t")
t("She looks tired and wounded.", "她看起来疲惫又受伤。", "_t")
t("[Ask where to learn tinkers crafting]", "[问她哪里可以学到蒸汽技术]", "_t")
t("Reveal the location of a teacher.", "揭示工匠大师的位置。", "_t")
t("Tinker's Master", "工匠大师", "_t")
t("She points a location on your map, in a remote area to the north.", "她指出了地图上的一个位置，在北方的某地。", "_t")
t("You are given a strange metal contraption, explaining that using it will transport you to tinker's cave.", "你获得了一个奇怪的金属装置，使用它可以进入工匠大师的山洞。", "_t")
t("gained knowledge of tinker technology", "获得蒸汽科技的奥秘", "_t")
t("Steamtech", "蒸汽科技", "_t")
t("I've changed my mind.", "我改变主意了。", "_t")
t("Which kind of item would you like ?", "你想要哪种类型的装备？", "_t")
t("#CRIMSON#Your timetravel has no effect on pre-determined outcomes such as this.", "#CRIMSON#你的时间穿越对这种已经预设好的结局没有任何作用。", "_t")
t([[Do you want to name your item?
%s]], [[你想要命名你的物品吗？
%s]], "tformat")
t("Yes, please.", "是的。", "_t")
t("Name your item", "为你的装备命名", "_t")
t("Name", "名称", "_t")
t("#LIGHT_BLUE#The merchant carefully hands you: %s", "#LIGHT_BLUE#商人小心地交给了你：%s", "log")
t("No thanks.", "不用了，谢谢。", "_t")
t("Oh I am sorry, it seems we could not make the item your require.", "啊真抱歉，看来我们无法制作你所要求的装备。", "_t")
t("Oh, let's try something else then.", "好吧，我们试试别的东西。", "_t")
t("Oh well, maybe later then.", "好吧，以后再说。", "_t")

------------------------------------------------

section "tome-orcs/superload/mod/class/Actor.lua"

t("#FFD700#St. power#FFFFFF#: ", "#FFD700#蒸汽强度#FFFFFF#: ", "_t")
t("Kruk Invasion", "克鲁克入侵", "_t")
t("You can not recall until you have placed the bomb at the tunnel's end!", "你只有在隧道尽头放置炸弹之后，才能启用回归之杖！", "_t")
t("scroll", "卷轴", "_t")
t("This parchment contains some lore.", "这张卷轴里包含了一些手札。", "_t")
t("time-warped paper scrap", "被时间扭曲的纸片", "_t")
t("It came a long way away!", "它远道而来！", "_t")
t("#LIGHT_BLUE#Spacetime shudders for an instant as a note falls out from a different timeline!", "#LIGHT_BLUE#时空发生了一瞬间的震动，一张纸条从另一个时间线掉了出来！", "saySimple")
t("You gain %0.2f gold from the melting of %s.", "你回收了%s，获得了%0.2f金币。", "log", {2,1})
t("When you close the inventory window, all items in the APE will be melted.", "当你关闭物品栏的时候，所有APE里面的物品都会被分解。", "_t")
t("melt down", "融解", "_t")
-- untranslated text
--[==[
t("APE", "APE", "_t")
--]==]


------------------------------------------------

section "tome-possessors/data/birth/psionic.lua"

t("Possessor", "占据者", "birth descriptor name")
t("#CRIMSON#BEWARE: This class is very #{italic}#strange#{normal}# and may be confusing to play for beginners.#LAST#", "#CRIMSON#注意: 该职业机制相当 #{italic}#奇怪#{normal}#，可能不适合新手使用。#LAST#", "_t")
t("Possessors are a rare breed of psionics. Some call them body snatchers. Some call them nightmarish.", "占据者是一类极其稀有的灵能力者。有些人称其为身体掠夺者，有些人视其为噩梦。", "_t")
t("They are adept at stealing their foes corpses for their own use. Discarding their own bodies for a while to use other's.", "他们擅长偷取敌人死亡后的身体，能暂时抛弃自己的躯体，使用其他身体。", "_t")
t("Their most important stats are: Willpower and Cunning", "他们最重要的属性是：意志和灵巧。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +2 Strength, +2 Dexterity, +0 Constitution", "#LIGHT_BLUE# * +2 力量 , +2 敏捷 , +0 体质", "_t")
t("#LIGHT_BLUE# * +0 Magic, +3 Willpower, +2 Cunning", "#LIGHT_BLUE# * +0 魔法 , +3 意志 , +2 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# -4", "#GOLD#每等级生命加值：#LIGHT_BLUE# -4", "_t")

------------------------------------------------

section "tome-possessors/data/talents/psionic/deep-horror.lua"

t("Mind Steal", "精神窃取", "talent name")
t("%s resists the mind steal!", "%s抵制了精神窃取！", "logSeen")
t("%s has no stealable talents.", "%s没有可以窃取的技能。", "logPlayer")
t("Mind Steal", "精神窃取", "_t")
t("Choose a talent to steal:", "选择要窃取的技能：", "_t")
t([[Your mere presence is a blight in your foes minds. Using this link you are able to reach out and steal a talent from a target.
		For %d turns you will be able to use a random active (not passive, not sustained) talent from your target, and they will loose it.
		You may not steal a talent which you already know.
		The stolen talent will not use any resources to activate.
		At level 5 you are able to choose which talent to steal.
		The talent stolen will be limited to at most level %d.]], [[链接目标，偷取目标一个技能。
		持续 %d 回合，你获得目标一个随机主动技能（非被动，非持续），目标会失去该技能。
		你不会偷取一个已有的技能。
		偷取的技能不消耗任何能量。
		在等级 5 时，可选择偷取的技能。
		偷取的技能等级被限制成最高为 %d 级。]], "tformat")
t("Spectral Dash", "幽灵冲锋", "talent name")
t([[For a brief moment your whole body becomes etheral and you dash into a nearby creature and all those in straight line behind it (in range %d).
		You reappear on the other side, with %d more psi and having dealt %0.2f mind damage to your targets.
		]], [[短暂的一瞬间，你的整个身体变得飘渺，你对附近一个生物进行一次直线冲锋 (范围 %d)。
		你再次出现在另一边，获得 %d 灵能值并对目标造成 %0.2f 精神伤害。
		]], "tformat")
t("Writhing Psionic Mass", "扭动灵能团", "talent name")
t([[Your physical form is but a mere extension of your mind, you can bend it at will for %d turns.
		While under the effect you gain %d%% all resistances and have %d%% chance to ignore all critical hits.
		On activation you also remove up to %d physical or mental effects.
		]], [[你的身体形态只不过是你心灵的延伸，你可以随意扭曲它 %d 回合。
		效果生效时，你全部抗性提升 %d%% 并有 %d%% 几率避免被暴击。
		激活时，你最多可以移除 %d 个物理或者精神效果。
		]], "tformat")
t("Ominous Form", "不祥躯体", "talent name")
t("You are already assuming a form.", "你已经占据了一个躯体。", "logPlayer")
t("%s resists your attack!", "%s抵抗了你的攻击！", "logPlayer")
t([[Your psionic powers have no limits. You are now able to assault a target and clone its body without killing it.
		The form is only temporary, lasting %d turns and subject to the same restrictions as your normal powers.
		While using a stolen form your health is bound to your target. (Your life%% will always be identical to your target's life%%)
		]], [[你的灵能力量没有限制。你现在能够攻击一个目标，克隆它的身体，且不需要杀死它。
		身体只是暂时的，持续 %d 回合并受到你正常力量的限制。
		该身体的生命值与你目标的生命值绑定在一起。（你的血量百分比和目标的血量百分比相同）
		]], "tformat")

------------------------------------------------

section "tome-possessors/data/talents/psionic/possession.lua"

t("Possession Talent %d", "附身技能%d", "tformat")
t("You must assume a form to use that form's talents.", "你必须占据一个身体才能使用这个身体的技能。", "logPlayer")
t([[When you assume a form, this talent will be replaced with one of the body's talents.
			The only use for this talent is to pre-organize your hotkeys bar.]], [[附身时，该技能会被替换成身体的其中一个技能。
			该技能的唯一用法是放在热键栏上。]], "tformat")
t("none", "没有", "_t")
t("\
%s%s%d)%s#LAST# (#LIGHT_BLUE#lv %d#LAST#, #LIGHT_RED#HP:%d/%d#LAST#)", "\
%s%s%d)%s#LAST# (#LIGHT_BLUE#等级 %d#LAST#, #LIGHT_RED#生命值:%d/%d#LAST#)", "tformat")
t("Destroy Body", "摧毁身体", "talent name")
t("You have no stored bodies to delete.", "你没有存储的身体，无需删除。", "logPlayer")
t([[Discard a body from your psionic reserve.
		Bodies possessed:
		%s]], [[从你的灵能仓库中丢弃身体。
		拥有的身体 :
		%s]], "tformat")
t("Assume Form", "附身", "talent name")
t("You have no stored bodies to use.", "你没有可以用于附身的身体。", "logPlayer")
t("#CRIMSON#A strange feeling comes over you as two words imprint themselves on your mind: '#{italic}#Not yet.#{normal}#'", "#CRIMSON#一种奇怪的感觉油然而生，两个词印入你的脑海：“#{italic}#还不是时候。#{normal}#”", "logPlayer")
t([[You call upon one of your reserve bodies, assuming its form.
		A body used this way may not be healed in any way.
		You can choose to exit the body at any moment by using this talent again, returning it to your reserve as it is.
		When you reach 0 life you are forced out of it and the shock deals %d%% of the maximum life of your normal body to you while reducing your movement speed by 50%% and your damage by 60%% for 6 turns.
		The cooldown only starts when you resume your normal form.
		While in another body all experience you gain still goes to you but will not be applied until you revert back.
		While in another body your currently equiped objects are #{italic}#merged#{normal}# in you, you can not take them of or wear new ones.
		Bodies possessed:
		%s]], [[选择一个身体，附身。
		以这种方式使用的身体不能以任何方式被治愈。
		你可以随时通过再次使用这个技能来选择退出身体，将其按原样送回你的备用身体库。
		当生命为 0 时被迫离开身体，冲击对你最大血量造成 %d%% 的损失并降低 50%% 移动速度和 60%% 伤害，持续 6 回合。
		技能冷却仅在恢复正常形式时开始冷却。
		附身时仍会获得经验，但不会被应用，直到你离开身体。
		附身时你现有的装备被#{italic}#合并#{normal}#到你身上，你无法更换装备。
		拥有的身体 :
		%s]], "tformat")
t("Possess", "附身", "talent name")
t("You do not have enough room in your bodies storage.", "你的身体存储空间不够。", "logPlayer")
t("This creature is immune to possession.", "这个生物免疫附身。", "logPlayer")
t("You may not possess a creature which you summoned.", "你不能附身你自己召唤的生物。", "logPlayer")
t("You may not possess a creature which has an expiration time or a master.", "你不能附身有时间限制或者主人的生物。", "logPlayer")
t("You may not possess a creature of this rank (%s%s#LAST#).", "你不能附身这个阶级的生物（%s%s#LAST#）。", "logPlayer")
t("Possess", "附身", "_t")
t("Permanently learn to possess creatures of type #LIGHT_BLUE#%s#LAST# (you may only do that a few times, based on talent level) ?", "确认要永久性地学习占据#LIGHT_BLUE#%s#LAST#身体的能力吗（你只能学习有限次，基于技能等级）？", "tformat")
t("No", "否", "_t")
t("Yes", "是", "_t")
t("You may not possess this kind of creature.", "你不能附身这类生物。", "logPlayer")
t("You have no more room available to store a new body.", "你没有足够的位置来存放新的身体。", "logPlayer")
t("Your target is dead!", "你的目标死了！", "logPlayer")
t([[You cast a psionic web at a target that lasts for %d turns. Each turn it deals %0.2f mind damage.
		If the target dies with the web in place you will capture its body and store it in a hidden psionic reserve.
		At any further time you can use the Assume Form talent to temporarily shed your own body and assume your new form, strengths and weaknesses both.
		You may only use this power if you have room for a new body in your storage.

		You may only steal the body of creatures of the following rank %s%s#LAST# or lower.
		At level 3 up to rank %s%s#LAST#.
		At level 5 up to rank %s%s#LAST#.
		At level 7 up to rank %s%s#LAST#.

		You may only steal the body of creatures of the following types: #LIGHT_BLUE#%s#LAST#
		When you try to possess a creature of a different type you may learn this type permanently, you can do that %d more times.]], [[你对目标投掷一个持续 %d 回合的灵能网。每回合造成 %0.2f 精神伤害。
		如果目标在持续时间内死亡，你会获得它的身体并放入你的灵能仓库中。
		在任何时候，你可以使用附身技能暂时脱离你的身体进入新的身体，继承其优势和弱点。
		灵能仓库有位置时才能使用该技能。

		你可以偷取以下阶级生物的身体 %s%s#LAST# 或者更低。
		等级 3 时最多可偷取 %s%s#LAST#。
		等级 5 时最多可偷取 %s%s#LAST#。
		等级 7 时最多可偷取 %s%s#LAST#。

		你可能只会偷走以下类型的生物的尸体 : #LIGHT_BLUE#%s#LAST#
		当你尝试附身不同类型的生物时，你可以永久学习此类型，你还可以执行 %d 次。]], "tformat")
t("Self Persistence", "自我坚持", "talent name")
t("When you assume the form of an other body you can still keep %d%% of the values (defences, crits, powers, save, ...) of your own body.", "当你附身时，你还可以保留自己身体的属性 %d%%（闪避，暴击，强度，豁免……）。", "tformat")
t("Improved Form", "身体改进", "talent name")
t([[When you assume the form of another body you gain %d%% of the values (defences, crits, powers, save, ...) of the body.
		In addition talents gained from bodies are limited to level %0.1f.]], [[当你附身时，你获得身体 %d%% 的数值（闪避，暴击，强度，豁免……）。
		此外，从身体获得的技能等级最高为 %0.1f。]], "tformat")
t("Full Control", "完全控制", "talent name")
t([[When you assume the form of an other body you gain more control over the body:
		- at level 1 you gain one more talent slot
		- at level 2 you gain one more talent slot
		- at level 3 you gain resistances and flat resistances
		- at level 4 you gain one more talent slot
		- at level 5 you gain all speeds (only if they are superior to yours)
		- at level 6+ you gain one more talent slot
		]], [[附身时，可更好的控制身体 :
		- 在等级 1 时，可额外获得一个技能位
		- 在等级 2 时，可额外获得一个技能位
		- 在等级 3 时，可获得抗性和固定减伤
		- 在等级 4 时，可额外获得一个技能位
		- 在等级 5 时，可获得所有速度（只有当他们优于你时）
		- 在等级 6 以上时，可额外获得一个技能位
		]], "tformat")

------------------------------------------------

section "tome-possessors/overload/mod/dialogs/AssumeFormSelectTalents.lua"

t("Assume Form: Select Talents (max talent level %0.1f)", "附身: 选择技能 (最大技能等级 %0.1f)", "tformat")
t("Possess Body", "附身", "_t")
t("Cancel", "取消", "_t")
t("#SLATE##{italic}#Your level of #LIGHT_BLUE#Full Control talent#LAST# is not high enough to use all the talents of this body. Select which to keep, your choice will be permanent for this body and its clones.", "#SLATE##{italic}#你的 #LIGHT_BLUE#完全控制#LAST# 技能 等级 不足，无法使用该身体的所有技能，选择需要保留的技能。你的选择对该身体及其克隆永久生效。", "_t")
