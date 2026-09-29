# batch-074：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02349
位置：mod-tome.lua:30413；section：mod-tome/data/talents/techniques/duelist.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The flow of battle invigorates you, allowing you to press your advantage as the fight progresses.
		Up to once each per turn, while dual wielding, you may:
		Riposte -- If a melee or archery attack misses you or you parry it, you instantly restore %0.1f stamina and gain %d%% of a turn.
		Recover -- On performing a critical strike with your offhand weapon, you instantly restore %0.1f stamina.
```
译文：
```text
战斗鼓舞着你，让你在战斗中获得优势。
		双持武器时，每回合各至多一次，你可以：
		反击 -- 如果你闪避或抵挡了近战或弓箭攻击，你立刻回复 %0.1f 体力并获得 %d%% 额外回合。
		回复 -- 副手武器暴击时回复 %0.1f 体力。
```

## entry-02350
位置：mod-tome.lua:30423；section：mod-tome/data/talents/techniques/duelist.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
Terrain prevents #Source# from switching places with #Target#.
```
译文：
```text
地形阻止了#Source#与#Target#的换位。
```

## entry-02351
位置：mod-tome.lua:30424；section：mod-tome/data/talents/techniques/duelist.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Make a cunning feint that tricks your target into swapping places with you.  While moving, you take the opportunity to trip them, pinning and dazing them for 2 turns.
		Switching places distracts your foes and allows you to improve your defenses:  For %d turns, Dual Weapon Mastery yields one extra parry each turn and you are %d%% less likely to miss your parry opportunities.
		The chance to pin and to daze increases with your Accuracy
```
译文：
```text
以巧妙的虚招诱使目标与你换位。换位移动时你趁机将其绊倒，使其定身并眩晕 2 回合。
		换位令你的敌人分心，使你的防御得到强化：%d 回合内，双持掌握每回合提供额外一次招架机会，你错失招架机会的几率下降 %d%%。
		定身与眩晕几率受命中加成。
```

## entry-02352
位置：mod-tome.lua:30431；section：mod-tome/data/talents/techniques/duelist.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot use Lunge without dual wielding!
```
译文：
```text
你需要双持武器来施展这个技能！
```

## entry-02353
位置：mod-tome.lua:30433；section：mod-tome/data/talents/techniques/duelist.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Exploiting a gap in your target's defenses, you make a lethal strike with your offhand weapon for %d%% damage that causes them to drop their weapon, disarming them for %d turns.
		Tempo will reduce the cooldown of this talent by 1 turn each time it is triggered defensively.
		The chance to disarm increases with your Accuracy.
```
译文：
```text
你攻其不备，用副手发起致命打击，造成 %d%% 伤害并使其武器脱落，缴械 %d 回合。
		每当节奏被防御性触发（近战或射击落空、或被招架）时，本技能的冷却时间减少 1 回合。
		缴械几率受命中加成。
```

## entry-02354
位置：mod-tome.lua:30444；section：mod-tome/data/talents/techniques/excellence.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your reflexes are lightning-fast, if you spot a projectile (arrow, shot, spell, ...) you can instantly shoot at it without taking a turn to take it down.
		You can shoot down up to %d projectiles.
```
译文：
```text
你的反射神经像闪电一样快。当你瞄准抛射物（箭矢、弹药、法术等）时，你能马上击落它而不消耗时间。
		你最多能击落 %d 个目标。
```

## entry-02355
位置：mod-tome.lua:30449；section：mod-tome/data/talents/techniques/excellence.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You rush toward your foe, readying your shot. If you reach the enemy, you release the shot, imbuing it with great power.
		The shot does %d%% weapon damage and knocks back your target by %d.
```
译文：
```text
你冲向你的敌人，并准备好射击。如果你接触到敌人，你将射出你准备好的箭矢/弹药，给予其强劲的力量。
		射击造成 %d%% 武器伤害并击退对手 %d 码。
