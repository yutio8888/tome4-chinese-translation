# 修复窗口 7 出版证据与暂停交接

## 范围与成果

- 审核 253（`batch-ba766c90924912867b02`）已完全闭合：72 `done` / 8
  `repair_required`，证据提交为 `3927ca05a43daee81bb2a2fadaf77d2b3b881d0b`，收尾提交为
  `e103379a5e809923401aa0099cfbdc9f104725ca`；收尾后的 queue、push、远端 HEAD 与 SQLite
  evidence head 核验均已完成。原始证明见
  [review253-push-verification.json](publication/review253-push-verification.json)。
- 窗口 7 仅处理审核 253 确认的八个 target：疾病传播范围、法杖粗大尖端、时间抹除日志时态、
  盾牌敏捷替代力量的属性加成范围、Mind Storm 弹体含义与 3 LF / 6 TAB、挽歌护盾的持续时间
  延长及抗争/怨恨语义、spinneret 的吐丝器官语义、eviscerated 的剖腹/内脏意象。
- 译文提交为 `312dcd6844f80fff34911999bffab7a8f954e34f`，只修改 `mod-tome.lua` 的八个
  target；没有修改术语库、规则或工具。Daze=眩晕与 Probability Travel=次元移动保持基线术语，
  spinneret 只改本批未鉴定物品名，不扩大到已明确排除的兄弟条目。
- publication EXECUTOR 没有修改 Lua、术语、规则、工具、旧证据或 `.ai`，也没有重跑 queue、catalog、
  migration-chain、复审或完整门禁。

## 独立复审、源码裁决与收敛

四成员 stage 与最终 full review 分开记录，历轮原始 `ISSUE` 均保留：

- R0 四 lane 原始结果为 6 `OK` / 2 `ISSUE`。宿主依据固定 ToME 源码确认疾病应传播目标身上的
  所有疾病，并确认盾牌动作应为持盾跃向目标；两项均在原八 target 内有界修复。
- R1 四 lane 原始结果为 6 `OK` / 2 `ISSUE`。Mind Storm 的额外弹体总量量词为一级 confirmed，
  获有界修复；spinneret 的已鉴定名称与任务文本兄弟项只记 `advisory/declined_scope`。
- R2 四 lane 原始结果为 6 `OK` / 2 `ISSUE`。第二轮后的 SENIOR `scope_audit` 对挽歌实际触发
  条件结论为 `keep`，对 spinneret 范围外兄弟项结论为 `narrow`。宿主只接受一个挽歌触发句修复：
  排除自身施加及 `other` 类型的负面状态；没有扩大兄弟项或默认三轮上限。
- R3 四 lane 原始结果为 7 `OK` / 1 `ISSUE`。Vault 的选择坐标/实际落点观察经源码核验后只记
  非阻断 clarity advisory，不构成一级错误，故按收敛规则进入最终全量复审。
- cycle 3 attempt 2 的 full `FINAL_REVIEW` 原始结果为 8 `OK` / 0 `ISSUE`，范围内无 accepted
  或 deferred finding。该最终 8 `OK` 不改写此前各轮的真实 `ISSUE` 与裁决。

完整裁决见归档中的 [REVIEW-SUMMARY.json](orchestration/.ai/task/repair-w7-20260922/REVIEW-SUMMARY.json)
及各轮 `ADJUDICATION`。实施/复审 child 共 22 个，均在 immutable checkpoint 中确认归档；publication child 也已由宿主收获并确认归档，合计23个。
最终生命周期与状态见[收尾增量](closure/snapshot-delta.json)。

## 门禁、冻结归档与重放

- 最终完整门禁 `.artifacts/i18n/ci-gates/run.4d0v0980/results.json` 为 17/17 通过，包含严格
  addon build；最终译文 SHA-256 为
  `27bbaafdde1755891aa4a7ce3f4c2f5c1bb5e20554dc626f2bb3fb332889a434`，任务为
  `DONE_VERIFIED`。
