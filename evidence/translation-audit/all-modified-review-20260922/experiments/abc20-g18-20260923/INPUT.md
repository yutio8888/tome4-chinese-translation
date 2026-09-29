# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03853–entry-03892 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g18-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03853 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03853
位置：tome-orcs.lua:2545；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The anti-scrying nexus you folk set up here is damn impressive, as is the time-release pseudo-rune powered by it - hard to find a spare spot on my skin for it, but I can feel it working for a few days after I'm back in Maj'Eyal.  Great for making sure we can get away from the West portal and disperse without the A.K. catching on or tracking us to a common point of convergence.

Got a proposal, though.  With a few little tweaks, I could make one that doesn't require the bearer's consent to use.  You aren't the only ones buying slaves from me, and when I get a customer who wants them taken right back to the West, we have to do the anti-scrying enchantments ourselves.  I don't know if you've noticed, but proper mages still aren't easy to come by - I barely made a profit last time I did it.

Say the word, and I'll send over the temporary rune design so you can set the nexus to recognize it.  No charge from me - if you accept it, it'll pay for itself.

[i](You assume the elaborate, glowing shape below is an Ogric equivalent to a signature.)[/i] 
```
译文：
```text
老兄，你们设置的反侦测水晶真他妈够劲的，还有这个被它驱动的延时释放的伪符文——我的皮肤上没有什么空位了，但我能感受到，这玩意儿在我回马基埃亚尔之后几天都能用。这肯定能保证，我们可以安心从西部的传送门逃走，绝对不会被联合王国抓到，他们也肯定没法追踪我们的痕迹。

现在，我现在有一个想法。只要稍微整一下，我就可以让这玩意儿不需要使用者的意愿就能工作。你不是唯一一个从我这里买奴隶的人，要是你想把他们带回西部去的话，我们可得好好做点反侦测的准备。我不知道你有没有注意到，但合格的法师如今还是很难请到——上次，我差点把老本都给赔光了。

只要你一句话，我就把这个临时的符文设计发给你，你设置好水晶就能用了。我不收你的钱——只要你愿意用，这笔投入很快就能回本。

[i]（你猜想，下面画着的这个精心设计的，闪闪发光的图案，在食人魔文化里有着和签名一样的用途。）[/i] 
```

## entry-03854
位置：tome-orcs.lua:2559；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
We get it: it's our fault the farportal mailing system isn't perfect.  Our people are still working on undoing that jury-rigged configuration that keeps your portal from transporting anything that isn't living - and if we get it wrong, that means people start getting teleported into walls again.  It's already a damn miracle you can get through the portal without coming out naked on the other side, let alone still carrying your backpacks and all their contents.

In the meantime: we're still losing a few letters going through the mailing system, and the lost ones could end up teleported to pretty much anywhere.  They could end up ten feet from the portal, or they could end up right in some A.K. busybody's hands, or they could just warp themselves right up Urh'Rok's nose for all we know.  Likewise, anything written on those notes could end up exactly where you don't want them, wherever that might be.

My point is, when you're writing those letters, write them like King Tolak's looking over your left shoulder and your grandmother's looking over your right - or at least show SOME semblance of subtlety.  Don't complain about the prices of "illegal potions," complain about "extra-strength medicine."  Don't ask about safety accommodations for "slaves," ask about "private servants."  And please, for the love of Linaniil, [i]stop calling the farportal a farportal![/i]  The A.K. doesn't even know we [i]have[/i] this thing yet, and we don't want to give them any ideas on where or how to start looking.  Call it a courier, or a pack golem, or a trained uruivellas for all I care.

-Korbek

PS: Yes, I'm breaking my own rules with this letter - you idiots clearly don't understand subtlety, so I can't assume you'd understand a subtly-written letter.  Yes, I'm aware there's a chance this letter could end up in enemy hands.  No, the irony of that situation would not be lost on me.  Yes, I will hurt whoever thinks they're clever by bringing up any of the preceding.
```
译文：
```text
我们知道：远行传送门邮递系统并不完美这件事当然是我们的过错。我们还在努力修复那个让传送门无法传送任何非活物的临时配置——如果我们搞砸了的话，那么很快就会又有人被传送到墙里了。你能够这样穿过远行传送门，而不是裸体出现在另一边，包里的东西都完好无损，已经他妈的是一件奇迹了，好不好。

与此同时：我们的邮递系统仍然会丢失几封信，这些丢失的邮件可能会出现在任何地方。据我所知，可能会出现在传送门十英尺以内的地方，也有可能出现在某个联合王国好事者的手里，还有可能出现在乌鲁洛克的鼻子底下，都有可能。也就是说，你写的每一封信都有可能出现在你最不希望出现的地方，不管那是多么遥远的地方，明白吗。

我想说的就是，当你写信的时候，请你想象一下，托拉克国王就在你左边看着，你奶奶站在你右边看着——或者，至少你得明白什么叫隐晦一点，好吗？别再抱怨“非法药剂”的价格了，你能说“大力药”吗？别再讨论使用“奴隶”的安全设施了，可以用“私人仆人”这词吗？还有，拜托，为了莱娜尼尔的爱，[i]别再把远行传送门叫做远行传送门了，好吗！[/i]联合王国甚至还不知道我们[i]有[/i]这个东西，可以不要再给他们侦查的线索了吗？随便你叫他什么，快递员，邮递傀儡，训练好的乌尔维拉斯，随你怎么说都行，拜托了。

——库贝克

注：是的，我知道我自己这份信打破了规则——你们这些白痴连隐晦的重要性都不知道，我怎么指望能用一份隐晦的信让你们明白？是的，我知道这份信也有可能落到敌人手里。不，别指望你能用这个场景的讽刺性来笑话我。是的，谁敢列出以上我所说的任何一条，来显示自己很聪明，我就打烂你的嘴。
```

## entry-03855
位置：tome-orcs.lua:2577；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i](You see here a rotting human hand in a black leather glove, severed at the wrist.  It is still clutching a cracked artifact resembling an Orb of Many Ways, with a note folded up between the orb and its palm.)[/i]

"Drew the short straw" for the calibration [i]my entire ass.[/i]  That cheat used translocation magic and everyone there knew it.  If there's one thing I miss about the Ziguranth, it's that with them around, you only had to watch for sleight-of-hand and wear a mind-caging cap to avoid getting ripped off.

Speaking of ripoffs, why are we trusting this corpse-lover anyway? I guess it WOULD cost more to make a fake this convincing than we paid for it, but...  why would Tannen have made a portal that only works on the living, then used it to pay off a necromancer, [i]the only type of person who'd call that a downside?[/i]

Well, I guess that's what made him a [i]mad[/i] alchemist, and not some rich potion-brewer living comfortably.  Not like anyone can ask him now, except for who we got this altar from.

Anyway...  Korbek, if you're reading this, it means those crotch-heights screwed up again.  Send them back the orb, and hopefully it'll tell them what they need (well, as far as I'm concerned, [i]hopefully[/i] it'll blow them apart).  You got the calibration right on your end, and your poorly-disguised thugs are doing just fine (and stop with the illusions, it's just insulting, we don't care who or what you are as long as your gold glitters).  We just need to get the signal lock straight on our side, and we'll be able to fill the order you sent over, and then some.

Seriously, though, I'm writing this note so even if I get killed from this, I'm doing you a favor.  If I'm dead, I'd appreciate you showing your gratitude by making sure that ankle-biting son-of-a-ritch has played his last game of musical straws.

```
译文：
```text
[i]（你看到了一只被黑色皮手套包裹的腐烂的人手，手腕被切断了。它的手里拿着一个破碎的神器，样子就像是多元水晶球，水晶球和它的手掌之间夹着一张纸条。）[/i]

“抽到签的人负责矫正传送门”[i]我的屁股[/i]。大家都知道，那个作弊的家伙肯定使用了换位魔法。如果说我有什么怀念伊格兰斯的地方的话，那就是如果他们还在，你只要能看穿那些家伙的手上功夫，戴上一顶抗精神攻击的帽子，就不会被人狠宰一通。

说到宰人，我们干嘛要信任那个恋尸癖？我知道，如果真的是造假的话，以我们所付的代价，这造假的成本未免也太高了，但是……为什么泰恩在制作了一个只能用来传输活物的传送门之后，把它交给了一个死灵法师来偿债，[i]这是世界上唯一一个会把这件事看做致命缺陷的家伙？[/i]

好吧，我知道，这就是为什么他是一个[i]疯狂炼金师[/i]，而不是一个安居乐业的普通药水贩子。而且，除了我们拿到传送祭坛的那个家伙，也没有人能亲自去问他。

不管怎么样……库贝克，如果你读到这份信的话，说明那些缩头缩脑的死矮子又搞砸了。把水晶球交回给他们，希望这里面能够记录下他们所需要的信息（好吧，如果要我说的话，[i]希望这东西把他们全炸死[/i]）。你那边的校准没有问题，并且你那些伪装地很差的暴徒干的也不错（别再放幻术了，这简直是一种侮辱。只要你们肯出钱，我们根本不关心你是谁或者是什么。）我们只需要把我们这边的信号锁调准，就可以完成你送过来的请求，甚至更多。

不过，说真的，我写这份信，是为了确保即使我在这个过程中死了，我也能够为你做一些事。如果我真的死了，希望你确保那个里奇养的小瘪三，是最后一次在抽签的时候玩他有趣的出千游戏了。对此，我会非常感激的。

```

## entry-03856
位置：tome-orcs.lua:2625；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
To think such an advanced civilization was hiding nearly right under our noses!  Not that the proximity made it any easier for me to conduct my research - it seems that unless you're a Sunwall citizen, a blood relative of King Tolak, or a merchant with enough gold to bribe the guards to look the other way, it's nearly impossible for a civilian to use the portal to the East.  Fortunately, Grand Councilor Kasyros himself was shown my writings to give him a basic overview of all the species his people were unfamiliar with, and he requested my presence to study his people.

Steam Giants are strikingly similar to what humans would look like, were they 8-10 feet tall and slightly on the stocky side (in contrast to the gangly, yet deceptively strong giants of Daikara).  Their most distinguishing physical trait is almost certainly their steam, for which they are named - their skin has numerous pores and vents which are capable of emitting pressurized steam.  They have limited conscious control over this; at rest they are nearly invisible and emit either a gentle mist or nothing at all, but they can will them to seal shut or distend widely, which, in addition to being rather disconcerting to watch, emits a stream or burst of pressurized steam.

Rather ingeniously, they have figured out how to use this steam to power and operate a wide array of metallic contraptions.  Although the giants' oldest texts have been lost to occasional fires and other disasters, they claim that the first bit of "steam-tech" was a simple whistle; from there, they discovered a sort of pressurized stone-cleaner, and from there more and more complex contraptions.  A similar effect can theoretically be achieved by using a furnace to boil water, but this method requires attention and adjustment that comes as naturally to the Steam Giants as breathing; perhaps it is this intuitive quality that made it so easy for them to accomplish so much with it.

The Steam Giants of the Atmos Tribe have hidden in the Clork mountains for ages; it is truly fortunate for them that the Spellblaze missed them entirely, for they were so concentrated and so few in number that it surely would have eradicated them.  They have kept their interactions with other races to a minimum; while Grand Councilor Kasyros claims this was due to fear of both what the outside world could do to them, and what their careless intervention could do to outsiders, most of the other Atmos I spoke to claimed to merely find the "lesser races" to be boorish and unpleasant.  (This is an entirely understandable view, seeing as their only neighbors until just recently have been Orcs.) 

While this isolation has given them peace to let their society develop, it has also fostered a strain of sophistry and disconnection to reality, according to Kasyros, who has begun open trade with the Sunwall and Allied Kingdoms to grant his citizens some fresh perspective.  I could not hope to fully analyze this society during my brief stay; the only deeper insight worth noting I was able to see is that they value physical fitness almost exactly as much as intellectual pursuits, perhaps owing to the fact that steam-tech can be made more powerful through more efficient construction OR simply being able to force out more steam from one's vents.  Their government, accordingly, is chosen by an apparent compromise between democracy and bloodsport (aside from a brief period under King Traglamar, which Kasyros would only tell me "was deeply embarassing for all involved").  Although I cannot say how it reflects on the Atmos people in a greater sense, I feel I must make special note that they have learned how to make the best absinthe I have ever tasted.

Alas, I was not able to study them for long enough to learn more than this.  Kasyros tells me he cannot accompany me any longer, for he has arranged a meeting with the Hero of Maj'Eyal - something about using an exploratory farportal for disposal purposes?  Whatever the case, although most of our contact with the Atmos is still done via constructs dropped from airships, we will soon gain the opportunity to meet more of them in person, and perhaps outsiders other than myself will soon be allowed to see their cities for themselves.  Their help in crushing the Kruk Rebellion and thwarting their leader's attempts to commandeer [b]IMMOLATUS, IMPUDENT RAVAGER OF THE HEAVENS[/b] has ensured that they will be enduring allies with us for an age to come.
```
译文：
```text
想想看吧，就在我们的眼皮底下，竟然藏着这样一个高度发达的文明！然而，我们之间这样的接近，并没有给我的研究提供什么方便——除非你是太阳堡垒的公民，托拉克国王本人的亲戚，或者是腰缠万贯的富商，能用足够的钱贿赂卫兵网开一面。否则，像我这样的平民，几乎没有任何使用远行传送门通往远东的机会。幸运的是，卡西罗斯议长本人曾经读过我的书，用以了解这个世界上他的族人所不熟悉的那些众多种族。现在，他邀请我亲自研究他的族人。

蒸汽巨人看起来与人类惊人地相似，他们身高8-10英尺，身材稍显矮胖，这与岱卡拉那些瘦高但出人意料地强壮的巨人形成了鲜明的对比。他们最具标志性的外貌特征是他们身上的蒸汽，这就是他们被命名为蒸汽巨人的原因——他们的皮肤上有许多毛孔和通风口，可以从中排出高压的蒸汽。他们可以对排气的行为进行有限的主动控制；在休息的时候，他们的排气行为通常是不可见的，只能依稀看到轻柔的薄雾，或者干脆什么也看不到。但是，他们也可以主动封闭或扩张排气口，放出一股气流或一团高压蒸汽，这样的场景看起来颇为令人不安。

他们相当巧妙地想到了使用这股蒸汽来驱动和操纵各种各样的金属装置的方法。尽管这些巨人们最早的文字记录被偶然的火灾和其他的灾害摧毁了，他们声称，最早的“蒸汽科技”只是一种简单的哨子。在此之后，他们发明了使用加压蒸汽清洁物体表面的方法，然后逐渐发明了一系列越来越复杂的装置。原理上，使用炉子来加热水也可以产生蒸汽，达到类似的效果，不过这种需要操作者仔细关注、控制蒸汽，而这一切对于蒸汽巨人来说都如同呼吸一样简单。或许，正是因为这种直观的感觉，让他们可以如此轻松地用蒸汽实现这样多的东西。

气之部族的蒸汽巨人在克拉克山脉中藏匿了几个世纪；幸运的是，他们从未受到魔法大爆炸的影响，考虑到他们的生存环境如此集中，人口又是这么稀少，这样的灾害恐怕会完全灭绝他们。他们尽力将与其他种族之间的互动降低到最低限度。按照卡西罗斯议长的说法，这是因为他们既害怕外部世界可能对它们造成的威胁，也害怕他们不谨慎的发明可能会给外面世界的人带来怎样的影响，但按照我从其他气之部族的人的说法，他们只是觉得那些“下等种族”又粗野又令人不快而已。（考虑到直到不久之前，他们唯一的邻居就是兽人，我完全可以理解他们的这种看法）

按照卡西罗斯的说法，尽管和外界的隔绝给了他们社会发展所需要的和平空间，这同时也助长了他们社会中倡导诡辩，脱离现实的思想。因此，他最近开始了和太阳堡垒与联合王国之间的开放贸易，希望能给他的族人带来一些看待问题的全新视角。由于我只有短暂停留在这里的机会，并没有时间能够深入分析他们的社会。因此，我唯一能够注意到的，他们社会中的深层因素，就是他们将身体健壮看的和对智慧的追求同样重要。也许这是因为，他们的蒸汽科技的力量，不仅可以来源于精巧高效的设计，[b]也[/b]可以来自于能够从排气孔中喷出更多蒸汽的，强大的肉体力量。因此，他们的政府，是通过某种由民主体制和血腥竞技结合而成的制度选拔出来的（除了国王特拉格拉玛统治的短暂时期，卡西罗斯只告诉我，“这件事对所有相关人员来说都是相当尴尬的”）。尽管我不知道这是否反映了气之部族人的某种重要品质，我觉得我还有必要特别提一句，他们还掌握着酿造我所尝过的最好的苦艾酒的技术。

唉，我没有机会研究他们足够长的时间，所以我的发现只有这些了。卡西罗斯告诉我，他不能再陪我了，因为他和马基·埃亚尔的英雄之间已经安排好了一场聚会——好像是有关使用探险远行传送门来进行垃圾清理？不管怎样，尽管我们大部分人和气之部族之间唯一的沟通的渠道，就是从飞艇上掉下来的装置，我们很快就会获得和更多他们面对面接触的机会。也许，未来还会有除了我之外的来访者，被许可亲自访问他们美丽的城市。他们在粉碎克鲁克叛乱，以及阻止他们的领袖强占[b]撼天动地，无耻的天空肆虐者[/b]中所作出的贡献，已经向我们证明，他们将会是我们未来一段时间中当之无愧的盟友。
```

