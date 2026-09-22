# batch-046：9 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01308
位置：mod-tome.lua:18137；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

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
任何完整的著述都少不了至少简要提及那些肆虐于我们世界的野蛮种族。他们没有任何值得一提的文明社会，一般来说也不具备高等思维或文化，但是对于那些热衷于分析低等智慧生物的人而言，他们仍然值得研究。

巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。岩石巨魔生活于东北部的山脉地区，有些为了寻找食物和散播暴力甚至走到了更远的地方。他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。森林巨魔生活在浓密的森林和沼泽中，在德斯镇东部的巨魔沼泽尤为臭名卓著。他们比岩石巨魔同胞有着更为敏捷的速度和更为发达的言语能力，并且以移动迅速和能够使用精工武器闻名，尽管他们泛绿的外皮没有那么厚实，肌肉也不如岩石巨魔发达。所有的巨魔有着快速的新陈代谢能力，再严重的伤口，恢复只要几个小时。据测量，他们在出生时只有8英寸长，但是在2年内他们就可以成长完全，并且很少有寿命超过10年的。他们一开始被认为仅比野兽好一点，然而在烈火纪时，他们被兽人当做战士般训练，甚至学习了一些基础语言和战术，使得他们更加危险。虽然兽人已经走了，但他们的仆人仍然存在，并且他们偏远的繁殖地和极高的出生率至今仍挫败着彻底根除他们的企图。

巨人们通常住在岱卡拉周围的山峦中。他们在体型上有着很大的差异，但基本上不会低于10英尺高。他们看起来就像是具有浮肿面部特征和更长的四肢的放大人类。他们属于游牧部落，随着季节的变化，从一个山头迁移到另一个山头，以鹿和羊为食。他们通常是和善的生物，只有当他们的领土受到入侵或者他们的后辈受到威胁时才会变的具有攻击性。有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击市民，但是这极其少见并且大多发生在极端的严冬。巨人们似乎没有值得一提的优越文化和语言，但是却向我们揭示了有限智慧的运用和团结一致的精神。

娜迦曾被认为仅存于神话中，但是据可靠消息以及死亡的标本表明他们是真实存在的。他们的上半身是人形，有着金色的头发和苗条的身段，但是下半身却极像一只巨蛇的尾巴。他们大约身高6英尺，尽管他们的尾巴可能更长。他们在马基·埃亚尔的东岸和东南岸都有踪迹，这似乎表明波涛之下存在着某种异域文明。近几百年才有关于他们的记载，而且只是近来人们才开始认为他们不只是醉酒水手的荒诞幻想。他们可以在水里和陆地上呼吸，同时拥有肺和鳃，并且据说在陆地上有着非常惊人的速度。有人可能认为它们只是特殊的怪物，但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。现在还不知道他们是否有复杂的语言，但是他们目前的对外回复只是极端的暴力，并且东海的渔民们经常要提防碰上这些邪恶的生物。

恶魔的起源尚未完全清楚，但是很显然他们具有某种智慧，所以我觉得有必要在此写下一段。众所周知，他们是由某种魔法仪式召唤而来，并且在黄昏纪时期，小恶魔们经常受雇于邪恶的巫师。最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。那必然是一个地狱般的地方才能容下如此多恐怖的生物。恶魔们在外观和能力上不尽相同，正如我们世界里的生物一样。他们通常流着泛蓝的血液，血肉与皮肤呈金属质感，往往会与我们的空气产生奇异反应——有些燃起火焰，有些释放出可怕的酸液或喷吐出黑暗之云。他们似乎都在某种程度上通晓魔法，并且他们之中最强者具有真正可怕的力量。幸运的是他们是非常罕见的种族，而且自从魔法淡出人们的视野后，出现的更加稀少了。
```

## entry-01309
位置：mod-tome.lua:18154；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Loremaster Greynot's Analysis of the Races - Chapter 11 - Dragons
```
译文：
```text
博学者格雷诺特关于种族的调查——第十一章——龙族
```

