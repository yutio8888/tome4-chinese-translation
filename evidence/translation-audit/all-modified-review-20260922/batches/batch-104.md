# batch-104：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03429
位置：tome-ashes-urhrok.lua:1232；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select the victim:
```
译文：
```text
选择受害者：
```

## entry-03430
位置：tome-ashes-urhrok.lua:1233；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using demonic forces you create a link of pain from a source creature to a victim for %d turns.
		Each time the source creature takes damage the victim takes %d%% of the damage.
		If the victim dies from the effect you gain a burst of energy, reducing all remaining cooldowns by 1.
```
译文：
```text
使用恶魔之力，你在源生物与牺牲生物间构造痛苦链接，持续 %d 回合。
		每次源生物受到伤害时，%d%% 伤害由牺牲生物承受。
		当牺牲生物因此效果死亡时，你将获得能量，减少所有技能冷却时间 1 回合。
```

## entry-03431
位置：tome-ashes-urhrok.lua:1241；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Demon horns temporarily grow on your shield as you bash a foe with it for %d%% damage.
		If the attack hits the creature is impaled by the horns, causing it to bleed black blood for 50%% of the damage done as darkness over 5 turns.
		Any time you damage this foe in melee while it bleeds you get healed for %d (this can only happen once per turn).
		The healing power increases with your spellpower.
```
译文：
```text
你的盾牌上长出临时的恶魔之角。
		你盾击敌人造成 %d%% 伤害。
		如果攻击命中，目标将被恶魔角刺穿，流血 5 回合，合计受到额外 50%% 黑暗伤害。
		每次你攻击被恶魔角刺穿的目标时，你回复 %d 生命（每回合至多 1 次）。
		治疗效果受法术强度加成。
```

## entry-03432
位置：tome-ashes-urhrok.lua:1256；section：tome-ashes-urhrok/data/talents/corruptions/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (demonic husk)
```
译文：
```text
%s（恶魔尸傀）
```

## entry-03433
位置：tome-ashes-urhrok.lua:1273；section：tome-ashes-urhrok/data/talents/corruptions/oppression.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your successful melee hits apply a stacking effect that decreases damage done by %d%%.
		You can have up to %d stacks per target and further attacks refresh the duration, but any turn you are farther than %d spaces from the victim the fear will wear off quickly.
		At level 3 it also slows by %0.2f%% per stack.
		At level 5 you can horrify enemies in a radius of %d.
		This talent ignores saves and immunities.
		
```
译文：
```text
你的攻击能够惊吓目标，降低目标 %d%% 的伤害。
	此效果可以叠加 %d 次，每次攻击会刷新持续时间。但是当目标与你距离超过 %d 码，恐惧效果会迅速消退。
	技能 3 级时，每次叠加会同时减少目标 %0.2f%% 的速度。
	技能 5 级时，可以影响到 %d 码内的所有敌对生物。
	此技能无视豁免和免疫。
```

## entry-03434
位置：tome-ashes-urhrok.lua:1344；section：tome-ashes-urhrok/data/talents/corruptions/torture.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target with your weapon doing %d%% weapon damage. If the attack hits, the target is afflicted with Fiery Torment for %d turns, reducing their fire resistance by %d%%.
		When Fiery Torment ends the victim will take %d fire damage. This damage will increase by %d%% of all damage taken while under torment.
		The damage dealt by the effect will increase with spellpower.
		Demons under fiery torment will be burned by the flames of the Fearscape.
```
译文：
```text
用武器攻击敌人，造成 %d%% 武器伤害。如果命中，目标受到灼魂之罚的影响，持续 %d 回合，火焰抗性降低 %d%%。
	当灼魂之罚结束，敌人会受到 %d 点火焰伤害。
	在灼魂之罚持续时间内目标受到的所有伤害，有 %d%% 会加成到火焰伤害中。
	效果的伤害会随法术强度提升。
	被灼魂之罚影响的恶魔会被恶魔空间中的火焰焚烧。
```

