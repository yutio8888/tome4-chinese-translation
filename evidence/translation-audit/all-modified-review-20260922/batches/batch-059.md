# batch-059：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01746
位置：mod-tome.lua:23626；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CADET_BLUE#Your %s has expired.
```
译文：
```text
#CADET_BLUE#你的%s消失了。
```

## entry-01747
位置：mod-tome.lua:23634；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Prepare which traps? (maximum: %d, up to tier %d)%s
```
译文：
```text
准备什么陷阱？(最多%d个，最高阶级 %d)%s
```

## entry-01748
位置：mod-tome.lua:23644；section：mod-tome/data/talents/cunning/traps.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 (normal trigger)
```
译文：
```text
 （常规触发）
```

## entry-01749
位置：mod-tome.lua:23645；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#No changes to trap preparation.
```
译文：
```text
#LIGHT_BLUE#陷阱准备未作更改。
```

## entry-01750
位置：mod-tome.lua:23646；section：mod-tome/data/talents/cunning/traps.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GREY#(see trap description)#LAST#
```
译文：
```text
#GREY#（见陷阱描述）#LAST#
```

## entry-01751
位置：mod-tome.lua:23647；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%sTier %d: %s#LAST#
%s
```
译文：
```text
%s材质等级 %d：%s#LAST#
%s
```

## entry-01752
位置：mod-tome.lua:23666；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01753
位置：mod-tome.lua:23669；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Deploy a noisy lure that attracts all creatures within radius %d to it for %d turns.
		It has %d life (based on your Cunning) and is very durable, with %d armor and %d%% resistance to non-physical damage.
		At level 5, when the lure is destroyed, it will trigger some traps in a radius of 2 around it (check individual trap descriptions to see if they are triggered).
		Use of this talent will not break stealth.
```
译文：
```text
抛出一个诱饵来吸引 %d 码半径内的所有生物，持续 %d 回合。
		诱饵有 %d 生命（基于灵巧），且非常坚韧，拥有 %d 护甲和 %d%% 非物理伤害抗性。
		在等级 5 时，当诱饵被摧毁时，它会触发其周围 2 码范围内的部分陷阱（请查看各陷阱自身的说明，以确认其是否会被触发）。
		此技能不会打断潜行状态。
```

## entry-01754
位置：mod-tome.lua:23681；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Cancelled Trap Priming.
```
译文：
```text
#LIGHT_BLUE#取消即爆陷阱。
```

## entry-01755
位置：mod-tome.lua:23683；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Preparing %s (instant trigger)
```
译文：
```text
#LIGHT_GREEN#准备%s中（立刻触发）
```

## entry-01756
位置：mod-tome.lua:23699；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Shrapnel (radius 2) deals %0.2f physical damage, reduces accuracy, armour, and defence by %d.
```
译文：
```text
刀片（范围2）%0.2f 物理伤害，减少命中、护甲和闪避 %d。
```

## entry-01757
位置：mod-tome.lua:23703；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a pressure triggered trap that explodes into a radius 2 wave of razor sharp wire, doing %0.2f physical damage. Those struck by the wire may be shredded, reducing accuracy, armor and defence by %d.
		This trap can use a primed trigger and a high level lure can trigger it.%s
```
译文：
```text
放置压力感应陷阱，触发后爆开半径 2 格的锋利刀片，造成 %0.2f 物理伤害。被击中的目标可能被刀片切割，命中、护甲和闪避下降 %d。
		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
```

## entry-01758
位置：mod-tome.lua:23708；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Deals %0.2f physical damage and pins, slows (30%%), and wounds for an additional %0.2f damage over 5 turns).
```
译文：
```text
%0.2f 物理伤害，定身、30%% 减速，5回合额外 %0.2f 流血伤害。
```

## entry-01759
位置：mod-tome.lua:23713；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Deals %0.2f acid damage, disarms for %d turns.
```
译文：
```text
%0.2f 酸性伤害，缴械 %d 回合。
```

## entry-01760
位置：mod-tome.lua:23724；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a pressure triggered trap that collapses the ground under the target, dealing %0.2f physical damage while burying them (removing from combat) for 5 turns.
Victims may resist being buried, in which case they are pinned (ignores 50%% pin immunity) instead.
```
译文：
```text
放置一个压力感应陷阱，目标经过时地面将坍塌，造成 %0.2f 物理伤害并将其埋在地下（暂时移出游戏）5 回合。
如果目标抵抗被埋，那么他将被定身（无视 50%% 定身免疫）。
```