## entry-03857
位置：tome-orcs.lua:2646；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Scholar Graynot's Assessment of the Species, Chapter 83: Wei...
```
译文：
```text
博学者格雷诺特关于人种的调查——第八十三章——Wei……
```

## entry-03858
位置：tome-orcs.lua:2647；section：tome-orcs/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)
```
译文：
```text
（当时空异常从另一条世界线拉入这条纸条的时候，这张纸条突然着火了。你还没来得及看完标题，这张纸条已经被烧得一干二净。）
```

## entry-03859
位置：tome-orcs.lua:2685；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A Reminder to Our Constituents:

Any votes for an individual candidate for office cease to be valid once the primaries are over, and the field has been narrowed down to two (or rarely three, in a close race) candidates.  At this point, you cannot vote for your candidate; instead, a competition will be held, after which its victor will be awarded with the position.  The vote you are submitting now determines how they will be competing.  While we cannot enforce how or why you vote, we request that you respect the spirit of our system, and select a competition which reflects the candidates' capability to handle the responsibilities of the Chief Councilor position.
```
译文：
```text
敬告广大选民：
初选结束后，任何向个人的投票将会不再有效，名额会被削减到两名（如果票数接近，有时会是三名）候选人。在那个时候，您将不能为您的候选人投票；相对应的，将会举行一个比赛，胜利者会获得职位。您现在的投票将会决定他们竞争的方式。我们不能强制要求您投票的方式或动机，但我们仍然请求您尊重我们体制的精神，选择一个能够反映出候选人作为议长履行职责的能力的合适的比赛项目。
```

## entry-03860
位置：tome-orcs.lua:2690；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A Plea from the Volunteer's Bureau of Gaming:

Once again, we find ourselves faced with an election for the competition of Chief Councilor.  While this is the most prestigious position in our government, it should not be forgotten that is also arguably the most complex, and the one bearing the greatest responsibility for the fate of our people.  A Chief Councilor's duties require not only cautious, reasoned foresight, but a quick wit to get emergencies under control in little time; yet, he or she must be aware of the precedent set or the unintended consequences of such decisive action, never acting rashly or out of ill temper.  Such a leader would wield our citizens and our military like a drunkard with a glass bottle, not caring if his weapon is shattered in the process. He or she must be able to develop creative solutions to problems but be open to outside advice, to be a character judge capable of selecting his or her most valuable acquaintances and a persuader to convince them to do the tasks for which they are most suited...  suffice to say, there are a great many mental skills required.  Accordingly, the competition should be one that tests all these skills.

This election, we are formally endorsing the board game [i]Automobiles and Automatons v9.8,[/i] a refined variant of the game introduced last year in a competition for the Marshall of the City Guard.  Its "oil-punk" science-fantasy setting, although perhaps easy to brush off as irrelevant to our reality, has its own consistent internal rules, forcing its players to learn a new status quo and work with it, as our leaders must be willing to learn from ongoing events and rapidly adapt to them; yet, since the game has been out for a year already and there are already numerous books about strategies for it, it also tests our candidates' long-term memory, as our leaders must be able to remember our history, to repeat our ancestors' successes but not their failures.  The rules of v9.8 are somewhat, but not entirely, different from those of previous versions, making these strategy books only partially accurate, just as our ancestors' wisdom only reflected the world they lived in, not the increasingly different one of the present.

v9.8 uses the "Crumbling Divide" map, providing a barrier that eliminates the possibility of an aggressive player gaining an early victory, tests the players' ability to plan in the long term, and yet due to the presence of non-player foes on either side, they still must be able to make plans in the short-term that will ensure their survival and leave them in an advantageous position when the barrier fades.  Non-player foes follow a predictable set of rules, eliminating luck as a factor, and our necropsychs have found a method of copying the same spiritual consciousness into two figurines, meaning that both players will be using identical sets of Negotiator figurines to demonstrate their diplomatic finesse.  (As always, the figurines are designed to release their spirits after no more than one month, ensuring that this process is as humane as possible to the deceased.)

The consumer edition of this game, v6.0, has won countless awards for its engaging and challenging play, with special attention given to the diverse array of viable strategies and skills tested by it.  Both sides agreed it was a fair game in the Marshall's election, as v1.0; v9.8 is unlikely to disappoint as a method of selecting our next leader.  Vote for [i]Automobiles and Automatons v9.8[/i] this year, and you will not be let down by its winner.
```
译文：
```text
游戏志愿者局的请愿：

又一次，我们面临着选举议长的比赛了。这是政府中最有名望的职位，但也别忘了它可以说是最复杂的职位，承担着我们人民命运的最大责任。一个议长不仅需要谨慎而理性的远见，也需要在短期内解决紧急事态的急智；并且，他或她必须明白这些决定的先例以及非预期后果，行动既不冒进也不出于心血来潮。否则，这样的领袖会像是一个醉鬼拿着玻璃瓶那样，轻率地对待我们的人民和军队，而不关心那武器是否会破碎。他或她必须能创造性地解决问题，同时包容外界的建议，还要做一个知人者，能选出他或她身边最具价值的人才，以及一个说客，能说服这些人去做他们最适合的工作……可以说，成为议长需要很多精神上的技能。因此，这个竞赛必须要考验所有这些技能。

这次选举，我们隆重推出桌面游戏[i]汽车与机器人第9.8版[/i]，一款去年曾用于选出城市卫兵团长的游戏的改良版。它基于“石油朋克”的科幻设定，或许会被认为与现实不符而被人忽略，但它有着它严谨的内部规则，会迫使其玩家学习新的环境并掌握它，就像我们的领袖们也必须愿意从正在进行的事件中学习并迅速适应它们；并且，由于这个游戏已经推出了一年，有无数关于游戏策略的书已经被出版，玩这个游戏也能测试候选人的长时记忆，因为我们的领袖必须得以史为鉴知兴衰。9.8版本的规则和之前的版本略有不同，但却并非完全不同。这样，那些策略书籍仅仅是部分准确的，就像我们祖先的智慧只能反映他们所处的时代，而不是面临巨变的今日。

9.8版本使用“破碎两极”地图，地图中有一个结界，这消除了那些具有侵略性的玩家获得快速胜利的可能性，测试了玩家们长期谋划的能力，而且因为两侧都有非玩家敌人，他们仍然要有短期计划，以保证生存，并在结界消散后占据优势。非玩家的敌人遵循可预测的规则，排除了运气因素，我们的通灵师也找出了一个把相同意识复制到两个模型中的办法，这意味着双方玩家都会使用相同的谈判者模型来体现他们的外交手腕。（和往常一样，这个模型被设计成在使用后一个月内解放里面的灵魂，以确保这一过程对于亡者来说尽量人道。）

这一游戏的消费者版本，6.0版，以它令人沉浸又富于挑战的游戏性已获得了无数奖项，尤其因它不同类型的多变策略，以及其对多种技能的综合考验备受瞩目。在1.0版本的游戏用于选出卫兵队长时，双方都同意游戏是公平的；作为选出我们下一个领袖的方式，9.8版本绝对不会令人失望。今年，投[i]汽车与机器人第9.8版[/i]一票吧，你不会为它的胜者而失望的。
```

## entry-03861
位置：tome-orcs.lua:2708；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Councilor Tantalos, unlike that cowardly wimp Chief Councilor Kasyros, knows just what to do to solve the steam shortages, and isn't afraid to do it!  Even though he can't reveal his plan yet for security reasons, the Geothermal Authority and our military's highest generals have assured us that his plan would work, without requiring us to ration steam usage or regulate our appliances; let's see Tantalos show that old geezer what-for, and end this drought for good!

VOTE FISTICUFFS
```
译文：
```text
坦塔洛斯议员，不像卡西罗斯议长那位懦弱的窝囊废。他知道该如何解决蒸汽短缺的问题，也不怕去执行这一方案！即使由于安全原因，他现在还不能公布计划，地热局和我们军队高级将领已经向我们保证，他的计划一定会奏效，我们再也无需节省蒸汽用量或是管控我们的器具；让我们看看坦塔洛斯怎样让那个老东西难堪，并永远结束蒸汽枯竭！

[b]请投肉搏战[/b]
```

## entry-03862
位置：tome-orcs.lua:2714；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
My fellow councilors,

In this time of increasing vent-drought, it is tempting for us to seek the easy way out.  I understand that at this point, I am powerless to prevent our new Chief Councillor's plans to take the promising vents under the Kruk orcs, but should we fail, you may be tempted to compensate by approaching that...  entity who called itself "the Loyalist."  I am of the opinion that this would be a foolish decision.

Do you remember the Official Histories' record of when we first interacted with the lesser races?  They spoke of them as an entertaining, jovial bunch, friends and companions with our own people.  How naive we were back then...  but when our ancestors saw their true nature, the brutality they were capable of, they recorded these acts in detail.  They did not, however, explicitly tell us not to trust the Orcs.  They did not explicitly tell us that they are pests to be avoided, or a scourge to be eradicated, or a pitiful, fallen reminder of why letting the lesser races use our discoveries will only end in tragedy.  They simply recorded what they learned, and allowed future generations to come to those conclusions themselves, compared with their own observations - and in our grandparents' case, by unfortunate personal experience.  Even through the distress and feelings of betrayal at the time, even though opinions ran in every direction from fury to sorrow at the lesser races' barbarism, not one of the Councilors responsible for recording events gave in to editorialism.  Perhaps we would be in a better situation if they had, so we would have not repeated their mistake of trust, but they stayed fair nonetheless.

Going even further back, they spoke of relations with our now-distant kin, the Sturmos Tribe.  Though the records describe a strained relationship, the mentions of their boorish behavior are recorded in a matter-of-fact nature, and interspersed with the mentions of their advanced metallurgy techniques and other such valuable things we gained from cooperating with them.  Although their current state of Great Firestorm-induced exile to the mountains of Maj'Eyal makes it a rather moot point, the fact still stands that if we were somehow in a position to trade with them, we could rely on the Official Histories for a trustworthy indication of, at a minimum, how they [i]used[/i] to behave.

The examples go on; the Official Histories have remained dispassionate and fair, and a reliable metric for making decisions.  Not once did our forefathers allow their biases to influence their recordings.  Not once did a fervent political movement manage to compromise their integrity.  Not one chapter of these texts can be safely and fully discredited as the subjective, unfair writings of a dominant political party, or the deluded ramblings of a movement influenced by some banal philosophical fad.

(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)

My point is, the Official Histories have a very well-proven track record.  Every single time but once, they have given a solid analysis of the evidence.  Every single time but once, they have refrained from outright suggesting a course of action.  And only once have they allowed something as subjective as a gut feeling into their reports.

Do you know what they say about the meeting with the Loyalist?  After a brief description of the events of the meeting - a strange creature approaching the Council of the time, demonstrating its power by using a small wand to blast a hole halfway to Eyal's core (a wand which he then handed them as though it were a child's cheaply-made toy), stating it could offer us a source of near-infinite energy in return for a rather inconvenient magical artifact.  When they turned it down, the creature gave a speech recorded in verbatim detail: "It hardly matters.  I have all the time in the world to wait for your people to trip over their own hubris and shatter.  If you will not allow me to save you, then I need only sift through the shards of your ruined cities to find it."

Our forefathers say this creature gave them a means of contacting it again, but outright refuse to say what it was; the only reason we still know how to reach it is the yearly messages dropped on the Palace's front steps.  After mentioning that, they wrote this:

"Do not trust this Loyalist.  When we look upon him, we feel something deep within us, older than ourselves, telling us that he is simply... [i]wrong[/i].  His intentions with the Eye, an artifact with incredible power that we have yet to successfully harness, cannot be good for anyone, least of all ourselves.  Never give him the Eye, and continue our work of trying to find a means of destroying it.  Never accept any other deal he offers.  If you are ever unfortunate enough to see him as well, you will immediately understand why we say this."

Perhaps political discourse has gotten a bit...  muddier in recent years.  With the bickering and sniping of modern-day debates, it can be hard to believe that past Councilors had ideas other than their careers in mind, that a vehement display of emotion would be something other than political posturing.  But even if those Councilors were just as petty and selfish as we are, they did not let it affect the Official Histories, not once.

I intend to trust the only advice our ancestors gave us in the Official Histories.  I beg of you all to do so as well.
```
译文：
```text
议员同志们，在这一出气口枯竭加剧的时期，一个简易的解决方法是极具诱惑性的。我明白，目前我已经无力阻止我们的新议长去夺取克鲁克兽人地盘底下的那些有前景的出气口，但是一旦我们失败了，你们也许会试图去接近那个……自称“忠诚者”的个体来补救这一切。我个人认为这会是个愚蠢的决定。

你们还记得，在正史中我们第一次与那些下等种族接触时的记载吗？上面写着，它们是一群有趣又快活的人，是我们的朋友和同伴。我们那时可真是天真啊……但是当我们的祖先们看到了他们的真实本性和他们潜在的残暴之后，祖先们把这些详尽记录下来。然而他们没有明确地告诉我们不要信任兽人。他们没有直接告诉我们这个种族是要远离的害虫，或是一个要消灭的祸害，也没有留下一个可悲的警示，告诉我们让那些下等种族使用我们的发明创造只会导致悲剧。祖先们只是把他们学到的记录下来，让后人对照自己的观察结果，得出自己的结论————这是我们的祖父母辈以不幸的个人经验而体会到的。即使他们悲伤着，感觉到被背叛，即使思绪万千，对下等种族的野蛮感到震怒又哀怜，当时那些负责记录事件的议员们，没有一个抒发个人观点。或许，假如他们愿意表达这种观点，我们可能会处于一个更好的处境，不会再重复他们轻信的错误，不过无论如何，他们仍然保持了公正的记述。

再往前追溯，祖先们谈论过与我们今日的远亲风暴部族。尽管这些纪录中描述了我们与他们紧张的关系，对他们本性中的粗野举动的记述确实完全实事求是的。而且，记录中还提到了关于他们先进冶金技术的论述，以及其他和他们合作获得的好处。尽管一场巨大的火风暴后，他们至今流亡于马基埃亚尔的群山中，让与他们打交道的想法不太可能实现，但如果我们一旦有机会与他们交易，正史还是提供了一个可靠的指示，至少，也能告诉我们他们[i]曾经[/i]如何。

这样的例子还有许多；正史一直以来都是冷静而不偏不倚的，是做决定的一个可靠标尺。前人们从来不让个人的偏见影响他们的纪录。这一纪录的诚实也从来未在狂热的政治运动中妥协。在这些文字中，没有一个章节可以被论定为某个优势政党的主观臆断，或是受某个陈腐的哲学思潮影响的胡言乱语。

（显然，特拉格拉玛王短暂的仁政除外，但是要明白这是特例，不值得进一步讨论。）

我认为正史对以往的事情有非常可靠的纪录。除了一次以外，他们都对证据进行了可靠的分析；除了一次以外，他们都克制住自己，没有直接给出行动方案。只有这一次，他们在报告中透露出了本能感受这样主观的东西。

你们知道他们怎样描述与“忠诚者”的会面吗？简短地讨论了几件事后，那个奇怪的生物接近了当时的议会，用一根小小的魔杖，炸出一个半途通往埃亚尔核心的洞，来展示他的力量（它接下来把这个魔杖随意地交给了议会成员，就像把它当是儿童的劣质玩具），声称它可以为我们提供一个近乎无穷的能源，而他只需要一个令人感到不便的魔法古物为交换。在他们拒绝后，那个生物发表了看法，原文如下：“这不怎么要紧。我有世界上所有的时间等待你们的人民因为自己的骄傲摔得粉身碎骨。如果你不让我来拯救你们的话，我只需要从你们文明的废墟中找到它。”

我们的祖先写下，这个生物给了他们再次与它联络的方式，但祖先们拒绝了写下这一联络方式是什么；我们仍然知道怎样与它联系的原因，在于在一条在烟雾宫殿前门留下的年度总结信息。在提到这以后，他们写道：

“别相信这个‘忠诚者’。当我们抬头看他时，我们感觉到在自己内心深处，有一种比自己要古老的存在，告诉我们他是……[i]错误的[/i]。他对于‘眼’，一个有我们至今没有成功掌控的强大力量的古物，抱着意图，这不可能对任何人有好处。永远别给他‘眼’，而且要继续找到一种销毁‘眼’的方法。永远别接受他给出的其他交易。如果你们有一天也不幸地要见他，你们会立即明白为什么我们这么说。”

或许这几年，政治争端变得有些……令人头脑混乱了。今日的辩论中到处都是口角和中伤，让人很难相信，过去的议员们脑海里会考虑超越他们职业生涯以外的东西，那种激昂的感情表达也不仅仅是政治上的装腔作势。不过即使那些议员们像我们一样器量狭小而自私，他们也未曾影响过正史的记录，一次也没有。

我想要信任祖先们在正史中给出的唯一建议。我也请求你们都这样。
```

