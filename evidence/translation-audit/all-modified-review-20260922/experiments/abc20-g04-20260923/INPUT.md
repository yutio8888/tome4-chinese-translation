# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03292–entry-03332 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g04-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03292 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03292
位置：mod-tome.lua:42861；section：mod-tome/dialogs/orders/Talents.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Enter the talent weight multiplier
```
译文：
```text
输入技能权重乘数
```

## entry-03293
位置：mod-tome.lua:42862；section：mod-tome/dialogs/orders/Talents.lua；source_tag：_t；args_order：None；special：None

原文：
```text
0 is off, 1 is normal
```
译文：
```text
0 表示不使用这个技能，1 为默认
```

## entry-03294
位置：mod-tome.lua:42950；section：mod-tome/dialogs/shimmer/ShimmerRemoveSustains.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##CRIMSON#WARNING: this is an EXPERIMENTAL feature. It may explode!#LAST##{normal}#
Sustains auras with name in #YELLOW#yellow#LAST# can not be automatically turned back on if disabled. After turning them on here, you need to unsustain and resustain them manually.

#{bold}#This is a purely cosmetic change.#{normal}#
```
译文：
```text
#{bold}##CRIMSON#警告：这是一项实验性功能。它随时可能出现问题！#LAST##{normal}#
名称显示为#YELLOW#黄色#LAST#的持续技能光环，如果被禁用，将无法自动重新开启。在你在这里调整之后，需要手动先关闭再重新启用这些持续技能。

#{bold}#这个改变只会带来视觉上的变化。#{normal}#
```

## entry-03295
位置：mod-tome.lua:43048；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Arcane Combat
```
译文：
```text
奥术格斗
```

## entry-03296
位置：mod-tome.lua:43049；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You may select a spell for Arcane Combat to automatically trigger with melee attacks.  Otherwise, select 'Random spells' to have a spell selected automatically with each attack.

```
译文：
```text
你可以选择一项法术，在奥术格斗中进行近战攻击时自动施放。如果你选择随机法术，每次攻击时会随机施放一个法术。

```

## entry-03297
位置：mod-tome.lua:43054；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Each time Arcane Combat is triggered, a random allowed spell will be used.
```
译文：
```text
每当奥术格斗触发的时候，会施放一个随机可用的法术。
```

## entry-03298
位置：mod-tome.lua:43056；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
All known spells that can be used with Arcane Combat.
```
译文：
```text
所有已学会的可用于奥术格斗的法术。
```

## entry-03299
位置：mod-tome.lua:43067；section：mod-tome/init.lua；source_tag：init.lua description；args_order：None；special：None

