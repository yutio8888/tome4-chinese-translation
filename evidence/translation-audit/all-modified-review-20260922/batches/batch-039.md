# batch-039：4 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01226
位置：mod-tome.lua:15571；section：mod-tome/data/lore/fearscape.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You see a female human lying unconscious on a black altar, twisted sigils scored into her naked flesh.
Around her are several figures in dark robes.

As they notice you one calls out 'Intruder! Protect the seed of Kryl-Feijan!'
```
译文：
```text
你看见一名人类女子赤身裸体地昏倒在黑色祭坛上，扭曲的符印深深刻入她的肌肤。
她身旁站着数名黑袍人。

他们一发现你，其中一人便大喊：“入侵者！保护克里尔·费扬之种！”
```

## entry-01227
位置：mod-tome.lua:15732；section：mod-tome/data/lore/fun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#3. Unwanted Attention#{normal}#

Sadly, it is not only the peasantry and our "virtuous" archmage cousins that disapprove of our work. Though not entirely understood, necromancy is known to create "ripples" of a sort across the many dimensions, ripples that attract extra-planar attention. As a necromancer's power grows, so do said ripples, until eventually said necromancer finds all manner of demonic force and entity beating down their door, both mentally and physically.

Once again, opinions differ on this demonic interference. Necromancy is such a beautiful, divergent art, is it not? The Tren? method sees the necromancer's corruption by outside forces as a negative thing, and practitioners of said method often take measures to divert supernatural attention from themselves, creating talismans to act as spiritual "conductors" or living close to the communities that despise them, the life essences of the masses masking the necromancer's dark emanations. On the other hand, the Beinagrind method welcomes the cursed whisperings that come from the demonic realms, believing it to be the completion of their psyches. Only once their spirits have been "corrupted" (a term Beinagrind practitioners scoff at) do people realize their true ambitions, they claim. Why these "true ambitions" always seem to be the utter and complete destruction of all life in this world and the summoning of unthinkable atrocities from the outer dimensions is unexplored.

You may have noticed that no instruction has been given on how to deal with the attention of common folk. That is because a true necromancer requires none. They are vermin, fit only to be crushed.
```
译文：
```text
#{italic}#3. 不受欢迎的关注#{normal}#

遗憾的是，并非只有平民和我们自诩“高尚”的大法师同道反对我们的事业。虽然人们尚未完全理解其中原理，但已知死灵法术会在诸多位面之间激起某种“涟漪”，招来位面之外的关注。死灵法师的力量越强，涟漪也越强，最终形形色色的恶魔力量与实体都会找上门来，从精神和肉体两方面破门而入。

对于这种恶魔干涉，各家意见再次出现分歧。死灵法术正是如此美妙而多姿多彩的艺术，不是吗？崔恩流派认为，死灵法师被外来力量腐化绝非好事。该派修习者常设法把超自然力量的注意引向别处，例如制作护符充当精神“导体”，或居住在憎恶他们的社区附近，借芸芸众生的生命精华掩盖死灵法师散发的黑暗气息。另一方面，贝纳格雷德流派欣然接纳来自恶魔领域的诅咒低语，相信它们能使心智臻于完整。他们声称，唯有精神受到“腐化”（贝纳格雷德修习者对这个词嗤之以鼻），人们才会认清自己真正的野心。至于这些“真正的野心”为何总是彻底毁灭世间一切生命，并从外层位面召来难以想象的恐怖之物，至今无人探究。

你或许已经注意到，本书没有说明如何应付普通人的关注。真正的死灵法师根本不需要这种指导。那些人不过是害虫，只配被碾碎。
```

## entry-01228
位置：mod-tome.lua:15875；section：mod-tome/data/lore/fun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#An undead hunter's guide, by Aslabor Borys#{normal}#

