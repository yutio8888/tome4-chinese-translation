# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03733–entry-03772 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g15-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03733 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03733
位置：tome-orcs.lua:347；section：tome-orcs/data/chats/destructicus.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*Are you SURE you want to ERADICATE THE STEAM GIANTS?*#WHITE#
```
译文：
```text
#LIGHT_GREEN#*你确认要消灭蒸汽巨人么？*#WHITE#
```

## entry-03734
位置：tome-orcs.lua:349；section：tome-orcs/data/chats/destructicus.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*Are you SURE you want to WASTE YOUR SHOT?*#WHITE#
```
译文：
```text
#LIGHT_GREEN#*你确认要浪费子弹么？*#WHITE#
```

## entry-03735
位置：tome-orcs.lua:350；section：tome-orcs/data/chats/destructicus.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*The Steam Giants are too great a threat to allow their escape - you will not have them simply return someday to finish what they attempted, and wipe out your Pride.  You press the #{italic}#"PREVIOUS TARGET"#{normal}# button, and fire on the airship.  There is a great roar and a flash of flame; you see its missile flying away from you through the window, as you see it racing towards your view, and the terrified passengers, on the scrying panel.

It reaches its mark, and the panel goes dark as a tremendous, multicolored blast fills your vision through the window.
 
The Steam Giants are no more.
 
The secondary charges from the warhead detonate, as burning debris falls into the sea, and the ongoing display serves as a signal to all the Orcs of Var'Eyal, and anyone else who may be watching: This is the fate of all who would try to eradicate the Orcs.  The previous millennia of oppression, genocide, and bullying are over: your people will never be pushed around like this again.
 
A nagging thought in the back of your head insists that you now know how the Sun Paladins felt, how King Toknor felt, how the halflings felt, how everyone that has always committed such atrocities against the Orcs felt.  It can keep whining all it wants - your people are finally safe.*#WHITE#
```
译文：
```text
#LIGHT_GREEN#*让蒸汽巨人们逃离太过危险 - 你不能允许他们这样简单的离开，然后将来某日再实现其图谋，消灭你的部落。你按下#{italic}#"上一名目标"#{normal}# 按钮，朝飞船开火。一阵巨大的轰鸣声和一道强烈的火光闪过，你从窗户里看见导弹朝目标飞去，飞向你视线远处，拥挤的飞船里惊恐的乘客那边。

导弹到达了目的地，巨大的爆炸堵塞了你透过窗户的视线，面板随之变暗。

蒸汽巨人消失了。

弹头的次级装药引爆，燃烧的残骸坠入大海，这场持续的烟火盛宴成为大陆上所有兽人，甚至所有能看到这一盛景的生物的信号：
这就是所有试图消灭兽人的种族的命运。千年的压制、欺凌和屠杀被终结了：你的人民再也不会沦落如斯。

无法摆脱的念头自你脑后升腾，你现在明白了太阳骑士的感受，明白了图库纳国王的感受，明白了半身人的感受，明白了所有曾对兽人施以暴行的人的感受。
随它哀诉去吧————但你的人民终于安全了。*#WHITE#
```

## entry-03736
位置：tome-orcs.lua:404；section：tome-orcs/data/chats/john-surrender.lua；source_tag：_t；args_order：None；special：None

原文：
```text
DEATH!
```
译文：
```text
去死吧！
```

## entry-03737
位置：tome-orcs.lua:409；section：tome-orcs/data/chats/john-surrender.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#[destroy him to power the ring]#WHITE# So be it!
```
译文：
```text
#LIGHT_GREEN#[杀死他来强化戒指]#WHITE# 如你所愿！
```

## entry-03738
位置：tome-orcs.lua:410；section：tome-orcs/data/chats/john-surrender.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#[bind him to the ring]#WHITE# No, you are more useful alive and broken to me!
```
译文：
```text
#LIGHT_GREEN#[将他绑定到戒指上]#WHITE# 不，你活着对我更有用！
```

## entry-03739
位置：tome-orcs.lua:411；section：tome-orcs/data/chats/john-surrender.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*The malevolent energies around you condensate into the ring, absorbing the last remains of John.
The ring is now much more powerful.*#WHITE#
Aeryn... my love...
```
译文：
```text
#LIGHT_GREEN#*你周围的邪恶能量凝聚到戒指中，吸收了约翰的剩余力量。
戒指变得更加强大了。*#WHITE#
艾琳……我的爱人……
```

