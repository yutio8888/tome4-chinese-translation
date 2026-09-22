# batch-130：32 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-04113
位置：tome-orcs.lua:8216；section：tome-orcs/superload/mod/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You can not recall until you have placed the bomb at the tunnel's end!
```
译文：
```text
你只有在隧道尽头放置炸弹之后，才能启用回归之杖！
```

## entry-04114
位置：tome-orcs.lua:8259；section：tome-orcs/superload/mod/class/interface/Archery.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-04115
位置：tome-orcs.lua:8341；section：tome-orcs/superload/mod/dialogs/debug/DebugMain.lua；source_tag：_t；args_order：None；special：None

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

坦塔洛斯：“这是[i]无关紧要[/i] 的。托马克？你一直在占卜潜在的地热能源，你能告诉大家哪里最有潜力吗？”

托马克：叹气。“不幸的是，就在克鲁克兽人的地盘底下。那确实是个有潜力的源头，提供能源的岩浆可不像我们地盘底下的都枯竭了，但是在那里挖掘会……好吧，我们都知道他们能多快的把建筑工具变成能威胁我们的武器。如果我们把能用来开采的最新式采矿工具带过去————”

坦塔洛斯：大笑。“采矿工具！你把我当成是怎样的傻瓜？帕拉奎，告诉我那些在大陆上到处搜寻兽人反叛者的齐腰高的小傻战士们在想什么。”举起手打断荣誉终身议员卡西罗斯。“我保证，真的无关紧要。”

帕拉奎：“不满……以及隐藏的，长期发酵的怒火。有些人想消灭克鲁克兽人，也有人想监禁他们。不论是哪种，我们都没法直接介入，不过确实可以提供某种支持。”

坦塔洛斯：“那么，在恰当的协商后，我们可以让那些有[i]无数[/i]兽人作战经验的小东西，来协助我们，让在克鲁克兽人境内的一切行动更易掌控。最少，我们可以取得那些已被长期证明能割断兽人喉咙的武器装备……自然，我们确实得想法子改成我们的尺寸。”

帕拉奎：“他们有个种族，护甲可以给我们用。穿起来有点紧，但是足够了。”

坦塔洛斯：“那就更好了！还有……卡西罗斯，我想让[i]你[/i]告诉我人民最在意什么。我敢肯定，你身上的伤痕一定能提醒你，公民们的意志是什么，对吧？”

卡西罗斯：[这一表述被视作过分的亵渎，以4比2的投票，通过从记录中削除。]

坦塔洛斯：“真是不成体统的发言啊！只是你们不能接受群众想要回他们的蒸汽。比起想要那些狡猾的小绿人们在身边，比起他们害怕把自己的手弄脏，比起想要以[i]你们[/i]的方法做事，更想要蒸汽。所以！这决定了我们从这方案里获益良多，决定了我们有或能找到解决困难的方式，也决定了这是选民们想要的。我看不需要进一步讨论了。纳沙尔，之后我想跟你讨论一个魔杖的事情。散会。”

[同时，卡西罗斯议员也在从议会正式辞职时做了一个不短的演讲。演讲被另一个文件记载。] 
```

## entry-04116
位置：tome-possessors.lua:5；section：tome-possessors/data/achievements/possessors.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kill your own Doomed Shade in the body of Bill.
```
译文：
```text
使用比尔的身体杀死你自己的被诅咒的影子。
```

## entry-04117
位置：tome-possessors.lua:7；section：tome-possessors/data/achievements/possessors.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kill Kryl'Feijan with the body of Shasshhiy'Kaish, or vice-versa.
```
译文：
```text
使用克里尔·费扬的身体杀死莎西·凯希，或者使用莎西·凯希的身体杀死克里尔·费扬。
```

## entry-04118
位置：tome-possessors.lua:9；section：tome-possessors/data/achievements/possessors.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kill High Paladin Aeryn with the body of Sun Paladin John.
```
译文：
```text
使用太阳骑士约翰的身体杀死高阶太阳骑士艾琳。
```

## entry-04119
位置：tome-possessors.lua:15；section：tome-possessors/data/birth/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#CRIMSON#BEWARE: This class is very #{italic}#strange#{normal}# and may be confusing to play for beginners.#LAST#
```
译文：
```text
#CRIMSON#注意: 该职业机制相当 #{italic}#奇怪#{normal}#，可能不适合新手使用。#LAST#
```