```

## entry-02356
位置：mod-tome.lua:30456；section：mod-tome/data/talents/techniques/excellence.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activating this talent enhances your reflexes to incredible levels.  Each time you are attacked in melee, you have a %d%% chance get a defensive shot off in time to intercept the attack, fully disrupting it (including extra blows from certain talents), dealing %d%% archery damage, and knocking the attacker back %d tiles.
		Activating this talent will not interrupt reloading.
```
译文：
```text
激活该技能会大幅强化你的反射神经。每次你受到近战攻击，你有 %d%% 的几率及时进行一次防御性射击来拦截并完全瓦解对方这次攻击（包括某些技能带来的额外打击），造成 %d%% 射击伤害，同时击退对方 %d 码。激活这项技能不会中断装填弹药。
```

## entry-02357
位置：mod-tome.lua:30460；section：mod-tome/data/talents/techniques/excellence.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a shot at your target's throat, mouth, or equivalent body part, doing %d%% damage and silencing it for %d turns.
		The silence chance increases with your Accuracy.
```
译文：
```text
你瞄准目标的喉咙、嘴巴或相关部位，造成 %d%% 伤害，并沉默对方 %d 个回合。
		沉默几率随命中增长。
```

## entry-02358
位置：mod-tome.lua:30500；section：mod-tome/data/talents/techniques/finishing-moves.lua；source_tag：_t；args_order：None；special：None

原文：
```text
@Source@ throws a wild haymaker!
```
译文：
```text
@Source@打出狂暴的重拳！
```

## entry-02359
位置：mod-tome.lua:30518；section：mod-tome/data/talents/techniques/grappling.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Make a melee attack for %d%% damage and then attempt to grapple a target up to one size category larger than yourself for %d turns. A grappled opponent will be unable to move, take %d damage each turn, and %d%% of the damage you receive from any source will be redirected to them as physical damage.
		Any movement from the target or you will break the grapple. Maintaining a grapple drains %d stamina per turn.
		You may only grapple a single target at a time, and using any targeted unarmed talent on a target that you're not grappling will break the grapple.
```
译文：
```text
对目标进行一次近战攻击，造成 %d%% 武器伤害并抓取目标（可抓取目标的身材最多比你大 1 级）持续 %d 回合。被钳住的对手将无法移动，每回合受到 %d 物理伤害，同时你从任何来源受到的伤害的 %d%% 将以物理伤害的形式转移至它身上。
		任何目标或你的移动将会打破抓取。维持抓取每回合消耗 %d 体力。
		同时你只能抓取 1 个目标，并且对任意一个你未在抓取中的目标使用指向性徒手技能均会打破抓取。
```

## entry-02360
位置：mod-tome.lua:30524；section：mod-tome/data/talents/techniques/grappling.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your grapples with additional effects. All additional effects will apply to every grapple with no additional save or resist check.
		#RED#Talent Level 1:  Reduces physical power by %d
		Talent Level 3:  Silences
		Talent Level 5:  Reduces global action speed by %d%%
```
译文：
```text
增强你的抓取，获得额外效果，所有效果不需通过其他豁免或抵抗鉴定。
		#RED# 等级 1：减少 %d 物理强度
		等级 3：沉默
		等级 5：目标减速 %d%%
```

## entry-02361
位置：mod-tome.lua:30532；section：mod-tome/data/talents/techniques/grappling.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot move!
```
译文：
```text
你无法移动！
```

## entry-02362
位置：mod-tome.lua:30533；section：mod-tome/data/talents/techniques/grappling.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Rushes forward and attempts to take the target to the ground, making a melee attack for %d%% damage then attempting to grapple them. If you're already grappling the target you'll instead slam them into the ground creating a radius 5 shockwave for %d physical damage and breaking your grapple.
		The grapple effects and duration will be based off your grapple talent, if you have it, and the damage will scale with your Physical Power.
```
译文：
```text
冲向目标，试图将其扑倒在地，进行一次近战攻击造成 %d%% 伤害，然后尝试抓取。如果已在抓取状态，则将目标猛砸向地面，制造冲击波，在半径 5 的范围内造成 %d 物理伤害并解除抓取。
		抓取效果和持续时间取决于你的抓取技能（若已习得），伤害受物理强度加成。
```

## entry-02363
位置：mod-tome.lua:30549；section：mod-tome/data/talents/techniques/magical-combat.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Arcane Combat
```
译文：
```text
奥术格斗
```

