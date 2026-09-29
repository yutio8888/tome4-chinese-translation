# batch-045：6 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01302
位置：mod-tome.lua:18083；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Ogres have never been a thriving race, starting from their abrupt appearance as soldiers and laborers for the Conclave during the Allure Wars (unexplained aside from a highly implausible story from the Conclave's Overseers about a lost mountain tribe).  Left without homes or proper runic training after the war's end, they were forced to found their own tribes and rediscover the fields of rune and infusion creation for themselves, and though their numbers dropped rapidly, they enjoyed a brief period of relative success as nomadic rune-traders, virtually unaffected by the Spellblaze.  The Spellhunt nearly proved to be their undoing, as their monstrous size and rune-covered skin made them popular targets; they were thought to be extinct, and only in recent years has the city of Elvala revealed that some Ogres took refuge there during this time.  Their descendants still live today, fearful of persecution but gradually beginning to explore outside Elvala for the first time in ages.

Ogres' most striking feature is their size, by far the largest of any intelligent race; they average at roughly 8'4" tall, and most are nearly half as wide with muscle.  They have a similar range of skin tones to humans, although slightly grayer on the whole; their hair tends to be dark brown or black, and their eyes run the gamut from black to bright blue to purple, presumably a side-effect of runic mis-transcription.  Their angular facial features invite some impolite comparisons to Orcs, with strong jawlines, disproportionately large mouths and teeth, and squarish heads, but otherwise resemble those of humans.  It would be remiss of me to describe Ogres' appearance without mentioning the intricate, glowing pattern of runes covering their skin from head to toe, although the exact patterns and colors vary.  

Although they excel at physical tasks for obvious reasons, and the necessity of careful inscription has made their finger dexterity (and penmanship) rather impressive, their limb movements tend to be slow and clumsy due to their size, and they tire quickly if they over-exert themselves during strenuous labor.  Their slow speech, incredible appetites, and lack of interest in arts or most scholarly concerns has led to a misconception that they are dim-witted; however, Ogres forced into studious tasks have performed admirably, and one needs only look at their runic patterns to know the patient study and artistic vision they are capable of, if properly motivated.  This may tie into the humble, duty-bound mindset that seems to be an inherent property of the species - most Ogres show absolutely no interest in leadership or impressing others, only completing tasks in the most reliable manner possible, and such strategies tend to be rather simple.

While Shalore use of magic is (arguably) a choice, Ogres have no such luxury.  Their inscriptions are as crucial to their well-being and structural integrity as any internal organ, and attempts by Ziguranth to "cleanse" captured Ogres of their runes invariably lead to them first collapsing under their own weight, then their organs shutting down one by one; one can assume that their natural infusions are just as vital.  As such, Ogre reproduction is a careful task; a newborn can live for a few months unaltered, but after this the parents must give their child a thorough regimen of runic inscription and herbal infusions.  The parents typically perform this task together, using each others' runes as a reference, and any mistakes made in the transcription will affect the child's health and development (usually adversely, though it is believed that transcription errors are responsible for mitigating Ogres' once-uncontrollable tempers).  As such, the inscribed patterns are as much of an influence on the child's development as the physical and mental traits of his or her parents.	

Due to the safety and comfort of Elvala, and their mistrust of much of the outside world, most Ogres who leave their home do so for trade purposes; no longer using Shaloren as couriers, some have begun to enter the growing market of runes and infusions, and have proven very successful thanks to their natural talent in this area.  Those few who could be considered "adventurers" tend to pack up their things and leave abruptly, not for glory or riches, but because they see a recurring source of misery in the world and wish to dispose of it themselves as a public service.  It is not uncommon for an Ogre to sigh in frustration after hearing about a hijacked shipment of grain, head out, return a few days later with the blood of a once-persistent bandit clan stuck to his club, and go right back to tending his crops.
```
译文：
```text
食人魔从来不是一个昌盛的种族。在厄流纪的长期征战中，这个种族突然出现在世人的视线里，作为孔克雷夫的工人和士兵。孔克雷夫的长老会宣称他们是在崇山峻岭中找到了隐藏于世间许久的食人魔，然而这个故事难以置信，漏洞百出，使得目前食人魔的产生仍然原因不明。在旷日持久的战争结束后，流离失所的他们无家可归，也没有接受过系统化的符文训练，只能被迫重新建立起自己的部落，自行重新摸索出符文与纹身的制作之道。尽管这一过程伴随着大规模的人口减员，他们作为游牧的符文商人度过了一段相对成功的日子，基本没有受到魔法大爆炸的影响。接踵而来的魔法狩猎几乎让这个种族就此灭绝。因为他们怪异的体格和满身符文的皮肤，他们迅速成为猎魔者的首要目标。几乎所有人都认为这个种族已经灭绝，直到近几年埃尔瓦拉城才透露，当年曾有一批食人魔在此避难。他们的后代仍然生活在今天，尽管仍然畏惧着外人的迫害，他们中的少数仍然尝试着向埃尔瓦拉以外的区域前去探索。

食人魔们最引人注目的特征是他们高大的体格，目前是所有智慧种族中体格最为硕大的一个。他们通常身高在8英尺4英寸左右，大多数人浑身的肌肉使他们的宽度几乎达到身高的一半。就像人类一样，他们也有各种类似的不同肤色，但总体而言比较偏灰色。它们的头发趋向于呈黑色或深褐色，眼睛的颜色分布在从黑色到湖蓝色到紫色的广泛色域内，想必是符文转录错误引发的副作用。他们面部的棱角引发了一些与野蛮的兽人族的令人不快的比较，连同强壮的下颌，不成比例地巨大的嘴巴和牙齿，以及方形的头。然而在其他方面，他们十分类似于人类。当然，最为不得不提的是，错综复杂地闪烁着的符文遍布于他们全身，从头到脚，尽管确切的图案和颜色各不相同。

他们一眼看上去就很适合体力任务，并且对于管理符文的重要性使他们手指变得十分灵巧，就连写出来的书法也令人印象深刻。然而，由于他们的庞大体型，他们的肢体动作往往显得缓慢而笨拙。并且，他们如果在艰苦的劳动中透支体力就会很快变得无比疲倦。他们语速缓慢，胃口令人难以置信的大，对艺术和科学基本没有兴趣，引发了广泛的误解，让人们往往趋向于认为这是一个低智商的种族。然而事实上，即便是被迫从事学术工作的食人魔，也表现得令人钦佩。只需要看看他们所制的符文图案，就能了解到他们只要需要的情况下就能发挥出多么伟大的艺术造诣和技术水平。这可能与一种谦卑而尽责的心态有关，这种心态似乎是该种族与生俱来的属性——大部分食人魔对领导他人或者给他人留下深刻的印象毫无兴趣，只一心关注于用最可靠的方式完成他们所做的事，而这种方式往往是最简单而毫不花哨的一种。

或许即使是永恒精灵也有可能放弃魔法的力量，但是食人魔可没有这样的奢侈。他们身上的符文对他们的健康和身体结构的完整性而言，其重要性不亚于任何一个内脏器官。伊格兰斯曾试着“净化”所捕获食人魔身上的符文，结果导致他们先因自身重量而瘫倒，随后器官一个接一个停止工作。可以假定，他们身上的纹身也相当重要。因此，食人魔的生育是一个十分复杂的过程。婴儿们可以保持没有符文的状态几个月，在此之后父母必须在他的身上铭刻一套包含各种符文和纹身的复杂的整体。父母们通常一起完成这项铭刻工作，使用彼此的符文作为参考，并且在这个转录的过程中的任何错误都会影响孩子的健康和发育。通常这一影响是不利的，然而因祸得福，似乎也正是转录错误缓解了食人魔们过去火爆的脾气。因此，孩子们身上所铭刻的符文和纹身对它们未来的发展，和父母本身的身心特质同样重要。

由于埃尔瓦拉的安逸舒适以及食人魔对外部世界根深蒂固的不信任，绝大多数离开家园的食人魔仅仅是为了一些商业目的。不再需要永恒精灵作为他们的中介人，一些人已经开始进入纹身和符文这一不断增长的市场，他们在这方面的天赋使他们在这一领域大获成功。而那些少数可以被视为冒险家的人，往往只是收拾好自己的东西突然离开，不为荣耀和财富，只为消除世界上不断出现的苦难与不幸而为他人奉献。经常听到这样的故事，一个食人魔偶尔听到有满载粮食的货船被劫的消息，立即出发。几天之后，他带着狼牙棒上那伙长期为患的强盗的血回来，然后继续回到乡间照料他的庄稼。
```

## entry-01303
位置：mod-tome.lua:18100；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Chapter 8 - Orcs (extinct)
```
译文：
```text
博学者格雷诺特关于种族的调查——第八章——兽人（灭绝）
```

## entry-01304
位置：mod-tome.lua:18101；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The orcs are, joyfully, extinct from Maj'Eyal, following the purge instigated by King Toknor the Brave at the start of the Age of Ascendancy. But an academic study of their previous culture and civilisation is still of interest, primitive though it may have been.

Orcs were generally around 6'1", with green or black skin. They varied greatly in physical appearance and build, most likely due to their exceptionally fast breeding rates. The majority of orcs were thick-built and heavily muscled, well remembered as the stock grunts of their terrible armies. However in the Age of Pyre a greater number of thinner, stringier orcs appeared, oft versed in destructive magics.

The orcs were first encountered by the Eldoral halflings, who tried to use the simple creatures as servants, but gave up after finding them to be too violent. In the many centuries since wars and battles have been almost continuously fought with the brutes. Their oft superior numbers have at times threatened to overwhelm all of civilisation, even leading to such drastic defensive measures as the Spellblaze. The most terrifying time though was during the Age of Pyre, when the orcs developed arcane abilities, and under the leadership of Garkul the Devourer they swept through the continent, mercilessly slaying all before them. In the end 10,000 halflings gave up their lives in the Battle of Nargol to defeat their demonic leader and stem their army's advance. Gradually the civilised races began to recover, and finally King Toknor and Queen Mirvenia succeeded in uniting the human and halfling kingdoms, putting together a force to push back the orcs and ultimately extinguishing them entirely.

Recent investigations of orcish ruins have revealed a surprising amount of cultural material, and even crude artworks based around fertility and battle. Some evidence has also been found of strong community elements to their culture, with much focus on sporting activities and racial pride events. However these are still clearly lacking in the subtleties and aesthetics of our more advanced cultures, and any attempt to compare them with us must be overshadowed by their brutality, territorial violence, and obsession with war.

There have been no substantiated reports of orcs for over 100 years. What reported sightings there are tend to be from such unreliable sources as adventurers and hermits, and have never been verified. We should be thankful that these horrible creatures have been banished to the annals of history, surviving only as stories to be told to misbehaving children.
```
译文：
```text
兽人们，很高兴地说，已经从马基·埃亚尔大陆上绝迹了——这紧随着勇者图库纳国王在卓越纪之初发动的清剿。但是对它们从前文化与文明的学术研究却仍然很有价值，尽管它可能相当原始。

兽人身高大约在6英尺1英寸左右，皮肤呈绿色或黑色。他们的外表与体格差异极大，这很可能与他们惊人的繁殖速度有关。大部分兽人体格粗壮、肌肉发达，作为他们那些可怕军队中的普通士卒而广为人知。然而在烈火纪，出现了大量更为瘦削、精悍的兽人，他们往往通晓毁灭性的法术。

最早与兽人接触的是艾德瑞尔半身人，他们本想把这些头脑简单的生物用作仆役，但在发现它们过于凶残后便放弃了。在此后的数个世纪里，人们几乎从未间断地与这些野兽征战厮杀。它们往往占据数量优势，一度威胁要压垮整个文明，甚至迫使各族采取了魔法大爆炸这样极端的防御手段。而最可怕的时期是在烈火纪，兽人掌握了奥术能力，在吞噬者加库尔的率领下横扫大陆，无情地屠戮面前的一切。最终，一万名半身人在纳格尔之战中献出了生命，击败了他们那恶魔般的领袖，并遏止了兽人军队的推进。此后各文明种族逐渐恢复，最终图库纳国王与米雯尼雅女王成功统一了人类与半身人的王国，集结起一支力量将兽人击退，并最终将他们彻底消灭。

近来对兽人废墟的调查揭示出数量惊人的文化遗存，甚至还有以生育与战斗为主题的粗糙艺术品。也有证据表明他们的文化中带有强烈的群体色彩，尤其重视体育活动与彰显民族自豪的活动。然而这些显然仍缺乏我们更先进文化所具有的精妙与美感，任何将他们与我们相提并论的尝试，都必然会被他们的野蛮、对领地的暴力和对战争的痴迷所掩盖。

100多年来，再没有关于兽人的确切报告。现有的所谓目击，多半出自冒险者和隐士这类不可靠的来源，也从未得到证实。我们理应庆幸这些可怕的生物已被逐入历史的册页，只作为讲给顽劣孩童的故事而留存。
```

## entry-01305
位置：mod-tome.lua:18118；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Chapter 9 - Sher'Tul (extinct)
```
译文：
```text
博学者格雷诺特关于种族的调查——第九章——夏·图尔人（灭绝）
```

## entry-01306
位置：mod-tome.lua:18119；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Ah, the legendary Sher'Tul! How any scholar does love to write about them. Indeed, the texts are many, but the facts are few, as so little is known about this crucible race. The most learned and factual academic on the subject is the renowned explorer and archaeologist Darwood Oakton, but he has alas been missing for several months at the time of writing. I will attempt to summarise here some of his key discoveries.

The Sher'Tul lived over ten thousand years ago, during what is referred to as the Age of Haze. The name of the race we know from the elves, who speak of the ancient beings with awe and reverence, yet know little else about them. Ruins of fantastical Sher'Tul structures have been found all across Maj'Eyal, and some have been observed in sunken lands off the coasts, implying that in their time the Sher'Tul must have ruled unopposed all across the world.

The farportals were first discovered by the halflings during the Age of Allure, and after much experimentation they were found to be able to transport items and creatures over vast distances. The arcane powers behind these incredible artifacts are still far beyond the understanding of the greatest minds of our time. The one attempt to truly tap into these powers ended in disaster - the Shaloren moved all known farportals to a remote spot near their capital, and their most powerful mages were overwhelmed as they unleashed the Spellblaze, killing them instantly and tearing apart the continent. What remains of farportals are left in the world have since been left untouched.

Of their physical appearance we know almost nothing, as there is no surviving artwork or records which depict themselves. However they must have been of similar form to other common races, as their ruins contain stairs, doorways and rooms not unfit for humans. Oakton estimates from his studies of their tools and artifacts that they would have stood around 5'4" tall, with uncommonly long limbs and fingers.

What caused them to become extinct is unknown, though many theories abound. The most popular in academic circles at the moment is that their mighty magics were their undoing, turned upon their own people during some great civil strife. Other theories hold weight though - Archiman Garybald, Professor of Demonic Studies, believes that the extensive uses of arcane energies by the Sher'Tul may have attracted twisted forces from other worlds which wiped out the ancient race. Some even believe that they are not truly extinct, but are in hiding, or have left this world for elsewhere. I fear the truth may never be fully known, but the ongoing study and examination of the relics they have left behind continues to provide immense value and inspiration.
```
译文：
```text
啊，传奇的夏·图尔！学者们是多么爱研究他们啊。事实上，相关的文献很多，但有事实根据的很少，所以有关该种族的信息也较少。最权威的研究是基于知名探险家和考古学家达沃德·欧卡顿的发现，但遗憾的是，截至本文写就之时，他已失踪好几个月了。在此，我将总结下他关键性的几个发现。

夏·图尔生活在距今一万多年前，被称为混沌纪的时代。这个种族的名字来源于精灵族，他们以敬畏之情述说着古代种族，即便如此，他们也对其知之甚少。在马基·埃亚尔大陆上，夏·图尔如梦似幻的废墟结构被找出并探索，有的废墟甚至位于海洋中沉没的大陆上，暗示着夏·图尔人曾经一度无可匹敌地统治过整个世界。

传送门的首次发现是在厄流纪，被半身人发现，在大量的实验后他们发现可以将物品和生物传送到很远的地方。这些奇迹背后的奥术原理仍远远超出我们能够理解的范围。唯一一次真正尝试利用这些力量的行为以灾难告终——永恒精灵将所有已知的传送门搬到了靠近他们首都的偏僻之处，他们最强大的法师在释放魔法大爆炸时被力量所吞噬，瞬间死亡，大陆也因此分崩离析。那些在大陆上剩下的传送门，至今无人敢碰。

关于他们的长相几乎没有人说得清，因为没有任何留存的艺术作品或记录来描述他们的外貌。然而他们肯定与其他种族有着类似的特征，因为他们的废墟中存在着适合人类的楼梯、门廊和房间。欧卡顿通过研究他们的工具和遗迹，得出了这样的结论：他们大约高5英尺4英寸左右，有着异常修长的四肢和手指。

他们绝迹的原因始终是个未解之谜，尽管有着各种猜想。在考古界最流行的说法是他们强大的魔法毁灭了自己，内战使他们消弭在历史中。其他理论——阿奇曼·加里伯德，恶魔研究教授则相信，夏·图尔人大量使用奥术能量，可能因此引来了异界的扭曲力量，最终导致整个种族的毁灭。有的人则更相信他们不是真的绝迹了，而是隐匿了起来，或者离开了这个世界。我恐怕真相永远无人知晓，但是对夏·图尔文明的深入研究仍有着非常重要的价值和意义。
```

## entry-01307
位置：mod-tome.lua:18136；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Chapter 10 - Monstrous Races
```
译文：
```text
博学者格雷诺特关于种族的调查——第十章——怪物种族
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Facial features	脸部特征	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
age of pyre	烈火纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	global	1.8beta 的统一译法；替换“派尔纪”
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
brutality	残暴	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
cleanse	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key，与 cleansing keyword 同一 cohort；不约束动作、技能说明或其他语境
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
inscriptions	刻印	T.GAME.TALENT_CATEGORY	talents	talent category	preferred	global	统一核心和兽人战役的技能类别译法；具体类型仍使用“纹身/符文”
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
misc	杂项	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
unknown	未知	T.UI.LABEL	ui	_t	preferred	global	未知条目/名称占位（15 处）
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
