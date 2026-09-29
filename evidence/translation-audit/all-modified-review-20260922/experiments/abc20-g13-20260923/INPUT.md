# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03653–entry-03692 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g13-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03653 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03653
位置：tome-cults.lua:3802；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Slowly transfered to a Forbidden Tome.
```
译文：
```text
正在被缓慢转移到禁忌之书。
```

## entry-03654
位置：tome-cults.lua:3832；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reduces all damage taken by %d%% and remove all detrimental effects on application.
```
译文：
```text
降低所有受到的伤害 %d%%。施加该效果的时候会解除所有负面效果。
```

## entry-03655
位置：tome-cults.lua:3845；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is starting to get mad (%d stacks), reducing mind damage resistance by %d%%, mental save by %d, confusion resistance by %d%%, generating %0.1f insanity per turn.
```
译文：
```text
目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，%d%% 混乱免疫，每回合获得 %0.1f 疯狂值。
```

## entry-03656
位置：tome-cults.lua:3865；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s body is evolved!
```
译文：
```text
#Target#的身体进化了！
```

## entry-03657
位置：tome-cults.lua:3875；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is enveloped with entropic forces!
```
译文：
```text
#Target#被熵能覆盖！
```

## entry-03658
位置：tome-cults.lua:3880；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is bolstered at the sight of the horror!
```
译文：
```text
#Target#在恐魔的视线中被强化了！
```

## entry-03659
位置：tome-cults.lua:3929；section：tome-cults/data/zones/entropic-void/grids.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The rift leads... somewhere.
```
译文：
```text
裂缝通向…某个地方。
```

## entry-03660
位置：tome-cults.lua:3975；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Training dummy. Use it to train.
```
译文：
```text
训练用傀儡。用它来训练吧。
```

## entry-03661
位置：tome-cults.lua:3979；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A human student.
```
译文：
```text
一个人类学徒。
```

## entry-03662
位置：tome-cults.lua:3982；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A shalore student.
```
译文：
```text
一个永恒精灵学徒。
```

## entry-03663
位置：tome-cults.lua:3985；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A halfling student.
```
译文：
```text
一个半身人学徒。
```

## entry-03664
位置：tome-cults.lua:4026；section：tome-cults/data/zones/ft-haze-cave/grids.lua；source_tag：say；args_order：None；special：None

原文：
```text
#YELLOW#You hear a terrible shriek.
```
译文：
```text
#YELLOW#你听到了一声可怕的尖叫。
```

## entry-03665
位置：tome-cults.lua:4035；section：tome-cults/data/zones/ft-haze-cave/npcs.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
Grung made great being angry!
```
译文：
```text
格朗格激怒了伟大的存在！
```

## entry-03666
位置：tome-cults.lua:4088；section：tome-cults/data/zones/ft-haze-cave/zone.lua；source_tag：log；args_order：None；special：None

原文：
```text
#ANTIQUE_WHITE#Grung: %s
```
译文：
```text
#ANTIQUE_WHITE#格朗格：%s
```

## entry-03667
位置：tome-cults.lua:4097；section：tome-cults/data/zones/ft-home/grids.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You can leave items here for safekeeping.
```
译文：
```text
你可以把物品安全地留在这里。
```

## entry-03668
位置：tome-cults.lua:4141；section：tome-cults/data/zones/ft-horrors/objects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A page of the tome.
```
译文：
```text
书页。
```

## entry-03669
位置：tome-cults.lua:4194；section：tome-cults/data/zones/ft-illusory-castle/grids.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#GOLD#An object rolls from the chest!
```
译文：
```text
#GOLD#一件物品从宝箱中掉了出来！
```

## entry-03670
位置：tome-cults.lua:4297；section：tome-cults/data/zones/ft-illusory-castle/zone.lua；source_tag：log；args_order：None；special：None

原文：
```text
#%s#Welcome to chapter "%s"!
```
译文：
```text
#%s#欢迎来到章节 "%s"！
```

## entry-03671
位置：tome-cults.lua:4308；section：tome-cults/data/zones/ft-yaech/grids.lua；source_tag：say；args_order：None；special：None

原文：
```text
#YELLOW#You hear a terrible shriek.
```
译文：
```text
#YELLOW#你听到了一声可怕的尖叫。
```

## entry-03672
位置：tome-cults.lua:4360；section：tome-cults/data/zones/godfeaster/zone.lua；source_tag：say；args_order：None；special：None

原文：
```text
#OLIVE_DRAB#You can feel tremors in the worm.. A gastric wave is coming! Dodge to an alcove!
```
译文：
```text
#OLIVE_DRAB#你能感觉到虫子在颤抖……一波胃液来了！躲进凹室！
```

## entry-03673
位置：tome-cults.lua:4483；section：tome-cults/data/zones/test/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Swordsmith
```
译文：
```text
铸剑铺
```

## entry-03674
位置：tome-cults.lua:4484；section：tome-cults/data/zones/test/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Nature's Punch
```
译文：
```text
自然的重击
```

## entry-03675
位置：tome-cults.lua:4487；section：tome-cults/data/zones/test/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Night's Star
```
译文：
```text
暗夜之星
```

## entry-03676
位置：tome-cults.lua:4514；section：tome-cults/data/zones/town-kroshkkur/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Destroy @himher@!
```
译文：
```text
摧毁@himher@！
```

## entry-03677
位置：tome-cults.lua:4516；section：tome-cults/data/zones/town-kroshkkur/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A drem cultist.
```
译文：
```text
一位德瑞姆邪教徒。
```

