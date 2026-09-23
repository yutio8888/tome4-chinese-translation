# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03893–entry-03932 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g19-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

## 判断依据与范围

1. 原文/译文及身份以本包和 entries.json 为准；邻近译文仅来自同目录 context.lua。术语只用本包末尾子集；按 source_tag/category/语境匹配，existing 不是强制改名依据。不得读取当前翻译文件、其他实验文件、SPEC/STATE、历史报告或生产结论。
2. 游戏机制以可核验的实际源码行为为准。本体固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC使用source-access列明且哈希固定的公开快照，源码仓库/commit未固定，必须显式标注。DLC机制疑点可陈述快照内已证事实，但目标版本适用性缺口保留待确认，不将引擎commit套用DLC。缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认。英文、术语或旧译不能覆盖源码；沿袭上游的误述和翻译新增分开，不仅凭变量名猜机制。
3. 可读本INPUT、entries.json、context.lua、source-access.json及其中sections列明的本组sources文件。可在这些单文件内搜索。源码缺失已明确列在unavailable_components，不把其他组件同名代码当作它的证据。
4. 追调用链时，本体只能git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<明确相关的单文件path>；DLC只能读取source-access中dlc_additional_sources列明、哈希匹配的相关单文件。每个新增文件说明哪个已读调用/符号/require引入。禁止当前源码工作树、其他commit、整目录git grep/rg/find或历史审核查找；不能读取共享DLC快照中的locales等其他语言答案。证据不足写待确认。
5. 不把问题扩大为全局重命名或术语策略。格式结合实际显示/参数消费判断：保留source_tag、args_order、special；占位符、标记及段落/换行差异只有导致错误参数、错误显示或信息结构丢失时才算缺陷。合法排版和等价重排不算缺陷。

## 四类判定（按以下顺序合并一条内的多个claim）

- **存在问题**：至少一个有可核验证据的错误或遗漏，涉及事实、作用对象/所属关系、数量/条件/范围/时序、玩家操作、语义信息、明确适用的术语要求或运行时格式。轻微并不自动变为建议；必须解释具体哪项信息错误或丢失，不因可自行猜出原意便忽略。
- **待确认**：没有已证实问题，但有具体疑点因证据不足无法定论。指出缺哪项证据。不得把待确认当未发现问题。
- **仅建议**：没有上述问题或未决疑点，仅更自然的措辞、个人偏好、无损排版等；不得将建议计作缺陷。
- **未发现问题**：无上述三类事项。

一条同时有已证实问题和待确认claim，总判定为存在问题，但须分别列出各claim状态。若只有建议和未决claim，总判定为待确认。不同条目重复同一问题仍分别覆盖；同条重复表述不重复计claim。

## 输出

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03893 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03893
位置：tome-orcs.lua:3980；section：tome-orcs/data/talents/celestial/reflection.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creates a wall %d units long for %d turns, reflecting all projectiles that hit it and blocking sight.
```
译文：
```text
创造一堵墙长 %d 持续 %d 回合，反射所有击中此墙的飞行物并且阻挡视线。
```

## entry-03894
位置：tome-orcs.lua:3987；section：tome-orcs/data/talents/celestial/reflection.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summons a clone for %d turns which casts all the spells you cast, dealing %d%% damage and having %d%% health. Additionally, all light damage the clone deals becomes darkness damage and all darkness damage becomes light damage.
```
译文：
```text
召唤一个持续 %d 回合能施放你所有法术的镜像，造成 %d%% 的伤害和拥有 %d%% 生命值。此外，镜像造成的所有光伤害转换为暗影伤害，所有暗影伤害转换为光伤害。
```

