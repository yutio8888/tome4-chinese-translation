# batch-048：20 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01325
位置：mod-tome.lua:18914；section：mod-tome/data/lore/orc-prides.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#Chapter Four: Conqueror of West and East#{normal}#

#{italic}#"Our strength must come through our pride, and our pride must rise from our strength. Many are our powers and abilities, and we are unified in our pride of them. Be proud in our great race and revel in the glories we can achieve together."
- Sayings of Garkul the Devourer#{normal}#

For many years the great conquest could not be held back. Garkul marched across the lands, insufferable of any resistance. The Eldoral were broken, and they fled to their halfling cousins the Nargols in the south. The humans were split into many kingdoms, and Garkul began to pick them off one by one, leaving just a few isolated in the west and south. The Thaloren hid in their dark forests, penned in by the mighty orcish armies. The Shaloren tried to fight, and with their great magics they created grave opposition to the orcish troops, but gradually they were beaten back and forced to retreat to their capital in the south-west. The dwarves viciously defended their halls in the east, and Garkul could not penetrate their cities of stone, but he laid plans in place to take them through caves below.

All the centre of Maj'Eyal was under Garkul's dominion - from the northern wastes to the southern lakes; from the Daikara Mountains to the western ocean. Orc patrols covered every valley and every field, and any enemies found were eradicated. Garkul's support was utterly unwavering, as every orc took new pride in their amazing achievements under his leadership.

But victory was not complete, as many centres of power and resistance still remained, and the Nargol were still a grave threat from the south. Garkul was careful not to overreach, not to spread his forces too thin before victory was assured. He knew he must bide his time and build up his forces to their greatest possible strength.

Then beneath the dwarven city of Reknor our scouts discovered an amazing thing - a Sher'Tul farportal. The blood mages studied it, and after some time they succeeded in activating it, and discovered a new land. It was the lost East, sundered from Maj'Eyal after the great cataclysm. Garkul saw here a great opportunity, and he instructed many thousands of young warriors and mages to be sent over to the east. There they formed training grounds where the military could train and practise to master their techniques before returning to join the wars in the west. Garkul named them the Prides, for he said here was were the strength of our race would lie, and here was what we would be most proud of.

But while Garkul was busy establishing the Prides the Nargol king was planning a strategy of defence. He knew that the orcish armies would come for his kingdom soon, and he drew on the powers of his greatest strategists to prepare a force that could not be overcome. He summoned the mightiest alchemists from all the lands and together they laid plans for a creation that could not be beaten: the giant golem Atamathon.

When Garkul next returned from the east he heard from his spies of great operations afoot in the Nargol kingdom, and he knew that he must face down the halflings. He did not know that it would be his last battle.
```
译文：
```text
#{bold}#第四章：东西方的征服者#{normal}#

#{italic}#"我们的力量必须源于自豪，而我们的自豪必须崛起于力量。我们的力量与本领多不胜数，而为之自豪让我们团结一心。为我们伟大的种族感到自豪吧，尽情沉醉于我们携手铸就的辉煌之中。"
- 吞噬者加库尔语录#{normal}#

多年来，伟大的征伐势不可挡。加库尔率军踏遍大地，绝不容忍任何抵抗。艾德瑞尔人被击溃，逃往南方投奔他们的半身人同族纳格尔人。人类分裂成许多王国，加库尔开始将他们逐一歼灭，只在西方和南方留下少数孤立的残部。自然精灵躲入黑暗的森林之中，被强大的兽人大军团团困住。永恒精灵试图抵抗，凭借强大的魔法给兽人部队造成了沉重的阻击，但依然节节败退，被迫退守西南方的首都。矮人在东方死守大厅，加库尔无法攻破他们的石城，但他已布下计划，准备从下方的洞穴杀入。

整个马基·埃亚尔的中部尽在加库尔的掌控之下——从北方荒原到南方湖泊，从岱卡拉山脉到西方海洋。兽人巡逻队遍布每座山谷与田野，发现的任何敌人都被彻底铲除。加库尔得到了绝对坚定不移的拥戴，因为在加库尔的领导下取得的辉煌成就，让每一名兽人都萌生了全新的自豪。

然而胜利尚未彻底完成，因为仍有许多权力与抵抗中心尚存，而南方的纳格尔人依然是一大严重威胁。加库尔行事谨慎，在确保胜利之前绝不盲目冒进、分散兵力。他明白自己必须等待时机，将麾下大军积蓄至最强战力。

