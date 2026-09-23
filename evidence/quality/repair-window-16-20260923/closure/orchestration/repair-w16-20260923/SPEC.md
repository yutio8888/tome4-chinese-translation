# 修复窗口16：262批7条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线c2043cc40a6e39d3af7c0f92f9e91f7a6d5651e9。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的7个target及evidence/quality/repair-window-16-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/LF/TAB全部保持基线（\t\t 缩进按原文逐行恢复）。专名、技能名、伤害类型沿用本库现有译名（先在mod-tome.lua查证），不自行新造。

7条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 若失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰7个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核263。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 50级祝贺提示（class/Actor.lua:3974）：恢复 congratulations! 后的段间空行（\n\n），“勇敢的向前”用副词“地”；颜色标记保持。
- 星辰契约说明（talents/uber/str.lua:311 起，tformat）：The strength of your bond is so strong 写出“你与它的羁绊之强”一类（羁绊，不是你自身的力量）；光辉引力写明范围内敌人被拉向被击中的目标（celestial/combat.lua:99–104 pull(target.x,target.y,5)），不写成拉向自己；每一行前导缩进恢复为与原文一致的 \t\t（不得用空格）；%% 与 #GOLD#…#LAST# 保持。“埃亚尔大陆”为本库既有用法，本窗口不改。
- 不死猎人指南（lore/fun.lua:213–290，长篇多段）：usually armed and sometimes even armoured（通常持械，有时甚至披甲）；with cold steel 不得增“刺穿喉咙”；Ever fought a snow giant? 不得增“一向被视为力量象征的”；all screaming for your blood to be spilt 为众头颅尖叫着要你流血（不是因果句）；I always receive the same answer 为“总是得到同样的回答”；巫妖段原文是传说不及其可怖（它超越传说），不得写成传说“有所失实”；wild infusion 保持术语“野性纹身”。
- 矮人送药（chats/alchemist-last-hope.lua:405–406，颜色标记与换行保持）：I put a bit of the good stuff in this one 为“我往这瓶里加了点好料”；though it won’t do you any favors tomorrow morning 为“不过明早可有你受的”一类（宿醉），不得写“没什么用”“也许”；Taint of Purging 沿用本库现有译名；wife 句逐句对照。
- 成就说明（achievements/quests.lua:107）：closing the Void portal 为“关闭虚空传送门”，using yourself as a sacrifice 为以自身为祭品。
- 牺牲死讯（chats/sorcerer-end.lua:146/161，tformat）：%s 运行时为反身代词“他自己/她自己”（utils.lua his_her_self），整串嵌入以玩家名为主语的死讯；按同族“牺牲了%s，引来遥远太阳炽烈的怒火”（mod-tome.lua 现有）的句式改为“牺牲了%s，将维网带给众生”一类，保持 %s 恰一个。
- 强化弹药（talents/techniques/munitions.lua:414）：Venomous 的 nature damage 译为“自然伤害”（本库伤害类型统一译名），其余数值、占位符与各行逐句对照。

## f14a476f19489b0f6a79876e7004c6a59a54d9b0e78e967691071d34b66990ed

section: mod-tome/class/Actor.lua
source_tag: _t

source: You have achieved #LIGHT_GREEN#level 50#WHITE#, congratulations!

This level is special, it granted you #LIGHT_GREEN#10#WHITE# more stat points, #LIGHT_GREEN#3#WHITE# more class talent points and #LIGHT_GREEN#3#WHITE# more generic talent points.
Now go forward boldly and triumph!

target: 你达到了#LIGHT_GREEN#等级 50#WHITE#，祝贺你！
这个等级很特殊，你可以得到额外的#LIGHT_GREEN#10#WHITE#点属性点，#LIGHT_GREEN#3#WHITE#点职业技能点和#LIGHT_GREEN#3#WHITE#点通用技能点。
现在，勇敢的向前并取得最终的胜利吧！

确认依据：50 级祝贺提示：原文首句与第二段之间有空行（\n\n），译文只保留一个换行，丢失段间空行；按换行不变量整句修复，其余内容一致。

## f15f5593c718735620a18ddf5948ac4c1b17670950691754aaf89d449e936d16

section: mod-tome/data/talents/uber/str.lua
source_tag: tformat

