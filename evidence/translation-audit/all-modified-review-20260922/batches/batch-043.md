# batch-043：10 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01282
位置：mod-tome.lua:17791；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Many are the tales of how our world was made, from the absurd to the romantic to the horrific. But they are all mere myths, with no more than seeds of truth to even the most reliable. The history of our race goes back far, but it is tantalisingly scant in details from before we met the other races. Indeed, it is only through our battles with the others that we halflings have any ancient records at all.

The elves one would suspect of having the greatest knowledge of elder times, but they are aloof and silent. One must judge from this that either they do not know, or that the truth ashames them. The latter would certainly not surprise me.

The humans have more myths than they have brain cells. It seems that each village has several versions of their own local tales, usually passed down orally over the ages. It is clear that not a single element of any of their myths can be construed to contain any essence of the truth.

The dwarves are reticent about the subject of how they were made. They say that such talk is "not profitable". However upon further pressing (and bribing) they will open up a little further. They as a race are of the most fervent belief that they were the last people to be made in Maj'Eyal. They say they are the "final product". Their word for all other races in fact translates directly to "prototype". This mostly singular outlook does of course seem absurd, but one need only look at the rest of dwarven society to see that they are an absurd race with ridiculous ideals. If they are what they consider perfection then I thank whatever god made me that I am flawed!

The subject of gods is of course a difficult one. Clearly there are no divine forces at work in the world today. But the world as we know it did not come from nothing, and even the great Sher'Tul clearly did naught more than manipulate the world - they did not make it.

By logical conjecture one can only presume that some great being made the world. This must have been a benevolent being, for it is clear that "He" created creatures separate from himself to walk the earth. Clearly this is we halflings. We are the only race that truly appreciates the world. We do not warp it with magic experiments like the Shaloren, nor hide from it like the Thaloren. We do not bring destruction like the orcs, or petty greed like the dwarves. And our understanding and knowledge is so far advanced than the humans that it is hard to understand why we share the same world with them at all. We were quite clearly the first of the current races to be created, and our natural feelings of entitlement to all there is in Maj'Eyal must stem from this.

Now that this has been clearly analysed in logical terms, one must consider the source of the other races. It is impossible that they were made by the same god - truly impossible. What strange being could create our race, so gifted and rounded, and yet make such warped and twisted creatures as the dwarves and humans? No, clearly other gods were responsible, lesser gods than our own which copied his grand design. But with fudging fingers and inelegant touches the works of their design were clearly far inferior to the subtleties and perfection which crafted us.

However there remains the matter of the Sher'Tul. Clearly these were of greater power than us, and yet they disappeared. One must presume that our god made this race before us, but was somehow unhappy with them, and so removed them and made us instead. We are not as powerful as the Sher'Tul - not yet at least - but we have our own gifts that evidently give us a greater place in our creator's heart. This would explain why we were the first race to unlock the powers of the Sher'Tul farportals. We had a natural affinity to the works of our elder brethren.

So what happened to these gods after they had made the races which we see today? One must presume strife between them, and that they killed themselves, or took their battle away from the world. Our creator, seeing the other gods killed or left, must have then entrusted the world to us halflings, knowing that we would rule over it in his stead. This is why at every point in history we have played a pivotal role in the shaping of our world. It is our rightful inheritance, and it is our duty to rule it well.
```
译文：
```text
关于这个创世的故事有许多版本，有的荒诞不经，有的浪漫无比，有的则令人恐惧。但他们都只不过是神话而已，即使其中最可信的也只包含些许真相的种子。我们的种族历史悠久，但是与其它种族有交集前的历史记载较为稀少。事实上，唯有通过与其它种族的战争，我们才留下了这些古老的记载。

精灵们可能拥有关于古代历史最多的知识，但他们对此沉默寡言。一种普遍的推测是真正的历史要么就并不为其所知，要么就是会让其蒙羞而被故意隐藏了起来。而后者一点都不会让我们感到奇怪。

