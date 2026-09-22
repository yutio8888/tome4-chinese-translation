# batch-066：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02028
位置：mod-tome.lua:26499；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time one of your foes bites the dust, you feel a surge of power, increasing your strength by 2 (stacking up to a maximum of %d) for %d turns.
```
译文：
```text
每当你让一个敌人扑街，你会漏出一股汹涌的霸气，增加你 2 点力量，上限 %d，持续 %d 回合。
```

## entry-02029
位置：mod-tome.lua:26514；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You expend massive amounts of energy to launch yourself across %d squares at incredible speed. All enemies in your path will be knocked flying and dealt between %d and %d Physical damage.
		At talent level 5, you can batter through solid walls.
```
译文：
```text
消耗大量能量，以惊人的速度冲锋 %d 格。路径上的所有敌人会被击飞并受到 %d 至 %d 点物理伤害。
		技能等级 5 时你能冲过墙壁。
```

## entry-02030
位置：mod-tome.lua:26530；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Quickly reload your ammo by %d (depends on masteries and object bonuses).
		Doing so requires no turn but you are considered disarmed for 2 turns.

		Reloading does not break stealth.
```
译文：
```text
立刻装填 %d 弹药（数量取决于专精与装备加成）。
		此举不消耗回合，但你在 2 回合内被视为缴械。

		装填弹药不会打破潜行。
```

## entry-02031
位置：mod-tome.lua:26537；section：mod-tome/data/talents/misc/npcs.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Sweep
```
译文：
```text
横扫
```

## entry-02032
位置：mod-tome.lua:26539；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Sweep without dual wielding!
```
译文：
```text
你只有在双持状态下才能使用这个技能！
```

## entry-02033
位置：mod-tome.lua:26556；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throws a vial of sticky smoke that explodes in radius %d on your foes, reducing their vision range by %d for 5 turns.
		Creatures affected by smoke bomb can never prevent you from stealthing, even if their proximity would normally forbid it.
		Use of this will not break stealth.
```
译文：
```text
向你的敌人投掷一小瓶在半径 %d 码范围内爆炸的粘性烟雾，使他们的视野范围减少 %d，持续5回合。
		受烟雾弹影响的生物永远不会阻止你潜行，即使通常情况下接近它们会导致无法潜行。
		使用这个技能不会打破潜行。
```

## entry-02034
位置：mod-tome.lua:26562；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
Terrain prevents #Source# from switching places with #Target#.
```
译文：
```text
地形阻止了#Source#与#Target#的换位。
```

## entry-02035
位置：mod-tome.lua:26563；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using a series of tricks and maneuvers, you switch places with your target.
		Switching places will confuse your foes, granting you Evasion (50%%) for %d turns.
		While switching places, your weapon(s) will connect with the target; this will not do weapon damage, but on hit effects of the weapons can trigger.
```
译文：
```text
通过一系列的技巧和动作，你可以和你的目标交换位置。
		这个换位动作会迷惑你的敌人，让你获得持续 %d 回合的 50%% 概率躲闪效果。
		切换位置时，你的武器将会击中目标；这不会造成武器伤害，但武器的命中特效可能会触发。
```

## entry-02036
位置：mod-tome.lua:26573；section：mod-tome/data/talents/misc/npcs.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ dashes quickly!
```
译文：
```text
@Source@快速移动！
```

## entry-02037
位置：mod-tome.lua:26577；section：mod-tome/data/talents/misc/npcs.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Hide in Plain Sight
```
译文：
```text
明处潜行
```

## entry-02038
位置：mod-tome.lua:26579；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have learned how to be stealthy even when in plain sight of your foes.  You may attempt to enter stealth regardless of how close you are to your enemies, but success is more likely against fewer opponents that are farther away.
		Your chance to succeed is determined by comparing %0.2f times your stealth power (currently %d) to the stealth detection of all enemies (reduced by 10%% per tile distance) that have a clear line of sight to you.
		You always succeed if you are not directly observed.
		This resets the cooldown of your Stealth talent, and, if successful, all creatures currently following you will lose track of your position.
		You estimate your current chance to hide as %0.1f%%.
```
译文：
```text
即使在你的敌人面前，你也学会了如何隐身。不管你与敌人有多近，你都可以尝试潜行，但敌人越少，距离越远成功率越高。
		你的成功率取决于你潜行强度的%0.2f倍（当前值 %d），以及所有视线能及你的敌人的侦测潜行能力（离你距离每有一格则下降10%%）。
		如果没有生物能看到你，你一定会潜行成功。
		这一技能会重置潜行技能的冷却时间。如果使用成功的话，所有正在追踪你的生物都会失去对你位置的感知。
		你估计你目前使用这一技能的成功率为%0.1f%%。
