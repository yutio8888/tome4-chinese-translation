# batch-080：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02572
位置：mod-tome.lua:34395；section：mod-tome/data/texts/unlock-paladin_fallen.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class Evolution: #LIGHT_GREEN#Fallen (Sun Paladin)
```
译文：
```text
新职业进阶：#LIGHT_GREEN#堕落者（太阳骑士）
```

## entry-02573
位置：mod-tome.lua:34438；section：mod-tome/data/texts/unlock-psionic_mindslayer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Mindslayer (Psionic)
```
译文：
```text
新的职业：#LIGHT_GREEN#心灵杀手（灵能系）
```

## entry-02574
位置：mod-tome.lua:34439；section：mod-tome/data/texts/unlock-psionic_mindslayer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Mindslayers are the frontline fighters of the Yeeks' Way. Absolutely devoted to serving the Way, and thus all Yeeks, they dive into battle with nothing but their own mind.
Yeeks are natively psionic and thus most Mindslayers are Yeeks, but psionic powers do happen - rarely - in other races too.

You have saved a fellow Yeek Mindslayer and can now create characters with the #LIGHT_GREEN#Mindslayer class#WHITE#.

Mindslayers use their powerful psionic powers to supplement their low physical strength and dive into battle.
Class features:#YELLOW#
- Erect psionic shields around you both for protection and to absorb energy
- Engulf yourself in psionic auras - unleashing pain to all those near you
- Use your psionic "third hand" to hold a second weapon, floating in front of you
- Unleash the power of your sustained auras and shields by spiking them in great bursts of power#WHITE#

Mindslayers use their mind to manipulate the world.
They require energy to do so, which they take from the world around them.
While their shields are up incoming damage will be partly absorbed and the energy stored for later use.

```
译文：
```text
心灵杀手是夺心魔维网的前线战士。他们绝对忠于维网，亦即全体夺心魔，只凭自己的心灵便投身战斗。
夺心魔天生拥有灵能，因此大多数心灵杀手都是夺心魔；不过其他种族偶尔也会觉醒灵能。

你解救了一个夺心魔心灵杀手，现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#心灵杀手#WHITE#。

心灵杀手以强大的灵能力量弥补孱弱的肉体，投身近身战斗。
职业特点：#YELLOW#
- 在周身架起灵能护盾，既保护自己又吸收能量。
- 以灵能光环笼罩自身，让附近所有敌人承受痛苦。
- 用灵能“第三只手”握持第二把武器，使其悬浮在你面前。
- 令持续维持的光环和护盾过载，以巨大的能量爆发释放其力量。#WHITE#

心灵杀手用心灵操纵世界。
为此，他们需要从周围世界汲取能量。
护盾存在时，部分来袭伤害会被吸收，并储存为供以后使用的能量。

```

## entry-02575
位置：mod-tome.lua:34474；section：mod-tome/data/texts/unlock-psionic_solipsist.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Solipsist (Psionic)
```
译文：
```text
新职业：#LIGHT_GREEN#织梦者（灵能系）
```

## entry-02576
位置：mod-tome.lua:34475；section：mod-tome/data/texts/unlock-psionic_solipsist.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Solipsists are powerful psionicists that believe that the world is made up of nothing more than the thoughts and dreams of those that live in it.
This power does not come without a price, however.  The Solipsist must constantly fight with their own ego in order to keep a clear view of reality, lest they fall into a state of solipsism, the belief that the world and those that live in it are nothing more than figments of their own mind.

You've experienced the power of dreams first hand and may now create characters with the #LIGHT_GREEN#Solipsist class#WHITE#.

Solipsists use the power of thought and dreams to manipulate the world around them.
Class features:#YELLOW#
- Distort the fabric of reality
- Store and discharge psionic feedback
- Summon powerful warriors birthed from your own consciousness
- Convert damage you take into Psi damage and keep yourself alive with your mental reserves
- Put your foes to sleep, enter their dreams, and become their worst nightmare#WHITE#

