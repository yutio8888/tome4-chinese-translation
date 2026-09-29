# batch-070：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02188
位置：mod-tome.lua:28416；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The targetted teleport fizzles and works randomly!
```
译文：
```text
传送定位失败了，变为随机传送！
```

## entry-02189
位置：mod-tome.lua:28417；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Teleports you randomly within a large range (%d).
		At level 4, it allows you to specify which creature to teleport.
		At level 5, it allows you to choose the target area (radius %d).
		If the target area is not in line of sight, there is a chance the spell will partially fail and teleport the target randomly.
		Random teleports have a minimum range of %d.
		The range will increase with your Spellpower.
```
译文：
```text
在 %d 码范围内随机传送。
		在等级 4 时，你可以传送指定生物（怪物或被护送者）。
		在等级 5 时，你可以选择传送位置（半径 %d）。
		如果目标位置不在你的视线里，则法术有可能失败，变为随机传送。
		随机传送的最小半径为 %d。
		影响范围受法术强度加成。
```

## entry-02190
位置：mod-tome.lua:28429；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
This intricate spell erects a space distortion around the caster that is linked to another distortion, placed around a target.
		Any time the caster should take damage, there is a %d%% chance that it will instead be warped by the shield and hit the designated target.
		Once the maximum damage (%d) is absorbed, the time runs out (%d turns), or the target dies, the shield will crumble.
		The max damage the shield can absorb will increase with your Spellpower.
```
译文：
```text
这个复杂的法术可以扭曲施法者周围的空间，此空间可连接至范围内的另外 1 个目标。
		任何时候，施法者所承受的伤害有 %d%% 的概率转移给指定连接的目标。
		一旦吸收伤害达到上限（%d），持续时间到了（%d 回合）或目标死亡，护盾会破碎掉。
		护盾的伤害最大吸收值受法术强度加成。
```

## entry-02191
位置：mod-tome.lua:28437；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you hit a solid surface, this spell tears down the laws of probability to make you instantly appear on the other side.
		Teleports up to %d grids.
		After a successful probability travel you are left unstable, unable to do it again for a number of turns equal to %d%% of the number of tiles you blinked through.
		The range will improve with your Spellpower.
```
译文：
```text
当你击中一个固体表面时，此法术撕碎概率法则，令你瞬间出现在另一面。
		传送最大距离为 %d 码。
		成功穿越后，你会陷入不稳定状态，在相当于穿越码数 %d%% 的回合内无法再次穿越。
		传送距离受法术强度加成。
```

## entry-02192
位置：mod-tome.lua:28450；section：mod-tome/data/talents/spells/death.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Press your advantage when your foes are starting to crumble.
		For every detrimental effect on the target you deals %0.2f frostdusk damage (with diminishing returns) and reduce its global speed by 25%% for one turn per effect (up to a maximum of %d).
		The diminishing returns on damage bonus works this way:
		- 2 effects: %0.2f
		- 5 effects: %0.2f
		- 10 effects: %0.2f
		- 15 effects: %0.2f
		And so on...
		Damage increases with your Spellpower.
		
```
译文：
```text
利用敌人的痛楚打击敌人。
		目标每具有一个负面效果，造成 %0.2f 霜暮伤害（有收益衰减），并降低其全局速度 25%% 1回合（最大 %d 回合）。
		伤害加成的收益衰减如下面所示：
		- 2 个效果：%0.2f 伤害
		- 5 个效果：%0.2f 伤害
		- 10 个效果：%0.2f 伤害
		- 15 个效果：%0.2f 伤害
		以此类推。
		伤害受法术强度加成。
		
```

## entry-02193
位置：mod-tome.lua:28477；section：mod-tome/data/talents/spells/death.lua；source_tag：tformat；args_order：[1, 2, 3, 5, 4]；special：None

原文：
```text
Your body starts to radiate shadows, increasing your darkness resistance by %d%%, armour by %d and defence by %d.
		Any time you absorb a soul the shadows pulse outward, dealing %0.2f frostdusk damage to all foes in range %d and knocking them back 3 tiles.
		This can only happen once per turn.
		The damage increases with your Spellpower.