source: During your studies of celestial forces you came in contact with an entity far beyond Eyal: the living incarnation of a Star!
		By allying yourself with it you can gain its power!

		Grants multiple benefits:
		- The strength of your bond is so strong that you can now #GOLD#wield a two-handed weapon and a shield together#LAST#
		- 50%% of all damage you deal is converted to #GOLD#light damage#LAST#
		- #GOLD#Gravitic Effulgence#LAST#: whenever your Weapon of Light hits the damage is now a radius 2 sphere and all foes in range 5 are drawn to it. (You can toggle this effect)
		- The damage and chance to trigger of #GOLD#Searing Sight#LAST# is doubled
		- Whenever #GOLD#Sun's Vengeance#LAST# triggers the remaining cooldown of Judgement is reduced by 6.
		- If you also know #GOLD#Irresistible Sun#LAST#, it will set the fire and light resistances of those affected to 0%%

		#{italic}##GOLD#Will you bind yourself to the Distant Sun?#{normal}#
		

target: 在研习天体之力时，你接触到了距离埃亚尔大陆极其遥远的存在：一颗恒星的化身！
        与它结盟，你将获得它的力量。

        增益：
        - 你的力量如此强大，你可以#GOLD#同时装备双手武器和盾牌#LAST#
        - 50%% 伤害转化为 #GOLD#光系伤害#LAST#
        - #GOLD#光辉引力#LAST#：光明之刃变成半径2的球形伤害，且可以将5格范围内的敌人拉过来（你可以开关此效果）。
		- #GOLD#灼热之视#LAST# 的伤害和触发概率翻倍
        - #GOLD#阳光之怒#LAST# 触发时，裁决的剩余冷却时间减少6回合。
        - 若你也习得 #GOLD#无御之日#LAST#，它将使受影响者的光系和火焰伤害抗性降低为 0%%

		#{italic}##GOLD#你会同遥远的太阳联合吗？#{normal}#
		

确认依据：星辰契约说明（tformat）：The strength of your bond is so strong 指与恒星化身的羁绊之强使你能同持双手武器与盾，现译“你的力量如此强大”丢失 bond 且改变因由；另多行前导 \t\t 被改成 8 个空格而其余行保留 \t\t，缩进不一致。整条对照修复，恢复与原文一致的 \t\t。
与 surface 同向：星辰契约说明 The strength of your bond 被译成“你的力量”，丢失与恒星化身的羁绊。宿主另核 celestial/combat.lua:99–104：光辉引力以被击中目标为中心收集半径 5 内敌人并 pull(target.x,target.y,5)，即拉向被击中的目标；现译“将5格范围内的敌人拉过来”易读作拉向施法者，一并明确。Eyal=“埃亚尔大陆”为本库既有用法（23 处），不在本条改动范围。整条修复，恢复 \t\t 缩进。

## f18f9a4e901a0f5c2e93872aacc75f8e8a9fef72f107cad5788e3bd5c4ee5c8c

section: mod-tome/data/lore/fun.lua
source_tag: _t

source: #{italic}#An undead hunter's guide, by Aslabor Borys#{normal}#

So, apparently I'm a legend now. Hah, knock a vampire's head off with a greatmaul and suddenly you're up there with Toknor and Mirvenia apparently. More and more often these days I get novice adventurers coming up to me, asking me for advice when it comes to battling the undead. My first instinct was to tell them to get back home and become bakers or gardeners or something. If they need crib notes for combat they obviously aren't cut out for it.

But then I was thinking, these are good kids. Heck, I'd buy every man and woman in the world who's bumped off a ghoul a free drink if I could. If they want help when it comes to putting down necromancer slime and their chilling creations, I would be more than happy to oblige. Not much of a writer, but let's see. First...

#{bold}#1. Ghouls#{normal}#

Every once in a while, people come to me and say "Are all necromancers truly evil?" "Surely necromancy could be used for good!" "Isn't it wrong to discriminate against others simply because of the magicks they practice?" To these people, the first thing I usually say - shortly after giving them a black eye - is to take a look at a ghoul. Take a good, long look. Take in the diseased, putrescent flesh. Take in the oozing, exposed organs. Take in its features, slowly rotting to mulch. It used to be a person. It used to have a family, people who loved it. Now it's a walking corpse, its only desire being death and the mad, all-encompassing consumption of living flesh. Are all necromancers truly evil? A thousand times, yes.