Solipsists use their mind to manipulate the world around them.
They require energy to do so, which they recover naturally over time, and through methods others use to heal the body.

```
译文：
```text
织梦者是强大的灵能力者，他们相信世界是由思想和人们的梦境组成的。
这种力量并非毫无代价，织梦者必须不断与自己的自我抗争，以保持对现实的清晰认识，以免陷入唯我论状态，认为世界和生活在其中的人们不过是自己心灵的幻象。

你先前已经体验过梦境的力量了，现在你可以在创建人物时选择新的职业 #LIGHT_GREEN#织梦者#WHITE#。

织梦者利用思想和梦境的力量掌控身边的天地。
职业特点：#YELLOW#
- 能够扭曲现实位面
- 可储存并释放反馈能量
- 从意识中召唤强大的战士
- 将你受到的伤害转化为灵能值损失，并用精神储备维持自己的生命
- 使你的敌人陷入沉睡，进入它们的梦境，成为对方的梦魇。#WHITE#

织梦者利用思想和梦境的力量掌控身边的天地。
他们需要灵能来做这一切，而他们的灵能既可以通过自然回复，也可以通过其他人恢复生命值的方法来回复。

```

## entry-02577
位置：mod-tome.lua:34511；section：mod-tome/data/texts/unlock-race_ogre.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Ogres are magically-altered Humans, taking refuge in Elvala among the Shalore. 
Their enormous bodies, bolstered by (and dependent on) an intricate web of glowing runes covering their skin, make them an intimidating sight that belies their conscientious and modest nature.
Ogres were created (and subsequently abandoned) by the Conclave during the Allure Wars, to serve as their warriors and workers.  Their massive size and glowing runes made it impossible for them to hide during the Spellhunt, and only those who fled to Shalore lands survived extermination.
Their talent with inscriptions is unparalleled, as they need to be able to maintain their own inscriptions to survive, and have passed down the knowledge of how to do so; while their tendency to solve problems in the most simple and direct manner available (combined with an...  intense temper) has given them an unfair reputation as unintelligent brutes, a growing trade industry in inscription production is gradually eroding this image.

You have learned the details of the Ogres' past and put their terrified creators to rest, and have technically brought the Allure Wars to their long-overdue conclusion by eliminating the last remnants of the Conclave.  You can now create new #LIGHT_GREEN#Ogre#WHITE# characters to see their magical might in action!

Race features:#YELLOW#
- Strong but not stupid
- Efficient at using all kind of runes and infusions
- Imbued with arcane forces
#WHITE#

```
译文：
```text
食人魔是被魔法改变的人类，在埃尔瓦拉与永恒精灵为伴避难。
他们庞大的身躯由覆盖皮肤的复杂发光符文网络强化（也依赖于这套符文网络），外表令人生畏，却掩盖了他们认真而谦逊的天性。
在厄流战争中，孔克雷夫创造了食人魔作为工人和战士，但最后他们成为了被遗弃的种族。他们庞大的体型和身上闪光的符文让他们在魔法狩猎期间无处藏身，只有那些逃去永恒精灵领地的少量族群幸免于难。
因为他们必须要维护自己身上的刻印存活下去，他们操纵刻印的能力无可比拟，并且这份知识一直世代传承下去。他们解决问题的时候习惯使用最简单直接的手段，再加上他们……暴躁的脾性，这一切让他们获得了“愚蠢粗暴的野蛮人”这一不公的名声。然而，日益发展的刻印制作贸易正逐渐消除这种印象。

你学习了食人魔的过去，并让他们那惊恐万分的创造者得以安息。随着孔克雷夫最后残余的毁灭，厄流战争终于迎来了真正的结束。现在，你可以创造新的#LIGHT_GREEN#食人魔#WHITE#角色，在实战中发挥他们的魔法力量吧！

种族特色：#YELLOW#
- 强壮但不愚笨
- 善于使用各种纹身和符文
- 灌注奥术的力量
#WHITE#

```

