# 修复窗口 11 出版证据

## 范围与结果

本窗口处理审核 257 的 4 条确认项：Trollmire 日记残页的两处空行与 `get wind of` 习语、
Torment 的伤害阈值与判定方式、鼠巫妖头骨的未鉴定名称，以及角色面板“状态效果抗性”标题。
译文提交为 `6eca6f9952781a1e98d117d35fac2c7028bacb85`。

任务 `repair-w11-20260923` 的 `execute-01` 实施了 4 条修复。`REVIEW(0)/full`
（`codex/gpt-6-sol`）结果为 3 OK / 1 ISSUE：指出 Torment 会在
`torment.lua:144–149` 对每个冷却中的技能分别进行概率判定。该 reviewer 回显的
`revision_key` 有一段重复；宿主核对原生日志后进行了 hand-attribution，原始字节保留于
`r0a1-original.raw`，当时先将该观察判为 pending。

`FINAL(1)/full`（`claude/claude-opus-5-5`）同样为 3 OK / 1 ISSUE，指出相同的机制问题。
宿主依据 `AGENTS.md`“机制以源码实际行为为准”的规则，将该问题更正为 confirmed 一级缺陷；
R0 的 pending 记录已标记为 superseded，不列入待用户审阅清单。`execute-02` 有界修复为
“每个冷却中的技能各有 %d%% 概率减少 1 回合冷却时间”。随后 `RE_REVIEW(2)`
（`codex/gpt-6-sol`）为 4 OK，`FINAL(3)`（`claude/claude-opus-5-5`）为 4 OK。

完整门禁两次均为 17/17 通过并包含严格构建：一次位于 `execute-01` 后，另一次位于
`execute-02` 后并作为最终门禁。任务达到 `DONE_VERIFIED`。

## Catalog 与迁移

新 catalog 为 `5020a313d684c44e837ce0bd2bd8a4062ad42a784b356cc802a934d6dfa1d957`，
migration 为 `5033b3e3c151150bebed931811e95f1cd91e7838e16773d0fe2e43bf4135a176`。
迁移结果为 4 条 `revision_changed`、29,824 条 `unchanged`、0 条
`ambiguous/unmapped`；4 个 successor 等待重新审核，不继承原 revision 的 done 状态。

## 生命周期与后续边界

2 个 executor 与 4 个 reviewer child 均已确认归档。本 publication child 尚待宿主归档。
证据提交、第二次 queue rebuild 和 push 仍由宿主执行，此处不提前宣称完成；完成后继续审核
258（默认 80 条）。

原始附件见 [publication](publication/)，冻结任务快照清单见
[orchestration-pack-manifest.json](orchestration-pack-manifest.json)。
