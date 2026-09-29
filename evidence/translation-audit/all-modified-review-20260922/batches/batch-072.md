# batch-072：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02268
位置：mod-tome.lua:29652；section：mod-tome/data/talents/spells/stone-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Carve 40 to 80 alchemist gems out of a natural gemstone.
		Alchemist gems are used for many other spells, and each gem type creates a different effect.
```
译文：
```text
从自然宝石中制造 40 ～ 80 个炼金宝石。
		许多法术需要使用炼金宝石，每种宝石拥有不同的特效。
```

## entry-02269
位置：mod-tome.lua:29662；section：mod-tome/data/talents/spells/stone-alchemy.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You imbue your %s with %s.
```
译文：
```text
你在 %s 上安装了 %s。
```

## entry-02270
位置：mod-tome.lua:29663；section：mod-tome/data/talents/spells/stone-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Imbue %s with a gem (up to tier %d), granting it additional powers.
		You can only imbue items once, and it is permanent.
```
译文：
```text
在 %s 上附魔宝石（最大材质等级 %d），使其获得额外增益。
		你只能给每个装备附魔 1 次，并且此效果是永久的。
```

## entry-02271
位置：mod-tome.lua:29670；section：mod-tome/data/talents/spells/stone-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Crush 5 alchemist gems into dust to mark impassable terrain next to you. You immediately enter it and appear on the other side of the obstacle, up to %d grids away.
```
译文：
```text
将 5 枚炼金宝石碾碎为粉末，标记你身旁的一块不可通行地形。你立即进入其中并出现在障碍物另一侧，穿越距离至多 %d 格。
```

## entry-02272
位置：mod-tome.lua:29688；section：mod-tome/data/talents/spells/stone.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures %d missile-shaped rocks that you target individually at any target or targets in range.  Each missile deals %0.2f physical damage, and an additional %0.2f bleeding damage every turn for 5 turns.
		At talent level 5, you can conjure one additional missile.
		The damage will increase with your Spellpower.
```
译文：
```text
释放出 %d 个岩石飞弹，你可以为每个飞弹独立指定射程内的任意目标。每个飞弹造成 %0.2f 物理伤害和每回合 %0.2f 流血伤害，持续 5 回合。
		在等级 5 时，你可以额外释放一个飞弹。
		伤害受法术强度加成。
```

## entry-02273
位置：mod-tome.lua:29694；section：mod-tome/data/talents/spells/stone.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You root yourself into the earth, and transform your flesh into stone.  While this spell is sustained, you may not move, and any forced movement will end the effect.
		Your stone form and your affinity with the earth while the spell is active has the following effects:
		* Reduces the cooldown of Earthen Missiles, Pulverizing Auger, Earthquake, and Mudslide by %d%%.
		* Grants %d%% Fire Resistance, %d%% Lightning Resistance, %d%% Acid Resistance, and %d%% Stun Resistance.
		Resistances scale with your Spellpower.
```
译文：
```text
你将自己扎根于土壤并使你的肉体融入石头。
		当此技能被激活时你不能移动并且任何移动会打断此技能效果。
		当此技能激活时，受你的石化形态和土壤相关影响，会产生以下效果：
		* 减少岩石飞弹、粉碎钻击、地震和山崩地裂冷却时间回合数：%d%%
		* 获得 %d%% 火焰抗性，%d%% 闪电抗性，%d%% 酸性抗性和 %d%% 震慑抵抗。
		受法术强度影响，抗性按比例加成。
```

## entry-02274
位置：mod-tome.lua:29705；section：mod-tome/data/talents/spells/stone.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Causes a violent earthquake that deals %0.2f physical damage in a radius of %d each turn for %d turns, and potentially stuns any and all creatures it affects.
		The damage will increase with your Spellpower.
```
译文：
```text
引起一波强烈的地震，每回合造成 %0.2f 物理伤害（%d 码半径范围），持续 %d 回合。有概率震慑此技能所影响到的怪物。
		伤害受法术强度加成。
```

## entry-02275
位置：mod-tome.lua:29717；section：mod-tome/data/talents/spells/storm.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lightning emanates from you in a circular wave with radius %d, doing %0.2f to %0.2f lightning damage (%0.2f average) and possibly dazing anyone affected (75%% chance).
		The damage will increase with your Spellpower.
```
译文：
```text
一圈闪电从你身上放射出来，在 %d 码范围内对目标造成 %0.2f ～ %0.2f 闪电伤害（平均 %0.2f）并有 75%% 概率眩晕敌人。
		伤害受法术强度加成。
```