## entry-04120
位置：tome-possessors.lua:22；section：tome-possessors/data/birth/psionic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# -4
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# -4
```

## entry-04121
位置：tome-possessors.lua:28；section：tome-possessors/data/talents/psionic/battle-psionics.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require a mainhand weapon and an offhand mindstar to use this talent.
```
译文：
```text
你需要主手武器副手灵晶才能使用这一技能。
```

## entry-04122
位置：tome-possessors.lua:30；section：tome-possessors/data/talents/psionic/battle-psionics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You imbue your offhand mindstar with wild psionic forces.
		While active you gain %d%% more of your mindstar's mindpower and mind critical chance.
		Each time you make a melee attack you also add a stack of Psionic Disruption to your target.
		Each stack lasts for %d turns and deals %0.2f mind damage over the duration (max %d stacks).
		If you do not have a one handed weapon and a mindstar equiped, but have them in your off set, you instantly automatically switch. The wild psionic powers are incompatible with the focused nature of psiblades.
```
译文：
```text
向副手灵晶灌注狂暴的灵能力量。
		生效时，灵晶的精神强度和精神暴击几率增加 %d%%。
		每次近战攻击，都会给目标附加 1 层灵能瓦解效果。
		每层效果持续 %d 回合造成 %0.2f 精神伤害 (最多 %d 层)。
		如果你没有装备单手武器和灵晶，但在备用武器组里装备了它们，你会立刻自动切换到那组武器。此技能与心灵利刃不兼容。
```

## entry-04123
位置：tome-possessors.lua:56；section：tome-possessors/data/talents/psionic/battle-psionics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You concentrate to create a psionic block field all around you for 5 turns.
		While the effect holds all damage against you have a %d%% chance to be fully ignored.
		When damage is cancelled you instinctively make a retaliation mind strike against the source, dealing %0.2f mind damage. (The retaliation may only happen 2 times per turn.)
		
```
译文：
```text
创造一个持续 5 回合的灵能盾牌围绕你。
		技能生效时有 %d%% 几率会无视伤害。
		如果伤害被无视，你会对目标进行反击，造成 %0.2f 精神伤害。（每回合最多 2 次）
		
```

## entry-04124
位置：tome-possessors.lua:68；section：tome-possessors/data/talents/psionic/body-snatcher.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mind is so powerful it can bend reality, providing you with an extra-natural #{italic}#storage#{normal}# for bodies you snatch.
		You can store up to %d bodies.
```
译文：
```text
你的头脑是如此强大，它可以扭曲现实，为你提供一个超自然的 #{italic}#仓库#{normal}# 来储存你抢夺的身体。
		你最多可以储存 %d 具身体。
```

## entry-04125
位置：tome-possessors.lua:73；section：tome-possessors/data/talents/psionic/body-snatcher.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (Psionic Minion)
```
译文：
```text
%s（灵能仆从）
```

## entry-04126
位置：tome-possessors.lua:82；section：tome-possessors/data/talents/psionic/body-snatcher.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you store a body you also store %d more identical copies of it that you can use later.
		When you store a rare/unique/boss or higher rank creature you only get a third of the uses (but never less than one).
```
译文：
```text
当你获得一个身体时复制 %d 个克隆体.
		当你获得稀有/史诗/Boss 或者更高阶级的身体时，复制的数量除以 3（至少一个）。
