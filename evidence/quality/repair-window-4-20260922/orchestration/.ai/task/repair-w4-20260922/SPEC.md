# 修复窗口4：247—249的17条已确认译文

模式implement，Paseo MCP，schema5 translation_contextual_v2。用户持续授权审核和逐批推送；三批已finalize并推送，基线f9a2b3c76e2a34b2507bd4689adc74b11a6e414f。

唯一EXECUTOR只可修改mod-tome.lua中下列17个source/section/source_tag的target，以及evidence/quality/repair-window-4-20260922/的本窗口证据。后续宿主提供确定事实后另加出版范围；初次实施禁止handoff/catalog/migration操作。不得修改其他译文、术语、规则、工具或旧证据；不得stage/commit、写.ai或创建agent。保留baseline全部无关文件。

三个来源批次各自真实repair preflight已通过，共16条正式候选；另1条248回忆录来自独立宿主补充。WORKSET是17条有界宿主组合清单，不是伪造单一生产批次。SOURCE-CLAIMS是宿主裁决，不可提供给独立reviewer；SOURCE-ANCHORS只含固定公开源码，术语按冻结精确行及其语境使用。

固定源码624a67329fe2ad440c5b344785a9c73fcf22ae63；全部tome。保持source/source_tag/args_order/special、printf/markup不变。换行的唯一授权变化：e22d6fff0c和e454e243b1各由当前5个LF恢复原文7个LF及对应段落布局；其余target的LF及全部target的TAB序列保持baseline。不得依据旧英文恢复与源码冲突的机制。无术语库/全局单位策略改动。Archmage、RW1-SIB-01/02和旧source-key blocked均排除。

验收：LuaJIT加载只变这17个target、其余记录完全一致；严格lint、已有claims strict registry、空白及不变量检查；若产生proposal须proposal --strict。每个数值占位符列index/quantity_kind/producer/consumer，涉及治疗/伤害/时长/敌我限制需方向值流证据。四成员独立v2 REVIEW及最新whole-workset FINAL_REVIEW，完整17门禁/严格addon构建和DONE_VERIFIED；译文commit→queue rebuild→单次catalog/migration-chain→证据commit→queue rebuild→push，successor仍需重新审核。主代理负责完整门禁。

长篇回忆录e433115e63只修L1裸体/自身念头激起欲望、L3来自群星并坠落的水晶塔比喻、L5条件性不得不恨、L7向东出发及气氛随即变化四处；其他advisory和大小姐称谓不借机全面改写。先前advisory不自动成为缺陷。

当前16个section anchor仅定位这17条，不扩大编辑范围。

## e22d6fff0cc51ce714d920dcfd172d742b1e3e254c20401732fc7c2e59d63fa0

来源batch: batch-fe19bbe5e5898a0c3547
section: mod-tome/dialogs/Birther.lua
source_tag: _t

source: Custom Tiles have been added as a thank you to everyone that has donated to ToME.
They are a fun cosmetic feature that allows you to choose a tile for your character from a list of nearly 180 (with more to be added over time), ranging from special humanoid tiles to downright wonky ones!

If you'd like to use this feature and find this game good you should consider donating. It will help ensure its survival.
While this is a free game that I am doing for fun, if it can help feed my family a bit I certainly will not complain as real life can be harsh sometimes.
You will need an online profile active and connected for the tile selector to enable. If you choose to donate now you will need to restart the game to be granted access.

Donators will also gain access to the Exploration Mode featuring infinite lives.

当前target: 添加自定义角色贴图模式是为了对所有ToME捐赠者表示感谢。
你可以从近180个（以后还会添加）图标中选择一个你喜欢的角色个性贴图，从特殊的人形生物到各种奇怪的贴图都有。