```
译文：
```text
你的身体开始散发暗影，获得 %d%% 暗影抗性，%d 护甲值和 %d 闪避值。
		每当吸收灵魂，你体内的黑暗会放射出来，对范围 %d 内所有敌人造成 %0.2f 霜暮伤害，并将其击退 3 格。
		这一效果每回合最多触发一次。
		伤害受法术强度提升。
```

## entry-02194
位置：mod-tome.lua:28496；section：mod-tome/data/talents/spells/deeprock.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You call upon the very core of the world, harnessing its power to transform your body.
		For %d turns you become a Deeprock Elemental, gaining two size categories%s.
		This increases your Physical damage by %0.1f%% and Physical damage penetration by %0.1f%%%s, and armour by %d.%s
		The effects increase with spellpower.
```
译文：
```text
你呼唤世界深层的核心之力，用来改造自己的身体。
		%d 回合内，你将变成深岩元素形态，增加 2 点体型 %s。
		同时，你将增加 %0.1f%% 物理伤害和 %0.1f%% 物理抗性穿透 %s，并获得 %d 点护甲。%s
		效果受法术强度加成。
```

## entry-02195
位置：mod-tome.lua:28507；section：mod-tome/data/talents/spells/deeprock.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you turn into a Deeprock elemental your Arcane damage is increased by %0.1f%%, Arcane damage penetration by %0.1f%% and you gain the power to invoke volcanos:
		%s
```
译文：
```text
当你进入深岩元素形态时，增加 %0.1f%% 奥术伤害和 %0.1f%% 奥术抗性穿透，同时获得激发火山的能力：
		%s
```

## entry-02196
位置：mod-tome.lua:28511；section：mod-tome/data/talents/spells/deeprock.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you turn into a Deeprock elemental your Nature damage is increased by %0.1f%%, Nature damage penetration by %0.1f%% and you gain the power to throw boulders:
		%s
```
译文：
```text
当你进入深岩元素形态时，增加 %0.1f%% 自然伤害和 %0.1f%% 自然抗性穿透，同时获得投掷巨石的能力：
		%s
```

## entry-02197
位置：mod-tome.lua:28545；section：mod-tome/data/talents/spells/divination.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Form a map of your surroundings in your mind in a radius of %d
```
译文：
```text
通过意念探测周围地形，有效范围：%d 码。
```

## entry-02198
位置：mod-tome.lua:28627；section：mod-tome/data/talents/spells/eldritch-shield.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Eldritch Blow without a shield!
```
译文：
```text
没有盾牌，无法使用奥术盾击！
```

## entry-02199
位置：mod-tome.lua:28646；section：mod-tome/data/talents/spells/eldritch-shield.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Eldricth Fury without a shield!
```
译文：
```text
没有盾牌无法使用奥术连击！
```

## entry-02200
位置：mod-tome.lua:28647；section：mod-tome/data/talents/spells/eldritch-shield.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the dazing blows!
```
译文：
```text
%s抵抗了眩晕打击！
```

## entry-02201
位置：mod-tome.lua:28654；section：mod-tome/data/talents/spells/eldritch-shield.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Eldritch Slam without a shield!
```
译文：
```text
没有盾牌就无法使用奥术猛击！
```

## entry-02202
位置：mod-tome.lua:28667；section：mod-tome/data/talents/spells/eldritch-stone.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
poisoned for %0.1f Nature damage over 6 turns (%d%% healing reduction)
```
译文：
```text
中毒 6 回合受到合计 %0.1f 点自然伤害（同时减少 %d%% 治疗效果）
```

## entry-02203
位置：mod-tome.lua:28699；section：mod-tome/data/talents/spells/energy-alchemy.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is energized by the attack, reducing some talent cooldowns!
```
译文：
```text
%s被这次攻击充能，减少了部分技能冷却时间！
```

## entry-02204
位置：mod-tome.lua:28700；section：mod-tome/data/talents/spells/energy-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While Lightning Infusion is active, your bombs energize your golem.
		All talents on cooldown on your golem have %d%% chance to be reduced by %d.
```
译文：
```text
当闪电充能开启时，你的炸弹会给傀儡充能。
		你的傀儡的所有冷却中技能有 %d%% 概率减少 %d 回合冷却时间。
```