## entry-03435
位置：tome-ashes-urhrok.lua:1368；section：tome-ashes-urhrok/data/talents/corruptions/wrath.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require a two handed weapon and being able to move to use this talent.
```
译文：
```text
你需要装备一把双手武器且可以移动，才能施展这个技能。
```

## entry-03436
位置：tome-ashes-urhrok.lua:1382；section：tome-ashes-urhrok/data/talents/corruptions/wrath.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your body overflows with the power of the Fearscape, turning you into a powerful demon for %d turns. This increases your stamina regen and physical power by %d, and your disarm and stun immunity by %d%%.
		The physical power, stamina regen, and status resistances increase with your spellpower.
		Your other talents also gain a variety of bonuses:
		-Draining Assault: Reduces cooldown by %d.
		-Reckless Strike: Gain %d%% resistance penetration for all elements for %d turns.
		-Obliterating Smash: Increases range by %d.
		-Abduction: If it hits, get an additional %d attacks at 35%% weapon damage.
		-Incinerating Blows: Increases chance of bonus damage to %d%%.
		-Fearfeast: Gain %0.1f vim per stack.
		-Maw of Urh'rok: Increases cone width by %d degrees.
```
译文：
```text
恶魔空间的力量充溢了你的身体，将你转换成一个强大的恶魔，持续 %d 回合。
	变身期间，体力恢复和物理强度增加 %d，缴械和震慑抗性增加 %d%%。
	物理强度、体力恢复和状态抗性加值受法术强度加成。
	变身期间，其他技能也受到强化：
	汲魂痛击：冷却时间减少 %d。
	舍身一击：增加 %d%% 全体抗性穿透，持续 %d 回合。
	歼灭挥斩：增加半径 %d。
	锁魂之链：如果命中，额外附加 %d 次 35%% 武器伤害的攻击。
	焚尽强击：增加额外伤害几率至 %d%%。
	恐惧盛宴：每汲取一层叠加的恐惧，获得 %0.1f 点活力。
	乌鲁洛克之口：角度增加 %d。
```

## entry-03437
位置：tome-ashes-urhrok.lua:1411；section：tome-ashes-urhrok/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hasten yourself out of phase, teleporting you to a specific location up to %d spaces away.
		You can activate this talent up to twice within the same turn, but the second activation will not be instant.
		Afterwards you stay out of phase for 5 turns. In this state your defense is increased by %d and all your resistances by %d%%.
		The bonus will increase with your Willpower.
```
译文：
```text
加速自身，以至于脱离空间，传送半径 %d。
		你在同一回合内至多连用两次该技能，且第二次使用会消耗时间。
		之后，你停留在相位外 5 回合，闪避增加 %d，全体抗性增加 %d%%。
		效果受意志加成。
```

## entry-03438
位置：tome-ashes-urhrok.lua:1423；section：tome-ashes-urhrok/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your original invisibility talent was corrupted and twisted.
		You have %d%% chance to turn into a dúathedlen for 5 turns, when hit by a blow doing at least 10%% of your total life.
		While in this form you gain the following effects:
		- you have permanent stealth (power %d)
		- your darkness damage is increased by %d%%
		- any non mind and non physical damage you deal above %d triggers a darkness explosion of radius 1 for half the damage (this can only happen once per turn)
		- when you transform the cooldowns of Haste of the Doomed and Pitiless are reset
		
```
译文：
```text
你原本的隐身技能被腐化扭曲了。
		当你受到一次至少为你总生命值 10%% 的伤害时，有 %d%% 几率转变成多瑟顿形态 5 回合。
		在多瑟顿形态下：
		- 你获得永久潜行 (强度 %d)
		- 你的暗影伤害增加 %d%%
		- 每当你造成超过 %d 点的非物理非精神伤害时，在半径 1 的范围内产生一次暗影爆炸，造成额外 50%% 伤害（每回合至多 1 次）。
		- 变形时重置种族技能“末日加速”与种族技能“无情”
		
```

## entry-03439
位置：tome-ashes-urhrok.lua:1449；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# imbues its weapon with demonic fire.
```
译文：
```text
#Target#用恶魔之火给武器附魔。
```

## entry-03440
位置：tome-ashes-urhrok.lua:1451；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s weapon looks less threatening.
```
译文：
```text
#Target#的危险度看起来降低了。
```

## entry-03441
位置：tome-ashes-urhrok.lua:1478；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s is no longer blazing.
```
译文：
```text
#Target#不再闪耀。
```

## entry-03442
位置：tome-ashes-urhrok.lua:1497；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# suffers!
```
译文：
```text
#Target# 被折磨！
```

