# batch-032：5 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01215
位置：mod-tome.lua:14230；section：mod-tome/data/lore/angolwen.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#"What is Magic?"
#{italic}#A study by Archmage Tazimar Tarelion#{normal}#

How uncouth and common a question it must seem, and yet it is the one I am asked most often, even by some of our most learned students. Too often we teach The Art by practice and imitation and concentration on the end effects, without teaching in greater detail of the underlying principles. Just as a musician may merrily play on his harp without knowing how the sound arises from the vibration of the strings, so a mage may make use of magic without realising the true forces at work. In this document I hope to give learning on the nature of magic, and how the underlying effects give rise to all the wondrous fruits we can produce.

Alchemists will tell you that the world is made up of many base materials - lead, copper, iron, gold and so on. They are fixated on splitting things down into these components and investigating how they react with each other. However there is more to the world than this. Certainly they represent the physical make-up of things, but they do not show the forces and energy that bring everything into motion. The forces of fire, cold, lightning and life itself are all very real effects, and these we call the Elements of Eyal. The true archmage is interested in the interactions of the elemental forces of the world, and manipulating them to his or her need.

The elemental forces exist naturally in the world, and are weaved around all things in an all-encompassing canvas. They move, vibrate and resonate with the materials of the world, and the effects of each play heavily on one another. All creatures naturally make use of these elements, and some are more attuned to these threads than others. With great training and practice we can become more attuned to these wild forces ourselves, and in so doing some can match the speed of wolves, the strength of bears, the tenacity of treants and even the immense natural powers of dragons.

But there is another way of gaining access to these elemental forces - a more direct way, though some would call it unnatural. Long ago people discovered with much training how to concentrate their wills to pluck the elemental threads directly. This can release great energies, and these can be shaped to produce real effects in the world. Plumes of fire, bolts of lightning and blasts of ice can all be called forth by those suitably trained. The true masters of magic can go much further, combining many resonant forces to create complex physical effects.

The tapping of threads can be a draining task, requiring much effort of will to sustain. This is what we versed in the arcane call "mana", that mental stamina dedicated to the interaction with the elements of the world. Continual use of magic is like the constant lifting and holding of heavy weights, and eventually one will find one's capacity drained. Practice allows one to build up greater pools of mana, and certain runes and spells can gradually build extra reserves to be called upon as needed.

Magical runes and items are imbued with an attachment to certain elemental threads. This requires delicate work by experienced and gifted enchanters. The most intricate of magical artifacts demand many years of work, using intense mental effort to permanently attune the core materials to the right elemental energies. Gemstones are especially easy to work with in this craft, and alchemists use them often to bring about elemental effects.

Some believe that magic is inherently wrong, that the so-called twisting of the elements with one's will can only lead to terrible things. As students of Angolwen I assume you disagree! Magic is simply an extension of the forces of nature, and are we not natural creatures that use it? But remember that magic is still a powerful force that can be used for good or ill. Magic is indeed a tool of immense value - use it wisely.

```
译文：
```text
#{bold}#“魔法究竟是什么？”
#{italic}#大法师塔兹玛·泰尔兰的研究报告#{normal}#

这问题听起来多么粗俗平常，可它偏偏是我最常被问到的问题，甚至一些学识最渊博的学生也会询问。我们太常借实践、模仿和对最终效果的专注来教授魔法技艺，却不更详细地教授底层原理。正如音乐家可以快乐地弹奏竖琴，却不知声音如何由琴弦震动产生，法师也可以运用魔法，却不了解其中真正起作用的力量。我希望在这篇文章中教授魔法的本质，以及底层效应如何结出我们所能创造的一切奇妙果实。

炼金师会告诉你这世界是由许多基本材料构成——铅、铜、铁、金等等。他们专注于将物品分解成基本元素来分析他们是如何互相影响的。但这只是世界的一面，基本元素虽然表现了物质面上世界的构成，却不能解释推动万物运动的力量与能量。火之力、冰之力、闪电之力、乃至生命之力都是真实存在的，而这些力量我们称之为埃亚尔元素。真正的大法师专注于元素之力是如何影响这个世界的，并善于操作这股力量为己所用。