So, apparently I'm a legend now. Hah, knock a vampire's head off with a greatmaul and suddenly you're up there with Toknor and Mirvenia apparently. More and more often these days I get novice adventurers coming up to me, asking me for advice when it comes to battling the undead. My first instinct was to tell them to get back home and become bakers or gardeners or something. If they need crib notes for combat they obviously aren't cut out for it.

But then I was thinking, these are good kids. Heck, I'd buy every man and woman in the world who's bumped off a ghoul a free drink if I could. If they want help when it comes to putting down necromancer slime and their chilling creations, I would be more than happy to oblige. Not much of a writer, but let's see. First...

#{bold}#1. Ghouls#{normal}#

Every once in a while, people come to me and say "Are all necromancers truly evil?" "Surely necromancy could be used for good!" "Isn't it wrong to discriminate against others simply because of the magicks they practice?" To these people, the first thing I usually say - shortly after giving them a black eye - is to take a look at a ghoul. Take a good, long look. Take in the diseased, putrescent flesh. Take in the oozing, exposed organs. Take in its features, slowly rotting to mulch. It used to be a person. It used to have a family, people who loved it. Now it's a walking corpse, its only desire being death and the mad, all-encompassing consumption of living flesh. Are all necromancers truly evil? A thousand times, yes.

Even this most basic of undead minions can strike terror into the unprepared. The multitude of diseases that a normal ghoul carries are contagious in a manner many adventurers do not truly appreciate until they see the sores and necrosis visibly spreading up their arm from where a ghoul bit them. Such maladies must be dealt with promptly: if bitten by a ghoul, immediately plunge the afflicted area in scalding hot water, then wrap it quickly in clean cloth lined with mugwort and quartz powder. The wound must remain dressed for three weeks, with new dressings applied every four days, and make sure to burn the old ones! Failing the above, a wild infusion also works splendidly.

    * * *


#{bold}#2. Skeletons#{normal}#

What guide to the undead would be complete without mentioning the humble skeleton? Despite these clattering and chittering bones of the deceased often looking so fragile that a stiff breeze could break them apart, in many ways they are more dangerous than their ghoul cousins.

With no masses of rotted and ruined flesh to reanimate, necromancers can commit themselves fully to bestowing some level of fighting skill on a reanimated skeleton, and since a fighter's weapons will often last as long as his bones will, skeletons are usually armed and sometimes even armoured. The potential skill of a skeleton doesn't stop at melee weapons either - fallen archers take up their bows once again, and although difficult by comparison, some necromancers can even grant dead mages their magic powers once again.

Some adventurers find themselves baffled when it comes to fighting skeletons. How do you destroy a foe who, by all rights, should be destroyed already? To these adventurers, I say take heart. The more broken and incomplete a body is, the more effort it takes to keep it reanimated. As most necromancers see skeletons as the lowest of low peons, you can expect a few good blows to easily dissipate the minimal effort their masters put into creating them.

    * * *


#{bold}#3. Wights#{normal}#

Wights are an odd duck amongst the undead, often not created by necromancers specifically, but instead rising of their own volition when the conditions are right. Wights are by no means individual souls, but often part of a gestalt; when a particular land has seen enough bloodshed - battlefields, forest, crypts and graveyards - wights can be seen to rise en masse, a near-physical representation of the battles and turmoil the land has faced. Sadly, it is for this reason that necromancers often facilitate the creation of wights regardless, for no other study or profession causes so much blood or death.

Those who have had encounters with wights often describe them as indistinct skeletal figures, wrapped in flowing cloaks that become faded and incorporeal at their edges, while strange lights dance where their eyes should remain. Survivors tell of a peculiar sense of exhaustion when in close proximity to them, as though merely being close to these figments of death causes one's life force to sputter and fade. Regardless of this and their ghostly appearance however, it has been recorded that steel and strength of arms is yet enough to destroy them, or at least to erase them for the time being. It's just a shame that such battles are likely to simply create more of them in the long run...

    * * *