## entry-02276
位置：mod-tome.lua:29726；section：mod-tome/data/talents/spells/storm.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Hurricane
```
译文：
```text
飓风
```

## entry-02277
位置：mod-tome.lua:29743；section：mod-tome/data/talents/spells/temporal.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
This intricate spell instantly erects a time shield around the caster, preventing any incoming damage and sending it forward in time.
		Once either the maximum damage (%d) is absorbed, or the time runs out (%d turns), the stored damage will return as a temporal restoration field over time (5 turns).
		Each turn the restoration field is active, you get healed for 10%% of the absorbed damage (Aegis Shielding talent affects the percentage).
		The shield's max absorption will increase with your Spellpower.
```
译文：
```text
这个复杂的法术在施法者周围立刻制造一个时间屏障，吸收你受到的伤害。
		一旦达到最大伤害吸收值（%d）或持续时间（%d 回合）结束，存储的能量会治疗你，持续 5 回合，每回合回复总吸收伤害的 10%%（强化护盾技能会影响该系数）。
		最大吸收值受法术强度加成。
```

## entry-02278
位置：mod-tome.lua:29750；section：mod-tome/data/talents/spells/temporal.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Removes the target from the flow of time for %d turns. In this state, the target can neither act nor be harmed.
		Time does not pass at all for the target, no talents will cooldown, no resources will regen, and so forth.
		The duration will increase with your Spellpower.
```
译文：
```text
将目标从时光的流动中移出，持续 %d 回合。
		在此状态下，目标不能动作也不能被伤害。
		对于目标来说，时间是静止的，技能无法冷却，也没有能量回复……
		持续时间受法术强度加成。
```

## entry-02279
位置：mod-tome.lua:29769；section：mod-tome/data/talents/spells/thaumaturgy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#%s [known, eligible]#LAST#
```
译文：
```text
#LIGHT_BLUE#%s [已学会，可触发]#LAST#
```

## entry-02280
位置：mod-tome.lua:29790；section：mod-tome/data/talents/spells/thaumaturgy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
By weaving arcane triggers around you feet you can use the residual energies of your beam spells for free movement.
		Each time you cast a beam spell you can move right afterwards without spending a turn.
		This spell has %d charges. Once all charges are spent it unsustains.
		If you exit combat with some charges left it will after 10 turn regenerates its charges, if you have enough mana.
```
译文：
```text
你将奥术力量编织于双脚，可以使用射线类法术来进行免费移动。
		每当你释放一个射线类法术，你可以立刻移动一次，不需要消耗时间。
		这一法术有 %d 次充能。当充能耗尽时，这一法术将会解除持续。
		若你在尚有剩余充能时脱离战斗，则在脱离战斗 10 回合后，只要法力充足便会消耗法力补满充能，否则解除持续。
```

## entry-02281
位置：mod-tome.lua:29798；section：mod-tome/data/talents/spells/thaumaturgy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using your near-perfect knowledge of beam spells you combine them all into a powerful 3-wide beam of pure energy.
		The beam deals %0.2f thaumic damage and always goes as far as possible.
		Thaumic damage can never be resisted by anything but "Resistance: All", always uses your highest resistance penetration and highest damage type bonus and can never be altered into other damage types.
		It can trigger Burning Wake and Hurricane.
		It is affected by the wet status (+30%% damage) if you are in Shivgoroth Form.
		It has a 25%% chance to either stun or freeze the targets for 3 turns (if Crystalline Focus or Uttercold are active, respectively).
		Each time you deal damage with a beam spell, the remaining cooldown is reduced by 1 (this can happen only once per turn).
		The damage will increase with your Spellpower.
```
译文：
```text
你的射线类法术已臻化境，可以将各种元素合并起来，发射出纯粹能量构成，宽度为3的强力射线。
		射线造成 %0.2f 奇术伤害，且必定发射到最远距离。
		奇术伤害无法被“全体抗性”之外的任何抗性阻挡，使用你最高的抗性穿透属性和最高的伤害加成属性，且无法被变为其他伤害类型。
		这一技能可以触发无尽之焰和飓风。
		如果你处在西弗格罗斯形态下，对潮湿目标伤害增加 30%%。
		在开启水晶力场或绝对零度的情况下，技能分别有 25%% 几率震慑或冻结目标 3 回合。
		每当你使用射线类技能造成伤害，这一技能的冷却时间降低 1 回合（这一效果每回合最多触发一次）。
		伤害受法术强度加成。
```

