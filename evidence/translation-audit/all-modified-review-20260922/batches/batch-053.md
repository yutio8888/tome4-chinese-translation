# batch-053：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01505
位置：mod-tome.lua:20980；section：mod-tome/data/talents/celestial/celestial.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Sing of death and damnation.
```
译文：
```text
死亡和毁灭之歌。
```

## entry-01506
位置：mod-tome.lua:20992；section：mod-tome/data/talents/celestial/chants.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You chant the glory of the Sun, granting you %d%% physical damage resistance, %d physical save, %d armour and +15%% armour hardiness.
		You may only have one Chant active at once.
		The effects will increase with your Spellpower.
```
译文：
```text
颂赞日之荣耀，使你获得 %d%% 物理抗性，%d 物理豁免，%d 护甲与 15%% 护甲强度。
		同时只能激活一种赞歌。
		效果受法术强度加成。
```

## entry-01507
位置：mod-tome.lua:20998；section：mod-tome/data/talents/celestial/chants.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You chant the glory of the Sun, granting you %d%% fire, lightning, acid and cold damage resistance, %d spell save and reduces the damage from enemies 3 or more spaces away by %d%%.
	You may only have one Chant active at once.
	The effects will increase with your Spellpower.
```
译文：
```text
颂赞日之荣耀，使你获得 %d%% 火焰、闪电、酸性和寒冷抗性，%d 法术豁免，并减少三格外敌人对你造成的伤害 %d%%。
	同时只能激活一种赞歌。
	效果受法术强度加成。
```

## entry-01508
位置：mod-tome.lua:21014；section：mod-tome/data/talents/celestial/chants.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have learned to sing the praises of the Sun, in the form of three defensive Chants.
			Chant of Fortitude: Increases your mental save by %d and maximum life by %d%%.
			Chant of Fortress: Increases your physical save by %d, your physical resistance by %d%%, your armour by %d and your armour hardiness by 15%%.
			Chant of Resistance: Increases you spell save by %d, your fire/cold/lightning/acid resistances by %d%% and reduces all damage that comes from distant enemies (3 spaces or more) by %d%%.
			You may only have one Chant active at a time.
```
译文：
```text
你学会了三种防御赞歌，以此咏唱对太阳的赞颂：
			坚韧赞歌：增加 %d 精神豁免，%d%% 最大生命值
			堡垒赞歌：增加 %d 物理豁免，%d%% 物理抗性，%d 护甲，15%% 护甲强度
			元素赞歌：增加 %d 法术豁免，%d%% 火焰 /寒冷 /闪电 /酸性抗性，减少三格外敌人对你造成的伤害 %d%%。
			你同时只能激活一种赞歌。
```

## entry-01509
位置：mod-tome.lua:21029；section：mod-tome/data/talents/celestial/chants.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your skill at Chanting now extends the cloak of light, increasing your light radius by %d.
		Also, when you start a new Chant, you will be cured of all cross-tier effects and cured of up to %d debuffs.
		Chant of Fortitude cures mental effects.
		Chant of Fortress cures physical effects.
		Chant of Resistance cures magical effects.
```
译文：
```text
咏唱赞歌的娴熟技艺让光明得以扩散，增加 %d 光照半径。
		每次你咏唱新的赞歌时，你将解除自身的越层效果（失去平衡、法术冲击和思维封锁），并额外解除 %d 项相应类型的负面状态。
		坚韧赞歌：解除精神负面状态
		堡垒赞歌：解除物理负面状态
		元素赞歌：解除魔法负面状态。
```

## entry-01510
位置：mod-tome.lua:21053；section：mod-tome/data/talents/celestial/circles.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creates a circle of radius %d at your feet; the circle protects you from silence effects while you remain in its radius while silencing and dealing %d light damage to everyone else who enters. The circle lasts %d turns.
```
译文：
```text
在你的脚下制造一个 %d 码半径范围的法阵，当你在法阵内，它会使你免疫沉默效果，并沉默进入此范围的其他所有生物，对其造成 %d 光系伤害。
		法阵持续 %d 回合。
```