Even this most basic of undead minions can strike terror into the unprepared. The multitude of diseases that a normal ghoul carries are contagious in a manner many adventurers do not truly appreciate until they see the sores and necrosis visibly spreading up their arm from where a ghoul bit them. Such maladies must be dealt with promptly: if bitten by a ghoul, immediately plunge the afflicted area in scalding hot water, then wrap it quickly in clean cloth lined with mugwort and quartz powder. The wound must remain dressed for three weeks, with new dressings applied every four days, and make sure to burn the old ones! Failing the above, a wild infusion also works splendidly.

    * * *


#{bold}#2. Skeletons#{normal}#

What guide to the undead would be complete without mentioning the humble skeleton? Despite these clattering and chittering bones of the deceased often looking so fragile that a stiff breeze could break them apart, in many ways they are more dangerous than their ghoul cousins.

With no masses of rotted and ruined flesh to reanimate, necromancers can commit themselves fully to bestowing some level of fighting skill on a reanimated skeleton, and since a fighter's weapons will often last as long as his bones will, skeletons are usually armed and sometimes even armoured. The potential skill of a skeleton doesn't stop at melee weapons either - fallen archers take up their bows once again, and although difficult by comparison, some necromancers can even grant dead mages their magic powers once again.

Some adventurers find themselves baffled when it comes to fighting skeletons. How do you destroy a foe who, by all rights, should be destroyed already? To these adventurers, I say take heart. The more broken and incomplete a body is, the more effort it takes to keep it reanimated. As most necromancers see skeletons as the lowest of low peons, you can expect a few good blows to easily dissipate the minimal effort their masters put into creating them.

    * * *


#{bold}#3. Wights#{normal}#

Wights are an odd duck amongst the undead, often not created by necromancers specifically, but instead rising of their own volition when the conditions are right. Wights are by no means individual souls, but often part of a gestalt; when a particular land has seen enough bloodshed - battlefields, forest, crypts and graveyards - wights can be seen to rise en masse, a near-physical representation of the battles and turmoil the land has faced. Sadly, it is for this reason that necromancers often facilitate the creation of wights regardless, for no other study or profession causes so much blood or death.

Those who have had encounters with wights often describe them as indistinct skeletal figures, wrapped in flowing cloaks that become faded and incorporeal at their edges, while strange lights dance where their eyes should remain. Survivors tell of a peculiar sense of exhaustion when in close proximity to them, as though merely being close to these figments of death causes one's life force to sputter and fade. Regardless of this and their ghostly appearance however, it has been recorded that steel and strength of arms is yet enough to destroy them, or at least to erase them for the time being. It's just a shame that such battles are likely to simply create more of them in the long run...

    * * *


#{bold}#4. Vampires#{normal}#

Vampires are so far removed from other varieties of undead it seems almost unreal. What grants them their longevity? How do they retain such great intelligence? Beyond their sallow complexion and drawn features, why do they not decay and decompose as their ghoulish siblings do? The study of vampiric nature is one long list of unanswered questions, each new study adding yet more to the ever-growing pile.

As said before, a vampire's greatest strength is its resemblance to a living man, both in mind and body. Thanks to this, vampires are known for residing comparatively close to normal towns and villages far more than other undead. Some have even been known to keep their lairs within these communities themselves! Despite their resemblance however, there are many telltale signs of vampirism: Unnaturally pale skin, long and distinctive fangs, an aversion to sunlight, and much more besides. In an effort to avoid close inspection, some vampires are known to masquerade as men of wealth, often cloistering themselves in remote locations to discourage prying eyes.

But perhaps the most astonishing thing regarding vampires is their propensity for alliance and familial relationships. No other undead being even approaches matching the incomprehensible tangle of clans, broods, families and bloodkin that vampires create for themselves. It is for this reason that vampires often end up becoming rulers of lesser undead themselves, commanding them as a normal necromancer would. So, in turn, treat them as you would a necromancer - with cold steel.

    * * *


#{bold}#5. Spirits#{normal}#

During my travels, I have noticed that some communities in the wild no longer bury their deceased as is the norm in larger settlements. Some folk burn the corpses of their fallen, committing their ashes to the earth instead. When asked why they perform this peculiar practice, I always receive the same answer: Necromancers. Fearful of their dead rising up to slay them at the whims of delusional, murderous filth, they believe that with the burning of the dead, their spirits are forever beyond the reach of a necromancer's bony fingers.

