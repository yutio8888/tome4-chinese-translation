# batch-114：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03685
位置：tome-cults.lua:4636；section：tome-cults/overload/data/texts/intro-krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome #LIGHT_GREEN#@name@#WHITE#.

You are a Krog, a former ogre stripped of its runes by the Ziguranth. Ogres cannot live without runes, yet you a Krog have been kept alive by the powers of nature coursing through your body. 

All Krogs are infused with anti-magic forces as a result of the changes made to their bodies by the Ziguranth. While much of Maj'Eyal shuns the arcane, there is still those who practice it, and you would like nothing more then to eradicate them from the world.

You have come to an old ruin named Kor'Pul on a mission to eliminate the foulest of arcane creations: undeads.

```
译文：
```text
欢迎 #LIGHT_GREEN#@name@#WHITE#。

你是一个克罗格。你曾经是一个食人魔，然而你的符文被伊格兰斯取下了。食人魔失去了符文会无法存活，而你这样克罗格却可以通过你身体内的自然力量存活。
作为上面条件的附加作用，克罗格的身体被伊格兰斯的反魔法力量所灌注。虽然大部分马基埃亚尔人都远离奥术魔法，但仍然有一些人在实践奥术魔法，而你的目标就是从世界上消灭他们。
你来到了一个古老的废墟：卡普尔。你的任务是消灭掉奥术魔法最为邪恶的创造：亡灵。

```

## entry-03686
位置：tome-cults.lua:4660；section：tome-cults/overload/data/texts/unlock-demented_cultist_entropy.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Cultist of Entropy (Demented)
```
译文：
```text
新职业 : #LIGHT_GREEN#熵教徒（疯狂系）
```

## entry-03687
位置：tome-cults.lua:4697；section：tome-cults/overload/data/texts/unlock-race_drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Drems are a mutated offshoot of the dwarven race.
Long ago the mysterious machines that seem to be the source of dwarves malfunctioned and started to create all kind of monstrous beings, including Drems.
Something in Kroshkkur seems to try to #{italic}#fix#{normal}# them by making them sentient.

You have learned the origins of Drems and can now create new #LIGHT_GREEN#Drem#WHITE# characters!

Race features:#YELLOW#
- Enter a Frenzy to eliminate cooldown on talents
- Bleed your black blood on your attackers
- Learn to summon a horror!
#WHITE#

```
译文：
```text
德瑞姆是矮人的变异亚种。
在很久以前，那些似乎是矮人源头的神秘机器失灵了，开始创造出各种怪物，包括德瑞姆。
克诺什库尔中的某种东西似乎想要#{italic}#修正#{normal}#他们，给予了他们智慧。

你已经了解了德瑞姆的起源，你现在可以创造新的#LIGHT_GREEN#德瑞姆#WHITE#角色！

种族特色：#YELLOW#
- 进入狂热状态，使技能不进入冷却
- 让黑血溅到攻击你的人身上
- 可以学会召唤一个恐魔！
#WHITE#

```

## entry-03688
位置：tome-cults.lua:4724；section：tome-cults/overload/data/texts/unlock-race_krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Race: #LIGHT_GREEN#Krog
```
译文：
```text
新种族：#LIGHT_GREEN#克罗格
```

## entry-03689
位置：tome-cults.lua:4725；section：tome-cults/overload/data/texts/unlock-race_krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Ogres were created long ago by terrible ways as elite fighters in the allure wars. Imbued from birth with runes their bodies can not survive without the arcane forces powering them.

But while they are magic users Ziguranth took pity on them for they had not chosen their fate, it was forced upon them.
After lots of painful, but required, experiments Zigur was finally able to create an offshoot of the ogre race by replacing their runes and arcane forces with drake blood and nature.
Ever since the Krogs as they are called have been mighty stalwards of nature and staunch protectors of Zigur. Elite fighters capable of dual wielding any one handed weapons to crush all foes of Nature!

You have rescued a group of them from the undead flith can now create new #LIGHT_GREEN#Krog#WHITE# characters!

Race features:#YELLOW#
- Their wrath is so terrible they can stun their foes with any attacks
- Drake infused blood that lets them resist the elements themselves
- A mastery of infusions like no others
- A warborn race, able to dual wield any one handed weapons and survive situations that would kill most others
#WHITE#

```
译文：
```text
食人魔在很久以前的厄流战争中被以恐怖的手段制造出来，作为战争的精英战士。他们从生下来身体就灌注着符文能量，没有这些奥术能量就无法生存。