## entry-01761
位置：mod-tome.lua:23729；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Explodes (radius 2) for %0.2f physical damage, 50%% blind/daze for %d turns.
```
译文：
```text
爆炸（半径2）造成 %0.2f 物理伤害，50%% 致盲/眩晕 %d 回合。
```

## entry-01762
位置：mod-tome.lua:23730；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a trap that explodes in a radius of 2, dealing %0.2f physical damage and blinding and dazing (50%% chance of each) any creature caught inside for %d turns.
		This trap can use a primed trigger and a high level lure can trigger it.%s
```
译文：
```text
放置一个闪光陷阱。产生一个 2 码范围的爆炸，造成 %0.2f 物理伤害，致盲和眩晕目标 %d 回合（各 50%% 几率）。
		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
```

## entry-01763
位置：mod-tome.lua:23739；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires a beam (range 5) at a foe each turn for %0.2f arcane damage.  Lasts %d turns.
```
译文：
```text
每回合发射（射程5）的射线，造成 %0.2f 奥术伤害。持续 %d 回合。
```

## entry-01764
位置：mod-tome.lua:23740；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a magical trap that fires a beam of arcane energy at a random foe (within range 5) each turn for %d turns, inflicting %0.2f arcane damage.
This trap requires 20 Magic to prepare and does not refund stamina when it expires.
#YELLOW#Activates immediately when placed.#LAST#
```
译文：
```text
放置魔法陷阱，每回合朝 5 格内的随机敌人射出奥术射线，持续 %d 回合，造成 %0.2f 奥术伤害。
该陷阱需要 20 魔法才能准备，消失时不返还体力。
#YELLOW#放置后立刻激活。#LAST#
```

## entry-01765
位置：mod-tome.lua:23748；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Releases a radius 3 poison gas cloud, poisoning for %0.2f nature damage over 5 turns with a 25%% for enhanced effects.
```
译文：
```text
释放范围 3的毒气，5回合内 %0.2f 自然伤害，25%% 几率强化毒素效果。
```

## entry-01766
位置：mod-tome.lua:23756；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Explodes (radius 2):  Deals %0.2f cold damage and pins for 3 turns.  Area freezes (%0.2f cold damage, 25%% freeze chance) for 5 turns.
```
译文：
```text
爆炸（范围 2）：%0.2f 寒冷伤害并定身 3 回合。范围冻结 (%0.2f 寒冷伤害，25%% 冻结几率) 5回合。
```

## entry-01767
位置：mod-tome.lua:23757；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a trap that explodes into a radius 2 cloud of freezing vapour when triggered.  Foes take %0.2f cold damage and are pinned for 3 turns.
		The freezing vapour persists for 5 turns, dealing %0.2f cold damage each turn to foes with a 25%% chance to freeze.
		This trap can use a primed trigger and a high level lure can trigger it.%s
```
译文：
```text
放置一个陷阱，激活后产生半径 2 的冰冻气体，造成 %0.2f 寒冷伤害并定身 3 回合。
		冰冻气体持续 5 回合，每回合造成 %0.2f 伤害，有 25%% 几率冻结。
		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
```

## entry-01768
位置：mod-tome.lua:23764；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Explodes (radius 2): stuns and combusts for %0.2f fire damage per turn for 3 turns.  Area deflagrates (%0.2f fire damage) for 5 turns.
```
译文：
```text
爆炸（范围 2）：震慑并在3回合内每回合造成 %0.2f 火焰伤害。范围火焰 (%0.2f 火焰伤害) 持续5 回合。
```

## entry-01769
位置：mod-tome.lua:23765；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a pressure triggered trap that explodes in a radius 2 cloud of searing flames when triggered, stunning foes with the blast (%0.2f fire damage per turn) for 3 turns.
		The deflagration persists in the area for 5 turns, burning foes for %0.2f fire damage each turn.
		This trap can use a primed trigger and a high level lure can trigger it.%s
```
译文：
```text
放置一个压力感应陷阱，激活后产生半径 2 的火云，震慑敌人 (每回合 %0.2f 火焰伤害) 3 回合。
		火焰持续 5 回合，每回合燃烧造成 %0.2f 火焰伤害。
		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