Alas, this is not true. While fire may burn away a man's physical being, no flame can touch his spirit. Unfortunately, necromancers can. Bereft of both body and freedom, many souls are driven mad in the employ of necromancers, ceaselessly drifting through windswept crypts, harrying any unfortunate wanderers they encounter with a multitude of curses and hexes. Worst of all are those spirits who embrace their newfound purpose, causing them to grow in power at a frightening rate. No other being in Maj'Eyal is so obviously abhorrent to existence itself as these "dreads"; it is almost as though creation itself wants these beings gone from her world. It is my hope that you, and many others, oblige her wish.

    * * *


#{bold}#6. Bone Giants#{normal}#

One of the most horrific, vomit-inducing expressions of the necromancer's so-called "art" is the bone giant. Not content with merely profaning the bodies of singular souls, some ambitious necromancers work to bind the bodies of countless skeletons together, creating hideous engines of destruction that can stand many times higher than the height of a normal man.

It is a deadly mistake to liken these abominations to the golems alchemists and archmages employ. Wilful and fey as they are, normal mages often only craft golems for utility and their own protection, while necromancers create bone giants for the sole purpose of dealing death, and the only limit to their destructive capability is the necromancer's twisted imagination. Ever fought a snow giant? Imagine one with six arms and fingers like blades, wrought of sharpened ribs. Imagine one with countless skulls lining every inch of its wretched body, all screaming for your blood to be spilt as it thrashes spinal columns like whips from its disfigured hands! After facing one of these grotesque amalgamations, you'll be begging to go back to the Daikara to pick on simple, frost-rimed sub-men.

    * * *


#{bold}#7. Liches#{normal}#

Hate made flesh. Evil made pure. Death incarnate. The culmination of a necromancer's work. Whatever you know liches as, I can tell you that they do not match the countless myths and legends that surround their terrible figures. They surpass them.

Once a powerful necromancer finally crosses the border between life and death, the abyssal power that they could only initially grasp in dribs and drabs becomes theirs to control totally. It is often said that unexpected quakes, crops failing, and the leaves simultaneously falling from the trees heralds the birth of a lich. Lords of the undead, liches can annihilate ghouls and skeletons, banish dreads with a glance, and reduce bone giants to powder within moments.

As to how to actually destroy one? Well, tell you what. If you manage to defeat one of these abominations, be a dear and write a guide for me, for I have absolutely, positively, no idea.

    * * *

target: #{italic}#一名不死猎人的指南 作者：阿斯拉伯·波利斯#{normal}#

这么说，我如今也成传奇人物了。哈，不过是用大槌敲掉一个吸血鬼的脑袋，转眼就有人把我和图库纳、米雯尼雅相提并论。最近越来越多的新手冒险者跑来问我，该怎样对付不死生物。我的第一反应，是叫他们回家当面包师、园丁，随便做点别的。打架还得看小抄，显然就不是这块料。

不过转念一想，这些孩子都不坏。见到世上任何一个干掉过食尸鬼的男人或女人，我都乐意请上一杯。要是他们需要帮忙收拾死灵法师那帮渣滓和他们阴森森的造物，我当然愿意效劳。我不太会写东西，不过试试看吧。首先……

#{bold}#1、食尸鬼#{normal}#

时不时有人来问我：“所有死灵法师真的都邪恶吗？”“死灵法术难道不能用于善事？”“仅仅因为别人修习某种魔法就歧视他们，难道不是错的吗？”对这些人，我通常先赏一只乌眼青，然后叫他们好好看看食尸鬼。仔仔细细看个够：染病腐败的血肉，裸露在外、不断渗液的脏器，还有渐渐烂成泥浆的面孔。它从前也是个人，也曾有家庭，有爱它的人。如今却成了一具行尸走肉，唯一的欲望就是死亡，以及疯狂地吞噬一切活人的血肉。所有死灵法师真的都邪恶吗？千真万确，是。

即使是这种最基础的不死仆从，也足以让毫无准备的人胆寒。普通食尸鬼携带的多种疾病极易传染；许多冒险者直到亲眼看见溃疡与坏死从被咬处沿手臂蔓延，才真正明白危险。这类病症必须立刻处理：若被食尸鬼咬伤，马上将患处浸入滚烫的热水，再迅速用内衬艾蒿与石英粉的干净布料包好。伤口必须包扎三周，每四天更换一次敷料，而且务必烧掉旧敷料！做不到这些，用野性纹身也很有效。

    * * *


