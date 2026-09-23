section "tome-cults/overload/mod/class/CultsDLC.lua"

t("Insanity", "疯狂值", "_t")
t([[Your mental insanity.  The higher it is the more random your damage and cooldowns become.

Damage and cooldowns have a chance to increase or decrease by up to chaotic%.

Both the chance and size of effects will increase with insanity.]], [[你的精神的疯狂程度。这一数值越高，你的技能的冷却时间和所造成的伤害随机性就越大。

伤害和冷却时间将会在 混沌度% 的范围内上下浮动。

浮动的几率和浮动的效果都会随疯狂值提升而上升。]], "_t")
t("%d%%%% (%d%%%% chaotic)", "%d%%%% (%d%%%% 混沌度)", "tformat")
t("Use the book-like display for Forbidden Tomes. This option requires both framebuffers and shaders to be active in the video options.#WHITE#", "在禁忌之书中使用书本式显示效果。这一效果需要在图像设置里开启帧缓冲和着色器。#WHITE#", "_t")
t("#GOLD##{bold}#Forbidden Cults: Use Book visual for forbidden tomes#WHITE##{normal}#", "#GOLD##{bold}#禁忌邪教：禁忌之书使用书本效果#WHITE##{normal}#", "_t")
t("enabled", "已启用", "_t")
t("disabled", "已禁用", "_t")
t("#CRIMSON#This was a very satisfying meal, 'you' feel strengthened. (+1 generic talent point)", "#CRIMSON#这份餐营养丰富，“你”觉得自己变强了（+1通用技能点）", "log")
t("#CRIMSON#[The parasite loves death and pain and gives no choice but to shoot down the airship]", "#CRIMSON#[寄生兽喜欢杀戮和痛苦，直接帮你按下了击落飞船的按钮。]", "_t")
t("#CRIMSON#[The parasite is hungry and promptly swallows and eat Melinda].", "#CRIMSON#[寄生兽很饿，吃下了梅琳达]。", "_t")
t("#CRIMSON#[The parasite is hungry and promptly swallows and eat Aeryn].", "#CRIMSON#[寄生兽很饿，吃下了艾琳]。", "_t")
t("#CRIMSON#[The parasite is hungry and attacks Slasul].", "#CRIMSON#[寄生兽很饿，攻击了萨拉苏尔]。", "_t")
t("#CRIMSON#[The parasite is hungry and promptly swallows and eat %s].", "#CRIMSON#[寄生兽很饿，吃下了%s]。", "tformat")
t("#CRIMSON#[The parasite is hungry and takes over the conversation.]#LAST# I smelled a weakling here and wanted a nice meal. [point your finger at the captured merchant]", "#CRIMSON#[寄生兽很饿，接管了你们的对话。]#LAST#我闻到这里有股弱者的味道，我想要一顿美餐。[把你的手指指向被抓住的商人]", "_t")
t("Ah I see, you are a ...thing... of special tastes. Very well, I'd rather have you as a friend so have your meal and someday we may have some more business to do together.", "啊，我明白了，你是一个…品味独特的…家伙。很好，我希望你是我的朋友，所以吃吧，总有一天我们会有更多的生意要做。", "_t")
t("[eat the merchant]", "[吃掉商人]", "_t")
t("#CRIMSON#[The parasite is hungry and promptly swallows and eat Fillarel]#LAST# No I have not...", "#CRIMSON#[寄生兽很饿，直接吃掉了菲拉瑞尔]#LAST# 不，我不…", "_t")
t("#CRIMSON#[The parasite is hungry and promptly swallows and eat the yeek wayist]#LAST# I 'saved' you to get a nice meal...", "#CRIMSON#[寄生兽很饿，直接吃掉了夺心魔灵能力者]#LAST# 我“救你”是为了美餐一顿", "_t")
t("#RED#You can't enter a Forbidden Tome from here!#LAST#", "#RED#你不能在这里进入禁忌之书！#LAST#", "log")
t("The protagonist of the story is dead.", "故事的主角死了。", "_t")
t("#PURPLE#%s starts to crumble to dust, it will be gone once you exit it!", "#PURPLE#%s开始粉碎成尘土，如果你离开这本书，它就会消失！", "log")
t("%s of the Blightspawn", "枯萎之子 %s", "tformat")
-- untranslated text
--[==[
t("#AQUAMARINE#%s", "#AQUAMARINE#%s", "log")
--]==]


------------------------------------------------

section "tome-cults/overload/mod/dialogs/FontSacrifice.lua"

t([[The font of sacrifice allows you to spend gold to reroll specific parts of a random artifact or rare item (you must first unequip it).
Each reroll costs #GOLD#500 gold#LAST# for a lesser ego and #GOLD#1000 gold#LAST# for a greater ego per each time you've rerolled that ego type on the same object.
Lesser and Greater egos can only be rerolled into the same type, and only egos with compatible power sources will be offered.

Note:  Many egos and external talents don't currently display properly but will apply to the item correctly.]], [[牺牲之泉允许你花费金币来重置随机神器或稀有物品的部分属性（你必须先脱掉装备）。
重置价格与重置次数有关，重置一个低级词缀，每重置一次多花费#GOLD#500 金币#LAST#，高级词缀每次多花费#GOLD#1000 金币#LAST#。
低级词缀只能重置成低级词缀，高级词缀只能重置成高级词缀，只有力量来源相符的词缀才会被选中。

请注意：许多词缀和额外技能在这里不会正常显示，但是它们会正确地加在物品上。]], "_t")
t("Font of Sacrifice", "牺牲之泉", "_t")
t("Name", "名称", "_t")
t("Properties", "属性", "_t")
t("Reroll properties set", "重置该属性", "_t")
t("Not enough money", "金钱不足", "_t")
t("You need at least #GOLD#%s gold#LAST# to reroll this item.", "你需要至少#GOLD#%s 金币#LAST#才能重置这个物品。", "tformat")
t("Confirm", "确认", "_t")
t("So you want to spend #GOLD#%s gold#LAST# to reroll this set of properties?", "你想要花费#GOLD#%s 金币#LAST#重置这条物品属性吗？", "tformat")
t(" (Greater)", " （高级词缀）", "_t")
t("Type: %s / %s", "类型：%s/%s", "tformat")
t([[Powered by #VIOLET#arcane forces#LAST#
]], [[装备力量来源 #VIOLET#奥术力量#LAST#
]], "_t")
t([[Infused by #OLIVE_DRAB#nature#LAST#
]], [[装备力量来源 #OLIVE_DRAB#自然力量#LAST#
]], "_t")
t([[Infused by #ORCHID#arcane disrupting forces#LAST#
]], [[装备力量来源 #ORCHID#反魔法力量#LAST#
]], "_t")
t([[Crafted by #LIGHT_UMBER#a master#LAST#
]], [[装备制造者 #LIGHT_UMBER#某位大师#LAST#
]], "_t")
t([[Infused by #YELLOW#psionic forces#LAST#
]], [[装备力量来源 #YELLOW#灵能#LAST#
]], "_t")
t([[Powered by #CRIMSON#unknown forces#LAST#
]], [[装备力量来源 #CRIMSON#未知力量#LAST#
]], "_t")
t("#CRIMSON#Your timetravel has no effect on pre-determined outcomes such as this.", "#CRIMSON#你的时间穿越对这种已经预设好的结局没有任何作用。", "_t")
t("Select a properties set", "选择属性", "_t")
t("Select properties set #{bold}#\"%s\"#{normal}# ?", "选择属性#{bold}#\"%s\"#{normal}#？", "tformat")
t("Error!", "错误！", "_t")
t("The gizmocombobulator of the font seems to have failed, you have not been billed.", "牺牲之泉的组合装置失败了，你没有因此被扣款。", "_t")