```

## entry-01770
位置：mod-tome.lua:23795；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Radius 2 antimagic: Drains up to %d mana, %d vim, %d positive/negative, deals up to %0.2f arcane damage.  Removes %d magical effects and silences for %d turns.
```
译文：
```text
半径 2 反魔：吸收至多 %d 法力，%d 活力，%d 正负能量，造成至多 %0.2f 奥术伤害。解除 %d 项魔法效果，沉默 %d 回合。
```

## entry-01771
位置：mod-tome.lua:23796；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a trap that releases a burst of antimagic energies (radius 2), draining up to %d mana, %d vim, %d positive and %d negative energies from affected targets, while inflicting up to %0.2f arcane damage based on the resources drained, silencing for %d turns, and removing up to %d beneficial magical effects or sustains.
		The draining effect scales with your Willpower, and you must have 25 Willpower to prepare this trap.
		This trap can use a primed trigger and a high level lure can trigger it.%s
```
译文：
```text
放置一个陷阱，触发后释放半径 2 的反魔能量波，吸取至多 %d 法力 , %d 活力 , %d 正能量和 %d 负能量，并造成至多 %0.2f 奥术伤害（基于吸取能量），沉默 %d 回合，并解除至多 %d 项正面魔法状态或者维持技能。
		吸取效果受意志加成，你需要 25 点意志来使用该技能。
		该陷阱可以被设置为直接激活，也可以被高等级诱饵激活。%s
```

## entry-01772
位置：mod-tome.lua:23804；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Explodes (radius 2) for %0.2f fire damage over 3 turns.
```
译文：
```text
爆炸（半径 2）：3回合内 %0.2f 火焰伤害。
```

## entry-01773
位置：mod-tome.lua:23805；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a simple yet effective trap that explodes in a radius 2 on contact, setting those affected on fire for %0.2f fire damage over 3 turns.
		This trap can use a primed trigger and a high level lure can trigger it.%s
```
译文：
```text
放置一个简单而有效的陷阱，有目标接触陷阱时，它会在半径 2 范围内爆炸，使受影响的目标着火，并在 3 回合内造成 %0.2f 点火焰伤害。
		该陷阱可以被设置为直接激活，也可以被高等级的诱饵激活。%s
```

## entry-01774
位置：mod-tome.lua:23811；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Target knocked back up to %d grids%s and dazed.
```
译文：
```text
目标被击退最多 %d 格%s，并眩晕。
```

## entry-01775
位置：mod-tome.lua:23812；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s knocks %s back!
```
译文：
```text
%s 将 %s 击退！
```

## entry-01776
位置：mod-tome.lua:23813；section：mod-tome/data/talents/cunning/traps.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s fails to knock %s back!
```
译文：
```text
%s 未能将 %s 击退！
```

## entry-01777
位置：mod-tome.lua:23825；section：mod-tome/data/talents/cunning/traps.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lay a trap armed with potent venom.  A creature passing over it will be dealt %0.2f nature damage and be stunned and poisoned for %0.2f nature damage per turn for 4 turns.
```
译文：
```text
放置一个涂了颠茄毒素的陷阱，经过的生物会受到 %0.2f 自然伤害，并被震慑和中毒 4 回合，中毒每回合造成 %0.2f 自然伤害。
```

## entry-01778
位置：mod-tome.lua:23843；section：mod-tome/data/talents/cursed/advanced-shadowmancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Target a nearby shadow, and force it to slam into a nearby enemy, dealing %0.1f Physical damage.
		Your shadow will then set them as their target, and they will target your shadow.
		Damage increases with your Mindpower.
```
译文：
```text
指定附近的一个阴影，令其攻击附近的一个敌人，造成 %0.1f 物理伤害。
		你的阴影将把那个敌人设为目标，而敌人也会攻击那个阴影。
		伤害受精神强度加成。
```

## entry-01779
位置：mod-tome.lua:23858；section：mod-tome/data/talents/cursed/advanced-shadowmancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Share your hatred with all shadows within sight range, gaining temporary full control. You then fire a blast of pure hatred from all affected shadows, dealing %0.1f Mind damage per blast.
		You cannot cancel this talent once the first bolt is cast.
		Damage increases with your Mindpower.
