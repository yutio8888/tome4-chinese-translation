# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03413–entry-03452 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g07-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03413 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03413
位置：tome-ashes-urhrok.lua:980；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Strike a blow with your weapon for %d%% blight damage.
		If the attack hits a demonic seed tries to take hold inside your foe and you follow up with a shield strike dealing %d%% damage and dazing your target for %d turns.
		
		The seed requires a powerful host to nourish it and can only take hold in creatures that are worth experience and that are not summoned demons.
		The chance for the seed to take hold is based on the creatures rank:
		%sNormal#LAST#:  5%%
		%sElite#LAST#:  20%%
		%sRare#LAST# or %sUnique#LAST#:  50%%
		%sBoss#LAST#:  100%%
		When the host dies the seed fills with the vim of the dying creature and turns into a specific demon seed that can be used to summon that demon.
		If you already have a seed of the same time in your inventory or equipment it will instead increase its level if the host was of higher level than the seed and the demon inside will regenerate %d%% health and resurrect if it was dead.

		Higher talent levels allow for more powerful demon types.
		Implanting a seed into unique demons, if successful, will always try to grant a seed of that type, if available.
```
译文：
```text
对目标造成 %d%% 枯萎武器伤害。
		如果攻击命中，你会将恶魔种子植入目标体内，然后用盾牌攻击目标，造成 %d%% 盾牌伤害并眩晕 敌人 %d 回合。

		种子需要足够强大的宿主来成长，它只能寄生在值得获取经验值的生物体内，不能寄生在被召唤的恶魔体内。
		种子的存活几率基于宿主的级别：
		%s普通生物#LAST#:5%%
		%s精英生物#LAST#:20%%
		%s稀有#LAST#与%s史诗生物#LAST#:50%%
		%sBoss#LAST#:100%%
		当宿主死亡时，种子将吸收宿主的活力，成长为一个特定的恶魔种子，能用于召唤恶魔。
		如果你的背包或装备上已经有了同类的恶魔种子，且宿主等级高于恶魔的等级，它会提升种子的等级。此外，里面的恶魔会恢复 %d%% 生命值，如果已死则会被复活。

		高技能等级将带来更强大的种子。
		如果成功将种子植入史诗生物（Unique）的体内，且它有对应的恶魔种子的话，你必定会获得该恶魔种子。
```

## entry-03414
位置：tome-ashes-urhrok.lua:1010；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03415
位置：tome-ashes-urhrok.lua:1035；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select a teleport location...
```
译文：
```text
选择传送位置…
```

## entry-03416
位置：tome-ashes-urhrok.lua:1037；section：tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Teleports you randomly within a small range of up to %d grids with %d precision.
		In the spot you left you will summon a random demon from your seeds for %d turns.
		If the target area is not in line of sight, there is a chance the spell will fizzle.
		This spell requires an unsummoned, alive, demon seed equiped in a worn equipment to work.
		The range will increase with your Spellpower.
```
译文：
```text
传到 %d 码外的一个位置，误差 %d。
		在离开的位置，你将随机召唤一个恶魔，持续 %d 回合。
		如果目标地点不在视线内，有一定几率失败。
		该技能需要你的装备上附着有至少一个未召唤的存活的恶魔种子。
		传送距离受法术强度加成。
```

## entry-03417
位置：tome-ashes-urhrok.lua:1075；section：tome-ashes-urhrok/data/talents/corruptions/demonic-strength.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Demonic Blood flows through your veins, increasing your spellpower by %d and your maximum vim by %d.
		Additionally, you will recieve a bonus to all damage equal to %d%% of your current vim (Currently %d%%).
```
译文：
```text
你体内涌动着恶魔之血，增加 %d 点法术强度和 %d 点活力上限。
	同时获得相当于当前活力 %d%% 的全伤害加成（当前 %d%%）。
```

## entry-03418
位置：tome-ashes-urhrok.lua:1079；section：tome-ashes-urhrok/data/talents/corruptions/demonic-strength.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with a defensive aura, increasing armor by %d, and inflicting %0.2f fire and %0.2f blight damage to all attacking foes.
Additionally, your vim will enhance your defences, reducing all damage by %d%% of your current vim (currently %d), but never reducing by more than half of the original damage. This will cost vim equal to 5%% of the damage blocked.
The damage will scale with your Spellpower.
```
译文：
```text
深渊气息围绕着你，增加 %d 点护甲，增加 %0.2f 点火焰、%0.2f 点枯萎近战反击伤害。
	同时你的活力会增强你的防御，减少相当于当前活力 %d%% 的伤害（目前为 %d 点），但不会减少超过原伤害的一半。此效果会消耗等同于 5%% 减少伤害值的活力。
	伤害值受法术强度加成。
