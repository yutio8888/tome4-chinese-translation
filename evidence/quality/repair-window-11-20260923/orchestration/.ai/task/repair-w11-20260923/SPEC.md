# 修复窗口11：257批4条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线11fc456c447adab739028e74b8921607657d3b0f。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的4个target及evidence/quality/repair-window-11-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/TAB全部保持基线；LF 须与 source 对齐（见 Trollmire 条）。

4条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 若失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰4个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核258。

范围约束：Trollmire 日记残页恢复原文的两处空行（第一段引语后、中间“……”后各一空行，使 LF 数与 source 一致），get wind of me 译为“察觉到我”一类，不增加气味/追踪；其余句子逐句对照原文，不改开头叙述句。Torment 第一句去掉“超过”，阈值为“至少 %d%%”（基数为最大生命值，单次打击），占位符顺序不变，第二、三句保持。鼠巫妖头骨未鉴定名译为“落满灰尘的鼠头骨”一类（与鉴定名“鼠巫妖头骨”一致用“头骨”）。角色面板标题改为“#LIGHT_BLUE#状态效果抗性：”，颜色标记与全角冒号保持。

## ebc837780344f493663f77584fce3427e1246afecec3705e4e6f824d1d15aae6

section: mod-tome/data/lore/trollmire.lua
source_tag: _t

source: You find a tattered page scrap. Perhaps this is part of a diary entry.
"...ack again, but he's just a stupid old troll. It'll be easy to not let him get wind of me.

...

...initely found his treasure stash further on, but had to turn back. If you get this, HELP!"

target: 你找到了一片破烂的纸页残片。也许这是某篇日记的一部分。
“……又回来了，不过他只是那只又老又蠢的巨魔。要掩住气味、不让他循迹找到我，轻而易举。
……
……肯定在更前面找到了他的藏宝处，可我不得不折回来。如果你看到这些，救命！”

确认依据：lore/trollmire.lua:40–45（624a6732）trollmire-note-2：get wind of me 是习语“察觉到我”，译文“掩住气味、不让他循迹找到我”按字面误作嗅觉追踪；且原文 "...ack again…" 段后与 "..." 前后各有一个空行（41/42/43/44/45 行），译文删去两处空行，属换行不变量缺陷。整条有界修复（保留两处空行，译为“不让他察觉到我”一类）。
与 surface 同向的独立语境复核：lore/trollmire.lua:40–45 两处空行被删（换行不变量），get wind of me 为“察觉”习语却被字面译作掩盖气味。确认整条修复。

## ebcb3ef07162cd324a09d6a79dd7c76e4eb4ed2e7ef04b4c5121c6056309f6b3

section: mod-tome/data/talents/corruptions/torment.lua
source_tag: tformat

source: When you are dealt a blow that reduces your life by at least %d%%, you have a %d%% chance to reduce the remaining cooldown of all your talents by 1.
		Temporary life from Sanguine Infusion will not count against the damage threshold.
		The chance will increase with your Spellpower.

target: 当你遭受到超过至少 %d%% 总生命值的伤害时，你有 %d%% 概率降低所有技能 1 回合冷却时间。
		鲜血灌注带来的额外生命值，不会影响该技能的伤害阈值。
		概率受法术强度加成。

确认依据：corruptions/torment.lua:132–159：callbackOnHit 判定 cb.value >= max_life * l / 100（含等于，基数为扣除 Blood Grasp 临时生命后的最大生命值）；译文“超过至少 %d%%”自相矛盾且“超过”排除等于。修为“至少 %d%% 最大生命值”一类。
与 surface 同向：torment.lua:136–140 判定 cb.value >= max_life*l/100（含等于），“超过至少”自相矛盾。确认修为“至少”；第二句 Blood Grasp 临时生命不计入阈值的译法可保留。

## ec13c4e923325038bfd4900bf725f7d7fd1df53b9c73baafaba3787affc1b5d4

section: mod-tome/data/general/events/rat-lich.lua
source_tag: _t

source: dusty rat skull

target: 肮脏的鼠骷髅

确认依据：general/events/rat-lich.lua:44–51：RATLICH_SKULL（subtype="skull"）未鉴定名 dusty rat skull，鉴定名 Skull of the Rat Lich 现译“鼠巫妖头骨”；“鼠骷髅”把头骨误作整具骷髅且与鉴定名不一致，dusty 为“落满灰尘的”而非“肮脏的”。修为“落满灰尘的鼠头骨”一类。
与 surface 同向：rat-lich.lua:50 dusty 为“落满灰尘”，“肮脏”改变语义；同条 skull 与鉴定名“鼠巫妖头骨”应一致。确认修复。

## eccfcfca31053195a67592051cc6d3444160027936f780df84a8d90e641ce269

section: mod-tome/dialogs/CharacterSheet.lua
source_tag: _t

source: #LIGHT_BLUE#Effect resistances:

target: #LIGHT_BLUE#状态效果免疫：

确认依据：dialogs/CharacterSheet.lua:1277–1300：Effect resistances 标题下每项显示 100-canBe 概率或 attr×100 的 0–100% 抵抗百分比，并非绝对免疫；译文“状态效果免疫”把部分抗性说成免疫，属保真缺陷。修为“状态效果抗性”。