## entry-02205
位置：mod-tome.lua:28704；section：mod-tome/data/talents/spells/energy-alchemy.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You need to ready alchemist gems in your quiver.
```
译文：
```text
你需要在箭袋中装填炼金宝石。
```

## entry-02206
位置：mod-tome.lua:28705；section：mod-tome/data/talents/spells/energy-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
By crushing an alchemist gem you generate a thunderclap in a cone of radius %d dealing %0.2f physical damage and %0.2f lightning damage.
		All creatures caught inside are knocked back and disarmed for %d turns.
		The duration and damage will increase with your Spellpower.
```
译文：
```text
粉碎一颗炼金宝石，制造一次闪电霹雳，在半径 %d 的锥形区域内造成 %0.2f 点物理伤害和 %0.2f 点闪电伤害。
		范围内的生物将会被击退并被缴械 %d 回合。
		伤害和持续时间受法术强度加成。
```

## entry-02207
位置：mod-tome.lua:28713；section：mod-tome/data/talents/spells/energy-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Infuse your body with lightning energy, bolstering your movement speed by +%d%%.
		Each turn, a foe within range %d will be struck by lightning and be dealt %0.1f Lightning damage.
		In addition, damage to your health will energize you.
		At the start of each turn in which you have lost at least %d life (20%% of your maximum life) since your last turn, you will gain %d%% of a turn.
		The effects increase with your Spellpower.
```
译文：
```text
将闪电能量填充到身体中，增加 %d%% 移动速度。
		每回合半径 %d 内的一个敌人将会被闪电击中，造成 %0.1f 点闪电伤害。
		另外，对你的伤害会激活你。
		每次你的回合开始时，如果自上个回合以来你损失了至少 %d 点生命（20%% 最大生命值），你将获得 %d%% 个额外回合。
		上述效果均随法术强度提升。
```

## entry-02208
位置：mod-tome.lua:28780；section：mod-tome/data/talents/spells/eradication.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with Frostdusk, increasing all your darkness and cold damage by %0.1f%%, and ignoring %d%% of the darkness and cold resistance of your targets.
		At the end of each turn if you are under 1 life you are healed for %d%% of all damage you dealt.
```
译文：
```text
使用霜暮的力量覆盖全身，增加 %0.1f%% 暗影和寒冷伤害，并无视目标 %d%% 的暗影和寒冷抗性。
		此外，若你生命值少于1点，你造成的伤害会在回合结束时以 %d%% 比例治疗自身。
```

## entry-02209
位置：mod-tome.lua:28788；section：mod-tome/data/talents/spells/explosives.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You need to ready alchemist gems in your quiver.
```
译文：
```text
你需要在箭袋中装填炼金宝石。
```

## entry-02210
位置：mod-tome.lua:28797；section：mod-tome/data/talents/spells/explosives.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Grants %d%% protection to you, your golem and other friendly creatures against the elemental damage of your own bombs, and against external elemental damage (fire, cold, lightning and acid) by %d%%.
		At talent level 5 it also protects against all side effects of your bombs.
```
译文：
```text
提高你、你的傀儡和其他友好生物对自己炸弹 %d%% 的元素伤害抗性，并增加 %d%% 对外界元素伤害（火焰、寒冷、闪电和酸性）的抗性。
		在技能等级 5 时它同时会保护你免疫你的炸弹所带来的特殊效果。
```

## entry-02211
位置：mod-tome.lua:28801；section：mod-tome/data/talents/spells/explosives.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your alchemist bombs now affect a radius of %d around them.
		Explosion damage may increase by %d%% (if the explosion is not contained) to %d%% if the area of effect is confined.
```
译文：
```text
炼金炸弹的爆炸半径现在为 %d 码。
		增加 %d%% （地形开阔）～ %d%% （地形狭窄）爆炸伤害。
```

## entry-02212
位置：mod-tome.lua:28848；section：mod-tome/data/talents/spells/fire.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Flame
```
译文：
```text
火焰
```

## entry-02213
位置：mod-tome.lua:28849；section：mod-tome/data/talents/spells/fire.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures up a bolt of fire, setting the target ablaze and doing %0.2f fire damage over 3 turns.
		At level 5, it will create a beam of flames.
		The damage will increase with your Spellpower.
```
译文：
```text
制造一道火焰弹，使目标进入灼烧状态并在 3 回合内造成 %0.2f 火焰伤害。
		在等级 5 时，它会变为一道贯穿的火焰光束。
		伤害受法术强度加成。