人类稀奇古怪的传说比他们的脑细胞还多，他们的每个村庄都有数个版本的创世故事，这些故事通常都是经由祖祖辈辈们一代代口述而流传下来。很明显，这些故事都没有根据，毫不可信。

矮人们则对他们的起源保持着奇怪的沉默。他们宣称讨论历史“不能盈利”。但在进一步施压（与贿赂）后，这些家伙也是会透露一点细节的。他们的种族内普遍认为自身是马基·埃亚尔里最后被创造出的——被称为“最终之作”。在他们的语言中其他的种族被称为“原型”。这个观点真是荒诞，而且我们只需一眼就能发现矮人的本质，他们本就是个有着可笑形象的荒诞社会，如果他们真是神最完美的作品，那感谢神明在我身上创造的缺陷！

对于神明的研究当然是道难题，苦于今日并没有发现什么神圣力量残存于世。可是世界并不是凭空创造出来的，就算是伟大的夏·图尔也只是凭着自己的意愿改造世界而已，他们并没有创世。

先从理论上来看，只能推测出是一种伟大的存在创造了这个世界。他一定亲切又和蔼，因为很明显他创造了大陆上繁荣的生命，而我们半身人正是他伟大的产物。我们可以说是唯一真正能够欣赏这个世界的种族。我们不会像永恒精灵一样用奇怪的魔法力量扭曲这个世界，亦不会像自然精灵一样消极避世。我们不会像兽人一样带来无尽的破坏，也不会像矮人一样贪婪无度。而且，我们所理解和掌握的知识比起人类来实在先进太多，真不明白为何要和他们分享同一个世界。我们半身人一定是现存种族里最先被创造出来的，这显然赋予了我们对马基·埃亚尔天然的所有权。

现在从逻辑上来说已经很清楚了，必须考证其他种族的起源。因为他们不可能由同一个上帝所创造——真的不可能。是什么神奇的存在创造了我们的种族，使我们如此全面而有天赋，然后再创造那些畸形扭曲的生物，比如矮人和人类？不，很显然其他创造者也很负责，但比起我们的创造者来差了一些。只要通过对比我们和他们手工制作的“艺术品”就可以看出，他们是多么的粗糙不堪，而我们是多么的完美。

然而夏·图尔的存在又该如何解释。很显然那是比我们更加强大的种族，尽管他们已经消失了。可以肯定我们的创造者在我们之前制造了他们，但是可能不满意他们，于是将他们移除，另外创造了我们。虽然我们没有夏·图尔人那么强大——至少目前还没有——但是我们有自己的天赋，显然在我们伟大的创造者心中占有着更重要的位置。这样就可以解释为什么我们是第一个打开夏·图尔传送门的种族。因为我们和我们的兄弟种族有着天然的联系。

