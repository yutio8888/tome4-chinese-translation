# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03373–entry-03412 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g06-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03373 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03373
位置：tome-ashes-urhrok.lua:518；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Though they retain use of their hands, this altered offshoot of the Fire Imp has made a much more powerful sacrifice: the ability to breathe air.  Most of the dominant species of Eyal reside above the water, making its oceans and lakes a prime location for carrying out covert operations, conducting experiments too dangerous to perform on our own soil, and preparing portals for a full-scale invasion.  As our scouts and servants beneath the seas, water imps forego the fire-slinging abilities shared by their brethren, instead focusing on ice-magic that is similarly effective underwater.  Like a wretchling, a Water Imp does not expect to live to see peacetime, and thus has no need to breathe above the surface.  Remember to pay tribute to the Water Imp whenever you can; since they do not fight alongside our land-based forces, it's all too easy to forget the selfless sacrifices they've made, and their enormous contributions in gathering intelligence and setting up remote bases.
```
译文：
```text
尽管他们依旧使用双手作战，这群变种的火魔婴做出了更加伟大的牺牲：他们放弃了呼吸空气的能力。大部分占据主导地位的埃亚尔种族生活在水上，让海洋和湖泊成为我们的藏身的主要根据地，实施那些对于我们的土壤来说过于危险的实验，同时为制造全面侵略的传送门做准备。作为我们在海里的使者，小水怪们放弃了同胞们使用火焰的能力，转而使用在水里同样有效的冰系法术。和酸液树魔类似，小水怪们并不指望能活到和平到来，因此没有必要在地表呼吸。请记得随时为小水怪们奉上礼物，不能因为他们没有同大家在地表作战，就轻易遗忘他们做出的无私牺牲，以及在收集情报和建立远方基地方面做出的巨大贡献。
```

## entry-03374
位置：tome-ashes-urhrok.lua:520；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Clever and tough, the engineers and warriors of our kind, making armor for our forces and holding the front lines against the hordes of Eyal.  While the children of ruby study new magical spells for our arsenal, and the children of emerald study ways to make our own bodies deadlier, the children of onyx focus on making new constructs from scratch, lashing flesh, magic, and steel together into towering creations that strike fear into Eyal.  Those who fight on the front lines have been created to do so rather than born, churned out in a semi-mature state by factories with Forge-Giant-produced armor bolted onto their skin at "birth."  Though they are mostly flesh, the warrior onyx known as Quasits are very much machines, made with bolstered muscles without losing the clever minds they come from.  As eager as they are brilliant, Quasits are well-disciplined and capable in combat, and their armor allows them to easily take blows that would devastate a Wretchling or Fire Imp.  Devotion will get us far on its own, but the Quasit shows how much more we can do when we have fervor and patience working hand-in-hand.
```
译文：
```text
聪明而顽强，我们中的工程师与战士，为我们制造护甲，同时奋战在埃亚尔边界前线。红宝石的孩子们学习兵工厂新的魔法，绿翡翠的孩子们学习令身躯更加致命的技巧，而玛瑙色的孩子们专心学习新的构架体，将魔法、血肉和钢铁融为一体，在埃亚尔大陆制造恐惧。那些奋战在前线的，与其说是生出来，不如说是制造出来——在工厂里由半成熟态大量炮制，一“出生”就身着锻造巨人亲制的护甲。尽管仍是血肉之躯，玛瑙战士——或者说夸塞魔——有着钢铁般的纪律和强大的近战能力，同时他们的护甲能抵抗重击，即使那重击能轻易毁灭一只酸液树魔或者火魔婴。奉献让我们向前迈进，但夸塞魔展示出，当我们拥有热情和耐心携手并进时，我们将走得更远。
```

## entry-03375
位置：tome-ashes-urhrok.lua:540；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The modified children of emerald, known as the Wretchlings, willingly accept their role as the arrows in Urh'Rok's quiver, and most only live to see a couple of engagements before giving their lives in battle.  Once in a great while, though, one will stand toe-to-toe with the enemy and repeatedly come out on top.  These outstanding fighters, chosen by fate and their own talent, are recalled, then put through a series of tests to ensure that their survival was not due to luck alone.  Roughly 70% of these are then assigned to breeding duties, ensuring that the Wretchling bloodline gets ever stronger as it is forged in the fires of combat; the rest, whether due to sterility, consuming too much resources to sustain their brood, or simply insisting on staying in the fights for which they were created, are nurtured to maturity and once again let loose on the battlefield.  If wretchlings are our arrows, wretch titans are our trebuchet boulders, causing a tremendous amount of damage to the enemy line with their incredible strength and the geysers of acid spurting from their flesh.  Although no less aggressive than their younger counterparts, wretch titans generally have a much higher survival rate, due to not only their formidable power and size, but the sheer terror they cause when charging at the enemy - few Eyalites would stand and fight against such a foe, particularly when it means standing in a rapidly-growing pool of acid.
```
译文：
```text
绿翡翠的孩子们，酸液树魔，愉快地接受了作为乌鲁洛克之箭的身份，大部分在战死前都只能见证几次战斗。但少数情况下，也会有个体在面对面的厮杀中取得持续的胜利。这些卓越的被命运和他们自身天赋选定的近战专家，将被召回做检测，以确保并非是全然的幸运令其生存。其中约 70% 会被指派承担繁殖任务，让酸液树魔的血统在战火熔炉中不断变得更加强壮；其余的，不论是因为无法生育、消耗过多资源喂养后代，还是坚持留在为之而生的战场上，都会被培育成熟后再次放回战场。如果说酸液树魔是我们的箭矢，那么腐化泰坦就是投石机抛出的巨石，以不可思议的力量和从血肉中喷涌的酸液对敌军战线造成巨大破坏。他们不比酸液树魔杀伤力小，同时生存率要高得多——这不仅仅是因为他们的力量和体积，更是因为他们面对敌人时制造的恐惧——几乎无人能站在他们面前肉搏，尤其是在地表上有不断扩张的强酸池时。
```

## entry-03376
位置：tome-ashes-urhrok.lua:542；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A walking monument to times of prosperity, the dolleg was once a beast of burden, carrying loads of trade goods through the Sher'Tul portals.  Reliable, friendly, and rather intelligent for a beast, dollegs were often taken in as beloved pets as well - their joyous chirps when seeing their master get home could brighten up anyone's day, and despite their large size they were gentle enough to play with our young.  Their kind temperament and dutiful labor were the pride of our breeding practices, and two-thirds of our population either owned, lived in a home with, or worked with a dolleg.  In the wake of Mal'Rok's destruction, the children of emerald developed an effective process to convert these companions into beasts of war, covered in acidic spines and thick plating, and loyally tearing through our enemies with incredible force.  Unfortunately, their friendly demeanor was lost in order to make them merciless in combat; of all the sacrifices we've had to make for our war, it might be the loss of our gentle companions that troubles us the most.
```
译文：
```text
活着的繁荣纪念碑——多雷格曾是负重的野兽，身载货物经过夏·图尔传送门。可信，友善，同时比野兽更有智力，多雷格也一度充当爱宠——当看见主人回家时他们发出的欢鸣能让人快活一整天，同时，尽管体型庞大，他们动作却十分温柔，和孩子们玩耍时也不必担心。他们温和的脾性与本分的劳作是我们繁衍中的荣耀，三分之二的人在生活中都有一只多雷格陪伴，一起工作或者生活。在玛·洛克毁灭后，绿翡翠的孩子们发明了一种有效的方法将多雷格转化为战争巨兽，身躯被酸刺与厚甲覆盖，忠诚驱使他们以巨力猛冲向敌人。不幸的是，他们温和的举止在培育其无情战斗的能力时丧失殆尽；尽数我们为战争作出的牺牲，失去温柔伙伴可能是最大、也是最困扰我们的一项。
```

