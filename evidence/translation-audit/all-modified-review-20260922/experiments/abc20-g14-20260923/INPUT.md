# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03693–entry-03732 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g14-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03693 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03693
位置：tome-cults.lua:4790；section：tome-cults/overload/mod/class/CultsDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#CRIMSON#[The parasite is hungry and promptly swallows and eat Melinda].
```
译文：
```text
#CRIMSON#[寄生兽很饿，吃下了梅琳达]。
```

## entry-03694
位置：tome-cults.lua:4791；section：tome-cults/overload/mod/class/CultsDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#CRIMSON#[The parasite is hungry and promptly swallows and eat Aeryn].
```
译文：
```text
#CRIMSON#[寄生兽很饿，吃下了艾琳]。
```

## entry-03695
位置：tome-cults.lua:4792；section：tome-cults/overload/mod/class/CultsDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#CRIMSON#[The parasite is hungry and attacks Slasul].
```
译文：
```text
#CRIMSON#[寄生兽很饿，攻击了萨拉苏尔]。
```

## entry-03696
位置：tome-cults.lua:4865；section：tome-cults/overload/mod/dialogs/FontSacrifice.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (Greater)
```
译文：
```text
 （高级词缀）
```

## entry-03697
位置：tome-cults.lua:4934；section：tome-cults/superload/mod/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
As you enter Last Hope a courier finds you to deliver a letter from Protector Myssil of Zigur:

%s, while you were away destroying arcane filth I have received grave news.
A group of Krogs has been ambushed and taken to a hidden ruin on the eastern shores of the sea of Sash near Zigur.
From what the scouts can tell they were taken by a group of necromancers, probably to do vile experiments on them.

All our other elite fighting forces are currently abroad, you are their only hope.
Please, go there at once, free them and show the necromancers filth the True Wrath of the Ziguranth!

#{italic}#Protector Myssil#{normal}#

```
译文：
```text
当你进入最后的希望时，一个信使找到你并给你一份来自守护者米歇尔的信：

%s，当你在外面打击肮脏的奥术势力时，我收到了一个令人震惊的消息。
一群克罗格遭到伏击并被带到伊格附近的萨希海东海岸隐藏的废墟中。
侦察员看见他们被一群死灵法师带走，可能会对他们进行邪恶的实验。

我们其他所有的精英部队都在外面，你是他们唯一的希望。
请立刻去那里解救他们，并让死灵法师见识一下伊格兰斯的愤怒！

#{italic}#守护者米歇尔#{normal}#

```

## entry-03698
位置：tome-items-vault.lua:53；section：tome-items-vault/overload/data/chats/items-vault-command-orb.lua；source_tag：_t；args_order：None；special：None

原文：
```text

#CRIMSON#Note for Steam Players#ANCIENT_WHITE#: This feature requires you to have registered a profile & bound it to steam (automatic if you register ingame) because it needs to store things on the server.
Until you do so you will get an error.
```
译文：
```text

#CRIMSON#对Steam玩家的提醒#ANCIENT_WHITE#: 因为这项功能需要你在服务器上存储数据，使用共享仓库需要你注册了游戏账户，并将其绑定到Steam（如果你在游戏内注册，这个过程将会自动完成）。
否则，你将会遇到一个错误。
```

## entry-03699
位置：tome-items-vault.lua:78；section：tome-items-vault/overload/mod/class/ItemsVaultDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text

#CRIMSON#This item has been sent to the Item's Vault.
```
译文：
```text

#CRIMSON#这个物品已被上传到共享仓库。
```

## entry-03700
位置：tome-items-vault.lua:85；section：tome-items-vault/overload/mod/class/ItemsVaultDLC.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#Error while transfering %s to the online item's vault, please retry later.
```
译文：
```text
#LIGHT_RED#将物品%s传输到在线共享仓库时发生错误，请稍后再试。
```

## entry-03701
位置：tome-items-vault.lua:87；section：tome-items-vault/overload/mod/class/ItemsVaultDLC.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#You transfer %s to the offline item's vault.
```
译文：
```text
#LIGHT_BLUE#你将%s传输到离线共享仓库。
```

