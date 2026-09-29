# batch-062：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01866
位置：mod-tome.lua:24937；section：mod-tome/data/talents/gifts/fire-drake.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Spit a cloud of flames, doing %0.2f fire damage in a radius of %d each turn for %d turns.
		The flames will ignore the caster, and will drain 10%% of the damage dealt as the flames consume enemies life force and transfer it to the user.
		The damage will increase with your Mindpower, and can critical.
		Each point in fire drake talents also increases your fire resistance by 1%%.
```
译文：
```text
你喷出一片火焰，范围内的目标每回合会受到 %0.2f 火焰伤害（影响半径 %d），持续 %d 回合。
		火焰会无视使用者，并吸收 10%% 伤害治疗自身。
		伤害受精神强度加成。技能可暴击。
		每点火龙系的技能可以使你增加火焰抗性 1%%。
```

## entry-01867
位置：mod-tome.lua:24945；section：mod-tome/data/talents/gifts/fire-drake.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ breathes fire!
```
译文：
```text
@Source@喷出火焰！
```

## entry-01868
位置：mod-tome.lua:24956；section：mod-tome/data/talents/gifts/fungus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with a myriad of tiny, nearly invisible, reinforcing fungi.
		You gain %d maximum life and %d life regeneration.
		The effects will increase with your Willpower.
```
译文：
```text
使你自身周围环绕无数微不可见、有治疗作用的孢子。
		你获得 %d 最大生命值，%d 生命回复。
		效果受意志值加成。
```

## entry-01869
位置：mod-tome.lua:24962；section：mod-tome/data/talents/gifts/fungus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The fungus on your body allows regeneration effects to last longer.
		Each time you gain a beneficial effect with the regeneration subtype you increase its duration by %d%% + 1 rounded up.
		The effect will increase with your Mindpower.
```
译文：
```text
你身上的真菌让回复效果更加持久。
		每当你获得一个回复类的增益效果，你会让它的持续时间增加 %d%% +1，向上取整。
		技能效果受精神强度加成。
```

## entry-01870
位置：mod-tome.lua:24969；section：mod-tome/data/talents/gifts/fungus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your fungus reaches into the primordial ages of the world, granting you ancient instincts.
		Each time you receive non-regeneration healing you gain %0.1f%% of a turn per 100 life healed.  This effect can't add energy past 2 stored turns and overhealing is not counted.
		Also, regeneration effects on you will decrease your equilibrium by %0.1f each turn.
		The turn gain increases with your Mindpower.
```
译文：
```text
你的孢子可以追溯到创世纪元，你可以传承来自远古的天赋。
		每当你获得一个非回复的治疗效果，每治疗 100 点生命值，你获得 %0.1f%% 个回合。
		这一效果最多获得 2 个回合。
		同时，每当你受到回复作用时，每回合你的失衡值将会减少 %0.1f。
		增益回合受精神强度加成。
```

## entry-01871
位置：mod-tome.lua:24977；section：mod-tome/data/talents/gifts/fungus.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Sudden Growth
```
译文：
```text
骤然生长
```

## entry-01872
位置：mod-tome.lua:24987；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Nature heals and cleans you.
```
译文：
```text
利用大自然的力量治疗你受到的创伤、清洁你的身体。
```

## entry-01873
位置：mod-tome.lua:24989；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The way to combat magic, or even nullify it.
```
译文：
```text
对抗乃至使魔法失效的手段。
```

## entry-01874
位置：mod-tome.lua:24990；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：talent type；args_order：None；special：None

原文：
```text
summoning (melee)
```
译文：
```text
召唤（近战）
```

## entry-01875
位置：mod-tome.lua:24991；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The art of calling creatures adept in melee combat to your aid.
```
译文：
```text
召唤近战生物来协助你战斗的艺术。
```

## entry-01876
位置：mod-tome.lua:24992；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：talent type；args_order：None；special：None

原文：
```text
summoning (distance)
```
译文：
```text
召唤（远程）
```

## entry-01877
位置：mod-tome.lua:24993；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The art of calling creatures adept in elemental destruction to your aid.
```
译文：
```text
召唤远程元素攻击类生物来协助你战斗的艺术。
```

## entry-01878
位置：mod-tome.lua:24994；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：talent type；args_order：None；special：None