## entry-03895
位置：tome-orcs.lua:3994；section：tome-orcs/data/talents/celestial/sol.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fire out an orb of light that deals %0.2f light damage and then returns, dealing the same amount of damage again and reducing the cooldown by half (%d) when it reaches you. The damage will increase with your spellpower. The ball will travel at most %d distance to return to you.
```
译文：
```text
发射一个光球造成 %0.2f 的光伤害然后折返，再次造成相同的伤害并且当回到你身上的时候减少一半 (%d) 的冷却时间。伤害受法术强度加成。球体最多飞行 %d 然后折回你。
```

## entry-03896
位置：tome-orcs.lua:3996；section：tome-orcs/data/talents/celestial/sol.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While sustained, this ability speeds up outgoing projectiles by %d%% while slowing incoming projectiles by %d%%. The increase and decrease improve with your spellpower
```
译文：
```text
开启时，增加发射出去的抛射物 %d%% 速度，减少射向你的抛射物 %d%% 速度。增加和减少随着你的法术强度提高。
```

## entry-03897
位置：tome-orcs.lua:4010；section：tome-orcs/data/talents/celestial/void.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Twilit Echoes
```
译文：
```text
暮光回响
```

## entry-03898
位置：tome-orcs.lua:4011；section：tome-orcs/data/talents/celestial/void.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target feels the echoes of all your light and dark damage for %d turns. 

Light damage slows the target by %0.2f%% per point of damage dealt for %d turns, up to a maximum of %d%% at %d damage.
Dark damage creates an effect at the tile for %d turns which deals %d%% of the damage dealt each turn. It will be refreshed as long as the target continues taking damage from it or another source while Twilit Echoes is active, dealing its remaining damage over the new duration as well as the new damage.
```
译文：
```text
目标会感受到你造成的所有光系和暗影伤害的回响，持续 %d 回合。

每造成 1 点光系伤害，目标便会减速 %0.2f%%，持续 %d 回合；减速上限为 %d%%，造成 %d 点伤害时达到上限。
暗影伤害会在目标所在格产生一个持续 %d 回合的效果，每回合造成该次伤害的 %d%%。在暮光回响生效期间，只要目标继续受到此效果或其他来源的伤害，该地块效果就会刷新；剩余伤害和新伤害会一并分摊到新的持续时间内。
```

## entry-03899
位置：tome-orcs.lua:4020；section：tome-orcs/data/talents/celestial/void.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summons the starscape in the surrounding area in a radius of %d. For %d turns, this area exists outside normal time, and in zero gravity. In addition to the effects of zero gravity, Movement of projectiles and other creatures is three times as slow. Spells and attacks cannot escape the radius until the effect ends.
```
译文：
```text
在 %d 范围内召唤一片星界领域。%d 回合内，这个区域存在于正常时间之外，且重力为零。除了零重力之外，抛射物和生物的活动比平时慢 3 倍。法术和攻击不能逃脱范围，直到效果结束。
```

## entry-03900
位置：tome-orcs.lua:4056；section：tome-orcs/data/talents/misc/npcs.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Slumbering...
```
译文：
```text
沉睡中…
```

## entry-03901
位置：tome-orcs.lua:4064；section：tome-orcs/data/talents/misc/npcs.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03902
位置：tome-orcs.lua:4065；section：tome-orcs/data/talents/misc/npcs.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#ORCHID#%s summons a %s...
```
译文：
```text
#ORCHID#%s召唤了一个%s……
```

## entry-03903
位置：tome-orcs.lua:4066；section：tome-orcs/data/talents/misc/npcs.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#ORCHID#%s summons a %s...
```
译文：
```text
#ORCHID#%s召唤了一个%s……
```

## entry-03904
位置：tome-orcs.lua:4069；section：tome-orcs/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Create a circle of cursed ground (radius %d) for %d turns. Any foes inside will be cursed, all new negative effects on them will have their duration doubled.
		
```
译文：
```text
创造一片诅咒之地（半径 %d 码）%d 回合。任何陷入其中的敌人都会被诅咒，任何他们新得到的负面状态的持续时间都会翻倍。
		
```

## entry-03905
位置：tome-orcs.lua:4077；section：tome-orcs/data/talents/misc/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Summon a storm of swirling sawblades to slice your foes, inflicting %d physical damage and bleeding to anyone who approaches for %d turns.
		The damage and duration will increase with your Mindpower.
```
译文：
```text
召唤由旋转锯刃组成的风暴撕裂敌人，对所有靠近者造成 %d 点物理伤害并使其流血。风暴持续 %d 回合。
		伤害和持续时间随精神强度提高。
```

