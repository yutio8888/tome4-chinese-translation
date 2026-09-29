# batch-056：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01625
位置：mod-tome.lua:22512；section：mod-tome/data/talents/chronomancy/temporal-hounds.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Upon activation summon a Temporal Hound.  Every %d turns another hound will be summoned, up to a maximum of three hounds. If a hound dies you'll summon a new hound in %d turns.  
		Your hounds inherit your increased damage percent, have %d%% physical resistance and %d%% temporal resistance, and are immune to teleportation effects.
		Hounds will get, %d Strength, %d Dexterity, %d Constitution, %d Magic, %d Willpower, and %d Cunning, based on your Magic stat.
```
译文：
```text
召唤一条时空猎犬。
		每隔 %d 回合召唤另一条时空猎犬，直至最多 3 条。
		当一条猎犬死去时，你将在 %d 回合内召唤一条新的猎犬。
		你猎犬继承你的伤害加成，有 %d%% 物理和 %d%% 时空抗性，对传送效果免疫。
		猎犬将拥有 %d 力量，%d 敏捷，%d 体质，%d 魔法，%d 意志和 %d 灵巧，基于你的魔法。
```

## entry-01626
位置：mod-tome.lua:22521；section：mod-tome/data/talents/chronomancy/temporal-hounds.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-01627
位置：mod-tome.lua:22522；section：mod-tome/data/talents/chronomancy/temporal-hounds.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-01628
位置：mod-tome.lua:22540；section：mod-tome/data/talents/chronomancy/temporal-hounds.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must have temporal hounds to use this talent.
```
译文：
```text
你必须拥有时空猎犬来使用该技能。
```

## entry-01629
位置：mod-tome.lua:22541；section：mod-tome/data/talents/chronomancy/temporal-hounds.lua；source_tag：tformat；args_order：[2, 1, 3, 4, 5]；special：None

原文：
```text
Command your Temporal Hounds to breathe time, dealing %0.2f temporal damage and reducing the three highest stats of all targets in a radius %d cone.
		Affected targets will have their stats reduced by %d for %d turns.  You are immune to the breath of your own hounds and your hounds are immune to stat damage from other hounds.
		When you learn this talent, your hounds gain %d%% temporal damage affinity.
```
译文：
```text
命令猎犬们使用时光吐息，对半径 %d 的锥形范围内所有目标造成 %0.2f 点时空伤害，并使其三项最高属性降低 %d 点，持续 %d 回合。
		你免疫自己猎犬的吐息。自己的猎犬免疫其他猎犬的属性降低效果。
		当你学会该技能后，猎犬们获得 %d%% 时空伤害亲和。
```

## entry-01630
位置：mod-tome.lua:22552；section：mod-tome/data/talents/chronomancy/threaded-combat.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-01631
位置：mod-tome.lua:22593；section：mod-tome/data/talents/chronomancy/timeline-threading.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The real %s... or so %s says.
```
译文：
```text
真正的%s……或者%s这样说。
```

## entry-01632
位置：mod-tome.lua:22595；section：mod-tome/data/talents/chronomancy/timeline-threading.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01633
位置：mod-tome.lua:22596；section：mod-tome/data/talents/chronomancy/timeline-threading.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
For the next %d turns two alternate versions of you enter your timeline.  While the effect is active all damage done by you or your copies is reduced by two thirds and all damage received is split between the three of you.
		Temporal Fugue does not normally cooldown while active.  You may take direct control of your clones, give them orders, and set their talent usage.
		Damage you deal to Fugue Clones or that they deal to you or each other is reduced to zero.
```
译文：
```text
接下来 %d 回合，2 个你的镜像进入你的时间线。
		当技能生效时，所有你或者你的镜像造成的伤害会减少 2/3，所有你或者镜像受到的伤害会由你们三者均分。
		开启时该技能不会正常冷却。你能直接控制你的镜像，给他们指令，或者调整技能使用策略。
		你和镜像不会互相伤害。
```

## entry-01634
位置：mod-tome.lua:22603；section：mod-tome/data/talents/chronomancy/timeline-threading.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your Rethread now braids the lifelines of all targets it hits for %d turns.  Braided targets take %d%% of all damage dealt to other braided targets.
		The amount of damage shared will scale with your Spellpower.
```
译文：
```text
你的重组技能将目标的生命线编织在一起 %d 回合。
		受影响的生物将受到其他受影响生物受到的 %d%% 伤害。
		伤害受法术强度加成。
