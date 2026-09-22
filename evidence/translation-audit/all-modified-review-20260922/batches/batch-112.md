# batch-112：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03605
位置：tome-cults.lua:3200；section：tome-cults/data/talents/demented/tentacles.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your left hand mutates into a disgusting mass of tentacles.
		When you have your offhand empty you automatically hit your target and those on the side whenever you hit with a basic attack.
		Also increases Physical Power by %d, and increases weapon damage by %d%% for your tentacles attacks.
		Each time you make an attack with your tentacle you gain %d insanity.
		You generate a low power psionic field around you when around #{italic}#'civilized people'#{normal}# that prevents them from seeing you for the horror you are.

		Your tentacle hand currently has these stats%s:
		%s
```
译文：
```text
你的左手异变成为一坨恶心的触手。
		副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。
		物理强度提高 %d，触手武器伤害提高 %d%%。
		每次触手攻击时，获得 %d 疯狂值。
		附近有 #{italic}# 普通人 #{normal}# 时会自动生成微弱的心灵护盾，避免被他们发现你的恐魔形态。
		你的触手当前属性为 %s :
		%s
```

## entry-03606
位置：tome-cults.lua:3214；section：tome-cults/data/talents/demented/tentacles.lua；source_tag：_t；args_order：None；special：None

原文：
```text
, #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#
```
译文：
```text
，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#
```

## entry-03607
位置：tome-cults.lua:3237；section：tome-cults/data/talents/demented/tentacles.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s's tentacle fails to move %s!
```
译文：
```text
%s的触手无法移动%s！
```

## entry-03608
位置：tome-cults.lua:3260；section：tome-cults/data/talents/demented/timethief.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Release a surge of entropy, cleansing yourself of afflictions while draining the energy from others. All enemies in range 10 will have the duration of %d beneficial effects reduced by %d turns, while you will have an equal number of detrimental effects reduced by the same duration.
```
译文：
```text
释放熵的浪潮，清除自己的灾祸，同时吸取他人的能量。10 码内所有敌人的 %d 项有益效果持续时间缩短 %d 回合。自身同等数量的有害效果持续时间缩短同等回合。
```

## entry-03609
位置：tome-cults.lua:3266；section：tome-cults/data/talents/demented/timethief.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03610
位置：tome-cults.lua:3280；section：tome-cults/data/talents/demented/void.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must be wearing light armor for this talent.
```
译文：
```text
你必须穿着轻甲才能使用这一技能。
```

## entry-03611
位置：tome-cults.lua:3282；section：tome-cults/data/talents/demented/void.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#FIREBRICK##Target#'s void star absorbs the damage from #Source#, converting it into entropy!#LAST#
```
译文：
```text
#FIREBRICK##Target#的虚空之星吸收了来自#Source#的伤害，将其转化为熵！#LAST#
```

## entry-03612
位置：tome-cults.lua:3284；section：tome-cults/data/talents/demented/void.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjure void stars that orbit you, defending you from incoming attacks. Each time an attack deals more than 10%% of your maximum life, a star will be consumed to reduce the damage taken by %d%%, of which 40%% will be dealt to you as entropic backlash.
		You regenerate 1 star every %d turns, stacking up to 4 times.
		This talent will only function in light armor.
```
译文：
```text
形成围绕你旋转，为你抵御伤害的虚空之星。
		每当受到超过 10%% 最大生命的伤害时，消耗一颗虚空之星，使受到的伤害减少 %d%%，自己受到等同于减免伤害 40%% 的熵能反冲。
		虚空之星每经过 %d 回合自动恢复一颗。
		此技能只有装备轻甲时生效。
```

## entry-03613
位置：tome-cults.lua:3291；section：tome-cults/data/talents/demented/void.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reinforce your armor with countless tiny void stars, increasing armor by %d.
Each time your void stars are fully depleted, you gain a shield absorbing the next %d damage taken within %d turns. This shield cannot trigger again until your void stars are fully restored.
```
译文：
```text
用无数微小的虚空之星强化护甲，护甲值提高 %d。
每次虚空之星完全消耗后，生成一个吸收 %d 伤害的护盾持续 %d 回合。在虚空之星完全恢复前无法再次生成护盾。
```

## entry-03614
位置：tome-cults.lua:3300；section：tome-cults/data/talents/demented/void.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Consuming a void star, you use it to summon a void monolith at the targeted location for %d turns. The monolith is very durable, and while immobile it will attempt to daze enemies within radius %d for 2 turns every half a turn using your spellpower.
			The monolith will gain %d life rating and %d%% all resist based on your Magic stat.
```
译文：
```text
消耗一枚虚空之星，在目标位置召唤持续 %d 回合的虚无巨石。巨石非常坚固，无法移动，每半回合对 %d 码范围内敌人施加眩晕2回合（基于本体法术强度）。
			基于你的魔法属性，巨石获得 %d 生命成长和 %d%% 全体抗性。
```

