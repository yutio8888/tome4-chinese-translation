# batch-125：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03913
位置：tome-orcs.lua:4573；section：tome-orcs/data/talents/steam/automated-butchery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You override all security measures of your tinkers, allowing you to reset the cooldown of %d of most of your steamtech talents of tier %d or less and instantly increases your steam level by %d%% of the maximum.
		In addition for 6 turns your maximum steam capacity is doubled, but steam regeneration is halved.
		#{italic}#Master of Tech, Master of Death!#{normal}#
```
译文：
```text
你开启全部插件的超频模式，重置最多 %d 个蒸汽科技技能（%d 层级或以下）的冷却时间，直接恢复 %d%% 蒸汽值。
		在 6 回合内，蒸汽值最大值翻倍，但是恢复值减半。
		#{italic}#科技至尊、死亡之主！！#{normal}#
```

## entry-03914
位置：tome-orcs.lua:4625；section：tome-orcs/data/talents/steam/avoidance.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s activates %s cloak's restoration systems!
```
译文：
```text
%s激活了%s披风的恢复系统！
```

## entry-03915
位置：tome-orcs.lua:4687；section：tome-orcs/data/talents/steam/battlefield-management.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Firmly plant your steamsaws in the ground, using them to propel yourself very quickly (+%d%% movement speed).
		Any foes on either side of your movement get wrecked by the saws, knocking them 3 tiles away from you.
		Attacking or using any talent will break this effect.
		When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage to all foes around you. To do full damage you need to have moved at least 5 times, otherwise damage is lower (or null for no movement).
		#{italic}#The wheels of death! Amazing!#{normal}#
```
译文：
```text
把链锯深深插入地面，作为履带，增强自己的行动能力（移动速度增加 %d%%）。
		在你移动路线两侧的敌人被链锯割断，被击退 3 码。
		攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成 %d%% 武器伤害。你需要至少移动五次来达到最高伤害，否则伤害会降低。若不移动则没有伤害。
		#{italic}#冲锋！死亡之轮！！#{normal}#
```

## entry-03916
位置：tome-orcs.lua:4727；section：tome-orcs/data/talents/steam/blacksmith.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Working long hours at a forge has made you incredibly slow to tire and given you endless vitality.
		Your healing factor is increased by %d%% and your life regeneration by %0.2f.
		Stopping you is nearly impossible; your pinning resistance is increased by %d%%.
```
译文：
```text
长时间的锻造工作让你拥有不可思议的持久力和无尽的活力。
		你的治疗系数增加 %d%%，生命恢复增加 %0.2f。
		你力大无穷，很难被阻止，定身抗性增加 %d%%。
```

## entry-03917
位置：tome-orcs.lua:4788；section：tome-orcs/data/talents/steam/butchery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Continuously swing your steamsaws around you, dealing %d%% weapon damage to adjacent foes each time you attack.
		Your chaotic motions make it difficult for anything to hit you, granting %d%% chance to completely negate all damage.
		Damage avoidance chance increases with Steampower.
		#{italic}#Make the metal talk!#{normal}#
```
译文：
```text
持续挥舞你的链锯，每次你攻击时对周围敌人造成 %d%% 武器伤害。
		你狂乱的动作使你很难被命中，%d%% 几率无视伤害。
		伤害无效概率随蒸汽强度提高。
		#{italic}#感受金属之怒吧！！#{normal}#
```

## entry-03918
位置：tome-orcs.lua:4796；section：tome-orcs/data/talents/steam/butchery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You temporarily overcharge the saw motors, increasing the effective talent level of all saw talents by %d%% for %d turns.
		#{italic}#The pain shall never stop!#{normal}#
```
译文：
```text
链锯引擎临时进入过载模式，增加 %d%% 的链锯相关技能有效等级，持续 %d 回合。
		#{italic}#无尽地痛苦#{normal}#
```

## entry-03919
位置：tome-orcs.lua:4822；section：tome-orcs/data/talents/steam/chemical-warfare.lua；source_tag：tformat；args_order：[2, 1, 3, 4]；special：None

