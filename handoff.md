# 翻译审核当前交接

更新时间：2026-09-19

## 当前状态

- **生产审核暂停。** 维护者要求完成审核批 210 后暂停；不得自动恢复或启动后续批次。
- 审核批已完成至 210，修复批已完成至 231；下一步是**修复批 232**，仅在维护者明确恢复后执行。
- 审核与修复保持严格 1:1 交替。恢复时从 `repair_required` 取最旧约 20 条 FIFO；长期待人工裁决项继续跳过。
- batch 210 evidence 的 HEAD 为 `632e1b0b95c3383e62945d4342179a8ef9f4cacf`，已 finalize；当时无活动批次。
- 当时 queue rebuild 后 `repair_required=131`。这是 2026-09-19 的交接快照，不替代恢复前的只读重查。
- 当前会话只授权本地工作，**未授权 push、开 PR 或发布**。

## 恢复后的首批范围

修复批 232 首先处理审核批 210 已确认、无需新增专名策略的项目：

- 刻印 lore 中 `herbal infusions` 的“草药输液”改为“纹身”，纠正修复批 231 的错误，并与既有 `infusion` 译法对齐。
- 盾牌文案 `Block the wielder` 的“玩家”改为“持有者”。
- Weisman 信件：`limb` 改为“四肢”，`At first` 改为“起初”，补足 `ridiculous pomposity`、`false heroics`、`town square` 的语义。

恢复前还须重查 queue、工作树、当前 HEAD 和任务状态；本文件不是恢复授权，也不冻结新的 workset。

## 待维护者裁决

下列专名或全局术语决定不得在普通修复批内自行裁决：

`Shantiz`、`Continuum Destabilization`、`Feed Strengths`、`Corrupted Negation`、
`archery prowess`、`Pushy elf`、`Hurricane`、`Sapphire`（2 项）、`Dirge Intoner`、
`-Attenuate`、`Summertide`、`the Darkness`、`Arena Master` 头衔、`slimy` 词缀、
`Massive Blow`、`Sudden Growth`、`slime mold`、`Power/Range` 面板、`blood-etched`、
`Intricate Tools`、`Flexible Combat`、`Curse of Shrouds`、`Reabsorb`、`Empty Hand`、
`Epoch's Curve`、`Hide in Plain Sight`。

权威逐条明细仍在维护者记忆 `repair-batch-cursor`；这里只保留当前交接所需清单。

## 已知机制与操作事实

- 表层筛查使用 4 lane、并发上限 3；交叉复核使用 1 个 full child。具体 provider/model 选择仍以恢复时可用 profile 和任务契约为准，本文件不改变选择政策。
- 表层派发、finish 通知、收获、归档和恢复使用 [orchestration README](tools/orchestration/README.md) 的当前入口；不得轮询猜测完成状态。
- freeze MISS：真正死键按既有 host-block 流程处理；运行期拼接或小写实体名（form #7/#8）不是死键。batch 208 的 `gem.lua` / `alchemist lapis lazuli` 暴露了 `freeze_workset.py` 只在 `source_tag == 'entity name'` 校验 concat、漏掉 `alchemist gem` 标签的缺口；该工具修复仍待维护者另行授权。
- 固定版本机制事实优先于既有译文、术语库和模型 finding；DLC 来源未固定时必须记录实际公开源码来源与未固定状态。

## 当前入口与历史

- 正式操作和验收：[代理工作流](docs/agent-workflow.md)、[编排说明](tools/orchestration/README.md)。
- 适用契约：[surface screen v1](docs/paseo-translation-surface-screen-v1-contract.md)、[context review v2](docs/paseo-translation-context-review-v2-contract.md)。
- 2026-09-19 以前的完整交接、旧性能任务状态、历史批次表和事故记录已归档到
  [历史交接存档](docs/handoff-history-through-20260919.md)。归档内容仅供追溯，**不构成当前授权**。
