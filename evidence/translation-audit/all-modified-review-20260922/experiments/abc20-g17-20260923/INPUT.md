# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03813–entry-03852 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g17-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03813 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03813
位置：tome-orcs.lua:1599；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This cloak seems to incorporate a series of blades attached to various spring mechanisms.  Apparently the designer believed that the best defense was an active one.
```
译文：
```text
这件披风上布满了刀刃和机关。显然制作者认为“最好的防御就是进攻”。
```

## entry-03814
位置：tome-orcs.lua:1601；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source#'s %s #GOLD#lashes out#LAST#, cutting #Target#!
```
译文：
```text
#Source#的%s#GOLD#向外割去#LAST#，切开了#Target#！
```

## entry-03815
位置：tome-orcs.lua:1613；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
every third hit always crits.
```
译文：
```text
第三下攻击必定暴击。
```

## entry-03816
位置：tome-orcs.lua:1652；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#F53CBE#%s's shadow awakens!
```
译文：
```text
#F53CBE#%s的阴影觉醒了！
```

## entry-03817
位置：tome-orcs.lua:1666；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You move 3 spaces at once.
```
译文：
```text
一次走3格。
```

## entry-03818
位置：tome-orcs.lua:1671；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s summons a barrier of steam from %s %s!
```
译文：
```text
%s使用%s%s召唤出蒸汽屏障！
```

## entry-03819
位置：tome-orcs.lua:1693；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This intricate set of steamsaws lock together in a nearly indecipherable system.
They sure seem sharp though.
```
译文：
```text
这套蒸汽链锯以奇特的方式锁在一起，看上去非常锋利。
```

## entry-03820
位置：tome-orcs.lua:1719；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
summon a treant (5 turn cooldown)
```
译文：
```text
召唤一个树人（5回合冷却）
```

## entry-03821
位置：tome-orcs.lua:1728；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
On Taking Damage: Blindside the attacker (range 6).
```
译文：
```text
受伤触发：闪电突袭（范围 6）。
```

## entry-03822
位置：tome-orcs.lua:1736；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Attack speed increases with paradox, up to 250% at 1000 paradox.
```
译文：
```text
攻击速度随紊乱值增加，1000紊乱时为250%。
```

## entry-03823
位置：tome-orcs.lua:1740；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
There is an attached note.
 
'I've spilt the heartsblood of my work, feeling it pound, like a heart, in my palms.
Some people just can't let go until they've bled dry.'
```
译文：
```text
上面粘着一页笔记。

'我将我的心血之作分离，感受它的跳动，像心脏一样跳动，在我的手心里。
总有些人不到血流尽，不撒手。'
```

## entry-03824
位置：tome-orcs.lua:1773；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#PURPLE#%s activates and teleports away all nearby creatures!
```
译文：
```text
#PURPLE#%s启动，传送走了周围的所有生物！
```

## entry-03825
位置：tome-orcs.lua:1774；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#PURPLE#%s activates and increases %s's resistances!
```
译文：
```text
#PURPLE#%s启动，增加了%s的抗性！
```

## entry-03826
位置：tome-orcs.lua:1775；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#PURPLE#%s activates and increases %s's arcane dynamo power!
```
译文：
```text
#PURPLE#%s启动，增强了%s的奥术发电机的能力！
```

## entry-03827
位置：tome-orcs.lua:1791；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
How do these even work?
```
译文：
```text
这玩意到底怎么用？
```

## entry-03828
位置：tome-orcs.lua:1832；section：tome-orcs/data/ingredients.lua；source_tag：ingredient name；args_order：None；special：None

原文：
```text
lump of stralite
```
译文：
```text
斯莱特块
```

## entry-03829
位置：tome-orcs.lua:1835；section：tome-orcs/data/ingredients.lua；source_tag：ingredient name；args_order：None；special：None

原文：
```text
stack of herbs (viperweed)
```
译文：
```text
一束植物（蛇草）
```

## entry-03830
位置：tome-orcs.lua:1836；section：tome-orcs/data/ingredients.lua；source_tag：ingredient name；args_order：None；special：None

原文：
```text
stack of herbs (sessali)
```
译文：
```text
一束植物（延龄草）
```

## entry-03831
位置：tome-orcs.lua:1837；section：tome-orcs/data/ingredients.lua；source_tag：ingredient name；args_order：None；special：None

原文：
```text
stack of herbs (bilberry)
```
译文：
```text
一束植物（越桔）
```

## entry-03832
位置：tome-orcs.lua:1838；section：tome-orcs/data/ingredients.lua；source_tag：ingredient name；args_order：None；special：None

原文：
```text
stack of herbs (burdock)
```
译文：
```text
一束植物（牛蒡）
```

## entry-03833
位置：tome-orcs.lua:1839；section：tome-orcs/data/ingredients.lua；source_tag：ingredient name；args_order：None；special：None

原文：
```text
stack of herbs (goldleaf)
```
译文：
```text
一束植物（金叶）
```

## entry-03834
位置：tome-orcs.lua:1851；section：tome-orcs/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
lump of stralite
```
译文：
```text
斯莱特块
```