## entry-03377
位置：tome-ashes-urhrok.lua:544；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The minotaur is one of Eyal's more interesting creatures, and a good example of the devious designs the Sher'Tul had in mind while creating or altering Eyal's races.  Its instincts draw it toward narrow corridors, twisted passages, magical artifacts, and surges of magical energy, resulting in horned beast-men frequently blundering their way into our bases and encampments.  They also seem to soak up empowering magic very readily, and alter their forms accordingly - a typical minotaur is no match for our forces, but occasionally blight will mutate one into an extremely dangerous horror.  Said blighted forms are too unstable for use among our ranks, but with some effort by the children of emerald and ruby, we can give one the gifts of massively increased strength and the ability to unleash waves of flame on our enemies.  While we currently need to keep most of them enthralled to ensure their loyalty, we've recently begun breeding minotaurs on our continent so we can train them from birth to know our cause of righteous revenge - and already some wandering minotaurs accept our cause and our blessings willingly!  It seems the natives of Eyal are no kinder to their own brethren than they are to us.
```
译文：
```text
米诺陶是埃亚尔大陆上颇为神奇的生物，同时也是夏·图尔人制造或者改变埃亚尔种族的一个绝妙的例子。它的本能驱使它走向狭窄的走廊、曲折的通道、魔法神器和魔法能量的涌动之处，结果这些长角的兽人经常误打误撞闯入我们的基地和营地。它们也很容易吸收强化魔法并随之改变形态——普通的米诺陶根本不是我军对手，但偶尔枯萎之力会将其中一只变异成极其危险的恐魔。这些枯萎形态不够稳定，不能为我们所用，但经过红宝石和绿翡翠的孩子们的努力后，我们能将无比的力量与释放火焰的能力赋予之。我们现在不得不奴役它们中的大部分以确保忠诚，同时最近我们也开始在我们的大陆上饲养米诺陶，这样我们就能从小灌输我们正义的复仇——已经有部分米诺陶自愿接受了我们的理由和祝福！似乎埃亚尔的原住民对其同胞也并不比对我们友善。
```

## entry-03378
位置：tome-ashes-urhrok.lua:548；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The Divine Tournament of Combat is the most straightforward of our competitions for the spectator, but those competing have a huge variety of possible divisions to enter.  Most are based on the maximum amount of energy consumed by their entrants since (and including) birth; others include those set in an open field for direct combat, or a difficult-to-navigate forest of pillars to properly evaluate those who use hit-and-run tactics or excel at setting up or detecting ambushes.  In the high-energy divisions, those competing are typically not born in the conventional manner, usually being constructs made by a team performing a collaborative effort.  The constructs we now call Champions of Urh'Rok have utterly devastated most of the high-energy open-field divisions, while performing adequately in the less-direct ones, making them a solid fit for production and deployment in the invasion.  Their development team has earned a place of honor for their ingenious methods of creating such incredible strength with a sustainable amount of energy-input, and once mass-production is in order, these gigantic creatures will become the backbone of our military.  Once they arrive on the surface, Eyal will experience a few fleeting moments of terror before their utter annihilation.
```
译文：
```text
神圣战斗锦标赛是对我们的观众来说最为熟悉的比赛，然而有些人不知道的是，这场锦标赛有非常多的组别。大部分的组别划分来自于选手从出生开始所消耗的能量，而其他的一些分类方法包括在开放场地的直接战斗，亦或是在难以辨认方向的复杂迷宫里进行，以选拔那些能够灵活地使用游击战术、精巧的发动和判别突袭的选手。在最高能量的组别，那些挑战者并不是正常出生的天才，而是在各个比赛有关的研究团队团结合作，精心设计的产物。这些造物现在被我们称为乌鲁洛克的精英卫兵，他们在高能组的开放场地直接战斗领域几乎所向披靡，在其他复杂的环境下也有相当出色的表现，让他们可以在未来侵略部队的组成和部署中发挥极大的作用。制造他们的研究团队为他们的伟大创造——通过很少的能量就能创造拥有如此强大力量的造物——获得了崇高的赞誉。这些巨大的怪物将会成为我们军队的中流砥柱。只要他们组成的军队成批到达埃亚尔，那些弱小的生物瞬间就会被他们强大的力量彻底歼灭。
```