```
译文：
```text
和视野内的所有阴影共享你的仇恨，获得临时的完全控制。随后你从所有受影响的阴影中发射一道纯粹的仇恨冲击，每道造成 %0.1f 精神伤害。
		一旦发射了第一道，便无法取消该技能。
		伤害受精神强度加成。
```

## entry-01780
位置：mod-tome.lua:23872；section：mod-tome/data/talents/cursed/bloodstained.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Teleport to an enemy, striking them for 100%% weapon damage, bleeding them for %d%% weapon damage over five turns, and marking them for six turns. You will not teleport if you are already adjacent.

When the marked enemy dies, the cooldown of this talent will be reduced by two turns for every turn the mark had remaining.

Each point in Bloodstained talents reduces the amount of damage you take from bleed effects by 2%%
```
译文：
```text
传送至一个敌人面前，攻击造成 100%% 武器伤害，使其在5回合里受到相当于 %d%% 武器伤害的流血伤害，并标记它6回合。如果目标已经在你身边，则不会传送。

被标记的敌人死亡时，标记每剩余一回合此技能的冷却减少2回合。

每一点血染系技能使你受到的流血伤害减少2%%。
```

## entry-01781
位置：mod-tome.lua:23912；section：mod-tome/data/talents/cursed/crimson-templar.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you kill an enemy, their death forms a cursed magical pattern on the ground. This creates a circle of radius %d which blinds enemies and deals them %0.2f light damage, while giving you %d positive energy per turn. The circle lasts for %d turns.
							The damage will increase with your Spellpower.
							The duration of the circle can be increased by a critical hit.
							The blind chance increases with your Spellpower.
							You can activate this talent to draw the pattern in your own blood, creating it underneath you at the cost of %d%% of your maximum life.

```
译文：
```text
当你杀死敌人时，死亡会在地面上形成一个魔法咒印。产生一个半径 %d 的法阵，会致盲敌人并造成 %0.2f 光系伤害，同时每回合给予你 %d 正能量。法阵持续 %d 回合。
							伤害受法术强度加成。
							持续时间可以暴击。
							致盲概率受法术强度加成。
							你可以主动使用这一技能，支付 %d%% 最大生命，用自己的鲜血在脚下绘制咒印。

```

## entry-01782
位置：mod-tome.lua:23948；section：mod-tome/data/talents/cursed/cursed-aura.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The %s lies defiled at your feet. An aura of hatred surrounds you and you now feel truly cursed. You have gained the Cursed Aura talent tree and 1 point in Defiling Touch, but at the cost of 2 Willpower.
```
译文：
```text
你的脚下躺着被亵渎的%s。一股仇恨的气息笼罩了你，你感到自己真正被诅咒了。你获得了诅咒光环技能树和等级 1 的诅咒之触，但是需永久消耗 2 点意志。
```

## entry-01783
位置：mod-tome.lua:23980；section：mod-tome/data/talents/cursed/cursed-aura.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your curses bring you dark gifts. Unlocks bonus level %d effects on all of your curses, allowing you to gain that effect when the power level of your curse reaches that level. At talent level 5, the luck penalty of cursed effects is reduced to 1.
		Talent levels above 5 add bonus power levels to your curses, increasing their effects (currently %0.1f).
```
译文：
```text
你的诅咒带来黑暗的礼物。解锁所有诅咒第 %d 层效果，并允许你在诅咒达到该等级时获得此效果。
		在等级 5 时，因诅咒带来的幸运惩罚降到 1。
		等级 5 以上时为诅咒增加额外能量等级，增强其效果（当前增加 %0.1f）。
```

## entry-01784
位置：mod-tome.lua:24031；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your weapon yearns for its next victim.
```
译文：
```text
你的武器渴望着下一个牺牲者。
```

## entry-01785
位置：mod-tome.lua:24033；section：mod-tome/data/talents/cursed/cursed.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Each day, you lift your weary body and begin the unending hunt.
```
译文：
```text
你不知疲倦无时无刻狩猎你的下一个目标。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cancel	取消	T.UI.LABEL	ui	_t	preferred	global	通用界面按钮（42 处）；对话框/菜单取消操作
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Positive energy	正能量	T.GAME.RESOURCE	combat	_t	preferred	core	太阳骑士/赞歌职业资源；与 Negative energy 负能量区分
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
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
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
