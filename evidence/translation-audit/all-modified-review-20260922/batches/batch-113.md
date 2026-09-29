# batch-113：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03645
位置：tome-cults.lua:3644；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Target briefly saw what True Horror means, deeply scaring it. %d%% chances to fail using a talent.
```
译文：
```text
目标被真正的恐惧吓倒，%d%% 几率使用技能失败。
```

## entry-03646
位置：tome-cults.lua:3679；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is overwhelmed by voices from the void, giving them a 20%% higher chance to spawn hallucinations from Dark Whispers and causing them to take an additional %d%% temporal damage from Dark Whispers and Hideous Visions.
```
译文：
```text
目标被虚空之声淹没，让他们从黑暗低语中产生幻觉的几率增加 20%%，并使他们从黑暗低语和失智冲击中受到额外 %d%% 时空伤害。
```

## entry-03647
位置：tome-cults.lua:3707；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is doomed to ruin.  On falling below 75%%, 50%% or 25%% life all enemies in radius %d will take %0.2f darkness damage
```
译文：
```text
目标被诅咒进入毁灭状态。当生命值降低至 75%%, 50%% 或 25%% 时，%d 格内敌人将受到 %0.2f 暗影伤害。
```

## entry-03648
位置：tome-cults.lua:3725；section：tome-cults/data/timed_effects.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#ORANGE#The wounds of #Source# appear on #target#!#LAST#
```
译文：
```text
#ORANGE##Source#身上的创伤出现在#target#身上！#LAST#
```

## entry-03649
位置：tome-cults.lua:3733；section：tome-cults/data/timed_effects.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#LIGHT_RED#A void annihilator manifests from %s!
```
译文：
```text
#LIGHT_RED#一个虚空歼灭者从%s的身上出现了！
```

## entry-03650
位置：tome-cults.lua:3770；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The target has %d increased saves and defense, %d%% increased critical chance, and %d%% chance to avoid all damage.
```
译文：
```text
目标豁免和闪避增加 %d，暴击率增加 %d%%，有 %d%% 几率闪避所有伤害。
```

## entry-03651
位置：tome-cults.lua:3776；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target has tied itself to the fate of another. If it dies, it's chosen target will die in it's place and it will be healed by %d for each stack of Fortune and Jinx.
```
译文：
```text
目标将自身的命运和另一个人相连，当它死亡时，选择的目标将代替它死亡。此时，自身的幸运层数和所选目标身上的不幸层数会被消耗；若所选目标有不幸，则按其层数治疗，否则按自身的幸运层数治疗，每层恢复 %d 点生命。
```

## entry-03652
位置：tome-cults.lua:3794；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Teleport: Kroshkkur
```
译文：
```text
传送：克诺什库尔
```

## entry-03653
位置：tome-cults.lua:3802；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Slowly transfered to a Forbidden Tome.
```
译文：
```text
正在被缓慢转移到禁忌之书。
```

## entry-03654
位置：tome-cults.lua:3832；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reduces all damage taken by %d%% and remove all detrimental effects on application.
```
译文：
```text
降低所有受到的伤害 %d%%。施加该效果的时候会解除所有负面效果。
```

## entry-03655
位置：tome-cults.lua:3845；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is starting to get mad (%d stacks), reducing mind damage resistance by %d%%, mental save by %d, confusion resistance by %d%%, generating %0.1f insanity per turn.
```
译文：
```text
目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，%d%% 混乱免疫，每回合获得 %0.1f 疯狂值。
```

## entry-03656
位置：tome-cults.lua:3865；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s body is evolved!
```
译文：
```text
#Target#的身体进化了！
```

## entry-03657
位置：tome-cults.lua:3875；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is enveloped with entropic forces!
```
译文：
```text
#Target#被熵能覆盖！
```

## entry-03658
位置：tome-cults.lua:3880；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is bolstered at the sight of the horror!
```
译文：
```text
#Target#在恐魔的视线中被强化了！
```

## entry-03659
位置：tome-cults.lua:3929；section：tome-cults/data/zones/entropic-void/grids.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The rift leads... somewhere.
```
译文：
```text
裂缝通向…某个地方。
```

## entry-03660
位置：tome-cults.lua:3975；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Training dummy. Use it to train.
```
译文：
```text
训练用傀儡。用它来训练吧。
```