## entry-03835
位置：tome-orcs.lua:1852；section：tome-orcs/data/ingredients.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A lump of stralite.
```
译文：
```text
一块斯莱特。
```

## entry-03836
位置：tome-orcs.lua:1856；section：tome-orcs/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stack of herbs (viperweed)
```
译文：
```text
一束植物（蛇草）
```

## entry-03837
位置：tome-orcs.lua:1858；section：tome-orcs/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stack of herbs (sessali)
```
译文：
```text
一束植物（延龄草）
```

## entry-03838
位置：tome-orcs.lua:1859；section：tome-orcs/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stack of herbs (bilberry)
```
译文：
```text
一束植物（越桔）
```

## entry-03839
位置：tome-orcs.lua:1860；section：tome-orcs/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stack of herbs (burdock)
```
译文：
```text
一束植物（牛蒡）
```

## entry-03840
位置：tome-orcs.lua:1861；section：tome-orcs/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stack of herbs (goldleaf)
```
译文：
```text
一束植物（金叶）
```

## entry-03841
位置：tome-orcs.lua:1875；section：tome-orcs/data/lore/destructicus.lua；source_tag：_t；args_order：None；special：None

原文：
```text
INTRODUCING!

The most powerful, most fearsome, most awesome weapon ever conceived by giants, men, nature, or anything before us:

#{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY#{normal}#

Containing a warhead laden with explosive runes, alchemical reagents, vile curses, steel drake scales, ritch venom, and little slips of paper bearing most unkind statements about your target's mother

Travelling at a speed which could be charitably described as absurd, and uncharitably described as obscene

Launched with such force that its operator will need a fireproof suit to avoid immolation from the backblast alone (fireproof suit not included)

Absolutely guaranteed to destroy ANY autonomous entity it detonates against!  Orcs!  Dragons!  Golems smaller than a medium-sized village!

A MANDATORY addition to your home or airship!

For pricing, please discuss the matter with Kaltor, and then forget about it entirely.  If price is a factor for you, you almost certainly cannot afford DESTRUCTICUS.

#{italic}#(Disclaimer: We are not responsible for any injuries, deaths, or loss of property resulting from improper transport of DESTRUCTICUS.  We are not responsible for determining the proper method of transporting DESTRUCTICUS.  Additional missiles for DESTRUCTICUS are not available.  Accuracy at ranges greater than DESTRUCTICUS' blast radius is not guaranteed.  We are not responsible for any injuries, deaths, or loss of property resulting from DESTRUCTICUS changing direction in mid-flight.)#{normal}#
```
译文：
```text
隆重推出！

巨人、人类、大自然以及我们之前的一切存在所能构想出的最具威力、最令人胆寒、最震撼的终极武器：

#{bold}#毁灭号——狂妄的天空穿透者#{normal}#

弹头满载爆炸符文、炼金试剂、恶毒诅咒、钢龙鳞片、里奇毒液，以及写着对目标母亲最不客气问候的小纸条。

其飞行速度，客气地说叫荒诞不经，不客气地说简直骇人听闻。

发射威力极其惊人，操作员需自备防火服以防仅凭尾焰就被当场火化（防火服需自理）。

绝对保证摧毁其引爆所波及的任何自主实体！兽人！巨龙！体积小于中型村庄的傀儡！

您的住宅或飞艇之绝对必备良品！

关于定价，请与卡托尔面议，然后彻底忘掉这件事。如果价格对您是个需要考虑的因素，您几乎注定买不起毁灭号。

#{italic}#（免责声明：我们不对因毁灭号运输不当导致的任何伤亡或财产损失负责。我们不负责指定毁灭号的正确运输方式。毁灭号不提供备用导弹。不保证在毁灭号爆炸半径以外的精准度。我们不对毁灭号在飞行中自行改变方向所导致的任何伤亡或财产损失负责。）#{normal}#
```

## entry-03842
位置：tome-orcs.lua:1975；section：tome-orcs/data/lore/dominion-port.lua；source_tag：_t；args_order：None；special：None