## entry-02282
位置：mod-tome.lua:29843；section：mod-tome/data/talents/spells/water.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
A #LIGHT_BLUE#wave of icy water#LAST# erupts from the ground!
```
译文：
```text
一股 #LIGHT_BLUE#冰冷的水流#LAST# 从地面上涌现！
```

## entry-02283
位置：mod-tome.lua:29853；section：mod-tome/data/talents/spells/water.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You absorb latent cold around you, turning into an ice elemental - a shivgoroth - for %d turns.
		While transformed, you do not need to breathe, gain access to the Ice Storm talent at level %d, gain %d%% resistance to cuts and stuns, gain %d%% cold resistance, and all cold damage heals you for %d%% of the damage done.
		The power will increase with your Spellpower.

		#AQUAMARINE#Ice storm:#LAST#
		%s
```
译文：
```text
你吸收周围的寒冰围绕你，将自己转变为纯粹的冰元素——西弗格罗斯，持续 %d 回合。
		转化成元素后，你不需要呼吸并获得等级 %d 的冰雪风暴，获得 %d%% 震慑和流血抵抗，%d%% 寒冷伤害抗性。所有寒冷伤害可对你产生治疗，治疗量基于伤害值的 %d%%。
		效果受法术强度加成。

		#AQUAMARINE#冰雪风暴：#LAST#
		%s
```

## entry-02284
位置：mod-tome.lua:29880；section：mod-tome/data/talents/spells/wildfire.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Burning Wake
```
译文：
```text
无尽之焰
```

## entry-02285
位置：mod-tome.lua:29881；section：mod-tome/data/talents/spells/wildfire.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your Flame, Flameshock, Fireflash and Blastwave spells leave a burning wake on the ground, burning all within for %0.2f fire damage for 4 turns.
		The damage will increase with your Spellpower.
```
译文：
```text
你的火焰、火焰冲击、爆裂火球和火焰新星都会在地上留下燃烧的火焰，每回合对范围内的所有单位造成 %0.2f 火焰伤害，持续 4 回合。
		伤害受法术强度加成。
```

## entry-02286
位置：mod-tome.lua:29903；section：mod-tome/data/talents/techniques/2h-assault.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning blow!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-02287
位置：mod-tome.lua:29911；section：mod-tome/data/talents/techniques/2h-assault.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Death Dance without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展死亡之舞！
```

## entry-02288
位置：mod-tome.lua:29928；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Death Dance without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展死亡之舞！
```

## entry-02289
位置：mod-tome.lua:29931；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Berserker without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展狂战士！
```

## entry-02290
位置：mod-tome.lua:29932；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You enter an aggressive battle stance, increasing Accuracy by %d and Physical Power by %d, at the cost of -10 Defense and -10 Armour.
		While berserking, you are nearly unstoppable, granting you %d%% stun and pinning resistance.
		The Accuracy bonus increases with your Dexterity, and the Physical Power bonus with your Strength.
```
译文：
```text
进入狂暴的战斗状态，以减少 10 点闪避和 10 点护甲的代价增加 %d 点命中和 %d 点物理强度。
		开启狂暴时你无人能挡，增加 %d%% 震慑和定身抵抗。
		命中受敏捷值加成；
		物理强度受力量值加成。
```

## entry-02291
位置：mod-tome.lua:29939；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ uses Warsqueak.
```
译文：
```text
@Source@发出吱吱的战吼。
```

## entry-02292
位置：mod-tome.lua:29940；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ uses Warshout.
```
译文：
```text
@Source@发出战吼。
```

## entry-02293
位置：mod-tome.lua:29941；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Warshout without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展战争怒吼！
```

## entry-02294
位置：mod-tome.lua:29944；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Death Blow without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展致命打击！
```

## entry-02295
位置：mod-tome.lua:29954；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Stunning Blow without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展震慑打击！
```

## entry-02296
位置：mod-tome.lua:29955；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning blow!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-02297
位置：mod-tome.lua:29960；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Sunder Armour without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展破甲！
```

## entry-02298
位置：mod-tome.lua:29961；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s shatters %s shield!
```
译文：
```text
#CRIMSON#%s粉碎了%s的护盾！
```

## entry-02299
位置：mod-tome.lua:29968；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Sunder Arms without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展破刃！
```

## entry-02300
位置：mod-tome.lua:29973；section：mod-tome/data/talents/techniques/2hweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Blood Frenzy without a two-handed weapon!
```
译文：
```text
你需要装备一把双手武器来施展血之狂暴！
```

## entry-02301
位置：mod-tome.lua:29982；section：mod-tome/data/talents/techniques/acrobatics.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot move!
```
译文：
```text
你无法移动！
```

