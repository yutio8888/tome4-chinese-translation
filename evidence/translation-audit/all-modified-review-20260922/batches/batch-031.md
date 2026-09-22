# batch-031：10 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01205
位置：mod-tome.lua:13677；section：mod-tome/data/ingredients.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Try to get any knots out before returning. Wear gloves.
```
译文：
```text
在回来之前把打结在上面的其他蠕虫统统清理掉。戴上手套。
```

## entry-01206
位置：mod-tome.lua:13682；section：mod-tome/data/ingredients.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Looks much like any other rock, though this one was recently sentient and trying to murder you.
```
译文：
```text
它看起来和其他石头没什么两样，只不过这块不久前还具有意识，并且曾试图杀死你。
```

## entry-01207
位置：mod-tome.lua:13690；section：mod-tome/data/ingredients.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
wretchling eyeball
```
译文：
```text
小劣魔之眼
```

## entry-01208
位置：mod-tome.lua:13709；section：mod-tome/data/keybinds/tome.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Show character sheet (player)
```
译文：
```text
显示角色面板（玩家）
```

## entry-01209
位置：mod-tome.lua:13710；section：mod-tome/data/keybinds/tome.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Show character sheet (actor @ cursor)
```
译文：
```text
显示角色面板（光标位置的角色）
```

## entry-01210
位置：mod-tome.lua:13785；section：mod-tome/data/lore/age-allure.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#Hompalan's Log Entry 4#{normal}#
#{italic}#Age of Allure 4544#{normal}#

Just when I was getting somewhere the military decide to barge in and take over. Don't they realise what a serious scientific project this is? All they care about is the little stripes on their helmets. Some tell rumours of humans threatening to attack the facility, but I really care not for such trivial politics. Besides, what threat could those stupid lanklegs really be? I suppose I shall have to persevere though, and try to work around these insane security restrictions.


#{bold}#Hompalan's Log Entry 5#{normal}#
#{italic}#Age of Allure 4545#{normal}#

Well, I suppose this whole war thing wasn't just hot wind after all. Apparently there's lots of people dying outside. What a nuisance - I just want to get on with my work without my supplies being cut off. There is one upside though - human test subjects! We're going to get started on them in the coming months.
I must say I'll be glad to get rid of these disgusting yeeks. They disturb me somehow with their oversized heads. Why we ever decided to use these useless creatures as servants is beyond me... At least the human subjects will be able to talk, lacking though they be in true mental capacity.


#{bold}#Hompalan's Log Entry 6#{normal}#
#{italic}#Age of Allure 4546#{normal}#

Test subject A-C: Imploded during transition.
Test subject D: Exploded during transition.
Test subject E: Half transitioned, half remained. Partial success?
Test subject F: Imploded during transition.
Test subject G: Turned to goo during transition.
Test subject H-K: Imploded during transition.
Test subject L: Frozen during transition.
Test subject M: Survived first transition. Imploded 2 seconds after. Progress!
Test subject N: Survived first transition, but in coma. Died after 4 days.

We're really getting somewhere here... Just a shame humans are such messy creatures! Honestly, how much intestines do they need?! Will start on the next set of subjects early in the new year.

```
译文：
```text
#{bold}#红帕兰的日志记录四#{normal}#
#{italic}#厄流纪 4544年#{normal}#

正当我的研究刚有进展时，军方就闯进来接管了一切。他们难道没有意识到这是个严肃的科学项目吗？这些人满脑子想的就是头盔上那几道小杠杠。有传言说人类威胁要进攻这座设施，但我根本不在乎这种琐碎的政治。再说，那些愚蠢的长腿能有什么威胁？看来我还是只能坚持下去，想办法绕开这些荒唐的安保限制。


#{bold}#红帕兰的日志记录五#{normal}#
#{italic}#厄流纪 4545年#{normal}#

好吧……看来这场战争并不只是空话。外面显然死了很多人。真麻烦——我只想继续工作，不要断了我的补给。不过倒有一个好处——人类试验品！接下来几个月就要开始在他们身上测试了。
我必须说，能摆脱这些令人作呕的夺心魔真让我高兴。他们那大得过分的脑袋总让我感到不安。我们当初究竟为什么会决定让这些无用的生物当仆从……至少人类试验品能够说话，尽管他们并不具备真正的思考能力。


#{bold}#红帕兰的日志记录六#{normal}#
#{italic}#厄流纪 4546年#{normal}#

实验品 A-C：在传送过程中向内爆裂。
试验品 D：在传送过程中爆炸。
试验品 E：一半传送走了，一半留在原地。这算部分成功？
试验品 F：在传送过程中向内爆裂。
试验品 G：在传送过程中变成肉酱。
试验品 H-K：在传送过程中向内爆裂。
试验品 L：在传送过程中被冻结。
试验品 M：在第一次传送中存活，2秒后向内爆裂，总算是有点进展了。
试验品 N：在第一次传送中存活，但昏迷不醒，于4天后死亡。

我们的实验真的有进展了……只可惜人类真是肮脏的生物！说真的，他们到底需要多少肠子？！明年初就开始测试下一批试验品。

```