## entry-02578
位置：mod-tome.lua:34540；section：mod-tome/data/texts/unlock-rogue_marauder.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Marauder (Rogue)
```
译文：
```text
新职业：#LIGHT_GREEN#掠夺者（盗贼系）
```

## entry-02579
位置：mod-tome.lua:34541；section：mod-tome/data/texts/unlock-rogue_marauder.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Some rogues live by strength rather than cunning, relying on vicious attacks instead of stealth and subterfuge. These bandits maraud the land, lightly armoured and wielding dual weapons, taking what they can by force.

You have learned the value in causing sheer damage in combat and can now create characters with the #LIGHT_GREEN#Marauder class#WHITE#.

Marauders are highly mobile rogues with a range of dextrous techniques and tactics at their disposal. Class features:#YELLOW#
- Move with ease around the battlefield, dancing around your foes and avoiding their attacks
- Wield dual weapons and unleash devastating techniques on your opponents
- Rely on pure thuggery to cripple your enemies before taking them down#WHITE#

Marauders use stamina to fuel their techniques, which replenishes slowly over time.

```
译文：
```text
有些盗贼依靠力量而非诡计生存，以凶狠的攻击取代潜行与欺骗。这些强盗身着轻甲、双持武器，横行各地，以武力夺取一切。

你已经明白在战斗中造成巨大伤害的价值，现在你在创建人物时可以选择新的职业 #LIGHT_GREEN#掠夺者#WHITE#。

掠夺者是机动性极高的盗贼，掌握着各种灵巧的技术与战术。
职业特点：#YELLOW#
- 轻松穿行战场，在敌人之间起舞并避开他们的攻击。
- 双持武器，对敌人施展毁灭性的技法。
- 依靠纯粹的暴力重创敌人，再将其击倒。#WHITE#

掠夺者使用体力值来施放他们的技能，体力值会随时间缓慢恢复。

```

## entry-02580
位置：mod-tome.lua:34567；section：mod-tome/data/texts/unlock-rogue_poisons.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Talent Category: #LIGHT_GREEN#Poisons
```
译文：
```text
新的技能树：#LIGHT_GREEN#毒素系
```

## entry-02581
位置：mod-tome.lua:34624；section：mod-tome/data/texts/unlock-undead_ghoul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Race: #LIGHT_GREEN#Ghoul (Undead)
```
译文：
```text
新种族：#LIGHT_GREEN#食尸鬼（不死亡灵）
```

## entry-02582
位置：mod-tome.lua:34625；section：mod-tome/data/texts/unlock-undead_ghoul.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Ghouls are evil undead creatures. Usually raised by Necromancers to serve as mindless servants, some manage to keep their sentience and roam the world in a blazing path of destruction.
You have killed the Master, a malevolent undead creature. You can now create a new character with the #LIGHT_GREEN#Ghoul race#WHITE#.

Race features:#YELLOW#
- Great poison resistance
- Bleeding immunity
- Stun resistance
- Fear immunity
- Special ghoul talents: ghoulish leap, gnaw and retch#WHITE#

```
译文：
```text
食尸鬼是邪恶的不死亡灵。通常被死灵法师复活为无意识的仆从，但有些食尸鬼设法保留了意识，在世界上留下一条燃烧的毁灭之路。
你杀死了主人，一个恶毒的不死亡灵。现在你在创建人物时可以选择新的种族：#LIGHT_GREEN#食尸鬼#WHITE#。

种族特色：#YELLOW#
- 强大的毒素抗性
- 流血免疫
- 震慑抵抗
- 恐惧免疫
- 特殊的食尸鬼技能：食尸鬼跳跃、啃噬和腐秽呕吐#WHITE#

```

## entry-02583
位置：mod-tome.lua:34648；section：mod-tome/data/texts/unlock-undead_skeleton.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Race: #LIGHT_GREEN#Skeleton (Undead)
```
译文：
```text
新种族：#LIGHT_GREEN#骷髅（不死亡灵）
```