## entry-01310
位置：mod-tome.lua:18155；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The common man may scoff at the idea of classifying dragons as an intelligent race, but experienced wyrmics know otherwise. Dragons are incredibly long-lived creatures, with some known to survive for thousands of years. Though in their early life they are of a bestial nature, as they advance through the centuries they gain an ever keener and more developed intellect. The eldest of wyrms are sometimes considered the most subtle and intelligent of creatures in Maj'Eyal, capable of telepathic communication and advanced mental abilities, and wyrmics speak of them with the highest reverence.

Dragons come in many shapes and sizes, normally growing from 5' long hatchlings to 20' long mature drakes, with some of the greatest wyrms growing to over 40' in length. They are generally winged, with large lizard-like maws and sharp talons on both their fore and hind legs. They are often noted for the lustrous colour of their scales, normally representing an attunement to one of the key Elements of Eyal. This attunement is unseen in any other race, and some philosophers believe that dragons predate all other races, being formed as raw representations of the elements of nature at the beginning of the world. However this theory may be borne purely from the fanatical delusions of certain wyrmics who have studied the creatures for too long.

All corners of Maj'Eyal show some trace of different types of dragons. The Daikara Pass and surrounding mountain chains are home to a great number of ice and storm dragons. Numerous sand and red dragons can be found in the western desert and hills, and many have been the reports of gigantic sea dragons in the deepest oceans, especially to the south.

Attacks from dragons on humans and halfling settlements are fairly rare, but when they occur they can be truly devastating. Usually they are to feed on livestock, but now and then come attacks from newly matured drakes, seeking out precious metals and gemstones to build up a hoard. Dragon hoards have become a thing of legend, with the greatest wyrms rumoured to protect literal mountains of gold, but in modern times truly sizeable hoards are rare. The dwarves farmed hoarding dragons almost to extinction in the Age of Allure, and most dragons these days retain only modest treasures in their lairs.

Dragons are regularly hunted for their thick scales and their elementally imbued bones. Dragonskin leather is prized amongst armour-workers, as when properly treated it is both light and tough, and oft retains some inkling of the original wyrm's power. Dragon-bone is highly favoured by staff-crafters for its natural attunement to elemental forces, and is sometimes used by fletchers in the crafting of the most delicate yet resilient bows and arrows. However the hunting of dragons for their skin and bones is greatly opposed by many wyrmics, and there is an increasing market for "naturally harvested" drake materials - those taken from dragons which have died of natural causes. Still, demand for all dragon materials is strong with exceptionally high prices paid, and many are the greedy souls that lose their lives each year at the fangs and claws of these magnificent creatures.
```
译文：
```text
一般人也许会嘲笑我把龙作为单独列出的智慧种族，但是经验丰富的龙战士们知道其实不然。龙族是另人难以置信的长寿生命，某些已知的龙族已经存活了数千年之久。尽管在他们早期的生命中，他们兽性的一面比较多，但是随着他们生活几个世纪以后，他们会获得前所未有的超强理解力。那些远古巨龙有时被认为是马基·埃亚尔最狡猾和富有智慧的生物，他们拥有心灵沟通和优秀的精神能力，并且龙战士们始终对龙族有着最崇高的敬意。

龙族有着不同的大小和形状，一般常见于5英尺长的幼仔到20英尺长的成年龙族，某些最强大的龙族体长能达到40英尺。他们通常是带翅膀的、有着蜥蜴般的巨口，前后肢都生有锋利的巨爪。他们通常有着鲜艳色彩的鳞片，通常代表与埃亚尔某种元素的亲和。这种亲和力在任何其他种族都未曾出现过，有些学者认为，龙族先于其他一切种族存在，是在世界之初作为自然元素的原初具现而形成的。然而这个理论只有那些狂热的研究了龙族太久的龙战士信徒们才会相信。

马基·埃亚尔的每一个角落都能发现不同类型的龙族。岱卡拉山脉聚集了很多的冰龙和风龙。大量的沙龙和赤龙可以在西部沙漠和丘陵中找到，并且还有许多报道提到在大洋深处有着巨大的海龙，尤其是在南部地区。