## entry-03443
位置：tome-ashes-urhrok.lua:1505；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Damage from soulburn.
```
译文：
```text
来自灵魂燃烧的伤害。
```

## entry-03444
位置：tome-ashes-urhrok.lua:1538；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Infected by a demon seed. When it dies the caster has a %d%% chance to get back the matured seed.
```
译文：
```text
目标被恶魔之种感染，死亡时施法者有 %d%% 几率获得成熟的种子。
```

## entry-03445
位置：tome-ashes-urhrok.lua:1550；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Gain %d%% resistance and %d%% affinity to acid.
```
译文：
```text
获得%d%% 酸性抗性与 %d%%酸性伤害亲和。
```

## entry-03446
位置：tome-ashes-urhrok.lua:1597；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#ORANGE##Source# shares some pain with #target#!#LAST#
```
译文：
```text
#ORANGE##Source#与#target#共享痛苦！#LAST#
```

## entry-03447
位置：tome-ashes-urhrok.lua:1612；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
All damage affinity increased by %d%%.
Will not die until %d life
```
译文：
```text
全体伤害亲和增加 %d%%。
生命值不低于 %d 时不会死亡。
```

## entry-03448
位置：tome-ashes-urhrok.lua:1625；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have %d charges.
```
译文：
```text
叠加次数：%d。
```

## entry-03449
位置：tome-ashes-urhrok.lua:1628；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The target is surrounded by a fire haven, granting 40% fire damage affinity but -15% to blight resistance.
```
译文：
```text
目标被火焰庇护围绕，获得 40% 火焰伤害亲和，但减少 15% 枯萎抗性。
```

## entry-03450
位置：tome-ashes-urhrok.lua:1637；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Triggers Blood Drinker if this creature dies.
```
译文：
```text
这个生物死后会触发饮血者效果。
```

## entry-03451
位置：tome-ashes-urhrok.lua:1641；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：effect subtype；args_order：None；special：None

原文：
```text
affinity
```
译文：
```text
伤害亲和
```

## entry-03452
位置：tome-ashes-urhrok.lua:1643；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
All damage affinity increased by %d%%.
```
译文：
```text
全体伤害亲和提升%d%%。
```

## entry-03453
位置：tome-ashes-urhrok.lua:1655；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CRIMSON#Your corruption explodes around %s!
```
译文：
```text
#CRIMSON#你的腐化在%s周围爆炸！
```

## entry-03454
位置：tome-ashes-urhrok.lua:1729；section：tome-ashes-urhrok/data/zones/searing-halls/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A demon with 3 arms, ready to mutilate you. For experiment. Not for fun. Nope.
```
译文：
```text
一个长着三只手的恶魔，准备切割你。不是娱乐，而是实验。
```

## entry-03455
位置：tome-ashes-urhrok.lua:1752；section：tome-ashes-urhrok/init.lua；source_tag：init.lua description；args_order：None；special：None

原文：
```text
Many in Maj'Eyal have heard of "demons", sadistic creatures who appear seemingly from nowhere, leaving a trail of suffering and destruction whereever they go.  Their Fearscape floats far above the skies, watching and waiting, but not idly; their agents scout the land, their legions build up their forces, and their scholars develop new spells and strategies.  As the barrier between our worlds begins to crack under their scrutiny, helpless Eyalites have begun to disappear, whisked up to serve as their slaves and playthings.  They imbue these victims with magical powers to better survive the ensuing stresses - can you use your new-found abilities to escape the legions of Mal'Rok?