## entry-02584
位置：mod-tome.lua:34649；section：mod-tome/data/texts/unlock-undead_skeleton.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Skeletons are evil undead creatures. Usually raised by Necromancers to serve as mindless servants, some manage to keep their sentience and roam the world in a blazing path of destruction.
You have killed the Master, a malevolent undead creature. You can now create a new character with the #LIGHT_GREEN#Skeleton race#WHITE#.

Race features:#YELLOW#
- Poison immunity
- Bleeding immunity
- Fear immunity
- No need to breathe
- Special skeleton talents: bone armour, resilient bones, re-assemble#WHITE#

```
译文：
```text
骷髅是邪恶的不死亡灵。通常被死灵法师复活为无意识的仆从，但有些骷髅设法保留了意识，在世界上留下一条燃烧的毁灭之路。
你杀死了主人，一个恶毒的不死亡灵。现在你在创建人物时可以选择新的种族：#LIGHT_GREEN#骷髅#WHITE#。

种族特色：#YELLOW#
- 毒素免疫
- 流血免疫
- 恐惧免疫
- 无需呼吸
- 特殊骷髅技能：骨质盔甲，弹力骨骼，重组#WHITE#

```

## entry-02585
位置：mod-tome.lua:34672；section：mod-tome/data/texts/unlock-wanderer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Wanderer
```
译文：
```text
新职业：#LIGHT_GREEN#流浪者
```

## entry-02586
位置：mod-tome.lua:34673；section：mod-tome/data/texts/unlock-wanderer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You have wanderer quite a lot since your birth!
You can now create new characters with the #LIGHT_GREEN#Wanderer class#WHITE#.

Wanderers start the game with 3 randomly selected class trees, 1 randomly selected generic tree and Combat Training.
Every 5 levels the gain a new random class tree and every 10 levels they gain a new generic tree.
They are a #{bold}#bonus#{normal}# class, in no way meant to be balanced or even working with all possible talent combos.
Use at your own risk, and have fun.
```
译文：
```text
从出生以来，你已旅行过许多地方！
现在你在创建人物时可以选择新的职业：#LIGHT_GREEN#流浪者#WHITE#。

流浪者开始游戏时拥有三系随机职业技能，一系随机通用技能，以及战斗训练系。
每升五级将获得额外一系随机职业技能，每升10级将获得额外一系随机通用技能。
他们是一种 #{bold}# 奖励 #{normal}# 职业，没有经过任何的平衡测试，也不保证技能可用。
风险自负，游戏愉快。
```

## entry-02587
位置：mod-tome.lua:34690；section：mod-tome/data/texts/unlock-warrior_brawler.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Brawler (Warrior)
```
译文：
```text
新职业：#LIGHT_GREEN#格斗家（战士系）
```

## entry-02588
位置：mod-tome.lua:34691；section：mod-tome/data/texts/unlock-warrior_brawler.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The ravages of the Spellblaze stretched armies thin and left many unprotected. Not everyone could afford the luxury of a weapon.
Without steel or iron, poor communities of all races turned to the strength of their own bodies for defense against the darkness.
These unarmed techniques still exist today.

You have learned these techniques and can now create new characters with the #LIGHT_GREEN#Brawler class#WHITE#.

Brawlers are warriors who fight with little more than their own bodies as weapons.
Class features:#YELLOW#
- Build deadly combination attacks with your strikes
- Wear gauntlets or gloves to boost your damage
- Outwit your foes and set them up for deadly counter attacks
- Control your enemies and break their bones with fierce grappling techniques#WHITE#

Brawlers use stamina and must remain at least semi-mobile.  As such they cannot perform their unarmed talents in massive armor.

```
译文：
```text
魔法大爆炸的蹂躏令军队捉襟见肘，许多人无人保护。并非每个人都买得起武器这种奢侈品。
没有钢铁，各族贫困社群只能依靠自身躯体的力量抵御黑暗。
这些徒手技艺流传至今。

你已经学会了这种技巧，现在你在创建人物时可以选择新的职业：#LIGHT_GREEN#格斗家#WHITE#。

