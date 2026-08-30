# 生产译文审核收敛实施规格（分阶段实施）

> **状态：分阶段实施的设计 SPEC，非当前契约。** `translation_surface_screen_v1`
> 最小 pilot、surface manifest/result validator、append-only ledger validator 及相关
> `DONE_VERIFIED` 门禁已落地；deep-review、repair 与完整三任务生产 DAG 仍是后续
> 工作。已实施部分以 `AGENTS.md`、活跃 Paseo 契约和工具行为为准，本文不覆盖
> 它们。所有数量是规划参数或当前估算，不是权威 ledger 事实。

## 1. 目标、原则与三任务 DAG

当前约有 **2.6 万条未逐条语义审核**；这是估算，深审全覆盖不可行。目标是以可恢复、可
度量且不宣称未深审条目已获同等保证的漏斗逐批收敛。筛查只产生候选；固定源码核验和
裁决后，只有 `confirmed` finding 才能进入修复。

每个生产批次必须是下列不可合并的三任务 DAG（箭头表示不可跳过的输入边）：

```
surface-screen (review_only) ──immutable handoff──> deep-review (review_only)
                                      │
                                      └─ candidates + confirmed findings ──> repair (implement)
```

- **surface-screen**：`executing_role=REVIEWER`，terminal predicate 是完整冻结 screen 集合已按本
  SPEC 运行、每项有 `OK|issue` 和 evidence 引用；不得写译文或裁决 finding。
- **deep-review**：`executing_role=REVIEWER`（与 screen 使用独立 attempt），terminal predicate 是
  完整 deep workset 已逐项给出 `OK|issue`，并使每个 issue 可被 ORCHESTRATOR 按固定源码
  标为 `refuted|advisory|pending|confirmed`；不得写译文。
- **repair**：`executing_role=EXECUTOR`，terminal predicate 是所有 confirmed 修复或明确 no-fix
  close 已 revalidated，且 final full 成功；REVIEWER/SCOUT 只读。

ORCHESTRATOR 独占 task `STATE`、裁决、不可变 handoff 的发布以及任务 terminal 决策；REVIEWER
只读，EXECUTOR 是唯一可写实现内容的角色。上述 `executing_role` 只表示执行者，不转移这些
所有权。

每个 handoff 是不可变 JSON：包含上游 task identity、ordered entry-revision identity、
输入 snapshot hash、算法/version、源码 identity、结果 hash、attempt 和生成者/时间；下游
只接受 hash 与集合、顺序、版本逐项相等的 handoff。任何更新产生新 attempt/handoff，旧
记录只读保留；不得用 completion 记录互相替代。repair 只能接收裁决后的 confirmed 清单，
不能把 screen/deep 的 `issue` 直接当修复指令。

### surface contract 与 v2 边界

surface-screen 的最小 pilot 已以 `translation_surface_screen_v1` 独立 purpose/contract 落地；
其输入/输出 schema、terminal predicate、q/r 四路分批、carry-over、raw bytes 绑定、
surface evidence reconciliation 与 ledger 迁移规则以
[`paseo-translation-surface-screen-v1-contract.md`](paseo-translation-surface-screen-v1-contract.md)
和现行工具为准。这只完成 surface 阶段的 review-only pilot，不代表 deep-review、
repair 或本 SPEC 的完整三任务 DAG 已实现。

surface v1 与 `translation_contextual_v2` 只共享 **q/r 四路 partition algorithm**
（稳定排序、`q=floor(n/4)`、前 `r=n mod 4` 路多一项），不复用 v2 的
terminals、stages、`DONE` 语义、completion 记录或 envelope。现行
`translation_contextual_v2` 与 v1 fixture、lane envelope/result schema 继续原样有效；未来
deep/repair schema、迁移和兼容仍须另立实现任务，不能隐式改写 surface v1 或 v2。

## 2. 两级漏斗与完整 batching 算法

每批先冻结 workset、source/target snapshot、固定源码 identity、术语 snapshot 和算法版本。

1. **全量确定性层**：对整个冻结 workset 检查 key、`source/source_tag`、placeholder、
   markup、参数顺序、newline、special、target 存在性、格式、lint、范围和 identity。
   任一失败则 fail closed，不能送 screen；修复后对同一 revision 重跑。
