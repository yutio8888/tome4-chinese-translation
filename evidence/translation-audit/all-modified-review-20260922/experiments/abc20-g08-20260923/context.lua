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

section "tome-ashes-urhrok/data/zones/searing-halls/npcs.lua"

t("demon", "恶魔", "entity type")
t("minor", "小恶魔", "entity subtype")
t("demonic clerk", "恶魔职员", "entity name")
t("A small demon, he looks alarmed at your seeming freedom.", "一个小恶魔，他对你的自由感到非常惊惶。", "_t")
t("mutilator", "恶魔切割者", "entity name")
t("A demon with 3 arms, ready to mutilate you. For experiment. Not for fun. Nope.", "一个长着三只手的恶魔，准备切割你。不是娱乐，而是实验。", "_t")
t("investigator", "恶魔调查者", "entity name")
t("This demon is dedicated to #{italic}#extracting#{normal}# information from #{italic}#willing#{normal}# subjects.", "这个恶魔专心于从#{italic}#志愿者#{normal}#手里#{italic}#获取#{normal}#资料。", "_t")
t("Planar Controller", "空间控制者", "entity name")
t("major", "大恶魔", "entity subtype")
t("A huge demon towers above you, it is obviously in control of all the portals in the nearby Fearscape area.", "一个巨大的恶魔朝你走来，显然他控制着附近所有的传送门。", "_t")
t("and teleported to Mal'Rok for more experiments", "并被带去玛·洛克做为进一步的实验对象。", "_t")

------------------------------------------------

section "tome-ashes-urhrok/init.lua"

t("Ashes of Urh'Rok", "乌鲁洛克之烬", "init.lua long_name")
t([[Many in Maj'Eyal have heard of "demons", sadistic creatures who appear seemingly from nowhere, leaving a trail of suffering and destruction whereever they go.  Their Fearscape floats far above the skies, watching and waiting, but not idly; their agents scout the land, their legions build up their forces, and their scholars develop new spells and strategies.  As the barrier between our worlds begins to crack under their scrutiny, helpless Eyalites have begun to disappear, whisked up to serve as their slaves and playthings.  They imbue these victims with magical powers to better survive the ensuing stresses - can you use your new-found abilities to escape the legions of Mal'Rok?

Features:
* Start with a new class, the Doombringer!  These avatars of demonic destruction charge into battle with massive two-handed weapons, cutting swaths of firey devastation through hordes of opponents.  Armed with flame magic and demonic strength, they delight in fighting against overwhelming odds, softening up the crowd with waves of fire, then feeding on the flames and suffering of their surroundings to stay alive while quickly reducing any group to a pile of ash and gore.
* Unlock a new class, the Demonologist, with an all-new item enhancement mechanic!  Bearing a shield and the magic of the Spellblaze itself, these melee-fighting casters can grow demonic seeds from their fallen enemies.  Imbue these seeds onto your items to gain a wide array of new talents and passive benefits, and summon the demons within them to fight on your side!  Ever looked at a gigantic demon-cursed minotaur and wished it was on your side for once?  Well, now you CAN summon one to pound your foes into paste while you cast devastating spells from afar, or call forth a squad of Fire Imps to pelt your enemies to death while they exhaust themselves on your impenetrable defenses!  Demons have persistent health, making them a little more precious than disposable necromancer skeletons or summoner beasts, but can be revived from death nonetheless.
* Two new zones, with all-new art, foes, and bosses!  You've seen the plains of the Fearscape before, now see the lairs and headquarters of the demons themselves!
* Over 10,000 words of written lore to find!  The demons were once an enlightened, peaceful race, hailing from a distant planet known as Mal'Rok; learn what drove them to plot Eyal's eternal torture!  Discover monuments to each of the demonic species and noteworthy individuals, showing the place of honor each has among them!  Get a glimpse into the culture and daily lives of these sadistic invaders and their brainwashed thralls!
* Unlock a new race, Doomelves: Shalore who've taken to the demonic alterations especially well, corrupting their typical abilities into a darker form.  Blink away to safety, transform into a shadowy dúathedlen to hide in the shadows or prey on your foes with blasts of darkness, use your new resilience to soak up status effects and critical hits, and assault your enemies' minds to leave them unsteady in combat!
* Between the aforementioned classes and Doomelves, a whopping 75 new talents!
* Unlock two new cosmetic options!  You know you've always wanted demon-horns.  
* Two new events, appearing anywhere in Eyal!
* 20 new artifacts, with unique and interesting effects.  Collect the Obsidian Treasures to amass more and more power!  Slip your hands into the Will of Ul'Gruth and watch your sweeping blows smash down walls!  Wear a giant hideous hell-mouth as a fashionable belt!
* 7 new achievements!  Conquer the worst Urh'Rok's forces can throw at you, and hang their metaphorical skulls from your profile page!
]], [[在马基埃亚尔，很多人都曾听闻“恶魔”的大名，作为仿佛凭空出现的暴虐生物，他们无论走到哪里都会留下痛苦和毁灭。他们的恐惧空间高浮于天幕之上，并非闲置，而是一直在观察等待；他们的探员搜寻这片土地，他们的军团不断积蓄力量，他们的学者开发出全新的策略和法术。隔绝两端世界的屏障，在他们的破坏下开始破碎；无助的埃亚尔居民悄然消失，被掠走成为他们的奴隶和玩物。恶魔用魔法力量改造了受害者，使其能够在恶魔的拷问中存活 —— 你，能使用自己刚刚觉醒的新力量，逃脱玛·洛克的恶魔军团吗？

游戏特性：
* 使用全新职业开局，毁灭使者！他们是恶魔毁灭力量的化身，手拿双手武器加入战斗，将敌人化为一片火海。他们的手中掌握着火焰的魔法和恶魔的力量，在与势不可挡的敌人战斗中寻求欢愉。他们释放火海削弱敌群，随后吸收周围的火焰和痛苦，将任何敌人迅速化为灰烬。
* 解锁全新职业，恶魔使者，拥有全新的物品强化机制！这些近战施法者手拿盾牌，掌握魔法大爆炸本身的力量，可以从倒下的敌人身上培育出恶魔种子。将这些恶魔种子附魔到你的物品里，可以获得各种全新的技能和被动的能力，并召唤种子里的恶魔来加入战斗！你是否曾经看着巨大的恶魔牛头人，希望它能为你作战？现在，你确实可以召唤出来，你在远处释放法术的同时，他可以将敌人捣成浆糊。你也可以召唤火焰恶魔将敌人烧成灰烬，同时看着敌人在你铁壁般的防御面前无可奈何！恶魔具有更持久的生命值，比死灵法师易碎的骷髅或者自然召唤师的召唤兽更加珍贵，但仍然可以从死亡中复活。
* 两个新地区，具有全新的艺术，敌人和Boss！你以前曾经看过恶魔空间的平原，现在则可以看到恶魔自己的巢穴和总部！
* 超过一万字的全新手札！恶魔曾经是开明的和平种族，来自遥远的行星玛·洛克。了解是什么驱使他们策划给予埃亚尔永恒的折磨！探索恶魔物种和著名人物的纪念碑，展示每个人在其中的荣誉地位！瞥见这些嗜虐侵略者及其洗脑奴隶的文化和日常生活！
* 解锁一个新种族，魔化精灵：那些被恶魔的力量所改变的永恒精灵，他们的种族能力被腐化成了黑暗的形态。闪烁至安全处；变身为多瑟顿形态，在阴影中隐藏或给予敌人黑暗打击；坚韧缓和了负面状态和暴击伤害；在战斗中攻击敌人的精神，使他们难以为继！
* 上述职业和种族，提供了多达75个新技能！
* 解锁两个新的幻化选项！你知道你会想要恶魔之角的。
* 两个新随机事件，可能在埃亚尔大陆任何地方发生！
* 20个新神器，具有独特而有趣的效果。收集黑曜石宝藏以积累越来越多的力量！双手戴上乌尔格鲁斯的意志，挥舞拳头砸破墙壁！穿着巨大的可怕地狱嘴作为时尚腰带！
* 7个新成就！战胜乌鲁洛克最强大的敌人，将他们的头骨悬挂在个人页面上！
]], "init.lua description")

