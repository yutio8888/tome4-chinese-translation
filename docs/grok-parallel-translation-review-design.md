# Grok：Tome4 并行翻译审阅设计方案

状态：设计提案。本文本身不修改现行 Paseo 契约、checker 或门禁。并行
lane **不是**无契约／无流程变更的优化：在下文列出的契约与 checker 变更
完成、经独立交叉复审并落地之前，批次保持现行串行。只有 Phase 0 的度量
不依赖这些变更。

## 1. 目标与边界

本方案解决 P2 剩余长文本审阅的墙钟时间问题，同时保留当前流程已经证明有
价值的约束：

- 固定源码、受跟踪工作集和逐条候选身份；
- 同一 workspace 同时只有一个任务内容写入 agent；lane 内 EXECUTOR 唯一写入，
  REVIEWER 独立只读，第二轮后由 SENIOR_REVIEWER 校准范围；
- 一个 wave 只有一个 ORCHESTRATOR，它直接拥有全部 lane 与 integration 的
  child；不存在 lane-orchestrator；
- 集成写入同样遵守该不变量：只有 fresh integration EXECUTOR 可写组合译文；
- source、source_tag、`args_order`、`special`、占位符和换行不变量；
- confirmed finding 才能进入修复；
- 子 agent 终态核验、归档纪律、五步门禁、完整构建和 `DONE_VERIFIED`；
- 首轮与最终轮对**最新完整候选的全部 keys**做全量复审；
- Phase 1 并行 lane 的 collateral 集必须为空，且 SPEC 禁止 collateral 修改；
- 术语库、全局重命名、P3 操作仍由维护者单独授权。

目标是在不降低上述标准的前提下，把稳定批次吞吐提高到当前的 2–4 倍，并
显著减少多轮复审重复读取和回显完整长文本的成本。墙钟加速不得早于契约与
checker 落地。

## 2. 现有流程的主要瓶颈

### 2.1 批次之间完全串行

当前只有一个共享工作树。即使两个批次涉及不同 section，也不能让两个
EXECUTOR 同时写 `mod-tome.lua`。其后 REVIEWER、修复、门禁同样排队，导致
大部分可并行工作被串行化。

### 2.2 每个修复周期重新全量复审

b38 的 52 条经历五份有效全量 review；后续轮次往往只剩少量局部 finding，但
reviewer 仍须重新读取并回显全部 52 对。它保证了完整性，却让后期边际成本
远高于边际收益。

### 2.3 review 输出重复携带长 source/target

`translation_contextual_v1` 要求每条 evidence 回显完整 source 与 target。
长篇 lore 可使单次结果达到十几万字符；传输截断、冻结字节不一致和 session
抽取成本也随之增加。b38 已出现三次无效 review 输出。

### 2.4 门禁重复且无法跨批次摊销

每批都运行 464 项单测和完整 addon 构建是安全的，但多个互不相交的批次串行
执行同一套门禁，墙钟时间无法重叠。

### 2.5 `mod-tome.lua` 是单体集成点

普通 Git 分支虽然能隔离写入，但多个分支都修改同一大文件。集成不得依赖行号
补丁，也不得由 ORCHESTRATOR cherry-pick 或手写合并 target。必须以调用身份
合并已审核 target，并由 integration EXECUTOR 在严格 SPEC 下写入。

## 3. 总体架构

方案代号为 **Grok**。并行发生在批次之间、且仅发生在互不相交的 lane
workspace 之间。同一 lane 内部仍保持作者、审核者和修复者的顺序隔离。
组合结果不在 lane DONE 时进入集成分支。

```text
WAVE PLANNER → 最小 conflict preflight（不确定则串行或 WAIT_USER）
  ├─ Lane A workspace/worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW → lane DONE
  ├─ Lane B workspace/worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW → lane DONE
  ├─ Lane C workspace/worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW → lane DONE
  └─ Lane D workspace/worktree ─ EXECUTOR → REVIEWER → FIX/REVIEW → lane DONE
                                      │
                                      ▼ 全部参与 lane 均 DONE
                    受管 integration task（fresh EXECUTOR 为唯一集成写入者）
                                      │
                                      ▼
     冻结组合候选与 translation-only diff → 独立最终全量复审（全部 keys）
     → 门禁 → 构造 prospective DONE WAVE（临时冻结，不发布）
     → integration EXECUTOR 写 wave evidence（绑定 prospective identity）
     → 原子发布相同字节为权威 WAVE.json → 最终 allowed-files／diff／
       evidence closure → 外部 DONE_VERIFIED
```

- 每条 lane 使用 Paseo 管理的独立 worktree、独立 workspace、独立 task ID
  和独立分支，以满足「同一 workspace 同时只有一个任务内容写入 agent」。
- 唯一跨 workspace 拓扑见第 5.1 节：一个 wave ORCHESTRATOR 直接创建并拥有
  全部 lane／integration child；契约扩展允许 `child_dispatch.workspace_id`
  与 root workspace 不同。禁止再引入任何 lane-orchestrator。
- Phase 1 的并行度可配置为 2–4 条活跃 lane，默认 2、硬上限 4。
  在契约允许跨 workspace 的受管 wave、且 Phase 1 最小 WAVE／MERGE-QUEUE
  schema 与 checker 落地之前，不得派发并行 lane。
- Wave ORCHESTRATOR 只提供／裁决受控输入并做核验：维护 `.ai/waves/` 编排
  记录、排队、核验和门禁。它不写任务内容文件，不维护一份可手写的「集成
  工作树内容」。译文 Lua 与受跟踪 wave evidence 只由 lineage 核验的
  integration EXECUTOR 写入。必要时同一 integration task 内可派发
  fresh evidence-only EXECUTOR：这是语义写入子集（prompt／dispatch 只
  允许唯一 wave evidence 路径），**不是**第二份机器可读 `allowed_files`。
  唯一授权面仍是 integration `task-content-allowed-files/1` 的
  `translation_fix_paths ∪ {wave_evidence_path}`。终结协议见第 5.6 节：
  先冻结 prospective DONE WAVE，再写 evidence，再原子发布相同字节，
  最后跑 closure；`DONE_VERIFIED` 是外部 checker 终态，不写入被哈希
  WAVE。

同一 lane 内禁止下列重叠：

- EXECUTOR 与 REVIEWER 不得同时运行；
- 候选冻结后，任何写入都会使当前 review 失效；
- 修复必须由 fresh EXECUTOR 完成；
- cycle 2 起的修复仍须先经 SENIOR_REVIEWER；
- 已结束 child 不得 follow-up 续跑；无效输出先归档再 fresh retry。

Wave 内禁止下列行为：

- ORCHESTRATOR cherry-pick、应用 TARGET-PATCH、编辑译文 Lua 或手工拼接
  target；
- 在任一参与 lane 未 DONE 时开始集成写入；
- 用 lane 级 DONE 代替 wave／integration 的冻结、最终复审、门禁与外部
  `DONE_VERIFIED`；
- 把 closure identity 或 lane 最终 identity 当作组合候选的 full identity；
- 在 integration 最终复审仍有 accepted／deferred finding 时跑门禁或宣布
  wave DONE；
- 重渲染或改字段后再把 prospective DONE WAVE 发布为权威 `WAVE.json`；
- 把 `DONE_VERIFIED` 写入被哈希的 WAVE 字节。

## 4. 图感知批次规划与最小 conflict preflight

新增 wave planner。**最小 conflict preflight 是 Phase 1 的前置条件**，不是
Phase 2 才引入的优化。未通过 preflight 的候选对不得进入同一 wave 的并行
DISPATCHED。

### 4.1 冻结集合

派发任何并行 lane 之前，必须冻结并交叉比较下列集合；任一项无法确定即不得
并行，改为串行或 `WAIT_USER`：

1. **调用集合**：每个拟派发批次中全部词法 `t()` 的
   `(section, source, source_tag, args_order, special)`，以及对应
   `revision_key`；
2. **运行时键／tag**：`(runtime_key, source_tag)`；
3. **术语与叙事依赖**：工作集内高复用术语 claim，以及同一连续故事、章节
   或人物关系闭包；
4. **collateral**：由第 5.6 节算法从该 lane 机器可读 task-content
   `allowed_files` **独立推导**，不得由 `collateral-authorization/1`
   自己声明 primary／ordinary 后自证。Phase 1 将
   `ordinary_non_collateral_paths` **规范固定为** `[]`，不得由规划者
   任意声明。`primary_content_paths` 必须绑定 WAVE 外部冻结、checker
   可独立读取的 `lane-workset/1`（`WAVE.lanes[].workset_path`／
   `workset_identity`，DISPATCHED 前冻结）。checker 从该冻结 workset
   的调用定位实际译文文件并独立导出 primary paths，要求它与 lane
   `task-content-allowed-files/1`.`translation_fix_paths` 以及
   `collateral-authorization/1`.`primary_content_paths` **精确相等**。
   然后 `collateral_paths = sort(allowed_files − primary − [])`。
   Phase 1 并行要求重算结果为**空数组**，且每条并行 lane 的 SPEC 必须
   明文禁止 collateral 修改。任一拟派发批次重算非空、ordinary 不是
   `[]`、primary 与独立导出不等、或 SPEC 仍授权非主译文路径时，该批次
   不得进入同一 wave 的并行 DISPATCHED，改为串行或 `WAIT_USER`。
   checker **不得**因声明 `[]` 而跳过加载 workset／授权字节。第 5.6 节
   唯一 wave evidence 路径不是 4.1 collateral：它不得出现在任何 lane
   SPEC、lane `allowed_files` 或 `collateral_paths` 中，只作为
   integration 任务内容写入。

三类集合（调用、运行时键／tag、术语与叙事依赖）、`lane-workset/1`
与 collateral 授权／推导 artifact 都必须有第 5.6 节的 exact-key
canonical artifact；CONFLICT-PREFLIGHT 根对象另有外部绑定的
`conflict_preflight_identity`。checker 从绑定字节重算 identity、相交、
primary 导出与 PASS，不得只信声明布尔值或空数组。

两边集合相交、锚点歧义、工作集条数与词法 `t()` 数不一致、collateral 不
为空、SPEC 未禁止 collateral，或上述任一集合不能从受跟踪工作集确定性算
出时，fail closed：不并行，或进入 `WAIT_USER`。禁止把「看起来像不同
section」当作不相交。

`TARGET-PATCH` 只编码 `t()` 的 target 字节。Phase 2 以后若要支持
collateral，必须另定义独立补丁契约（例如 `collateral-patch/1`），覆盖非
`t()` 路径的有界 hunk；不得借用 `TARGET-PATCH` 的 schema、身份配方或
apply／verify。在该独立契约落地前，并行 wave 继续要求 collateral 为空。

### 4.2 冲突图（Phase 2 的可选调度扩展）

Phase 1 交付最小 WAVE／MERGE-QUEUE／CONFLICT-PREFLIGHT（含根 identity
与 `collateral-authorization/1`）／`lane-workset/1`／
`task-content-allowed-files/1`／`integration-content-diff/1`／
wave-evidence schema 与 checker，并执行 4.1 的可重算相交检测；同一
checker 在 Phase 1 即允许 2–4 条 lane。Phase 2 **不**新写一套 checker，
只可选增加 `CONFLICT-GRAPH.json` 的 exact-key 字段、图着色和调度检查。

Phase 2 冲突图：节点是有界批次，边表示两个批次不适合同时进入可合并状态。
边至少来自 4.1 的四类集合，以及「相同 section 或相同 `t()` 调用」。规划器
按图着色分配 lane。没有边的批次可以并行；存在边的批次进入不同 wave 或同
一 lane 串行。

### 4.3 加权批次大小

批次大小不再只按 pair 数决定，而使用加权预算：

```text
weight = source_tokens
       + 0.6 × target_tokens
       + narrative_dependency_penalty
       + shared_key_penalty
```

建议普通 lane 为 20k–35k source tokens。`misc.lua`、`last-hope.lua` 这类
大 section 只能按完整故事或标题锚点切分，不得在章节中间切断。

## 5. Lane 与 wave 生命周期

每条 lane 继续使用现有任务状态机。wave 层状态为：

```text
PLANNED → PREFLIGHT → DISPATCHED → LANES_READY → INTEGRATING
        → FINAL_REVIEW → GATED → DONE
                              └──────────────→ WAIT_USER / STOP
```

`state` 只允许上述十个字面量。未完成 PREFLIGHT 不得进入 DISPATCHED。
LANES_READY 表示全部参与 lane 已 `DONE_VERIFIED`。lane DONE 不是 wave
DONE。WAVE.`state="DONE"` 表示权威 WAVE 已发布且 wave evidence 已存在，
但尚可能未通过外部 `DONE_VERIFIED`；`DONE_VERIFIED` 不写入 WAVE。

### 5.1 唯一跨 workspace 拓扑

Phase 1 并行采用且只采用下列拓扑。任何「每条 lane 一个 orchestrator」或
未命名的中间编排根都是契约错误，必须 `WAIT_USER`，不得派发。

1. **一个 wave ORCHESTRATOR 直接拥有全部 child。** 全部 lane EXECUTOR／
   REVIEWER／SENIOR_REVIEWER／SCOUT，以及 integration 的同类 child，都由
   该 ORCHESTRATOR 通过 agent-scoped 创建接口直接创建。parent lineage
   必须精确等于 `WAVE.json` 的 `orchestrator_agent_id`。
2. **契约扩展：`child_dispatch.workspace_id` 可以与 root 不同。** 现行
   「child 属于当前 workspace」检查改为：child 属于其
   `child_dispatch.workspace_id`，该值必须等于所属 **task**
   `STATE.workspace_id`；允许该值与 `WAVE.json.root_workspace_id` 不同。
   每条 `child_dispatches[]` 记录必须带非空 `workspace_id`。
3. **每个 lane／integration STATE 的 `orchestrator_agent_id` 都是同一个
   wave ORCHESTRATOR。** 该字段在任务内仍不得改变。禁止在 lane workspace
   内创建 role=`orchestrator` 的 child，禁止把某个 lane EXECUTOR 或未记录
   的会话当作该 lane 的编排根。
4. **`STATE.child_dispatches` 只记录该 task 的直接 children。** lane A
   的 STATE 不得收录 lane B 或 integration 的 dispatch；cross-task 绑定
   只存在于 `WAVE.json`。
5. **wave 状态汇总绑定。** `WAVE.json` 是唯一跨 workspace 的权威索引，
   见第 5.6 节。

Lineage／recovery／archive 校验（fail closed）：

