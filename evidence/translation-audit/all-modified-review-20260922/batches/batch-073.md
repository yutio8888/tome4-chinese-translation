# batch-073：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02308
位置：mod-tome.lua:30050；section：mod-tome/data/talents/techniques/archery.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ shoots!
```
译文：
```text
@Source@射击！
```

## entry-02310
位置：mod-tome.lua:30064；section：mod-tome/data/talents/techniques/archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires a shot that explodes into a radius %d ball of razor sharp fragments on impact, dealing %d%% weapon damage and leaving targets crippled for %d turns, reducing their attack, spell and mind speed by %d%%.
		Each target struck has a %d%% chance to be marked.
		The status chance increases with your Accuracy.
```
译文：
```text
发射命中后爆裂成 %d 格半径球型范围碎片的弹药，造成 %d%% 武器伤害并致残目标 %d 回合，降低 %d%% 攻击、施法和精神速度。
		每个被击中的目标有 %d%% 几率被标记。
		致残几率受命中加成。
```

## entry-02311
位置：mod-tome.lua:30070；section：mod-tome/data/talents/techniques/archery.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the scattershot!
```
译文：
```text
%s抵抗了分散射击！
```

## entry-02312
位置：mod-tome.lua:30077；section：mod-tome/data/talents/techniques/archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire a precise shot dealing %d%% weapon damage, with 100 increased accuracy. This shot will bypass other enemies between you and your target.
Only usable against marked targets, and consumes the mark on hit.
```
译文：
```text
瞄准目标头部发射穿透性弹药，造成 %d%% 武器伤害。
此次攻击额外获得 100 命中，且能穿透目标以外单位。
只能对被标记的单位使用，命中时消耗该标记。
```

## entry-02313
位置：mod-tome.lua:30082；section：mod-tome/data/talents/techniques/archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire countless shots into the sky to rain down around your target, inflicting %d%% weapon damage to all within radius %d.
If the primary target is marked, you consume the mark to fire a second volley of arrows for %d%% damage at no ammo cost.
```
译文：
```text
你向天空发射无数弹药，如箭雨般落向目标，造成 %d%% 武器伤害，杀伤半径 %d 格。
如果中心目标被标记，你将消耗其标记，不消耗弹药发射额外齐射一轮，造成 %d%% 伤害。
```

## entry-02314
位置：mod-tome.lua:30087；section：mod-tome/data/talents/techniques/archery.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the disarm!
```
译文：
```text
%s抵抗了缴械！
```

## entry-02315
位置：mod-tome.lua:30088；section：mod-tome/data/talents/techniques/archery.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the slow!
```
译文：
```text
%s抵抗了减速！
```

## entry-02316
位置：mod-tome.lua:30089；section：mod-tome/data/talents/techniques/archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a disabling shot at a target's throat (or equivalent), dealing %d%% weapon damage and silencing them for %d turns.
If the target is marked, you consume the mark to fire two secondary shots at their arms and legs (or other appendages) dealing %d%% damage, reducing their movement speed by 50%% and disarming them for the duration.
The status chance increases with your Accuracy.
```
译文：
```text
你朝目标的喉咙（或者类似部位）射击，造成 %d%% 武器伤害并沉默 %d 回合。
如果目标被标记，则消耗标记并额外向目标的手臂与腿（或者类似附肢）射击两次，造成 %d%% 伤害，并在相同的持续时间内降低其 50%% 移动速度并将其缴械。
状态效果几率受命中加成。
```

## entry-02317
位置：mod-tome.lua:30095；section：mod-tome/data/talents/techniques/archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you consume a mark, you gain %d%% increased attack speed for 2 turns and the cooldown of %d random techniques are reduced by %d turns.
```
译文：
```text
每次消耗标记时，获得 %d%% 攻击速度加成，持续 2 回合，并随机减少 %d 个战斗技巧系技能的冷却时间 %d 回合。
```

## entry-02318
位置：mod-tome.lua:30106；section：mod-tome/data/talents/techniques/archery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a pinning shot, doing %d%% damage and pinning your target to the ground for %d turns.
		The pinning chance increases with your Dexterity.
```
译文：
```text
你射出定身一箭，造成 %d%% 伤害，并定身目标 %d 回合。
		定身几率受敏捷加成。
```

## entry-02319
位置：mod-tome.lua:30115；section：mod-tome/data/talents/techniques/assassination.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Coup de Grace without dual wielding!
```
译文：
```text
你需要双持武器来施展这个技能！
```

## entry-02320
位置：mod-tome.lua:30116；section：mod-tome/data/talents/techniques/assassination.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# delivers a Coup de Grace against #Target#!
```
译文：
```text
#Source#对#Target#发起致命一击！
```