## entry-03863
位置：tome-orcs.lua:2758；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The Steam Council has been called to order, with Chief Councilor Tantalos presiding.  

TANTALOS: "Greetings, my fellow- heh, now [i]lesser[/i] Councilors!  It is my pleasure to finally lead the proceedings.  The agenda for today..." Ruffles through papers. "Is irrelevant, for I have a solution to every malady mentioned therein.  The first order--"

KASYROS: "With all due respect, Chief Councilor, the agenda--"

TANTALOS: "Is.  [i]Irrelevant.[/i]  Tormak?  You've been scrying on potential sources of geothermal energy, would you care to inform the others where you see the most potential?"

TORMAK: Sighs. "Right under the Kruk orcs, unfortunately.  It's a promising source for sure, the magma powering it hasn't drained out like it has under us, but digging there would...  well, we all know how quickly they turned construction tools into weapons to rival our own.  If we went in there with the state-of-the-art mining equipment necessary to--"

TANTALOS: Laughter. "Mining equipment!  What manner of fool do you take me for?  Palaquie, tell me what's going through the minds of those silly little waist-height warriors, rummaging through the mainland for Orcish rebels." Holds up hand to silence Councilor Emeritus Kasyros. "This IS relevant, I assure you."

PALAQUIE: "Discontent...  revolving around hidden, long-fermented resentment. Some want the Kruk exterminated, others imprisoned.  Neither can afford direct intervention, but some form of support will assuredly be available."

TANTALOS: "So, with the right negotiation, we can get these tinies, who have [i]endless[/i] experience fighting Orcs, to assist us and make any sort of action in Kruk territory more manageable.  At a bare minimum, we can obtain weaponry that has long proved sufficient for slashing Orcish throats...  although we'll need it custom-fit for our size, naturally."

PALAQUIE: "They have a race whose armor would work.  A tight fit, but sufficient."

TANTALOS: "Even better!  And...  Kasyros, I'm going to let [i]you[/i] tell me what the people care about most.  I'm sure your bruises are adequate reminders of the citizens' will?"

KASYROS: [Statement was deemed excessively profane and stricken from the record by 4-2 vote.]

TANTALOS: "Such undignified conduct!  All because you can't accept that the public wants their steam back.  More than they want those filthy little greenskins around, more than they fear getting their hands dirty, more than they want [i]your[/i] way of doing things.  So!  It's resolved that we have much to gain from this, it's resolved that we have or can obtain the means to carry it out, and it's resolved that it is what the voting public desires.  I see no need for further debate.  Nashal, I'd like to speak to you after this about a wand.  Meeting adjourned."

[At this time, Councilor Kasyros gave a lengthy speech before officially resigning from the Council.  It has been recorded in a separate document.] 
```
译文：
```text
在坦塔洛斯议长的主持下，蒸汽议会正式开会。

坦塔洛斯：“你们好啊，我的同……哈，现在是[i]下级[/i]议员们！这是我的荣幸，能够终于主事。今日的议程……”翻动手中的文件。“无关紧要，因为我已经为所有要解决的问题有了一个对应的方案。首先————”

卡西罗斯：“尊敬的议长，议程————”

坦塔洛斯：“这件事[i]无关紧要[/i]。托马克？你一直在占卜潜在的地热能源，你能告诉大家哪里最有潜力吗？”

托马克：叹气。“不幸的是，就在克鲁克兽人的地盘底下。那确实是个有潜力的源头，提供能源的岩浆可不像我们地盘底下的都枯竭了，但是在那里挖掘会……好吧，我们都知道他们能多快的把建筑工具变成能威胁我们的武器。如果我们把能用来开采的最新式采矿工具带过去————”

坦塔洛斯：大笑。“采矿工具！你把我当成是怎样的傻瓜？帕拉奎，告诉我那些在大陆上到处搜寻兽人反叛者的齐腰高的小傻战士们在想什么。”举起手打断荣誉终身议员卡西罗斯。“我向你保证，这确实相关。”

帕拉奎：“不满……以及隐藏的，长期发酵的怒火。有些人想消灭克鲁克兽人，也有人想监禁他们。不论是那种，我们都没法直接介入，不过确实可以提供某种支持。”

坦塔洛斯：“那么，在恰当的协商后，我们可以让那些有[i]无数[/i]兽人作战经验的小东西，来协助我们，让在克鲁克兽人境内的一切行动更易掌控。最少，我们可以取得那些已被长期证明能割断兽人喉咙的武器装备……自然，我们确实得想法子改成我们的尺寸。”

帕拉奎：“他们有个种族，护甲可以给我们用。穿起来有点紧，但是足够了。”

坦塔洛斯：“那就更好了！还有……卡西罗斯，我想让[i]你[/i]告诉我人民最在意什么。我敢肯定，你身上的伤痕一定能提醒你，公民们的意志是什么，对吧？”

卡西罗斯：[这一表述被视作过分的亵渎，以4比2的投票，通过从记录中削除。]

坦塔洛斯：“真是不成体统的发言啊！只是你们不能接受群众想要回他们的蒸汽。比起想要那些狡猾的小绿人们在身边，比起他们害怕把自己的手弄脏，比起想要以[i]你们[/i]的方法做事，更想要蒸汽。所以！这决定了我们从这方案里获益良多，决定了我们有或能找到解决困难的方式，也决定了这是选民们想要的。我看不需要进一步讨论了。纳沙尔，之后我想跟你讨论一个魔杖的事情。散会。”

[同时，卡西罗斯议员也在从议会正式辞职时做了一个不短的演讲。演讲被另一个文件记载。] 
```

## entry-03864
位置：tome-orcs.lua:2808；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(Ink has been spilled on this transcript - you can only read certain passages.)

???: "[...]ame me for this!  YOUR mechanics examined that airship, YOUR equipment was used to repair it, and it's YOUR fault it went down!"

NASHAL: "Yes, and I told you to call the attack off the moment I heard the news - the Loyalist's wand as a fire-support tool was far too valuable to conduct the invasion without it.  But no, Palaquie had to insist on going right then--"

PALAQUIE: "My visions do not lie.  It was the best way forward.  Our odds of success at that point, low as they were, were still better than if we had let Pendor's inflexible, time-dependent plan sit and--"

PENDOR: "DON'T YOU EVEN START, YOU YETI-LOVI--[...]"

[...]

Motion made to record the statement that Councilor Pendor would not know decent equipment if it shot or stabbed him in the face passed, 3-1, with Councilor Tantalos abstaining.

Motion made to record the statement that Councilor Tormak's robes smell of absinthe and vagrants passed, 3-1, with Councilor Tantalos abstaining.

Motion made to begin an official inquiry passed 3-1, with Councilor Tantalos abstaining.  The first order of business at the next session will be determining whether or not Councilor Nashal's state-of-the-art mining and extracting equipment is capable of extracting her head from her--

[...]

TANTALOS: "If you are all quite finished with this rubbish...  How bad is the situation, exactly?  I want details and facts, not blame."

TORMAK: "You don't want blame because this whole thing was YOUR idea!  It's YOUR fault we--"

Motion to censure Councilor Tantalos for defenestrating Councilor Tormak has failed, 1-1 (tie broken by Chief Councilor status), with Palaquie, Nashal, and Pendor abstaining.

[...]

TANTALOS: "So, a few wastrels in the marketplace are gone, and the Kruk have moved on to the mainland.  As far as I am concerned, they are not presently our responsibility - these 'Allied Kingdoms' and 'Sunwall' folk can deal with them.  Thanks to Pendor's scouts, we have a weapon we can point at the Kruk Pride homeland as a deterrent, which should buy us even more time.  We should use this time to bolster our defenses...  and consider additional options.  Meeting adjourned."

PALAQUIE: "Additional options?"

TANTALOS: "The meeting has been adjourned.  You should be training our necropsychs, Councilor."
```
译文：
```text
（墨水被洒在这个记录上————你只能读到一些段落。）

？？？：“[……]怪我！那架飞船是你的机械师检查的，是在用你的设备修理它，也是因为你的错它才坠落！”

纳沙尔：“是吗，我在听到那个消息时也告诉你了要取消攻击————忠诚者的魔杖作为火力支援工具太珍贵了，我们进攻的时候绝对离不了它。但不，帕拉奎非要坚持当即出发————”

帕拉奎：“我眼前的景象不会作假。那是前进最好的方法。我们那时的成功几率虽然低，还是强于假如让潘多尔做主，用那个不灵活，依靠时机的方案————”

潘多尔：“你再说一句看看，你这个恋雪人————[……]”

[……]

记录下“潘多尔议员不知道什么是优良的设备，除非亲自射到或者刺到他脸上”的表述的动议以3比1的投票通过，议员坦塔洛斯弃权。

记录下“托马克议员的长袍闻起来有苦艾酒和流浪汉的味道”的表述的动议以3比1的投票通过，议员坦塔洛斯弃权。

进行官方调查的动议以3比1的投票通过，议员坦塔洛斯弃权。接下来进行调查的第一部分，将会决定是否纳沙尔议员的最新式采矿和提取工具能够将她的头从她的————

[……]

坦塔洛斯：“如果你们都闹够了……到底情况有多糟糕？我想要细节和事实，而不是抱怨。”

托马克：“你不想要抱怨是因为整件事都是你的主意！这是你的错所以我们————”

谴责坦塔洛斯议员把托马克议员扔出窗外的动议未被通过（1比1，平局被议长否决），议员帕拉奎、纳沙尔和潘多尔弃权。

[……]

坦塔洛斯：“所以，商场里的那些饭桶死了，克鲁克兽人已经开始在大陆行动。据我所知，这目前不是我们应当担心的————那些“联合王国”和“太阳堡垒”的家伙们可以对付。多亏了潘多尔的斥候，我们有了一个武器，可以作为一个威慑力量对准克鲁克部落的老家，这会给我们争取更多的时间。我们应该用这段时间加强守备……并考虑其他方案。散会。”

帕拉奎：“其他方案？”

坦塔洛斯：“已经休会了。你现在应该去训练我们的通灵师，议员。”
```

## entry-03865
位置：tome-orcs.lua:2874；section：tome-orcs/data/lore/palace-fumes.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
TANTALOS: "Tell the others of the unfortunate developments, Palaquie."

PALAQUIE: "The Kruk Orcs, under %s, appear to have pushed to the last bastion of the Sunwall forces...  none of my visions predict this ending favorably for anyone of non-Orcish descent.  With the Sunwall gone, there will be no further distractions for the Kruk.  In short, the Sunwall are doomed - and we are next."

TANTALOS: "Where there's a will, Palaquie, there's a way.  What of the Migratory Leviathan?  Nashal, do you have any idea where--"

NASHAL: "About that...  Kasyros stole it when everything started going to slag.  We'd take it back, but he's using it to evacuate civilians.  We'd end up using too many bullets on our own people that belong in the Kruk Orcs."

TANTALOS: "Unfortunate, but we'll surely be able to convict him of treason once this all blows over.  Pendor, you've been working with our marksmen - how are they doing?"

PENDOR: "Scared scrapless, Your Honor, but they're learning quick.  I managed to snatch up some newer Flameshot rifles from Kaltor's surplus, and our Retaliators are as strong as ever."

TANTALOS: "Splendid to hear.  And what of that backup weapon you had mentioned - what was that name again, #{bold}#DESTRUCTICUS, IMPOLITE PENETRATOR OF-#{normal}#"

TORMAK: "It's gone.  The mages I sent with Pendor's runners...  their invisibility spells were inadequate.  The Orcs found them...  if it's any consolation, they don't appear to have realized what the keys are for, or what it's capable of.  I'm...  I'm sorry."

Lengthy pause.

TANTALOS: "...I think it's time."  Removes a briefcase from behind the podium, and opens it to show the other Councilors its contents, before closing it and holding it again.  Councilors Palaquie, Tormak, and Nashal audibly gasp.  Motion to strike all description of its contents from the record passed, 3-2.

TORMAK: "You can't be serious!  How is that going to make the situation BETTER?"

PALAQUIE: "It cannot."

NASHAL: "I can't agree with this, Councilor Tantalos, your predecessor had a point--"

TANTALOS: Pounds fist, breaking podium.  "That doddering old coward knew NOTHING!"  Pause; sighs.  "None of us do.  All we know is, this eye's almost certainly useful for more than making declogging draught from its tears, and the person who wants it is the type of person who casually digs holes to the center of Eyal.  We've tried everything; the time for a last resort has come, and we are in dire need of a miracle.  This... 'Loyalist' is the only possible source of miracles around, and if infinite energy and blasting holes through the planet are within his capabilities, then disposing of these barbarians should be quite simple."

PALAQUIE: "If our ancestors are to believed, this could result in a fate worse than our own destruction--"

TANTALOS: "Would everyone who doesn't have any #{italic}#better#{normal}# ideas cease their jabbering before I cease it #{italic}#for them?#{normal}#"

[Silence.]

TANTALOS: "As I thought.  Nashal, prepare the G.E.M. and a retinue of guards and mechanics.  There is business I must attend to.  Meeting adjourned."
```
译文：
```text
坦塔洛斯：“告诉大家现在的不利形势，帕拉奎。”

帕拉奎：“克鲁克兽人，在%s的带领下，看上去已经攻到太阳堡垒军的最后一个堡垒了……我的各个预测景象都不会倾向于任何非兽人血统的一方获取胜利。太阳堡垒陷落后，对于克鲁克兽人就没有什么阻碍了。简而言之，太阳堡垒气数已尽————而我们是下一个。”

坦塔洛斯：“帕拉奎，有志者事竟成。“迁徙的利维坦”怎么样了？纳沙尔，你知不知道它在————”

纳沙尔：“那个啊……在事态变得糟糕的时候，卡西罗斯偷走了它。我们想要把它夺回来，但是他正在用它撤离平民。如果那样的话，我们会把大量本应用在克鲁克兽人身上的子弹，射向我们自己的人民的。”

坦塔洛斯：“真不走运，不过一切结束后我们一定能定他叛国罪。潘多尔，你最近在训练我们的枪手吧————他们怎样了？”

潘多尔：“那群废物们吓得不轻，尊敬的议长，但是他们进步得很快。我从卡尔托剩下的货物中收集了一些新式的喷火步枪，而我们的复仇者部队处在巅峰状态。”

坦塔洛斯：“听起来真不错。那个你提到过的备用武器————叫什么来着，#{bold}#毁天灭地、无礼的贯穿者————#{normal}#”

托马克：“它不见了。那些我派给潘多尔的传令兵的法师……他们的隐形咒语不准。兽人们找到了他们……若这算是一点安慰，他们似乎还没意识到钥匙是做什么用的，也不知道那些武器能做什么。我……我很抱歉。”

漫长的沉默。

坦塔洛斯：“……我认为是时候了。”从讲台后拿出一个手提箱，打开给其他议员看里面的东西，又合上它把它收起来。帕拉奎、托马克和纳沙尔议员都发出喘气声。清除有关箱子里东西的记录的动议以3比2通过。

托马克：“你别开玩笑吧！这东西怎么能改善现在的情况？”

帕拉奎：“它不能。”

纳沙尔：“我不能同意这样做，坦塔洛斯议员，您的前任的观点确实有道理————”

坦塔洛斯：挥拳砸桌子，把讲台砸烂了。“那个走不稳路的老懦夫什么也不知道！”停顿；叹气。“我们也都不知道。我们知道的是，这个眼的作用肯定不仅仅是用它的泪水来做清淤药水，而想要它的人，是那种可以随心所欲挖出通向埃亚尔地心的洞的人。我们已经试过了所有方案；最后挣扎的时刻来临了，我们相当渴望一个奇迹。这个……“忠诚者”是我们身边唯一可能的奇迹来源，如果无限能源和在星球中间穿洞在他的能力限度之内，那么把那群野蛮人赶走应该非常简单。”

帕拉奎：“如果我们的祖先可信的话，这可能比我们自身的毁灭更糟糕————”

坦塔洛斯：“你们这些想不出#{italic}#更好#{normal}#主意的人能不能闭上叽叽喳喳的嘴，在我来#{italic}#帮你们#{normal}#闭上之前？”

[沉默。]