```

## entry-03419
位置：tome-ashes-urhrok.lua:1089；section：tome-ashes-urhrok/data/talents/corruptions/doom-covenant.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your affinity for the shadows grow stronger.
		Whenever one of your spells deal darkness damage you have a %d%% chance to gain 8%% to all damage affinity for 8 turns.
		If you kill a creature with darkness damage this effect always triggers.
		You can only gain one stack of Dark Reign per turn.
		This effect stacks multiplicatively up to %d times.
```
译文：
```text
你与阴影的联系更加紧密了。
		每次你使用法术造成暗影伤害时，你有 %d%% 几率获得 8%% 全体伤害亲和，持续 8 回合。
		如果你用暗影伤害杀死一个生物，这一效果必定触发。
		你每回合最多只能获得一层黑暗支配效果。
		这个效果能叠加至最多 %d 层。
```

## entry-03420
位置：tome-ashes-urhrok.lua:1113；section：tome-ashes-urhrok/data/talents/corruptions/doom-covenant.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Pay %d%% of your current life and gain 100%% darkness damage conversion for 1 turns.
			If Dark Reign is active you also gain %d stamina and %d vim per stack.
```
译文：
```text
支付 %d%% 当前生命值，1 回合内你造成的所有伤害转化为黑暗伤害。
		如果黑暗支配开启，每有一层，你获得 %d 体力与 %d 活力。
```

## entry-03421
位置：tome-ashes-urhrok.lua:1144；section：tome-ashes-urhrok/data/talents/corruptions/doom-shield.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Taking example from Mal'Rok, the demon's homeworld you harden yourself.
		Increases total armour by %d%% + 10 and spellpower by %d.
```
译文：
```text
从恶魔家乡玛·洛克中学习，强化自身。
		增加 10 + %d%% 总护甲值，获得 %d 法术强度。
```

## entry-03422
位置：tome-ashes-urhrok.lua:1152；section：tome-ashes-urhrok/data/talents/corruptions/doom-shield.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your shield is infused with a powerful blight. Anytime you block and apply a counterstrike effect the target is also afflicted by a curse of impotence.
		Cursed creatures have all their damage decreased by %d%% for 5 turns.
		The effects will improve with your Spellpower.
```
译文：
```text
你的盾牌充满强大的枯萎能量。每次你格挡并附加反击状态时，目标将被虚弱诅咒感染，5 回合内降低 %d%% 伤害。
		效果受法术强度加成。
```

## entry-03423
位置：tome-ashes-urhrok.lua:1162；section：tome-ashes-urhrok/data/talents/corruptions/fearfire.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-03424
位置：tome-ashes-urhrok.lua:1163；section：tome-ashes-urhrok/data/talents/corruptions/fearfire.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Open a gateway to the Fearscape, stepping through it to a nearby location. As you step out, a burst of fire will leave with you, dealing %0.2f demonfire damage to everyone within %d spaces and leaving flames which will deal an additional %0.2f demonfire damage over 4 turns.
		Additionally, shifting through reality enhances your awareness, allowing you to see all enemies within %d spaces for the next 3 turns.
		The damage will scale with your Spellpower and the range will increase with the talent level.
```
译文：
```text
开启通往恶魔空间的炼狱之门，踏入并传送到附近位置。
	当你踏出炼狱之门时，炼狱之火随之喷发，造成 %0.2f 恶魔之火伤害，伤害 %d 码内所有生物。地上的余烬会造成持续 4 回合的额外 %0.2f 恶魔之火伤害。

	穿越空间增强了你的直觉，让你能够在 4 回合内觉察到 %d 码内的所有敌对生物。

	伤害受法术强度加成，范围随技能等级增大。
```

## entry-03425
位置：tome-ashes-urhrok.lua:1172；section：tome-ashes-urhrok/data/talents/corruptions/fearfire.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Removes all detrimental effects but causes you to burn for %d%% of your max health per effect, over 7 turns.
		This ignores all resists, defenses, and affinities.
		This does not take a turn.
