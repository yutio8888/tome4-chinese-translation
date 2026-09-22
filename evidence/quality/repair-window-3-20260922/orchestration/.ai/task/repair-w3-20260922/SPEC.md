# 修复窗口3：244—246的14条已确认译文

模式implement，Paseo MCP，schema5 translation_contextual_v2。用户已恢复连续审核并授权调整流程/prompt后继续，每批推送。246已finalize、维护已推送，基线9fb5ec1df3c74e09fd981bb7d16300d6bce25ef9。

唯一EXECUTOR只可修改mod-tome.lua中下列14个source/section/source_tag的target，以及evidence/quality/repair-window-3-20260922/的本窗口核验证据。后续宿主提供确定事实后可更新handoff.md和逐字节安装已验证catalog/migration产物；初次实施禁止这些出版操作。不得修改其他译文/术语/规则/工具/旧证据，禁止stage/commit、写.ai或创建agent。保留baseline全部无关未跟踪文件。

每个来源批次必须真实repair preflight通过后才派发实施；原schema workset分别保留。三条独立宿主补充另列，不伪造repair_required或durable batch。WORKSET.json是14条有界宿主组合清单，不是官方单批workset。SOURCE-ANCHORS.json只含固定公开源码；SOURCE-CLAIMS.json为宿主确认依据，不可提供给独立reviewer。

固定tome源码624a67329fe2ad440c5b344785a9c73fcf22ae63；全部为tome，无DLC。保留source/source_tag/args_order/special、printf/markup及当前target换行/tab序列；只改获准target，全条核对完整性。不得恢复与固定实现矛盾的英文表述。归档RW1-SIB-01/02和Archmage不在范围。

验收：14条实际修复；LuaJIT加载只变这14个target，其他记录完全一致；严格lint/已有proposal校验（若产生proposal）、空白/占位符/markup/newline/tab不变量；每个数值占位符记录quantity_kind/index/producer/consumer，涉及治疗/伤害/持续时间和附加机制的方向值流有源码锚点；四成员独立v2 REVIEW及FINAL全量复审；完整17门禁/严格addon构建、DONE_VERIFIED；译文commit→queue rebuild→单次catalog/migration-chain→证据commit→queue rebuild→push。successor仍待重新审核。

当前14节anchor范围只用于来源定位，不扩大14条编辑范围。

## df61b36589e10427e9962900498418cf33dc207b93ebf0018c7d8b4a92c59345

来源batch: batch-f426f5a2d72329efe102
section: mod-tome/data/talents/psionic/psi-archery.lua
source_tag: tformat

source: You temporarily set aside a part of you mind to direct your telekinetically-wielded bow. It will automatically attack the nearest target each turn for %d turns.
			The telekinetically-wielded bow uses Willpower in place of Strength and Cunning in place of Dexterity to determine attack and damage.
			You are not telekinetically wielding anything right now.

当前target: 你暂时分出一部分精神去控制念动之弓。它会在 %d 回合内自动攻击1个目标。
			念动弓使用意志和灵巧来代替力量和敏捷决定攻击。
			你暂时还没有装备任何念动武器。

确认修复依据：补回每回合自动攻击及属性同时决定攻击和伤害。固定源码rng.table选敌，不能照英文恢复最近目标；无须改同族其他条目。

## df8f5280bf187a1f2e54241eff9b371cbcdb0d753fe7f40c7534d827878af4b4

来源batch: batch-f426f5a2d72329efe102
section: mod-tome/data/talents/cursed/shadows.lua
source_tag: tformat

source: While this ability is active, you will continually call up to %d level %d shadows to aid you in battle. Each shadow costs 5 hate to summon. Shadows are weak combatants that can: Use Arcane Reconstruction to heal themselves (level %d), Blindside their opponents (level %d), and Phase Door from place to place.
		Shadows ignore %d%% of the damage dealt to them by their master.

当前target: 当此技能激活时，你可以召唤 %d 个等级 %d 的阴影帮助你战斗。每个阴影需消耗 5 点仇恨值召唤。
		阴影是脆弱的战士，它们能够：使用奥术重组治疗自己（等级 %d），使用闪电突袭攻击敌人（等级 %d），使用相位之门进行传送。
		阴影无视主人对它们造成的 %d%% 伤害。