```

## entry-02214
位置：mod-tome.lua:28884；section：mod-tome/data/talents/spells/frost-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Invoke a blast of cold all around you with a radius of %d, doing %0.1f Cold damage and freezing creatures to the ground for %d turns.
		Affected creatures can still act, but cannot move.
		The duration will increase with your Spellpower.
```
译文：
```text
在半径 %d 的范围内激发寒冰能量，造成 %0.1f 点寒冷伤害，同时将周围的生物冻结在地面上 %d 个回合。
		受影响的生物能够行动，但不能移动。
		持续时间受法术强度加成。
```

## entry-02215
位置：mod-tome.lua:28890；section：mod-tome/data/talents/spells/frost-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Turn your body into pure ice, increasing your Cold damage affinity by %d%% and your physical resistance by %d%%.
		You have a %d%% chance to shrug off all direct critical hits (physical, mental, spell).
		The effects increase with your Spellpower.
```
译文：
```text
将你的身体转化为纯净的寒冰体，你受到的寒冰伤害的 %d%% 会治疗你，同时你的物理抗性增加 %d%%。
		你有 %d%% 几率摆脱暴击伤害（物理，精神，法术）。
		效果受法术强度加成。
```

## entry-02216
位置：mod-tome.lua:28945；section：mod-tome/data/talents/spells/golem.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# provokes #Target# to attack it.
```
译文：
```text
#Source#强制#Target#攻击它。
```

## entry-02217
位置：mod-tome.lua:28948；section：mod-tome/data/talents/spells/golem.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the crushing!
```
译文：
```text
%s抵抗了压碎！
```

## entry-02218
位置：mod-tome.lua:28976；section：mod-tome/data/talents/spells/golem.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Target# is pulled toward #Source#!
```
译文：
```text
#Target#被拉向#Source#！
```

## entry-02219
位置：mod-tome.lua:28979；section：mod-tome/data/talents/spells/golem.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Turns the golem's skin into molten rock. The heat generated sets ablaze everything inside a radius of 3, doing %0.2f fire damage in 3 turns for %d turns.
		Burning is cumulative; the longer they stay within range, they higher the fire damage they take.
		In addition the golem gains %d%% fire resistance.
		Molten Skin damage will not affect friendly creatures.
		The damage and resistance will increase with your Spellpower.
```
译文：
```text
使傀儡的皮肤化为熔岩。产生的高温会点燃半径 3 格内的一切，使其在 3 回合内受到 %0.2f 点火焰伤害；炽热皮肤持续 %d 回合。
		灼烧可以叠加；目标处于范围内越久，受到的火焰伤害越高。
		此外，傀儡获得 %d%% 火焰抗性。
		炽热皮肤的伤害不会影响友方生物。
		伤害和抗性随你的法术强度提高。
```

## entry-02220
位置：mod-tome.lua:28989；section：mod-tome/data/talents/spells/golem.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The golem self-destructs, destroying itself and generating a blast of fire in a radius of %d, doing %0.2f fire damage.
		This spell is only usable when the golem's master is dead.
```
译文：
```text
傀儡引爆自己，摧毁傀儡并产生一个火焰爆炸，%d 码有效范围内造成 %0.2f 火焰伤害。
		这个技能只有傀儡的主人死亡时能够使用。
```

## entry-02221
位置：mod-tome.lua:28995；section：mod-tome/data/talents/spells/golem.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The golem automatically reconfigures heavy mail and massive armours designed for living creatures to protect its own vital areas.
	%s armour value by %d, armour hardiness by %d%%, and provides %d%% critical hit reduction when wearing heavy mail or massive armour.
```
译文：
```text
傀儡学会重新组装重甲和板甲，以便更加适用于傀儡。
	当装备重甲或板甲时，%s护甲 %d 点，护甲强度 %d%%，并且减少 %d%% 被暴击率。
```

## entry-02222
位置：mod-tome.lua:29000；section：mod-tome/data/talents/spells/golem.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Breathe poison on your foes, doing %d damage over a few turns.
		The damage will increase with your Magic.
```
译文：
```text
对你的敌人喷吐毒雾，在几个回合内造成 %d 点伤害。伤害受魔力值加成。
```