- **创建后：** agent 的 workspace 等于所属 task 的 `workspace_id`；
  `labels.task_id`／`labels.role`／所需 `labels.purpose` 精确匹配；
  parent 精确等于 wave `orchestrator_agent_id`；REVIEWER／SENIOR_REVIEWER／
  SCOUT 未造成该 workspace 工作树变化。
- **恢复查询：** 先按**该 child 所属 task** 的 `workspace_id`／cwd 限定，
  再按 task_id、role、purpose、parent lineage（语境再加 candidate／
  dispatch）过滤，最后才做 0／1／多匹配判定。不得按 `root_workspace_id`
  去列举其他 lane 的 child，也不得把 root 下列出的唯一 agent 当作某条
  lane 的匹配。列表截断或身份无法确认时 `WAIT_USER`。
- **归档：** 仍由同一 wave ORCHESTRATOR 对每个 child 即时归档；确认前
  不得 phase transition 或创建 successor。归档查询同样按该 child 的
  `workspace_id` 限定。
- **交叉约束：** 任一 `agent_id` 不得出现在两个 task 的
  `child_dispatches` 中；任一 lane `workspace_id` 必须两两不同，且不得
  等于 `root_workspace_id`。`integration.workspace_id` 可以等于
  `root_workspace_id`。DISPATCHED 期间不得存在 integration EXECUTOR；
  INTEGRATING 起全部 lane 的写入 child 必须已确认归档。

### 5.2 预处理

wave ORCHESTRATOR 一次性完成整个 wave 的只读工作：

- 固定唯一 `base_commit`（40-lowercase-hex），写入 WAVE／MERGE-QUEUE／
  各 lane STATE 基线与日后 TARGET-PATCH；
- 生成各 lane 的 exact-key `lane-workset/1`（编排记录，不是任务内容），
  写入 `WAVE.lanes[].workset_path`；
- 校验词法 `t()` 数、固定源码、`args_order` 和共享键；
- 生成术语快照、故事依赖组和 4.1 冻结集合的 exact-key canonical
  artifact（写入 CONFLICT-PREFLIGHT，属编排记录，不是任务内容），并从
  冻结 workset 独立导出的 primary paths 与各 lane 已冻结的机器可读
  SPEC／SCOPE／allowed-files 字节推导 `collateral-authorization/1`（
  ordinary 固定为 `[]`，不得手填 primary 后自证）；
- 运行最小 conflict preflight；并行还要求每条 lane 的 collateral 重算
  为空且 SPEC 禁止 collateral；checker 稍后从 WAVE 绑定的 preflight
  路径／identity、lane workset 与授权字节重算，不把此时的 PASS 声明或
  空数组当作终局；
- 仅在 preflight 通过后建立独立 worktree／workspace，并写入第 5.6 节的
  冻结 WAVE／MERGE-QUEUE／CONFLICT-PREFLIGHT／各 lane-workset 编排记录。
  DISPATCHED 前 WAVE 必须保存 `conflict_preflight_path` 与
  `conflict_preflight_identity`（根对象 canonical JSON 的 SHA-256），
  以及每条 lane 的 `workset_path` 与 `workset_identity`；从 DISPATCHED
  起上述字段冻结。ORCHESTRATOR 不写受跟踪 wave evidence。

### 5.3 Lane 执行

每条 lane 独立执行完整现行流程：

1. EXECUTOR 全量审核并修改；
2. 宿主机械核验范围与不变量；
3. 冻结候选并运行 preflight；
4. 独立 REVIEWER（首轮全量）；
5. host adjudication；
6. 有界 FIX 和复审（cycle 2 起先经 SENIOR_REVIEWER）；中间轮可用 v1 dependency closure，
   不确定时回退 full，最终轮全量；
7. 五步门禁与适用完整门禁；
8. 从**最终**候选派生 TARGET-PATCH，且 `base_commit` 等于 wave 冻结
   base；
9. lane 完成态检查（`DONE_VERIFIED`）。

一个 lane 失败或进入 `WAIT_USER` 不应取消其他无冲突 lane，但该 lane 的
TARGET-PATCH 不得进入集成。wave 计划因此不完整时，集成不得自行缩小或改写
范围，必须 `WAIT_USER`。

### 5.4 集成写入

完成 lane 不直接修改集成分支。每条 DONE lane 输出由其最终审核 envelope
派生的 TARGET-PATCH。之后建立一个**受管 integration task**：

- 新的 task ID、SPEC、PLAN、SCOPE、STATE；
- `change_class` 按实际写入内容声明；首次引入 wave／integration 机制本身
  属于 `infrastructure`／`translation_workflow`，落地后的常规组合写入按
  译文任务处理，但不得跳过独立最终复审与 DONE closure；
- **统一的任务内容授权面**是一份机器可读的
  `task-content-allowed-files/1`（默认路径为 integration `SCOPE.json`，
  由 WAVE.`integration.allowed_files_path`／
  `allowed_files_identity` 绑定）。其 `allowed_files` 必须等于下列
  二者的并集，禁止除此之外的扩展，也禁止为 evidence-only dispatch
  另建第二份授权面：(i) 参与且已 DONE 的各 lane 冻结 `lane-workset/1`
  独立导出 primary 之并集（`translation_fix_paths`）；(ii) 第 5.6 节
  唯一精确 wave evidence 路径。allowed-files checker 与最终
  base→工作树 diff closure **只认**该 `allowed_files` 全量。
- `translation_fix_paths` 可继续称为 semantic／translation scope 或
  union SCOPE，但**只是内容修复子集**，不得被 allowed-files checker
  误作全部授权。FIX 范围精确等于该子集。该 wave evidence 路径必须
  明文写入 integration SPEC 与上述授权面，类型为 wave integration
  evidence，不得标为 lane collateral，也不得进入任何 lane 的
  `allowed_files` 或 `collateral_paths`。wave evidence 不是 FIX
  范围，只在最终复审与门禁通过后、按第 5.6 节终结协议由 EXECUTOR
  写入；
- `STATE.orchestrator_agent_id` 等于 wave ORCHESTRATOR；
- **唯一写入者**是该 task 的 fresh、lineage 核验 EXECUTOR（含日后
  FIX EXECUTOR，以及必要时同一 task 内只写 evidence 的 fresh
  EXECUTOR）；ORCHESTRATOR 不写任务内容文件。evidence-only 是同一
  integration task 内 fresh dispatch 的**语义写入子集**，不是新的
  机器授权面：不得再定义第二份 `allowed_files`。其 prompt／dispatch
  只允许唯一 wave evidence 路径；机器授权仍是本 task 已冻结的唯一
  并集。安全性由已冻结 `integration-content-diff/1` identity 保证：
  evidence dispatch 前后，checker 要求所有 `translation_fix_paths`
  内容哈希与该 frozen artifact 完全一致，任何翻译变化 fail closed；
- 首次 apply 前必须同时满足第 5.6 节 commit／tree 谓词：`HEAD` 的
  **commit OID** 精确等于冻结 `base_commit`；index 树与 tracked worktree
  内容树均精确等于 `base_commit^{tree}`。任务内容（译文、受跟踪
  `evidence/`、术语库、以及 SPEC 允许的其他受跟踪路径）若 dirty 或
  untracked，必须拒绝。只允许下列 **ignored runtime artifacts** 以
  ignored／untracked 形式存在，且不得把它们当作 tree 相等的证据：
  `.ai/waves/`、`.ai/task/`、`.ai/reviews/`、`.artifacts/`。禁止再把
  「HEAD／tree 等于 `base_commit`」写成 tree OID 等于 commit OID；
- EXECUTOR 按冻结队列顺序 `apply-target-patch --strict`；冲突、重复、
  重叠、额外修改、未完成 lane、`base_commit` 不一致、`old_target` 与
  `base_commit^{tree}` 重算值不一致一律 fail closed，不得猜测；
- 同一 lineage 核验的 integration EXECUTOR 在 integration task 内写入
  唯一 wave evidence 文件（exact-key schema 见 5.6）；ORCHESTRATOR 只
  提供／裁决受控输入并核验该文件，不创建、不编辑、不覆盖它；
- 写入顺序遵守第 5.6 节唯一终结协议：prospective DONE WAVE → evidence
  → 原子发布权威 WAVE → 最终 closure。最终 allowed-files checker 仍
  核验 `base_commit`→最终工作树全部任务内容 diff 属于唯一并集。外部
  结果为 `DONE_VERIFIED`，不写入 WAVE 字节；
- ORCHESTRATOR 只排队、核验 export／apply 结果、冻结组合候选与
  translation-only diff artifact、派发独立最终复审、在无 open
  finding 后跑门禁、构造／原子发布 WAVE 并核验 evidence 绑定与
  closure；不 cherry-pick，不应用 target，不编辑译文，不写 wave
  evidence。

全部参与 lane 均 DONE 后才进入 INTEGRATING。禁止在仍有未完成 lane 时把已
完成 lane 增量合入集成工作树。lane TARGET-PATCH 只是 apply 的输入，不是
组合候选的权威身份。

### 5.5 集成最终复审与 accepted finding 收敛

Apply 成功后，integration EXECUTOR 的工作树是组合译文的当前内容。随后：

1. 冻结 **integration 自己的** 最新完整候选，并同时冻结第 5.6 节
   `integration-content-diff/1`（translation-only；preimage 不含 wave
   evidence）。组合 envelope 是一份新冻结的完整 payload：按
   MERGE-QUEUE 顺序并入各 lane 最终 snapshot／context，并按
   integration 工作树的实际 target 重渲染术语子集与 briefing，再按
   当时生效的 full 配方哈希。它不是各 lane identity 的拼接，也不得用某
   条 lane 的 identity、lane TARGET-PATCH identity 或任何 closure
   identity 代替。
2. 独立最终复审覆盖该组合候选的**全部 keys**，绑定该 identity，
   `review_kind=full`。
3. **无** accepted／deferred finding 时，才跑完整五步门禁与适用 CI。
4. 若最终复审产生 accepted finding，不得跳过修复、不得改写 lane patch、
   不得由 ORCHESTRATOR 手改译文。收敛路径只允许：

   - 宿主按现行规则裁决；只有 confirmed 进入修复；
   - 归档当前 reviewer 后，派发 **fresh integration FIX EXECUTOR**；
   - 修复范围精确等于 `translation_fix_paths`（内容修复子集／union
     SCOPE）；超出该子集、需要改术语库／全局重命名、或暴露跨 lane
     共享键冲突时，停止并 `WAIT_USER`，不得猜合并。FIX EXECUTOR 不得
     写入 wave evidence；wave evidence 仍只在门禁通过后的收束写入；
   - FIX EXECUTOR 在 integration 工作树产出 **integration 自己的权威
     translation-only diff／provenance**（`integration-content-diff/1`
     + 新冻结 full envelope）。此后组合候选以 integration task 的最新
     候选为权威；既有 lane patch 仍只是历史输入，不再 re-export 为
     组合身份；
   - 每次修复后重冻最新候选 identity **与** translation-only
     `integration-content-diff/1`；中间轮按 schema 4 v1 closure 规则复审确定性子集，不确定时
     回退 full，收敛后再对**全部 keys** 做一次 `FINAL_REVIEW/full`；
   - `cycle >= 2` 的普通 review finding 必须先经 SENIOR_REVIEWER；
   - integration 使用自己的 `cycle`／`max_cycles`（schema 4 translation implement 默认 3），与各 lane
     的计数独立；达到上限仍未清空 finding 则 `WAIT_USER`。

5. 门禁通过后按第 5.6 节**唯一无循环终结协议**收束：构造 prospective
   DONE WAVE 并计算其 identity → lineage 核验的 integration EXECUTOR
   写 wave evidence（绑定该 prospective identity）→ 将完全相同的
   prospective 字节原子发布为权威 `WAVE.json` → 重跑最终
   allowed-files／diff／evidence closure 与各 lane／integration
   checker。外部结果为 `DONE_VERIFIED`；该终态不写入被哈希 WAVE，也
   不得修改 WAVE 字节。integration task 与 wave 均须满足第 5.6 节的
   wave DONE predicate；checker 必须区分 lane identity／record 与
   wave／integration identity／record。禁止「先写 evidence 再生成
   final WAVE」，也禁止「先发布 DONE WAVE 再写 evidence」。

在上述契约与 checker 变更完成前，不得派发并行 lane，批次保持串行。

### 5.6 WAVE.json、MERGE-QUEUE.json 与机械闭合

Phase 1 即交付下列最小 exact-key schema 与 checker。身份字段不得写入被
哈希的根对象：`wave_record_identity`、`merge_queue_identity`、
`conflict_preflight_identity`、`workset_identity`、
`allowed_files_identity`、`content_diff_identity` 均不得出现在各自被
哈希对象内部。`wave_record_identity`／`merge_queue_identity` 只写入
唯一 wave evidence 文件；`conflict_preflight_identity`、
`workset_identity` 与 `content_diff_identity` 由 WAVE 外部绑定（后二者
中 content-diff 另由 wave-evidence 交叉绑定）。`DONE_VERIFIED` 不写入
被哈希 WAVE。规范化字节
配方与第 6.2 节相同：UTF-8 JSON，object key 递归按字节序排序，array
保持冻结顺序，分隔符精确为逗号和冒号，无多余空白、无换行，
`ensure_ascii=false`；缺键、额外键、错误容器使序列化失败。非 JSON
绑定文件（lane／integration `SPEC.md`）的 identity 为原始 UTF-8 字节
的 SHA-256。

编排记录路径（ignored runtime，由 ORCHESTRATOR 维护，不是任务内容）：

```text
.ai/waves/<wave-id>/WAVE.json
.ai/waves/<wave-id>/WAVE.DONE.prospective.json
.ai/waves/<wave-id>/MERGE-QUEUE.json
.ai/waves/<wave-id>/CONFLICT-PREFLIGHT.json
.ai/waves/<wave-id>/LANE-<lane-id>-WORKSET.json
```

`WAVE.DONE.prospective.json` 是终结协议的临时冻结路径，**不是**权威
`WAVE.json`。`LANE-<lane-id>-WORKSET.json` 的 `<lane-id>` 必须与对应
`WAVE.lanes[].lane_id` 字节相等。

integration 编排／核验产物（ignored runtime；由 lineage 核验的
integration EXECUTOR 或工具写出，不是 ORCHESTRATOR 手写任务内容）：

```text
.ai/task/<integration-task-id>/SCOPE.json
.ai/task/<integration-task-id>/INTEGRATION-CONTENT-DIFF.json
```

`SCOPE.json` 在 Grok wave 的 integration／lane 任务中必须是
`task-content-allowed-files/1`。`INTEGRATION-CONTENT-DIFF.json` 只存在
于 integration task。

