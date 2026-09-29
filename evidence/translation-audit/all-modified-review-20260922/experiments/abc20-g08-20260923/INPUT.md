# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03453–entry-03492 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g08-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03453 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03453
位置：tome-ashes-urhrok.lua:1655；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CRIMSON#Your corruption explodes around %s!
```
译文：
```text
#CRIMSON#你的腐化在%s周围爆炸！
```

## entry-03454
位置：tome-ashes-urhrok.lua:1729；section：tome-ashes-urhrok/data/zones/searing-halls/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A demon with 3 arms, ready to mutilate you. For experiment. Not for fun. Nope.
```
译文：
```text
一个长着三只手的恶魔，准备切割你。不是娱乐，而是实验。
```

## entry-03455
位置：tome-ashes-urhrok.lua:1752；section：tome-ashes-urhrok/init.lua；source_tag：init.lua description；args_order：None；special：None

原文：
```text
Many in Maj'Eyal have heard of "demons", sadistic creatures who appear seemingly from nowhere, leaving a trail of suffering and destruction whereever they go.  Their Fearscape floats far above the skies, watching and waiting, but not idly; their agents scout the land, their legions build up their forces, and their scholars develop new spells and strategies.  As the barrier between our worlds begins to crack under their scrutiny, helpless Eyalites have begun to disappear, whisked up to serve as their slaves and playthings.  They imbue these victims with magical powers to better survive the ensuing stresses - can you use your new-found abilities to escape the legions of Mal'Rok?

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

```
译文：
```text
在马基埃亚尔，很多人都曾听闻“恶魔”的大名，作为仿佛凭空出现的暴虐生物，他们无论走到哪里都会留下痛苦和毁灭。他们的恐惧空间高浮于天幕之上，并非闲置，而是一直在观察等待；他们的探员搜寻这片土地，他们的军团不断积蓄力量，他们的学者开发出全新的策略和法术。隔绝两端世界的屏障，在他们的破坏下开始破碎；无助的埃亚尔居民悄然消失，被掠走成为他们的奴隶和玩物。恶魔用魔法力量改造了受害者，使其能够在恶魔的拷问中存活 —— 你，能使用自己刚刚觉醒的新力量，逃脱玛·洛克的恶魔军团吗？

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

```

## entry-03456
位置：tome-ashes-urhrok.lua:1825；section：tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome #LIGHT_GREEN#@name@#WHITE#.
You do not remember much of your life before you were on this burning continent, floating in the void between worlds.  You have been helping demons, happily participating in their experiments to shatter some sort of shield preventing them from taking their righteous revenge on Eyal.

You are being taken by your handler to the torture-pits to help them figure out how to cause the most pain to those on Eyal, when you hear a roaring above you; you look up and see a burning meteor, flying closer, and the demons' spells failing to divert its course!  It lands near you, knocking you off your feet with its shockwave and killing your handler instantly.

As you recover, and your platform of searing earth splits from the main continent, your old memories flood your mind and you come to your senses - the demons are out to destroy your home!

#{bold}#You must escape!#{normal}#.

```
译文：
```text
你好，#LIGHT_GREEN#@name@#WHITE#。
你已经不太记得来到这片漂浮在虚空中的燃烧大陆之前的记忆了。你曾经帮助过恶魔，欢欣着参与他们的实验，以打破某种阻止恶魔正义复仇的无形屏障。

你被你的“主人”带到折磨场以帮助研究如何对埃亚尔大陆的生灵造成更大的痛苦，突然一阵轰鸣从天上传来，你抬头，看见一颗燃烧着的陨石正在坠落。恶魔试图用法术改变其轨迹，但没有成功！它落在你身边，砸死了你的“主人”，同时你也被冲击波击飞。

当你醒来后，你发现你身处一处和主大陆分离的焦土，而你旧时的记忆渐渐涌来。你立时惊醒——恶魔们要毁灭你的故乡！

#{bold}#你必须逃离这里！#{normal}#。

```

## entry-03457
位置：tome-ashes-urhrok.lua:1846；section：tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Corruptor (Demonologist)
```
译文：
```text
新职业：#LIGHT_GREEN#堕落系（恶魔使者）
```

## entry-03458
位置：tome-ashes-urhrok.lua:1847；section：tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Demons in their invasion of Eyal have abducted natives of the planet and mindwiped them to serve as double agents.
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

```
译文：
```text
在入侵埃亚尔大陆的过程中，恶魔绑架了这颗星球的居民，将他们洗脑后训练为双面间谍。

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

```

## entry-03459
位置：tome-ashes-urhrok.lua:1908；section：tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Race: #LIGHT_GREEN#Doomelf
```
译文：
```text
新种族：#LIGHT_GREEN#魔化精灵
```

