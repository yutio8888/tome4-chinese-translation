# batch-098：32 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03292
位置：mod-tome.lua:42861；section：mod-tome/dialogs/orders/Talents.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Enter the talent weight multiplier
```
译文：
```text
输入技能权重乘数
```

## entry-03293
位置：mod-tome.lua:42862；section：mod-tome/dialogs/orders/Talents.lua；source_tag：_t；args_order：None；special：None

原文：
```text
0 is off, 1 is normal
```
译文：
```text
0 表示不使用这个技能，1 为默认
```

## entry-03294
位置：mod-tome.lua:42950；section：mod-tome/dialogs/shimmer/ShimmerRemoveSustains.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##CRIMSON#WARNING: this is an EXPERIMENTAL feature. It may explode!#LAST##{normal}#
Sustains auras with name in #YELLOW#yellow#LAST# can not be automatically turned back on if disabled. After turning them on here, you need to unsustain and resustain them manually.

#{bold}#This is a purely cosmetic change.#{normal}#
```
译文：
```text
#{bold}##CRIMSON#警告：这是一项实验性功能。它随时可能出现问题！#LAST##{normal}#
名称显示为#YELLOW#黄色#LAST#的持续技能光环，如果被禁用，将无法自动重新开启。在你在这里调整之后，需要手动先关闭再重新启用这些持续技能。

#{bold}#这个改变只会带来视觉上的变化。#{normal}#
```

## entry-03295
位置：mod-tome.lua:43048；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Arcane Combat
```
译文：
```text
奥术格斗
```

## entry-03296
位置：mod-tome.lua:43049；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You may select a spell for Arcane Combat to automatically trigger with melee attacks.  Otherwise, select 'Random spells' to have a spell selected automatically with each attack.

```
译文：
```text
你可以选择一项法术，在奥术格斗中进行近战攻击时自动施放。如果你选择随机法术，每次攻击时会随机施放一个法术。

```

## entry-03297
位置：mod-tome.lua:43054；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Each time Arcane Combat is triggered, a random allowed spell will be used.
```
译文：
```text
每当奥术格斗触发的时候，会施放一个随机可用的法术。
```

## entry-03298
位置：mod-tome.lua:43056；section：mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
All known spells that can be used with Arcane Combat.
```
译文：
```text
所有已学会的可用于奥术格斗的法术。
```

## entry-03299
位置：mod-tome.lua:43067；section：mod-tome/init.lua；source_tag：init.lua description；args_order：None；special：None

原文：
```text
Welcome to Maj'Eyal.

This is the Age of Ascendancy. After over ten thousand years of strife, pain and chaos the known world is at last at relative peace.
The last effects of the #FF0000#Spellblaze#WHITE# have been tamed. The land slowly heals itself and the civilisations rebuild themselves after the Age of Pyre.

It has been one hundred and twenty-two years since the Allied Kingdoms were established under the rule of #14fffc#Toknor#ffffff# and his wife #14fffc#Mirvenia#ffffff#.
Together they ruled the kingdoms with fairness and brought prosperity to both Halflings and Humans.
The King died of old age fourteen years ago, and his son #14fffc#Tolak#ffffff# is now King.

The Elven kingdoms are quiet. The Shaloren Elves in their home of Elvala are trying to make the world forget about their role in the Spellblaze and are living happy lives under the leadership of #14fffc#Aranion Gayaeil#ffffff#.
The Thaloren Elves keep to their ancient tradition of living in the woods, ruled as always by #14fffc#Nessilla Tantaelen#ffffff# the wise.

The Dwarves of the Iron Throne have maintained a careful trade relationship with the Allied Kingdoms for nearly one hundred years, yet not much is known about them, not even their leader's name.

While the people of Maj'Eyal know that the mages helped put an end to the terrors of the Spellblaze, they also did not forget that it was magic that started those events. As such, mages are still shunned from society, if not outright hunted down.
Still, this is a golden age. Civilisations are healing the wounds of thousands of years of conflict, and the Humans and the Halflings have made a lasting peace.

You are an adventurer, set out to discover wonders, explore old places, and venture into the unknown for wealth and glory.

```
译文：
```text
欢迎来到马基·埃亚尔的世界！

现在的埃亚尔大陆是卓越纪。在长达一万年的冲突痛苦和混乱之后，我们所知的世界终于进入了一个相对和平的时期。
#FF0000#“魔法大爆炸”#WHITE#所造成的影响已经渐渐减轻。烈火纪之后，大地慢慢自愈，各个文明也纷纷开始重建家园。

自联合王国在#14fffc#图库纳#ffffff#与其妻#14fffc#米雯尼雅#ffffff#的统治下建立，至今已有一百二十二年。
在他们的统治下，王国天下太平，无论是人类还是半身人的居住地都欣欣向荣，一片繁华。
十四年前，国王因年纪过大而去世了，他的儿子，#14fffc#托拉克#ffffff#继承了王位。

精灵们的王国安详而平和。住在埃尔瓦拉的永恒精灵们试图让世界忘记他们在魔法大爆炸中扮演的角色，在精灵王#14fffc#艾伦尼恩·加威尔#ffffff#的统治下快乐地生活着。
而自然精灵则遵从古老的传统，住在森林当中，一如既往地由贤者#14fffc#奈希拉·坦泰兰#ffffff#统领。

近一百年来，钢铁王座的矮人们一直小心谨慎地与联合王国维持着贸易往来，但外界对这个种族所知甚少，甚至不知道他们的统治者是谁。

尽管马基·埃亚尔大陆上的居民都知道是魔法师们帮忙终止了恐怖的魔法大爆炸，但他们也没有忘记正是魔法本身造成了这场灾难。因此法师们至今仍遭社会排斥，甚至被公开猎杀。
无论如何，这是个黄金时代，所有的文明在过去数千年中经历的不幸正在好转，甚至人类和半身人之间已经形成了长久的和平。

你是一名冒险者，去见识奇观、探索古迹，为财富与荣耀踏入未知之地。

```