那么在那些神创造了这些种族后又发生了什么？肯定是他们之间发生了纠葛，或者他们同归于尽，亦或是他们的战场远离了这个世界。我们的创造者，看到其他众神，或是被杀或是离开，肯定是将这个世界委托给了我们半身人，因为他知道我们将代替他掌管这个世界。这就是为何在历史的每一个节点上，我们都在世界的塑造中扮演了关键角色。这是我们当之无愧的继承权，治理好这个世界也是我们的职责。
```

## entry-01283
位置：mod-tome.lua:17826；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Eyal was raised from Darkness,
And One came who made a blinding light called Sun,
But Eyal flinched and said, "It is too bright!"
So Gerlyk spun Eyal around; thus his face was half-time in light and half-time in shadow,
But in shadow Eyal became lonely and cried.

And so Gerlyk made him two younger sisters who danced around Eyal
And kept him in good spirits.
But the moonsisters became jealous of their brother's affection,
Threatening to fight and scream.
Thus Gerlyk separated them so that Eyal would only ever dance with one at a time.

In the summer Eyal dances with the moonsister Altia.
She sings songs of joy and laughter,
And brings friends and family together,
And she glows yellow with mirth.
In the winter Eyal dances with the moonsister Felia.
She tells tales of times begone,
And makes men walk alone in thought,
And she glows blue with solemness.

But in the time between,
When both sisters are slimly seen on each side of Eyal,
Glaring at each other from behind their brother's belly,
Then the world goes still, and the winds hold their breath, and the oceans lie flat.
For this is the Time of Balance, when the Darkness rises deepest, and all life is in peril.
Aye, and Gerlyk did say, "Let no man walk abroad this night, lest Darkness catch him and take him forever."
Aye, and Gerlyk did walk abroad that night, into Darkness beyond, and has ne'er since been seen.
```
译文：
```text
埃亚尔从黑暗中升起，
创造者制造了一团耀眼的光叫做太阳，
但是埃亚尔认为这团光过于刺目，
于是盖里克让埃亚尔自转起来；这样它的面孔一半时间沐浴光明，一半时间沉入黑暗，
但是埃亚尔黑暗的那面感觉很孤单并伤心的哭泣。

所以盖里克为他造了两个妹妹，她们围绕着埃亚尔起舞，
让他保持好心情。
但是月亮姐妹开始争风吃醋，妒忌对方得到哥哥的宠爱，
以武力威胁并大声嚷嚷。
于是盖里克将她们分开这样埃亚尔只能和其中一位跳舞。

夏天埃亚尔和月亮女神亚缇娅共舞。
她笑着唱着快乐的歌，
让朋友和家人欢聚，
她闪耀着欢乐的金色。
冬天埃亚尔和月亮女神菲莉娅共舞。
她讲述着往昔的故事，
使人们独自行走在沉思中，
她闪耀着肃穆的蓝色。

但在交替之时，
两姐妹只能在埃亚尔两端，
隔着哥哥的身躯互相怒视。
世界在这一刻静止了，清风不再吹拂，大海也不再掀起波澜。
这就是平衡日，是黑暗最深的时刻，万物都处在危险之中。
盖里克说：“没有人能走入今晚的黑夜，否则黑暗将抓住他并使他永坠黑暗。”
然后，盖里克走入了这样的黑夜，进入了无尽的黑暗，并再也没出现过。
```

## entry-01284
位置：mod-tome.lua:17883；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Death is nearing. I can feel her chilling breath down the back of my neck. So many of us firstborn have passed on already. I cannot allow it... I will not let myself rot into dirt like the others. I am the mightiest of the Shaloren - I have a right to life!

```
译文：
```text
死亡正在逼近。我能感到她在我脖子后面冰冷的呼吸。我们这些首生者中已有许多人逝去。我不能容忍……我不会让自己像其他人一样化为尘土。我是最强大的永恒精灵——我有权活下去！

```

## entry-01285
位置：mod-tome.lua:17885；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Death mocks my experiments. I can preserve the flesh of my servants, tightly wrapped and salted, treated with the correct chemicals. I can animate them, make them shuffle about the empty halls of my mausoleum. But they are but empty shells, devoid of any soul. Is this how my majesty is to end? I demand a greater fate...

My days are numbered. Each night that passes saps strength from me. I must find the way to preserve my soul within my flesh. My greatness cannot be allowed to fade.
```
译文：
```text
死亡嘲弄着我的实验。我可以保存侍从们的血肉，将他们紧紧包裹、以盐腌渍，并用正确的化学药剂加以处理。我可以驱动他们，让他们在我陵寝空荡的厅堂间蹒跚游荡。但他们不过是没有任何灵魂的容器。这意味着我的霸业要结束了？我要求一个更伟大的命运……

我的日子屈指可数。我的力量随着每个夜晚逐渐流逝。我必须找到将灵魂保存在肉体里的方法。我的伟大绝不容许消逝。
```

## entry-01286
位置：mod-tome.lua:17921；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I fell asleep in a dark hollow, but my sleep was troubled by terrible dreams. The dreams are so vivid in my mind!

