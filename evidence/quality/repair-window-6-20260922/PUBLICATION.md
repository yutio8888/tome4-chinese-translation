# 修复窗口 6 出版证据

## 范围与成果

- 审核 252 已完成，结果为 78 `done` / 2 `repair_required`。收尾提交
  `805b67263c3359441a4e6e12f3ebd0d2bdc5a0da`、queue 同步、push 与远端核验已于
  2026-09-22 13:27 UTC 完成；核验原件见
  [review252-push-verification.json](publication/review252-push-verification.json)。
- 因审核 252 确认 newline 问题，窗口 6 在安全边界提前修复，范围恰为两条真实 repair
  preflight：日记条目仅恢复省略号前后两个空行，文字不变；古战场成就补回主动惊扰行为和
  后果关系。
- 译文提交为 `38e666aaae9e5738819e3b6525398b9bfc9872eb`，只修改 `mod-tome.lua`
  的两个 target。`source`、`source_tag`、`args_order`、printf、markup 和 TAB 均未改变，
  没有术语库变更。
- 本出版阶段没有修改 Lua、术语、规则、工具、旧证据或 `.ai`，也没有重跑 queue、catalog、
  migration-chain、复审或完整门禁。

## 复审、门禁与生命周期

- 首轮 full `REVIEW` 和最终 full `FINAL_REVIEW` 的原始结果均为 2 `OK` / 0 `ISSUE`。
  没有追加修复轮或 SENIOR 升级，默认 `max_cycles=3` 未扩展。
- 最终完整门禁 `run.ko6u_j8h` 为 17/17 通过，包含严格 addon 构建；任务状态为
  `DONE_VERIFIED`。
- 实施、首轮复审和最终复审三个 child 均已确认归档。本出版 child 尚待宿主收获并确认归档，
  本文不提前宣称其已归档。
- [HOST-AUDIT-COUNT-CORRECTION.json](publication/HOST-AUDIT-COUNT-CORRECTION.json)
  仅把实施审计汇总中的 12 次调用更正为真实 11 次；全部实际调用已逐项检查。原 immutable
  快照保持不变，范围裁决及 finding 均未改变。

## 冻结归档与重放

归档的 [orchestration-pack-manifest.json](orchestration-pack-manifest.json) 与 producer manifest
逐字节相同。清单的 97 个目标在复制前后均按声明的 SHA-256 和字节数核对，合计
765,623 bytes。归档 `STATE.json` 明确来自 immutable
`STATE-review-validation-checkpoint.json`，不是出版时的可变 `STATE.json`。冻结源码、SPEC、
原始报告和 literal 行末空白均保持原始字节。

producer 的独立 snapshot 重放结果保存在
[PACK-REPLAY-PROBE.json](publication/PACK-REPLAY-PROBE.json)。本出版阶段又从受跟踪归档目录
只读运行：

`python3 -B tools/ai_state_check.py .ai/task/repair-w6-20260922/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-6-20260922/orchestration --target DONE`

实际结果为 RC 0，stdout 为 `DONE_VERIFIED: DONE predicate verified`，stderr 为空。

## Catalog、迁移与真实计时

- 第一次 queue rebuild：RC 0，`222.21649448899552` 秒。
- 单次候选 catalog build：RC 0，`3.5976528999744914` 秒。
- 单次 migration-chain：成功，总计 `231.52436333103105` 秒；plan 为 RC 0、
  `223.6283655950101` 秒，check 为 RC 0、`3.2227891150396317` 秒，apply 为 RC 0、
  `4.629509743012022` 秒；投影调用一次。
- catalog 从 `c267a00eaf39f49b99266912241cfed79dfcbda440903763975ea2e4334a239d`
  迁移到 `6f08ccf5394d2f0431a066c1315ba5abcdeaed1928e4781a0b1cb65e37e68405`。
  2 条 revision changed、29,826 条 unchanged，0 ambiguous、0 unmapped；2 个 successor
  已入队，后续必须重新审核，不能继承旧 revision 的完成态。
- migration ID 为
  `92da0238e3a17f7b5d3b4e46156ef0b9d5bacfd653bb2e00618d6f0ede25a83d`。
  catalog entries、exclusions、manifest 的 SHA-256 依次为
  `f72cfe936694012d0d2b9c53b6b37893ff874c0446fe7f24e068baa43c0deb04`、
  `1288283aa25ae95c3bf311850e168ecb04d25cd09370e02fb84e5fb9110a7da0`、
  `4b045f8829798256a67867e01ea16c98a5456c8417c5e05e3f57299633d80fd6`。

原始 producer 核验、计时和日志保存在 [publication/](publication/)；五个候选 catalog 文件、
migration、15 个 publication 原始附件以及 `mod-tome.lua` 相对译文提交均已逐字节复核。

## 尚未完成的出版步骤

本文件生成时实际 `HEAD` 为译文提交 `38e666aa…`，本地远端跟踪引用 `origin/develop` 为
`805b6726…`。本次证据/catalog/migration commit、提交后的第二次 queue rebuild、push 与远端
复核仍待宿主执行；本文不宣称这些步骤已经完成。闭合后继续审核 253，默认 80 条，并开启新的
修复窗口。

旧 Archmage、旧回忆录 pending、旧 blocked、审核 252 范围外格式 pending 以及
`RW1-SIB-01/02` 的边界不扩大、不清零。`.ai/consult/`、`recipe` 和 15 个旧 source-workset
保留，不纳入本次提交或清理。
