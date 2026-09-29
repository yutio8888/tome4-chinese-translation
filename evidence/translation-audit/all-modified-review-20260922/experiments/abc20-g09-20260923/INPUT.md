# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03493–entry-03532 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g09-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03493 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03493
位置：tome-cults.lua:556；section：tome-cults/data/general/npcs/corrupted_blobs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A green oozing defence cell of the Maggot.
```
译文：
```text
这团绿泥是巨大蛆虫的防御细胞。
```

## entry-03494
位置：tome-cults.lua:558；section：tome-cults/data/general/npcs/corrupted_blobs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A reddish attack cell that will crawl to you to distract you while the rest of the organism attacks.
```
译文：
```text
一团红色的攻击细胞，它会爬到你的身边，在这个生物体的其余部分发动攻击时分散你的注意力。
```

## entry-03495
位置：tome-cults.lua:580；section：tome-cults/data/general/npcs/horror.lua；source_tag：_t；args_order：None；special：None

原文：
```text
And you thought radiant horrors were bad.
```
译文：
```text
你还以为光芒恐魔就够糟了呢。
```

## entry-03496
位置：tome-cults.lua:585；section：tome-cults/data/general/npcs/horror.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A strange tall crystal pusling with nether energies. It's broken. Tentacles come out of it to get you! #{bold}#RUN!#{normal}#
```
译文：
```text
一团发射出虚空能量的高大水晶。它的破裂处伸出触手抓向你。#{bold}#快跑！#{normal}#
```

## entry-03497
位置：tome-cults.lua:676；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A writhing mass of tentacles roughtly warped into the form of a ring. A dark malovelant power emanates from it.
```
译文：
```text
大量扭曲的触须弯曲成了指环的形状。一团黑暗的恶意力量从里面散发出来。
```

## entry-03498
位置：tome-cults.lua:677；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
When first worn the ring attunes to you, letting you choose a prodigy it will forever grant while worn (can not be changed once chosen, re-wear it to select again if you refused to choose at first).
```
译文：
```text
当你第一次戴上戒指的时候，选择一个觉醒技能，你将在戴上这个戒指的时候获得这个觉醒技能（一旦选择就不能改变。如果你第一次没有选择，可以在重新装备的时候进行选择）。
```

## entry-03499
位置：tome-cults.lua:678；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#DARK_SEA_GREEN#While the ring senses battle it grips your finger so hard you can not take it off.
```
译文：
```text
#DARK_SEA_GREEN#指环感知到了战斗，牢牢抓住了你的手指，你无法脱下。
```

## entry-03500
位置：tome-cults.lua:679；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#DARK_SEA_GREEN#As you put the %s on your finger, you feel more attuned to the horror within you.
```
译文：
```text
#DARK_SEA_GREEN#当你将%s戴在手上，你觉得你和体内的恐魔更加协调了。
```

## entry-03501
位置：tome-cults.lua:683；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
It seems willing and able to talk to you (use Command Staff).
```
译文：
```text
它似乎愿意和你交谈（使用法杖掌控）。
```

## entry-03502
位置：tome-cults.lua:727；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of power (+3% spell critical chance)
```
译文：
```text
威力的重要性（+3% 法术暴击率）
```

## entry-03503
位置：tome-cults.lua:728；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of thought (+10 spell save)
```
译文：
```text
思考的重要性（+10 法术豁免）
```

## entry-03504
位置：tome-cults.lua:729；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of magic (+5 magic)
```
译文：
```text
魔法的重要性（+5 魔力）
```

## entry-03505
位置：tome-cults.lua:730；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of wisdom (+5 willpower)
```
译文：
```text
智慧的重要性（+5 意志）
```

## entry-03506
位置：tome-cults.lua:738；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of evading blows (+10 defense)
```
译文：
```text
闪避攻击的重要性（+10 闪避）
```

## entry-03507
位置：tome-cults.lua:739；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of speed (+10% movement speed)
```
译文：
```text
速度的重要性（+10% 移动速度）
```

## entry-03508
位置：tome-cults.lua:740；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of reflexes (+5 dexterity)
```
译文：
```text
反应力的重要性（+5 敏捷）
```

## entry-03509
位置：tome-cults.lua:741；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The importance of a honed mind (+5 cunning)
```
译文：
```text
磨砺心智的重要性（+5 灵巧）
```

## entry-03510
位置：tome-cults.lua:757；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#DARK_SEA_GREEN#The %s reaches for %s with a tentacle!
```
译文：
```text
#DARK_SEA_GREEN#%s使用触手抓握%s！
```

## entry-03511
位置：tome-cults.lua:776；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#As you wear the sword you feel it attuning to your Krog body, increasing in power!
```
译文：
```text
#LIGHT_BLUE#你感受到你的剑和克罗格的身躯共鸣，解放了强大的力量！
```

## entry-03512
位置：tome-cults.lua:778；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#AQUAMARINE#As the twin weapons of the Krogs are reunited you can feel bursting with power!
```
译文：
```text
#AQUAMARINE#克罗格的两把武器集齐了，你感觉到力量暴涨！
```

## entry-03513
位置：tome-cults.lua:800；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This unusually thick robe constantly wriggles and squirms. Small worms sometimes pop out of it, dropping to the floor. The worms will cushion attacks against your person, but you somehow do not like the idea of having so many parasitic creatures so close to your vulnerable flesh.
```
译文：
```text
这件异常厚重的长袍不断蠕动。上面的小蠕虫有时会从上面跳出来，掉到地板上。这些蠕虫会缓冲敌人对你的攻击，但是让这么多寄生生物如此接近你脆弱的肉体……实在是太恶心了。
```

## entry-03514
位置：tome-cults.lua:825；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
As you combine the two pair of shoes you make something marvelous: %s
```
译文：
```text
当你将这两件鞋子结合时，你制造出了神奇的道具：%s
```

## entry-03515
位置：tome-cults.lua:830；section：tome-cults/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s activates %s %s!
```
译文：
```text
%s激活了%s%s！
```

