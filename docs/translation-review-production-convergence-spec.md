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
surface-screen (review_only) ──surface handoff──> deep-review (review_only)
                                                     │
                                ORCHESTRATOR adjudication handoff
                                                     │
                                                     ▼
                                              repair (implement)
```

- **surface-screen**：`executing_role=REVIEWER`，terminal predicate 是完整冻结 screen 集合已按本
  SPEC 运行、每项 raw result 恰为 `OK|ISSUE` 并带 evidence 引用；不得写译文或裁决 finding。
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

冻结是三段只追加边界，后段只能引用前段的 hash，不能让初始 manifest 预知未来结果：

1. **batch draft freeze**：冻结 surface eligible 集合 `E`、按稳定优先序得到的 `B`
   （batch-selected）与 `C`（queue carry-over），并同时冻结与 `B` 不交的 ordered promotion
   pool `S`。manifest 对 `S` 记录 canonical ordered-list hash、journal cutoff event、promotion
   eligibility policy identity/hash 及每项来源 provenance；还绑定 source/target snapshot、固定
   源码 identity、术语 snapshot、policy/算法版本等确定性输入。此时只 acquire `B` 的 queue
   ownership，绝不 acquire `C` 或 `S`；draft 必须证明 `S ∩ B = ∅`，且不含尚未产生的
   `X/I/T/A`、raw result、routing、`H/R`、`D` 或 deep segments。
2. **surface terminal freeze**：确定性 gate 与全部 surface lane/zero result 完成并验证后，先完成
   下述 dependency normalization，再由 ORCHESTRATOR 原子发布 `surface_handoff`。该 publication
   建立 `SURFACE_TERMINAL`，并冻结互斥的 `X/I/T/A`、`I` 的逐项 disposition、raw
   `OK|ISSUE` 结果、与 raw 结果分离的 routing sibling mapping/section，以及按 revision identity
   和原依赖边排序的 `required_H` directive 及其 directive identity/SHA-256；`required_H` 恰好且只含
   冻结 `S` 中将由 deep freeze 吸收到 `H` 的外部 entry dependencies，不含同批保留在 `O/J/T` 的依赖，
   也不含同批 `Q→O` override；schema 的分类枚举必须显式包含 `X=deterministic_failed`、
   `I=invalidated`、`T=mandatory_deep_observation` 与
   `A=surface_input`，其中每个 `I` 恰有一个 `successor|requeue|tombstone` disposition。raw item
   schema 不得增加 routing extra field。只有该 handoff 发布后这些结果与 directive 才成为本 batch
   的冻结事实。
3. **deep freeze**：只在已发布 `surface_handoff` 和 draft 冻结的 `S` 上按冻结 cadence 派生
   `H/R`，并验证 `S = H ⊎ R`；随后计算完整 revision workset `D`、稳定分段并原子发布 deep
   freeze manifest。相同 transition group acquire `D \ B` 的 ownership（包括 promoted `H`）；
   任一 revision 已有其他活动 owner即 backpressure/fail closed，manifest 不得部分发布。只有从
   此边界起 `D` 和 `deep_done_segments/deep_pending_segments` 才归本 batch。coordinator 必须记录
   实际 ownership set；闭批时精确 release 仍由本 batch 持有且非 terminal 的 revision，不能按
   推测集合释放。

### 阶段内处理步骤

冻结边界确定后，各阶段按以下顺序处理；本列表不延续上面的三段 freeze 编号：

1. **全量确定性层**：对 `B` 检查 key、`source/source_tag`、placeholder、markup、参数顺序、
   newline、special、target 存在性、格式、lint、范围和 identity。`X` 严格只表示
   construction/extraction/manifest/canonicalization/input-shape failure；现行 ledger 以
   `queued → deterministic_failed` 记录失败，并在修正构造输入、产生新 attempt 和重冻后，仅以
   `deterministic_failed → deterministic_pass` 及 `deterministic_layer` provenance 离开；旧 attempt
   明确 invalidated/disposed，不能留在可继续批次中。确定性规则发现的真实 target 内容问题不进 `X`、
   不自动确认，而记录为 mandatory-deep observation `T`，携带规则/evidence，纳入本批 deep
   review 和后续裁决。`T` 所需 ledger provenance/transition 仍待实施，在迁移和 writer gate 落地
   前生产流程 fail closed，不得伪造现行状态或自动确认。
2. **surface screen**：只对确定性通过项筛查，最多 80 条，分四个互斥有序 lane；四 lane
   的有序并集必须精确等于 screen 集合。
3. **context/deep review**：revision workset 由 route-selected `O`、raw issue `J`、
   mandatory-deep observation `T` 与 deep-only promoted `H` 构成。目标容量 16–32；少于 16
   按实际数量执行，超过 32 必须稳定拆分，不得截断或丢弃。容量不足只产生该 batch 的
   `deep_pending_segments`（有序、互斥、带 owner），不得静默 carry-over 到下批。全部 pending
   segments drain、逐项出结果并完成相应裁决前，该 batch 不得 terminal 或 `DONE`；中断恢复仍
   回到原 batch，输入漂移则在原 batch fail closed 后显式重开新 batch。

批处理是全定义算法：queue 在 batch draft freeze **之前**按全局优先序排序并截取前
`min(N,80)`；该集合称为 **batch-selected revisions**，不得与 raw surface `OK` 后的
**route-selected** 注解混称 `selected`。确定性 gate 在 `B` 内产生 `X=deterministic_failed`、
`I=invalidated`、`T=mandatory_deep_observation` 与 `A=surface_input`；只有 `A` 按 canonical
entry-revision identity 的稳定字节序排序并分 lane。每个 `I` 必须在 transition group 中具有且仅具有
`successor/requeue/tombstone` disposition；未处置不得发布 surface zero 或继续 terminal。raw
surface result 仍恰为 `OK|ISSUE`；ORCHESTRATOR 对 raw `OK` 另算 `selected|deferred` routing，
并写入 `surface_handoff` 中与 raw results 平级、按 revision identity 关联的独立 mapping/section，
绝不写成 raw item extra field。设 `N` 为冻结 eligible 候选总数，`m=min(N,80)` 为
batch-selected revision 数：

- `|surface_input|=0`（包括 `m=0`）：不 dispatch surface，记录绑定空 `surface_input` 的零项结果。
- `1≤|surface_input|≤3`：一个 `full` task，覆盖全部 `surface_input`。
- `4≤|surface_input|≤80`：令 `q=floor(|surface_input|/4)`、`r=|surface_input| mod 4`，切成四个连续 lane；前 r lane 为 q+1，其余为 q；不得空 lane，且四 lane 总和恰为 `|surface_input|`（现行 surface v1 已实现此 lane 算法）。
- `N>80`：全局优先序的前 80 构成当前 batch-selected revisions，其余是 batch manifest 中互斥的 queue `carry_over`；不得把它们记为完成、不得声称是 surface v1 自身 carry-over。batch-selected revisions 与 queue `carry_over` 的并集恰为冻结 eligible 集合且交集为空；`surface_input` 仍按 canonical identity 排序，不改写 surface v1 的 lane 语义。
- surface result 验证后、`surface_handoff` 冻结前执行 **dependency normalization**。同批已处于 `O/J/T` 的必要 entry dependency 优先保留原 bucket，不得重路由；同批 `Q` 才记录不可变 routing override `Q→O`，并以合法 `screened → deep_queued` transition 纳入 `O`；指向同批 `X`、`I` 或其他 bucket 的 dependency 一律 fail closed。任何外部 entry dependency 必须已在 draft 的 `S` 中，否则 stale/refreeze 或 fail closed，禁止冻结后扩张 pool。normalization 在 `surface_handoff.required_H` 冻结 required-H directive，并冻结其 directive identity/SHA-256；该 directive 恰好且只含冻结 `S` 中将吸收到 `H` 的外部 entry dependencies，明确排除同批保留在 `O/J/T` 的依赖和同批 `Q→O` override。deep freeze 派生 `H/R` 时，外部 `sampling_queued` dependency 必须先以 origin provenance 和合法 `sampling_queued → deep_queued` transition 进入 `H`，才能进入 `D`。`S` 中其他外部 dependency 只允许已是 `deep_queued` 且具有完整 provenance 的项：deep freeze 只 acquire ownership、保留来源且不伪造 self-transition，随后纳入 `H`；`screened` 不得直接进入 deep handoff。`deep_handoff` 正文中的 ordered required-H consumption mapping 必须绑定同一 directive identity/SHA-256，并逐项记录 required dependency identity、原依赖边、来源状态和最终 `H` bucket；来源为 `sampling_queued` 的项同时记录实际 `sampling_queued → deep_queued` ledger transition group identity 与 ownership acquire group identity，来源已是 `deep_queued` 的项只记录实际 ownership acquire group identity且不得伪造 ledger self-transition。冻结 `S` 外或不满足上述来源路径的 dependency 一律 fail closed，不能用 context 引用绕过 ledger。
- normalization 后 `D=O⊎J⊎T⊎H`，按 canonical identity 排成最多 32 条的连续 segment；每段原则上至少 16 条，但最后 tail 可以小于 16。非 entry-revision 的源码 context/evidence closure 单独记为 `K`，用固定 recipe 产生 ordered canonical hash 并绑定 `D`/source identity；`K` 不含 entry revision、不计入 `D` 或 segment 数。deep workset 为空时不 dispatch，所有 `deep_done_segments` 与本 batch `deep_pending_segments` 的互斥并集必须精确等于 `D`；pending 全部 drain 前不得关闭 batch。

每阶段记录实际数、理由、漏斗版本、输入 identity 和 queue carry-over；“约 2.6 万”、80、
16–32 均不得写成完成数量或覆盖率事实。

### 2.1 backlog catalog、snapshot 与持久队列（待实施）

生产入口不是目录扫描所得的临时列表，而是一个可重算的 **backlog catalog**。每个 catalog
snapshot 必须绑定 extractor/manifest identity、组件集合、原始输入快照、canonicalization
版本和生成参数；正文按 `logical_entry_identity` 排序，逐行至少记录 logical/revision
identity、组件/路径、source/target/source_tag hash、当前风险输入字段和可处理/排除原因。manifest
记录 schema、行数、正文 SHA-256、生成时间和父 snapshot。只有 manifest 与正文 hash、行数、
identity 唯一性检查全部通过的 snapshot 才可成为某个 epoch 的权威分母。排除项也必须逐项留在
snapshot 或配套 exclusion 表中，带 reason code，不能先过滤再声称全量；catalog 估算不得替代
该分母。具体受跟踪路径、schema 和生成器尚未实现，后续工作包必须先冻结它们。

全局队列由受跟踪的 append-only transition journal 与可丢弃、可重建的 materialized view 组成，
不依赖常驻服务或外部数据库。ledger transition event 至少绑定 event id、catalog/policy epoch、
logical/revision identity、from/to state、batch/task/handoff identity、reason、attempt 和前序 event hash；queue ownership event 使用同一 identity/provenance 外壳，但记录 `acquire|release`、owner 与 reason，不含 ledger from/to state。单维护者只在一个工作树中原子发布一次 transition group。replay 必须拒绝重复 event、非法迁移、
断链、未知 revision 和同一 revision 的多个活动 owner。view 至少暴露 queue ownership reservation、各阶段运行态、`sampling_queued`、`retryable`、`pending`、`closed`、`invalidated` 与 carry-over；其中 reservation、`retryable`、`pending`、`pool_remainder` 以及 coordinator 的 batch-selected/route-selected/deferred/carry-over 都只是 queue/coordinator/view 注解，不是现行 15-state ledger entry 状态。ledger entry 的可处理主链保持 `queued → deterministic_pass → screened`，其余注解不得伪造 ledger 状态或跳过迁移。view 不是权威事实；删除后用 catalog+journal 得到相同 bytes 才算可恢复。

每批选择只读取一个已冻结 catalog snapshot 与一个 policy epoch，冻结 surface draft 前使用如下稳定优先键；先按此全局序截取至 80，再 canonical sort，不能让 surface lane 反向定义 queue：

1. 已承诺 carry-over（按原 batch 和原序位）；
2. 因中断而可重试且输入仍相同的 revision（按首次入队 event）；
3. 强制 deep 风险优先级；
4. 入队 epoch、组件/stratum 和 canonical entry-revision bytes。

在同一优先级中不得用文件系统遍历顺序、child 完成顺序、provider/model 或墙钟随机数排序。
batch draft manifest 记录完整 eligible-set hash、排序算法/version、截取边界、未取条目的 ordered
hash、`batch_selected` 与 coordinator queue `carry_over`；重算必须得到同一 `B/C`。它还从 journal
cutoff 前按 eligibility policy identity 枚举所有可 promotion 的外部 revisions：合法
`sampling_queued` 项，以及依赖图中可能成为本批 entry dependency、已是 `deep_queued` 且具有
完整 provenance 的项，生成 ordered `S`；`screened` 项不得进入该 pool。manifest 记录 `S` 的
canonical hash、cutoff、policy hash、来源状态和 provenance，并验证 `S∩B=∅`。draft 不预填
`surface_input`、raw/routing、`H/R`、deep 集合或 segments。dependency normalization 完成后，
`surface_handoff` 追加冻结 `X/I/T/A` 四分区、每个 `I` 的 disposition、raw results、routing、
routing overrides，以及按 revision identity 和原依赖边排序、可重放的 `required_H` directive 及其 directive identity/SHA-256；其 schema 分类枚举与 §2 的 `X/I/T/A` 定义完全一致。随后 deep freeze 才从
`S` 派生并冻结 `H/R`、验证 `S=H⊎R`，再冻结 `D`、`K` 的独立 canonical hash、
`deep_done_segments` 初始空集、`deep_pending_segments` 及 provenance。各阶段声明的子分区互斥且
无遗漏；不得把 surface v1 的输出字段或分 lane 结果称为 coordinator queue `C`。draft 选择后仅以
queue ownership reservation annotation/event acquire `B`，绝不 acquire `C` 或 `S`；deep freeze
再在一个原子 transition group 中 acquire `D \ B`。该事件不是 ledger transition，不含把
ledger revision 从 `queued` 改为 reservation 的 from/to state。一个 revision 同时只能属于一个未
终结 batch；发现已有 owner 必须 backpressure/fail closed，不得抢占或部分冻结。coordinator 记录
实际 acquire/release 集合；release 同样只是带 reason 的 ownership event，不改变或制造 ledger
state。闭批精确 release 实际 ownership set 中仍非 terminal 的 revision。

新 catalog 到来时先做 reconciliation：logical identity 消失是删除 `tombstone`（保留旧 revision，不制造新条目）；同一 logical identity 的 source/target snapshot 或固定源码改变是同 logical identity 的 revision bump；`source_tag` 或 `call_locator` 改变是新 logical identity 的 migration edge，必须记录旧→新映射及 parent lineage。无法建立唯一映射时列入未映射清单、fail closed，不猜测、不按行号配对。旧 revision 追加 `invalidated`，创建新 revision 并重新入队；不覆盖旧状态。target 修复同样形成新 revision，且只有完成 repair
handoff/revalidation 后才能把新 revision 接入闭环。进程中断后先 replay journal，再核对所有带活动 reservation annotation／running stage 的 task 与已发布 handoff：输入完全相同则从最后一个已原子发布的 stage
继续；只有未发布 partial 则丢弃 partial 并 fresh retry；输入不同则 stale/refreeze。恢复或重算
normalization 时仍须优先保留 `O/J/T`、只将同批 `Q` 转入 `O`、只将冻结 `S` 中合法
`sampling_queued` 或已 `deep_queued` 的外部依赖转入 `H`，其余 fail closed；不得从 `screened`
直接恢复到 deep。恢复必须从已发布 `surface_handoff` 重算同一 required-H directive identity/SHA-256；
仅当 deep freeze 已发布时，还必须重算 ordered consumption mapping，并重新验证
`required_H_consumed == surface_handoff.required_H` 的 ordered identity equality、
`required_H_consumed ⊆ H`、`required_H_consumed ∩ R == ∅`；任一不符即 stale/refreeze 或 fail closed，
不得沿用 partial consumption。deep freeze 尚未发布时不得要求或伪造 consumption mapping。恢复过程
不得凭 child 的单一 status 猜测，也不得跳过 `AGENTS.md` 的生命周期复查。

### 2.2 单维护者的有界并发与 backpressure（待实施）

并发单位是 **batch/stage 的活动 workset**，不是随意启动的 child 数。默认规划窗口为一个活动
生产 batch：surface 至多一个 lane group（算法需要时最多四个 REVIEWER lane）、deep 至多一个
segment、repair 至多一个 EXECUTOR；跨 stage 可以预备已冻结输入，但不能让两个 writer 或两个
repair workset 并行。所有上限都写入 policy epoch 和 batch manifest，pilot 可把 lane 上限降为
1；上限不是完成承诺。SCOUT 占 deep 的只读辅助槽，不扩大 deep workset。

coordinator 每次 dispatch 前以 journal/view 重算 WIP：活动 child、带 reservation ownership 的 revision、未裁决
issue、`pending`、待 repair confirmed、carry-over 与最老队龄。出现任一情形即 backpressure：
达到任一冻结 WIP 上限；有未发布/无法 reconciliation 的 handoff；repair 或 adjudication 积压
达到其上限；门禁失败；队列 view 不能重算一致。此时停止领取新 batch，优先 drain 当前
adjudication/repair/retry；不能靠丢弃、降风险或把 deferred 标 closed 恢复吞吐。连续两个无成果
EXECUTOR、身份歧义等仍按 `AGENTS.md` 停止而不是自动扩容。容量调整只能在 epoch 边界修改下一
policy；无需分布式锁、worker daemon、租约服务或企业调度器。

## 3. 双层 identity、风险与上下文

`logical_entry_identity` 是跨版本稳定主键：canonical 编码包含规范化来源组件/路径、稳定调用定位或 revision key、`source_tag` 和必要组件字段；用明确版本的 hash（例如 SHA-256）对 length-prefixed、UTF-8 canonical bytes 计算。recipe 必须固定 domain separator、字段顺序、编码和长度单位；缺字段、canonical 失败或 hash 碰撞均 fail closed，不能猜测或以行号替代。一次性旧 ledger 映射必须输出映射表与未映射清单。

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

风险与抽检必须由可版本化的 `policy_epoch` 计算。冻结 policy 至少包含 feature schema/ruleset、规则优先级、强制 deep predicate、stratum 定义、每层 sampling threshold、公开 seed、hash 算法、容量/WIP 上限、依赖闭包版本和生效 catalog snapshot。epoch 只冻结有限、明确列举的 catalog slice；有 `starts_at`、`ends_at` 和“无未决 owner/未发布 handoff”三项结束条件。未处理 revision 在 epoch 交界原子重评分并保序（保留旧决策和新决策 hash），不得借边界丢弃或重复。仅 routing-only policy（队列优先级、容量、cadence）可不生成新 revision；改变 fidelity/semantic rules、canonicalization、源码或目标输入的 policy 必须生成新 revision 并走 invalidation/requeue。输入特征只来自冻结条目、规则和
源码 identity；provider/model 可作为成本观测维度，但不得成为风险、抽样、覆盖或质量判定
输入。每个 revision 保存 feature vector/hash、命中的 rule id、risk class、sample score 和决策
理由，使第三方可从 snapshot+policy 重算。

**强制 deep 集合**为：所有 R-high、surface `issue`、新出现或 reopened 的 confirmed/pending
依赖、规则指定的 runtime/数值/参数/markup/核心术语项，以及依赖闭包。它先于抽样和容量截取，
超过当期 deep 容量时形成该 batch 的稳定 `deep_pending_segments` 并触发 backpressure，绝不能降级、丢弃或转为下批 carry-over。R-medium 与
R-low 的质量抽检对冻结 policy 与 revision 输入计算固定 hash score，并以该 stratum 的冻结 threshold 决定是否入选；同一输入重复运行选择相同。canonical recipe 的唯一字段顺序为 `domain || seed-field || epoch-field || stratum-field || revision-field`：domain separator 是 ASCII `tome4-i18n-sampling-v1\0`，随后依次以 UTF-8、无符号大端 u64 length-prefix 编码公开 `seed`、`policy_epoch`、`stratum`、`entry_revision_identity`；`digest=SHA-256(domain || seed-field || epoch-field || stratum-field || revision-field)`，`score` 是 digest 前 8 bytes 的无符号大端整数。`threshold` 为冻结的 `[0,2^64]` 整数，且仅当 `score < threshold` 入样（0 必不入样，2^64 必入样）。实现必须提供 Unicode（多字节及组合字符）、空字段、`score=threshold-1/threshold` 以及两个 threshold 极值的固定测试向量，包含 canonical bytes、digest、score 和预期布尔值。抽样单位、总体 N、入样 n、未响应/失效数都按 stratum 记录。抽中只使当前 surface revision 进入 route-selected；未抽中进入 `sampling_queued`；二者都不因
抽样动作变为 deep-reviewed/closed。deep-only promoted 集合 `H` 只从 draft 已按 journal cutoff、
eligibility policy identity/hash 和 canonical order 冻结的 `S` 派生，与本批 surface `B` 分开。
coordinator 对 `S` 中 sampling candidates 按冻结的 `(policy_epoch, score, origin_batch_id,
origin_ordinal, entry_revision_identity)`（各字段的升降序方向也由 policy 固定）稳定排序、按冻结
cadence 选取，再把 dependency normalization 标为 required 的 `S` 项确定性并入 `H`；不得使用
child 完成顺序或墙钟补位。`H` 每项按其冻结来源状态执行合法 transition：`sampling_queued` 使用
`sampling_queued → deep_queued`，另一允许来源只能是已 `deep_queued`，此时仅 acquire ownership
而不伪造 self-transition；未入 `H` 的 `R` 保持原来源状态，并只使用 coordinator-only
`pool_remainder` 标记（不是 ledger reason），绝不重过 surface `A`。每个提升项的
`deep_handoff` artifact body 中 promotion provenance section 明列 `origin_batch_id`、origin ordinal、
origin policy hash、origin decision hash 和提升原因；这些 origin metadata 不属于 ledger provenance
record，现行 ledger provenance record 仍严格为 `{kind, sha256}`；`H` 纳入 deep freeze、`deep_handoff` 与 ownership，并单独做 promotion
守恒 `S = H ⊎ R`。原 batch 关闭时 reservation 必须原子 release 回 queue并保留
provenance，禁止悬挂 owner。

首个 production epoch 是冷启动校准：先对所有强制 deep 项和一个覆盖组件、文本类型、长度、
历史变更与风险层的冻结分层样本做 deep，不用这一批同时训练再改选这一批。记录 surface
issue 的确认率，以及抽检中发现但 surface 未报的实质 issue（操作性 false negative）；没有
独立 deep 样本、样本为零或分母不足时只报告“不可估”，不得报告零漏报。epoch 结束后才可根据
冻结结果提出下一 policy：保留旧 policy/hash 和决策记录，离线 replay 新旧 policy 的集合差异、
容量与各 stratum 影响，经审核后从下一 policy epoch 生效，不回写当前批次。发现漏报时，对
同 rule/stratum 形成稳定 backsweep 候选并按新 revision/新 batch 处理；不得把统计外推成已确认
finding。误报/漏报、reopen 和返工反馈都只能改变下一 epoch 的规则、threshold 或样本率。

SCOUT 仅在 ORCHESTRATOR 无法可靠闭合机制调用链、来源、依赖闭包或风险分类时按需派发；
返回路径、固定 commit/snapshot 和关键调用的压缩证据，只读且不产生 finding contract。
ORCHESTRATOR 核验后才可放入 briefing。context 仅在条目进入 deep 且当前 claim 需要时释放
最小源码引用、术语 snapshot 和依赖；全仓库或其他任务上下文不得扩散。证据仍不能闭合则
`pending`，停止自动修复。

## 4. 状态表与修复收敛

所有迁移都必须由 revision identity、输入 snapshot/version 和不可变上游 handoff 证明；每个
task 只能由 ORCHESTRATOR 写入 `STATE`、发布 handoff，并判定 terminal 或 `WAIT_USER`。

确定性层是三任务 DAG 之外的前置 gate，不是 semantic task。`X=deterministic_failed` 严格限于
`construction_or_extraction_or_input_shape`：ORCHESTRATOR 修正 manifest/提取/canonicalization
输入，以同 revision 创建新 attempt，明确旧 attempt invalidated/disposition，重新冻结并重跑
deterministic；现行合法离开路径是带 `deterministic_layer` provenance 的
`deterministic_failed → deterministic_pass`。成功重冻后新 attempt 不再含该 `X`，失败则继续
fail closed。真实 target 内容问题
不得进入 `X`，而成为 `T=mandatory_deep_observation`：它只能进入 deep `observed → adjudication`，
不能由 deterministic 自动确认；只有 `confirmed` 才进入 repair，产生 parent→successor revision，
successor 再重跑 deterministic。现行 ledger 尚无 deterministic-observation provenance 与对应
`queued/deterministic_pass → deep_queued` migration，后续工作包必须实现 schema、合法 transition、
canonical provenance 和 writer gate；落地前 `T` 路径不得用于生产或自动确认。`invalidated` 也不是
终点：每项必须记录唯一的 `successor|requeue|tombstone` disposition 和对应 provenance。只要当前
attempt 的 `X` 非空或 `I` 有任何未处置项，batch 只能进入 correction/stale/requeue 路径，禁止
surface/deep/repair zero path 继续到 `DONE`。

| 对象 | 状态/迁移（精确定义） |
|---|---|
| entry-revision | 可处理主链严格为 `queued → deterministic_pass → screened`，绝不包含 reservation；queue coordinator 的 acquire/release reservation 只是 ownership annotation/event，不产生 ledger from/to state。`screened` 后按 raw surface `OK|ISSUE` 与独立 routing annotation 分支：raw `OK` 且 route-deferred 时进入 `sampling_queued`（绝不等同于 `deep_reviewed` 或 `closed`；合法退出是未来 batch 带 origin provenance 直接提升为 `deep_queued → deep_reviewed`，不重过 surface，或因 identity 变化使旧 revision `invalidated` 并按 disposition 创建/requeue successor）；raw `OK` 且 route-selected，或 raw `ISSUE`，进入 `deep_queued → deep_reviewed`。dependency normalization 优先保留同批 `O/J/T`，同批 `Q→O` 使用合法 `screened → deep_queued` 路径；外部 dependency 只可从冻结 `S` 中合法的 `sampling_queued` 路径进入 deep，或在已是 `deep_queued` 时保留状态并 acquire ownership，不能从 `screened` 直达 deep 或以其他方式跳态。`T` 是 mandatory deep 的 entry revision，所有权属于 `D`；待 deterministic-observation migration 落地后才可经其专用 provenance 进入 `deep_queued`，现行 ledger 不得伪造该迁移。deep `OK` 只能经 `revalidated → closed`；deep `issue`（包括 `T`）必须先进入 `finding observed → adjudication`，`refuted|advisory` 可在裁决记录和 revalidation 后关闭，`pending` 只能补足证据后 re-adjudication，`confirmed` 只能经 repair 的 `fixed|no_fix_closed` 和 revalidation 后关闭。任一未关闭 revision 遇输入／源码 identity 变化必须 invalidated 并给出 `successor|requeue|tombstone` disposition；已关闭结果只有新的 fidelity/completeness/grammar/terminology/runtime/明显 translationese 证据才可 `reopened → deep_queued`，偏好不得 reopen。`X` 只由同 revision 的新 attempt correction/refreeze 离开；旧 attempt 明确 invalidated/disposed，不能直接跃迁到 semantic 状态。confirmed target repair 产生 successor 后由 successor 重跑 gate。 |
| surface task | `queued → running → terminal`；零项由 coordinator 追加绑定 zero artifact 的 `zero/no-dispatch` edge，跳过 `RUNNING` 但仍为 terminal，非零项必须产生完整 screen handoff 后为 `terminal`。transport、缺文件或超限为 `retryable`，归档旧 attempt 后 fresh retry；输入／候选漂移为 `stale`，必须 refreeze 后重跑；不能把 child 结束当 terminal 成功。raw surface 输出严格且恰好只能是 `OK|ISSUE`；`selected|deferred` 是 ORCHESTRATOR 按冻结 policy 写入 `surface_handoff` 的 routing annotation，不能拼入或替代 raw result。raw `OK` 的 route-selected revision 才进入 deep，route-deferred revision 留在 ledger 待后续抽检，二者都不能把条目声明为 deep-reviewed；raw `ISSUE` 必须进入 deep。`retryable` 只可经 fresh retry 回到 `queued`，`stale` 只可经 refreeze 回到 `queued`。 |
| deep task | `queued → running → terminal`；零项由 coordinator 追加绑定 zero artifact 的 zero edge，跳过 `RUNNING` 但仅在完整 deep workset 为空时 terminal，非零项必须产生完整 deep handoff 后为 `terminal`。transport、缺文件或超限为 `retryable`，候选／输入漂移为 `stale`，只可经 refreeze 回到 `queued`；`retryable` 只可经 fresh retry 回到 `queued`；逐项结果为 `OK|issue`，但 `OK` 只表示 deep 结果完成，不替代 finding adjudication。 |
| finding | `observed → refuted|advisory|pending|confirmed`；`pending` 必须保留为 pending，并由 ORCHESTRATOR 在补足证据后执行 re-adjudication，再转为其他 finding terminal；不得自动修复；`confirmed → fixed|no_fix_closed`，二者均须源码／语境证据、裁决记录和 revalidation；已 closed 只有新的 fidelity/completeness/grammar/terminology/runtime/明显 translationese 证据才 `reopened → confirmed`，偏好不 reopen；不可调和冲突或身份无法确认进入 `WAIT_USER`。 |
| repair task | 非零项为 `queued → running → revalidated → terminal → closed`，且须先原子发布 result marker 与 transition group 才能 terminal。零 confirmed 项不走 `RUNNING`，而在 plan/result zero artifacts、marker 与空 transition group 原子发布并验证后，严格走 coordinator/task chain `ADJUDICATED → REVALIDATED → REPAIR_TERMINAL → CLOSED`；zero plan/result 必须绑定这三个 edge 和同一 attempt。失败为 `retryable`，归档旧 attempt 后 fresh retry 回到 `queued`；输入漂移为 `stale`，需重新冻结并回到 `queued`；达到 max_cycles、身份无法确认或不可调和冲突为 `WAIT_USER`。 |

`DONE` 只有同时满足：surface、deep、repair 三 task 各自已到 terminal；三者的不可变 handoff
已由 ORCHESTRATOR 发布并逐项相容；ledger、阶段状态、review records、冻结输入和最新门禁
一致；repair workset 的所有 revision 均已处理。surface raw `OK` 加 route-deferred annotation 不是 deep terminal
的替代，route-deferred 条目不计入 deep-reviewed；deep 的 zero/no-dispatch 只在 deep workset 确实为
零时成立。每批必须有 closure 检查未解决 finding、依赖和 invalidation。

final full 有两层且都必须成功：(a) **deterministic final full** 的唯一最终覆盖集合严格为
`F ⊎ U`（非仅 changed）；(b) **semantic final full** 的唯一 revision 集合严格为
`(D \ P_fixed) ⊎ F`。设 `P_fixed` 为因 repair 产生 successor、因而被替换的 parent revisions，`F` 为其
一一对应的 successor revisions；同一 `P_fixed` parent 可以同时含 fixed 与 `no_fix_closed`
finding，其中 no-fix finding 仍须逐 finding 闭环，但不把该 parent 放入 `U`。`U` 只含没有
successor、至少含一个 confirmed finding，且其全部 confirmed findings 均为 `no_fix_closed` 的 parent revisions；
`repair_workset = P_fixed ⊎ U`，最终 repair revision set 严格为 `F ⊎ U`，且映射
`P_fixed ↔ F` 是双射，`P_fixed`、`F`、`U` 两两按 revision identity 不交。原冻结 `D` 及其 context hash `K` 只读保留为 provenance；semantic final
以 successor identity 替换 `P_fixed` 后，必须对 `(D \ P_fixed) ⊎ F` 重算 dependency routing 和
非 entry-revision context/evidence closure/hash，不能沿用 parent 的闭包或历史成功。原 repair input
`P_fixed ⊎ U` 由 repair-plan/input-integrity preflight 核验；其中仅 `P_fixed` parent 不计入
deterministic final-full coverage，`U` 保留在该覆盖集合 `F ⊎ U` 中。`STATE.cycle` 的最新 stage
必须唯一且是
该 cycle 最大 `(cycle,attempt)` 的成功 `FINAL_REVIEW/full`；旧 cycle 成功或另一个 stage 不能
满足 DONE。final 失败只能进入更高 cycle 的 `RE_REVIEW/full|closure` 修复序列后重做 final full。

### 4.1 三任务 immutable handoff 与 batch coordinator（待实施）

一个 `batch_id` 对应一个只增不改的 coordinator record，绑定 catalog/policy epoch、batch-selected
revision 集合、三 task identity、attempt、各 handoff hash、journal transition group、门禁和
状态。非零路径为 `PLANNED → RESERVED → SURFACE_RUNNING → SURFACE_TERMINAL → DEEP_RUNNING →
DEEP_TERMINAL → ADJUDICATED → REPAIR_RUNNING → REVALIDATED → REPAIR_TERMINAL → CLOSED →
DONE_VERIFIED`，并有 `RETRYABLE|STALE|WAIT_USER|ROLLED_BACK` 分支。非零 repair 只有在
`repair_result_handoff` marker 与对应 ledger/journal transition group 原子发布、replay 验证成功后
才进入 `REPAIR_TERMINAL`，closure 守恒通过后才进入 `CLOSED`；`DONE_VERIFIED` 只能从
`CLOSED` 前进。零项不得为了形式经过 running：当且仅当 `surface_input` 为空，追加绑定 surface
zero artifact 的 `RESERVED → SURFACE_TERMINAL`；当且仅当完整 deep workset `D` 为空，追加绑定
deep zero artifact 的 `SURFACE_TERMINAL → DEEP_TERMINAL`，且 `surface_handoff.required_H` 非空时禁止该
edge；当且仅当 confirmed repair workset
为空，仍须先原子发布并验证 repair plan zero artifact、repair result zero artifact、marker 与空
transition group，才可严格追加 `ADJUDICATED → REVALIDATED → REPAIR_TERMINAL → CLOSED`；
plan/result zero artifacts 绑定同一 batch/task/attempt 和这三个 edge。不得省略 `REVALIDATED` 或
用 terminal 反推 revalidation。这些都是显式 coordinator edges。
`X` 非空或存在无 disposition 的 `I` 时禁止任何 zero edge。状态只能由 ORCHESTRATOR 在验证前序
artifact 后追加；child 退出、部分 lane/segment 完成或 view 中显示 closed 均不能推进 coordinator。

跨任务发布四种不同的 immutable handoff，不能共用或覆写：

1. `surface_handoff`：完整 batch-selected revisions、draft hash（含 ordered `S` hash/cutoff/policy identity）、四 lane/zero/full 结果和 ordered coordinator queue carry-over。其分类 schema 必须枚举且仅按 §2.1 含 `X=deterministic_failed`、`I=invalidated`、`T=mandatory_deep_observation`、`A=surface_input`，每个 `I` 必须有恰一个 `successor|requeue|tombstone` disposition；raw results section 的每项 result 字段恰为 `OK|ISSUE`。ORCHESTRATOR 计算的 `selected|deferred` 及 dependency `Q→O` override 必须位于与 raw results 分离的 sibling routing mapping/section，以 revision identity 关联；同一 artifact body 还必须包含按 revision identity 和原依赖边排序、可重放的 `required_H` directive 及其 directive identity/SHA-256。`required_H` 的 schema 恰好且只允许冻结 `S` 中将吸收到 `H` 的外部 entry dependencies，排除同批保留在 `O/J/T` 的依赖和同批 `Q→O` override；禁止把 routing 当 raw item extra field、拼接进 raw result，或把 batch-selected 与 route-selected 混称；
2. `deep_handoff`：绑定该 batch-owned 的完整 revision workset `D`、独立 context/evidence closure `K` 的 canonical hash、`deep_done_segments` 与 `deep_pending_segments`。同一 artifact body 必须新增一个 section，保存绑定 producer `surface_handoff.required_H` directive identity/SHA-256 的 ordered required-H consumption mapping；每项记录 required dependency identity、原依赖边、来源状态与最终 `H` bucket。来源为 `sampling_queued` 的项必须同时记录实际 `sampling_queued → deep_queued` ledger transition group identity 与 ownership acquire group identity；来源已是 `deep_queued` 的项只记录实际 ownership acquire group identity，不得伪造 ledger self-transition。该 mapping 的 ordered identity projection 定义为 `required_H_consumed`。该 section 是既有 `deep_handoff` 正文的一部分，不是新 artifact 或 handoff。它不允许未派发 carry-over；所有 pending 必须在同一 batch drain 并逐项出结果后才能 terminal。先前 `sampling_queued` revision 若在未来 batch 提升，可作为该未来 batch 的 deep handoff 输入，但其 `deep_handoff` artifact body 中 promotion provenance section 必须明列 `origin_batch_id`、origin ordinal、origin policy hash、origin decision hash 与提升原因；这些 origin metadata 不属于 ledger provenance record，现行 ledger provenance record 仍严格为 `{kind, sha256}`；
3. `repair_plan_handoff`：逐 finding 裁决 provenance、仅 confirmed 的 repair workset、parent identity、预期 successor 映射和 revalidation/final-full 要求；它是 immutable 输入计划，不包含执行结果。
4. `repair_result_handoff`：绑定且仅绑定一个 `repair_plan_handoff`，逐项记录 fixed/no-fix result、实际 parent→successor 映射、no-fix 理由、revalidation 与 final-full 结果；repair terminal 只有在该 handoff 发布且 publication event 成功后成立。`repair_handoff` 不是两者的别名；repair terminal/publication 必须分别可重放核验。

**兼容边界：**现行 append-only ledger 的 provenance kind 是九项闭集：
`deterministic_layer`、`surface_handoff`、`deep_handoff`、legacy `repair_handoff`、
`adjudication_record`、`revalidation_record`、`revision_freeze_record`、`reopen_evidence_record`、
`identity_snapshot`；其中没有 `repair_plan_handoff` 或 `repair_result_handoff`，且
`adjudication → fixed` 使用 legacy `repair_handoff` 是已实现迁移。后续迁移工作包只需新增后两种
schema/kind、canonical encoding、publication marker、validator 及相关 writer version gate，并提供
legacy `repair_handoff` 历史记录的只读 replay/查询兼容。迁移和门禁落地前，生产 writer 禁止发出
两个新 kind；legacy `repair_handoff` 只读保留，不回写、拆分或冒充新 plan/result。另行待实施的
`T` deterministic-observation provenance/migration 不属于这两种 repair kind，必须在其自己的后续
工作包中显式加入闭集、transition policy 与 writer gate。

四者共同使用含 schema/version、batch/task/attempt、ordered revision identity、输入 snapshot、policy/source/terminology identity、producer role、结果正文 hash、时间和 parent handoff hash 的外壳；正文 canonical bytes 与 manifest 分开 hash。发布采用 content-addressed artifact 先落盘、校验 bytes/hash/manifest 后，最后以单一原子 commit marker/event 同时公布 artifact set 的语义；marker 固定 ordinal、artifact hash/size、schema、parent、batch/task/attempt、creation order 和 fsync result。artifact 及其目录 fsync 后才能写 marker，再 fsync marker 所在目录；replay 只接受唯一、完整且 hash 匹配的 marker，孤儿 artifact 忽略；marker 缺任一 artifact、重复 ordinal、hash/size 不符或 marker 不完整则 fail closed。具体路径和 validator 尚待实现。下游
preflight 重算正文 hash、集合/顺序、parent、task purpose/role 和 attempt；对 required-H 还须由 producer
`surface_handoff` 重算 directive identity/SHA-256 和 ordered consumption mapping。preflight 与 replay
都必须机械验证 `required_H_consumed == surface_handoff.required_H`（ordered identity 相等）、
`required_H_consumed ⊆ H`、`required_H_consumed ∩ R == ∅`，任一不符即拒绝。
后来的修正必须生成新 attempt 和新 handoff，旧 bytes 永久只读。

零项是有证据的 terminal，不是缺记录：surface zero 只按 `A=surface_input` 是否为空判定，与
batch-selected revision 数无关；deep zero 当且仅当已冻结的 entry-revision workset
`D = O ⊎ J ⊎ T ⊎ H` 为空（`K` 是单独 hash 的非 revision context，不参与判空），且
`surface_handoff.required_H` 非空时即使其他分区为空也禁止 deep zero edge；repair zero
仅当所有 deep issue（包括 `T` observation）均完成裁决且 confirmed 集合为零。每种 zero handoff
仍须绑定输入并给出空集合 hash，
coordinator 通过上述显式 zero bypass edge 逐 stage 前进。若 batch 含 raw `OK` 加 route-deferred annotation，本 batch 可以在该 revision 仍为
`sampling_queued` 时闭合，但 batch 报告必须显示 deferred 数且不能把它们计作 deep terminal。

完整 `DONE_VERIFIED` 还要求：coordinator 最新 attempt 唯一；四 handoff 链和 queue journal 可
replay；batch-selected、queue carry-over、surface、deep、confirmed、successor 与 closed 集合做
分层集合守恒核对；`X = ∅`，且 `I` 每项都有且仅有一个已发布
`successor|requeue|tombstone` disposition；无未决的 batch-owned finding/dependency；当前输入的
两层 final full 与所有适用门禁成功；coverage 报告使用同一 catalog/policy epoch。对每个 batch，
设 `E` 为本批 surface eligible revisions，`B` 为 batch-selected revisions，`C` 为 queue
carry-over，`X` 为仅 construction/extraction/input-shape 的 deterministic-failed，`I` 为
invalidated，`T` 为 mandatory-deep target-content observation，`A` 为 `surface_input`，`O` 为
raw `OK` 且 route-selected（含 normalization 的 `Q→O` override），`Q` 为 raw `OK` 且仍
route-deferred 的 `sampling_queued`，`J` 为 raw `ISSUE`。另设 `S` 为 draft 按 canonical
hash/journal cutoff/eligibility policy identity 冻结的 ordered promotion pool，`H` 为按冻结
policy/score/origin ordinal 稳定 cadence 提升并吸收冻结 required entry dependency 的 deep-only
revisions，`R = S \ H` 为未提升 pool remainder（只使用 coordinator-only `pool_remainder`
标记，且该标记不是 ledger reason）；
`S∩B=∅`，故 `H` 与 `B` 不交。`K` 专指
non-entry-revision context/evidence closure，按固定 canonical recipe 单独 hash，不属于 revision
集合或 ledger transition。`D` 是完整 entry-revision deep workset，则分层等式严格为：

- `E = B ⊎ C`；
- `B = X ⊎ I ⊎ T ⊎ A`；
- `A = O ⊎ Q ⊎ J`；
- `S = H ⊎ R`；
- `required_H_consumed == surface_handoff.required_H`（ordered identity equality）；
- `required_H_consumed ⊆ H`；
- `required_H_consumed ∩ R == ∅`；
- `D = O ⊎ J ⊎ T ⊎ H`；
- `D = deep_done_segments ⊎ deep_pending_segments`。

每个 `⊎` 都表示该边界按 entry-revision identity 互斥且无遗漏；dependency normalization 必须在
surface freeze 前优先保留同批 `O/J/T`，只将同批 `Q` 转入 `O`，并只将冻结 `S` 中来源为合法
`sampling_queued` 或已 `deep_queued` 的外部 dependency 纳入 `H`；其余 fail closed，不能落入
`K`，也不能从 `screened` 直达 deep。`Q` 不计入
`D` 或 `deep_done_segments`；`H` 直接从冻结 sampling pool（及具合法来源/provenance 的等价外部
依赖）提升，不重过 `A`。`T` 归 `D` 且必须完成 deep/adjudication，不能自动确认。deep zero 当且
仅当 `D = ∅` 且 `surface_handoff.required_H = ∅`；`required_H` 非空时禁止 deep zero edge。reservation
acquire/release 是 queue ownership event，不是 `E` 的条目类别；release 后的 revision 只有在未来
batch 重新成为 eligible 才进入该批等式。fixed parent→successor 不混入以上漏斗分区，而按
repair/final 等式另行核对：`P_fixed` 以 parent 因 repair 产生 successor 为准；`U` 只含无 successor、至少含一个 confirmed finding，且
全部 confirmed findings 均为 `no_fix_closed` 的 parent。同一 `P_fixed` parent 上的 no-fix finding
仍逐 finding 闭环且不进入 `U`。`repair_workset = P_fixed ⊎ U`，最终 repair revision set
`= F ⊎ U`，且 `P_fixed ↔ F` 一一对应；semantic final revision set 唯一为
`(D \ P_fixed) ⊎ F`，并按 successor identities 重算 dependency routing 和 `K` hash，原 `D/K`
只读保留为 provenance。任何不满足等式的 batch fail closed。它只证明该 batch
的声明边界，不证明 backlog 已深审完。
这些 coordinator/handoff validator 与三任务级 `DONE_VERIFIED` **尚未实现**；当前 surface v1
的 terminal/DONE 语义保持原样，不能被本节文字推定升级。

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

### 5.1 覆盖、质量、吞吐与队列指标

每份报告必须绑定 catalog snapshot、policy epoch、截止 journal event、batch/attempt 和生成查询
版本。覆盖按 **entry-revision** 去重，同时另报 logical entry 数；跨 snapshot 趋势不得把失效
revision 当成当前覆盖。至少分开报告以下互斥或明确可重叠的量，禁止只给一个“审核率”：

- `deterministic_pass / catalog_eligible`，另列 failed、excluded、invalidated；
- `surface_terminal / deterministic_pass`，另列 raw `OK` 中 route-selected、raw `OK` 中 route-deferred、raw `ISSUE` 和 queue carry-over；
- `deep_terminal / catalog_eligible` 与各 stratum 的 `deep_terminal / stratum_N`，明确其中强制与
  概率样本；
- `repaired_revalidated / confirmed_repair_required`、`no_fix_closed / confirmed`；
- `closed_after_deep / catalog_eligible`，绝不包含仅 deterministic、surface OK 或未抽中的条目。

质量观测至少包括：surface issue 的 confirmed/advisory/refuted/pending 比率；分层独立 deep
样本中的 false-negative 发现数和率（分母为实际 deep 样本，附 N/n，样本不足报不可估）；finding
确认率；reopen 率；新 revision 在后续 final/review 失败导致的返工率。它们是观测指标而非未抽样
总体的保证，不把 model 自报置信度当证据。

吞吐/成本按 stage 同时报实际 wall time、维护者 active time、child attempts、fresh retry、处理
revision 数、deep 完成数、confirmed 修复数、SCOUT 调用及可取得的 token/计费；provider/model
只作为标签。报告 median/p90 前必须有样本量，否则列原始值。队列健康至少报告 queued/reservation-owned（queue annotation）/
sampling_queued/pending/confirmed-waiting-repair/carry-over、最老队龄、到达率、各 stage 完成率、
WIP、stale/retry 率和 backlog burn-down；burn-down 以 snapshot 新增/失效分开解释，不能用关闭旧
revision 掩盖新积压。预算触顶只触发 backpressure/人工决策，不得降低证据门槛。

### 5.2 pilot、扩容、常态运行与回滚

上线按 policy epoch 渐进推进，所有阈值在 epoch 开始前写入准入记录，不在运行中追着结果改。准入记录还必须固定 batch cadence、每 batch 的 80-item surface horizon、catalog scope（`full_catalog` 或 `risk_prioritized_subset`）以及 subset 的 stopping rule（达到 80、队列耗尽或明确风险覆盖条件，含实际停止证明）；未写明这些字段不得宣称全 catalog 收敛：

1. **shadow/dry-run**：只生成 catalog、replay queue、风险/抽样决策和 batch manifests，不 dispatch；
   要求重复生成 bytes 一致、集合守恒、旧 surface/v1/v2 fixture 与现行门禁不变。
2. **pilot**：选择一个预先冻结的小 catalog slice，采用最低并发，完整走 surface→deep→repair
   和恢复演练；要求 handoff/preflight、zero/carry-over、invalidation、fresh retry、指标分母和
   `DONE_VERIFIED` 均可重算，且无静默丢条。
3. **扩容**：一次只提高一个冻结维度（slice、lane、deep segment 或 sampling rate），至少完成
   一个无未决 batch 的 epoch 后再评估；准入要求门禁全绿、WIP/队龄未越界、抽检分母足够且无
   未处置漏报 backsweep、成本在预设预算内。
4. **常态**：仍保持单维护者有界 WIP、epoch 冻结、周期抽检和定期 offline replay；连续批次只
   自动选择已被 policy 完全定义的下一 slice，不能自动改 policy 或扩并发。

任一阶段出现 hash/replay/集合守恒失败、错误覆盖声明、handoff 原子性无法证明、重复 owner、
门禁回归、漏报触及未评估 stratum、WIP/成本越界或 `AGENTS.md` 停止条件，即停止领取新 batch。
回滚是追加 `ROLLED_BACK`/失效事件、恢复上一个已验证 policy 和并发上限，并 drain 或 stale/refreeze
现有 batch；不得删除 journal/handoff、覆写结果或把新 policy 下的完成偷渡到旧 epoch。若 schema
不向后兼容，保留新 catalog 为只读并从最后一个可 replay checkpoint 重建新 revision 队列。
涉及已写译文的 repair 不做破坏性 git reset：按正常新 revision/新 repair 提交反向修复并重新
门禁。无法证明安全回退边界时进入 `WAIT_USER`。

## 6. 实施状态、后续工作包与验收

| 工作包 | 当前状态 | 仍待实施 |
|---|---|---|
| 1. 身份/surface ledger | surface v1 已实现双 identity 重算、canonical SHA-256、append-only 迁移验证、失效/reopen 规则和状态门禁 | 生产旧 ledger 迁移、碰撞处置报告与长期指标审计 |
| 2. catalog/queue | 无生产 backlog catalog、权威 snapshot、全局 transition journal 或可重建 queue view | 冻结受跟踪 schema/path、生成/replay/reconciliation validator、稳定选批与恢复探针 |
| 3. 确定性筛查 | 现行 surface manifest 已实现稳定排序、q/r 四 lane、zero/full 与 legacy surface carry-over 的无静默丢条验证；这不是本文 coordinator queue `C` | 全量生产规则、风险 feature、真实 catalog/batch draft freeze 及 coordinator `C` 的 schema/journal/validator |
| 4. 风险/抽检/容量 | 本文仅定义 policy epoch、强制 deep、稳定分层抽样和单维护者 WIP/backpressure | policy artifact/离线 replay、冷启动 pilot、feedback/backsweep、容量与队列健康门禁 |
| 5. surface/deep 编排 | `translation_surface_screen_v1` review-only pilot、整组发布、fresh retry、provenance 和 surface 范围的 `DONE_VERIFIED` 已实现 | 16–32 deep segment、按需 context、SCOUT 压缩和 deep handoff/terminal |
| 6. 筛查—裁决—修复 | surface observation 已明确不能直接关闭 finding 或宣称 deep-reviewed；现行 ledger provenance 是含 legacy `repair_handoff`、不含 plan/result 的九项闭集，并已实现 `adjudication → fixed` | batch coordinator、完整三任务 DAG；新增 `repair_plan_handoff`/`repair_result_handoff` schema、validator、marker 与相关 writer version gate，legacy `repair_handoff` 只读兼容；另增 `T` deterministic-observation provenance/migration/writer gate；repair closure/reopen/final full 与原子发布 |
| 7. 指标/门禁/上线 | surface/ledger 工具、契约检查、回归测试和 `ai_state_check.py` 接口已实现 | 诚实覆盖与成本/质量/队列报告、三任务级 `DONE_VERIFIED`、shadow→pilot→扩容→常态及回滚演练 |

已实施的 surface pilot 必须继续证明旧 v1/v2 fixture 不变、完整输入无静默丢条、
identity/快照可重算、screen 不直接关闭 finding、live-profile 可路由，并通过契约检查、
相关测试、适用门禁和 `git diff --check`。剩余工作包在后续任务中还必须额外证明：
accepted 结果可由固定源码重算，deep/repair 集合和依赖无静默丢失，且只有当前输入的
最新成功 final full 才能闭合完整三任务 `DONE_VERIFIED`。