确认修复依据：持续激活期间会自动补召阴影至最多%d，单只5仇恨；不写成一次或任意手动召唤。保留等级、各技能名/等级和主人减伤。

## dfdfbe60890fa648d9b45b47b9e18c6c12129666160860591d4b44ba0e08c378

来源batch: batch-939b816bedca462e4fc8
section: mod-tome/data/talents/spells/aether.lua
source_tag: tformat

source: Surround yourself with Pure Aether, increasing all your arcane damage by %0.1f%% and ignoring %d%% arcane resistance of your targets.
		At level 5 casting Aether Avatar removes up to %d magical or physical detrimental effects.

当前target: 纯净的以太能量环绕着你，增加 %0.1f%% 奥术伤害并且无视目标 %d%% 奥术抗性。
		在等级 5 时，使用以太之体会移除 %d 个魔法或物理负面效果。

确认修复依据：清除数量是最多%d，不保证每次清除恰好该数量。

## dff11a9be5d688263842862c8d065f6da9d332faef7d18b35855b7bb17934e32

来源batch: batch-939b816bedca462e4fc8
section: mod-tome/data/talents/cursed/crimson-templar.lua
source_tag: tformat

source: Draw on the wounds of enemies within range 10, healing yourself and putting them into a merciful sleep.
							The sleep chance increases with your Spellpower.
							You are healed for %d%% of the remaining damage of bleed effects on enemies in range (minimum %d per bleed). Enemies fall asleep for %d turns longer than their longest-lasting bleed, rendering them unable to act. The strength of the sleep effect is based on the strength of the bleed. Excess damage will reduce their sleep duration.
							
							When the sleep ends, each target will benefit from Insomnia for a number of turns equal to the amount of time it was asleep (up to ten turns max), granting it 50%% sleep immunity.

当前target: 吸收附近10码范围内敌人的伤痕以治疗自己，并仁慈地使它们入睡。
							睡眠概率受法术强度加成。
							你获得距离内敌人剩余流血伤害 %d%% 的治疗（每个流血敌人至少 %d 点）。敌人睡眠的持续时间为 %d 回合加上流血效果中最长的持续时间，期间无法行动。睡眠效果的强度由流血效果的强度决定，额外的伤害会缩短它们睡眠的时间。

							睡眠结束时，目标会受失眠效果获得50%%睡眠免疫，持续时间等于它睡着的时间（最大10回合）。

确认修复依据：minimum %d per bleed是每个流血效果的最低治疗量，不是每个流血敌人。循环每个effect执行math.max再累计。全条其他机制保留。

## e035e585a6aab2d698f018e59bf75b627f451524788fe8df9a739acf45e9b317

来源batch: batch-939b816bedca462e4fc8
section: mod-tome/data/damage_types.lua
source_tag: _t

source: skewered

当前target: 被烤成肉串

确认修复依据：skewered死亡描述指刺穿/穿成串，不含烤制含义。

## e0886c07f8c3d3450ad3db559fbbbaebe377e0d67e2374b0c374089d6f22fd1c

来源batch: batch-939b816bedca462e4fc8
section: mod-tome/data/timed_effects/floor.lua
source_tag: tformat

source: The target is in a whistling vortex, granting +%d ranged defense, -%d ranged accuracy and incoming projectiles are 30%% slower.

当前target: 目标靠近尖啸漩涡，增加 +%d 远程闪避，同时 -%d 远程命中，并且抛射物减缓 30%%。

确认修复依据：目标处于漩涡中；减速对象是向目标飞来的抛射物，不泛指其发射的抛射物。保留两项远程属性和30%%。

## e1177a8f9f689644a232269ab42be3597862f1d26ab23562b7d6171aa6d4faf9

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/lore/shertul.lua
source_tag: _t

source: You see a mural showing a huge metropolis made of crystal, with small islands of stone floating in the air behind it. In the foreground is sitting a Sher'Tul, with a hand stretched up to the sky.
There is some text beneath 