## entry-02321
位置：mod-tome.lua:30119；section：mod-tome/data/talents/techniques/assassination.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Attempt to finish off a wounded enemy, striking them with both weapons for %d%% increased by 50%% if their life is below 30%%.  A target brought below 20%% of its maximum life must make a physical save against your Accuracy or be instantly slain.
		You may take advantage of finishing your foe this way to activate stealth (if known).
```
译文：
```text
尝试终结一名受伤的敌人，用双持武器攻击对方，造成 %d%% 武器伤害，如果对方的生命值在30%% 以下，伤害还会增加50%%。20%% 生命以下的目标将用物理豁免对抗你的命中，若未通过则会被立刻秒杀。
		如果该技能杀死敌人，且你学会了潜行技能，你将进入潜行状态。
```

## entry-02322
位置：mod-tome.lua:30129；section：mod-tome/data/talents/techniques/assassination.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Target# avoids a garrote from #Source#!
```
译文：
```text
#Target#避免了被#Source#勒住喉咙！
```

## entry-02323
位置：mod-tome.lua:30160；section：mod-tome/data/talents/techniques/battle-tactics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lashes at the target, doing %d%% weapon damage.
		If the attack hits, the target will bleed for %d%% weapon damage over 7 turns, and all healing will be reduced by %d%%.
```
译文：
```text
割裂目标并造成 %d%% 武器伤害。
		如果攻击命中目标，则目标会持续流血 7 回合，
		造成总计 %d%% 武器伤害。在此过程中，任何对目标的治疗效果减少 %d%%。
```

## entry-02324
位置：mod-tome.lua:30165；section：mod-tome/data/talents/techniques/battle-tactics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Take a defensive stance to resist the onslaught of your foes.
		While wounded, you gain all damage resistance equal to %d%% of your missing health.
		(So if you have lost 70%% of your life, you gain %d%% all resistance.)
		In addition, your all damage resistance cap increases %0.1f%% closer to 100%%.
		This consumes stamina rapidly the longer it is sustained (%0.1f stamina/turn, increasing by 0.3/turn).
		The resist is recalculated each time you take damage.
```
译文：
```text
采取一个防守姿态并抵抗敌人的猛攻。
		当你受伤后，你获得相当于 %d%% 损失生命值百分比的全体伤害抗性。
		例如：当你损失 70%% 生命时获得 %d%% 抗性。
		同时，你的全体伤害抗性上限与 100%% 的差距缩小 %0.1f%%。
		该技能消耗体力迅速，体力值基础消耗 %0.1f，每回合增加 0.3。
		每次受到伤害时都会重新计算抗性。
```

## entry-02325
位置：mod-tome.lua:30189；section：mod-tome/data/talents/techniques/bloodthirst.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Delight in spilling the blood of your foes.  After scoring a critical hit, your maximum hit points will be increased by %d%%, your life regeneration by %0.2f per turn, and your stamina regeneration by %0.2f per turn for %d turns.
		The life and stamina regeneration will stack up to five times, for a maximum of %0.2f and %0.2f each turn, respectively.
```
译文：
```text
沐浴着敌人的鲜血令你感到兴奋。
		在成功打出一次暴击后，会增加你 %d%% 的最大生命值、%0.2f 每回合生命回复点数和 %0.2f 每回合体力回复点数持续 %d 回合。
		生命与体力回复可以叠加 5 次直至 %0.2f 生命和 %0.2f 体力回复/回合。
```

## entry-02326
位置：mod-tome.lua:30194；section：mod-tome/data/talents/techniques/bloodthirst.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You delight in the inflicting of wounds, providing %d physical power.
		In addition when you make a creature bleed its physical damage resistance is reduced by %d%% (but never below 0%%).
		Physical power depends on your Strength stat.
```
译文：
```text
你沉醉于撕裂伤口的兴奋中，增加 %d 物理强度。
		同时，每次你让敌人流血时，它的物理抗性下降 %d%% （但不会小于 0%%）
		物理强度加成受力量影响。
```

## entry-02327
位置：mod-tome.lua:30200；section：mod-tome/data/talents/techniques/bloodthirst.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You enter a battle frenzy for %d turns. During that time, you can not use items, healing has no effect, and your health cannot drop below 1.
		At the end of the frenzy, you regain %d%% of your health per foe slain during the frenzy.
		While Unstoppable is active, Berserker Rage critical bonus is disabled as you lose the thrill of the risk of death.
```
译文：
```text
你进入疯狂战斗状态 %d 回合。
		在这段时间内你不能使用物品，并且治疗无效，此时你的生命值无法低于 1 点。
		状态期间你每杀死一个敌人，都会在状态结束时回复 %d%% 最大生命值。
		当进入无双状态时，由于你失去了死亡的威胁，狂战之怒不能提供暴击加成。
