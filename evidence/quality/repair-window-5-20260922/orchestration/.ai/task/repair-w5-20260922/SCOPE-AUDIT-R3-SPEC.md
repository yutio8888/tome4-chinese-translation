# 修复窗口5：250—251的18条已确认译文

模式implement，Paseo MCP，schema5 translation_contextual_v2。用户持续授权审核、修复和推送；机制高影响问题触发251安全边界提前修复。两个来源批次均已finalize并推送，基线29bac12f03dba82f6da158ec61e8bfdbdfac7e63。

唯一EXECUTOR只可修改mod-tome.lua下列18个source/section/source_tag的target，以及evidence/quality/repair-window-5-20260922/的本窗口证据。初次实施禁止handoff/catalog/migration操作。不得修改其他译文、术语、规则、工具或旧证据；不得stage/commit、写.ai或创建agent。保留baseline全部无关文件。

两个真实repair preflight共16条正式候选；另2条来自251独立宿主补充。WORKSET为有界组合，不冒充单一生产批次。SOURCE-CLAIMS仅供实施，不提供给独立reviewer。SOURCE-ANCHORS为固定公开源码，TERM-SNAPSHOT按精确行语境使用。

固定源码624a67329fe2ad440c5b344785a9c73fcf22ae63；全部tome。保持source/source_tag/args_order/special、printf/markup不变。唯一布局例外e56b636891：target从2LF/6TAB恢复source的1LF/2TAB，取消首段中间额外分段，并让伤害加成句前仅保留原文换行和两个TAB；其他target的LF/TAB保持baseline。无术语库/全局策略改动。Archmage类名、人物音译、旧pending及RW1-SIB-01/02均排除。

回忆录323606655f仅修188星云位于高台上方及所有表面发光；e5dc6a60be仅修350死亡人数、352灾变指代、362医生严令和已确认直接引语句末标点。禁止全面重写或自动接纳旧164/198/210观察。啃噬仅恢复感染后后续死亡分支限定，不否定直接击杀生成分支；失衡值必须兼容正负变化；精神暴击可治疗，不限定攻击。

验收：LuaJIT加载仅18个target变化，其他记录一致；严格lint、strict claims registry、空白和不变量检查；proposal若产生须strict。每个数值占位符列index/quantity_kind/producer/consumer，机制须方向值流证据。四成员独立v2 REVIEW和最新whole-workset FINAL_REVIEW；完整17门禁/严格构建和DONE_VERIFIED。译文commit→queue rebuild→单次catalog/migration→证据commit→queue rebuild→push；successor重新审核，之后继续252。主代理负责完整门禁。

17个section anchor仅定位工作集，不扩大范围。

## 323606655fb0b28b2c29b00cb042c85bf7b8f6275a6d327194b05db0b076bfd3

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/lore/elvala.lua
source_tag: _t

source: #{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Three: The Farportal#{normal}#

“Why are ye not leader?” asked Linaniil, resting her head in her hand with her naked form strewn across my bed.
 
I looked at her, surprised by the sudden question.  My mind struggled briefly with the strange query, still recovering from the heat of sex but a minute before.  “Why should I be leader?” I asked back.
 
“Because ye are strong, of course,” she responded.  “I deem ye stronger in battle than any of your kin.  Ye should rule with such strength.”
 
I chuckled softly.  “Mere strength is not enough to rule a people.  It requires responsibilities, careful decision making, and above all – politics.  I have no interest in such matters.  Ephinias is far better suited to those sorts of things.  Give me a sword and soldiers to lead into battle and I am content.  Let the leaders worry about where I should point my blade.”

She was quiet a moment, seemingly dissatisfied with that response.  “Ye are not happy with the current plans though.”

For a moment I was struck with shock.  It surprised me how clearly she divined my inner thoughts.  I had not expressed my concerns to anyone, yet she could so easily read me.  Five weeks it had been since we first met, and it seemed like there was nothing I could hide from her keen sight.
 
The preparations for the Spellblaze were well underway.  Turthel of the Kar’Krul had returned to his northern citadel, but he left his daughters as ambassadors to aid in our designs.  It meant Linaniil and I had many an opportunity to meet, though we kept it secret.  Few of my race would understand or approve of such a liaison, and none of us could afford a scandal. Yet I could not resist this human mage’s advancements, nor she mine.
 
“I am a warrior,” I said to her finally, getting brusquely from my bed and recovering my robes.  “I settle my battles facing my foe, not by toying with relics from afar.  It irks me that we must deal with our enemies in such a craven way.”

“But does it not excite ye, using these Sher’Tul ruins?” she said, putting a finger to her lower lip as she still languished in my bed, the sheets sticking tightly to her bare skin.  She seemed visibly aroused by her thoughts.  “Such powers lain dormant for so long, ready to be summoned to our control...  How it were I to command so great a venture!”

I shook my head sadly as I finished buttoning up my doublet.  “I do not trust those ruins.  We Shaloren are mighty, but we have yet to reach the heights of the Sher’Tul, nor do we truly understand the devices they have left behind.  My thoughts are more with your sister Neira on this.  We should stick to what abilities we have mastered, without stretching ourselves to such grand experimentation.”
 
Linaniil looked at me intently, a touch of humour in her dark eyes.  “If ye were leader then ye could stop this.  But then I would have to hate ye.”
 
I allowed myself a thin smile.  “Well, that would indeed be a terrible and dangerous thing.”  I finished dressing whilst Linaniil still lay in my bed, her face reflective.  “I must go now to check on the latest operations at the farportal.  You are welcome to join me.”
 
She shook her head languidly.  “Nay, I wish to rest more.  And besides, hearing their reports would but make me jealous.  Leave me here awhile – I wilst depart in secret later.”
 
I left my chamber then, dark thoughts now brooding at the back of my mind.  The date was coming closer when our plans would come to fruition and the Great Spellblaze would be unleashed.  A heavy foreboding lay over my heart.  Yet the alternatives seemed grim.  The war with the orcs was going badly, with few races able to secure their borders well and attacks from the brutes ever increasing.  Their numbers seemed inexhaustible.  Though they had little skill in warfare they could bring great harm to unprotected townsteads, and in enough force could bring down cities.  One human kingdom had collapsed under their attacks but a week before.  After that many who had initially rejected our plans came begging for our protection.  The Spellblaze seemed our only hope against imminent disaster.
 
Such thoughts were weighing on my mind as I passed from my chambers in the palace, down to the courtyard by the main gate.  Then from the corner of my eye I saw a swish of long red hair, and spun round thinking Linaniil had followed me.  But the golden robes and bright eyes of Neira revealed otherwise.
 
“Expecting someone else?” she asked with a wide smile, seeing the surprised look on my face.
 
“I was deep in thought,” I explained, bowing slightly to greet her.  “I am just on my way to inspect the farportal operations.  Perhaps you-“
 
“I shall join ye,” she said quickly, not waiting for my invitation.  I nodded my assent and guided her to my carriage.
 
As soon as we took off east the mood changed.  “She wilst only hurt ye,” said Neira suddenly.
 
I cursed quietly, understanding her meaning.  “Are there no secrets to be had in all Eyal?” I muttered.
 
“Not between sisters, and especially not between twins.”  She smiled warmly at me, yet there was no humour in her eyes.  “I mean it though.  I love mine sister, but I know her ways.  She be fickle, and willed to do her own thing when she likes.  Do not be surprised when she bores of ye.  Nor hurt.”
 
“I am quite capable of taking care of myself,” I said in clipped tone.
 
She gazed into my eyes a moment and then turned away to stare out the window.  “Well, I have warned ye...” she replied softly, a touch of sadness in her voice.
 
Was it jealousy perhaps that stirred such an outburst?  And for her sister’s attention or for mine?  I never did discover.  The rest of the trip was spent in sullen silence.  The sun was setting behind our carriage, casting a long shadow on the path ahead, and bathing the land about in crimson light.  It seemed for a moment like we rode into some demon’s plane, pitch black shadows melting into blood-red soil, whilst cold white stars began to spear through the sky above.  I shivered suddenly as the ruins came into view.
 