元素之力天然存在于世界，编织在万物周围，构成一幅无所不包的织布。它们与世界中的物质一同移动、震动与共鸣，彼此的效应互相深刻影响。所有生物都会自然地运用这些元素，但有些生物比其他生物更贴合这些丝线。通过大量训练与实践，我们自己也能更贴合这些狂野力量；如此一来，有些人就能匹敌狼的速度、熊的力量、树人的坚韧，甚至巨龙的浩大自然之力。

但还有另一种获得元素之力的方式——一种更直接、虽然有人会称之为不自然的方式。很久以前，人们发现，经过大量训练后，可以集中意志，直接拨动元素丝线。这能释放巨大能量，而这些能量又可被塑造成世界中真实存在的效果。受过适当训练的人可召出火焰烟柱、闪电之箭与寒冰爆流。真正的魔法大师还能走得更远，将多种共鸣力量结合起来，创造复杂的物质效果。

拨动丝线会消耗巨大，需要投入大量意志来维持。我们精通奥术之人将这种专门用于与世界元素互动的精神耐力称为“法力”。持续使用魔法就像不断举起并托住重物，最终会发现自己的能力已被耗尽。练习能让人积累更庞大的法力储备，某些符文与法术也能逐渐积累额外储备，以供需要时调用。

魔法符文和物品都被灌注了与某些元素丝线的联系。这需要经验丰富、天赋过人的附魔师进行精巧作业。最精密的魔法神器需要多年制作，以强大精神力将核心材料永久调谐到正确的元素能量。宝石尤其容易用于这种技艺，炼金师常用它们引发元素效应。

一些人笃信法术的存在本身就是个错误，所谓的凭某人意志扭曲元素之力只能带来可怕的后果。作为安格利文里的学生我假定你们都是不同意这种说法的。魔法只是自然之力的延伸，我们身为自然生物为何不能去尝试运用它？但你们要谨记魔法的存在仍是一柄双刃剑。作为工具它确实能产生极大的价值——明智的使用它。

```

## entry-01216
位置：mod-tome.lua:14450；section：mod-tome/data/lore/daikara.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#Relle, Cornac Fighter and Expedition Leader#{normal}#
It knows we're here.  Xann's gone, and I have to assume the worst.  Too late to run.  One option left, a contraption Sodelost ensured us he'd be able to use to get the kill...  shame he didn't leave instructions behind with it, it's unclear how to arm it, and I don't want to add "being charred to a crisp" to my list of troubles today.
I might not know a great deal about artifice, but I know how wild animals work, and for all the praise they get, dragons are no better.  I don't need to know how to rig this device so it goes off when the beast steps on it - I just need to put it inside something it'll eat whole...
#{italic}#Judging from this note's intact state and delicate placement next to a sack covered in assorted animal viscera, the dragon not only avoided setting off the trap, but has kept it as a trophy.  Inside the sack is a disarmed trap featuring a few recognizable alchemical flasks, and a means of mixing them in the right proportion when a pressure plate is triggered to produce a blast of dragonsfire. Figuring out how to arm it is almost as easy as figuring out how to make more traps like it.#{normal}#
```
译文：
```text
#{bold}#探险队队长，科纳克人战士瑞丽#{normal}#
那条龙知道我们在这里。希安失踪了，我只能作最坏的打算。逃跑已经太迟。只剩一个选择：苏达罗斯特向我们保证，他能用这套装置杀死那条龙……可惜他没把说明留在装置旁边，没人知道该如何启动它，而我可不想让今天的麻烦清单再多出”被烧成焦炭”这一项。
我或许不太懂机关术，却知道野兽会怎么做。龙尽管备受赞颂，在这一点上也不比其他野兽高明。我无需知道怎样把装置设成野兽踩中时触发——只须将它放进某种会被一口吞下的东西里……
#{italic}#从纸条完好无损的状态，以及它被小心摆放在一个沾满各种动物内脏的袋子旁边来看，那条龙不仅没有触发陷阱，还把它当作战利品收藏了起来。袋中有一个已解除的陷阱，装有几只尚能辨认的炼金药瓶；压力板触发时，机关会按正确比例混合其中的药剂，爆发出龙火。弄清如何启动它，几乎与弄清如何制作更多同类陷阱一样简单。#{normal}#
```