#{bold}#2、骷髅#{normal}#

要是不死族狩猎指南里都没有最常见的骷髅那还算个屁指南？虽然这些亡灵身上的白骨在走路时上下乱颤，搞得一副弱柳扶风的样子，但是从许多方面来说，它们都远比自己的食尸鬼表亲要危险多了。

因为骷髅身上通常不会有那么多累赘腐肉，死灵法师得以全身心的投入对骷髅战斗能力的授予，同时由于战士们生前所用的武器几乎和他们的骨头一样经久耐用，我们遇到的骷髅兵大多都是持有武器或是全副武装的。何况骷髅对我们的威胁并不仅仅是近身战：死去的弓箭手会再度拿起弓；虽然更为困难，有些死灵法师甚至能让死去的法师重获魔法力量。

不少冒险者在面对骷髅时都疑惑不解——如何摧毁一个早已死的不能再死的骷髅。对于这些冒险者，我只想说：鼓起勇气吧。骷髅的身躯越是遭到破坏残缺，死灵法师们驱动它们所要消耗的法力就越大。因为大多数的死灵法师都将骷髅视为最低等的奴隶，相信在你数个重击之后就能驱除死灵法师附着于其身上的微弱法力。

    * * *


#{bold}#3、尸妖#{normal}#

尸妖是不死生物中的异类，往往并非由死灵法师特意创造，而是在条件成熟时自行出现。尸妖绝不是单独的灵魂，而常是某种集合意识的一部分；某片土地经历了足够多的杀戮——无论战场、森林、地宫还是墓园——尸妖便会成群升起，几乎是这片土地所受战争与动荡的实体化身。遗憾的是，死灵法师仍常常促成尸妖诞生，因为没有别的学问或行当会制造如此多的鲜血与死亡。

与尸妖战斗过的人经常将其描述为：一具轮廓模糊的骷髅身形，裹着飘动的褪色长袍，袍角逐渐变淡、虚化，本该是眼睛的位置则跳动着诡异的光。幸存者们则述说只要靠近这种诡异的生物，仅仅是靠近这些死亡的化身，自己的生命力就会不住地衰减、消逝。

万幸的是，尸妖虽然看上去很像鬼魂，已经被证实它们还是能被武器和腕力所消灭，至少是暂时消除了它们的威胁。无奈的是，这种战斗长远来说只是变相的壮大了尸妖族群而已。

    * * *


#{bold}#4、吸血鬼#{normal}#

吸血鬼与其他种类的不死生物相去甚远，简直令人难以置信。是什么让他们如此长寿？而他们又是如何保留这样强大的智力？暂且不提他们萎黄的面色与消瘦的五官，他们为何不像食尸鬼同类一样腐烂分解？

关于吸血鬼本质的研究仍有许多未解之谜，而每个新课题似乎也只是增加了更多的谜题而已。

如前所述，吸血鬼最大的优势，是身心都与活人极其相似。因此，比起其他不死生物，吸血鬼往往住得离普通城镇和村庄近得多；有些甚至直接把巢穴设在这些社区之中！

然而再怎么像人，吸血鬼仍有许多显眼征兆：不自然的苍白皮肤、细长醒目的尖牙、畏惧阳光，等等。为了躲避近距离盘查，有些吸血鬼会伪装成富人，常年幽居偏远之地，不让好奇者靠近。

但也许吸血鬼最让人称奇的地方，是他们纷繁复杂的系谱和族群。他们自发组建部族、血盟、家族等不可思议的集群，这是其他不死族无法望其项背的。借助团体的力量，吸血鬼常常成为弱小不死族的主宰者，像一名普通的死灵法师一样操作指挥着自己的奴隶。所以，请你也像对付死灵法师一样对付他们——用钢剑刺穿他们的喉咙。

    * * *


#{bold}#5、幽灵#{normal}#

在我的旅程中，我注意到荒野中的一些社区已不再像较大的聚居地通常那样埋葬死者。取而代之的是，他们会将死者的尸体焚化并将骨灰撒落在大地之上。当我询问他们这奇怪行为背后的意义时，几乎都是同样的原因：死灵法师。