------------------------------------------------

section "tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua"

t("Welcome to Tales of Maj'Eyal - #CRIMSON#Ashes of Urh'Rok", "欢迎来到马基埃亚尔 - #CRIMSON#乌鲁洛克之烬", "_t")
t([[Welcome #LIGHT_GREEN#@name@#WHITE#.
You do not remember much of your life before you were on this burning continent, floating in the void between worlds.  You have been helping demons, happily participating in their experiments to shatter some sort of shield preventing them from taking their righteous revenge on Eyal.

You are being taken by your handler to the torture-pits to help them figure out how to cause the most pain to those on Eyal, when you hear a roaring above you; you look up and see a burning meteor, flying closer, and the demons' spells failing to divert its course!  It lands near you, knocking you off your feet with its shockwave and killing your handler instantly.

As you recover, and your platform of searing earth splits from the main continent, your old memories flood your mind and you come to your senses - the demons are out to destroy your home!

#{bold}#You must escape!#{normal}#.
]], [[你好，#LIGHT_GREEN#@name@#WHITE#。
你已经不太记得来到这片漂浮在虚空中的燃烧大陆之前的记忆了。你曾经帮助过恶魔，欢欣着参与他们的实验，以打破某种阻止恶魔正义复仇的无形屏障。

你被你的“主人”带到折磨场以帮助研究如何对埃亚尔大陆的生灵造成更大的痛苦，突然一阵轰鸣从天上传来，你抬头，看见一颗燃烧着的陨石正在坠落。恶魔试图用法术改变其轨迹，但没有成功！它落在你身边，砸死了你的“主人”，同时你也被冲击波击飞。

当你醒来后，你发现你身处一处和主大陆分离的焦土，而你旧时的记忆渐渐涌来。你立时惊醒——恶魔们要毁灭你的故乡！

#{bold}#你必须逃离这里！#{normal}#。
]], "_t")

------------------------------------------------

section "tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua"