## entry-03906
位置：tome-orcs.lua:4154；section：tome-orcs/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your yeti's fur acts like a shield, providing %d%% cold resistance, %d%% physical resistance and %d magical save.
```
译文：
```text
你厚实的雪人毛皮能像盾牌一样保护你，为你提供 %d%% 寒冷抗性，%d%% 物理抗性和 %d 魔法豁免。
```

## entry-03907
位置：tome-orcs.lua:4211；section：tome-orcs/data/talents/psionic/action-at-a-distance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Call a streak of lightning on your target, dealing %0.2f to %0.2f lightning damage.
		If it is wet the lightning propagates to all foes in radius %d, doing the same damage to each.
		All affected foes are seared for 4 turns, reducing their fire resistance by %d%% and and mind save by %d.
		The damage will increase with your Mindpower.
```
译文：
```text
召唤一道闪电劈向你的目标，造成 %0.2f 到 %0.2f 闪电伤害。
		如果目标被浸湿了，那么闪电扩散，对半径 %d 码内的所有单位造成同样的伤害。
		所有被劈中的单位都会被烧焦 4 回合，降低他们的火焰抗性 %d%% 和精神豁免 %d。
		伤害受精神强度加成。
```

## entry-03908
位置：tome-orcs.lua:4252；section：tome-orcs/data/talents/psionic/gestalt.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Temporarily expand your mind to force your Gestalt upon your foes in a radius of 5. Up to %d foe(s) will be affected.
		The Gestalt will drain each affected foe's powers (physical power, mind power, spell power and steam power) by %d for 5 turns.
		Your own powers will be increased in return by the drained amount (reduced for each additional foe).
		In addition for 5 turns you can sense creatures beyond your sight, even through walls in radius %d.
		The effects improve with your Mindpower.
```
译文：
```text
暂时延伸你的心灵以使你的格式塔笼罩你周围半径 5 码内的敌人，最多可影响 %d 个敌人。
		格式塔会吸收每个被影响敌人的力量（物理强度，精神强度，法术强度，蒸汽强度）%d 点，持续 5 回合。
		你自身的力量会增加所吸取的数额（每多吸收一个额外的敌人，效果都会衰减）。
		除此之外，在 5 回合内你可以超脱视线的感知半径 %d 码内的生物。
		效果受精神强度加成。
```

## entry-03909
位置：tome-orcs.lua:4361；section：tome-orcs/data/talents/spells/occult-technomancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You imbue a steamsaw with arcane and temporal forces, making it spin very fast around your waist (ignoring requirements).
		The saw spins so fast it it disturbs spacetime around you, increasing your spellpower by up to %d, your spell critical chance by up to %d and your mana regen by up to %0.1f (depending on steamsaw tier).
		Any successful melee attack against you also triggers an automatic steamsaw attack that cannot miss dealing %d%% weapon damage as occult damage (arcane and temporal).
		The steamsaw used will provide its bonus as if it was worn, but you can not Block with it.
		Increases steamsaws weapon damage by %d%% and uses Magic instead of Strength to determine their damage.
		If using Aether Avatar, all Occult Technomancy spells become usable for its duration and all occult damage becomes pure arcane.

		#{italic}#When you first learn this talent you also learn the Steamsaw tinker creation if you didn't already know it.#{normal}#
		
```
译文：
```text
你把奥术和时空能量注入一把蒸汽链锯，让它绕着你的腰飞速旋转（无视装备需求）。
		这把链锯旋转的速度是那么快，它扰乱了你周围的时空。最多增加你 %d 的法术强度，%d 的法术暴击率，和 %0.1f 的法力值恢复（基于蒸汽链锯的材质等级）
		任何对你的成功的近战攻击都会触发一次必定命中的自动的蒸汽链锯反击，造成 %d%% 玄机（奥术和时空）武器伤害。
		使用这种方法装备的蒸汽链锯会提供装备它所提供的属性加成，但你不能使用它来格挡。
		增加蒸汽链锯的武器伤害 %d%%，并在使用蒸汽链锯时用魔力值代替力量值计算伤害。
		如果你激活了以太之体，所有科技法术：玄机系的技能都可以在其持续期间使用，并且所有玄机伤害都会转化为纯净的奥术伤害。

		#{italic}#当你第一次学会这一技能的时候，如果你还没有掌握蒸汽链锯的配方，你还会同时学会这一配方。#{normal}#
		
```

