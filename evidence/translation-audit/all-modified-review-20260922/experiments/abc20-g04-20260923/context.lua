section "mod-tome/dialogs/orders/Talents.lua"

t("Define tactical talents usage", "设定技能使用策略", "_t")
t([[%s is listening attentively, and wants to know what talents to use.
You can modify the tactical weights of various talents to increase or decrease their use.  The weights are multiplicative (zero will turn the talent off) and relative (changing everything to a weight of 2 will not alter how talents are used relative to each other).
Word travels fast in Maj'Eyal, and if %s is a summon all future summons of the same type will remember your preferences.
]], [[%s正在仔细地听着你，向你询问该怎么使用它的技能。
你可以修改他的技能使用策略中每个技能的权重，增加或减少某些技能使用的概率。这些权重是乘法性的（权重为零表示该技能永远不会被使用）和相对性的（把所有技能的权重都调整为 2，并不会改变各技能之间的相对使用）
在马基·埃亚尔消息传播得很快。如果 %s 是一个召唤生物，所有同类的召唤生物都会记住你的设置。
]], "tformat")
t("Talent Name", "技能名", "_t")
t("Weight", "权重", "_t")
t("Enter the talent weight multiplier", "输入技能权重乘数", "_t")
t("0 is off, 1 is normal", "0 表示不使用这个技能，1 为默认", "_t")
-- untranslated text
--[==[
t("", "", "_t")
--]==]


------------------------------------------------

section "mod-tome/dialogs/shimmer/ShimmerRemoveSustains.lua"

