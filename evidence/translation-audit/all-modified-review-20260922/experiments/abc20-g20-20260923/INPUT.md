# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03933–entry-03972 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g20-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

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

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03933 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


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

## entry-03953
位置：tome-orcs.lua:5416；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires your ammo at an enemy in range %d for %d%% weapon damage.  If this tinker is made of voratun you will fire an additional shot.
			This shot is a ranged melee attack but will use the ranged procs of your ammo as well.
```
译文：
```text
向在 %d 码范围内的一个敌人开火造成 %d%% 的武器伤害。如果手炮是由沃瑞钽钢制作的，你能多一次额外的射击。射击是远程攻击将会触发弹药特效。
```

## entry-03954
位置：tome-orcs.lua:5419；section：tome-orcs/data/talents/steam/other.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03955
位置：tome-orcs.lua:5422；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Quickly create a psionic-enhanced metal contraption that lures all your foes to it and reflects %d%% of the damage it takes to its attackers.
		The contraption will have %d life and last 5 turns.
		Damage, life, resists, and armor scale with your Steampower.
```
译文：
```text
快速制造一个灵能强化的金属装置，吸引所有敌人攻击它，并将其所受伤害的 %d%% 反弹给攻击者。
该装置拥有 %d 点生命值，持续 5 回合。
其伤害、生命值、抗性和护甲随你的蒸汽强度提升。
```

## entry-03956
位置：tome-orcs.lua:5437；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the pistons to crush your target for %d turns and dealing %d%% unarmed melee damage.
		While the target is held it can not move and its armour and defense are reduced by %d.
		#{italic}#Crush their bones!#{normal}#
```
译文：
```text
激活活塞碾压你的目标 %d 回合，并造成 %d%% 的徒手伤害。
被碾压的目标会被定身，且其护甲和闪避减少 %d。
#{italic}#压碎他们的骨头 !#{normal}#
```

## entry-03957
位置：tome-orcs.lua:5444；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Grab the target and pull them towards you, striking for %d%% unarmed melee damage, and if you hit, pinning them for %d turns.
```
译文：
```text
抓住目标把目标向你拉拢，造成 %d%% 的徒手伤害，如果命中，目标定身 %d 回合。
```

## entry-03958
位置：tome-orcs.lua:5470；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a cone of blighted needles, hitting everything in a frontal cone of radius %d for %0.2f physical damage.
		Each creature hit has a %d%% chance of being infected by a random disease, doing %0.2f blight damage and reducing either Constitution, Strength or Dexterity by %d for 20 turns.
		The damage and disease effects increase with your Steampower.
```
译文：
```text
你射出一片枯萎的针，打击 %d 码锥形范围内的目标，造成 %0.2f 的物理伤害。
每个命中目标都有 %d%% 几率感染一种随机疾病，造成 %0.2f 枯萎伤害同时降低体质，力量或敏捷 %d 点持续 20 回合。
		伤害和疾病效果受蒸汽强度加成。
```

## entry-03959
位置：tome-orcs.lua:5476；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s shreds through sandwalls!
```
译文：
```text
%s 挖开沙墙！
```

## entry-03960
位置：tome-orcs.lua:5483；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a cone of healing with radius %d, healing other mechanical creatures (steam spiders) for %d.
		The healing will increase with your Steampower.
```
译文：
```text
释放一片锥形半径 %d 码的修理器，修复机械生物（蒸汽蜘蛛）%d 生命值。
　　治疗量受蒸汽强度加成。
```

## entry-03961
位置：tome-orcs.lua:5486；section：tome-orcs/data/talents/steam/other.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Arcane Disruption Wave
```
译文：
```text
奥术干扰波
```

## entry-03962
位置：tome-orcs.lua:5492；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Shatters the mind of your victim, giving you full control over its actions for 6 turns.
		When the effect ends, you pull out your mind and the victim's body collapses, dead.
		This effect does not work on rares, bosses, or undead.
		.
```
译文：
```text
粉碎你的受害者的内心，给你完全控制其行为 6 回合。
　　当效果结束时，你抽出了自己的思维，受害者的身体会崩溃，死亡。
　　稀有怪、boss、亡灵不受控制。
```

## entry-03963
位置：tome-orcs.lua:5508；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a handful of dust that rapidly oxidises, releasing a blinding light.
		Creatures in a cone of radius %d are blinded for %d turns.
		The blindness effect is applied with your Steampower.
```
译文：
```text
扔一把尘土，迅速氧化，释放出眩目的光芒。
		致盲锥形半径 %d 码内的生物 %d 回合。
		致盲强度受蒸汽强度加成。
```

