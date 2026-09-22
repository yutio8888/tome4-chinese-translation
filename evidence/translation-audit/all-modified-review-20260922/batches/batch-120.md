# batch-120：4 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

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

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
DESTRUCTICUS	毁灭号	T.GAME.ENTITY	creatures	_t	preferred	dlc	Embers of Rage 武器“裂天者 毁灭号”的简称；欢呼与叙词统一为“毁灭号”，不写作“毁天灭地”
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Kruk Pride	克鲁克部落	T.PN.FACTION	society	faction name	existing	dlc	Embers of Rage 阵营
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Tantalos	坦塔洛斯	T.PN.PERSON	society	entity name	preferred	dlc	气之部族首席议员；统一书信署名、叙事引用与实体名，不写作“坦塔罗斯”
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Yeti	雪人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	兽人战役种族
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
brutality	残暴	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
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
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
yeti	雪人	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
yeti	雪人	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
```