Few Sher’Tul ruins have been discovered which even come close to matching the grandeur of those which were near Elvala.  Many centuries our people spent excavating them, digging deep into the ground, ever careful not to damage or upset the relics.  The centrepiece was the Crystal Tower.  From the surface all that could be seen of it was a wide, even-sided square, which when cleaned of soil revealed a white stone smoother than marble.  But delving down our archaeologists found it plummeted deep, deep below the ground.  Half a mile it went down, the featureless white stone not bearing a single mark or engraving anywhere on its surface, until it ended suddenly and without foundation.  It was like the whole tower was separate from the earth, some strange thing of the stars that had dropped from the skies and lay sleeping beneath the soil.
 
Some years earlier our people had solved the invisible runes that allowed it to be opened, revealing vast crystal-lined halls and chambers arrayed in geometric patterns of sublime beauty.  Light sparked and shone from every surface, and the walls seemed to hum with energy.  Many shafts and passageways could only be navigated by flight, and at the top was found a grand room large enough to encompass the whole palace of Elvala.  At its centre was the farportal, a raised dais forty feet in diameter and crackling with energy upon which slowly spun a cloud of stars.  It was beautiful and frightening, enchanting and terrifying.  No power of the Shaloren could discern its operation, and though through careful experimentation we were able to manipulate its energies, never could we get a true grasp of the forces that lay beneath.

Neira and I descended to the base of the tower, smothered in the cold shadows of the excavated ruins.  I nodded to the guards as we passed through the square white entrance, and Neira’s eyes instantly enlarged in wonder.  The scintillating rooms were eye-catching to be sure, but they were also desolate and empty.  I tried to imagine what it must have looked like when filled with Sher’Tul.  “How did they all die?” I asked under my breath as we traversed the crystal halls, a question many had asked before.
 
The sorceress picked up on my words and laughed softly.  “It be a mystery, of course!  Mine mother once taught me that they killed themselves in a great civil war, using magics far beyond our imaginings.”
 
“I wonder,” said I.  We had our own records, of course, which we didn’t share with the younger races, but they were not so clear-cut as the many myths that had spread over the ages.
 
We reached the central shaft, and from there levitated up past floors and floors of abandoned chambers, living spaces, workshops, storerooms, and many other areas of purpose undivined by our loremasters.  Finally, after ascending for several minutes, we rose into the grand chamber of the farportal, and Neira gasped to see its size.  Her eyes soon settled on the great Sher’Tul farportal, sparks from it reflecting off the roof hundreds of feet above.  About it were bustling many of our Shaloren mages in silken robes, and Ephinias himself was leading the operations.
 
He broke from his advisers as he saw us arrive, and strode towards us with a confident smile on his face.  Though he wore the grey robes of a research mage he still bore his great golden staff, Luminis, token of his position as king.
 
“Ah, General Aranion!” he said, “You have come at last.  And brought the Kar’Krul girl with you; how splendid.”
 
I gave a small bow.  “Your majesty.  I am here for the update on our operations.”
 
“Yes, yes, of course,” he said with a dismissive hand gesture.  “And doubtless the girl is here to make sure we know what we’re doing?”
 
If Neira was offended she covered it up well.  “It would be mine delight to see evidence of ye skill and power over the ruins, lord Ephinias.”
 
The king smiled and nodded then, and called to some of his aides.  “Prepare the topography demonstration, using the acute fire strand.”  He turned back to us then.  “It is not mere skill and power of course that we can show you, but subtlety and scale too.  Now excuse me a moment whilst I join the others.”
 
He went with two of the senior research mages then to the front of the farportal.  They faced each other and began a low humming in unison, and slowly it seemed that the sparks from the farportal began to flicker redly.  Over the course of a few minutes their hum became a higher pitched chant, but softly sung and still in perfect unison.  As they raised their staffs there appeared above the farportal an image in flames, and looking at it both Neira and I marvelled, for we could see clearly that it was an image of ourselves, looking upwards, as if looking we were staring into a mirror.  Our features and movements were all clearly discernible, down the smallest detail, all carved out of flickering orange fire.
 
Then the chanting rose higher and it seemed the image zoomed out, so that we saw the farportal nearby us and the mages gathered about.  And still the focus soared upwards till we were but specks in a wide hall, until the image was displaced by a white square with carven edges dug into the earth about it, and I knew we were looking at the top of the Crystal Tower from above.  The view widened, and I could see the land rushing away, and the city of Elvala to the west.  The chanting rose higher and now the sea could be seen, and the mountains to the north-west, and all the land about.  And soon the continent was visible, right to the frozen north, and the ocean wrapped all about, and it seemed small white stars were dotted about the landscape.  The singing reached a crescendo and before us hung an image of the whole of Eyal, a globe of fire suspended in mid-air, slowly turning.
 
Then the chanting stopped and the image disappeared, and I could hear beside me Neira suddenly gasp for air, as if she had not dared draw breath through the last few minutes.
 
“You see now?” said Ephinias, grinning with pleasure.  “From the smallest detail to the grandest scale we can manipulate the farportal’s energy.  And did you see those white points marked across the image?  They are the other farportals spread across the world, and this one can connect to them all.  With careful, delicate control we can harmonise the energy of them all and use it to our will.  I’m afraid your sword can be no match to this, Aranion.”
 
I had no words to respond, and only nodded softly, still in awe of what I had seen.  Neira seemed the same, and I could see her now staring at the farportal with the same eager eyes as her sister.  She was converted.
 
Yet my hand strayed across the hilt of Mooncutter, and my heart still murmured with unease.

当前target: #{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第三章：远行传送门#{normal}#

“为什么你不是精灵们的领袖呢？”，莱娜尼尔赤裸着身体横卧在我的床上，单手托头问道。

我的思绪还没有从片刻前的温存中缓过来，对于这个突然的问题感到有些惊异。“为什么我会想要成为他们的领袖呢？”，我反问道。

“当然了，因为你的实力是那么的强啊”，她回答道，“我觉得你是你同族中战斗能力最强的一位，这样强大的力量足以让你成为他们的领袖。”

我微笑道，“光靠武力是无法引领族人的。一个优秀的领袖需要勇于承担责任，审慎做出决定，并具有灵活的政治手腕。我对于这方面的事情可没有什么兴趣，毕竟，伊菲尼亚斯陛下在这方面比我擅长多了。只要给我一把剑，让我能够和部下一起驰骋沙场，我就已经心满意足了，让真正的领袖来思考我和我的战士应该与谁作战吧。”

她沉默半晌，看上去对我的回答并不满意，“呐，不过呢，你看起来对目前的计划并不满意。”

这一令人惊讶的提问让我感到一阵震惊，我不知道她究竟是如何瞬间洞悉了我的内心想法。在此之前，我从来没有在任何人面前表现出过我的担忧，然而她一下子就看穿了我的伪装。她和我五个星期前才刚刚见面，然而任何事情都逃脱不了她敏锐的洞察。

关于魔法大爆炸计划的筹备工作正在有条不紊地进行当中。卡库罗尔首领特塞尔已经返回了他位于北方的城堡，然而他的两个女儿仍然作为大使留在这里，协助我们的计划。这意味着莱娜尼尔和我可以时常相见，然而我们始终保守秘密。我高傲的同族们仍然难以接受精灵与人类的浪漫关系，而我们也无法接受可能迎来的流言蜚语。即使这样，我也难以抵御她的魅力，而她也是一样。

“我是一个战士，”许久的沉思后，我从床上爬起，整理我的长袍，“我喜欢亲自面对敌人，而不是借助某件遗物从远处消灭他们。这样的懦夫行径令真正的战士作呕。”