## entry-03379
位置：tome-ashes-urhrok.lua:550；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The power of Urh'Rok cannot be overstated, except by claiming it to be infinite.  Most of his strength and will are occupied at the moment, keeping our shattered home from splintering off into the void; as such, he cannot spend time or effort making equipment for our army.  The children of onyx recognized this, and worked on a way to maximize the amount of benefit they could get from a small portion of his power; Urh'Rok was pleased by their idea, and granted their request in full, giving them a handful of enormous hammers, each one glowing with his magic.  These were then given to modified variants of the Champion of Urh'Rok template, built for raw strength at the expense of speed and energy-efficient creation, and now they work tirelessly, heating raw metal with their magic until it is workable, then pounding it into their shape, automatically imbuing the resulting armor and weaponry with Urh'Rok's blessing.  Thanks to an assortment of detachable heads for these hammers, every single swing produces several pieces of usable equipment.  The constant exposure to the power of Urh'Rok has made these creatures almost absurdly formidable, but as useful as they would be on the front lines, they are even more useful bolstering the rest of our forces with blessed equipment; that said, should our scouting parties encounter a problem that requires drastic and immediate intervention, sending a Forge-Giant down is a reliable emergency option, and would immediately clear up any combat-related difficulties should the situation call for it.
```
译文：
```text
要说怎么形容乌鲁洛克大人的强大能力的话，没有什么词语比“无穷无尽”更加合适了。不过不幸的是，由于他大部分的力量和意志都被用于凝聚我们被炸得支离破碎的土地，不让其飞散到无尽虚空之中；他或许没有足够的时间和精力来为我们的部队制造装备。缟玛瑙之子们意识到了这个问题，找到了一种从父亲大人的强大力量中的一小部分最大程度地发挥的方法。乌鲁洛克大人认可了他们的提议，制造了一些灌注了他强大魔法力量的巨锤。这些赠礼被带给一些被改造的乌鲁洛克精英卫兵，以牺牲一定行动速度和能量燃率的代价，他们获得了无与伦比的强大蛮力。他们日夜不停地工作，将金属的原材料用魔法熔炼，然后将其导入模具中，自动锻造成注入了乌鲁洛克的祝福的魔钢武器和护甲。在各种可拆卸的锤头的帮助下，只要一击就能瞬间制造出数个装备零件。长期暴露在乌鲁洛克的强大力量下，这些生物拥有可畏的强大力量。然而，与在前线作战相比，他们更应该留在这里为我们的部队送去支援的装备。因而，只有在我们的先遣部队遇到需要立即强大的武力介入的危急时刻，我们才会向下遣送锻造巨人，他们强大的力量将会立即扫清战斗中所面临的一切困难。
```

## entry-03380
位置：tome-ashes-urhrok.lua:552；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Thanks to numerous contacts we have on Eyal's surface, ranging from easily-duped natives to our own scouting teams, we've managed to gain a few captive Eyalites.  These prisoners are useful for a variety of tasks, including manual labor, magical research, stress relief, and developing new methods of torture (those last two often being one in the same).  We try to preserve these temporarily-valuable subjects for as long as we can, but invariably, an experiment goes wrong or someone uses too much force, and the captive ends up mortally wounded.  Rather than let these world-breakers escape their eternal fate by simply dying, we put their bodies and life-essence to use, combining several fallen Eyalites into a creature held together by their collective rage and suffering.  You'd think this would be a bad idea to have walking around our base of operations, but as it turns out, it just takes a few simple enchantments to redirect their vengeful instincts towards their former brethren, making them fearsome and sadistic in combat.  Their rampages against their "tormentors" are simply hilarious!
```
译文：
```text
源于我们对埃亚尔大陆的多次接触，从容易受骗的当地傻瓜到我们有组织的探险队，我们有机会活捉了一些埃亚尔人。这些俘虏能够用于许多工作，比如苦力、魔法研究、找乐子，以及发明新的酷刑（后两者通常是同一回事）。我们曾经试图长期保存这些暂时还是比较珍贵的样本。不过每一次，只要实验出了点问题，或者有谁下手的时候稍微没有掌握好力度，这些样本就会当场惨死。对于这些破坏世界的邪徒来说，让他们通过死亡逃离自己永恒折磨的命运实在是太便宜他们了。我们把他们的肢体和生命精华取出，用他们的愤怒和痛苦将几个埃亚尔人的尸体拼接在一起。你或许觉得让他们在我们的指挥部附近晃来晃去是个坏主意，不过事实证明，只需要几个简单的魔法就可以把他们复仇的强烈冲动转移到他们曾经的同族身上，让他们在战斗中变得施虐成性、令人望而生畏。看看他们在狂乱中屠杀自己眼中的“敌人”的样子，还真是让人忍俊不禁！
```

## entry-03381
位置：tome-ashes-urhrok.lua:554；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#This plaque is mostly covered in shifting shadows.  You can only make out a little bit of the text.#{normal}#

#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#heregs are not the only way we recycle #927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#arness their fear and suspici#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#outs.  Cautious and yet sadistic, these assassins #927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#markably effective in indirect combat, setting ambus#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#justice.  Additionally, the shadows they produce #927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#spionage, scouting, and #927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#king them a val#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#tion to our intel-gathering camps. Redee#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST# data they contribute on#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST# paving the way for our invasion.

#{italic}#As you reach the end, the text goes completely black, and a new message forms.#{normal}#

#{bold}#WE SEE YOU.#{normal}#
```
译文：
```text
#{italic}#上面的文字被浮动的阴影所笼罩，你只能依稀看到模糊的文字碎片#{normal}#

#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～~#LAST#希瑞格并不是我们回收#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～#LAST#卸下他们的恐惧和怀#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～#LAST#。他们已经变得谨慎，然而仍然足够施虐成性，这些暗夜的杀手#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～~ ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～#LAST#他们卓越的表现在非直接战斗，尤其是发动突#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～#LAST#义。另外，他们制造的黑暗之雾#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～~#LAST#间谍活动，侦察活动，以及#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～~#LAST#给他们一个#927e64#～～～～～～～～～～～～～～～#LAST#息提供给了我们的情报机构。为了偿#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～~#LAST#他们提供的数据被用#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～~#LAST#为我们最终的侵略铺平了道路。

#{italic}#当你看到最后，上面的文字一下子笼罩在完全的黑暗之中，一行新的消息浮现出来#{normal}#

#{bold}#我们正看着你。#{normal}#
```

## entry-03382
位置：tome-ashes-urhrok.lua:568；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The onslaught of the Sher'Tul portals never truly stopped.  Magic still pours from them, threatening to do even more damage to our home; it would be completely destroyed by now, if not for our Father.  Part of his work to keep Mal'Rok structurally intact is to blow great gusts across the devastated land, forcing the ravenous flames back into the portal network from whence they came.  It would seem, though, that the flames took souvenirs with them; our scouting parties have noted that Sher'Tul portals on Eyal, even those which have been completely deactivated, will occasionally emit a shade of one of our fallen citizens, imbued by some of Urh'Rok's power, smelling of Mal'Rok's ashes, and warped to insanity by its transit through the unstable rifts.  While this is a troubling revalation of the true horror of the Sher'Tul weapons, telling us that even now our fallen cannot rest in peace, the fact that they are arriving on Eyal in defiance of the shield is some consolation, as it means that those most wronged by the betrayal can claim their revenge personally.
```
译文：
```text
夏·图尔传送门的影响从未停止。直到现在，奥术能量仍然在从中向外散溢而出，威胁着对我们的故乡做出更大的破坏；如果不是我们父亲大人的能力，恐怕我们的故乡早已经被其完全毁坏。他保持玛·洛克结构稳定的一个重要过程是在荒芜的土地上吹起狂暴的怒风，将饥渴的热焰吹回传送门的网络之中。然而，我们发现，这些烈火即使走时也要从我们的故乡掠夺些东西才肯返回。我们的埃亚尔探险队记录了在埃亚尔发现的夏·图尔传送门附近经常徘徊着我们牺牲同胞的灵魂——即使是那些已经关闭的传送门也不例外。他们被乌鲁洛克的力量所浸染，被玛·洛克的灰烬所环绕，在穿梭时空裂缝的过程中被折磨地几近疯狂。这昭示着有关夏·图尔人邪恶武器的恐怖力量，告诉我们即使是那些逝者在他们的折磨下也不得安眠。然而，他们绕过环绕埃亚尔的护盾到达星球表面的事实也给我们带来了些许慰藉，这些在夏·图尔人阴毒背叛的惨剧中受害的无辜者终于有机会亲自复仇了。
```