#{bold}#4. Vampires#{normal}#

Vampires are so far removed from other varieties of undead it seems almost unreal. What grants them their longevity? How do they retain such great intelligence? Beyond their sallow complexion and drawn features, why do they not decay and decompose as their ghoulish siblings do? The study of vampiric nature is one long list of unanswered questions, each new study adding yet more to the ever-growing pile.

As said before, a vampire's greatest strength is its resemblance to a living man, both in mind and body. Thanks to this, vampires are known for residing comparatively close to normal towns and villages far more than other undead. Some have even been known to keep their lairs within these communities themselves! Despite their resemblance however, there are many telltale signs of vampirism: Unnaturally pale skin, long and distinctive fangs, an aversion to sunlight, and much more besides. In an effort to avoid close inspection, some vampires are known to masquerade as men of wealth, often cloistering themselves in remote locations to discourage prying eyes.

But perhaps the most astonishing thing regarding vampires is their propensity for alliance and familial relationships. No other undead being even approaches matching the incomprehensible tangle of clans, broods, families and bloodkin that vampires create for themselves. It is for this reason that vampires often end up becoming rulers of lesser undead themselves, commanding them as a normal necromancer would. So, in turn, treat them as you would a necromancer - with cold steel.

    * * *


#{bold}#5. Spirits#{normal}#

During my travels, I have noticed that some communities in the wild no longer bury their deceased as is the norm in larger settlements. Some folk burn the corpses of their fallen, committing their ashes to the earth instead. When asked why they perform this peculiar practice, I always receive the same answer: Necromancers. Fearful of their dead rising up to slay them at the whims of delusional, murderous filth, they believe that with the burning of the dead, their spirits are forever beyond the reach of a necromancer's bony fingers.

Alas, this is not true. While fire may burn away a man's physical being, no flame can touch his spirit. Unfortunately, necromancers can. Bereft of both body and freedom, many souls are driven mad in the employ of necromancers, ceaselessly drifting through windswept crypts, harrying any unfortunate wanderers they encounter with a multitude of curses and hexes. Worst of all are those spirits who embrace their newfound purpose, causing them to grow in power at a frightening rate. No other being in Maj'Eyal is so obviously abhorrent to existence itself as these "dreads"; it is almost as though creation itself wants these beings gone from her world. It is my hope that you, and many others, oblige her wish.

    * * *


#{bold}#6. Bone Giants#{normal}#

One of the most horrific, vomit-inducing expressions of the necromancer's so-called "art" is the bone giant. Not content with merely profaning the bodies of singular souls, some ambitious necromancers work to bind the bodies of countless skeletons together, creating hideous engines of destruction that can stand many times higher than the height of a normal man.

It is a deadly mistake to liken these abominations to the golems alchemists and archmages employ. Wilful and fey as they are, normal mages often only craft golems for utility and their own protection, while necromancers create bone giants for the sole purpose of dealing death, and the only limit to their destructive capability is the necromancer's twisted imagination. Ever fought a snow giant? Imagine one with six arms and fingers like blades, wrought of sharpened ribs. Imagine one with countless skulls lining every inch of its wretched body, all screaming for your blood to be spilt as it thrashes spinal columns like whips from its disfigured hands! After facing one of these grotesque amalgamations, you'll be begging to go back to the Daikara to pick on simple, frost-rimed sub-men.

    * * *


#{bold}#7. Liches#{normal}#

Hate made flesh. Evil made pure. Death incarnate. The culmination of a necromancer's work. Whatever you know liches as, I can tell you that they do not match the countless myths and legends that surround their terrible figures. They surpass them.

Once a powerful necromancer finally crosses the border between life and death, the abyssal power that they could only initially grasp in dribs and drabs becomes theirs to control totally. It is often said that unexpected quakes, crops failing, and the leaves simultaneously falling from the trees heralds the birth of a lich. Lords of the undead, liches can annihilate ghouls and skeletons, banish dreads with a glance, and reduce bone giants to powder within moments.