t("New Class: #LIGHT_GREEN#Corruptor (Demonologist)", "新职业：#LIGHT_GREEN#堕落系（恶魔使者）", "_t")
t([[Demons in their invasion of Eyal have abducted natives of the planet and mindwiped them to serve as double agents.
Trained in the use of the demon's own forces they have created many dark cults to spread fear and terror.
Some have managed to escape their programming and chose to follow their own desires instead.

You have defeated countless demons, seen how their essence work, witnessed how to bind demons to your own purpose and can now create new characters with the #LIGHT_GREEN#Demonologist class#WHITE#.

Corruptors are spellcasters, ranged attackers using magic.
Class features:#YELLOW#
- Infect your foes with demonic seeds.
- Bind demonic seeds to your equipment to enhance them.
- Summon and control demons to do your binding.
- Blend corrupted magic with a martial shield training to protect yourself and ruin your foes.#WHITE#

Corruptors use "vim" to power their special abilities.
Vim is the life force of all beings. It does not regenerate, and can only be stolen from your foes.
]], [[在入侵埃亚尔大陆的过程中，恶魔绑架了这颗星球的居民，将他们洗脑后训练为双面间谍。

他们接受使用恶魔之力的训练，并通过黑暗仪式来传播不安与恐慌。

也有一些人成功逃脱了恶魔的控制，选择追随自己的渴望与意志。

你打败了无数的恶魔，掌握了他们本质的运作，见证了如何束缚恶魔为你所用，现在在你创建人物时可以选择新的职业 #LIGHT_GREEN#恶魔使者#WHITE#。

堕落系是施法职业，能使用魔法攻击敌人。
职业特点：#YELLOW#
- 向敌人注射恶魔之种
- 将恶魔种子附着在装备上，以强化装备效果
- 召唤并控制恶魔
- 将堕落魔法与盾牌战技结合，保护自己并毁灭敌人。#WHITE#

堕落者使用活力值来施放他们的法术。
活力是所有生物的生命力量，它不会自己回复，而必须从你的目标身上偷取。
]], "_t")

------------------------------------------------

section "tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua"

t("New Race: #LIGHT_GREEN#Doomelf", "新种族：#LIGHT_GREEN#魔化精灵", "_t")
t([[Doomelves are not a real race, they are Shaloren that have been taken by demons and transformed into harbingers of doom.
Their skills in inflicting and resisting pain have been honed by their rigorous training on the Fearscape.

You have killed the only three explorers from Mal'Rok that could have told the demons the truth and thus have earned the right to make #LIGHT_GREEN#Doomelf#WHITE# characters.

Race features:#YELLOW#
- Instant cast phase door
- Can turn into a dúathedlen
- Can increase detrimental effects and reduce beneficial ones on their foes
#WHITE#
]], [[魔化精灵并不是一个真正的种族，他们曾是永恒精灵，而被恶魔抓去，变为末日的使者。
恶魔空间的烈火和严格训练磨砺了他们抵御痛苦、施展痛苦的强大能力。

你已经终结了从恶魔家乡玛·洛克来的仅有的那三位探险者。现在，恶魔们将无法了解到有关埃亚尔大陆的真相，#LIGHT_GREEN#魔化精灵#WHITE# 应运而生。

种族特点 :#YELLOW#
- 使用加速技能，瞬间穿梭空间
- 转化成多瑟顿形态
- 可以延长敌人的负面效果，缩短敌人的正面效果
#WHITE#
]], "_t")

------------------------------------------------

section "tome-ashes-urhrok/overload/mod/class/DemonologistsDLC.lua"

t("Shadow Power: ", "阴影强度： ", "_t")

------------------------------------------------

section "tome-cults/data/achievements/all.lua"

t("You were not supposed to see that!", "你不应该看这些！", "achievement name")
t("Read a Forbidden Tome.", "读一本禁忌之书。", "_t")
t("Bookception!", "书中之书！", "achievement name")
t("Found the Forbidden Tome reward inside the Forbidden Tome: \"Of Knowledge And Horrors\".", "在禁忌之书《知识与恐怖》中，找到禁忌之书的奖励。", "_t")
t("Recursive Home of Recursion", "递归之家", "achievement name")
t("Left the Forbidden Tome: \"Home, Horrific Home\" on the floor of The Home Which Is Not.", "将禁忌之书《家，可怕的家》留在了“非家之家”的地板上。", "_t")
t("They Came From Outer Space!", "他们来自外太空！", "achievement name")
t("Discovered the true origin of dwarves and drems.", "发现矮人和德瑞姆的来历。", "_t")
t("The True Coward", "真正的懦夫", "achievement name")
t("Win without having saved Kroshkkur, Derth, the lost merchant, Melinda and lady Aeryn.", "在不拯救克诺什库尔、德斯镇、商人、米琳达和艾琳的情况下获得胜利。", "_t")
t("Sequence Master", "序列大师", "achievement name")
t("Use 5 different glyph sequences.", "使用5种不同的符文序列。", "_t")
t("Is that how it feels to be an escort quest?!", "这就是被护送的感受么？！", "achievement name")
t("Got saved from death in the Godfeaster by Malyu and managed to escape.", "被马虑护送离开巨大蠕虫噬神者。", "_t")
t("Not Really Yourself", "并非自我", "achievement name")
t("Let a parasitic horror take over your body and watch it grow in power.", "让寄生恐魔占据身体，日渐强大。", "_t")
t("Myths of an age past", "神代奥秘", "achievement name")
t("Learned all there is to learn about the Gods and the Godslayers.", "了解目前关于神和噬神者的所有信息。", "_t")
t("Dethroned", "废黜", "achievement name")
t("Vanquished the Glass Golem without letting it use the glass throne to heal.", "在不让玻璃傀儡借助玻璃王座治疗的情况下击败它。", "_t")
t("A View From The Gallery", "画廊一瞥", "achievement name")
t("Briefly lived as a lowly halfling during the time of the Sher'tuls.", "短暂地作为一名半身人活在夏·图尔的时代。", "_t")
t("Entropy's End", "熵之终结", "achievement name")
t("Destroyed the Hypostasis of Entropy.", "消灭熵的本质。", "_t")

