# Grok：Tome4 并行翻译审阅设计方案

状态：设计提案，尚未修改现有 Paseo 契约或门禁。

## 1. 目标与边界

本方案解决 P2 剩余长文本审阅的墙钟时间问题，同时保留当前流程已经证明有价值的约束：

- 固定源码、受跟踪工作集和逐条候选身份；
- EXECUTOR 唯一写入，REVIEWER 独立只读，第二轮后由 SENIOR_REVIEWER 校准范围；
- source、source_tag、参数、标记、占位符和换行不变量；
- confirmed finding 才能进入修复；
- 子 agent 终态核验、归档纪律、五步门禁、完整构建和 `DONE_VERIFIED`；
- 术语库、全局重命名、P3 操作仍由维护者单独授权。

目标是在不降低上述标准的前提下，把稳定批次吞吐提高到当前的 2–3 倍，并显著减少多轮复审重复读取和回显完整长文本的成本。

## 2. 现有流程的主要瓶颈

### 2.1 批次之间完全串行

当前只有一个共享工作树。即使两个批次涉及不同 section，也不能让两个 EXECUTOR 同时写
`mod-tome.lua`。其后 REVIEWER、修复、门禁同样排队，导致大部分可并行工作被串行化。

### 2.2 每个修复周期重新全量复审

b38 的 52 条经历五份有效全量 review；后续轮次往往只剩少量局部 finding，但 reviewer 仍须重新读取并回显全部 52 对。它保证了完整性，却让后期边际成本远高于边际收益。

### 2.3 review 输出重复携带长 source/target

`translation_contextual_v1` 要求每条 evidence 回显完整 source 与 target。长篇 lore 可使单次结果达到十几万字符；传输截断、冻结字节不一致和 session 抽取成本也随之增加。b38 已出现三次无效 review 输出。

### 2.4 门禁重复且无法跨批次摊销

每批都运行 464 项单测和完整 addon 构建是安全的，但多个互不相交的批次串行执行同一套门禁，墙钟时间无法重叠。

### 2.5 `mod-tome.lua` 是单体集成点

普通 Git 分支虽然能隔离写入，但多个分支都修改同一大文件，顺序 cherry-pick 仍可能产生文本冲突。应以 section/调用身份合并 target，而不是依赖行号补丁。

## 3. 总体架构

方案代号为 **Grok**。并行发生在批次之间；同一批次内部仍保持作者、审核者和修复者的顺序隔离。

```text
                         ┌─ Lane A worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW ─┐
WAVE PLANNER → conflict ├─ Lane B worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW ─┼→ merge queue
               graph    └─ Lane C worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW ─┘      │
                                                                                       ▼
                                                        semantic apply → global gates → commit
```

主编排者只维护一个集成工作树。每条 lane 使用 Paseo 管理的独立 worktree、独立 task ID 和独立分支。建议并发上限为三条活跃 lane，使主编排者仍保留一个协调槽位。

同一 lane 内禁止下列重叠：

- EXECUTOR 与 REVIEWER 不得同时运行；
- 候选冻结后，任何写入都会使当前 review 失效；
- 修复必须由 fresh EXECUTOR 完成；
- cycle 2 起的修复仍须先经 SENIOR_REVIEWER。

## 4. 图感知批次规划

新增 wave planner，在派发前为候选 section 建立冲突图。节点是一个有界批次，边表示两个批次不适合同时进入可合并状态。

边至少来自：

1. 相同 section 或相同 `t()` 调用；
2. 相同运行时键及 `source_tag`；
3. 同一高复用术语 claim；
4. 同一连续故事、章节或人物关系闭包；
5. 条件性 collateral 可能触及对方范围；
6. 两个批次都需要修改非 `mod-tome.lua` 的同一文件。

规划器按图着色分配 lane。没有边的批次可以并行；存在边的批次进入不同 wave 或同一 lane 串行。

批次大小不再只按 pair 数决定，而使用加权预算：

```text
weight = source_tokens
       + 0.6 × target_tokens
       + narrative_dependency_penalty
       + shared_key_penalty
```

建议普通 lane 为 20k–35k source tokens。`misc.lua`、`last-hope.lua` 这类大 section 只能按完整故事或标题锚点切分，不得在章节中间切断。

## 5. Lane 生命周期

每条 lane 继续使用现有任务状态机，另增加 wave 层状态：

```text
PLANNED → DISPATCHED → LANES_READY → MERGING → GATED → DONE
                              └──────────────→ WAIT_USER / STOP
```

### 5.1 预处理

主编排者一次性完成整个 wave 的只读工作：

- 固定 base commit；
- 生成各 lane 的 tracked workset；
- 校验词法 `t()` 数、固定源码、`args_order` 和共享键；
- 生成术语快照、故事依赖组和冲突图；
- 建立独立 worktree。