坦塔洛斯：“这就对了。纳沙尔，准备好GEM，随从的守卫和机械师。我还有要做的事情。散会。”
```

## entry-03866
位置：tome-orcs.lua:2959；section：tome-orcs/data/lore/pocket-time.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<? Lore.init_pocket_time_data() ?>Once upon a time, there was a Halfling alchemist by the name of <?=Lore.pocket_time_winner.name?>.  Alongside her trusty golem, she marched into the Trollmire, disposing of all foes in her path; when she encountered Prox, though, and he bent down to roar mere inches from her face, well inside a bomb's blast radius, she panicked and pulled a vial off her belt--

Once upon a time, there was a Dwarven berserker by the name of <?=Lore.pocket_time_winner.name?>.  Fleeing through the halls of Reknor as his friend was cut down by Orcish warriors, he ran face-first into a couple of them and--

Once upon a time, there was a Cornac rogue by the name of <?=Lore.pocket_time_winner.name?>.  His traps made short work of Prox, but when Bill the Stone Troll tossed him around his lair, he lost his bearings and stepped on--

Once upon a time--

Once upon a time, there was a great hero, a Dwarven Stone-Warden by the name of <?=Lore.pocket_time_winner.name?>, who began her adventure swearing incomprehensibly about unfairness before shrugging and continuing onward.  She escaped from Reknor with her closest companion, used her natural powers to purge the Deep Bellow and The Maze of the corrupting forces therein, rescued a strange new creature called a "yeek" from the clutches of the murderous Subject Z, and even shrugged off boulders thrown at her by the giants of Daikara as she inexorably pushed forward, slaying so many threats that had harmed so many people before her.  She uncovered the long-lost Conclave Vault and put the last of the original Ogres to rest, rescued a damsel from the clutches of the Sect of Kryl-Feijan, and finally found herself standing at the gates of the tower of Dreadfell, her skills honed by her trials and laden with exotic equipment found in her travels.  Climbing through the waves of shambling undead, she finally faced The Master head-on, when a skeletal warrior struck her from behind.  A stunning blow from its warhammer struck her right where she'd applied a wild infusion, the only one she had.  Dazed and stumbling, trying to invoke its power, she only became lucid when a terrible cold crept up her limbs, encasing her in ice--

Once upon a time, there was a Thalore summoner by the name of <?=Lore.pocket_time_winner.name?>, who began her adventure right next to a snake that was unnaturally skilled with temporal magic--

Once upon a time, there was a terrible villain, an Ogre reaver by the name of <?=Lore.pocket_time_winner.name?>, who found himself fascinated by the corrupted crystalline structures of the Spellblaze Caverns.  He first drowned a Last Hope guard in the dead of night to steal her enchanted ring, then began to leave a trail of destruction throughout the land, feeding on the strength of those hewn with his battleaxe or impaled with his longsword, and growing ever more powerful with every death he caused.  He joined the cause of the Grand Corruptor in an assault on Zigur to ensure that nothing could stop his arcane plagues from spreading, then took the Heart of the Sandworm Queen to Spellblaze-tainted lands to pervert its natural blessing into a blighted font of suffering.  He sat and watched as a cult sacrificed a maiden to summon their demonic master just so he could kill it himself, and salivated at the prospect of traveling to the Far East and seeing four armies' worth of Orcs broken and bleeding, tumors and boils spreading across their skin as the life slowly left their eyes.  The finest soldiers of Vor Pride could do nothing to prevent him from raiding their armory, but one crippled and diseased Orc pulled himself up against its sealed doors and begged him not to open them; he simply laughed before crushing his skull under his boot as he walked toward it, then kicked the door down, only to feel his bone armor disintegrate under a storm of breath attacks from an army of unspeakably powerful multi-hued wyrms.  Even <?=Lore.pocket_time_winner.name?> knew when he had to flee from a fight, and clenched his fist as he charged his Phase Door rune; when the blinding flash of light cleared, he found himself mere inches from--

Once upon a time, there was a Doomelf by the name of <?=Lore.pocket_time_winner.name?>, freed from demonic mind-control by a lucky meteor strike, who set out to use her new-found powers to escape the orbital hell on which she was trapped.  Investigators and mutilators, designed for torturing captives but far too frail for direct combat, fell under her infernal blade nearly as easily as the unaltered Children of Ruby who had few skills outside clerical work, and soon she began to feel that the demonic magic she had been imbued with may have made her nearly unstoppable.  When a demonic statue called out to her, she thought nothing of trying to absorb more of its power, barely even noticing when the statue called forth a Champion of Urh'Rok--

Once upon a time, there was a Shalore Adventurer by the name of <?=Lore.pocket_time_winner.name?>, who was quite certain of what he was doing.  He'd learned an extremely uncommon set of abilities - great talent with unarmed martial arts, some psychic potential to swing a staff in the air while leaving his hands free, stone magic that used his punches as a focus to blast foes with a hailstorm of earthen missiles - and once he had enough practice to master a few of these, he started effortlessly destroying any foe he faced... until he encountered the Weirdling Beast.  The battle was intense, and soon, both were on the verge of death, on opposite sides of the fortress's foyer; the Adventurer knew he couldn't afford to rush in close to finish the beast off, so he launched a pair of earthen missiles at it instead.  However, the moment they left his hands, he felt the grip of hard bone around his waist, legs, and back, pulling him at an incomprehensible speed into the Weirdling Beast's grasp.  Perhaps <?=Lore.pocket_time_winner.name?> could have survived an ensuing fistfight, but he had been pulled faster than his own missiles could fly, and now he found himself between the stony projectiles and their original target--

Once upon a time, a great spirit put down its pen and closed its notebook, sighing in frustration.
```
译文：
```text
<? Lore.init_pocket_time_data() ?>从前，有个半身人炼金术师叫做<?=Lore.pocket_time_winner.name?>。和她可靠的傀儡一起，她向巨魔沼泽前进，把挡住她的敌人消灭殆尽；不过当她遇到了普洛克斯时，他弯下腰来在离她脸几英寸的地方大吼，正好在炸弹的爆炸范围之内，她慌张起来把一个炼金瓶从腰带上拽开————

从前，有个矮人狂战士名叫<?=Lore.pocket_time_winner.name?>。在瑞库纳的大厅逃离时，在他的朋友被兽人战士砍倒后，他直接向几个兽人正面冲去，然后————

从前，有个科纳克人盗贼名叫<?=Lore.pocket_time_winner.name?>。他的陷阱很快解决了普洛克斯，但当岩石巨魔比尔在他的巢穴里把他扔了出去，他失去平衡踩在了————

从前————

从前，有个大英雄，一个矮人岩石守卫名叫<?=Lore.pocket_time_winner.name?>，在开始她的旅程时发表了一番关于不公平的费解的话，然后耸肩继续前进。她与最亲近的同伴一道从瑞库纳逃离，使用了她的自然能力清除了深渊咆哮与迷宫里的堕落之力，从嗜杀的实验体Z的魔掌中拯救了一个奇怪的叫做“夺心魔”的新生物，甚至在势不可挡地推进时，甩开了岱卡拉的巨人向她扔去的巨石，消灭了伤害了以往许多人的威胁。她发现了失落的孔克雷夫地下实验室，让最后几个最初被造出来的食人魔安息，从克里尔·费扬邪教徒的魔掌中救出了一个姑娘，最终站在了恐惧王座的塔门前，技艺百经锤炼，满载旅程中找到的各种珍奇装备。她一边往上爬，一边与一波波蹒跚的不死生物而战，她终于见到了吸血鬼领主迎面而来。这是，一个骷髅战士从后袭来。当她想用她仅有的那一个狂暴纹身时，它的战锤挥击震慑了她。当她因震慑而失去平衡，想要激活纹身的力量，一阵可怕的寒流涌遍了她的四肢，把她包裹在冰块之中时，她才清醒过来————

从前，有个自然精灵召唤师叫做<?=Lore.pocket_time_winner.name?>, 在一条蛇旁开始了旅程，这条蛇不自然地精通时间魔法————

从前，有个可怕的恶棍，一个食人魔收割者叫做<?=Lore.pocket_time_winner.name?>，他发现自己为魔法大爆炸影响的山洞中被污染的晶体结构着迷。他首先在夜深人静之时淹死了一个最后的希望的守卫，偷走了她的附魔戒指，然后在大陆上一路留下他毁灭的轨迹，吸取着被他双手斧砍死或被他的长剑穿透的对手的力量，在造成一场场死亡的同时变得更强大。他参与了大腐化者的事业来袭击伊格，来确保没人能阻止他的奥术瘟疫散播，之后把沙虫女王的心脏带到魔法大爆炸污染的土地上，来把它的自然祝福腐化成一种枯萎的苦难力量。他对一个邪教献祭少女来召唤他们的恶魔主人袖手旁观，这样他能亲自杀死它。他旅行到远东，看到四支兽人大军溃散而流血，肿块和疮遍布他们的皮肤，同时生命缓慢地从眼中流失而垂涎不已。沃尔部落最好的战士对于他劫掠兵器库而无可奈何，但一个瘸腿而病弱的兽人堵在封印的门前求他别打开；他只是大笑，走向门，踩过兽人的头，在靴子下碾碎，之后把门踢倒，突然感觉到他的骨盾在一群无可言喻地强大的七彩龙的吐息风暴中解体。即使是<?=Lore.pocket_time_winner.name?>也知道什么时候该从战斗中逃跑，在激活相位门符文的同时握紧了拳头；当刺眼的闪光消失时，他发现自己几英寸外就是————

从前，有个魔化精灵叫<?=Lore.pocket_time_winner.name?>，由于一个好运天降的落星从恶魔的心灵控制中解脱，出发去用她新得到的力量来从她被困住的轨道地狱中逃脱。那些调查员和切割者是被设计来折磨囚徒，他们对于近身战斗来说过于脆弱，在她的烈火之刃面前，几乎就像是那些未被转变的，除了文书工作外没什么技能的红宝石之子那样轻松倒下，很快，她开始感觉她体内被灌注的恶魔魔法说不定已让她接近无敌。当她看到一个恶魔雕像时，她除了想吸收更多力量外没想别的，根本没注意到雕像召唤了一个乌鲁洛克的精英卫兵————


从前，有个永恒精灵冒险者叫<?=Lore.pocket_time_winner.name?>，他对于自己在做什么非常确信。他学会了一套相当不寻常的能力————了不起的空手武术天赋，一种在空中挥动法杖的心灵潜能，用拳击触发的石系魔法来用暴风般的石弹来击退敌人们————一旦他在这些方面都有了一些实战经验，他开始秒杀所有遇到的敌人……直到他遇到了异形触手。战斗非常激烈，不一会儿，双方都在死亡的边缘上，位于要塞前厅的两端；冒险者知道他没法冲上前近距离解决那野兽，因此他取而代之地向它发射了一双石弹。然而，当石弹从手中离开时，他感到坚硬的骨爪紧紧环绕腰、腿和后背，以一种无可理喻的速度把他拖入异形触手的手掌心。或许<?=Lore.pocket_time_winner.name?>可能会在接下来的近身拳击中活下来，但他被拖动的速度快于石弹的飞行，现在他发现自己处在这些石制投射物和他们原来的目标之间————

从前，一个伟大的灵魂放下了它的笔，合上了它的笔记本，沮丧地叹气。
```

## entry-03867
位置：tome-orcs.lua:2998；section：tome-orcs/data/lore/pocket-time.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<? Lore.init_pocket_time_data() ?>Once upon a time, there was <?=Lore.pocket_time_winner.race?> <?=Lore.pocket_time_winner.class?> by the name of <?=Lore.pocket_time_winner.name?>.  <?=Lore.pocket_time_winner.HeShe?> came from humble beginnings, dealing with minor threats like the mad nature-guardian Norgos or yet another reincarnation of Kor'Pul, but as <?=Lore.pocket_time_winner.heshe?> traveled throughout the land, <?=Lore.pocket_time_winner.heshe?> grew stronger and more skilled, and began to take on ever more fearsome opponents.  <?=Lore.pocket_time_winner.HeShe?> purged the corrupted horrors of Yiikgur and claimed the long-forgotten flying fortress for <?=Lore.pocket_time_winner.himher?>self, but even this was a mere stepping stone on the way to the tower of Dreadfell.  The Master, a necromancer of terrible power and even more terrible sadism, waited for <?=Lore.pocket_time_winner.himher?> there with an army of the undead, clutching an ancient weapon of incredible power...  but <?=Lore.pocket_time_winner.name?> bravely pressed on, cutting through the hordes of skeletons and ghouls, prevailing where so many others had failed.  Eventually, <?=Lore.pocket_time_winner.heshe?> stood victorious over the vampire's body, and took the Staff of Absorption with <?=Lore.pocket_time_winner.himher?>, safely away from undead hands.  Maj'Eyal was safe once more.

Unfortunately, what awaited <?=Lore.pocket_time_winner.himher?> next was a quest with even greater stakes.  Orcs, a once-thought-vanquished threat, had reappeared in force in Maj'Eyal!  Despite <?=Lore.pocket_time_winner.name?>'s best efforts to store the staff in a safe place, the orcs stole it, and <?=Lore.pocket_time_winner.name?> was forced to follow them all the way through an ancient, impossibly advanced Farportal to get it back.  The portal crackled and whirled as <?=Lore.pocket_time_winner.name?> held up the Orb of Many Ways to activate it; <?=Lore.pocket_time_winner.heshe?> took a deep breath, closed <?=Lore.pocket_time_winner.hisher?> eyes, and a moment later, <?=Lore.pocket_time_winner.heshe?> became the first person to go from Maj'Eyal to Var'Eyal, the distant continent of the Far East, in centuries.

A long-lost band of allies, the people of Sunwall, awaited <?=Lore.pocket_time_winner.himher?> there - as did four armies of orcs!  Once again, though, <?=Lore.pocket_time_winner.name?> refused to back down when the fate of the world was in <?=Lore.pocket_time_winner.hisher?> hands.  Blessed by High Paladin Aeryn, <?=Lore.pocket_time_winner.heshe?> set out to reclaim the Staff of Absorption from the Orcish Prides.  Storms of fire and ice assaulted <?=Lore.pocket_time_winner.himher?> on <?=Lore.pocket_time_winner.hisher?> way to challenge the grand magus Vor, a foe who could call forth the heavens themselves to pulverize <?=Lore.pocket_time_winner.himher?>, but his meteors weren't enough to stop <?=Lore.pocket_time_winner.himher?>; the dragon-tamers of Gorbat Pride, master wyrmics with unparalleled control over the forces of Nature, merely gave <?=Lore.pocket_time_winner.name?> the opportunity to become the world's most accomplished dragonslayer.  The bone fortress of Rak'Shor Pride crumbled as <?=Lore.pocket_time_winner.heshe?> put its inhabitants to rest, and even when orcs stood in <?=Lore.pocket_time_winner.hisher?> way to do what orcs are best known for at Grushnak Pride, their brute force with strength and steel was simply not strong enough.
<? if not Lore.pocket_time_winner.sacrifice then ?>
But right as <?=Lore.pocket_time_winner.heshe?> set out to climb the tower, <?=Lore.pocket_time_winner.heshe?> got an urgent message from High Paladin Aeryn!  <?=Lore.pocket_time_winner.HeShe?> journeyed across the wastes of Eruan with haste, arriving at another farportal.  Without a thought to where it led, <?=Lore.pocket_time_winner.name?> rushed in at her orders; <?=Lore.pocket_time_winner.heshe?> found <?=Lore.pocket_time_winner.himher?>self in a vast plain of fire and magma, with a narrow stretch of land leading far into the distance.  Behind <?=Lore.pocket_time_winner.himher?>, <?=Lore.pocket_time_winner.heshe?> heard clanging and crashing - the orcs were after <?=Lore.pocket_time_winner.himher?> even here, and the Sun Paladins were valiantly holding the line to keep them away.  They told <?=Lore.pocket_time_winner.himher?> to do one thing: run!  And run <?=Lore.pocket_time_winner.heshe?> did, cutting through and sidestepping countless great red drakes in the process, the glowing magma spitting and bubbling on either side of the perilous stony bridge.  At the end, <?=Lore.pocket_time_winner.heshe?> caught the sight of the Staff for the first time since Maj'Eyal - and the culprits were, surprisingly, a human and an elf!  These two sorcerers, driven by a combination of good intentions, sheer madness, and tragic love, had manipulated the Orc Prides into stealing the staff for them - to what end, <?=Lore.pocket_time_winner.heshe?> still did not know.  Nonetheless, the spell they were channeling was thwarted, and <?=Lore.pocket_time_winner.heshe?> returned to the East victorious, ready to assault the sorcerers' lair of the High Peak.

Threats even greater than any <?=Lore.pocket_time_winner.heshe?> had faced before awaited <?=Lore.pocket_time_winner.himher?>.  The tower itself was trying to stop <?=Lore.pocket_time_winner.himher?>, changing conditions assaulting <?=Lore.pocket_time_winner.hisher?> defenses on each floor, combined with an army of every foe imaginable, but <?=Lore.pocket_time_winner.heshe?> would not be hindered, and pushed past everything on <?=Lore.pocket_time_winner.hisher?> final ascent.  On the top floor, <?=Lore.pocket_time_winner.heshe?> was finally met with the sorcerers, Argoniel and Elandar, face-to-face.  They told <?=Lore.pocket_time_winner.himher?> of their plans with the staff, ones far more dangerous than mere global domination - no, they sought to bring back a threat that only the long-gone Sher'Tul could have dealt with.  A threat long forgotten, lost and tumbling between the stars: Gerlyk, a god driven mad from isolation.  They had to be stopped!

