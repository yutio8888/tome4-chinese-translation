# batch-118：10 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

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

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Atmos Tribe	气之部族	T.PN.FACTION	society	faction name	preferred	dlc	Embers of Rage 阵营专名；统一为“气之部族”（叙事文本曾作“气之部落”），与气之部族 NPC/叙事一致
Brilliant Auto-loading Orc Expeller	精良的自动装填式兽人驱逐装置	T.GAME.ENTITY	items	entity name	existing	dlc	Embers of Rage 商品实体名；重复运行时键统一
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
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
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Steam Quarry	蒸汽采石场	T.PN.PLACE	places	entity name	preferred	dlc	Embers of Rage 地点，地热阀所在；与“蒸汽商场”区分
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Tantalos	坦塔洛斯	T.PN.PERSON	society	entity name	preferred	dlc	气之部族首席议员；统一书信署名、叙事引用与实体名，不写作“坦塔罗斯”
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
book	书	T.GAME.ENTITY	items	entity type	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
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
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
potion	药水	T.GAME.ENTITY	items	entity type	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steam quarry	蒸汽采石场	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