## entry-03300
位置：mod-tome.lua:43106；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Stunning an opponent slows down their movement and reduces their damage output, giving you the opportunity to tactically reposition or finish them off at less risk.
```
译文：
```text
震慑可以减缓目标的移动速度，降低其伤害输出，为你制造机会重新占位，或以更低的风险将其解决。
```

## entry-03301
位置：mod-tome.lua:43108；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
In the Age of Pyre the orcs learned the secrets of magic, and with their newfound powers nearly overcame the whole of Maj'Eyal.
```
译文：
```text
在烈火纪，兽人掌握了魔法的奥秘，凭借新获得的力量几乎征服了整个马基·埃亚尔。
```

## entry-03302
位置：mod-tome.lua:43109；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
The orcs once terrorised the whole continent. In the Age of Ascendancy they were rendered extinct, but rumours abound of hidden groups biding their time to return.
```
译文：
```text
兽人曾经给整个大陆带来了一场浩劫。在卓越纪，他们已被彻底灭绝，但传言四起，仍有隐匿的团体在蛰伏待机，伺机卷土重来。
```

## entry-03303
位置：mod-tome.lua:43111；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Alchemists can transmute gems to create fiery explosions, and are known to travel with a sturdy golem for extra protection.
```
译文：
```text
炼金术士可以转化宝石制造炽烈的爆炸，并且往往带着一尊坚固的傀儡随行以获得额外保护。
```

## entry-03305
位置：mod-tome.lua:43115；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Who knows what dark thoughts drive people to necromancy? Its art is as old as magic itself, and its creations have plagued all the races since the earliest memories.
```
译文：
```text
天知道是怎样的堕落思想才能使一个人成为死灵法师。这门艺术就像魔法一样历史悠久，它的造物自最早的记忆以来就一直困扰着所有种族。
```

## entry-03306
位置：mod-tome.lua:43118；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
"The Spellblaze tore Eyal apart and nearly brought about the end of all civilisation. Two thousand years on its shadow still hangs over many lands, and the prideful mages have never been forgiven their place in bringing it about.
```
译文：
```text
魔法大爆炸撕裂了埃亚尔大陆，整个文明差点被彻底摧毁。两千年岁月已过，爆炸的阴影依然笼罩着很多地区。而那些高傲的法师们，也从未因其在促成此事中所扮演的角色而获得宽恕。
```