龙族攻击人类和半身人聚居地的事情是少见的，但一旦出现这种情况，通常是毁灭性的灾难。通常它们是为了找牲畜吃，但有时也有来自成年巨龙的攻击，是为了寻找贵金属和宝石来作储藏。龙族的财富已经成为了一种传奇，传说那些最伟大的巨龙守护着真正成山的黄金，但是现在如此多的宝藏几乎没有。矮人们在厄流纪大肆猎捕囤积财宝的龙，使这一类龙几乎绝迹，现在的大部分龙族在巢穴里只有适量的财富。

龙族经常由于它们厚实的鳞片和蕴含元素之力的骨头而被狩猎。龙皮革是护甲制作者们珍视的材料，因为经过适当处理后它既轻便又坚韧，并且通常保留着原龙的一丝力量。龙骨是法杖制作者们最喜爱的材料，因为它与元素力量的天然亲和极高，有时也被用于制造纤薄且柔韧的弓箭。然而，对龙族的不断狩猎引起了许多龙战士们的强烈不满，并且交易“自然采集”的龙族材料的市场也日益增多——那些人只取自然死亡的龙族身上的材料。尽管如此，各类龙族材料的需求依然旺盛，价格也高得惊人，每年都有许多贪婪之徒丧生于这些壮丽生物的尖牙利爪之下。
```

## entry-01311
位置：mod-tome.lua:18207；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Running man, running man
Your time is ending soon
Running man, running man
Will not save sun nor moons

Running man, running man
Survival growing slim
Running man, running man
You know your fate is grim

Running man, running man
Now's the time to choose
Running man, running man
Your honour or your shoes!
```
译文：
```text
逃跑者，逃跑者
你的时间不多了
逃跑者，逃跑者
你救不下日与月

逃跑者，逃跑者
生机越来越渺茫
逃跑者，逃跑者
你已获悉残酷命运

逃跑者，逃跑者
现在是时候去选择
逃跑者，逃跑者
你的名誉或你的鞋！
```

## entry-01312
位置：mod-tome.lua:18235；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
In Age of Allure rose an archmage high
With power beyond compare
And the people poor would not come nigh
His dark and terrible lair

Whilst crops fell dead in drought and blight
And children grew diseased
The wizard dread stole in the night
To pillage what he pleased

But a hero came with shining sword
And a will of solid steel
Not seeking fame or high reward
He followed but his zeal

"From Zigur I come on righteous quest
To battle foes arcane
I will not succumb to magic detest
I will end this evil reign"

And so he rode on pure-white steed
To the warlock's hold
That dank abode of dark misdeed
He entered brave and bold

There battle blazed beyond all sight
Sword clashed with spell
Blood was razed in fearsome fight
Scream followed yell

A beam was cast of arcane pure
Piercing mail and shield
But still steadfast with flesh secure
The hero did not yield

A slash tore through the wizard's cloth
His hat dropped to the ground
From loose grip flew his staff so wroth
Thus fell the mage renowned

Now bare of skin and weaponless
Here lay but a man
No arcane sin could now redress
The blood that freely ran

"Fool warlock dead, you were too vain
To gifts of Nature trust
Your faith instead in tools arcane
Now to Nature you are dust"
```
译文：
```text
厄流纪崛起一位大法师
有着无与伦比的能力
贫苦百姓不敢靠近
他黑暗而可怕的巢穴

当作物死于干旱和枯萎
感染疾病的孩童增长
巫师在夜里偷偷的潜入
来掠夺他想要的一切

但是来了一位英雄，他手持宝剑
并且他拥有磐石般的意志
不求名利与荣耀
但求问心无愧

“来自伊格我肩负着使命
打败邪恶巫师是我的义务
我不会屈服于可怕的魔法
我将结束这邪恶的统治”

于是他骑着一匹骏马
向巫师的巢穴前进
幽暗的洞穴吞噬着一切
他却凛然不惧

战斗之激烈难以想象
那是剑与魔法的火花
战斗伴随着鲜血的绽放
怒吼声与尖叫声此起彼伏

一束纯净的奥术射线
撕裂了护甲与盾牌
但他仍坚定信念
英雄永不屈服

刀光划过了巫师的衣袍
他的帽子掉在了地上
法杖也因失去控制而落下
臭名昭著的法师终于陨落

如今赤身裸体、手无寸铁
这里只躺着一个凡人
奥术之罪再也无法弥补
那自由流淌的鲜血