唯一受跟踪 wave evidence 路径（普通路径；由 lineage 核验的 integration
EXECUTOR 在 integration task 内写入；ORCHESTRATOR 不写此文件）：

```text
evidence/quality/p2-waves/<wave-id>-adjudication.json
```

`<wave-id>` 必须与 `WAVE.wave_id` 字节相等。该路径必须写入
`WAVE.wave_evidence_path`，必须明文列入 integration SPEC 与
`task-content-allowed-files/1`.`allowed_files`（类型为 wave
integration evidence，不是 lane collateral），且不得列入任何 lane
SPEC 或 lane `allowed_files`。

#### WAVE.json

`schema_id` 必须精确为 `wave/1`，`schema_version` 必须为整数 `1`。根对象
恰好包含下列 14 个键，不得有额外键：

```json
{
  "schema_id": "wave/1",
  "schema_version": 1,
  "wave_id": "p2-wave-001",
  "state": "PREFLIGHT",
  "base_commit": "<40-lowercase-hex>",
  "orchestrator_agent_id": "<wave-orchestrator-agent-id>",
  "root_workspace_id": "<workspace-id>",
  "ordered_lane_ids": ["A", "B"],
  "lanes": [
    {
      "lane_id": "A",
      "task_id": "p2-tome-texts-bNN-001",
      "workspace_id": "<lane-workspace-id>",
      "state_path": ".ai/task/<task-id>/STATE.json",
      "spec_path": ".ai/task/<task-id>/SPEC.md",
      "workset_path": ".ai/waves/<wave-id>/LANE-A-WORKSET.json",
      "workset_identity": null,
      "collateral_empty": true,
      "final_candidate_identity": null,
      "final_review_kind": null,
      "final_review_dispatch_id": null,
      "final_review_record": null,
      "target_patch_path": ".ai/task/<task-id>/TARGET-PATCH.json",
      "target_patch_identity": null
    }
  ],
  "integration": {
    "task_id": null,
    "workspace_id": null,
    "state_path": null,
    "spec_path": null,
    "allowed_files_path": null,
    "allowed_files_identity": null,
    "combined_candidate_identity": null,
    "content_diff_path": null,
    "content_diff_identity": null,
    "final_review_kind": null,
    "final_review_dispatch_id": null,
    "final_review_record": null
  },
  "merge_queue_path": ".ai/waves/<wave-id>/MERGE-QUEUE.json",
  "conflict_preflight_path": ".ai/waves/<wave-id>/CONFLICT-PREFLIGHT.json",
  "conflict_preflight_identity": null,
  "wave_evidence_path": "evidence/quality/p2-waves/<wave-id>-adjudication.json"
}
```

`lanes[]` 每项恰好包含示例中的 14 个键；`integration` 恰好包含示例中的
12 个键。被哈希 WAVE **不得**包含 `done_verified` 键。`ordered_lane_ids`
与 `lanes[].lane_id` 集合和顺序 1:1。Phase 1 并行 `ordered_lane_ids`
长度必须在 2–4 之间，默认生成 2 条，少于 2 或多于 4 均 fail closed。
`wave_evidence_path` 必须精确
等于 `evidence/quality/p2-waves/<wave-id>-adjudication.json`，其中
`<wave-id>` 与根上 `wave_id` 字节相等。`conflict_preflight_path` 必须
精确等于 `.ai/waves/<wave-id>/CONFLICT-PREFLIGHT.json`。每条 lane 的
`workset_path` 必须精确等于
`.ai/waves/<wave-id>/LANE-<lane-id>-WORKSET.json`，其中 `<lane-id>` 与
该项 `lane_id` 字节相等。`collateral_empty` 必须为 JSON `true` 才可
DISPATCHED；checker 不得只信该布尔值，必须从 WAVE 绑定的
`lane-workset/1` 独立导出 primary，再按第 5.6 节算法重算每个
`collateral_paths` 为空。`base_commit` 匹配 `^[0-9a-f]{40}$`。身份类
字段在尚未绑定时必须为 JSON `null`，一旦绑定必须匹配
`^[0-9a-f]{64}$`（dispatch_id 除外，它遵守语境 dispatch 规范）。
`final_review_kind` 一旦绑定必须为 `"full"`，不得为 `"closure"`。
Phase 1 即使仍使用 v1 七键 envelope，WAVE 绑定也写 `"full"`，表示该
记录覆盖最新完整候选的全部 keys；它不是 v1 payload 的键。lane／
integration 任务的 `DONE_VERIFIED` 由 checker 对绑定 STATE 实跑
`ai_state_check.py` 得出；wave 级 `DONE_VERIFIED` 是外部终态，二者
均不写入被哈希 WAVE。

DISPATCHED **之前** WAVE 必须写入 `conflict_preflight_path` 与
`conflict_preflight_identity`，以及每条 lane 的 `workset_path` 与
`workset_identity`。`conflict_preflight_identity` 必须等于对
CONFLICT-PREFLIGHT 根对象按 6.2 配方序列化后的 SHA-256；该 identity
**不**写入 preflight 根对象。`workset_identity` 必须等于对对应
`lane-workset/1` 根对象按 6.2 配方序列化后的 SHA-256；该 identity
**不**写入 workset 根对象。从 DISPATCHED 起下列字段冻结、不得改写：
`wave_id`、`base_commit`、`orchestrator_agent_id`、
`root_workspace_id`、`ordered_lane_ids`、`merge_queue_path`、
`conflict_preflight_path`、`conflict_preflight_identity`、
`wave_evidence_path`、各 lane 的 `task_id`／`workspace_id`／path／
`workset_path`／`workset_identity`／`collateral_empty`。只允许按下面
的状态表填充身份、review 绑定、integration 授权面／content-diff 绑定。
`allowed_files_path`／`allowed_files_identity` 在 INTEGRATING 起一旦
绑定即冻结；`content_diff_path`／`content_diff_identity` 在
FINAL_REVIEW 起一旦绑定即冻结（每次 FIX 后重冻，再进入下一轮复审）。

`wave_record_identity = SHA-256(canonical prospective DONE WAVE bytes)`，
其中 WAVE.`state` 必须精确为 `"DONE"`，且根对象不含 `done_verified`。
该值只写入唯一 wave evidence 文件，不回写进 WAVE.json。权威
`WAVE.json` 必须是与 prospective 完全相同的字节，不得重渲染或改字段。
WAVE 自己的 identity 不得进入被哈希的 WAVE 根对象。禁止把
`state="GATED"`（或更早）的 WAVE canonical 字节当作最终
`wave_record_identity`。

#### MERGE-QUEUE.json

`schema_id` 必须精确为 `merge-queue/1`，`schema_version` 必须为整数 `1`。
根对象恰好包含下列 6 个键，不得有额外键：

```json
{
  "schema_id": "merge-queue/1",
  "schema_version": 1,
  "wave_id": "p2-wave-001",
  "base_commit": "<40-lowercase-hex>",
  "ordered_lane_ids": ["A", "B"],
  "items": [
    {
      "lane_id": "A",
      "task_id": "p2-tome-texts-bNN-001",
      "target_patch_path": ".ai/task/<task-id>/TARGET-PATCH.json",
      "target_patch_identity": null,
      "candidate_identity": null
    }
  ]
}
```

`items[]` 每项恰好包含这 5 个键。`items` 的长度、顺序、`lane_id`、
`task_id` 必须与 WAVE.`ordered_lane_ids`／`lanes[]` 一致。
`base_commit`／`wave_id` 必须与 WAVE 字节相等。DISPATCHED 之后
`wave_id`、`base_commit`、`ordered_lane_ids`、各 `task_id`／
`target_patch_path` 冻结。LANES_READY 起 `target_patch_identity` 与
`candidate_identity` 必须为 64-lowercase-hex。
`merge_queue_identity = SHA-256(canonical MERGE-QUEUE.json bytes)`，由
integration EXECUTOR 写入唯一 wave evidence 文件，不回写进队列根对象。

#### CONFLICT-PREFLIGHT.json（Phase 1 最小，可重算）

`schema_id` 必须精确为 `conflict-preflight/1`，`schema_version` 必须为
整数 `1`。根对象恰好包含下列 8 个键，**不得**包含自身 identity。
`conflict_preflight_identity = SHA-256(canonical 本根对象 bytes)`，由
WAVE 与 wave-evidence 外部绑定。checker 以 WAVE 为唯一入口，读取
`conflict_preflight_path`，用 6.2 配方对当前字节重算 identity，必须与
WAVE 冻结的 `conflict_preflight_identity` 以及 wave-evidence 中的同名
字段字节相等；不得只验证文件内部自洽。还必须从 WAVE 绑定的
`lane-workset/1` 独立导出 primary，并从绑定字节重算各 lane 集合
hash、pairwise intersections、`ordinary=[]` 的 collateral 推导与
PASS，不得只信 `pairwise_intersections_empty`、`result` 或空
`collateral_paths`。

三类冻结集合各有唯一 exact-key canonical artifact，**嵌入**对应
`sets[]` 项（不另建路径）。identity 是该嵌入对象 canonical JSON 的
SHA-256，配方同 6.2。`items` 必须按下面给出的排序键字节序唯一排序；
无法唯一排序或出现重复项则不得生成 preflight，fail closed。

**`call-set/1`**（调用集合）根恰好 5 键；`items[]` 每项恰好 6 键：

```json
{
  "schema_id": "call-set/1",
  "schema_version": 1,
  "lane_id": "A",
  "task_id": "p2-tome-texts-bNN-001",
  "items": [
    {
      "revision_key": "<key>",
      "section": "mod-tome/data/lore/example.lua",
      "source": "<精确 source 字节>",
      "source_tag": "_t",
      "args_order": null,
      "special": null
    }
  ]
}
```

`items` 排序键：`revision_key`，然后 `section`、`source`、`source_tag`、
`canonical(args_order)`、`canonical(special)`。`args_order`／`special`
无值时为 JSON `null`，不得缺键。

**`runtime-key-set/1`** 根恰好 5 键；`items[]` 每项恰好 2 键。`items`
排序键：`runtime_key`，然后 `source_tag`。

```json
{
  "schema_id": "runtime-key-set/1",
  "schema_version": 1,
  "lane_id": "A",
  "task_id": "p2-tome-texts-bNN-001",
  "items": [
    {"runtime_key": "<runtime-key>", "source_tag": "_t"}
  ]
}
```

**`term-narrative-set/1`** 根恰好 5 键；`items[]` 每项恰好 2 键。
`kind` 只能是 `"term_claim"` 或 `"narrative_closure"`；`key` 为该
claim／闭包的冻结标识字符串，非空。`items` 排序键：`kind`，然后
`key`。不能从受跟踪工作集确定性冻结 `key` 时，不得并行。

```json
{
  "schema_id": "term-narrative-set/1",
  "schema_version": 1,
  "lane_id": "A",
  "task_id": "p2-tome-texts-bNN-001",
  "items": [
    {"kind": "term_claim", "key": "<frozen-claim-id>"}
  ]
}
```

#### `lane-workset/1`（primary 的外部冻结来源）

现有 P2 批次 workset 缺少 `schema_id`、`lane_id`、冻结 `revision_key`
与确定性导出的 primary content file paths，不足以作为 checker 可独立
验证的 exact-key 来源。Phase 1 新增最小 `lane-workset/1`。路径必须精确
为 `.ai/waves/<wave-id>/LANE-<lane-id>-WORKSET.json`。`schema_id` 必须
精确为 `lane-workset/1`，`schema_version` 必须为整数 `1`。根对象恰好
7 个键，不得有额外键；identity **不**写入本对象：
`workset_identity = SHA-256(canonical 本根对象 bytes)`。WAVE
`lanes[]` 保存 `workset_path` 与 `workset_identity`，DISPATCHED 前
写入并冻结。

```json
{
  "schema_id": "lane-workset/1",
  "schema_version": 1,
  "lane_id": "A",
  "task_id": "p2-tome-texts-bNN-001",
  "ordered_revision_keys": ["<key-1>"],
  "calls": [
    {
      "revision_key": "<key-1>",
      "section": "mod-tome/data/lore/example.lua",
      "source": "<精确 source 字节>",
      "source_tag": "_t",
      "args_order": null,
      "special": null
    }
  ],
  "primary_content_paths": ["mod-tome.lua"]
}
```

`calls[]` 每项恰好 6 个键，与 `call-set/1`.`items[]` 相同。`calls` 与
`ordered_revision_keys` 1:1 同序。`lane_id`／`task_id` 必须与 WAVE
对应 lane 字节相等。`primary_content_paths` 按路径字节序排序、无重复。

独立导出算法（checker 必须执行，不得信任 workset 或 collateral
artifact 中的声明数组）：

```text
for each call in lane-workset/1.calls
    （若已冻结 review envelope，其调用集合必须与 calls 1:1 同键）:
  用 pinned manifest 的 component.sources.mount 前缀匹配 call.section，
  得到唯一 component；取其 component.translation 为该调用的实际译文
  文件（例如 section "mod-tome/…" → "mod-tome.lua"）。
  无唯一匹配、匹配到非受跟踪译文文件、或定位失败 → fail closed。
exported_primary = sort_by_path_bytes(unique(located translation files))
```

要求精确相等：

```text
exported_primary
  == lane-workset/1.primary_content_paths
  == lane task-content-allowed-files/1.translation_fix_paths
  == collateral-authorization/1.primary_content_paths
```

任一不等、workset identity 与 WAVE 冻结值不等，或无法从绑定路径读取
workset 当前字节，则不得 DISPATCHED／不得报告 wave `DONE_VERIFIED`。

第四类是嵌入的 `collateral-authorization/1`。它**记录**推导结果，
**不得**作为 primary／ordinary 的权威来源，不得自己声明这两类路径后
自证 collateral 为空。该 artifact 根恰好 13 个键；
`primary_content_paths`／`ordinary_non_collateral_paths`／
`collateral_paths` 均为按路径字节序排序的字符串数组，无重复：

```json
{
  "schema_id": "collateral-authorization/1",
  "schema_version": 1,
  "lane_id": "A",
  "task_id": "p2-tome-texts-bNN-001",
  "spec_path": ".ai/task/<task-id>/SPEC.md",
  "spec_identity": "<64-lowercase-hex>",
  "scope_path": ".ai/task/<task-id>/SCOPE.json",
  "scope_identity": "<64-lowercase-hex>",
  "allowed_files_path": ".ai/task/<task-id>/SCOPE.json",
  "allowed_files_identity": "<64-lowercase-hex>",
  "primary_content_paths": ["mod-tome.lua"],
  "ordinary_non_collateral_paths": [],
  "collateral_paths": []
}
```

