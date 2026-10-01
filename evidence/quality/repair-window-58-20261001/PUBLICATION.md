# 修复窗口 58 发布记录

## 范围

窗口 57 的 87 个 successor 经第 373 批（`batch-eb93936e38c73186d222`）与第 374 批（`batch-2e8beab0b2f9b05c4c94`）审核后确认 3 条；审核队列耗尽、积压 3 条。用户于 2026-10-01 指示“开小窗口修这 3 条”。

- 主游戏 1 条（`2822ed0142`，age-allure）：副歌“嘿，我，现为守卫”改为“嘿，你”，共 4 处。
- Cults 1 条（`e2c9218ea9`，fay-willows）：骷髅转而去夺取城门、步步逼近的亡灵大军、排成射击队列，以及 FINAL 确认的两处 lockstep“步调一致”。
- Orcs 1 条（`cc6d1a5034`，pocket-time）：练到足以精通其中几项、与吸血鬼领主正面交锋、含糊不清地咒骂了一通不公平。

主游戏按 manifest 固定 commit `624a673` 核验；DLC 来源仓库与 commit 未固定。本窗口不改术语库；无同键兄弟。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-R0.json`](publication/ADJUDICATION-R0.json)、[`publication/ADJUDICATION-F0.json`](publication/ADJUDICATION-F0.json)、[`publication/ADJUDICATION-R1.json`](publication/ADJUDICATION-R1.json) 与 [`publication/ADJUDICATION-F1.json`](publication/ADJUDICATION-F1.json)。

`execute-01` 修改 3 条 → REVIEW(0) `r0a1`（GPT-6.1 Sol）提出 3 个 ISSUE：pocket-time“秒杀”按第 374 批裁决驳回，age-allure 歌词意译与 fay-willows lockstep 记 advisory → FINAL(0) `f0a2`（Opus 5.5）确认 1 项（fay-willows 两处 lockstep，由 advisory 升为 confirmed）→ `execute-02` → RE_REVIEW(1) `r1a1` 记 1 项 advisory（age-allure 食人魔化歌其余意译句，carry_forward）→ FINAL(1) `f1a2` 在 `/workspace/tome4-dlcs` 下 grep ashes-urhrok，越出输入指定源码位置，故拒收（见 [`publication/INVALID-F1A2.json`](publication/INVALID-F1A2.json)，不计轮次）→ fresh retry `f1a3` 3/3 OK，cycle 1 收敛（`max_cycles=5`）。

## 门禁与标识

门禁 17/17 全过，含严格构建；状态为 `DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

- 译文提交：`54c307a7300b08c917b16d6f4ff0001c19e70b9d`
- 新 catalog：`34b6eb1b93d977a0919cb2f67967632f079c88904afd5992e602b9d5587e9ecf`
- migration：`2f023eaf7da8e87222d2d242509b8b9ef2d040b0a77226c598dff8ae6265894d`

## 后续

3 个 successor 必须作为第 375 批重新审核，不继承旧 revision 的 done 状态。窗口 59 积压 0 条。

本 publication child 待宿主归档。