I saw the red star, and it became a land of fire floating in the night sky, full of black creatures with yellow eyes and hungry red mouths. And beyond the red star, far beyond was a dim world, but fractured and split all about its surface. As the world spun the split continents crushed against each other, and lava spilled up, and lands sunk into the ground. Demonic mouths screamed up as they disappeared into fiery death. It was if the world was tearing itself apart, but some force of will was desperately trying to keep it held together.

And I saw then in the centre of the world, as it spun and crumpled and crunched, a vast figure with a horned head and outstretched limbs and shining white eyes. It held tight to the innards of the world, holding it together against forces threatening to pull the whole planet apart. The giant face contorted and screamed in pain and fury.

“Urh'Rok,” a deep voice spoke within my head. “Our god, our saviour, holder of our world. In the name of Urh'Rok we seek vengeance against Amakthel and the Sher'Tul. The petty world of Eyal shall fall!” And then I woke up, and I felt sure something was nearby, looking for me. I fled instantly.

Am I going mad? The name “Urh'Rok” still rebounds through my skull and my vision is dimmed. Perhaps I have been wearing this ring too long...

Yes, yes, this is all clearly an illusion! A strange nightmare that I shall wake up from. I shall take the ring off, and go visit the lovely moonstone again. Once I see the stars all shall be well...
```
译文：
```text
我在一片黑暗的山洞中渐渐睡去，但是我的睡眠被一个可怕的梦吵醒了。即使刚睡醒的脑袋仍然一团浆糊，那个梦仍然在我的脑海中异常清晰。

我看到眼前红色的星星越来越大，原来，那是一片在夜空中漂浮着的燃烧的大陆，上面满是有着黄色眼睛和贪婪的红色大嘴的黑色生物。在红色星星的上方遥远的地方是一片黑暗的世界，但是那个世界似乎被某种力量切得支离破碎。在这个世界旋转的过程中，破碎的大陆互相撞击，岩浆的波浪浮浮沉沉，陆地沉入地底。我听到恶魔般的吼叫，那是大陆上的生物被烈火吞没时的绝望呻吟。似乎这个世界被完全撕裂开来，但是某种意志的力量努力试图将他们固定在一起。

视野中，随着这个世界逐渐旋转，逐渐被挤压碎裂，我隐约能看到那个世界的中心。在那里，是一个拥有闪烁的白色眼睛，头上长角的巨大影像。它向外伸展而出的强壮四肢紧紧抓着世界的核心，试图将它连结在一起，来对抗那些不断将这颗星球撕裂的可怕力量。在剧烈的痛苦和愤怒中，巨人的表情被其扭曲，发出怒吼。

“乌鲁洛克，”一个深沉的声音在我的脑海中响起。“我们的神，我们的救世主，保护世界之人。以乌鲁洛克的名义，我们将向阿马克泰尔和夏·图尔人复仇。渺小的埃亚尔世界终将陨落！”我被噩梦所惊醒，直觉告诉我有什么东西就在附近，正在搜寻着我。我立刻拔腿就跑。

是我的脑子出了什么问题吗？那个奇怪的名字，“乌鲁洛克”仍然在我的心头回响，我的视野也变得昏暗起来。大概是我戴了这个戒指太久了的副作用的缘故……

唉，对，这一定是我的幻觉！我早该从这个怪梦里醒来了。我应该赶紧脱下这个该死的戒指，回去看看我可爱的月亮石们。只要能让我看见美丽的星空，一切都一定会好起来的……
```

## entry-01287
位置：mod-tome.lua:17943；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Introduction
```
译文：
```text
博学者格雷诺特关于种族的调查——引言
```

## entry-01288
位置：mod-tome.lua:17944；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
I set out here to give a full and complete analysis of all the intelligent races in Maj'Eyal. This is an ambitious project to say the least, but it is put together from a great many years labour, including travels across all the kingdoms and direct meetings with many of the highest rulers and most learned sages. I have drawn my findings from common knowledge, exclusive interviews, and studies of many thousands of pages of texts and histories, some going back dozens of centuries.