------------------------------------------------

section "tome-cults/data/birth/demented.lua"

t("Demented", "疯狂系", "birth descriptor name")
t("The thirst for knowledge is seen by most arcane users as as good thing.", "对知识的渴望被大多数奥术使用者视为一件好事。", "_t")
t("But some take it too far, some delve into lost knowledge. They may gain huge power from it, but at what cost?", "但某些人走得太远，某些人陷入失落的知识中。他们或许得到了巨大的力量，但代价是什么呢？", "_t")
t("Writhing One", "蠕动者", "birth descriptor name")
t("Writhing Ones know that what we call #{italic}#horrors#{normal}# hold the key to some ancient knowledge and power from the Age of Haze and they are ready to do anything to access it.", "蠕动者知道，我们所谓的#{italic}#恐魔#{normal}#掌握着混沌纪远古知识与力量的关键，他们愿意为获取这些而不择手段。", "_t")
t("In their lust for power they somehow lost a part of themselves, turning more and more into the horrors they study.", "在极度渴求力量的同时，他们似乎失去了部分自我，和他们所研究的恐魔越来越相似。", "_t")
t("Most of them forgo an entire arm to turn it into a deadly tentacle.", "他们中大部分人选择将一整只手臂化作致命触手。", "_t")
t("Some are even known to never leave their sanctuary without their own worm that walks friend.", "某些人甚至拒绝在没有蠕虫合体的陪同下离开避难所。", "_t")
t("Their most important stats are: Strength and Magic", "他们最重要的属性是：力量和魔法。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +3 Strength, +0 Dexterity, +3 Constitution", "#LIGHT_BLUE# * +3 力量，+0 敏捷，+3 体质", "_t")
t("#LIGHT_BLUE# * +3 Magic, +0 Willpower, +0 Cunning", "#LIGHT_BLUE# * +3 魔法，+0 意志，+0 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# +3", "#GOLD#每等级生命加值：#LIGHT_BLUE# +3", "_t")
t("Cultist of Entropy", "熵教徒", "birth descriptor name")
t("Everything ends eventually. Harness this inevitability.", "万物终将消亡。这一点可以被利用。", "_t")
t("Cultists of Entropy are doomed beings which have unlocked the secrets of using entropy as a weapon. Their spells cause their bodies to wither away from entropic backlash, but they have learned how to resist this backlash and even pass it onto their foes.", "熵教徒是被诅咒的存在，他们能使用熵作为武器。他们的法术产生熵能反冲伤害自身，但他们学会如何抵抗反冲甚至将其转移至敌人身上。", "_t")
t("Their most important stats are: Magic and Cunning", "他们最重要的属性是：魔法和灵巧。", "_t")
t("#LIGHT_BLUE# * +0 Strength, +0 Dexterity, +0 Constitution", "#LIGHT_BLUE# * +0 力量，+0 敏捷，+0 体质", "_t")
t("#LIGHT_BLUE# * +6 Magic, +0 Willpower, +3 Cunning", "#LIGHT_BLUE# * +6 魔法，+0 意志，+3 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# -4", "#GOLD#每等级生命加值：#LIGHT_BLUE# -4", "_t")

------------------------------------------------

section "tome-cults/data/birth/drem.lua"

