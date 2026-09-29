# 修复窗口 53 发布记录

## 范围

审核队列耗尽后积压 18 条（第364批 4 条、第365批 5 条、第367批 3 条、第368批 6 条），用户于 2026-09-29 选择立即开窗。范围包括主游戏 16 条（`mod-tome.lua`）和 Orcs 2 条（`tome-orcs.lua`）；术语库 `classes.tsv` 的 Archmage 行升为 `preferred`（用户 2026-09-28 裁决保留“元素法师”）；另有同键兄弟 1 条 runtime-sync（caldizar `55872e196b` 逐字节同步已复审的 `d64daff63a`）。主游戏按 manifest 固定的 engine commit `624a673` 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。范围外 `8b977dd836`（Archmage）仍为 `pending_repair`，不在本窗口。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修改 18 条与术语 1 行 → REVIEW(0) r0a1（GPT-6 Sol）16 OK／2 确认（速射姿态按实现只需投石索、夏·图尔内乱句）→ execute-02 → RE_REVIEW(1) r1a1 17 OK／1 确认（噩梦诅咒“折磨”按实现反击来源者）→ execute-03 → RE_REVIEW(2) r2a1 18/18 → FINAL(2) f2a2（Opus 5.5）17 OK／1 确认（夏·图尔 lore 首段，宿主整条逐句另补 4 处）→ execute-04 → RE_REVIEW(3) r3a1 18/18 → FINAL(3) f3a2 18/18，cycle 3 收敛（`max_cycles` 5）→ execute-05 runtime-sync。

## 门禁与标识

门禁 17/17 全部通过，包含严格构建；状态为 `DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

- 译文提交：`359798c301d07abbccfa503ccd9c2b5657c3e725`
- 新 catalog：`cd2d8f8880856795f5a4650efad202178c9b660a338bcd272c60bd158d073510`
- migration：`7ed5bcec6d8c59a381f37e30588935e4f399e2eb8a738651d5a1b0b25c4033da`

## 后续

19 个 successor 必须重新审核，不继承旧 revision 的 done 状态。本 publication child 待宿主归档。