```

## entry-04127
位置：tome-possessors.lua:88；section：tome-possessors/data/talents/psionic/body-snatcher.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you assume a form you may cannibalize a body in your reserve to replenish your current body.
		You can only use bodies that are of same or higher rank for the effect to work and each time you heal a body the effect will be reduced by 33%% for that body.
		Your current body will heal for %d%% of the max life of the cannibalized one and you will also regenerate 50%% of this value as psi.
		The healing effect is more psionic in nature than a real heal. As such may things that prevent healing will not prevent cannibalize from working.
		Cannibalize is the only possible way to heal a body.
		
```
译文：
```text
吞噬一具储备的身体，用来补充现在的身体。
		你只能吞噬同阶级或更高阶级的身体，且每次治疗后该身体的治疗效果降低 33%%。
		当前身体恢复被吞噬身体最大生命值 %d%% 的生命，同时恢复该数值 50%% 的灵能。
		该治疗在本质上比真正的治疗更接近灵能，因此阻止治疗的效果无法阻止吞噬生效。吞噬是治疗身体的唯一方法。
		
```

## entry-04128
位置：tome-possessors.lua:107；section：tome-possessors/data/talents/psionic/deep-horror.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mere presence is a blight in your foes minds. Using this link you are able to reach out and steal a talent from a target.
		For %d turns you will be able to use a random active (not passive, not sustained) talent from your target, and they will loose it.
		You may not steal a talent which you already know.
		The stolen talent will not use any resources to activate.
		At level 5 you are able to choose which talent to steal.
		The talent stolen will be limited to at most level %d.
```
译文：
```text
链接目标，偷取目标一个技能。
		持续 %d 回合，你获得目标一个随机主动技能（非被动，非持续），目标会失去该技能。
		你不会偷取一个已有的技能。
		偷取的技能不消耗任何能量。
		在等级 5 时，可选择偷取的技能。
		偷取的技能等级被限制成最高为 %d 级。
```

## entry-04129
位置：tome-possessors.lua:119；section：tome-possessors/data/talents/psionic/deep-horror.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
For a brief moment your whole body becomes etheral and you dash into a nearby creature and all those in straight line behind it (in range %d).
		You reappear on the other side, with %d more psi and having dealt %0.2f mind damage to your targets.
		
```
译文：
```text
短暂的一瞬间，你的整个身体变得飘渺，你对附近一个生物进行一次直线冲锋 (范围 %d)。
		你再次出现在另一边，获得 %d 灵能值并对目标造成 %0.2f 精神伤害。
		
```

## entry-04130
位置：tome-possessors.lua:133；section：tome-possessors/data/talents/psionic/deep-horror.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You are already assuming a form.
```
译文：
```text
你已经占据了一个躯体。
```

## entry-04131
位置：tome-possessors.lua:164；section：tome-possessors/data/talents/psionic/possession.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CRIMSON#A strange feeling comes over you as two words imprint themselves on your mind: '#{italic}#Not yet.#{normal}#'
```
译文：
```text
#CRIMSON#一种奇怪的感觉油然而生，两个词印入你的脑海：“#{italic}#还不是时候。#{normal}#”
```

