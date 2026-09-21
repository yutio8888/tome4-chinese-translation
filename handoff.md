# 翻译审核当前交接

更新时间：2026-09-21（审核 241、修复 266 完成后）

## 当前状态

- 生产审核在本次性能优化期间保持暂停；已完成至审核批 241、修复批 266，下一审核批为 242。
- 当前没有需要从活动 checkpoint 恢复的交接。恢复前仍须核对 HEAD、queue、工作树和真实 task 状态；
  只有主代理完成候选验证后可明确通知原 Opus 5 宿主恢复。
- 本任务不继承历史 push、开 PR 或发布授权；不得由性能脚本自动 commit/rebuild/push。
- 当前唯一已知 `repair_required` `8b977dd836…` 属未解决口径，不计入新的可执行 20-revision 阈值，
  不得因此永久阻塞后续审核；本轮优化不裁决它。
- 旧实现对该 revision 所在历史 batch 的真实 preflight 已正确拒绝：该 batch 部分 repair rows 已不是
  current durable winners。baseline 为 2 次真实投影（约 210.35 秒、210.91 秒），总墙钟 423.89 秒，
  queue/checkpoint 未变。候选必须对同一输入保持同一拒绝和零 workset，不得放宽 winner 校验。

## 首轮有界试运行

原 Opus 5 宿主恢复后，从审核批 242 开始，最多连续完成 242–244 三批。每批完成裁决后累计本窗口新增、
confirmed 且可执行的 repair revision，按 revision 去重：达到 20 条，或出现机制/运行/placeholder 等高影响
confirmed finding 时，在当前批 finalize 且 checkpoint 已移除后提前进入修复窗口。三批结束仍有可执行项时
同样进入一个修复窗口；没有可执行项则不制造空 repair/migration。

修复窗口须对每个已提交来源 batch 分别 preflight，建立一个列明来源 batch、revision 和获准同族范围的
IMPLEMENT 任务；完成独立复审与完整门禁后，严格执行：译文 commit → 计时 queue rebuild → 单次 catalog
build → migration-chain → 必要 repair evidence commit → 再次计时 queue rebuild。每个来源的 provenance、
逐项验收和 successor 重审不可因集中修复而省略，两次真实 rebuild 也不能省略。

首轮相应修复窗口完成后，宿主向当前主代理报告并暂停，供其收集测量；这是操作暂停点，不是要求用户再次批准。
主代理可在既有连续审核授权范围内根据结果继续安排。报告至少含：

- 每条实际命令、全历史投影和门禁的 wall time；
- 审核完成数、修复完成数及各自提交；
- 未决术语/口径、最老可执行积压和 `8b977dd836…` 的未决状态；
- 失败、重试、恢复动作及最终 queue/checkpoint 状态。

只有审核和修复端到端数据都齐备后才能评估整体收益；单次或仅审核侧变快只作为样本报告。

## 历史待维护者术语／口径

下列历史 pending 与当前可执行修复分列，不计入窗口阈值，也不得在普通修复窗口内擅自裁决或清零：

`Shantiz`、`Continuum Destabilization`、`Feed Strengths`、`Corrupted Negation`、
`archery prowess`、`Pushy elf`、`Hurricane`、`Sapphire`（2 项）、`Dirge Intoner`、
`-Attenuate`、`Summertide`、`the Darkness`、`Arena Master` 头衔、`slimy` 词缀、
`Massive Blow`、`Sudden Growth`、`slime mold`、`Power/Range` 面板、`blood-etched`、
`Intricate Tools`、`Flexible Combat`、`Curse of Shrouds`、`Reabsorb`、`Empty Hand`、
`Epoch's Curve`、`Hide in Plain Sight`、`Artelia Firstborn`。

权威逐条明细仍在维护者的 repair cursor；每个窗口报告它们的状态，但本性能任务不改口径。

## 操作入口与不变量

- 修复窗口和投影复用命令见 [orchestration README](tools/orchestration/README.md#repair-preflight-与-migration-有界串联)。
- 调度、20-revision 阈值及无空窗口规则见 [代理工作流](docs/agent-workflow.md#wp2-lite-三批修复窗口)。
- 仍只允许一个 production writer；活动 checkpoint 内不改译文，不放宽来源、术语、复审、门禁或失败恢复。
- surface 使用 4 lane、并发上限 3；contextual 使用一个 full child，具体模型仍以恢复时的 profile 和契约为准。
- freeze MISS 不能单独证明运行期拼接键或小写实体名 form 7/8 是死键；须按固定源码和实际运行组合核验。
- `alchemist gem` 标签缺口已在 commit `9935df0` 修复：`freeze_workset.py` 的运行期实体名标签集合已包含
  `entity name`、`gem name`、`alchemist gem`，相关调用共用该集合；不得恢复成待授权工具修复。
- 固定版本源码事实优先；DLC 来源未固定时如实记录实际公开源码来源和未固定状态。
- 历史 pending／待维护者术语单列并在每个窗口报告，不擅自修复、清零或计入可执行阈值。
- 2026-09-19 以前的批次细节与事故记录见
  [历史交接存档](docs/handoff-history-through-20260919.md)，只供追溯，不构成当前授权。