### 5.2 Lane 执行

每条 lane 独立执行：

1. EXECUTOR 全量审核并修改；
2. 宿主机械核验范围与不变量；
3. 冻结候选并运行 preflight；
4. 独立 REVIEWER；
5. host adjudication；
6. 有界 FIX 和复审；
7. lane 完成态检查。

一个 lane 失败或进入 `WAIT_USER` 不应取消其他无冲突 lane。

### 5.3 集成

完成 lane 不直接修改集成分支。它输出语义补丁，由主编排者按队列逐个应用。每次应用后重新检查共享键和候选旧值；不允许自动猜测冲突结果。

## 6. 语义补丁代替行号补丁

新增规范化 `TARGET-PATCH.json`：

```json
{
  "base_commit": "<sha>",
  "task_id": "p2-tome-texts-bNN-001",
  "changes": [
    {
      "section": "mod-tome/data/lore/example.lua",
      "ordinal": 17,
      "source_sha256": "<sha256>",
      "source_tag": "_t",
      "old_target_sha256": "<sha256>",
      "new_target": "译文"
    }
  ]
}
```

集成工具按 `section + ordinal + source_sha256 + source_tag` 解析真实调用，并要求当前 target 与
`old_target_sha256` 一致才写入。这样可以：

- 避免多个 worktree 修改单体 `mod-tome.lua` 时的行号冲突；
- 在上游批次改变相邻文本后仍安全定位；
- 对共享键、重复 source 和相同 section 内的重复调用 fail closed；
- 精确证明最终集成只包含已审核 target。

建议新增命令：

- `python3 -B tools/i18n export-target-patch ...`
- `python3 -B tools/i18n apply-target-patch --strict ...`
- `python3 -B tools/i18n verify-target-patch ...`

## 7. Review 协议优化

### 7.1 第一阶段：无需修改契约

最先落地的版本仍使用 `translation_contextual_v1`。加速完全来自多个独立 worktree 的批次级并行，因此不改变当前 evidence、复审或门禁语义。

### 7.2 第二阶段：`translation_contextual_v2`

在工具和契约测试完备后，reviewer 不再逐条回显完整 source/target，而返回：

```json
{
  "contract": "translation_contextual_v2",
  "candidate_identity": "<sha256>",
  "coverage": {
    "ordered_revision_count": 42,
    "ordered_revision_digest": "<sha256>"
  },
  "findings": [
    {
      "revision_key": "bNN-07-example",
      "observation": "...",
      "source_sha256": "<sha256>",
      "target_sha256": "<sha256>"
    }
  ]
}
```

宿主工具从冻结 envelope 重算 coverage 和每条 evidence hash。输出仍与全部 revision 严格绑定，但只传输 finding，不重复传输几十篇长文。预期可消除大部分截断和 evidence 字节漂移失败。

### 7.3 中间轮使用依赖闭包复审

首轮和最终轮仍为全量复审。中间 FIX 后的 reviewer 只读取：

- 本轮实际变化的 target；
- 尚未关闭的 finding；
- 与变化目标共享运行时键的调用；
- 同一标题、章节、人物关系或术语 claim 的依赖组；
- executor 意外触及的任何额外目标。

该集合称为 review closure，并有独立 identity。若 closure 无法可靠计算，则自动回退全量复审。这样 b38 一类批次可从“五次全量”降为“首轮全量 + 三次闭包 + 最终全量”。

这项优化需要新契约和工具支持，不能在现行 `translation_contextual_v1` 下自行采用。

## 8. 术语与共享键隔离

普通 lane 对术语库只读。任何需要以下操作的 observation 都进入 quarantine：

- 修改 terminology；
- 全局重命名；
- 改动另一个 lane 或范围外 section 的共享键；
- 确立跨批次人物、地点或组织译名。

quarantine 项写入 wave 的 `TERM-CLAIMS.json`，按标准化 source、tag、候选译名和证据去重。它们不会阻塞无关 lane，但在未裁决前不得进入目标集成。真正的术语修改仍由单写入者的独立术语批次完成。

## 9. 门禁策略

### 9.1 可立即实施的保守模式

在不修改 `AGENTS.md` 的情况下，每条 lane 仍完整运行：

1. strict lint；
2. 464 项单测；
3. runtime collision scan；
4. runtime key classification；
5. diff check；
6. `tools/ci-gates.sh`；
7. `DONE_VERIFIED`。

这些门禁可以在不同 worktree 并行运行。集成 wave 后再额外跑一次完整五步和 CI，确认组合结果。

### 9.2 可选的快速模式

若维护者以后明确修改仓库规则，可考虑 lane 内只跑 strict lint、范围验证和 diff check，把完整单测/构建合并到 wave 集成后运行一次。