## entry-01511
位置：mod-tome.lua:21056；section：mod-tome/data/talents/celestial/circles.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creates a circle of radius %d at your feet; the circle slows incoming projectiles by %d%% and attempts to push all creatures other than yourself out of its radius, inflicting %0.2f light damage and %0.2f darkness damage per turn as it does so.  The circle lasts %d turns.
		The effects will increase with your Spellpower.
```
译文：
```text
在你的脚下制造一个 %d 码半径范围的法阵，它会减慢 %d%% 抛射物速度并尝试将除你以外的其他生物推出法阵范围，同时每回合造成 %0.2f 光系伤害和 %0.2f 暗影伤害。法阵持续 %d 回合。
		效果受法术强度加成。
```

## entry-01512
位置：mod-tome.lua:21076；section：mod-tome/data/talents/celestial/combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Infuse your weapon with the power of the Sun, adding %0.1f light damage on each melee hit.
		Additionally, if you have a temporary damage shield active, melee hits will increase its power by %d once per turn.
		The damage dealt and shield bonus will increase with your Spellpower.
```
译文：
```text
使你的武器充满太阳能量，每次近战命中造成 %0.1f 光系伤害。
		如果你同时打开了临时伤害护盾，每回合一次，你的近战攻击命中可以增加护盾 %d 强度。
		伤害和护盾加成受法术强度加成。
```

## entry-01513
位置：mod-tome.lua:21083；section：mod-tome/data/talents/celestial/combat.lua；source_tag：tformat；args_order：[1, 2, 3, 5, 4]；special：None

原文：
```text
In a pure display of power, you project a ranged melee attack, doing %d%% weapon damage.
		If the target is outside of melee range, you have a chance to project a second attack against it for %d%% weapon damage.
		The second strike chance (which increases with distance) is %0.1f%% at range 2 and %0.1f%% at the maximum range of %d.
		The range will increase with your Strength.
```
译文：
```text
你展现纯粹的力量，发动一次远程近战攻击，造成 %d%% 武器伤害。
		如果目标在近战范围以外，有一定几率进行二次打击，造成 %d%% 武器伤害。
		二次打击几率随距离增加，距离 2 时为 %0.1f%%，距离最大（%d）时几率为 %0.1f%%。
		攻击距离受力量值加成。
```

## entry-01514
位置：mod-tome.lua:21091；section：mod-tome/data/talents/celestial/combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your weapon attacks burn with righteous fury, dealing %d%% of your lost HP as additional Fire damage (up to %d, Current:  %d).
		Targets struck are also afflicted with a Martyrdom effect that causes them to take %d%% of all damage they deal for 4 turns.
		The bonus damage can only occur once per turn.
```
译文：
```text
你使用武器攻击时，造成相当于 %d%% 你已损失的生命值的火焰伤害，至多 %d 点，当前 %d 点
		然后令目标进入殉难状态，受到 %d%% 自己造成的伤害，持续 4 回合。
		每回合最多触发一次额外伤害。
```

## entry-01515
位置：mod-tome.lua:21097；section：mod-tome/data/talents/celestial/combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Any attack that would drop you below 1 hit point instead triggers Second Life, deactivating the talent, setting your hit points to 1, then healing you for %d.
```
译文：
```text
任何使你生命值降到 1 点以下的攻击都会激活第二生命，自动中断此技能并将你的生命值恢复到 1 点，然后受到 %d 点治疗。
```

## entry-01516
位置：mod-tome.lua:21110；section：mod-tome/data/talents/celestial/crusader.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You strike your foe with your two handed weapon, dealing %d%% weapon damage.
		If the attack hits, all foes in radius 2 will have their light resistance reduced by %d%% and their damage reduced by %d%% for 5 turns.
```
译文：
```text
你用双手武器攻击敌人，造成 %d%% 武器伤害。
		如果攻击命中，半径 2 以内的敌人光系抗性下降 %d%%，伤害下降 %d%% , 持续 5 回合。