原文：
```text
You consume all Miasma Engine stacks you have to fire a blast of corrosive death through your steamgun, dealing %d%% weapon damage as acid in a radius %d cone with a %d%% chance to remove a random beneficial physical or mental effect. For every stack beyond the first the damage dealt is increased by 50%% and there is a %d%% chance to remove an additional effect.
		This attack ignores all enemy armour, and you must have at least 1 stack of Miasma Engine to use this talent.
```
译文：
```text
你消耗所有瘴气引擎的叠加效果，并用你的蒸汽枪发射出毁灭性的腐蚀爆炸，在 %d 码范围的扇形区域内造成 %d%% 酸性武器伤害，并有 %d%% 的几率移除一个随机的有益物理或精神效果。你瘴气引擎叠加的层数每超过一层，则增加 50%% 伤害，并有 %d%% 几率额外移除一个效果。
		这一攻击无视敌人护甲，你至少需要有一层瘴气引擎效果才能使用这个技能。
```

## entry-03920
位置：tome-orcs.lua:4857；section：tome-orcs/data/talents/steam/demolition.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You mount a grenade launcher on your steamgun that launches high explosive rounds. Each time you make a basic attack with your steamgun or a heavy weapon, you fire a grenade at the target that explodes for %d%% steamgun damage in radius %d.
		This talent also reinforces the armor of you and your minions to give you immunity to your own grenades.
		You can only fire a single grenade once every 9 turns.
```
译文：
```text
你在蒸汽枪上安装一个发射高爆弹的榴弹发射器。每当你用蒸汽枪进行普通攻击或使用重装武器攻击时，都会向目标发射一枚榴弹，造成 %d%% 蒸汽枪伤害，作用半径 %d 码。
		此技能还会强化你和随从的护甲，使你与随从免疫你自己发射的榴弹。
		每 9 回合只能发射一枚榴弹。
```

## entry-03921
位置：tome-orcs.lua:4930；section：tome-orcs/data/talents/steam/elusiveness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The thrill of the hunt invigorates you. For each foe in radius %d around you, you gain 20%% movement speed (up to %d%%).
		Current bonus: %d%%.
```
译文：
```text
被猎杀的危险令你激动不已。
		半径 %d 内每有一个敌人，你获得 20%% 移动速度（最多 %d%%）。
		当前加成：%d%%。
```

## entry-03922
位置：tome-orcs.lua:4945；section：tome-orcs/data/talents/steam/elusiveness.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While your foes are distracted by your Awesome Toss, you use powerful steam motors to jump into the air and kick a target %d tiles away.
		The impact is so great that it ripples outwards, slowing all creatures in radius 3 by %d%% for 4 turns while the reaction force propels you %d tiles backwards.
```
译文：
```text
当你的敌人被致命翻转吸引时，你启动强力的蒸汽引擎，跳向空中，将目标踢走 %d 码。
		这次攻击冲击力非常大，半径 3 以内所有生物将被减速 %d%%，持续 4 回合。
		反冲力也让你后退 %d 码。
```

## entry-03923
位置：tome-orcs.lua:4954；section：tome-orcs/data/talents/steam/engineering.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You open all steam valves at once, releasing a radius %d wave of superheated steam around yourself which deals %0.2f fire damage (but can not be a critical hit).
		If you had at least 35 steam, the vapours will be so hot that they can burn sensory organs, blinding affected creatures for %d turns.
		The effects scale with your current steam value; at 1 steam they are only 15%% as effective as at 50 or more (current factor %d%%).
```
译文：
```text
你打开所有蒸汽阀，释放半径 %d 的蒸汽冲击波，造成 %0.2f 火焰伤害。（这一技能无法暴击）
		若你有至少 35 点蒸汽，气体的温度将变得极高，能烧伤感知器官，令受影响的生物目盲 %d 回合。
		效果受当前蒸汽值加成。1 点蒸汽值时，强度仅为 50 或更高点蒸汽值的 15%%。
		当前强度系数 %d%%。
```

## entry-03924
位置：tome-orcs.lua:4969；section：tome-orcs/data/talents/steam/engineering.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Sometimes, being a master tinker requires taking risks; yours are more calculated than others.
		Gain %d cunning, %d physical save, %d%% resistance to self-inflicted damage, and %d%% chance to avoid being critically hit.