t("Skin", "皮肤", "birth facial category")
t("Hairs", "发型", "birth facial category")
t("Facial features", "脸部特征", "birth facial category")
t("Horns", "角", "birth facial category")
t("Special", "特殊", "birth facial category")
t("Drem", "德瑞姆", "birth descriptor name")
t("Faceless, but not mindless.", "没有面孔，但并非无脑。", "_t")
t("Drem are mindless mutants who live deep in the earth. It is only recently that thinking Drem have appeared among them. They still remain deep below Eyal's surface, believing that they would not be welcomed among the surface races.", "德瑞姆是生存于地底深处的异变种，直到最近才发现具有思维能力的个体。他们仍生存于地底，认为他们不会被地上种族欢迎。", "_t")
t("They possess the #GOLD#Frenzy#WHITE# talent which allows them to ignore cooldowns once in a while.", "他们拥有 #GOLD#狂热#WHITE# 技能，让他们偶尔能无视冷却时间。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +3 Strength, +1 Dexterity, +1 Constitution", "#LIGHT_BLUE# * +3 力量，+1 敏捷，+1 体质", "_t")
t("#LIGHT_BLUE# * +2 Magic, -1 Willpower, +0 Cunning", "#LIGHT_BLUE# * +2 魔法，-1 意志，+0 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# 12", "#GOLD#每等级生命加值：#LIGHT_BLUE# 12", "_t")
t("#GOLD#Experience penalty:#LIGHT_BLUE# 12%", "#GOLD#经验惩罚：#LIGHT_BLUE# 12%", "_t")
t("Skin Color 1", "皮肤颜色1", "_t")
t("Skin Color 2", "皮肤颜色2", "_t")
t("Skin Color 3", "皮肤颜色3", "_t")
t("Skin Color 4", "皮肤颜色4", "_t")
t("Skin Color 5", "皮肤颜色5", "_t")
t("Skin Color 6", "皮肤颜色6", "_t")
t("Skin Color 7", "皮肤颜色7", "_t")
t("Skin Color 8", "皮肤颜色8", "_t")
t("Skin Color 9", "皮肤颜色9", "_t")
t("Demonic Red Skin", "恶魔红皮肤", "_t")
t("Dark Hair 1", "深色头发1", "_t")
t("Redhead Hair 1", "红发1", "_t")
t("Beard 1", "络腮胡1", "_t")
t("Beard 2", "络腮胡2", "_t")
t("Redhead Beard 1", "红色络腮胡1", "_t")
t("Redhead Beard 2", "红色络腮胡2", "_t")
t("Demonic Beard", "恶魔络腮胡", "_t")
t("Demonic Redhead Beard", "恶魔红色络腮胡", "_t")
t("Demonic Horns 1", "恶魔角1", "_t")
t("Demonic Horns 2", "恶魔角2", "_t")
t("Demonic Horns 3", "恶魔角3", "_t")
t("Demonic Horns 4", "恶魔角4", "_t")
t("Demonic Horns 5", "恶魔角5", "_t")
t("Demonic Horns 6", "恶魔角6", "_t")
t("Demonic Horns 7", "恶魔角7", "_t")
t("Demonic Horns 8", "恶魔角8", "_t")
t("Bikini / Mankini", "比基尼/男性比基尼", "_t")

------------------------------------------------

section "tome-cults/data/birth/krog.lua"

t("Skin", "皮肤", "birth facial category")
t("Hairs", "发型", "birth facial category")
t("Facial features", "脸部特征", "birth facial category")
t("Tatoos", "纹身", "birth facial category")
t("Special", "特殊", "birth facial category")
t("Krog", "克罗格", "birth descriptor name")
t("Once an abomination, now a weapon.", "曾为憎恶，现为兵器。", "_t")
t("Krogs were formerly Ogres, that have been radically changed. Stripped of the runes from their bodies, the Ziguranth have managed to prevent the Krog from dying by injecting them with a concoction of natural infusions and drake blood. The Krog are entirely devoted to the anti-magic cause and seemingly know of nothing else in their lives.", "克罗格由食人魔彻底转变而来。伊格兰斯去除他们身上的符文，并为他们注射纹身与龙血的混合物以防止他们死亡。克罗格完全献身于反魔事业，生活中似乎对其他事物一无所知。", "_t")
t("They possess the #GOLD#Wrath of the Wilds#WHITE# talent which allows them to stun/daze their foes.", "他们拥有 #GOLD#自然之怒#WHITE# 技能，让他们能震慑/眩晕敌人。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +3 Strength, -1 Dexterity, +2 Constitution", "#LIGHT_BLUE# * +3 力量，-1 敏捷，+2 体质", "_t")
t("#LIGHT_BLUE# * -2 Magic, +2 Willpower, +0 Cunning", "#LIGHT_BLUE# * -2 魔法，+2 意志，+0 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# 13", "#GOLD#每等级生命加值：#LIGHT_BLUE# 13", "_t")
t("#GOLD#Experience penalty:#LIGHT_BLUE# 15%", "#GOLD#经验惩罚：#LIGHT_BLUE# 15%", "_t")
t("Skin Color 1", "皮肤颜色1", "_t")
t("Skin Color 2", "皮肤颜色2", "_t")
t("Skin Color 3", "皮肤颜色3", "_t")
t("Skin Color 4", "皮肤颜色4", "_t")
t("Skin Color 5", "皮肤颜色5", "_t")
t("Dark Hair 1", "深色头发1", "_t")
t("Dark Hair 2", "深色头发2", "_t")
t("Dark Hair 3", "深色头发3", "_t")
t("Dark Hair 4", "深色头发4", "_t")
t("Dark Hair 5", "深色头发5", "_t")
t("Dark Hair 6", "深色头发6", "_t")
t("Dark Hair 7", "深色头发7", "_t")
t("Dark Hair 8", "深色头发8", "_t")
t("Blond Hair 1", "金发1", "_t")
t("Blond Hair 2", "金发2", "_t")
t("Blond Hair 3", "金发3", "_t")
t("Blond Hair 4", "金发4", "_t")
t("Blond Hair 5", "金发5", "_t")
t("Blond Hair 6", "金发6", "_t")
t("Blond Hair 7", "金发7", "_t")
t("Blond Hair 8", "金发8", "_t")
t("Redhead Hair 1", "红发1", "_t")
t("Redhead Hair 2", "红发2", "_t")
t("Redhead Hair 3", "红发3", "_t")
t("Redhead Hair 4", "红发4", "_t")
t("Redhead Hair 5", "红发5", "_t")
t("Redhead Hair 6", "红发6", "_t")
t("Redhead Hair 7", "红发7", "_t")
t("Redhead Hair 8", "红发8", "_t")
t("Facial Warpaint", "脸部战争印记", "_t")
t("Dark Beard 1", "深色络腮胡1", "_t")
t("Dark Beard 2", "深色络腮胡2", "_t")
t("Dark Beard 3", "深色络腮胡3", "_t")
t("Dark Beard 4", "深色络腮胡4", "_t")
t("Dark Beard 5", "深色络腮胡5", "_t")
t("Blond Beard 1", "金色络腮胡 1", "_t")
t("Blond Beard 2", "金色络腮胡 2", "_t")
t("Blond Beard 3", "金色络腮胡 3", "_t")
t("Blond Beard 4", "金色络腮胡 4", "_t")
t("Blond Beard 5", "金色络腮胡 5", "_t")
t("Readhead Beard 1", "红色络腮胡1", "_t")
t("Readhead Beard 2", "红色络腮胡2", "_t")
t("Readhead Beard 3", "红色络腮胡3", "_t")
t("Readhead Beard 4", "红色络腮胡4", "_t")
t("Readhead Beard 5", "红色络腮胡5", "_t")
t("Tatoo 1", "纹身1", "_t")
t("Tatoo 2", "纹身2", "_t")
t("Bikini / Mankini", "比基尼/男性比基尼", "_t")