```

## entry-01517
位置：mod-tome.lua:21116；section：mod-tome/data/talents/celestial/crusader.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While wielding a two handed weapon, your critical strike chance is increased by %d%%, and your melee criticals instill you with righteous strength, increasing all physical and light damage you deal by %d%%, stacking up to 3 times.
		In addition, your melee critical strikes leave a lasting lightburn on the target, dealing %0.2f light damage over 5 turns and reducing opponents armour by %d.
		The damage increases with your Spellpower.
```
译文：
```text
当装备双手武器时，你的暴击率增加 %d%% , 同时你的近战暴击会引发光明之力，增加 %d%% 物理和光系伤害加成，最多叠加 3 次。
		同时，你的近战暴击会在目标身上留下灼烧痕迹，5 回合内造成 %0.2f 光系伤害，同时减少 %d 护甲。
		伤害受法强加成。
```

## entry-01518
位置：mod-tome.lua:21122；section：mod-tome/data/talents/celestial/crusader.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Infuse your two handed weapon with light while spinning around.
		All creatures in radius one take %d%% weapon damage.
		In addition while spinning your weapon shines so much it deals %d%% light weapon damage to all foes in radius 2.
		At level 4 your spinning blade creates a shield that blocks all damage for 1 turn.
```
译文：
```text
旋转一周，同时将光明之力充满武器。
		半径 1 以内的敌人将受到 %d%% 武器伤害，同时半径 2 以内的敌人将受到 %d%% 光系武器伤害。
		技能等级 4 或以上时，在旋转时你会制造一层护盾，吸收 1 回合内的所有攻击。
```

## entry-01519
位置：mod-tome.lua:21142；section：mod-tome/data/talents/celestial/dark-sun.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Singularity Armor
```
译文：
```text
奇点护甲
```

## entry-01520
位置：mod-tome.lua:21166；section：mod-tome/data/talents/celestial/darkside.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your curse feeds on the magic, which in turn is powered by the curse.
You gain a bonus to Spellpower equal to %d%% of your Willpower.
You gain a bonus to Mindpower equal to %d%% of your Magic.

#{italic}#Something is not quite right inside you.  Your solar spells are somehow twisted, but your bloody rites make things clear as day.#{normal}#
```
译文：
```text
你的诅咒汲取着魔法同时又驱动着魔法。
你获得相当于 %d%% 意志的法术强度加值。
你获得相当于 %d%% 魔法的精神强度加值。

#{italic}#你的体内有些不对劲。你的太阳法术不知何故被扭曲了，但你血腥的仪式使得事物如同白昼一样清晰。#{normal}#
```

## entry-01521
位置：mod-tome.lua:21176；section：mod-tome/data/talents/celestial/darkside.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s's teleportation fizzles!
```
译文：
```text
%s 的传送失败了！
```

## entry-01522
位置：mod-tome.lua:21177；section：mod-tome/data/talents/celestial/darkside.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s emerges from the darkness!
```
译文：
```text
%s从黑暗中现身了！
```

## entry-01523
位置：mod-tome.lua:21204；section：mod-tome/data/talents/celestial/dirge.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sing a song of violence and victory (mostly violence) and sustain yourself through cruelty.
Each time you deal a critical strike you gain 10%% of a turn (only once per turn).
Each time you kill a creature you gain %d%% of a turn (only once per turn).

```
译文：
```text
唱一首关于暴力与胜利的歌（主要是暴力），以残酷来维持自身。
你每次暴击时获得 10%% 个回合的时间（每回合限一次）。
你每次杀死一个生物时获得 %d%% 个回合的时间（每回合限一次）。

```

## entry-01524
位置：mod-tome.lua:21227；section：mod-tome/data/talents/celestial/dirge.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Dirge Intoner
```
译文：
```text
挽歌吟诵者
```

## entry-01525
位置：mod-tome.lua:21239；section：mod-tome/data/talents/celestial/dirge.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Dirge Nihilist
```
译文：
```text
挽歌虚无者
```

## entry-01526
位置：mod-tome.lua:21275；section：mod-tome/data/talents/celestial/glyphs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When one of your spells goes critical, you bind glyphs in radius 1 centered on a random target in range %d at the cost of 5 positive and 5 negative energy.
		Glyphs last for %d turns and cause various effects when an enemy enters their grid.
		Glyphs will only spawn on enemies that aren't adjacent to an existing glyph.
		This can only happen every %d game turns.
		Glyph effects will scale with your Spellpower.

		Available glyphs are:
		#ffd700#Glyph of Sunlight#LAST#:  Bind sunlight into a glyph. When triggered it will release a brilliant light, dealing %0.2f light damage and healing you for %d.
		#7f7f7f#Glyph of Moonlight#LAST#:  Bind moonlight into a glyph. When triggered it will release a fatiguing darkness,  dealing %0.2f darkness damage and reducing the foes damage dealt by %d%% for %d turns.
		#9D9DC9#Glyph of Twilight#LAST#:  Bind twilight into a glyph. When triggered it will release a burst of twilight, dealing %0.2f light and %0.2f darkness damage and knocking the foe back %d tiles.
		