原文：
```text
Welcome to Maj'Eyal.

This is the Age of Ascendancy. After over ten thousand years of strife, pain and chaos the known world is at last at relative peace.
The last effects of the #FF0000#Spellblaze#WHITE# have been tamed. The land slowly heals itself and the civilisations rebuild themselves after the Age of Pyre.

It has been one hundred and twenty-two years since the Allied Kingdoms were established under the rule of #14fffc#Toknor#ffffff# and his wife #14fffc#Mirvenia#ffffff#.
Together they ruled the kingdoms with fairness and brought prosperity to both Halflings and Humans.
The King died of old age fourteen years ago, and his son #14fffc#Tolak#ffffff# is now King.

The Elven kingdoms are quiet. The Shaloren Elves in their home of Elvala are trying to make the world forget about their role in the Spellblaze and are living happy lives under the leadership of #14fffc#Aranion Gayaeil#ffffff#.
The Thaloren Elves keep to their ancient tradition of living in the woods, ruled as always by #14fffc#Nessilla Tantaelen#ffffff# the wise.

The Dwarves of the Iron Throne have maintained a careful trade relationship with the Allied Kingdoms for nearly one hundred years, yet not much is known about them, not even their leader's name.

While the people of Maj'Eyal know that the mages helped put an end to the terrors of the Spellblaze, they also did not forget that it was magic that started those events. As such, mages are still shunned from society, if not outright hunted down.
Still, this is a golden age. Civilisations are healing the wounds of thousands of years of conflict, and the Humans and the Halflings have made a lasting peace.

You are an adventurer, set out to discover wonders, explore old places, and venture into the unknown for wealth and glory.

```
译文：
```text
欢迎来到马基·埃亚尔的世界！

现在的埃亚尔大陆是卓越纪。在长达一万年的冲突痛苦和混乱之后，我们所知的世界终于进入了一个相对和平的时期。
#FF0000#“魔法大爆炸”#WHITE#所造成的影响已经渐渐减轻。烈火纪之后，大地慢慢自愈，各个文明也纷纷开始重建家园。

自联合王国在#14fffc#图库纳#ffffff#与其妻#14fffc#米雯尼雅#ffffff#的统治下建立，至今已有一百二十二年。
在他们的统治下，王国天下太平，无论是人类还是半身人的居住地都欣欣向荣，一片繁华。
十四年前，国王因年纪过大而去世了，他的儿子，#14fffc#托拉克#ffffff#继承了王位。

精灵们的王国安详而平和。住在埃尔瓦拉的永恒精灵们试图让世界忘记他们在魔法大爆炸中扮演的角色，在精灵王#14fffc#艾伦尼恩·加威尔#ffffff#的统治下快乐地生活着。
而自然精灵则遵从古老的传统，住在森林当中，一如既往地由贤者#14fffc#奈希拉·坦泰兰#ffffff#统领。

近一百年来，钢铁王座的矮人们一直小心谨慎地与联合王国维持着贸易往来，但外界对这个种族所知甚少，甚至不知道他们的统治者是谁。

尽管马基·埃亚尔大陆上的居民都知道是魔法师们帮忙终止了恐怖的魔法大爆炸，但他们也没有忘记正是魔法本身造成了这场灾难。因此法师们至今仍遭社会排斥，甚至被公开猎杀。
无论如何，这是个黄金时代，所有的文明在过去数千年中经历的不幸正在好转，甚至人类和半身人之间已经形成了长久的和平。

你是一名冒险者，去见识奇观、探索古迹，为财富与荣耀踏入未知之地。

```

## entry-03300
位置：mod-tome.lua:43106；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Stunning an opponent slows down their movement and reduces their damage output, giving you the opportunity to tactically reposition or finish them off at less risk.
```
译文：
```text
震慑可以减缓目标的移动速度，降低其伤害输出，为你制造机会重新占位，或以更低的风险将其解决。
```

## entry-03301
位置：mod-tome.lua:43108；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
In the Age of Pyre the orcs learned the secrets of magic, and with their newfound powers nearly overcame the whole of Maj'Eyal.
```
译文：
```text
在烈火纪，兽人掌握了魔法的奥秘，凭借新获得的力量几乎征服了整个马基·埃亚尔。
```

## entry-03302
位置：mod-tome.lua:43109；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
The orcs once terrorised the whole continent. In the Age of Ascendancy they were rendered extinct, but rumours abound of hidden groups biding their time to return.
```
译文：
```text
兽人曾经给整个大陆带来了一场浩劫。在卓越纪，他们已被彻底灭绝，但传言四起，仍有隐匿的团体在蛰伏待机，伺机卷土重来。
```

## entry-03303
位置：mod-tome.lua:43111；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Alchemists can transmute gems to create fiery explosions, and are known to travel with a sturdy golem for extra protection.
```
译文：
```text
炼金术士可以转化宝石制造炽烈的爆炸，并且往往带着一尊坚固的傀儡随行以获得额外保护。
```

## entry-03305
位置：mod-tome.lua:43115；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Who knows what dark thoughts drive people to necromancy? Its art is as old as magic itself, and its creations have plagued all the races since the earliest memories.
```
译文：
```text
天知道是怎样的堕落思想才能使一个人成为死灵法师。这门艺术就像魔法一样历史悠久，它的造物自最早的记忆以来就一直困扰着所有种族。
```

## entry-03306
位置：mod-tome.lua:43118；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
"The Spellblaze tore Eyal apart and nearly brought about the end of all civilisation. Two thousand years on its shadow still hangs over many lands, and the prideful mages have never been forgiven their place in bringing it about.
```
译文：
```text
魔法大爆炸撕裂了埃亚尔大陆，整个文明差点被彻底摧毁。两千年岁月已过，爆炸的阴影依然笼罩着很多地区。而那些高傲的法师们，也从未因其在促成此事中所扮演的角色而获得宽恕。
```

