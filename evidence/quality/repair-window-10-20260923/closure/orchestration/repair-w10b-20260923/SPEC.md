# 修复窗口10（重跑 w10b）：256批5条确认问题

本任务取代 repair-w10-20260923（STOP_VERIFIED，max_cycles 用尽未收敛）。原任务经 REVIEW(0)/FINAL(1)/RE_REVIEW(2)/FINAL(3) 四轮，其余4条自 FINAL(1) 起均 OK，长篇传说 eb0868d54c 每轮暴露新的忠实度缺陷，FINAL(3) 仅余一字主语错误（被我和→被我们和）。用户2026-09-23裁决按 w9b 先例重跑：唯一EXECUTOR逐字应用 .ai/task/repair-w10-20260923/FINAL-TARGETS.json 的5个最终 target（含该一字修复），再按 REVIEW(0)/full→FINAL_REVIEW(1)/full 独立复审；不再开任何修复轮，任一 confirmed 一级 finding 即交回用户。证据目录为 evidence/quality/repair-window-10-20260923/w10b/。

Paseo MCP / schema5 translation_contextual_v2 implement；基线5f817c4bf9b83f1d95a14494489c109e8e14a56a。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的5个target及evidence/quality/repair-window-10-20260923/w10b/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/TAB保持基线；LF除eb0868d54c须与原文一致（14个）外保持基线。

5条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 若失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰5个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核257。

范围约束：Plate of the Blackened Mind 描述整句忠实（deep black、absorbs all light that touches it、dark power、primal, yet aware 均须体现，不添加“邪恶”），物品名不改；魔法大爆炸区域效果只改警告句为确定语气“反射传送魔法”，前半句抗性数值与“区域效果：”前缀不动；时空特工入职信只修四处：a few decades（几十年）、fair game（可随意下手/不受约束的时段）、cheat at a few lotteries（在几次彩票上作弊）、quite literally the best roast-yeti restaurant（字面意义上最好的烤雪人餐厅），其余段落不动；刀刃风暴构造体 short_info 补主语“构造体”并改为“所有相邻敌人”；碾压擒抱解除提示改为挣脱“碾压擒抱”（现行效果名）。排除全部advisory、3条pending（Blunt Thrust、If I Should Die Before I Wake、Crystal Shard）及其他已有blocked/repair。

## eaacc62b76fcf99259afd5a9503a5d781d019aabbd5a574b060dd0ab83d4372b

section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: This deep black armor absorbs all light that touches it. A dark power sleeps within, primal, yet aware. When you touch the plate, you feel dark thoughts creeping into your mind.

target: 这件黑色的胸甲吸收了附近的所有光线。你能感受到其中沉睡着一股邪恶的力量。当你触摸它时，你感到黑暗的思想在不断的涌现在你的脑海。

确认依据：world-artifacts.lua:5135 Plate of the Blackened Mind 描述：primal, yet aware 被省略并另加原文没有的“邪恶的”；absorbs all light that touches it 被译成“吸收了附近的所有光线”，deep black 被弱化。完整性缺陷，整句有界修复。
与 surface 键同一缺陷的独立语境复核：world-artifacts.lua:5135 Plate of the Blackened Mind，primal, yet aware 被删、dark 改“邪恶”、absorbs all light that touches it 误作“吸收附近的所有光线”。确认整句修复。

## eafab19df4d889cb91ad909c639f97ff4190bd602bf5e7dbf40e08a8781f293a

section: mod-tome/data/timed_effects/other.lua
source_tag: _t

source: Zone-wide effect: The power of the Spellblaze still burns here. -10% resistance to fire, arcane and blight damage, but +10% cold resistance. WARNING: The powerful magic here reflects teleportation magic!

target: 区域效果：魔法大爆炸的火焰仍在燃烧，-10% 火焰、枯萎、奥术抗性，+10% 寒冷抗性。警告：强大的魔法能量可能干扰传送法术！

确认依据：timed_effects/other.lua:3333–3342 ZONE_AURA_SPELLBLAZE：原文为确定语气 reflects teleportation magic（反射传送魔法），译文“可能干扰传送法术”既把 reflects 弱化为“干扰”又添加原文没有的“可能”。activate 仅改抗性、未实现传送逻辑，源码无法支持更弱或更强的说法，故以原文为准；独立语境复核同向。忠实度缺陷，有界修复警告句。
与 surface 键同向：other.lua:3336 reflects teleportation magic 被弱化为“可能干扰传送法术”；activate 不实现传送逻辑，以原文为准。确认修复警告句。

## eb0868d54cceb1fe91ec45de453b482ca64cb324c275e44b48ac5a8bf812cdc1

section: mod-tome/data/lore/misc.lua
source_tag: _t

source: Congratulations, sir and/or madam. Whether by invitation, discovering it on your own, or simply being enough of a thorn in our side to recruit rather than dispose of, you have gained the secrets of chronomancy. The ultimate power of time - the ability to reset and try again if you fail, the ability to save time by seeing the results of investigations before they happen. Though our powers are bound to post-Spellblaze Eyal, they are those of nigh-omnipotence with enough patience.