格斗家是以自身身体作战的职业。
职业特点：#YELLOW#
- 可以制造致命的连击
- 装备臂铠或手套来提升伤害
- 使用计谋迷惑你的敌人并伺机反击
- 使用凶猛的关节技控制敌人并打碎他们的骨头#WHITE#

格斗家使用体力，并且必须至少保持一定的机动性。因此，身穿板甲时无法施展徒手技能。

```

## entry-02589
位置：mod-tome.lua:34724；section：mod-tome/data/texts/unlock-wilder_oozemancer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Oozemancer (Wilder)
```
译文：
```text
新职业：#LIGHT_GREEN#软泥使（野性系）
```

## entry-02590
位置：mod-tome.lua:34725；section：mod-tome/data/texts/unlock-wilder_oozemancer.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The long Nature's hatred of all arcane forces has managed to create Oozemancers as the ultimate answer to archmagi.
You have met and destroyed a corrupted one and can now create new characters with the #LIGHT_GREEN#Oozemancer class#WHITE#.

Oozemancer are Wilders, who are at home in the wilds and draw their power from their connection with nature.
Class features:#YELLOW#
- Offensive long range nature and acidic attacks
- Inherently antimagic
- Summon various kinds of oozes to your side for a short while
- Use oozes, slimes, mucus and moss against Nature's foes#WHITE#

All Wilder classes use Equilibrium for their powers. It represents their connection to nature. 
The higher it gets the more off-balance they are with it. A high Equilibrium makes for a chance to fail to use a power and lose a turn.

```
译文：
```text
自然长期对一切奥术能量的憎恨最终成功地制造出软泥使这一职业，作为对抗元素法师的最终答案。
你已经遇到并且摧毁了一名堕落的软泥使，现在可以创建能学习 #LIGHT_GREEN#软泥使#WHITE# 职业的新角色。

软泥使属于野性系，以野外为家，与自然的联系是他们的力量来源。
职业特点：#YELLOW#
- 远距离的自然与酸性攻击
- 天生反魔
- 短暂召唤各种软泥怪到你身边
- 使用软泥、史莱姆、粘液和苔藓来对抗自然的敌人#WHITE#

所有野性系职业使用自然失衡值作为其能量，它与自然之间的联系密切相关。
失衡值越高，他们与自然越不平衡。失衡值过高可能导致能力使用失败并损失一个回合。

```

## entry-02591
位置：mod-tome.lua:34754；section：mod-tome/data/texts/unlock-wilder_stone_warden.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Stone Warden (Wilder)
```
译文：
```text
新职业：#LIGHT_GREEN#岩石守卫（野性系）
```

## entry-02592
位置：mod-tome.lua:34755；section：mod-tome/data/texts/unlock-wilder_stone_warden.lua；source_tag：_t；args_order：None；special：None

原文：
```text
While most races of Eyal firmly believe that arcane and nature forces are opposites, Dwarves have found a way to bind them together and meld them into a power to be reckoned with.

You have mastered some arcane and wild talents at a crude level can now create new dwarf characters with the #LIGHT_GREEN#Stone Warden class#WHITE#.

Stone Wardens are Wilders, who are at home in the wilds and draw their power from their connection with nature and arcane
Class features:#YELLOW#
- Dual wield shields and bash your foes with arcane enhanced shield strikes
- Combine arcane and nature forces to split yourself into two powerful halves
- Use vines of stone to grab and assail your foes
- Turn into a huge earth elemental and summon volcanos
- Dwarf race exclusive class (Select it at birth for the option to even appear)#WHITE#

All Wilder classes use Equilibrium for their powers. It represents their connection to nature. 
The higher it gets the more off-balance they are with it. A high Equilibrium makes for a chance to fail to use a power and lose a turn.
Stone Wardens also use Mana.

```
译文：
```text
尽管大部分埃亚尔的种族都坚信奥术和自然的力量势不两立，矮人们找到了一种方法，可以将它们联结起来，组成一种让人无法忽视的强大力量。

你已经初步掌握了一些奥术与自然技能，现在创建的新矮人角色可以选择#LIGHT_GREEN#岩石守卫职业#WHITE#。

岩石守卫是野性系职业，它们植根于自然，从自然和奥术的联结中汲取力量。
职业特性：#YELLOW#
- 双持盾牌，使用奥术强化的盾牌打击攻击敌人
- 结合奥术和自然的力量，产生两个强大的分身。
- 使用岩石藤蔓抓取并攻击敌人。
- 变化成巨大的岩石元素，召唤火山。
- 这是矮人专属的职业，只有在创建角色画面选择矮人才能看到。#WHITE#

所有野性系职业使用自然失衡值作为其能量，它与自然之间的联系密切相关。
失衡值越高，他们与自然越不平衡。失衡值过高可能导致能力使用失败并损失一个回合。
岩石守卫同样使用法力值。

```