## entry-03661
位置：tome-cults.lua:3979；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A human student.
```
译文：
```text
一个人类学徒。
```

## entry-03662
位置：tome-cults.lua:3982；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A shalore student.
```
译文：
```text
一个永恒精灵学徒。
```

## entry-03663
位置：tome-cults.lua:3985；section：tome-cults/data/zones/ft-cultist/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A halfling student.
```
译文：
```text
一个半身人学徒。
```

## entry-03664
位置：tome-cults.lua:4026；section：tome-cults/data/zones/ft-haze-cave/grids.lua；source_tag：say；args_order：None；special：None

原文：
```text
#YELLOW#You hear a terrible shriek.
```
译文：
```text
#YELLOW#你听到了一声可怕的尖叫。
```

## entry-03665
位置：tome-cults.lua:4035；section：tome-cults/data/zones/ft-haze-cave/npcs.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
Grung made great being angry!
```
译文：
```text
格朗格激怒了伟大的存在！
```

## entry-03666
位置：tome-cults.lua:4088；section：tome-cults/data/zones/ft-haze-cave/zone.lua；source_tag：log；args_order：None；special：None

原文：
```text
#ANTIQUE_WHITE#Grung: %s
```
译文：
```text
#ANTIQUE_WHITE#格朗格：%s
```

## entry-03667
位置：tome-cults.lua:4097；section：tome-cults/data/zones/ft-home/grids.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You can leave items here for safekeeping.
```
译文：
```text
你可以把物品安全地留在这里。
```

## entry-03668
位置：tome-cults.lua:4141；section：tome-cults/data/zones/ft-horrors/objects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A page of the tome.
```
译文：
```text
书页。
```

## entry-03669
位置：tome-cults.lua:4194；section：tome-cults/data/zones/ft-illusory-castle/grids.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#GOLD#An object rolls from the chest!
```
译文：
```text
#GOLD#一件物品从宝箱中掉了出来！
```

## entry-03670
位置：tome-cults.lua:4297；section：tome-cults/data/zones/ft-illusory-castle/zone.lua；source_tag：log；args_order：None；special：None

原文：
```text
#%s#Welcome to chapter "%s"!
```
译文：
```text
#%s#欢迎来到章节 "%s"！
```

## entry-03671
位置：tome-cults.lua:4308；section：tome-cults/data/zones/ft-yaech/grids.lua；source_tag：say；args_order：None；special：None

原文：
```text
#YELLOW#You hear a terrible shriek.
```
译文：
```text
#YELLOW#你听到了一声可怕的尖叫。
```

## entry-03672
位置：tome-cults.lua:4360；section：tome-cults/data/zones/godfeaster/zone.lua；source_tag：say；args_order：None；special：None

原文：
```text
#OLIVE_DRAB#You can feel tremors in the worm.. A gastric wave is coming! Dodge to an alcove!
```
译文：
```text
#OLIVE_DRAB#你能感觉到虫子在颤抖……一波胃液来了！躲进凹室！
```

## entry-03673
位置：tome-cults.lua:4483；section：tome-cults/data/zones/test/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Swordsmith
```
译文：
```text
铸剑铺
```

## entry-03674
位置：tome-cults.lua:4484；section：tome-cults/data/zones/test/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Nature's Punch
```
译文：
```text
自然的重击
```

## entry-03675
位置：tome-cults.lua:4487；section：tome-cults/data/zones/test/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Night's Star
```
译文：
```text
暗夜之星
```

## entry-03676
位置：tome-cults.lua:4514；section：tome-cults/data/zones/town-kroshkkur/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Destroy @himher@!
```
译文：
```text
摧毁@himher@！
```

## entry-03677
位置：tome-cults.lua:4516；section：tome-cults/data/zones/town-kroshkkur/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A drem cultist.
```
译文：
```text
一位德瑞姆邪教徒。
```

## entry-03678
位置：tome-cults.lua:4544；section：tome-cults/data/zones/town-kroshkkur/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Swordsmith
```
译文：
```text
铸剑铺
```

## entry-03679
位置：tome-cults.lua:4545；section：tome-cults/data/zones/town-kroshkkur/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Nature's Punch
```
译文：
```text
自然的重击
```

## entry-03680
位置：tome-cults.lua:4548；section：tome-cults/data/zones/town-kroshkkur/traps.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Night's Star
```
译文：
```text
暗夜之星
```

## entry-03681
位置：tome-cults.lua:4559；section：tome-cults/hooks/bonestaff.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GREY##{italic}#You feel the bones of the staff creeking and vibrating in your hand.#{normal}##LAST# Yes... #{italic}#"master"#{normal}#.
```
译文：
```text
#GREY##{italic}#你感受到手中的骨杖在你的手上颤动：#{normal}##LAST# 是的……#{italic}#“主人”#{normal}#。
```