## entry-03307
位置：mod-tome.lua:43119；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Some are cursed with mental powers beyond their full control, turning them to a dark life powered by hatred.
```
译文：
```text
某些人被诅咒，获得了超出自身完全掌控的精神力量，从此堕入由仇恨驱动的黑暗生涯。
```

## entry-03308
位置：mod-tome.lua:43120；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Dreadfell has always been shunned for its haunted crypts, but of late rumours tell of a darker and more terrible power in residence.
```
译文：
```text
恐惧王座一直以来都因其闹鬼的地宫而为人所避讳，但最近有流言传出，此地盘踞着一股更加黑暗可怖的力量。
```

## entry-03309
位置：mod-tome.lua:43121；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.
```
译文：
```text
虽然有人说还能在某些隐秘之地找到夏·图尔的神器，但据说不可轻慢它们。
```

## entry-03310
位置：mod-tome.lua:43124；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Arcane Blades employ a fusion of melee and magical combat. Their training is harsh but the most dedicated rise to great powers.
```
译文：
```text
奥术之刃是一个混合了魔法与近战的职业。他们的训练非常严酷，但最为投入者终能获得强大的力量。
```

## entry-03311
位置：mod-tome.lua:43136；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Trolls were once seen as little more than beasts or pests, but the orcs trained them up for use in war and they became much more intelligent and fearsome.
```
译文：
```text
巨魔从前不过被视作与野兽或害虫无异的东西，不过后来兽人因为战争的需要对它们加以训练，如今它们变得聪明得多，也可怕得多。
```

## entry-03312
位置：mod-tome.lua:43137；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Some say that the foot of a halfling is lucky to own. Halflings do not take well to those who enquire too forcefully.
```
译文：
```text
有人说拥有一只半身人的脚能带来好运。半身人可不待见那些打听得太起劲的家伙。
```

## entry-03313
位置：mod-tome.lua:43142；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Alchemists can bind gems to armour to grant them magical effects, to protect the wearer or improve their powers. Some commercial alchemists can imbue gems into jewellery.
```
译文：
```text
炼金术士可以把宝石镶嵌到盔甲上，赋予其魔法效果，以保护穿戴者或增强其能力。一些提供商业服务的炼金术士还能把宝石镶嵌到首饰中。
```

## entry-03314
位置：mod-tome.lua:43163；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Brawlers are trained in the use of their fists and mastery of their bodies. They can be as dangerous in combat as any swordsman.
```
译文：
```text
格斗家受过双拳运用与身体掌控的训练。他们在战斗中的杀伤力不亚于任何一个持剑的战士。
```

## entry-03315
位置：mod-tome.lua:43164；section：mod-tome/init.lua；source_tag：init.lua load_tips；args_order：None；special：None

原文：
```text
Lightning is a chaotic element that is hard to control. It is said that those most attuned to it are eventually driven insane.
```
译文：
```text
雷电是一种混沌的元素力量，难以操控。据说与之最为亲和者最终都会陷入疯狂。
```

## entry-03316
位置：mod-tome.lua:43184；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A cloak can simply keep you warm or grant you wondrous powers should you find a magical one.
```
译文：
```text
斗篷可以让你保持温暖，而一些魔法斗篷可以给你神奇的力量。
```

## entry-03317
位置：mod-tome.lua:43192；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Sandals or boots can be worn on your feet.
```
译文：
```text
你的脚上可以穿上鞋子。
```

## entry-03318
位置：mod-tome.lua:43196；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your readied ammo.
```
译文：
```text
你准备好的弹药。
```

## entry-03319
位置：mod-tome.lua:43200；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weapon Set 2: Most weapons are wielded in the main hand. Press 'x' to switch weapon sets.
```
译文：
```text
第二套武器：大部分武器使用主手抓握。按 X 键切换武器套。
```

## entry-03320
位置：mod-tome.lua:43202；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weapon Set 2: You can use shields or a second weapon in your off-hand, if you have the talents for it. Press 'x' to switch weapon sets.
```
译文：
```text
第二套武器：如果你有对应的技能，你可以副手使用盾牌或第二把武器。按 X 键切换武器套。
```

## entry-03321
位置：mod-tome.lua:43204；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Weapon Set 2: Object held in your telekinetic grasp. It can be a weapon or some other item to provide a benefit to your psionic powers. Press 'x' to switch weapon sets.
```
译文：
```text
第二套武器：使用你的念动力抓取的物品。你可以抓取武器，或者抓取其他物品来为你的心灵力量提供增益。按 X 键切换武器套。
```

