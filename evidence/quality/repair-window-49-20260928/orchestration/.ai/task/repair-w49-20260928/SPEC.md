# 合并修复窗口 49：第359批确认项，2 条

Paseo MCP / schema5 translation_contextual_v2 implement。基线 58f278c8ddf1f7b24d35aaa8ef4cb94ee0c337a7。审核队列已耗尽，积压 2 条低于 20 的开窗阈值；用户 2026-09-28 明确选择开窗口 49 修这 2 条（不含范围外 8b977dd836）。用户已授权连续审核与合并修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。

唯一 EXECUTOR 仅可修改：WORKSET.json 列出的 2 个 target（mod-tome.lua、tome-ashes-urhrok.lua 各一条），以及 `evidence/quality/repair-window-49-20260928/` 下的修复证据。不得修改 source、source_tag、section、args_order、运行键、其他译文、术语库、规则工具或旧证据；不得 stage、commit、push、创建 agent 或修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

**本窗口是定向修改，不是全文重译。** 每条只改 SOURCE-CLAIMS 点名的词语或句子（以及为此必须调整的衔接字），不得借机改写其余部分；即使发现别处可疑，也只在报告中列出、不改（宿主另行登记）。修改点名句时须对照整句原文，不留同句其他旧错。专名沿用本库既有译法（莱娜尼尔、伊菲尼亚斯、特塞尔、卡库罗尔、夏·图尔、绿翡翠之子、小劣魔等）。

保留 printf 占位符、`%%`、`#TAG#`、`#{italic}#`、`#{normal}#`、`#{bold}#`、`<?=...?>` 模板、`@name@` 等 markup 的数量、顺序及适用位置；保留 source_tag。LF/TAB 结构与现译逐行一致（本窗口不改换行）。用 LuaJIT 加载两个译文文件，证明恰 2 个 target 变动且其他记录不变；执行 strict lint 及 git diff --check。无需完整门禁，宿主在独立复审后统一运行 17 项。主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证；DLC 源码只在 SOURCE-ANCHORS 给出的 checkout 下按条目路径取证，不扫 `/`、`/workspace` 或无关目录；DLC 源码仓库与 commit 未固定。

审查：cycle-0 `REVIEW/full` 用 Codex GPT-6 Sol；确认问题合并给一次 EXECUTOR fix；收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。v2 FINAL 如有任何 ISSUE，先修复并完成 RE_REVIEW，再重新 FINAL（同 cycle 用下一个 attempt）。max_cycles=5。reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。与本窗口裁决无关的既有问题由宿主记 advisory 并 carry_forward 到后续审核，不扩大本窗口范围。

## 条目与已确认修复依据

- 7c7be93333f2afcd4e3c207742450ce03b715bcecbf9cdc7b71e410d53c754c8 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/lore/demon.lua | 第359批确认（公开 Ashes tome-ashes-urhrok/data/lore/demon.lua:295 小劣魔雕像 lore）：“These children of emerald were among the first to alter themselves for our quest for vengeance”是“最早为复仇改造自身的族群之一”，改掉“第一批同意改变自身以帮助复仇”（删增译“同意”，among the first 译出“之一”）；只改该句。
- d38555ee6a6bfa577bc075bd950f590a5a0add177a6198908fe3925fe0baa909 | mod-tome.lua | mod-tome/data/lore/elvala.lua | 第359批确认（固定 commit 624a673 game/modules/tome/data/lore/elvala.lua，艾伦尼恩回忆录第一章“命运之会”）七处：(1)第36行“as the party approached the citadel”＝一行人走近城堡，改掉“当人群到达我们的大本营时”；(2)第64行“legends and myths still abound to scare people away from anything to do with the Sher’Tul. But we are confident that we know what we are doing here”——被传说吓退的是“人们”，伊菲尼亚斯自己“有信心”，改掉“阻止我们探索夏·图尔的原因之一”与“我们现在清醒地认识到”；(3)第46行删去增译“与隐藏的傲慢”（原文只有 her extreme rudeness and her wild presumptions），“在喘气的同时勉强说道”补出 incredulous（笑得喘不过气、难以置信地反问），“贴身战士”与第44行同一 mere fighter 的译法（前文“只会近身搏斗的战士”）对齐；(4)第52行删去增译“阐述自己的要求”（原文只说以他素闻的生硬简短方式开口）；(5)第72行“Very well”是审慎应允，“非常好”改“好吧”一类；(6)第50行“with a mock bow of my head”＝故作姿态地欠身，改掉“点头答道”；(7)第48行“burn foes from afar”＝从远处焚烧敌人，改掉“烧伤敌人”。