就在此时，在矮人城市瑞库纳的深处，我们的斥候发现了一件令人惊叹之物——一座夏·图尔远行传送门。血法师们对此展开研究，一段时间后成功将其激活，并发现了一片全新的陆地。那是失落的远东，在大灾变之后与马基·埃亚尔隔绝分离。加库尔在此看到了巨大的契机，下令将数以千计的年轻战士与法师送往远东。他们在那里建立了训练营地，军队可以在返回西方参战之前在那里操练以精通战技。加库尔将其命名为各个兽人部落（Prides），因为他说我族的力量将寄托于此，而这也将是我们最引以为傲之所在。

然而当加库尔忙于建立各个部落之时，纳格尔国王正筹划着防御策略。他知道兽人大军很快就会攻打自己的王国，便动用了最顶尖谋士的力量，准备打造一支无法战胜的武装。他召集了全大陆最强大的炼金术士，一同谋划制造一件不可战胜的造物：巨型傀儡阿塔玛森。

当加库尔下一次从远东返回时，他从斥候口中获悉了纳格尔王国正在紧锣密鼓展开的大动作，他知道自己必须正面迎击半身人。但他未曾料到，这将是他此生最后一战。
```

## entry-01326
位置：mod-tome.lua:19079；section：mod-tome/data/lore/orc-prides.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Sher'Tul ruin matches description from high command. Investigation begun, but slow. Looks like it crashed into the ground long ago - hard to access many areas. Target item has been described by command as a staff. Do not know why a staff so important. Surely the ultimate weapon should be a sword or axe, like that wielded by the great Garkul?

Have heard many rumours against high command lately - strange rumours, indeed. Perhaps by completing this mission I shall get closer to them so that I might seek the truth...

...

Curses and banes! Some bastard blaze-born THIEF has raided the ruins! And a halfling no less, a curr-damned halfling! I am pyred with rage!

He got in during dusk somehow, crawling through a tunnel too narrow for my workers to reach. He grabbed a staff from the ruins and snuck out past my orcs! The dirty, treacherous sneak has run away, and my career with him! I have sent scouts to track him, but he is proving elusive. But I will not let him escape! This is unforgiveable!

...

We've followed the tracks of the wretch. It seems as if he met up with a dwarf and a human near a town called Derth, and they travelled south-east from there. Following the three of them was much easier than the sneak alone, but we still must take care to remain hidden. Our orders from high command strictly forbid showing ourselves, and we must avoid battle as much as possible. I have a trained team of archers and fighters with me that know how to stay hidden in the woods.

The thief and his cursed allies have entered an old ruined tower called Dreadfell. It an ancient place, known to be filled with undead in its dungeons. If we break in we're bound to cause a stir, and so close to the big human town east of here... I am not sure how to proceed, and have sent a message to command requesting instructions. For now we wait in the woods, keeping an eye on the entrance for any change. If anyone comes out from the tower with that staff they will face my wrath!

...

Word is finally back from command - hold position and wait for the staff to emerge. If it doesn't happen soon then they will send their own agents in time.

In time! Bah! This will be my ruin if it comes to that. If there is any appearance of the staff I must snatch it and get back East as soon as possible...
```
译文：
```text
夏·图尔废墟与最高统帅部的描述完全一致。调查已经展开，但进展缓慢。看起来它在很久以前就坠毁到了地面上——许多区域都难以进入。统帅部将目标物品描述为一根法杖。不知道为何一根法杖会如此重要。最强的终极兵器难道不该是剑或战斧吗，就像伟大的加库尔所挥舞的那样？

最近听到了许多针对最高统帅部的流言——确实是些古怪的流言。或许通过完成这次任务，我能更接近他们，从而探寻真相……

……


该死！诅咒降临！不知哪个天杀的烈焰杂种盗贼洗劫了废墟！而且竟然是个半身人，一条该死的半身人杂种狗！我真是怒火中烧！

不知怎的，他趁着黄昏潜入了进去，爬过了一条连我的劳工都进不去的狭窄地道。他从废墟里夺走了一根法杖，竟然从我的兽人身边偷偷溜了出去！这个肮脏阴险的潜行者逃之夭夭了，我的前程也随之搭了进去！我已派斥候追踪他，但这厮极其狡猾。但我决不能让他逃脱！这绝对不可饶恕！

……


我们循着那个无赖的踪迹一路追踪。看来他在一个叫德斯镇的地方与一名矮人和一名人类会合，随后一同向东南进发。跟踪他们三个人比跟踪单独一个潜行者容易得多，但我们仍必须格外谨慎以保持隐蔽。最高统帅部的指令严禁我们暴露行踪，且必须尽可能避免战斗。我随身带领着一支训练有素的弓箭手与战士小队，他们懂得如何在林中隐匿。

那个盗贼和他该死的同党已经进入了一座名为恐惧王座的古老废弃高塔。那是一处古老的地方，地牢中素以塞满不死亡灵而著称。如果我们强行闯入必将引起骚动，况且此处离东面的人类大城镇又是如此之近……我拿不准该如何行事，已向统帅部发信请示指令。眼下我们潜伏在林中，密切注视着入口处的动静。若是有人带着那根法杖从塔里出来，定要承受我的滔天怒火！

……

统帅部终于传回了回信——坚守阵地，等待法杖现身。若是近期内仍未出现，他们届时会派出自己的密探。

届时！呸！真到了那个地步我就彻底完了。一旦那根法杖露面，我必须一把抢下它，以最快的速度返回远东……
```