## entry-03516
位置：tome-cults.lua:880；section：tome-cults/data/glyph_sequences/cults.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#PURPLE#For an instant you feel as if time slowed down over the world! #{italic}#(worldmap patrols permanently slowed down)#{normal}#
```
译文：
```text
#PURPLE#在一瞬间，你感觉到整个世界的时间好像变慢了！#{italic}#（世界地图巡逻队的速度永久减缓了。）#{normal}#
```

## entry-03517
位置：tome-cults.lua:918；section：tome-cults/data/lore/dremwarves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The exploration of the cavity has been interesting, to say the least. At its very centre, we discovered a strange, egg-shaped structure. It's made out of some sort of metal which I have not seen before. Despite being covered in layers of ancient dust, the metal was untarnished and showed no noticeable signs of decay. It was highly resistant to damage, as our attempts to cut through it were met with failure, even when we employed magical means. There was a notable dent in its side, something which could have only been caused by a tremendous amount of force.

There was a passage way leading into the egg, which I volunteered to step through first. The inside of the egg was stranger still. There were dozens of metal tubes which covered the ceiling. Even as I stood there, I could hear the sound of some liquid pouring through them. The walls were covered in blinking lights and yet more metallic objects which I could not make sense of. It is obvious that the egg was some sort of massive machine. I cannot understand how it works or how it was made, though. There is no magic that I can sense, so this machine must rely entirely on mechanical means to function. No race that I know of has the knowledge to build such a thing. I could only imagine what sort of genius could design such a thing, let alone build it. 

Most interesting of all is that the egg has a thin layer of void energy over its entire surface. Us Drem are familiar with such energies, as we have dedicated much of our study to the otherworldly. The even spread of these energies suggests that this egg was completely bathed in them at some point. I do not know what circumstances could have lead to this, for such a concentration of these energies simply couldn't exist on Eyal. Not without causing a violent explosion, at least. We have done such experiments before.

Going deeper inside it, I began to notice that there were a number of glass pipes, wide enough for one of our party to fit in with room to spare. The metallic tubes above me fed into these pipes and pumped some sort of greenish liquid. I had planned to take a closer look, but it was then that we were set upon.

A number of things came crawling out from the dark. Us Drem are rather accustomed to sudden violence, so we tore into them before we could get a clear view of them. We sustained a few minor injuries, but the real shock came after we got a closer look at our attackers. They appeared to be some strange cross between dwarf, drem and something else, yet possessing a strangely child-like body. I imagine the jagged, razor sharp teeth aren't entirely natural either. We were not to be deterred, however. Surface folk may be shocked by such a creature, but we have seen far more sinister things down here.

We had to cut through dozens of them, maybe hundreds of them, in our journey through the egg. There was obviously a source of these things, and their vague resemblance to us spurned me to keep fighting. We eventually came to a chamber which I guessed was the centre of the egg. We found the source of our tormentors. Some great machine, which connected with dozens of glass tubes, appeared to have a malignant growth attached to it. The creatures were being spat out of broken tubes, rapidly growing to their full size and rushing toward us. Each creature varied from looking like a half formed dwarf, drem or some sort of bizarre, tentacled horror.

In the end, we eventually broke the pipes leading into the glass tubes and the creatures stopped coming out. That liquid must have been some sort of substance to nourish those creatures. Without that liquid, only feeble and half formed fetuses crawled out.

But that was only one machine that was making them. We ended up sealing off the chamber as best as we could, but we can hear more of them coming. One of the creatures latched onto my arm during the fight as well. It has infected me with some virulent disease, making my flesh wither away and turned into dried leather.

There is no misunderstanding our fate. We lost many Drem in the fight, and I am not the only one who has been infected with this disease. We are going to die in this room. But, I am content with this fate. I have worked out the truth of our origins.

We wandered into the back of the room where there were yet more tubes. To my surprise, these tubes contained fully formed bodies. A dwarf, complete with a long beard, floated inside the tube. He seemed to twitch like he was in the middle of a dream. As we went further and further down, we found yet more dwarves sleeping inside tubes. But, what we noticed was how with each dwarf, they continued to become more and more malformed. Eventually, we reached the final tube and we found a faceless dwarf inside. In other words, a Drem.

This egg has to be where we came from. This machine was built to create dwarves. I do not understand the process, but I have seen the outcome for myself. It is us Drem that are the anomaly, the dysfunctional byproduct of this machine's disrepair. Feral Drem must have emerged from this egg and ventured into the underground, where they then multiplied independently of the egg. These mutant fetuses must be the result of further disrepair and corruption, judging by the black growth which engulfs the machine in this room.

So, I know now. Even if this discovery never leaves this room, I can die content. Even if I am the product of a broken piece of machinery, I am happy that I had a chance to witness this moment. If you find these notes, please bring them back to my fellow Drem. I am sure they would be happy to know the truth too.
```
译文：
```text
可以说，对洞窟的探索很有意思。在它的中心，我们发现了一个奇怪的蛋形结构。它是由某种我以前没有见过的金属制成的。尽管蛋上覆盖着一层尘土，显示它的历史十分古老，金属却未被破坏，也没有明显的腐蚀迹象。它对各种伤害有很高的抵抗力，即使我们使用魔法手段也没法刺穿它。它的侧面有明显的凹痕，考虑到它卓越的防御力，这个凹痕只有可能是由巨大的力量造成的。

在蛋的外部，有一条通往蛋形结构的通道，我自愿第一个踏入那里。蛋形结构的内部更加陌生。天花板上覆盖着几十根的金属管道，站在管道下，我能听到液体从管道中流过的声音。墙上覆盖着闪烁的灯光，还有更多我无法理解的金属物体。很明显，这个巨蛋是一种巨大的机器。不过，我既不知道它是如何工作的，也不知道它是怎么被制造出来的。我没有感觉到任何魔法的气息，所以这台机器一定是完全依靠机械手段来运作的。我所知道的任何种族都没有建立这样的东西的知识。我不知道到底是什么样的天才可以设计出这样的东西，更不知道谁有能力建造这样的庞然大物。

最有趣的是，巨蛋的整个表面都有覆盖着一层薄薄的虚空能量。我们德瑞姆熟悉这种能量，因为我们研究的主要方向就是异世界。这些能量在巨蛋的外侧均匀散布，表明在某个时刻，这个蛋被这种能量完全沐浴了。我不知道在什么情况下可能会导致这种情况，因为这些能量根本不可能存在于埃亚尔集中出现，否则一定会引起剧烈的爆炸。我们之前做过这样的实验。

进一步深入它，我开始注意到有很多玻璃管，管径很宽，足够让我们的一个小队在里面行走。上方的金属管连入了这些管道，泵进了某种绿色液体。我们本来打算靠近仔细观察一下，但是那时我们突然被袭击了。

一些东西从黑暗中爬了出来。我们德瑞姆习惯于应对突如其来的暴力行为。因此，我们还没来得及看清楚袭击者的面容之前，就本能地把他们撕成了碎片。我们只遭受了轻微损伤，但在我们仔细观察了袭击者之后，我们深深被震惊了。它们似乎是矮人，德瑞姆或是其他生物之间的一种奇异的杂交，但却拥有一个奇怪的孩子般的身体。它们有着锯齿状的锋利的牙齿，显得十分不自然。地面上的人可能会被这样的生物震惊，然而，我们不会被吓倒，因为我们曾经见到过无数更加险恶的东西。

在我们在巨蛋中探索时，我们不得不打倒了几十个，乃至上百个这种怪物。显然，这里就是这些怪物的来源，它们与我们在外貌上的相似性，激励着我继续战斗。最终，我们来到了一个小房间，看来这里就是这个巨蛋的中心。我们找到了这些怪物的来源。那是一些巨大的机器，连接着几十根玻璃管子，有某种恶性的生长物附着在上面。破碎的管子不断吐出这些怪物，迅速成长成完整的大小，然后向我们冲来。这些怪物看起来像是半成型的矮人，德瑞姆，以及某种奇异的，长着触手的恐魔。

我们打破了通往玻璃管的管道，不再有怪物从里面出来了。那些液体肯定是滋养这些怪物的物质，失去了那种液体，里面跑出来的只有一些虚弱的、不成型的生命体。

但我们只是关闭了一台机器而已。我们尽可能地封闭了房间，但我们可以听到更多怪物袭来的声音。在激烈的战斗中，其中一个生物在我的手臂上咬了一口。它传染给了我一种致命的疾病，使我的肌肉萎缩，看起来如同晒干的皮革一般。

我们清楚地了解了自己的命运。我们在战斗中失去了很多同胞，其他人也都感染了这种可怕的疾病。我们即将在这个房间里死去。但是，我们面对着即将到来的死亡命运，却只感到充实和满足，因为我已经弄清了有关我们起源的真相。

我们徘徊到那些还有更多管子的房间里面。令我惊讶的是，管子里是完全成形的生命体。一个留着长胡须的矮人漂浮在管内。他的身体轻轻抽动，仿佛正在梦中。我们越走越远，发现更多矮人睡在管子中，也同时注意到，随着我们继续前进，那些矮人也变得越来越畸形。最终，我们到达了最后一个管子，我们发现里面有一个无脸的矮人——换句话说，一个德瑞姆。

这个巨蛋就是我们的起源。这台机器是为了创造矮人而建造的。我并不了解这个制造的详细过程，但我已经明白了结果。我们德瑞姆一族，是一种异常，是这台年久失修的机器功能失调的副产品。原生的德瑞姆一定是从这个巨蛋中出生的。他们离开创造自己的巨蛋独自生活，冒险进入地下，开始繁衍生息。这些突变的胎儿，一定是这台机器因为年久失修而进一步退化的结果，正如我们在这些机器上看到的，吞噬着这些机器的黑色怪物一样。

所以，我现在知道了一切。即使我们的发现也许会永远留在这个房间里，我也可以死得其所。虽然我们是这台机器的故障的产物，但是我还是很高兴，有机会亲眼见证这一刻。如果你找到这些笔记，请把它们带回给我的德瑞姆同胞。我相信他们会很乐意知道真相。
```

