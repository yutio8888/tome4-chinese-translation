# batch-063：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01906
位置：mod-tome.lua:25173；section：mod-tome/data/talents/gifts/mindstar-mastery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You hit a foe with your mainhand psiblade doing %d%% weapon damage, channeling all the damage done through your offhand psiblade with which you touch a friendly creature to heal it.
		The maximum heal possible is %d. Equilibrium of the healed target will also decrease by 10%% of the heal power.
		Max heal will increase with your Mindpower and Mindstar power (requires two mindstars, multiplier %2.f).
```
译文：
```text
你用主手心灵利刃攻击敌人造成 %d%% 武器伤害，用副手心灵利刃传导敌人所受的伤害能量来治疗友方单位。
		治疗最大值为 %d。受到治疗效果的目标失衡值会降低治疗量的 10%%。
		最大治疗值受精神强度和灵晶强度加成（需要 2 只灵晶，加成比例 %2.f）。
```

## entry-01907
位置：mod-tome.lua:25183；section：mod-tome/data/talents/gifts/moss.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instantly grow a moss circle of radius %d at your feet.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss is very thick and sticky causing all foes passing through it have their movement speed reduced by %d%% and have a %d%% chance to be pinned to the ground for 4 turns.
		The moss lasts %d turns.
		Moss talents are instant but place all other moss talents on cooldown for 3 turns.
		The damage will increase with your Mindpower.
```
译文：
```text
在你的脚下，半径 %d 的范围内生长出苔藓。
		每回合苔藓对半径内的敌人会造成 %0.2f 点自然伤害。
		这种苔藓又厚又黏，所有经过的敌人的移动速度会被降低 %d%%，并有 %d%% 概率被定身 4 回合。
		苔藓持续 %d 个回合。
		苔藓系技能无需使用时间，但会让同系其他技能进入 3 回合的冷却。
		伤害受精神强度加成。
```

## entry-01908
位置：mod-tome.lua:25195；section：mod-tome/data/talents/gifts/moss.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instantly grow a moss circle of radius %d at your feet.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss has vampiric properties and heals the user for %d%% of the damage done.
		The moss lasts %d turns.
		Moss talents are instant but place all other moss talents on cooldown for 3 turns.
		The damage will increase with your Mindpower.
```
译文：
```text
在你的脚下，半径 %d 的范围内生长出苔藓。
		每回合苔藓对半径内的敌人会造成 %0.2f 点自然伤害。
		这种苔藓具有吸血功能，会治疗使用者，数值等于造成伤害的 %d%%。
		苔藓持续 %d 个回合。
		苔藓系技能无需使用时间，但会让同系其他技能进入 3 回合的冷却。
		伤害受精神强度加成。
```

## entry-01909
位置：mod-tome.lua:25207；section：mod-tome/data/talents/gifts/moss.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instantly grow a moss circle of radius %d at your feet.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss is very slippery and causes affected foes to have a %d%% chance of failing to perform complex actions.
		The moss lasts %d turns.
		Moss talents are instant but place all other moss talents on cooldown for 3 turns.
		The damage and the chance to apply the slippery effect increase with your Mindpower.
```
译文：
```text
在你的脚下，半径 %d 的范围内生长出苔藓。
		每回合苔藓对半径内的敌人会造成 %0.2f 点自然伤害。
		这种苔藓十分光滑，会使所有受影响的敌人有 %d%% 概率不能做出复杂行动。
		苔藓持续 %d 个回合。
		苔藓系技能无需使用时间，但会让同系其他技能进入 3 回合的冷却。
		自然伤害和光滑效果的施加几率受精神强度加成。
```

## entry-01910
位置：mod-tome.lua:25219；section：mod-tome/data/talents/gifts/moss.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Instantly grow a moss circle of radius %d at your feet.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss is coated with strange fluids and has a %d%% chance to confuse (power %d%%) foes passing through it for 2 turns.
		The moss lasts %d turns.
		Moss talents are instant but place all other moss talents on cooldown for 3 turns.
		The damage will increase with your Mindpower.