“然而，开发夏·图尔人遗迹中失落的力量不是那么让人心潮澎湃吗？”她呢喃着，手指轻触下唇，仍慵懒地躺在我的床上，被单紧贴着她赤裸的肌肤。她显然因自己的念头而兴奋不已，“这样强大的能量已经在世间沉眠了那么长时间，直到今天，我们强大的魔法可以让我们亲自驾驭它们，把雷霆万钧的恢弘气势掌握在不及盈寸的掌心之中……唉，若能由我亲自统领这般伟业，该有多好！”

搭上上衣的搭扣，我有些遗憾地摇了摇头。“坦率地说，我并不信任这些遗迹的力量。是的，我们永恒精灵的确有着强大的魔法实力。然而，我们渺小的知识比起那些夏·图尔人实在是相距甚远，以至于我们甚至无法理解他们所遗留下来的物件究竟有什么意义。在这一意义上，我的想法更接近你的孪生姐妹尼耶拉。我们应该用稳健的脚步前行，妥善而审慎地使用那些我们所能掌握的能力，而不是猛然把我们的野心扩展到这种庞大的实验之上。”

莱娜尼尔凝望着我，用调笑一般的语调柔声说道，“如果你是领袖，你就能阻止这一切；但那样的话，我就不得不恨你。”

我露出了浅浅的微笑。“嘛，那还真是一件可怕而又危险的事情。”当我更衣完成时，莱娜尼尔仍然在床上休息，眉间若有所思。“我必须要前去了解远行传送门那边工作的最新进展了。如果你乐意的话，请务必和我一同前去。”

她有些倦怠地摇了摇头。“不，我想要再休息一下。还有，听取他们的报告只会让我嫉妒不已。请让我在这里呆一会儿吧——我稍后就会秘密离开。”

我小心地关上卧房的房门，一股阴霾仍然在脑海之中萦绕。随着时间的推进，魔法大爆炸的庞大计划也一天天被提上日程，一股不详的预感涌上心头。命运总是那么残酷，与计划进行的有条不紊相伴的是兽人战线上的节节败退，只有少数几个种族能够防守他们的边境线，而兽人们的进攻却永不停歇，愈演愈烈。他们的数量似乎无穷无尽，永不枯竭。他们虽然不善战，却能重创毫无防备的村镇；只要兵力足够，甚至能攻陷城市。一周前，刚刚有一个人类王国在他们频繁的攻击下不堪其扰，最终溃败。此后，许多起初拒绝我们计划的人都跑来祈求我们的保护。看起来，对于兽人的侵袭这一迫在眉睫的危险，魔法大爆炸可能会成为我们唯一的希望。

我从卧房顺着宫殿向前，混乱的思绪在我的脑海中盘旋，伴随着我漫步过庭院走向大门。眼前红发女子轻盈的身影让我误以为莱娜尼尔已经跟着我一路走来，然而她金色的长袍和明亮的眼睛让我想起了，那是她的孪生姐妹尼耶拉。

“在想着什么人吗？”，她微笑地望着我，观察着刚刚表情细微的变化。

“抱歉，我刚才正在思考一些问题，”我轻轻弯腰对她示意。“我正准备前去督导和远行传送门有关的工作事宜，如果您——”

“我想和您一同前去。”还没等我说完，她就爽快地回应道。我点了点头，领着她坐上我的马车。

我们刚乘车向东出发，气氛便变了。尼耶拉突然说道：“她这样做只会伤害你。”

我一下子明白了她的意思，感到一阵震惊。“要命，在埃亚尔已经不存在秘密了吗？”我小声说道

“姐妹之间没有什么能隐瞒，尤其我们还是双胞胎。”她温柔地微笑着，然而眼神却没有一丝开玩笑的气息。“我是认真的。我爱我的姐妹，但我了解她的行事风格。她喜怒无常，想怎么做就怎么做。如果她对你感到厌倦，不要惊讶，也不要伤心。”

“我想，我应该有能力整理自己的心情。”我抿嘴说道。

她凝望着我的眼神慢慢移开，遥望着窗外变幻不定的风景。“唉，我想我已经提醒了你…”她柔声回答道，声音中仿佛包含着一阵忧伤。

是嫉妒促使她说出这番话吗？她嫉妒的是姐妹对我的关注，还是我对她姐妹的关注？我始终没有弄清。剩余的旅途中，我和尼耶拉始终保持沉默。夕阳从马车的背后缓缓落下，巨大的阴影投射在向前的小路上，暮色的笼罩将周围的风景染上了一片深红。有一瞬间，我们仿佛在恶魔的位面上漫步，漆黑的阴影慢慢融化在血色的土壤之上，群星惨淡的冷白色光辉似乎瞬间从苍穹直射下来。繁星点点间，遗迹从地平线映入眼帘，让我不禁颤栗。

已发现的夏·图尔遗迹中，鲜有能与埃尔瓦拉附近那一处的宏伟相提并论的。我们的人民花了几个世纪来悉心研究它，调动的工程量庞大无匹深入地下，却又如此小心地不曾损坏和扰乱任何遗迹中的古物。这个遗迹的核心被称为水晶塔。从地面上向下看，我们只能看到巨大的方块，在泥土被清理之后显露出来是比大理石更加光滑的白色石板。继续往下挖掘，白色石板似乎无穷无尽，其表面也没有任何能够给出说明的雕刻和标记，直到半英里后我们找到了它的底部，没有地基那样的设施。这简直就像整座塔都与大地分离，是某种来自群星的奇异之物，从天空坠落后沉睡在泥土之下。

若干年前，我们的魔法师找到了遗迹上不可见的符文，终于叩开了遗迹的大门。遗迹内，壮观的水晶大厅以庄严而又优美的几何图案有规律的排布着，就连墙壁似乎也呼吸着能量。许多甬道和通路都只能通过飞行才能到达，而其顶端是一个足以容纳整个埃尔瓦拉宫殿的巨大房间。在它的中央是远行传送门，一个直径四十英尺的高台，巨大能量如同星云般在周围盘旋，噼啪作响。那是何等美丽而可畏，迷人而恐怖的壮观景象。永恒精灵们根本无法理解它工作的真正原理。即使通过小心的实验我们有办法操纵它所具有的能量，我们也永远无法真正知悉到底是什么力量驱动着它。

我和尼耶拉下到塔底，四周笼罩在已发掘遗迹的冰冷阴影中。穿过白色方形入口时，我向卫兵微微点头，尼耶拉则惊奇地睁大了眼睛。这座闪光的大厅的确足够吸引眼球，但是里面空无一物的情景不禁令人感到孤单。我试着去构想许久之前，当这里仍然被夏·图尔人所充满的情景。“为什么夏·图尔人灭亡了呢？”漫步于水晶大厅，我轻声向尼耶拉问出了那个或许问过许多次的问题。

尼耶拉听言微笑起来。“这当然是个谜啦！不过，我的母亲曾经告诉我，夏·图尔人在一场宏大的内战中走向了灭亡，他们所使用的魔法超乎我们任何人的想象。”

“我也想知道。”我回答道。我们当然有自己的记录，只是不曾与较年轻的种族分享；但这些记录远不像历经岁月流传的诸多神话那样结论分明。

我们到达了中央甬道。我们悬浮而起，缓缓上升，眼前一层层废弃的屋室从上方进入我们的视线，然后缓缓地在视野中消失。卧房、工坊、储藏室、还有很多房间就连我们的博学之人也没法猜测出是用来干什么的。在经过几分钟的上升后，我们到达了远行传送门所在的大厅，尼耶拉不禁因惊讶而倒吸一口冷气。她的眼睛很快看到了夏·图尔的远行传送门，闪耀、映照着几百英尺之上的天花板上的图案。在传送门的周围，一大群身穿高级丝绸长袍的永恒精灵法师正在紧张地工作中，而伊菲尼亚斯陛下正亲自指挥着他们。