## entry-03518
位置：tome-cults.lua:948；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 1, Chapter 1] - Devastation of the Spellblaze
```
译文：
```text
菲·维莉欧斯的冒险 [第1卷，第1章] - 魔法大爆炸的破坏
```

## entry-03519
位置：tome-cults.lua:998；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 1, Chapter 2] - Infusion Avoidance
```
译文：
```text
菲·维莉欧斯的冒险 [第1卷，第2章] - 对纹身的排斥
```

## entry-03520
位置：tome-cults.lua:1040；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 1, Chapter 3] - Shaloren Suffering
```
译文：
```text
菲·维莉欧斯的冒险 [第1卷，第3章] - 痛苦中的永恒精灵
```

## entry-03521
位置：tome-cults.lua:1078；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 1, Chapter 4] - Medical Treatment
```
译文：
```text
菲·维莉欧斯的冒险 [第1卷，第4章] - 医疗
```

## entry-03522
位置：tome-cults.lua:1079；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]It still strikes me how adverse the shaloren are to infusions. Seemingly they would rather tempt fate and avoid using them. One of the purposes of infusions is to restore one to good health after suffering an injury, but for a shalore it was more a means of last resort to avoid dying. What's more, they seem to fail to understand that holding off on infusion use simply results in them using infusions more in the long run, as beyond just mending their flesh they will have to stave off infection from their open wounds as well.[/i]

Over the next few days I mixed and created several infusions for use by the shaloren. The workshop contained all the amenities for sleeping, and the healer would often bring basic food staples and drink to me. Well, I should say to the shalore it may have been basic food and drink, but by thalore standards I was treated pretty lavishly. I mean, I know the dwarves treat alcohol as a staple good for consumption but apparently so did the shaloren with the amount of wine I was given. Anyhow, how I was treated was quite better then I would have expected to be sure.

Around the fourth day, after having created a great number of infusions, I was asked to come up to help apply them. Many of those I treated were near death, riddled by festering infections brought about from simply bandaging their wounds and nothing else. Similar to how I had treated the wounded shaloren in that lean-to, I only used the infusions as much as possible to get them off of death's door. This wasn't really due to having a lack of infusions but more so as a result of the stubborn mindset shaloren seemed to have in regards to infusions for some reason.

It was about a week later when most of the refugees had been treated that word had arrived of a detachment of shaloren soldiers that had returned from their battles with the orcs. Apparently they had been fighting on the eastern side of the continent along with the Human Kingdoms of the East when the Spellblaze occurred. The scarce few that were still alive after had traveled back to Elvala, but had been stalled as a result of being unable to travel directly through the middle of the continent. Of those that had survived, only a couple hundred had managed to make it back alive.

By this point I had at least some sympathy for those I treated, what after having tended to hundreds of them. But what caught my attention more was what they had said about having been unable to travel directly to Elvala. In the middle of the continent the Midvale Plains were located, a large flat land from which one could literally see just an open field. From my basic knowledge of the continent, the plains were completely open and easily traversable. Unless there was some huge orcish army that had survived and blocked their path, there would have been no need to move northwards around this area.

I didn't have long to ponder my thoughts before one of the assistant healers approached, and handed a bunch of strange tablets in a leather pouch to me. Pulling one of them out I noticed a glowing insignia inscribed on it, which seemed to course with the powers of the arcane. As I turned to ask what these were for, I found only an empty space as the healer had moved on to tend to the soldiers that were entering the building. Perplexed and befuddled as to what I should do with the strange tablets, a nearby tap on my shoulder brought my attention to one of the soldiers. A hand soon reached over and took one of the strange tablets from the pouch.