```
译文：
```text
在你的脚下，半径 %d 的范围内生长出苔藓。
		每回合苔藓对半径内的敌人会造成 %0.2f 点自然伤害。
		这种苔藓上沾满了奇怪的液体，有 %d%% 概率让对方混乱（%d%% 强度）2 个回合。
		苔藓持续 %d 个回合。
		苔藓系技能无需使用时间，但会让同系其他技能进入 3 回合的冷却。
		伤害受精神强度加成。
```

## entry-01911
位置：mod-tome.lua:25260；section：mod-tome/data/talents/gifts/mucus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mucus is brought to near sentience.
		Each turn, there is a %d%% chance that a random spot of your mucus will spawn a Mucus Ooze.
		Mucus Oozes last %d turns and will attack any of your foes by spitting slime at them.
		You may have up to %d Mucus Oozes active at any time (based on your Cunning).
		Any time you deal a mental critical, the remaining time on all of your Mucus Oozes will increase by 2.
		The spawn chance increases with your Mindpower.
```
译文：
```text
你的粘液有了自己的感知。每回合有 %d%% 几率，随机一个滴有你的粘液的格子会产生一只粘液软泥怪。
		粘液软泥怪会存在 %d 回合，会向任何附近的敌人释放史莱姆喷吐。
		同时场上可存在 %d 只粘液软泥怪。（基于你的灵巧值）
		每当你造成一次精神暴击，你的所有粘液软泥怪的存在时间会延长 2 回合。
		生成概率受精神强度加成。
```

## entry-01912
位置：mod-tome.lua:25272；section：mod-tome/data/talents/gifts/mucus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You temporarily merge with your mucus, cleansing yourself of %d physical or magical detrimental effects.
		You can then reemerge on any tile within sight and range that is also covered by mucus.
		This is quick, performed in only %d%% of the normal time, but you must be in contact with your mucus.
```
译文：
```text
你暂时性的和粘液融为一体，净化你身上 %d 物理或魔法负面效果。
		然后，你可以闪现到视野且射程内任何有粘液覆盖的区域。
		此技能使用速度很快，只消耗一般技能使用时间的 %d%%，但只有当你站在粘液区时才能使用。
```

## entry-01913
位置：mod-tome.lua:25288；section：mod-tome/data/talents/gifts/ooze.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your body is more like that of an ooze.
		When you take damage, you may split and create a Bloated Ooze nearby within your line of sight.
		This ooze has as much health as twice the damage you took (up to a maximum of %d, based on your Mindpower and maximum life).
		The chance to split equals the percent of your health lost times %0.2f.
		You may have up to %d Bloated Oozes active at any time (limited by talent level and the summoning limit), and all damage you take will be split equally between you and them so long as this talent is active.
		Bloated Oozes last for %d turns, are very resilient (%d%% all damage resistance to damage not coming through your shared link), and regenerate life quickly.
		%sThe chance to split increases with your Cunning.
```
译文：
```text
你的身体构造变的像软泥怪一样。
		当你受到攻击时，你有几率分裂出一个浮肿软泥怪，其生命值为你所承受的伤害值的两倍（最大 %d，基于你的精神强度和最大生命值）。
		分裂几率为你损失生命百分比的 %0.2f 倍。
		你同时最多只能拥有 %d 只浮肿软泥怪，你所承受的所有伤害会在你和浮肿软泥怪间均摊。
		每只浮肿软泥怪存在 %d 回合，对非均摊的伤害的抗性很高（%d%% 对全部伤害的抗性），同时生命回复快。
		%s几率受灵巧加成。
```

## entry-01914
位置：mod-tome.lua:25300；section：mod-tome/data/talents/gifts/ooze.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Reabsorb
```
译文：
```text
再吸收
```

## entry-01915
位置：mod-tome.lua:25301；section：mod-tome/data/talents/gifts/ooze.lua；source_tag：tformat；args_order：[1, 3, 2, 4]；special：None

原文：
```text
You randomly merge with an adjacent bloated ooze, granting you 40%% all damage resistance for %d turns.
		This process releases a burst of antimagic, dealing %0.1f Manaburn damage in radius %d.
		This talent allows you to restore %0.1f Equilibrium per turn while Mitosis is active.
		The damage, duration and Equilibrium restoration increase with your Mindpower.