`spec_identity` 为 `SPEC.md` 原始 UTF-8 字节的 SHA-256。
`scope_path` 指向该 lane 的 `task-content-allowed-files/1`。Phase 1
要求 `allowed_files_path` 与 `scope_path` 字节相等，且
`allowed_files_identity` 与 `scope_identity` 字节相等（均为该 JSON
文件 canonical 字节的 SHA-256）。Phase 1 将
`ordinary_non_collateral_paths` **规范固定为 JSON `[]`**：checker
发现任何非空声明即 fail closed，不得把它当作减法集合。wave evidence
路径不得出现在任何 lane 的 `allowed_files`、`primary_content_paths`、
`ordinary_non_collateral_paths` 或 `collateral_paths` 中。

确定性推导（checker 必须执行；primary 来自冻结 workset 的独立导出，
ordinary 固定为 `[]`）：

```text
authorized = task-content-allowed-files/1.allowed_files
             （从 WAVE 绑定的 lane SCOPE／allowed_files_path 当前字节加载）
exported_primary = 上列 lane-workset 独立导出算法
ordinary_non_collateral_paths = []    # Phase 1 规范常量，非规划者字段
collateral_paths = sort_by_path_bytes(
  authorized
  minus exported_primary
  minus []
)
```

忽略态 runtime 前缀（`.ai/task/`、`.ai/waves/`、`.ai/reviews/`、
`.artifacts/`）不是任务内容，不得进入 `allowed_files`；若出现则落入
remainder，Phase 1 失败（不得把它们改填进 ordinary 来消掉）。Phase 1
并行要求重算 `collateral_paths` 为 `[]`。声明 `primary_content_paths`
必须等于 `exported_primary`；声明 `ordinary_non_collateral_paths` 必须
为 `[]`；声明 `collateral_paths`、重算数组与
`collateral_authorization_identity`（嵌入对象 canonical SHA-256）必须
字节级一致。不得因 collateral artifact 内声明 `[]` 而跳过 workset
加载与独立导出。

CONFLICT-PREFLIGHT 根对象：

```json
{
  "schema_id": "conflict-preflight/1",
  "schema_version": 1,
  "wave_id": "p2-wave-001",
  "base_commit": "<40-lowercase-hex>",
  "ordered_lane_ids": ["A", "B"],
  "sets": [
    {
      "lane_id": "A",
      "task_id": "p2-tome-texts-bNN-001",
      "call_set": {"schema_id": "call-set/1", "schema_version": 1, "lane_id": "A", "task_id": "p2-tome-texts-bNN-001", "items": []},
      "call_set_identity": "<64-lowercase-hex>",
      "runtime_key_set": {"schema_id": "runtime-key-set/1", "schema_version": 1, "lane_id": "A", "task_id": "p2-tome-texts-bNN-001", "items": []},
      "runtime_key_set_identity": "<64-lowercase-hex>",
      "term_narrative_set": {"schema_id": "term-narrative-set/1", "schema_version": 1, "lane_id": "A", "task_id": "p2-tome-texts-bNN-001", "items": []},
      "term_narrative_set_identity": "<64-lowercase-hex>",
      "collateral_authorization": {
        "schema_id": "collateral-authorization/1",
        "schema_version": 1,
        "lane_id": "A",
        "task_id": "p2-tome-texts-bNN-001",
        "spec_path": ".ai/task/<task-id>/SPEC.md",
        "spec_identity": "<64-lowercase-hex>",
        "scope_path": ".ai/task/<task-id>/SCOPE.json",
        "scope_identity": "<64-lowercase-hex>",
        "allowed_files_path": ".ai/task/<task-id>/SCOPE.json",
        "allowed_files_identity": "<64-lowercase-hex>",
        "primary_content_paths": ["mod-tome.lua"],
        "ordinary_non_collateral_paths": [],
        "collateral_paths": []
      },
      "collateral_authorization_identity": "<64-lowercase-hex>"
    }
  ],
  "pairwise_intersections_empty": true,
  "result": "PASS"
}
```

`sets[]` 每项恰好包含示例中的 10 个键。`sets` 与
WAVE.`ordered_lane_ids` 1:1。每项 `lane_id`／`task_id` 必须与三个嵌入
集合 artifact 以及 `collateral_authorization` 根上同名字段字节相等，
并与 WAVE 绑定的 `lane-workset/1` 同名字段字节相等。`call_set.items[]`
必须与该 lane `lane-workset/1.calls[]` 1:1 同序同键。四个 `*_identity`
必须等于 checker 从对应嵌入对象重算的 SHA-256；声明值与重算值任一不
等即失败。`lanes[].spec_path` 必须与该 lane
`collateral_authorization.spec_path` 字节相等。`lanes[].workset_path`
／`workset_identity` 必须与当前 `lane-workset/1` 字节一致。
`collateral_authorization.primary_content_paths` 必须等于从该 workset
独立导出的 primary，不得把嵌入声明当作来源。

Pairwise 重算（对 `ordered_lane_ids` 中每一对 `a < b`）：

- 调用集合相交：两边 `call_set.items[]` 在
  `(section, source, source_tag, canonical(args_order), canonical(special))`
  上有交集；
- 运行时键相交：两边 `runtime_key_set.items[]` 在
  `(runtime_key, source_tag)` 上有交集；
- 术语／叙事相交：两边 `term_narrative_set.items[]` 在 `(kind, key)`
  上有交集。

Phase 1 并行要求：每个 `ordinary_non_collateral_paths` 为 `[]`；每个
`collateral_paths` 按 workset 独立导出算法重算为 `[]`；三类 pairwise
交集全部为空；由此重算 `pairwise_intersections_empty` 为 JSON
`true`、`result` 为 `"PASS"`。文件内声明值必须与重算值字节级相等；
不得因声明 `true`／`"PASS"`／`[]` 而跳过重算、跳过加载 lane workset
或跳过加载授权字节。任一项非空、primary 与独立导出不等、ordinary 非
空或无法重算则不得 DISPATCHED。DONE checker 还须确认当前
CONFLICT-PREFLIGHT 文件字节的 canonical SHA-256 等于 WAVE 冻结的
`conflict_preflight_identity`，且每个 lane-workset 当前字节的
canonical SHA-256 等于 WAVE 冻结的 `workset_identity`。

Phase 2 的 `CONFLICT-GRAPH.json` 是独立文件，不进入 `wave/1` 根对象，
也不替代上述集合 artifact。

#### `task-content-allowed-files/1`（统一授权面）

路径默认 `.ai/task/<task-id>/SCOPE.json`。`schema_id` 必须精确为
`task-content-allowed-files/1`，`schema_version` 必须为整数 `1`。根对象
恰好 7 个键，不得有额外键；三个数组／路径字段均按路径字节序排序、无
重复。identity **不**写入本对象：
`allowed_files_identity = SHA-256(canonical 本根对象 bytes)`。

```json
{
  "schema_id": "task-content-allowed-files/1",
  "schema_version": 1,
  "task_id": "p2-tome-texts-bNN-001",
  "wave_id": "p2-wave-001",
  "allowed_files": ["mod-tome.lua"],
  "translation_fix_paths": ["mod-tome.lua"],
  "wave_evidence_path": null
}
```

约束：

- `allowed_files` 是 allowed-files checker 与最终 diff closure 的**唯一**
  授权数组。`translation_fix_paths` 只是内容修复子集（semantic／
  translation scope／union SCOPE）；checker 不得把它当作全部授权。
- lane：`wave_evidence_path` 必须为 JSON `null`；`allowed_files` 必须
  与 `translation_fix_paths` 字节级相等，且必须等于该 lane 冻结
  `lane-workset/1` 独立导出的 primary；不得包含
  `WAVE.wave_evidence_path`。
- integration：`wave_evidence_path` 必须与 `WAVE.wave_evidence_path`
  字节相等；`translation_fix_paths` 必须等于参与且已 DONE 的各 lane
  独立导出 primary 之并集（按路径字节序）；`allowed_files` 必须
  等于 `translation_fix_paths ∪ {wave_evidence_path}` 的排序唯一并集。
  这是 integration task 的**唯一** task-content 授权面。不得为 fresh
  evidence-only dispatch 再定义第二份 `allowed_files`。
- FIX EXECUTOR 只可写 `translation_fix_paths`。evidence-only 是同一
  integration task 内 fresh dispatch 的语义写入子集：prompt／dispatch
  只允许 `wave_evidence_path`，机器授权仍是上述唯一并集。evidence
  dispatch 前后，checker 要求每个 `translation_fix_paths` 文件的内容
  哈希与冻结 `integration-content-diff/1` 完全一致（`entries[].
  new_content_sha256`，未出现在 `changed_paths` 的路径则与
  `old_content_sha256`／`base_commit^{tree}` 字节一致）；任何翻译
  变化 fail closed。
- WAVE.`integration.allowed_files_path`／`allowed_files_identity`
  绑定 integration 这份对象；lane 的对应绑定在
  `collateral-authorization/1`，但其 primary 来自 WAVE 绑定的
  `lane-workset/1`，不是 collateral artifact 自证。

integration 示例（`allowed_files` 为 FIX 子集与唯一 wave evidence
路径的并集）：

```json
{
  "schema_id": "task-content-allowed-files/1",
  "schema_version": 1,
  "task_id": "<integration-task-id>",
  "wave_id": "p2-wave-001",
  "allowed_files": [
    "evidence/quality/p2-waves/p2-wave-001-adjudication.json",
    "mod-tome.lua"
  ],
  "translation_fix_paths": ["mod-tome.lua"],
  "wave_evidence_path": "evidence/quality/p2-waves/p2-wave-001-adjudication.json"
}
```

#### `integration-content-diff/1`（可重算、非自引用）

路径：`.ai/task/<integration-task-id>/INTEGRATION-CONTENT-DIFF.json`。
`schema_id` 必须精确为 `integration-content-diff/1`，`schema_version`
必须为整数 `1`。根对象恰好 8 个键；`entries[]` 每项恰好 3 个键。
identity **不**写入本对象。

```json
{
  "schema_id": "integration-content-diff/1",
  "schema_version": 1,
  "wave_id": "p2-wave-001",
  "task_id": "<integration-task-id>",
  "base_commit": "<40-lowercase-hex>",
  "translation_paths": ["mod-tome.lua"],
  "changed_paths": ["mod-tome.lua"],
  "entries": [
    {
      "path": "mod-tome.lua",
      "old_content_sha256": "<64-lowercase-hex>",
      "new_content_sha256": "<64-lowercase-hex>"
    }
  ]
}
```

```text
content_diff_identity = SHA-256(canonical integration-content-diff/1 bytes)
```

重算配方（preimage **只**覆盖 wave evidence 写入前的 translation-only
integration 内容 diff，明确排除 wave evidence 自身）：

1. `translation_paths` 必须与冻结的 integration
   `translation_fix_paths` 字节级相等，按路径字节序排序，不得包含
   `WAVE.wave_evidence_path`。
2. 对每个 `translation_paths` 项，从 `base_commit^{tree}` 取旧文件字节
   （`old_content_sha256 = SHA-256(旧字节)`），从冻结当时的工作树取新
   文件字节（`new_content_sha256 = SHA-256(新字节)`）。
3. `changed_paths` 为 `old_content_sha256 != new_content_sha256` 的
   路径，按路径字节序排序；`entries` 与 `changed_paths` 1:1 同序。
4. 不得把含 `content_diff_identity` 的对象再哈希；不得用含 wave
   evidence 的最终工作树 diff 作为本 artifact 的 preimage。
5. WAVE.`integration.content_diff_path`／`content_diff_identity` 与
   wave-evidence.`integration` 同名字段绑定同一路径与 identity。
   DONE checker 从冻结 artifact 与当前 translation-only 工作树相对
   `base_commit^{tree}` 独立重算并比较。

本文件在最新 full candidate 冻结时一并冻结；每次 integration FIX 后
必须重冻后再进入下一轮全量复审。写入 wave evidence **不得**改写本文件。

#### wave evidence（`wave-evidence/1`）

唯一文件：`evidence/quality/p2-waves/<wave-id>-adjudication.json`，即
`WAVE.wave_evidence_path`。`schema_id` 必须精确为 `wave-evidence/1`，
`schema_version` 必须为整数 `1`。根对象恰好包含下列 13 个键，不得有
额外键。本文件是 integration 任务内容，不是 lane collateral，也不是
`.ai/waves/` 编排记录。

写入者：integration task 中 lineage 核验的 EXECUTOR（parent 为 wave
`orchestrator_agent_id`，`labels.role=executor`，workspace 等于
integration `workspace_id`）。写入发生在最终复审无 open finding、门禁
通过之后，且 prospective DONE WAVE 已按第 5.6 节终结协议冻结并算出
`wave_record_identity` 之后、权威 `WAVE.json` 发布之前。evidence 绑定
该 prospective identity；不得把 GATED（或更早）WAVE 字节的哈希写入
`wave_record_identity`。若当时已无未归档 EXECUTOR，则在**同一**
integration task 内派发 fresh evidence-only EXECUTOR：这是语义写入
子集，prompt／dispatch 只允许本文件，不得改译文，**不得**另建第二份
`allowed_files`。checker 在该 dispatch 前后核验所有
`translation_fix_paths` 内容哈希与冻结 `integration-content-diff/1`
完全一致。ORCHESTRATOR 不得创建、编辑或覆盖本文件；它只把路径与受控
输入交给 EXECUTOR，并在 WAVE／MERGE-QUEUE／DONE 核验中绑定路径、
identity 与内容。evidence 通过 schema／identity／prospective 引用与
译文未漂移检查后，将完全相同的 prospective 字节原子发布为权威
`WAVE.json`，再跑最终 closure；外部 `DONE_VERIFIED` 不写入 WAVE。