- [orchestration-pack-manifest.json](orchestration-pack-manifest.json) 与 producer manifest
  逐字节相同。452 个目标均按声明的 SHA-256 和字节数复制并复核，合计 2,317,751 bytes。
  归档 `STATE.json` 来自 immutable `STATE-review-validation-checkpoint.json`，不是 publication
  阶段的可变 STATE；冻结文件的行末与空白未清洗。
- producer 的独立快照回放见 [PACK-REPLAY-PROBE.json](publication/PACK-REPLAY-PROBE.json)。
  本出版阶段又对受跟踪归档只读运行 `ai_state_check.py`，结果同为
  `DONE_VERIFIED: DONE predicate verified`。

## Catalog、迁移与真实计时

- 第一次 queue rebuild：RC 0，`220.09007790399482` 秒。
- 单次候选 catalog build：RC 0，`3.464086058025714` 秒。
- 单次 migration-chain：成功，总计 `230.27504705701722` 秒；plan 为 RC 0、
  `222.38536847900832` 秒，check 为 RC 0、`3.253067454963457` 秒，apply 为 RC 0、
  `4.59663287200965` 秒；投影调用一次。
- catalog 从 `6f08ccf5394d2f0431a066c1315ba5abcdeaed1928e4781a0b1cb65e37e68405`
  迁移到 `0fece77f6c05306c2706b263729cc1a3b5fcdf1dc29f58bd41af380204595696`。
  8 条 revision changed、29,820 条 unchanged，0 ambiguous、0 unmapped；8 个 successor 已入队，
  必须重新审核，不能继承旧 revision 的完成态。
- migration ID 为
  `677e6622a2146f9f9686ee91c9d1bc3f02990c8d08547df721786877dd287325`。catalog entries、
  exclusions、manifest 的 SHA-256 依次为
  `1bf8b0be16804ea7ad36b35ce73840d250610952b2dfbccf37c13363c6824d3c`、
  `1288283aa25ae95c3bf311850e168ecb04d25cd09370e02fb84e5fb9110a7da0`、
  `b177257a6962c1e8f657a50d179ca35c983c6d391f184c79567e420c3a9b6f17`。

五个候选 catalog 文件、migration 和 [publication/](publication/) 中 16 个 producer/253 收尾
附件均按来源逐字节安装并复核。

## 已完成的宿主收尾与暂停状态

用户于 2026-09-22 明确要求“这轮修复完成后暂停并撰写handoff文档”。因此窗口 7 闭合后为
STOP，不得自动启动审核 254；此前连续授权不覆盖暂停后的新批次，继续工作需要新的用户授权。

证据/catalog/migration提交`bfa1a096da0b6d790167de0f600c7aff41dfcb59`，提交后的第二次queue rebuild、push、
本地/远端/SQLite三方核验均已于`2026-09-22T16:14:31.628477+00:00`完成。
队列为 **22254 done / 1 repair_required / 24 blocked / 7549 queued**，8个successor逐条验证queued。
23个child全部确认归档，最终STATE为`DONE_VERIFIED`。

原452项包保持不变；27项收尾增量与基础包合并独立重放通过。
见[实测收尾证明](closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-CLOSURE.json)、
[增量清单](closure/snapshot-delta.json)及[重放结果](closure/replay-verification.json)。
提交检查发现12处冻结历史空白，均以来源和Git索引SHA绑定记录例外，原字节未修改。
首次收尾脚本遗漏补丁中的space-before-tab诊断，经一次有界诊断完成独立核验；
详见[提交核验](closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-STAGING-VERIFICATION.json)。
最终handoff与本收尾证明随文档提交保存；此后仅同步queue/push，当前STOP，未启动254。

旧 Archmage、旧回忆录 pending、`RW1-SIB-01/02`、旧 blocked 及 spinneret/Vault 范围外兄弟
或后续观察均保持原状态，不因本次闭合而清零或扩大。`.ai/consult/`、recipe 和 15 个旧
source-workset 保留，不纳入本次清理。