## entry-03307
位置：mod-tome.lua:43119；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Some are cursed with mental powers beyond their full control, turning them to a dark life powered by hatred.
```
译文：
```text
某些人被诅咒，获得了超出自身完全掌控的精神力量，从此堕入由仇恨驱动的黑暗生涯。
```

## entry-03308
位置：mod-tome.lua:43120；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Dreadfell has always been shunned for its haunted crypts, but of late rumours tell of a darker and more terrible power in residence.
```
译文：
```text
恐惧王座一直以来都因其闹鬼的地宫而为人所避讳，但最近有流言传出，此地盘踞着一股更加黑暗可怖的力量。
```

## entry-03309
位置：mod-tome.lua:43121；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.
```
译文：
```text
虽然有人说还能在某些隐秘之地找到夏·图尔的神器，但据说不可轻慢它们。
```

## entry-03310
位置：mod-tome.lua:43124；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Arcane Blades employ a fusion of melee and magical combat. Their training is harsh but the most dedicated rise to great powers.
```
译文：
```text
奥术之刃是一个混合了魔法与近战的职业。他们的训练非常严酷，但最为投入者终能获得强大的力量。
```

## entry-03311
位置：mod-tome.lua:43136；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Trolls were once seen as little more than beasts or pests, but the orcs trained them up for use in war and they became much more intelligent and fearsome.
```
译文：
```text
巨魔从前不过被视作与野兽或害虫无异的东西，不过后来兽人因为战争的需要对它们加以训练，如今它们变得聪明得多，也可怕得多。
```

## entry-03312
位置：mod-tome.lua:43137；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Some say that the foot of a halfling is lucky to own. Halflings do not take well to those who enquire too forcefully.
```
译文：
```text
有人说拥有一只半身人的脚能带来好运。半身人可不待见那些打听得太起劲的家伙。
```

## entry-03313
位置：mod-tome.lua:43142；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Alchemists can bind gems to armour to grant them magical effects, to protect the wearer or improve their powers. Some commercial alchemists can imbue gems into jewellery.
```
译文：
```text
炼金术士可以把宝石镶嵌到盔甲上，赋予其魔法效果，以保护穿戴者或增强其能力。一些提供商业服务的炼金术士还能把宝石镶嵌到首饰中。
```

## entry-03314
位置：mod-tome.lua:43163；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Brawlers are trained in the use of their fists and mastery of their bodies. They can be as dangerous in combat as any swordsman.
```
译文：
```text
格斗家受过双拳运用与身体掌控的训练。他们在战斗中的杀伤力不亚于任何一个持剑的战士。
```

## entry-03315
位置：mod-tome.lua:43164；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Lightning is a chaotic element that is hard to control. It is said that those most attuned to it are eventually driven insane.
```
译文：
```text
雷电是一种混沌的元素力量，难以操控。据说与之最为亲和者最终都会陷入疯狂。
```

## entry-03316
位置：mod-tome.lua:43184；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A cloak can simply keep you warm or grant you wondrous powers should you find a magical one.
```
译文：
```text
斗篷可以让你保持温暖，而一些魔法斗篷可以给你神奇的力量。
```

## entry-03317
位置：mod-tome.lua:43192；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Sandals or boots can be worn on your feet.
```
译文：
```text
你的脚上可以穿上鞋子。
```

## entry-03318
位置：mod-tome.lua:43196；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your readied ammo.
```
译文：
```text
你准备好的弹药。
```

## entry-03319
位置：mod-tome.lua:43200；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weapon Set 2: Most weapons are wielded in the main hand. Press 'x' to switch weapon sets.
```
译文：
```text
第二套武器：大部分武器使用主手抓握。按 X 键切换武器套。
```

## entry-03320
位置：mod-tome.lua:43202；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weapon Set 2: You can use shields or a second weapon in your off-hand, if you have the talents for it. Press 'x' to switch weapon sets.
```
译文：
```text
第二套武器：如果你有对应的技能，你可以副手使用盾牌或第二把武器。按 X 键切换武器套。
```

## entry-03321
位置：mod-tome.lua:43204；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weapon Set 2: Object held in your telekinetic grasp. It can be a weapon or some other item to provide a benefit to your psionic powers. Press 'x' to switch weapon sets.
```
译文：
```text
第二套武器：使用你的念动力抓取的物品。你可以抓取武器，或者抓取其他物品来为你的心灵力量提供增益。按 X 键切换武器套。
```

## entry-03322
位置：mod-tome.lua:43208；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
List of items that can be instantly used by swift hands.
```
译文：
```text
无影手可即时使用（不消耗回合）的物品列表。
```