当前target: 你在壁画上看到一个巨大的水晶之城，有数个浮空岛悬浮在周围。在画面的最前端坐着的是夏·图尔人，他向天空笔直的举起手臂。
下面有一行文字

确认修复依据：恢复水晶城后方的小型石质岛屿、前景夏·图尔与伸向天空的手；不增加额外关系，保持换行。

## e122dd9c588110e524f88fff62fa5c22a25ecd479f49ee7c2fe5fdf14a7ea7d1

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/birth/classes/afflicted.lua
source_tag: _t

source: The Doomed strike from behind a veil of darkness or a host of shadows.

当前target: 末日使者操纵阴影，从黑暗中发动攻击。

确认修复依据：恢复从黑暗帷幕或阴影群掩护下出击的并列关系。操纵阴影有职业语境但不足以替代该句；不改职业名。

## e128c83148dea5452e6b6b00ae7f012edd33d7b5df2e8a7be284e4930a7f56b2

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/talents/gifts/fungus.lua
source_tag: tformat

source: Your fungus reaches into the primordial ages of the world, granting you ancient instincts.
		Each time you receive non-regeneration healing you gain %0.1f%% of a turn per 100 life healed.  This effect can't add energy past 2 stored turns and overhealing is not counted.
		Also, regeneration effects on you will decrease your equilibrium by %0.1f each turn.
		The turn gain increases with your Mindpower.

当前target: 你的孢子可以追溯到创世纪元，你可以传承来自远古的天赋。
		每当你获得一个非回复的治疗效果，每治疗 100 点生命值，你获得 %0.1f%% 个回合。
		这一效果最多获得 2 个回合。
		同时，每当你受到回复作用时，每回合你的失衡值将会减少 %0.1f。
		增益回合受精神强度加成。

确认修复依据：治疗先截断溢出量，再按每100实际治疗获得回合能量；能量总存储最多2回合，不是每次最多获2回合。保留regeneration排除、失衡每回合减少、精神强度加成。

## e1343327ead953361b1fefe6fb85fd1569679eb6b9a269a08a6f5c1c8a473152

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/timed_effects/physical.lua
source_tag: tformat

source: Engaged in a grapple draining %d stamina per turn and redirecting %d%% of damage taken to %s.  Any movement will break the effect as will some unarmed talents.

当前target: 目标进入抓取状态，每回合吸取 %d 体力，同时将 %d%% 伤害转移到 %s。任何移动或其他一些徒手技能都会取消这个状态。

确认修复依据：擒抱消耗持有者自身的体力，并将所受伤害的一部分转给抓取目标；不是吸取资源，也不是消耗生命。保持3个占位符次序与中断条件。

## e172753e04e296ee928a40a0b54f754ad2788f68a8563f03f587fefe0f4a66f1

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/talents/psionic/solipsism.lua
source_tag: tformat

source: Each time you take damage, you roll %d%% of your mental save against it.  A successful saving throw can crit and will reduce the damage by at least 50%%.
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		The first talent point also increases your solipsism threshold by 10%% (currently %d%%).

当前target: 每当你受到伤害时，你会使用 %d%% 精神豁免来鉴定。鉴定时精神豁免可能暴击，至少减少 50%% 的伤害。
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能也会增加你 10 %%唯我临界点（当前 %d%%）。

确认修复依据：只有豁免检定成功才减伤至少50%%，且该成功分支能精神暴击。固定代码支持基础属性10的既有补充，保留其正确逻辑；不借机全局改名或单位。

## e1884052fcd739907285aff6c5dc71dab76ccba369640aefe7951a978c6d79c7

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/talents/chronomancy/other.lua
source_tag: tformat

source: You manipulate the spacetime continuum in such a way that you switch places with another creature with in a range of %d.  The targeted creature will be confused (power %d%%) for %d turns.
		The spell's hit chance will increase with your Spellpower.

当前target: 你控制时间的流动来使你和 %d 码范围内的某个怪物交换位置。目标会混乱（%d%% 强度）%d 回合。
		法术命中率受法术强度加成。