```
译文：
```text
成为大师意味着你经历了更多危险，你的计算力也超越凡人。
		增加 %d 灵巧，%d 物理豁免，%d%% 自身伤害抗性，%d%% 几率避免暴击。
```

## entry-03925
位置：tome-orcs.lua:4985；section：tome-orcs/data/talents/steam/furnace.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While Furnace is on your armour is so hot from the furnace it dissipates parts of all energy based attacks against you.
		All non physical, non mind damage is reduced by %d (current %d).
		Each turn this happens you gain a molten point (up to 10), decreasing the efficiency of the reduction by 25%%.
		Molten points are removed upon running or resting.
		#{italic}#Hot liquid metal, the fun!#{normal}#
		
```
译文：
```text
你的护甲温度极高，能驱散部分能量攻击。
		所有非物理、非精神伤害降低 %d 点（当前 %d）。
		每回合该效果触发时，你获得 1 点融化点数（最多 10 点），使减伤效率降低 25%%。
		奔跑或休息时会清除融化点数。
		#{italic}#火热的液态金属，乐趣无穷！#{normal}#
		
```

## entry-03926
位置：tome-orcs.lua:5007；section：tome-orcs/data/talents/steam/furnace.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you reach 10 molten points your armour overheats, reaching temperatures so high that they cauterize up to %d detrimental physical effects on you.
		A special medical injector injects you with a fire immunity serum at that precise moment to make you immune to the burning effect.
		When this happens all molten points are consumed and trigger a Furnace Vent at the creature that triggered the last molten point.
		This effect drains 15 steam when triggered, and will not trigger if steam is too low.
		#{italic}#It's only a flesh burn!#{normal}#
		
```
译文：
```text
当你达到 10 点融化点数时，你的护甲过热，温度极高，以至于 %d 个负面物理状态被高温驱散。
		同时，一个特殊的医疗注射器会为你注射火焰免疫血清，令你免疫烧伤效果。
		该效果触发时，消耗所有融化点数，并自动对最后一次提供融化点数的生物触发一次通风孔效果。
		该效果将消耗 15 点蒸汽。蒸汽不足时不能触发。
		#{italic}#只是肉体在燃烧！#{normal}#
		
```

## entry-03927
位置：tome-orcs.lua:5023；section：tome-orcs/data/talents/steam/gadgets.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You link your weapons and shield to your steam generators, using them to load ammunition and improve the power of your weapons. 
		Each time you fire your Steamgun, you have a %d%% chance to reload 1 Heavy Weapon ammo.
		Each time you fire a Heavy Weapon you reload %d ammo.
		Each time you raise your shield to block, you reload 1 Heavy Weapon ammo.
		This also increases weapon damage by %d%% and Physical Power by 30 when using steamguns or heavy weapons.
		In addition, your steamgun and heavy weapon shots now bypass friendly targets harmlessly.
```
译文：
```text
你将武器和盾牌连接到蒸汽机，使用它们来为你的武器填充弹药，并强化武器的能力。
		每当你使用蒸汽枪射击的时候，有 %d%% 的几率填充一枚重装武器的弹药。
		每当你使用重装武器射击的时候，会填充 %d 枚弹药。
		每当你使用盾牌格挡的时候，会填充一枚重装武器的弹药。
		这一技能也会在你使用蒸汽枪或重装武器的时候提升武器伤害 %d%%，提升物理强度 30。
		另外，你的蒸汽枪和重装武器射击可以安全地穿过友方目标。
```

## entry-03928
位置：tome-orcs.lua:5036；section：tome-orcs/data/talents/steam/gadgets.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Current exoskeleton life: %d/%d
		You craft a set of steam powered armor that fits over your regular armor, enhancing your defense. The armor has %d life, and 50%% of all damage taken is redirected to it.
		Your powered armour repairs 5%% of it’s maximum life each turn, and each time you spend steam it will be repaired for %d%% of the steam cost.
		The armor's maximum life will increase with your Steampower.