## entry-03323
位置：mod-tome.lua:43240；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I begin my writings with a study of the humans, currently the most populous of the races in Maj'Eyal. The greatest kingdom in number are by far the Cornacs, but mention should also be made of the Sholtar and Mardrop kingdoms, and the Higher bloodline. The biggest human population centre is around the citadel of Last Hope, though many other settlements exist across all corners of Maj'Eyal.

 Cornacs are normally around 5'9", with generally dark hair, brown eyes and ruddy features. Most Cornacs take up roles as tradesmen, farmers, or other manual labour jobs. It is a sad fact that the majority of bandit groups tend to be dominated by Cornacs. Cornac families tend to be large, and since the Age of Dusk their population has expanded rapidly, especially in the farming lands in the west and around Last Hope in the south.

 Sholtar are generally 5'11", with dark skin, hair and eyes. They originate from the south-east of Maj'Eyal, and are few in number since the Cataclysm tore much of their land into the sea. Their affinity with nature is renowned, and they are often found employed as healers, infusion crafters or wyrmic huntsmen.

 Mardrop humans are all but extinct, after the Spellhunt and the plagues during the Age of Dusk. They were known to be powerful spellcasters, and as such were prime targets by the spellhunters. However some trace of them can still be found, as their fiery hair and freckled skin oft can appear in those of distant descent. A few are rumoured to still possess citadels and towers in remote locations.

 Highers are on average 6'0", with fair hair and skin and blue or grey eyes. The majority of scholarly roles are taken up by Highers, and they tend to fill most of the noble classes. Some say this is due to discrimination and elitism, though these may simply be jealous sentiments. There are also rumours that the superior intellects of Highers are due to arcane experiments instigated by the ancient Conclave during the Age of Allure, but I have found no records to support this idea and must consider it to be baseless. The Higher bloodline is renowned as a mark of excellence, and mixing with lower bloods is strongly frowned upon.

 All human kingdoms were united by King Toknor the Brave in the Age of Pyre, and remain under the rule of his son King Tolak the Fair. A full discussion of the long human history would require a far more detailed document.
```
译文：
```text
我从人类的研究开始，他们目前是马基·埃亚尔人口最多的种族。若论人口数量，科纳克王国远超其他人类王国。此外，肖尔塔王国和马卓普王国以及高等人类这一血统支系也值得一提。最大的人类聚居地在最后的希望要塞周围，另外还有许多聚居地存在于马基·埃亚尔的每个角落。

 科纳克人基本身高在5英尺9英寸左右，有着黑色的头发、棕色的眼睛以及红润的肌肤。大多数科纳克人选择商人、农民或者其他体力劳动职业。不幸的是，大部分强盗组织也更倾向于被科纳克人控制。科纳克人的家族很庞大，并且自黄昏纪以来他们的人口增长极快，特别是在西部农业地区和南部的最后的希望一带，这种现象尤为明显。

 肖尔塔人基本身高在5英尺11英寸左右，黑皮肤黑头发黑眼睛。他们起源于马基·埃亚尔的东南地区，自从大爆炸将他们大部分土地沉入海洋后，他们的数量急剧减少。他们以自然亲和著称，并且经常作为治疗师、注能物工匠或龙战士猎手行走于世。

 在黄昏纪的魔法狩猎与瘟疫之后，马卓普人几乎灭绝。他们以强大的施法者著称，也因此成为猎魔者的首要目标。不管怎样，他们的血统特征——火红的头发以及生有雀斑的皮肤，仍会出现在血缘疏远的后裔身上。有部分传言说他们仍住在某些遥远的地方的城堡或高塔里。

 高等人类基本身高在6英尺左右，有着金色的头发、白皙的皮肤和蓝色或灰色的眼睛。大多数学者都是高等人类，贵族阶层也大多由他们占据。有人说这都是歧视和精英理论所导致的，虽然这可能只是简单的嫉妒情绪。也有传言说高等人类的高智商是厄流纪时期秘法会法师们的实验成果，但是我找不到任何证据来支持这一论点，我只能认为这种说法毫无根据。高等人类的血统被认为是优秀的标志，与低等血统通婚则为世所不齿。

 在烈火纪，勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子公正之王托拉克的手中。一份关于人类漫长历史的全面报告需要更加详细的文本来叙述。