```
译文：
```text
移除所有负面状态，但每移除一个状态，会在 7 回合内灼烧自身，受到合计 %d%% 最大生命值的伤害。
	伤害无视一切抗性、防御效果和伤害亲和。

此技能瞬发。
```

## entry-03426
位置：tome-ashes-urhrok.lua:1179；section：tome-ashes-urhrok/data/talents/corruptions/fearfire.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Exhale a wave of dark fire with radius %d, lasting 4 turns. Any non-demon caught in the area will take %0.2f fire damage, and flames will be left dealing a further %0.2f each turn. Demons will be healed for the same amount.
		The damage will increase with your Strength Stat, but critically hit as a spell.
```
译文：
```text
在 %d 码的锥形范围内，喷出持续 4 回合的暗黑火焰。
	范围内所有的非恶魔生物受到 %0.2f 火焰伤害，同时火焰会造成每回合 %0.2f 的灼烧伤害。
	恶魔受到等量的治疗。

	伤害受力量加成，该技能使用魔法暴击率。
```

## entry-03427
位置：tome-ashes-urhrok.lua:1209；section：tome-ashes-urhrok/data/talents/corruptions/heart-of-fire.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Restore yourself to full health, but take damage equal to the damage healed over %d turns. This damage is split evenly among you and all burning enemies in radius %d. Damage you take is irresistable. Damage to enemies is fire damage.
```
译文：
```text
生命值恢复为满值，但治疗值转化为持续 %d 回合的伤害。
	伤害会平均分配给你自己和 %d 码范围内的燃烧敌对生物。
	你受到的伤害无法减免，敌对生物受到火焰伤害。
```

## entry-03428
位置：tome-ashes-urhrok.lua:1231；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select the source:
```
译文：
```text
选择源生物：
```

## entry-03429
位置：tome-ashes-urhrok.lua:1232；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select the victim:
```
译文：
```text
选择受害者：
```

## entry-03430
位置：tome-ashes-urhrok.lua:1233；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using demonic forces you create a link of pain from a source creature to a victim for %d turns.
		Each time the source creature takes damage the victim takes %d%% of the damage.
		If the victim dies from the effect you gain a burst of energy, reducing all remaining cooldowns by 1.
```
译文：
```text
使用恶魔之力，你在源生物与牺牲生物间构造痛苦链接，持续 %d 回合。
		每次源生物受到伤害时，%d%% 伤害由牺牲生物承受。
		当牺牲生物因此效果死亡时，你将获得能量，减少所有技能冷却时间 1 回合。
```

## entry-03431
位置：tome-ashes-urhrok.lua:1241；section：tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Demon horns temporarily grow on your shield as you bash a foe with it for %d%% damage.
		If the attack hits the creature is impaled by the horns, causing it to bleed black blood for 50%% of the damage done as darkness over 5 turns.
		Any time you damage this foe in melee while it bleeds you get healed for %d (this can only happen once per turn).
		The healing power increases with your spellpower.
```
译文：
```text
你的盾牌上长出临时的恶魔之角。
		你盾击敌人造成 %d%% 伤害。
		如果攻击命中，目标将被恶魔角刺穿，流血 5 回合，合计受到额外 50%% 黑暗伤害。
		每次你攻击被恶魔角刺穿的目标时，你回复 %d 生命（每回合至多 1 次）。
		治疗效果受法术强度加成。
```

## entry-03432
位置：tome-ashes-urhrok.lua:1256；section：tome-ashes-urhrok/data/talents/corruptions/npcs.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s (demonic husk)
```
译文：
```text
%s（恶魔尸傀）
```

## entry-03433
位置：tome-ashes-urhrok.lua:1273；section：tome-ashes-urhrok/data/talents/corruptions/oppression.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your successful melee hits apply a stacking effect that decreases damage done by %d%%.
		You can have up to %d stacks per target and further attacks refresh the duration, but any turn you are farther than %d spaces from the victim the fear will wear off quickly.
		At level 3 it also slows by %0.2f%% per stack.
		At level 5 you can horrify enemies in a radius of %d.
		This talent ignores saves and immunities.
		
```
译文：
```text
你的攻击能够惊吓目标，降低目标 %d%% 的伤害。
	此效果可以叠加 %d 次，每次攻击会刷新持续时间。但是当目标与你距离超过 %d 码，恐惧效果会迅速消退。
	技能 3 级时，每次叠加会同时减少目标 %0.2f%% 的速度。
	技能 5 级时，可以影响到 %d 码内的所有敌对生物。
	此技能无视豁免和免疫。