------------------------------------------------

section "tome-cults/superload/mod/class/Game.lua"

t("Class: Cultist of Entropy", "职业：熵教徒", "_t")
t("Race: Drem", "种族：德瑞姆", "_t")
t("Race: Krog", "种族：克罗格", "_t")
t("Class tree: Scourge drake", "职业技能树：天谴之龙", "_t")
t("Class feature: Alchemist's Glass Golem", "职业特性：炼金术师的玻璃傀儡", "_t")
t("Saving is not possible in the S.M.A.C.K. Do you want to cancel the fight?", "不能在S.M.A.C.K里面存档。你确定要取消这场战斗吗？", "_t")
t("Urgent affair in Zigur", "发生在伊格的紧急事件", "_t")
t([[As you enter Last Hope a courier finds you to deliver a letter from Protector Myssil of Zigur:

%s, while you were away destroying arcane filth I have received grave news.
A group of Krogs has been ambushed and taken to a hidden ruin on the eastern shores of the sea of Sash near Zigur.
From what the scouts can tell they were taken by a group of necromancers, probably to do vile experiments on them.

All our other elite fighting forces are currently abroad, you are their only hope.
Please, go there at once, free them and show the necromancers filth the True Wrath of the Ziguranth!

#{italic}#Protector Myssil#{normal}#
]], [[当你进入最后的希望时，一个信使找到你并给你一份来自守护者米歇尔的信：

%s，当你在外面打击肮脏的奥术势力时，我收到了一个令人震惊的消息。
一群克罗格遭到伏击并被带到伊格附近的萨希海东海岸隐藏的废墟中。
侦察员看见他们被一群死灵法师带走，可能会对他们进行邪恶的实验。

我们其他所有的精英部队都在外面，你是他们唯一的希望。
请立刻去那里解救他们，并让死灵法师见识一下伊格兰斯的愤怒！

#{italic}#守护者米歇尔#{normal}#
]], "_t")
-- untranslated text
--[==[
t("S.M.A.C.K", "S.M.A.C.K", "_t")
--]==]


------------------------------------------------

section "tome-items-vault/overload/data/chats/items-vault-command-orb.lua"

t("Transfering this item will place a level %d requirement on it, since it has no requirements. ", "由于该物品没有等级限制，传输这个物品会给其施加%d的等级限制。", "tformat")
t("Some properties of the item will be lost upon transfer, since they are class- or talent-specific. ", "某些物品属性将会在传输的时候丢失，因为它们是部分职业/技能限定的。", "_t")
t([[*#LIGHT_GREEN#This orb seems to be some kind of interface to an extra-dimentional vault of items.
All your characters in alternate universes will be able to access it from here.
Only items from a validated game versions are uploadable.#WHITE#*

#GOLD#Donator's Feature#ANCIENT_WHITE#: Items are saved on the server, only donators have access to this feature and the number of items storable at once depends on your generosity.
I, DarkGod, the maker of this game want to personaly thank all donators because you people are keeping this game going. Thanks and enjoy!]], [[*#LIGHT_GREEN#这个水晶球看起来像是一个访问某个超次元物品仓库的接口。
你在其他宇宙中的所有角色都可以从这里访问它。
只有经过验证的游戏版本中的物品才能上载。#WHITE#*

#GOLD#捐赠者特权#ANCIENT_WHITE#: 物品保存在服务器上，只有捐赠者有权使用此功能，同时存储的物品数量取决于您的慷慨程度。
我，DarkGod，这个游戏的制作人，想要亲自感谢所有的捐赠者，是你们让这个游戏继续下去。谢谢，好好享受!]], "_t")
t("\
#CRIMSON#Note for Steam Players#ANCIENT_WHITE#: This feature requires you to have registered a profile & bound it to steam (automatic if you register ingame) because it needs to store things on the server.\
Until you do so you will get an error.", "\
#CRIMSON#对Steam玩家的提醒#ANCIENT_WHITE#: 因为这项功能需要你在服务器上存储数据，使用共享仓库需要你注册了游戏账户，并将其绑定到Steam（如果你在游戏内注册，这个过程将会自动完成）。\
否则，你将会遇到一个错误。", "_t")
t("[Place an item in the vault]", "[将物品放入共享仓库中]", "_t")
t("Item's Vault", "共享仓库", "_t")
t("You can not place an item in the vault from an un-validated game.", "你不能从未验证的游戏版本里将物品放入共享仓库。", "_t")
t("Place an item in the Item's Vault", "将物品放入共享仓库", "_t")
t("Caution", "注意", "_t")
t("Continue?", "继续吗？", "_t")
t("[Retrieve an item from the vault]", "[从共享仓库中取回物品]", "_t")
t("#GOLD#I wish to help the funding of this game and donate#WHITE#", "#GOLD#我想资助这个游戏并捐款#WHITE#", "_t")
t("[Leave the orb alone]", "[离开水晶球]", "_t")

------------------------------------------------

section "tome-items-vault/overload/mod/class/ItemsVaultDLC.lua"

t("the #GOLD#Item's Vault#WHITE#", "#GOLD#共享仓库#WHITE#", "_t")
t("\
#CRIMSON#This item has been sent to the Item's Vault.", "\
#CRIMSON#这个物品已被上传到共享仓库。", "_t")
t("Transfering...", "传输中…", "_t")
t("Teleporting object to the vault, please wait...", "正在将物品传输到共享仓库，请稍候…", "_t")
t("unknown reason", "原因不明", "_t")
t("#LIGHT_BLUE#You transfer %s to the online item's vault.", "#LIGHT_BLUE#你将%s传输到在线共享仓库。", "logPlayer")
t("#LIGHT_RED#Error while transfering %s to the online item's vault, please retry later.", "#LIGHT_RED#将物品%s传输到在线共享仓库时发生错误，请稍后再试。", "logPlayer")
t("#CRIMSON#Server said: %s", "#CRIMSON#服务器信息: %s", "logPlayer")
t("#LIGHT_BLUE#You transfer %s to the offline item's vault.", "#LIGHT_BLUE#你将%s传输到离线共享仓库。", "logPlayer")
t("Teleporting object from the vault, please wait...", "正在从共享仓库中接收物品，请稍候…", "_t")
t("Transfer failed", "传输失败", "_t")
t([[This item comes from a previous version and would not work in your current game.
To prevent the universe from imploding the item was not transfered from the vault.]], [[这一物品来自以前的游戏版本，无法在当前游戏中工作。
为了防止当前宇宙发生问题，你无法从共享仓库中取回这个物品。]], "_t")
t("Item's Vault", "共享仓库", "_t")
t("Checking item's vault list, please wait...", "正在检查共享仓库列表，请稍候…", "_t")