## entry-02302
位置：mod-tome.lua:29985；section：mod-tome/data/talents/techniques/acrobatics.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# #YELLOW#vaults#LAST# over #target#!
```
译文：
```text
#Source##YELLOW#撑杆跳过#LAST# #target#！
```

## entry-02303
位置：mod-tome.lua:30008；section：mod-tome/data/talents/techniques/acrobatics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You gain greater facility with your acrobatic moves, lowering the cooldowns of Vault, Tumble, and Trained Reactions by %d, and their stamina costs by %0.1f.
		At Rank 3 you also gain 10%% global speed for 1 turn after Trained Reactions activates. At rank 5 this speed bonus improves to 20%% and lasts for 2 turns.
```
译文：
```text
你使用杂耍系技能更加得心应手，降低撑杆跳、翻滚和受训反应的冷却时间 %d 回合，降低技能的体力消耗 %0.1f。
		在等级 3 时，每当受训反应触发，你获得 10%% 的全局速度 1 回合。
		在等级 5 时，速度加成变为 20%%，持续 2 回合。
```

## entry-02304
位置：mod-tome.lua:30023；section：mod-tome/data/talents/techniques/agility.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the daze!
```
译文：
```text
%s抵抗了眩晕！
```

## entry-02305
位置：mod-tome.lua:30031；section：mod-tome/data/talents/techniques/agility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You rush toward your foe, readying your shot. If you reach the enemy, you release the shot, imbuing it with great power.
		The shot does %d%% weapon damage and knocks back your target by %d.
		The cooldown of this talent is reduced by 1 each time you move.
		This requires a sling to use.
```
译文：
```text
你冲向敌人，同时准备射击。当你接近敌人时，立刻射击，释放强大的威力。
		射击造成 %d%% 武器伤害并击退目标 %d 格。
		每次你移动时，该技能的冷却时间减少 1 回合。
		该技能需要投石索。
```

## entry-02306
位置：mod-tome.lua:30039；section：mod-tome/data/talents/techniques/agility.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Rapid Fire without a bow or sling!
```
译文：
```text
你需要一把弓或者投石索来施放这个技能！
```

## entry-02307
位置：mod-tome.lua:30040；section：mod-tome/data/talents/techniques/agility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enter a fluid, mobile shooting stance that excels at close combat. Your ranged attack speed is increased by %d%% and each time you shoot you gain %d%% increased movement speed for 2 turns.
Ranged attacks against targets will also grant you up to %d%% of a turn. This is 100%% effective against targets within 3 tiles, and decreases by 20%% for each tile beyond that (to 0%% at 8 tiles). This cannot occur more than once per turn.
Requires a sling to use.
```
译文：
```text
进入流畅灵活的射击姿势，擅长近距离射击。你的远程攻击速度增加 %d%%，每次射击令你在两回合内移动速度增加 %d%%。
命中敌人的远程攻击将给你带来最多 %d%% 额外回合，该效果对三格以内的目标有 100%% 效果，每增加 1 格距离，效果降低 20%%（8 格降为 0%%）。该效果每回合只能生效一次。
该技能需要投石索。
```

## 相关术语快照
```tsv
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Berserker	狂战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Death Dance	死亡之舞	T.GAME.TALENT	talents	talent name	existing	core	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fireflash	爆裂火球	T.GAME.TALENT	talents	talent name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Flameshock	火焰冲击	T.GAME.TALENT	talents	talent name	existing	core	
Frenzy	狂热	T.GAME.TALENT	talents	talent name	existing	global	
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Time Shield	时间盾	T.GAME.TALENT	talents	talent name	preferred	core	时空静止系技能及同名状态；统一技能说明与异常效果中的引用，并与 Temporal Shield“时光之盾”区分
Trained Reactions	受训反应	T.GAME.TALENT	talents	talent name	preferred	core	杂耍系防御持续技能；强调经过训练形成的反应能力，并统一两个技能定义及相关冷却、触发状态
Tumble	翻筋斗	T.GAME.TALENT	talents	talent name	existing	core	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
Warshout	战争怒吼	T.GAME.TALENT	talents	talent name	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
frenzy	狂乱	T.GAME.EFFECT	combat	effect subtype	existing	global	与技能名 Frenzy 的译法区分
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
shivgoroth	西弗格罗斯	T.GAME.ENTITY	creatures	entity name	preferred	core	寒冰元素生物专名；统一实体名、形态技能、状态说明与变形日志，不写作“西弗戈洛斯”
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