当他看到我们的到来时，他先行从一旁围绕的皇家顾问身边脱开身来，怀着自信的笑容向我们走来。尽管他穿着魔法研究院的灰色长袍，他的手中仍然拿着那把金色的法杖，辉光杖，作为他国王身份的证明。

“啊！真高兴见到你，艾伦尼恩将军！”他说道，“你终于来了。这位是卡库罗尔的大小姐吧，真是太好了。”

我微微鞠躬。“陛下。我此来是想了解我们行动的最新进展。”

“啊，啊，当然是的，”他有些鄙夷地挥了挥手。“那么不用说，这位小姐一定是来这里确认我们到底会不会用魔法吧。”

尼耶拉的微笑令人无法判断她到底是否是在生气。“能够亲眼见证你们有关遗迹能量的强大能力和丰富技巧将会是我无上的荣幸，伊菲尼亚斯大人。”

国王微笑着点了点头，回身叫来了他的副官。“准备地形演示，使用锐火束。”他回身向我们说道。“我向你们展示的可不只是技巧和能力，而是从精微到庞大的一切细节。现在请二位稍候片刻，我去与他们会合。”

他与其他两名研究院高阶法师一起走到远行传送门面前，互相遥望，四周传来一阵阵和谐的低吟。随着法术的和声在大厅中飘扬，远行传送门周围的闪烁着星星点点的隐约红色。几分钟后，他们的低吟音调渐渐升高，变成了无比默契的轻声吟唱，然而始终保持在完美的协调之中。紧接着，他们高举手中的法杖，远行传送门上方浮现出一幅由火焰构成的影像。在它的悉心雕刻中，慢慢形成了一幅清晰的画卷，呈现出我和尼耶拉两人的图像。所有的特征都如此明晰，所有的动作都精巧符合，下至最小的细节都清晰可辨，简直如同站在一面巨大而澄澈的明镜之前。

紧接着，随着吟唱的歌声越来越大，影像中的视野也愈发宽广，从中呈现出我们身边的远行传送门和周围围绕着的众多法师。视野飞腾而上，眼前所见的东西越来越小，最终化为宏伟大厅内的一个小点。紧接着，画面被一个白色的方形取代，周围是挖掘直入地底的痕迹，显然我们的视野正处于水晶塔的正上方。随着聚焦范围越来越大，大地奔腾而过，西部埃尔瓦拉市的房屋隐约可见。伴随着吟诵之声，我们看到了奔腾的大海，看到了西北的层峦叠嶂。我们看到了整片大陆的全景，北部寒风笼罩的高原被冰雪所覆盖，包围着的海洋似乎无穷无尽，大陆上闪烁着无数的白色小点，如同繁星一般。咏唱达到了高潮，我们从宇宙俯瞰到了埃亚尔星球的全景，在火焰的缭绕中悬浮于半空之中，慢慢转动。

然后咏唱停止了，先前的图像瞬间消失地无影无踪。我似乎听到尼耶拉因为刚才令人窒息的壮观景象而喘不过气来。

“你现在看到了吗？”伊菲尼亚斯陛下大笑着。“我们可以全方位操纵这个远行传送门的所有能量，无论是最小的细节还是最大的范围，一切尽在掌握之中。还有，你看到地图上所标注的那些白点吗？这是世界上其他的远行传送门，而我们的这个传送门可以与它们中的任何一个链接。经过精心的操纵和悉心的控制，我们可以协调他们全部的能量，并用来实现我们的愿望。我想，你的那把剑可干不了这种事情，艾伦尼恩先生。”

我仍然被我刚才所见到的奇景所震惊，无话可说，只能微微点头。尼耶拉似乎也产生了一样的想法，以和她的孪生姐妹一样的热切眼神望着这座远行传送门。是的，她的想法被改变了。

然而，我的手仍然环绕着斩月剑的剑柄，心头隐隐呢喃着不安之情。

确认修复依据：固定lore/elvala.lua:188明确各个表面闪耀光芒，对应译文只保留墙壁能量，缺少该完整分句；190段闪光大厅描述属于另句，不能代替188分句。新revision全条审核内确认局部遗漏，不追溯改写窗口4限定修复的原结论。
固定lore/elvala.lua:188把缓慢旋转的cloud of stars放在高台之上，译文改成高台周围盘旋的能量，确认空间关系/意象合并失真。该条其他子判断降为advisory：176低声咒骂在译文次句“要命”及“小声说道”中可有语用对应，不能只凭“震惊”断言咒骂完全消失；186从地面所见square译巨大方块有形状表达粗略，但不足以单独断定三维结构错误。只修已确认星云位置，与surface独立确认的188光芒分句遗漏合并；不全面重写回忆录或自动纳入旧164/198/210 pending。

## 6c8f3562302d0a5e1ba9bbc8c6a971067384f1cb608e249486af93d49f57b586

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/zones/orc-breeding-pit/zone.lua
source_tag: _t

source: You arrive in a small underground structure. There are orcs there and as soon as they notice you they scream 'Protect the mothers!'.

当前target: 你来到了一个小型地下建筑内。那里有着许多兽人，当他们注意到你时，他们叫道“保护母亲们！”。

确认修复依据：固定orc-breeding-pit/zone.lua:69–74为叙述中直接引出喊声，译文“叫道…！”后又加句号形成重复句末终止标点；确认局部中文标点问题，不改变刚修复的建筑内空间关系。

## e564485d2aa300744c287c80e47a5c602d5669aba25c8114826b6a5bb2cc94b2

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/general/npcs/wight.lua
source_tag: _t

source: It is a ghostly apparition with a humanoid form.

当前target: 它有着人类的脸孔，幽灵般的影子。

确认修复依据：固定general/npcs/wight.lua:65–69描述forest wight整体humanoid form；译文把人形改成人类脸孔，确认形态对象偏移。

## e5666d20d3c3d8abd1d9a79f05c34e328e546c52648ceb73f41abcc1d9a4b800

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/talents/undeads/ghoul.lua
source_tag: tformat

source: Gnaw your target for %d%% damage.  If your attack hits, the target may be infected with Ghoul Rot for %d turns.
		Each turn, Ghoul Rot inflicts %0.2f blight damage.
		Targets suffering from Ghoul Rot rise as friendly ghouls when slain.
		Ghouls last for %d turns and can use Gnaw, Ghoulish Leap, Stun, and Rotting Disease.
		The blight damage scales with your Constitution.

当前target: 啃噬目标，造成 %d%% 伤害。如果你的攻击命中，目标可能感染食尸鬼腐烂疫病，持续 %d 回合。
		食尸鬼腐烂疫病每回合造成 %0.2f 枯萎伤害。
		目标被杀死时会变成为你作战的友方食尸鬼。
		食尸鬼傀儡持续 %d 回合，可以使用啃噬、食尸鬼跳跃、震慑和腐烂疫病。
		受体质影响，枯萎伤害按比例加成。

确认修复依据：固定undeads/ghoul.lua:226–256及timed_effects/magical.lua:2429–2454、Actor.lua:3399–3405：非致死命中须成功感染GHOUL_ROT且make_ghoul有效，之后死亡才生成友方食尸鬼，译文第三句省略此限定。但surface称感染为全部复活的必要条件过强：Gnaw直接击杀且可染病时会直接spawn_ghoul。只确认后续死亡分支说明遗漏，修复不得断言未感染时任何分支均不能复活。

## e56b636891bf60ce57bbc04833cdc971eb4223a6f9b4ed3404f271b3b83f8ea4

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/talents/cursed/darkness.lua
source_tag: tformat

source: Spawn tendrils of darkness to pursue a single target for up to 12 turns, leaving behind a trail of creeping darkness as they move. Targets seized by the tendrils are pinned for %d turns and shrouded in darkness. The darkness deals %0.2f damage per turn to those within.
		The damage will increase with your Mindpower. You do +%d%% damage to anything that has entered your creeping dark.