“愚蠢的术士已死，你太过自负
未将信任交给自然的恩赐
你的信念转向了奥术之器
如今你已归于尘土”
```

## entry-01313
位置：mod-tome.lua:18334；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You wake suddenly from your unexpected slumber and attempt to quickly regain your bearings. However, you are not prepared for the bizarre vision that greets you: instead of land and sky you see only amorphous shapes and varying degrees of light. A strange psychedelic haze permeates the air and otherworldly colors and shadows flicker in and out of your peripheral vision. 
As you begin to come to grips with this strange environment, you realize with horror that you cannot move! Your body feels as if it is completely without weight and try as you may you cannot budge an inch. You experience a sense of Déjà Vu as you recall past nightmares of being paralyzed. That's when it strikes you: you never woke up at all, you're still asleep! This epiphany is only reinforced when you notice a strange phenomenon: mirror copies of yourself are being slowly projected from where you stand and are moving about of their own volition.
They all seem to be focused on something in particular, but what? Just as soon as you set your mind to discerning what your dreamselves are focusing on, you feel it. With horror, you realize that you are not alone here. 
Somehow, your foe has invaded your very subconcious and is attacking you in your dreams. Still unable to move, your lucid mind races on how to handle such an insane and horrible situation. On a whim you concentrate on one of your projections and you find that you can control it. 
Free now to face this nightmare, you turn to find your foe. While you have a sense that having one of your dreamselves destroyed may not by itself be catastrophic, what would happen if several or many are cut down? Unwilling to find out, you resolve yourself to end this offensive intrustion into your mind.
```
译文：
```text
你从意料外的沉睡中骤然醒来，试图尽快辨明自己身在何处。然而，你对眼前离奇的场景毫无准备：没有陆地，没有天空，只有不断变化的形状和光线。迷幻的烟雾弥漫在空气中，各色阴影在视野中飞舞……
当你的眼睛渐渐习惯这幅奇怪的场景时，你惊恐地发觉你动不了了！你的身体似乎完全没有重量，任你如何挣扎也移动不了一寸。更奇怪的是，当你回想起麻痹的噩梦时，有种似曾相识的感觉，正当此时，你忽然意识到：自己根本没有醒来，仍处于沉睡之中！你突然注意到奇怪的现象，让你更加确信这一点：你自己的镜像正在逐渐从你站的位置产生，并自主行动。
他们似乎都集中精神于某个东西，但那个是什么？正在你思考你的梦中自我在关注什么时，你感觉到了它。你惊恐地意识到，这里不止你一个人。
你的敌人侵入了你的潜意识，开始在梦境中攻击你。虽然依旧不能动，但你的大脑也开始思考如何在这疯狂而恐怖的处境下存活。当你试着集中精神到你的梦中自我上时，你发现你能够控制它。
终于能自由行动去面对这场噩梦，你转身寻找你的敌人，虽然你感觉到让你的一个梦中自我被摧毁似乎不会成为灾难，但如果有数个乃至许多个梦中自我相继被摧毁呢？那会发生什么，你不愿去探究，于是下定决心终结这场对你心灵的侵犯。
```

## entry-01314
位置：mod-tome.lua:18345；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Dear graverobber,

Try to be a little faster next time.

Love, #{italic}#Eden#{normal}#
```
译文：
```text
亲爱的盗墓贼，

下次记得快一点。