原文：
```text
OPERATIONS PERFORMED:

-With information provided by "Sunny Day," we were able to secure an Allied Kingdoms supply ship during the brief window in which it was unguarded, with no personal casualties.  We technically broke our agreement (Taroggos has been adequately disciplined), but because the ship was carrying more useful materials than expected, we were able to take a hefty supply of troll-sized (or close enough to it) arms and armor, alongside lumber, furniture, and smaller stralite equipment which can be easily melted down and repurposed into something useful, before delivering the promised amount of cargo to "Vapor Trail."  Combined with the payment received from "Sunny Day," we made a significant profit and reinforced our relationship with "Vapor Trail."  (Our relationship with "Sunny Day" is of no consequence; repeat business was unlikely.)

-The last cargo ship I had sent home, the one with countless small crates and the order to confiscate them all and hold onto them for further instruction, contains one crate full of You-Know-What received as payment for a product received via Iron Throne smugglers.  This crate is labelled "47-C."  Dispose of the others, as they are [i]extremely[/i] thoroughly trapped.  The exchange with "Sherry Toll" was mercifully uneventful, and the goods provided appear to be functional.  With all due respect, Boss, if this doesn't get me a promotion, what will?

-Our contacts with the black market of Maj'Eyal and our establishment of a safe trading hub for their activity has continued to be immensely profitable, in addition to providing us an exploitable means of getting objects of our choosing into Maj'Eyal.  "Vapor Trail" has been an eager participant, and we've made a killing off selling Atmos absinthe to the Allied Kingdoms smugglers, as well as selling Elvala wine and brandy to them.  I'll be sending a ship full of our profits (useful metals, alchemical ingredients, slaves) back home on a bi-monthly basis; search the crew to make sure they haven't been lining their pockets, and keelhaul any you catch.

-Crew disobedience and morale continues to be something of a problem, despite regular floggings, but we're still retaining enough of them and getting enough use out of them.  That said, feel free to keep sending sentenced criminals our way - they're surprisingly productive as long as we give them enough booze and cheerblossom.
```
译文：
```text
行动记录：

- 根据“大晴天”提供的信息，我们趁一艘联合王国补给船短暂无人看守时夺取了它，而且没有人员伤亡。我们理论上破坏了约定（塔洛格格斯已经被妥当处罚了），但是因为船承载了比预期更多的有用材料，在我们运送了承诺的货物量到“汽化液之径”之前，我们获取了可观的，巨魔尺寸（或者接近）的补给物资，包括武器防具，以及木材、家具以及较为小型的，能够重铸成有用东西的斯莱特装备。加上从“大晴天”收到的支付，我们获得了可观的利润并且加强了与“汽化液之径”的关系。（我们与“大晴天”的关系无足轻重；毕竟不太可能再与他们做生意了。）

- 上一艘我送回家的货船，也就是那个载着无数小箱子的，接到命令没收全部货物，并扣押下来等待进一步指令的那艘。这艘船上面包括了一个满盛着“你懂的”的箱子，作为从钢铁王座的走私者那里以货物形式支付的报酬。这个箱子被标作“47-C”。其余箱子都处理掉，因为它们布满了[i]极其[/i]周密的陷阱。和“雪利酒收费站”的交易很幸运地没出岔子，货物看上去也很有用。头儿，如果这些功绩都不能让我升职，还有什么会？

- 我们与马基亚埃尔的黑市的那些合约，以及在那里建立一个安全的交易枢纽的行动持续创收大量利润。并且，这还让我们增加了一个有利的途径，让我们想要的东西进入马基亚埃尔。“汽化液之径”一直是一个热诚的参与者，我们靠向联合王国的走私者卖蒸汽牌苦艾酒以及埃尔瓦拉产的葡萄酒和白兰地大赚了一笔。我将每两个月送一艘船回来，满载着我们的获利（有用的金属、炼金术原料、奴隶）；在船员中搜查他们是否揩油了，如果你抓住了就都绑在船底拖行。

- 船员的不服从以及他们的士气不足是一个持续存在的问题。尽管我们经常鞭笞他们，但我们仍留住了足够的人手，也从他们身上得到了不少用处。也就是说，请继续多送点服刑的犯人来我们这儿：只要我们给足够的酒类和鼓舞之花，他们就会努力工作了。
```

## entry-03843
位置：tome-orcs.lua:1993；section：tome-orcs/data/lore/dominion-port.lua；source_tag：_t；args_order：None；special：None

原文：
```text
OVERALL ANALYSIS:

Boss, if there's one thing I can say, it's that you didn't make a mistake by pardoning me and my crew.  The materials I've shipped home have surely been invaluable for our preparations, and the moment the top brass decides they want to start the invasion, I can start spiking the outgoing liquors and cheerblossom with time-delay potions of your choice, crippling the Allied Kingdoms from within by starting a plague or turning every minor lawbreaker into a berserk madman.  If nothing else, the You-Know-What will be [i]very[/i] useful when push comes to shove.

As per your orders, we've restricted most of our intervention to sabotaging the Allied Kingdoms, but I wonder if some amount of focus on the orcs would be helpful.  A band of them has recently emerged from the Clork Peninsula, victorious over Sun Paladins and Atmos alike; we've lost contact with "Sunny Day," and "Vapor Trail" has kept exports to a minimum for fear of detection.  If we don't do something about this soon, they may become a bigger obstacle than the Allied Kingdoms.

I await your reply - and more dried meat, my crew loves the stuff and these smugglers can't be arsed to bring us something so mundane.
```
译文：
```text
总体分析：

头儿，如果我要说什么的话，那就是你饶恕我和我的船员是对的。那些我运回家的材料确实对我们的准备很有价值。只要高层决定开始入侵，我就能在外运的酒类和鼓舞之花中掺入你指定的延时药剂，通过引发瘟疫，或把每个犯点小罪的人都变成狂暴疯子，从内部瘫痪联合王国。无论如何，那个“你懂的”在最终关头会[i]非常[/i]有用。

根据你的命令，我们已把大部分干预行动限制在破坏联合王国上，但是我觉得多一些对于兽人们的关注也可能有好处。一帮兽人最近从克拉克半岛出现，战胜了太阳骑士和气之部族；我们已失去与“大晴天”的联系，而“汽化液之径”害怕被觉察，把他们的出口活动限制在最小。如果我们不赶紧做些什么的话，他们可能变成比联合王国更大的阻碍。

我等待你的回复，以及更多肉干，我的船员喜欢这个，而那些走私者懒得给我们送来这种平凡的东西。
```