Turning to see what the soldier was up to, I noticed the huge gashes through the blackened armor he wore. For a moment I stuttered a bit as my hands were full holding the runes and unable to grab any infusions, but then I noticed something peculiar. Amazingly the insignia on the tablet seemed to shimmer and shift, before somehow merging with the soldier's hand. A light blue glow seemed to take a hold of the soldiers eyes as a strange energy seemingly coursed through his body. What occurred next truly caught me off guard as the soldier eventually began to murmur some words, and his deep gaping wounds began to close on their own.

Completely at a loss for what was occurring, the soldier seemed to be healing himself in front of me. As the moment passed the light blue glow left his eyes and they returned to their normal color, his wounds not just healed but showing absolutely no sign of an injury even having existed. It was my first time ever witnessing the use of runes or the use of healing spells. I'd heard of spell use before but I’d never known that runes had even existed at that point in my life. I soon learned the tablets I had been given were called manasurge runes, and that they enabled the restoration of mana lines within a person.

I don't know much about the arcane even now or how it works, but apparently something about the Spellblaze had permanently altered the workings of magic from that point in the world, and while with training it was still possible to call on the powers of magic, it was much more difficult than before. Other wounded soldiers would come after the first and much in the same way they would take the manasurge runes, gain the glowing insignias on their hands, or arms, or legs, really any body part that they wish, and then proceed to cast spells, promptly healing themselves or sometimes other soldiers.

After a while the number of wounded soldiers began to dwindle as most of them didn't require rest after healing themselves. When their numbers began to reach more manageable amounts, the chief healer approached to thank me on behalf of the Shaloren for my efforts. Suddenly remembering the entire reason I had come here to begin with, I noted that I had been fulfilling my end of the bargain. Nodding to this the chief healer looked behind me as a soldier approached and responded "The lieutenant will escort you to the general." I was taken aback by this somewhat but assumed this general held the answers as to the events that had taken place.

The soldier led me to the center of the city where a grand building lay. After meeting with a couple of the guards clad head to toe in shiny plate armor, we were let in. It took several minutes walking through the building’s halls, seemingly walking the building’s entire length to the end of it. Eventually I came to a luxurious looking room, decorations made of stralite and gold lining the walls and displayed pictures of what I assumed to be important figures in Shaloren history. Here I was told to wait, and left by the lieutenant as he entered a nearby room.
```
译文：
```text
[i]我仍然对永恒精灵反对纹身的程度感到十分震惊。似乎他们宁愿接受命运，也要避免使用它们。纹身的目的之一是在受伤后恢复健康，但对于永恒精灵来说，这更是避免死亡的最后手段。更重要的是，他们似乎不明白，推迟纹身的使用只会导致他们在长期内更多地使用纹身，如果不尽快修补他们的皮肤上的伤口，就会面临开放伤口的感染。[/i]

在接下来的几天里，我混合并制作了一些纹身，供永恒精灵使用。工作间里有所有睡觉的便利设施，治疗师经常给我带来基本的主食和饮料。好吧，我应该对永恒精灵说，这可能对它们来说是基本的食物和饮料，但按照自然精灵的标准，我受到了相当慷慨的对待。我的意思是，我知道矮人把酒当作主食来食用，但很明显，根据我拿到的葡萄酒的数量来看，永恒精灵也差不多。不管怎样，我受到的待遇比我预料的要好得多。

大约在第四天，在我做了大量的纹身后，我被他们要求协助使用它们。我治疗过的许多人都快死了，他们被仅仅包扎伤口带来的溃烂感染所困扰。和我在那个简易安置点里对待受伤的永恒精灵的方式类似，我只是尽可能用纹身把他们从鬼门关带回来而已。这并不是因为缺少纹身，而是因为永恒精灵似乎出于某种原因对纹身有着固执的心态。

大约一个星期后，在大多数难民受到治疗后，永恒精灵士兵的一个分遣队的消息传来，他们与兽人战斗后返回埃尔瓦拉。很明显，当魔法大爆炸发生时，他们一直在大陆的东部和东部的人类王国并肩作战。少数仍然活着的人准备返回埃尔瓦拉，但他们由于无法直接穿越大陆中部而停滞不前。在那些幸存下来的人中，只有几百人设法活着回来。

在这个时刻，在我治疗了数百人之后，我至少对我治疗过的那些人有了一些同情。但更吸引我注意的是他们所说的自己无法直接前往埃尔瓦拉这一点。在大陆中部的米德瓦尔平原是一个广阔的平原，可以看作一片真正的平地。根据我的地理学基础知识，这片平原是完全开放的，很容易穿越。除非有一支庞大的兽人军队幸存下来并封锁了他们的道路，否则根本没有必要在这个地区向北移动。

我没有想太久，一个助理治疗师就走过来，递给我一堆装在皮包里的奇怪平板。我把其中一个拿出来，注意到上面刻着一个发光的徽章，看起来像是某种奥术的力量。当我转过身去问这些是干什么用的时候，我发现对方已经走开了，因为治疗师已经开始照料进入大楼的士兵了。对于该如何处理这些奇怪的平板，我感到困惑不解。正在这时，一个士兵拍了拍我的肩膀，吸引了我的注意。他的手很快伸过来，从袋子里拿出一片奇怪的平板。

我转过身去看那个士兵也在干什么，注意到他穿的黑色盔甲上有一道巨大的伤口。有一瞬间，我有些手足无措，因为我的手都拿着符文，无法抓起任何纹身，但后来，我注意到一件奇怪的东西。令人惊讶的是，平板上的徽章似乎在闪烁和移动，然后与士兵的手融合。一种淡蓝色的光芒从士兵的眼睛中闪过，一股奇怪的能量似乎在他的身体里流动。接下来发生的事情真的让我措手不及，士兵开始喃喃自语，他深深的伤口开始自行愈合。

我对于士兵身上发生的一切完全不知所措，他在我面前自愈了。随着时间的流逝，淡蓝色的光芒从他的眼睛中消失，双眼恢复了正常的颜色，他的伤口不仅愈合了，而且完全没有受伤的迹象。这是我第一次看到使用符文和治疗法术。我以前听说过法术的使用，但在那时，我甚至从来没有听说过符文的，甚至不知道符文的存在。我很快就知道，我得到的平板被称为法力涌动符文，它们可以恢复人体内的法力通路。

直到现在，我对奥术魔法都不太了解，也不知道它是如何工作的，但是很明显，从魔法大爆炸那时起，某些东西已经永久地改变了魔法的工作方式，虽然通过训练仍然可以召唤魔法的力量，但这比以前困难得多。其他受伤的士兵也以同样的方式接受治疗，他们拿起法力涌动符文，让发光的印记嵌入手、胳膊、腿，或者任何他们想要的身体部位，然后开始施法，迅速治愈自己，或者治愈其他士兵。