如果你喜欢这类游戏并且你觉得这款游戏很好，你可以考虑捐赠。这会帮助延长这款游戏的寿命。尽管这只是我自娱自乐所做的一款游戏，如果它还能帮助我分担一点养家糊口的压力的话，我就谢天谢地，不会再抱怨现实的诸多压力了。
你需要一个已激活并保持连接的在线档案，贴图选择器才能启用。如果你现在选择捐赠，你需要重启游戏才能获得权限。
捐赠者也可以激活探索模式，获得无限的生命数。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/dialogs/Birther.lua:1396-1403展示捐赠自定义贴图说明。if you would like to use this feature被译为喜欢这类游戏，改变条件；还合并survival之后的换行及末段空行。恢复使用此功能的条件并按原文段落换行，不扩大到其他捐赠条目。surface将问题简述为this game误译不够精确，以完整条件的固定原文校正其归因。

## e2be3d83772c355423e6bac093c843cee00dbef05f7f18fb8303e7605123a3c2

来源batch: batch-fe19bbe5e5898a0c3547
section: mod-tome/init.lua
source_tag: init.lua load_tips

source: Corruptors feed off the essence of others, and can use their own corrupted blood to launch deadly magical attacks.

当前target: 腐化者可以吸取他人的精华，并使用他们的堕落力量发动致命的魔法攻击。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/init.lua:135加载提示明确their own corrupted blood。译文他们的堕落力量遗漏血液且归属不清；应恢复自身的腐化之血，不修改职业名称或术语库。

## e318607df2361e6d5bf0ed02ff84a4a4e2d4459d0f87c6e393be9d1b44375e8a

来源batch: batch-d83278160a384bef39ff
section: mod-tome/data/zones/wilderness/grids.lua
source_tag: _t

source: After walking many hours, you finally reach the end of the way. You are nearly on top of one of the highest peaks you can see.
The storm is raging above your head.

当前target: 在行走了几个小时后，你终于到达了终点。你站在了你能看到的最高峰位置。
风暴在你的头顶肆虐。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/data/zones/wilderness/grids.lua:726-727 明确nearly on top of one of the highest peaks。当前译文已经站在最高峰位置丢失尚近峰顶与之一两个限定；恢复这两点。many hours与几个小时是数量程度措辞，可一并准确表达为行走多时，但不把时间表达定为独立重大机制错误。

## e359df96b12ef0227123eb3b64af5384e6a7e5bdfc28b8c6311a180790638160

来源batch: batch-d83278160a384bef39ff
section: mod-tome/data/talents/spells/fire.lua
source_tag: tformat

source: Conjures up a bolt of fire that moves toward the target and explodes into a flash of fire, doing %0.2f fire damage in a radius of %d.
		The damage will increase with your Spellpower.

当前target: 向你的目标发射一枚爆裂火球，造成 %0.2f 火焰伤害，有效范围 %d 码。
		伤害受法术强度加成。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/data/talents/spells/fire.lua:140-181 Fireflash的range=7与radius缩放值独立，target.type=ball、radius来自getRadius，info传入的%d就是伤害半径。当前有效范围未准确说明爆炸的范围伤害半径，应明确目标处爆炸并对半径%d内造成伤害。surface断言已明确误译为射程过强，按半径关系遗漏确认；保留既有单位策略，不扩大为全局“码”替换。

## e3aebb45950c7a7bf37c98e7aafde7bcc1d72459cb6b3f0ddd94362771a61b71

来源batch: batch-d83278160a384bef39ff
section: mod-tome/data/zones/orc-breeding-pit/zone.lua
source_tag: _t

source: You arrive in a small underground structure. There are orcs there and as soon as they notice you they scream 'Protect the mothers!'.

当前target: 你来到了一个小型地下建筑前。那里有着许多兽人，当他们注意到你时，他们叫道“保护母亲们！”。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/data/zones/orc-breeding-pit/zone.lua:69-74 on_enter新区域时显示arrive in a small underground structure。当前建筑前改为建筑外部，恢复进入/抵达建筑内部的空间关系。