Features:
* Start with a new class, the Doombringer!  These avatars of demonic destruction charge into battle with massive two-handed weapons, cutting swaths of firey devastation through hordes of opponents.  Armed with flame magic and demonic strength, they delight in fighting against overwhelming odds, softening up the crowd with waves of fire, then feeding on the flames and suffering of their surroundings to stay alive while quickly reducing any group to a pile of ash and gore.
* Unlock a new class, the Demonologist, with an all-new item enhancement mechanic!  Bearing a shield and the magic of the Spellblaze itself, these melee-fighting casters can grow demonic seeds from their fallen enemies.  Imbue these seeds onto your items to gain a wide array of new talents and passive benefits, and summon the demons within them to fight on your side!  Ever looked at a gigantic demon-cursed minotaur and wished it was on your side for once?  Well, now you CAN summon one to pound your foes into paste while you cast devastating spells from afar, or call forth a squad of Fire Imps to pelt your enemies to death while they exhaust themselves on your impenetrable defenses!  Demons have persistent health, making them a little more precious than disposable necromancer skeletons or summoner beasts, but can be revived from death nonetheless.
* Two new zones, with all-new art, foes, and bosses!  You've seen the plains of the Fearscape before, now see the lairs and headquarters of the demons themselves!
* Over 10,000 words of written lore to find!  The demons were once an enlightened, peaceful race, hailing from a distant planet known as Mal'Rok; learn what drove them to plot Eyal's eternal torture!  Discover monuments to each of the demonic species and noteworthy individuals, showing the place of honor each has among them!  Get a glimpse into the culture and daily lives of these sadistic invaders and their brainwashed thralls!
* Unlock a new race, Doomelves: Shalore who've taken to the demonic alterations especially well, corrupting their typical abilities into a darker form.  Blink away to safety, transform into a shadowy dúathedlen to hide in the shadows or prey on your foes with blasts of darkness, use your new resilience to soak up status effects and critical hits, and assault your enemies' minds to leave them unsteady in combat!
* Between the aforementioned classes and Doomelves, a whopping 75 new talents!
* Unlock two new cosmetic options!  You know you've always wanted demon-horns.  
* Two new events, appearing anywhere in Eyal!
* 20 new artifacts, with unique and interesting effects.  Collect the Obsidian Treasures to amass more and more power!  Slip your hands into the Will of Ul'Gruth and watch your sweeping blows smash down walls!  Wear a giant hideous hell-mouth as a fashionable belt!
* 7 new achievements!  Conquer the worst Urh'Rok's forces can throw at you, and hang their metaphorical skulls from your profile page!

```
译文：
```text
在马基埃亚尔，很多人都曾听闻“恶魔”的大名，作为仿佛凭空出现的暴虐生物，他们无论走到哪里都会留下痛苦和毁灭。他们的恐惧空间高浮于天幕之上，并非闲置，而是一直在观察等待；他们的探员搜寻这片土地，他们的军团不断积蓄力量，他们的学者开发出全新的策略和法术。隔绝两端世界的屏障，在他们的破坏下开始破碎；无助的埃亚尔居民悄然消失，被掠走成为他们的奴隶和玩物。恶魔用魔法力量改造了受害者，使其能够在恶魔的拷问中存活 —— 你，能使用自己刚刚觉醒的新力量，逃脱玛·洛克的恶魔军团吗？

游戏特性：
* 使用全新职业开局，毁灭使者！他们是恶魔毁灭力量的化身，手拿双手武器加入战斗，将敌人化为一片火海。他们的手中掌握着火焰的魔法和恶魔的力量，在与势不可挡的敌人战斗中寻求欢愉。他们释放火海削弱敌群，随后吸收周围的火焰和痛苦，将任何敌人迅速化为灰烬。
* 解锁全新职业，恶魔使者，拥有全新的物品强化机制！这些近战施法者手拿盾牌，掌握魔法大爆炸本身的力量，可以从倒下的敌人身上培育出恶魔种子。将这些恶魔种子附魔到你的物品里，可以获得各种全新的技能和被动的能力，并召唤种子里的恶魔来加入战斗！你是否曾经看着巨大的恶魔牛头人，希望它能为你作战？现在，你确实可以召唤出来，你在远处释放法术的同时，他可以将敌人捣成浆糊。你也可以召唤火焰恶魔将敌人烧成灰烬，同时看着敌人在你铁壁般的防御面前无可奈何！恶魔具有更持久的生命值，比死灵法师易碎的骷髅或者自然召唤师的召唤兽更加珍贵，但仍然可以从死亡中复活。
* 两个新地区，具有全新的艺术，敌人和Boss！你以前曾经看过恶魔空间的平原，现在则可以看到恶魔自己的巢穴和总部！
* 超过一万字的全新手札！恶魔曾经是开明的和平种族，来自遥远的行星玛·洛克。了解是什么驱使他们策划给予埃亚尔永恒的折磨！探索恶魔物种和著名人物的纪念碑，展示每个人在其中的荣誉地位！瞥见这些嗜虐侵略者及其洗脑奴隶的文化和日常生活！
* 解锁一个新种族，魔化精灵：那些被恶魔的力量所改变的永恒精灵，他们的种族能力被腐化成了黑暗的形态。闪烁至安全处；变身为多瑟顿形态，在阴影中隐藏或给予敌人黑暗打击；坚韧缓和了负面状态和暴击伤害；在战斗中攻击敌人的精神，使他们难以为继！
* 上述职业和种族，提供了多达75个新技能！
* 解锁两个新的幻化选项！你知道你会想要恶魔之角的。
* 两个新随机事件，可能在埃亚尔大陆任何地方发生！
* 20个新神器，具有独特而有趣的效果。收集黑曜石宝藏以积累越来越多的力量！双手戴上乌尔格鲁斯的意志，挥舞拳头砸破墙壁！穿着巨大的可怕地狱嘴作为时尚腰带！
* 7个新成就！战胜乌鲁洛克最强大的敌人，将他们的头骨悬挂在个人页面上！