原文：
```text
summoning (utility)
```
译文：
```text
召唤（通用）
```

## entry-01879
位置：mod-tome.lua:24996；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：talent type；args_order：None；special：None

原文：
```text
summoning (augmentation)
```
译文：
```text
召唤（增益）
```

## entry-01880
位置：mod-tome.lua:24997；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The art of manipulating the lifespan and location of your summons.
```
译文：
```text
操纵召唤物寿命和位置的战斗艺术。
```

## entry-01881
位置：mod-tome.lua:24999；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The art of improving the quality of your summons.
```
译文：
```text
增强召唤物的战斗艺术。
```

## entry-01882
位置：mod-tome.lua:25001；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Through dedicated consumption of slime mold juice, you have gained an affinity with slime molds.
```
译文：
```text
通过坚持饮用黏菌汁液，你获得了对黏菌的亲和力。
```

## entry-01883
位置：mod-tome.lua:25003；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
By covering yourself in fungus, you better your healing.
```
译文：
```text
利用真菌环绕周身，增强你的治疗能力。
```

## entry-01884
位置：mod-tome.lua:25005；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Take on the defining aspects of a Sand Drake.
```
译文：
```text
化身成为土龙形态使你能使用土龙技能。
```

## entry-01885
位置：mod-tome.lua:25007；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Take on the defining aspects of a Fire Drake.
```
译文：
```text
化身成为火龙形态使你能使用火龙技能。
```

## entry-01886
位置：mod-tome.lua:25009；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Take on the defining aspects of a Cold Drake.
```
译文：
```text
化身成为冰龙形态使你能使用冰龙技能。
```

## entry-01887
位置：mod-tome.lua:25011；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Take on the defining aspects of a Storm Drake.
```
译文：
```text
化身成为雷龙形态使你能使用雷龙技能。
```

## entry-01888
位置：mod-tome.lua:25013；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Take on the defining aspects of a Venom Drake.
```
译文：
```text
化身成为毒龙形态使你能使用毒龙技能。
```

## entry-01889
位置：mod-tome.lua:25015；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Take on the aspects of aged and powerful dragons.
```
译文：
```text
继承远古真龙的力量使你能使用强大的龙族技能。
```

## entry-01890
位置：mod-tome.lua:25017；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Learn to channel your mental power through mindstars, forming powerful psionic blades.
```
译文：
```text
学会将你的精神能量灌注于灵晶中，产生心灵利刃。
```

## entry-01891
位置：mod-tome.lua:25019；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Cover the floor with natural mucus.
```
译文：
```text
用粘液覆盖地面。
```

## entry-01892
位置：mod-tome.lua:25023；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You learn to control moss, making it grow at will to help you on the battlefield.
```
译文：
```text
你学会控制苔藓生长，帮助战斗。
```

## entry-01893
位置：mod-tome.lua:25027；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You channel ooze through your psiblades.
```
译文：
```text
你向心灵利刃里灌注软泥能量。
```

## entry-01894
位置：mod-tome.lua:25029；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You channel acid through your psiblades.
```
译文：
```text
你向心灵利刃里灌注酸性能量。
```

## entry-01895
位置：mod-tome.lua:25031；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Unleash nature's fury against foes around you.
```
译文：
```text
向敌人释放自然的愤怒。
```

## entry-01896
位置：mod-tome.lua:25035；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Control the stone itself and bring it alive in the form of dreadful vines.
```
译文：
```text
掌握岩石并赋予其生命，形成恐怖的藤蔓。
```

## entry-01897
位置：mod-tome.lua:25037；section：mod-tome/data/talents/gifts/gifts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Learn to harness the innate power of your race.
```
译文：
```text
学会驾驭自身与生俱来的种族力量。
```

## entry-01898
位置：mod-tome.lua:25090；section：mod-tome/data/talents/gifts/higher-draconic.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ breathes venom!
```
译文：
```text
@Source@呼出毒液！
```

## entry-01899
位置：mod-tome.lua:25114；section：mod-tome/data/talents/gifts/malleable-body.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your body is more like that of an ooze, you can split into two for %d turns.
		Your original self has the original ooze aspect while your mitosis gains the acid aspect.
		If you know the Oozing Blades tree all the talents inside are exchanged for those of the Corrosive Blades tree.
		Your two selves share the same healthpool.
		While you are split both of you gain %d%% all resistances.
		Resistances will increase with Mindpower.
```
译文：
```text
你的身体变得像软泥怪一样，你可以分裂成2个，持续 %d 回合。
		你的本体获得原始的软泥特性，而分裂体则获得酸性特性。
		如果你习得软泥之刃系技能树，则该技能树会变为腐蚀之刃技能树。
		你和分裂体共享生命。
		当你分裂时，你和分裂体增加 %d%% 所有抵抗。
		抵抗受精神强度加成。
```