## entry-01327
位置：mod-tome.lua:19139；section：mod-tome/data/lore/rhaloren.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The Scintillating Caverns must be protected. Our great leader has ordered it so, and his word is more binding than any law. Our numbers are few, and we must move in secrecy, but a quiet watch will be made on the caverns. Any who are seen to interfere in them must be lured here to our place of strength, and brought before me for inquisition.

More have joined our cause. Their eyes have been opened to the injustice our people have suffered, blamed by the other races for the Spellblaze and its effects. They are sick of the cowardice of the Council, who sit in silence as we are scorned and hated across the world. But most of all they are inspired by our great leader, and the powers he has gained from studying the Spellblaze. He alone realizes our full potential, he alone can see in our hearts what we are truly capable of. He has blessed me, rescued me from a tortured life and touched me with his power. Only he can lead our people! With his mastery the world will see our strength and recognise us as a true force to be reckoned with.

Trust in his power, for he shall bring us all to glory.

-- The Inquisitor
```
译文：
```text
闪光洞穴必须受到保护。伟大的领袖已经下令，他的话比任何法律都更不容违逆。我们人数不多，行动必须隐秘，但仍要暗中监视洞穴。凡被发现干涉其中事务的人，都必须诱到我们这处据点，再带到我面前接受审问。

又有更多人投身我们的事业。他们终于看清了我族遭受的不公：其他种族把魔法大爆炸及其影响都归罪于我们。他们受够了长老会的怯懦——当我们在世界各地遭到蔑视与憎恨时，那群人只会默不作声。但最令他们振奋的，还是我们伟大的领袖，以及他研究魔法大爆炸所得的力量。唯有他洞悉我族全部潜能，唯有他能看透我们内心真正拥有的力量。他赐福于我，将我从备受折磨的人生中拯救出来，又以自己的力量触碰了我。唯有他能领导我们的人民！在他的掌控下，世界将见证我们的力量，承认我们是一股不可轻视的势力。

信赖他的力量吧，他必将带领我们所有人走向荣耀。

-- 审判者
```

## entry-01328
位置：mod-tome.lua:19211；section：mod-tome/data/lore/sandworm.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I have stared in the mouths of crimson wyrms
And felt the claws of drakes so sleek
But through deserts dry and sandy storms
There is something else I seek

In the trail of giant worms I walk
Through tunnels of sand below
Of arcane tools let there be no talk
It's on the wyrmic path I go!
```
译文：
```text
我曾凝视赤红巨龙的巨口深处
也曾领教矫健幼龙利爪
可穿过干旱荒漠与沙暴
我所追寻的另有其物

我循着巨型沙龙的踪迹
穿行在地下沙土隧道
休要再提那些奥术器具
我走的是龙战士之道！
```

## entry-01329
位置：mod-tome.lua:19276；section：mod-tome/data/lore/scintillating-caves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I have been given permission to explore the scintillating caves to the east. Normally they are sealed off, but having a father on the council has its uses, even if he is normally a dumb buffoon...

