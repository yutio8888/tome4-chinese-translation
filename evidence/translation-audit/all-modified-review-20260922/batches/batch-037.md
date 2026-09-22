# batch-037：1 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01224
位置：mod-tome.lua:15300；section：mod-tome/data/lore/elvala.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#From the memoirs of Aranion Gawaeil, leader of the Grand Council of Elvala#{normal}#

#{bold}#Chapter Seven: Into Darkness#{normal}#

We veiled our guilt, cloaked our crimes.  Though we had some communication with the outside through halfling traders and the odd disguised Shaloren adventurer, we remained mute to the world at large, hidden from their accusing gaze.  Outside our quiet walls others had not the luxury of hiding.  The Spellhunt was begun, and it knew no mercy.

Ordinary people rose up against what they perceived as the arrogance of the mages, a revolt against the power of the few that had ruined the lives of so many.  Any suspected of sorcery or ties to the Art were cruelly dealt with.  There was sympathy for none, and many innocents fell victim to the unquenchable thirst for retribution.  The madness swept across the whole of Maj’Eyal.

Law and order had broken down.  Armies, territories and whole cities had been destroyed or ravaged by the Spellblaze, with many areas left completely uninhabitable.  Kingdoms fell and tyrants arose.  Bandits picked at the bones of civilisation like vultures on a rotten corpse.

An organisation called the Ziguranth, thought dead long ago, came into resurgence, gaining popular support from the people in their anti-magic crusade.  We heard of some mages going into hiding, but inevitably being rooted out, or fleeing desperately from place to place.  Dark tales also arose of necromancers and fell wizards creating dungeons and strongholds, fending off or evading attacks, and beginning reigns of terror.

And one tale came to my ears of a group of mages that managed to band together and stay in hiding, though always on the run from the chasing Ziguranth.  The story from outside was that they were led by a demon with fiery hair, fiercely glowing eyes and hands wrapped in flames, that fought with blazing wrath and could be opposed by none.  I knew that description well...

I carried out my reign, my duty, taking care of the Shaloren people.  We were safe from attackers, secure in our supplies through discrete trade, and slowly building back some of what we had lost.  But both fear and shame prevented us from showing our face to the world.

Fifteen long years passed before I awoke one night in my council chambers, the crescent Wintertide moon softly illuminating a shape near the end of my bed.  The figure was tall and slim, wrapped in tight-fitting wools and furs.  Her crimson hair stirred gently as she stood with her back to me.  Memories arose of a night long ago, in a more innocent time, when a younger me and a younger her first became close.

I barely dared to whisper her name, afraid that she might disappear, an apparition or a dream that could be broken by a spoken word.  “Linaniil,” I softly mouthed.  She turned to me, and I saw those same dark eyes I remembered.  But they were surrounded by lines of care, the markings of years of strain and responsibility clear on her face.

Rising from my bed I gathered a robe about me.  I took a few steps towards her but stopped, not able to move myself any further.  I wanted to be near her, to put my arms around her, but it felt as if she were across a wide chasm from me, a gulf of time and pain between us.

“I have come for help, Aranion,” she said in a low voice, not quite meeting my gaze.  “There be something I seek, and ye must aid me in achieving it.”  I did not understand, but I nodded my assent.  “Get ye dressed and ready then.  There be a long journey ahead of us.”

She stepped towards the window, her back towards me again, waiting as I put on a stralite mail and gathered my sword.  When she noticed I was ready she levitated out, and I followed.

We whistled through the air, travelling northwards at great speed.  The lands swept beneath us, and the climate grew colder as we went further and further north.  Hours passed in intrepid silence, till we were flying above snowy tundra.  We soared past plains of white and grey before we reached a low range of hills.  Here Linaniil slowed and descended, and I went down beside her.  We came to rest before a dark opening at the foot of the hills.

Linaniil stood for a while staring at the black cave.  Fear radiated from her face, but her eyes were hard and determined.  “It is here,” she said quietly, her voice steady.  I followed her gaze, trying to guess what secrets this remote place contained, but I could sense nothing special.

She marched forwards and I followed, until we came right up to the shadowed opening.  Linaniil hesitated a moment, staring into the blackness, before finally stepping inside and being swallowed from sight.  I could feel it then, the sensation that something ancient lay in this place.  My skin tingled and my arcane attunement felt on fire.  This dark cave held some mysterious force, secluded from all knowledge since the oldest days of Eyal.  There was something here that could change the destiny of the world.

I took a deep breath and stepped forwards.
```
译文：
```text
#{italic}#来自 艾伦尼恩·加威尔 ——时任埃尔瓦拉最高议会的领袖——的回忆#{normal}#

#{bold}#第七章：进入黑暗#{normal}#

我们掩藏了自己的罪恶，遮蔽了自己的罪行。虽然我们通过半身人商人和偶尔乔装出行的永恒精灵冒险者与外界保持着些许联系，但面对整个世界，我们依旧沉默，躲在他们谴责的目光之外。可在我们寂静的城墙之外，其他人没有这份藏身的奢侈。魔法狩猎开始了，并且毫无怜悯。