## entry-03383
位置：tome-ashes-urhrok.lua:570；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Teleportation is one of the most crucial areas of magical research to our cause of revenge; until we break the Sher'Tul-made shield surrounding Eyal, it will remain our only means of reaching the surface.  One of our leading scholars, a child of onyx known as Draebor, has perfected short-range teleportation and has been studying methods to work his skills into a mass-producible artifact to grant this ability to all of our troops.  He's kept his work under wraps as of late, but rumor has it that he's been reverse-engineering the Sher'Tul portals, letting our invasion get through via their own weapons.  Whatever he's up to, keep an eye out - big things are just around the corner, courtesy of his dedicated research!
```
译文：
```text
传送术是完成我们复仇行动的重要研究领域。在我们打破围绕埃亚尔大陆的夏·图尔之盾之前，传送术将是我们达到大陆表面唯一的手段。我们的领军学者之一—缟玛瑙之子德瑞宝——掌握着完美的短距传送术，并且一直在研究方案将他的技术融入工艺品并量产化，使我们的军队都具备这样的能力。他一直将研究的进程保密，但是有谣言说他正在反向驱动夏·图尔的传送门，让我们通过夏·图尔的武器发动侵略。无论他做到哪一步，我们都要拭目以待——多亏了他的专注的研究，即将有重大的事件发生！
```

## entry-03384
位置：tome-ashes-urhrok.lua:572；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Once a naturalist and explorer, this scholar frequently made trips to Eyal in the period before Mal'Rok's destruction.  Her journals about a wide assortment of curious species living in the shadow of the Sher'Tul were a delightful read for our citizens, and she had a genuine love for these pitiable, uncivilized creatures.  She, along with two of her companions, were trapped on Eyal when the portal network was destroyed; for a long time, she was feared dead, or worse, turned traitor and working with the natives against her old home.  In any case, it was assumed she would have expired of old age by the time we arrived in orbit around the planet.  Once we got there, though, something curious happened: by magic we still haven't been able to reverse-engineer, a handful of Eyalites dressed in strange robes appeared on our continent, proclaiming devotion to Shasshhiy'Kaish and wishing to be subjected to our experiments.  Ever since then, batches of these willing captives have been delivered with great regularity.  Sadly, they have not been as great a boon to our research as this would sound - all of them appear with nearly every shred of their essence drained, leaving them on the edge of death, and that's not counting the frequent cases of internal bleeding and the rare occasion of them appearing with a rewired nervous system that perceives pain as pleasure, frustrating our attempts to create better methods of punishment.  Nonetheless, they are both cooperative and plentiful, and have been quite helpful.  We cannot be sure that Shasshhiy'Kaish herself is still alive, but if she is, we can be sure her allegiances are with our cause.

#{italic}#A short message is etched below the main text.#{normal}#

Cute.  I'll let it stay.  
-S.

```
译文：
```text
作为一名博物学者和探险家，这位学者经常在玛·洛克毁灭前的日子里到埃亚尔大陆旅行。她在旅行日志中记载了栖息于夏·图尔人阴影中种类繁多的神奇生物，我们的市民们都乐于阅读这些作品。她对这些可怜、未开化的生物有一种由衷的热爱。当传送门网络被摧毁的时候，她和另外两名同伴被困于埃亚尔大陆。很长一段时间里，大家都担心她死了，或者更糟——成为一名叛徒并与埃亚尔的居民们一同反抗她的家乡。不管哪种情况，当我们进入这颗星球的轨道时，她应当已经死于衰老。当我们到达那里时，意想不到的事发生了：通过一种我们至今仍无法逆向解析的魔法，一些穿着奇怪长袍的埃亚尔人在我们的大陆上出现，这些人声称忠于莎西·凯希，并愿为我们的实验献身。从那以后，一批又一批类似的志愿俘虏被传送了过来。可惜的是，这些人对实验并没有带来想象中的帮助——他们的每一丝生命精华已被汲取殆尽，陷于死亡边缘。这还没有算上常见的体内出血的情况，又或者是神经网络重接导致他们将痛苦视为快乐的情况，这让我们开发更好惩罚手段的努力无功而返。不过，总的来说他们既合作又数量充足，并且很有帮助。我们不确定莎西·凯希是否还存活。如果她还活着，我们相信她的忠诚与我们同在。

#{italic}#在主要文字的下面蚀刻着一条简短的信息。#{normal}#

真可爱。我准备留下这些文字。

—S。

```

## entry-03385
位置：tome-ashes-urhrok.lua:586；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
demon statue: Walrog
```
译文：
```text
恶魔雕像：乌尔罗格
```

## entry-03386
位置：tome-ashes-urhrok.lua:587；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#The message at the base of this statue has been scratched out, and a new one has been carved in its place.#{normal}#

Walrog, if you're reading this: We're still alive, but keep up the good work.
-S.
```
译文：
```text
#{italic}#这座雕像底座上原有的文字已经被刮掉，一行新的留言取代了它的位置。#{normal}#

乌尔罗格，如果你看到这个：我们还活着，继续好好干。
—S。
```