## entry-01211
位置：mod-tome.lua:13840；section：mod-tome/data/lore/age-allure.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#Hompalan's Log Entry 7#{normal}#
#{italic}#Age of Allure 4547#{normal}#

Test subject O: Imploded during transition.
Test subject P: Survived first transition, but turned mad - had to be put down.
Test subject Q: Survived first transition. Imploded on return transition.
Test subject R: Died during first transition.
Test subject S-T: Imploded on return transition.
Test subject U: Survived return transition. Muttered something about hearing a voice before jumping back into portal - imploded. What a nuisance!
Test subject V: Died on return transition.

Running out of letters soon. Also out of subjects for now. Will have to wait for the soldiers to fetch me more.


#{bold}#Hompalan's Log Entry 8#{normal}#
#{italic}#Age of Allure 4548#{normal}#

Test subject W: Shrunk during first transition, before exploding. (error in calibration?)
Test subject X: Returned from second transition missing head. How bizarre.
Test subject Y: Disappeared during transition.
Test subject Z: Survived both transitions. Remarkable!

Subject Z currently raving, but I believe this is due to stressful conditions, not a direct corrosion of mental faculties from the portal use. Will have to study further.

```
译文：
```text
#{bold}#红帕兰的日志记录七#{normal}#
#{italic}#厄流纪 4547年#{normal}#

试验品 O：在传送过程中向内爆裂。
试验品 P：在第一次传送中存活，但疯了，不得不被处死。
试验品 Q：在第一次传送中存活，在传送回来的过程中向内爆裂。
试验品 R：在第一次传送中死亡。
试验品 S-T：在返回传送过程中向内爆裂。
试验品 U：在返回传送中存活。他喃喃说了句似乎听见某个声音的话，便又跳进传送门——随后向内爆裂。真麻烦！
试验品 V：在传送回来的过程中死亡。

试验品编号的字母快用完了，眼下试验品也已耗尽。必须等待士兵们给我提供更多的人类。


#{bold}#红帕兰的日志记录八#{normal}#
#{italic}#厄流纪 4548年#{normal}#

试验品 W：在第一次传送中缩小，随后爆炸。（校准错误？）
试验品 X：在传送回来时头没了，真古怪。
试验品 Y：在传送过程中消失不见。
试验品 Z：在两次传送中都存活了下来。了不起！

试验品 Z 目前仍在胡言乱语，但我相信这是紧张环境所致，而非使用传送门直接侵蚀了他的心智。还需进一步研究。