## entry-03844
位置：tome-orcs.lua:2012；section：tome-orcs/data/lore/emporium.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#CLOGGING NO MORE!#{normal}#
If steam-vent congestion ails you, avail yourself of:
 
#{italic}#[An illustration depicts a rectangular glass bottle, labelled "DR. RAGLUK's DECLOGGING DRAUGHT".]#{normal}#
 
MADE WITH LOVE, CARE, AND THE PUREST MINERALS FROM THE STEAM QUARRY
 
Just one capful will cleanse your pores, flushing toxins out with the steam!
 
ALSO EFFECTIVE FOR: Headaches, nausea, ennui, fatigue, aches and pains, and general malaise!
 
#{italic}#[A disclaimer occupies the bottom margin of the poster, in print so small you doubt the giants would be able to read it.]#{normal}#
 
WARNING: This product has been determined by the Council of Health Authority to be correlated with the following conditions: Inverse vertigo, increased hair flammability, non-vaporous sweating, night terrors, liver dysphoria, headaches, miner's lung, brainlock, day terrors, mitosis, visions of a great butchered being, miner's elbow, skeletal emancipation, gastrointestinal infamy, brittle kidney, pinaciphobia, decreased global speed, teleportitis, miner's tongue, merged nostrils, an ancient and foul curse, lowered steam pressure, fat burning (literal), ocular feathering, Orcish body odor, arcane disruption, gravity loss, bloodlock, malfeasance, rectal carpeting, nihilism, mid-evening terrors, knee rust, and minor clogging of the pores.
```
译文：
```text
#{bold}#不再堵塞！#{normal}#

如果蒸汽孔阻塞困扰你，请用这个来帮你：

#{italic}#【一幅插图描绘着一个长方形的玻璃瓶，标签上写着“拉格卢克博士的清淤药水”。】#{normal}#

用爱、关怀和蒸汽矿场最纯净的矿物质制成！

只要一瓶盖的量就能清洁你的气孔，和蒸汽一道排出毒素！

也对以下症状有效：头痛、恶心、倦怠、疲劳、各种疼痛，以及广泛性的不适！

#{italic}#【一个备注占据了海报的底部边缘，印刷字体太小以致于你怀疑巨人们能不能看到。】#{normal}#

警告：经卫生理事局评议，此产品与以下症状有相关性：反转性眩晕、毛发可燃性增加、非蒸汽性出汗、夜间惊恐发作、肝火、头痛、尘肺病、脑锁、日间惊恐发作、有丝分裂、关于巨大被宰割物的幻觉、矿工肘、关节松脱、肠胃糜烂、肾脆症、尖端恐惧症、整体速度下降、随机传送症、矿工舌、鼻孔合并、某个古老又邪恶的诅咒、低蒸汽压、脂肪燃烧（字面意义）、眼部羽化、兽人体味、奥术干扰、重力丧失、血锁、渎职、直肠沉积、虚无主义、傍晚惊恐发作、膝盖生锈，以及气孔的轻微堵塞。
```

## entry-03845
位置：tome-orcs.lua:2041；section：tome-orcs/data/lore/emporium.lua；source_tag：_t；args_order：None；special：None

原文：
```text
CLOSING SALE
for
KALTOR's FIREARMS, ARMOR, AND OTHER MARTIAL SUNDRIES
 
It is with a heavy heart that I must announce our closing.  After over twenty years of service, I am shutting my doors - the people of the Atmos Tribe apparently wish to trust the Guard with their well-being, and the Guard chooses to maintain the weapons it already has rather than purchase things like the #{italic}#BRILLIANT AUTO-LOADING ORC EXPELLER#{normal}# (only 30 gold!), or the #{italic}#PRESSURE-ENHANCED SLASHPROOF COMBAT SUIT#{normal}# (only 450 gold!).  I even offered discount options such as the #{italic}#LIL SURPRISE#{normal}# (now only 15 gold!), and yet the city would have none of it.  It would seem my services, and my talents, are simply not wanted.
 
Even if you have no fear of the orcish tribes, ritch swarms, and other assorted threats that lurk just outside our city walls, please consider purchasing some of my wares.  They are truly beautiful displays of craftsmanship, and would do well as a desk sculpture or (if properly disarmed) a child's toy.  If nothing else, you will be ensuring that a once-proud artisan with great love and respect for his craft need not resort to begging on the streets.
```
译文：
```text
卡托尔的军火、护甲和军用杂货店即将停业

我心情沉重地宣布我们店的停业。二十年的经营后，我要关门了————气之部族的居民显然想要用他们的全身心信任守卫们，而守卫们却想维持原来的配备，而不是去购置像是“#{italic}#光辉灿烂的自动装填的兽人驱除器#{normal}#”（仅售30金币！）或者是“#{italic}#增压的防挥砍的战斗服#{normal}#”（仅售450金币！）。我甚至推出了像是“#{italic}#小小大惊喜#{normal}#”（现在仅售15金币！）这样的优惠，但是这个城市不愿意买任何一件。看上去我的竭诚服务和才华横溢真的没人需要。