## entry-03387
位置：tome-ashes-urhrok.lua:594；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
demon statue: Kryl-Feijan
```
译文：
```text
恶魔雕像：克里尔·费扬
```

## entry-03388
位置：tome-ashes-urhrok.lua:595；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#The text at the base of this statue has been scratched out.  A note is attached in its place.#{normal}#

Hello, Eyalite.  The text here wouldn't have meant a whole lot to you; a whole lot of blathering about his accomplishments as a naturalist, and his mysterious disappearance.  Let me tell you what you need to know instead.

Kryl-Feijan was my lover, and along with a friend by the name of Walrog we came to Eyal out of curiosity and thirst for knowledge.  It was an enlightening hobby, and the reports we made of your many, primitive species were read all across our world.  Do not think you deserved this attention; you were not special in any way aside from your inferiority.  How could the planet of the powerful, intelligent Sher'Tul create such savages that had barely escaped feudalism?  Your sins were endearing, and your failures amusing.  And it was knowing this, along with the curious absence of the Sher'Tul, that led us to go out and investigate when a wounded child of onyx came through our portal, deactivated it, and told us of horrible destruction unleashed on Mal'Rok by Eyal.  We knew you were not capable of such feats, so we had to learn the answers for ourselves; Kryl-Feijan and I adopted our usual disguises as human mages, while Walrog arranged to scout the seas for anomalies, then meet us back after a few days.

When we emerged from our underground lodge, we were surprised to see firestorms (although not nearly so fierce) raging across Eyal as well.  What surprised us more, though, was an enraged horde of peasants, provoked by our unfortunate choice of disguises - in your ignorance, you chose to blame spellcasters for the disaster.  We tried to escape, but the mob swarmed us from all directions, and were soon upon us.

Soon, I was tied up and restrained, while they gloated and made threats I couldn't hear over the din of the crowd.  I could have fought back, but I kept telling myself only to lash out once I was sure my life was in danger, reassuring myself that the people of Eyal who were once so fascinating to me surely couldn't be aware of what they were doing.  Judging from the geysers of flame bursting above my head, my lover was not so patient; when the blasts stopped and the crowd started to clear away, I saw why he'd fought so fiercely.  His injuries were horrific, clearly done to make him suffer rather than incapacitate him, and he was on the edge of death.  In a moment of desperation, I muttered a spell to myself to understand what was going through their minds, what could possibly justify such treatment.  That's when I learned what they'd done to him, and what they were planning with me, but neither was as awful as the unthinking hate motivating it...  there are both too many words for it and not enough.  Horrible, barbaric, sadistic, all are accurate but none fully convey the evil of it.  That moment is when I learned the true savagery of Eyal, and realized the fate all Eyalites deserve.  That moment is when my patience broke.

There is a type of magic on Mal'Rok that will allow one to transfer his or her life-essence to another, prolonging the latter's lifespan at the expense of the former.  Voluntary donations to honored figures are popular, but the reverse - draining another to help one's self - was considered the gravest of sins, a statement that you considered your life to be worth more than another's, which is a decision nobody should be allowed to make when they have a vested interest in it.  Walrog had taught this forbidden spell to me, and only now did I use it, withering the horde all at once and forcing their lives into Kryl-Feijan.  The survivors, too weak to stand up against me, suffered greatly, playthings of my brief and furious revenge.  Unfortunately, even all the life I'd drained was not quite enough to restore my lover to health; all it could do was keep him in limbo, in incredible pain and unable to act, but still alive.

I took his surviving essence and fled to safety, then started picking the natives off one by one, extending my lifespan and getting ever closer to restoring him to health.  I can only assume Walrog is doing the same, preying on sailors first and then naga; I've lost contact with him, but the stories of terrors from the sea tell me he's still alive.  Keeping Kryl-Feijan in limbo consumes a great deal of energy, though, and soon lone travellers were not enough to keep him stable; I needed others to work for me, gathering victims and willingly sacrificing themselves once they'd outlived their usefulness.  And that is when I learned of the approach of the Fearscape, and came up with an offer I could make to the residents of Eyal.

When the legions of Urh'Rok manage to get an invasion force to Eyal's surface - not if, but when - you will all suffer, more than you can possibly imagine.  Many of you will die; some will not be so lucky, and will be an ever-living target of their rage, tortured until the end of time.  Their reasons are somewhat inaccurate, but make no mistake: you deserve the fate they have lined up for you.  Even if I wanted to, neither I nor anything else in the universe could stop their invasion, save the word of Urh'Rok himself - and that seems rather unlikely.  If you assist me and follow my orders to my satisfaction, I can guarantee you two things.  One, your inevitable agonizing fate WILL end in death, after a maximum of a couple of weeks; even the armies of Mal'Rok can't undo the effects of having your life-essence drained.  And two, before you feel the pain, you will feel nearly-equal pleasure.  With my magical skills, I can alter myself into any form, create all manner of illusions, and manipulate all your senses to your liking.  Your wildest, most unrealistic fantasies will become true; the time before the pain starts will be so enjoyable as to eclipse every moment of your pathetic lives that came before.  And if you think yourself above such hedonism, consider the psionically-gifted servitors I've recently acquired, and the way they could change your memories - when the "demons" are dripping acid into your eyes, then growing them back with more nerve endings than before so you can feel the pain more acutely, won't it be much more bearable if you're under the delusion that you've made a selfless sacrifice to save Eyal, and that your children and loved ones aren't suffering the same fate?

Countless others have agreed to this deal in the millenia before you were even born, and I have amassed enough essence to contain Kryl-Feijan in a stable "seed."  Once it is planted in a suitable victim and allowed to grow, he will once again walk Eyal, far more powerful than he was before, and the two of us will do everything we can to speed up your miserable world's much-deserved death.  Technically, any sentient and fleshy body would work, but I'd like someone who'll be missed, whose death will allow my lover's first act in rebirth to cause great misery to Eyal.  If you'd like to accept my deal, come unarmed and alone to the Crypt of Kryl-Feijan, and join your fellow Eyalites in servitude to me.  And if you were to bring a suitable host for my lover...  well, that'd be deserving of some special, one-on-one attention, wouldn't it?

Eyal is doomed to perish in screaming agony.  Wouldn't you at least like a good-bye kiss first?

-S.
```
译文：
```text
#{italic}#这座雕像底座上原有的文字已经被刮掉，一段笔记被留在了那里。#{normal}#

你好，埃亚尔人。这里原本的文字对你们来说并不重要：只不过是一个博物学者喋喋不休地讲述他的成就和谜一般的失踪。我来讲一些你们应当知道的东西。

克里尔·费扬是我的爱人。出于好奇和对知识的渴望，我们与一位朋友——乌尔罗格——来到了埃亚尔大陆。这个爱好带给我们很多启发，我们撰写的关于埃亚尔大陆原始物种的报告，在我们的世界被广泛传阅。别以为你们值得这样的注意；除了劣等，你们别无其他特质。孕育了强大，聪慧的夏·图尔人的这颗行星是怎么创造你们这样还没脱离封建社会的野蛮人的？你们的罪孽让人欣喜，你们的失败令人发笑。正是因为这，再加上夏·图尔人的神秘失踪，当那名受伤的缟玛瑙之子穿过并关闭了我们的传送门，告诉我们埃亚尔大陆给玛·洛克带来了可怕的毁灭时，我们立刻知道你们没能力实现这样的壮举。所以我们决定亲自出发寻找事件的真相。克里尔·费扬和我像往常一样变装为人类法师，乌尔罗格则在海上搜寻异常，并在几天后与我们会面。

从地底的居所出发后，我们惊讶的发现火焰风暴（尽管没那么猛烈）也在埃亚尔大陆肆虐。更令我们吃惊的是大量的无知难民，将这一切归罪于魔法师。我们的伪装正好激怒了他们。我们试图从暴民中脱身，但是人群蜂拥而至，最后控制了我们。

很快，我就被绑起来，他们满意地看着我们，并且发出种种威胁，然而嘈杂的人声淹没了他们的声音，我没能听清楚。我本可以反击，然而我一直忍耐，想着只要在真正有性命之虞的时候抽身逃走就行，不停地劝慰自己，那些曾经对我来说多么吸引人的埃亚尔住民们根本不知道他们在做什么。然而，一连串在我头上爆炸的火焰显示出我的爱人显然没有那么耐心。当爆炸平息，人群散开的时候，我终于知道他为什么如此凶猛地反击了。他受了很严重的伤，明显是为了让他受苦而不是限制他的行动，他就快死了。在一瞬的绝望之后，我低声念出了咒语，读取了他们的思想，了解他们为什么如此对待我的爱人。于是我知道了他们对我的爱人做了什么，以及他们将要对我做些什么，更可怕的是支配他们行动的那不假思索的憎恨……有很多词可以用来形容，可憎的、野蛮的、虐待狂的，都很准确，但是却无法描述那其中的邪恶。正是在那时，我了解了埃亚尔的野蛮，以及所有埃亚尔人应得的命运。同时，我的忍耐已经突破了极限。

玛·洛克的世界里有这样一种魔法，它可以让一个人把他的生命精华转移给另一个人，以前者的生命为代价，延长后者的寿命。对受人尊敬的名人志愿奉献生命很常见，但是反之——汲取别人的生命来帮助自己——被认为是最严重的罪行。这等同于宣称你的生命比其他人的更有价值。当人们能从中获得利益的时候，这样的权衡是不被允许的。乌尔罗格曾将这个禁咒传授给我，也只有在那时我使用了这个咒语，使暴民们的生命全部枯萎，并将它们转移到克里尔·费扬体内。即使是幸存的暴民，也承受了巨大的痛苦，摇摇欲坠，成为了我疾风暴雨般复仇的牺牲品。不幸的是，我汲取来的所有生命也不足以让我的爱人恢复健康，仅仅能让他在地狱门前徘徊，忍受着无尽的痛苦，丧失行动的能力，苟延残喘。

我带着他仅存的精华逃跑到安全的地方，然后开始一个接一个的夺走埃亚尔人的精华，延长我的寿命，并尽可能的让他恢复健康。我猜想乌尔罗格也在这么做，捕食水手，然后是娜迦。我们失去了联系，但是一些海上的恐怖传说让我相信他还活着。维持克里尔·费扬的生存消耗了许多能量，再过不久，独行的旅人已经不足以使他的状况稳定。我需要其他人为我工作，收集牺牲品，并在物尽其用之后奉献生命。也正是在那时，我得知了恐惧空间正在逼近，并且想出了一个给埃亚尔人的提议。

总有一天，乌鲁洛克的军团将对埃亚尔展开侵略。你们都会遭受难以想象的痛苦。你们许多人都会死去。当然不是所有人都这么幸运，剩下那些会成为他们无尽狂怒的靶子，他们会一直折磨你直到时间的尽头。他们的理由是——或许不准确，但是我没有说错——“他们所安排的命运是你们应得的”。我或者宇宙中任何事物都没法阻止他们的侵略，尽管我很想这么做。恐怕只有乌鲁洛克本人的话语才能阻止这一切——而这看起来也不太现实。如果你们能帮助我，并且服从我的命令，让我感到满意，我可以保证你们两件事：第一，你无法避免的可悲命运将会以死亡终结，最多只要几周的时间，哪怕乌鲁洛克的军队也无法在我汲取你们的生命精华之后撤销这个行动。第二，在你们感到痛苦之前，你们会感到等量的快乐。通过魔法，我可以让自己变成各种形态，生成各种各样的幻想，按你们的喜好操纵你们的感官。你们最疯狂最不现实的梦想将会成真。等待痛苦到来的时间将会变得令人愉悦，让你的之前的人生黯然失色。如果你们觉得不屑于这种享乐主义，那么我最近招纳的有心灵能力方面天赋的仆从值得考虑，他们可以改变你们的记忆。当“恶魔们”将酸液滴入你的眼球，再将它放回神经更加密集的地方去，于是你会感到更加剧烈的痛苦。如果这时，你产生了你在为拯救埃亚尔大陆而无私的奉献生命，并且你的爱人孩子不会承受如此痛苦的幻觉，你会不会感觉这一切更加容易忍耐了呢。

在你们诞生千年之前，数不清的其他人已经接受了这个提议，我积累了足够的精华将克里尔·费扬保存在一个稳定的“种子”之中。一旦将它种在合适的牺牲品之中放任生长，他将以更加强大的姿态重返埃亚尔大陆。我们两人将会用尽所有手段来加速你们可悲世界的应得的末日。理论上，任何有灵性的血肉之躯都可以作为种子的容器。但是我想要一个会被怀念的人，杀死他可以让我爱人重生的第一步给这个世界带来巨大的不幸。如果你接受我的提议，就卸下武装只身前往克里尔·费扬地宫，与你的埃亚尔同胞一起为我效劳。如果你能给我的爱人带来一个合适的容器……很好，那将会得到某种特殊的、一对一的照顾，怎么样？

埃亚尔注定在痛苦的尖叫中灭亡。你们不想先来个告别之吻吗？

—S。
```