As to how to actually destroy one? Well, tell you what. If you manage to defeat one of these abominations, be a dear and write a guide for me, for I have absolutely, positively, no idea.

    * * *
```
译文：
```text
#{italic}#一名不死猎人的指南 作者：阿斯拉伯·波利斯#{normal}#

这么说，我如今也成传奇人物了。哈，不过是用大槌敲掉一个吸血鬼的脑袋，转眼就有人把我和图库纳、米雯尼雅相提并论。最近越来越多的新手冒险者跑来问我，该怎样对付不死生物。我的第一反应，是叫他们回家当面包师、园丁，随便做点别的。打架还得看小抄，显然就不是这块料。

不过转念一想，这些孩子都不坏。见到世上任何一个干掉过食尸鬼的男人或女人，我都乐意请上一杯。要是他们需要帮忙收拾死灵法师那帮渣滓和他们阴森森的造物，我当然愿意效劳。我不太会写东西，不过试试看吧。首先……

#{bold}#1、食尸鬼#{normal}#

时不时有人来问我：“所有死灵法师真的都邪恶吗？”“死灵法术难道不能用于善事？”“仅仅因为别人修习某种魔法就歧视他们，难道不是错的吗？”对这些人，我通常先赏一只乌眼青，然后叫他们好好看看食尸鬼。仔仔细细看个够：染病腐败的血肉，裸露在外、不断渗液的脏器，还有渐渐烂成泥浆的面孔。它从前也是个人，也曾有家庭，有爱它的人。如今却成了一具行尸走肉，唯一的欲望就是死亡，以及疯狂地吞噬一切活人的血肉。所有死灵法师真的都邪恶吗？千真万确，是。

即使是这种最基础的不死仆从，也足以让毫无准备的人胆寒。普通食尸鬼携带的多种疾病极易传染；许多冒险者直到亲眼看见溃疡与坏死从被咬处沿手臂蔓延，才真正明白危险。这类病症必须立刻处理：若被食尸鬼咬伤，马上将患处浸入滚烫的热水，再迅速用内衬艾蒿与石英粉的干净布料包好。伤口必须包扎三周，每四天更换一次敷料，而且务必烧掉旧敷料！做不到这些，用野性纹身也很有效。

    * * *


#{bold}#2、骷髅#{normal}#

要是不死族狩猎指南里都没有最常见的骷髅那还算个屁指南？虽然这些亡灵身上的白骨在走路时上下乱颤，搞得一副弱柳扶风的样子，但是从许多方面来说，它们都远比自己的食尸鬼表亲要危险多了。

因为骷髅身上通常不会有那么多累赘腐肉，死灵法师得以全身心的投入对骷髅战斗能力的授予，同时由于战士们生前所用的武器几乎和他们的骨头一样经久耐用，我们遇到的骷髅兵大多都是持有武器或是全副武装的。何况骷髅对我们的威胁并不仅仅是近身战：死去的弓箭手会再度拿起弓；虽然更为困难，有些死灵法师甚至能让死去的法师重获魔法力量。

不少冒险者在面对骷髅时都疑惑不解——如何摧毁一个早已死的不能再死的骷髅。对于这些冒险者，我只想说：鼓起勇气吧。骷髅的身躯越是遭到破坏残缺，死灵法师们驱动它们所要消耗的法力就越大。因为大多数的死灵法师都将骷髅视为最低等的奴隶，相信在你数个重击之后就能驱除死灵法师附着于其身上的微弱法力。

    * * *


#{bold}#3、尸妖#{normal}#

尸妖是不死生物中的异类，往往并非由死灵法师特意创造，而是在条件成熟时自行出现。尸妖绝不是单独的灵魂，而常是某种集合意识的一部分；某片土地经历了足够多的杀戮——无论战场、森林、地宫还是墓园——尸妖便会成群升起，几乎是这片土地所受战争与动荡的实体化身。遗憾的是，死灵法师仍常常促成尸妖诞生，因为没有别的学问或行当会制造如此多的鲜血与死亡。