```

## entry-02039
位置：mod-tome.lua:26589；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are able to perform usually unstealthy actions (attacking, using objects, ...) without breaking stealth.	 When you perform such an action while stealthed, you have a chance to stay hidden.
		Success is more likely against fewer opponents and is determined by comparing %0.2f times your stealth power (currently %d) to the stealth detection (reduced by 10%% per tile distance) of all enemies that have a clear line of sight to you.
		Your base chance of success is 100%% if you are not directly observed, and good or bad luck may also affect it.
		You estimate your current chance to maintain stealth as %0.1f%%.
```
译文：
```text
你学会在潜行状态下使用一些通常会打破潜行的技能（如攻击，使用物品……）当你在隐身状态下这么做的时候，你有一定概率不会打破潜行状态。
		面对的对手越少，成功率越高；你的成功率取决于你潜行强度的%0.2f倍（当前值 %d），以及所有视线能及你的敌人的侦测潜行能力（离你距离每有一格则下降10%%）。
		当你不在敌人的视野内时，基础成功率为 100%%，这一几率还受你的运气影响。
		你估计当前成功率为 %0.1f%%。
```

## entry-02040
位置：mod-tome.lua:26599；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Whilst wearing leather or lighter armour, you gain %d%% Defense and %d%% Armour hardiness.
```
译文：
```text
当你身着轻甲和布甲时，你会增加 %d%% 近身闪避和 %d%% 护甲强度。
```

## entry-02041
位置：mod-tome.lua:26605；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You literally dance around your foes, increasing your movement speed by %d%% and reducing the cooldown of Hack'n'Back, Rush, Disengage and Evasion by %d turns.
```
译文：
```text
你在敌人周围跳起华丽的舞蹈，增加 %d%% 移动速度并减少燕回斩、冲锋、逃脱和回避的冷却时间 %d 回合。
```

## entry-02042
位置：mod-tome.lua:26607；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your cunning manipulations allow you to use charms (wands, totems and torques) more efficiently, reducing their cooldowns by %d%%.
```
译文：
```text
你灵活的头脑，使你可以更加有效的使用护符（魔杖、图腾和项圈），减少 %d%% 护符的冷却时间。
```

## entry-02043
位置：mod-tome.lua:26615；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Precision without dual wielding!
```
译文：
```text
你只有在双持状态下才能使用这个技能！
```

## entry-02044
位置：mod-tome.lua:26620；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require two melee weapons to use this talent.
```
译文：
```text
你需要双持近战武器才能使用这个技能。
```

## entry-02045
位置：mod-tome.lua:26621；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Momentum without dual wielding melee weapons!
```
译文：
```text
你只有双持近战武器的时候才可以使用急速切割！
```

## entry-02046
位置：mod-tome.lua:26635；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire bone spears in all directions, hitting all foes within radius %d for %0.2f physical damage, and inflicting bleeding for another %0.2f damage over 5 turns.
		The damage will increase with your Spellpower.
```
译文：
```text
向所有方向射出骨矛，对 %d 码范围内所有敌人造成 %0.2f 物理伤害，同时在 5 回合内造成 %0.2f 流血伤害。
		伤害受法术强度加成。
```

## entry-02047
位置：mod-tome.lua:26644；section：mod-tome/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to invoke your shadow!
```
译文：
```text
没有足够的空间召唤阴影！
```

## entry-02048
位置：mod-tome.lua:26660；section：mod-tome/data/talents/misc/npcs.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Dismay
```
译文：
```text
惊骇
```

## entry-02049
位置：mod-tome.lua:26661；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each turn, those caught in your gloom must save against your Mindpower or have an %0.1f%% chance of becoming dismayed for %d turns. When dismayed, the first melee attack against the foe will result in a critical hit.
```
译文：
```text
在黑暗光环里的每一个目标每回合必须与你的精神强度进行豁免鉴定，未通过鉴定则有 %0.1f%% 概率陷入惊慌失措持续 %d 回合，对处于惊慌失措状态的目标发动的首次近战攻击必定暴击。
```

## entry-02050
位置：mod-tome.lua:26667；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creates a circle of radius %d at your feet; the circle lights up affected tiles, increases your positive energy by %d each turn and deals %0.2f light damage and %0.2f fire damage per turn to everyone else within its radius.  The circle lasts %d turns.
		The damage will increase with your Spellpower.
```
译文：
```text
在你的脚下制造一个 %d 码半径的法阵，它会照亮范围区域，每回合增加 %d 正能量，并对范围内除你之外的所有生物每回合造成 %0.2f 光系伤害和 %0.2f 火焰伤害。
		阵法持续 %d 回合。
		伤害受法术强度加成。