## entry-01217
位置：mod-tome.lua:14458；section：mod-tome/data/lore/daikara.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#Relle, Cornac Fighter and Expedition Leader#{normal}#
It knows we're here.  Xann's gone, and I have to assume the worst.  Too late to run.  One option left, a contraption Sodelost ensured us he'd be able to use to get the kill...  shame he didn't leave instructions behind with it, it's unclear how to arm it, and I don't want to add "being frozen solid" to my list of troubles today.
I might not know a great deal about artifice, but I know how wild animals work, and for all the praise they get, dragons are no better.  I don't need to know how to rig this device so it goes off when the beast steps on it - I just need to put it inside something it'll eat whole...
#{italic}#Judging from this note's intact state and delicate placement next to a sack covered in assorted animal viscera, the dragon not only avoided setting off the trap, but has kept it as a trophy.  Inside the sack is a disarmed trap featuring a few recognizable alchemical flasks, and a means of mixing them in the right proportion when a pressure plate is triggered to produce a blast of ice. Figuring out how to arm it is almost as easy as figuring out how to make more traps like it.#{normal}#
```
译文：
```text
#{bold}#探险队队长，科纳克人战士瑞丽#{normal}#
那条龙知道我们在这里。希安失踪了，我只能作最坏的打算。逃跑已经太迟。只剩一个选择：苏达罗斯特向我们保证，他能用这套装置杀死那条龙……可惜他没把说明留在装置旁边，没人知道该如何启动它，而我可不想让今天的麻烦清单再多出“被彻底冻住”这一项。
我或许不太懂机关术，却知道野兽会怎么做。龙尽管备受赞颂，在这一点上也不比其他野兽高明。我无需知道怎样把装置设成野兽踩中时触发——只须将它放进某种会被一口吞下的东西里……
#{italic}#从纸条完好无损的状态，以及它被小心摆放在一个沾满各种动物内脏的袋子旁边来看，那条龙不仅没有触发陷阱，还把它当作战利品收藏了起来。袋中有一个已解除的陷阱，装有几只尚能辨认的炼金药瓶；压力板触发时，机关会按正确比例混合其中的药剂，爆发出寒冰。弄清如何启动它，几乎与弄清如何制作更多同类陷阱一样简单。#{normal}#
```

## entry-01218
位置：mod-tome.lua:14722；section：mod-tome/data/lore/elvala.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Two: A Night to Remember#{normal}#

It was three nights later I awoke in darkness from a troubled dream to find my window open, the silk drapes billowing in the breeze.  As my eyes adjusted to the light I saw Linaniil stood at the foot of my bed, a thin azure dress clinging to her skin in the chill night air.  Around her was a cashmere belt inset with opals and woven with pale runes, and gold jewellery adorned her neck and wrists.  A long staff rested lightly in her hands, rubies glistening in its decorated top.  Her red hair stirred in the wind as she gazed at me.
 
“What are you doing here?” I enquired.  I did not bother asking how she managed to sneak into my bedchamber, past many guards.  I knew that no less than a council member would be able to divine her presence when she put her mind to illusion.
 
She looked at me slowly for a moment, before turning her eyes to the rest of the room, analysing my personal space in detail.  “There be a band of orcs marauding in the north,” she said in a distracted tone.  She picked an ornamental dagger from a shelf and looked it over as she spoke.  “They look like to cause trouble for some outlying elven settlements.”
 
“I will summon a raiding party at once,” I said, rising quickly from my bed, unheeding of modesty.
 
“Oh, how boring!” she complained, putting the dagger down and spinning to face me.  “What of the promise ye made to hunt orc together?”
 
“What, just the two of us?”
 
“Aye,” she said, looking my unclad form up and down with a slow gaze, seeming to take delight in the sight.  “Or are ye not man enough?”
 
“A strange question to ask of an elf, my lady.  But I can take this band of orcs myself, I am sure.  If you wish to tag along then I cannot promise to keep you safe.”
 
She laughed then, and the sound was like ringing crystal.  “Very well then!  Get ye your steel stick and we shall see who holds their own best.”  I agreed with a smile, and went to my armoury and shoved on metal greaves and a chain hauberk, my breastplate and steel gauntlets.  Linaniil tutted in surly impatience.  “Must ye wear that tin suit?”
 
“It is my battle gear,” said I, pulling on my visored helm and wrapping a thick cloak round my shoulders.
 
“Ye look like a golem,” she muttered, visibly annoyed.  “Come then, I grow bored.”  She leapt out the window, taking to the air with grace, flying away into the night.
 
I took then my greatsword from its hanging.  It was a simple looking blade, adorned only with a heavy moonstone on its pommel.  But its looks belied its power, for it was forged by the dwarves in their early years, before vanity overcame their works and their weapons became more for show than for battle.  It had an edge that clove through steel and bone with ease, without ever dulling the blade.  Mooncutter it is called, though it is lost to me now.  I gave it a swing through the air before leaping out the window myself, conjuring a cushion of air beneath me and following swiftly after Linaniil.
 
With rapid pace we flew through the scattered clouds in silence for twenty minutes before Linaniil began to descend.  I could see nestled between some low hills were the flames of campfires, and as we came closer the sound of orcish chanting became clear.  “How shall we approach them?” I called out, wondering what tactics the sorceress would want to employ.
 
“Directly,” she said, and with that she made a sudden burst of speed, coming right above the orcish camp and descending in their midst.  With a curse I sped after her, landing by her side and drawing Mooncutter as the orcs rose in fury and alarm, grabbing up their weapons.  As a ring of dark swords and spears and halberds gathered round us Linaniil turned to me with a wild smile.  “Time to dance.”
 
She shot forth a ray of purple arcane energy from her right hand, whilst her left held up her staff, its tip blazing like a torch.  Flames leapt up in tandem from my own blade as I rose it high, and swept it before me in a wide arc, cutting down the nearest brute and sending a shocking wave of fire into the troops behind it.  I pressed forward, forcing back the orcs before me with a roaring hot wind.  Their weapons dropped from their hands as they reached up to cover their faces, and with a grin of satisfaction I rushed to hew their heads off.  But as I swung my blade I was knocked to the ground from behind by a blast of fire, and turning about I saw Linaniil standing in a pillar of flame, her arms outstretched as it expanded around her.  “Too hot for ye, Aranion?” she called out as the orcs nearby were fried to a crisp, their flesh withering into black dust.
 
I grunted, and turned my blade into ice, and with deft sword strokes sent streams of freezing cold into the orcs around her, so that they shattered like glass before the fire ever hit them.  Linaniil cursed my name as she dropped the flames from about her.  “Don’t ruin my fun!” she exclaimed, before teleporting to the other side of the camp and beginning to blast the orcs there.

I laughed and turned on the beasts nearest me, and brought tumults to the earth with each swing, so that they lost their footing and fell to the ground before my sword found their throats.  Then I conjured a mighty spark of lightning, spearing it through their densest ranks, and I rushed along its glowing length hewing down the monsters before they could react.  I laughed again with the fey heat of battle, and I discarded my helm and tore off my platemail, taking joy from moving about the field with ease and slaughtering my inferior foes.  Mooncutter danced through their flesh, and their dark blood gushed and fountained with joyful rhythm.

On the far side of the camp explosions and screams marked Linaniil’s passage, and I saw burning limbs flying into the air and streaks of fire tearing through the night.  The sorceress was wreathed in flames, her eyes shining, and the dancing blaze about her made her look like a nymph of fire incarnate.  No more beautiful and awe-inspiring a sight had I ever beheld.

Seeing their numbers quickly dwindling the orcs began to flee, but I phased to block their retreat and called forth a wave of water, forcing them back against Linaniil’s flames.  There against the wall of fire I dashed them, and great numbers of them fell like leaves scattered in the wind.  Blood spilled thick and plentiful, and with but a few more thrusts of Mooncutter and blasts from Linaniil’s hands the battle was over.  Not a single orc still moved, and well over four hundred lay dead on the ground.
 
Linaniil and I stood facing each other, panting with sudden exhaustion as the adrenaline of the fight left us.  “I lost count,” I said between breaths, “of who slew more…”  She grinned coyly at me, sweat trickling down her face.  Minor cuts and burns left her robe in tatters, with one shoulder strap hanging loose.  Her glistening chest heaved up and down with each breath, and her deep eyes looked at me with naked intensity.
 
She strode forward then, and grabbing me roughly by my hauberk she pulled my lips to hers.  The kiss was hot and fierce, and as she bit my lower lip the course of blood in battle came back to me afresh.  I kissed her again and grabbed her body, pulling her tight to me, our lips locked.  She tore lustfully at my remaining armour, flinging it to the ground, and I slid off her silken clothes, till we were left bare beneath the stars.  Then against a rocky outcrop we pressed against each other, still gasping and sweating from the fight.  There with blazing passion flesh met flesh and our hot moans rose into the cold night sky.
```
译文：
```text
#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆 #{normal}#

#{bold}#第二章：难忘之夜#{normal}#

三天后的午夜，我在一场噩梦中惊醒。眼前窗户大开，晦暗的光线中丝织的帘幕在晚风中舞动。随着我的眼睛渐渐适应了夜晚微弱的亮光，我看见莱娜尼尔就站在我的床尾，一袭轻薄的蔚蓝长裙在寒夜的空气里紧贴着她的肌肤。她的腰间环绕着镶嵌着蛋白石和苍色符文的羊绒腰带，颈上腕间环绕着闪耀的金制首饰，一根长杖轻轻搁在她的手中，杖首的装饰上嵌着数颗红宝石，熠熠生辉。清风吹拂，她澄澈的眸子中映出我的影子，红色的长发迎风飘荡。

“你在做什么呢？”，我轻轻问道。我并没有打算询问她到底是如何绕过那些卫兵悄悄潜入我的卧房的。我知道，至少得是议会成员，才能在她专心施展幻象时察觉她的存在。

她明媚的目光轻柔地凝视着我，接着在屋子的四周扫过，仔细分析着房间里的每一个部分。“有一队兽人正在北方四处劫掠，”她稍有些心不在焉地说道，手中漫不经心地把玩着我在架子上放着的一把装饰用匕首，“他们看起来会给一些外围的精灵聚落惹上麻烦。”

“我立刻就召集突击队迎敌。”，我不顾礼仪地从床上坐起。

“唔，那样多无聊啊”，嘟哝着的她将匕首轻轻放下，回身面向着我，“那你许下的、要一起去猎兽人的承诺呢？”

“……什么？就只有我们两个人去吗？”

“是啊”，她的目光在我赤裸的身体上缓缓游移，上下打量，似乎对眼前的景色颇为享受，”还是说你不够男人？”

“对于精灵族来说这还真是个怪问题，我的女士。不过，我可以在此保证，只需要我一个人也可以亲手干掉那些兽人。如果你真的想要一同前行的话，我可能没法确保您的安全。”

她的笑声如同水晶泠泠碰撞般清脆。“那真是太好了！来，拿上你的金属棍子，让我们来看看谁更能撑得住。”我微笑着点头，走进武器库，匆匆套上金属护胫、锁子甲、胸甲和钢制护手。莱娜尼尔不耐烦地咂舌道，“你非得穿上这堆废铜烂铁不可吗？”

“这是我的战斗服”，我戴上头盔，披上斗篷。

“唔，看起来简直就像一只傀儡，”她小声咕哝着，”快来吧，我有点无聊了。”紧接着，她轻巧地越过窗台，优雅地随风而去，在夜空中划出一道弧线。

随后我从剑架上取下我的双手巨剑。乍一眼看上去，这似乎只是一把普通的剑刃，唯一的装饰是剑柄上一颗硕大的月亮石。这把剑由矮人于多年之前所铸，其貌不扬却强韧无比。之后，他们的虚荣和浮华替代了匠人的坚毅，让装备成为了用于炫耀的道具而不是用于战斗的兵器。这把剑的剑锋可以轻易穿透钢铁和骨头，且永不卷刃。它的名字叫做斩月剑，尽管现在已经随着岁月的流逝而不知所踪。我凌空挥动爱剑，随即跃出窗外，在身下唤出气流软垫，迅速追随莱娜尼尔而去。

我们在零散的云层间疾飞，沉默了二十分钟，莱娜尼尔才开始下降。低矮群山之间点缀着营地的篝火；随着我们飞近，兽人的吟唱声渐渐清晰。“我们该怎么接近他们？”我高声问道，想知道这位女魔法师准备采取什么战术。

“直冲进去。”话音刚落，她骤然加速，飞到兽人营地正上方，落在他们中间。我咒骂一声，急忙追上，在她身旁落地并拔出斩月剑；兽人惊怒地起身，纷纷抓起武器。当一圈黑沉沉的刀剑、长矛和戟将我们团团围住时，莱娜尼尔转向我，露出狂野的笑容。

“舞会开始了”

一道紫色的奥术能量从她的右手指尖射出，而她左手高举法杖，杖端如同火炬般被炽焰所缠绕。随着剑刃高举，一团团火焰从我的剑刃上腾跃而起，在我面前呈弧形喷发出来，迅速击倒了最前排的兽人，爆裂的冲击波向他身后的部队席卷而去。我紧逼而前，以咆哮的炽热之风迫退身前的兽人。他们的武器纷纷脱手落地，只能抬手遮挡脸面；我怀着满意的微笑冲上前去，正要斩下他们的头颅。可就在挥剑之际，一团火焰自背后将我击倒。转身望去，只见莱娜尼尔站在熊熊烈火之中，双臂向前伸展，烈焰应之而动。“对你来说是不是有些太热了呢，艾伦尼恩先生？”。在她的谈笑之间，周围的兽人纷纷被烈焰吞噬，转瞬便灰飞烟灭。

我闷哼一声，将剑刃化为坚冰，以精妙的剑技向她周围的兽人劈出道道凛冽寒流，在火焰触及之前便将他们冻成冰雕，碎裂如玻璃。莱娜尼尔咒骂着我的名字，撤去了周身的火焰。”别抢了我的乐子！”她大喊道，随即传送到兽人营地的另一侧，在那里掀起新一轮烈焰。

我大笑着扑向最近的野兽，每一挥都让大地剧震，兽人在震波中失去平衡纷纷倒下，任凭我的利剑穿透他们的喉咙。紧接着，狂暴的闪电在剑锋聚集，如同投枪一般射出，贯穿兽人们最密集的军列；我沿着它发光的轨迹冲锋，在他们还没来得及反应之前挥剑将这些怪物一一劈倒。我在战斗的狂热中再次大笑，丢掉头盔撕下板甲，享受卸甲后在战场上轻快移动、屠戮这些弱小之敌的快乐。斩月剑在他们的血肉间穿梭舞动，他们的黑血喷涌如泉，节奏欢畅。

远处营地爆炸的烟雾和兽人的惨叫声点缀着莱娜尼尔的足迹；我看见燃烧的断肢飞上半空，道道火光撕裂夜色。烈焰缠绕着女魔法师的周身，她的眸子熠熠生辉，四周跃动的火光让她宛如火灵的仙女下凡一般。此情此景，真是我一生所见最为美好最为震撼的那一刻。

剩余的兽人眼看人数锐减，开始逃跑；但我相位移动到他们前方，截断退路，又召来一股洪水，逼他们退回莱娜尼尔的烈焰之中。火墙之前，我将他们击溃，大批兽人如风中落叶般倒下。鲜血大股涌出；斩月剑又刺出几下，莱娜尼尔又轰出几道法术，战斗便结束了。没有一个兽人还能动弹，地上倒着远超四百具尸体。

面对面地，我和莱娜尼尔的身躯矗立在硝烟弥漫的战场上，随着战斗的肾上腺素退去，突如其来的疲惫令两个人气喘吁吁，呼出的气息在空气中凝成雾气。我气喘吁吁地说道，”我已经记不清了，到底是谁杀的更多…”。她害羞地微笑着，汗水从泛红的面颊滴落。战斗中的刀伤和灼烧让她的长袍残破不堪，一侧肩带松松垂落。她泛着光泽的胸膛剧烈起伏，深邃的双眼以赤裸的炽烈目光看着我。

她大步走来，粗暴地揪住我的锁子甲，把我的双唇拉向她。这一吻火热而激烈；她咬住我的下唇，战斗中奔涌的热血顿时再度沸腾。我又吻住她，一把搂住她的身体，将她紧紧拉向自己，双唇始终交缠。她欲火中烧地撕扯我剩下的护甲，将其甩在地上；我也褪下她的丝绸衣裳，直到我们赤裸着站在群星之下。我们靠在一处岩壁上，紧贴着彼此，仍因刚才的战斗喘息流汗。炽烈的激情中，肌肤交融，我们火热的呻吟升入寒冷的夜空。
```

## entry-01219
位置：mod-tome.lua:14813；section：mod-tome/data/lore/elvala.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The Spellblaze Chronicles(3): The Farportal
```
译文：
```text
魔法大爆炸纪事(3)：远行传送门
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Angolwen	安格利文	T.PN.PLACE	places	nil	preferred	core	维护者于 2026-08-25 裁定统一为“安格利文”；“安格列文”已被取代
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Armoury	护甲店	T.GAME.ENTITY	places	entity name	existing	core	城镇商店实体
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
uber	觉醒技	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	高阶/觉醒技能类别
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