2. **surface screen**：只对确定性通过项筛查，最多 80 条，分四个互斥有序 lane；四 lane
   的有序并集必须精确等于 screen 集合。
3. **context/deep review**：由 screen issue、风险策略及必要依赖构成 deep workset。目标
   容量 16–32；少于 16 按实际数量执行，超过 32 必须稳定拆分，不得截断或丢弃。

批处理是全定义算法：对冻结候选按 canonical entry-revision identity 的稳定字节序排序，
设 `n` 为本次待处理总数：

- `n=0`：不 dispatch，记录零项结果。
- `1≤n≤3`：一个 `full` task，覆盖全部 n 项。
- `4≤n≤80`：以 `q=floor(n/4)`、`r=n mod 4` 切成四个连续 lane；前 r lane 为 q+1，
  其余为 q；不得空 lane，且四 lane 总和恰为 n（现行 surface v1 已实现此算法）。
- `n>80`：取排序后的前 80 做当前四 lane，其余按相同顺序保留为 stable carry-over，
  下批优先处理；不得把 carry-over 记为完成。
- deep 列表以相同排序和依赖闭包重算：按最多 32 条连续 segment 拆分；每段原则上至少
  16 条，但最后 tail 可以小于 16；`n=0` 不 dispatch，所有 segment 的互斥并集必须精确
  等于 deep workset。

每阶段记录实际数、理由、漏斗版本、输入 identity 和未派发 carry-over；“约 2.6 万”、80、
16–32 均不得写成完成数量或覆盖率事实。

## 3. 双层 identity、风险与上下文

`logical_entry_identity` 是跨版本稳定主键：canonical 编码包含规范化来源组件/路径、稳定
调用定位或 revision key、`source_tag` 和必要组件字段；用明确版本的 hash（例如 SHA-256）
对 length-prefixed、UTF-8 canonical bytes 计算。缺字段、canonical 失败或 hash 碰撞均
fail closed，不能猜测或以行号替代。一次性旧 ledger 映射必须输出映射表与未映射清单。

`entry_revision_identity` 是逻辑 identity 的版本化 revision：由 logical identity、原始
source/target snapshot hash、`source_tag`、固定源码/public commit 或 protected snapshot、
术语/规则版本组成。logical identity 不变而 target 修复产生新 candidate/revision，保留
parent lineage；source、source_tag 或固定源码身份变化即 invalidated，必须新 revision，
不得覆盖旧历史。

logical identity 是 ledger、长期指标去重和跨 revision 统计键；revision identity 是阶段
状态、finding、candidate、context、attempt、failure/recovery 和最终覆盖的键。指标同时记录
snapshot、stage 和 attempt，不能由 provider/model 名称推导稳定性。

- **R-high**：数值、持续时间、条件、范围、触发、参数顺序、markup/placeholder、runtime
  文本、核心术语或源码行为风险；必须 deep，必要时 SCOUT。
- **R-medium**：叙事关系、跨条一致性、歧义术语、复杂上下文或筛查命中；按容量 deep，不能
  因 surface OK 自动关闭。
- **R-low**：确定性层充分证明且无语义风险信号；留在 ledger 待抽检队列，**不得伪称深审
  完成**。R-low 与 `AGENTS.md` 或项目 roadmap 的 P3 无关；触及 roadmap P3 策略或全局重命名
  仍须交回用户。

SCOUT 仅在 ORCHESTRATOR 无法可靠闭合机制调用链、来源、依赖闭包或风险分类时按需派发；
返回路径、固定 commit/snapshot 和关键调用的压缩证据，只读且不产生 finding contract。
ORCHESTRATOR 核验后才可放入 briefing。context 仅在条目进入 deep 且当前 claim 需要时释放
最小源码引用、术语 snapshot 和依赖；全仓库或其他任务上下文不得扩散。证据仍不能闭合则
`pending`，停止自动修复。

## 4. 状态表与修复收敛

所有迁移都必须由 revision identity、输入 snapshot/version 和不可变上游 handoff 证明；每个
task 只能由 ORCHESTRATOR 写入 `STATE`、发布 handoff，并判定 terminal 或 `WAIT_USER`。

