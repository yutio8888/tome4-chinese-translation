# 修复窗口12：258批3条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线20e1610e573837ff6b8899b54d9663b956dddfba。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的3个target及evidence/quality/repair-window-12-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/LF/TAB全部保持基线。

3条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 若失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰3个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核259。

范围约束：格斗家描述整句忠实——列出 pit-fighter（地下拳场斗士一类）、boxer（拳击手）、amateur practitioner（业余习武者，不得写“门外汉”），the Brawler's skills 写明职业名“格斗家的技能”，still handy today 保留。零点城镇 Zemekkys 描述：timeless elf 译为“不显年岁的精灵”一类，删去“中年”，其余句子逐句对照原文（不增“岁月不曾留下痕迹”之类原文没有的内容若与 timeless 重复可合并）。岱卡拉任务日志（fire dragon 条）补 huge（巨型/巨大的），dwelled there 为“盘踞在那里的”，颜色标记不动。同族 ice dragon 条（mod-tome.lua 20799）不在本窗口范围，不改。

## ed8673e41a7d04e69012aca27620bd886c1712ff3aec6ece4efab8e8f801ead1

section: mod-tome/data/birth/classes/warrior.lua
source_tag: _t

source: Whether a pit-fighter, a boxer, or just an amateur practitioner, the Brawler's skills are still handy today.

target: 无论是一个职业拳手还是个业余的门外汉，格斗技能直到现在仍然十分有用。

确认依据：birth/classes/warrior.lua:343 Brawler 描述：列举 pit-fighter、boxer、amateur practitioner 三类，译文漏 pit-fighter（地下格斗士/角斗拳手），且 the Brawler's skills 被泛化为“格斗技能”丢失职业名“格斗家”（classes.tsv:23 Brawler=格斗家）。整句修复。
与 surface 同向的独立语境复核：birth/classes/warrior.lua:343 漏 pit-fighter；“门外汉”（外行）与 practitioner（实际习练者）相反；the Brawler's skills 被泛化为“格斗技能”，丢职业名“格斗家”。整句修复。

## ed86ff05a4f099244e7dfde68a8a2d2c325860305f6b0ab71656467cf4330fbb

section: mod-tome/data/zones/town-point-zero/npcs.lua
source_tag: _t

source: A timeless elf stands before you. Even though his age is impossible to determine, you feel he has seen many things.

target: 一位中年精灵站在你面前，岁月不曾在其脸上留下痕迹。尽管你不知道他活了多久，但是你仍能感到他已经遍览世间万物。

确认依据：zones/town-point-zero/npcs.lua:134：A timeless elf…his age is impossible to determine；译文“中年精灵”凭空断定年龄，与后句“不知道他活了多久”自相矛盾。修为“一位看不出年岁的精灵”一类。
与 surface 同向：town-point-zero/npcs.lua:134 A timeless elf…age is impossible to determine，“中年精灵”凭空断定年龄且与后句矛盾。修为“不显年岁的精灵”一类。

## edc794ff9790e88861a4368d236f7fb2c49abe4a7ae8e706d3ed071218d6af4a

section: mod-tome/data/quests/starter-zones.lua
source_tag: _t

source: #LIGHT_GREEN#* You have explored the Daikara and vanquished the huge fire dragon that dwelled there.#WHITE#

target: #LIGHT_GREEN#* 你已经探索了岱卡拉并杀死了这里的火龙。#WHITE#

确认依据：quests/starter-zones.lua:56 岱卡拉任务日志：the huge fire dragon that dwelled there，译文“这里的火龙”漏 huge（巨大的）且 there→“这里”视角偏差。修为“盘踞在那里的巨型火龙”一类。
