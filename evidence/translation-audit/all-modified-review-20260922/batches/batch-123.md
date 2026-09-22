# batch-123：4 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

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

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Gates of Morning	晨曦之门	T.PN.PLACE	places	_t	existing	core	
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Norgos	诺尔格斯	T.PN.PERSON	society	entity name	preferred	core	自然精灵开场的守护巨熊；统一巢穴、任务、实体名及人物代词
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Oozemancer	软泥使	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Stone Warden	岩石守卫	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Wilder	野性系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
cleansing	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key；同 cohort 的 cleanse 运行键亦采用“洁净”；不约束其他语境
cleansing 	洁净的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的前缀名称；保留 source 尾空格；不约束技能、伤害类型、日志或叙事中的 cleansing
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
derth	德斯镇	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
iron throne	钢铁王座	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
shatur	夏特尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
slaver	奴隶贩子	T.NARRATIVE.LORE	narrative	_t	preferred	core	鲜血之环语境中的奴隶贩子；与被奴役者 slave“奴隶”区分。entity name 标签下译文曾作“奴隶商”，裁决统一为“奴隶贩子”
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
var'eyal	瓦·埃亚尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