确定性层是三任务 DAG 之外的前置 gate，不是 semantic task：`deterministic_failed` 必须先
进入 correction 路由，由 ORCHESTRATOR 修正输入／构造并重新冻结、重算 handoff，再回到
`deterministic_pass`；此路由不 dispatch surface、deep 或 repair，不能以 no-dispatch 当作
任务成功。

| 对象 | 状态/迁移（精确定义） |
|---|---|
| entry-revision | `queued → deterministic_pass → screened` 后必须按 surface 结果分支：`OK(deferred) → sampling_queued`（命名的 ledger-only 静置状态，绝不等同于 `deep_reviewed` 或 `closed`；唯一合法退出是之后被选入 `deep_queued → deep_reviewed`，或因输入／源码 identity 变化 `invalidated → queued` 形成新 revision）；`OK(selected)` 或 `issue → deep_queued → deep_reviewed`。deep `OK` 只能经 `revalidated → closed`；deep `issue` 必须先进入 `finding observed → adjudication`，`refuted|advisory` 可在裁决记录和 revalidation 后关闭，`pending` 只能补足证据后 re-adjudication，`confirmed` 只能经 repair 的 `fixed|no_fix_closed` 和 revalidation 后关闭。任一未关闭 revision 遇输入／源码 identity 变化只能 `invalidated → queued`（新 revision，保留旧历史）；已关闭结果只有新的 fidelity/completeness/grammar/terminology/runtime/明显 translationese 证据才可 `reopened → deep_queued`，偏好不得 reopen。确定性失败为 `deterministic_failed`，只能经上述前置 correction 回到 `deterministic_pass`；不满足条件不得前进。 |
| surface task | `queued → running → terminal`；零项为 `zero/no-dispatch` terminal，非零项必须产生完整 screen handoff 后为 `terminal`。transport、缺文件或超限为 `retryable`，归档旧 attempt 后 fresh retry；输入／候选漂移为 `stale`，必须 refreeze 后重跑；不能把 child 结束当 terminal 成功。其结果逐项为 `OK(selected)`、`OK(deferred)` 或 `issue`：selected 才进入 deep，deferred 留在 ledger 待后续抽检，二者都不能把条目声明为 deep-reviewed；`issue` 必须进入 deep。`retryable` 只可经 fresh retry 回到 `queued`，`stale` 只可经 refreeze 回到 `queued`。 |
| deep task | `queued → running → terminal`；零项为 `zero/no-dispatch` terminal，非零项必须产生完整 deep handoff 后为 `terminal`。transport、缺文件或超限为 `retryable`，候选／输入漂移为 `stale`，只可经 refreeze 回到 `queued`；`retryable` 只可经 fresh retry 回到 `queued`；逐项结果为 `OK|issue`，但 `OK` 只表示 deep 结果完成，不替代 finding adjudication。 |
| finding | `observed → refuted|advisory|pending|confirmed`；`pending` 必须保留为 pending，并由 ORCHESTRATOR 在补足证据后执行 re-adjudication，再转为其他 finding terminal；不得自动修复；`confirmed → fixed|no_fix_closed`，二者均须源码／语境证据、裁决记录和 revalidation；已 closed 只有新的 fidelity/completeness/grammar/terminology/runtime/明显 translationese 证据才 `reopened → confirmed`，偏好不 reopen；不可调和冲突或身份无法确认进入 `WAIT_USER`。 |
| repair task | `queued → running → revalidated → closed`；零 confirmed 项仍须显式 `zero/no-dispatch` terminal 并完成 closure；失败为 `retryable`，归档旧 attempt 后 fresh retry 回到 `queued`；输入漂移为 `stale`，需重新冻结并回到 `queued`；达到 max_cycles、身份无法确认或不可调和冲突为 `WAIT_USER`。 |

`DONE` 只有同时满足：surface、deep、repair 三 task 各自已到 terminal；三者的不可变 handoff
已由 ORCHESTRATOR 发布并逐项相容；ledger、阶段状态、review records、冻结输入和最新门禁
一致；repair workset 的所有 revision 均已处理。surface 的 `OK(deferred)` 不是 deep terminal
的替代，deferred 条目不计入 deep-reviewed；deep 的 zero/no-dispatch 只在 deep workset 确实为
零时成立。每批必须有 closure 检查未解决 finding、依赖和 invalidation。

