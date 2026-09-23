# 修复窗口17发布记录

修复窗口17仅处理审核263确认的5条问题，未扩大范围：

- 猎头者挑战播报改为“你取下了 %s 的首级，令本层所有敌人为之迟疑”，不再误述为“暂停”。
- Exploit Weakness 写明近战攻击命中，并恢复结尾 `\n\t\t`。
- 单项效果抵抗提示改为“效果抵抗几率/完全抵抗该特定效果的几率”。
- 教程完成文本删去3处词中硬换行，LF 由14降至11。
- 思维形态说明恢复原文换行结构，LF 由7降至3；`warrior` 改用本库“战士”。

任务 `repair-w17-20260923` 中，`execute-01`（`codex/gpt-5.6-sol`）实施5条修改。`REVIEW(0)/full`（`codex/gpt-6-sol`）给出4 OK / 1 ISSUE，确认 `R0-HEADHUNTER-OVERSTATE`：`execute-01` 增译“失去对你的锁定”，扩大了 `setTarget` 的实际范围。`execute-02` 仅删去该增译分句。`FINAL(1)/full`（`claude-opus-5-5`）给出5 OK，任务收敛。完整门禁17/17通过，包含严格构建，状态为 `DONE_VERIFIED`。

译文提交为 `8390dd69d6d3ea359ada0ea2ea838cd533e14aa4`；新 catalog 为 `78635878a70f7ff2d9a1d4e36e7ad9115ab8a80d906670ecff0fce7332abd239`；migration 为 `5168dcc75a66cf6b89dc5c5ee1f0753064d427cc9461ad4a7ca1680c0fb084ec`。迁移结果为5条 `revision_changed`、29,823条 `unchanged`、0条 `ambiguous/unmapped`，5个 successor 待重新审核且不继承 `done`。本窗口无新增 pending。

两个 executor child 与两个 reviewer child 均已归档确认；本 publication child 待宿主归档。冻结编排证据见[编排快照](orchestration/)，逐字复制的发布附件见[publication](publication/)，迁移记录见[迁移文件](../../production-review-v2-lite/migrations/5168dcc75a66cf6b89dc5c5ee1f0753064d427cc9461ad4a7ca1680c0fb084ec.json)。本证据提交、第二次 queue rebuild 与 push 均由宿主后续执行，尚未宣称完成。