过了一段时间，受伤的士兵开始减少，因为他们中的大多数人在痊愈后不需要休息。当痊愈士兵的数量开始达到一定程度时，主治医师代表永恒精灵来感谢我的努力。我突然想起我来这里的全部原因，意识到我已经完成了我的交易。当一名士兵走近时，主治医师向我点头，看着我，回答说：“中尉会护送你去见将军。”我对此感到有些吃惊，但我认为这位将军对所发生的事件有了答案。

士兵把我带到市中心，那里有一座宏伟的建筑物。在会见了几个身穿闪亮装甲从头武装到脚的警卫后，我们被允许进入。我们在大楼的大厅里走了几分钟，似乎走到了大楼的尽头。最后，我来到了一个豪华的房间，墙壁上有着斯莱特和黄金做成的装饰，并展示了一些我认为是永恒精灵历史上重要人物的画像。在这里，中尉让我等着，然后走进附近的一个房间。
```

## entry-03523
位置：tome-cults.lua:1120；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 1, Chapter 5] - General Aranion Gawaeil
```
译文：
```text
菲·维莉欧斯的冒险 [第1卷，第5章] - 艾伦尼恩·加威尔将军
```

## entry-03524
位置：tome-cults.lua:1154；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 1, Chapter 6] - Leaving Elvala
```
译文：
```text
菲·维莉欧斯的冒险 [第1卷，第6章] - 离开埃尔瓦拉
```

## entry-03525
位置：tome-cults.lua:1196；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 2, Chapter 1] - At The Gates
```
译文：
```text
菲·维莉欧斯的冒险 [第2卷，第1章] - 大门口
```