## entry-03678
位置：tome-cults.lua:4544；section：tome-cults/data/zones/town-kroshkkur/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Swordsmith
```
译文：
```text
铸剑铺
```

## entry-03679
位置：tome-cults.lua:4545；section：tome-cults/data/zones/town-kroshkkur/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Nature's Punch
```
译文：
```text
自然的重击
```

## entry-03680
位置：tome-cults.lua:4548；section：tome-cults/data/zones/town-kroshkkur/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Night's Star
```
译文：
```text
暗夜之星
```

## entry-03681
位置：tome-cults.lua:4559；section：tome-cults/hooks/bonestaff.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GREY##{italic}#You feel the bones of the staff creeking and vibrating in your hand.#{normal}##LAST# Yes... #{italic}#"master"#{normal}#.
```
译文：
```text
#GREY##{italic}#你感受到手中的骨杖在你的手上颤动：#{normal}##LAST# 是的……#{italic}#“主人”#{normal}#。
```

## entry-03682
位置：tome-cults.lua:4595；section：tome-cults/hooks/bonestaff.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Great!
```
译文：
```text
太棒了！
```

## entry-03683
位置：tome-cults.lua:4596；section：tome-cults/hooks/bonestaff.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GREY##{italic}#The staff stays calm.#{normal}##LAST# Stupid useless pathetic excuse of a #{italic}#"necromancer"#{normal}#! Why refuse to use true power?!
```
译文：
```text
#GREY##{italic}#法杖平静了下来。#{normal}##LAST#像你这样的#{italic}#"死灵法师"#{normal}#竟然会用这样蹩脚的借口！为什么要拒绝使用真正的力量？！
```

## entry-03684
位置：tome-cults.lua:4614；section：tome-cults/overload/data/texts/intro-cults.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome #LIGHT_GREEN#@name@#WHITE#.
You are one of several like-minded individuals that delves into knowledge long lost and forgotten, seeking sanctuary from an outside hostile world to such activities. Delving into research within the forgotten and inactive fortress of Kroshkkur, the reasons of pursuit differ among a myriad of topics. Some look to uncover knowledge hailing back to the Age of Haze when beings immensely powerful walked Eyal, while others explore the origins of themselves and other races.

Regardless of the subject or method of research, no rules exist to constrain anyone in their approach. This has led to experimentation into what many would deem mad and certainly forbidden among the surface dwellers. If Kroshkkur were to be found it would most certainly be destroyed. Therefore the only rules that truly exist in the sanctuary are that of secrecy and safeguarding the accrued knowledge that has been obtained therein.

But today the sanctuary is threatened by a giant worm that is tunneling directly towards Kroshkkur. If nothing is done it will collide with and destroy what remains of the ancient fortress. One idea to dealing with the worm is for someone to teleport inside it and make there way towards the worms brain cluster and destroy it. Alternatively, you consider leaving before the worm arrives and finding your own purpose in the outside world.

As with all things here, nothing restrains you in what path you #{bold}#ultimately choose#{normal}#. The question is whether you step into the #{bold}#portal to teleport into the worm#{normal}# or leave now while it is safe to do so and let #{bold}#Kroshkkur be destroyed#{normal}#.

```
译文：
```text
欢迎 #LIGHT_GREEN#@name@#WHITE#。
你是一群钻研那些丢失遗忘已久的知识的志同道合者之一。在这个对这些知识并不友好的世界，你们找到了一个避难所。在被遗忘的废弃堡垒克诺什库尔，你们基于自己的理由追寻禁忌的知识。有些人希望解开过去的阴影，了解到有关无比强大的古代生物在埃亚尔行走的混沌纪的过去，而有些人则孜孜探索自己和其他种族的起源。

在这里，没有任何规则限制任何人，不管你研究的主题和方法是什么。这导致了对许多地表人视为疯狂且被禁止之事的实验，而你们的研究内容也被普通人的社会所禁止。如果克诺什库尔被发现，它一定会被摧毁。因此，在避难所的唯一规则就是必须对在里面学到的知识进行严格的保密和保护。

然而今天，避难所却面临着一条直接冲向克诺什库尔的巨型蠕虫的威胁。如果再不迅速做出决断，它将会直接撞向并摧毁古代堡垒的残骸。有一个击败蠕虫的办法，那就是将某一个人传送到蠕虫体内，让他前往蠕虫的脑簇所在之处，将其摧毁。或者，你也可以考虑在蠕虫到来之前离开，在外面的世界找到你自己的目的。

就像这里的一切一样，没有人会干涉#{bold}#你自己的选择#{normal}#。你可以现在#{bold}#踏入通向巨型蠕虫体内的传送门#{normal}#或者就这样离开#{bold}#任由克诺什库尔被巨型蠕虫摧毁#{normal}#。

```

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

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cultist of Entropy	熵教徒	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业
Demented	疯狂系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业类别名
Drem	德瑞姆	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Frenzy	狂热	T.GAME.TALENT	talents	talent name	existing	global	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Krog	克罗格	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Swordsmith	长剑铁匠铺	T.GAME.ENTITY	places	entity name	existing	core	城镇商店实体
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
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
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
demented	疯狂	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
drem	德瑞姆	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
entropy	熵	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
entropy	熵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
frenzy	狂乱	T.GAME.EFFECT	combat	effect subtype	existing	global	与技能名 Frenzy 的译法区分
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
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
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
tentacles	触手	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