他们害怕死者会在妄想而嗜杀的渣滓驱使下爬起来杀害自己，于是相信焚烧尸体能让灵魂永远逃出死灵法师枯骨般手指的掌握。

可惜事实并非如此。火焰能烧毁人的肉身，却没有任何火焰能够触及灵魂。

更为不幸的是，死灵法师却可以触到。同时失去身体和自由的痛苦，让许多灵魂在死灵法师的奴役下疯狂了，它们不停地飘荡在风蚀的地宫之中，用种种诅咒与妖法折磨着任何不幸与之遭遇的游荡者。

最糟糕的是那些接受了自己新使命的灵魂，它们的力量会以惊人的速度增长。在马基·埃亚尔，没有任何生物像这些“噩灵”一样如此明显地为存在本身所憎恶——仿佛造物本身也想将它们从这个世界抹去。希望你和更多人能遂她所愿。

    * * *


#{bold}#6、骸骨巨人#{normal}#

死灵法师所谓的“艺术”中最恐怖、最令人作呕的表现之一，就是骸骨巨人。有些野心勃勃的死灵法师不满足于只亵渎一具遗骸，便把无数骷髅的骨架缚在一起，造出比常人高出数倍的丑恶毁灭机器。

将骸骨巨人与法师或炼金术士的傀儡一视同仁是大错特错的。尽管这些法师老头们偏执又古怪，但通常法师们制造傀儡的目的只是用来当苦力或自卫。而死灵法师创造骸骨巨人的唯一目就是制造死亡，对一只骸骨巨人能力的唯一限制竟然只是其创造者扭曲的想象力。你有没有与一向被视为力量象征的雪巨人战斗过？那就想象一下长着六只胳膊的骸骨巨人吧——手指由削尖的肋骨制成，如刀刃般锋利；再想象无数头颅悬挂在这具骸骨巨人每一寸肢体上，它们都尖叫着怒吼着，因为你的每滴鲜血都令其饥渴无比。它用畸形的双手挥舞脊柱作鞭！你若有幸见识了这扭曲的混合体，恐怕会巴不得回到岱卡拉，去欺负那些头脑简单、浑身覆霜的低等类人生物。

    * * *


#{bold}#7、巫妖#{normal}#

他的身体由憎恨组成，他是纯粹的邪恶、死亡的化身，死灵法师的无上杰作。我能明确的告诉你巫妖并不是你想象中的那样，关于它的无数传奇和神话也的确有所失实。

他的恐怖远超于此。

当一名强大的死灵法师最终超越了生死界限后，他从前只能零星借用的地狱力量一下子完全服从于他。传说中，大地莫名的震颤、谷物奇怪的枯萎、树叶的同时凋零都预示着一只巫妖的诞生。作为至高的不死之主，巫妖能瞬间泯灭无数食尸鬼与骷髅，眨眼间将噩灵驱散，片刻就使骸骨巨人灰飞烟灭。

至于消灭巫妖的确切方法嘛……这么说吧，如果你成功的摧毁了这样的怪物，亲爱的请你一定要为我写一篇指南。因为我真的，完全，没有办法。

    * * *

确认依据：lore/fun.lua:217–289 不死猎人指南（宿主逐句核对固定源码）：usually armed and sometimes even armoured 被夸大为“大多都是持有武器或是全副武装的”；treat them as you would a necromancer - with cold steel 增译“刺穿他们的喉咙”；Ever fought a snow giant? 增译“一向被视为力量象征的”；all screaming for your blood to be spilt 被改成因果“因为你的每滴鲜血都令其饥渴无比”；I always receive the same answer 弱化为“几乎都是同样的原因”；巫妖段“传说与之不符是因为它超越传说”被译成传说“有所失实”，与下句自相矛盾。忠实性缺陷，整条逐句对照修复（wild infusion=野性纹身保持）。

## f19cec2641cd74c4c3020f07432b8402ddc8f9efc02c378e785fd4a3668a339f

section: mod-tome/data/chats/alchemist-last-hope.lua
source_tag: _t

source: #LIGHT_GREEN#*The dwarf finally returns with a vial and a small pouch.*#WHITE#
I put a bit of the good stuff in this one, though it won't do you any favors tomorrow morning. And careful with that Taint of Purging, especially if the wife answers the door the next time you knock. Har!

