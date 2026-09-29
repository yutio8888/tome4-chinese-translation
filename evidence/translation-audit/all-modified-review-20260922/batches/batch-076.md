# batch-076：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02429
位置：mod-tome.lua:30978；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Physical conditioning.
```
译文：
```text
强化你的体质。
```

## entry-02430
位置：mod-tome.lua:30980；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Base martial arts attack and stances.
```
译文：
```text
基础武学和姿态。
```

## entry-02432
位置：mod-tome.lua:30986；section：mod-tome/data/talents/techniques/techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your ammo is incompatible with your missile launcher.
```
译文：
```text
你的弹药与你的远程发射武器不匹配。
```

## entry-02433
位置：mod-tome.lua:31025；section：mod-tome/data/talents/techniques/throwing-knives.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You keep a special stash of %d throwing knives in your bandolier, which you can throw all at once at enemies within a radius %d cone, for %d%% damage each.
		Each target can be hit up to 5 times, if the number of knives exceeds the number of enemies.  Creatures block knives from hitting targets behind them.
```
译文：
```text
额外存储 %d 把飞刀，可以一次性扔出，每把飞刀对 %d 格锥形范围内的敌人造成 %d%% 伤害。
		如果飞刀数量多于敌人，每个目标最多被同时击中 5 次。飞刀无法穿透生物。
```

## entry-02434
位置：mod-tome.lua:31029；section：mod-tome/data/talents/techniques/throwing-knives.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are able to target your throwing knives with pinpoint accuracy, increasing their critical strike chance by %d%% and critical strike damage by %d%%. 
In addition, your critical strikes with throwing knives have a %d%% chance to randomly disable your target, possibly disarming, silencing or pinning them for 2 turns.
```
译文：
```text
精准地投掷飞刀，增加 %d%% 暴击几率、%d%% 暴击伤害。
此外，飞刀暴击时还有 %d%% 几率缴械沉默或者定身敌人持续 2 回合。
```

## entry-02435
位置：mod-tome.lua:31034；section：mod-tome/data/talents/techniques/throwing-knives.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You can throw knives with lightning speed, increasing your attack speed with them by %d%% and giving you a %d%% chance when striking a target in melee to throw a knife at a random foe within 7 tiles for 100%% damage. 
		This bonus attack can only trigger once per turn, and does not trigger from throwing knife attacks.
```
译文：
```text
你可以闪电般地投掷你的飞刀。增加 %d%% 攻击速度，近战攻击时有 %d%% 几率投掷一把飞刀随机对 7 格范围内的一名敌人造成 100%% 伤害。
		每回合仅触发 1 次，不会被投掷飞刀触发。
```

## entry-02436
位置：mod-tome.lua:31039；section：mod-tome/data/talents/techniques/throwing-knives.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a knife coated with venom, doing %d%% damage as nature and inflicting additional effects based on your active vile poisons (as per the Venomous Strike talent):
		
		%s
		Using this talent puts your Venomous Strike talent on cooldown.
```
译文：
```text
投掷一把剧毒飞刀，造成 %d%% 自然伤害并根据你当前生效的邪恶毒素附加额外效果（和毒素爆发相同）:

		%s
		使用这技能将使毒素爆发进入冷却。
```

## entry-02437
位置：mod-tome.lua:31052；section：mod-tome/data/talents/techniques/thuggery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You smack your forehead against your enemy's head (or whatever sensitive part you can find), causing %0.1f Physical damage.
		If the attack hits, the target is confused (%d%% effect) for %d turns.
		Damage done increases with the quality of your headgear, your Strength, and your physical damage bonuses.
		Confusion power increases with your Dexterity, and chance increases with Accuracy.
```
译文：
```text
你用前额猛击敌人头部（或者任意你能找到的有效位置），造成 %0.1f 物理伤害。
		如果此次攻击命中，则目标会混乱(%d%% 强度) %d 回合。
		伤害受头盔品质、力量和物理伤害加成。
		混乱强度受敏捷加成，几率受命中加成。
```

## entry-02438
位置：mod-tome.lua:31064；section：mod-tome/data/talents/techniques/thuggery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You go all out, trying to burn down your foes as fast as possible.
		You gain +%d%% attack speed, +%d%% critical chance and +%d%% physical resistance penetration, but this talent drains 6 stamina each turn.
		This effect is disabled automatically on rest or run.
		