## entry-03682
位置：tome-cults.lua:4595；section：tome-cults/hooks/bonestaff.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Great!
```
译文：
```text
太棒了！
```

## entry-03683
位置：tome-cults.lua:4596；section：tome-cults/hooks/bonestaff.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GREY##{italic}#The staff stays calm.#{normal}##LAST# Stupid useless pathetic excuse of a #{italic}#"necromancer"#{normal}#! Why refuse to use true power?!
```
译文：
```text
#GREY##{italic}#法杖平静了下来。#{normal}##LAST#像你这样的#{italic}#"死灵法师"#{normal}#竟然会用这样蹩脚的借口！为什么要拒绝使用真正的力量？！
```

## entry-03684
位置：tome-cults.lua:4614；section：tome-cults/overload/data/texts/intro-cults.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome #LIGHT_GREEN#@name@#WHITE#.
You are one of several like-minded individuals that delves into knowledge long lost and forgotten, seeking sanctuary from an outside hostile world to such activities. Delving into research within the forgotten and inactive fortress of Kroshkkur, the reasons of pursuit differ among a myriad of topics. Some look to uncover knowledge hailing back to the Age of Haze when beings immensely powerful walked Eyal, while others explore the origins of themselves and other races.

Regardless of the subject or method of research, no rules exist to constrain anyone in their approach. This has led to experimentation into what many would deem mad and certainly forbidden among the surface dwellers. If Kroshkkur were to be found it would most certainly be destroyed. Therefore the only rules that truly exist in the sanctuary are that of secrecy and safeguarding the accrued knowledge that has been obtained therein.

But today the sanctuary is threatened by a giant worm that is tunneling directly towards Kroshkkur. If nothing is done it will collide with and destroy what remains of the ancient fortress. One idea to dealing with the worm is for someone to teleport inside it and make there way towards the worms brain cluster and destroy it. Alternatively, you consider leaving before the worm arrives and finding your own purpose in the outside world.

As with all things here, nothing restrains you in what path you #{bold}#ultimately choose#{normal}#. The question is whether you step into the #{bold}#portal to teleport into the worm#{normal}# or leave now while it is safe to do so and let #{bold}#Kroshkkur be destroyed#{normal}#.

```
译文：
```text
欢迎 #LIGHT_GREEN#@name@#WHITE#。
你是一群钻研那些丢失遗忘已久的知识的志同道合者之一。在这个对这些知识并不友好的世界，你们找到了一个避难所。在被遗忘的废弃堡垒克诺什库尔，你们基于自己的理由追寻禁忌的知识。有些人希望解开过去的阴影，了解到有关无比强大的古代生物在埃亚尔行走的混沌纪的过去，而有些人则孜孜探索自己和其他种族的起源。

在这里，没有任何规则限制任何人，不管你研究的主题和方法是什么。这导致了对许多地表人视为疯狂且被禁止之事的实验，而你们的研究内容也被普通人的社会所禁止。如果克诺什库尔被发现，它一定会被摧毁。因此，在避难所的唯一规则就是必须对在里面学到的知识进行严格的保密和保护。

然而今天，避难所却面临着一条直接冲向克诺什库尔的巨型蠕虫的威胁。如果再不迅速做出决断，它将会直接撞向并摧毁古代堡垒的残骸。有一个击败蠕虫的办法，那就是将某一个人传送到蠕虫体内，让他前往蠕虫的脑簇所在之处，将其摧毁。或者，你也可以考虑在蠕虫到来之前离开，在外面的世界找到你自己的目的。

就像这里的一切一样，没有人会干涉#{bold}#你自己的选择#{normal}#。你可以现在#{bold}#踏入通向巨型蠕虫体内的传送门#{normal}#或者就这样离开#{bold}#任由克诺什库尔被巨型蠕虫摧毁#{normal}#。

```

## 相关术语快照
```tsv
Annihilator	歼灭者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	兽人战役职业
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Drem	德瑞姆	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Swordsmith	长剑铁匠铺	T.GAME.ENTITY	places	entity name	existing	core	城镇商店实体
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
drem	德瑞姆	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
rift	裂隙	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