当前target: 召唤黑暗触手攻击某个敌人，持续12回合。当黑暗触手移动时，黑暗之雾会跟随蔓延。
			被触手抓住的敌人会被定身 %d 回合并被黑暗笼罩，每回合黑暗会造成 %0.2f 点伤害。
			伤害受精神强度加成。你对任何进入黑暗之雾的人造成 +%d%% 伤害。

确认修复依据：固定cursed/darkness.lua:23–134、430–480以duration=12创建追踪实体，目标死亡、距离无法追上、无路可行会提前消散，命中后改为pinDuration倒计时；原文up to 12 turns遗漏最多。原文1LF、译文2LF，另有缩进TAB差异；LF是独立明确布局缺陷，TAB不与LF混称。保留伤害与定身参数顺序。

## e571821f554e422e76e7d61ff2e0b59c881c060dee564ca73d1931a370aaf36e

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/timed_effects/floor.lua
source_tag: tformat

source: The target is near a font of life, granting %+0.2f life regeneration, %+0.2f equilibrium regeneration, %+0.2f stamina regeneration and %+0.2f psi regeneration.  (Only living creatures benefit.)

当前target: 目标靠近生命之泉，增加 %+0.2f 生命回复，%+0.2f 失衡值回复，%+0.2f 体力回复和 %+0.2f 灵能回复。不死族无法获得此效果。

确认修复依据：固定timed_effects/floor.lua:53–68只允许checkClassification(living)受益；Actor.lua:7047–7076的unliving还含construct、crystal，living为其反集。译文只说不死族无法获益不能覆盖构装体与水晶，确认适用对象限定遗漏。

## e58ba9366dc38017fba82ac5414a31156f391810dbf1c3772493a73f0b502f6b

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/birth/classes/mage.lua
source_tag: _t

source: Archmagi start with knowledge of many schools of magic. However, they usually refuse to have anything to do with Necromancy.

当前target: 元素法师学习各种学科的魔法知识。然而，他们通常拒绝任何死灵法术。

确认修复依据：固定birth/classes/mage.lua:139–151明确start with knowledge，187–214列出出生已掌握多个法术系及四个初始技能。现译学习各种学科遗漏初始就掌握的状态；只修此说明限定，不涉及Archmage类名政策。

## e5a468946bbe8421dc673a8358f1e8b04e53ed7ebcf19fe37a117d637e147798

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/chats/alchemist-last-hope.lua
source_tag: _t

source: #LIGHT_GREEN#*A dwarf in stained, battered mail armor opens the door.*#WHITE#
Say, you interested in dismembering stuff and getting paid?

当前target: #LIGHT_GREEN#*一位穿着肮脏破旧锁甲的矮人开了门。*#WHITE#
说！你是不是对收钱帮人搜集材料感兴趣？

确认修复依据：固定chats/alchemist-last-hope.lua:121–142是初遇炼金术士对白，dismembering明确肢解，后续proposal索取monster parts；泛化为搜集材料遗漏该动作。Say是搭话语而非要求对方说话的命令，现译“说！”也使语气不自然。确认局部对白语义，不扩大任务情节。

## e5bca739cc706c2620c6d1500b1bce2fd364d5d3c988d56409e2135e3e3c08bc

来源batch: batch-990137011625a41fa36b
section: mod-tome/init.lua
source_tag: init.lua load_tips

source: The Thaloren and Shaloren elves have never had good relations, and have been outright hostile since the Spellblaze devastated many Thaloren lands.

当前target: 自然精灵与永恒精灵之间关系一直不佳，自从魔法大爆炸摧毁了很多自然精灵大陆之后，他们之间更是相互敌视。

确认修复依据：固定init.lua:115的many Thaloren lands指多处自然精灵领地；many不是许多大陆，后一句另谈Maj’Eyal东部。确认大陆误译，沿用现有自然精灵名称。

## e5dc6a60be28b479ec1dd1180035c4d256f55eefea348f4d9323f856574ec50e

来源batch: batch-990137011625a41fa36b
section: mod-tome/data/lore/elvala.lua
source_tag: _t

source: #{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Six: A Changed Eyal#{normal}#

Perhaps what happened will never be truly understood.  What Sher’Tul ruins survived the Spellblaze have been little touched since - the burned hand learns its lesson.  But we know that Ephinias and his mages lost control somehow, whatever delicacy and balance they wrought with coming untangled.  At the moment they tried to connect to the other farportals the imbalance was reverberated, resonated, magnified beyond control.  The farportal in the Crystal Tower imploded in a fraction of a second, killing all within and crushing the land about.  The energies in the Sher’Tul relics then erupted in a blaze of white light, turning the air to fire and the ground to ruin.  The blaze swept eastwards, rolling over our battle with an unstoppable destructive force, and then carrying on towards the Thaloren lands.  Most of the ancient forests of Shatur were ripped from their roots, and the lands lain cursed ever since.

Meanwhile the other farportals all over Maj’Eyal erupted, white stone cracking and vast swathes of energy spilling forth.  All of the Cornac lands to the west were turned to desert, the dwarven halls of Korhek crumpled, the midvale plains were risen up as mountains and Lake Nur formed in their wake.  In the south the ancient tower of Darafel was collapsed, and the forests beside it morphed into an ever-broiling scar of lava and blackened earth.  Far in the east the Naloren farportal, the largest of all in Maj’Eyal, disappeared in a vast earthquake that swallowed everything for miles around, and boiling water spewed up to fill its cavernous depths.

And whilst this destruction was wrought the incredible energies disrupted all of the mana flow around Eyal.  Streams of energy that followed set, slowly changing courses, now were flooded and droughted, warped and split.  The threads of the elements were in vast disarray, and any attuned to magic suddenly found themselves far away from their accustomed power sources.

Even the Heavens were changed.  The wandering star of Vor disappeared, the constellations were tilted off their normal course, and the seasons rent harsher since.  Some say the moons dimmed and the sun went whiter after that day.  I do not know.  The whole world has seemed darker to me.

The numbers killed are beyond count.  The initial destruction took at least five million lives, and the terror that followed claimed far more.  For though it had been a day of tragedy and immeasurable woe, it was to be followed by a bloody age of darkness and torment.

But none of this I knew as I lay weeping in the aftermath, cradling in my lap the one life I cared about.  In abject misery I called on all the healing powers I could to bring her back to me for but one moment.  Her heart beat softly, and her eyes opened, but seemed glassy and far away.

“Linaniil,” I whispered, and her dark eyes turned towards my face.  I tried to mumble an apology, to say I was sorry and was unable to help her, but emotions overcame my voice.  Her gaze at me was empty, as if she looked right through me, before she turned her eyes away.  Slowly she raised a hand to an amulet about her neck, and with a light touch it glowed and then cracked.  Her eyes closed again but I could feel the power from the artifact pumping into her, strengthening her heart-beat and mending her flesh.  She was unconscious and still badly wounded, but for now the mortal threat was gone.

My thoughts were mixed - glad she was no longer at death’s door, but worried she might relapse, and at the back of my mind scared of that empty look she had given me.  Could she possibly forgive my part in this?

Carefully I picked up her frail body, and began the journey back to Elvala.  Two days it took on foot, through blasted and ruined ground.  On the passage I came across other survivors, refugees now leaving their destroyed homes, heading to the city to seek shelter.  I tried to nurse Linaniil as best I could, giving her water during brief periods of waking and dressing her wounds, but true healing could not happen till I reached the city.

Elvala was a quiet chaos, oppressed by fear and uncertainty, an air of dread filling all the streets.  The news had broken that our army had been entirely wiped out - there would be no loved ones returning to their families, and the sound of stifled mourning was to be heard in all corners of the city.

I took Linaniil straight to the healing grounds in the palace and gave her to the doctors with the strictest instructions.  They were swamped by casualties, but followed my orders without question, tending immediately to her wounds and applying tinctures and regenerative spells.

It was as I watched over her quietly that a party bustled loudly into the grounds.  I recognised at their head was Perissa, a senior court official.  At her side was an elderly human who immediately went to where Linaniil lay.