## entry-03389
位置：tome-ashes-urhrok.lua:637；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Our tournaments, run ever since our salvation from the dust mages under the command and inspiration of Urh'Rok, are not simply tests of direct combat, as many may think.  We have those, yes, but we also have competitions for scholarly work, attentiveness, physical endurance, philosophy, and countless other fields.  Perhaps the most prestigious of these, though, is the Divine Tournament of Tactics, by which our military leaders are selected.  Through a series of trials, we are compared in our abilities to assess a combat scenario and swiftly handle it, rated on speed, casualties, deployment efficiency, and a variety of other factors.  Khulmanar, a child of onyx, is the reigning champion of these, and has been for most of the time that we've spent waiting for our continent to reach Eyal.  Chosen by our process as the wisest tactical mind among our people, he was selected to meet with Urh'Rok himself to gain his approval to lead our forces in the invasion.  Urh'Rok was so impressed by Khulmanar that he used a significant portion of the little energy he's not using to hold our world together to build Khulmanar a new body, one strong enough to let him direct battles from the front-line without fear.  With a form and weapons granted by our Father, and a mind given his direct, enthusiastic approval, Khulmanar is considered to be the avatar of Urh'Rok, and his commands in battle are to be treated with the same reverence we would give to the words of Father himself.
```
译文：
```text
自从我们被从尘埃法师的控制之下解放后，在乌尔洛克的命令和鼓动下，我们开始举办锦标赛。这个比赛，不像很多人想的那样，仅仅是为了测试直接的战斗。除此之外我们还有学术工作、专注、物理耐受、哲学等诸多其他领域的竞赛。或许，这其中最著名的当属神圣战术竞标赛，我们的军事领导人正是通过这个赛事选拔出来的。比赛包括一系列试炼，评估我们对战况进行分析和处理的能力，包括速度、伤亡、部署效率以及一些其他的因素。库马纳，缟玛瑙之子，是这些项目的冠军，并且在等待我们的大陆到达埃亚尔的大部分时间里，他都维持了统治地位。通过我们竞赛所筛选出的最杰出的战略大师，库马纳被乌鲁洛克亲自召见以获准统御我们的入侵部队。库马纳给乌鲁洛克留下了很深的印象，于是后者从他维持我们世界的力量以外的部分中抽取了很大一部分，为库马纳创造了一个全新的肉身，让他能够在前线无所畏惧的指引战斗。拥有我们的父所赐予的武器与躯壳，精神受到父的指引，库马纳被视作乌鲁洛克的化身，他在战场上的指令受到如同父一般的尊敬。
```

## entry-03390
位置：tome-ashes-urhrok.lua:638；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
demon statue: Lithfengel
```
译文：
```text
恶魔雕像：里斯丰格
```

