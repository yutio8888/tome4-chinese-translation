# batch-122：2 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

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

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Argoniel	艾格尼尔	T.PN.PERSON	society	entity name	existing	core	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Dreadfell	恐惧王座	T.PN.PLACE	places	nil	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Gates of Morning	晨曦之门	T.PN.PLACE	places	_t	existing	core	
Gerlyk	盖里克	T.PN.PERSON	society	_t	preferred	core	人类造物主专名；统一巅峰剧情、虚空任务及创世传说，不写作“加莱克”
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Norgos	诺尔格斯	T.PN.PERSON	society	entity name	preferred	core	自然精灵开场的守护巨熊；统一巢穴、任务、实体名及人物代词
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Orc Pride	兽人部落	T.PN.FACTION	society	nil	existing	core	
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Scourge from the West	西方天灾	T.PN.PERSON	society	_t	preferred	dlc	Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Yeek	夺心魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
high peak	巅峰	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infinite dungeon	无尽地下城	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
kor'pul	卡·普尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
orc prides	兽人部落	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	与地点/阵营名称按 source_tag 区分
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
var'eyal	瓦·埃亚尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