```
译文：
```text
每当你的法术暴击时，你消耗 5 点正能量和负能量，在范围 %d 内的随机目标周围 1 码半径的区域内放置随机圣印。
		圣印持续 %d 回合，当敌人踩上时，会对其产生特殊效果。
		圣印只会在周围没有圣印的敌人周围产生。
		每 %d 游戏回合最多触发一次该效果。
		圣印效果受法术强度加成。

		有以下几种可用的圣印：
		#ffd700#日光圣印#LAST#——将阳光注入圣印。当其触发时，将会释放出明亮耀眼的光芒，造成 %0.2f 光系伤害，并恢复你 %d 生命值。
		#7f7f7f#月光圣印#LAST#——将月光注入圣印。当其触发时，将会释放出疲惫困倦的黑暗，造成 %0.2f 暗影伤害，并使目标所造成的伤害减少 %d%%，持续 %d 回合。
		#9D9DC9#暮光圣印#LAST#——将暮光注入圣印。当其触发时，将会释放出突然爆炸的暮光，造成 %0.2f 光系和 %0.2f 暗影伤害，并将目标击退 %d 格。
		
```

## entry-01527
位置：mod-tome.lua:21306；section：mod-tome/data/talents/celestial/glyphs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Up to 3 times per turn when one of your glyphs triggers you feel a surge of celestial power, increasing your darkness and light resistance and affinity by 5%% for %d turns, stacking up to %d times.
```
译文：
```text
当你的圣印触发时，天空能量的涌动让你获得暗影、光系抗性和伤害亲和各 5%%，持续 %d 回合，最多叠加 %d 次。该效果每回合最多触发 3 次。
```

## entry-01528
位置：mod-tome.lua:21308；section：mod-tome/data/talents/celestial/glyphs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Destabilize your glyphs, triggering every glyph in radius 10 with an enemy standing on it.
		At talent level 2 glyphs triggered this way will leave a residue of themselves on the ground, dealing damage each turn for %d turns.
		#ffd700#Sunlight#LAST#:  %0.2f light damage.
		#7f7f7f#Moonlight#LAST#:  %0.2f darkness damage.
		#9D9DC9#Twilight#LAST#:  %0.2f light and %0.2f darkness damage
```
译文：
```text
激发所有圣印，10格内所有上方站着敌人的圣印将被触发。
		技能等级2时，该效果触发的圣印将在地面遗留能量，在 %d 回合内持续造成伤害。
		#ffd700#日光圣印#LAST#：%0.2f 光系伤害。
		#7f7f7f#月光圣印#LAST#：%0.2f 暗影伤害。
		#9D9DC9#暮光圣印#LAST#：%0.2f 光系和 %0.2f 暗影伤害。
```

## entry-01529
位置：mod-tome.lua:21330；section：mod-tome/data/talents/celestial/guardian.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Brandish without a shield!
```
译文：
```text
没有盾牌就无法使用剑盾之怒！
```

## entry-01530
位置：mod-tome.lua:21335；section：mod-tome/data/talents/celestial/guardian.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Retribution without a shield!
```
译文：
```text
没有盾牌就无法使用惩戒之盾！
```

## entry-01531
位置：mod-tome.lua:21343；section：mod-tome/data/talents/celestial/guardian.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Crusade without a shield!
```
译文：
```text
使用十字军打击必须使用盾牌！
```

## entry-01532
位置：mod-tome.lua:21344；section：mod-tome/data/talents/celestial/guardian.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You demonstrate your dedication to the light with a measured attack striking once with your weapon for %d%% Light damage and once with your shield for %d%% Light damage.
			If the first strike connects %d random talent cooldowns are reduced by 1.
			If the second strike connects you are cleansed of %d debuffs.