“General Aranion!” announced Perissa loudly, “I heard you were here, but I could scarce believe it.  Thank the threads you have returned to us!  This is a grave time; we must talk at once.”

But I ignored her as I saw the human touch Linaniil’s hand, and her eyes gently open.  “Cuilan?” she murmured softly.

“Aye, it is me, my lady,” he said quietly.  “I have been sent here by your father.  He has ordered me to pass you this.”  And with that he brought forth a golden ring set with a fiery ruby.  I recognised it immediately as the Ring of Kar’Krul, worn by the mighty Turthel.  Linaniil sat up quickly, wincing from the pain, but with her eyes locked on the ring as it was placed in her hand.

“But mine father...”

“I’m sorry, my lady.  It brings me great sorrow to bear you this news.  Your father and his court are dead.  His last act was to instruct me to bring this ring to you and your sister.  Neira...” he said glancing about.  “Is she...?”  He saw the look in Linaniil’s eyes and dipped his head despondently.  “I see.  I am terribly sorry.  It becomes my duty then, my lady, to declare you the new leader of the Kar’Krul.”

“General Aranion,” interjected Perissa.  “I really must speak with you now!”

“Wait!” I barked, and turned to the human Cuilan.  “What is happening here?  How could one such as Turthel be killed?”

The man looked at me then with a wan sadness in his eyes, before turning to address Linaniil.  “Yesterday, the day after the terrible Spellblaze, as we began some attempt at reconstruction, still struggling to realign our mana paths, a murmur began amongst the people.  It spoke thus: The Kar’Krul circle of mages had betrayed the ordinary people.  They accused us of siding with the elves to destroy non-mages, of toying with terrible powers beyond our control, of deliberately massacring them out of evil and malice.  We could not logic with them, they would listen to no reason, and they rose up in violent anger.  They attacked many of us, with farming instruments and whatever weapons they could find.  Our defences were weak, and striking back just made the crowd fiercer.  We retreated to your father’s home, begging for help, but he shook his head and said he could not fight back.  They came for us then, storming his palace, and Turthel ordered all to put up no resistance.  He handed me his ring, saying to seek you out in Elvala, and then stepped outside to face the crowds.  He didn’t resist!  The people... they... they...”  He lapsed into sullen silence, shaking his head in sorrow.  He looked like he wanted to cry, but had no tears left to shed.  Linaniil’s face was graven and she stared hard at the ring.

Perissa grabbed me then and turned me to her attention.  “This is what I need to speak with you about, General Aranion.  If this human’s tale is to be believed then we are in very grave danger!  Scout reports suggest there is a body of humans coming here from the north as we speak.  From what this human says they seek retribution - they wish to slaughter us all.  A storm of wrath lies on our borders and we are defenseless!  We need you desperately to organise our defence, to protect our city and our people.”

I felt numb, the events overwhelming me.  “But who leads us?” I said.

“There is no one.  What royals are known to be alive are not suited.  We are entering a time of war, a terrible time like no other we have ever faced.  We need military leadership.  You, General Aranion, you must be our leader.”

I held Perissa’s gaze then and saw the wisdom in her words.  My duty as a Shaloren was clear.  But my heart tremored as I turned to look at Linaniil.

“This be our path then, Aranion,” she said quietly, raising herself from the bed and carefully placing the ring on the middle finger of her right hand.  “I must tend to mine people, and ye to yours.  We will not meet again.”

“But your wounds-” I tried to object.

“Will never heal!” she cried, hate dripping from her voice.  Her eyes were like cold and impenetrable ice, a smouldering anger deep within.  “Come, Cuilan, we must leave this place.”  And with that they departed, Linaniil walking tall and proud in spite of her injuries.

I closed off my heart and my emotions then, lest they overwhelm me.  My duty was before me, and the events of the past had to be locked away from memory.

The ceremony was organised in under an hour, and I was anointed leader of the Grand Council of Elvala, head of the Shaloren people.  On my order rangers began transporting in survivors from outpost settlements, whilst I commanded our remaining mages to begin a new endeavour around our city walls.

The first waves of the storm of hate came the next day.  Human peasants and farmers, ordinary workers armed poorly, their looted swords and spears badly wielded.  I stood alone at our gates as they approached, Mooncutter in my hand.  When the first few charged at me I thrust the blade into the soil and tore a great chasm in the earth, and our mages summoned forth mists and smoke that rose from the ground and began to surround our whole city.  As the peasants stumbled in confusion archers started firing from our walls.  What few made it through the smoke and arrows I took on, tearing Mooncutter through their flesh with little resistance.  Their blood gushed out in the gallons, drenching our ground, staining my skin.  It was like a warm shower over my boiling emotions, a bath of blood to wash over my sins.

The Shroud of Elvala was begun, as our whole city was wreathed in cloud and smoke.  Our shield, our mask, our hiding.  It would last for centuries, the only dealings with the outside world being in furtive secrecy.


当前target: #{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第六章：被改变的埃亚尔#{normal}#

或许，我们永远不会知道当天到底发生了什么。魔法大爆炸后幸存下来的夏·图尔遗迹，自此几乎无人敢碰——这一教训对人们来说已经足够深刻了。我们唯一知道的是，不管伊菲尼亚斯曾经拥有多么精妙和平衡的控制，在那一刻，他们失控了。在他们连接到其他传送门的一瞬间，微小的不平衡迅速被回响，共振，放大，瞬间失去了控制。在不到一秒钟的时间里，水晶塔中的远行传送门向内坍缩，杀死了其中所有人，并压垮四周的大地。随后，夏·图尔遗迹中的能量化作耀眼白光爆发，将空气化为火焰，将大地化为废墟。大火迅速向东袭来，用它势不可挡的毁灭力量将我们战场上的一切全部摧毁，然后直接席卷向自然精灵的领地。夏特尔的远古森林纷纷被连根拔起，从此，那片大地被永远诅咒。

同时，在马基·埃亚尔的其他远行传送门都纷纷爆发，磐石也被其撕裂，大量的能量向外涌出。西部科纳克人王国的土地迅速化为了沙漠，矮人大厅科尔赫克倒塌了，中部的平原隆起成为山脉，中间形成了纳尔湖。在南部，远古高塔德拉斐尔倒塌了，周围的森林化为被永远灼热的岩浆和黑石覆盖的焦土。在遥远的东方，纳鲁精灵所拥有的，整个马基·埃亚尔最大的传送门，被一场剧烈的地震所吞噬。剧烈的地震吞噬了周围数英里内的一切，沸水喷涌而出，填满了地震留下的巨大空腔。

当这场毁灭发生时，惊人的能量扰乱了环绕埃亚尔的所有法力流动。能量的流动曾经遵循相对固定、缓慢变化的路线，如今却忽而洪泛，忽而枯竭，被扭曲、被分裂。元素脉络陷入极度混乱，任何与魔法调谐的人都突然发现，自己已远离惯用的力量之源。

就连苍穹也发生了变化。在星间漫游的沃尔之星消失了，星座也偏离了他们正常的轨道，季节变化变得远比以前更为极端。有人说，从那以后，月亮变得更暗，而太阳也变得更白。我不知道这些。在我眼里，整个世界从那一刻起都变得黯淡了。

这一切的受难者数不胜数。最初的破坏至少夺走了五百万人的生命，而随后的恐怖事件则造成了更大的毁灭。因为，这不仅是悲剧和无尽灾厄的一天，而且还带来了一个充满黑暗和折磨的血腥时代。

然而，在我在灾难之中抱着我生命中最重视的人的身体，放声痛哭的一刻，我还不知道之后所发生的那些无尽的困难。在无尽的痛苦中，我试图使用我所有的治疗力量，试图能够挽回她的生命，哪怕只是延长她一秒钟的时间。她的心跳微弱，睁开的双眸如玻璃一样，离我的距离仿佛在两个世界一样那么遥远。