```
译文：
```text
当前机械外骨骼生命值：%d / %d
		你制造一台蒸汽驱动的机械外骨骼，可以装载在你平常的护甲外面，增强你的防御能力。机械外骨骼具有 %d 生命值，你受到的所有伤害的 50%% 会转移到它身上。
		你的机械外骨骼每回合会修复 5%% 的最大生命值，每当你消耗蒸汽的时候，他也会修复相当于蒸汽值消耗 %d%% 的生命值。
		外骨骼的最大生命值受蒸汽强度加成。
```

## entry-03929
位置：tome-orcs.lua:5048；section：tome-orcs/data/talents/steam/gadgets.lua；source_tag：tformat；args_order：[1, 3, 2]；special：None

原文：
```text
Prepare a defensive device that stores an electrical charge for 8 turns.
If your life falls below 0 while the AED is active it will activate to shock you back into life, negating the triggering attack, restoring %d life and dealing %0.2f lightning damage in radius %d that dazes affected enemies for 3 turns.
If the AED does not activate, the cooldown is reduced by 15 turns.
The healing and damage will increase with your Steampower.
```
译文：
```text
准备好一个防御性的设备，其电力可以持续 8 回合。
当你的生命值降到 0 点以下的时候，电击除颤器会启动，把你救活，取消这一致死的攻击，恢复 %d 点生命值，并在半径 %d 码范围内造成 %0.2f 闪电伤害，眩晕目标 3 回合。
如果电击除颤器没有启动，其冷却时间会减少 15 回合。
生命值恢复量和伤害受蒸汽强度加成。
```

## entry-03930
位置：tome-orcs.lua:5060；section：tome-orcs/data/talents/steam/gunner-training.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases weapon damage by %d%% and Physical Power by 30 when using steamguns.
		Also, increases your reload rate by %d.
```
译文：
```text
当你使用蒸汽枪时，增加 30 物理强度和 %d%% 武器伤害。
		你的装填弹药速率增加 %d。
```

## entry-03931
位置：tome-orcs.lua:5089；section：tome-orcs/data/talents/steam/gunslinging.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have learned to fire while moving.
		In one motion, you fire your double steamguns (100%% weapon damage, 1 tile range penalty) and may then move to an adjacent tile (unless pinned to the ground or immobilized).
		This talent can be activated for up to %d consecutive turns before it goes on cooldown, and takes time according to your steamtech speed or movement speed (if you move), whichever is slower.
		When Strafe ends you may instantly reload between %d and %d ammo (based on the number of strafes you performed and your ammo capacity).
```
译文：
```text
你学会如何在移动中射击。
		在射击（100%% 武器伤害，射程 -1）的同时你能移动到相邻的一格。
		该技能在冷却前能激活连续 %d 个回合，消耗时间取决于蒸汽速度和移动速度较慢者。
		扫射结束后，你立刻获得 %d 到 %d 弹药（取决于扫射期间你消耗的弹药与你的弹药容量）。
```

## entry-03932
位置：tome-orcs.lua:5106；section：tome-orcs/data/talents/steam/gunslinging.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using small engines to augment your reflexes you are able to automatically fire retaliatory shots at your foes doing %d%% weapon damage.
		Retaliation shots are fired when you evade/are missed by a melee or ranged attack.
		This can only happen once per turn and uses shots as normal.
```
译文：
```text
开启引擎强化反射神经，你能进行反击射击，造成 %d%% 武器伤害。
		反击射击是当你闪避或躲闪近战、远程攻击时触发的自动射击。
		反击射击一回合只能触发一次，且照常消耗弹药。
```

## entry-03933
位置：tome-orcs.lua:5112；section：tome-orcs/data/talents/steam/gunslinging.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your cunning and dexterity allow you to fire incredible trick shots that can hit multiple targets.
		You precisely aim your trick shot to ricochet amongst foes you can see so that whenever it hits something solid (creature or solid wall), it will bounce towards the next closest foe.
		It may ricochet up to %d times (or until it misses) within range 5 of your first target and will not target the same foe twice.
		Your shot deals %d%% weapon damage on its first strike, but loses %d%% damage and %d(%d%%) accuracy with each bounce.
```
译文：
```text
你的灵敏让你能射出同时击中多个敌人的子弹。
		你精确地瞄准敌人，子弹命中后将弹射至其他目标上。
		子弹最多弹射 %d 次，只能在第一个目标周围 5 码范围内弹射，不会命中同一个目标两次。
		第一次命中将造成 %d%% 武器伤害，之后每次弹射下降 %d%% 伤害和 %d （%d%%）命中。