```

## entry-01635
位置：mod-tome.lua:22608；section：mod-tome/data/talents/chronomancy/timeline-threading.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The timeline is too fractured to do this now.
```
译文：
```text
目前的时间线过于破碎，你现在无法这么做。
```

## entry-01636
位置：mod-tome.lua:22612；section：mod-tome/data/talents/chronomancy/timeline-threading.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Over the next %d turns, you attempt to remove the target from the timeline, lowering its resistance to physical and temporal damage by %d%%.
		If you manage to kill the target while the spell is in effect, you'll be returned to the point in time you cast this spell and the target will be slain.
		This spell splits the timeline.  Attempting to use another spell that also splits the timeline while this effect is active will be unsuccessful.
		The resistance penalty will scale with your Spellpower.
```
译文：
```text
接下来 %d 回合，你尝试抹杀目标在当前时间线的存在，降低目标物理和时空抗性 %d%%。
		如果你在法术生效期间击杀了目标，你将会返回到你释放该法术的时间点，而目标将被杀死。
		该法术会分裂时间线。法术生效期间，其余分裂时间线的法术将无法成功使用。
		抗性减少程度受法术强度加成。
```

## entry-01637
位置：mod-tome.lua:22631；section：mod-tome/data/talents/chronomancy/timetravel.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is immune!
```
译文：
```text
%s 免疫了！
```

## entry-01638
位置：mod-tome.lua:22633；section：mod-tome/data/talents/chronomancy/timetravel.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Something has prevented the timetravel.
```
译文：
```text
某物阻止了时空旅行。
```

## entry-01640
位置：mod-tome.lua:22642；section：mod-tome/data/talents/chronomancy/timetravel.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The spell fizzles...
```
译文：
```text
法术失败了……
```

## entry-01641
位置：mod-tome.lua:22645；section：mod-tome/data/talents/chronomancy/timetravel.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Some rookie paradox mage is about to find out that the standard-issue Temporal Reprieve takes you to a random safe-zone, not a fixed one, and left the contents of their pack strewn about the place. Nearly all of it is equipment that your transmutation chest won't process and is unusable by anything with less than twelve limbs, so you kick most of it into the void, but a crumpled note catches your eye...
```
译文：
```text
某个新手时空法师马上就会发现，标准的时空避难所会把你传送到一个随机的安全区域，而不是固定的地方，而这位法师已经把背包里的东西散落在了此处。这些装备几乎都是你的转化之盒处理不了的、没有十二条肢体根本用不了的东西，所以你把大部分踢进了虚空，但一张皱巴巴的笔记引起了你的注意……
```

## entry-01642
位置：mod-tome.lua:22646；section：mod-tome/data/talents/chronomancy/timetravel.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Transport yourself to a safe place for %d turns.
```
译文：
```text
将自己传送至安全的位置，停留 %d 回合。
```

## entry-01643
位置：mod-tome.lua:22659；section：mod-tome/data/talents/corruptions/blight.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Corrupted Negation
```
译文：
```text
堕落驱散
```

## entry-01644
位置：mod-tome.lua:22672；section：mod-tome/data/talents/corruptions/blight.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A furious storm of blighted poison rages around the caster in a radius of %d for %d turns.  Each creature hit by the storm takes %0.2f blight damage and is poisoned for %0.2f blight damage over 4 turns.
		At talent level 2 you have a chance to inflict Insidious Blight, which reduces healing by %d%%.
		At talent level 4 you have a chance to inflict Numbing Blight, which reduces all damage dealt by %d%%.
		At talent level 6 you have a chance to inflict Crippling Blight, which causes talents to have a %d%% chance of failure.
		Each possible effect is equally likely.
		The poison damage dealt is capable of a critical strike.
		The damage will increase with your Spellpower.
```
译文：
```text
一股强烈的剧毒风暴围绕着施法者，半径 %d 持续 %d 回合。风暴内的生物将进入中毒状态，受到 %0.2f 枯萎伤害并中毒 4 回合受到额外 %0.2f 枯萎伤害。
		技能等级 2 时有几率触发阴险毒素效果，降低 %d%% 治疗系数。
		技能等级 4 时有几率触发麻痹毒素效果，降低 %d%% 伤害。
		技能等级 6 时有几率触发致残毒素效果，%d%% 几率使用技能失败。
		中毒几率在可能的毒素效果中平分。
		毒素伤害可以暴击。
		伤害受法术强度加成。
```