```
译文：
```text
你随机吸收一个紧靠你的浮肿软泥怪，获得 40%% 对全部伤害的抗性，持续 %d 个回合。
		同时你会释放一股反魔能量，在 %d 半径内造成 %0.1f 点法力燃烧伤害。
		如果有丝分裂技能开启，每回合你将减少 %0.1f 点失衡值。
		伤害、持续时间和失衡值减少量受精神强度加成。
```

## entry-01916
位置：mod-tome.lua:25316；section：mod-tome/data/talents/gifts/ooze.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Indiscernible Anatomy
```
译文：
```text
难以辨认的解剖结构
```

## entry-01918
位置：mod-tome.lua:25327；section：mod-tome/data/talents/gifts/oozing-blades.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Channel slime through your psiblades, extending their reach to create a beam doing %0.1f Slime damage.
		The damage increases with your Mindpower.
```
译文：
```text
在你的心灵利刃里充填史莱姆能量，延展攻击范围，形成一道射线，造成 %0.1f 点史莱姆伤害。
		伤害受精神强度加成。
```

## entry-01919
位置：mod-tome.lua:25331；section：mod-tome/data/talents/gifts/oozing-blades.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You gain %d%% Nature resistance.
		When you deal Acid damage to a creature, you gain a %0.1f%% bonus to Nature damage for %d turns. 
		This damage bonus will improve up to 4 times (no more than once each turn) with later Acid damage you do, up to a maximum of %0.1f%%.
		The resistance and damage increase improve with your Mindpower.
```
译文：
```text
你的自然抗性增加 %d%%。
		当你造成酸性伤害时，你的自然伤害增加 %0.1f%%，持续 %d 回合。
		伤害加成能够积累到最多4倍（1回合至多触发1次），最大值 %0.1f%%。
		抗性和伤害加成受精神强度加成。
```

## entry-01920
位置：mod-tome.lua:25339；section：mod-tome/data/talents/gifts/oozing-blades.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You use your psiblades to fire a small worm at a foe.
		When it hits, it will burrow into the target's brain and stay there for 6 turns, interfering with its ability to use talents.
		Each time a talent is used there is %d%% chance that %d talent(s) are placed on a %d turn(s) cooldown.
		The chance will increase with your Mindpower.
```
译文：
```text
你利用你的心灵利刃朝你的敌人发射一条小蠕虫。
		当攻击击中时，它会进入目标大脑，并在那里待 6 回合，干扰对方使用技能的能力。
		每次对方使用技能时，有 %d%% 概率 %d 个技能被打入 %d 个回合的冷却。
		概率受精神强度加成。
```

## entry-01921
位置：mod-tome.lua:25402；section：mod-tome/data/talents/gifts/sand-drake.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ breathes sand!
```
译文：
```text
@Source@呼出流沙！
```

## entry-01922
位置：mod-tome.lua:25403；section：mod-tome/data/talents/gifts/sand-drake.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You breathe sand in a frontal cone of radius %d. Any target caught in the area will take %0.2f physical damage, and will be blinded for %d turns.
		The damage will increase with your Strength, the critical chance is based on your Mental crit rate, and the Blind apply power is based on your Mindpower.
		Each point in sand drake talents also increases your physical resistance by 0.5%%.
```
译文：
```text
你在前方 %d 码锥形范围内喷出流沙。此范围内的目标会受到 %0.2f 物理伤害并被致盲 %d 回合。
		伤害受力量值加成。技能暴击率基于精神暴击值计算，致盲强度基于你的精神强度。
		每点土龙系的天赋可以使你增加物理抗性 0.5%%。
```

## entry-01923
位置：mod-tome.lua:25465；section：mod-tome/data/talents/gifts/storm-drake.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-01924
位置：mod-tome.lua:25467；section：mod-tome/data/talents/gifts/storm-drake.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summon a tornado that moves very slowly towards the target, following it if it changes position.
		Each time it moves every foes within radius 2 takes %0.2f lightning damage and is knocked back 2 spaces.
		When it reaches the target it explodes in a radius of %d, knocking back targets and dealing %0.2f lightning and %0.2f physical damage.
		The tornado will move a maximum of 20 times.
		Damage will increase with your Mindpower.
		Each point in storm drake talents also increases your lightning resistance by 1%%.
```
译文：
```text
召唤一个龙卷风，它会向着目标极为缓慢地移动，并在目标移动时跟随目标，最多移动20次。
		每当它移动时，半径2范围内的所有敌人会受到 %0.2f 闪电伤害，并被击退2格。
		当它碰到目标的时候，会在 %d 码范围内引发爆炸，击退目标，并造成 %0.2f 闪电和 %0.2f 物理伤害。
		伤害受精神强度加成
		每点雷龙系的天赋可以使你增加闪电抗性 1%%。
```