```

## entry-03934
位置：tome-orcs.lua:5143；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You replace your steamgun and attack with an incendiary device that projects streams of liquid flame at your foes.
		
		Deals %d%% steamgun damage as fire over 3 turns to enemies in radius 5.

		These attacks cannot miss and ignore armor.
```
译文：
```text
你将你的蒸汽枪替换成一把强大的蒸汽动力的喷火器，将你的敌人化为灰烬。

		在 5 码范围内，在 3 回合内造成 %d%% 火焰蒸汽枪伤害。

		这一攻击必定命中目标，无视护甲。
```

## entry-03935
位置：tome-orcs.lua:5158；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You replace your steamgun and attack with a lightning-charged staff to engage in close combat.
		
		Deals %d%% steamgun damage as lightning to enemies in a frontal arc, as well as reducing the damage they deal by %d%% for 3 turns. This counts as a melee attack but triggers ammunition on-hit effects. All shockstaff attacks will also make a shield slam for the same damage as lightning. 

		You can charge up to your steamgun's range to make shockstaff attacks.
```
译文：
```text
你将你的蒸汽枪替换成一根通了强电的电棍，用于进行近战格斗。

		在前方造成 %d%% 闪电蒸汽枪伤害，并降低他们所造成的伤害 %d%%，持续 3 回合。这一效果视作近战攻击，但可以触发弹药的命中效果。所有电击棒伤害也会附加一次盾牌攻击，造成同样的闪电伤害。

		你可以冲刺进行电击棒攻击，冲刺范围等于蒸汽枪射程。
```

## entry-03936
位置：tome-orcs.lua:5175；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You replace your steamgun and attack with a multi-barreled bolt launcher, firing deadly chemical-infused flechettes.
		
		Each attack fires twice for %d%% weapon damage as acid and generates %d steam per hit.
```
译文：
```text
你把你的蒸汽枪替换成一把多管重型枪械，发射注入了致命的化学物质的子弹。

		每次攻击造成两次 %d%% 酸性武器伤害，击中恢复 %d 蒸汽。
```

## entry-03937
位置：tome-orcs.lua:5181；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the disarm!
```
译文：
```text
%s抵抗了缴械！
```

## entry-03938
位置：tome-orcs.lua:5185；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning blow!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-03939
位置：tome-orcs.lua:5186；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the stunning shock!
```
译文：
```text
%s抵抗了震慑打击！
```

## entry-03940
位置：tome-orcs.lua:5210；section：tome-orcs/data/talents/steam/heavy-weapons.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s slams into something solid, emitting a pulse of stunning lightning!
```
译文：
```text
%s击中了某物，放出一股震慑闪电冲击！
```

## entry-03941
位置：tome-orcs.lua:5225；section：tome-orcs/data/talents/steam/inscriptions.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Implant: Steam Generator
```
译文：
```text
植入物：蒸汽制造机
```

## entry-03942
位置：tome-orcs.lua:5247；section：tome-orcs/data/talents/steam/magnetism.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# shatters '#Target#'.
```
译文：
```text
#Source#击碎了'#Target#'。
```

## entry-03943
位置：tome-orcs.lua:5275；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Link to the summoner.
```
译文：
```text
链接到召唤者。
```

## entry-03944
位置：tome-orcs.lua:5277；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The mecharachnid self-destructs, destroying itself and generating a blast of fire in a radius of %d, doing %0.2f fire damage.
		This spell is only usable when the mecharachnid's master is dead.
```
译文：
```text
机械蜘蛛引爆自己，摧毁机械蜘蛛并在 %d 码范围内产生一个火焰爆炸，造成 %0.2f 火焰伤害。
		这个技能只有机械蜘蛛的主人死亡时能够使用。
```

## entry-03945
位置：tome-orcs.lua:5303；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Mecharachnid chassis changed to: #GOLD#%s
```
译文：
```text
机械蜘蛛底盘切换为：#GOLD#%s
```