I myself am a Higher human, in the employ of the court of King Tolak the Fair, but I have done my best to write all accounts from a purely neutral standpoint. I leave it to my peers to judge my success.

Index:
Chapter 1 - Humans
Chapter 2 - Halflings
Chapter 3 - Dwarves
Chapter 4 - Shaloren
Chapter 5 - Thaloren
Chapter 6 - Naloren (extinct)
Chapter 7 - Ogres
Chapter 8 - Orcs (extinct)
Chapter 9 - Sher'Tul (extinct)
Chapter 10 - Monstrous Races
Chapter 11 - Dragons

```
译文：
```text
我从这里开始，来对马基·埃亚尔大陆上的所有智慧种族进行充分和全面的分析。尽管这是一项庞大的计划，不过它已经有了许多年的准备，包括我在马基·埃亚尔各王国的旅途中与许多最高统治者和最博学的圣贤们的当面会晤。我从众人所知的常识、独家采访以及数千页典籍与历史——其中有些甚至可以追溯到数十个世纪前——中进行资料的搜集和整理。

我自己就是一个高等人类，效力于公正之王托拉克的朝廷，但是我尽量从纯粹中立的角度来叙述各个种族的历史。我等着同行们对我的工作进行评价。

目录：
第1章 - 人类
第2章 - 半身人
第3章 - 矮人
第4章 - 永恒精灵
第5章 - 自然精灵
第6章 - 纳鲁精灵（已灭绝）
第7章 - 食人魔
第8章 - 兽人（已灭绝）
第9章 - 夏·图尔人（已灭绝）
第10章 - 怪物种族
第11章 - 龙族

```

## entry-01289
位置：mod-tome.lua:17977；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Chapter 1 - Humans
```
译文：
```text
博学者格雷诺特关于种族的调查——第一章——人类
```

## entry-01290
位置：mod-tome.lua:17978；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

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

在黄昏纪的魔法狩猎与瘟疫之后，马卓普人几乎灭绝。他们以强大的施法者著称，也因此成为猎魔者的首要目标。不管怎样，他们的血统特征——火红的头发以及生有雀斑的皮肤，仍会出现在遥远后裔的身上。有部分传言说他们仍住在某些遥远的地方的城堡或高塔里。

高等人类基本身高在6英尺左右，有着金色的头发、白皙的皮肤和蓝色或灰色的眼睛。大多数学者都是高等人类，贵族阶层也大多由他们占据。有人说这都是歧视和精英理论所导致的，虽然这可能只是简单的嫉妒情绪。也有传言说高等人类的高智商是厄流纪时期孔克雷夫法师们的实验成果，但是我找不到任何证据来支持这一论点，我只能认为这种说法毫无根据。高等人类的血统被认为是优秀的标志，与低等血统通婚则为世所不齿。

在烈火纪，勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子公正之王托拉克的手中。一份关于人类漫长历史的全面报告需要更加详细的文本来叙述。
```

## entry-01291
位置：mod-tome.lua:17999；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Chapter 2 - Halflings
```
译文：
```text
博学者格雷诺特关于种族的调查——第二章——半身人
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Gerlyk	盖里克	T.PN.PERSON	society	_t	preferred	core	人类造物主专名；统一巅峰剧情、虚空任务及创世传说，不写作“加莱克”
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Sholtar	肖尔塔	T.PN.PLACE	places	nil	preferred	core	维护者于 2026-08-25 裁定统一为“肖尔塔”；“肖塔尔”和“肖塔”已被取代
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
age of pyre	烈火纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	global	1.8beta 的统一译法；替换“派尔纪”
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flat	固定伤害减免	T.GAME.EFFECT	combat	effect subtype	preferred	global	flat damage reduction 机制；与正文'固定伤害减免'一致（P0 复审子代理 #83，用户确认）
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
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
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