## entry-03322
位置：mod-tome.lua:43208；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
List of items that can be instantly used by swift hands.
```
译文：
```text
无影手可即时使用（不消耗回合）的物品列表。
```

## entry-03323
位置：mod-tome.lua:43240；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I begin my writings with a study of the humans, currently the most populous of the races in Maj'Eyal. The greatest kingdom in number are by far the Cornacs, but mention should also be made of the Sholtar and Mardrop kingdoms, and the Higher bloodline. The biggest human population centre is around the citadel of Last Hope, though many other settlements exist across all corners of Maj'Eyal.

 Cornacs are normally around 5'9", with generally dark hair, brown eyes and ruddy features. Most Cornacs take up roles as tradesmen, farmers, or other manual labour jobs. It is a sad fact that the majority of bandit groups tend to be dominated by Cornacs. Cornac families tend to be large, and since the Age of Dusk their population has expanded rapidly, especially in the farming lands in the west and around Last Hope in the south.

 Sholtar are generally 5'11", with dark skin, hair and eyes. They originate from the south-east of Maj'Eyal, and are few in number since the Cataclysm tore much of their land into the sea. Their affinity with nature is renowned, and they are often found employed as healers, infusion crafters or wyrmic huntsmen.

 Mardrop humans are all but extinct, after the Spellhunt and the plagues during the Age of Dusk. They were known to be powerful spellcasters, and as such were prime targets by the spellhunters. However some trace of them can still be found, as their fiery hair and freckled skin oft can appear in those of distant descent. A few are rumoured to still possess citadels and towers in remote locations.

 Highers are on average 6'0", with fair hair and skin and blue or grey eyes. The majority of scholarly roles are taken up by Highers, and they tend to fill most of the noble classes. Some say this is due to discrimination and elitism, though these may simply be jealous sentiments. There are also rumours that the superior intellects of Highers are due to arcane experiments instigated by the ancient Conclave during the Age of Allure, but I have found no records to support this idea and must consider it to be baseless. The Higher bloodline is renowned as a mark of excellence, and mixing with lower bloods is strongly frowned upon.

 All human kingdoms were united by King Toknor the Brave in the Age of Pyre, and remain under the rule of his son King Tolak the Fair. A full discussion of the long human history would require a far more detailed document.
```
译文：
```text
我从人类的研究开始，他们目前是马基·埃亚尔人口最多的种族。若论人口数量，科纳克王国远超其他人类王国。此外，肖尔塔王国和马卓普王国以及高等人类这一血统支系也值得一提。最大的人类聚居地在最后的希望要塞周围，另外还有许多聚居地存在于马基·埃亚尔的每个角落。

 科纳克人基本身高在5英尺9英寸左右，有着黑色的头发、棕色的眼睛以及红润的肌肤。大多数科纳克人选择商人、农民或者其他体力劳动职业。不幸的是，大部分强盗组织也更倾向于被科纳克人控制。科纳克人的家族很庞大，并且自黄昏纪以来他们的人口增长极快，特别是在西部农业地区和南部的最后的希望一带，这种现象尤为明显。

 肖尔塔人基本身高在5英尺11英寸左右，黑皮肤黑头发黑眼睛。他们起源于马基·埃亚尔的东南地区，自从大爆炸将他们大部分土地沉入海洋后，他们的数量急剧减少。他们以自然亲和著称，并且经常作为治疗师、注能物工匠或龙战士猎手行走于世。

 在黄昏纪的魔法狩猎与瘟疫之后，马卓普人几乎灭绝。他们以强大的施法者著称，也因此成为猎魔者的首要目标。不管怎样，他们的血统特征——火红的头发以及生有雀斑的皮肤，仍会出现在血缘疏远的后裔身上。有部分传言说他们仍住在某些遥远的地方的城堡或高塔里。

 高等人类基本身高在6英尺左右，有着金色的头发、白皙的皮肤和蓝色或灰色的眼睛。大多数学者都是高等人类，贵族阶层也大多由他们占据。有人说这都是歧视和精英理论所导致的，虽然这可能只是简单的嫉妒情绪。也有传言说高等人类的高智商是厄流纪时期秘法会法师们的实验成果，但是我找不到任何证据来支持这一论点，我只能认为这种说法毫无根据。高等人类的血统被认为是优秀的标志，与低等血统通婚则为世所不齿。

 在烈火纪，勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子公正之王托拉克的手中。一份关于人类漫长历史的全面报告需要更加详细的文本来叙述。
```