## entry-03910
位置：tome-orcs.lua:4380；section：tome-orcs/data/talents/spells/occult-technomancy.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# annihilates '#Target#'!
```
译文：
```text
#Source#毁灭了'#Target#'！
```

## entry-03911
位置：tome-orcs.lua:4539；section：tome-orcs/data/talents/steam/artillery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You use your rocket pods to launch yourself into the air for 3 turns, firing a radius 2 barrage of rockets that deal %d%% steamgun damage as fire in radius 2. 
		While flying you gain %d%% movement speed, %d%% chance to evade melee and ranged attacks, and can reactivate this talent at will to repeat the rocket barrage.
		Using any talent other than Rocket Barrage will end this effect immediately.
```
译文：
```text
你启动火箭发射器，将自己发射到天空中，持续 3 回合，同时发射范围为 2 的火箭弹幕，在 2 码半径内造成 %d%% 火焰蒸汽枪伤害。
		当处在飞行状态的时候，你获得 %d%% 移动速度，%d%% 几率躲闪近战和远程攻击，并且可以重新激活这个技能，再次发射火箭弹幕。使用任何火箭弹幕之外的技能都会提前终止这一效果。
```

## entry-03912
位置：tome-orcs.lua:4559；section：tome-orcs/data/talents/steam/automated-butchery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You send a saw mounted on an automated steam propulsor to assault a foe, dealing %0.2f physical damage each turn for 4 turns and silencing it.
		At the end of the duration, the saw explodes for %0.2f fire damage and flies back, pulling the target up to %d tiles towards you.
		The damage will increase with your Steampower.
```
译文：
```text
你用自动蒸汽弹射器向敌人发射一把链锯，造成 %0.2f 物理伤害并沉默敌人，持续 4 回合。
		持续时间结束后，链锯爆炸，造成 %0.2f 的火焰伤害并飞回，将目标向你的位置拉扯 %d 格。
		伤害受蒸汽强度加成。
```

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

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cancel	取消	T.UI.LABEL	ui	_t	preferred	global	通用界面按钮（42 处）；对话框/菜单取消操作
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Medical Injector	医疗注射器	T.GAME.TALENT	talents	talent name	preferred	dlc	Embers of Rage 药剂注射技能与植入物选择项名称；统一为“医疗注射器”，不写作“药物注射器”
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Slumber	沉睡	T.GAME.EFFECT	combat	_t	preferred	core	状态名；与同名技能统一
Slumber	沉睡	T.GAME.TALENT	talents	talent name	preferred	core	技能名；指睡眠状态，不是催眠动作
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Twilit Echoes	暮光回响	T.GAME.TALENT	talents	talent name	preferred	dlc	Embers of Rage 黄昏系技能；光系伤害造成减速，暗影伤害生成可由后续伤害刷新的地块效果，统一重复运行时键及状态说明
Yeti	雪人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	兽人战役种族
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
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
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
flesh	肉	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
gestalt	格式塔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
gestalt	格式塔	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
gravity	重力	T.GAME.DAMAGE	combat	damage type	existing	core	
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
medical injector	医疗注射器	T.GAME.ENTITY	items	_t	preferred	dlc	Embers of Rage 用于施用药剂的通用装置；统一实体说明、格式文本与日志中的引用，不写作“医用/药物注射器”
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
occult technomancy	科技法术：玄机	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
reload rate	每次装填弹药数	T.TECH.FORMAT	tech	tformat	preferred	core	弓与投石索机制属性；实际增加每次自动装填的弹药数量，并非缩短装填耗时
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
slumber	沉睡	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	深度睡眠技能类型；与施加催眠的动作区分
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
steamsaw	蒸汽链锯	T.GAME.ENTITY	items	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
technomancy	科技法术	T.GAME.EFFECT	combat	effect subtype	existing	dlc	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
yeti	雪人	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
yeti	雪人	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
```