即使你们一点也不怕那些兽人部落、里奇虫群和在我们城市外游荡的各种威胁，请还是考虑一下要不要买我的一些东西。它们确实美丽得体现了匠人精神，而且可以做好的书桌摆设品或者是孩子的玩具（如果做好了保险措施的话）。如果你愿意伸出援手的话，你可以让一个热爱又尊重他的作品，曾经自豪的工艺大师不再被迫流落街头乞讨。
```

## entry-03846
位置：tome-orcs.lua:2073；section：tome-orcs/data/lore/emporium.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#KEEP THE PRESSURE UP!#{normal}#
#{italic}#An announcement on power consumption, paid for by the Council of Geothermal Authority#{normal}#

As per our previous announcements, the geothermal vents of the Steam Quarry have begun to taper off in output.  While our geologists and military consider all available options for finding new vents (or alternative sources of steam power), we need YOUR cooperation to keep the pipes from running dry!  Here's how you can help make sure we have enough steam for everyone:

-Cook the old-fashioned way - with flame magic, or a firewood stove.  Flash-steamers, although certainly a convenient way of preparing food, are VERY inefficient.  For a free handbook on delicious and easy-to-learn recipes for a conventional or pyromancy-based stove, simply come to the Council of Geothermal Authority offices and take one from the lobby.

-Remember to shut off your appliances when you're done with them!  A full 5% of our power usage is estimated to be from washing machines, mills, carousels, generator-powered lighting, and other such devices left plugged in when not in use.  When you are done using an appliance, make sure it has been deactivated; to be completely sure, our experts recommend shutting off the valve entirely, then disconnecting the appliance and placing a standard cap over the output pipe.

-Have your pipes checked regularly.  Leaking valves and loose fittings can consume tremendous amounts of steam pressure; you are only required to have your home steam-pipes inspected every three years, but additional inspections are available at no charge (once every six months).  Volunteering for these inspections can reduce your geothermal consumption, and fees, dramatically.

-Use your own steam!  With regular exercise and a good diet, you can create your own power by wearing a collection suit, and plug the pressurized reserve tanks into your home intake valves to reduce the amount of power drawn from the geothermal system by over 40% (depending on personal production).  Short-term use of declogging tonics may help, but long-term use is generally ill-advised.

-Do NOT pressurize tanks from the tap and sell them to others!  This is a violation of Council law, punishable by a fine of up to 3,000 gold and up to four years in prison, per tank.

Thank you for helping ensure we ALL have power, while we work on curing this shortage!
```
译文：
```text
#{bold}#保持蒸汽压力！#{normal}#

#{italic}#地热能源理事局关于能源消耗的通知#{normal}#

我们之前的通知表明了蒸汽矿场地热出气口的输出在逐渐减少。在我们的地质学家和军方正在考虑其他寻找新出气口（或其他替代性蒸汽能源）的方案时，我们需要你们的合作来防止管道枯竭！为了大家都有足够蒸汽用，您可以通过以下的方法做出贡献：

- 用老式方法烹饪 —— 用火焰魔法或是烧柴的炉子。闪蒸炉尽管是准备食物的快捷方式，不过确实能源效率很低。如您需要免费的《传统或魔法炉子，美味易学的食谱手册》，请到地热能源理事局办事处的大堂领取一份。

- 当您用完蒸汽设备后请记得关闭！据统计，我们足足5%的能源消耗来源于用完洗衣机、磨坊、旋转木马、蒸动灯和其他类似设备不拔插头。当您用完设备后，请确认断气；如果要完全确定，我们的专家建议把气阀给全关掉，然后断开与设备的连接，把一个标配的盖子放在出气管上。

- 经常检查您的管道。泄漏的阀门和松散的接头会消耗大量的蒸汽气压；您家里的蒸汽阀只需要每三年检查一次，但是附加的检查是免费的（每六个月一次）。自愿报名这些检查会让地热消耗和费用大大减轻。

- 用您自体的蒸汽！只要定期锻炼，合理安排膳食，您只要穿着收集服就可以自己供能，然后把上面的压缩储存箱接在家里的进气阀上就可以减少40%来自地热系统的消耗（根据个人生产量而不同）。短期使用清淤药水可能有助于提高产量，但不建议长期使用。

- 请勿从地热系统的气管里装气卖给他人！这违反了理事局制定的相关法律，违者每违法售出一罐将遭受最高3000金币罚金，并处四年监禁。

感谢您为保证大家都能用上能源而出力，与此同时我们也在着手解决能源短缺的问题！
```

## entry-03847
位置：tome-orcs.lua:2141；section：tome-orcs/data/lore/gem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
"...thing on? Okay, good. This is Haze Commander Parmor of the Geothermal Exploratory Mole, on a mission to..."  She sighs. " 'Find the Loyalist and arrange for our safe transport to his refuge, offering him his previous terms of agreement.' Which is Council-speak for 'flee in terror to the only thing that could bail us out of this mess, and bring the Eye with us.' Personally, I'm not keen on putting our fates in the hands of some nutter who lives underground and..." Indistinct grumbling. "...not even my damn job, I didn't sign up to be some politician's valet--"

