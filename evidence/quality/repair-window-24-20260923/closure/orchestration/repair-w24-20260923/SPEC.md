# 修复窗口24：270批6条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线22fdab0552c3da559bd2b780fd11b5cc06a712e1。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的6个target及evidence/quality/repair-window-24-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致（多段条目逐行比对空行位置，不只看总数）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证，并查同技能/同效果相邻条目已用译法），不自行新造。

6条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处；下列示例措辞仅为方向，落笔时仍须逐词对照原文。LuaJIT全记录比较恰6个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核271。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 飞镖发射器抵抗日志（talents/cunning/artifice.lua:643，logSeen）：%s resists the sedation!——效果 EFF_SEDATED 本库名“被镇静”，“睡眠”改为“镇静”一类；%s 保持。
- 敏锐直觉说明（talents/spells/divination.lua:88–92，tformat）：原文 3 行（2 个 \n，第 2、3 行以 \t\t 开头）。现译拆成 5 行，须恢复为 3 行：首句 getting information from moments in the future 按原文译（不加“直觉”）；第二行 Improves your capacity to see invisible foes by +%d, to see through stealth by +%d, and to perform a critical spell cast by +%d%%. 合为一行；第三行 The effects will improve with your Spellpower.。
- 狂热说明（talents/cursed/slaughter.lua:153–157，tformat）：4 fast attacks … damage each 的 each 指每次攻击（不是每个目标），补“快速”；Stalked prey are always targeted if nearby 译“总是”（附近有被追踪的猎物时四次都攻击它）；原文盾牌句前为 \n\n\t\t（空一行），须恢复该空行；其余两行逐句对照。
- 奥术至上法杖描述（general/objects/world-artifacts-maj-eyal.lua:1027–1028）：原文两句之间 1 个 \n，须恢复；yet alone it seems incomplete 意为“单独一件时似乎并不完整”（该法杖与奥术理解之帽成套），不要写“整体来看”。
- 吸食抗性说明（talents/cursed/dark-sustenance.lua:193–194，tformat）：原文 1 个 \n\t\t（在 Improves with your Mindpower 前），现译多一处换行，把“对‘所有’抗性无效”并回第一行。
- 意志属性说明（load.lua:186）：原文只列 mana、stamina、PSI capacity 与 chance to resist mental attacks，删去现译多出的“精神力”；抗精神攻击几率可沿用同族力量说明“物理豁免”的写法用“精神豁免”。

## f99ebf3aa31971c0fe288ed01ecb2f56e42155e9832ca192b83b48e197376201

section: mod-tome/data/talents/cunning/artifice.lua
source_tag: logSeen

source: %s resists the sedation!

target: %s抵抗了睡眠！

确认依据：talents/cunning/artifice.lua:639–643（624a673）：Dart Launcher（飞镖发射器）睡眠飞镖命中后施加 EFF_SEDATED，否则记录 "%s resists the sedation!"；本库该效果名 Sedated=“被镇静”（mod-tome.lua:37588）。现译“抵抗了睡眠”与效果名不一致（术语一级），改为“抵抗了镇静”一类，%s 保持。

## f9b4a1d58a20ced35e1f12e04dc703344d5b311f94d1374b580371ae719c5dc6

section: mod-tome/data/talents/spells/divination.lua
source_tag: tformat

source: You focus your senses, getting information from moments in the future.
		Improves your capacity to see invisible foes by +%d, to see through stealth by +%d, and to perform a critical spell cast by +%d%%.
		The effects will improve with your Spellpower.

target: 你集中精神，通过直觉获取未来的信息。
		增加侦测隐形等级 +%d
		增加侦测潜行等级 +%d
		增加法术暴击几率 +%d%%
		此效果受法术强度加成。

确认依据：talents/spells/divination.lua:88–92（624a673）Keen Senses（敏锐直觉）说明：原文 2 个 LF（3 行），现译 4 个 LF，把第二行拆成三行（一级换行不变量，与既往 blighted-ruins/Thought-Forms 裁决一致）；且“通过直觉获取未来的信息”增添原文没有的“直觉”，原文为 getting information from moments in the future。整条修复：恢复 3 行、\t\t 缩进，首句按原文译出“从未来的片刻中获取信息”一类，侦测隐形/潜行/法术暴击三项并回一行。

## fa2a8ff2837f8b980c322619eca7a3917f0dafa7754a02dc8d84ebeb5e94cb04

section: mod-tome/data/talents/cursed/slaughter.lua
source_tag: tformat