## entry-03324
位置：mod-tome.lua:43261；section：mod-tome/load.lua；source_tag：_t；args_order：None；special：None

原文：
```text
No text would be complete without at least a brief note of some of the more brutish races which infest our world. These do not hold any civilised society of note, nor in general do they seem capable of any form of higher thought or culture, but they are still of interest to study for any who take delight in analysing beings of more primitive intellect.

 Trolls come in two main types - Kezrak and Moltep, or stone and forest trolls as they are colloquially known. Stone trolls infest many mountain chains to the north-east, and some have been known to wander further afield in search of food or to spread violence. They are generally over 8' high, with extremely pronounced muscular strength and a thick, solid hide which bears the appearance of coal or granite. Forest trolls are generally found in dense woods or swamps, with the Trollmire east of Derth being especially infamous. They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons, though their greenish hide is not as thick and their musculature less developed. All trolls have intensely fast metabolisms, capable of healing from grievous wounds within a matter of hours. At birth they measure just eight inches long, but within two years grow to full maturity, and rarely live beyond ten years old. They used to be considered little more than beasts, but towards the end of the Age of Pyre many were trained as fighters by the orcs, and were even taught the basics of language and certain battle tactics, making them much more dangerous. Though the orcs are gone their servants remain, and their remote breeding areas and intense birth rates have so far scampered attempts to eradicate them completely.

 Giants live mostly around the mountainous peaks surrounding the Daikara Pass. They vary greatly in size, but are normally at least 10' tall. They look somewhat like large, deformed humans, with swollen or distended facial features and much longer, swinging limbs. They live in nomadic tribes, moving from peak to peak with the seasons, feeding on wild deer and goats. They are usually peaceful creatures, only turning violent when their territory is encroached or their young are threatened. There are sometimes reports of giants coming to lowlands and stealing farm animals or attacking communities, but these are rare and normally isolated to particularly harsh winters. Giants seem to have no developed culture or language worth mentioning, but have been noted to show interactions of limited intelligence and to commune well in groups.

 Nagas were once believed to be mere myth, but reliable reports and even the capturing of dead physical samples has shown them to be real creatures. The upper half of their body is humanoid in form, with blonde hair and an extremely thin build, but the lower half is like that of a giant snake's tail. They stand around 6' tall on land, though their tails extend several feet further. They have been encountered off the eastern and south-eastern coasts of Maj'Eyal, which seems to indicate some exotic civilisation beneath the waves. Records of them exist only from the last few hundred years, and only more recently have they been interpreted as more than just the wild fantasies of inebriated sailors. They can breathe in air and underwater, possessing both lungs and gills, and have been reported to move with surprising speed on the ground. One might think them simply odd monsters, but they decorate themselves in jewellry and craft weapons and armour from materials found on the sea-bed, such as supple mail formed from layers of thick shark-hide. This would suggest an advanced culture, but communication with them so far has proved impossible. It is not known if they are capable of complex speech, but to date their only response to those who encounter them has been extreme violence, and fishermen in the east are always wary of coming across these vicious creatures.

 The origin of Demons is not wholly known, but it is clear that they are capable of intelligence and so I feel the need to describe them somewhat here. It is known that they can be summoned by certain magical rites, and minor demons were oft in the employ of evil sorcerers during the Age of Dusk. The main theory, which is supported by certain studies by Shaloren archmages, seems to indicate that they come from another world than our own, with connections formed through intense arcane energies. It must be a truly terrifying place to host such foul denizens. Demons vary immensely in appearance and power, as much as the creatures of our own world vary. They generally have blueish blood and metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness. All seem versed in magical abilities to some degree, and the strongest of them possess truly terrifying powers. Luckily they are exceptionally rare, and seem to be much less common in modern times since magic has fallen out of use.
```
译文：
```text
没有任何文字可以诠释那些影响我们世界的野蛮种族。他们没有任何文化遗留，也没有任何先进的智慧或文化，但是他们仍能激起大家研究原始种族的兴趣。

 巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。岩石巨魔生存与东北部的山脉地区，有些为了寻找食物和散播暴力甚至走到了更远的地方。他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。森林巨魔生活在浓密的森林和沼泽中，在德斯镇东部的巨魔沼泽尤为臭名卓著。他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速和能够使用精工武器闻名，尽管他们泛绿的外皮没有那么厚实，肌肉也不如岩石巨魔发达。所有的巨魔有着快速的新陈代谢能力，再严重的伤口，恢复只要几个小时。据测量，他们在出生时只有8英寸长，但是在2年内他们就可以成长完全，并且很少有寿命超过10年的。他们一开始被认为仅比野兽好一点，然而在烈火纪时，他们被兽人当做战士般训练，甚至学习了一些基础语言和战术，使得他们更加危险。虽然兽人已经走了，但他们的仆人仍然存在，并且他们偏远的繁殖地和极高的出生率至今仍挫败着彻底根除他们的企图。

 巨人们通常住在岱卡拉周围的山峦中。他们在体型上有着很大的差异，但基本上不会低于10英尺高。他们看起来就像是具有浮肿面部特征和更长的四肢的放大人类。他们属于游牧部落，随着季节的变化，从一个山头迁移到另一个山头，以鹿和羊为食。他们通常是和善的生物，只有当他们的领土受到入侵或者他们的后辈受到威胁时才会变的具有攻击性。有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击市民，但是这极其少见并且大多发生在极端的严冬。巨人们似乎没有值得一提的优越文化和语言，但是却向我们揭示了有限智慧的运用和团结一致的精神。

 娜迦曾被认为仅存于神话中，但是据可靠消息以及死亡的标本表明他们是真实存在的。他们的上半身是人形，有着金色的头发和苗条的身段，但是下半身却极像一只巨蛇的尾巴。他们大约身高6英尺，尽管他们的尾巴可能更长。他们在马基·埃亚尔的东岸和东南岸都有踪迹，这似乎表明波涛之下存在着某种异域文明。有关他们的记载只有近一百年的，并且越来越多的证据表明他们并不是喝醉水手们的幻觉。他们可以在水里和陆地上呼吸，同时拥有肺和鳃，并且据说在陆地上有着非常惊人的速度。有人可能认为它们只是特殊的怪物，但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。现在还不知道他们是否有复杂的语言，但是他们目前的对外回复只是极端的暴力，并且东海的渔民们经常要提防碰上这些邪恶的生物。

 恶魔的起源尚未完全清楚，但是很显然他们具有某种智慧，所以我觉得有必要在此写下一段。众所周知，他们是由某种魔法仪式召唤而来，并且在黄昏纪时期，小恶魔们经常受雇于邪恶的巫师。最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。那必然是一个地狱般的地方才能容下如此多恐怖的生物。恶魔们在外观和能力上不尽相同，正如我们世界里的生物一样。他们通常有偏蓝的血液和金属化的血肉，可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中。他们似乎都在某种程度上通晓魔法，并且他们之中最强者具有真正可怕的力量。幸运的是他们是非常罕见的种族，而且自从魔法淡出人们的视野后，出现的更加稀少了。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Arcane Blade	奥术之刃	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Brawler	格斗家	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Dreadfell	恐惧王座	T.PN.PLACE	places	nil	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Facial features	脸部特征	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Sholtar	肖尔塔	T.PN.PLACE	places	nil	preferred	core	维护者于 2026-08-25 裁定统一为“肖尔塔”；“肖塔尔”和“肖塔”已被取代
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
Trollmire	巨魔沼泽	T.PN.PLACE	places	_t	preferred	core	任务与地点叙述统一；troll 指巨魔，不是食人魔，与 narrative.tsv 的 trollmire→巨魔沼泽 一致；“Of trolls and damp caves”是任务标题，不作同名处理；2026-09-16 用户裁决，由 existing 升为 preferred
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
age of pyre	烈火纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	global	1.8beta 的统一译法；替换“派尔纪”
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
derth	德斯镇	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
iron throne	钢铁王座	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactical	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 tactic 同义的变体
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
trollmire	巨魔沼泽	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	与同类手札标题统一；troll 指巨魔，不是食人魔
unknown	未知	T.UI.LABEL	ui	_t	preferred	global	未知条目/名称占位（15 处）
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
