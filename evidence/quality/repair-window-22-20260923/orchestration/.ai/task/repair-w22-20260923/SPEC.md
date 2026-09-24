# 修复窗口22：268批6条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线fe25b62530506305364476e175ed7c5884b7018b。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的6个target及evidence/quality/repair-window-22-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致（多段条目逐行比对空行位置，不只看总数）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证，并查同技能/同物品相邻条目已用译法），不自行新造。

6条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰6个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核269。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 欺诈斗篷生效日志（timed_effects/other.lua:2614，tformat）：making %s appear human——效果设 fake_race="Human"，是伪装成人类；改为“……让%s看起来像人类”一类。#LIGHT_BLUE#、#Target#、%s 保持。
- 电鳗尾炼金说明（ingredients.lua:156）：It doesn't much matter 为“其实没多大关系/无所谓”；其余逐句对照（Where does the eel stop and the tail start? 为“电鳗从哪儿算起、尾巴从哪儿开始？”一类）。
- 厄奇斯成就说明（achievements/quests.lua:219）：Freed Derth from the onslaught of the mad Tempest, Urkis. 补出 mad（疯狂的）与 onslaught（猛攻/肆虐）；Tempest 沿用本条现有“风暴魔导师”，德斯镇、厄奇斯沿用现译。
- 挂坠说明（general/objects/world-artifacts-far-east.lua:58）：a hematite moon eclipsing a golden sun——赤铁矿之月遮蔽金色太阳（unided_name 为 gray and gold pendant，不要写“红月”）；其余逐句对照。
- 腐化蒸汽（talents/misc/npcs.lua:1386，Blightzone info，tformat）：Corrupted vapour rises at the target location (radius 4)——补主语“腐化的蒸汽在目标位置升起”（半径 4），%0.2f/%d 顺序与 \n\t\t 保持；“码”与本库半径写法一致即可。
- 分裂 Mitosis（talents/gifts/ooze.lua:112–118，tformat）：补 nearby within your line of sight（在附近视线内）、(limited by talent level and the summoning limit)、so long as this talent is active（仅在本技能生效期间均摊），take damage 译“受到伤害”；%d/%0.2f/%d/%d/%d%%/%s 顺序与每行 \n\t\t 保持，逐行对照 7 行结构。浮肿软泥怪沿用现译。

## f7641a73ef53957fb0485b33b1aa7d135467409f556f72c351b6150f004e95af

section: mod-tome/data/timed_effects/other.lua
source_tag: tformat

source: #LIGHT_BLUE#An illusion appears around #Target# making %s appear human.

target: #LIGHT_BLUE##Target#周围的幻影让%s看起来像活着一样。

确认依据：timed_effects/other.lua:2614 CLOAK_OF_DECEPTION on_gain：斗篷在不死族身上制造幻象使其 appear human（看起来像人类，从而能进入人类城镇）；现译“看起来像活着一样”把“人类”换成“活着”，外观含义改变。整条修复为“看起来像人类”一类，#LIGHT_BLUE#/#Target#/%s 保持。
与 surface 同向并补充：timed_effects/other.lua:2604–2621 CLOAK_OF_DECEPTION long_desc 为 making it look human，activate 设 fake_race="Human"、fake_subrace="Cornac" 并改阵营为 allied-kingdoms；是伪装成人类而非“像活着”。整条修复为“看起来像人类”。

## f78b208ac1339275462eccbe631bfdb774062c7b7176b047b072786b7987612e

section: mod-tome/data/ingredients.lua
source_tag: _t

source: I know, I know. Where does the eel stop and the tail start? It doesn't much matter. The last ten inches or so should do nicely.

target: 我知道，我知道。你想问电鳗的尾巴是哪一段？没有确切的答案。最后 10 英寸或许是最合适的。

确认依据：ingredients.lua 电鳗尾 desc：It doesn't much matter 意为“其实没多大关系”（紧接“最后十英寸左右就行”）；现译“没有确切的答案”语义改变。整条逐句核对后修复。

## f7bd4de1f91451ebe16d1927f0b5ce047318d81002068752738c63bd9ff08cf8

section: mod-tome/data/achievements/quests.lua
source_tag: _t

source: Freed Derth from the onslaught of the mad Tempest, Urkis.

target: 从风暴魔导师厄奇斯手里成功解救德斯镇。