```json
{
  "schema_id": "wave-evidence/1",
  "schema_version": 1,
  "wave_id": "p2-wave-001",
  "base_commit": "<40-lowercase-hex>",
  "orchestrator_agent_id": "<wave-orchestrator-agent-id>",
  "wave_record_identity": "<64-lowercase-hex>",
  "merge_queue_identity": "<64-lowercase-hex>",
  "conflict_preflight_path": ".ai/waves/<wave-id>/CONFLICT-PREFLIGHT.json",
  "conflict_preflight_identity": "<64-lowercase-hex>",
  "lanes": [
    {
      "lane_id": "A",
      "task_id": "p2-tome-texts-bNN-001",
      "workspace_id": "<lane-workspace-id>",
      "final_candidate_identity": "<64-lowercase-hex>",
      "target_patch_identity": "<64-lowercase-hex>",
      "final_review_kind": "full",
      "final_review_dispatch_id": "<dispatch-id>",
      "final_review_record": "<record-id>",
      "done_verified": true
    }
  ],
  "integration": {
    "task_id": "<integration-task-id>",
    "workspace_id": "<integration-workspace-id>",
    "executor_agent_id": "<lineage-verified integration EXECUTOR>",
    "combined_candidate_identity": "<64-lowercase-hex>",
    "content_diff_path": ".ai/task/<integration-task-id>/INTEGRATION-CONTENT-DIFF.json",
    "content_diff_identity": "<64-lowercase-hex>",
    "final_review_kind": "full",
    "final_review_dispatch_id": "<dispatch-id>",
    "final_review_record": "<record-id>",
    "initial_git": {
      "head_commit": "<40-lowercase-hex>",
      "index_tree": "<40-lowercase-hex>",
      "worktree_tree": "<40-lowercase-hex>"
    },
    "done_verified": true
  },
  "collateral_empty": true,
  "gates_result": "PASS"
}
```

`lanes[]` 每项恰好 9 个键，与 WAVE.`ordered_lane_ids` 1:1。
`integration` 恰好 11 个键；`initial_git` 恰好 3 个键。
`orchestrator_agent_id` 只记录 wave 编排者身份，不得当作内容作者。
内容作者是 `integration.executor_agent_id`，必须等于 integration
STATE 中 lineage 核验的 EXECUTOR `agent_id`。
`combined_candidate_identity` 不得等于任一 lane 的
`final_candidate_identity`、任一 `target_patch_identity` 或任何
closure identity。`target_patch_identity` 只出现在 `lanes[]`，只记为
apply 输入。`conflict_preflight_path`／`conflict_preflight_identity`
必须与 WAVE 冻结值字节相等，且等于对当前 preflight 文件字节重算的
canonical SHA-256。`content_diff_path`／`content_diff_identity` 必须
与 WAVE.`integration` 同名字段字节相等，且等于对冻结
`integration-content-diff/1` 重算的 identity；不得用含 evidence 的
最终 diff 或含自身 identity 的对象冒充。`collateral_empty` 与
`gates_result` 是声明值；checker 必须从 WAVE 绑定的 `lane-workset/1`
独立导出 primary、令 ordinary=`[]` 后重算 collateral 为空，并从绑定
STATE 实跑的 lane／integration `DONE_VERIFIED` 与门禁记录核验
`gates_result` 为 `"PASS"`。wave-evidence 内的 `done_verified` 只记录
当时 lane／integration 任务 checker 结果，不是 wave 级终态，也不得
回写进被哈希 WAVE。

`initial_git` 记录首次 apply 前的实测 OID，供 DONE 时核验（当时工作
树已前进）。谓词：

- `head_commit` 必须等于冻结 `base_commit`（commit OID）；
- `index_tree` 与 `worktree_tree` 必须彼此相等，且等于
  `base_commit^{tree}`（tree OID）。checker 从 git 对象库解析
  `base_commit^{tree}`，不把 tree OID 与 commit OID 直接比较。

wave evidence 自身 identity 不得写入本文件；checker 从绑定路径读取
字节并按 6.2 配方核验内容。

#### 按 `state` 的绑定填充

| `state` | lane 身份 | integration 身份 | 根级冻结／绑定 |
| --- | --- | --- | --- |
| PREFLIGHT | 身份字段 `null`；`workset_identity` 可仍 `null` | 全部 `null` | `conflict_preflight_identity` 可仍 `null` |
| DISPATCHED | 身份字段 `null`；`workset_path`／`workset_identity` 已为路径＋64-hex 并冻结 | 全部 `null` | `conflict_preflight_path`／`conflict_preflight_identity` 已为 64-hex 并冻结 |
| LANES_READY | 最终候选／review／patch 身份均为 64-hex；对应 lane STATE 已 `DONE_VERIFIED`（外部，不写入 WAVE） | `task_id` 等可仍为 `null` | 同上 |
| INTEGRATING | 同上 | task／workspace／path／`allowed_files_path`／`allowed_files_identity` 非空并冻结；候选与 content-diff 可仍 `null` | 同上 |
| FINAL_REVIEW | 同上 | `combined_candidate_identity`、`content_diff_path`／`content_diff_identity` 为 64-hex 并冻结 | 同上 |
| GATED | 同上 | 最终复审绑定完成，finding 已清空，门禁声明通过 | 不得把本状态 WAVE 字节当作最终 `wave_record_identity`；prospective 尚未发布 |
| DONE | 同上 | 全部绑定完成 | 权威 WAVE 已发布（字节＝prospective）且 evidence 已存在；**尚可能未** `DONE_VERIFIED` |

`DONE_VERIFIED` 是外部 checker 终态，不出现在上表 WAVE 字段中，也不
写入被哈希 WAVE。`wave_evidence_path` 自 DISPATCHED 起冻结，但
`wave-evidence/1` 文件只在上表 `DONE` 时必须存在且完整；更早状态若该
路径已有文件，checker 仍按 schema 解析，不得当作 DONE 证明。

#### 唯一无循环终结协议

全篇只采用下列精确协议。禁止「先写 evidence 再生成 final WAVE」，也
禁止「先发布 DONE WAVE 再写 evidence」。禁止回绕或重渲染。

a. **构造 prospective DONE WAVE。** 最终复审与门禁通过后，ORCHESTRATOR
   构造精确 canonical bytes：`state="DONE"`；**不包含** `done_verified`
   声明；绑定所有前阶段 frozen identities（含各 lane
   `workset_path`／`workset_identity`、`conflict_preflight_identity`、
   `allowed_files_identity`、`content_diff_identity`、lane／
   integration 最终候选与 review 绑定）以及唯一 wave evidence 普通
   路径。写入明确的临时冻结路径
   `.ai/waves/<wave-id>/WAVE.DONE.prospective.json`，**不**发布为权威
   `WAVE.json`。
b. **计算** `prospective wave_record_identity = SHA-256(该 prospective
   canonical bytes)`。
c. **lineage 核验的 integration EXECUTOR 写 wave evidence**，evidence
   绑定该 prospective identity。必要时同一 task 内 fresh evidence-only
   dispatch，语义上只写 evidence 路径。
d. **checker 验证** evidence schema／identity、引用的 prospective
   identity，以及所有 `translation_fix_paths` 内容哈希相对冻结
   `integration-content-diff/1` 未漂移。
e. **将完全相同的 prospective bytes 原子发布**为权威
   `.ai/waves/<wave-id>/WAVE.json`；不得重渲染、不得改字段、不得补写
   `done_verified`。发布后权威 WAVE 字节必须与 prospective 文件字节
   全等。
f. **运行最终** `base_commit`→工作树 allowed-files／diff／evidence
   closure 与各 lane／integration checker。外部结果为
   `DONE_VERIFIED`。`DONE_VERIFIED` 不写入被哈希 WAVE，不修改 WAVE
   bytes。

崩溃恢复（fail closed；identity 或字节不一致则 `WAIT_USER`）：

- 临时 prospective 已存在、evidence 不存在：续写 evidence，复用已冻
  结的 prospective 字节，不得重新生成不同 identity。
- evidence 已存在、权威 WAVE 尚未发布（仍为 GATED 或 prospective 未
  拷贝）：核验 evidence 引用的 prospective identity 与当前
  prospective 字节后，原子发布相同字节。
- 权威 WAVE 已发布、closure 未完成：只重跑 closure，不得改 WAVE 或
  evidence 字节。
- prospective／权威 WAVE／evidence 引用的 identity 或字节不一致：fail
  closed／`WAIT_USER`，不得修补哈希。
- 临时 prospective 与 evidence 均缺失、WAVE 仍为 GATED：仅当从 GATED
  绑定确定性重放步骤 a 所得字节唯一时才可重建 prospective；否则
  `WAIT_USER`。

前一阶段 identity 的绑定是单向的：preflight／workset identity 不包含
WAVE 或 evidence；content-diff identity 不包含 evidence 或 WAVE；
prospective DONE WAVE identity 不包含 evidence 内容。不得要求
evidence 先哈希尚未冻结的 prospective WAVE，也不得在 WAVE 仍为 GATED
时把该哈希标为最终 identity，更不得在发布后再改 WAVE 字节。

#### Wave DONE predicate（checker 机械闭合）

Phase 1 wave checker 以权威 `WAVE.json` 为**唯一入口**，只读核验；经
WAVE 绑定路径读取 MERGE-QUEUE、CONFLICT-PREFLIGHT、各
`lane-workset/1`、各 lane／integration STATE／SPEC／
`task-content-allowed-files/1`／TARGET-PATCH、
`integration-content-diff/1`、prospective 冻结文件、以及唯一 wave
evidence。任一项失败则不得报告 wave `DONE_VERIFIED`：

1. WAVE／MERGE-QUEUE／CONFLICT-PREFLIGHT／`lane-workset/1`／
   `task-content-allowed-files/1`／`collateral-authorization/1`／
   `integration-content-diff/1`／wave evidence 均能按上述 exact-key
   schema 解析；无额外键；canonical 重算不失败。根对象键数：WAVE 14、
   WAVE.`lanes[]` 14、WAVE.`integration` 12、MERGE-QUEUE 6、
   CONFLICT-PREFLIGHT 8、`sets[]` 10、`lane-workset/1` 7、
   `collateral-authorization/1` 13、`task-content-allowed-files/1` 7、
   `integration-content-diff/1` 8、wave-evidence 13、
   wave-evidence.`lanes[]` 9、wave-evidence.`integration` 11。权威
   WAVE 不得含 `done_verified` 键。
2. `WAVE.state` 精确为 `"DONE"`。权威 WAVE 字节必须与
   `WAVE.DONE.prospective.json` 全等。`wave_record_identity` 必须等于
   对该 prospective／权威 DONE WAVE 字节重算的 SHA-256，不得等于任何
   GATED／更早快照。
3. `base_commit` 在 WAVE、MERGE-QUEUE、CONFLICT-PREFLIGHT、每份
   TARGET-PATCH、`integration-content-diff/1`、以及 wave evidence 中
   为同一 commit OID（`^[0-9a-f]{40}$`）。integration 首次 apply 前的
   `initial_git.head_commit` 等于该 commit OID；`initial_git.index_tree`
   与 `initial_git.worktree_tree` 等于 `base_commit^{tree}`。不得要求
   tree OID 等于 commit OID。
4. 每个 lane／integration `STATE.orchestrator_agent_id` 等于
   `WAVE.orchestrator_agent_id`。
5. 每个 lane：`STATE.task_id`／`workspace_id` 与 WAVE 绑定一致；
   `child_dispatches` 每条 `workspace_id` 等于该 lane workspace；parent
   lineage 等于 wave ORCHESTRATOR；无 role=`orchestrator` 的 child；现有
   `ai_state_check.py` 对该 STATE 返回 `DONE_VERIFIED`（外部，不写入
   WAVE）；checker 加载 WAVE 绑定的 `workset_path` 当前字节，重算
   `workset_identity`，按独立导出算法得到 primary，并要求它与 lane
   `translation_fix_paths` 及 `collateral-authorization/1`.
   `primary_content_paths` 精确相等；`ordinary_non_collateral_paths`
   必须为 `[]`；再 `collateral = allowed_files − primary − []` 重算为
   `[]`，且 SPEC 禁止 collateral；WAVE `collateral_empty` 必须与该重算
   一致，不得只信布尔声明、空数组或 collateral artifact 自证；
   `final_candidate_identity` 等于该 lane 最新 full contextual
   identity；`final_review_kind="full"`；`final_review_record` 存在且
   绑定同一 identity 与 `final_review_dispatch_id`；TARGET-PATCH 的
   `candidate_identity`／`target_patch_identity`／`ordered_revision_keys`
   与最终 envelope 一致。
6. MERGE-QUEUE 的每项 `candidate_identity`／`target_patch_identity` 与
   对应 lane 绑定字节相等。
7. integration：STATE 存在且 `DONE_VERIFIED`；`combined_candidate_identity`
   为 64-hex，且不等于任一 lane 的 `final_candidate_identity`，也不等于
   任何 closure identity；最终复审 `review_kind="full"` 且绑定该 identity；
   `open_accepted_findings` 与 `deferred_findings` 均为 `[]`；权威
   translation-only diff／envelope 属于 integration task 的
   `integration-content-diff/1`，而非某份 lane TARGET-PATCH。
   `task-content-allowed-files/1`.`allowed_files` 必须等于
   `translation_fix_paths ∪ {WAVE.wave_evidence_path}`；这是唯一授权
   面，不得存在第二份 evidence-only `allowed_files`。FIX 子集不得被
   当作全部授权。WAVE.`integration.allowed_files_path`／
   `allowed_files_identity` 必须与当前授权面字节一致。每个
   `translation_fix_paths` 文件的当前内容哈希必须与冻结
   `integration-content-diff/1` 完全一致。
8. 全部参与 child 在各自 STATE 中 `archive_confirmed=true`；同一
   `agent_id` 不跨 task 出现。
9. `WAVE.wave_evidence_path` 精确等于唯一公式路径；该文件存在且为
   `wave-evidence/1`；从 prospective／权威 DONE WAVE／MERGE-QUEUE 绑定
   字节重算 `wave_record_identity` 与 `merge_queue_identity`，文件内
   对应字段必须与之相等。`conflict_preflight_path`／
   `conflict_preflight_identity` 在 WAVE 与 wave-evidence 中字节相等，
   且等于对当前 preflight 文件字节重算的 canonical SHA-256。每个
   `workset_identity` 等于对当前 `lane-workset/1` 字节重算的 SHA-256。
   `integration.executor_agent_id` 必须是 integration STATE 中
   lineage 核验的 EXECUTOR。ORCHESTRATOR 内容 diff 不得包含该路径。
10. 从 WAVE 绑定的 `lane-workset/1` 独立导出每个 primary，从
    CONFLICT-PREFLIGHT 绑定的嵌入 artifact 重算三个集合 identity、
    `collateral_authorization_identity`、全部 pairwise intersections、
    每个 `ordinary_non_collateral_paths=[]`、每个推导所得
    `collateral_paths=[]`，以及 `pairwise_intersections_empty`／
    `result`；声明值必须与重算值相等。
11. 从冻结 `integration-content-diff/1` 与当前工作树相对
    `base_commit^{tree}` 的 translation-only 路径独立重算
    `content_diff_identity`；必须与 WAVE 与 wave-evidence 的绑定值
    相等。preimage 不得包含 wave evidence，也不得包含自身 identity。
    evidence 写入后各 `translation_fix_paths` 内容哈希仍须与该冻结
    artifact 一致。
