# 修复窗口 52 发布记录

## 范围

本窗口处理 4 条宿主补充（审核队列耗尽、积压为 0 时经用户于 2026-09-28 批准）：

- `b5e754f6ab`：Orcs lore 分类中的 Sunwall Observatory 从“太阳堡垒瞭望台”改为“太阳堡垒观星台”。唯一文献为天文学家日志，区域名、任务和成就均使用“观星台”。
- `5d156a408b`：艾琳结局成就 Last Instant of Sanity 补回 `your patron`＝“太阳主上”及 `in a searing flash`。
- `1e5fe478f9`：同缺陷兄弟 AOADS_BURN 成就补回 `your patron Distant Sun`＝“你的主上遥远的太阳”。
- `d58b645c3b`：同缺陷兄弟夏·图尔结局叙述将 `succumbed to the fight` 改为“在这场搏斗中倒下”，并补回“太阳主上”。

修改涉及 `mod-tome.lua`、`tome-orcs.lua`；术语库 `narrative.tsv` 的 Sunwall Observatory 行改为“太阳堡垒观星台”并升为 `preferred`（用户 2026-09-28 裁决）。无跨组件同键兄弟（`check_siblings` 为 0）。主游戏按 manifest 固定的 engine commit `624a673` 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。Archmage 按用户同日裁决保留“元素法师”，范围外 `8b977dd836` 不在本窗口。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修改 4 条与术语 1 行 → REVIEW(0) r0a1（GPT-6 Sol）4/4 OK → FINAL(0) f0a2（Opus 5.5）4/4 OK。cycle 0 收敛（`max_cycles` 5）。

## 门禁与标识

门禁 17/17 全部通过，包含严格构建；状态为 `DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

- 译文提交：`9362911053e2ff022f3ed7d7e80cab07459ed930`
- 新 catalog：`538a4d20024882e2bf0908ca25a3185a0de5d60fa78eb92bff1f852aa55f0d13`
- migration：`6b75b260078d4a5d606542869f59a04240f16e70cfb732fdb05013734159bb44`

## 后续

4 个 successor 必须重新审核，不继承旧 revision 的 done 状态。本 publication child 待宿主归档。