#{italic}#(You hear a door opening, and another voice speaks.)#{normal}#

"Captain, the tea-maker isn't working!  Get someone on that, post-haste!"

#{italic}#(The door closes.)#{normal}#

"...Yeah, Councillor Tantalos is getting his tea as soon as he can un-kick the hornet's nest that got us into this chaos.  Moving on...  departure was on time, projected journey to the Loyalist's last known position is underway, making a tunnel there from right under the palace.  All systems functioning, except for the tea-maker, and I can't give a slag about that.  End log."
```
译文：
```text
“……什么事？好，好的。这里是地热探测鼹鼠GEM，阴霾指挥官帕默，我们正在执行的任务是…”她叹了一口气“上面写着，‘寻找忠诚者，将我们安全地运送到他的避难所，并向他提供我们之前在协议中许诺的东西。’如果不用官腔的话，就是‘在恐惧中逃跑，逃向唯一能够把我们从这篇混乱中解救出来的家伙那里，别忘了把“眼睛”带走。’从个人角度，我可不想把我们的命运，交到某个生活在地底下的狂人手里，而且…”含糊不清的抱怨“…这根本他妈的不是我的工作，我可不是某些政治家的仆人——”

#{italic}#（你听到了开门的声音，有另一个人的声音响起）#{normal}#

“船长，沏茶机坏了！快叫人来处理，马上！”

#{italic}#（关门声）#{normal}#

“……是的，坦塔洛斯议员还他妈的想喝茶，要不是他刚刚给我们捅了个大马蜂窝，把我们搞的一团糟。继续……我们的出发时间很准时，正在准备前往忠诚者的上一个位置，我们将会从宫殿下方挖一条隧道过去。所有系统工作正常，除了沏茶机，去你妈的沏茶机。日志结束。”
```

## entry-03848
位置：tome-orcs.lua:2159；section：tome-orcs/data/lore/gem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
"...for posterity!  Let's make sure future generations can hear the moments of history being made!" You hear the voice of Councillor Tantalos again... and then you hear a very strange voice, one that's all too clear. Even with the device playing it, it sounds like it's coming from inside your own head.#{normal}#

"Yes, yes, good idea. This is an important day, for both of us - no, for Eyal...  You've brought what I asked for so long ago, then?"

"Of course!  It's just--  bring the cart around here!"  (Clanking and grinding.)  "Open it up, if you wish."

"No need.  I can feel its power, it's so familiar and yet so new...  This could only be the Eye of Amakthel Himself!  It's beautiful, and all will know its beauty..."

"Er...  splendid, I assume!  This is the beginning of a long and beautiful partnership between the Atmos and...  your people!  Shall I go back up and tell them we're ready for them, and you're ready to handle the Orc situation? They're, ah, rather eager to come down here--"

"GO FORTH, MY HERALD. TELL THEM ALL ARE WELCOME."

"Wh-what are you--"  #{italic}#Screams in the background.  Gurgling.  Crashing.  A distant, bestial roar.#{normal}#

"AMAKTHEL WILL REWARD YOU FOR YOUR SERVICE AS YOU DESERVE." More crashing.  "YOU SHALL BE BLESSED WITH A BETTER NEW FORM.  A BETTER NEW MIND.  ALL YOUR PEOPLE ARE WELCOME TO..."

#{italic}#(You hear Parmor's voice again.)#{normal}#  "Slag it, RUN!  Grab everything and--"  (The recording ends.)

```
译文：
```text
“……为了繁荣！让我们用声音记录下，这个值得被子孙后代铭记的，改变历史的时刻！”你又听到了坦塔洛斯议员的声音……但你还听到了另一个奇怪的声音，一个清晰的声音。尽管是机器在播放着声音，但这段声音就像是从你的脑海里传来的一样。#{normal}#

“是的，是的，这是一个好主意。这将会是一个重要的日子，对我们——不，对整个埃亚尔都值得铭记……那么，你今天把我一直以来都要的东西带来了？”

“当然了！它就在——来啊，把车推上来！”（叮叮当当的声音）“如果您乐意的话，请你亲自打开看一下。”

“不用了。我能感受到它的力量，多么熟悉而又新鲜的力量……这只能是阿马克泰尔本人的眼睛！它是多么的令人沉醉啊，很快，所有人都会感受到它的美丽…”

“呃……太棒了，我保证！这将会是气之部族和……你的人民之间漫长而友好的友谊的开始！我这就回去告诉他们，我们已经准备好了，并且你也准备好处理兽人问题了，对吧？他们，啊，一定会很愿意亲自来这里——”

“去吧。我的传令官。告诉他们，我十分欢迎你们。”

“你，你在——” #{italic}#传来一声声尖叫。血液流淌之声。猛烈的撞击声。然后是一阵遥远的，野兽般的咆哮。#{normal}#

“这是阿马克泰尔在亲自奖励你对他的服侍，是你所应得的荣耀。”更多的撞击声。“这是神给你的祝福。一具更美好的全新的身躯。一个更美好的全新心智。你的人民都可以得到这份…”

#{italic}#（你听到了帕默的声音。）#{normal}#  “操，大家快跑！带上所有东西，快——”（纪录终止了）

```