```

## entry-01212
位置：mod-tome.lua:13887；section：mod-tome/data/lore/age-allure.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#Hompalan's Log Entry 9#{normal}#
#{italic}#Age of Allure 4549#{normal}#

Subject Z is still doing well. Have completed numerous further transitions with him. Is capable of intelligent dialogue at times, though his species is fairly limited in intellect. Seems to have little real clue as to what is going on, and is always asking what time it is. What a fool... I must conjecture that humans are far too tall to have blood pumped all the way to their brain. Still, I dare not risk sending any halflings through the portal yet, and what humans I have sent through since have all died.


#{bold}#Hompalan's Log Entry 10#{normal}#
#{italic}#Age of Allure 4550#{normal}#

Beginning to suspect subject Z has latent magical powers. Have seen him move much faster than I thought his species capable, and mend broken objects without any obvious means of repair. These are small things, but I believe the portals may be somehow enhancing a basic ability. Will need to test more. He still seems quite dumb though. Said his last journey took three days, when clearly it took but seconds. He began to eat ravenously afterwards. I suspect he is just greedy. I saw him staring for a long time at the farportal earlier, but I had my assistants pull him away before he did any damage.


#{bold}#Hompalan's Log Entry 11#{normal}#
#{italic}#Age of Allure 4551#{normal}#

Subject Z has vanished! This is terrible! It was not even during a portal transit. It looked like he simply stepped into his own shadow and disappeared. My research is ruined!! There will never be another subject like him!

The military are annoying me to no end. I told them to find me more test subjects immediately, but they gave some excuses about enemy patrols in the area. Do they think I care about such trivial things?! And now I hear them practising their fighting in the corridors. They are even grunting and screaming in fake battle noises like stupid children. Do they not realise what an important facility this is? Can they not understand how my genius is disturbed by---

```
译文：
```text
#{bold}#红帕兰的日志记录九#{normal}#
#{italic}#厄流纪 4549年#{normal}#

试验品 Z 状态依然良好。已经让他完成了许多次后续传送。他偶尔能进行有条理的对话，尽管他的种族智力颇为有限。他似乎根本不知道发生了什么，而且总在问现在是什么时候。真是个傻瓜……我猜，人类长得太高，血液根本泵不到他们的大脑。不过，我暂时仍不敢冒险把半身人送进传送门，而此后送进去的人类又全都死了。


#{bold}#红帕兰的日志记录十#{normal}#
#{italic}#厄流纪 4550年#{normal}#

我开始怀疑试验品 Z 拥有潜在的魔法力量。我曾看见他以远超我对其种族预期的速度移动，还在没有任何明显修理手段的情况下修好损坏的物品。这些都是小事，但我相信传送门可能以某种方式增强了他的基础能力。还需要更多测试。不过他依然看起来相当愚蠢。他说上一次旅程花了 3 天，而明明只过了几秒。此后他便狼吞虎咽地吃了起来。我怀疑他只是贪吃。之前我看见他盯着远行传送门看了很久，但在他造成破坏之前，我就让助手把他拉开了。


#{bold}#红帕兰的日志记录十一#{normal}#
#{italic}#厄流纪 4551年#{normal}#

试验品 Z 消失了！真糟糕！这甚至不是发生在传送门转移期间。他看起来只是一步跨入自己的影子，然后就消失了。我的研究毁了！！再也不会有像他一样的试验品了！

军方真是把我烦透了。我让他们立即给我找来更多试验品，他们却用附近有敌方巡逻队这种借口推脱。他们以为我会在乎这种琐事吗？！现在我又听见他们在走廊里练习战斗。他们甚至像蠢孩子一样哼哼哈哈，故意发出战斗时的吼叫声。他们难道不知道这座设施有多重要吗？他们难道不明白自己如何打扰了我这位天才的——

```

## entry-01213
位置：mod-tome.lua:13952；section：mod-tome/data/lore/age-allure.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Work in a hospital like this is more draining than I thought it'd be.  I thought I'd have no trouble with motivation, helping our wounded get back to health again, but seeing so many of them, and knowing there are some I cannot help...  it weighs heavily on my mind.  It would be difficult to go on, if I did not keep a few things in mind: 

One, that I am truly doing the best I can to minimize the world's suffering, both directly by healing, and indirectly by ensuring that the world will be united under the wise, thoughtful rule of the Conclave.  Ready access to regeneration infusions ensures that even the most dire of wounds can be healed in a matter of days, and the soldiers can return to the battlefield; furthermore, the Overseers have granted us access to their amnesia-inducing spells, allowing us to properly treat those who have been traumatized by the horrors of battle.  May the eyes of the Higher watch over this world for thousands of years to come.