## entry-03460
位置：tome-ashes-urhrok.lua:1909；section：tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Doomelves are not a real race, they are Shaloren that have been taken by demons and transformed into harbingers of doom.
Their skills in inflicting and resisting pain have been honed by their rigorous training on the Fearscape.

You have killed the only three explorers from Mal'Rok that could have told the demons the truth and thus have earned the right to make #LIGHT_GREEN#Doomelf#WHITE# characters.

Race features:#YELLOW#
- Instant cast phase door
- Can turn into a dúathedlen
- Can increase detrimental effects and reduce beneficial ones on their foes
#WHITE#

```
译文：
```text
魔化精灵并不是一个真正的种族，他们曾是永恒精灵，而被恶魔抓去，变为末日的使者。
恶魔空间的烈火和严格训练磨砺了他们抵御痛苦、施展痛苦的强大能力。

你已经终结了从恶魔家乡玛·洛克来的仅有的那三位探险者。现在，恶魔们将无法了解到有关埃亚尔大陆的真相，#LIGHT_GREEN#魔化精灵#WHITE# 应运而生。

种族特点 :#YELLOW#
- 使用加速技能，瞬间穿梭空间
- 转化成多瑟顿形态
- 可以延长敌人的负面效果，缩短敌人的正面效果
#WHITE#

```

## entry-03461
位置：tome-ashes-urhrok.lua:1934；section：tome-ashes-urhrok/overload/mod/class/DemonologistsDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Shadow Power: 
```
译文：
```text
阴影强度： 
```

## entry-03462
位置：tome-cults.lua:5；section：tome-cults/data/achievements/all.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Read a Forbidden Tome.
```
译文：
```text
读一本禁忌之书。
```

## entry-03463
位置：tome-cults.lua:42；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, +0 Dexterity, +3 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，+0 敏捷，+3 体质
```

## entry-03464
位置：tome-cults.lua:43；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Magic, +0 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * +3 魔法，+0 意志，+0 灵巧
```

## entry-03465
位置：tome-cults.lua:44；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# +3
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# +3
```

## entry-03466
位置：tome-cults.lua:51；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# -4
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# -4
```

## entry-03467
位置：tome-cults.lua:66；section：tome-cults/data/birth/drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, +1 Dexterity, +1 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，+1 敏捷，+1 体质
```

## entry-03468
位置：tome-cults.lua:67；section：tome-cults/data/birth/drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +2 Magic, -1 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * +2 魔法，-1 意志，+0 灵巧
```

## entry-03469
位置：tome-cults.lua:68；section：tome-cults/data/birth/drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 12
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 12
```

## entry-03470
位置：tome-cults.lua:69；section：tome-cults/data/birth/drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Experience penalty:#LIGHT_BLUE# 12%
```
译文：
```text
#GOLD#经验惩罚：#LIGHT_BLUE# 12%
```

## entry-03471
位置：tome-cults.lua:111；section：tome-cults/data/birth/krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, -1 Dexterity, +2 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，-1 敏捷，+2 体质
```

## entry-03472
位置：tome-cults.lua:112；section：tome-cults/data/birth/krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * -2 Magic, +2 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * -2 魔法，+2 意志，+0 灵巧
```

## entry-03473
位置：tome-cults.lua:113；section：tome-cults/data/birth/krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 13
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 13
```

## entry-03474
位置：tome-cults.lua:114；section：tome-cults/data/birth/krog.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Experience penalty:#LIGHT_BLUE# 15%
```
译文：
```text
#GOLD#经验惩罚：#LIGHT_BLUE# 15%
```

## entry-03475
位置：tome-cults.lua:193；section：tome-cults/data/chats/godfeaster-malyu-escaped.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Oh, I suddenly feel like I have potential to grow.
```
译文：
```text
哦，我觉得我的潜能增长了。
```

## entry-03476
位置：tome-cults.lua:194；section：tome-cults/data/chats/godfeaster-malyu-escaped.lua；source_tag：_t；args_order：None；special：None

原文：
```text
...Fine, be that way. Good luck out there, though.
```
译文：
```text
…好吧，就这样吧。祝你一路顺风。
```

## entry-03477
位置：tome-cults.lua:207；section：tome-cults/data/chats/godfeaster-malyu.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Who..what.. YES!
```
译文：
```text
是谁…什么…对！我在里面！
```

## entry-03478
位置：tome-cults.lua:326；section：tome-cults/data/general/events/digestive-sack.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#DARK_SEA_GREEN#An object rolls from the sack!
```
译文：
```text
#DARK_SEA_GREEN#一个物品从消化袋里掉了出来！
```