```
译文：
```text
你以一次沉稳的攻击展现对圣光的奉献：先用武器攻击造成 %d%% 光系伤害，再用盾牌攻击造成 %d%% 光系伤害。
			如果第一次攻击命中，随机 %d 个技能冷却时间减少1回合。
			如果第二次攻击命中，除去你身上至多 %d 个负面状态。
```

## entry-01533
位置：mod-tome.lua:21407；section：mod-tome/data/talents/celestial/hymns.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your skill in Hymns now improves your sight in darkness, increasing your infravision radius by %d.
		Also, when you end a Hymn, you will gain a buff of a type based on which Hymn you ended.
		Hymn of Shadows increases your movement speed by %d%% for one turn.
		Hymn of Detection makes you invisible (power %d) for %d turns.
		Hymn of Perseverance grants a damage shield (power %d) for %d turns.
```
译文：
```text
咏唱圣诗的娴熟技艺让黑暗不再阻碍你的视线，增加 %d 暗视半径。
		每次你结束旧的圣诗时，你将获得圣诗提供的增益效果。
		暗影圣诗：增加 %d%% 移动速度，持续 1 回合。
		侦测圣诗：获得强度 %d 的隐形，持续 %d 回合。
		坚毅圣诗：护盾 (%d 强度) 持续 %d 回合。
```

## entry-01534
位置：mod-tome.lua:21433；section：mod-tome/data/talents/celestial/light.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A magical zone of Sunlight appears around you, healing and shielding all within a radius of %d for %0.2f per turn and increasing healing effects on everyone within by %d%%. The effect lasts for %d turns.
		Existing damage shields will be added to instead of overwritten and have their duration set to 2 if it isn't higher.
		If the same shield is refreshed 20 times it will become unstable and explode, removing it.
		It also lights up the affected area.
		The amount healed will increase with the Magic stat
```
译文：
```text
阳光倾泻在你周围 %d 码范围内，每回合治疗所有单位 %0.2f 生命值，给予其等量的护盾，并增加此范围内所有人 %d%% 治疗效果。此效果持续 %d 回合。
		如果已经存在护盾，则护盾将会增加等量数值，如果护盾持续时间不足 2 回合，会延长至 2 回合。
		当同一个护盾被刷新 20 次后，将会因为不稳定而破碎。
		它同时会照亮此区域。
		治疗量受魔力值加成。
```

## entry-01535
位置：mod-tome.lua:21456；section：mod-tome/data/talents/celestial/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Explodes (radius 1) for %d light damage.
```
译文：
```text
爆炸（范围 1）造成 %d 光系伤害。
```

## entry-01536
位置：mod-tome.lua:21483；section：mod-tome/data/talents/celestial/radiance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are so infused with sunlight that your body glows permanently in radius %d, even in dark places.
		Your vision and body adapt to this glow, giving you %d%% blindness resistance, %d%% light resistance, and %d%% light affinity.
		The light radius overrides your normal light if it is bigger (it does not stack).
		
```
译文：
```text
你的体内充满了阳光，即使身处黑暗之中，身体也会永久发出半径 %d 的光芒。
		你的眼睛和身体适应了光明，获得 %d%% 目盲免疫，%d%% 光系抗性和 %d%% 光系伤害亲和。
		光照超过你的灯具时取代之，不与灯具叠加光照。
		
```

## entry-01537
位置：mod-tome.lua:21502；section：mod-tome/data/talents/celestial/radiance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The light of your Radiance allows you to see that which would normally be unseen and strike that which would normally be protected.
		All enemies in your Radiance aura have their invisibility and stealth power reduced by %d; all actors affected by illumination have their defense reduced by %d as well as all evasion bonuses from being unseen negated.
		In addition, your light damage is increased by %d%% and your strikes ignore %d%% of the light resistance of your targets.
		The invisibility, stealth power, and defense reductions increase with your Spellpower.
```
译文：
```text
光辉可以让你看到平时无法见到的敌人，并攻击被保护的敌人。
		在光辉光环的影响下的敌人，其隐形和潜行强度降低 %d。所有被光照的目标，闪避值降低 %d，且不受不可见带来的闪避加成影响。
		此外，你的光系伤害增加 %d%%，你的攻击无视敌人 %d%% 的光系伤害抗性。
		隐形、潜行强度和闪避值降低效果受法术强度加成。
```