## entry-03740
位置：tome-orcs.lua:417；section：tome-orcs/data/chats/john-surrender.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*The malevolent energies around you condense into the ring, binding John to it forever.
The ring is now able to summon him for a few turns at will.*#WHITE#
#{bold}#I HATE YOU!#{normal}#
```
译文：
```text
#LIGHT_GREEN#*在你周围的邪恶能量凝聚到戒指中，将约翰绑定到戒指上。
戒指现在具有召唤他的能力。*#WHITE#
#{bold}#我恨你！#{normal}#
```

## entry-03741
位置：tome-orcs.lua:426；section：tome-orcs/data/chats/john-worldmap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*As you approach you recognize Outpost Leader John. But there is a kind of terrible darkness, you can feel his hatred crystallize the air.*#WHITE#
@playername@. You malevolent creature! #{bold}#YOU KILLED HER! YOU MURDEROUS DOG!#{normal}#
You #{italic}#dare#{normal}# carry her ring around like a trophy! I can feel it on you. Give it back! DIE!
```
译文：
```text
#LIGHT_GREEN#*当你靠近时，你认出了那是前哨站首领约翰。但他身边环绕着可怕的黑暗，你能感受到他的仇恨令空气结晶。*#WHITE#
@playername@ 你这个残忍的畜生！#{bold}#你杀了她！你这条残忍的狗！#{normal}#
你 #{italic}#竟敢#{normal}# 带着她的戒指作为战利品！我能感觉到它在你身上。拿出来，受死吧！！
```

## entry-03742
位置：tome-orcs.lua:432；section：tome-orcs/data/chats/john-worldmap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
She left me no choice; I had to protect #{bold}#my#{normal}# people.
```
译文：
```text
她令我别无选择；我必须保护 #{bold}#我的#{normal}# 族民。
```

## entry-03743
位置：tome-orcs.lua:435；section：tome-orcs/data/chats/john-worldmap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
What?
```
译文：
```text
什么？
```

## entry-03744
位置：tome-orcs.lua:440；section：tome-orcs/data/chats/kaltor-entry.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*As you open the door to the shop, you are greeted by a pair of Steam Giant guards, staring at you and holding their steamguns tightly, at the ready but not aimed at you.*#WHITE#
No sudden moves, @playername@. Kaltor's orders are to consider you a customer for now. Try anything foolish, and you'll be a live demonstration for his newest guns instead.  Understand?
```
译文：
```text
#LIGHT_GREEN#*当你打开商店大门，你被两名蒸汽巨人守卫迎接，他们盯着你看，手中紧握蒸汽枪，准备就绪，但并没有瞄准你。*#WHITE#
别乱动，@playername@。卡托尔的指令让我们将你视为顾客。做蠢事的话，你就会成为他新枪的活体演示。明白了么？
```

## entry-03745
位置：tome-orcs.lua:457；section：tome-orcs/data/chats/kaltor-shop.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Finally a practical giant! Show me your wares.
```
译文：
```text
终于来了一位有理性的巨人！给我看看你的货。
```