```

## entry-03324
位置：mod-tome.lua:43261；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
No text would be complete without at least a brief note of some of the more brutish races which infest our world. These do not hold any civilised society of note, nor in general do they seem capable of any form of higher thought or culture, but they are still of interest to study for any who take delight in analysing beings of more primitive intellect.

 Trolls come in two main types - Kezrak and Moltep, or stone and forest trolls as they are colloquially known. Stone trolls infest many mountain chains to the north-east, and some have been known to wander further afield in search of food or to spread violence. They are generally over 8' high, with extremely pronounced muscular strength and a thick, solid hide which bears the appearance of coal or granite. Forest trolls are generally found in dense woods or swamps, with the Trollmire east of Derth being especially infamous. They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons, though their greenish hide is not as thick and their musculature less developed. All trolls have intensely fast metabolisms, capable of healing from grievous wounds within a matter of hours. At birth they measure just eight inches long, but within two years grow to full maturity, and rarely live beyond ten years old. They used to be considered little more than beasts, but towards the end of the Age of Pyre many were trained as fighters by the orcs, and were even taught the basics of language and certain battle tactics, making them much more dangerous. Though the orcs are gone their servants remain, and their remote breeding areas and intense birth rates have so far scampered attempts to eradicate them completely.

 Giants live mostly around the mountainous peaks surrounding the Daikara Pass. They vary greatly in size, but are normally at least 10' tall. They look somewhat like large, deformed humans, with swollen or distended facial features and much longer, swinging limbs. They live in nomadic tribes, moving from peak to peak with the seasons, feeding on wild deer and goats. They are usually peaceful creatures, only turning violent when their territory is encroached or their young are threatened. There are sometimes reports of giants coming to lowlands and stealing farm animals or attacking communities, but these are rare and normally isolated to particularly harsh winters. Giants seem to have no developed culture or language worth mentioning, but have been noted to show interactions of limited intelligence and to commune well in groups.

 Nagas were once believed to be mere myth, but reliable reports and even the capturing of dead physical samples has shown them to be real creatures. The upper half of their body is humanoid in form, with blonde hair and an extremely thin build, but the lower half is like that of a giant snake's tail. They stand around 6' tall on land, though their tails extend several feet further. They have been encountered off the eastern and south-eastern coasts of Maj'Eyal, which seems to indicate some exotic civilisation beneath the waves. Records of them exist only from the last few hundred years, and only more recently have they been interpreted as more than just the wild fantasies of inebriated sailors. They can breathe in air and underwater, possessing both lungs and gills, and have been reported to move with surprising speed on the ground. One might think them simply odd monsters, but they decorate themselves in jewellry and craft weapons and armour from materials found on the sea-bed, such as supple mail formed from layers of thick shark-hide. This would suggest an advanced culture, but communication with them so far has proved impossible. It is not known if they are capable of complex speech, but to date their only response to those who encounter them has been extreme violence, and fishermen in the east are always wary of coming across these vicious creatures.

 The origin of Demons is not wholly known, but it is clear that they are capable of intelligence and so I feel the need to describe them somewhat here. It is known that they can be summoned by certain magical rites, and minor demons were oft in the employ of evil sorcerers during the Age of Dusk. The main theory, which is supported by certain studies by Shaloren archmages, seems to indicate that they come from another world than our own, with connections formed through intense arcane energies. It must be a truly terrifying place to host such foul denizens. Demons vary immensely in appearance and power, as much as the creatures of our own world vary. They generally have blueish blood and metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness. All seem versed in magical abilities to some degree, and the strongest of them possess truly terrifying powers. Luckily they are exceptionally rare, and seem to be much less common in modern times since magic has fallen out of use.
```
译文：
```text
没有任何文字可以诠释那些影响我们世界的野蛮种族。他们没有任何文化遗留，也没有任何先进的智慧或文化，但是他们仍能激起大家研究原始种族的兴趣。

 巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。岩石巨魔生存与东北部的山脉地区，有些为了寻找食物和散播暴力甚至走到了更远的地方。他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。森林巨魔生活在浓密的森林和沼泽中，在德斯镇东部的巨魔沼泽尤为臭名卓著。他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速和能够使用精工武器闻名，尽管他们泛绿的外皮没有那么厚实，肌肉也不如岩石巨魔发达。所有的巨魔有着快速的新陈代谢能力，再严重的伤口，恢复只要几个小时。据测量，他们在出生时只有8英寸长，但是在2年内他们就可以成长完全，并且很少有寿命超过10年的。他们一开始被认为仅比野兽好一点，然而在烈火纪时，他们被兽人当做战士般训练，甚至学习了一些基础语言和战术，使得他们更加危险。虽然兽人已经走了，但他们的仆人仍然存在，并且他们偏远的繁殖地和极高的出生率至今仍挫败着彻底根除他们的企图。

 巨人们通常住在岱卡拉周围的山峦中。他们在体型上有着很大的差异，但基本上不会低于10英尺高。他们看起来就像是具有浮肿面部特征和更长的四肢的放大人类。他们属于游牧部落，随着季节的变化，从一个山头迁移到另一个山头，以鹿和羊为食。他们通常是和善的生物，只有当他们的领土受到入侵或者他们的后辈受到威胁时才会变的具有攻击性。有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击市民，但是这极其少见并且大多发生在极端的严冬。巨人们似乎没有值得一提的优越文化和语言，但是却向我们揭示了有限智慧的运用和团结一致的精神。

 娜迦曾被认为仅存于神话中，但是据可靠消息以及死亡的标本表明他们是真实存在的。他们的上半身是人形，有着金色的头发和苗条的身段，但是下半身却极像一只巨蛇的尾巴。他们大约身高6英尺，尽管他们的尾巴可能更长。他们在马基·埃亚尔的东岸和东南岸都有踪迹，这似乎表明波涛之下存在着某种异域文明。有关他们的记载只有近一百年的，并且越来越多的证据表明他们并不是喝醉水手们的幻觉。他们可以在水里和陆地上呼吸，同时拥有肺和鳃，并且据说在陆地上有着非常惊人的速度。有人可能认为它们只是特殊的怪物，但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。现在还不知道他们是否有复杂的语言，但是他们目前的对外回复只是极端的暴力，并且东海的渔民们经常要提防碰上这些邪恶的生物。

 恶魔的起源尚未完全清楚，但是很显然他们具有某种智慧，所以我觉得有必要在此写下一段。众所周知，他们是由某种魔法仪式召唤而来，并且在黄昏纪时期，小恶魔们经常受雇于邪恶的巫师。最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。那必然是一个地狱般的地方才能容下如此多恐怖的生物。恶魔们在外观和能力上不尽相同，正如我们世界里的生物一样。他们通常有偏蓝的血液和金属化的血肉，可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中。他们似乎都在某种程度上通晓魔法，并且他们之中最强者具有真正可怕的力量。幸运的是他们是非常罕见的种族，而且自从魔法淡出人们的视野后，出现的更加稀少了。
```

