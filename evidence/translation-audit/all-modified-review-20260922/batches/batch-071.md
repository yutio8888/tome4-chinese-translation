# batch-071：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02228
位置：mod-tome.lua:29163；section：mod-tome/data/talents/spells/master-necromancer.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#GREY#(%d to minion: %s)#LAST#
```
译文：
```text
#GREY#(%d 到不死随从：%s)#LAST#
```

## entry-02229
位置：mod-tome.lua:29183；section：mod-tome/data/talents/spells/master-of-bones.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Call of the Crypt
```
译文：
```text
地宫召唤
```

## entry-02230
位置：mod-tome.lua:29184；section：mod-tome/data/talents/spells/master-of-bones.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Call upon the battlefields of old, collecting bones, fusing them with souls, and forging them into skeletal minions.
		Up to %d skeleton warriors of level %d are summoned, and up to %d skeletons can be controlled at once.
		At level 3 the summons become armoured skeletons warriors.
		At level 5, for every 3 skeleton warriors, a skeleton mage or archer will also be created without costing any souls. If this makes you go over your skeleton limit, a normal skeleton will be removed and its soul refunded.

		#GREY##{italic}#Skeleton minions come in fewer numbers than ghoul minions but are generally more durable.#{normal}#
		
```
译文：
```text
从古战场中收集白骨，将灵魂附着在白骨上，将其转化为你的骷髅随从。
		最多召唤 %d 个 %d 级的骷髅战士，且最多可同时掌控 %d 个骷髅。
		技能等级 3 时，你将会改为召唤武装骷髅战士。
		技能等级 5 时，每当你召唤 3 个骷髅战士，将会额外召唤一个骷髅法师或骷髅弓箭手，不消耗灵魂。如果这超过了你的骷髅数量上限，会移除一个普通骷髅，并返还其灵魂消耗。

		#GREY##{italic}#骷髅的数量一般来说比食尸鬼更少，但是它们一般来说更加强韧。#{normal}#
		
```

## entry-02231
位置：mod-tome.lua:29199；section：mod-tome/data/talents/spells/master-of-bones.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Any time one of your skeleton or bone giant dies, it shatters in radius %d, making any foe bleed for %0.2f physical damage over 5 turns.
		If any other skeleton or bone giant minion is in the radius it will pickup some of the bones to enhance itself, increasing maximum and current life by %d, armour by %d and gain %0.2f physical melee retaliation for 20 turns.
		This talent never works when you kill your own minions.
		
```
译文：
```text
每当你的骷髅或骨巨人死去时，它会在半径 %d 码范围内粉碎，使敌人在5回合内受到 %0.2f 物理流血伤害。
		如果范围内有其他骷髅或骨巨人，它们会使用这些骸骨强化自己，增加最大和当前生命值 %d，护甲值 %d，并获得 %0.2f 物理近战报复效果，持续 20 回合。
		如果你杀死自己的随从，这一效果不会触发。
		
```

## entry-02232
位置：mod-tome.lua:29277；section：mod-tome/data/talents/spells/master-of-flesh.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Shattering up to %d ghouls or ghasts you create a putrescent swirling cloud of radius %d that follows you around for 3 turns per dead ghoul plus one turn. Oldest ghouls are prioritized for destruction.
		Any ghoul or ghast dying or expiring within this cloud increases its duration by %d turn and every two absorbed ghoul/ghast your gain back one soul.
		The cloud deals %0.2f frostdusk damage to any foes caught inside.
		The damage will increase with your Spellpower.
		
```
译文：
```text
你粉碎最多 %d 个食尸鬼或妖鬼，在身边创造出半径 %d 码、并持续跟随你的腐败云雾，持续时间为杀死的食尸鬼数量乘 3 再加一回合。你会优先选择最老的食尸鬼。
		每个在云雾中死去或到期的食尸鬼或妖鬼会增加它的持续时间 %d 回合，每死亡2个食尸鬼或妖鬼会恢复1点灵魂。
		云雾会对其中的所有敌人造成 %0.2f 霜暮伤害。
		伤害受法术强度加成。
		
```

## entry-02233
位置：mod-tome.lua:29323；section：mod-tome/data/talents/spells/meta.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You learn to finely craft and tune your spells, reducing all their cooldowns by %d%%.
		In doing so you can also carve a hole in spells that affect an area to avoid damaging yourself.  The chance of success is %d%%.
		In addition, you hone your damaging spells to spellshock their targets. Whenever you deal damage with a spell you attempt to spellshock them with %d more Spellpower than normal. Spellshocked targets suffer a temporary 20%% penalty to damage resistances.
```
译文：
```text
你学会巧妙控制和调谐你的法术，降低 %d%% 法术冷却时间。
		此外，你可以控制自己的攻击性魔法，尝试在攻击范围中留出空隙，避免伤及自身。成功概率为 %d%%。
		此外，你还能磨练你的伤害法术，尝试对目标施加法术冲击。每当你用法术造成伤害时，你会尝试以比正常高出 %d 点的法术强度对目标施加法术冲击。被法术冲击的目标暂时减少 20%% 伤害抗性。
```