## entry-03746
位置：tome-orcs.lua:460；section：tome-orcs/data/chats/kaltor-shop.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*A well-dressed giant stands in front of you, covered in expensive jewelry; judging from the poorly-fastened clasp on his necklace, you can assume he acquired it all fairly recently.  He grins as he leans down over the counter to get a good view of you.*#WHITE#
Ah, welcome, @playername@! #LIGHT_GREEN#*he yells in a voice loud enough to catch the attention of all in the shop, as he lifts his head to look around.*#WHITE# Yes, you heard me right, @playername@! The very same one who's been running rampant through the Vaporous Emporium is coming to ME for armaments! I don't think I could've asked for a stronger endorsement! #LIGHT_GREEN#*He looks back down to you, leaning over the counter to point out a glass display case loaded with exotic weaponry and armor.*#WHITE#
Well, I'm not one to turn down anyone with gold, and seeing as you've already made me rich, I'll even give you a discount, down to my pre-attack prices. #LIGHT_GREEN#*He leans in uncomfortably close, staring you in the eyes.* #WHITE#Or, if you came to do here what you did in the Emporium... #LIGHT_GREEN#*He directs his glare toward the multiple well-armed guards staring at you and standing still on the sides of the room.*#WHITE# I'm sure my #{italic}#emergency safety measures#{normal}# would just #{italic}#love#{normal}# an opportunity to try out their shiny new toys.
```
译文：
```text
#LIGHT_GREEN#*一名衣着讲究的巨人站在你面前，戴满昂贵的珠宝；从他松垮的项链扣上看，你猜测他是最近才拿到的。他微笑着从柜台往下看，注视着你。*#WHITE#
哦，欢迎，@playername@! #LIGHT_GREEN#*他的声音大的让店里所有人都听见，同时他抬起头张望四周。*#WHITE# 是的，听见了么，@playername@！就是那个在蒸汽商场猖獗无比的家伙，他到我这来买装备了！我认为不会有比这更好的宣传了！#LIGHT_GREEN#*他转过头看你，指出一个玻璃展台，那上面装满异种武器和护甲。*#WHITE#
好吧，我不会拒绝任何带着钱过来的人，同时你也已经让我富裕不少了。我甚至还能给你打个折，降到进攻前的价格。#LIGHT_GREEN#*他靠得过近，让你感觉不太舒服。他直视着你的眼睛。*#WHITE#或者，你也可以试试你在蒸汽商店里干的事情……
#LIGHT_GREEN#*他指向周围和房间里那些装备良好的警卫。*#WHITE#
我相信我的#{italic}#紧急安全保卫#{normal}#一定#{italic}#爱死了#{normal}#每一个尝试新玩具的机会。
```

## entry-03747
位置：tome-orcs.lua:467；section：tome-orcs/data/chats/kaltor-shop.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome back, @playername@!  You see this, customers?  This fearsome, savage master of battle was so impressed by my products that he came back for more!
#LIGHT_GREEN#*He points to a new poster on the wall next to him, showing your face and the caption #{bold}#"KALTOR: THE CHOICE OF DESTROYERS!"#{normal}#*#WHITE#

So, what'll it be?
```
译文：
```text
欢迎回来，@playername@! 来看看这个，顾客们？这位可怕而野蛮的战斗大师也对我的产品印象深刻，现在他又回来买东西了！
#LIGHT_GREEN#*他指向墙上贴着的新海报，上面是你的脸和一行大字 #{bold}#"卡托尔：破坏者的选择！"#{normal}#*#WHITE#

那么，你要做什么呢？
```

## entry-03748
位置：tome-orcs.lua:474；section：tome-orcs/data/chats/kaltor-shop.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#*Kaltor is busy packing some of his goods away in crates; he hands one to a worker, carrying it out the back door, before turning to you.*#WHITE#
	Make it quick, @playername@. Not to be rude, but there's a private airship out there with my name on it, and I'd rather have a bird's-eye view of what you're about to do than a front-row seat.
```
译文：
```text
#LIGHT_GREEN#*卡托尔忙着打包货物；他将箱子递给一个工人带到后门，然后转过头和你说话。*#WHITE#
	快点吧，@playername@。不是我粗鲁，但现在有一艘我的飞船在外面，我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。