## entry-03526
位置：tome-cults.lua:1230；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 2, Chapter 2] - Exchange of Information
```
译文：
```text
菲·维莉欧斯的冒险 [第2卷，第2章] - 交换情报
```

## entry-03527
位置：tome-cults.lua:1231；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]You know, it is really hard to know someone. The messenger was a good example of this, as I would soon find out. I had pegged him for being a disgruntled human that had suffered greatly because of the Spellblaze. In reality he was much more than just disgruntled, and I believe he may have been a member of the group instigating the Spellhunt. I'm sure he and the others who had left after with that human in the dark cloak died taking part in a nefarious plot that I would learn the day after. But did he die willingly? That's the real question I think about now in regards to him.[/i]

Finishing my meal, I decided to probe the messenger for information. Upon the completion of his last tirade I asked, "So how are things faring here?" A sigh escaped the man as he answered, "Well, the Nargols appear to have everything under control. They are managing to get enough food for all the refugees streaming in; even managed to procure some alcohol for those dwarves. I have to say it was quite a surprise to see them out here. I wonder if they happen to have anymore homes elsewhere on the continent outside of the Iron Throne. Hard to really know with how secretive the dwarves are though."

While I wasn't exactly interested in the dwarves, that last statement disconnected quite a bit from what I knew about them. From my knowledge of the dwarves, they all lived in the Iron Throne, or at least cities nearby to it. Querying the messenger he soon explained. "Well, the dwarves you see here now had a home over there in the western mountains. The Cornacs were completely ignorant that they had taken up residence so close to them, and the dwarves likely would have kept it a secret. Unfortunately for them they were forced to show themselves since the blasted mages caused their home to collapse in on them."

Satisfied with that answer I remembered about that hollering dwarf when entering the city. I wondered if perhaps the messenger might know something about what that was all about. Noting it I said, "You wouldn't happen to know anything regarding items the dwarves might be carrying that the guards at the city gates would confiscate would you?" The messengers soldiers shrugged before he replied back, "Likely was carrying some item of arcane properties that an accursed mage enchanted long ago. Those dwarves seem to be getting the worse treatment in regards to that, what with the little care they give towards whether an item is contaminated with magic or not."

Shaking his head before going on, the messenger mused aloud, "You know, the Nargol are actively attempting to confiscate items of magical origin as a means of appeasement to placate the halflings living here. They say that it's too dangerous for civilians to carry such items. Personally I say it is too dangerous for anyone to be carrying such items, them included. Of course they are too arrogant to bother fellow halflings living in the city already in regards to giving up such items, expecting them to 'voluntarily' give them up. Really it is just the dwarves, the halfling refugees from outside the city, and us humans getting our possessions taken away." The human proceeded to laugh as he finished saying these words.

The messenger stopped laughing though as a human in a dark cloak approached and leaned down to say something to him. The messenger nodded to the figure upon which he said back, "I'll catch up later, relay back to me the plan when we are ready." To this the human in the dark cloak bowed, hurried over to another table with a couple of halflings and then a table with a dwarf, before then leaving the establishment and disappearing. The halflings and the dwarf finished their food and packed up their things before they quietly left as well. Wondering just who this messenger was I glanced at him to see he examining eyes looking towards me. In a relaxed voice the messenger said, "Don't mind them, were having such a nice conversation to have the others ruin it."

At that point I realized that there was more to this human than I had initially thought. I wondered if he might be a bit more dangerous than I was giving him credit for. Perhaps a bit rashly I decided to see just how much this man knew, and so I quietly stated, "You wouldn't happen to have any plans to deal with the Shaloren?" Almost instantly the mans stance and posture changed before in a new tone he continued to speak, "Oh wouldn't it be so great to wipe those miserable louts from the face of Eyal. I assume you likely left your forest because you know they were responsible and would like nothing more than to bathe in their blood. Don't most of us all. In due time they will be made to pay in full for for unleashing the Spellblaze on Maj'Eyal."

Cautiously I asked in as angry of a voice as I could muster, "Spellblaze, is that what they call it?" Quickly confirming back to me this he stated "indeed, or so I have been told." Seeing as how the man liked to talk I waited for him to feed me more information "I tell you what, perhaps you should come with me to a little gathering of friends to discuss it. We've got a plan that we will be putting into motion soon to ensure nature never suffers as badly as I'm sure you a thalore can feel it suffer. You see, while the Shaloren are most definitely responsible it isn't like none of the other races knew about their so called grand plan. Every race, save for perhaps the Dwarves, had some knowledge of the Spellblaze."

Obviously the messenger was likely part of whatever group the shalore general had feared. I could tell that the messenger most definitely was in whatever schemes were being orchestrated too, and possibly ones that required secrecy as confirmed from the cloaked man from before. I considered going to his little gathering of friends, but I wasn't really interested in participating in whatever scheme they were going to partake in, and I could sense a feeling of danger as well. "I thank you for the offer, but I must decline" I finally said. To this I got a raised eyebrow as he quickly stated back, "Really, I would think a thalore such as yourself would jump at a chance to exact retribution against any who defile nature as has been done?"

His words made me think for a moment, but I simply got up and left. I remember him calling out that should I change my mind, that I would be 'welcomed as a new initiate for sure'. The sun had begun to set in the sky as I left the building. Figuring I should look for a place to stay for the night I found an inn and purchased a room. I figured that in the morning I would go to the market and buy some food and supplies for my journey home. I slept soundly until early in the morning before the sun had begun to rise when the sounds of screaming filled my ears. Wondering what was going on I looked out the window of my room to see fire and smoke rising from a large building in the distance.
```
译文：
```text
[i]你知道吗，了解一个人真的很难。我很快就发现那个信使就是一个很好的例子。我原来以为他是一个因为遭受了魔法大爆炸而心怀不满的人。实际上，他不仅仅是内心不满，我极大程度上相信他还是那个煽动魔法狩猎的组织的成员。我很确信，他，以及其他追随那个穿着深色斗篷的人类的家伙，因为卷入一场我事后知道的邪恶的阴谋而死。但他是自愿死去的吗？这是我现在真正想知道的关于他的问题。[/i]

吃完了饭，我决定向这个信使打探消息。在他结束最后的激情演说之后，我问道：“那么事情进展如何了？” 他叹了口气，说：“现在纳格尔人似乎控制了一切。他们正在设法为所有涌进城内的难民们搞到足够的食物，甚至为矮人们设法搞到一些酒水。不得不说，看到他们这样做，我有点惊讶。我不知道除了钢铁王座之外，他们在大陆的其他地方是否还有家园。然而，要想真正了解矮人们的隐秘程度是很难的。”

虽然我对矮人们并不是很感兴趣，但最后这句话与我对他们的了解有很大的出入。据我对于矮人的了解，他们全部都生活在钢铁王座，或者至少居住在距离那里很近的城市。我对信使的话表示疑问，他随后解释到：“你现在在这看到的矮人们都住在西边的山里。科纳克人完全不知道矮人们住的距离他们那么近，而且矮人似乎对此保密。不幸的是，他们被迫暴露了自己，因为法师制造的爆炸摧毁了他们的家园。”

对于信使的回答我很满意，我突然会想起今早进城的时候遇到的那个骂骂咧咧的矮人。我在想，那个信使是不是知道一些什么东西。想到这一点，我问道：“你可能还不知道，士兵会没收矮人们携带的物品，知道吗？”信使耸了耸肩，回答道：“他们很可能携带某种，被那些该诅咒的法师很久以前附魔的，带有奥术力量的物品。在这方面，那些矮人们似乎受到了更糟糕的待遇，因为他们一点也不在乎这个物品是否被附魔过。”

他摇了摇头，若有所思的说道：“纳格尔人正积极的试图通过没收魔法物品，作为用来安抚居住在这里的半身人的一种手段。我个人认为任何人携带这样的物品都是非常危险的，包括他们自己。当然了，他们太过于傲慢，以至于他们不会去试图没收住在城里的半身人的魔法物品，指望着他们‘自愿’放弃。实际上，只有矮人、城市外面的半身人难民和我们人类的财产被夺走了。”那个人类说完这些话，就笑了起来。

当一个披着深色斗篷的人走近并弯下身对他说话时，信使停止了大笑。信使对着他回答的人点了点头，并说道：“我随后就到，等我们准备好了之后，再把计划跟我复述一遍。”那个身穿深色斗篷的人鞠了一躬，匆匆地走到了另一张有一对半身人夫妇的桌子，然后又走到一个矮人的桌子旁，再然后就离开这里消失了。那一对半身人夫妇和矮人吃完东西，收拾好行李，也悄悄的离开了。我想知道这个信使到底是谁，我瞥了他一眼，看到他正在用审视的目光看着我。信使用轻松的语气说道：“别理他们，我们谈的这么愉快，别被这些小事打扰了。”

在那一刻，我意识到这个信使比我最初想象的要复杂的多了。我想知道他是不是比我想象的还要危险一点。或许有一点鲁莽，我决定去了解这个男人到底知道多少，然后我轻声问道：“你对永恒精灵有什么想法？”那个信使的立场和姿态立马就变了，随后换了一种口吻继续说：“啊，要是能让把这群可悲的笨蛋彻底从埃亚尔扫除就好了。我想，你离开森林，恐怕就是因为知道他们才是罪魁祸首，准备让他们血债血偿。我们大多数人和你一样，他们终将会为在马基埃亚尔引发魔法大爆炸的行为付出代价。”

我谨慎的尽可能地用愤怒的语气问道：“你们把那个叫做魔法大爆炸？”他快速的肯定了这一说法：“是的，别人都是这样告诉我的。”这个男人看起来很愿意聊天，我等着他吐露更多的消息。“我告诉你，或许你应该和我一起去参加那个小型的朋友聚会，一起讨论这个问题。我们已经有了一个计划，我们会尽快行动，确保大自然不会再遭受和魔法大爆炸一样糟糕的事情，我相信你这个自然精灵一定能够感受到大自然的痛苦不堪。你知道么，永恒精灵他们绝对要对那个事件负责，但是并非其他种族都不知道他们那个所谓的伟大的计划。或许除了矮人，每一个种族都对魔法大爆炸有一定了解。”

很显然，这个信使很可能就是永恒精灵的将军所担心的那个组织的一员。我觉得那个信使一定参与了他们所说的那个计划，不管那个计划是什么。并且，从他与之前来过的穿斗篷的人的对话的反应来看，他们进行的计划还需要保密。我本来考虑去参加他的朋友聚会，但是我又对参与他们精心设计的计划不感兴趣，而且我能嗅到一丝危险的气息。“感谢你的邀请，但是我必须拒绝。”我最终说道。听到这个回答，信使挑了下眉，然后快速回答我：“说真的，像你这样的自然精灵，难道不想抓住任何机会，对玷污自然的人进行报复吗？”

他的话让我想了一会儿，但是我最终站起来，然后离开了。我记得他大声说道，如果我能改变主意，我会被“作为新成员而受到欢迎”。当我离开酒馆时，太阳已经开始落山了。考虑到我应该找一个地方过夜，我找到一个旅店然后开了一个房间。我打算早上的时候去市场买一些食物和补给为回家做准备。我睡得很沉，直到在清晨，太阳还没有升起的时候，我的耳朵里充满了尖叫声。我想知道发生了什么事情，打开了房间的窗户，发现远处的大楼燃起了大火，冒着浓烟。
```