------------------------------------------------

section "tome-cults/data/chats/godfeaster-malyu-escaped.lua"

t([[#DARK_SEA_GREEN##{italic}#Fresh air!#{normal}##LAST#
Nice job! You handled yourself a lot better than I thought you would. Now, usually I get a reward... What? Why are you looking at me like that? I'm obviously the one who saved you here. It's customary for adventurers to get rewarded when they do a good deed.]], [[#DARK_SEA_GREEN##{italic}#新鲜的空气！#{normal}##LAST#
干得好！你做的比我想象中的好多了。现在，一般我会得到一个奖励…唔？你为什么这么看着我？很显然，我救了你。冒险者做好事的时候通常会得到奖励。]], "_t")
t("[Offer to teach her '%s'.]", "[同意教她 '%s'。]", "tformat")
t("[Offer her stat increases.]", "[你决定增加她的属性。]", "_t")
t("[Offer her nothing.]", "[你什么也不给她。]", "_t")
t("Oh this will sure come in handy! Thanks!", "哦，这个技能很有用！谢谢！", "_t")
t("Take care!", "那就这样吧，再见！", "_t")
t("I always did want to learn how to do these kind of things!", "太好了！我一直想要学这种东西！", "_t")
t("Oh, I suddenly feel like I have potential to grow.", "哦，我觉得我的潜能增长了。", "_t")
t("...Fine, be that way. Good luck out there, though.", "…好吧，就这样吧。祝你一路顺风。", "_t")
t("You too!", "你也是！", "_t")

------------------------------------------------

section "tome-cults/data/chats/godfeaster-malyu.lua"

t("#DARK_SEA_GREEN##{italic}#As you move you suddenly find yourself entrapped in a hidden digestive sack that seems to void all your abilities!#{normal}##LAST#", "#DARK_SEA_GREEN##{italic}#在你向前移动的时候，你突然发现自己掉进了一个隐藏的消化袋里，它似乎要耗尽你所有的能力！#{normal}##LAST#", "_t")
t("[try to kick your way out]", "[试着拳打脚踢]", "_t")
t("[try to cut your way out]", "[试着拿剑乱砍]", "_t")
t("[try to shout your way out]", "[试着喊救命]", "_t")
t([[#DARK_SEA_GREEN##{italic}#As were starting to lose hope you hear some kind of cutting.#{normal}##LAST#
There's someone else in here?]], [[#DARK_SEA_GREEN##{italic}#在你快要放弃希望的时候，你听到了切开东西的声音。#{normal}##LAST#
有人在里面吗？]], "_t")
t("Who..what.. YES!", "是谁…什么…对！我在里面！", "_t")
t([[#DARK_SEA_GREEN##{italic}#As the sack gets cut and you regain your mobility you see your savior is some kind of adventurer, she was probably eaten by the Godfeaster too.#{normal}##LAST#
This thing ate you too? Hey, at least you've got company. Name's Malyu, I've been stuck in here for a few days now and had to tough it out alone. I was about to go for this thing's brain when you showed up. What say we team up and get out of here together?
]], [[#DARK_SEA_GREEN##{italic}#当袋子被切破开来，你恢复了你的能力。你看到了救你的人是一个冒险家，她好像也被噬神者吞下了。#{normal}##LAST#
这个东西也吃了你？嘿，至少你有一个伴了。我的名字是马虑，我在这里被困了几天了，不得不独自面对这一切。我本来准备破坏这个东西的大脑，结果遇到了你。我们一起离开这个地方怎么样？
]], "_t")
t("I am glad for the help, you saved me. Let's kill this thing and get out!", "感谢你的帮助，你救了我。我们一起杀了这个怪物，逃出去吧！", "_t")
t("Malyu", "马虑", "_t")