Two, that the "side project" the Overseers have assigned me to is working out very well.  Those wounded who have consented to our trial treatments, consisting of a unique combination of experimental variations on heroism infusions and shielding runes, have experienced slightly increased physical strength and endurance, with no sign of the effects wearing off.  There is one mild side effect which has given me cause to worry, though I dare not speak of my misgivings to anyone else; some of those treated have needed to be disciplined for getting too "enthusiastic" in battle.  The Overseers have assured me that this is actually having a net positive effect on morale, and thus I can wait to cure these aggressive tendencies until the war is over.  In the meantime, I am proud of my work, and although it's nothing so glorious as the creation of the Higher race, it will be a tremendous boon to our society in the long term.

And three, that the war will soon be over, and with it we shall no longer have to bear the maiming of our proud soldiers and the impudence of the Nargol.  We have made impressive gains in territory in the last few days, thwarting numerous ambushes and keeping our momentum as we expand further into Nargol lands.  Granted, one cannot be sure of how much of what we're hearing has been "cleaned up" by the Overseers, but one recent statement from the Nargol leads me to believe it is the truth:

"This is your last chance to back down.  A great tragedy will ensue if you continue to push further, and do not accept our previously-stated terms of peaceful resolution.  Do not force us to do this."

After waging a war of trickery and deceit, those halflings think they can bluff us!  Once their military is broken, we can bring their citizens into our fold and enlighten them, and then the true healing can begin.
```
译文：
```text
在这样的医院工作，比我预想的更令人精疲力竭。我本以为，帮助伤员恢复健康定能让我始终充满动力；可看到他们有这么多，又知道有些人我无能为力……这令我心情沉重。若不是时刻记着几件事，我很难继续坚持。

第一，我确实在尽全力减少世间的痛苦：既直接治疗病痛，也间接保证世界将在孔克雷夫明智而深思熟虑的统治下归于一统。随时可用的再生纹身确保即便最严重的伤势也能在几天内治愈，让士兵重返战场；此外，长老会还授予我们使用致人失忆的法术，让我们能够妥善治疗那些被战场恐怖景象创伤的人。愿高等人类的眼睛在未来数千年间守望这个世界。

第二，长老会指派给我的那个“子计划”进展十分顺利。那些同意参加我们的试验性治疗——由英勇纹身与护盾符文的实验性变体独特组合而成——的伤者，在术后体力和耐力都有了轻微的提升，并且这一提升并不随时间消退。尽管如此，还是有一个轻微的副作用令我颇为担忧，虽然我不敢把我的疑虑告诉其他人：其中一部分志愿者已经由于在战斗中表现得过于“士气高涨”而受到了处分。长老会向我保证，这种攻击性其实整体上有助于提高部队士气，因此我可以等到战争结束后再治疗这些攻击倾向。在此期间，我为我的工作深感骄傲。虽然比起创造高等人类种族这实在只能算是微不足道的改进，然而长期而言这也将会给我们的社会带来巨大的福音。

第三，战争很快就会结束，我们将不必再忍受骄傲士兵们的残缺，也不必再忍受纳格尔的傲慢。最近几天，我们取得了令人瞩目的领土进展，粉碎了多次伏击，在继续深入纳格尔领土时仍保持着推进势头。当然，没人能确定我们听到的消息有多少经过长老会“润色”，但纳格尔最近的一份声明让我相信战报属实：

“这是你们退让的最后机会。如果你们继续向前推进，拒绝接受我们先前提出的和平解决条件，巨大的悲剧就会随之而来。不要逼我们这么做。”

这些半身人打了一场充满阴谋与欺骗的战争，如今竟以为能吓住我们！等他们的军队被击垮，我们就能将他们的公民纳入自己的怀抱、启蒙他们，届时真正的治愈就会开始。
```

## entry-01214
位置：mod-tome.lua:14196；section：mod-tome/data/lore/angolwen.lua；source_tag：_t；args_order：None；special：None

原文：
```text
It were some years now since twain of our brightest students left Angolwen, sullied by our veil of secrecy and our silent duty. It still lies heavy on mine heart to think of what they could accomplish within our private circle. I but hope that one day they whilst return, and they whilst understand the reasons behind our solemn mission.

But I must think of the future, for too many are the regrets of mine long past, and to hold their burdens overlong is to be crushed. I must think of ye, young acolytes, who start now in the learning of our lores. I must explain to ye our mission, our purpose, our justification, so that ye understand all what we do and why. In secrecy we operate, trying to heal the harms of our past, trying to build a better future. For our penance is great, and never should it be forgotten in all Eyal the terrors of the Spellblaze.