该模式会改变“每批完整门禁”的现行不变量，未经维护者裁决不得启用。首版 Grok 不依赖这项优化。

## 10. 调度策略

建议最多三个活跃 worker：

- reviewer 优先于新 executor，尽快释放已写入 lane；
- 同一时刻最多两个 EXECUTOR，降低 CPU、磁盘和大模型写入竞争；
- 第三个槽位用于 REVIEWER、SENIOR_REVIEWER 或 SCOUT；
- 完成的 child 经 status、attention、activeTurn 和工作树复核后立即归档；
- progress-only 或无 diff 的 executor 仍按无效 dispatch 处理，fresh retry，不续跑旧 child。

示例流水：

```text
T0  A-exec   B-exec   C-scout
T1  A-review B-exec   C-exec
T2  A-fix    B-review C-exec
T3  A-review B-fix    C-review
T4  merge A  B-review C-fix
```

## 11. 失败关闭与恢复

以下情况只暂停相关 lane：

- 单次 agent 无效输出；
- 候选 contract/evidence 校验失败；
- 有界修复未通过局部 lint；
- 语义补丁旧 target hash 不匹配。

以下情况暂停整个 wave：

- 两条 lane 对同一运行时键给出不同目标；
- 需要术语库或全局重命名裁决；
- 集成后完整门禁失败且一次有界诊断无法归因；
- 同一 revision 出现实质冲突意见；
- child 生命周期或归档状态无法确认；
- 集成补丁触及未授权 section。

任何 lane 都可以从 tracked workset、candidate envelope、semantic patch 和 STATE 重建；不得依赖某个 agent 会话继续存在。

## 12. 产物与审计

建议新增：

```text
.ai/waves/<wave-id>/WAVE.json
.ai/waves/<wave-id>/CONFLICT-GRAPH.json
.ai/waves/<wave-id>/MERGE-QUEUE.json
.ai/task/<task-id>/TARGET-PATCH.json
evidence/quality/p2-waves/<wave-id>-adjudication.json
```

`.ai/` 继续作为可重建的运行态；冻结工作集、人工裁决和最终 wave 结果进入受跟踪 `evidence/`。

wave evidence 至少记录：各 lane base commit、候选 identity、语义补丁 hash、review/fix 周期、decline 理由、合并顺序、共享键差异和最终门禁。

## 13. 分阶段实施

### Phase 0：度量

不改流程，只在接下来两个批次记录各阶段墙钟时间、token、输出字节、无效 dispatch、finding 数和门禁时间，建立基线。

### Phase 1：安全并行 MVP

- 两条独立 worktree lane；
- 保持 `translation_contextual_v1`；
- 每 lane 保持全部现有门禁；
- 主编排者串行 cherry-pick，并在 wave 末重跑完整 CI。

这是唯一无需修改审核 contract 的阶段。

### Phase 2：三 lane 与语义补丁

- 引入 conflict graph 和 `TARGET-PATCH.json`；
- 扩展到三 lane；
- 用语义应用替代直接 cherry-pick `mod-tome.lua`；
- 增加 wave 状态检查和集成 evidence。

### Phase 3：紧凑 review 与闭包复审

- 定义 `translation_contextual_v2`；
- findings-only + coverage digest；
- 首轮/最终轮全量，中间轮依赖闭包；
- 更新契约文档、角色 prompt、checker 和单测后才启用。

### Phase 4：超大 section 分片

只对 `misc.lua`、`last-hope.lua` 等大 section，按故事连通分量建立多个只读 review shard。所有 shard 必须精确分区且最终仍经过一个全量 reviewer。此阶段收益最不确定，不作为 MVP 前置条件。

## 14. 验收指标

前三个 wave 以如下指标判断是否保留方案：

- 墙钟吞吐至少提高 2 倍；
- source/tag/args_order/markup/newline 漂移为 0；
- runtime collision 为 0；
- invalid review 输出率不高于现有基线，Phase 3 后目标低于 2%；
- 中间复审输入/输出 token 降低至少 50%；
- 语义补丁 merge 冲突率低于 10%；
- 随机抽取至少 10% 已合并条目做全量独立复审，不出现确认级漏检；
- 任一 wave 都能从受跟踪 evidence 和忽略态 STATE 重建。

## 15. 推荐决策

建议立即批准 **Phase 0 + Phase 1**：它不放宽现有任何质量规则，只用独立 worktree 把不同批次并行化。

Phase 2 在两 lane 试运行稳定后实施。Phase 3 涉及审核契约语义变化，应作为单独基础设施任务交叉复审。Phase 4 仅在跨批次并行仍不足以处理超大 section 时启用。

不建议一开始就在同一批次内让多个 writer 修改 `mod-tome.lua`，也不建议先取消每批完整门禁；两者风险高于当前真正的首要瓶颈——批次间串行和 review 文本冗余。