“莱娜尼尔，”我轻声低语，她黑色的眼睛转向我的脸庞。我试图呢喃着说出我的道歉，试图说出我无法拯救她的痛苦，但我实在是没有办法说出口。她望向我的目光空灵无物，仿佛穿透了我的身体，然后慢慢转向了另一个地方。她的手中慢慢拿起了她脖子上的一串吊坠，在那一瞬间，吊坠发出了一束光芒，然后碎裂了。她的眼睛再一次闭上，但我能感受到，她刚刚拿着的神器的力量已经灌注进了她的身体里，修复着她的肉体，她的心跳也不再那么微弱。她仍然处在无意识中，仍然身受重伤。然而现在，致命的威胁已经消失了。

我的心中百感交集——我为她逃离死神的拥抱感到欣喜，但又对她的虚弱状态感到担忧。而且，她刚才看向我时空洞的眼神让我心如刀割。她会原谅我在这场灾难中扮演的角色吗？

我小心地抱起她脆弱的身躯，慢慢走向返回埃尔瓦拉的路。在灼烧的废土之上，我走了两天的时间。在路上，我能看到其他的幸存者，他们是逃离自己被摧毁的家园的灾民，正在试图在城市里找到避难所。我试图尽我所能护理莱娜尼尔，不断给她水，处理着她的伤口，但只有我到达城市的时候才能找到真正的治疗师。

埃尔瓦拉处在一片寂静的混乱之中，人们被不确定性和恐怖所压倒，每一条街道都弥漫着恐惧的气息。有关我们的军队全军覆灭的消息已经传了开来——他们的家人再也没法看到自己的亲人回到家园，城市的每一个角落里都充满了令人窒息的痛苦哀悼。

我把莱娜尼尔带到了王宫的医院，让最好的治疗师给她治疗。医院里现在已经满是受伤的灾民，他们对我的指令没有半点疑虑，立刻使用药剂和治疗性的法术处理了她的伤口。

正当我静静地看着她时，一群人吵吵嚷嚷地冲了进来。我认出他们的头领是佩里萨，王廷中的高级官员。在她身边的是一位年长的人类，他立即走向莱娜尼尔躺在的地方。

“艾伦尼恩将军！”佩里萨大喊道，“我听说你在这里，真是难以置信。感谢命运之线！现在是严峻的时刻，我们必须马上谈谈。”

但我没有理她，我看到那个人类轻碰了莱娜尼尔的手，她的眼睛缓缓张开。“崔岚？”她低声呢喃道。

“嗯，是我，小姐”，他轻声说道。“我是奉你父亲之命来到这里的。他命我把这个交给你。”他的手中拿出了一枚纯金的戒指，上面镶嵌着火焰般的红宝石。我一下子认了出来，正是强大的特塞尔所佩戴的卡库罗尔之戒。莱娜尼尔一下子坐了起来，似乎仍然在痛苦中挣扎，但她的眼睛紧盯着她手中的那枚戒指。

“但是，我父亲…”

“我很抱歉，小姐。向您传达这个消息实在是让人无比悲痛。你的父亲和他王廷里所有的人都已经去世了。他给我最后的指令就是让我把这枚戒指带给你和你的孪生姐妹。尼耶拉……”，他向周围看去。“她…？”他看到了莱娜尼尔的目光，失落的慢慢低下头。“我明白了。我真的十分抱歉。那么，我有责任宣布这件事。小姐，我要宣布，你现在就是卡库罗尔的新领袖。”

“艾伦尼恩将军！”佩里萨打断了他的发言，“我真的必须马上和你谈谈！”

“等等！”，我怒吼起来，转向崔岚。“到底发生了什么？特塞尔这么强大的人怎么可能被杀？”

那个男人看向我，眼中充满了无尽的悲伤，然后又重新看向莱娜尼尔。“昨天，也就是可怕的魔法大爆炸之后的一天。我们本来准备开始重建工作，大部分人还在调整自己的法力通道的。然而，在人群中出现了一种谣言。他们说：卡库罗尔的法师们背叛了普通人。他们指责我们和永恒精灵合谋，想要操纵超越想象的可怕力量，故意展开这种邪恶恐怖的屠杀，试图清除所有不是法师的人。我们无法说服他们，他们什么也不肯相信，愤怒地开始了暴动。他们使用农具或者他们能够找到的任何东西攻击我们。我们根本没有能力保护自己，试图反击只是让人群变得更加愤怒。我们撤退到你父亲的宫廷，请求他帮助我们，但是他摇了摇头，说他绝不会伤害自己的人民。那些人跟随我们，冲进了特塞尔的宫殿，但是特塞尔命令我们放弃抵抗。他把他的戒指交给了我，然后一个人走了出去，直面了外面的人群。他根本没有抵抗！那些人……他们……他们……”，他悲伤地陷入沉默，痛苦地摇着头。他仿佛看上去想要痛哭失声，但是已经失去了眼泪。莱娜尼尔面如死灰，用凝重的眼神注视着那枚戒指。

佩里萨抓住我，强制把我的脸转向她的方向。“这就是我要跟你说的事情，艾伦尼恩将军。如果有关人类的事情是真的话，那么我们现在已经处在非常危险的境地了！在我们说话的时候，就有哨兵向我们报告，一群人类正在从北方向我们这边过来。那些人类说他们要寻求复仇——他们要杀光我们！现在，我们的国境已经被愤怒的浪潮所包围，而我们已经毫无防备，孤立无援！我们需要你组织我们的防御，我们要保护我们的城市和我们的人民。”

我仍然处于麻木的状态，这一连串的事件把我吓倒了。“但是谁来领导我们？”我问道。

“没有人。即使还有王族还活着，他们也不适合现在的状况。我们现在已经进入了战争的时代，这是我们中间的任何人都没有经历过的可怕的时代。我们需要军人来领导这一切。你，艾伦尼恩将军，你必须成为我们的领袖。”

我迎上佩里萨的目光，领会到了她话语中的智慧。我作为一个永恒精灵的责任已经很清楚了。但当我看向莱娜尼尔的时候，我的心还是忍不住颤抖。

“这就是我们的道路，艾伦尼恩”，她静静地说着，从床上爬了起来，小心翼翼在右手中指上戴上了那枚戒指。“我必须领导我的人民，而你需要领导你的人民。我们永远不会再相见了。”

“但是你的伤口——”我试图反对

“那份伤痛永远不会痊愈！”她怒吼着，话语中透露着恨意。她的眼神像一块冰，无法穿透的冰，那是一份内心深处深藏的愤怒。“来吧，崔岚，我们必须离开这个地方。”。然后，他们离开了。莱娜尼尔尽管还受着伤，仍然高傲地走着。

我封闭了我的心房，压制了我的感情。我不能让这些感情压倒我的责任。我还有我必须要做的事情，过去发生的一切都将永远在记忆中被封存。

继位仪式在一小时以内就开始了。我受膏成为埃尔瓦拉最高议会的领导，永恒精灵人民的领袖。在我的指挥下，我们的游侠开始从周围的哨站和定居点撤离幸存者，而我命令剩下的法师围绕我们的城墙开始新的努力。

第一波仇恨的浪潮在第二天就席卷而来。人类的农民和工人组成了这群人，装备简陋，笨拙地挥舞着掠来的刀剑和长矛。我独自一人站在城门外，手持斩月剑，迎向他们。当他们冲向我的时候，我将长剑插入大地，在大地上撕开一道裂痕。我们的法师迅速让一层层重叠浓厚的迷雾从地面上升起，环绕了我们的整个城市。当那些农民陷入混乱的时候。弓箭手们开始从城墙上向下射击。只有几个人能够躲过烟雾和箭雨的夹击，我的斩月剑可以十分轻松地穿透那些仅存的人的血肉。他们的鲜血从身体中喷出，渗透了周围的大地，沾染了我的身体。我心头沸腾的感情沐浴在鲜血之中，那是我所犯下的罪恶的血雨。