## e3b3e027a23bb74af6498bd77e02209815d965362c91056e4c4da45cbb9b23b7

来源batch: batch-d83278160a384bef39ff
section: mod-tome/data/timed_effects/mental.lua
source_tag: tformat

source: The target is lost in a nightmare that deals %0.2f darkness damage each turn and has a %d%% chance to cause a random detrimental effect.

当前target: 目标陷入清醒状态的噩梦之中，每回合造成 %0.2f 暗影伤害，并有 %d%% 概率受到一个随机不良效果。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/data/timed_effects/mental.lua:1602-1620 long_desc无清醒限定，on_timeout还显式检测sleep并提高不良效果几率。名称Waking Nightmare不能覆盖实际执行逻辑；去掉正文新增的清醒状态，不改效果名或术语库。contextual OK没有反向源码证据，宿主按固定代码确认surface此项。

## e3ed20c85beb1beae7cebab978c0437294794c8be88182aef1cf88fa0fe96a79

来源batch: batch-d83278160a384bef39ff
section: mod-tome/data/talents/cunning/cunning.lua
source_tag: _t

source: Collection of known poisons.

当前target: 制造各种不同毒素。

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/data/talents/cunning/cunning.lua:26是cunning/poisons-effects类别的Collection of known poisons说明，并非制造动作。当前制造各种不同毒素改变界面类别描述，恢复已知毒素集合/汇集的含义。

## e407b46fe58cb5b80eeea8e60392e672f075aa716a945c90d8ae7e403b3e7e59

来源batch: batch-d83278160a384bef39ff
section: mod-tome/data/talents/uber/cun.lua
source_tag: logSeen

source: #VIOLET#%s assembles %s!

当前target: #VIOLET#%s 重组为 %s！

确认修复依据：固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63：game/modules/tome/data/talents/uber/cun.lua:209-243创建TELOS_SPIRE物品o并加入self物品栏；日志两个%s分别self:getName与o:getName。当前重组为把执行者说成变身为物品，应表达执行者组装出该物品，保持两个参数顺序及markup不变。

## e433115e63be43b015cca379eadf2b0d75276411aabedf7c8c47ceebbbe1465d

来源batch: batch-d83278160a384bef39ff
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

“为什么你不准备成为精灵们的领袖呢？”，莱娜尼尔悠闲地躺在我的床上，双手撑着头饶有兴致地问道。

我的思绪还没有从片刻前的温存中缓过来，对于这个突然的问题感到有些惊异。“为什么我会想要成为他们的领袖呢？”，我反问道。

“当然了，因为你的实力是那么的强啊”，她回答道，“我觉得你是你同族中战斗能力最强的一位，这样强大的力量足以让你成为他们的领袖。”

我微笑道，“光靠武力是无法引领族人的。一个优秀的领袖需要勇于承担责任，审慎做出决定，并具有灵活的政治手腕。我对于这方面的事情可没有什么兴趣，毕竟，伊菲尼亚斯陛下在这方面比我擅长多了。只要给我一把剑，让我能够和部下一起驰骋沙场，我就已经心满意足了，让真正的领袖来思考我和我的战士应该与谁作战吧。”

她沉默半晌，看上去对我的回答并不满意，“呐，不过呢，你看起来对目前的计划并不满意。”

这一令人惊讶的提问让我感到一阵震惊，我不知道她究竟是如何瞬间洞悉了我的内心想法。在此之前，我从来没有在任何人面前表现出过我的担忧，然而她一下子就看穿了我的伪装。她和我五个星期前才刚刚见面，然而任何事情都逃脱不了她敏锐的洞察。

关于魔法大爆炸计划的筹备工作正在有条不紊地进行当中。卡库罗尔首领特塞尔已经返回了他位于北方的城堡，然而他的两个女儿仍然作为大使留在这里，协助我们的计划。这意味着莱娜尼尔和我可以时常相见，然而我们始终保守秘密。我高傲的同族们仍然难以接受精灵与人类的浪漫关系，而我们也无法接受可能迎来的流言蜚语。即使这样，我也难以抵御她的魅力，而她也是一样。