Fortunately, <?=Lore.pocket_time_winner.name?> did not go into this battle alone.  High Paladin Aeryn arrived to fight by <?=Lore.pocket_time_winner.hisher?> side, and the four of them clashed in a fight for the fate of Eyal.  Even with Argoniel's fearsome bone-armor whirling around her, even with Elandar's impressive spells flying through the air, even with the portals summoning foes of all sorts to join the battle...  in the end, the forces of good prevailed.  The sorcerers were defeated, and the portal was sealed, forever.

Eyal had been saved, thanks to <?=Lore.pocket_time_winner.name?>.  Most of the world may not have known what happened at the top of High Peak, but they were in the grips of peril, and were now free of it.  None can say what our champion did after that...  but whatever it was, <?=Lore.pocket_time_winner.heshe?>, and all life on Eyal, lived happily ever after.
<? else ?>
Threats even greater than any <?=Lore.pocket_time_winner.heshe?> had faced before awaited <?=Lore.pocket_time_winner.himher?> in the tower of High Peak.  The tower itself was trying to stop <?=Lore.pocket_time_winner.himher?>, changing conditions assaulting <?=Lore.pocket_time_winner.hisher?> defenses on each floor, combined with an army of every foe imaginable, but <?=Lore.pocket_time_winner.heshe?> would not be hindered, and pushed past everything on <?=Lore.pocket_time_winner.hisher?> final ascent.  Alas, the most trying challenge of these was on the penultimate floor: High Paladin Aeryn.  The Gates of Morning had been destroyed, because <?=Lore.pocket_time_winner.name?> didn't manage to stop the ritual of the Charred Scar, despite the calls to help <?=Lore.pocket_time_winner.heshe?> heard.  She blamed <?=Lore.pocket_time_winner.name?> for this, and the two fought...  but Aeryn relented once <?=Lore.pocket_time_winner.heshe?> realized <?=Lore.pocket_time_winner.heshe?> had been beaten.

On the top floor, <?=Lore.pocket_time_winner.heshe?> was finally met with the sorcerers, Argoniel and Elandar, face-to-face.  They told <?=Lore.pocket_time_winner.himher?> of their plans with the staff, ones far more dangerous than mere global domination - no, they sought to bring back a threat that only the long-gone Sher'Tul could have dealt with.  A threat long forgotten, lost and tumbling between the stars: Gerlyk, a god driven mad from isolation.  They had to be stopped!

The three of them clashed in a fight for the fate of Eyal.  Even with Argoniel's fearsome bone-armor whirling around her, even with Elandar's impressive spells flying through the air, even with the portals summoning foes of all sorts to join the battle...  in the end, the forces of good prevailed.  The sorcerers were defeated, and the portal was sealed, forever...  but at a terrible cost.  <?=Lore.pocket_time_winner.name?> had seen the farportal - the sorcerers had managed to charge it with too much energy, and the Staff alone was not enough to stop it.  <?=Lore.pocket_time_winner.HeShe?> selflessly made the ultimate sacrifice, using <?=Lore.pocket_time_winner.hisher?> life to destroy the portal.

None on Eyal would ever know of <?=Lore.pocket_time_winner.hisher?> sacrifice, or that they were ever in danger...  but thanks to our champion, they could live happily ever after.
<? end ?>
<? if Lore.pocket_time_winner.is_yeek then ?>[i]...Well, let's just assume that's how it went, anyway.  The alternative would make it quite difficult to tell the next story.[/i]<? end ?>

```
译文：
```text
<? Lore.init_pocket_time_data() ?>从前，有一位名叫<?=Lore.pocket_time_winner.name?>的<?=Lore.pocket_time_winner.race?> <?=Lore.pocket_time_winner.class?>。<?=Lore.pocket_time_winner.HeShe?>出身卑微，开始只进行一些简单的冒险，例如疯狂的自然守护者诺尔格斯或者是卡·普尔的另一个化身。随着<?=Lore.pocket_time_winner.heshe?>继续周游各地的旅行，<?=Lore.pocket_time_winner.heshe?>变得越来越强大，越来越熟练，开始尝试挑战越来越强大的对手。<?=Lore.pocket_time_winner.HeShe?>清除了占据伊克格的恐魔，并占领了这个被遗忘已久的飞行堡垒，作为下一步攻入恐惧王座的据点。“领主”，一个有着强大的力量和虐待欲望的恐怖死灵法师，正带领着一支庞大的不死军队在那里等待着<?=Lore.pocket_time_winner.himher?>，手握一把具有强大力量的远古神器……但是<?=Lore.pocket_time_winner.name?>勇敢地向前前进，穿过成群的骷髅和食尸鬼，在许多人失败的地方获得了成功。最终，<?=Lore.pocket_time_winner.heshe?>光荣地站在那具吸血鬼的尸体之上，手中拿着从死灵大军手中夺回的吸能法杖，马基埃亚尔再次恢复了和平。

然而，等待着<?=Lore.pocket_time_winner.himher?>的则是更加危险的挑战。兽人，一个认为已经被战胜已久的威胁，重新出现在了马基埃亚尔的土地上！尽管 <?=Lore.pocket_time_winner.name?>努力将法杖存在了安全的地方，兽人们还是设法偷走了它，<?=Lore.pocket_time_winner.name?>不得不追随着他们，穿过发达到让人难以置信的远行传送门，试图追回法杖。<?=Lore.pocket_time_winner.name?>手握着多元水晶球，深吸一口气，穿过劈啪作响的传送门漩涡，那一瞬间，<?=Lore.pocket_time_winner.heshe?>成为第一个从马基·埃亚尔到达瓦·埃亚尔的人，那是和马基·埃亚尔分割了几个世纪的远东大陆。

在那里等待着<?=Lore.pocket_time_winner.himher?>的，有着失落已久的盟友，太阳堡垒的人们——也有四支庞大的兽人军队。又一次，世界的命运落在了<?=Lore.pocket_time_winner.hisher?>手中，而<?=Lore.pocket_time_winner.himher?>绝不愿朝困难屈服。在接受了高阶太阳骑士艾琳的祝福之后，<?=Lore.pocket_time_winner.heshe?>出发前去进攻兽人部落，夺回被夺走的吸能法杖。与大魔导师沃尔的战斗充满了火焰和冰霜的风暴，那是可以召唤来自天空的力量来试图毁灭对手的强大敌人，但是沃尔的陨石也无法阻挡<?=Lore.pocket_time_winner.himher?>的胜利。加伯特部落的驯龙师和高阶龙战士对自然力量的掌控无出其右，但这只是让<?=Lore.pocket_time_winner.name?>成为了世界上最伟大的屠龙者。随着拉克·肖部落高大的白骨堡垒轰然倒下，<?=Lore.pocket_time_winner.heshe?>让死者们终于得到了安息。最终，以兽人中最强大的力量著称的格鲁希纳克部落的精英部队也倒在了<?=Lore.pocket_time_winner.hisher?>面前。
<? if not Lore.pocket_time_winner.sacrifice then ?>
但是正当<?=Lore.pocket_time_winner.heshe?>攀爬高塔之前，<?=Lore.pocket_time_winner.heshe?>收到了来自高阶太阳骑士艾琳的紧急消息。<?=Lore.pocket_time_winner.HeShe?>急忙穿越了艾露安的废墟，到达了另一座远行传送门的面前。没有任何犹豫，<?=Lore.pocket_time_winner.name?>冲进了传送门中；<?=Lore.pocket_time_winner.heshe?>发现自己身处一片广阔的火焰与岩浆平原，狭长的土地通往远方。在<?=Lore.pocket_time_winner.himher?>身后，<?=Lore.pocket_time_winner.heshe?>听见了兵器的碰撞声：那是追随<?=Lore.pocket_time_winner.himher?>到达这里的兽人军队，太阳骑士们正严守防线，试图阻止敌军靠近。那些太阳骑士只告诉<?=Lore.pocket_time_winner.himher?>一件事：快跑！于是，<?=Lore.pocket_time_winner.heshe?>不顾一切地奋勇向前冲去，穿过和避开无数的红色巨龙，灼热的岩浆在危险的石桥两侧喷涌而出。最终，<?=Lore.pocket_time_winner.heshe?>的眼前终于又出现了吸能法杖的身影——然而，令人惊讶的是，真正的幕后黑手竟然是一个精灵和一个人类！那两位法师，在良好的意图，无尽的疯狂和悲剧性的爱的驱使之下，操纵兽人部落偷取法杖给他们——他们的目的到底是什么，<?=Lore.pocket_time_winner.heshe?>仍然尚不清楚。然而，他们所施展的法术被阻止了，<?=Lore.pocket_time_winner.heshe?>胜利回到了远东大陆，准备突袭这两位法师位于巅峰高塔的最终堡垒。

在那里等待着的，是远胜于<?=Lore.pocket_time_winner.heshe?>之前所见过的一切的恐怖挑战。高塔本身正在试图阻挡着<?=Lore.pocket_time_winner.himher?>，在每一层不断切换着环境，对<?=Lore.pocket_time_winner.hisher?>的防御做出挑战。在每一层，都有着一切可能出现的可怕怪物的严加守卫，但是<?=Lore.pocket_time_winner.heshe?>毫不畏惧，奋勇向前，击败了一切敌人，最终到达了顶层。在顶层，<?=Lore.pocket_time_winner.heshe?>终于见到了那两位法师，埃兰达和艾格尼尔。他们告诉了<?=Lore.pocket_time_winner.himher?>有关法杖的真正计划，这比征服世界还要可怕的多——不，他们将要召回只有消失已久的夏·图尔人才能应对的远古威胁。那是被世人遗忘，流浪在群星中的恐怖：盖里克，在长期的隔绝之中陷入了无尽的疯狂。他们的计划必须被阻止！

幸运的是，<?=Lore.pocket_time_winner.name?>并未独自战斗。高阶太阳骑士艾琳来到了这里，与<?=Lore.pocket_time_winner.hisher?>并肩作战，这四个人将会为了埃亚尔的未来展开一场旷世之战。艾格尼尔恐怖的骨盾环绕在她的四周，埃兰达强大的法术在空中撕裂一切，四周的传送门不断召唤各种敌人加入战场……然而最终，正义终于得到了胜利。法师们被打败了，传送门也被永久封印了。

埃亚尔的命运被<?=Lore.pocket_time_winner.name?>拯救了。这个世界上的大部分人，还不曾知道在巅峰上发生了什么，不知道世界曾经那样危在旦夕，但现在已经重现了和平。没有人知道，我们的英雄在之后去了哪里……但是，无论如何，<?=Lore.pocket_time_winner.heshe?>，以及埃亚尔的所有生灵，一直幸福地生活了下去。
<? else ?>
在那里等待着的，是远胜于<?=Lore.pocket_time_winner.heshe?>之前所见过的一切的恐怖挑战。高塔本身正在试图阻挡着<?=Lore.pocket_time_winner.himher?>，在每一层不断切换着环境，对<?=Lore.pocket_time_winner.hisher?>的防御做出挑战。在每一层，都有着一切可能出现的可怕怪物的严加守卫，但是<?=Lore.pocket_time_winner.heshe?>毫不畏惧，奋勇向前，击败了一切敌人，最终到达了顶层。在倒数第二层，出现的挑战者是出人意料的：高阶太阳骑士艾琳。晨曦之门被摧毁了，因为<?=Lore.pocket_time_winner.name?>未能阻止法师们在灼烧之痕举行的仪式。艾琳将责任归咎于<?=Lore.pocket_time_winner.name?>的身上，他们进行了激烈的战斗……然而最后，艾琳被击败了。

在顶层，<?=Lore.pocket_time_winner.heshe?>终于见到了那两位法师，埃兰达和艾格尼尔。他们告诉了<?=Lore.pocket_time_winner.himher?>有关法杖的真正计划，这比征服世界还要可怕的多——不，他们将要召回只有消失已久的夏·图尔人才能应对的远古威胁。那是被世人遗忘，流浪在群星中的恐怖：盖里克，在长期的隔绝之中陷入了无尽的疯狂。他们的计划必须被阻止！

这三个人将会为了埃亚尔的未来展开一场旷世之战。艾格尼尔恐怖的骨盾环绕在她的四周，埃兰达强大的法术在空中撕裂一切，四周的传送门不断召唤各种敌人加入战场……然而最终，正义终于得到了胜利。法师们被打败了，传送门也被永久封印了……但是，付出的代价是惨重的。<?=Lore.pocket_time_winner.name?>看到了远行传送门的景象——两位法师为它注入了太多的能量，光使用吸能法杖已经无法阻止它了。<?=Lore.pocket_time_winner.HeShe?>无私地做出了牺牲，使用<?=Lore.pocket_time_winner.hisher?>的生命作为代价，摧毁了传送门。

在埃亚尔，没有人知道是<?=Lore.pocket_time_winner.hisher?>牺牲拯救了他们，甚至对他们曾经出于怎样的危机浑然不知……然而，正是因为这位英雄的努力，他们才能够和平幸福地生活了下去。
<? end ?>
<? if Lore.pocket_time_winner.is_yeek then ?>[i]……好吧，我们假设事情就是这样的。如果不这样的话，要想讲下一个故事就变得太困难了。[/i]<? end ?>

```

## entry-03868
位置：tome-orcs.lua:3046；section：tome-orcs/data/lore/pocket-time.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<? Lore.init_pocket_time_data() ?>Once upon a time, there was a spirit known as the Eidolon, older than anything on Eyal.  Some called it a savior, a bringer of order and justice; others, a dark god, spreading terror for its own amusement.  Such mortal classifications are hopelessly inadequate to describe the incomprehensibly far-sighted motivations of a being nearly as old as time itself...  but if you were to ask the Eidolon, it would call itself a storyteller.

Whether the story exists only in its own head or is reflected across the Shandral system, none can say - but the Eidolon needed heroes for its story, as it always has.  Today, the hero it needed was a master of battle, the likes of which had not been seen since the age of Garkul the Devourer.  It considered a few different options, deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen.  Its chosen protagonist met every challenge put before <?=Lore.pocket_time_winner.himher?>, sometimes with ease, often with difficulty, occasionally escaping through luck alone, but eventually stood atop the High Peak, having saved Eyal from the greatest threat it had ever faced<? if Lore.pocket_time_winner.sacrifice then ?> by sacrificing <?=Lore.pocket_time_winner.himher?>self to shut down the Sorcerers' farportal<? end ?>.
<? if not Lore.pocket_time_winner.sacrifice then ?>
And what then?  A master of battle has nothing to do once the battle is won.  <?=Lore.pocket_time_winner.HeShe?> could've sought out harder foes, but the only ones <?=Lore.pocket_time_winner.heshe?> would be likely to find would either be pointless to face, or outright harmful to the citizens of Eyal; they would add nothing to the story.  The Eidolon could have introduced a foe strong enough to finally destroy <?=Lore.pocket_time_winner.himher?>, but what kind of ending would that be?  Instead, the Eidolon decided to let its protagonist retire as <?=Lore.pocket_time_winner.heshe?> wished...  whether <?=Lore.pocket_time_winner.heshe?> chose to descend to inevitable doom in the Infinite Dungeon, to attempt to slay impossible foes like Atamathon and Linaniil, or to simply retire and live out the rest of <?=Lore.pocket_time_winner.hisher?> days in the reclaimed Sher'Tul fortress.  In any case, the story was over; there wasn't any room left for the rest of <?=Lore.pocket_time_winner.name?>'s life.<? end ?>

Of course, a character like that can't simply be thrown away.  The story may be over, but it can be told again and again, and as such there would be as many Heroes of Maj'Eyal as there were people who'd listen to the story, each hearing it and imagining it slightly differently from the next.  Even the storyteller would dream up more situations for the Hero of Maj'Eyal, always wondering - what if I found an even match for this first warrior?  Don't I owe <?=Lore.pocket_time_winner.himher?> the reward of a fight <?=Lore.pocket_time_winner.heshe?> would be eager to participate in, and one that would give <?=Lore.pocket_time_winner.himher?> the challenge <?=Lore.pocket_time_winner.heshe?> craved so dearly?  Wouldn't such a duel be worth writing about?  And so, it kept <?=Lore.pocket_time_winner.name?> in mind, promising to remember <?=Lore.pocket_time_winner.himher?> whenever it found or created a threat worthy of <?=Lore.pocket_time_winner.himher?>.

[b]<?=player.name?>[/b], you crave the thrill and tension of a close fight as much as <?=Lore.pocket_time_winner.heshe?> does.  I owe this opportunity to you in life, and the Scourge from the West in <?=Lore.pocket_time_winner.hisher?> legend; all I ask in return is that the two of you give me a battle that the people of Eyal will sing songs about.
```
译文：
```text
<? Lore.init_pocket_time_data() ?>从前，有一个叫做艾德隆的灵魂，比埃亚尔的一切都要古老。有人称之为救世主，是秩序和正义的使者；也有人称之为黑暗之神，传播恐怖以自娱自乐。这样的凡人分类，是无可救药地不足以描述一个几乎和时间一样古老的存在那不可思议的长远动机的……但是，如果你亲自问它的话，它会自称是一个讲故事的人。

不管这个故事是只存在于它的脑海里，还是反映在整个珊德拉星系之中，没有人知道——但是，艾德隆的故事里需要英雄，一直都是这样。今天，他所需要的英雄是一位战斗的大师，一位从吞噬者加库尔的时代以来就未曾出现的大师。他会综合考虑各种各样的可能性，面对无数的困难，有些可能允许一部分的错误，但是最终只会选择一个。被它所选中的主角战胜了摆在<?=Lore.pocket_time_winner.himher?>面前的一切挑战，有时举重若轻，有时艰难取胜，也有的时候则透过运气勉强通过。但最终，<?=Lore.pocket_time_winner.himher?>站在了巅峰之上，<? if Lore.pocket_time_winner.sacrifice then ?>通过牺牲<?=Lore.pocket_time_winner.himher?>的生命来关闭了法师的远行传送门<? end ?>，从而把埃亚尔从其所面临的最大的威胁面前解救出来。
<? if not Lore.pocket_time_winner.sacrifice then ?>
之后呢？在战斗胜利之后，这位为战斗而生的大师就无事可做了。<?=Lore.pocket_time_winner.HeShe?> 本可以找到更加强大的敌人，但<?=Lore.pocket_time_winner.heshe?>很快发现自己面对的东西要么毫无意义，要么只会对埃亚尔的世界有害，不会给故事增添任何内容。艾德隆也可以创造一个强大到足以击败<?=Lore.pocket_time_winner.himher?>的敌人，但这又是什么样的结局呢？最终，艾德隆决定遵循<?=Lore.pocket_time_winner.heshe?>的意愿，让这位英雄从此退休……无论<?=Lore.pocket_time_winner.heshe?>选择前往无尽地下城寻求无穷无尽的挑战，去挑战像阿塔玛森或是莱娜尼尔这样几乎不可能击败的恐怖敌人，还是就此在夏·图尔堡垒中度过余生。无论是哪一种，这个故事都结束了，<?=Lore.pocket_time_winner.name?>的故事就此走到了尽头。<? end ?>

当然，这样的角色不能简单地被抛弃。故事可能已经结束了，但它可以一次又一次地被讲述。这样一来，每有一个愿意听故事的，就会出现一位马基·埃亚尔的英雄。每个人都听到了故事，并且对它的想象与下一个略有不同。即使是讲故事的人，也会为马基·埃亚尔的英雄设想更多的场景，总是在想——我是否能给这第一位战士找到一位势均力敌的对手呢？我是否正欠<?=Lore.pocket_time_winner.himher?>一个奖赏，一场真正能够让<?=Lore.pocket_time_winner.heshe?>兴奋地参与的战斗，一个<?=Lore.pocket_time_winner.himher?>渴望已久的终极挑战呢？这样的战斗，难道不值得记述下来吗？因此，它将<?=Lore.pocket_time_winner.name?>的名字在脑海中记录下来，愿意一直牢记住<?=Lore.pocket_time_winner.himher?>，直到它找到或者创造了一位真正能够和<?=Lore.pocket_time_winner.himher?>势均力敌的对手。

[b]<?=player.name?>[/b]，你和<?=Lore.pocket_time_winner.heshe?>一样，渴望势均力敌的战斗所带来的刺激与紧张。我此生欠你这个机会，也欠传说中的西方灾星这个机会；作为回报，我只希望你们二人为我献上一场足以让埃亚尔人传唱的战斗。
```