## entry-02593
位置：mod-tome.lua:34790；section：mod-tome/data/texts/unlock-wilder_summoner.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Summoner (Wilder)
```
译文：
```text
新职业：#LIGHT_GREEN#召唤师（野性系）
```

## entry-02594
位置：mod-tome.lua:34791；section：mod-tome/data/texts/unlock-wilder_summoner.lua；source_tag：_t；args_order：None；special：None

原文：
```text
In the wilds, some people and creatures are able, by the sole force of their will, to call upon allies to help them in combat.
You have witnessed such an act and can now create new characters with the #LIGHT_GREEN#Summoner class#WHITE#.

Summoners are Wilders, who are at home in the wilds and draw their power from their connection with nature.
Class features:#YELLOW#
- Summon allies, ranging from a war hound to the mighty fire drake
- Take direct control of your summons
- Augment your summons with various powers#WHITE#

All Wilder classes use Equilibrium for their powers. It represents their connection to nature. 
The higher it gets the more off-balance they are with it. A high Equilibrium makes for a chance to fail to use a power and lose a turn.

```
译文：
```text
在野外，有些人和生物仅凭意志力，就能召唤盟友协助战斗。
你已经见证了这种力量的存在，现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#召唤师#WHITE#。

召唤师属于野性系，以野外为家，与自然的联系是他们的力量来源。
职业特点：#YELLOW#
- 能召唤盟友，从战争猎犬到强大的火龙不等
- 能直接控制你的召唤物
- 使用不同的方式强化你的召唤物#WHITE#

所有野性系职业使用自然失衡值作为其能量，它与自然之间的联系密切相关。
失衡值越高，他们与自然越不平衡。失衡值过高可能导致能力使用失败并损失一个回合。

```

## entry-02595
位置：mod-tome.lua:34818；section：mod-tome/data/texts/unlock-wilder_wyrmic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Class: #LIGHT_GREEN#Wyrmic (Wilder)
```
译文：
```text
新职业：#LIGHT_GREEN#龙战士（野性系）
```

## entry-02596
位置：mod-tome.lua:34819；section：mod-tome/data/texts/unlock-wilder_wyrmic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Some people, either through training or magic, can take on the defining aspects of the dragon-kin themselves.
You have consumed a magic that allows you to gain such a power. You can now also create new characters with the #LIGHT_GREEN#Wyrmic class#WHITE#.

Wyrmics are Wilders, who are at home in the wilds and draw their power from their connection with the dragons.
Class features:#YELLOW#
- Take on the aspects of drakes: fire, cold, sand, and more
- Breath weapons: fire, ice, sand, and more
- Powerful melee combatant#WHITE#

All Wilder classes use Equilibrium for their powers. It represents their connection to nature. 
The higher it gets the more off-balance they are with it. A high equilibrium makes for a chance to fail to use a power and lose a turn.
Wyrmics are also trained in the martial arts and use stamina for some techniques.

```
译文：
```text
有些人，无论通过训练还是魔法，都能获得龙族的特征。
你已经吞服了能让你获得这种力量的魔法。现在你可以在创建人物时选择新的职业：#LIGHT_GREEN#龙战士#WHITE#。