“我是一个战士，”许久的沉思后，我从床上爬起，整理我的长袍，“我喜欢亲自面对敌人，而不是借助某件遗物从远处消灭他们。这样的懦夫行径令真正的战士作呕。”

“然而，开发夏·图尔人遗迹中失落的力量不是那么让人心潮澎湃吗？”她呢喃着，手指轻触下唇，光滑的皮肤置身于柔软的被子的紧紧环绕中，仿佛已经被她那恢弘的梦想深深吸引，“这样强大的能量已经在世间沉眠了那么长时间，直到今天，我们强大的魔法可以让我们亲自驾驭它们，把雷霆万钧的恢弘气势掌握在不及盈寸的掌心之中……唉，若能由我亲自统领这般伟业，该有多好！”

搭上上衣的搭扣，我有些遗憾地摇了摇头。“坦率地说，我并不信任这些遗迹的力量。是的，我们永恒精灵的确有着强大的魔法实力。然而，我们渺小的知识比起那些夏·图尔人实在是相距甚远，以至于我们甚至无法理解他们所遗留下来的物件究竟有什么意义。在这一意义上，我的想法更接近你的孪生姐妹尼耶拉。我们应该用稳健的脚步前行，妥善而审慎地使用那些我们所能掌握的能力，而不是猛然把我们的野心扩展到这种庞大的实验之上。”

莱娜尼尔凝望着我，用调笑一般的语调柔声说道，“如果你成为了领袖，你可能会阻止这一切；但那样的话，或许我会一辈子恨你。”

我露出了浅浅的微笑。“嘛，那还真是一件可怕而又危险的事情。”当我更衣完成时，莱娜尼尔仍然在床上休息，眉间若有所思。“我必须要前去了解远行传送门那边工作的最新进展了。如果你乐意的话，请务必和我一同前去。”

她有些倦怠地摇了摇头。“不，我想要再休息一下。还有，听取他们的报告只会让我嫉妒不已。请让我在这里呆一会儿吧——我稍后就会秘密离开。”

我小心地关上卧房的房门，一股阴霾仍然在脑海之中萦绕。随着时间的推进，魔法大爆炸的庞大计划也一天天被提上日程，一股不详的预感涌上心头。命运总是那么残酷，与计划进行的有条不紊相伴的是兽人战线上的节节败退，只有少数几个种族能够防守他们的边境线，而兽人们的进攻却永不停歇，愈演愈烈。他们的数量似乎无穷无尽，永不枯竭。他们虽然不善战，却能重创毫无防备的村镇；只要兵力足够，甚至能攻陷城市。一周前，刚刚有一个人类王国在他们频繁的攻击下不堪其扰，最终溃败。此后，许多起初拒绝我们计划的人都跑来祈求我们的保护。看起来，对于兽人的侵袭这一迫在眉睫的危险，魔法大爆炸可能会成为我们唯一的希望。

我从卧房顺着宫殿向前，混乱的思绪在我的脑海中盘旋，伴随着我漫步过庭院走向大门。眼前红发女子轻盈的身影让我误以为莱娜尼尔已经跟着我一路走来，然而她金色的长袍和明亮的眼睛让我想起了，那是她的孪生姐妹尼耶拉。

“在想着什么人吗？”，她微笑地望着我，观察着刚刚表情细微的变化。

“抱歉，我刚才正在思考一些问题，”我轻轻弯腰对她示意。“我正准备前去督导和远行传送门有关的工作事宜，如果您——”

“我想和您一同前去。”还没等我说完，她就爽快地回应道。我点了点头，领着她坐上我的马车。

马车缓缓前行，尼耶拉的声音突然从我耳边传来。“她这样做只会伤害你。”