```

## entry-02051
位置：mod-tome.lua:26677；section：mod-tome/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Cold Flames slowly spread from %d spots in a radius of %d around the targeted location. The flames deal %0.2f cold damage, and have a chance of freezing.
		Damage improves with your Spellpower.
```
译文：
```text
冰冷的火焰从目标位置周围 %d 处地点缓慢扩散，范围半径 %d 格。火焰会造成 %0.2f 冰冷伤害并有几率冰冻目标。
		伤害受法术强度加成。
```

## entry-02052
位置：mod-tome.lua:26712；section：mod-tome/data/talents/misc/objects.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You attune your %s to deal #ORANGE#mind#LAST# damage.
```
译文：
```text
你调谐了你的 %s，使其造成#ORANGE#精神#LAST#伤害。
```

## entry-02053
位置：mod-tome.lua:26722；section：mod-tome/data/talents/misc/objects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Bring a damage-type-specific ward into being. The ward will fully negate as many attacks of its element as it has charges.
		You can activate the following wards: %s
```
译文：
```text
激活指定伤害类型的抵抗状态，可完全抵消该属性的攻击，能抵消的次数等于其充能数。
		你能激活的伤害类型有：%s
```

## entry-02054
位置：mod-tome.lua:26731；section：mod-tome/data/talents/misc/objects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 Increases your spell save by %d for that turn.
```
译文：
```text
 那回合增加 %d 点法术豁免。
```

## entry-02055
位置：mod-tome.lua:26733；section：mod-tome/data/talents/misc/objects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 All blocked damage heals the wielder.
```
译文：
```text
 所有格挡的伤害值会治疗持有者。
```

## entry-02056
位置：mod-tome.lua:26734；section：mod-tome/data/talents/misc/objects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Raise your shield into blocking position for 2 turns reducing all non-Mind damage by %d. If you block all of an attack's damage, the attacker will be vulnerable to a deadly counterstrike (the next weapon attack will instead deal 200%% damage) for one turn.
			Counterstrike can normally only effect one enemy per block.
			If any damage was successfully blocked this effect will be removed at the start of your turn.
			If the shield has damage resistance to the blocked damage type the block value is increased by 50%%.
			
			Current Bonuses:  %s%s%s%s
```
译文：
```text
举起你的盾牌进入防御姿态 2 回合，减少所有非精神攻击伤害 %d。如果你完全格挡了一次攻击，攻击者将陷入可被致命反击的状态（下一次武器攻击将改为造成 200%% 伤害），持续 1 回合。
		每次格挡通常只能反击一个敌人。
		如果有任何伤害被成功格挡，此效果将在回合开始时移除。
		如果盾牌对格挡伤害类型有伤害抗性，则格挡值增加50%%。

		当前加成：%s%s%s%s
```

## entry-02057
位置：mod-tome.lua:26769；section：mod-tome/data/talents/misc/objects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You absorb latent cold around you, turning into an ice elemental - a shivgoroth - for %d turns.
		While transformed, you do not need to breathe, gain access to the Ice Storm talent at level %d, gain %d%% resistance to cuts and stuns, gain %d%% cold resistance, and all cold damage heals you for %d%% of the damage done.
		The power will increase with your Spellpower.
```
译文：
```text
你吸收周围的寒冰围绕你，将自己转变为纯粹的冰元素——西弗格罗斯，持续 %d 回合。
		转化成元素后，你不需要呼吸并获得等级 %d 的冰雪风暴，获得 %d%% 切割和震慑抵抗，%d%% 寒冰抗性，所有冰冷伤害可对你产生治疗，治疗量基于伤害值的 %d%%。
		效果受法术强度加成。
```

## entry-02058
位置：mod-tome.lua:26777；section：mod-tome/data/talents/misc/objects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Raise your dagger into blocking position for one turn, reducing the damage of all physical melee attacks against you by %d. If you block all of an attack's damage, the attacker will be vulnerable to a deadly counterstrike (a normal attack will instead deal 200%% damage) for one turn and be left disarmed for 3 turns.
		The blocking value will increase with your Dexterity and Cunning.
```
译文：
```text
举起你的匕首来格挡攻击一回合，减少所有物理伤害 %d 点。如果你完全格挡了一次攻击的伤害，攻击者将进入致命的被反击状态（对其进行的下一次武器攻击伤害增加到 200%%）一回合并被缴械三回合。
		格挡值受敏捷值和灵巧值加成。
