# 修复窗口25发布记录

## 范围与结果

本窗口处理审核271确认的8条修复：

- 疲劳圣印改为“经过圣印的敌人会减速”。
- 指令水晶球（亡灵）描述改为“黑暗的幻象充满你的脑海”。
- 血祭施法效果改为“堕落系法术消耗生命值而非活力值”。
- 减速说明恢复末尾换行与缩进。
- 摄魂剑·莫瑞格日志改为“汲取了%s的被困灵魂，施展%s”。
- 第一滴血补回“命中时”与“（若能标记）”。
- 阿马克泰尔壁画 lore 逐句重译。
- 盗匪首领日志恢复威胁语气与“绑在柱上烧死”。

任务 `repair-w25-20260923` 中，`execute-01`（`codex/gpt-5.6-sol`）实施8条修复；宿主逐条逐行核对行数、空行下标与行首 TAB。`execute-01` 原生日志含2次 Codex `wait` function_call，仓库解析器白名单未收录，宿主经仅增补这两类条目的临时解析器副本收取，详见[宿主 executor 审计](orchestration/.ai/task/repair-w25-20260923/HOST-EXECUTOR-AUDIT.json)。`REVIEW(0)/full`（`codex/gpt-6-sol`）结果为 7 OK / 1 ISSUE：血祭施法效果的英文原句本身与 `incVim` 实现不符，实际机制仅在活力不足时以生命支付缺额；译文忠实原句，宿主判为 advisory，并登记 pending 第19项。`FINAL(1)/full`（`claude-opus-5-5`）结果为 8 OK，任务收敛，无修复轮。完整门禁全部通过并包含严格构建，状态为 `DONE_VERIFIED`。

译文提交为 `805a9f155dff64cc18cf644b0af2856b0936e06f`；新 catalog 为 `38cb5f33c905a333728676e30a67692632830852be8790e532980702de21a18f`；migration 为 `f2ddf2cbd8e0610b40955d746594ed530f3dbadc05dee7153fff88b708434f38`。迁移结果为8条 `revision_changed`、29,820条 `unchanged`、0条 `ambiguous/unmapped`，8个 successor 待重新审核且不继承 `done`。本窗口新增 pending 第19项，pending 文件由宿主维护。

1个 executor 与2个 reviewer child 均已归档确认；本 publication child 待宿主归档。冻结编排证据见[编排快照](orchestration/)，PACK-MANIFEST 逐字副本位于[窗口根目录](orchestration-pack-manifest.json)，逐字复制的发布附件见[publication](publication/)，迁移记录见[迁移文件](../../production-review-v2-lite/migrations/f2ddf2cbd8e0610b40955d746594ed530f3dbadc05dee7153fff88b708434f38.json)。

## 后续

本证据提交、第二次 queue rebuild 与 push 由宿主执行；完成后继续审核272（默认80条）。以上后续步骤尚未完成。