我一下子明白了她的意思，感到一阵震惊。“要命，在埃亚尔已经不存在秘密了吗？”我小声说道

“姐妹之间没有什么能隐瞒，尤其我们还是双胞胎。”她温柔地微笑着，然而眼神却没有一丝开玩笑的气息。“我是认真的。我爱我的姐妹，但我了解她的行事风格。她喜怒无常，想怎么做就怎么做。如果她对你感到厌倦，不要惊讶，也不要伤心。”

“我想，我应该有能力整理自己的心情。”我抿嘴说道。

她凝望着我的眼神慢慢移开，遥望着窗外变幻不定的风景。“唉，我想我已经提醒了你…”她柔声回答道，声音中仿佛包含着一阵忧伤。

是嫉妒促使她说出这番话吗？她嫉妒的是姐妹对我的关注，还是我对她姐妹的关注？我始终没有弄清。剩余的旅途中，我和尼耶拉始终保持沉默。夕阳从马车的背后缓缓落下，巨大的阴影投射在向前的小路上，暮色的笼罩将周围的风景染上了一片深红。有一瞬间，我们仿佛在恶魔的位面上漫步，漆黑的阴影慢慢融化在血色的土壤之上，群星惨淡的冷白色光辉似乎瞬间从苍穹直射下来。繁星点点间，遗迹从地平线映入眼帘，让我不禁颤栗。

已发现的夏·图尔遗迹中，鲜有能与埃尔瓦拉附近那一处的宏伟相提并论的。我们的人民花了几个世纪来悉心研究它，调动的工程量庞大无匹深入地下，却又如此小心地不曾损坏和扰乱任何遗迹中的古物。这个遗迹的核心被称为水晶塔。从地面上向下看，我们只能看到巨大的方块，在泥土被清理之后显露出来是比大理石更加光滑的白色石板。继续往下挖掘，白色石板似乎无穷无尽，其表面也没有任何能够给出说明的雕刻和标记，直到半英里后我们找到了它的底部，没有地基那样的设施。这简直就像着整座塔并不是立于地面之上，而是在天空中漂浮，直到某种力量让它从空中坠落，静静地在大地中沉眠了无数的岁月。

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

确认修复依据：L1: 裸体及人物受自身念头激起欲望的场景信息在译文中被删除/改成单纯被梦想吸引。应恢复原文事实，保留适当文学表达，不额外扩写。
L3: 译文仍有“就像”比喻框架，撤销模型“断言历史”的归因；但源文来自群星、从天空坠落的奇异事物被改成原先在天空漂浮、由某种力量使其坠落，新增悬浮状态与外力因果并遗漏群星意象。仅恢复原比喻内容，不把修辞比喻改成史实。
L5: would have to hate ye译成“或许我会一辈子恨你”，将必然/不得不的条件结果弱化为可能，并无依据增加终生期限。应恢复条件关系与语气，不增加一辈子。
L7: As soon as we took off east the mood changed被压缩为马车缓缓前行，遗漏向东出发及气氛随即变化，并新增缓慢速度。恢复这一句明确的方位与气氛转折；只修改此句，不全面改写旅途叙事。
只修以上4处已确认内容；其余advisory、大小姐称谓及长篇其他文风不全面重写。

## e454e243b1498217d1c15d8dba629bd73dd8959e05c0c6c1545c4bd7be6cfbb0

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/lore/keepsake.lua
source_tag: _t

source: You've entered a tranquil meadow. Something about this place seems familiar but you're not quite sure.
The only thing that you are sure of is that it has offered you a moment of rest from the long suffering of your cursed life.
You feel the hate inside you melt away. You feel as if the curse has subsided for a moment.

This place makes you wonder if there is a way to end the curse.
And if you can't overcome it you might be able to master it and take back a part of your life.
Either way, you feel the time has come to do something more about this curse.