## entry-03869
位置：tome-orcs.lua:3113；section：tome-orcs/data/lore/primal-forest.lua；source_tag：_t；args_order：None；special：None

原文：
```text
EYAL NEEDS YOU!

The damage left in the Scintillating Caverns, in Norgos' Lair, and in countless other places has only now become clear, after the Hero of Maj'Eyal made them safe to explore once more.  Now that peace has been brought to these lands, Eyal is beginning to heal - but with the arrival of our magic-using cousins from the East and the Allied Kingdoms' growing acceptance of magic, the balance may once more tip towards ruin - but YOUR help can keep Eyal healthy!  Join the Menders, and start helping the planet today!

LEARNING AND OBSERVING

Our founders, once Guardians of Shatur, have always known the importance of maintaining a balanced ecosystem.  Do your hobbies include birdwatching, exploring the wilderness, and taking in the sights of natural flora?  We can provide you with a list of animals, plants, and fungi of interest; simply go out and write down where you explored, when, and how many of these species you saw.  Our experienced naturalists can use this information to track migration patterns and monitor the spread or decline of those species, allowing us to take action if one becomes endangered or invasive; already, they're working to restore the balance disrupted by the Hero of Maj'Eyal's constant slaying of local wildlife.  Change is inherent to the natural order; our experts know to only step in if a change would drastically and destructively hurt the ecosystem.  Nature solves most of its problems on its own, but occasionally we may need to hold its hand (particularly in response to mutations caused by unchecked use of arcane magic).  If you'd like to learn more about the natural order, we have a diverse community of knowledgeable naturalists who are happy to answer questions or provide a more thorough education.

REPAIRING AND HEALING

Volunteers who prefer a more hands-on approach can expect to start making a difference right away, by joining our reclamation and decontamination efforts.  It's no secret that the Hero of Maj'Eyal's many battles took their unfortunate toll; many places are still littered with magic-contaminated objects or bodies, and in some places the ground itself has been polluted by the residual effects of these spells.  (This is, of course, to say nothing of the trees burned down, etc. by beasts and ne'er-do-wells trying to stop the Hero!)  You can help by destroying dangerously magical objects, planting trees, slaying ecologically-disruptive beasts (such as Norgos), and participating in cleansing rituals to speed up the healing process.

ABILITY, RESPONSIBILITY, AND ACCEPTANCE

The wilds of Eyal are a dangerous place; we do not expect our scholars to go into them defenseless!  For those who are already accustomed to use of the arcane, our partnership with the Living Fossils allows us to identify safe and responsible methods of using magic, and provide them with an introduction to the ways of Nature, and those who are already adept with Nature can always hone their skills with our veteran members.  If you have no ability with either, you're in luck!  We're eager to show you how to accept Nature's favors to defend yourself.  Anyone can learn to summon loyal beasts or channel wyrmic strength if they're willing to try!  These abilities can be used without giving up your attunement to the arcane, but you may find that you don't need your spells anymore, once you've seen how effective Nature's power is.  We will never force you to give up magic, but if you happen to be looking for a greater commitment, speak to your instructor about following the path of the oozemancer.

```
译文：
```text
[b]埃亚尔需要你！[/b]

在马基·埃亚尔的英雄扫清了闪光洞穴、诺尔格斯巢穴、和世界各处数不清的场所，让人们可以在那些安全的地方探索之后，人们终于开始正视魔法大爆炸对那里所造成的伤害。尽管这些地方现在已经变得和平，埃亚尔正在逐渐恢复——但是，由于我们那些使用魔法的东部同胞的到来，以及联合王国越来越接受奥术魔法使用的影响，自然和魔法之间的平衡被渐渐破坏，世界濒临毁灭的边缘——但是，[b]你的[/b]帮助可以让埃亚尔保持健康！请加入修复者，从今天开始，帮助这颗星球吧！

[b]学习与观察[/b]

我们的创始人曾是夏特尔的守护者，他们一直深切了解有关维持一个平衡的生态系统的重要性。你喜欢观鸟，探索大自然，欣赏多姿多彩的植物吗？我们可以向你提供一系列有关各种奇珍异兽、以及奇特的植物和真菌的列表。只要你在四处探索，记录下各种观察到的生物的分布和数量。我们那些富有经验的自然学家可以使用这些信息来追踪这些生物迁徙的模式，观察它们的扩散和消亡。这样，如果有一种生物濒临灭绝或受到入侵，我们就可以立即采取行动。现在，我们正在修复那些因为马基·埃亚尔的英雄对自然生物的杀戮，而遭到破坏的各地脆弱的生态平衡。改变是自然重要的组成部分，因此我们的专家只会在生态系统面临毁灭性严重威胁的时候，才会选择介入。大自然能够自己解决它大部分的问题，但有时，我们也需要亲自向大自然伸出援手，例如应对那些因为不恰当的奥术魔法使用造成的变异物种。如果你想要更多了解大自然的秩序和平衡，我们有一个多元化的，知识渊博的自然学家群体。他们十分乐意回答你的各种问题，乃至向你提供深入的教育。

[b]修复与治疗[/b]

对于那些更加喜欢亲自动手的志愿者，你们可以加入我们的修复和净化事业，立刻给这个世界带来改变。马基·埃亚尔的英雄的众多战斗也带来了许多不幸的损失，这并不是一个秘密。许多地方到处都是被魔法污染的物件和尸体，还有些地方的土地仍然被残留的魔法所污染。当然，更不用说，还有那些野兽和不负责任的蠢货试图阻止英雄的时候，被他们烧毁的森林！你可以通过摧毁危险的魔法物品，重新种植树木，杀死那些破坏生态的野兽（比如诺尔格斯）以及参加我们的净化仪式，来加快这个世界愈合的进程。

[b]能力、责任与认可[/b]

埃亚尔的野外是一个危险的场所；我们可不希望我们的学者手无寸铁地走进荒野！对于那些已经习惯于使用奥术魔法的人，我们和那些活化石的合作，让我们可以辨别出正确和理性的使用魔法的做法，并向你们展示自然之道的基础。对于那些已经精通自然力量的人，你们可以和我们的老成员之间相互切磋，磨练技巧。如果你两者都不了解的话，那么你就走运了！我们十分乐意向你展示如何使用自然的力量来保护自己。只要你愿意尝试，每个人都有机会掌握召唤忠诚野兽的能力，或是引导巨龙的力量！这些能力在你不放弃奥术魔法的情况下，也可以尽情使用。但是我想，当你见到大自然的力量是多么有效而强大的时候，你就再也不想使用你过去使用的那些魔法了。我们绝不会强迫你放弃魔法，但是，如果你想要追求更多献身于自然事业的话，也可以和我们的导师交谈，我们向你介绍软泥使的力量。
```

## entry-03870
位置：tome-orcs.lua:3159；section：tome-orcs/data/lore/primal-forest.lua；source_tag：_t；args_order：None；special：None

原文：
```text
[i](You see here a leaf-bound journal; the moment you open it, it begins to wither and crumble.  You manage to rip out one page; it is still disintegrating, but slowly enough that you can read it before it turns to dust.)[/i]

Another vandalized poster.  Calling us traitors, collaborators, declaring themselves the True Ziguranth.  Fools, the lot of them.

When I established the Menders, it wasn't because I thought the arrival of a handful of magic-users who also happen to be decent people disproved anything taught in Zigur or my childhood in Shatur.  It wasn't because I suddenly forgot that anything derived from arcane magic, no matter whether or not it's wrapped up in some mumbo-jumbo about the heavens, carries the risk of mutating into something that could put the Spellblaze to shame.  It was because those maniacs had ignored the shifting political tides for so long that they found themselves sliding into irrelevance, then went and skipped directly over irrelevance into pariahdom with that foolhardy assassination attempt.  They can blame the Far East all they want, but that was only the last nail in the coffin, alongside widespread acceptance of runes and alchemists operating openly across the continent.

I can appreciate their dedication.  I can appreciate their frustration, and how seeing the world treating magic-use as normal would just make them want to get more violent - but the fact is, the raid on Zigur was a mercy kill, preventing the fanatics from making us look even worse in the public eye.  We are long past the point where intimidation can get us anywhere - so we need to try a new approach.  If reminding the world of the horrors of magic isn't working anymore, the Spellblaze and the Age of Dusk being too faded from public memory, then we need to remind them of the wonders of Nature instead, wonders they can see for themselves, today.  If the public won't believe that magic is evil, they can believe that Nature is better.  If we can't make magic taboo, we can make magic obsolete...  and all of this gathers support we'd otherwise lack, curious minds waiting to be taught the beauty of Nature and warned of the hazards of the arcane.

So maybe the old guard's been overrun with Thaloren, youths, and others who care a great deal more about loving nature than hating magic.  I don't see why this is a problem - making Nature stronger will make it more capable of resisting the damage magic may inflict.  We've allowed the idea of supporting Nature over magic to survive the Allied Kingdoms' treaty with the Gates of Morning, the raid on Zigur, and the attacks on Ziguranth patrols.  We've established ourselves as a selfless, charitable organization working for the good of all, a reputation that will grant us significantly more credibility than our previous public image of a band of crazed fanatics.

Perhaps most meaningfully of all, there are [i]far[/i] more Menders now than there were Ziguranth in the last century.  These allies will help us support Nature to an incredible degree, and we've started offering volunteer courses in classical anti-magic training, allowing them to further refine our techniques for dealing with rogue mages.  If and when arcane magic causes another catastrophe, these allies will rally behind us as we defend Nature from those who threaten it...  And, who knows, maybe we actually CAN teach mages to show a sane level of restraint without wiping them all out.  I'm keeping my eyes open for ways to make that happen, no matter how unlikely they may be.

In the meantime, paying off Stone Warden trainers and buying enough mindstars and herbal infusions for our initiates isn't cheap.  I'm not proud of what I'm doing to pay the bills, and am fully aware of what it'd do to the organization if someone saw me, but this is the fastest and easiest money I've ever made.  Ten minutes of concentration, a few hours to re-establish my equilibrium, and I can grow enough cheerblossom to cover our expenses for a week.
```
译文：
```text
[i]（你看到了一本被书页包裹的笔记；当你打开它的时候，它就开始慢慢枯萎、碎裂。你努力撕下了一页，它仍然在慢慢分解，但是分解的速度慢到你能够读完，才最终化成了尘土。）[/i]

又有一张海报被他们毁坏了。他们称我们为叛徒、通敌者，宣称自己才是真正的伊格兰斯。他们这群傻瓜。

我建立修复者的理由，并不是因为那些碰巧上是好人的魔法使用者的到来，就能颠覆我过去在夏特尔和伊格的时候所受到的一切教育。这也不是因为我已经遗忘了，任何从奥术魔法之中产生的力量，不管是否被他们包裹在有关天空的一系列繁文缛节里，仍然有着被人扭曲，产生比魔法大爆炸更加可怕的灾难的危险性。这一切都是因为，那群疯子一直以来都无视着政治潮流中发生的巨大转变，不知道自己已经变成了无关紧要的局外人。然后，他们那场莽撞的暗杀行动，彻底让他们的地位从局外人成为了贱民。他们尽管可以把他们所遭受的不幸都归咎于远东的人，但这只是他们棺材板上的最后一颗钉子而已，而没有意识到早在更早之前，符文已经在这片大地上广泛使用，炼金术师在各处公开营业了。

我很欣赏他们的奉献精神。我也很能理解他们的挫败感，他们看到，这个世界越来越将魔法的使用看做稀松平常的事，而变得越来越暴力——但是，实际上，伊格被摧毁对我们来说可以说是一种安乐死，这避免了那些狂热分子进一步在公众面前破坏我们的形象。我们早就应该知道，光靠暴力威慑是不能解决一切问题的——因此，我们必须尝试一种新的办法。既然黄昏纪和魔法大爆炸这样的过去，早就已经在公众的视野之中淡忘。过去警告世人魔法的恐怖的方法，已经不再能够起到作用。那么，我们应该改为向他们展示大自然中那些他们今天就能亲眼目睹的奇迹。既然公众已经不相信魔法是邪恶的了，我们应该向他们展现，自然是更好的。如果我们不能让魔法成为禁忌，我们可以让魔法成为一种过时的技术……而这一切可以吸引无数我们过去所忽视的支持者，我们将可以在他们充满好奇心的心灵中展现自然的美好，并警告奥术魔法带来的恐怖。

所以，那些过去的守护者，现在已经被自然精灵，年轻人，还有更多比起对魔法的痛恨，更关心对自然的热爱的人所代替。我不认为这里有什么问题——让自然的势力更加强大，才能抵挡魔法所造成的伤害。我们高举着“自然胜过魔法”的旗号，从联合王国与晨曦之门的条约、对伊格的袭击，以及对伊格兰斯巡逻队的搜捕中幸存下来。我们建立了一个无私的慈善组织，为所有人的利益而工作。这一声誉，比起过去一群狂热的极端分子的公众形象，在大众面前更加可信地多。

另外，最重要的是，我们招募的修复者的数量，已经[i]远远超过[/i]伊格兰斯一个世纪里招募的成员的数量。这些盟友对我们在保护自然事业上的支持达到了一个难以相信的程度。我们已经开始了向他们提供传统的反魔法训练的志愿课程，让他们进一步锤炼自己对抗游荡法师的能力。如果奥术魔法造成了另一次灾难，这些盟友将会追随我们成为我们保护自然免受威胁的坚强后盾……另外，谁知道呢，也许我们[b]真的可以[/b]教会那些法师，学会一点理性的克制，而不需要把他们全部杀光。我会一直寻求实现这种目标的方法，不管它的可能性有多么渺茫。

与此同时，支付岩石守卫训练师的工资，以及给我们的新成员购买足够的灵晶和草本纹身的价格可不便宜。我知道我支付账目的方法不太光彩，我也知道如果被人看到这事，我的组织会受到多么坏的影响，但是这是我能找到的赚钱最快最容易的方法了。只要十分钟的专注，再花上几个小时来恢复我的失衡值，我种出的鼓舞之花就足够支付我们一个礼拜的开销了。
```

