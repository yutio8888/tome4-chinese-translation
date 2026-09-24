# 修复窗口23：269批3条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线bcc6d11ff20f7efa6ecbd18e2ffd0777e524a4a0。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的3个target及evidence/quality/repair-window-23-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致（多段条目逐行比对空行位置，不只看总数）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证，并查同技能/同效果相邻条目已用译法），不自行新造。

3条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处；下列示例措辞仅为方向，落笔时仍须逐词对照原文。LuaJIT全记录比较恰3个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核270。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 夺心魔任务说明（quests/start-yeek.lua:23，原文末尾带一个换行）：You have been tasked to remove at least one of the threats to the yeeks.——补出 at least（至少清除其中一个），任务后文列出两处威胁（Murgol 水下巢穴、ritch 隧道）；yeek 保持“夺心魔”（用户 2026-09-16 裁定）；保持原文末尾换行。
- 埃亚尔之怒技能类别说明（talents/gifts/gifts.lua:44）：Unleash nature's fury against foes around you.——补“周围的敌人”；类别名“埃亚尔之怒”不改。
- 奥术漩涡效果说明（timed_effects/magical.lua:2672，tformat）：a manathrust fires from it to a random foe in sight doing %0.2f arcane damage to all——奥术射线（manathrust）射向视野内随机一名敌人，对射线路径上的所有目标造成 %0.2f 奥术伤害；其余句子（无敌人时本体多受 50%% 伤害、目标死亡时剩余伤害化为半径 2 的奥术爆炸）逐句对照；%0.2f 与 50%% 保持。

## f8a393e313adfeab02c028ebb2e35f44f1ddb1557a8fea34db2b0f1b23da41a0

section: mod-tome/data/quests/start-yeek.lua
source_tag: _t

source: You have been tasked to remove at least one of the threats to the yeeks.


target: 你被派去清除对夺心魔的两大威胁之一。


确认依据：quests/start-yeek.lua:23：You have been tasked to remove at least one of the threats to the yeeks.——任务列出两处威胁（Murgol 水下巢穴、ritch 隧道），完成任一即可；现译“清除……两大威胁之一”删去 at least，读作只需且只清除其中一个（删限定词类）。整条修复为“至少清除一个”一类；yeek 保持“夺心魔”（用户 2026-09-16 裁定）。

## f8f18f9470ee9132598ded6a7b56fe64bb66357e323b82d5c3937ac6db3a5592

section: mod-tome/data/talents/gifts/gifts.lua
source_tag: _t

source: Unleash nature's fury against foes around you.

target: 向敌人释放自然的愤怒。

确认依据：talents/gifts/gifts.lua:44 技能类别 eyal's fury 说明：Unleash nature's fury against foes around you.——现译“向敌人释放自然的愤怒”漏 around you（周围的敌人）。整条修复。

## f8f6be5a29af31327cf6a9ca51b895a3455c23aaff4991a472908899d6be09db

section: mod-tome/data/timed_effects/magical.lua
source_tag: tformat

source: An arcane vortex follows the target. Each turn a manathrust fires from it to a random foe in sight doing %0.2f arcane damage to all. If no foes are found the main target takes 50%% more arcane damage this turn. If the target dies the remaining damage is dealt as a radius 2 ball of arcane.

target: 一个奥术漩涡跟随着目标。每回合一发奥术射线从它身上释放出来，随机对附近视野内的目标造成 %0.2f 奥术伤害。如果视野内没有任何其他目标，则该回合会对初始目标附加额外的 50%%奥术伤害。如果目标死亡，残余伤害引发半径为 2 的奥术爆炸。

确认依据：timed_effects/magical.lua:2672–2692 ARCANE_VORTEX：每回合从漩涡向视野内随机敌人发射 beam（eff.src:project type="beam"），路径上所有目标都受 %0.2f 奥术伤害（to all）；现译“随机对附近视野内的目标造成伤害”漏掉射线贯穿、对路径上全部目标生效。整条修复。
与 surface 同向并补充：ARCANE_VORTEX on_timeout 有敌人时被附身目标自身先受 eff.dam，再向随机敌人发射 beam，路径上所有单位受伤；现译只写“随机对……目标造成”，漏射线贯穿与本体同时受伤。整条修复。