These caves are the site of where the Spellblaze began. An ancient Sher'Tul farportal lay buried here, and our ancestors tapped into that power to their destruction. Many of the greatest Shaloren mages stood here, and when the energies beyond comprehension erupted they were all annihilated instantly. It was a terrible loss to our people - such knowledge and power lost forever!

Now the ancient ruins have become overgrown by crystals. Reports say that they grow each year. Could they be alive..?

I must admit that stepping into the starting place of the Spellblaze fills me with immense trepidation. This was where the great destruction began, that tore through our world, wiping out cities, tearing the world apart. And yet look at the beauty here!

```
译文：
```text
我获准探索东面的闪光洞穴。那里通常被严密封锁，不过有个身居长老会的父亲确实很有用——哪怕他平日只是个愚蠢的小丑……

魔法大爆炸正是从这些洞穴开始的。一座夏·图尔时代遗留的远行传送门深埋于此，我们的祖先抽取其中的力量，最终招致自身毁灭。许多最伟大的永恒精灵法师都曾站在这里；超乎理解的能量失控爆发时，他们顷刻间尽数湮灭。这是我族惨痛的损失——那般学识与力量从此永远消逝！

如今，水晶已经爬满了古老废墟。据报告，它们每年都在生长。它们会不会是活的……？

我必须承认，踏入魔法大爆炸的起点，令我心中充满强烈的不安。席卷世界的大毁灭就是从这里开始的：城市被抹去，整个世界遭到撕裂。可是看看这里，多么美丽！

```

## entry-01330
位置：mod-tome.lua:19334；section：mod-tome/data/lore/scintillating-caves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#10th Mirth, Year 122 of the Age of Ascendancy#{normal}#
The council has seen fit to allow me to investigate the scintillating caverns after that Rhaloren madman started raving on the streets about how someone had "befouled" them... I do not see any such befoulment, but neither do I see the moving crystals this place was rumoured to have. There are oddly misplaced crystal shards, which seem to have sheared off of something larger, but hardly anything spectacular.

#{italic}#2nd Summertide, Year 122 of the Age of Ascendancy#{normal}#
It's strange, really.. from the fragments I've been able to find, they seem to adhere to the ethereal geometry of magics - the red fragments seem to be pieces of fire magic from their geometry; the blue adheres to water, etc... there also seem to be pieces of deformed crystal, as though some terrible power warped whatever colour some of these crystals used to be into something they were never intended to be - is this the "befoulment" the madman raved about?

#{italic}#3rd Summertide, Year 122 of the Age of Ascendancy#{normal}#
Well... that was certainly unexpected. There may be some truth to the rumours that these crystals can move about, or at least that they have some will of their own - I was just about to finish my investigation of the caves, when in the very last part of the cave I hadn't yet explored, I saw what appeared to be two giant... legs, growing from the cavern. I was immediately overcome by feelings of fear and malice, and not my own - that crystal sent them to me, that I was unwelcome here, that it was not yet finished. I dare not tell the council of my cowardice, so I shall... invent a more fitting report in a much safer place. If some wayward adventurer finds these notes, it is my surmise that whomever destroyed the original crystals left such a strong impression of strength and will that the rudimentary intelligence governing them decided the form of its destroyer was stronger than the original, crystalline shapes.
```
译文：
```text
#{italic}#卓越纪122年狂欢月10日#{normal}#
那个罗兰精灵疯子走上街头大喊大叫，声称有人“玷污”了闪光洞穴，长老会这才认为应该准许我前来调查……我没看出这里有任何所谓的玷污，但也没有见到传闻中会移动的水晶。只有一些位置古怪的水晶碎片，像是从某个更大的东西上断裂下来的，实在称不上惊人。

#{italic}#卓越纪122年炎华2日#{normal}#
说来确实奇怪……从我找到的碎片判断，它们似乎都遵循魔法那无形的几何结构：以形态来看，红色碎片似乎是火焰魔法的一部分，蓝色则对应水，诸如此类……此外还有一些畸变的水晶碎片，仿佛某种可怕力量把这些水晶原有的颜色与元素属性扭成了绝不应有的形态——这就是那个疯子叫嚷的“玷污”吗？

#{italic}#卓越纪122年炎华3日#{normal}#
好吧……这可真是出乎意料。水晶能够移动的传闻或许确有几分真实，至少它们似乎拥有自己的意志——我正要结束洞穴调查，却在最后一处尚未探索的角落里，看见两条巨大的……腿，仿佛正从洞穴中生长出来。恐惧与恶意顿时淹没了我，可那不是我的情绪——是水晶把它们送进我心里，告诉我这里不欢迎我，也告诉我它的形态尚未完成。我不敢向长老会坦白自己的怯懦，所以还是……到安全得多的地方，编一份更体面的报告吧。若有哪位四处游荡的冒险者发现这些笔记，我的推测是：摧毁原有水晶的某个存在，以其力量与意志留下了无比深刻的印象，于是支配水晶的原始意识认定，毁灭者的形态比原本的水晶形态更加强大。
```