## entry-03871
位置：tome-orcs.lua:3307；section：tome-orcs/data/lore/sunwall.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
We've done it... we've finally done it. Well, granted, our %s did much of the work, but the result is the same: neither the East nor the West will ever need to fear Orcish rule again. The Prides have been crushed, the survivors have been contained, and our patrols are mopping up the few remaining bands of futile stragglers. Our long-lost allies from the West have come to support us with materials and manpower, and we can finally turn this entire continent into something beautiful. For the first time, Sunwall will not be the solitary bastion of civilization on Var'Eyal.

And yet...

There is one group that remains.  A tiny Orcish pride, really more of a small town, managed to evade our savior's wrath...  a single weed on the edges of our pristine garden, a troubling ember threatening to set the whole continent aflame.  King Tolak has noble aims in trying to set a better example than his vengeful father, but I doubt he'd risk redeeming the Orcs if he'd been through what we have.  The Allied Kingdoms don't know what it's like to live in fear of the Prides, knowing that at any moment they could overrun the Sunwall and take our heads as trophies.  They've got a farportal to hide behind, and don't have to think about their homes and families falling to the same horror that we've been struggling against for our entire lives.  If they did...  suffice to say, they wouldn't have bothered putting up a comfortable camp for the surviving Orcs until the continent was truly safe.

By the Sun...  why would our High Paladin agree to this treaty?  After what we've all been through...

The Orcish scouts are getting bolder.  They've been approaching closer before fleeing, and coming more frequently.  They haven't engaged us yet, but it's only a matter of time...  and all I'm allowed to do is sit and wait on this ugly little bridge, as the West watches from a continent away.  Staring at an open wound, waiting for it to become infected, because they'd rather make a pretty little bow out of the bandages.
```
译文：
```text
我们做到了……终于做到了。好吧，诚然，大部分工作是我们的%s完成的，但结果并无不同：东方和西方都再也不必惧怕兽人统治。四大兽人部落已被粉碎，幸存者受到控制，巡逻队正在扫荡所剩无几、徒劳流窜的残兵。失散已久的西方盟友带着物资和人力前来支援，我们终于可以把整片大陆建设得更加美好。太阳堡垒将第一次不再是瓦·埃亚尔唯一的文明堡垒。

然而……

仍有一群兽人存在。一个小小的兽人部落——其实更像一座小镇——躲过了救世主的怒火……如整洁花园边缘的一株杂草，又像威胁点燃整片大陆的一点余烬。托拉克国王试图树立比复仇心切的父亲更好榜样，志向固然高尚；可若他经历过我们所经历的一切，我怀疑他是否还会冒险去拯救兽人。联合王国不知道活在四大部落阴影下是什么滋味，不知道太阳堡垒随时可能被攻陷、我们的头颅被割下当作战利品的恐惧。他们有远行传送门可作屏障，无需担心家园和亲人遭遇我们一生都在抗争的同样恐怖。如果他们也要担这种心……只消说，在大陆真正安全之前，他们绝不会费心为幸存兽人搭起舒适营地。

以太阳之名……经历这一切之后，我们的至高太阳骑士为何还会同意这份条约？

兽人斥候越来越大胆。他们逃走前会靠得更近，出现得也更频繁。虽然尚未交战，却只是时间问题……而我获准做的只有坐在这座难看的小桥上等待；西方人则从另一个大陆远远观望。就像盯着一道敞开的伤口，等它感染，只因他们宁愿把绷带系成漂亮的蝴蝶结。
```

## entry-03872
位置：tome-orcs.lua:3400；section：tome-orcs/data/lore/sunwall.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
(As you approach the farportal, a herald emerges, holding an envelope; he doesn't quite hand it to you as much as throw it at you from a safe distance, then salutes and retreats back into the swirling rift.  The letter bears the royal seal of the Allied Kingdoms.)

%s...  I think I'm beginning to understand why you have acted this way.  At first, I was...  well, not as much surprised as disappointed.  I'd thought that showing your people mercy was the right decision.  That my father had been too consumed by rage, that the Orcs could be truly be better people if we gave them a chance, and if you were shown how much of a better place Eyal could be if you were to cooperate with us.  That no matter what my father, my mother, and my allies had told me, the Orcish race contained, somewhere deep down, the same potential for learning, growth, and beauty present in Humans, Halflings, Elves, Dwarves, and Ogres.

But now...  I see no good in you.  So many are dead, because I couldn't bring myself to admit that some people are beyond redemption.  Because I thought all you needed was a second chance, that you had goals other than blind, bloody revenge, that you'd see that we had held you in the grip of our absolute mercy, and opted to offer you an open hand rather than crush you as easily as clenching our fist.

I will not make the same mistake again.

You've shown me that the Orcish heart is empty of everything but lust for death and destruction, that no matter how good a future is laid out in front of you, you will discard it simply for the thrill of battle against the reasonable people who want this better future to come.  You've shown me that the prejudices I've strived to transcend were right all along.  You've shown me that my father's only mistake was not going far enough - a continent free of Orcs is not enough to keep us safe.  Instead, your kind must be purged from all of Eyal - and the battle to make this happen is inevitable, for you will continue pushing for it no matter how much we try to make peace an option.  And yet...  you've made me understand the reason of this approach, of treating everyone else like an irrational threat to your existence, for it is the only proper way for us to treat you.

You won't get another second chance from us.  Instead, we'll give you the only thing you've ever wanted: a battle.  Through this portal waits the army of the Allied Kingdoms, once foes or begrudging co-inhabitants who have grown into true allies because we have a desire for peace and cooperation that your kind will never know.  We wait on an open battlefield, ready to demonstrate our combined might.  The Shaloren of Elvala prepare spells as the Ogres grip their clubs tighter; the Halflings and Humans of Derth and Last Hope have forgotten their age-old rivalry, working together to brew alchemical bombs and build great golems, or take up positions with a bow or sling; the Dwarves of Iron Throne and the Thaloren of Shatur, not even proper allies with us before now, realize you are too great a threat to go neglected, and now our ranks are lined with Wilders summoning countless beasts and treants, and fierce warriors who will #{italic}#not#{normal}# be moved.  Even the forces of the Sunwall have joined us, a contingent of their finest warriors sent to reinforce our lines and quickly train our soldiers in the magical techniques they've honed over the years, using you irredeemable savages as their sharpening stones.

I shall be waiting in the front line of this glorious alliance, sword in hand.  I, King Tolak the Fair, son of Toknor who once purged your people from Maj'Eyal, I who once fought to spare your kind from slavery or extinction, now eagerly await the opportunity to finish what he started.  If I die, Toknor's bloodline dies with me; this is a risk I am willing - no, #{italic}#excited#{normal}# to take, to settle the fate of all civilized peoples of Eyal, once and for all.

You want your revenge on my father's people, foul cur?  #{italic}#Come and get it.#{normal}#

(You admit, it is rather tempting...  but the guaranteed safety of your people takes priority, and besides, you wouldn't put it past the Allied Kingdoms to have a team of archers and slingers waiting to snipe everyone who came through, one by one.  You destroy the portal, eliminating King Tolak's army as a threat, and ensuring Sun Paladin Aeryn won't be getting any reinforcements.  Time to take advantage of your newfound privacy, and finish off the Sunwall forces, once and for all...)
```
译文：
```text
（你走近远行传送门时，一名传令官从中现身，手持信封。他与其说是把信交给你，不如说是隔着一段安全距离将它扔了过来；随后敬礼，退回旋转的裂隙。信上盖着联合王国的皇家印章。）

%s……我想，我开始明白你为何如此行事了。起初我……与其说惊讶，不如说失望。我原以为宽恕你的人民才是正确决定；原以为父亲只是被怒火蒙蔽；原以为只要给兽人机会，让你们看到若与我们合作，埃亚尔会变得多么美好，你们便真能成为更好的人。无论父亲、母亲和盟友怎样告诫我，我都相信兽人族内心深处也拥有和人类、半身人、精灵、矮人及食人魔一样的潜力，能够学习、成长，创造美好。

可如今……我在你身上看不到丝毫善意。因为我不愿承认有些人无可救赎，才有如此多人丧命。因为我以为你需要的只是第二次机会，以为你除了盲目而血腥的复仇还另有目标；以为你会明白，我们本可用绝对力量把你攥在掌中轻易碾碎，却选择向你伸出援手，施以彻底的慈悲。

我不会再犯同样的错误。

你让我看到，兽人之心除了对死亡和毁灭的渴望外空无一物；不论眼前铺开怎样美好的未来，你们都只为与希望它成真的理性之人交战的刺激而将其舍弃。你让我看到，我努力超越的偏见从一开始就是对的。你让我看到，父亲唯一的错误，是做得还不够彻底——仅让一个大陆摆脱兽人，并不足以保障我们的安全。你们必须从整个埃亚尔被肃清；而这场战争无可避免，因为无论我们怎样努力保留和平的可能，你们都会不断把事态推向战争。然而……你也让我理解了你们为何用这种方式看待世人，把其他所有人都当作威胁自身存续的无理敌人——因为这正是我们对待你们的唯一正确方式。

我们不会再给你第二次机会。相反，我们会给你一直想要的唯一东西：一场战斗。传送门另一侧，联合王国的军队正等着你。我们过去或为仇敌，或只是勉强共居，如今却因怀有你们永远无法理解的和平与合作愿望而成为真正盟友。我们在开阔战场上列阵，准备展示联合起来的力量。埃尔瓦拉的永恒精灵准备法术，食人魔握紧棍棒；德斯镇与最后的希望城的半身人和人类已经忘却古老敌对，携手调制炼金炸弹、建造巨型傀儡，或带着弓与投石索各就各位；钢铁王座的矮人和夏特尔的自然精灵此前甚至算不上我们的正式盟友，如今也意识到你们的威胁不容忽视。阵线中列满能召唤无数野兽与树人的自然之力强者，以及#{italic}#绝不#{normal}#退让的勇猛战士。就连太阳堡垒也加入了我们，派出一支精锐增援阵线，并迅速训练士兵掌握他们多年来磨炼的魔法技艺——而你们这些无可救赎的野蛮人，正是他们的磨刀石。

我会手持长剑，等在这光荣联盟的最前线。我，公正之王托拉克，曾把你们从马基·埃亚尔肃清的图库纳之子；我，曾为让你们免于奴役或灭绝而战，如今迫不及待要完成父亲开创的事业。若我战死，图库纳的血脉也将随我断绝；为了彻底决定埃亚尔所有文明人民的命运，我愿意——不，我#{italic}#期待#{normal}#——冒这个风险。

你这卑劣的恶犬，想向我父亲的人民复仇？#{italic}#那就来拿。#{normal}#

（你承认，这确实颇具诱惑……但族人的绝对安全更为重要。何况，你完全相信联合王国会安排一队弓手和投石手守在门后，把每个穿过传送门的人逐一射杀。你摧毁了传送门，消除托拉克国王军队的威胁，也确保太阳骑士艾琳得不到任何增援。是时候利用刚获得的隐蔽优势，彻底解决太阳堡垒的部队了……）
```

## entry-03873
位置：tome-orcs.lua:3434；section：tome-orcs/data/lore/sunwall.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Lady Aeryn,

My apologies, but you're going to have to go back to King Tolak empty-handed - we still don't have any idea how the smugglers are getting through.  The best evidence we've got is some rumbling in the desert near the Dominion Port (which is still too heavily guarded for a direct attack before the Allied Kingdoms can grant us full assistance), suggesting geomantic tunnel formation, but that could just as easily be the few of Briagh's spawn that the Hero of Maj'Eyal didn't mop up.  Scrying spells aren't helping either - there's some sort of counter-scrying ward being applied, but it's so well-hidden that we can't tell where on the continent it's coming from or how many entities are being affected by it.  The only thing that seems certain is that they've got another farportal hacked together - the only one we know of is right in the middle of Gates of Morning, and I'd like to think that we're not so incompetent we wouldn't notice a steady stream of slavers and bootleggers strolling past 70% of us.  If they're actually using that one, then they're using the best invisibility spell we have ever seen.

...Haven't ever seen?  Whatever.

Anyway, my advice is to request permission to send a few Shining Inquisitors to King Tolak to assist in the investigations on his end.  However they're evading detection here in the East, they either can't use it in the West or simply let their guard down once they're back home, judging from the rising arrest rates - we can help the Allied Kingdoms hit the weak link of this chain, and have the Inquisitors keep an eye on things in Maj'Eyal while they're at it.  Not that I don't trust that King Tolak intends to honor his commitment to keep those foul Ziguranth from ever pulling off anything like the Sunset Massacre again, but...  well, if a farportal altar made it onto the black market under the Allied Kingdoms' watch, possibly courtesy of a mad alchemist who lived practically next door to the King, I don't have too much faith in their ability to drag a bunch of clandestine fanatics into the light, out from the cover of that supposedly-benign Menders group.  I'm sure they're trying their hardest; all I'm suggesting is that we do the same.
```
译文：
```text
艾琳女士：

抱歉，你只能空手回去见托拉克国王了——我们仍不知道走私者如何通过。现有最好证据是巨魔帝国港口附近沙漠传来震动（那里守卫仍太严密，在联合王国全面支援前无法正面进攻），似乎有人用地术开凿隧道；不过也可能只是马基·埃亚尔英雄未清剿干净的少数布莱亚后代在活动。探知法术也无济于事——某种反探知结界正发挥作用，却隐藏得极好，我们无法判断它来自大陆何处，也不知道影响了多少实体。唯一似乎可以确定的是，他们又拼凑出了一座远行传送门。我们知道的唯一一座就在晨曦之门正中央，而我愿意相信我们还没无能到让一队又一队奴隶贩子和私酒贩子从七成守军眼皮底下走过都察觉不到。若他们真在用那座门，那他们施展的就是我们有史以来见过的最佳隐形法术。

……从未见过？算了。

总之，我建议申请许可，派几名日光裁判官前往托拉克国王处，协助他们那边的调查。从逮捕人数不断上升来看，无论走私者在东方如何避开侦测，他们到了西方要么无法再用同样手段，要么只是回家后放松了警惕。我们可以帮助联合王国打击这条链上的薄弱环节，也让裁判官顺便留意马基·埃亚尔的动向。倒不是说我不相信托拉克国王会履行承诺，绝不让那些邪恶的伊格兰斯再制造日落大屠杀那样的惨剧，但……唉，在联合王国眼皮底下，远行传送门祭坛都流入了黑市，幕后还可能是一个几乎就住在国王隔壁的疯狂炼金术师；要说他们能把一群秘密狂热分子从那个貌似无害的“修复者”组织掩护下拖到阳光中，我实在信心不足。我相信他们已经竭尽全力；我只是建议我们也这么做。
```

## entry-03874
位置：tome-orcs.lua:3505；section：tome-orcs/data/lore/weissi.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Did you know the Sher'Tul had brothers?  Long before their creation, when the gods were still young and gleeful, Quekjora convinced them they could work together to bring life to Eyal. Perhaps they could have, were they more mature at the time...  Eager cooperation withered under exposure to personal tastes and creative differences, the friendships of our creators turned to animosity, and yet we were still made.
 
We had no overt flaws.  The gods were mercilessly vigilant, eager to use any imperfections as an excuse to berate their perpetrator and claim superiority, and thus we were only allowed to live when they were out of ammunition to use.  We seemed perfect, even to a deep inspection...
 
I doubt any of them deliberately cursed us - no one of them could've done something so powerful.  Subconscious touches, psychic leakage, and other such imperceptible forces added up over time to indicate one inescapable truth: we were not wanted.  We had been forged in a bitter compromise, one desired by nobody involved; their hatred, their neglect, their frustration is the foundation of everything we are, and we carry it deep within ourselves.  Perhaps such a creature naturally attracts the ire of the universe, of fate itself. 

Or maybe we just angered someone powerful enough to put a retroactive temporal curse on us, or it was Amakthel personally ensuring his pet project would have no equals. We may never be certain.  All we know is, something - be it probability, or the universe's combined will, or simply our own bad luck - will not tolerate our existence, nor that of anything like us.

```
译文：
```text
你知道夏·图尔人有兄弟吗？在他们被创造出来之前，当众神还青春年少又无忧无虑，奎克久拉说服大家来一起合作为埃亚尔带来生命。也许他们真的能够实现这样的合作，如果他们当时更为成熟的话……热忱的合作在个人品味和创意的差异面前衰退了，我们的创造者的友谊变成了敌意，然而我们还是被这样创造出来了。

我们的身上没有明显的缺陷。众神们无情地警惕着对方，热心地用造物身上任何的不完美之处来指责其创造者，以显示自己的优越，直到他们弹尽粮绝，我们才被创造了出来。我们看上去很完美，细细检查也如此，然而……

我们不认为众神中有人故意来诅咒我们————没人能做出如此威力无穷的举动。潜意识中的触动，灵能的泄漏，还有其他的无法察觉的力量日积月累，表明了一个无可辩驳的事实：我们是不被需要的存在。我们在一场苦涩的、无人真正想要的妥协中铸就；众神的憎恨，他们的忽略，他们的懊丧是我们存在的基石，我们在自身的存在中也一直传承下来。也许我们这种生物，命中注定天怒人怨，被命运所诅咒。

或者我们只是激怒了另一位强大的存在，给我们施加了一个有追溯能力的时空诅咒，或者是因为阿马克泰尔本人想让他的宠物工程无可比拟。我们可能永远都不能确定这件事的原因。我们知道的是，有一种东西————不管是概率，或是宇宙的集体意志，或者仅仅只是我们自己的厄运————永远不会容许我们，或与我们相似的任何事物存在。

```