你钟爱的#{italic}#艾登#{normal}#
```

## entry-01315
位置：mod-tome.lua:18375；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}#How to Summon a Phoenix#{normal}#
	  10 pouches faeros ash
	  5 vials fire wyrm saliva
	  3 red crystal shards
	  3 pouches bone giant dust
	  1 vial greater demon bile
	  1 skeleton mage skull
	  pinch of luminous horror dust

This is a long and complex ceremony, and all steps must be followed precisely if you wish to succeed. Heed well that for the errant fool who takes on what they cannot finish, there will be consequences. To play with fire and assert your dominance over the flames comes with risks if you overestimate your power. 
	
The ritual begins with a vessel; any man will do. Bind them in place with flame secure bindings, and give a sound gag. The gag isn't strictly necessary, but the screams of agony tend to be quite distracting and inspirit mistakes after a few days.

Take 2 vials fire wyrm saliva and dissolve 2 pouches faeros ash in each. Be sure to dissolve completely. A few fireballs at the vial can do the trick if they're stubborn. Using one of the prepared vials, begin to etch the saliva in the skin of the vessel, heating it so that it brands the shape of --- 

#{italic}#The remainder of the scroll has been singed into a pile of char, illegible and scattering into a cloud of ash as you grasp it#{normal}#
	
```
译文：
```text
#{bold}#如何召唤凤凰#{normal}#
	  10袋法罗的灰烬
	  5瓶火龙涎
	  3块红色水晶碎片
	  3袋骨巨人骨灰
	  1瓶大恶魔胆汁
	  1个骷髅法师头骨
	  一小撮金色恐魔的粉尘

这是一个漫长而复杂的仪式，如果你想要成功的话，就必须严格遵循所有的步骤。要知道，自视过高的蠢材如果冒险进行自己没有能力掌控的仪式，一定会迎来自己应得的下场。如果你高估了自己掌控火焰的力量，那么等待你的只有玩火自焚的结局。

仪式需要一份祭品，随便哪个人都可以。用防火胶布把他绑住，塞住他的嘴巴。虽然塞住嘴巴这一步不是必须的，但是那个人痛苦的惨叫会让人相当分心，几天下来容易让你在仪式中出错。

取2瓶火龙涎，每瓶各溶入2袋法罗的灰烬。一定要充分溶解。如果还有没有完全溶解的部分，就往瓶子里放几个小火球。使用一瓶准备好的溶液，用火龙涎在祭品的皮肤上蚀刻，加热使其烙出——的形状——

#{italic}#卷轴的剩余部分已经被烧焦了，无法辨认。当你抓到这份卷轴的时候，那些残存的纸页就化为了灰烬#{normal}#
	
```

## entry-01316
位置：mod-tome.lua:18410；section：mod-tome/data/lore/misc.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your arcane abilities have been interfered with!

Eyal is a torn world, and the forces of nature can react strongly to the arcane energies that seek to manipulate them. Some items and areas are imbued with anti-magic, a natural energy that disrupts magical abilities and effects. There are even those who have learned to harness anti-magic into their own wild abilities, and who use them to hunt down and destroy those who practise magic. So beware, caster! It is a hostile world ye wander in.
```
译文：
```text
你的奥术能量被干扰了！

埃亚尔是一个被撕裂的世界，自然力量会对试图操纵它们的奥术能量产生强烈反应。某些物品和地方被灌输了反魔力量，这是一种能干扰魔法能力和效果的自然能量。甚至还有一些人学会了驾驭反魔力量，将其融入自身的野性能力中，用于猎捕并摧毁魔法使用者。小心，施法者！你漫游的世界并不友好。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Facial features	脸部特征	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Slumber	沉睡	T.GAME.EFFECT	combat	_t	preferred	core	状态名；与同名技能统一
Slumber	沉睡	T.GAME.TALENT	talents	talent name	preferred	core	技能名；指睡眠状态，不是催眠动作
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Trollmire	巨魔沼泽	T.PN.PLACE	places	_t	preferred	core	任务与地点叙述统一；troll 指巨魔，不是食人魔，与 narrative.tsv 的 trollmire→巨魔沼泽 一致；“Of trolls and damp caves”是任务标题，不作同名处理；2026-09-16 用户裁决，由 existing 升为 preferred
Wyrmic	龙战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
age of pyre	烈火纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	global	1.8beta 的统一译法；替换“派尔纪”
animal	动物	T.GAME.ENTITY	creatures	entity type	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
derth	德斯镇	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
luminous horror	金色恐魔	T.GAME.ENTITY	creatures	entity name	preferred	core	核心实体名称；与 radiant horror“光芒恐魔”区分
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
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
scroll	卷轴	T.GAME.ENTITY	items	entity type	existing	global	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
slumber	沉睡	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	深度睡眠技能类型；与施加催眠的动作区分
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
trollmire	巨魔沼泽	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	与同类手札标题统一；troll 指巨魔，不是食人魔
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