```
译文：
```text
你疯狂地杀戮，试图尽快击倒你的敌人。
		增加 %d%% 攻击速度，%d%% 暴击率和 %d%% 物理抗性穿透，每回合消耗 6 点体力。
		该效果在休息或者奔跑时自动解除。
		
```

## entry-02439
位置：mod-tome.lua:31076；section：mod-tome/data/talents/techniques/tireless-combatant.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Any time you do not have an opponent in a square adjacent to you, you gain %0.1f Stamina regeneration. At talent level 3 or more, you also gain an equal amount of life regen when Breathing Room is active.
```
译文：
```text
当没有敌人与你相邻的时候，你获得 %0.1f 体力回复。技能等级 3 及以后，这个技能带给你等量的生命回复。
```

## entry-02440
位置：mod-tome.lua:31097；section：mod-tome/data/talents/techniques/unarmed-discipline.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Unleash a flurry of disruptive kicks at your target's vulnerable areas. For each combo point you attack for %d%% weapon damage and deactivate one physical sustain.
			At talent level 3 #DARK_ORCHID#Magical#LAST# sustains will also be effected.
			At talent level 5 #YELLOW#Mental#LAST# sustains will also be effected.
			Using this talent removes your combo points.
```
译文：
```text
对目标的要害部位释放一连串破坏性踢击。每有一个连击点，对目标造成 %d%% 武器伤害，并解除目标一项物理持续技能。
		等级 3 时，#DARK_ORCHID#魔法#LAST#持续技能也会受影响。
		等级 5 时，#YELLOW#精神#LAST#持续技能也会受影响。
		使用该技能将除去全部连击点。
```

## entry-02441
位置：mod-tome.lua:31108；section：mod-tome/data/talents/techniques/unarmed-discipline.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Toughen your body blocking up to %d damage per combo point (Max %d) across 2 turns.
			Current block value: %d
			Using this talent removes your combo points.
			The damage absorbed scales with your Physical Power.
```
译文：
```text
硬化身体，每有一点连击点就能格挡 %d 点伤害（至多 %d），持续 2 回合。
			当前格挡值：%d
			使用该技能会除去所有连击点。
			伤害吸收受物理强度加成。
```

## entry-02442
位置：mod-tome.lua:31117；section：mod-tome/data/talents/techniques/unarmed-discipline.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# strikes at a vital spot on #target#!
```
译文：
```text
#Source#攻向#target#的要害！
```

## entry-02443
位置：mod-tome.lua:31118；section：mod-tome/data/talents/techniques/unarmed-discipline.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using your deep knowledge of anatomy, you strike a target in a vital pressure point for %d%% weapon damage, bypassing their defense and evasion.
		This strike inflicts terrible wounds inside the target's body, causing them to take physical damage equal to 100%% of any damage dealt during the attack each turn for 4 turns, increasing by %d%% each turn (so after 4 turns, they would have taken a total of %d%% damage).
		If the target dies while under or from this effect their body will explode in a radius %d shower of bone and gore, inflicting physical damage equal to the current tick to all enemies and granting you 4 combo points.
```
译文：
```text
使用你深刻的解剖学知识，击中敌人的穴道造成 %d%% 武器伤害，无视闪避和躲闪效果。
		这次攻击在敌人身上造成可怕的内伤，在之后的 4 回合内，每回合都造成相当于本次攻击所造成伤害 100%% 的物理伤害，且每回合递增 %d%%（因此 4 回合后共计造成 %d%% 伤害）。
		如果目标死在该效果下，他们身体会爆炸，并让半径 %d 内的敌人受到等于他们当前回合的点穴伤害的物理伤害，并给你 4 点连击点。
```

## entry-02444
位置：mod-tome.lua:31127；section：mod-tome/data/talents/techniques/unarmed-training.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Empty Hand
```
译文：
```text
赤手空拳
```

## entry-02445
位置：mod-tome.lua:31128；section：mod-tome/data/talents/techniques/unarmed-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Grants %d Physical Power when fighting unarmed (or with gloves or gauntlets).
		This talent's effects will scale with your level.
```
译文：
```text
当你徒手或仅装备手套和臂铠时提高 %d 物理强度。
		效果受角色等级加成。
```

## entry-02446
位置：mod-tome.lua:31132；section：mod-tome/data/talents/techniques/unarmed-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases all unarmed damage by %d%% and physical power by 30 (including grapples and kicks).
		Note that brawlers naturally gain 0.5 Physical Power per character level while unarmed (current brawler physical power bonus: %0.1f) and attack 20%% faster while unarmed.