与尸妖战斗过的人经常将其描述为：一具轮廓模糊的骷髅身形，裹着飘动的褪色长袍，袍角逐渐变淡、虚化，本该是眼睛的位置则跳动着诡异的光。幸存者们则述说只要靠近这种诡异的生物，仅仅是靠近这些死亡的化身，自己的生命力就会不住地衰减、消逝。

万幸的是，尸妖虽然看上去很像鬼魂，已经被证实它们还是能被武器和腕力所消灭，至少是暂时消除了它们的威胁。无奈的是，这种战斗长远来说只是变相的壮大了尸妖族群而已。

    * * *


#{bold}#4、吸血鬼#{normal}#

吸血鬼与其他种类的不死生物相去甚远，简直令人难以置信。是什么让他们如此长寿？而他们又是如何保留这样强大的智力？暂且不提他们萎黄的面色与消瘦的五官，他们为何不像食尸鬼同类一样腐烂分解？

关于吸血鬼本质的研究仍有许多未解之谜，而每个新课题似乎也只是增加了更多的谜题而已。

如前所述，吸血鬼最大的优势，是身心都与活人极其相似。因此，比起其他不死生物，吸血鬼往往住得离普通城镇和村庄近得多；有些甚至直接把巢穴设在这些社区之中！

然而再怎么像人，吸血鬼仍有许多显眼征兆：不自然的苍白皮肤、细长醒目的尖牙、畏惧阳光，等等。为了躲避近距离盘查，有些吸血鬼会伪装成富人，常年幽居偏远之地，不让好奇者靠近。

但也许吸血鬼最让人称奇的地方，是他们纷繁复杂的系谱和族群。他们自发组建部族、血盟、家族等不可思议的集群，这是其他不死族无法望其项背的。借助团体的力量，吸血鬼常常成为弱小不死族的主宰者，像一名普通的死灵法师一样操作指挥着自己的奴隶。所以，请你也像对付死灵法师一样对付他们——用钢剑刺穿他们的喉咙。

    * * *


#{bold}#5、幽灵#{normal}#

在我的旅程中，我注意到荒野中的一些社区已不再像较大的聚居地通常那样埋葬死者。取而代之的是，他们会将死者的尸体焚化并将骨灰撒落在大地之上。当我询问他们这奇怪行为背后的意义时，几乎都是同样的原因：死灵法师。

他们害怕死者会在妄想而嗜杀的渣滓驱使下爬起来杀害自己，于是相信焚烧尸体能让灵魂永远逃出死灵法师枯骨般手指的掌握。

可惜事实并非如此。火焰能烧毁人的肉身，却没有任何火焰能够触及灵魂。

更为不幸的是，死灵法师却可以触到。同时失去身体和自由的痛苦，让许多灵魂在死灵法师的奴役下疯狂了，它们不停地飘荡在风蚀的地宫之中，用种种诅咒与妖法折磨着任何不幸与之遭遇的游荡者。

最糟糕的是那些接受了自己新使命的灵魂，它们的力量会以惊人的速度增长。在马基·埃亚尔，没有任何生物像这些“噩灵”一样如此明显地为存在本身所憎恶——仿佛造物本身也想将它们从这个世界抹去。希望你和更多人能遂她所愿。

    * * *


#{bold}#6、骸骨巨人#{normal}#

死灵法师所谓的“艺术”中最恐怖、最令人作呕的表现之一，就是骸骨巨人。有些野心勃勃的死灵法师不满足于只亵渎一具遗骸，便把无数骷髅的骨架缚在一起，造出比常人高出数倍的丑恶毁灭机器。