## entry-01645
位置：mod-tome.lua:22718；section：mod-tome/data/talents/corruptions/bone.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures up a spear of bones, doing %0.2f physical damage to all targets in a line.  Each target takes an additional %d%% damage for each magical debuff they are afflicted with up to a max of %d%% (%d).
		The damage will increase with your Spellpower.
```
译文：
```text
释放一根骨矛，对一条线上的目标造成 %0.2f 物理伤害。这些目标每具有一个魔法负面效果，就额外受到 %d%% 的伤害，最多达到 %d%%（%d）。
		伤害受法术强度加成。
```

## entry-01646
位置：mod-tome.lua:22748；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Manipulate life force to feed your own dark powers.
```
译文：
```text
操纵生命之力来提高你自身的黑暗力量。
```

## entry-01647
位置：mod-tome.lua:22750；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
All the tools to torment your foes.
```
译文：
```text
用尽一切办法折磨你的敌人。
```

## entry-01648
位置：mod-tome.lua:22754；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of bones.
```
译文：
```text
控制白骨的力量。
```

## entry-01649
位置：mod-tome.lua:22756；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Hex your foes, hindering and crippling them.
```
译文：
```text
对你的敌人施加邪术，阻碍并削弱他们。
```

## entry-01650
位置：mod-tome.lua:22758；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Curse your foes, hindering and crippling them.
```
译文：
```text
诅咒你的目标，阻碍并削弱他们的力量。
```

## entry-01651
位置：mod-tome.lua:22762；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Spread diseases to your foes.
```
译文：
```text
在你的目标中传播疾病。
```

## entry-01652
位置：mod-tome.lua:22764；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Bring pain and destruction to the world.
```
译文：
```text
给这个世界带来痛苦和毁灭。
```

## entry-01653
位置：mod-tome.lua:22766；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Enhanced melee combat through the dark arts.
```
译文：
```text
利用黑暗力量来增强你的近战格斗。
```

## entry-01654
位置：mod-tome.lua:22768；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of blood, both your own and your foes'.
```
译文：
```text
操纵你和你目标鲜血的力量。
```

## entry-01655
位置：mod-tome.lua:22770；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Bring corruption and decay to all who oppose you.
```
译文：
```text
使任何敌对你的目标腐败和衰弱。
```

## entry-01656
位置：mod-tome.lua:22772；section：mod-tome/data/talents/corruptions/corruptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of the demonic shadowflame.
```
译文：
```text
学习驾驭恶魔暗影之火的力量。
```

## entry-01657
位置：mod-tome.lua:22823；section：mod-tome/data/talents/corruptions/plague.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whenever you deal non-disease blight damage you apply a disease dealing %0.2f blight damage per turn for 6 turns and reducing one of its physical stats (strength, constitution, dexterity) by %d. The three diseases can stack.
		Virulent Disease will always try to apply a disease the target does not currently have, and also one that will have the most debilitating effect for the target.
		This disease will try to prioritize being applied to an enemy with a high disease count near the target.
		The effect will increase with your Spellpower.
```
译文：
```text
每当你造成一个非疾病的枯萎伤害时，你将会对目标施加一项疾病，每回合造成 %0.2f 枯萎伤害，持续 6 回合，并降低其一项物理能力值（力量、体质、敏捷）%d。三种疾病可以叠加。
		剧毒瘟疫总是会试图施加一项目标当前尚未感染、且对目标负面效果最大的疾病。
		该疾病会优先施加在目标附近疾病数量较多的敌人身上。
		疾病效果随法术强度提升。
```

## entry-01658
位置：mod-tome.lua:22837；section：mod-tome/data/talents/corruptions/plague.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
Diseases #DARK_GREEN#BURN THROUGH#LAST# %s!
```
译文：
```text
疾病在 %s 身上 #DARK_GREEN#燃烧#LAST#！
```

## entry-01659
位置：mod-tome.lua:22839；section：mod-tome/data/talents/corruptions/plague.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
All your foes within a radius %d ball infected with a disease enter a cataleptic state, stunning them for %d turns and dealing %d%% of all remaining disease damage instantly.
```
译文：
```text
所有 %d 码球形范围内感染疾病的敌人进入僵硬状态，震慑它们 %d 回合并立即爆发 %d%% 剩余所有疾病伤害。
```

## entry-01660
位置：mod-tome.lua:22862；section：mod-tome/data/talents/corruptions/reaving-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you hit an enemy with a melee weapon you enter a bloodlust-infused frenzy, increasing your Spellpower by %0.1f.
		This effect stacks up to 10 times for a total Spellpower gain of %d.
		The frenzy lasts 3 turns.
```
译文：
```text
每当你使用近战武器击中一个目标，你进入嗜血状态，增加你的法术强度 %0.1f。
		这一效果最多叠加 10 层，共获得 %d 法术强度。
		嗜血状态持续 3 回合。
```