## entry-03391
位置：tome-ashes-urhrok.lua:639；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Lithfengel, mentor of Draebor and child of emerald, was one of our finest scholars.  When most of us were still too afraid to go near a portal, he recovered an intact one and began to pry apart its secrets, in hopes of reaching Eyal.  His data showed that although this portal was still technically connected to Eyal, the link between the two worlds was still fluctuating far too much to make it safe for travel, the still-raging flames threatening to tear any prospective passengers apart before they reached their destination.  Rather than try to repair the link directly, he went into his lab and didn't emerge for a few days; when he came out, he glowed with a strange new enchantment, proclaiming it would adaptively mutate him to endure whatever damage the portal would otherwise inflict.  Saying that the consequences of failure were too awful to risk inflicting on other test subjects, he entered the portal himself, promising to return immediately after he arrived; he has not been seen since.  May he rest in peace for his selfless devotion.
```
译文：
```text
里斯丰格，小恶魔德瑞宝的导师，绿翡翠之子，是最杰出的学者之一。当我们大部分人还畏惧接近传送门的时候，他早已找到了一个未被人使用过的，并且开始窥探其中的秘密，希望能够达到埃亚尔。他的数据显示，尽管这个传送门与埃亚尔连接，但是两个世界之间的波动使得前往另一个世界的旅行太过危险，肆虐的火焰会在你到达目的之前将你撕碎。比起直接修复连接，里斯丰格躲入他的实验室里好几天。当他出来的时候，他浑身笼罩着一层奇异的新符咒散发的光芒，宣称这道符咒将会使他产生适应性突变来抵御传送门将会造成的任何伤害。由于他说实施其他实验的失败后果太过危险，他独自一人进入了传送门，并且承诺在到达之后会立即返回，从那以后再也没有人见到他。看在他无私奉献的份上，愿他能够安息。
```

## entry-03392
位置：tome-ashes-urhrok.lua:641；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Recently, the cultists of Shasshhiy'Kaish have begun speaking of a "demon seed," a sort of magical cluster of life-essence which can be implanted in a sentient being, allowing it to grow inside of them and eventually become one of our citizens.  Inspired by this idea, the children of emerald have developed a prototype of this form of magic, and the children of onyx have made a chassis to carry it into combat.  Rogroth generates countless essence-less seeds from within its frame, then embeds them in nearby living beings, so when they expire, their life-essence goes directly into the seed and allows it to grow.  We have not yet perfected its production capabilities, so currently the seeds will only become degenerate husks when they grow, but fear not!  As we get data from the tests of this design, we'll improve on it, and soon the slaughter of our foes will cause wretchlings, quasits, and even thaurheregs to spring up from their corpses.  With a little bit of luck and some decisive early skirmishes, we could even bypass the problem of getting an invasion force to the surface entirely, growing it there instead.
```
译文：
```text
最近，莎西·凯希的教徒们开始谈论起“恶魔种子”。这是一串具有魔力的生命精华，可以被植入有灵性的生物中，并在其中发育为我们的公民。在这个传说的启发下，绿翡翠之子研究出了这种魔法的原形，缟玛瑙之子制造了能够将其应用于战斗的基座。洛格罗斯在这个构造中留下了无数没有精华的种子，并将这些种子嵌入附近的生物中，当这些生物死去，他们的生命精华将会流入并滋长这些种子。我们还没有完善的生产能力，所以目前这些种子只会成长为退化的空壳。但是别担心！随着我们获取相关的数据，我们将会改进它。不久的将来，当杀死我们的敌人后，酸液树魔、夸塞魔，甚至是修尔希瑞格将会从他们的尸体中诞生。只需要早期的小规模战斗，加上一点好运，我们可以在埃亚尔生产我们的入侵部队，直接传送部队的难题就这么被绕过了。
```

## entry-03393
位置：tome-ashes-urhrok.lua:643；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
One of the problems with making daelach is the inherent instability that comes from creating something that is almost entirely made of magic.  If ambient levels of blight are even slightly too high, it can set off a chain reaction that at best destroys the daelach, and at worst destroys most of the mages who were building it.  Daelach production is thus theoretically cheap, but in practice involves great expense, and usually a blighted daelach has to be immediately put down lest it cause tremendous damage.  One specimen, though, adapted to the blight in a very interesting way, sprouting wings and bolstering its usual firestorms with blight, but otherwise remaining perfectly balanced and controllable.  We'll try to recreate this happy accident however we can, but in the meantime, it will prove effective on the surface of Eyal.
```
译文：
```text
制造达莱奇的问题之一就是创造纯粹魔法生物所固有的不稳定性。如果周边的枯萎水平哪怕高那么一点点，也会导致连锁反应，轻则摧毁达莱奇，重则会杀死大部分负责制造达莱奇的法师。因此制造达莱奇的理论成本很低廉，但是实际上会带来巨大的费用。而且，一个枯萎化的达莱奇必须立刻被压制，以免它造成巨大的损害。不过，有一个样本用一种有趣的方式进行了枯萎化，它长出了翅膀，并用枯萎能量强化了他的火焰风暴，另一方面它维持了平衡与可控性。我们将会用尽所有办法尝试重现这个令人惊喜的意外，与此同时，它会前往埃亚尔大陆证明他的实际效果。
```

## entry-03394
位置：tome-ashes-urhrok.lua:645；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Of the anomalies and phenomena we've noticed in our studies of the shield protecting Eyal, none have frustrated us so much as meteors.  Certain powerful Eyalite spellcasters can pull a large meteor into low orbit, passing it through the shield relatively unharmed, aside from being split into predictably-sized chunks, which are then called to the surface one-by-one in a series of devastating meteoric crashes.  While we have not yet found a way to reverse-engineer these spells to protect our standard troops from disintegration, we have had some limited success in making a construct that closely resembles a meteor in composition and appearance.  Harkor'Zun, a being made mostly of stone, was simply dropped from our platform; the shield shattered him as expected, but we had designed him to survive this, the fragments merging back into their completed form once he reached the surface.  It would seem, though, that either we made him to be too sturdy, or the shield envelops incoming objects in a sort of anti-magic coating, as he has been unable to start the second stage of this process, wherein he merges these fragments back into a completed form.  Should an Eyalite stumble upon him and attempt to destroy the fragments, Harkor'Zun will be able to re-combine and "thank" whoever granted him his ascension.
```
译文：
```text
在我们对守护埃亚尔之盾的研究所发现的规律与异常现象之中，没有一个像流星这样让我们沮丧。一些强大的埃亚尔法师可以将大型的流星拖入低空轨道，在几乎没有损伤的情况下使它通过护盾，唯一的损伤是陨石被分割成若干大块，然后被依次召唤到地表造成毁灭性的陨石撞击。我们还没有找到反制这些咒语的方法来保护我们的军队免于溃散。我们在制造一种成分和外观都酷似陨石的造物方面取得了一些有限的成功。哈卡祖，大部分由石头构成的生物，被我们从我们的平台上丢下。如同想象的那样，护盾将它撕得粉碎，不过我们的设计让它能够得以生存。碎片在到达埃亚尔之后重新融合到一起，组成完整形态。然而，或许是因为我们将它制造的太过顽固，又或许是护盾将侵入的物体包裹上反魔法的外衣，哈卡祖无法进行第二阶段——将碎片重组的阶段。如果有埃亚尔人偶然发现它并试图摧毁这些碎片，哈卡祖将能够重新组合，并“答谢”那个助它升华之人。
```

## entry-03395
位置：tome-ashes-urhrok.lua:676；section：tome-ashes-urhrok/data/quests/start-ashes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You do not remember much of your life before you were on this burning continent, floating in the void between worlds.  You have been helping demons, happily participating in their experiments to shatter some sort of shield preventing them from taking their righteous revenge on Eyal.

You are being taken by your handler to the torture-pits to help them figure out how to cause the most pain to those on Eyal, when you hear a roaring above you; you look up and see a burning meteor, flying closer, and the demons' spells failing to divert its course!  It lands near you, knocking you off your feet with its shockwave and killing your handler instantly.

As you recover, and your platform of searing earth splits from the main continent, your old memories flood your mind and you come to your senses - the demons are out to destroy your home!  You must escape... but not without destroying the crystal they've used to keep track of you.

```
译文：
```text
你已经不太记得来到这片漂浮在虚空中的燃烧大陆之前的记忆了。你曾经帮助过恶魔，欢欣着参与他们的实验，以打破某种阻止恶魔降临大举复仇入侵埃亚尔的无形屏障。

你被你的“主人”带到折磨场以帮助研究如何对埃亚尔大陆的生灵造成更大的痛苦，突然一阵轰鸣从天上传来，你抬头，看见一颗燃烧着的陨石正在坠落。恶魔试图用法术改变其轨迹，但没有成功！它落在你身边，砸死了你的“主人”，同时你也被冲击波击飞。