## entry-01331
位置：mod-tome.lua:19358；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
which you do not understand: #{italic}#'Sho ch'zun Eyal mor donuth, ik ranaheli donoth trun ze.'#{normal}#
```
译文：
```text
不明意义的文字：#{italic}#“Sho ch'zun Eyal mor donuth, ik ranaheli donoth trun ze.”#{normal}#
```

## entry-01332
位置：mod-tome.lua:19359；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#'In the beginning the world was dark, and the petty gods fought over their broken lands.'#{normal}#
```
译文：
```text
#{italic}#“世界之初一片黑暗，伪神们为支离破碎的土地争斗不休。”#{normal}#
```

## entry-01333
位置：mod-tome.lua:19365；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#'But AMAKTHEL came, and his might surpassed all else, and the petty gods fled before his glory. And he made the Sun from his breath and held it above the world and said, "All that this light touches shall be mine, and this light shall touch all the world.'#{normal}#
```
译文：
```text
#{italic}#但阿马克泰尔来了，他的勇武震慑了众人，伪神们慑服于他的荣耀。他深呼吸后把太阳高举到了世界之上，说：“阳光所至，即我所至，这光芒将照亮全世界。”#{normal}#
```

## entry-01334
位置：mod-tome.lua:19370；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
which you do not understand: #{italic}#'Ik AMAKTHEL cosio SHER'TUL, ik baladath peris furko masa bren doth benna zi, ik blod is "Fen makel ath goru domus ik denz tro ala fron."'#{normal}#
```
译文：
```text
不明意义的文字：#{italic}#“Ik AMAKTHEL cosio SHER'TUL, ik baladath peris furko masa bren doth benna zi, ik blod is "Fen makel ath goru domus ik denz tro ala fron."”#{normal}#
```

## entry-01335
位置：mod-tome.lua:19371；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#'And AMAKTHEL made the SHER'TUL, and gave unto us the powers to achieve all that we set our will to, and said to us "Go forth to where the light touches and take all for your own."'#{normal}#
```
译文：
```text
#{italic}#并且阿马克泰尔制造了夏·图尔，给予我们完成自我意志的力量，他对我们说：“走向光所照及之处，为自己取得一切。”#{normal}#
```

## entry-01336
位置：mod-tome.lua:19377；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#'We conquered the world, and built for ourselves towering cities of crystal and fortresses that travelled the skies. But some were not content...'#{normal}#
```
译文：
```text
#{italic}#'我们征服了世界，为自己建造了高耸的水晶之城和遨游天际的堡垒，但有些人还不满足……'#{normal}#
```

## entry-01337
位置：mod-tome.lua:19379；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This mural shows nine Sher'Tul standing side by side, each holding aloft a dark weapon. Your eyes are drawn to a runed staff held by the red-robed figure in the centre. It seems familiar somehow...
There is some text beneath 
```
译文：
```text
这幅壁画显示了九个夏·图尔人肩并肩站着，每人手里都高举着一件黑色武器。你的注意力集中在画面中间——被红袍者举起的符文法杖上。它看起来很眼熟……
下面有一行文字
```

## entry-01338
位置：mod-tome.lua:19385；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You see images of epic battles, with Sher'Tul warriors fighting and slaying god-like figures over ten times their size.
There is some text underneath 
```
译文：
```text
你在这幅壁画上看到一幕幕史诗般的战斗——夏·图尔的战士们正与十倍于自身的神明般的存在厮杀，并将其斩灭。
下面有一行文字
```