## entry-02364
位置：mod-tome.lua:30550；section：mod-tome/data/talents/techniques/magical-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
				
				Currently selected spell: %s
```
译文：
```text

				目前选择的法术：%s
```

## entry-02365
位置：mod-tome.lua:30554；section：mod-tome/data/talents/techniques/magical-combat.lua；source_tag：_t；args_order：None；special：None

原文：
```text
				
				Currently selected spell: Random
```
译文：
```text

				目前选择的法术：随机
```

## entry-02366
位置：mod-tome.lua:30572；section：mod-tome/data/talents/techniques/magical-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The user gains a bonus to Spellpower equal to %d%% of your Cunning (Current bonus: %d).
```
译文：
```text
增加相当于你 %d%% 灵巧的法术强度。目前的法术强度加成：%d。
```

## entry-02367
位置：mod-tome.lua:30576；section：mod-tome/data/talents/techniques/magical-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Raw magical damage channels through the caster's weapon, increasing raw Physical Power by %d%% of your Magic (current bonus: %d).
		Each time you crit with a melee blow, you will unleash a radius %d ball of arcane damage, doing %0.2f.
		The bonus scales with your Spellpower and talent level.
		If you are using a shield this will only occur 50%% of the time.
		If you are dual wielding this will only occur 50%% of the time.
		At level 5 the ball becomes radius 2.
		
```
译文：
```text
通过你的武器来传送原始的魔法伤害。增加相当于你 %d%% 魔法属性值的物理强度（当前值：%d）。
		每当你近战攻击暴击时，你会释放一个半径为 %d 码的奥术属性的魔法球，造成 %0.2f 的伤害。
		增益随法术强度与技能等级提升。
		当使用盾牌时，只有50%% 的几率触发。
		当双持武器时，只有50%% 的几率触发。
		技能等级 5 时，魔法球的半径变成 2。
```

## entry-02368
位置：mod-tome.lua:30603；section：mod-tome/data/talents/techniques/marksmanship.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire a shot at the target tile that blinds enemies for %d turns, marks them for 2 turns and illuminates the area within radius %d for %d turns. Enemies within the illuminated area lose %d defence and stealth power and cannot benefit from concealment.
		The status chance increases with your Accuracy, and the defense reduction with your Dexterity.
```
译文：
```text
发射闪光弹，致盲敌人 %d 回合，标记他们 2 回合并照亮 %d 格范围 %d 回合。范围内的敌人降低 %d 闪避和潜行强度，不能从隐匿技能得到任何加成。
		状态效果几率受命中加成，闪避削减受敏捷加成。
```

## entry-02369
位置：mod-tome.lua:30612；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must be able to move to use %s!
```
译文：
```text
要使用 %s，你必须能够移动！
```

## entry-02370
位置：mod-tome.lua:30613；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
%s is not usable while wearing heavy armour.
```
译文：
```text
%s 在身着重甲时无法使用。
```

## entry-02371
位置：mod-tome.lua:30627；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your quick wit and reflexes allow you to anticipate attacks against you, granting you a %d%% chance to evade melee and ranged attacks and %d increased defense for %d turns.
		The chance to evade and defense bonus increase with your Dexterity.
```
译文：
```text
你的战斗技巧和反射神经让你能迅速躲闪攻击，获得 %d%% 几率躲闪近战与远程攻击，闪避值增加 %d，持续 %d 回合。
		躲闪几率和闪避加成受敏捷加成。
```

## entry-02372
位置：mod-tome.lua:30631；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You must have an empty space to roll to.
```
译文：
```text
你必须有一个空的格子才能翻筋斗过去。
```

## entry-02373
位置：mod-tome.lua:30632；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
In an extreme feat of agility, you move to a spot you can see within range, bounding around, over, or through any enemies in the way.
		This talent cannot be used while wearing heavy armor, and leaves you exhausted.  The exhaustion increases the cost of your activated Mobility talents by %d%% (stacking), but fades over %d turns.
```
译文：
```text
你迅速地移动至范围内可见的位置，跃过路径上所有敌人。
		该技能在身着重甲时不能使用，使用后你会进入疲劳状态，增加移动系技能消耗 %d%% （可以叠加），%d 回合后解除。