## entry-02234
位置：mod-tome.lua:29329；section：mod-tome/data/talents/spells/meta.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mastery over magic is so great that you can alter the energy of all damaging spells to suit your needs.
		Whenever you deal damage with a spell you attune to the element of that spell for 6 turns, converting %d%% of any damage you deal into that element.
		This effect will not override itself and will only trigger from spells directly cast by you, not from damage over time or ground damage effects.
```
译文：
```text
你对魔法的掌握是如此精巧，你可以调节任何伤害性法术的能量，来为你所用。
		每当你使用法术造成伤害的时候，你会调谐到该法术的元素，持续 6 回合，你造成的所有伤害中的 %d%% 将会转化为该元素。
		这一效果不会覆盖自身，只会被你直接释放的法术触发，不会因持续伤害或地面伤害效果而触发。
```

## entry-02235
位置：mod-tome.lua:29335；section：mod-tome/data/talents/spells/meta.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mastery of arcane flows allow you to reset the cooldown of up to %d of your spells (that don't have a fixed cooldown) of tier %d or less.
		In addition for %d turns you are overflowing with energy; all known spells are considered one talent level higher when casting them.
```
译文：
```text
你对奥术的精通使你能重置法术的冷却时间，重置至多 %d 个法术的冷却（对固定冷却时间的技能无效），对技能层次 %d 或更低的技能有效。
		此外，在接下来的 %d 回合内，你充满能量，释放法术的时候，技能等级视为额外增加 1 级。
```

## entry-02236
位置：mod-tome.lua:29363；section：mod-tome/data/talents/spells/necrosis.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
As you continue to attune your body to undeath you reject nature as a whole.
		As long as you have no natural infusion on your skin, each rune on it increases your minimum negative life by -%d and your spells critical chance by %0.1f%%.

		Currently: %s
```
译文：
```text
你拒绝自然，让自己的身体离不死越来越近。
		如果没有自然纹身，你身上的每个符文提供 -%d 生命底线和 %0.1f%% 法术暴击率。

		当前：%s
```

## entry-02237
位置：mod-tome.lua:29370；section：mod-tome/data/talents/spells/necrosis.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Spikes of Decrepitude
```
译文：
```text
衰老尖刺
```

## entry-02238
位置：mod-tome.lua:29371；section：mod-tome/data/talents/spells/necrosis.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each turn you unleash dark powers through your runeskin.
		For each rune you have a random foe in sight will be hit by a spike of decrepitude, dealing %0.2f frostdusk damage.
		A foe can only be hit by one spike per turn.
		If your life is below 1, the spikes also reduce all damage done by the targets by %d%%.
```
译文：
```text
你每回合都从符文皮肤中释放出黑暗能量。
		你每拥有一个符文，就会用衰老尖刺攻击视野内的一名随机敌人，造成 %0.2f 霜暮伤害。
		每个敌人每回合只会被尖刺攻击一次。
		如果你的生命值在 1 以下，尖刺还会使目标造成的伤害减少 %d%%。
```

## entry-02239
位置：mod-tome.lua:29415；section：mod-tome/data/talents/spells/phantasm.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creates a globe of pure light within a radius of %d that illuminates the area and deals %0.2f damage to all creatures.
		At level 3, it also blinds all who see it (except the caster) for %d turns.
```
译文：
```text
制造一个发光的球体，照亮 %d 码半径范围区域，并对所有生物造成 %0.2f 点光系伤害。
		在等级 3 时，它同时可以致盲看到它的人（施法者除外）%d 回合。
```

## entry-02240
位置：mod-tome.lua:29486；section：mod-tome/data/talents/spells/rime-wraith.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hoarfrost now has additional effects:
		- if friendly: magical and physical saves increased by %d, at level 5 healing factor is also increased by 15%%.
		- if hostile: magical and physical saves reduced by %d, at level 5 all talents cool down 15%% slower.
		
```
译文：
```text
寒霜覆盖效果获得以下额外效果：
		- 友方目标：提升 %d 魔法和物理豁免，技能等级 5 时，还会提升治疗系数 15%%。
		- 敌对目标：降低 %d 魔法和物理豁免，技能等级 5 时，还会使技能冷却时间延长 15%%。
		
```

## entry-02241
位置：mod-tome.lua:29498；section：mod-tome/data/talents/spells/spectre.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-02242
位置：mod-tome.lua:29499；section：mod-tome/data/talents/spells/spectre.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s's ghost walk fizzles!
```
译文：
```text
%s的游魂行走失败了！
```