## entry-01339
位置：mod-tome.lua:19388；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
which you do not understand: #{italic}#'Ranaheli meth dondruil ik duzin, ik leisif konru as neremin. Eyal matath bre sun. Ach unu rana soriton...'#{normal}#
```
译文：
```text
不明意义的文字：#{italic}#'Ranaheli meth dondruil ik duzin, ik leisif konru as neremin. Eyal matath bre sun. Ach unu rana soriton……'#{normal}#
```

## entry-01340
位置：mod-tome.lua:19395；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#'The almighty AMAKTHEL was assaulted on his golden throne, and though many died before his feet, he was finally felled.'#{normal}#
```
译文：
```text
#{italic}#'全能的阿马克泰尔在他的黄金王座上遭到了围攻，尽管无数人死在了他的脚下，他最终还是陨落了。'#{normal}#
```

## entry-01341
位置：mod-tome.lua:19402；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This final mural has been ruined, with deep scores and scratches etched across its surface. All you can see of the original appears to be flames.
```
译文：
```text
最后的这块壁画损坏得很严重，表面刻满了深深的刻痕和划痕。你所能辨认出的原始图案似乎只有火焰。
```

## entry-01342
位置：mod-tome.lua:19405；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
a living Sher'Tul?!
```
译文：
```text
活着的夏·图尔人？！
```

## entry-01343
位置：mod-tome.lua:19406；section：mod-tome/data/lore/shertul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You somehow got teleported to an other Sher'Tul Fortress, in a very alien location. There you saw a living Sher'Tul.
```
译文：
```text
你不知怎么地被传送到了另一座夏·图尔要塞，位于一个非常陌生的地方。在那里，你看到了一位活着的夏·图尔人。
```

## entry-01344
位置：mod-tome.lua:19454；section：mod-tome/data/lore/slazish.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#Touching the conch makes it emit a sound. As you put it to your ear you hear a deep voice emanating from within:#{normal}#

"Waverider Tiamel reporting. Immediate perimeter is secure, though I have sent some members to scout the surrounding areas. I will feel better when we have mapped the land and are ready to sustain a larger team. Still, we should be perfectly safe as long as the landdwellers do not know of our presence. And even if they dare come here the magics of Zoisla will put their puny star worship to shame.

"I fear that some of the team are not taking our mission seriously. Do they not know the responsibility the Saviour has laid on us? We are his arms and tails in this far land, and it is our duty to protect the farportal which will help bring us to greater strengths. We are his first line of attack against the blood relatives of those who doomed our race so long ago. And with our efforts we shall push forward our race to new boundaries, laying the path for the bright future our great Saviour has planned for us. Long live Slasul! Long live the legend of the Devourer!"
```
译文：
```text
#{italic}#触摸这只海螺可以使它发出声音。当你将它放于耳边时，你听到了一阵低沉的声音从里面传出来：#{normal}#

"踏浪者塔米尔报告。据点周边已确保安全，不过我已派出几名队员侦察附近地带。等我们绘制好这片陆地的地图，并具备维持一支更大规模队伍的条件，我才会更加安心。只要陆地居民不知道我们的存在，我们应该就绝对安全。即便他们胆敢来到这里，佐西拉的魔法也会让他们那微不足道的星辰崇拜相形见绌。

"我担心队里有些人没有严肃对待我们的使命。难道他们不知道救世主赋予我们的责任吗？在这片遥远的土地上，我们就是他的手臂和尾巴；我们有责任守护那座远行传送门，它将为我们带来更强大的兵力。我们是他进攻那些很久以前毁掉我们种族之人血亲的先锋。凭借我们的努力，我们将带领种族开拓新的疆界，为伟大救世主替我们筹划的光明未来铺平道路。萨拉苏尔万岁！吞噬者的传说万岁！"
```

## 相关术语快照
```tsv
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Dreadfell	恐惧王座	T.PN.PLACE	places	nil	existing	core	
Dwarf	矮人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Scintillating Caves	闪光洞穴	T.PN.PLACE	places	_t	preferred	core	核心地点名；与手札分类及正文保持一致
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
derth	德斯镇	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
dwarf	矮人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
petty gods	伪神	T.NARRATIVE.LORE	narrative	_t	preferred	core	阿马克泰尔叙事中的贬称，与普通“众神”区分
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
rhaloren	罗兰精灵	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
scintillating caves	闪光洞穴	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	与地点名 Scintillating Caves 统一
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
torture	折磨	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
trance	入定	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	灵能系技能类型；指专注的入定状态，不是幻想
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
```