12. 权威 WAVE 发布之后，对 `base_commit`→最终工作树的全部任务内容
    路径（含 evidence）重跑 allowed-files／diff closure：变更路径必须
    是唯一 integration `allowed_files` 并集的子集；wave evidence 路径
    必须在最终 diff 中出现；`translation_fix_paths` 不得被误用作该
    检查的全部授权。evidence schema／identity／prospective 引用交叉
    核验通过后，checker 才报告外部 `DONE_VERIFIED`；该结果不写入
    WAVE 字节。

Checker 不把「各 lane 均 DONE」当作 wave DONE。Phase 2 只可选在此
predicate 上增加：存在并校验 `CONFLICT-GRAPH.json`（第 13 节）。
MERGE-QUEUE checker 与 DONE checker
均须绑定并核验同一 `wave_evidence_path`、其 identity 字段与内容；不得
另设入口绕过 WAVE。

## 6. 语义补丁 `TARGET-PATCH`

### 6.1 版本化 schema

规范化文件为任务作用域普通 JSON：

```text
.ai/task/<task-id>/TARGET-PATCH.json
```

`schema_id` 必须精确为 `target-patch/1`，`schema_version` 必须为整数 `1`。
根对象恰好包含下列 7 个键，不得有额外键：

```json
{
  "schema_id": "target-patch/1",
  "schema_version": 1,
  "base_commit": "<40-lowercase-hex>",
  "task_id": "p2-tome-texts-bNN-001",
  "candidate_identity": "<64-lowercase-hex>",
  "ordered_revision_keys": ["<key-1>", "<key-2>"],
  "changes": [
    {
      "revision_key": "<key-1>",
      "section": "mod-tome/data/lore/example.lua",
      "source": "<精确 source 字节>",
      "source_tag": "_t",
      "args_order": null,
      "special": null,
      "call_index": null,
      "old_target": "<精确旧 target 字节>",
      "new_target": "<精确新 target 字节>"
    }
  ]
}
```

约束：

- `base_commit` 必须精确等于该 wave／lane 冻结的 `base_commit`
  （`^[0-9a-f]{40}$`），不得改写为 lane 完成时的 HEAD 或其他 commit；
- `candidate_identity` 必须是该 lane **最终**审核 envelope 的 identity
  （`translation_contextual_v1` 或日后 v2 的 **full** identity），不是
  中间 cycle、不是 closure identity；
- `ordered_revision_keys` 与最终 envelope 的冻结顺序和集合精确一致；
- `changes` 只含 `new_target` 与 `old_target` 字节不等的条目，顺序与
  `ordered_revision_keys` 中这些 key 的相对顺序一致；
- 每个 `changes[]` 必须恰好包含 9 个键：`revision_key`、`section`、
  `source`、`source_tag`、`args_order`、`special`、`call_index`、
  `old_target`、`new_target`；`args_order`／`special` 无值时为 JSON
  `null`，不得缺键；
- `new_target` 必须与最终 envelope 中该 `revision_key` 的
  `translation_snapshot.target` 字节相等；`source` 必须与 snapshot
  `source` 字节相等；
- `old_target` 必须从冻结 `base_commit^{tree}` **重算**：定位该调用后
  取其 target 字节。不得只与 export 时 lane 工作树或 apply 时当前树比较
  了事。重算失败、定位不唯一且 `call_index` 不能消歧，或重算值与字段
  字节不等，一律 fail closed；
- 出现在 `ordered_revision_keys` 但不在 `changes` 中的 key，其 envelope
  target 必须与 `base_commit^{tree}` 中该调用的 target 字节相等。

定位真实调用使用
`(section, source, source_tag, canonical(args_order), canonical(special),
call_index)`。`call_index` 为该元组在文件顺序下精确匹配中的 0-based
下标；匹配唯一时必须为 JSON `null`，不唯一时必须为冻结的非负整数。缺省、
类型错误或与树中匹配不一致则 fail closed。行号不作为定位身份。

### 6.2 规范序列化与哈希配方

canonical TARGET-PATCH bytes = UTF-8 JSON：

- object key 递归按字节序排序；
- array 保持冻结顺序；
- 分隔符精确为逗号和冒号，无多余空白、无换行；
- `ensure_ascii=false`，字符串按 JSON 转义规则；
- 错误容器、缺键、额外键使序列化失败。

```text
target_patch_identity = SHA-256(canonical TARGET-PATCH bytes)
field_sha256(s)       = SHA-256(UTF-8 bytes of s)
```

`canonical(args_order)`／`canonical(special)` 使用与 patch 相同的紧凑
UTF-8 JSON；JSON `null` 保持 `null`。`apply`／`verify` 用 `field_sha256`
核验 `source`／`old_target`／`new_target` 与最终 envelope 及工作树字节。
`target_patch_identity` 由 integration EXECUTOR 写入唯一 wave evidence
的 `lanes[].target_patch_identity`，不回写进被哈希的 patch 根对象。
WAVE.json、MERGE-QUEUE.json、CONFLICT-PREFLIGHT.json、
`lane-workset/1`、嵌入的 `call-set/1`／`runtime-key-set/1`／
`term-narrative-set/1`／`collateral-authorization/1`、
`task-content-allowed-files/1`、`integration-content-diff/1`、
`wave-evidence/1`、v2 payload／结果、`review-closure/1` 与
`closure-dependency-graph/1` 使用同一配方。
`conflict_preflight_identity`、`workset_identity`、
`allowed_files_identity`、`content_diff_identity` 均不得写入各自被
哈希的根对象。

### 6.3 export／apply／verify

建议命令（落地时作为契约／工具任务，不在本文修改 `tools/`）：

- `python3 -B tools/i18n export-target-patch ...`
- `python3 -B tools/i18n apply-target-patch --strict ...`
- `python3 -B tools/i18n verify-target-patch ...`

规则：

- **export 只从最终候选派生**：最终 envelope、其 `candidate_identity`、
  以及该 identity 对应工作树。中间 FIX、未完成 FINAL_REVIEW、或仍有
  accepted／deferred finding 时拒绝 export。`base_commit` 写入冻结
  wave／lane base；每个 `old_target` 从 `base_commit^{tree}` 重算；
- **apply 到集成工作树的唯一执行者是 integration EXECUTOR**。lane
  EXECUTOR 只在本 lane workspace 写入本 lane 译文，不把 patch 应用到
  集成树。ORCHESTRATOR 不得 apply。首次 apply 前必须满足：`HEAD` commit
  OID 精确等于同一 `base_commit`；index 树与 tracked worktree 内容树
  精确等于 `base_commit^{tree}`；任务内容无 dirty／untracked；仅允许
  第 5.4 节列出的 ignored runtime artifacts。后续 patch 仍按
  MERGE-QUEUE 顺序应用到该同一基线之上；
- **verify** 拒绝：`base_commit` 与 WAVE／lane 冻结 base 不等、重复
  `revision_key`、重叠定位元组（含相同 `call_index`）、SPEC 外路径、
  未在 `changes` 中声明的 `t()` target 改动、`new_target` 与最终
  envelope 不等、`old_target` 与 `base_commit^{tree}` 重算值不等、
  `old_target` 与 apply 时当前树不等、源调用字段不匹配、未完成 lane 的
  patch、以及参与 lane 集合与冻结 MERGE-QUEUE 不一致。

只与当前树比较而不能从 `base_commit^{tree}` 复现 `old_target`，不得视为
verify 通过。

这样可以：在不相交 lane 之间避免行号冲突；在相邻文本被上游改写后仍按调用
身份定位；对共享键、重复 source 和未完成组合 fail closed；精确证明最终
集成只包含已审核 target。

## 7. Review 协议

### 7.1 Phase 1 仍使用 `translation_contextual_v1`

最先落地的并行版本仍使用 `translation_contextual_v1` 的七键 envelope 与
逐条回显结果。这**不**表示 Phase 1 无需契约或流程变更。并行所依赖的变更
是 wave／integration 任务、第 5.1 节拓扑扩展、第 5.6 节最小 WAVE／
MERGE-QUEUE／CONFLICT-PREFLIGHT／`lane-workset/1`／allowed-files／
content-diff schema 与 checker、conflict preflight、TARGET-PATCH、
由冻结 workset 独立导出的空 collateral，以及对组合候选与
translation-only diff 的冻结、独立最终复审（含 accepted finding
收敛）、门禁、第 5.6 节终结协议与外部 `DONE_VERIFIED`。这些完成前
只能串行。

Lane 内与 integration 的首轮／最终轮均使用 v1 全量复审；schema 4 implement 的中间轮已经可
使用普通七键 v1 子集 envelope 做 closure。v2 不是 subset closure 的前置条件。

### 7.2 `translation_contextual_v2`：未来紧凑输出优化

v2 **不得**做成 findings-only 加 coverage digest。缺少逐条 disposition
会使「未报 finding 的 key 已被审核」不可核验。v2 在工具和契约测试完备后
可于 Phase 3 启用，但它只优化 full／closure 结果的重复长文本回显，不负责解锁 subset
closure；后者已由 v1 七键 envelope 加记录层 metadata 实现。schema 在本文一次性定义完整，落地时不得再发明键。
规范化字节配方与第 6.2 节相同。

#### Full payload（被哈希对象）

根对象恰好 8 个键，不得有额外键；`translation_snapshot[]` 每项恰好
`revision_key`、`source`、`target` 三键；`bounded_context[]` 每项恰好
`revision_key`、`context` 两键：

```json
{
  "contract": "translation_contextual_v2",
  "review_kind": "full",
  "ordered_revision_keys": ["<key-1>", "<key-2>"],
  "translation_snapshot": [
    {"revision_key": "<key-1>", "source": "<冻结 source>", "target": "<冻结 target>"}
  ],
  "fixed_source_identity": "<manifest 固定的来源身份>",
  "terminology_snapshot": "<渲染进 briefing 的精确术语子集字符串>",
  "bounded_context": [
    {"revision_key": "<key-1>", "context": "<有界语境字符串>"}
  ],
  "rendered_briefing": "<计算身份前的最终渲染 briefing 字符串>"
}
```

约束：`contract` 精确为 `translation_contextual_v2`；`review_kind` 精确为
`"full"`；`ordered_revision_keys` 与两个 array 1:1 且顺序冻结；除 JSON
字符串与这两个 array 外不得出现其他类型；`rendered_briefing` 不得嵌入已
计算的 64-hex identity。`fixed_source_identity` 取值与 v1 相同。

```text
candidate_identity = SHA-256(canonical full payload bytes)
```

`candidate_identity` 必须匹配 `^[0-9a-f]{64}$`。它不得进入被哈希的
payload。外层 envelope 恰好两个键：

```json
{
  "candidate_identity": "<64-lowercase-hex>",
  "payload": {"…": "上列 8 键 payload 原样"}
}
```

宿主在派发前、返回后和接受前都从 payload 按配方重算 identity；envelope
值、返回值回显与重算值三者任一不等即作废。

#### Full 结果

结果必须是单一紧凑 JSON object，根恰好 6 个键：

```json
{
  "contract": "translation_contextual_v2",
  "candidate_identity": "<64-lowercase-hex>",
  "review_kind": "full",
  "disposition_digest": "<64-lowercase-hex>",
  "dispositions": [
    {"revision_key": "<key-1>", "disposition": "OK"},
    {"revision_key": "<key-2>", "disposition": "finding"}
  ],
  "findings": [
    {
      "revision_key": "<key-2>",
      "observation": "<非空问题描述>",
      "source_sha256": "<64-lowercase-hex>",
      "target_sha256": "<64-lowercase-hex>"
    }
  ]
}
```

`dispositions[]` 每项恰好 `revision_key`、`disposition` 两键。
`findings[]` 每项恰好 `revision_key`、`observation`、`source_sha256`、
`target_sha256` 四键。

校验（fail closed）：

1. `contract` 精确等于 `translation_contextual_v2`；
2. `review_kind` 精确为 `"full"`，且与被哈希 payload 中的 `review_kind`
   一致；
3. `candidate_identity` 匹配 `^[0-9a-f]{64}$`，回显 envelope 值，且等于
   从冻结 payload 重算的 SHA-256；
4. `dispositions` 长度、集合和顺序与冻结 `ordered_revision_keys` 精确
   一致；每个 `disposition` 只能是 `OK` 或 `finding`；
5. `findings` 与 `disposition == "finding"` 的条目 1:1：相同
   `revision_key` 集合、相同相对顺序、无额外、无缺失；`OK` 条目不得出现
   在 `findings`；
6. 每条 finding 的 `source_sha256`／`target_sha256` 必须等于
   `field_sha256(冻结 source)`／`field_sha256(冻结 target)`；
7. `observation` 非空，且不得使用 `OK` 作为 finding 文本；
8. 不得填写 severity、确认状态、suggested fix 或未声明字段。

`disposition_digest` 配方（对 `dispositions` 数组本身做 canonical JSON，
不是字符串拼接）：

```text
canonical_disposition_bytes = UTF-8 JSON(array of dispositions)
  配方同 6.2
disposition_digest = SHA-256(canonical_disposition_bytes)
```

宿主从冻结 envelope 重算 digest 与每条 source／target hash；digest 或
hash 不匹配即作废。输出仍与全部冻结 revision 严格绑定，但不回显完整长
文本。现行 full 与 closure identity 都继续使用 `translation_contextual_v1` 的七键
配方；本节 schema 只在 Phase 3 作为 compact-output 优化进入派发与结果。

### 7.3 中间轮 review closure

首轮和**最终轮**仍为全量复审：最终 phase 必须复审**最新完整候选的全部
keys**，绑定完整候选 identity。schema 4 implement 的中间 FIX 后 reviewer 现在即可读取普通
七键 v1 subset envelope；review 记录在 envelope 外保存 `review_kind=closure`、
`parent_candidate_identity` 与有序 inclusion。closure 结果不能充当 FINAL_REVIEW 或
wave／integration 的 full 证明。现行 v1 的 changed+dependency closure 由 ORCHESTRATOR 根据
任务 diff、finding 与批内依赖确定；checker 只验证 record／envelope 自洽，不机械重建完整
依赖集合。任何歧义回退 full，强制最终 full 是 correctness backstop。

#### 未来 v2 可选的紧凑 closure manifest（不是 v1 subset 的前置条件）

