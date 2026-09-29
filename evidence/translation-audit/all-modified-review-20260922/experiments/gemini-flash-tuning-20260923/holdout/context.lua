section "tome-orcs/data/chats/kaltor-shop.lua"

t("Finally a practical giant! Show me your wares.", "终于来了一位有理性的巨人！给我看看你的货。", "_t")
t("Die giant scum! For Kruk! For Garkul! For the Pride!", "死吧，巨人渣渣！为了克鲁克！为了加库尔！为了部落", "_t")
t("No need for shopping now.", "现在不需要购物。", "_t")
t([[#LIGHT_GREEN#*A well-dressed giant stands in front of you, covered in expensive jewelry; judging from the poorly-fastened clasp on his necklace, you can assume he acquired it all fairly recently.  He grins as he leans down over the counter to get a good view of you.*#WHITE#
Ah, welcome, @playername@! #LIGHT_GREEN#*he yells in a voice loud enough to catch the attention of all in the shop, as he lifts his head to look around.*#WHITE# Yes, you heard me right, @playername@! The very same one who's been running rampant through the Vaporous Emporium is coming to ME for armaments! I don't think I could've asked for a stronger endorsement! #LIGHT_GREEN#*He looks back down to you, leaning over the counter to point out a glass display case loaded with exotic weaponry and armor.*#WHITE#
Well, I'm not one to turn down anyone with gold, and seeing as you've already made me rich, I'll even give you a discount, down to my pre-attack prices. #LIGHT_GREEN#*He leans in uncomfortably close, staring you in the eyes.* #WHITE#Or, if you came to do here what you did in the Emporium... #LIGHT_GREEN#*He directs his glare toward the multiple well-armed guards staring at you and standing still on the sides of the room.*#WHITE# I'm sure my #{italic}#emergency safety measures#{normal}# would just #{italic}#love#{normal}# an opportunity to try out their shiny new toys.]], [[#LIGHT_GREEN#*一名衣着讲究的巨人站在你面前，戴满昂贵的珠宝；从他松垮的项链扣上看，你猜测他是最近才拿到的。他微笑着从柜台往下看，注视着你。*#WHITE#
哦，欢迎，@playername@! #LIGHT_GREEN#*他的声音大的让店里所有人都听见，同时他抬起头张望四周。*#WHITE# 是的，听见了么，@playername@！就是那个在蒸汽商场猖獗无比的家伙，他到我这来买装备了！我认为不会有比这更好的宣传了！#LIGHT_GREEN#*他转过头看你，指出一个玻璃展台，那上面装满异种武器和护甲。*#WHITE#
好吧，我不会拒绝任何带着钱过来的人，同时你也已经让我富裕不少了。我甚至还能给你打个折，降到进攻前的价格。#LIGHT_GREEN#*他靠得过近，让你感觉不太舒服。他直视着你的眼睛。*#WHITE#或者，你也可以试试你在蒸汽商店里干的事情……
#LIGHT_GREEN#*他指向周围和房间里那些装备良好的警卫。*#WHITE#
我相信我的#{italic}#紧急安全保卫#{normal}#一定#{italic}#爱死了#{normal}#每一个尝试新玩具的机会。]], "_t")
t([[Welcome back, @playername@!  You see this, customers?  This fearsome, savage master of battle was so impressed by my products that he came back for more!
#LIGHT_GREEN#*He points to a new poster on the wall next to him, showing your face and the caption #{bold}#"KALTOR: THE CHOICE OF DESTROYERS!"#{normal}#*#WHITE#

So, what'll it be?]], [[欢迎回来，@playername@! 来看看这个，顾客们？这位可怕而野蛮的战斗大师也对我的产品印象深刻，现在他又回来买东西了！
#LIGHT_GREEN#*他指向墙上贴着的新海报，上面是你的脸和一行大字 #{bold}#"卡托尔：破坏者的选择！"#{normal}#*#WHITE#

那么，你要做什么呢？]], "_t")
t([[#LIGHT_GREEN#*Kaltor is busy packing some of his goods away in crates; he hands one to a worker, carrying it out the back door, before turning to you.*#WHITE#
	Make it quick, @playername@. Not to be rude, but there's a private airship out there with my name on it, and I'd rather have a bird's-eye view of what you're about to do than a front-row seat.]], [[#LIGHT_GREEN#*卡托尔忙着打包货物；他将箱子递给一个工人带到后门，然后转过头和你说话。*#WHITE#
	快点吧，@playername@。不是我粗鲁，但现在有一艘我的飞船在外面，我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。]], "_t")
t([[#LIGHT_GREEN#*He frowns in mock disappointment, as he presses a button on his stylish coat; it hisses, and you hear motors whirring*#WHITE#
Oh, what a pity.  Guards?  Ten thousand gold to whoever gets the killing blow.  Store credit, of course.]], [[#LIGHT_GREEN#*他假装失望地皱起眉头，按下外套上的按钮。它发出嘶嘶声，你听见引擎的轰鸣。*#WHITE#
真遗憾。警卫？谁杀了他，就有一万金的赏钱。当然，记在商店账上。]], "_t")
t("DEATH!", "去死吧！", "_t")

------------------------------------------------

section "tome-orcs/data/damage_types.lua"

t("pulse detonator", "脉冲爆弹", "damage type")
t("%s is knocked back!", "%s 被击退！", "logSeen")
t("%s resists the knockback!", "%s抵抗了击退！", "logSeen")
t("darkness pull", "黑暗抓取", "damage type")
t("%s is pulled!", "%s被拖动！", "logSeen")
t("%s resists the pull!", "%s抵抗了拖动！", "logSeen")
t("darkness pin", "黑暗定身", "damage type")
t("%s resists!", "%s抵抗了效果！", "logSeen")
t("drain negative", "吸收负能量", "damage type")
t("null_type", "无属性", "damage type")
t("light + dark", "光+暗", "damage type")
t("blighted needles", "枯萎之针", "damage type")
t("infective darkness", "传染黑暗", "damage type")
t("fiery vapour", "火焰蒸汽", "damage type")
t("repairing", "修复", "damage type")
t("mind drone", "精神无人机", "damage type")
t("20% chance of physical repulsion", "20% 几率物理排斥", "damage type")
t("temporal ripples", "时空波纹", "damage type")
t("curse of amakthel", "阿马克泰尔的诅咒", "damage type")
t("psionic searing", "灵能焦灼", "damage type")
t("resource shock", "资源冲击", "damage type")
t("smoke cloud", "烟雾云", "damage type")
t("lightning web", "闪电之网", "damage type")
t("incendiary grenade", "燃烧榴弹", "damage type")
t("chemical grenade", "化学榴弹", "damage type")
t("shock grenade", "震荡榴弹", "damage type")
t("phosphorous", "磷火", "damage type")
t("fire wall", "火墙", "damage type")
t("volatile fuel", "易燃燃料", "damage type")
t("chemical", "化学", "damage type")
t("debilitating acid", "弱化酸液", "damage type")
t("caustic steam", "腐蚀蒸汽", "damage type")
t("galvanic", "放电", "damage type")
t("occult", "玄机", "damage type")
t("terrene", "寒岩", "damage type")

------------------------------------------------

section "tome-orcs/data/general/events/merchant-stall.lua"

t("market stall", "市场摊位", "_t")
t("A market stall, it looks abandoned..", "一个市场摊位，看起来被遗弃了……", "_t")
t("- #GOLD#%0.2f gold#LAST# worth of money", "- #GOLD#%0.2f 金币#LAST#", "tformat")
t("Market Stall", "市场摊位", "_t")
t([[You loot the stall and gain:
]], [[你洗劫了这个市场摊位，获得了：
]], "_t")

------------------------------------------------

section "tome-orcs/data/general/npcs/hethugoroth.lua"

t("elemental", "元素生物", "entity type")
t("vapour", "蒸汽", "entity subtype")
t("hethugoroth", "赫斯格鲁斯", "entity name")
t("A swirling mass of hot vapour animated into a semblance of life.", "一个看似有生命的灼热蒸汽漩涡。", "_t")
t("greater hethugoroth", "大型赫斯格鲁斯", "entity name")
t("ultimate hethugoroth", "终极赫斯格鲁斯", "entity name")

------------------------------------------------

section "tome-orcs/data/general/objects/boss-artifacts.lua"

t("Yeti-fur Cloak", "雪人毛皮斗篷", "entity name")
t("matted fur cloak", "乱蓬蓬的毛皮斗篷", "_t")
t("This fur cloak is thick and matted, yet remains incredibly soft to the touch.", "这件毛皮斗篷厚实而毛绒蓬乱，摸起来却出奇地柔软。", "_t")
t("Korbek's Spyglass", "库贝克的小型望远镜", "entity name")
t("golden telescope", "金色望远镜", "_t")
t("This antique spyglass is weathered from use, but seems well maintained.", "这个年代久远的小型望远镜由于使用过多有些褪色，但是仍然保养得很好。", "_t")
t("Talosis' Counterpoint", "泰勒西斯的反驳", "entity name")
t("ornate gun", "华丽的手枪", "_t")
t("It's said that Talosis never lost an argument. Now you know why.", "据说泰勒西斯从没有输过一场争吵。现在你知道原因了。", "_t")
t("The Twisted Blade", "扭曲之刃", "entity name")
t("vile, twisted steamsaw", "邪恶、扭曲的蒸汽锯", "_t")
t("You see flecks of gold in this vile mass of twisted steel, implying a once great origin. Whatever glory it once had is long gone, replaced by something far more sinister...", "你在这块邪恶、扭曲的铁块上发现金色的斑点，暗示着它不同寻常的来历。然而曾经的辉煌，都已经成为了过去，如今已被更加邪恶的东西取代", "_t")
t("Fully heal yourself. (15 turn cooldown)", "完全治疗（15回合冷却）", "_t")
t("Sunstone", "太阳石", "entity name")
t("warm stone", "温暖的石头", "_t")
t("This strange stone shines with the heat of the Sun. Perhaps it could be used to generate more steam?", "这块奇怪的石头发出太阳的光和热。或许它可以用来产生更多的蒸汽？", "_t")
t("Overseer", "监视者", "entity name")
t("cracked mindstar", "破裂的灵晶", "_t")
t("Fragments of the Mindwall's power still inhabit this cracked, ancient gem.", "意念之墙的力量碎片仍然依附在这块破裂的古老宝石上。", "_t")
t("reduces mental save", "减少精神豁免", "_t")
t("either mentally dominate or psychically stun (depending on immunities) a nearby target within range %d for %d turns (success depends on Mindpower)", "对范围 %d 内的一个目标施加精神控制或精神震慑（取决于其免疫状态），持续 %d 回合（成功率取决于精神强度）", "tformat")
t("#Source# psychically dominates #target# through %s %s!", "#Source#使用%s%s精神控制#target#！", "logCombat")
t("Ureslak's Focus", "乌瑞斯拉克的焦点", "entity name")
t("multi-hued", "多彩", "entity subtype")
t("crystallized drake heart", "晶化龙心", "_t")
t("This cracked gemstone fell from the remains of the dead Ureslak. It appears to have been turned into a vibrant crystal in whatever process reanimated him.", "这块开裂的宝石来自死去的乌瑞斯拉克的遗骸。在使乌瑞斯拉克复生的某种过程中，它似乎被转化成了一块绚丽的水晶。", "_t")
t("Starcaller", "召星者", "entity name")
t("black staff", "黑色的法杖", "_t")
t("A light staff covered in stralite and gems. It seems to reflect the light of the stars even in daylight.", "一把被斯莱特和宝石覆盖的轻型法杖。即使在白天，似乎也在反射着星星的光芒。", "_t")
t("Liquid Metal Cloak", "液态金属披风", "entity name")
t("shiny metallic cloak", "闪亮的金属披风", "_t")
t("This strange sheet of metal flows with the wind just like a normal cloak. Whoever crafted it was a true master.", "这片奇特的金属如同普通的披风一样随风摆动。打造它的人无疑是一位大师。", "_t")

------------------------------------------------

section "tome-orcs/data/lore/dominion-port.lua"

t("dominion port", "巨魔帝国港口", "newLore category")
t("'disciplinary report'", "纪律报告", "_t")
t([[DISCIPLINARY REPORT:

-Blackhorn the Brash, theft of personal quantities of Atmos absinthe.  Twenty lashes.
-Swabbie Grobbo, theft of personal quantities of Shaloren wine.  Twelve lashes.
-First Mate Grapeshot, improper use of a cannon.  Twenty lashes, demotion.
-Taroggos, killing crew of targeted supply ship in defiance of client's wishes.  Three lashes.  [i]note: payment received regardless,  all goods retrieved and delivered accordingly[/i]
-Runty, theft of personal quantities of Dwarven ale.  Eleven lashes.
-Hamfist, theft of commercial quantities of Ogric brandy.  Fifty lashes, docked pay.
-Dogchucker the Summoner, disfiguring another crewmember.  Punishment waived.  [i]note: determined to be accident[/i]
-Tidal Torgor, accidental sinking of friendly vessel.  One thousand lashes, over five days.  [i]note: should be keelhauled but we need all the aquamancers we can get![/i]
-Lieutenant Grapeshot, improper use of a cannon.  Thirty lashes, demotion.
-Lady Laggo, skimming profits from loot sales.  Thirty lashes, demotion to punitive duties.
-Shifty, insubordination.  Ten lashes.
-Swabbie Grogbreath, insufficient swabbing.  Loss of liquor privileges.
-Cannoneer Grapeshot, improper use of a cannon.  Thirty lashes, demotion.
-Pencil-Pusher Pilgo, reassigning Grapeshot to cannoneer position.  Thirty-five lashes.  [i]note: laugh it up you insubordinate punk[/i]
-Smokey, excessive use of fire onboard flammable ship.  Will not be allowed healing for wounds sustained when hat caught fire.
-Swabbie Grogbreath, violation of loss of liquor privileges.  Punishment waived.  [i]note: the foul swill he found is punishment enough[/i]
-Sticks, attempted mutiny.  Keelhauled.
-Crabhide, support of attempted mutiny.  Keelhauled.
-Pegfist Pogga, failure to report attempted mutiny.  Keelhauled.
-Gunner Bilgebloat, fraternizing with attempted mutineers.  Keelhauled.
-First Mate Brakka, failure to keelhaul enough attempted mutineers.  Keelhauled.
-Captain Bloody-Keel, excessive keelhauling.  Keelhauled twice.
-Swabbie Grapeshot, improper use of a mop.  Fifty lashes, demotion.
]], [[纪律报告：

“盛气凌人的”黑角，偷窃个人用量的蒸汽牌苦艾酒。二十鞭刑。
水手哥罗博，偷窃个人用量的永恒精灵葡萄酒。十二鞭刑。
大副葡萄弹，不当使用加农炮。二十鞭刑以及降职。
塔洛格格斯，无视客户的意愿，杀害目标补给船上的船员。三鞭鞭刑。
[i]注：尽管如此仍然收到了付款，所有货物收发无误。[/i]
阿短，偷窃个人用量的矮人麦酒。十一鞭刑。
大拳，偷窃商业用量的兽人白兰地。五十鞭刑，减薪。
召唤师狗门卫，致另一船员毁容。免除惩罚。
[i]注：绝对是一场意外[/i]
潮之托尔格，过失令一友方船只沉没，一千鞭刑，五天之内完成。
[i]注：需要绑在船底拖行，但是我们需要一切能用的上的水术士！[/i]
上尉葡萄弹，不当使用加农炮。三十鞭刑以及降职。
拉果女士，贪污战利品销售利润。三十鞭刑，降职做惩罚性杂务。
鬼祟，不遵守命令。十鞭刑。
水手掺水酒之息，擦拭不够。免除饮酒福利。
炮手葡萄弹，不当使用加农炮。三十鞭刑以及降职。
办事员皮尔果，把葡萄弹重新放在开炮的职位上。三十五鞭刑。
[i]注：继续笑吧，你这个不遵守命令的小瘪三[/i]
烟熏，在可燃的船上过量用火。当帽子着火造成伤的时候不准接受治疗。
水手掺水酒之息，违反免除饮酒。免除惩罚。
[i]注：他找到的发酸的烈酒已经足够惩罚了[/i]
棒子，企图叛变。绑在船底拖行。
蟹皮，支持未遂的叛变。绑在船底拖行。
佩格拳波加，未报告未遂叛变。绑在船底拖行。
枪手舱底打嗝，与叛变企图者亲善。绑在船底拖行。
大副布拉卡，没有拖行够那些叛变企图者。绑在船底拖行。
船长血色龙骨，过量的船底拖行。绑在船底拖行两次。
水手葡萄弹，不当使用一个拖把。五十鞭刑以及降职。
]], "_t")
t("operations performed", "行动记录", "_t")
t([[OPERATIONS PERFORMED:

-With information provided by "Sunny Day," we were able to secure an Allied Kingdoms supply ship during the brief window in which it was unguarded, with no personal casualties.  We technically broke our agreement (Taroggos has been adequately disciplined), but because the ship was carrying more useful materials than expected, we were able to take a hefty supply of troll-sized (or close enough to it) arms and armor, alongside lumber, furniture, and smaller stralite equipment which can be easily melted down and repurposed into something useful, before delivering the promised amount of cargo to "Vapor Trail."  Combined with the payment received from "Sunny Day," we made a significant profit and reinforced our relationship with "Vapor Trail."  (Our relationship with "Sunny Day" is of no consequence; repeat business was unlikely.)

-The last cargo ship I had sent home, the one with countless small crates and the order to confiscate them all and hold onto them for further instruction, contains one crate full of You-Know-What received as payment for a product received via Iron Throne smugglers.  This crate is labelled "47-C."  Dispose of the others, as they are [i]extremely[/i] thoroughly trapped.  The exchange with "Sherry Toll" was mercifully uneventful, and the goods provided appear to be functional.  With all due respect, Boss, if this doesn't get me a promotion, what will?

-Our contacts with the black market of Maj'Eyal and our establishment of a safe trading hub for their activity has continued to be immensely profitable, in addition to providing us an exploitable means of getting objects of our choosing into Maj'Eyal.  "Vapor Trail" has been an eager participant, and we've made a killing off selling Atmos absinthe to the Allied Kingdoms smugglers, as well as selling Elvala wine and brandy to them.  I'll be sending a ship full of our profits (useful metals, alchemical ingredients, slaves) back home on a bi-monthly basis; search the crew to make sure they haven't been lining their pockets, and keelhaul any you catch.

-Crew disobedience and morale continues to be something of a problem, despite regular floggings, but we're still retaining enough of them and getting enough use out of them.  That said, feel free to keep sending sentenced criminals our way - they're surprisingly productive as long as we give them enough booze and cheerblossom.]], [[行动记录：

- 根据“大晴天”提供的信息，我们趁一艘联合王国补给船短暂无人看守时夺取了它，而且没有人员伤亡。我们理论上破坏了约定（塔洛格格斯已经被妥当处罚了），但是因为船承载了比预期更多的有用材料，在我们运送了承诺的货物量到“汽化液之径”之前，我们获取了可观的，巨魔尺寸（或者接近）的补给物资，包括武器防具，以及木材、家具以及较为小型的，能够重铸成有用东西的斯莱特装备。加上从“大晴天”收到的支付，我们获得了可观的利润并且加强了与“汽化液之径”的关系。（我们与“大晴天”的关系无足轻重；毕竟不太可能再与他们做生意了。）

- 上一艘我送回家的货船，也就是那个载着无数小箱子的，接到命令没收全部货物，并扣押下来等待进一步指令的那艘。这艘船上面包括了一个满盛着“你懂的”的箱子，作为从钢铁王座的走私者那里以货物形式支付的报酬。这个箱子被标作“47-C”。其余箱子都处理掉，因为它们布满了[i]极其[/i]周密的陷阱。和“雪利酒收费站”的交易很幸运地没出岔子，货物看上去也很有用。头儿，如果这些功绩都不能让我升职，还有什么会？

- 我们与马基亚埃尔的黑市的那些合约，以及在那里建立一个安全的交易枢纽的行动持续创收大量利润。并且，这还让我们增加了一个有利的途径，让我们想要的东西进入马基亚埃尔。“汽化液之径”一直是一个热诚的参与者，我们靠向联合王国的走私者卖蒸汽牌苦艾酒以及埃尔瓦拉产的葡萄酒和白兰地大赚了一笔。我将每两个月送一艘船回来，满载着我们的获利（有用的金属、炼金术原料、奴隶）；在船员中搜查他们是否揩油了，如果你抓住了就都绑在船底拖行。

- 船员的不服从以及他们的士气不足是一个持续存在的问题。尽管我们经常鞭笞他们，但我们仍留住了足够的人手，也从他们身上得到了不少用处。也就是说，请继续多送点服刑的犯人来我们这儿：只要我们给足够的酒类和鼓舞之花，他们就会努力工作了。]], "_t")
t("overall analysis", "总体分析", "_t")
t([[OVERALL ANALYSIS:

Boss, if there's one thing I can say, it's that you didn't make a mistake by pardoning me and my crew.  The materials I've shipped home have surely been invaluable for our preparations, and the moment the top brass decides they want to start the invasion, I can start spiking the outgoing liquors and cheerblossom with time-delay potions of your choice, crippling the Allied Kingdoms from within by starting a plague or turning every minor lawbreaker into a berserk madman.  If nothing else, the You-Know-What will be [i]very[/i] useful when push comes to shove.

As per your orders, we've restricted most of our intervention to sabotaging the Allied Kingdoms, but I wonder if some amount of focus on the orcs would be helpful.  A band of them has recently emerged from the Clork Peninsula, victorious over Sun Paladins and Atmos alike; we've lost contact with "Sunny Day," and "Vapor Trail" has kept exports to a minimum for fear of detection.  If we don't do something about this soon, they may become a bigger obstacle than the Allied Kingdoms.

I await your reply - and more dried meat, my crew loves the stuff and these smugglers can't be arsed to bring us something so mundane.]], [[总体分析：

头儿，如果我要说什么的话，那就是你饶恕我和我的船员是对的。那些我运回家的材料确实对我们的准备很有价值。只要高层决定开始入侵，我就能在外运的酒类和鼓舞之花中掺入你指定的延时药剂，通过引发瘟疫，或把每个犯点小罪的人都变成狂暴疯子，从内部瘫痪联合王国。无论如何，那个“你懂的”在最终关头会[i]非常[/i]有用。

根据你的命令，我们已把大部分干预行动限制在破坏联合王国上，但是我觉得多一些对于兽人们的关注也可能有好处。一帮兽人最近从克拉克半岛出现，战胜了太阳骑士和气之部族；我们已失去与“大晴天”的联系，而“汽化液之径”害怕被觉察，把他们的出口活动限制在最小。如果我们不赶紧做些什么的话，他们可能变成比联合王国更大的阻碍。

我等待你的回复，以及更多肉干，我的船员喜欢这个，而那些走私者懒得给我们送来这种平凡的东西。]], "_t")

------------------------------------------------

section "tome-orcs/data/quests/yeti-abduction.lua"

t("Yeti Reinforcements", "雪人援军", "_t")
t("You found a yeti mind control tinker. If you can tame 8 wild yetis and send them back to Kruk Pride they can be trained and sent back to you at your request using a psychoportation beacon.", "你找到了一个雪人心灵控制器配件。如果你能驯服 8 只野生雪人并将它们送回克鲁克部落，它们便可接受训练；之后你可以通过精神传送信标，随时将它们召回身边。", "_t")
t("Wild yetis are mostly found in yeti's caves.", "野生雪人主要出现在雪人洞穴。", "_t")
t("#LIGHT_GREEN#* Captured eight yetis (will be available to summon at level 20).#WHITE#", "#LIGHT_GREEN#* 抓住了八只雪人（你至少需要20级才能召唤他们）#WHITE#", "_t")
t("#LIGHT_GREY#* Captured %d/8 yetis.#WHITE#", "#LIGHT_GREY#* 捕获了 %d/8 个雪人。#WHITE#", "tformat")
t("Yeti's Psychoportation Beacon", "雪人精神传送信标", "_t")
t("Call a trained yeti to your side.", "召唤雪人来协助你。", "_t")
t("Yetis left to call: %d", "剩余可召唤的雪人：%d", "tformat")
t("call a trained yeti for help", "召唤受训练的雪人来帮助你", "_t")
t("The yetis are not ready yet.", "雪人还没有准备好。", "log")
t("Yeti", "雪人", "_t")
t("You extract the psychoportation beacon from the mind controller. Yetis will require some time to train before being usable.", "你从精神控制器上提取精神传送信标。雪人需要一些时间来训练才能使用。", "log")
-- untranslated text
--[==[
t("", "", "_t")
--]==]


------------------------------------------------

section "tome-orcs/data/talents/celestial/crepescula.lua"

t("Twilit Echoes", "暮光回响", "talent name")
t([[The target feels the echoes of all your light and dark damage for %d turns. 

Light damage slows the target by %0.2f%% per point of damage dealt for %d turns, up to a maximum of %d%% at %d damage.
Dark damage creates an effect at the tile for %d turns which deals %d%% of the damage dealt each turn. It will be refreshed as long as the target continues taking damage from it or another source while Twilit Echoes is active, dealing its remaining damage over the new duration as well as the new damage.]], [[目标会感受到你造成的所有光系和暗影伤害的回响，持续 %d 回合。

每造成 1 点光系伤害，目标便会减速 %0.2f%%，持续 %d 回合；减速上限为 %d%%，造成 %d 点伤害时达到上限。
暗影伤害会在目标所在格产生一个持续 %d 回合的效果，每回合造成该次伤害的 %d%%。在暮光回响生效期间，只要目标继续受到此效果或其他来源的伤害，该地块效果就会刷新；剩余伤害和新伤害会一并分摊到新的持续时间内。]], "tformat")

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

section "tome-orcs/data/timed_effects/other.lua"

t("speed", "速度", "effect subtype")
t("Celestial Acceleration", "天体加速", "_t")
t("Your movement speed is increased by %d%%.", "移动速度增加 %d%%。", "tformat")
t("Your casting speed is increased by %d%%.", "施法速度增加 %d%%。", "tformat")
t("Your attack speed is increased by %d%%.", "攻击速度增加 %d%%。", "tformat")
t("Your mind speed is increased by %d%%.", "精神速度增加 %d%%。", "tformat")
t("Your global speed is increased by %d%%.", "整体速度增加 %d%%。", "tformat")
t("spacetime", "时空", "effect subtype")
t("Outside the Starscape", "星界之外", "_t")
t("This unit is outside of the starscape and cannot be harmed from within it,", "该单位处于星界外，不能被星界内单位伤害。", "_t")
t("confusion", "混乱", "effect subtype")
t("Mindblasted", "精神震爆", "_t")
t("The target is confused, acting randomly (chance %d%%) and unable to perform complex actions.", "目标陷入混乱，有 %d%% 几率随机行动，并且无法执行复杂动作。", "tformat")
t("#Target# wanders around!", "#Target#漫无目的地四处游荡！", "_t")
t("+Confused", "+混乱", "_t")
t("#Target# seems more focused.", "#Target#恢复了理智。", "_t")
t("-Confused", "-混乱", "_t")
t("sun", "太阳", "effect subtype")
t("Shield of the Sun", "日光之盾", "_t")
t("The power of the Sun itself shields the target.", "太阳的力量保护着目标。", "_t")
t("TO THE MOUNTAINS!", "前往山上！", "_t")
t("A Light in the Darkness", "黑暗之光", "_t")
t("The power of the Sun imbues the target.", "太阳的力量充盈着目标。", "_t")
t("other", "其他", "effect subtype")
t("X-Ray Vision", "X光视觉", "_t")
t("Can see EVERYTHING.", "能看见一切事物。", "_t")
t("Aiming!", "瞄准！", "_t")
t("Aiming a powerful beam. MOVE OUT!", "正瞄准发射强力激光。快跑！", "_t")
t("#PURPLE#NEKTOSH AIMS A POWERFUL BEAM! #{bold}#MOVE!!#{normal}#", "#PURPLE#纳克托什使用强大的光线瞄准目标！#{bold}#快跑！！#{normal}#", "saySimple")
t("%s blinks away and summons some help!", "%s传送离开，召唤帮助！", "logSeen")
t("lightning", "闪电", "effect subtype")
t("Capacitor Discharge", "电力放出", "_t")
t("Storing damage to unleash as a powerful lightning bolt (%d/%d).", "已格挡伤害可累积至上限，准备放出强力闪电（%d/%d）。", "tformat")
t("tactical", "战术", "effect subtype")
t("Upgrade", "炮台升级", "_t")
t("This turret has been greatly enhanced.", "这个炮台被大幅强化了。", "tformat")
t("steamtech", "蒸汽科技", "effect subtype")
t("Guardian Shield", "守卫护盾", "_t")
t("%d%% of all incoming damage is redirected to the adjacent Guardian Turret.", "所受到的伤害的 %d%% 会转移到邻近的守卫炮台上。", "tformat")
t("#STEEL_BLUE#(%d shared)#LAST#", "#STEEL_BLUE#(%d 伤害共享)#LAST#", "tformat")
t("Countdown", "倒计时", "_t")
t("At the end of this effect, your missile will explode!", "导弹会在该效果到时间后爆炸！", "tformat")
t("Locked On", "目标锁定", "_t")
t("Automatically firing a missile barrage against a target for %d%% increased damage.", "自动朝目标发射火箭弹幕，伤害增加 %d%%。", "tformat")
t("The target has been marked by a rocket pod, reducing defence by %d and negating all evasion effects.", "目标被火箭发射器锁定，降低闪避值 %d，且躲闪效果失效。", "tformat")
t("#Target# has been marked by a rocket pod!", "#Target#被火箭发射器锁定！", "_t")
t("+Locked On", "+目标锁定", "_t")
t("#Target# is no longer being marked by a rocket pod.", "#Target#不再被火箭发射器锁定。", "_t")
t("-Locked On", "-目标锁定", "_t")
t("miscellaneous", "杂项", "effect subtype")
t("Mecharachnid out of sight", "视野外的机械蜘蛛", "_t")
t("The Mecharachnid is out of sight of the annihilator; direct control will be lost!", "机械蜘蛛已脱离歼灭者视野；若未能在四回合内恢复视线，将失去直接控制！", "_t")
t("#LIGHT_RED##Target# is out of sight of its master; direct control will break!", "#LIGHT_RED##Target#在主人视野外；直接控制中断了！", "_t")
t("+Out of sight", "+视野外", "_t")
t("#LIGHT_RED#You lost sight of your mecharachnid for too long; direct control is broken!", "#LIGHT_RED#你失去机械蜘蛛视野太久，直接控制被中断了！", "logPlayer")
t("mecharachnid out of sight", "机械蜘蛛在视野外", "_t")
t("Piloted", "正在驾驶", "_t")
t("Currently piloted.", "正在驾驶机械蜘蛛。", "tformat")
t("#GREEN#%s takes direct control of their mecharachnid!", "#GREEN#%s 直接控制机械蜘蛛！", "logSeen")
t("Direct Control", "直接控制", "_t")
t("Direct control by the pilot increases damage by %d%% and resistances by %d%%.", "机械蜘蛛被驾驶员直接控制，增加全部伤害 %d%%，增加全部抗性 %d%%；每回合使非固定冷却技能额外减少 1 回合冷却。", "tformat")
t("Heavy Ammunition", "重装武器弹药", "_t")
t("%d Ammo", "%d 弹药", "tformat")
t("Has %d heavy ammunition loaded. Current heavy weapon will be unequiped when no ammunitions are left.", "目前装载了 %d 枚重装武器弹药。如果弹药耗尽，会自动取下当前的重装武器。", "tformat")
t("Stormstrike", "暴风打击", "_t")
t("The target has been staggered, reducing all damage dealt by %d%%.", "目标站立不稳，造成的所有伤害降低 %d%%。", "tformat")
t("acid", "酸性", "effect subtype")
t("Catalyst", "催化剂", "_t")
t("The target has been injected with chemicals, reducing all saves by %d.", "目标被化学药剂注射，降低所有豁免 %d。", "tformat")
t("healing", "治疗", "effect subtype")
t("Automated Repair System", "自动修复系统", "_t")
t("Engaged in automated repairs, preventing any action but increasing life regen by %d, all resistances by %d%% and preventing death until falling below -%d life.", "进入自动修复模式，无法行动，但生命恢复速率增加 %d，生命值回满时立即结束该模式，全部抗性提升 %d%%，死亡生命下限为 -%d。", "tformat")
t("#Target# shuts down and engages its automated repair system.", "#Target#关机，启动自动修复系统。", "_t")
t("+Automated Repair System", "+自动修复系统", "_t")
t("#Target#'s repairs are complete.", "#Target#修复完成。", "_t")
t("-Automated Repair System", "-自动修复系统", "_t")
t("Demagnetized", "消磁", "_t")
t("Beneficial effects of Magnetic Field lost.", "失去磁性力场所给予的增益效果。", "tformat")
t("technomancy", "科技法术", "effect subtype")
t("spell", "法术", "effect subtype")
t("Galvanic Rods", "放电柱", "_t")
t([[Rods available:
]], [[可用放电柱：
]], "_t")
t([[#LIGHT_GREEN#- Rod (%d): available
]], [[#LIGHT_GREEN#- 放电柱 (%d): 可用
]], "tformat")
t([[#LIGHT_RED#- Rod (%d): %d turns
]], [[#LIGHT_RED#- 放电柱 (%d): %d 回合
]], "tformat")
t("cunning", "灵巧", "effect subtype")
t("Incoming Disasters", "灾祸临近", "_t")
t("Vulnerable to more cross tier effects.", "会受到更多跨层效果影响。", "tformat")

------------------------------------------------

section "tome-orcs/data/zones/internment-camp/objects.lua"

t("piece of correspondence", "一封信", "entity name")
t("An internal correspondence letter.", "内部信件。", "_t")

------------------------------------------------

section "tome-orcs/data/zones/ritch-hive/zone.lua"

t("Ritch Hive", "里奇巢穴", "_t")
t([[You arrive in a maze of shifty sand tunnels.
But you have with you the power of technology! You have been given a #GOLD#Stralite Sand Shredder#LAST#. Use it to dig yourself a path should there be none to be found.
#{italic}#Simply walk into a wall with the shredder equipped and the sand will crumble before you!#{normal}#

Beware to not draw too much attention to yourself, and do not forget to collect the eggs!]], [[你到达了一片由沙子形成的不断变化的通道构成的迷宫。
但是这一次，你有了科技的力量！你得到了一套#GOLD#斯莱特掘沙者#LAST#。若没有现成的通道，就用它为自己挖出一条路来。
#{italic}#只需要装备着掘沙者走向沙墙，这面沙墙就会在你面前坍塌！#{normal}#

小心不要引起太多注意，也不要忘了收集里奇虫卵！]], "_t")
t("%d Collected", "已收集：%d", "tformat")

------------------------------------------------

section "tome-orcs/data/zones/sunwall-outpost/npcs.lua"

t("human", "人类", "entity subtype")
t("Outpost Leader John", "前哨站队长约翰", "entity name")
t("This warrior's armor glows with a bright golden light. He wields an ornate sword and shield, and marches towards you with confidence.", "这位战士的盔甲闪耀着璀璨的金光。他挥动华丽的剑与盾，自信地向你冲来。", "_t")
t("humanoid", "人形生物", "entity type")
t("orc", "兽人", "entity subtype")
t("orc retaliator", "兽人反击者", "entity name")
t("A stern-looking orc, armed to the teeth.", "一个严肃的兽人，武装到牙齿。", "_t")
t("orc gunslinger", "兽人快枪手", "entity name")
t("A nasty looking orc armed with double steamguns.", "一个面目凶恶的兽人，手持两把蒸汽枪。", "_t")

------------------------------------------------

section "tome-orcs/overload/mod/class/interface/PartyTinker.lua"

t("unknown tinker", "未知插件", "_t")
t("can not create tier %d", "无法创建等级%d", "tformat")
t("requires %s level %d", "需要%s等级%d", "tformat")
t("requires %d %s", "需要%d个%s", "tformat")
t("requires %s", "需要%s", "tformat")
t("Impossible to create %s(%s)", "无法创造 %s(%s)", "tformat")
t("Created tinker: %s", "创造插件：%s", "log")
t("Created tinker: %s", "创造插件：%s", "saySimple")
t("Learnt new tinker schematic: #LIGHT_GREEN#%s", "已学习新的配方：#LIGHT_GREEN#%s", "log")
t("Learnt new tinker schematic: #LIGHT_GREEN#%s", "已学习新的配方：#LIGHT_GREEN#%s", "saySimple")

------------------------------------------------

section "tome-possessors/data/talents/psionic/psychic-blows.lua"

t("You are disarmed.", "你被缴械了。", "logPlayer")
t("You require a two handed weapon to use this talent.", "你需要装备一把双手武器来施展这个技能。", "logPlayer")
t("Psychic Crush", "精神粉碎", "talent name")
t("%s's Psychic Image", "%s的精神影像", "tformat")
t("A temporary psionic imprint.", "一个临时的心灵印记", "_t")
t("#ROYAL_BLUE#%s's psychic imprint appears!", "#ROYAL_BLUE#%s的心灵印记浮现了！", "logSeen")
t("%s resists the psychic blow!", "%s抵抗了精神打击！", "logSeen")
t([[Using both your mind and your arms you propel your two handed weapon to deal a huge strike doing %d%% weapon mind damage.
		If the blow connects and the target fails a mental save there is %d%% chance that the blow was so powerful it ripped a psychic imprint off the target.
		It will appear nearby and serve you for %d turns.
		If you do not have a two handed weapon equiped, but have it in your off set, you instantly automatically switch.]], [[用双手武器攻击敌人造成 %d%% 武器精神伤害。
		如果命中且目标没有通过精神豁免有 %d%% 几率剥夺目标的心灵印记。
		它会出现在附近，并为你服务 %d 回合。
		如果你没有装备双手武器，但在备用武器组里装备了它，你会立刻自动切换到那组武器。]], "tformat")
t("Force Shield", "力场盾", "talent name")
t([[You create a psionic shield from your weapon that prevents you from ever taking blows that deal more than %d%% of your maximum life and gives you %d%% evasion.
		In addition, each time you take a melee hit the attacker automatically takes revenge strike that deals %d%% weapon damage as mind damage. (This effect can only happen once per turn)
		If you do not have a two handed weapon equiped, but have it in your off set, you instantly automatically switch.]], [[你通过武器创造灵能力场盾，每次受到伤害时，伤害不会超过最大生命值 %d%%，并有 %d%% 的几率闪避攻击。
		此外，每次受到近战攻击时，攻击者会受到 %d%% 武器精神伤害的反击，（每回合一次）
		如果你没有装备双手武器，但在备用武器组里装备了它，你会立刻自动切换到那组武器。]], "tformat")
t("Unleashed Mind", "心灵释放", "talent name")
t([[You concentrate your powerful psionic powers on your weapon and briefly unleash your fury.
		All foes in radius %d will take a melee attack dealing %d%% weapon damage as mind damage.
		Any psionic clones in the radius will have its remaining time extended by %d turns.
		If you do not have a two handed weapon equiped, but have it in your off set, you instantly automatically switch.]], [[你将强大的灵能力集中在你的武器上，并短暂地释放你的愤怒。
		半径 %d 内的敌人受到近战攻击造成 %d%% 武器精神伤害。
		范围内所有灵能克隆体的剩余持续时间延长 %d 回合。
		如果你没有装备双手武器，但在备用武器组里装备了它，你会立刻自动切换到那组武器。]], "tformat")
t("Seismic Mind", "心灵地震", "talent name")
t([[You shatter your weapon in the ground, projecting a psionic shockwave in a cone of radius %d.
		Any foes in the area will take %d%% weapon damage as mind damage.
		Any psionic clones hit will instantly shatter, exploding for %0.2f physical damage in radius 1.
		If you do not have a two handed weapon equiped, but have it in your off set, you instantly automatically switch.]], [[你在地面上打碎你的武器，将一个心灵的冲击波投射在半径为 %d 的圆锥上。
		范围内的所有敌人受到 %d%% 武器精神伤害。
		任何被击中的灵能克隆体将立即破碎，在半径 1 的范围内爆炸造成 %0.2f 物理伤害。
		如果你没有装备双手武器，但在备用武器组里装备了它，你会立刻自动切换到那组武器。]], "tformat")

------------------------------------------------

section "tome-possessors/data/timed_effects.lua"

t("psionic", "灵能", "effect subtype")
t("possession", "附身", "effect subtype")
t("Ominous Form", "不祥躯体", "_t")
t("You stole your current form and share damage and healing with it.", "你偷取了当前躯体，并和它共享伤害与治疗。", "_t")
t("Assume Form", "附身", "_t")
t("You use the body of one of your fallen victims. You can not heal in this form.", "你使用你最近消灭的敌人的身体。在这个状态下你不能被治疗。", "_t")
t("#CRIMSON#While you assume a form you may not levelup. All exp gains are delayed and will be granted when you reintegrate your own body.", "#CRIMSON#当你附身一个身体的时候，你不能升级。所有获得的经验值都会被保存，在你回到自己的身体的时候获得。", "_t")
t("#CRIMSON#Your body died! You quickly return to your normal one but the shock is terrible!", "#CRIMSON#你的身体死掉了！你快速回到了你原来的身体，但是这对你产生了极大的冲击！", "say")
t("was killed by possession aftershock", "被附身的影响杀死", "_t")
t("Kryl-Feijan", "克里尔·费扬", "_t")
t("Your possessed body's eyelids briefly flutter, and a tear rolls down its cheek. You didn't tell it to do that.", "你控制的身躯眼睑微微颤动，眼泪顺着脸颊滚落。你没有让它这么做。", "_t")
t("Shasshhiy'Kaish", "莎西·凯希", "_t")
t("The flames surrounding Shasshhiy'Kaish slowly die as she falls to her knees.  \"Fiend...  and I thought #{italic}#I#{normal}# could cause suffering.  It's the one thing Eyalites always did best,\" she spits.  \"I heard what had happened to him, and my followers have given more than enough of their life to restore me after this.  All you've accomplished here - [cough] - is giving us a worthwhile new goal...  and target.  All will be repaid tenfold, Eyalite.\"  Her coughing grows weaker, until she abruptly bursts into flame; her ashes scatter into the wind.", "莎西·凯希跪倒在地，她周围的火焰慢慢熄灭。“你们才是真正的恶魔……我以为#{italic}#我#{normal}#是制造痛苦的大师。但现在看来，你们埃亚尔人才是最擅长带来折磨的人。”她啐了一口唾沫。“我听说了他所发生的事情，我的追随者给了我足够的生命，让我可以东山再起。你对我所做的一切——【咳嗽】——只是给了我一个新的目标……一个复仇的对象。你们所做的一切都将被十倍偿还，埃亚尔人。”她的咳嗽声越来越轻，直到最终迸发成一团火焰。她的灰烬散落在风中。", "_t")
t("High Sun Paladin Aeryn", "高阶太阳骑士艾琳", "_t")
t("Aeryn's bewildered and terrified cries grow quiet, but...  your ears don't ring or hurt as screams of horror and rage surround you, louder than should be deafening.  When they shift to accusations, an unfamiliar guilt dominates your thoughts; you are forced to abandon your body before it can compel you to punish yourself.", "艾琳困惑而惊恐的哭声渐渐平静下来，但是……当恐惧和愤怒的尖叫声围绕着你，比震耳欲聋还要响亮的时候，你的耳朵不会响也不会痛。当他们转向指责时，一种陌生的罪恶感支配着你的思想；在它迫使你惩罚自己之前，你被迫放弃你的身体。", "_t")
t("stun", "震慑", "effect subtype")
t("Possession Aftershock", "附身余震", "_t")
t("The target is reeling from the aftershock of a destroyed possessed body, reducing damage by 60%%, reducing movement speed by 50%%.", "目标正承受附身躯体被摧毁后的余震，伤害减少 60%%, 移动速度减少 50%%。", "tformat")
t("#Target# is stunned!", "#Target#被震慑！", "_t")
t("+Stunned", "+震慑", "_t")
t("#Target# is not stunned anymore.", "#Target#不再被震慑。", "_t")
t("-Stunned", "-震慑", "_t")
t("possess", "附身", "effect subtype")
t("mind", "精神", "effect subtype")
t("Possess", "附身", "_t")
t("The victim is snared in a psionic web that is destroying its mind and preparing its body for possession.  It takes %0.2f Mind damage per turn.", "目标被困在灵能网中，其心智正被摧毁，身体正为附身做准备。每回合受到 %0.2f 精神伤害。", "tformat")
t("#Target#'s mind is convulsing.", "#Target#的精神在抽搐。", "_t")
t("#Target#'s mind is not convulsing anymore.", "#Target#的精神不再抽搐。", "_t")
t("#PURPLE##Source# shatters #Target#'s mind and takes possession of its body.", "#PURPLE##Source#粉碎了#Target#的精神，控制了它的身体。", "logCombat")
t("#PURPLE##Source# shatters #Target#'s mind, utterly destroying it.", "#PURPLE##Source#粉碎了#Target#的精神，完全摧毁了它。", "logCombat")
t("Psychic Wipe", "精神抹除", "_t")
t("Ethereal fingers destroy the brain dealing %0.2f mind damage per turn and reducing mental save by %d.", "空灵手指摧毁目标大脑，每回合造成 %0.2f 精神伤害，并减少 %d 精神豁免。", "tformat")
t("#Target# suddently feels strange in the brain.", "#Target# 突然觉得脑袋里很奇怪。", "_t")
t("#Target# feels less strange.", "#Target#不再觉得奇怪。", "_t")
t("Ghastly Wail", "恐怖嚎叫", "_t")
t("The target is dazed, rendering it unable to move, halving all damage done, defense, saves, accuracy, spell, mind and physical power. Any damage will remove the daze.", "目标被眩晕，无法移动，所有攻击伤害、闪避、豁免、命中、法术、精神和物理强度减半。任何伤害均会打断眩晕效果。", "_t")
t("#Target# is dazed!", "#Target#被眩晕！", "_t")
t("+Dazed", "+眩晕", "_t")
t("#Target# is not dazed anymore.", "#Target#从眩晕中恢复。", "_t")
t("-Dazed", "-眩晕", "_t")
t("Mind Steal", "精神窃取", "_t")
t("Stolen talent: %s", "偷取技能: %s", "tformat")
t("#Target# stole a talent!", "#Target#偷取了一个技能！", "_t")
t("#Target# forgot a talent.", "#Target#忘掉了一个技能。", "_t")
t("%s can not use %s because it was stolen!", "%s无法使用%s，因为它被偷走了！", "_t")
t("Writhing Psionic Mass", "扭动灵能团", "_t")
t("All resists increased by %d%%, chance to be crit reduced by %d%%.", "所有抗性增加 %d%%, 被暴击率减少 %d%%。", "tformat")
t("#Target#'s body writhe in psionic energies!", "#Target#的身体在灵能中扭曲！", "_t")
t("#Target#'s body looks more at rest.", "#Target#的身体恢复了原状。", "_t")
t("damage", "伤害", "effect subtype")
t("Psionic Disruption", "灵能瓦解", "_t")
t("%d stacks. Each stack deals %0.2f mind damage per turn.", "%d 层。每层效果每回合造成 %0.2f 精神伤害。", "tformat")
t("#Target# is disprupted by psionic energies!", "#Target#被灵能力量干扰！", "_t")
t("#Target# no longer tormented by psionic energies.", "#Target#不再被灵能力量折磨。", "_t")
t("Psionic Block", "灵能格挡", "_t")
t("%d%% chances to ignore damage and to retaliate with %0.2f mind damage.", "%d%% 几率无视伤害并反击 %0.2f 精神伤害。", "tformat")
t("#Target# is protected by a psionic block!", "#Target#被灵能格挡保护！", "_t")
t("#Target# no longer protected by the psionic block.", "#Target#不再被灵能格挡保护。", "_t")
t("#ROYAL_BLUE#The attack against %s is cancelled by a psionic block!", "#ROYAL_BLUE#对%s的攻击被灵能格挡！", "logSeen")
t("Sadist", "虐待狂", "_t")
t("Mindpower (raw) increased by %d.", "精神强度（原始值）增加 %d。", "tformat")
t("#Target# is empowered by the suffering of others!", "#Target#被其他人的痛苦强化！", "_t")
t("#Target# is no longer empowered.", "#Target#不再被强化。", "_t")
t("Radiate Agony", "痛苦辐射", "_t")
t("All damage reduced by %d%%.", "所有伤害减少 %d%%。", "tformat")
t("#Target# focuses on pain!", "#Target#聚焦痛苦！", "_t")
t("#Target# is no longer focusing on pain.", "#Target#不再聚焦痛苦。", "_t")
t("lock", "封锁", "effect subtype")
t("Tortured Mind", "精神拷打", "_t")
t("%d talents unusable.", "%d 项技能不能使用。", "tformat")
t("#Target# is tormented!", "#Target#被折磨！", "_t")
t("#Target# is less tormented.", "#Target#的痛苦减轻了。", "_t")
t("%s can not use %s because of Tortured Mind!", "由于精神拷打，%s无法使用%s！", "_t")

------------------------------------------------
