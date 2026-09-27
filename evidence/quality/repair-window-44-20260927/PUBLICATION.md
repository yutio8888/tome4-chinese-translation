# 修复窗口 44 发布记录

## 范围

来源批次 343、344、345、346、347、348 共 24 条确认问题（343 批 2、344 批 7、345 批 3、346 批 1、347 批 6、348 批 5），均为 `tome-orcs.lua`，已全部修复；无跨组件同键兄弟（`check_siblings` 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 预检

开窗前宿主预检 12 个结构/运行时要点（[`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)：换行、制表符、markup 与寒冰之怒 `tformat` 裸 `%`），并入首轮修复。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修复 24 条 → REVIEW(0) r0a1（GPT-6 Sol）PASS → FINAL(0) f0a2（Opus 5.5）3 条确认（卡托尔告示商品名、部落史 squeamish、帕默广播 grunts/slashing）→ execute-02 → RE_REVIEW(1) r1a1 1 条 advisory（珍珠面板，与第 37 行同物一并转窗口 45）→ FINAL(1) f1a2 2 条确认（血液灵晶“两倍”被删、选举告示 rarely）＋1 条 advisory（Chief Councilor 保持“议长”）→ execute-03 → RE_REVIEW(2) r2a1 2 条确认（修复者日志“童年”宾语、太阳堡垒书信原谅对象）→ execute-04 → RE_REVIEW(3) r3a1 1 条 advisory（闪电球 bolt/ball，待审第 33 项）→ FINAL(3) f3a2 24/24 OK，cycle 3 收敛（max_cycles 5）。

## 重启

窗口在 ADJUDICATE cycle 1 因本机重启暂停，暂停前全部 child 已归档确认；恢复后续跑，无 child 跨越重启。

## 门禁

首轮 04-quality-facts-unit-tests 因环境变化失败（重启后 `PATH` 新增 `/opt/agents/bin` 包装器遮蔽真实 `pi`，详见 [`publication/HOST-NOTES.md`](publication/HOST-NOTES.md)），去掉该目录后完整重跑 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`16eadd082289e2cf1aef22fb8a9a32d3612175e0`
- 新 catalog：`8a407b557a4a3924bc894e92a8a52148bbf2305bcb3c66951e2701b6672fa271`
- migration：`50e8f36cb7bd8eba7ee5a8258569e832c972d6f0de3f99e98dd962ea006359a0`

## 后续

24 个 successor 必须重新审核，不继承旧 done。窗口 45 预定并入 Psy Worm 裸 `%`、lint 漏检修复与 Destructicus 面板两条。待用户审阅项不变。

本 publication child 待宿主归档。