## entry-03964
位置：tome-orcs.lua:5515；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a handful of dust that is very itchy to touch.
		Creatures in a cone of radius %d are itchy for %d turns, causing them to fail talents %d%% of the time.
		The itchiness effect is applied with your Steampower.
```
译文：
```text
释放一把痒痒粉。
		锥形半径 %d 码内的生物 %d 回合内很痒，导致它们释放技能 %d%% 几率失败。
		致痒强度受蒸汽强度加成。
```

## entry-03965
位置：tome-orcs.lua:5521；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the explosion!
```
译文：
```text
%s 抵抗了爆炸！
```

## entry-03966
位置：tome-orcs.lua:5522；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a grenade at your foes, dealing %0.2f physical damage in radius %d.
		Creatures hit will also be stunned for %d turns.
		The stun effect is applied with your Steampower.
```
译文：
```text
向你的敌人投掷手榴弹，造成 %0.2f 物理伤害，半径 %d 码。
　　目标也会震慑 %d 回合。
　　震慑强度受蒸汽强度加成。
```

## entry-03967
位置：tome-orcs.lua:5552；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special explosive shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it does normal steamgun damage and explodes within radius %d, which does %0.2f physical damage.
		This talent does not use ammo as it is the ammo.
```
译文：
```text
你使用蒸汽枪在射程内制造一场特殊的爆炸。
　　当每一个弹片击中它的目标，造成正常蒸汽枪伤害和半径 %d 码内的爆炸，造成 %0.2f 的物理伤害，
　　这个技能不使用弹药。
```

## entry-03968
位置：tome-orcs.lua:5573；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-03969
位置：tome-orcs.lua:5593；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the pull!
```
译文：
```text
%s抵抗了拖动！
```

## entry-03970
位置：tome-orcs.lua:5594；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special hook shot with your steamgun(s) at a target creature or location.
		If you target a creature, they are pulled up to %d tiles towards you.
		If you target an empty tile, you are pulled up to %d tiles towards it.
		This talent does not use ammo as it is the ammo.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标或某处
如果你的目标是一个生物，他们被拉向你 %d 码
如果你的目标是一个空地，你会被拉向空地 %d 码
这个技能不使用弹药。
```

## entry-03971
位置：tome-orcs.lua:5610；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special voltaic shot with your steamgun(s) at a target for 100%% weapon damage as lightning.
		The shot will release powerful electrical currents at up to %d nearby enemies. 
		Each bolt does %0.2f lightning damage.
		This talent does not use ammo as it is the ammo.
		Bolt damage scales with Steampower.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标造成 100%% 闪电武器伤害。
这将释放强大的电流，打击周围 %d 的敌人。
每个闪电球造成 %0.2f 的闪电伤害
这个技能不使用弹药
闪电球伤害受蒸汽强度加成。
```

## entry-03972
位置：tome-orcs.lua:5628；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special botanical shot with your steamgun(s) at a target for 100%% weapon damage as nature.
		The shot will release spores which grow into Nourishing Moss in a radius of %d for %d turns.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss has vampiric properties and heals the user for %d%% of the damage done.
		This talent does not use ammo as it is the ammo.
		Moss damage scales with Steampower.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标造成 100%% 自然武器伤害。
将释放孢子生长成半径 %d 的苔藓 %d 回合。
每回合苔藓造成 %0.2f 自然伤害对半径内的每一个敌人。
这种苔藓有吸血特性，伤害的 %d%% 治愈使用者。
这个技能不使用弹药
苔藓伤害受蒸汽强度加成。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
chemical	化学	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mechanical	机械	T.GAME.ENTITY	creatures	entity type	existing	dlc	Embers of Rage 实体类型
mecharachnid	机械蜘蛛	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
steamsaw	蒸汽链锯	T.GAME.ENTITY	items	entity subtype	existing	dlc	Embers of Rage 实体子类型
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
voratun	沃瑞钽	T.GAME.ENTITY	items	entity subtype	preferred	global	最高级金属材料（22 处）；与 iron 铁、steel 钢并列
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