将骸骨巨人与法师或炼金术士的傀儡一视同仁是大错特错的。尽管这些法师老头们偏执又古怪，但通常法师们制造傀儡的目的只是用来当苦力或自卫。而死灵法师创造骸骨巨人的唯一目就是制造死亡，对一只骸骨巨人能力的唯一限制竟然只是其创造者扭曲的想象力。你有没有与一向被视为力量象征的雪巨人战斗过？那就想象一下长着六只胳膊的骸骨巨人吧——手指由削尖的肋骨制成，如刀刃般锋利；再想象无数头颅悬挂在这具骸骨巨人每一寸肢体上，它们都尖叫着怒吼着，因为你的每滴鲜血都令其饥渴无比。它用畸形的双手挥舞脊柱作鞭！你若有幸见识了这扭曲的混合体，恐怕会巴不得回到岱卡拉，去欺负那些头脑简单、浑身覆霜的低等类人生物。

    * * *


#{bold}#7、巫妖#{normal}#

他的身体由憎恨组成，他是纯粹的邪恶、死亡的化身，死灵法师的无上杰作。我能明确的告诉你巫妖并不是你想象中的那样，关于它的无数传奇和神话也的确有所失实。

他的恐怖远超于此。

当一名强大的死灵法师最终超越了生死界限后，他从前只能零星借用的地狱力量一下子完全服从于他。传说中，大地莫名的震颤、谷物奇怪的枯萎、树叶的同时凋零都预示着一只巫妖的诞生。作为至高的不死之主，巫妖能瞬间泯灭无数食尸鬼与骷髅，眨眼间将噩灵驱散，片刻就使骸骨巨人灰飞烟灭。

至于消灭巫妖的确切方法嘛……这么说吧，如果你成功的摧毁了这样的怪物，亲爱的请你一定要为我写一篇指南。因为我真的，完全，没有办法。

    * * *