## entry-03875
位置：tome-orcs.lua:3579；section：tome-orcs/data/lore/weissi.lua；source_tag：_t；args_order：None；special：None

原文：
```text
If you would indulge us...  Next to you is a tablet that was just carved by our machines, moments before you arrived.  If our curse holds, it will be completely illegible, but if it has been lifted, it will bear our name.  A blatant, distinct word that is an undeniable mark of our existence, a sign that no matter how it may have wanted to, the universe could not forget us.  Look to your right, and learn the name of those who have far more right to exist than you do, who have fought far harder for it, and will sink their hooks so deep into reality that it must either lift them up or be dragged into the depths with them.  Learn the name feared by existence itself!

#{italic}#(You look to your right, and see a tablet which has been broken into fragments.  The fragments are still arranged roughly in the right shape, and you can read a single word; another, larger fragment bears a sentence.)#{normal}#


```
译文：
```text
如果你还愿意继续听下去的话……在你身边，是一块石板，是在你过来时前刚刚由我们的机器雕刻完成的。如果我们的诅咒还在持续下去，上面的字将会是完全无法辨认的，而如果诅咒被解除，这上面会刻着我们的名字。那是一个显眼、独特的名字，是我们存在的无可否认的标志。一个表明，宇宙也忘不了我们。往你右边看，看看我们这个群体的名字，这一群体比你们远远更有权利存在，却不得不为了那权利比你们都努力地斗争，他们奋力将钩子扎入最深的现实，让现实不得不要么将他们连根拔起，要不被他们一道拖进深渊。看吧，这个被存在本身畏惧的名字！

#{italic}#（你往右看，看到一块破裂成碎片的石板。石板仍然按照正确的形状排列，你可以读到一个词；另一个大一些的碎片上有个句子。）#{normal}#


```

## entry-03876
位置：tome-orcs.lua:3634；section：tome-orcs/data/quests/amakthel.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The humans, elves, and halflings will not be able to hurt your people again.  By destroying the farportal and denying King Tolak's army its glorious battle, you have ensured the safety of your people from the Allied Kingdoms, and by storming the Gates of Morning you have eliminated the last bearers of the West's hateful aggression in Var'Eyal.
```
译文：
```text
无论是人类、精灵还是半身人，都再也无法伤害你的族人。你摧毁了远行传送门，使托拉克国王的军队失去了这场光荣的战斗，从而确保族人免受联合王国侵害。你攻下晨曦之门，也消灭了西方在瓦·埃亚尔施行可恨侵略的最后一批爪牙。
```

## entry-03877
位置：tome-orcs.lua:3636；section：tome-orcs/data/quests/amakthel.lua；source_tag：_t；args_order：None；special：None

原文：
```text
  The messages of the Lost City give you cause to remain ever vigilant for the threats they warned of, including their authors, and you wonder what your people will do now that their struggle to escape eradication, one that has defined them for their entire recorded history, has ceased to be a concern.
```
译文：
```text
  来自失落之城的消息让你充满警醒，无论是那些他们警告的恐怖威胁，还是他们本身。你想知道，当你的人民所极力摆脱的灭亡威胁：那个镌刻在你们整个历史中的威胁，现在已经不复存在的时候，你们的人民又将何去何从。
```

## entry-03878
位置：tome-orcs.lua:3659；section：tome-orcs/data/quests/destroy-sunwall.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The people of the sunwall have lingered on this land for too long and now they are spreading their control to all the mainland. This must not be allowed!
With the help of their newfound allies in the west they keep a permanent guard over the farportal. The portal must be permanently destroyed to prevent reinforcements.
The leader of the Sunwall, High Sun Paladin Aeryn must be punished for her crimes against the Prides.
```
译文：
```text
太阳堡垒的人已经盘踞在这片土地上太久，如今更把控制扩展到整个大陆。绝不能允许这种事发生！
在他们来自西方的新盟友的帮助下，他们永久守护着远行传送门。摧毁远行传送门，防止援军前来！
太阳堡垒的领袖，高阶太阳骑士艾琳，将会为她对部落犯下的恶行付出代价。
```

## entry-03879
位置：tome-orcs.lua:3721；section：tome-orcs/data/quests/kill-dominion.lua；source_tag：_t；args_order：None；special：None

原文：
```text
It would be a good idea for you to not be there anymore when the bomb explodes however.
```
译文：
```text
在炸弹爆炸前，你最好提前逃走。
```

## entry-03880
位置：tome-orcs.lua:3763；section：tome-orcs/data/quests/kruk-invasion.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You place the detonator, you have 220 turns to get out or be destroyed by the explosion.
Use your #{bold}##GOLD#Rod of Recall#LAST##{normal}#!
```
译文：
```text
你成功安装了炸弹，将于220回合后爆炸。你需要在爆炸前离开。
使用 #{bold}##GOLD#回归之杖#LAST##{normal}#！
```

## entry-03881
位置：tome-orcs.lua:3772；section：tome-orcs/data/quests/palace.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The time for revenge is at hand! The Tribe stands crippled under your assaults.
```
译文：
```text
复仇的时刻终于到了！气之部族在你的攻击下濒临瘫痪。
```

## entry-03882
位置：tome-orcs.lua:3813；section：tome-orcs/data/quests/ritch-hive.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Stralite Sand Shredder
```
译文：
```text
斯莱特掘沙者
```

## entry-03883
位置：tome-orcs.lua:3893；section：tome-orcs/data/quests/yeti-abduction.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Call a trained yeti to your side.
```
译文：
```text
召唤雪人来协助你。
```

## entry-03884
位置：tome-orcs.lua:3894；section：tome-orcs/data/quests/yeti-abduction.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Yetis left to call: %d
```
译文：
```text
剩余可召唤的雪人：%d
```

## entry-03885
位置：tome-orcs.lua:3930；section：tome-orcs/data/talents/celestial/cosmic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires out a bolt of cosmic energy in the target direction. The projectile continues until it hits a wall or the edge of the map, dealing %0.2f dark damage to enemies hit and restoring %d negative energy. The negative energy gained is reduced by 25%% per enemy hit, restoring a maximum of %d. Enemies hit will become aware of you.
```
译文：
```text
向目标方向射出一道宇宙能量。直到碰到墙或者到达地图边缘，对敌人造成 %0.2f 的暗影伤害并回复 %d 负能量。负能量回复量最大为 %d，每击中一个敌人将少回复 25%% 的负能量，被击中的敌人将注意到你。
```

## entry-03886
位置：tome-orcs.lua:3933；section：tome-orcs/data/talents/celestial/cosmic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire an orb of negative energy towards a spot within range %d.
		When the orb reaches its destination, it will teleport you to its location.
		The speed of the projectile (%d%%) increases with your movement speed
```
译文：
```text
在 %d 码内发射一个负能量球。
		当负能量球到达目的地时，会将你传送到其位置。
		其飞行速度 (%d%%) 受你的移动速度加成。
```

## entry-03887
位置：tome-orcs.lua:3939；section：tome-orcs/data/talents/celestial/cosmic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sends out a slow-moving spiral of cosmic energy towards a target location within range 8.
		As the cosmic energy moves, it pulls in targets adjacent to it, dealing %0.2f darkness damage and granting you 1 negative energy per hit.
```
译文：
```text
在 8 码内发出一个缓慢移动的螺旋宇宙能量。
		当它移动时，会把相邻的目标拉向它，造成 %0.2f 暗影伤害并每击中一次回复 1 点负能量。
```

## entry-03888
位置：tome-orcs.lua:3952；section：tome-orcs/data/talents/celestial/crepescula.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Twilit Echoes
```
译文：
```text
暮光回响
```

## entry-03889
位置：tome-orcs.lua:3953；section：tome-orcs/data/talents/celestial/crepescula.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target feels the echoes of all your light and dark damage for %d turns. 

Light damage slows the target by %0.2f%% per point of damage dealt for %d turns, up to a maximum of %d%% at %d damage.
Dark damage creates an effect at the tile for %d turns which deals %d%% of the damage dealt each turn. It will be refreshed as long as the target continues taking damage from it or another source while Twilit Echoes is active, dealing its remaining damage over the new duration as well as the new damage.
```
译文：
```text
目标会感受到你造成的所有光系和暗影伤害的回响，持续 %d 回合。

每造成 1 点光系伤害，目标便会减速 %0.2f%%，持续 %d 回合；减速上限为 %d%%，造成 %d 点伤害时达到上限。
暗影伤害会在目标所在格产生一个持续 %d 回合的效果，每回合造成该次伤害的 %d%%。在暮光回响生效期间，只要目标继续受到此效果或其他来源的伤害，该地块效果就会刷新；剩余伤害和新伤害会一并分摊到新的持续时间内。
```

## entry-03890
位置：tome-orcs.lua:3965；section：tome-orcs/data/talents/celestial/energies.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases your movement speed by %0.2f%% per percent of positive energy and your casting speed by %0.2f%% per percent of negative energy, up to a maximum of %0.2f%% at 80%%. Sustained energy still counts toward the maximum.
```
译文：
```text
每 1%% 的正能量增加 %0.2f%% 的移动速度，每 1%% 的负能量增加 %0.2f%% 施法速度，在 80%% 时达到最大值，为 %0.2f%%. 持续能量仍然算向最大值。
```

## entry-03891
位置：tome-orcs.lua:3967；section：tome-orcs/data/talents/celestial/energies.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whichever of your positive and negative energies is a higher percentage regenerates towards its max instead of its normal resting value (%d positive, %d negative). Your negative and positive regeneration/degeneration rates are increased to %0.2f.
```
译文：
```text
无论是你的正能量还是负能量都将用更高百分比的恢复替代正常的休息值 (%d 正能量，%d 负能量)。你的正能量和负能量恢复/ 消退速度增加至 %0.2f。
```

## entry-03892
位置：tome-orcs.lua:3977；section：tome-orcs/data/talents/celestial/reflection.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Create a distortion at the target tile, knocking back all projectiles and changing their direction to face away if possible.
```
译文：
```text
在目标所在地创造一个地块，击退所有的飞行物如果可能的话还会改变他们的方向。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Argoniel	艾格尼尔	T.PN.PERSON	society	entity name	existing	core	
Atmos Tribe	气之部族	T.PN.FACTION	society	faction name	preferred	dlc	Embers of Rage 阵营专名；统一为“气之部族”（叙事文本曾作“气之部落”），与气之部族 NPC/叙事一致
Berserker	狂战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Corruptor	腐化者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
DESTRUCTICUS	毁灭号	T.GAME.ENTITY	creatures	_t	preferred	dlc	Embers of Rage 武器“裂天者 毁灭号”的简称；欢呼与叙词统一为“毁灭号”，不写作“毁天灭地”
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Dreadfell	恐惧王座	T.PN.PLACE	places	nil	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Gates of Morning	晨曦之门	T.PN.PLACE	places	_t	existing	core	
Gerlyk	盖里克	T.PN.PERSON	society	_t	preferred	core	人类造物主专名；统一巅峰剧情、虚空任务及创世传说，不写作“加莱克”
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
High Sun Paladin Aeryn	太阳骑士艾琳	T.PN.PERSON	society	entity name	existing	core	
High Sun Paladin Aeryn	高阶太阳骑士艾琳	T.PN.PERSON	society	_t	preferred	core	太阳堡垒领袖的完整头衔；统一任务标题和叙事中的称呼，不省略“高阶”
High Sun Paladin Aeryn	高阶太阳骑士艾琳	T.PN.PERSON	society	entity name	preferred	core	太阳堡垒领袖实体名；与任务及对话中的完整头衔统一
High Sun Paladin Aeryn	高阶太阳骑士艾琳	T.PN.PERSON	society	logPlayer	preferred	core	太阳堡垒领袖在玩家日志中的完整头衔
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Kruk Pride	克鲁克部落	T.PN.FACTION	society	faction name	existing	dlc	Embers of Rage 阵营
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Negative energy	负能量	T.GAME.RESOURCE	combat	_t	preferred	core	星空法师/死亡赞歌职业资源；与 Positive energy 正能量区分
Norgos	诺尔格斯	T.PN.PERSON	society	entity name	preferred	core	自然精灵开场的守护巨熊；统一巢穴、任务、实体名及人物代词
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Oozemancer	软泥使	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Orc Pride	兽人部落	T.PN.FACTION	society	nil	existing	core	
Paradox	紊乱值	T.GAME.RESOURCE	resources	_t	existing	core	
Phase Door	相位之门	T.GAME.TALENT	talents	talent name	existing	core	
Positive energy	正能量	T.GAME.RESOURCE	combat	_t	preferred	core	太阳骑士/赞歌职业资源；与 Negative energy 负能量区分
Reaver	收割者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Rod of Recall	回归之杖	T.GAME.ENTITY	items	entity name	preferred	core	核心传送工具实体名；统一物品标题、任务、对话、成就与日志中的引用，不写作“召回之杖”或“回城之杖”
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Scourge from the West	西方天灾	T.PN.PERSON	society	_t	preferred	dlc	Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Stone Warden	岩石守卫	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Tannen	泰恩	T.PN.PERSON	society	entity name	preferred	core	最后的希望城法师与传送门研究者；统一实体名、任务说明和对话中的称呼
Tantalos	坦塔洛斯	T.PN.PERSON	society	entity name	preferred	dlc	气之部族首席议员；统一书信署名、叙事引用与实体名，不写作“坦塔罗斯”
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Trollmire	巨魔沼泽	T.PN.PLACE	places	_t	preferred	core	任务与地点叙述统一；troll 指巨魔，不是食人魔，与 narrative.tsv 的 trollmire→巨魔沼泽 一致；“Of trolls and damp caves”是任务标题，不作同名处理；2026-09-16 用户裁决，由 existing 升为 preferred
Twilit Echoes	暮光回响	T.GAME.TALENT	talents	talent name	preferred	dlc	Embers of Rage 黄昏系技能；光系伤害造成减速，暗影伤害生成可由后续伤害刷新的地块效果，统一重复运行时键及状态说明
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Wilder	野性系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Yeek	夺心魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Yeti	雪人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	兽人战役种族
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
book	书	T.GAME.ENTITY	items	entity type	existing	global	
brutality	残暴	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
cleansing	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key；同 cohort 的 cleanse 运行键亦采用“洁净”；不约束其他语境
cleansing 	洁净的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的前缀名称；保留 source 尾空格；不约束技能、伤害类型、日志或叙事中的 cleansing
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
derth	德斯镇	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
dominion port	巨魔帝国港口	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
exploratory farportal	探索用远行传送门	T.GAME.ENTITY	items	_t	preferred	core	夏·图尔堡垒用于前往随机探索区域的远行传送门；与普通 farportal 区分，统一设施、任务与警告文本中的引用
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
high peak	巅峰	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infinite dungeon	无尽地下城	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
iron throne	钢铁王座	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
kor'pul	卡·普尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lost city	失落之城	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
multi-hued	多彩	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体生成修饰语；与 multihued entity subtype 的既有“多彩”统一，不使用名词性“混晶石”
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
orc prides	兽人部落	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	与地点/阵营名称按 source_tag 区分
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
paradox	紊乱	T.GAME.TALENT	talents	talent type	preferred	core	时空技能类别名；资源数值在其他语境使用“紊乱值”
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
potion	药水	T.GAME.ENTITY	items	entity type	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shatur	夏特尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slaver	奴隶贩子	T.NARRATIVE.LORE	narrative	_t	preferred	core	鲜血之环语境中的奴隶贩子；与被奴役者 slave“奴隶”区分。entity name 标签下译文曾作“奴隶商”，裁决统一为“奴隶贩子”
slavers	奴隶贩子	T.NARRATIVE.LORE	narrative	_t	preferred	core	鲜血之环语境中的奴隶贩子复数；与被奴役者 slaves“奴隶”区分
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
superiority	优势	T.GAME.EFFECT	combat	effect subtype	preferred	core	superiority 系效果类别（Juggernaut 等）；talent type 语境保持“战术优化”；P0 审核确认
superiority	战术优化	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	superiority 技能树分类译名；与 effect subtype 的“优势”区分；P0 审核确认
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
trollmire	巨魔沼泽	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	与同类手札标题统一；troll 指巨魔，不是食人魔
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
var'eyal	瓦·埃亚尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wild infusion	野性纹身	T.GAME.ENTITY	items	entity name	preferred	core	物品实体名称；与 Wild infusion 技能名统一
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
yeti	雪人	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
yeti	雪人	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