普通人站了起来，反抗那些他们眼中傲慢的法师，反抗那少数人的力量——正是这种力量毁掉了无数人的生活。任何被怀疑通晓巫术或与奥术有牵连的人都会被残酷对待。他们不同情任何人，许多无辜者都变成了这场不可抑制的报复欲望的受害者。疯狂席卷了整个马基·埃亚尔。

法律和秩序已经完全崩溃。魔法大爆炸带来的灾难肆虐摧毁了无数的军队，领土和城市，许多土地都变得完全无法居住。王国倒台，暴君取而代之。强盗们如同腐烂尸体上的秃鹫，在文明的废墟上四处横行霸道。

一个名为伊格兰斯、外界以为早已消亡的组织，突然重新兴起。他们在民众反对魔法的狂热中获得了广泛的支持。我听说，有些法师躲藏了起来，但终究难免被揪出来，或是拼命地不断东躲西藏。还有另一些黑暗的故事，那些死灵法师和堕落的巫师为了抵抗或躲避攻击，修筑了地牢和堡垒，开始了恐怖的统治。

我还听到了另一个故事，有一群法师决定团结，一起隐藏起来，然而他们仍然不断在伊格兰斯的袭击下被迫逃跑。在那些外面世界的传说里，那些法师被一个有着火焰一样的头发，烈焰一般的双眼，手中裹挟着火焰的恶魔所领导。她用愤怒的烈焰战斗，没人能够战胜她。我对于这样的描述很是熟悉……

我仍然继续着我的统治，继续着我的职责，保护永恒精灵人民。我们已经不用害怕袭击者，可以通过零散的交易确保我们的补给，并且正在慢慢重建我们所失去的东西。但是，畏惧和羞愧仍然让我们不敢向世界展示我们自己。

十五年后的一个夜晚，我在我的议会室里醒来，看到霜华之月的月牙微光照亮了我床位的一个身影。那是一个高大而苗条的身影，身穿紧身的羊毛与毛皮衣物。她背对着我，深红的长发在空中起舞。我想到了无数年前的夜晚，那是我还更加天真的时代，年轻时的我和年轻时的她第一次如此靠近的那个夜晚。

我简直不敢说出她的名字，生怕这一切都只是我的一场梦境，当我说出那个名字的时候，这个美好的梦境就会破裂而消失殆尽。“莱娜尼尔…”我轻声说道。她的身体转向我，我看到我记忆中的那双黑色的眼睛。然而，她的脸上已经充满了操劳的痕迹，岁月、压力和责任已经在她的脸上留下了痕迹。

我从床上起来，穿上我的长袍。我朝着她的方向前进了几步，但停了下来，不敢再次继续前进。我想要接近她，想要再一次和她相拥，但那一瞬间，我们之间仿佛又有了一道巨大的藩篱——时间和苦痛的鸿沟已经阻隔了我们。

“我是来这里请求帮忙的，艾伦尼恩”，她用低沉的声音说道，目光却不大敢与我对视。“我有一些想要寻求的东西，你必须帮我实现它。”我不明白这意味着什么，但我还是点头同意。“穿好衣服，准备出发吧。前面还有很长的一段路要走。”

她走向窗台，再一次背对着我，直到我穿上斯莱特锁甲，拿起我的剑。当她注意到我已经准备好了的时候，她向外飞去，而我也紧随其后。

我们在空中呼啸而过，以极快的速度向北飞行。望向我们脚下所飞过的大地的痕迹，随着我们向北方越走越远，气候越来越冷。在一片沉默中，时间缓缓流逝，我们飞越白雪皑皑的苔原。我们掠过了白色和灰色的平原，到达了一片低山丘陵。莱娜尼尔在这里减速并下降，我也紧随在她的身后。我们在山脚下的一个黑暗的洞口前停了下来。

莱娜尼尔站在这里，凝望着眼前黑色的山洞。她的脸上散发着些许恐惧，但她的眼睛充满意志和决心。“它在这里，”她用坚定的口气平静地说道。我循着她的目光，试图猜测这个遥远的地方包含着什么秘密，但我没有察觉到任何特别之处。

她不断向前，我紧随其后，直到我们来到了一个被阴影覆盖的入口。莱娜尼尔迟疑了一会儿，望向洞口的黑暗，然后终于走了进去，从视野中消失了。我可以感受到，某种古老的力量正在这里沉睡。我的皮肤一阵刺痛，体内的奥术亲和如同燃烧起来。这个黑暗的洞穴里蕴藏着某种神秘力量，自埃亚尔最古老的时代起便不为人知。这里的某样东西足以改变世界的命运。

我深吸一口气，向前走去。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
veil	猎杀	T.GAME.EFFECT	combat	effect subtype	preferred	core	仅用于 Stalking/Stalked 的内部效果分类；按猎杀机制语境处理，不作普通名词“面纱”
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