```

## entry-03456
位置：tome-ashes-urhrok.lua:1825；section：tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome #LIGHT_GREEN#@name@#WHITE#.
You do not remember much of your life before you were on this burning continent, floating in the void between worlds.  You have been helping demons, happily participating in their experiments to shatter some sort of shield preventing them from taking their righteous revenge on Eyal.

You are being taken by your handler to the torture-pits to help them figure out how to cause the most pain to those on Eyal, when you hear a roaring above you; you look up and see a burning meteor, flying closer, and the demons' spells failing to divert its course!  It lands near you, knocking you off your feet with its shockwave and killing your handler instantly.

As you recover, and your platform of searing earth splits from the main continent, your old memories flood your mind and you come to your senses - the demons are out to destroy your home!

#{bold}#You must escape!#{normal}#.

```
译文：
```text
你好，#LIGHT_GREEN#@name@#WHITE#。
你已经不太记得来到这片漂浮在虚空中的燃烧大陆之前的记忆了。你曾经帮助过恶魔，欢欣着参与他们的实验，以打破某种阻止恶魔正义复仇的无形屏障。

你被你的“主人”带到折磨场以帮助研究如何对埃亚尔大陆的生灵造成更大的痛苦，突然一阵轰鸣从天上传来，你抬头，看见一颗燃烧着的陨石正在坠落。恶魔试图用法术改变其轨迹，但没有成功！它落在你身边，砸死了你的“主人”，同时你也被冲击波击飞。

当你醒来后，你发现你身处一处和主大陆分离的焦土，而你旧时的记忆渐渐涌来。你立时惊醒——恶魔们要毁灭你的故乡！

#{bold}#你必须逃离这里！#{normal}#。

```

## entry-03457
位置：tome-ashes-urhrok.lua:1846；section：tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Corruptor (Demonologist)
```
译文：
```text
新职业：#LIGHT_GREEN#堕落系（恶魔使者）
```

## entry-03458
位置：tome-ashes-urhrok.lua:1847；section：tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Demons in their invasion of Eyal have abducted natives of the planet and mindwiped them to serve as double agents.
Trained in the use of the demon's own forces they have created many dark cults to spread fear and terror.
Some have managed to escape their programming and chose to follow their own desires instead.

You have defeated countless demons, seen how their essence work, witnessed how to bind demons to your own purpose and can now create new characters with the #LIGHT_GREEN#Demonologist class#WHITE#.

Corruptors are spellcasters, ranged attackers using magic.
Class features:#YELLOW#
- Infect your foes with demonic seeds.
- Bind demonic seeds to your equipment to enhance them.
- Summon and control demons to do your binding.
- Blend corrupted magic with a martial shield training to protect yourself and ruin your foes.#WHITE#

Corruptors use "vim" to power their special abilities.
Vim is the life force of all beings. It does not regenerate, and can only be stolen from your foes.

```
译文：
```text
在入侵埃亚尔大陆的过程中，恶魔绑架了这颗星球的居民，将他们洗脑后训练为双面间谍。

他们接受使用恶魔之力的训练，并通过黑暗仪式来传播不安与恐慌。

也有一些人成功逃脱了恶魔的控制，选择追随自己的渴望与意志。

你打败了无数的恶魔，掌握了他们本质的运作，见证了如何束缚恶魔为你所用，现在在你创建人物时可以选择新的职业 #LIGHT_GREEN#恶魔使者#WHITE#。

堕落系是施法职业，能使用魔法攻击敌人。
职业特点：#YELLOW#
- 向敌人注射恶魔之种
- 将恶魔种子附着在装备上，以强化装备效果
- 召唤并控制恶魔
- 将堕落魔法与盾牌战技结合，保护自己并毁灭敌人。#WHITE#

堕落者使用活力值来施放他们的法术。
活力是所有生物的生命力量，它不会自己回复，而必须从你的目标身上偷取。

```