## entry-03325
位置：mod-tome.lua:43278；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The dwarves are an exceptionally secretive and quiet race, reluctant to talk about themselves to outsiders unless hefty bribes are paid. Many times in their history they have cut off all contact with the other races for no known reason, shutting tight the great iron doors that cover the trade passages to their mines and their cavernous cities. However of late they have become more open with the outside world, and I have even had the pleasure of receiving the unique distinction of being allowed to enter their main city, the Iron Throne, and speaking with several of their guild leaders.

 Dwarves are around 5' tall, with generally brown or grey hair. They are usually stocky and muscular, and known to be very resistant to any physical suffering. Their females can be hard to distinguish from their males, but can usually be identified by the beads braided into their beards. All dwarves are highly proud of their beards, and take immaculate care of them. The greatest insult to a dwarf is to belittle his beard, and the greatest sign of suffering in a dwarf is for him to tear at his beard.

 Dwarves are known especially for their smithwork and artificing, which is unrivalled amongst all the other races. They also make cunning merchants, known to drive a hard bargain. Their society consists of a fairly strict caste system, with families belonging to guilds of miners, smelters, craftsmen, and so on, and deviance into work outside of one's guild of birth is almost unheard of. However there is no perceived inequality between guilds, with each having equal representation on their ruling Committee of Guilds. Who actually acts as figurehead is unknown to outsiders though, and no amount of bribing will encourage any dwarf to speak on the subject. When it is mentioned in passing their allusions to a leader are normally marked by an almost religious reverence.

 Their skill with metal is renowned above all else. Dwarven steel is considered the most durable material for use in construction, and dwarves are the finest workers with stralite and voratun, precious metals of immense value. They trade heavily in their crafts from their capital the Iron Throne, but allow no outsiders in - instead they send innumerable merchant caravans out to all the cities to ply their wares.

 As well as the many merchant dwarves one may meet there are also a great deal of young dwarves who venture beyond their halls of stone. These are generally of adventuring fare, and it is encouraged in dwarven society to experience something of the wider world in one's younger years. This is known to them as being "smithed upon the anvil of the world". In private though some senior dwarves admit that this activity is promoted to help with their "market research strategy".
