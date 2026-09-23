# 修复窗口14：260批3条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线e255e9ff3d10532997ddef35bcdc8cd3d9cda0a1。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的3个target及evidence/quality/repair-window-14-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/LF/TAB全部保持基线。

3条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 若失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰3个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核261。

范围约束：
- 珠宝师对话（jewelry-store.lua:168–172，多行对话，保留颜色标记与换行）：potent amulets 为“强力的项链”（amulet 维持本库物品类别译名“项链”，不改“护身符”），不加比较义“更”；冬潮之月传说写明其一部分因离太阳过近而融化、从天空坠落，删去原文没有的“融入了大地，使那个地方充满能量”；坠落处形成湖泊、湖水浸润月光万古、足以锻造强大神器、用卷轴召唤、回去研究手册等其余句子逐句对照原文，不增不减。
- Guided Shot（psi-archery.lua:50）：写出以精确的念力微调导引箭矢射向目标（telekinetic nudges），“精确地”用副词“地”；数值句“造成普通伤害，但命中和暴击率提高 %d”保持。
- 巨狼描述（canine.lua:62）：snaps at you 为“朝你猛咬/扑咬”，prowls 为“潜行逡巡/游荡”，不得写“咆哮”；Larger than a normal wolf 保留。

## ef7d5a43a10dc8eae43e1f4e8f15d7ca626123291c6d722daf5395cf2080324e

section: mod-tome/data/chats/jewelry-store.lua
source_tag: _t

source: #LIGHT_GREEN#*He quickly looks at the tome and looks amazed.*#WHITE# This is an amazing find! Truly amazing!
With this knowledge I could create potent amulets. However, it requires a special place of power to craft such items.
There are rumours about a site of power in the southern mountains. Old legends tell about a place where a part of the Wintertide Moon melted when it got too close to the Sun and fell from the sky.
A lake formed in the crater of the crash. The water of this lake, soaked in intense Moonlight for eons, should be sufficient to forge powerful artifacts!
Go to the lake and then summon me with this scroll. I will retire to study the tome, awaiting your summon.

target: #LIGHT_GREEN#*他快速浏览了那本手册，露出了惊讶的表情。*#WHITE# 这真是神奇的发现！太神奇了！
有了这些知识我就能制造更强大的项链了。不过这需要一个特殊的地方来完成制作过程。
传言在南部山脉之中有个地方充满能量。有个古老的传说，当冬月与太阳距离太接近的时候它的一部分从空中掉落了下来并融入了大地，使那个地方充满能量。
在坠落的地方形成了一个湖泊，湖水吸收了万年月光的力量，应该足以锻造出强大的神器。
去找到那个湖泊，然后使用这个卷轴将我召唤过去，从现在开始我要潜心研修你的这本手册，等待你召唤我的那一刻。

确认依据：chats/jewelry-store.lua:168–169 珠宝师对话：原文为冬潮之月的一部分因离太阳过近而 melted（融化）并从天空坠落，译文漏“融化”并凭空加“融入了大地，使那个地方充满能量”的因果；potent amulets 为“强力的项链”，译文“更强大的”多出比较义。忠实性缺陷，整段对照原文修复（amulet 仍用项链）。

## ef9f97a2e35279283eb9a65b619c956c309c9fdce53a4f3b656da98956a54c4d

section: mod-tome/data/talents/psionic/psi-archery.lua
source_tag: tformat

source: Fire and guide an arrow to its target with precise telekinetic nudges. Does normal damage, but accuracy and crit chance are increased by %d.

target: 射出一支导引箭精确的飞向敌人。造成普通伤害，但是命中和暴击率提高 %d。

确认依据：talents/psionic/psi-archery.lua:50 Guided Shot（psionic/psi-archery）：with precise telekinetic nudges 是念力微调导引箭矢的心灵异能方式，译文“射出一支导引箭精确的飞向敌人”删去念力、改写成箭自带导引，且“精确的”应作“精确地”。与 contextual 独立复核同向，宿主由 advisory 改判 confirmed（完整性）；数值部分（atk 与 crit_chance 同加 shot_boost）无误。整句修复。
与 surface 同向：psi-archery.lua:50 漏译 telekinetic nudges（念力微调导引），“精确的”应作“精确地”。

## efe21d07a2bbc4c69fbb66e67a4ca2343455241783abe030016d3abfc2348cfd

section: mod-tome/data/general/npcs/canine.lua
source_tag: _t

source: Larger than a normal wolf, it prowls and snaps at you.

target: 它比普通的狼更大，在你面前徘徊咆哮。

确认依据：general/npcs/canine.lua:62 巨狼描述：snaps at you 是朝你猛咬、扑咬，译文“咆哮”把动作误译为吼叫；prowls 为潜行逡巡。与 contextual 独立复核同向，宿主由 advisory 改判 confirmed（动作误译）。整句修复。
与 surface 同向：canine.lua:62 snaps at you 为猛咬/扑咬，“咆哮”误译动作。