## entry-03702
位置：tome-items-vault.lua:111；section：tome-items-vault/overload/mod/dialogs/ItemsVault.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This item has been placed recently in the vault, you must wait a bit before removing it.
```
译文：
```text
该物品刚刚被放入共享仓库，你需要等待一段时间才能将其移除。
```

## entry-03703
位置：tome-items-vault.lua:130；section：tome-items-vault/overload/mod/dialogs/ItemsVaultOffline.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This item has been placed recently in the vault, you must wait a bit before removing it.
```
译文：
```text
该物品刚刚被放入共享仓库，你需要等待一段时间才能将其移除。
```

## entry-03704
位置：tome-orcs.lua:34；section：tome-orcs/data/achievements/special.lua；source_tag：achievement name；args_order：None；special：None

原文：
```text
Once Upon A Time, In the West...
```
译文：
```text
很久很久以前，在西方……
```

## entry-03705
位置：tome-orcs.lua:43；section：tome-orcs/data/achievements/special.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Wield the Annihilator as an Annihilator.
```
译文：
```text
作为歼灭者（职业），装备歼灭者（武器）。
```

## entry-03706
位置：tome-orcs.lua:57；section：tome-orcs/data/achievements/story.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You have defeated the Sher'tul Priest trying to resurrect Amakthel, saving both the Prides and the world.
```
译文：
```text
你消灭了试图复活阿马克泰尔的夏·图尔牧师，拯救了部落和世界。
```

## entry-03707
位置：tome-orcs.lua:70；section：tome-orcs/data/birth/classes/empyreal.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +6 Magic, +0 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * +6 魔法，+0 意志，+0 灵巧
```

## entry-03708
位置：tome-orcs.lua:71；section：tome-orcs/data/birth/classes/empyreal.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# +0
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# +0
```

## entry-03709
位置：tome-orcs.lua:88；section：tome-orcs/data/birth/classes/tinker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 2
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 2
```

## entry-03710
位置：tome-orcs.lua:92；section：tome-orcs/data/birth/classes/tinker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +0 Strength, +4 Dexterity, +1 Constitution
```
译文：
```text
#LIGHT_BLUE# * +0 力量，+4 敏捷，+1 体质
```

## entry-03711
位置：tome-orcs.lua:93；section：tome-orcs/data/birth/classes/tinker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +0 Magic, +0 Willpower, +4 Cunning
```
译文：
```text
#LIGHT_BLUE# * +0 魔法，+0 意志，+4 灵巧
```

## entry-03712
位置：tome-orcs.lua:94；section：tome-orcs/data/birth/classes/tinker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# -1
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# -1
```

## entry-03713
位置：tome-orcs.lua:101；section：tome-orcs/data/birth/classes/tinker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +0 Magic, +3 Willpower, +3 Cunning
```
译文：
```text
#LIGHT_BLUE# * +0 魔法，+3 意志，+3 灵巧
```

## entry-03714
位置：tome-orcs.lua:153；section：tome-orcs/data/birth/races/orc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
They possess the #GOLD#Orcish Fury#WHITE# which allows them to increase all their damage for a few turns.
```
译文：
```text
他们拥有 #GOLD#兽人之怒#WHITE#，让他们能在几回合内增加伤害。
```

## entry-03715
位置：tome-orcs.lua:155；section：tome-orcs/data/birth/races/orc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +2 Strength, +1 Dexterity, +1 Constitution
```
译文：
```text
#LIGHT_BLUE# * +2 力量，+1 敏捷，+1 体质
```

## entry-03716
位置：tome-orcs.lua:156；section：tome-orcs/data/birth/races/orc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * -1 Magic, +1 Willpower, +1 Cunning
```
译文：
```text
#LIGHT_BLUE# * -1 魔法，+1 意志，+1 灵巧
```

## entry-03717
位置：tome-orcs.lua:157；section：tome-orcs/data/birth/races/orc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 12
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 12
```

## entry-03718
位置：tome-orcs.lua:158；section：tome-orcs/data/birth/races/orc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Experience penalty:#LIGHT_BLUE# 12%
```
译文：
```text
#GOLD#经验惩罚：#LIGHT_BLUE# 12%
```