## entry-03946
位置：tome-orcs.lua:5320；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Leap into your mecharachnid, assuming direct control of it for %d turns. While piloting it, all damage dealt is increased by %d%%, resistances are increased by %d%%, and all of its talents cooldown twice as fast.
```
译文：
```text
跳入机械蜘蛛，直接控制它 %d 回合。当控制它的时候，它所造成的所有伤害增加 %d%%，抗性增加 %d%%，所有技能冷却时间减半。
```

## entry-03947
位置：tome-orcs.lua:5329；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# provokes #Target# to attack it.
```
译文：
```text
#Source#强制#Target#攻击它。
```

## entry-03948
位置：tome-orcs.lua:5330；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You rush to the target and strike with your tailsaw, dealing %d%% damage and taunting enemies within radius %d.
		You now also use your Dexterity in place of Strength when equipping Steamsaws as well as when calculating weapon damage, and have your Steamsaw damage increased by %d%% and Physical Power by %d.
```
译文：
```text
你冲向敌人，用尾部蒸汽链锯进行攻击，造成 %d%% 伤害，并嘲讽半径 %d 码内的所有敌人。
		装备蒸汽链锯的时候，你使用敏捷代替力量值计算装备需求和计算武器伤害，并且增加你蒸汽链锯的伤害 %d%%，物理强度 %d。
```

## entry-03949
位置：tome-orcs.lua:5339；section：tome-orcs/data/talents/steam/mecharachnid.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
On falling below 0 life, you engage an automated repair mode. While in this mode you cannot act, but can survive below -%d life, heal for %0.1f life each turn and have all resistances increased by %d%%. This will last until you are destroyed or until you are fully healed.
		This effect has a cooldown.
```
译文：
```text
当生命值降低到 0 点以下的时候，你会启动自动修理模式。在自动修理模式下，你不能活动，生命值下限为 -%d，每回合恢复 %0.1f 生命值，并且所有抗性增加 %d%%。这一效果直到你的生命值完全恢复或者你被摧毁才会终止。
		这一效果具有冷却时间。
```

## entry-03950
位置：tome-orcs.lua:5374；section：tome-orcs/data/talents/steam/mechstar.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you fire your metalstar, your also establish a psionic bloodlink with the shrapnel still inside for %d turns.
		Each turn the victims are drained for %0.2f physical damage, half of which heals you (each additional victim healing is reduced by half).
		If the victim move more than twice away from the radius of Metalstar (currently %d) the effect stops.
		This damage does not break daze and increases with your Steampower.
```
译文：
```text
每次你使用灵晶射击时，你将与灵晶碎片建立血液灵能联系，持续 %d 回合。
		每回合目标将受到 %0.2f 物理伤害，一半伤害值将转化为治疗。
		每增加一名额外目标，其带来的治疗量进一步减半。
		当目标距离超过金属灵晶范围（当前 %d）的两倍时，效果中止。
		该伤害不会打断眩晕效果，受蒸汽强度加成。
```

## entry-03951
位置：tome-orcs.lua:5403；section：tome-orcs/data/talents/steam/other.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Allows you to create tinkers.
```
译文：
```text
使用该技能来制造药剂、附着物等道具。
```

## entry-03952
位置：tome-orcs.lua:5415；section：tome-orcs/data/talents/steam/other.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You have no ammo!
```
译文：
```text
你没有子弹！
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cancel	取消	T.UI.LABEL	ui	_t	preferred	global	通用界面按钮（42 处）；对话框/菜单取消操作
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Medical Injector	医疗注射器	T.GAME.TALENT	talents	talent name	preferred	dlc	Embers of Rage 药剂注射技能与植入物选择项名称；统一为“医疗注射器”，不写作“药物注射器”
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
heavy weapons	重装武器	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mecharachnid	机械蜘蛛	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
medical injector	医疗注射器	T.GAME.ENTITY	items	_t	preferred	dlc	Embers of Rage 用于施用药剂的通用装置；统一实体说明、格式文本与日志中的引用，不写作“医用/药物注射器”
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
reload rate	每次装填弹药数	T.TECH.FORMAT	tech	tformat	preferred	core	弓与投石索机制属性；实际增加每次自动装填的弹药数量，并非缩短装填耗时
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
steamsaw	蒸汽链锯	T.GAME.ENTITY	items	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