然而，伊格兰斯同情他们被强迫而无法选择的命运。
在经过无数痛苦但不可避免的实验后，伊格兰斯终于创造出食人魔的一个亚种。他们用龙血和自然之力替代了食人魔体内的符文和奥术力量。
在那之后，被称为克罗格的食人魔们就成为了自然的坚盾和伊格的坚实保护者。这些精英战士能够双持挥舞任何单手武器，摧毁所有自然的敌人

你从不死生物的魔爪中救下了一群克罗格，你现在可以创造新的#LIGHT_GREEN#克罗格#WHITE# 角色！

种族特点：#YELLOW#
- 他们的愤怒如此恐怖，任何攻击都能够震慑对手。
- 他们龙血灌注的身体可以抵抗元素魔法伤害。
- 他们是自然纹身的大师。
- 他们是战斗种族，可以双持任何单手武器，在足以杀死大多数其他生物的处境中依旧保持坚韧。
#WHITE#

```

## entry-03690
位置：tome-cults.lua:4758；section：tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Talent Category: #LIGHT_GREEN#Scourge Drake
```
译文：
```text
新技能树：#LIGHT_GREEN#天谴之龙
```

## entry-03691
位置：tome-cults.lua:4759；section：tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Drakes are forces of Nature, the ultimate apex predators. But even they can be corrupted beyond hope.
You have encountered the horror that came out of Kroltar, the mightiest wyrm, and vanquished it.

You can now master Scourge Drake magic and create new Wyrmic characters that can learn the #LIGHT_GREEN#Scourge Drake talents#WHITE#.

Talents:
- #YELLOW#Tentacled Wings: #WHITE#Project slimy tentacles to pull your foes to you
- #YELLOW#Decaying Grounds: #WHITE#Cover the ground in blighted energies, increasing cooldowns
- #YELLOW#Augment Despair: #WHITE#Hit where it hurts, doing more damage based on detrimental effects
- #YELLOW#Maggot Breath: #WHITE#Breath maggots to slow down your foes

```
译文：
```text
龙是自然力量的化身，是究极的捕食者。然而，就连他们也能够被绝望所腐化。
你遇到了从最强大的巨龙库洛塔身上产生的恐魔，并击败了它。
你现在可以掌握天谴龙的魔法，你创建的新龙战士角色可以使用新的#LIGHT_GREEN#天谴之龙#WHITE#系技能

技能列表：
- #YELLOW#触手之翼：#WHITE# 伸出黏滑的触手，将敌人拉向你
- #YELLOW#腐朽之地：#WHITE# 在地面中灌注枯萎能量，增加技能冷却时间
- #YELLOW#扩大绝望：#WHITE# 击打对手受伤的地方，对方负面效果越多伤害越高。
- #YELLOW#蛆虫吐息：#WHITE# 喷吐蛆虫，让你的敌人减速

```

## entry-03692
位置：tome-cults.lua:4774；section：tome-cults/overload/mod/class/CultsDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your mental insanity.  The higher it is the more random your damage and cooldowns become.

Damage and cooldowns have a chance to increase or decrease by up to chaotic%.

Both the chance and size of effects will increase with insanity.
```
译文：
```text
你的精神的疯狂程度。这一数值越高，你的技能的冷却时间和所造成的伤害随机性就越大。

伤害和冷却时间将会在 混沌度% 的范围内上下浮动。

浮动的几率和浮动的效果都会随疯狂值提升而上升。
```

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

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Annihilator	歼灭者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	兽人战役职业
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cultist of Entropy	熵教徒	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Demented	疯狂系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业类别名
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Drem	德瑞姆	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Frenzy	狂热	T.GAME.TALENT	talents	talent name	existing	global	
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Krog	克罗格	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Melinda	梅琳达	T.PN.PERSON	society	entity name	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
Whitehoof	白蹄	T.PN.RACE	creatures	birth descriptor name	existing	dlc	兽人战役种族
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
demented	疯狂	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
drem	德瑞姆	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
entropy	熵	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
entropy	熵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
frenzy	狂乱	T.GAME.EFFECT	combat	effect subtype	existing	global	与技能名 Frenzy 的译法区分
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
kor'pul	卡·普尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
krog	克罗格	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
krog	克罗格	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
maggot	蛆虫	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
parasite	寄生	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tentacles	触手	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
