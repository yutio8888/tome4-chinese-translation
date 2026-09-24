# 修复窗口21：267批5条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线8e06944f8250f4edaba7e674ad32ac5c1167f6eb。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的5个target及evidence/quality/repair-window-21-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致（多段条目逐行比对空行位置，不只看总数）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证），不自行新造。

5条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰5个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核268。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 技能名 Sun Flare（talents/celestial/sunlight.lua:69，光系球形爆发）：flare 为“耀斑”，改为“太阳耀斑”（用户 2026-09-23 明确批准）；“日珥”是另一种太阳现象。全库仅此一行，不涉及其他条目。
- 盾牌敏捷格挡日志（talents/techniques/agility.lua:71，tformat "%s(%d deflected)#LAST#"）：%d 为被盾牌偏转抵消的伤害量，写成“%s(%d 被偏转)#LAST#”一类，不要写成技能名；%s、%d、#LAST# 保持。
- 枯萎遗迹 lore（lore/blighted-ruins.lua:27）：原文单段、0 个换行；删去现译“这令我很不悦。”后插入的 \n\t，全文为一段；其余逐句对照。
- Solipsist 职业说明引语（birth/classes/psionic.lua:139）：the world is the collective dream of those that live in it 为“世界是其居民共同的梦”；Find and wake the sleeper and you'll unlock the potential of your dreams 为“找到并唤醒沉睡者，你就能发掘梦境的潜能”一类；原文两句之间的两个空格如何处理沿用本库同族说明写法。
- 静电网（talents/psionic/charged-mastery.lua:119–122，tformat）：which will add %0.1f additional Lightning damage to your next attack for each turn you spend within its area——写出“你在网中每停留一回合，下一次攻击就额外增加 %0.1f 闪电伤害”一类（按回合累加）；%d/%d/%0.1f/%d%%/%0.1f 顺序与 \n\t\t 保持。

## f6a545d079ceafc869ce383b0a85a769f06125cc6ee7d85e92bda7016ad346aa

section: mod-tome/data/talents/celestial/sunlight.lua
source_tag: talent name

source: Sun Flare

target: 日珥闪耀

确认依据：talents/celestial/sunlight.lua:69 技能名 Sun Flare（光系球形爆发，致盲并造成光伤）；flare 为“耀斑”，现译“日珥闪耀”的日珥（prominence）是另一种太阳现象。全库“日珥”“耀斑”各仅此一处，无引用同步与冲突，改为“太阳耀斑”一类属单条纠错而非全局重命名。

## f6e111a3a18ec5cc0950dad5670f848fb3f7e10be1e165b158d14a7635e0c096

section: mod-tome/data/talents/techniques/agility.lua
source_tag: tformat

source: %s(%d deflected)#LAST#

target: %s(%d 敏捷防御)#LAST#

确认依据：talents/techniques/agility.lua:71 盾牌敏捷格挡：delayedLogDamage 显示被抵消的伤害量 ("%s(%d deflected)#LAST#"，lastdam - dam)；现译“(%d 敏捷防御)”把偏转量说成防御名称。改为“(%d 被偏转)”一类，%s/%d 与 #LAST# 保持。
与 surface 同向：agility.lua:69–71 %d 为 lastdam-dam 即被盾牌偏转抵消的伤害量；现译“敏捷防御”读作技能名。整条修复为“(%d 被偏转)”一类。

## f6eae8d3af4e8b950b4458502bc97789ad577070d04ea09f8d7f439c58289462

section: mod-tome/data/lore/blighted-ruins.lua
source_tag: _t

source: Work on my glorious project has been delayed. This displeases me. The fools from the nearby village are starting to suspect my presence, and have begun guarding their graveyards and cemeteries closely. Whatever meagre remains I can steal away are often too rotted or insubstantial to use for my project, so I have no choice but to use them as sub-par minions instead. Perhaps they will sow enough conflict and discord so that new, fresher remains will become available...

target: 我伟大的计划被耽搁了。这令我很不悦。
	附近村庄里的傻瓜开始怀疑我的存在，严密守卫起他们的坟地和墓园。我能偷走的少量遗骸往往腐烂得太厉害或残缺得无法用于计划，因此只得把它们制成次等仆从。或许这些仆从能制造足够多的冲突和混乱，让我得到更新鲜的遗骸……

确认依据：lore/blighted-ruins.lua:27 原文为单段连续文本（0 个 LF），现译在首段后插入 \n\t（一级换行不变量）。整条修复：删去该换行与制表符，其余逐句对照。
与 surface 同向：blighted-ruins.lua:27 单段无换行，现译插入 \n\t（一级换行不变量）。整条修复。

## f6f9c01056769d4ee1c33b21364ce5189614c942cdcba107930cf4ce5c138ce4

section: mod-tome/data/birth/classes/psionic.lua
source_tag: _t

source: Some believe that the world is the collective dream of those that live in it.  Find and wake the sleeper and you'll unlock the potential of your dreams.

target: 有些人认为世界由许多个梦境组成，而我们生活在这些梦境里。寻找并唤醒沉睡者，你可以打开通往梦境之门。

确认依据：birth/classes/psionic.lua:139 Solipsist 职业说明引语：the world is the collective dream of those that live in it（世界是其居民共同的梦）；unlock the potential of your dreams（发掘你梦境的潜能）。现译“由许多个梦境组成”“打开通往梦境之门”偏离原意。整条修复。
与 surface 同向，并补充：下一行 psionic.lua:141 讲“the collective vision of those that experience it”，现译“许多个梦境”与之矛盾；unlock the potential of your dreams 被改为“打开通往梦境之门”。整条修复。

## f72ac3de1cbba4a5ace7e3e532c6f8df16b4eba09fab16a1d0f942059c8b31c9

section: mod-tome/data/talents/psionic/charged-mastery.lua
source_tag: tformat

source: Cast a net of static electricity in a radius of %d for %d turns.
		Enemies standing in the net will take %0.1f Lightning damage and be slowed by %d%%.
		When you move through the net, a static charge will accumulate on your weapon which will add %0.1f additional Lightning damage to your next attack for each turn you spend within its area.
		These effects scale with your Mindpower.

target: 在半径 %d 范围中散布一个持续 %d 回合的静电捕网。
		站在网中的敌人受到 %0.1f 的闪电伤害并被减速 %d%%。
		当你在网中穿梭，你的武器上会逐渐累加静电充能，让你的下一次攻击造成额外 %0.1f 的闪电伤害。
		技能效果受精神强度加成。

确认依据：talents/psionic/charged-mastery.lua:119–122 静电网：add %0.1f additional Lightning damage to your next attack for each turn you spend within its area——每在网中停留一回合累加一次；现译漏“每停留一回合”，读作固定一次加成（删限定词类缺陷）。整条修复，%d/%0.1f/%d%% 顺序与 \n\t\t 保持。
与 surface 同向：damage_types.lua:3935–3946 每回合在网中给予 STATIC_CHARGE，mental.lua:2812–2813 on_merge 叠加 power，故加成按停留回合累加；现译漏 for each turn you spend within its area。整条修复。