## entry-01900
位置：mod-tome.lua:25136；section：mod-tome/data/talents/gifts/malleable-body.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your body's internal organs are melted together, making it much harder to suffer critical hits.
		All direct critical hits (physical, mental, spells) against you have a %d%% chance to instead do their normal damage.
```
译文：
```text
你身体的内部器官融化在一起，使你更难遭受暴击。
		所有对你产生的直接暴击（物理、精神、法术）都有 %d%% 几率改按普通伤害结算。
```

## entry-01901
位置：mod-tome.lua:25151；section：mod-tome/data/talents/gifts/mindstar-mastery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Channel your mental power through your wielded mindstars, generating psionic blades.
		Mindstar psiblades have their damage modifiers (how much damage they gain from stats) multiplied by %0.2f, their armour penetration by %0.2f and mindpower, willpower and cunning by %0.2f.
		Also passively increases weapon damage by %d%% and physical power by 30 when using mindstars.
```
译文：
```text
将你的精神能量灌入你所装备的灵晶中，使其生成心灵利刃。
		灵晶所产生的心灵利刃的伤害修正（从属性中获得的伤害值）变为 %0.2f 倍，护甲穿透变为 %0.2f 倍，精神强度、意志和灵巧变为 %0.2f 倍。
		同时，还会在使用灵晶时增加 %d%% 武器伤害与 30 点物理强度。
```

## entry-01902
位置：mod-tome.lua:25157；section：mod-tome/data/talents/gifts/mindstar-mastery.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require a psiblade in your mainhand to use this talent.
```
译文：
```text
你需要主手的心灵利刃来使用该技能。
```

## entry-01903
位置：mod-tome.lua:25158；section：mod-tome/data/talents/gifts/mindstar-mastery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You touch the target with your psiblade, bringing the forces of nature to bear on your foe.
		Thorny vines will grab the target, slowing it by %d%% and dealing %0.2f nature damage each turn for 10 turns.
		Damage will increase with your Mindpower and Mindstar power (requires two mindstars, multiplier %2.f).
```
译文：
```text
你通过心灵利刃接触你的目标，将自然的怒火带给你的敌人。
		荆棘藤蔓会抓取目标，使其减速 %d%%，并且每回合造成 %0.2f 自然伤害，持续 10 回合。
		伤害受精神强度和灵晶强度加成（需要 2 只灵晶，加成比例 %2.f）。
```

## entry-01904
位置：mod-tome.lua:25164；section：mod-tome/data/talents/gifts/mindstar-mastery.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require two psiblades in your hands to use this talent.
```
译文：
```text
你需要双手的心灵利刃来使用该技能。
```

## entry-01905
位置：mod-tome.lua:25165；section：mod-tome/data/talents/gifts/mindstar-mastery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Smash your psiblades into the ground, creating a tide of crystallized leaves circling you in a radius of 3 for 7 turns.
		All foes hit by the leaves will start bleeding for %0.2f per turn (cumulative).
		All allies hit will be covered in leaves, granting them %d%% chance to completely avoid any damaging attack.
		Damage and avoidance will increase with your Mindpower and Mindstar power (requires two mindstars, multiplier %0.2f).
```
译文：
```text
将你的心灵利刃砸入地面，在你周围 3 码半径范围内形成一圈盘旋的结晶树叶，持续 7 回合。
		被树叶击中的敌人会开始流血，每回合受到 %0.2f 点伤害（可叠加）。
		所有被树叶覆盖的同伴，获得 %d%% 概率完全免疫任何伤害。
		伤害和免疫几率受精神强度和灵晶强度加成（需要 2 只灵晶，加成比例 %0.2f）。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
dragon	龙	T.GAME.ENTITY	creatures	entity type	existing	global	
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mainhand	主手	T.GAME.ENTITY	items	nil	existing	core	
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