## entry-03849
位置：tome-orcs.lua:2195；section：tome-orcs/data/lore/gem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#(You hear loud, mechanical rumbling; in the distance, you hear sounds of struggling and bludgeoning, swords slicing through flesh, steamguns being fired, and shouts of pain from giant and horror alike.  Parmor sounds panicked.)#{normal}#

"Mayday, mayday, we are bailing out!  Tantalos is gone, and we are NOT going back for him!  Scrap the tunnel to the Palace of Fumes, scrap the entire damn council, we're getting as far away from here as we can--"  Loud hissing.  "MOTHER OF--!"  Grunts, squishing, slashing.  "Flooring it all the way to the damn Sunwall, we're taking the first farportal off this continent whether those tinies like it or not!  Guess this technically counts as treason, mutiny, whatever, but if the Council's hearing this, BLOW IT OUT YOUR STEAM-HOLES, WE'D RATHER LIVE!  Altitude rising, surface approaching, this is H.C. Parmor signing off--"
```
译文：
```text
#{italic}#（你听到了巨大的，机械的轰鸣声。在远处，你听到挣扎和殴打的声音，听到利刃刺破血肉，蒸汽枪的枪声，以及巨人和恐魔发出的痛苦怒吼。帕默的声音听起来惊慌失措。）#{normal}#

“求救，求救，我们在撤离！坦塔洛斯完蛋了，我们绝对不会再回去救他的！去你妈的烟雾宫殿的隧道，去你妈的天杀的议会，我们必须赶紧跑，越远越好——”巨大的嘶嘶声。“狗娘——！”撞击声，挤压声，破碎声。“给我朝太阳堡垒前进，我们要使用这个大陆上的第一个远行传送门，不管你们这些家伙喜不喜欢！我可不管这是不是什么叛国、谋反，去他妈的，如果你们议会在听着的话，放你娘的蒸汽孔，老子只想活下去！海拔上升，准备接近地面，这里是 H.C. 帕默，播报完毕——”
```

## entry-03850
位置：tome-orcs.lua:2203；section：tome-orcs/data/lore/gem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Too many of them.  Couldn't pull more Atmos back in, wasn't safe, couldn't tell them from the others.  Hope we've got enough fuel to get us to the surface.
```
译文：
```text
他们太多了！我们没法救回更多的同胞，这太危险了，已经没法把他们和那些家伙分开了。希望还有足够的燃料让我们可以钻出地面。
```

## entry-03851
位置：tome-orcs.lua:2218；section：tome-orcs/data/lore/internment-camp.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#To: Guard Captain Galsamae
From: Administrator Quellop#{normal}#

It's good to see that you and your followers have arrived safely! Hopefully you're settling in all right; thank you for coming, and pass my thanks on to the Elvala diplomats for getting you here on such short notice. I hope this is the first step in your kind - you Ogres, of course, but also the Shaloren who sent you here - joining forces with the Allied Kingdoms.

There are no Ziguranth here in the Far East, and the orcs in this camp have been compliant so far, on account of Mindwall's elaborate illusions. It's the most humane way to deal with them that we've found so far - we hope that his influence will have a permanent calming effect on them over time, but until then, they're happy and docile in their little dream-world. All you have to do is protect against any stragglers outside the walls looking to break their kin out of here, and patrol the halls to make sure any orcs who've managed to shake off the illusions are swiftly apprehended and dealt with. This should be a pretty easy job - if you need any particular help or provisions, though, let me know and I'll do what I can!

Sincerely,
Administrator Quellop

#{bold}#---#{normal}#

#{italic}#To: Administrator Quellop
From: Guard Captain Galsamae#{normal}#

We need four more chairs in the break room.

-Galsamae

#{bold}#---#{normal}#

#{italic}#To: Guard Captain Galsamae
From: Administrator Quellop#{normal}#

I'm sorry, but we can't really afford that, as the budget for amenities and luxuries is stretched pretty thin here as-is. Please try to keep your requests limited to necessities - even with Last Hope's merchants competing on price, the security over by the farportal means it's still not cheap to get things here.

Regretfully,
Administrator Quellop
```
译文：
```text
#{italic}#致：卫队队长加尔萨迈
来自：管理员夸洛普#{normal}#


很高兴看到你和你的随从已经安全抵达！感谢你的光临，也感谢埃尔瓦拉的外交官能在这么短的时间内联系到你过来，希望你能在这里安顿下来。我希望这将会成为你们一族——当然，不仅是你们食人魔，也包括派遣你们过来的永恒精灵——与联合王国的合作部队的良好的第一步。

在远东这里没有伊格兰斯。得益于意念之墙精巧的幻象技术，关押在这里的兽人都十分顺从。到目前为止，这是我们找到的和他们打交道的最人道的方法——我们希望，随着时间流逝，他的能力最终可以对这些兽人起到永久的镇定效果。不过，在那之前，他们都会这样傻乎乎地，温顺而快乐生活在梦中的小小世界里。你所需要的就是守住这里的围墙，不能让外部的游荡的兽人进来救走他们的同族。同时，还要巡逻这里的大厅，确保那些成功脱离幻象的兽人被我们迅速逮捕和解决。这应该会是一件非常容易的工作——但是，如果你需要任何特别帮助或补给的话，请立刻告诉我，我将尽我所能帮助你！