当前target: 映入眼帘的，是一片宁静祥和的草原。这里似乎有什么令你感到熟悉，但你并不十分确定。
唯一可以确定的是，它让你从受诅咒人生的漫长苦难中得到了片刻喘息。
你感到体内的仇恨渐渐消融，仿佛连诅咒也暂时消退了。
在这片宁静的草地中，你萌发出一个念头。是否有什么方法能结束诅咒？即使你无法消除诅咒，你却有可能掌控它，并且夺回自己的一部分人生。
不管怎样，你感到是时候进一步应对这道诅咒了。


确认修复依据：固定源码 keepsake.lua:24–31 的7个LF在译文变为5个，This place前空行与And if前换行缺失；确认换行不变量缺陷，恢复两个换行。

## e4871be69ccc6d47bae940feeec6c9dc9392935cf4c279d4ebee63e15e143af4

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: A pristine belt of purest white leather with a runed voratun buckle. The ravages of neither time nor the elements have touched it.

当前target: 一条有着沃瑞钽雕刻标志的皮带扣，用纯白色皮革制作的古朴的腰带。不论时间还是环境都不能对它造成任何损害。

确认修复依据：固定 world-artifacts.lua:1615–1650 描述的是完好无瑕的白皮革腰带及刻符文的沃瑞钽带扣；现译古朴和修饰结构失真且漏符文，确认局部保真/语法问题。不推导不可毁坏属性。

## e4afe73e4f1c341bdd477f280fcefcb613e1b759c5ccdc2f46d867e73ce8a573

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/lore/shertul.lua
source_tag: _t

source: #{italic}#'The Great Sin.'#{normal}#

当前target: #{italic}#罪恶之源。#{normal}#

确认修复依据：固定 lore/shertul.lua:92–104 的The Great Sin是折磨阿马克泰尔壁画的字幕，指所绘大罪；译罪恶之源添加无依据的起源关系。确认局部字幕语义偏差，非全局术语策略。

## e4c192463aa9c11e29c4827fe3c1a1f22fda6a4b707e99e65f33c226ddf24d68

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/init.lua
source_tag: init.lua load_tips

source: 120 years ago Toknor and Mirvenia united the human and halfling kingdoms and wiped out the orcish race, thus establishing the Age of Ascendancy.

当前target: 120年前，图库纳与米雯尼雅将人类与半身人的王国联合起来，击溃了兽人军团，自此开启了卓越纪元。

确认修复依据：固定 init.lua:88–99 历史提示写wiped out the orcish race，同组有rendered extinct及隐藏兽人传闻；现译击溃军团将种族层面消灭弱化为军事胜利。恢复叙事表述，不以游戏中仍有兽人擅改旁白。

## e4c5fea288174229bde4b4395e927b41096465706d2818d60c003404609782bb

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/zones/town-shatur/npcs.lua
source_tag: entity name

source: thalore wilder

当前target: 精灵自然师

确认修复依据：固定 town-shatur/npcs.lua:23–29,71–88 的NPC所属subtype/faction及种族天赋均明确thalore；精灵泛称丢失原文明示的自然精灵亚种。确认局部名称遗漏，沿用现有自然精灵表达，不改变术语状态或跨批次命名政策。

## e4c8e609097f1ac7a9e630119b83b8c8f722ea7538d69233e06dcf289c3f25ce

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/talents/corruptions/vile-life.lua
source_tag: tformat

source: You manipulate the vim of enemies in radius %d to temporarily invert all healing done to them (but not natural regeneration).
		For 5 turns all healing will instead damage them for %d%% of the healing done as blight.
		The effect will increase with your Spellpower.

当前target: 你操控周围%d码范围内目标的活力，临时将他们所受到的所有治疗转化为伤害（但生命值自然回复除外）。
		在 5 回合内，他们受到的一切治疗将会被转化为相当于治疗量 %d%% 的枯萎伤害。
		效果受法术强度加成。