```

## entry-03434
位置：tome-ashes-urhrok.lua:1344；section：tome-ashes-urhrok/data/talents/corruptions/torture.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hits the target with your weapon doing %d%% weapon damage. If the attack hits, the target is afflicted with Fiery Torment for %d turns, reducing their fire resistance by %d%%.
		When Fiery Torment ends the victim will take %d fire damage. This damage will increase by %d%% of all damage taken while under torment.
		The damage dealt by the effect will increase with spellpower.
		Demons under fiery torment will be burned by the flames of the Fearscape.
```
译文：
```text
用武器攻击敌人，造成 %d%% 武器伤害。如果命中，目标受到灼魂之罚的影响，持续 %d 回合，火焰抗性降低 %d%%。
	当灼魂之罚结束，敌人会受到 %d 点火焰伤害。
	在灼魂之罚持续时间内目标受到的所有伤害，有 %d%% 会加成到火焰伤害中。
	效果的伤害会随法术强度提升。
	被灼魂之罚影响的恶魔会被恶魔空间中的火焰焚烧。
```

## entry-03435
位置：tome-ashes-urhrok.lua:1368；section：tome-ashes-urhrok/data/talents/corruptions/wrath.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You require a two handed weapon and being able to move to use this talent.
```
译文：
```text
你需要装备一把双手武器且可以移动，才能施展这个技能。
```

## entry-03436
位置：tome-ashes-urhrok.lua:1382；section：tome-ashes-urhrok/data/talents/corruptions/wrath.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your body overflows with the power of the Fearscape, turning you into a powerful demon for %d turns. This increases your stamina regen and physical power by %d, and your disarm and stun immunity by %d%%.
		The physical power, stamina regen, and status resistances increase with your spellpower.
		Your other talents also gain a variety of bonuses:
		-Draining Assault: Reduces cooldown by %d.
		-Reckless Strike: Gain %d%% resistance penetration for all elements for %d turns.
		-Obliterating Smash: Increases range by %d.
		-Abduction: If it hits, get an additional %d attacks at 35%% weapon damage.
		-Incinerating Blows: Increases chance of bonus damage to %d%%.
		-Fearfeast: Gain %0.1f vim per stack.
		-Maw of Urh'rok: Increases cone width by %d degrees.
```
译文：
```text
恶魔空间的力量充溢了你的身体，将你转换成一个强大的恶魔，持续 %d 回合。
	变身期间，体力恢复和物理强度增加 %d，缴械和震慑抗性增加 %d%%。
	物理强度、体力恢复和状态抗性加值受法术强度加成。
	变身期间，其他技能也受到强化：
	汲魂痛击：冷却时间减少 %d。
	舍身一击：增加 %d%% 全体抗性穿透，持续 %d 回合。
	歼灭挥斩：增加半径 %d。
	锁魂之链：如果命中，额外附加 %d 次 35%% 武器伤害的攻击。
	焚尽强击：增加额外伤害几率至 %d%%。
	恐惧盛宴：每汲取一层叠加的恐惧，获得 %0.1f 点活力。
	乌鲁洛克之口：角度增加 %d。
```

## entry-03437
位置：tome-ashes-urhrok.lua:1411；section：tome-ashes-urhrok/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Hasten yourself out of phase, teleporting you to a specific location up to %d spaces away.
		You can activate this talent up to twice within the same turn, but the second activation will not be instant.
		Afterwards you stay out of phase for 5 turns. In this state your defense is increased by %d and all your resistances by %d%%.
		The bonus will increase with your Willpower.
```
译文：
```text
加速自身，以至于脱离空间，传送半径 %d。
		你在同一回合内至多连用两次该技能，且第二次使用会消耗时间。
		之后，你停留在相位外 5 回合，闪避增加 %d，全体抗性增加 %d%%。
		效果受意志加成。