下列 10 键 manifest 只描述未来 v2 compact-output 的可选强绑定设计。现行 v1 subset closure
不创建它或 dependency graph artifact、不把 `review_kind` 加入 payload，也不改变七键
candidate identity：STATE review 记录的 parent／inclusion 与普通 v1 envelope 只提供
self-consistency binding，closure 完整性仍由 ORCHESTRATOR 负责。

路径：`.ai/task/<task-id>/REVIEW-CLOSURE-<cycle>.json`。`schema_id` 必须
精确为 `review-closure/1`，`schema_version` 必须为整数 `1`。根对象恰好
包含下列 **10** 个键，不得有第 11 键；`inclusion[]` 每项恰好
`revision_key`、`reasons` 两键；`subset_payload` 恰好 8 个键，形状与
7.2 full payload 相同，但 `review_kind` 必须为 `"closure"`，且其
`ordered_revision_keys` 必须与根上同名字段字节级相等。这 10 个键是：
`schema_id`、`schema_version`、`review_kind`、
`parent_candidate_identity`、`cycle`、`post_fix_diff_identity`、
`ordered_revision_keys`、`inclusion`、`dependency_graph_digest`、
`subset_payload`。canonical 哈希向量即这 10 键对象的 6.2 配方字节，
不多也不少：

```json
{
  "schema_id": "review-closure/1",
  "schema_version": 1,
  "review_kind": "closure",
  "parent_candidate_identity": "<最新完整候选的 64-lowercase-hex>",
  "cycle": 3,
  "post_fix_diff_identity": "<64-lowercase-hex>",
  "ordered_revision_keys": ["<subset-key-1>", "<subset-key-2>"],
  "inclusion": [
    {
      "revision_key": "<subset-key-1>",
      "reasons": ["changed_target"]
    }
  ],
  "dependency_graph_digest": "<64-lowercase-hex>",
  "subset_payload": {
    "contract": "translation_contextual_v2",
    "review_kind": "closure",
    "ordered_revision_keys": ["<subset-key-1>", "<subset-key-2>"],
    "translation_snapshot": [
      {"revision_key": "<subset-key-1>", "source": "<冻结 source>", "target": "<冻结 target>"}
    ],
    "fixed_source_identity": "<manifest 固定的来源身份>",
    "terminology_snapshot": "<精确术语子集字符串>",
    "bounded_context": [
      {"revision_key": "<subset-key-1>", "context": "<有界语境字符串>"}
    ],
    "rendered_briefing": "<闭包 briefing>"
  }
}
```

禁止用字符串拼接、分隔符或「manifest 字节 + 子 envelope 字节」构造
identity。唯一配方：

```text
closure_identity = SHA-256(canonical review-closure/1 bytes)
```

`parent_candidate_identity`、`post_fix_diff_identity`、
`dependency_graph_digest` 与 `closure_identity` 均须匹配
`^[0-9a-f]{64}$`。`cycle` 必须是正整数 JSON number，且等于 STATE 中该
次 FIX 的 `cycle`。`inclusion.reasons` 是非空数组，元素只能是
`changed_target`、`open_finding`、`shared_runtime_key`、
`narrative_or_term_claim`、`extra_touched_target`。每个 closure key 必须
出现在 `inclusion` 中且 reasons 非空；`inclusion` 顺序与
`ordered_revision_keys` 1:1。

`post_fix_diff_identity` 为该 cycle 冻结的有界任务自身 diff 原始字节的
SHA-256，并与 STATE 中该 cycle 的 diff 记录一致。

`dependency_graph_digest` 为下列 exact-key 图对象的 canonical UTF-8 JSON
之 SHA-256，不是边列表的手写拼接：

```json
{
  "schema_id": "closure-dependency-graph/1",
  "schema_version": 1,
  "nodes": ["<revision_key>"],
  "edges": [
    {"from": "<key>", "to": "<key>", "reason": "shared_runtime_key"}
  ]
}
```

图根恰好 4 键；`edges[]` 每项恰好 `from`、`to`、`reason` 三键。为使
digest 唯一：`nodes` 按 revision_key 字节序排序；`edges` 按 `from`、
`to`、`reason` 字节序排序。图不能按此规则唯一规范化则不得生成 closure，
回退全量。

#### Closure 结果

根对象恰好 10 个键（与 manifest 同为 10 键，但是另一组键，不得混用）；
`dispositions[]`／`findings[]` 的 exact-key 与 7.2 相同。结果绑定的
`candidate_identity` 必须回显并等于对 **10 键** `review-closure/1`
manifest 重算的 `closure_identity`：

```json
{
  "contract": "translation_contextual_v2",
  "candidate_identity": "<closure_identity 的 64-lowercase-hex>",
  "review_kind": "closure",
  "parent_candidate_identity": "<parent full 的 64-lowercase-hex>",
  "cycle": 3,
  "post_fix_diff_identity": "<64-lowercase-hex>",
  "dependency_graph_digest": "<64-lowercase-hex>",
  "disposition_digest": "<64-lowercase-hex>",
  "dispositions": [
    {"revision_key": "<subset-key-1>", "disposition": "OK"}
  ],
  "findings": []
}
```

校验在 7.2 的 1、4–8 条之外，还要求：`review_kind` 精确为 `"closure"`；
`candidate_identity` 回显并等于从冻结 manifest 重算的 `closure_identity`；
`parent_candidate_identity`、`cycle`、`post_fix_diff_identity`、
`dependency_graph_digest` 与 manifest 对应字段字节相等；`dispositions`
只覆盖 closure `ordered_revision_keys`，不得覆盖父候选的全部 keys。

#### Identity 区分

| 种类 | 哈希对象 | 用途 |
| --- | --- | --- |
| full `candidate_identity` | v1 七键 payload，或 v2 8 键 full payload（含 `review_kind=full`） | 首轮、最终轮、TARGET-PATCH、integration 组合候选 |
| v1 closure `candidate_identity` | 普通七键 v1 subset payload；`review_kind`、parent 与 inclusion 仅在 review 记录 | 现行 schema 4 中间轮 |
| future v2 closure identity | 整个 10 键 `review-closure/1` 对象的 canonical JSON（`schema_id`、`schema_version`、`review_kind`、`parent_candidate_identity`、`cycle`、`post_fix_diff_identity`、`ordered_revision_keys`、`inclusion`、`dependency_graph_digest`、`subset_payload`） | 仅未来 compact-output 中间轮 |
| `target_patch_identity` | canonical TARGET-PATCH（7 键根对象，不含自身 identity） | export／apply／verify；写入 wave evidence 的 `lanes[].target_patch_identity` |
| `conflict_preflight_identity` | canonical 8 键 CONFLICT-PREFLIGHT 根（不含自身 identity） | WAVE 从 DISPATCHED 冻结；wave-evidence 与 DONE checker 交叉核验当前字节 |
| `workset_identity` | canonical 7 键 `lane-workset/1` 根（不含自身 identity） | WAVE `lanes[]` 从 DISPATCHED 冻结；checker 独立导出 primary |
| `wave_record_identity` | canonical 14 键 prospective DONE WAVE 根（`state=DONE`，不含 `done_verified`，不含自身 identity） | 只写入 wave evidence；权威 WAVE 必须是相同字节 |
| `content_diff_identity` | canonical 8 键 `integration-content-diff/1`（不含自身 identity；preimage 为 translation-only） | WAVE 与 wave-evidence 绑定；不得用含 evidence 的最终 diff 或自哈希冒充 |

现行 v1 保持七键 identity 不变，由 review 记录的互斥 `review_kind` 区分 full／closure；
closure 记录另存 `parent_candidate_identity` 与有序 inclusion。未来 v2 若启用，则其 full 与
closure 哈希对象包含互斥的 `review_kind` 字面量，且 v2 closure 记录再保存 `cycle`、
`post_fix_diff_identity` 与 `dependency_graph_digest`。

checker 与 ORCHESTRATOR 不得把 closure identity／closure 记录当作
FINAL_REVIEW 完成证明，也不得把它写入 WAVE 的
`final_candidate_identity` 或 `combined_candidate_identity`。
FINAL_REVIEW 必须绑定最新完整候选的 full identity 与其全部 keys。

若 closure 无法可靠计算、post-fix diff 含声明外写入、parent identity
漂移、key 集合不确定、或 dependency graph 不能得出单一结果，则自动
回退 `RE_REVIEW/full`。v1 subset closure 由 schema 4 契约支持，checker 只验证其 envelope／
record 自洽；未来 v2 仅替换输出的长文本回显方式，不改变该 fallback 或最终 full 要求。

## 8. 术语与共享键隔离

普通 lane 对术语库只读。任何需要以下操作的 observation 都进入 quarantine：

- 修改 terminology；
- 全局重命名；
- 改动另一个 lane 或范围外 section 的共享键；
- 确立跨批次人物、地点或组织译名。

quarantine 项写入 wave 的 `TERM-CLAIMS.json`，按标准化 source、tag、候选
译名和证据去重。它们不会阻塞无关 lane，但在未裁决前不得进入目标集成。
真正的术语修改仍由单写入者的独立术语批次完成。

## 9. 门禁策略

### 9.1 首版：每 lane 与 integration 均完整门禁

每条 lane 与 integration task 都完整运行：

1. strict lint；
2. 464 项单测；
3. runtime collision scan；
4. runtime key classification；
5. diff check；
6. `tools/ci-gates.sh`；
7. `DONE_VERIFIED`。

Lane 门禁可在不同 worktree 并行。Integration 仅在组合候选最终复审无
accepted／deferred finding 之后，才跑同一套完整五步和 CI。Wave checker
以权威 WAVE 为唯一入口，按第 5.6 节 predicate 机械闭合：所有参与
lane 与 integration 均已外部 `DONE_VERIFIED`，组合候选是 integration
自己的最新 full identity，最终复审 `review_kind=full`，WAVE／
MERGE-QUEUE／CONFLICT-PREFLIGHT／`lane-workset/1`（含冻结根 identity
与从 workset 独立导出的 collateral）与唯一 wave evidence 绑定完整，
translation-only `integration-content-diff/1` 可重算且译文未漂移，
prospective 与权威 WAVE 字节全等，最终 allowed-files／diff／evidence
closure 覆盖含 evidence 的全部任务内容，且 preflight PASS 由绑定字节
重算而非声明布尔值或空数组。wave 级 `DONE_VERIFIED` 不写入 WAVE。

### 9.2 可选的快速模式

若维护者以后明确修改仓库规则，可考虑 lane 内只跑 strict lint、范围验证和
diff check，把完整单测／构建合并到 integration 后运行一次。

该模式会改变「每批完整门禁」的现行不变量，未经维护者裁决不得启用。首版
Grok 不依赖这项优化。

## 10. 调度策略

建议按 wave 配置 2–4 条活跃 lane（默认 2；仅在 PREFLIGHT 通过且契约已允许
跨 workspace 受管 lane 之后）：

- reviewer 优先于新 executor，尽快释放已写入 lane；
- 资源充足时可同时推进最多四条 lane；资源受限时保持默认两条，不因配置上限
  强行占满 worker；
- REVIEWER、SENIOR_REVIEWER 或 SCOUT 与 lane 的具体并发由编排器按可用槽位
  调度，不改变每条 lane 内的角色顺序；
- 完成的 child 经 status、attention、activeTurn 和工作树复核后立即归档；
- progress-only 或无 diff 的 executor 仍按无效 dispatch 处理，fresh retry，
  不续跑旧 child。

示例流水（integration 不得插在未完成 lane 之前）：

```text
T0  A-exec   B-exec   C-scout
T1  A-review B-exec   C-exec
T2  A-fix    B-review C-exec
T3  A-review B-fix    C-review
T4  A-DONE   B-review C-fix
T5  A-DONE   B-DONE   C-DONE
T6  integration-exec（fresh EXECUTOR apply TARGET-PATCH；HEAD commit OID
    = base_commit，index／tracked worktree 树 = base_commit^{tree}）
T7  integration-final-review（组合候选全部 keys；有 accepted finding 则
    fresh integration FIX EXECUTOR → 重冻 full → 再全量复审）
T8  gates；构造 prospective DONE WAVE；integration EXECUTOR 写入唯一
    wave evidence（绑定 prospective identity）；原子发布相同字节为
    权威 WAVE；最终 allowed-files／diff／evidence closure；外部
    DONE_VERIFIED（仅在 finding 清空且 5.6 predicate 通过后）
```

## 11. 失败关闭与恢复

以下情况只暂停相关 lane：

- 单次 agent 无效输出；
- 候选 contract／evidence 校验失败；
- 有界修复未通过局部 lint；
- 该 lane 的 TARGET-PATCH export／verify 失败，且尚未进入集成
  （含 `old_target` 与 `base_commit^{tree}` 重算值不一致）。

以下情况暂停整个 wave，或根本不得进入并行 DISPATCHED：

- conflict preflight 不确定、发现相交、ordinary 非 `[]`、primary 与
  冻结 workset 独立导出不等、或任一并行 lane 的 collateral 非空／
  SPEC 仍授权 collateral 修改；
- 拟派发批次需要 collateral 写入：不得并行，改为串行或 `WAIT_USER`；
- evidence-only dispatch 改动了任何 `translation_fix_paths` 字节，或
  试图另建第二份 `allowed_files`；
- prospective／权威 WAVE／evidence 引用的 identity 或字节不一致；
  重渲染或改字段后再发布 WAVE；把 `DONE_VERIFIED` 写入被哈希 WAVE；
- 出现 lane-orchestrator、lane `orchestrator_agent_id` 与 wave 不一致、
  `child_dispatch.workspace_id` 与所属 task 不一致，或跨 task 复用
  `agent_id`；
- 两条 lane 对同一运行时键给出不同目标；
- 需要术语库或全局重命名裁决；
- 集成最终复审的 accepted finding 超出 `translation_fix_paths`（内容
  修复子集／union SCOPE）、触及术语／全局重命名、或暴露共享键冲突；
  该子集内的 accepted finding 走第 5.5 节的 fresh integration FIX
  EXECUTOR，不暂停 wave，也不得跳过修复去跑门禁；
- `TARGET-PATCH.base_commit` 与冻结 wave／lane base 不等；integration
  首次 apply 前 `HEAD` commit OID 不等于该 `base_commit`，或 index／
  tracked worktree 内容树不等于 `base_commit^{tree}`；任务内容
  dirty／untracked；或 `old_target` 不能从 `base_commit^{tree}` 重算；
- 用 closure identity 或某条 lane identity 充当组合 full identity 或
  FINAL_REVIEW 证明；
- 集成后完整门禁失败且一次有界诊断无法归因；
- 同一 revision 出现实质冲突意见；
- child 生命周期或归档状态无法确认；
- 集成补丁触及未授权 section、出现额外写入或未完成 lane；
- 组合候选与 integration 最新 envelope 漂移。