```
译文：
```text
增加 %d%% 所有徒手伤害，并提高 30 物理强度（包括抓取与踢击）。
		注意：格斗家徒手时天生随角色每级获得 0.5 物理强度（当前物理强度加成：%0.1f），且徒手时攻击速度提高 20%%。
```

## entry-02447
位置：mod-tome.lua:31136；section：mod-tome/data/talents/techniques/unarmed-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mastery of unarmed combat unifies your body. Increases your Strength by %d based on Cunning and your Constitution by %d based on Dexterity.
```
译文：
```text
你对徒手格斗的掌握强化了你的身体，增加 %d 力量（基于灵巧），%d 体质（基于敏捷）。
```

## entry-02448
位置：mod-tome.lua:31147；section：mod-tome/data/talents/techniques/warcries.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# shatters '#Target#'.
```
译文：
```text
#Source#击碎了'#Target#'。
```

## entry-02449
位置：mod-tome.lua:31188；section：mod-tome/data/talents/techniques/weaponshield.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hit your target with your shield 3 times for %d%% damage then quickly return to a blocking position.  The bonus block will not check or trigger Block cooldown.
```
译文：
```text
用盾牌拍击目标 3 次，造成 %d%% 盾牌伤害，然后迅速进入格挡状态。
		这次额外格挡既不检查也不触发格挡技能的冷却（冷却中仍可获得）。
```

## entry-02450
位置：mod-tome.lua:31191；section：mod-tome/data/talents/techniques/weaponshield.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Assault without a mainhand weapon and shield!
```
译文：
```text
没有主手武器和盾牌，无法使用强袭！
```

## entry-02451
位置：mod-tome.lua:31195；section：mod-tome/data/talents/techniques/weaponshield.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enter a protective battle stance allowing you to defend yourself more proficiently while using a shield.
		Increases Armour by %d, Block value by %d, and reduces Block cooldown by 2.
		Increases stun and knockback resistance by %d%%.
		The Armor and Block bonuses increase equally with your Dexterity and Strength.
```
译文：
```text
进入一个保护性的战斗姿态，让你在使用盾牌的同时更熟练地保护自己。
		提升护甲值 %d，格挡值 %d，减少格挡冷却 2 回合。
		提升眩晕和击退抗性 %d%%。
		护甲和格挡值加成受你的敏捷和力量值影响。
```

## entry-02452
位置：mod-tome.lua:31202；section：mod-tome/data/talents/techniques/weaponshield.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Repulsion
```
译文：
```text
盾牌排斥
```

## entry-02453
位置：mod-tome.lua:31214；section：mod-tome/data/talents/techniques/weaponshield.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Improves your damage with shield-based skills, and increases your Spell (+%d) and Physical (+%d) Saves.
```
译文：
```text
提高你使用盾牌系技能时造成的伤害，并提高法术豁免（+%d）和物理豁免（+%d）。
```

## entry-02454
位置：mod-tome.lua:31246；section：mod-tome/data/talents/uber/const.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You know how to protect yourself with the deepest shadows. As long as you stand on an unlit tile you gain %d armour, 50%% armour hardiness, and 20%% evasion.
		Any time you deal darkness damage, you will unlight both the target tile and yours.
		Passively increases your stealth rating by %d.
		The armor bonus scales with your Constitution.
```
译文：
```text
你懂得如何融入阴影，当你站在黑暗地形上时将增加 %d 点护甲、50%%护甲强度和 20%% 躲闪概率。
		同时，你造成的暗影伤害会使你当前所在区域和目标区域陷入黑暗。
		被动增加 %d 潜行强度。
		受体质影响，护甲加值有额外加成。
```

## entry-02455
位置：mod-tome.lua:31257；section：mod-tome/data/talents/uber/const.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fungal spores have colonized your blood, so that each time you use an infusion you store %d fungal power.
		You may use this prodigy to release the power as a heal (never more than %d life) and remove up to 10 detrimental magical effects.
		Fungal power lasts for up to 6 turns, losing the greater of 10 potency or 10%% of its power each turn.
		The amount of fungal power produced and the maximum heal possible increase with your Constitution and maximum life.
```
译文：
```text
真菌充斥在你的血液中，每当使用纹身时你都会储存 %d 的真菌能量。
		当使用此技能时，可释放能量治愈伤口 (恢复值不超过 %d), 并解除至多 10 个负面魔法效果。
		真菌之力最多保存 6 回合，每回合减少 10 点或当前真菌之力的 10%%，取较大者。
		真菌能量的产生量和治疗上限随你的体质和最大生命值提高。
```