确认修复依据：恢复操纵时空、与另一个生物交换位置；Map.ACTOR无敌对怪物限制。范围单位跨批统一不在范围；保留目标混乱强度/时长和命中加成。

## e1cd6fb504f3f8c421bbdb98148886f74982d2a5c9d5460e47e768a5388dc529

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/lore/misc.lua
source_tag: _t

source: Dear Rolf,

I hope this letter finds you well. I must apologise for this recent dry spell in our communication; my adventures across Maj'Eyal have taken many exciting and perilous turns as of late. What turns do I speak of, you ask? I know how you delight in reading the accounts of my exploits, so I shall waste no further time on this pre-amble.

Imagine, if you will, a wolf. Imagine a beastly wolf, a wolf with strength, ferocity and a lust for flesh matching that of an entire pack of its lesser kind. You too may have some small experience with these "wargs" as the locals are wont to call them. Now... imagine one the size of a bear. Truly, as I travelled the lands surrounding Derth did I come across such a monstrous, awe-inspiring, lupine adversary. With fangs of a length to match my own blade, I entered combat against this lupine lord and its skulking brood. To my regret I failed in slaying the beast, but I assure you - simply surviving against such feral rage is an honour worthy of recognition and renown.

And indeed, would there have been much glory in killing such a creature? True, I would have had enough to fur to line each and every boot and hat in Derth, but legends must live on. They are what give this world its very spirit!

With eager anticipation for your reply,
Weisman

当前target: 亲爱的罗尔夫，

我希望这封信可以安全的到达你手。我必须为我们最近这段时间疏于联系道歉：最近，我在马基·埃亚尔各地的冒险经历又有了许多惊险刺激的转折。你问我说的是什么转折？我知道你很喜欢阅读我的冒险事迹，所以客套话我就不多说了。

想像一下，一只庞大如熊的饿狼，赤眼如炙，饥渴的吞噬着它周围一切的生命。这只暴君所带来的威胁远超一整群它弱小的同类。你也许亦曾对付一些当地人口中所谓的座狼，但想象一下这只如同熊一般巨大的“好家伙”。事实上，当我在周围的旅行时，不巧就遭遇到了这样一只令人生畏的贪婪怪物，它挥舞的獠牙比我的剑还要长。于是我与这只座狼王和它的狼子狼孙们展开了激烈的搏斗。可惜的是我最终并没有杀死这只野兽，但我能自豪的说，能从这场战斗中存活就已经是值得称道的了。

再说，杀死这样的生物又能有多大荣耀呢？对，我确实会得到一大堆狼毛，多到足以给德斯镇每双靴子和每顶帽子做毛皮衬里，但我的内心告诉自己这种传说中的生物必须让其繁衍下去。因为正是它们，赋予了这个世界真正的灵魂！

殷切的期盼着你的回信，
威斯曼

确认修复依据：完整恢复书信事实：问候收信人安好、德斯周边遇敌、狼的力量凶性嗜血与整群同类相当、獠牙与剑等长、传说应流传；删除赤眼/吞噬周围一切生命等杜撰，不将live on改为生物繁殖。保留既有专名及段落布局。

## e200845e1abc8076051b8f755bd28ff1bfe68ebb7009b6c15f1b022aaecd461a

来源batch: batch-a5489a23ea457e1c6fde
section: mod-tome/data/talents/techniques/warcries.lua
source_tag: tformat

source: Your battle cry shatters the will of your foes within a radius of %d, lowering their Defense by %d for 7 turns, making them easier to hit.
		All evasion and concealment bonuses are also disabled.
		The chance to hit increases with your Physical Power.

当前target: 你的怒喝会减少 %d 码半径范围内敌人的意志，减少它们 %d 闪避，持续 7 回合。
		同时，躲闪效果和不可见带来的闪避效果会被取消。
		命中率受物理强度加成。

确认修复依据：shatters the will是击溃斗志，不减少Willpower属性。实际效果降combat_def并禁用evasion和不可见未命中优势；若修正文中范围形状，固定target.type=cone为准，不写成全向半径。单位全局统一不在范围。