## entry-01661
位置：mod-tome.lua:22895；section：mod-tome/data/talents/corruptions/rot.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your body has become a mass of living corruption, increasing your blight and acid resistance by %d%% and blight affinity by %d%%.
On taking damage greater than 15%% of your maximum health, the damage will be reduced by %d%% and a carrion worm mass will burst forth onto a nearby tile, attacking your foes for 5 turns.
You can never have more than 5 worms active from any source at a time.
When a carrion worm dies it will explode into a radius 2 pool of blight for 5 turns, dealing %0.2f blight damage each turn and healing you for 33%% of that amount.
```
译文：
```text
你的身体已经腐败，增加 %d%% 枯萎和酸性抗性，%d%% 枯萎伤害亲和。
		每当你受到大于最大生命值 15%% 的伤害时，该伤害将减少 %d%%，同时在相邻的格子生成一团腐尸蠕虫，攻击你的敌人 5 回合。
		无论来源为何，你同时最多只能拥有 5 只蠕虫。
		蠕虫死亡时将爆炸，产生半径 2 的枯萎毒池，持续 5 回合，每回合造成 %0.2f 枯萎伤害，并按该伤害的 33%% 治疗你。
```

## entry-01662
位置：mod-tome.lua:22904；section：mod-tome/data/talents/corruptions/rot.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The worm walk fizzles!
```
译文：
```text
蠕虫行走失败了！
```

## entry-01663
位置：mod-tome.lua:22940；section：mod-tome/data/talents/corruptions/sanguisuge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Absorbs the life force of your foes as you kill them.
		As long as this talent is active, vim will decrease by 0.5 per turn and increase by %0.1f for each kill of a non-undead creature (in addition to the usual increase based on Willpower).
```
译文：
```text
当你杀死敌人时，你会吸收其生命力。
		当此技能激活时，每回合会消耗 0.5 点活力；当你杀死一个非不死族单位时，会获得 %0.1f 点活力（在基于意志的常规击杀加成之外额外获得）。
```

## entry-01664
位置：mod-tome.lua:22955；section：mod-tome/data/talents/corruptions/scourge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Strike the target with both weapons dealing %d%% damage with each hit.  Each strike that hits will increase the duration of the lowest duration disease effect by %d.
```
译文：
```text
向目标挥舞两把武器，每次攻击造成 %d%% 伤害，每次命中都会使目标身上持续时间最短的疾病效果的持续时间延长 %d 回合。
```

## entry-01665
位置：mod-tome.lua:22962；section：mod-tome/data/talents/corruptions/scourge.lua；source_tag：tformat；args_order：[1, 3, 2]；special：None

原文：
```text
Strike with each of your weapons, doing %d%% acid weapon damage with each hit.
		If at least one of the strikes hits, an acid splash is generated, doing %0.2f acid damage to all enemies in radius %d around the foe you struck.
		The splash damage will increase with your Spellpower.
```
译文：
```text
用每把武器打击目标，每次攻击造成 %d%% 酸性武器伤害。
		如果有至少一次攻击命中目标，则会产生酸系溅射，以被你击中的敌人为中心，对半径 %d 格范围内的所有敌人造成 %0.2f 酸性伤害。
		溅射伤害受法术强度加成。
```

## 相关术语快照
```tsv
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Frenzy	狂热	T.GAME.TALENT	talents	talent name	existing	global	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Paradox	紊乱值	T.GAME.RESOURCE	resources	_t	existing	core	
Paradox Mage	时空法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Temporal Hounds	时空猎犬	T.GAME.TALENT	talents	talent type	preferred	core	时空系召唤技能类别及生物称谓；统一不用“时空猎狗”
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
carrion worm mass	腐肉虫群	T.GAME.ENTITY	creatures	entity name	existing	core	统一实体名、生成日志及腐肉虫疾病描述
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
corruption	堕落	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
frenzy	狂乱	T.GAME.EFFECT	combat	effect subtype	existing	global	与技能名 Frenzy 的译法区分
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
paradox	紊乱	T.GAME.TALENT	talents	talent type	preferred	core	时空技能类别名；资源数值在其他语境使用“紊乱值”
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