龙战士属于野性系，以野外为家，力量来自于与龙族的联系。
职业特点：#YELLOW#
- 获得龙兽的形态特征：火焰、寒冷、沙土等
- 吐息武器：火焰、寒冰、沙土等
- 强大的近战战斗能力#WHITE#

所有野性系职业使用自然失衡值作为其能量，它与自然之间的联系密切相关。
失衡值越高，他们与自然越不平衡。失衡值过高可能导致能力使用失败并损失一个回合。
此外龙战士也受过武术训练，使用体力值施展部分技巧。

```

## entry-02597
位置：mod-tome.lua:34848；section：mod-tome/data/texts/unlock-yeek.lua；source_tag：_t；args_order：None；special：None

原文：
```text
New Race: #LIGHT_GREEN#Yeek
```
译文：
```text
新种族：#LIGHT_GREEN#夺心魔
```

## entry-02598
位置：mod-tome.lua:34849；section：mod-tome/data/texts/unlock-yeek.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Yeeks are a mysterious race of small humanoids native to the tropical island of Rel.
Their body is covered with white fur and their disproportionate heads give them a ridiculous look, yet they are a cunning and willful race.
Although they are now nearly unheard of in Maj'Eyal, they spent many centuries as secret slaves to the Halfling nation of Nargol.
They gained their freedom during the Age of Pyre and have since then followed 'The Way' - a unity of minds enforced by their powerful psionics.

You have helped a Yeek Wayist and can now create a new character with the #LIGHT_GREEN#Yeek race#WHITE#.

Race features:#YELLOW#
- Mental domination racial power
- Confusion resistance
- Fast leveling
- Frail body#WHITE#

```
译文：
```text
夺心魔是热带小岛瑞尔岛上比较神秘的人形原住民种族。
他们的身体长着白色的毛发，另外他们有着不成比例的巨大脑袋使他们看上去样子有点滑稽。
不过他们是非常灵巧而且意志强大的种族。
尽管在马基·埃亚尔几乎没有听说过他们，但在烈火纪元之前的漫长岁月里，他们曾是半身人国家纳格尔的秘密奴隶。
他们在烈火纪元获得了自由，并从此遵循“维网”——一种由他们强大的灵能维系的心灵统一。

你帮助了一名夺心魔维网信徒，现在你可以在创建人物时选择新的种族：#LIGHT_GREEN#夺心魔#WHITE#。

种族特点：#YELLOW#
- 拥有精神控制的种族能力
- 混乱抗性
- 升级较快
- 脆弱的身躯#WHITE#

```

## entry-02599
位置：mod-tome.lua:34882；section：mod-tome/data/timed_effects/floor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is near a font of life, granting %+0.2f life regeneration, %+0.2f equilibrium regeneration, %+0.2f stamina regeneration and %+0.2f psi regeneration.  (Only living creatures benefit.)
```
译文：
```text
目标靠近生命之泉，增加 %+0.2f 生命回复，%+0.2f 失衡值回复，%+0.2f 体力回复和 %+0.2f 灵能回复。不死族无法获得此效果。
```

## entry-02600
位置：mod-tome.lua:34883；section：mod-tome/data/timed_effects/floor.lua；source_tag：floorEffect desc；args_order：None；special：None

原文：
```text
Spellblaze Scar
```
译文：
```text
魔法大爆炸伤痕
```

## entry-02601
位置：mod-tome.lua:34884；section：mod-tome/data/timed_effects/floor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The target is near a spellblaze scar, granting +25% spell critical chance, +10% fire and blight damage but critical spells will drain arcane forces.
```
译文：
```text
目标接近魔法大爆炸伤痕，获得 25%法术暴击率，增加 10%火焰和枯萎伤害，但是法术暴击会消耗法力值。
```