## entry-01925
位置：mod-tome.lua:25480；section：mod-tome/data/talents/gifts/storm-drake.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You breathe lightning in a frontal cone of radius %d. Any target caught in the area will take %0.2f to %0.2f lightning damage (%0.2f average) and be stunned for 3 turns.
		The damage will increase with your Strength, and the critical chance is based on your Mental crit rate, and the Stun apply power is based on your Mindpower.
		Each point in storm drake talents also increases your lightning resistance by 1%%.
```
译文：
```text
你在前方 %d 码锥形范围内喷出闪电。此范围内的目标会受到 %0.2f ～ %0.2f 闪电伤害（平均 %0.2f）并被震慑 3 回合。
		伤害受力量值加成。技能暴击率基于精神暴击值计算，震慑强度受精神强度影响。
		每点雷龙系的天赋可以使你增加闪电抗性 1%%。
```

## entry-01926
位置：mod-tome.lua:25492；section：mod-tome/data/talents/gifts/summon-advanced.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While Master Summoner is active, when a creature you summon appears in the world, it will trigger a wild effect:
		- Ritch Flamespitter: Reduce fire resistance of all foes in the radius by %d%%
		- Hydra: Generates a cloud of lingering poison, poisoning all foes caught within for %0.1f nature damage per turn (cumulative)
		- Rimebark: Reduce cold resistance of all foes in the radius by %d%%
		- Fire Drake: Appears with %d fire drake hatchling(s)
		- War Hound: Reduce physical resistance of all foes in the radius by %d%%
		- Jelly: Reduce nature resistance of all foes in the radius by %d%%
		- Minotaur: Reduces movement speed of all foes in the radius by %0.1f%%
		- Stone Golem: Dazes all foes in the radius
		- Turtle: Heals all friendly targets in the radius %d HP
		- Spider: Pins all foes in the radius
		Radius for effects is %d, and the duration of each lasting effect is %d turns.
		The effects improve with your mindpower.
```
译文：
```text
当召唤精通激活时，每个召唤兽出现在世界上时，它会触发 1 个野性效果：
		- 喷火里奇：减少范围内所有敌人的火焰抗性 %d%%
		- 三头蛇：生成一片持续的毒雾，范围内所有敌人每回合受到 %0.1f 自然伤害（可叠加）
		- 雾凇：减少范围内所有敌人的寒冷抗性 %d%%
		- 火龙：出现 %d 只小火龙
		- 战争猎犬：减少范围内所有敌人的物理抗性 %d%%
		- 果冻怪：减少范围内所有敌人的自然抗性 %d%%
		- 米诺陶：减少范围内所有敌人的移动速度 %0.1f%%
		- 岩石傀儡：眩晕范围内所有敌人
		- 乌龟：治疗范围内所有友军单位 %d 生命值
		- 蜘蛛：定身范围内所有敌人。
		效果范围 %d，每个持续效果维持 %d 回合。
		效果受精神强度加成。
```

## entry-01928
位置：mod-tome.lua:25560；section：mod-tome/data/talents/gifts/summon-augmentation.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Destroys one of your summons, making it detonate in radius of %d.
		- Ritch Flamespitter: Explodes into a fireball dealing %d damage, flameshocking damaged foes
		- Hydra: Grants %d%% lightning, acid, and nature affinity as well as %d life regen per turn to all friendly creatures for 7 turns
		- Rimebark: Explodes into an iceball dealing %d ice damage, possibly freezing damaged foes
		- Fire Drake: Explodes into a cloud of lingering fire, dealing %d damage per turn
		- War Hound: Explodes into a sharp ball, cutting all creatures for %0.1f bleeding damage per turn for 6 turns
		- Jelly: Explodes into a ball of slowing slime, dealing %d nature damage and slowing foes by %0.1f%%
		- Minotaur: Confuses foes at %d%% power for 5 turns
		- Stone Golem: Grants %d armour and %d%% armour hardiness to all friendly creatures for 5 turns
		- Turtle: Grants a small shell shield to all friendly creatures, granting %d%% all resist for 5 turns
		- Spider: Knocks back all foes %d tiles
		In addition, a random summon will come off cooldown.
		Hostile effects will not hit you or your other summons.
		The effects improve with your mindpower, and some can crit.