```

## entry-02328
位置：mod-tome.lua:30241；section：mod-tome/data/talents/techniques/buckler-training.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 At talent level 5, your Bash and Smash shield hits are guaranteed criticals.
```
译文：
```text
技能等级 5 时，你的击退射击的盾击必定暴击。
```

## entry-02329
位置：mod-tome.lua:30242；section：mod-tome/data/talents/techniques/buckler-training.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 At talent level 5, your Bash and Smash shield hit is a guaranteed critical.
```
译文：
```text
技能等级 5 时，你的击退射击的盾击必定暴击。
```

## entry-02330
位置：mod-tome.lua:30245；section：mod-tome/data/talents/techniques/buckler-training.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#ORCHID##Source# follows up with a countershot.#LAST#
```
译文：
```text
#ORCHID##Source#追加了一次反击射击。#LAST#
```

## entry-02331
位置：mod-tome.lua:30254；section：mod-tome/data/talents/techniques/combat-techniques.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ rushes out!
```
译文：
```text
@Source@冲了出去！
```

## entry-02332
位置：mod-tome.lua:30270；section：mod-tome/data/talents/techniques/combat-techniques.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your combat focus allows you to regenerate stamina faster (+%0.1f stamina/turn).
```
译文：
```text
你专注于战斗，使得你可以更快的回复体力（+%0.1f 体力/回合）。
```

## entry-02333
位置：mod-tome.lua:30272；section：mod-tome/data/talents/techniques/combat-techniques.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your combat focus allows you to regenerate life faster (+%0.1f life/turn).
```
译文：
```text
你专注于战斗，使你可以更快的回复生命值（+%0.1f 生命值/回合）。
```

## entry-02334
位置：mod-tome.lua:30274；section：mod-tome/data/talents/techniques/combat-techniques.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Rigorous training allows you to be more resistant to some spell effects (+%d spell save).
```
译文：
```text
严格的训练使得你对某些法术效果具有更高的抗性（+%d 法术豁免）。
```

## entry-02335
位置：mod-tome.lua:30286；section：mod-tome/data/talents/techniques/combat-training.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(Note that brawlers will be unable to perform many of their talents in massive armour.)
```
译文：
```text
（请注意，格斗家在身穿板甲的时候，无法使用大部分技能。）
```

## entry-02336
位置：mod-tome.lua:30287；section：mod-tome/data/talents/techniques/combat-training.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(Note that wearing mail or plate armour will interfere with stealth.)
```
译文：
```text
（请注意，身穿重甲或板甲的时候不可以潜行。）
```

## entry-02337
位置：mod-tome.lua:30288；section：mod-tome/data/talents/techniques/combat-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You become better at using your armour to deflect blows and protect your vital areas. Increases Armour value by %d, Armour hardiness by %d%%, and reduces the chance melee or ranged attacks critically hit you by %d%% with your current body armour.
		(This talent only provides bonuses for heavy mail or massive plate armour.)
		At level 1, it allows you to wear heavy mail armour, gauntlets, helms, and heavy boots.
		At level 2, it allows you to wear shields.
		At level 3, it allows you to wear massive plate armour.
		%s
```
译文：
```text
你使用防具来偏转攻击和保护重要部位的能力加强了。
		根据现有防具，提高 %d 护甲值和 %d%% 护甲强度，并减少 %d%% 近战和远程攻击的暴击几率。
		（这项技能只对重甲或板甲提供加成。）
		在等级 1 时，能使你装备锁甲、金属手套、头盔和重靴。
		在等级 2 时，能使你装备盾牌。
		在等级 3 时，能使你装备板甲。
		%s
```

## entry-02338
位置：mod-tome.lua:30301；section：mod-tome/data/talents/techniques/combat-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You learn to maintain your agility and manage your combat posture while wearing robes or light armour.  When wearing armour no heavier than leather in your main body slot, you gain %d Defense, %d%% Armour hardiness, and %d%% reduced Fatigue.
		In addition, when you step adjacent to a (visible) enemy, you use the juxtaposition to increase your total Defense by %d for 2 turns.
		The Defense bonus scales with your Dexterity.
```
译文：
```text
你学会在身着轻甲和布甲时保持敏捷，获得 %d 闪避，%d%% 护甲强度，减少 %d%% 疲劳。
		此外，每当你进入和（可见的）敌人相邻的位置时，你获得 %d 闪避，持续 2 回合。
		闪避受敏捷加成。
```