```

## entry-02374
位置：mod-tome.lua:30636；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#FIREBRICK##Target# reacts to %s from #Source#, mitigating the blow!#LAST#.
```
译文：
```text
#FIREBRICK##Target# 对#Source#的%s迅速反应，降低了伤害！#LAST#。
```

## entry-02375
位置：mod-tome.lua:30641；section：mod-tome/data/talents/techniques/mobility.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have trained to be very light on your feet and have conditioned your reflexes to react faster than thought to damage you take.
		While this talent is active, you instantly react to any direct damage (not from status effects, etc.) that would hit you for at least %d%% of your maximum life.
		This requires %0.1f stamina and reduces the damage by %d%%.
		Your reactions are too slow for this if you are wearing heavy armour.
		The damage reduction improves with your Defense.
```
译文：
```text
经过训练后，你脚步轻快，神经敏锐。
		技能开启时，你会对达到或超过你 %d%% 最大生命值的直接伤害做出反应（状态效果带来的伤害除外）。
		消耗 %0.1f 体力，你将减少 %d%% 伤害。
		身着重甲时无法使用。
		伤害减免受闪避加成。
```

## entry-02376
位置：mod-tome.lua:30655；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have learned to create and equip specialist ammunition:
Incendiary - Shots deal an additional %d%% weapon damage as fire in a radius %d ball. This cannot occur more than once per turn.
Venomous - Shots deal %0.2f nature damage and inflict numbing poison, dealing a further %0.2f nature damage over 5 turns and reducing all damage dealt by %d%%.
Piercing - Shots reduce armor and saves by %d for 3 turns, and your physical penetration is increased by %d%%.
You can only have 1 type of ammunition loaded at a time.
The poison damage dealt, armor penetration and save reduction will increase with your Physical Power.
```
译文：
```text
你学会了制造和装备专门的弹药：
燃烧弹- 命中后，对目标附近的敌人造成 %d%% 火焰武器伤害，范围最大为 %d，每回合最多一次。
剧毒弹- 命中后，对目标造成 %0.2f 自然伤害并感染麻痹毒素，在 5 回合内造成 %0.2f 自然伤害并削弱其 %d%% 的伤害。
穿甲弹- 命中后，使目标的护甲和豁免减少 %d，持续 3 回合，你的物理穿透增加 %d%%。
同时只能装备一种弹药。
毒素伤害、护甲和豁免削减受物理强度加成。
```

## entry-02377
位置：mod-tome.lua:30667；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Load incendiary ammunition, causing attacks to deal an additional %d%% weapon damage as fire in a radius %d ball around your target. 
		This cannot trigger more than once per turn.
		The damage will scale with your Physical Power.
```
译文：
```text
装填燃烧弹，使你的攻击额外造成 %d%% 武器伤害的火焰伤害，作用于以目标为中心、半径 %d 的范围内。
		该技能每回合最多触发一次。
		伤害受物理强度加成。
```

## entry-02378
位置：mod-tome.lua:30673；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Load venomous ammunition, causing ranged attacks to deal %0.2f nature damage and inflict numbing poison, dealing %0.2f nature damage over 5 turns and reducing all damage dealt by %d%%. 
		The damage will scale with your Physical Power.
```
译文：
```text
装填剧毒弹，使远程攻击对目标造成 %0.2f 自然伤害并感染麻痹毒素，在 5 回合内造成 %0.2f 自然伤害并使其造成的所有伤害降低 %d%%。
		伤害受物理强度加成。
```

## entry-02379
位置：mod-tome.lua:30677；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Load piercing ammunition, causing attacks to reduce the target's armor and saves by %d for 3 turns, and increasing your physical penetration by %d%%.
		The armor and save reduction will scale with your Physical Power.
```
译文：
```text
装填穿甲弹，使目标的护甲和豁免减少 %d 持续 3 回合，你的物理穿透增加 %d%%。
		护甲和豁免削减受物理强度加成。