## entry-03615
位置：tome-cults.lua:3304；section：tome-cults/data/talents/demented/void.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s rends the essence of %s, restoring %d void shards!
```
译文：
```text
%s撕裂了%s的精华，恢复%d个虚空之星！
```

## entry-03616
位置：tome-cults.lua:3312；section：tome-cults/data/talents/demented/writhing-body.lua；source_tag：_t；args_order：None；special：None

原文：
```text
, #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#
```
译文：
```text
，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#
```

## entry-03617
位置：tome-cults.lua:3372；section：tome-cults/data/talents/misc/misc.lua；source_tag：tformat；args_order：[2, 1]；special：None

原文：
```text
Self destruct in a glorious explosion of gore dealing %0.2f blight damage to all enemies in %d radius.  Your summoner must be dead to use this talent.
```
译文：
```text
自爆成一团光荣的血肉，对半径 %d 格范围内的所有敌人造成 %0.2f 枯萎伤害。这个技能只有主人死亡时能够使用。
```

## entry-03618
位置：tome-cults.lua:3373；section：tome-cults/data/talents/misc/misc.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Teleport: Kroshkkur
```
译文：
```text
传送：克诺什库尔
```

## entry-03619
位置：tome-cults.lua:3375；section：tome-cults/data/talents/misc/misc.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The spell fizzles...
```
译文：
```text
法术失败了……
```

## entry-03620
位置：tome-cults.lua:3395；section：tome-cults/data/talents/misc/misc.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Evolve %d allies within radius 10 in random ways for 5 turns.
		#ORCHID#Speed:#LAST# Increases global speed by %d%%.
		#ORCHID#Form:#LAST# Increases all stats by %d.
		#ORCHID#Power:#LAST# Increases all damage by %d%%.
```
译文：
```text
以随机方式进化 10 格范围内至多 %d 名友方单位，持续 5 回合。
		#ORCHID#速度：#LAST# 增加 %d%% 整体速度。
		#ORCHID#形态：#LAST# 增加 %d 全属性。
		#ORCHID#力量：#LAST# 增加 %d%% 伤害。
```

## entry-03621
位置：tome-cults.lua:3406；section：tome-cults/data/talents/misc/misc.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the splinters!
```
译文：
```text
%s 抵抗了玻璃碎片！
```

## entry-03622
位置：tome-cults.lua:3417；section：tome-cults/data/talents/misc/misc.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# expertly hurls a pebble at #target#!
```
译文：
```text
#Source#朝#target#投掷鹅卵石！
```

## entry-03623
位置：tome-cults.lua:3443；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your skin grows small spikes coated in dark blight.
		When you are hit in melee the attacker starts bleeding black blood for 5 turns that deals %0.2f darkness damage each turn. This effect may only happen once per turn.
		You are empowered by the sight of the black blood, for each bleeding creature in radius 2 you gain 5%% all resistances, limited to %d creatures.
		The damage will scale with your Magic stat.
```
译文：
```text
你的皮肤生长出被黑暗和枯萎力量覆盖的尖刺。
		当你被近战攻击命中时，攻击者开始流出黑血，持续 5 回合，每回合造成 %0.2f 暗影伤害。该效果每回合只能触发一次。
		同时，目睹黑血会使你受到强化：2 格范围内每个可见的流着黑血的生物，都使你获得 5%% 全部抗性，最多计 %d 个生物。
		伤害随魔法属性提升。
```

## entry-03624
位置：tome-cults.lua:3451；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your faceless visage is puzzling and emotionless, allowing you to more easily resist mind tricks.
		You gain %d mental save, %d%% confusion immunity.
```
译文：
```text
你无面孔的脸没有情感，令人困惑。这让你更容易抵抗精神冲击。
		你获得 %d 精神豁免，%d%% 混乱免疫。
```

