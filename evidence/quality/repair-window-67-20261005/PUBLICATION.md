# 修复窗口 67 发布记录

## 范围

本窗口发布 2 条译文：`mod-tome.lua` 1 条、`tome-cults.lua` 1 条；无术语改动。

- 宿主补充 `9d3fc01bdf`（不计积压）：Cults 奎科加章节（`kroshkkur.lua:107`，源文 `records of Anglowen`）“根据安格列文的记载”→“根据安格利文的记载”，按 `terminology/places.tsv:20` Angolwen＝安格利文（preferred）；窗口 66 REVIEW r0a1 确认诸神前言同名术语时发现。
- 用户 2026-10-05 授权的 `fc55a88fd6`：`mod-tome.lua:422` 护送奖励日志“%s 技能 %s (+%d 等级)”→“%s技能 %s（+%d 级）”，与已改的同族选项（`mod-tome.lua:425`、`tome-orcs.lua:582`）一致；源码 `EscortRewards.lua:537` → `escort-quest.lua:36` → `escort-duty.lua:64`“作为奖励，你%s。”。
- 新译文由宿主写定（[`publication/NEW-TARGETS.json`](publication/NEW-TARGETS.json)），EXECUTOR 逐字替换；宿主核验 2 条 after 与 new_target 逐字相等（[`publication/HOST-EXACT-DIFF.json`](publication/HOST-EXACT-DIFF.json)）。窗口内修复后宿主重新逐字核验 2 条：REVIEW r0a1 确认的奎科加章节 librarians 漏译（“记录者”→“图书管理员”）与宿主同条确认的 might be 被写成“其实是”（→“可能来自”），由 execute-02 修复，见 [`publication/HOST-EXACT-DIFF-POST-FIX1.json`](publication/HOST-EXACT-DIFF-POST-FIX1.json)。`NEW-TARGETS.json` 是 execute-01 的冻结输入，保留该条初稿；终稿以 POST-FIX1 核验为准。
- 主游戏按 manifest 固定 commit `624a673` 核验；Cults 源码来源未固定，按公开源码核验并如实标注。四个 locale 文件中无同键兄弟；主游戏 `mod-tome/load.lua` 段另有该章旧版文本的副本（`e4824491182e`），运行时键不同且为已登记死键（`batch-ac27e658…` 中经 host-block 放行），不同步。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 → REVIEW r0a1（gpt-6.1-sol）1 OK／1 ISSUE，确认忠实性 1 条（奎科加章节 librarians 被译作“记录者”）＋宿主同条确认 1 条（might be 被写成“其实是”），execute-02 → RE_REVIEW r1a1 2/2 OK → FINAL f1a2（Opus 5.5）2/2 OK；第 1 轮收敛（`max_cycles` 5），无无效尝试。

门禁 17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`0de585f6fa87ef93761e4a85e168a70d06cebb30`
- 新 catalog：`59f6d8272ff985ec3476131c03ce8ee38505a91bb284abf48813f71f09369913`
- migration：`a0f4f2206d3ff692ae44f032e55b69e282b42d9240718e6da31d6bfd5b1a3038`

## 后续

- 2 个 successor 必须重新审核，不继承旧 done。
- 下一个修复窗口（68）积压 0 条。

本 publication child 待宿主归档。