## entry-02602
位置：mod-tome.lua:34886；section：mod-tome/data/timed_effects/floor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The target is walking on blighted soil, reducing diseases resistance by 60% and giving all attacks a 40% chance to infect the target with a random disease (can only happen once per turn).
```
译文：
```text
目标行走在荒芜之地上，减少 60%疾病抵抗并且对目标的所有攻击有 40%的几率使其感染某种疾病（每回合只能触发一次）。
```

## entry-02603
位置：mod-tome.lua:34892；section：mod-tome/data/timed_effects/floor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is near an antimagic bush, granting +20%% nature damage, +20%% nature resistance penetration and -%d spellpower.
```
译文：
```text
目标靠近反魔灌木，增加 20%% 自然伤害，20%% 自然抗性穿透。同时 -%d 法术强度。
```

## entry-02604
位置：mod-tome.lua:34914；section：mod-tome/data/timed_effects/magical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target has been splashed with acid, reducing armour by %d%% (#RED#%d#LAST#).
```
译文：
```text
目标被酸液覆盖，护甲减少 %d%%（#RED#%d#LAST#）。
```

## entry-02605
位置：mod-tome.lua:34935；section：mod-tome/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# turns to #GREY#STONE#LAST#!
```
译文：
```text
#Target#变成了#GREY#石头#LAST#！
```

## entry-02606
位置：mod-tome.lua:34980；section：mod-tome/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# summons a storm to protect them!
```
译文：
```text
#Target#召唤风暴来保护自己！
```

## entry-02607
位置：mod-tome.lua:34985；section：mod-tome/data/timed_effects/magical.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#BLUE##Target#'s stormshield is out of charges and dissipates!#LAST#.
```
译文：
```text
#BLUE##Target#的风暴护盾超过吸收次数而消失了！#LAST#。
```

## entry-02608
位置：mod-tome.lua:34998；section：mod-tome/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s is no longer being purged.
```
译文：
```text
#Target#不再被净化。
```

## entry-02609
位置：mod-tome.lua:35003；section：mod-tome/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Improves senses, allowing the detection of unseen things.
```
译文：
```text
强化感知，可以看到看不到的东西。
```

## entry-02610
位置：mod-tome.lua:35018；section：mod-tome/data/timed_effects/magical.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is confused, acting randomly (chance %d%%), unable to perform complex actions and takes %0.2f darkness damage per turn.
```
译文：
```text
目标处于混乱，随机行动 (%d%% 几率)，不能完成复杂的动作，每回合受到 %0.2f 暗影伤害。
```

## entry-02611
位置：mod-tome.lua:35042；section：mod-tome/data/timed_effects/magical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
An Arcane Eye has seen this creature.
```
译文：
```text
一个奥术之眼正在观察着这个生物。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Brawler	格斗家	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dwarf	矮人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Ghoulish Leap	定向跳跃	T.GAME.TALENT	talents	talent name	existing	core	
Gnaw	啃噬	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼近战技能及召唤物能力；与技能描述中的啃咬动作保持一致
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Island of Rel	瑞尔岛	T.PN.PLACE	places	_t	preferred	core	核心地点专名；统一世界地图、通道入口及夺心魔相关叙述
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Marauder	掠夺者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Mindslayer	心灵杀手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Oozemancer	软泥使	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Solipsist	织梦者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Stone Warden	岩石守卫	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Wayist	维网信徒	T.PN.FACTION	society	_t	preferred	core	遵循维网（The Way）的夺心魔；与 The Way=维网 对应
Wilder	野性系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Yeek	夺心魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
age of pyre	烈火纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	global	1.8beta 的统一译法；替换“派尔纪”
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
dwarf	矮人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
inscriptions	刻印	T.GAME.TALENT_CATEGORY	talents	talent category	preferred	global	统一核心和兽人战役的技能类别译法；具体类型仍使用“纹身/符文”
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
thuggery	暴徒手段	T.GAME.TALENT	talents	talent type	preferred	core	以头槌、暴力抗性、恶毒打击和不择手段为主题的技能树类别；与 assassination“暗杀”区分，叙述语境可按句义译作“暴力”
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