```

## entry-03749
位置：tome-orcs.lua:480；section：tome-orcs/data/chats/kaltor-shop.lua；source_tag：_t；args_order：None；special：None

原文：
```text
DEATH!
```
译文：
```text
去死吧！
```

## entry-03750
位置：tome-orcs.lua:508；section：tome-orcs/data/chats/metash.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The rest of us have fled, hiding in caverns across the peninsula...  I cannot in good conscience ask you to face certain death before his magic for our sakes, but striking first may be the only way to save your people.  He appears to be stalling the invasion, buying you some time, but if you cannot catch him off-guard before he finally commits to it...  I've seen his power cut through a mountain like it was a leaf, soft-foot.  There can be no victory against that kind of magic.  Run, hide, and hope he falls victim to an accident or loses the remaining fragments of his sanity that keep him capable of casting spells.
```
译文：
```text
我们其他人都跑了，藏身在洞穴中……凭良心说，我不应让你直面他的魔法，那一定会带来死亡。但只有抢先下手，才能拯救你的族民。他暂时不会进攻，为你赢得了一些时间。但如果你不能在他进攻前打他个措手不及……软蹄者，我曾经看着他的力量洞穿山脉，仿佛穿过一片树叶般轻松。算了，不可能战胜这种魔法的。跑吧，躲起来，希望他能意外身亡，或者进一步失去理智以至于不能施法吧。
```

## entry-03751
位置：tome-orcs.lua:513；section：tome-orcs/data/chats/metash.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Hail, @playername@!
```
译文：
```text
嘿，@playername@！
```

## entry-03752
位置：tome-orcs.lua:514；section：tome-orcs/data/chats/metash.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Our is free Metash, the tyrant is no more.
```
译文：
```text
我们自由了梅塔什，暴君被打败了。
```

## entry-03753
位置：tome-orcs.lua:515；section：tome-orcs/data/chats/metash.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I came here to warn the Kruk Pride of the threat Nektosh poses and ask for their help, but they have some more immediate threats to deal with...  We should help them repel these Steam Giants.  They are the only people who have ever treated us with respect and dignity; if they are crushed by the Atmos Tribe or the Allied Kingdoms, we will surely be next.  Their success is our survival.

Unfortunately, they cannot afford to spare the warriors to retake the Mana Caves from that tyrant, and I need to stay here to help them defend their land.  The task of freeing our clan is in your hands, when you feel ready for it.
```
译文：
```text
我来这里是为了警告克鲁克部落独角者纳克托什的危险，并请求他们的帮助。但他们有更迫切的威胁需要处理……我们应该帮他们抵抗蒸汽巨人。他们是唯一以尊重和尊严对待我们的人，如果他们被气之部族或者联合王国摧毁，下一个就是我们。他们的成功就是我们的生存希望。

不幸的是，他们现在没有空闲的战士来帮我们从暴君手中夺回魔法洞穴。我需要留在这保护他们。解放我们氏族的任务就交给你了，做好准备去吧。
```

## entry-03754
位置：tome-orcs.lua:523；section：tome-orcs/data/chats/metash.lua；source_tag：_t；args_order：None；special：None

原文：
```text
He...  he found a wand?  And he realized it was running dry, but only after taking over the tribe?  I pity him, but I cannot forgive him for being willing to sacrifice so many Whitehooves and Orcs to escape the consequences of his brief lapse into madness...  still, as a personal request I ask that you not tell others of his last thoughts.  The Nektosh we once knew saved our tribe from the corrupted magic deep under Eyal; he deserves to, at worst, be remembered as one who tragically succumbed to its influence.

Ultimately, though, the choice is yours; it is more important that he is no longer a threat.  There are some who may still cling to the false hope he gave them, but we will retake the Mana Caves from them in time.  We owe you a great debt, and now that we have no more pressing concerns, we can aid Kruk Pride in their rebellion.  Good travels, @playername@.
```
译文：
```text
他……  他找到了一根魔棒？然后等到他掌控了我们氏族，才发现能量快用完了？我对此感到遗憾，但我不能原谅他。为了逃避自己陷入疯狂的责任，他准备牺牲这么多重要的白蹄族人和兽人……尽管如此，我请求你不要告诉别人他的想法。纳克托什是曾经将我们从埃亚尔深处的堕落魔法中拯救出来的英雄，他至少应该被铭记为一个悲剧性地屈服于那种影响的人。