## entry-03528
位置：tome-cults.lua:1268；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 2, Chapter 3] - Blazing Madness
```
译文：
```text
菲·维莉欧斯的冒险 [第2卷，第3章] - 燃烧的疯狂
```

## entry-03529
位置：tome-cults.lua:1298；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 2, Chapter 4] - Despicable Atrocities
```
译文：
```text
菲·维莉欧斯的冒险 [第2卷，第4章] - 卑鄙的暴行
```

## entry-03530
位置：tome-cults.lua:1340；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 2, Chapter 5] - Psionic Trickery
```
译文：
```text
菲·维莉欧斯的冒险 [第2卷，第5章] - 灵能诡计
```

## entry-03531
位置：tome-cults.lua:1341；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i]I'm told that what I likely witnessed in the tent was the result of a psionic slaver. Using my own psyche against me, a manifested image of my own thoughts emerged for which the slaver could use against me. I had been lucky as I had managed to free myself from the slaver's hold, dispelling the image. Had I not done so, it was entirely possible that I could have become enthralled to the slavers will and made to do their bidding unquestioningly.[/i]

I hit the ground hard as I landed towards the back of the tent. Dazed I began to stand to look up at who had thrown me, coming face to face with one of the masked individuals, who I assumed helped take part in the event I had just seen. Slowly a hand reach up to remove the mask, revealing the face of the human messenger. He began to laugh before finally speaking and saying, "Fancy meeting you here, I knew I saw something in you when we conversed in the inn." The messenger laughed some more while I got up. I must have been in a bit of shock from the impact as my vision seemed fuzzy and hazy, while the things in the tent seemingly blurred together. Demandingly I responded to the messenger, “What to you want, why have you thrown me in here?"

The messenger stopped laughing and a calm smile appeared on his face, "Because I would like to have words with you, of course. What were you doing when you came here, when you came to the Nargol Kingdom?" I froze at those words, wondering how much danger I was in. The messenger stood unnaturally silent, his eyes seemingly reading me as thoughts of what to say flew through my mind. I stuttered in fright "I-I was del-livering some med-i-cal aid for th-the Nargols to us-e." A hard blow then struck my face as the messenger slapped me, sending me reeling to the side of the tent. The messenger stated in a raised voice “Indeed," before turning his head to shout at me saying "FROM THE Shaloren!"

Taking a step forward the messenger gave me a hard kick to the stomach, the force winding me and causing me to fall to the ground. I soon received another kick with the back of the heel to my face, causing blood to stream out. Bending down and picking me up by my hair the messenger drew me close to his face, spitting in it with both his saliva and his words, "I had thought better of you since you killed that Eldoral halfling. I figured you might be a fellow ally of nature, but that isn't the case, is it? You made it down to those shaloren, beyond that little wall of magic smoke they put up to hide themselves from us. You could have carried out a small portion of nature's wrath, but instead of enacting nature's fury you turned your back on it AND SIDED WITH THOSE WHO UNLEASHED THE SPELLBLAZE ON US!"

Crying now I was sobbing tears that mixed with the blood coming out of my face. Between sobs I quickly stated, "Enough pain has been felt already without adding to it-" before my head was abruptly smashed into the ground by the messenger. He yelled back "NO AMOUNT OF PAIN, FAY, WILL MAKE UP FOR WHAT THEY HAVE DONE! Every last one of those shaloren deserves to die. To die as painfully as those we burned-." The messenger continued to rant, but hearing my name called I stopped to think, ignoring the rest of what he had to say. How did he know my name? I never gave it to him, to anyone in the Nargol Kingdom, or even any of the shaloren for that matter. "How do you know my name?" I said to the messenger.

His ranting cut off immediately as the messenger looked down at me before replying, "Whatever do you mean Fay, you told me your name back at when, when-." Abruptly the messenger stopped talking, and seemingly the facial expressions seemed to fade away, leaving a faceless humanoid. I didn't know what was going on but knew then this was an imposter. I could feel an anger within me, and with my hand I grabbed whatever it was that I had been talking to. It struggled to keep a hold of me, trying to keep me down, but being closer to the ground I managed to pull it down with me. With my other hand I pulled back and began to punch at its head, until it seemingly faded from existence.

I began to regain vision of my surroundings and looking around I noticed the human with the dark cloak. I quickly realized this was the same human who had briefly visited the messenger when I was talking to him in the inn, as well as the one who stood in the center of the crowd and likely instigated the barbaric display outside. Getting up I said again, "Who are you really?" The figure began to back up in the direction of the tent opening, as if to escape now that I was free of whatever had been done to me. Moving to chase the fiend before he fled out of the tent, I began to run towards the opening. I don't know what happened next but the next moment I found myself face down on the ground.

I was pinned to the ground, unable to move or speak. Attempting to look at what was above me I noticed a halfling, likely the same one that had been standing with the human in the crowd. The human stopped moving away and after a brief moment of surveying the situation came up to stand next to me. As the human hovered over me he stated, "That was quite unexpected, you must have some impressive willpower to resist me thalore. I'm afraid though that if I can't bend you to my will then I am going to have to kill you." As the words trailed off, the human reached with one hand into its cloak, pulling out a small dagger with which I assumed to kill me.

I jostled around attempting to break free of the halfling’s hold, yet somehow despite the halfling’s smaller size than my own I could not break free, and he was doing this with just one arm. Taking the dagger in hand, the human pulled back and then thrust forward to finish me off. I was sure I would be killed, but in the next instant I noticed the dagger tumbling in the air. A bit confused at this, it would take me a moment to realize that the halfling that was holding me down had prevented the human from killing me. Seemingly as confused as me, the human seemingly look at the halfling with disbelief. Finally coming to his senses, the human finally regained his composure to ask the simple question on both of our minds. "What are you doing?"
```
译文：
```text
[i]我听说我在帐篷里看到的可能是一个灵能奴役者。他们能利用我自己的心理对抗我，奴役者创造了一个我的意识构成的形象，用来对付我。我很幸运，因为我设法摆脱了奴役者的控制，驱散了这个形象。如果我没有这样做，我完全有可能被奴役者的意志所吸引，毫无疑问地服从他们的命令。[/i]

我跌入帐篷里，重重地摔在地上。我被撞击搞的头晕目眩，开始站起来抬头看是谁在拉我，发现和我面对面的是其中一个蒙面人，那个蒙面人应该参与了我刚才所目睹的事件。蒙面人慢慢地一只手向上伸去揭开面具，露出了人类信使的脸。他笑了起来，最后开口说：“想不到在这里遇见你，我知道，我们在客栈交谈时，我看到了你身上的某些东西。”我起身时，信使又笑了几声。我的视线一片模糊，帐篷里的东西看起来模糊不清，我想我一定是受到了一些冲击。我问使者说：“你要什么，为什么把我拉到这里？”

信使不再笑了，脸上露出平静的笑容，“因为我当然想和你谈谈。当你来到这里，当你来到纳格尔王国的时候，你在做什么？”我被那些话吓住了，不知道自己有多危险。信使站在那里，不自然地保持沉默，他的眼睛似乎在阅读我的思想，阅读我脑子里闪过的该说什么的念头。我吓得结结巴巴地说：“我——我正在给纳格尔王国送去一些医疗救助。”突然，信使扇了我一巴掌，我的脸受到了沉重的打击，我摇摇晃晃地走到帐篷边上。送信人提高嗓门说：“是的”，然后转过头对我喊道：“从永恒精灵那里来！”

信使向前迈了一步，狠狠地踢了我一下肚子，我因为这股剧痛摔倒在地。他很快又踢了我一脚，脚踩在我的脸上，鲜血向下流出。信使弯下腰来，抓起我的头发，把我拉近他的脸，把唾沫吐在我的脸上，说道：“自从你杀了那个艾德瑞尔半身人，我就更想念你了。我想你可能是大自然的盟友，但事实并非如此，对吧？你到了那些永恒精灵那里，进入了他们为躲避我们而竖起的那堵魔法烟墙。你本可以对他们释放自然的愤怒，但你没有贯彻自然的愤怒，而是背弃了它，你站在了那些导致了魔法大爆炸的人一边！”

我哭着，抽泣着，眼泪和从我脸上流出的血混在一起。我抽泣着说：“他们已经感觉到了足够的痛苦，没有必要对它们施加更多的痛苦了。”然后，我的头突然被信使砸在地上。他喊道：“菲，再多的痛苦也弥补不了他们所做的一切！永恒精灵中的每一个人都应该死。就像我们烧死的人一样，痛苦地死去——”使者继续咆哮，但听到我的名字，我停下来思考，忽略了他要说的其他话。他怎么知道我的名字？我从来没有告诉过他，也没有告诉过纳格尔王国的任何人，甚至没有告诉过永恒精灵中的任何人。“你怎么知道我的名字？”我对信使说。

信使低头看了我一眼，然后回答说：“你是什么意思，菲，你以前告诉过我你的名字，在，在——”信使突然停止说话，他的面部表情消失了，留下了一个面目全非的人形。我不知道发生了什么，但我知道这是个骗子。我能感觉到内心的愤怒，我用手抓住我刚才对话的人。他挣扎着抱住我，试图把我压下去，但由于离地较近，我设法把他拉了下来。我用另一只手往回拉，开始打他的头，直到他消失了。

我开始重新看清周围的环境，环顾四周，我注意到了那个穿着深色斗篷的人类。我很快意识到，这就是我在客栈和信使谈话时短暂拜访过的那个人，也是站在人群中间，很可能是煽动外面的野蛮私刑的那个人。我又站起来说：“你到底是谁？”这个人影开始向帐篷开口的方向后退，好像是要逃走，因为我已经摆脱了他对我所做的一切。在这个恶棍逃出帐篷之前，我想要追他，而向帐篷开口跑去。然而，不知道接下来发生了什么，但下一刻我发现自己脸朝下趴在地上。

我被压在地上，动弹不得，也说不出话来。我试着看看上面的东西，在我身上压着一个半身人，很可能就是和那个人类站在一起蛊惑群众的那个半身人。那个人类停止了移动，调查了一小会儿情况，然后走到我的身边，说道：“这真是出乎意料，你一定有某种令人印象深刻的意志力来抵抗我，自然精灵。但我担心，如果我不能让你服从我的意愿，我就不得不杀了你。”当说完这句话后，那个人类一只手伸进斗篷，拔出一把小匕首，我想是用来杀我的。

我推推搡搡着试图挣脱半身人的束缚，但不知怎么的，尽管半身人比我自己的体型小，我还是无法挣脱，而他只用一只胳膊就固定住了我。那个人类拿着匕首向后，接着向前刺去，准备把我杀掉。我确信自己很快就要丧命了，但在接下来的一瞬间，我发现匕首弹飞出去，在空中翻滚。困惑许久，我才意识到，那个压着我的半身人阻止了人类杀死我。人类不相信地看着半身人，似乎和我一样困惑。终于，他恢复了镇定，醒悟过来，问了我们两个心里共同的问题。“你在干什么？”
```