```

## entry-02059
位置：mod-tome.lua:26799；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While Highers are not meant to rule other humans - and show no particular will to do so - they are frequently called to higher duties.
		Their nature grants them better senses than other humans.
		Increase blindness immunity by %d%%, maximum sight range by %d, and increases existing infravision, and heightened senses range by %d.
		At talent level 5, each time you hit a target you gain telepathy to all similar creatures in radius 15 for 5 turns.
```
译文：
```text
虽然高等人类的高贵血统并不意味着统治他人——他们也没有特别的意愿去那样做——但是他们经常承担更高的义务。
		他们的本能使得他们比别人有更强的直觉。
		增加 %d%% 目盲免疫，提高 %d 点最大视野范围并提高 %d 夜视及感应范围。
		技能等级 5 时，每次你命中目标，你将获得 15 格范围内同类型生物感知能力，持续 5 回合。
```

## entry-02060
位置：mod-tome.lua:26807；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Highers were originally created during the Age of Allure by the human Conclave. They are imbued with magic at the very core of their being.
		Increase spell save by %d and arcane resistance by %d%%.
		Also, when you cast a spell dealing damage, you gain a 20%% bonus to the damage type for 5 turns. (This effect has a cooldown.)
```
译文：
```text
高等人类们最初是在厄流纪由孔克雷夫创造的。他们天生具有魔法天赋。
		提高 %d 点法术豁免和 %d%% 奥术抗性。
		每次释放伤害法术时，5 回合内该伤害类型获得 20%% 伤害加成。（该效果有冷却时间。）
```

## entry-02061
位置：mod-tome.lua:26812；section：mod-tome/data/talents/misc/races.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Highborn's Bloom
```
译文：
```text
高等人类之绽放
```

## entry-02062
位置：mod-tome.lua:26832；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The world grows old as you stand through the ages. To you, time is different.
		Reduces the time remaining on detrimental effects by %d, most cooling down talents by %d, and increases the time remaining on beneficial effects by %d (up to 2 times the current duration).
```
译文：
```text
世界在不断的变老，而你似乎永恒不变。对于你来说，时间是不同寻常的。
		减少 %d 回合负面状态的持续时间，减少大多数技能 %d 回合冷却时间，并增加 %d 回合增益状态的持续时间（至多延长为剩余时间的两倍）。
```

## entry-02063
位置：mod-tome.lua:26841；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Thaloren have an affinity for natural elements, allowing them to heal for a portion of damage taken from them.
		You gain %d%% Nature and Acid damage affinity.
```
译文：
```text
自然精灵对自然元素有亲和力，这让它们在受到伤害时可以获得一定的治疗。
		获得 %d%% 自然和酸性伤害亲和。
```

## entry-02064
位置：mod-tome.lua:26849；section：mod-tome/data/talents/misc/races.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-02065
位置：mod-tome.lua:26890；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：[1, 4, 2, 3]；special：None

原文：
```text
Halfling's incredible luck always kicks in at just the right moment to save their skin.
		Whenever you take %d%% or more of your life from a single attack, you gain %d%% Evasion and %d additional defense for the next %d turns. The defense increases based on your luck and other defensive stats.
```
译文：
```text
半身人强大的人品在关键时刻总能保他们一命。
		每当你受到相当于生命值 %d%% 或更多的单次伤害时，你在接下来的 %d 回合内获得 %d%% 躲闪概率和 %d 点闪避值（其中闪避值加成基于幸运和其他闪避相关数值）。
```

## entry-02066
位置：mod-tome.lua:26894；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Halflings have always been a very organised and methodical race; the more foes they face, the more organised they are.
		If two or more foes are in sight your Physical Power, Physical Save, Spellpower, Spell Save, Mental Save, and Mindpower are increased by %0.1f per foe (up to 5 foes).
```
译文：
```text
半身人向来是一个有组织、有条理的种族，敌人越多他们越团结。
		如果有 2 个或多个敌人在你的视野里，每个敌人都会使你的所有强度和豁免提高 %0.1f（最多 5 个敌人）。
```

## entry-02067
位置：mod-tome.lua:26898；section：mod-tome/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Halflings have one of the most powerful military forces in the known world and have been at war with most other races for thousands of years.
		Removes %d stun, daze, or pin effects and grants immunity to stuns, dazes and pins for %d turns.
```
译文：
```text
半身人拥有已知世界最强大的军事力量之一，数千年来一直与大多数其他种族交战。
		移除 %d 个震慑、眩晕或定身效果，并使你对震慑、眩晕和定身免疫 %d 回合。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Positive energy	正能量	T.GAME.RESOURCE	combat	_t	preferred	core	太阳骑士/赞歌职业资源；与 Negative energy 负能量区分
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
age of allure	厄流纪	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	既有时代专名，全仓相关叙事统一使用；不按普通词 allure 逐字翻译
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
charm	护符	T.GAME.ENTITY	items	entity type	existing	global	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
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
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
shivgoroth	西弗格罗斯	T.GAME.ENTITY	creatures	entity name	preferred	core	寒冰元素生物专名；统一实体名、形态技能、状态说明与变形日志，不写作“西弗戈洛斯”
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
