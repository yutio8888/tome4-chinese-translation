# 修复窗口 58：第373、374批确认的 3 条

Paseo MCP / schema5 translation_contextual_v2 implement。基线 12376f4bfd991734907d9d2afa08bc7fba0abb0f。来源批次：`batch-eb93936e38c73186d222`（第373批，确认 2 条）与 `batch-2e8beab0b2f9b05c4c94`（第374批，确认 1 条），均为窗口57 successor 的审核结果。审核队列已耗尽，积压 3 条；用户 2026-10-01 指示“开小窗口修这 3 条”。用户已授权连续审核与合并修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。

唯一 EXECUTOR 仅可修改：WORKSET.json 列出的 3 个 target（mod-tome.lua、tome-cults.lua、tome-orcs.lua）以及 `evidence/quality/repair-window-58-20261001/` 下的修复证据。不改术语库。不得修改 source、source_tag、section、args_order、运行键、其他译文、规则工具或旧证据；不得 stage、commit、push、创建 agent 或修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

**本窗口是定向修改，不是全文重译。** 每条只改 SOURCE-CLAIMS 点名的片段（claim 中「现译片段 → 新片段」给出了建议写法，可在不改变其意思的前提下为衔接做最小调整）；不得借机改写其余部分。即使发现别处可疑，也只在报告中列出、不改。

保留 printf 占位符、`%%`、`#TAG#`、`<?...?>` 模板片段、`[i]`/`[/i]` 等 markup 的数量、顺序及适用位置；保留 source_tag。LF/TAB 结构与现译逐行一致。用 LuaJIT 加载三个译文文件，证明恰 3 个 target 变动且其他记录不变；执行 strict lint 及 git diff --check。无需完整门禁，宿主在独立复审后统一运行 17 项。主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证；DLC 源码只在 SOURCE-ANCHORS 给出的 checkout 下按条目路径取证，不扫 `/`、`/workspace` 或无关目录；DLC 源码仓库与 commit 未固定。

审查：cycle-0 `REVIEW/full` 用 Codex GPT-6.1 Sol（medium）；确认问题合并给一次 EXECUTOR fix；收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。v2 FINAL 如有任何 ISSUE，先修复并完成 RE_REVIEW，再重新 FINAL（同 cycle 用下一个 attempt）。max_cycles=5。reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。与已记录裁决相冲的指摘由宿主按裁决驳回；与本窗口修改无关的既有问题记 advisory 并 carry_forward。

## 条目与已确认修复依据

- 2822ed0142e25ad3d61be2eaf672c8f62b7a09dcfa94a8c60d795e5b2d1e30b0 | mod-tome.lua | mod-tome/data/lore/age-allure.lua | 第373批 surface 确认（宿主按固定 commit 624a673 game/modules/tome/data/lore/age-allure.lua:282/297/302/323 独立核验）：副歌“Hey, now, you're a guard now, stand vigil in the tanks”是对听者（第二人称）说的，与上一行“you're a healer”并列；现译把“你”误作“我”。四处「嘿，我，现为守卫，进入休眠仓，保持警戒。」→「嘿，你，现为守卫，进入休眠仓，保持警戒。」（只改“我”→“你”，其余不变）
- cc6d1a5034ef0a29fd00222ed3d95df63125db3f7784febbe1270fe331b14359 | tome-orcs.lua | tome-orcs/data/lore/pocket-time.lua | 第374批 surface＋contextual 确认（公开 Orcs DLC tome-orcs/data/lore/pocket-time.lua:55/63，来源未固定）：①“once he had enough practice to master a few of these”：「一旦他在这些方面都有了一些实战经验」→「一旦他练到足以精通其中几项」；②“she finally faced The Master head-on”主语是她：「她终于见到了吸血鬼领主迎面而来。」→「她终于与吸血鬼领主正面交锋。」；③“swearing incomprehensibly about unfairness”：「发表了一番关于不公平的费解的话」→「含糊不清地咒骂了一通不公平」。其余不变，<?...?> 模板与“————”保持。
- e2c9218ea95a18baa45059280337170935967edba71fca669c1529a01f214b26 | tome-cults.lua | tome-cults/data/lore/fay-willows.lua | 第373批 contextual 确认（公开 Cults DLC data/lore/fay-willows.lua:671/677 一带，来源未固定）：①“Having lost control of the battlements, a small force of the skeletons moved to take over the gates”——骷髅已在城垛上，是转去夺取城门放外面的亡灵进城：「一小队骷髅冲了进来，接管城门」→「一小队骷髅转而去夺取城门」；②“leaving the rest of us to fend off the encroaching undead horde”：「抵御入侵的不死部落」→「抵御步步逼近的亡灵大军」；③“ordered the mages to form a firing line”：「组成一条火线」→「排成射击队列」。其余不变。