source: Assault nearby foes with 4 fast attacks for %d%% (at 0 Hate) to %d%% (at 100+ Hate) damage each. Stalked prey are always targeted if nearby.
		At level 3 the intensity of your assault overwhelms anyone who is struck, reducing their Defense by %d for 4 turns.
		The damage multiplier and Defense reduction increase with your Strength.

		This talent will also attack with your shield, if you have one equipped.

target: 对附近目标进行 4 次攻击每个目标造成 %d%% （0仇恨值）至 %d%% （100+仇恨值）。附近被追踪的目标会被优先攻击。
		等级 3 时你的猛烈攻击会同时降低目标 %d 的闪避，持续 4 回合。
		伤害加成和闪避减值受力量值加成。
		如果你装备了盾牌，这一技能也会用你的盾牌攻击。

确认依据：talents/cursed/slaughter.lua:125–156（624a673）Frenzy（狂热）：for i=1,4 每次攻击各自选目标（有被追踪猎物则总是它，否则 rng.table 随机），damageMultiplier 作用于每次攻击；原文 4 fast attacks … damage each。现译“进行 4 次攻击每个目标造成”把 each 误作“每个目标”并漏 fast；原文盾牌句前为 \n\n\t\t（空行），现译只剩 \n\t\t（一级换行不变量）。整条修复，Stalked prey are always targeted 译“总是”。
与 surface 同向：slaughter.lua:125–146 Frenzy（狂热）for i=1,4 每次攻击各自选目标，附近有被追踪猎物时四次都打它；damage each 指每次攻击，现译“每个目标造成”误挂，“优先攻击”弱化 always。并入同条整句修复（含 fast 与盾牌句前空行）。

## fa465502e545e8daab7e688c0cadc77fc113384d23abfce5bda0d700e99300d8

section: mod-tome/data/general/objects/world-artifacts-maj-eyal.lua
source_tag: _t

source: A long slender staff, made of ancient dragon-bone, with runes emblazoned all over its surface in bright silver.
It hums faintly, as if great power is locked within, yet alone it seems incomplete.

target: 一根又细又长的法杖，由远古龙骨制成，它通体铭刻着银色的符文。它会发出微弱的嗡嗡声，似乎有一股强大的力量被锁在了里面，整体来看，它似乎是不完整的。

确认依据：general/objects/world-artifacts-maj-eyal.lua:1018–1028（624a673）Staff of Arcane Supremacy（奥术至上法杖）描述：原文两句间 1 个 \n，现译 0 个 LF 并成一段（一级换行不变量，与既往裁决一致）。宿主另核（线索来自已作废的 contextual 首次尝试，结论由宿主独立核验）：该法杖 set_list 与 SET_HAT_CHANNELERS 成套（同文件 1052/1088 行），yet alone it seems incomplete 意为“单独一件似乎并不完整”，现译“整体来看，它似乎是不完整的”意思相反（一级 fidelity）。整条修复：恢复换行，末句译为“单独一件时似乎并不完整”一类，其余逐句对照。

## fa46681a109915eadaeb8a5f74146c0e687ad7709a4f3c15ca0be7472136ada1

section: mod-tome/data/talents/cursed/dark-sustenance.lua
source_tag: tformat

source: Enhances your feeding by reducing your targeted foe's resistances, multiplying them by %0.2f and increasing your resistances by the amount drained. Resistance to "all" is not affected.
		Improves with your Mindpower.

target: 提高你的吸食能力，将目标的伤害抗性降低到原来的 %0.2f 倍，并将你自身相应的伤害抗性提高相同数值。
		对“所有”抗性无效。
		效果受精神强度加成。

确认依据：dark-sustenance.lua Feed Strengths（吸食抗性）说明：原文 1 个 LF（\n\t\t 在 Improves with your Mindpower 前），现译 2 个，在“对‘所有’抗性无效”前额外换行（一级换行不变量）。整条修复：并回首段，只保留原位置一处 \n\t\t。

## fa9d429c2df842ba7888976927b58a0bd6d198f251995c016354229009062727

section: mod-tome/load.lua
source_tag: _t

source: Willpower defines your character's ability to concentrate. It increases your mana, stamina and PSI capacity, and your chance to resist mental attacks.

target: 意志属性是你的专注能力，提升意志可以提升你的法力值、体力值、灵能值、精神力和精神豁免。

确认依据：升级 surface advisory：本条源串为 load.lua:186 属性定义，只列 mana/stamina/PSI capacity 与抗精神攻击几率，不含 Mindpower；TooltipsData.lua:243 是另一条字符串。现译多出“精神力”既是增译，又与本库 Mindpower=“精神强度”不一致（术语一级）。整条修复：去掉“精神力”，按原文四项译出，“抵抗精神攻击的几率”可沿用“精神豁免”一类本库说法。