## entry-01538
位置：mod-tome.lua:21534；section：mod-tome/data/talents/celestial/sun.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Calls forth a ray of light from the Sun, doing %0.1f Light damage to the target.
		At level 3 the ray will be so intense it will also blind the target and everyone in a radius 2 around it for %d turns.
		The damage dealt will increase with your Spellpower.
```
译文：
```text
召唤太阳之力，形成一道射线，造成 %0.1f 点光系伤害。
		等级 3 时射线变得如此强烈，目标及其周围半径 2 以内的所有单位将被致盲 %d 回合。
		伤害受法术强度加成。
```

## entry-01539
位置：mod-tome.lua:21540；section：mod-tome/data/talents/celestial/sun.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A path of sunlight appears in front of you for 5 turns. All foes standing inside take %0.1f Light damage per turn.
		While standing in the path, your movement takes no time and can not trigger traps.
		The damage done will increase with your Spellpower.
```
译文：
```text
在你面前出现一条阳光大道，持续 5 回合。任何站在上面的敌人每回合受到 %0.1f 点光系伤害。
		你站在上面行走不消耗时间，也不会触发陷阱。
		伤害受法术强度加成。
```

## entry-01540
位置：mod-tome.lua:21556；section：mod-tome/data/talents/celestial/sun.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You wrap yourself in a cloak of sunlight that empowers your magic and protects you for 6 turns.
		While the cloak is active, your spell casting speed is increased by %d%%, your spell cooldowns are reduced by %d%%, and you cannot take more than %d%% of your maximum life from a single blow.
		The effects will increase with your Spellpower.
```
译文：
```text
你将自己包裹在阳光中，增强你的魔法并保护你 6 回合。
		你的施法速度增加 %d%%，法术冷却减少 %d%%，同时一次攻击不能对你造成超过 %d%% 最大生命的伤害。
		效果受法术强度加成。
```

## entry-01541
位置：mod-tome.lua:21597；section：mod-tome/data/talents/celestial/twilight.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instantly travel to your jumpgate, as long as you are within %d tiles of it.
```
译文：
```text
在 %d 格范围以内你可以立即传送至你的跃迁之门。
```

## entry-01542
位置：mod-tome.lua:21606；section：mod-tome/data/talents/celestial/twilight.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Let out a mental cry that shatters the will of your targets within radius %d, dealing %0.2f darkness damage and confusing (%d%% to act randomly) them for %d turns.
		The damage will improve with your spellpower and the duration will improve with your Cunning.
```
译文：
```text
在 %d 码半径范围内释放一股精神冲击，摧毁目标的意志，对其造成 %0.2f 暗影伤害，并使其混乱 (%d%% 几率随机行动)，持续 %d 回合。
		伤害受法术强度加成，持续时间受灵巧加成。
```

## entry-01543
位置：mod-tome.lua:21610；section：mod-tome/data/talents/celestial/twilight.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01544
位置：mod-tome.lua:21621；section：mod-tome/data/talents/celestial/twilight.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Create a second shadow jumpgate at your location. As long as you sustain this spell, you can use 'Jumpgate: Teleport' to instantly travel to the jumpgate, as long as you are within %d tiles of it.
```
译文：
```text
在你当前位置创造第二个暗影跃迁之门。只要你维持本法术，便可使用「跃迁之门II：传送」立即传送至该跃迁之门，只要你在其 %d 码范围内。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Celestial	天空系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Hymn of Detection	侦测圣诗	T.GAME.TALENT	talents	talent name	preferred	core	月亮圣诗技能；提高潜行与隐形侦测、允许无惩罚攻击不可见目标并强化暴击伤害，统一技能名及圣诗入门/专家中的引用
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Negative energy	负能量	T.GAME.RESOURCE	combat	_t	preferred	core	星空法师/死亡赞歌职业资源；与 Positive energy 正能量区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
celestial	天空	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
cleanse	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key，与 cleansing keyword 同一 cohort；不约束动作、技能说明或其他语境
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
dirge	挽歌	T.GAME.EFFECT	combat	effect subtype	preferred	core	稳定版 1.7.6 的魔法持续效果名称
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
illumination	照明	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