```

## entry-02380
位置：mod-tome.lua:30682；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires a special shot based on your currently loaded ammo:
Incendiary - Fire a shot that deals %d%% weapon damage as fire and covers targets in radius %d in sticky pitch for %d turns, reducing global speed by %d%% and increasing fire damage taken by %d%%.
Venomous - Fire a shot that deals %d%% weapon damage as nature and explodes into a radius %d cloud of crippling poison for %d turns, dealing %0.2f nature damage each turn and giving affected targets a %d%% chance to fail talent usage.
Piercing - Fire a shot that explodes into a radius %d burst of shredding shrapnel, dealing %d%% weapon damage as physical and removing %d beneficial physical effects or sustains.
The poison damage dealt increases with your Physical Power, and status chance increases with your Accuracy.
```
译文：
```text
根据当前装填的弹药进行一次特殊的射击
燃烧弹- %d%% 火焰武器伤害。在半径 %d 码范围内用粘稠的沥青包裹敌人 %d 回合，减少 %d%% 全局速度并增加其受到的火焰伤害 %d%%。
剧毒弹- %d%% 自然武器伤害。爆炸会形成半径 %d 的致残毒气云，持续 %d 回合，每回合造成 %0.2f 自然伤害并使目标使用技能有 %d%% 几率失败。
穿甲弹- 在半径 %d 码范围内爆炸，造成 %d%% 物理武器伤害，并移除 %d 个有益的物理效果或持续技能。
毒素伤害受物理强度加成，状态触发几率受命中加成。
```

## entry-02381
位置：mod-tome.lua:30692；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You create enhanced versions of your ammunition, granting them additional effects.
Incendiary - The explosion radius is increased by 1, and the ground beneath is ignited dealing an additional %0.2f fire damage each turn for 3 turns.
Venomous - Inflicts leeching poison, dealing %0.2f nature damage over 3 turns and causing you to heal for 100%% of all damage the poison deals to the target.
Piercing - Punctures the target’s armor, increasing all damage they take by %d%% for 3 turns.
You only have a limited amount of this ammo, causing this talent to have a cooldown.
The damage dealt will increase with your Physical Power, and status chance increases with your Accuracy.
```
译文：
```text
你制造出强化版弹药，获得额外效果：
燃烧弹- 爆炸范围增加 1, 点燃地面每回合额外造成 %0.2f 火焰伤害持续 3 回合。
剧毒弹- 感染吸血毒素，3 回合内造成 %0.2f 毒素伤害，毒素造成的 100%% 伤害会治疗你。
穿甲弹- 击穿目标护甲，目标受到的所有伤害增加 %d%% 持续 3 回合。
你的强化版弹药有限，所以技能有冷却时间。
伤害受物理强度加成，状态触发几率受命中加成。
```

## entry-02382
位置：mod-tome.lua:30704；section：mod-tome/data/talents/techniques/munitions.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You mix together your munitions, leading to powerful new effects:
Incendiary - Targets struck by the explosion have their armor and saves reduced by %d for 3 turns, and your physical and fire penetration is increased by %d%%.
Venomous - Shots deal an additional %d%% weapon damage as nature in a radius %d ball, which applies numbing poison as per Exotic Munitions. This cannot occur more than once per turn.
Piercing - Shots deal %0.2f physical damage and maim the target, bleeding them for a further %0.2f physical damage over 5 turns and reducing all damage dealt by %d%%.
The physical damage dealt, armor penetration and save reduction will increase with your Physical Power.
```
译文：
```text
混合你的弹药，造成更强力的效果：
燃烧弹- 受到爆炸袭击的目标护甲和豁免减少 %d 持续 3 回合，你的物理和火焰穿透增加 %d%%.
剧毒弹- 额外造成 %d%% 自然武器伤害，作用于半径 %d 的球形范围，并如同异种弹药一样施加麻痹毒素。每回合最多生效一次。
穿甲弹- 造成 %0.2f 物理伤害并使目标伤残（Maim），在 5 回合内额外流血造成 %0.2f 物理伤害，并使其造成的所有伤害减少 %d%%.
物理伤害、护甲和豁免削减受物理强度加成。
```