But trust me - "enough patience" is one nasty limiting reagent. You're going to be running out of that fast when you've spent the last week trying to dismantle an Age of Dusk-era house-of-cards system of causally interdependent tyrannies without causing dwarven extinction, and a plague just broke out right when you had things almost perfect, for the sixth time--

Look. The point is, there's a reason the person who writes the invitations and the mission statements isn't someone out in the field - and you're lucky enough to be working for someone who understands that you need more flexibility than idealism allows. Our squad knows that to stay sane, we have to know when "time flows forward at a rate of one second per second" isn't the only rule we have to break. That it's generally okay to skip the trial and just deal with a temporally hazardous jackass as you see fit, if you've foreseen a guilty verdict - as long as your investigations are solid when you actually conduct them (and you do have to do the work once in a while, or you'll only be capable of seeing yourself procrastinating). And if you just need to not be watched, you should know that there are a few decades in the Age of Dusk we and a few other squads recognize as "fair game" - whatever experiments you've wondered about or horrors you want to inflict, just keep it to the time period of infinite forgotten evils and it doesn't hurt anything in the grand scheme. Trust me, we've checked - nothing in that time period matters unless you've got another Spellblaze to set off.

But most importantly, you should know: Zemekkys is even lazier than I am, but he has status to maintain. If you continually violate his will, there will come a point at which you will be informed that you have been caught and should stop resisting. Accept whatever fate he doles out for you. If you do not stop, there will come a point where he will be forced to make an example of you so severe that the entire cosmos will notice your non-existence. Obviously we can't be sure how many of us he's done this to (if any) or how it works, but we're pretty sure that the result looks like something starting with a W.

Everyone here wants the same thing - keep spacetime stable, have fun with your powers, cheat at a few lotteries - but we've got cover to maintain and, in theory, an actual job to do if something ever cracks that Sher'Tul shield or the Greigu find a way to bypass a portal-filter. Scratch backs when yours gets scratched, don't make so much noise that the system comes crashing down on your head, and you'll enjoy your stay in eternity.

Welcome to Point Zero, agent. Enclosed are timespace coordinates to what is, quite literally, the best roast-yeti restaurant that could possibly exist - I'll have the squad meet you there and then. Thank me later.

[i]-Galsamae[/i]

PS: You might encounter a... benefactor of sorts in your travels. You'll know it when you see it, ham-fistedly yanking its puppets back from the brink of death; if you see it for yourself, we regret to inform you that you've taken a one-way trip off prime Timeline-E4-RL territory for a doomed offshoot unless "he" feels like weaving you back in - and it tends to only do that to people who narrowly avert its engineered apocalypses through incredible power or luck. If you have been chosen by its schemes, play along and you might get brought back from the temporal graveyard that is the Timeline-E4-EXPADV subnetwork. We do not know what it is - a runaway creation of our own, a competing culture's weapon, or something far above ourselves - but if it has hostile intent, it has already won. So far it's been... mostly cooperative. Just make a point not to remind it that we're its competition.

target: 女士们先生们，恭喜你。无论是你受到了时空的邀请，是你自己发现了这一切的秘密，还是作为我们曾经的眼中钉，觉得比起对付还是招揽你更好，总之，你已经获得了时空魔法的奥秘。我们掌握有关时间的终极力量——能够在你失败时不断重试，能够通过预知结果来节约时间，甚至在调查发生前就看到结果。尽管我们的能力被限制在于魔法大爆炸后的埃亚尔，只要你有足够的耐心，我们将可以无所不知，无所不能。

不过，相信我——“足够的耐心”已经是足够令人讨厌的限制了。如果你曾经花费整整一周的时间，试图拆解黄昏纪暴君你方唱罢我登场的政治游戏，还不能让矮人一族因此灭绝；结果就在一切眼看近乎完美的时候，一场瘟疫偏偏爆发了，毁掉你满盘的计划——而且这已经是第六次了——很快你也会丧失耐心的。

看。这就是问题的关键。那些任务说明和邀请之所以不是由一线人员撰写的，是有原因的——你也有同样的幸运，我们知道在你的工作中需要的“灵活性”远比理想主义更重要。我们的小队知道要保持理智，我们也知道“每过一秒就有一秒钟的时间流过”也只是我们要打破的众多规律之一。如果你能够预见到一个有罪判决，在时空中不经审判处理掉一个潜在的罪犯也不是什么大事——只要你的调查可以被证明是确凿可信的（而且总有一天你要亲自做这件事，否则你只能看到自己不停拖延）而且，如果你只是想要一个不被监视的地方，你知道，在黄昏纪的一些时代被我和其他几个小队当做了“公平竞赛”的区域——无论你想要做什么样的实验，或者想要给其他人带来怎样的恐怖，只要你到那些有关无尽的被遗忘的邪恶的时间段去做，这不会对事情的大局产生任何影响。相信我，我们已经确认了——这段时间发生的一切事情都无足轻重，除非你真有本事引发第二次魔法大爆炸。

不过你还是要知道一些最重要的事情：虽然泽梅基斯比我还懒，但他也有他要维持的东西。如果你不停违抗他的意志，总有一天，你会被告知，你已经被抓到了，请你停止抵抗。接受他为你安排的命运。如果你仍然负隅顽抗的话，很快，他会不得不把你作为一个严厉的例子，以至于整个宇宙都会注意到你的灭亡。很显然，我们也不确定他真的对谁做过这样的事情，或者是他到底会做什么，不过，我们可以确定，你的命运会和某个以“W-”开头的东西差不多。

这里的所有人都有一致的目标——保持时空稳定，享受自己的力量，和概率开个玩笑——但是我们有要维持的掩护身份，并且，理论上来说，当有人摧毁了夏·图尔防护罩或者Greigu找到了一个方法穿越传送门屏障之类的事情发生时，我们是真的有事可做的。别人帮了你的忙，你也要记得还回去；但别把动静弄得太大，免得整个系统在你头顶崩塌。如此这般的话，你就能享受这份永恒。

欢迎来到零点圣域，特工。这里面装的时空坐标指向的东西，只有我们可以毫不客气地说，是有史以来可能存在的最好的烤雪人餐厅——我的小队会在那时那地等你。一会儿谢。
[i]-加尔萨麦[/i]

注：你可能会在旅途中遇到一些……某种意义上的恩人。当你看见它时就会认出它——它正笨拙地把它的傀儡从死亡边缘拽回来。如果你亲眼见证了这一切，我们很遗憾地通知你，你已经踏上一条单程旅途，离开了作为主时间线的E4-RL辖域，落入一条注定灭亡的支线——除非“他”愿意把你重新编织回来。而它似乎一般只会对那些凭借惊人的力量或运气、堪堪躲过它一手策划的末日的人这么做。如果你已被它的算计选中，那就顺着演下去，你或许能从E4-EXPADV时间轴子网络那座时间坟场里被带回来。我们不知道它是什么 —— 到底是我们自己失控的创造物，是某个竞争对手的武器，或者远远超出我们自己的东西 —— 但是如果它有敌意，它已经赢了。到目前为止，它一直是……处在合作的状态。请注意不要提醒它我们是它的竞争对手。

确认依据：lore/misc.lua:725/729：a few decades in the Age of Dusk 被译成“黄昏纪的一些时代”（几十年→时代，时长错误）；cheat at a few lotteries 被译成“和概率开个玩笑”，丢失彩票作弊。忠实度缺陷，两处有界修复。
独立语境复核补充并经宿主核验 lore/misc.lua:725–735：除 surface 键的 a few decades→“一些时代”与 cheat at a few lotteries 丢失外，fair game 习语被直译为“公平竞赛”（原意为可以随意下手、不受约束的时段），what is, quite literally, the best roast-yeti restaurant 被误译为“只有我们可以毫不客气地说”。四处一并有界修复。

## eb509ae5feddd122d38bc3d5582be3bebe229872cf02b5a7e613395661b2f98f

section: mod-tome/data/talents/cunning/traps.lua
source_tag: tformat

source: Construct attacks all adjacent enemies each turn for %d turns.

target: 每回合攻击周围生物，持续 %d 回合。

确认依据：cunning/traps.lua:391–425 bladestorm construct on_act 仅对 reactionToward<0 的相邻敌人 attackTarget；译文“每回合攻击周围生物”把敌人扩大为所有生物并删去“所有”，主语“构造体”也缺失。机制描述缺陷，整句修复。
与 surface 键同一缺陷：traps.lua bladestorm construct on_act 仅 attackTarget reactionToward<0 的相邻目标；译文缺主语“构造体”，“周围生物”扩大对象并删“所有”。确认整句修复。

## eb5c2ab3aa8096189932ae157832e572e2feb4932de587f716702ce8c9e03c81

section: mod-tome/data/timed_effects/physical.lua
source_tag: _t

source: #Target# has escaped the crushing hold.

target: #Target#脱离了击碎效果。

确认依据：timed_effects/physical.lua:1494–1502 CRUSHING_HOLD（现行效果名“碾压擒抱”，grapple/pin）；on_lose 文本“脱离了击碎效果”把 crushing hold 误作击碎效果，与效果名不一致，确认修复为挣脱碾压擒抱。
与 surface 键同一缺陷：physical.lua:1494–1502 CRUSHING_HOLD（grapple/pin，现行效果名“碾压擒抱”），“脱离了击碎效果”误译，确认修复为挣脱碾压擒抱。

## 最终 target 以 FINAL-TARGETS.json 为准

上文“范围约束”记录的是256批原始确认要点；原任务复审后另有裁决（ADJUDICATION-R0/F1/R2/F3）：刀刃风暴主语用术语库 preferred“构装体”；时空特工入职信除原四处外，另修 nigh-omnipotence、纸牌屋暴政体系、结尾空行（LF 14）、lucky enough、一秒一秒规则、潜在罪犯句、status to maintain、non-existence/how many (if any)、mostly cooperative、Sher'Tul 防护罩裂缝、invitation 增译、competing culture、似乎、Look 等，以及 F3 的“我们和其他几个小队”。EXECUTOR 必须逐字应用 .ai/task/repair-w10-20260923/FINAL-TARGETS.json 中5个 final_target，不得自行改写。