------------------------------------------------

section "tome-cults/data/general/events/digestive-sack.lua"

t("\
#DARK_SEA_GREEN#It was corrupted by the digestive sack.", "\
#DARK_SEA_GREEN#这个物品被消化袋腐化了。", "_t")
t("\
#DARK_SEA_GREEN#It was hardened by the digestive sack.", "\
#DARK_SEA_GREEN#这个物品被消化袋强化了。", "_t")
t("\
#DARK_SEA_GREEN#It was changed by the digestive sack.", "\
#DARK_SEA_GREEN#这个物品被消化袋改变了。", "_t")
t("corrupted #base#", "腐化的 #base#", "_t")
t("giant digestive sack", "巨大的消化袋", "_t")
t("Giant Digestive Sack", "巨大的消化袋", "_t")
t("Open the sack?", "打开袋子？", "_t")
t("#DARK_SEA_GREEN#An object rolls from the sack!", "#DARK_SEA_GREEN#一个物品从消化袋里掉了出来！", "logSeen")
t("#DARK_SEA_GREEN#A not yet digested foe burst out from the sack!", "#DARK_SEA_GREEN#一个没有被完全消化的敌人从消化袋里掉了出来！", "logSeen")
t("giant digestive sack (opened)", "打开的巨大消化袋", "_t")
t("#DARK_SEA_GREEN#Sickening fumes emanates from the sack as it opens!", "#DARK_SEA_GREEN#袋子打开时散发出令人作呕的烟雾！", "logSeen")
t("Open", "打开", "_t")
t("Leave", "离开", "_t")

------------------------------------------------

section "tome-cults/data/general/events/space-dwarf-ship.lua"

t("floor", "地板", "_t")
t("wall", "墙壁", "_t")
t("strange metallic capsule", "诡异的金属舱", "_t")
t("Strange metallic capsule", "诡异的金属舱", "_t")
t("You have already scavenged what you could understand and use.", "你已经找遍了你能理解和使用的东西。", "_t")
t([[The thing in front of you appears to be a strange dome made from green glass. Judging by the crater around it, this dome must have crashed into the earth with tremendous force. Stranger still is the figure seated inside it. It appears to be wearing a suit made of an unknown material and a glass dome over its head. Looking inside the dome, you can plainly see that the figure is a dwarf! There is no mistaking that oversized nose. Judging by the smell, he has been dead for quite some time.

You are fairly sure that the dwarves aren't capable of making something like this and they definitely don't dress like that. So, where did this odd dwarf come from? Taking a closer look, you find a strange device attached to the dwarf's arm. You remove it with no small amount of effort. It is completely unlike anything you have seen before and you're not really sure what to make of it. Perhaps if you hold onto it, you might be able to discern its functionality later.]], [[出现在你眼前的是一个被绿色玻璃遮罩的太空舱，根据附近的弹坑判断，这个太空舱曾以极快的速度撞击地面，里面仍坐着一个奇怪的生物，穿着不明材质的衣服，戴着绿色玻璃做成的头罩。透过绿色的玻璃看去，能看到矮人标志性的大鼻子，你清楚地发现这是一个矮人！从气味判断，他已经死了很久了。

你很肯定矮人不会做出这样的东西，而且他们绝对不会穿那样的衣服。那么，这个奇怪的矮人是从哪里来的？仔细观察，你会发现一个奇怪的装置附在矮人的手臂上。你费了不小的力气才把它取下来。它和你见过的任何东西都不一样，你也不知道该怎么做。如果你留下它，也许你以后可以辨别出它的功能。]], "_t")
t("previous level", "前往上一层", "_t")
t("ladder back to %s", "返回%s的楼梯", "tformat")
t("Eerie Cave", "诡异洞穴", "_t")
t("eerie cave", "诡异的洞穴", "_t")

------------------------------------------------

section "tome-cults/data/general/grids/fonts.lua"

t("floor", "地板", "entity type")
t("creep", "菌毯", "entity subtype")
t("font of knowledge", "知识之泉", "entity name")
t("Font of Knowledge", "知识之泉", "_t")
t("Do you want to touch it?", "你想要触碰它吗？", "_t")
t("No", "否", "_t")
t("Yes", "是", "_t")
t("#CRIMSON#Your timetravel has no effect on pre-determined outcomes such as this.", "#CRIMSON#你的时间穿越对这种已经预设好的结局没有任何作用。", "_t")
t("#PURPLE#The %s glows as you touch it. Your knowledge grows (+1 prodigy point).", "#PURPLE#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 觉醒点）。", "log")
t("#VIOLET#The %s glows as you touch it. Your knowledge grows (+1 category point).", "#VIOLET#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 技能树解锁点）。", "log")
t("#YELLOW#The %s glows as you touch it. Your knowledge grows (+1 class talent point).", "#YELLOW#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 职业技能点）。", "log")
t("#ORANGE#The %s glows as you touch it. Your knowledge grows (+1 generic talent point).", "#ORANGE#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 通用技能点）。", "log")
t("#AQUAMARINE#The %s glows as you touch it. Your knowledge grows (+3 stat points).", "#AQUAMARINE#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+3 属性点）。", "log")
t("cave", "山洞", "entity subtype")
t("font of sacrifice", "牺牲之泉", "entity name")