```
译文：
```text
矮人是非常神秘且低调的种族，一般来说，除非你给他们点好处，否则他们不会谈论任何与己有关的事。历史上，他们曾经多次无缘无故的切断和外界的联系，落下的钢铁大门隔绝了外界的交易通道以及通往他们矿井和地下城市的道路。不过，近来他们对外界越来越开放，我甚至获得了进入他们首都——钢铁王座的殊荣，并有幸与他们的主要领导人对话。

 矮人们基本身高在5英尺左右，有着棕色或灰色的头发。他们通常身材敦实、肌肉结实，并以超强的物理抵抗能力而闻名于世。他们的性别通常较难区分，但可以通过编入胡须的珠饰来辨认。所有的矮人都非常自豪于他们的大胡子，并且对他们的胡子非常爱护。对于矮人来说，贬低他的胡子就是最大的侮辱，而矮人极度痛苦时会撕扯自己的胡子。

 矮人擅长锻造和精工，这一点在所有种族中都是无与伦比的。他们同时精于商业，擅长讨价还价。他们的社会有着相当严格的等级制度，家庭通常会隶属于矿业公会、冶炼公会、工匠公会等等，脱离出身公会另谋生计的个人几乎从未听说过。不过，在公会之间并无地位不平等之说，各公会在统领众公会的公会委员会中拥有平等的代表权。谁实际担任名义领袖，外人不得而知，再多的贿赂也不能使任何矮人就此开口。当话题偶然被提及时，他们对那位领袖的暗示几乎总带着一种近乎信仰的敬畏。

 他们对金属的加工技艺也是举世闻名的。矮人钢被认为是建筑中最耐久的材料，而矮人也是加工斯莱特和沃瑞钽这两种价值连城的贵金属的最佳工匠。他们在首都——钢铁王座中进行大量的交易，但是从不欢迎外来者——相反，他们会指派无数商队到各个城市去售卖货物。

 在众多的矮人商人出现的同时，越来越多的年轻矮人更加倾向于从他们的石头洞穴里出去冒险。他们一般以探险为业，在矮人社会中，一个人在年轻的时候出去闯荡是值得鼓励和赞扬的。矮人称这种经历为在“世界之砧”上锤炼自己。不过私下里，一些年长的矮人承认推广这项活动是为了帮助他们的“市场调查策略”。
