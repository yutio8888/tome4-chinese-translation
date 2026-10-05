# 修复窗口 67：宿主补充与用户授权项（2 条）

Paseo MCP / schema5 translation_contextual_v2 implement。基线 36009f67a486f1b41e3c2620ad696a6bb0a91cab。

## 来源

- 9d3fc01bdf：窗口66 REVIEW r0a1 确认诸神前言“安格列文”时，宿主发现同文件奎科加章节另有一处“安格列文”（records of Anglowen），不在窗口66 workset，登记为窗口67宿主补充（不计积压）。
- fc55a88fd6：mod-tome.lua:422 护送奖励日志“%s 技能 %s (+%d 等级)”与已改的同族选项（mod-tome.lua:425、tome-orcs.lua:582）写法不一致；此前未获授权。
- 第404批审完窗口66 的 25 个 successor 后审核队列清空，窗口67积压 0。2026-10-05 用户选择“小窗口67并含 422 行”，授权开窗修这 2 条。

用户已授权修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。

## 写入权限

唯一 EXECUTOR 仅可修改以下内容：

- WORKSET.json 列出的 2 个 target（mod-tome.lua 1 条、tome-cults.lua 1 条）；
- `evidence/quality/repair-window-67-20261005/` 下的修复证据。

不得修改：source、source_tag、section、args_order、运行键、其他译文、术语库、规则工具或旧证据。

不得 stage、commit、push，不得创建 agent，不得修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

## 改写要求

按 NEW-TARGETS.json 中每条的 new_target 整条替换现有 target（宿主已按各条“修复：”与整句对照写定全文；old_target 为现值）：

- 两条均保持现有 LF／`\t` 结构不变；
- fc55a88fd6 的 `%s`、`%s`、`%d` 三个占位符顺序与个数不变（source_tag 为 tformat，不得出现裸 %）；
- 所有占位符、`#COLOR#`、`#{italic}#` 等标记与 `@name@` 令牌保持不变；source_tag 不变。

## 验证要求

- 用 LuaJIT 加载 mod-tome.lua 与 tome-cults.lua，证明恰 2 个 target 变动、其他记录不变；
- 执行 strict lint 及 git diff --check。

无需完整门禁，宿主在独立复审后统一运行 17 项。

## 取证范围

- 主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证；Cults 公开源码在 /workspace/tome4-dlcs/cults（仓库与 commit 未固定）。
- 不扫 `/`、`/workspace` 或无关目录。

## 审查安排

- cycle-0 `REVIEW/full` 用 Codex GPT-6.1 Sol（medium）。
- 收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。
- v2 FINAL 有任何 ISSUE 时，先修复并完成 RE_REVIEW，再重新 FINAL。max_cycles=5。
- reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。

## 宿主裁决依据

与已记录用户裁决相冲的指摘，宿主按裁决驳回（如 The Master＝领主、Archmage 职业名保留元素法师）。与本窗口修改无关的既有问题，宿主按源码核实后决定当窗修复或记 advisory 并 carry_forward。

## 条目与已确认修复依据

- 9d3fc01bdf37e358131c3837beb44ef55eccf2509a576826c6ce9a31947351a0 | tome-cults.lua | tome-cults/data/lore/kroshkkur.lua | 宿主补充（窗口66 REVIEW r0a1 确认 d2614f771f 的“安格列文”时发现，不在窗口66 workset）：Cults 公开源码 tome-cults/data/lore/kroshkkur.lua:107（来源仓库与 commit 未固定，文件 SHA 与第401批 workset 一致）奎科加章节 “According to the records of Anglowen, Quekorja was slain during the Godhunt...” 的 Anglowen 是上游对 Angolwen 的笔误；现译“根据安格列文的记载”与 terminology/places.tsv:20 Angolwen＝安格利文（preferred）不符。修复：“安格列文”→“安格利文”；整句其余（弑神之战、法师莱娜尼尔、无可匹敌的大法师）与全库一致，不改。
- fc55a88fd602ed5d2b8326d1f91d116116c44c1c5d2a9a94c4c364e15f21b04d | mod-tome.lua | mod-tome/class/EscortRewards.lua | 用户 2026-10-05 授权（窗口67）：主游戏固定 commit 624a673 的 game/modules/tome/class/EscortRewards.lua:537 以 ("%s talent %s (+%d level(s))"):tformat(knowTalent and _t"improved" or _t"learnt", t.name, level) 生成护送奖励日志，经 data/chats/escort-quest.lua:36 存为 reward_message，在 data/quests/escort-duty.lua:64 套入 "As a reward you %s."（现译“作为奖励，你%s。”）。现译“%s 技能 %s (+%d 等级)”显示为“作为奖励，你提升了 技能 X (+1 等级)。”，与已改的同族选项 "[%s talent %s (+%d level(s))]"（mod-tome.lua:425、tome-orcs.lua:582 均为“[%s技能 %s（+%d 级）]”）写法不一致。修复：→“%s技能 %s（+%d 级）”，显示为“作为奖励，你提升了技能 X（+1 级）。”；占位符顺序不变。