当然，选择权在你手中；重要的是他的威胁解除了。虽然仍有人沉醉于他给予的虚假希望中，但我们马上就能夺回魔法洞穴了。我们都欠你很多。现在，我们紧迫的危机已经解除了，该是帮助克鲁克部落的时候了。祝你好运，@playername@。
```

## entry-03755
位置：tome-orcs.lua:557；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Waiting for me?
```
译文：
```text
等我？
```

## entry-03756
位置：tome-orcs.lua:558；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
What do you need me for?
```
译文：
```text
你要我干啥？
```

## entry-03757
位置：tome-orcs.lua:559；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I have muscle tissue for you.
```
译文：
```text
我有一些肌肉组织要给你。
```

## entry-03758
位置：tome-orcs.lua:562；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I see...
```
译文：
```text
我明白了……
```

## entry-03759
位置：tome-orcs.lua:567；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
That is... generous of you.
```
译文：
```text
这真是……慷慨。
```

## entry-03760
位置：tome-orcs.lua:574；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
What do you wish to learn?
```
译文：
```text
你想学什么？
```

## entry-03761
位置：tome-orcs.lua:575；section：tome-orcs/data/chats/weissi-machine.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use your %s anymore; it is tainted by magic.
```
译文：
```text
你不能再使用 %s，它已被魔法所污染。
```

## entry-03762
位置：tome-orcs.lua:604；section：tome-orcs/data/damage_types.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-03763
位置：tome-orcs.lua:607；section：tome-orcs/data/damage_types.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is pulled!
```
译文：
```text
%s被拖动！
```

## entry-03764
位置：tome-orcs.lua:608；section：tome-orcs/data/damage_types.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the pull!
```
译文：
```text
%s抵抗了拖动！
```

## entry-03765
位置：tome-orcs.lua:711；section：tome-orcs/data/general/events/merchant-stall.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A market stall, it looks abandoned..
```
译文：
```text
一个市场摊位，看起来被遗弃了……
```

## entry-03766
位置：tome-orcs.lua:714；section：tome-orcs/data/general/events/merchant-stall.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You loot the stall and gain:

```
译文：
```text
你洗劫了这个市场摊位，获得了：

```

## entry-03767
位置：tome-orcs.lua:724；section：tome-orcs/data/general/events/sewer-alligator-nest.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#GOLD#The conduit shatters open, releasing huge angry alligators!
```
译文：
```text
#GOLD#管道破裂，释放出愤怒的巨大鳄鱼！
```

## entry-03768
位置：tome-orcs.lua:757；section：tome-orcs/data/general/grids/mechstone.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This door seems to have been sealed off. You think you can open it.
```
译文：
```text
这扇门似乎被封住了，你觉得你可以打开它。
```

## entry-03769
位置：tome-orcs.lua:773；section：tome-orcs/data/general/grids/mechwall.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This door seems to have been sealed off. You think you can open it.
```
译文：
```text
这扇门似乎被封住了，你觉得你可以打开它。
```

## entry-03770
位置：tome-orcs.lua:791；section：tome-orcs/data/general/grids/slumbering_cave.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
corrupted cave door (open)
```
译文：
```text
被污染的山洞门（已打开）
```

## entry-03771
位置：tome-orcs.lua:840；section：tome-orcs/data/general/npcs/hethugoroth.lua；source_tag：entity type；args_order：None；special：None

原文：
```text
elemental
```
译文：
```text
元素生物
```

## entry-03772
位置：tome-orcs.lua:957；section：tome-orcs/data/general/npcs/sunwall-mage.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
astral conjurer
```
译文：
```text
星空魔术师
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Atmos Tribe	气之部族	T.PN.FACTION	society	faction name	preferred	dlc	Embers of Rage 阵营专名；统一为“气之部族”（叙事文本曾作“气之部落”），与气之部族 NPC/叙事一致
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Kruk Pride	克鲁克部落	T.PN.FACTION	society	faction name	existing	dlc	Embers of Rage 阵营
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Oppression	压制	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Whitehooves	白蹄	T.PN.FACTION	society	faction name	existing	dlc	Embers of Rage 阵营
armament	武装	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
vaporous emporium	蒸汽商场	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
var'eyal	瓦·埃亚尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
whitehooves	白蹄	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