确认依据：achievements/quests.lua:219：Freed Derth from the onslaught of the mad Tempest, Urkis.——现译“从风暴魔导师厄奇斯手里成功解救德斯镇”漏译 mad（疯狂的）与 onslaught（猛攻）。整条修复，Tempest 沿用本条现有“风暴魔导师”，不扩大为族内统一。

## f8180dfe1116080a85bf70f93352e02f2f613a4f0d5d83fc1d58e13f6d509456

section: mod-tome/data/general/objects/world-artifacts-far-east.lua
source_tag: _t

source: This small pendant depicts a hematite moon eclipsing a golden sun and according to legend was worn by one of the Sunwall's founders.

target: 一个小小的垂饰，雕刻着红月吞日的图案。传说其主人是太阳堡垒的建立者之一。

确认依据：general/objects/world-artifacts-far-east.lua:58 挂坠 desc：a hematite moon eclipsing a golden sun——赤铁矿（材质）之月遮蔽金色太阳；现译“红月吞日”丢失 hematite 材质与 golden。整条修复。
与 surface 同向并补充：world-artifacts-far-east.lua:57 unided_name 为 a gray and gold pendant，赤铁矿月亮为灰色；“红月”与灰金配色矛盾且丢失 golden。整条修复为“赤铁矿之月遮蔽金色太阳”一类。

## f83a8191e966db8ebd1c7b88f3c053c38d1c05394b20452aef239ec110f28195

section: mod-tome/data/talents/misc/npcs.lua
source_tag: tformat

source: Corrupted vapour rises at the target location (radius 4) doing %0.2f blight damage every turn for %d turns.
		The damage increases with Spellpower.

target: 蒸腾目标区域（4码范围）造成每回合 %0.2f 枯萎伤害持续 %d 回合。
		伤害受法术强度加成。

确认依据：talents/misc/npcs.lua 腐化蒸汽 info：Corrupted vapour rises at the target location——现译“蒸腾目标区域”漏主语“腐化蒸汽”且把 rises at 误成及物“蒸腾”。整条修复，%0.2f/%d 与 \n\t\t 保持。
与 surface 同向：npcs.lua:1386 Corrupted vapour rises at the target location；现译丢主语、把“蒸腾”作及物。整条修复。

## f894de79df6d2ecec361043978ae052e31f288ef0034c595ee979ae68db2af8d

section: mod-tome/data/talents/gifts/ooze.lua
source_tag: tformat

source: Your body is more like that of an ooze.
		When you take damage, you may split and create a Bloated Ooze nearby within your line of sight.
		This ooze has as much health as twice the damage you took (up to a maximum of %d, based on your Mindpower and maximum life).
		The chance to split equals the percent of your health lost times %0.2f.
		You may have up to %d Bloated Oozes active at any time (limited by talent level and the summoning limit), and all damage you take will be split equally between you and them so long as this talent is active.
		Bloated Oozes last for %d turns, are very resilient (%d%% all damage resistance to damage not coming through your shared link), and regenerate life quickly.
		%sThe chance to split increases with your Cunning.

target: 你的身体构造变的像软泥怪一样。
		当你受到攻击时，你有几率分裂出一个浮肿软泥怪，其生命值为你所承受的伤害值的两倍（最大 %d，基于你的精神强度和最大生命值）。
		分裂几率为你损失生命百分比的 %0.2f 倍。
		你同时最多只能拥有 %d 只浮肿软泥怪，你所承受的所有伤害会在你和浮肿软泥怪间均摊。
		每只浮肿软泥怪存在 %d 回合，对非均摊的伤害的抗性很高（%d%% 对全部伤害的抗性），同时生命回复快。
		%s几率受灵巧加成。

确认依据：talents/gifts/ooze.lua Mitosis info：现译漏 within your line of sight（在视线内生成）、(limited by talent level and the summoning limit)、so long as this talent is active（仅在技能生效期间均摊），并把 take damage 缩窄为“受到攻击”。整条逐句核对后修复，占位符顺序与 \n\t\t 保持。
与 surface 同向并补充：ooze.lua:36 getMax 受 checkMaxSummon 召唤上限与技能等级双重限制；ooze.lua:112–119 伤害均摊只在技能生效期间成立；另漏 within your line of sight。整条修复。