## entry-03719
位置：tome-orcs.lua:210；section：tome-orcs/data/birth/races/whitehooves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
- special whitehoof talents: dead hide, lifeless rush, essence drain
```
译文：
```text
- 特殊白蹄天赋：亡者之皮，无生突袭，吸取精华。
```

## entry-03720
位置：tome-orcs.lua:212；section：tome-orcs/data/birth/races/whitehooves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, -1 Dexterity, +2 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，-1 敏捷，+2 体质
```

## entry-03721
位置：tome-orcs.lua:213；section：tome-orcs/data/birth/races/whitehooves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +2 Magic, -3 Willpower, +1 Cunning
```
译文：
```text
#LIGHT_BLUE# * +2 魔法，-3 意志，+1 灵巧
```

## entry-03722
位置：tome-orcs.lua:214；section：tome-orcs/data/birth/races/whitehooves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 14
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 14
```

## entry-03723
位置：tome-orcs.lua:215；section：tome-orcs/data/birth/races/whitehooves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Experience penalty:#LIGHT_BLUE# 15%
```
译文：
```text
#GOLD#经验惩罚：#LIGHT_BLUE# 15%
```

## entry-03724
位置：tome-orcs.lua:261；section：tome-orcs/data/birth/races/yeti.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +5 Strength, -3 Dexterity, +4 Constitution
```
译文：
```text
#LIGHT_BLUE# * +5 力量，-3 敏捷，+4 体质
```

## entry-03725
位置：tome-orcs.lua:262；section：tome-orcs/data/birth/races/yeti.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +0 Magic, +1 Willpower, -1 Cunning
```
译文：
```text
#LIGHT_BLUE# * +0 魔法，+1 意志，-1 灵巧
```

## entry-03726
位置：tome-orcs.lua:263；section：tome-orcs/data/birth/races/yeti.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 13
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 13
```

## entry-03727
位置：tome-orcs.lua:264；section：tome-orcs/data/birth/races/yeti.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Experience penalty:#LIGHT_BLUE# 12%
```
译文：
```text
#GOLD#经验惩罚：#LIGHT_BLUE# 12%
```

## entry-03728
位置：tome-orcs.lua:300；section：tome-orcs/data/chats/aaf.lua；source_tag：log；args_order：None；special：None

原文：
```text
#PURPLE#The %s teaches you: #GOLD#Steamtech/Physics#LAST#, #GOLD#Steamtech/Chemistry#LAST# and two starter crafting talents.
```
译文：
```text
#PURPLE#%s教会你：#GOLD#蒸汽科技/物理#LAST#, #GOLD#蒸汽科技/化学#LAST#和两项入门制造技能。
```

## entry-03729
位置：tome-orcs.lua:303；section：tome-orcs/data/chats/aaf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The machine gives you a small metallic box labelled as #{italic}#"Automated Portable Extractor"#{normal}#.
It seems to be used to break down metallic items into lumps of metal and infusions into herbs which are used to craft tinkers.

#{bold}#You will have to choose to use it or the Transmogrification Chest when you destroy items. You can choose the default one by using it with no items to destroy.#{normal}#

```
译文：
```text
机械交给你一个小金属盒，上面写着 #{italic}#"便携式自动提取仪"#{normal}#。
它似乎能将金属物品转化为铁块，将纹身转化为植物。

#{bold}#你可以选择使用它或者转化之盒。在里面没有物品时使用它则设置为默认使用。#{normal}#

```