任何 lane 都可以从冻结 `lane-workset/1`、candidate envelope、semantic
patch 和 STATE 重建；wave 还可以从 WAVE／prospective／MERGE-QUEUE／
CONFLICT-PREFLIGHT 绑定（含冻结根 identity 与各 `workset_identity`）、
`task-content-allowed-files/1`、`integration-content-diff/1` 与唯一
wave evidence 重建。终结协议的崩溃恢复见第 5.6 节。不得依赖某个
agent 会话继续存在。ORCHESTRATOR 不通过保留一份可手改的集成 diff 来
恢复，也不写 wave evidence；integration 修复后的权威译文内容是
`integration-content-diff/1` 与最新 full envelope，wave evidence 由其
EXECUTOR 按终结协议绑定 prospective identity 写入。

## 12. 产物与审计

建议新增：

```text
.ai/waves/<wave-id>/WAVE.json
.ai/waves/<wave-id>/WAVE.DONE.prospective.json
.ai/waves/<wave-id>/CONFLICT-PREFLIGHT.json
.ai/waves/<wave-id>/MERGE-QUEUE.json
.ai/waves/<wave-id>/LANE-<lane-id>-WORKSET.json
.ai/waves/<wave-id>/CONFLICT-GRAPH.json          # Phase 2 only
.ai/task/<task-id>/SCOPE.json                    # task-content-allowed-files/1
.ai/task/<task-id>/TARGET-PATCH.json
.ai/task/<integration-task-id>/INTEGRATION-CONTENT-DIFF.json
.ai/task/<task-id>/REVIEW-CLOSURE-<cycle>.json   # Phase 3 only
evidence/quality/p2-waves/<wave-id>-adjudication.json
```

Phase 1 即要求 WAVE／MERGE-QUEUE／CONFLICT-PREFLIGHT／
`lane-workset/1`／`collateral-authorization/1`／
`task-content-allowed-files/1`／`integration-content-diff/1`／
`wave-evidence/1` 的 exact-key schema（第 5.6 节）。
`CONFLICT-GRAPH.json` 只在 Phase 2 由扩展 checker 要求。

`.ai/` 继续作为可重建的运行态（第 5.4 节列出的 ignored runtime
artifacts）；冻结工作集、人工裁决和最终 wave 结果进入受跟踪
`evidence/`。TARGET-PATCH 与 closure manifest 是编排／核验产物，可由
工具在 `.ai/task/` 写出；译文 Lua 与受跟踪 `evidence/` 仍按任务 SPEC 由
EXECUTOR 写入。WAVE.json、prospective、MERGE-QUEUE.json、
CONFLICT-PREFLIGHT.json 与 `lane-workset/1` 由 ORCHESTRATOR 维护为编排
记录，不是任务内容。

唯一 wave evidence 文件、写入者、task-content allowed-files 授权面、
SPEC 归属与 exact-key schema 以第 5.6 节为准，不以本列表再列一份字段。
checker 以 WAVE 为唯一入口绑定 `wave_evidence_path`、
`workset_path`／identity、`conflict_preflight_path`／identity、
`content_diff_path`／identity、`allowed_files_path`／identity 与内容。
不得把 ORCHESTRATOR 记为内容作者，不得把 lane patch identity 记为组合
候选，不得把 GATED WAVE 字节当作最终 `wave_record_identity`，不得在
发布后改写权威 WAVE 字节。

## 13. 分阶段实施

### Phase 0：度量

不改流程，只在接下来两个批次记录各阶段墙钟时间、token、输出字节、无效
dispatch、finding 数和门禁时间，建立基线。这是唯一无需契约／checker 变更
的阶段。现行 P2 批次在后续基础设施落地前继续串行。

### Phase 1：契约门控的并行 MVP

本阶段**必须先**作为 `infrastructure`／`translation_workflow` 任务落地
下列变更，并经独立交叉复审与 checker 覆盖；完成前保持串行：

- 第 5.1 节跨 workspace 拓扑：一个 wave ORCHESTRATOR 直接拥有全部
  child；`child_dispatch.workspace_id` 可与 root 不同；各 lane STATE
  的 `orchestrator_agent_id` 相同；禁止 lane-orchestrator；
- 第 5.6 节最小 `wave/1`（根 14 键；`lanes[]` 14 键，含
  `workset_path`／`workset_identity`，不含 `done_verified`；
  `integration` 12 键，不含 `done_verified`）、`merge-queue/1`（根 6
  键）、`conflict-preflight/1`（根 8 键，外部绑定根 identity）、
  `lane-workset/1`（根 7 键）、`collateral-authorization/1`（根 13
  键；ordinary 固定 `[]`，primary 来自 workset 独立导出）、
  `task-content-allowed-files/1`（根 7 键）、
  `integration-content-diff/1`（根 8 键）、`wave-evidence/1`（根 13
  键）以及三类冻结集合 artifact 的 exact-key schema、canonical
  identity 与 wave DONE predicate；Phase 1 **即交付**对应 checker，而
  不是留到 Phase 2；checker 以 WAVE 为唯一入口，从绑定字节重算
  preflight、workset primary、collateral、translation-only diff 与
  evidence，不信声明布尔值或空数组；
- 受管 wave／integration task：唯一 task-content `allowed_files` 授权
  面（`translation_fix_paths` **加** 唯一 wave evidence 路径；不为
  evidence-only 另建第二份授权面）、冻结组合候选与 translation-only
  diff、独立最终复审、第 5.5 节 accepted finding 收敛（fresh
  integration FIX EXECUTOR、仅 `translation_fix_paths`、重冻 full 与
  content-diff、cycle 2 起 senior audit）、完整门禁、第 5.6 节终结
  协议与外部 `DONE_VERIFIED`；integration SPEC 明文包含唯一 wave
  evidence 路径；`translation_fix_paths` 不得被 allowed-files checker
  误作全部授权；
- 最小 conflict preflight（第 4.1 节）；并行 lane collateral 必须由
  冻结 `lane-workset/1` 独立导出 primary、ordinary=`[]` 后重算为空且
  SPEC 禁止 collateral；三类集合与 `collateral-authorization/1` 嵌入
  CONFLICT-PREFLIGHT 供重算；WAVE 从 DISPATCHED 起冻结
  `conflict_preflight_path`／identity 与各 `workset_path`／identity；
- `target-patch/1` 的 schema、哈希配方、export／apply／verify；
  `base_commit` 等于冻结 base（commit OID）；integration 首次 apply 前
  `HEAD` commit OID 等于该 base，index 与 tracked worktree 内容树等于
  `base_commit^{tree}`；`old_target` 从 `base_commit^{tree}` 重算；
- 明确 ORCHESTRATOR 不写任务内容文件（含 wave evidence）；fresh
  integration EXECUTOR 为唯一集成写入者。evidence-only 是同一 task 内
  语义写入子集，不是第二授权面；冲突 fail closed。终结协议：
  DISPATCHED 冻结 WAVE／preflight／workset → apply／FIX → 冻结候选
  与 translation-only diff → 终审／门禁 → 构造 prospective DONE WAVE
  → 写 wave evidence（绑定 prospective identity）→ 原子发布相同字节
  → 最终 closure → 外部 `DONE_VERIFIED`（不写入 WAVE）。

上述落地后才允许：

- 2–4 条独立 worktree／workspace lane，默认 2、硬上限 4；
- lane 内仍用 `translation_contextual_v1`，首轮／最终轮全量，完整门禁；
- 全部 lane DONE 后由 integration EXECUTOR 应用 TARGET-PATCH，再冻结
  integration 自己的组合候选并做独立最终全量复审；有 finding 则走 5.5。

不得把「多条 worktree + 主编排者 cherry-pick」当作 Phase 1。带
collateral 的批次在本阶段保持串行或 `WAIT_USER`。

### Phase 2：完整冲突图与调度优化（可选扩展，不新写 checker）

- 增加独立文件 `CONFLICT-GRAPH.json` 的 exact-key 字段与检查，并在最小
  preflight 之上做着色；
- 不把「增加 wave 状态检查」写成新能力——该检查属于 Phase 1；
- 不改变 Phase 1 已冻结的 TARGET-PATCH 身份配方，除非走独立契约修订；
- 若要支持 collateral，必须另立补丁契约，不得借用 TARGET-PATCH；在该
  契约落地前并行仍要求 collateral 为空。

Phase 2 `CONFLICT-GRAPH.json` 最小 exact-key：`schema_id` 精确为
`conflict-graph/1`，`schema_version` 为整数 `1`；根恰好 6 键：
`schema_id`、`schema_version`、`wave_id`、`base_commit`、`nodes`、
`edges`。`nodes[]` 恰好 `lane_id`、`task_id` 两键；`edges[]` 恰好
`a`、`b`、`reasons` 三键（`reasons` 为非空字符串数组）。`nodes` 与
WAVE.`ordered_lane_ids` 1:1。无边才可并行。

### Phase 3：紧凑 review 输出（closure 已由 v1 支持）

- 可选启用第 7.2／7.3 节定义的 `translation_contextual_v2` exact-key full
  envelope／结果与 10 键 `review-closure/1`，仅用于压缩输出；有序 disposition +
  canonical digest + finding 1:1，而不是 findings-only；
- v1 中间 closure 不依赖该 manifest；采用 v2 时 full 与 closure identity／record 分离，
  closure 仍不得充当 final full；
- 首轮／最终轮仍全量覆盖最新完整候选全部 keys；不确定即回退全量；
- 更新契约文档、角色 prompt、checker 和单测后才启用。

### Phase 4：超大 section 分片

只对 `misc.lua`、`last-hope.lua` 等大 section，按故事连通分量建立多个只读
review shard。所有 shard 必须精确分区且最终仍经过一个全量 reviewer，绑定
完整候选 identity。此阶段收益最不确定，不作为 MVP 前置条件。

## 14. 验收指标

前三个**已启用并行**的 wave 以如下指标判断是否保留方案（Phase 0 只建基线，
不宣称吞吐提升）：

- 墙钟吞吐至少提高 2 倍；
- source／tag／args_order／special／markup／newline 漂移为 0；
- runtime collision 为 0；
- invalid review 输出率不高于现有基线，Phase 3 后目标低于 2%；
- 中间复审输入 token 由 v1 closure 降低；Phase 3 启用 v2 compact output 后，输入／输出 token
  合计降低至少 50%；
- 语义补丁 merge 因冲突 fail closed 的比例可解释，且不得靠人工猜测合并；
  目标低于 10% 的可恢复冲突；
- 随机抽取至少 10% 已合并条目做全量独立复审，不出现确认级漏检；
- 任一 wave 都能从受跟踪 evidence 和忽略态 STATE 重建；
- ORCHESTRATOR 的内容 diff 为空：译文与 evidence 的作者是 lineage 核验的
  EXECUTOR；
- 每个并行 wave 的组合候选都有独立于各 lane 的 full identity、最终全量
  复审记录和 integration `DONE_VERIFIED`；权威身份是 integration 最新
  候选，lane patch 只记为输入；
- 无并行 wave 在 PREFLIGHT 不确定、ordinary 非 `[]`、primary 与
  workset 独立导出不等、collateral 非空、或 SPEC 仍授权 collateral
  时被 DISPATCHED；
- 每个并行 wave 都有可被 checker 重算的 `WAVE.json`／`MERGE-QUEUE.json`
  exact-key 记录、冻结的 `conflict_preflight_identity` 与各
  `workset_identity`、可重算的 `integration-content-diff/1`、唯一
  `wave-evidence/1` 文件与 prospective／权威 DONE WAVE 相同字节的
  `wave_record_identity`；第 5.6 节 predicate 为 `true`；
- 每个并行 wave 只有一个 `orchestrator_agent_id`；不存在
  lane-orchestrator；每条 `child_dispatch.workspace_id` 等于所属 task
  workspace；
- 每份 TARGET-PATCH 的 `base_commit` 等于冻结 base（commit OID）；
  integration 首次 apply 前 `HEAD` commit OID 等于该 base，index 与
  tracked worktree 内容树等于 `base_commit^{tree}`；`old_target` 可从
  `base_commit^{tree}` 重算；任务内容无 dirty／untracked；
- 每个并行 wave 的 wave evidence 由 lineage 核验的 integration EXECUTOR
  写入 `WAVE.wave_evidence_path`，并列入 integration 唯一
  `task-content-allowed-files/1`.`allowed_files` 与 SPEC；不为
  evidence-only 另建授权面；ORCHESTRATOR 内容 diff 不含该路径；按第
  5.6 节终结协议发布权威 WAVE 后对 base→最终工作树全部任务内容重跑
  allowed-files／diff／evidence closure，外部才 `DONE_VERIFIED`；
- integration 最终复审若曾有 accepted finding，则存在
  `translation_fix_paths` 内的 integration FIX provenance 与重冻 full
  及 translation-only diff 复审，且未在有 open finding 时宣布 DONE。

## 15. 推荐决策

建议立即批准 **Phase 0**。现行串行 P2 继续，同时把 **Phase 1** 列为独立
基础设施任务：先改契约／最小 wave schema 与 checker／跨 workspace 拓扑
扩展／TARGET-PATCH／`lane-workset/1` 独立导出的空 collateral preflight
／唯一 integration allowed-files 授权面／translation-only content-diff
／finding 收敛／第 5.6 节终结协议，再以默认两条 lane 做首轮验证，并用
3／4 lane 正例确认可配置上限。不要批准「无契约变更
的并行 MVP」，也不要把 wave checker 推迟到 Phase 2。带 collateral 的
批次继续串行，直到另有独立补丁契约。

Phase 2 在 Phase 1 的 2–4 lane 试运行稳定后按需实施，只增加完整冲突图、
图着色与调度优化，不负责引入第三或第四条 lane。
Phase 3 只承担 compact-output 契约变化，应作为单独基础设施任务交叉复审，并按第
7.2／7.3 节已冻结的 exact-key schema 落地；它不是 v1 subset closure 的前置条件。Phase 4 仅在跨批次并行仍不足
以处理超大 section 时启用。

不建议一开始就在同一 workspace 内让多个 writer 修改 `mod-tome.lua`，不建议
由 ORCHESTRATOR cherry-pick 集成，不建议引入 lane-orchestrator，也不建议
先取消每批完整门禁。真正的首要瓶颈仍是批次间串行和 review 文本冗余，但
解除串行的前提是组合候选仍能被冻结、独立终审、在 union 内收敛 finding、
按冻结 base 验证补丁、门禁和 DONE 闭合。