当你醒来后，你发现你身处一个和主大陆分离的平台，而你旧时的记忆渐渐涌来。你立刻惊醒——恶魔们要毁灭你的故乡！你必须逃离……同时别忘了摧毁他们用以追踪你的水晶体。

```

## entry-03396
位置：tome-ashes-urhrok.lua:714；section：tome-ashes-urhrok/data/talents/corruptions/black-magic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
By gorging yourself on up to %d stacks of Bleak Outcome from a creature, you turn into an Ominous Shadow for one turn per stack.
		While transformed you are invisible (power %d), convert 100%% of all damage done to darkness and gain darkness resistance penetration and damage increase equal to your highest.
		While transformed you can not apply new Bleak Outcome stacks.
```
译文：
```text
你吞噬一个生物身上最多 %d 层悲惨结局效果，使自己化为不祥黑影，每层持续 1 回合。
		不祥黑影状态下你处于隐形（强度 %d）造成的所有伤害转化为暗影伤害，并获得相当于你最高伤害加成和抗性穿透的暗影伤害加成和抗性穿透。
		在变身状态下，无法施加新的悲惨结局效果。
```

## entry-03397
位置：tome-ashes-urhrok.lua:725；section：tome-ashes-urhrok/data/talents/corruptions/brutality.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target twice, doing %d%% weapon damage each hit. You gain life equal to %d%% of the damage dealt, and you gain %d vim for each attack that hits.
```
译文：
```text
对目标攻击两次，每次造成 %d%% 武器伤害，吸取 %d%% 的伤害回复生命，同时每次击中均回复 %d 活力。
```

## entry-03398
位置：tome-ashes-urhrok.lua:728；section：tome-ashes-urhrok/data/talents/corruptions/brutality.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the grasp!
```
译文：
```text
%s 抵抗了抓取！
```

## entry-03399
位置：tome-ashes-urhrok.lua:794；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You spawn a pool of acid in radius 4 around you for %d turns, dealing %0.2f acid damage to all creatures, including you.
		You also gain 40%% acid resistance and %d%% acid affinity.
		The damage scales with your Spellpower.
```
译文：
```text
在半径 4 的范围内制造持续 %d 回合的酸池，造成 %0.2f 酸性伤害（包括自己）。
		你获得 40%% 酸性抗性与 %d%% 酸性伤害亲和。
		伤害受法术强度加成。
```

## entry-03400
位置：tome-ashes-urhrok.lua:801；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Select a use for the %s charge(s):
```
译文：
```text
选择%s次充能的用途：
```

## entry-03401
位置：tome-ashes-urhrok.lua:802；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Shield for %d damage (50%% reflect).
```
译文：
```text
产生护盾，抵挡%d伤害（50%% 反射）。
```

## entry-03402
位置：tome-ashes-urhrok.lua:865；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You enchant your shield to grant you power for %d turns.
		While the effect last your Strength and Magic stats are increased by 10%% of your shield block value.
```
译文：
```text
你利用盾牌来强化自身，力量和魔法增加 10%% 格挡值，持续 %d 回合。
```

## entry-03403
位置：tome-ashes-urhrok.lua:874；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Raging flames burn foes and allies alike, doing %0.2f fire damage in a radius of %d each turn for %d turns.
		Demons standing in the doomfire will instead be healed.
		The damage will increase with your Spellpower.
```
译文：
```text
向地上释放一片火焰，每回合可对敌我双方造成 %0.2f 火焰伤害，半径 %d 码，持续 %d 回合。
		站在毁灭之火中的恶魔不会被伤害，而会被治疗。
		伤害受法术强度加成。
```

## entry-03404
位置：tome-ashes-urhrok.lua:880；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whenever you take blight damage you bask in the sweet pain for 2 turns, increasing all damage affinity by 15%%.
		This can only happen every %d turns.
```
译文：
```text
每当你受到枯萎伤害，你沐浴痛苦的甜美，在 2 回合内提升全体伤害亲和 15%%。
		这一效果最多每 %d 回合触发一次。
```

## entry-03405
位置：tome-ashes-urhrok.lua:884；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whenever you block an attack with your shield, you randomly hex the attacker with one of the hexes: Pacification, Domination, Burning or Empathic as if cast at talent level %d.
		This may only happen once per turn.
```
译文：
```text
当你使用盾牌格挡一次攻击，你会朝攻击者释放一个随机邪术：宁神邪术、支配邪术、燃烧邪术或是转移邪术，技能等级为 %d。
		这一效果最多每回合触发一次。
```

## entry-03406
位置：tome-ashes-urhrok.lua:888；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whenever make a melee attack, you have a %d%% chance to randomly curse the target with one of the curses: Defenselessness, Impotence, Death or Vulnerability as if cast at talent level %d.
		This may only happen once per turn.
```
译文：
```text
每当你进行一次近战攻击，你有 %d%% 几率随机对目标释放一次诅咒：衰竭诅咒、虚弱诅咒、死亡诅咒或弱点诅咒，技能等级为 %d。
		这一效果最多每回合触发一次。
```

## entry-03407
位置：tome-ashes-urhrok.lua:939；section：tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whenever you take direct damage, there is a %d%% chance that your your diseased body erupts in blight, diseasing your attacker with a random disease for %d turns.
		Each turn the disease deals %0.2f blight damage and reduce one random attribute (strength, dexterity, constitution) by %d.
		This may only happen once per turn.
		The damage increases with your spellpower.
```
译文：
```text
每当你受到直接伤害时，你充满疫病的躯体有 %d%% 几率爆发出枯萎能量，使攻击者感染随机疾病，持续 %d 回合。
		疾病每回合造成 %0.2f 枯萎伤害，并会降低随机一项属性（力量、敏捷或体质）%d。
		这一效果最多每回合触发一次。
		伤害受法术强度加成。
```

## entry-03408
位置：tome-ashes-urhrok.lua:969；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (%d/%d life, level %d)
```
译文：
```text
%s (%d/%d 生命值，等级 %d)
```

## entry-03409
位置：tome-ashes-urhrok.lua:971；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The seed of a demon.
```
译文：
```text
恶魔的种子。
```

## entry-03410
位置：tome-ashes-urhrok.lua:972；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Demon status: %s.
```
译文：
```text
恶魔状态：%s。
```

## entry-03411
位置：tome-ashes-urhrok.lua:974；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：_t；args_order：None；special：None

原文：
```text
dead (can not be summoned)
```
译文：
```text
死亡（无法召唤）
```

## entry-03412
位置：tome-ashes-urhrok.lua:977；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CRIMSON#You feed vim into your %s, increasing its level to %d and healing it.
```
译文：
```text
#CRIMSON#你将活力注入你的 %s，将其等级提升到 %d，并治疗了它。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Thrall	奴仆	T.GAME.EFFECT	combat	_t	preferred	core	精神支配后目标的状态身份；与 Mental Domination“精神控制”能力名区分
Tumble	翻筋斗	T.GAME.TALENT	talents	talent name	existing	core	
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
engineering	工程	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fearscape	恶魔空间	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactical	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 tactic 同义的变体
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
torture	折磨	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