## entry-02339
位置：mod-tome.lua:30313；section：mod-tome/data/talents/techniques/combat-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases weapon damage by %d%% and physical power by 30 when using exotic weapons.
```
译文：
```text
使用特殊武器时，增加 %d%% 武器伤害，增加 30 物理强度。
```

## entry-02340
位置：mod-tome.lua:30319；section：mod-tome/data/talents/techniques/conditioning.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You recover faster from poisons, diseases and wounds, reducing the duration of all such effects by %d%%.  
			Whenever your life falls below 50%%, your life regeneration increases by %0.1f for %d turns (%d total). This effect can only happen once every %d turns.
		The regeneration scales with your Constitution.
```
译文：
```text
你受中毒、疾病和创伤的影响较小，减少 %d%% 此类效果的持续时间。
		此外在生命值低于 50%% 时，你的生命回复将会增加 %0.1f，持续 %d 回合，共回复 %d 生命值，但每隔 %d 回合才能触发一次。
		生命回复受体质值加成。
```

## entry-02341
位置：mod-tome.lua:30325；section：mod-tome/data/talents/techniques/conditioning.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#ORCHID#%s has recovered!#LAST#
```
译文：
```text
#ORCHID#%s恢复了！#LAST#
```

## entry-02342
位置：mod-tome.lua:30344；section：mod-tome/data/talents/techniques/conditioning.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You release a surge of adrenaline that increases your Physical Power by %d for %d turns. While the effect is active, you may continue to fight beyond the point of exhaustion.
		You may continue to use stamina based talents while at zero stamina at the cost of life.
		The Physical Power increase will scale with your Constitution.
		Using this talent does not take a turn.
```
译文：
```text
你激活肾上腺素来增加 %d 物理强度持续 %d 回合。
		此技能激活时，你可以不知疲倦地战斗，若体力为 0，可继续使用消耗体力的技能，代价为消耗生命。
		物理强度受体质值加成。
		使用本技能不会消耗额外回合。
```

## entry-02343
位置：mod-tome.lua:30369；section：mod-tome/data/talents/techniques/dualweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must dual wield to manage contact with your target!
```
译文：
```text
你只有在双持状态下才能使用这个技能！
```

## entry-02344
位置：mod-tome.lua:30377；section：mod-tome/data/talents/techniques/dualweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must dual wield to perform an Offhand Jab!
```
译文：
```text
你只有在双持状态下才能使用这个技能！
```

## entry-02345
位置：mod-tome.lua:30379；section：mod-tome/data/talents/techniques/dualweapon.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
With a quick shift of your momentum, you execute a surprise unarmed strike in place of your normal offhand attack.
		This allows you to attack with your mainhand weapon for %d%% damage and unarmed for %d%% damage.  If the unarmed attack hits, the target is confused (%d%% power) for %d turns.
		The chance to confuse increases with your Accuracy.
```
译文：
```text
你迅速移动，用徒手攻击敌人。
		造成 %d%% 主手武器伤害，%d%% 徒手伤害。
		若徒手攻击命中，敌人将被混乱（%d%% 强度）%d 回合。
		混乱几率受命中加成。
```

## entry-02346
位置：mod-tome.lua:30386；section：mod-tome/data/talents/techniques/dualweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Dual Strike without dual wielding!
```
译文：
```text
你只有在双持状态下才能使用这个技能！
```

## entry-02347
位置：mod-tome.lua:30393；section：mod-tome/data/talents/techniques/dualweapon.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Flurry without dual wielding!
```
译文：
```text
你只有在双持状态下才能使用这个技能！
```

## entry-02348
位置：mod-tome.lua:30407；section：mod-tome/data/talents/techniques/duelist.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your offhand weapon damage penalty is reduced to %d%%.
		Up to %0.1f times a turn, you have a %d%% chance to parry up to %d damage (based on your offhand weapon damage) from a melee or ranged attack.  The number of parries increases with your Cunning.  (A fractional parry has a reduced chance to succeed.)
		A successful parry reduces damage like armour (before any attack multipliers) and prevents critical strikes.  It is difficult to parry attacks from unseen attackers and you cannot parry with a mindstar.
```
译文：
```text
你的副手武器伤害惩罚降低至 %d%%。
		每回合至多 %0.1f 次，你有 %d%% 几率抵挡一次近战或远程攻击的至多 %d 点伤害（基于副手武器伤害）。抵挡次数随灵巧提高；若次数为小数，小数部分对应的抵挡成功率会降低。
		成功抵挡会像护甲一样在攻击倍率生效前减免伤害，并阻止这次攻击暴击。来自未发现攻击者的攻击很难抵挡，且你无法使用灵晶抵挡。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Berserker	狂战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Brawler	格斗家	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Frenzy	狂热	T.GAME.TALENT	talents	talent name	existing	global	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
frenzy	狂乱	T.GAME.EFFECT	combat	effect subtype	existing	global	与技能名 Frenzy 的译法区分
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mainhand	主手	T.GAME.ENTITY	items	nil	existing	core	
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
offhand	副手	T.GAME.ENTITY	items	nil	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