## entry-03532
位置：tome-cults.lua:1374；section：tome-cults/data/lore/fay-willows.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Escapades of Fay Willows [Book 2, Chapter 6] - Spared
```
译文：
```text
菲·维莉欧斯的冒险 [第2卷，第6章] - 死里逃生
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Drem	德瑞姆	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Dwarf	矮人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Krog	克罗格	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
Thrall	奴仆	T.GAME.EFFECT	combat	_t	preferred	core	精神支配后目标的状态身份；与 Mental Domination“精神控制”能力名区分
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
book	书	T.GAME.ENTITY	items	entity type	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
corruption	堕落	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
drem	德瑞姆	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
dwarf	矮人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flat	固定伤害减免	T.GAME.EFFECT	combat	effect subtype	preferred	global	flat damage reduction 机制；与正文'固定伤害减免'一致（P0 复审子代理 #83，用户确认）
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
iron throne	钢铁王座	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
krog	克罗格	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
krog	克罗格	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
maggot	蛆虫	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
manasurge rune	法力涌动符文	T.GAME.ENTITY	items	entity name	preferred	core	物品实体名称；与 Manasurge 技能名统一
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mechanical	机械	T.GAME.ENTITY	creatures	entity type	existing	dlc	Embers of Rage 实体类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
nether	彼世	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
radiant horror	光芒恐魔	T.GAME.ENTITY	creatures	entity name	preferred	core	核心实体名称；与 1.8beta 的实体译法一致，描述性复数文本仍按语境处理
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
slaver	奴隶贩子	T.NARRATIVE.LORE	narrative	_t	preferred	core	鲜血之环语境中的奴隶贩子；与被奴役者 slave“奴隶”区分。entity name 标签下译文曾作“奴隶商”，裁决统一为“奴隶贩子”
slavers	奴隶贩子	T.NARRATIVE.LORE	narrative	_t	preferred	core	鲜血之环语境中的奴隶贩子复数；与被奴役者 slaves“奴隶”区分
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
tentacles	触手	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
```