```
译文：
```text
献祭一只召唤兽，使它在 %d 码范围内爆炸。
		-喷火里奇：形成一个火球，造成 %d 伤害，并火焰冲击敌人。
		-三头蛇：范围内所有友方单位获得 %d%% 闪电、酸液和自然伤害亲和，并获得每回合 %d 生命回复，持续 7 回合。
		-雾凇：形成一个冰球，造成 %d 冰冷伤害，可能冰冻敌人。
		-火龙：形成一片火焰，每回合造成 %d 伤害。
		-战争猎犬：形成锋利的球，让周围的生物在 6 回合内每回合受到 %0.1f 点流血伤害。
		-果冻怪：形成一片能减速的淤泥，造成 %d 自然伤害，并使敌人减速 %0.1f%%。
		-米诺陶斯：使敌人混乱 5 回合（强度 %d%%）。
		-岩石傀儡：使周围的友方单位获得 %d 护甲值和 %d%% 护甲强度，持续 5 回合。
		-乌龟：给所有友方单位提供一个甲壳护盾，所有抗性提升 %d%%，持续 5 回合。
		-蜘蛛：将所有敌人击退 %d 格。
		此外，随机的某个召唤技能会冷却完毕。
		引爆产生的负面效果不会影响到你或你的召唤兽。
		效果受精神强度加成，其中一些可以暴击。
```

## entry-01929
位置：mod-tome.lua:25588；section：mod-tome/data/talents/gifts/summon-augmentation.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases all your summons' max life by %0.1f%% and extends your summons' maximum lifetime by %d turns.
```
译文：
```text
提升你所有召唤物的最大生命值 %0.1f%%，并延长所有召唤物的存活时间 %d 回合。
```

## entry-01930
位置：mod-tome.lua:25635；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A furious ice storm rages around the user doing %0.2f cold damage in a radius of 3 each turn for %d turns.
		It has 25%% chance to freeze damaged targets.
		The damage and duration will increase with your Willpower.
```
译文：
```text
一阵激烈的冰风暴环绕施法者造成每回合 %0.2f 冰冷伤害，有效范围 3 码，持续 %d 回合。
		有 25%% 几率使受伤害目标被冰冻。
		受意志影响，伤害和持续时间有额外加成。
```

## entry-01931
位置：mod-tome.lua:25646；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Ritch Flamespitter
```
译文：
```text
召唤：喷火里奇
```

## entry-01932
位置：mod-tome.lua:25647；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ summons a Ritch Flamespitter!
```
译文：
```text
@Source@召唤了一只喷火里奇！
```

## entry-01933
位置：mod-tome.lua:25649；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01934
位置：mod-tome.lua:25650；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (wild summon)
```
译文：
```text
%s（野性召唤）
```

## entry-01935
位置：mod-tome.lua:25651；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summon a Ritch Flamespitter for %d turns to burn your foes to death. Flamespitters are weak in melee and die easily, but they can burn your foes from afar.
		It will get %d Willpower, %d Cunning and %d Constitution.
		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
		Their Willpower and Cunning will increase with your Mindpower.
```
译文：
```text
召唤一只喷火里奇来燃烧敌人，持续 %d 回合。喷火里奇近战薄弱且容易死亡，但是它们可以从远处燃烧敌人。
		它拥有 %d 点意志，%d 点灵巧和 %d 点体质。
		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
		喷火里奇的意志和灵巧受精神强度加成。
```

## entry-01936
位置：mod-tome.lua:25658；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Hydra
```
译文：
```text
召唤：三头蛇
```