## entry-03459
位置：tome-ashes-urhrok.lua:1908；section：tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Race: #LIGHT_GREEN#Doomelf
```
译文：
```text
新种族：#LIGHT_GREEN#魔化精灵
```

## entry-03460
位置：tome-ashes-urhrok.lua:1909；section：tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Doomelves are not a real race, they are Shaloren that have been taken by demons and transformed into harbingers of doom.
Their skills in inflicting and resisting pain have been honed by their rigorous training on the Fearscape.

You have killed the only three explorers from Mal'Rok that could have told the demons the truth and thus have earned the right to make #LIGHT_GREEN#Doomelf#WHITE# characters.

Race features:#YELLOW#
- Instant cast phase door
- Can turn into a dúathedlen
- Can increase detrimental effects and reduce beneficial ones on their foes
#WHITE#

```
译文：
```text
魔化精灵并不是一个真正的种族，他们曾是永恒精灵，而被恶魔抓去，变为末日的使者。
恶魔空间的烈火和严格训练磨砺了他们抵御痛苦、施展痛苦的强大能力。

你已经终结了从恶魔家乡玛·洛克来的仅有的那三位探险者。现在，恶魔们将无法了解到有关埃亚尔大陆的真相，#LIGHT_GREEN#魔化精灵#WHITE# 应运而生。

种族特点 :#YELLOW#
- 使用加速技能，瞬间穿梭空间
- 转化成多瑟顿形态
- 可以延长敌人的负面效果，缩短敌人的正面效果
#WHITE#

```

## entry-03461
位置：tome-ashes-urhrok.lua:1934；section：tome-ashes-urhrok/overload/mod/class/DemonologistsDLC.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Shadow Power: 
```
译文：
```text
阴影强度： 
```

## entry-03462
位置：tome-cults.lua:5；section：tome-cults/data/achievements/all.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Read a Forbidden Tome.
```
译文：
```text
读一本禁忌之书。
```

## entry-03463
位置：tome-cults.lua:42；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, +0 Dexterity, +3 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，+0 敏捷，+3 体质
```

## entry-03464
位置：tome-cults.lua:43；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Magic, +0 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * +3 魔法，+0 意志，+0 灵巧
```

## entry-03465
位置：tome-cults.lua:44；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# +3
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# +3
```

## entry-03466
位置：tome-cults.lua:51；section：tome-cults/data/birth/demented.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# -4
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# -4
```

## entry-03467
位置：tome-cults.lua:66；section：tome-cults/data/birth/drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, +1 Dexterity, +1 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，+1 敏捷，+1 体质
```

## entry-03468
位置：tome-cults.lua:67；section：tome-cults/data/birth/drem.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +2 Magic, -1 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * +2 魔法，-1 意志，+0 灵巧
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Corruptor	腐化者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Demonologist	恶魔使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Doombringer	毁灭使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Haste of the Doomed	末日加速	T.GAME.TALENT	talents	talent name	preferred	dlc	Ashes of Urh'Rok 魔化精灵种族技能；保留 of the Doomed 限定，不缩写为“加速”
Horns	角	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Out of Phase	脱离现实	T.GAME.EFFECT	combat	_t	preferred	core	传送后获得的相位状态名；统一沿用效果定义，不泛化为“传送后加成”
Phase Door	相位之门	T.GAME.TALENT	talents	talent name	existing	core	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Thrall	奴仆	T.GAME.EFFECT	combat	_t	preferred	core	精神支配后目标的状态身份；与 Mental Domination“精神控制”能力名区分
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
corruption	堕落	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
demonic strength	恶魔之力	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fearscape	恶魔空间	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
torture	折磨	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