I should know well, for I were there. But a young mage was I, though not without promise. I knew of the Shaloren mages' experiments on the Sher'Tul ruins. Aye, and I were jealous of the powers they sought to unlock. No fear or caution had I in my arrogant youth, thinking only of opportunities and glory. Heed well that thought...

Two thousand six hundred cycles of the Sun have passed above my head, and yet still I cannot shake the memory of the day the sky turned to flame and the earth was torn to shreds. I felt the magic in the air, the sudden unleashing of arcane energies beyond anyone's control. I knew in an instant that the Shaloren had unlocked the power of the farportals, but the forces were far beyond their expectations. I saw within seconds the streams of blazing energy tear through the sky above our heads, and then rain down in crimson plumes of destruction. It was all I could to put a shield about myself, and the burns I suffered were terrible, such that scars remain to this day. No one about me survived. Still I remember mine sister Neira's shortened scream as she stood beside me, her skin flayed off by the terrible energies, her body consumed by a pyre of flames, her ashes strewn by a great tumult in the earth. Twenty-six centuries have passed and still I do wake to the sound of that scream...

Many were the loved ones I lost that day, and I were not alone. Countless perished across the lands, and countless more died in the chaos which followed. Then the Spellhunt began, and the people rose against the arrogance of the mages and began slaughtering us mercilessly. After the Spellblaze our abilities were in disarray, our mana channels sundered. We were nigh defenceless, and it took great effort to gather many of us together and found the hidden city of Angolwen. A great many mages were killed in the riots that followed, aye and many innocents too, for distrust was rife and the thirst for blood all-consuming. But alas, the suffering did not end there.

The effects of the Spellblaze can still be seen today, in tortured lands and blighted earths. In the Age of Dusk it were much worse. New diseases arose, plagues swept across all cities, civilisations brought to nothing. All our races came close to extinction, and an age of darkness came upon all learning and enlightenment. Feudal lords and bandit gangs fought amongst what little healthy lands were left, whilst the blights continued to ravage what free people remained. That was when I did begin our secret missions to repair the world, to make right the errors of our actions. In silent operation we visited the broken lands and used our powers to heal, not to destroy. Many centuries it took, but at last the aftereffects of the Spellblaze began to diminish, and the people began to rebuild.

Ah, how much hope was in me then. But foolish were I to think it could be so easy. The wounds of Eyal struck deeper than mere diseases on the surface. The poison went down much further, and the cracks tore through the very roots of our world. One dark and stormy day a great cataclysm swept forth from the east, and the land rose 500 leagues into the sky. We could do naught but gasp in horror as whole cities, whole races were swept into the sea. The continents were sheared apart and all of Eyal forever changed. It was a sight to humble even the greatest archmage.

Aye, and humility is what I teach to ye now. Know ye well that there are forces out there which dwarf ye into insignificance. Know as well that they have no glory, no pride, for they are forces of ultimate destruction which bring only terror and pain.

Our mission is to help the world. Our penance is to act in secret. Old wounds remain and new threats do arise, but all must be dealt with from behind our cloak of silence. The mistrust of our ilk still lies deep in people's minds, and there are even those who hate us with a violent passion. But the world is changing, and perhaps one day we shall be accepted again in society. Until then remember well this lesson of humility, and in the open world keep ye secret, and keep ye safe.
```
译文：
```text
我们最聪慧的两名学生离开安格利文已有数年，他们厌倦了我们隐秘的帷幕和无声的职责。想到他们若留在我们这秘密的圈子里能有何种成就，我心头依然沉重。我只希望他们终有一日归来，并理解我们为何肩负这项庄严的使命。

但我必须思考未来，我遥远的过去已有太多憾事，长期背负它们只会被压垮。我必须想到你们——这些刚开始学习我们知识的年轻学徒。我必须向你们解释我们的使命、目的与理由，让你们明白我们做的一切以及为何要做。我们在秘密中行动，试图治愈过去造成的伤害，试图建立更美好的未来。我们需要做出巨大赎罪，整个埃亚尔都永不应忘记魔法大爆炸的恐怖。