## entry-02383
位置：mod-tome.lua:30718；section：mod-tome/data/talents/techniques/pugilism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases your Accuracy by %d, the damage multiplier of your striking talents (Pugilism and Finishing Moves) by %d%%, and reduces all damage taken by %d.
		The offensive bonuses scale with your Dexterity and the damage reduction with your Strength.
```
译文：
```text
增加你 %d 命中。你攻击系技能（拳术、终结技）伤害增加 %d%% , 同时减少 %d 受到的伤害。
		攻击加成（命中与伤害）受敏捷加成，伤害减免受力量加成。
```

## entry-02384
位置：mod-tome.lua:30723；section：mod-tome/data/talents/techniques/pugilism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Deliver two quick punches that deal %d%% damage each, and switch your stance to Striking Stance. If you already have Striking Stance active and Double Strike isn't on cooldown, this talent will automatically replace your normal attacks (and trigger the cooldown).
		If either jab connects, you earn one combo point. At talent level 4 or greater, if both jabs connect, you'll earn two combo points.
```
译文：
```text
对目标进行 2 次快速打击，每次打击造成 %d%% 伤害并使你的姿态切换为攻击姿态，如果你已经在攻击姿态且此技能已就绪，那么此技能会自动取代你的普通攻击（并触发冷却）。
		若任一次打击命中，你获得 1 点连击点。在等级 4 或更高等级时，若两次打击都命中，则获得 2 点连击点。
```

## entry-02385
位置：mod-tome.lua:30740；section：mod-tome/data/talents/techniques/pugilism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Lashes out at the target with three quick punches that each deal %d%% damage.
		Earns one combo point. If your talent level is 4 or greater, this instead earns one combo point per blow that connects.
```
译文：
```text
对目标造成 3 次快速打击，每击造成 %d%% 伤害。
		此攻击使你获得 1 点连击点；在技能等级 4 或更高时，改为每次命中的打击都使你获得 1 点连击点。
```

## entry-02386
位置：mod-tome.lua:30749；section：mod-tome/data/talents/techniques/reflexes.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your reflexes are lightning-fast, if you spot a projectile (arrow, shot, spell, ...) you can instantly shoot at it without taking a turn to take it down.
		You can shoot down up to %d projectiles.
		In addition, your heightened senses also reduce the speed of incoming projectiles by %d%%, and prevents your own projectiles from striking you.
```
译文：
```text
你的反射像闪电一样快，如果你发现一个抛射物（箭矢，弹丸，法术，……）你可以不消耗时间立刻射击之。
		最多可同时击落 %d 个抛射物。
		此外，射向你的抛射物飞行速度下降 %d%%，你的抛射物不再击中你自己。
```

## entry-02387
位置：mod-tome.lua:30755；section：mod-tome/data/talents/techniques/reflexes.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activating this talent enhances your reflexes to incredible levels.  Each time you are attacked in melee, you have a %d%% chance to fire off a defensive shot off in time to intercept the attack, evading it and dealing %d%% archery damage.
		This cannot damage the same target more than once per turn.
```
译文：
```text
激活这个技能将你的反应提升到令人难以置信的水平。每当你被近身攻击，你有 %d%% 几率射出一箭拦截攻击，躲闪攻击并造成 %d%% 弓箭伤害。
		每回合对同一目标最多造成一次伤害。
```

## entry-02388
位置：mod-tome.lua:30760；section：mod-tome/data/talents/techniques/reflexes.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You take close notice of the target for the next 5 turns. If they attempt to use a non-instant talent you react with incredible speed, firing a shot dealing 25%% damage that causes the talent to fail and go on cooldown.
This shot is instant, cannot miss, and puts %d other talents on cooldown for %d turns.
```
译文：
```text
你在接下来的 5 回合内密切关注目标。当其使用非瞬间技能时，你立刻做出反应，射出一箭造成 25%% 伤害打断技能并使其进入冷却。
该攻击为瞬间击中，必中，并使其它 %d 个技能进入冷却 %d 回合。
```

## 相关术语快照
```tsv
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Fade	消隐	T.GAME.TALENT	talents	talent name	existing	core	
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global action speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	效果说明中的全局行动速度全称；沿用界面机制名“全局速度”
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
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