------------------------------------------------

section "tome-items-vault/overload/mod/dialogs/ItemsVault.lua"

t("Item's Vault", "共享仓库", "_t")
t("Impossible to contact the server, please wait a few minutes and try again.", "无法连接到服务器，请稍候几分钟，然后重试。", "_t")
t("Item's Vault (%d/%d)", "共享仓库 (%d/%d)", "tformat")
t([[Retrieve an item from the vault. When you place an item in the vault the paradox energies around it are so powerful you must wait one hour before retrieving it.
	#CRIMSON#Warning: while you *can* retrieve items made with previous versions of the game, no guarantee is given that the universe (or your character) will not explode.]], [[从共享仓库中拿取物品。当你将物品放入共享仓库的时候，会产生强大的悖论能量，你需要等待1小时才能取回它。
	#CRIMSON#警告: 尽管你 *可以* 取回来自以前游戏版本的物品，没有人保证宇宙（或你的角色）不会爆炸。]], "_t")
t("Name", "名称", "_t")
t("Usable", "可用", "_t")
t("#LIGHT_GREEN#Yes", "#LIGHT_GREEN#是", "_t")
t("#LIGHT_RED#In less than one minute", "#LIGHT_RED#剩余小于1分钟", "_t")
t("#LIGHT_RED#In %d minutes", "#LIGHT_RED#剩余约%d分钟", "tformat")
t("Cooldown", "冷却时间", "_t")
t("This item has been placed recently in the vault, you must wait a bit before removing it.", "该物品刚刚被放入共享仓库，你需要等待一段时间才能将其移除。", "_t")
t("#LIGHT_BLUE#You transfer %s from the online item's vault.", "#LIGHT_BLUE#你从在线共享仓库中取回物品%s。", "log")
t("#LIGHT_RED#Error while transfering from the online item's vault, please retry later.", "#LIGHT_RED#从在线共享仓库中获取物品失败，请稍候再试。", "log")

------------------------------------------------

section "tome-items-vault/overload/mod/dialogs/ItemsVaultOffline.lua"

t("Item's Vault", "共享仓库", "_t")
t("Impossible to contact the server, please wait a few minutes and try again.", "无法连接到服务器，请稍候几分钟，然后重试。", "_t")
t("Item's Vault (%d/%d)", "共享仓库 (%d/%d)", "tformat")
t([[Retrieve an item from the vault. When you place an item in the vault the paradox energies around it are so powerful you must wait one hour before retrieving it.
	#CRIMSON#Warning: while you *can* retrieve items made with previous versions of the game, no guarantee is given that the universe (or your character) will not explode.]], [[从共享仓库中拿取物品。当你将物品放入共享仓库的时候，会产生强大的悖论能量，你需要等待1小时才能取回它。
	#CRIMSON#警告: 尽管你 *可以* 取回来自以前游戏版本的物品，没有人保证宇宙（或你的角色）不会爆炸。]], "_t")
t("Name", "名称", "_t")
t("Usable", "可用", "_t")
t("#LIGHT_GREEN#Yes", "#LIGHT_GREEN#是", "_t")
t("#LIGHT_RED#In less than one minute", "#LIGHT_RED#剩余小于1分钟", "_t")
t("#LIGHT_RED#In %d minutes", "#LIGHT_RED#剩余约%d分钟", "tformat")
t("Cooldown", "冷却时间", "_t")
t("This item has been placed recently in the vault, you must wait a bit before removing it.", "该物品刚刚被放入共享仓库，你需要等待一段时间才能将其移除。", "_t")
t("#LIGHT_BLUE#You transfer %s from the offline item's vault.", "#LIGHT_BLUE#你从离线共享仓库中取回物品%s。", "log")
t("#LIGHT_RED#Error while transfering from the offline item's vault, please retry later.", "#LIGHT_RED#从离线共享仓库中获取物品失败，请稍候再试。", "log")


section "tome-orcs/data/achievements/special.lua"

t("No mercy!", "心狠手辣！", "achievement name")
t("Killed 1000 steam giants civilians.", "杀死 1000 名蒸汽巨人居民。", "_t")
t("Mercy, mercy!", "慈悲为怀", "achievement name")
t("Killed Talosis without any civilians deaths.", "杀死泰勒西斯但不杀死其他居民。", "_t")
t("This will make a big Omelette!", "搞个大家伙！", "achievement name")
t("Collected 40 ritch eggs in the Ritch Hive.", "在里奇巢穴中收集 40 枚里奇蛋。", "_t")
t("An Other Brick in the Wall", "特立独行", "achievement name")
t("Defeated Aeryn in the Gates of Morning without destroying the Observatory nor using ritches help.", "在晨曦之门打败艾琳，但不摧毁观星台，也不借助里奇的帮助。", "_t")
t("No Steam, No Palace. No Palace, No Palace!", "若无蒸汽，则无宫殿。若无宫殿，亦无宫殿！", "achievement name")
t("Destroyed the Palace of Fumes without first destroying the geothermal valves in the Steam Quarry.", "在不先摧毁蒸汽采石场中的地热阀的情况下摧毁烟雾宫殿。", "_t")
t("Here, I Think You Dropped This", "这是你掉的么？", "achievement name")
t("Killed Ureslak the Eternal while wielding Ureslak's Femur.", "拿着乌瑞斯拉克的大腿打败永恒的乌瑞斯拉克。", "_t")
t("Do not go gentle into that good night", "不要温和地走进那个良夜", "achievement name")
t("Trapped John.", "捕获约翰。", "_t")
t("I did not want that!", "非我本意", "achievement name")
t("Tricked Nektosh into killing one of his own people.", "令独角者纳克托什误杀己方。", "_t")
t("We weren't kidding!", "认真点，这不是个玩笑！", "achievement name")
t("Die to Nektosh's beam without being pinned, stunned, asleep, dazed, or confused.", "在没有被定身、震慑、沉睡、眩晕或混乱的情况下，被独角者纳克托什的光束杀死。", "_t")
t("Make Him Squirm", "榨干他", "achievement name")
t("Made Nektosh use up the last of his power, then left the area and ignored him until beating the game. The other Whitehooves will catch on any second now...", "让纳克托什用尽能量，然后离开区域并无视他，直到胜利为止。其他白蹄兽人随时都会发现真相……", "_t")
t("True Savior", "真正的救星", "achievement name")
t("Freed all the Orc Prides without killing a single mind-controlled orc.", "释放所有兽人部落，并且不杀死任何一名被精神控制的兽人。", "_t")
t("Mender", "修理工", "achievement name")
t("Destroyed the bosses of the Primal Forest without killing any uncorrupted treants.", "杀死原始森林的boss，同时不杀死任何一名未腐化的树精。", "_t")
t("Sufficiently Advanced Technology", "高科技", "achievement name")
t("Put five points into each of the tinker-crafting talents as any mage class.", "作为任何法师职业，将每个蒸汽配件制造技能均投入5点技能点数。", "_t")
t("Radiant Horrorc", "光明克星", "achievement name")
t("While fighting in a Sunwall zone, use a Fiery Salve to reach at least 66% affinity for Fire and Light. Pointing and laughing is optional.", "在晨曦之门的区域内战斗时，开启烈火药剂，并获得至少 66% 火焰和光明吸收。指指点点和嘲笑，随你便。", "_t")
t("Blood on the Moon", "月上血痕", "achievement name")
t("Kill all of the Star Gazers within 7 game turns.", "7个游戏回合内击杀所有观星者。", "_t")
t("Once Upon A Time, In the West...", "很久很久以前，在西方……", "achievement name")
t("Hear the Eidolon's retelling of the Scourge from the West's journey.", "听艾德隆讲述西方天灾的旅程。", "_t")
t("A Fistful of Gold", "一大堆金币", "achievement name")
t("Buy an item from an AAA.", "从 AAA 买东西。", "_t")
t("For a Few Gold More", "更多金币", "achievement name")
t("Completely deplete an AAA's stock.", "清空一个AAA的库存。", "_t")
t("The Good, The Bad, and The Yeti", "好人、坏人和雪人", "achievement name")
t("Use mind-controlled yetis to kill 30 foes.", "使用被精神控制的雪人，击杀30名敌人。", "_t")
t("Total Annihilation: Redundancy", "完全歼灭：多此一举", "achievement name")
t("Wield the Annihilator as an Annihilator.", "作为歼灭者（职业），装备歼灭者（武器）。", "_t")

------------------------------------------------

section "tome-orcs/data/achievements/story.lua"

t("Across the Narrow Sea", "跨越狭海", "achievement name")
t("Destroyed the Sunwall Outpost to secure a way to the mainland.", "消灭太阳堡垒前哨站，以确保通往大陆的道路。", "_t")
t("Reclaiming Garkul's Heritage", "加库尔之遗产", "achievement name")
t("Freed the remnants of the Prides from the Internment Camp.", "释放拘留营中的部落成员。", "_t")
t("The High Lady's Destiny (Finale)", "艾琳的陨落", "achievement name")
t("Crushed High Sun Paladin Aeryn and with her destroyed the bastion of the Sunwall.", "杀死高阶太阳骑士艾琳，并摧毁晨曦之门。", "_t")
t("One Ill Turn Deserves Another", "以眼还眼", "achievement name")
t("The Palace of Fumes stands in ruins, its Council shattered. The Atmos Tribe will not bother the Prides anymore.", "烟雾宫殿被摧毁，议会分崩离析。气之部族不再威胁你的部落。", "_t")
t("The Dead God Rests", "亡神沉眠", "achievement name")
t("You have defeated the Sher'tul Priest trying to resurrect Amakthel, saving both the Prides and the world.", "你消灭了试图复活阿马克泰尔的夏·图尔牧师，拯救了部落和世界。", "_t")
t("To the Bitter End", "直至最后", "achievement name")
t("You have destroyed the last remnants of the Atmos Tribe, ending their civilization.", "你消灭了气之部族的最后成员，终结了他们的文明。", "_t")
t("Imp'ing Away", "飞走的小鬼", "achievement name")
t("You have spared the last remnants of the Atmos Tribe, showing mercy where others gave none to the orcs.", "你拯救了气之部族的最后成员，展现了兽人未曾得到的仁慈。", "_t")

------------------------------------------------

section "tome-orcs/data/birth/classes/empyreal.lua"

t("Empyreal", "高天者", "birth descriptor name")
t("Their most important stats are: Magic and Constitution", "他们最重要的属性是：魔法和体质。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +0 Strength, +0 Dexterity, +3 Constitution", "#LIGHT_BLUE# * +0 力量，+0 敏捷，+3 体质", "_t")
t("#LIGHT_BLUE# * +6 Magic, +0 Willpower, +0 Cunning", "#LIGHT_BLUE# * +6 魔法，+0 意志，+0 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# +0", "#GOLD#每等级生命加值：#LIGHT_BLUE# +0", "_t")

------------------------------------------------

section "tome-orcs/data/birth/classes/tinker.lua"

t("Tinker", "工匠系", "birth descriptor name")
t("Tinkers use steamtech to power their attacks, defenses, ...", "工匠们使用蒸汽科技来强化攻击、防御，……", "_t")
t("Build, experiment, discover. The path of inventions is never over!", "制造、实验、发现。创造之路永无止境！", "_t")
t("%s healing salve", "%s 治疗药剂", "tformat")
t("simple", "简单的", "_t")
t("%s frost salve", "%s 寒霜药剂", "tformat")
t("Sawbutcher", "链锯屠夫", "birth descriptor name")
t("A formidable behemoth of war using steamsaws to improve his deadliness.", "可怕的战争巨兽，使用蒸汽链锯增加致命杀伤力。", "_t")
t("Their most important stats are: Strength and Cunning", "他们最重要的属性是：力量和灵巧", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +5 Strength, +0 Dexterity, +1 Constitution", "#LIGHT_BLUE# * +5 力量，+0 敏捷，+1 体质", "_t")
t("#LIGHT_BLUE# * +0 Magic, +0 Willpower, +3 Cunning", "#LIGHT_BLUE# * +0 魔法，+0 意志，+3 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# 2", "#GOLD#每等级生命加值：#LIGHT_BLUE# 2", "_t")
t("Gunslinger", "枪手", "birth descriptor name")
t("A tinker who dual-wields steamguns to great effect.", "双持蒸汽枪的工匠。", "_t")
t("Their most important stats are: Cunning and Dexterity", "他们最重要的属性是：灵巧和敏捷", "_t")
t("#LIGHT_BLUE# * +0 Strength, +4 Dexterity, +1 Constitution", "#LIGHT_BLUE# * +0 力量，+4 敏捷，+1 体质", "_t")
t("#LIGHT_BLUE# * +0 Magic, +0 Willpower, +4 Cunning", "#LIGHT_BLUE# * +0 魔法，+0 意志，+4 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# -1", "#GOLD#每等级生命加值：#LIGHT_BLUE# -1", "_t")
t("Psyshot", "灵能射手", "birth descriptor name")
t("Bend the mind, bend the tech. All around inspire dread.", "扭曲精神，扭曲科技，一切都是为了激发恐惧。", "_t")
t("Powerful psionics are able to enter a gestalt with steam generators and technology to enhance their own mental prowess.", "强大的灵能使用者能够与蒸汽发生器和科技形成格式塔联结，以增强自身的精神力量。", "_t")
t("The Psyshot combines this ability to gestalt to enhance his mindstar all the while shooting her steamgun to devastate the enemy lines.", "灵能射手将这项能力与格式塔结合，来强化灵晶的力量，同时使用蒸汽枪毁灭敌人。", "_t")
t("Their most important stats are: Cunning, Willpower and Dexterity", "他们最重要的属性是：灵巧、意志和敏捷", "_t")
t("#LIGHT_BLUE# * +0 Strength, +3 Dexterity, +0 Constitution", "#LIGHT_BLUE# * +0 力量，+3 敏捷，+0 体质", "_t")
t("#LIGHT_BLUE# * +0 Magic, +3 Willpower, +3 Cunning", "#LIGHT_BLUE# * +0 魔法，+3 意志，+3 灵巧", "_t")
t("Annihilator", "歼灭者", "birth descriptor name")
t("The Annihilator is a master of destruction, wielding the most devastating steamtech inventions to lay waste to their foes.", "歼灭者是破坏的大师，他们掌握着最具破坏力的蒸汽科技成果，可以给他们的敌人带来无尽的毁灭。", "_t")
t("While normally wielding a steamgun loaded with experimental ammunition and an electrically charged shield, they can equip heavy weapons such as flamethrowers.", "他们通常装备着装载着实验性弹药的蒸汽枪和一面电力充能的盾牌，但他们也可以装备像火焰喷射器那样的重装武器。", "_t")
t("More adept at technology than most other tinkers, they supplement their weapons with automated turrets, mechanical minions and other such devices.", "他们比其他的工匠更加精通科学技术，他们使用自动炮台、机械随从和各种各样的强大发明来充实自己的武器库。", "_t")
t("#LIGHT_BLUE# * +0 Strength, +4 Dexterity, +0 Constitution", "#LIGHT_BLUE# * +0 力量，+4 敏捷，+0 体质", "_t")
t("#LIGHT_BLUE# * +0 Magic, +0 Willpower, +5 Cunning", "#LIGHT_BLUE# * +0 魔法，+0 意志，+5 灵巧", "_t")
t("Research. Tinker. Annihilate.", "研究。制造。歼灭。", "_t")

------------------------------------------------

section "tome-orcs/data/birth/races/orc.lua"

t("Skin", "皮肤", "birth facial category")
t("Facial features", "脸部特征", "birth facial category")
t("Tatoos", "纹身", "birth facial category")
t("Horns", "角", "birth facial category")
t("Special", "特殊", "birth facial category")
t("Orc", "兽人", "birth descriptor name")
t("Orcs have a long and sad history. They are seen, and are, as an aggressive race that more than one time managed to imperil all of Maj'Eyal.", "兽人拥有久远而悲伤的历史。他们被视为（也确实如此）一个侵略性种族，曾不止一次危及整个马基埃亚尔世界。", "_t")
t("But one year ago the Scourge from the West came and wiped four of the five Prides. And a hundred years ago King Toknor wiped all traces of orcs from Maj'Eyal.", "但是一年前，来自西方的天灾消灭了五个兽人部落中的四个。一百年前，图库纳国王消灭了马基埃亚尔本土的所有兽人。", "_t")
t("The orc race is dangerously on the brink of destruction. One wrong move is all that is needed.", "兽人种族正危险地处于毁灭边缘。只需走错一步，就足以毁灭。", "_t")
t("But they are strong and will face whatever is needed to ensure a future of their own!", "但他们意志强大，敢于直面任何磨难，来创造属于他们的未来！", "_t")
t("Skin Color 1", "皮肤颜色1", "_t")
t("Skin Color 2", "皮肤颜色2", "_t")
t("Skin Color 3", "皮肤颜色3", "_t")
t("Skin Color 4", "皮肤颜色4", "_t")
t("Skin Color 5", "皮肤颜色5", "_t")
t("Demonic Red Skin", "恶魔红皮肤", "_t")
t("Goggles 1", "护目镜1", "_t")
t("Goggles 2", "护目镜2", "_t")
t("Goggles 3", "护目镜3", "_t")
t("Goggles 4", "护目镜4", "_t")
t("Jaws 1", "下颚1", "_t")
t("Jaws 2", "下颚2", "_t")
t("Mechbiter 1", "机械牙1", "_t")
t("Mechbiter 2", "机械牙2", "_t")
t("Monocle Left 1", "左侧单片眼镜1", "_t")
t("Monocle Left 2", "左侧单片眼镜2", "_t")
t("Monocle Right 1", "右侧单片眼镜1", "_t")
t("Monocle Right 2", "右侧单片眼镜2", "_t")
t("Tatoos 1", "纹身1", "_t")
t("Tatoos 2", "纹身2", "_t")
t("Tatoos 3", "纹身3", "_t")
t("Demonic Horns 1", "恶魔角1", "_t")
t("Demonic Horns 2", "恶魔角2", "_t")
t("Demonic Horns 3", "恶魔角3", "_t")
t("Demonic Horns 4", "恶魔角4", "_t")
t("Demonic Horns 5", "恶魔角5", "_t")
t("Demonic Horns 6", "恶魔角6", "_t")
t("Demonic Horns 7", "恶魔角7", "_t")
t("Demonic Horns 8", "恶魔角8", "_t")
t("Bikini / Mankini", "比基尼/男性比基尼", "_t")
t("They possess the #GOLD#Orcish Fury#WHITE# which allows them to increase all their damage for a few turns.", "他们拥有 #GOLD#兽人之怒#WHITE#，让他们能在几回合内增加伤害。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +2 Strength, +1 Dexterity, +1 Constitution", "#LIGHT_BLUE# * +2 力量，+1 敏捷，+1 体质", "_t")
t("#LIGHT_BLUE# * -1 Magic, +1 Willpower, +1 Cunning", "#LIGHT_BLUE# * -1 魔法，+1 意志，+1 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# 12", "#GOLD#每等级生命加值：#LIGHT_BLUE# 12", "_t")
t("#GOLD#Experience penalty:#LIGHT_BLUE# 12%", "#GOLD#经验惩罚：#LIGHT_BLUE# 12%", "_t")

------------------------------------------------

section "tome-orcs/data/birth/races/whitehooves.lua"

t("Skin", "皮肤", "birth facial category")
t("Facial features", "脸部特征", "birth facial category")
t("Horns", "角", "birth facial category")
t("Special", "特殊", "birth facial category")
t("Undead", "不死族", "_t")
t("Grave strength, dread will, this flesh cannot stay still. Kings die, masters fall, we will outlast them all.", "死亡的力量，恐惧的意志，这些肉体不会沉寂。国王去世，主人陨落，我们才是永生。", "_t")
t("Undead are humanoids (Humans, Elves, Dwarves, ...) that have been brought back to life by the corruption of dark magics.", "不死族是被黑暗魔法复活的人形生物（人类，精灵，矮人…）。", "_t")
t("Undead can take many forms, from ghouls to vampires and liches.", "不死族有多种形态，从食尸鬼、吸血鬼到巫妖。", "_t")
t("Skin Color 1", "皮肤颜色1", "_t")
t("Skin Color 2", "皮肤颜色2", "_t")
t("Skin Color 3", "皮肤颜色3", "_t")
t("Skin Color 4", "皮肤颜色4", "_t")
t("Skin Color 5", "皮肤颜色5", "_t")
t("Skin Color 6", "皮肤颜色6", "_t")
t("Skin Color 7", "皮肤颜色7", "_t")
t("Demonic Red Skin", "恶魔红皮肤", "_t")
t("Beard 1", "络腮胡1", "_t")
t("Beard 2", "络腮胡2", "_t")
t("Redhead Beard", "红色络腮胡", "_t")
t("Hair 1", "发型1", "_t")
t("Hair 2", "发型2", "_t")
t("Hair 3", "发型3", "_t")
t("Hair 4", "发型4", "_t")
t("Redhead Hair 1", "红发1", "_t")
t("Redhead Hair 2", "红发2", "_t")
t("Horns 1", "长角1", "_t")
t("Horns 2", "长角2", "_t")
t("Horns 3", "长角3", "_t")
t("Horns 4", "长角4", "_t")
t("Demonic Horns 1", "恶魔角1", "_t")
t("Demonic Horns 2", "恶魔角2", "_t")
t("Demonic Horns 3", "恶魔角3", "_t")
t("Demonic Horns 4", "恶魔角4", "_t")
t("Demonic Horns 5", "恶魔角5", "_t")
t("Demonic Horns 6", "恶魔角6", "_t")
t("Demonic Horns 7", "恶魔角7", "_t")
t("Demonic Horns 8", "恶魔角8", "_t")
t("Bikini / Mankini", "比基尼/男性比基尼", "_t")
t("Whitehoof", "白蹄", "birth descriptor name")
t("A clan of minotaurs turned to necromancy when faced with imminent destruction.", "一支米诺陶氏族在灭亡迫近时转而研究死灵法术。", "_t")
t("Whitehooves are resilient and magic imbued undead, hardened by their trials and made stronger by their undeath.", "白蹄族是强韧而充满魔法力量的亡灵，在磨砺中变得坚韧，因不死而更加强大。", "_t")
t("They now seek to help their orc allies, in hope they will help them back.", "他们现在试图帮助兽人盟友，希望兽人将来也能回报他们。", "_t")
t("They have access to #GOLD#special talents#WHITE# and a wide range of undead abilities:", "他们拥有 #GOLD# 特殊天赋#WHITE# 和一系列不死族能力：", "_t")
t("- silence resistance", "- 沉默抗性", "_t")
t("- bleeding immunity", "- 流血免疫", "_t")
t("- fear immunity", "- 恐惧免疫", "_t")
t("- no need to breathe", "- 不需要呼吸", "_t")
t("- special whitehoof talents: dead hide, lifeless rush, essence drain", "- 特殊白蹄天赋：亡者之皮，无生突袭，吸取精华。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +3 Strength, -1 Dexterity, +2 Constitution", "#LIGHT_BLUE# * +3 力量，-1 敏捷，+2 体质", "_t")
t("#LIGHT_BLUE# * +2 Magic, -3 Willpower, +1 Cunning", "#LIGHT_BLUE# * +2 魔法，-3 意志，+1 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# 14", "#GOLD#每等级生命加值：#LIGHT_BLUE# 14", "_t")
t("#GOLD#Experience penalty:#LIGHT_BLUE# 15%", "#GOLD#经验惩罚：#LIGHT_BLUE# 15%", "_t")

------------------------------------------------

section "tome-orcs/data/birth/races/yeti.lua"

t("Skin", "皮肤", "birth facial category")
t("Hairs", "发型", "birth facial category")
t("Facial features", "脸部特征", "birth facial category")
t("Horns", "角", "birth facial category")
t("Special", "特殊", "birth facial category")
t("Yeti", "雪人", "birth descriptor name")
t("Infuse the mind, sacrifice the body but the Pride remains.", "强化心智，牺牲肉体，但部落犹存。", "_t")
t("Yetis are a towering mass of muscle.", "雪人族具有强大的肉体。", "_t")
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
t("Hair 1", "发型1", "_t")
t("Hair 2", "发型2", "_t")
t("Beard 1", "络腮胡1", "_t")
t("Beard 2", "络腮胡2", "_t")
t("Beard 3", "络腮胡3", "_t")
t("Eyebrows", "眉毛", "_t")
t("Fangs", "尖牙", "_t")
t("Mustache", "八字胡", "_t")
t("Demonic Horns 1", "恶魔角1", "_t")
t("Demonic Horns 2", "恶魔角2", "_t")
t("Demonic Horns 3", "恶魔角3", "_t")
t("Demonic Horns 4", "恶魔角4", "_t")
t("Demonic Horns 5", "恶魔角5", "_t")
t("Demonic Horns 6", "恶魔角6", "_t")
t("Demonic Horns 7", "恶魔角7", "_t")
t("Demonic Horns 8", "恶魔角8", "_t")
t("Bikini / Mankini", "比基尼/男性比基尼", "_t")
t("Kruk Yeti", "克鲁克雪人", "birth descriptor name")
t("Yetis are a towering mass of muscle. While normal yetis are non-sentient beasts this kind is special.", "雪人族具有强大的肉体。通常，他们只是无知觉的野兽，但这种有所不同。", "_t")
t("A few orcs of the Kruk pride have mastered techno-psionics, allowing them to literally hijack a yeti's mind and transfer their own mind inside.", "少数克鲁克部落的兽人掌握了灵能，让他们能操控雪人族的思维，并用自己的意志取代。", "_t")
t("Doing so drains their old knowledge and they need to start afresh, gaining considerable strength in the process; for the good of the Prides.", "这样做会耗尽他们旧有的知识，必须重新开始，但在此过程中能获得强大的力量；这一切都是为了部落的利益。", "_t")
t("They possess the #GOLD#Algid Rage#WHITE# talent which allows them to encase their foes in blocks of ice.", "他们拥有 #GOLD#寒冰之怒#WHITE#技能，让他们能将敌人封在冰块中。", "_t")
t("#GOLD#Stat modifiers:", "#GOLD#属性修正：", "_t")
t("#LIGHT_BLUE# * +5 Strength, -3 Dexterity, +4 Constitution", "#LIGHT_BLUE# * +5 力量，-3 敏捷，+4 体质", "_t")
t("#LIGHT_BLUE# * +0 Magic, +1 Willpower, -1 Cunning", "#LIGHT_BLUE# * +0 魔法，+1 意志，-1 灵巧", "_t")
t("#GOLD#Life per level:#LIGHT_BLUE# 13", "#GOLD#每等级生命加值：#LIGHT_BLUE# 13", "_t")
t("#GOLD#Experience penalty:#LIGHT_BLUE# 12%", "#GOLD#经验惩罚：#LIGHT_BLUE# 12%", "_t")

------------------------------------------------

section "tome-orcs/data/chats/aaf.lua"

t([[#LIGHT_GREEN#*Before you stands a strange triangular device, some kind of automated facility.*#WHITE#
It seems to be able to teach you the tinker crafting techniques, but requires input to do so (500 gold and a talent category point).]], [[#LIGHT_GREEN#*你面前有一个奇怪的三角形设备，似乎是某种自动设施。*#WHITE#
	似乎它能教授你制造配件的技巧，但需要你一些投入（500金币+一点大系点）。]], "_t")
t("[pay 500 gold and a talent category points]", "[支付500金币和一点大系点]", "_t")
t("#PURPLE#The %s teaches you: #GOLD#Steamtech/Physics#LAST#, #GOLD#Steamtech/Chemistry#LAST# and two starter crafting talents.", "#PURPLE#%s教会你：#GOLD#蒸汽科技/物理#LAST#, #GOLD#蒸汽科技/化学#LAST#和两项入门制造技能。", "log")
t("[access store]", "[进入商店]", "_t")
t("[leave]", "[离开]", "_t")
t([[The machine gives you a small metallic box labelled as #{italic}#"Automated Portable Extractor"#{normal}#.
It seems to be used to break down metallic items into lumps of metal and infusions into herbs which are used to craft tinkers.

#{bold}#You will have to choose to use it or the Transmogrification Chest when you destroy items. You can choose the default one by using it with no items to destroy.#{normal}#
]], [[机械交给你一个小金属盒，上面写着 #{italic}#"便携式自动提取仪"#{normal}#。
它似乎能将金属物品转化为铁块，将纹身转化为植物。

#{bold}#你可以选择使用它或者转化之盒。在里面没有物品时使用它则设置为默认使用。#{normal}#
]], "_t")
t("[take it]", "[拿走]", "_t")

------------------------------------------------

section "tome-orcs/data/chats/destructicus-lead.lua"

t([[#LIGHT_GREEN#*Several loyal Orcs are eagerly waiting outside the palace to meet you; one steps forward, handing you a set of keys.  The word 'DESTRUCTICUS' is etched into one.*#WHITE#
Chief @playername@!  The Giants are fleeing, and we intercepted a scout carrying this!  We believe they can be used with...  well, you should see for yourself!  Please, come with us to the mountains just south of Kruk Pride!
#LIGHT_GREEN#*This sounds important.  You should probably head there right away!*#WHITE#]], [[#LIGHT_GREEN#*数名忠诚的兽人在宫殿外焦急地等待着你；其中一名兽人走上前，交给你一串钥匙，上面写着“毁灭号”。*#WHITE#
@playername@首领！巨人们在逃跑，我们抓住了一名侦查兵，他身上带着这个！我们认为它是用于……算了，您应该亲自来看看！请跟我们来克鲁克部落南边的山脉！
#LIGHT_GREEN#*这听起来非常重要，你应该马上过去*#WHITE#]], "_t")
t("Lead the way.", "带路吧。", "_t")

------------------------------------------------

section "tome-orcs/data/chats/destructicus.lua"

t("DESTRUCTICUS!", "“毁灭号！”", "_t")
t("Fire Imp", "火焰小鬼", "_t")
t("Steam Giant Airship", "蒸汽巨人飞船", "_t")
t("#LIGHT_GREEN#*#{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}# stands before you, and as much as it pains you to admit it, Kaltor's advertisement wasn't flattering enough.  This may be the most unreasonably lethal device you've ever seen.  The sunlight, gleaming off its voratun body, seems dull compared to the intensely glowing mass of unstable runes on its tip; its surface has the ornate grooves of a metal that has been psionically reforged through hours of migraine-inducing concentration.  The bayonet mounted on the launching tube just seems like gloating.  This particular model appears to be equipped with an enclosed, fireproof booth around its control panel, and a built-in tea dispenser in said booth, which your fellow orcs have already taken the liberty of filling with looted Dwarven ale.  It is truly a thing of beauty.*#WHITE#", "#LIGHT_GREEN#*#{bold}#裂天者 毁灭号#{normal}# 站在你面前，让你痛苦地承认，卡托尔的广告还远不够夸耀。这可能是你见过的最无端致命的设备。阳光照耀在它的沃瑞钽躯壳上，与它尖端那团散发着炽烈光芒的不稳定符文相比显得黯淡；它的表面有着华丽的沟槽，那是经过数小时令人头痛欲裂的专注心灵锻造重塑的金属。发射管上安装的刺刀仿佛在炫耀一般。这个型号似乎还配备了一个密封防火的控制舱，舱内有一台内置的茶饮机，你的兽人同胞们已经擅自往里面灌满了抢来的矮人麦酒。这真是一件美得惊人的造物。*#WHITE#", "_t")
t("[continue]", "[继续]", "_t")
t("#LIGHT_GREEN#*You enter the booth, sit down, and insert the key.  #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}# whirrs to life, its base slightly rotating underneath you.  A strange beaded panel slides in front of you, pins pushing out and pulling back by magnetic force to display the outline of an airship (and a tiny speck), and the words #{italic}#\"AERIAL TARGETS FOUND: 2.\"#{normal}#*#WHITE#", "#LIGHT_GREEN#*你进入了操作室，坐好，插入钥匙。#{bold}#裂天者 毁灭号#{normal}# 启动了它的生命，它的基座开始运转。一块奇怪的珍珠板从你前方滑过，针伸了出来，被电磁力量控制，显示出飞船的轮廓（以及一个小黑点）与以下短语：#{italic}#“发现空中目标-数目：2”。#{normal}#*#WHITE#", "_t")
t([[#LIGHT_GREEN#*#{italic}#"OBTAINING SCRYING LOCK...  OBTAINED."#{normal}#
 
The beaded panel is suddenly awash with colors, showing the colossal interior of the airship.  Steam Giant families huddle and weep, sorting through the few belongings they could take with them when fleeing; a guard sits on a pile of luggage and storage crates, head in her hands.  The view pans around the cabin, and you see a few crew members hurrying between the captain's quarters and the engine room, pausing to take worried glances out the window - at you.
 
This airship appears to be evacuating what's left of the Atmos Tribe.  With the press of a single button, you could eradicate the Steam Giant species forever.
 
You press a button labelled #{italic}#"SELECT NEXT TARGET"#{normal}#, and the panel shifts to show a very lost and very confused Fire Imp, flying in the air near nothing of importance.  Firing on it would have little effect whatsoever, aside from showing off DESTRUCTICUS's power in the most harmless way possible.*#WHITE#]], [[#LIGHT_GREEN#*#{italic}#"获取侦测锁定中……已获取。"#{normal}#

珍珠面板突然充满色彩，显示飞船的巨大内部结构。蒸汽巨人们拥挤而哭泣，整理着逃离时仅能带走的少量财物；一名守卫双手抱头，坐在一堆行李和储物箱上。视角切换到船舱，你看见一些成员匆忙走过船长室和引擎室，偶尔忧虑地瞥向窗外——看向你。
飞船似乎正在疏散气之部族的残余成员。只要按下一个按钮，你将能永久摧毁蒸汽巨人这个种族。

你按下按钮 #{italic}#"选择下个目标"#{normal}#，面板显示出一个迷茫而混乱的火焰小鬼，在空中无害地飞舞。向他开火没什么意义，只是以最无害的方式炫耀毁灭号的力量。*#WHITE#]], "_t")
t("[shoot down the airship]", "[击落飞船]", "_t")
t("[shoot down the imp]", "[击落小鬼]", "_t")
t("#LIGHT_GREEN#*Are you SURE you want to ERADICATE THE STEAM GIANTS?*#WHITE#", "#LIGHT_GREEN#*你确认要消灭蒸汽巨人么？*#WHITE#", "_t")
t("[back]", "[返回]", "_t")
t("#LIGHT_GREEN#*Are you SURE you want to WASTE YOUR SHOT?*#WHITE#", "#LIGHT_GREEN#*你确认要浪费子弹么？*#WHITE#", "_t")
t([[#LIGHT_GREEN#*The Steam Giants are too great a threat to allow their escape - you will not have them simply return someday to finish what they attempted, and wipe out your Pride.  You press the #{italic}#"PREVIOUS TARGET"#{normal}# button, and fire on the airship.  There is a great roar and a flash of flame; you see its missile flying away from you through the window, as you see it racing towards your view, and the terrified passengers, on the scrying panel.

It reaches its mark, and the panel goes dark as a tremendous, multicolored blast fills your vision through the window.
 
The Steam Giants are no more.
 
The secondary charges from the warhead detonate, as burning debris falls into the sea, and the ongoing display serves as a signal to all the Orcs of Var'Eyal, and anyone else who may be watching: This is the fate of all who would try to eradicate the Orcs.  The previous millennia of oppression, genocide, and bullying are over: your people will never be pushed around like this again.
 
A nagging thought in the back of your head insists that you now know how the Sun Paladins felt, how King Toknor felt, how the halflings felt, how everyone that has always committed such atrocities against the Orcs felt.  It can keep whining all it wants - your people are finally safe.*#WHITE#]], [[#LIGHT_GREEN#*让蒸汽巨人们逃离太过危险 - 你不能允许他们这样简单的离开，然后将来某日再实现其图谋，消灭你的部落。你按下#{italic}#"上一名目标"#{normal}# 按钮，朝飞船开火。一阵巨大的轰鸣声和一道强烈的火光闪过，你从窗户里看见导弹朝目标飞去，飞向你视线远处，拥挤的飞船里惊恐的乘客那边。

导弹到达了目的地，巨大的爆炸堵塞了你透过窗户的视线，面板随之变暗。

蒸汽巨人消失了。

弹头的次级装药引爆，燃烧的残骸坠入大海，这场持续的烟火盛宴成为大陆上所有兽人，甚至所有能看到这一盛景的生物的信号：
这就是所有试图消灭兽人的种族的命运。千年的压制、欺凌和屠杀被终结了：你的人民再也不会沦落如斯。

无法摆脱的念头自你脑后升腾，你现在明白了太阳骑士的感受，明白了图库纳国王的感受，明白了半身人的感受，明白了所有曾对兽人施以暴行的人的感受。
随它哀诉去吧————但你的人民终于安全了。*#WHITE#]], "_t")
t("[leave]", "[离开]", "_t")
t([[#LIGHT_GREEN#*No...  you will not sink to the depths that King Toknor did, that the Sun Paladins did, that so many others have sunk to.  These refugees are not a threat, and could not possibly become one for quite some time...  but it might be for the best that they're made fully aware of what you're capable of, the fate you could've given them through so little effort, and given a display that'll make sure they remember that they owe their lives to your mercy.
 
You target the Fire Imp, and fire the weapon.  With a great roar and a flash of flame, #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}# races towards the increasingly distressed imp.  It panics, flitting to the side evasively as #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}# corrects its course to compensate, until it gives up and shrugs dejectedly; you can't hear the scrying panel over the missile's roaring, but you're fairly sure you can see the imp mouthing "this is 'blazing ridiculous."
 
It impacts, and your vision is filled with an enormous, multicolored explosion.  Shrapnel and debris falls harmlessly into a barren mountaintop, and a great booming noise can be heard across the continent.  
 
Taking a swig from a freshly-dispensed mug of ale, you switch the now-empty #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}#'s targeting controls over to the airship, and you see the giants cheering and hugging, crying in joy and relief.  A few wonder aloud if you meant to do that, but most recognize it as the display of mercy that it is.
 
As the secondary charges go off, the ongoing pyrotechnic display acts as a celebratory signal to the Steam Giants, the Orcs, and anyone else who may be watching: The war is over.  Var'Eyal, and the Orcs who now own it, will know peace for the first time in millennia.*#WHITE#]], [[#LIGHT_GREEN#*不……你不会让自己踏入那无尽的深渊，踏入那图库纳国王、太阳骑士和所有其他人都曾陷入的深渊中。

这些难民不再是威胁，很长时间内都不可能成为威胁……但最好能让他们充分意识到你的力量，你本能轻易带来的毁灭命运，向他们展示这一切，让他们永远铭记：他们的生死取决于你的仁慈。

你瞄准了火焰小鬼，令武器开火。巨大的轰鸣声和火光闪过，#{bold}#裂天者 毁灭号#{normal}#朝那只越来越惊慌的小鬼冲过去。它惊恐无比，试图躲避，而#{bold}#裂天者 毁灭号#{normal}#相对修正了行进路线，直到它彻底放弃，沮丧地耸了耸肩。在导弹的轰鸣声中，你听不见侦测面板的声音，不过你能肯定那只小鬼的嘴型在说“这简直荒谬透顶”。

导弹到达了目的地，巨大的爆炸堵塞了你透过窗户的视线。碎片无害地坠落在山顶，整个大陆都听见了巨大的爆鸣声。

痛饮刚分下来的美酒，你将已经空膛的#{bold}#裂天者 毁灭号#{normal}#指向飞船，不出所料看见巨人们欢呼拥抱，喜极而泣。少数大声质疑你为什么这么做，而大部分人明白这是仁慈的表示。

当次级装药引爆时，这场持续的烟火盛宴成为大陆上所有蒸汽巨人，所有兽人，甚至所有能看到这一盛景的生物的庆典：
战争结束了。
千年以来，瓦·埃亚尔，以及拥有它的兽人们，第一次明白了和平的意义。*#WHITE#]], "_t")

------------------------------------------------