## entry-03730
位置：tome-orcs.lua:317；section：tome-orcs/data/chats/destructicus-lead.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*Several loyal Orcs are eagerly waiting outside the palace to meet you; one steps forward, handing you a set of keys.  The word 'DESTRUCTICUS' is etched into one.*#WHITE#
Chief @playername@!  The Giants are fleeing, and we intercepted a scout carrying this!  We believe they can be used with...  well, you should see for yourself!  Please, come with us to the mountains just south of Kruk Pride!
#LIGHT_GREEN#*This sounds important.  You should probably head there right away!*#WHITE#
```
译文：
```text
#LIGHT_GREEN#*数名忠诚的兽人在宫殿外焦急地等待着你；其中一名兽人走上前，交给你一串钥匙，上面写着“毁灭号”。*#WHITE#
@playername@首领！巨人们在逃跑，我们抓住了一名侦查兵，他身上带着这个！我们认为它是用于……算了，您应该亲自来看看！请跟我们来克鲁克部落南边的山脉！
#LIGHT_GREEN#*这听起来非常重要，你应该马上过去*#WHITE#
```

## entry-03731
位置：tome-orcs.lua:332；section：tome-orcs/data/chats/destructicus.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*You enter the booth, sit down, and insert the key.  #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}# whirrs to life, its base slightly rotating underneath you.  A strange beaded panel slides in front of you, pins pushing out and pulling back by magnetic force to display the outline of an airship (and a tiny speck), and the words #{italic}#"AERIAL TARGETS FOUND: 2."#{normal}#*#WHITE#
```
译文：
```text
#LIGHT_GREEN#*你进入了操作室，坐好，插入钥匙。#{bold}#裂天者 毁灭号#{normal}# 启动了它的生命，它的基座开始运转。一块奇怪的珍珠板从你前方滑过，针伸了出来，被电磁力量控制，显示出飞船的轮廓（以及一个小黑点）与以下短语：#{italic}#“发现空中目标-数目：2”。#{normal}#*#WHITE#
```

## entry-03732
位置：tome-orcs.lua:333；section：tome-orcs/data/chats/destructicus.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*#{italic}#"OBTAINING SCRYING LOCK...  OBTAINED."#{normal}#
 
The beaded panel is suddenly awash with colors, showing the colossal interior of the airship.  Steam Giant families huddle and weep, sorting through the few belongings they could take with them when fleeing; a guard sits on a pile of luggage and storage crates, head in her hands.  The view pans around the cabin, and you see a few crew members hurrying between the captain's quarters and the engine room, pausing to take worried glances out the window - at you.
 
This airship appears to be evacuating what's left of the Atmos Tribe.  With the press of a single button, you could eradicate the Steam Giant species forever.
 
You press a button labelled #{italic}#"SELECT NEXT TARGET"#{normal}#, and the panel shifts to show a very lost and very confused Fire Imp, flying in the air near nothing of importance.  Firing on it would have little effect whatsoever, aside from showing off DESTRUCTICUS's power in the most harmless way possible.*#WHITE#
```
译文：
```text
#LIGHT_GREEN#*#{italic}#"获取侦测锁定中……已获取。"#{normal}#

珍珠面板突然充满色彩，显示飞船的巨大内部结构。蒸汽巨人们拥挤而哭泣，整理着逃离时仅能带走的少量财物；一名守卫双手抱头，坐在一堆行李和储物箱上。视角切换到船舱，你看见一些成员匆忙走过船长室和引擎室，偶尔忧虑地瞥向窗外——看向你。
飞船似乎正在疏散气之部族的残余成员。只要按下一个按钮，你将能永久摧毁蒸汽巨人这个种族。

你按下按钮 #{italic}#"选择下个目标"#{normal}#，面板显示出一个迷茫而混乱的火焰小鬼，在空中无害地飞舞。向他开火没什么意义，只是以最无害的方式炫耀毁灭号的力量。*#WHITE#
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Annihilator	歼灭者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	兽人战役职业
Atmos Tribe	气之部族	T.PN.FACTION	society	faction name	preferred	dlc	Embers of Rage 阵营专名；统一为“气之部族”（叙事文本曾作“气之部落”），与气之部族 NPC/叙事一致
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
DESTRUCTICUS	毁灭号	T.GAME.ENTITY	creatures	_t	preferred	dlc	Embers of Rage 武器“裂天者 毁灭号”的简称；欢呼与叙词统一为“毁灭号”，不写作“毁天灭地”
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Krog	克罗格	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Kruk Pride	克鲁克部落	T.PN.FACTION	society	faction name	existing	dlc	Embers of Rage 阵营
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Melinda	梅琳达	T.PN.PERSON	society	entity name	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
Whitehoof	白蹄	T.PN.RACE	creatures	birth descriptor name	existing	dlc	兽人战役种族
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
chemistry	化学	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
krog	克罗格	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
krog	克罗格	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
parasite	寄生	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
physics	物理	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamtech	蒸汽科技	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