## entry-02223
位置：mod-tome.lua:29032；section：mod-tome/data/talents/spells/golemancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Improves your golem's proficiency with weapons, increasing its Accuracy by %d, Physical Power by %d and damage by %d%%.
```
译文：
```text
提高傀儡的武器熟练度，增加它 %d 点命中、%d 物理强度和 %d%% 伤害。
```

## entry-02224
位置：mod-tome.lua:29067；section：mod-tome/data/talents/spells/grave.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You summon a corpselight that radiates cold for 7 turns in radius %d.
		Every turn all foes inside take %0.2f cold damage.
		Anytime you cast a spell while standing inside your corpselight's area it grows by one stack, each stack giving +1 radius and +10%% damage.
		The corpselight can gain at most %d stacks and the radius will never extend beyond 10.
		If cast while under 1 life it spawns with 3 stacks.
		The damage will increase with your Spellpower.
```
译文：
```text
你召唤一个半径为 %d 的鬼火，散发出刺骨的尸寒，持续 7 回合。
		在每个回合内，每个被鬼火覆盖的敌人会受到 %0.2f 寒冷伤害。
		每当你在鬼火的范围内施放法术，它会强化一层，每一层增长半径 1，伤害增加 10%%。
		鬼火最多可以叠加强化 %d 层，且半径最大为 10。
		如果在生命值为 1 以下时使用技能，鬼火初始强度为 3 层。
		伤害受法术强度加成。
```

## entry-02225
位置：mod-tome.lua:29079；section：mod-tome/data/talents/spells/grave.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#STEEL_BLUE#The corpselight implodes!
```
译文：
```text
#STEEL_BLUE#鬼火爆炸了！
```

## entry-02226
位置：mod-tome.lua:29080；section：mod-tome/data/talents/spells/grave.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Upon expiring the corpselight implodes, pulling in all foes towards its center and dealing %0.2f cold damage.
		The damage is increased by +10%% per stack.
		The damage will increase with your Spellpower.

		#PURPLE#Learning this spell will make Corpselight cost two souls to use instead of one.
```
译文：
```text
你的鬼火消失时会发生爆炸，将所有敌人拖向中心位置，并造成 %0.2f 寒冷伤害。
		鬼火每叠加一层，伤害增加 10%%。
		伤害受法术强度加成。

		#PURPLE#学习这一技能会把你阴燃鬼火消耗的灵魂数量从 1 增加到 2。
```

## entry-02227
位置：mod-tome.lua:29143；section：mod-tome/data/talents/spells/master-necromancer.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sends out a surge of undeath energies into your aura.
		All minions inside gain 25%% speed for %d turns
		All non-ghoul minions are healed by %d%%.
		If you know Call of the Mausoleum, the time remaining to the next free ghoul is reduced by %d.
		if you know Corpse Explosion or Putrescent Liquefaction the duration of those effects are increased by %d.
		All non-undead foes caught inside are dazed for %d turns.
		In addition all your minions (created after you learn this spell) have a passive health regeneration.
```
译文：
```text
在你的光环中放出一股不死能量。
		范围内所有随从获得 25%% 速度，持续 %d 回合。
		所有非食尸鬼的随从被治疗 %d%%。
		如果你掌握陵墓召唤技能，到下一个免费食尸鬼的时间降低 %d。
		如果你掌握夺命尸爆或腐烂液化技能，这些效果的持续时间延长 %d。
		范围内所有非不死生物的敌人都会被茫然 %d 回合。
		此外，你的所有随从（在学会该法术后制造的）获得额外被动生命回复。
```

## 相关术语快照
```tsv
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Probability Travel	次元移动	T.GAME.TALENT	talents	talent name	preferred	core	时空系概率旅行技能；通过概率效应穿越墙壁，统一技能名、状态名及异常名称，不写作“相位移动”或直译为“概率移动”
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armours	护甲	T.GAME.ENTITY	items	nil	existing	core	复数实体类别
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
eldritch	骇异	T.GAME.ENTITY	creatures	entity subtype	preferred	global	1.8beta 在核心和 Cults of Entropy 中统一使用；专名（Eldritch eye 艾尔德里奇之眼、Eldritch Channeler 埃尔德里奇主宰者）保留音译
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