target: #LIGHT_GREEN#*那个矮人终于回来了，手里拿着一个药瓶和一个小袋子。*#WHITE#
这里面我给你带来个好东西，尽管也许明天早上对你没什么用。小心使用这个“清除印记”，如果下次你敲门的时候，是我老婆开门的话，你可要小心点，哈！

确认依据：chats/alchemist-last-hope.lua:405–406 矮人送药对话：I put a bit of the good stuff in this one, though it won’t do you any favors tomorrow morning 意为“我往这瓶里加了点好料（烈酒），不过明早可有你受的（宿醉）”；现译“这里面我给你带来个好东西，尽管也许明天早上对你没什么用”把“往里加料”误为“带来好东西”、把“会让你难受”误为“没用”并增“也许”。与 contextual 独立复核同向，宿主由 advisory 改判 confirmed（语义）。整条对照修复。
与 surface 同向：alchemist-last-hope.lua:405–406 往瓶里加了好料/明早宿醉难受被误译为“带来个好东西/也许明早没什么用”。整条修复。

## f1e389dfae61e9e641ad6118c5b582f3ebbc6ebd99b27bc67e514b415781fe89

section: mod-tome/data/achievements/quests.lua
source_tag: _t

source: Won ToME by closing the Void portal using yourself as a sacrifice.

target: 以自己的牺牲来阻止虚空传送门，通关ToME。

确认依据：成就说明 Won ToME by closing the Void portal using yourself as a sacrifice：closing 为“关闭”，现译“阻止虚空传送门”误述动作（本库 closing the void farportal=关闭虚空传送门，mod-tome.lua:16039）。

## f20e44ef63bf290de8b5b00aaf83cc4009d914cd52d517dd2f94051892ef77e6

section: mod-tome/data/chats/sorcerer-end.lua
source_tag: tformat

source: sacrificing %s to bring the Way to all

target: %s牺牲自己，将维网带给众生

确认依据：chats/sorcerer-end.lua:146/161 special_death_msg ("sacrificing %s to bring the Way to all"):tformat(string.his_her_self(player))，%s 运行时为“他自己/她自己”（mod-tome.lua:1403–1404）；现译“%s牺牲自己，将维网带给众生”渲染为“他自己牺牲自己…”，%s 语义角色错置。同族 fiery wrath 句译“牺牲了%s，引来…”（mod-tome.lua:6142），按同式修复。
与 surface 同向：%s 为 string.his_her_self 反身代词（utils.lua:953–957），special_death_msg 再嵌入 PartyDeath.lua:123–131 以玩家名为主语的死讯；按同族“牺牲了%s，引来…”式修复。

## f22305679ecdc81c0b2ea179ae3a753148e5fbfa642c29acd3be9976241fd18c

section: mod-tome/data/talents/techniques/munitions.lua
source_tag: tformat

source: You create enhanced versions of your ammunition, granting them additional effects.
Incendiary - The explosion radius is increased by 1, and the ground beneath is ignited dealing an additional %0.2f fire damage each turn for 3 turns.
Venomous - Inflicts leeching poison, dealing %0.2f nature damage over 3 turns and causing you to heal for 100%% of all damage the poison deals to the target.
Piercing - Punctures the target’s armor, increasing all damage they take by %d%% for 3 turns.
You only have a limited amount of this ammo, causing this talent to have a cooldown.
The damage dealt will increase with your Physical Power, and status chance increases with your Accuracy.

target: 你制造出强化版弹药，获得额外效果：
燃烧弹- 爆炸范围增加 1, 点燃地面每回合额外造成 %0.2f 火焰伤害持续 3 回合。
剧毒弹- 感染吸血毒素，3 回合内造成 %0.2f 毒素伤害，毒素造成的 100%% 伤害会治疗你。
穿甲弹- 击穿目标护甲，目标受到的所有伤害增加 %d%% 持续 3 回合。
你的强化版弹药有限，所以技能有冷却时间。
伤害受物理强度加成，状态触发几率受命中加成。

确认依据：talents/techniques/munitions.lua:414 强化弹药 Venomous：leeching poison 造成 nature damage，本库伤害类型统一译“自然伤害”；现译“毒素伤害”误述伤害类型（机制术语）。整条对照修复。
与 surface 同向：munitions.lua:418 damDesc(self, DamageType.NATURE, poison)，应为“自然伤害”。