此致，
管理员夸洛普

#{bold}#---#{normal}#

#{italic}#致：管理员夸洛普
来自：卫队队长加尔萨迈#{normal}#

请在休息室里增加四把椅子。

——加尔萨迈

#{bold}#---#{normal}#

#{italic}#致：卫队队长加尔萨迈
来自：管理员夸洛普#{normal}#

很抱歉，但是我们实在买不起这些。我们能花在设施和非必需品上的预算，和往常一样，已经被压缩到了极限。请尽可能只需求必需品——尽管最后的希望的商人们用低廉的价格相互竞争，但考虑到远行传送门的严密安保，在这里要想买到东西仍然十分不便宜。

充满抱歉，
管理员夸洛普
```

## entry-03852
位置：tome-orcs.lua:2523；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I'm not going to lie to you: things aren't going great.  Between the Doomelf escape incidents, the deaths of Khulmanar and a great deal of our more expensive combatants at the hands of the Anomaly, and the disappearance of the First Duathedlen, we've been set back pretty far this year.  As such, your orders are simple: lay low.  Stay out of sight, and conduct passive observation until we can get a foothold and a new plan.

And regarding the First Duathedlen - quit your murmuring right now.  I've seen his track record, and I know most of you know it too, which is why we can safely say that despite his... nature, his loyalty is [b]not[/b] in question - we can assume his abrupt cessation of communication is a necessary part of his investigations, and not him going rogue.  If you see him, tell us of his whereabouts, but do not interfere.

[i](The letter is signed with an unreadable but formal-looking demonic seal.)[/i] 
```
译文：
```text
我准备实话实说：事情的进展并不顺利。除了魔化精灵的逃亡事件之外，还有库马纳的死，我们众多精英卫兵在那场异常中的牺牲，以及第一位多瑟顿的失踪…我们今年的损失已经够严重了。所以，给你们的命令很简单：保持低调。远离敌人的视线，进行被动的观察，直到我们可以获得一个新的立足点，开展新的计划。

还有，有关第一位多瑟顿的事情——你现在就别抱怨这些了。我看到过他的记录，我知道你们大部分人也都看过，这就是为什么我可以放心的说，尽管他的…本性如此，但他的忠诚是[b]无可挑剔[/b]的——我们可以假定，他的突然失联是他进行的调查的一个重要组成部分，而并不是他叛逃了。如果你看到了他，请告诉我们他的位置，但千万不要干涉他的行动。

[i]（这封信是用一个难以辨认，但看起来很正式的恶魔印章签署的。）[/i] 
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Atmos Tribe	气之部族	T.PN.FACTION	society	faction name	preferred	dlc	Embers of Rage 阵营专名；统一为“气之部族”（叙事文本曾作“气之部落”），与气之部族 NPC/叙事一致
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Blindside	闪电突袭	T.GAME.TALENT	talents	talent name	preferred	core	技能会以极快速度瞬移至目标身边并攻击；按机制译作“闪电突袭”，不按普通动词字面译作“偷袭”
Brilliant Auto-loading Orc Expeller	精良的自动装填式兽人驱逐装置	T.GAME.ENTITY	items	entity name	existing	dlc	Embers of Rage 商品实体名；重复运行时键统一
DESTRUCTICUS	毁灭号	T.GAME.ENTITY	creatures	_t	preferred	dlc	Embers of Rage 武器“裂天者 毁灭号”的简称；欢呼与叙词统一为“毁灭号”，不写作“毁天灭地”
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Hairs	发型	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Paradox	紊乱值	T.GAME.RESOURCE	resources	_t	existing	core	
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Steam Quarry	蒸汽采石场	T.PN.PLACE	places	entity name	preferred	dlc	Embers of Rage 地点，地热阀所在；与“蒸汽商场”区分
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Tantalos	坦塔洛斯	T.PN.PERSON	society	entity name	preferred	dlc	气之部族首席议员；统一书信署名、叙事引用与实体名，不写作“坦塔罗斯”
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
book	书	T.GAME.ENTITY	items	entity type	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
cleanse	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key，与 cleansing keyword 同一 cohort；不约束动作、技能说明或其他语境
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
gravity	重力	T.GAME.DAMAGE	combat	damage type	existing	core	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
iron throne	钢铁王座	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mechanical	机械	T.GAME.ENTITY	creatures	entity type	existing	dlc	Embers of Rage 实体类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
palace of fumes	烟雾宫殿	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	Embers of Rage 地点手札类别
paradox	紊乱	T.GAME.TALENT	talents	talent type	preferred	core	时空技能类别名；资源数值在其他语境使用“紊乱值”
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
potion	药水	T.GAME.ENTITY	items	entity type	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steam quarry	蒸汽采石场	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
steamsaw	蒸汽链锯	T.GAME.ENTITY	items	entity subtype	existing	dlc	Embers of Rage 实体子类型
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