## entry-02243
位置：mod-tome.lua:29519；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Arcane studies manipulate the raw magic energies to shape them into both offensive and defensive spells.
```
译文：
```text
用奥术操控魔法源能量，使你能用此能量进行攻击和防御。
```

## entry-02244
位置：mod-tome.lua:29521；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Tap on the core arcane forces of the aether, unleashing devastating effects on your foes.
```
译文：
```text
释放以太的核心力量，将敌人毁灭。
```

## entry-02245
位置：mod-tome.lua:29523；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of fire to burn your foes to ashes.
```
译文：
```text
使用火的威力将你的目标烧成灰烬。
```

## entry-02246
位置：mod-tome.lua:29525；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of wildfire to burn your foes to ashes.
```
译文：
```text
使用野火的威力将你的目标烧成灰烬。
```

## entry-02247
位置：mod-tome.lua:29527；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of the earth to protect and destroy.
```
译文：
```text
使用土的力量进行攻击和防御。
```

## entry-02248
位置：mod-tome.lua:29529；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of the stone to protect and destroy.
```
译文：
```text
使用石的力量进行攻击和防御。
```

## entry-02249
位置：mod-tome.lua:29531；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of water to drown your foes.
```
译文：
```text
使用水的力量淹死目标。
```

## entry-02250
位置：mod-tome.lua:29533；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of ice to freeze and shatter your foes.
```
译文：
```text
使用冰的力量冰冻并粉碎你的目标。
```

## entry-02251
位置：mod-tome.lua:29535；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of the air to fry your foes.
```
译文：
```text
操纵大气的力量轰击你的目标。
```

## entry-02252
位置：mod-tome.lua:29537；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harness the power of the storm to incinerate your foes.
```
译文：
```text
使用风暴的力量打击你的目标。
```

## entry-02253
位置：mod-tome.lua:29539；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Meta spells alter the working of magic itself.
```
译文：
```text
超魔系法术能改变魔法的效能。
```

## entry-02254
位置：mod-tome.lua:29541；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The school of time manipulation.
```
译文：
```text
学习操控时间。
```

## entry-02255
位置：mod-tome.lua:29543；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Control the power of tricks and illusions.
```
译文：
```text
掌控诡计与幻象之力。
```

## entry-02256
位置：mod-tome.lua:29545；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Magical enhancement of your body.
```
译文：
```text
用魔法强化你的身体。
```

## entry-02257
位置：mod-tome.lua:29547；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The pinacle of spellcasting.
```
译文：
```text
施放法术的巅峰。
```

## entry-02258
位置：mod-tome.lua:29549；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Conveyance is the school of travel. It allows you to travel faster and to track others.
```
译文：
```text
学习传送，使你能更快的旅行或者追踪目标。
```

## entry-02259
位置：mod-tome.lua:29551；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Divination allows the caster to sense its surroundings, and find hidden things.
```
译文：
```text
侦查技能可以使施放者能侦查周围环境，搜寻隐藏的东西。
```

## entry-02260
位置：mod-tome.lua:29553；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Command the arcane forces into healing and protection.
```
译文：
```text
使用奥术力量进行治疗和防御。
```

## entry-02261
位置：mod-tome.lua:29555；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Manipulate gems to turn them into explosive magical bombs.
```
译文：
```text
用宝石制造各种魔法炸弹。
```

## entry-02262
位置：mod-tome.lua:29559；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Learn to craft and upgrade your golem.
```
译文：
```text
学习制造并提升你的傀儡。
```

## entry-02263
位置：mod-tome.lua:29561；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Advanced golem operations.
```
译文：
```text
高级傀儡操纵技巧。
```

## entry-02264
位置：mod-tome.lua:29564；section：mod-tome/data/talents/spells/spells.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Alchemical control over fire.
```
译文：
```text
操控火焰的炼金法术。
```

## entry-02265
位置：mod-tome.lua:29638；section：mod-tome/data/talents/spells/staff-combat.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Blunt Thrust without a staff weapon!
```
译文：
```text
你需要一把法杖来施展该技能！
```

## entry-02266
位置：mod-tome.lua:29639；section：mod-tome/data/talents/spells/staff-combat.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning blow!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-02267
位置：mod-tome.lua:29640；section：mod-tome/data/talents/spells/staff-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hit a target for %d%% melee damage and stun it for %d turns.
		Stun chance will improve with Spellpower.
		At level 5, this attack cannot miss.
```
译文：
```text
挥动法杖对目标造成 %d%% 近程伤害并震慑目标 %d 回合。
		震慑概率受法术强度加成
		在等级 5 时，此攻击必中。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
ghost	幽灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
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
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wildfire	焱	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	技能类型与技能树内部名称；与“焱系”“焱之书”保持一致，普通描述中的 wildfire 仍按语境译为“野火”
```
