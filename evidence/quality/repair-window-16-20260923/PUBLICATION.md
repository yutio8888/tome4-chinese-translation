# 修复窗口 16 出版证据

## 范围与结果

本窗口处理审核 262 的 7 条确认项：50 级祝贺文本恢复段间空行并改为“勇敢地”；星辰契约将
`bond` 译为“羁绊”，明确光辉引力会将敌人拉向被击中的目标，并恢复 `\t\t` 缩进；不死猎人
指南修正六处增译、夸大、因果错置、弱化和巫妖段反义，并将多拆出的段落合并回原结构，LF
由 86 降至 72，与原文一致；矮人送药改为“加了点好料，明早可有你受的”；成就改为“以自身
为祭品关闭虚空传送门”；牺牲死讯改为“牺牲了%s，将维网带给众生”；强化弹药 Venomous
改为“自然伤害”。

任务 `repair-w16-20260923` 的 `execute-01`（`codex/gpt-5.6-sol`）实施了 7 条修复。宿主
verify 暴露 lore 段落拆分，`execute-02` 仅合并段落。`REVIEW(0)/full`
（`codex/gpt-6-sol`）结果为 6 OK / 1 ISSUE：Eyal 应译为“埃亚尔大陆”，裁决为 advisory，
列入 pending #16。`FINAL(1)/full`（`claude-opus-5-5`）结果为 6 OK / 1 ISSUE：署名
“不死猎人”存在歧义；宿主初判 advisory，但 `DONE` 检查要求最新 FINAL 无 ISSUE，故改判为
二级问题并有界修复。`execute-03` 仅将署名改为“一名不死生物猎人的指南”。
`RE_REVIEW(2)`（`gpt-6-sol`）结果为 6 OK / 1 ISSUE，仍为同一 Eyal 观察并裁决为
advisory；`FINAL(3)/full`（`claude-opus-5-5`）结果为 7 OK，任务收敛。完整门禁
17/17 通过并包含严格构建，任务达到 `DONE_VERIFIED`。

## Catalog 与迁移

译文提交为 `3a21f17035b51c61f592858e2b5ca7a6e9c51d6d`；新 catalog 为
`9b4f2e06ce73c07cc0ca9810db96caba529a5f15b175558803b21f1313fb2b4e`，migration 为
`456baa4ae824b48ffdd8c7ec72c1c93055e8fb4c51077e79eab0852d8c2747a0`。迁移结果为
7 条 `revision_changed`、29,821 条 `unchanged`、0 条 `ambiguous/unmapped`；7 个
successor 等待重新审核，不继承原 revision 的 done 状态。

## 待用户审阅、生命周期与后续边界

待用户审阅清单新增第 16 项（Eyal 全库译法）和第 17 项（lore 标题“不死猎人指南”两处），
由宿主在证据提交中写入 `pending-user-review.md`。3 个 executor 与 4 个 reviewer child 均已
确认归档，本 publication child 尚待宿主归档。

本证据提交、第二次 queue rebuild 和 push 仍由宿主执行，此处不提前宣称完成；完成后继续审核
263（默认 80 条）。

原始附件见 [publication](publication/)，冻结任务快照清单见
[orchestration-pack-manifest.json](orchestration-pack-manifest.json)。