```

## entry-03326
位置：mod-tome.lua:43295；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Quekorja was the god of time and possibilities. What stands out about Eyal's myths regarding Quekorja is how wildly inconsistent they are. In particular, tales after the Godhunt tend to have a far less favourable outlook of the god than pre-Godhunt myths. Speculation regarding this is due to Quekorja supposedly taking an interest in written history and appointing its own librarians to record its tales. Since there are no surviving records of this library existing, this theory is considered to be pure conjecture and has no concrete evidence to validate it. There have been some unusual records found too, supposedly written by the same authors on the same dates, but wildly varying in their tone and their description of the god itself. Given the god's ability to control time, it is thought these notes might be from alternate timelines, further obscuring the truth about the god itself.

 Quekorja was also thought to be responsible for the creat...[i](You know you read this section, but you can't actually remember it. It is almost like something has deliberately erased it from your mind.)[/i]

 According to the records of Anglowen, Quekorja was slain during the Godhunt and its body discovered by the mage Linaniil. Linaniil managed to absorb a small portion of the god's power through a dangerous ritual. This tiny shard of power she acquired made her an archmage without peer, a testament to the sheer might of the gods.
```
译文：
```text
奎科加是时间和可能性之神。在埃亚尔关于奎科加的神话传说中，最突出的一点就是它们之间有着极大的矛盾，而在弑神之战之后的传说中它的形象远不如前。对此的猜测是奎科加自己可能十分爱好书写历史，指派了自己的记录者来记录自己的故事，但并没有证据表明有这样一个图书馆存在，因而这种理论被认为只是没有依据的臆测，没有实际证据的支持。另外还有一些不寻常的记录，本应是同一个作者在同一天写的，但其语调和对此神的描述却大相径庭。由于奎科加能够操控时间，因而有观点认为这些记录其实是来自别的时间线。这更加增添了奎科加的神秘。

 奎科加也被认为创……[i]（你记得你读过这段文字，但就是记不起其内容，就好像它是被有意从你的脑海中抹去了一样。）[/i]

 根据安格利文的记载，奎科加在弑神之战之中被杀死了，它的尸体后来被法师莱娜尼尔发现。她成功通过一个危险的仪式吸收了此神的一小部分力量，而就是这微小的力量也使她成为了无可匹敌的大法师。这也证实了诸神的力量是多么的强大。
```

## entry-03327
位置：tome-addon-dev.lua:28；section：tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Translation text checked.
Logs written to %s
```
译文：
```text
已检查翻译文件。
日志目录：%s
```

## entry-03328
位置：tome-addon-dev.lua:31；section：tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Translation text rearranged.
Logs written to %s
```
译文：
```text
翻译文件编排完成。
日志目录：%s
```

## entry-03329
位置：tome-addon-dev.lua:95；section：tome-addon-dev/superload/mod/dialogs/debug/AddonDeveloper.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Addon init.lua must contain a tags table, i.e: tags={'foo', 'bar'}
```
译文：
```text
插件init.lua必须包含tags表字段，例：tags={'foo', 'bar'}
```

## entry-03330
位置：tome-addon-dev.lua:109；section：tome-addon-dev/superload/mod/dialogs/debug/AddonDeveloper.lua；source_tag：_t；args_order：None；special：None

原文：
```text
There was an error uploading the addon.
```
译文：
```text
上传插件时发生错误。
```

## entry-03331
位置：tome-addon-dev.lua:118；section：tome-addon-dev/superload/mod/dialogs/debug/AddonDeveloper.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Addon update & preview succesfully uploaded to the Workshop.
```
译文：
```text
插件更新和预览图成功上传到Steam创意工坊。
```

## entry-03332
位置：tome-addon-dev.lua:119；section：tome-addon-dev/superload/mod/dialogs/debug/AddonDeveloper.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Addon update succesfully uploaded to the Workshop.
```
译文：
```text
插件更新成功上传到Steam创意工坊。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Arcane Blade	奥术之刃	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Brawler	格斗家	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Dreadfell	恐惧王座	T.PN.PLACE	places	nil	existing	core	
Dwarf	矮人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Facial features	脸部特征	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Library	图书馆	T.GAME.ENTITY	places	entity name	existing	core	城镇实体
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
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
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Sholtar	肖尔塔	T.PN.PLACE	places	nil	preferred	core	维护者于 2026-08-25 裁定统一为“肖尔塔”；“肖塔尔”和“肖塔”已被取代
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
Trollmire	巨魔沼泽	T.PN.PLACE	places	_t	preferred	core	任务与地点叙述统一；troll 指巨魔，不是食人魔，与 narrative.tsv 的 trollmire→巨魔沼泽 一致；“Of trolls and damp caves”是任务标题，不作同名处理；2026-09-16 用户裁决，由 existing 升为 preferred
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
age of pyre	烈火纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	global	1.8beta 的统一译法；替换“派尔纪”
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
derth	德斯镇	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
dwarf	矮人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
iron throne	钢铁王座	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactical	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 tactic 同义的变体
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
trollmire	巨魔沼泽	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	与同类手札标题统一；troll 指巨魔，不是食人魔
unknown	未知	T.UI.LABEL	ui	_t	preferred	global	未知条目/名称占位（15 处）
voratun	沃瑞钽	T.GAME.ENTITY	items	entity subtype	preferred	global	最高级金属材料（22 处）；与 iron 铁、steel 钢并列
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