final full 有两层且都必须成功： (a) **deterministic final full** 精确覆盖 repair task
冻结的整个 repair workset（所有 entry-revision，非仅 changed）；(b) **semantic final full**
精确覆盖该 repair task 的完整 deep workset 加全部 confirmed finding 的依赖闭包。不得用历史
成功替代当前输入。`STATE.cycle` 的最新 stage 必须唯一且是该 cycle 最大 `(cycle,attempt)`
的成功 `FINAL_REVIEW/full`；旧 cycle 成功或另一个 stage 不能满足 DONE。final 失败只能进入
更高 cycle 的 `RE_REVIEW/full|closure` 修复序列后重做 final full。

## 5. 失败矩阵与停止

| 失败 | 处理 |
|---|---|
| pre-dispatch 构造错误、缺字段、非法集合 | 不 dispatch；修正并重新冻结/重算 handoff |
| candidate/snapshot/identity drift | 使 attempt stale，整批 refreeze；不得部分沿用 |
| 合法 candidate 的 child/result transport、缺文件、超限 | 保留诊断，archive 旧 attempt，fresh retry 同 purpose/workspace/lineage；重建并核验完整 lane group |
| child 有未提交 raw partials | 不发布；按 live 事实保留或经生命周期流程清理，重新取得完整结果；不得当作成功 |
| 已持久化的 partial publication | fail closed，冻结已发布 bytes，reconcile provenance；无法证明原子完整性则 WAIT_USER |
| archive 状态/identity/lineage 歧义 | 重新查询并检查工作树、记录和 archive；能闭合则 reconciliation，否则 WAIT_USER |
| 两轮 live requery 预算耗尽仍不能判定运行/终态 | **WAIT_USER，不得直接 stop** |
| 不可调和 identity、源码版本或最终覆盖冲突 | WAIT_USER，保留历史，不覆盖或猜测 |

除上述 funnel-specific additions 外，完整停止条件以 `AGENTS.md`「连续批次模式」的「必须
停下并交回用户」整节为准，包含：同一 revision 两轮独立复审实质矛盾；需改术语库、全局
重命名或跨批次统一策略；门禁失败且一次有界诊断无法归因；子 agent 生命周期/归档预算/身份
仍无法确认；达到 `max_cycles`；连续两个 EXECUTOR 无成果；需要 push、开 PR、发布，或触及任何 P3 事项；批次边界存在实质歧义。roadmap P3 与 R-low 无关，不得用连续批次模式绕过这些条件。

## 6. 实施状态、后续工作包与验收

| 工作包 | 当前状态 | 仍待实施 |
|---|---|---|
| 1. 身份/ledger | surface v1 已实现双 identity 重算、canonical SHA-256、append-only 迁移验证、失效/reopen 规则和状态门禁 | 生产旧 ledger 迁移、碰撞处置报告与长期指标审计 |
| 2. 确定性筛查 | surface manifest 已实现稳定排序、q/r 四 lane、zero/full/carry-over 和无静默丢条验证 | 全量生产规则、风险信号和与真实批次冻结的前置 gate |
| 3. surface/deep 编排 | `translation_surface_screen_v1` review-only pilot、整组发布、fresh retry、provenance 和 `DONE_VERIFIED` surface 闭合已实现 | 16–32 deep segment、按需 context、SCOUT 压缩和 deep handoff/terminal |
| 4. 筛查—裁决—修复 | surface observation 已明确不能直接关闭 finding 或宣称 deep-reviewed | 完整三任务 DAG、不可变跨任务 handoff、repair closure/reopen/final full 与原子发布 |
| 5. 指标/门禁 | surface/ledger 工具、契约检查、回归测试和 `ai_state_check.py` 接口已实现 | 完整漏斗指标、报告、CI 与三任务级 `DONE_VERIFIED` |

已实施的 surface pilot 必须继续证明旧 v1/v2 fixture 不变、完整输入无静默丢条、
identity/快照可重算、screen 不直接关闭 finding、live-profile 可路由，并通过契约检查、
相关测试、适用门禁和 `git diff --check`。剩余工作包在后续任务中还必须额外证明：
accepted 结果可由固定源码重算，deep/repair 集合和依赖无静默丢失，且只有当前输入的
最新成功 final full 才能闭合完整三任务 `DONE_VERIFIED`。