## entry-04132
位置：tome-possessors.lua:187；section：tome-possessors/data/talents/psionic/possession.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You may not possess a creature of this rank (%s%s#LAST#).
```
译文：
```text
你不能附身这个阶级的生物（%s%s#LAST#）。
```

## entry-04133
位置：tome-possessors.lua:195；section：tome-possessors/data/talents/psionic/possession.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You cast a psionic web at a target that lasts for %d turns. Each turn it deals %0.2f mind damage.
		If the target dies with the web in place you will capture its body and store it in a hidden psionic reserve.
		At any further time you can use the Assume Form talent to temporarily shed your own body and assume your new form, strengths and weaknesses both.
		You may only use this power if you have room for a new body in your storage.

		You may only steal the body of creatures of the following rank %s%s#LAST# or lower.
		At level 3 up to rank %s%s#LAST#.
		At level 5 up to rank %s%s#LAST#.
		At level 7 up to rank %s%s#LAST#.

		You may only steal the body of creatures of the following types: #LIGHT_BLUE#%s#LAST#
		When you try to possess a creature of a different type you may learn this type permanently, you can do that %d more times.
```
译文：
```text
你对目标投掷一个持续 %d 回合的灵能网。每回合造成 %0.2f 精神伤害。
		如果目标在持续时间内死亡，你会获得它的身体并放入你的灵能仓库中。
		在任何时候，你可以使用附身技能暂时脱离你的身体进入新的身体，继承其优势和弱点。
		灵能仓库有位置时才能使用该技能。

		你可以偷取以下阶级生物的身体 %s%s#LAST# 或者更低。
		等级 3 时最多可偷取 %s%s#LAST#。
		等级 5 时最多可偷取 %s%s#LAST#。
		等级 7 时最多可偷取 %s%s#LAST#。

		你可能只会偷走以下类型的生物的尸体 : #LIGHT_BLUE#%s#LAST#
		当你尝试附身不同类型的生物时，你可以永久学习此类型，你还可以执行 %d 次。
```

## entry-04134
位置：tome-possessors.lua:219；section：tome-possessors/data/talents/psionic/possession.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you assume the form of an other body you can still keep %d%% of the values (defences, crits, powers, save, ...) of your own body.
```
译文：
```text
当你附身时，你还可以保留自己身体的属性 %d%%（闪避，暴击，强度，豁免……）。
```

## entry-04135
位置：tome-possessors.lua:221；section：tome-possessors/data/talents/psionic/possession.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you assume the form of another body you gain %d%% of the values (defences, crits, powers, save, ...) of the body.
		In addition talents gained from bodies are limited to level %0.1f.
```
译文：
```text
当你附身时，你获得身体 %d%% 的数值（闪避，暴击，强度，豁免……）。
		此外，从身体获得的技能等级最高为 %0.1f。
```

## entry-04136
位置：tome-possessors.lua:225；section：tome-possessors/data/talents/psionic/possession.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you assume the form of an other body you gain more control over the body:
		- at level 1 you gain one more talent slot
		- at level 2 you gain one more talent slot
		- at level 3 you gain resistances and flat resistances
		- at level 4 you gain one more talent slot
		- at level 5 you gain all speeds (only if they are superior to yours)
		- at level 6+ you gain one more talent slot
		
```
译文：
```text
附身时，可更好的控制身体 :
		- 在等级 1 时，可额外获得一个技能位
		- 在等级 2 时，可额外获得一个技能位
		- 在等级 3 时，可获得抗性和固定减伤
		- 在等级 4 时，可额外获得一个技能位
		- 在等级 5 时，可获得所有速度（只有当他们优于你时）
		- 在等级 6 以上时，可额外获得一个技能位
		
```

## entry-04137
位置：tome-possessors.lua:270；section：tome-possessors/data/talents/psionic/psionic-menace.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You point your ghastly finger at a foe affected by Ghastly Wail and send a psionic impulse to tell it to simply die.
		The target will take %d%% of the life it already lost as mind damage.
		On targets of rank boss or higher the damage is limited to %d.
		If the target dies from the Finger and is of a type you can already absorb it is directly absorbed into your bodies reserve.
		If you do not have two mindstars equiped, but have them in your off set, you instantly automatically switch. The wild psionic powers are incompatible with the focused nature of psiblades.
```
译文：
```text
用手指对受到恐怖嚎叫效果影响的敌人射出一道冲击波。
		目标将受到相当于其已损失生命值 %d%% 的精神伤害。
		对 boss 或者更高阶级的目标伤害最高为 %d。
		如果目标死于死亡一指，且其类型是你已经可以吸收的，则直接吸收到你的身体储备中。
		如果你没有双持灵晶，但在备用武器组里装备了它们，你会立刻自动切换到那组武器。此技能与心灵利刃不兼容。
```

## entry-04138
位置：tome-possessors.lua:317；section：tome-possessors/data/talents/psionic/psychic-blows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You create a psionic shield from your weapon that prevents you from ever taking blows that deal more than %d%% of your maximum life and gives you %d%% evasion.
		In addition, each time you take a melee hit the attacker automatically takes revenge strike that deals %d%% weapon damage as mind damage. (This effect can only happen once per turn)
		If you do not have a two handed weapon equiped, but have it in your off set, you instantly automatically switch.
```
译文：
```text
你通过武器创造灵能力场盾，每次受到伤害时，伤害不会超过最大生命值 %d%%，并有 %d%% 的几率闪避攻击。
		此外，每次受到近战攻击时，攻击者会受到 %d%% 武器精神伤害的反击，（每回合一次）
		如果你没有装备双手武器，但在备用武器组里装备了它，你会立刻自动切换到那组武器。
```

## entry-04139
位置：tome-possessors.lua:323；section：tome-possessors/data/talents/psionic/psychic-blows.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You concentrate your powerful psionic powers on your weapon and briefly unleash your fury.
		All foes in radius %d will take a melee attack dealing %d%% weapon damage as mind damage.
		Any psionic clones in the radius will have its remaining time extended by %d turns.
		If you do not have a two handed weapon equiped, but have it in your off set, you instantly automatically switch.
```
译文：
```text
你将强大的灵能力集中在你的武器上，并短暂地释放你的愤怒。
		半径 %d 内的敌人受到近战攻击造成 %d%% 武器精神伤害。
		范围内所有灵能克隆体的剩余持续时间延长 %d 回合。
		如果你没有装备双手武器，但在备用武器组里装备了它，你会立刻自动切换到那组武器。
```

## entry-04140
位置：tome-possessors.lua:343；section：tome-possessors/data/talents/psionic/ravenous-mind.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You feed on the pain of all foes in sight. For each one of them with life under 80%% you gain a stack of Sadist effect that increases your raw mindpower by %d.
		
```
译文：
```text
你从视野内所有敌人的痛苦中得到养分。每一个生命值低于 80%% 的敌人将让你获得一层虐待狂效果，每层增加你的原始精神强度 %d。
		
```

## entry-04141
位置：tome-possessors.lua:356；section：tome-possessors/data/talents/psionic/ravenous-mind.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
As long as you have at least a stack of Sadist you can radiate agony to all those you see in radius %d with 80%% or lower life left.
		For 5 turns their mind will be so focused on their own pain that they will deal %d%% less damage to you.
```
译文：
```text
当你至少有一层虐待狂效果时，你可以将自己的痛苦分享给半径 %d 内所有可见的、生命值 80%% 或更低的敌人。
		持续 5 回合，他们的头脑将如此专注于自己的痛苦，对你的伤害减少 %d%%。
```

## entry-04142
位置：tome-possessors.lua:376；section：tome-possessors/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kryl-Feijan
```
译文：
```text
克里尔·费扬
```

## entry-04143
位置：tome-possessors.lua:427；section：tome-possessors/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Mindpower (raw) increased by %d.
```
译文：
```text
精神强度（原始值）增加 %d。
```

## entry-04144
位置：tome-possessors.lua:500；section：tome-possessors/overload/mod/dialogs/AssumeFormSelectTalents.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#SLATE##{italic}#Your level of #LIGHT_BLUE#Full Control talent#LAST# is not high enough to use all the talents of this body. Select which to keep, your choice will be permanent for this body and its clones.
```
译文：
```text
#SLATE##{italic}#你的 #LIGHT_BLUE#完全控制#LAST# 技能 等级 不足，无法使用该身体的所有技能，选择需要保留的技能。你的选择对该身体及其克隆永久生效。
```

## 相关术语快照
```tsv
Cancel	取消	T.UI.LABEL	ui	_t	preferred	global	通用界面按钮（42 处）；对话框/菜单取消操作
Cannibalize	吞噬	T.GAME.TALENT	talents	talent name	preferred	dlc	possessors 附身系技能：吞噬储备身体以补充当前身体；统一技能名、对话框按钮与描述，不写作“合并”
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Psionic Disruption	灵能瓦解	T.GAME.TALENT	talents	talent name	existing	dlc	
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Tantalos	坦塔洛斯	T.PN.PERSON	society	entity name	preferred	dlc	气之部族首席议员；统一书信署名、叙事引用与实体名，不写作“坦塔罗斯”
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
flat	固定伤害减免	T.GAME.EFFECT	combat	effect subtype	preferred	global	flat damage reduction 机制；与正文'固定伤害减免'一致（P0 复审子代理 #83，用户确认）
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mainhand	主手	T.GAME.ENTITY	items	nil	existing	core	
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
offhand	副手	T.GAME.ENTITY	items	nil	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