```

## entry-03438
位置：tome-ashes-urhrok.lua:1423；section：tome-ashes-urhrok/data/talents/misc/races.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your original invisibility talent was corrupted and twisted.
		You have %d%% chance to turn into a dúathedlen for 5 turns, when hit by a blow doing at least 10%% of your total life.
		While in this form you gain the following effects:
		- you have permanent stealth (power %d)
		- your darkness damage is increased by %d%%
		- any non mind and non physical damage you deal above %d triggers a darkness explosion of radius 1 for half the damage (this can only happen once per turn)
		- when you transform the cooldowns of Haste of the Doomed and Pitiless are reset
		
```
译文：
```text
你原本的隐身技能被腐化扭曲了。
		当你受到一次至少为你总生命值 10%% 的伤害时，有 %d%% 几率转变成多瑟顿形态 5 回合。
		在多瑟顿形态下：
		- 你获得永久潜行 (强度 %d)
		- 你的暗影伤害增加 %d%%
		- 每当你造成超过 %d 点的非物理非精神伤害时，在半径 1 的范围内产生一次暗影爆炸，造成额外 50%% 伤害（每回合至多 1 次）。
		- 变形时重置种族技能“末日加速”与种族技能“无情”
		
```

## entry-03439
位置：tome-ashes-urhrok.lua:1449；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# imbues its weapon with demonic fire.
```
译文：
```text
#Target#用恶魔之火给武器附魔。
```

## entry-03440
位置：tome-ashes-urhrok.lua:1451；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s weapon looks less threatening.
```
译文：
```text
#Target#的危险度看起来降低了。
```

## entry-03441
位置：tome-ashes-urhrok.lua:1478；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s is no longer blazing.
```
译文：
```text
#Target#不再闪耀。
```

## entry-03442
位置：tome-ashes-urhrok.lua:1497；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# suffers!
```
译文：
```text
#Target# 被折磨！
```

## entry-03443
位置：tome-ashes-urhrok.lua:1505；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Damage from soulburn.
```
译文：
```text
来自灵魂燃烧的伤害。
```

## entry-03444
位置：tome-ashes-urhrok.lua:1538；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Infected by a demon seed. When it dies the caster has a %d%% chance to get back the matured seed.
```
译文：
```text
目标被恶魔之种感染，死亡时施法者有 %d%% 几率获得成熟的种子。
```

## entry-03445
位置：tome-ashes-urhrok.lua:1550；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Gain %d%% resistance and %d%% affinity to acid.
```
译文：
```text
获得%d%% 酸性抗性与 %d%%酸性伤害亲和。
```

## entry-03446
位置：tome-ashes-urhrok.lua:1597；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#ORANGE##Source# shares some pain with #target#!#LAST#
```
译文：
```text
#ORANGE##Source#与#target#共享痛苦！#LAST#
```

## entry-03447
位置：tome-ashes-urhrok.lua:1612；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
All damage affinity increased by %d%%.
Will not die until %d life
```
译文：
```text
全体伤害亲和增加 %d%%。
生命值不低于 %d 时不会死亡。
```

## entry-03448
位置：tome-ashes-urhrok.lua:1625；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have %d charges.
```
译文：
```text
叠加次数：%d。
```

## entry-03449
位置：tome-ashes-urhrok.lua:1628；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The target is surrounded by a fire haven, granting 40% fire damage affinity but -15% to blight resistance.
```
译文：
```text
目标被火焰庇护围绕，获得 40% 火焰伤害亲和，但减少 15% 枯萎抗性。
```

## entry-03450
位置：tome-ashes-urhrok.lua:1637；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Triggers Blood Drinker if this creature dies.
```
译文：
```text
这个生物死后会触发饮血者效果。
```

## entry-03451
位置：tome-ashes-urhrok.lua:1641；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：effect subtype；args_order：None；special：None

原文：
```text
affinity
```
译文：
```text
伤害亲和
```

## entry-03452
位置：tome-ashes-urhrok.lua:1643；section：tome-ashes-urhrok/data/timed_effects.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
All damage affinity increased by %d%%.
```
译文：
```text
全体伤害亲和提升%d%%。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
All Resists	全部抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 All Resists 行；对应 resists.all
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cursed	被诅咒者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Haste of the Doomed	末日加速	T.GAME.TALENT	talents	talent name	preferred	dlc	Ashes of Urh'Rok 魔化精灵种族技能；保留 of the Doomed 限定，不缩写为“加速”
Horns	角	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Out of Phase	脱离现实	T.GAME.EFFECT	combat	_t	preferred	core	传送后获得的相位状态名；统一沿用效果定义，不泛化为“传送后加成”
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cursed	诅咒	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fearscape	恶魔空间	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