## entry-02456
位置：mod-tome.lua:31266；section：mod-tome/data/talents/uber/const.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Thanks to your newfound knowledge of corruption, you've learned some tricks for toughening your body... but only if you are healthy enough to withstand the strain from the changes.
		Improves your life by 500, your defense by %d, your armour by %d, your armour hardiness by 20%% and your saves by %d as your natural toughness and reflexes are pushed beyond their normal limits.
		Your saves armour and defense will improve with your Constitution.
```
译文：
```text
多亏了你在枯萎能量上的新发现，你学到一些方法来增强你的体质。但是只有当你有一副强壮的体魄时方能承受这剧烈的变化。
		增加你 500 点生命上限，%d 点闪避，%d 护甲值，20%% 护甲强度，%d 所有豁免，你天生的韧性和反应能力突破了自然极限。
		豁免、护甲和闪避受体质值加成。
```

## entry-02457
位置：mod-tome.lua:31276；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#%s slows from critical velocity!
```
译文：
```text
#LIGHT_BLUE#%s 从临界速度减慢！
```

## entry-02458
位置：mod-tome.lua:31277；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#%s reaches critical velocity!
```
译文：
```text
#LIGHT_BLUE#%s 达到了临界速度！
```

## entry-02459
位置：mod-tome.lua:31290；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You unleash a blast of #LIGHT_STEEL_BLUE#temporal#LAST# energy!
```
译文：
```text
你释放出#LIGHT_STEEL_BLUE#时空#LAST#能量的爆炸！
```

## entry-02460
位置：mod-tome.lua:31291；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You unleash a blast of #DARK_GREEN#virulent blight!#LAST#!
```
译文：
```text
你释放出 #DARK_GREEN#枯萎疾病#LAST#爆炸！
```

## entry-02461
位置：mod-tome.lua:31292；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You unleash a blast of #GREEN#acid#LAST#!
```
译文：
```text
你释放出#GREEN#酸液#LAST#爆炸！
```

## entry-02462
位置：mod-tome.lua:31293；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You unleash a blast of numbing #GREY#darkness#LAST#!
```
译文：
```text
你释放出麻痹#GREY#暗影#LAST#爆炸！
```

## entry-02463
位置：mod-tome.lua:31294；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You unleash a confusing blast of #YELLOW#mental#LAST# energy!
```
译文：
```text
你释放出#YELLOW#精神#LAST#混乱爆炸！
```

## entry-02464
位置：mod-tome.lua:31295；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You unleash a crippling blast of earthen energy!
```
译文：
```text
你释放出大地致残爆炸！
```

## entry-02465
位置：mod-tome.lua:31296；section：mod-tome/data/talents/uber/cun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(Cooldowns)
```
译文：
```text
（冷却时间）
```

## entry-02466
位置：mod-tome.lua:31322；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#VIOLET#%s assembles %s!
```
译文：
```text
#VIOLET#%s 重组为 %s！
```

## entry-02467
位置：mod-tome.lua:31326；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with earthen power!
```
译文：
```text
%s涌起大地能量的狂潮！
```

## entry-02468
位置：mod-tome.lua:31327；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with #PURPLE#arcane#LAST# power!
```
译文：
```text
%s涌起#PURPLE#奥术#LAST#能量的狂潮！
```

## entry-02469
位置：mod-tome.lua:31328；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with #LIGHT_RED#fiery#LAST# power!
```
译文：
```text
%s涌起#LIGHT_RED#火焰#LAST#能量的狂潮！
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Brawler	格斗家	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corruption	堕落	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
knockback	击退	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Knockback Resistance；战斗日志“%s抵抗了击退！”
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mainhand	主手	T.GAME.ENTITY	items	nil	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
throwing knives	飞刀	T.GAME.ENTITY	items	talent type	preferred	core	灵巧系远程投掷武器类别；在技能说明中与普通匕首 knives 并列
throwing knives	飞刀	T.GAME.ENTITY	items	tformat	preferred	core	技能机制说明中的投掷匕首；沿用飞刀类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