## entry-03625
位置：tome-cults.lua:3455；section：tome-cults/data/talents/misc/races.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03626
位置：tome-cults.lua:3458；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your affinity with things that dwell deep beneath the surface allows you to summon a hungering mouth.
		The mouth has %d bonus life, lasts for %d turns, and deals no damage.
		Each turn the mouth will draw all enemies in radius 10 2 spaces towards itself.
		Its bonus life depends on your Constitution stat and talent level.  Many other stats will scale with level.
```
译文：
```text
你同地下深处某物的联系让你能召唤一只饥饿巨口。
		每回合它将周围 10 码内所有敌人朝自身拉近 2 码。
		它有 %d 额外生命，存在 %d 回合，不造成伤害。
		它的额外生命取决于你的体质和技能等级。许多其他属性受等级影响。
```

## entry-03627
位置：tome-cults.lua:3470；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You unleash the wrath of the wilds for 5 turns.
		When you deal damage to a creature while wrath is active you have %d%% chance (100%% for the first creature hit each turn) to stun them for 3 turns.
		This effect can only stun a creature once per turn.
		Chance scales with your Constitution and apply power is the highest or your physical or mind power.
```
译文：
```text
你释放持续 5 回合的自然的愤怒。
		愤怒状态下，每当你造成伤害时有 %d%% （每回合攻击的第一个生物 100%%）几率震慑 3 回合。
		每个敌人每回合只能被该技能震慑一次。
		震慑几率受体质影响，强度由物理或精神强度中较高一项决定。
```

## entry-03628
位置：tome-cults.lua:3487；section：tome-cults/data/talents/misc/races.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LAST# #{italic}#(current)#{normal}#
```
译文：
```text
#LAST# #{italic}#（当前）#{normal}#
```

## entry-03629
位置：tome-cults.lua:3490；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：[1, 3, 2, 4, 5, 6]；special：None

原文：
```text
Since ziguranth removed those filthy magic runes from your body you have needed an alternative form of power to sustain your body. Thanks to drake blood you have found that power.
		Your blood hardens yourself, passively increasing stun resistance by %d%%, %s resistance by %d%% and dealing %d %s damage on melee attacks.
		You can activate this talent to change which drake aspect to bring forth, altering the elemental type of the bonus.
		The resistance and damage scales with your Willpower.

		Changing your aspect requires combat experience, you may only do so after slaying 100 enemies (current %d).

		When you learn this talent you become so strong you can wield any type of one handed weapon in your offhand.
```
译文：
```text
伊格兰斯除去了你身体内部肮脏的魔法符文，此后你需要另一种力量来维持你的身体。多亏了龙血，你找到了这种力量。
		龙血强化了你，使你获得 %d%% 震慑抗性，%d%% %s 伤害抗性，%d %s 近战附加伤害。
		你可以主动开启该技能来改变龙血类型，进而改变相应元素。
		抗性和附加伤害受意志值加成。

		改变龙血类型需要战斗经验，你必须杀死 100 个敌人后才能使用（当前 %d）。

		当你学会该技能时，你变得如此强大，以至于能双持任何单手武器。
```

## entry-03630
位置：tome-cults.lua:3510；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You were created by ziguranth for one purpose only, to wage war on magic!
			Strike your target dealing %d%% %s weapon damage and silencing them for %d turns.
			The damage type will change with your drake aspect.
			The chance to silence will increase with the highest of your physical or mind power.
```
译文：
```text
你被伊格制造的唯一理由：对魔法作战！
		打击你的敌人，造成 %d%% %s 武器伤害，并沉默它们 %d 回合。
		伤害类型根据龙血的类型而决定。
		沉默的几率受物理强度或精神强度的最高值加成。
```