确认修复依据：固定 vile-life.lua:128–159 设置ball/radius及friendlyfire=false，engine/interface/ActorProject.lua:243–264,482–504跳过reactionToward>=0对象。原文enemies确为敌方限定，目标漏译；恢复半径内敌人，不扩大到全局距离单位策略。
确认enemies敌方限制被省略（vile-life.lua:128–159和ActorProject.lua友方过滤）。目标确为range8内选点的ball，参数为半径；周围未明确指自己，不能将其单独认定为必然错误自中心，但应随本项写成半径%d内敌人以去歧义。仅限本条，不全局修改距离单位。

## e50eb91c9e7b1a7ac740aa13bdeed09cd39db28d1a47e0916ff4f592feb731db

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/birth/classes/wilder.lua
source_tag: _t

source: The Spellblaze's scars may be starting to heal,
but little can change how the partisans feel.
Nature and arcane could bridge their divide -
and when it comes down to it, gold won't take sides...

当前target: 魔法大爆炸带来的裂痕已经开始痊愈。
然而人们心中的偏见仍没有消失。
自然与奥术本可弥合分歧——
在这两者之间，金钱从不站队……

确认修复依据：固定 birth/classes/wilder.lua:260 明确may be starting to heal，现译已经开始痊愈把可能/刚开始陈述为确定。接受独立复审提出的这条具体保真问题，局部恢复或许开始愈合的情态；表面partisans/偏见意见仍有下文种族阵营观念支撑，维持advisory，不重写全诗。

## e542306f47aa86f981bed8d5e008a42f8ffc57e090d8061a1841e9939e14c0d2

来源batch: batch-1da0a9afd2d1888c2099
section: mod-tome/data/talents/misc/npcs.lua
source_tag: tformat

source: You are able to perform usually unstealthy actions (attacking, using objects, ...) without breaking stealth.	 When you perform such an action while stealthed, you have a chance to stay hidden.
		Success is more likely against fewer opponents and is determined by comparing %0.2f times your stealth power (currently %d) to the stealth detection (reduced by 10%% per tile distance) of all enemies that have a clear line of sight to you.
		Your base chance of success is 100%% if you are not directly observed, and good or bad luck may also affect it.
		You estimate your current chance to maintain stealth as %0.1f%%.

当前target: 你学会在潜行状态下使用一些通常会打破潜行的技能（如攻击，使用物品……）当你在隐身状态下这么做的时候，你有一定概率不会打破潜行状态。
		面对的对手越少，成功率越高；你的成功率取决于你潜行强度的%0.2f倍（当前值 %d），以及所有视线能及你的敌人的侦测潜行能力（离你距离每有一格则下降10%%）。
		当你不在敌人的视野内时，基础成功率为 100%%，这一几率还受你的运气影响。
		你估计当前成功率为 %0.1f%%。

确认修复依据：固定 talents/misc/npcs.lua:3135–3163 首两句间明确句号；现译……）当……缺句界，确认局部语法问题，补句号。TAB不直接等同LF不变量；动作/潜行术语精细化及原本正确的数值公式不由本意见自动扩大修复。
固定 talents/misc/npcs.lua:3135–3163 反复用同一T_STEALTH/stealthDetection，首句actions明确包括使用物品，使用技能不能准确统摄所列行为。确认本条局部行动范围及潜行状态表达应一致，修复首句技能→行动、隐身→潜行，并合并既有句号修复；不动正确的三个格式参数/公式或开展跨批次术语改名。

## 首轮复审后有界补充（2026-09-22）

原四项回忆录修复保留。宿主根据 ADJUDICATION-R0.json 接受 RW4-R0-01/02：在相同已选条目、原138/158行对应段落内，另修“为何不是领袖”的当前身份及“身为领袖就能阻止”的能力关系。仅新增这两个子句，不扩大到其他段落、大小姐、其他文风、术语或条目；原冻结review输入和原实施证据不追溯改写。新EXECUTOR只修改 FIX-1.md 指定两处和本窗口新增本轮证据。