## entry-01937
位置：mod-tome.lua:25659；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ summons a 3-headed hydra!
```
译文：
```text
@Source@召唤了一只三头蛇！
```

## entry-01938
位置：mod-tome.lua:25660；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A strange reptilian creature with three smouldering heads.
```
译文：
```text
长着三颗灼热冒烟的头颅的奇怪爬行动物。
```

## entry-01939
位置：mod-tome.lua:25661；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summon a 3-headed Hydra for %d turns to destroy your foes. 3-headed hydras are able to breathe poison, acid and lightning.
		It will get %d Willpower, %d Constitution and 18 Strength.
		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
		Their Willpower will increase with your Mindpower.
```
译文：
```text
召唤一只三头蛇来摧毁敌人，持续 %d 回合。
		三头蛇可以喷出毒系、酸系、闪电吐息。
		它拥有 %d 点意志，%d 点体质和 18 点力量。
		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
		三头蛇的意志受精神强度加成。
```

## entry-01940
位置：mod-tome.lua:25669；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Rimebark
```
译文：
```text
召唤：雾凇
```

## entry-01941
位置：mod-tome.lua:25670；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ summons a Rimebark!
```
译文：
```text
@Source@召唤了一只雾凇！
```

## entry-01942
位置：mod-tome.lua:25672；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summon a Rimebark for %d turns to harass your foes. Rimebarks cannot move, but they have a permanent ice storm around them, damaging and freezing anything coming close in a radius of 3.
		It will get %d Willpower, %d Cunning and %d Constitution.
		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
		Their Willpower and Cunning will increase with your Mindpower.
```
译文：
```text
召唤 1 棵持续 %d 回合的雾凇骚扰敌人。
		雾凇不可移动，但是永远有寒冰风暴围绕着它们，伤害并冰冻 3 码半径范围内的任何人。
		它拥有 %d 点意志，%d 点灵巧和 %d 点体质。
		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
		雾凇的意志和灵巧受精神强度加成。
```

## entry-01943
位置：mod-tome.lua:25680；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Fire Drake
```
译文：
```text
召唤：火龙
```

## entry-01944
位置：mod-tome.lua:25681；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ summons a Fire Drake!
```
译文：
```text
@Source@召唤了一只火龙！
```

## entry-01945
位置：mod-tome.lua:25683；section：mod-tome/data/talents/gifts/summon-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summon a Fire Drake for %d turns to burn and crush your foes to death. Fire Drakes are behemoths that can burn foes from afar with their fiery breath.
		It will get %d Strength, %d Constitution and 38 Willpower.
		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
		Their Strength and Constitution will increase with your Mindpower.
```
译文：
```text
召唤一只火龙来摧毁敌人，持续 %d 回合。
		火龙是可以从很远的地方烧毁敌人的强大生物。
		它拥有 %d 点力量，%d 点体质和 38 点意志。
		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
		火龙的力量和体质受精神强度加成。
```

## entry-01946
位置：mod-tome.lua:25701；section：mod-tome/data/talents/gifts/summon-melee.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@source@ oozes over the ground!!
```
译文：
```text
@source@在地上散布！！
```

## entry-01947
位置：mod-tome.lua:25705；section：mod-tome/data/talents/gifts/summon-melee.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
War Hound
```
译文：
```text
召唤：战争猎犬
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Equilibrium	失衡值	T.GAME.RESOURCE	resources	_t	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Flameshock	火焰冲击	T.GAME.TALENT	talents	talent name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
bloated ooze	浮肿软泥怪	T.GAME.ENTITY	creatures	_t	preferred	core	软泥系“有丝分裂”生成的召唤物；统一实体名及“软泥召唤”“强化吸收”等技能说明，不省略“软泥”
cleansing	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key；同 cohort 的 cleanse 运行键亦采用“洁净”；不约束其他语境
cleansing 	洁净的	T.GAME.ENTITY	items	entity name	preferred	core	仅适用于核心装备 ego 的前缀名称；保留 source 尾空格；不约束技能、伤害类型、日志或叙事中的 cleansing
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mainhand	主手	T.GAME.ENTITY	items	nil	existing	core	
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
offhand	副手	T.GAME.ENTITY	items	nil	existing	core	
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