## entry-03631
位置：tome-cults.lua:3520；section：tome-cults/data/talents/misc/races.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# tries to bite #target#!
```
译文：
```text
#Source#试图咬#target#！
```

## entry-03632
位置：tome-cults.lua:3522；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You try to bite off your foe with your #{italic}#head#{normal}# for %d%% blight weapon damage.
		If the target falls under 20%% life you have %d%% chances to outright kill it (bosses are immune).
		Whenever you succesfully bite a foe you regenerate %0.1f life per turn for 5 turns.
		Instant kill chances and regeneration increase with your Constitution stat and weapon damage increases with the highest of your Strength, Dexterity or Magic stat.
```
译文：
```text
你尝试用 #{italic}#头#{normal}# 咬你的敌人造成 %d%% 枯萎武器伤害。
		如果目标被咬后生命不足 20%%，你有 %d%% 几率直接杀死它（对 boss 无效）。
		你咬中以后 5 回合内每回合回复 %0.1f 生命。
		秒杀几率和生命回复受体质加成，武器伤害受力量敏捷魔法中最高值影响。
```

## entry-03633
位置：tome-cults.lua:3530；section：tome-cults/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Without the distraction of #{bold}#thoughts#{normal}# or #{bold}#self#{normal}# your body reacts faster and better to aggressions.
		Increases global speed by %d%%.
```
译文：
```text
没有 #{bold}#思维#{normal}# 和 #{bold}#自我#{normal}# 的干扰，你的身体全凭本能行动，反应速度更快。
		整体速度增加 %d%%。
```

## entry-03634
位置：tome-cults.lua:3552；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Fight your foe! If anything wrong happens, the Fortress will pull you out.
```
译文：
```text
攻击敌人！如果出了什么问题，堡垒会把你送出去。
```

## entry-03635
位置：tome-cults.lua:3559；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# starts to bleed black blood.
```
译文：
```text
#Target#开始流出黑血。
```

## entry-03636
位置：tome-cults.lua:3560；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# stops bleeding black blood.
```
译文：
```text
#Target#不再流出黑血。
```

## entry-03637
位置：tome-cults.lua:3568；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is caught by a slimy tendril.
```
译文：
```text
#Target#被黏稠触须捕获。
```

## entry-03638
位置：tome-cults.lua:3569；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is free from the tendril.
```
译文：
```text
#Target#逃脱黏稠触须。
```

## entry-03639
位置：tome-cults.lua:3572；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is constricted by a tentacle.
```
译文：
```text
#Target#被触手缠绕。
```

## entry-03640
位置：tome-cults.lua:3602；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Terrified of the horror duo attacking them reducing defense and spell save by %d.
```
译文：
```text
因两只恐魔的现身而惊恐，闪避和法术豁免降低 %d。
```

## entry-03641
位置：tome-cults.lua:3603；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is terrified of the horrors attacking him!
```
译文：
```text
#Target#因攻击他的恐魔惊恐！
```

## entry-03642
位置：tome-cults.lua:3609；section：tome-cults/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%d stacks, +%d%% to all damage dealt.
```
译文：
```text
%d 层，+%d%% 所有造成的伤害。
```

## entry-03643
位置：tome-cults.lua:3628；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is empowered by the pain of its victim.
```
译文：
```text
#Target#被牺牲者的痛苦强化。
```

## entry-03644
位置：tome-cults.lua:3633；section：tome-cults/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#PURPLE##Target# turns into an horror.
```
译文：
```text
#PURPLE##Target#变成了恐魔。
```

## 相关术语快照
```tsv
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Constrict	缠绕	T.GAME.TALENT	talents	talent name	preferred	core	1.8beta 在技能名、状态和战斗日志中统一使用
Constricted	缠绕	T.GAME.EFFECT	combat	_t	preferred	core	状态名及其战斗日志统一使用“缠绕”
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
Ziguranth	伊格兰斯	T.PN.FACTION	society	nil	preferred	core	反魔教团专名（全称）；与其据点地名 Zigur「伊格」同源且紧密关联，但指称不同：固定源码 624a673 同一句写作 “The defenders of Zigur were crushed, the Ziguranth scattered and weakened.”，Zigur 是被攻陷的据点，Ziguranth 是被打散的教团。教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换（b23 曾把「去伊格训练」误作「伊格兰斯」）。
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
cleansing	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key；同 cohort 的 cleanse 运行键亦采用“洁净”；不约束其他语境
cleansing 	洁净的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的前缀名称；保留 source 尾空格；不约束技能、伤害类型、日志或叙事中的 cleansing
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
entropy	熵	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
entropy	熵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
offhand	副手	T.GAME.ENTITY	items	nil	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
tentacles	触手	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