------------------------------------------------

section "tome-cults/data/general/grids/fortress-multiverse.lua"

t("entropic breach", "熵之裂口", "entity name")
t("Entropic Wormhole Control Orb", "熵虫洞控制球", "entity name")
t("#CRIMSON#The entropic forces are already at work. FIGHT!", "#CRIMSON#熵已经在起作用了。战斗！", "say")
t("#CRIMSON#The entropic control orb seems unresponsive...", "#CRIMSON#熵控制球看上去不对你起反应……", "say")
t("#PURPLE#Make sure you are connected and joined the main Tales of Maj'Eyal chat channel.", "#PURPLE#确认你连接到了网络，并加入了马基·埃亚尔聊天频道。", "log")

------------------------------------------------

section "tome-cults/data/general/grids/godfeaster.lua"

t("floor", "地板", "entity type")
t("floor", "地板", "entity subtype")
t("exit to the worldmap", "通往世界地图的出口", "entity name")
t("previous level", "前往上一层", "entity name")
t("next level", "前往下一层", "entity name")
t("godfeaster", "噬神者", "entity subtype")
t("floor", "地板", "entity name")
t("wall", "墙壁", "entity type")
t("godfeaster wall", "噬神者墙", "entity name")
t("godfeaster door", "噬神者门", "entity name")
t("open godfeaster door", "打开的噬神者门", "entity name")
t("This door seems to have been sealed off. You think you can open it.", "这扇门似乎被封住了，你觉得你可以打开它。", "_t")

------------------------------------------------

section "tome-cults/data/general/grids/maggot.lua"

t("floor", "地板", "entity type")
t("floor", "地板", "entity subtype")
t("exit to the worldmap", "通往世界地图的出口", "entity name")
t("previous level", "前往上一层", "entity name")
t("next level", "前往下一层", "entity name")
t("maggot", "蛆虫", "entity subtype")
t("floor", "地板", "entity name")
t("wall", "墙壁", "entity type")
t("maggot wall", "蛆虫墙", "entity name")
t("maggot door", "蛆虫门", "entity name")
t("open maggot door", "打开的蛆虫门", "entity name")
t("This door seems to have been sealed off. You think you can open it.", "这扇门似乎被封住了，你觉得你可以打开它。", "_t")

------------------------------------------------

section "tome-cults/data/general/grids/slimy_godfeaster.lua"

t("floor", "地板", "entity type")
t("floor", "地板", "entity subtype")
t("exit to the worldmap", "通往世界地图的出口", "entity name")
t("previous level", "前往上一层", "entity name")
t("next level", "前往下一层", "entity name")
t("slimy_godfeaster", "史莱姆噬神者", "entity subtype")
t("floor", "地板", "entity name")
t("wall", "墙壁", "entity type")
t("slimy_godfeaster wall", "史莱姆噬神者墙", "entity name")
t("slimy_godfeaster door", "史莱姆噬神者门", "entity name")
t("open slimy_godfeaster door", "打开的史莱姆噬神者门", "entity name")
t("This door seems to have been sealed off. You think you can open it.", "这扇门似乎被封住了，你觉得你可以打开它。", "_t")

------------------------------------------------

section "tome-cults/data/general/npcs/blobs.lua"

t("vermin", "害虫", "entity type")
t("blob", "生物质团", "entity subtype")
t("Ewwww.", "额…", "_t")
t("plasmic disruptor", "浆胞破坏者", "entity name")
t("A green oozing defence cell of the Maggot.", "这团绿泥是巨大蛆虫的防御细胞。", "_t")
t("mastocytic feeder", "肥大胞吞噬者", "entity name")
t("A reddish attack cell that will crawl to you to distract you while the rest of the organism attacks.", "一团红色的攻击细胞，它会爬到你的身边，在这个生物体的其余部分发动攻击时分散你的注意力。", "_t")
t("protoplasmic controller", "原生质操控者", "entity name")
t("Acid. Fire. Pain.", "酸液。火焰。痛苦。", "_t")
t("dendritic hemospinner", "树突胞递呈者", "entity name")
t("This strange cell can somehow connect to Eyal itself.", "这个奇怪的细胞似乎可以通过某种方法连接到埃亚尔本身。", "_t")
t("acidic digestor", "酸胞消化者", "entity name")
t("You look like nutriments.", "你看起来像是营养成分。", "_t")
t("protosentient globula", "原知觉球体", "entity name")
t("A huge globula of protoplasma. You can feel a kind of protosentience emanating from it, and you can tell it is hungry.", "一大团原生质球体。你能感觉到某种原始感知从它身上散发出来，并且能看出它很饥饿。", "_t")

------------------------------------------------