t("Shimmer: Remove Sustains Effects", "幻化：移除持续技能效果", "_t")
t("Name", "名称", "_t")
t("Active", "激活", "_t")
t("\
#{italic}##CRIMSON#This cosmetic feature is only available to donators/buyers. You can only preview.#WHITE##{normal}#", "\
#{italic}##CRIMSON#这项时装特性仅对捐赠者/购买者可用。你只能预览。#WHITE##{normal}#", "_t")
t([[#{bold}##CRIMSON#WARNING: this is an EXPERIMENTAL feature. It may explode!#LAST##{normal}#
Sustains auras with name in #YELLOW#yellow#LAST# can not be automatically turned back on if disabled. After turning them on here, you need to unsustain and resustain them manually.

#{bold}#This is a purely cosmetic change.#{normal}#]], [[#{bold}##CRIMSON#警告：这是一项实验性功能。它随时可能出现问题！#LAST##{normal}#
名称显示为#YELLOW#黄色#LAST#的持续技能光环，如果被禁用，将无法自动重新开启。在你在这里调整之后，需要手动先关闭再重新启用这些持续技能。

#{bold}#这个改变只会带来视觉上的变化。#{normal}#]], "_t")
t("Donator Cosmetic Feature", "捐赠者时装特性", "_t")
t("This cosmetic feature is only available to donators/buyers.", "这项时装特性仅对捐赠者/购买者可用。", "_t")
t("shimmer ingame", "游戏内幻化", "_t")
t("Donate", "捐赠", "_t")
t("Cancel", "取消", "_t")
t("#LIGHT_RED#no", "#LIGHT_RED#否", "_t")
t("#LIGHT_GREEN#yes", "#LIGHT_GREEN#是", "_t")

------------------------------------------------

section "mod-tome/dialogs/talents/MagicalCombatArcaneCombat.lua"

t("Arcane Combat", "奥术格斗", "_t")
t([[You may select a spell for Arcane Combat to automatically trigger with melee attacks.  Otherwise, select 'Random spells' to have a spell selected automatically with each attack.
]], [[你可以选择一项法术，在奥术格斗中进行近战攻击时自动施放。如果你选择随机法术，每次攻击时会随机施放一个法术。
]], "_t")
t("Talent", "技能", "_t")
t("Random spells", "随机法术", "_t")
t("Each time Arcane Combat is triggered, a random allowed spell will be used.", "每当奥术格斗触发的时候，会施放一个随机可用的法术。", "_t")
t("#{bold}#Choose a spell#{normal}#", "#{bold}#选择一个法术#{normal}#", "_t")
t("All known spells that can be used with Arcane Combat.", "所有已学会的可用于奥术格斗的法术。", "_t")
-- untranslated text
--[==[
t("", "", "_t")
--]==]


------------------------------------------------

section "mod-tome/init.lua"

t("Tales of Maj'Eyal: Age of Ascendancy", "马基·埃亚尔的传说：卓越纪", "init.lua long_name")
t([[Welcome to Maj'Eyal.

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
]], [[欢迎来到马基·埃亚尔的世界！

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
]], "init.lua description")
t("Though magic is still shunned in Maj'Eyal, rumours abound of secret havens of mages.", "尽管魔法在马基·埃亚尔大陆遭到排斥，不过传说仍然有一个法师的秘密庇护所。", "init.lua load_tips")
t("The Rush talent lets you close in on an enemy quickly and daze them, disabling them whilst you hack down their friends.", "冲锋技能可以让你快速接近敌人并眩晕目标，你可以借此时机击倒它的同伴。", "init.lua load_tips")
t("Stunning an opponent slows down their movement and reduces their damage output, giving you the opportunity to tactically reposition or finish them off at less risk.", "震慑可以减缓目标的移动速度，降低其伤害输出，为你制造机会重新占位，或以更低的风险将其解决。", "init.lua load_tips")
t("Movement is key on the battlefield. A stationary fighter will become a dead fighter. One must always seek the position of greatest tactical advantage and continue to re-evaluate throughout the battle.", "移动是战斗制胜的关键。一个固定不动的战士只会变成一个死的战士。战斗过程中你必须随时调整你的走位以保持你的优势。", "init.lua load_tips")
t("In the Age of Pyre the orcs learned the secrets of magic, and with their newfound powers nearly overcame the whole of Maj'Eyal.", "在烈火纪，兽人掌握了魔法的奥秘，凭借新获得的力量几乎征服了整个马基·埃亚尔。", "init.lua load_tips")
t("The orcs once terrorised the whole continent. In the Age of Ascendancy they were rendered extinct, but rumours abound of hidden groups biding their time to return.", "兽人曾经给整个大陆带来了一场浩劫。在卓越纪，他们已被彻底灭绝，但传言四起，仍有隐匿的团体在蛰伏待机，伺机卷土重来。", "init.lua load_tips")
t("Intense willpower lets wyrmics take on the natural powers of dragons.", "高强度的意志使龙战士可以获得龙族的自然力量。", "init.lua load_tips")
t("Alchemists can transmute gems to create fiery explosions, and are known to travel with a sturdy golem for extra protection.", "炼金术士可以转化宝石制造炽烈的爆炸，并且往往带着一尊坚固的傀儡随行以获得额外保护。", "init.lua load_tips")
t("In the Age of Pyre the giant golem Atamathon was built with the sole purpose of stopping the orcish leader Garkul the Devourer. The golem was single-handedly destroyed by the orc, who then slaughtered an army of thousands before the demonic fighter was finally slain.", "在烈火纪，人们建造巨型傀儡阿塔玛森的唯一目的，就是阻止兽人首领吞噬者加库尔。加库尔仅凭一己之力便摧毁了这尊傀儡，随后又屠戮了一支数千人的军队，最终这名如恶魔般的战士才被杀死。", "init.lua load_tips")
t("None know what the Sher'Tul looked like, or what caused them all to disappear thousands of years ago. Their rare ruins are a source of mystery and terror.", "无人知晓夏·图尔人的长相，也没有人知道为什么他们在几千年前突然消失了。至今我们仍能从他们仅存的废墟里感受到他们的神秘和恐怖。", "init.lua load_tips")
t("In deep places dark things dwell beyond description or understanding. None know the source of these hideous horrors.", "地城深处潜藏着无法用语言描述或理解的黑暗事物，无人知道它们是从哪里而来。", "init.lua load_tips")
t("Who knows what dark thoughts drive people to necromancy? Its art is as old as magic itself, and its creations have plagued all the races since the earliest memories.", "天知道是怎样的堕落思想才能使一个人成为死灵法师。这门艺术就像魔法一样历史悠久，它的造物自最早的记忆以来就一直困扰着所有种族。", "init.lua load_tips")
t("Some say that in their early days the Shaloren kings experimented with necromancy to preserve their flesh after death, but with little success. The Shaloren vehemently deny this.", "传说很早以前永恒精灵的王侯们利用死灵法术进行试验，试图让他们死后的肉体仍能永葆青春。不过他们并没有成功。但永恒精灵们都否认这个传说的真实性。", "init.lua load_tips")
t("120 years ago Toknor and Mirvenia united the human and halfling kingdoms and wiped out the orcish race, thus establishing the Age of Ascendancy.", "120年前，图库纳与米雯尼雅将人类与半身人的王国联合起来，击溃了兽人军团，自此开启了卓越纪元。", "init.lua load_tips")
t("\"The Spellblaze tore Eyal apart and nearly brought about the end of all civilisation. Two thousand years on its shadow still hangs over many lands, and the prideful mages have never been forgiven their place in bringing it about.", "魔法大爆炸撕裂了埃亚尔大陆，整个文明差点被彻底摧毁。两千年岁月已过，爆炸的阴影依然笼罩着很多地区。而那些高傲的法师们，也从未因其在促成此事中所扮演的角色而获得宽恕。", "init.lua load_tips")
t("Some are cursed with mental powers beyond their full control, turning them to a dark life powered by hatred.", "某些人被诅咒，获得了超出自身完全掌控的精神力量，从此堕入由仇恨驱动的黑暗生涯。", "init.lua load_tips")
t("Dreadfell has always been shunned for its haunted crypts, but of late rumours tell of a darker and more terrible power in residence.", "恐惧王座一直以来都因其闹鬼的地宫而为人所避讳，但最近有流言传出，此地盘踞着一股更加黑暗可怖的力量。", "init.lua load_tips")
t("Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.", "虽然有人说还能在某些隐秘之地找到夏·图尔的神器，但据说不可轻慢它们。", "init.lua load_tips")
t("Drakes and wyrms are the strongest natural creatures in the world, capable of powers far beyond most other beings.", "龙与巨龙是这个世界上最强大的自然生物，它们所拥有的力量远在其他生物之上。", "init.lua load_tips")
t("Giant worms tear open huge passageways through the deserts in the west. It is said great riches lie buried beneath the sand, still decorating the corpses of those who went there seeking great riches.", "西部沙漠中的巨型蠕虫挖掘出了很多巨大的通道。传说在那沙洞深处埋藏着很多诱人的宝物。不过除了宝物之外，更多的便是那些寻宝人的尸体。", "init.lua load_tips")
t("Arcane Blades employ a fusion of melee and magical combat. Their training is harsh but the most dedicated rise to great powers.", "奥术之刃是一个混合了魔法与近战的职业。他们的训练非常严酷，但最为投入者终能获得强大的力量。", "init.lua load_tips")
t("Wild infusions call upon the powers of nature to protect the flesh and rid oneself of afflictions.", "野性纹身召唤自然之力保护血肉，并驱除自身的不良状态。", "init.lua load_tips")
t("Shield runes act instantly, letting one protect oneself quickly whilst also preparing to flee or launch a counter attack.", "护盾符文为瞬发技能，可以在你准备逃跑或者反击的同时提供防护。", "init.lua load_tips")
t("Greater training in the use of armour lets it be used more effectively, blocking more damage and reducing the chance of an enemy hitting a critical spot.", "高级的护甲训练可以有效提高你的防护能力，使你格挡更多伤害并降低你受到致命一击的几率。", "init.lua load_tips")
t("The Thick Skin talent reduces all incoming damage, letting you survive for longer before needing to heal.", "硬化皮肤技能可以降低所有受到的伤害，让你在需要治疗前存活更久。", "init.lua load_tips")
t("Regeneration infusions act over several turns, letting you anticipate damage that will be taken and prepare for it.", "恢复纹身的效果持续数个回合，开启后每回合会恢复一定的生命值，使你的战斗更加从容不迫。", "init.lua load_tips")
t("In the most dire circumstances teleportation can be the best escape, but is not without risk.", "在最危急的时刻，传送可能是最好的逃生手段，但也并非没有风险。", "init.lua load_tips")
t("The Ziguranth are an ancient order vehemently opposed to magic. Some have become so attuned to nature they can resist arcane forces with their will alone.", "伊格兰斯是一个古老的反魔阵营，他们中的一些人可以依靠自身的意志力来抵抗奥术能量。", "init.lua load_tips")
t("Records say that giants once lived civilised lives, with mastery of many crafts and sciences. Now, though, they have adopted nomadic cultures, turning hostile against those that encroach on their lands.", "据史书记载，巨人族曾经也有高度发达的文明，掌握着许多手工和科学技术。不过现在他们已经适应了游牧生活，他们会攻击任何试图侵略的敌人。", "init.lua load_tips")
t("Zigur was founded by escapees of Conclave experiments during the Allure wars between humans and halflings.", "伊格是由厄流纪人类与半身人战争中的孔克雷夫实验逃亡者创立的。", "init.lua load_tips")
t("The Thaloren and Shaloren elves have never had good relations, and have been outright hostile since the Spellblaze devastated many Thaloren lands.", "自然精灵与永恒精灵之间关系一直不佳，自从魔法大爆炸摧毁了很多自然精灵大陆之后，他们之间更是相互敌视。", "init.lua load_tips")
t("The third elven race, the Naloren, were rendered extinct after a huge cataclysm swept the eastern side of Maj'Eyal into the sea.", "精灵第三分支，纳鲁精灵，在魔法大爆炸将马基·埃亚尔的东部地区沉入海底后，彻底灭绝。", "init.lua load_tips")
t("Trolls were once seen as little more than beasts or pests, but the orcs trained them up for use in war and they became much more intelligent and fearsome.", "巨魔从前不过被视作与野兽或害虫无异的东西，不过后来兽人因为战争的需要对它们加以训练，如今它们变得聪明得多，也可怕得多。", "init.lua load_tips")
t("Some say that the foot of a halfling is lucky to own. Halflings do not take well to those who enquire too forcefully.", "有人说拥有一只半身人的脚能带来好运。半身人可不待见那些打听得太起劲的家伙。", "init.lua load_tips")
t("The Nargol empire was once the largest force in Maj'Eyal, but a combination of the Spellblaze and orcish attacks have dwindled it into insignificance.", "纳格尔王国曾经是马基·埃亚尔最强大的国家。但是经历了魔法大爆炸和兽人的入侵之后他们已经变得无足轻重了。", "init.lua load_tips")
t("Some of the most powerful undead do not fall easily, and only through extreme persistence can they be put to rest.", "那些最强大的不死族并不是那么容易被打败的，只有通过不懈的战斗才能将它们彻底置于死地。", "init.lua load_tips")
t("History says little of the ancient race of yeeks that lived in halfling territory, but vanished before the time of the Spellblaze.", "历史对居住在半身人领地上的古代夺心魔族记载甚少，他们在魔法大爆炸之前就已销声匿迹。", "init.lua load_tips")
t("Dwarves are naturally a inquisitive people, but do not enjoy such inquisition turned on them. Most live secretive lives in their closed-off city, the Iron Throne.", "矮人们好管闲事，但他们自己却不喜欢别人来打搅，他们大多数居住在秘密的地下城市——钢铁王座之中。", "init.lua load_tips")
t("Alchemists can bind gems to armour to grant them magical effects, to protect the wearer or improve their powers. Some commercial alchemists can imbue gems into jewellery.", "炼金术士可以把宝石镶嵌到盔甲上，赋予其魔法效果，以保护穿戴者或增强其能力。一些提供商业服务的炼金术士还能把宝石镶嵌到首饰中。", "init.lua load_tips")
t("The Spellblaze was followed by the Age of Dusk, when disease was rife and civilisation collapsed. Necromancers and fell sorcerers took advantage of the chaos to spread their vile deeds.", "魔法大爆炸之后到来的是黄昏纪，那是一个疫病肆虐文明溃败的时代。死灵法师和一些堕落法师利用当时的混乱来散播他们的恶行。", "init.lua load_tips")
t("After the Spellblaze came the Spellhunt, when the normal people rose against the arrogance of the mages and hunted them down like wolves. Some survived and went into hiding, but many innocents were killed.", "魔法大爆炸之后，猎魔行动随之而来。普通民众奋起反抗法师的傲慢，像猎狼一样追杀他们。一些法师幸存下来并躲藏起来，但也有许多无辜者遇害。", "init.lua load_tips")
t("Demons are thought to come from another world, brought to Eyal by magical forces. Some are highly intelligent and follow their own ambitions. To what end, none know.", "人们认为恶魔是被魔法力量从其他世界带到埃亚尔大陆的。有些恶魔具有高度的智慧并有他们自己的野心，没人知道他们的真正目的。", "init.lua load_tips")
t("The art of potion making fell into decline after the Spellhunt, and only a rare few now master the gift.", "猎魔行动之后炼金技术严重衰退，现在只有极少数人掌握这种技能了。", "init.lua load_tips")
t("It's said that some rare powers can save your soul from the edge of death.", "传说有些罕见的力量可以在死亡边缘拯救你的灵魂。", "init.lua load_tips")
t("Rumours tell of a shadowy cult kidnapping women and performing strange rites. Their intentions are unknown, and they have so far evaded capture.", "传说有一个邪教组织，他们绑架妇女举行奇怪的仪式，没人知道他们真正的目的，至今他们还没有被抓捕。", "init.lua load_tips")
t("Though slavery is illegal there is still a black market for it, and in some areas men are even used for blood sports.", "尽管贩奴被严令禁止但地下交易却仍然存在。有些地方奴隶甚至被作为一种血腥运动项目的道具。", "init.lua load_tips")
t("Maj'Eyal is the biggest continent in the world of Eyal. Though records suggest other continents and islands may exist it has not been possible to cross the wide and stormy oceans since the Spellblaze and the Cataclysm.", "马基·埃亚尔是埃亚尔世界中最大的一块大陆。虽然有记载世界上有可能还存在着其他大陆或者岛屿，但自从魔法大爆炸和大灾变发生之后，穿越浩瀚的风暴之海已经不大可能了。", "init.lua load_tips")
t("The effects of the Spellblaze were not all instant, and many centuries later the Cataclysm tore the continent apart once more, devastating coastal areas the destroying all of the Naloren lands.", "魔法大爆炸造成的影响并非仅局限于那一瞬间，数个世纪之后，大灾变再次撕裂了大陆，摧毁了沿海地区，并摧毁了所有纳鲁人的土地。", "init.lua load_tips")
t("Archers are fast and deadly, and with pinning shots can render their foes helpless as they swiftly dispatch them.", "弓箭手行动迅捷而致命，他们可以使用定身射击使敌人无力反抗，然后迅速解决他们。", "init.lua load_tips")
t("Reavers are powerful fighters with corrupted blood, and the strength to wield a one-handed weapon in each arm.", "收割者是流着堕落之血的强大战士，他们双手各可以装备一件单手武器。", "init.lua load_tips")
t("Corruptors feed off the essence of others, and can use their own corrupted blood to launch deadly magical attacks.", "腐化者可以吸取他人的精华，并使用他们的堕落力量发动致命的魔法攻击。", "init.lua load_tips")
t("Clever rogues can lay traps to damage or debilitate their foes without having to go near them.", "聪明的盗贼可以在不近身的情况下安置陷阱对敌人造成伤害或者削弱他们。", "init.lua load_tips")
t("Rogues can move silently and stealthily, letting them approach foes unaware or avoid them entirely.", "盗贼可以悄无声息的移动，在敌人毫无察觉的情况下悄悄近身，或者完全避开敌人。", "init.lua load_tips")
t("A movement infusion can let you quickly approach a ranged opponent, or quickly escape a melee one.", "移动纹身可以使你快速地接近一个远程敌人或者逃离近战敌人。", "init.lua load_tips")
t("Invisibility lets you escape notice, giving you the freedom to move or recover your resources, but reduces your damage.", "隐身可以使敌人忽略你，让你自由移动、恢复能量，不过这会降低你的伤害输出。", "init.lua load_tips")
t("Poison is the domain of assassins and master rogues, and its cunning use can cripple or kill enemies over a long fight.", "毒药学是盗贼大师和刺客的技能，它可以在一场长时间的战斗中削弱或杀死敌人。", "init.lua load_tips")
t("Summoners can call upon a variety of natural creatures to protect and support them, reducing the risk to their own flesh considerably.", "召唤师可以召唤不同的自然生物来支援和保护他们，这样可以减少他们直面敌人的危险。", "init.lua load_tips")
t("The highest sorcerers are known as archmages, and the masters amongst them are said to have the power to change the world. They are feared immensely.", "元素法师被认为是最高级别的法师，而其中的魔导师更是拥有改变世界的强大法力，他们也是世人最惧怕之人。", "init.lua load_tips")
t("Bulwarks are defensive fighters that can take hits more readily than other warriors whilst preparing for the most effective counter attacks.", "盾战士是防御型的战士，他们可以比其他战士职业承受更多伤害，在防御的同时他们也能随时做出反击。", "init.lua load_tips")
t("Brawlers are trained in the use of their fists and mastery of their bodies. They can be as dangerous in combat as any swordsman.", "格斗家受过双拳运用与身体掌控的训练。他们在战斗中的杀伤力不亚于任何一个持剑的战士。", "init.lua load_tips")
t("Lightning is a chaotic element that is hard to control. It is said that those most attuned to it are eventually driven insane.", "雷电是一种混沌的元素力量，难以操控。据说与之最为亲和者最终都会陷入疯狂。", "init.lua load_tips")

------------------------------------------------

section "mod-tome/load.lua"

t("In main hand", "在主手", "_t")
t("Most weapons are wielded in the main hand.", "大部分武器使用主手抓握。", "_t")
t("In off hand", "在副手", "_t")
t("You can use shields or a second weapon in your off-hand, if you have the talents for it.", "如果你有对应的技能，你可以副手使用盾牌或第二把武器。", "_t")
t("Psionic focus", "心灵传动", "_t")
t("Object held in your telekinetic grasp. It can be a weapon or some other item to provide a benefit to your psionic powers.", "使用你的念动力抓取的物品。你可以抓取武器，或者抓取其他物品来为你的心灵力量提供增益。", "_t")
t("On fingers", "在手指上", "_t")
t("Rings are worn on fingers.", "戒指戴在手指上。", "_t")
t("Around neck", "在脖子上", "_t")
t("Amulets are worn around the neck.", "项链戴在脖子上。", "_t")
t("Light source", "光源", "_t")
t("A light source allows you to see in the dark places of the world.", "光源可以让你看清这个世界的黑暗角落。", "_t")
t("Main armor", "主护甲", "_t")
t("Armor protects you from physical attacks. The heavier the armor the more it hinders the use of talents and spells.", "护甲保护你免受物理攻击。护甲越重，穿着它释放技能和法术就越难。", "_t")
t("Cloak", "斗篷", "_t")
t("A cloak can simply keep you warm or grant you wondrous powers should you find a magical one.", "斗篷可以让你保持温暖，而一些魔法斗篷可以给你神奇的力量。", "_t")
t("On head", "在头上", "_t")
t("You can wear helmets or crowns on your head.", "你可以在头上戴头盔或王冠。", "_t")
t("Around waist", "在腰间", "_t")
t("Belts are worn around your waist.", "腰带戴在腰间。", "_t")
t("On hands", "在手上", "_t")
t("Various gloves can be worn on your hands.", "你的手上可以戴上手套。", "_t")
t("On feet", "在脚上", "_t")
t("Sandals or boots can be worn on your feet.", "你的脚上可以穿上鞋子。", "_t")
t("Tool", "工具", "_t")
t("This is your readied tool, always available immediately.", "这是你准备好的工具，可以随时使用。", "_t")
t("Quiver", "弹药袋", "_t")
t("Your readied ammo.", "你准备好的弹药。", "_t")
t("Socketed Gems", "镶嵌宝石", "_t")
t("Gems worn in/on the body, providing their worn bonuses.", "装在身体内/外的宝石，提供宝石的装备属性。", "_t")
t("Second weapon set: In main hand", "第二套武器：在主手", "_t")
t("Weapon Set 2: Most weapons are wielded in the main hand. Press 'x' to switch weapon sets.", "第二套武器：大部分武器使用主手抓握。按 X 键切换武器套。", "_t")
t("Second weapon set: In off hand", "第二套武器：在副手", "_t")
t("Weapon Set 2: You can use shields or a second weapon in your off-hand, if you have the talents for it. Press 'x' to switch weapon sets.", "第二套武器：如果你有对应的技能，你可以副手使用盾牌或第二把武器。按 X 键切换武器套。", "_t")
t("Second weapon set: psionic focus", "第二套武器：灵能聚焦物", "_t")
t("Weapon Set 2: Object held in your telekinetic grasp. It can be a weapon or some other item to provide a benefit to your psionic powers. Press 'x' to switch weapon sets.", "第二套武器：使用你的念动力抓取的物品。你可以抓取武器，或者抓取其他物品来为你的心灵力量提供增益。按 X 键切换武器套。", "_t")
t("Second weapon set: Quiver", "第二套武器：箭袋", "_t")
t("Weapon Set 2: Your readied ammo.", "第二套武器：你准备好的弹药。", "_t")
t("Swift Hands", "无影手", "_t")
t("List of items that can be instantly used by swift hands.", "无影手可即时使用（不消耗回合）的物品列表。", "_t")
t("Strength", "力量", "stat name")
t("str", "力量", "stat short_name")
t("Strength defines your character's ability to apply physical force. It increases your melee damage, damage done with heavy weapons, your chance to resist physical effects, and carrying capacity.", "力量属性影响你的角色的物理能力，提升力量可以提高物理强度，提高使用重型武器造成的伤害，提高物理豁免，同时提高你的负重量。", "_t")
t("Dexterity", "敏捷", "stat name")
t("dex", "敏捷", "stat short_name")
t("Dexterity defines your character's ability to be agile and alert. It increases your chance to hit, your ability to avoid attacks, and your damage with light or ranged weapons.", "敏捷属性影响你的灵巧和警觉能力，提升敏捷可以提升命中，提升闪避，提升使用轻武器和远程武器造成的伤害。", "_t")
t("Magic", "魔力", "stat name")
t("mag", "魔力", "stat short_name")
t("Magic defines your character's ability to manipulate the magical energy of the world. It increases your spell power, and the effect of spells and other magic items.", "魔法属性影响你驾驭魔法能量的能力，提升魔法可以提高你的法术强度，法术的效果和其他魔法物品的使用效果。", "_t")
t("Willpower", "意志", "stat name")
t("wil", "意志", "stat short_name")
t("Willpower defines your character's ability to concentrate. It increases your mana, stamina and PSI capacity, and your chance to resist mental attacks.", "意志属性是你的专注能力，提升意志可以提升你的法力值、体力值、灵能值、精神力和精神豁免。", "_t")
t("Cunning", "灵巧", "stat name")
t("cun", "灵巧", "stat short_name")
t("Cunning defines your character's ability to learn, think, and react. It allows you to learn many worldly abilities, and increases your mental capabilities and chance of critical hits.", "灵巧属性提升你学习、思考和反应能力。提升灵巧可以让你学习更多的技能，提升精神能力和暴击几率。", "_t")
t("Constitution", "体质", "stat name")
t("con", "体质", "stat short_name")
t("Constitution defines your character's ability to withstand and resist damage. It increases your maximum life and physical resistance.", "体质属性影响你抵抗和承受伤害的能力，提升体质可以提高你的最大生命值和物理豁免。", "_t")
t("Luck", "幸运", "stat name")
t("lck", "幸运", "stat short_name")
t("Luck defines your character's fortune when dealing with unknown events. It increases your critical strike chance, your chance of random encounters, ...", "幸运属性影响你的角色在参与未知事件的幸运度。它可以增加你的暴击率，以及增加引发某些随机事件的几率。", "_t")
t("All kinds of weapons", "各种类型的武器", "_t")
t("All kinds of armours", "各种类型的护甲", "_t")
t("Rings and Amulets", "戒指和项链", "_t")
t("Gems", "宝石", "_t")
t("Infusions, Runes, ...", "纹身，符文，…", "_t")
t("Tinkers", "插件", "_t")
t("Miscellaneous", "杂项", "_t")
t("Quest and plot related items", "任务和剧情物品", "_t")
t("Transmogrification Chest", "转化之盒", "_t")
t("All", "所有", "_t")
t([[I begin my writings with a study of the humans, currently the most populous of the races in Maj'Eyal. The greatest kingdom in number are by far the Cornacs, but mention should also be made of the Sholtar and Mardrop kingdoms, and the Higher bloodline. The biggest human population centre is around the citadel of Last Hope, though many other settlements exist across all corners of Maj'Eyal.

 Cornacs are normally around 5'9", with generally dark hair, brown eyes and ruddy features. Most Cornacs take up roles as tradesmen, farmers, or other manual labour jobs. It is a sad fact that the majority of bandit groups tend to be dominated by Cornacs. Cornac families tend to be large, and since the Age of Dusk their population has expanded rapidly, especially in the farming lands in the west and around Last Hope in the south.

 Sholtar are generally 5'11", with dark skin, hair and eyes. They originate from the south-east of Maj'Eyal, and are few in number since the Cataclysm tore much of their land into the sea. Their affinity with nature is renowned, and they are often found employed as healers, infusion crafters or wyrmic huntsmen.

 Mardrop humans are all but extinct, after the Spellhunt and the plagues during the Age of Dusk. They were known to be powerful spellcasters, and as such were prime targets by the spellhunters. However some trace of them can still be found, as their fiery hair and freckled skin oft can appear in those of distant descent. A few are rumoured to still possess citadels and towers in remote locations.

 Highers are on average 6'0", with fair hair and skin and blue or grey eyes. The majority of scholarly roles are taken up by Highers, and they tend to fill most of the noble classes. Some say this is due to discrimination and elitism, though these may simply be jealous sentiments. There are also rumours that the superior intellects of Highers are due to arcane experiments instigated by the ancient Conclave during the Age of Allure, but I have found no records to support this idea and must consider it to be baseless. The Higher bloodline is renowned as a mark of excellence, and mixing with lower bloods is strongly frowned upon.

 All human kingdoms were united by King Toknor the Brave in the Age of Pyre, and remain under the rule of his son King Tolak the Fair. A full discussion of the long human history would require a far more detailed document.]], [[我从人类的研究开始，他们目前是马基·埃亚尔人口最多的种族。若论人口数量，科纳克王国远超其他人类王国。此外，肖尔塔王国和马卓普王国以及高等人类这一血统支系也值得一提。最大的人类聚居地在最后的希望要塞周围，另外还有许多聚居地存在于马基·埃亚尔的每个角落。

 科纳克人基本身高在5英尺9英寸左右，有着黑色的头发、棕色的眼睛以及红润的肌肤。大多数科纳克人选择商人、农民或者其他体力劳动职业。不幸的是，大部分强盗组织也更倾向于被科纳克人控制。科纳克人的家族很庞大，并且自黄昏纪以来他们的人口增长极快，特别是在西部农业地区和南部的最后的希望一带，这种现象尤为明显。

 肖尔塔人基本身高在5英尺11英寸左右，黑皮肤黑头发黑眼睛。他们起源于马基·埃亚尔的东南地区，自从大爆炸将他们大部分土地沉入海洋后，他们的数量急剧减少。他们以自然亲和著称，并且经常作为治疗师、注能物工匠或龙战士猎手行走于世。

 在黄昏纪的魔法狩猎与瘟疫之后，马卓普人几乎灭绝。他们以强大的施法者著称，也因此成为猎魔者的首要目标。不管怎样，他们的血统特征——火红的头发以及生有雀斑的皮肤，仍会出现在血缘疏远的后裔身上。有部分传言说他们仍住在某些遥远的地方的城堡或高塔里。

 高等人类基本身高在6英尺左右，有着金色的头发、白皙的皮肤和蓝色或灰色的眼睛。大多数学者都是高等人类，贵族阶层也大多由他们占据。有人说这都是歧视和精英理论所导致的，虽然这可能只是简单的嫉妒情绪。也有传言说高等人类的高智商是厄流纪时期秘法会法师们的实验成果，但是我找不到任何证据来支持这一论点，我只能认为这种说法毫无根据。高等人类的血统被认为是优秀的标志，与低等血统通婚则为世所不齿。

 在烈火纪，勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子公正之王托拉克的手中。一份关于人类漫长历史的全面报告需要更加详细的文本来叙述。]], "_t")
t([[No text would be complete without at least a brief note of some of the more brutish races which infest our world. These do not hold any civilised society of note, nor in general do they seem capable of any form of higher thought or culture, but they are still of interest to study for any who take delight in analysing beings of more primitive intellect.

 Trolls come in two main types - Kezrak and Moltep, or stone and forest trolls as they are colloquially known. Stone trolls infest many mountain chains to the north-east, and some have been known to wander further afield in search of food or to spread violence. They are generally over 8' high, with extremely pronounced muscular strength and a thick, solid hide which bears the appearance of coal or granite. Forest trolls are generally found in dense woods or swamps, with the Trollmire east of Derth being especially infamous. They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons, though their greenish hide is not as thick and their musculature less developed. All trolls have intensely fast metabolisms, capable of healing from grievous wounds within a matter of hours. At birth they measure just eight inches long, but within two years grow to full maturity, and rarely live beyond ten years old. They used to be considered little more than beasts, but towards the end of the Age of Pyre many were trained as fighters by the orcs, and were even taught the basics of language and certain battle tactics, making them much more dangerous. Though the orcs are gone their servants remain, and their remote breeding areas and intense birth rates have so far scampered attempts to eradicate them completely.

 Giants live mostly around the mountainous peaks surrounding the Daikara Pass. They vary greatly in size, but are normally at least 10' tall. They look somewhat like large, deformed humans, with swollen or distended facial features and much longer, swinging limbs. They live in nomadic tribes, moving from peak to peak with the seasons, feeding on wild deer and goats. They are usually peaceful creatures, only turning violent when their territory is encroached or their young are threatened. There are sometimes reports of giants coming to lowlands and stealing farm animals or attacking communities, but these are rare and normally isolated to particularly harsh winters. Giants seem to have no developed culture or language worth mentioning, but have been noted to show interactions of limited intelligence and to commune well in groups.

 Nagas were once believed to be mere myth, but reliable reports and even the capturing of dead physical samples has shown them to be real creatures. The upper half of their body is humanoid in form, with blonde hair and an extremely thin build, but the lower half is like that of a giant snake's tail. They stand around 6' tall on land, though their tails extend several feet further. They have been encountered off the eastern and south-eastern coasts of Maj'Eyal, which seems to indicate some exotic civilisation beneath the waves. Records of them exist only from the last few hundred years, and only more recently have they been interpreted as more than just the wild fantasies of inebriated sailors. They can breathe in air and underwater, possessing both lungs and gills, and have been reported to move with surprising speed on the ground. One might think them simply odd monsters, but they decorate themselves in jewellry and craft weapons and armour from materials found on the sea-bed, such as supple mail formed from layers of thick shark-hide. This would suggest an advanced culture, but communication with them so far has proved impossible. It is not known if they are capable of complex speech, but to date their only response to those who encounter them has been extreme violence, and fishermen in the east are always wary of coming across these vicious creatures.

 The origin of Demons is not wholly known, but it is clear that they are capable of intelligence and so I feel the need to describe them somewhat here. It is known that they can be summoned by certain magical rites, and minor demons were oft in the employ of evil sorcerers during the Age of Dusk. The main theory, which is supported by certain studies by Shaloren archmages, seems to indicate that they come from another world than our own, with connections formed through intense arcane energies. It must be a truly terrifying place to host such foul denizens. Demons vary immensely in appearance and power, as much as the creatures of our own world vary. They generally have blueish blood and metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness. All seem versed in magical abilities to some degree, and the strongest of them possess truly terrifying powers. Luckily they are exceptionally rare, and seem to be much less common in modern times since magic has fallen out of use.]], [[没有任何文字可以诠释那些影响我们世界的野蛮种族。他们没有任何文化遗留，也没有任何先进的智慧或文化，但是他们仍能激起大家研究原始种族的兴趣。

 巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。岩石巨魔生存与东北部的山脉地区，有些为了寻找食物和散播暴力甚至走到了更远的地方。他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。森林巨魔生活在浓密的森林和沼泽中，在德斯镇东部的巨魔沼泽尤为臭名卓著。他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速和能够使用精工武器闻名，尽管他们泛绿的外皮没有那么厚实，肌肉也不如岩石巨魔发达。所有的巨魔有着快速的新陈代谢能力，再严重的伤口，恢复只要几个小时。据测量，他们在出生时只有8英寸长，但是在2年内他们就可以成长完全，并且很少有寿命超过10年的。他们一开始被认为仅比野兽好一点，然而在烈火纪时，他们被兽人当做战士般训练，甚至学习了一些基础语言和战术，使得他们更加危险。虽然兽人已经走了，但他们的仆人仍然存在，并且他们偏远的繁殖地和极高的出生率至今仍挫败着彻底根除他们的企图。

 巨人们通常住在岱卡拉周围的山峦中。他们在体型上有着很大的差异，但基本上不会低于10英尺高。他们看起来就像是具有浮肿面部特征和更长的四肢的放大人类。他们属于游牧部落，随着季节的变化，从一个山头迁移到另一个山头，以鹿和羊为食。他们通常是和善的生物，只有当他们的领土受到入侵或者他们的后辈受到威胁时才会变的具有攻击性。有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击市民，但是这极其少见并且大多发生在极端的严冬。巨人们似乎没有值得一提的优越文化和语言，但是却向我们揭示了有限智慧的运用和团结一致的精神。

 娜迦曾被认为仅存于神话中，但是据可靠消息以及死亡的标本表明他们是真实存在的。他们的上半身是人形，有着金色的头发和苗条的身段，但是下半身却极像一只巨蛇的尾巴。他们大约身高6英尺，尽管他们的尾巴可能更长。他们在马基·埃亚尔的东岸和东南岸都有踪迹，这似乎表明波涛之下存在着某种异域文明。有关他们的记载只有近一百年的，并且越来越多的证据表明他们并不是喝醉水手们的幻觉。他们可以在水里和陆地上呼吸，同时拥有肺和鳃，并且据说在陆地上有着非常惊人的速度。有人可能认为它们只是特殊的怪物，但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。现在还不知道他们是否有复杂的语言，但是他们目前的对外回复只是极端的暴力，并且东海的渔民们经常要提防碰上这些邪恶的生物。

 恶魔的起源尚未完全清楚，但是很显然他们具有某种智慧，所以我觉得有必要在此写下一段。众所周知，他们是由某种魔法仪式召唤而来，并且在黄昏纪时期，小恶魔们经常受雇于邪恶的巫师。最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。那必然是一个地狱般的地方才能容下如此多恐怖的生物。恶魔们在外观和能力上不尽相同，正如我们世界里的生物一样。他们通常有偏蓝的血液和金属化的血肉，可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中。他们似乎都在某种程度上通晓魔法，并且他们之中最强者具有真正可怕的力量。幸运的是他们是非常罕见的种族，而且自从魔法淡出人们的视野后，出现的更加稀少了。]], "_t")
t([[The dwarves are an exceptionally secretive and quiet race, reluctant to talk about themselves to outsiders unless hefty bribes are paid. Many times in their history they have cut off all contact with the other races for no known reason, shutting tight the great iron doors that cover the trade passages to their mines and their cavernous cities. However of late they have become more open with the outside world, and I have even had the pleasure of receiving the unique distinction of being allowed to enter their main city, the Iron Throne, and speaking with several of their guild leaders.

 Dwarves are around 5' tall, with generally brown or grey hair. They are usually stocky and muscular, and known to be very resistant to any physical suffering. Their females can be hard to distinguish from their males, but can usually be identified by the beads braided into their beards. All dwarves are highly proud of their beards, and take immaculate care of them. The greatest insult to a dwarf is to belittle his beard, and the greatest sign of suffering in a dwarf is for him to tear at his beard.

 Dwarves are known especially for their smithwork and artificing, which is unrivalled amongst all the other races. They also make cunning merchants, known to drive a hard bargain. Their society consists of a fairly strict caste system, with families belonging to guilds of miners, smelters, craftsmen, and so on, and deviance into work outside of one's guild of birth is almost unheard of. However there is no perceived inequality between guilds, with each having equal representation on their ruling Committee of Guilds. Who actually acts as figurehead is unknown to outsiders though, and no amount of bribing will encourage any dwarf to speak on the subject. When it is mentioned in passing their allusions to a leader are normally marked by an almost religious reverence.

 Their skill with metal is renowned above all else. Dwarven steel is considered the most durable material for use in construction, and dwarves are the finest workers with stralite and voratun, precious metals of immense value. They trade heavily in their crafts from their capital the Iron Throne, but allow no outsiders in - instead they send innumerable merchant caravans out to all the cities to ply their wares.

 As well as the many merchant dwarves one may meet there are also a great deal of young dwarves who venture beyond their halls of stone. These are generally of adventuring fare, and it is encouraged in dwarven society to experience something of the wider world in one's younger years. This is known to them as being "smithed upon the anvil of the world". In private though some senior dwarves admit that this activity is promoted to help with their "market research strategy".]], [[矮人是非常神秘且低调的种族，一般来说，除非你给他们点好处，否则他们不会谈论任何与己有关的事。历史上，他们曾经多次无缘无故的切断和外界的联系，落下的钢铁大门隔绝了外界的交易通道以及通往他们矿井和地下城市的道路。不过，近来他们对外界越来越开放，我甚至获得了进入他们首都——钢铁王座的殊荣，并有幸与他们的主要领导人对话。

 矮人们基本身高在5英尺左右，有着棕色或灰色的头发。他们通常身材敦实、肌肉结实，并以超强的物理抵抗能力而闻名于世。他们的性别通常较难区分，但可以通过编入胡须的珠饰来辨认。所有的矮人都非常自豪于他们的大胡子，并且对他们的胡子非常爱护。对于矮人来说，贬低他的胡子就是最大的侮辱，而矮人极度痛苦时会撕扯自己的胡子。

 矮人擅长锻造和精工，这一点在所有种族中都是无与伦比的。他们同时精于商业，擅长讨价还价。他们的社会有着相当严格的等级制度，家庭通常会隶属于矿业公会、冶炼公会、工匠公会等等，脱离出身公会另谋生计的个人几乎从未听说过。不过，在公会之间并无地位不平等之说，各公会在统领众公会的公会委员会中拥有平等的代表权。谁实际担任名义领袖，外人不得而知，再多的贿赂也不能使任何矮人就此开口。当话题偶然被提及时，他们对那位领袖的暗示几乎总带着一种近乎信仰的敬畏。

 他们对金属的加工技艺也是举世闻名的。矮人钢被认为是建筑中最耐久的材料，而矮人也是加工斯莱特和沃瑞钽这两种价值连城的贵金属的最佳工匠。他们在首都——钢铁王座中进行大量的交易，但是从不欢迎外来者——相反，他们会指派无数商队到各个城市去售卖货物。

 在众多的矮人商人出现的同时，越来越多的年轻矮人更加倾向于从他们的石头洞穴里出去冒险。他们一般以探险为业，在矮人社会中，一个人在年轻的时候出去闯荡是值得鼓励和赞扬的。矮人称这种经历为在“世界之砧”上锤炼自己。不过私下里，一些年长的矮人承认推广这项活动是为了帮助他们的“市场调查策略”。]], "_t")
t([[Quekorja was the god of time and possibilities. What stands out about Eyal's myths regarding Quekorja is how wildly inconsistent they are. In particular, tales after the Godhunt tend to have a far less favourable outlook of the god than pre-Godhunt myths. Speculation regarding this is due to Quekorja supposedly taking an interest in written history and appointing its own librarians to record its tales. Since there are no surviving records of this library existing, this theory is considered to be pure conjecture and has no concrete evidence to validate it. There have been some unusual records found too, supposedly written by the same authors on the same dates, but wildly varying in their tone and their description of the god itself. Given the god's ability to control time, it is thought these notes might be from alternate timelines, further obscuring the truth about the god itself.

 Quekorja was also thought to be responsible for the creat...[i](You know you read this section, but you can't actually remember it. It is almost like something has deliberately erased it from your mind.)[/i]

 According to the records of Anglowen, Quekorja was slain during the Godhunt and its body discovered by the mage Linaniil. Linaniil managed to absorb a small portion of the god's power through a dangerous ritual. This tiny shard of power she acquired made her an archmage without peer, a testament to the sheer might of the gods.]], [[奎科加是时间和可能性之神。在埃亚尔关于奎科加的神话传说中，最突出的一点就是它们之间有着极大的矛盾，而在弑神之战之后的传说中它的形象远不如前。对此的猜测是奎科加自己可能十分爱好书写历史，指派了自己的记录者来记录自己的故事，但并没有证据表明有这样一个图书馆存在，因而这种理论被认为只是没有依据的臆测，没有实际证据的支持。另外还有一些不寻常的记录，本应是同一个作者在同一天写的，但其语调和对此神的描述却大相径庭。由于奎科加能够操控时间，因而有观点认为这些记录其实是来自别的时间线。这更加增添了奎科加的神秘。

 奎科加也被认为创……[i]（你记得你读过这段文字，但就是记不起其内容，就好像它是被有意从你的脑海中抹去了一样。）[/i]

 根据安格利文的记载，奎科加在弑神之战之中被杀死了，它的尸体后来被法师莱娜尼尔发现。她成功通过一个危险的仪式吸收了此神的一小部分力量，而就是这微小的力量也使她成为了无可匹敌的大法师。这也证实了诸神的力量是多么的强大。]], "_t")
t("You have accomplished great deeds, but if you enter the infinite dungeon there will be no way back. You will go on and on until you meet your glorious death.", "你已经完成了你的伟大使命，不过当你进入无尽地下城之后就永远不能再回来，你只有不断地前进直到你光荣地死去。", "_t")

section "tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua"

t([[[ERROR] format string error near '%s' of string %s
]], [[[ERROR] 格式化字符串错误位于'%s'，源字符串%s
]], "tformat")
t([[[WARNING]Mismatched tformat string:
        Source: %s %s
        Target: %s %s (args=%s)
]], [[[WARNING]tformat字符串不匹配:
        源: %s %s
        翻译: %s %s (args=%s)
]], "log")
t([[[WARNING]Mismatched translation for %s(%s): 
Last occurance: %s (from section %s)
Current occurance: %s (from section %s)
]], [[[WARNING]翻译内容不匹配 %s(%s): 
上次出现: %s (section %s)
本次出现: %s (section %s)
]], "log")
t("Success", "成功", "_t")
t([[Translation text checked.
Logs written to %s]], [[已检查翻译文件。
日志目录：%s]], "tformat")
t([[Translation text rearranged.
Logs written to %s]], [[翻译文件编排完成。
日志目录：%s]], "tformat")
-- untranslated text
--[==[
t("\
-- new text\
", "\
-- new text\
", "_t")
t("\
-- untranslated text\
", "\
-- untranslated text\
", "_t")
t("\
-- old translated text\
", "\
-- old translated text\
", "_t")
--]==]


------------------------------------------------

section "tome-addon-dev/superload/mod/dialogs/debug/AddonDeveloper.lua"

t("Addon Developer", "插件开发", "_t")
t([[- Your profile has been enabled for addon uploading, you can go to #{italic}##LIGHT_BLUE#https://te4.org/addons/tome#LAST##{normal}# and upload your addon.
]], [[- 你的用户账户支持插件上传，你可以访问 #{italic}##LIGHT_BLUE#https://te4.org/addons/tome#LAST##{normal}# 上传插件。
]], "_t")
t("Archive for %s", "%s的压缩包", "tformat")
t([[Addon archive created:
- Addon file: #LIGHT_GREEN#%s#LAST# in folder #{bold}#%s#{normal}#
- Addon MD5: #LIGHT_BLUE#%s#LAST# (this was copied to your clipboard)
%s
]], [[插件压缩包已创建完成:
- 插件文件: #LIGHT_GREEN#%s#LAST# 位于文件夹 #{bold}#%s#{normal}#
- 插件MD5: #LIGHT_BLUE#%s#LAST# 已复制到剪贴板
%s
]], "_t")
t("Registering new addon", "正在注册新插件", "_t")
t("Addon init.lua must contain a tags table, i.e: tags={'foo', 'bar'}", "插件init.lua必须包含tags表字段，例：tags={'foo', 'bar'}", "_t")
t("Addon init.lua must contain a description field", "插件init.lua必须包含description字段", "_t")
t("Addon: %s", "插件: %s", "tformat")
t("Addon #LIGHT_GREEN#%s#LAST# registered. You may now upload a version for it.", "插件 #LIGHT_GREEN#%s#LAST#已注册。你可以开始上传了。", "tformat")
t("Addon #LIGHT_RED#%s#LAST# not registered: %s", "插件#LIGHT_RED#%s#LAST#未能注册: %s", "tformat")
t("unknown reason", "原因不明", "_t")
t("Uploading addon", "正在上传插件", "_t")
t("Addon #LIGHT_GREEN#%s#LAST# uploaded, players may now play with it!", "插件#LIGHT_GREEN#%s#LAST#已上传，其他玩家可以游玩了！", "tformat")
t("Addon #LIGHT_RED#%s#LAST# not upload: %s", "插件#LIGHT_RED#%s#LAST#未能上传: %s", "tformat")
t("Connecting to server", "正在连接到服务器", "_t")
t("Steam Workshop: %s", "Steam创意工坊: %s", "tformat")
t("Update error: %s", "更新错误: %s", "tformat")
t("unknown", "未知", "_t")
t("Uploading addon to Steam Workshop", "正在将插件上传到Steam创意工坊", "_t")
t("There was an error uploading the addon.", "上传插件时发生错误。", "_t")
t([[Addon succesfully uploaded to the Workshop.
You need to accept Steam Workshop Agreement in your Steam Client before the addon is visible to the community.]], [[插件已经上传到Steam创意工坊。
你需要先在Steam客户端中接受Steam创意工坊许可协议，才能让其他用户看到你的插件。]], "_t")
t("Go to Workshop", "去创意工坊", "_t")
t("Later", "以后再说", "_t")
t("Addon succesfully uploaded to the Workshop.", "插件已经上传到Steam创意工坊。", "_t")
t("Uploading addon preview to Steam Workshop", "正在上传插件预览图到Steam创意工坊。", "_t")
t("There was an error uploading the addon preview.", "上传插件预览图时发生错误。", "_t")
t("Addon update & preview succesfully uploaded to the Workshop.", "插件更新和预览图成功上传到Steam创意工坊。", "_t")
t("Addon update succesfully uploaded to the Workshop.", "插件更新成功上传到Steam创意工坊。", "_t")
t("Choose an addon for MD5", "选择需要计算MD5的插件", "_t")
t("MD5 for %s", "%s的MD5", "tformat")
t([[Addon MD5: #LIGHT_BLUE#%s#LAST# (this was copied to your clipboard).
However you should'nt need that anymore, you can upload your addon directly from here.]], [[插件 MD5: #LIGHT_BLUE#%s#LAST#（已复制到剪贴板）。
不过你应该不需要它了，你可以直接在这里上传。]], "tformat")
t("Choose an addon to archive", "选择需要压缩的插件", "_t")
t("Choose an addon to register", "选择需要注册的插件", "_t")
t("Choose an addon to publish", "选择需要发布的插件", "_t")
t("Name for this addon's release", "插件的版本名称", "_t")
t("Name", "名称", "_t")
t("Choose an addon to publish to Steam Workshop (needs to have been published to te4.org first)", "选择需要发布到Steam创意工坊的插件（你需要先在te4.org上发布）", "_t")
t("Addon preview", "插件预览图", "_t")
t([[Addons on Steam Workshop need a "preview" image for the listing.
The game has generated a default one, however it is best if you make a custom one and place it in the folder #LIGHT_GREEN#%s#LAST# named #LIGHT_BLUE#%s#LAST# (512x512 is a good size for it)
You can still upload now and place it later.]], [[Steam创意工坊上的插件需要一张预览图。
游戏已经创建了一张默认的预览图，不过你最好自己制作一个，然后放置在文件夹#LIGHT_GREEN#%s#LAST#内，文件名为#LIGHT_BLUE#%s#LAST#（512x512是一个合适的图片大小）
你也可以现在先上传，之后再放置预览图。]], "_t")
t("Upload now", "现在上传", "_t")
t("Wait", "等待", "_t")
t("Generate Addon's MD5", "生成插件MD5", "_t")
t("Register new Addon", "注册新插件", "_t")
t("Publish Addon to te4.org", "将插件发布到te4.org", "_t")
t("Publish Addon to Steam Workshop", "将插件发布到Steam创意工坊", "_t")

------------------------------------------------