## entry-03479
位置：tome-cults.lua:327；section：tome-cults/data/general/events/digestive-sack.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#DARK_SEA_GREEN#A not yet digested foe burst out from the sack!
```
译文：
```text
#DARK_SEA_GREEN#一个没有被完全消化的敌人从消化袋里掉了出来！
```

## entry-03480
位置：tome-cults.lua:329；section：tome-cults/data/general/events/digestive-sack.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#DARK_SEA_GREEN#Sickening fumes emanates from the sack as it opens!
```
译文：
```text
#DARK_SEA_GREEN#袋子打开时散发出令人作呕的烟雾！
```

## entry-03481
位置：tome-cults.lua:347；section：tome-cults/data/general/events/space-dwarf-ship.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You have already scavenged what you could understand and use.
```
译文：
```text
你已经找遍了你能理解和使用的东西。
```

## entry-03482
位置：tome-cults.lua:384；section：tome-cults/data/general/grids/fonts.lua；source_tag：log；args_order：None；special：None

原文：
```text
#PURPLE#The %s glows as you touch it. Your knowledge grows (+1 prodigy point).
```
译文：
```text
#PURPLE#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 觉醒点）。
```

## entry-03483
位置：tome-cults.lua:385；section：tome-cults/data/general/grids/fonts.lua；source_tag：log；args_order：None；special：None

原文：
```text
#VIOLET#The %s glows as you touch it. Your knowledge grows (+1 category point).
```
译文：
```text
#VIOLET#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 技能树解锁点）。
```

## entry-03484
位置：tome-cults.lua:386；section：tome-cults/data/general/grids/fonts.lua；source_tag：log；args_order：None；special：None

原文：
```text
#YELLOW#The %s glows as you touch it. Your knowledge grows (+1 class talent point).
```
译文：
```text
#YELLOW#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 职业技能点）。
```

## entry-03485
位置：tome-cults.lua:387；section：tome-cults/data/general/grids/fonts.lua；source_tag：log；args_order：None；special：None

原文：
```text
#ORANGE#The %s glows as you touch it. Your knowledge grows (+1 generic talent point).
```
译文：
```text
#ORANGE#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+1 通用技能点）。
```

## entry-03486
位置：tome-cults.lua:388；section：tome-cults/data/general/grids/fonts.lua；source_tag：log；args_order：None；special：None

原文：
```text
#AQUAMARINE#The %s glows as you touch it. Your knowledge grows (+3 stat points).
```
译文：
```text
#AQUAMARINE#当你触摸%s的时候，它闪烁了一下。你的知识增长了（+3 属性点）。
```

## entry-03487
位置：tome-cults.lua:410；section：tome-cults/data/general/grids/fortress-multiverse.lua；source_tag：say；args_order：None；special：None

原文：
```text
#CRIMSON#The entropic control orb seems unresponsive...
```
译文：
```text
#CRIMSON#熵控制球看上去不对你起反应……
```

## entry-03488
位置：tome-cults.lua:427；section：tome-cults/data/general/grids/godfeaster.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This door seems to have been sealed off. You think you can open it.
```
译文：
```text
这扇门似乎被封住了，你觉得你可以打开它。
```

## entry-03489
位置：tome-cults.lua:443；section：tome-cults/data/general/grids/maggot.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This door seems to have been sealed off. You think you can open it.
```
译文：
```text
这扇门似乎被封住了，你觉得你可以打开它。
```

## entry-03490
位置：tome-cults.lua:475；section：tome-cults/data/general/grids/slimy_godfeaster.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This door seems to have been sealed off. You think you can open it.
```
译文：
```text
这扇门似乎被封住了，你觉得你可以打开它。
```

## entry-03491
位置：tome-cults.lua:537；section：tome-cults/data/general/npcs/blobs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A green oozing defence cell of the Maggot.
```
译文：
```text
这团绿泥是巨大蛆虫的防御细胞。
```

## entry-03492
位置：tome-cults.lua:539；section：tome-cults/data/general/npcs/blobs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A reddish attack cell that will crawl to you to distract you while the rest of the organism attacks.
```
译文：
```text
一团红色的攻击细胞，它会爬到你的身边，在这个生物体的其余部分发动攻击时分散你的注意力。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Corruptor	腐化者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Demonologist	恶魔使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Doombringer	毁灭使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Horns	角	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Phase Door	相位之门	T.GAME.TALENT	talents	talent name	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Thrall	奴仆	T.GAME.EFFECT	combat	_t	preferred	core	精神支配后目标的状态身份；与 Mental Domination“精神控制”能力名区分
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
corruption	堕落	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
demonic strength	恶魔之力	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fearscape	恶魔空间	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
maggot	蛆虫	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
torture	折磨	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