我对此无比了解，因为那时，身为一个年轻法师我就在现场。我听说了永恒精灵法师在夏·图尔遗迹上的实验。是的，我对他们将发掘出的力量感到无比的嫉妒。年少轻狂的我满脑子都是机遇和荣誉的诱惑，一点也不明白谨慎与小心的重要。看看吧，这样的想法带来了什么样的恶果……

两千六百次太阳轮回已从我头顶流过，可我仍无法摆脱那一天天空化为火海、大地被撕成碎片的记忆。我感受到空气中的魔力，感受到远超任何人控制的奥术能量猛然释放。我瞬间明白，永恒精灵已解开远行传送门的力量，但那股力量远超他们的预期。短短几秒间，我看见燃烧的能量洪流撕裂头顶的天空，继而化作绯红的毁灭烟柱倾泻而下。我只来得及给自己罩上护盾，却仍被严重烧伤，疤痕至今尚存。我身边无人生还。我仍记得姐姐尼拉站在我身旁时那声截然而止的尖叫：可怕的能量剥去她的皮肤，火堆般的烈焰吞没她的身体，她的灰烬被大地的剧烈震动抛散。二十六个世纪过去了，我仍会被那声尖叫惊醒……

那天我失去了许多所爱之人，而且绝不只有我。无数人死于各地，更有无数人死于随后的混乱。之后魔法狩猎开始，民众奋起反抗法师的傲慢，毫不留情地屠杀我们。魔法大爆炸后，我们的能力陷入紊乱，法力通道也被切断。我们几乎毫无防卫能力，历尽艰辛才聚集众多法师，建立隐藏城市安格利文。随后的暴乱中，许多法师被杀，也有许多无辜者死去；当时猜忌遍地，嗜血欲望吞噬了一切。但不幸的是，苦难并未到此结束。

魔法大爆炸的影响今日仍随处可见：土地扭曲，大地枯萎。黄昏纪时，情况还要糟得多。新疾病不断出现，瘟疫席卷各座城市，文明化为乌有。所有种族都接近灭绝，知识与启蒙堕入黑暗时代。封建领主和强盗团伙为剩下的少数健康土地争战，枯萎病却继续蹂躏尚存的自由人民。正是在那时，我开始秘密行动，修复世界，弥补我们行为的过错。我们默默访问破碎的土地，用力量治愈，而非毁灭。这耗费了数个世纪，但魔法大爆炸的后果终于开始减退，人们也开始重建。

啊，那时我心中充满希望。可我竟愚蠢地以为事情会如此简单。埃亚尔的伤口比表面的疾病深得多。毒素深入下方，裂缝撕开了我们世界的根基。一个黑暗的风暴日，一场大灾变从东方席卷而来，大地升至天空五百里格之高。整座城市、整个种族被卷入海中，我们只能惊恐地倒吸凉气。各片大陆被生生切开，整个埃亚尔从此永远改变。那番景象，足以令最伟大的大法师也心生谦卑。

是的，这就是为何我要让你学习身为法师的谦卑。让你了解在绝对的力量下你是多么的渺小。让你了解这力量无关荣耀与自豪，它终极的破坏力只会带来痛苦与恐惧。

我们的使命是帮助世界。我们的赎罪是在秘密中行动。旧伤仍在，新威胁又不断出现，但一切都必须在沉默的斗篷后处理。人们心中对我们同类的不信任依然根深蒂固，甚至有人狂热而暴力地憎恨我们。但世界正在改变，也许终有一日，我们会重新被社会接纳。在此之前，牢记这节谦卑之课；踏入外界时保守秘密，保护好自己。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Angolwen	安格利文	T.PN.PLACE	places	nil	preferred	core	维护者于 2026-08-25 裁定统一为“安格利文”；“安格列文”已被取代
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Dwarf	矮人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Yeek	夺心魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cracks	裂缝	T.GAME.ENTITY	places	entity subtype	preferred	dlc	地面裂缝的实体子类型；与 dug rubble“挖出的碎石”区分
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
dwarf	矮人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
torture	折磨	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
veil	猎杀	T.GAME.EFFECT	combat	effect subtype	preferred	core	仅用于 Stalking/Stalked 的内部效果分类；按猎杀机制语境处理，不作普通名词“面纱”
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