```

## entry-01229
位置：mod-tome.lua:16042；section：mod-tome/data/lore/high-peak.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#On touching the still-wet diamond, you find yourself experiencing memories that are not your own, memories that slowly seep into your mind with increasing detail.  You cannot tell if the initial haze covering them is a side-effect of the absorption process, or if it's from being dazed and waking from unconsciousness in these memories...#{normal}#

#FIREBRICK#Pain#LAST#.  Everywhere, but where is worst...

Abdomen.  Broken ribs?  Breathe in--  #FIREBRICK#yes they're broken#LAST#.  Shallow breaths.  What happ--  right.  Damned orcs.  Didn't expect them on this continent, much less in a Sher'Tul ruin.  Didn't even expect a Sher'Tul ruin...  Carrying Ziguranth weapons, preventing healing magic from working.  So now we've got #{italic}#two#{normal}# bands of past-their-prime savages working together to burn down civilization.  Lovely.

[...]

Elandar, leaning over me, can't hug me because of my ribcage.  Says I should be dead.  That he found what he thinks is the fabled Blood of Life, and poured it down my throat and into my wounds.  That I'm healing, but...  if he was wrong, we can't go back to them.  Back to #{italic}#her#{normal}# - not after last time.  I can't let them take me from Elandar, not after all he's done for me, no matter what they might find if they analyze what's left in that bottle.

The pain is fading - little by little, ribs mending minute by minute, I can breathe slightly deeper before #FIREBRICK#hitting#LAST# that sudden wall of #FIREBRICK#agony#LAST#.  It feels...  healthy.  Powerful, even.  Whatever my love may have found, his gift is definitely capable of nourishing living creatures...  but there are other feelings too.  Feelings of being trapped.  Lost.  Alone.  Homesick for a home I'm already lying in.

[...]

I have my theories, unsettling as they are, as to what's coming over me - what I suspect to have invisibly replaced my subconscious already, what I constantly feel my conscious thoughts drifting towards if I'm not focusing, why that ability to hold conscious attention on anything else seems to be slipping more every minute.  Committing suicide or sending myself to an Angolwen asylum (if they were that merciful) are not options - egotistical as this sounds, I know the happiness I bring to Elandar's tragic life is the only thing that keeps him going.  I believe I can use this bond and the #FIREBRICK#painfully unnatural#LAST# urges that come with it...  productively, without breaking my love's heart or leaving a worse world behind.  I will be happy, Elandar will be happy, and #FIREBRICK#he#LAST# will be happy.
```
译文：
```text
#{italic}#触碰这颗仍然湿润的钻石时，你发现自己正在亲历一段不属于你的记忆。记忆逐渐渗入脑海，细节愈发清晰。你分不清笼罩其上的最初朦胧究竟是吸收过程的副作用，还是因为自己在这些记忆中昏昏沉沉、刚从失去意识中醒来……#{normal}#

#FIREBRICK#痛#LAST#。无处不在，可哪里最痛……

腹部。肋骨断了？吸气——#FIREBRICK#果然断了#LAST#。浅浅呼吸。发生了什——对了。该死的兽人。没想到他们会出现在这片大陆，更没想到会出现在一处夏·图尔遗迹。就连这里会有夏·图尔遗迹都没想到……他们带着伊格兰斯的武器，让治疗魔法无法生效。于是现在有#{italic}#两伙#{normal}#早已过气的野蛮人联手焚毁文明。真好。

[……]

埃兰达俯身看着我；因为我的胸廓，他没法拥抱我。他说我本该已经死了。他找到了一样他认为是传说中生命之血的东西，把它灌进我的喉咙、倒进我的伤口。他说我正在愈合，可是……如果他猜错了，我们就不能回到他们那里。不能回到#{italic}#她#{normal}#身边——上次那件事之后不行。无论他们分析瓶中剩余物时会发现什么，我都不能让他们把我从埃兰达身边夺走，尤其是在他为我做了这一切之后。

疼痛正在一点点消退，肋骨分分秒秒愈合。我现在可以把气吸得稍深一些，才会#FIREBRICK#撞上#LAST#那堵突如其来的#FIREBRICK#剧痛#LAST#之墙。感觉……很健康，甚至充满力量。不管我的爱人找到了什么，他的馈赠无疑能够滋养生灵……但我也感到了别的东西。受困。迷失。孤独。躺在家中，却仍在思乡。

[……]

我对侵袭我的东西已有猜测，尽管这些猜测令人不安——我怀疑它已经悄无声息地取代了我的潜意识；只要不集中精神，我就不断感觉有意识的思绪向它飘去；而我将注意力维持在其他任何事物上的能力，仿佛每分钟都在进一步衰退。自杀，或把自己送进安格利文的疯人院（如果他们肯这么仁慈），都不是选项——听来或许自负，但我知道，我给埃兰达悲惨人生带来的幸福，是支撑他活下去的唯一事物。我相信，我能善加利用这份联结，以及随之而来的那些#FIREBRICK#反常得令人痛苦#LAST#的冲动……既不让爱人心碎，也不留下一个更加糟糕的世界。我会幸福，埃兰达会幸福，#FIREBRICK#他#LAST#也会幸福。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Angolwen	安格利文	T.PN.PLACE	places	nil	preferred	core	维护者于 2026-08-25 裁定统一为“安格利文”；“安格列文”已被取代
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Lich	巫妖	T.PN.RACE	creatures	birth descriptor name	existing	core	亡灵种族/形态
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
corruption	堕落	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
gestalt	格式塔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
gestalt	格式塔	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
ghost	幽灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
necrosis	坏死	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	死灵法师操控生命衰败、负生命与死亡边界的技能类型；区别于 necromancy（死灵法术）
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
vermin	害虫	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wild infusion	野性纹身	T.GAME.ENTITY	items	entity name	preferred	core	物品实体名称；与 Wild infusion 技能名统一
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