埃尔瓦拉的帷幕升起了，整座城市被迷雾所覆盖。这是我们的盾牌，我们的面纱，我们的藏身之所。这持续了几个世纪，在此期间和外界的一切交易都被严格守秘。


确认修复依据：固定lore/elvala.lua:368–396的完整直接引语与叙述，现译“等等！”，和“离开这个地方。”。形成多余句末标点；可按中文直接引语修正。一般“……”后逗号的位置须按所引内容是否独立完整判断，不把一切引号外逗号自动判错。其他保真疑点另按具体源码裁决，不由标点观察自动扩展。
固定lore/elvala.lua:350明确死亡者无法计数，随后恐怖夺去更多生命；现译受难者及更大毁灭弱化死亡人数语义。352的none of this回指前述世界灾变和伤亡，现译不知道之后无尽困难改变指代及时间。362的strictest instructions修饰对医生的严令，现译最好的治疗师新增人员质量且漏严令。确认这三项局部叙事保真，与surface已确认标点合并，不扩大为全章重写。

## e643063dc0d8687f0db0be01762c55b0d0d2003bcb203da2a3533bfb864fbf1f

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/class/Object.lua
source_tag: _t

source: Equilibrium when firing a critical mind attack: 

当前target: 精神暴击时回复失衡值：

确认修复依据：Object.lua1817显示带符号equilibrium_on_crit属性，Combat.lua2082直接incEquilibrium该值；字段并非固定回复，译文不应预设回复方向。
Object.lua1817显示带符号equilibrium_on_crit属性，Combat.lua2082直接incEquilibrium该值；字段并非固定回复，译文不应预设回复方向。 对contextual观察只确认方向预设错误；incEquilibrium按带符号数值变化，不能把模型“该值增加失衡值”泛化为所有属性值均为正数。

## e66d53860d323fe59145c87fbfd046cd371500e0dac3d2d80f6a9457769102f7

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/data/talents/misc/npcs.lua
source_tag: tformat

source: Whilst wearing leather or lighter armour, you gain %d%% Defense and %d%% Armour hardiness.

当前target: 当你身着轻甲和布甲时，你会增加 %d%% 近身闪避和 %d%% 护甲强度。

确认修复依据：Combat.lua1266—1273的MOBILE_DEFENCE改变combatDefenseBase；1276—1293近战及远程防御均取该值，Archery.lua315消费combatDefenseRanged；近身限定错误。

## e67a8fe84f90497d0b1820eae7f50ee3d7ec863639fe06515b0b99e1d0c53f04

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: This voratun shield, coated with thick vines, was imbued with nature's power long ago by the Halfling General Almadar Riul, who used it to stave off the magic and diseases of orcish corruptors during the peak of the Pyre Wars.

当前target: 这块沃瑞钽盾牌表面被厚实的藤蔓所缠绕，其中注入了许多年前的半身人将军阿尔曼达·鲁伊尔的自然力量，他在烈火战争中用这个盾牌驱散了兽人堕落者的魔法与疾病。

确认修复依据：world-artifacts.lua2316明确stave off抵挡而非驱散，during peak of Pyre Wars缺少时期限定；long ago修饰注入自然力量时间。
world-artifacts.lua2316明确stave off抵挡而非驱散，during peak of Pyre Wars缺少时期限定；long ago修饰注入自然力量时间。 contextual附带Almadar译名音节建议无冻结术语及统一命名依据，仅记advisory，不修专名。

## e68cd1e92d8d4ed30000ea6f99cf98644f5bbccf68cc81a9817a93fd369ba8b9

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/data/talents/cursed/force-of-will.lua
source_tag: logCombat

source: #Source# was blasted %d spaces into #Target#!

当前target: #Source# 被推送%d格进入#Target#！

确认修复依据：源码第71–76行表明被击退者移动若干格后与 nextTarget 发生碰撞；“被推送%d格进入#Target#”把碰撞关系表述成进入目标体内，关系语义失真。 固定源码独立核验确认；纳入窗口5补充修复候选。

## e6976768f97b261a317d34b20fbdd66a6f42788687a1c448ec78f729eb5b8bd7

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/class/interface/Combat.lua
source_tag: logSeen

source: #{bold}#%s's mind surges with critical power!#{normal}#

当前target: #{bold}#%s的精神攻击造成了致命一击！#{normal}#

确认修复依据：该日志由 mindCrit 的暴击分支触发，而固定源码 call.lua 第134–137行将 mindCrit 用于 target:heal；因此它也可描述治疗暴击，“精神攻击造成了致命一击”错误限定为攻击并误述效果。 固定源码独立核验确认；纳入窗口5补充修复候选。

## e6a5f4780937d2b884c85e9711316fe7e45d277b6fef5bfa73f1b62aa3904f24

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/data/timed_effects/other.lua
source_tag: _t

source: The target's unnatural body has responded to damage taken.

当前target: 目标的诅咒之体对其所承受的苦难做出了回应。

确认修复依据：other.lua1791是damage taken的效果描述，后续增伤/属性改变取决于受伤反馈；苦难泛化具体受伤条件，应恢复所受伤害，诅咒之体名称本身有curse语境支持。

## e6e55301b89dee55821a8b311c6125f3607fc4de27096984e2ba712db523e8c5

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/class/Game.lua
source_tag: log

source: Showing big healthbars and tactical borders.

当前target: 显示大血条+边框。

确认修复依据：Game.lua2017—2026设置viewer faction并区分仅血条模式；tactical是战术/阵营边框用途限定，译文只剩边框丢失该限定。

## e70622f7b5f74ce35bd24cd6de77e1cc75ee3d7e008c7265c4e84c4c77a76ec9

来源batch: batch-c8180aa79c1822c18e7c
section: mod-tome/data/quests/lumberjack-cursed.lua
source_tag: _t

source: You met a half-mad lumberjack fleeing a small village, rambling about an untold horror lurking there, slaughtering people.

当前target: 你遇到了一个从小村庄里逃出来的半疯癫的伐木工人，大声喊着有个没见过的吓人的东西在里面杀人。

确认修复依据：固定quests/lumberjack-cursed.lua23描写rambling语无伦次絮叨，非大声喊叫；untold horror在此是难以言说的恐怖，非没见过的东西。确认说话状态及恐怖描述的局部偏移。
固定quests/lumberjack-cursed.lua23描写rambling语无伦次絮叨，非大声喊叫；untold horror在此是难以言说的恐怖，非没见过的东西。确认说话状态及恐怖描述的局部偏移。 潜伏也未明确表达，可在本句修复时恢复；不接受由此扩展为整类任务日志文风重写。

## 首轮后局部范围校准

ADJUDICATION-R0.json / FIX-1-REPLACEMENTS.json 显式纳入五处精确替换，限三个现有revision。回忆录额外允许188首句的破解符文关系，以及380失控力量、382复仇消息归属；不是全文重写。其他观察裁决不构成新授权。

## 第二次局部范围校准

ADJUDICATION-R1.json / FIX-2-REPLACEMENTS.json 仅增加回忆录380与382行的两处精确子句修复，保持原18条边界。reviewer泛化出的动机、全局术语或人物改名不纳入。

## 第二轮独立范围校准后的第三轮局部修复

仅纳入ADJUDICATION-R2 / FIX-3-REPLACEMENTS中的装备条件短语与392叙述句末句号；scope-audit-r2-01已完成并归档。不得因此改写同段其他子句、食尸鬼称谓或跨类职业译名。

## 用户授权的第四轮有界修复

用户在三轮上限暂停后明确回复“同意”，授权增加一轮（max_cycles=4），仅将188行对应段落中的“就连墙壁似乎也呼吸着能量”改为“就连墙壁似乎也随着能量嗡嗡作响”，其余范围和门禁不变。先完成范围校准；具体执行仍由唯一EXECUTOR完成。
